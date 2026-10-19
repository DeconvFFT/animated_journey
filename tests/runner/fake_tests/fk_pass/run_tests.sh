#!/usr/bin/env bash
# Fake PASSING area for tests/runner. Writes envelopes into $LJ_RUNNER_EVIDENCE_DIR/fk-pass and exits 0.
# FK_SLEEP=N makes it take N seconds (used to test the quick budget flag).
set -u
EV="${LJ_RUNNER_EVIDENCE_DIR:?}/fk-pass"; mkdir -p "$EV"
mode="${1:-}"
env_line() {  # date status test avail_min
  printf '{"schema":"lj-evidence/1","package":"FK-1","test":"%s","date_utc":"%s","status":"%s","env":{"platform":"linux"},"disk":{"avail_mb_start":900,"planned_write_mb":0,"avail_mb_min":%s,"avail_mb_end":900,"floor_mb":400,"hard_floor_mb":250},"expected":"x","actual":"y","notes":"","unverified_reasons":[]}\n' "$3" "$1" "$2" "$4"
}
# an OLD failing envelope for t_dup (must lose against the newer PASS below) with a higher avail_mb_min
env_line 2026-10-01 FAIL t_dup 300 > "$EV/old.jsonl"
{ env_line 2026-10-19 PASS t1 500; env_line 2026-10-19 PASS t2 450; env_line 2026-10-19 PASS t_dup 123; env_line 2026-10-19 UNVERIFIED t_win 600; } > "$EV/tests.jsonl"
printf '{"schema":"lj-evidence-summary/1","package":"FK-1"}\n' > "$EV/summary.json"
echo "fk_pass: mode=${mode#--}"
[[ -n "${FK_SLEEP:-}" ]] && sleep "$FK_SLEEP"
echo "RESULT PASS fk_pass :: 4 envelopes written"
exit 0
