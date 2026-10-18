#!/usr/bin/env python3
"""Paper-print wobble on twos: a rigid card moves to a new pose every `hold` frames.

Own implementation of research note T4 (tested 2026-10-18, [66]); parameter names
follow pasteup [60]. Only translation and rotation: photo pixels are never repainted.
A fixed --seed gives the same wobble every run.

Usage:
  python jitter_twos.py --card card.png --out-dir frames --seed 7
  ffmpeg -framerate 24 -i frames/f%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p wobble.mp4
  python jitter_twos.py --selftest
"""
import argparse
import random
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def wobble_frames(card, out_dir, n=48, hold=2, jitter_px=3, jitter_deg=0.6, seed=7,
                  size=(1280, 720), bg=(92, 70, 52)):
    """card: RGBA print with a white border. Writes f0000.png ... into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(seed)              # private RNG: same seed -> same wobble
    dx = dy = rot = 0.0
    for f in range(n):
        if f % hold == 0:                  # new pose only every `hold` frames
            dx = rnd.uniform(-jitter_px, jitter_px)
            dy = rnd.uniform(-jitter_px, jitter_px)
            rot = rnd.uniform(-jitter_deg, jitter_deg)
        canvas = Image.new("RGB", size, bg)
        r = card.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
        x = (size[0] - r.width) // 2 + int(dx)
        y = (size[1] - r.height) // 2 + int(dy)
        canvas.paste(r, (x, y), r)
        canvas.save(out_dir / f"f{f:04d}.png")


def synthetic_card(w=400, h=300, border=14):
    """A plain printed-photo stand-in: white border, grey-blue picture, transparent outside."""
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rectangle((0, 0, w - 1, h - 1), fill=(255, 255, 255, 255))
    d.rectangle((border, border, w - 1 - border, h - 1 - border), fill=(150, 170, 190, 255))
    d.ellipse((w * 0.35, h * 0.3, w * 0.65, h * 0.7), fill=(236, 214, 190, 255))
    return card


def selftest():
    """Expect 24 of 24 held pairs identical, 23 of 23 pose changes different, same seed repeats."""
    n, hold = 48, 2
    card = synthetic_card()
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "a", Path(tmp) / "b"
        wobble_frames(card, a, n=n, hold=hold, seed=7)
        wobble_frames(card, b, n=n, hold=hold, seed=7)
        frames = [np.asarray(Image.open(a / f"f{i:04d}.png")) for i in range(n)]
        again = [np.asarray(Image.open(b / f"f{i:04d}.png")) for i in range(n)]
    blocks = [frames[i] for i in range(0, n, hold)]
    held = sum(np.array_equal(frames[i], frames[i + 1]) for i in range(0, n, hold))
    changes = sum(not np.array_equal(frames[i + hold - 1], frames[i + hold])
                  for i in range(0, n - hold, hold))
    repeat = all(np.array_equal(x, y) for x, y in zip(frames, again))
    print(f"held pairs identical: {held} of {len(blocks)}")
    print(f"pose changes different: {changes} of {len(blocks) - 1}")
    print(f"same seed repeats exactly: {repeat}")
    ok = held == len(blocks) and changes == len(blocks) - 1 and repeat
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hold-on-twos paper wobble for a printed-photo card.")
    ap.add_argument("--card", help="RGBA PNG of the print, transparent outside, white border")
    ap.add_argument("--out-dir", default="frames", help="folder for f0000.png, f0001.png, ...")
    ap.add_argument("--frames", type=int, default=48)
    ap.add_argument("--hold", type=int, default=2, help="frames per pose (2 smooth, 3 chunky)")
    ap.add_argument("--jitter-px", type=float, default=3.0)
    ap.add_argument("--jitter-deg", type=float, default=0.6)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--bg", default="92,70,52", help="backdrop colour as R,G,B (default wood brown)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.card:
        ap.error("--card is required (or use --selftest)")
    card = Image.open(a.card).convert("RGBA")
    bg = tuple(int(v) for v in a.bg.split(","))
    wobble_frames(card, a.out_dir, n=a.frames, hold=a.hold, jitter_px=a.jitter_px,
                  jitter_deg=a.jitter_deg, seed=a.seed, size=(a.width, a.height), bg=bg)
    print(f"wrote {a.frames} frames to {a.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
