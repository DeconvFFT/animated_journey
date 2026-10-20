#!/usr/bin/env python3
"""dissolve_routes.py: where does each dissolve route put the half-way frame of the same cross dissolve? (week-2 close-out, package c1; rule "one chapter, one dissolve route")

USAGE  python3 -I spikes/sp1_craft_cli/drivers/dissolve_routes.py [--no-chromium]
Takes the colour pair T2 uses for its dissolve ((201, 70, 60) to (40, 91, 200), two flat frames) and measures the half-way pixel of
  * ffmpeg 6.1.1 `xfade=transition=fade` (the Route B dissolve), and
  * headless Chromium compositing one flat layer at opacity 0.5 over the other (the Route A / CSS opacity cross-fade; the harness's browser, via Playwright),
then compares both with the two candidate answers: the AVERAGE OF THE ENCODED VALUES and the 50/50 MIX IN LINEAR LIGHT (sRGB transfer function). FilmCraft 0.9.0's own
figure for the same pair is read from build/evidence/wp07/t2_filmcraft_v0.9.0.json (not measured here). Writes build/evidence/wp07/dissolve_routes.json.
It is a container measurement on flat colours: it says which space each route blends in, not how any route looks on a photograph, and nothing about Windows builds of ffmpeg,
Chromium or FilmCraft. Chromium missing is UNVERIFIED for that route, never a failure. Reads no personal media (there is none); writes only to a temp folder and the evidence file.
EXIT CODE  0 when every route measured landed on the encoded average or the linear-light mix (within 2 levels); 1 when one landed on neither; 2 when ffmpeg could not run."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402

A = (201, 70, 60)
B = (40, 91, 200)
TOL = 2.0
PW_DEFAULT = "/opt/node-tools/node_modules/playwright"
CHROMIUM_DEFAULT = "/opt/pw-browsers/chromium"


def to_linear(v):
    c = v / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_encoded(lin):
    c = 12.92 * lin if lin <= 0.0031308 else 1.055 * (lin ** (1.0 / 2.4)) - 0.055
    return 255.0 * c


def candidates():
    enc = [(a + b) / 2.0 for a, b in zip(A, B)]
    lin = [to_encoded(0.5 * to_linear(a) + 0.5 * to_linear(b)) for a, b in zip(A, B)]
    return enc, lin


def judge(px, enc, lin):
    d_enc = max(abs(p - e) for p, e in zip(px, enc))
    d_lin = max(abs(p - m) for p, m in zip(px, lin))
    where = "encoded average" if d_enc <= TOL and d_enc < d_lin else ("linear-light mix" if d_lin <= TOL else "neither")
    return {"pixel": list(px), "levels_from_encoded_average": round(d_enc, 2), "levels_from_linear_light_mix": round(d_lin, 2), "blends_in": where}


def hexcol(c):
    return "0x%02X%02X%02X" % c


def xfade_mid(tmp):
    """Half-way pixel of xfade=fade over 1 s (24 frames) at 24 fps: the frame 12 frames after the fade starts."""
    raw = os.path.join(tmp, "xfade.rgb")
    fc = "[0:v][1:v]xfade=transition=fade:duration=1:offset=0.5,format=rgb24"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=%s:s=64x64:r=24:d=2,format=rgb24" % hexcol(A), "-f", "lavfi", "-i", "color=c=%s:s=64x64:r=24:d=2,format=rgb24" % hexcol(B),
           "-filter_complex", fc, "-frames:v", "36", "-f", "rawvideo", raw]
    p = subprocess.run(cmd, capture_output=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg exit %s: %s" % (p.returncode, p.stderr.decode("utf-8", "replace")[-200:]))
    data = open(raw, "rb").read()
    frame = 64 * 64 * 3
    n = len(data) // frame
    if n < 25:
        raise RuntimeError("only %d frames came out" % n)
    # fade runs frames 12..35; the half-way weight is reached at frame 24
    off = 24 * frame + (32 * 64 + 32) * 3
    return n, tuple(data[off:off + 3])


CHROMIUM_JS = """
import { createRequire } from 'module';
const req = createRequire(process.env.DR_PW_PARENT + '/');
const { chromium } = req(process.env.DR_PW_NAME);
const b = await chromium.launch({ executablePath: process.env.DR_CHROMIUM, args: ['--force-color-profile=srgb'] });
const p = await b.newPage({ viewport: { width: 64, height: 64 } });
await p.setContent('<body style="margin:0"><div style="position:absolute;inset:0;background:rgb(%d,%d,%d)"></div><div style="position:absolute;inset:0;background:rgb(%d,%d,%d);opacity:0.5"></div></body>');
await p.screenshot({ path: process.env.DR_OUT });
await b.close();
""" % (A + B)


def chromium_mid(tmp):
    pw = os.environ.get("PW_PATH") or PW_DEFAULT
    exe = os.environ.get("PW_CHROMIUM") or CHROMIUM_DEFAULT
    node = shutil.which("node")
    if not node or not os.path.isdir(pw) or not os.path.exists(exe):
        return None, "node, Playwright (%s) or Chromium (%s) not found" % (pw, exe)
    js = os.path.join(tmp, "mid.mjs")
    out = os.path.join(tmp, "mid.png")
    open(js, "w").write(CHROMIUM_JS)
    env = dict(os.environ, DR_PW_PARENT=os.path.dirname(pw), DR_PW_NAME=os.path.basename(pw), DR_CHROMIUM=exe, DR_OUT=out)
    p = subprocess.run([node, js], capture_output=True, timeout=120, env=env, cwd=tmp)
    if p.returncode != 0 or not os.path.exists(out):
        return None, "node exit %s: %s" % (p.returncode, p.stderr.decode("utf-8", "replace")[-200:])
    from PIL import Image
    im = Image.open(out).convert("RGB")
    return tuple(im.getpixel((32, 32))), ""


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-chromium", action="store_true", help="skip the Chromium route (it is then UNVERIFIED)")
    a = ap.parse_args(argv)
    enc, lin = candidates()
    res = {"colour_pair": [list(A), list(B)], "encoded_average": [round(v, 1) for v in enc], "linear_light_mix": [round(v, 1) for v in lin], "tolerance_levels": TOL, "routes": {}}
    tmp = tempfile.mkdtemp(prefix="dissolve_routes.", dir=os.environ.get("LJ_SCRATCH") or None)
    unv = []
    rc = 0
    try:
        try:
            n, px = xfade_mid(tmp)
            r = judge(px, enc, lin)
            r.update(route="ffmpeg xfade=fade (Route B)", frames_read=n, ffmpeg=L.tool_version(["ffmpeg", "-version"]))
            res["routes"]["ffmpeg_xfade"] = r
        except (OSError, RuntimeError, subprocess.SubprocessError) as e:
            res["routes"]["ffmpeg_xfade"] = {"error": str(e)[:300]}
            rc = 2
        if a.no_chromium:
            unv.append("Chromium route not measured (--no-chromium)")
        else:
            try:
                px, why = chromium_mid(tmp)
            except (OSError, ValueError, subprocess.SubprocessError) as e:
                px, why = None, str(e)[:200]
            if px is None:
                unv.append("Chromium route not measured: " + why)
                res["routes"]["chromium_opacity"] = {"error": why}
            else:
                r = judge(px, enc, lin)
                r.update(route="headless Chromium, one flat layer at opacity 0.5 over the other (Route A / CSS cross-fade)")
                res["routes"]["chromium_opacity"] = r
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # FilmCraft 0.9.0's figure for the same pair comes from the T2 envelope (a CLI run on another day), not from this script
    t2 = os.path.join(L.EVID, "t2_filmcraft_v0.9.0.json")
    try:
        d = L.read_json(t2)["detail"]["results"]["dissolve"]
        if [list(d["neighbour_a"]), list(d["neighbour_b"])] == [list(A), list(B)]:
            r = judge(tuple(d["nearest_pixel"]), enc, lin)
            r.update(route="FilmCraft 0.9.0 CLI, frame nearest the cut (read from t2_filmcraft_v0.9.0.json, not measured here)")
            res["routes"]["filmcraft_0.9.0"] = r
    except (OSError, ValueError, KeyError, TypeError):
        unv.append("FilmCraft figure not read: t2_filmcraft_v0.9.0.json missing or without a dissolve result")
    for name, r in res["routes"].items():
        if r.get("blends_in") == "neither":
            rc = max(rc, 1)
        print("%-18s %s" % (name, json.dumps(r.get("pixel") or r.get("error"))) + ("  -> " + r["blends_in"] if "blends_in" in r else ""))
    print("encoded average %s   linear-light mix %s" % (res["encoded_average"], res["linear_light_mix"]))
    status = "FAIL" if rc else ("UNVERIFIED" if unv else "PASS")
    ms = {k: v.get("blends_in", "not measured") for k, v in res["routes"].items()}
    L.envelope("dissolve_routes", status, "each route's half-way pixel of the same cross dissolve lands on the encoded average or the linear-light mix (within %g levels)" % TOL,
               "; ".join("%s: %s" % kv for kv in sorted(ms.items())), notes="Flat colours, Linux container only; says which space a route blends in, nothing about photographs or Windows.",
               unverified_reasons=unv, extra=res)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
