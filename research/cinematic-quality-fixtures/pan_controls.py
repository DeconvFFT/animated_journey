"""Control and stress tests for pan_estimator (follow-up round 1, M-C9b). Usage: python3 -I pan_controls.py SRC_DIR OUT_JSONL
Controls: static texture (expect 0), flat grain-only frames (expect INCONCLUSIVE), fade to black, a fast 10% push-in (zoom, no pan),
and a pan combined with a push-in."""
import sys, os, json, math
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pan_estimator as pe, pan_validate as pv
W, H, N = pv.W, pv.H, pv.N
src_dir, outp = sys.argv[1:3]
fn = next(f for f in sorted(os.listdir(src_dir)) if f.startswith("p3") and f.endswith("_4k.png"))
src = Image.open(os.path.join(src_dir, fn)).convert("RGB"); rng = np.random.default_rng(3)
def audit(name, L, note=""):
    s, res = pe.pan_audit(L)
    rec = dict(control=name, note=note, verdict=s['verdict'], est_peak_px=round(s['peak_px'], 3), valid_frac=round(s['valid_frac'], 2), twos=s['twos'], fast_head=[round(float(x), 2) for x in res['fast'][:6]])
    open(outp, "a").write(json.dumps(rec) + "\n"); print(rec, flush=True)
base = pv.luma(pv.window(src, 1800.0, 540))
audit("static texture", np.stack([base] * N), "40 identical frames: speed 0 is a valid PASS")
audit("flat grain only", np.stack([rng.normal(128, 2, (H, W)).astype(np.float32) for _ in range(N)]), "no texture, independent noise: must not invent a speed")
fade = [pv.luma(pv.window(src, 1800.0 - 8.0 * i, 540)) * max(0.0, 1 - i / (N - 1)) for i in range(N)]
audit("8 px/frame pan fading to black", np.stack(fade), "truth 8.0 while visible")
# push-in only, 10% over 40 frames, no pan: tile-edge displacement is the zoom seen as translation
fr = []
for i in range(N):
    z = 1 + 0.10 * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1))); w, h = 1920 / z, 1080 / z; x0, y0 = 1800 + (1920 - w) / 2, 540 + (1080 - h) / 2
    fr.append(pv.luma(np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)))))
audit("10% push-in over 1.7 s, no pan", np.stack(fr), "zoom shows as translation in outer tiles; true edge speed at the peak is about 0.1 x 960 x pi / 2 / 39 = 3.9 px/frame")
# pan 8 px/frame plus the same push-in: the estimator should stay near 8 plus the zoom contribution, not crash
fr = []
for i in range(N):
    z = 1 + 0.05 * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1))); w, h = 1920 / z, 1080 / z; x0, y0 = 1800 - 8.0 * i + (1920 - w) / 2, 540 + (1080 - h) / 2
    fr.append(pv.luma(np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)))))
audit("8 px/frame pan plus 5% push-in", np.stack(fr), "truth: 8 px/frame centre, outer tiles add up to 0.05 x 960 x pi / 2 / 39 = 1.9 px/frame")
