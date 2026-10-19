#!/usr/bin/env python3
"""asset_tool.py: the download, hash and extraction-plan steps of one SP1 stage (called by run_sp1.sh).

USAGE  python3 -I spikes/sp1_craft_cli/drivers/asset_tool.py SUBCOMMAND ...
  head    APP TAG                      HEAD the Linux tarball; print JSON (status, bytes); exit 3 and write blocked_proof.json if it fails
  get     APP TAG --dest FILE          download the tarball (curl -f -L) into FILE; exit 3 and write blocked_proof.json on any failure
  verify  FILE APP TAG                 SHA-256 of FILE against release_assets.json (and the independent value of r8_hashes.json when there
                                       is one); prints OK or REJECTED; exit 0 / 1. Run BEFORE any extraction.
  plan    LISTING APP PROFILE          read a `tar -tvzf` listing; print JSON with the members to extract and their sizes
  ledger  --check                      check the download ledger: each tarball once (a second fetch needs an `exception`), under 2 GB
  ledger  --add APP TAG --stage S [--exception TEXT] [--t1only]   append a ledger line for the tarball just fetched
  ledger  --count APP TAG              print how many ledger lines this tarball already has (a number, nothing else)
  ledger  --refetch-exception APP TAG  if this tarball already has a ledger line, print the exception text a second fetch must carry
                                       ("re-fetch: the earlier copy (stage ID, t1-only) was deleted with its tree"); else print nothing
ENVIRONMENT  FORCE_BAD_ASSET=1 asks for a deliberately wrong asset name (the blocked-download test).
             LJ_RELEASE_BASE, LJ_SP1_ASSETS, LJ_SP1_R8, LJ_SP1_EVIDENCE: test overrides (a local fake release server, a fake table, a scratch evidence folder).
EXIT CODES  0 ok; 1 hash mismatch or ledger violation (a finding); 2 bad usage; 3 download blocked.
NEVER TOUCHES  anything but the files it is given; it runs nothing from a download.
"""
import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402

BLOCKED = os.path.join(L.EVID, "blocked_proof.json")


def tarball_info(app, tag):
    assets = L.load_assets()
    pin = L.find_pin(assets, app, tag)
    if not pin:
        print("ERROR: %s %s is not one of the six pins in the asset table" % (app, tag), file=sys.stderr)
        sys.exit(2)
    return pin, pin["linux_x86_64_tarball"]


def requested_name(name):
    if os.environ.get("FORCE_BAD_ASSET") == "1":
        return name + ".does-not-exist"  # a deliberately wrong name: GitHub answers 404
    return name


def cmd_head(a):
    pin, tb = tarball_info(a.app, a.tag)
    url = L.asset_url(a.app, a.tag, requested_name(tb["name"]))
    h = L.curl_head(url, 60)
    ok = h["curl_exit"] == 0 and h["status"] == 200
    if not ok:
        pr = L.curl_probe(url, 60)  # curl -f on a 1 KB range: its own exit code and stderr line (a HEAD says exit 0 even for a 404)
        L.write_blocked_proof(BLOCKED, url, h["status"] or pr["status"], pr["curl_exit"] or h["curl_exit"], pr["stderr"] or h["stderr"], h["status_lines"],
                              context={"step": "head", "app": a.app, "tag": a.tag, "head_curl_exit": h["curl_exit"], "head_status": h["status"],
                                       "probe_status": pr["status"], "forced_bad_asset": os.environ.get("FORCE_BAD_ASSET") == "1"})
        print("BLOCKED: %s -> HTTP %s, curl exit %s, curl said: %s. Proof: %s. Fallback: spikes/sp1_craft_cli/FALLBACK.md"
              % (tb["name"], h["status"] or pr["status"], pr["curl_exit"] or h["curl_exit"], L.scrub(pr["stderr"] or h["stderr"] or "(nothing)"), L.rel(BLOCKED)))
        return 3
    print(json.dumps({"name": tb["name"], "status": h["status"], "bytes": h["content_length"], "expected_bytes": tb["bytes"],
                      "size_matches_table": h["content_length"] == tb["bytes"]}))
    return 0


def cmd_get(a):
    pin, tb = tarball_info(a.app, a.tag)
    url = L.asset_url(a.app, a.tag, requested_name(tb["name"]))
    if os.path.exists(a.dest):
        print("ERROR: %s exists; a stage downloads into a new empty folder" % L.rel(a.dest), file=sys.stderr)
        return 2
    r = L.curl_get(url, a.dest)
    if r["curl_exit"] != 0 or r["status"] != 200:
        heads = L.curl_head(url, 30)["status_lines"]
        L.write_blocked_proof(BLOCKED, url, r["status"], r["curl_exit"], r["stderr"], heads, bytes_received=r["bytes"],
                              context={"step": "get", "app": a.app, "tag": a.tag, "forced_bad_asset": os.environ.get("FORCE_BAD_ASSET") == "1"})
        if os.path.exists(a.dest):
            os.remove(a.dest)
        print("BLOCKED: GET %s -> HTTP %s, curl exit %s, curl said: %s. Proof: %s" % (tb["name"], r["status"], r["curl_exit"], L.scrub(r["stderr"]), L.rel(BLOCKED)))
        return 3
    print("downloaded %s: %d bytes in %.1f s (HTTP %s)" % (tb["name"], r["bytes"], r["seconds"], r["status"]))
    return 0


def independent_value(app, tag, kind):
    r8path = os.environ.get("LJ_SP1_R8") or os.path.join(L.SP1, "r8_hashes.json")
    if r8path == "none":
        return None
    try:
        r8 = L.read_json(r8path)
    except (OSError, ValueError):
        return None
    for ex in r8["expected"]:
        if ex["app"] == app and ex["tag"] == tag and ex["kind"] == kind:
            return ex["sha256"]
    return None


def cmd_verify(a):
    pin, tb = tarball_info(a.app, a.tag)
    got = L.sha256_file(a.file)
    size = os.path.getsize(a.file)
    ind = independent_value(a.app, a.tag, "linux_x86_64_tarball")
    problems = []
    if got != tb["sha256"]:
        problems.append("SHA-256 %s... differs from the release listing %s..." % (got[:12], tb["sha256"][:12]))
    if ind and got != ind:
        problems.append("SHA-256 %s... differs from the independent value %s... (research/craft-motion.md)" % (got[:12], ind[:12]))
    if tb.get("bytes") and size != tb["bytes"]:
        problems.append("size %d differs from the listed %d" % (size, tb["bytes"]))
    if problems:
        print("REJECTED: %s: %s. Nothing was extracted." % (tb["name"], "; ".join(problems)))
        return 1
    print("OK: %s sha256 %s%s" % (tb["name"], got, " (also equals the independent value)" if ind else " (no independent value for this asset: integrity only)"))
    return 0


def cmd_plan(a):
    prof = L.read_json(os.path.join(L.SP1, "config.json"))["profiles"][a.profile]
    members = []
    for ln in open(a.listing, "r", encoding="utf-8", errors="replace"):
        m = re.match(r"^([-dlhpcbs])\S*\s+\S+\s+(\d+)\s+\S+\s+\S+\s+(.*?)(?: -> .*)?$", ln.rstrip())
        if m:
            members.append({"type": m.group(1), "bytes": int(m.group(2)), "name": m.group(3)})
    files = [m for m in members if m["type"] in "-"]
    cli = a.app + "-cli"
    cli_members = [m for m in files if os.path.basename(m["name"]) == cli]
    gui = [m for m in files if os.path.basename(m["name"]) == a.app]
    if not cli_members:
        print(json.dumps({"error": "no member named %s in the tarball" % cli, "files": len(files)}))
        return 1
    if prof["extract"] == "all":
        chosen = members
    else:
        # lean: the CLI itself plus small neighbours it may need (libraries and data under lib/ or share/), never the GUI program
        chosen = list(cli_members)
        budget = 40 * 1048576
        for m in sorted(files, key=lambda x: x["bytes"]):
            if m in chosen or m in gui:
                continue
            if re.search(r"/(lib|lib64|libexec|share)/", "/" + m["name"]) and m["bytes"] <= budget:
                chosen.append(m)
                budget -= m["bytes"]
    total = sum(m["bytes"] for m in chosen if m["type"] == "-")
    out = {"profile": a.profile, "members_total": len(members), "files_total": len(files), "all_bytes": sum(m["bytes"] for m in files),
           "chosen_count": len(chosen), "chosen_bytes": total, "chosen_mb": round(total / 1048576.0, 1),
           "cli_member": cli_members[0]["name"], "cli_bytes": cli_members[0]["bytes"], "gui_bytes": gui[0]["bytes"] if gui else None,
           "chosen": [m["name"] for m in chosen]}
    print(json.dumps(out))
    return 0


def ledger_path():
    return os.path.join(L.EVID, "download_ledger.jsonl")


def read_ledger():
    rows = []
    if os.path.exists(ledger_path()):
        for ln in open(ledger_path(), "r", encoding="utf-8"):
            if ln.strip():
                rows.append(json.loads(ln))
    return rows


def cmd_ledger(a):
    if a.count or a.refetch_exception:
        app, tag = a.count or a.refetch_exception
        pin, tb = tarball_info(app, tag)
        prior = [r for r in read_ledger() if r["asset"] == tb["name"]]
        if a.count:
            print(len(prior))
        elif prior:
            last = prior[-1]
            # t1_only is recorded from this change on; the two lines written before it came from --t1-only acceptance runs (build/reports/WP-07.md)
            t1 = ", t1-only" if last.get("t1_only", True) else ""
            print("re-fetch: the earlier copy (stage %s%s) was deleted with its tree" % (last.get("stage") or "unknown", t1))
        return 0
    if a.add:
        app, tag = a.add
        pin, tb = tarball_info(app, tag)
        L.append_jsonl(ledger_path(), {"asset": tb["name"], "app": app, "tag": tag, "bytes": tb["bytes"], "sha256": tb["sha256"], "date_utc": L.today(),
                                       "stage": a.stage or "", "fetch": 1 + sum(1 for r in read_ledger() if r["asset"] == tb["name"]),
                                       "exception": a.exception or "", "t1_only": bool(a.t1only)})
        print("ledger: %s recorded" % tb["name"])
        return 0
    rows = read_ledger()
    seen, problems = {}, []
    for r in rows:
        seen.setdefault(r["asset"], []).append(r)
    for name, rs in sorted(seen.items()):
        if len(rs) > 1 and not all(r.get("exception") for r in rs[1:]):
            problems.append("%s was fetched %d times and a later fetch has no recorded exception" % (name, len(rs)))
    total = sum(r["bytes"] for r in rows)
    allowance = L.read_json(os.path.join(L.SP1, "config.json"))["disk"]["download_allowance_mb"] * 1048576
    if total > allowance:
        problems.append("total fetched %d bytes is over the %d byte allowance" % (total, allowance))
    print("ledger: %d fetches, %d distinct assets, %.1f MB in total (allowance %d MB)%s" % (len(rows), len(seen), total / 1048576.0, allowance // 1048576,
                                                                                         "" if not problems else "; PROBLEMS: " + "; ".join(problems)))
    return 1 if problems else 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("head", "get"):
        p = sub.add_parser(name)
        p.add_argument("app")
        p.add_argument("tag")
        if name == "get":
            p.add_argument("--dest", required=True)
    p = sub.add_parser("verify")
    p.add_argument("file")
    p.add_argument("app")
    p.add_argument("tag")
    p = sub.add_parser("plan")
    p.add_argument("listing")
    p.add_argument("app")
    p.add_argument("profile", choices=("full", "lean"))
    p = sub.add_parser("ledger")
    p.add_argument("--check", action="store_true")
    p.add_argument("--add", nargs=2, metavar=("APP", "TAG"))
    p.add_argument("--count", nargs=2, metavar=("APP", "TAG"))
    p.add_argument("--refetch-exception", nargs=2, metavar=("APP", "TAG"))
    p.add_argument("--stage")
    p.add_argument("--exception")
    p.add_argument("--t1only", action="store_true")
    a = ap.parse_args(argv)
    return {"head": cmd_head, "get": cmd_get, "verify": cmd_verify, "plan": cmd_plan, "ledger": cmd_ledger}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
