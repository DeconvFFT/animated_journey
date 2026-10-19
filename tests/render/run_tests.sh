#!/usr/bin/env bash
# tests/render/run_tests.sh - WP-04 tests: Route A harness render.mjs, the test card, fetch_libs.sh, test_strings.json (build plan A1 to A11, SP2).
#
#   bash tests/render/run_tests.sh --quick          # at most about 60 s: no downloads, no timed runs, no run over 20 MB
#   bash tests/render/run_tests.sh --all            # every acceptance test; timed runs under lj_bench, the 2,400-frame run under lj_with_disk
#   bash tests/render/run_tests.sh --list           # list the tests and which set they belong to
#   bash tests/render/run_tests.sh --summarize      # rewrite summary.json, tests.jsonl and tests_all.txt from the per-test evidence (after a partial rerun)
#   bash tests/render/run_tests.sh --all --only a7_fonts,a5_chain_output     # development: run only these
#
# What it does: runs tests/render/run_checks.py, which renders with node pipeline/bin/render.mjs (headless Chromium from PW_CHROMIUM or
# /opt/pw-browsers/chromium), checks the results with ffprobe, ImageMagick compare and Pillow, and writes one evidence envelope per test
# (lj-evidence/1) under build/evidence/wp04/. It renders under renders/wp04/ and the scratch folder (both git-ignored) and removes frames
# as soon as they are hashed. It never touches the network except a7_add_script (npm pack of one font, skipped when the registry is
# unreachable). Exit 0 = every test PASS, SKIPPED or UNVERIFIED; 1 = a FAIL or BLOCKED test; 2 = bad usage; 3 = a needed tool is missing.
set -u
cd "$(dirname "$0")/../.." || exit 3
mode="${1:---quick}"
case "$mode" in
  --quick|--all|--list|--summarize) ;;
  *) echo "usage: bash tests/render/run_tests.sh [--quick|--all|--list|--summarize] [--only name,name]" >&2; exit 2 ;;
esac
for t in python3 node ffmpeg ffprobe; do
  command -v "$t" >/dev/null 2>&1 || { echo "run_tests: $t not found" >&2; exit 3; }
done
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
exec python3 -I tests/render/run_checks.py "$@"
