#!/usr/bin/env python3
"""make_evidence.py: turn the RESULT lines of a WP-11a test run into evidence envelopes (build plan 4.2).

  python3 -I tests/runner/make_evidence.py LOGFILE OUTDIR --mode quick|all --avail-start MB --avail-min MB
Reads    LOGFILE   lines "GROUP name" and "RESULT PASS|FAIL|UNVERIFIED|SKIPPED test :: detail" written by run_tests.sh
Writes   OUTDIR/tests_<mode>.jsonl   one lj-evidence/1 envelope per test (disk figures in every one)
         OUTDIR/summary_<mode>.json  counts per group and overall (lj-evidence-summary/1); also summary.json for --all
         OUTDIR/unverified.txt       what could only be checked in part, and why
Standard library only. Records no host, user or absolute path: the environment block holds platform, processor
count and tool versions only.
"""
import argparse
import datetime
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

UNVERIFIED_NOTES = [
    "Both scripts were run on Linux only. Nothing here says anything about Windows: neither script is meant for Windows, and no Windows behaviour is claimed.",
    "public_lint.py --text does not exist yet (WP-03). The runner's call to it (text on stdin, exit 0 = clean) is an assumed contract, exercised only against tests/runner/lint_stub.py.",
    "The 60 s / 900 s per-area limits, the 300 s quick budget and the 16 MB output cap are plan numbers or defaults chosen here; the real areas' run times were observed once, on a shared and nearly full disk.",
    "Deleting with cleanup_scratch.sh --yes was exercised on fake trees only; it was never run with --yes on the real scratch folder, vendor/ or renders/.",
    "A real full disk was met once by accident while the runner ran (another job filled the volume): the runner then stopped with a misleading exit 2. That was corrected to exit 3 (environment), "
    "and the corrected path is tested with a scanner stub that raises OSError, not on a really full disk.",
    "Process-group handling (setsid, kill of the whole group, zombie-aware checks) was tested on Linux in this container only.",
]


def avail_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", "/"], capture_output=True, text=True, env=dict(os.environ, LC_ALL="C")).stdout.splitlines()[1].split()[3]
        return int(out.rstrip("M"))
    except Exception:
        return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("outdir")
    ap.add_argument("--mode", default="all")
    ap.add_argument("--avail-start", type=int, default=None)
    ap.add_argument("--avail-min", type=int, default=None)
    a = ap.parse_args(argv)
    end = avail_mb()
    start = a.avail_start if a.avail_start is not None else end
    mn = a.avail_min if a.avail_min is not None else min(x for x in (start, end) if x is not None)
    env = {"platform": platform.system().lower(), "nproc": os.cpu_count(), "python": platform.python_version(), "bash": os.environ.get("BASH_VERSION", "").split("(")[0] or None}
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    group = "ungrouped"
    envelopes, groups = [], {}
    for line in Path(a.log).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("GROUP "):
            group = line[6:].strip()
            continue
        m = re.match(r"RESULT (PASS|FAIL|UNVERIFIED|SKIPPED) (\S+) :: ?(.*)$", line)
        if not m:
            continue
        status, name, detail = m.groups()
        e = {"schema": "lj-evidence/1", "package": "WP-11a", "test": "%s.%s" % (group, name), "date_utc": date, "status": status, "env": env,
             "disk": {"avail_mb_start": start, "planned_write_mb": 0, "avail_mb_min": mn, "avail_mb_end": end, "floor_mb": 400, "hard_floor_mb": 250},
             "expected": "pass", "actual": detail[:300], "notes": "", "unverified_reasons": []}
        if status == "UNVERIFIED":
            e["unverified_reasons"] = [detail[:300]]
        envelopes.append(e)
        g = groups.setdefault(group, {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0})
        g[status] += 1
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / ("tests_%s.jsonl" % a.mode), "w", encoding="utf-8") as f:
        for e in envelopes:
            f.write(json.dumps(e, sort_keys=True) + "\n")
    tot = {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0}
    for g in groups.values():
        for k, v in g.items():
            tot[k] += v
    summary = {"schema": "lj-evidence-summary/1", "package": "WP-11a", "mode": a.mode, "date_utc": date, "env": env, "groups": groups, "counts": tot}
    # summary_<mode>.json always; summary.json (the one INDEX.md links) only from --all, the full result
    for name in (["summary_%s.json" % a.mode] + (["summary.json"] if a.mode == "all" else [])):
        with open(out / name, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=1)
            f.write("\n")
    with open(out / "unverified.txt", "w", encoding="utf-8") as f:
        f.write("WP-11a: what is UNVERIFIED or only partly checked, and why\n\n")
        for n in UNVERIFIED_NOTES:
            f.write("- " + n + "\n")
    print("envelopes written:", len(envelopes), tot)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
