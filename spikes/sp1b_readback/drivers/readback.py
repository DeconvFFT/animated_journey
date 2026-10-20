"""readback.py: the read-backs of SP1b for PhotoCraft, VectorCraft and LightCraft on their Linux CLIs. Imported by visual_app.py.

Each function takes (cli, work, ck, findings) and measures; every input is SYNTHETIC (the WP-06 emitters, the reused fixtures of research/craft-visual-fixtures).
A criterion (ck.add) is a pass mark of the playbook's five-minute test; a finding (findings.append) is a measured fact the pipeline needs. Every number here is a
Linux CLI result and says nothing about Windows.

  photocraft   info and convert on the WP-06 ORA and on at-layers.ora: layer names compared with stack.xml through info, a PNG, an ORA and a PSD
  vectorcraft  convert of the WP-06 rig and of at-rig.svg, then the reused check_ids.py (and the WP-06 gate around it); a PNG and a PDF export of at-rig.svg
  lightcraft   render of a synthetic JPEG with LIGHTCRAFT_GPU=0; the faded-print-a.lcpreset import and the reused steps file, paths rewritten for this folder
"""
import json
import os
import shutil
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402

L = B.L


class HarnessError(Exception):
    pass


def tail_err(r):
    return (r["stderr"] or r["stdout"])[-200:].strip().replace("\n", " | ")


def first_line(text):
    ls = [x for x in text.strip().splitlines() if x.strip()]
    return ls[0] if ls else ""


# ----------------------------------------------------------------------------- PhotoCraft
def photocraft(cli, work, ck, findings):
    from PIL import Image, ImageChops, ImageStat
    d = os.path.join(work, "pc")
    os.makedirs(d, exist_ok=True)
    ora_wp06 = os.path.join(d, "wp06.ora")
    ok, msg = B.make_wp06_ora(ora_wp06)
    if not ok:
        raise HarnessError("WP-06 ORA emitter failed: " + msg[-200:])
    ora_at = os.path.join(d, "at-layers.ora")
    shutil.copyfile(os.path.join(B.FIX, "at-layers.ora"), ora_at)
    shapes = {}

    def one(name, ora):
        (cw, chh), exp = B.ora_expected(ora)
        p = "RB.photocraft.%s." % name
        r = cli.json(["info", ora, "--compact"], "info %s.ora --compact" % name)
        ck.add(p + "info_json", r["rc"] == 0 and isinstance(r["json"], (dict, list)), "exit %s, %s" % (r["rc"], "JSON" if r["json"] is not None else "no JSON: " + tail_err(r)), "`info <ora> --compact` prints the layer tree as JSON")
        shapes[name] = L.shape_of(r["json"], 3) if r["json"] is not None else None
        found = B.layer_names(r["json"]) if r["json"] is not None else []
        missing = [n for n in exp if n not in found]
        extra = [n for n in found if n not in exp]
        ck.add(p + "layer_names", not missing and len(found) >= len(exp), "stack.xml %s; info %s; missing %s; extra %s" % (exp, found, missing or "none", extra or "none"),
               "every layer name in stack.xml appears in the info layer tree, with the same spelling")
        filt = [n for n in found if n in exp]
        order = "top-first" if filt == exp else ("bottom-first" if filt == list(reversed(exp)) else "other")
        findings.append({"id": p + "layer_order", "finding": "the order in which info lists the layers", "measured": order, "implication": "a reader of the manifest must know which end is the top"})
        canvas = [d2 for d2 in L.walk(r["json"] or {}) if ("width" in d2 and "height" in d2)]
        if canvas:
            c0 = canvas[0]
            findings.append({"id": p + "canvas", "finding": "document size in the info JSON", "measured": "%sx%s (stack.xml says %sx%s)" % (c0.get("width"), c0.get("height"), cw, chh), "implication": ""})
        # convert to a flat PNG and compare with the ORA's own mergedimage.png
        png = os.path.join(d, name + ".out.png")
        rc_ = cli.run(["convert", ora, png], "convert %s.ora out.png" % name)
        sz = B.image_size(png) if os.path.exists(png) and open(png, "rb").read(8) == b"\x89PNG\r\n\x1a\n" else None
        ck.add(p + "convert_png", rc_["rc"] == 0 and sz == (cw, chh), "exit %s, PNG size %s (canvas %sx%s)%s" % (rc_["rc"], sz, cw, chh, ("; " + tail_err(rc_)) if rc_["rc"] else ""), "`convert <ora> out.png` writes a PNG of the canvas size")
        if sz == (cw, chh):
            with zipfile.ZipFile(ora) as z:
                import io
                merged = Image.open(io.BytesIO(z.read("mergedimage.png"))).convert("RGB")
            got = Image.open(png).convert("RGB")
            mad = sum(ImageStat.Stat(ImageChops.difference(merged, got)).mean) / 3.0
            ck.add(p + "flatten_matches_mergedimage", mad <= 8.0, "mean absolute difference %.2f levels against the ORA's mergedimage.png (mark: at most 8, a planner's proposal)" % mad,
                   "PhotoCraft's own flatten of the layers is close to the merged image the emitter wrote")
        # ORA -> ORA -> info: layer names survive a PhotoCraft save
        o2 = os.path.join(d, name + ".out.ora")
        rc_ = cli.run(["convert", ora, o2], "convert %s.ora out.ora" % name)
        r2 = cli.json(["info", o2, "--compact"], "info out.ora") if rc_["rc"] == 0 and os.path.exists(o2) else None
        n2 = B.layer_names(r2["json"]) if r2 and r2["json"] is not None else []
        ck.add(p + "ora_roundtrip_names", rc_["rc"] == 0 and all(n in n2 for n in exp), "convert exit %s; names after ORA to ORA: %s (expected %s)%s" % (rc_["rc"], n2, exp, ("; " + tail_err(rc_)) if rc_["rc"] else ""),
               "layer names survive a PhotoCraft ORA save (the playbook's read-back)")
        if rc_["rc"] == 0 and os.path.exists(o2):
            rc, out, err = B.run_py([os.path.join(B.RT, "validate_ora.py"), o2])
            findings.append({"id": p + "wp06_validator_on_photocraft_ora", "finding": "the WP-06 ORA validator on the ORA PhotoCraft wrote", "measured": "exit %s: %s" % (rc, " | ".join(out.strip().splitlines()[-2:])),
                             "implication": "an ORA PhotoCraft writes may differ from the emitter's (for example in layer paths or attributes); the reader must not assume the emitter's exact layout"})
        # ORA -> PSD -> info
        psd = os.path.join(d, name + ".out.psd")
        rc_ = cli.run(["convert", ora, psd], "convert %s.ora out.psd" % name)
        magic = open(psd, "rb").read(4) if os.path.exists(psd) else b""
        r3 = cli.json(["info", psd, "--compact"], "info out.psd") if rc_["rc"] == 0 and magic == b"8BPS" else None
        n3 = B.layer_names(r3["json"]) if r3 and r3["json"] is not None else []
        ck.add(p + "psd_names", rc_["rc"] == 0 and magic == b"8BPS" and all(n in n3 for n in exp), "convert exit %s, PSD signature %s; names in the PSD: %s (expected %s)%s" % (rc_["rc"], magic, n3, exp, ("; " + tail_err(rc_)) if rc_["rc"] else ""),
               "layer names survive ORA to PSD (the playbook: PhotoCraft offers a PSD when the work has adjustment layers, so the PSD must read back)")
        # PSD -> ORA -> info is how the pipeline would take a PhotoCraft PSD back; names again
        if rc_["rc"] == 0 and magic == b"8BPS":
            o3 = os.path.join(d, name + ".from_psd.ora")
            rc3 = cli.run(["convert", psd, o3], "convert out.psd out.ora")
            r4 = cli.json(["info", o3, "--compact"], "info from_psd.ora") if rc3["rc"] == 0 and os.path.exists(o3) else None
            n4 = B.layer_names(r4["json"]) if r4 and r4["json"] is not None else []
            findings.append({"id": p + "psd_back_to_ora", "finding": "names after ORA to PSD to ORA", "measured": "convert exit %s; %s (expected %s)" % (rc3["rc"], n4, exp), "implication": "whether a PhotoCraft PSD can be taken back to an ORA by the pipeline"})

    for name, ora in (("wp06", ora_wp06), ("at", ora_at)):
        ck.section("photocraft " + name, one, name, ora)
    return {"info_shapes": shapes}


# ----------------------------------------------------------------------------- VectorCraft
def svg_diff(a, b):
    """{id: {kind: 'circle->path', data: {attr: [before, after]}}} for every authored id whose element kind or data-* attributes differ (standard library)."""
    import xml.etree.ElementTree as ET

    def scan(path):
        out = {}
        for e in ET.parse(path).getroot().iter():
            i = e.get("id")
            if i:
                out[i] = (e.tag.split("}")[-1], {k: v for k, v in e.attrib.items() if k.startswith("data-")})
        return out
    sa, sb = scan(a), scan(b)
    res = {}
    for i, (tag, data) in sa.items():
        if tag in ("linearGradient", "radialGradient", "clipPath", "mask", "filter", "symbol", "stop"):
            continue
        if i not in sb:
            res[i] = {"lost": True}
            continue
        d = {}
        if sb[i][0] != tag:
            d["kind"] = "%s->%s" % (tag, sb[i][0])
        dd = {k: [v, sb[i][1].get(k)] for k, v in data.items() if sb[i][1].get(k) != v}
        if dd:
            d["data"] = dd
        if d:
            res[i] = d
    return res


def vectorcraft(cli, work, ck, findings):
    d = os.path.join(work, "vc")
    os.makedirs(d, exist_ok=True)
    rig = os.path.join(d, "wp06_rig.svg")
    ok, msg = B.make_wp06_rig(rig)
    if not ok:
        raise HarnessError("WP-06 rig emitter failed: " + msg[-200:])
    at = os.path.join(d, "at-rig.svg")
    shutil.copyfile(os.path.join(B.FIX, "at-rig.svg"), at)
    check_ids = os.path.join(B.FIX, "check_ids.py")
    gate = os.path.join(B.RT, "svg_rig.py")
    def one(name, src):
        p = "RB.vectorcraft.%s." % name
        out = os.path.join(d, name + ".rt.svg")
        r = cli.json(["convert", src, out], "convert %s.svg out.svg" % name)
        txt = open(out, encoding="utf-8", errors="replace").read(4000) if os.path.exists(out) else ""
        ck.add(p + "convert", r["rc"] == 0 and "<svg" in txt, "exit %s, output %s%s" % (r["rc"], "an SVG" if "<svg" in txt else "missing or not an SVG", ("; " + tail_err(r)) if r["rc"] else ""), "`convert in.svg out.svg` writes an SVG")
        if not os.path.exists(out):
            return
        j = r["json"] if isinstance(r["json"], dict) else {}
        findings.append({"id": p + "import_warnings", "finding": "what reading the input left out (importWarnings) and the export's own warnings", "measured": {"importWarnings": j.get("importWarnings"), "warnings": j.get("warnings")},
                         "implication": "the playbook expects the feColorMatrix filter of at-rig.svg to be named as ignored"})
        p1 = subprocess.run([sys.executable, "-I", check_ids, src, out], capture_output=True, text=True, timeout=60)
        lines = p1.stdout.strip().splitlines()
        ck.add(p + "check_ids_exit0", p1.returncode == 0, "reused check_ids.py exit %s: %s" % (p1.returncode, " || ".join(l[:160] for l in lines[:2])),
               "no authored id and no data-* attribute is lost (check_ids.py exits 0)")
        findings.append({"id": p + "check_ids_output", "finding": "the reused check_ids.py output lines (viewBox, classes, style)", "measured": [l[:200] for l in lines], "implication": "the viewBox change from 100 50 400 300 to 0 0 400 300 is expected for at-rig.svg (research/craft-visual.md)"})
        findings.append({"id": p + "element_diff", "finding": "per authored id: element kind and data-* attributes before and after (only the differences)", "measured": svg_diff(src, out),
                         "implication": "a circle or rect that became a path keeps its id and its transform, but a script that animates cx, cy, r, x, y, width or height no longer finds those attributes"})
        rc, gout, gerr = B.run_py([gate, "gate", src, out, "--label", name])
        ck.add(p + "wp06_gate_exit0", rc == 0, "svg_rig.py gate exit %s: %s" % (rc, " | ".join(gout.strip().splitlines()[-2:])), "the WP-06 gate (check_ids.py plus the element-kind rule) passes")
        inf = cli.json(["info", src], "info %s.svg" % name)
        ck.add(p + "info_json", inf["rc"] == 0 and isinstance(inf["json"], dict), "exit %s, %s" % (inf["rc"], "JSON" if inf["json"] is not None else "no JSON: " + tail_err(inf)), "`info <svg>` prints a JSON summary")
        if isinstance(inf["json"], dict):
            findings.append({"id": p + "info_shape", "finding": "the key structure of `info`", "measured": L.shape_of(inf["json"], 2), "implication": ""})
    for name, src in (("wp06", rig), ("at", at)):
        ck.section("vectorcraft " + name, one, name, src)
    # the playbook's step 4: PNG and PDF export at scale 2
    png, pdf = os.path.join(d, "at-rig.png"), os.path.join(d, "at-rig.pdf")
    r = cli.run(["run", "--in", at, "--export", png, "--export", pdf, "--scale", "2"], "run --in at-rig.svg --export png --export pdf --scale 2")
    sz = B.image_size(png) if os.path.exists(png) and open(png, "rb").read(8) == b"\x89PNG\r\n\x1a\n" else None
    pdf_ok = os.path.exists(pdf) and open(pdf, "rb").read(5) == b"%PDF-"
    ck.add("RB.vectorcraft.at.export_png_pdf", r["rc"] == 0 and sz is not None and pdf_ok and abs(sz[0] / float(sz[1]) - 4 / 3.0) < 0.02,
           "exit %s, PNG size %s, PDF %s%s" % (r["rc"], sz, "valid header" if pdf_ok else "missing", ("; " + tail_err(r)) if r["rc"] else ""), "both files are written; the PNG keeps the 4:3 shape (the playbook's step 4)")
    return {}


# ----------------------------------------------------------------------------- LightCraft
def lightcraft(cli, work, ck, findings):
    d = os.path.join(work, "lc")
    prints = os.path.join(d, "prints")
    out = os.path.join(d, "out")
    os.makedirs(prints, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    src = os.path.join(d, "print.jpg")
    B.make_test_jpeg(src, 3000, 2000)
    env = {"LIGHTCRAFT_GPU": "0"}
    dst = os.path.join(d, "print.out.jpg")
    r = cli.run(["render", src, "-o", dst, "--set", "light.exposure=0.3", "--set", "color.vibrance=25", "--size", "2048", "--quality", "92"], "render print.jpg (LIGHTCRAFT_GPU=0)", extra_env=env)
    isjpg = os.path.exists(dst) and open(dst, "rb").read(2) == b"\xff\xd8"
    sz = B.image_size(dst) if isjpg else None
    ck.add("RB.lightcraft.render_written", r["rc"] == 0 and isjpg and sz is not None and max(sz) == 2048, "exit %s, JPEG %s, size %s%s" % (r["rc"], isjpg, sz, ("; " + tail_err(r)) if r["rc"] else ""),
           "LIGHTCRAFT_GPU=0 render writes a JPEG with a 2048 px long edge (playbook five-minute test, step 2)")
    if isjpg:
        a, b = B.mean_luma(src), B.mean_luma(dst)
        ck.add("RB.lightcraft.render_brighter", b >= a + 2.0, "mean luma %.1f -> %.1f (exposure +0.3; mark: at least +2 levels, a planner's proposal)" % (a, b), "the file is brighter")
    # the reused steps file with this folder's paths
    for i in range(3):   # three DIFFERENT cards: LightCraft's import skips content duplicates (found by the first real run, where the three cards were identical)
        B.make_test_jpeg(os.path.join(prints, "scan%02d.jpg" % (i + 1)), 1200, 800, variant=i + 1)
    preset = os.path.join(d, "faded-print-a.lcpreset")
    shutil.copyfile(os.path.join(B.FIX, "faded-print-a.lcpreset"), preset)
    steps = os.path.join(d, "steps.jsonl")
    swaps = {"C:\\lj\\at\\prints": prints, "C:\\lj\\at\\faded-print-a.lcpreset": preset, "C:\\lj\\at\\out": out}
    n_lines = 0
    with open(steps, "w", encoding="utf-8", newline="\n") as f:
        for ln in open(os.path.join(B.FIX, "at-lightcraft-steps.jsonl"), encoding="utf-8"):
            if not ln.strip():
                continue
            obj = json.loads(ln)

            def sub(o):
                if isinstance(o, str):
                    return swaps.get(o, o)
                if isinstance(o, list):
                    return [sub(x) for x in o]
                if isinstance(o, dict):
                    return {k: sub(v) for k, v in o.items()}
                return o
            f.write(json.dumps(sub(obj)) + "\n")
            n_lines += 1
    lib = os.path.join(d, "lib")
    os.makedirs(lib, exist_ok=True)
    r = cli.run(["run", "--library", lib, "--script", steps], "run --library --script (preset import, apply, two exports)", extra_env=env)
    res = []
    for ln in r["stdout"].splitlines():
        ln = ln.strip()
        if ln.startswith("{"):
            try:
                res.append(json.loads(ln))
            except ValueError:
                pass
    bad = [x for x in res if x.get("ok") is False]
    ck.add("RB.lightcraft.script_ran", r["rc"] == 0 and len(res) >= n_lines and not bad, "exit %s, %d JSON result lines for %d steps, %d with ok=false%s" % (r["rc"], len(res), n_lines, len(bad), ("; " + tail_err(r)) if r["rc"] else ""),
           "the steps file runs: every result line parses and none says ok=false (playbook step 3)")
    findings.append({"id": "RB.lightcraft.result_line_shape", "finding": "the key structure of one result line per step", "measured": [L.shape_of(x, 2) for x in res[:6]], "implication": "the playbook says each line must have ok true"})
    findings.append({"id": "RB.lightcraft.run_stdout_excerpt", "finding": "the start of the script run's output (so a surprise in the result shape can be read from the evidence)", "measured": B.excerpt(r["stdout"], 900), "implication": ""})
    # the EXACT id, read from the preset.import result (a substring match would accept a renamed 'lj-faded-print-a-2'); the quoted-id search is the fallback if the result has another shape
    ids = [e.get("id") for x in res if x.get("command") == "preset.import" and isinstance(x.get("result"), dict) for e in (x["result"].get("imported") or []) if isinstance(e, dict)]
    exact = "lj-faded-print-a" in ids if ids else any('"id": "lj-faded-print-a"' in json.dumps(x) for x in res if x.get("command") == "preset.import")
    ck.add("RB.lightcraft.preset_id_kept", exact, "preset.import imported ids: %s (expected lj-faded-print-a exactly)" % (ids or "none read"), "the .lcpreset import keeps the id lj-faded-print-a (no clash), so preset.apply can find it")
    jp = sorted(x for x in os.listdir(out) if x.lower().endswith(".jpg"))
    tf = sorted(x for x in os.listdir(out) if x.lower().endswith((".tif", ".tiff")))
    jmagic = all(open(os.path.join(out, x), "rb").read(2) == b"\xff\xd8" for x in jp) if jp else False
    tmagic = all(open(os.path.join(out, x), "rb").read(4) in (b"II*\x00", b"MM\x00*") for x in tf) if tf else False
    imported = sum(len(x.get("result", {}).get("imported", [])) for x in res if x.get("command") == "library.import" and isinstance(x.get("result"), dict))
    dupes = sum(len(x.get("result", {}).get("duplicates", [])) for x in res if x.get("command") == "library.import" and isinstance(x.get("result"), dict))
    findings.append({"id": "RB.lightcraft.import_counts", "finding": "library.import of the prints folder: items imported and content duplicates skipped", "measured": {"files_in_folder": 3, "imported": imported, "duplicates_skipped": dupes},
                     "implication": "LightCraft skips a file whose content equals one already in the library: two identical scans import as one"})
    ck.add("RB.lightcraft.import_all_distinct_prints", imported == 3 and dupes == 0, "3 distinct synthetic prints: %d imported, %d skipped as duplicates" % (imported, dupes), "every distinct print in the folder reaches the library")
    ck.add("RB.lightcraft.exports_written", len(jp) == 3 and len(tf) == 3 and jmagic and tmagic, "JPEG exports %s, TIFF exports %s, JPEG magic %s, TIFF magic %s" % (jp, tf, jmagic, tmagic),
           "one JPEG and one 16-bit TIFF per print, named {name}-{seq:2}")
    if tf:
        ident = subprocess.run(["identify", "-format", "%z %[colorspace]", os.path.join(out, tf[0])], capture_output=True, text=True, timeout=60)
        findings.append({"id": "RB.lightcraft.tiff_depth", "finding": "bit depth and colour space of the first TIFF export (ImageMagick identify)", "measured": ident.stdout.strip() or ident.stderr.strip()[:100], "implication": "the steps ask for bitDepth 16"})
    # running the preset import twice is documented as harmless; a finding, not a criterion (the one-line syntax is the part not shown by the playbook)
    again = cli.run(["run", "--library", lib, "preset.import", 'paths=["%s"]' % preset], "run preset.import (second time)", extra_env=env)
    findings.append({"id": "RB.lightcraft.preset_import_twice", "finding": "the same preset imported a second time", "measured": "exit %s: %s" % (again["rc"], first_line(again["stdout"] or again["stderr"])[:200]), "implication": "the playbook says identical presets are skipped"})
    return {}
