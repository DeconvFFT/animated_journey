"""Validate pan_estimator on synthetic pans cut from 4K scans at 1:1 (so a window of 1920x1080 slides over the scan).
Usage: python3 -I pan_validate.py SRC_DIR OUT_JSONL WORK_DIR [variants comma list] [print prefixes comma list]
Variants: clean, grain_h264, twos, ease, parallax.  Speeds in frame widths per second: 0.10, 1/7 (=0.1429, the MO6 limit), 0.20, 0.30."""
import sys, os, json, time, math, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pan_estimator as pe
W, H, FPS, N = 1920, 1080, 24, 40
SPEEDS = [0.10, 1 / 7, 0.20, 0.30]
LUMA = np.array([0.299, 0.587, 0.114], np.float32)

def window(src, x0, y0): return np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + W, y0 + H)), dtype=np.uint8)
def luma(a): return a.astype(np.float32) @ LUMA

def disp_profile(vpk_px, kind, twos=False):
    n = N - 1
    if kind == 'ease': d = vpk_px * 0.5 * (1 - np.cos(2 * np.pi * np.arange(n) / (n - 1)))
    else: d = np.full(n, vpk_px)
    if twos:   # movement happens only on even output frames (one drawing every two frames): 2*d applied every other step
        d2 = np.zeros(n); d2[0::2] = 2 * d[0::2]; d = d2
    return d

def make_clip(src, vpk_px, kind='linear', twos=False, noise=0.0, parallax=None, rng=None):
    sw, sh = src.size; y0 = (sh - H) // 2
    d = disp_profile(vpk_px, kind, twos); total = d.sum()
    xs = (sw - W - 20) - np.concatenate([[0], np.cumsum(d)])      # window moves left => content moves right (+x)
    assert xs.min() > 0, (xs.min(), total)
    frames = []
    for i in range(N):
        a = window(src, xs[i], y0)
        if parallax is not None:
            fg, fg_v_px, cx, cy, rx, ry = parallax
            dfg = disp_profile(fg_v_px, kind, twos); xf = (fg.size[0] - W - 20) - np.concatenate([[0], np.cumsum(dfg)])
            b = window(fg, xf[i], y0)
            yy, xx = np.mgrid[0:H, 0:W]
            # blob anchored in the foreground layer's own coordinates, so it moves with the foreground layer
            m = (((xx + xf[i] - cx) / rx) ** 2 + ((yy + y0 - cy) / ry) ** 2) < 1
            a = np.where(m[..., None], b, a)
        if noise > 0 and rng is not None:
            a = np.clip(a.astype(np.float32) + rng.normal(0, noise, a.shape[:2])[..., None], 0, 255).astype(np.uint8)
        frames.append(a)
    return np.stack(frames), d

def via_h264(frames, work, crf=18):
    mp4 = os.path.join(work, f"v_{os.getpid()}.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", str(crf), "-pix_fmt", "yuv420p", mp4], stdin=subprocess.PIPE)
    p.stdin.write(frames.tobytes()); p.stdin.close(); p.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    os.remove(mp4); return np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W, 3)

if __name__ == "__main__":
    src_dir, outp, work = sys.argv[1:4]
    variants = (sys.argv[4] if len(sys.argv) > 4 else "clean,grain_h264,twos,ease,parallax").split(",")
    prefixes = (sys.argv[5] if len(sys.argv) > 5 else "p1,p2,p3").split(",")
    os.makedirs(work, exist_ok=True); rng = np.random.default_rng(7)
    pr_files = {p: next(f for f in sorted(os.listdir(src_dir)) if f.startswith(p) and f.endswith("_4k.png")) for p in prefixes}
    for pr, fn in pr_files.items():
        src = Image.open(os.path.join(src_dir, fn)).convert("RGB")
        other = Image.open(os.path.join(src_dir, pr_files[prefixes[(prefixes.index(pr) + 1) % len(prefixes)]])).convert("RGB")
        for var in variants:
            for sp in SPEEDS:
                t0 = time.time(); vpk = sp * W / FPS
                if var == 'parallax' and sp < 0.2: continue       # foreground = the speed under test, background fixed at 0.10 fw/s
                kw = dict(); kind = 'ease' if var == 'ease' else 'linear'
                if var == 'parallax':
                    # background at 0.10 fw/s, foreground blob at the tested speed
                    fr, d = make_clip(src, 0.10 * W / FPS, kind, parallax=(other, vpk, 1500, 1080, 520, 380))
                    truth_px = vpk
                else:
                    fr, d = make_clip(src, vpk, kind, twos=(var == 'twos'), noise=2.0 if var == 'grain_h264' else 0.0, rng=rng)
                    truth_px = vpk
                if var == 'grain_h264': fr = via_h264(fr, work)
                L = luma(fr)
                s, res = pe.pan_audit(L, fps=FPS)
                rec = dict(print=pr, variant=var, speed_fw_s=round(sp, 4), truth_px=truth_px, est_peak_px=s['peak_px'], est_peak_med5_px=s['peak_med5_px'], est_median_px=s['median_px'], fast_px=[round(float(x), 3) for x in res['fast']],
                           est_peak_fw_s=s['peak_fw_s'], valid_frac=s['valid_frac'], twos_detected=s['twos'], verdict=s['verdict'], limit_px=s['limit_px'],
                           err_peak_px=s['peak_px'] - truth_px, err_median_px=(s['median_px'] - (truth_px if kind == 'linear' else float('nan'))),
                           secs=round(time.time() - t0, 1))
                open(outp, "a").write(json.dumps(rec) + "\n"); print(rec, flush=True)
