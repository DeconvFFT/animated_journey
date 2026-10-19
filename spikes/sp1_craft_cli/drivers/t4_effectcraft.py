#!/usr/bin/env python3
"""t4_effectcraft.py: SP1 test T4 (EffectCraft titles, line-draw and parallax) with the pass marks of research/craft-motion.md R8, at 1080p24.

USAGE  python3 -I t4_effectcraft.py --app effectcraft --tag vX.Y.Z --cli ABSOLUTE_PATH --home DIR --work DIR [--profile lean|full] [--plan-json J] [--mini]
Run it under lj_bench inside lj_with_disk (run_sp1.sh does). --mini shrinks the content for the mechanism tests against a fake CLI (envelope UNVERIFIED).

WHAT IT BUILDS (all synthetic, neutral geometry; no deity, symbol or script)
  Title     text layer "TEST 0123" with opacity and position keys and a wiggle expression, transparent background (RGBA).
  Line      a pasted SVG of three plain strokes with Trim Paths End keyed 0 -> 100.
  Parallax  five layers (one solid, four shapes), classic 3D, a camera with a slow dolly. The layers are solids and shapes, not imported RGBA
            footage: this measures the 3D compositor, not footage decode (a limit of this test, recorded in the evidence).
WHAT IT MEASURES  (RAYON_NUM_THREADS=1 for the parallax comp, as the plan says)
  png         Title and Line as RGBA PNG sequences at default threads: no crash or OOM; the PNGs carry alpha (transparent corner pixel).
  parallax    seconds per frame at one thread (startup subtracted) under 3 s; peak RSS under 6 GB; a short default-threads sample is recorded too.
  prores4444  Title as ProRes 4444 RGBA: ffprobe pix_fmt (yuva444p12le expected) and the colour tags (issue #340), decode silent, frame count.
  h264        Title as H.264: frame count, decode silent.
  determinism the same frame rendered by two separate processes is byte-identical (the expression comp).
  killed      OBSERVATION only: an H.264 render killed after 3 s; does the file have a moov atom (documents issue #1615)? Never a pass criterion.
EXIT CODES  0 all pass; 1 a measured criterion failed; 2 the harness could not drive the CLI (a command-surface surprise, NOT a verdict on EffectCraft).
NEVER TOUCHES  anything outside --home and --work except the evidence file.
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402

SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='700' viewBox='0 0 1200 700'>"
       "<path id='line_a' d='M100 600 L400 150 L700 600 L1000 150' fill='none' stroke='#ffffff' stroke-width='10'/>"
       "<path id='line_b' d='M100 100 L1100 100' fill='none' stroke='#ffffff' stroke-width='8'/>"
       "<path id='line_c' d='M150 650 C400 400 800 900 1050 600' fill='none' stroke='#ffffff' stroke-width='8'/></svg>")


class HarnessError(Exception):
    pass


def ok(res):
    return res["rc"] == 0 and not res["killed"]


def why(res):
    return "exit %s%s: %s" % (res["rc"], (" (killed by %s)" % res["killed"]) if res["killed"] else "", res["stderr"][-300:].strip())


class T4:
    def __init__(self, a, cfg):
        self.a, self.cfg = a, cfg
        self.rec = L.Recorder()
        self.cli = L.Cli(a.cli, a.home, a.work, self.rec, rss_kill_mb=10240, timeout_s=900)
        self.crit, self.R = [], {}
        self.out = os.path.join(a.work, "exports")
        os.makedirs(self.out, exist_ok=True)
        self.proj = os.path.join(a.work, "t4.ecproj")
        self.w, self.h = cfg["size"]
        self.fps = cfg["fps"]

    def criterion(self, cid, passed, measured, mark):
        self.crit.append({"id": cid, "pass": bool(passed), "measured": measured, "mark": mark})
        print("  %s  %s  measured: %s  (mark: %s)" % ("PASS" if passed else "FAIL", cid, measured, mark))

    def ex(self, cid, params, label=None, first=False):
        pre = ["--empty", "--save-as", self.proj] if first else ["--project", self.proj, "--save"]
        r = self.cli.json(pre + ["exec", cid, "--params", json.dumps(params)], label or ("exec " + cid))
        if not ok(r):
            raise HarnessError("%s failed: %s" % (cid, why(r)))
        return r["json"] if isinstance(r["json"], dict) else {}

    def setp(self, comp, layer, path, value, time_s=None, expression=None):
        args = ["--project", self.proj, "--save", "set", comp, layer, path, json.dumps(value)]
        if time_s is not None:
            args += ["--time", str(time_s)]
        if expression:
            args += ["--expression", expression]
        r = self.cli.run(args, "set %s %s" % (layer, path))
        if not ok(r):
            raise HarnessError("set %s %s failed: %s" % (layer, path, why(r)))

    # ------------------------------------------------------------------ the three comps
    def build(self):
        w, h, fps = self.w, self.h, self.fps
        dur = 3
        self.ex("comp.new", {"name": "Title", "width": w, "height": h, "frameRate": fps, "duration": dur}, first=True)
        self.ex("layer.newText", {"name": "T", "text": "TEST 0123", "size": 160, "fill": "#ffffff"})
        self.setp("Title", "T", "transform/opacity", 0, 0)
        self.setp("Title", "T", "transform/opacity", 100, 1)
        self.setp("Title", "T", "transform/position", [w / 2.0, h / 2.0], expression="wiggle(0.3, 12)")
        self.ex("comp.new", {"name": "Line", "width": w, "height": h, "frameRate": fps, "duration": dur})
        r = self.ex("edit.pasteSvg", {"svg": SVG, "name": "Draw", "comp": "Line"})
        r2 = self.ex("layer.addShapeItem", {"layer": "Draw", "kind": "trim", "comp": "Line"})
        trim = r2.get("path") or "contents/trim"
        self.R["line_trim_path"] = trim
        self.setp("Line", "Draw", trim.rstrip("/") + "/end", 0, 0)
        self.setp("Line", "Draw", trim.rstrip("/") + "/end", 100, 2)
        self.ex("comp.new", {"name": "Parallax", "width": w, "height": h, "frameRate": fps, "duration": dur})
        self.ex("layer.newSolid", {"name": "P0", "comp": "Parallax"})
        for i in range(1, 5):
            self.ex("layer.newShape", {"kind": "ellipse", "name": "P%d" % i, "comp": "Parallax"})
        names = ["P%d" % i for i in range(0, 5)]
        self.ex("layer.setSwitch", {"layers": names, "switch": "threeD", "value": True, "comp": "Parallax"})
        for i, n in enumerate(names):
            self.setp("Parallax", n, "transform/position", [w / 2.0 + (i - 2) * 120, h / 2.0, i * 400])
        self.ex("layer.newCamera", {"name": "Cam", "comp": "Parallax"})
        self.setp("Parallax", "Cam", "transform/position", [w / 2.0, h / 2.0, -1500], 0)
        self.setp("Parallax", "Cam", "transform/position", [w / 2.0, h / 2.0, -1400], dur)

    # ------------------------------------------------------------------ render helpers
    def render_seq(self, comp, seconds, label, env=None, fmt="png"):
        d = os.path.join(self.out, label)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        out = os.path.join(d, "%s_[#####].png" % comp)
        r = self.cli.run(["--project", self.proj, "render", "--comp", comp, "--out", out, "--format", fmt, "--channels", "rgba", "--start", "0", "--end", str(seconds)],
                         "render %s %s s PNG" % (comp, seconds), extra_env=env, timeout_s=900)
        files = sorted(glob.glob(os.path.join(d, "*.png")))
        return r, files

    def alpha_ok(self, files):
        if not files:
            return None
        from PIL import Image
        with Image.open(files[0]) as im:
            if im.mode != "RGBA":
                return False
            return im.getpixel((2, 2))[3] == 0

    # ------------------------------------------------------------------ the tests
    def run_all(self):
        cfg = self.cfg
        ps = cfg["prores_seconds"]
        fps = self.fps
        self.build()
        n_png = fps  # one second
        # PNG with alpha, default threads
        for comp in ("Title", "Line"):
            r, files = self.render_seq(comp, 1, "png_" + comp.lower())
            al = self.alpha_ok(files)
            self.R["png_" + comp.lower()] = {"wall_s": r["wall_s"], "rss_mb": r["max_rss_mb"], "files": len(files), "alpha_transparent_corner": al, "rc": r["rc"],
                                             "ms_per_frame": round(1000.0 * r["wall_s"] / max(len(files), 1), 1)}
            self.criterion("T4.%s_no_oom_default_threads" % comp.lower(), ok(r) and len(files) >= n_png - 1, "exit %s, %d PNGs, peak RSS %.0f MB" % (r["rc"], len(files), r["max_rss_mb"]),
                           "no crash or OOM at 1080p with default threads")
            self.criterion("T4.%s_png_has_alpha" % comp.lower(), al is True, "RGBA with a transparent corner pixel: %s" % al, "PNGs have alpha")
            shutil.rmtree(os.path.join(self.out, "png_" + comp.lower()), ignore_errors=True)
        # parallax, one thread, startup subtracted
        env1 = {"RAYON_NUM_THREADS": str(cfg["rayon_threads"])}
        r1, f1 = self.render_seq("Parallax", 1.0 / fps, "par1", env=env1)
        rN, fN = self.render_seq("Parallax", 0.5, "par12", env=env1)
        nfr = max(len(fN), 1)
        per = (rN["wall_s"] - r1["wall_s"]) / max(nfr - len(f1), 1) if nfr > len(f1) else rN["wall_s"] / nfr
        self.R["parallax_1thread"] = {"frames": len(fN), "wall_s": rN["wall_s"], "baseline_wall_s": r1["wall_s"], "s_per_frame": round(per, 2), "rss_mb": rN["max_rss_mb"], "rc": rN["rc"]}
        self.criterion("T4.parallax_speed", ok(rN) and len(fN) > 0 and per < cfg["parallax_max_seconds_per_frame"], "%.2f s/frame over %d frames, one thread (startup %.1f s subtracted)" % (per, len(fN), r1["wall_s"]),
                       "under %d s/frame at RAYON_NUM_THREADS=1" % cfg["parallax_max_seconds_per_frame"])
        self.criterion("T4.parallax_rss", ok(rN) and rN["max_rss_mb"] < cfg["parallax_max_rss_mb"], "%.0f MB peak" % rN["max_rss_mb"], "under %d MB" % cfg["parallax_max_rss_mb"])
        rD, fD = self.render_seq("Parallax", 0.25, "parD")
        self.R["parallax_default_threads_sample"] = {"frames": len(fD), "wall_s": rD["wall_s"], "rss_mb": rD["max_rss_mb"], "rc": rD["rc"], "note": "recorded, not a criterion"}
        for d in ("par1", "par12", "parD"):
            shutil.rmtree(os.path.join(self.out, d), ignore_errors=True)
        # ProRes 4444 RGBA
        outp = os.path.join(self.out, "title4444.mov")
        rp = self.cli.run(["--project", self.proj, "render", "--comp", "Title", "--out", outp, "--format", "prores", "--prores", "4444", "--channels", "rgba", "--start", "0", "--end", str(ps)],
                          "render Title ProRes 4444 %d s" % ps, timeout_s=900)
        pinfo = {"rc": rp["rc"], "wall_s": rp["wall_s"], "rss_mb": rp["max_rss_mb"], "seconds": ps}
        if ok(rp) and os.path.exists(outp):
            st = L.ffprobe_stream(outp)
            pinfo.update(pix_fmt=st.get("pix_fmt"), codec=st.get("codec_name"), profile=st.get("profile"),
                         frames_counted=int(st["nb_read_frames"]) if str(st.get("nb_read_frames", "")).isdigit() else None,
                         color_space=st.get("color_space"), color_transfer=st.get("color_transfer"), color_primaries=st.get("color_primaries"), color_range=st.get("color_range"),
                         decode_errors=L.decode_errors(outp), size_mb=round(os.path.getsize(outp) / 1048576.0, 1))
            os.remove(outp)
        else:
            pinfo["error"] = why(rp)
        self.R["prores4444"] = pinfo
        self.criterion("T4.prores4444_decodes", ok(rp) and pinfo.get("decode_errors", "x") == "" and pinfo.get("frames_counted") == ps * fps,
                       "frames %s of %d, decode %r" % (pinfo.get("frames_counted"), ps * fps, pinfo.get("decode_errors", "no file")[:120]), "4444 file decodes in ffmpeg with no errors and the right frame count")
        self.R["prores4444_pix_fmt_expected"] = "yuva444p12le"
        self.R["prores4444_pix_fmt_matches_expectation"] = pinfo.get("pix_fmt") == "yuva444p12le"
        # H.264
        outh = os.path.join(self.out, "title.mp4")
        rh = self.cli.run(["--project", self.proj, "render", "--comp", "Title", "--out", outh, "--format", "h264", "--start", "0", "--end", str(ps)], "render Title H.264 %d s" % ps, timeout_s=900)
        hinfo = {"rc": rh["rc"], "wall_s": rh["wall_s"], "rss_mb": rh["max_rss_mb"]}
        if ok(rh) and os.path.exists(outh):
            st = L.ffprobe_stream(outh)
            hinfo.update(frames_counted=int(st["nb_read_frames"]) if str(st.get("nb_read_frames", "")).isdigit() else None, pix_fmt=st.get("pix_fmt"), decode_errors=L.decode_errors(outh),
                         color_space=st.get("color_space"), color_transfer=st.get("color_transfer"), color_primaries=st.get("color_primaries"), color_range=st.get("color_range"))
            os.remove(outh)
        else:
            hinfo["error"] = why(rh)
        self.R["h264"] = hinfo
        self.criterion("T4.h264_decodes", ok(rh) and hinfo.get("decode_errors", "x") == "" and hinfo.get("frames_counted") == ps * fps,
                       "frames %s of %d, decode %r" % (hinfo.get("frames_counted"), ps * fps, hinfo.get("decode_errors", "no file")[:120]), "H.264 decodes with no errors and the right frame count")
        # determinism: the same frame from two processes
        hs = []
        for k in (1, 2):
            p = os.path.join(self.out, "det%d.png" % k)
            rr = self.cli.run(["--project", self.proj, "render-frame", "--comp", "Title", "--time", "0.5", "--out", p, "--transparent"], "render-frame determinism #%d" % k)
            hs.append(hashlib.sha256(open(p, "rb").read()).hexdigest() if ok(rr) and os.path.exists(p) else None)
        self.R["determinism"] = {"sha256_first_12": [h[:12] if h else None for h in hs]}
        self.criterion("T4.determinism", hs[0] is not None and hs[0] == hs[1], "run 1 %s, run 2 %s" % tuple(h[:12] if h else None for h in hs), "expression comps produce identical frames on two runs")
        # observation: a killed H.264 render
        outk = os.path.join(self.out, "killed.mp4")
        argv = L.sandbox_argv(self.a.cli, ["--project", self.proj, "render", "--comp", "Parallax", "--out", outk, "--format", "h264", "--start", "0", "--end", "3"], self.a.home, 60,
                              {"RAYON_NUM_THREADS": "1"})
        rk = L.run_watched(argv, self.cli.tdir, os.path.join(self.cli.tdir, "k.o"), os.path.join(self.cli.tdir, "k.e"), wall_s=3)
        self.R["killed_h264_observation"] = {"killed_by": rk["killed"], "file_exists": os.path.exists(outk), "has_moov": L.has_moov(outk) if os.path.exists(outk) else None,
                                              "note": "observation only (issue #1615): a render stopped mid-way leaves a file; whether it plays is the finding"}
        if os.path.exists(outk):
            os.remove(outk)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default="effectcraft")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cli", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--profile", default="lean", choices=("lean", "full"))
    ap.add_argument("--plan-json", default="{}")
    ap.add_argument("--mini", action="store_true")
    ap.add_argument("--parallax-max-s", type=float, default=None, help="tests only: override the 3 s/frame mark to exercise the failing path")
    a = ap.parse_args(argv)
    if not os.path.isabs(a.cli) or not os.path.isfile(a.cli):
        print("ERROR: --cli must be an existing absolute path", file=sys.stderr)
        return 2
    cfgall = L.read_json(os.path.join(L.SP1, "config.json"))
    cfg = dict(cfgall["t4"])
    cfg["prores_seconds"] = cfg["prores_seconds"][a.profile]
    if a.mini:
        cfg.update(size=[320, 180], prores_seconds=1)
    if a.parallax_max_s is not None:
        cfg["parallax_max_seconds_per_frame"] = a.parallax_max_s
    t = T4(a, cfg)
    print("T4 %s %s (profile %s%s)" % (a.app, a.tag, a.profile, ", MINI content" if a.mini else ""))
    err, t0 = None, time.monotonic()
    try:
        t.run_all()
    except HarnessError as e:
        err = str(e)
        print("  HARNESS: " + err)
    shutil.rmtree(t.out, ignore_errors=True)
    failed = [c for c in t.crit if not c["pass"]]
    if err:
        status, rc = "UNVERIFIED", 2
        actual = "the harness could not drive the CLI: %s; %d criteria measured before that, %d failed" % (err, len(t.crit), len(failed))
    elif a.mini:
        status, rc = "UNVERIFIED", (0 if not failed else 1)
        actual = "MINI content against a stand-in CLI (mechanism test): %d criteria, %d failed" % (len(t.crit), len(failed))
    else:
        status, rc = ("PASS", 0) if not failed else ("FAIL", 1)
        actual = "%d criteria, %d failed%s" % (len(t.crit), len(failed), (": " + "; ".join(c["id"] for c in failed)) if failed else "")
    L.envelope("t4_%s_%s" % (a.app, a.tag) + ("_mini" if a.mini else ""), status,
               "no OOM at 1080p default threads (Title, Line); PNGs have alpha; parallax under 3 s/frame and 6 GB at one thread; ProRes 4444 and H.264 decode silent with the right frame count; two runs identical",
               actual, notes="Parallax layers are solids and shapes, not footage. A Linux CLI pass proves nothing about Windows.",
               unverified_reasons=(["mini content, stand-in CLI"] if a.mini else []) + ([err] if err else []) + ["Windows behaviour is not tested by a Linux CLI run"],
               extra={"profile": a.profile, "mini": a.mini, "criteria": t.crit, "results": t.R, "calls": t.rec.calls[-60:], "calls_total": len(t.rec.calls), "harness_error": err,
                      "sandbox": {"network_isolation": "unshare -rn" if L.unshare_ok() else "not available", "rayon_threads_parallax": cfg["rayon_threads"]},
                      "wall_s": round(time.monotonic() - t0, 1), "contaminated": os.environ.get("LJ_BENCH_CONTAMINATED", "not-timed")})
    print("T4 %s: %s" % (a.tag, status))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
