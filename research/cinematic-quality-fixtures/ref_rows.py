"""Round 2: Pillow / ffmpeg reference rows for the renderer comparison, on the SAME still, push length and amount as the renderer under test.
  python3 -I ref_rows.py STILL_4K.png OUT.jsonl N AMOUNT [methods: pil_box,pil_extent,zoompan]
Each row: raw frames and the same frames after x264 CRF 14, with mo8_audit's numbers (9-frame-mean versions a, b, c and 4th-difference versions a_d4, b_d4).
The push is a cosine in-out of AMOUNT over N frames at 24 fps, centred, 1080p output, as in zoompan_vs_subpixel_prints.py."""
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mo8_audit as ma
W, H, FPS = 1920, 1080, 24
still_path, outp, N, AMT = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
methods = (sys.argv[5] if len(sys.argv) > 5 else "pil_box,pil_extent,zoompan").split(",")
src = Image.open(still_path).convert("RGB")
def z_at(i): return 1 + AMT * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1)))
def pil(kind):
    sw, sh = src.size; out = np.empty((N, H, W, 3), np.uint8)
    for i in range(N):
        z = z_at(i); w, h = sw / z, sh / z; x0, y0 = (sw - w) / 2, (sh - h) / 2
        out[i] = np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))) if kind == "pil_box" else \
                 np.asarray(src.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC))
    return out
def zoompan():
    z = f"1+{AMT}*(0.5-0.5*cos(PI*on/{N-1}))"
    vf = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}:d={N},format=rgb24"
    r = subprocess.run([ma.FFMPEG, "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", still_path, "-vf", vf, "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(N, H, W, 3)
for m in methods:
    fr = zoompan() if m == "zoompan" else pil(m)
    for codec, frames in (("raw", fr), ("h264_crf14", ma.via_h264(fr))):
        r = ma.audit(frames)
        rec = dict(method=m, N=N, amount=AMT, codec=codec, still=os.path.basename(still_path), a=r["mo8a_centre_jit_px"], b=r["mo8b_edge_jit_px"], c=r["mo8c_rough"],
                   a_d4=r["mo8a_d4_px"], b_d4=r["mo8b_d4_px"], zoom_total_pct=r["zoom_total_pct"], ease_class=r["ease_class"])
        open(outp, "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
