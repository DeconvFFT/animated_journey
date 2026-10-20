#!/usr/bin/env python3
"""ledger_row.py: the bpy wheel set of SP3 on the download ledger (gate w2, nudge 6; SP3 review nudge 1). Standard library only, no network.

USAGE  python3 -I spikes/sp3_blender/ledger_row.py check  [--requirements FILE] [--summary FILE]
       python3 -I spikes/sp3_blender/ledger_row.py count  [--ledger FILE]
       python3 -I spikes/sp3_blender/ledger_row.py append [--ledger FILE] --stage NAME [--date YYYY-MM-DD] [--fetch N] [--exception TEXT] [--note TEXT]

WHAT  SP3 installs bpy 5.2.2 with pip, which is a download of 428 MB (the 402 MB bpy wheel plus 11 small dependency wheels). The Craft tarballs have a ledger
      (build/evidence/wp07 and wp10 download_ledger.jsonl) that spikes/sp1b_readback/check_ledger.py and the integration test disk.downloads_under_2gb_allowance read; pip fetches
      were outside it, so the allowance check read 623.6 MB when the true figure was about 1.5 GB. This tool puts the pip fetches on the same ledger, one row per fetch of the set,
      and applies the same rule: a second fetch of the same set needs a recorded exception (a reason), exactly as for a tarball.
  check   the requirements file spikes/sp3_blender/requirements-bpy.txt is a --require-hashes file: the --require-hashes line, twelve requirements each pinned with ==, exactly one
          sha256 per requirement (64 hex digits), a size comment per requirement, and (when --summary is given or the default file exists) the same names, versions and digests as
          the pip report of the 20 Oct 2026 run (build/evidence/w2-sp3/run2_pip_summary.json). Exit 0 or 1. Reads only.
  count   how many fetches of the set the ledger already holds (prints the number).
  append  adds one row (asset bpy-5.2.2-wheelset-cp313-linux-x86_64, kind pip-wheel-set, bytes = the sum of the twelve files, sha256 = the bpy wheel's). The fetch number is the
          count plus one unless --fetch says otherwise (a back-fill); a fetch after the first needs --exception, else exit 3 and nothing is written.
EXIT CODES  0 done   1 the check found a problem   2 bad usage / unreadable file   3 a further fetch has no recorded reason
Prints no path of the machine, no host and no user name.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
ASSET = "bpy-5.2.2-wheelset-cp313-linux-x86_64"
REQ_DEFAULT = os.path.join(HERE, "requirements-bpy.txt")
SUMMARY_DEFAULT = os.path.join(REPO, "build", "evidence", "w2-sp3", "run2_pip_summary.json")
LEDGER_DEFAULT = os.path.join(REPO, "build", "evidence", "wp10", "download_ledger.jsonl")
REQ_REL = "spikes/sp3_blender/requirements-bpy.txt"


def parse_requirements(path):
    """-> (problems, [ {name, version, sha256, file, bytes} ], has_require_hashes_line, file_sha256)"""
    problems, reqs = [], []
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    has_flag = any(l.strip() == "--require-hashes" for l in lines)
    pending = None            # (file, bytes) from the last size comment
    i = 0
    while i < len(lines):
        l = lines[i].rstrip()
        m = re.match(r"^# (\S+\.whl) (\d+) bytes$", l)
        if m:
            pending = (m.group(1), int(m.group(2)))
        mr = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9.!+_-]+)\s*\\\s*$", l)
        if mr:
            hashes = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("--hash="):
                hashes += re.findall(r"--hash=sha256:([0-9a-f]{64})\s*$", lines[j].strip()) or ["BAD:" + lines[j].strip()[:20]]
                j += 1
            if len(hashes) != 1 or hashes[0].startswith("BAD:"):
                problems.append("%s==%s must carry exactly one --hash=sha256:<64 hex digits> line (found %s)" % (mr.group(1), mr.group(2), hashes))
            if pending is None:
                problems.append("%s==%s has no '# <file>.whl <bytes> bytes' comment before it" % (mr.group(1), mr.group(2)))
            reqs.append({"name": mr.group(1), "version": mr.group(2), "sha256": hashes[0] if hashes else "", "file": pending[0] if pending else "", "bytes": pending[1] if pending else 0})
            pending = None
            i = j
            continue
        if l and not l.startswith("#") and l != "--require-hashes":
            problems.append("unexpected line (only comments, --require-hashes and pinned requirements belong here): %s" % l[:60])
        i += 1
    return problems, reqs, has_flag, hashlib.sha256(raw).hexdigest()


def do_check(a):
    try:
        problems, reqs, flag, _ = parse_requirements(a.requirements)
    except (OSError, UnicodeDecodeError) as e:
        print("ledger_row: cannot read the requirements file (%s)" % type(e).__name__, file=sys.stderr)
        return 2
    if not flag:
        problems.append("the --require-hashes line is missing")
    if len(reqs) != 12:
        problems.append("expected 12 pinned requirements (bpy and its 11 dependency wheels), found %d" % len(reqs))
    if not reqs or reqs[0]["name"] != "bpy" or reqs[0]["version"] != "5.2.2":
        problems.append("the first requirement must be bpy==5.2.2")
    summ_path = a.summary
    compared = 0
    if summ_path and os.path.isfile(summ_path):
        try:
            summ = json.load(open(summ_path, "r", encoding="utf-8"))["files"]
        except (OSError, ValueError, KeyError):
            summ = None
            problems.append("the pip report summary cannot be read")
        if summ is not None:
            want = {(f["name"].lower().replace("_", "-"), f["version"]): f for f in summ}
            have = {(r["name"].lower().replace("_", "-"), r["version"]): r for r in reqs}
            for k in sorted(set(want) | set(have)):
                if k not in have:
                    problems.append("%s %s is in the pip report but not in the requirements file" % k)
                elif k not in want:
                    problems.append("%s %s is in the requirements file but not in the pip report" % k)
                else:
                    compared += 1
                    if want[k]["sha256"] != have[k]["sha256"]:
                        problems.append("%s %s: the digest differs from the pip report" % k)
                    if want[k]["file"] != have[k]["file"]:
                        problems.append("%s %s: the file name differs from the pip report (%s vs %s)" % (k + (have[k]["file"][:40], want[k]["file"][:40])))
    total = sum(r["bytes"] for r in reqs)
    print("requirements-bpy.txt: %d pinned requirements, %s, %s bytes in all (the bpy wheel %s); %d compared with the pip report of 20 Oct 2026; %s" % (
        len(reqs), "--require-hashes line present" if flag else "NO --require-hashes line", "{:,}".format(total), "{:,}".format(reqs[0]["bytes"]) if reqs else "?", compared,
        "OK" if not problems else "PROBLEMS: " + "; ".join(problems)))
    return 1 if problems else 0


def ledger_rows(path):
    rows = []
    if os.path.isfile(path):
        for ln in open(path, "r", encoding="utf-8"):
            if ln.strip():
                try:
                    rows.append(json.loads(ln))
                except ValueError:
                    raise SystemExit("ERROR: the ledger is not JSON lines")
    return rows


def do_count(a):
    n = sum(1 for r in ledger_rows(a.ledger) if r.get("asset") == ASSET)
    print(n)
    return 0


def do_append(a):
    try:
        problems, reqs, flag, req_sha = parse_requirements(a.requirements)
    except (OSError, UnicodeDecodeError):
        print("ledger_row: cannot read the requirements file", file=sys.stderr)
        return 2
    if problems or not flag or len(reqs) != 12:
        print("ledger_row: the requirements file does not pass 'check'; nothing was written", file=sys.stderr)
        return 2
    n = sum(1 for r in ledger_rows(a.ledger) if r.get("asset") == ASSET)
    fetch = a.fetch or (n + 1)
    if fetch > 1 and not (a.exception or "").strip():
        print("ledger_row: the ledger already holds %d fetch(es) of the bpy wheel set; a further fetch needs a recorded reason (--exception, or SP3_FETCH_REASON for run_sp3.sh --run). Nothing was written." % n, file=sys.stderr)
        return 3
    date = a.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    row = {"app": "bpy", "asset": ASSET, "bytes": sum(r["bytes"] for r in reqs), "date_utc": date, "exception": (a.exception or "").strip() if fetch > 1 else "",
           "fetch": fetch, "files": len(reqs), "kind": "pip-wheel-set", "requirements": REQ_REL, "requirements_sha256": req_sha, "sha256": reqs[0]["sha256"],
           "source": "pypi.org", "stage": a.stage, "tag": "5.2.2", "wheel_bytes": reqs[0]["bytes"]}
    if a.note:
        row["note"] = a.note
    os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
    with open(a.ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    print("ledger: fetch %d of the bpy wheel set recorded (%s bytes, stage %s)" % (fetch, "{:,}".format(row["bytes"]), a.stage))
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("--requirements", default=REQ_DEFAULT)
    c.add_argument("--summary", default=SUMMARY_DEFAULT)
    n = sub.add_parser("count")
    n.add_argument("--ledger", default=LEDGER_DEFAULT)
    p = sub.add_parser("append")
    p.add_argument("--ledger", default=LEDGER_DEFAULT)
    p.add_argument("--requirements", default=REQ_DEFAULT)
    p.add_argument("--stage", required=True)
    p.add_argument("--date")
    p.add_argument("--fetch", type=int)
    p.add_argument("--exception", default="")
    p.add_argument("--note", default="")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        return do_check(a)
    if a.cmd == "count":
        return do_count(a)
    if a.cmd == "append":
        return do_append(a)
    ap.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
