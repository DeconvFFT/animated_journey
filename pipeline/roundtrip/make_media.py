#!/usr/bin/env python3
"""make_media.py: generate SYNTHETIC test media for the round-trip tests (WP-06): numbered test-card stills (PNG) and a sine-tone WAV.

  python3 -I pipeline/roundtrip/make_media.py OUTDIR [--stills 4] [--size 2880x1620] [--seconds 20] [--prefix ch01]

Writes   OUTDIR/<prefix>_s01.png ... (a flat dark card with a grid, a numbered label, four corner colour chips, a centre cross and a
         colour-bar strip; no photograph, no person, no symbol of any kind: build plan 4.10)
         OUTDIR/mix_<prefix>.wav (mono, 48 kHz, 16-bit sine, -18 dBFS: a stand-in audio cue, not music and not a voice)
It never reads or overwrites a file that already exists (it skips it and says so), so it can not touch real media by accident.
Needs Pillow for the stills (python3 -I picks up the system copy); the WAV uses only the standard library.
EXIT CODES  0 ok   2 bad usage   3 Pillow missing
"""
import argparse
import math
import os
import struct
import sys
import wave

sys.dont_write_bytecode = True

HUES = [(24, 32, 48), (40, 28, 52), (22, 48, 44), (52, 38, 24), (30, 30, 30), (48, 24, 32)]


def still_png(path, width, height, index, label, base=None):
    """One test card. Deterministic: the same arguments give the same bytes on the same Pillow. `base` is an optional (r, g, b) background; left out, the card takes
    the dark tint HUES[index - 1], so every card made before this argument existed is unchanged. A test chapter whose dissolve must be visible one frame at a time asks
    for a base that differs strongly from its neighbour (the dark tints differ by at most about 30 levels, which a step-through cannot see)."""
    from PIL import Image, ImageDraw, ImageFont
    base = tuple(base) if base is not None else HUES[(index - 1) % len(HUES)]
    im = Image.new("RGB", (width, height), base)
    d = ImageDraw.Draw(im)
    step = max(width // 24, 8)
    for x in range(0, width + 1, step):
        d.line([(x, 0), (x, height)], fill=(88, 96, 112), width=1 if (x // step) % 4 else 3)
    for y in range(0, height + 1, step):
        d.line([(0, y), (width, y)], fill=(88, 96, 112), width=1 if (y // step) % 4 else 3)
    cx, cy = width // 2, height // 2
    d.line([(0, 0), (width - 1, height - 1)], fill=(150, 160, 176), width=2)
    d.line([(0, height - 1), (width - 1, 0)], fill=(150, 160, 176), width=2)
    r = height // 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(240, 240, 240), width=max(height // 270, 2))
    chip = height // 10
    for (x0, y0, col) in ((0, 0, (220, 60, 60)), (width - chip, 0, (60, 200, 80)), (0, height - chip, (70, 110, 230)),
                          (width - chip, height - chip, (230, 210, 60))):
        d.rectangle([x0, y0, x0 + chip - 1, y0 + chip - 1], fill=col)
    bars = [(235, 235, 235), (235, 235, 60), (60, 235, 235), (60, 235, 60), (235, 60, 235), (235, 60, 60), (60, 60, 235), (16, 16, 16)]
    bh = height // 12
    bw = (width - 2 * chip) // len(bars)
    for i, col in enumerate(bars):
        d.rectangle([chip + i * bw, height - chip - bh, chip + (i + 1) * bw - 1, height - chip], fill=col)
    try:
        font = ImageFont.load_default(size=max(height // 6, 12))
        small = ImageFont.load_default(size=max(height // 16, 10))
    except TypeError:                                   # very old Pillow: fixed small bitmap font
        font = small = ImageFont.load_default()
    d.text((cx, cy - r - height // 12), label, fill=(255, 255, 255), font=font, anchor="mm")
    d.text((cx, cy + r + height // 14), "%dx%d  TEST CARD %02d" % (width, height, index), fill=(200, 210, 224), font=small, anchor="mm")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    im.save(path, "PNG", optimize=True, compress_level=9)


def sine_wav(path, seconds, rate=48000, freq=220.0, dbfs=-18.0):
    n = int(seconds * rate)
    amp = 32767.0 * (10.0 ** (dbfs / 20.0))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        chunk = 4800
        for start in range(0, n, chunk):
            m = min(chunk, n - start)
            w.writeframes(b"".join(struct.pack("<h", int(round(amp * math.sin(2 * math.pi * freq * (start + i) / rate)))) for i in range(m)))


def make_all(outdir, stills=4, size=(2880, 1620), seconds=20, prefix="ch01"):
    """Create what is missing; return the list of (path, 'created'|'kept')."""
    done = []
    for i in range(1, stills + 1):
        p = os.path.join(outdir, "%s_s%02d.png" % (prefix, i))
        if os.path.exists(p):
            done.append((p, "kept"))
            continue
        still_png(p, size[0], size[1], i, "%s S%02d" % (prefix.upper(), i))
        done.append((p, "created"))
    p = os.path.join(outdir, "mix_%s.wav" % prefix)
    if os.path.exists(p):
        done.append((p, "kept"))
    else:
        sine_wav(p, seconds)
        done.append((p, "created"))
    return done


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate synthetic test-card stills and a sine WAV (never overwrites).")
    ap.add_argument("outdir")
    ap.add_argument("--stills", type=int, default=4)
    ap.add_argument("--size", default="2880x1620")
    ap.add_argument("--seconds", type=float, default=20.0)
    ap.add_argument("--prefix", default="ch01")
    try:
        a = ap.parse_args(argv)
        w, h = (int(p) for p in a.size.lower().split("x"))
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    except ValueError:
        print("make_media: --size must look like 2880x1620", file=sys.stderr)
        return 2
    try:
        res = make_all(a.outdir, a.stills, (w, h), a.seconds, a.prefix)
    except ImportError:
        print("make_media: Pillow is not installed", file=sys.stderr)
        return 3
    for p, what in res:
        print("%s %s" % (what, p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
