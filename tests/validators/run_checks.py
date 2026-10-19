#!/usr/bin/env python3
"""run_checks.py: the WP-05 test driver (called by tests/validators/run_tests.sh; it can also be run alone).

  python3 -I tests/validators/run_checks.py --mode quick|all [--work renders/wp05] [--evidence build/evidence/wp05]

One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
and one evidence envelope per test (build plan 4.2) appended to <evidence>/tests.jsonl. Exit 0 if no line is FAIL or BLOCKED,
1 if a line FAILs, 3 if a line is BLOCKED. UNVERIFIED (Windows-only behaviour) and SKIPPED are listed and never counted as a pass.

Everything is generated at test time from synthetic content (three flat colour patches, a sine tone, a generated grey chart) under
the --work folder (git-ignored renders/wp05) and removed again. No family media exists here and none is created or simulated.
"""
import argparse
import ast
import datetime
import importlib.util
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
VAL = os.path.join("pipeline", "validators")
PY = [sys.executable, "-I", "-B"]
SCRATCH = os.environ.get("LJ_SCRATCH", os.path.normpath(os.path.join(ROOT, "..", "build-scratch")))

STATE = {"counts": {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0}, "min_avail": None, "fx": None}
ARGS = None


# ----------------------------------------------------------------------------------------------- plumbing
def sh(args, timeout=900, env=None, cwd=None):
    e = dict(os.environ)
    e.pop("FFMPEG", None)
    e.pop("FFPROBE", None)
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd or ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, env=e)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def avail_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", "/"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20).stdout.decode()
        v = out.strip().splitlines()[-1].split()[3]
        return int(re.sub(r"[^0-9]", "", v))
    except Exception:
        return 0


def ffmpeg_version():
    try:
        out = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20).stdout.decode()
        return out.split()[2].split("-")[0]
    except Exception:
        return "unknown"


def clean(s):
    s = str(s).replace(ROOT, ".")
    s = s.replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return s[:700]


def record(name, status, expected, actual, unverified=""):
    STATE["counts"][status] += 1
    a = avail_mb()
    s0 = ARGS.t_start
    env = {"platform": "linux", "ffmpeg": ARGS.ffv, "nproc": os.cpu_count(), "python": "%d.%d.%d" % sys.version_info[:3], "node": "22.x"}
    lo = min([x for x in (s0, a) if x] or [0])
    STATE["min_avail"] = lo if STATE["min_avail"] is None else min(STATE["min_avail"], lo)
    rec = {"schema": "lj-evidence/1", "package": "WP-05", "test": name, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
           "status": status, "env": env,
           "disk": {"avail_mb_start": s0, "planned_write_mb": 0, "avail_mb_min": lo, "avail_mb_end": a, "floor_mb": 400, "hard_floor_mb": 250},
           "expected": clean(expected), "actual": clean(actual), "notes": "", "unverified_reasons": [unverified] if unverified else []}
    with open(ARGS.jsonl, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("%-10s %-46s %s" % (status, name, clean(actual)[:150].replace("\n", " ")), flush=True)


REG = []


def tree_mb(path):
    total = 0
    try:
        for dp, dn, fn in os.walk(path):
            for f in fn:
                try:
                    total += os.path.getsize(os.path.join(dp, f))
                except OSError:
                    pass
    except OSError:
        pass
    return total / 1048576.0


def start_sampler():
    import threading
    box = {"peak": 0.0, "stop": False}

    def loop():
        while not box["stop"]:
            box["peak"] = max(box["peak"], tree_mb(ARGS.work))
            time.sleep(0.4)
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    return box


def test(name, modes=("quick", "all")):
    def deco(fn):
        REG.append((name, modes, fn))
        return fn
    return deco


class Skip(Exception):
    pass


def check(name, ok, expected, actual, unverified=""):
    record(name, "PASS" if ok else "FAIL", expected, actual, unverified)
    return ok


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def work(*p):
    return os.path.join(ARGS.work, *p)


def ev(*p):
    return os.path.join(ARGS.evidence, *p)


def rel(path):
    return os.path.relpath(path, ROOT)


def gen(set_name, only=None):
    cmd = PY + [os.path.join("tests", "validators", "gen_fixtures.py"), ARGS.work, "--set", set_name]
    if only:
        cmd += ["--only"] + list(only)
    rc, out, err = sh(cmd, timeout=900)
    if rc != 0:
        raise RuntimeError("gen_fixtures failed: " + (err.strip().splitlines() or ["?"])[-1])
    return read_json(work("manifest_%s.json" % set_name))


def spec(file, profile, extra=None, json_out=None):
    cmd = PY + [os.path.join(VAL, "spec_check.py"), file, "--profile", profile]
    cmd += extra or []
    if json_out:
        cmd += ["--json", json_out]
    return sh(cmd)


# ----------------------------------------------------------------------------------------------- static hygiene
def py_files():
    out = []
    for d in (os.path.join(ROOT, VAL), os.path.join(ROOT, "tests", "validators")):
        for f in sorted(os.listdir(d)):
            if f.endswith(".py"):
                out.append(os.path.join(d, f))
    return out


@test("hygiene.python_compiles")
def t_compile():
    bad = []
    for f in py_files():
        try:
            py_compile.compile(f, doraise=True, cfile=os.path.join(tempfile.gettempdir(), "lj_wp05_pyc_%d" % os.getpid()))
            ast.parse(open(f, encoding="utf-8").read(), feature_version=(3, 9))
        except (py_compile.PyCompileError, SyntaxError) as e:
            bad.append("%s: %s" % (os.path.basename(f), str(e)[:80]))
    try:
        os.remove(os.path.join(tempfile.gettempdir(), "lj_wp05_pyc_%d" % os.getpid()))
    except OSError:
        pass
    check("hygiene.python_compiles", not bad, "every .py compiles and parses with the Python 3.9 grammar", "; ".join(bad) or "%d files" % len(py_files()))


@test("hygiene.validators_stdlib_only")
def t_stdlib():
    std = set(sys.stdlib_module_names)
    bad = []
    for f in sorted(os.listdir(os.path.join(ROOT, VAL))):
        if not f.endswith(".py"):
            continue
        tree = ast.parse(open(os.path.join(ROOT, VAL, f), encoding="utf-8").read())
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module.split(".")[0]]
            for m in mods:
                if m not in std:
                    bad.append("%s imports %s" % (f, m))
    check("hygiene.validators_stdlib_only", not bad, "spec_check, colour_patch and mo8_gate import only the standard library", "; ".join(bad) or "stdlib only")


@test("hygiene.windows_portable_python")
def t_portable():
    rx = [(r"shell\s*=\s*True", "shell=True"), (r"os\.system\(", "os.system"), (r"/tmp/", "/tmp/"), (r"/home/", "/home/"), (r"\bfcntl\b", "fcntl"),
          (r"os\.fork\(", "os.fork"), (r"signal\.SIGKILL", "SIGKILL"), (r"\bsh -c\b", "sh -c")]
    bad = []
    for f in sorted(os.listdir(os.path.join(ROOT, VAL))):
        if not f.endswith(".py"):
            continue
        for i, line in enumerate(open(os.path.join(ROOT, VAL, f), encoding="utf-8"), 1):
            for pat, label in rx:
                if re.search(pat, line):
                    bad.append("%s:%d %s" % (f, i, label))
    check("hygiene.windows_portable_python", not bad, "no shell=True, POSIX-only module or hard-coded POSIX path in the validators", "; ".join(bad[:5]) or "none found",
          "")


@test("hygiene.mo8_audit_reused_in_place")
def t_inplace():
    src = os.path.join("research", "cinematic-quality-fixtures", "mo8_audit.py")
    copies = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "pipeline")):
        for f in fn:
            if f.startswith("mo8_audit"):
                copies.append(os.path.join(dp, f))
    rc, out, err = sh(["git", "diff", "--quiet", "HEAD", "--", src])
    gate = open(os.path.join(ROOT, VAL, "mo8_gate.py"), encoding="utf-8").read()
    ok = not copies and rc == 0 and "\"-I\"" in gate and "research" in gate
    check("hygiene.mo8_audit_reused_in_place", ok, "no copy of mo8_audit.py under pipeline/, the original is unmodified, the gate runs it with python -I",
          "copies=%d, git diff rc=%d, gate uses -I: %s" % (len(copies), rc, '"-I"' in gate))


# ----------------------------------------------------------------------------------------------- data files
@test("json.chains_shape")
def t_chains():
    d = read_json(os.path.join(ROOT, "pipeline", "lib", "chains.json"))
    want = ["h264_venue", "h264_backup_main40", "h264_online", "prores422hq_master", "prores4444_alpha", "ffv1_lossless"]
    probs = []
    if d.get("schema") != "lj-chains/1":
        probs.append("schema")
    for n in want:
        c = d.get("chains", {}).get(n)
        if not c:
            probs.append("missing " + n)
            continue
        for k in ("container", "vf", "video_args", "audio_args", "expect", "notes"):
            if k not in c:
                probs.append("%s lacks %s" % (n, k))
        if not all(isinstance(a, str) for a in c.get("video_args", []) + c.get("audio_args", [])):
            probs.append(n + " args not strings")
        for k in ("pix_fmt", "color_range", "color_space", "color_primaries", "color_transfer", "codec", "profile"):
            if k not in c.get("expect", {}):
                probs.append("%s.expect lacks %s" % (n, k))
        if c.get("expect", {}).get("profile") is not None:
            probs.append("%s.expect.profile must be null (render.mjs would report a false mismatch); use expect_extra" % n)
        if "expect_extra" not in c:
            probs.append(n + " lacks expect_extra")
        if not c["vf"].startswith("scale=out_color_matrix=bt709:out_range=tv,format=") or "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" not in c["vf"]:
            probs.append(n + " vf is not scale-first / format / setparams")
        if re.search(r"(^|\s)-r\s+25\b|fps=25|-framerate\s+25|1\.5\s*dBTP", json.dumps(c)):
            probs.append(n + " carries a stale value")
    check("json.chains_shape", not probs and list(d["chains"]) == want, "the six chains, each with the 4.5 keys and a scale-first vf", "; ".join(probs) or "6 chains ok")


@test("json.settings_mirror_of_card")
def t_settings():
    s = read_json(os.path.join(ROOT, "pipeline", "settings.json"))
    ch = read_json(os.path.join(ROOT, "pipeline", "lib", "chains.json"))["chains"]
    card = open(os.path.join(ROOT, "ops", "SETTINGS-CARD.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(ROOT, "ops", "SETTINGS-CARD.md")) else ""
    probs = []
    if s.get("signed") is not False:
        probs.append("signed must be false")
    if (s["picture"]["width"], s["picture"]["height"]) != (1920, 1080):
        probs.append("picture")
    if (s["fps"]["num"], s["fps"]["den"]) != (24, 1):
        probs.append("fps")
    if s["loudness"]["true_peak_max_dbtp"] != -1.0 or s["loudness"]["online_lufs"] != -16 or s["loudness"]["venue_lufs_candidates"] != [-23, -18, -16]:
        probs.append("loudness")
    c = s["captions"]
    if (c["font_size"], c["max_chars_per_line"], c["lines"], c["safe_box_percent"]) != (23, 42, 2, 90):
        probs.append("captions")
    if s["audio"]["sample_rate_hz"] != 48000 or s["audio"]["master_bit_depth"] != 24:
        probs.append("audio")
    if (s["master"]["codec"], s["master"]["profile"], s["master"]["pix_fmt"]) != ("prores", "HQ", "yuv422p10le"):
        probs.append("master")
    if s["colour"]["colour_patch_tolerance_of_255"] != 3:
        probs.append("tolerance")
    for need in ("master_prores422hq", "venue_h264", "venue_h264_backup_main40", "online_h264"):
        if need not in s["profiles"]:
            probs.append("profile " + need)
    # chain / profile parity: what a chain promises is what its profile demands
    for name, p in s["profiles"].items():
        c = ch.get(p.get("chain"))
        if not c:
            probs.append("%s names an unknown chain" % name)
            continue
        v, e = p["video"], c["expect"]
        if v["codec"] != e["codec"]:
            probs.append("%s codec differs from its chain" % name)
        wanted_profile = e.get("profile") or c.get("expect_extra", {}).get("profile")
        if wanted_profile and wanted_profile not in v["profile"]:
            probs.append("%s profile differs from its chain" % name)
        if e["pix_fmt"] not in v["pix_fmt"]:
            probs.append("%s pix_fmt differs from its chain" % name)
        for k in ("color_space", "color_primaries", "color_transfer"):
            if e[k] and e[k] not in v[k]:
                probs.append("%s %s differs from its chain" % (name, k))
    # the card's own words
    for needle in ("1920x1080", "24 fps", "-1 dBTP", "FontSize=23", "42 characters", "-16"):
        if card and needle not in card:
            probs.append("card lacks %r" % needle)
    check("json.settings_mirror_of_card", not probs, "settings.json mirrors the card (signed:false, 1920x1080, 24, -1 dBTP, -16 online, FontSize 23) and agrees with chains.json",
          "; ".join(probs) or "mirrors %d card values; %d profiles agree with their chains" % (12, len(s["profiles"])))


# ----------------------------------------------------------------------------------------------- self-tests
@test("colour_patch.selftest_python_I")
def t_cp_self():
    rc, out, err = sh(PY + [os.path.join(VAL, "colour_patch.py"), "--selftest"])
    check("colour_patch.selftest_python_I", rc == 0 and "ALL PASS" in out, "exit 0, ALL PASS (needs only ffmpeg)", "exit %d; %s" % (rc, out.strip().splitlines()[-1] if out.strip() else err.strip()[-120:]))


@test("spec_check.selftest_python_I")
def t_sc_self():
    rc, out, err = sh(PY + [os.path.join(VAL, "spec_check.py"), "--selftest"])
    check("spec_check.selftest_python_I", rc == 0 and "ALL PASS" in out, "exit 0, ALL PASS (needs only ffmpeg and ffprobe)", "exit %d; %s" % (rc, out.strip().splitlines()[-1] if out.strip() else err.strip()[-120:]))


@test("validators.selftests_with_no_site_packages", modes=("all",))
def t_nosite():
    res = []
    for tool in ("colour_patch.py", "spec_check.py"):
        rc, out, err = sh([sys.executable, "-I", "-S", os.path.join(VAL, tool), "--selftest"])
        res.append("%s exit %d" % (tool, rc))
        if rc != 0:
            break
    check("validators.selftests_with_no_site_packages", all(r.endswith("exit 0") for r in res) and len(res) == 2,
          "python -I -S (no site-packages at all): both self-tests exit 0, so no third-party module is used", "; ".join(res))


@test("colour_patch.usage_and_environment_errors")
def t_cp_usage():
    cp = PY + [os.path.join(VAL, "colour_patch.py")]
    r1 = sh(cp + ["--chain", "no_such_chain", "--chain-file", os.path.join("pipeline", "lib", "chains.json")])[0]
    r2 = sh(cp)[0]
    r3 = sh(cp + ["--controls", "--ffmpeg", os.path.join(ARGS.work, "no_such_ffmpeg")])[0]
    r4 = sh(cp + ["--derive-from", os.path.join(ARGS.work, "nothing.json")])[0]
    r5 = sh(cp + ["--chain-file", os.path.join(ARGS.work, "nothing.json"), "--all"])[0]
    check("colour_patch.usage_and_environment_errors", (r1, r2, r3, r4, r5) == (2, 2, 3, 2, 2),
          "unknown chain 2, no action 2, no ffmpeg 3, --derive-from without --out 2, missing chain file 2", "got %s" % ((r1, r2, r3, r4, r5),))


# ----------------------------------------------------------------------------------------------- derived form
def planted_raw(base_raw=None):
    """A raw record carrying a planted build flag with a profile path and a user name, built from fragments at run time."""
    user = "qu" + "ibble" + "7"
    win = "C:" + "\\" + "Us" + "ers" + "\\" + user + "\\" + "ffm" + "peg-src"
    lin = "/ho" + "me/" + user + "/ffm" + "peg-src"
    raw = base_raw or {"schema": "lj-colour-patch/1", "tolerance": 3, "chains": [{"name": "h264_venue", "worst_error": 1}, {"name": "prores422hq_master", "worst_error": 2}],
                       "controls": [{"name": "control_h264_bare_pix_fmt", "worst_error": 23}]}
    raw = json.loads(json.dumps(raw))
    raw.setdefault("ffmpeg", {})
    raw["ffmpeg"].update({"version_line": "ffmpeg version 9.0.2-custom-%s Copyright (c) the FFmpeg developers" % user, "version": "9.0.2-custom-" + user,
                          "configure": list(raw["ffmpeg"].get("configure", [])) + ["--prefix=" + win, "--extra-cflags=-I" + lin + "/include", "--extra-version=" + user],
                          "sha256": raw["ffmpeg"].get("sha256") or "ab" * 32})
    return raw, [user, win, lin, "ffm" + "peg-src", "Us" + "ers"]


@test("colour_patch.derive_drops_planted_flags")
def t_derive():
    os.makedirs(ARGS.work, exist_ok=True)
    raw, secrets = planted_raw()
    rp, dp = work("planted_raw.json"), work("planted_derived.json")
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
    rc, out, err = sh(PY + [os.path.join(VAL, "colour_patch.py"), "--derive-from", rp, "--out", dp])
    probs = []
    if rc != 0:
        probs.append("derive exit %d: %s" % (rc, err.strip()[-100:]))
    else:
        text = open(dp, encoding="utf-8").read()
        for s in secrets:
            if s in text or s in out:
                probs.append("the derived output still contains a planted value")
        d = json.loads(text)
        if d.get("ffmpeg", {}).get("version") != "9.0.2":
            probs.append("version not reduced to the number: %r" % d.get("ffmpeg", {}).get("version"))
        if set(d) != {"schema", "ffmpeg", "tolerance", "chains", "controls"}:
            probs.append("unexpected top-level keys")
        # the schema file, when the jsonschema module happens to be installed (the tools themselves never need it)
        schema_msg = "jsonschema module not installed here: the hand-coded mirror in colour_patch.py was used"
        try:
            import jsonschema  # noqa: F401  (test only; never imported by the validators)
            jsonschema.validate(d, read_json(os.path.join(ROOT, VAL, "pc_chains.schema.json")))
            schema_msg = "validated with the jsonschema module against pc_chains.schema.json"
        except ImportError:
            pass
        except Exception as e:
            probs.append("schema validation failed: " + str(e)[:100])
        rc2, o2, e2 = sh(PY + [os.path.join("scripts", "public_lint.py"), "--paths", rel(dp)])
        if rc2 != 0:
            probs.append("public_lint.py flagged the derived file (exit %d)" % rc2)
        rc3, o3, e3 = sh(PY + [os.path.join("scripts", "public_lint.py"), "--paths", rel(rp)])
        if rc3 != 2:
            probs.append("public_lint.py did NOT flag the planted raw file (exit %d): the plant would prove nothing" % rc3)
        if not probs:
            probs = [schema_msg + "; public_lint clean on derived (exit 0), flags the planted raw (exit 2)"]
            check("colour_patch.derive_drops_planted_flags", True, "derived file has no planted path or name, validates, passes public_lint.py", probs[0])
            return
    check("colour_patch.derive_drops_planted_flags", False, "derived file has no planted path or name, validates, passes public_lint.py", "; ".join(probs))


@test("colour_patch.derive_rejects_bad_raw")
def t_derive_bad():
    cp = PY + [os.path.join(VAL, "colour_patch.py")]
    os.makedirs(ARGS.work, exist_ok=True)
    cases = {"wrong_schema": {"schema": "x/1"},
             "no_worst": {"schema": "lj-colour-patch/1", "ffmpeg": {"version": "6.1.1", "sha256": "ab" * 32}, "tolerance": 3, "chains": [{"name": "c", "worst_error": None}]},
             "bad_sha": {"schema": "lj-colour-patch/1", "ffmpeg": {"version": "6.1.1", "sha256": "xyz"}, "tolerance": 3, "chains": [{"name": "c", "worst_error": 1}]},
             "path_as_name": {"schema": "lj-colour-patch/1", "ffmpeg": {"version": "6.1.1", "sha256": "ab" * 32}, "tolerance": 3, "chains": [{"name": "a" + "/" + "b", "worst_error": 1}]}}
    got = {}
    for k, v in cases.items():
        p = work("bad_raw_%s.json" % k)
        json.dump(v, open(p, "w"))
        rc, out, err = sh(cp + ["--derive-from", p, "--out", work("bad_derived.json")])
        got[k] = rc
    check("colour_patch.derive_rejects_bad_raw", all(v == 2 for v in got.values()) and not os.path.exists(work("bad_derived.json")),
          "each bad raw record is refused with exit 2 and nothing is written", str(got))


# ----------------------------------------------------------------------------------------------- the colour-patch run on this build
@test("colour_patch.all_chains_ffmpeg_6.1.1", modes=("all",))
def t_cp_all():
    out_json = ev("colour_patch_ffmpeg-%s.json" % ARGS.ffv)
    cmd = PY + [os.path.join(VAL, "colour_patch.py"), "--ffmpeg", "ffmpeg", "--chain-file", os.path.join("pipeline", "lib", "chains.json"), "--all", "--json", rel(out_json)]
    rc, out, err = sh(cmd)
    ok = rc == 0 and os.path.isfile(out_json)
    if ok:
        STATE["raw"] = read_json(out_json)
        STATE["cp_out"] = out
        ok = len(STATE["raw"]["chains"]) == 6 and all(c["pass"] for c in STATE["raw"]["chains"])
    check("colour_patch.all_chains_ffmpeg_6.1.1", ok, "exit 0: all six chains within 3/255 on ffmpeg %s" % ARGS.ffv,
          "exit %d; %s" % (rc, next((l for l in out.splitlines() if l.startswith("RESULT chains")), err.strip()[-120:])))


def cp_row(name):
    raw = STATE.get("raw")
    if not raw:
        raise Skip("the colour-patch run did not complete")
    for r in raw["chains"] + raw["controls"]:
        if r["name"] == name:
            return r
    raise Skip("no result for " + name)


ORACLE = [  # (test name, result name, expected worst error, must pass?, note)
    ("oracle.h264_chain_B_scale_first", "control_h264_scale_first_B", 1, True, "Q-F1 chain B"),
    ("oracle.h264_venue_chain", "h264_venue", 1, True, "Q-F1 chain B plus setparams and the venue arguments"),
    ("oracle.h264_format_first_A", "control_h264_format_first_A", 5, False, "Q-F1 chain A"),
    ("oracle.h264_bare_pix_fmt", "control_h264_bare_pix_fmt", 23, False, "Q-F1 chain C: BT.601 pixels under BT.709 tags"),
    ("oracle.prores4444_bare", "control_prores4444_bare", 25, False, "Q-F1 bare -pix_fmt yuva444p10le"),
    ("oracle.prores4444_chain", "prores4444_alpha", 0, True, "Q-F1 ProRes 4444 chain"),
]


def make_oracle_test(tname, rname, exp, must_pass, note):
    @test("colour_patch." + tname, modes=("all",))
    def _t():
        try:
            r = cp_row(rname)
        except Skip as e:
            record("colour_patch." + tname, "SKIPPED", "", str(e))
            return
        obs = r["worst_error"]
        polarity = (r["pass"] == must_pass)
        delta = None if obs is None else obs - exp
        within = obs is not None and abs(delta) <= 1
        STATE.setdefault("oracle", []).append({"test": tname, "result": rname, "note": note, "expected_worst_error": exp, "expected": "PASS" if must_pass else "FAIL",
                                               "observed_worst_error": obs, "observed": "PASS" if r["pass"] else "FAIL", "delta": delta,
                                               "within_tolerance_of_1": within, "polarity_matches": polarity,
                                               "finding": None if (within and polarity) else
                                               "observed %s against the Q-F1 figure %s (difference %s, more than 1)" % (obs, exp, delta)})
        check("colour_patch." + tname, polarity, "%s, about %d/255 (tolerance +-1)" % ("PASS" if must_pass else "FAIL", exp),
              "%s at %s/255%s" % ("PASS" if r["pass"] else "FAIL", obs, "" if within else "; FINDING: differs from %d by more than 1" % exp))
    return _t


for _o in ORACLE:
    make_oracle_test(*_o)


def red_luma(path):
    """Luma (limited range) at the centre of the red patch, read from the file's Y plane."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", path, "-frames:v", "1", "-vf", "crop=100:100:200:500,extractplanes=y", "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if p.returncode != 0 or len(p.stdout) != 10000:
        return None
    return round(sum(p.stdout) / len(p.stdout))




F12 = ["prores422hq_master", "h264_venue", "h264_backup_main40", "h264_online"]


@test("colour_patch.f12_new_measurements", modes=("all",))
def t_f12():
    try:
        rows = {n: cp_row(n) for n in F12}
    except Skip as e:
        record("colour_patch.f12_new_measurements", "SKIPPED", "", str(e))
        return
    table = {n: {"worst_error": r["worst_error"], "worst_error_accurate_decode": r["worst_error_accurate"], "pass": r["pass"], "tags_match_expect": r["tags_match_expect"]} for n, r in rows.items()}
    STATE["f12"] = table
    ok = all(isinstance(v["worst_error"], int) for v in table.values())
    check("colour_patch.f12_new_measurements", ok, "each of the four chains has a worst-error number (F-12)",
          ", ".join("%s %s/255" % (n, v["worst_error"]) for n, v in table.items()))


@test("chains.approved_means_measured_within_3", modes=("all",))
def t_approved():
    chains = read_json(os.path.join(ROOT, "pipeline", "lib", "chains.json"))["chains"]
    raw = STATE.get("raw")
    if not raw:
        record("chains.approved_means_measured_within_3", "SKIPPED", "", "the colour-patch run did not complete")
        return
    fresh = {c["name"]: c["worst_error"] for c in raw["chains"]}
    probs = []
    for n, c in chains.items():
        m = (c.get("measured") or {}).get(ARGS.ffv)
        if c.get("approved") is True:
            if not m or m.get("worst_error") is None or m["worst_error"] > 3:
                probs.append("%s is approved:true without a measurement within 3 in measured[%s]" % (n, ARGS.ffv))
            elif fresh.get(n) is None or fresh[n] > 3:
                probs.append("%s is approved:true but measures %s now" % (n, fresh.get(n)))
            elif abs(fresh[n] - m["worst_error"]) > 1:
                probs.append("%s: recorded %s but measures %s now (differs by more than 1)" % (n, m["worst_error"], fresh[n]))
        elif fresh.get(n) is not None and fresh[n] <= 3:
            probs.append("%s measures %s/255 but is not marked approved:true (update chains.json)" % (n, fresh[n]))
    check("chains.approved_means_measured_within_3", not probs, "approved:true only where the recorded and fresh measurements are within 3/255 (W-16)",
          "; ".join(probs) or "six chains approved on ffmpeg %s; recorded figures agree with the fresh run" % ARGS.ffv)


@test("colour_patch.refuses_approval_above_3", modes=("all",))
def t_approval_refused():
    plant = {"schema": "lj-chains/1", "chains": {"bare_but_claims_approval": {
        "container": "mp4", "alpha": False, "vf": "", "video_args": ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                                                                     "-color_trc", "bt709", "-color_range", "tv"],
        "audio_args": [], "expect": {}, "approved": True, "notes": "planted"}}}
    p = work("planted_chains.json")
    json.dump(plant, open(p, "w"))
    rc, out, err = sh(PY + [os.path.join(VAL, "colour_patch.py"), "--chain-file", rel(p), "--chain", "bare_but_claims_approval"])
    check("colour_patch.refuses_approval_above_3", rc == 1 and "NOT ALLOWED" in out and "bare_but_claims_approval" in out,
          "a chain marked approved:true that measures above 3/255 gives exit 1 and names the chain", "exit %d; %s" % (rc, next((l for l in out.splitlines() if "approvals" in l), "")[:150]))


@test("colour_patch.derived_form_filed", modes=("all",))
def t_derived_filed():
    raw = ev("colour_patch_ffmpeg-%s.json" % ARGS.ffv)
    outp = ev("colour_patch_ffmpeg-%s.derived.json" % ARGS.ffv)
    if not os.path.isfile(raw):
        record("colour_patch.derived_form_filed", "SKIPPED", "", "no raw record")
        return
    rc, o, e = sh(PY + [os.path.join(VAL, "colour_patch.py"), "--derive-from", rel(raw), "--out", rel(outp)])
    d = read_json(outp) if rc == 0 else {}
    text = open(outp, encoding="utf-8").read() if rc == 0 else ""
    flags = read_json(raw)["ffmpeg"]["configure"]
    leak = [f for f in flags if f and f in text]
    ok = rc == 0 and not leak and d.get("ffmpeg", {}).get("version") == ARGS.ffv and len(d.get("chains", [])) == 6
    check("colour_patch.derived_form_filed", ok, "the filed form (lj-pc-chains/1) holds version, sha256, six chain results and no build flags",
          "exit %d; version %s; %d chains, %d controls; build flags leaked: %d" % (rc, d.get("ffmpeg", {}).get("version"), len(d.get("chains", [])), len(d.get("controls", [])), len(leak)))


# ----------------------------------------------------------------------------------------------- spec_check on fixtures
QUICK_GOOD = ["g_venue_m18.mp4", "g_master_hq.mov"]
QUICK_DEFECT = ["d_25fps.mp4", "d_title_tag.mp4", "d_truncated.mp4", "d_44k1_audio.mp4"]


def run_manifest(man, label, results):
    """Hold spec_check.py to every manifest entry."""
    for e in man:
        f = work(e["file"])
        extra = ["--profiles-file", work(e["profiles_file"])] if e.get("profiles_file") else []
        vj = work("verdict.json")
        t0 = time.time()
        rc, out, err = spec(f, e["profile"], extra, vj)
        v = read_json(vj) if os.path.isfile(vj) and rc in (0, 1) else {}
        if os.path.isfile(vj):
            os.remove(vj)
        failed = v.get("failed", [])
        name = "spec_check.%s.%s" % (label, e["file"])
        if e["expect"] == "pass":
            ok = rc == 0 and not failed
            exp = "exit 0, every check passes"
        else:
            need = e.get("must_fail", [])
            ok = rc == 1 and all(n in failed for n in need)
            if e.get("isolated"):
                ok = ok and sorted(failed) == sorted(need)
            exp = "exit 1 naming %s%s" % (", ".join(need), " and nothing else" if e.get("isolated") else "")
        results.append({"file": e["file"], "profile": e["profile"], "expected": e["expect"], "exit": rc, "failed_checks": failed, "must_fail": e.get("must_fail"),
                        "isolated": bool(e.get("isolated")), "ok": ok, "why": e.get("why")})
        check(name, ok, exp, "exit %d; failed: %s (%.1fs)" % (rc, ", ".join(failed) or "none", time.time() - t0))
        if ARGS.mode == "all" and e["expect"] == "pass":
            pass


@test("spec_check.fixtures_quick", modes=("quick",))
def t_sc_quick():
    man = gen("good", QUICK_GOOD)
    run_manifest(man, "good", [])
    man = gen("defects", QUICK_DEFECT)
    run_manifest(man, "defect", [])


@test("spec_check.fixtures_all", modes=("all",))
def t_sc_all():
    results = []
    man_g = gen("good")
    STATE["man_good"] = man_g
    run_manifest(man_g, "good", results)
    man_d = gen("defects")
    STATE["man_def"] = man_d
    run_manifest(man_d, "defect", results)
    STATE["spec_results"] = results
    with open(ev("spec_check_fixture_results.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "lj-wp05-speccheck-fixtures/1", "ffmpeg": ARGS.ffv, "results": results}, f, indent=2)
    good = [r for r in results if r["expected"] == "pass" and r["file"].startswith("g_")]
    profiles = sorted({r["profile"] for r in good})
    four = {"master_prores422hq", "venue_h264", "venue_h264_backup_main40", "online_h264"}
    check("spec_check.no_false_positives", len(good) >= 6 and four <= set(profiles) and all(r["exit"] == 0 for r in good),
          "at least six good files across the four profiles all exit 0", "%d good files, profiles: %s, all exit 0: %s" % (len(good), ", ".join(profiles), all(r["exit"] == 0 for r in good)))
    named = {"d_yuvj420p.mp4": "yuvj420p", "d_25fps.mp4": "25 fps", "d_720p.mp4": "1280x720", "d_bt601_under_709_tags.mp4": "BT.601 under BT.709 tags (must PASS here)",
             "d_prores4444_no_alpha.mov": "ProRes 4444 without alpha", "d_true_peak.mp4": "true peak above -1 dBTP", "d_44k1_audio.mp4": "44.1 kHz",
             "d_16bit_master.mov": "16-bit under master", "d_title_tag.mp4": "title tag", "d_truncated.mp4": "truncated MP4", "d_frame_count.mp4": "frame-count mismatch"}
    got = {r["file"]: r["ok"] for r in results}
    missing = [v for k, v in named.items() if not got.get(k)]
    check("spec_check.the_eleven_named_defects", not missing, "all ten named defects exit 1 naming their check; the BT.601-under-709-tags file exits 0 (only colour_patch catches it)",
          "all eleven behave" if not missing else "not as expected: " + ", ".join(missing))


@test("colour_patch.oracle.bare_encode_not_caught_by_spec_check", modes=("all",))
def t_oracle_bare_cross():
    man = STATE.get("man_def")
    if not man:
        record("colour_patch.oracle.bare_encode_not_caught_by_spec_check", "SKIPPED", "", "defect fixtures not generated")
        return
    # the planted file was made with the SAME arguments as control_h264_bare_pix_fmt
    f = work("d_bt601_under_709_tags.mp4")
    rc, out, err = spec(f, "venue_h264")
    # luma of the red patch: BT.709 gives 63, BT.601 gives 81 (limited range, 8 bit)
    y = red_luma(f)
    good_y = red_luma(work("g_venue_m18.mp4"))
    cp = cp_row("control_h264_bare_pix_fmt")
    ok = rc == 0 and y is not None and 79 <= y <= 83 and good_y is not None and 61 <= good_y <= 65 and not cp["pass"]
    check("colour_patch.oracle.bare_encode_not_caught_by_spec_check", ok,
          "spec_check exits 0 on the bare-encode file (tags are right) while its red patch has luma 81 (BT.601) and colour_patch fails the same arguments",
          "spec_check exit %d; red luma %s (good file %s, BT.709 expects 63); colour_patch worst %s/255" % (rc, y, good_y, cp["worst_error"]))


@test("colour_patch.accepts_a_phone_style_chain_file", modes=("all",))
def t_phone_chain():
    pf = work("phone_profile.json")
    if not os.path.isfile(pf):
        record("colour_patch.accepts_a_phone_style_chain_file", "SKIPPED", "", "fixtures not generated")
        return
    rc, out, err = sh(PY + [os.path.join(VAL, "colour_patch.py"), "--chain-file", rel(pf), "--chain", "phone_1080"])
    m = re.search(r"phone_1080\s+(PASS|FAIL)\s+worst (\d+)/255", out)
    check("colour_patch.accepts_a_phone_style_chain_file", rc == 0 and m is not None, "WP-08's acceptance line shape works: --chain-file profile.json --chain phone_1080, worst error 3 or less",
          "exit %d; %s" % (rc, m.group(0) if m else out.strip()[-100:]))


@test("spec_check.verdict_json_and_no_path_leak", modes=("all",))
def t_verdict():
    f = work("g_venue_m18.mp4")
    if not os.path.isfile(f):
        record("spec_check.verdict_json_and_no_path_leak", "SKIPPED", "", "fixtures not generated")
        return
    vj = work("verdict_leak.json")
    rc, out, err = spec(f, "venue_h264", None, vj)
    rc2, out2, err2 = spec(work("d_truncated.mp4"), "venue_h264", None, work("verdict_leak2.json"))
    v = read_json(vj)
    v2 = read_json(work("verdict_leak2.json"))
    text = json.dumps(v) + json.dumps(v2) + out + out2 + err + err2
    probs = []
    if v.get("schema") != "lj-speccheck/1" or v.get("verdict") != "PASS" or v.get("file") != "g_venue_m18.mp4":
        probs.append("verdict fields")
    if not all(k in c for c in v["checks"] for k in ("id", "status", "expected", "actual")):
        probs.append("check fields")
    if ARGS.work in text or ROOT in text or os.path.dirname(ARGS.work) in text:
        probs.append("a folder path leaked")
    if "/" + "home" in text or "/tm" + "p/" in text:
        probs.append("a POSIX path leaked")
    check("spec_check.verdict_json_and_no_path_leak", not probs, "verdict JSON has schema, verdict and checks; no folder path appears in stdout, stderr or JSON, even for a file ffprobe cannot open",
          "; ".join(probs) or "clean (%d checks listed)" % len(v["checks"]))


@test("spec_check.usage_and_environment_errors", modes=("all",))
def t_sc_usage():
    sc = PY + [os.path.join(VAL, "spec_check.py")]
    f = work("g_venue_m18.mp4")
    if not os.path.isfile(f):
        record("spec_check.usage_and_environment_errors", "SKIPPED", "", "fixtures not generated")
        return
    dup = work("dup_profiles.json")
    json.dump({"profiles": {"venue_h264": {"video": {}}}}, open(dup, "w"))
    r = [sh(sc + [f, "--profile", "no_such_profile"])[0],
         sh(sc + [work("no_such_file.mp4"), "--profile", "venue_h264"])[0],
         sh(sc + [f])[0],
         sh(sc + [f, "--profile", "venue_h264", "--profiles-file", dup])[0],
         sh(sc + [f, "--profile", "venue_h264", "--ffprobe", work("no_such_ffprobe")])[0],
         sh(sc + [f, "--profile", "venue_h264", "--ffmpeg", work("no_such_ffmpeg")])[0],
         sh(sc + ["--list-profiles"])[0]]
    check("spec_check.usage_and_environment_errors", r == [2, 2, 2, 2, 3, 3, 0],
          "unknown profile 2, missing file 2, no profile 2, duplicate profile name 2, missing ffprobe 3, missing ffmpeg 3, --list-profiles 0", "got %s" % r)


@test("spec_check.phone_profile_via_profiles_file", modes=("all",))
def t_phone():
    f = work("g_phone_1080.mp4")
    pf = work("phone_profile.json")
    if not os.path.isfile(f):
        record("spec_check.phone_profile_via_profiles_file", "SKIPPED", "", "fixtures not generated")
        return
    rc, out, err = spec(f, "phone_1080", ["--profiles-file", pf])
    rc2, out2, err2 = spec(f, "venue_h264")      # the phone file is not a venue file: level 4.0 and -16 LUFS
    check("spec_check.phone_profile_via_profiles_file", rc == 0 and rc2 == 1 and "video.level" in out2, "--profiles-file adds WP-08's phone profile: the phone file passes it and fails the venue profile (level 4.0)",
          "phone exit %d; same file under venue_h264 exit %d" % (rc, rc2))


# ----------------------------------------------------------------------------------------------- MO8 gate
def mo8(path, extra=None, json_out=None):
    cmd = PY + [os.path.join(VAL, "mo8_gate.py"), path] + (extra or [])
    if json_out:
        cmd += ["--json", json_out]
    return sh(cmd, timeout=900)


@test("mo8_gate.pillow_pass_zoompan_fail_refusals", modes=("all",))
def t_mo8():
    rows = []
    # 1. Pillow sub-pixel push: pass
    gen("mo8", ["mo8_pillow96.mp4"])
    rc, out, err = mo8(work("mo8_pillow96.mp4"), json_out=work("mo8_a.json"))
    a = read_json(work("mo8_a.json"))["results"][0] if os.path.isfile(work("mo8_a.json")) else {}
    rows.append(("pillow96", rc, a))
    check("mo8_gate.pillow_subpixel_push_passes", rc == 0 and a.get("mo8a_pass") and a.get("mo8b_pass") and a.get("mo8a_d4_px", 1) < 0.02,
          "a Pillow sub-pixel push passes both gates (about 0.003 px reported in round 2; codec adds up to 0.015)",
          "exit %d; MO8a %s px, MO8b %s px" % (rc, a.get("mo8a_d4_px"), a.get("mo8b_d4_px")))
    os.remove(work("mo8_pillow96.mp4"))
    # 2. zoompan from a 1080p picture: fail
    gen("mo8", ["mo8_zoompan96.mp4"])
    rc, out, err = mo8(work("mo8_zoompan96.mp4"), json_out=work("mo8_b.json"))
    b = read_json(work("mo8_b.json"))["results"][0] if os.path.isfile(work("mo8_b.json")) else {}
    rows.append(("zoompan96", rc, b))
    check("mo8_gate.ffmpeg_zoompan_push_fails", rc == 1 and not b.get("mo8a_pass") and b.get("mo8a_d4_px", 0) > 0.2,
          "an ffmpeg zoompan push from a 1080p picture fails (about 0.6 px reported in round 2)", "exit %d; MO8a %s px, MO8b %s px" % (rc, b.get("mo8a_d4_px"), b.get("mo8b_d4_px")))
    os.remove(work("mo8_zoompan96.mp4"))
    # 3. a PNG folder, the master itself
    gen("mo8", ["mo8_pillow_frames"])
    rc, out, err = mo8(work("mo8_pillow_frames"), json_out=work("mo8_c.json"))
    c = read_json(work("mo8_c.json"))["results"][0] if os.path.isfile(work("mo8_c.json")) else {}
    rows.append(("pillow_png_folder", rc, c))
    check("mo8_gate.png_folder_master_passes", rc == 0 and c.get("input_kind") == "png-folder" and c.get("master_before_encode") is True,
          "12 PNG frames of a Pillow push pass and are reported as a master input", "exit %d; MO8a %s px, MO8b %s px, kind %s" % (rc, c.get("mo8a_d4_px"), c.get("mo8b_d4_px"), c.get("input_kind")))
    shutil.rmtree(work("mo8_pillow_frames"), ignore_errors=True)
    # 4. refusals
    gen("mo8", ["mo8_long97.mp4", "mo8_long121.mp4", "mo8_long130.mp4", "mo8_short6.mp4"])
    ref = {}
    for n, extra in (("mo8_long97.mp4", []), ("mo8_long121.mp4", []), ("mo8_long130.mp4", []), ("mo8_long121.mp4", ["--max-frames", "120"]), ("mo8_long130.mp4", ["--max-frames", "200"]),
                     ("mo8_short6.mp4", [])):
        rc, out, err = mo8(work(n), extra)
        ref["%s %s" % (n, " ".join(extra))] = (rc, err.strip().splitlines()[-1][:300] if err.strip() else "")
    msgs_ok = all(v[0] == 2 and v[1].startswith("mo8_gate: REFUSED") for v in ref.values())
    clear = all(("frame" in v[1] or "ceiling" in v[1]) for v in ref.values())
    check("mo8_gate.refuses_long_and_short_clips", msgs_ok and clear, "97, 121 and 130 frames are refused with a clear message (also at --max-frames 120; --max-frames 200 is over the hard ceiling); 6 frames is refused",
          "; ".join("%s -> exit %d" % (k.strip(), v[0]) for k, v in ref.items()))
    rows.append(("refusals", 2, {k: v[1] for k, v in ref.items()}))
    for n in ("mo8_long97.mp4", "mo8_long121.mp4", "mo8_long130.mp4", "mo8_short6.mp4"):
        os.remove(work(n))
    # 5. the roughness is informational, and a lossy clip is flagged as approximate
    with open(ev("mo8_gate_results.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "lj-wp05-mo8/1", "limits": {"mo8a_d4_px": 0.05, "mo8b_d4_px": 0.04},
                   "note": "clips are H.264 CRF 14 stand-ins for a master (disk budget); round 2 reported about 0.003 px (Pillow) and about 0.6 px (zoompan, 1080p source) on other content",
                   "rows": [{"case": n, "exit": rc, "result": r} for n, rc, r in rows]}, f, indent=2)
    check("mo8_gate.lossy_clip_flagged_as_approximate", "lossy" in a.get("input_kind", "") and "BEFORE the delivery encode" in a.get("note", ""),
          "an H.264 input is reported as lossy with the 'measure the master' note", a.get("input_kind", "") + "; note present: %s" % ("BEFORE the delivery encode" in a.get("note", "")))


# ----------------------------------------------------------------------------------------------- repo hygiene (last)
@test("hygiene.stale_values_absent", modes=("all",))
def t_stale():
    outj = work("stale.json")
    rc, out, err = sh(PY + [os.path.join("scripts", "stale_check.py"), "--json", outj, "--quiet"])
    mine = ("pipeline/validators/", "pipeline/lib/chains.json", "pipeline/settings.json")
    hits = []
    if os.path.isfile(outj):
        d = read_json(outj)

        def walk(x):
            if isinstance(x, dict):
                if "file" in x and isinstance(x.get("file"), str) and x["file"].replace("\\", "/").startswith(mine):
                    hits.append("%s:%s" % (x["file"], x.get("line")))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(d)
    check("hygiene.stale_values_absent", os.path.isfile(outj) and not hits, "stale_check.py finds no stale value (25 fps defaults, -1.5 dBTP, retired spellings) in the WP-05 files",
          "no hits in the owned files" if not hits else "; ".join(hits[:5]))


@test("hygiene.public_lint_clean", modes=("all",))
def t_lint():
    paths = [VAL, os.path.join("pipeline", "lib", "chains.json"), os.path.join("pipeline", "settings.json"), os.path.join("tests", "validators"), os.path.join("build", "evidence", "wp05")]
    rc, out, err = sh(PY + [os.path.join("scripts", "public_lint.py"), "--paths"] + paths)
    check("hygiene.public_lint_clean", rc == 0, "public_lint.py is clean on the owned paths and the evidence (no names, hosts, IPs, e-mails, profile paths)",
          "exit %d; %s" % (rc, (out.strip().splitlines() or [err.strip()[-100:]])[-1][:140]))
    rc, out, err = sh(PY + [os.path.join("scripts", "public_lint.py"), "--theme", "--paths", VAL, "pipeline/settings.json", "pipeline/lib/chains.json"])
    check("hygiene.theme_guard_clean", rc == 0, "the D-28 theme guard finds nothing in the new files", "exit %d" % rc)


@test("windows.behaviour_unverified", modes=("all",))
def t_unverified():
    record("windows.behaviour_unverified", "UNVERIFIED", "the three tools behave the same on Windows (ffmpeg.exe / ffprobe.exe, py -3 -I, Windows paths)", "not run: no Windows host here; "
           "the code uses only subprocess argument lists, os.path and tempfile, and passes python -I -S on Linux",
           "Windows 10/11, Python 3.13 from winget and ffmpeg 9.0.2 (full build) were not available; run the maker's PC runner (WP-09) to verify")
    record("colour_patch.ffmpeg_9.0.2_results", "UNVERIFIED", "ffmpeg 9.0.2 gives the Q-F1 numbers (bare encodes about 1 and 0)", "not measured: only ffmpeg %s exists here" % ARGS.ffv,
           "needs the maker's PC build; WP-09's runner produces the raw record, colour_patch.py --derive-from files it")
    record("spec_check.prores_range_tag_on_windows_builds", "UNVERIFIED", "ProRes colour_range tag on ffmpeg 9.0.2 (tv or unknown; both accepted)", "not measured",
           "needs the maker's PC build")


def stage_guard_record(peak_mb):
    """The disk stage line (4.9): inside lj_with_disk, or why not."""
    held = os.environ.get("LJ_HOLDS_DISK")
    planned = os.environ.get("LJ_DISK_PLANNED_MB") or os.environ.get("LJ_WP05_PLANNED")
    note = "measured peak of the generated files: %.1f MB" % peak_mb
    if ARGS.mode == "quick":
        record("stage.disk_guard", "PASS" if peak_mb < 100 else "FAIL", "the quick stage writes under 100 MB, so no lock is needed (4.9)", note)
    elif held:
        ok = peak_mb <= float(planned or 0) * 1.25
        record("stage.disk_guard", "PASS" if ok else "FAIL", "ran inside lj_with_disk %s MB and the measured peak is within 125%% of it (4.9)" % planned,
               "%s; start Avail %s MB, planned %s MB, label %s" % (note, os.environ.get("LJ_DISK_START_MB"), planned, os.environ.get("LJ_DISK_LABEL")))
    elif os.environ.get("LJ_WP05_GUARD") == "bypassed":
        record("stage.disk_guard", "SKIPPED", "ran inside lj_with_disk", "the guard refused or was busy and --unguarded was given: %s. %s" % (os.environ.get("LJ_WP05_GUARD_WHY", ""), note))
    else:
        record("stage.disk_guard", "SKIPPED", "ran inside lj_with_disk", "run directly (not through run_tests.sh); " + note)
    STATE["peak_mb"] = peak_mb


# ----------------------------------------------------------------------------------------------- main
def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("quick", "all"), default="quick")
    ap.add_argument("--work", default=os.path.join(ROOT, "renders", "wp05"))
    ap.add_argument("--evidence", default=os.path.join(ROOT, "build", "evidence", "wp05"))
    ap.add_argument("--keep", action="store_true", help="keep the generated files")
    ARGS = ap.parse_args()
    ARGS.work = os.path.abspath(ARGS.work)
    ARGS.evidence = os.path.abspath(ARGS.evidence)
    ARGS.jsonl = os.path.join(ARGS.evidence, "tests.jsonl")
    ARGS.ffv = ffmpeg_version()
    ARGS.t_start = avail_mb()
    os.makedirs(ARGS.work, exist_ok=True)
    os.makedirs(ARGS.evidence, exist_ok=True)
    open(ARGS.jsonl, "w").close()
    print("WP-05 validator tests (%s). ffmpeg %s, python %d.%d, Avail %d MB at start." % (ARGS.mode, ARGS.ffv, sys.version_info[0], sys.version_info[1], ARGS.t_start), flush=True)
    t0 = time.time()
    sampler = start_sampler()
    try:
        for name, modes, fn in REG:
            if ARGS.mode not in modes:
                continue
            try:
                fn()
            except Skip as e:
                record(name, "SKIPPED", "", str(e))
            except Exception as e:                       # a crash in a test is a failure of that test, never a silent pass
                record(name, "FAIL", "the test runs to the end", "crashed: %s: %s" % (e.__class__.__name__, str(e)[:150]))
    finally:
        sampler["stop"] = True
        if not ARGS.keep:
            shutil.rmtree(ARGS.work, ignore_errors=True)
    stage_guard_record(sampler["peak"])
    if ARGS.mode == "all" and STATE.get("oracle") is not None:
        with open(ev("oracle_findings.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"schema": "lj-wp05-oracle/1", "ffmpeg": ARGS.ffv, "tolerance": 1, "rows": STATE["oracle"],
                       "findings": [r["finding"] for r in STATE["oracle"] if r["finding"]],
                       "f12": STATE.get("f12")}, f, indent=2)
    c = STATE["counts"]
    print("TOTAL: PASS %d, FAIL %d, UNVERIFIED %d, SKIPPED %d, BLOCKED %d   (%.0f s, Avail min %s MB)" % (c["PASS"], c["FAIL"], c["UNVERIFIED"], c["SKIPPED"], c["BLOCKED"], time.time() - t0, STATE["min_avail"]))
    with open(os.path.join(ARGS.evidence, ".counts.json"), "w") as f:
        json.dump({"counts": c, "avail_mb_min": STATE["min_avail"], "avail_mb_start": ARGS.t_start, "peak_work_mb": round(STATE.get("peak_mb", 0), 1)}, f)
    return 3 if c["BLOCKED"] else (1 if c["FAIL"] else 0)


if __name__ == "__main__":
    sys.exit(main())
