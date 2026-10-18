#!/usr/bin/env python3
"""Two-point eye alignment (similarity transform) for same-pose pairs.

Method after PyImageSearch (2017-05-22): turn the photo so the eye line is level,
scale it so the eyes sit a fixed distance apart, and move the eye midpoint to a
fixed target. Needs Pillow and numpy only. Research note T1, tested 2026-10-18.

"Left" and "right" mean the picture's left and right, not the subject's.

Usage:
  python align_eyes.py --image photo.jpg --left-eye 812,640 --right-eye 1180,652 --out aligned.png
  python align_eyes.py --selftest
  python align_eyes.py --make-test-image synthetic_face.png
"""
import argparse
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

TARGET_LEFT = (0.35, 0.40)   # fraction of (width, height); tested setting in research note [64]
TARGET_RIGHT = (0.65, 0.40)
TEST_LEFT_EYE = (300.0, 400.0)   # eye centres in the synthetic test face (pixels)
TEST_RIGHT_EYE = (500.0, 400.0)


def similarity_for_eyes(left_eye, right_eye, out_size, target_left, target_right):
    """Return (R, t) mapping source pixels to output pixels: out = R @ src + t."""
    W, H = out_size
    tl = np.array([target_left[0] * W, target_left[1] * H], float)
    tr = np.array([target_right[0] * W, target_right[1] * H], float)
    lx, ly = left_eye
    rx, ry = right_eye
    sv = np.array([rx - lx, ry - ly], float)
    dv = tr - tl
    scale = np.linalg.norm(dv) / np.linalg.norm(sv)
    ang = math.atan2(dv[1], dv[0]) - math.atan2(sv[1], sv[0])
    c, s = math.cos(ang) * scale, math.sin(ang) * scale
    R = np.array([[c, -s], [s, c]])
    mid = np.array([(lx + rx) / 2, (ly + ry) / 2])
    t = (tl + tr) / 2 - R @ mid
    return R, t


def align(img, left_eye, right_eye, out_size=(1080, 1080),
          target_left=TARGET_LEFT, target_right=TARGET_RIGHT):
    """Warp img so the two eye points land on the targets. PIL samples output -> source."""
    img = img.convert("RGB")
    R, t = similarity_for_eyes(left_eye, right_eye, out_size, target_left, target_right)
    Ri = np.linalg.inv(R)
    ti = -Ri @ t
    return img.transform(out_size, Image.Transform.AFFINE,
                         (Ri[0, 0], Ri[0, 1], ti[0], Ri[1, 0], Ri[1, 1], ti[1]),
                         resample=Image.Resampling.BICUBIC, fillcolor=(20, 20, 20))


def make_synthetic_face(size=(800, 1000)):
    """A cartoon face with two dark eye dots at TEST_LEFT_EYE and TEST_RIGHT_EYE. No real person."""
    img = Image.new("RGB", size, (200, 200, 200))
    d = ImageDraw.Draw(img)
    d.ellipse((140, 140, 660, 820), fill=(236, 214, 190))
    for ex, ey in (TEST_LEFT_EYE, TEST_RIGHT_EYE):
        d.ellipse((ex - 12, ey - 12, ex + 12, ey + 12), fill=(30, 30, 30))
    d.line((400, 460, 400, 520), fill=(150, 110, 90), width=6)
    d.arc((340, 580, 460, 640), start=0, end=180, fill=(150, 60, 60), width=8)
    return img


def warp_similarity(img, angle_deg, scale, shift):
    """Apply a known similarity transform F(p) = scale * R(angle) p + shift to an image."""
    a = math.radians(angle_deg)
    Rinv = np.array([[math.cos(-a), -math.sin(-a)], [math.sin(-a), math.cos(-a)]]) / scale
    ti = -Rinv @ np.asarray(shift, float)
    return img.transform(img.size, Image.Transform.AFFINE,
                         (Rinv[0, 0], Rinv[0, 1], ti[0], Rinv[1, 0], Rinv[1, 1], ti[1]),
                         resample=Image.Resampling.BICUBIC, fillcolor=(200, 200, 200))


def forward(p, angle_deg, scale, shift):
    a = math.radians(angle_deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return scale * (R @ np.asarray(p, float)) + np.asarray(shift, float)


def dark_centre(img, near, radius=40, thresh=90):
    """Centroid of dark pixels in a window around `near`: where the eye dot really is."""
    g = np.asarray(img.convert("L"), float)
    x0, y0 = max(int(near[0]) - radius, 0), max(int(near[1]) - radius, 0)
    win = g[y0:int(near[1]) + radius, x0:int(near[0]) + radius]
    ys, xs = np.nonzero(win < thresh)
    if len(xs) == 0:
        return None
    return np.array([xs.mean() + x0, ys.mean() + y0])


def selftest():
    """Three synthetic poses spanning rotation -12..+9 degrees and scale 0.6..1.7.

    The true eye positions are known analytically, so the error is measured
    on where the dark dots land after alignment, against the targets.
    """
    base = make_synthetic_face()
    W, H = 1080, 1080
    cases = [(-12.0, 0.6), (0.0, 1.0), (9.0, 1.7)]
    errors = []
    for angle, scale in cases:
        mid_src = (np.array(TEST_LEFT_EYE) + np.array(TEST_RIGHT_EYE)) / 2
        shift = np.array([400.0, 500.0]) - forward(mid_src, angle, scale, (0, 0))
        posed = warp_similarity(base, angle, scale, shift)
        eyeL = forward(TEST_LEFT_EYE, angle, scale, shift)
        eyeR = forward(TEST_RIGHT_EYE, angle, scale, shift)
        out = align(posed, eyeL, eyeR, out_size=(W, H))
        for target, rel in ((TARGET_LEFT, "L"), (TARGET_RIGHT, "R")):
            want = np.array([target[0] * W, target[1] * H])
            got = dark_centre(out, want)
            err = float("nan") if got is None else float(np.linalg.norm(got - want))
            errors.append(err)
            print(f"case rot={angle:+5.1f} scale={scale:.1f} eye={rel} error={err:.2f} px")
    worst = max(errors)
    print(f"worst error over {len(errors)} eye points: {worst:.2f} px")
    return 0 if worst < 3.0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Align a photo so two eye points land on fixed targets.")
    ap.add_argument("--image", help="input photo (any format Pillow reads)")
    ap.add_argument("--left-eye", help="x,y of the eye on the picture's left, in pixels")
    ap.add_argument("--right-eye", help="x,y of the eye on the picture's right, in pixels")
    ap.add_argument("--out", help="output image, e.g. aligned.png")
    ap.add_argument("--size", type=int, default=1080, help="square output size in pixels (default 1080)")
    ap.add_argument("--target-y", type=float, default=0.40, help="eye line height as a fraction (default 0.40)")
    ap.add_argument("--selftest", action="store_true", help="run three synthetic cases and print the error")
    ap.add_argument("--make-test-image", metavar="PATH", help="write the synthetic test face to PATH")
    a = ap.parse_args(argv)

    if a.make_test_image:
        make_synthetic_face().save(a.make_test_image)
        print(f"wrote {a.make_test_image}")
        return 0
    if a.selftest:
        return selftest()
    if not (a.image and a.left_eye and a.right_eye and a.out):
        ap.error("--image, --left-eye, --right-eye and --out are required")

    def xy(text):
        x, y = text.split(",")
        return float(x), float(y)

    tl = (TARGET_LEFT[0], a.target_y)
    tr = (TARGET_RIGHT[0], a.target_y)
    img = Image.open(a.image)
    out = align(img, xy(a.left_eye), xy(a.right_eye), out_size=(a.size, a.size),
                target_left=tl, target_right=tr)
    out.save(a.out)
    print(f"wrote {a.out} ({a.size}x{a.size})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
