"""Validate pan_ease_classifier.py on synthetic pans with KNOWN easing, cut from a 4K print at 1:1 (so every sub-pixel shift is a Lanczos resample).
  python3 -I pan_ease_validate.py SRC_4K.png OUT.jsonl [treatments comma list] [eases comma list] [N=96] [tag]
Treatments: clean | grain_h264 (sigma 2 noise + H.264 CRF 18) | twos (one drawing per two frames) | int_steps (camera path rounded to whole pixels, like ffmpeg crop)
            | parallax (two layers: background at half the speed of the foreground ellipse, same ease) | tilt (vertical move, clean) | left (opposite direction, clean)
Each clip is normalised to a PEAK speed of 11 px/frame (env PEAK_PX overrides) (0.1375 frame widths per second, just under the MO6 limit) so the estimator works in its validated regime.
One JSON line per clip: truth (ease, hold lead/trail, total px) against the classifier's answer."""
import sys, os, json, time, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pan_estimator as pe
import pan_ease_classifier as pc
W, H, FPS = 1920, 1080, 24
LUMA = np.array([0.299, 0.587, 0.114], np.float32)
PEAK = float(os.environ.get("PEAK_PX", "11.0"))      # peak per-frame step in px (set PEAK_PX=3 for slow drifts)

# truth eases: (name, function, family)
TRUTH = {k: v for k, v in pc.TEMPLATES.items()}
HOLDS = {  # name -> (base template, hold_lead, hold_trail)
    "hold25+power2.inOut": ("power2.inOut", 0.25, 0.0),
    "power2.out+hold25": ("power2.out", 0.0, 0.25),
}
DEFAULT_EASES = ["none (linear)", "sine.inOut", "power1.inOut", "power2.inOut", "power3.inOut", "smootherstep", "sine.out", "power1.out", "power2.out",
                 "power3.out", "expo.out", "sine.in", "power2.in", "back.out(1.7)", "hold25+power2.inOut", "power2.out+hold25"]

CSS = {  # CSS timing functions (out of the classifier's template library) -> (control points, family by the CSS name's own meaning)
    "css:ease": ((0.25, 0.1, 0.25, 1.0), "in-out"), "css:ease-in": ((0.42, 0.0, 1.0, 1.0), "in"), "css:ease-out": ((0.0, 0.0, 0.58, 1.0), "out"),
    "css:ease-in-out": ((0.42, 0.0, 0.58, 1.0), "in-out"), "css:back-out": ((0.34, 1.56, 0.64, 1.0), "settle"),
}
def cubic_bezier(x1, y1, x2, y2):
    def f(u):
        u = np.asarray(u, float); out = np.empty_like(u)
        for k, ui in enumerate(u):
            lo, hi = 0.0, 1.0
            for _ in range(50):
                s = (lo + hi) / 2
                x = 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s ** 2 * x2 + s ** 3
                if x < ui: lo = s
                else: hi = s
            s = (lo + hi) / 2
            out[k] = 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s ** 2 * y2 + s ** 3
        return out
    return f

def curve(name, N):
    """Normalised position curve p_i in [0,1] (can exceed 1 for back.out) and its (a, b) hold interval."""
    a = b0 = 0.0; base = name; lead = trail = 0.0
    if name in HOLDS: base, lead, trail = HOLDS[name]
    fn = cubic_bezier(*CSS[name][0]) if name in CSS else TRUTH[base][0]
    t = np.linspace(0, 1, N)
    u = np.clip((t - lead) / ((1 - trail) - lead), 0, 1)
    return np.asarray(fn(u), float), lead, trail

def total_for_peak(p, peak=PEAK):
    d = np.abs(np.diff(p)).max()
    return peak / d                       # total px so that the largest per-frame step equals `peak`

def window(src, x0, y0): return np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + W, y0 + H)), dtype=np.uint8)
def crop_int(src, x0, y0):
    x0 = int(round(x0)); y0 = int(round(y0)); return np.asarray(src.crop((x0, y0, x0 + W, y0 + H)), dtype=np.uint8)
def luma(a): return a.astype(np.float32) @ LUMA

def via_h264(frames, work, crf=18):
    mp4 = os.path.join(work, f"v_{os.getpid()}.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", str(crf), "-pix_fmt", "yuv420p", mp4], stdin=subprocess.PIPE)
    pr.stdin.write(frames.tobytes()); pr.stdin.close(); pr.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    os.remove(mp4); return np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W, 3)

def make(src, other, ease, treat, N, rng):
    sw, sh = src.size
    p, lead, trail = curve(ease, N)
    D = total_for_peak(p)
    if treat == "twos":                   # one drawing per two output frames: same camera path, positions held on odd frames
        p = p[(np.arange(N) // 2) * 2]
    pos = p * D
    vertical = treat == "tilt"; left = treat == "left"
    span = (sh - H - 20) if vertical else (sw - W - 20)
    assert pos.max() - pos.min() < span, (ease, treat, pos.max() - pos.min(), span)
    # content moves toward +x (right) when the window moves left; "left" treatment is the opposite
    start = span if not left else 10
    sign = -1 if not left else +1
    frames = []
    for i in range(len(pos)):
        x = start + sign * pos[i]
        if treat == "int_steps": a = crop_int(src, x, (sh - H) // 2) if not vertical else crop_int(src, (sw - W) // 2, x)
        elif vertical: a = window(src, (sw - W) // 2, x)
        else: a = window(src, x, (sh - H) // 2)
        if treat == "parallax":
            xs2 = (other.size[0] - W - 20) - 2.0 * pos[i]            # foreground layer moves at 2x the background displacement, same ease
            b = window(other, xs2, (other.size[1] - H) // 2)
            yy, xx = np.mgrid[0:H, 0:W]
            m = (((xx + xs2 - 1500) / 520) ** 2 + ((yy + (other.size[1] - H) // 2 - 1080) / 380) ** 2) < 1
            a = np.where(m[..., None], b, a)
        if treat == "grain_h264": a = np.clip(a.astype(np.float32) + rng.normal(0, 2.0, a.shape[:2])[..., None], 0, 255).astype(np.uint8)
        frames.append(a)
    fr = np.stack(frames)
    return fr, p, D, lead, trail

if __name__ == "__main__":
    src_path, outp = sys.argv[1:3]
    treats = (sys.argv[3] if len(sys.argv) > 3 else "clean,grain_h264,twos,int_steps").split(",")
    eases = (sys.argv[4] if len(sys.argv) > 4 else ",".join(DEFAULT_EASES)).split(",")
    N = int(sys.argv[5]) if len(sys.argv) > 5 else 96
    tag = sys.argv[6] if len(sys.argv) > 6 else os.path.basename(src_path)
    work = os.path.dirname(os.path.abspath(outp)); rng = np.random.default_rng(11)
    src = Image.open(src_path).convert("RGB")
    other_path = os.environ.get("OTHER_4K")
    other = Image.open(other_path).convert("RGB") if other_path else src.transpose(Image.FLIP_LEFT_RIGHT)
    for treat in treats:
        for ease in eases:
            t0 = time.time()
            fr, p, D, lead, trail = make(src, other, ease, treat, N, rng)
            if treat == "grain_h264": fr = via_h264(fr, work)
            c = pc.classify_clip(luma(fr), FPS)
            truth_fam = (CSS[ease][1] if ease in CSS else (TRUTH[HOLDS[ease][0]][1] if ease in HOLDS else TRUTH[ease][1]))
            truth_cls = HOLDS[ease][0] if ease in HOLDS else ease
            truth_axis = {"tilt": "tilt up", "left": "pan right"}.get(treat, "pan left")
            rec = dict(src=tag, treat=treat, N=N, peak_px_truth=PEAK, truth=truth_cls, truth_family=truth_fam, truth_hold_lead=lead, truth_hold_trail=trail,
                       truth_total_px=round(float(D * p[-1] * (2.0 if treat == "parallax" else 1.0)), 1), truth_axis=truth_axis,
                       est=c.get("cls"), est_family=c.get("family"), est_hold_lead=c.get("hold_lead_frac"), est_hold_trail=c.get("hold_trail_frac"),
                       rmse=c.get("rmse"), runner_up=c.get("runner_up"), margin_other_family=c.get("margin_other_family"), feature_family=c.get("feature_family"),
                       agree=c.get("agree"), low_confidence=c.get("low_confidence"), est_axis=c.get("axis"), est_total_px=c.get("total_px"), est_peak_px=c.get("peak_px"),
                       twos_detected=c.get("twos"), mo6_verdict=c.get("mo6_verdict"), family_key=c.get("family_key"),
                       family_ok=bool(c.get("family") == truth_fam), class_ok=bool(c.get("cls") == truth_cls), axis_ok=bool(c.get("axis") == truth_axis),
                       secs=round(time.time() - t0, 1))
            open(outp, "a").write(json.dumps(rec) + "\n")
            print(treat, ease, "->", c.get("cls"), c.get("family"), "family_ok" if rec["family_ok"] else "FAMILY_MISS", rec["secs"], "s", flush=True)
