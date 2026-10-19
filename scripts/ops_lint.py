#!/usr/bin/env python3
"""ops_lint.py - check the week-1 ops files (WP-02) against the register and the redaction rules.

WHAT IT CHECKS (read-only; it never writes, moves or deletes anything)
  1. ops/decisions.csv against DECISIONS.md: same ID set (compared by a plain scan of the
     register AND by the generator's parser; the number of lines that look like a register row,
     emphasis marks around the ID included, must equal the generator's row count), no
     duplicates, valid status words, exact header, every generated column equal
     (orchestrator-owned columns are ignored).
  2. ops/hours.csv: exact header, activity enum, `who` is exactly maker or agent (a who column
     in a public repository is a name slot), date/minutes/ID shapes, and every cell
     against the identifying-data patterns and the local deny list; a note over 80
     characters is a WARNING (probably prose about a person).
  3. ops/SETTINGS-CARD.md: rows TD-1..TD-4, Colour, Sound, Phone (PH1 and PH2: W-63), Script
     stack, Fonts and Burn-in path (the rows W-16 and O-14 say the maker signs on Sun 1 Nov)
     with their register IDs and key values, the "Language and script" line, a "signed:" line,
     no unverified-on-Windows claim, and every cited D-/W-/O-/S- ID exists in DECISIONS.md. When
     pipeline/phone/test_strings.json exists, the scripts the "Caption and font test ran in:"
     line says were tested must have strings there (else a note says it was not cross-checked).
  4. ops/GATHER.md: Part A / Part B headings, the Part B gate sentence, the required
     IDs (five stand-in scans LJ-ST-0001..0005 front and back, OBJ, REC, DEV, ERA, FP, HUM, SND),
     stand-in box code only in Part A and never in Part B, no real-box scan ID in Part A,
     every cited register ID exists.
  5. Every text file under ops/ (.md .csv .json .txt): no e-mail, IP, MAC, profile path,
     token, GUID/serial or at-sign handle, no placeholder marker (the word TODO or FIXME),
     and no name from the local deny list.

WHERE "IDENTIFYING DATA" COMES FROM (build plan 4.13)
  Every pattern is read from scripts/redaction_patterns.json (owner WP-03). This tool
  carries no regex of its own for e-mail, IP, MAC, paths, tokens, GUIDs or handles. If
  that file is missing or invalid the tool FAILS CLOSED: it prints why and exits 2.
  The local deny list (the maker's real names, kept on the maker's PC only) is read from
  scripts/public_lint.deny.local.txt when it exists, from each --deny-file, from the
  file named by the environment variable LJ_DENY_FILE, and, in --hours mode, from a file
  beside the checked file with the same base name and the extension .deny.txt (tests).
  A deny entry is matched as a whole word, case-insensitively; entries under 3 characters
  are skipped with a note. Findings print the category, file:line and a MASKED hit (the
  first two characters, then at most 8 asterisks: the mask section of the pattern file, the
  same as public_lint prints), never the full value and never its length.

HOW TO RUN (standard library only; always with -I)
  python3 -I scripts/ops_lint.py                         # everything under ops/
  python3 -I scripts/ops_lint.py --hours FILE            # only one hours file
  python3 -I scripts/ops_lint.py --strict                # warnings also fail
  Other options: --root DIR (repository root, default: the folder above scripts/),
  --ops-dir DIR, --register FILE, --patterns FILE, --deny-file FILE (repeatable), --json.

EXIT CODES (build plan 4.3)
  0 all checks pass (warnings allowed unless --strict); 1 a check failed or identifying data
  was found (the acceptance tests ask for 1 here); 2 bad usage, or the pattern file is
  missing/invalid (fail closed); 3 not used.
"""
import argparse
import csv
import importlib.util
import io
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED_CATEGORIES = ["email", "ipv4", "ipv6", "mac", "profile_path_windows",
                       "profile_path_linux", "token_shape", "guid_serial", "handle"]
TEXT_SUFFIXES = (".md", ".csv", ".json", ".txt")
MARKERS = ["TO" + "DO", "FIX" + "ME"]  # built from parts so this file does not contain them
NOTE_WARN_LEN = 80
REG_ID_RE = re.compile(r"\b([DWOS])-([0-9]{2,3})\b")  # two or three digits: W-60 today, W-100 possible
# What a register row is (the ID cell may carry an annotation, `| O-06 (absorbs O-40) |`) is defined
# once, as ROW_RE in decisions_to_csv.py; check_decisions() uses it through the loaded sibling.
LJ_ID_RE = re.compile(r"\bLJ-([A-Z0-9]{1,4})-([0-9]{4})-([FB])(?:-R[0-9]+)?\b")


def load_sibling(name):
    path = os.path.join(HERE, name + ".py")
    spec = importlib.util.spec_from_file_location("lj_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Findings:
    def __init__(self):
        self.fail = []   # (file, line, category, text)
        self.warn = []
        self.notes = []
        self.passes = []

    def add_fail(self, file, line, category, text):
        self.fail.append((file, line, category, text))

    def add_warn(self, file, line, category, text):
        self.warn.append((file, line, category, text))


# ---------------------------------------------------------------- pattern file (4.13)

class PatternError(Exception):
    pass


class Patterns:
    def __init__(self, path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except OSError as exc:
            raise PatternError("cannot read the pattern file (%s)" % exc.strerror)
        except ValueError as exc:
            raise PatternError("the pattern file is not valid JSON (%s)" % str(exc)[:80])
        cats = data.get("categories") if isinstance(data, dict) else None
        if not isinstance(cats, list) or not cats:
            raise PatternError("the pattern file has no 'categories' list")
        self.categories = []
        ids = set()
        for c in cats:
            if not isinstance(c, dict) or "id" not in c or "regex" not in c:
                raise PatternError("a category lacks 'id' or 'regex'")
            flags = re.I if str(c.get("flags", "")) == "i" else 0
            try:
                rx = re.compile(c["regex"], flags)
            except re.error as exc:
                raise PatternError("category %s does not compile (%s)" % (c["id"], exc))
            ids.add(c["id"])
            scope = c.get("scope", "both")
            if scope in ("text", "both"):
                self.categories.append((c["id"], rx, c))
        missing = [i for i in REQUIRED_CATEGORIES if i not in ids]
        if missing:
            raise PatternError("required categories missing: " + ", ".join(missing))
        self.exemptions = []
        for e in data.get("exemptions", []) or []:
            if isinstance(e, dict) and "regex" in e:
                try:
                    flags = re.I if str(e.get("flags", "")) == "i" else 0
                    self.exemptions.append((e.get("id", "exemption"), re.compile(e["regex"], flags), e))
                except re.error as exc:
                    raise PatternError("exemption %s does not compile (%s)" % (e.get("id"), exc))
        mask = data.get("mask") or {}
        self.keep = int(mask.get("keep", 2))
        self.fill = str(mask.get("fill", "*")) or "*"
        self.cap = int(mask.get("cap", 8))  # same mask as public_lint: a hit's length does not leak
        nc = data.get("name_checks") or {}
        self.min_name_len = int(nc.get("min_name_len", 3))
        self.placeholders = [str(p) for p in (data.get("placeholders") or [])]
        ld = data.get("local_deny")
        self.local_deny_rel = None
        if isinstance(ld, str):
            self.local_deny_rel = ld
        elif isinstance(ld, dict):
            self.local_deny_rel = ld.get("path") or ld.get("file")
        self.version = data.get("version")

    def mask(self, hit):
        hit = hit.strip()
        if len(hit) <= self.keep:
            return self.fill * max(len(hit), 1)
        return hit[:self.keep] + self.fill * min(len(hit) - self.keep, self.cap)

    def exempt(self, category, start, end, line):
        for _id, rx, e in self.exemptions:
            applies = e.get("applies_to") or e.get("categories") or e.get("category") or e.get("category_id")
            if applies:
                applies = [applies] if isinstance(applies, str) else list(applies)
                if category not in applies:
                    continue
            for m in rx.finditer(line):
                if m.start() <= start and m.end() >= end:
                    return True
        return False

    def scan_line(self, line):
        """Return [(category, hit)] for one line of text."""
        out = []
        for cid, rx, _c in self.categories:
            for m in rx.finditer(line):
                hit = m.group(0)
                if not hit or hit in self.placeholders:
                    continue
                if self.exempt(cid, m.start(), m.end(), line):
                    continue
                out.append((cid, hit))
        return out


def load_deny(paths, patterns, findings):
    """Read deny lists; return a list of (display_mask, compiled regex)."""
    entries = []
    for p in paths:
        if not p or not os.path.isfile(p):
            continue
        try:
            raw = read_text_file(p).splitlines()  # UTF-8, UTF-8 BOM, UTF-16 or Windows-1252: Notepad writes any
        except OSError:
            findings.notes.append("a deny list could not be read and was skipped")
            continue
        for item in raw:
            name = item.strip()
            if not name or name.startswith("#"):
                continue
            if len(name) < patterns.min_name_len:
                findings.notes.append("a deny-list entry under %d characters was skipped "
                                      "(it would match ordinary words)" % patterns.min_name_len)
                continue
            body = r"\s+".join(re.escape(w) for w in name.split())
            entries.append((patterns.mask(name), re.compile(r"(?<!\w)" + body + r"(?!\w)", re.I | re.U)))
    return entries


# ---------------------------------------------------------------- text scanning

def scan_text(label, text, patterns, deny, findings, column_of=None):
    """Scan a file's text line by line for identifying data and placeholder markers."""
    for n, line in enumerate(text.splitlines(), 1):
        for cid, hit in patterns.scan_line(line):
            where = column_of(n, line, hit) if column_of else ""
            findings.add_fail(label, n, cid, ("%s: " % where if where else "") + "masked hit " + patterns.mask(hit))
        for display, rx in deny:
            m = rx.search(line)
            if m:
                where = column_of(n, line, m.group(0)) if column_of else ""
                findings.add_fail(label, n, "local_deny",
                                  ("%s: " % where if where else "") + "masked hit " + display)
        for mk in MARKERS:
            if mk in line:
                findings.add_fail(label, n, "placeholder_marker", "an unfinished-work marker is not allowed in ops files")


def read_text_file(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


# ---------------------------------------------------------------- individual checks

def check_hours(path, label, hours_mod, patterns, deny, findings):
    try:
        text = read_text_file(path)
    except OSError as exc:
        findings.add_fail(label, 0, "hours_file", "cannot read the file (%s)" % exc.strerror)
        return
    rows, problems = hours_mod.parse(text)
    for line, msg in problems:
        findings.add_fail(label, line, "hours_format", msg)
    header = hours_mod.HEADER

    def column_of(n, line, hit):
        try:
            cells = next(csv.reader([line]))
        except (csv.Error, StopIteration):
            return ""
        if n == 1:
            return "header"
        if len(cells) == len(header):
            for name, cell in zip(header, cells):
                if hit.lower() in cell.lower():
                    return name
        return ""

    scan_text(label, text, patterns, deny, findings, column_of=column_of)
    for line_no, row in rows:
        if len(row["note"]) > NOTE_WARN_LEN:
            findings.add_warn(label, line_no, "note_length",
                              "note is %d characters (over %d): probably prose about a person; "
                              "shorten it to IDs and relation tokens" % (len(row["note"]), NOTE_WARN_LEN))


def check_decisions(csv_path, register_path, d2c, findings):
    label = "ops/decisions.csv"
    try:
        with open(register_path, "r", encoding="utf-8") as fh:
            reg_text = fh.read()
    except OSError as exc:
        findings.add_fail(label, 0, "register", "cannot read DECISIONS.md (%s)" % exc.strerror)
        return set()
    # plain scan: every line the shared row pattern matches, with no table or cell checks
    reg_ids_plain = ["%s-%s" % (m.group(1), m.group(2))
                     for m in (d2c.ROW_RE.match(ln) for ln in reg_text.splitlines()) if m]
    reg_set = set(reg_ids_plain)
    if len(reg_ids_plain) != len(reg_set):
        findings.add_fail("DECISIONS.md", 0, "register", "the register lists an ID twice")
    # every line that starts like a register row, including an ID wrapped in emphasis or code marks
    # (`| **O-95** |`): the generator must have produced exactly one row for each of them
    looks_like_row = sum(1 for ln in reg_text.splitlines() if d2c.NEAR_MISS_RE.match(ln))
    try:
        rows = d2c.build_rows(d2c.parse_register(reg_text))
    except ValueError as exc:
        findings.add_fail("DECISIONS.md", 0, "register", "the register is malformed: %s" % exc)
        return reg_set
    gen_set = {r["id"] for r in rows}
    if gen_set != reg_set:
        findings.add_fail(label, 0, "parser", "the generator's parser and the plain scan disagree on the ID set")
    if looks_like_row != len(rows):
        findings.add_fail(label, 0, "parser", "%d line(s) start like a register row but the generator made %d row(s): "
                          "a row is being dropped" % (looks_like_row, len(rows)))
    try:
        problems = d2c.compare(rows, csv_path)
    except OSError as exc:
        findings.add_fail(label, 0, "decisions_file", "cannot read the file (%s)" % exc.strerror)
        return reg_set
    except UnicodeDecodeError:
        findings.add_fail(label, 0, "decisions_file", "the file is not valid UTF-8")
        return reg_set
    for p in problems[:60]:
        findings.add_fail(label, 0, "decisions_mismatch", p)
    if len(problems) > 60:
        findings.add_fail(label, 0, "decisions_mismatch", "... and %d more problem(s)" % (len(problems) - 60))
    # independent ID-set comparison, not using the generator's comparison
    try:
        recs = list(csv.reader(io.StringIO(read_text_file(csv_path), newline="")))
        csv_ids = [r[0] for r in recs[1:] if r and r[0]]
        if set(csv_ids) != reg_set:
            miss = sorted(reg_set - set(csv_ids))
            extra = sorted(set(csv_ids) - reg_set)
            if miss:
                findings.add_fail(label, 0, "id_set", "missing from the CSV: " + ", ".join(miss[:10]))
            if extra:
                findings.add_fail(label, 0, "id_set", "not in the register (invented): " + ", ".join(extra[:10]))
        if len(csv_ids) != len(set(csv_ids)):
            findings.add_fail(label, 0, "id_set", "duplicate IDs in the CSV")
    except OSError:
        pass
    return reg_set


def check_cited_ids(label, text, reg_set, findings):
    if not reg_set:
        return
    for n, line in enumerate(text.splitlines(), 1):
        for m in REG_ID_RE.finditer(line):
            rid = "%s-%s" % (m.group(1), m.group(2))
            if rid not in reg_set:
                findings.add_fail(label, n, "cited_id", "%s is cited but is not in DECISIONS.md" % rid)


CARD_ROWS = [
    # (row marker, register IDs that must be cited in that row, strings that must appear in it)
    ("**TD-1", ["W-15"], ["1920x1080"]),
    ("**TD-2", ["W-14"], ["24 fps"]),
    ("**TD-3", ["W-18"], ["FontSize=23", "`MarginV` 20"]),
    ("**TD-4", ["W-17"], ["1080p24", "2K Flat"]),
    ("**Colour", ["W-16"], ["BT.709"]),
    ("**Sound", ["W-19"], ["-1 dBTP", "48 kHz"]),
    ("**Phone", ["D-27", "W-63"], ["(J)", "PHONE-ROW.md", "WP-08", "FontSize=28"]),
    # rows the register says the maker signs on Sun 1 Nov (W-16 "Added 2026-10-19", O-14)
    ("**Script stack", ["W-75"], ["Gujarati"]),
    ("**Fonts", ["W-75"], ["OFL.txt"]),
    ("**Burn-in path", ["W-16"], ["`ass`", "`subtitles`"]),
]


def check_card(path, label, reg_set, findings, test_strings_path=None):
    try:
        text = read_text_file(path)
    except OSError as exc:
        findings.add_fail(label, 0, "card_file", "cannot read the file (%s)" % exc.strerror)
        return
    for needle in ["TD-1", "TD-2", "TD-3", "TD-4", "Phone", "D-27", "Language and script"]:
        if needle not in text:
            findings.add_fail(label, 0, "card_content", "the card does not contain '%s'" % needle)
    lines = text.splitlines()
    for marker, ids, needles in CARD_ROWS:
        row = None
        for n, line in enumerate(lines, 1):
            if line.startswith("| " + marker):
                row = (n, line)
                break
        if row is None:
            findings.add_fail(label, 0, "card_row", "no table row starting with '%s'" % marker.strip("*"))
            continue
        n, line = row
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6 or not all(cells):
            findings.add_fail(label, n, "card_row", "'%s' must have 6 non-empty columns, found %d"
                              % (marker.strip("*"), len(cells)))
            continue
        for rid in ids:
            if rid not in cells[3]:
                findings.add_fail(label, n, "card_row", "'%s' must cite %s in its Register column" % (marker.strip("*"), rid))
        for needle in needles:
            if needle not in line:
                findings.add_fail(label, n, "card_value", "'%s' row lacks the value '%s'" % (marker.strip("*"), needle))
    lang = [ln for ln in lines if "Caption and font test ran in:" in ln]
    if not lang:
        findings.add_fail(label, 0, "card_language", "the 'Caption and font test ran in:' line is missing")
    elif "NOT TESTED" not in lang[0]:
        findings.add_fail(label, 0, "card_language", "the language line must say which scripts are NOT TESTED")
    signed = re.findall(r"^signed:\s*(\S+)\s*$", text, re.M)
    if len(signed) != 1 or signed[0] not in ("no", "yes"):
        findings.add_fail(label, 0, "card_signature", "exactly one 'signed: no' or 'signed: yes' line is required")
    elif signed[0] == "yes":
        if "<date>" in text:
            findings.add_fail(label, 0, "card_signature", "signed: yes but the language line still has the <date> placeholder")
        if not re.search(r"^date signed:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}", text, re.M):
            findings.add_fail(label, 0, "card_signature", "signed: yes but 'date signed:' has no date")
    if "UNVERIFIED" not in text:
        findings.add_fail(label, 0, "card_content", "the card must mark Windows behaviour UNVERIFIED (W-28)")
    check_cited_ids(label, text, reg_set, findings)
    check_card_scripts(text, label, test_strings_path, findings)


def check_card_scripts(card_text, label, path, findings):
    """The scripts the card says were tested must be scripts that have strings in
    pipeline/phone/test_strings.json (4.15), when that file exists."""
    line = [ln for ln in card_text.splitlines() if "Caption and font test ran in:" in ln]
    if not line:
        return
    if not path or not os.path.isfile(path):
        findings.notes.append("pipeline/phone/test_strings.json is not present: the card's tested-script claim was not cross-checked")
        return
    try:
        data = json.loads(read_text_file(path))
        scripts = data.get("scripts", {})
        with_strings = {k.lower() for k, v in scripts.items() if isinstance(v, dict) and v.get("strings")}
    except (ValueError, OSError, AttributeError):
        findings.add_fail(label, 0, "card_scripts", "pipeline/phone/test_strings.json is not valid")
        return
    m = re.search(r"ran in:\s*`?([^;(]*?)\s*(?:\(|\bon\b)", line[0])
    claimed = [x.strip().lower() for x in re.split(r"[,/]| and ", m.group(1)) if x.strip()] if m else []
    if not claimed:
        findings.add_fail(label, 0, "card_scripts", "could not read the tested script names from the language line")
    for sc in claimed:
        if sc not in with_strings:
            findings.add_fail(label, 0, "card_scripts",
                              "the card says '%s' was tested but test_strings.json has no strings for it" % sc)


def check_gather(path, label, reg_set, findings):
    try:
        text = read_text_file(path)
    except OSError as exc:
        findings.add_fail(label, 0, "gather_file", "cannot read the file (%s)" % exc.strerror)
        return
    lines = text.splitlines()
    a_ix = b_ix = None
    for n, line in enumerate(lines):
        if re.match(r"^##\s+Part A\b.*P-LOCK", line, re.I) and a_ix is None:
            a_ix = n
        if re.match(r"^##\s+Part B\b.*Sun 15 Nov.*P-LOCK", line, re.I) and b_ix is None:
            b_ix = n
    if a_ix is None:
        findings.add_fail(label, 0, "gather_parts", "heading 'Part A ... P-LOCK' is missing")
    if b_ix is None:
        findings.add_fail(label, 0, "gather_parts", "heading 'Part B ... Sun 15 Nov ... P-LOCK' is missing")
    if a_ix is not None and b_ix is not None and b_ix < a_ix:
        findings.add_fail(label, 0, "gather_parts", "Part B comes before Part A")
    gate = [ln for ln in lines if re.match(r"^\*\*Gate:", ln)]
    if not gate or not all(s in gate[0] for s in ("P-LOCK", "Sat 14 Nov", "Sun 15 Nov", "D-13")):
        findings.add_fail(label, 0, "gather_gate", "the Part B gate sentence (P-LOCK, Sat 14 Nov, Sun 15 Nov, D-13) is missing")
    elif b_ix is not None:
        gate_ix = [n for n, ln in enumerate(lines) if ln.startswith("**Gate:")][0]
        if gate_ix < b_ix:
            findings.add_fail(label, gate_ix + 1, "gather_gate", "the gate sentence must sit inside Part B")
    required = []
    for i in range(1, 6):
        required += ["LJ-ST-%04d-F" % i, "LJ-ST-%04d-B" % i]
    # ranges are written "OBJ-01 to OBJ-05", so the two ends must be present
    required += ["OBJ-01", "OBJ-05", "ERA-1", "ERA-5", "HUM-01", "REC-01", "DEV-01", "FP-01", "FP-10", "SND-01"]
    for rid in required:
        if rid not in text:
            findings.add_fail(label, 0, "gather_ids", "required ID %s is missing" % rid)
    for n, line in enumerate(lines):
        for m in LJ_ID_RE.finditer(line):
            box = m.group(1)
            in_b = b_ix is not None and n >= b_ix
            if in_b and box == "ST":
                findings.add_fail(label, n + 1, "gather_ids", "stand-in ID %s appears in Part B (stand-ins are Part A only)" % m.group(0))
            if (not in_b) and box != "ST":
                findings.add_fail(label, n + 1, "gather_ids", "real-box scan ID %s appears before P-LOCK (Part A allows box ST only)" % m.group(0))
    check_cited_ids(label, text, reg_set, findings)


def check_howto(path, label, reg_set, findings):
    try:
        text = read_text_file(path)
    except OSError as exc:
        findings.add_fail(label, 0, "howto_file", "cannot read the file (%s)" % exc.strerror)
        return
    if "no names in note: ids and relation tokens only" not in text.lower():
        findings.add_fail(label, 0, "howto_content", "the sentence 'no names in note: IDs and relation tokens only' is missing")
    sentence = [x for x in re.split(r"(?<=[.])\s+", text.replace("\n", " ")) if "no names in note" in x.lower()]
    if not sentence or not ("`maker`" in sentence[0] and "`agent`" in sentence[0]):
        findings.add_fail(label, 0, "howto_content",
                          "the 'no names in note' sentence must also say that `who` is `maker` or `agent`")
    if "log honestly" not in text.lower():
        findings.add_fail(label, 0, "howto_content", "the 'log honestly' sentence is missing")
    check_cited_ids(label, text, reg_set, findings)


# ---------------------------------------------------------------- driver

def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint the ops files (read-only).")
    ap.add_argument("--root", default=os.path.dirname(HERE), help="repository root (default: above scripts/)")
    ap.add_argument("--ops-dir", help="ops folder (default: ROOT/ops)")
    ap.add_argument("--register", help="DECISIONS.md (default: ROOT/DECISIONS.md)")
    ap.add_argument("--patterns", help="redaction pattern file (default: ROOT/scripts/redaction_patterns.json, "
                                       "falling back to the one beside this script)")
    ap.add_argument("--deny-file", action="append", default=[], help="extra deny list (repeatable)")
    ap.add_argument("--hours", metavar="FILE", help="lint only this hours file")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    ops = os.path.abspath(args.ops_dir) if args.ops_dir else os.path.join(root, "ops")
    register = args.register or os.path.join(root, "DECISIONS.md")
    pat_path = args.patterns or os.path.join(root, "scripts", "redaction_patterns.json")
    if not args.patterns and not os.path.isfile(pat_path):
        pat_path = os.path.join(HERE, "redaction_patterns.json")

    try:
        patterns = Patterns(pat_path)
    except PatternError as exc:
        print("ops_lint: FAIL CLOSED: %s." % exc, file=sys.stderr)
        print("ops_lint: scripts/redaction_patterns.json (build plan 4.13, owner WP-03) must exist and be valid; "
              "nothing was checked.", file=sys.stderr)
        return 2

    findings = Findings()
    hours_mod = load_sibling("hours_report")
    d2c = load_sibling("decisions_to_csv")

    deny_paths = []
    local_rel = patterns.local_deny_rel or "scripts/public_lint.deny.local.txt"
    deny_paths.append(os.path.join(root, local_rel) if not os.path.isabs(local_rel) else local_rel)
    deny_paths.extend(args.deny_file)
    if os.environ.get("LJ_DENY_FILE"):
        deny_paths.append(os.environ["LJ_DENY_FILE"])
    if args.hours:
        deny_paths.append(os.path.splitext(args.hours)[0] + ".deny.txt")
    deny = load_deny(deny_paths, patterns, findings)
    findings.notes.append("pattern file version %s, %d text categories, %d deny-list name(s) loaded"
                          % (patterns.version, len(patterns.categories), len(deny)))

    checked = []
    if args.hours:
        if not os.path.isfile(args.hours):
            print("ops_lint: %s does not exist (the planted-note fixture is built by "
                  "tests/ops/make_fixtures.py)" % os.path.basename(args.hours), file=sys.stderr)
            return 2
        label = os.path.basename(args.hours)
        check_hours(args.hours, label, hours_mod, patterns, deny, findings)
        checked.append(label)
    else:
        if not os.path.isdir(ops):
            print("ops_lint: the ops folder does not exist", file=sys.stderr)
            return 2
        reg_set = check_decisions(os.path.join(ops, "decisions.csv"), register, d2c, findings)
        check_hours(os.path.join(ops, "hours.csv"), "ops/hours.csv", hours_mod, patterns, deny, findings)
        check_card(os.path.join(ops, "SETTINGS-CARD.md"), "ops/SETTINGS-CARD.md", reg_set, findings,
                   os.path.join(root, "pipeline", "phone", "test_strings.json"))
        check_gather(os.path.join(ops, "GATHER.md"), "ops/GATHER.md", reg_set, findings)
        check_howto(os.path.join(ops, "HOURS-HOWTO.md"), "ops/HOURS-HOWTO.md", reg_set, findings)
        checked = ["ops/decisions.csv", "ops/hours.csv", "ops/SETTINGS-CARD.md", "ops/GATHER.md", "ops/HOURS-HOWTO.md"]
        # every other text file: identifying data, markers, deny list (hours.csv was scanned above)
        for dirpath, _dirs, files in sorted(os.walk(ops)):
            for fname in sorted(files):
                full = os.path.join(dirpath, fname)
                rel = "ops/" + os.path.relpath(full, ops).replace(os.sep, "/")
                if not fname.lower().endswith(TEXT_SUFFIXES) or rel == "ops/hours.csv":
                    continue
                try:
                    scan_text(rel, read_text_file(full), patterns, deny, findings)
                except OSError as exc:
                    findings.add_fail(rel, 0, "file", "cannot read the file (%s)" % exc.strerror)
                if rel not in checked:
                    checked.append(rel)

    failed = bool(findings.fail) or (args.strict and bool(findings.warn))
    if args.json:
        print(json.dumps({"checked": checked, "failures": [list(x) for x in findings.fail],
                          "warnings": [list(x) for x in findings.warn], "notes": findings.notes,
                          "status": "FAIL" if failed else "PASS"}, indent=2))
        return 1 if failed else 0

    print("ops_lint: checked %d file(s): %s" % (len(checked), ", ".join(checked)))
    for note in sorted(set(findings.notes)):
        print("  note: " + note)
    for file, line, cat, text in findings.fail:
        print("  FAIL %s%s [%s] %s" % (file, (":%d" % line) if line else "", cat, text))
    for file, line, cat, text in findings.warn:
        print("  WARN %s%s [%s] %s" % (file, (":%d" % line) if line else "", cat, text))
    if failed:
        print("ops_lint: FAIL (%d failure(s), %d warning(s))" % (len(findings.fail), len(findings.warn)))
        return 1
    print("ops_lint: PASS (%d warning(s))" % len(findings.warn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
