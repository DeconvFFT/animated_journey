#!/usr/bin/env bash
# tests/roundtrip/run_tests.sh [--quick|--all] [--keep]     WP-06: round-trip emitters and validators (ORA, SVG ids, OTIO)
#
#   --quick  (well under 60 s, no network, no timed runs) hygiene checks, kb_scale, the ORA emitter and validator with the reused make_ora.py and
#            at-layers.ora, nineteen planted ORA defects, the SVG rig through Inkscape plain-SVG export with the reused check_ids.py (clean pass-through,
#            three planted defects, the Inkscape data-* finding), the OTIO emitter and validator (template parity, opentimelineio 0.18.1 load, twenty-seven
#            planted defects, refusals) and adapter_probe.sh with the reused make_otio.py
#   --all    everything in --quick plus the plug-in adapter probe (pip, about 4 MB, throw-away venv; SKIPPED if the network or pip is not there)
#   --keep   leave the generated files in renders/wp06 (git-ignored); by default they are removed again
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
# Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line was BLOCKED.
# Every test also writes one evidence envelope (build plan 4.2) to build/evidence/wp06/tests_quick.jsonl or tests_all.jsonl (one file per mode, so a later --quick
# run never overwrites the --all evidence), with its disk figures.
# The whole run writes about 3 MB (test cards and a sine WAV), so it takes no disk lock (writes under 100 MB do not, 4.9); it records df in every envelope.
# It needs the venv <scratch>/venv-otio (opentimelineio==0.18.1) for the library checks; without it those tests are SKIPPED, not passed.
set -u
MODE="--quick"; KEEP=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick|--all) MODE="$1";;
    --keep) KEEP="--keep";;
    *) echo "usage: run_tests.sh [--quick|--all] [--keep]" >&2; exit 2;;
  esac
  shift
done
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$ROOT/build/evidence/wp06" "$ROOT/renders"
cd "$ROOT" || exit 2
exec python3 -I -B "$ROOT/tests/roundtrip/run_checks.py" --mode "${MODE#--}" ${KEEP:+"$KEEP"}
