#!/usr/bin/env python3
"""make_fixtures.py - build (or remove) the one WP-02 fixture that contains planted bad strings.

WHY IT IS BUILT, NOT COMMITTED
  tests/ops/fixtures/hours_bad_note.csv holds an e-mail-shaped string, a profile path, an
  IP number, a social handle and a made-up name. The repository is public (D-26) and its
  hygiene lint must stay clean, so the bad strings are joined from fragments here and the
  file is git-ignored (tests/ops/fixtures/.gitignore). tests/ops/run_tests.sh builds it
  before the tests and removes it afterwards.

USAGE
  python3 -I tests/ops/make_fixtures.py          # write tests/ops/fixtures/hours_bad_note.csv
  python3 -I tests/ops/make_fixtures.py --clean  # remove it
The made-up name in the note is listed in tests/ops/fixtures/hours_bad_note.deny.txt, the
sidecar deny list that ops_lint.py reads when it lints that file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "fixtures", "hours_bad_note.csv")

EMAIL = "pat" + "." + "invalid" + "@" + "mailbox-" + "nowhere" + "." + "example"
PROFILE = "C:" + "\\" + "Users" + "\\" + "qzxuser" + "\\" + "Desktop" + "\\" + "scan.tif"
NAME = "Qzx" + "plorp"
IPV4 = "172" + "." + "16" + "." + "4" + "." + "9"
HANDLE = "@" + "qzx" + "_handle"
LONG_NOTE = ("synthetic fixture row: this note is deliberately long so that it goes over the "
             "eighty character limit and draws a warning")

ROWS = [
    ("2026-10-19", "-", "admin", "30", "maker", "synthetic fixture row: wrote to " + EMAIL),
    ("2026-10-19", "-", "scan", "20", "maker", "synthetic fixture row: saved to " + PROFILE),
    ("2026-10-20", "-", "story", "45", "maker", "synthetic fixture row: spoke with " + NAME),
    ("2026-10-20", "-", "admin", "15", "maker", "synthetic fixture row: router at " + IPV4),
    ("2026-10-21", "-", "gather", "25", "maker", "synthetic fixture row: posted by " + HANDLE),
    ("2026-10-21", "-", "learn", "60", "maker", LONG_NOTE),
    ("2026-10-22", "C01", "story", "30", "maker", "synthetic fixture row: clean row for OBJ-01"),
]


def build():
    lines = ["date,shot_or_chapter,activity,minutes,who,note"]
    for r in ROWS:
        lines.append(",".join(r))
    return "\n".join(lines) + "\n"


def main(argv):
    if "--clean" in argv:
        try:
            os.remove(TARGET)
            print("removed hours_bad_note.csv")
        except FileNotFoundError:
            print("hours_bad_note.csv was not present")
        return 0
    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(build())
    print("wrote tests/ops/fixtures/hours_bad_note.csv (git-ignored; planted strings built from fragments)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
