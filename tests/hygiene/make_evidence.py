#!/usr/bin/env python3
"""make_evidence.py: turn the RESULT lines of a hygiene test run into evidence envelopes (build plan 4.2).

  python3 -I tests/hygiene/make_evidence.py LOGFILE OUTDIR --mode quick|all --avail-start MB --avail-min MB
Reads    LOGFILE    lines "GROUP name" and "RESULT PASS|FAIL test :: detail" written by run_tests.sh
Writes   OUTDIR/tests.jsonl   one lj-evidence/1 envelope per test (disk figures in every one)
         OUTDIR/summary.json  counts per group and overall
         OUTDIR/unverified.txt  what could only be checked in part, and why
Standard library only. Records no host, user or absolute path: the environment block holds platform,
processor count and tool versions only.
"""
import argparse
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


def avail_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", "/"], capture_output=True, text=True, env=dict(os.environ, LC_ALL="C")).stdout.splitlines()[1].split()[3]
        return int(out.rstrip("M"))
    except Exception:
        return None


def tool_version(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip().splitlines()
        return out[0] if out else None
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
    env = {"platform": platform.system().lower(), "nproc": os.cpu_count(), "python": platform.python_version(),
           "bash": (tool_version(["bash", "--version"]) or "")[:40].replace("GNU bash, version ", "").split(" ")[0],
           "pwsh": None}
    pw = shutil.which("pwsh")
    if not pw:
        cand = Path(__file__).resolve().parents[3] / "build-scratch" / "pwsh" / "pwsh"
        pw = str(cand) if cand.exists() else None
    if pw:
        v = tool_version([pw, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"])
        env["pwsh"] = v
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
        env_ = {"schema": "lj-evidence/1", "package": "WP-03", "test": "%s.%s" % (group, name), "date_utc": date, "status": status, "env": env,
                "disk": {"avail_mb_start": start, "planned_write_mb": 0, "avail_mb_min": mn, "avail_mb_end": end, "floor_mb": 400, "hard_floor_mb": 250},
                "expected": "pass", "actual": detail[:300], "notes": "", "unverified_reasons": []}
        if status == "UNVERIFIED":
            env_["unverified_reasons"] = [detail[:300]]
        envelopes.append(env_)
        g = groups.setdefault(group, {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0})
        g[status] += 1
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "tests.jsonl", "w", encoding="utf-8", newline="\n") as fh:
        for e in envelopes:
            fh.write(json.dumps(e, sort_keys=True) + "\n")
    total = {k: sum(g[k] for g in groups.values()) for k in ("PASS", "FAIL", "UNVERIFIED", "SKIPPED")}
    (out / "summary.json").write_text(json.dumps({"schema": "lj-evidence-summary/1", "package": "WP-03", "mode": a.mode, "date_utc": date, "env": env, "groups": groups, "total": total,
                                                  "disk": {"avail_mb_start": start, "avail_mb_min": mn, "avail_mb_end": end}}, indent=1) + "\n", encoding="utf-8")
    (out / "unverified.txt").write_text(
        "WP-03 behaviour that could not be verified here (all of it needs a Windows PC):\n"
        "- Windows PowerShell 5.1 reading scripts/redaction_patterns.json (win/step0_pc_tests.ps1 was run on PowerShell 7 only; the regex dialect is the common subset of Python re and .NET, but .NET Framework on 5.1 was not run).\n"
        "- scripts/public_lint.py, scripts/stale_check.py and tests on Windows (py -3 -I): only run on Linux here; paths use forward slashes internally and pathlib, but Windows was not exercised.\n"
        "- win/kit2/run_checks_pc.ps1 (WP-09) had not landed when this ran: its -PatternSelfTest consumer is SKIPPED: not landed.\n"
        "- the disk guard is Linux only (flock, df, /proc/loadavg); on the maker's PC it is not used.\n", encoding="utf-8")
    print("evidence: %d envelopes, %s" % (len(envelopes), json.dumps(total)))
    return 0 if total["FAIL"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
