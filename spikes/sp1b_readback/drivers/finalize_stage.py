#!/usr/bin/env python3
"""finalize_stage.py: write the evidence envelope of one SP1b stage after it has ended (called by run_sp1b.sh).

USAGE  finalize_stage.py --id ID --app APP --tag TAG --exit RC --planned MB --label LABEL --df-before MB --df-after MB [--reason TEXT] [--fetched 0|1] [--kept-deleted 0|1]
       finalize_stage.py --id ID --note TEXT          (append a note for the final envelope of that stage)
Exit codes of the stage and the status they give: 0 PASS, 1 FAIL (a finding about the app), 2 UNVERIFIED (the harness could not drive the CLI), 3 BLOCKED (the disk guard
refused or tripped, the download was blocked, or the exact need after the download did not fit), 4 FAIL "hash mismatch (stop and report)".
It merges the disk guard's own ledger line (start, minimum and end Avail) into the stage envelope and into the driver envelopes of that app (build plan 4.2: the `disk` object is
required), and records a finding when the Avail drop is more than 25% over the planned figure. Writes only under build/evidence/wp10/. Standard library only.
"""
import argparse
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402

L = B.L
STATUS = {0: "PASS", 1: "FAIL", 2: "UNVERIFIED", 3: "BLOCKED", 4: "FAIL"}


def ledger_line(label):
    path = os.path.join(L.SCRATCH, "disk-ledger.jsonl")
    last = None
    if os.path.exists(path):
        for ln in open(path, "r", encoding="utf-8"):
            try:
                rec = json.loads(ln)
            except ValueError:
                continue
            if rec.get("label") == label:
                last = rec
    return last


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--app")
    ap.add_argument("--tag", default="")
    ap.add_argument("--exit", type=int, default=None)
    ap.add_argument("--planned", type=int, default=0)
    ap.add_argument("--label", default="")
    ap.add_argument("--df-before", type=int, default=None)
    ap.add_argument("--df-after", type=int, default=None)
    ap.add_argument("--reason", default="")
    ap.add_argument("--fetched", type=int, default=0)
    ap.add_argument("--kept-deleted", type=int, default=0)
    ap.add_argument("--kept-applies", type=int, default=0, help="1 for the FilmCraft stage, whose source is the tarball WP-07 kept")
    ap.add_argument("--note")
    a = ap.parse_args(argv)
    notes_path = os.path.join(L.EVID, ".stage_%s.notes" % a.id)
    if a.note:
        os.makedirs(L.EVID, exist_ok=True)
        with open(notes_path, "a", encoding="utf-8") as f:
            f.write(L.scrub(a.note) + "\n")
        return 0
    notes = []
    if os.path.exists(notes_path):
        notes = [x.rstrip("\n") for x in open(notes_path, "r", encoding="utf-8")]
        os.remove(notes_path)
    led = ledger_line(a.label) if a.label else None
    rc = a.exit if a.exit is not None else 3
    status = STATUS.get(rc, "FAIL")
    reason = a.reason or {4: "hash mismatch (stop and report)"}.get(rc, "")
    disk = {"avail_mb_start": (led or {}).get("avail_mb_start", a.df_before), "planned_write_mb": a.planned, "avail_mb_min": (led or {}).get("avail_mb_min"),
            "avail_mb_end": (led or {}).get("avail_mb_end", a.df_after), "floor_mb": 400, "hard_floor_mb": 250}
    sampled = None
    minf = os.path.join(L.EVID, ".stage_%s.min" % a.id)
    if os.path.exists(minf):
        try:
            sampled = int(open(minf).read().strip())
        except ValueError:
            sampled = None
        os.remove(minf)
    if isinstance(sampled, int) and isinstance(disk["avail_mb_min"], int):
        disk["avail_mb_min"] = min(disk["avail_mb_min"], sampled)   # the 0.25 s sampler can see a peak the guard's 5 s poll misses
    elif isinstance(sampled, int):
        disk["avail_mb_min"] = sampled
    vals = [v for v in (disk["avail_mb_start"], disk["avail_mb_end"], disk["avail_mb_min"]) if isinstance(v, int)]
    if disk["avail_mb_min"] is None and vals:
        disk["avail_mb_min"] = min(vals)
    drop = (disk["avail_mb_start"] - disk["avail_mb_min"]) if isinstance(disk["avail_mb_start"], int) and isinstance(disk["avail_mb_min"], int) else None
    over = bool(drop is not None and a.planned and drop > a.planned * 1.25)
    if over:
        notes.append("FINDING: the Avail drop of %d MB is more than 25%% over the planned %d MB (other writers share the volume, so this is an upper bound for this stage's own peak)" % (drop, a.planned))
    if status == "PASS" and not (a.planned == 0 or (isinstance(disk["avail_mb_start"], int) and disk["avail_mb_start"] - a.planned >= 400)):
        notes.append("FINDING: the stage started with Avail minus planned below the 400 MB floor")
    # the driver envelopes of this app get the real disk figures
    patched = []
    if a.app:
        for f in glob.glob(os.path.join(L.EVID, "*_%s_%s.json" % (a.app, a.tag))) + glob.glob(os.path.join(L.EVID, "t3_%s_%s.json" % (a.app, a.tag))):
            try:
                rec = L.read_json(f)
            except (OSError, ValueError):
                continue
            if rec.get("package") == "WP-10" and "stage_" not in os.path.basename(f):
                rec["disk"] = dict(disk)
                L.write_json(f, rec)
                patched.append(os.path.basename(f))
    detail = {"stage": a.id, "app": a.app, "tag": a.tag, "exit_code": rc, "reason": reason, "fetched": bool(a.fetched), "kept_tarball_deleted": (bool(a.kept_deleted) if a.kept_applies else None),
              "avail_drop_mb": drop, "avail_min_sampled_every_0_25_s_mb": sampled, "avail_drop_over_plan_by_more_than_25_percent": over, "avail_drop_includes_other_writers": True,
              "df_before_mb": a.df_before, "df_after_mb": a.df_after, "df_delta_mb": (a.df_after - a.df_before) if (a.df_before is not None and a.df_after is not None) else None,
              "guard_ledger": {k: led.get(k) for k in ("status", "exit", "lock_wait_s")} if led else None, "driver_envelopes_patched": sorted(patched), "label": B.LABEL}
    exp = "the stage ran inside lj_with_disk, ended with exit 0 and left vendor/craft-sp1b empty"
    B.envelope("stage_" + a.id, status, exp, ("exit %s%s" % (rc, (": " + reason) if reason else "")), notes=" ".join(notes), disk=disk, extra=detail)
    print("stage %s: %s%s" % (a.id, status, (" (%s)" % reason) if reason else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
