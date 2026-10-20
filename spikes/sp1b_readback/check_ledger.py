#!/usr/bin/env python3
"""check_ledger.py: was each Craft tarball fetched once in the fortnight? (build plan nudge 6; WP-07 and WP-10 ledgers together.) READ-ONLY, standard library only.

USAGE  python3 -I spikes/sp1b_readback/check_ledger.py [--require-all] [--json OUT.json]
         [--wp07 FILE] [--wp10 FILE] [--disk-ledger FILE] [--evidence DIR] [--assets FILE]      (the overrides, and the environment variables LJ_SP1_EVIDENCE, LJ_SCRATCH and LJ_SP1_ASSETS, are for tests)
SOURCES  build/evidence/wp07/download_ledger.jsonl (EffectCraft and FilmCraft, written by WP-07), build/evidence/wp10/download_ledger.jsonl (PhotoCraft, VectorCraft and LightCraft, and the
         FilmCraft exception if WP-07 could not keep its tarball, written by WP-10), the stage envelopes build/evidence/wp10/stage_*.json (did the stage fetch?), and the disk guard's own
         ledger in the scratch folder (a guard line per stage, with its status). A BLOCKED stage fetched nothing and is listed as such.
RULES  each of the five pinned tarballs (PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0, EffectCraft 0.11.1) has at most one fetch, or a later fetch that carries a recorded
       exception (printed with its reason); the FilmCraft 0.8.0 fallback and SoundCraft have none unless the ledger says why; the total stays under the download allowance (ALLOWANCE_MB, 2,560 MB since 2026-10-20); a stage envelope that says
       it fetched must have its ledger line. A pip fetch (a row with "kind": "pip-wheel-set", written by spikes/sp3_blender/ledger_row.py: the bpy wheel and its dependency wheels for SP3)
       counts toward the total like a tarball, and a later fetch of the same set needs a recorded exception too (added Tue 20 Oct 2026, gate w2 nudge 6: pip fetches were outside the ledger).
EXIT CODES (build plan 4.3)  0 the rules hold (a tarball not fetched yet is listed, not a failure)   1 a rule is broken, or --require-all and a tarball was not fetched   2 bad usage / unreadable file
Prints no path, host or user name.
"""
import argparse
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
FIVE = [("photocraft", "v0.10.0"), ("vectorcraft", "v0.13.1"), ("lightcraft", "v0.9.1"), ("filmcraft", "v0.9.0"), ("effectcraft", "v0.11.1")]
ALLOWANCE_MB = 2560        # MiB. 2026-10-20 (week-2 close-out gate): raised from 2048 so that G1's third bpy wheel-set fetch (about 428 MB, Sun 15 Nov) is not stopped by its own guard.
                           # Keep equal to download_allowance_mb in spikes/sp1_craft_cli/config.json and DOWNLOAD_ALLOWANCE_MB in tests/integration/run_checks.py.


def read_jsonl(path):
    rows = []
    if path and os.path.exists(path):
        for ln in open(path, "r", encoding="utf-8"):
            if ln.strip():
                try:
                    rows.append(json.loads(ln))
                except ValueError:
                    raise SystemExit("ERROR: %s is not JSON lines" % os.path.basename(path))
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--require-all", action="store_true")
    ap.add_argument("--json")
    evid_default = os.environ.get("LJ_SP1_EVIDENCE") or os.path.join(REPO, "build", "evidence", "wp10")
    scratch_default = os.environ.get("LJ_SCRATCH") or os.path.join(os.path.dirname(REPO), "build-scratch")
    ap.add_argument("--evidence", default=evid_default)
    ap.add_argument("--wp07", default=os.path.join(os.path.dirname(os.path.abspath(evid_default)), "wp07", "download_ledger.jsonl"))
    ap.add_argument("--wp10", default=os.path.join(evid_default, "download_ledger.jsonl"))
    ap.add_argument("--disk-ledger", default=os.path.join(scratch_default, "disk-ledger.jsonl"))
    ap.add_argument("--assets", default=os.environ.get("LJ_SP1_ASSETS") or os.path.join(REPO, "spikes", "sp1_craft_cli", "release_assets.json"))
    a = ap.parse_args(argv)
    rows = [dict(r, ledger="wp07") for r in read_jsonl(a.wp07)] + [dict(r, ledger="wp10") for r in read_jsonl(a.wp10)]
    guard = read_jsonl(a.disk_ledger)
    stages = {}
    for f in glob.glob(os.path.join(a.evidence, "stage_*.json")):
        try:
            d = json.load(open(f, "r", encoding="utf-8"))
        except (OSError, ValueError):
            continue
        stages[(d.get("detail") or {}).get("stage") or os.path.basename(f)] = d
    assets = {}
    try:
        for p in json.load(open(a.assets, "r", encoding="utf-8"))["pins"]:
            assets[(p["app"], p["tag"])] = p["linux_x86_64_tarball"]
    except (OSError, ValueError, KeyError):
        print("ERROR: cannot read the asset table", file=sys.stderr)
        return 2
    problems, table = [], []
    for app, tag in FIVE:
        tb = assets.get((app, tag), {})
        if not tb:
            table.append({"asset": "%s-%s (not in this asset table)" % (app, tag.lstrip("v")), "bytes": 0, "fetches": 0, "state": "not in the asset table that was given", "exceptions": [], "guard_stage_lines": []})
            continue
        mine = [r for r in rows if r.get("asset") == tb.get("name")]
        exc = [(r.get("fetch"), r.get("ledger"), r.get("stage"), r.get("exception")) for r in mine if r.get("exception")]   # every recorded exception, on whichever fetch carries it
        if len(mine) > 1 and not all(r.get("exception") for r in mine[1:]):
            problems.append("%s was fetched %d times and a later fetch has no recorded exception" % (tb.get("name"), len(mine)))
        sid = "%s-%s" % (app, tag)
        st = stages.get(sid)
        if st and (st.get("detail") or {}).get("fetched") and not mine:
            problems.append("stage %s says it fetched, but no ledger holds the fetch" % sid)
        guard_lines = [g for g in guard if str(g.get("label", "")).startswith(("sp1b-" + sid, "sp1-" + sid))]
        if len(mine) == 0:
            state = "not fetched" + ((" (stage %s: %s)" % (st["status"], (st.get("detail") or {}).get("reason") or "no reason recorded")) if st else " (no stage has run for it)")
            if app == "filmcraft" and not st:
                state += "; WP-07 fetched it once and kept it" if any(r.get("asset") == tb.get("name") for r in rows) else ""
        elif len(mine) == 1:
            state = "fetched once (%s, stage %s, %s)%s" % (mine[0].get("ledger"), mine[0].get("stage"), mine[0].get("date_utc"), ("; exception: " + mine[0]["exception"]) if mine[0].get("exception") else "")
        else:
            state = "fetched %d times; recorded exceptions: %s" % (len(mine), "; ".join("%s stage %s: %s" % (e[1], e[2], e[3]) for e in exc))
        table.append({"asset": tb.get("name"), "bytes": tb.get("bytes"), "fetches": len(mine), "state": state, "exceptions": [{"ledger": e[1], "stage": e[2], "reason": e[3]} for e in exc],
                      "guard_stage_lines": [{"status": g.get("status"), "avail_mb_start": g.get("avail_mb_start"), "avail_mb_min": g.get("avail_mb_min")} for g in guard_lines][-2:]})
        if a.require_all and len(mine) == 0:
            problems.append("%s was not fetched (--require-all)" % tb.get("name"))
    known = {tb.get("name") for tb in (assets.get(k, {}) for k in FIVE)}
    pip_sets = {}
    for r in rows:
        if r.get("kind") == "pip-wheel-set":
            pip_sets.setdefault(r.get("asset"), []).append(r)
    for asset, mine in sorted(pip_sets.items()):
        exc = [(r.get("fetch"), r.get("ledger"), r.get("stage"), r.get("exception")) for r in mine if r.get("exception")]
        if len(mine) > 1 and not all(r.get("exception") for r in mine[1:]):
            problems.append("%s was fetched %d times and a later fetch has no recorded exception" % (asset, len(mine)))
        state = "pip wheel set from PyPI, %d fetch(es) of %s bytes each (%s)" % (len(mine), "{:,}".format(int(mine[0].get("bytes") or 0)), ", ".join(str(r.get("stage")) for r in mine))
        table.append({"asset": asset, "bytes": int(mine[0].get("bytes") or 0), "fetches": len(mine), "state": state, "exceptions": [{"ledger": e[1], "stage": e[2], "reason": e[3]} for e in exc],
                      "guard_stage_lines": []})
    for r in rows:
        if r.get("kind") == "pip-wheel-set":
            continue
        if r.get("asset") not in known:
            note = "the FilmCraft 0.8.0 fallback" if "0.8.0" in str(r.get("asset")) else "an asset outside the five pinned tarballs"
            if "soundcraft" in str(r.get("asset")):
                problems.append("a SoundCraft tarball was fetched (%s), but T5 is cut and SoundCraft is not pinned (D-12)" % r.get("asset"))
            elif "0.8.0" in str(r.get("asset")) and not r.get("exception") and not r.get("stage"):
                problems.append("%s fetched with no stage" % r.get("asset"))
            table.append({"asset": r.get("asset"), "bytes": r.get("bytes"), "fetches": 1, "state": "listed: %s (%s, stage %s)" % (note, r.get("ledger"), r.get("stage")), "exceptions": [], "guard_stage_lines": []})
    total = sum(int(r.get("bytes") or 0) for r in rows)
    if total > ALLOWANCE_MB * 1048576:
        problems.append("total fetched %d bytes is over the %d MB allowance" % (total, ALLOWANCE_MB))
    n_done = sum(1 for t in table[:5] if t["fetches"] >= 1)
    head = "ledger: %d fetches in the two ledgers, %d of the 5 pinned tarballs fetched, %.1f MB of the %d MB allowance; %s" % (
        len(rows), n_done, total / 1048576.0, ALLOWANCE_MB, "each fetched once or with a recorded exception: OK" if not problems else "PROBLEMS: " + "; ".join(problems))
    print(head)
    for t in table:
        print("  %-42s %12s bytes  %s" % (t["asset"], "{:,}".format(t["bytes"] or 0), t["state"]))
    exc_all = [(t["asset"], e) for t in table for e in t["exceptions"]]
    print("exceptions: " + ("none" if not exc_all else "; ".join("%s -> %s (stage %s): %s" % (n, e["ledger"], e["stage"], e["reason"]) for n, e in exc_all)))
    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump({"schema": "lj-ledger-check/1", "ok": not problems, "problems": problems, "tarballs": table, "total_bytes": total, "allowance_mb": ALLOWANCE_MB}, open(a.json, "w"), indent=2, sort_keys=True)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
