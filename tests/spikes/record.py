#!/usr/bin/env python3
"""record.py: append one evidence envelope (build plan 4.2) for a test line to a JSON-lines file under build/evidence/wp10/.
USAGE  python3 -I tests/spikes/record.py STATUS NAME EXPECTED ACTUAL [--unverified REASON] [--out FILE]
Reads df for the required `disk` object; prints nothing. Standard library only (it reuses the WP-07 library through spikes/sp1b_readback/drivers/sp1b_lib.py)."""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "spikes", "sp1b_readback", "drivers"))
import sp1b_lib as B  # noqa: E402

L = B.L


def main(argv):
    out = os.path.join(L.EVID, "tests.jsonl")
    unv = []
    args = list(argv)
    while "--unverified" in args:
        i = args.index("--unverified")
        unv.append(args[i + 1])
        del args[i:i + 2]
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 4:
        print(__doc__)
        return 2
    status, name, expected, actual = args
    rec = {"schema": "lj-evidence/1", "package": L.PACKAGE, "test": name, "date_utc": L.today(), "status": status, "env": L.env_block(), "disk": L.disk_object(),
           "expected": expected, "actual": L.scrub(actual), "notes": "", "unverified_reasons": unv}
    L.append_jsonl(out, rec)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
