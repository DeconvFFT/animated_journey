#!/usr/bin/env python3
"""phone_check.py: does the text on a phone-size screen still read? Legibility, shaping and fill-crop checks for the phone file. WP-08, decision D-27.

  python3 -I pipeline/phone/phone_check.py FILE.mp4 [--scenario NAME ...] [--aspect 19.5:9] [--json OUT.json]    check a phone file made by encode_phone.py (its OUTPUT.ass and
                                                                                                                  OUTPUT.phone.json must be beside it; sim_share.sh copies them)
  python3 -I pipeline/phone/phone_check.py --style phone [--scenario NAME ...] [--json OUT] [--scripts-json OUT]    check a caption STYLE of profile.json for every script in test_strings.json
  python3 -I pipeline/phone/phone_check.py --selftest                                                               mechanisms only: a tiny caption fails, a large one passes, ...
  python3 -I pipeline/phone/phone_check.py --finding-fs23 --out build/evidence/wp08/finding_fontsize23.json        write the FontSize=23 verdict per scenario as a FINDING (exit 0 either way)
  python3 -I pipeline/phone/phone_check.py --candidates [--out FILE]                                                measure the candidate FontSizes and say which one the rule picks
  python3 -I pipeline/phone/phone_check.py --shaping-paths [--out FILE]                                             the `ass` filter against the `subtitles` filter, per script (IoU against Pillow-raqm)
  python3 -I pipeline/phone/phone_check.py --write-row PHONE-ROW.md [--evidence build/evidence/wp08]               write PHONE-ROW.md from the evidence files
  Options: --ass FILE --sidecar FILE (a file's caption file and sidecar)  --max-cues N  --no-diff  --ffmpeg PATH  --thresholds FILE  --strings FILE  --profile FILE  --keep  --quiet

SCENARIOS (pipeline/phone/thresholds.json viewports; every figure is an assumption about typical phones and is UNVERIFIED)
  portrait        held upright, 390 CSS px wide, device pixel ratio 3, the 16:9 picture full width (advisory: upright is degraded by design, the hand-over says 'turn it sideways')
  landscape       the same phone sideways, 844 CSS px wide, picture fitted to the height (the intended view)
  small_portrait  360 CSS px wide at ratio 2 (a 720p-class phone) upright (advisory)
  shared          the file re-encoded to 480p at about 1 Mbps with x264 veryfast (a messenger), viewed sideways; a file that is already 480p or smaller is used as it is
  fill_20x9       16:9 filled to a 20:9 screen: scaled to the screen width, so about 10% of the picture height is cropped at the top and again at the bottom (--aspect 19.5:9: about 9%)

WHAT IS MEASURED, per scenario and per script (a metric names its threshold in thresholds.json, with its source and (J) where it is a proposal)
  x-height (Latin) or base-letter band (other scripts) and cap height, in pixels, millimetres and arcminutes at the 35 cm design distance (and at 40 cm), and as a percentage of
  picture height; the 10th-percentile stroke width of the caption letters on the scenario's smallest grid; WCAG contrast of the fill against the outline; the caption box inside
  the 90% box; the caption POSITION (bottom and top of the box as a percentage of picture height against the scenario's crop line; fill_20x9: bottom at or above 88%, and the share of
  the caption ink that stays on the screen); in a file, the thin lines of the scene layout (width on the grid and contrast kept) and the title height (at least 5% of picture height).
  Per script that has strings in test_strings.json (a script without strings is reported NOT TESTED, never PASS): the burned line is drawn by libass (the burn-in path); the
  SHAPING check registers it on a Pillow-raqm drawing of the same text (translation and a small uniform scale) and needs an ink IoU of at least 0.9, else it is a shaping finding;
  the MARK-SURVIVAL check reads that script's marks[] (codepoints and kind) from the same file, finds each mark's zone by differential rendering at 8x with Pillow-raqm (the text with
  and without the mark's codepoints; no coordinate is stored or assumed) and requires, after the downscale to the scenario's grid, at least 2 px of ink in the zone and the burned ink
  in the mark's window to be closer to the reference with the mark than to the reference without it.

WHAT IT NEVER DOES. It never edits the file it checks (the SHA-256 is compared before and after), never uploads anything, uses no network, prints base file names only (no folder, user or
host names), writes only what --json / --out / --scripts-json / --write-row name, and keeps its scratch in a temporary folder that it removes. numpy, Pillow (with raqm) and ffmpeg are required.
EXIT  0 no blocking check failed (an advisory scenario may still FAIL: it is listed); 1 a blocking check, a shaping check or the burn match failed; 2 bad usage or invalid input; 3 environment
      problem. --finding-fs23, --candidates and --shaping-paths exit 0 however the numbers come out (they write findings); --selftest exits 1 if a mechanism does not work.
"""
import argparse
import datetime
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
THRESHOLDS = os.path.join(HERE, "thresholds.json")
PROFILE = os.path.join(HERE, "profile.json")
STRINGS = os.path.join(HERE, "test_strings.json")
SETTINGS = os.path.join(ROOT, "pipeline", "settings.json")

PASS, FAIL, INFO, NM, NT = "PASS", "FAIL", "INFO", "NOT MEASURED", "NOT TESTED"
W0, H0 = 1920, 1080


class Usage(Exception):
    pass


class Env(Exception):
    pass


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


try:
    import numpy as np
    import PIL
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, features as pil_features
except ImportError as _e:  # pragma: no cover
    sys.stdout.write("ENVIRONMENT PROBLEM: numpy and Pillow are required (%s)\n" % _e)
    sys.exit(3)


# ====================================================================================================== loading
def load_ep():
    """encode_phone.py, loaded by path (python -I does not put this folder on sys.path)."""
    spec = importlib.util.spec_from_file_location("lj_encode_phone", os.path.join(HERE, "encode_phone.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


EP = load_ep()


def read_json(path):
    return EP.read_json(path)


def load_thresholds(path=None):
    t = read_json(path or THRESHOLDS)
    for k in ("distance_cm", "x_height", "contrast", "stroke", "box90", "position", "title", "marks", "iou", "viewports", "degrade_shared"):
        if k not in t:
            raise Usage("thresholds file has no '%s'" % k)
    return t


def scripts_with_strings(strings):
    out = {}
    for name, blk in strings["scripts"].items():
        out[name] = [s for s in (blk.get("strings") or [])]
    return out


def cp_to_char(cp):
    m = re.fullmatch(r"U\+([0-9A-Fa-f]{4,6})", cp.strip())
    if not m:
        raise Usage("marks[] codepoint '%s' is not of the form U+XXXX" % cp)
    return chr(int(m.group(1), 16))


def strip_marks(text, mark):
    drop = set(cp_to_char(c) for c in mark["codepoints"])
    return "".join(ch for ch in text if ch not in drop)


# ====================================================================================================== geometry and units
def parse_aspect(txt):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*", txt or "")
    if not m or float(m.group(2)) <= 0:
        raise Usage("--aspect wants W:H, for example 20:9 or 19.5:9")
    return float(m.group(1)), float(m.group(2))


def fill_crop_pct(aspect_w, aspect_h):
    """Percent of the picture height cropped at the top, and again at the bottom, when a 16:9 picture is scaled to the width of an aspect_w:aspect_h screen."""
    visible = (16.0 / 9.0) / (aspect_w / aspect_h)
    return max(0.0, (1.0 - visible) / 2.0 * 100.0)


def arcmin(h_mm, dist_cm):
    return math.degrees(2.0 * math.atan((h_mm / 10.0) / (2.0 * dist_cm))) * 60.0


def geometry(name, thr, aspect=None):
    """Everything a scenario needs: device pixels per source pixel, picture size in mm, the crop, the smallest grid."""
    vp = thr["viewports"][name]
    css_w, css_h, dpr = float(vp["css_w"]), float(vp["css_h"]), float(vp["dpr"])
    asp = None
    if name == "fill_20x9":
        asp = aspect or parse_aspect(vp.get("aspect", "20:9"))
        css_h = css_w * asp[1] / asp[0]
    k = min(css_w / 16.0, css_h / 9.0) if vp["mode"] == "fit" else max(css_w / 16.0, css_h / 9.0)
    pic_css_w, pic_css_h = 16.0 * k, 9.0 * k
    mm_per_css = float(vp["screen_w_mm"]) / css_w
    s_dev = pic_css_w * dpr / float(W0)
    visible = min(1.0, css_h / pic_css_h)
    crop = (1.0 - visible) / 2.0 * 100.0
    deg = thr.get(vp["degrade"]) if vp.get("degrade") else None
    s_share = (float(deg["height"]) / float(H0)) if deg else None
    return {"scenario": name, "gate": vp["gate"], "description": vp["description"], "css_w": css_w, "css_h": css_h, "dpr": dpr, "mode": vp["mode"],
            "aspect": ("%g:%g" % asp) if asp else None, "device_px_per_source_px": s_dev, "picture_w_mm": pic_css_w * mm_per_css, "picture_h_mm": pic_css_h * mm_per_css,
            "crop_each_pct": crop, "visible_rows_pct": [crop, 100.0 - crop], "degrade": deg, "share_px_per_source_px": s_share,
            "smallest_grid_px_per_source_px": min(s_dev, s_share) if s_share else s_dev}


# ====================================================================================================== pixel primitives
def srgb_to_linear(c):
    c = np.asarray(c, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rel_luminance(rgb):
    """WCAG 2.1 relative luminance of an (H, W, 3) uint8 image."""
    lin = srgb_to_linear(rgb)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def wcag_ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def ink_bbox(cov, thr=0.5):
    """(x0, y0, x1, y1) with x1, y1 exclusive, of pixels above thr; None if empty."""
    m = cov > thr
    if not m.any():
        return None
    ys = np.where(m.any(axis=1))[0]
    xs = np.where(m.any(axis=0))[0]
    return int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1


def vextent(cov):
    """Sub-pixel vertical extent of flat-topped, flat-bottomed ink: the sum over rows of the row's maximum coverage (an edge row covered 0.3 counts 0.3)."""
    return float(np.clip(cov, 0, 1).max(axis=1).sum())


def _run_sums(a, tiny=0.08):
    """Per pixel: the sum of coverage along the horizontal run (pixels above tiny) that contains it; 0 elsewhere."""
    m = a > tiny
    h, w = a.shape
    pad = np.zeros((h, 1), dtype=bool)
    mp = np.concatenate([pad, m, pad], axis=1)
    starts = mp[:, 1:-1] & ~mp[:, :-2]
    run_id = np.cumsum(starts.ravel()).reshape(h, w)
    ids = run_id[m]
    sums = np.bincount(ids, weights=a[m].astype(np.float64))
    out = np.zeros((h, w), dtype=np.float64)
    out[m] = sums[ids]
    return out


def stroke_widths(cov):
    """Local stroke width at every core ink pixel (coverage >= 0.5): the smaller of the horizontal and the vertical run, in pixels with sub-pixel coverage."""
    cov = np.clip(cov.astype(np.float64), 0, 1)
    hr = _run_sums(cov)
    vr = _run_sums(cov.T).T
    core = cov >= 0.5
    sw = np.minimum(hr, vr)
    return sw[core]


def stroke_stat(cov, pct=10):
    v = stroke_widths(cov)
    if v.size == 0:
        return None
    return {"p": float(np.percentile(v, pct)), "median": float(np.median(v)), "pct": pct, "n": int(v.size)}


def scale_cov(arr, s, shift=0):
    """Resample a float coverage image by s with the assumed device scaler (Pillow BICUBIC, which is Catmull-Rom and filters when it shrinks). shift pads the
    top and left by that many source pixels first, which moves the sampling phase."""
    a = np.asarray(arr, dtype=np.float32)
    if shift:
        a = np.pad(a, ((shift, 0), (shift, 0)))
    nw, nh = max(1, int(round(a.shape[1] * s))), max(1, int(round(a.shape[0] * s)))
    im = Image.fromarray(a, mode="F").resize((nw, nh), Image.BICUBIC)
    return np.clip(np.asarray(im, dtype=np.float32), 0.0, 1.0)


def scale_rgb(img, s):
    h, w = img.shape[:2]
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    return np.asarray(Image.fromarray(img).resize((nw, nh), Image.BICUBIC))


def iou_binary(a, b):
    a, b = a.astype(bool), b.astype(bool)
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 1.0


def iou_soft(a, b):
    a, b = np.clip(a, 0, 1), np.clip(b, 0, 1)
    u = np.maximum(a, b).sum()
    return float(np.minimum(a, b).sum() / u) if u else 1.0


# ====================================================================================================== libass rendering (the burn-in path)
FILTER_TAGS = "format=yuv444p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
FILTER_RGB = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"


class Work:
    """A temporary folder that is removed on exit."""

    def __init__(self, keep=False):
        self.keep = keep
        self.path = tempfile.mkdtemp(prefix="ljphonechk_")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        if not self.keep:
            shutil.rmtree(self.path, ignore_errors=True)


class Tools:
    def __init__(self, ffmpeg=None, keep=False):
        self.ffmpeg = EP.resolve_tool(ffmpeg, "FFMPEG", "ffmpeg")
        self.ffprobe = EP.ffprobe_for(self.ffmpeg, None)
        self.version = EP.ffmpeg_version(self.ffmpeg)
        self.work = Work(keep)
        self.lock = EP.read_json(EP.LOCK_PATH)
        self.log_lines = []

    def run(self, cmd, cwd=None, timeout=600):
        return EP.run(cmd, cwd=cwd, timeout=timeout)

    def sub(self, name):
        p = os.path.join(self.work.path, name)
        os.makedirs(p, exist_ok=True)
        return p

    def close(self):
        self.work.__exit__()


def load_png_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"))


def libass_batch(tools, ass_text, n, bg="000000", size=(W0, H0), scripts=("latin",), vf_filter="ass", shaping=None, tag="b", srt_text=None, srt_style=None):
    """Render frames 0..n-1 of a 1 fps clip: frame k shows what ASS cue k (or SRT cue k) shows. Returns (list of (H, W, 3) uint8, libass log lines).
    vf_filter 'ass' draws the ASS text; 'subtitles' draws the SRT text (the path of the settings card, FontSize through force_style)."""
    d = tools.sub("lb_" + tag + "_%d" % len(os.listdir(tools.work.path)))
    fdir = os.path.join(d, "fonts")
    os.makedirs(fdir, exist_ok=True)
    for sc in sorted(set(scripts) | {"latin"}):
        fam, path = EP.font_for_script(sc, tools.lock)
        shutil.copyfile(path, os.path.join(fdir, os.path.basename(path)))
    if vf_filter == "ass":
        with open(os.path.join(d, "c.ass"), "w", encoding="utf-8", newline="\n") as f:
            f.write(ass_text)
        filt = "ass=c.ass:fontsdir=fonts" + (":shaping=%s" % shaping if shaping else "")
    else:
        with open(os.path.join(d, "c.srt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(srt_text)
        filt = "subtitles=c.srt:fontsdir=fonts:force_style='%s'" % srt_style
    vf = FILTER_TAGS + "," + filt + "," + FILTER_RGB
    cmd = [tools.ffmpeg, "-hide_banner", "-nostdin", "-v", "verbose", "-y", "-f", "lavfi", "-i", "color=c=0x%s:s=%dx%d:r=1:d=%d" % (bg, size[0], size[1], n), "-vf", vf,
           "-frames:v", str(n), "-start_number", "0", "o_%03d.png"]
    rc, so, se = tools.run(cmd, cwd=d)
    if rc != 0:
        raise Env("libass render failed: %s" % EP.tail(se, 3))
    log = [re.sub(r"^\[[^\]]*\]\s*", "", l.strip()) for l in se.decode("utf-8", "replace").splitlines() if "fontselect:" in l or "Shaper:" in l or ("Glyph" in l and "not found" in l)]
    imgs = [load_png_rgb(os.path.join(d, "o_%03d.png" % k)) for k in range(n)]
    tools.log_lines.extend(log)
    shutil.rmtree(d, ignore_errors=True)
    return imgs, log


def cues_for(lines_list, per=1000):
    return [{"start_ms": k * per, "end_ms": k * per + 900, "lines": list(lines)} for k, lines in enumerate(lines_list)]


def families_for(tools, scripts):
    return {sc: EP.font_for_script(sc, tools.lock)[0] for sc in set(scripts) | {"latin"}}


def render_cues(tools, lines_list, style, fill_only=True, size=(W0, H0), shaping=None, outline_override=None):
    """Render each entry of lines_list (a list of caption lines) as its own cue with the style. fill_only: white on black with no outline, so the green channel is the
    coverage of the glyphs. Otherwise: the full style on mid grey. Returns a list of float32 coverage arrays (fill_only) or (H, W, 3) uint8 images."""
    scripts = set(EP.script_of_text(l) for lines in lines_list for l in lines)
    fams = families_for(tools, scripts)
    cues = cues_for(lines_list)
    st = dict(style)
    ass = EP.build_ass(cues, st, fams, outline_override=(0 if fill_only else outline_override))
    imgs, _log = libass_batch(tools, ass, len(cues), bg=("000000" if fill_only else "808080"), size=size, scripts=scripts, shaping=shaping, tag="c")
    if fill_only:
        return [im[..., 1].astype(np.float32) / 255.0 for im in imgs]
    return imgs


# ====================================================================================================== font metrics (stdlib parse of OS/2 and head; WOFF, TTF, OTF)
def font_metrics(path):
    """unitsPerEm, sxHeight, sCapHeight, winAscent, winDescent of a font file, read from its OS/2 and head tables (WOFF 1.0, TrueType or OpenType)."""
    import struct
    import zlib
    with open(path, "rb") as f:
        d = f.read()
    tabs = {}
    if d[:4] == b"wOFF":
        num = struct.unpack(">H", d[12:14])[0]
        for i in range(num):
            tag, off, cl, ol, _cs = struct.unpack(">4sIIII", d[44 + 20 * i:64 + 20 * i])
            raw = d[off:off + cl]
            tabs[tag.decode("latin-1")] = zlib.decompress(raw) if cl < ol else raw
    else:
        num = struct.unpack(">H", d[4:6])[0]
        for i in range(num):
            tag, _cs, off, ln = struct.unpack(">4sIII", d[12 + 16 * i:28 + 16 * i])
            tabs[tag.decode("latin-1")] = d[off:off + ln]
    if "head" not in tabs or "OS/2" not in tabs:
        raise Env("%s has no head or OS/2 table" % os.path.basename(path))
    upem = struct.unpack(">H", tabs["head"][18:20])[0]
    os2 = tabs["OS/2"]
    ver = struct.unpack(">H", os2[0:2])[0]
    win_a, win_d = struct.unpack(">HH", os2[74:78])
    xh = ch = None
    if ver >= 2 and len(os2) >= 90:
        xh, ch = struct.unpack(">hh", os2[86:90])
    return {"units_per_em": upem, "x_height": xh or None, "cap_height": ch or None, "win_ascent": win_a, "win_descent": win_d, "os2_version": ver}


# ====================================================================================================== Pillow-raqm reference, registration, IoU
def raqm_font(path, size):
    if not pil_features.check("raqm"):
        raise Env("Pillow was built without raqm; the IoU reference needs it")
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


LANG = {"latin": "en", "devanagari": "hi", "bengali": "bn", "gujarati": "gu", "tamil": "ta", "telugu": "te", "kannada": "kn", "malayalam": "ml"}


def raqm_canvas(texts, font_path, px, script, pad=24):
    font = raqm_font(font_path, px)
    asc, desc = font.getmetrics()
    lang = LANG.get(script, "en")
    length = max(font.getlength(t, language=lang) for t in texts)
    return (int(asc + desc + 2 * pad), int(length + 2 * pad + px))


def raqm_render(text, font_path, px, script, canvas=None, pad=24):
    """Coverage (float32, 0..1) of the text drawn with Pillow-raqm at px pixels (an em size). The baseline sits at a fixed row and the pen starts at a fixed column,
    so renderings of related strings line up when they share a canvas."""
    font = raqm_font(font_path, px)
    asc, desc = font.getmetrics()
    lang = LANG.get(script, "en")
    if canvas is None:
        canvas = raqm_canvas([text], font_path, px, script, pad)
    im = Image.new("L", (canvas[1], canvas[0]), 0)
    ImageDraw.Draw(im).text((pad, pad + asc), text, font=font, fill=255, anchor="ls", language=lang)
    return np.asarray(im, dtype=np.float32) / 255.0


def reduce8(a, k=8):
    h, w = a.shape
    return a[:(h // k) * k, :(w // k) * k].reshape(h // k, k, w // k, k).mean(axis=(1, 3))


def shift2(a, dx, dy):
    """Shift an array by integer (dx, dy) with zero fill."""
    out = np.zeros_like(a)
    h, w = a.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    if xs1 > xs0 and ys1 > ys0:
        out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = a[ys0:ys1, xs0:xs1]
    return out


def window(a, y0, x0, h, w):
    """a[y0:y0+h, x0:x0+w] with zero fill outside a."""
    out = np.zeros((h, w), dtype=a.dtype)
    sy0, sx0 = max(0, y0), max(0, x0)
    sy1, sx1 = min(a.shape[0], y0 + h), min(a.shape[1], x0 + w)
    if sy1 > sy0 and sx1 > sx0:
        out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = a[sy0:sy1, sx0:sx1]
    return out


class Registration:
    """A libass fill-coverage image of one line and the Pillow-raqm reference of the same text, registered by a translation (in 1/8 pixel steps) and a small uniform
    scale. The scale is a nuisance parameter: libass maps FontSize to an em size by its own rule and quantises glyph advances, so the same text comes out up to a few percent
    wider or narrower than the reference at the same nominal size; the reference's em is therefore fitted to the libass ink (width and height) before the IoU is taken.
    fill: the libass coverage cropped to the line's ink box plus a margin (1x). ok False when the line has no ink.
    After construction: em_px (the fitted em), ref1 (the reference at 1x on the crop grid), iou_b and iou_s (binary and soft IoU), full8 and the 8x renderings of the variants
    (the same text with marks removed) on one canvas; to_grid(a8) puts any 8x canvas image on the crop grid."""

    def __init__(self, fill_full, text, font_path, script, variants=(), margin=6, k=8):
        self.k, self.margin, self.text, self.font_path, self.script = k, margin, text, font_path, script
        self.variants_text = list(variants)
        bb = ink_bbox(fill_full, 0.5)
        self.ok = bb is not None
        self.iou_b = self.iou_s = None
        if not self.ok:
            return
        x0, y0, x1, y1 = bb
        self.bbox = bb
        self.fx0, self.fy0 = max(0, x0 - margin), max(0, y0 - margin)
        self.fx1, self.fy1 = min(fill_full.shape[1], x1 + margin), min(fill_full.shape[0], y1 + margin)
        self.fill = fill_full[self.fy0:self.fy1, self.fx0:self.fx1]
        self.libass_ink = (x1 - x0, y1 - y0)
        r100 = raqm_render(text, font_path, 100, script)
        b100 = ink_bbox(r100, 0.5)
        if b100 is None:
            self.ok = False
            return
        em_h = 100.0 * (y1 - y0) / float(b100[3] - b100[1])
        em_w = 100.0 * (x1 - x0) / float(b100[2] - b100[0])
        cands = sorted(set(round(em_w * (1 + d), 2) for d in (-0.012, -0.006, 0.0, 0.006, 0.012)) | {round(em_h, 2)})
        best = None
        for em in cands:                                              # coarse: reference at 2x, shifts in half pixels
            sc, dx2, dy2 = self._fit_at(em, 2, (0, 0), (4, 2, 1))
            if best is None or sc > best[0]:
                best = (sc, em, dx2, dy2)
        self.em_px = best[1]
        sc, dx8, dy8 = self._fit_at(self.em_px, self.k, (best[2] * (self.k // 2), best[3] * (self.k // 2)), (4, 2, 1))     # fine: 8x around the coarse optimum
        self.dx8, self.dy8 = dx8, dy8
        self._build(self.em_px)
        self.ref1 = self.ref_at(self.dx8, self.dy8)
        self.iou_b = iou_binary(self.fill > 0.5, self.ref1 > 0.5)
        self.iou_s = iou_soft(self.fill, self.ref1)

    # --- one candidate em, at k times the resolution
    def _origin_k(self, full, k):
        b = ink_bbox(full, 0.5)
        x0, y0 = self.bbox[0], self.bbox[1]
        return b, b[0] - (x0 - self.fx0) * k, b[1] - (y0 - self.fy0) * k

    def _origin(self, full8):
        return self._origin_k(full8, self.k)

    def _fit_at(self, em, k, start, steps):
        full = raqm_render(self.text, self.font_path, round(em * k, 2), self.script)
        b, ox, oy = self._origin_k(full, k)
        h, w = self.fill.shape
        crop = window(full, oy, ox, h * k, w * k)
        fb = self.fill > 0.5

        def score(dx, dy):
            return iou_binary(fb, reduce8(shift2(crop, dx, dy), k) > 0.5)
        dx, dy = start
        best = score(dx, dy)
        for step in steps:
            moved = True
            while moved:
                moved = False
                for ddx, ddy in ((step, 0), (-step, 0), (0, step), (0, -step)):
                    sc = score(dx + ddx, dy + ddy)
                    if sc > best + 1e-9:
                        best, dx, dy, moved = sc, dx + ddx, dy + ddy, True
        return best, dx, dy

    def _build(self, em):
        """Render the text and its variants on one canvas at the fitted em."""
        k = self.k
        px = round(em * k, 2)
        texts = [self.text] + self.variants_text
        canvas = raqm_canvas(texts, self.font_path, px, self.script)
        self.full8 = raqm_render(self.text, self.font_path, px, self.script, canvas=canvas)
        self.var8 = [raqm_render(t, self.font_path, px, self.script, canvas=canvas) if t else np.zeros(canvas, dtype=np.float32) for t in self.variants_text]
        b8, self.ox, self.oy = self._origin(self.full8)
        self.ref_ink = ((b8[2] - b8[0]) / float(k), (b8[3] - b8[1]) / float(k))
        h, w = self.fill.shape
        self.crop8 = window(self.full8, self.oy, self.ox, h * k, w * k)

    def ref_at(self, dx8, dy8):
        return reduce8(shift2(self.crop8, dx8, dy8), self.k)

    def to_grid(self, a8):
        """An image on the 8x canvas (a zone mask, a variant rendering) mapped to the 1x grid of the fill crop, with the fitted shift."""
        h, w = self.fill.shape
        return reduce8(shift2(window(a8, self.oy, self.ox, h * self.k, w * self.k), self.dx8, self.dy8), self.k)


# ---------------------------------------------------------------------------------------------------- mark zones (differential rendering)
def _max_filter(mask, size):
    """Dilation of a boolean mask by a square of the given odd size (separable shifts, no external library)."""
    r = size // 2
    m = np.asarray(mask, dtype=bool)
    h = m.copy()
    for d in range(1, r + 1):
        h[:, d:] |= m[:, :-d]
        h[:, :-d] |= m[:, d:]
    v = h.copy()
    for d in range(1, r + 1):
        v[d:, :] |= h[:-d, :]
        v[:-d, :] |= h[d:, :]
    return v


def _min_filter(mask, size):
    """Erosion by a square (the dual of the dilation)."""
    return ~_max_filter(~np.asarray(mask, dtype=bool), size)


def mark_regions(full8, strip8, kind, k=8):
    """The zone of one mark by differential rendering: the string drawn with and without the mark's codepoints, at 8x, on one canvas. Nothing is stored or assumed about
    where the mark sits. The two renderings agree before the mark (same pen start) and, after the mark, once the stripped one is moved by the difference of the right edges
    (a conjunct is narrower than its two plain consonants; a vowel sign is wider than none). The columns where they disagree under both alignments are the mark's
    WINDOW. The ZONE is the ink the mark ADDS inside that window (ink of the full rendering that the stripped one, in place or moved, does not explain). A mark that adds no
    ink of its own (a virama that only joins two consonants, kind 'conjunct') has the window's ink of the full rendering as its zone. Returns (zone, window, basis) as
    boolean arrays on the 8x canvas; basis 'added', 'window_ink' or 'none' (no difference at all)."""
    fm, sm = full8 >= 0.5, strip8 >= 0.5
    r = 3

    def cols_differ(a, b):
        da = a & ~_max_filter(b, 2 * r + 1)
        db = b & ~_max_filter(a, 2 * r + 1)
        return ((da | db).sum(axis=0) > 2)
    d0 = cols_differ(fm, sm)
    if not d0.any():
        return np.zeros_like(fm), np.zeros_like(fm), "none"
    xs = np.where(fm.any(axis=0))[0]
    ss = np.where(sm.any(axis=0))[0]
    dw = int(xs[-1] - ss[-1]) if xs.size and ss.size else 0
    sm_sh = shift2(sm.astype(np.uint8), dw, 0) > 0
    d1 = cols_differ(fm, sm_sh) if dw != 0 else d0
    x_left = int(np.where(d0)[0][0])
    x_right = int(max(np.where(d0)[0][-1] if dw == 0 else 0, np.where(d1)[0][-1] if d1.any() else x_left))
    x_right = max(x_right, x_left)
    pad = k
    x0, x1 = max(0, x_left - pad), min(fm.shape[1] - 1, x_right + pad)
    win = np.zeros_like(fm)
    win[:, x0:x1 + 1] = True
    explained = _max_filter(sm, 2 * r + 1) | (_max_filter(sm_sh, 2 * r + 1) if dw != 0 else False)
    added = fm & ~explained & win
    added = _max_filter(_min_filter(added, 3), 3) & added          # drop one-pixel fringes
    if kind != "conjunct" and int(added.sum()) >= 3 * k * k:
        return added, win, "added"
    return fm & win, win, "window_ink"


class MarkGeom:
    """One mark of one string, on the 1x crop grid of the line's Registration: zone, window, the reference with the mark (W) and without it (O), and the basis."""

    def __init__(self, reg, mark, idx):
        self.kind, self.codepoints = mark["kind"], list(mark["codepoints"])
        self.ok = False
        self.zone_px = 0
        full8, strip8 = reg.full8, reg.var8[idx]
        zone8, win8, self.basis = mark_regions(full8, strip8, self.kind, reg.k)
        if self.basis == "none":
            self.note = "the string drawn with and without this mark is identical (the face draws nothing for it)"
            return
        self.zone = reg.to_grid(zone8.astype(np.float32))
        self.win = reg.to_grid(win8.astype(np.float32))
        self.W = reg.ref1
        self.O = reg.to_grid(strip8)
        self.zone_px = int((self.zone > 0.5).sum())
        self.ok = self.zone_px > 0
        self.note = "" if self.ok else "the zone is empty at 1x"


def _transform(a, s, shift=0):
    """The scenario's device scaler applied to a coverage image."""
    return scale_cov(a, s, shift)


def mark_eval(geom, B, s, cfg, shifts=(0, 1, 2, 3), grid_already=False):
    """Does the mark survive the scenario? B is the burned line's coverage on the same 1x crop grid as geom (or, when grid_already, already on the scenario grid together with
    scaled geometry given by the caller). Rule (thresholds.json marks): at least min_ink_px pixels of burned ink in the zone after the scaling to the scenario's grid, AND the
    burned ink inside the mark's window is closer to the reference WITH the mark than to the reference WITHOUT it, AND its IoU with the reference with the mark is at least
    zone_iou_min. Worst case over the sampling phases. Returns a dict."""
    thr = cfg["coverage_threshold"]
    worst = None
    for sh in (shifts if s != 1.0 else (0,)):
        Bs = _transform(B, s, sh)
        Zs = _transform(geom.zone, s, sh) > 0.5
        Ws = _transform(geom.W, s, sh) > 0.5
        Os = _transform(geom.O, s, sh) > 0.5
        Cs = _transform(geom.win, s, sh) > 0.5
        Bb = Bs > thr
        ink = int((Bb & Zs).sum())
        bw, ww, ow = Bb & Cs, Ws & Cs, Os & Cs
        iw, io = iou_binary(bw, ww), iou_binary(bw, ow)
        res = {"ink_px": ink, "iou_with": iw, "iou_without": io, "zone_px_grid": int(Zs.sum())}
        score = (min(ink, 10 ** 6), iw - io)
        if worst is None or score < worst[0]:
            worst = (score, res)
    res = worst[1]
    res["closer_to_with"] = res["iou_with"] > res["iou_without"]
    res["survives"] = bool(res["ink_px"] >= cfg["min_ink_px"] and res["iou_with"] >= cfg["zone_iou_min"] and res["closer_to_with"])
    return res


# ====================================================================================================== frames: degrade (a messenger), decode
def write_png_seq(folder, frames, pattern="f_%03d.png"):
    for i, fr in enumerate(frames):
        Image.fromarray(fr).save(os.path.join(folder, pattern % i), compress_level=1)


def degrade_frames(tools, frames, deg, repeat=24):
    """Imitate a messenger: each frame is shown for `repeat` frames at 24 fps (so the encoder has a realistic bit budget per frame), the clip is re-encoded to
    deg['height'] p at about deg['video_bitrate'] with the given preset and profile, and the last repeated frame of each is decoded again (native size, RGB). Returns a list of
    (H', W', 3) uint8 arrays."""
    d = tools.sub("dg_%d" % len(os.listdir(tools.work.path)))
    write_png_seq(d, frames)
    tags = "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
    vf = "fps=24,scale=-2:%d:flags=bicubic:out_color_matrix=bt709:out_range=tv,format=yuv420p,%s" % (deg["height"], tags)
    cmd = [tools.ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-framerate", "1", "-i", "f_%03d.png", "-vf", vf, "-c:v", "libx264", "-preset", deg["preset"],
           "-profile:v", deg["profile"], "-b:v", deg["video_bitrate"], "-maxrate", deg["maxrate"], "-bufsize", deg["bufsize"], "-g", "48", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-an", "d.mp4"]
    rc, so, se = tools.run(cmd, cwd=d)
    if rc != 0:
        raise Env("degrade encode failed: %s" % EP.tail(se, 3))
    sel = "select=not(mod(n+1\\,%d))" % repeat
    cmd = [tools.ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", "d.mp4", "-vf", sel + "," + FILTER_RGB, "-fps_mode", "passthrough", "-start_number", "0", "o_%03d.png"]
    rc, so, se = tools.run(cmd, cwd=d)
    if rc != 0:
        raise Env("degrade decode failed: %s" % EP.tail(se, 3))
    out = [load_png_rgb(os.path.join(d, "o_%03d.png" % k)) for k in range(len(frames))]
    shutil.rmtree(d, ignore_errors=True)
    return out


def decode_indices(tools, path, indices, extra_vf=None):
    """Decode the frames of a file at the given frame numbers to (1080-grid, native-size) RGB arrays, in the order of `indices`."""
    d = tools.sub("dc_%d" % len(os.listdir(tools.work.path)))
    order = sorted(set(indices))
    sel = "select=" + "+".join("eq(n\\,%d)" % i for i in order)
    vf = sel + "," + (extra_vf + "," if extra_vf else "") + FILTER_RGB
    cmd = [tools.ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", path, "-vf", vf, "-fps_mode", "passthrough", "-start_number", "0", "o_%03d.png"]
    rc, so, se = tools.run(cmd, cwd=d)
    if rc != 0:
        raise Env("could not decode frames: %s" % EP.tail(se, 3))
    got = {}
    for k, idx in enumerate(order):
        p = os.path.join(d, "o_%03d.png" % k)
        if not os.path.isfile(p):
            raise Env("frame %d is past the end of the file" % idx)
        got[idx] = load_png_rgb(p)
    shutil.rmtree(d, ignore_errors=True)
    return [got[i] for i in indices]


def up_to_1080(img):
    """Native-size RGB to 1920x1080 (bicubic), for coordinates; the grid-limited information stays limited."""
    if img.shape[0] == H0 and img.shape[1] == W0:
        return img
    return np.asarray(Image.fromarray(img).resize((W0, H0), Image.BICUBIC))


# ====================================================================================================== test lines from test_strings.json
def line_chars(text):
    return EP.count_chars(text)


def compose_lines(words, max_chars, n_lines=2):
    """Caption lines of the fewest-fixed-length kind: words (allowlisted strings) cycled and joined with a space, each line filled up to max_chars characters. Every token is one of
    the allowlisted strings, so no new test text is ever written (4.10)."""
    lines, k = [], 0
    for _ in range(n_lines):
        cur = []
        while True:
            w = words[k % len(words)]
            cand = " ".join(cur + [w])
            if cur and line_chars(cand) > max_chars:
                break
            if not cur and line_chars(cand) > max_chars:
                cur.append(w)
                k += 1
                break
            cur.append(w)
            k += 1
            if len(cur) >= 12:
                break
        lines.append(" ".join(cur))
    return lines


def script_blocks(strings):
    """[(script, strings[])] in file order, with the strings list (maybe empty)."""
    return [(name, list(blk.get("strings") or [])) for name, blk in strings["scripts"].items()]


def lint_strings(strings):
    """Problems with the test strings file itself: a script with strings but no marks[] key on any string, or a string with no text. Returns a list of problem strings."""
    probs = []
    for name, blk in strings["scripts"].items():
        strs = blk.get("strings") or []
        if not strs or name == "latin":
            continue
        for s in strs:
            if "marks" not in s:
                probs.append("script '%s', string '%s': no marks[] key (a script with strings needs marks[] on every string, even an empty list)" % (name, s.get("id")))
            if not s.get("text"):
                probs.append("script '%s', string '%s': empty text" % (name, s.get("id")))
    return probs


# ====================================================================================================== metrics on rendered captions
def luma_of(img):
    return rel_luminance(img)


def diff_box(img, ref, thr=40):
    """Bounding box (x0, y0, x1, y1; x1 and y1 exclusive) of the pixels where img differs from ref by more than thr (0..255, any channel). None if nothing differs."""
    d = np.abs(img.astype(np.int16) - ref.astype(np.int16)).max(axis=2) > thr
    if not d.any():
        return None
    ys, xs = np.where(d.any(axis=1))[0], np.where(d.any(axis=0))[0]
    return int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1


def contrast_in_box(img, box):
    """WCAG contrast of the fill against the outline inside a caption box: the 98th and the 2nd percentile of relative luminance. Returns (ratio, l_hi, l_lo)."""
    x0, y0, x1, y1 = box
    lum = luma_of(img[y0:y1, x0:x1])
    hi, lo = float(np.percentile(lum, 98)), float(np.percentile(lum, 2))
    return wcag_ratio(hi, lo), hi, lo


def scale_box(box, s):
    x0, y0, x1, y1 = box
    return (int(math.floor(x0 * s)), int(math.floor(y0 * s)), int(math.ceil(x1 * s)), int(math.ceil(y1 * s)))


def check(cid, status, value=None, limit=None, detail=""):
    d = {"id": cid, "status": status}
    if value is not None:
        d["value"] = value
    if limit is not None:
        d["limit"] = limit
    if detail:
        d["detail"] = detail
    return d


def rnd(v, n=2):
    return None if v is None else round(float(v), n)


# ====================================================================================================== ASS text helpers (the file the burn-in used)
def ass_style_header(ass_text):
    """({style name: {field: value}}, [event rows as dicts]) from an ASS file made by encode_phone.py (or any ASS with Format lines)."""
    styles, events = {}, []
    sfmt = efmt = None
    sect = ""
    for raw in ass_text.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if line.startswith("["):
            sect = line.lower()
            continue
        if sect == "[v4+ styles]":
            if line.startswith("Format:"):
                sfmt = [c.strip() for c in line[7:].split(",")]
            elif line.startswith("Style:") and sfmt:
                vals = [c.strip() for c in line[6:].split(",")]
                styles[vals[0]] = dict(zip(sfmt, vals))
        elif sect == "[events]":
            if line.startswith("Format:"):
                efmt = [c.strip() for c in line[7:].split(",")]
            elif line.startswith("Dialogue:") and efmt:
                vals = line[9:].split(",", len(efmt) - 1)
                events.append(dict(zip(efmt, [v.strip() if k != "Text" else v for k, v in zip(efmt, vals)])))
    return styles, events


def _ass_ms(t):
    h, m, s = t.strip().split(":")
    sec, _, frac = s.partition(".")
    return ((int(h) * 60 + int(m)) * 60 + int(sec)) * 1000 + int((frac + "00")[:2]) * 10


def ass_cues(ass_text):
    """[{'start_ms','end_ms','style','lines':[plain text per line]}] of an ASS file (override tags removed; \\N splits lines)."""
    styles, events = ass_style_header(ass_text)
    out = []
    for e in events:
        txt = e["Text"].replace("\\n", "\\N")
        lines = [re.sub(r"\{[^}]*\}", "", p).strip() for p in txt.split("\\N")]
        out.append({"start_ms": _ass_ms(e["Start"]), "end_ms": _ass_ms(e["End"]), "style": e["Style"], "lines": [l for l in lines if l]})
    return out


def ass_for_render(ass_text, n_cues, fill_only=True, order=None):
    """The same ASS with every cue moved to k*1000 ms (k = its rank in `order`), and, when fill_only, white fill, no outline and no shadow (so the green channel on black is the
    glyph coverage). Used to draw exactly what the burn-in drew, without the picture behind it."""
    styles, events = ass_style_header(ass_text)
    out, sect, sfmt, efmt, k = [], "", None, None, 0
    idx = {j: r for r, j in enumerate(order)} if order is not None else None
    ev_i = 0
    for raw in ass_text.replace("\r\n", "\n").split("\n"):
        line = raw
        s = raw.strip()
        if s.startswith("["):
            sect = s.lower()
        elif sect == "[v4+ styles]" and s.startswith("Format:"):
            sfmt = [c.strip() for c in s[7:].split(",")]
        elif sect == "[v4+ styles]" and s.startswith("Style:") and sfmt and fill_only:
            vals = [c.strip() for c in s[6:].split(",")]
            d = dict(zip(sfmt, vals))
            d["PrimaryColour"], d["SecondaryColour"], d["Outline"], d["Shadow"], d["BorderStyle"] = "&H00FFFFFF", "&H00FFFFFF", "0", "0", "1"
            line = "Style: " + ",".join(d[c] for c in sfmt)
        elif sect == "[events]" and s.startswith("Format:"):
            efmt = [c.strip() for c in s[7:].split(",")]
        elif sect == "[events]" and s.startswith("Dialogue:") and efmt:
            if idx is not None and ev_i not in idx:
                ev_i += 1
                continue
            vals = s[9:].split(",", len(efmt) - 1)
            d = dict(zip(efmt, vals))
            kk = idx[ev_i] if idx is not None else ev_i
            d["Start"], d["End"] = _ass_time_ms(kk * 1000), _ass_time_ms(kk * 1000 + 900)
            line = "Dialogue: " + ",".join(d[c] for c in efmt)
            ev_i += 1
        out.append(line)
    return "\n".join(out) + "\n"


def _ass_time_ms(ms):
    cs = int(round(ms / 10.0))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return "%d:%02d:%02d.%02d" % (h, m, s, c)


def tile_line(text, allow):
    """Can the line be written as allowlisted strings joined by single spaces? Returns the list of allowlist entries (in order) or None. allow: [(text, entry)]."""
    text = text.strip()
    memo = {}

    def go(pos):
        if pos == len(text):
            return []
        if pos in memo:
            return memo[pos]
        res = None
        for t, ent in allow:
            if text.startswith(t, pos):
                end = pos + len(t)
                if end == len(text):
                    res = [ent]
                    break
                if text[end] == " ":
                    rest = go(end + 1)
                    if rest is not None:
                        res = [ent] + rest
                        break
        memo[pos] = res
        return res
    return go(0)


def row_bands(cov, thr=0.5, gap=6):
    """Runs of rows that hold ink, merged when separated by fewer than `gap` empty rows. [(r0, r1)] with r1 exclusive."""
    rows = np.where((cov > thr).any(axis=1))[0]
    if rows.size == 0:
        return []
    bands, start, prev = [], rows[0], rows[0]
    for r in rows[1:]:
        if r - prev > gap:
            bands.append((int(start), int(prev) + 1))
            start = r
        prev = r
    bands.append((int(start), int(prev) + 1))
    return bands


# ====================================================================================================== a caption run: every script that has strings, every scenario
class StyleRun:
    """Renders the allowlisted test strings of every script that has strings, in the given caption style, with libass (the burn-in path), and measures them in each scenario.
    A script whose strings are empty is reported NOT TESTED, never PASS. Everything is derived from the rendering; nothing about where a mark sits is assumed.
    FileRun (below) is the same analysis on the lines burned into a real file."""

    mode = "style"

    def __init__(self, tools, thr, style, strings, scenarios, aspect=None, scripts_only=None, shifts=(0, 1, 2, 3), want_marks=True, style_name="", say_fn=None, burn_text=None):
        self.burn_text = burn_text or {}                # {string id: text actually burned}: the negative controls burn something other than the line asked for
        self.tools, self.thr, self.style, self.strings = tools, thr, dict(style), strings
        self.scenarios, self.aspect, self.shifts, self.want_marks, self.style_name = list(scenarios), aspect, shifts, want_marks, style_name
        self.scripts_only = scripts_only
        self.say = say_fn or (lambda m: None)
        self.blocks, self.items, self.cues = [], [], {}
        self.fill_clean = {}
        self._deg = {}

    # ---------------------------------------------------------------- what is shown
    def prepare(self):
        max_chars = int(self.style.get("max_chars_per_line", 32))
        lines_fill, cue_lines, cue_keys = [], [], []
        for name, strs in script_blocks(self.strings):
            if self.scripts_only and name not in self.scripts_only:
                continue
            if not strs:
                self.blocks.append({"script": name, "tested": False})
                continue
            self.blocks.append({"script": name, "tested": True})
            words = [s["text"] for s in strs if s.get("kind", "word") == "word"] or [s["text"] for s in strs]
            cue = compose_lines(words, max_chars, int(self.style.get("max_lines", 2)))
            cue_lines.append(cue)
            cue_keys.append(name)
            for s in strs:
                self.items.append({"key": (name, s["id"]), "script": name, "id": s["id"], "text": s["text"], "marks": list(s.get("marks") or []), "kind": s.get("kind")})
                lines_fill.append([self.burn_text.get(s["id"], s["text"])])
        if not lines_fill:
            raise Usage("no script with strings to test")
        for it, cov in zip(self.items, render_cues(self.tools, lines_fill, self.style)):
            self.fill_clean[it["key"]] = cov
        for k, im in zip(cue_keys, render_cues(self.tools, cue_lines, self.style, fill_only=False)):
            self.cues[k] = [{"img": im, "ref": 128, "lines": cue_lines[cue_keys.index(k)]}]

    # ---------------------------------------------------------------- what is on the screen in a scenario (clean, or after the messenger)
    def B_actual(self, key, deg):
        if not deg:
            return self.fill_clean[key]
        if "fill" not in self._deg:
            ks = list(self.fill_clean.keys())
            frames = [np.repeat((np.clip(self.fill_clean[k], 0, 1) * 255).astype(np.uint8)[..., None], 3, axis=2) for k in ks]
            self._deg["fill"] = {k: up_to_1080(fr)[..., 1].astype(np.float32) / 255.0 for k, fr in zip(ks, degrade_frames(self.tools, frames, deg))}
        return self._deg["fill"][key]

    def cue_actual(self, script, deg):
        if not deg:
            return [(c["img"], c["ref"]) for c in self.cues[script]]
        if "cue" not in self._deg:
            ks = list(self.cues.keys())
            flat = [(k, i) for k in ks for i in range(len(self.cues[k]))]
            frames = degrade_frames(self.tools, [self.cues[k][i]["img"] for k, i in flat], deg)
            self._deg["cue"] = {}
            for (k, i), fr in zip(flat, frames):
                self._deg["cue"].setdefault(k, []).append((fr, 128))
        return self._deg["cue"][script]

    # ---------------------------------------------------------------- scenario independent: registration, shaping IoU, face size, mark zones
    def analyse(self):
        lock = self.tools.lock
        self.scr = {}
        for b in self.blocks:
            name = b["script"]
            if not b["tested"] and not b.get("partial"):
                self.scr[name] = {"tested": False}
                continue
            fam, path = self.font_of(name)
            rec = {"tested": bool(b["tested"]), "partial": bool(b.get("partial")), "family": fam, "strings": {}, "font_path": path}
            ems = []
            its = [it for it in self.items if it["script"] == name]
            for it in its:
                variants = [strip_marks(it["text"], m) for m in it["marks"]] if self.want_marks else []
                reg = Registration(self.fill_clean[it["key"]], it["text"], path, name, variants=variants)
                srec = {"id": it["id"], "kind": it["kind"], "reg": reg, "marks": it["marks"], "ok": reg.ok, "geoms": []}
                if reg.ok:
                    ems.append(reg.em_px)
                    srec["iou"], srec["iou_soft"] = reg.iou_b, reg.iou_s
                    if self.want_marks:
                        srec["geoms"] = [MarkGeom(reg, m, i) for i, m in enumerate(it["marks"])]
                rec["strings"][it["id"]] = srec
            rec["em_px"] = float(np.median(ems)) if ems else self.em_from_style(name, path)
            if rec["partial"] and name != "latin":
                rec["face"] = {"basis": "no test strings in this file for this script: size not measured", "x_height_px": None, "cap_height_px": None, "unit": "base-letter band"}
            elif name == "latin" and rec["em_px"] is None:
                rec["face"] = {"basis": "no style numbers in the caption file: size not measured", "x_height_px": None, "cap_height_px": None, "unit": "x-height"}
            elif name == "latin":
                m = font_metrics(path)
                if not (m["x_height"] and m["cap_height"]):
                    raise Env("the Latin font has no sxHeight and sCapHeight in its OS/2 table")
                rec["face"] = {"basis": "OS/2 sxHeight and sCapHeight of the font file times the em fitted to the libass ink", "x_height_px": m["x_height"] / m["units_per_em"] * rec["em_px"],
                               "cap_height_px": m["cap_height"] / m["units_per_em"] * rec["em_px"], "unit": "x-height"}
            else:
                bands = []
                for it in its:
                    allm = set()
                    for m in it["marks"]:
                        allm |= set(cp_to_char(c) for c in m["codepoints"])
                    base = "".join(ch for ch in it["text"] if ch not in allm).strip()
                    if base and rec["em_px"]:
                        bb = ink_bbox(raqm_render(base, path, round(rec["em_px"] * 8, 2), name), 0.5)
                        if bb:
                            bands.append((bb[3] - bb[1]) / 8.0)
                rec["face"] = {"basis": "ink height of the test strings with their marks removed (top of the headline to the baseline), median over the strings: an analogue of the "
                                        "x-height for a script that has none (W-18 sizes Gujarati by the height of KA)", "x_height_px": float(np.median(bands)) if bands else None,
                               "cap_height_px": float(np.max(bands)) if bands else None, "unit": "base-letter band"}
            self.scr[name] = rec

    def font_of(self, script):
        return EP.font_for_script(script, self.tools.lock)

    def em_from_style(self, script, path):
        return None

    def deg_for(self, geo):
        return geo["degrade"]

    def cue_measures(self, script, deg):
        """The caption box of each cue as it is on the screen: [{'box': (x0, y0, x1, y1) in 1080p pixels, 'mask': bool (1080p) of the caption ink, 'img': the frame (native size),
        'g': its grid relative to 1080p}]. Here: the full-style libass drawing on mid grey (outline included), clean or after the messenger."""
        out = []
        for img, ref in self.cue_actual(script, deg):
            img1080 = up_to_1080(img)
            ref1080 = np.full_like(img1080, ref) if np.isscalar(ref) else up_to_1080(ref)
            box = diff_box(img1080, ref1080, 40)
            if box is None:
                continue
            mask = np.abs(img1080.astype(np.int16) - ref1080.astype(np.int16)).max(axis=2) > 40
            out.append({"box": box, "mask": mask, "img": img, "g": img.shape[0] / float(H0)})
        return out

    def s_min_for(self, s):
        return s

    # ---------------------------------------------------------------- one scenario
    def scenario(self, name):
        thr = self.thr
        geo = geometry(name, thr, self.aspect)
        s_dev = geo["device_px_per_source_px"]
        s_min = self.s_min_for(geo["smallest_grid_px_per_source_px"])
        mm_per_px = geo["picture_h_mm"] / float(H0)
        deg = self.deg_for(geo)
        d35, d40 = thr["distance_cm"]["verdict"], thr["distance_cm"]["margin_50plus"]
        out = {"geometry": {k: (rnd(v, 4) if isinstance(v, float) else v) for k, v in geo.items() if k != "degrade"}, "gate": geo["gate"], "scripts": {}}
        for b in self.blocks:
            sc = b["script"]
            if not b["tested"] and not b.get("partial"):
                out["scripts"][sc] = {"status": NT, "reason": b.get("reason") or "no strings in test_strings.json (pending the maker's script, O-10)", "checks": []}
                continue
            rec = self.scr[sc]
            checks, sizes, posrec = [], None, None
            face = rec["face"]
            # --- size
            px = face["x_height_px"]
            if px is None:
                checks.append(check("x_height_arcmin", NM, detail="no measurable ink"))
            else:
                mm = px * mm_per_px
                a35, a40 = arcmin(mm, d35), arcmin(mm, d40)
                d50 = thr["distance_cm"].get("proxy_cm", 50)
                a50 = arcmin(mm, d50)
                pct = px / H0 * 100.0
                xh = thr["x_height"]
                tgt = "target %g' %s" % (xh["target_arcmin"], "reached" if a35 >= xh["target_arcmin"] else "not reached")
                checks.append(check("x_height_arcmin", PASS if a35 >= xh["floor_arcmin"] else FAIL, rnd(a35, 2), xh["floor_arcmin"],
                                    "%s %.1f px at 1080p = %.2f mm on this picture = %.2f arcmin at %g cm (%.2f at %g cm); floor %g', %s (arcminute limits UNVERIFIED)" % (
                                        face["unit"], px, mm, a35, d35, a40, d40, xh["floor_arcmin"], tgt)))
                checks.append(check("x_height_arcmin_50cm", INFO, rnd(a50, 2), xh["floor_arcmin"],
                                    "%.2f arcmin at %g cm, the arm's-length proxy for a 50+ viewer (playbook Exercise 4); %s the %g' floor; reported, never gated (the maker's phone test, question 3, is the measurement)" % (
                                        a50, d50, "at or above" if a50 >= xh["floor_arcmin"] else "below", xh["floor_arcmin"])))
                checks.append(check("x_height_pct", PASS if pct >= xh["floor_pct"] else FAIL, rnd(pct, 2), xh["floor_pct"],
                                    "%s is %.2f%% of picture height (floor %g%%, target %g%%; W-63)" % (face["unit"], pct, xh["floor_pct"], xh["target_pct"])))
                cph = face["cap_height_px"] or 0
                sizes = {"unit": face["unit"], "x_height_px_1080": rnd(px, 2), "x_height_pct": rnd(pct, 2), "x_height_mm": rnd(mm, 3), "x_height_arcmin_35cm": rnd(a35, 2),
                         "x_height_arcmin_40cm": rnd(a40, 2), "x_height_arcmin_50cm": rnd(a50, 2), "x_height_device_px": rnd(px * s_dev, 2), "cap_height_px_1080": rnd(cph, 2), "cap_height_pct": rnd(cph / H0 * 100.0, 2),
                         "cap_height_mm": rnd(cph * mm_per_px, 3), "cap_height_arcmin_35cm": rnd(arcmin(cph * mm_per_px, d35), 2)}
            # --- strokes (the burned fill, scaled to the scenario's smallest grid, worst phase)
            sp = []
            for it in ([] if rec["partial"] else self.items):
                if it["script"] != sc:
                    continue
                sr = rec["strings"][it["id"]]
                if not sr["ok"]:
                    continue
                cov = self.B_actual(it["key"], deg)
                reg = sr["reg"]
                win = cov[reg.fy0:reg.fy1, reg.fx0:reg.fx1]
                for sh in (self.shifts if s_min != 1.0 else (0,)):
                    st = stroke_stat(scale_cov(win, s_min, sh), thr["stroke"]["percentile"])
                    if st:
                        sp.append((st["p"], st["median"]))
            if rec["partial"]:
                pass
            elif sp:
                p10 = min(v[0] for v in sp)
                med = float(np.median([v[1] for v in sp]))
                lim = thr["stroke"]["min_effective_px"]
                checks.append(check("stroke_width_px", PASS if p10 >= lim else FAIL, rnd(p10, 2), lim,
                                    "10th percentile of the local stroke width of the caption letters on the scenario's smallest grid (%.3f of source) = %.2f px (median %.2f)" % (s_min, p10, med)))
            else:
                checks.append(check("stroke_width_px", NM, detail="no ink"))
            # --- contrast and position, from the cue frames (worst over the cues)
            worst = None
            for cm in self.cue_measures(sc, deg):
                box, img, g = cm["box"], cm["img"], cm["g"]
                x0, y0, x1, y1 = box
                top, bot, left, right = y0 / H0 * 100.0, y1 / H0 * 100.0, x0 / W0 * 100.0, x1 / W0 * 100.0
                t = min(s_dev, g)
                cr = contrast_in_box(img if t >= g else scale_rgb(img, t / g), scale_box(box, t))
                crop = geo["crop_each_pct"]
                tot = int(cm["mask"].sum())
                r0, r1 = int(round(crop / 100.0 * H0)), int(round((100.0 - crop) / 100.0 * H0))
                vis = float(cm["mask"][r0:r1].sum()) / tot if tot else 1.0
                cur = {"top": top, "bot": bot, "left": left, "right": right, "contrast": cr[0], "vis": vis}
                if worst is None:
                    worst = cur
                else:
                    worst = {"top": min(worst["top"], top), "bot": max(worst["bot"], bot), "left": min(worst["left"], left), "right": max(worst["right"], right),
                             "contrast": min(worst["contrast"], cr[0]), "vis": min(worst["vis"], vis)}
            if worst is None:
                checks.append(check("caption_box", NM, detail="no caption ink found in the cue frames"))
            else:
                top, bot, left, right, crv, vis = worst["top"], worst["bot"], worst["left"], worst["right"], worst["contrast"], worst["vis"]
                cmin = thr["contrast"]["min_ratio"]
                checks.append(check("contrast_ratio", PASS if crv >= cmin else FAIL, rnd(crv, 1), cmin,
                                    "WCAG ratio of the fill (98th percentile) to the outline (2nd percentile) inside the caption box on the scenario's pixels; target %g" % thr["contrast"]["target_ratio"]))
                b90 = thr["box90"]
                inside = left >= b90["x_min_pct"] and right <= b90["x_max_pct"] and top >= b90["y_min_pct"] and bot <= b90["y_max_pct"]
                checks.append(check("box90", PASS if inside else FAIL, "L%.1f R%.1f T%.1f B%.1f" % (left, right, top, bot), "5..95 both ways",
                                    "caption box as a percentage of picture width and height (W-18: inside the 90% by 90% box)"))
                pos = thr["position"]
                crop = geo["crop_each_pct"]
                lim_b = min(pos["caption_bottom_max_pct"], 100.0 - crop - pos["crop_margin_pts"]) if crop > 0 else pos["caption_bottom_max_pct"]
                lim_t = max(pos["caption_top_min_pct"], crop + pos["crop_margin_pts"]) if crop > 0 else pos["caption_top_min_pct"]
                if crop > 0:
                    checks.append(check("caption_bottom_pct", PASS if bot <= lim_b + 1e-9 else FAIL, rnd(bot, 1), "<= %.1f" % lim_b,
                                        "bottom of the caption box at %.1f%% of picture height; a %s fill crop removes the bottom %.1f%%, so the limit is %.1f%% (crop line %.1f%% minus a %g-point margin, "
                                        "or %g%% if lower) (J)" % (bot, geo["aspect"], crop, lim_b, 100 - crop, pos["crop_margin_pts"], pos["caption_bottom_max_pct"])))
                    checks.append(check("caption_top_pct", PASS if top >= lim_t - 1e-9 else FAIL, rnd(top, 1), ">= %.1f" % lim_t, "top of the caption box at %.1f%% of picture height" % top))
                    checks.append(check("caption_visible_fraction", PASS if vis >= pos["fill_visible_min"] else FAIL, rnd(vis, 4), ">= %g" % pos["fill_visible_min"],
                                        "fraction of the caption ink that stays on the screen when the player fills it"))
                else:
                    checks.append(check("caption_bottom_pct", INFO, rnd(bot, 1), "<= %g in fill_20x9" % pos["caption_bottom_max_pct"],
                                        "bottom of the caption box at %.1f%%, top at %.1f%% (the 88%% limit is gated in fill_20x9; here only the 90%% box is)" % (bot, top)))
                posrec = {"caption_top_pct": rnd(top, 2), "caption_bottom_pct": rnd(bot, 2), "caption_left_pct": rnd(left, 2), "caption_right_pct": rnd(right, 2), "visible_fraction": rnd(vis, 4),
                          "crop_each_pct": rnd(crop, 2), "contrast_ratio": rnd(crv, 1), "bottom_limit_pct": rnd(lim_b, 1)}
            # --- mark survival
            if self.want_marks and not rec["partial"]:
                for it in self.items:
                    if it["script"] != sc or not it["marks"]:
                        continue
                    sr = rec["strings"][it["id"]]
                    if not sr["ok"]:
                        checks.append(check("marks:" + it["id"], FAIL, detail="no ink for this string"))
                        continue
                    reg = sr["reg"]
                    Bwin = self.B_actual(it["key"], deg)[reg.fy0:reg.fy1, reg.fx0:reg.fx1]
                    parts, allok = [], True
                    for m, g in zip(it["marks"], sr["geoms"]):
                        if not g.ok:
                            parts.append("%s %s: NOT MEASURED (%s)" % (m["kind"], "+".join(m["codepoints"]), g.note))
                            allok = False
                            continue
                        res = mark_eval(g, Bwin, s_min, thr["marks"], self.shifts)
                        parts.append("%s %s: %d px of ink in the zone (%s zone, %d px at 1080p); IoU with the mark %.2f, without %.2f -> %s" % (
                            m["kind"], "+".join(m["codepoints"]), res["ink_px"], g.basis, g.zone_px, res["iou_with"], res["iou_without"], "survives" if res["survives"] else "LOST"))
                        allok = allok and res["survives"]
                    checks.append(check("marks:" + it["id"], PASS if allok else FAIL, detail="; ".join(parts)))
            out["scripts"][sc] = {"status": FAIL if any(c["status"] == FAIL for c in checks) else PASS, "checks": checks, "sizes": sizes, "position": posrec}
        fails = [(sc, c["id"]) for sc, v in out["scripts"].items() for c in v.get("checks", []) if c["status"] == FAIL]
        out["verdict"] = FAIL if fails else PASS
        out["failed_checks"] = ["%s:%s" % f for f in fails]
        return out

    def global_checks(self):
        """Per script: shaping IoU against Pillow-raqm (scenario independent)."""
        res = {}
        for b in self.blocks:
            sc = b["script"]
            if not b["tested"]:
                res[sc] = {"status": NT, "reason": b.get("reason") or "no strings in test_strings.json (pending the maker's script, O-10)"}
                continue
            rec = self.scr[sc]
            lim = self.thr["iou"]["min"]
            per = {sid: rnd(sr.get("iou"), 3) for sid, sr in rec["strings"].items()}
            vals = [v for v in per.values() if v is not None]
            ok = bool(vals) and min(vals) >= lim and all(sr["ok"] for sr in rec["strings"].values())
            res[sc] = {"status": PASS if ok else FAIL, "iou_min": rnd(min(vals), 3) if vals else None, "iou_limit": lim, "iou_by_string": per, "family": rec["family"],
                       "em_px": rnd(rec["em_px"], 2), "strings_tested": len(per),
                       "finding": None if ok else "SHAPING FINDING: the libass ink of at least one test string of this script does not match the Pillow-raqm reference (IoU below %g); "
                                                  "see build/evidence/wp08/shaping_paths.json" % lim}
        return res

    def run(self):
        self.prepare()
        self.analyse()
        rep = {"mode": self.mode, "style": self.style_name, "style_params": {k: self.style.get(k) for k in ("font_size", "font_size_by_script", "margin_v", "outline", "max_chars_per_line", "max_lines")},
               "ffmpeg": self.tools.version, "scenarios": {}, "iou": self.global_checks()}
        for name in self.scenarios:
            self.say("  scenario %s ..." % name)
            rep["scenarios"][name] = self.scenario(name)
        rep["scripts_tested"] = [b["script"] for b in self.blocks if b["tested"]]
        rep["scripts_not_tested"] = [b["script"] for b in self.blocks if not b["tested"]]
        rep["scripts_partial"] = [b["script"] for b in self.blocks if b.get("partial") and not b["tested"]]
        return rep


# ====================================================================================================== lines and title in a frame (the phone-safe frame rules)
def _lum255(img):
    return rel_luminance(img) * 255.0


def line_contrast(lum, box, s):
    """Contrast of a line against its surround on a luminance image: |(the most deviating pixel in the line's box) - (median of the ring around it)|. box in source pixels, s the
    scale of `lum` relative to the source."""
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = int(math.floor(x0 * s)), int(math.floor(y0 * s)), int(math.ceil(x1 * s)), int(math.ceil(y1 * s))
    m = 6
    h, w = lum.shape
    ring = lum[max(0, Y0 - m):min(h, Y1 + m), max(0, X0 - m):min(w, X1 + m)].copy()
    inner = np.zeros(ring.shape, dtype=bool)
    iy0, ix0 = Y0 - max(0, Y0 - m), X0 - max(0, X0 - m)
    inner[max(0, iy0 - 1):iy0 + (Y1 - Y0) + 1, max(0, ix0 - 1):ix0 + (X1 - X0) + 1] = True
    bgv = float(np.median(ring[~inner])) if (~inner).any() else float(np.median(ring))
    core = lum[max(0, Y0):min(h, Y1), max(0, X0):min(w, X1)]
    dev = np.abs(core - bgv)
    return float(dev.max()) if dev.size else 0.0


def lines_check(tools, thr, frame, items, scenario, aspect=None, gate_from=None, frame_native=None):
    """The thin-line rule of the phone-safe frame on a decoded frame. items: [{'kind', 'width_px', 'box': (x0, y0, x1, y1) in 1080p pixels}]. For each line: its width on the
    scenario's smallest grid (width x scale) and the contrast it keeps (retention) against the surround. A line of gate_from pixels or more (default
    thresholds stroke.must_survive_from_width_px) FAILs below stroke.min_effective_px or stroke.retention_min; a thinner line is measured and reported (INFO).
    frame: the frame at 1920x1080 (coordinates, and the contrast before the scenario). frame_native: the frame as it reaches the scenario at its own grid (for 'shared', the
    messenger's output at 480p; for a file that is already small, the file's own frame); computed here when not given."""
    geo = geometry(scenario, thr, aspect)
    cfg = thr["stroke"]
    gate_from = cfg["must_survive_from_width_px"] if gate_from is None else gate_from
    if frame_native is None:
        frame_native = degrade_frames(tools, [frame], geo["degrade"])[0] if geo["degrade"] else frame
    g = frame_native.shape[0] / float(H0)
    t = min(geo["smallest_grid_px_per_source_px"], g)
    img_t = frame_native if t >= g - 1e-9 else scale_rgb(frame_native, t / g)
    lum0, lum1 = _lum255(frame), _lum255(img_t)
    res = []
    for it in items:
        c0 = line_contrast(lum0, it["box"], 1.0)
        c1 = line_contrast(lum1, it["box"], t)
        ret = (c1 / c0) if c0 > 0 else 0.0
        eff = it["width_px"] * t
        gated = it["width_px"] >= gate_from
        ok = eff >= cfg["min_effective_px"] and ret >= cfg["retention_min"]
        res.append({"kind": it["kind"], "width_px": it["width_px"], "effective_px": rnd(eff, 2), "retention": rnd(ret, 2), "gated": gated, "status": (PASS if ok else FAIL) if gated else INFO})
    return res


def title_ink_pct(frame, box):
    """Ink height of the title in a box as a percentage of picture height: rows holding pixels well above the box's background level."""
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    lum = _lum255(frame)[max(0, y0):y1, max(0, x0):x1]
    bgv = float(np.percentile(lum, 20))
    top = float(lum.max())
    if top - bgv < 40:
        return None
    rows = np.where((lum > bgv + 0.5 * (top - bgv)).any(axis=1))[0]
    return float((rows[-1] - rows[0] + 1) / H0 * 100.0) if rows.size else None


def ink_stroke_p10(frame_native, box, t, pct=10):
    """10th-percentile stroke width of bright ink in a box of a decoded frame (a title or a headline), on the scenario's grid t (the frame's own grid g is what it arrived at;
    when t is smaller the frame is scaled down by t/g), worst over four sampling phases. None when the box holds no ink."""
    g = frame_native.shape[0] / float(H0)
    x0, y0, x1, y1 = [int(round(v * g)) for v in box]
    lum = _lum255(frame_native)[max(0, y0):y1, max(0, x0):x1]
    if lum.size == 0:
        return None
    bgv = float(np.percentile(lum, 20))
    top = float(lum.max())
    if top - bgv < 40:
        return None
    cov = np.clip((lum - bgv) / (top - bgv), 0.0, 1.0).astype(np.float32)
    worst = None
    for sh in (0, 1, 2, 3):
        c = cov if t >= g - 1e-9 else scale_cov(cov, t / g, sh)
        st = stroke_stat(c, pct)
        if st and (worst is None or st["p"] < worst):
            worst = st["p"]
        if t >= g - 1e-9:
            break
    return worst


# ====================================================================================================== a real file: the lines burned into it
def degrade_file(tools, path, deg, out_name="shared.mp4"):
    """Re-encode a file the way a messenger would (thresholds degrade_shared); returns the path of the copy in the work folder. Never touches the input."""
    d = tools.sub("df_%d" % len(os.listdir(tools.work.path)))
    tags = "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
    vf = "scale=-2:%d:flags=bicubic:out_color_matrix=bt709:out_range=tv,format=yuv420p,%s" % (deg["height"], tags)
    cmd = [tools.ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", os.path.abspath(path), "-an", "-vf", vf, "-c:v", "libx264", "-preset", deg["preset"], "-profile:v", deg["profile"],
           "-b:v", deg["video_bitrate"], "-maxrate", deg["maxrate"], "-bufsize", deg["bufsize"], "-g", "48", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-color_range", "tv", out_name]
    rc, so, se = tools.run(cmd, cwd=d)
    if rc != 0:
        raise Env("the messenger re-encode failed: %s" % EP.tail(se, 3))
    return os.path.join(d, out_name)


def alpha_from_diff(img1080, ref1080, rows):
    """Coverage of a white caption fill over a known picture: (G - G_ref) / (255 - G_ref), only inside the rows (r0, r1) of one caption line; zero elsewhere."""
    g, gr = img1080[..., 1].astype(np.float32), ref1080[..., 1].astype(np.float32)
    a = np.clip((g - gr) / np.maximum(255.0 - np.minimum(gr, 215.0), 40.0), 0.0, 1.0)
    out = np.zeros_like(a)
    r0, r1 = rows
    out[r0:r1] = a[r0:r1]
    return out


class FileRun(StyleRun):
    """The same analysis on the captions burned into a phone file. The caption file the burn-in used (OUTPUT.ass, written by encode_phone.py) says what was burned and when:
    libass draws it again, clean, to give each line's own shape, which is registered against Pillow-raqm for the shaping IoU and gives the mark zones; the file's own decoded
    frames, differenced against a caption-free frame of the same file, give what is on the screen (box, contrast, strokes, mark ink), and for 'shared' the file is re-encoded the way
    a messenger would first. A line that is one or more allowlisted test strings joined by spaces (test_strings.json) is tested for shaping and marks; any other text is free text:
    its position, size and contrast are measured, but it is NOT TESTED for marks. The differencing needs a caption-free frame and a static picture under the captions (the test
    master has both); --no-diff uses the libass drawing of the burned file instead."""

    mode = "file"

    def __init__(self, tools, thr, path, ass_text, strings, scenarios, aspect=None, shifts=(0, 1, 2, 3), say_fn=None, max_cues=12, use_diff=True, probe=None):
        StyleRun.__init__(self, tools, thr, {}, strings, scenarios, aspect=aspect, shifts=shifts, want_marks=True, style_name="file", say_fn=say_fn)
        self.path, self.ass_text, self.max_cues, self.use_diff, self.probe = path, ass_text, max_cues, use_diff, probe
        self.fps = 24.0
        self.native_h = int(probe["video"]["height"])
        self.native_scale = min(1.0, self.native_h / float(H0))
        self.free_lines = 0
        self.burn_match = {}

    # the style numbers that the burn-in used, read back from the ASS
    def ass_style_numbers(self):
        styles, _ev = ass_style_header(self.ass_text)
        st = next(iter(styles.values()), {})
        return st

    def em_from_style(self, script, path):
        m = font_metrics(path)
        styles, _ev = ass_style_header(self.ass_text)
        fs = None
        for nm, st in styles.items():
            if nm.endswith(script):
                fs = float(st["Fontsize"])
        if fs is None:
            return None
        play_y = float(re.search(r"PlayResY:\s*(\d+)", self.ass_text).group(1))
        return fs * (H0 / play_y) * m["units_per_em"] / float(m["win_ascent"] + m["win_descent"])

    def prepare(self):
        cues = ass_cues(self.ass_text)
        if not cues:
            raise Usage("the caption file holds no cues")
        allow = []
        for name, strs in script_blocks(self.strings):
            for s in strs:
                allow.append((s["text"], {"script": name, "entry": s}))
        allow.sort(key=lambda t: -len(t[0]))
        # pick the cues to look at: the widest line first, then evenly spaced
        order = sorted(range(len(cues)), key=lambda i: -max((EP.count_chars(l) for l in cues[i]["lines"]), default=0))
        chosen = set(order[:1])
        step = max(1, len(cues) // max(1, self.max_cues))
        chosen |= set(range(0, len(cues), step))
        chosen = sorted(chosen)[:max(self.max_cues, 1)]
        self.chosen = chosen
        # a caption-free frame of the same file
        dur_ms = int(float(self.probe["format"].get("duration") or 0) * 1000)
        busy = [(c["start_ms"], c["end_ms"]) for c in cues]
        ref_t = None
        for t in [100] + [c["end_ms"] + 200 for c in cues] + [max(0, c["start_ms"] - 200) for c in cues]:
            if 0 <= t < dur_ms - 100 and not any(a - 100 <= t <= b + 100 for a, b in busy):
                ref_t = t
                break
        self.ref_idx = int(round(ref_t / 1000.0 * self.fps)) if ref_t is not None else None
        self.cue_idx = {i: int(round(((cues[i]["start_ms"] + cues[i]["end_ms"]) / 2) / 1000.0 * self.fps)) for i in chosen}
        self.diff = self.use_diff and self.ref_idx is not None
        # libass draws the burned file's captions again, clean (white on black, no outline)
        scripts = set(EP.script_of_text(l) for i in chosen for l in cues[i]["lines"])
        ass_fill = ass_for_render(self.ass_text, len(cues), True, order=chosen)
        imgs, _log = libass_batch(self.tools, ass_fill, len(chosen), bg="000000", scripts=scripts, tag="fr")
        fills = [im[..., 1].astype(np.float32) / 255.0 for im in imgs]
        self.fills = dict(zip(chosen, fills))
        self.rows, self.lines = {}, []
        script_cues = {}
        for i in chosen:
            c = cues[i]
            bands = row_bands(self.fills[i])
            by_line = len(bands) == len(c["lines"])
            for j, text in enumerate(c["lines"]):
                sc = EP.script_of_text(text)
                script_cues.setdefault(sc, set()).add(i)
                tiling = tile_line(text, allow)
                if not by_line or tiling is None:
                    self.free_lines += 1
                    continue
                key = (sc, "c%d_l%d" % (i, j))
                r0, r1 = bands[j]
                marks, seen = [], set()
                for ent in tiling:
                    for m in (ent["entry"].get("marks") or []):
                        sig = (tuple(m["codepoints"]), m["kind"])
                        if sig not in seen:
                            seen.add(sig)
                            marks.append(m)
                cov = np.zeros_like(self.fills[i])
                cov[r0:r1] = self.fills[i][r0:r1]
                self.fill_clean[key] = cov
                self.rows[key] = (max(0, r0 - 3), min(H0, r1 + 3), i)
                self.items.append({"key": key, "script": sc, "id": key[1], "text": text, "marks": marks, "kind": "line"})
        self.blocks = []
        have = set(it["script"] for it in self.items)
        for name, strs in script_blocks(self.strings):
            if name in have:
                self.blocks.append({"script": name, "tested": True})
            elif name in script_cues:
                self.blocks.append({"script": name, "tested": False, "partial": True, "reason": "free text only: no marks[] or reference strings for the lines of this script in the file"})
            elif strs:
                self.blocks.append({"script": name, "tested": False, "reason": "not in this file's captions"})
            else:
                self.blocks.append({"script": name, "tested": False, "reason": "no strings in test_strings.json (pending the maker's script, O-10)"})
        for sc in script_cues:
            if sc not in [b["script"] for b in self.blocks]:
                self.blocks.append({"script": sc, "tested": False, "partial": True, "reason": "no test strings for this script"})
        # frames from the file
        self.cue_ids = {sc: sorted(v) for sc, v in script_cues.items()}
        self._frames = {}
        self._load_frames(None)

    def _load_frames(self, deg):
        tag = "deg" if deg else "clean"
        path = self.path
        if deg:
            path = degrade_file(self.tools, self.path, deg)
        idxs = list(self.cue_idx.values()) + ([self.ref_idx] if self.ref_idx is not None else [])
        frames = decode_indices(self.tools, path, idxs)
        self._frames[tag] = {}
        for k, i in enumerate(list(self.cue_idx.keys())):
            self._frames[tag][i] = frames[k]
        self._frames[tag]["ref"] = frames[len(self.cue_idx)] if self.ref_idx is not None else None
        if deg:
            shutil.rmtree(os.path.dirname(path), ignore_errors=True)

    def _state(self, deg):
        tag = "deg" if deg else "clean"
        if tag not in self._frames:
            self._load_frames(deg)
        return self._frames[tag]

    def B_actual(self, key, deg):
        r0, r1, i = self.rows[key]
        if not self.diff:
            return self.fill_clean[key]
        fr = self._state(deg)
        img, ref = up_to_1080(fr[i]), up_to_1080(fr["ref"])
        cache = self._deg.setdefault("B_%s" % ("deg" if deg else "clean"), {})
        if key not in cache:
            cache[key] = alpha_from_diff(img, ref, (r0, r1))
        return cache[key]

    def cue_actual(self, script, deg):
        fr = self._state(deg)
        out = []
        for i in self.cue_ids.get(script, []):
            if self.diff:
                out.append((fr[i], fr["ref"]))
            else:
                # no caption-free frame (or --no-diff): the libass drawing of the burned captions, on grey
                ass_full = ass_for_render(self.ass_text, len(self.cue_idx), False, order=[i])
                im, _l = libass_batch(self.tools, ass_full, 1, bg="808080", scripts=set([script]), tag="ff")
                out.append((im[0], 128))
        return out

    def deg_for(self, geo):
        d = geo["degrade"]
        if d and self.native_h <= d["already_degraded_if_height_at_most"]:
            return None
        return d

    def s_min_for(self, s):
        return min(s, self.native_scale)

    def ref_frame(self, deg):
        return self._state(deg)["ref"]

    def cue_measures(self, script, deg):
        """Each cue's caption box in the file: the white fill found by differencing the cue frame against the caption-free frame, looked for only in the rows of the cue's own lines
        (plus a margin), then grown by the outline width of the burn-in (a black outline cannot be told from a dark picture, so it is added from the ASS style, not detected).
        Without a caption-free frame the libass drawing of the burned captions stands in for the file's pixels."""
        if not self.diff:
            return StyleRun.cue_measures(self, script, deg)
        fr = self._state(deg)
        styles, _ev = ass_style_header(self.ass_text)
        play_y = float(re.search(r"PlayResY:\s*(\d+)", self.ass_text).group(1))
        op = max(float(st.get("Outline", 0)) for st in styles.values()) * H0 / play_y if styles else 0.0
        out = []
        for i in self.cue_ids.get(script, []):
            bands = row_bands(self.fills[i])
            if not bands:
                continue
            w0, w1 = max(0, bands[0][0] - 40), min(H0, bands[-1][1] + 40)
            img, ref = up_to_1080(fr[i]), up_to_1080(fr["ref"])
            a = alpha_from_diff(img, ref, (w0, w1))
            mask = a > 0.5
            if not mask.any():
                continue
            ys, xs = np.where(mask.any(axis=1))[0], np.where(mask.any(axis=0))[0]
            box = (max(0, int(xs[0] - math.ceil(op))), max(0, int(ys[0] - math.ceil(op))), min(W0, int(xs[-1] + 1 + math.ceil(op))), min(H0, int(ys[-1] + 1 + math.ceil(op))))
            out.append({"box": box, "mask": mask, "img": fr[i], "g": fr[i].shape[0] / float(H0)})
        return out


def burn_match_report(run):
    """IoU of the file's own burned lines (decoded, differenced) against the clean libass drawing of the same ASS: does the sidecar describe what is in the file?"""
    res = {}
    if not run.diff:
        return {"status": NM, "reason": "no caption-free frame in the file (or --no-diff): the libass drawing of the burned captions stands in for the file's pixels"}
    for it in run.items:
        key = it["key"]
        Bf = run.B_actual(key, False)
        c = run.fill_clean[key]
        res[it["id"]] = rnd(iou_binary(Bf > 0.5, c > 0.5), 3)
    lim = run.thr["file_check"]["burn_match_iou_min"]
    vals = list(res.values())
    return {"status": PASS if vals and min(vals) >= lim else FAIL, "iou_min": min(vals) if vals else None, "limit": lim, "by_line": res}


# ====================================================================================================== reports
def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def scenario_line(name, sv):
    parts = []
    for sc, v in sv["scripts"].items():
        if v.get("status") == NT:
            parts.append("%s NOT TESTED" % sc)
        else:
            parts.append("%s %s" % (sc, v["status"]))
    return "%-14s %-4s (%s)  %s" % (name, sv["verdict"], sv["gate"], "; ".join(parts))


def thr_gate(lines):
    ws = [c["width_px"] for c in lines if c["gated"]]
    return min(ws) if ws else 0


def print_report(rep, say_fn=say, quiet=False):
    say_fn("style %s: %s" % (rep.get("style") or rep.get("mode"), json.dumps(rep.get("style_params"), ensure_ascii=False)))
    for sc, v in rep["iou"].items():
        if v["status"] == NT:
            say_fn("  %-10s NOT TESTED (%s)" % (sc, v.get("reason")))
        else:
            say_fn("  %-10s shaping IoU against Pillow-raqm: %s (min %s, limit %s, %d strings)  family %s%s" % (sc, v["status"], v["iou_min"], v["iou_limit"], v["strings_tested"], v["family"],
                                                                                                          ("  <- " + v["finding"]) if v.get("finding") else ""))
    for name, sv in rep["scenarios"].items():
        say_fn(scenario_line(name, sv))
        if quiet:
            continue
        for sc, v in sv["scripts"].items():
            if v.get("status") == NT:
                continue
            for c in v["checks"]:
                if c["status"] != PASS or c["id"].startswith(("caption_bottom", "x_height_arcmin")):
                    say_fn("     %-4s %-10s %-24s %s" % (c["status"], sc, c["id"], (c.get("detail") or "")[:230]))
        ln = sv.get("lines", [])
        if ln:
            gated = [c for c in ln if c["gated"]]
            thin = [c for c in ln if not c["gated"]]
            bad = [c for c in gated if c["status"] == FAIL]
            say_fn("     lines: %d gated (%d px or more): %d pass, %d fail%s; thinner lines, reported only: %s" % (
                len(gated), thr_gate(ln), len(gated) - len(bad), len(bad), ("  <- " + ", ".join("%s %d px keeps %s" % (c["kind"], c["width_px"], c["retention"]) for c in bad)) if bad else "",
                "; ".join("%s %d px -> %s px keeps %s" % (c["kind"], c["width_px"], c["effective_px"], c["retention"]) for c in thin) or "none"))
        for c in sv.get("frame_checks", []):
            say_fn("     %-4s frame      %s %s" % (c["status"], c["id"], c.get("detail", "")))


def exit_code(rep):
    bad = [n for n, sv in rep["scenarios"].items() if sv["verdict"] == FAIL and sv["gate"] == "blocking"]
    iou_bad = [sc for sc, v in rep["iou"].items() if v["status"] == FAIL]
    extra = rep.get("burn_match", {}).get("status") == FAIL
    return 1 if (bad or iou_bad or extra) else 0


def scripts_tested_doc(rep, strings_path):
    tested, not_tested = rep["scripts_tested"], rep["scripts_not_tested"]
    per = {}
    for sc, v in rep["iou"].items():
        if v["status"] == NT:
            per[sc] = {"status": NT, "reason": v.get("reason")}
            continue
        marks_total = marks_ok = 0
        for sv in rep["scenarios"].values():
            sr = sv["scripts"].get(sc, {})
            for c in sr.get("checks", []):
                if c["id"].startswith("marks:"):
                    marks_total += 1
                    marks_ok += 1 if c["status"] == PASS else 0
        per[sc] = {"status": v["status"], "strings_tested": v["strings_tested"], "shaping_iou_min": v["iou_min"], "shaping_iou_limit": v["iou_limit"], "family": v["family"],
                   "mark_checks": marks_total, "mark_checks_passed": marks_ok,
                   "scenarios": {n: sv["scripts"].get(sc, {}).get("status") for n, sv in rep["scenarios"].items()}}
    failed = [sc for sc in tested if per[sc]["status"] == FAIL]
    line = "Scripts tested: %s (neutral strings) on %s; NOT TESTED: %s (name the maker's script, O-10)" % (", ".join(tested) or "none", today(), ", ".join(not_tested) or "none")
    if failed:
        line += " [shaping FAIL for: %s]" % ", ".join(failed)
    return {"schema": "lj-scripts-tested/1", "date_utc": today(), "tool": "phone_check.py", "ffmpeg": rep.get("ffmpeg"), "style": rep.get("style"), "strings_file": os.path.basename(strings_path),
            "checked_by_reader": "false for every entry in test_strings.json until the maker confirms them: shape tests only, never shown to anyone",
            "scripts_tested": tested, "scripts_not_tested": not_tested, "scripts": per, "line": line}


# ====================================================================================================== the FontSize=23 finding, the candidate sizes, the shaping paths
def run_style(tools, thr, prof, style_key, strings, scenarios, aspect=None, want_marks=True, say_fn=None, font_size=None, margin_v=None, scripts_only=None):
    style = dict(prof["caption"]["styles"][style_key])
    if font_size is not None:
        style["font_size"] = font_size
    if margin_v is not None:
        style["margin_v"] = margin_v
    run = StyleRun(tools, thr, style, strings, scenarios, aspect=aspect, scripts_only=scripts_only, want_marks=want_marks, style_name=style_key, say_fn=say_fn)
    return run.run()


def finding_fs23(tools, thr, prof, strings, say_fn=say):
    """What FontSize=23 does on a phone, per scenario, measured. A finding, not a pass condition: the verdicts are whatever the numbers say."""
    scenarios = list(thr["viewports"].keys())
    ven = run_style(tools, thr, prof, "venue_fs23", strings, scenarios, say_fn=say_fn)
    pho = run_style(tools, thr, prof, prof["caption"]["default_style"], strings, scenarios, say_fn=say_fn)
    by = {}
    for n in scenarios:
        v = ven["scenarios"][n]
        entry = {"gate": v["gate"], "verdict": v["verdict"], "failed_checks": v["failed_checks"], "scripts": {}}
        for sc, sv in v["scripts"].items():
            if sv.get("status") == NT:
                entry["scripts"][sc] = {"status": NT}
                continue
            entry["scripts"][sc] = {"status": sv["status"], "sizes": sv["sizes"], "position": sv["position"],
                                    "failed": [c["id"] for c in sv["checks"] if c["status"] == FAIL],
                                    "checks": {c["id"]: {"status": c["status"], "value": c.get("value"), "limit": c.get("limit")} for c in sv["checks"]}}
        by[n] = entry
    cmp_ = {n: {"verdict": pho["scenarios"][n]["verdict"], "failed_checks": pho["scenarios"][n]["failed_checks"],
                "latin": {"x_height_pct": pho["scenarios"][n]["scripts"]["latin"]["sizes"]["x_height_pct"], "x_height_arcmin_35cm": pho["scenarios"][n]["scripts"]["latin"]["sizes"]["x_height_arcmin_35cm"],
                          "caption_bottom_pct": (pho["scenarios"][n]["scripts"]["latin"]["position"] or {}).get("caption_bottom_pct")}} for n in scenarios}
    lat = by["landscape"]["scripts"]["latin"]
    fill = by["fill_20x9"]["scripts"]["latin"]
    words = ["FontSize=23 (MarginV 20), the venue caption of the settings card, drawn by libass in Noto Sans on a 1080p frame and viewed in the five scenarios: "
             "sideways its Latin x-height is %.2f%% of picture height (%.2f arcmin at 35 cm; floor %g%% / %g arcmin) and the caption box ends at %.1f%% of picture height; "
             "against the %.1f%% limit that applies when a 20:9 player fills the screen." % (
                 lat["sizes"]["x_height_pct"], lat["sizes"]["x_height_arcmin_35cm"], thr["x_height"]["floor_pct"], thr["x_height"]["floor_arcmin"], lat["position"]["caption_bottom_pct"],
                 fill["position"]["bottom_limit_pct"])]
    return {"schema": "lj-finding/1", "package": "WP-08", "finding": "fontsize23_on_a_phone", "kind": "FINDING, not a pass condition: the verdicts below are whatever the measurements say; nothing asserts them",
            "date_utc": today(), "ffmpeg": tools.version, "summary": words[0], "style": prof["caption"]["styles"]["venue_fs23"]["description"],
            "style_params": ven["style_params"], "scenarios": by, "phone_style_for_comparison": {"style": prof["caption"]["default_style"], "style_params": pho["style_params"], "scenarios": cmp_},
            "iou": ven["iou"], "unverified": ["every viewport figure and the arcminute limits (thresholds.json unverified list)", "how a given player implements fill (arithmetic, not a measurement of any app)",
                                              "the face: FontSize means a different x-height in a different face (the research fixtures used Liberation Sans; this run uses Noto Sans from the lock file)"]}


def candidates_doc(tools, thr, prof, strings, say_fn=say):
    sizes = prof["caption"]["candidate_font_sizes"]
    rows = []
    for fs in sizes:
        rep = run_style(tools, thr, prof, prof["caption"]["default_style"], strings, ["landscape", "fill_20x9"], want_marks=False, font_size=fs)
        lat = rep["scenarios"]["landscape"]["scripts"]["latin"]
        dev = rep["scenarios"]["landscape"]["scripts"].get("devanagari", {})
        fl = rep["scenarios"]["fill_20x9"]["scripts"]["latin"]
        row = {"font_size": fs, "latin_x_height_px": lat["sizes"]["x_height_px_1080"], "latin_x_height_pct": lat["sizes"]["x_height_pct"], "latin_arcmin_35cm": lat["sizes"]["x_height_arcmin_35cm"],
               "latin_arcmin_40cm": lat["sizes"]["x_height_arcmin_40cm"], "devanagari_band_pct": (dev.get("sizes") or {}).get("x_height_pct"),
               "devanagari_arcmin_35cm": (dev.get("sizes") or {}).get("x_height_arcmin_35cm"), "block_top_pct": lat["position"]["caption_top_pct"], "block_bottom_pct": fl["position"]["caption_bottom_pct"],
               "block_left_pct": lat["position"]["caption_left_pct"], "block_right_pct": lat["position"]["caption_right_pct"], "box90": [c["status"] for c in lat["checks"] if c["id"] == "box90"][0],
               "fill_20x9_bottom_limit_pct": fl["position"]["bottom_limit_pct"]}
        xh = thr["x_height"]
        row["meets_rule"] = bool(row["latin_arcmin_35cm"] >= xh["target_arcmin"] and row["latin_arcmin_40cm"] >= xh["floor_arcmin"] and row["latin_x_height_pct"] >= xh["floor_pct"]
                                 and (row["devanagari_band_pct"] is None or row["devanagari_band_pct"] >= xh["floor_pct"]) and row["block_bottom_pct"] <= row["fill_20x9_bottom_limit_pct"] and row["box90"] == PASS)
        rows.append(row)
        say_fn("  FontSize %-3g latin x-height %.2f%% (%.1f' at 35 cm, %.1f' at 40 cm), devanagari band %s%%, block %.1f%% to %.1f%% high, box90 %s -> %s" % (
            fs, row["latin_x_height_pct"], row["latin_arcmin_35cm"], row["latin_arcmin_40cm"], row["devanagari_band_pct"], row["block_top_pct"], row["block_bottom_pct"], row["box90"],
            "meets the rule" if row["meets_rule"] else "does not"))
    pick = next((r["font_size"] for r in rows if r["meets_rule"]), None)
    return {"schema": "lj-candidates/1", "package": "WP-08", "date_utc": today(), "ffmpeg": tools.version, "margin_v": prof["caption"]["styles"][prof["caption"]["default_style"]]["margin_v"],
            "rule": "the smallest candidate FontSize whose Latin x-height in landscape reaches the target (%g arcmin) at the %g cm design distance and the floor (%g arcmin) at the %g cm margin distance, "
                    "whose x-height and Devanagari base-letter band are at least %g%% of picture height, and whose two-line block (MarginV %g, %d characters a line) ends at or above the fill_20x9 limit "
                    "and inside the 90%% box (J; arcminute limits UNVERIFIED)" % (thr["x_height"]["target_arcmin"], thr["distance_cm"]["verdict"], thr["x_height"]["floor_arcmin"],
                                                                                 thr["distance_cm"]["margin_50plus"], thr["x_height"]["floor_pct"],
                                                                                 prof["caption"]["styles"][prof["caption"]["default_style"]]["margin_v"], prof["caption"]["styles"][prof["caption"]["default_style"]]["max_chars_per_line"]),
            "rows": rows, "picked_font_size": pick, "profile_font_size": prof["caption"]["styles"][prof["caption"]["default_style"]]["font_size"],
            "agrees_with_profile": pick == prof["caption"]["styles"][prof["caption"]["default_style"]]["font_size"],
            "note": "Latin only has an x-height; other scripts are sized by font_size_by_script once a reader of that script has looked (W-18 sizes Gujarati by the height of KA)."}


def shaping_paths_doc(tools, thr, prof, strings, say_fn=say):
    """The burn-in paths against the Pillow-raqm reference, per script: the `ass` filter on an ASS file (the profile's path), the same with libass forced to simple shaping, and the
    `subtitles` filter on an SRT (the path ffmpeg before n9.0 draws in simple shaping)."""
    style = dict(prof["caption"]["styles"][prof["caption"]["default_style"]])
    out = {"schema": "lj-shaping-paths/1", "package": "WP-08", "date_utc": today(), "ffmpeg": tools.version, "style": prof["caption"]["default_style"], "scripts": {}, "notes": []}
    ass_cfg = prof["caption"]["ass"]
    for name, strs in script_blocks(strings):
        if not strs:
            out["scripts"][name] = {"status": NT, "reason": "no strings in test_strings.json"}
            continue
        fam, path = EP.font_for_script(name, tools.lock)
        texts = [s["text"] for s in strs]
        cues = cues_for([[t] for t in texts])
        ass = EP.build_ass(cues, style, {name: fam, "latin": EP.font_for_script("latin", tools.lock)[0]}, outline_override=0)
        srt = "".join("%d\n00:00:%02d,000 --> 00:00:%02d,900\n%s\n\n" % (k + 1, k, k, t) for k, t in enumerate(texts))
        fs = style["font_size"]
        srt_style = "FontName=%s,FontSize=%g,MarginV=%g,Outline=0,Shadow=0,PrimaryColour=&HFFFFFF&,WrapStyle=2" % (fam, fs, style["margin_v"])
        paths = {}
        for label, kind in (("ass", "ass"), ("ass_simple_shaping", "ass_simple"), ("subtitles", "subtitles")):
            if kind == "ass":
                imgs, log = libass_batch(tools, ass, len(texts), scripts=[name], tag="sp1")
            elif kind == "ass_simple":
                imgs, log = libass_batch(tools, ass, len(texts), scripts=[name], shaping="simple", tag="sp2")
            else:
                imgs, log = libass_batch(tools, None, len(texts), scripts=[name], vf_filter="subtitles", srt_text=srt, srt_style=srt_style, tag="sp3")
            ious = {}
            for s, im in zip(strs, imgs):
                cov = im[..., 1].astype(np.float32) / 255.0
                reg = Registration(cov, s["text"], path, name)
                ious[s["id"]] = rnd(reg.iou_b, 3) if reg.ok else None
            vals = [v for v in ious.values() if v is not None]
            paths[label] = {"iou_by_string": ious, "iou_min": min(vals) if vals else None, "meets_%g" % thr["iou"]["min"]: bool(vals) and min(vals) >= thr["iou"]["min"],
                            "shaper_lines": sorted(set(l for l in log if l.startswith("Shaper")))}
            say_fn("  %-10s %-20s IoU min %s" % (name, label, paths[label]["iou_min"]))
        out["scripts"][name] = {"status": "MEASURED", "family": fam, "paths": paths}
    lim = thr["iou"]["min"]
    ind = {k: v for k, v in out["scripts"].items() if v.get("status") == "MEASURED"}
    table = "; ".join("%s: ass %.3f, subtitles %.3f" % (k, v["paths"]["ass"]["iou_min"], v["paths"]["subtitles"]["iou_min"]) for k, v in ind.items())
    ass_ok = all(v["paths"]["ass"]["iou_min"] >= lim for v in ind.values()) if ind else None
    sub_bad = [k for k, v in ind.items() if v["paths"]["subtitles"]["iou_min"] < lim]
    out["finding"] = ("On ffmpeg %s (IoU limit %g, lowest per script) %s. The `ass` filter on an ASS file %s the limit for every script with strings; the `subtitles` filter %s. "
                      "The `subtitles` and the forced-simple-shaping results match, which is what the pre-n9.0 simple-shaping behaviour (W-75) predicts." % (
                          tools.version, lim, table, "reaches" if ass_ok else "does NOT reach", ("falls below it for: " + ", ".join(sub_bad)) if sub_bad else "also reaches it here"))
    out["notes"] = ["The profile burns every script with the `ass` filter whatever the build (W-75): one path, tested, and it does not depend on the PC build's subtitles filter.",
                    "UNVERIFIED on Windows: the PC's ffmpeg build (9.0.2 expected) has never been run here."]
    return out


# ====================================================================================================== check a file
def check_file(tools, thr, prof, strings, path, scenarios, aspect=None, ass_path=None, sidecar_path=None, max_cues=12, use_diff=True, say_fn=say):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise Usage("the file %s does not exist" % os.path.basename(path))
    ass_path = ass_path or path + ".ass"
    sidecar_path = sidecar_path or path + ".phone.json"
    if not os.path.isfile(ass_path):
        raise Usage("%s is not beside the file: encode_phone.py writes OUTPUT.ass and OUTPUT.phone.json next to the phone file, and sim_share.sh copies them next to its output. "
                    "Without the caption file the tool cannot tell what was burned (use --ass FILE)" % os.path.basename(ass_path))
    side = EP.read_json(sidecar_path) if os.path.isfile(sidecar_path) else {}
    with open(ass_path, "rb") as f:
        ass_text = f.read().decode("utf-8-sig")
    h_before = EP.sha256_file(path)
    pr = EP.probe(tools.ffprobe, path)
    if pr["video"] is None:
        raise Usage("the file has no video stream")
    v = pr["video"]
    run = FileRun(tools, thr, path, ass_text, strings, scenarios, aspect=aspect, say_fn=say_fn, max_cues=max_cues, use_diff=use_diff, probe=pr)
    rep = run.run()
    rep["style"] = (side.get("style") or "file")
    rep["style_params"] = side.get("style_params")
    dur = float(pr["format"].get("duration") or 0)
    size_b = os.path.getsize(path)
    rep["file"] = {"name": os.path.basename(path), "width": int(v["width"]), "height": int(v["height"]), "codec": v.get("codec_name"), "profile": v.get("profile"), "level": v.get("level"),
                   "frames": v.get("nb_frames"), "duration_s": rnd(dur, 3), "average_mbps": rnd(size_b * 8.0 / dur / 1e6, 3) if dur else None, "sha256": h_before, "cues_looked_at": len(run.chosen),
                   "caption_free_frame": run.ref_idx is not None, "differenced": bool(run.diff), "free_text_lines": run.free_lines,
                   "sidecar": os.path.basename(sidecar_path) if side else None, "caption_file": os.path.basename(ass_path)}
    rep["burn_match"] = burn_match_report(run)
    # the phone-safe frame rules on the scene layout, when the encode kept it
    lay = side.get("layout") if side else None
    if lay and run.ref_idx is not None:
        strokes = [{"kind": s["kind"], "width_px": s["width_px"], "box": (s["box"]["x0"], s["box"]["y0"], s["box"]["x1"], s["box"]["y1"])} for s in lay.get("strokes", [])]
        ref_clean = up_to_1080(run.ref_frame(False))
        title, headline = lay.get("title"), lay.get("headline")
        for n in scenarios:
            sv = rep["scenarios"][n]
            geo = geometry(n, thr, aspect)
            after = run.ref_frame(bool(run.deg_for(geo)))
            lines = lines_check(tools, thr, ref_clean, strokes, n, aspect, frame_native=after) if strokes else []
            sv["lines"] = lines
            sv["frame_checks"] = []
            lim = thr["title"]["min_pct"]
            for label, box in (("title", title), ("headline", headline)):
                if not box:
                    continue
                b = (box["x0"], box["y0"], box["x1"], box["y1"])
                pct = title_ink_pct(ref_clean, b)
                if label == "title":
                    sv["frame_checks"].append(check("title_height_pct", NM if pct is None else (PASS if pct >= lim else FAIL), rnd(pct, 2) if pct else None, lim,
                                                    "ink height of the title line as a percentage of picture height (ROADMAP section 6: at least %g%%)" % lim))
                t = min(geo["smallest_grid_px_per_source_px"], after.shape[0] / float(H0))
                st = ink_stroke_p10(after, b, t, thr["stroke"]["percentile"])
                if st is None:
                    sv["frame_checks"].append(check("%s_stroke_px" % label, NM, detail="no ink found in the box"))
                else:
                    sl = thr["stroke"]["min_effective_px"]
                    sv["frame_checks"].append(check("%s_stroke_px" % label, PASS if st >= sl else FAIL, rnd(st, 2), sl,
                                                    "10th-percentile stroke width of the %s letters on the scenario's smallest grid (%.3f of source)%s" % (
                                                        label, t, "; the headline is the first script with strings and headline:true" if label == "headline" else "")))
            more = ["lines:%s%dpx" % (c["kind"], c["width_px"]) for c in lines if c["status"] == FAIL] + [c["id"] for c in sv["frame_checks"] if c["status"] == FAIL]
            if more:
                sv["verdict"] = FAIL
                sv["failed_checks"] = sv["failed_checks"] + more
    if EP.sha256_file(path) != h_before:
        raise Env("the input file changed while it was being checked (this must never happen)")
    rep["input_unchanged"] = True
    return rep


# ====================================================================================================== self-test (mechanisms only: no assertion about FontSize=23)
class Selftest:
    def __init__(self, tools, thr, prof, strings):
        self.tools, self.thr, self.prof, self.strings = tools, thr, prof, strings
        self.n_pass = self.n_fail = 0

    def ok(self, name, cond, detail=""):
        say("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
        if cond:
            self.n_pass += 1
        else:
            self.n_fail += 1
        return cond

    def style(self, **kw):
        st = dict(self.prof["caption"]["styles"][self.prof["caption"]["default_style"]])
        st.update(kw)
        return st

    def one(self, style, scenarios, scripts=("latin",), want_marks=False, strings=None, burn_text=None):
        run = StyleRun(self.tools, self.thr, style, strings or self.strings, scenarios, scripts_only=list(scripts) if scripts else None, want_marks=want_marks, style_name="selftest", burn_text=burn_text)
        return run.run()

    def margin_for_bottom(self, style, target_pct):
        """The integer MarginV that puts the bottom of a one-line Latin caption box at about target_pct of the picture height (the line's position is linear in MarginV: one unit is 3.75 px)."""
        probe = dict(style, margin_v=0, max_lines=1, max_chars_per_line=9)
        text = [s["text"] for s in self.strings["scripts"]["latin"]["strings"]][0]
        img = render_cues(self.tools, [[text]], probe, fill_only=False)[0]
        box = diff_box(img, np.full_like(img, 128), 40)
        unit = H0 / float(EP.read_json(EP.PROFILE_PATH)["caption"]["ass"]["play_res_y"])
        return int(round((box[3] - target_pct / 100.0 * H0) / unit)), box[3] / H0 * 100.0

    def run(self):
        thr, tools = self.thr, self.tools
        # --- arithmetic and primitives
        self.ok("fill_crop_20x9_is_10_percent", abs(fill_crop_pct(20, 9) - 10.0) < 0.01, "%.2f%% of picture height off the top and again off the bottom" % fill_crop_pct(20, 9))
        self.ok("fill_crop_19.5x9_is_about_9_percent", abs(fill_crop_pct(19.5, 9) - 8.97) < 0.05, "%.2f%%" % fill_crop_pct(19.5, 9))
        self.ok("arcminute_arithmetic", abs(arcmin(2.0, 35) - 19.64) < 0.05, "2.0 mm at 35 cm = %.2f arcmin" % arcmin(2.0, 35))
        self.ok("wcag_white_on_black_is_21", abs(wcag_ratio(1.0, 0.0) - 21.0) < 1e-9, "%.1f" % wcag_ratio(1.0, 0.0))
        line1, line4 = np.zeros((40, 80), np.float32), np.zeros((40, 80), np.float32)
        line1[20, :] = 1.0
        line4[18:22, :] = 1.0
        s1, s4 = stroke_stat(line1, 10)["p"], stroke_stat(line4, 10)["p"]
        self.ok("stroke_meter_tells_1px_from_4px", abs(s1 - 1.0) < 0.05 and abs(s4 - 4.0) < 0.05, "1 px line reads %.2f, 4 px line reads %.2f" % (s1, s4))
        self.ok("lint_flags_a_script_with_strings_and_no_marks", len(lint_strings({"scripts": {"x": {"strings": [{"id": "a", "text": "q"}]}}})) == 1 and not lint_strings(self.strings),
                "a block with strings and no marks[] is reported; the real file is clean")
        allow = [(s["text"], {"script": n, "entry": s}) for n, strs in script_blocks(self.strings) for s in strs]
        dev = [s["text"] for s in self.strings["scripts"]["devanagari"]["strings"] if s.get("kind") == "word"]
        self.ok("tile_line_accepts_allowlisted_strings_only", tile_line(dev[0] + " " + dev[1], allow) is not None and tile_line(dev[0] + " zz", allow) is None, "two allowlisted words tile; an extra word does not")

        # --- a known-tiny caption fails portrait (and the physical size is the reason)
        rep = self.one(self.style(font_size=8, max_chars_per_line=9, max_lines=1), ["portrait", "landscape"])
        c = {k["id"]: k for k in rep["scenarios"]["portrait"]["scripts"]["latin"]["checks"]}
        self.ok("known_tiny_caption_fails_portrait", rep["scenarios"]["portrait"]["verdict"] == FAIL and c["x_height_arcmin"]["status"] == FAIL,
                "FontSize 8: x-height %s arcmin at 35 cm in portrait (floor %g)" % (c["x_height_arcmin"].get("value"), thr["x_height"]["floor_arcmin"]))

        # --- a caption at least twice the threshold passes portrait
        fl = thr["x_height"]["floor_arcmin"]
        geo = geometry("portrait", thr)
        need_mm = 2.0 * (thr["distance_cm"]["verdict"] * 10.0) * math.tan(math.radians(2.05 * fl / 60.0 / 2.0))
        need_px = need_mm / (geo["picture_h_mm"] / H0)
        pth = EP.PROFILE_PATH
        lat_font = EP.font_for_script("latin", tools.lock)[1]
        fm = font_metrics(lat_font)
        em = need_px / (fm["x_height"] / float(fm["units_per_em"]))
        fs = int(math.ceil(em * (fm["win_ascent"] + fm["win_descent"]) / fm["units_per_em"] / (H0 / 288.0)))
        rep = self.one(self.style(font_size=fs, max_chars_per_line=9, max_lines=2), ["portrait", "landscape"])
        pv = rep["scenarios"]["portrait"]["scripts"]["latin"]
        c = {k["id"]: k for k in pv["checks"]}
        a35 = c["x_height_arcmin"].get("value") or 0
        self.ok("caption_at_twice_the_threshold_passes_portrait", rep["scenarios"]["portrait"]["verdict"] == PASS and a35 >= 2 * fl - 0.01,
                "FontSize %d: x-height %.1f arcmin at 35 cm in portrait, which is %.2f times the floor of %g; failed checks: %s" % (fs, a35, a35 / fl, fl, rep["scenarios"]["portrait"]["failed_checks"] or "none"))

        # --- a 1-px hairline fails 'shared'; a 4-px line (control) passes it
        fr = np.zeros((H0, W0, 3), np.uint8)
        yy = np.linspace(40, 90, H0).astype(np.uint8)[:, None, None]
        fr[:] = yy
        fr[300, 100:900] = 255
        fr[400:404, 100:900] = 255
        items = [{"kind": "hline", "width_px": 1, "box": (100, 300, 900, 301)}, {"kind": "hline", "width_px": 4, "box": (100, 400, 900, 404)}]
        res = lines_check(tools, thr, fr, items, "shared", gate_from=1)
        self.ok("one_pixel_hairline_fails_shared", res[0]["status"] == FAIL and res[1]["status"] == PASS,
                "1 px line: %s px on the share grid, keeps %s of its contrast -> %s; 4 px control: %s px, keeps %s -> %s" % (
                    res[0]["effective_px"], res[0]["retention"], res[0]["status"], res[1]["effective_px"], res[1]["retention"], res[1]["status"]))
        res_def = lines_check(tools, thr, fr, items, "shared")
        self.ok("thin_lines_are_reported_not_gated_at_the_default_gate", res_def[0]["status"] == INFO and res_def[1]["status"] == PASS,
                "at the default gate (%d px) the 1 px line is reported (%s), the 4 px line is gated (%s)" % (thr["stroke"]["must_survive_from_width_px"], res_def[0]["status"], res_def[1]["status"]))

        # --- position: a caption box ending at 95% fails fill_20x9, one ending at 85% passes
        st = self.style(max_lines=1, max_chars_per_line=9)
        out = {}
        for tgt in (95.0, 85.0):
            m, _b0 = self.margin_for_bottom(st, tgt)
            rep = self.one(dict(st, margin_v=m), ["fill_20x9"])
            lv = rep["scenarios"]["fill_20x9"]["scripts"]["latin"]
            c = {k["id"]: k for k in lv["checks"]}
            out[tgt] = (c["caption_bottom_pct"], lv["position"]["caption_bottom_pct"], m)
        self.ok("box_ending_at_95_percent_fails_fill_20x9", out[95.0][0]["status"] == FAIL and abs(out[95.0][1] - 95.0) <= 0.8,
                "MarginV %d puts the box bottom at %.1f%% (limit %s) -> %s" % (out[95.0][2], out[95.0][1], out[95.0][0].get("limit"), out[95.0][0]["status"]))
        self.ok("box_ending_at_85_percent_passes_fill_20x9", out[85.0][0]["status"] == PASS and abs(out[85.0][1] - 85.0) <= 0.8,
                "MarginV %d puts the box bottom at %.1f%% (limit %s) -> %s" % (out[85.0][2], out[85.0][1], out[85.0][0].get("limit"), out[85.0][0]["status"]))
        rep = self.one(dict(st, margin_v=out[95.0][2]), ["fill_20x9"], strings=self.strings)
        c = {k["id"]: k for k in rep["scenarios"]["fill_20x9"]["scripts"]["latin"]["checks"]}
        self.ok("the_cropped_caption_loses_ink", c["caption_visible_fraction"]["status"] == FAIL and c["caption_visible_fraction"]["value"] < 0.999,
                "at 95%% the share of the caption ink that stays on a filled 20:9 screen is %.3f" % c["caption_visible_fraction"]["value"])

        # --- mark survival: positive and negative control, on the Devanagari strings that have marks
        ph = self.style()
        pos = self.one(ph, ["landscape"], scripts=("devanagari",), want_marks=True)
        mchecks = {k["id"]: k for k in pos["scenarios"]["landscape"]["scripts"]["devanagari"]["checks"] if k["id"].startswith("marks:")}
        self.ok("marks_survive_in_the_correct_burn_in_(positive_control)", bool(mchecks) and all(k["status"] == PASS for k in mchecks.values()),
                ", ".join("%s %s" % (k["id"][6:], k["status"]) for k in mchecks.values()))
        burn = {}
        for s in self.strings["scripts"]["devanagari"]["strings"]:
            if s.get("marks"):
                drop = set()
                for m in s["marks"]:
                    drop |= set(cp_to_char(cc) for cc in m["codepoints"])
                burn[s["id"]] = "".join(ch for ch in s["text"] if ch not in drop)
        neg = self.one(ph, ["landscape"], scripts=("devanagari",), want_marks=True, burn_text=burn)
        nchecks = {k["id"]: k for k in neg["scenarios"]["landscape"]["scripts"]["devanagari"]["checks"] if k["id"].startswith("marks:")}
        self.ok("deleted_mark_codepoints_fail_mark_survival_(negative_control)", bool(nchecks) and all(k["status"] == FAIL for k in nchecks.values()),
                ", ".join("%s %s" % (k["id"][6:], k["status"]) for k in nchecks.values()))

        # --- a script with no strings is NOT TESTED, never PASS
        sx = json.loads(json.dumps(self.strings))
        sx["scripts"]["tamil"] = {"status": "pending_O-10", "strings": []}
        rep = self.one(self.style(), ["landscape"], scripts=("latin", "tamil"), strings=sx)
        t1, t2 = rep["iou"]["tamil"]["status"], rep["scenarios"]["landscape"]["scripts"]["tamil"]["status"]
        self.ok("script_without_strings_is_not_tested_never_pass", t1 == NT and t2 == NT and "tamil" in rep["scripts_not_tested"] and "tamil" not in rep["scripts_tested"],
                "IoU status %s, scenario status %s, listed as not tested: %s" % (t1, t2, "tamil" in rep["scripts_not_tested"]))
        return self.n_fail


# ====================================================================================================== command line
def build_parser():
    p = argparse.ArgumentParser(prog="phone_check.py", description="Legibility, shaping and fill-crop checks for the phone file (WP-08, D-27).", add_help=True)
    p.add_argument("file", nargs="?", help="a phone file made by encode_phone.py (with OUTPUT.ass and OUTPUT.phone.json beside it)")
    p.add_argument("--scenario", action="append", default=[], help="portrait, landscape, small_portrait, shared, fill_20x9 (repeatable; default all five)")
    p.add_argument("--aspect", default=None, help="screen aspect for fill_20x9, W:H (default 20:9; 19.5:9 crops about 9%%)")
    p.add_argument("--style", default=None, help="check a caption STYLE of profile.json for every script in test_strings.json (no file)")
    p.add_argument("--selftest", action="store_true", help="mechanisms only; exit 1 if one does not work")
    p.add_argument("--finding-fs23", action="store_true", help="write the FontSize=23 verdict per scenario as a finding (exit 0 either way); needs --out")
    p.add_argument("--candidates", action="store_true", help="measure the candidate FontSizes and say which one the rule picks")
    p.add_argument("--shaping-paths", action="store_true", help="the ass filter against the subtitles filter, per script (IoU against Pillow-raqm)")
    p.add_argument("--write-row", default=None, metavar="OUT", help="write PHONE-ROW.md from the evidence folder (--evidence)")
    p.add_argument("--evidence", default=None, help="evidence folder for --write-row (default build/evidence/wp08)")
    p.add_argument("--out", default=None, help="output file for --finding-fs23, --candidates, --shaping-paths")
    p.add_argument("--json", default=None, help="write the full report here (style and file modes)")
    p.add_argument("--scripts-json", default=None, help="write scripts_tested.json here (style mode)")
    p.add_argument("--ass", default=None, help="the caption file the burn-in used (default FILE.ass)")
    p.add_argument("--sidecar", default=None, help="the encode sidecar (default FILE.phone.json)")
    p.add_argument("--max-cues", type=int, default=12, help="how many cues of a file to look at (default 12)")
    p.add_argument("--no-diff", action="store_true", help="do not difference the file's frames; use the libass drawing of the burned captions")
    p.add_argument("--ffmpeg", default=None)
    p.add_argument("--thresholds", default=None)
    p.add_argument("--strings", default=None)
    p.add_argument("--profile", dest="profile_file", default=None)
    p.add_argument("--keep", action="store_true", help="keep the work folder")
    p.add_argument("--quiet", action="store_true")
    return p


def write_json(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    EP.write_json(path, obj)


def main(argv=None):
    a = build_parser().parse_args(argv)
    tools = None
    try:
        modes = [bool(a.selftest), bool(a.finding_fs23), bool(a.candidates), bool(a.shaping_paths), bool(a.write_row), bool(a.style), bool(a.file)]
        if sum(modes) != 1:
            raise Usage("give exactly one of: a FILE, --style NAME, --selftest, --finding-fs23, --candidates, --shaping-paths, --write-row OUT")
        thr = load_thresholds(a.thresholds)
        prof = EP.load_profile(a.profile_file)
        strings = read_json(a.strings or STRINGS)
        probs = lint_strings(strings)
        if probs:
            raise Usage("test_strings.json: " + "; ".join(probs))
        scen = a.scenario or list(thr["viewports"].keys())
        for n in scen:
            if n not in thr["viewports"]:
                raise Usage("unknown scenario '%s' (known: %s)" % (n, ", ".join(thr["viewports"])))
        aspect = parse_aspect(a.aspect) if a.aspect else None
        if a.write_row:
            return write_row(a, thr, prof)
        tools = Tools(a.ffmpeg, a.keep)
        say("phone_check: ffmpeg %s; libass drawing, Pillow %s with raqm %s; every figure marked (J) or UNVERIFIED in thresholds.json is a proposal or an assumption" % (
            tools.version, PIL.__version__, pil_features.version("raqm")))
        if a.selftest:
            n = Selftest(tools, thr, prof, strings).run()
            say("SELFTEST %s" % ("FAILED: %d mechanism(s) did not work" % n if n else "passed: every mechanism worked (no assertion about FontSize=23)"))
            return 1 if n else 0
        if a.finding_fs23:
            if not a.out:
                raise Usage("--finding-fs23 needs --out FILE")
            doc = finding_fs23(tools, thr, prof, strings, say_fn=say)
            write_json(a.out, doc)
            say("FINDING (not a pass condition): " + doc["summary"])
            for n, e in doc["scenarios"].items():
                say("  %-14s %-4s (%s)  failed: %s" % (n, e["verdict"], e["gate"], ", ".join(e["failed_checks"]) or "none"))
            say("wrote %s" % os.path.basename(a.out))
            return 0
        if a.candidates:
            doc = candidates_doc(tools, thr, prof, strings, say_fn=say)
            say("the rule picks FontSize %s; the profile says %s (%s)" % (doc["picked_font_size"], doc["profile_font_size"], "agree" if doc["agrees_with_profile"] else "DISAGREE"))
            if a.out:
                write_json(a.out, doc)
                say("wrote %s" % os.path.basename(a.out))
            return 0
        if a.shaping_paths:
            doc = shaping_paths_doc(tools, thr, prof, strings, say_fn=say)
            say("FINDING: " + doc["finding"])
            if a.out:
                write_json(a.out, doc)
                say("wrote %s" % os.path.basename(a.out))
            return 0
        if a.style:
            if a.style not in prof["caption"]["styles"]:
                raise Usage("caption style '%s' is not in profile.json (known: %s)" % (a.style, ", ".join(prof["caption"]["styles"])))
            rep = run_style(tools, thr, prof, a.style, strings, scen, aspect=aspect, say_fn=say if not a.quiet else None)
        else:
            rep = check_file(tools, thr, prof, strings, a.file, scen, aspect=aspect, ass_path=a.ass, sidecar_path=a.sidecar, max_cues=a.max_cues, use_diff=not a.no_diff, say_fn=say if not a.quiet else None)
            f = rep["file"]
            say("file %s: %dx%d %s, %.2f Mbps average, %s cues looked at, caption-free frame %s, differenced %s; input unchanged: %s" % (
                f["name"], f["width"], f["height"], f["codec"], f["average_mbps"] or 0, f["cues_looked_at"], "found" if f["caption_free_frame"] else "NOT found", f["differenced"], rep["input_unchanged"]))
            bm = rep["burn_match"]
            say("  burned captions against the libass drawing of the caption file: %s%s" % (bm["status"], (" (IoU min %s, limit %s)" % (bm["iou_min"], bm["limit"])) if bm.get("iou_min") is not None else " (%s)" % bm.get("reason", "")))
        print_report(rep, quiet=a.quiet)
        if a.json:
            write_json(a.json, rep)
            say("wrote %s" % os.path.basename(a.json))
        if a.scripts_json:
            write_json(a.scripts_json, scripts_tested_doc(rep, a.strings or STRINGS))
            say("wrote %s" % os.path.basename(a.scripts_json))
        rc = exit_code(rep)
        blocking = [n for n, sv in rep["scenarios"].items() if sv["verdict"] == FAIL and sv["gate"] == "blocking"]
        advisory = [n for n, sv in rep["scenarios"].items() if sv["verdict"] == FAIL and sv["gate"] != "blocking"]
        say("RESULT: %s%s%s" % ("blocking scenarios failed: " + ", ".join(blocking) if blocking else "no blocking scenario failed",
                                ("; advisory scenarios failed (listed above, not gated): " + ", ".join(advisory)) if advisory else "",
                                "; a shaping or burn-match check failed" if (rc and not blocking) else ""))
        return rc
    except Usage as e:
        say("USAGE/INPUT PROBLEM: %s" % e)
        return 2
    except Env as e:
        say("ENVIRONMENT PROBLEM: %s" % e)
        return 3
    finally:
        if tools:
            tools.close()


def register_phone_values():
    """The PH2 cap (Mb/s) and the phone caption line length that DECISIONS.md states in W-63 and W-18, read the way tests/integration reads them; {} when a row is missing or
    no longer has the shape. Used only to word PHONE-ROW.md truthfully: the register wins, so the row says "(inside W-63's 4)" while the register says 4 and "(W-63)" once the
    register states the profile's own figure (gate review r1, nudge 2). Reads DECISIONS.md and nothing else."""
    out = {}
    try:
        with open(os.path.join(ROOT, "DECISIONS.md"), "r", encoding="utf-8-sig") as fh:
            text = fh.read()
    except OSError:
        return out
    w63 = re.search(r"^\| W-63 \|.*$", text, re.M)
    w18 = re.search(r"^\| W-18 \|.*$", text, re.M)
    if w63:
        m = re.search(r"PH2, the small copy:\*\*\s*1280x720, CRF \d+, ([0-9.]+) Mb/s cap", w63.group(0))
        if m:
            out["ph2_cap_mbps"] = float(m.group(1))
    if w18:
        m = re.search(r"phone file carries its own caption setting: `FontSize=\d+`, `MarginV` \d+, two lines, at most (\d+) characters", w18.group(0))
        if m:
            out["max_chars"] = int(m.group(1))
    return out


def write_row(a, thr, prof):
    """PHONE-ROW.md: the settings card's Phone row and the language note, with the measured numbers, from the evidence files (so that the text and the evidence cannot disagree)."""
    ev = a.evidence or os.path.join(ROOT, "build", "evidence", "wp08")
    files = {"style": "phone_style.json", "scripts": "scripts_tested.json", "fs23": "finding_fontsize23.json", "cand": "caption_candidates.json",
             "fill": "fill_20x9_phone.json", "venue": "fill_20x9_venue_margin.json"}
    d = {}
    for k, name in files.items():
        p = os.path.join(ev, name)
        if not os.path.isfile(p):
            raise Usage("--write-row needs %s in the evidence folder (run build/evidence/wp08 steps of tests/phone/run_tests.sh --all first)" % name)
        d[k] = EP.read_json(p)
    st = prof["caption"]["styles"][prof["caption"]["default_style"]]
    vn = prof["caption"]["styles"]["venue_fs23"]
    lat = d["style"]["scenarios"]["landscape"]["scripts"]["latin"]
    dev = d["style"]["scenarios"]["landscape"]["scripts"].get("devanagari") or {}
    fl = d["fill"]["scenarios"]["fill_20x9"]["scripts"]
    fv = d["venue"]["scenarios"]["fill_20x9"]["scripts"]
    f23 = d["fs23"]["scenarios"]
    pos = thr["position"]
    date = d["scripts"]["date_utc"]
    ver = d["style"].get("ffmpeg")
    bottoms = [v["position"]["caption_bottom_pct"] for v in fl.values() if v.get("position")]
    tops = [v["position"]["caption_top_pct"] for v in fl.values() if v.get("position")]
    vbottoms = [v["position"]["caption_bottom_pct"] for v in fv.values() if v.get("position")]
    vlost = max(100.0 * (1.0 - v["position"]["visible_fraction"]) for v in fv.values() if v.get("position"))
    verdict_fill = d["fill"]["scenarios"]["fill_20x9"]["verdict"]
    verdict_venue = d["venue"]["scenarios"]["fill_20x9"]["verdict"]
    shared = d["style"]["scenarios"]["shared"]["verdict"]
    port = d["style"]["scenarios"]["portrait"]
    lat_port = port["scripts"]["latin"]["sizes"]["x_height_arcmin_35cm"]
    cand = {r["font_size"]: r for r in d["cand"]["rows"]}
    f23l = f23["landscape"]["scripts"]["latin"]
    f23f = f23["fill_20x9"]["scripts"]["latin"]
    reg = register_phone_values()
    prof_cap = float(prof["chains"]["phone_720_share"]["bitrate_cap_mbps"]) if "bitrate_cap_mbps" in prof["chains"]["phone_720_share"] else None
    if prof_cap is None:
        m_cap = re.search(r"-maxrate\W+(\d+)(k|M)", " ".join(prof["chains"]["phone_720_share"]["video_args"]))
        prof_cap = (int(m_cap.group(1)) / 1000.0) if (m_cap and m_cap.group(2) == "k") else float(m_cap.group(1))
    if reg.get("ph2_cap_mbps") == prof_cap:
        cap_words = "a %g Mb/s cap (W-63)" % prof_cap
    elif reg.get("ph2_cap_mbps"):
        cap_words = "about %g Mb/s cap (inside W-63's %g)" % (prof_cap, reg["ph2_cap_mbps"])
    else:
        cap_words = "about %g Mb/s cap (W-63 gives its own figure)" % prof_cap
    if reg.get("max_chars") == st["max_chars_per_line"]:
        len_words = "W-18; %d fits the 90%% box in both scripts tested; the venue file keeps its own guide of 42" % st["max_chars_per_line"]
    elif reg.get("max_chars"):
        len_words = "W-18 says %d; %d is the stricter figure of the build plan and fits the 90%% box in both scripts tested" % (reg["max_chars"], st["max_chars_per_line"])
    else:
        len_words = "W-18 gives its own figure; %d is the build plan's and fits the 90%% box in both scripts tested" % st["max_chars_per_line"]
    cols = []
    cols.append("**Phone** (D-27)")
    cols.append("The film and any keepsake must play beautifully on a phone: readable words, a frame that survives phone cropping, and a file that survives being shared.")
    cols.append(
        "**Proposed (J), measured on synthetic test material:** two phone files from the one locked timeline, never a second edit (W-63). **PH1**, the phone master: 1920x1080, 24 fps, H.264 High 4.1, "
        "yuv420p, BT.709 tags on the master before the burn-in, CRF 20 with an 8 Mb/s cap, AAC-LC 192 kbps 48 kHz stereo, `+faststart`. **PH2**, the small copy for a phone with little free storage: "
        "1280x720, CRF 22, %s, level 3.1, captions burned on the 1080 frame before the downscale. Both SDR only (no HDR), -16 LUFS integrated and -1 dBTP on the "
        "final MP4. **Phone captions** are burned in at their own setting, measured and not guessed: `FontSize=%g`, `MarginV` %g, white with a black outline, two lines, at most %d characters "
        "a line (%s), the block from **%.1f%% to %.1f%% of the picture height**; the letters "
        "(Latin x-height %.2f%%, Devanagari base letter %.2f%% of the picture height) clear the 3.2%% floor of W-63. **Filled to the screen** (a 20:9 phone set to fill crops about 10%% off the top "
        "and the bottom): the box ends at **%.1f%%** against a limit of %.1f%%, so the whole bottom line stays; verdict **%s**. Moved to a phone by cable or a private link only." % (
            cap_words, st["font_size"], st["margin_v"], st["max_chars_per_line"], len_words, min(tops), max(bottoms), lat["sizes"]["x_height_pct"], (dev.get("sizes") or {}).get("x_height_pct", float("nan")),
            max(bottoms), pos["caption_bottom_max_pct"], verdict_fill))
    cols.append("D-27, W-63, W-18, W-19")
    cols.append("The ffprobe lines above on each phone file (PH1 reads 1920x1080; PH2 reads 1280x720, level 31); `python3 -I pipeline/phone/phone_check.py FILE.mp4` (five views: upright, "
                "sideways, small phone, after sharing, filled to the screen) and `python3 -I pipeline/phone/phone_check.py FILE.mp4 --scenario fill_20x9` (prints where the caption's bottom edge "
                "sits as a percentage of the picture height); then your own phone (`pipeline/phone/PHONE-TEST.md`, seven questions). UNVERIFIED until you try it.")
    cols.append("The caption numbers can only move by the phone test, not by taste (Gujarati is sized by the height of its letter KA, not by `FontSize`). A smaller size loses the letter-height floor "
                "(FontSize 26 reads %.2f%%, FontSize 24 %.2f%%); a larger one moves the block up (FontSize 32 starts at %.1f%%). The venue caption (`FontSize=%g`, `MarginV` %g) ends at %.1f%%, so when a phone fills "
                "the screen up to %.0f%% of its ink falls off the bottom (a caption burned at the venue's 5%% margin would lose most of its lower line). PH1 goes to her phone by cable if 1 GB is free there, else PH2 (O-54). Sharing by a family chat or a cloud photo library is not allowed "
                "(D-02, D-15)." % (cand[26]["latin_x_height_pct"], cand[24]["latin_x_height_pct"], cand[32]["block_top_pct"], vn["font_size"], vn["margin_v"], max(vbottoms), vlost))
    row = "| " + " | ".join(cols) + " |"
    lines = []
    lines.append("# Phone row of the settings card (WP-08, measured %s)" % date)
    lines.append("")
    lines.append("*Written by `python3 -I pipeline/phone/phone_check.py --write-row` from the evidence files in `build/evidence/wp08/`, so the text and the measurements cannot disagree. Every figure "
                 "is measured on synthetic, style-neutral test material (ffmpeg %s, Noto Sans and Noto Sans Devanagari) and stays a proposal (J) until the maker has looked at a real phone "
                 "(`PHONE-TEST.md`). Nothing here is signed by an agent. UNVERIFIED: real phones, a messenger's own encoder, how a given player implements fill, the arcminute limits, and "
                 "everything on the maker's Windows PC.*" % ver)
    lines.append("")
    lines.append("## 1. The row (the orchestrator pastes this over the Phone row of `ops/SETTINGS-CARD.md`)")
    lines.append("")
    lines.append("| Row | In plain words | Proposed value | Register | Command that proves it | If you change it |")
    lines.append("|---|---|---|---|---|---|")
    lines.append(row)
    lines.append("")
    lines.append("## 2. Caption size and position, measured")
    lines.append("")
    lines.append("| What | Value | Where it comes from |")
    lines.append("|---|---|---|")
    lines.append("| Caption size | `FontSize=%g`, `MarginV` %g, outline %g (about %.1f px at 1080p), at most %d characters a line, two lines | `profile.json` (J); the rule in `caption_candidates.json` picks %s |" % (
        st["font_size"], st["margin_v"], st["outline"], st["outline"] * H0 / float(prof["caption"]["ass"]["play_res_y"]), st["max_chars_per_line"], d["cand"]["picked_font_size"]))
    lines.append("| Letter height, Latin x-height | %.2f%% of the picture height (%.1f px at 1080p); %.1f arcmin at 35 cm sideways, %.1f at 40 cm; floor 3.2%% / 18 arcmin, target 3.8%% / 21 | `phone_style.json`, landscape (arcminute limits UNVERIFIED) |" % (
        lat["sizes"]["x_height_pct"], lat["sizes"]["x_height_px_1080"], lat["sizes"]["x_height_arcmin_35cm"], lat["sizes"]["x_height_arcmin_40cm"]))
    if dev.get("sizes"):
        lines.append("| Letter height, Devanagari base letter | %.2f%% of the picture height (%.1f px); %.1f arcmin at 35 cm sideways | `phone_style.json`; an analogue of the x-height, not the same thing |" % (
            dev["sizes"]["x_height_pct"], dev["sizes"]["x_height_px_1080"], dev["sizes"]["x_height_arcmin_35cm"]))
    lines.append("| Letter height at arm's length (50 cm) | Latin x-height reads %.1f arcmin sideways, %s the 18 arcmin floor; filled to the screen it reads %.1f | `phone_style.json` (INFO only; the maker's phone test, question 3, is the measurement) |" % (
        lat["sizes"]["x_height_arcmin_50cm"], "at or above" if lat["sizes"]["x_height_arcmin_50cm"] >= thr["x_height"]["floor_arcmin"] else "below",
        d["style"]["scenarios"]["fill_20x9"]["scripts"]["latin"]["sizes"]["x_height_arcmin_50cm"]))
    lines.append("| Caption position (picture height from the top) | block **%.1f%% to %.1f%%**; the bottom edge must be at the %g%% line or higher up the picture (a smaller percentage) | `fill_20x9_phone.json` (the encoded test file, differenced against a caption-free frame) |" % (
        min(tops), max(bottoms), pos["caption_bottom_max_pct"]))
    lines.append("| Filled to a 20:9 screen (`fill_20x9`) | **%s**: the box ends at %.1f%% against the limit of %.1f%% (the 90%% crop line minus a 2-point margin); the whole bottom line stays | `fill_20x9_phone.json` |" % (
        verdict_fill, max(bottoms), d["fill"]["scenarios"]["fill_20x9"]["scripts"]["latin"]["position"]["bottom_limit_pct"]))
    lines.append("| The same file burned with the venue size and margin | **%s**: the box ends at %.1f%% and %s | `fill_20x9_venue_margin.json` |" % (
        verdict_venue, max(vbottoms), ("up to %.0f%% of the caption's ink falls off the bottom when the phone fills the screen" % vlost) if verdict_venue == FAIL else "stays whole"))
    lines.append("| After sharing (480p, about 1 Mbps) | **%s** (all blocking checks, marks included) | `phone_style.json` scenario `shared`; the encoded file through `sim_share.sh` is in `shared_phone_check.json` |" % shared)
    lines.append("| Upright in a chat or player (`portrait`) | letters read about %.0f arcmin at 35 cm, below the 18 arcmin floor: **degraded by design**; the hand-over says \"turn it sideways\" | `phone_style.json`, an advisory view (W-18: the phone file is made for landscape) |" % lat_port)
    lines.append("")
    lines.append("## 3. FontSize=23 on a phone (a finding, not a pass condition)")
    lines.append("")
    lines.append("The venue caption (`FontSize=%g`, `MarginV` %g, Noto Sans) measured the same way (`finding_fontsize23.json`): sideways the Latin x-height is %.2f%% of the picture height "
                 "(%.2f arcmin at 35 cm; floor 3.2%% / 18); filled to the screen the box ends at %.1f%% for Latin and %s for Devanagari (limit %.1f%%). Scenario verdicts: %s. The venue size is "
                 "the venue's; the phone file carries its own." % (vn["font_size"], vn["margin_v"], f23l["sizes"]["x_height_pct"], f23l["sizes"]["x_height_arcmin_35cm"], f23f["position"]["caption_bottom_pct"],
                                                                   ("%.1f%%" % f23["fill_20x9"]["scripts"]["devanagari"]["position"]["caption_bottom_pct"]) if f23["fill_20x9"]["scripts"].get("devanagari", {}).get("position") else "n/a",
                                                                   f23f["position"]["bottom_limit_pct"], ", ".join("%s %s" % (n, f23[n]["verdict"]) for n in f23)))
    lines.append("")
    lines.append("## 4. Language and script note (the orchestrator pastes this line into the card's language note)")
    lines.append("")
    lines.append("`" + d["scripts"]["line"] + "`")
    lines.append("")
    lines.append("The shaping and mark-survival tests loop over every script in `pipeline/phone/test_strings.json` that has strings: today Latin and Devanagari (neutral, plain Sanskrit-derived words, "
                 "`checked_by_reader: false` until the maker confirms them). Her language is Gujarati (D-31) and it is **NOT TESTED**: adding it is the three small steps of the build plan (4.10): "
                 "one font entry in `libs.lock.json`, one reader-confirmed block with `marks[]` in `test_strings.json`, and a rerun; nothing else changes.")
    lines.append("")
    path = os.path.abspath(a.write_row)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    say("wrote %s" % os.path.basename(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
