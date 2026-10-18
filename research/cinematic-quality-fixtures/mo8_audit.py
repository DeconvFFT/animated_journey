"""MO8 audit of ANY push or pull, whatever rendered it (round 2, 2026-10-18).
Reports the three numbers from FQ2 on the delivered file, plus the ease class of the zoom-rate curve.

  python3 -I mo8_audit.py clip.mp4 [clip2.mov ...]
  python3 -I mo8_audit.py frames_dir/            (a folder of numbered PNG frames, sorted by name; also reports the result after x264 CRF 14, key after_h264_crf14)
  options: --h264 (force the x264 pass for a video file), --no-h264 (skip it for a folder)

Output: one JSON line per input with
  mo8a_centre_jit_px   rms of the x,y translation residual (frame minus its 9-frame mean), in 1080p pixels   (limit 0.05, FQ2)
  mo8b_edge_jit_px     rms of the zoom-rate residual times half the frame width (960 px at 1080p)             (limit 0.04, FQ2)
  mo8c_rough           std(zoom-rate residual) / mean zoom rate                                               (informational, 0.10 at a 4% push over 4 s)
  mo8a_d4_px, mo8b_d4_px   the same two jitters from the 4th difference (round 2): curvature-free, so valid for any push duration; the 9-frame-mean versions above
                       contain the ease curve's own curvature and read too high for pushes shorter than about 3 s
  zoom_total_pct       total zoom estimated from the zoom-rate series (sum of per-pair rates)
  ease_features, ease_class   from zoom_velocity_classifier.features()/classify() (same rules as MO1b/MO2)
Frames are scaled to 1920x1080 before measuring (bicubic) when the file is another size, so the pixel numbers are 1080p-equivalent.
Needs ffmpeg, numpy, Pillow. Keep this file beside zoompan_vs_subpixel_prints.py and zoom_velocity_classifier.py.
Windows: use  py -3 -I mo8_audit.py clip.mp4  (or python -I).  The scripts call "ffmpeg" from PATH; set FFMPEG=C:\\path\\ffmpeg.exe to override."""
import os, sys, json, subprocess, glob
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zoompan_vs_subpixel_prints as zp        # analyse(), series(), metrics(), luma()
import zoom_velocity_classifier as zv          # features(), classify()

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
W, H = 1920, 1080


def load_video(path, w=W, h=H):
    r = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", f"scale={w}:{h}:flags=bicubic,format=rgb24", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3)


def load_dir(d, w=W, h=H):
    files = sorted(glob.glob(os.path.join(d, "*.png")))
    out = []
    for f in files:
        im = Image.open(f).convert("RGB")
        if im.size != (w, h):
            im = im.resize((w, h), Image.BICUBIC)
        out.append(np.asarray(im))
    return np.stack(out)


def via_h264(frames, crf=14):
    """Encode the frames with x264 (CRF 14, yuv420p, as in FQ2) and decode them again: the file the venue would play."""
    import tempfile
    fd, mp4 = tempfile.mkstemp(suffix=".mp4"); os.close(fd)
    try:
        p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "24", "-i", "-", "-c:v", "libx264",
                              "-crf", str(crf), "-pix_fmt", "yuv420p", mp4], stdin=subprocess.PIPE)
        p.stdin.write(np.ascontiguousarray(frames).tobytes()); p.stdin.close(); p.wait()
        return load_video(mp4)
    finally:
        try: os.remove(mp4)
        except OSError: pass


def d4_sigma(x):
    """White-jitter sigma from the 4th difference: var(d4) = 70 sigma^2 for white noise, and a smooth ease curve contributes almost nothing,
    so unlike the 9-frame running-mean residual (which also contains the curve's own curvature) it does not rise for short, fast pushes."""
    d = np.diff(np.asarray(x, float), 4)
    return float(np.sqrt(np.mean(d ** 2) / 70.0)) if len(d) else float("nan")


def luma_down(frames, f):
    """Luma, block-averaged by f, one frame at a time (same numbers as zp.down(zp.luma(frames), f), but about 3 GB less memory for 96 frames)."""
    n = len(frames); out = np.empty((n, H // f, W // f), np.float32)
    for i in range(n):
        l = frames[i].astype(np.float32) @ zp.LUMA
        out[i] = l.reshape(H // f, f, W // f, f).mean(axis=(1, 3)) if f > 1 else l
    return out


def audit(frames, f=4):
    """frames: uint8 (N,1080,1920,3). f = analysis down-scale (4 = 480x270, as in FQ2)."""
    P = zp.series(luma_down(frames, f), 1)     # columns: tx, ty, zoom-rate per frame pair (series() gets frames already down-scaled)
    m = zp.metrics(P, f)
    v = P[:, 2]
    feats = zv.features(v)
    return dict(frames=int(len(frames)),
                mo8a_centre_jit_px=round(float(np.hypot(m["tx_jit_px1080"], m["ty_jit_px1080"])), 4),
                tx_jit_px=round(m["tx_jit_px1080"], 4), ty_jit_px=round(m["ty_jit_px1080"], 4),
                mo8b_edge_jit_px=round(m["edge_jit_px1080"], 4),
                mo8c_rough=round(m["rough"], 4),
                mo8a_d4_px=round(float(np.hypot(d4_sigma(P[:, 0]) * f, d4_sigma(P[:, 1]) * f)), 4),
                mo8b_d4_px=round(d4_sigma(v) * (W / 2), 4),
                mean_zoom_rate=round(m["mean_speed"], 6),
                zoom_total_pct=round(float(100 * np.abs(v).sum()), 3),
                ease_features=feats, ease_class=zv.classify(feats))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force_h264 = "--h264" in sys.argv; skip_h264 = "--no-h264" in sys.argv
    for p in args:
        isdir = os.path.isdir(p)
        fr = load_dir(p) if isdir else load_video(p)
        rec = audit(fr)
        rec["input"] = os.path.basename(p.rstrip("/\\"))
        if (isdir or force_h264) and not skip_h264:      # frame folders are lossless: also report the file after x264 CRF 14
            rec["after_h264_crf14"] = audit(via_h264(fr))
        print(json.dumps(rec))
