#!/usr/bin/env python3
"""kb_scale.py: the Ken Burns scale maths for FilmCraft (research/craft-motion.md R2 and R8). Standard library only. No file is read or written.

FilmCraft's Motion Scale is a percentage of the source's NATIVE pixels when scale_to_frame is false (100 = one source pixel per frame pixel).
For a source of w x h pixels in a sequence of W x H pixels:

    fit   = min(W / w, H / h) * 100     the whole picture is visible (bars may show)
    cover = max(W / w, H / h) * 100     the frame is filled (the picture is cropped)

    3600 x 2400 into 1080p:   fit 45.0     cover 53.3 (53.34 in two decimals, see below)
    2880 x 1620 into 1080p:   fit 66.67    cover 66.67   (the conformed still: both agree)

A Ken Burns move is cover x 1.00 -> cover x 1.12..1.25 with a slow position drift (R2 step 1). The picture's centre sits at the
Position value in sequence pixels (960,540 is the middle of 1080p). UNVERIFIED against a real FilmCraft: the first and last frame of a
gridded still must be measured (WP-07 T2).

ROUNDING  fit is rounded to the nearest 0.01. cover is rounded UP to the next 0.01, so that the rounded number never shows a sliver of
black at the frame edge (66.6667 becomes 66.67; 53.3333 becomes 53.34). All arithmetic is exact (fractions) until the last step.

USAGE
  python3 -I pipeline/roundtrip/kb_scale.py 3600 2400                       fit and cover into 1920x1080
  python3 -I pipeline/roundtrip/kb_scale.py 2880 1620 --seq 1920x1080 --zoom 1.2 --json
  python3 -I pipeline/roundtrip/kb_scale.py --selftest                      the unit tests (45.0, 53.3, 66.67 and more)

EXIT CODES  0 ok   1 a self-test failed   2 bad usage
"""
import argparse
import json
import math
import sys
from fractions import Fraction

sys.dont_write_bytecode = True


def _ratios(src_w, src_h, seq_w, seq_h):
    if min(src_w, src_h, seq_w, seq_h) <= 0:
        raise ValueError("sizes must be positive whole numbers")
    return Fraction(seq_w, src_w), Fraction(seq_h, src_h)


def fit_scale(src_w, src_h, seq_w=1920, seq_h=1080):
    """Percent that shows the whole picture, rounded to the nearest 0.01."""
    r = min(_ratios(src_w, src_h, seq_w, seq_h)) * 100
    return float(round(r * 100) / 100)


def cover_scale(src_w, src_h, seq_w=1920, seq_h=1080):
    """Percent that fills the frame, rounded UP to the next 0.01."""
    r = max(_ratios(src_w, src_h, seq_w, seq_h)) * 100
    return float(Fraction(math.ceil(r * 100), 100))


def scale_for(mode, src_w, src_h, seq_w=1920, seq_h=1080):
    if mode == "fit":
        return fit_scale(src_w, src_h, seq_w, seq_h)
    if mode == "cover":
        return cover_scale(src_w, src_h, seq_w, seq_h)
    raise ValueError("mode must be 'fit' or 'cover', not %r" % (mode,))


def edge_margin_px(src_w, src_h, seq_w, seq_h, scale_pct, pos_x, pos_y):
    """Smallest distance in sequence pixels between the picture's edge and the frame's edge, over the four sides.
    Zero or more means the frame is covered everywhere; negative means that many pixels of black show on the worst side.
    The picture is drawn at its native size times scale, with its centre at (pos_x, pos_y)."""
    dw = src_w * scale_pct / 100.0
    dh = src_h * scale_pct / 100.0
    return min((pos_x - dw / 2.0) * -1.0,            # left edge must be at or left of 0
               (pos_x + dw / 2.0) - seq_w,           # right edge must be at or right of the frame's right edge
               (pos_y - dh / 2.0) * -1.0,
               (pos_y + dh / 2.0) - seq_h)


def move_is_edge_safe(src_w, src_h, seq_w, seq_h, keys, tol_px=0.5):
    """keys = [(scale_pct, pos_x, pos_y), ...]. Linear interpolation of both between keys cannot create a gap that neither key has
    (the picture's edge position is linear in time), so checking the keys is enough for a Linear move. Returns (ok, worst_margin_px)."""
    worst = min(edge_margin_px(src_w, src_h, seq_w, seq_h, s, x, y) for s, x, y in keys)
    return worst >= -tol_px, worst


# ------------------------------------------------------------------------------------------------------------- self-test
def selftest():
    fails = []

    def eq(name, got, want):
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))
        return got == want

    eq("fit 3600x2400", round(fit_scale(3600, 2400), 1), 45.0)
    eq("cover 3600x2400 (one decimal)", round(cover_scale(3600, 2400), 1), 53.3)
    eq("cover 3600x2400 (two decimals, rounded up)", cover_scale(3600, 2400), 53.34)
    eq("fit 2880x1620", fit_scale(2880, 1620), 66.67)
    eq("cover 2880x1620", cover_scale(2880, 1620), 66.67)
    eq("fit equals cover for a 16:9 source", fit_scale(2880, 1620), cover_scale(2880, 1620))
    eq("native 1080p is 100", fit_scale(1920, 1080), 100.0)
    eq("native 1080p cover is 100", cover_scale(1920, 1080), 100.0)
    eq("a 4K source fits at 50", fit_scale(3840, 2160), 50.0)
    eq("portrait 2400x3600 fits at 30", fit_scale(2400, 3600), 30.0)
    eq("portrait 2400x3600 covers at 80", cover_scale(2400, 3600), 80.0)
    eq("scale_for fit", scale_for("fit", 3600, 2400), 45.0)
    # cover never leaves a gap: the rounded number is at least the exact one
    for w, h in ((3600, 2400), (2880, 1620), (4000, 3000), (1234, 987), (2999, 1999)):
        ex = float(max(Fraction(1920, w), Fraction(1080, h)) * 100)
        if cover_scale(w, h) < ex:
            fails.append("cover %dx%d rounded below the exact value" % (w, h))
        if cover_scale(w, h) - ex >= 0.01:
            fails.append("cover %dx%d rounded up by a whole 0.01 or more" % (w, h))
    # edge safety
    ok, worst = move_is_edge_safe(2880, 1620, 1920, 1080, [(66.67, 960, 540), (80.0, 930, 520)])
    eq("the R3 template move keeps the frame covered", ok, True)
    ok, worst = move_is_edge_safe(2880, 1620, 1920, 1080, [(66.67, 960, 540), (66.67, 900, 540)])
    eq("a sideways drift at 66.67 shows black", ok, False)
    ok, worst = move_is_edge_safe(3600, 2400, 1920, 1080, [(45.0, 960, 540)])
    eq("fit on a 3:2 source leaves bars", ok, False)
    for m in fails:
        print("FAIL", m)
    if not fails:
        print("PASS kb_scale selftest: fit 45.0, cover 53.3 (53.34), 2880x1620 66.67 for both, rounding, edge safety")
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ken Burns scale maths for FilmCraft (fit and cover percentages).")
    ap.add_argument("width", nargs="?", type=int)
    ap.add_argument("height", nargs="?", type=int)
    ap.add_argument("--seq", default="1920x1080", help="sequence size, default 1920x1080")
    ap.add_argument("--zoom", type=float, default=1.2, help="end scale = cover x ZOOM (default 1.2; the plan uses 1.12 to 1.25)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if a.selftest:
        return selftest()
    if not a.width or not a.height:
        print("kb_scale: give the source width and height, or --selftest", file=sys.stderr)
        return 2
    try:
        sw, sh = (int(p) for p in a.seq.lower().split("x"))
        fit, cover = fit_scale(a.width, a.height, sw, sh), cover_scale(a.width, a.height, sw, sh)
    except ValueError as e:
        print("kb_scale: %s" % e, file=sys.stderr)
        return 2
    end = round(cover * a.zoom, 2)
    out = {"source": [a.width, a.height], "sequence": [sw, sh], "fit": fit, "cover": cover, "fit_1dp": round(fit, 1), "cover_1dp": round(cover, 1),
           "kenburns_start": cover, "kenburns_end": end, "zoom": a.zoom}
    if a.json:
        print(json.dumps(out, sort_keys=True))
    else:
        print("source %dx%d into %dx%d" % (a.width, a.height, sw, sh))
        print("  fit   %.2f   (%.1f to one decimal)" % (fit, fit))
        print("  cover %.2f   (%.1f to one decimal; rounded up so the frame stays covered)" % (cover, cover))
        print("  Ken Burns %.2f -> %.2f (x%.2f)" % (cover, end, a.zoom))
    return 0


if __name__ == "__main__":
    sys.exit(main())
