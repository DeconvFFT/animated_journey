#!/usr/bin/env python3
"""phone_check.py: does the text on a phone-size screen still read? Legibility, shaping and fill-crop checks for the phone file. WP-08, decision D-27.

  python3 -I pipeline/phone/phone_check.py FILE.mp4 [--scenario NAME ...] [--aspect 19.5:9] [--json OUT.json]      check a phone file (needs its OUTPUT.phone.json and
                                                                                                                  OUTPUT.ass beside it, which encode_phone.py writes)
  python3 -I pipeline/phone/phone_check.py --style phone [--scenario NAME ...] [--json OUT.json]                    check a caption STYLE for every script in test_strings.json
  python3 -I pipeline/phone/phone_check.py --selftest                                                               mechanisms only (a tiny caption fails, a large one passes, ...)
  python3 -I pipeline/phone/phone_check.py --finding-fs23 --out build/evidence/wp08/finding_fontsize23.json         write the FontSize=23 verdict per scenario as a FINDING (exit 0 either way)
  python3 -I pipeline/phone/phone_check.py --candidates [--out FILE]                                                measure the candidate FontSizes and say which one the rule picks
  python3 -I pipeline/phone/phone_check.py --shaping-paths [--out FILE]                                             the `ass` filter against the `subtitles` filter, per script (IoU against Pillow-raqm)
  Options: --scripts-json FILE (write scripts_tested.json)  --ffmpeg PATH  --thresholds FILE  --strings FILE  --profile FILE  --keep (keep the work folder)  --quiet

SCENARIOS (thresholds.json viewports; every figure is an assumption about typical phones and UNVERIFIED)
  portrait        held upright, 390 CSS px wide, device pixel ratio 3, the 16:9 picture full width (advisory: upright is degraded by design)
  landscape       the same phone sideways, 844 CSS px wide, picture fitted to the height (the intended view)
  small_portrait  360 CSS px wide at ratio 2 (a 720p-class phone) upright (advisory)
  shared          the file re-encoded to 480p at about 1 Mbps with veryfast (a messenger), viewed sideways; a file that is already 480p or smaller is used as it is
  fill_20x9       16:9 filled to a 20:9 screen: scaled to the screen width, so about 10% of the picture height is cropped at the top and at the bottom (--aspect 19.5:9: about 9%)

WHAT IS MEASURED, per scenario (a metric names its threshold in thresholds.json, with its source and (J) where it is a proposal)
  x-height and cap height of the caption face: pixels (physical device pixels), millimetres and arcminutes at the 35 cm design distance (and at 40 cm), and as a percentage of
    picture height; minimum stroke width (the 10th percentile of local stroke width, so hairlines and the Devanagari headline show) in pixels after the scenario's smallest grid;
    WCAG contrast of the fill against the outline; caption inside the 90% box; title at least 5% of picture height; caption POSITION: the bottom and top of the caption box
    as a percentage of picture height against the scenario's crop line (fill_20x9: bottom at or above 88%), and the fraction of the caption ink that stays on screen.
  Per script that has strings in test_strings.json (the others are reported NOT TESTED, never PASS): the burned line is rendered by libass in the style under test; the
    mark-survival check reads that script's marks[] (codepoints and kind) from the same file, derives each mark's zone by differential rendering with and without the mark's
    codepoints at 8x with Pillow-raqm (no coordinate is stored or assumed) and requires at least 2 px of ink, matching the reference, in that zone after the downscale to each
    scenario; and the libass-versus-Pillow-raqm IoU of the ink must reach 0.9, else the script gets a shaping finding.

WHAT IT NEVER DOES. It never edits the file it checks, never uploads anything, uses no network, prints base file names only (no folder, user or host names), writes only what
--json / --out / --scripts-json name, and keeps its scratch in a temporary folder that it removes. numpy and Pillow (with raqm) and ffmpeg are required.
EXIT  0 no blocking check failed (an advisory scenario may still FAIL: it is listed); 1 a blocking check failed; 2 bad usage or invalid input; 3 environment problem.
      --finding-fs23, --candidates, --shaping-paths exit 0 however the numbers come out (they write findings); --selftest exits 1 if a mechanism does not work.
"""
import argparse
import datetime
import importlib.util
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

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


# ====================================================================================================== Pillow-raqm reference, registration, IoU
def raqm_font(path, size):
    if not pil_features.check("raqm"):
        raise Env("Pillow was built without raqm; the IoU reference needs it")
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


LANG = {"latin": "en", "devanagari": "hi", "bengali": "bn", "gujarati": "gu", "tamil": "ta", "telugu": "te", "kannada": "kn", "malayalam": "ml"}


def raqm_render(text, font_path, px, script, canvas=None, pad=24):
    """Coverage (float32, 0..1) of the text drawn with Pillow-raqm at px pixels (an em size). The baseline sits at a fixed row, so two renderings of related strings
    (with and without a mark) line up when they share a canvas size."""
    font = raqm_font(font_path, px)
    asc, desc = font.getmetrics()
    lang = LANG.get(script, "en")
    if canvas is None:
        length = font.getlength(text, language=lang)
        canvas = (int(asc + desc + 2 * pad), int(length + 2 * pad + px))
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
    """A libass fill-coverage image of one line and the Pillow-raqm reference of the same text, registered at sub-pixel precision.
    fill: the libass coverage cropped to the line's ink box plus a margin (1x). full8: the reference at 8x on its own canvas (kept for zone derivation).
    After fit(): ref1 is the reference at 1x on the crop's grid, iou_b and iou_s the binary and soft IoU, and map8(a) puts any 8x canvas image (a zone) on the same grid."""

    def __init__(self, fill_full, text, font_path, script, margin=6, k=8):
        self.k, self.margin, self.text, self.font_path, self.script = k, margin, text, font_path, script
        bb = ink_bbox(fill_full, 0.5)
        self.ok = bb is not None
        if not self.ok:
            return
        x0, y0, x1, y1 = bb
        self.fx0, self.fy0 = max(0, x0 - margin), max(0, y0 - margin)
        self.fx1, self.fy1 = min(fill_full.shape[1], x1 + margin), min(fill_full.shape[0], y1 + margin)
        self.fill = fill_full[self.fy0:self.fy1, self.fx0:self.fx1]
        self.libass_ink = (x1 - x0, y1 - y0)
        r100 = raqm_render(text, font_path, 100, script)
        b100 = ink_bbox(r100, 0.5)
        h100 = b100[3] - b100[1]
        self.em_px = 100.0 * (y1 - y0) / float(h100)                    # the em size that gives libass's ink height
        self.full8 = raqm_render(text, font_path, round(self.em_px * k, 2), script)
        b8 = ink_bbox(self.full8, 0.5)
        self.ref_ink = ((b8[2] - b8[0]) / float(k), (b8[3] - b8[1]) / float(k))
        # origin (in canvas coordinates) that puts the reference ink's top-left on the libass ink's top-left
        self.ox = b8[0] - (x0 - self.fx0) * k
        self.oy = b8[1] - (y0 - self.fy0) * k
        h, w = self.fill.shape
        self.crop8 = window(self.full8, self.oy, self.ox, h * k, w * k)
        self.dx8 = self.dy8 = 0
        self.iou_b = self.iou_s = None
        self.ref1 = None

    def ref_at(self, dx8, dy8):
        return reduce8(shift2(self.crop8, dx8, dy8), self.k)

    def fit(self):
        if not self.ok:
            return self
        fb = self.fill > 0.5

        def score(dx8, dy8):
            return iou_binary(fb, self.ref_at(dx8, dy8) > 0.5)
        dx8, dy8, best = 0, 0, score(0, 0)
        for step in (8, 4, 2, 1):
            moved = True
            while moved:
                moved = False
                for ddx, ddy in ((step, 0), (-step, 0), (0, step), (0, -step)):
                    sc = score(dx8 + ddx, dy8 + ddy)
                    if sc > best + 1e-9:
                        best, dx8, dy8, moved = sc, dx8 + ddx, dy8 + ddy, True
        self.dx8, self.dy8 = dx8, dy8
        self.ref1 = self.ref_at(dx8, dy8)
        self.iou_b = best
        self.iou_s = iou_soft(self.fill, self.ref1)
        return self

    def to_grid(self, a8):
        """An image on the full8 canvas (an 8x zone mask, say) mapped to the 1x grid of the fill crop, with the fitted shift."""
        h, w = self.fill.shape
        return reduce8(shift2(window(a8, self.oy, self.ox, h * self.k, w * self.k), self.dx8, self.dy8), self.k)


# ---------------------------------------------------------------------------------------------------- mark zones (differential rendering)
def _max_filter(mask, size):
    im = Image.fromarray((mask.astype(np.uint8)) * 255)
    return np.asarray(im.filter(ImageFilter.MaxFilter(size))) > 0


def _min_filter(mask, size):
    im = Image.fromarray((mask.astype(np.uint8)) * 255)
    return np.asarray(im.filter(ImageFilter.MinFilter(size))) > 0


def _best_shift(fm, sm, avoid=24, limit=None):
    """The horizontal shift of sm (other than near 0) that overlaps fm most, by cross-correlation along x summed over rows."""
    h, w = fm.shape
    n = 1
    while n < 2 * w:
        n *= 2
    fa = np.fft.rfft(fm.astype(np.float32), n=n, axis=1)
    sa = np.fft.rfft(sm.astype(np.float32), n=n, axis=1)
    corr = np.fft.irfft((fa * np.conj(sa)).sum(axis=0), n=n)
    lim = limit or w // 2
    best, bdx = -1.0, 0
    for dx in range(-lim, lim + 1):
        if abs(dx) < avoid:
            continue
        v = corr[dx % n]
        if v > best:
            best, bdx = v, dx
    return bdx


def derive_zone(full8, strip8, k=8):
    """The ink the mark adds, found by differential rendering at 8x: ink of the full string that the string without the mark does not explain, after allowing the part of the
    string that sits to the right of the mark to have moved sideways. Returns a boolean mask on the full8 canvas (empty if the mark adds nothing)."""
    fm, sm = full8 >= 0.5, strip8 >= 0.5
    r = 3
    exp0 = _max_filter(sm, 2 * r + 1)
    un0 = fm & ~exp0
    explained = exp0
    dx = _best_shift(fm & un0 | fm, sm)
    if dx != 0:
        shifted = shift2(sm.astype(np.uint8), dx, 0) > 0
        exp1 = _max_filter(shifted, 2 * r + 1)
        un01 = un0 & ~exp1
        if (int(un0.sum()) - int(un01.sum())) >= 0.03 * max(1, int(fm.sum())):
            explained = exp0 | exp1
    zone = fm & ~explained
    zone = _max_filter(_min_filter(zone, 3), 3) & zone          # drop one-pixel fringes
    return zone
