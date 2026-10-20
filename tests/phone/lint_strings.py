#!/usr/bin/env python3
"""lint_strings.py: the test-string allowlist lint (build plan 4.10, WP-08). Standard library only.

  python3 -I tests/phone/lint_strings.py [--root DIR ...] [--strings FILE] [--quiet]

pipeline/phone/test_strings.json is the ONLY place a test string may be written. This lint fails (exit 1) when:
  1. any script block of the strings file has strings but a string has no marks[] key (every non-Latin string needs marks[], even an empty list: the mark-survival check reads it)
     or no text;
  2. a text file under a root holds Indic text (U+0900 to U+0DFF) that is not made of allowlisted strings (each space-separated word of an Indic run must be one of the allowlisted
     Indic words);
  3. a caption fixture (.srt, .vtt, .ass) holds a cue line that is not allowlisted strings joined by single spaces;
  4. a Latin test phrase of the allowlist's own family ("Test" followed by digits) appears with different text.
The strings file itself is skipped. Default roots: pipeline/phone, tests/phone, .claude/skills/mobile-phone-delivery. Exit 0 clean; 1 findings; 2 bad usage.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
STRINGS = os.path.join(ROOT, "pipeline", "phone", "test_strings.json")
TEXT_EXT = (".py", ".sh", ".md", ".json", ".html", ".js", ".mjs", ".srt", ".vtt", ".ass", ".txt", ".csv")
INDIC = re.compile("[" + chr(0x0900) + "-" + chr(0x0DFF) + chr(0x200C) + chr(0x200D) + "]")
INDIC_RUN = re.compile("[" + chr(0x0900) + "-" + chr(0x0DFF) + "][" + chr(0x0900) + "-" + chr(0x0DFF) + chr(0x200C) + chr(0x200D) + " ]*")
TIME_LINE = re.compile(r"-->|^\d+$|^WEBVTT|^NOTE\b")


def load_strings(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strings_problems(d):
    probs = []
    for name, blk in d.get("scripts", {}).items():
        strs = blk.get("strings") or []
        for s in strs:
            if not s.get("text"):
                probs.append("test_strings.json: script '%s', string '%s' has no text" % (name, s.get("id")))
            if name != "latin" and "marks" not in s:
                probs.append("test_strings.json: script '%s' has strings but string '%s' has no marks[] key" % (name, s.get("id")))
    return probs


def allow_list(d):
    texts = []
    for blk in d.get("scripts", {}).values():
        for s in blk.get("strings") or []:
            texts.append(s["text"])
    return sorted(set(texts), key=lambda t: -len(t))


def tiles(line, allow):
    line = line.strip()
    memo = {}

    def go(pos):
        if pos == len(line):
            return True
        if pos in memo:
            return memo[pos]
        ok = False
        for t in allow:
            if line.startswith(t, pos):
                end = pos + len(t)
                if end == len(line) or (line[end] == " " and go(end + 1)):
                    ok = True
                    break
        memo[pos] = ok
        return ok
    return go(0)


def cue_lines(path, text):
    if path.endswith(".ass"):
        for raw in text.splitlines():
            if raw.startswith("Dialogue:"):
                body = raw.split(",", 9)[-1]
                for part in body.replace("\\n", "\\N").split("\\N"):
                    part = re.sub(r"\{[^}]*\}", "", part).strip()
                    if part:
                        yield part
    else:
        for raw in text.splitlines():
            s = raw.strip().lstrip("﻿")
            if s and not TIME_LINE.search(s):
                yield s


def scan(roots, strings_path):
    d = load_strings(strings_path)
    findings = strings_problems(d)
    allow = allow_list(d)
    indic_words = set()
    for t in allow:
        if INDIC.search(t):
            indic_words.update(t.split(" "))
    latin_ok = set(t for t in allow if not INDIC.search(t))
    scanned = 0
    skip = os.path.abspath(strings_path)
    for root in roots:
        for dp, dn, fn in os.walk(root):
            dn[:] = [x for x in dn if x not in ("__pycache__", "node_modules", ".git")]
            for name in sorted(fn):
                p = os.path.join(dp, name)
                if os.path.abspath(p) == skip or not name.lower().endswith(TEXT_EXT):
                    continue
                try:
                    with open(p, encoding="utf-8") as f:
                        text = f.read()
                except (OSError, UnicodeDecodeError):
                    continue
                scanned += 1
                rel = os.path.relpath(p, ROOT) if os.path.abspath(p).startswith(ROOT) else os.path.basename(p)
                for m in INDIC_RUN.finditer(text):
                    for w in m.group(0).split(" "):
                        w = w.strip()
                        if w and w not in indic_words:
                            findings.append("%s: Indic text that is not an allowlisted string (%d characters, starts U+%04X)" % (rel, len(w), ord(w[0])))
                if name.lower().endswith((".srt", ".vtt", ".ass")):
                    for ln in cue_lines(p, text):
                        if not tiles(ln, allow):
                            findings.append("%s: a caption line that is not allowlisted strings joined by single spaces (%d characters)" % (rel, len(ln)))
                for m in re.finditer(r"\bTest \d+\b", text):
                    if m.group(0) not in latin_ok:
                        findings.append("%s: a Latin test phrase of the allowlist's family that is not on the allowlist (%d characters)" % (rel, len(m.group(0))))
    return scanned, findings


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", default=[])
    ap.add_argument("--strings", default=STRINGS)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    roots = [os.path.abspath(r) for r in a.root] or [os.path.join(ROOT, "pipeline", "phone"), os.path.join(ROOT, "tests", "phone"), os.path.join(ROOT, ".claude", "skills", "mobile-phone-delivery")]
    roots = [r for r in roots if os.path.isdir(r)]
    if not os.path.isfile(a.strings):
        print("USAGE: the strings file does not exist")
        return 2
    scanned, findings = scan(roots, a.strings)
    if not a.quiet:
        for f in findings:
            print("FINDING  " + f)
    print("lint_strings: %d file(s) scanned, %d finding(s)" % (scanned, len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
