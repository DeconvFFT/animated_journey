#!/usr/bin/env bash
# tests/ops/run_tests.sh - WP-02 tests (ops files, hours report, decisions CSV, ops lint).
#
#   bash tests/ops/run_tests.sh --quick   # a few seconds, no ffmpeg, no downloads, no timed runs
#   bash tests/ops/run_tests.sh --all     # also runs the settings-card commands on tiny test files (needs ffmpeg)
#   bash tests/ops/run_tests.sh --list    # list the tests
#
# What it does: runs tests/ops/run_checks.py (which writes build/evidence/wp02/). One test builds
# the fixture that contains planted bad strings (git-ignored, joined from fragments) and removes it
# again; the trap below removes it even if the run is interrupted. It reads the repository and writes only to a temporary
# folder and to build/evidence/wp02/. Exit 0 = every test PASS/SKIPPED/UNVERIFIED, 1 = a FAIL
# or BLOCKED test. Set LJ_PATTERNS=<file> to run against another pattern file (development only);
# set LJ_KEEP_FIXTURES=1 to leave tests/ops/fixtures/hours_bad_note.csv in place.
set -u
cd "$(dirname "$0")/../.." || exit 3
mode="${1:---quick}"
case "$mode" in
  --quick|--all|--list) ;;
  *) echo "usage: bash tests/ops/run_tests.sh [--quick|--all|--list]" >&2; exit 2 ;;
esac
command -v python3 >/dev/null 2>&1 || { echo "python3 not found" >&2; exit 3; }
if [ "$mode" = "--list" ]; then
  exec python3 -I tests/ops/run_checks.py --list
fi
cleanup() {
  if [ -z "${LJ_KEEP_FIXTURES:-}" ]; then python3 -I tests/ops/make_fixtures.py --clean >/dev/null 2>&1 || true; fi
}
trap cleanup EXIT
python3 -I tests/ops/run_checks.py "$mode"
exit $?
