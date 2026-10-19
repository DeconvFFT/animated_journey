#!/usr/bin/env python3
"""spec_check.py: does this finished video file meet its delivery profile? (G6 machinery.) Standard library only. READ-ONLY.

It reads the file with ffprobe and ffmpeg and never changes it. Needs ffmpeg and ffprobe (ffprobe is looked for beside ffmpeg).

WHAT IT CHECKS, per profile (profiles come from pipeline/settings.json plus any --profiles-file; each check has an id that a
failure names):
  container.readable    ffprobe can open it (a truncated MP4 with no moov atom fails here)
  container.type        mp4 profile: not a QuickTime brand; mov profile: QuickTime brand
  container.moov        the moov atom exists (MP4/MOV)
  container.atoms       the top-level atoms run exactly to the end of the file (nothing cut off)
  container.faststart   moov comes before mdat (profiles that ask for +faststart)
  video.streams         exactly one video stream
  video.codec / video.profile / video.level / video.pix_fmt     codec, profile, level and pixel format are the profile's
  video.size            1920x1080
  video.fps             r_frame_rate = avg_frame_rate = 24/1 (W-14)
  video.frame_count     nb_frames = round(duration x 24)
  video.color_range / video.color_space / video.color_primaries / video.color_transfer    the four colour tags (BT.709, limited)
                        ProRes: an 'unknown' range tag is accepted with a note (what ffmpeg 6.1.1 writes)
  video.alpha           alpha profiles: the pixel format carries an alpha plane
  video.bitrate         the average video bit rate is under the profile's cap (venue: 20 Mbps, W-17)
  audio.present / audio.codec / audio.profile / audio.sample_rate / audio.channels / audio.bits
                        48 kHz; master PCM s24le with 24 bits; delivery AAC-LC stereo
  audio.true_peak       ebur128 true peak at or below -1 dBTP over the whole file (W-19, S-28)
  audio.integrated      integrated loudness within +-1 LU of the profile's target (online -16; venue -23, -18 or -16, chosen on 22 Feb)
  integrity.decode      ffmpeg decodes every frame and sample with nothing printed on stderr
  metadata.neutral      no tags except encoder and the structural ones ffmpeg writes (no title, artist, comment, date, location ...);
                        the structural ones include the Matroska muxer's own per-stream DURATION tag (a timecode, e.g. 00:00:02.000000000)

WHAT IT CANNOT SEE: pixel colours. A BT.601 matrix under BT.709 tags passes every check here (the tags are right); only
colour_patch.py catches it. Run both. Loudness is read to 0.1 dB (the ebur128 summary precision).

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows; no admin rights; nothing is installed, downloaded or changed)
  python3 -I pipeline/validators/spec_check.py FILE --profile venue_h264
  python3 -I pipeline/validators/spec_check.py FILE --profile phone_1080 --profiles-file pipeline/phone/profile.json
  python3 -I pipeline/validators/spec_check.py --list-profiles
  python3 -I pipeline/validators/spec_check.py --selftest                      needs only ffmpeg
  py -3 -I pipeline\\validators\\spec_check.py CLIP.mp4 --profile online_h264 --ffmpeg C:\\Tools\\ffmpeg\\bin\\ffmpeg.exe
  Options: --settings F (default pipeline/settings.json), --profiles-file F (repeatable; an object with a "profiles" object),
           --json OUT.json (the verdict), --ffmpeg PATH (FFMPEG), --ffprobe PATH (FFPROBE), --no-loudness, --timeout SECONDS

WHAT IT PRINTS. One line per check (PASS / FAIL), then RESULT. The verdict JSON (schema lj-speccheck/1) has the same checks. It
names the file by its base name only (never a folder), prints metadata values masked (first two characters and asterisks) and
replaces the file's path inside ffmpeg messages with <file>. Files should have neutral names anyway (W-17).

EXIT CODES (build plan 4.3)  0 every check passed   1 a check failed (the failed ids are printed)   2 bad usage or invalid input
(no such file, unknown profile, unreadable profile file)   3 environment problem (ffmpeg or ffprobe not found)

PROFILE SHAPE (pipeline/settings.json "profiles"; see pipeline/validators/README.md): container, faststart, video {codec, profile[],
level[], pix_fmt[], width, height, fps, color_*[], alpha, max_mbps}, audio {required, codec, profile[], sample_rate, channels[],
bits_per_sample}, loudness {true_peak_max_dbtp, integrated_lufs[], tolerance_lu}, metadata "neutral".
UNVERIFIED on Windows and on ffmpeg 9.0.2 until the maker runs it (WP-09's runner). Verified on ffmpeg 6.1.1 (Linux) only.
"""
import argparse
import datetime
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from fractions import Fraction

TOOL_VERSION = 1
SCHEMA = "lj-speccheck/1"
WRONG_FPS = 24 + 1          # the self-test's planted frame-rate defect: one picture a second too many

# tags ffmpeg's muxers write on their own and that carry no personal content
STRUCTURAL_TAGS = {"major_brand", "minor_version", "compatible_brands", "encoder"}
HANDLER_OK = {"videohandler", "soundhandler", "core media video", "core media audio", "apple video media handler",
              "apple sound media handler", "subtitlehandler", "data handler"}
VENDOR_OK = {"[0][0][0][0]", "ffmp", "fmpg", "apl0", "appl"}
ENCODER_RX = re.compile(r"^[A-Za-z0-9 ._+()\-]{1,80}$")
LANG_RX = re.compile(r"^[a-z]{3}$")
# The Matroska muxer writes a per-stream DURATION tag on its own (e.g. 00:00:02.000000000) and -map_metadata -1 cannot remove it. A
# timecode-shaped value carries nothing personal, so it is structural; any other value under that key is still reported.
DURATION_RX = re.compile(r"^\d\d:\d\d:\d\d\.\d+$")
ADDR_RX = re.compile(r"\s*@ 0x[0-9a-fA-F]+")   # ffmpeg prints heap addresses such as [NULL @ 0x55ce...]: not identifying, but never filed


class EnvError(Exception):
    """ffmpeg or ffprobe missing (exit 3)."""


class Usage(Exception):
    """Bad command line or invalid input (exit 2)."""


# ----------------------------------------------------------------------------------------------- helpers
def say(msg=""):
    print(msg)
    sys.stdout.flush()


def read_text_any(path):
    with open(path, "rb") as f:
        b = f.read()
    if b.startswith(b"\xef\xbb\xbf"):
        return b[3:].decode("utf-8")
    if b.startswith(b"\xff\xfe") or b.startswith(b"\xfe\xff"):
        return b.decode("utf-16")
    return b.decode("utf-8")


def write_json(path, obj):
    text = json.dumps(obj, indent=2, ensure_ascii=True) + "\n"
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def resolve_exe(name):
    if not name:
        return None
    if os.path.sep in name or (os.path.altsep and os.path.altsep in name) or os.path.isabs(name):
        return name if os.path.isfile(name) else None
    return shutil.which(name)


def find_tools(ffmpeg_arg, ffprobe_arg):
    ffmpeg = resolve_exe(ffmpeg_arg or os.environ.get("FFMPEG") or "ffmpeg")
    if not ffmpeg:
        raise EnvError("ffmpeg not found. Pass --ffmpeg PATH or set FFMPEG.")
    probe = ffprobe_arg or os.environ.get("FFPROBE")
    probe = resolve_exe(probe) if probe else None
    if (ffprobe_arg or os.environ.get("FFPROBE")) and not probe:
        raise EnvError("the ffprobe you named was not found.")
    if not probe:
        d, b = os.path.split(ffmpeg)
        if b.lower().startswith("ffmpeg"):
            sib = os.path.join(d, "ffprobe" + b[len("ffmpeg"):])
            if os.path.isfile(sib):
                probe = sib
    if not probe:
        probe = shutil.which("ffprobe")
    if not probe:
        raise EnvError("ffprobe not found (it ships beside ffmpeg). Pass --ffprobe PATH or set FFPROBE.")
    return ffmpeg, probe


def run(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except FileNotFoundError:
        raise EnvError("cannot run %s (not found)" % os.path.basename(str(cmd[0])))
    except subprocess.TimeoutExpired:
        return 124, "", "timed out after %s s" % timeout
    except OSError as e:
        raise EnvError("cannot run %s (%s)" % (os.path.basename(str(cmd[0])), e.__class__.__name__))
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def scrub(text, path):
    """Remove the file's path (and folder) from a tool message."""
    if not text:
        return text
    for s in (path, os.path.abspath(path), os.path.dirname(os.path.abspath(path))):
        if s and s not in (".", os.sep):
            text = text.replace(s, "<file>" if s == path or s == os.path.abspath(path) else "<folder>")
    return text.strip()


def decode_messages(stderr, path):
    """ffmpeg's decode complaints as one stable line: path scrubbed, heap addresses removed, duplicates dropped and the messages sorted (threaded
    decoders interleave them in a different order on every run), so a filed verdict JSON is the same each time for the same file."""
    lines = set()
    for ln in scrub(stderr, path).splitlines():
        ln = " ".join(ADDR_RX.sub("", ln).split())
        if ln and not ln.startswith("Last message repeated"):       # a repeat counter depends on how the threads interleaved
            lines.add(ln)
    return " | ".join(sorted(lines))


def mask(value, keep=2, fill="*", cap=8):
    v = str(value)
    if len(v) <= keep:
        return fill * max(1, len(v))
    return v[:keep] + fill * min(len(v) - keep, cap)


def to_fraction(s):
    try:
        f = Fraction(str(s))
        return f if f.denominator != 0 else None
    except (ValueError, ZeroDivisionError):
        return None


# ----------------------------------------------------------------------------------------------- profiles
def load_json_file(path, what):
    try:
        d = json.loads(read_text_any(path))
    except OSError:
        raise Usage("cannot read %s %s" % (what, os.path.basename(path)))
    except ValueError:
        raise Usage("%s %s is not valid JSON" % (what, os.path.basename(path)))
    if not isinstance(d, dict):
        raise Usage("%s %s: expected a JSON object" % (what, os.path.basename(path)))
    return d


def default_settings():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")


def load_profiles(settings_path, extra_files):
    profiles = {}
    sources = {}
    files = []
    if settings_path:
        files.append((settings_path, True))
    for f in extra_files or []:
        files.append((f, False))
    for path, is_settings in files:
        if is_settings and not os.path.isfile(path):
            if extra_files:
                continue                     # a profiles file alone is enough when the settings file is absent
            raise Usage("settings file not found: %s" % os.path.basename(path))
        d = load_json_file(path, "profiles file")
        block = d.get("profiles")
        if not isinstance(block, dict) or not block:
            raise Usage("%s has no \"profiles\" object" % os.path.basename(path))
        for name, prof in block.items():
            if not isinstance(prof, dict) or not isinstance(prof.get("video"), dict):
                raise Usage("profile %s in %s needs a \"video\" object" % (name, os.path.basename(path)))
            if name in profiles:
                raise Usage("profile %s is defined in both %s and %s" % (name, sources[name], os.path.basename(path)))
            profiles[name] = prof
            sources[name] = os.path.basename(path)
    return profiles, sources


# ----------------------------------------------------------------------------------------------- ISO base media atoms
def scan_atoms(path):
    """Walk the top-level boxes of an MP4/MOV. Returns dict(kind, atoms[(type, offset, size)], complete, size, error)."""
    size = os.path.getsize(path)
    out = {"is_iso": False, "major_brand": None, "atoms": [], "complete": False, "file_size": size, "problem": None}
    try:
        f = open(path, "rb")
    except OSError:
        out["problem"] = "cannot open the file"
        return out
    with f:
        pos = 0
        n = 0
        while pos < size and n < 100000:
            f.seek(pos)
            hdr = f.read(8)
            if len(hdr) < 8:
                out["problem"] = "%d stray byte(s) at the end" % len(hdr)
                break
            sz, typ = struct.unpack(">I4s", hdr)
            try:
                typ = typ.decode("latin-1")
            except Exception:
                typ = "????"
            hdrlen = 8
            if sz == 1:
                ext = f.read(8)
                if len(ext) < 8:
                    out["problem"] = "cut inside a box header"
                    break
                sz = struct.unpack(">Q", ext)[0]
                hdrlen = 16
            elif sz == 0:
                sz = size - pos
            if n == 0:
                out["is_iso"] = typ in ("ftyp", "moov", "mdat", "free", "skip", "wide", "styp")
                if typ == "ftyp":
                    out["major_brand"] = f.read(4).decode("latin-1", "replace")
            if sz < hdrlen:
                out["problem"] = "a box at offset %d has an impossible size" % pos
                break
            out["atoms"].append((typ, pos, sz))
            if pos + sz > size:
                out["problem"] = "box '%s' declares %d bytes but only %d remain: the file is cut short" % (typ, sz, size - pos)
                break
            pos += sz
            n += 1
        else:
            out["complete"] = (pos == size)
    if out["problem"] is None and not out["complete"] and out["atoms"] and sum(a[2] for a in out["atoms"]) == size:
        out["complete"] = True
    return out


# ----------------------------------------------------------------------------------------------- probing
PROBE_ENTRIES = ("stream=index,codec_type,codec_name,profile,level,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,"
                 "start_time,bit_rate,color_range,color_space,color_primaries,color_transfer,sample_rate,channels,sample_fmt,"
                 "bits_per_sample,bits_per_raw_sample:stream_tags:format=format_name,duration,size,bit_rate,nb_streams:format_tags")


def ffprobe_json(ffprobe, path, timeout):
    rc, out, err = run([ffprobe, "-v", "error", "-of", "json", "-show_entries", PROBE_ENTRIES, path], timeout=timeout)
    if rc != 0:
        msg = ADDR_RX.sub("", scrub(err, path))
        msg = " ".join(msg.split())
        return None, msg[:240] or "ffprobe exited %d" % rc
    try:
        return json.loads(out), ""
    except ValueError:
        return None, "ffprobe printed no JSON"


def count_packets(ffprobe, path, timeout):
    rc, out, err = run([ffprobe, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                        "-of", "csv=p=0", path], timeout=timeout)
    try:
        return int(out.strip().split(",")[0])
    except (ValueError, IndexError):
        return None


EBU_I = re.compile(r"^\s*I:\s+(-?(?:inf|[0-9]+(?:\.[0-9]+)?))\s+LUFS", re.M)
EBU_P = re.compile(r"^\s*Peak:\s+(-?(?:inf|[0-9]+(?:\.[0-9]+)?))\s+dBFS", re.M)


def measure_loudness(ffmpeg, path, timeout):
    rc, out, err = run([ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-i", path, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       timeout=timeout)
    text = err
    cut = text.rfind("Summary:")
    tail = text[cut:] if cut >= 0 else ""
    mi = EBU_I.findall(tail)
    mp = EBU_P.findall(tail)
    if rc != 0 or not mi or not mp:
        return None, None, "could not read the ebur128 summary (exit %d)" % rc

    def num(s):
        return float("-inf") if s.lstrip("-") == "inf" else float(s)
    return num(mi[-1]), num(mp[-1]), ""


# ----------------------------------------------------------------------------------------------- the checks
class Report(object):
    def __init__(self):
        self.checks = []
        self.notes = []

    def add(self, cid, ok, expected, actual, detail=""):
        self.checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "expected": str(expected), "actual": str(actual), "detail": detail})
        return ok

    def note(self, text):
        self.notes.append(text)

    @property
    def failed(self):
        return [c["id"] for c in self.checks if c["status"] == "FAIL"]


def as_list(v):
    if v is None:
        return None
    return list(v) if isinstance(v, (list, tuple)) else [v]


def check_member(rep, cid, actual, allowed, detail=""):
    allowed = as_list(allowed)
    if allowed is None:
        return
    rep.add(cid, str(actual) in [str(a) for a in allowed], "/".join(str(a) for a in allowed), actual, detail)


def pcm_bits(stream):
    for key in ("bits_per_sample", "bits_per_raw_sample"):
        try:
            v = int(stream.get(key))
            if v > 0:
                return v
        except (TypeError, ValueError):
            pass
    return None


def tag_problems(tags_by_scope):
    """Return a list of (scope, key, masked value) for tags that are not neutral."""
    bad = []
    for scope, tags in tags_by_scope:
        for k, v in (tags or {}).items():
            kl = str(k).lower()
            val = str(v)
            if kl in ("major_brand", "minor_version", "compatible_brands"):
                continue
            if kl == "encoder":
                if not ENCODER_RX.match(val):
                    bad.append((scope, k, mask(val)))
                continue
            if kl == "handler_name":
                if val.lower() not in HANDLER_OK:
                    bad.append((scope, k, mask(val)))
                continue
            if kl == "duration":
                if not DURATION_RX.match(val):
                    bad.append((scope, k, mask(val)))
                continue
            if kl == "language":
                if not LANG_RX.match(val):
                    bad.append((scope, k, mask(val)))
                continue
            if kl == "vendor_id":
                if val.lower() not in VENDOR_OK:
                    bad.append((scope, k, mask(val)))
                continue
            bad.append((scope, k, mask(val)))
    return bad


def check_file(path, pname, prof, ffmpeg, ffprobe, opts):
    rep = Report()
    timeout = opts.get("timeout", 900)
    vp = prof.get("video", {})
    ap = prof.get("audio") or {}
    lp = prof.get("loudness") or {}
    fps = to_fraction(vp.get("fps", "24/1")) or Fraction(24)
    container = prof.get("container")

    # ---- ffprobe first (so the readable check leads), then the container structure, which works even when ffprobe cannot open the file
    atoms = scan_atoms(path)
    is_isobmff = container in ("mp4", "mov")
    probe, why = ffprobe_json(ffprobe, path, timeout)
    if probe is None:
        rep.add("container.readable", False, "ffprobe opens the file", "cannot open", why)
    else:
        rep.add("container.readable", True, "ffprobe opens the file", "ok")
    if is_isobmff:
        types = [a[0] for a in atoms["atoms"]]
        has_moov = "moov" in types
        rep.add("container.moov", has_moov, "moov atom present", "present" if has_moov else "missing",
                "" if has_moov else "no moov atom: the file was cut short or the encode never finished")
        rep.add("container.atoms", atoms["complete"], "atoms run to the end of the file",
                "complete" if atoms["complete"] else "incomplete", atoms["problem"] or "")
        if prof.get("faststart"):
            if has_moov and "mdat" in types:
                ok = types.index("moov") < types.index("mdat")
                rep.add("container.faststart", ok, "moov before mdat", "moov before mdat" if ok else "moov after mdat",
                        "" if ok else "re-mux with -movflags +faststart (or encode with it)")
            else:
                rep.add("container.faststart", False, "moov before mdat", "cannot tell", "moov or mdat missing")
    if probe is None:
        return rep, None
    streams = probe.get("streams", [])
    fmt = probe.get("format", {}) or {}
    vs = [s for s in streams if s.get("codec_type") == "video"]
    au = [s for s in streams if s.get("codec_type") == "audio"]

    if is_isobmff and atoms["is_iso"]:
        brand = (atoms["major_brand"] or "").strip()
        if container == "mp4":
            rep.add("container.type", brand != "qt", "MP4 brand (not QuickTime)", repr(atoms["major_brand"]))
        else:
            rep.add("container.type", brand == "qt", "QuickTime brand", repr(atoms["major_brand"]))
    elif container == "mkv":
        rep.add("container.type", "matroska" in str(fmt.get("format_name", "")), "matroska", fmt.get("format_name"))

    # ---- video
    rep.add("video.streams", len(vs) == 1, "exactly 1 video stream", "%d" % len(vs))
    if vs:
        v = vs[0]
        check_member(rep, "video.codec", v.get("codec_name"), vp.get("codec"))
        check_member(rep, "video.profile", v.get("profile"), vp.get("profile"))
        if vp.get("level") is not None:
            check_member(rep, "video.level", v.get("level"), vp.get("level"))
        pf = v.get("pix_fmt")
        check_member(rep, "video.pix_fmt", pf, vp.get("pix_fmt"))
        if "alpha" in vp:
            has_alpha = bool(re.match(r"^(yuva|gbra|rgba|bgra|argb|abgr|ya)", str(pf)))
            rep.add("video.alpha", has_alpha == bool(vp["alpha"]), "alpha plane" if vp["alpha"] else "no alpha plane",
                    "alpha plane" if has_alpha else "no alpha plane (pix_fmt %s)" % pf)
        w, h = v.get("width"), v.get("height")
        rep.add("video.size", (w, h) == (vp.get("width", 1920), vp.get("height", 1080)),
                "%sx%s" % (vp.get("width", 1920), vp.get("height", 1080)), "%sx%s" % (w, h))
        r_fps, a_fps = to_fraction(v.get("r_frame_rate")), to_fraction(v.get("avg_frame_rate"))
        rep.add("video.fps", r_fps == fps and a_fps == fps, "r_frame_rate = avg_frame_rate = %s" % vp.get("fps", "24/1"),
                "r=%s avg=%s" % (v.get("r_frame_rate"), v.get("avg_frame_rate")))
        # frame count against duration
        nb = None
        try:
            nb = int(v.get("nb_frames"))
        except (TypeError, ValueError):
            nb = count_packets(ffprobe, path, timeout)
        dur = None
        for src in (v.get("duration"), fmt.get("duration")):
            try:
                dur = float(src)
                break
            except (TypeError, ValueError):
                continue
        if nb is None or dur is None:
            rep.add("video.frame_count", False, "nb_frames = round(duration x fps)", "nb_frames=%s duration=%s" % (nb, dur), "cannot read the frame count or duration")
        else:
            exp = int(math.floor(dur * float(fps) + 0.5))
            rep.add("video.frame_count", nb == exp, "nb_frames = round(duration x %s) = %d" % (vp.get("fps", "24/1"), exp),
                    "%d (duration %.3f s)" % (nb, dur),
                    "" if nb == exp else "frames and duration disagree: variable timing, a trimmed edit list, or dropped / duplicated frames")
        # colour tags (ffprobe omits a tag it does not know)
        for key in ("color_range", "color_space", "color_primaries", "color_transfer"):
            allowed = as_list(vp.get(key))
            if allowed is None:
                continue
            got = v.get(key) or "unknown"
            ok = str(got) in [str(a) for a in allowed]
            detail = ""
            if ok and got == "unknown" and key == "color_range":
                detail = "accepted: this ProRes range tag is 'unknown' on ffmpeg 6.1.1"
                rep.note("video.color_range is 'unknown' (accepted for ProRes: ffmpeg 6.1.1 does not write it)")
            rep.add("video." + key, ok, "/".join(str(a) for a in allowed), got, detail)
        # bit rate cap
        cap = vp.get("max_mbps")
        if cap:
            br = None
            for src in (v.get("bit_rate"),):
                try:
                    br = float(src)
                except (TypeError, ValueError):
                    pass
            if br is None and dur and fmt.get("size"):
                try:
                    br = float(fmt["size"]) * 8.0 / dur
                except (TypeError, ValueError):
                    br = None
            if br is None:
                rep.add("video.bitrate", False, "at most %s Mbps" % cap, "unknown")
            else:
                rep.add("video.bitrate", br / 1e6 <= float(cap), "at most %s Mbps" % cap, "%.2f Mbps" % (br / 1e6))

    # ---- audio
    if ap.get("required", True):
        rep.add("audio.present", len(au) >= 1, "at least 1 audio stream", "%d" % len(au))
    if au:
        a = au[0]
        check_member(rep, "audio.codec", a.get("codec_name"), ap.get("codec"))
        if ap.get("profile") is not None:
            check_member(rep, "audio.profile", a.get("profile"), ap.get("profile"))
        if ap.get("sample_rate") is not None:
            rep.add("audio.sample_rate", str(a.get("sample_rate")) == str(ap["sample_rate"]), "%s Hz" % ap["sample_rate"], "%s Hz" % a.get("sample_rate"))
        if ap.get("channels") is not None:
            check_member(rep, "audio.channels", a.get("channels"), ap.get("channels"))
        if ap.get("bits_per_sample") is not None:
            b = pcm_bits(a)
            rep.add("audio.bits", b == ap["bits_per_sample"], "%s-bit" % ap["bits_per_sample"], "%s-bit" % b if b else "not a PCM stream")
        # loudness
        if lp and not opts.get("no_loudness"):
            integ, peak, lwhy = measure_loudness(ffmpeg, path, timeout)
            if integ is None:
                rep.add("audio.true_peak", False, "readable", "unreadable", lwhy)
                if lp.get("integrated_lufs"):
                    rep.add("audio.integrated", False, "readable", "unreadable", lwhy)
            else:
                lim = float(lp.get("true_peak_max_dbtp", -1.0))
                rep.add("audio.true_peak", peak <= lim, "at most %.1f dBTP" % lim, "%s dBTP" % ("-inf" if peak == float("-inf") else "%.1f" % peak),
                        "" if peak <= lim else "the loudest peak is over the ceiling (W-19): lower the master's peak or re-run the limiter")
                targets = as_list(lp.get("integrated_lufs"))
                tol = float(lp.get("tolerance_lu", 1.0))
                if targets:
                    best = min(targets, key=lambda t: abs(integ - float(t))) if integ != float("-inf") else None
                    ok = best is not None and abs(integ - float(best)) <= tol + 1e-9
                    rep.add("audio.integrated", ok, "within +-%.1f LU of %s LUFS" % (tol, "/".join(str(t) for t in targets)),
                            "%s LUFS" % ("-inf" if integ == float("-inf") else "%.1f" % integ),
                            "" if ok else "integrated loudness is not within tolerance of any target for this profile")
                else:
                    rep.note("integrated loudness %.1f LUFS (informational for this profile)" % integ if integ != float("-inf") else "integrated loudness -inf LUFS (silent)")
    elif ap.get("required", True):
        pass

    # ---- integrity
    rc, so, se = run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", path, "-f", "null", "-"], timeout=timeout)
    msg = decode_messages(se, path)
    rep.add("integrity.decode", rc == 0 and not msg, "decodes with nothing on stderr", "clean" if (rc == 0 and not msg) else "problems",
            msg[:240] if msg else ("ffmpeg exit %d" % rc if rc else ""))

    # ---- neutral metadata
    if prof.get("metadata", "neutral") == "neutral":
        scopes = [("format", fmt.get("tags"))] + [("stream %s" % s.get("index"), s.get("tags")) for s in streams]
        bad = tag_problems(scopes)
        rep.add("metadata.neutral", not bad, "no tags except encoder (and structural tags)",
                "clean" if not bad else "; ".join("%s: %s=%s" % b for b in bad[:6]),
                "" if not bad else "strip with -map_metadata -1 (and -metadata:s:v:0 handler_name= if needed)")
    return rep, probe


# ----------------------------------------------------------------------------------------------- verdict
def make_verdict(path, pname, prof, rep, ffmpeg_version):
    failed = rep.failed
    return {"schema": SCHEMA, "tool_version": TOOL_VERSION, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
            "file": os.path.basename(path), "profile": pname, "profile_description": prof.get("description", ""),
            "ffmpeg": ffmpeg_version, "verdict": "FAIL" if failed else "PASS", "failed": failed, "checks": rep.checks, "notes": rep.notes,
            "limits": ["pixels are not read: a BT.601 matrix under BT.709 tags passes here; run colour_patch.py",
                       "loudness is read to 0.1 dB"]}


def ffmpeg_version_token(ffmpeg):
    try:
        rc, out, err = run([ffmpeg, "-hide_banner", "-version"], timeout=60)
    except EnvError:
        return None
    parts = out.splitlines()[0].split() if out else []
    tok = parts[2] if len(parts) > 2 else ""
    m = re.match(r"^n?([0-9]+(?:\.[0-9]+){1,3})", tok)
    return m.group(1) if m else None


def print_report(path, pname, prof, rep):
    say("spec_check: %s against profile %s%s" % (os.path.basename(path), pname, (" (" + prof["description"] + ")") if prof.get("description") else ""))
    for c in rep.checks:
        line = "  %-4s %-22s want %s; got %s" % (c["status"], c["id"], c["expected"], c["actual"])
        if c["detail"]:
            line += "  [" + c["detail"] + "]"
        say(line)
    for n in rep.notes:
        say("  NOTE %s" % n)
    failed = rep.failed
    if failed:
        say("RESULT: FAIL (%d of %d checks failed: %s)" % (len(failed), len(rep.checks), ", ".join(failed)))
    else:
        say("RESULT: PASS (%d checks)" % len(rep.checks))


# ----------------------------------------------------------------------------------------------- self-test
def _lavfi_audio(level_lufs, seconds, burst=None, rate=48000):
    amp = 10 ** (level_lufs / 20.0)
    if burst:
        ex = "%.5f*sin(2*PI*1000*t)+if(between(t,1,1.002),%.3f*sin(2*PI*500*t),0)" % (amp, burst)
        return "aevalsrc=exprs='%s|%s':s=%d:d=%s" % (ex, ex, rate, seconds)
    ex = "%.5f*sin(2*PI*1000*t)" % amp
    return "aevalsrc=exprs=%s|%s:s=%d:d=%s" % (ex, ex, rate, seconds)


def _make_clip(ffmpeg, out, *, fps=24, size="1920x1080", lufs=-16.0, burst=None, rate=48000, extra_meta=None, seconds=2, pix="yuv420p",
               trim=False):
    """A small H.264 + AAC clip made like the project's online chain, with one thing changeable."""
    vf = "scale=out_color_matrix=bt709:out_range=tv,format=%s,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" % pix
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y",
           "-f", "lavfi", "-i", "smptehdbars=size=%s:rate=%d,format=rgb24" % (size, fps),
           "-f", "lavfi", "-i", _lavfi_audio(lufs, seconds, burst, rate),
           "-frames:v", str(fps * seconds), "-vf", vf,
           "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-crf", "18", "-maxrate", "10M", "-bufsize", "20M",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
           "-c:a", "aac", "-b:a", "192k", "-ar", str(rate), "-ac", "2", "-movflags", "+faststart", "-map_metadata", "-1"]
    for k, v in (extra_meta or {}).items():
        cmd += ["-metadata", "%s=%s" % (k, v)]
    cmd.append(out)
    rc, so, se = run(cmd, timeout=300)
    if rc != 0:
        last = se.strip().splitlines()[-1][:160] if se.strip() else "no message"
        raise EnvError("could not make a self-test clip (does this ffmpeg have libx264 and aac?): " + last)
    if trim:
        trimmed = out + ".trim.mp4"
        rc, so, se = run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-ss", "0.5", "-i", out, "-c", "copy", trimmed], timeout=120)
        if rc == 0:
            os.replace(trimmed, out)


def default_chains():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "chains.json")


# A profile for the project's own lossless chain (ffv1_lossless in chains.json). settings.json has no mkv profile today; this one lives here
# so the self-test can prove that the chain's own output passes every check, the Matroska muxer's DURATION tag included.
FFV1_SELFTEST_PROFILE = {
    "description": "self-test: the ffv1_lossless chain's own mkv output (FFV1 4:4:4 10-bit, PCM s24le)", "container": "mkv",
    "video": {"codec": ["ffv1"], "pix_fmt": ["yuv444p10le"], "width": 1920, "height": 1080, "fps": "24/1", "color_range": ["tv"],
              "color_space": ["bt709"], "color_primaries": ["bt709"], "color_transfer": ["bt709"], "alpha": False},
    "audio": {"required": True, "codec": ["pcm_s24le"], "sample_rate": 48000, "channels": [2], "bits_per_sample": 24},
    "loudness": {"true_peak_max_dbtp": -1.0}, "metadata": "neutral"}


def _make_ffv1_clip(ffmpeg, out, chain, seconds=1, fps=24):
    """One second of flat grey through the ffv1_lossless chain exactly as chains.json spells it."""
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y",
           "-f", "lavfi", "-i", "color=c=gray:size=1920x1080:rate=%d,format=rgb24" % fps,
           "-f", "lavfi", "-i", _lavfi_audio(-20.0, seconds),
           "-frames:v", str(fps * seconds), "-vf", chain["vf"]] + [str(a) for a in chain["video_args"]] + \
          ["-map", "0:v:0", "-map", "1:a:0"] + [str(a) for a in chain["audio_args"]] + [out]
    rc, so, se = run(cmd, timeout=300)
    if rc != 0:
        last = se.strip().splitlines()[-1][:160] if se.strip() else "no message"
        raise EnvError("could not make the FFV1 self-test clip: " + last)


def selftest(args):
    ffmpeg, ffprobe = find_tools(args.ffmpeg, args.ffprobe)
    settings = args.settings or default_settings()
    profiles, _src = load_profiles(settings, args.profiles_file)
    if "online_h264" not in profiles:
        raise Usage("the self-test needs the online_h264 profile in pipeline/settings.json")
    prof = profiles["online_h264"]
    say("spec_check --selftest: ffmpeg %s. Needs only ffmpeg and ffprobe; writes only to a temporary folder." % (ffmpeg_version_token(ffmpeg) or "?"))
    work = tempfile.mkdtemp(prefix="lj_sc_self_")
    fails = 0
    try:
        def case(name, want_fail_ids, **kw):
            nonlocal fails
            out = os.path.join(work, name + ".mp4")
            _make_clip(ffmpeg, out, **kw)
            rep, _p = check_file(out, "online_h264", prof, ffmpeg, ffprobe, {"timeout": 300})
            if want_fail_ids is None:
                ok = not rep.failed
                detail = "exit 0, all %d checks pass" % len(rep.checks) if ok else "unexpected failures: " + ", ".join(rep.failed)
            else:
                ok = all(w in rep.failed for w in want_fail_ids)
                detail = "exit 1 naming %s" % ", ".join(want_fail_ids) if ok else "failed ids were [%s], wanted %s" % (", ".join(rep.failed), ", ".join(want_fail_ids))
            say("  %-5s %-34s %s" % ("PASS" if ok else "FAIL", name, detail))
            if not ok:
                fails += 1
            try:
                os.remove(out)
            except OSError:
                pass
        case("good_online_clip", None)
        case("planted_wrong_frame_rate", ["video.fps"], fps=WRONG_FPS)
        case("planted_44k1_audio", ["audio.sample_rate"], rate=44100)
        case("planted_title_tag", ["metadata.neutral"], extra_meta={"title": "Selftest Title"})
        case("planted_loud_peak", ["audio.true_peak"], burst=0.98)
        case("planted_frame_count_vs_duration", ["video.frame_count"], trim=True)
        # the project's own lossless chain: its mkv carries the muxer's per-stream DURATION tag, which must count as structural (review r1)
        chains = load_json_file(default_chains(), "chains file").get("chains") or {}
        if "ffv1_lossless" not in chains:
            raise Usage("the self-test needs the ffv1_lossless chain in pipeline/lib/chains.json")
        mkv = os.path.join(work, "good_ffv1_lossless.mkv")
        _make_ffv1_clip(ffmpeg, mkv, chains["ffv1_lossless"])
        rep, probe = check_file(mkv, "ffv1_selftest", FFV1_SELFTEST_PROFILE, ffmpeg, ffprobe, {"timeout": 300})
        tagged = any(isinstance(s.get("tags"), dict) and any(str(k).lower() == "duration" for k in s["tags"]) for s in (probe or {}).get("streams", []))
        ok = not rep.failed
        say("  %-5s %-34s %s" % ("PASS" if ok else "FAIL", "good_ffv1_lossless_mkv",
                                 ("exit 0, all %d checks pass%s" % (len(rep.checks), " (the muxer's DURATION tag was present and accepted)" if tagged else " (this build wrote no DURATION tag)"))
                                 if ok else "unexpected failures: " + ", ".join(rep.failed)))
        if not ok:
            fails += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    say("spec_check --selftest: %s" % ("ALL PASS" if not fails else "%d FAILED" % fails))
    return 0 if not fails else 1


# ----------------------------------------------------------------------------------------------- main
def build_parser():
    p = argparse.ArgumentParser(prog="spec_check.py", description="Check a finished video file against a delivery profile. See the header of this file.")
    p.add_argument("file", nargs="?", help="the video file to check")
    p.add_argument("--profile", help="profile name (see --list-profiles)")
    p.add_argument("--settings", default=None, help="settings file with the profiles (default pipeline/settings.json)")
    p.add_argument("--profiles-file", action="append", help="another profiles file, for example the phone profile (repeatable)")
    p.add_argument("--json", default=None, help="write the verdict JSON here")
    p.add_argument("--ffmpeg", default=None, help="ffmpeg path (default FFMPEG or ffmpeg on PATH)")
    p.add_argument("--ffprobe", default=None, help="ffprobe path (default FFPROBE, beside ffmpeg, or on PATH)")
    p.add_argument("--no-loudness", action="store_true", help="skip the ebur128 pass (fast; the verdict says so)")
    p.add_argument("--timeout", type=int, default=900, help="seconds allowed for each ffmpeg / ffprobe call")
    p.add_argument("--list-profiles", action="store_true", help="print the profile names and exit")
    p.add_argument("--selftest", action="store_true", help="mechanism tests; needs only ffmpeg")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            return selftest(args)
        settings = args.settings or default_settings()
        profiles, sources = load_profiles(settings, args.profiles_file)
        if args.list_profiles:
            for name in sorted(profiles):
                say("%-28s %-22s %s" % (name, sources[name], profiles[name].get("description", "")))
            return 0
        if not args.file or not args.profile:
            raise Usage("usage: spec_check.py FILE --profile NAME   (profiles: %s)" % ", ".join(sorted(profiles)))
        if args.profile not in profiles:
            raise Usage("unknown profile %s (known: %s)" % (args.profile, ", ".join(sorted(profiles))))
        if not os.path.isfile(args.file):
            raise Usage("no such file: %s" % os.path.basename(args.file))
        ffmpeg, ffprobe = find_tools(args.ffmpeg, args.ffprobe)
        prof = profiles[args.profile]
        rep, _probe = check_file(args.file, args.profile, prof, ffmpeg, ffprobe, {"timeout": args.timeout, "no_loudness": args.no_loudness})
        if args.no_loudness:
            rep.note("loudness was NOT checked (--no-loudness)")
        print_report(args.file, args.profile, prof, rep)
        verdict = make_verdict(args.file, args.profile, prof, rep, ffmpeg_version_token(ffmpeg))
        if args.json:
            write_json(args.json, verdict)
        return 1 if rep.failed else 0
    except Usage as e:
        print("spec_check: %s" % e, file=sys.stderr)
        return 2
    except EnvError as e:
        print("spec_check: environment problem: %s" % e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
