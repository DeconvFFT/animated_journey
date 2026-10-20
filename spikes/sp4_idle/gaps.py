#!/usr/bin/env python3
"""gaps.py: read an SP4 job log and say whether the container was kept awake, paused or killed while the job ran. Standard library only. READ-ONLY.

USAGE  python3 -I spikes/sp4_idle/gaps.py LOG [--gap-limit 30] [--interval N] [--now EPOCH] [--json OUT.json]
LOG    the file spikes/sp4_idle/job.sh wrote: '# start epoch=E interval=I seconds=S ...', then 'E SEQ' lines, then '# end epoch=E reason=...'.
OUTPUT the number of ticks, the interval and the expected number, the MAXIMUM GAP between two lines, every gap over --gap-limit seconds (default 30) with where it fell, and a VERDICT:
         kept awake  the job reached its end line (or the expected number of ticks) and no gap is over the limit: nothing stopped the container while the job ran
         paused      the job reached its end but at least one gap is over the limit: the container (or the job) was frozen and thawed. The longest gap is the length of the freeze.
         killed      the job never wrote its end line and stopped short of its expected length (and is not still running): it was ended from outside (SIGKILL, container stop or reset)
         running     the log is still being written (its last line is newer than 2 intervals + 5 s before --now, default the clock) and has no end line yet; judge it again later
         unreadable  no start line, a line that is not 'EPOCH SEQ', or epochs that go backwards
       A log whose job was ended with TERM or INT (end line reason=term) is "killed" too: somebody stopped it, it did not finish.
EXIT CODES (build plan 4.3)  0 kept awake   1 paused or killed (a finding: the container did not stay awake)   2 bad usage, unreadable file or log   3 running (judge later)
Prints no path, host or user name; it reads only the file you name.
"""
import argparse
import json
import re
import sys
import time

sys.dont_write_bytecode = True


def parse(path):
    start = end = None
    ticks = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for n, ln in enumerate(f, 1):
            ln = ln.strip()
            if not ln:
                continue
            if ln.startswith("# start"):
                start = {k: v for k, v in re.findall(r"(\w+)=(\S+)", ln)}
            elif ln.startswith("# end"):
                end = {k: v for k, v in re.findall(r"(\w+)=(\S+)", ln)}
            elif ln.startswith("#"):
                continue
            else:
                m = re.fullmatch(r"(\d{9,11})\s+(\d+)", ln)
                if not m:
                    raise ValueError("line %d is not 'EPOCH SEQ'" % n)
                ticks.append((int(m.group(1)), int(m.group(2))))
    return start, end, ticks


def analyse(path, gap_limit=30, interval=None, now=None):
    start, end, ticks = parse(path)
    if start is None:
        raise ValueError("no '# start' line")
    for a, b in zip(ticks, ticks[1:]):
        if b[0] < a[0]:
            raise ValueError("epochs go backwards at tick %d" % b[1])
    interval = interval or int(start.get("interval", "0")) or 10
    seconds = int(start.get("seconds", "0") or 0)
    expected = max(seconds // interval, 1) if seconds else None
    t0 = int(start.get("epoch", ticks[0][0] if ticks else 0))
    points = [t0] + [t for t, _ in ticks]
    if end and end.get("epoch", "").isdigit():
        points.append(int(end["epoch"]))
    gaps = [(points[i + 1] - points[i], points[i], i) for i in range(len(points) - 1)]
    max_gap = max((g[0] for g in gaps), default=0)
    over = [{"seconds": g[0], "after_tick": g[2], "at_offset_s": g[1] - t0} for g in gaps if g[0] > gap_limit]
    now = now if now is not None else int(time.time())
    last = points[-1]
    complete = bool(end and end.get("reason") == "done") or (expected is not None and len(ticks) >= expected)
    if end and end.get("reason") not in (None, "done"):
        verdict = "killed"
    elif complete:
        verdict = "paused" if over else "kept awake"
    elif now - last <= 2 * interval + 5:
        verdict = "running"
    else:
        verdict = "killed"
    return {"ticks": len(ticks), "expected_ticks": expected, "interval_s": interval, "seconds_planned": seconds, "max_gap_s": max_gap, "gap_limit_s": gap_limit,
            "gaps_over_limit": over, "ended_with_end_line": bool(end), "end_reason": (end or {}).get("reason"), "df_avail_mb_start": start.get("df_avail_mb"),
            "df_avail_mb_end": (end or {}).get("df_avail_mb"), "span_s": last - t0, "verdict": verdict}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("log")
    ap.add_argument("--gap-limit", type=int, default=30)
    ap.add_argument("--interval", type=int)
    ap.add_argument("--now", type=int)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    try:
        r = analyse(a.log, a.gap_limit, a.interval, a.now)
    except (OSError, ValueError) as e:
        print("gaps.py: cannot read the log: %s" % e, file=sys.stderr)
        return 2
    print("ticks: %d of %s expected, interval %d s, span %d s" % (r["ticks"], r["expected_ticks"], r["interval_s"], r["span_s"]))
    print("maximum gap: %d s (limit for listing: %d s)" % (r["max_gap_s"], r["gap_limit_s"]))
    if r["gaps_over_limit"]:
        for g in r["gaps_over_limit"]:
            print("  gap of %d s after tick %d (%d s into the run)" % (g["seconds"], g["after_tick"], g["at_offset_s"]))
    else:
        print("gaps over %d s: none" % r["gap_limit_s"])
    print("end line: %s%s; df Avail at start %s MB, at end %s MB" % ("yes" if r["ended_with_end_line"] else "NO", (" (reason %s)" % r["end_reason"]) if r["end_reason"] else "", r["df_avail_mb_start"], r["df_avail_mb_end"]))
    print("VERDICT: %s" % r["verdict"])
    if a.json:
        with open(a.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(dict(r, schema="lj-sp4-gaps/1"), f, indent=2, sort_keys=True)
    return {"kept awake": 0, "paused": 1, "killed": 1, "running": 3}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
