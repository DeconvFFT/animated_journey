# Stdlib-only OpenRaster writer for the PhotoCraft acceptance test (no Pillow needed).
import sys, zlib, struct, zipfile, pathlib

def png_rgba(w, h, pixel):                      # pixel(x, y) -> (r, g, b, a)
    raw = b"".join(b"\x00" + b"".join(bytes(pixel(x, y)) for x in range(w)) for y in range(h))
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

W, H = 320, 200
layers = [   # top-first, as in the OpenRaster spec
    dict(name="Title tint",  src="data/title.png", x=24,  y=24,  w=160, h=48,  opacity="0.6", op="svg:multiply",
         px=lambda x, y: (200, 60, 60, 255)),
    dict(name="Photo",       src="data/photo.png", x=0,   y=0,   w=W,   h=H,   opacity="1.0", op="svg:src-over",
         px=lambda x, y: ((x // 16) * 16 * 255 // W, (y // 16) * 16 * 255 // H, 128, 255)),
]
xml = [f'<?xml version="1.0" encoding="UTF-8"?>\n<image version="0.0.3" w="{W}" h="{H}" xres="300" yres="300"><stack>']
for L in layers:
    xml.append(f'<layer name="{L["name"]}" src="{L["src"]}" x="{L["x"]}" y="{L["y"]}" opacity="{L["opacity"]}" '
               f'visibility="visible" composite-op="{L["op"]}"/>')
xml.append("</stack></image>")
out = pathlib.Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(out, "w") as z:
    z.writestr(zipfile.ZipInfo("mimetype"), "image/openraster", compress_type=zipfile.ZIP_STORED)   # first, stored
    z.writestr("stack.xml", "\n".join(xml), compress_type=zipfile.ZIP_DEFLATED)
    for L in layers:
        z.writestr(L["src"], png_rgba(L["w"], L["h"], L["px"]), compress_type=zipfile.ZIP_STORED)
    z.writestr("mergedimage.png", png_rgba(W, H, lambda x, y: ((x // 16) * 16 * 255 // W, (y // 16) * 16 * 255 // H, 128, 255)))
print("wrote", out)
