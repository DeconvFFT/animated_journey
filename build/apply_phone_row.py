#!/usr/bin/env python3
"""build/apply_phone_row.py: settle the phone row in one step (gate review r1, nudge 2). Standard library only.

WHO RUNS IT   the orchestrator, after choosing the measured values. The implementor may not edit DECISIONS.md (the register is the orchestrator's), so this
              script is the prepared, tested edit. Nothing is changed unless you pass --apply.
WHY           pipeline/phone/profile.json and PHONE-ROW.md hold the figures WP-08 measured (PH2 cap 3.5 Mb/s; at most 32 characters a line for the phone burn-in);
              DECISIONS.md W-63 says 4 Mb/s and W-18 says 36. The register wins, so the cheapest way to one source of truth is to amend the two rows to the
              measured values (3.5 stays inside the old 4 cap; 32 fits the 90% by 90% box in both scripts at FontSize=28, which 36 does not). If you prefer the
              register as it is, do NOT run this; regenerate profile.json to 4 and 36 instead (parity.phone_profile_vs_register names the fix).

WHAT --apply DOES, IN ORDER (each step prints what it did; any refusal stops it before the next step)
  1. DECISIONS.md W-63: "1280x720, CRF 22, 4 Mb/s cap, level 3.1," becomes "... 3.5 Mb/s cap, level 3.1,".
     DECISIONS.md W-18: "two lines, at most 36 characters, block at 68 to 86% of height" becomes "two lines, at most 32 characters (measured to fit the 90% by 90%
     box in both scripts at FontSize=28; the venue file keeps its own guide of 42), block at 68 to 86% of height". Both phrases must occur exactly once.
  2. python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv        (the mirror follows the register)
  3. python3 -I pipeline/phone/phone_check.py --write-row pipeline/phone/PHONE-ROW.md    (regenerated; it now reads the register, so it says "(W-63)", not "inside W-63's 4")
  4. the Phone row of ops/SETTINGS-CARD.md is replaced by the Phone row of PHONE-ROW.md section 1 (the card's language line was filled separately)
  5. the four checks that must go green: parity.decisions_csv_vs_register, parity.phone_profile_vs_register, parity.card_phone_row_vs_phone_row_md,
     parity.card_language_note_vs_scripts_tested (tests/integration, written to a scratch folder that is removed again), and scripts/ops_lint.py.
AFTER IT (not done here, because they are playbook and skill text): the old figures still sit in playbooks/theatrical-delivery.md, agent-pipeline.md,
  cinematic-quality.md, mobile-delivery.md, toolchain.md and the skills mobile-phone-delivery, theatrical-delivery-and-rights and cinematic-quality-bar
  (grep -rn "4 Mb/s cap\\|at most 36 characters\\|36 characters a line"); a scribe pass makes them say the register's figures. Add the dated amendment note to
  DECISIONS.md's own change log in the register's usual way. Then run: bash build/run_all_checks.sh --quick

USAGE         python3 -I build/apply_phone_row.py           dry run: prints the three edits and the checks it would run, writes nothing
              python3 -I build/apply_phone_row.py --apply   makes the edits and runs the checks (exit 1 if a check fails; the edits stay, git diff shows them)
EXIT CODES    0 done (or a clean dry run) | 1 a check failed after --apply | 2 a phrase was not found exactly once, or bad usage
NEVER         commits, pushes, deletes, uses the network, or prints a name, host or home folder (paths are repository-relative).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.dont_write_bytecode = True

W63_OLD = "1280x720, CRF 22, 4 Mb/s cap, level 3.1,"
W63_NEW = "1280x720, CRF 22, 3.5 Mb/s cap, level 3.1,"
W18_OLD = "two lines, at most 36 characters, block at 68 to 86% of height"
W18_NEW = ("two lines, at most 32 characters (measured to fit the 90% by 90% box in both scripts at FontSize=28; "
           "the venue file keeps its own guide of 42), block at 68 to 86% of height")
CHECKS = ["parity.decisions_csv_vs_register", "parity.phone_profile_vs_register", "parity.card_phone_row_vs_phone_row_md", "parity.card_language_note_vs_scripts_tested"]


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def run(args, **kw):
    return subprocess.run([sys.executable, "-I"] + args, cwd=ROOT, capture_output=True, text=True, **kw)


def amend_register(apply):
    path = os.path.join(ROOT, "DECISIONS.md")
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")
    bom = text.startswith("﻿")
    body = text[1:] if bom else text
    out = body
    for row, old, new in (("W-63", W63_OLD, W63_NEW), ("W-18", W18_OLD, W18_NEW)):
        m = re.search(r"^\| %s \|.*$" % row, out, re.M)
        if not m:
            print("REFUSED: DECISIONS.md has no %s row" % row)
            return None
        n = m.group(0).count(old)
        if n == 0 and new in m.group(0):
            print("already  %s: the register already states the measured figure" % row)
            continue
        if n != 1:
            print("REFUSED: %s: the phrase %r occurs %d times in the row, expected 1" % (row, old, n))
            return None
        out = out[:m.start()] + m.group(0).replace(old, new) + out[m.end():]
        print("%-8s %s: %r -> %r" % ("change" if apply else "would", row, old, new))
    if apply and out != body:
        with open(path, "wb") as fh:
            fh.write((("﻿" if bom else "") + out).encode("utf-8"))
    return True


def paste_row(apply):
    src = os.path.join(ROOT, "pipeline", "phone", "PHONE-ROW.md")
    card = os.path.join(ROOT, "ops", "SETTINGS-CARD.md")
    if not apply:
        print("would    paste the Phone row of pipeline/phone/PHONE-ROW.md section 1 over the Phone row of ops/SETTINGS-CARD.md")
        return True
    row = [ln for ln in open(src, encoding="utf-8").read().splitlines() if ln.startswith("| **Phone** (D-27) |")]
    text = open(card, encoding="utf-8").read()
    lines = text.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.startswith("| **Phone** (D-27) |")]
    if len(row) != 1 or len(idx) != 1:
        print("REFUSED: expected one Phone row in PHONE-ROW.md (found %d) and one in the card (found %d)" % (len(row), len(idx)))
        return None
    lines[idx[0]] = row[0]
    with open(card, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))
    print("change   ops/SETTINGS-CARD.md: the Phone row is now PHONE-ROW.md section 1")
    return True


def main(argv):
    if any(a != "--apply" for a in argv):
        print("usage: python3 -I build/apply_phone_row.py [--apply]")
        return 2
    apply = "--apply" in argv
    print("apply_phone_row: %s" % ("MAKING THE EDITS" if apply else "dry run, nothing is written"))
    if amend_register(apply) is None:
        return 2
    for name, args in (("decisions_to_csv --write", ["scripts/decisions_to_csv.py", "--write", "ops/decisions.csv"]),
                       ("phone_check --write-row", ["pipeline/phone/phone_check.py", "--write-row", "pipeline/phone/PHONE-ROW.md"])):
        if not apply:
            print("would    run python3 -I %s" % " ".join(args))
            continue
        r = run(args)
        print("%-8s %s: exit %d: %s" % ("ran", name, r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:160]))
        if r.returncode != 0:
            print(r.stderr[-400:])
            return 1
    if paste_row(apply) is None:
        return 2
    if not apply:
        print("would    then run %s and scripts/ops_lint.py" % ", ".join(CHECKS))
        print("dry run done. Nothing was written. Run with --apply to make the edits.")
        return 0
    base = os.path.join(os.path.dirname(ROOT), "build-scratch")
    os.makedirs(base, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="apr.", dir=base)
    failed = 0
    try:
        r = run(["tests/integration/run_checks.py", "--mode", "quick", "--only", ",".join(CHECKS), "--evidence", os.path.join(tmp, "ev"), "--work", os.path.join(tmp, "work")])
        for ln in r.stdout.splitlines():
            if ln.startswith(("PASS", "FAIL", "BLOCKED", "UNVERIFIED", "SKIPPED")):
                print("  " + ln[:200])
                failed += ln.startswith(("FAIL", "BLOCKED"))
        if r.returncode != 0 and not failed:
            failed += 1
            print("  integration run exited %d" % r.returncode)
        r2 = run(["scripts/ops_lint.py"])
        print("  ops_lint exit %d: %s" % (r2.returncode, (r2.stdout.strip().splitlines() or [""])[-1][:160]))
        failed += r2.returncode != 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("%s: %d check(s) failed. Next: git diff DECISIONS.md ops pipeline/phone, then the scribe pass named in this script's header, then bash build/run_all_checks.sh --quick" % ("OK" if not failed else "NOT OK", failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
