#!/usr/bin/env python3
"""make_summary.py: build/evidence/wp07/summary.json and unverified.txt from tests.jsonl (standard library only).
USAGE  python3 -I tests/sp1/make_summary.py [MODE | --from-transcript FILE]     MODE is quick or all (recorded in the summary). Reads tests.jsonl, the stage envelopes and the guard ledger."""
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "spikes", "sp1_craft_cli", "drivers"))
import sp1_lib as L  # noqa: E402


def from_transcript(path):
    """Rebuild tests.jsonl from a saved console transcript of run_tests.sh. Used once, when a later run was cut short by a full disk and had overwritten the
    envelopes of the last good run; every rebuilt record says so in `notes`."""
    import re
    rows = []
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^(PASS|FAIL|UNVERIFIED|BLOCKED|SKIPPED)\s+(\S+)\s{2}(.*)$", ln.rstrip("\n"))
        if not m:
            continue
        rows.append({"schema": "lj-evidence/1", "package": L.PACKAGE, "test": m.group(2), "date_utc": L.today(), "status": m.group(1), "env": L.env_block(), "disk": L.disk_object(),
                     "expected": "see tests/sp1/run_tests.sh", "actual": L.scrub(m.group(3)),
                     "notes": "rebuilt from the saved console transcript %s, because a later run was cut short by a full disk and overwrote the original envelopes" % os.path.basename(path),
                     "unverified_reasons": ["rebuilt from a transcript"] if m.group(1) == "UNVERIFIED" else []})
    with open(os.path.join(L.EVID, "tests.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    return rows


def real_run_state():
    """One sentence about the real CLI results, derived from the driver envelopes (stand-in `_mini` envelopes do not count)."""
    parts = []
    for prefix, label in (("t1_filmcraft", "T1 FilmCraft"), ("t2_filmcraft", "T2 FilmCraft"), ("t1_effectcraft", "T1 EffectCraft"), ("t4_effectcraft", "T4 EffectCraft")):
        found = []
        for p in sorted(glob.glob(os.path.join(L.EVID, prefix + "_*.json"))):
            if p.endswith("_mini.json"):
                continue
            d = L.read_json(p)
            if (d.get("detail") or {}).get("mini"):
                continue
            found.append(d["status"])
        parts.append("%s %s" % (label, "/".join(found) if found else "NOT RUN"))
    return "Real CLI results: " + "; ".join(parts) + ". The harness is also proven against stand-in CLIs, which say nothing about FilmCraft or EffectCraft."


def main(argv):
    if argv and argv[0] == "--from-transcript":
        from_transcript(argv[1])
        argv = ["all"]
    mode = argv[0] if argv else "all"
    src = "tests_quick.jsonl" if mode == "quick" else "tests.jsonl"
    rows = [json.loads(x) for x in open(os.path.join(L.EVID, src)) if x.strip()]
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    stages = []
    for p in sorted(glob.glob(os.path.join(L.EVID, "stage_*.json"))):
        d = L.read_json(p)
        if (d.get("detail") or {}).get("forced_bad_asset"):
            continue  # the deliberate wrong-asset test is not a real stage
        stages.append({"stage": d["test"], "status": d["status"], "reason": d["actual"], "disk": d["disk"]})
    avail = [r["disk"]["avail_mb_min"] for r in rows if r.get("disk") and r["disk"].get("avail_mb_min") is not None]
    summary = {"schema": "lj-wp-summary/1", "package": L.PACKAGE, "date_utc": L.today(), "mode": mode, "counts": counts, "tests": [{"name": r["test"], "status": r["status"]} for r in rows],
               "real_stages": stages, "lowest_avail_mb_seen_by_the_tests": min(avail) if avail else None,
               "real_run_state": real_run_state()}
    L.write_json(os.path.join(L.EVID, "summary.json" if mode != "quick" else "summary_quick.json"), summary)
    if mode == "quick":
        print("summary_quick.json written (%s)" % ", ".join("%s %d" % kv for kv in sorted(counts.items())))
        return 0
    lines = ["WP-07 UNVERIFIED items (generated from tests.jsonl; the standing list is in build/reports/WP-07.md)", ""]
    for r in rows:
        if r["status"] in ("UNVERIFIED", "BLOCKED"):
            lines.append("%s  %s: %s" % (r["status"], r["test"], r["actual"][:300]))
    lines += ["", "Standing: nothing about Windows is verified (PowerShell 5.1 itself, where each zip unpacks, portable.txt handling, what each app writes);",
              "T1 confirmed the describe documents the drivers rely on; the shapes of the timeline, inspect and export results and the FilmCraft keyframe convention for clips that do not start at 0 are assumptions until T2 runs;",
              "the Parallax comp uses solids and shapes, not footage; timings are valid only when contaminated=no."]
    open(os.path.join(L.EVID, "unverified.txt"), "w", encoding="utf-8").write("\n".join(L.scrub(x) for x in lines) + "\n")
    print("summary.json and unverified.txt written (%s)" % ", ".join("%s %d" % kv for kv in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
