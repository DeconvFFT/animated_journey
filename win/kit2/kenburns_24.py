#!/usr/bin/env python3
"""kenburns_24.py: Exercise 2, Ken Burns by script, at the project rate of 24 fps (W-14). WP-09, kit B.

WHAT IT DOES
  Takes two or more of YOUR OWN stills (not family photos before the P-LOCK gate, D-13), gives each one a slow camera move of about
  six seconds (push-in, pan, pull-out), joins the moves with one-second dissolves (ffmpeg xfade) and writes ONE video file:
  1920x1080, 24 fps, H.264 High, yuv420p, BT.709 limited-range tags, made through the project's `h264_online` chain
  (pipeline/lib/chains.json), so the pixels are right and not just the tags (W-16).
  Three moves of 6 s joined by 1 s dissolves are 16.0 s = 384 frames.

HOW THE PICTURE IS MADE (why it does not shimmer, why a round thing stays round)
  * Each still is first turned the right way up (EXIF), then a 16:9 window is chosen inside it. The picture is NEVER stretched to
    fit: every window has exactly the 16:9 shape, so a circle stays a circle. (`zoompan` on a 3:2 photo squashed a circle to
    641 x 541 pixels in the research; this tool measures the ratio of a drawn circle in its self-test and it reads 1.00.)
  * Every frame is cut out and scaled in ONE step by Pillow's resize(box=...) with LANCZOS, where the box has fractional pixel
    positions. That is the sub-pixel method of research/cinematic-quality-fixtures/zoompan_vs_subpixel_prints.py (pil_resize_box),
    ported here with that file cited because its frame count is a module-level constant. ffmpeg's `zoompan` snaps to whole
    pixels and shimmers, so it is a PROOF tool only (W-41); --proof-zoompan makes it so you can see the difference.
  * The frames go to ONE ffmpeg through a pipe, as raw RGB. ffmpeg cuts the stream into the moves, dissolves them with xfade and
    encodes with the h264_online chain. Nothing big is written to disk on the way.

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows; needs Pillow and numpy: py -3 -m pip install --user pillow numpy)
  py -3 -I win\\kit2\\kenburns_24.py still1.jpg still2.jpg still3.jpg --out renders\\ex02\\ex02_kenburns.mp4
  py -3 -I win\\kit2\\kenburns_24.py still1.jpg still2.jpg still3.jpg --proof-zoompan        also the zoompan version, to compare
  py -3 -I win\\kit2\\kenburns_24.py still1.jpg still2.jpg still3.jpg --gate-window          also a lossless 96-frame push for mo8_gate.py
  py -3 -I win\\kit2\\kenburns_24.py --selftest --out renders\\wp09\\ex02.mp4                 synthetic stills only; checks itself
  Options: --moves push,pan,pull (one per still, repeated; also: drift)   --seconds 6   --fade 1   --focus X,Y (0..1, one pair
           for all stills or one pair per still; where the 16:9 window sits in a still that is not 16:9)   --ffmpeg PATH (FFMPEG)
           --chains-file F   --gate-frames N (12..96)   --test-tone (adds a quiet -16 LUFS test tone so the file passes the full
           online_h264 profile; the self-test uses it)   --work DIR (where temporary files go; default a new folder under the
           system temp folder, deleted at the end)

WHAT IT PRINTS. Numbered steps, one line before each action and "ok" after; the stills are named by NUMBER and size only (never
by file name); the output is named by base name only. It ends with the read-back of the finished file: width, height,
r_frame_rate, codec, profile, pix_fmt, the four colour tags, frame count, duration, each PASS or FAIL, and RESULT.
WHAT IT WRITES. The one output file (and, if you ask, <name>_push_only.mkv, <name>_zoompan_proof.mp4 and
<name>_push_only_zoompan.mkv beside it) and a temporary folder that is deleted at the end. A lossless gate window is large
(about 100 to 250 MB for real photos): delete it after you have run the gate.
WHAT IT NEVER TOUCHES. It reads the stills you name and nothing else; it never changes them, never uses the network and never
installs anything.

EXIT CODES (build plan 4.3)  0 done and the read-back passed   1 the read-back (or a self-test check) failed   2 bad usage or an
unusable still   3 environment problem (ffmpeg, Pillow, numpy or the chain file missing, ffmpeg failed, no disk space)
UNVERIFIED on Windows until the maker runs it. Verified on ffmpeg 6.1.1, Python 3.13, Pillow 12.3, numpy 2.5 (Linux).
"""
import argparse
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
if HERE not in sys.path:          # python -I does not put the script's folder on sys.path
    sys.path.insert(0, HERE)
import pc_helpers                  # noqa: E402  (the test tone and the chain reader are shared with the PC runner)

FPS = 24
W, H = 1920, 1080
ASPECT = 16.0 / 9.0
DEFAULT_SECONDS = 6
DEFAULT_FADE = 1
GATE_FRAMES = 96
GATE_MIN = 12
DEFAULT_CHAINS = os.path.join(REPO, "pipeline", "lib", "chains.json")
DEFAULT_OUT = os.path.join(REPO, "renders", "ex02", "ex02_kenburns.mp4")
ONLINE_CHAIN = "h264_online"
MASTER_CHAIN = "ffv1_lossless"
PIP_LINE = "py -3 -m pip install --user pillow numpy"

# The moves. z = zoom (1.0 is the whole 16:9 window of the still, 1.2 is 20 percent closer); cx, cy = where the window's centre
# is, as a fraction of that 16:9 window (0.5, 0.5 is the middle). Every move eases in and out with a cosine curve.
MOVES = {
    "push":  {"z0": 1.00, "z1": 1.15, "c0": (0.50, 0.50), "c1": (0.50, 0.50), "what": "slow push-in on the middle"},
    "pan":   {"z0": 1.35, "z1": 1.35, "c0": (0.38, 0.50), "c1": (0.62, 0.50), "what": "slow pan from left to right, close up"},
    "pull":  {"z0": 1.20, "z1": 1.00, "c0": (0.44, 0.56), "c1": (0.50, 0.50), "what": "slow pull-out with a small drift"},
    "drift": {"z0": 1.10, "z1": 1.25, "c0": (0.56, 0.44), "c1": (0.46, 0.54), "what": "push-in that drifts down and left"},
}
DEFAULT_MOVES = ["push", "pan", "pull"]

# colours of the synthetic test stills (style-neutral, D-28/D-29: grey texture, a disc, three flat patches)
DISC_RGB = (250, 215, 40)
PATCHES_RGB = [("red", (255, 0, 0)), ("grey50", (128, 128, 128)), ("skin", (224, 172, 140))]


class Usage(Exception):
    """Bad usage or an unusable still (exit 2)."""


class EnvError(Exception):
    """Missing tool, failed ffmpeg, no disk space (exit 3)."""


def say(msg=""):
    print(msg)
    sys.stdout.flush()


# ------------------------------------------------------------------------------------------------------ libraries and tools
def need_libs():
    try:
        import numpy                                  # noqa: F401
        from PIL import Image                         # noqa: F401
    except ImportError as e:
        raise EnvError("Pillow and numpy are needed (%s). Install them for your user with:  %s" % (str(e).split("'")[1] if "'" in str(e) else "import error", PIP_LINE))


def resolve_exe(name):
    return pc_helpers.resolve_exe(name)


def ffprobe_for(ffmpeg):
    d, b = os.path.split(ffmpeg)
    if b.lower().startswith("ffmpeg"):
        sib = os.path.join(d, "ffprobe" + b[len("ffmpeg"):])
        if os.path.isfile(sib):
            return sib
    return shutil.which("ffprobe")


def load_chain(chains_path, name):
    d = pc_helpers.read_chains(chains_path)
    ch = d["chains"].get(name)
    if not ch or not isinstance(ch.get("video_args"), list) or not isinstance(ch.get("vf"), str):
        raise Usage("the chain file has no usable %s chain" % name)
    return ch


# ------------------------------------------------------------------------------------------------------ geometry
def ease(t):
    """Cosine ease in and out: 0 at t=0, 1 at t=1, flat at both ends."""
    return 0.5 - 0.5 * math.cos(math.pi * t)


def base_window(sw, sh, focus=(0.5, 0.5)):
    """The largest 16:9 window inside a still of sw x sh, as floats (x0, y0, w, h) with w/h exactly 16/9.
    `focus` places it inside the slack (0 = against the left/top edge, 1 = against the right/bottom edge)."""
    if sw / float(sh) >= ASPECT:
        bh = float(sh)
        bw = bh * ASPECT
    else:
        bw = float(sw)
        bh = bw / ASPECT
    fx = min(1.0, max(0.0, focus[0]))
    fy = min(1.0, max(0.0, focus[1]))
    return ((sw - bw) * fx, (sh - bh) * fy, bw, bh)


def move_box(move, base, i, n):
    """The source box (x0, y0, x1, y1), in floats, for frame i of n. Its shape is exactly 16:9 and it stays inside `base`."""
    bx, by, bw, bh = base
    t = ease(i / float(n - 1)) if n > 1 else 0.0
    z = move["z0"] + (move["z1"] - move["z0"]) * t
    cx = move["c0"][0] + (move["c1"][0] - move["c0"][0]) * t
    cy = move["c0"][1] + (move["c1"][1] - move["c0"][1]) * t
    w = bw / z
    h = bh / z
    x0 = bx + cx * bw - w / 2.0
    y0 = by + cy * bh - h / 2.0
    x0 = min(max(x0, bx), bx + bw - w)            # never outside the window (a request to leave it is clamped, not an error)
    y0 = min(max(y0, by), by + bh - h)
    return (x0, y0, x0 + w, y0 + h)


def project(box, point):
    """Where a point of the still lands in the 1920x1080 output for a given box (floats)."""
    x0, y0, x1, y1 = box
    return ((point[0] - x0) * W / (x1 - x0), (point[1] - y0) * H / (y1 - y0))


# ------------------------------------------------------------------------------------------------------ stills
def to_rgb8(img):
    """Pillow image -> 8-bit RGB. 16-bit greys (I;16) are scaled down, not clipped."""
    import numpy as np
    from PIL import Image
    if img.mode in ("I;16", "I;16B", "I;16L", "I"):
        a = np.asarray(img).astype(np.float32)
        top = 65535.0 if a.max() > 255 else 255.0
        img = Image.fromarray(np.clip(a * 255.0 / top, 0, 255).astype(np.uint8), "L")
    return img.convert("RGB")


def load_still(path):
    """Open a still, turn it the right way up, make it 8-bit sRGB RGB. Returns (image, notes)."""
    from PIL import Image, ImageOps
    notes = []
    try:
        img = Image.open(path)
        img.load()
    except Image.DecompressionBombError:
        raise Usage("a still is larger than Pillow's safety limit; shrink it first (for example with ImageMagick: magick in.tif -resize 6000x out.jpg)")
    except (OSError, ValueError):
        raise Usage("cannot open a still as an image (is it a photo file? JPEG, PNG and TIFF work)")
    icc = img.info.get("icc_profile")
    try:
        before = img.size
        img = ImageOps.exif_transpose(img)
        if img.size != before:
            notes.append("turned upright from its EXIF orientation")
    except Exception:
        notes.append("EXIF orientation could not be read")
    if icc:
        try:
            from PIL import ImageCms
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            desc = ImageCms.getProfileDescription(src) or ""
            if "srgb" not in desc.lower():
                img = ImageCms.profileToProfile(to_rgb8(img), src, ImageCms.createProfile("sRGB"), outputMode="RGB")
                notes.append("converted from its embedded colour profile to sRGB")
        except Exception:
            notes.append("has a colour profile that could not be read: colours are used as they are")
    return to_rgb8(img), notes


def parse_focus(text, n):
    """'0.5,0.5' (all stills) or '0.5,0.5,0.3,0.6,...' (one pair per still) -> list of n (fx, fy)."""
    if not text:
        return [(0.5, 0.5)] * n
    try:
        v = [float(x) for x in text.replace(";", ",").split(",") if x.strip() != ""]
    except ValueError:
        raise Usage("--focus wants numbers between 0 and 1, for example 0.5,0.4")
    if len(v) == 2:
        pairs = [(v[0], v[1])] * n
    elif len(v) == 2 * n:
        pairs = [(v[2 * k], v[2 * k + 1]) for k in range(n)]
    else:
        raise Usage("--focus wants one pair (X,Y) for all stills or %d pairs (one per still)" % n)
    for fx, fy in pairs:
        if not (0.0 <= fx <= 1.0 and 0.0 <= fy <= 1.0):
            raise Usage("--focus numbers must be between 0 and 1")
    return pairs


# ------------------------------------------------------------------------------------------------------ synthetic stills (tests and --selftest)
def grey_texture(w, h, seed, rng_lo=95, rng_hi=165):
    """Neutral grey, low-contrast 1/f-like texture (smooth enough to compress, rich enough for the MO8 estimator).
    Deterministic: seeded, no clock, no random module."""
    import numpy as np
    from PIL import Image
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for gw, gh in ((12, 8), (24, 16), (48, 32), (96, 64)):
        g = (rng.random((gh, gw)) * 255).astype(np.uint8)
        im = Image.fromarray(g, "L").resize((w, h), Image.BICUBIC)
        acc += np.asarray(im, np.float32) * amp
        tot += amp
        amp *= 0.65
    acc /= tot
    acc = rng_lo + (acc - acc.min()) / max(1e-6, (acc.max() - acc.min())) * (rng_hi - rng_lo)
    return Image.fromarray(np.clip(acc, 0, 255).astype(np.uint8), "L").convert("RGB")


def synthetic_still(index, size=(3000, 2000)):
    """A 3:2 still (not 16:9 on purpose, so the crop has work to do) with a drawn disc and three flat colour patches.
    Returns (image, info) where info has the disc centre/radius and the patch centres in still pixels."""
    from PIL import ImageDraw
    w, h = size
    img = grey_texture(w, h, 11 + index)
    d = ImageDraw.Draw(img)
    cx, cy, r = w // 2, h // 2, int(h * 0.18)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=DISC_RGB)
    patches = []
    side = 160
    top = int(h * 0.78)
    for k, (name, rgb) in enumerate(PATCHES_RGB):
        x0 = cx - side // 2 + (k - 1) * 2 * side
        d.rectangle((x0, top, x0 + side - 1, top + side - 1), fill=rgb)
        patches.append({"name": name, "rgb": rgb, "centre": (x0 + side / 2.0, top + side / 2.0)})
    if index % 3 == 1:                       # variety: a thin frame line, neutral
        d.rectangle((int(w * 0.12), int(h * 0.22), int(w * 0.88), int(h * 0.80)), outline=(210, 210, 210), width=6)
    if index % 3 == 2:                       # variety: a cross of two lines through the disc
        d.line((cx - 2 * r, cy, cx + 2 * r, cy), fill=(40, 40, 40), width=8)
        d.line((cx, cy - 2 * r, cx, cy + 2 * r), fill=(40, 40, 40), width=8)
    return img, {"disc_centre": (cx, cy), "disc_radius": r, "patches": patches, "size": size}


def make_synthetic_stills(folder, count=3):
    """Write `count` synthetic JPEGs (quality 95, 4:4:4) into `folder`; returns [(path, info)]."""
    out = []
    for k in range(count):
        img, info = synthetic_still(k)
        p = os.path.join(folder, "still%d.jpg" % (k + 1))
        img.save(p, "JPEG", quality=95, subsampling=0)
        out.append((p, info))
    return out


# ------------------------------------------------------------------------------------------------------ ffmpeg plumbing
def tail_of(path, n=6):
    try:
        with open(path, "rb") as f:
            lines = f.read().decode("utf-8", "replace").strip().splitlines()
    except OSError:
        return []
    return [ln[:200] for ln in lines[-n:]]


def scrub(text, work):
    return text.replace(work, "<work>") if work else text


def start_raw_encoder(ffmpeg, args_after_input, work, tag, fps=FPS):
    """Start ffmpeg reading raw 1920x1080 RGB frames from stdin. Returns (process, logpath)."""
    log = os.path.join(work, "ffmpeg_%s.log" % tag)
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-video_size", "%dx%d" % (W, H), "-framerate", str(fps), "-i", "-"] + args_after_input
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=open(log, "wb"))
    except OSError:
        raise EnvError("cannot start ffmpeg")
    return p, log


def finish_encoder(p, log, work, what):
    try:
        if p.stdin:
            p.stdin.close()
    except (BrokenPipeError, OSError):
        pass
    rc = p.wait()
    if rc != 0:
        tail = " | ".join(scrub(t, work) for t in tail_of(log))
        raise EnvError("ffmpeg failed while making %s (exit %s): %s" % (what, rc, tail or "no message"))


def write_frame(p, data, log, work, what):
    try:
        p.stdin.write(data)
    except (BrokenPipeError, OSError):
        try:
            p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            pass
        tail = " | ".join(scrub(t, work) for t in tail_of(log))
        raise EnvError("ffmpeg stopped early while making %s: %s" % (what, tail or "no message"))


def build_graph(n, frames, fade_frames, online_vf):
    """filter_complex for n moves of `frames` frames each, dissolved by `fade_frames` frames: one raw stream in, one picture out.
    The stream is cut back into the moves with trim, dissolved with xfade (in planar RGB, so no colour matrix is applied by
    accident), then the h264_online chain's own vf (scale first, then format, then setparams) makes the BT.709 YCbCr."""
    parts = ["[0:v]format=gbrp,split=%d%s" % (n, "".join("[s%d]" % k for k in range(n)))]
    for k in range(n):
        parts.append("[s%d]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[v%d]" % (k, k * frames, (k + 1) * frames, k))
    prev = "v0"
    for k in range(1, n):
        off = k * (frames - fade_frames)
        label = "x%d" % k
        parts.append("[%s][v%d]xfade=transition=fade:duration=%.6f:offset=%.6f[%s]" % (prev, k, fade_frames / float(FPS), off / float(FPS), label))
        prev = label
    parts.append("[%s]%s[vout]" % (prev, online_vf))
    return ";".join(parts)


def replace_file(src, dst):
    try:
        os.replace(src, dst)
    except OSError:
        raise EnvError("cannot write %s (is the old file open in a player? close it and run again)" % os.path.basename(dst))


def clamp_box(box, size):
    """Float-rounding guard: a box may not leave the still (it can exceed it by 1e-12 when a window touches the edge)."""
    return (max(0.0, box[0]), max(0.0, box[1]), min(float(size[0]), box[2]), min(float(size[1]), box[3]))


def render_movie(ffmpeg, stills, moves, out, chain, master_chain, seconds, fade, work, gate_path=None, gate_frames=GATE_FRAMES, tone=False, log=say):
    """The whole job. `stills` = list of (PIL image, base window); `moves` = list of move dicts. Returns a dict of facts."""
    from PIL import Image
    n = len(stills)
    frames = int(round(seconds * FPS))
    fade_frames = int(round(fade * FPS))
    total = n * frames - (n - 1) * fade_frames
    lanczos = getattr(Image, "Resampling", Image).LANCZOS
    partial = out + ".part.mp4"                      # next to the output, so the final rename never crosses a drive
    graph = build_graph(n, frames, fade_frames, chain["vf"])
    args = ["-filter_complex", graph]
    if tone:
        args = ["-f", "lavfi", "-i", pc_helpers.tone_source("%.3f" % (total / float(FPS))), "-filter_complex", graph, "-af", pc_helpers.tone_filter()]
    args += ["-map", "[vout]"]
    if tone:
        args += ["-map", "1:a"]
    args += list(chain["video_args"])
    if tone:
        args += list(chain.get("audio_args", [])) + ["-t", "%.3f" % (total / float(FPS))]
    else:
        args += ["-an"]
    args += [partial]
    # the input order matters for the tone: input 0 is the raw pipe (declared first by start_raw_encoder), input 1 the tone
    enc, enc_log = start_raw_encoder(ffmpeg, args, work, "main")
    gate = None
    gate_log = None
    gate_window = None
    if gate_path:
        first = 0
        gate_len = min(gate_frames, frames - fade_frames)
        gate_start = max(0, frames - fade_frames - gate_len)         # the window ends where the first dissolve starts
        gate_window = (gate_start, gate_start + gate_len)
        gate_args = ["-vf", master_chain["vf"]] + list(master_chain["video_args"]) + [gate_path + ".part.mkv"]
        gate, gate_log = start_raw_encoder(ffmpeg, gate_args, work, "gate")
    t0 = time.time()
    try:
        for k in range(n):
            img, base = stills[k]
            mv = moves[k]
            log("  move %d of %d: %s, %d frames (%s)" % (k + 1, n, mv["name"], frames, mv["what"]))
            for i in range(frames):
                box = clamp_box(move_box(mv, base, i, frames), img.size)
                data = img.resize((W, H), lanczos, box=box).tobytes()
                write_frame(enc, data, enc_log, work, "the movie")
                if gate is not None and k == 0 and gate_window[0] <= i < gate_window[1]:
                    write_frame(gate, data, gate_log, work, "the gate window")
        finish_encoder(enc, enc_log, work, "the movie")
        if gate is not None:
            finish_encoder(gate, gate_log, work, "the gate window")
    except BaseException:
        for pr in (enc, gate):
            if pr is not None and pr.poll() is None:
                try:
                    pr.kill()
                except OSError:
                    pass
        for leftover in ([partial] + ([gate_path + ".part.mkv"] if gate_path else [])):
            try:
                os.remove(leftover)
            except OSError:
                pass
        raise
    replace_file(partial, out)
    if gate_path:
        replace_file(gate_path + ".part.mkv", gate_path)
    return {"frames": total, "seconds": total / float(FPS), "render_s": time.time() - t0, "gate_window": gate_window, "move_frames": frames, "fade_frames": fade_frames}


# ------------------------------------------------------------------------------------------------------ the zoompan proof
def zoompan_filter(seconds, amount, fps=FPS):
    """The ffmpeg zoompan text for a push-in lasting `seconds`. d is the number of frames: SECONDS x 24, so 5 s is d=120."""
    d = int(round(seconds * fps))
    z = "1+%s*(0.5-0.5*cos(PI*on/%d))" % (repr(float(amount)), d - 1)
    return ("zoompan=z='%s':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d" % (z, d, W, H, fps)), d


def make_zoompan_proof(ffmpeg, img, base, chain, master_chain, out_mp4, out_gate, work, seconds=5, amount=0.15, gate_frames=GATE_FRAMES, log=say):
    """The playbook's zoompan push (crop to 16:9 first, scale up, zoompan) as a proof clip, plus a lossless window for the gate."""
    bx, by, bw, bh = base
    cw = int(bw) // 2 * 2
    chh = min(int(round(cw * 9 / 16.0 / 2.0)) * 2, img.size[1])
    cx0 = min(int(bx), img.size[0] - cw)
    cy0 = min(int(by), img.size[1] - chh)
    crop = img.crop((cx0, cy0, cx0 + cw, cy0 + chh))     # an integer-pixel 16:9 crop: that is all zoompan can start from
    png = os.path.join(work, "proof_base.png")
    crop.save(png, "PNG", compress_level=1)
    zp, d = zoompan_filter(seconds, amount)
    pre = "scale=6000:-1:flags=lanczos,"
    glen = min(gate_frames, d - 12)
    g0 = 6
    fc = ("[0:v]%s%s,format=rgb24,split=2[p][q];[p]%s[o];[q]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS,%s[g]"
          % (pre, zp, chain["vf"], g0, g0 + glen, master_chain["vf"]))
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", png, "-filter_complex", fc,
           "-map", "[o]"] + list(chain["video_args"]) + ["-an", out_mp4 + ".part.mp4",
           "-map", "[g]"] + list(master_chain["video_args"]) + [out_gate + ".part.mkv"]
    logf = os.path.join(work, "ffmpeg_proof.log")
    log("  zoompan proof: %d frames (d=%d for %g s), then a %d-frame lossless window" % (d, d, seconds, glen))
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=open(logf, "wb"), timeout=1800)
    except (OSError, subprocess.TimeoutExpired):
        raise EnvError("ffmpeg could not make the zoompan proof")
    if r.returncode != 0:
        raise EnvError("ffmpeg failed while making the zoompan proof: %s" % " | ".join(scrub(t, work) for t in tail_of(logf)))
    replace_file(out_mp4 + ".part.mp4", out_mp4)
    replace_file(out_gate + ".part.mkv", out_gate)
    return d, glen


# ------------------------------------------------------------------------------------------------------ read-back
def probe(ffprobe, path):
    cmd = [ffprobe, "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
           "stream=width,height,r_frame_rate,avg_frame_rate,codec_name,profile,level,pix_fmt,color_range,color_space,color_primaries,color_transfer,nb_frames,nb_read_frames,duration",
           "-of", "json", path]
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        return json.loads(r.stdout.decode("utf-8", "replace"))["streams"][0]
    except (OSError, ValueError, KeyError, IndexError, subprocess.TimeoutExpired):
        raise EnvError("ffprobe could not read the finished file")


def read_back(ffprobe, path, expect_frames, log=say):
    """Print and judge the Exercise 2 fields. Returns the list of failed check names."""
    s = probe(ffprobe, path)
    want = [
        ("width", s.get("width"), 1920), ("height", s.get("height"), 1080),
        ("r_frame_rate", s.get("r_frame_rate"), "24/1"), ("avg_frame_rate", s.get("avg_frame_rate"), "24/1"),
        ("codec_name", s.get("codec_name"), "h264"), ("profile", s.get("profile"), "High"), ("pix_fmt", s.get("pix_fmt"), "yuv420p"),
        ("color_range", s.get("color_range"), "tv"), ("color_space", s.get("color_space"), "bt709"),
        ("color_primaries", s.get("color_primaries"), "bt709"), ("color_transfer", s.get("color_transfer"), "bt709"),
        ("frames", int(s.get("nb_read_frames") or s.get("nb_frames") or -1), expect_frames),
    ]
    failed = []
    for name, got, exp in want:
        ok = got == exp
        log("  %s %-16s want %-9s got %s" % ("PASS" if ok else "FAIL", name, exp, got))
        if not ok:
            failed.append(name)
    try:
        dur = float(s.get("duration"))
        ok = abs(dur - expect_frames / float(FPS)) < 0.05
        log("  %s %-16s want %-9s got %.3f" % ("PASS" if ok else "FAIL", "duration_s", "%.3f" % (expect_frames / float(FPS)), dur))
        if not ok:
            failed.append("duration_s")
    except (TypeError, ValueError):
        log("  FAIL duration_s       unreadable")
        failed.append("duration_s")
    return failed


def decode_frame_rgb(ffmpeg, path, index):
    """Decode one frame to an (H, W, 3) uint8 array with the BT.709 limited-range read-back colour_patch.py uses."""
    import numpy as np
    vf = "trim=start_frame=%d:end_frame=%d,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24" % (index, index + 1)
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if r.returncode != 0 or len(r.stdout) != W * H * 3:
        raise EnvError("could not decode a frame of the finished file")
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, 3)


def measure_disc(frame, rgb=DISC_RGB, tol=70.0):
    """Aspect ratio of the disc of colour `rgb` in a decoded frame: (std_x / std_y of the mask, bbox_w / bbox_h, area_px)."""
    import numpy as np
    d = frame.astype(np.float32) - np.array(rgb, np.float32)
    mask = (d * d).sum(axis=2) < tol * tol
    ys, xs = np.nonzero(mask)
    if len(xs) < 200:
        return None
    ratio_std = float(xs.std() / ys.std())
    ratio_box = float((xs.max() - xs.min() + 1) / float(ys.max() - ys.min() + 1))
    return ratio_std, ratio_box, int(len(xs))


def measure_patches(frame, patches, box, half=18):
    """Read the three colour patches of a synthetic still back out of a decoded frame; returns [(name, expected, got, worst_error)]."""
    import numpy as np
    out = []
    for p in patches:
        x, y = project(box, p["centre"])
        x, y = int(round(x)), int(round(y))
        block = frame[max(0, y - half):y + half, max(0, x - half):x + half].reshape(-1, 3).astype(np.float32)
        got = block.mean(axis=0)
        worst = float(np.abs(got - np.array(p["rgb"], np.float32)).max())
        out.append((p["name"], tuple(p["rgb"]), tuple(int(round(v)) for v in got), worst))
    return out


# ------------------------------------------------------------------------------------------------------ the job
def make_moves(names, n):
    out = []
    for k in range(n):
        nm = names[k % len(names)]
        if nm not in MOVES:
            raise Usage("unknown move %s (use: %s)" % (nm, ", ".join(sorted(MOVES))))
        mv = dict(MOVES[nm])
        mv["name"] = nm
        out.append(mv)
    return out


def check_disk(path_dir, need_mb, what):
    try:
        free = shutil.disk_usage(path_dir).free / 1e6
    except OSError:
        return
    if free < need_mb:
        raise EnvError("not enough free disk space for %s: %.0f MB free, about %d MB needed" % (what, free, need_mb))


def run_job(a, stills_paths, selftest_info=None):
    """Shared by the normal run and --selftest. Returns (exit_code, facts)."""
    steps = 5 + (1 if a.proof_zoompan else 0) + (1 if a.selftest else 0)
    sn = [0]

    def step(label):
        sn[0] += 1
        say("[%d/%d] %s ..." % (sn[0], steps, label))

    step("Checking Pillow, numpy and ffmpeg")
    need_libs()
    ffmpeg = resolve_exe(a.ffmpeg)
    if not ffmpeg:
        raise EnvError("ffmpeg not found (%s). Put ffmpeg on PATH, or pass --ffmpeg with its full path; the README has the install line." % os.path.basename(a.ffmpeg))
    ffprobe = ffprobe_for(ffmpeg)
    if not ffprobe:
        raise EnvError("ffprobe not found (it ships beside ffmpeg)")
    online = load_chain(a.chains_file, ONLINE_CHAIN)
    master = load_chain(a.chains_file, MASTER_CHAIN)
    say("  ok: ffmpeg and ffprobe found; chain %s read from %s" % (ONLINE_CHAIN, os.path.basename(a.chains_file)))

    seconds, fade = a.seconds, a.fade
    frames = int(round(seconds * FPS))
    fade_frames = int(round(fade * FPS))
    if not (1 <= fade_frames and 2 * fade_frames <= frames):
        raise Usage("--fade must be at least 1 frame and at most half of --seconds")
    if abs(frames - seconds * FPS) > 1e-6 or abs(fade_frames - fade * FPS) > 1e-6:
        raise Usage("--seconds and --fade must be whole numbers of frames at 24 fps (for example 6 and 1, or 5.5 and 0.5)")
    if not 12 <= a.gate_frames <= GATE_FRAMES:
        raise Usage("--gate-frames must be between 12 and %d" % GATE_FRAMES)

    out = a.out
    out_dir = os.path.dirname(os.path.abspath(out))
    stem = os.path.splitext(os.path.basename(out))[0]
    if not out.lower().endswith(".mp4"):
        raise Usage("--out must end in .mp4")
    for sp in stills_paths:
        if os.path.abspath(sp) == os.path.abspath(out):
            raise Usage("--out is one of the stills; choose another name")
    os.makedirs(out_dir, exist_ok=True)
    gate_path = os.path.join(out_dir, stem + "_push_only.mkv") if a.gate_window else None
    per_frame = 0.6 if a.selftest else 2.6                    # MB per lossless frame: synthetic textures versus real photographs
    check_disk(out_dir, 100 + (a.gate_frames * per_frame if a.gate_window else 0) + (a.gate_frames * per_frame if a.proof_zoompan else 0), "the output files")

    step("Loading %d still(s)" % len(stills_paths))
    loaded = []
    focus = parse_focus(a.focus, len(stills_paths))
    for k, sp in enumerate(stills_paths):
        img, notes = load_still(sp)
        base = base_window(img.size[0], img.size[1], focus[k])
        loaded.append((img, base))
        shape = "already 16:9" if abs(img.size[0] / float(img.size[1]) - ASPECT) < 0.002 else "not 16:9: a 16:9 window is cut, nothing is stretched"
        say("  still %d: %dx%d, %s%s" % (k + 1, img.size[0], img.size[1], shape, ("; " + "; ".join(notes)) if notes else ""))
    moves = make_moves([m.strip() for m in a.moves.split(",") if m.strip()], len(loaded))
    for k, (img, base) in enumerate(loaded):
        mv = moves[k]
        zmax = max(mv["z0"], mv["z1"])
        narrowest = base[2] / zmax
        if narrowest < W:
            say("  WARNING still %d (%s): its closest window is only %d px wide, so it is enlarged to 1920 px (it will look soft on a big screen); use a bigger still or a gentler move" % (k + 1, mv["name"], int(narrowest)))

    work = a.work or tempfile.mkdtemp(prefix="lj_kb_")
    os.makedirs(work, exist_ok=True)
    facts = {}
    try:
        step("Rendering %d moves of %g s with %g s dissolves (the picture is cut and scaled by Pillow, sub-pixel, then encoded by ffmpeg)" % (len(loaded), seconds, fade))
        res = render_movie(ffmpeg, loaded, moves, out, online, master, seconds, fade, work, gate_path, a.gate_frames, a.test_tone)
        facts.update(res)
        say("  ok: %d frames, %.1f s of video in %.0f s" % (res["frames"], res["seconds"], res["render_s"]))
        if gate_path:
            say("  ok: lossless window of move 1, frames %d to %d (%d frames), for mo8_gate.py" % (res["gate_window"][0], res["gate_window"][1] - 1, res["gate_window"][1] - res["gate_window"][0]))

        step("Reading the finished file back with ffprobe")
        failed = read_back(ffprobe, out, res["frames"])
        facts["failed"] = list(failed)

        if a.proof_zoompan:
            step("Making the zoompan PROOF (not for delivery, W-41) so you can see the difference")
            img0, base0 = loaded[0]
            pz = os.path.join(out_dir, stem + "_zoompan_proof.mp4")
            pg = os.path.join(out_dir, stem + "_push_only_zoompan.mkv")
            d, glen = make_zoompan_proof(ffmpeg, img0, base0, online, master, pz, pg, work, 5, 0.15, a.gate_frames)
            facts["zoompan_d"] = d
            say("  ok: %s (5 s, d=%d) and %s (%d frames, lossless)" % (os.path.basename(pz), d, os.path.basename(pg), glen))
            say("  Compare it with your push: the zoompan version jitters by about half a pixel; mo8_gate.py fails it and passes the sub-pixel push.")

        sel_failed = []
        if a.selftest:
            step("Self-test: a drawn disc must stay round, and flat colours must come out right")
            sel_failed = selftest_checks(ffmpeg, out, selftest_info, moves, loaded, res)
            facts["selftest_failed"] = sel_failed
        step("Cleaning up the temporary folder")
    finally:
        if not a.work:
            shutil.rmtree(work, ignore_errors=True)
    allfailed = list(facts.get("failed", [])) + list(facts.get("selftest_failed", []))
    say("RESULT: %s" % ("PASS" if not allfailed else "FAIL (%s)" % ", ".join(allfailed)))
    say("wrote: %s" % os.path.basename(out) + (", %s" % os.path.basename(gate_path) if gate_path else ""))
    return (1 if allfailed else 0), facts


def selftest_checks(ffmpeg, out, info, moves, loaded, res):
    """Disc aspect ratio and colour patches, measured on the DECODED output (not on the source). Returns failed check names."""
    failed = []
    idx = 1                                                   # frame 1 of move 1: the window is still the whole 16:9 window
    frame = decode_frame_rgb(ffmpeg, out, idx)
    m = measure_disc(frame)
    if m is None:
        say("  FAIL disc_aspect       the drawn disc was not found in the output frame")
        failed.append("disc_aspect")
    else:
        rs, rb, area = m
        ok = abs(rs - 1.0) <= 0.01 and abs(rb - 1.0) <= 0.01
        say("  %s disc_aspect       want 1.00 +- 0.01   got %.3f (spread) and %.3f (bounding box); %d px" % ("PASS" if ok else "FAIL", rs, rb, area))
        if not ok:
            failed.append("disc_aspect")
    box = move_box(moves[0], loaded[0][1], idx, res["move_frames"])
    for name, exp, got, worst in measure_patches(frame, info[0]["patches"], box):
        ok = worst <= 3.0
        say("  %s colour_%-8s want %s got %s worst %.1f/255 (limit 3, W-16)" % ("PASS" if ok else "FAIL", name, exp, got, worst))
        if not ok:
            failed.append("colour_" + name)
    return failed


def selftest(a):
    need_libs()
    work = tempfile.mkdtemp(prefix="lj_kb_st_")
    try:
        say("selftest: three synthetic 3000x2000 stills (grey texture, a yellow disc, three flat colour patches); nothing of yours is read.")
        made = make_synthetic_stills(work, 3)
        a.test_tone = True
        a.gate_window = True
        a.selftest = True
        a.proof_zoompan = True                    # so the gate can be shown to pass the sub-pixel push and fail the zoompan one
        if a.gate_frames == GATE_FRAMES and not a._gate_frames_given:
            a.gate_frames = 48
        code, facts = run_job(a, [p for p, _ in made], [i for _, i in made])
        return code
    finally:
        shutil.rmtree(work, ignore_errors=True)


def build_parser():
    p = argparse.ArgumentParser(prog="kenburns_24.py", description="Ken Burns by script at 24 fps (Exercise 2, WP-09). See the header of this file.")
    p.add_argument("stills", nargs="*", help="two or more stills of your own (JPEG, PNG or TIFF), one move each")
    p.add_argument("--out", default=DEFAULT_OUT, help="the .mp4 to write (default renders/ex02/ex02_kenburns.mp4 in the project folder)")
    p.add_argument("--moves", default=",".join(DEFAULT_MOVES), help="comma list of: %s (default push,pan,pull)" % ",".join(sorted(MOVES)))
    p.add_argument("--seconds", type=float, default=DEFAULT_SECONDS, help="seconds per move (default 6)")
    p.add_argument("--fade", type=float, default=DEFAULT_FADE, help="seconds of each dissolve (default 1)")
    p.add_argument("--focus", default=None, help="where the 16:9 window sits in a still that is not 16:9: X,Y from 0 to 1 (one pair, or one per still)")
    p.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"))
    p.add_argument("--chains-file", default=DEFAULT_CHAINS)
    p.add_argument("--proof-zoompan", action="store_true", help="also make the ffmpeg zoompan version (proof only, W-41)")
    p.add_argument("--gate-window", action="store_true", help="also write <name>_push_only.mkv, a lossless window of move 1 for mo8_gate.py")
    p.add_argument("--gate-frames", type=int, default=GATE_FRAMES, help="frames in that window, 12 to 96 (default 96)")
    p.add_argument("--test-tone", action="store_true", help="add a quiet 1 kHz tone at -16 LUFS (for checking the file against the full online profile)")
    p.add_argument("--work", default=None, help="folder for temporary files (default: a new temporary folder, deleted at the end)")
    p.add_argument("--selftest", action="store_true", help="make synthetic stills, run everything, check the result")
    return p


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    a = build_parser().parse_args(argv)
    a._gate_frames_given = any(x == "--gate-frames" or x.startswith("--gate-frames=") for x in argv)
    try:
        if a.selftest:
            if a.stills:
                raise Usage("--selftest takes no stills (it makes its own)")
            if a.out == DEFAULT_OUT:
                a.out = os.path.join(REPO, "renders", "wp09", "ex02.mp4")
            return selftest(a)
        if len(a.stills) < 2:
            raise Usage("give at least two stills (three for the exercise), or --selftest")
        for sp in a.stills:
            if not os.path.isfile(sp):
                raise Usage("a still was not found: %s" % os.path.basename(sp))
        a.selftest = False
        code, _facts = run_job(a, a.stills)
        return code
    except Usage as e:
        print("kenburns_24: %s" % e, file=sys.stderr)
        return 2
    except EnvError as e:
        print("kenburns_24: environment problem: %s" % e, file=sys.stderr)
        return 3
    except pc_helpers.Usage as e:
        print("kenburns_24: %s" % e, file=sys.stderr)
        return 2
    except pc_helpers.EnvError as e:
        print("kenburns_24: environment problem: %s" % e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
