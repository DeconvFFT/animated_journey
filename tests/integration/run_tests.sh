#!/usr/bin/env bash
# tests/integration/run_tests.sh [--quick|--all|--list] [--only name,name]    WP-11b: do the pieces of weeks 1 and 2 fit together?
#
#   --quick  (at most 60 s, no render, no download, no timed run): the parity tests (settings card, phone row, harness chain, pins, decisions mirror, pc_report
#            fields, lj.ps1 close v0, Noto families, scripts tested), the redaction checks (public_lint --self-test with zero skipped consumers, the path denylist,
#            build/evidence/pc/, the derivation tools), the disk checks from every evidence envelope, the hygiene checks (stale_check --new-only, public_lint over the
#            diff and the build, the theme guard, file size, binary, 8 MB, ignored files), the docs and the readiness map, INDEX.md, and the negative controls
#   --all    everything in --quick plus the end-to-end tests: the WP-04 test card through --chain h264_venue and spec_check.py; the A11 MO8 pair; a harness-rendered
#            ProRes master through encode_phone.sh, spec_check.py, colour_patch.py and phone_check.py --scenario fill_20x9 (about 3 minutes, under 100 MB, the master under
#            lj_with_disk 100; the encode takes its own guard)
#   --list   print the tests and which set each belongs to
#
# One line per test: PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED name detail. Exit 0 if no line is FAIL or BLOCKED, 1 if a line FAILs, 3 if the disk guard blocked a heavy step.
# Evidence: one lj-evidence/1 envelope per test in build/evidence/wp11b/tests_quick.jsonl or tests_all.jsonl, summary_<mode>.json, and the console copy tests_<mode>.txt.
# With --only the same three files get an _only suffix (tests_<mode>_only.jsonl, summary_<mode>_only.json, tests_<mode>_only.txt): a partial run never replaces the mode's evidence.
# Writes only under build/evidence/wp11b/, renders/wp11b/ (removed again) and a scratch folder it removes. Never calls run_week2_checks.sh (the runner refuses a nested run).
# Real cleanup: scripts/cleanup_scratch.sh --yes is NOT run on the real tree (it would delete the PowerShell the Windows-script tests use). The orchestrator runs it as the
# last step of the fortnight; the dry run and a faithful fake-tree --yes are tested here.
set -u
cd "$(dirname "$0")/../.." || exit 3
MODE="${1:---quick}"
case "$MODE" in
  --quick|--all|--list) ;;
  *) echo "usage: bash tests/integration/run_tests.sh [--quick|--all|--list] [--only name,name]" >&2; exit 2 ;;
esac
shift
ONLY=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --only) ONLY="${2:-}"; shift;;
    *) echo "usage: bash tests/integration/run_tests.sh [--quick|--all|--list] [--only name,name]" >&2; exit 2;;
  esac
  shift
done
for t in python3 git; do
  command -v "$t" >/dev/null 2>&1 || { echo "run_tests: $t not found" >&2; exit 3; }
done
if [ "$MODE" = "--list" ]; then exec python3 -I -B tests/integration/run_checks.py --list; fi
if [ "$MODE" = "--all" ]; then
  for t in ffmpeg ffprobe node; do
    command -v "$t" >/dev/null 2>&1 || { echo "run_tests: $t not found" >&2; exit 3; }
  done
fi
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p build/evidence/wp11b
ARGS=(--mode "${MODE#--}")
[ -n "$ONLY" ] && ARGS+=(--only "$ONLY")
# A partial run (--only) writes tests_<mode>_only.{txt,jsonl} and summary_<mode>_only.json, never the mode's evidence files.
SUFFIX=""
[ -n "$ONLY" ] && SUFFIX="_only"
python3 -I -B tests/integration/run_checks.py "${ARGS[@]}" 2>&1 | tee "build/evidence/wp11b/tests_${MODE#--}${SUFFIX}.txt"
exit "${PIPESTATUS[0]}"
