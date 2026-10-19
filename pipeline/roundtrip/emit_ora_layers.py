#!/usr/bin/env python3
"""emit_ora_layers.py: write a SYNTHETIC layered still as OpenRaster (.ora) for the PhotoCraft hand-off tests (WP-06). Pillow.

  python3 -I pipeline/roundtrip/emit_ora_layers.py OUT.ora [--width 640] [--height 360]

The layers are generated test cards, NOT a photograph (no family media exists here and none may be created or simulated). They are named by
id, top first as OpenRaster wants, and the bottom layer is the as-found layer (W-27):

    L30_label      200x60 chip at (24,24), svg:multiply, opacity 0.6
    L20_figure     240x200 flat shapes with anti-aliased (straight-alpha) edges at (200,80), svg:src-over
    L10_restored   full-canvas colour ramp with a grid, opaque
    L00_asfound    full-canvas flat card (four colour patches and a grid), opaque: the "untouched" layer

Format: 8-bit sRGB straight-alpha RGBA PNG layers under data/, 'mimetype' FIRST and STORED, stack.xml (version 0.0.3, which PhotoCraft v0.9.0
and v0.10.0 both read the old way: research/craft-visual.md), mergedimage.png at canvas size. Fixed member timestamps and permissions, so the
same Pillow gives the same bytes. validate_ora.py is the checker. It writes the one file you name and reads nothing.
EXIT CODES  0 ok   2 bad usage   3 Pillow missing
"""
import argparse
import io
import os
import sys
import zipfile

sys.dont_write_bytecode = True

STAMP = (1980, 1, 1, 0, 0, 0)


def _layers(w, h):
    """Return the layer list top-first: dicts with name, src, x, y, opacity, op, image (RGBA)."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.load_default(size=max(h // 14, 10))
    except TypeError:
        font = ImageFont.load_default()

    # L00_asfound: flat card with four patches and a faint grid
    l00 = Image.new("RGBA", (w, h), (72, 68, 62, 255))
    d = ImageDraw.Draw(l00)
    for x in range(0, w, 40):
        d.line([(x, 0), (x, h)], fill=(96, 92, 86, 255))
    for y in range(0, h, 40):
        d.line([(0, y), (w, y)], fill=(96, 92, 86, 255))
    pw, ph = w // 4, h // 4
    for i, col in enumerate(((150, 90, 80), (90, 140, 90), (80, 100, 150), (160, 150, 90))):
        d.rectangle([i * pw + 8, h - ph - 8, i * pw + pw - 8, h - 8], fill=col + (255,))
    d.text((w // 2, h // 3), "L00 AS-FOUND  TEST CARD", fill=(235, 230, 220, 255), font=font, anchor="mm")

    # L10_restored: a colour ramp, opaque
    l10 = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    d = ImageDraw.Draw(l10)
    for x in range(w):
        t = x / float(max(w - 1, 1))
        d.line([(x, 0), (x, h)], fill=(int(40 + 190 * t), int(90 + 80 * (1 - t)), int(200 - 150 * t), 255))
    for x in range(0, w, 40):
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, 255), width=1)
    for y in range(0, h, 40):
        d.line([(0, y), (w, y)], fill=(255, 255, 255, 255), width=1)
    d.text((w // 2, h - h // 8), "L10 RESTORED  TEST CARD", fill=(255, 255, 255, 255), font=font, anchor="mm")

    # L20_figure: a disc and a bar over transparency, drawn at 4x and reduced so the edges carry partial (straight) alpha
    fw, fh = 240, 200
    big = Image.new("RGBA", (fw * 4, fh * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.ellipse([40 * 4, 20 * 4, 160 * 4, 140 * 4], fill=(235, 190, 40, 255))
    d.rectangle([100 * 4, 130 * 4, 140 * 4, 190 * 4], fill=(40, 60, 90, 255))
    d.polygon([(170 * 4, 150 * 4), (230 * 4, 150 * 4), (200 * 4, 100 * 4)], fill=(190, 50, 60, 220))
    l20 = big.resize((fw, fh), Image.LANCZOS)

    # L30_label: an opaque chip to be multiplied at 60 percent
    l30 = Image.new("RGBA", (200, 60), (210, 90, 90, 255))
    d = ImageDraw.Draw(l30)
    d.text((100, 30), "L30 LABEL", fill=(255, 255, 255, 255), font=font, anchor="mm")

    return [
        dict(name="L30_label", src="data/L30_label.png", x=24, y=24, opacity=0.6, op="svg:multiply", image=l30),
        dict(name="L20_figure", src="data/L20_figure.png", x=200, y=80, opacity=1.0, op="svg:src-over", image=l20),
        dict(name="L10_restored", src="data/L10_restored.png", x=0, y=0, opacity=1.0, op="svg:src-over", image=l10),
        dict(name="L00_asfound", src="data/L00_asfound.png", x=0, y=0, opacity=1.0, op="svg:src-over", image=l00),
    ]


def _merge(w, h, layers):
    """Composite bottom-up onto an opaque canvas. Handles svg:src-over and svg:multiply with layer opacity."""
    from PIL import Image, ImageChops
    canvas = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    for L in reversed(layers):
        im = L["image"]
        alpha = im.getchannel("A").point(lambda v, o=L["opacity"]: int(round(v * o)))
        region = canvas.crop((L["x"], L["y"], L["x"] + im.width, L["y"] + im.height))
        if L["op"] == "svg:multiply":
            src_rgb = ImageChops.multiply(region.convert("RGB"), im.convert("RGB"))
        else:
            src_rgb = im.convert("RGB")
        blended = Image.composite(src_rgb, region.convert("RGB"), alpha).convert("RGBA")
        canvas.paste(blended, (L["x"], L["y"]))
    return canvas


def _png(im):
    b = io.BytesIO()
    im.save(b, "PNG", optimize=True, compress_level=9)
    return b.getvalue()


def _member(z, name, data, method):
    zi = zipfile.ZipInfo(name, STAMP)
    zi.compress_type = method
    zi.external_attr = 0o644 << 16
    z.writestr(zi, data)


def build_ora(path, width=640, height=360):
    """Write the file; return a dict describing it (canvas, layers top-first)."""
    layers = _layers(width, height)
    merged = _merge(width, height, layers)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<image version="0.0.3" w="%d" h="%d" xres="300" yres="300"><stack>' % (width, height)]
    for L in layers:
        xml.append('<layer name="%s" src="%s" x="%d" y="%d" opacity="%.1f" visibility="visible" composite-op="%s"/>' % (
            L["name"], L["src"], L["x"], L["y"], L["opacity"], L["op"]))
    xml.append("</stack></image>")
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        _member(z, "mimetype", b"image/openraster", zipfile.ZIP_STORED)            # first, stored
        _member(z, "stack.xml", ("\n".join(xml) + "\n").encode("utf-8"), zipfile.ZIP_DEFLATED)
        for L in layers:
            _member(z, L["src"], _png(L["image"]), zipfile.ZIP_STORED)
        _member(z, "mergedimage.png", _png(merged), zipfile.ZIP_STORED)
    return {"canvas": [width, height], "layers": [L["name"] for L in layers]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write a synthetic layered still (OpenRaster) with L00_asfound at the bottom.")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=640)
    ap.add_argument("--height", type=int, default=360)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if a.width < 480 or a.height < 300 or a.width > 4096 or a.height > 4096:
        print("emit_ora_layers: size must be between 480x300 and 4096x4096 (the figure layer sits at 200,80 and is 240x200)", file=sys.stderr)
        return 2
    try:
        info = build_ora(a.out, a.width, a.height)
    except ImportError:
        print("emit_ora_layers: Pillow is not installed", file=sys.stderr)
        return 3
    print("wrote %s: %dx%d canvas, layers top-first %s" % (a.out, info["canvas"][0], info["canvas"][1], ", ".join(info["layers"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
