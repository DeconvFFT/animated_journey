#!/usr/bin/env python3
"""prepare_defects.py: the first step of `bash tests/sp1/run_tests.sh --defects-only` (part 2 of a full --all). Standard library only.

USAGE  python3 -I tests/sp1/prepare_defects.py TESTS.jsonl

Part 2 APPENDS its planted-defect lines (`fake.defect_*`) to the tests.jsonl that part 1 wrote. This step makes that safe to repeat (w2t-t2-wording, 2026-10-20):
  * it REFUSES (exit 2, nothing written) when the file is missing or holds no part-1 line; the marker is `fake.verify_flipped_byte`, the last line part 1 writes
    (the flipped-byte line runs before the defect lines);
  * otherwise it drops every `fake.defect_*` line already in the file (an earlier part 2), so that a second run, or a run after a stale part 1, leaves one set of 12 lines, not two
    (make_summary.py counts every line, so duplicates would be counted twice). The other lines are kept byte for byte and in order. The write is atomic (temp file, then replace).
EXIT   0 ready; 2 refused. Prints one line either way and no path of the machine.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
MARKER = "fake.verify_flipped_byte"
PREFIX = "fake.defect_"


def test_name(line):
    try:
        obj = json.loads(line)
    except ValueError:
        return ""
    return str(obj.get("test", "")) if isinstance(obj, dict) else ""


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    path = argv[0]
    try:
        with open(path, encoding="utf-8") as f:
            rows = [ln for ln in f if ln.strip()]
    except OSError:
        rows = []
    if not any(test_name(ln) == MARKER for ln in rows):
        print("REFUSED: --defects-only is part 2 and needs part 1 first (run: bash tests/sp1/run_tests.sh --all --skip-defects); "
              "tests.jsonl is missing or holds no part-1 line (%s). Nothing was written." % MARKER)
        return 2
    keep = [ln for ln in rows if not test_name(ln).startswith(PREFIX)]
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(ln if ln.endswith("\n") else ln + "\n" for ln in keep)
    os.replace(tmp, path)
    print("--defects-only: kept %d part-1 line(s), dropped %d earlier %s* line(s)" % (len(keep), len(rows) - len(keep), PREFIX))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
