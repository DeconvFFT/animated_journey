#!/usr/bin/env python3
"""stage_budget.py: the disk arithmetic of the SP1b stages (called by run_sp1b.sh). Standard library only; writes nothing.

USAGE  python3 -I stage_budget.py list [--no-exit-code]     the stage plan with sizes, df, and a refusal line (exit 3) for any stage whose Avail minus planned is under 400 MB
       python3 -I stage_budget.py budget APP                JSON: planned_mb and its parts for one stage (reads the kept tarball's listing for FilmCraft)
       python3 -I stage_budget.py plan LISTING APP          JSON: the one CLI member to extract from a `tar -tvzf` listing, its size, and the exact need
       python3 -I stage_budget.py after-download LISTING APP AVAIL_MB    JSON: does the exact need (CLI + outputs) still leave the floor? (the check made after the download)
WHY. Everything is one nearly full volume other jobs write to. The plan's table (PhotoCraft 300, VectorCraft 450, LightCraft 350, FilmCraft 300 MB) is a
planning estimate; the real figure is computed here: tarball + CLI member + outputs. The tarball size comes from release_assets.json, the CLI size from the tarball
listing (exact for FilmCraft, whose tarball is already on disk; assumed 1.15 x the tarball for the other three until their listing exists).
ENVIRONMENT  LJ_DF_CMD (a fake df), LJ_SP1_ASSETS (the asset table), LJ_SP1B_KEEP_DIR (where WP-07 kept the FilmCraft tarball; default vendor/craft/_keep).
EXIT CODES  0 ok   2 bad usage   3 `list`: a stage is refused (Avail minus planned below the floor) or df cannot be read
"""
import json
import math
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402

L = B.L
CFG = os.path.join(B.SP1B, "config.json")
MIB = 1048576.0


def cfg():
    return L.read_json(CFG)


def mb_up(n):
    return int(math.ceil(n / MIB))


def keep_dir():
    return os.environ.get("LJ_SP1B_KEEP_DIR") or os.path.join(B.REPO, "vendor", "craft", "_keep")


def tarball(app, tag):
    pin = L.find_pin(L.load_assets(), app, tag)
    if not pin:
        raise SystemExit("ERROR: %s %s is not a pin of the asset table" % (app, tag))
    return pin["linux_x86_64_tarball"]


def parse_listing(text):
    members = []
    for ln in text.splitlines():
        m = re.match(r"^([-dlhpcbs])\S*\s+\S+\s+(\d+)\s+\S+\s+\S+\s+(.*?)(?: -> .*)?$", ln.rstrip())
        if m:
            members.append({"type": m.group(1), "bytes": int(m.group(2)), "name": m.group(3)})
    return members


def cli_member(members, app):
    c = [m for m in members if m["type"] == "-" and os.path.basename(m["name"]) == app + "-cli"]
    return c[0] if c else None


def kept_path(app, tag):
    return os.path.join(keep_dir(), tarball(app, tag)["name"])


def kept_cli_bytes(path):
    """The exact size of the CLI member of the kept tarball, from a listing (tar -tvzf writes nothing)."""
    p = subprocess.run(["tar", "-tvzf", path], capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        return None
    m = cli_member(parse_listing(p.stdout), "filmcraft")
    return m["bytes"] if m else None


def budget(stage, c):
    app, tag = stage["app"], stage["tag"]
    tb = tarball(app, tag)
    out = c["budget"]["outputs_mb"]
    if stage["source"] == "kept":
        kp = kept_path(app, tag)
        if os.path.exists(kp):
            cb = kept_cli_bytes(kp)
            if cb:
                cli_mb = mb_up(cb)
                return {"planned_mb": cli_mb + out, "tarball_mb_downloaded": 0, "tarball_on_disk_mb": mb_up(os.path.getsize(kp)), "cli_mb": cli_mb, "cli_basis": "exact, from `tar -tvzf` of the kept tarball", "outputs_mb": out,
                        "fetch": False}
        # the kept tarball is missing: one re-fetch (a recorded ledger exception), so it is planned like the others
    tb_mb = mb_up(tb["bytes"])
    cli_mb = mb_up(tb["bytes"] * c["budget"]["cli_over_tarball_assumed"])
    return {"planned_mb": tb_mb + cli_mb + out, "tarball_mb_downloaded": tb_mb, "cli_mb": cli_mb, "cli_basis": "assumed %.2f x the tarball (FilmCraft measured %.2f)" % (c["budget"]["cli_over_tarball_assumed"], c["budget"]["cli_over_tarball_measured"]["filmcraft 0.9.0"]),
            "outputs_mb": out, "fetch": True, "refetch_exception": stage["source"] == "kept"}


def cmd_list(no_exit):
    c = cfg()
    floor = c["disk"]["floor_mb"]
    avail = L.df_avail_mb()
    print("run_sp1b.sh --list    (build plan WP-10; nothing is downloaded or written)")
    if avail is None:
        print("cannot read free disk space (df gave no number)")
        return 3
    print("")
    print("Stages, in this order (the FilmCraft stage runs first because it deletes the kept tarball and so gives the next three more room):")
    refused = []
    a = avail
    for st in c["stages"]:
        tb = tarball(st["app"], st["tag"])
        b = budget(st, c)
        envp = os.path.join(L.EVID, "stage_%s.json" % st["id"])
        prev, dk = "", {}
        if os.path.exists(envp):
            try:
                rec = L.read_json(envp)
                prev, dk = rec.get("status", ""), rec.get("disk") or {}
            except (OSError, ValueError):
                prev = ""
        if prev in ("PASS", "FAIL"):
            # a stage that already ran is not run again by --all (its tarball is gone): shown with its size and what it used, not counted against the disk
            print("  %d. %-12s %-8s tests: %-16s already run: %s; tarball %s bytes (%d MB)" %
                  (st["order"], st["app"], st["tag"], "+".join(st["tests"]).upper().replace("READBACK", "read-backs"), prev, "{:,}".format(tb["bytes"]), mb_up(tb["bytes"])))
            print("       planned %s MB at the time; Avail start %s, minimum %s, end %s MB (build/evidence/wp10/stage_%s.json). --all skips it; --again would re-fetch with a recorded ledger exception" %
                  (dk.get("planned_write_mb"), dk.get("avail_mb_start"), dk.get("avail_mb_min"), dk.get("avail_mb_end"), st["id"]))
            continue
        left = a - b["planned_mb"]
        verdict = "ok" if left >= floor else "REFUSED"
        src = "kept tarball in vendor/craft/_keep (%d MB on disk, no download)" % b.get("tarball_on_disk_mb", 0) if not b["fetch"] else "download %s bytes (%d MB)" % ("{:,}".format(tb["bytes"]), b["tarball_mb_downloaded"])
        print("  %d. %-12s %-8s tests: %-16s %s" % (st["order"], st["app"], st["tag"], "+".join(st["tests"]).upper().replace("READBACK", "read-backs"), src))
        print("       planned %d MB = %s%d MB CLI (%s) + %d MB outputs;  Avail at this stage %d MB leaves %d MB: %s" %
              (b["planned_mb"], ("%d MB tarball + " % b["tarball_mb_downloaded"]) if b["fetch"] else "", b["cli_mb"], b["cli_basis"], b["outputs_mb"], a, left, verdict))
        if left < floor:
            refused.append("REFUSED: Avail %d MB minus planned %d MB leaves %d MB, below the %d MB floor (%s)." % (a, b["planned_mb"], left, floor, st["id"]))
        if not b["fetch"] or st["source"] == "kept":
            a += b.get("tarball_on_disk_mb", 0)  # the kept tarball is deleted when this stage ends, so the next stage starts with more room
    print("")
    print("Plan table of build plan 4.9 for comparison (estimates, MB): " + ", ".join("%s %d" % (k, v) for k, v in c["plan_table_mb"].items()) +
          ". The figures above are computed from the tarball sizes in release_assets.json and, for FilmCraft, the tarball listing.")
    print("Disk: df says Avail %d MB now. Floor %d MB (Avail minus planned must stay at or above it), hard floor %d MB. Each stage re-reads df live; the guard is the authority." % (avail, floor, c["disk"]["hard_floor_mb"]))
    print("Not fetched: SoundCraft (T5 cut, D-12). Fetched by WP-07: EffectCraft. Each tarball once; the ledger check is spikes/sp1b_readback/check_ledger.py.")
    if refused:
        print("")
        for r in refused:
            print(r)
        print("Remedy: " + c["remedy"] + ".")
        return 0 if no_exit else 3
    print("")
    print("OK: every stage that has not run yet fits at today's Avail. Start them with: bash spikes/sp1b_readback/run_sp1b.sh --all")
    return 0


def cmd_budget(app):
    c = cfg()
    st = next((s for s in c["stages"] if s["app"] == app), None)
    if not st:
        print("ERROR: unknown app %s" % app, file=sys.stderr)
        return 2
    print(json.dumps(budget(st, c)))
    return 0


def cmd_plan(listing, app):
    members = parse_listing(open(listing, "r", encoding="utf-8", errors="replace").read())
    m = cli_member(members, app)
    if not m:
        print(json.dumps({"error": "no member named %s-cli in the tarball" % app, "members": len(members)}))
        return 1
    print(json.dumps({"app": app, "members_total": len(members), "files_total": sum(1 for x in members if x["type"] == "-"), "all_mb": round(sum(x["bytes"] for x in members if x["type"] == "-") / MIB, 1),
                      "cli_member": m["name"], "cli_bytes": m["bytes"], "cli_mb": round(m["bytes"] / MIB, 1), "chosen": [m["name"]], "chosen_mb": round(m["bytes"] / MIB, 1)}))
    return 0


def cmd_after(listing, app, avail):
    c = cfg()
    members = parse_listing(open(listing, "r", encoding="utf-8", errors="replace").read())
    m = cli_member(members, app)
    if not m:
        print(json.dumps({"ok": False, "reason": "no member named %s-cli" % app}))
        return 1
    need = mb_up(m["bytes"]) + c["budget"]["outputs_mb"]
    left = int(avail) - need
    print(json.dumps({"ok": left >= c["disk"]["floor_mb"], "need_mb": need, "avail_mb": int(avail), "leaves_mb": left, "floor_mb": c["disk"]["floor_mb"]}))
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "list":
        return cmd_list("--no-exit-code" in argv)
    if argv[0] == "budget" and len(argv) == 2:
        return cmd_budget(argv[1])
    if argv[0] == "plan" and len(argv) == 3:
        return cmd_plan(argv[1], argv[2])
    if argv[0] == "after-download" and len(argv) == 4:
        return cmd_after(argv[1], argv[2], argv[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
