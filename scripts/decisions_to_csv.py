#!/usr/bin/env python3
"""decisions_to_csv.py - turn the decisions register (DECISIONS.md) into ops/decisions.csv.

WHAT IT DOES
  DECISIONS.md is the single source of truth (A-06). This tool reads its four tables
  (D decided, W defaults, O open questions, S superseded values) and writes a flat CSV
  mirror, one row per ID, so the plan, the planning skill and a restart-without-memory
  reader (W-13) can sort and filter it. The CSV is NEVER hand-typed: change the
  register, then run --write again.

HOW TO RUN (standard library only; always with -I)
  python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv   # (re)generate
  python3 -I scripts/decisions_to_csv.py --check ops/decisions.csv   # compare, exit 0/1
  Options: --register PATH (default: DECISIONS.md next to the scripts folder).

COLUMNS
  id,table,short_title,value_or_default,status,decide_by,owner,source,last_changed,maker_answer,note
  * table: T1 (decided), T2.1/T2.2/T2.3 (defaults), T3 (open), T4 (superseded values).
  * status vocabulary: decided, default, open, pending, answered, superseded, applied,
    outstanding. D rows are `decided` (D-14 and D-23 are `superseded`: D-23 says so itself
    and D-29 replaces it; D-14's repository visibility is superseded by D-26, conflict C-07).
    W rows are `default`. O rows are `open`, `pending` (the register marks the maker as
    already pending) or `answered` (the By column says "answered ..."; O-05, O-13). S rows
    carry the Table 4 Status word (`applied` or `outstanding`); the full status text goes
    in `note`.
  * Long values are cut so the cell is at most 300 characters and ends in
    `... see DECISIONS.md`. Markdown bold/italic/backtick marks are removed, and the
    public repository owner account name is written as <owner> (D-26: no usernames).
  * `maker_answer` and `last_changed` belong to the orchestrator: they are empty when a
    row is first created, are never overwritten, and are carried over by --write when the
    file already exists. --check ignores them.

WHAT IT PRINTS / TOUCHES
  Prints the row counts and any mismatch. --write replaces only the file you name (via a
  temporary file in the same folder). --check is read-only. Nothing else is touched, no
  network, no names: the register itself holds IDs only (D-26).

EXIT CODES (build plan 4.3)
  0 ok; 1 the CSV does not match the register; 2 bad usage or an unreadable/invalid
  register or file.
"""
import argparse
import csv
import io
import os
import re
import sys

COLUMNS = ["id", "table", "short_title", "value_or_default", "status", "decide_by",
           "owner", "source", "last_changed", "maker_answer", "note"]
ORCHESTRATOR_OWNED = ["last_changed", "maker_answer"]
GENERATED = [c for c in COLUMNS if c not in ORCHESTRATOR_OWNED]
STATUSES = ["decided", "default", "open", "pending", "answered", "superseded", "applied",
            "outstanding"]
CELLS_PER_PREFIX = {"D": 5, "W": 6, "O": 4, "S": 5}
MAX_LEN = 300
CUT_SUFFIX = "... see DECISIONS.md"
# D-14 still says "private" while D-26 (later) says public: build plan conflict C-07. The
# register is not edited by this tool; once DECISIONS.md says so itself, detection from
# the text takes over and this entry can be deleted.
KNOWN_SUPERSEDED = {"D-14": "D-26"}

ROW_RE = re.compile(r"^\|\s*([DWOS])-([0-9]{2})\s*\|")
SUPERSEDED_BY_RE = re.compile(r"superseded by (D-[0-9]{2})", re.I)
REPLACES_RE = re.compile(r"\b(?:replaces|supersedes) (D-[0-9]{2})\b", re.I)
# The repository owner is a public account name (a username). The register keeps it; this
# mirror does not copy it (D-26: no usernames in generated files): github.com/<owner>/...
# and <owner>/animated_journey are written with the placeholder <owner>.
OWNER_URL_RE = re.compile(r"(github\.com/)[A-Za-z0-9_.-]+(/)")
OWNER_REPO_RE = re.compile(r"(?<![/\w<-])[A-Za-z0-9_-]+/(animated_journey)\b")
PENDING_RE = re.compile(r"^\*\*\(pending(?:;\s*([^)]*))?\)\*\*\s*")


def clean(text):
    """Strip Markdown emphasis and code marks and collapse whitespace."""
    t = text.replace("**", "").replace("`", "")
    t = OWNER_URL_RE.sub(r"\1<owner>\2", t)
    t = OWNER_REPO_RE.sub(r"<owner>/\1", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def cut(text):
    if len(text) <= MAX_LEN:
        return text
    keep = MAX_LEN - len(CUT_SUFFIX)
    head = text[:keep]
    space = head.rfind(" ")
    if space > keep // 2:
        head = head[:space]
    return head.rstrip(" ,;:") + CUT_SUFFIX


def split_cells(line):
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def parse_register(text):
    """Return a list of raw rows: dict(id, table, cells[]). Raises ValueError on a
    malformed register (wrong cell count, duplicate ID, ID in the wrong table)."""
    rows, seen = [], {}
    table = None
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## 1."):
            table = "T1"
        elif line.startswith("### 2.1"):
            table = "T2.1"
        elif line.startswith("### 2.2"):
            table = "T2.2"
        elif line.startswith("### 2.3"):
            table = "T2.3"
        elif line.startswith("## 3."):
            table = "T3"
        elif line.startswith("## 4."):
            table = "T4"
        elif line.startswith("## ") and not line.startswith("## 2."):
            table = None
        m = ROW_RE.match(line)
        if not m:
            continue
        prefix, rid = m.group(1), "%s-%s" % (m.group(1), m.group(2))
        want = {"D": ("T1",), "W": ("T2.1", "T2.2", "T2.3"), "O": ("T3",), "S": ("T4",)}[prefix]
        if table not in want:
            raise ValueError("line %d: %s is in table %s but belongs to %s" % (n, rid, table, "/".join(want)))
        cells = split_cells(line)
        if len(cells) != CELLS_PER_PREFIX[prefix]:
            raise ValueError("line %d: %s has %d cells, expected %d"
                             % (n, rid, len(cells), CELLS_PER_PREFIX[prefix]))
        if rid in seen:
            raise ValueError("line %d: %s appears twice (first on line %d)" % (n, rid, seen[rid]))
        seen[rid] = n
        rows.append({"id": rid, "table": table, "cells": cells})
    if not rows:
        raise ValueError("no register rows found: is this DECISIONS.md?")
    return rows


def build_rows(raw):
    """Raw rows -> list of dicts keyed by COLUMNS (orchestrator-owned columns empty)."""
    replaced_by = {}
    for r in raw:
        if r["id"].startswith("D"):
            for target in REPLACES_RE.findall(clean(" ".join(r["cells"][1:3]))):
                replaced_by.setdefault(target, r["id"])
    out = []
    for r in raw:
        rid, table, c = r["id"], r["table"], r["cells"]
        row = {k: "" for k in COLUMNS}
        row["id"], row["table"] = rid, table
        prefix = rid[0]
        if prefix == "D":
            title, value, since, source = clean(c[1]), clean(c[2]), clean(c[3]), clean(c[4])
            row.update(short_title=title, value_or_default=value, status="decided", source=source)
            notes = []
            sup = SUPERSEDED_BY_RE.search(title + " " + value)
            by = (sup.group(1) if sup and sup.group(1) != rid else None) \
                or replaced_by.get(rid) or KNOWN_SUPERSEDED.get(rid)
            if by:
                row["status"] = "superseded"
                notes.append("superseded by %s" % by)
            if since:
                notes.append("since %s" % since)
            row["note"] = "; ".join(notes)
        elif prefix == "W":
            row.update(short_title=clean(c[1]), value_or_default=clean(c[2]), status="default",
                       decide_by=clean(c[3]), owner=clean(c[4]), source=clean(c[5]))
        elif prefix == "O":
            by_raw, question, rec = clean(c[1]), c[2], clean(c[3])
            note = ""
            status = "open"
            pm = PENDING_RE.match(question)
            if pm:
                status = "pending"
                question = question[pm.end():]
                note = clean(pm.group(1)) if pm.group(1) else ""
            if by_raw.lower().startswith("answered"):
                status = "answered"
            row.update(short_title=clean(question), value_or_default=rec, status=status,
                       decide_by=by_raw, owner="Maker", note=note)
        else:  # S
            stale, canon, where, status_text = clean(c[1]), clean(c[2]), clean(c[3]), clean(c[4])
            word = re.match(r"([A-Za-z]+)", status_text)
            status = word.group(1).lower() if word else ""
            row.update(short_title=stale, value_or_default=canon, status=status, source=where)
            row["note"] = "" if status_text.lower() == status else status_text
        for k in ("short_title", "value_or_default", "decide_by", "owner", "source", "note"):
            row[k] = cut(row[k])
        out.append(row)
    return out


def counts(rows):
    c = {}
    for r in rows:
        c[r["id"][0]] = c.get(r["id"][0], 0) + 1
    return c


def count_text(rows):
    c = counts(rows)
    t = {}
    for r in rows:
        t[r["table"]] = t.get(r["table"], 0) + 1
    return "%d rows (%s; by table %s)" % (
        len(rows), ", ".join("%s %d" % (k, c[k]) for k in "DWOS" if k in c),
        ", ".join("%s %d" % (k, t[k]) for k in sorted(t)))


def render_csv(rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS)
    for r in rows:
        w.writerow([r[k] for k in COLUMNS])
    return buf.getvalue()


def read_csv_file(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    text = raw.decode("utf-8")
    reader = csv.reader(io.StringIO(text, newline=""))
    recs = list(reader)
    return recs


def load_register(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        print("decisions_to_csv: cannot read the register %s (%s)" % (os.path.basename(path), exc.strerror),
              file=sys.stderr)
        raise SystemExit(2)


def do_write(rows, path):
    existing = {}
    if os.path.exists(path):
        try:
            recs = read_csv_file(path)
        except (OSError, UnicodeDecodeError) as exc:
            print("decisions_to_csv: cannot read the existing %s: %s" % (os.path.basename(path), exc),
                  file=sys.stderr)
            return 2
        if recs:
            head = recs[0]
            for rec in recs[1:]:
                if len(rec) == len(head) and rec and rec[0]:
                    d = dict(zip(head, rec))
                    existing[d["id"]] = {k: d.get(k, "") for k in ORCHESTRATOR_OWNED}
    for r in rows:
        for k in ORCHESTRATOR_OWNED:
            r[k] = existing.get(r["id"], {}).get(k, "")
    data = render_csv(rows)
    folder = os.path.dirname(os.path.abspath(path))
    tmp = os.path.join(folder, ".decisions_to_csv.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except OSError as exc:
        print("decisions_to_csv: cannot write %s (%s)" % (os.path.basename(path), exc.strerror), file=sys.stderr)
        return 2
    kept = sum(1 for r in rows if r["id"] in existing and any(existing[r["id"]].values()))
    print("wrote %s: %s; orchestrator-owned cells carried over: %d row(s)"
          % (os.path.basename(path), count_text(rows), kept))
    return 0


def compare(rows, path):
    """Compare the CSV at `path` with the register rows. Returns a list of problem strings
    (empty means the CSV matches). Raises OSError / UnicodeDecodeError if unreadable."""
    recs = read_csv_file(path)
    if not recs or recs[0] != COLUMNS:
        return ["header must be exactly: " + ",".join(COLUMNS)
                + " (found: " + (",".join(recs[0]) if recs else "empty file")[:140] + ")"]
    problems, csv_rows, seen = [], {}, set()
    for i, rec in enumerate(recs[1:], 2):
        if not any(rec):
            continue
        if len(rec) != len(COLUMNS):
            problems.append("line %d: %d columns, expected %d" % (i, len(rec), len(COLUMNS)))
            continue
        d = dict(zip(COLUMNS, rec))
        if d["id"] in seen:
            problems.append("line %d: duplicate ID %s" % (i, d["id"]))
        seen.add(d["id"])
        csv_rows[d["id"]] = d
        if d["status"] not in STATUSES:
            problems.append("line %d: %s has status '%s', not one of %s"
                            % (i, d["id"], d["status"], "|".join(STATUSES)))
    want = {r["id"]: r for r in rows}
    for rid in want:
        if rid not in csv_rows:
            problems.append("%s is in DECISIONS.md but missing from the CSV" % rid)
    for rid in csv_rows:
        if rid not in want:
            problems.append("%s is in the CSV but not in DECISIONS.md (invented ID)" % rid)
    for rid, w in want.items():
        d = csv_rows.get(rid)
        if not d:
            continue
        for k in GENERATED:
            if d[k] != w[k]:
                problems.append("%s: column '%s' differs from the register (csv: '%s' / register: '%s')"
                                % (rid, k, d[k][:60], w[k][:60]))
    return problems


def do_check(rows, path):
    try:
        problems = compare(rows, path)
    except (OSError, UnicodeDecodeError) as exc:
        print("decisions_to_csv: cannot read %s: %s" % (os.path.basename(path), exc), file=sys.stderr)
        return 2
    if problems:
        for p in problems[:50]:
            print("  " + p)
        if len(problems) > 50:
            print("  ... and %d more" % (len(problems) - 50))
        print("FAIL: %s does not match the register (%d problem(s)); regenerate with --write"
              % (os.path.basename(path), len(problems)))
        return 1
    print("OK: %s matches the register: %s" % (os.path.basename(path), count_text(rows)))
    return 0


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="DECISIONS.md -> ops/decisions.csv")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", metavar="CSV", help="generate the CSV")
    g.add_argument("--check", metavar="CSV", help="compare the CSV with the register")
    ap.add_argument("--register", default=os.path.join(os.path.dirname(here), "DECISIONS.md"),
                    help="path to DECISIONS.md")
    args = ap.parse_args(argv)
    text = load_register(args.register)
    try:
        rows = build_rows(parse_register(text))
    except ValueError as exc:
        print("decisions_to_csv: the register is malformed: %s" % exc, file=sys.stderr)
        return 2
    if args.write:
        return do_write(rows, args.write)
    return do_check(rows, args.check)


if __name__ == "__main__":
    sys.exit(main())
