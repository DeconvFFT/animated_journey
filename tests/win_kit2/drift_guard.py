#!/usr/bin/env python3
"""drift_guard.py: the PowerShell helpers that win/kit2/*.ps1 carry as pasted copies must stay byte-identical (WP-09, review r1).

  python3 -I -B tests/win_kit2/drift_guard.py [FOLDER]        (default: win/kit2 next to this tests folder)

Each maker's script is self-contained on purpose (the maker runs ONE file), so Show-Path, Clean-Message, Quote-Arg, Invoke-Tool,
Find-Exe and Find-Python are pasted into several scripts. This guard finds every `function NAME ... }` (ends at the first line that is
exactly `}`, the same pattern the quoting test uses), compares the copies byte for byte, requires the expected number of copies (so a
changed pattern can never pass by finding nothing), and requires the one-line "# Shared helpers" note in every script that holds a
copy, naming every script that holds one.

Prints one line per function and `RESULT: OK` or `RESULT: DRIFT`. Exit 0 identical, 1 drift. Read-only.
"""
import glob
import os
import re
import sys

NAMES = ["Show-Path", "Clean-Message", "Quote-Arg", "Invoke-Tool", "Find-Exe", "Find-Python"]
MIN_COPIES = {"Show-Path": 4, "Clean-Message": 4, "Quote-Arg": 2, "Invoke-Tool": 2, "Find-Exe": 2, "Find-Python": 2}
NOTE_MARK = b"# Shared helpers"


def body(src, name):
    m = re.search(rb"^function " + re.escape(name.encode()) + rb"\b.*?\n\}\r?\n", src, re.S | re.M)
    return m.group(0) if m else None


def main(argv):
    folder = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "win", "kit2")
    files = sorted(glob.glob(os.path.join(folder, "*.ps1")))
    srcs = {}
    for f in files:
        with open(f, "rb") as fh:
            srcs[os.path.basename(f)] = fh.read()
    problems = []
    holders = set()
    for name in NAMES:
        copies = {}
        for base, src in srcs.items():
            b = body(src, name)
            if b is not None:
                copies[base] = b
                holders.add(base)
        groups = {}
        for base, b in copies.items():
            groups.setdefault(b, []).append(base)
        n = len(copies)
        ok = len(groups) == 1 and n >= MIN_COPIES[name]
        print("%s %-14s %d cop%s in %s%s" % ("OK   " if ok else "DRIFT", name, n, "y" if n == 1 else "ies", ", ".join(sorted(copies)) or "no script",
                                             "" if len(groups) <= 1 else "; DIFFERENT VERSIONS: " + " | ".join(" + ".join(sorted(g)) for g in groups.values())))
        if len(groups) > 1:
            problems.append("%s differs between %s" % (name, " and ".join(" + ".join(sorted(g)) for g in groups.values())))
        elif n < MIN_COPIES[name]:
            problems.append("%s: found %d cop%s, expected at least %d" % (name, n, "y" if n == 1 else "ies", MIN_COPIES[name]))
    for base in sorted(holders):
        notes = [ln for ln in srcs[base].splitlines() if ln.startswith(NOTE_MARK)]
        missing = [h for h in sorted(holders) if not notes or h.encode() not in notes[0]]
        ok = len(notes) == 1 and not missing
        print("%s header note in %s%s" % ("OK   " if ok else "DRIFT", base, "" if ok else " (%s)" % ("no single '# Shared helpers' line" if len(notes) != 1 else "does not name " + ", ".join(missing))))
        if not ok:
            problems.append("%s: the '# Shared helpers' note is missing, repeated or does not name every sibling" % base)
    print("RESULT: %s" % ("OK, %d scripts, %d shared functions identical in every copy" % (len(holders), len(NAMES)) if not problems else "DRIFT: " + "; ".join(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
