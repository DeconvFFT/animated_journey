#!/usr/bin/env bash
# run_tests.sh: the WP-11a test runner (check-runner skeleton run_week2_checks.sh, INDEX.md writer, cleanup_scratch.sh).
#
#   bash tests/runner/run_tests.sh --quick   fake-area tests of the runner and of cleanup_scratch.sh, the lint and syntax
#                                            checks (under 60 s, no downloads, no timed runs)
#   bash tests/runner/run_tests.sh --all     quick + the extra checks marked "all" (rerun, real-tree dry run with a hash)
#
# Prints RESULT lines (PASS/FAIL), writes the log to build/evidence/wp11a/tests_<mode>.txt and the envelopes
# (tests_<mode>.jsonl, summary.json, unverified.txt; build plan 4.2). Everything that runs the runner uses fake areas
# and a fake evidence folder; the real build/evidence/INDEX.md is only ever written by a deliberate runner run.
# Never writes outside the repo and the scratch folder beside it. Exit 0 only when every test passed.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO" || exit 3
MODE=""
case "${1:-}" in --quick) MODE=quick ;; --all) MODE=all ;; *) echo "usage: bash tests/runner/run_tests.sh --quick|--all" >&2; exit 2 ;; esac
EV="${LJ_RUNNER_EVIDENCE_DIR:-$REPO/build/evidence}/wp11a"
mkdir -p "$EV" || exit 3
LOG="$EV/tests_${MODE}.txt"
: > "$LOG"
avail() { LC_ALL=C df -BM -P / | awk 'NR==2{gsub(/M/,"",$4);print $4}'; }
AVAIL0="$(avail)"; AMIN="$AVAIL0"; FAILS=0
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
track() { local a; a="$(avail)"; [[ "$a" =~ ^[0-9]+$ ]] && (( a < AMIN )) && AMIN="$a"; return 0; }
run_group() {  # script args...  (a script that prints GROUP and RESULT lines)
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" | grep -E '^(GROUP|RESULT) ' | tee -a "$LOG"
  FAILS=$((FAILS + $(printf '%s\n' "$out" | grep -c '^RESULT FAIL')))
  if [[ $rc -ne 0 ]] && ! printf '%s\n' "$out" | grep -q '^RESULT FAIL'; then say "RESULT FAIL $(basename "$1")_exit :: exit $rc and no failing RESULT line"; FAILS=$((FAILS + 1)); fi
  track
}
say "WP-11a runner tests, mode $MODE (Avail at start: ${AVAIL0} MB)"
run_group bash tests/runner/test_runner.sh "$MODE"
run_group bash tests/runner/test_cleanup.sh "$MODE"
say "GROUP hygiene_of_the_owned_files"
out="$(python3 -I scripts/public_lint.py --paths scripts/run_week2_checks.sh scripts/cleanup_scratch.sh tests/runner 2>&1)"; rc=$?
if [[ $rc -eq 0 ]]; then say "RESULT PASS public_lint_owned_paths :: scripts/run_week2_checks.sh, scripts/cleanup_scratch.sh, tests/runner clean (exit 0)"; else say "RESULT FAIL public_lint_owned_paths :: exit $rc; $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ' | cut -c1-200)"; FAILS=$((FAILS + 1)); fi
track
say "SUMMARY mode=$MODE failures=$FAILS"
python3 -I tests/runner/make_evidence.py "$LOG" "$EV" --mode "$MODE" --avail-start "$AVAIL0" --avail-min "$AMIN" | tee -a "$LOG" | tail -n 1
[[ "$FAILS" -eq 0 ]]
