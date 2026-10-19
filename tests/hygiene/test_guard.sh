#!/usr/bin/env bash
# test_guard.sh: acceptance tests for scripts/lj_guard.sh (build plan 4.9, WP-03 "guard tests").
#
# Every test uses its own throw-away scratch folder (LJ_SCRATCH) and a FAKE df (LJ_DF_CMD), so the real
# disk is never filled and the real locks are never touched. Each test prints one line:
#     RESULT PASS|FAIL <name> :: <detail>
# Exit 0 when all pass, 1 otherwise. Needs bash, flock, awk. Takes about 20 seconds.
#   bash tests/hygiene/test_guard.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
GUARD="$REPO/scripts/lj_guard.sh"
BASE="${LJ_TEST_BASE:-$(cd "$REPO/.." && pwd)/build-scratch}"
mkdir -p "$BASE"
T="$(mktemp -d "$BASE/hyg-guard.XXXXXX")"
trap 'rm -rf "$T"' EXIT
FAILS=0

pass() { printf 'RESULT PASS %s :: %s\n' "$1" "${2:-}"; }
fail() { printf 'RESULT FAIL %s :: %s\n' "$1" "${2:-}"; FAILS=$((FAILS + 1)); }
expect() { if [[ "$2" == "$3" ]]; then pass "$1" "$4"; else fail "$1" "expected [$2] got [$3] $4"; fi; }
now() { date +%s.%N; }

# a fake df: prints df -P style output with the number held in $1 (a file)
mkfake() {  # dir name value
  printf '%s\n' "$3" > "$1/$2.val"
  cat > "$1/$2.sh" <<EOF
#!/usr/bin/env bash
v=\$(cat "$1/$2.val")
printf 'Filesystem     1048576-blocks  Used Available Capacity Mounted on\n/dev/fake          100000M  9999M %sM      99%% /\n' "\$v"
EOF
  chmod +x "$1/$2.sh"
}

new_scratch() { local d="$T/$1"; mkdir -p "$d"; printf '%s\n' "$d"; }

# ----------------------------------------------------------------------------- 1. parsing of df
S="$(new_scratch s1)"; mkfake "$S" f 4321
out="$(LJ_SCRATCH="$S" LJ_DF_CMD="$S/f.sh" bash "$GUARD" avail)"
expect "avail_parses_fake_df_P_format" 4321 "$out" "(fake df -P style output)"
out="$(LJ_SCRATCH="$S" LJ_DF_CMD="echo 777" bash "$GUARD" avail)"
expect "avail_accepts_a_bare_integer" 777 "$out" ""
real="$(bash "$GUARD" avail)"; dfr="$(LC_ALL=C df -BM -P / | awk 'NR==2{gsub(/M/,"",$4);print $4}')"
if [[ "$real" =~ ^[0-9]+$ ]] && (( real - dfr < 300 && dfr - real < 300 )); then pass "avail_matches_real_df" "guard $real MB, df $dfr MB (the volume is shared, so a small drift is normal)"; else fail "avail_matches_real_df" "guard [$real] df [$dfr]"; fi

# ----------------------------------------------------------------------------- 2. usage errors and exit codes
S="$(new_scratch s2)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" LJ_POLL_S=0.3
bash "$GUARD" with_disk 10 label true 2>"$S/err"; rc=$?
expect "usage_missing_dashdash_exits_2" 2 "$rc" "$(head -c 80 "$S/err")"
bash "$GUARD" with_disk abc label -- true 2>"$S/err"; rc=$?
expect "usage_planned_not_a_number_exits_2" 2 "$rc" ""
bash "$GUARD" with_disk 10 label -- bash -c 'exit 7' 2>"$S/err"; rc=$?
expect "command_exit_code_passes_through" 7 "$rc" ""
bash "$GUARD" with_disk 10 label -- true 2>"$S/err"; rc=$?
expect "command_success_exits_0" 0 "$rc" ""

# ----------------------------------------------------------------------------- 3. refusal arithmetic (fake df 700 MB)
S="$(new_scratch s3)"; mkfake "$S" f 700
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
bash "$GUARD" with_disk 300 boundary -- true 2>"$S/err"; rc=$?
expect "df700_planned_300_runs_boundary_exactly_400_left" 0 "$rc" "Avail 700 - 300 = 400 is allowed (floor is >= 400)"
bash "$GUARD" with_disk 350 p350 -- true 2>"$S/err"; rc=$?
expect "df700_planned_350_refused_350_left" 3 "$rc" "$(grep -o 'REFUSED.*' "$S/err" | head -c 110)"
grep -q 'Avail 700 MB minus planned 350 MB leaves 350 MB, below the 400 MB floor' "$S/err" && pass "refusal_message_has_exact_figures_350" "" || fail "refusal_message_has_exact_figures_350" "$(cat "$S/err")"
bash "$GUARD" with_disk 320 p320 -- true 2>"$S/err"; rc=$?
expect "df700_planned_320_refused" 3 "$rc" ""
grep -q 'Avail 700 MB minus planned 320 MB leaves 380 MB, below the 400 MB floor' "$S/err" && pass "refusal_message_has_exact_figures_320" "" || fail "refusal_message_has_exact_figures_320" "$(cat "$S/err")"
grep -q 'Lean-profile hint' "$S/err" && pass "refusal_message_carries_the_lean_profile_hint" "" || fail "refusal_message_carries_the_lean_profile_hint" ""
bash "$GUARD" with_disk 301 p301 -- true 2>"$S/err"; rc=$?
expect "df700_planned_301_refused_one_over" 3 "$rc" ""
ran="$S/ran"; rm -f "$ran"
bash "$GUARD" with_disk 320 p320 -- bash -c "touch '$ran'" 2>/dev/null
[[ ! -e "$ran" ]] && pass "refused_command_never_started" "" || fail "refused_command_never_started" "the command ran"

# ----------------------------------------------------------------------------- 3b. leading zeros in PLANNED_MB (review r2)
# 08 used to abort the refusal test with "value too great for base" and then run the command (fail-open, exit 0);
# 010 was read as octal 8 and written to the ledger as "planned_mb":010, which is not valid JSON.
S="$(new_scratch s3b)"; mkfake "$S" f 405
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
ran="$S/ran08"; rm -f "$ran"
bash "$GUARD" with_disk 08 zero08 -- bash -c "touch '$ran'" 2>"$S/err"; rc=$?
expect "planned_08_df405_is_refused_exit_3" 3 "$rc" "$(grep -o 'REFUSED.*' "$S/err" | head -c 100)"
if grep -qiE 'value too great|syntax error|arithmetic|operand' "$S/err"; then fail "planned_08_prints_no_arithmetic_error" "$(head -c 200 "$S/err")"; else pass "planned_08_prints_no_arithmetic_error" "stderr: $(head -c 60 "$S/err" | tr '\n' ' ')"; fi
grep -q 'Avail 405 MB minus planned 8 MB leaves 397 MB, below the 400 MB floor' "$S/err" && pass "planned_08_is_read_as_decimal_8" "" || fail "planned_08_is_read_as_decimal_8" "$(head -c 200 "$S/err")"
[[ ! -e "$ran" ]] && pass "planned_08_refused_command_never_started" "" || fail "planned_08_refused_command_never_started" "the command ran (fail-open)"
bash "$GUARD" with_disk 010 zero010 -- true 2>"$S/err010"; rc=$?
expect "planned_010_df405_is_refused_as_decimal_10" 3 "$rc" "$(grep -o 'planned [0-9]* MB leaves [0-9]* MB' "$S/err010" | head -n 1)"
mkfake "$S" g 5000
LJ_DF_CMD="$S/g.sh" bash "$GUARD" with_disk 010 zero010ok -- true 2>"$S/err010ok"; rc=$?
expect "planned_010_df5000_runs_and_exits_0" 0 "$rc" ""
python3 -I - "$S/disk-ledger.jsonl" <<'PY' && pass "planned_010_ledger_lines_are_json_with_planned_mb_10" "refused and ok lines both parse and say 10" || fail "planned_010_ledger_lines_are_json_with_planned_mb_10" "$(grep -E 'zero0' "$S/disk-ledger.jsonl" | head -c 300)"
import json, sys
seen = {}
for line in open(sys.argv[1], encoding="utf-8"):
    d = json.loads(line)                      # a line with "planned_mb":010 raises here
    seen[d["label"]] = d["planned_mb"]
assert seen.get("zero08") == 8 and seen.get("zero010") == 10 and seen.get("zero010ok") == 10, seen
assert all(type(v) is int for v in seen.values()), seen
PY
grep -q '"label":"zero010ok","planned_mb":10,' "$S/disk-ledger.jsonl" && pass "planned_010_is_written_as_planned_mb_10_not_010" "" || fail "planned_010_is_written_as_planned_mb_10_not_010" "$(grep 'zero010ok' "$S/disk-ledger.jsonl" | head -c 200)"

# ----------------------------------------------------------------------------- 4. serialise, BUSY
S="$(new_scratch s4)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
# the first job holds the lock for 2.2 s, so the second waits about 1.9 s: lock_wait_s is whole seconds ($SECONDS), and only a wait of at least 1 s is sure to read 1 or more (with a 0.9 s wait the test failed about one run in ten)
job() { bash "$GUARD" with_disk 10 "$1" -- bash -c "echo start-$1 \$(date +%s.%N) >> '$S/order'; sleep 2.2; echo end-$1 \$(date +%s.%N) >> '$S/order'" 2>>"$S/err4"; }
job A & pa=$!; sleep 0.3; job B & pb=$!; wait $pa; ra=$?; wait $pb; rb=$?
expect "two_jobs_both_succeed" "0 0" "$ra $rb" ""
seq="$(awk '{print $1}' "$S/order" | tr '\n' ' ')"
expect "two_jobs_serialise_start_end_start_end" "start-A end-A start-B end-B " "$seq" "(order of start/end markers written by the jobs)"
endA="$(awk '$1=="end-A"{print $2}' "$S/order")"; startB="$(awk '$1=="start-B"{print $2}' "$S/order")"
awk -v e="$endA" -v s="$startB" 'BEGIN{exit !(s>=e)}' && pass "second_job_started_after_first_ended" "" || fail "second_job_started_after_first_ended" "endA=$endA startB=$startB"
nl="$(grep -c '"label":"[AB]"' "$S/disk-ledger.jsonl")"
expect "ledger_has_one_line_per_job" 2 "$nl" ""
la="$(grep '"label":"A"' "$S/disk-ledger.jsonl" | sed 's/.*"ended_utc":"\([^"]*\)".*/\1/')"; lb="$(grep '"label":"B"' "$S/disk-ledger.jsonl" | sed 's/.*"started_utc":"\([^"]*\)".*/\1/')"
[[ "$lb" > "$la" || "$lb" == "$la" ]] && pass "ledger_shows_them_one_after_the_other" "A ended $la, B started $lb" || fail "ledger_shows_them_one_after_the_other" "A ended $la, B started $lb"
grep '"label":"B"' "$S/disk-ledger.jsonl" | grep -q '"lock_wait_s":[1-9]' && pass "ledger_records_that_the_second_job_waited" "" || fail "ledger_records_that_the_second_job_waited" "$(grep '"label":"B"' "$S/disk-ledger.jsonl")"

S="$(new_scratch s4b)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
bash "$GUARD" with_disk 10 HOLDER-JOB -- sleep 4 2>/dev/null & ph=$!
sleep 0.5
t0="$(now)"
LJ_LOCK_WAIT_S=2 bash "$GUARD" with_disk 10 WAITER -- true 2>"$S/err"; rc=$?
t1="$(now)"
expect "waiter_with_LJ_LOCK_WAIT_S_2_exits_3" 3 "$rc" ""
grep -q 'BUSY: held by HOLDER-JOB' "$S/err" && pass "busy_message_names_the_holder" "$(grep -o 'BUSY[^(]*' "$S/err")" || fail "busy_message_names_the_holder" "$(cat "$S/err")"
awk -v a="$t0" -v b="$t1" 'BEGIN{d=b-a; exit !(d>=1.8 && d<8)}' && pass "waiter_gave_up_after_about_2_seconds" "" || fail "waiter_gave_up_after_about_2_seconds" "took $(awk -v a="$t0" -v b="$t1" 'BEGIN{print b-a}')s"
wait $ph; rch=$?
expect "holder_itself_finished_normally_despite_the_waiter" 0 "$rch" ""
LJ_LOCK_WAIT_S=2 LJ_DF_CMD="$S/f.sh" bash "$GUARD" with_disk 10 LATER -- true 2>/dev/null; rc=$?
expect "lock_is_free_again_after_the_holder_finished" 0 "$rc" ""

# ----------------------------------------------------------------------------- 5. the hard floor
S="$(new_scratch s5)"; mkfake "$S" f 900
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" LJ_POLL_S=0.3 LJ_TERM_GRACE_S=10
cat > "$S/child.sh" <<EOF
#!/usr/bin/env bash
# a sleeping child with a cleanup trap; after 1 s the "disk" drops below the hard floor
trap 'sleep 1.5; echo CLEANUP-RAN \$(date +%s.%N) > "$S/cleanup"; exit 143' TERM
echo child-started > "$S/child-started"
( sleep 1; echo 200 > "$S/f.val" ) &
sleep 30 &
wait
EOF
chmod +x "$S/child.sh"
mkfake "$T/s5w" w 5000 2>/dev/null || { mkdir -p "$T/s5w"; mkfake "$T/s5w" w 5000; }
t0="$(now)"
bash "$GUARD" with_disk 100 FLOOR-JOB -- bash "$S/child.sh" 2>"$S/err" &
pf=$!
# a waiter that must NOT get the lock until the child's cleanup has finished
( sleep 1.6; LJ_DF_CMD="$T/s5w/w.sh" bash "$GUARD" with_disk 10 AFTER-FLOOR -- bash -c "echo started \$(date +%s.%N) > '$S/waiter-started'" 2>/dev/null ) &
pw=$!
wait $pf; rc=$?
t1="$(now)"
wait $pw 2>/dev/null
expect "floor_trip_exits_3" 3 "$rc" ""
grep -q 'DISK-FLOOR' "$S/err" && pass "floor_trip_prints_DISK-FLOOR" "$(grep -o 'DISK-FLOOR[^(]*' "$S/err" | head -c 130)" || fail "floor_trip_prints_DISK-FLOOR" "$(cat "$S/err")"
[[ -s "$S/cleanup" ]] && pass "childs_cleanup_trap_ran" "" || fail "childs_cleanup_trap_ran" "no cleanup marker"
sleep 0.2
if pgrep -f "$S/child.sh" >/dev/null 2>&1; then fail "child_process_group_is_gone" "child still running"; else pass "child_process_group_is_gone" ""; fi
awk -v a="$t0" -v b="$t1" 'BEGIN{d=b-a; exit !(d<12)}' && pass "floor_trip_did_not_wait_for_the_30s_sleep" "took $(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')s" || fail "floor_trip_did_not_wait_for_the_30s_sleep" "took too long"
cl="$(awk '{print $2}' "$S/cleanup" 2>/dev/null)"; ws="$(awk '{print $2}' "$S/waiter-started" 2>/dev/null)"
if [[ -n "$cl" && -n "$ws" ]] && awk -v c="$cl" -v w="$ws" 'BEGIN{exit !(w>=c)}'; then pass "lock_was_held_through_the_cleanup" "waiter started after the cleanup finished"; else fail "lock_was_held_through_the_cleanup" "cleanup=$cl waiter=$ws"; fi
grep 'FLOOR-JOB' "$S/disk-ledger.jsonl" | grep -q '"status":"floor"' && pass "ledger_records_status_floor" "" || fail "ledger_records_status_floor" ""
mn="$(grep 'FLOOR-JOB' "$S/disk-ledger.jsonl" | sed 's/.*"avail_mb_min":\([0-9]*\).*/\1/')"
[[ "$mn" =~ ^[0-9]+$ ]] && (( mn <= 250 )) && pass "ledger_min_is_below_the_hard_floor" "min $mn MB" || fail "ledger_min_is_below_the_hard_floor" "min [$mn]"
# LJ_ON_ABORT runs under the lock, once
S="$(new_scratch s5b)"; mkfake "$S" f 900
cat > "$S/child.sh" <<EOF
#!/usr/bin/env bash
( sleep 0.7; echo 100 > "$S/f.val" ) &
sleep 30 &
wait
EOF
LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" LJ_ON_ABORT="touch '$S/aborted'" bash "$GUARD" with_disk 100 ABORT-JOB -- bash "$S/child.sh" 2>/dev/null; rc=$?
[[ $rc -eq 3 && -e "$S/aborted" ]] && pass "LJ_ON_ABORT_cleanup_line_ran_after_the_floor_trip" "" || fail "LJ_ON_ABORT_cleanup_line_ran_after_the_floor_trip" "rc=$rc"
unset LJ_ON_ABORT

# an outside TERM (a package's `timeout`) is forwarded to the command's group: its trap runs, the lock is released
S="$(new_scratch s5c)"; mkfake "$S" f 5000
cat > "$S/child.sh" <<CHILD
#!/usr/bin/env bash
trap 'echo cleanup-ran > "$S/cleanup"; exit 0' TERM
sleep 30 &
wait
CHILD
LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" timeout 1.5 bash "$GUARD" with_disk 10 TIMEOUT-JOB -- bash "$S/child.sh" 2>/dev/null; rc=$?
sleep 1
[[ $rc -eq 124 ]] && pass "outer_timeout_exits_124_as_usual" "" || fail "outer_timeout_exits_124_as_usual" "rc=$rc"
[[ -s "$S/cleanup" ]] && pass "outer_TERM_is_forwarded_and_the_childs_cleanup_trap_ran" "" || fail "outer_TERM_is_forwarded_and_the_childs_cleanup_trap_ran" "no cleanup marker"
LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" LJ_LOCK_WAIT_S=1 bash "$GUARD" with_disk 10 NEXT -- true 2>/dev/null; rc=$?
expect "lock_is_released_after_an_outer_timeout" 0 "$rc" ""
grep -q '"label":"TIMEOUT-JOB"' "$S/disk-ledger.jsonl" && pass "ledger_line_written_even_after_an_outer_timeout" "" || fail "ledger_line_written_even_after_an_outer_timeout" ""

# ----------------------------------------------------------------------------- 6. bench inside disk; reverse refused; nesting
S="$(new_scratch s6)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S" LJ_POLL_S=0.5 G="$GUARD"
bash "$GUARD" with_disk 10 OUTER -- bash -c '. "$G"; lj_bench bash -c "echo bench-ran"' >"$S/out" 2>"$S/err"; rc=$?
[[ $rc -eq 0 ]] && grep -q 'bench-ran' "$S/out" && grep -q 'bench: nproc=' "$S/err" && pass "lj_bench_inside_lj_with_disk_works" "$(grep -o 'bench: nproc=[^(]*' "$S/err")" || fail "lj_bench_inside_lj_with_disk_works" "rc=$rc $(cat "$S/err")"
bash "$GUARD" bench bash -c '. "$G"; lj_with_disk 10 INNER -- true' >"$S/out" 2>"$S/err"; rc=$?
[[ $rc -eq 3 ]] && grep -q 'lock order is disk, then bench' "$S/err" && pass "reverse_order_lj_with_disk_inside_lj_bench_refused" "exit 3 with the lock-order message" || fail "reverse_order_lj_with_disk_inside_lj_bench_refused" "rc=$rc $(cat "$S/err")"
bash "$GUARD" with_disk 10 OUTER2 -- bash -c '. "$G"; lj_with_disk 10 INNER2 -- true' >"$S/out" 2>"$S/err"; rc=$?
[[ $rc -ne 0 ]] && grep -q 'REFUSED: lj_with_disk was called inside a running lj_with_disk' "$S/err" && pass "nested_lj_with_disk_refused_not_deadlocked" "" || fail "nested_lj_with_disk_refused_not_deadlocked" "rc=$rc"
bash "$GUARD" bench bash -c '. "$G"; lj_bench true' >"$S/out" 2>"$S/err"; rc=$?
[[ $rc -eq 3 ]] && grep -q 'REFUSED: lj_bench was called inside a running lj_bench' "$S/err" && pass "nested_lj_bench_refused_not_deadlocked" "" || fail "nested_lj_bench_refused_not_deadlocked" "rc=$rc"
# bench lock serialises
bash "$GUARD" bench sleep 4 2>/dev/null & pb1=$!
sleep 0.4
LJ_LOCK_WAIT_S=1 bash "$GUARD" bench true 2>"$S/err"; rc=$?
[[ $rc -eq 3 ]] && grep -q 'BUSY: held by sleep' "$S/err" && pass "bench_lock_is_exclusive_and_names_the_holder" "" || fail "bench_lock_is_exclusive_and_names_the_holder" "rc=$rc $(cat "$S/err")"
kill $pb1 2>/dev/null; wait $pb1 2>/dev/null

# load and nproc recorded; contamination flag
echo "3.50 3.00 2.00 1/100 1234" > "$S/load-busy"; echo "0.05 0.10 0.10 1/100 1234" > "$S/load-idle"
out="$(LJ_LOADAVG_FILE="$S/load-busy" LJ_NPROC=4 bash "$GUARD" bench bash -c 'echo $LJ_BENCH_NPROC $LJ_BENCH_LOAD1_START $LJ_BENCH_CONTAMINATED' 2>/dev/null)"
expect "bench_exports_nproc_load_and_flags_a_busy_machine_contaminated" "4 3.50 yes" "$out" ""
out="$(LJ_LOADAVG_FILE="$S/load-idle" LJ_NPROC=4 bash "$GUARD" bench bash -c 'echo $LJ_BENCH_NPROC $LJ_BENCH_LOAD1_START $LJ_BENCH_CONTAMINATED' 2>/dev/null)"
expect "bench_idle_machine_is_not_contaminated" "4 0.05 no" "$out" ""
LJ_LOADAVG_FILE="$S/load-idle" bash "$GUARD" bench bash -c 'exit 5' 2>/dev/null; rc=$?
expect "bench_passes_the_command_exit_code" 5 "$rc" ""

# sourced into a caller that runs under set -euo pipefail, and with a shell function as the command
S="$(new_scratch s6b)"; mkfake "$S" f 5000
cat > "$S/strict.sh" <<STRICT
#!/usr/bin/env bash
set -euo pipefail
export LJ_SCRATCH="$S" LJ_DF_CMD="$S/f.sh" LJ_POLL_S=0.2
. "$GUARD"
my_fn() { echo "function ran as the command"; }
lj_with_disk 100 strict-mode -- bash -c 'echo hello from the stage'
lj_with_disk 0 fn-as-command -- my_fn
if lj_with_disk 99999 too-big -- true; then echo UNEXPECTED; else echo refused-as-expected; fi
echo survived-set-euo-pipefail
STRICT
bash "$S/strict.sh" >"$S/out" 2>"$S/err"; rc=$?
[[ $rc -eq 0 ]] && grep -q 'survived-set-euo-pipefail' "$S/out" && grep -q 'function ran as the command' "$S/out" && grep -q 'refused-as-expected' "$S/out" && grep -q 'strict-mode: finished with exit 0' "$S/err" \
  && pass "guard_works_in_a_caller_with_set_euo_pipefail_and_with_a_shell_function_as_command" "" || fail "guard_works_in_a_caller_with_set_euo_pipefail_and_with_a_shell_function_as_command" "rc=$rc $(tail -n 3 "$S/err")"

# ----------------------------------------------------------------------------- 7. the ledger carries no path or host
S="$(new_scratch s7)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
bash "$GUARD" with_disk 10 "stage/with/path@host.example C:\\x" -- true 2>/dev/null
bash "$GUARD" with_disk 10 plain-label -- true 2>/dev/null
bash "$GUARD" bench true 2>/dev/null
led="$(cat "$S/disk-ledger.jsonl" "$S/bench-ledger.jsonl")"
host="$(hostname 2>/dev/null)"; me="$(id -un 2>/dev/null)"
bad=""
[[ "$led" == *"/"* ]] && bad="$bad slash"
[[ "$led" == *"\\"* ]] && bad="$bad backslash"
[[ "$led" == *"@"* ]] && bad="$bad at-sign"
[[ -n "$host" && "$led" == *"$host"* ]] && bad="$bad hostname"
[[ -n "$me" && ${#me} -ge 4 && "$led" == *"$me"* ]] && bad="$bad username"
[[ "$led" == *"$S"* ]] && bad="$bad scratch-path"
[[ -z "$bad" ]] && pass "ledger_lines_carry_no_path_host_or_user" "$(wc -l < "$S/disk-ledger.jsonl") disk + $(wc -l < "$S/bench-ledger.jsonl") bench lines checked" || fail "ledger_lines_carry_no_path_host_or_user" "found:$bad"
grep -q '"label":"stage_with_path_host.example C:_x"' "$S/disk-ledger.jsonl" && pass "label_is_sanitised_slashes_and_at_signs_become_underscores" "" || fail "label_is_sanitised_slashes_and_at_signs_become_underscores" "$(head -c 200 "$S/disk-ledger.jsonl")"
python3 -I - "$S/disk-ledger.jsonl" <<'PY' && pass "ledger_lines_are_valid_json_with_the_envelope_fields" "" || fail "ledger_lines_are_valid_json_with_the_envelope_fields" ""
import json, sys
for line in open(sys.argv[1]):
    d = json.loads(line)
    for k in ("label", "planned_mb", "avail_mb_start", "avail_mb_min", "avail_mb_end", "floor_mb", "hard_floor_mb", "date_utc", "status", "exit"):
        assert k in d, k
PY

# ----------------------------------------------------------------------------- 8. does not touch anything but its own files
S="$(new_scratch s8)"; mkfake "$S" f 5000
export LJ_DF_CMD="$S/f.sh" LJ_SCRATCH="$S"
before="$(ls -A "$S" | sort | tr '\n' ' ')"
bash "$GUARD" with_disk 10 X -- true 2>/dev/null
after="$(ls -A "$S" | sort | tr '\n' ' ')"
new="$(comm -13 <(echo "$before" | tr ' ' '\n' | sort) <(echo "$after" | tr ' ' '\n' | sort) | tr '\n' ' ')"
expect "guard_writes_only_its_lock_and_ledger_files" "disk-ledger.jsonl disk.lock " "$new" "(new entries in the scratch folder; the state folder is removed)"

printf '\nguard tests: %d failed\n' "$FAILS"
[[ $FAILS -eq 0 ]]
