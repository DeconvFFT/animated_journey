#!/usr/bin/env python3
"""pr4_parity.py: the PR4 parity guard (build status issue 28, item 1; the pattern is the exact-string check of tests/ops/run_checks.py for O-08).

PR4, the seva-article rule, is one sentence. DECISIONS.md states it in its Codes line (the VR/PR line), in W-61 and in W-70, and says it is
copied verbatim into ROADMAP.md section 4.4 and PLAN-ON-A-PAGE.md rule 3. The Sunday sheet, four playbooks and four installed skills carry
it word for word as well. Any change to the sentence must move every copy, so this guard reads the sentence from the Codes line, counts it
byte for byte in each file that should carry it, and prints the counts.

  python3 -I scripts/pr4_parity.py              check the repository and print the counts
  python3 -I scripts/pr4_parity.py --self-test  plant defects in a synthetic tree and check that each one is caught
  python3 -I scripts/pr4_parity.py --root DIR   check another tree (default: the repository this script is in)

What it checks (COPIES and SKILLS below hold the expected counts; change them in the same commit as any copy it counts):
  1. each listed file holds the sentence exactly the expected number of times (a byte-for-byte match on UTF-8 bytes);
  2. the one clause-aligned family: the lines of playbooks/hindu-visual.md that say "untouched" and the sentence's closing clause but not the
     whole sentence (the changelog section is history and is not counted), as many as expected;
  3. no near copy: a line that carries the sentence's first words or its second clause but not the whole sentence is a copy that drifted;
  4. no unlisted copy: no other .md file under playbooks/, .claude/skills/, skills-staging/ or the repository root carries the sentence or a near copy.
A skill is read from skills-staging/<name>/SKILL.md while that staged copy exists (it is the version waiting to be installed), otherwise from
.claude/skills/<name>/SKILL.md; the output says which.

Prints one line per file (found / expected), the totals, then PASS or FAIL. Reads only; writes nothing; stdlib only.
Exit 0 every count as expected | 1 a count, a copy or a family differs | 2 usage, or the sentence could not be read from the Codes line.
Windows: not run there (the orchestrator's container check); nothing in it is specific to Linux.
"""
import argparse
import contextlib
import hashlib
import io
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# (file, expected verbatim copies, where they are). DECISIONS.md is read first; its three copies include the Codes line the sentence is taken from.
COPIES = [
    ("DECISIONS.md", 3, "Codes (VR/PR line), W-61, W-70"),
    ("QUESTIONS-SUN-25-OCT.md", 3, "the three why-lines (7, 37, 72)"),
    ("ROADMAP.md", 1, "section 4.4"),
    ("PLAN-ON-A-PAGE.md", 1, "rule 3"),
    ("playbooks/pushtimarg-world.md", 4, "T2 row PR4, reverence norms, the Q4 note, pitfall 14"),
    ("playbooks/hindu-visual.md", 1, "Step 6 route (3)"),
    ("playbooks/ai-imagery.md", 1, "the Deities paragraph"),
    ("playbooks/mobile-delivery.md", 1, "the surfaces table, her own deities on a phone surface"),
]
SKILLS = [
    ("pushtimarg-seva-and-pichwai", 1, "Guardrails, Surprise"),
    ("hindu-visual-language", 2, "procedure step 5, Guardrails, Privacy"),
    ("ai-photo-to-animation-pipeline", 2, "procedure, the deities line; Ethics guardrails, Deities"),
    ("mobile-phone-delivery", 1, "Guardrails, Deities"),
]
# The clause-aligned family: lines that restate the rule in the playbook's own words and carry its closing clause.
CLAUSE_FILE = "playbooks/hindu-visual.md"
CLAUSE_EXPECTED = 6
CLAUSE_MARKER = b"untouched"
SCAN_DIRS = ["playbooks", ".claude/skills", "skills-staging"]
CODES_START = b"- **VR-1 to VR-3 and PR1 to PR25**"
SENTENCE_FROM = b"rule 3: "
SENTENCE_TO = [b" (touching or handling", b"; PR5"]    # the pointer after the sentence in the Codes line; the sentence stops where the first one begins


class Unreadable(Exception):
    pass


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def read_sentence(decisions):
    """The register's sentence, taken from the Codes line of DECISIONS.md (bytes). Raises Unreadable if the line no longer has the expected shape."""
    lines = [l for l in decisions.split(b"\n") if l.startswith(CODES_START)]
    if len(lines) != 1:
        raise Unreadable("DECISIONS.md has %d lines starting %r; expected exactly one (the Codes VR/PR line)" % (len(lines), CODES_START.decode()))
    line = lines[0]
    a = line.find(SENTENCE_FROM)
    if a < 0:
        raise Unreadable("the Codes VR/PR line no longer contains %r, the words that introduce the sentence" % SENTENCE_FROM.decode())
    a += len(SENTENCE_FROM)
    ends = [line.find(t, a) for t in SENTENCE_TO]
    ends = [e for e in ends if e > a]
    if not ends:
        raise Unreadable("the Codes VR/PR line has no pointer (%s) after the sentence, so its end cannot be found" % " or ".join(repr(t.decode()) for t in SENTENCE_TO))
    s = line[a:min(ends)].strip()
    if not s.startswith(b"her Thakorji, ") or b"; " not in s or len(s) < 100:
        raise Unreadable("the text after %r does not look like PR4 (it starts %r)" % (SENTENCE_FROM.decode(), s[:40].decode("utf-8", "replace")))
    return s


def line_numbers(data, needle):
    return [i + 1 for i, l in enumerate(data.split(b"\n")) if needle in l]


def locate_skill(root, name):
    """(relative path, state) of the skill file the table should read: the staged copy while it exists, else the installed one."""
    staged = "skills-staging/%s/SKILL.md" % name
    if os.path.isfile(os.path.join(root, staged)):
        return staged, "staged, waiting to be installed"
    return ".claude/skills/%s/SKILL.md" % name, "installed"


def check(root):
    """Returns (rows, notes, problems, total, nfiles, clause) for the tree at root. Raises Unreadable."""
    sentence = read_sentence(read_bytes(os.path.join(root, "DECISIONS.md")))
    cut = sentence.find(b" and ")
    first_words = sentence[:cut] if cut > 20 else sentence[:43]                  # "her Thakorji, chitraji, any picture of hers"
    second = sentence[sentence.index(b"; ") + 2:]
    second_clause = second[:second.index(b"(") + 1] if b"(" in second else second[:40]   # "a seva article outside the mandir ("
    closing = sentence[sentence.rindex(b"each logged"):]                         # "each logged as a G5 flag (O-48)"
    rows, problems, notes = [], [], []
    targets = [(f, n, why, "") for f, n, why in COPIES]
    for name, n, why in SKILLS:
        path, state = locate_skill(root, name)
        targets.append((path, n, why, state))
    listed = set()
    total = nfiles = 0
    for path, expected, why, state in targets:
        listed.add(path)
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            rows.append((path, None, expected, why, state))
            problems.append("%s is missing (expected %d copies)" % (path, expected))
            continue
        data = read_bytes(full)
        found = data.count(sentence)
        rows.append((path, found, expected, why, state))
        total += found
        nfiles += 1
        if found != expected:
            problems.append("%s holds %d copies of the sentence; expected %d" % (path, found, expected))
        for needle in (first_words, second_clause):
            for ln in line_numbers(data, needle):
                if sentence not in data.split(b"\n")[ln - 1]:
                    problems.append("%s:%d carries a clause of the sentence but not the sentence byte for byte (a copy that drifted)" % (path, ln))
    # 2. the clause-aligned family
    clause_lines = []
    cpath = os.path.join(root, CLAUSE_FILE)
    if os.path.isfile(cpath):
        lines = read_bytes(cpath).split(b"\n")
        end = len(lines)
        for i, l in enumerate(lines):
            if re.match(rb"^#{1,6}\s+change ?log\b", l, re.I):
                end = i
                break
        for i, l in enumerate(lines[:end]):
            if CLAUSE_MARKER in l and closing in l and sentence not in l:
                clause_lines.append(i + 1)
    if len(clause_lines) != CLAUSE_EXPECTED:
        problems.append("%s has %d clause-aligned lines (with %r and %r, not the whole sentence, outside the changelog); expected %d"
                        % (CLAUSE_FILE, len(clause_lines), CLAUSE_MARKER.decode(), closing.decode(), CLAUSE_EXPECTED))
    # 4. unlisted copies
    staged_names = set()
    sdir = os.path.join(root, "skills-staging")
    if os.path.isdir(sdir):
        staged_names = {d for d in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, d))}
    candidates = [f for f in sorted(os.listdir(root)) if f.endswith(".md") and os.path.isfile(os.path.join(root, f))]
    for d in SCAN_DIRS:
        for dp, dn, fn in os.walk(os.path.join(root, d)):
            dn[:] = sorted(x for x in dn if x != "__pycache__")
            for f in sorted(fn):
                if f.endswith(".md"):
                    candidates.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
    for rel in candidates:
        parts = rel.split("/")
        if rel in listed:
            continue
        if parts[:2] == [".claude", "skills"] and len(parts) > 2 and parts[2] in staged_names:
            continue                                            # superseded by the staged copy of the same skill
        data = read_bytes(os.path.join(root, rel))
        if sentence in data or first_words in data or second_clause in data:
            ln = (line_numbers(data, sentence) or line_numbers(data, first_words) or line_numbers(data, second_clause))[0]
            problems.append("%s:%d carries the sentence or a clause of it but is not in the table (add it to COPIES or SKILLS with its count, or reword the line)" % (rel, ln))
    info = {"bytes": len(sentence), "sha": hashlib.sha256(sentence).hexdigest()[:12]}
    return rows, info, problems, total, nfiles, clause_lines


def report(root):
    try:
        rows, info, problems, total, nfiles, clause_lines = check(root)
    except Unreadable as e:
        print("PR4 parity: cannot read the register's sentence: %s" % e)
        return 2, None
    out = ["PR4 parity guard: the register's sentence (DECISIONS.md, Codes line), %d bytes, sha256 %s" % (info["bytes"], info["sha"]),
           "verbatim copies, found / expected, by file:"]
    w = max(len(r[0]) for r in rows)
    for path, found, expected, why, state in rows:
        out.append("  %-*s  %s / %d   %s%s" % (w, path, "missing" if found is None else found, expected, why, "  [%s]" % state if state else ""))
    expected_total = sum(r[2] for r in rows)
    out.append("verbatim copies in all: %d / %d in %d files" % (total, expected_total, nfiles))
    out.append("clause-aligned lines in %s (\"untouched\" and the closing clause, not the whole sentence; the changelog is not counted): %d / %d%s"
               % (CLAUSE_FILE, len(clause_lines), CLAUSE_EXPECTED, " at lines " + ", ".join(str(x) for x in clause_lines) if clause_lines else ""))
    out.append("problems: %s" % ("none" if not problems else "%d" % len(problems)))
    out.extend("  FAIL: " + p for p in problems)
    out.append("PR4 parity: %s (%d verbatim copies in %d files, %d clause-aligned lines)" % ("PASS" if not problems else "FAIL", total, nfiles, len(clause_lines)))
    print("\n".join(out))
    return (0 if not problems else 1), out


# ---------------------------------------------------------------------------------------------------------------------- self-test
SYNTH_SENTENCE = ("her Thakorji, chitraji, any picture of hers and anything inside the mandir are never photographed without her knowing; "
                  "a seva article outside the mandir (the jhari in its cloth, the lamp, the closed doors) may be photographed by sight, untouched, "
                  "on an unsynced phone (O-58), each logged as a G5 flag (O-48)")


def build_tree(root, staged=()):
    """A synthetic tree that satisfies the table: every listed file holds its copies, one per line, among filler lines."""
    def put(rel, text):
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(text.encode("utf-8"))
    codes = ("- **VR-1 to VR-3 and PR1 to PR25**: the checks. PR4, **the seva-article rule**, one sentence copied verbatim here, in `ROADMAP.md` and in "
             "`PLAN-ON-A-PAGE.md` rule 3: %s (touching or handling any seva article without her knowing is PR10/PR14, W-70); PR5 to PR9 more." % SYNTH_SENTENCE)
    for f, n, why in COPIES:
        lines = ["# %s" % f, "filler"]
        if f == "DECISIONS.md":
            lines.append(codes)
            lines += ["| W-%d | row | x %s (a picture may be pusht) |" % (61 + 9 * i, SYNTH_SENTENCE) for i in range(n - 1)]
        else:
            lines += ["note %d: %s." % (i, SYNTH_SENTENCE) for i in range(n)]
        if f == CLAUSE_FILE:
            lines += ["clause line %d: by sight and untouched, %s, never the Thakorji or anything inside the mandir." % (i, "each logged as a G5 flag (O-48)")
                      for i in range(CLAUSE_EXPECTED)]
            lines += ["## Changelog", "- 2026-10-20: by sight and untouched, each logged as a G5 flag (O-48), history only."]
        put(f, "\n".join(lines) + "\n")
    for name, n, why in SKILLS:
        sub = "skills-staging" if name in staged else ".claude/skills"
        put("%s/%s/SKILL.md" % (sub, name), "\n".join(["# %s" % name] + ["rule %d: %s." % (i, SYNTH_SENTENCE) for i in range(n)]) + "\n")


def self_test():
    problems = []
    ran = []

    def case(label, edit, expect_rc, expect_text=None, staged=()):
        with tempfile.TemporaryDirectory(prefix="pr4-parity-") as td:
            build_tree(td, staged)
            edit(td)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc, _ = report(td)
            text = buf.getvalue()
            ran.append(label)
            ok = rc == expect_rc and (expect_text is None or expect_text in text)
            print("  %-4s %s (exit %d, wanted %d%s)" % ("ok" if ok else "FAIL", label, rc, expect_rc, "" if expect_text is None else "; text %r %s" % (expect_text, "found" if expect_text in text else "NOT FOUND")))
            if not ok:
                problems.append(label)

    def sub(rel, old, new, count=1):
        def f(td):
            full = os.path.join(td, rel)
            data = read_bytes(full).decode("utf-8")
            assert data.count(old) >= 1, (rel, old)
            with open(full, "wb") as fh:
                fh.write(data.replace(old, new, count).encode("utf-8"))
        return f

    def append(rel, text):
        def f(td):
            with open(os.path.join(td, rel), "ab") as fh:
                fh.write(text.encode("utf-8"))
        return f

    def remove(rel):
        return lambda td: os.remove(os.path.join(td, rel))

    print("pr4_parity self-test (a synthetic tree in a temporary folder; each planted defect must be caught):")
    case("clean tree passes", lambda td: None, 0, "PR4 parity: PASS (21 verbatim copies in 12 files, 6 clause-aligned lines)")
    case("clean tree with the four skills staged passes", lambda td: None, 0, "[staged, waiting to be installed]", staged=[s[0] for s in SKILLS])
    case("one changed word in one playbook copy", sub("playbooks/ai-imagery.md", "any picture of hers", "any picture of hers or hers"), 1, "a copy that drifted")
    case("one changed character in the Sunday sheet", sub("QUESTIONS-SUN-25-OCT.md", "(O-58)", "(O-59)"), 1, "QUESTIONS-SUN-25-OCT.md holds 2 copies")
    case("a copy missing from a skill", sub(".claude/skills/hindu-visual-language/SKILL.md", SYNTH_SENTENCE, "see the register"), 1, "hindu-visual-language/SKILL.md holds 1 copies")
    case("a skill file missing", remove(".claude/skills/mobile-phone-delivery/SKILL.md"), 1, "is missing")
    case("a listed file with one copy too many", append("ROADMAP.md", "extra: %s.\n" % SYNTH_SENTENCE), 1, "ROADMAP.md holds 2 copies")
    case("a copy in a file that is not in the table", append("playbooks/new-note.md", "x %s.\n" % SYNTH_SENTENCE), 1, "is not in the table")
    case("a half-copy in a file that is not in the table", append("playbooks/new-note.md", "x a seva article outside the mandir (the jhari in its cloth.\n"), 1, "is not in the table")
    case("a clause-aligned line loses its 'untouched'", sub(CLAUSE_FILE, "clause line 0: by sight and untouched", "clause line 0: by sight"), 1, "has 5 clause-aligned lines")
    case("the changelog line is not counted as clause-aligned", lambda td: None, 0, "6 / 6")
    case("a staged copy that is wrong beats an installed copy that is right",
         lambda td: (build_tree_staged_wrong(td)), 1, "skills-staging/pushtimarg-seva-and-pichwai/SKILL.md holds 0 copies")
    case("an installed copy that a staged copy supersedes is not a stray",
         lambda td: write_installed_too(td, "pushtimarg-seva-and-pichwai"), 0, "PR4 parity: PASS", staged=["pushtimarg-seva-and-pichwai"])
    ptr = " (touching or handling any seva article without her knowing is PR10/PR14, W-70)"
    case("the Codes line without its pointer still reads (the next PR code ends the sentence)", sub("DECISIONS.md", ptr, ""), 0, "PR4 parity: PASS")
    case("the Codes line with neither the pointer nor the next PR code", lambda td: (sub("DECISIONS.md", ptr, "")(td), sub("DECISIONS.md", "; PR5 to PR9 more.", ".")(td)), 2, "cannot read the register's sentence")
    case("no Codes line", sub("DECISIONS.md", "- **VR-1 to VR-3 and PR1 to PR25**", "- **VR**"), 2, "cannot read the register's sentence")
    print("self-test: %s" % ("PASS, %d cases" % len(ran) if not problems else "FAIL: " + "; ".join(problems)))
    return 0 if not problems else 1


def write_installed_too(td, name):
    """Helper for one self-test case: the staged copy is right and an installed copy of the same skill also carries the sentence (a partial install)."""
    full = os.path.join(td, ".claude", "skills", name, "SKILL.md")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as fh:
        fh.write(("# installed\nrule: %s.\n" % SYNTH_SENTENCE).encode("utf-8"))


def build_tree_staged_wrong(td):
    """Helper for one self-test case: the installed copy is right, the staged copy exists and is wrong; the table must read the staged one."""
    full = os.path.join(td, "skills-staging", "pushtimarg-seva-and-pichwai", "SKILL.md")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as fh:
        fh.write(b"# staged\nthe old short form: nothing in seva is photographed without her knowing (PR4).\n")


def main(argv):
    ap = argparse.ArgumentParser(description="PR4 parity guard: the register's seva-article sentence, byte for byte, in every copy.")
    ap.add_argument("--root", default=ROOT, help="the tree to check (default: the repository this script is in)")
    ap.add_argument("--self-test", action="store_true", help="plant defects in a synthetic tree and check that each is caught")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not os.path.isfile(os.path.join(a.root, "DECISIONS.md")):
        print("usage: %s has no DECISIONS.md" % a.root, file=sys.stderr)
        return 2
    return report(a.root)[0]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
