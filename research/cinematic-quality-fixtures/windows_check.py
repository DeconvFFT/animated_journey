"""One-command check of the measurement scripts on the maker's PC (round 2). Records versions and runs, with the maker's ffmpeg build and caption font:
  1. caption_xheight.py       x-height of FontSize=20/23/26 at 1080p in the caption font, with a font-fallback check against the font's own metrics
  2. zoom_velocity_classifier.py   roughness of a Pillow push and a zoompan push (expect zoompan clearly rougher) with ZV_SIZE=1920x1080
  3. mo8_audit.py             centre/edge jitter of the same two pushes (expect Pillow <= 0.05 px, zoompan about 0.3 px)
  4. pan_estimator.py         three constant-speed pans at 8, 11.43 and 16 px/frame (expect each within 0.3 px of the truth)
  5. pan_ease_classifier.py   one cosine in-out pan (expect family in-out)

  py -3 -I windows_check.py WORKDIR --font "C:\\Windows\\Fonts\\arial.ttf" --font-name "Arial" [--ffmpeg "C:\\tools\\ffmpeg\\bin\\ffmpeg.exe"] [--quick]
  (or  python -I windows_check.py ... ).  Needs Python 3.10+, numpy and Pillow (py -3 -m pip install numpy pillow). Takes about 5 minutes (--quick: about 2).
Writes WORKDIR/windows_check_report.json and prints a PASS / CHECK table. Send the JSON back. No personal material is used (a generated test still).
Keep this file in the same folder as the five scripts above, zoompan_vs_subpixel_prints.py, pan_estimator.py and ab_push_card.py (it imports the still generator)."""
import os, sys, json, platform, subprocess, hashlib, shutil, argparse, time, re, math
import numpy as np
from PIL import Image
import PIL

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
W, H, FPS = 1920, 1080, 24


def run(cmd, cwd=None, env=None, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def versions(ffmpeg, font):
    d = dict(date=time.strftime("%Y-%m-%d %H:%M:%S"), platform=platform.platform(), machine=platform.machine(), python=sys.version.split()[0],
             numpy=np.__version__, pillow=PIL.__version__)
    try:
        from PIL import features
        d["pillow_freetype"] = features.version("freetype2"); d["pillow_raqm"] = bool(features.check("raqm"))
    except Exception: pass
    rc, out, err = run([ffmpeg, "-hide_banner", "-version"])
    lines = out.splitlines()
    d["ffmpeg_version_line"] = lines[0] if lines else err[:200]
    d["ffmpeg_configuration"] = next((l for l in lines if l.startswith("configuration:")), "")
    d["ffmpeg_libs"] = [l.strip() for l in lines if l.startswith("lib")]
    cfg = d["ffmpeg_configuration"]
    d["ffmpeg_has_libass"] = "--enable-libass" in cfg; d["ffmpeg_has_fontconfig"] = ("--enable-libfontconfig" in cfg) or ("--enable-fontconfig" in cfg)
    d["ffmpeg_has_libx264"] = "--enable-libx264" in cfg; d["ffmpeg_has_harfbuzz"] = "--enable-libharfbuzz" in cfg
    rc, out, _ = run([ffmpeg, "-hide_banner", "-filters"])
    d["filter_subtitles"] = " subtitles " in out; d["filter_zoompan"] = " zoompan " in out
    p = shutil.which(ffmpeg) or ffmpeg
    if os.path.exists(p): d["ffmpeg_path"] = p; d["ffmpeg_sha256"] = sha256(p); d["ffmpeg_bytes"] = os.path.getsize(p)
    if font and os.path.exists(font):
        from PIL import ImageFont
        f = ImageFont.truetype(font, 100)
        d["font_file"] = font; d["font_bytes"] = os.path.getsize(font); d["font_sha256"] = sha256(font); d["font_names"] = list(f.getname())
        try:
            from fontTools.ttLib import TTFont
            t = TTFont(font); d["font_fonttools"] = dict(unitsPerEm=t["head"].unitsPerEm, hhea_asc=t["hhea"].ascent, hhea_desc=t["hhea"].descent,
                                                       os2_xHeight=getattr(t["OS/2"], "sxHeight", None), os2_capHeight=getattr(t["OS/2"], "sCapHeight", None))
        except Exception: d["font_fonttools"] = "fontTools not installed (optional)"
    return d


def luma_zoom_frames(still, N, amt, mode):
    """Pillow resize(box) Lanczos push (mode 'pil') frames as uint8 array."""
    sw, sh = still.size; out = np.empty((N, H, W, 3), np.uint8)
    for i in range(N):
        z = 1 + amt * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1))); w, h = sw / z, sh / z; x0, y0 = (sw - w) / 2, (sh - h) / 2
        out[i] = np.asarray(still.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)))
    return out


def encode(frames, mp4, ffmpeg, crf=14):
    p = subprocess.Popen([ffmpeg, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", str(crf),
                          "-pix_fmt", "yuv420p", mp4], stdin=subprocess.PIPE)
    for fr in frames: p.stdin.write(np.ascontiguousarray(fr).tobytes())      # frame by frame: no second copy of the whole clip in memory
    p.stdin.close(); p.wait()
    if p.returncode != 0: raise RuntimeError("ffmpeg encode failed (is libx264 in this build?)")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("work"); ap.add_argument("--font", default=None); ap.add_argument("--font-name", default=None)
    ap.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg")); ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(); work = os.path.abspath(a.work); os.makedirs(work, exist_ok=True)
    ff = shutil.which(a.ffmpeg) or a.ffmpeg
    if os.path.exists(ff): a.ffmpeg = os.path.abspath(ff)                  # the sub-scripts change directory, so the path must be absolute
    if a.font: a.font = os.path.abspath(a.font)
    N = 48 if a.quick else 96
    AMT = 0.02 if a.quick else 0.04          # same peak speed per frame; the 9-frame-mean jitter numbers (b, c) are only comparable at the full 96 frames / 4%
    env = dict(os.environ); env["FFMPEG"] = a.ffmpeg
    ffdir = os.path.dirname(shutil.which(a.ffmpeg) or a.ffmpeg)
    if ffdir: env["PATH"] = ffdir + os.pathsep + env.get("PATH", "")      # the scripts that call plain "ffmpeg" now get the maker's build
    env["ZV_SIZE"] = "1920x1080"
    py = [sys.executable, "-I"]
    rep = dict(versions=versions(a.ffmpeg, a.font), checks={})
    rows = []
    def record(name, status, detail): rep["checks"][name] = dict(status=status, **detail); rows.append((name, status, detail.get("summary", "")))

    # 1. caption x-height
    if a.font and a.font_name:
        t0 = time.time(); wd = os.path.join(work, "cx")
        rc, out, err = run(py + [os.path.join(HERE, "caption_xheight.py"), wd, a.font, a.font_name], env=env)
        res = json.load(open(os.path.join(wd, "q1_results.json"))) if rc == 0 and os.path.exists(os.path.join(wd, "q1_results.json")) else []
        r1080 = [r for r in res if r["H"] == 1080]
        ok = bool(r1080) and all(abs(r.get("gap_pts", 9)) <= 0.25 for r in r1080)
        record("1_caption_xheight", "PASS" if ok else "CHECK", dict(summary="x-height % at FontSize 20/23/26: " + ", ".join(str(r["xh_pct"]) for r in r1080) + (" (font as expected)" if ok else " (gap to font metrics > 0.25 pt: libass may have used another font, or the run failed)"),
                                                                    rows=r1080, secs=round(time.time() - t0, 1), stderr=err[-400:] if rc else ""))
    else:
        record("1_caption_xheight", "SKIPPED", dict(summary="pass --font and --font-name to measure the caption font"))

    # shared still
    from ab_push_card import synthetic_still
    still = synthetic_still()
    still_png = os.path.join(work, "still_4k.png"); still.save(still_png)

    # 2 and 3. pushes
    t0 = time.time()
    pil_mp4 = os.path.join(work, "pil_push.mp4"); zp_mp4 = os.path.join(work, "zp_push.mp4")
    encode(luma_zoom_frames(still, N, AMT, "pil"), pil_mp4, a.ffmpeg)
    zexpr = f"1+{AMT}*(0.5-0.5*cos(PI*on/{N-1}))"
    rc, _, err = run([a.ffmpeg, "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", still_png, "-vf",
                      f"zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}:d={N},format=yuv420p", "-frames:v", str(N), "-c:v", "libx264", "-crf", "14", zp_mp4], env=env)
    if rc != 0: record("2_zoom_velocity_classifier", "CHECK", dict(summary="zoompan failed: " + err[-300:]));
    else:
        rough = {}
        for tag, mp4 in (("pillow", pil_mp4), ("zoompan", zp_mp4)):
            rc, out, err = run(py + [os.path.join(HERE, "zoom_velocity_classifier.py"), mp4], env=env)
            m = re.search(r"roughness ([0-9.]+)", out); rough[tag] = float(m.group(1)) if m else None
        ratio = rough["zoompan"] / rough["pillow"] if rough.get("pillow") and rough.get("zoompan") else None
        record("2_zoom_velocity_classifier", "PASS" if ratio and ratio >= 1.5 else "CHECK",
               dict(summary=f"roughness Pillow {rough['pillow']}, zoompan {rough['zoompan']}, ratio {None if ratio is None else round(ratio, 2)} (expect >= 1.5; round 1 saw 4 to 15 on real prints)", roughness=rough, secs=round(time.time() - t0, 1)))
        t0 = time.time(); audits = {}
        for tag, mp4 in (("pillow", pil_mp4), ("zoompan", zp_mp4)):
            rc, out, err = run(py + [os.path.join(HERE, "mo8_audit.py"), mp4], env=env)
            try: audits[tag] = json.loads(out.strip().splitlines()[-1])
            except Exception: audits[tag] = dict(error=(err or out)[-300:])
        pj = audits["pillow"].get("mo8a_centre_jit_px"); zj = audits["zoompan"].get("mo8a_centre_jit_px")
        ok = pj is not None and zj is not None and pj <= 0.05 and zj >= 0.15
        record("3_mo8_audit", "PASS" if ok else "CHECK", dict(summary=f"centre jitter Pillow {pj} px (limit 0.05), zoompan {zj} px (expect about 0.6 here: the yuv420p chain doubles zoompan's error from 0.29 through rgb24; round 2 container: Pillow 0.003, zoompan 0.63); 4th-difference edge jitter {audits['pillow'].get('mo8b_d4_px')} / {audits['zoompan'].get('mo8b_d4_px')}",
                                                               audits=audits, secs=round(time.time() - t0, 1)))

    # 4. pan estimator
    t0 = time.time(); pans = {}
    npan = 24 if a.quick else 36
    for sp in (8.0, 11.43, 16.0):
        frames = np.empty((npan, H, W, 3), np.uint8)
        for i in range(npan):
            x0 = 1850 - sp * i; frames[i] = np.asarray(still.resize((W, H), Image.LANCZOS, box=(x0, 540, x0 + W, 540 + H)))
        mp4 = os.path.join(work, f"pan_{sp}.mp4"); encode(frames, mp4, a.ffmpeg, crf=18)
        rc, out, err = run(py + [os.path.join(HERE, "pan_estimator.py"), mp4, str(FPS)], env=env)
        try: j = json.loads(out.strip().splitlines()[-1]); pans[sp] = dict(est_peak_px=round(j["peak_px"], 3), verdict=j["verdict"], err=round(j["peak_px"] - sp, 3))
        except Exception: pans[sp] = dict(error=(err or out)[-300:])
    ok = all("err" in v and abs(v["err"]) <= 0.3 for v in pans.values())
    record("4_pan_estimator", "PASS" if ok else "CHECK", dict(summary="; ".join(f"{k} px/frame -> {v.get('est_peak_px')}" for k, v in pans.items()) + " (expect within 0.3)", pans=pans, secs=round(time.time() - t0, 1)))

    # 5. pan ease classifier
    t0 = time.time()
    if os.path.exists(os.path.join(HERE, "pan_ease_classifier.py")):
        n = 72 if a.quick else 96
        u = np.linspace(0, 1, n); p = 0.5 - 0.5 * np.cos(np.pi * u); D = 11.0 * (n - 1) / (math.pi / 2)
        frames = np.empty((n, H, W, 3), np.uint8)
        for i in range(n):
            x0 = 1850 - D * p[i]; frames[i] = np.asarray(still.resize((W, H), Image.LANCZOS, box=(x0, 540, x0 + W, 540 + H)))
        mp4 = os.path.join(work, "pan_sine.mp4"); encode(frames, mp4, a.ffmpeg, crf=18)
        rc, out, err = run(py + [os.path.join(HERE, "pan_ease_classifier.py"), mp4, str(FPS)], env=env)
        try: j = json.loads(out.strip().splitlines()[-1]); ok = j.get("family") == "in-out"; record("5_pan_ease_classifier", "PASS" if ok else "CHECK", dict(summary=f"cosine in-out pan -> {j.get('cls')} ({j.get('family')}), rmse {j.get('rmse')}, key {j.get('family_key')}", result=j, secs=round(time.time() - t0, 1)))
        except Exception: record("5_pan_ease_classifier", "CHECK", dict(summary="failed: " + (err or out)[-300:]))
    else:
        record("5_pan_ease_classifier", "SKIPPED", dict(summary="pan_ease_classifier.py not in this folder"))

    json.dump(rep, open(os.path.join(work, "windows_check_report.json"), "w"), indent=1)
    v = rep["versions"]
    print("\n== versions ==\n" + "\n".join(f"{k}: {v[k]}" for k in ("platform", "python", "numpy", "pillow", "ffmpeg_version_line", "ffmpeg_has_libass", "ffmpeg_has_fontconfig", "ffmpeg_has_libx264") if k in v))
    print("\n== checks ==")
    for n, s, d in rows: print(f"{s:8s} {n}: {d}")
    print("\nReport:", os.path.join(work, "windows_check_report.json"))
    for f in os.listdir(work):
        if f.endswith(".mp4") or f.endswith("_4k.png"):
            try: os.remove(os.path.join(work, f))
            except OSError: pass


if __name__ == "__main__":
    main()
