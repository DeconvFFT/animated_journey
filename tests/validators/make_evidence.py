#!/usr/bin/env python3
"""make_evidence.py: build build/evidence/wp05/summary.json and environment.json from the test envelopes (WP-05).

  python3 -I tests/validators/make_evidence.py

Reads build/evidence/wp05/tests.jsonl (the last run), tests_quick.jsonl (the last --quick run), .counts.json (written by run_checks.py) and
guard_stage.json (the disk guard's ledger line for the stage). Writes summary.json and environment.json. No host, user or path information is
recorded: versions and counts only.
"""
import datetime
import json
import os
import platform
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EV = os.path.join(ROOT, "build", "evidence", "wp05")


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


def version_of(cmd):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30).stdout.decode().split("\n")[0].strip()
    except Exception:
        return None


def main():
    allr, quick = lines("tests.jsonl"), lines("tests_quick.jsonl")
    groups = {}
    for r in allr:
        g = r["test"].split(".")[0]
        groups.setdefault(g, {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0})[r["status"]] += 1
    counts = {}
    p = os.path.join(EV, ".counts.json")
    if os.path.isfile(p):
        counts = json.load(open(p))
    guard = {}
    gp = os.path.join(EV, "guard_stage.json")
    if os.path.isfile(gp) and open(gp).read().strip():
        try:
            guard = json.loads(open(gp).read().strip().splitlines()[-1])
        except ValueError:
            guard = {}
    summary = {"schema": "lj-evidence-summary/1", "package": "WP-05", "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
               "all_run": tally(allr), "quick_run": tally(quick), "groups": groups,
               "disk": {"stage_label": guard.get("label"), "planned_mb": guard.get("planned_mb"), "avail_mb_start": guard.get("avail_mb_start"),
                        "avail_mb_min": guard.get("avail_mb_min"), "avail_mb_end": guard.get("avail_mb_end"), "floor_mb": 400, "hard_floor_mb": 250,
                        "measured_peak_of_generated_files_mb": counts.get("peak_work_mb"), "guard_status": guard.get("status")},
               "unverified": sorted({r["test"] for r in allr if r["status"] == "UNVERIFIED"})}
    env = {"platform": "linux", "python": "%d.%d.%d" % sys.version_info[:3], "ffmpeg": (version_of(["ffmpeg", "-version"]) or "").split(" Copyright")[0],
           "ffprobe": (version_of(["ffprobe", "-version"]) or "").split(" Copyright")[0], "nproc": os.cpu_count(), "machine": platform.machine()}
    for name, obj in (("summary.json", summary), ("environment.json", env)):
        with open(os.path.join(EV, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=2)
            f.write("\n")
    for leftover in (".counts.json",):
        try:
            os.remove(os.path.join(EV, leftover))
        except OSError:
            pass
    print("wrote summary.json and environment.json; all-run:", summary["all_run"], "quick-run:", summary["quick_run"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
