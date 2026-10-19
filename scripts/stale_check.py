#!/usr/bin/env python3
"""stale_check.py: the stale-copy check (DECISIONS.md W-29; build plan WP-03). Standard library only. READ-ONLY.

WHAT IT DOES
  Greps the playbooks, skills, fixtures and scripts for every stale value in Table 4 of DECISIONS.md
  (S-01 to S-65 in register v3) and for the retired spellings W-29 names ("L1 process lock", "spikes
  S1-S5", Minecraft, voxel, the placeholder observances, "the T2 rule", "not applied here", ...), using
  scripts/stale_patterns.json. The W-29 allowlist (scripts/stale_allowlist.json) suppresses the
  legitimate contexts. It FIXES NOTHING: the report is a work order for the scribes.
  The register and this check must not drift: when Table 4 grows, the rows and their patterns are added
  to the pattern file in the same pass and the baseline is re-cut the same day; --self-test fails when a
  Table 4 id has no row, when a row's status disagrees with Table 4, or when the O-row bound is behind.

  Scanned: playbooks/, .claude/skills/, skills-staging/, research/*-fixtures/, research/sources/, win/,
  pipeline/, scripts/, ops/, spikes/.  Excluded (historical or authoritative): research/*.md, reviews/,
  DECISIONS.md, ROADMAP.md, PLAN-ON-A-PAGE.md, CHARTER.md, CLAUDE.md, build/, its own pattern, allowlist and
  baseline files, ops/decisions.csv (the generated mirror of DECISIONS.md) and tests/.

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows)
  python3 -I scripts/stale_check.py                          report mode: prints a summary, exit 1 if any
                                                             non-allowlisted FAIL hit exists
  python3 -I scripts/stale_check.py --json OUT.json --md OUT.md     also writes the report files
  python3 -I scripts/stale_check.py --strict                 the pre-gate mode: prints only the failing hits
  python3 -I scripts/stale_check.py --baseline               writes scripts/stale_baseline.json (today's hits; re-cut it the
                                                             same day Table 4 or the patterns grow, or --new-only lists old
                                                             copies as new)
  python3 -I scripts/stale_check.py --new-only               exit 1 only for FAIL hits not in the baseline
                                                             (used by lj.ps1 close until the Haiku passes land)
  python3 -I scripts/stale_check.py --audit-allowlist        lists allowlist entries that suppress nothing (an entry marked
                                                             "structural" is printed as 'unused by design', not dead)
  python3 -I scripts/stale_check.py --self-test              every pattern has samples and they behave; every Table 4 id has a row
  Options: --root DIR (tree to scan, default the repository), --patterns F, --allowlist F, --baseline-file F,
           --register F (the DECISIONS.md the self-test reads Table 4 from; default DIR/DECISIONS.md).

THE REPORT (--json / --md)
  Counts per Table 4 row (all rows are listed, with zero if clean); REGRESSIONS (a hit on a row whose
  Table 4 status is applied: what the scribes thought they fixed but did not); WORK ORDERS for the
  outstanding rows (file:line and the canonical value); the rows that are not fully machine-checkable;
  and INFO candidate new Table 4 rows (none today: register v3 made Minecraft, voxel, Mojang and the
  placeholder observances rows S-42 to S-65), which never affect the exit code. Each hit is tagged
  changelog, code or prose: a changelog line that quotes an old value is still a hit (W-29 says "fails
  if found") but is shown apart. Some patterns choose the Table 4 row by file (D-29 terms: S-42 to S-50,
  S-54), so a hit is filed under the row whose scribe owns that file.

EXIT CODES (build plan 4.3)   0 clean (no non-allowlisted FAIL hit, or no NEW one with --new-only)
  1 a finding (FAIL hits; new hits; a dead allowlist entry; a self-test failure)
  2 bad usage or an invalid pattern, allowlist or baseline file
  3 environment problem (the tree to scan is missing)
It never writes outside the files named by --json, --md, --baseline and --baseline-file, never deletes,
never touches the network, and prints no names, hosts or absolute paths (paths are repo-relative).
"""
import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parent
PATTERNS_DEFAULT = HERE / "stale_patterns.json"
ALLOWLIST_DEFAULT = HERE / "stale_allowlist.json"
BASELINE_DEFAULT = HERE / "stale_baseline.json"

APPLIED = ("applied", "applied today", "check")
CODE_EXT = {".py", ".sh", ".ps1", ".mjs", ".js", ".mlt", ".json", ".jsonl", ".lcpreset", ".otio", ".svg", ".xml", ".html", ".css", ".yaml", ".yml"}
CHANGELOG_RX = re.compile(r"^\s*(?:[-*>]\s*)?(?:\*\*)?(?:v[0-9][0-9.]*[\s,;:.·-]*)?(?:20[0-9]{2}-[0-9]{2}-[0-9]{2})")


# a reading aid, not a filter: lines that say the old value is retired, superseded, replaced or absent
RETIRE_RX = re.compile(r"\b(?:retired|superseded|supersedes|replaced|replaces|replace|no longer|formerly|former|earlier|older|old|there (?:is|are) no|no 25-minute|not planned|does not exist|removes|removed|dropped|void)\b", re.I)


class Invalid(Exception):
    """A pattern, allowlist or baseline file is unusable (exit 2)."""


class EnvProblem(Exception):
    """The tree to scan is missing (exit 3)."""


def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------- loading
def _load_json(path, what):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except OSError:
        raise Invalid("%s is missing or unreadable" % what)
    except ValueError:
        raise Invalid("%s does not parse as JSON" % what)


def _rx(pattern, flags, what):
    try:
        return re.compile(pattern, re.I if "i" in (flags or "") else 0)
    except re.error as e:
        raise Invalid("%s has a regex that does not compile (%s)" % (what, e))


def load_patterns(path):
    d = _load_json(path, "the pattern file")
    if d.get("schema") != "lj-stale-patterns/1":
        raise Invalid("the pattern file has the wrong schema")
    pats = []
    attributions = d.get("attributions") or {}
    for p in d.get("patterns", []):
        for k in ("id", "row_id", "severity", "regex"):
            if k not in p:
                raise Invalid("a pattern lacks %s" % k)
        if p["severity"] not in ("FAIL", "WARN"):
            raise Invalid("pattern %s has severity %s" % (p["id"], p["severity"]))
        q = dict(p)
        q["rx"] = _rx(p["regex"], p.get("flags", ""), "pattern " + p["id"])
        # which Table 4 row owns a hit can depend on the file (and on the line): first matching entry wins, else row_id
        att = p.get("attribute") or []
        if isinstance(att, str):
            if att not in attributions:
                raise Invalid("pattern %s names the attribution list %s, which the pattern file does not have" % (p["id"], att))
            att = attributions[att]
        q["attr"] = []
        for a in att:
            if not a.get("row_id") or not a.get("files"):
                raise Invalid("pattern %s has an attribution entry without row_id or files" % p["id"])
            q["attr"].append({"row_id": a["row_id"], "files": list(a["files"]),
                              "rx": _rx(a["if_line"], a.get("flags", "i"), "attribution of pattern " + p["id"]) if a.get("if_line") else None})
        q["only_files"] = list(p.get("only_files") or [])
        pats.append(q)
    infos = []
    for p in d.get("info", []):
        q = dict(p)
        q["rx"] = _rx(p["regex"], p.get("flags", ""), "info pattern " + p["id"])
        infos.append(q)
    rows = {r["row_id"]: r for r in d.get("rows", [])}
    return d, pats, infos, rows


def load_allowlist(path):
    d = _load_json(path, "the allowlist")
    if d.get("schema") != "lj-stale-allowlist/1":
        raise Invalid("the allowlist has the wrong schema")
    entries = []
    for e in d.get("entries", []):
        for k in ("id", "file", "context_regex", "reason", "register_row"):
            if k not in e:
                raise Invalid("an allowlist entry lacks %s" % k)
        if e.get("structural") and not e.get("structural_reason"):
            raise Invalid("allowlist entry %s is marked structural but gives no structural_reason" % e["id"])
        q = dict(e)
        q["rx"] = _rx(e["context_regex"], e.get("flags", "i"), "allowlist entry " + e["id"])
        q["window"] = e.get("window") or {"before": 0, "after": 0}
        q["rows"] = e.get("rows") or []
        entries.append(q)
    return d, entries


# ----------------------------------------------------------------------------- walking the tree
_GLOB_CACHE = {}


def _glob_rx(pat):
    """Path-aware glob: * and ? stop at a slash, ** crosses slashes."""
    rx = _GLOB_CACHE.get(pat)
    if rx is None:
        out, i = "", 0
        while i < len(pat):
            c = pat[i]
            if pat.startswith("**", i):
                out += ".*"
                i += 2
                continue
            out += "[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c)
            i += 1
        rx = _GLOB_CACHE[pat] = re.compile("^" + out + "$")
    return rx


def glob_match(rel, pat):
    return pat == "*" or bool(_glob_rx(pat).match(rel))


def _matches(rel, pat):
    """rel is a posix path relative to the root. A pattern ending in / is a directory prefix."""
    if pat.endswith("/"):
        base = pat[:-1]
        return rel == base or rel.startswith(base + "/") or glob_match(rel, base) or any(glob_match("/".join(rel.split("/")[:n]), base) for n in range(1, len(rel.split("/"))))
    return rel == pat or glob_match(rel, pat)


def resolve_row(p, rel, line):
    """The Table 4 row a hit is filed under: the first attribution entry that matches the file (and the line), else the pattern's own row."""
    for a in p["attr"]:
        if any(glob_match(rel, g) for g in a["files"]) and (a["rx"] is None or a["rx"].search(line)):
            return a["row_id"]
    return p["row_id"]


def rows_of(p):
    """Every Table 4 row a pattern can file a hit under."""
    return {p["row_id"]} | {a["row_id"] for a in p["attr"]}


def list_files(root, scan):
    root = Path(root)
    inc, exc = scan["include"], scan["exclude"]
    maxb = int(scan.get("max_file_bytes", 2000000))
    out = []
    seen = set()
    for pat in inc:
        # expand a glob such as research/*-fixtures/ into real folders
        base = pat.rstrip("/")
        if any(ch in base for ch in "*?["):
            cands = sorted(p for p in root.glob(base) if p.is_dir())
        else:
            cands = [root / base] if (root / base).exists() else []
        for c in cands:
            if c.is_file():
                walk = [c]
            else:
                walk = []
                for dp, dn, fn in os.walk(c):
                    dn[:] = sorted(d for d in dn if d not in (".git", "node_modules", "__pycache__", "vendor"))
                    for f in sorted(fn):
                        walk.append(Path(dp) / f)
            for f in walk:
                rel = f.relative_to(root).as_posix()
                if rel in seen:
                    continue
                if any(_matches(rel, e) for e in exc):
                    continue
                try:
                    if f.is_symlink() or not f.is_file() or f.stat().st_size > maxb:
                        continue
                except OSError:
                    continue
                seen.add(rel)
                out.append(rel)
    return sorted(out)


def read_lines(root, rel):
    try:
        raw = (Path(root) / rel).read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192] and not (raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff")):
        return None  # binary
    try:
        if raw.startswith(b"\xef\xbb\xbf"):
            text = raw[3:].decode("utf-8", errors="replace")
        elif raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
            text = raw.decode("utf-16", errors="replace")
        else:
            text = raw.decode("utf-8", errors="replace")
    except UnicodeError:
        return None
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


# ----------------------------------------------------------------------------- scanning
def kind_of(rel, line):
    if CHANGELOG_RX.match(line):
        return "changelog"
    ext = Path(rel).suffix.lower()
    if ext == ".csv":
        return "data"
    if ext in CODE_EXT:
        return "code"
    return "prose"


def excerpt(line, m):
    s = line.strip()
    off = len(line) - len(line.lstrip())
    a, b = m.start() - off, m.end() - off
    lo, hi = max(0, a - 55), min(len(s), b + 55)
    t = s[lo:hi].replace("`", "'")
    return ("..." if lo > 0 else "") + t + ("..." if hi < len(s) else "")


def fingerprint(rel, pid, line):
    norm = " ".join(line.split())
    return hashlib.sha1(("%s|%s|%s" % (rel, pid, norm)).encode("utf-8")).hexdigest()[:16]


def allow_for(entries, rel, row_id, lines, idx):
    """Return the id of the first allowlist entry that suppresses a hit on lines[idx], or None."""
    for e in entries:
        if e["rows"] and row_id not in e["rows"]:
            continue
        if not (e["file"] == "*" or e["file"] == rel or glob_match(rel, e["file"])):
            continue
        b, a = int(e["window"].get("before", 0)), int(e["window"].get("after", 0))
        ctx = "\n".join(lines[max(0, idx - b): idx + a + 1])
        if e["rx"].search(ctx):
            return e["id"]
    return None


def scan_tree(root, doc, pats, infos, entries):
    files = list_files(root, doc["scan"])
    hits, info_hits = [], []
    nlines = 0
    for rel in files:
        lines = read_lines(root, rel)
        if lines is None:
            continue
        nlines += len(lines)
        here = [p for p in pats if not p["only_files"] or any(glob_match(rel, g) for g in p["only_files"])]
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            for p in here:
                for m in p["rx"].finditer(line):
                    row_id = resolve_row(p, rel, line)
                    aid = allow_for(entries, rel, row_id, lines, i)
                    hits.append({"row_id": row_id, "pattern": p["id"], "severity": p["severity"], "file": rel, "line": i + 1,
                                 "kind": kind_of(rel, line), "retirement_note": bool(RETIRE_RX.search(line)), "excerpt": excerpt(line, m), "allowed": bool(aid), "allow_id": aid,
                                 "fp": fingerprint(rel, p["id"], line)})
            for p in infos:
                for m in p["rx"].finditer(line):
                    info_hits.append({"info": p["id"], "file": rel, "line": i + 1, "excerpt": excerpt(line, m)})
    hits.sort(key=lambda h: (h["file"], h["line"], h["pattern"]))
    info_hits.sort(key=lambda h: (h["file"], h["line"], h["info"]))
    return files, nlines, hits, info_hits


# ----------------------------------------------------------------------------- the report
def build_report(doc, rows, files, nlines, hits, info_hits, infos, root_label):
    live = [h for h in hits if not h["allowed"]]
    row_ids = [r["row_id"] for r in doc["rows"]]
    per_row = []
    for rid in row_ids:
        r = rows[rid]
        hs = [h for h in live if h["row_id"] == rid]
        per_row.append({"row_id": rid, "status": r["status"], "coverage": r["coverage"], "stale": r["stale"], "canonical": r["canonical"], "owner": r["owner"],
                        "fail": sum(1 for h in hs if h["severity"] == "FAIL"), "warn": sum(1 for h in hs if h["severity"] == "WARN"),
                        "allowlisted": sum(1 for h in hits if h["allowed"] and h["row_id"] == rid),
                        "fail_changelog": sum(1 for h in hs if h["severity"] == "FAIL" and h["kind"] == "changelog"),
                        "files": sorted(set(h["file"] for h in hs))})
    order = {rid: i for i, rid in enumerate(row_ids)}
    regress = sorted((h for h in live if rows[h["row_id"]]["status"] in APPLIED), key=lambda h: (order[h["row_id"]], h["file"], h["line"], h["pattern"]))
    work = []
    for r in per_row:
        if r["status"] == "outstanding":
            work.append({"row_id": r["row_id"], "canonical": r["canonical"], "owner": r["owner"],
                         "hits": [h for h in live if h["row_id"] == r["row_id"]]})
    info = []
    for p in infos:
        hs = [h for h in info_hits if h["info"] == p["id"]]
        byfile = {}
        for h in hs:
            byfile[h["file"]] = byfile.get(h["file"], 0) + 1
        info.append({"id": p["id"], "suggested_row": p["suggested_row"], "description": p["description"], "total": len(hs), "files": dict(sorted(byfile.items()))})
    notcheck = []
    for r in doc["rows"]:
        if r["coverage"] != "full":
            notcheck.append({"row_id": r["row_id"], "coverage": r["coverage"],
                             "reason": r.get("coverage_note") or "only the phrases listed in the pattern file are searched; a reworded copy needs a human reader"})
    return {
        "schema": "lj-stale-report/1", "tool": "scripts/stale_check.py", "date_utc": today(), "root": root_label,
        "patterns_version": doc.get("version"),
        "scanned": {"include": doc["scan"]["include"], "exclude": doc["scan"]["exclude"], "files": len(files), "lines": nlines},
        "summary": {"fail": sum(1 for h in live if h["severity"] == "FAIL"), "warn": sum(1 for h in live if h["severity"] == "WARN"),
                    "allowlisted": sum(1 for h in hits if h["allowed"]), "regressions": len(regress),
                    "regressions_that_look_like_retirement_notes": sum(1 for h in regress if h["retirement_note"]),
                    "regressions_in_changelog_lines": sum(1 for h in regress if h["kind"] == "changelog"),
                    "outstanding_hits": sum(len(w["hits"]) for w in work), "info_candidates_total": sum(i["total"] for i in info)},
        "rows": per_row, "regressions": regress, "work_orders": work, "not_machine_checkable": notcheck, "info_candidates": info,
        "allowlisted_by_entry": _count_by(h["allow_id"] for h in hits if h["allowed"]),
        "hits": live,
    }


def _count_by(it):
    out = {}
    for k in it:
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def md_safe(s):
    return s.replace("|", "/").replace("\n", " ")


def render_md(rep):
    L = []
    s = rep["summary"]
    L.append("# Stale-copy check report (W-29)")
    L.append("")
    L.append("Generated by `scripts/stale_check.py` on %s (UTC date). Read-only: nothing was fixed. Patterns version %s. Scanned %d files, %d lines." % (rep["date_utc"], rep["patterns_version"], rep["scanned"]["files"], rep["scanned"]["lines"]))
    L.append("")
    L.append("Scanned: %s." % ", ".join("`%s`" % x for x in rep["scanned"]["include"]))
    L.append("Excluded (historical or authoritative): %s." % ", ".join("`%s`" % x for x in rep["scanned"]["exclude"][:14]))
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Measure | Count |")
    L.append("|---|---|")
    L.append("| FAIL hits (not allowlisted) | %d |" % s["fail"])
    L.append("| WARN hits (a human decides) | %d |" % s["warn"])
    L.append("| Allowlisted hits (the W-29 allowlist) | %d |" % s["allowlisted"])
    L.append("| REGRESSIONS (hits on rows Table 4 marks applied) | %d |" % s["regressions"])
    L.append("| of which the line says retired, superseded, replaced or absent (a reading aid, not a filter) | %d |" % s["regressions_that_look_like_retirement_notes"])
    L.append("| of which changelog lines | %d |" % s["regressions_in_changelog_lines"])
    L.append("| Outstanding-row hits (the Haiku work order) | %d |" % s["outstanding_hits"])
    L.append("| INFO candidate hits (never fail the check) | %d |" % s["info_candidates_total"])
    L.append("")
    L.append("Exit code of this run: %s." % ("1 (non-allowlisted FAIL hits exist; expected until the outstanding rows are patched)" if s["fail"] else "0"))
    L.append("")
    L.append("## Every Table 4 row")
    L.append("")
    L.append("| Row | Status | Coverage | FAIL | WARN | Allowlisted | Of FAIL: changelog lines | Files with hits |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rep["rows"]:
        L.append("| %s | %s | %s | %d | %d | %d | %d | %s |" % (r["row_id"], r["status"], r["coverage"], r["fail"], r["warn"], r["allowlisted"], r["fail_changelog"],
                                                          ", ".join("`%s`" % f for f in r["files"][:4]) + (" +%d" % (len(r["files"]) - 4) if len(r["files"]) > 4 else "") if r["files"] else "-"))
    L.append("")
    L.append("## REGRESSIONS: hits on rows that Table 4 marks applied")
    L.append("")
    if not rep["regressions"]:
        L.append("None.")
    else:
        L.append("This is what the scribes thought they fixed but did not (or a changelog or note that still quotes the old value; the `kind` says which). One line per hit: `file:line [pattern, severity, kind]` then the text around the match.")
        L.append("")
        cur = None
        for h in rep["regressions"]:
            if h["row_id"] != cur:
                cur = h["row_id"]
                r = next(x for x in rep["rows"] if x["row_id"] == cur)
                L.append("")
                L.append("### %s (%s): canonical value: %s" % (cur, r["status"], md_safe(r["canonical"])))
                L.append("")
            L.append("- `%s:%d` [%s, %s, %s%s] %s" % (h["file"], h["line"], h["pattern"], h["severity"], h["kind"], ", retirement note?" if h["retirement_note"] else "", md_safe(h["excerpt"])))
    L.append("")
    L.append("## WORK ORDERS: rows Table 4 marks outstanding")
    L.append("")
    for w in rep["work_orders"]:
        r = next(x for x in rep["rows"] if x["row_id"] == w["row_id"])
        L.append("### %s: %d hit(s); owner: %s" % (w["row_id"], len(w["hits"]), md_safe(w["owner"])))
        L.append("")
        L.append("Stale: %s" % md_safe(r["stale"]))
        L.append("")
        L.append("Canonical: %s" % md_safe(w["canonical"]))
        L.append("")
        if not w["hits"]:
            L.append("No hits.")
        cur = None
        for h in w["hits"]:
            if h["file"] != cur:
                cur = h["file"]
                L.append("")
                L.append("`%s`" % cur)
                L.append("")
            L.append("- line %d [%s, %s, %s%s] %s" % (h["line"], h["pattern"], h["severity"], h["kind"], ", retirement note?" if h["retirement_note"] else "", md_safe(h["excerpt"])))
        L.append("")
    L.append("## Not machine-checkable (prose)")
    L.append("")
    if not rep["not_machine_checkable"]:
        L.append("None.")
    for n in rep["not_machine_checkable"]:
        L.append("- **%s** (%s): %s" % (n["row_id"], n["coverage"], n["reason"]))
    L.append("")
    L.append("All other rows are covered by at least one pattern; a row with zero hits above is clean for the phrases it searches, not proof that no reworded copy exists.")
    L.append("")
    L.append("## INFO: candidate new Table 4 rows (never affect the exit code)")
    L.append("")
    if rep["info_candidates"]:
        L.append("Consequences of D-27, D-28 and D-29 that Table 4 does not yet cover. Counts are over the same scanned files.")
    else:
        L.append("None today. Minecraft, voxel, Mojang and the placeholder observances were INFO candidates until register v3 made them Table 4 rows S-42 to S-65; they are FAIL patterns now. New candidates go in the pattern file's `info` list.")
    L.append("")
    for i in rep["info_candidates"]:
        L.append("### %s: %d hit(s); suggested row: %s" % (i["id"], i["total"], md_safe(i["suggested_row"])))
        L.append("")
        L.append(i["description"])
        L.append("")
        for f, n in list(i["files"].items())[:25]:
            L.append("- `%s`: %d" % (f, n))
        if len(i["files"]) > 25:
            L.append("- ... and %d more files" % (len(i["files"]) - 25))
        L.append("")
    L.append("## Allowlisted hits by entry")
    L.append("")
    for k, v in rep["allowlisted_by_entry"].items():
        L.append("- `%s`: %d" % (k, v))
    L.append("")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- baseline
def write_baseline(path, doc, hits):
    live = [h for h in hits if not h["allowed"]]
    by_row = {}
    for h in live:
        by_row.setdefault(h["row_id"], {"FAIL": 0, "WARN": 0})[h["severity"]] += 1
    data = {"schema": "lj-stale-baseline/1", "date_utc": today(), "patterns_version": doc.get("version"),
            "note": "Today's hits: counts and locations. --new-only compares the fingerprint (file, pattern, normalised line text), not the line number, so inserting lines does not make old hits look new.",
            "counts": {"FAIL": sum(1 for h in live if h["severity"] == "FAIL"), "WARN": sum(1 for h in live if h["severity"] == "WARN"), "by_row": dict(sorted(by_row.items()))},
            "hits": [{"fp": h["fp"], "file": h["file"], "line": h["line"], "row_id": h["row_id"], "pattern": h["pattern"], "severity": h["severity"]} for h in live]}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8", newline="\n")
    return data


def load_baseline(path):
    d = _load_json(path, "the baseline file")
    if d.get("schema") != "lj-stale-baseline/1" or not isinstance(d.get("hits"), list):
        raise Invalid("the baseline file is not a stale baseline")
    counts = {}
    for h in d["hits"]:
        counts[h["fp"]] = counts.get(h["fp"], 0) + 1
    return d, counts


def new_hits(hits, base_counts):
    left = dict(base_counts)
    new = []
    for h in hits:
        if h["allowed"]:
            continue
        if left.get(h["fp"], 0) > 0:
            left[h["fp"]] -= 1
        else:
            new.append(h)
    gone = sum(v for v in left.values() if v > 0)
    return new, gone


# ----------------------------------------------------------------------------- the register (DECISIONS.md)
def read_register(path):
    """Table rows of the register as {id: [cells]} for ids such as S-01 and O-84, or None if the file is missing."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except OSError:
        return None
    out = {}
    for line in text.split("\n"):
        m = re.match(r"^\| ([A-Z]{1,2}-[0-9]+) \|", line)
        if m and m.group(1) not in out:
            out[m.group(1)] = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
    return out


def register_status(cell):
    """The row status a Status cell stands for. A cell that still has outstanding work (even beside 'applied today' for the register,
    the roadmap and the plan page, which are not scanned) is outstanding for the scanned tree."""
    low = cell.lower()
    if "outstanding" in low:
        return "outstanding"
    if "applied today" in low:
        return "applied today"
    if "applied" in low:
        return "applied"
    return None


def last_number(register, prefix):
    nums = [int(k[len(prefix):]) for k in register if k.startswith(prefix) and k[len(prefix):].isdigit()]
    return max(nums) if nums else None


# ----------------------------------------------------------------------------- self-test
def self_test(doc, pats, infos, rows, adoc, entries, register=None, register_label="DECISIONS.md"):
    problems = []
    ok = 0

    def chk(cond, msg):
        nonlocal ok
        if cond:
            ok += 1
        else:
            problems.append(msg)

    for p in pats + infos:
        pos, neg = p.get("positive_samples") or [], p.get("negative_samples") or []
        chk(len(pos) >= 1, "%s has no positive sample" % p["id"])
        chk(len(neg) >= 1, "%s has no negative sample" % p["id"])
        for s in pos:
            chk(p["rx"].search(s) is not None, "%s: positive sample not matched: %r" % (p["id"], s))
        for s in neg:
            chk(p["rx"].search(s) is None, "%s: negative sample matched: %r" % (p["id"], s))
    # Table 4 is the source of truth: every S-nn id in the register needs a row here (nothing is hard-coded, so the next growth is a JSON edit)
    reg_s = sorted(k for k in register if re.match(r"^S-[0-9]+$", k)) if register else []
    if reg_s:
        print("register check: %d Table 4 ids (%s to %s) read from %s" % (len(reg_s), reg_s[0], reg_s[-1], register_label))
    else:
        print("register check: SKIPPED (no Table 4 rows found in %s); rows are checked against the pattern file only" % register_label)
    want = sorted(set(reg_s) | {"W-29"} | set(rows))
    for rid in want:
        chk(rid in rows, "Table 4 row %s is missing from the pattern file's rows[] (add the row and its patterns; the baseline is re-cut the same day)" % rid)
        r = rows.get(rid)
        if reg_s and rid not in reg_s and rid != "W-29":
            chk(False, "row %s is in the pattern file but not in Table 4 of the register" % rid)
        if r:
            n = sum(1 for p in pats if rid in rows_of(p))
            if r["coverage"] in ("full", "partial"):
                chk(n >= 1, "row %s claims coverage %s but has no pattern" % (rid, r["coverage"]))
            else:
                chk(r["coverage"] == "none" and bool(r.get("coverage_note")), "row %s is not machine-checkable (coverage %r) and gives no coverage_note" % (rid, r["coverage"]))
            chk(r["status"] in ("outstanding", "applied", "applied today", "check"), "row %s has status %r" % (rid, r["status"]))
            if reg_s and rid in reg_s:
                want_status = register_status(register[rid][-1])
                chk(want_status is None or r["status"] == want_status,
                    "row %s has status %r but Table 4 says %r (update the row's status here when Table 4 changes)" % (rid, r["status"], want_status))
    for p in pats:
        for rid in sorted(rows_of(p)):
            chk(rid in rows, "pattern %s names an unknown row %s" % (p["id"], rid))
        if p["only_files"] or p["attr"]:
            chk(all(isinstance(g, str) and g for g in p["only_files"]) and all(a["files"] for a in p["attr"]), "pattern %s has an empty file glob" % p["id"])
        if p.get("register_prefix"):
            # a pattern bounded by the register's last row (an O-row above O-84): the bound must be the register's own last row
            pre, last = p["register_prefix"], p.get("register_last", "")
            if register:
                n = last_number(register, pre)
                chk(n is not None and last == "%s%d" % (pre, n),
                    "pattern %s stops at %s but the register's last %s row is %s (extend the pattern in the same pass as the register edit)" % (p["id"], last, pre, "%s%s" % (pre, n)))
                chk(n is not None and p["rx"].search("%s%d" % (pre, n + 1)) is not None and p["rx"].search("%s%d" % (pre, n)) is None,
                    "pattern %s must match %s%s and must not match %s%s" % (p["id"], pre, (n or 0) + 1, pre, n))
    # the allowlist: ids unique, every entry cites the W-29 row, and the count is the file's own (a new W-29 context is an orchestrator edit of the file)
    chk(len(entries) == len(adoc.get("entries", [])) and len(set(e["id"] for e in entries)) == len(entries), "allowlist entry ids must be unique (%d entries)" % len(entries))
    chk(all(e.get("register_row") == "W-29" for e in entries), "every allowlist entry must cite register_row W-29")
    print("allowlist: %d entries (%d structural), %d patterns, %d rows" % (len(entries), sum(1 for e in entries if e.get("structural")), len(pats), len(rows)))
    # allowlist samples, end to end in a throw-away tree
    with tempfile.TemporaryDirectory(prefix="lj-stale-selftest-") as td:
        tdp = Path(td)
        for e in entries:
            chk(len(e.get("positive_samples") or []) >= 1 and len(e.get("negative_samples") or []) >= 1, "allowlist %s needs a positive and a negative sample" % e["id"])
            rel = e["file"] if "*" not in e["file"] else "playbooks/sample.md"
            (tdp / rel).parent.mkdir(parents=True, exist_ok=True)
            for sample, expect_allowed in [(s, True) for s in e.get("positive_samples", [])] + [(s, False) for s in e.get("negative_samples", [])]:
                (tdp / rel).write_text("# sample\n" + sample + "\n", encoding="utf-8")
                _f, _n, hs, _i = scan_tree(tdp, {"scan": {"include": ["playbooks/", "."], "exclude": [], "max_file_bytes": 100000}}, pats, [], entries)
                hs = [h for h in hs if h["file"] == rel and h["row_id"] in (e["rows"] or [h["row_id"]])]
                if expect_allowed and e.get("structural"):
                    # a structural entry suppresses nothing on today's tree: its positive sample is text the entry's context describes
                    # but that no live line contains, or that the pattern does not hit at all (AL-4). Either way the sample has no LIVE hit.
                    chk(e["rx"].search(sample) is not None, "allowlist %s (structural): the context regex does not describe its own sample: %r" % (e["id"], sample))
                    chk(not any(not h["allowed"] for h in hs), "allowlist %s (structural): its positive sample is still a live hit, so the entry does not do its job: %r (hits %s)" % (e["id"], sample, [(h["pattern"], h["allowed"]) for h in hs]))
                elif expect_allowed:
                    chk(bool(hs) and all(h["allowed"] and h["allow_id"] for h in hs), "allowlist %s: positive sample not fully suppressed: %r (hits %s)" % (e["id"], sample, [(h["pattern"], h["allowed"]) for h in hs]))
                else:
                    chk(bool(hs) and any(not h["allowed"] for h in hs), "allowlist %s: negative sample should still be a live hit: %r" % (e["id"], sample))
            (tdp / rel).unlink()
    # include/exclude behaviour on a throw-away tree
    with tempfile.TemporaryDirectory(prefix="lj-stale-selftest-") as td:
        tdp = Path(td)
        stale = "the L1 process lock is on Sat 14 Nov\n"
        for rel in ["playbooks/a.md", ".claude/skills/x/SKILL.md", "research/q-fixtures/f.py", "research/sources/s.txt", "win/w.ps1", "scripts/t.py", "ops/o.csv",
                    "research/notes.md", "reviews/r.md", "DECISIONS.md", "build/b.md", "scripts/stale_patterns.json", "ops/decisions.csv", "tests/t.md", "research/other/o.md"]:
            (tdp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tdp / rel).write_text(stale, encoding="utf-8")
        files, _n, hs, _i = scan_tree(tdp, doc, pats, [], [])
        found = sorted(set(h["file"] for h in hs))
        want_found = ["ops/o.csv", "playbooks/a.md", "research/q-fixtures/f.py", "research/sources/s.txt", "scripts/t.py", "win/w.ps1", ".claude/skills/x/SKILL.md"]
        chk(found == sorted(want_found), "include/exclude: found %s, wanted %s" % (found, sorted(want_found)))
    print("self-test: %d checks, %d problems" % (ok + len(problems), len(problems)))
    for p in problems:
        print("  FAIL " + p)
    return not problems


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="stale_check.py", allow_abbrev=False, description="W-29 stale-copy check (read-only).")
    ap.add_argument("--root", default=str(ROOT_DEFAULT))
    ap.add_argument("--patterns", default=str(PATTERNS_DEFAULT))
    ap.add_argument("--allowlist", default=str(ALLOWLIST_DEFAULT))
    ap.add_argument("--baseline-file", default=None)
    ap.add_argument("--register", default=None, help="DECISIONS.md for --self-test to read Table 4 from (default: ROOT/DECISIONS.md)")
    ap.add_argument("--json", metavar="OUT.json")
    ap.add_argument("--md", metavar="OUT.md")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--new-only", action="store_true")
    ap.add_argument("--audit-allowlist", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    try:
        args = ap.parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    modes = [args.baseline, args.new_only, args.audit_allowlist, args.self_test, args.strict]
    if sum(1 for m in modes if m) > 1:
        print("choose one of --strict, --baseline, --new-only, --audit-allowlist, --self-test")
        return 2
    try:
        doc, pats, infos, rows = load_patterns(args.patterns)
        adoc, entries = load_allowlist(args.allowlist)
    except Invalid as e:
        print("INVALID INPUT: %s" % e)
        return 2
    root = Path(args.root)
    base_file = Path(args.baseline_file) if args.baseline_file else (root / "scripts" / "stale_baseline.json")

    if args.self_test:
        reg_path = Path(args.register) if args.register else root / "DECISIONS.md"
        register = read_register(reg_path)
        label = "the --register file" if args.register else "ROOT/DECISIONS.md"
        return 0 if self_test(doc, pats, infos, rows, adoc, entries, register=register, register_label=label) else 1

    if not root.is_dir():
        print("ENVIRONMENT: the tree to scan does not exist")
        return 3
    files, nlines, hits, info_hits = scan_tree(root, doc, pats, infos, entries)
    live = [h for h in hits if not h["allowed"]]
    fail = [h for h in live if h["severity"] == "FAIL"]
    warn = [h for h in live if h["severity"] == "WARN"]

    if args.audit_allowlist:
        used = {}
        for h in hits:
            if h["allowed"]:
                used[h["allow_id"]] = used.get(h["allow_id"], 0) + 1
        unused = [e for e in entries if used.get(e["id"], 0) == 0]
        # an entry marked structural suppresses nothing by construction (its reason is in the allowlist): not dead
        dead = [e["id"] for e in unused if not e.get("structural")]
        by_design = [e["id"] for e in unused if e.get("structural")]
        for e in entries:
            tag = "   DEAD" if e["id"] in dead else ("   unused by design (structural)" if e["id"] in by_design else "")
            print("%-42s suppresses %3d hit(s)%s" % (e["id"], used.get(e["id"], 0), tag))
        for i in by_design:
            print("  %s: %s" % (i, next(e["structural_reason"] for e in entries if e["id"] == i)))
        if dead:
            print("audit: %d dead entry(ies): %s" % (len(dead), ", ".join(dead)))
            return 1
        print("audit: no dead entries (%d entries%s)" % (len(entries), ", %d unused by design" % len(by_design) if by_design else ""))
        return 0

    if args.baseline:
        data = write_baseline(base_file, doc, hits)
        print("baseline written: %d FAIL and %d WARN hits recorded (file: %s)" % (data["counts"]["FAIL"], data["counts"]["WARN"], "scripts/stale_baseline.json" if args.baseline_file is None else "the --baseline-file path"))
        return 0

    if args.new_only:
        try:
            bdoc, bcounts = load_baseline(base_file)
        except Invalid as e:
            print("INVALID INPUT: %s (run --baseline first)" % e)
            return 2
        new, gone = new_hits(hits, bcounts)
        nf = [h for h in new if h["severity"] == "FAIL"]
        nw = [h for h in new if h["severity"] == "WARN"]
        for h in nf + nw:
            print("NEW %s %s:%d [%s] %s" % (h["severity"], h["file"], h["line"], h["pattern"], h["excerpt"]))
        print("new-only: %d new FAIL hit(s), %d new WARN hit(s); %d baseline hit(s) no longer present" % (len(nf), len(nw), gone))
        return 1 if nf else 0

    rep = build_report(doc, rows, files, nlines, hits, info_hits, infos, "repository root")
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if args.md:
        Path(args.md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.md).write_text(render_md(rep), encoding="utf-8", newline="\n")
    if args.strict:
        for h in fail:
            print("FAIL %s %s:%d [%s] %s" % (h["row_id"], h["file"], h["line"], h["pattern"], h["excerpt"]))
        print("strict: %d FAIL hit(s) (%d WARN not counted)" % (len(fail), len(warn)))
        return 1 if fail else 0
    if not args.quiet:
        s = rep["summary"]
        print("stale_check: scanned %d files, %d lines" % (rep["scanned"]["files"], rep["scanned"]["lines"]))
        print("  FAIL %d, WARN %d, allowlisted %d, REGRESSIONS %d, outstanding-row hits %d, INFO candidate hits %d" % (s["fail"], s["warn"], s["allowlisted"], s["regressions"], s["outstanding_hits"], s["info_candidates_total"]))
        for r in rep["rows"]:
            if r["fail"] or r["warn"]:
                print("  %-5s %-13s FAIL %3d WARN %3d allowlisted %3d" % (r["row_id"], r["status"], r["fail"], r["warn"], r["allowlisted"]))
        if args.json or args.md:
            print("  report written to the --json / --md paths")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
