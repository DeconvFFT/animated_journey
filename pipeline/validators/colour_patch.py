#!/usr/bin/env python3
"""colour_patch.py: the colour-patch test (W-16). Standard library only. Needs ffmpeg (ffprobe is optional).

WHAT IT PROVES. Colour tags are not evidence: a BT.601 matrix under BT.709 tags passes every tag check (research Q-F1).
So this tool looks at PIXELS. It builds one 1920x1080 frame of three flat vertical patches, pure red (255,0,0), 50 percent
grey (128,128,128) and a skin tone (224,172,140), encodes 2 frames of it through each named chain (the chain's own video
arguments from pipeline/lib/chains.json), decodes the file back to RGB with
    scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24
and reports, per patch, the difference to the source out of 255.
THE MEASUREMENT IS MADE AT THE CHAIN'S OUTPUT SIZE: the colour conversion above runs on the decoded picture at whatever size the
chain produced (a 1280x720 phone copy is converted at 1280x720), and only then is the RGB picture stretched back to 1920x1080 by
nearest-neighbour (scale=1920:1080:flags=neighbor, which copies pixels and changes no value) so the same patch boxes can be read.
A chain whose output is 1920x1080 is read exactly as before (that last step does nothing). A chain PASSES when its worst per-channel error is 3 or
less (W-16, tolerance +-3/255). Run it once for every command-line template and again on every ffmpeg build: the container's
6.1.1 and the winget 9.0.2 build gave different pixels under identical tags.

NEGATIVE CONTROLS (built in, always run with --all or --controls). They are the encodes that went wrong in Q-F1:
  control_h264_format_first_A    format=yuv420p before scale (about 5/255 on every build measured): expected to FAIL
  control_h264_bare_pix_fmt      bare -pix_fmt yuv420p plus tags (about 23 on ffmpeg 6.1.1, about 1 from 7.1): build dependent
  control_prores4444_bare        bare -pix_fmt yuva444p10le plus tags (about 25 on 6.1.1, about 0 on 9.0.2): build dependent
and two that test the tool itself, on any build:
  control_h264_scale_first_B     scale first (about 1): must PASS
  control_wrong_matrix_bt601     deliberately encoded with the BT.601 matrix: must FAIL (if it passes, the tool is broken)
A control that behaves as the trap predicts shows "TRAP PRESENT" for the build: that is information, not a failure.

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows; no admin rights; nothing is installed or downloaded)
  python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json OUT.json
  python3 -I pipeline/validators/colour_patch.py --chain h264_venue                 one chain from the default chain file
  python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080
  py -3 -I pipeline\\validators\\colour_patch.py --ffmpeg C:\\Tools\\ffmpeg\\bin\\ffmpeg.exe --all --json %TEMP%\\colour_patch_pc.json
  python3 -I pipeline/validators/colour_patch.py --derive-from RAW.json --out DERIVED.json    the FILED form (see below)
  python3 -I pipeline/validators/colour_patch.py --selftest                                   needs only ffmpeg
  Options: --ffmpeg PATH (also honours the FFMPEG environment variable), --ffprobe PATH (FFPROBE; default: beside ffmpeg),
           --chain NAME (repeatable), --chain-file F (default pipeline/lib/chains.json), --all, --controls, --tolerance N (3),
           --keep-dir DIR (keep the encoded 2-frame files, for looking at), --json OUT.json (the RAW record), --quiet

THE RAW JSON AND THE DERIVED FORM (build plan 4.4 and 4.16). The raw file (--json) records the ffmpeg version line, the build
configure flags and the SHA-256 of the ffmpeg binary, plus every chain result. The configure flags of a build someone compiled
can contain folder names, so on the maker's PC the raw file is READ BY THE MAKER AND PASTED IN CHAT ONLY: it is never copied
into the project folder, never committed, never filed. The orchestrator then runs --derive-from on the pasted text (saved as a
scratch file outside the repo) and files only the derived result: ffmpeg version number, binary SHA-256, chain names, worst
errors and pass flags (schema lj-pc-chains/1, pipeline/validators/pc_chains.schema.json). The derived writer builds its output
from a fixed list of fields, keeps only the leading version number of the version line, and refuses to write anything else.
The binary's path is never recorded in either form; console output shows the file name of --json only.

WHAT IT TOUCHES. It runs the ffmpeg you name (and ffprobe if found), writes only inside a new temporary folder (deleted at the
end) and the one file named by --json / --out. It never reads personal media, never uses the network, never changes settings.

RESULT LINES. "RESULT chains: N of M within 3/255; ABOVE TOLERANCE: ..." names chains that were measured and are too far off. A chain
that could not be encoded or decoded at all has its OWN line, "RESULT chains: could not be measured (encode/decode error): ...", with
the reason in the chain's ERROR line above: that is a tool or chain-definition problem, not a colour problem. Both end in exit 1.

EXIT CODES (build plan 4.3)  0 every real chain passed (controls are information) and the tool's own controls behaved
  1 a chain is above the tolerance, could not be measured (encode or decode error), is marked approved:true in the chain file while
  measuring above the tolerance, or a tool control misbehaved   2 bad usage or invalid input
  3 environment problem (ffmpeg not found / not runnable)

UNVERIFIED on Windows and on ffmpeg 9.0.2 until the maker runs it (WP-09's runner). Verified on ffmpeg 6.1.1 (Linux) only.
"""
import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

TOOL_VERSION = 1
TOLERANCE = 3
W, H, FPS = 1920, 1080, 24
PATCH_W = W // 3
# name, source RGB, source alpha (alpha chains only: straight alpha, so the colour must not depend on it; the alpha values
# 255 / 200 / 128 let the alpha read-back show that the alpha plane really survived)
PATCHES = [("red", (255, 0, 0), 255), ("grey50", (128, 128, 128), 200), ("skin", (224, 172, 140), 128)]
BOX = 100          # half-size of the square read at the centre of each patch (a 200 x 200 block)
DECODE_VF = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
DECODE_VF_ACCURATE = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb24"
# After the colour conversion (done at the chain's own output size) the RGB picture is stretched to the 1920x1080 patch grid by
# nearest-neighbour, which copies pixels: flat patches keep their exact values, and a 1920x1080 chain is passed through unchanged.
READBACK_VF = "scale=%d:%d:flags=neighbor" % (W, H)
SETPARAMS = "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
EXT = {"mp4": ".mp4", "mov": ".mov", "mkv": ".mkv", "matroska": ".mkv"}
RAW_SCHEMA = "lj-colour-patch/1"
DERIVED_SCHEMA = "lj-pc-chains/1"
NAME_RX = re.compile(r"^[A-Za-z0-9_.-]{1,60}$")
SHA_RX = re.compile(r"^[0-9a-f]{64}$")
VERSION_RX = re.compile(r"^(?:[0-9]+(?:\.[0-9]+){1,3}|N-[0-9]+-g[0-9a-f]{7,12})$")

# Built-in controls. expect: "pass" / "fail" are enforced on every build (they test the tool); None = build dependent (information).
CONTROLS = [
    {"name": "control_h264_scale_first_B", "container": "mp4", "alpha": False, "expect_result": "pass",
     "vf": "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
     "video_args": ["-c:v", "libx264", "-crf", "18"] + TAGS,
     "notes": "Q-F1 chain B: scale first. Must pass on every build (about 1/255)."},
    {"name": "control_h264_format_first_A", "container": "mp4", "alpha": False, "expect_result": None,
     "vf": "format=yuv420p,scale=out_color_matrix=bt709:out_range=tv",
     "video_args": ["-c:v", "libx264", "-crf", "18"] + TAGS,
     "notes": "Q-F1 chain A: format before scale converts twice (5/255 on 6.1.1, 7.1.1, 8.1.2 and 9.0.2)."},
    {"name": "control_h264_bare_pix_fmt", "container": "mp4", "alpha": False, "expect_result": None,
     "vf": "",
     "video_args": ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p"] + TAGS,
     "notes": "Bare -pix_fmt: BT.601 pixels under BT.709 tags on 6.1.1 (about 23); BT.709 from 7.1 (about 1). Tags pass either way."},
    {"name": "control_prores4444_bare", "container": "mov", "alpha": True, "expect_result": None,
     "vf": "",
     "video_args": ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"] + TAGS,
     "notes": "Bare -pix_fmt yuva444p10le: BT.601 pixels on 6.1.1 (about 25); correct on 9.0.2."},
    {"name": "control_wrong_matrix_bt601", "container": "mkv", "alpha": False, "expect_result": "fail",
     "vf": "scale=out_color_matrix=bt601:out_range=tv,format=yuv444p10le," + SETPARAMS,
     "video_args": ["-c:v", "ffv1"],
     "notes": "Deliberately BT.601 under BT.709 tags, lossless 4:4:4. Must fail on every build: if it passes, this tool is broken."},
    {"name": "control_lossless_709", "container": "mkv", "alpha": False, "expect_result": "pass",
     "vf": "scale=out_color_matrix=bt709:out_range=tv,format=yuv444p10le," + SETPARAMS,
     "video_args": ["-c:v", "ffv1"],
     "notes": "Lossless 4:4:4 with the BT.709 matrix. Must pass on every build; it needs no x264 or ProRes encoder (self-test)."},
]


class EnvError(Exception):
    """ffmpeg is missing or cannot run (exit 3)."""


class Usage(Exception):
    """Bad command line or invalid input (exit 2)."""


# ----------------------------------------------------------------------------------------------- small helpers
def say(msg=""):
    print(msg)
    sys.stdout.flush()


def read_text_any(path):
    """Read UTF-8, UTF-8 with BOM, or UTF-16 (what 'command > file' writes in Windows PowerShell 5.1)."""
    with open(path, "rb") as f:
        b = f.read()
    if b.startswith(b"\xef\xbb\xbf"):
        return b[3:].decode("utf-8")
    if b.startswith(b"\xff\xfe") or b.startswith(b"\xfe\xff"):
        return b.decode("utf-16")
    return b.decode("utf-8")


def write_json(path, obj):
    """BOM-less UTF-8, LF line ends, written to a sibling temp file and renamed."""
    text = json.dumps(obj, indent=2, sort_keys=False, ensure_ascii=True) + "\n"
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def resolve_exe(name):
    """Return the full path of an executable given a name or a path, or None."""
    if not name:
        return None
    if os.path.sep in name or (os.path.altsep and os.path.altsep in name) or os.path.isabs(name):
        return name if os.path.isfile(name) else None
    return shutil.which(name)


def ffprobe_for(ffmpeg, explicit=None):
    cand = explicit or os.environ.get("FFPROBE")
    if cand:
        return resolve_exe(cand)
    exe = resolve_exe(ffmpeg)
    if exe:
        d, b = os.path.split(exe)
        if b.lower().startswith("ffmpeg"):
            sib = os.path.join(d, "ffprobe" + b[len("ffmpeg"):])
            if os.path.isfile(sib):
                return sib
    return shutil.which("ffprobe")


def run(cmd, data=None, timeout=300):
    try:
        p = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except FileNotFoundError:
        raise EnvError("cannot run %s (not found)" % os.path.basename(str(cmd[0])))
    except subprocess.TimeoutExpired:
        return 124, b"", b"timed out"
    except OSError as e:
        raise EnvError("cannot run %s (%s)" % (os.path.basename(str(cmd[0])), e.__class__.__name__))
    return p.returncode, p.stdout, p.stderr


def first_lines(b, n=3, work=None):
    s = b.decode("utf-8", "replace").strip().splitlines()[:n]
    out = " | ".join(x.strip() for x in s)
    out = re.sub(r"@ 0x[0-9a-fA-F]+", "", out)        # ffmpeg heap addresses: not identifying, but they make the record differ run to run
    if work:
        out = out.replace(work, "<tmp>")
    return out[:300]


def binary_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def ffmpeg_info(ffmpeg):
    """version_line, version (leading token), configure flags list, sha256 of the binary. No path."""
    exe = resolve_exe(ffmpeg)
    if not exe:
        raise EnvError("ffmpeg not found (%s). Pass --ffmpeg PATH or set FFMPEG." % os.path.basename(str(ffmpeg)))
    rc, out, err = run([exe, "-hide_banner", "-version"], timeout=60)
    text = out.decode("utf-8", "replace")
    if rc != 0 or not text.lower().startswith("ffmpeg version"):
        raise EnvError("%s did not answer -version like ffmpeg" % os.path.basename(exe))
    lines = text.splitlines()
    version_line = lines[0].strip()
    token = version_line.split()[2] if len(version_line.split()) > 2 else ""
    conf = []
    for ln in lines:
        if ln.startswith("configuration:"):
            conf = ln[len("configuration:"):].split()
    return {"version_line": version_line, "version": token, "configure": conf, "sha256": binary_sha256(exe), "_exe": exe}


def short_version(token):
    """The leading version number only: 6.1.1-3ubuntu5 -> 6.1.1 ; 9.0.2-essentials_build-... -> 9.0.2 ; N-123-gabcdef0-... -> N-123-gabcdef0."""
    m = re.match(r"^n?([0-9]+(?:\.[0-9]+){1,3})", token)
    if m:
        return m.group(1)
    m = re.match(r"^(N-[0-9]+-g[0-9a-f]{7,12})", token)
    if m:
        return m.group(1)
    return None


# ----------------------------------------------------------------------------------------------- the test frame
def make_frame(alpha):
    """One 1920x1080 frame, three flat vertical patches, as raw rgb24 (or rgba)."""
    rows = []
    for _name, rgb, a in PATCHES:
        px = bytes(rgb) + (bytes([a]) if alpha else b"")
        rows.append(px * PATCH_W)
    row = b"".join(rows)
    return row * H


def patch_box(i):
    cx = i * PATCH_W + PATCH_W // 2
    cy = H // 2
    return cx - BOX, cx + BOX, cy - BOX, cy + BOX


def read_patches(raw, channels):
    """Mean of the central block of each patch per channel -> list of (mean tuple, max abs pixel error vs source tuple)."""
    out = []
    stride = W * channels
    for i, (_n, rgb, _a) in enumerate(PATCHES):
        x0, x1, y0, y1 = patch_box(i)
        sums = [0] * channels
        n = 0
        worst = 0
        for y in range(y0, y1, 4):                          # every 4th row is plenty for a flat patch
            base = y * stride
            seg = raw[base + x0 * channels: base + x1 * channels]
            for k in range(channels):
                col = seg[k::channels]
                sums[k] += sum(col)
                if k < 3:
                    ref = rgb[k]
                    mx = max(col)
                    mn = min(col)
                    worst = max(worst, abs(mx - ref), abs(mn - ref))
            n += x1 - x0
        out.append(([s / float(n) for s in sums], worst))
    return out


# ----------------------------------------------------------------------------------------------- one chain
def is_pass(worst_error, tolerance):
    """W-16: a chain passes when its worst per-channel error out of 255 is at most the tolerance."""
    return worst_error is not None and worst_error <= tolerance


def chain_is_alpha(ch):
    if "alpha" in ch:
        return bool(ch["alpha"])
    blob = str(ch.get("vf", "")) + " " + str((ch.get("expect") or {}).get("pix_fmt", ""))
    return bool(re.search(r"yuva|gbra|rgba|bgra|argb|abgr", blob))


def probe_stream(ffprobe, path):
    if not ffprobe:
        return None
    rc, out, err = run([ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=codec_name,profile,pix_fmt,width,height,color_range,color_space,color_primaries,color_transfer",
                        "-of", "json", path], timeout=60)
    if rc != 0:
        return None
    try:
        s = json.loads(out.decode("utf-8", "replace"))["streams"][0]
    except (ValueError, KeyError, IndexError):
        return None
    s.setdefault("color_range", "unknown")
    return s


def compare_expect(observed, expect, extra=None):
    """Compare ffprobe's view with the chain's expect block (plus expect_extra, which holds the profile); null / absent keys are not asserted."""
    if observed is None or not expect:
        return None, []
    expect = dict(expect)
    for k, v in (extra or {}).items():
        if expect.get(k) is None:
            expect[k] = v
    keymap = {"codec": "codec_name", "profile": "profile", "pix_fmt": "pix_fmt", "color_range": "color_range",
              "color_space": "color_space", "color_primaries": "color_primaries", "color_transfer": "color_transfer"}
    bad = []
    for k, probe_key in keymap.items():
        want = expect.get(k)
        if want is None:
            continue
        got = observed.get(probe_key)
        if str(got) != str(want):
            bad.append("%s: chain expects %s, file has %s" % (k, want, got))
    return (not bad), bad


def decode_first_frame(ffmpeg, path, vf, pix_fmt, channels):
    """First frame as raw RGB(A) on the 1920x1080 patch grid. The colour conversion in `vf` runs at the file's own size; READBACK_VF then
    stretches the result to 1920x1080 by nearest-neighbour, so a chain with a different output size (the 1280x720 phone copy) is measured too."""
    rc, out, err = run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", path, "-vf", vf + "," + READBACK_VF, "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", pix_fmt, "pipe:1"], timeout=120)
    if rc != 0 or len(out) != W * H * channels:
        return None, first_lines(err) or "decode gave %d bytes" % len(out)
    return out, ""


def measure(ffmpeg, ffprobe, chain, workdir, tolerance, keep_dir=None, kind="chain"):
    """Encode the 2-frame patch clip through one chain and read it back. Returns a result dict."""
    name = chain["name"]
    alpha = chain_is_alpha(chain)
    res = {"name": name, "kind": kind, "container": chain.get("container", "mp4"), "alpha": alpha,
           "encode_ok": False, "error": None, "patches": [], "worst_error": None, "pass": False,
           "worst_error_accurate": None, "max_pixel_error": None, "output_size": None, "tags": None, "tags_match_expect": None,
           "tag_mismatches": [], "alpha_error": None, "approved_in_file": chain.get("approved") if isinstance(chain.get("approved"), bool) else None}
    ext = EXT.get(res["container"], "." + str(res["container"]))
    out = os.path.join(workdir, "p_%s%s" % (re.sub(r"[^A-Za-z0-9_.-]", "_", name), ext))
    pf, ch = ("rgba", 4) if alpha else ("rgb24", 3)
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pf, "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "pipe:0", "-frames:v", "2"]
    if chain.get("vf"):
        cmd += ["-vf", chain["vf"]]
    cmd += [str(a) for a in chain.get("video_args", [])] + [out]
    frame = make_frame(alpha)
    rc, so, se = run(cmd, data=frame + frame, timeout=300)
    if rc != 0 or not os.path.isfile(out):
        res["error"] = "encode failed: " + first_lines(se, work=workdir)
        return res
    res["encode_ok"] = True
    raw, why = decode_first_frame(ffmpeg, out, DECODE_VF, "rgb24", 3)
    if raw is None:
        res["error"] = "decode failed: " + why
        return res
    worst = 0
    maxpix = 0
    for (name_p, rgb, _a), (mean, mpx) in zip(PATCHES, read_patches(raw, 3)):
        dec = [int(round(m)) for m in mean[:3]]
        err = [d - s for d, s in zip(dec, rgb)]
        worst = max(worst, max(abs(e) for e in err))
        maxpix = max(maxpix, mpx)
        res["patches"].append({"name": name_p, "source": list(rgb), "decoded": dec, "error": err})
    res["worst_error"] = worst
    res["max_pixel_error"] = maxpix
    res["pass"] = is_pass(worst, tolerance)
    # diagnostic: the same file decoded with the accurate scaler flags (separates the file from swscale's default 10-bit path)
    raw2, _w = decode_first_frame(ffmpeg, out, DECODE_VF_ACCURATE, "rgb24", 3)
    if raw2 is not None:
        w2 = 0
        for (_n, rgb, _a), (mean, _m) in zip(PATCHES, read_patches(raw2, 3)):
            w2 = max(w2, max(abs(int(round(m)) - s) for m, s in zip(mean[:3], rgb)))
        res["worst_error_accurate"] = w2
    if alpha:
        rawa, _w = decode_first_frame(ffmpeg, out, "format=rgba", "rgba", 4)
        if rawa is not None:
            ea = 0
            for (_n, _rgb, a), (mean, _m) in zip(PATCHES, read_patches(rawa, 4)):
                ea = max(ea, abs(int(round(mean[3])) - a))
            res["alpha_error"] = ea
    obs = probe_stream(ffprobe, out)
    if obs is not None:
        if obs.get("width") and obs.get("height"):
            res["output_size"] = "%sx%s" % (obs["width"], obs["height"])
        res["tags"] = {k: obs.get(k) for k in ("codec_name", "profile", "pix_fmt", "color_range", "color_space", "color_primaries", "color_transfer")}
        res["tags_match_expect"], res["tag_mismatches"] = compare_expect(obs, chain.get("expect"), chain.get("expect_extra"))
    if keep_dir:
        try:
            shutil.copy2(out, os.path.join(keep_dir, os.path.basename(out)))
        except OSError:
            pass
    try:
        os.remove(out)
    except OSError:
        pass
    return res


def judge_control(c, r):
    """Attach the control's meaning to its result."""
    exp = c.get("expect_result")
    r["control_expect"] = exp if exp else "build-dependent"
    if r["worst_error"] is None:
        r["control_ok"] = None
        r["trap_present"] = None
        return
    failed = not r["pass"]
    r["trap_present"] = failed if exp is None else None
    if exp == "pass":
        r["control_ok"] = not failed
    elif exp == "fail":
        r["control_ok"] = failed
    else:
        r["control_ok"] = True
    r["notes"] = c.get("notes", "")


def split_results(results):
    """(names measured and above the tolerance, names that could not be measured at all). A chain with no worst_error hit an encode or
    decode error: that is a tool or chain-definition problem and is reported on its own line, never as a colour result."""
    unmeasured = [r["name"] for r in results if r["worst_error"] is None]
    above = [r["name"] for r in results if r["worst_error"] is not None and not r["pass"]]
    return above, unmeasured


def chain_result_lines(results, tolerance):
    """The RESULT lines for the chains (empty list when there are none)."""
    if not results:
        return []
    above, unmeasured = split_results(results)
    lines = ["RESULT chains: %d of %d within %d/255%s" % (len(results) - len(above) - len(unmeasured), len(results), tolerance,
                                                         ("; ABOVE TOLERANCE: " + ", ".join(above)) if above else "")]
    if unmeasured:
        lines.append("RESULT chains: could not be measured (encode/decode error; the reason is on the ERROR line, so run without --quiet): " + ", ".join(unmeasured))
    return lines


# ----------------------------------------------------------------------------------------------- chain files
def load_chain_file(path):
    try:
        d = json.loads(read_text_any(path))
    except (OSError, ValueError) as e:
        raise Usage("cannot read chain file %s (%s)" % (os.path.basename(path), e.__class__.__name__))
    if not isinstance(d, dict) or not isinstance(d.get("chains"), dict):
        raise Usage("chain file %s: expected an object with a \"chains\" object (schema lj-chains/1)" % os.path.basename(path))
    chains = {}
    for name, ch in d["chains"].items():
        if not isinstance(ch, dict) or not isinstance(ch.get("video_args", []), list):
            raise Usage("chain %s: needs an object with a video_args array" % name)
        c = dict(ch)
        c["name"] = name
        chains[name] = c
    return chains


def default_chain_file():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "lib", "chains.json")


# ----------------------------------------------------------------------------------------------- the run
def run_test(args):
    info = ffmpeg_info(args.ffmpeg)
    ffmpeg = info.pop("_exe")
    ffprobe = ffprobe_for(args.ffmpeg, args.ffprobe)
    chains = {}
    chain_file_used = None
    want = list(args.chain or [])
    need_file = args.all or (want and any(not w.startswith("control_") for w in want))
    if args.chain_file or need_file:
        cf = args.chain_file or default_chain_file()
        if not os.path.isfile(cf):
            raise Usage("chain file not found: %s" % os.path.basename(cf))
        chains = load_chain_file(cf)
        chain_file_used = os.path.basename(cf)
    run_chains = []
    if args.all:
        run_chains = list(chains.values())
    for w in want:
        if w.startswith("control_"):
            continue
        if w not in chains:
            raise Usage("chain %s is not in %s (known: %s)" % (w, chain_file_used, ", ".join(sorted(chains)) or "none"))
        if chains[w] not in run_chains:
            run_chains.append(chains[w])
    run_controls = []
    if args.all or args.controls:
        run_controls = list(CONTROLS)
    for w in want:
        if w.startswith("control_"):
            hit = [c for c in CONTROLS if c["name"] == w]
            if not hit:
                raise Usage("unknown control %s (known: %s)" % (w, ", ".join(c["name"] for c in CONTROLS)))
            if hit[0] not in run_controls:
                run_controls.append(hit[0])
    if not run_chains and not run_controls:
        raise Usage("nothing to run: give --chain NAME, --all or --controls")

    say("colour_patch: ffmpeg %s (sha256 %s...)" % (short_version(info["version"]) or "?", info["sha256"][:12]))
    say("colour_patch: encodes 2 frames per chain into a temporary folder (deleted at the end), decodes them back, compares with the source.")
    say("colour_patch: tolerance %d/255 per channel (W-16). Pass/fail is on pixels; tags are shown for information." % args.tolerance)
    if ffprobe is None:
        say("colour_patch: ffprobe not found: the tag read-back is skipped (pixels are still tested).")
    work = tempfile.mkdtemp(prefix="lj_cp_")
    keep = None
    if args.keep_dir:
        keep = args.keep_dir
        os.makedirs(keep, exist_ok=True)
    results, ctrl_results = [], []
    try:
        for ch in run_chains:
            r = measure(ffmpeg, ffprobe, ch, work, args.tolerance, keep, "chain")
            results.append(r)
            show(r, args.quiet)
        for c in run_controls:
            r = measure(ffmpeg, ffprobe, c, work, args.tolerance, keep, "control")
            judge_control(c, r)
            ctrl_results.append(r)
            show(r, args.quiet)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    chains_fail, chains_error = split_results(results)
    # a chain that is marked approved:true must measure within tolerance on this build: an approval above 3/255 is a lie (W-16)
    approval_violations = [r["name"] for r in results if r.get("approved_in_file") is True and not r["pass"]]
    bad_controls = [r["name"] for r in ctrl_results if r.get("control_ok") is False or (r["error"] and CONTROL_BY_NAME[r["name"]].get("expect_result"))]
    raw = {"schema": RAW_SCHEMA, "tool_version": TOOL_VERSION,
           "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
           "platform": {"system": platform.system(), "machine": platform.machine(), "python": platform.python_version()},
           "ffmpeg": {"version_line": info["version_line"], "version": info["version"], "configure": info["configure"], "sha256": info["sha256"]},
           "tolerance": args.tolerance,
           "patches": [{"name": n, "rgb": list(rgb)} for n, rgb, _a in PATCHES],
           "decode": DECODE_VF, "chain_file": chain_file_used,
           "chains": results, "controls": ctrl_results,
           "read_back": READBACK_VF,
           "summary": {"chains": len(results), "chains_failed": chains_fail, "chains_error": chains_error, "approval_violations": approval_violations, "controls_misbehaved": bad_controls,
                       "traps_present": [r["name"] for r in ctrl_results if r.get("trap_present")]}}
    say("")
    for line in chain_result_lines(results, args.tolerance):
        say(line)
    if approval_violations:
        say("RESULT approvals: NOT ALLOWED, marked approved:true in the chain file but above %d/255 (or not measurable) on this build: %s" % (args.tolerance, ", ".join(approval_violations)))
    if ctrl_results:
        trap = raw["summary"]["traps_present"]
        say("RESULT controls: %s" % (("TRAP PRESENT on this build for: " + ", ".join(trap)) if trap else "no build-dependent trap shown on this build"))
        if bad_controls:
            say("RESULT controls: TOOL PROBLEM, a control that must behave a fixed way did not: " + ", ".join(bad_controls))
    if args.json:
        write_json(args.json, raw)
        say("colour_patch: wrote the RAW record %s. It holds build flags: the maker pastes it in chat only; never file it." % os.path.basename(args.json))
    return raw, (1 if (chains_fail or chains_error or bad_controls or approval_violations) else 0)


CONTROL_BY_NAME = {c["name"]: c for c in CONTROLS}


def show(r, quiet=False):
    if quiet:
        return
    if r["worst_error"] is None:
        say("  %-30s ERROR  %s" % (r["name"], r["error"]))
        return
    tag = "PASS" if r["pass"] else "FAIL"
    extra = ""
    if r["kind"] == "control" and r.get("trap_present"):
        extra = "  TRAP PRESENT"
    if r["kind"] == "control" and r.get("control_ok") is False:
        extra = "  CONTROL MISBEHAVED"
    acc = "" if r["worst_error_accurate"] is None else "  accurate-decode %d" % r["worst_error_accurate"]
    tm = ""
    if r["tags_match_expect"] is False:
        tm = "  tags differ from chain expect: " + "; ".join(r["tag_mismatches"])
    al = "" if r["alpha_error"] is None else "  alpha-error %d" % r["alpha_error"]
    if r.get("output_size") and r["output_size"] != "%dx%d" % (W, H):
        al += "  measured at %s" % r["output_size"]
    per = "  ".join("%s %s" % (p["name"], "/".join("%+d" % e for e in p["error"])) for p in r["patches"])
    say("  %-30s %s  worst %d/255%s%s%s%s%s   [%s]" % (r["name"], tag, r["worst_error"], acc, al, extra, tm, "", per))


# ----------------------------------------------------------------------------------------------- derived form (4.16)
def derive(raw_path, out_path):
    """RAW record -> the filed form: version number, binary sha256, chain names, worst errors, pass flags. Nothing else."""
    try:
        raw = json.loads(read_text_any(raw_path))
    except (OSError, ValueError) as e:
        raise Usage("cannot read the raw file (%s)" % e.__class__.__name__)
    if not isinstance(raw, dict) or raw.get("schema") != RAW_SCHEMA:
        raise Usage("the input is not a %s record" % RAW_SCHEMA)
    ff = raw.get("ffmpeg") or {}
    ver = short_version(str(ff.get("version") or ""))
    if not ver:
        ver = short_version(str((ff.get("version_line") or "").replace("ffmpeg version", "").strip()))
    sha = str(ff.get("sha256") or "").lower()
    if not ver or not VERSION_RX.match(ver):
        raise Usage("the raw record has no usable ffmpeg version number")
    if not SHA_RX.match(sha):
        raise Usage("the raw record has no 64-hex binary SHA-256")
    tol = raw.get("tolerance", TOLERANCE)
    if not isinstance(tol, int) or isinstance(tol, bool) or not 0 <= tol <= 255:
        raise Usage("the raw record has an invalid tolerance")

    def rows(items):
        out = []
        for r in items or []:
            nm = str(r.get("name", ""))
            we = r.get("worst_error")
            if not NAME_RX.match(nm):
                raise Usage("a chain name in the raw record is not a plain identifier")
            if not (isinstance(we, int) and not isinstance(we, bool) and 0 <= we <= 255):
                raise Usage("chain %s has no usable worst_error (it did not run?)" % nm)
            out.append({"name": nm, "worst_error": we, "pass": we <= tol})
        return out

    derived = {"schema": DERIVED_SCHEMA, "ffmpeg": {"version": ver, "sha256": sha}, "tolerance": tol,
               "chains": rows(raw.get("chains")), "controls": rows(raw.get("controls"))}
    problems = validate_derived(derived)
    if problems:
        raise Usage("the derived record would be invalid: " + "; ".join(problems))
    write_json(out_path, derived)
    return derived


def validate_derived(d):
    """Hand-coded mirror of pipeline/validators/pc_chains.schema.json (draft-07 subset). Returns a list of problems."""
    errs = []
    if not isinstance(d, dict):
        return ["not an object"]
    allowed = {"schema", "ffmpeg", "tolerance", "chains", "controls"}
    for k in d:
        if k not in allowed:
            errs.append("unexpected key %s" % k)
    if d.get("schema") != DERIVED_SCHEMA:
        errs.append("schema must be %s" % DERIVED_SCHEMA)
    ff = d.get("ffmpeg")
    if not isinstance(ff, dict) or set(ff) != {"version", "sha256"}:
        errs.append("ffmpeg must have exactly version and sha256")
    else:
        if not isinstance(ff["version"], str) or not VERSION_RX.match(ff["version"]):
            errs.append("ffmpeg.version must be a plain version number")
        if not isinstance(ff["sha256"], str) or not SHA_RX.match(ff["sha256"]):
            errs.append("ffmpeg.sha256 must be 64 lower-case hex characters")
    tol = d.get("tolerance")
    if not isinstance(tol, int) or isinstance(tol, bool) or not 0 <= tol <= 255:
        errs.append("tolerance must be an integer 0..255")
    for key, required in (("chains", True), ("controls", False)):
        arr = d.get(key)
        if arr is None and not required:
            continue
        if not isinstance(arr, list):
            errs.append("%s must be an array" % key)
            continue
        for i, row in enumerate(arr):
            if not isinstance(row, dict) or set(row) != {"name", "worst_error", "pass"}:
                errs.append("%s[%d] must have exactly name, worst_error, pass" % (key, i))
                continue
            if not isinstance(row["name"], str) or not NAME_RX.match(row["name"]):
                errs.append("%s[%d].name must be a plain identifier" % (key, i))
            we = row["worst_error"]
            if not isinstance(we, int) or isinstance(we, bool) or not 0 <= we <= 255:
                errs.append("%s[%d].worst_error must be an integer 0..255" % (key, i))
            if not isinstance(row["pass"], bool):
                errs.append("%s[%d].pass must be a boolean" % (key, i))
            elif isinstance(we, int) and isinstance(tol, int) and row["pass"] != (we <= tol):
                errs.append("%s[%d].pass disagrees with worst_error and tolerance" % (key, i))
    return errs


# ----------------------------------------------------------------------------------------------- self-test
def selftest(args):
    """Mechanism tests that need only ffmpeg (lossless FFV1 encodes; no x264, no ProRes, no ffprobe)."""
    info = ffmpeg_info(args.ffmpeg)
    ffmpeg = info["_exe"]
    say("colour_patch --selftest: ffmpeg %s. Needs only ffmpeg; writes only to a temporary folder." % (short_version(info["version"]) or "?"))
    fails = 0

    def check(name, ok, detail=""):
        nonlocal fails
        say("  %-5s %-44s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails += 1

    frame = make_frame(False)
    check("frame.size", len(frame) == W * H * 3, "%d bytes" % len(frame))
    pm = read_patches(frame, 3)
    check("frame.patch_values", all([int(round(m)) for m in mean[:3]] == list(rgb) for (mean, _x), (_n, rgb, _a) in zip(pm, PATCHES)),
          "read back exactly 255,0,0 / 128,128,128 / 224,172,140")
    work = tempfile.mkdtemp(prefix="lj_cp_self_")
    try:
        good = measure(ffmpeg, None, CONTROL_BY_NAME["control_lossless_709"], work, TOLERANCE, None, "control")
        check("mechanism.lossless_709_passes", good["worst_error"] is not None and good["pass"] and good["worst_error"] <= 1,
              "worst %s/255 (want 1 or less)" % good["worst_error"] if good["worst_error"] is not None else good["error"])
        bad = measure(ffmpeg, None, CONTROL_BY_NAME["control_wrong_matrix_bt601"], work, TOLERANCE, None, "control")
        check("mechanism.wrong_matrix_is_caught", bad["worst_error"] is not None and not bad["pass"] and bad["worst_error"] > 10,
              "worst %s/255 (want above 10)" % bad["worst_error"] if bad["worst_error"] is not None else bad["error"])
        # a chain whose output is not 1920x1080 (the 1280x720 phone copy) is read back at its own size, not rejected
        small = dict(CONTROL_BY_NAME["control_lossless_709"], name="selftest_720_lossless",
                     vf=CONTROL_BY_NAME["control_lossless_709"]["vf"].replace("scale=out_color_matrix", "scale=1280:720:out_color_matrix", 1))
        small_bad = dict(CONTROL_BY_NAME["control_wrong_matrix_bt601"], name="selftest_720_wrong_matrix",
                         vf=CONTROL_BY_NAME["control_wrong_matrix_bt601"]["vf"].replace("scale=out_color_matrix", "scale=1280:720:out_color_matrix", 1))
        probe = ffprobe_for(args.ffmpeg, getattr(args, "ffprobe", None))
        g720 = measure(ffmpeg, probe, small, work, TOLERANCE, None, "chain")
        b720 = measure(ffmpeg, probe, small_bad, work, TOLERANCE, None, "chain")
        size_ok = probe is None or g720["output_size"] == "1280x720"
        check("mechanism.720p_chain_is_measured", g720["worst_error"] is not None and g720["pass"] and g720["worst_error"] <= 1 and size_ok,
              ("worst %s/255 at %s (want 1 or less at 1280x720)" % (g720["worst_error"], g720["output_size"] or "size not probed")) if g720["worst_error"] is not None else g720["error"])
        check("mechanism.720p_wrong_matrix_is_caught", b720["worst_error"] is not None and not b720["pass"] and b720["worst_error"] > 10,
              ("worst %s/255 (want above 10)" % b720["worst_error"]) if b720["worst_error"] is not None else b720["error"])
        # a chain that cannot be encoded is reported as "could not be measured", never as "above tolerance"
        broken = measure(ffmpeg, None, {"name": "selftest_no_such_encoder", "container": "mp4", "vf": "", "video_args": ["-c:v", "no_such_encoder_xyz"]},
                         work, TOLERANCE, None, "chain")
        lines = chain_result_lines([good, broken], TOLERANCE)
        check("mechanism.unmeasurable_chain_is_separate", broken["worst_error"] is None and split_results([good, broken]) == ([], ["selftest_no_such_encoder"])
              and any("could not be measured" in l for l in lines) and not any("ABOVE TOLERANCE" in l for l in lines),
              "an encode error gives its own RESULT line and no ABOVE TOLERANCE")
        check("mechanism.tolerance_edge", is_pass(3, 3) and not is_pass(4, 3) and is_pass(0, 3) and not is_pass(None, 3),
              "3 passes, 4 fails, tolerance 3")
        # derive round trip with a synthetic raw record (no ffmpeg involved)
        raw = {"schema": RAW_SCHEMA, "tolerance": 3,
               "ffmpeg": {"version_line": "ffmpeg version 9.0.2-test_build", "version": "9.0.2-test_build", "configure": ["--enable-gpl"], "sha256": "ab" * 32},
               "chains": [{"name": "c1", "worst_error": 1}, {"name": "c2", "worst_error": 4}], "controls": []}
        rp = os.path.join(work, "raw.json")
        op = os.path.join(work, "derived.json")
        with open(rp, "w", encoding="utf-8") as f:
            json.dump(raw, f)
        d = derive(rp, op)
        check("derive.round_trip", d["chains"][0]["pass"] is True and d["chains"][1]["pass"] is False and not validate_derived(d),
              "pass flags follow worst_error; schema mirror accepts it")
        check("derive.drops_build_flags", "configure" not in json.dumps(d) and "enable-gpl" not in json.dumps(d), "no configure flags in the derived record")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    say("colour_patch --selftest: %s" % ("ALL PASS" if not fails else "%d FAILED" % fails))
    return 0 if not fails else 1


# ----------------------------------------------------------------------------------------------- main
def build_parser():
    p = argparse.ArgumentParser(prog="colour_patch.py", add_help=True, description="Colour-patch test (W-16). See the header of this file.")
    p.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"), help="ffmpeg to test (default: FFMPEG or 'ffmpeg' on PATH)")
    p.add_argument("--ffprobe", default=None, help="ffprobe (default: FFPROBE, or beside ffmpeg, or on PATH)")
    p.add_argument("--chain", action="append", help="chain name (repeatable); control_* names run a built-in control")
    p.add_argument("--chain-file", default=None, help="chains file (default: pipeline/lib/chains.json); any file with a \"chains\" object works")
    p.add_argument("--all", action="store_true", help="every chain in the chain file plus the built-in controls")
    p.add_argument("--controls", action="store_true", help="only the built-in controls")
    p.add_argument("--tolerance", type=int, default=TOLERANCE, help="pass at this worst per-channel error out of 255 (default 3, W-16)")
    p.add_argument("--keep-dir", default=None, help="copy the encoded 2-frame test files here (optional)")
    p.add_argument("--json", default=None, help="write the RAW record here (read by the maker, pasted in chat only)")
    p.add_argument("--derive-from", default=None, metavar="RAW", help="read a raw record and write the filed form to --out")
    p.add_argument("--out", default=None, help="output file for --derive-from")
    p.add_argument("--selftest", action="store_true", help="mechanism tests; needs only ffmpeg")
    p.add_argument("--quiet", action="store_true", help="print only the result lines")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.derive_from:
            if not args.out:
                raise Usage("--derive-from needs --out")
            d = derive(args.derive_from, args.out)
            say("colour_patch: wrote the derived record %s (ffmpeg %s, %d chains, %d controls). No build flags, no paths." %
                (os.path.basename(args.out), d["ffmpeg"]["version"], len(d["chains"]), len(d["controls"])))
            return 0
        if args.selftest:
            return selftest(args)
        _raw, code = run_test(args)
        return code
    except Usage as e:
        print("colour_patch: %s" % e, file=sys.stderr)
        return 2
    except EnvError as e:
        print("colour_patch: environment problem: %s" % e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
