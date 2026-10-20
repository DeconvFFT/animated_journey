#!/usr/bin/env python3
"""check_verdicts.py: is spikes/VERDICTS-W2.md complete? (build plan WP-10 acceptance.) READ-ONLY, standard library only.

USAGE  python3 -I tests/spikes/check_verdicts.py [--file PATH] [--root DIR]
RULES  the main table has exactly five rows, SP1 to SP5; each has a status word (Done, Partial, Deferred or Not run), a non-empty justification and next step, an ISO date, and at least one
       evidence path in backticks that EXISTS under the repository root (a trailing * is a glob); the SP1 sub-table has exactly six rows T1 to T6 with the same fields and evidence rule;
       T5 and T6 are "Not run"; T5's justification says "learning-only app, no decision depends on it"; T6's says the web builds are not pins; every Craft result is labelled a Linux CLI result.
EXIT CODES  0 complete   1 something is missing   2 bad usage / unreadable file
"""
import argparse
import glob
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
STATUS = ("Done", "Partial", "Deferred", "Not run")


def rows(text, first_col_pat):
    out = []
    for ln in text.splitlines():
        if ln.startswith("|") and re.match(r"\|\s*\*{0,2}(%s)\b" % first_col_pat, ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            out.append(cells)
    return out


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", default=os.path.join(REPO, "spikes", "VERDICTS-W2.md"))
    ap.add_argument("--root", default=REPO)
    a = ap.parse_args(argv)
    try:
        text = open(a.file, "r", encoding="utf-8").read()
    except OSError as e:
        print("check_verdicts: cannot read the file: %s" % e, file=sys.stderr)
        return 2
    problems = []

    def evidence_ok(cell, label):
        paths = re.findall(r"`([^`\s]+)`", cell)
        paths = [p for p in paths if "/" in p or p.endswith((".md", ".json", ".py", ".sh", ".txt", ".jsonl"))]
        if not paths:
            problems.append("%s: no evidence path in backticks" % label)
            return
        for p in paths:
            if not glob.glob(os.path.join(a.root, p)):
                problems.append("%s: evidence path does not exist: %s" % (label, p))

    main_rows = rows(text, r"SP[1-5]")
    ids = [re.sub(r"\W", "", r[0]) for r in main_rows]
    if ids != ["SP1", "SP2", "SP3", "SP4", "SP5"]:
        problems.append("main table rows are %s, expected SP1 to SP5 once each" % ids)
    for r in main_rows:
        label = re.sub(r"\W", "", r[0])
        if len(r) < 7:
            problems.append("%s: expected 7 columns, found %d" % (label, len(r)))
            continue
        status = r[2].replace("*", "").strip()
        if not any(status.startswith(s) for s in STATUS):
            problems.append("%s: status %r is not one of %s" % (label, status, STATUS))
        evidence_ok(r[3], label)
        if len(r[4]) < 40:
            problems.append("%s: justification is empty or too short" % label)
        if len(r[5]) < 10:
            problems.append("%s: next step is empty" % label)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[6]):
            problems.append("%s: date %r is not YYYY-MM-DD" % (label, r[6]))
    t_rows = rows(text, r"T[1-6]")
    tids = [re.sub(r"\W", "", r[0].split(" ")[0]) for r in t_rows]
    tids = [re.match(r"T[1-6]", re.sub(r"[*]", "", r[0])).group(0) for r in t_rows]
    if tids != ["T1", "T2", "T3", "T4", "T5", "T6"]:
        problems.append("SP1 sub-table rows are %s, expected T1 to T6 once each" % tids)
    for r, t in zip(t_rows, tids):
        if len(r) < 6:
            problems.append("%s: expected 6 columns, found %d" % (t, len(r)))
            continue
        status = r[1].replace("*", "").strip()
        if not any(status.startswith(s) for s in STATUS):
            problems.append("%s: status %r is not one of %s" % (t, status, STATUS))
        evidence_ok(r[2], t)
        if len(r[3]) < 20:
            problems.append("%s: justification is empty or too short" % t)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[5]):
            problems.append("%s: date %r is not YYYY-MM-DD" % (t, r[5]))
        if t in ("T5", "T6") and not status.startswith("Not run"):
            problems.append("%s must be 'Not run', found %r" % (t, status))
        if t == "T5" and "learning-only app, no decision depends on it" not in r[3]:
            problems.append("T5 justification must say 'learning-only app, no decision depends on it'")
        if t == "T6" and "web builds are not pins" not in r[3]:
            problems.append("T6 justification must say the web builds are not pins")
    if "Linux CLI result" not in text or "not evidence for Windows" not in text:
        problems.append("the file must label the Craft results as Linux CLI results, not evidence for Windows")
    print("check_verdicts: %d main rows, %d SP1 test rows; %s" % (len(main_rows), len(t_rows), "complete" if not problems else "PROBLEMS: " + "; ".join(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
