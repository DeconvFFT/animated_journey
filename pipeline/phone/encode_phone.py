#!/usr/bin/env python3
"""encode_phone.py: make the phone file (PH1 / PH2) from the 16:9 master, with the captions burned in. WP-08, decision D-27.

  python3 -I pipeline/phone/encode_phone.py MASTER CAPTIONS.srt OUTPUT.mp4 [--profile phone_1080|phone_720_share] [--style phone|venue_fs23]
  Windows (UNVERIFIED, never run there):  py -3 -I pipeline\\phone\\encode_phone.py MASTER CAPTIONS.srt OUTPUT.mp4
  Usual way, inside the disk guard:      bash pipeline/phone/encode_phone.sh MASTER CAPTIONS.srt OUTPUT.mp4

WHAT IT DOES, in the order it prints it
  1. reads pipeline/phone/profile.json (the chain, the caption style) and probes the master: it must be 16:9 1920x1080 at 24 fps with sound;
  2. makes a throw-away work folder and copies in the caption file (as caps.srt) and the font files it needs (as fonts/*);
  3. turns the SRT into an ASS file with the profile's phone caption style (the same 384x288 canvas ffmpeg gives an SRT, so FontSize means what
     the settings card means; a header line 'YCbCr Matrix: TV.709'); one font per script (from pipeline/lib/libs.lock.json);
  4. burns the captions with the `ass` filter, then runs the chain's vf (scale, format, setparams) and encodes the video;
  5. audio: two-pass loudnorm to -16 LUFS / -1 dBTP (second pass linear), AAC, then measures the AAC file and repeats with a lower true-peak target if
     the file reads above -1.0 dBTP;
  6. muxes with +faststart and no metadata, then checks the result (size, rate, frame count, tags, bit rate against the cap + 10%, moov before mdat,
     loudness) and writes OUTPUT.phone.json (a sidecar for phone_check.py) and OUTPUT.ass (the caption file as burned).

WHY THE `ass` FILTER AND RELATIVE NAMES. ffmpeg before n9.0 draws the `subtitles` filter in simple shaping and breaks Indic conjuncts and vowel signs
without any warning (W-75). The `ass` filter on an ASS file shapes correctly on 6.1.1 (measured, build/evidence/wp08/shaping_paths.json), so one path
serves every script. ffmpeg runs with its working folder set to the work folder and only RELATIVE file names (caps.ass, fonts) inside the filter string,
so a Windows drive-letter colon never reaches the filter (the caption_xheight round-2 lesson). The master and the output are ordinary arguments.

WHAT IT NEVER TOUCHES. It never writes to the master, never edits the caption file, never uploads anything, and never uses the network. It writes only
OUTPUT, OUTPUT.phone.json, OUTPUT.ass and its own work folder (removed at the end unless --keep-work). It prints base names only, no folder paths, no user
or host names. Caption text is never printed (a real film's captions are private); only cue numbers and character counts.

OPTIONS  --profile NAME (phone_1080)   --style NAME (profile caption.default_style)   --no-captions   --layout FILE (a scene report's layout, copied into the sidecar)
         --fontsdir DIR (extra .ttf/.otf/.woff files copied into the work folder's fonts)   --family SCRIPT=NAME (repeatable; font family name for a script)
         --ffmpeg PATH (or env FFMPEG)   --ffprobe PATH   --work DIR   --keep-work   --allow-long-lines   --overwrite   --dry-run (print the plan, run nothing)   --no-sidecar
EXIT     0 done and every own check passed; 1 the file was made but one of its own checks failed (a finding); 2 bad usage or invalid input; 3 environment
         problem (a tool or font is missing). Standard library only (python 3.9 or later) plus ffmpeg and ffprobe.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PROFILE_PATH = os.path.join(HERE, "profile.json")
LOCK_PATH = os.path.join(ROOT, "pipeline", "lib", "libs.lock.json")
VENDOR = os.path.join(ROOT, "vendor")


class Usage(Exception):
    pass


class Env(Exception):
    pass


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


# ------------------------------------------------------------------------------------------------ small helpers
def read_json(path):
    try:
        with open(path, "rb") as f:
            raw = f.read()
        for bom, enc in ((b"\xef\xbb\xbf", "utf-8"), (b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16")):
            if raw.startswith(bom):
                return json.loads(raw.decode(enc).lstrip("\ufeff"))
        return json.loads(raw.decode("utf-8"))
    except (OSError, ValueError) as e:
        raise Usage("cannot read %s (%s)" % (os.path.basename(path), e.__class__.__name__))


def write_json(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def run(cmd, cwd=None, timeout=1800):
    """Run an argument list (never a shell string). Returns (returncode, stdout bytes, stderr bytes)."""
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        raise Env("tool not found: %s" % os.path.basename(str(cmd[0])))
    except subprocess.TimeoutExpired:
        raise Env("a tool ran longer than %d s: %s" % (timeout, os.path.basename(str(cmd[0]))))
    return p.returncode, p.stdout, p.stderr


def tail(b, n=6):
    lines = [l for l in b.decode("utf-8", "replace").splitlines() if l.strip()]
    return " | ".join(lines[-n:])[:600]


def resolve_tool(explicit, env_name, default):
    exe = explicit or os.environ.get(env_name) or default
    if os.path.dirname(exe) and os.path.isfile(exe):
        return exe
    found = shutil.which(exe)
    if not found:
        raise Env("%s not found (put it on PATH, or give --%s PATH / set %s)" % (default, default, env_name))
    return found


def ffprobe_for(ffmpeg, explicit):
    if explicit or os.environ.get("FFPROBE"):
        return resolve_tool(explicit, "FFPROBE", "ffprobe")
    d, base = os.path.dirname(ffmpeg), os.path.basename(ffmpeg)
    cand = os.path.join(d, base.replace("ffmpeg", "ffprobe")) if d else None
    if cand and os.path.isfile(cand):
        return cand
    return resolve_tool(None, "FFPROBE", "ffprobe")


def ffmpeg_version(ffmpeg):
    rc, out, err = run([ffmpeg, "-hide_banner", "-version"], timeout=60)
    m = re.search(r"ffmpeg version (\S+)", out.decode("utf-8", "replace"))
    return m.group(1) if m else None


def probe(ffprobe, path):
    rc, out, err = run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", path], timeout=120)
    if rc != 0:
        raise Usage("ffprobe could not read %s: %s" % (os.path.basename(path), tail(err, 2)))
    d = json.loads(out.decode("utf-8", "replace"))
    v = [s for s in d.get("streams", []) if s.get("codec_type") == "video"]
    a = [s for s in d.get("streams", []) if s.get("codec_type") == "audio"]
    return {"video": v[0] if v else None, "audio": a[0] if a else None, "format": d.get("format", {})}


def fps_of(stream):
    for key in ("avg_frame_rate", "r_frame_rate"):
        v = stream.get(key, "0/1")
        try:
            n, d = v.split("/")
            if int(d) != 0:
                return int(n), int(d)
        except ValueError:
            pass
    return 0, 1


def mp4_atoms(path):
    """Top-level boxes of an MP4 as [(type, offset)]. Reads headers only."""
    out = []
    size_total = os.path.getsize(path)
    with open(path, "rb") as f:
        pos = 0
        while pos + 8 <= size_total:
            f.seek(pos)
            hdr = f.read(8)
            if len(hdr) < 8:
                break
            size, typ = struct.unpack(">I4s", hdr)
            hlen = 8
            if size == 1:
                big = f.read(8)
                if len(big) < 8:
                    break
                size = struct.unpack(">Q", big)[0]
                hlen = 16
            elif size == 0:
                size = size_total - pos
            out.append((typ.decode("latin-1"), pos))
            if size < hlen:
                break
            pos += size
    return out


# ------------------------------------------------------------------------------------------------ profile, fonts, scripts
def load_profile(path=None):
    p = read_json(path or PROFILE_PATH)
    for k in ("chains", "profiles", "caption", "encode"):
        if k not in p:
            raise Usage("profile.json has no '%s' object" % k)
    return p


SCRIPT_RANGES = [("devanagari", 0x0900, 0x097F), ("devanagari", 0xA8E0, 0xA8FF), ("bengali", 0x0980, 0x09FF), ("gujarati", 0x0A80, 0x0AFF),
                 ("tamil", 0x0B80, 0x0BFF), ("telugu", 0x0C00, 0x0C7F), ("kannada", 0x0C80, 0x0CFF), ("malayalam", 0x0D00, 0x0D7F)]


def script_of_char(ch):
    cp = ord(ch)
    for name, lo, hi in SCRIPT_RANGES:
        if lo <= cp <= hi:
            return name
    return None


def script_of_text(text):
    """The Indic script that has the most letters in the text, else 'latin'."""
    counts = {}
    for ch in text:
        s = script_of_char(ch)
        if s:
            counts[s] = counts.get(s, 0) + 1
    if not counts:
        return "latin"
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def mixed_scripts(text):
    has_latin = any(ch.isalpha() and ord(ch) < 0x250 for ch in text)
    indic = set(script_of_char(ch) for ch in text if script_of_char(ch))
    return len(indic) + (1 if has_latin else 0) > 1


def count_chars(line):
    """Characters a reader counts: code points that are not combining marks (vowel signs, viramas, nuktas, anusvara)."""
    return len([c for c in line if not unicodedata.category(c).startswith("M")])


def font_for_script(script, lock=None, vendor=VENDOR):
    """(family, file path) of a libass-readable regular-weight font for the script, from libs.lock.json. Raises Env if there is none."""
    lock = lock if lock is not None else read_json(LOCK_PATH)
    best = None
    for f in lock.get("fonts", []):
        if f.get("role") == "script_family" and script in (f.get("scripts") or []):
            for face in f.get("faces", []) or []:
                files = face.get("files") or {}
                if str(face.get("weight")) != "400" or "woff" not in files:
                    continue
                rank = 0 if face.get("subset") == script else 1
                cand = (rank, f["family"], os.path.join(vendor, files["woff"]["to"]))
                if best is None or cand < best:
                    best = cand
    if best is None:
        raise Env("no fetched, libass-readable font for the script '%s' (libs.lock.json has none: run pipeline/lib/fetch_libs.sh --scripts %s, then add the strings and marks to test_strings.json)" % (script, script))
    if not os.path.isfile(best[2]):
        raise Env("the font file for '%s' is not in vendor/ (run pipeline/lib/fetch_libs.sh)" % script)
    return best[1], best[2]


# ------------------------------------------------------------------------------------------------ SRT -> ASS
TIME_RE = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*(\d+):(\d{2}):(\d{2})[,.](\d{1,3})")


def _ms(h, m, s, frac):
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int((frac + "00")[:3])


def parse_srt(text):
    """Cues as [{'start_ms','end_ms','lines':[...]}]. Reads UTF-8 text that may have a BOM and CRLF line ends."""
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    cues = []
    for block in re.split(r"\n[ \t]*\n", text.strip()):
        lines = block.split("\n")
        i = 0
        if lines and re.fullmatch(r"\s*\d+\s*", lines[0]):
            i = 1
        if i >= len(lines):
            continue
        m = TIME_RE.search(lines[i])
        if not m:
            raise Usage("caption file: a block has no 'start --> end' line (block %d)" % (len(cues) + 1))
        start, end = _ms(*m.groups()[:4]), _ms(*m.groups()[4:])
        body = [l.strip() for l in lines[i + 1:] if l.strip()]
        if end <= start:
            raise Usage("caption file: cue %d ends before it starts" % (len(cues) + 1))
        cues.append({"start_ms": start, "end_ms": end, "lines": body})
    if not cues:
        raise Usage("caption file: no cues found")
    return cues


def _ass_time(ms):
    cs = int(round(ms / 10.0))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return "%d:%02d:%02d.%02d" % (h, m, s, c)


def _ass_text(line):
    """One caption line to ASS text: <i>, <b>, <u> become override tags, other tags go, braces are escaped."""
    line = re.sub(r"<\s*([ibu])\s*>", lambda m: "{\\%s1}" % m.group(1), line, flags=re.I)
    line = re.sub(r"<\s*/\s*([ibu])\s*>", lambda m: "{\\%s0}" % m.group(1), line, flags=re.I)
    parts = re.split(r"(\{\\[ibu][01]\})", line)
    out = []
    for p in parts:
        if re.fullmatch(r"\{\\[ibu][01]\}", p):
            out.append(p)
        else:
            p = re.sub(r"<[^>]*>", "", p).replace("\\", "").replace("{", "(").replace("}", ")")
            out.append(p)
    return "".join(out)


def plain_line(line):
    """The caption line as a reader sees it (tags removed), for counting."""
    return re.sub(r"<[^>]*>", "", line).strip()


def _bgr(rrggbb):
    r, g, b = rrggbb[0:2], rrggbb[2:4], rrggbb[4:6]
    return "&H00%s%s%s" % (b.upper(), g.upper(), r.upper())


def style_name(script):
    return "ljphone-" + script


def build_ass(cues, style, families, play=(384, 288), ycbcr="TV.709", wrap_style=2, scaled="yes", outline_override=None):
    """The ASS text for the cues. style: a profile caption style dict. families: {script: font family name} for every script in the cues.
    One ASS style per script, sized by style['font_size_by_script'][script] or style['font_size']."""
    fs_by = style.get("font_size_by_script") or {}
    scripts = sorted(set(script_of_text(l) for c in cues for l in c["lines"]) | {"latin"})
    outline = style.get("outline", 0.8) if outline_override is None else outline_override
    head = ["[Script Info]", "; made by encode_phone.py from an SRT; the text is the caption file's own, nothing is invented", "ScriptType: v4.00+",
            "PlayResX: %d" % play[0], "PlayResY: %d" % play[1], "WrapStyle: %d" % wrap_style, "ScaledBorderAndShadow: %s" % scaled,
            "Kerning: yes", "YCbCr Matrix: %s" % ycbcr, "", "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"]
    for sc in scripts:
        fam = families.get(sc)
        if not fam:
            raise Env("no font family for the script '%s'" % sc)
        fs = fs_by.get(sc, style["font_size"])
        head.append("Style: %s,%s,%s,%s,%s,%s,&H00000000,%d,0,0,0,100,100,0,0,1,%s,%s,2,%d,%d,%d,1" % (
            style_name(sc), fam, ("%g" % fs), _bgr(style.get("primary_colour", "FFFFFF")), _bgr(style.get("primary_colour", "FFFFFF")),
            _bgr(style.get("outline_colour", "000000")), int(style.get("bold", 0)), ("%g" % outline), ("%g" % style.get("shadow", 0)),
            int(style.get("margin_lr", 0)), int(style.get("margin_lr", 0)), int(style["margin_v"])))
    head += ["", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for c in cues:
        sc0 = script_of_text(c["lines"][0])
        texts = []
        for k, line in enumerate(c["lines"]):
            sc = script_of_text(line)
            pre = "{\\r%s}" % style_name(sc) if (k > 0 and sc != sc0) else ""
            texts.append(pre + _ass_text(line))
        head.append("Dialogue: 0,%s,%s,%s,,0,0,0,,%s" % (_ass_time(c["start_ms"]), _ass_time(c["end_ms"]), style_name(sc0), "\\N".join(texts)))
    return "\n".join(head) + "\n"


def check_caption_limits(cues, style, allow_long=False):
    """Lines and characters against the style. Returns a list of problem strings (cue numbers and counts only, never the text)."""
    problems = []
    for i, c in enumerate(cues, 1):
        if len(c["lines"]) > style["max_lines"]:
            problems.append("cue %d has %d lines (the %s style allows %d)" % (i, len(c["lines"]), "caption", style["max_lines"]))
        for k, line in enumerate(c["lines"], 1):
            n = count_chars(plain_line(line))
            if n > style["max_chars_per_line"]:
                problems.append("cue %d line %d has %d characters (limit %d)" % (i, k, n, style["max_chars_per_line"]))
            if mixed_scripts(plain_line(line)):
                problems.append("cue %d line %d mixes scripts (W-18: one script per line; a mixed line leans on font fallback and is not tested)" % (i, k))
    return problems


def prepare_fonts(workdir, scripts, fontsdir=None, family_overrides=None, lock=None):
    """Copy the fonts the cues need into <workdir>/fonts and return {script: family}."""
    fdir = os.path.join(workdir, "fonts")
    os.makedirs(fdir, exist_ok=True)
    fams = {}
    family_overrides = family_overrides or {}
    for sc in sorted(set(scripts) | {"latin"}):
        if sc in family_overrides:
            fams[sc] = family_overrides[sc]
            continue
        fam, path = font_for_script(sc, lock)
        shutil.copyfile(path, os.path.join(fdir, os.path.basename(path)))
        fams[sc] = fam
    if fontsdir:
        if not os.path.isdir(fontsdir):
            raise Usage("--fontsdir is not a folder")
        for name in sorted(os.listdir(fontsdir)):
            if name.lower().endswith((".ttf", ".otf", ".ttc", ".woff")):
                shutil.copyfile(os.path.join(fontsdir, name), os.path.join(fdir, name))
    return fams


# ------------------------------------------------------------------------------------------------ audio
def parse_loudnorm_json(stderr_bytes):
    txt = stderr_bytes.decode("utf-8", "replace")
    i = txt.rfind("{")
    j = txt.rfind("}")
    if i < 0 or j < i:
        raise Env("loudnorm printed no measurement")
    d = json.loads(txt[i:j + 1])
    return {k: float(d[k]) for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}


def measure_ebur128(ffmpeg, path):
    """(integrated LUFS, true peak dBTP) of the audio of a file, by ebur128 with peak=true."""
    rc, out, err = run([ffmpeg, "-hide_banner", "-nostats", "-nostdin", "-i", path, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"], timeout=600)
    txt = err.decode("utf-8", "replace")
    k = txt.rfind("Summary:")
    if rc != 0 or k < 0:
        raise Env("could not measure loudness: %s" % tail(err, 2))
    s = txt[k:]
    mi = re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", s)
    mp = re.search(r"True peak:\s*\n\s*Peak:\s+(-?[\d.]+|-inf)\s+dBFS", s)
    if not mi or not mp:
        raise Env("could not read the ebur128 summary")
    return float(mi.group(1)), float(mp.group(1))


def encode_audio(ffmpeg, src_abs, workdir, chain, enc, say_fn):
    """Two-pass loudnorm then AAC into workdir/audio.m4a. Returns a dict with the measured result of the final audio."""
    lo = enc["loudness"]
    target_i, tp = lo["integrated_lufs"], lo["target_tp_start_dbtp"]
    final = None
    for attempt in range(1, int(lo["retries"]) + 2):
        base = "loudnorm=I=%g:TP=%g:LRA=%g" % (target_i, tp, lo["lra"])
        say_fn("      loudnorm pass 1 (measure), target %g LUFS, true-peak target %g dBTP" % (target_i, tp))
        rc, out, err = run([ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", src_abs, "-vn", "-map", "0:a:0", "-af", base + ":print_format=json", "-f", "null", "-"], cwd=workdir)
        if rc != 0:
            raise Env("loudnorm pass 1 failed: %s" % tail(err, 3))
        m = parse_loudnorm_json(err)
        if m["input_i"] < -70:
            raise Usage("the master's sound is silent (nothing to normalise)")
        af = (base + ":measured_I=%.2f:measured_TP=%.2f:measured_LRA=%.2f:measured_thresh=%.2f:offset=%.2f:linear=true,aresample=48000"
              % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
        say_fn("      loudnorm pass 2 (linear) then AAC: measured input %.1f LUFS, %.1f dBTP" % (m["input_i"], m["input_tp"]))
        rc, out, err = run([ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", src_abs, "-vn", "-map", "0:a:0", "-af", af] + [str(a) for a in chain["audio_args"]] + ["-map_metadata", "-1", "audio.m4a"], cwd=workdir)
        if rc != 0:
            raise Env("audio encode failed: %s" % tail(err, 3))
        lufs, peak = measure_ebur128(ffmpeg, os.path.join(workdir, "audio.m4a"))
        say_fn("      AAC file measures %.1f LUFS, %.1f dBTP" % (lufs, peak))
        final = {"integrated_lufs": lufs, "true_peak_dbtp": peak, "tp_target_dbtp": tp, "passes": attempt, "input_lufs": m["input_i"], "input_tp_dbtp": m["input_tp"]}
        if peak <= lo["true_peak_dbtp"] + 1e-9:
            return final
        tp -= lo["target_tp_step_db"]
        say_fn("      above %g dBTP after AAC: lowering the true-peak target to %g and repeating" % (lo["true_peak_dbtp"], tp))
    return final


# ------------------------------------------------------------------------------------------------ main
def layout_of(obj):
    """The scene layout from a render.mjs report (its scene_report.layout), from a scene report ({'layout': ...}) or from the layout itself."""
    obj = obj.get("scene_report", obj) or obj
    return obj.get("layout", obj)


def build_parser():
    p = argparse.ArgumentParser(prog="encode_phone.py", description="Make the phone file from the 16:9 master with burned-in captions (WP-08).", add_help=True)
    p.add_argument("master", help="the master (ProRes .mov) or any 1920x1080 24 fps clip with sound")
    p.add_argument("captions", nargs="?", help="SRT file (UTF-8); omit with --no-captions")
    p.add_argument("output", help="OUTPUT.mp4")
    p.add_argument("--profile", default="phone_1080")
    p.add_argument("--style", default=None)
    p.add_argument("--no-captions", action="store_true")
    p.add_argument("--layout", default=None)
    p.add_argument("--fontsdir", default=None)
    p.add_argument("--family", action="append", default=[], help="SCRIPT=FAMILY (repeatable)")
    p.add_argument("--ffmpeg", default=None)
    p.add_argument("--ffprobe", default=None)
    p.add_argument("--work", default=None)
    p.add_argument("--keep-work", action="store_true")
    p.add_argument("--allow-long-lines", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-sidecar", action="store_true")
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    steps = 9
    n = [0]

    def step(msg):
        n[0] += 1
        say("[%d/%d] %s ..." % (n[0], steps, msg))

    work = None
    try:
        # --- 1. profile and inputs
        step("Reading profile.json and the options")
        if a.no_captions and a.captions is not None:
            raise Usage("--no-captions and a caption file were both given")
        prof = load_profile()
        if a.profile not in prof["chains"] or a.profile not in prof["profiles"]:
            raise Usage("profile '%s' is not in profile.json (known: %s)" % (a.profile, ", ".join(sorted(prof["profiles"]))))
        chain, pspec = prof["chains"][a.profile], prof["profiles"][a.profile]
        cap = prof["caption"]
        style_key = a.style or cap["default_style"]
        if style_key not in cap["styles"]:
            raise Usage("caption style '%s' is not in profile.json (known: %s)" % (style_key, ", ".join(sorted(cap["styles"]))))
        style = cap["styles"][style_key]
        if style_key != cap["default_style"]:
            say("      NOTE: caption style '%s' is not the phone deliverable style ('%s')" % (style_key, cap["default_style"]))
        master = os.path.abspath(a.master)
        out_abs = os.path.abspath(a.output)
        if not os.path.isfile(master):
            raise Usage("the master %s does not exist" % os.path.basename(a.master))
        if os.path.normcase(master) == os.path.normcase(out_abs):
            raise Usage("the output is the master: refusing to overwrite it")
        if os.path.exists(out_abs) and not a.overwrite:
            raise Usage("%s already exists (use --overwrite)" % os.path.basename(a.output))
        cues, srt_text = None, None
        if not a.no_captions:
            if not a.captions:
                raise Usage("give a caption file, or --no-captions")
            if not os.path.isfile(a.captions):
                raise Usage("the caption file %s does not exist" % os.path.basename(a.captions))
            with open(a.captions, "rb") as f:
                srt_text = f.read().decode("utf-8-sig", "replace")
            cues = parse_srt(srt_text)
            probs = check_caption_limits(cues, style, a.allow_long_lines)
            if probs and not a.allow_long_lines:
                raise Usage("captions break the %s style: %s (re-break the lines, or --allow-long-lines)" % (style_key, "; ".join(probs[:6])))
            for pr in probs:
                say("      WARNING: " + pr)
            say("      %d cues; scripts: %s; style %s: FontSize %g, MarginV %g, outline %g, at most %d characters and %d lines" % (
                len(cues), ", ".join(sorted(set(script_of_text(l) for c in cues for l in c["lines"]))), style_key, style["font_size"], style["margin_v"],
                style["outline"], style["max_chars_per_line"], style["max_lines"]))
        layout = read_json(a.layout) if a.layout else None
        fam_over = {}
        for item in a.family:
            if "=" not in item:
                raise Usage("--family wants SCRIPT=FAMILY")
            k, v = item.split("=", 1)
            fam_over[k.strip()] = v.strip()
        ffmpeg = resolve_tool(a.ffmpeg, "FFMPEG", "ffmpeg")
        ffprobe = ffprobe_for(ffmpeg, a.ffprobe)
        say("      ffmpeg %s" % (ffmpeg_version(ffmpeg) or "(version unreadable)"))

        # --- 2. probe the master
        step("Probing the master (%s)" % os.path.basename(a.master))
        pr = probe(ffprobe, master)
        v, au = pr["video"], pr["audio"]
        if v is None:
            raise Usage("the master has no video stream")
        w, h = int(v["width"]), int(v["height"])
        fn, fd = fps_of(v)
        if (w, h) != (1920, 1080):
            raise Usage("the master is %dx%d; the phone file is cut from the 1920x1080 master (no reframing, no crop)" % (w, h))
        if (fn, fd) != (24, 1):
            raise Usage("the master runs at %d/%d fps; the phone file keeps the film's 24 fps" % (fn, fd))
        if au is None:
            raise Usage("the master has no sound; the phone profile needs an audio track (-16 LUFS / -1 dBTP)")
        nb = int(v.get("nb_frames") or 0)
        dur = float(pr["format"].get("duration") or v.get("duration") or 0)
        say("      %dx%d, 24 fps, %s %s, %d frames, %.2f s; audio %s %s Hz" % (w, h, v.get("codec_name"), v.get("pix_fmt"), nb, dur, au.get("codec_name"), au.get("sample_rate")))
        tagged = v.get("color_space") == "bt709"
        if not tagged:
            say("      NOTE: the master's colour_space tag is '%s', not bt709: the burn-in would be drawn in BT.601 on this ffmpeg. Tagging it BT.709 before the burn-in "
                "(correct only if the master really is BT.709, which the harness master always is)." % v.get("color_space", "unset"))

        # --- 3. the plan
        vf_parts = []
        if not tagged:
            vf_parts.append("setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv")
        if cues:
            vf_parts.append("ass=caps.ass:fontsdir=fonts")
        vf_parts.append(chain["vf"])
        vf = ",".join(vf_parts)
        step("Plan")
        say("      video filter: %s" % vf)
        say("      video args: %s" % " ".join(str(x) for x in chain["video_args"]))
        say("      audio: two-pass loudnorm to %g LUFS / %g dBTP, then %s" % (prof["encode"]["loudness"]["integrated_lufs"], prof["encode"]["loudness"]["true_peak_dbtp"], " ".join(str(x) for x in chain["audio_args"])))
        if a.dry_run:
            say("DRY RUN: nothing was run and nothing was written.")
            return 0

        # --- 4. work folder
        step("Making the work folder (relative names only inside the filter)")
        work = tempfile.mkdtemp(prefix="ljphone_", dir=a.work) if a.work else tempfile.mkdtemp(prefix="ljphone_")
        fams = {}
        if cues:
            scripts = set(script_of_text(l) for c in cues for l in c["lines"])
            fams = prepare_fonts(work, scripts, a.fontsdir, fam_over)
            with open(os.path.join(work, "caps.srt"), "w", encoding="utf-8", newline="\n") as f:
                f.write(srt_text)
            ass_text = build_ass(cues, style, fams, play=(cap["ass"]["play_res_x"], cap["ass"]["play_res_y"]), ycbcr=cap["ass"]["ycbcr_matrix"],
                                 wrap_style=cap["ass"]["wrap_style"], scaled=cap["ass"]["scaled_border_and_shadow"])
            with open(os.path.join(work, "caps.ass"), "w", encoding="utf-8", newline="\n") as f:
                f.write(ass_text)
            say("      wrote caps.srt, caps.ass (styles per script: %s) and fonts/ (%s)" % (", ".join(sorted(fams)), ", ".join(sorted(os.listdir(os.path.join(work, "fonts"))))))

        # --- 5. video
        step("Encoding the video (captions burned on the 1080 frame, then the chain)")
        cmd = [ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", master, "-map", "0:v:0", "-an", "-vf", vf] + [str(x) for x in chain["video_args"]] + ["video.mp4"]
        rc, so, se = run(cmd, cwd=work)
        if rc != 0 or not os.path.isfile(os.path.join(work, "video.mp4")):
            raise Env("video encode failed: %s" % tail(se, 4))
        say("      video.mp4 %d bytes" % os.path.getsize(os.path.join(work, "video.mp4")))
        if cues:
            log = se.decode("utf-8", "replace")
            for line in log.splitlines():
                if "fontselect" in line or "Glyph" in line and "not found" in line:
                    say("      libass: " + re.sub(r"\[[^\]]*\]\s*", "", line.strip())[:160])

        # --- 6. audio
        step("Encoding the sound")
        aud = encode_audio(ffmpeg, master, work, chain, prof["encode"], lambda m: say(m))

        # --- 7. mux
        step("Muxing with faststart and no metadata")
        rc, so, se = run([ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", "video.mp4", "-i", "audio.m4a", "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
                          "-movflags", "+faststart", "-map_metadata", "-1", "-fflags", "+bitexact", "final.mp4"], cwd=work)
        if rc != 0:
            raise Env("mux failed: %s" % tail(se, 3))
        partial = out_abs + ".partial"
        shutil.copyfile(os.path.join(work, "final.mp4"), partial)
        os.replace(partial, out_abs)

        # --- 8. checks
        step("Checking the result")
        checks = []

        def chk(cid, ok, detail):
            checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})
            say("      %s  %s  %s" % ("PASS" if ok else "FAIL", cid, detail))

        po = probe(ffprobe, out_abs)
        ov, oa = po["video"], po["audio"]
        ow, oh = int(ov["width"]), int(ov["height"])
        want_w, want_h = pspec["video"]["width"], pspec["video"]["height"]
        chk("size", (ow, oh) == (want_w, want_h), "%dx%d (profile %dx%d)" % (ow, oh, want_w, want_h))
        chk("fps", fps_of(ov) == (24, 1), "%d/%d" % fps_of(ov))
        onb = int(ov.get("nb_frames") or 0)
        chk("frame_count", (nb == 0) or (onb == nb), "%d frames (master %d)" % (onb, nb))
        want = {"pix_fmt": pspec["video"]["pix_fmt"], "color_range": pspec["video"]["color_range"], "color_space": pspec["video"]["color_space"],
                "color_primaries": pspec["video"]["color_primaries"], "color_transfer": pspec["video"]["color_transfer"]}
        bad = [k for k, vv in want.items() if str(ov.get(k)) not in vv]
        chk("tags", not bad, "pix_fmt %s, range %s, matrix %s, primaries %s, transfer %s" % (ov.get("pix_fmt"), ov.get("color_range"), ov.get("color_space"), ov.get("color_primaries"), ov.get("color_transfer")) + ("; wrong: " + ",".join(bad) if bad else ""))
        chk("codec", ov.get("codec_name") == "h264" and ov.get("profile") in pspec["video"]["profile"] and int(ov.get("level", 0)) in pspec["video"]["level"],
            "%s %s level %s" % (ov.get("codec_name"), ov.get("profile"), ov.get("level")))
        size_b = os.path.getsize(out_abs)
        odur = float(po["format"].get("duration") or 0)
        mbps = (size_b * 8.0 / odur / 1e6) if odur > 0 else 0.0
        capm = float(chain.get("bitrate_cap_mbps") or 0)
        lim = capm * (1 + prof["encode"]["bitrate_tolerance_pct"] / 100.0)
        chk("bitrate", capm > 0 and mbps <= lim, "%.2f Mbps average over the file (cap %.2f Mbps + %d%% = %.2f)" % (mbps, capm, prof["encode"]["bitrate_tolerance_pct"], lim))
        at = mp4_atoms(out_abs)
        names = [t for t, _o in at]
        ok_order = "moov" in names and "mdat" in names and names.index("moov") < names.index("mdat")
        chk("faststart", ok_order, "atoms: %s" % ", ".join(names))
        fl, fp = measure_ebur128(ffmpeg, out_abs)
        chk("loudness", abs(fl - prof["encode"]["loudness"]["integrated_lufs"]) <= pspec["loudness"]["tolerance_lu"], "%.1f LUFS integrated on the final file (target %g +- %g)" % (fl, prof["encode"]["loudness"]["integrated_lufs"], pspec["loudness"]["tolerance_lu"]))
        chk("true_peak", fp <= pspec["loudness"]["true_peak_max_dbtp"] + 1e-9, "%.1f dBTP on the final file (limit %g)" % (fp, pspec["loudness"]["true_peak_max_dbtp"]))
        chk("audio", oa is not None and oa.get("codec_name") == "aac" and str(oa.get("sample_rate")) == "48000" and int(oa.get("channels", 0)) == 2,
            "%s %s Hz %s ch" % (oa.get("codec_name") if oa else None, oa.get("sample_rate") if oa else None, oa.get("channels") if oa else None))
        tags = (po["format"].get("tags") or {})
        extra = sorted(k for k in tags if k.lower() not in ("encoder", "major_brand", "minor_version", "compatible_brands"))
        chk("metadata", not extra, "format tags other than the structural ones: %s" % (", ".join(extra) or "none"))

        # --- 9. sidecar and caption file
        step("Writing the sidecar and the caption file next to the output")
        written = [os.path.basename(out_abs)]
        if cues:
            with open(out_abs + ".ass", "w", encoding="utf-8", newline="\n") as f:
                f.write(ass_text)
            written.append(os.path.basename(out_abs) + ".ass")
        if not a.no_sidecar:
            side = {"schema": "lj-phone-sidecar/1", "tool": "encode_phone.py", "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
                    "profile": a.profile, "style": style_key, "style_params": {k: style.get(k) for k in ("font_size", "font_size_by_script", "margin_v", "outline", "max_chars_per_line", "max_lines")},
                    "captions": ({"cues": len(cues), "ass_file": os.path.basename(out_abs) + ".ass", "filter": "ass", "families": fams,
                                  "max_line_chars": max(count_chars(plain_line(l)) for c in cues for l in c["lines"]),
                                  "max_lines": max(len(c["lines"]) for c in cues)} if cues else None),
                    "input": {"name": os.path.basename(master), "width": w, "height": h, "frames": nb, "duration_s": round(dur, 3), "color_space_tag": v.get("color_space")},
                    "output": {"name": os.path.basename(out_abs), "width": ow, "height": oh, "bytes": size_b, "average_mbps": round(mbps, 3), "sha256": sha256_file(out_abs)},
                    "audio": aud, "layout": (layout_of(layout) if isinstance(layout, dict) else None),
                    "checks": checks, "ffmpeg": ffmpeg_version(ffmpeg),
                    "unverified": ["everything on Windows (never run there)", "the colour of the burned captions on ffmpeg 9.0.2 (the PC build): the master is tagged BT.709 and the caption is white with a black outline, which no matrix changes, but a tinted caption needs the twelve-patch test first (W-16)"]}
            write_json(out_abs + ".phone.json", side)
            written.append(os.path.basename(out_abs) + ".phone.json")
        say("files written: %s" % ", ".join(written))
        failed = [c["id"] for c in checks if c["status"] != "PASS"]
        if failed:
            say("RESULT: the file was made but these checks failed: %s" % ", ".join(failed))
            return 1
        say("RESULT: done, every check passed (%.2f Mbps, %.1f LUFS, %.1f dBTP)" % (mbps, fl, fp))
        return 0
    except Usage as e:
        say("USAGE/INPUT PROBLEM: %s" % e)
        return 2
    except Env as e:
        say("ENVIRONMENT PROBLEM: %s" % e)
        return 3
    finally:
        if work and not a.keep_work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
