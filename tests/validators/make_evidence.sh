#!/usr/bin/env bash
# tests/validators/make_evidence.sh [--wait SECONDS] [--unguarded] [--planned-mb N]     WP-05: run everything and file the evidence
#
# Runs run_tests.sh --quick, then run_tests.sh --all (the guarded stage; the options are passed on), then the acceptance commands of
# the work package on their own, and writes build/evidence/wp05/{tests_quick.txt,tests_all.txt,tests_quick.jsonl,acceptance_transcript.txt,
# summary.json,environment.json}. Exit code: that of the --all run (0 only if no test failed and the disk stage was not blocked).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EV="$ROOT/build/evidence/wp05"
mkdir -p "$EV"
cd "$ROOT" || exit 2
bash tests/validators/run_tests.sh --quick 2>&1 | tee "$EV/tests_quick.txt"
cp "$EV/tests.jsonl" "$EV/tests_quick.jsonl"
bash tests/validators/run_tests.sh --all "$@" 2>&1 | tee "$EV/tests_all.txt"
RC="${PIPESTATUS[0]}"
{
  echo "# WP-05 acceptance commands, run on their own (the same commands run_tests.sh --all runs inside its stage)"
  echo
  echo '$ python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json build/evidence/wp05/colour_patch_ffmpeg-6.1.1.json'
  python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json build/evidence/wp05/colour_patch_ffmpeg-6.1.1.json; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/colour_patch.py --selftest'
  python3 -I pipeline/validators/colour_patch.py --selftest; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/spec_check.py --selftest'
  python3 -I pipeline/validators/spec_check.py --selftest; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/spec_check.py --list-profiles'
  python3 -I pipeline/validators/spec_check.py --list-profiles; echo "exit=$?"
} > "$EV/acceptance_transcript.txt" 2>&1
python3 -I tests/validators/make_evidence.py
exit "$RC"
