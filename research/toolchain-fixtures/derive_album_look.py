#!/usr/bin/env python3
"""derive_album_look.py: turn sampled prints into one repeatable ffmpeg "album look".

Research fixture for research/toolchain.md, "Follow-up research (round 2)", section F14.
Written and run 2026-10-18 on Python 3.13, numpy 2.5, Pillow 12.3 (no other packages), ffmpeg 6.1.1.
Run it as:  python3 -I derive_album_look.py samples.json look.json
(-I keeps the script from importing anything out of the folder it sits in.)

WHAT IT DOES (the method, in the order the code does it)
 1. For each print in samples.json it reads three boxes (fractions of the image, so they survive a rescale):
      print_area  where the picture is (excludes scanner black, mat, border)
      white       a patch on a KNOWN-WHITE object (shirt, wall, paper, cloth)
      skin        a patch of skin in a midtone (cheek or forehead, not a highlight, not a shadow)
      flat        an even area (sky, painted wall) used only to measure grain
 2. It measures, in gamma-encoded sRGB 0..1 (the numbers a scanner file holds; no linearising):
      floor_c     per-channel 0.5th percentile of the picture after a 3x3 median (print black, lift)
      ceil_c      per-channel 99.5th percentile (print white level / roll-off)
      W, S        median RGB of the white and skin patches
      sigma_*     standard deviation of the flat patch after removing a best-fit plane (grain),
                  for luma and for R, G, B, plus the R-G residual correlation
 3. Cast = chromaticity of the white patch (unit vector W/|W|), NOT its brightness (a white shirt in shade is
    darker than the paper white). If the scan includes the print's own unprinted paper margin, put a "paper" box
    in samples.json: it replaces the in-scene white for the cast (no scene light in it). White level = the
    brightest channel's 99.5th percentile of the picture (median over the prints); black = per-channel 0.5th
    percentile. Percentiles are read from a box-averaged thumbnail so grain and dust do not bias them. So:
        white_c = cast_c / max(cast) * level,        black_c = floor_c
 4. It compares the white-patch cast with three automatic illuminant guesses (grey-world, max-RGB, shades-of-grey
    p=6) and prints the angular error in degrees. Use this to see whether a no-patch method could be trusted.
 5. It checks that the prints agree with each other (angle between their casts, spread of floors and grain).
    If they do not agree (cast angle over 3 degrees, floors over 0.06 apart, white levels over 0.08 apart) the flag
    ONE_ALBUM_LOOK is false and the numbers are for information only. The 3-degree and 0.06 / 0.08 limits are
    judgement, not a published standard: tune them once on the maker's own prints by eye.
 6. Skin is a CHECK, plus an optional anchor. After removing floor and white, the skin hue angle on a
    vectorscope (BT.709) should sit near the skin line (about 123 degrees). If the album's skin is far off,
    a straight black/white mapping is not enough (crossover) and the 3-point curve is needed (needs ref_skin).
 7. It writes look.json and an ffmpeg -vf string:
        colorlevels (exact black and white per channel)
        format=yuv444p, noise (luma grain, strength looked up from the measured table), format back,
        and, when the measured grain is spatially correlated (lag-1 autocorrelation of 0.3 or more), a second
        string "ffmpeg_filter_complex_soft_grain" that builds the grain at half or third size and scales it up.
    Same string -> same pixels (noise seed is fixed at ffmpeg's default 123457; checked: identical on ffmpeg
    6.1.1 Linux and 8.1.1 Windows, zero pixels differing).
    Not done here: the optional mid-tone anchor (a 3-point curve through the skin sample needs a reference skin
    value from the clean art; see the notes, F14.5). The skin sample is used as a check only.
"""
import json, math, sys
import numpy as np
from PIL import Image, ImageFilter

LUMA = np.array([0.2126, 0.7152, 0.0722])          # Rec.709 weights, applied to gamma-encoded values
SKIN_LINE_DEG = 123.0                                # the "I line" of a vectorscope, the usual skin guide
# ffmpeg 6.1.1, flat grey, format=yuv444p,noise=c0s=N:c0f=t+u -> measured luma sigma in 8-bit levels.
# Measured at grey 64, 128, 192 (identical at all three). Rebuild with calibrate_noise() if ffmpeg changes.
NOISE_TABLE = {1: 0.0, 2: 0.5, 3: 0.819, 4: 1.112, 5: 1.402, 6: 1.701, 7: 2.219, 8: 2.668, 9: 3.043,
               10: 3.42, 11: 3.754, 12: 4.082, 14: 4.735, 16: 5.333, 18: 5.938, 20: 6.695, 24: 8.066,
               28: 9.344, 32: 10.701, 40: 13.396}


def load(path, long_side=None):
    im = Image.open(path).convert("RGB")
    if long_side:
        s = long_side / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im


def crop_frac(arr, box):
    h, w = arr.shape[:2]
    x0, y0, x1, y1 = box
    return arr[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]


def luma(a):
    return a @ LUMA


def plane_residual(ch):
    """Residual of a best-fit plane (removes sky/wall gradient). ch is 2-D."""
    h, w = ch.shape
    yy, xx = np.mgrid[0:h, 0:w]
    A = np.stack([np.ones(h * w), xx.ravel() / w, yy.ravel() / h], axis=1)
    coef, *_ = np.linalg.lstsq(A, ch.ravel(), rcond=None)
    return (ch.ravel() - A @ coef).reshape(h, w)


def quad_residual(ch):
    """Residual of a best-fit quadratic surface; if the plane residual is much larger, the patch is not flat."""
    h, w = ch.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y = xx.ravel() / w, yy.ravel() / h
    A = np.stack([np.ones(h * w), x, y, x * x, x * y, y * y], axis=1)
    coef, *_ = np.linalg.lstsq(A, ch.ravel(), rcond=None)
    return (ch.ravel() - A @ coef).reshape(h, w)


def jitter_boxes(box, d=0.15):
    """Five boxes: the original and four shifted by +-d of its own size (to see how much the sample moves)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    return [box] + [[x0 + dx * d * w, y0 + dy * d * h, x1 + dx * d * w, y1 + dy * d * h]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]


def vector_angle(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    c = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


SOFT_SIGMA_PER_STRENGTH = 0.272   # luma sigma per noise strength for a grain layer built at half size and scaled up bicubic (ffmpeg 6.1.1)
FLAT_MAX_SIGMA = 12.0                                     # levels; above this the "flat" patch is rejected as structure


def cast_box_of(spec):
    return spec.get("paper") or spec["white"]


def measure(path, spec, long_side=None):
    im = load(path, long_side)
    arr = np.asarray(im).astype(np.float64) / 255.0
    pic = crop_frac(arr, spec["print_area"])
    # Percentiles are taken on a box-averaged thumbnail (about 480 px wide) so that grain and dust do not bias the
    # black floor and white ceiling (tested: on the full-size image the floor read 0.016 too low for sigma 5 grain).
    red = max(1, pic.shape[1] // 480)
    thumb = Image.fromarray((pic * 255 + 0.5).astype(np.uint8)).reduce(red)
    med = np.asarray(thumb).astype(np.float64) / 255.0
    flat_px = med.reshape(-1, 3)
    floor = np.percentile(flat_px, 0.5, axis=0)
    ceil = np.percentile(flat_px, 99.5, axis=0)
    L_white = float(np.percentile(luma(flat_px), 99.5))
    W = np.median(crop_frac(arr, cast_box_of(spec)).reshape(-1, 3), axis=0)
    S = np.median(crop_frac(arr, spec["skin"]).reshape(-1, 3), axis=0)
    grain = {}
    if spec.get("flat"):
        fl = crop_frac(arr, spec["flat"])
        res = np.stack([plane_residual(fl[..., c]) for c in range(3)], axis=-1)
        res_y = plane_residual(luma(fl))
        ok = res_y.std() * 255 <= FLAT_MAX_SIGMA                 # a "flat" patch with sigma above this holds structure
        grain = {
            "sigma_luma_levels": float(res_y.std() * 255) if ok else None,
            "sigma_rgb_levels": (res.std(axis=(0, 1)) * 255).tolist(),
            "grain_corr_RG": float(np.corrcoef(res[..., 0].ravel(), res[..., 1].ravel())[0, 1]),
            "grain_lag1_autocorr": float(np.corrcoef(res_y[:, :-1].ravel(), res_y[:, 1:].ravel())[0, 1]),
            "flat_patch_flatness_ratio": round(float(res_y.std() / max(quad_residual(luma(fl)).std(), 1e-9)), 2),
            "flat_mean": float(luma(fl).mean()),
            "flat_patch_rejected_as_structured": (not ok),
        }
    cast_box = cast_box_of(spec)                        # the unprinted paper margin beats an in-scene white when the scan has one
    jit = [np.median(crop_frac(arr, b).reshape(-1, 3), axis=0) for b in jitter_boxes(cast_box)]
    jit_angle = max(vector_angle(j, jit[0]) for j in jit[1:])
    m = flat_px
    est = {
        "grey_world": m.mean(axis=0),
        "max_rgb": ceil,
        "shades_of_grey_p6": (np.mean(m ** 6, axis=0)) ** (1 / 6),
    }
    err = {k: round(vector_angle(v, W), 2) for k, v in est.items()}
    return {
        "file": path, "size": list(im.size),
        "floor": floor.tolist(), "ceil": ceil.tolist(), "L_white": L_white,
        "white_patch": W.tolist(), "skin_patch": S.tolist(),
        "white_chroma": (W / luma(W)).tolist(),
        **grain,
        "white_patch_box_jitter_deg": round(jit_angle, 2),
        "illuminant_angle_error_vs_white_patch_deg": err,
    }


def skin_check(S, floor, white):
    n = np.clip((np.asarray(S) - floor) / np.maximum(np.asarray(white) - floor, 1e-6), 0, 1)
    y = float(n @ LUMA)
    cb, cr = (n[2] - y) / 1.8556, (n[0] - y) / 1.5748
    return {"relative_level": round(y, 3), "hue_deg": round(math.degrees(math.atan2(cr, cb)) % 360, 1),
            "off_skin_line_deg": round(abs((math.degrees(math.atan2(cr, cb)) % 360) - SKIN_LINE_DEG), 1)}


def noise_strength(sigma):
    """Smallest table strength whose measured sigma reaches the target; linear between table rows."""
    pts = sorted(NOISE_TABLE.items())
    if sigma <= pts[0][1]:
        return 0
    for (n0, s0), (n1, s1) in zip(pts, pts[1:]):
        if s0 <= sigma <= s1:
            return round(n0 + (n1 - n0) * (sigma - s0) / (s1 - s0), 1) if s1 > s0 else n1
    return pts[-1][0]


def derive(samples, long_side=None):
    per = [measure(p["file"], p, long_side) for p in samples["prints"]]
    floor = np.median([m["floor"] for m in per], axis=0)
    L_white = float(np.median([m["L_white"] for m in per]))   # kept in the report; the level now comes from `top`
    unit = [np.array(m["white_chroma"]) / np.linalg.norm(m["white_chroma"]) for m in per]
    cast = np.mean(unit, axis=0)
    cast /= np.linalg.norm(cast)
    top = float(np.median([max(m["ceil"]) for m in per]))   # brightest channel of the print's white
    white = np.clip(cast / cast.max() * top, 0, 1)         # keep the white patch's chromaticity, set the level by the print
    ang = [round(vector_angle(unit[i], unit[j]), 2) for i in range(len(unit)) for j in range(i + 1, len(unit))]
    sig_all = [m["sigma_luma_levels"] for m in per if m.get("sigma_luma_levels") is not None]
    spread = {
        "cast_pairwise_angle_deg": ang,
        "floor_range": (np.max([m["floor"] for m in per], axis=0) - np.min([m["floor"] for m in per], axis=0)).round(3).tolist(),
        "white_level_range": round(max(max(m["ceil"]) for m in per) - min(max(m["ceil"]) for m in per), 3),
        "white_patch_box_jitter_deg": [m["white_patch_box_jitter_deg"] for m in per],
        "flat_patch_flatness_ratio": [m.get("flat_patch_flatness_ratio") for m in per],
        "sigma_luma_range": [round(min(sig_all), 2), round(max(sig_all), 2)] if sig_all else None,
    }
    coherent = max(ang) <= 3.0 and max(spread["floor_range"]) <= 0.06 and spread["white_level_range"] <= 0.08
    sigma = float(np.median(sig_all)) if sig_all else 0.0
    skin = [skin_check(m["skin_patch"], floor, white) for m in per]
    n_str = noise_strength(sigma)
    levels = (f"colorlevels=rimin=0:gimin=0:bimin=0:rimax=1:gimax=1:bimax=1:"
              f"romin={floor[0]:.4f}:gomin={floor[1]:.4f}:bomin={floor[2]:.4f}:"
              f"romax={white[0]:.4f}:gomax={white[1]:.4f}:bomax={white[2]:.4f}")
    grain = f"format=yuv444p,noise=c0s={n_str}:c0f=t+u,format=rgb24" if n_str else "format=rgb24"
    film = samples.get("film", {"width": 1920, "height": 1080, "fps": 25})
    lag1 = float(np.median([m["grain_lag1_autocorr"] for m in per if "grain_lag1_autocorr" in m])) if sig_all else 0.0
    soft = None
    if sig_all and lag1 >= 0.3:                                   # real grain is spatially correlated: build it small, scale it up
        half = 2 if lag1 < 0.75 else 3
        n_soft = round(min(sigma / SOFT_SIGMA_PER_STRENGTH, 100), 1)
        soft = (f"color=c=0x808080:s={film['width'] // half}x{film['height'] // half}:r={film['fps']},"
                f"format=yuv444p,noise=c0s={n_soft}:c0f=t+u,format=gray,scale={film['width']}:{film['height']}:flags=bicubic,format=rgb24[g];"
                f"[0:v]{levels},format=rgb24[b];[b][g]blend=all_mode=grainmerge:shortest=1")
    out = {
        "album": samples.get("album", "unnamed"), "chapter": samples.get("chapter", ""),
        "per_print": per, "spread": spread, "ONE_ALBUM_LOOK": bool(coherent),
        "black_c": floor.round(4).tolist(), "white_c": white.round(4).tolist(),
        "sigma_luma_levels": round(sigma, 2), "noise_strength": n_str, "skin_check": skin,
        "flat_patch_mean_level": round(float(np.median([m['flat_mean'] for m in per if 'flat_mean' in m])), 3) if sig_all else None,
        "grain_notes": {"corr_RG": round(float(np.median([m["grain_corr_RG"] for m in per if "grain_corr_RG" in m])), 2),
                        "lag1_autocorr": round(float(np.median([m["grain_lag1_autocorr"] for m in per if "grain_lag1_autocorr" in m])), 2),
                        "note": "lag1_autocorr near 0 = per-pixel noise (what ffmpeg noise makes); real grain is above 0.3, so soften the synthetic grain"} if sig_all else None,
        "ffmpeg_vf": levels + "," + grain,
        "ffmpeg_filter_complex_soft_grain": soft,
    }
    return out


if __name__ == "__main__":
    samples = json.load(open(sys.argv[1]))
    res = derive(samples, samples.get("working_long_side"))
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "per_print"}, indent=1))
    for m in res["per_print"]:
        print(m["file"], "illuminant error vs the cast patch (deg):", m["illuminant_angle_error_vs_white_patch_deg"])
