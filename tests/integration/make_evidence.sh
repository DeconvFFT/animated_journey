#!/usr/bin/env bash
# tests/integration/make_evidence.sh   WP-11b: run both suites and every acceptance command of the work package, one after the other, and keep the real output.
#
#   bash tests/integration/make_evidence.sh [--skip-runner]
#
# Writes build/evidence/wp11b/acceptance_transcript.txt (the exact console output of each command, paths relative, no host or user name), summary.json (the counts of
# both suites and the exit code of each acceptance command) and refreshes tests_quick/all.{jsonl,txt}. --skip-runner leaves out the two run_week2_checks.sh runs
# (about 25 minutes for --all) when only the integration suites are wanted. Never run from inside run_week2_checks.sh (the runner refuses a nested run).
# No step uses --only: a partial run writes only tests_<mode>_only.* files (run_checks.py), and this script removes any such leftover first, so the evidence folder holds
# whole-run results only. The index.* and readiness.* tests run inside runner_quick (the integration area is area 13).
set -u
cd "$(dirname "$0")/../.." || exit 3
EV=build/evidence/wp11b
mkdir -p "$EV"
rm -f "$EV"/tests_*_only.* "$EV"/summary_*_only.json
OUT="$EV/acceptance_transcript.txt"
# The scratch folder the transcript scrub follows is the one run_checks.py uses: $LJ_SCRATCH, else build-scratch next to the repository folder.
SCRATCH_DIR="${LJ_SCRATCH:-$(cd "$(pwd)/.." && pwd)/build-scratch}"
esc() { printf '%s' "$1" | sed -e 's/[][\\.*^$#]/\\&/g'; }          # a path as a literal in a sed expression that uses # as its delimiter
SKIP_RUNNER=0
[ "${1:-}" = "--skip-runner" ] && SKIP_RUNNER=1
: > "$OUT"
declare -A RC
run() {  # label command...
  local label="$1"; shift
  {
    echo "================================================================================"
    echo "\$ $*"
    echo "(started $(date -u +%H:%M:%SZ), Avail $(df -BM / | awk 'NR==2{print $4}'))"
  } >> "$OUT"
  local t0 rc
  t0=$(date +%s)
  "$@" 2>&1 | sed -e "s#$(esc "$(pwd)")#.#g" -e "s#$(esc "$SCRATCH_DIR")#<scratch>#g" >> "$OUT"
  rc=${PIPESTATUS[0]}
  echo "[exit $rc after $(( $(date +%s) - t0 )) s]" >> "$OUT"
  RC[$label]=$rc
  echo "$label: exit $rc"
}
run quick       bash tests/integration/run_tests.sh --quick
run all         bash tests/integration/run_tests.sh --all
run stale       python3 -I scripts/stale_check.py --new-only
run lint_diff   python3 -I scripts/public_lint.py
run lint_diff_flag python3 -I scripts/public_lint.py --diff
run lint_paths  python3 -I scripts/public_lint.py --paths win scripts pipeline ops spikes tests build skills-staging reviews/build
run lint_theme  python3 -I scripts/public_lint.py --theme
run selftest    python3 -I scripts/public_lint.py --self-test --fail-on-skip
run decisions   python3 -I scripts/decisions_to_csv.py --check ops/decisions.csv
run cleanup_dry bash scripts/cleanup_scratch.sh
if [ "$SKIP_RUNNER" = 0 ]; then
  run runner_quick bash scripts/run_week2_checks.sh --quick
  run runner_list  bash scripts/run_week2_checks.sh --list
  run runner_all   bash scripts/run_week2_checks.sh --all
fi
python3 -I - "$EV" "$(for k in "${!RC[@]}"; do echo "$k=${RC[$k]}"; done | sort | tr '\n' ' ')" <<'PY'
import json, sys, os, datetime
ev, rcs = sys.argv[1], sys.argv[2]
out = {"schema": "lj-evidence-summary/1", "package": "WP-11b", "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
       "acceptance_exit_codes": dict(x.split("=") for x in rcs.split())}
for m in ("quick", "all"):
    try:
        out[m] = json.load(open(os.path.join(ev, "summary_%s.json" % m))).get("counts")
    except (OSError, ValueError):
        out[m] = None
json.dump(out, open(os.path.join(ev, "summary.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(ev, "summary.json"), "a").write("\n")
PY
echo "transcript: $OUT"
