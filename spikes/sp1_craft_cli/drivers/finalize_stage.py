#!/usr/bin/env python3
"""finalize_stage.py: write the evidence envelope of one SP1 stage after it has ended (called by run_sp1.sh).

USAGE  finalize_stage.py --id ID --profile P --planned MB --exit RC --df-before MB --df-after MB --label LABEL --vendor DIR
       finalize_stage.py --id ID --status BLOCKED --reason TEXT --profile none     (a stage that never started)
       finalize_stage.py --id ID --note TEXT                                        (append a note for the final envelope)
Exit 4 is run_sp1.sh's internal code for "the tarball was rejected by its SHA-256": status FAIL, reason "hash mismatch (stop and report)", exit_code 1 and
hash_rejected true in the detail. A stage run with FORCE_BAD_ASSET=1 (the deliberate wrong-asset test) is written to stage_<id>_forced.json with
forced_bad_asset true in the detail; verdict.py and make_summary.py skip such envelopes, as verdict.py skips a forced blocked_proof.json.
It merges the disk guard's own ledger line (start, minimum and end Avail) into the stage envelope and into every driver envelope of
that stage (build plan 4.2: the `disk` object is required), checks that vendor/craft holds nothing but _keep/, and flags a stage whose
Avail dropped by more than 25% over its planned figure (build plan 4.9: a finding, not a failure).
Writes only under build/evidence/wp07/. Reads the guard ledger in the scratch folder. Standard library only.
"""
import argparse
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402


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
    ap.add_argument("--status")
    ap.add_argument("--reason", default="")
    ap.add_argument("--profile", default="none")
    ap.add_argument("--planned", type=int, default=0)
    ap.add_argument("--exit", type=int, default=None)
    ap.add_argument("--df-before", type=int, default=None)
    ap.add_argument("--df-after", type=int, default=None)
    ap.add_argument("--label", default="")
    ap.add_argument("--vendor", default=os.path.join(L.REPO, "vendor", "craft"))
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
    forced = os.environ.get("FORCE_BAD_ASSET") == "1"
    hash_rejected = a.exit == 4
    if hash_rejected:
        a.exit = 1  # the internal code 4 is shown as the exit code run_sp1.sh gives its caller
        a.reason = a.reason or "hash mismatch (stop and report)"
    if a.status:
        status = a.status
    else:
        status = {0: "PASS", 1: "FAIL", 2: "UNVERIFIED", 3: "BLOCKED"}.get(a.exit, "FAIL")  # 2: the harness could not drive the CLI, not a verdict on it
    disk = None
    detail = {"stage": a.id, "profile": a.profile, "exit_code": a.exit, "guard_ledger": None}
    if hash_rejected:
        detail["hash_rejected"] = True
    if forced:
        detail["forced_bad_asset"] = True  # a deliberate wrong-asset test run: not a real result for this stage
    if led:
        disk = {"avail_mb_start": led["avail_mb_start"], "planned_write_mb": led["planned_mb"], "avail_mb_min": led["avail_mb_min"],
                "avail_mb_end": led["avail_mb_end"], "floor_mb": led["floor_mb"], "hard_floor_mb": led["hard_floor_mb"]}
        detail["guard_ledger"] = {"status": led["status"], "exit": led["exit"], "lock_wait_s": led["lock_wait_s"]}
        if led["status"] == "refused":
            status = "BLOCKED"
            reason = "the disk guard refused the stage: Avail %s MB minus planned %s MB is below the %s MB floor" % (led["avail_mb_start"], led["planned_mb"], led["floor_mb"])
            a.reason = a.reason or reason
        elif led["status"] == "floor":
            status = "BLOCKED"
            a.reason = a.reason or "DISK-FLOOR: Avail fell below the hard floor while the stage ran; its process group was stopped"
        drop = (led["avail_mb_start"] or 0) - (led["avail_mb_min"] or 0)
        detail["avail_drop_mb"] = drop
        detail["avail_drop_includes_other_writers"] = True
        if led["planned_mb"] and drop > 1.25 * led["planned_mb"]:
            detail["finding"] = "Avail dropped %d MB, more than 25%% over the planned %d MB (other jobs write to this volume too)" % (drop, led["planned_mb"])
    else:
        disk = L.disk_object(planned_mb=a.planned)
    if a.df_before is not None and a.df_after is not None:
        kept = []
        keepdir = os.path.join(a.vendor, "_keep")
        if os.path.isdir(keepdir):
            kept = sorted(os.listdir(keepdir))
        kept_mb = round(sum(os.path.getsize(os.path.join(keepdir, k)) for k in kept) / 1048576.0, 1) if kept else 0
        delta = a.df_before - a.df_after
        detail["df_before_mb"], detail["df_after_mb"] = a.df_before, a.df_after
        detail["df_delta_mb"] = delta
        detail["kept_tarballs"] = kept
        detail["kept_mb"] = kept_mb
        detail["df_back_within_10mb_of_start_plus_kept"] = abs(delta - kept_mb) <= 10
        detail["df_note"] = "the volume is shared; a concurrent writer moves this figure, the vendor listing below is the exact one"
    left = sorted(x for x in os.listdir(a.vendor) if x != "_keep") if os.path.isdir(a.vendor) else []
    detail["vendor_craft_other_than_keep"] = left
    if left and status == "PASS":
        status = "FAIL"
        notes.append("vendor/craft still holds: " + ", ".join(left))
    if notes:
        detail["notes"] = notes
    env_name = "stage_" + a.id + ("_forced" if forced else "")
    L.envelope(env_name, status, "the stage ran inside lj_with_disk, ended with exit 0, and left vendor/craft with nothing but _keep/",
               ("exit %s" % a.exit if a.exit is not None else "not started") + ((": " + a.reason) if a.reason else ""), notes="; ".join(notes), disk=disk, extra=detail)
    # put the guard's final disk figures into every driver envelope of this stage
    if led and a.label:
        for p in glob.glob(os.path.join(L.EVID, "*.json")):
            try:
                d = json.load(open(p, "r", encoding="utf-8"))
            except ValueError:
                continue
            if isinstance(d, dict) and d.get("schema") == "lj-evidence/1" and d.get("stage") == a.label and os.path.basename(p) != env_name + ".json":
                d["disk"] = disk
                L.write_json(p, d)
    print("stage %s: %s%s" % (a.id, status, (" (" + a.reason + ")") if a.reason else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
