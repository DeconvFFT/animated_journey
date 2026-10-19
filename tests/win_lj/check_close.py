#!/usr/bin/env python3
"""check_close.py OUTPUT.txt EXPECTED.json [--no-canary]: compare a `lj.ps1 close` run with the planted tree's manifest.

Reads the WOULD REMOVE table of the saved console output and checks, against the manifest written by make_trees.py:
  * the set of "where" entries is exactly the expected set (nothing missing, nothing extra),
  * every row's file count and size text match the manifest,
  * the numbers are 1..N without gaps and the TOTAL line adds up,
  * no protected, outside or canary name appears anywhere in the output (CANARY, OUTSIDE, secret.xmp, outside/).
Prints one line per check and "problems: N". Exit 0 if none, 1 otherwise. Standard library only.
"""
import json
import re
import sys


def fmt(n):
    if n < 1024:
        return "%d B" % n
    if n < 1048576:
        return "%.1f KB" % (n / 1024.0)
    if n < 1073741824:
        return "%.1f MB" % (n / 1048576.0)
    return "%.1f GB" % (n / 1073741824.0)


def main(argv):
    if len(argv) < 2:
        print("usage: check_close.py OUTPUT.txt EXPECTED.json", file=sys.stderr)
        return 2
    out = open(argv[0], encoding="utf-8", errors="replace").read()
    exp = json.load(open(argv[1], encoding="utf-8"))["would_remove"]
    problems = []
    lines = out.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("WOULD REMOVE"))
    except StopIteration:
        print("PROBLEM no WOULD REMOVE section")
        print("problems: 1")
        return 1
    rows = []
    total = None
    for l in lines[start + 1:]:
        if l.strip() == "":
            break
        m = re.match(r"^\s+(\d+)\s+(.+?)\s{2,}(\d+)\s+(\d+(?:\.\d)? (?:B|KB|MB|GB))\s{2}(<root>[/\\].*)$", l)
        if m:
            rows.append((int(m.group(1)), m.group(2), int(m.group(3)), m.group(4), m.group(5)))
        elif l.strip().startswith("TOTAL:"):
            total = l.strip()
    nums = [r[0] for r in rows]
    if nums != list(range(1, len(rows) + 1)):
        problems.append("numbers are not 1..N: %r" % nums)
    got = {}
    for n, what, files, size, where in rows:
        got[where[len("<root>/"):].replace("\\", "/")] = (files, size, what)
    want = {e["path"]: (e["files"], fmt(e["bytes"]), e["kind"]) for e in exp}
    for p in sorted(set(want) - set(got)):
        problems.append("missing from the list: " + p)
    for p in sorted(set(got) - set(want)):
        problems.append("listed but not expected: " + p)
    for p in sorted(set(got) & set(want)):
        if got[p][0] != want[p][0] or got[p][1] != want[p][1]:
            problems.append("count/size differ for %s: got %s %s, want %s %s" % (p, got[p][0], got[p][1], want[p][0], want[p][1]))
        if want[p][2] not in got[p][2]:
            problems.append("kind differs for %s: got %r, want %r" % (p, got[p][2], want[p][2]))
    tf = sum(e["files"] for e in exp)
    tb = sum(e["bytes"] for e in exp)
    wt = "TOTAL: %d item(s), %d file(s), %s" % (len(exp), tf, fmt(tb))
    if total != wt:
        problems.append("TOTAL line differs: got %r, want %r" % (total, wt))
    for bad in ("CANARY", "OUTSIDE", "secret.xmp", "outside/", "outside\\"):
        if bad in out:
            problems.append("forbidden text appears in the output: " + bad)
    print("rows: %d expected: %d listed-and-expected: %d" % (len(rows), len(exp), len(set(got) & set(want))))
    for p in problems:
        print("PROBLEM " + p)
    print("problems: %d" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
