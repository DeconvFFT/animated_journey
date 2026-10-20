#!/usr/bin/env bash
# test_runner.sh: tests of scripts/run_week2_checks.sh against FAKE areas (build plan WP-11a). Prints GROUP and RESULT lines.
#   bash tests/runner/test_runner.sh quick|all
# The fake areas live in tests/runner/fake_tests (passing, failing, hanging, planted e-mail; "missing" has no folder).
# Every run uses the runner's test hooks, so the real build/evidence is never touched. The planted strings are built
# from fragments here too, so this file holds none of them. In "all" mode it also checks the real area list.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO" || exit 3
MODE="${1:-quick}"
RUNNER="$REPO/scripts/run_week2_checks.sh"
FAKE="$REPO/tests/runner/fake_tests"
AREAS="$REPO/tests/runner/fake_areas.txt"
STUB="$REPO/tests/runner/lint_stub.py"
BASE="$(cd "$REPO/.." && pwd)/build-scratch"
mkdir -p "$BASE"
T="$(mktemp -d "$BASE/wp11a-run.XXXXXX")" || exit 3
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scratch"

P1="$(printf '%s%s' 'zz.plan' 'ted')"; P2="$(printf '%s%s' 'alice' '-fake')"; P3="$(printf '%s%s%s' 'nowhere' '-co' '.org')"

res() { echo "RESULT $1 $2 :: ${3:-}"; }
t() { local name="$1" detail="$2"; shift 2; if "$@" >/dev/null 2>&1; then res PASS "$name" "$detail"; else res FAIL "$name" "$detail"; fi; }
chk() { if [[ "$3" -eq 0 ]]; then res PASS "$1" "$2"; else res FAIL "$1" "$2"; fi; }   # chk NAME DETAIL EXITCODE
has() { grep -Eq -- "$1" "$2"; }            # has REGEX FILE
hasnt() { ! grep -Eq -- "$1" "$2"; }
alive() { [[ -r "/proc/$1/stat" ]] && [[ "$(awk '{print $3}' "/proc/$1/stat" 2>/dev/null)" != Z ]]; }   # running (a zombie awaiting its parent is dead)
dirhash() { [[ -d "$1" ]] || { echo absent; return; }; (cd "$1" && { find . -type f -exec sha256sum {} + 2>/dev/null | sort; find . -printf '%p %y\n' | sort; }) | sha256sum | cut -c1-16; }

# rr EVDIR AREASFILE [ENV=VAL ...] -- ARGS...   runs the runner with the test hooks; stdout -> $T/out, stderr -> $T/err, exit -> RC
rr() {
  local ev="$1" af="$2"; shift 2
  local envs=()
  while [[ $# -gt 0 && "$1" != "--" ]]; do envs+=("$1"); shift; done
  shift
  RC=0
  env LJ_RUNNER_AREAS_FILE="$af" LJ_RUNNER_EVIDENCE_DIR="$ev" LJ_RUNNER_TESTS_DIR="$FAKE" LJ_RUNNER_TIMEOUT_S=2 \
      LJ_RUNNER_KILL_GRACE_S=1 LJ_SCRATCH="$T/scratch" "${envs[@]}" bash "$RUNNER" "$@" > "$T/out" 2> "$T/err" || RC=$?
}
sub_areas() { grep -E "^($1)\|" "$AREAS" > "$2"; }   # sub_areas 'fk_pass|fk_fail' FILE
sub_areas 'fk_pass|fk_missing' "$T/a_passmiss.txt"
sub_areas 'fk_missing' "$T/a_miss.txt"
sub_areas 'fk_hang' "$T/a_hang.txt"
sub_areas 'fk_email' "$T/a_email.txt"
sub_areas 'fk_pass' "$T/a_pass.txt"
sub_areas 'fk_pass|fk_fail|fk_missing|fk_email' "$T/a_nohang.txt"

echo "GROUP full_fake_set_quick"
EV="$T/ev1"; mkdir -p "$EV/fk-missing"
# an OLD envelope for the area that has not landed: it is counted, but must show as not refreshed by this run
printf '%s\n' '{"schema":"lj-evidence/1","package":"FK-3","test":"old","date_utc":"2026-10-01","status":"PASS","disk":{"avail_mb_min":900}}' > "$EV/fk-missing/old.jsonl"
touch -d '2 days ago' "$EV/fk-missing/old.jsonl"
rr "$EV" "$AREAS" FK_PIDFILE="$T/pids" -- --quick
cp "$T/out" "$T/t1.out"; cp "$T/err" "$T/t1.err"; T1RC=$RC
t failing_or_hung_area_makes_exit_1 "exit $T1RC (fk_fail fails, fk_hang times out)" test "$T1RC" -eq 1
t console_pass_row "fk_pass PASS" has '^\[ ?[0-9]+/5\] fk_pass +FK-1 +PASS ' "$T/t1.out"
t console_fail_row "fk_fail FAIL" has '^\[ ?[0-9]+/5\] fk_fail +FK-2 +FAIL ' "$T/t1.out"
t console_not_landed_row "fk_missing NOT LANDED" has '^\[ ?[0-9]+/5\] fk_missing +FK-3 +NOT LANDED ' "$T/t1.out"
t console_timeout_row "fk_hang TIMEOUT" has '^\[ ?[0-9]+/5\] fk_hang +FK-4 +TIMEOUT ' "$T/t1.out"
t index_shows_fail "INDEX.md row for fk_fail says FAIL" has '^\| 2 \| FK-2 \| fk_fail \| \*\*FAIL\*\* ' "$EV/INDEX.md"
t index_shows_not_landed "INDEX.md row for fk_missing says NOT LANDED" has '^\| 3 \| FK-3 \| fk_missing \| \*\*NOT LANDED\*\* ' "$EV/INDEX.md"
t index_shows_timeout "INDEX.md row for fk_hang says TIMEOUT" has '^\| 4 \| FK-4 \| fk_hang \| \*\*TIMEOUT\*\* ' "$EV/INDEX.md"
nalive=0; for p in $(cat "$T/pids" 2>/dev/null); do alive "$p" && nalive=$((nalive + 1)); done
t hung_area_and_its_child_are_killed "pids recorded: $(wc -w < "$T/pids" 2>/dev/null || echo 0), still running: $nalive" test "$nalive" -eq 0 -a -s "$T/pids"
secs="$(grep -E '^\[ ?[0-9]+/5\] fk_hang' "$T/t1.out" | grep -Eo '[0-9]+ s ' | head -n 1 | tr -dc 0-9)"
t hung_area_killed_promptly "took ${secs:-?} s with a 2 s limit and 1 s grace" test "${secs:-99}" -le 6
t wave1_quick_written "build/evidence/wave1_quick.txt equivalent exists" test -s "$EV/wave1_quick.txt"
t wave1_quick_is_the_console "wave1_quick.txt equals the console output byte for byte" cmp -s "$T/t1.out" "$EV/wave1_quick.txt"
t index_and_json_written "INDEX.md and week2_summary.json exist" test -s "$EV/INDEX.md" -a -s "$EV/week2_summary.json"
leak="$(grep -rIl -e "$P1" -e "$P2" -e "$P3" "$EV" "$T/t1.out" "$T/t1.err" 2>/dev/null | wc -l)"
t planted_strings_never_stored_or_printed "files holding a raw planted string: $leak" test "$leak" -eq 0
t planted_string_is_masked_in_the_console_copy "wave1_quick.txt shows the masked form" has 'last line: .*zz\*{4,}' "$EV/wave1_quick.txt"
t planted_string_is_masked_in_the_area_log "area log shows the masked form" has 'zz\*{4,}' "$EV/wp11a/area_fk_email_quick.txt"
t area_log_counts_masked_values "area_fk_email_quick.txt header" has 'masked_values=[3-9]' "$EV/wp11a/area_fk_email_quick.txt"
t area_logs_exist_for_every_area "5 logs (the not-landed one is a one-line note)" test "$(ls "$EV/wp11a" | grep -c '^area_.*_quick.txt$')" -eq 5
t area_got_the_quick_flag "fk_pass log shows mode=quick" has 'mode=quick' "$EV/wp11a/area_fk_pass_quick.txt"
python3 -I - "$EV" > "$T/links.out" 2>&1 <<'PY'
import os, re, sys
ev = sys.argv[1]
text = open(os.path.join(ev, "INDEX.md"), encoding="utf-8").read()
rows = [l for l in text.splitlines() if re.match(r"^\| \d+ \|", l)]
bad = n = 0
for r in rows:
    ls = re.findall(r"\]\(([^)]+)\)", r)
    if not ls:
        bad += 1
    for l in ls:
        n += 1
        if not os.path.exists(os.path.join(ev, l)):
            bad += 1
print("rows", len(rows), "links", n, "missing", bad)
sys.exit(1 if (bad or n == 0 or len(rows) != 5) else 0)
PY
lrc=$?
chk index_rows_link_evidence_that_exists "$(cat "$T/links.out")" "$lrc"
python3 -I - "$EV" > "$T/json.out" 2>&1 <<'PY'
import json, sys
d = json.load(open(sys.argv[1] + "/week2_summary.json"))
a = {x["area"]: x for x in d["areas"]}
assert d["schema"] == "lj-week2-summary/1" and d["mode"] == "quick" and d["exit_code"] == 1 and d["result"] == "FAIL"
assert d["totals"] == {"areas": 5, "landed": 4, "pass": 2, "fail": 1, "timeout": 1, "not_landed": 1}, d["totals"]
assert a["fk_pass"]["counts"] == {"PASS": 3, "FAIL": 0, "UNVERIFIED": 1, "SKIPPED": 0, "BLOCKED": 0}, a["fk_pass"]["counts"]
assert a["fk_pass"]["avail_mb_min"] == 123 and a["fk_fail"]["avail_mb_min"] == 700
assert a["fk_fail"]["counts"] == {"PASS": 0, "FAIL": 1, "UNVERIFIED": 0, "SKIPPED": 1, "BLOCKED": 1}, a["fk_fail"]["counts"]
assert a["fk_missing"]["landed"] is False and a["fk_missing"]["result"] == "NOT LANDED" and a["fk_hang"]["result"] == "TIMEOUT"
assert a["fk_missing"]["counts"]["PASS"] == 1 and a["fk_missing"]["envelopes_refreshed_this_run"] is False, a["fk_missing"]
assert a["fk_pass"]["envelopes_refreshed_this_run"] is True and a["fk_hang"]["envelopes_refreshed_this_run"] is None
assert d["disk"]["lowest_envelope_avail_mb_min"] == 123 and d["disk"]["entries_below_hard_floor"] == ["FK-1"]
assert isinstance(d["disk"]["hard_floor_mb"], int) and d["public_lint_text"].startswith("not available")
print("totals, counts, dedupe (old FAIL lost to newer PASS), avail minimum and flags all as expected")
PY
jrc=$?
chk summary_json_counts_dedupe_and_disk "$(tail -n 1 "$T/json.out")" "$jrc"
t low_disk_is_marked_in_index "fk_pass row carries LOW" has 'fk_pass \| \*\*PASS\*\* .*123 LOW' "$EV/INDEX.md"
t refreshed_column_in_index "fk_pass yes, fk_missing (older envelope) no, fk_hang -" bash -c "grep -Eq 'fk_pass .*\| 0 \| yes \| 123' '$EV/INDEX.md' && grep -Eq 'fk_missing .*\| 1 \| 0 \| 0 \| 0 \| 0 \| no \|' '$EV/INDEX.md' && grep -Eq 'fk_hang .*\| - \| n/a' '$EV/INDEX.md'"
t no_absolute_paths_in_outputs "no scratch path, /home or /root in console, INDEX, JSON" test "$(cat "$T/t1.out" "$EV/INDEX.md" "$EV/week2_summary.json" | grep -c -e "$T" -e '/home/' -e '/root')" -eq 0
t runner_cleans_its_scratch "no .wk2run folder left" test -z "$(ls -A "$T/scratch" | grep wk2run)"

echo "GROUP exit_semantics"
EV="$T/ev2"; mkdir -p "$EV"; rr "$EV" "$T/a_passmiss.txt" -- --quick
t pass_plus_missing_exit_0 "exit $RC" test "$RC" -eq 0
t missing_is_not_landed_when_alone_with_pass "row says NOT LANDED" has 'fk_missing \| \*\*NOT LANDED\*\*' "$EV/INDEX.md"
EV="$T/ev3"; mkdir -p "$EV"; rr "$EV" "$T/a_miss.txt" -- --quick
t only_missing_exit_0 "exit $RC, nothing landed" test "$RC" -eq 0 -a -s "$EV/wave1_quick.txt"
EV="$T/ev4"; mkdir -p "$EV"; rr "$EV" "$T/a_hang.txt" LJ_RUNNER_TIMEOUT_S=30 -- --quick --timeout 1
[[ "$RC" -eq 1 ]] && has 'fk_hang +FK-4 +TIMEOUT' "$T/out"; chk only_hang_exit_1_timeout "exit $RC" $?
has 'per-area limit 1 s' "$T/out"; chk timeout_option_wins_over_the_environment "--timeout 1 beat LJ_RUNNER_TIMEOUT_S=30" $?
t timeout_counts_as_fail_in_json "result FAIL, fail+timeout >= 1" python3 -I -c "import json,sys;d=json.load(open('$EV/week2_summary.json'));sys.exit(0 if d['result']=='FAIL' and d['totals']['timeout']==1 else 1)"
EV="$T/ev5"; mkdir -p "$EV"; rr "$EV" "$T/a_nohang.txt" -- --all
t all_mode_exit_1_and_flag_passed "exit $RC; fk_pass log shows mode=all" test "$RC" -eq 1 -a "$(grep -c 'mode=all' "$EV/wp11a/area_fk_pass_all.txt")" -ge 1
t all_mode_writes_no_wave1_quick "wave1_quick.txt is for --quick only" test ! -e "$EV/wave1_quick.txt" -a -s "$EV/wp11a/console_all.txt"
t all_mode_index_says_all "INDEX.md header names --all" has 'run_week2_checks.sh --all' "$EV/INDEX.md"
EV="$T/ev6"; mkdir -p "$EV"; rr "$EV" "$T/a_pass.txt" FK_SLEEP=2 LJ_RUNNER_BUDGET_S=1 LJ_RUNNER_TIMEOUT_S=20 -- --quick
[[ "$RC" -eq 0 ]] && has 'OVER BUDGET' "$EV/INDEX.md"; chk over_budget_is_flagged_not_failed "exit $RC; OVER BUDGET in INDEX" $?
t over_budget_in_json "over_budget true" python3 -I -c "import json,sys;d=json.load(open('$EV/week2_summary.json'));sys.exit(0 if d['over_budget'] is True else 1)"

echo "GROUP per_area_quick_limit"
# an area may carry its own quick limit as a sixth field (win_kit2 has 90 s in DEFAULT_AREAS); it applies to --quick only, and an explicit --timeout or LJ_RUNNER_TIMEOUT_S switches it off
printf 'fk_pass|FK-1|fk-pass|1|passing fake area with its own quick limit of 1 s|1\n' > "$T/a_qlim.txt"
EV="$T/ev40"; mkdir -p "$EV"; rr "$EV" "$T/a_qlim.txt" FK_SLEEP=1.5 LJ_RUNNER_TIMEOUT_S= -- --quick
[[ "$RC" -eq 1 ]] && has 'fk_pass +FK-1 +TIMEOUT' "$T/out" && has 'no result in 1 s' "$T/out"; chk area_quick_limit_applies_without_an_explicit_limit "exit $RC; the 1.5 s area was stopped at its own 1 s, not at the 60 s default" $?
has 'per-area limit 60 s \(own limit: fk_pass 1 s\)' "$T/out" && has 'per-area limit 60 s; own limit: fk_pass 1 s\.' "$EV/INDEX.md"; chk own_limit_is_named_in_console_and_index "console and INDEX.md say which area has its own limit" $?
t own_limit_is_in_the_json "areas[0].timeout_s is 1 and per_area_timeout_s is 60" python3 -I -c "import json,sys;d=json.load(open('$EV/week2_summary.json'));sys.exit(0 if d['areas'][0]['timeout_s']==1 and d['per_area_timeout_s']==60 else 1)"
EV="$T/ev41"; mkdir -p "$EV"; rr "$EV" "$T/a_qlim.txt" FK_SLEEP=1.5 LJ_RUNNER_TIMEOUT_S= -- --quick --timeout 4
[[ "$RC" -eq 0 ]] && has 'fk_pass +FK-1 +PASS' "$T/out" && ! has 'own limit' "$T/out"; chk timeout_option_switches_the_area_limit_off "exit $RC; --timeout 4 beat the area's 1 s and no own limit is claimed" $?
printf 'fk_pass|FK-1|fk-pass|1|bad|zero|\n' > "$T/a_qbad.txt"; printf 'fk_pass|FK-1|fk-pass|1|bad|0\n' > "$T/a_qzero.txt"
EV="$T/ev42"; mkdir -p "$EV"; rr "$EV" "$T/a_qbad.txt" -- --quick; r1=$RC; rr "$EV" "$T/a_qzero.txt" -- --quick; r2=$RC
[[ "$r1" -eq 2 && "$r2" -eq 2 ]] && has 'bad quick limit' "$T/err"; chk bad_area_limit_is_refused "a non-number and 0 are both usage errors (exit $r1, $r2)" $?
t default_area_list_gives_win_kit2_90_s "the real list: win_kit2 has 90 and no other area has an own limit" test "$(grep -cE '^  "[a-z0-9_]+\|[^"]*\|[0-9]+"$' "$RUNNER")" = 1 -a "$(grep -cE '^  "win_kit2\|[^"]*\|90"$' "$RUNNER")" = 1

echo "GROUP list_and_usage"
EV="$T/ev8"
h0="$(dirhash "$EV")"; rr "$EV" "$AREAS" -- --list; h1="$(dirhash "$EV")"
t list_exit_0_and_writes_nothing "exit $RC; evidence dir hash $h0 -> $h1 (absent means it was not created)" test "$RC" -eq 0 -a "$h0" = "$h1" -a ! -e "$EV"
has ' fk_pass +FK-1 .* yes ' "$T/out" && has ' fk_missing +FK-3 .* NOT LANDED ' "$T/out"; chk list_shows_landed_state_of_fakes "fk_pass yes, fk_missing NOT LANDED" $?
env -u LJ_RUNNER_AREAS_FILE -u LJ_RUNNER_EVIDENCE_DIR -u LJ_RUNNER_TESTS_DIR -u LJ_RUNNER_ACTIVE bash "$RUNNER" --list > "$T/real_list.out" 2>&1; RC=$?
got="$(awk 'NR>2 && $1 ~ /^[0-9]+$/ {printf "%s ", $2}' "$T/real_list.out")"
want="hygiene win ops validators render roundtrip sp1 win_lj win_kit2 phone spikes runner integration "
t list_prints_the_13_areas_in_order "exit $RC; $got" test "$RC" -eq 0 -a "$got" = "$want"
t list_marks_landed_areas "hygiene follows the folder on disk" bash -c "[[ -f tests/hygiene/run_tests.sh ]] && grep -Eq ' hygiene +WP-03 +1 +yes ' '$T/real_list.out' || [[ ! -f tests/hygiene/run_tests.sh ]]"
t list_last_line_counts "Landed: n of 13" has '^Landed: [0-9]+ of 13\.' "$T/real_list.out"
rc_of() { env -u LJ_RUNNER_AREAS_FILE -u LJ_RUNNER_EVIDENCE_DIR -u LJ_RUNNER_ACTIVE bash "$RUNNER" "$@" >/dev/null 2>&1; echo $?; }
t usage_no_args_exit_2 "exit $(rc_of)" test "$(rc_of)" -eq 2
t usage_unknown_arg_exit_2 "exit $(rc_of --bogus)" test "$(rc_of --bogus)" -eq 2
t usage_two_modes_exit_2 "exit $(rc_of --quick --all)" test "$(rc_of --quick --all)" -eq 2
t usage_bad_timeout_exit_2 "exit $(rc_of --quick --timeout abc)" test "$(rc_of --quick --timeout abc)" -eq 2
t usage_timeout_without_value_exit_2 "exit $(rc_of --quick --timeout)" test "$(rc_of --quick --timeout)" -eq 2
env -u LJ_RUNNER_EVIDENCE_DIR -u LJ_RUNNER_ACTIVE LJ_RUNNER_AREAS_FILE="$AREAS" bash "$RUNNER" --quick >/dev/null 2>&1; RC=$?
t areas_file_without_evidence_dir_exit_2 "a test run can not overwrite the real INDEX.md (exit $RC)" test "$RC" -eq 2
env -u LJ_RUNNER_AREAS_FILE -u LJ_RUNNER_EVIDENCE_DIR LJ_RUNNER_ACTIVE=1 bash "$RUNNER" --quick >"$T/rec.out" 2>"$T/rec.err"; RC=$?
[[ "$RC" -eq 3 ]] && has 'REFUSED' "$T/rec.err"; chk runner_inside_runner_refused "exit $RC (3 = environment)" $?

echo "GROUP redaction_fail_closed_and_lint_text"
EV="$T/ev9"; mkdir -p "$EV"; rr "$EV" "$T/a_pass.txt" LJ_RUNNER_PATTERNS="$T/nope.json" -- --quick
[[ "$RC" -eq 2 ]] && has 'pattern file' "$T/out"; chk missing_pattern_file_exit_2 "exit $RC" $?
t missing_pattern_file_runs_nothing_writes_nothing "no fk-pass folder, no INDEX.md" test ! -e "$EV/fk-pass" -a ! -e "$EV/INDEX.md" -a ! -e "$EV/wave1_quick.txt"
echo '{}' > "$T/empty.json"; rr "$EV" "$T/a_pass.txt" LJ_RUNNER_PATTERNS="$T/empty.json" -- --quick
[[ "$RC" -eq 2 && ! -e "$EV/fk-pass" ]]; chk invalid_pattern_file_exit_2 "exit $RC, nothing ran" $?
python3 -I - "$REPO/scripts/redaction_patterns.json" "$T/dead.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for c in d["categories"]:
    if c["id"] == "email":
        c["regex"] = "a^"          # valid, but it can never match
        c["positive_samples"] = []
json.dump(d, open(sys.argv[2], "w"))
PY
rr "$EV" "$T/a_pass.txt" LJ_RUNNER_PATTERNS="$T/dead.json" -- --quick
[[ "$RC" -eq 2 ]] && has 'did not flag' "$T/out"; chk scanner_that_misses_its_own_sample_exit_2 "exit $RC" $?
EV="$T/ev10"; mkdir -p "$EV"; rr "$EV" "$T/a_email.txt" -- --quick
[[ "$RC" -eq 0 ]] && has 'public_lint --text: not available yet' "$T/out"; chk lint_text_absent_is_stated "exit $RC" $?
EV="$T/ev11"; mkdir -p "$EV"; rr "$EV" "$T/a_email.txt" LJ_RUNNER_LINT="$STUB" STUB_MODE=ok STUB_SEEN="$T/seen_ok.txt" -- --quick
[[ "$RC" -eq 0 ]] && has 'public_lint --text: used' "$T/out"; chk lint_text_used_when_it_exists "exit $RC; says used" $?
t lint_text_receives_only_masked_text "stub saw $(wc -c < "$T/seen_ok.txt" 2>/dev/null || echo 0) bytes, raw planted strings: $(grep -c -e "$P1" -e "$P2" "$T/seen_ok.txt" 2>/dev/null)" test -s "$T/seen_ok.txt" -a "$(grep -c -e "$P1" -e "$P2" "$T/seen_ok.txt")" -eq 0
EV="$T/ev12"; mkdir -p "$EV"; rr "$EV" "$T/a_email.txt" LJ_RUNNER_LINT="$STUB" STUB_MODE=refuse STUB_SEEN="$T/seen_no.txt" -- --quick
[[ "$RC" -eq 2 ]] && has 'WITHHELD' "$T/err"; chk lint_text_refusal_exit_2 "exit $RC" $?
t lint_text_refusal_withholds_outputs "no INDEX.md, JSON or wave1_quick.txt" test ! -e "$EV/INDEX.md" -a ! -e "$EV/week2_summary.json" -a ! -e "$EV/wave1_quick.txt"
EV="$T/ev13"; mkdir -p "$EV"; rr "$EV" "$T/a_email.txt" LJ_RUNNER_LINT="$STUB" STUB_MODE=refuse LJ_RUNNER_LINT_TEXT=skip -- --quick
[[ "$RC" -eq 0 ]] && has 'public_lint --text: skipped' "$T/out"; chk lint_text_skip_switch_is_visible "exit $RC; output says skipped" $?
EV="$T/ev14"; mkdir -p "$EV"; rr "$EV" "$T/a_email.txt" LJ_RUNNER_LINT="$STUB" STUB_MODE=notext -- --quick
[[ "$RC" -eq 0 ]] && has 'not available yet' "$T/out"; chk lint_without_text_option_not_used "exit $RC" $?

echo "GROUP lock_and_disk_line"
EV="$T/ev40"; mkdir -p "$EV"
( env LJ_RUNNER_AREAS_FILE="$T/a_hang.txt" LJ_RUNNER_EVIDENCE_DIR="$EV" LJ_RUNNER_TESTS_DIR="$FAKE" LJ_RUNNER_TIMEOUT_S=2 LJ_RUNNER_KILL_GRACE_S=1 LJ_SCRATCH="$T/scratch" bash "$RUNNER" --quick > "$T/lockA.out" 2>&1 ) &
apid=$!; sleep 1.2
rr "$EV" "$T/a_pass.txt" -- --quick
[[ "$RC" -eq 3 ]] && has 'BUSY: another run_week2_checks.sh' "$T/err"; chk second_runner_for_the_same_evidence_folder_is_refused "exit $RC while the first holds the lock" $?
wait "$apid" 2>/dev/null
rr "$EV" "$T/a_pass.txt" -- --quick
chk lock_is_released_when_the_first_runner_ends "exit $RC afterwards" "$([[ "$RC" -eq 0 ]] && echo 0 || echo 1)"
EV="$T/ev41"; mkdir -p "$EV"; rr "$EV" "$T/a_pass.txt" LJ_DF_CMD="echo 123" -- --quick
has 'Avail at start: 123 MB \(hard floor 250 MB\) - BELOW the hard floor' "$T/out"; chk low_disk_is_named_at_the_start "LJ_DF_CMD=123 gives the BELOW line" $?
EV="$T/ev42"; mkdir -p "$EV"; rr "$EV" "$T/a_pass.txt" LJ_DF_CMD="echo 900" -- --quick
has 'Avail at start: 900 MB \(hard floor 250 MB\)\. ' "$T/out"; chk enough_disk_gives_no_warning "LJ_DF_CMD=900 gives no BELOW line" $?

echo "GROUP environment_failures"
EV="$T/ev50"; mkdir -p "$EV"; : > "$EV/wp11a"
rr "$EV" "$T/a_pass.txt" -- --quick
[[ "$RC" -eq 3 && ! -e "$EV/fk-pass" ]] && has 'not writable' "$T/err"; chk unwritable_evidence_folder_exit_3 "wp11a is a file: exit $RC, nothing ran" $?
EV="$T/ev51"; mkdir -p "$EV"; echo stale > "$EV/INDEX.md"; echo stale > "$EV/wave1_quick.txt"; echo stale > "$EV/week2_summary.json"
rr "$EV" "$T/a_email.txt" LJ_RUNNER_LINT="$STUB" STUB_MODE=oserror -- --quick
[[ "$RC" -eq 3 ]] && has 'is the disk full' "$T/err"; chk scanner_oserror_is_an_environment_failure_exit_3 "exit $RC (a full disk is not a redaction finding)" $?
[[ ! -e "$EV/INDEX.md" && ! -e "$EV/wave1_quick.txt" && ! -e "$EV/week2_summary.json" ]]; chk failed_run_removes_older_outputs "no stale INDEX.md, JSON or wave1_quick.txt is left looking current" $?

echo "GROUP interrupt"
EV="$T/ev43"; mkdir -p "$EV"; rm -f "$T/pids43"
env LJ_RUNNER_AREAS_FILE="$T/a_hang.txt" LJ_RUNNER_EVIDENCE_DIR="$EV" LJ_RUNNER_TESTS_DIR="$FAKE" LJ_RUNNER_TIMEOUT_S=60 LJ_RUNNER_KILL_GRACE_S=1 \
    LJ_SCRATCH="$T/scratch" FK_PIDFILE="$T/pids43" bash "$RUNNER" --quick > "$T/int.out" 2>&1 &
rpid=$!
for _ in $(seq 1 40); do [[ -s "$T/pids43" ]] && break; sleep 0.1; done
kill -TERM "$rpid" 2>/dev/null; wait "$rpid" 2>/dev/null; RC=$?
n43=0; for p in $(cat "$T/pids43" 2>/dev/null); do alive "$p" && n43=$((n43 + 1)); done
[[ "$RC" -eq 143 && "$n43" -eq 0 && -s "$T/pids43" ]]; chk term_stops_the_runner_and_kills_the_running_area "runner exit $RC; area processes still running: $n43" $?
chk interrupted_runner_removes_its_scratch "no .wk2run folder left" "$(ls -A "$T/scratch" | grep -c wk2run | sed 's/^0$/0/;t;s/.*/1/')"
[[ ! -e "$EV/INDEX.md" ]]; chk interrupted_runner_writes_no_index "no INDEX.md from a run that never finished" $?

echo "GROUP static"
t runner_syntax_bash_n "bash -n scripts/run_week2_checks.sh" bash -n "$RUNNER"
t runner_header_lists_the_13_areas "header names all 13 in order" bash -c "grep -n '^#   *[0-9]* *\(hygiene\|win\|ops\|validators\|render\|roundtrip\|sp1\|win_lj\|win_kit2\|phone\|spikes\|runner\|integration\) ' '$RUNNER' | awk '{print \$3}' | tr '\n' ' ' | grep -q 'hygiene win ops validators render roundtrip sp1 win_lj win_kit2 phone spikes runner integration'"
t runner_writes_no_bytecode "no lj_public_lint bytecode in scripts/__pycache__" test "$(find "$REPO/scripts/__pycache__" -name '*lj_public_lint*' 2>/dev/null | wc -l)" -eq 0

echo "GROUP edge_cases"
echo 'fk_edge|FK-6|fk-edge|1|edge cases' > "$T/a_edge.txt"
EV="$T/ev20"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=stray FK_PIDFILE="$T/stray.pid" -- --quick
sp="$(cat "$T/stray.pid" 2>/dev/null)"; sleep 0.3
[[ -n "$sp" ]] && ! alive "$sp"; chk stray_background_process_is_killed "exit $RC; pid ${sp:-none} gone" $?
has 'left background processes behind; killed' "$T/out"; chk stray_process_is_reported "console names it" $?
EV="$T/ev21"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=exit3 -- --quick
[[ "$RC" -eq 1 ]] && has 'FAIL +[0-9]+ s +exit 3 +exit 3 = environment' "$T/out"; chk exit_3_is_a_fail_with_environment_note "exit $RC" $?
EV="$T/ev22"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=longlog -- --quick
nl="$(wc -l < "$EV/wp11a/area_fk_edge_quick.txt")"
[[ "$nl" -le 403 ]] && has 'earlier [0-9]+ lines omitted' "$EV/wp11a/area_fk_edge_quick.txt" && has '^line 450$' "$EV/wp11a/area_fk_edge_quick.txt"; lrc=$?
chk long_log_is_capped_at_400_lines "$nl lines kept (header, omitted-note, 400), last line kept" "$lrc"
EV="$T/ev23"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=ansi -- --quick
[[ "$RC" -eq 0 ]] && ! grep -qP '[\x00-\x08\x0b-\x1f\x7f]' "$EV/wp11a/area_fk_edge_quick.txt" "$EV/wave1_quick.txt" && has 'red text' "$EV/wp11a/area_fk_edge_quick.txt"; chk control_characters_and_colour_codes_are_stripped "no ESC, CR or NUL in stored text" $?
EV="$T/ev24"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=badjson -- --quick
python3 -I - "$EV" > "$T/edge.out" 2>&1 <<'PY'
import json, sys
d = json.load(open(sys.argv[1] + "/week2_summary.json"))
x = d["areas"][0]
assert d["exit_code"] == 0 and x["counts"]["PASS"] == 1 and sum(x["counts"].values()) == 1, x["counts"]
assert x["avail_mb_min"] is None and x["unknown_status_envelopes"] == 1 and x["unreadable_evidence_files"] == 1, x
print("malformed file counted as unreadable, unknown status ignored, missing disk block gives n/a")
PY
erc=$?; chk malformed_and_odd_envelopes_do_not_crash_the_index "$(tail -n 1 "$T/edge.out")" "$erc"
has '\| n/a \|' "$EV/INDEX.md"; chk missing_disk_block_shows_n_a "INDEX shows n/a" $?
EV="$T/ev25"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=passfail -- --quick
[[ "$RC" -eq 0 ]] && has '^Check: fk_edge \(FK-6\) exited 0 but 1 FAIL envelope' "$T/out" && has '^- Check: fk_edge' "$EV/INDEX.md"; chk pass_with_a_fail_envelope_is_called_out "exit $RC; Check line in console and INDEX" $?
python3 -I -c "import json,sys;d=json.load(open('$EV/week2_summary.json'));sys.exit(0 if len(d['checks'])==1 else 1)"; chk checks_are_in_the_json "one check recorded" $?
EV="$T/ev26"; mkdir -p "$EV"; rr "$EV" "$T/a_edge.txt" FK_EDGE=exit3 -- --quick
has '^Check: fk_edge \(FK-6\) did not pass but no FAIL or BLOCKED envelope' "$T/out"; chk fail_without_any_envelope_is_called_out "exit 3 area with no envelopes" $?
EV="$T/ev27"; mkdir -p "$EV"; rr "$EV" "$AREAS" -- --quick
! has '^Check: fk_(pass|fail|email)' "$T/out"; chk consistent_areas_raise_no_check "fk_pass, fk_fail, fk_email: exit and envelopes agree" $?

if [[ "$MODE" == "all" ]]; then
  echo "GROUP per_area_quick_limit_all_mode"
  EV="$T/ev43"; mkdir -p "$EV"; rr "$EV" "$T/a_qlim.txt" FK_SLEEP=1.5 LJ_RUNNER_TIMEOUT_S= -- --all
  [[ "$RC" -eq 0 ]] && has 'fk_pass +FK-1 +PASS' "$T/out" && ! has 'own limit' "$T/out"; chk area_quick_limit_is_not_used_by_all "exit $RC; the 1.5 s area passed under the --all default (900 s)" $?
  EV="$T/ev44"; mkdir -p "$EV"; rr "$EV" "$T/a_qlim.txt" FK_SLEEP=1.5 LJ_RUNNER_TIMEOUT_S=4 -- --quick
  [[ "$RC" -eq 0 ]] && has 'fk_pass +FK-1 +PASS' "$T/out"; chk environment_limit_switches_the_area_limit_off "exit $RC; LJ_RUNNER_TIMEOUT_S=4 beat the area's 1 s" $?
fi

if [[ "$MODE" == "all" ]]; then
  echo "GROUP rerun_all_mode"
  sig() { python3 -I -c "import json,sys;d=json.load(open(sys.argv[1]));print(json.dumps([[x['area'],x['result'],x['counts'],x['envelopes']] for x in d['areas']]+[d['totals'],d['envelope_totals']],sort_keys=True))" "$1"; }
  EV="$T/ev30"; mkdir -p "$EV"; rr "$EV" "$AREAS" -- --quick; first="$(sig "$EV/week2_summary.json")"; rc1=$RC
  rr "$EV" "$AREAS" -- --quick; second="$(sig "$EV/week2_summary.json")"
  [[ "$rc1" == "$RC" && -n "$first" && "$first" == "$second" ]]; chk rerun_gives_the_same_results "second run: same exit ($RC), same results, counts and totals (times and disk figures differ by nature)" $?
  chk rerun_leaves_no_temp_files "no .tmp files in the evidence folders" "$(find "$EV" -name '*.tmp.*' | wc -l | sed 's/^0$/0/;t;s/.*/1/')"
fi
