"""Pan ease classifier (round 2, 2026-10-18): velocity curve from the phase-correlation vectors -> ease class, so MO1b and MO2 can stop reporting
`unknown` for pans and MO9 can count pan families from pixels.

  python3 -I pan_ease_classifier.py clip.mp4 [fps]      -> one JSON line (class, family, family_key, fit errors, holds, speeds)
  from pan_ease_classifier import classify_pan, family_key, mo9_check

Pipeline: pan_estimator.estimate_pan (tiled phase correlation, fastest textured layer per frame pair, twos handled with dt=2) -> signed velocity along the
principal axis -> 3-point median (drops one-frame spikes and dropouts) -> position curve p(t) = cumsum(v), normalised to [0, 1] -> least-squares fit of a library
of named easing curves, each allowed a hold at the start (a) and at the end (b): p(t) ~ T(clip((t - a)/(b - a), 0, 1)). The best template gives the class
(for example power2.out); its family gives the six-way label used by MO2 (in-out, out, in, settle, linear, plus the holds a and b).
A second, template-free rule (ends, peak position, reverse travel) cross-checks the family. Disagreement or a small margin sets low_confidence.

Conventions. Velocity is px per OUTPUT frame, +x = content moves right = camera pans LEFT (pan_estimator's convention), +y = content moves down = camera tilts UP.
Family key (playbook, MO9) = (ease family, axis, duration bucket, magnitude bucket): axis in {pan left, pan right, tilt up, tilt down}; duration buckets '<3', '3-6', '>6' s;
magnitude buckets '<3', '3-6', '>6' % of the frame width (pans) or height (tilts).
Needs numpy and ffmpeg (CLI only). Keep beside pan_estimator.py."""
import os, sys, json, math, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pan_estimator as pe

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


# ----------------------------------------------------------------------------- template library (GSAP names)
def _pow_in(n):  return lambda u: u ** n
def _pow_out(n): return lambda u: 1 - (1 - u) ** n
def _pow_inout(n): return lambda u: np.where(u < 0.5, 0.5 * (2 * u) ** n, 1 - 0.5 * (2 * (1 - u)) ** n)
def _back_out(c1=1.70158):
    c3 = c1 + 1
    return lambda u: 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2
_EXPO_N = 1 - 2.0 ** -10
TEMPLATES = {
    "none (linear)": (lambda u: u, "linear"),
    "sine.in": (lambda u: 1 - np.cos(u * np.pi / 2), "in"),
    "sine.out": (lambda u: np.sin(u * np.pi / 2), "out"),
    "sine.inOut": (lambda u: 0.5 - 0.5 * np.cos(np.pi * u), "in-out"),
    "power1.in": (_pow_in(2), "in"), "power1.out": (_pow_out(2), "out"), "power1.inOut": (_pow_inout(2), "in-out"),
    "power2.in": (_pow_in(3), "in"), "power2.out": (_pow_out(3), "out"), "power2.inOut": (_pow_inout(3), "in-out"),
    "power3.in": (_pow_in(4), "in"), "power3.out": (_pow_out(4), "out"), "power3.inOut": (_pow_inout(4), "in-out"),
    "power4.out": (_pow_out(5), "out"), "power4.inOut": (_pow_inout(5), "in-out"),
    "expo.out": (lambda u: (1 - 2.0 ** (-10 * u)) / _EXPO_N, "out"),
    "smootherstep": (lambda u: 6 * u ** 5 - 15 * u ** 4 + 10 * u ** 3, "in-out"),
    "smoothstep": (lambda u: 3 * u ** 2 - 2 * u ** 3, "in-out"),     # a cubic Hermite with zero end slopes: FilmCraft's bezier/autoBezier on two keyframes; Blender auto-clamped Bezier (round 2)
    "back.out(1.7)": (_back_out(), "settle"),
}
GRID_A = np.arange(0.0, 0.601, 0.025)
GRID_B = np.arange(0.40, 1.001, 0.025)
HOLD_PENALTY = 0.02          # prefers no hold when the fit is equal


# ----------------------------------------------------------------------------- velocity series
def principal_velocity(res):
    """Signed speed along the principal axis (px per output frame) from the fastest-layer vectors of pan_estimator.estimate_pan."""
    M = np.stack([res["vx"], res["vy"]], 1).astype(float)
    if not np.any(np.abs(M) > 1e-6):
        return np.zeros(len(M)), np.array([1.0, 0.0])
    _, _, vt = np.linalg.svd(M, full_matrices=False)
    e = vt[0]
    v = M @ e
    if v.sum() < 0:
        e, v = -e, -v
    return v, e


def clean(v, k=3):
    if len(v) < 5: return v
    p = np.pad(v, (k // 2, k // 2), mode="edge")
    return np.array([np.median(p[i:i + k]) for i in range(len(v))])


def fit_templates(v, templates=TEMPLATES):
    """Least-squares fit of every template to the normalised position curve. Returns a list sorted by error."""
    p = np.concatenate([[0.0], np.cumsum(v)])
    total = p[-1]
    if abs(total) < 1e-9:
        return [], p, total
    pn = p / total
    t = np.linspace(0, 1, len(p))
    out = []
    for name, (fn, fam) in templates.items():
        best = (9.0, 0.0, 1.0)
        for a in GRID_A:
            for b in GRID_B:
                if b - a < 0.25: continue
                u = np.clip((t - a) / (b - a), 0, 1)
                err = float(np.sqrt(np.mean((pn - fn(u)) ** 2))) + HOLD_PENALTY * (a + (1 - b))
                if err < best[0]: best = (err, float(a), float(b))
        out.append(dict(name=name, family=fam, rmse=round(best[0], 4), hold_lead=best[1], hold_trail=round(1 - best[2], 3)))
    out.sort(key=lambda r: r["rmse"])
    return out, p, total


def feature_family(v):
    """Template-free cross-check. Uses the moving part only (|v| above 5% of peak)."""
    s = np.abs(v).max()
    if s < 1e-9: return "static", {}
    act = np.where(np.abs(v) > 0.05 * s)[0]
    w = v[act[0]:act[-1] + 1] / s
    n = len(w); a = max(2, int(0.15 * n))
    ends_lo, ends_hi = float(np.abs(w[:a]).mean()), float(np.abs(w[-a:]).mean())
    peak = float(np.abs(w).argmax() / max(n - 1, 1))
    rev = float(-w[w < 0].sum() / max(w[w > 0].sum(), 1e-9))
    cv = float(np.abs(w).std() / max(np.abs(w).mean(), 1e-9))
    f = dict(start=round(ends_lo, 2), end=round(ends_hi, 2), peak_pos=round(peak, 2), reverse=round(rev, 3), cv=round(cv, 2))
    if rev > 0.02 and peak < 0.5: return "settle", f
    if cv < 0.12: return "linear", f
    if ends_lo < 0.5 and ends_hi < 0.5: return "in-out", f
    if ends_hi < 0.5 <= ends_lo: return "out", f
    if ends_lo < 0.5 <= ends_hi: return "in", f
    return "other", f


# ----------------------------------------------------------------------------- family key and MO9
def bucket_dur(s): return "<3" if s < 3 else ("3-6" if s <= 6 else ">6")
def bucket_mag(p): return "<3" if p < 3 else ("3-6" if p <= 6 else ">6")
def family_key(family, axis, dur_s, mag_pct): return f"{family}|{axis}|{bucket_dur(dur_s)}|{bucket_mag(mag_pct)}"


def mo9_check(keys, held=None, window=8, min_distinct=3, max_share=0.40, max_run=2, min_entropy=1.5):
    """MO9 chapter rule over every run of `window` consecutive moving shots. `keys` is a list of family keys (None or 'none' = held shot, ignored here;
    pass held=[bool,...] if the held-shot share (>= 35% of photo shots) should be reported too)."""
    ks = [k for k in keys if k and k != "none"]
    res = []
    for i in range(0, max(1, len(ks) - window + 1)):
        w = ks[i:i + window]
        if len(w) < window: break
        cnt = {k: w.count(k) for k in set(w)}
        share = max(cnt.values()) / window
        H = -sum((c / window) * math.log2(c / window) for c in cnt.values())
        run = max_r = 1
        for j in range(1, window):
            run = run + 1 if w[j] == w[j - 1] else 1
            max_r = max(max_r, run)
        res.append(dict(start=i, distinct=len(cnt), top_share=round(share, 2), entropy_bits=round(H, 2), longest_run=max_r,
                        ok=bool(len(cnt) >= min_distinct and share <= max_share and max_r <= max_run and H >= min_entropy)))
    out = dict(windows=res, ok=all(r["ok"] for r in res) if res else None, moving_shots=len(ks))
    if held is not None and len(held):
        out["held_share"] = round(float(np.mean(held)), 2); out["held_ok"] = bool(np.mean(held) >= 0.35)
    return out


def mo_verdicts(c, brief_family=None, drift_declared=False):
    """MO1b and MO2 for a pan, from classify_pan()'s dict. brief_family in {in-out, out, in, settle, drift, hold-snap} (the six families of the playbook).
    MO1b: pass unless the move is linear and no drift was declared; 'unknown' only if the template fit and the template-free rule disagree about linear vs eased.
    MO2: measured family equals the brief's; drift <-> linear; hold-snap <-> a hold of 25% of the clip or more at either end; 'unknown' when the two rules disagree."""
    if c.get("cls") == "static":
        return dict(MO1b="unknown", MO2="unknown", why="static")
    lin = [c["family"] == "linear", c["feature_family"] == "linear"]
    if lin[0] != lin[1]: mo1b = "unknown"
    else: mo1b = "pass" if (not lin[0] or drift_declared) else "fail"
    out = dict(MO1b=mo1b)
    if brief_family is None: out["MO2"] = "not asked"; return out
    held = c["hold_lead_frac"] >= 0.25 or c["hold_trail_frac"] >= 0.25
    measured = "hold-snap" if held else ("drift" if c["family"] == "linear" else c["family"])
    out["measured_family"] = measured
    if not c["agree"] and not held: out["MO2"] = "unknown"
    else: out["MO2"] = "pass" if measured == brief_family else "fail"
    return out


# ----------------------------------------------------------------------------- main entry points
def classify_pan(res, fps=24.0, min_peak_px=0.5):
    """res = pan_estimator.estimate_pan(...) result (or pan_audit()[1]). Returns the classification dict."""
    v, e = principal_velocity(res)
    n_pairs = len(v); dt = res.get("dt", 1)
    frames = n_pairs + dt
    W, H = res["W"], res["H"]
    vs = clean(v)
    peak = float(np.abs(vs).max()) if n_pairs else 0.0
    out = dict(frames=int(frames), dt=int(dt), axis_vec=[round(float(e[0]), 3), round(float(e[1]), 3)], peak_px=round(peak, 3), peak_fw_s=round(peak * fps / W, 4))
    if peak < min_peak_px:
        out.update(cls="static", family="none", low_confidence=False, note="peak speed under 0.5 px/frame: nothing to classify")
        return out
    fits, p, total = fit_templates(vs)
    best, second = fits[0], fits[1]
    # family of the best template; runner-up from a different FAMILY gives the margin
    other = next((f for f in fits if f["family"] != best["family"]), second)
    margin = (other["rmse"] - best["rmse"]) / max(other["rmse"], 1e-9)
    ff, feats = feature_family(vs)
    horiz = abs(e[0]) >= abs(e[1])
    if horiz: axis = "pan left" if e[0] > 0 else "pan right"            # content moves right => camera pans left
    else:     axis = "tilt up" if e[1] > 0 else "tilt down"
    extent = abs(float(total))
    mag_pct = 100.0 * extent / (W if horiz else H)
    dur_s = frames / fps
    low = bool(best["rmse"] > 0.05 or margin < 0.15 or ff != best["family"])
    out.update(cls=best["name"], family=best["family"], rmse=best["rmse"], runner_up=second["name"], runner_up_rmse=second["rmse"],
               best_other_family=other["name"], margin_other_family=round(float(margin), 3),
               hold_lead_frac=best["hold_lead"], hold_trail_frac=best["hold_trail"], feature_family=ff, features=feats, agree=bool(ff == best["family"]),
               low_confidence=low, axis=axis, total_px=round(extent, 1), mag_pct=round(mag_pct, 2), dur_s=round(dur_s, 2),
               family_key=family_key(best["family"], axis, dur_s, mag_pct))
    return out


def classify_clip(gray_frames, fps=24.0):
    """gray_frames: float/uint8 (N, 1080, 1920) luma. Detects footage on twos, estimates, classifies."""
    s, res = pe.pan_audit(gray_frames.astype(np.float32), fps=fps)
    c = classify_pan(res, fps=fps)
    c["twos"] = bool(s["twos"]); c["mo6_verdict"] = s["verdict"]; c["mo6_peak_px"] = round(s["peak_px"], 2)
    return c


if __name__ == "__main__":
    path = sys.argv[1]; fps = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
    r = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", "scale=1920:1080:flags=bicubic,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, 1080, 1920)
    print(json.dumps(classify_clip(fr, fps)))
