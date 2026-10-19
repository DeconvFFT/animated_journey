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


_D2C = []


def d2c_module():
    """scripts/decisions_to_csv.py, loaded only for its ONE definition of a register row (ROW_RE);
    ops_lint.py reads the same definition, so the tests no longer carry copies of it."""
    if not _D2C:
        import importlib.util
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("lj_decisions_to_csv", os.path.join(ROOT, "scripts", "decisions_to_csv.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _D2C.append(mod)
    return _D2C[0]


def register_ids():
    """Every register ID, one per line the shared row pattern matches (annotated ID cells included)."""
    rx = d2c_module().ROW_RE
    ids = []
    for line in read("DECISIONS.md").split("\n"):
        m = rx.match(line)
        if m:
            ids.append("%s-%s" % (m.group(1), m.group(2)))
    return ids


def loose_row_count(text):
    """An independent, deliberately dumb count: lines that START like a register row (`| O-6...`,
    also `| **O-6**` and `` | `O-6` ``). It does not share the row pattern, so a pattern that
    silently drops rows cannot also fool this."""
    return len(re.findall(r"^\|\s*[*_`~]*\s*[DWOS]-[0-9]", text, re.M))


def next_id(prefix):
    """The next unused register ID of a prefix (O-36 while the register ends at O-35), so the
    tests that add a row never depend on a snapshot of the register's size."""
    nums = [int(i[2:]) for i in register_ids() if i[0] == prefix]
    return "%s-%02d" % (prefix, max(nums) + 1)


def last_row_line(reg, prefix):
    """The register line of the last row with this prefix (an anchor to insert after)."""
    rx = d2c_module().ROW_RE
    return [l for l in reg.split("\n") if rx.match(l) and rx.match(l).group(1) == prefix][-1]


def make_fixtures_module():
    import importlib.util
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("lj_make_fixtures", os.path.join(ROOT, "tests", "ops", "make_fixtures.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pattern_mask():
    """The mask section of the pattern file in use: keep, fill, cap (public_lint's defaults when absent)."""
    with open(PATTERN_FILE, "r", encoding="utf-8") as fh:
        mk = (json.load(fh).get("mask") or {})
    return {"keep": int(mk.get("keep", 2)), "fill": str(mk.get("fill", "*")) or "*", "cap": int(mk.get("cap", 8))}


def pattern_files():
    """The real pattern file first (the planted strings follow WP-03's file), then the override."""
    return [os.path.join(ROOT, "scripts", "redaction_patterns.json"), PATTERN_FILE]


def planted_email():
    """The first positive sample of the email category, joined: a non-reserved shape that the
    pattern file does flag. It is read from the file so the fixture can not drift from its exemptions."""
    return make_fixtures_module().email_sample(*pattern_files())


def exempt_email():
    """An address the pattern file exempts (reserved example domain), from its own negative samples."""
    return make_fixtures_module().email_sample(*pattern_files(), kind="negative_samples", need="@")


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
    loose = loose_row_count(read("DECISIONS.md"))
    ok(loose == len(ids), "%d lines start like a register row but the row pattern found %d: a row is being dropped" % (loose, len(ids)))
    c = {k: sum(1 for i in ids if i[0] == k) for k in "DWOS"}
    got = {k: sum(1 for r in rows if r["id"][0] == k) for k in "DWOS"}
    ok(c == got, "per-prefix counts differ: %s vs %s" % (c, got))
    ctx.say(out.strip())
    # the register, not a number written in the plan or in this test, sets the count
    has(out, "%d rows (D %d, W %d, O %d, S %d" % (len(ids), c["D"], c["W"], c["O"], c["S"]))
    ctx.say("live register: %d rows (D %d, W %d, O %d, S %d); the CSV and the --check output agree"
            % (len(ids), c["D"], c["W"], c["O"], c["S"]))


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
    ok(all(r["status"] in ("decided", "superseded") for i, r in rows.items() if i[0] == "D"), "D rows")
    ok(all(r["status"] == "default" for i, r in rows.items() if i[0] == "W"), "W rows are defaults")
    ok(all(r["status"] in ("applied", "outstanding") for i, r in rows.items() if i[0] == "S"), "S rows carry the Table 4 status")
    # expectations derived from the register text itself (a plain split, not the generator's parser)
    want_out, want_pend, want_ans = set(), set(), set()
    for line in read("DECISIONS.md").split("\n"):
        m = d2c_module().ROW_RE.match(line)
        if not m or m.group(1) not in "SO":
            continue
        rid = "%s-%s" % (m.group(1), m.group(2))
        cells = [c.strip() for c in line[m.end():].split("|")]  # the cells after the ID cell
        if rid[0] == "S" and cells[-2].lower().startswith("**outstanding"):
            want_out.add(rid)
        if rid[0] == "O":
            if cells[0].lower().startswith("answered"):
                want_ans.add(rid)
            elif cells[1].startswith("**(pending"):
                want_pend.add(rid)
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
    current = register_ids()
    new_id = next_id("O")  # O-36 while the register ends at O-35; computed, not a snapshot
    n_o = sum(1 for i in current if i[0] == "O")
    anchor = last_row_line(reg, "O")
    new = anchor + "\n| %s | Sun 1 Nov | A synthetic test question? | A synthetic recommendation. |" % new_id
    p = ctx.write("DECISIONS.md", reg.replace(anchor, new, 1))
    out = os.path.join(ctx.tmp, "g.csv")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", out, "--register", p]); ok(rc == 0, o)
    has(o, "%d rows" % (len(current) + 1), "O %d" % (n_o + 1))
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", p])
    ok(rc == 1, o); has(o, new_id, "missing")
    ctx.say("%d rows (live register %d + %s); the old CSV is reported stale" % (len(current) + 1, len(current), new_id))


@test("decisions_three_digit_id", "negative: a W-100 row in a register copy reaches the CSV (it was silently dropped when IDs had to be two digits)")
def _(ctx):
    reg = read("DECISIONS.md")
    current = register_ids()
    anchor = last_row_line(reg, "W")
    row = "| W-100 | A synthetic three-digit default | A synthetic value. | Sun 1 Nov | Maker | synthetic |"
    p = ctx.write("DECISIONS.md", reg.replace(anchor, anchor + "\n" + row, 1))
    n_w = sum(1 for i in current if i[0] == "W")
    out = os.path.join(ctx.tmp, "w100.csv")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", out, "--register", p]); ok(rc == 0, o)
    has(o, "%d rows" % (len(current) + 1), "W %d" % (n_w + 1))
    ok("W-100" in [r["id"] for r in csv_rows(out)], "W-100 did not reach the CSV")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", out, "--register", p]); ok(rc == 0, o)
    # the committed CSV is now stale: --check names W-100, and so does ops_lint's independent scan
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", p])
    ok(rc == 1, o); has(o, "W-100", "missing")
    repo = ctx.clone()
    shutil.copy(p, os.path.join(repo, "DECISIONS.md"))
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "W-100", "id_set")
    shutil.copy(out, os.path.join(repo, "ops", "decisions.csv"))
    rc, o = ctx.lint(root=repo); ok(rc == 0, "a CSV regenerated from the W-100 register must pass: " + o)
    # a three-digit ID cited in an ops document is checked against the register as well
    edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nSee W-101.")
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "W-101", "cited_id")
    ctx.say("W-100 reaches the CSV (%d rows), --check and ops_lint report it missing from a stale CSV and pass on a fresh one; a cited W-101 is flagged" % (len(current) + 1))


@test("decisions_annotated_id", "negative: an annotated ID cell (| O-NN (absorbs O-MM) |) reaches the CSV with the annotation in note; a row that cannot be parsed is exit 2, never dropped in silence")
def _(ctx):
    reg = read("DECISIONS.md")
    current = register_ids()
    n_o = sum(1 for i in current if i[0] == "O")
    n_w = sum(1 for i in current if i[0] == "W")
    oid, wid = next_id("O"), next_id("W")
    gone = "O-%02d" % (int(oid[2:]) + 1)  # the ID the annotation says was absorbed: not a register row
    o_anchor, w_anchor = last_row_line(reg, "O"), last_row_line(reg, "W")
    o_row = "| %s (absorbs %s) | Sun 1 Nov | A synthetic test question? | A synthetic recommendation. |" % (oid, gone)
    w_row = "| %s (revises W-05) | A synthetic default | A synthetic value. | Sun 1 Nov | Maker | synthetic |" % wid
    text = reg.replace(o_anchor, o_anchor + "\n" + o_row, 1)
    text = text.replace(w_anchor, w_anchor + "\n" + w_row, 1)
    p = ctx.write("annotated.md", text)
    ok(loose_row_count(text) == len(current) + 2, "test setup: the two synthetic rows were not inserted")
    out = os.path.join(ctx.tmp, "annotated.csv")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", out, "--register", p]); ok(rc == 0, o)
    has(o, "%d rows" % (len(current) + 2), "O %d" % (n_o + 1), "W %d" % (n_w + 1))
    rows = {r["id"]: r for r in csv_rows(out)}
    ok(oid in rows and wid in rows, "%s / %s did not reach the CSV" % (oid, wid))
    ok(rows[oid]["note"] == "absorbs " + gone and rows[oid]["status"] == "open", "O note/status: %r %r" % (rows[oid]["note"], rows[oid]["status"]))
    ok(rows[wid]["note"] == "revises W-05" and rows[wid]["status"] == "default", "W note/status: %r %r" % (rows[wid]["note"], rows[wid]["status"]))
    ok("(" not in rows[oid]["note"] and "(" not in rows[wid]["note"], "the parentheses must be stripped")
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", out, "--register", p]); ok(rc == 0, o)
    # the live register's own annotated ID cells: every annotation is in the committed CSV's note
    live = {r["id"]: r for r in csv_rows(os.path.join(ROOT, "ops", "decisions.csv"))}
    annotated = []
    for line in reg.split("\n"):
        m = re.match(r"^\|\s*([DWOS]-[0-9]{2,3})\s+\((.+?)\)\s*\|", line)  # independent of the shared row pattern
        if m:
            annotated.append(m.group(1))
            ok(live.get(m.group(1), {}).get("note", "").startswith(m.group(2).replace("**", "")),
               "%s: the annotation %r is not at the start of its note in ops/decisions.csv" % (m.group(1), m.group(2)))
    # the committed CSV is stale against the copy: --check and ops_lint name both new IDs
    rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", p])
    ok(rc == 1, o); has(o, oid, wid, "missing")
    repo = ctx.clone()
    shutil.copy(p, os.path.join(repo, "DECISIONS.md"))
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, oid, "id_set"); lacks(o, "[parser]")
    shutil.copy(out, os.path.join(repo, "ops", "decisions.csv"))
    rc, o = ctx.lint(root=repo); ok(rc == 0, "a CSV regenerated from the annotated register must pass: " + o)
    # a citation of the annotated IDs in an ops document is accepted; the absorbed ID, which is not a row, is flagged
    edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nSee %s and %s." % (oid, wid))
    rc, o = ctx.lint(root=repo); ok(rc == 0, "cited_id must accept %s and %s: %s" % (oid, wid, o))
    edit(repo, "ops/GATHER.md", "See %s and %s." % (oid, wid), "See %s, %s and %s." % (oid, wid, gone))
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "%s is cited but is not in DECISIONS.md" % gone, "cited_id"); lacks(o, "%s is cited" % oid)
    # a row that cannot be parsed is a malformed register (exit 2 from the generator), never a row that vanishes
    cases = {
        "pipe": ("| %s|broken" % oid, "has 2 cells"),
        "suffix": ("| %sx | Sun 1 Nov | A synthetic question? | A synthetic recommendation. |" % oid, "looks like a register row but does not parse"),
        "digits": ("| O-%d | Sun 1 Nov | A synthetic question? | A synthetic recommendation. |" % 1234, "looks like a register row but does not parse"),
        "space": ("| O-6 | Sun 1 Nov | A synthetic question? | A synthetic recommendation. |", "looks like a register row but does not parse"),
        # an ID cell wrapped in emphasis or code marks used to be dropped in silence (--write exit 0, no message)
        "emphasis": ("| **%s** | Sun 1 Nov | A synthetic question? | A synthetic recommendation. |" % oid, "looks like a register row but does not parse"),
        "code": ("| `%s` | Sun 1 Nov | A synthetic question? | A synthetic recommendation. |" % oid, "looks like a register row but does not parse"),
    }
    for name, (line, why) in cases.items():
        bp = ctx.write("broken_%s.md" % name, reg.replace(o_anchor, o_anchor + "\n" + line, 1))
        bout = os.path.join(ctx.tmp, "broken_%s.csv" % name)
        rc, o = ctx.run(["scripts/decisions_to_csv.py", "--write", bout, "--register", bp])
        ok(rc == 2, "%s: --write exit %d: %s" % (name, rc, o)); has(o, "malformed", why)
        ok(not os.path.exists(bout), "%s: a CSV was written from a malformed register" % name)
        rc, o = ctx.run(["scripts/decisions_to_csv.py", "--check", os.path.join(ROOT, "ops", "decisions.csv"), "--register", bp])
        ok(rc == 2, "%s: --check exit %d: %s" % (name, rc, o))
    shutil.copy(bp, os.path.join(repo, "DECISIONS.md"))  # the last broken copy: ops_lint reports it, it does not skip the row
    rc, o = ctx.lint(root=repo); ok(rc == 1, o); has(o, "the register is malformed")
    # defence in depth: take the generator's own guard out (scratch copy of the three scripts). The emphasised row
    # is then dropped in silence by --write, and ops_lint's separate count of lines that look like a register row
    # still fires the `parser` finding. With the real scripts this finding cannot fire (the guard stops first).
    sdir = os.path.join(ctx.tmp, "scripts_noguard")
    os.makedirs(sdir)
    for f in ("ops_lint.py", "hours_report.py", "decisions_to_csv.py"):
        shutil.copy(os.path.join(ROOT, "scripts", f), sdir)
    src = open(os.path.join(sdir, "decisions_to_csv.py"), encoding="utf-8").read()
    guard = ("            if NEAR_MISS_RE.match(line):\n"
             "                raise ValueError(\"line %d: looks like a register row but does not parse\" % n)\n")
    ok(guard in src, "test setup: the guard in decisions_to_csv.py moved; update this test")
    open(os.path.join(sdir, "decisions_to_csv.py"), "w", encoding="utf-8", newline="").write(src.replace(guard, ""))
    emph = ctx.write("emphasis_only.md", reg.replace(o_anchor, o_anchor + "\n" + cases["emphasis"][0], 1))
    silent = os.path.join(ctx.tmp, "silent.csv")
    rc, o = ctx.run([os.path.join(sdir, "decisions_to_csv.py"), "--write", silent, "--register", emph])
    ok(rc == 0 and "%d rows" % len(current) in o, "test setup: without its guard the generator should drop the emphasised row in silence: %s" % o)
    shutil.copy(emph, os.path.join(repo, "DECISIONS.md"))
    shutil.copy(silent, os.path.join(repo, "ops", "decisions.csv"))
    rc, o = ctx.run([os.path.join(sdir, "ops_lint.py"), "--patterns", ctx.patterns(), "--root", repo])
    ok(rc == 1, o); has(o, "[parser]", "%d line(s) start like a register row but the generator made %d row(s)" % (len(current) + 1, len(current)))
    rc, o = ctx.lint(root=repo)   # the real scripts stop at the emphasised row
    ok(rc == 1, o); has(o, "the register is malformed")
    ctx.say("%s and %s reach the CSV (%d rows) with notes 'absorbs %s' and 'revises W-05'; %d live annotated ID cells carry their note; "
            "ops_lint accepts a citation of the new IDs and flags %s; six unparseable rows (including | **ID** | and | `ID` |) exit 2 and ops_lint reports "
            "the register malformed; with the guard removed the emphasised row is dropped by --write and ops_lint's `parser` finding fires"
            % (oid, wid, len(current) + 2, gone, len(annotated), gone))


@test("decisions_bad_register", "a malformed register (wrong cell count, duplicate ID, ID in the wrong table) exits 2")
def _(ctx):
    reg = read("DECISIONS.md")
    anchor = last_row_line(reg, "O")
    cases = {
        "cells": reg.replace(anchor, anchor + "\n| %s | only two cells |" % next_id("O"), 1),
        "dup": reg.replace(anchor, anchor + "\n" + anchor, 1),
        "table": reg.replace(anchor, anchor + "\n| %s | Sun 1 Nov | wrong table | x |" % next_id("W"), 1),
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
        ("date,activity,minutes\n2026-10-19,learn,5\n", "line 1", "header must be exactly", "found 3 column(s), masked: da**,ac******,mi*****"),
        (h + "19/10/2026,-,learn,30,maker,x\n", "line 2", "date '19********'"),
        (h + "2026-02-30,-,learn,30,maker,x\n", "line 2", "date '20********' is not a real calendar date"),
        (h + "2026-10-19,-,learn,1.5h,maker,x\n", "line 2", "minutes '1.**'"),
        (h + "2026-10-19,-,learn,0,maker,x\n", "line 2", "minutes '0'"),
        (h + "2026-10-19,-,learn,1441,maker,x\n", "line 2", "minutes '14**'"),
        (h + "2026-10-19,album pages,learn,30,maker,x\n", "line 2", "shot_or_chapter 'al"),
        (h + "2026-10-19,-,learn,30,maker,one, two\n", "line 2", "expected 6 columns, found 7"),
        (h + "2026-10-19,-,learn,30,,x\n", "line 2", "who '' must be exactly maker or agent"),
        (h + "2026-10-19,-,learn,30,someone,x\n", "line 2", "who 'so", "must be exactly maker or agent"),
        (h + "2026-10-19,-,learn,30,Maker,x\n", "line 2", "must be exactly maker or agent", "did you mean 'maker'"),
        (h + "2026-10-19,-,learn,30,AGENT,x\n", "line 2", "who 'AG", "did you mean 'agent'"),
        (h + "2026-10-19,c01,learn,30,maker,x\n", "line 2", "shot_or_chapter 'c0", "capital letters and a digit", "IDs are written in capital letters"),
        (h + "2026-10-19,CHAPTER-ONE,learn,30,maker,x\n", "line 2", "shot_or_chapter 'CH", "capital letters and a digit"),
        (h + "2026-10-19,-,Learn,30,maker,x\n", "line 2", "did you mean 'learn'"),
        ("", "line 1", "empty"),
    ]
    for text, *needles in cases:
        rc, o = hours(ctx, text)
        ok(rc == 1, "exit %d for %r: %s" % (rc, text[:50], o)); has(o, *needles)
        lacks(o, "someone", "album pages")
    # a shifted row can put a name in any column: no echoed cell may print it (date, minutes, the
    # header line); the model is hours_note_never_printed
    tok1, tok2 = "Zqx" + "name", "Sur" + "xname"
    shifted = [
        (h + "%s %s,-,learn,30,maker,x\n" % (tok1, tok2), "line 2", "date 'Zq"),
        (h + "2026-10-19,-,learn,%s %s,maker,x\n" % (tok1, tok2), "line 2", "minutes 'Zq"),
        (h + "%s %s,-,learn,%s %s,maker,x\n" % (tok1, tok2, tok1, tok2), "line 2", "date 'Zq", "minutes 'Zq"),
        (h + "2026-10-19,-,learn,%s,maker,x\n" % (tok1 + "9" * 40), "line 2", "minutes 'Zq"),
        ("%s,%s,learn,30,maker,x\n" % (tok1, tok2), "line 1", "header must be exactly", "masked: Zq"),
        ("%s;%s\n2026-10-19;learn\n" % (tok1, tok2), "line 1", "semicolon"),
        # a hyphenated personal name used to pass as a shot ID (^[A-Za-z0-9][A-Za-z0-9_.-]*$); an ID needs a capital and a digit
        (h + "2026-10-19,%s-%s,learn,30,maker,x\n" % (tok1, tok2), "line 2", "shot_or_chapter 'Zq", "a name is not an ID"),
        (h + "2026-10-19,%s-%s-%s,learn,30,maker,x\n" % (tok1, tok2, tok1), "line 2", "shot_or_chapter 'Zq", "a name is not an ID"),
    ]
    for text, *needles in shifted:
        rc, o = hours(ctx, text)
        ok(rc == 1, "exit %d for a shifted row: %s" % (rc, o)); has(o, *needles)
        lacks(o, tok1, tok2, tok1.lower(), tok2.lower(), tok1[2:], tok2[2:])
    rc, o = hours(ctx, shifted[2][0], "--json")
    ok(rc == 1, o); lacks(o, tok1, tok2)
    # what an ID is: a capital letter and a digit (C01, LJ-C01-S014, OBJ-02) pass; a name does not
    for good in ("C01", "LJ-C01-S014", "LJ-C01-S002", "OBJ-02", "-"):
        rc, o = hours(ctx, h + "2026-10-19,%s,learn,30,maker,x\n" % good, "--week-start", "2026-10-19")
        ok(rc == 0, "the shot/chapter ID %r must be accepted: %s" % (good, o))
    ctx.say("%d invalid files, each exit 1 with the line and the problem; %d shifted rows, name-shaped shot IDs and headers never print the planted tokens; "
            "C01, LJ-C01-S014, OBJ-02 and '-' are accepted" % (len(cases), len(shifted)))


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
    email = planted_email()
    ok("@" in email and email.rsplit(".", 1)[-1] not in ("example", "invalid", "test", "localhost"),
       "the planted e-mail must be a non-reserved shape, not one the pattern file exempts")
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
    planted = [email, email.split("@", 1)[0], email.split("@", 1)[1], "qzx" + "user", "Qzx" + "plorp", "172" + ".16", "qzx" + "_handle"]
    lacks(o, *planted)
    # the mask is exactly the pattern file's: keep, then fill up to cap (so a long hit does not leak its length)
    mk = pattern_mask()
    want_email = email[:mk["keep"]] + mk["fill"] * min(len(email) - mk["keep"], mk["cap"])
    ok(re.search(r"\[email\] note: masked hit " + re.escape(want_email) + r"$", o, re.M),
       "e-mail not masked exactly as '%s' (keep %d, cap %d)" % (want_email, mk["keep"], mk["cap"]))
    ok(len(email) - mk["keep"] > mk["cap"], "test setup: the planted e-mail must be longer than keep + cap to prove the cap")
    deny_name = "Qzx" + "plorp"
    want_deny = deny_name[:mk["keep"]] + mk["fill"] * min(len(deny_name) - mk["keep"], mk["cap"])
    ok(re.search(r"\[local_deny\] note: masked hit " + re.escape(want_deny) + r"$", o, re.M),
       "deny-list name not masked exactly as '%s'" % want_deny)
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


@test("lint_hours_shifted_masked", "ops_lint --hours on a shifted row (a name in date and minutes) exits 1 and never prints the planted tokens")
def _(ctx):
    tok1, tok2 = "Zqx" + "name", "Sur" + "xname"
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    p = ctx.write("shifted.csv", h + "%s %s,-,learn,%s %s,maker,x\n" % (tok1, tok2, tok1, tok2))
    rc, o = ctx.lint("--hours", p)
    ok(rc == 1, o); has(o, "shifted.csv:2 [hours_format]", "date 'Zq", "minutes 'Zq")
    lacks(o, tok1, tok2, tok1.lower(), tok2.lower())
    p1 = ctx.write("nohdr.csv", "%s,%s,learn,30,maker,x\n" % (tok1, tok2))
    rc, o = ctx.lint("--hours", p1)
    ok(rc == 1, o); has(o, "nohdr.csv:1 [hours_format]", "header must be exactly")
    lacks(o, tok1, tok2, tok1.lower(), tok2.lower())
    ctx.say("ops_lint --hours: exit 1 on a shifted row and on a header-less file; no planted token printed")


def edit(repo, rel, old, new, count=1):
    p = os.path.join(repo, rel)
    t = open(p, encoding="utf-8").read()
    ok(old in t, "test setup: %r not found in %s" % (old, rel))
    open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new, count))


@test("lint_neg_card", "negative: card without Phone (W-63, FontSize=28) / Script stack / Fonts / Burn-in rows / TD-3 MarginV / an invented ID / without the Language line / signed with <date>")
def _(ctx):
    cases = [
        ("no phone row", "| **Phone** (D-27)", "| **Handset** (D-27)", ["Phone", "card_row"]),
        ("no D-27 in the row", "| D-27, W-63, W-18 |", "| D-26, W-63, W-18 |", ["D-27"]),
        ("no W-63 on the Phone row", "| D-27, W-63, W-18 |", "| D-27, W-18 |", ["W-63", "card_row"]),
        ("Phone caption size missing", "`FontSize=28`", "`FontSize=26`", ["FontSize=28", "card_value"]),
        ("TD-3 without MarginV", "`MarginV` 20 or more (the default lets", "a margin (the default lets", ["MarginV", "card_value"]),
        ("no Script stack row", "| **Script stack** |", "| **Scripts** |", ["Script stack", "card_row"]),
        ("no Fonts row", "| **Fonts** |", "| **Typefaces** |", ["Fonts", "card_row"]),
        ("no Burn-in row", "| **Burn-in path** |", "| **Caption filter** |", ["Burn-in path", "card_row"]),

        ("invented ID", "(O-14)", "(W-99)", ["W-99", "cited_id"]),
        ("no language line", "Caption and font test ran in:", "Caption and font was run in:", ["card_language"]),
        ("no NOT TESTED", "gujarati NOT TESTED (D-31", "gujarati tested (D-31", ["NOT TESTED"]),
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
    # row-scoped mutations: a word taken out of one row only (the same word appears in other cells and rows)
    row_cases = [
        ("Script stack without Gujarati", "| **Script stack**", "Gujarati", "the local language", ["Script stack", "card_value", "Gujarati"]),
        ("Fonts without the OFL.txt hash", "| **Fonts**", "OFL.txt", "licence file", ["Fonts", "card_value", "OFL.txt"]),
        ("Burn-in row without the subtitles route", "| **Burn-in path**", "`subtitles`", "the other filter", ["Burn-in path", "card_value", "subtitles"]),
        ("Burn-in row without the ass route", "| **Burn-in path**", "`ass`", "the other route", ["Burn-in path", "card_value", "ass"]),
    ]
    for name, prefix, old, new, needles in row_cases:
        repo = ctx.clone()
        cp = os.path.join(repo, "ops", "SETTINGS-CARD.md")
        lines = open(cp, encoding="utf-8").read().split("\n")
        ix = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
        ok(len(ix) == 1 and old in lines[ix[0]], "test setup: one %s row containing %r" % (prefix, old))
        lines[ix[0]] = lines[ix[0]].replace(old, new)
        open(cp, "w", encoding="utf-8", newline="").write("\n".join(lines))
        rc, o = ctx.lint(root=repo)
        ok(rc == 1, "%s: exit %d: %s" % (name, rc, o)); has(o, *needles)
    ctx.say("%d card mutations (%d of them inside one row), each exit 1 naming the problem" % (len(cases) + len(row_cases), len(row_cases)))


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


@test("lint_neg_gather", "negative: GATHER without the gate / a stand-in ID / with a stand-in in Part B / a real-box ID in Part A / without SND-01")
def _(ctx):
    cases = [
        ("no gate", "**Gate: nothing", "**Rule: nothing", ["gather_gate"]),
        ("missing stand-in", "`LJ-ST-0003-F`", "`LJ-ST-0003-X`", ["LJ-ST-0003-F"]),
        ("no Part B heading", "## Part B: From Sun 15 Nov, only after P-LOCK passes", "## Later", ["gather_parts"]),
        ("stand-in in Part B", "| photo | `LJ-<box>-<nnnn>-F` |", "| photo | `LJ-ST-0009-F` |", ["Part B", "LJ-ST-0009-F"]),
        ("real box in Part A", "| [ ] | `LJ-ST-0005-F` |", "| [ ] | `LJ-B03-0005-F` |", ["before P-LOCK", "LJ-B03-0005-F"]),
        ("invented ID", "(O-06)", "(O-96)", ["O-96"]),
        ("no SND-01", "SND-01", "SND-0X", ["gather_ids", "SND-01"]),
    ]
    for name, old, new, needles in cases:
        repo = ctx.clone()
        if name == "no SND-01":
            edit(repo, "ops/GATHER.md", old, new, count=99)
        elif name == "real box in Part A":
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
    email = planted_email()  # the pattern file's own positive sample (a non-reserved shape), joined
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
    # the exemption works the other way too: an address on a reserved example domain (the pattern file's own
    # negative sample, which is the shape the fixture used before r1) passes; skipped for a development file
    if not USING_OVERRIDE:
        repo = ctx.clone()
        edit(repo, "ops/GATHER.md", "# GATHER: what to collect, and when", "# GATHER: what to collect, and when\n\nContact: " + exempt_email())
        rc, o = ctx.lint(root=repo); ok(rc == 0, "a reserved-domain address must pass: " + o)
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
    pf = ctx.write("mini.json", json.dumps({"schema": "synthetic", "version": "mini", "categories": cats, "mask": {"keep": 3, "fill": "#", "cap": 4}}))
    h = "date,shot_or_chapter,activity,minutes,who,note\n"
    p = ctx.write("m.csv", h + "2026-10-19,-,learn,30,maker,here is zzflagmeplease and PROBEWORD77\n"
                  "2026-10-19,-,learn,30,maker,someone" + "@" + "elsewhere" + ".example is not flagged by this file\n")
    rc, o = ctx.run(["scripts/ops_lint.py", "--patterns", pf, "--hours", p])
    ok(rc == 1, o)
    has(o, "m.csv:2 [email]", "m.csv:2 [custom_probe]")
    # keep 3, fill '#', cap 4 come from the file: 'zzflagmeplease' (14 characters) shows 3 + 4, not 3 + 11
    ok(re.search(r"\[email\] note: masked hit zzf####$", o, re.M), "mask keep/fill/cap not taken from the file:\n" + o)
    ok(re.search(r"\[custom_probe\] note: masked hit PRO####$", o, re.M), "mask keep/fill/cap not taken from the file:\n" + o)
    lacks(o, "m.csv:3", "zzf#####")
    ctx.say("the mini file flagged only what it defines; the mask keep, fill and cap came from the file as well")


@test("lint_mask_parity", "ops_lint and public_lint print the same mask for the same hit (keep, fill and cap from the pattern file)")
def _(ctx):
    import importlib.util
    sys.dont_write_bytecode = True
    mods = {}
    for name in ("ops_lint", "public_lint"):
        spec = importlib.util.spec_from_file_location("lj_parity_" + name, os.path.join(ROOT, "scripts", name + ".py"))
        mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mods[name])
    for label, pf in (("the pattern file in use", ctx.patterns()),
                      ("a file with keep 3, fill # and cap 4", ctx.write("parity.json", json.dumps(
                          {"version": "parity", "categories": [{"id": c, "scope": "both", "regex": "ZZNEVER" + c, "flags": ""} for c in
                           ["email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux", "token_shape", "guid_serial", "handle"]],
                           "mask": {"keep": 3, "fill": "#", "cap": 4}})))):
        ops = mods["ops_lint"].Patterns(pf)
        pub = mods["public_lint"].Patterns(json.load(open(pf, encoding="utf-8")))
        for value in ["a", "ab", "abc", "abcdefghij", "x" * 40, "someone" + "@" + "a-long-domain-name" + ".org"]:
            want = mods["public_lint"].mask(value, ops.keep, ops.fill, ops.cap)
            ok(ops.mask(value) == want, "%s: ops_lint masks %r as %r, public_lint as %r" % (label, value, ops.mask(value), want))
            ok(pub.mask(value) == ops.mask(value), "%s: public_lint's own Patterns masks %r differently" % (label, value))
        long_mask = ops.mask("x" * 40)
        ok(len(long_mask) == ops.keep + ops.cap, "%s: a 40-character hit is masked to %d characters, not %d" % (label, len(long_mask), ops.keep + ops.cap))
    ctx.say("ops_lint.mask equals public_lint.mask for six values under two mask settings; a 40-character hit shows keep + cap characters")


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
    cited = set("%s-%s" % m for m in re.findall(r"\b([DWOS])-([0-9]{2,3})\b", t))
    ok(cited and cited <= ids, "cited IDs not in the register: %s" % sorted(cited - ids))
    for rid in ["W-14", "W-15", "W-16", "W-17", "W-18", "W-19", "D-27", "D-31", "O-14", "O-15", "W-57", "W-63", "W-75"]:
        ok(rid in cited, "%s should be cited" % rid)
    # what the register says the maker signs on Sun 1 Nov (W-16 "Added 2026-10-19", O-14): TD-1..TD-4 plus the
    # phone rows (PH1, PH2: W-63), the font rows and the script decision (W-75, O-15) and the burn-in path
    rows = {ln.split("|")[1].strip(): [c.strip() for c in ln.strip().strip("|").split("|")] for ln in t.split("\n") if ln.startswith("| **")}
    def row(prefix):
        hit = [v for k, v in rows.items() if k.startswith(prefix)]
        ok(len(hit) == 1 and len(hit[0]) == 6, "the card needs exactly one six-column row starting %r" % prefix)
        return hit[0]
    phone, td3 = row("**Phone"), row("**TD-3")
    ok("D-27" in phone[3] and "W-63" in phone[3] and "W-18" in phone[3], "Phone row Register cell: %r" % phone[3])
    ok("PH1" in phone[2] and "PH2" in phone[2], "the Phone row must name PH1 and PH2 (W-63)")
    ok(all(n in phone[2] for n in ("1280x720", "CRF 20", "CRF 22", "8 Mb/s", "4 Mb/s", "level 3.1", "before the downscale")), "PH1/PH2 numbers (W-63)")
    ok(all(n in phone[2] for n in ("`FontSize=28`", "`MarginV` 40", "36 characters", "68 to 86%")), "the phone caption numbers are W-18's")
    ok("to be set by the phone test" not in t, "the Phone row must not defer to the phone test: W-18 fixes the phone caption size")
    ok("`MarginV` 20 or more" in td3[2] and "W-16" in td3[3] and "W-18" in td3[3], "TD-3 must carry MarginV 20 (W-16, W-18)")
    for prefix, regs, needles in [("**Script stack", ("W-75", "O-15"), ("Gujarati", "Devanagari", "shaped outlines")),
                                  ("**Fonts", ("W-75", "W-21"), ("OFL.txt", "fontselect:", "pasted from the T8 font rows")),
                                  ("**Burn-in path", ("W-16", "W-75", "O-14"), ("`ass`", "`subtitles`", "ab.srt"))]:
        r = row(prefix)
        ok(all(x in r[3] for x in regs), "%s: Register cell %r must cite %s" % (prefix, r[3], ", ".join(regs)))
        ok(all(x in " ".join(r) for x in needles), "%s: lacks one of %s" % (prefix, needles))
        ok("Proposed (J)" in r[2], "%s must be marked Proposed (J)" % prefix)
        ok("UNVERIFIED" in r[4], "%s must say UNVERIFIED in its proof cell until the PC run" % prefix)
    lang = [ln for ln in t.split("\n") if "Caption and font test ran in:" in ln]
    ok(len(lang) == 1 and "devanagari (neutral test strings) on <date>" in lang[0] and "gujarati NOT TESTED" in lang[0]
       and "D-31" in lang[0] and "32-string fixture of W-16/W-75" in lang[0], "the language line must say gujarati is NOT TESTED (D-31)")
    ok("until the maker's script is named" not in t, "D-31 names Gujarati: the card must not say the script is unnamed")
    status = [ln for ln in t.split("\n") if ln.startswith("*Status when drafted")]
    ok(status and "Gujarati" in status[0] and "D-31" in status[0] and "pending_O-10" in status[0]
       and "must pass before this card is signed" in status[0],
       "the status paragraph must say the Gujarati test is the one that counts (D-31, pending_O-10)")
    ok("<date>" in t and "Scripts tested:" in t, "the <date> and 'Scripts tested:' paste-over convention must stay")
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
    # A1 rows O-07 and O-08 follow the register's current wording (two candidate tunes, two takes each, W-65; the hichko question, W-67)
    o07 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-07")]
    ok(o07 and "W-65" in o07[0].split("|")[2], "the O-07 row's Register cell must cite W-65")
    ok(all(n in o07[0] for n in ("HUM-01", "HUM-04", "closed-mouth", "open-vowel", "birth or a wedding", "originals/", "uncleaned")),
       "the O-07 row must ask for two candidate tunes, a closed-mouth and an open-vowel take of each, uncleaned, into originals/ (HUM-01 to HUM-04)")
    o08 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-08")]
    ok(o08 and "W-67" in o08[0].split("|")[2], "the O-08 row's Register cell must cite W-67")
    ok(all(n in o08[0] for n in ("hichko", "every evening", "at what hour", "travel with her")), "the O-08 row must ask the hichko question")
    o10 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-10")]
    ok(o10 and "D-31" in o10[0].split("|")[2], "the O-10 row's Register cell must cite D-31")
    # the v3 / v3.1 wording of the register's sittings (O-06, O-08 with O-48, O-10, O-11) and the two own-material rows it added (O-54, O-71)
    o06 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-06")]
    ok(o06 and "and which of these does she do now" in o06[0] and "if it is seva craft, the material is the making, never the article" in o06[0],
       "the O-06 row must ask which of these crafts she does now and say that seva craft is the making, never the article")
    ok("O-48" in o08[0].split("|")[2] and all(n in o08[0] for n in ("inside the mandir", "any picture of hers", "only by sight, untouched", "G5 flag")),
       "the O-08 row must carry O-48's never-photograph rule (Register cell O-48)")
    ok("the prayer language of the house (kirtan, stotra, everyday speech)" in o10[0], "the O-10 row must ask for the prayer language of the house")
    o11 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-11")]
    ok(o11 and "whether it is her birthday stays in your notes and is never recorded" in o11[0],
       "the O-11 row must say that whether it is her birthday stays in the notes and is never recorded")
    o54 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-54")]
    ok(o54 and "O-54" in o54[0].split("|")[2] and "W-26" in o54[0].split("|")[2], "an O-54, W-26 row (her phone) is required")
    ok(all(n in o54[0] for n in ("make, model, Android version", "free storage", "USB-C", "video", "device-folder backup", "`DEV-xx`", "never a serial number or an account", "never looked at or tested before the reveal")),
       "the O-54 row must list make, model, Android version, storage, USB-C, the video app and device-folder backup, recorded as DEV-xx, never a serial number or an account")
    o71 = [ln for ln in g.split("\n") if ln.startswith("| [ ] | O-71")]
    ok(o71 and all(n in o71[0] for n in ("empty room", "seva article", "`SND-01`", "`SND-02`", "does not sync")),
       "an O-71 row (sounds of the house, SND-01, SND-02, ...) is required")
    ok("`SND-01`" in g.split("**ID shapes used on this page.**")[1].split("\n")[0], "SND-01 belongs in the ID-shapes line")
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
