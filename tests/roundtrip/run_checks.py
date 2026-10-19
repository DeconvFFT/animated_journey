#!/usr/bin/env python3
"""run_checks.py: the WP-06 test driver (called by tests/roundtrip/run_tests.sh; it can also be run alone).

  python3 -I tests/roundtrip/run_checks.py --mode quick|all [--work renders/wp06] [--evidence build/evidence/wp06] [--keep]

One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
and one evidence envelope per test (build plan 4.2) written to <evidence>/tests_<mode>.jsonl (tests_quick.jsonl or tests_all.jsonl: one file per mode, so a later
--quick run, for example the shared WP-11a runner's, can not overwrite the --all evidence). Exit 0 if no line is FAIL or BLOCKED, 1 if a line FAILs,
3 if a line is BLOCKED. UNVERIFIED (Windows or Craft-app behaviour) and SKIPPED are listed and never counted as a pass.
Set LJ_WP06_COUNTS=PATH to also write the run's peak size and lowest free space there (make_evidence.sh does; a normal run leaves no extra file).

What it covers (the WP-06 acceptance list): the ORA emitter and validator (R8 rules, the reused make_ora.py and at-layers.ora as references, nineteen planted
defects, and a test that holds a reference file to the same value rules), the SVG rig through Inkscape plain-SVG export and the reused check_ids.py (clean pass-through, three planted defects, the Inkscape data-* finding),
the OTIO emitter and validator (rebased from the 25 fps template, JSON-level rules, the opentimelineio 0.18.1 load, twenty-seven planted defects), kb_scale.py
(45.0, 53.3, 66.67), and adapter_probe.sh (reused make_otio.py unchanged).

Everything is generated at test time from synthetic content (test cards, a sine tone, a geometric rig) under the --work folder (git-ignored renders/wp06) and
removed again unless --keep. No family media exists here and none is created or simulated. The mode quick takes well under a minute, uses no network and
no timed runs; all adds the plug-in adapter probe (pip, about 4 MB).
"""
import argparse
import ast
import datetime
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline", "roundtrip"))
import plant  # noqa: E402

PY = [sys.executable, "-I", "-B"]
RT = os.path.join(ROOT, "pipeline", "roundtrip")
SCRATCH = os.environ.get("LJ_SCRATCH", os.path.normpath(os.path.join(ROOT, "..", "build-scratch")))
VENV_PY = os.path.join(SCRATCH, "venv-otio", "bin", "python")
CRAFT_VIS = os.path.join(ROOT, "research", "craft-visual-fixtures")
REUSED = ["research/craft-visual-fixtures/make_ora.py", "research/craft-visual-fixtures/check_ids.py", "research/craft-visual-fixtures/at-layers.ora",
          "research/sources/format-round1/make_otio.py"]
STATE = {"counts": {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0}, "min_avail": None, "peak_work_mb": 0.0}
ARGS = None
S = {}      # state shared between tests (paths made by earlier tests)


# ----------------------------------------------------------------------------------------------- plumbing
def sh(args, timeout=300, env=None, cwd=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd or ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, env=e)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def avail_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", "/"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20).stdout.decode()
        return int(re.sub(r"[^0-9]", "", out.strip().splitlines()[-1].split()[3]))
    except Exception:
        return 0


def clean(s):
    s = str(s).replace(ROOT, ".").replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return s[:700]


def tree_mb(path):
    total = 0
    for dp, dn, fn in os.walk(path):
        for f in fn:
            try:
                total += os.lstat(os.path.join(dp, f)).st_size
            except OSError:
                pass
    return total / 1048576.0


def record(name, status, expected, actual, unverified="", notes=""):
    STATE["counts"][status] += 1
    a = avail_mb()
    s0 = ARGS.t_start
    lo = min([x for x in (s0, a) if x] or [0])
    STATE["min_avail"] = lo if STATE["min_avail"] is None else min(STATE["min_avail"], lo)
    STATE["peak_work_mb"] = max(STATE["peak_work_mb"], tree_mb(ARGS.work))
    env = {"platform": "linux", "python": "%d.%d.%d" % sys.version_info[:3], "nproc": os.cpu_count(), "opentimelineio": S.get("otio_version", "not probed"),
           "inkscape": S.get("inkscape_version", "not probed")}
    rec = {"schema": "lj-evidence/1", "package": "WP-06", "test": name, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
           "status": status, "env": env,
           "disk": {"avail_mb_start": s0, "planned_write_mb": 0, "avail_mb_min": lo, "avail_mb_end": a, "floor_mb": 400, "hard_floor_mb": 250},
           "expected": clean(expected), "actual": clean(actual), "notes": clean(notes), "unverified_reasons": [unverified] if unverified else []}
    with open(ARGS.jsonl, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("%-10s %-46s %s" % (status, name, clean(actual)[:170].replace("\n", " ")), flush=True)


REG = []


def test(name, modes=("quick", "all")):
    def deco(fn):
        REG.append((name, modes, fn))
        return fn
    return deco


class Skip(Exception):
    pass


def check(name, ok, expected, actual, unverified="", notes=""):
    record(name, "PASS" if ok else "FAIL", expected, actual, unverified, notes)
    return ok


def work(*p):
    return os.path.join(ARGS.work, *p)


def evid(*p):
    return os.path.join(ARGS.evidence, *p)


def tool(name):
    return os.path.join(RT, name)


def failed_codes(out):
    m = re.search(r"^FAILED: (.*)$", out, re.M)
    return set(x.strip() for x in m.group(1).split(",")) if m else set()


def last(out, n=1):
    return " | ".join(out.strip().splitlines()[-n:])


def read_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def require(path, what):
    if not os.path.exists(path):
        raise Skip("%s is missing (an earlier test did not produce it)" % what)


# ----------------------------------------------------------------------------------------------- hygiene
OWNED_PY = ["pipeline/roundtrip/rt_common.py", "pipeline/roundtrip/validate_ora.py", "pipeline/roundtrip/emit_ora_layers.py", "pipeline/roundtrip/make_media.py",
            "pipeline/roundtrip/svg_rig.py", "pipeline/roundtrip/emit_otio.py", "pipeline/roundtrip/validate_otio.py", "pipeline/roundtrip/kb_scale.py",
            "tests/roundtrip/run_checks.py", "tests/roundtrip/plant.py", "tests/roundtrip/make_evidence.py"]
OWNED_SH = ["pipeline/roundtrip/svg_roundtrip.sh", "pipeline/roundtrip/adapter_probe.sh", "tests/roundtrip/run_tests.sh", "tests/roundtrip/make_evidence.sh"]


@test("hygiene.py_compile")
def t_compile():
    bad = []
    tmp = work("pyc_check")
    os.makedirs(tmp, exist_ok=True)
    for n, f in enumerate(OWNED_PY):
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            bad.append(f + " (missing)")
            continue
        try:
            py_compile.compile(p, cfile=os.path.join(tmp, "%d.pyc" % n), doraise=True)      # compiled into the work folder, never next to the source
        except py_compile.PyCompileError as e:
            bad.append("%s: %s" % (f, str(e)[:80]))
    shutil.rmtree(tmp, ignore_errors=True)
    check("hygiene.py_compile", not bad, "every .py compiles", "; ".join(bad) or "%d files compile" % len(OWNED_PY))
    old_grammar = []
    for f in OWNED_PY:
        if f.startswith("pipeline/"):
            try:
                ast.parse(open(os.path.join(ROOT, f), encoding="utf-8").read(), feature_version=(3, 8))
            except SyntaxError as e:
                old_grammar.append("%s: %s" % (f, e))
    check("hygiene.python38_grammar", not old_grammar, "the pipeline tools parse with the Python 3.8 grammar (the maker's PC may run an older 3.x)",
          "; ".join(old_grammar) or "all pipeline/roundtrip tools parse")


@test("hygiene.bash_syntax")
def t_bash():
    bad = []
    for f in OWNED_SH:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            bad.append(f + " (missing)")
            continue
        rc, o, e = sh(["bash", "-n", p])
        if rc:
            bad.append("%s: %s" % (f, e.strip()[:80]))
    check("hygiene.bash_syntax", not bad, "bash -n passes on every script", "; ".join(bad) or "%d scripts parse" % len(OWNED_SH))


@test("hygiene.stdlib_only")
def t_stdlib():
    ok_mods = set(sys.stdlib_module_names) | {"rt_common", "kb_scale", "make_media", "plant", "emit_otio"}
    third = {"PIL"}      # Pillow: only the three generators, and only inside functions
    bad = []
    pillow_files = []
    for f in OWNED_PY:
        tree = ast.parse(open(os.path.join(ROOT, f), encoding="utf-8").read())
        top = set()
        lazy = set()
        for node in ast.walk(tree):
            names = [a.name.split(".")[0] for a in node.names] if isinstance(node, ast.Import) else (
                [node.module.split(".")[0]] if isinstance(node, ast.ImportFrom) and node.module else [])
            for n in names:
                (top if n in ok_mods else lazy).add(n)
        extra = lazy - third
        if extra:
            bad.append("%s imports %s" % (f, sorted(extra)))
        if "PIL" in lazy:
            pillow_files.append(os.path.basename(f))
    check("hygiene.stdlib_only", not bad, "only the standard library (Pillow only in the generators)", "; ".join(bad) or "Pillow only in %s" % ", ".join(sorted(pillow_files)))
    # the validators must not need Pillow at all (they run on the maker's PC too)
    validators = [f for f in pillow_files if f.startswith("validate_") or f in ("kb_scale.py", "rt_common.py", "svg_rig.py", "emit_otio.py")]
    check("hygiene.validators_need_no_pillow", not validators, "validators, kb_scale, svg_rig and emit_otio do not import Pillow", ", ".join(validators) or "none do")


@test("hygiene.not_a_photo")
def t_nophoto():
    bad = []
    for f in ("pipeline/roundtrip/emit_ora_layers.py", "pipeline/roundtrip/make_media.py", "pipeline/roundtrip/svg_rig.py", "pipeline/roundtrip/emit_otio.py"):
        src = open(os.path.join(ROOT, f), encoding="utf-8").read()
        if re.search(r"Image\.open\(|ImageFile|\.jpg|\.jpeg|\.heic|\.tif", src):
            bad.append(f)
    check("hygiene.not_a_photo", not bad, "the generators never open an image file and name no photo format", ", ".join(bad) or "no Image.open, no jpg/heic/tif in any generator")


@test("hygiene.reused_unchanged")
def t_reused():
    rc, o, e = sh(["git", "diff", "--quiet", "--"] + REUSED)
    rc2, o2, e2 = sh(["git", "status", "--porcelain", "--"] + REUSED)
    check("hygiene.reused_unchanged", rc == 0 and not o2.strip(), "make_ora.py, check_ids.py, at-layers.ora and make_otio.py are byte-identical to HEAD",
          "git diff empty, status clean" if rc == 0 and not o2.strip() else "changed: " + o2.strip()[:200])


@test("hygiene.spec_json")
def t_spec():
    d = read_json(os.path.join(RT, "spec", "neutral_timeline.example.json"))
    ok = d.get("fps") == 24 and len(d["shots"]) == 4 and all(s.get("transition_out", {}).get("frames") == 24 for s in d["shots"][:3]) and d.get("synthetic_media") is True
    check("hygiene.spec_json", ok, "24 fps, four shots, three 24-frame dissolves, marked synthetic", "fps %s, %d shots" % (d.get("fps"), len(d["shots"])))


@test("hygiene.no_stale_rate")
def t_stale():
    # build the stale strings at run time so this file is not itself a hit
    r25 = str(24 + 1)
    pats = [re.compile(r"\b%s\s*fps\b" % r25, re.I), re.compile(r"fps\s*[=:]\s*%s\b" % r25), re.compile(r"\"rate\"\s*:\s*%s\b" % r25), re.compile(r"-r %s\b" % r25)]
    hits = []
    for base in ("pipeline/roundtrip", "tests/roundtrip"):
        for dp, dn, fn in os.walk(os.path.join(ROOT, base)):
            for f in fn:
                if not f.endswith((".py", ".sh", ".json", ".md")):
                    continue
                for i, line in enumerate(open(os.path.join(dp, f), encoding="utf-8", errors="replace"), 1):
                    if any(p.search(line) for p in pats) and "template" not in line.lower() and "old project rate" not in line.lower():
                        hits.append("%s:%d" % (os.path.relpath(os.path.join(dp, f), ROOT), i))
    check("hygiene.no_stale_rate", not hits, "no 25 fps default in a new file (mentions of the old template are allowed)", ", ".join(hits[:6]) or "no hits")


@test("hygiene.public_lint")
def t_lint():
    paths = ["pipeline/roundtrip", "tests/roundtrip", "build/evidence/wp06"]
    rc, o, e = sh(PY + ["scripts/public_lint.py", "--paths"] + [p for p in paths if os.path.exists(os.path.join(ROOT, p))])
    check("hygiene.public_lint", rc == 0, "public_lint.py exits 0 on the owned paths and the evidence", last(o) or last(e))
    rc, o, e = sh(PY + ["scripts/public_lint.py", "--theme", "--paths", "pipeline/roundtrip", "tests/roundtrip"])
    check("hygiene.theme_guard", rc == 0, "the D-28 keyword guard finds nothing in the owned paths", last(o, 2))


PYCACHE_BASES = ("pipeline/roundtrip", "tests/roundtrip")


def pycache_snapshot():
    """{__pycache__ folder relative to the repo: {(file name, mtime_ns, size)}} for every __pycache__ under the owned paths (an empty folder is an empty set)."""
    snap = {}
    for base in PYCACHE_BASES:
        for dp, dn, fn in os.walk(os.path.join(ROOT, base)):
            if os.path.basename(dp) != "__pycache__":
                continue
            files = set()
            for f in fn:
                try:
                    st = os.lstat(os.path.join(dp, f))
                    files.add((f, st.st_mtime_ns, st.st_size))
                except OSError:
                    pass
            snap[os.path.relpath(dp, ROOT).replace(os.sep, "/")] = files
    return snap


def pycache_new(before, after):
    """What appeared between two snapshots: a new __pycache__ folder (name/), or a new or rewritten file inside an old one (name/file)."""
    out = []
    for folder, files in sorted(after.items()):
        if folder not in before:
            out.append(folder + "/")
        else:
            out += ["%s/%s" % (folder, f[0]) for f in sorted(files - before[folder])]
    return out


@test("hygiene.no_pycache")
def t_pycache():
    # A __pycache__ that was already there when the run began is not this package's doing (any later tool that imports plant.py without -B leaves one),
    # so it is only a failure if git would not ignore it. What this run must not do is make one, or write into one.
    new = pycache_new(S.get("pycache_start", {}), pycache_snapshot())
    old = sorted(S.get("pycache_start", {}))
    unignored = []
    for folder in old:
        try:
            rc, o, e = sh(["git", "check-ignore", "-q", folder])
        except OSError:
            break                      # no git here: nothing to compare with, the folder is only reported
        if rc == 1:
            unignored.append(folder)
    detail = "none created during the run" + ("; %d already there at the start, all git-ignored, left alone" % len(old) if old and not unignored else "")
    if new:
        detail = "created during the run: " + ", ".join(new[:6])
    elif unignored:
        detail = "already there and NOT git-ignored (it could be committed): " + ", ".join(unignored[:6])
    check("hygiene.no_pycache", not new and not unignored,
          "the run creates no __pycache__ folder or .pyc file under the owned paths (one that was already there and is git-ignored is not this run's)", detail)


@test("hygiene.no_pycache_detects")
def t_pycache_detects():
    a = {"tests/roundtrip/__pycache__": {("plant.cpython-313.pyc", 1, 10)}}
    cases = [("nothing changed", a, dict(a), []),
             ("a new folder", a, dict(a, **{"pipeline/roundtrip/__pycache__": set()}), ["pipeline/roundtrip/__pycache__/"]),
             ("a new file in an old folder", a, {"tests/roundtrip/__pycache__": a["tests/roundtrip/__pycache__"] | {("rt_common.cpython-313.pyc", 2, 20)}},
              ["tests/roundtrip/__pycache__/rt_common.cpython-313.pyc"]),
             ("a rewritten file", a, {"tests/roundtrip/__pycache__": {("plant.cpython-313.pyc", 3, 10)}}, ["tests/roundtrip/__pycache__/plant.cpython-313.pyc"]),
             ("a folder that went away", a, {}, []),
             ("nothing before, a folder after", {}, a, ["tests/roundtrip/__pycache__/"])]
    bad = [n for n, b, c, want in cases if pycache_new(b, c) != want]
    check("hygiene.no_pycache_detects", not bad, "the comparison used by hygiene.no_pycache sees a new folder, a new file and a rewritten file, and ignores one that was already there",
          "all %d cases right" % len(cases) if not bad else "wrong: " + ", ".join(bad))


# ----------------------------------------------------------------------------------------------- kb_scale
@test("kb_scale.selftest")
def t_kb_self():
    rc, o, e = sh(PY + [tool("kb_scale.py"), "--selftest"])
    check("kb_scale.selftest", rc == 0 and "PASS" in o, "the unit tests pass", last(o))


@test("kb_scale.values")
def t_kb_vals():
    rows = {}
    for w, h in ((3600, 2400), (2880, 1620)):
        rc, o, e = sh(PY + [tool("kb_scale.py"), str(w), str(h), "--json"])
        rows[(w, h)] = json.loads(o) if rc == 0 else {}
    a, b = rows[(3600, 2400)], rows[(2880, 1620)]
    ok = (a.get("fit_1dp") == 45.0 and a.get("cover_1dp") == 53.3 and b.get("fit") == 66.67 and b.get("cover") == 66.67)
    check("kb_scale.values", ok, "3600x2400: fit 45.0, cover 53.3; 2880x1620: 66.67 for both",
          "3600x2400 fit %s cover %s (%s); 2880x1620 fit %s cover %s" % (a.get("fit_1dp"), a.get("cover_1dp"), a.get("cover"), b.get("fit"), b.get("cover")))
    with open(evid("kb_scale.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"3600x2400": a, "2880x1620": b}, f, indent=2, sort_keys=True)
        f.write("\n")


@test("kb_scale.cli_errors")
def t_kb_cli():
    rc1, o1, e1 = sh(PY + [tool("kb_scale.py")])
    rc2, o2, e2 = sh(PY + [tool("kb_scale.py"), "0", "100"])
    rc3, o3, e3 = sh(PY + [tool("kb_scale.py"), "100", "100", "--seq", "bad"])
    check("kb_scale.cli_errors", (rc1, rc2, rc3) == (2, 2, 2), "no size, a zero size and a bad --seq all exit 2", "exits %s %s %s" % (rc1, rc2, rc3))


# ----------------------------------------------------------------------------------------------- ORA
@test("ora.emit_validate")
def t_ora_emit():
    out = work("layers.ora")
    rc, o, e = sh(PY + [tool("emit_ora_layers.py"), out])
    check("ora.emit", rc == 0 and os.path.isfile(out), "emit_ora_layers.py exits 0 and writes the .ora", last(o) or last(e))
    rc, o, e = sh(PY + [tool("validate_ora.py"), out, "--json", evid("ora_validate_layers.json")])
    d = read_json(evid("ora_validate_layers.json")) if os.path.exists(evid("ora_validate_layers.json")) else {}
    check("ora.validate_emitted", rc == 0 and d.get("extra", {}).get("profile") == "pipeline" and d.get("counts", {}).get("WARN") == 0,
          "validate_ora.py exits 0 under the pipeline profile with no WARN", "exit %d; %s" % (rc, last(o)))
    S["ora"] = out


@test("ora.determinism")
def t_ora_det():
    require(work("layers.ora"), "layers.ora")
    import hashlib
    other = work("layers_again.ora")
    sh(PY + [tool("emit_ora_layers.py"), other])
    h = [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (work("layers.ora"), other)]
    os.remove(other)
    check("ora.determinism", h[0] == h[1], "two emits give the same bytes", "sha256 %s" % h[0][:16])


@test("ora.layer_content")
def t_ora_content():
    require(work("layers.ora"), "layers.ora")
    import io
    import xml.etree.ElementTree as ET
    import zipfile
    from PIL import Image
    z = zipfile.ZipFile(work("layers.ora"))
    root = ET.fromstring(z.read("stack.xml"))
    layers = [l.attrib for l in root.iter("layer")]
    names = [l["name"] for l in layers]
    ok_names = names == ["L30_label", "L20_figure", "L10_restored", "L00_asfound"]
    modes = {}
    partial_alpha = False
    for l in layers:
        im = Image.open(io.BytesIO(z.read(l["src"])))
        modes[l["name"]] = im.mode
        if l["name"] == "L20_figure":
            a = im.getchannel("A")
            lo, hi = a.getextrema()
            hist = a.histogram()
            partial_alpha = lo == 0 and hi == 255 and sum(hist[1:255]) > 0
    merged = Image.open(io.BytesIO(z.read("mergedimage.png")))
    check("ora.layer_content", ok_names and set(modes.values()) == {"RGBA"} and partial_alpha and merged.size == (640, 360),
          "four layers named by id, L00_asfound last (bottom), RGBA, straight alpha with partial values, merged at canvas size",
          "names %s; modes %s; partial alpha %s; merged %s" % (names, sorted(set(modes.values())), partial_alpha, merged.size))


@test("ora.reference_make_ora")
def t_ora_ref():
    ref = work("make_ora_ref.ora")
    scratch = os.path.join(SCRATCH, "wp06", "make_ora_cwd")
    os.makedirs(scratch, exist_ok=True)
    rc, o, e = sh(PY + [os.path.join(CRAFT_VIS, "make_ora.py"), ref], cwd=scratch)
    shutil.rmtree(scratch, ignore_errors=True)
    check("ora.reference_make_ora_runs", rc == 0 and os.path.isfile(ref), "the reused make_ora.py runs unchanged (cwd in scratch) and writes the file", last(o) or last(e))
    if not os.path.isfile(ref):
        return
    rc, o, e = sh(PY + [tool("validate_ora.py"), ref])
    check("ora.reference_make_ora_validates", rc == 0, "validate_ora.py exits 0 on its output", last(o))
    import zipfile
    a, b = zipfile.ZipFile(ref), zipfile.ZipFile(os.path.join(CRAFT_VIS, "at-layers.ora"))
    same = [n for n in ("stack.xml", "data/title.png", "data/photo.png", "mergedimage.png") if a.read(n) == b.read(n)]
    check("ora.reference_matches_fixture", len(same) == 4, "make_ora.py reproduces at-layers.ora (stack.xml and the three PNGs byte for byte)", "identical members: %s" % ", ".join(same))


@test("ora.at_layers")
def t_ora_at():
    rc, o, e = sh(PY + [tool("validate_ora.py"), os.path.join(CRAFT_VIS, "at-layers.ora"), "--json", evid("ora_validate_at_layers.json")])
    d = read_json(evid("ora_validate_at_layers.json"))
    warn_codes = [c["code"] for c in d["checks"] if c["status"] == "WARN"]
    check("ora.at_layers", rc == 0 and d["extra"]["profile"] == "reference" and warn_codes == ["layer_name_invalid"],
          "validate_ora.py exits 0 on research/craft-visual-fixtures/at-layers.ora (reference profile; its names 'Title tint' and 'Photo' are a WARN)",
          "exit %d; profile %s; WARN %s" % (rc, d["extra"]["profile"], warn_codes))
    rc2, o2, e2 = sh(PY + [tool("validate_ora.py"), os.path.join(CRAFT_VIS, "at-layers.ora"), "--profile", "pipeline"])
    check("ora.at_layers_strict", rc2 == 1 and {"layer_name_invalid", "asfound_not_bottom"} <= failed_codes(o2),
          "under --profile pipeline the same file fails on its names and the missing L00_asfound (so the reference profile is a choice, not a blind spot)",
          "exit %d; %s" % (rc2, last(o2)))


@test("ora.reference_values_strict")
def t_ora_ref_values():
    # review r1, break test B4: a bad layer value in a file under the reference profile (at-layers.ora) was only a WARN. Values are structural, so it must fail there too.
    src = os.path.join(CRAFT_VIS, "at-layers.ora")
    cases = [("opacity 1.5", 'opacity="0.6"', 'opacity="1.5"'), ("opacity not a number", 'opacity="0.6"', 'opacity="high"'),
             ("visibility shown", 'visibility="visible"', 'visibility="shown"'), ("composite-op unknown", 'composite-op="svg:multiply"', 'composite-op="svg:bogus"'),
             ("x fractional", 'x="24"', 'x="12.5"'), ("y not a number", 'y="24"', 'y="-"')]
    rows = []
    for name, old, new in cases:
        dst = work("ref_value_%d.ora" % len(rows))
        m = plant.read_members(src)
        plant._stack(m, lambda t, old=old, new=new: t.replace(old, new, 1))
        plant.write_members(dst, m)
        rc, o, e = sh(PY + [tool("validate_ora.py"), dst])
        rows.append((name, rc, failed_codes(o), "profile=reference" in o))
        os.remove(dst)
    ok = all(rc == 1 and got == {"layer_value_invalid"} and ref for _, rc, got, ref in rows)
    check("ora.reference_values_strict", ok, "a bad opacity, visibility, composite-op, x or y in at-layers.ora (reference profile) exits 1 naming layer_value_invalid, not a WARN",
          "; ".join("%s -> exit %d %s%s" % (n, rc, sorted(got), "" if ref else " (NOT the reference profile)") for n, rc, got, ref in rows))


@test("ora.usage")
def t_ora_usage():
    rc1, o1, e1 = sh(PY + [tool("validate_ora.py"), work("no_such_file.ora")])
    rc2, o2, e2 = sh(PY + [tool("validate_ora.py")])
    rc3, o3, e3 = sh(PY + [tool("emit_ora_layers.py"), work("x.ora"), "--width", "100"])
    check("ora.usage", (rc1, rc2, rc3) == (2, 2, 2), "a missing file, no argument and a too-small canvas exit 2", "exits %s %s %s" % (rc1, rc2, rc3))


@test("ora.planted_defects")
def t_ora_plant():
    require(work("layers.ora"), "layers.ora")
    table = {}
    for kind, (code, why) in plant.ORA_DEFECTS.items():
        dst = work("plant_ora_%s.ora" % kind)
        plant.plant_ora(kind, work("layers.ora"), dst)
        rc, o, e = sh(PY + [tool("validate_ora.py"), dst])
        got = failed_codes(o)
        table[kind] = {"expected_code": code, "exit": rc, "failed_codes": sorted(got), "described_as": why}
        check("ora.plant.%s" % kind, rc == 1 and got == {code}, "exit 1 naming exactly %s (%s)" % (code, why), "exit %d; FAILED %s" % (rc, sorted(got) or "nothing"))
        os.remove(dst)
    with open(evid("planted_defects_ora.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(table, f, indent=2, sort_keys=True)
        f.write("\n")


@test("ora.nested_groups")
def t_ora_groups():
    require(work("layers.ora"), "layers.ora")
    a, b, c = work("grp_a.ora"), work("grp_b.ora"), work("grp_c.ora")
    plant.nested_group_ora(work("layers.ora"), a, "0.0.3", True)
    plant.nested_group_ora(work("layers.ora"), b, "0.0.6", True)
    plant.nested_group_ora(work("layers.ora"), c, "0.0.6", False)
    ra = sh(PY + [tool("validate_ora.py"), a])
    rb = sh(PY + [tool("validate_ora.py"), b])
    rc = sh(PY + [tool("validate_ora.py"), c])
    for p in (a, b, c):
        os.remove(p)
    check("ora.nested_groups", ra[0] == 0 and rb[0] == 0 and rc[0] == 0 and "WARN group_isolation_implicit" in rc[1] and "WARN group_isolation_implicit" not in rb[1],
          "a nested group validates (exit 0); a version 0.0.6 group without isolation is a WARN (v0.10.0 reads it as isolate), with isolation it is clean",
          "exits %d %d %d; %s" % (ra[0], rb[0], rc[0], last(rc[1])))


@test("ora.offcanvas_option")
def t_ora_off():
    require(work("layers.ora"), "layers.ora")
    dst = work("plant_ora_off.ora")
    plant.plant_ora("layer_outside_canvas", work("layers.ora"), dst)
    rc, o, e = sh(PY + [tool("validate_ora.py"), dst, "--allow-offcanvas"])
    os.remove(dst)
    check("ora.offcanvas_option", rc == 0 and "WARN layer_outside_canvas" in o, "--allow-offcanvas turns the off-canvas layer into a WARN (PhotoCraft reads off-canvas offsets)", last(o))


# ----------------------------------------------------------------------------------------------- SVG
@test("svg.rig_rules")
def t_svg_rig():
    import xml.etree.ElementTree as ET
    p = work("svg_rig_check.svg")
    rc, o, e = sh(PY + [tool("svg_rig.py"), "gen", p])
    root = ET.parse(p).getroot()
    os.remove(p)
    ids = [x.get("id") for x in root.iter() if x.get("id")]
    pivots = [x for x in root.iter() if x.get("data-pivot")]
    zs = [x for x in root.iter() if x.get("data-z")]
    bad_attr = [x.tag for x in root.iter() if x.get("class") or x.get("style") or x.tag.endswith("}style") or x.tag.endswith("}animate")]
    idre = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")
    ok = (rc == 0 and len(ids) == len(set(ids)) and all(idre.match(i) for i in ids) and len(pivots) >= 4 and len(zs) >= 4
          and root.get("viewBox") == "0 0 640 360" and not bad_attr and not any(x.get("transform") for x in root.iter() if x.tag.endswith("}g")))
    check("svg.rig_rules", ok, "unique clean ids, data-pivot and data-z present, viewBox 0 0 640 360, no class, style, animation or transform on groups",
          "%d ids, %d data-pivot, %d data-z, viewBox %s" % (len(ids), len(pivots), len(zs), root.get("viewBox")))


@test("svg.roundtrip")
def t_svg_round():
    ink = shutil.which("inkscape")
    if not ink:
        raise Skip("inkscape is not installed")
    rc, o, e = sh(["inkscape", "--version"])
    S["inkscape_version"] = (o.strip().splitlines() or ["?"])[0].replace("Inkscape ", "").split(" ")[0]
    out = work("svg")
    res = work("svg_results.json")
    rc, o, e = sh(["bash", os.path.join(RT, "svg_roundtrip.sh"), "--out", out, "--json", res, "--finding", evid("svg_inkscape_finding.json")], timeout=300)
    npass = len(re.findall(r"^PASS svg\.", o, re.M))
    check("svg.roundtrip_script", rc == 0 and npass == 7 and "FAIL svg." not in o,
          "svg_roundtrip.sh exits 0: clean pass-through 0, three planted defects 1 each, two touch-ups and Inkscape's own format 0",
          "exit %d; %d PASS lines; %s" % (rc, npass, last(o)))
    if not os.path.exists(res):
        raise Skip("no results file")
    rows = {r["label"]: r for r in read_json(res)["results"]}
    r = rows.get("clean_passthrough", {})
    check("svg.clean_passthrough", r.get("raw_exit") == 0 and r.get("gate_exit") == 0 and r.get("authored") == 17,
          "the reused check_ids.py exits 0 on the Inkscape plain-SVG output (17 authored ids)", "raw_exit %s gate_exit %s authored %s" % (r.get("raw_exit"), r.get("gate_exit"), r.get("authored")))
    want = {"planted_ids_stripped": ("ids_lost", 1), "planted_kind_changed": ("element_kind_changed", 0), "planted_pivot_dropped": ("data_attr_changed", 1)}
    for label, (reason, raw) in want.items():
        r = rows.get(label, {})
        check("svg.%s" % label, r.get("gate_exit") == 1 and r.get("reasons") == reason and r.get("raw_exit") == raw,
              "gate exit 1 with reason %s (raw check_ids.py exit %d)" % (reason, raw),
              "gate_exit %s reasons %s raw_exit %s" % (r.get("gate_exit"), r.get("reasons"), r.get("raw_exit")))
    r = rows.get("planted_kind_changed", {})
    check("svg.finding_check_ids_kind_gap", r.get("raw_exit") == 0 and r.get("kind_changed") == "disc-a",
          "FINDING: the reused check_ids.py prints an element kind change but exits 0, so the gate adds the exit itself",
          "raw check_ids.py exit %s, kind_changed %s, gate exit %s" % (r.get("raw_exit"), r.get("kind_changed"), r.get("gate_exit")),
          notes="check_ids.py was not edited; svg_rig.py gate reads its summary line")


@test("svg.inkscape_finding")
def t_svg_finding():
    p = evid("svg_inkscape_finding.json")
    require(p, "the Inkscape finding")
    d = read_json(p)
    pl = d["plain_svg"]
    da, ids = pl["data_attributes"], pl["ids"]
    check("svg.ids_survive", ids["authored"] == 17 and ids["survived"] == 17 and not ids["lost"] and not ids["kind_changed"],
          "all 17 authored ids survive Inkscape's plain-SVG export, with the same element kinds",
          "survived %d of %d; lost %s; kind changed %s" % (ids["survived"], ids["authored"], ids["lost"], ids["kind_changed"]))
    check("svg.finding_data_attributes", da["total"] >= 15 and da["kept_verbatim"] == da["total"] and not da["changed"] and not da["dropped"],
          "FINDING recorded: every data-* attribute (pivot, z, role, note; on g, circle, rect, path, ellipse, use, text, linearGradient and an id-less g) survives verbatim",
          "kept %d of %d verbatim; changed %d; dropped %d; by element kind %s" % (da["kept_verbatim"], da["total"], len(da["changed"]), len(da["dropped"]),
                                                                              {k: "%d/%d" % (v["kept"], v["total"]) for k, v in sorted(da["by_element_kind"].items())}))
    ex = d["extra"]
    moved_group = ex["touch_group_moved"]["transform_added_to"]
    check("svg.finding_other", pl["viewBox"]["in"] == pl["viewBox"]["out"] and pl["inkscape_or_sodipodi_attributes"] == 0 and ids["added_by_tool"] > 0
          and ex["touch_child_moved"]["transform_added_to"] == [] and moved_group == ["orbit"],
          "FINDING recorded: viewBox unchanged, no inkscape:/sodipodi: attributes in plain output, Inkscape adds its own ids to id-less elements, moving a group adds a transform to it (a child's coordinates are rewritten instead)",
          "viewBox %s -> %s; %d tool-made ids (e.g. %s); inkscape/sodipodi attributes %d; plain output namespaces %s; group move adds transform to %s; Inkscape-format output has %d inkscape/sodipodi attributes" % (
              pl["viewBox"]["in"], pl["viewBox"]["out"], ids["added_by_tool"], ", ".join(ids["added_examples"][:3]), pl["inkscape_or_sodipodi_attributes"],
              [n.rsplit("/", 1)[-1] for n in pl["namespaces_in_output"]], moved_group, ex["inkscape_svg_format"]["inkscape_or_sodipodi_attributes"]))


@test("svg.gate_usage")
def t_svg_usage():
    rc1, o1, e1 = sh(PY + [tool("svg_rig.py"), "gate", work("nope.svg"), work("nope2.svg")])
    rc2, o2, e2 = sh(PY + [tool("svg_rig.py"), "plant", "bogus", "a", "b"])
    rc3, o3, e3 = sh(PY + [tool("svg_rig.py")])
    rc4, o4, e4 = sh(["bash", os.path.join(RT, "svg_roundtrip.sh"), "--bogus"])
    rc5, o5, e5 = sh(["bash", os.path.join(RT, "svg_roundtrip.sh"), "--inkscape", "no-such-inkscape-command", "--out", work("svg_none")])
    shutil.rmtree(work("svg_none"), ignore_errors=True)
    check("svg.gate_usage", rc1 == 3 or rc1 == 2, "gate on missing files does not report a pass", "gate exit %d" % rc1)
    check("svg.usage_exits", (rc2, rc3, rc4, rc5) == (2, 2, 2, 3), "a bogus defect, no command and a bogus option exit 2; a missing Inkscape exits 3", "exits %s %s %s %s" % (rc2, rc3, rc4, rc5))


# ----------------------------------------------------------------------------------------------- OTIO
@test("otio.venv")
def t_otio_venv():
    if not os.path.exists(VENV_PY):
        raise Skip("the opentimelineio venv does not exist (<scratch>/venv-otio); create it as in the README")
    rc, o, e = sh([VENV_PY, "-I", "-c", "import opentimelineio as o; print(o.__version__)"])
    S["otio_version"] = o.strip()
    mb = tree_mb(os.path.dirname(os.path.dirname(VENV_PY)))
    check("otio.venv", rc == 0 and o.strip() == "0.18.1" and mb < 60, "the venv holds opentimelineio 0.18.1 and is under the 60 MB planned for it",
          "opentimelineio %s, venv %.0f MB" % (o.strip(), mb))


@test("otio.emit_validate")
def t_otio_emit():
    out = work("ch.otio")
    shutil.rmtree(work("media"), ignore_errors=True)
    rc, o, e = sh(PY + [tool("emit_otio.py"), os.path.join(RT, "spec", "neutral_timeline.example.json"), out, "--timeline169", work("timeline169.json")])
    check("otio.emit", rc == 0 and os.path.isfile(out) and "4 clips, 3 dissolves, 3 markers, 1 audio cue(s), 480 frames at 24 fps" in o and "generated 5 test media" in o,
          "emit_otio.py exits 0: 4 clips, 3 dissolves, 3 markers, 1 audio cue, 480 frames at 24 fps, test media generated", last(o) or last(e))
    S["otio"] = out
    args = [tool("validate_otio.py"), out, "--json", evid("otio_validate_json_level.json")]
    rc, o, e = sh(PY + args)
    d = read_json(evid("otio_validate_json_level.json"))
    check("otio.validate_json_level", rc == 0 and d["counts"]["FAIL"] == 0 and d["counts"]["WARN"] == 0 and d["counts"]["PASS"] >= 20,
          "validate_otio.py exits 0 on the JSON-level rules (at least 20 checks, no WARN)", "exit %d; %s" % (rc, last(o)))
    if os.path.exists(VENV_PY):
        rc, o, e = sh(PY + [tool("validate_otio.py"), out, "--with-otio", VENV_PY, "--json", evid("otio_validate_with_otio.json")])
        d = read_json(evid("otio_validate_with_otio.json"))
        codes = [c["code"] for c in d["checks"]]
        check("otio.validate_with_otio", rc == 0 and "otio_loads" in codes and "otio_filmcraft_preserved" in codes and d["counts"]["FAIL"] == 0,
              "validate_otio.py --with-otio exits 0: opentimelineio 0.18.1 loads the file, counts and duration agree, metadata.filmcraft survives a write and read",
              "exit %d; %s" % (rc, last(o)))
    else:
        record("otio.validate_with_otio", "SKIPPED", "the load with opentimelineio", "venv missing")


@test("otio.determinism")
def t_otio_det():
    require(work("ch.otio"), "ch.otio")
    import hashlib
    other = work("ch_again.otio")
    sh(PY + [tool("emit_otio.py"), os.path.join(RT, "spec", "neutral_timeline.example.json"), other])
    h = [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (work("ch.otio"), other)]
    os.remove(other)
    check("otio.determinism", h[0] == h[1], "two emits give the same bytes", "sha256 %s" % h[0][:16])


@test("otio.content")
def t_otio_content():
    require(work("ch.otio"), "ch.otio")
    d = read_json(work("ch.otio"))
    v1 = d["tracks"]["children"][0]["children"]
    clips = [x for x in v1 if x["OTIO_SCHEMA"].startswith("Clip")]
    trans = [x for x in v1 if x["OTIO_SCHEMA"].startswith("Transition")]
    urls = [c["media_references"]["DEFAULT_MEDIA"]["target_url"] for c in clips]
    m0 = clips[0]["metadata"]["filmcraft"]["effects"][0]["params"]
    sc = [k["value"]["Float"] for k in m0["scale"]["keyframes"]]
    ps = [(k["value"]["Vec2"]["x"], k["value"]["Vec2"]["y"]) for k in m0["position"]["keyframes"]]
    s3 = clips[2]["metadata"]["filmcraft"]["effects"][0]["params"]["scale"]["keyframes"]
    ok = (len(clips) == 4 and len(trans) == 3 and all(t["in_offset"]["value"] + t["out_offset"]["value"] == 24 for t in trans)
          and all(u.startswith("media/") and not u.startswith("/") and "://" not in u for u in urls)
          and sc == [66.67, 80.0] and ps == [(960.0, 540.0), (930.0, 520.0)] and s3[0]["value"]["Float"] == 80.0 and s3[1]["value"]["Float"] == 66.67
          and d["global_start_time"]["rate"] == 24.0)
    check("otio.content", ok, "four clips and three 24-frame dissolves (12 + 12), relative media/ URLs, shot 1 scale 66.67 -> 80.0 and position (960,540) -> (930,520), shot 3 zooms out",
          "clips %d; dissolves %d; urls %s; shot 1 scale %s position %s; shot 3 scale %s -> %s" % (
              len(clips), len(trans), urls[0], sc, ps, s3[0]["value"]["Float"], s3[1]["value"]["Float"]))


def _diff(a, b, path, ignore, out):
    if ignore(path):
        return
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                if not ignore(path + "." + k):
                    out.append("extra in emitted: %s.%s" % (path, k))
            elif k not in b:
                if not ignore(path + "." + k):
                    out.append("missing in emitted: %s.%s" % (path, k))
            else:
                _diff(a[k], b[k], path + "." + k, ignore, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append("length differs at %s: %d vs %d" % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            _diff(x, y, "%s[%d]" % (path, i), ignore, out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        if abs(a - b) > 1e-9:
            out.append("%s: %r vs %r" % (path, a, b))
    elif a != b:
        out.append("%s: %r vs %r" % (path, a, b))


def _rebase(node, in_clip_range=False):
    """Rebase the E2 template from its old rate to 24: every rate becomes 24, clip source_range values keep their SECONDS (125 frames -> 120, 250 -> 240),
    dissolve offsets and marker times keep their frame counts (the template's dissolve is a 24-frame dissolve, 12 + 12)."""
    if isinstance(node, dict):
        if node.get("OTIO_SCHEMA", "").startswith("RationalTime"):
            v = node["value"] * 24.0 / 25.0 if in_clip_range else node["value"]
            return {"OTIO_SCHEMA": node["OTIO_SCHEMA"], "rate": 24.0, "value": v}
        return {k: _rebase(v, in_clip_range or (k == "source_range" and node.get("OTIO_SCHEMA", "").startswith("Clip"))) for k, v in node.items()}
    if isinstance(node, list):
        return [_rebase(x, in_clip_range) for x in node]
    return node


@test("otio.template_parity")
def t_otio_template():
    import emit_otio
    md = open(os.path.join(ROOT, "research", "craft-motion.md"), encoding="utf-8").read()
    i = md.index("**E2 template")
    block = md[md.index("```json", i) + 7: md.index("```", md.index("```json", i) + 7)]
    tpl = json.loads(block)
    old_rates = {r["rate"] for p, r in __import__("validate_otio").walk_rationals(tpl)}
    spec = {"schema": "lj-neutral-timeline/1", "name": "Chapter 01 draft", "fps": 24, "sequence": {"width": 1920, "height": 1080},
            "markers": [{"name": "Chapter 01", "at_frame": 0, "color": "GREEN", "comment": ""}],
            "shots": [{"id": "ch01_s01", "source": "media/ch01_s01.png", "source_size": [2880, 1620], "duration_frames": 120,
                       "motion": {"scale": {"from": "cover", "zoom": 1.2}, "position": [[960, 540], [930, 520]], "ease": "EaseOut"},
                       "transition_out": {"type": "dissolve", "frames": 24}},
                      {"id": "ch01_s02", "source": "media/ch01_s02.png", "duration_frames": 120}],
            "audio": [{"id": "music_bed", "source": "media/mix_ch01.wav", "start_frame": 0, "duration_frames": 240, "gain_db": 0.0}]}
    emitted, info = emit_otio.build(spec, work("template_parity_nowhere"), None)

    def ignore(p):
        return (p in ("$.name", "$.metadata") or p.endswith(".available_range") or (".children[1].children[0].metadata" in p and p.endswith(".metadata")))
    diffs = []
    _diff(_rebase(tpl), emitted, "$", ignore, diffs)
    check("otio.template_parity", not diffs and old_rates == {25.0},
          "the emitted file equals the R3 E2 template rebased to 24 fps (schemas, rates, 120- and 240-frame ranges, 12 + 12 dissolve, marker, Ken Burns keyframes and ticks), ignoring only the timeline name and metadata, available_range and the audio clip's metadata",
          "template rates %s; %d difference(s)%s" % (sorted(old_rates), len(diffs), (": " + "; ".join(diffs[:3])) if diffs else ""))


@test("otio.planted_defects")
def t_otio_plant():
    require(work("ch.otio"), "ch.otio")
    table = {}
    for kind, (code, why, extras) in plant.OTIO_DEFECTS.items():
        dst = work("plant_otio_%s.otio" % kind)
        plant.plant_otio(kind, work("ch.otio"), dst)
        rc, o, e = sh(PY + [tool("validate_otio.py"), dst])
        got = failed_codes(o)
        ok = rc == 1 and code in got and got <= ({code} | set(extras))
        table[kind] = {"expected_code": code, "exit": rc, "failed_codes": sorted(got), "described_as": why, "allowed_companions": list(extras)}
        check("otio.plant.%s" % kind, ok, "exit 1 naming %s (%s)%s" % (code, why, (", may also name " + ", ".join(extras)) if extras else ""),
              "exit %d; FAILED %s" % (rc, sorted(got) or "nothing"))
        os.remove(dst)
    with open(evid("planted_defects_otio.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(table, f, indent=2, sort_keys=True)
        f.write("\n")


@test("otio.options")
def t_otio_opts():
    require(work("ch.otio"), "ch.otio")
    # --no-media-check: a file whose media is absent passes with a WARN
    dst = work("plant_otio_nomedia.otio")
    plant.plant_otio("media_missing", work("ch.otio"), dst)
    rc, o, e = sh(PY + [tool("validate_otio.py"), dst, "--no-media-check"])
    os.remove(dst)
    check("otio.no_media_check", rc == 0 and "WARN media_exists_skipped" in o, "--no-media-check passes a file with a missing media path and says the check was skipped", last(o))
    # --lenient-filmcraft: unknown keys become WARN
    dst = work("plant_otio_lenient.otio")
    plant.plant_otio("filmcraft_key_unknown", work("ch.otio"), dst)
    rc, o, e = sh(PY + [tool("validate_otio.py"), dst, "--lenient-filmcraft"])
    os.remove(dst)
    check("otio.lenient_filmcraft", rc == 0 and "WARN filmcraft_key_unknown" in o, "--lenient-filmcraft turns an unknown filmcraft key into a WARN", last(o))
    # exits
    rc1, o1, e1 = sh(PY + [tool("validate_otio.py"), work("no_such.otio")])
    rc2, o2, e2 = sh(PY + [tool("validate_otio.py"), work("ch.otio"), "--with-otio", work("no_such_python")])
    rc3, o3, e3 = sh(PY + [tool("validate_otio.py"), work("ch.otio"), "--with-otio", sys.executable])
    check("otio.exit_codes", (rc1, rc2, rc3) == (2, 3, 3), "a missing file exits 2; an explicit missing interpreter and one without opentimelineio exit 3",
          "exits %s %s %s" % (rc1, rc2, rc3))
    rc4, o4, e4 = sh(PY + [tool("validate_otio.py"), work("ch.otio"), "--with-otio"], env={"LJ_SCRATCH": work("no_scratch_here")})
    check("otio.with_otio_auto_skips", rc4 == 0 and "WARN otio_load_skipped" in o4, "--with-otio without a value skips with a WARN when there is no venv", last(o4))
    # BOM tolerance
    dst = work("bom.otio")
    open(dst, "wb").write(b"\xef\xbb\xbf" + open(work("ch.otio"), "rb").read())
    rc, o, e = sh(PY + [tool("validate_otio.py"), dst])
    os.remove(dst)
    check("otio.accepts_utf8_bom", rc == 0, "a UTF-8 BOM (Windows PowerShell 5.1 Set-Content) does not break the validator", last(o))


@test("otio.weird_shapes")
def t_otio_weird():
    ts = {"OTIO_SCHEMA": "RationalTime.1", "rate": 24.0, "value": 0}
    shapes = {"list_root": [],
              "string_rate": {"OTIO_SCHEMA": "Timeline.1", "name": "x", "global_start_time": dict(ts, rate="24"), "metadata": [],
                              "tracks": {"OTIO_SCHEMA": "Stack.1", "children": [{"OTIO_SCHEMA": "Track.1", "kind": "Video", "children": [
                                  {"OTIO_SCHEMA": "Clip.2", "name": "a", "metadata": [], "markers": None, "media_references": {}}]}]}},
              "metadata_list_with_filmcraft": {"OTIO_SCHEMA": "Timeline.1", "name": "x", "global_start_time": ts, "metadata": {},
                                               "tracks": {"OTIO_SCHEMA": "Stack.1", "children": [{"OTIO_SCHEMA": "Track.1", "kind": "Video", "children": [
                                                   {"OTIO_SCHEMA": "Clip.2", "name": "a", "metadata": {"filmcraft": [1, 2]}, "markers": [], "media_references": {}}]}]}}}
    rows = []
    for name, d in shapes.items():
        p = work("weird_%s.otio" % name)
        json.dump(d, open(p, "w"))
        rc, o, e = sh(PY + [tool("validate_otio.py"), p, "--no-media-check"])
        rows.append((name, rc, "Traceback" in e or "Traceback" in o, last(o)))
        os.remove(p)
    check("otio.weird_shapes", all(rc == 1 and not tb for _, rc, tb, _ in rows), "oddly shaped JSON (a list root, a string rate, filmcraft as a list) exits 1 with a named reason and no traceback",
          "; ".join("%s -> exit %d%s" % (n, rc, " TRACEBACK" if tb else "") for n, rc, tb, _ in rows))
    p = work("not_a_zip.ora")
    open(p, "wb").write(os.urandom(2048))
    rc, o, e = sh(PY + [tool("validate_ora.py"), p])
    os.remove(p)
    check("ora.random_bytes", rc == 1 and failed_codes(o) == {"zip_unreadable"} and "Traceback" not in e, "a file of random bytes exits 1 naming zip_unreadable, no traceback", "exit %d; %s" % (rc, last(o)))


@test("otio.emit_refusals")
def t_otio_refuse():
    base = read_json(os.path.join(RT, "spec", "neutral_timeline.example.json"))
    cases = []

    def mk(name, fn):
        d = json.loads(json.dumps(base))
        fn(d)
        p = work("spec_%s.json" % name)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f)
        cases.append((name, p))
    old = str(24 + 1)
    mk("old_rate", lambda d: d.__setitem__("fps", int(old)))
    mk("abs_source", lambda d: d["shots"][0].__setitem__("source", "/media/ch01_s01.png"))
    mk("backslash_source", lambda d: d["shots"][0].__setitem__("source", "media\\ch01_s01.png"))
    mk("dup_id", lambda d: d["shots"][1].__setitem__("id", "ch01_s01"))
    mk("last_dissolve", lambda d: d["shots"][3].__setitem__("transition_out", {"type": "dissolve", "frames": 24}))
    mk("black_edge", lambda d: d["shots"][0]["motion"].__setitem__("position", [[760, 540], [930, 520]]))
    mk("bad_colour", lambda d: d["markers"][0].__setitem__("color", "MAUVE"))
    mk("size_4k", lambda d: d.__setitem__("sequence", {"width": 3840, "height": 2160}))
    mk("bad_ease", lambda d: d["shots"][0]["motion"].__setitem__("ease", "Bounce"))
    mk("too_long", lambda d: d["shots"][0].__setitem__("duration_frames", 500))
    rows = []
    for name, p in cases:
        rc, o, e = sh(PY + [tool("emit_otio.py"), p, work("refused.otio")])
        rows.append((name, rc, e.strip()[:90]))
        os.remove(p)
    check("otio.emit_refusals", all(rc == 2 for _, rc, _ in rows) and not os.path.exists(work("refused.otio")),
          "emit_otio.py refuses (exit 2, no file) an old frame rate, an absolute or backslash source, a repeated id, a dissolve on the last shot, a move that shows black, a bad marker colour, a 4K sequence, an unknown ease and a clip longer than its media",
          "; ".join("%s -> %d" % (n, rc) for n, rc, _ in rows), notes=" | ".join("%s: %s" % (n, m) for n, rc, m in rows[:3]))
    rc, o, e = sh(PY + [tool("emit_otio.py")])
    check("otio.emit_usage", rc == 2, "no arguments exits 2", "exit %d" % rc)
    rc, o, e = sh(PY + [tool("emit_otio.py"), os.path.join(RT, "spec", "neutral_timeline.example.json")])
    check("otio.emit_needs_output", rc == 2, "a spec without an output and without --timeline169 exits 2", "exit %d" % rc)


@test("otio.never_creates_real_media")
def t_otio_nocreate():
    base = read_json(os.path.join(RT, "spec", "neutral_timeline.example.json"))
    base["synthetic_media"] = False
    os.makedirs(work("nomedia"), exist_ok=True)
    p = work("nomedia", "spec_real.json")
    json.dump(base, open(p, "w"))
    rc, o, e = sh(PY + [tool("emit_otio.py"), p, work("nomedia", "x.otio")])
    made = os.path.exists(work("nomedia", "media"))
    shutil.rmtree(work("nomedia"), ignore_errors=True)
    check("otio.never_creates_media_without_the_flag", rc == 0 and not made, "a spec without synthetic_media: true creates no media file",
          "exit %d; media folder created: %s" % (rc, made))


@test("otio.adapter_probe")
def t_otio_probe():
    if not os.path.exists(VENV_PY):
        raise Skip("the opentimelineio venv does not exist")
    rc, o, e = sh(["bash", os.path.join(RT, "adapter_probe.sh"), "--json", evid("adapter_probe.json")], timeout=300)
    if not os.path.exists(evid("adapter_probe.json")):
        check("otio.adapter_probe", False, "adapter_probe.sh exits 0 and writes its JSON", "exit %d; %s" % (rc, last(e)))
        return
    d = read_json(evid("adapter_probe.json"))
    core = d["core_only"]
    check("otio.adapter_probe", rc == 0 and core["plain_otio_written"] and len(core["read_back_clips"]) == 5 and d["make_otio_unchanged_in_git"] is True
          and d["timeline169"]["fps"] == 24 and set(core["adapters"]) == {"cmx_3600", "fcpx_xml", "kdenlive", "mlt_xml"},
          "adapter_probe.sh exits 0: the reused make_otio.py (unchanged) ran against a 24 fps timeline169.json, wrote out.otio and read it back; the four adapters are each reported",
          "exit %d; working with the core install alone: %s; %s" % (rc, core["working"] or "none", d["finding"]))
    rc1, o1, e1 = sh(["bash", os.path.join(RT, "adapter_probe.sh"), "--bogus"])
    rc2, o2, e2 = sh(["bash", os.path.join(RT, "adapter_probe.sh"), "--python", work("no_such_python")])
    check("otio.adapter_probe_exit_codes", (rc1, rc2) == (2, 3), "a bogus option exits 2; an interpreter that does not exist exits 3", "exits %d %d" % (rc1, rc2))
    check("otio.adapter_probe_no_paths", not re.search(r"/home/|/tmp/|build-scratch", json.dumps(d)), "the probe JSON carries no folder names", "clean")


@test("otio.adapter_probe_plugins", modes=("all",))
def t_otio_probe_plugins():
    if not os.path.exists(VENV_PY):
        raise Skip("the opentimelineio venv does not exist")
    rc, o, e = sh(["bash", os.path.join(RT, "adapter_probe.sh"), "--with-plugins", "--json", evid("adapter_probe_with_plugins.json")], timeout=600)
    if rc == 3:
        raise Skip("the plug-in venv could not be built (no network or pip failed): %s" % last(e))
    d = read_json(evid("adapter_probe_with_plugins.json"))
    w = d["with_plugins"]
    rates = {k: v.get("frame_rate_found_in_output") for k, v in w["adapters"].items()}
    ok = (rc == 0 and sorted(w["working"]) == ["cmx_3600", "fcpx_xml", "kdenlive", "mlt_xml"] and w["opentimelineio"] == "0.18.1"
          and rates["cmx_3600"] == "last timecode 00:00:20:00" and rates["fcpx_xml"] == "25/600s" and rates["kdenlive"] == "24" and rates["mlt_xml"] == "24")
    check("otio.adapter_probe_plugins", ok, "with the four plug-in packages installed all four adapters write a file, and each shows 24 fps (EDL ends at 00:00:20:00 for 480 frames; FCPXML frameDuration 25/600 s = 1/24 s)",
          "exit %d; working %s; rate hints %s" % (rc, w["working"], rates))


# ----------------------------------------------------------------------------------------------- unverified
@test("windows.validators")
def t_win():
    record("windows.validators", "UNVERIFIED", "validate_ora.py, validate_otio.py and kb_scale.py run under py -3 -I on Windows PowerShell 5.1 and 7",
           "standard library only, os.path joins, UTF-8 and BOM reading, ASCII output, no shell=True; not run on Windows",
           unverified="no Windows host here; the maker or WP-09's runner verifies")
    record("craft_apps.accept_files", "UNVERIFIED", "PhotoCraft opens and keeps the ORA layer names; VectorCraft keeps the rig ids and data-*; FilmCraft imports the OTIO and shows the motion keyframes",
           "not run: no Craft app was started in this package", unverified="WP-10 on the Linux CLIs, and the maker's Windows five-minute tests, are the real evidence")


# ----------------------------------------------------------------------------------------------- main
def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "all"], default="quick")
    ap.add_argument("--work", default=os.path.join(ROOT, "renders", "wp06"))
    ap.add_argument("--evidence", default=os.path.join(ROOT, "build", "evidence", "wp06"))
    ap.add_argument("--keep", action="store_true", help="leave the generated files in --work")
    ARGS = ap.parse_args()
    ARGS.work, ARGS.evidence = os.path.abspath(ARGS.work), os.path.abspath(ARGS.evidence)
    ARGS.jsonl = os.path.join(ARGS.evidence, "tests_%s.jsonl" % ARGS.mode)       # one file per mode: a later --quick run never overwrites the --all evidence
    ARGS.t_start = avail_mb()
    S["pycache_start"] = pycache_snapshot()
    os.makedirs(ARGS.evidence, exist_ok=True)
    shutil.rmtree(ARGS.work, ignore_errors=True)
    os.makedirs(ARGS.work, exist_ok=True)
    open(ARGS.jsonl, "w").close()
    t0 = time.time()
    for name, modes, fn in REG:
        if ARGS.mode not in modes:
            continue
        try:
            fn()
        except Skip as e:
            record(name, "SKIPPED", "the test runs", str(e))
        except Exception as e:      # noqa: BLE001 - a crashing test is a failing test
            record(name, "FAIL", "the test runs to the end", "%s: %s" % (type(e).__name__, str(e)[:200]))
    n = STATE["counts"]
    print("TOTAL: PASS %d, FAIL %d, UNVERIFIED %d, SKIPPED %d, BLOCKED %d (%d s)" % (n["PASS"], n["FAIL"], n["UNVERIFIED"], n["SKIPPED"], n["BLOCKED"], time.time() - t0))
    counts_path = os.environ.get("LJ_WP06_COUNTS")              # only make_evidence.sh asks for this; a normal run leaves no extra file in the evidence folder
    if counts_path:
        with open(counts_path, "w") as f:
            json.dump({"peak_work_mb": round(STATE["peak_work_mb"], 1), "min_avail": STATE["min_avail"], "counts": n}, f)
    if not ARGS.keep:
        shutil.rmtree(ARGS.work, ignore_errors=True)
    return 3 if n["BLOCKED"] else (1 if n["FAIL"] else 0)


if __name__ == "__main__":
    sys.exit(main())
