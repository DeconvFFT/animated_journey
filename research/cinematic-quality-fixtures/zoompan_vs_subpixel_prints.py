"""Follow-up M-C7b: zoompan vs sub-pixel roughness on three scanned prints, from 4K and native-1080p sources.
Usage: python3 -I zoompan_vs_subpixel_prints.py SRC_DIR WORK_DIR OUT_JSONL [amt] [methods comma list]
SRC_DIR holds  <print>_4k.png and <print>_1080.png (16:9 crops). Needs ffmpeg 6.x, numpy, Pillow.
Metric (as in MO8): velocity = per-frame-pair zoom rate s from a 3-parameter least-squares (Lucas-Kanade) fit
(tx, ty, zoom about the frame centre); roughness = std(s - 9-frame moving mean) / mean|s|. Also reports translation
jitter (rms of tx,ty minus their 9-frame mean, in output pixels at the analysis scale, rescaled to 1080p px).
Frames are analysed twice: raw (no codec) and after H.264 CRF 14 yuv420p."""
import sys, os, math, json, time, subprocess
import numpy as np
from PIL import Image
W, H, N, FPS = 1920, 1080, 96, 24
LUMA = np.array([0.299, 0.587, 0.114], np.float32)

def zoom_at(i, amt): return 1 + amt * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1)))
def pil_extent(src, amt):
    sw, sh = src.size; out = np.empty((N, H, W, 3), np.uint8)
    for i in range(N):
        z = zoom_at(i, amt); w, h = sw / z, sh / z; x0, y0 = (sw - w) / 2, (sh - h) / 2
        out[i] = np.asarray(src.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC))
    return out
def pil_resize_box(src, amt):
    sw, sh = src.size; out = np.empty((N, H, W, 3), np.uint8)
    for i in range(N):
        z = zoom_at(i, amt); w, h = sw / z, sh / z; x0, y0 = (sw - w) / 2, (sh - h) / 2
        out[i] = np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)))
    return out
def ff_zoompan(png, amt, prescale):
    pre = f"scale=iw*{prescale}:ih*{prescale}:flags=lanczos," if prescale > 1 else ""
    z = f"1+{amt}*(0.5-0.5*cos(PI*on/{N-1}))"
    vf = f"{pre}zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}:d={N},format=rgb24"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", png, "-vf", vf,
                        "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(N, H, W, 3)
def encode_decode(frames, mp4):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", mp4], stdin=subprocess.PIPE)
    p.stdin.write(frames.tobytes()); p.stdin.close(); p.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    size = os.path.getsize(mp4)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W, 3), size
def luma(frames): return (frames.astype(np.float32) @ LUMA)
def down(a, f):
    if f == 1: return a
    n, h, w = a.shape; return a.reshape(n, h // f, f, w // f, f).mean(axis=(2, 4))
def blur(a, sigma):
    r = int(math.ceil(3 * sigma)); k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    p = np.pad(a, ((r, r), (0, 0)), mode="edge"); a = sum(k[i] * p[i:i + a.shape[0]] for i in range(2 * r + 1))
    p = np.pad(a, ((0, 0), (r, r)), mode="edge"); return sum(k[i] * p[:, i:i + a.shape[1]] for i in range(2 * r + 1))
def lk3(a, b):
    h, w = a.shape; g = blur((a + b) / 2, 1.0); gy, gx = np.gradient(g)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32); xs -= w / 2; ys -= h / 2
    m = (slice(int(0.06 * h), int(0.94 * h)), slice(int(0.06 * w), int(0.94 * w)))
    d = (blur(b, 1.0) - blur(a, 1.0))[m]
    A = np.stack([gx[m].ravel(), gy[m].ravel(), (xs * gx + ys * gy)[m].ravel()], 1)
    p = np.linalg.lstsq(A, -d.ravel(), rcond=None)[0]
    return p  # tx, ty (px at this scale), s (fractional zoom per frame pair)
def series(lum, f):
    a = down(lum, f); P = np.array([lk3(a[i], a[i + 1]) for i in range(len(a) - 1)])
    if P[:, 2].sum() < 0: P[:, 2] *= -1
    return P
def mm(x, k=9):
    p = np.pad(x, (k // 2, k // 2), mode="reflect"); return np.convolve(p, np.ones(k) / k, mode="valid")
def metrics(P, f, mean_speed=None):
    s = P[:, 2]; res = s - mm(s); ms = mean_speed if mean_speed else np.abs(s).mean()
    out = dict(rough=float(res.std() / ms), mean_speed=float(np.abs(s).mean()),
               edge_jit_px1080=float(res.std() * (W / 2)))   # zoom-rate jitter expressed as displacement at the frame edge, output px per frame (speed-independent)
    for j, nme in ((0, "tx"), (1, "ty")):
        out[nme + "_jit_px1080"] = float((P[:, j] - mm(P[:, j])).std() * f)
    return out
def orig_mc7(mp4):
    """The estimator behind M-C7 in research/cinematic-quality.md: zoom-only least squares at 240x135 on the H.264 file,
    frames scaled by ffmpeg (default bicubic) to gray, np.gradient, no pre-blur, margins 15/20 px."""
    w, h = 240, 135
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32); xs -= w / 2; ys -= h / 2
    c = (slice(15, h - 15), slice(20, w - 20)); v = []
    for i in range(len(a) - 1):
        gy, gx = np.gradient(a[i]); g = xs * gx + ys * gy; d = a[i + 1] - a[i]
        v.append(float((d[c] * g[c]).sum() / ((g[c] ** 2).sum() + 1e-9)))
    v = np.array(v); v = v * (1 if v.sum() >= 0 else -1)
    return dict(rough=float((v - mm(v)).std() / np.abs(v).mean()), mean_speed=float(np.abs(v).mean()))
def analyse(frames, f):
    return metrics(series(luma(frames), f), f)
if __name__ == "__main__":
    src_dir, work, outp = sys.argv[1:4]; amt = float(sys.argv[4]) if len(sys.argv) > 4 else 0.04
    methods = (sys.argv[5] if len(sys.argv) > 5 else "pil_extent,pil_box,zp,zp2x").split(",")
    scales = [int(x) for x in (sys.argv[6] if len(sys.argv) > 6 else "4,1").split(",")]
    os.makedirs(work, exist_ok=True)
    prints = sorted({f.rsplit("_", 1)[0] for f in os.listdir(src_dir) if f.endswith(".png")})
    if os.environ.get("ONLY_PRINT"): prints = [p for p in prints if p.startswith(os.environ["ONLY_PRINT"])]
    for pr in prints:
        for tag in ("4k", "1080"):
            png = os.path.join(src_dir, f"{pr}_{tag}.png"); src = Image.open(png).convert("RGB")
            for m in methods:
                if m == "zp4x" and tag == "4k": continue   # 16K intermediate is not practical
                t0 = time.time()
                if m == "pil_extent": fr = pil_extent(src, amt)
                elif m == "pil_box": fr = pil_resize_box(src, amt)
                elif m == "zp": fr = ff_zoompan(png, amt, 1)
                elif m.startswith("zp") and m.endswith("x"): fr = ff_zoompan(png, amt, int(m[2:-1]))
                else: raise SystemExit("unknown method " + m)
                mp4 = os.path.join(work, f"t_{os.getpid()}.mp4")
                dec, size = encode_decode(fr, mp4)
                orec = dict(print=pr, src=tag, method=m, amt=amt, codec="h264", scale="orig240", bytes_h264=size); orec.update(orig_mc7(mp4))
                open(outp, "a").write(json.dumps(orec) + "\n"); os.remove(mp4)
                for codec, frames in (("raw", fr), ("h264", dec)):
                    for f in scales:
                        rec = dict(print=pr, src=tag, method=m, amt=amt, codec=codec, scale=f, bytes_h264=size, secs=round(time.time() - t0, 1))
                        rec.update(analyse(frames, f)); open(outp, "a").write(json.dumps(rec) + "\n")
                print(pr, tag, m, "done", round(time.time() - t0, 1), "s", flush=True)
