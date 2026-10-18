"""MO6 pan-speed estimator: tiled phase correlation with sub-pixel peak refinement (numpy only).
Public API:
  estimate_pan(frames, fps=24, tiles=(3,3), ...) -> dict with per-pair tile velocities and clip-level numbers
  frames: float32 array (N, H, W) of luma (0..255), frames must be consecutive output frames.
Velocity convention: px per OUTPUT frame, +x = content moves right (camera pans left). Speeds are reported as
frame widths per second = |v| * fps / W  (MO6 limit 0.143 = 11.43 px/frame at 1920 wide, 24 fps).
"""
import numpy as np

def _win(h, w, alpha=0.5):
    def tuk(n):
        x = np.linspace(0, 1, n); w_ = np.ones(n)
        r = alpha / 2
        lo = x < r; hi = x > 1 - r
        w_[lo] = 0.5 * (1 + np.cos(np.pi * (x[lo] / r - 1)))
        w_[hi] = 0.5 * (1 + np.cos(np.pi * ((x[hi] - 1 + r) / r)))
        return w_
    return np.outer(tuk(h), tuk(w)).astype(np.float32)

def _band(h, w, f0):
    fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.fftfreq(w)[None, :]
    return np.exp(-((fy ** 2 + fx ** 2) / (f0 ** 2))).astype(np.float32)

def _wrap(i, n): return i - n if i > n // 2 else i

def _refine(R, py, px, h, w, half=1.0, step=0.05):
    """Upsampled-DFT local search (Guizar-Sicairos style) of the correlation surface around the integer peak."""
    ys = py + np.arange(-half, half + 1e-9, step); xs = px + np.arange(-half, half + 1e-9, step)
    fy = np.fft.fftfreq(h); fx = np.fft.fftfreq(w)
    Ey = np.exp(2j * np.pi * np.outer(ys, fy)).astype(np.complex64)      # (Ny, h)
    Ex = np.exp(2j * np.pi * np.outer(fx, xs)).astype(np.complex64)      # (w, Nx)
    S = (Ey @ R @ Ex).real
    iy, ix = np.unravel_index(S.argmax(), S.shape)
    # parabolic polish on the fine grid
    def par(m, p):
        d = m[p - 1] - 2 * m[p] + m[p + 1]
        return 0.0 if d == 0 else 0.5 * (m[p - 1] - m[p + 1]) / d
    dy = par(S[:, ix], iy) if 0 < iy < S.shape[0] - 1 else 0.0
    dx = par(S[iy, :], ix) if 0 < ix < S.shape[1] - 1 else 0.0
    return ys[iy] + dy * step, xs[ix] + dx * step, float(S[iy, ix]) / (h * w)

def _peaks(R, h, w, n_peaks=2, excl=4, excl2=9, f_refine=True, psr_gate=0.0):
    r = np.fft.ifft2(R).real
    out = []; rr = r.copy()
    for k in range(n_peaks):
        e = excl if k == 0 else excl2
        py, px = np.unravel_index(rr.argmax(), rr.shape); val = float(r[py, px])
        # a second peak must be a genuine local maximum of the surface, not the skirt of the first peak
        if k > 0:
            nb = r[np.ix_((np.arange(py - 1, py + 2) % h), (np.arange(px - 1, px + 2) % w))]
            if val < nb.max() - 1e-12 * abs(val): break
        m = np.ones(r.shape, bool)   # sidelobe statistics over the ORIGINAL surface, excluding the first peak's neighbourhood
        ys0 = (np.arange(py - excl, py + excl + 1) % h); xs0 = (np.arange(px - excl, px + excl + 1) % w)
        m[np.ix_(ys0, xs0)] = False
        side = r[m]; psr = (val - side.mean()) / (side.std() + 1e-12)
        sy, sx = _wrap(int(py), h), _wrap(int(px), w)
        if f_refine and psr >= psr_gate: ry, rx, pv = _refine(R, sy, sx, h, w)
        else: ry, rx, pv = float(sy), float(sx), val
        out.append(dict(vy=ry, vx=rx, peak=val, psr=float(psr)))
        ys = (np.arange(py - e, py + e + 1) % h); xs = (np.arange(px - e, px + e + 1) % w)
        rr[np.ix_(ys, xs)] = -1e9
    return out

def tile_grid(H, W, tiles):
    ty, tx = tiles; th, tw = H // ty, W // tx
    return [(i * th, (i + 1) * th, j * tw, (j + 1) * tw) for i in range(ty) for j in range(tx)]

def estimate_pan(frames, fps=24, tiles=(3, 3), dt=1, band=0.22, min_psr=10.0, min_tex=0.3, second_peak=0.5):
    """Return dict(pairs=[{t, tiles:[{box, peaks:[...]}]}], fast=array(T) per-pair fastest textured |v| (px/frame),
    vx=array(T) signed vx of that tile). dt=spacing between compared frames (use 2 for footage on twos)."""
    N, H, W = frames.shape
    boxes = tile_grid(H, W, tiles)
    th, tw = boxes[0][1] - boxes[0][0], boxes[0][3] - boxes[0][2]
    win = _win(th, tw); bw = _band(th, tw, band)
    def prep(f):
        out = []
        for (y0, y1, x0, x1) in boxes:
            t = f[y0:y1, x0:x1].astype(np.float32)
            tex = float(np.abs(np.gradient(t)[1]).mean() + np.abs(np.gradient(t)[0]).mean())
            t = (t - t.mean()) * win
            out.append((np.fft.fft2(t), tex))
        return out
    F = [prep(frames[i]) for i in range(N)]
    pairs = []; fast = []; fvx = []; fvy = []; conf = []; ngoods = []
    for t in range(N - dt):
        tl = []; best = (0.0, 0.0, 0.0, 0.0); ng = 0
        for k, (box) in enumerate(boxes):
            Fa, tex = F[t][k]; Fb, _ = F[t + dt][k]
            R = np.conj(Fa) * Fb; R = R / (np.abs(R) + 1e-3 * np.abs(R).max() + 1e-12); R = R * bw
            # conj(Fa)*Fb puts the correlation peak at +s when b(x) = a(x - s), i.e. content moved by +s (to the right)
            pk = _peaks(R, th, tw, n_peaks=2, psr_gate=min_psr)
            good = [p for p in pk if p['psr'] >= min_psr and tex >= min_tex]
            if len(good) == 2 and good[1]['peak'] < second_peak * good[0]['peak']: good = good[:1]
            tl.append(dict(box=box, tex=tex, peaks=pk, good=good)); ng += len(good)
            for p in good:
                s = np.hypot(p['vx'], p['vy']) / dt
                if s > best[0]: best = (s, p['vx'] / dt, p['vy'] / dt, p['psr'])
        pairs.append(tl); ngoods.append(ng); fast.append(best[0]); fvx.append(best[1]); fvy.append(best[2]); conf.append(best[3])
    return dict(pairs=pairs, fast=np.array(fast), vx=np.array(fvx), vy=np.array(fvy), psr=np.array(conf), ngood=np.array(ngoods), H=H, W=W, fps=fps, dt=dt)

def detect_twos(frames, tiles=(3, 3)):
    """True if every other frame pair is (near) identical: step 1 returns alternating ~0 / ~2v."""
    d = np.array([np.abs(frames[i + 1].astype(np.int16) - frames[i].astype(np.int16)).mean() for i in range(len(frames) - 1)])
    ev, od = d[0::2].mean(), d[1::2].mean()
    return bool(min(ev, od) < 0.05 * max(ev, od) and max(ev, od) > 0.0)

def summarise(res, smooth=5):
    """Clip-level numbers. peak_px = peak of the 5-frame running MEAN of the fastest textured layer's speed (px/frame); peak_med5_px = same with a
    running median. Mean is used for the verdict so that integer-rounded camera paths (steps of 11 and 12 px for a true 11.43) are judged on their
    average speed; a large gap between the two (or the per-frame list) shows uneven steps, which is MO8's job, not MO6's."""
    f = res['fast']; k = smooth
    p = np.pad(f, (k // 2, k // 2), mode='edge')
    med = np.array([np.median(p[i:i + k]) for i in range(len(f))]); mean = np.array([p[i:i + k].mean() for i in range(len(f))])
    W, fps = res['W'], res['fps']; nz = f[f > 1e-3]
    return dict(peak_px=float(mean.max()), peak_med5_px=float(med.max()), median_px=float(np.median(nz)) if len(nz) else 0.0,
                peak_fw_s=float(mean.max() * fps / W), median_fw_s=float((np.median(nz) if len(nz) else 0.0) * fps / W),
                valid_frac=float((res['ngood'] > 0).mean()), moving_frac=float((f > 1e-3).mean()), max_single_px=float(f.max()))

def pan_audit(frames, fps=24, tiles=(3, 3), limit_fw_s=1 / 7, tol_px=0.3, min_valid=0.5):
    """MO6 audit: auto-detect footage on twos, estimate, compare the peak with the limit.
    Verdicts: PASS / FAIL / INCONCLUSIVE (fewer than min_valid of the frame pairs had a confident textured tile: fades, flat frames, strong zoom)."""
    twos = detect_twos(frames)
    res = estimate_pan(frames, fps=fps, tiles=tiles, dt=2 if twos else 1)
    s = summarise(res); W = res['W']
    limit_px = limit_fw_s * W / fps
    s.update(twos=twos, limit_px=limit_px)
    s['borderline'] = bool(abs(s['peak_px'] - limit_px) <= 0.5)   # within 0.5 px of the limit: look at it by eye
    s['verdict'] = 'INCONCLUSIVE' if s['valid_frac'] < min_valid else ('PASS' if s['peak_px'] <= limit_px + tol_px else 'FAIL')
    return s, res


if __name__ == "__main__":
    # python3 -I pan_estimator.py clip.mp4 [fps]   -> one JSON line: verdict, peak speed (px/frame and frame widths/s), per-pair speeds
    import sys, json, subprocess
    path = sys.argv[1]; fps = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
    Wd, Hd = 1920, 1080
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={Wd}:{Hd}:flags=bicubic,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, Hd, Wd)
    s, res = pan_audit(fr, fps=fps)
    s["frames"] = int(len(fr)); s["fast_px"] = [round(float(x), 3) for x in res["fast"]]
    print(json.dumps(s))
