#!/usr/bin/env bash
# run_tests.sh: the WP-03 test runner (redaction patterns 4.13, disk/bench guard 4.9, stale_check, public_lint).
#
#   bash tests/hygiene/run_tests.sh --quick   pattern test, guard tests and the two self-tests (about 30 s, no downloads, no timed runs)
#   bash tests/hygiene/run_tests.sh --all     everything: quick + stale tests + lint tests + the acceptance commands on the real tree
#
# Prints RESULT lines (PASS/FAIL), writes the log to build/evidence/wp03/tests_<mode>.txt and, for --all, the
# envelopes tests.jsonl, summary.json and unverified.txt (build plan 4.2). Never writes outside the repo and
# the scratch folder beside it; never touches scripts/stale_baseline.json (the acceptance baseline run uses a
# scratch file). Exit 0 only when every test passed.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO" || exit 3
MODE=""
case "${1:-}" in --quick) MODE=quick ;; --all) MODE=all ;; *) echo "usage: bash tests/hygiene/run_tests.sh --quick|--all" >&2; exit 2 ;; esac
EV="$REPO/build/evidence/wp03"
mkdir -p "$EV"
BASE="$(cd "$REPO/.." && pwd)/build-scratch"
mkdir -p "$BASE"
LOG="$EV/tests_${MODE}.txt"
TMP="$(mktemp -d "$BASE/hyg-run.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
: > "$LOG"
AVAIL0="$(LC_ALL=C df -BM -P / | awk 'NR==2{gsub(/M/,"",$4);print $4}')"
AMIN="$AVAIL0"
FAILS=0
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
track_disk() { local a; a="$(LC_ALL=C df -BM -P / | awk 'NR==2{gsub(/M/,"",$4);print $4}')"; [[ "$a" =~ ^[0-9]+$ ]] && (( a < AMIN )) && AMIN="$a"; }
res() {  # PASS|FAIL name detail
  say "RESULT $1 $2 :: ${3:-}"
  [[ "$1" == FAIL ]] && FAILS=$((FAILS + 1))
  return 0
}
cmd_result() {  # name expected_exit detail_prefix -- command...
  local name="$1" want="$2" pre="$3"; shift 4
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [[ "$rc" == "$want" ]]; then res PASS "$name" "$pre exit $rc; $(printf '%s' "$out" | tail -n 1 | cut -c1-150)"; else res FAIL "$name" "$pre exit $rc, wanted $want; $(printf '%s' "$out" | tail -n 1 | cut -c1-150)"; fi
  track_disk
}
run_group() {  # group script... (a script that prints RESULT lines)
  local g="$1"; shift
  say "GROUP $g"
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" | grep -E '^RESULT ' | tee -a "$LOG"
  FAILS=$((FAILS + $(printf '%s\n' "$out" | grep -c '^RESULT FAIL')))
  [[ $rc -ne 0 && $(printf '%s\n' "$out" | grep -c '^RESULT FAIL') -eq 0 ]] && res FAIL "${g}_runner_exit" "exit $rc"
  track_disk
}

say "WP-03 hygiene tests, mode $MODE (Avail at start: ${AVAIL0} MB)"

say "GROUP patterns"
# the internal test writes the LANDED marker only on a full pass; keep it out of --quick reruns
out="$(python3 -I tests/hygiene/test_patterns.py --no-marker 2>&1)"; rc=$?
npass="$(printf '%s\n' "$out" | grep -c '^PASS')"; nfail="$(printf '%s\n' "$out" | grep -c '^FAIL')"
if [[ $rc -eq 0 ]]; then res PASS pattern_file_internal_test "$npass checks passed, 0 failed, exit 0"; else res FAIL pattern_file_internal_test "exit $rc; $(printf '%s\n' "$out" | grep '^FAIL' | head -n 2 | tr '\n' ' ')"; fi
track_disk

run_group guard bash tests/hygiene/test_guard.sh

say "GROUP self_tests"
cmd_result stale_check_self_test 0 "python3 -I scripts/stale_check.py --self-test:" -- python3 -I scripts/stale_check.py --self-test
cmd_result public_lint_self_test 0 "python3 -I scripts/public_lint.py --self-test:" -- python3 -I scripts/public_lint.py --self-test

if [[ "$MODE" == all ]]; then
  run_group stale python3 -I tests/hygiene/test_stale.py
  run_group lint python3 -I tests/hygiene/test_lint.py
  say "GROUP acceptance_on_the_real_tree"
  cmd_result stale_audit_allowlist_no_dead_entries 0 "--audit-allowlist:" -- python3 -I scripts/stale_check.py --audit-allowlist
  cmd_result stale_report_exits_1_as_expected 1 "report run:" -- python3 -I scripts/stale_check.py --json "$TMP/rep.json" --md "$TMP/rep.md"
  if python3 -I - "$TMP/rep.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
ids = [r["row_id"] for r in d["rows"]]
assert ids == ["S-%02d" % n for n in range(1, 42)] + ["W-29"], ids
assert d["summary"]["fail"] > 0 and d["work_orders"] and "info_candidates" in d
PY
  then res PASS stale_report_lists_every_table_4_row "42 rows S-01..S-41 + W-29, work orders and INFO candidates present"; else res FAIL stale_report_lists_every_table_4_row "rows missing"; fi
  cmd_result stale_baseline_then_new_only_exits_0 0 "--baseline (scratch file) then --new-only:" -- bash -c "python3 -I scripts/stale_check.py --baseline --baseline-file '$TMP/base.json' >/dev/null && python3 -I scripts/stale_check.py --new-only --baseline-file '$TMP/base.json'"
  cmd_result public_lint_own_files_clean 0 "public_lint on WP-03's own files:" -- python3 -I scripts/public_lint.py --paths scripts/redaction_patterns.json scripts/lj_guard.sh scripts/stale_check.py scripts/stale_patterns.json scripts/stale_allowlist.json scripts/public_lint.py scripts/public_lint.config.json tests/hygiene build/evidence/wp03
  res UNVERIFIED windows_powershell_5_1_reads_the_pattern_file "win/step0_pc_tests.ps1 was exercised on PowerShell 7 only; Windows PowerShell 5.1 can not be run here"
fi

say ""
say "hygiene tests ($MODE): $FAILS failed; Avail ${AVAIL0} MB at start, ${AMIN} MB minimum seen"
if [[ "$MODE" == all ]]; then
  python3 -I tests/hygiene/make_evidence.py "$LOG" "$EV" --mode all --avail-start "$AVAIL0" --avail-min "$AMIN" | tee -a "$LOG"
fi
[[ $FAILS -eq 0 ]]
