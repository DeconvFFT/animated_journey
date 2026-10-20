#!/usr/bin/env python3
"""t2_filmcraft.py: SP1 test T2 (FilmCraft, many stills) with the pass marks of research/craft-motion.md R8, scaled to the project rate (24 fps).

USAGE  python3 -I t2_filmcraft.py --app filmcraft --tag vX.Y.Z --cli ABSOLUTE_PATH --home DIR --work DIR [--profile lean|full] [--plan-json J] [--mini]
Run it under lj_bench inside lj_with_disk (run_sp1.sh does). --mini shrinks the content for the mechanism tests against a fake CLI; its envelope
is then UNVERIFIED, never PASS.

WHAT IT MEASURES (low-entropy JPEG stills from gen_stills.py; every call is one sandboxed CLI process, resident memory read from the kernel)
  scaling   N = 5, 20, 100 stills of 3600x2400, and N = 300 conformed at 2880x1620: import, place, render one frame, export a 2-second draft.
            Pass: no crash or hang; RSS slope (RSS(100) - RSS(20)) / 80 under 40 MB per still; RSS(300) under 12 GB (a watchdog kills at 10 GB).
  export    20 stills x 5 s at 24 fps = 2,400 frames with a Ken Burns move on each, H.264 "High Quality 1080p HD": at least 5 fps (under 8 minutes);
            ffprobe frame count equals 2,400; `ffmpeg -v error -i out -f null -` silent; offlineMedia empty. Then ProRes 422 HQ for 3 s (1 s in the
            lean profile): frame count equals seconds x 24 and the decode is silent.
  kenburns  a gridded still with a marker of known position: first and last frame positions within 1 px of the computed values (scale 100 = native
            pixels, position 960,540 = centre of 1920x1080, as research/cinematic-quality-fixtures/filmcraft_push.py found for 0.9.0).
  dissolve  a 12-frame cross dissolve between two flat-centre stills (the single-frame probe is `render --seconds`, the stepping probe is an exported H.264):
            T2.mid_dissolve   the frame nearest the half-way mix is within 2 levels of the 50/50 mix of the neighbours IN LINEAR LIGHT (sRGB transfer function).
                              Amended Tue 20 Oct 2026 (week-2 gate, nudge 1): the first wording compared with the average of the ENCODED values, which no gamma-correct
                              compositor can pass (FilmCraft measured (149, 81, 151) against a linear-light mix of (149.5, 81.3, 151.4)). The tolerance is unchanged.
            T2.dissolve_steps in a 2-second H.264 export around the cut, the 12 frames from one frame before the first blended frame hold at least 11 distinct
                              levels (the single-frame probe of 20 Oct showed 8): a dissolve that steps in pairs of identical frames judders on the venue screen.
EXIT CODES  0 all pass; 1 a measured criterion failed (a finding); 2 the harness could not drive the CLI (a command-surface surprise, NOT a verdict on FilmCraft).
THE ENVELOPE IS WRITTEN AFTER EVERY PHASE (describe, scaling, export, kenburns+dissolve), with status UNVERIFIED, detail.partial true and the note "stage still
running", and replaced by the final one when the run ends. The whole stage is capped at 60 minutes (run_sp1.sh, build plan 4.9) and the disk guard can stop it at
any moment; either way the criteria measured so far stay in the file. A TERM that reaches this process also writes a "stopped" envelope before it leaves.
NEVER TOUCHES  anything outside --home and --work except the evidence file. Only synthetic stills are used.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402
import gen_stills as G  # noqa: E402

TICKS = 254016000000
PRESET_H264 = "High Quality 1080p HD"
PRESET_PRORES = "Apple ProRes 422 HQ"


def srgb_to_linear(v):
    """8-bit sRGB code value (0..255) to linear light (0..1), the piecewise IEC 61966-2-1 transfer function."""
    c = v / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(lin):
    """Linear light (0..1) to an 8-bit sRGB code value as a float (0..255)."""
    c = 12.92 * lin if lin <= 0.0031308 else 1.055 * (lin ** (1.0 / 2.4)) - 0.055
    return 255.0 * c


def linear_light_mix(a, b, w=0.5):
    """The mix of two RGB triples in linear light, returned as float code values: what a gamma-correct compositor shows at blend weight w."""
    return [linear_to_srgb((1.0 - w) * srgb_to_linear(x) + w * srgb_to_linear(y)) for x, y in zip(a, b)]


def distinct_levels(values, gap):
    """Greedy count of distinct levels: a value within `gap` code values of a level already counted is the same level. Returns the list of levels."""
    levels = []
    for v in values:
        if all(abs(v - lv) > gap for lv in levels):
            levels.append(v)
    return levels


class HarnessError(Exception):
    pass


def int_ids(obj, keys):
    out = []
    for d in L.walk(obj):
        for k in keys:
            v = d.get(k)
            if isinstance(v, int) and not isinstance(v, bool):
                out.append(v)
            elif isinstance(v, list):
                for e in v:
                    if isinstance(e, int) and not isinstance(e, bool):
                        out.append(e)
                    elif isinstance(e, dict) and isinstance(e.get("id"), int):
                        out.append(e["id"])
    seen, res = set(), []
    for i in out:
        if i not in seen:
            seen.add(i)
            res.append(i)
    return res


def jsonl(text):
    rows = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln.startswith("{"):
            try:
                rows.append(json.loads(ln))
            except ValueError:
                pass
    return rows


def ok(res):
    return res["rc"] == 0 and not res["killed"]


def why(res):
    return "exit %s%s: %s" % (res["rc"], (" (killed by %s)" % res["killed"]) if res["killed"] else "", res["stderr"][-300:].strip())


class T2:
    def __init__(self, a, cfg):
        self.a, self.cfg = a, cfg
        self.rec = L.Recorder()
        self.cli = L.Cli(a.cli, a.home, a.work, self.rec, rss_kill_mb=cfg["rss_kill_mb"], timeout_s=900)
        self.crit = []
        self.R = {}
        self.stills = os.path.join(a.work, "stills")
        self.exp = os.path.join(a.work, "exports")
        self.proj = os.path.join(a.work, "proj")
        for d in (self.stills, self.exp, self.proj):
            os.makedirs(d, exist_ok=True)

    # ------------------------------------------------------------------ small helpers
    def criterion(self, cid, passed, measured, mark):
        self.crit.append({"id": cid, "pass": bool(passed), "measured": measured, "mark": mark})
        print("  %s  %s  measured: %s  (mark: %s)" % ("PASS" if passed else "FAIL", cid, measured, mark))

    def fc(self, proj, args, label, save=True, **kw):
        pre = ["--project", proj] + (["--save"] if save else [])
        return self.cli.json(pre + args, label, **kw)

    def new_project(self, name):
        proj = os.path.join(self.proj, name + ".fcproj")
        r = self.cli.json(["--save-as", proj, "exec", "file.newProject", "name=" + name], "exec file.newProject")
        if not ok(r):
            raise HarnessError("file.newProject failed: " + why(r))
        return proj

    def import_stills(self, proj, paths):
        r = self.fc(proj, ["exec", "file.import", json.dumps({"paths": paths})], "exec file.import (%d)" % len(paths))
        if not ok(r):
            return None, r
        ids = int_ids(r["json"], ("items", "imported", "ids", "item"))
        if len(ids) != len(paths):
            names = [os.path.basename(p) for p in paths]
            ri = self.cli.json(["--project", proj, "inspect", "project", "--compact"], "inspect project")
            m = {}
            for d in L.walk(ri["json"]):
                nm, i = d.get("name") or d.get("path") or "", d.get("id")
                if isinstance(i, int) and isinstance(nm, str) and os.path.basename(nm) in names:
                    m[os.path.basename(nm)] = i
            ids = [m[n] for n in names] if all(n in m for n in names) else []
        if len(ids) != len(paths):
            raise HarnessError("could not read the %d item ids after file.import (result shape: %s)" % (len(paths), json.dumps(L.shape_of(r["json"]))[:300]))
        return ids, r

    def new_sequence(self, proj, w=1920, h=1080, fps=24):
        r = self.fc(proj, ["exec", "file.newSequence", json.dumps({"name": "s", "width": w, "height": h, "fps": fps, "sampleRate": 48000})], "exec file.newSequence")
        if not ok(r):
            raise HarnessError("file.newSequence failed: " + why(r))

    def place_all(self, proj, ids, seconds_each, fps=24):
        """Place the items back to back on V1 with an explicit start and duration; returns the clip ids in order."""
        dur = int(seconds_each * TICKS)
        ops = os.path.join(self.a.work, "t", "place.jsonl")
        with open(ops, "w") as f:
            for k, i in enumerate(ids):
                f.write(json.dumps({"id": "timeline.place", "params": {"item": i, "track": "V1", "seconds": k * seconds_each, "duration": dur, "audio": False}}) + "\n")
        r = self.cli.run(["--project", proj, "--save", "run", ops], "run place (%d)" % len(ids))
        if not ok(r):
            raise HarnessError("timeline.place failed: " + why(r))
        clips = []
        for row in jsonl(r["stdout"]):
            got = int_ids(row.get("result"), ("clips", "clip", "id"))
            clips.append(got[0] if got else None)
        if len(clips) != len(ids) or None in clips:
            clips = self.clip_ids_from_inspect(proj, len(ids))
        return clips, r

    def clip_ids_from_inspect(self, proj, expect):
        r = self.cli.json(["--project", proj, "inspect", "sequence", "--compact"], "inspect sequence")
        cands = []
        for d in L.walk(r["json"]):
            if isinstance(d.get("id"), int) and any(k in d for k in ("start", "startTicks", "item", "itemId", "track", "duration")) and not ("width" in d and "height" in d):
                cands.append(d)
        cands.sort(key=lambda d: d.get("start", d.get("startTicks", 0)) if isinstance(d.get("start", d.get("startTicks", 0)), (int, float)) else 0)
        ids = [d["id"] for d in cands]
        if len(ids) != expect:
            raise HarnessError("could not read %d clip ids from inspect sequence (got %d; shape: %s)" % (expect, len(ids), json.dumps(L.shape_of(r["json"]))[:300]))
        return ids

    def keyframe_ops(self, clips, s0s, s1s, dur_ticks, fps=24):
        ops = os.path.join(self.a.work, "t", "kb.jsonl")
        last = dur_ticks - TICKS // fps
        with open(ops, "w") as f:
            for cid, s0, s1 in zip(clips, s0s, s1s):
                for t, v in ((0, s0), (last, s1)):
                    f.write(json.dumps({"id": "effects.setParam", "params": {"clip": cid, "effect": "motion", "param": "scale", "value": v, "time": t, "keyframe": True}}) + "\n")
        return ops

    # ------------------------------------------------------------------ phases
    def phase_describe(self):
        r = self.cli.json(["describe", "effects.setParam"], "describe effects.setParam")
        self.R["describe_setParam_shape"] = L.shape_of(r["json"]) if r["json"] is not None else None

    def phase_scaling(self):
        cfg, a = self.cfg, self.a
        lw, lh = cfg["large_size"]
        cw, ch = cfg["conformed_size"]
        n_large = cfg["n_large"]
        big = max(n_large)
        print("  generating %d stills of %dx%d and %d of %dx%d (JPEG, low entropy)" % (big, lw, lh, cfg["n_conformed"], cw, ch))
        large = [os.path.join(self.stills, "L", "s%04d.jpg" % i) for i in range(1, big + 1)]
        conf = [os.path.join(self.stills, "C", "s%04d.jpg" % i) for i in range(1, cfg["n_conformed"] + 1)]
        tot = 0
        for i, p in enumerate(large, 1):
            tot += G.make_still(p, lw, lh, i)
        for i, p in enumerate(conf, 1):
            tot += G.make_still(p, cw, ch, i)
        self.R["stills_written_mb"] = round(tot / 1048576.0, 1)
        rows = []
        for label, paths in [("%d@%dx%d" % (n, lw, lh), large[:n]) for n in n_large] + [("%d@%dx%d" % (cfg["n_conformed"], cw, ch), conf)]:
            n = len(paths)
            self.cli.peak_rss_mb = 0.0
            row = {"set": label, "n": n, "calls_ok": True, "walls_s": {}, "rss_mb": {}}
            t0 = time.monotonic()
            proj = self.new_project("n%d_%s" % (n, "c" if paths is conf else "l"))
            ids, rimp = self.import_stills(proj, paths)
            if ids is None:
                row.update(calls_ok=False, error="import: " + why(rimp))
                rows.append(row)
                continue
            row["walls_s"]["import"], row["rss_mb"]["import"] = rimp["wall_s"], rimp["max_rss_mb"]
            self.new_sequence(proj)
            try:
                self.place_all(proj, ids, 1.0)
            except HarnessError as e:
                row.update(calls_ok=False, error=str(e))
                rows.append(row)
                continue
            r1 = self.cli.run(["--project", proj, "render", "--seconds", "0.5", "--out", os.path.join(self.exp, "f_%d.png" % n)], "render one frame (N=%d)" % n)
            row["walls_s"]["render"], row["rss_mb"]["render"] = r1["wall_s"], r1["max_rss_mb"]
            r2 = self.cli.run(["--project", proj, "export", os.path.join(self.exp, "d_%d.mp4" % n), "--preset", PRESET_H264, "--start", "0", "--end", "2"], "export 2 s draft (N=%d)" % n)
            row["walls_s"]["export_2s"], row["rss_mb"]["export_2s"] = r2["wall_s"], r2["max_rss_mb"]
            for rr, nm in ((r1, "render"), (r2, "export")):
                if not ok(rr):
                    row["calls_ok"] = False
                    row.setdefault("error", "%s: %s" % (nm, why(rr)))
            row["peak_rss_mb"] = round(max(self.cli.peak_rss_mb, 0.0), 1)
            row["wall_total_s"] = round(time.monotonic() - t0, 1)
            rows.append(row)
            for f in os.listdir(self.exp):
                os.remove(os.path.join(self.exp, f))
            os.remove(proj)
            print("    N=%-4d peak RSS %7.1f MB, %s" % (n, row["peak_rss_mb"], "ok" if row["calls_ok"] else "FAILED: " + row.get("error", "")[:120]))
        self.R["scaling"] = rows
        by = {r["n"]: r for r in rows}
        lo, hi = sorted(n_large)[-2], sorted(n_large)[-1]
        nbig = by.get(hi)
        self.criterion("T2.no_crash_n%d_large" % hi, bool(nbig and nbig["calls_ok"]), (nbig or {}).get("error", "no crash or hang"), "no crash or hang at N=100 (3600x2400)")
        nconf = by.get(cfg["n_conformed"])
        self.criterion("T2.no_crash_n%d_conformed" % cfg["n_conformed"], bool(nconf and nconf["calls_ok"]), (nconf or {}).get("error", "no crash or hang"), "no crash or hang at N=300 (2880x1620)")
        if lo in by and hi in by and "peak_rss_mb" in by[lo] and "peak_rss_mb" in by[hi]:
            slope = (by[hi]["peak_rss_mb"] - by[lo]["peak_rss_mb"]) / float(hi - lo)
            self.R["rss_slope_mb_per_still"] = round(slope, 2)
            self.criterion("T2.rss_slope", slope < cfg["rss_slope_max_mb_per_still"], "%.2f MB per still (RSS(%d) %.0f - RSS(%d) %.0f over %d stills)" % (slope, hi, by[hi]["peak_rss_mb"], lo, by[lo]["peak_rss_mb"], hi - lo),
                           "under %d MB per still" % cfg["rss_slope_max_mb_per_still"])
        else:
            self.criterion("T2.rss_slope", False, "not measurable: a run of N=%d or N=%d did not finish" % (lo, hi), "under %d MB per still" % cfg["rss_slope_max_mb_per_still"])
        if nconf and "peak_rss_mb" in nconf:
            self.criterion("T2.rss_n%d" % cfg["n_conformed"], nconf["peak_rss_mb"] < cfg["rss_n300_max_mb"], "%.0f MB" % nconf["peak_rss_mb"], "under %d MB (watchdog kills at %d MB)" % (cfg["rss_n300_max_mb"], cfg["rss_kill_mb"]))
        else:
            self.criterion("T2.rss_n%d" % cfg["n_conformed"], False, "no figure: the run did not finish", "under %d MB" % cfg["rss_n300_max_mb"])

    def phase_export(self):
        cfg, a = self.cfg, self.a
        n, per, fps = cfg["export_stills"], cfg["seconds_per_still"], cfg["fps"]
        lw, lh = cfg["large_size"]
        frames = n * per * fps
        paths = [os.path.join(self.stills, "L", "s%04d.jpg" % i) for i in range(1, n + 1)]
        proj = self.new_project("export%d" % n)
        ids, r = self.import_stills(proj, paths)
        if ids is None:
            raise HarnessError("import for the export test failed: " + why(r))
        self.new_sequence(proj)
        clips, _ = self.place_all(proj, ids, per)
        dur = per * TICKS
        s0 = max(1920.0 / lw, 1080.0 / lh) * 100.0
        ops = self.keyframe_ops(clips, [s0] * n, [s0 * 1.12] * n, dur, fps)
        rk = self.cli.run(["--project", proj, "--save", "run", ops], "run keyframes (%d)" % (2 * n))
        if not ok(rk):
            raise HarnessError("keyframes failed: " + why(rk))
        out = os.path.join(self.exp, "t2_h264.mp4")
        rx = self.cli.json(["--project", proj, "export", out, "--preset", PRESET_H264], "export H.264 %d frames" % frames, timeout_s=1200)
        info = {"frames_expected": frames, "wall_s": rx["wall_s"], "rss_mb": rx["max_rss_mb"], "rc": rx["rc"], "killed": rx["killed"]}
        if ok(rx) and os.path.exists(out):
            st = L.ffprobe_stream(out)
            info.update(frames_counted=int(st.get("nb_read_frames", -1)) if str(st.get("nb_read_frames", "")).isdigit() else None, r_frame_rate=st.get("r_frame_rate"),
                        pix_fmt=st.get("pix_fmt"), size="%sx%s" % (st.get("width"), st.get("height")), fps_measured=round(frames / max(rx["wall_s"], 0.001), 2),
                        decode_errors=L.decode_errors(out), size_mb=round(os.path.getsize(out) / 1048576.0, 1))
            offline = [d.get("offlineMedia") for d in L.walk(rx["json"]) if "offlineMedia" in d] if rx["json"] is not None else []
            info["offline_media"] = offline[0] if offline else None
            os.remove(out)
        else:
            info["error"] = why(rx)
        self.R["h264_export"] = info
        self.criterion("T2.h264_completes", ok(rx), "exit %s after %.0f s" % (rx["rc"], rx["wall_s"]), "export finishes without crash, hang or the 10 GB kill")
        mark_s = cfg["h264_max_seconds"]
        self.criterion("T2.h264_speed", ok(rx) and info.get("fps_measured", 0) >= cfg["h264_min_fps"], "%s fps (%d frames in %.0f s)" % (info.get("fps_measured"), frames, rx["wall_s"]),
                       "at least %d fps, i.e. under %d s for %d frames (R8 pass mark, scaled to 2,400 frames at this film's 24 fps from R8's 3,000-frame figure)" % (cfg["h264_min_fps"], mark_s, frames))
        self.criterion("T2.h264_frame_count", info.get("frames_counted") == frames, "%s counted, %d expected, rate %s" % (info.get("frames_counted"), frames, info.get("r_frame_rate")), "ffprobe frame count equals expected")
        self.criterion("T2.h264_decode_silent", ok(rx) and info.get("decode_errors", "x") == "", repr(info.get("decode_errors", "no file"))[:200], "ffmpeg -v error -i out -f null - prints nothing")
        self.criterion("T2.offline_media_empty", info.get("offline_media") == [], repr(info.get("offline_media")), "offlineMedia: [] in the export result")
        # ProRes
        ps = cfg["prores_seconds"]
        outp = os.path.join(self.exp, "t2_prores.mov")
        rp = self.cli.json(["--project", proj, "export", outp, "--preset", PRESET_PRORES, "--start", "0", "--end", str(ps)], "export ProRes %d s" % ps, timeout_s=900)
        pinfo = {"seconds": ps, "frames_expected": ps * fps, "wall_s": rp["wall_s"], "rss_mb": rp["max_rss_mb"], "rc": rp["rc"]}
        if ok(rp) and os.path.exists(outp):
            st = L.ffprobe_stream(outp)
            pinfo.update(frames_counted=int(st["nb_read_frames"]) if str(st.get("nb_read_frames", "")).isdigit() else None, codec=st.get("codec_name"), profile=st.get("profile"),
                         pix_fmt=st.get("pix_fmt"), decode_errors=L.decode_errors(outp), size_mb=round(os.path.getsize(outp) / 1048576.0, 1),
                         fps_measured=round(ps * fps / max(rp["wall_s"], 0.001), 2))
            os.remove(outp)
        else:
            pinfo["error"] = why(rp)
        self.R["prores_export"] = pinfo
        self.criterion("T2.prores_frame_count", pinfo.get("frames_counted") == ps * fps, "%s counted, %d expected, codec %s %s" % (pinfo.get("frames_counted"), ps * fps, pinfo.get("codec"), pinfo.get("profile")),
                       "ffprobe frame count equals %d s x %d fps" % (ps, fps))
        self.criterion("T2.prores_decode_silent", ok(rp) and pinfo.get("decode_errors", "x") == "", repr(pinfo.get("decode_errors", "no file"))[:200], "decode silent")
        os.remove(proj)

    def phase_kenburns_dissolve(self):
        import numpy as np
        from PIL import Image
        cfg = self.cfg
        lw, lh = cfg["large_size"]
        fps = 24
        mk = (lw // 2 - 900 * lw // 3600, lh // 2 - 600 * lh // 2400)  # scales with the still; (900,600) at 3600x2400
        # two stills: S1 has the marker and a distinct flat centre, S2 a different flat centre
        s1, s2 = os.path.join(self.stills, "kb1.jpg"), os.path.join(self.stills, "kb2.jpg")
        G.make_still(s1, lw, lh, 11, colour=(200, 70, 60), marker_xy=mk)
        G.make_still(s2, lw, lh, 12, colour=(40, 90, 200))
        proj = self.new_project("kb")
        ids, r = self.import_stills(proj, [s1, s2])
        if ids is None:
            raise HarnessError("import for the Ken Burns test failed: " + why(r))
        self.new_sequence(proj)
        clips, _ = self.place_all(proj, ids, 3.0)
        s0 = max(1920.0 / lw, 1080.0 / lh) * 100.0
        s1v = s0 * 1.12
        ops = self.keyframe_ops(clips[:1], [s0], [s1v], 3 * TICKS, fps)
        rk = self.cli.run(["--project", proj, "--save", "run", ops], "run keyframes (Ken Burns test)")
        if not ok(rk):
            raise HarnessError("Ken Burns keyframes failed: " + why(rk))
        frames_total = 3 * fps
        t_last = (frames_total - 1) / float(fps)

        def centroid(png):
            im = np.asarray(Image.open(png).convert("RGB")).astype(np.int16)
            m = (im[:, :, 0] > 180) & (im[:, :, 2] > 180) & (im[:, :, 1] < 90)
            ys, xs = np.nonzero(m)
            if xs.size < 20:
                return None
            return float(xs.mean()) + 0.5, float(ys.mean()) + 0.5

        def expected(s):
            return 960.0 + (mk[0] - lw / 2.0) * s / 100.0, 540.0 + (mk[1] - lh / 2.0) * s / 100.0

        kb = {"marker_in_still": list(mk), "scale_first": round(s0, 3), "scale_last": round(s1v, 3), "frames": []}
        worst = 0.0
        for label, t, s in (("first", 0.0, s0), ("last", t_last, s1v)):
            png = os.path.join(self.exp, "kb_%s.png" % label)
            rr = self.cli.run(["--project", proj, "render", "--seconds", "%.6f" % t, "--out", png], "render Ken Burns %s frame" % label)
            if not ok(rr) or not os.path.exists(png):
                kb["frames"].append({"which": label, "error": why(rr)})
                worst = 99.0
                continue
            c = centroid(png)
            ex = expected(s)
            if c is None:
                kb["frames"].append({"which": label, "error": "marker not found in the rendered frame", "expected_px": [round(ex[0], 2), round(ex[1], 2)]})
                worst = 99.0
                continue
            err = max(abs(c[0] - ex[0]), abs(c[1] - ex[1]))
            worst = max(worst, err)
            kb["frames"].append({"which": label, "t_s": round(t, 4), "expected_px": [round(ex[0], 2), round(ex[1], 2)], "measured_px": [round(c[0], 2), round(c[1], 2)], "error_px": round(err, 2)})
        self.R["kenburns"] = kb
        self.criterion("T2.kenburns_positions", worst <= 1.0, "worst error %.2f px at the first and last keyframes" % worst, "within 1 px of the computed positions")

        # dissolve between the two clips: T2.mid_dissolve (single-frame probe) and T2.dissolve_steps (exported H.264)
        tol = float(cfg["dissolve_mid_tolerance_levels"])
        nfr = int(cfg["dissolve_frames"])
        mark_mid = "within %g levels of the 50/50 mix of the neighbours in linear light (sRGB transfer function)" % tol
        mark_steps = "at least %d distinct levels over the %d exported frames that start one frame before the first blended frame" % (cfg["dissolve_min_levels"], nfr)
        rt = self.fc(proj, ["exec", "sequence.applyVideoTransition", json.dumps({"clip": clips[1], "effect": "cross_dissolve", "frames": nfr})], "exec applyVideoTransition")
        dis = {"transition_exit": rt["rc"]}
        if not ok(rt):
            dis["error"] = why(rt)
            self.R["dissolve"] = dis
            self.criterion("T2.mid_dissolve", False, dis["error"][:200], mark_mid)
            self.criterion("T2.dissolve_steps", False, "not measured: the transition could not be applied", mark_steps)
            return
        A, B = G.centre_colour(s1), G.centre_colour(s2)
        cut = 3.0
        samples = []
        for k in range(-12, 13):
            t = cut + k / float(fps)
            png = os.path.join(self.exp, "ds_%d.png" % (k + 12))
            rr = self.cli.run(["--project", proj, "render", "--seconds", "%.6f" % t, "--out", png], "render dissolve frame %d" % k)
            if not ok(rr) or not os.path.exists(png):
                dis["error"] = why(rr)
                break
            im = Image.open(png).convert("RGB")
            px = np.asarray(im).astype(np.float64)
            patch = px[540 - 5:540 + 6, 960 - 5:960 + 6, :].reshape(-1, 3).mean(axis=0)
            samples.append((k, patch.tolist()))
            os.remove(png)
        if "error" in dis or not samples:
            dis.setdefault("error", "no frames")
            self.R["dissolve"] = dis
            self.criterion("T2.mid_dissolve", False, dis["error"][:200], mark_mid)
            self.criterion("T2.dissolve_steps", False, "not measured: the single-frame probe did not finish", mark_steps)
            return
        # the half-way mix a gamma-correct compositor shows: the 50/50 mix in linear light. (The first wording of this mark used the average of the encoded
        # values, (A + B) / 2, which is what Pillow's Image.blend and ffmpeg xfade show; it is kept in the envelope as `average_encoded` for the record.)
        mid = linear_light_mix(A, B, 0.5)
        avg_encoded = [(A[i] + B[i]) / 2.0 for i in range(3)]
        best = min(samples, key=lambda s: sum(abs(s[1][i] - mid[i]) for i in range(3)))
        dev = max(abs(best[1][i] - mid[i]) for i in range(3))
        dev_encoded = max(abs(best[1][i] - avg_encoded[i]) for i in range(3))
        alphas = []
        for k, p in samples:
            denom = (B[0] - A[0]) or 1
            alphas.append(round((p[0] - A[0]) / float(denom), 3))
        dis.update(neighbour_a=list(A), neighbour_b=list(B), midpoint_linear_light=[round(v, 1) for v in mid], average_encoded=[round(v, 1) for v in avg_encoded],
                   nearest_frame_offset=best[0], nearest_pixel=[round(v, 1) for v in best[1]], deviation_levels=round(dev, 2), deviation_from_encoded_average=round(dev_encoded, 2),
                   alpha_by_frame_encoded_red=dict(zip([k for k, _ in samples], alphas)))
        self.R["dissolve"] = dis
        self.criterion("T2.mid_dissolve", dev <= tol, "%.2f levels at frame offset %+d (neighbours %s and %s, linear-light mix %s; the average of the encoded values %s would be %.2f levels away)"
                       % (dev, best[0], A, B, [round(v) for v in mid], [round(v) for v in avg_encoded], dev_encoded), mark_mid)
        self.dissolve_steps(proj, cut, nfr, cfg, mark_steps)

    def dissolve_steps(self, proj, cut, nfr, cfg, mark):
        """T2.dissolve_steps: export 2 s of the dissolve project as H.264, read the centre patch of every frame, and count the distinct levels in the dissolve.

        The window is `nfr` frames long and starts one frame before the first blended frame (so it holds the last pure frame of the first still and the blended frames);
        two frames are the same level when their patch means are within cfg['dissolve_level_gap'] code values. The channel with the widest spread between the
        two stills is read. The first and last exported frames are the pure neighbours, so the count does not depend on the colour matrix of the decode."""
        fps = 24
        gap = float(cfg["dissolve_level_gap"])
        out = os.path.join(self.exp, "dissolve_steps.mp4")
        rx = self.cli.json(["--project", proj, "export", out, "--preset", PRESET_H264, "--start", "%g" % (cut - 1.0), "--end", "%g" % (cut + 1.0)], "export dissolve window (2 s)", timeout_s=600)
        info = {"window_s": [cut - 1.0, cut + 1.0], "rc": rx["rc"], "wall_s": rx["wall_s"], "frames_expected": 2 * fps, "cut_frame_index": fps, "min_levels": cfg["dissolve_min_levels"], "level_gap": gap}
        if not ok(rx) or not os.path.exists(out):
            info["error"] = why(rx)
            self.R["dissolve_export"] = info
            self.criterion("T2.dissolve_steps", False, "not measured: " + info["error"][:160], mark)
            return
        try:
            n, rgb = exported_patch_means(out, 960, 540, 5)
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            info["error"] = "could not read the exported frames: %s" % e
            self.R["dissolve_export"] = info
            self.criterion("T2.dissolve_steps", False, "not measured: " + info["error"][:160], mark)
            return
        finally:
            if os.path.exists(out):
                os.remove(out)
        info["frames_read"] = n
        first, last = rgb[0], rgb[-1]
        ch = max(range(3), key=lambda c: abs(last[c] - first[c]))
        vals = [row[ch] for row in rgb]
        span = abs(vals[-1] - vals[0])
        info.update(channel="RGB"[ch], pure_first=round(vals[0], 1), pure_last=round(vals[-1], 1), levels_by_frame=[round(v, 1) for v in vals])
        if n < 2 * fps - 2 or span < 20.0:
            info["error"] = "the export did not show two flat colours (%d frames, spread %.1f)" % (n, span)
            self.R["dissolve_export"] = info
            self.criterion("T2.dissolve_steps", False, "not measured: " + info["error"], mark)
            return
        blended = [i for i, v in enumerate(vals) if abs(v - vals[0]) > gap and abs(v - vals[-1]) > gap]
        if not blended:
            info.update(blended_frames=0, distinct_levels=0)
            self.R["dissolve_export"] = info
            self.criterion("T2.dissolve_steps", False, "no blended frame at all in the exported window: a hard cut", mark)
            return
        f0, f1 = blended[0], blended[-1]
        start = max(0, f0 - 1)
        window = vals[start:start + nfr]
        levels = distinct_levels(window, gap)
        info.update(blended_frames=len(blended), first_blended_index=f0, last_blended_index=f1, window_start_index=start, window_frames=len(window),
                    distinct_levels=len(levels), window_levels=[round(v, 1) for v in window], distinct_levels_in_whole_export=len(distinct_levels(vals, gap)))
        self.R["dissolve_export"] = info
        self.criterion("T2.dissolve_steps", len(levels) >= cfg["dissolve_min_levels"],
                       "%d distinct levels over %d exported frames (%d blended frames, from index %d, channel %s, levels %s)" % (len(levels), len(window), len(blended), f0, "RGB"[ch], [round(v) for v in window]), mark)


def exported_patch_means(path, cx, cy, half):
    """Decode every frame of an exported file and return (number of frames, [(r, g, b) mean of the square patch of side 2*half around (cx, cy)] per frame), via one ffmpeg pipe.
    The side is even on purpose: ffmpeg rounds a crop of a 4:2:0 picture down to even sizes, so an odd side would silently change the frame size and the frame count read back."""
    import numpy as np
    w = 2 * half
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "crop=%d:%d:%d:%d,format=rgb24" % (w, w, cx - half, cy - half), "-f", "rawvideo", "-"], capture_output=True, timeout=300)
    if p.returncode != 0:
        raise ValueError("ffmpeg exit %s: %s" % (p.returncode, L.scrub(p.stderr.decode("utf-8", "replace")[-200:])))
    arr = np.frombuffer(p.stdout, dtype=np.uint8)
    per = w * w * 3
    n = arr.size // per
    if n == 0:
        raise ValueError("ffmpeg produced no frames")
    arr = arr[:n * per].reshape(n, w * w, 3).astype(np.float64)
    return n, [tuple(float(x) for x in frame.mean(axis=0)) for frame in arr]


def write_envelope(t, a, cfg, t0, phase_done, err=None, stopped=None, final=False):
    """Write (or replace) the T2 envelope. final=False: the run is still going (after a phase): UNVERIFIED, partial. stopped: a TERM ended the run."""
    failed = [c for c in t.crit if not c["pass"]]
    unv = (["mini content, stand-in CLI"] if a.mini else []) + ["Windows behaviour is not tested by a Linux CLI run"]
    if stopped:
        status, rc = "UNVERIFIED", 3
        actual = "stage stopped before T2 finished (%s); %d criteria measured after phase '%s', %d failed" % (stopped, len(t.crit), phase_done, len(failed))
        unv.append("the run was stopped before the last phase: " + stopped)
    elif not final:
        status, rc = "UNVERIFIED", 0
        actual = "stage still running: phase '%s' done; %d criteria measured so far, %d failed" % (phase_done, len(t.crit), len(failed))
        unv.append("stage still running (a partial envelope, replaced when the run ends)")
    elif err:
        status, rc = "UNVERIFIED", 2
        actual = "the harness could not drive the CLI: %s; %d criteria measured before that, %d failed" % (err, len(t.crit), len(failed))
        unv.append(err)
    elif a.mini:
        status, rc = "UNVERIFIED", (0 if not failed else 1)
        actual = "MINI content against a stand-in CLI (mechanism test): %d criteria, %d failed" % (len(t.crit), len(failed))
    else:
        status, rc = ("PASS", 0) if not failed else ("FAIL", 1)
        actual = "%d criteria, %d failed%s" % (len(t.crit), len(failed), (": " + "; ".join(c["id"] for c in failed)) if failed else "")
    L.envelope("t2_%s_%s" % (a.app, a.tag) + ("_mini" if a.mini else ""), status,
               "all of: no crash at N=100 and N=300; RSS slope under 40 MB per still; RSS(N=300) under 12 GB; 2,400-frame H.264 at 5 fps or more with the right frame count and silent decode; "
               "ProRes frame count; Ken Burns first/last within 1 px; mid-dissolve within 2 levels of the linear-light mix of its neighbours (mark amended 2026-10-20); "
               "dissolve steps: at least 11 distinct levels over 12 exported frames (criterion added 2026-10-20); offlineMedia empty",
               actual, notes=("stage still running" if (not final and not stopped) else "A Linux CLI pass proves nothing about Windows. Timing is only valid when contaminated=no."),
               unverified_reasons=unv,
               extra={"profile": a.profile, "mini": a.mini, "criteria": t.crit, "results": t.R, "calls": t.rec.calls[-60:], "calls_total": len(t.rec.calls), "harness_error": err,
                      "partial": not final, "phase_done": phase_done, "stopped": stopped,
                      "sandbox": {"network_isolation": "unshare -rn" if L.unshare_ok() else "not available", "rss_kill_mb": cfg["rss_kill_mb"]},
                      "wall_s": round(time.monotonic() - t0, 1), "contaminated": os.environ.get("LJ_BENCH_CONTAMINATED", "not-timed")})
    return status, rc


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default="filmcraft")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cli", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--profile", default="lean", choices=("lean", "full"))
    ap.add_argument("--plan-json", default="{}")
    ap.add_argument("--mini", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isabs(a.cli) or not os.path.isfile(a.cli):
        print("ERROR: --cli must be an existing absolute path", file=sys.stderr)
        return 2
    cfgall = L.read_json(os.path.join(L.SP1, "config.json"))
    cfg = dict(cfgall["t2"])
    cfg["prores_seconds"] = cfgall["profiles"][a.profile]["prores_seconds"]
    if a.mini:
        cfg.update(n_large=[2, 4, 8], large_size=[720, 480], n_conformed=12, conformed_size=[576, 324], export_stills=3, seconds_per_still=1, h264_min_fps=5)
        cfg["prores_seconds"] = 1
    t = T2(a, cfg)
    print("T2 %s %s (profile %s%s)" % (a.app, a.tag, a.profile, ", MINI content" if a.mini else ""))
    err = None
    t0 = time.monotonic()
    done = "none"
    try:
        for name, fn in (("describe", t.phase_describe), ("scaling", t.phase_scaling), ("export", t.phase_export), ("kenburns_dissolve", t.phase_kenburns_dissolve)):
            fn()
            done = name
            if name != "kenburns_dissolve":
                write_envelope(t, a, cfg, t0, done)  # everything measured so far survives a timeout, a TERM or a DISK-FLOOR
    except HarnessError as e:
        err = str(e)
        print("  HARNESS: " + err)
    except SystemExit as e:  # the TERM handler of sp1_lib (the 60-minute timeout or the disk guard): record what was measured, then leave
        try:
            write_envelope(t, a, cfg, t0, done, stopped="TERM received (stage timeout or disk guard)")
        except OSError:
            pass
        shutil.rmtree(t.stills, ignore_errors=True)
        shutil.rmtree(t.exp, ignore_errors=True)
        raise
    shutil.rmtree(t.stills, ignore_errors=True)
    shutil.rmtree(t.exp, ignore_errors=True)
    status, rc = write_envelope(t, a, cfg, t0, done, err=err, final=True)
    print("T2 %s: %s" % (a.tag, status))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
