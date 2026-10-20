#!/usr/bin/env python3
"""t3_filmcraft.py: SP1 test T3 (interchange) on the FilmCraft CLI, with the expectations of research/craft-motion.md R8 T3. Linux CLI only.

USAGE  python3 -I t3_filmcraft.py --cli ABSOLUTE_PATH --home DIR --work DIR [--tag v0.9.0]
       python3 -I t3_filmcraft.py --selftest            (the pure comparison functions, against planted differences; no CLI)
       python3 -I t3_filmcraft.py --emit-chapter SPEC.json OUT.otio   (only the builder: neutral-timeline spec -> OTIO with metadata.filmcraft, plus the missing synthetic test
                                                         cards beside it; no CLI, no evidence. This is the step inputs() runs, and the one the Saturday test chapter in
                                                         research/craft-motion-fixtures/ is built with, so there is one builder and not two)

INPUTS (SYNTHETIC, generated here by the WP-06 emitter pipeline/roundtrip/emit_otio.py from its example spec: four numbered 2880x1620 test cards, a sine WAV,
three 24-frame dissolves, two sequence markers, one clip marker, Ken Burns in metadata.filmcraft). The PLAIN variant is the same file with metadata.filmcraft removed.

WHAT IT DOES (every call is one sandboxed CLI process: env -i, throw-away HOME, timeout, unshare -rn when it works, memory watchdog; the CLI's working folder is NOT the hand-off folder)
  A plain      file.import of the plain OTIO, inspect sequence: clips, durations, 3 dissolves, markers, audio; expectation: NO motion keyframes (R8: "and no motion (expected)")
  B metadata   file.import of the OTIO with metadata.filmcraft: the same structure, and 2 keyframes on motion.position and motion.scale of every clip
  C relative   the media resolve from the .otio's own folder whatever the CLI's working folder is (offlineMedia empty); a copy of the .otio alone in an empty folder reports
               its 5 media offline (the negative control that shows the offline report works)
  D export     file.exportInterchange to otio (beside the media, and in a sub-folder), xml (FCP7), fcpxml and edl; exit 0, bytes, the report lines, xmllint on the XML files,
               JSON parse of the OTIO, the WP-06 validator on the OTIO, the media references classified (relative or absolute)
  E re-import  every export imported into a fresh project and compared with the original sequence (clip names and frames, dissolves, markers, audio, keyframe counts), and
               its OTIO re-export compared keyframe by keyframe (time, value, interpolation name)
  F bare video a hand-made FCPXML whose storyline holds a bare <video>: the documented skip warning
CRITERIA are the R8 T3 pass marks and the mechanism checks; FINDINGS are measured facts the pipeline needs (what a format drops or rewrites). A finding never fails the run.
EXIT CODES  0 all criteria pass   1 a criterion failed (a finding about FilmCraft)   2 the harness could not drive the CLI (a command-surface surprise, NOT a verdict)
WRITES  build/evidence/wp10/t3_filmcraft_<tag>.json (lj-evidence/1, written after every section, replaced at the end). No absolute path, user name or host name is written.
NEVER TOUCHES  anything outside --home, --work and the evidence folder. The exports (which hold absolute file URLs) stay in --work and are deleted with it.
"""
import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402

L = B.L
TICKS = 254016000000
SPEC = os.path.join(B.RT, "spec", "neutral_timeline.example.json")
TOL = 0.011  # keyframe value tolerance (FCP7 and FCPXML write scale as a fraction and positions as offsets, so a tiny rounding is expected)


class HarnessError(Exception):
    pass


# ----------------------------------------------------------------------------- pure functions (also exercised by --selftest)
def frames(ticks, fps_num=24, fps_den=1):
    return round(ticks * fps_num / float(fps_den * TICKS))


def summarize(seq):
    """The comparable shape of `inspect sequence`: sequence settings, clips per track, transitions, markers, motion keyframe counts."""
    fr = seq["settings"]["frame_rate"]
    n, d = fr["num"], fr["den"]
    out = {"fps": [n, d], "size": [seq["settings"]["width"], seq["settings"]["height"]], "duration_frames": seq.get("durationFrames"),
           "markers": sorted([(m["name"], frames(m["start"], n, d)) for m in seq.get("markers", [])], key=lambda x: (x[1], x[0])), "tracks": []}
    for kind in ("video", "audio"):
        for tr in seq.get(kind, []):
            clips = []
            for it in tr.get("items", []):
                kf, val = {}, {}   # kf: parameter -> number of keyframes (`inspect sequence` prints the count, not the keys)
                for e in it.get("effects", []):
                    for pn, p in e.get("params", {}).items():
                        if p.get("keyframes"):
                            kf["%s.%s" % (e["effect"], pn)] = p["keyframes"]
                        if e["effect"] == "motion" and pn in ("scale", "position"):
                            val["%s.%s" % (e["effect"], pn)] = p.get("value")
                clips.append({"name": it["name"], "start": it["startFrame"], "end": it["endFrame"], "kf": kf, "motion_values": val})
            trans = [{"effect": t["effect"], "frames": frames(t["duration"], n, d), "start": frames(t["start"], n, d)} for t in tr.get("transitions", [])]
            out["tracks"].append({"kind": kind, "clips": clips, "transitions": trans})
    return out


def diff_summary(a, b, compare_keyframe_counts=True, compare_transition_starts=True):
    """Differences between two summaries, as short sentences. Track names are ignored (a re-import may call V1 'Video 1')."""
    d = []
    if a["fps"] != b["fps"]:
        d.append("frame rate %s vs %s" % (a["fps"], b["fps"]))
    if a["size"] != b["size"]:
        d.append("sequence size %s vs %s" % (a["size"], b["size"]))
    if a["duration_frames"] != b["duration_frames"]:
        d.append("duration %s vs %s frames" % (a["duration_frames"], b["duration_frames"]))
    if a["markers"] != b["markers"]:
        d.append("sequence markers %s vs %s" % (a["markers"], b["markers"]))
    for kind in ("video", "audio"):
        ta = [t for t in a["tracks"] if t["kind"] == kind]
        tb = [t for t in b["tracks"] if t["kind"] == kind]
        ca = [c for t in ta for c in t["clips"]]
        cb = [c for t in tb for c in t["clips"]]
        if len(ca) != len(cb):
            d.append("%s clip count %d vs %d" % (kind, len(ca), len(cb)))
        for x, y in zip(ca, cb):
            if x["name"] != y["name"]:
                d.append("%s clip name %s vs %s" % (kind, x["name"], y["name"]))
            if (x["start"], x["end"]) != (y["start"], y["end"]):
                d.append("%s clip %s frames %s-%s vs %s-%s" % (kind, x["name"], x["start"], x["end"], y["start"], y["end"]))
            if compare_keyframe_counts:
                kx, ky = x["kf"], y["kf"]
                if kx != ky:
                    d.append("%s clip %s keyframe counts %s vs %s" % (kind, x["name"], kx, ky))
        xa = [t for tr in ta for t in tr["transitions"]]
        xb = [t for tr in tb for t in tr["transitions"]]
        if len(xa) != len(xb):
            d.append("%s transition count %d vs %d" % (kind, len(xa), len(xb)))
        else:
            for p, q in zip(xa, xb):
                if p["effect"] != q["effect"] or p["frames"] != q["frames"] or (compare_transition_starts and p["start"] != q["start"]):
                    d.append("%s transition %s/%d@%d vs %s/%d@%d" % (kind, p["effect"], p["frames"], p["start"], q["effect"], q["frames"], q["start"]))
    return d


def _val(v):
    if isinstance(v, dict) and len(v) == 1:
        k, x = next(iter(v.items()))
        if isinstance(x, dict):
            return tuple(float(x[c]) for c in sorted(x))
        return (float(x),) if isinstance(x, (int, float)) and not isinstance(x, bool) else (x,)
    return (v,)


def otio_motion(doc):
    """{clip name: {param: [(time_ticks, value tuple, interp name)]}} from the metadata.filmcraft effects of an OTIO document."""
    res = {}
    for d in L.walk(doc):
        if str(d.get("OTIO_SCHEMA", "")).startswith("Clip"):
            fc = (d.get("metadata") or {}).get("filmcraft") or {}
            for e in fc.get("effects", []) or []:
                if e.get("effect") == "motion":
                    pr = {}
                    for pn, p in (e.get("params") or {}).items():
                        ks = p.get("keyframes") or []
                        if ks:
                            pr[pn] = [(k["time"], _val(k["value"]), k.get("interp")) for k in ks]
                    res[d.get("name")] = pr
    return res


def kf_compare(a, b, tol=TOL):
    """Keyframe fidelity between two otio_motion() results: same clips and params, same times, same values (within tol), same interpolation names."""
    out = {"clips": len(a), "same_clips": sorted(a) == sorted(b), "counts_equal": True, "times_equal": True, "values_equal": True, "interp_changes": []}
    for name in a:
        pa, pb = a[name], b.get(name, {})
        if sorted(pa) != sorted(pb):
            out["counts_equal"] = False
            continue
        for pn in pa:
            ka, kb = pa[pn], pb[pn]
            if len(ka) != len(kb):
                out["counts_equal"] = False
                continue
            for x, y in zip(ka, kb):
                if x[0] != y[0]:
                    out["times_equal"] = False
                if len(x[1]) != len(y[1]) or any(abs(p - q) > tol for p, q in zip(x[1], y[1]) if isinstance(p, float) and isinstance(q, float)):
                    out["values_equal"] = False
                if x[2] != y[2]:
                    ch = "%s->%s" % (x[2], y[2])
                    if ch not in out["interp_changes"]:
                        out["interp_changes"].append(ch)
    return out


def classify_ref(ref):
    """The FORM of a media reference, never its text (an absolute reference holds the machine's folder names)."""
    r = ref.strip()
    if re.match(r"^file://", r):
        return "absolute file URL"
    if re.match(r"^[A-Za-z]:[\\/]", r) or r.startswith("/") or r.startswith("\\\\"):
        return "absolute path"
    if r.startswith("../"):
        return "relative, one level up (../)"
    return "relative"


def refs_of(fmt, path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    if fmt == "otio":
        return [d["target_url"] for d in L.walk(json.loads(txt)) if isinstance(d.get("target_url"), str)]
    if fmt == "xml":
        return re.findall(r"<pathurl>(.*?)</pathurl>", txt)
    if fmt == "fcpxml":
        return re.findall(r'<media-rep[^>]*\bsrc="([^"]*)"', txt)
    if fmt == "edl":
        return [m.strip() for m in re.findall(r"^\* SOURCE FILE:\s*(.*)$", txt, re.M)]
    return []


def resolve_ref(ref, export_path):
    r = ref.strip()
    if r.startswith("file://"):
        u = urllib.parse.urlparse(r)
        return urllib.parse.unquote(u.path)
    if classify_ref(r) == "absolute path":
        return r
    return os.path.normpath(os.path.join(os.path.dirname(export_path), r))


def strip_filmcraft(doc):
    d = copy.deepcopy(doc)

    def rec(o):
        if isinstance(o, dict):
            md = o.get("metadata")
            if isinstance(md, dict) and "filmcraft" in md:
                del md["filmcraft"]
            for v in o.values():
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
    rec(d)
    return d


def emit_chapter(spec_path, out_otio):
    """The builder: the WP-06 emitter (pipeline/roundtrip/emit_otio.py) run on a neutral-timeline spec. Returns (rc, stdout, stderr); rc 0 written, 2 invalid spec, 3 Pillow missing.
    T3.inputs() calls it for the four-card example spec; `--emit-chapter` calls it for the Saturday test chapter. A synthetic spec makes the missing test cards beside OUT, never overwriting one."""
    return B.run_py([os.path.join(B.RT, "emit_otio.py"), spec_path, out_otio])


# ----------------------------------------------------------------------------- the driver
class T3:
    def __init__(self, a):
        self.a = a
        self.rec = L.Recorder()
        self.cli = L.Cli(a.cli, a.home, a.work, self.rec, rss_kill_mb=10240, timeout_s=300)
        self.ck = B.Checks()
        self.findings = []
        self.matrix = {}
        self.root = os.path.join(a.work, "t3")
        self.hand = os.path.join(self.root, "handoff")
        self.proj = os.path.join(self.root, "proj")
        self.out = os.path.join(self.root, "out")
        for d in (self.hand, self.proj, self.out):
            os.makedirs(d, exist_ok=True)
        self.name = "t3_filmcraft_%s" % a.tag
        self.offline = {}

    # ---- evidence
    def write(self, final=False, status=None, actual=None, extra_notes=""):
        st = status or ("UNVERIFIED" if not final else self.ck.status())
        act = actual or ("%d criteria, %d failed%s" % (len(self.ck.rows), len(self.ck.problems), (": " + "; ".join(self.ck.problems)) if self.ck.problems else ""))
        notes = ("" if final else "stage still running (partial). ") + extra_notes
        B.envelope(self.name, st, "R8 T3: plain OTIO gives correct durations and dissolves and NO motion; OTIO with metadata.filmcraft gives the motion keyframes; the exports are well formed "
                   "and re-import; FCPXML <video> gives the documented skip warning", act, notes=notes,
                   extra={"app": "filmcraft", "tag": self.a.tag, "partial": not final, "checks": self.ck.rows, "findings": self.findings, "formats": self.matrix,
                          "calls": self.rec.calls, "sandbox": {"env": "env -i with HOME, TMPDIR, XDG_*, PATH only", "network_isolation": "unshare -rn" if L.unshare_ok() else "not available",
                                                               "timeout_s": 300, "rss_kill_mb": 10240, "cwd": "a scratch folder that is not the hand-off folder"},
                          "inputs": "synthetic: WP-06 emit_otio.py example spec (4 test cards, 1 sine WAV)"})

    def finding(self, fid, text, measured, implication=""):
        self.findings.append({"id": fid, "finding": text, "measured": measured, "implication": implication})
        print("  FINDING  %s  %s" % (fid, str(measured)[:200]))

    # ---- CLI helpers
    def fc(self, proj, args, label, save=True):
        return self.cli.json(["--project", proj] + (["--save"] if save else []) + args, label)

    def new_project(self, name):
        proj = os.path.join(self.proj, name + ".fcproj")
        r = self.cli.json(["--save-as", proj, "exec", "file.newProject", "name=" + name], "exec file.newProject")
        if r["rc"] != 0:
            raise HarnessError("file.newProject failed: exit %s %s" % (r["rc"], r["stderr"][-200:]))
        return proj

    def import_file(self, name, path, label):
        proj = self.new_project(name)
        r = self.fc(proj, ["exec", "file.import", json.dumps({"paths": [path]})], label)
        if r["rc"] != 0 or not isinstance(r["json"], dict) or "documents" not in r["json"]:
            raise HarnessError("file.import failed for %s: exit %s %s" % (label, r["rc"], (r["stderr"] or r["stdout"])[-200:]))
        doc = r["json"]["documents"][0]
        seq = self.cli.json(["--project", proj, "inspect", "sequence", "--compact"], "inspect sequence")
        if seq["rc"] != 0 or not isinstance(seq["json"], dict) or "video" not in seq["json"]:
            raise HarnessError("inspect sequence failed after %s: exit %s" % (label, seq["rc"]))
        return proj, doc, r["json"], seq["json"]

    def export(self, proj, fmt, path):
        r = self.fc(proj, ["exec", "file.exportInterchange", json.dumps({"format": fmt, "path": path})], "exec file.exportInterchange " + fmt, save=False)
        if r["rc"] != 0 or not isinstance(r["json"], dict):
            return None, r
        return r["json"], r

    # ---- the sections
    def inputs(self):
        spec = os.path.join(self.hand, "spec.json")
        shutil.copyfile(SPEC, spec)
        self.otio_meta = os.path.join(self.hand, "ch01.otio")
        rc, out, err = emit_chapter(spec, self.otio_meta)
        if rc != 0:
            raise HarnessError("emit_otio.py failed: " + (out + err)[-200:])
        self.otio_plain = os.path.join(self.hand, "ch01_plain.otio")
        with open(self.otio_plain, "w", encoding="utf-8", newline="\n") as f:
            json.dump(strip_filmcraft(json.load(open(self.otio_meta, encoding="utf-8"))), f, indent=2)
        rc, out, err = B.run_py([os.path.join(B.RT, "validate_otio.py"), self.otio_meta])
        self.ck.add("T3.inputs.validate_otio_ok", rc == 0, (out.strip().splitlines() or ["(no output)"])[-1], "the WP-06 validator accepts the input before FilmCraft sees it")
        self.src_motion = otio_motion(json.load(open(self.otio_meta, encoding="utf-8")))

    def expect_structure(self, tag, summ, doc, rep, motion):
        ck = self.ck
        self.offline[tag] = len(doc.get("offlineMedia") or [])
        v = [t for t in summ["tracks"] if t["kind"] == "video"]
        au = [t for t in summ["tracks"] if t["kind"] == "audio"]
        clips = v[0]["clips"] if v else []
        ck.add("T3.%s.import_ok" % tag, doc.get("format") == "OpenTimelineIO" and not rep.get("errors") and doc.get("linkedMedia") == 5 and doc.get("offlineMedia") == [],
               "format %s, linkedMedia %s, offlineMedia %s, errors %s, report %s" % (doc.get("format"), doc.get("linkedMedia"), doc.get("offlineMedia"), rep.get("errors"), doc.get("report")),
               "file.import reads the OTIO, finds all 5 media, reports no error")
        ck.add("T3.%s.clips_and_durations" % tag, [(c["start"], c["end"]) for c in clips] == [(0, 120), (120, 240), (240, 360), (360, 480)] and [c["name"] for c in clips] == ["ch01_s01", "ch01_s02", "ch01_s03", "ch01_s04"],
               "video clips %s" % [(c["name"], c["start"], c["end"]) for c in clips], "four 120-frame clips back to back (480 frames, 20 s at 24 fps)")
        tr = v[0]["transitions"] if v else []
        ck.add("T3.%s.dissolves" % tag, len(tr) == 3 and all(t["effect"] == "cross_dissolve" and t["frames"] == 24 for t in tr),
               "transitions %s" % tr, "three 24-frame cross dissolves centred on the cuts (R8: correct durations and dissolve)")
        ck.add("T3.%s.markers_audio_settings" % tag, summ["markers"] == [("Chapter 01", 0), ("Cue: title in", 228)] and len(au) == 1 and [(c["name"], c["start"], c["end"]) for c in au[0]["clips"]] == [("music_bed", 0, 480)]
               and summ["fps"] == [24, 1] and summ["size"] == [1920, 1080] and summ["duration_frames"] == 480,
               "markers %s, audio %s, fps %s, size %s, duration %s" % (summ["markers"], [(c["name"], c["start"], c["end"]) for c in au[0]["clips"]] if au else None, summ["fps"], summ["size"], summ["duration_frames"]),
               "two sequence markers (frames 0 and 228), one 480-frame audio clip, 1920x1080 at 24/1, 480 frames")

    def section_ab(self):
        # A: plain
        proj, doc, rep, seq = self.import_file("plain", self.otio_plain, "import plain OTIO")
        self.proj_plain, self.seq_plain = proj, seq
        s = summarize(seq)
        self.sum_plain = s
        self.expect_structure("plain", s, doc, rep, False)
        nkf = sum(len(c["kf"]) for t in s["tracks"] for c in t["clips"])
        scales = [c["motion_values"].get("motion.scale") for t in s["tracks"] if t["kind"] == "video" for c in t["clips"]]
        self.ck.add("T3.plain.no_motion_keyframes", nkf == 0, "keyframed parameters across all clips: %d; motion.scale values %s" % (nkf, scales),
                    "R8 T3: plain OTIO gives correct durations and dissolve and NO motion (expected)")
        self.write()
        # B: with metadata
        proj, doc, rep, seq = self.import_file("meta", self.otio_meta, "import OTIO with metadata.filmcraft")
        self.proj_meta, self.seq_meta = proj, seq
        s = summarize(seq)
        self.sum_meta = s
        self.expect_structure("meta", s, doc, rep, True)
        vclips = [c for t in s["tracks"] if t["kind"] == "video" for c in t["clips"]]
        kfc = [{k: v for k, v in c["kf"].items() if k.startswith("motion.")} for c in vclips]
        self.ck.add("T3.meta.motion_keyframes", all(k == {"motion.position": 2, "motion.scale": 2} for k in kfc),
                    "keyframes per clip %s" % kfc, "R8 T3: OTIO with metadata.filmcraft gives the motion keyframes (2 on position, 2 on scale for each of the 4 clips)")
        self.ck.add("T3.motion_only_with_metadata", nkf_ok(self.sum_plain) and not nkf_ok(s), "plain: %d keyframed parameters, with metadata: %d" % (count_kf(self.sum_plain), count_kf(s)),
                    "the keyframes survive only with the metadata")
        self.write()

    def section_c(self):
        # the CLI's working folder (work/t) is not the hand-off folder; the plain and metadata imports above already resolved relative media from there
        lone = os.path.join(self.root, "lone")
        os.makedirs(lone, exist_ok=True)
        shutil.copyfile(self.otio_meta, os.path.join(lone, "ch01.otio"))
        proj = self.new_project("lone")
        r = self.fc(proj, ["exec", "file.import", json.dumps({"paths": [os.path.join(lone, "ch01.otio")]})], "import OTIO without its media (negative control)", save=False)
        doc = (r["json"] or {}).get("documents", [{}])[0] if isinstance(r["json"], dict) else {}
        off = doc.get("offlineMedia")
        self.ck.add("T3.relative.negative_control_offline", r["rc"] == 0 and isinstance(off, list) and len(off) == 5, "exit %s, offlineMedia entries %s, linkedMedia %s" % (r["rc"], len(off) if isinstance(off, list) else off, doc.get("linkedMedia")),
                    "an OTIO copied alone (no media/ folder beside it) reports its 5 media offline, so the offline report is real")
        offs = dict(self.offline)
        self.ck.add("T3.relative.resolved_from_the_otio_folder", offs == {"plain": 0, "meta": 0} and os.path.realpath(self.cli.tdir) != os.path.realpath(self.hand),
                    "offline media after the plain and metadata imports: %s; the CLI's working folder is not the hand-off folder: %s" % (offs, os.path.realpath(self.cli.tdir) != os.path.realpath(self.hand)),
                    "relative target_url resolve against the .otio's own folder, not the working folder")
        self.write()

    def section_d(self):
        ck = self.ck
        exp = {}
        plan = [("otio_beside", "otio", os.path.join(self.hand, "ch01.fc.otio")), ("otio_sub", "otio", os.path.join(self.out, "t3.otio")),
                ("xml", "xml", os.path.join(self.out, "t3.xml")), ("fcpxml", "fcpxml", os.path.join(self.out, "t3.fcpxml")), ("edl", "edl", os.path.join(self.out, "t3.edl"))]
        for key, fmt, path in plan:
            res, r = self.export(self.proj_meta, fmt, path)
            row = {"format": fmt, "exit": r["rc"], "bytes": os.path.getsize(path) if os.path.exists(path) else 0, "report": (res or {}).get("report", []), "where": "beside the media folder" if key == "otio_beside" else "sub-folder out/"}
            exp[key] = (fmt, path, row)
            ck.add("T3.export.%s.written" % key, r["rc"] == 0 and row["bytes"] > 0, "exit %s, %d bytes, report %s" % (r["rc"], row["bytes"], row["report"]), "file.exportInterchange writes the file")
            if r["rc"] == 0 and row["bytes"] > 0:
                refs = refs_of(fmt, path)
                forms = sorted({classify_ref(x) for x in refs})
                exists = [os.path.exists(resolve_ref(x, path)) for x in refs]
                row["media_refs"] = {"count": len(refs), "forms": forms, "all_resolve_from_the_file_folder": bool(refs) and all(exists)}
                if fmt in ("xml", "fcpxml"):
                    row["well_formed_xmllint"] = subprocess.run(["xmllint", "--noout", "--nonet", path], capture_output=True, text=True).returncode == 0
                    ck.add("T3.export.%s.xmllint" % key, row["well_formed_xmllint"], "xmllint --noout", "the exported XML is well formed")
                if fmt == "otio":
                    try:
                        json.load(open(path, encoding="utf-8"))
                        row["json_parses"] = True
                    except ValueError:
                        row["json_parses"] = False
                    ck.add("T3.export.%s.json" % key, row["json_parses"], "JSON parse", "the exported OTIO is JSON")
                    rc, out, err = B.run_py([os.path.join(B.RT, "validate_otio.py"), path, "--lenient-filmcraft", "--no-media-check"])
                    last = (out.strip().splitlines() or ["(no output)"])[-2:]
                    row["wp06_validator"] = {"exit": rc, "tail": last}
                    fc = (json.load(open(path, encoding="utf-8")).get("metadata") or {}).get("filmcraft", {}).get("settings", {})
                    ck.add("T3.export.%s.sequence_settings" % key, rc is not None and fc.get("width") == 1920 and fc.get("height") == 1080 and fc.get("frame_rate") == {"num": 24, "den": 1},
                           "metadata.filmcraft.settings: %sx%s at %s" % (fc.get("width"), fc.get("height"), fc.get("frame_rate")), "R8: FilmCraft's own OTIO export carries the sequence settings (a template for them)")
            self.matrix[key] = row
        # the facts the pipeline needs about media references
        for key in ("otio_beside", "otio_sub", "xml", "fcpxml", "edl"):
            row = self.matrix.get(key, {})
            mr = row.get("media_refs")
            if mr:
                absolute = "absolute file URL" in mr["forms"] or "absolute path" in mr["forms"]
                self.finding("export.%s.media_refs" % key, "how %s writes media references" % key, "%d reference(s), form(s): %s, all resolve from the file's own folder: %s" % (mr["count"], mr["forms"], mr["all_resolve_from_the_file_folder"]),
                             ("the file holds the exporting machine's absolute folder names (on the maker's PC: the profile folder): never commit it, never paste it; relink the media by hand in a fallback editor, or hand over the OTIO instead" if absolute
                              else "portable: the file and its media/ folder can be copied together"))
        ck.add("T3.export.otio_beside.relative", self.matrix.get("otio_beside", {}).get("media_refs", {}).get("forms") == ["relative"] and self.matrix["otio_beside"]["media_refs"]["all_resolve_from_the_file_folder"],
               "forms %s, all resolve %s" % (self.matrix.get("otio_beside", {}).get("media_refs", {}).get("forms"), self.matrix.get("otio_beside", {}).get("media_refs", {}).get("all_resolve_from_the_file_folder")),
               "an OTIO exported beside media/ writes relative references that resolve (research/craft-motion.md F3)")
        ck.add("T3.export.edl.relative", self.matrix.get("edl", {}).get("media_refs", {}).get("all_resolve_from_the_file_folder") is True and "absolute file URL" not in self.matrix.get("edl", {}).get("media_refs", {}).get("forms", []),
               "forms %s" % self.matrix.get("edl", {}).get("media_refs", {}).get("forms"), "the EDL names its source files relative to itself")
        self.exports = exp
        self.write()

    def section_e(self):
        ck = self.ck
        base = self.sum_meta
        a_otio = otio_motion(json.load(open(self.exports["otio_beside"][1], encoding="utf-8")))
        for key in ("otio_beside", "xml", "fcpxml", "edl"):
            fmt, path, row = self.exports[key]
            if not os.path.exists(path):
                continue
            proj, doc, rep, seq = self.import_file("re_" + key, path, "re-import " + key)
            s = summarize(seq)
            edl = fmt == "edl"
            diffs = diff_summary(base, s, compare_keyframe_counts=not edl, compare_transition_starts=not edl)
            promoted = []
            if fmt == "fcpxml":
                # the exporter's own report says "clip markers on V1 are written as primary-storyline markers and import as sequence markers": the original sequence markers must all
                # survive; the extra ones are the promoted clip markers, a finding and not a structural difference
                extra = [m for m in s["markers"] if m not in base["markers"]]
                if all(m in s["markers"] for m in base["markers"]) and extra:
                    promoted = extra
                    s2 = dict(s)
                    s2["markers"] = [m for m in s["markers"] if m in base["markers"]]
                    diffs = diff_summary(base, s2, compare_keyframe_counts=True)
            row["reimport"] = {"format": doc.get("format"), "linkedMedia": doc.get("linkedMedia"), "offlineMedia": len(doc.get("offlineMedia") or []), "report": doc.get("report"), "errors": rep.get("errors"),
                               "differences_from_original": diffs, "keyframed_parameters": count_kf(s)}
            # keyframe fidelity through this format: re-export the re-imported project as OTIO and compare with the first OTIO export
            rx = os.path.join(self.out, "re_%s.otio" % key)
            res, r = self.export(proj, "otio", rx)
            if res is not None and os.path.exists(rx):
                cmp_ = kf_compare(a_otio, otio_motion(json.load(open(rx, encoding="utf-8"))))
                row["keyframe_fidelity"] = cmp_
            else:
                cmp_ = None
            if promoted:
                row["reimport"]["clip_markers_promoted_to_sequence_markers"] = promoted
                self.finding("roundtrip.fcpxml.clip_markers", "FCPXML export writes a clip marker as a storyline marker; it re-imports as a SEQUENCE marker", promoted,
                             "put chapter cues on the sequence, not on clips, when the FCPXML route matters")
            if key == "otio_beside":
                ck.add("T3.roundtrip.otio_identical", not diffs and cmp_ is not None and cmp_["counts_equal"] and cmp_["times_equal"] and cmp_["values_equal"] and not cmp_["interp_changes"],
                       "differences %s; keyframes %s" % (diffs or "none", cmp_), "FilmCraft's OTIO export re-imports with the same clips, dissolves, markers and every keyframe (time, value, interpolation name)")
            elif key in ("xml", "fcpxml"):
                ck.add("T3.roundtrip.%s_structure" % key, not diffs, "differences %s" % (diffs or "none"), "clips, frames, dissolves, markers and audio survive %s" % key)
                ck.add("T3.roundtrip.%s_keyframes_time_and_value" % key, cmp_ is not None and cmp_["counts_equal"] and cmp_["times_equal"] and cmp_["values_equal"], "%s" % cmp_,
                       "the motion keyframes (count, time, value within 0.011) survive %s" % key)
                if cmp_ and cmp_["interp_changes"]:
                    self.finding("roundtrip.%s.ease" % key, "the interpolation name changes through %s (the ease the spec asked for is not carried)" % key, cmp_["interp_changes"])
            else:
                ck.add("T3.roundtrip.edl_no_motion", count_kf(s) == 0 and [c["name"] for t in s["tracks"] if t["kind"] == "video" for c in t["clips"]] == ["ch01_s01", "ch01_s02", "ch01_s03", "ch01_s04"],
                       "keyframed parameters %d; video clip names %s" % (count_kf(s), [c["name"] for t in s["tracks"] if t["kind"] == "video" for c in t["clips"]]),
                       "an EDL carries cuts and dissolves only: no motion keyframes (expected), clip names kept")
                if diffs:
                    self.finding("roundtrip.edl.cut_points", "the EDL re-imports with different cut frames (a dissolve is written as a cut plus a transition event)", diffs[:4])
            self.write()
        # a plain project exports and re-imports without gaining any motion
        res, r = self.export(self.proj_plain, "otio", os.path.join(self.out, "plain_export.otio"))
        p_motion = otio_motion(json.load(open(os.path.join(self.out, "plain_export.otio"), encoding="utf-8"))) if res is not None else None
        n = sum(len(v) for v in (p_motion or {}).values())
        ck.add("T3.plain.export_still_no_motion", res is not None and n == 0, "OTIO export of the plain-import project: %s keyframed motion parameters" % (n if p_motion is not None else "export failed"),
               "nothing invents motion: a plain import stays plain through an export")

    def section_f(self):
        import xml.etree.ElementTree as ET
        src = self.exports.get("fcpxml", (None, None, None))[1]
        if not src or not os.path.exists(src):
            self.ck.add("T3.fcpxml_bare_video.skip_warning", False, "no FCPXML export to derive the hand-made file from", "R8 T3: FCPXML <video> produces the documented skip warning")
            return
        t = ET.parse(src)
        r = t.getroot()
        sp = r.find(".//spine")
        first = next((c for c in sp if c.tag == "asset-clip"), None)
        if first is None:
            raise HarnessError("the exported FCPXML has no asset-clip in its storyline")
        first.tag = "video"
        bare = os.path.join(self.out, "bare_video.fcpxml")
        with open(bare, "w", encoding="utf-8", newline="\n") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + ET.tostring(r, encoding="unicode") + "\n")
        proj, doc, rep, seq = self.import_file("bare", bare, "import FCPXML with a bare <video>")
        s = summarize(seq)
        names = [c["name"] for tr in s["tracks"] if tr["kind"] == "video" for c in tr["clips"]]
        warn = [x for x in (doc.get("report") or []) if "video" in x.lower() and "skip" in x.lower()]
        self.ck.add("T3.fcpxml_bare_video.skip_warning", bool(warn) and "ch01_s01" not in names and len(names) == 3, "report %s; clips imported %s" % (doc.get("report"), names),
                    "R8 T3: a bare storyline <video> is skipped with a warning (the clip is not imported)")
        self.write()

    def measure_still_rate(self):
        rates = {}
        xp = self.exports.get("xml", (None, None, None))[1]
        fp = self.exports.get("fcpxml", (None, None, None))[1]
        if xp and os.path.exists(xp):
            t = open(xp, encoding="utf-8").read()
            rates["fcp7_xml_file_rates"] = sorted(set("%s%s" % (a, " NTSC" if b == "TRUE" else "") for a, b in
                                                      re.findall(r"<file id=\"[^\"]*\">\s*<name>[^<]*</name>\s*<pathurl>[^<]*</pathurl>\s*<rate>\s*<timebase>(\d+)</timebase>\s*<ntsc>(\w+)</ntsc>", t)))
            rates["fcp7_xml_sequence_timebase"] = sorted(set(re.findall(r"<sequence[^>]*>.*?<rate>\s*<timebase>(\d+)</timebase>", t, re.S)))[:1]
        if fp and os.path.exists(fp):
            t = open(fp, encoding="utf-8").read()
            rates["fcpxml_format_frame_durations"] = sorted(set(re.findall(r'<format [^>]*frameDuration="([^"]+)"', t)))
        self.finding("export.still_rate", "the frame rate FCP7 XML and FCPXML give the still media files, next to the sequence's own", rates,
                     "a still is written at 29.97 in these two formats while the sequence stays 24 fps; the maker-side Resolve import check (research/craft-motion.md F2) must look at the durations of the stills")

    def run(self):
        try:
            self.inputs()
            self.section_ab()
            self.section_c()
            self.section_d()
            self.section_e()
            self.section_f()
        except HarnessError as e:
            print("HARNESS ERROR: %s" % e)
            self.write(final=True, status="UNVERIFIED", actual="the harness could not drive the CLI: %s" % L.scrub(str(e)), extra_notes="a command-surface surprise, NOT a verdict on FilmCraft.")
            return 2
        except Exception as e:  # noqa: BLE001  (a driver bug must leave evidence, not a bare traceback)
            print("HARNESS EXCEPTION: %s: %s" % (type(e).__name__, e))
            self.write(final=True, status="UNVERIFIED", actual="a bug in the driver, not a verdict on FilmCraft: %s: %s" % (type(e).__name__, L.scrub(str(e))[:300]),
                       extra_notes="the criteria measured before the exception are in checks.")
            return 2
        self.measure_still_rate()
        self.write(final=True)
        print("T3 filmcraft %s: %s (%d criteria, %d failed, %d findings)" % (self.a.tag, self.ck.status(), len(self.ck.rows), len(self.ck.problems), len(self.findings)))
        return 0 if not self.ck.problems else 1


def count_kf(s):
    """Number of keyframed parameters (not keyframes) across all clips."""
    return sum(len(c["kf"]) for t in s["tracks"] for c in t["clips"])


def nkf_ok(s):
    return count_kf(s) == 0


# ----------------------------------------------------------------------------- selftest
def _fake_seq(kf=True, shift=0, drop_trans=False, rename=False):
    def clip(i):
        eff = []
        if kf:
            eff.append({"effect": "motion", "params": {"scale": {"keyframes": 2, "value": "Float(66.67)"}, "position": {"keyframes": 2, "value": "Vec2(1)"}}})
        return {"name": ("X" if rename and i == 0 else "ch01_s0%d" % (i + 1)), "startFrame": i * 120 + shift, "endFrame": i * 120 + 120, "effects": eff}
    tr = [] if drop_trans else [{"effect": "cross_dissolve", "duration": TICKS, "start": 108 * TICKS // 24} for _ in range(3)]
    return {"settings": {"frame_rate": {"num": 24, "den": 1}, "width": 1920, "height": 1080}, "durationFrames": 480, "markers": [{"name": "m", "start": 0}],
            "video": [{"name": "V1", "items": [clip(i) for i in range(4)], "transitions": tr}], "audio": []}


def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok = ok and cond
    a = summarize(_fake_seq())
    check("equal sequences have no differences", diff_summary(a, summarize(_fake_seq())) == [])
    check("a renamed clip is found", any("clip name" in x for x in diff_summary(a, summarize(_fake_seq(rename=True)))))
    check("a shifted clip is found", any("frames" in x for x in diff_summary(a, summarize(_fake_seq(shift=2)))))
    check("a missing keyframe set is found", any("keyframe counts" in x for x in diff_summary(a, summarize(_fake_seq(kf=False)))))
    check("keyframe counts can be ignored (the EDL case)", diff_summary(a, summarize(_fake_seq(kf=False)), compare_keyframe_counts=False) == [])
    check("a dropped dissolve is found", any("transition count" in x for x in diff_summary(a, summarize(_fake_seq(drop_trans=True)))))
    k1 = {"c": {"scale": [(0, (66.67,), "Linear"), (100, (80.0,), "EaseOut")]}}
    k2 = {"c": {"scale": [(0, (66.67,), "Linear"), (100, (80.0,), "Bezier")]}}
    k3 = {"c": {"scale": [(0, (66.67,), "Linear"), (100, (81.0,), "EaseOut")]}}
    k4 = {"c": {"scale": [(0, (66.67,), "Linear"), (101, (80.0,), "EaseOut")]}}
    check("kf_compare: same", kf_compare(k1, k1)["values_equal"] and kf_compare(k1, k1)["interp_changes"] == [])
    check("kf_compare: an interpolation change is named", kf_compare(k1, k2)["interp_changes"] == ["EaseOut->Bezier"] and kf_compare(k1, k2)["values_equal"])
    check("kf_compare: a changed value is found", not kf_compare(k1, k3)["values_equal"])
    check("kf_compare: a moved key time is found", not kf_compare(k1, k4)["times_equal"])
    check("classify_ref: forms", [classify_ref(x) for x in ("media/a.png", "../media/a.png", "file://localhost/x/a.png", "/x/a.png", "C:\\x\\a.png")] ==
          ["relative", "relative, one level up (../)", "absolute file URL", "absolute path", "absolute path"])
    check("otio_motion reads effects", otio_motion({"OTIO_SCHEMA": "Clip.2", "name": "c", "metadata": {"filmcraft": {"effects": [{"effect": "motion", "params": {"scale": {"keyframes": [{"time": 0, "value": {"Float": 66.67}, "interp": "Linear"}]}}}]}}}) == {"c": {"scale": [(0, (66.67,), "Linear")]}})
    check("strip_filmcraft removes the metadata", "filmcraft" not in json.dumps(strip_filmcraft({"metadata": {"filmcraft": {"a": 1}, "other": 2}})))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cli")
    ap.add_argument("--home")
    ap.add_argument("--work")
    ap.add_argument("--tag", default="v0.9.0")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--emit-chapter", nargs=2, metavar=("SPEC", "OUT_OTIO"), help="only build: spec -> OTIO (and the missing synthetic test cards beside it); needs no CLI")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.emit_chapter:
        rc, out, err = emit_chapter(os.path.abspath(a.emit_chapter[0]), os.path.abspath(a.emit_chapter[1]))
        sys.stdout.write(out)
        sys.stderr.write(err)
        return rc
    if not (a.cli and a.home and a.work) or not os.path.isabs(a.cli) or not os.path.isfile(a.cli):
        print("ERROR: --cli (an existing absolute path), --home and --work are required", file=sys.stderr)
        return 2
    return T3(a).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
