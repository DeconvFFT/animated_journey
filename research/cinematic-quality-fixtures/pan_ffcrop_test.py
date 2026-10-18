"""Independent generator for the pan estimator: ffmpeg's own `crop` filter walking over a 4K scan, so the test footage is not
made by the same code (Pillow Lanczos) as the estimator tests. crop x is an expression; ffmpeg truncates it to whole pixels, so a
non-integer speed produces uneven 11/12 px steps. Usage: python3 -I pan_ffcrop_test.py SRC_PNG OUT_JSONL"""
import sys, os, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pan_estimator as pe
W, H, FPS, N = 1920, 1080, 24, 40
LUMA = np.array([0.299, 0.587, 0.114], np.float32)
src, outp = sys.argv[1:3]
for sp in (0.10, 1 / 7, 0.20, 0.30):
    v = sp * W / FPS
    vf = f"crop=1920:1080:x='1900-{v}*n':y=540,format=rgb24"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", src, "-vf", vf, "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(N, H, W, 3).astype(np.float32) @ LUMA
    s, res = pe.pan_audit(fr, fps=FPS)
    steps = res['fast'][:12].round(2).tolist()
    rec = dict(generator="ffmpeg crop (integer x)", speed_fw_s=round(sp, 4), truth_mean_px=v, est_peak_px=s['peak_px'], est_peak_med5_px=s['peak_med5_px'], est_median_px=s['median_px'], verdict=s['verdict'], first_steps=steps)
    open(outp, "a").write(json.dumps(rec) + "\n"); print(rec, flush=True)
