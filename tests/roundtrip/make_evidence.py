#!/usr/bin/env python3
"""make_evidence.py: build build/evidence/wp06/summary.json and environment.json from the test envelopes (WP-06).

  python3 -I tests/roundtrip/make_evidence.py

Reads build/evidence/wp06/tests.jsonl (the last --all run), tests_quick.jsonl (the last --quick run), .counts.json (written by run_checks.py), guard_stage_venv.json
(the disk guard's ledger line for the venv stage) and the pip list of the venv. Writes summary.json, environment.json and venv_otio.json. No host, user or path
information is recorded: versions, counts and sizes only.
"""
import datetime
import json
import os
import platform
import shutil
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EV = os.path.join(ROOT, "build", "evidence", "wp06")
SCRATCH = os.environ.get("LJ_SCRATCH", os.path.normpath(os.path.join(ROOT, "..", "build-scratch")))
VENV = os.path.join(SCRATCH, "venv-otio")


def lines(name):
    p = os.path.join(EV, name)
    if not os.path.isfile(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def tally(recs):
    t = {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0}
    for r in recs:
        t[r["status"]] += 1
    return t


def out_of(cmd):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60).stdout.decode().strip()
    except Exception:
        return ""


def tree_mb(path):
    n = 0
    for dp, dn, fn in os.walk(path):
        for f in fn:
            try:
                n += os.lstat(os.path.join(dp, f)).st_size
            except OSError:
                pass
    return round(n / 1048576.0, 1)


def main():
    allr, quick = lines("tests.jsonl"), lines("tests_quick.jsonl")
    groups = {}
    for r in allr:
        groups.setdefault(r["test"].split(".")[0], {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0})[r["status"]] += 1
    counts = {}
    p = os.path.join(EV, ".counts.json")
    if os.path.isfile(p):
        counts = json.load(open(p))
    guard = {}
    gp = os.path.join(EV, "guard_stage_venv.json")
    if os.path.isfile(gp) and open(gp).read().strip():
        try:
            guard = json.loads(open(gp).read().strip().splitlines()[-1])
        except ValueError:
            guard = {}
    vpy = os.path.join(VENV, "bin", "python")
    venv = {"exists": os.path.isfile(vpy), "opentimelineio": out_of([vpy, "-I", "-c", "import opentimelineio as o; print(o.__version__)"]) if os.path.isfile(vpy) else None,
            "size_mb": tree_mb(VENV) if os.path.isdir(VENV) else None,
            "pip_packages": [l.strip() for l in out_of([vpy, "-m", "pip", "list", "--format=freeze", "--disable-pip-version-check"]).splitlines() if l.strip()] if os.path.isfile(vpy) else [],
            "created_by": "python3 -m venv, then pip install --no-cache-dir opentimelineio==0.18.1, run directly because the lj_with_disk stage was refused (guard_stage_venv.json, venv_guard_refusal.txt)",
            "guard_ledger_line": guard or None, "wheel_download": "843 kB"}
    summary = {"schema": "lj-evidence-summary/1", "package": "WP-06", "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
               "all_run": tally(allr), "quick_run": tally(quick), "groups": groups,
               "disk": {"venv_stage_label": guard.get("label"), "venv_stage_planned_mb": guard.get("planned_mb"), "venv_stage_status": guard.get("status"),
                        "venv_stage_avail_mb_start": guard.get("avail_mb_start"), "floor_mb": 400, "hard_floor_mb": 250,
                        "test_run_min_avail_mb": counts.get("min_avail"), "measured_peak_of_generated_files_mb": counts.get("peak_work_mb"),
                        "venv_size_mb": venv["size_mb"]},
               "unverified": sorted({r["test"] for r in allr if r["status"] == "UNVERIFIED"}),
               "skipped": sorted({r["test"] for r in allr if r["status"] == "SKIPPED"})}
    env = {"platform": "linux", "python": "%d.%d.%d" % sys.version_info[:3], "pillow": out_of([sys.executable, "-I", "-c", "import PIL; print(PIL.__version__)"]),
           "inkscape": (out_of(["inkscape", "--version"]).splitlines() or [""])[0] if shutil.which("inkscape") else None,
           "opentimelineio": venv["opentimelineio"], "nproc": os.cpu_count(), "machine": platform.machine()}
    for name, obj in (("summary.json", summary), ("environment.json", env), ("venv_otio.json", venv)):
        with open(os.path.join(EV, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=2, sort_keys=True)
            f.write("\n")
    try:
        os.remove(os.path.join(EV, ".counts.json"))
    except OSError:
        pass
    print("wrote summary.json, environment.json and venv_otio.json; all-run:", summary["all_run"], "quick-run:", summary["quick_run"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
