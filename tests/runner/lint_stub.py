#!/usr/bin/env python3
"""lint_stub.py: stands in for scripts/public_lint.py in the runner tests (build plan WP-11a).

It re-exports the real load_patterns (so the runner's masker works unchanged) and adds the command line the runner
assumes for the future  public_lint.py --text : text on stdin, exit 0 = clean. STUB_MODE picks the behaviour:
  ok       --help lists --text; --text records stdin to $STUB_SEEN and exits 0
  refuse   --help lists --text; --text records stdin and exits 2
  notext   --help does not list --text
  oserror  the scanner raises OSError (no space left on device) from its second use on, as a full disk would
Test helper only. Standard library only.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("real_public_lint", os.path.join(HERE, "..", "..", "scripts", "public_lint.py"))
_real = importlib.util.module_from_spec(_spec)
sys.dont_write_bytecode = True
_spec.loader.exec_module(_real)


class _Wrap:
    """The real Patterns object; in STUB_MODE=oserror its scan_line fails after the runner's own sanity probe."""

    def __init__(self, p):
        self._p = p
        self._n = 0

    def __getattr__(self, name):
        return getattr(self._p, name)

    def scan_line(self, *a, **k):
        self._n += 1
        if os.environ.get("STUB_MODE") == "oserror" and self._n > 1:
            raise OSError(28, "No space left on device")
        return self._p.scan_line(*a, **k)


def load_patterns(path):
    return _Wrap(_real.load_patterns(path))



def main(argv):
    mode = os.environ.get("STUB_MODE", "ok")
    if "--help" in argv:
        print("usage: lint_stub [--text]" if mode != "notext" else "usage: lint_stub")
        return 0
    if "--text" in argv and mode != "notext":
        data = sys.stdin.read()
        seen = os.environ.get("STUB_SEEN")
        if seen:
            with open(seen, "w", encoding="utf-8") as f:
                f.write(data)
        return 0 if mode == "ok" else 2
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
