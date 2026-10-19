#!/usr/bin/env python3
"""gen_stills.py: low-entropy synthetic JPEG stills for the SP1 tests (Pillow only).

Each still is a flat colour (a different one per index), a thin dark grid, a big index number in one corner, and optionally a magenta
square whose centre is known exactly. A 3600x2400 file is about 100 KB, yet the engine must decode all 8.6 million pixels, which is what
the memory and speed tests measure (decode cost depends on pixels, not on file size). PNG would not fit the disk (build plan WP-07).
The grid is placed so that the centre of the picture sits in the middle of a flat cell: a patch there is a true flat colour at any
scale of a centred move, which is what the dissolve check samples. No photograph, no face, no text but digits.

USAGE (as a module)  from gen_stills import make_still, flat_colour, grid_offsets
     python3 -I gen_stills.py OUT_DIR N WIDTH HEIGHT        # writes s0001.jpg .. sNNNN.jpg
"""
import colorsys
import os
import sys

sys.dont_write_bytecode = True
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

MARKER = (255, 0, 255)
MARKER_SIZE = 60


def flat_colour(idx):
    """A distinct, clearly non-magenta colour per index (golden-ratio hue steps, mid saturation and value)."""
    h = (idx * 0.618033988749895) % 1.0
    if 0.78 <= h <= 0.92:  # keep clear of magenta
        h = (h + 0.2) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.55, 0.85)
    return int(r * 255), int(g * 255), int(b * 255)


def grid_offsets(w, h, spacing=300):
    """First grid line positions so that the picture centre is the middle of a cell."""
    return (w // 2 - spacing // 2) % spacing, (h // 2 - spacing // 2) % spacing


def make_still(path, w, h, idx, colour=None, marker_xy=None, quality=75, spacing=300):
    colour = colour or flat_colour(idx)
    im = Image.new("RGB", (w, h), colour)
    d = ImageDraw.Draw(im)
    x0, y0 = grid_offsets(w, h, spacing)
    line = tuple(max(0, c - 70) for c in colour)
    for x in range(x0, w, spacing):
        d.rectangle([x - 2, 0, x + 1, h - 1], fill=line)
    for y in range(y0, h, spacing):
        d.rectangle([0, y - 2, w - 1, y + 1], fill=line)
    try:
        font = ImageFont.load_default(size=max(24, h // 12))
    except TypeError:  # an older Pillow without the size argument
        font = ImageFont.load_default()
    d.text((max(10, w // 60), max(10, h // 60)), "%04d" % idx, fill=(20, 20, 20), font=font)
    if marker_xy:
        mx, my = marker_xy
        half = MARKER_SIZE // 2
        d.rectangle([mx - half, my - half, mx + half - 1, my + half - 1], fill=MARKER)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    im.save(path, "JPEG", quality=quality, subsampling=2, optimize=True)
    return os.path.getsize(path)


def centre_colour(path):
    """The decoded colour at the exact centre of a still (what a flat-patch check should expect)."""
    with Image.open(path) as im:
        w, h = im.size
        return im.convert("RGB").getpixel((w // 2, h // 2))


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    out, n, w, h = argv[0], int(argv[1]), int(argv[2]), int(argv[3])
    total = 0
    for i in range(1, n + 1):
        total += make_still(os.path.join(out, "s%04d.jpg" % i), w, h, i)
    print("wrote %d stills of %dx%d, %.1f KB each on average" % (n, w, h, total / n / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
