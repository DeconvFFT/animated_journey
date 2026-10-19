#!/usr/bin/env python3
"""run_checks.py - WP-02 test runner (called by tests/ops/run_tests.sh).

Runs the acceptance tests and the negative tests for scripts/decisions_to_csv.py,
scripts/hours_report.py and scripts/ops_lint.py, and checks the ops files. For every test it
writes one evidence envelope (build plan 4.2, schema lj-evidence/1) to build/evidence/wp02/<test>.json
and appends the commands and their real output to build/evidence/wp02/transcript.txt.

  python3 -I tests/ops/run_checks.py --quick   # no ffmpeg, a few seconds
  python3 -I tests/ops/run_checks.py --all     # adds the settings-card commands run on tiny files
  --only NAME  run one test    --list  list the tests    --no-evidence  do not write evidence

Environment: LJ_PATTERNS=path uses that pattern file instead of scripts/redaction_patterns.json
(for development while the real file has not landed; the report says when it was used).

Everything the tests write goes to a temporary folder that is removed afterwards. Nothing in the
repository is modified: tracked files are hashed before and after (test readonly_proof).
Exit codes: 0 all tests PASS (or SKIPPED/UNVERIFIED), 1 at least one FAIL or BLOCKED.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PY = [sys.executable, "-I"]
EVID = os.path.join(ROOT, "build", "evidence", "wp02")
PATTERN_FILE = os.environ.get("LJ_PATTERNS") or os.path.join(ROOT, "scripts", "redaction_patterns.json")
USING_OVERRIDE = bool(os.environ.get("LJ_PATTERNS"))
PACKAGE = "WP-02"
TESTS = []


class Skip(Exception):
    pass


class Blocked(Exception):
    pass


def test(tid, title, quick=True, needs_patterns=False):
    def deco(fn):
        TESTS.append({"id": tid, "title": title, "fn": fn, "quick": quick, "needs_patterns": needs_patterns})
        return fn
    return deco


class Ctx:
    def __init__(self, tid):
        self.tid = tid
        self.tmp = tempfile.mkdtemp(prefix="lj-wp02-")
        self.log = []
        self.said = []
        self.unverified = []
        self.notes = []

    def run(self, args, cwd=None, extra_env=None):
        env = dict(os.environ)
        env.pop("LJ_PATTERNS", None)
        env.pop("LJ_DENY_FILE", None)
        if extra_env:
            env.update(extra_env)
        p = subprocess.run(PY + list(args), cwd=cwd or ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env)
        out = (p.stdout or "") + (p.stderr or "")
        self.log.append(("python3 -I " + " ".join(self._show(a) for a in args), p.returncode, out))
        return p.returncode, out

    def _show(self, a):
        if PATTERN_FILE and os.path.abspath(PATTERN_FILE) != os.path.join(ROOT, "scripts", "redaction_patterns.json"):
            a = a.replace(PATTERN_FILE, "<dev pattern file>")
        a = a.replace(self.tmp, "<tmp>").replace(ROOT, ".")
        return a

    def patterns(self):
        """The real pattern file when it exists (or the LJ_PATTERNS override); otherwise a tiny synthetic
        file, so that tests of ops_lint's own mechanisms (comparisons, exit codes, masking, deny list)
        do not depend on WP-03. Tests of what counts as identifying data need the real file instead."""
        if USING_OVERRIDE or os.path.isfile(PATTERN_FILE):
            return PATTERN_FILE
        self.used_mini = True
        cats = [{"id": cid, "scope": "both", "action": "refuse", "regex": "ZZNEVER" + cid.upper(), "flags": ""}
                for cid in ["email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux",
                            "token_shape", "guid_serial", "handle"]]
        return self.write("mini_patterns.json", json.dumps(
            {"schema": "synthetic", "version": "mini", "categories": cats, "mask": {"keep": 2, "fill": "*"}}))

    def lint(self, *args, root=None):
        a = ["scripts/ops_lint.py", "--patterns", self.patterns()]
        if root:
            a += ["--root", root]
        return self.run(a + list(args))

    def say(self, text):
        self.said.append(text)

    def write(self, rel, text, binary=False):
        path = os.path.join(self.tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8", "newline": ""})) as fh:
            fh.write(text)
        return path

    def clone(self):
        """A temp copy of the repository subset that ops_lint reads: ops/ and DECISIONS.md."""
        self.clones = getattr(self, "clones", 0) + 1
        dst = os.path.join(self.tmp, "repo%d" % self.clones)
        os.makedirs(dst)
        shutil.copytree(os.path.join(ROOT, "ops"), os.path.join(dst, "ops"))
        shutil.copy(os.path.join(ROOT, "DECISIONS.md"), os.path.join(dst, "DECISIONS.md"))
        return dst

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)


def has(out, *needles):
    for n in needles:
        ok(n in out, "expected %r in the output; got:\n%s" % (n, out[-600:]))


def lacks(out, *needles):
    for n in needles:
        ok(n not in out, "did not expect %r in the output" % n)


def read(rel):
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as fh:
        return fh.read()


def register_ids():
    return re.findall(r"^\|\s*([DWOS]-[0-9]{2})\s*\|", read("DECISIONS.md"), re.M)


def csv_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def need_patterns():
    if not USING_OVERRIDE and not os.path.isfile(PATTERN_FILE):
        raise Blocked("scripts/redaction_patterns.json (WP-03, build plan 4.13) has not landed; "
                      "ops_lint fails closed without it. Set LJ_PATTERNS to run against another file.")


def avail_mb():
    st = os.statvfs("/")
    return int(st.f_bavail * st.f_frsize / (1024 * 1024))


# ======================================================================= decisions_to_csv

@test("decisions_check_real", "decisions_to_csv --check ops/decisions.csv exits 0; independent count equals the CSV")
def _(ctx):
    rc, out = ctx.run(["scripts/decisions_to_csv.py", "--check", "ops/decisions.csv"])
    ok(rc == 0, out)
    ids = register_ids()
    rows = csv_rows(os.path.join(ROOT, "ops", "decisions.csv"))
    ok(len(rows) == len(ids) == len(set(ids)), "row count %d vs independent count %d" % (len(rows), len(ids)))
    c = {k: sum(1 for i in ids if i[0] == k) for k in "DWOS"}
    got = {k: sum(1 for r in rows if r["id"][0] == k) for k in "DWOS"}
    ok(c == got, "per-prefix counts differ: %s vs %s" % (c, got))
    ctx.say(out.strip())
    if (len(rows), c) != (166, {"D": 30, "W": 60, "O": 35, "S": 41}):
        ctx.notes.append("the register no longer has the 2026-10-19 snapshot size (166 rows: D 30, W 60, O 35, S 41); now %d %s"
                         % (len(rows), c))
    else:
        ctx.say("snapshot 2026-10-19 matches: 166 rows (D 30, W 60, O 35, S 41)")


@test("decisions_write_twice", "--write twice is byte-identical, and equals the committed file when no orchestrator cell is set")
def _(ctx):
    out_csv = os.path.join(ctx.tmp, "decisions.csv")
    rc, o1 = ctx.run(["scripts/decisions_to_csv.py", "--write", out_csv])
    ok(rc == 0, o1)
    first = open(out_csv, "rb").read()
    rc, o2 = ctx.run(["scripts/decisions_to_csv.py", "--write", out_csv])
    ok(rc == 0, o2)
    ok(open(out_csv, "rb").read() == first, "second --write changed the bytes")
    rc, o3 = ctx.run(["scripts/decisions_to_csv.py", "--check", out_csv])
    ok(rc == 0, o3)
    ok(not first.startswith(b"\xef\xbb\xbf") and b"\r" not in first, "must be UTF-8 without BOM and with LF line endings")
    committed = open(os.path.join(ROOT, "ops", "decisions.csv"), "rb").read()
    rows = csv_rows(os.path.join(ROOT, "ops", "decisions.csv"))
    if not any(r["maker_answer"] or r["last_changed"] for r in rows):
        ok(committed == first, "the committed ops/decisions.csv differs from a fresh generation: run --write")
        ctx.say("fresh generation equals the committed file byte for byte")
    ctx.say(o1.strip())


@test("decisions_write_in_place", "literal acceptance: --write ops/decisions.csv twice leaves the tracked file unchanged", quick=False)
def _(ctx):
    path = os.path.join(ROOT, "ops", "decisions.csv")
    before = open(path, "rb").read()
    try:
        rc, o1 = ctx.run(["scripts/decisions_to_csv.py", "--write", "ops/decisions.csv"])
        ok(rc == 0, o1)
        mid = open(path, "rb").read()
        rc, o2 = ctx.run(["scripts/decisions_to_csv.py", "--write", "ops/decisions.csv"])
        ok(rc == 0, o2)
        ok(open(path, "rb").read() == mid, "second --write changed the bytes")
        rc, o3 = ctx.run(["scripts/decisions_to_csv.py", "--check", "ops/decisions.csv"])
        ok(rc == 0, o3)
        ok(mid == before, "ops/decisions.csv was stale against DECISIONS.md (the test restored the old bytes)")
        ctx.say("in-place --write x2 then --check: exit 0, file unchanged")
    finally:
        with open(path, "wb") as fh:
            fh.write(before)


@test("decisions_content", "status vocabulary, D-14/D-23 notes, O-05/O-13 answered, S rows carry Table 4 status, 300-char cut")
def _(ctx):
    rows = {r["id"]: r for r in csv_rows(os.path.join(ROOT, "ops", "decisions.csv"))}
    vocab = {"decided", "default", "open", "pending", "answered", "superseded", "applied", "outstanding"}
    bad = [(i, r["status"]) for i, r in rows.items() if r["status"] not in vocab]
    ok(not bad, "statuses outside the vocabulary: %s" % bad)
    ok("superseded by D-26" in rows["D-14"]["note"] and rows["D-14"]["status"] == "superseded", "D-14 note/status")
    ok("superseded by D-29" in rows["D-23"]["note"] and rows["D-23"]["status"] == "superseded", "D-23 note/status")
    ok(rows["O-05"]["status"] == "answered" and rows["O-13"]["status"] == "answered", "O-05/O-13 must be answered")
    ok(all(rows[i]["maker_answer"] == "" and rows[i]["last_changed"] == "" for i in rows), "owner cells must start empty")
    ok(all(rows["D-%02d" % n]["status"] in ("decided", "superseded") for n in range(1, 31)), "D rows")
    ok(all(r["status"] == "default" for i, r in rows.items() if i[0] == "W"), "W rows are defaults")
    ok(all(r["status"] in ("applied", "outstanding") for i, r in rows.items() if i[0] == "S"), "S rows carry the Table 4 status")
    # expectations derived from the register text itself (a plain split, not the generator's parser)
    want_out, want_pend, want_ans = set(), set(), set()
    for line in read("DECISIONS.md").split("\n"):
        m = re.match(r"^\|\s*([SO]-[0-9]{2})\s*\|(.*)$", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if m.group(1)[0] == "S" and cells[-2].lower().startswith("**outstanding"):
            want_out.add(m.group(1))
        if m.group(1)[0] == "O":
            if cells[0].lower().startswith("answered"):
                want_ans.add(m.group(1))
            elif cells[1].startswith("**(pending"):
                want_pend.add(m.group(1))
    got = lambda st, pre: {i for i, r in rows.items() if i[0] == pre and r["status"] == st}
    ok(got("outstanding", "S") == want_out, "outstanding S rows: %s vs register %s" % (sorted(got("outstanding", "S")), sorted(want_out)))
    ok(got("pending", "O") == want_pend, "pending O rows: %s vs register %s" % (sorted(got("pending", "O")), sorted(want_pend)))
    ok(got("answered", "O") == want_ans and {"O-05", "O-13"} <= want_ans, "answered O rows: %s" % sorted(got("answered", "O")))
    longest = max(len(v) for r in rows.values() for v in r.values())
    ok(longest <= 300, "a cell is %d characters" % longest)
    cut = [(i, k) for i, r in rows.items() for k, v in r.items() if v.endswith("... see DECISIONS.md")]
    ok(cut, "expected at least one cut cell")
    text = open(os.path.join(ROOT, "ops", "decisions.csv"), encoding="utf-8").read()
    ok(not re.search(r"github\.com/(?!<owner>)", text), "the public repository owner handle must not be copied (D-26)")
    ok("**" not in text and "`" not in text, "Markdown marks must be removed")
    ctx.say("%d rows; %d cut cells; longest cell %d characters" % (len(rows), len(cut), longest))


@test("decisions_carry_over", "orchestrator-owned cells (maker_answer, last_changed) survive --write and are ignored by --check")
def _(ctx):
    p = os.path.join(ctx.tmp, "d.csv")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", p]); ok(rc == 0, o)
    lines = open(p, encoding="utf-8").read().split("\n")
    ix = [n for n, l in enumerate(lines) if l.startswith("O-12,")][0]
    rows = list(csv.reader([lines[ix]]))[0]
    rows[8] = "2026-10-26"
    rows[9] = "plan name recorded privately"
    buf = io.StringIO(); csv.writer(buf, lineterminator="").writerow(rows); lines[ix] = buf.getvalue()
    open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", p]); ok(rc == 0, "check must ignore owner cells: " + o)
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", p]); ok(rc == 0, o)
    has(o, "carried over: 1 row")
    r = {x["id"]: x for x in csv_rows(p)}["O-12"]
    ok(r["maker_answer"] == "plan name recorded privately" and r["last_changed"] == "2026-10-26", "values were lost")
    ctx.say(o.strip())


@test("decisions_neg_delete_row", "negative: a deleted ID row makes --check and ops_lint exit 1 naming the ID")
def _(ctx):
    repo = ctx.clone()
    p = os.path.join(repo, "ops", "decisions.csv")
    lines = open(p, encoding="utf-8").read().split("\n")
    open(p, "w", encoding="utf-8", newline="").write("\n".join(l for l in lines if not l.startswith("W-10,")))
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", p]); ok(rc == 1, o); has(o, "W-10", "missing")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "W-10")
    ctx.say("--check and ops_lint: exit 1, W-10 named")


@test("decisions_neg_invented_id", "negative: an invented ID row makes --check and ops_lint exit 1 naming the ID")
def _(ctx):
    repo = ctx.clone()
    p = os.path.join(repo, "ops", "decisions.csv")
    lines = open(p, encoding="utf-8").read().split("\n")
    w10 = [l for l in lines if l.startswith("W-10,")][0]
    lines.insert(lines.index(w10) + 1, "W-99," + w10[len("W-10,"):])
    open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", p]); ok(rc == 1, o); has(o, "W-99", "invented")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "W-99")
    ctx.say("--check and ops_lint: exit 1, W-99 named")


@test("decisions_neg_header", "negative: a changed header name makes --check and ops_lint exit 1 naming the header")
def _(ctx):
    repo = ctx.clone()
    p = os.path.join(repo, "ops", "decisions.csv")
    t = open(p, encoding="utf-8").read().replace("id,table,short_title,value_or_default,status,", "id,table,short_title,value_or_default,state,", 1)
    open(p, "w", encoding="utf-8", newline="").write(t)
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", p]); ok(rc == 1, o); has(o, "header")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "header")
    ctx.say("--check and ops_lint: exit 1, header named")


@test("decisions_neg_values", "negative: a changed status/value and an invalid status word are named by ID and column")
def _(ctx):
    repo = ctx.clone()
    p = os.path.join(repo, "ops", "decisions.csv")
    t = open(p, encoding="utf-8").read()
    lines = t.split("\n")
    ix = [n for n, l in enumerate(lines) if l.startswith("W-05,")][0]
    cells = next(csv.reader([lines[ix]]))
    cells[4] = "maybe"
    buf = io.StringIO(); csv.writer(buf, lineterminator="").writerow(cells); lines[ix] = buf.getvalue()
    ix = [n for n, l in enumerate(lines) if l.startswith("W-06,")][0]
    cells = next(csv.reader([lines[ix]]))
    cells[3] = "tampered value"
    buf = io.StringIO(); csv.writer(buf, lineterminator="").writerow(cells); lines[ix] = buf.getvalue()
    open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", p]); ok(rc == 1, o)
    has(o, "W-05", "status", "W-06", "value_or_default")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "W-05", "W-06")
    ctx.say("exit 1, W-05 status and W-06 value named")


@test("decisions_register_growth", "an added register row (for example a new O-36) is picked up with no code change")
def _(ctx):
    reg = read("DECISIONS.md")
    anchor = [l for l in reg.split("\n") if l.startswith("| O-35 |")][0]
    new = anchor + "\n| O-36 | Sun 1 Nov | A synthetic test question? | A synthetic recommendation. |"
    p = ctx.write("DECISIONS.md", reg.replace(anchor, new, 1))
    out = os.path.join(ctx.tmp, "g.csv")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", out, "--register", p]); ok(rc == 0, o)
    has(o, "167 rows", "O 36")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", p])
    ok(rc == 1, o); has(o, "O-36", "missing")
    ctx.say("167 rows with O-36 added; the old CSV is reported stale")


@test("decisions_bad_register", "a malformed register (wrong cell count, duplicate ID, ID in the wrong table) exits 2")
def _(ctx):
    reg = read("DECISIONS.md")
    anchor = [l for l in reg.split("\n") if l.startswith("| O-35 |")][0]
    cases = {
        "cells": reg.replace(anchor, anchor + "\n| O-36 | only two cells |", 1),
        "dup": reg.replace(anchor, anchor + "\n" + anchor, 1),
        "table": reg.replace(anchor, anchor + "\n| W-61 | Sun 1 Nov | wrong table | x |", 1),
    }
    for name, text in cases.items():
        p = ctx.write(name + ".md", text)
        rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", p])
        ok(rc == 2, "%s: exit %d: %s" % (name, rc, o))
        has(o, "malformed")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", os.path.join(ctx.tmp, "none.md")])
    ok(rc == 2, o)
    ctx.say("three malformed registers and a missing one: exit 2 each")


# ======================================================================= hours_report

def hours(ctx, text, *args, name="h.csv", binary=False):
    p = ctx.write(name, text, binary=binary)
    return ctx.run(["scripts/hours_report.py", p] + list(args))


@test("hours_header_only", "hours_report on the header-only ops/hours.csv: 'no rows yet', exit 0")
def _(ctx):
    rc, o = ctx.run(["scripts/hours_report.py", "ops/hours.csv", "--week-start", "2026-10-19"])
    ok(rc == 0, o); has(o, "no rows yet")
    ok(open(os.path.join(ROOT, "ops", "hours.csv"), encoding="utf-8").read() == "date,shot_or_chapter,activity,minutes,who,note\n",
       "ops/hours.csv must be the header only")
    ctx.say(o.strip())


@test("hours_9h30", "hours_9h30.csv: total 9.5 h and the '9 minutes' reading, exit 0")
def _(ctx):
    rc, o = ctx.run(["scripts/hours_report.py", "tests/ops/fixtures/hours_9h30.csv", "--week-start", "2026-10-19"])
    ok(rc == 0, o); has(o, "9.5 h", "570 minutes", "plan 9 minutes", "indicative")
    ctx.say(o.strip())


@test("hours_7h30", "hours_7h30.csv: 'under about 8 hours ... F-0 would become the plan', exit 0")
def _(ctx):
    rc, o = ctx.run(["scripts/hours_report.py", "tests/ops/fixtures/hours_7h30.csv", "--week-start", "2026-10-19"])
    ok(rc == 0, o); has(o, "7.5 h", "under about 8 hours", "F-0 would become the plan", "indicative")
    ctx.say(o.strip())


@test("hours_bad_activity", "hours_bad_activity.csv: exit 1 and the line number")
def _(ctx):
    rc, o = ctx.run(["scripts/hours_report.py", "tests/ops/fixtures/hours_bad_activity.csv"])
    ok(rc == 1, o); has(o, "line 3", "activity 'Ga", "gather|scan|story"); lacks(o, "Gathering")
    ctx.say(o.strip())


@test("hours_thresholds", "W-02 reading at every boundary (479/480/839/840/959/960 minutes)")
def _(ctx):
    cases = [(479, "under about 8 hours"), (480, "plan 9 minutes"), (839, "plan 9 minutes"),
             (840, "only if you add hours"), (959, "only if you add hours"), (960, "plan 12 minutes")]
    for mins, phrase in cases:
        rc, o = hours(ctx, "date,shot_or_chapter,activity,minutes,who,note\n2026-10-19,-,learn,%d,maker,x\n" % mins,
                      "--week-start", "2026-10-19")
        ok(rc == 0, o); has(o, phrase)
    ctx.say("6 boundary cases behave")


@test("hours_validation", "bad header, date, minutes, shot id, extra column, empty who: exit 1 with line numbers")
def _(ctx):
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    cases = [
        ("date,activity,minutes\n2026-10-19,learn,5\n", "line 1", "header must be exactly"),
        (h + "19/10/2026,-,learn,30,maker,x\n", "line 2", "date '19/10/2026'"),
        (h + "2026-02-30,-,learn,30,maker,x\n", "line 2", "not a real calendar date"),
        (h + "2026-10-19,-,learn,1.5h,maker,x\n", "line 2", "minutes '1.5h'"),
        (h + "2026-10-19,-,learn,0,maker,x\n", "line 2", "minutes '0'"),
        (h + "2026-10-19,-,learn,1441,maker,x\n", "line 2", "minutes '1441'"),
        (h + "2026-10-19,album pages,learn,30,maker,x\n", "line 2", "shot_or_chapter 'al"),
        (h + "2026-10-19,-,learn,30,maker,one, two\n", "line 2", "expected 6 columns, found 7"),
        (h + "2026-10-19,-,learn,30,,x\n", "line 2", "who '' must be exactly maker or agent"),
        (h + "2026-10-19,-,learn,30,someone,x\n", "line 2", "who 'so", "must be exactly maker or agent"),
        (h + "2026-10-19,-,learn,30,Maker,x\n", "line 2", "must be exactly maker or agent"),
        (h + "2026-10-19,-,Learn,30,maker,x\n", "line 2", "did you mean 'learn'"),
        ("", "line 1", "empty"),
    ]
    for text, *needles in cases:
        rc, o = hours(ctx, text)
        ok(rc == 1, "exit %d for %r: %s" % (rc, text[:50], o)); has(o, *needles)
        lacks(o, "someone", "album pages")
    ctx.say("%d invalid files, each exit 1 with the line and the problem" % len(cases))


@test("hours_usage", "missing file and bad --week-start exit 2")
def _(ctx):
    rc, o = ctx.run(["scripts/hours_report.py", os.path.join(ctx.tmp, "nope.csv")]); ok(rc == 2, o)
    rc, o = ctx.run(["scripts/hours_report.py", "ops/hours.csv", "--week-start", "19-10-2026"]); ok(rc == 2, o)
    rc, o = ctx.run(["scripts/hours_report.py", "ops/hours.csv", "--week-start", "2026-13-40"]); ok(rc == 2, o)
    rc, o = ctx.run(["scripts/hours_report.py", "ops/hours.csv", "--days", "0"]); ok(rc == 2, o)
    rc, o = ctx.run(["scripts/hours_report.py"]); ok(rc == 2, o)
    ctx.say("five usage errors: exit 2")


@test("hours_windows", "windows: rows outside the window, non-maker rows, several weeks, --days, --json")
def _(ctx):
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    body = (h + "2026-10-18,-,learn,60,maker,sunday before\n2026-10-19,-,learn,120,maker,a\n"
            "2026-10-25,-,admin,60,maker,b\n2026-10-26,-,learn,600,maker,next week\n2026-10-20,-,learn,90,agent,not counted\n")
    rc, o = hours(ctx, body, "--week-start", "2026-10-19")
    ok(rc == 0, o); has(o, "3.0 h", "(180 minutes)", "not counted (who is not 'maker'): 90 minutes")
    rc, o = hours(ctx, body)
    ok(rc == 0, o); has(o, "Window 2026-10-12", "Window 2026-10-19", "Window 2026-10-26", "10.0 h")
    rc, o = hours(ctx, body, "--week-start", "2026-11-02")
    ok(rc == 0, o); has(o, "none falls in the window", "no rows in this window")
    rc, o = hours(ctx, body, "--week-start", "2026-10-19", "--days", "14")
    ok(rc == 0, o); has(o, "13.0 h")
    rc, o = hours(ctx, body, "--week-start", "2026-10-19", "--json")
    ok(rc == 0, o)
    d = json.loads(o)
    ok(d["windows"][0]["maker_minutes"] == 180 and d["windows"][0]["not_counted_minutes"] == 90, str(d))
    ctx.say("windows, non-maker rows, --days and --json behave")


@test("hours_encodings", "Windows-style files: UTF-8 BOM, UTF-16 BOM, CRLF, blank rows, Windows-1252")
def _(ctx):
    h = "date,shot_or_chapter,activity,minutes,who,note\r\n"
    row = "2026-10-19,-,learn,570,maker,x\r\n"
    rc, o = hours(ctx, (h + row + ",,,,,\r\n\r\n").encode("utf-8-sig"), "--week-start", "2026-10-19", binary=True)
    ok(rc == 0, o); has(o, "9.5 h", "UTF-8 with BOM")
    rc, o = hours(ctx, (h + row).encode("utf-16"), "--week-start", "2026-10-19", binary=True)
    ok(rc == 0, o); has(o, "9.5 h", "UTF-16")
    rc, o = hours(ctx, (h + row.replace(",x", ",caf\u00e9")).encode("cp1252"), "--week-start", "2026-10-19", binary=True)
    ok(rc == 0, o); has(o, "9.5 h", "Windows-1252")
    rc, o = hours(ctx, h + row, "--week-start", "2026-10-19")
    ok(rc == 0, o); has(o, "9.5 h")
    ctx.say("4 encodings read; the CSV with CRLF and blank rows is accepted")
    ctx.unverified.append("Excel/Notepad save behaviour (BOM, date reformatting) on the maker's PC is UNVERIFIED; "
                          "the encodings above are simulated with bytes written here")


@test("hours_note_never_printed", "the note column is never printed, and only the file's base name appears")
def _(ctx):
    secret = "zqx" + "marker" + "note"
    text = "date,shot_or_chapter,activity,minutes,who,note\n2026-10-19,-,learn,30,maker,%s\n" % secret
    rc, o = hours(ctx, text, "--week-start", "2026-10-19")
    ok(rc == 0, o); lacks(o, secret, ctx.tmp)
    rc, o = hours(ctx, text, "--week-start", "2026-10-19", "--json")
    ok(rc == 0, o); lacks(o, secret, ctx.tmp)
    rc, o = hours(ctx, text.replace("learn", "Learn"))
    ok(rc == 1, o); lacks(o, secret, ctx.tmp)
    ctx.say("note text and temp paths absent from text, JSON and error output")


@test("hours_enum_parity", "the activity enum equals the enum in research/production-scale-fixtures/hours.csv and the plan")
def _(ctx):
    fixture = read("research/production-scale-fixtures/hours.csv")
    m = re.search(r"enum activity: ([a-zA-Z0-9_|]+)", fixture)
    ok(m, "the reference fixture has no enum line")
    ref = m.group(1).split("|")
    import importlib.util
    spec = importlib.util.spec_from_file_location("hours_report_mod", os.path.join(ROOT, "scripts", "hours_report.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(mod)
    ok(mod.ACTIVITIES == ref, "enum differs:\n%s\n%s" % (mod.ACTIVITIES, ref))
    ok(len(ref) == 20 and "event" in ref, "expected 20 activities including event (W-12)")
    ctx.say("20 activities equal to the production-scale reference")


# ======================================================================= ops_lint

@test("lint_real", "ops_lint.py on the real ops files exits 0", needs_patterns=True)
def _(ctx):
    need_patterns()
    rc, o = ctx.lint()
    ok(rc == 0, o)
    has(o, "ops_lint: PASS")
    ctx.say(o.strip())
    if USING_OVERRIDE:
        ctx.notes.append("run with LJ_PATTERNS override, not scripts/redaction_patterns.json")


@test("lint_bad_note", "ops_lint --hours hours_bad_note.csv: exit 1, line + category (e-mail, profile path, deny-list name), masked", needs_patterns=True)
def _(ctx):
    need_patterns()
    rc0, o0 = ctx.run(["tests/ops/make_fixtures.py"])
    ok(rc0 == 0, o0)
    try:
        rc, o = ctx.lint("--hours", "tests/ops/fixtures/hours_bad_note.csv")
    finally:
        if not os.environ.get("LJ_KEEP_FIXTURES"):
            ctx.run(["tests/ops/make_fixtures.py", "--clean"])
    ok(rc == 1, o)
    has(o, "hours_bad_note.csv:2 [email]", "hours_bad_note.csv:3 [profile_path", "hours_bad_note.csv:4 [local_deny]",
        "hours_bad_note.csv:5 [ipv4]", "hours_bad_note.csv:6 [handle]", "WARN hours_bad_note.csv:7 [note_length]")
    # masked: first two characters and asterisks, never the full value
    planted = ["invalid@" + "mailbox", "qzx" + "user", "Qzx" + "plorp", "172" + ".16", "qzx" + "_handle"]
    lacks(o, *planted)
    ok(re.search(r"\[email\] note: masked hit pa\*+", o), "e-mail not masked as 'pa***'")
    ok(re.search(r"\[local_deny\] note: masked hit Qz\*+", o), "deny-list name not masked as 'Qz***'")
    ctx.say(o.strip())


@test("lint_clean_hours", "hours_9h30.csv and hours_7h30.csv pass the note check", needs_patterns=True)
def _(ctx):
    need_patterns()
    for f in ("hours_9h30.csv", "hours_7h30.csv"):
        rc, o = ctx.lint("--hours", "tests/ops/fixtures/" + f)
        ok(rc == 0, o); has(o, "PASS")
    rc, o = ctx.lint("--hours", "ops/hours.csv"); ok(rc == 0, o)
    ctx.say("both fixtures and ops/hours.csv pass")


@test("lint_note_length", "a note over 80 characters is a WARNING (exit 0), and fails under --strict")
def _(ctx):
    long_note = "x" * 81
    p = ctx.write("long.csv", "date,shot_or_chapter,activity,minutes,who,note\n2026-10-19,-,learn,30,maker,%s\n" % long_note)
    rc, o = ctx.lint("--hours", p); ok(rc == 0, o); has(o, "WARN", "note_length", "81 characters")
    rc, o = ctx.lint("--hours", p, "--strict"); ok(rc == 1, o)
    p80 = ctx.write("ok80.csv", "date,shot_or_chapter,activity,minutes,who,note\n2026-10-19,-,learn,30,maker,%s\n" % ("x" * 80))
    rc, o = ctx.lint("--hours", p80, "--strict"); ok(rc == 0, o); lacks(o, "WARN")
    ctx.say("81 chars warns, 80 chars does not")


def edit(repo, rel, old, new, count=1):
    p = os.path.join(repo, rel)
    t = open(p, encoding="utf-8").read()
    ok(old in t, "test setup: %r not found in %s" % (old, rel))
    open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new, count))


@test("lint_neg_card", "negative: card without Phone / with an invented ID / without the Language line / signed with <date>")
def _(ctx):
    cases = [
        ("no phone row", "| **Phone** (D-27)", "| **Handset** (D-27)", ["Phone", "card_row"]),
        ("no D-27 in the row", "| D-27 |", "| D-26 |", ["D-27"]),
        ("invented ID", "(O-14)", "(W-99)", ["W-99", "cited_id"]),
        ("no language line", "Caption and font test ran in:", "Caption and font was run in:", ["card_language"]),
        ("no NOT TESTED", "NOT TESTED until", "tested until", ["NOT TESTED"]),
        ("signed yes with placeholder", "signed: no", "signed: yes", ["signed: yes"]),
        ("no TD-4", "**TD-4 DCP / venue file**", "**Venue file**", ["TD-4"]),
        ("wrong value", "1920x1080, 16:9.", "1280x720, 16:9.", ["1920x1080"]),
        ("no UNVERIFIED", "UNVERIFIED", "unchecked", ["UNVERIFIED"]),
    ]
    for name, old, new, needles in cases:
        repo = ctx.clone()
        edit(repo, "ops/SETTINGS-CARD.md", old, new, count=99)
        rc, o = ctx.lint(root=repo)
        ok(rc == 1, "%s: exit %d: %s" % (name, rc, o)); has(o, *needles)
    ctx.say("%d card mutations, each exit 1 naming the problem" % len(cases))


@test("lint_card_scripts", "the card's tested-script claim is cross-checked with pipeline/phone/test_strings.json when that file exists")
def _(ctx):
    repo = ctx.clone()
    rc, o = ctx.lint(root=repo); ok(rc == 0, o); has(o, "not cross-checked")
    ts = os.path.join(repo, "pipeline", "phone")
    os.makedirs(ts)
    good = {"schema": "lj-teststrings/1", "scripts": {"latin": {"strings": [{"id": "lat-test"}]},
            "devanagari": {"strings": [{"id": "dev-digits"}]}, "tamil": {"status": "pending_O-10", "strings": []}}}
    open(os.path.join(ts, "test_strings.json"), "w", encoding="utf-8").write(json.dumps(good))
    rc, o = ctx.lint(root=repo); ok(rc == 0, o); lacks(o, "not cross-checked")
    bad = json.loads(json.dumps(good)); bad["scripts"]["devanagari"]["strings"] = []
    open(os.path.join(ts, "test_strings.json"), "w", encoding="utf-8").write(json.dumps(bad))
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "card_scripts", "devanagari")
    open(os.path.join(ts, "test_strings.json"), "w", encoding="utf-8").write("{broken")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "card_scripts")
    ctx.say("absent: noted; devanagari with strings: pass; without strings or broken file: exit 1")


@test("lint_neg_gather", "negative: GATHER without the gate / a stand-in ID / with a stand-in in Part B / a real-box ID in Part A")
def _(ctx):
    cases = [
        ("no gate", "**Gate: nothing", "**Rule: nothing", ["gather_gate"]),
        ("missing stand-in", "`LJ-ST-0003-F`", "`LJ-ST-0003-X`", ["LJ-ST-0003-F"]),
        ("no Part B heading", "## Part B: From Sun 15 Nov, only after P-LOCK passes", "## Later", ["gather_parts"]),
        ("stand-in in Part B", "| photo | `LJ-<box>-<nnnn>-F` |", "| photo | `LJ-ST-0009-F` |", ["Part B", "LJ-ST-0009-F"]),
        ("real box in Part A", "| [ ] | `LJ-ST-0005-F` |", "| [ ] | `LJ-B03-0005-F` |", ["before P-LOCK", "LJ-B03-0005-F"]),
        ("invented ID", "(O-06)", "(O-96)", ["O-96"]),
    ]
    for name, old, new, needles in cases:
        repo = ctx.clone()
        if name == "real box in Part A":
            edit(repo, "ops/GATHER.md", "| [ ] | `LJ-ST-0005-F` | `LJ-ST-0005-B` |", "| [ ] | `LJ-B03-0005-F` | `LJ-ST-0005-B` |")
        elif name == "invented ID":
            edit(repo, "ops/GATHER.md", "| O-06 |", "| O-96 |")
        else:
            edit(repo, "ops/GATHER.md", old, new)
        rc, o = ctx.lint(root=repo)
        ok(rc == 1, "%s: exit %d: %s" % (name, rc, o)); has(o, *needles)
    ctx.say("%d GATHER mutations, each exit 1 naming the problem" % len(cases))


@test("lint_neg_howto_marker", "negative: HOURS-HOWTO without the 'no names in note' sentence; an unfinished-work marker")
def _(ctx):
    repo = ctx.clone()
    edit(repo, "ops/HOURS-HOWTO.md", "No names in note: IDs and relation tokens only; `who` is `maker` or `agent`, nothing else.", "Keep notes short.")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "howto_content", "no names in note")
    repo = ctx.clone()
    edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when " + "TO" + "DO")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "placeholder_marker")
    ctx.say("both mutations: exit 1")


@test("lint_neg_planted_text", "negative: identifying strings planted in the ops files are found, with file:line and a masked hit", needs_patterns=True)
def _(ctx):
    need_patterns()
    email = "pat" + "." + "invalid" + "@" + "mailbox-" + "nowhere" + "." + "example"
    ip = "172" + "." + "16" + "." + "4" + "." + "9"
    path = "C:" + "\\" + "Users" + "\\" + "qzxuser" + "\\" + "Desktop"
    handle = "@" + "qzx" + "_handle"
    for name, planted, cat in [("email", email, "email"), ("ip", ip, "ipv4"), ("path", path, "profile_path_windows"), ("handle", handle, "handle")]:
        repo = ctx.clone()
        edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nContact: " + planted)
        rc, o = ctx.lint(root=repo)
        ok(rc == 1, "%s: exit %d: %s" % (name, rc, o))
        has(o, "ops/GATHER.md:3 [%s]" % cat)
        lacks(o, planted)
    more = [("ipv6", ":".join(["2a02", "6b8", "0", "0", "0", "0", "0", "1"]), "ipv6"),
            ("mac", ":".join(["02", "1a", "2b", "3c", "4d", "5e"]), "mac"),
            ("linux path", "/home/" + "qzxuser" + "/scans", "profile_path_linux"),
            ("token", "ghp" + "_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8", "token_shape"),
            ("guid", "123e4567-" + "e89b-" + "12d3-" + "a456-" + "426614174000", "guid_serial"),
            ("65-hex", "0123456789abcdef" * 4 + "0", "guid_serial")]
    for name, planted, cat in more:
        repo = ctx.clone()
        edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nContact: " + planted)
        rc, o = ctx.lint(root=repo)
        ok(rc == 1, "%s: exit %d: %s" % (name, rc, o))
        has(o, "ops/GATHER.md:3 [%s]" % cat)
        lacks(o, planted)
    # a 64-character SHA-256 is public build identity and must NOT be flagged (4.13 exemption)
    repo = ctx.clone()
    edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nChecksum: " + "0123456789abcdef" * 4)
    rc, o = ctx.lint(root=repo); ok(rc == 0, "a 64-hex SHA-256 must pass: " + o)
    # other ops files are scanned too (here a hostile README)
    repo = ctx.clone()
    open(os.path.join(repo, "ops", "README.md"), "w", encoding="utf-8").write("see " + email + "\n")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "ops/README.md:1 [email]")
    ctx.say("e-mail, IPv4, IPv6, MAC, Windows and Linux profile paths, token, GUID, 65-hex run and handle planted: each found at its line, masked; a 64-hex SHA-256 passes")


@test("lint_pattern_samples", "ops_lint's reading of the pattern file agrees with the file's own positive/negative samples", needs_patterns=True)
def _(ctx):
    need_patterns()
    import importlib.util
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("ops_lint_mod", os.path.join(ROOT, "scripts", "ops_lint.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pat = mod.Patterns(PATTERN_FILE)
    join = lambda x: "".join(x) if isinstance(x, list) else str(x)
    checked = bad = 0
    problems = []
    for cid, _rx, c in pat.categories:
        for smp in c.get("positive_samples") or []:
            checked += 1
            if cid not in [h[0] for h in pat.scan_line(join(smp))]:
                problems.append("positive sample of %s not flagged" % cid)
        for smp in c.get("negative_samples") or []:
            checked += 1
            if cid in [h[0] for h in pat.scan_line(join(smp))]:
                problems.append("negative sample of %s flagged" % cid)
    if checked == 0 and USING_OVERRIDE:
        raise Skip("the development pattern file (LJ_PATTERNS) carries no samples; the real file must")
    ok(checked > 0, "the pattern file has no samples to compare with")
    ok(not problems, "; ".join(problems[:10]))
    ctx.say("%d samples in %d text categories behave as declared" % (checked, len(pat.categories)))


@test("lint_deny_list", "deny list: whole word, case-insensitive, short entries skipped, --deny-file and LJ_DENY_FILE honoured")
def _(ctx):
    name = "Qzx" + "plorp"
    deny = ctx.write("deny.txt", "# comment\n%s\nab\n" % name)
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    hit = ctx.write("hit.csv", h + "2026-10-19,-,learn,30,maker,met %s at the shop\n" % name.lower())
    near = ctx.write("near.csv", h + "2026-10-19,-,learn,30,maker,met %sish people about ab and cab\n" % name)
    rc, o = ctx.lint("--hours", hit, "--deny-file", deny); ok(rc == 1, o); has(o, "hit.csv:2 [local_deny]", "masked hit Qz", "under 3 characters"); lacks(o, name.lower())
    rc, o = ctx.lint("--hours", near, "--deny-file", deny); ok(rc == 0, "a longer word must not match: " + o)
    rc, o = ctx.lint("--hours", hit); ok(rc == 0, "without a deny list the note is clean: " + o)
    env_rc, env_out = ctx.run(["scripts/ops_lint.py", "--hours", hit, "--patterns", ctx.patterns()],
                              extra_env={"LJ_DENY_FILE": deny})
    ok(env_rc == 1, env_out); has(env_out, "local_deny")
    deny16 = ctx.write("deny16.txt", ("# notepad\r\n%s\r\n" % name).encode("utf-16"), binary=True)
    rc, o = ctx.lint("--hours", hit, "--deny-file", deny16); ok(rc == 1, "UTF-16 deny list not read: " + o); has(o, "local_deny")
    deny1252 = ctx.write("deny1252.txt", ("caf\u00e9\r\n%s\r\n" % name).encode("cp1252"), binary=True)
    rc, o = ctx.lint("--hours", hit, "--deny-file", deny1252); ok(rc == 1, "ANSI deny list not read: " + o); has(o, "local_deny")
    ctx.say("deny list behaviour verified: whole word, case-insensitive, short entries skipped, flag, env var, UTF-16 and ANSI files")


@test("lint_fail_closed", "fail closed: missing, invalid or incomplete pattern file exits 2 and checks nothing")
def _(ctx):
    for name, content in [("missing", None), ("badjson", "{not json"), ("nocats", "{}"),
                          ("badregex", json.dumps({"categories": [{"id": "email", "regex": "(", "scope": "both"}]})),
                          ("incomplete", json.dumps({"categories": [{"id": "email", "regex": "x", "scope": "both"}]}))]:
        p = os.path.join(ctx.tmp, name + ".json")
        if content is not None:
            open(p, "w", encoding="utf-8").write(content)
        rc, o = ctx.run(["scripts/ops_lint.py", "--patterns", p])
        ok(rc == 2, "%s: exit %d: %s" % (name, rc, o)); has(o, "FAIL CLOSED")
    ctx.say("five unusable pattern files: exit 2 each")


@test("lint_data_driven", "patterns come from the file: a tiny synthetic pattern file changes what is flagged (no regex inside ops_lint)")
def _(ctx):
    cats = []
    for cid in ["email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux", "token_shape", "guid_serial", "handle"]:
        cats.append({"id": cid, "scope": "both", "action": "refuse", "regex": "ZZNEVER" + cid.upper(), "flags": ""})
    cats[0]["regex"] = "zzflagme[a-z]*"          # the only category that can match
    cats.append({"id": "custom_probe", "scope": "text", "action": "refuse", "regex": "probeword[0-9]+", "flags": "i"})
    pf = ctx.write("mini.json", json.dumps({"schema": "synthetic", "version": "mini", "categories": cats, "mask": {"keep": 3, "fill": "#"}}))
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    p = ctx.write("m.csv", h + "2026-10-19,-,learn,30,maker,here is zzflagmeplease and PROBEWORD77\n"
                  "2026-10-19,-,learn,30,maker,someone" + "@" + "elsewhere" + ".example is not flagged by this file\n")
    rc, o = ctx.run(["scripts/ops_lint.py", "--patterns", pf, "--hours", p])
    ok(rc == 1, o)
    has(o, "m.csv:2 [email]", "m.csv:2 [custom_probe]", "masked hit zzf###", "masked hit PRO###")
    lacks(o, "m.csv:3")
    ctx.say("the mini file flagged only what it defines; the mask settings came from the file as well")


@test("lint_readonly", "ops_lint, hours_report and decisions_to_csv --check modify nothing in the repository")
def _(ctx):
    files = []
    for d in ("ops", "scripts"):
        for dp, _dn, fn in os.walk(os.path.join(ROOT, d)):
            if "__pycache__" in dp:
                continue
            files += [os.path.join(dp, f) for f in fn]
    before = {f: sha(f) for f in files}
    ctx.run(["scripts/hours_report.py", "ops/hours.csv"])
    ctx.run(["scripts/decisions_to_csv.py", "--check", "ops/decisions.csv"])
    if os.path.isfile(PATTERN_FILE) or USING_OVERRIDE:
        ctx.lint()
    after = {f: sha(f) for f in files}
    ok(before == after, "files changed: %s" % [f for f in before if before[f] != after.get(f)])
    ctx.say("%d files hashed before and after: identical" % len(files))


# ======================================================================= the documents

@test("card_content", "SETTINGS-CARD: TD-1..TD-4, Phone, D-27, Language and script line, signed: no, every cited ID exists")
def _(ctx):
    t = read("ops/SETTINGS-CARD.md")
    for n in ["TD-1", "TD-2", "TD-3", "TD-4", "Phone", "D-27", "Language and script", "Caption and font test ran in:", "NOT TESTED",
              "signed: no", "UNVERIFIED", "Proposed (J)"]:
        ok(n in t, "card lacks %r" % n)
    ok("WP-08 may refine the numbers before Sun 1 Nov" in t and "pipeline/phone/PHONE-ROW.md" in t, "phone row paste instruction")
    ids = set(register_ids())
    cited = set("%s-%s" % m for m in re.findall(r"\b([DWOS])-([0-9]{2})\b", t))
    ok(cited and cited <= ids, "cited IDs not in the register: %s" % sorted(cited - ids))
    for rid in ["W-14", "W-15", "W-16", "W-17", "W-18", "W-19", "D-27", "O-14", "O-15", "W-57"]:
        ok(rid in cited, "%s should be cited" % rid)
    ok(not re.search(r"25 ?fps|-1\.5 ?dBTP|fps=25", t), "stale value in the card")
    ctx.say("card cites %d register IDs, all present: %s" % (len(cited), ", ".join(sorted(cited))))


@test("howto_gather_content", "HOURS-HOWTO has the 'no names in note' sentence; GATHER has Part A/Part B, the gate, five stand-in scans, IDs only")
def _(ctx):
    h = read("ops/HOURS-HOWTO.md")
    ok("No names in note: IDs and relation tokens only" in h, "the sentence is missing")
    sent = [x for x in re.split(r"(?<=[.])\s+", h.replace("\n", " ")) if "No names in note" in x][0]
    ok("`maker`" in sent and "`agent`" in sent, "the who rule must be in the same sentence as the no-names rule")
    ok(len(h.split("\n")) <= 60 and len(h.split()) <= 800, "one page: %d lines, %d words" % (len(h.split("\n")), len(h.split())))
    for a in ["gather|scan|story", "brief_G0", "style_G1", "review_G2", "craft_refine_G3", "chapter_G4", "dignity_G5", "tech_G6", "event"]:
        ok(a.split("|")[0] in h, "activity %s not explained" % a)
    g = read("ops/GATHER.md")
    for n in ["## Part A", "## Part B", "**Gate:", "P-LOCK", "Sun 15 Nov", "D-02", "D-13", "D-15", "D-17", "W-49", "D-04"]:
        ok(n in g, "GATHER lacks %r" % n)
    for i in range(1, 6):
        ok("LJ-ST-%04d-F" % i in g and "LJ-ST-%04d-B" % i in g, "stand-in %d" % i)
    for n in ["O-06", "O-07", "O-08", "O-09", "O-10", "O-11", "DEV-01", "OBJ-01", "REC-01"]:
        ok(n in g, "GATHER lacks %r" % n)
    for n in ["id", "class", "holder", "cloud", "consent_state", "allowed_use", "as_found_photographed", "scanned", "returned"]:
        ok("`%s`" % n in g, "Part B field %s" % n)
    ctx.say("HOURS-HOWTO %d lines, %d words; GATHER structure present" % (len(h.split("\n")), len(h.split())))


@test("ops_hygiene", "ops files: no stale values, no D-28 exclusions, no Minecraft, no names/emails/IPs by a plain look (patterns checked by ops_lint)")
def _(ctx):
    stale = re.compile(r"fps=25|\b25 ?fps\b|-1\.5 ?dBTP|TP=-1\.5|L1 process lock|L1 lock|S1[-\u2013]S5|spikes? S1|25-minute|Minecraft|voxel|Mojang", re.I)
    theme = re.compile(r"\b(Mughal|Islamic|mosque|minaret|Taj Mahal|Red Fort|church|cathedral|crucifix|nativity|Christmas)\b", re.I)
    for f in ["ops/HOURS-HOWTO.md", "ops/GATHER.md", "ops/SETTINGS-CARD.md", "ops/hours.csv", "ops/gate_log.csv"]:
        t = read(f)
        m = stale.search(t); ok(not m, "%s has a stale value: %r" % (f, m and m.group(0)))
        m = theme.search(t); ok(not m, "%s has a D-28 exclusion: %r" % (f, m and m.group(0)))
        ok("\r" not in t, "%s must use LF line endings" % f)
    for f in ["ops/decisions.csv", "ops/gate_log.csv", "ops/hours.csv"]:
        ok(not open(os.path.join(ROOT, f), "rb").read().startswith(b"\xef\xbb\xbf"), "%s must have no BOM" % f)
    ok(read("ops/gate_log.csv") == "date,gate_id,runtime_before_min,runtime_after_min,trigger,measured_value,hours_per_week_H,decision_text,who\n",
       "gate_log.csv must be the header only, with the production-scale gate-decision schema")
    ref = read("research/production-scale-fixtures/decisions.csv").split("\n")[0]
    ok(ref == read("ops/gate_log.csv").strip(), "gate_log header must equal research/production-scale-fixtures/decisions.csv header")
    ok(read("research/production-scale-fixtures/hours.csv").split("\n")[0] == read("ops/hours.csv").strip(), "hours header parity")
    ctx.say("5 documents checked; gate_log and hours headers equal the production-scale fixtures")


@test("scripts_compile", "the three scripts compile and print --help (usage exits 0)")
def _(ctx):
    for s in ("hours_report", "decisions_to_csv", "ops_lint"):
        src = open(os.path.join(ROOT, "scripts", s + ".py"), encoding="utf-8").read()
        compile(src, s, "exec")
        ok(src.startswith("#!/usr/bin/env python3\n\"\"\""), "%s lacks the header comment (what it does, how to run, what it prints)" % s)
        rc, o = ctx.run(["scripts/%s.py" % s, "--help"]); ok(rc == 0 and "usage" in o.lower(), o)
    ctx.say("3 scripts compile; headers present; --help exits 0")


@test("public_lint_own_files", "scripts/public_lint.py (WP-03), when present, finds nothing in WP-02's own files")
def _(ctx):
    pl = os.path.join(ROOT, "scripts", "public_lint.py")
    if not os.path.isfile(pl):
        raise Skip("scripts/public_lint.py has not landed (WP-03); ops_lint scans ops/ with the same pattern file")
    rc, o = ctx.run(["scripts/public_lint.py", "--paths", "ops", "scripts/ops_lint.py", "scripts/hours_report.py",
                     "scripts/decisions_to_csv.py", "tests/ops", "build/evidence/wp02"])
    ok(rc == 0, o)
    ctx.say(o.strip()[-400:])


@test("card_commands_linux", "the settings-card ffprobe/ffmpeg commands give the printed answers on tiny test files (Linux)", quick=False)
def _(ctx):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise Skip("ffmpeg/ffprobe not installed")
    if avail_mb() < 60:
        raise Skip("less than 60 MB free on the shared volume; the (about 2 MB) test files were not made")
    d = ctx.tmp

    def sh(cmd):
        p = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
        ctx.log.append((" ".join(cmd).replace(d, "<tmp>"), p.returncode, (p.stdout or "") + (p.stderr or "")))
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    rc, o = sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x336699:size=1920x1080:rate=24,format=yuv422p10le",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000", "-t", "0.25", "-c:v", "prores_ks", "-profile:v", "3",
                "-c:a", "pcm_s24le", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "master.mov"])
    ok(rc == 0, o)
    rc, o = sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x336699:size=1920x1080:rate=24,format=yuv420p",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000", "-t", "1", "-c:v", "libx264", "-profile:v", "high",
                "-level", "4.1", "-crf", "18", "-c:a", "aac", "-b:a", "256k", "-ac", "2", "-color_range", "tv", "-colorspace", "bt709",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", "venue.mp4"])
    ok(rc == 0, o)
    rc, o = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name,width,height,pix_fmt", "-of", "csv=p=0", "master.mov"])
    ok(o.strip() == "prores,1920,1080,yuv422p10le", "TD-1 command printed %r" % o)
    rc, o = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate,avg_frame_rate", "-of", "csv=p=0", "venue.mp4"])
    ok(o.strip() == "24/1,24/1", "TD-2 command printed %r" % o)
    rc, o = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name,profile,level,pix_fmt", "-of", "default=nw=1", "venue.mp4"])
    ok(sorted(o.split()) == sorted(["codec_name=h264", "profile=High", "level=41", "pix_fmt=yuv420p"]), "TD-4 command printed %r" % o)
    rc, o = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_range,color_space,color_primaries,color_transfer", "-of", "default=nw=1", "venue.mp4"])
    ok(sorted(o.split()) == sorted(["color_range=tv", "color_space=bt709", "color_primaries=bt709", "color_transfer=bt709"]), "colour command printed %r" % o)
    rc, o = sh(["ffmpeg", "-nostats", "-i", "venue.mp4", "-af", "ebur128=peak=true", "-f", "null", "-"])
    ok(rc == 0 and "I:" in o and "Peak:" in o, "sound command did not print I: and Peak:")
    rc, o = sh(["ffmpeg", "-v", "error", "-y", "-ss", "0.2", "-i", "venue.mp4", "-frames:v", "1", "check.png"])
    ok(rc == 0 and os.path.getsize(os.path.join(d, "check.png")) > 0, "caption frame command")
    ctx.say("TD-1 prores,1920,1080,yuv422p10le; TD-2 24/1,24/1; TD-4 h264/High/41/yuv420p; colour tv+bt709x3; sound I:/Peak: printed; frame grab ok")
    ctx.unverified.append("the same commands on the maker's Windows PC (winget ffmpeg build) are UNVERIFIED until the PC check and colour-patch runner have run there (W-28)")


@test("windows_unverified", "Windows behaviour of the WP-02 files (Excel handling of hours.csv, py -3 -I on PowerShell 5.1/7) is UNVERIFIED", quick=True)
def _(ctx):
    ctx.unverified += [
        "py -3 -I scripts\\hours_report.py on Windows PowerShell 5.1 and PowerShell 7 was not run (no Windows here); the script is standard-library Python",
        "Excel / Notepad behaviour when the maker edits ops/hours.csv (date reformatting, BOM, UTF-16, ANSI) is simulated by bytes in hours_encodings, not observed",
        "the card commands on the maker's winget ffmpeg build are UNVERIFIED (W-28)",
    ]
    raise Skip("UNVERIFIED by design: see unverified_reasons")


# ======================================================================= runner

def write_evidence(tid, status, ctx, expected, actual, notes, unverified, a0, a1, amin):
    if not os.path.isdir(EVID):
        os.makedirs(EVID, exist_ok=True)
    env = {"platform": "linux", "python": "%d.%d.x" % sys.version_info[:2], "nproc": os.cpu_count()}
    ff = shutil.which("ffmpeg")
    if ff and tid == "card_commands_linux":
        try:
            first = subprocess.run([ff, "-version"], capture_output=True, text=True).stdout.split("\n")[0]
            env["ffmpeg"] = first.split()[2].split("-")[0]
        except (OSError, IndexError):
            pass
    doc = {"schema": "lj-evidence/1", "package": PACKAGE, "test": tid,
           "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
           "status": status, "env": env,
           "disk": {"avail_mb_start": a0, "planned_write_mb": 0, "avail_mb_min": amin, "avail_mb_end": a1,
                    "floor_mb": 400, "hard_floor_mb": 250},
           "expected": expected, "actual": actual, "notes": notes, "unverified_reasons": unverified}
    if USING_OVERRIDE and tid.startswith("lint"):
        doc["notes"] = (notes + " " if notes else "") + "ran against a development pattern file (LJ_PATTERNS), not the real scripts/redaction_patterns.json"
    with open(os.path.join(EVID, tid + ".json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--quick", action="store_true")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-evidence", action="store_true")
    args = ap.parse_args(argv)
    if args.list:
        for t in TESTS:
            print("%-28s %s%s" % (t["id"], "" if t["quick"] else "[--all] ", t["title"]))
        return 0
    if args.only:
        selected = [t for t in TESTS if t["id"] == args.only]
    else:
        selected = [t for t in TESTS if t["quick"] or not args.quick]
    if args.only and not selected:
        print("no such test: %s" % args.only, file=sys.stderr)
        return 2
    transcript = []
    counts = {}
    for t in selected:
        ctx = Ctx(t["id"])
        a0 = avail_mb()
        status, actual, err = "PASS", "", ""
        try:
            t["fn"](ctx)
            actual = " | ".join(ctx.said)
            if ctx.unverified and t["id"] == "windows_unverified":
                status = "UNVERIFIED"
        except Skip as exc:
            if ctx.unverified:
                status, actual = "UNVERIFIED", str(exc)
            else:
                status, actual = "SKIPPED", str(exc)
        except Blocked as exc:
            status, actual, err = "BLOCKED", str(exc), str(exc)
        except AssertionError as exc:
            status, actual, err = "FAIL", str(exc)[:1500], str(exc)
        except Exception as exc:  # a crash in a test is a failure of the test, not of the tool
            status, actual, err = "FAIL", "%s: %s" % (type(exc).__name__, exc), str(exc)
        a1 = avail_mb()
        counts[status] = counts.get(status, 0) + 1
        line = "%-10s %-28s %s" % (status, t["id"], t["title"])
        print(line)
        if status in ("FAIL", "BLOCKED"):
            for l in err.split("\n")[:12]:
                print("           " + ctx._show(l))
        if getattr(ctx, "used_mini", False):
            ctx.notes.append("ran with a synthetic mini pattern file because scripts/redaction_patterns.json is absent (mechanism test only)")
        for n in ctx.notes:
            print("           note: " + n)
        transcript.append("=" * 78)
        transcript.append("%s  %s" % (status, t["id"]))
        transcript.append(t["title"])
        for cmd, rc, out in ctx.log:
            transcript.append("$ " + cmd)
            body = ctx._show(out).rstrip("\n").split("\n")
            if len(body) > 40:
                body = body[:30] + ["... (%d more lines)" % (len(body) - 30)]
            transcript += ["  " + l for l in body if l != ""] or ["  (no output)"]
            transcript.append("  [exit %d]" % rc)
        if status in ("FAIL", "BLOCKED"):
            transcript.append("  " + ctx._show(err).replace("\n", "\n  "))
        ctx.cleanup()
        if not args.no_evidence:
            write_evidence(t["id"], status, ctx, t["title"], ctx._show(actual), " ".join(ctx.notes), ctx.unverified, a0, a1, min(a0, a1))
    if not args.no_evidence and not args.only:
        os.makedirs(EVID, exist_ok=True)
        with open(os.path.join(EVID, "transcript.txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("WP-02 test transcript (commands run from the repository root; outputs are the real outputs).\n")
            fh.write("\n".join(transcript) + "\n")
        with open(os.path.join(EVID, "summary.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"schema": "lj-evidence-summary/1", "package": PACKAGE,
                       "mode": "quick" if args.quick else "all", "counts": counts,
                       "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")}, fh, indent=1, sort_keys=True)
            fh.write("\n")
    print("-" * 60)
    print("WP-02 ops tests (%s): %s" % ("quick" if args.quick else "all", ", ".join("%d %s" % (v, k) for k, v in sorted(counts.items()))))
    bad = counts.get("FAIL", 0) + counts.get("BLOCKED", 0)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
