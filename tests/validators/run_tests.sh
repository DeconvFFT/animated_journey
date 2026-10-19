#!/usr/bin/env bash
# tests/validators/run_tests.sh [--quick|--all] [--planned-mb N] [--wait SECONDS] [--unguarded]    WP-05: the validators
#
#   --quick  (at most 60 s, no downloads, no timed runs) syntax and portability checks, data-file checks, both self-tests,
#            the derived-form leak test, and a handful of good and planted-defect files through spec_check.py
#   --all    everything in --quick plus: colour_patch.py --all on this ffmpeg (writes the raw record that is filed ONLY because
#            it is this container's public Ubuntu build), the Q-F1 regression oracle, the F-12 measurements, all good files and
#            all planted defects, the MO8 gate pair and its refusals, public_lint.py, stale_check.py. The render stage runs as ONE
#            lj_with_disk stage (build plan 4.9, planned peak 150 MB in the plan).
#
# Options: --planned-mb N  planned peak of the stage. Default: 150 (the plan's figure) when Avail - 150 >= 400 MB, else a lean
#                          figure of 30 MB: the measured peak of the generated files is 20 MB; plus 25% (4.9), rounded up. The real
#                          peak is measured and recorded in every run.
#          --wait S        if the guard would refuse for lack of free disk, poll every 20 s for up to S seconds (default 0)
#          --unguarded     if the guard still refuses (or is busy) after the wait, run anyway under the plan's under-100-MB rule and
#                          record the stage as SKIPPED with the reason; without this flag a refusal ends in BLOCKED (exit 3)
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
# Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if the disk guard blocked the stage.
# Every test also writes one evidence envelope (build plan 4.2) to build/evidence/wp05/tests_quick.jsonl or tests_all.jsonl (one file per mode,
# so a later --quick run can not overwrite the --all envelopes).
# Everything is generated at test time under renders/wp05/ (git-ignored) and removed again; nothing uses the network.
set -u
MODE="--quick"; PLANNED=""; WAIT=0; UNGUARDED=0; INNER=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick|--all) MODE="$1";;
    --planned-mb) PLANNED="$2"; shift;;
    --wait) WAIT="$2"; shift;;
    --unguarded) UNGUARDED=1;;
    --inner) INNER=1;;
    *) echo "usage: run_tests.sh [--quick|--all] [--planned-mb N] [--wait S] [--unguarded]" >&2; exit 2;;
  esac
  shift
done
M="${MODE#--}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SELF="$ROOT/tests/validators/run_tests.sh"
EVID="$ROOT/build/evidence/wp05"
WORK="$ROOT/renders/wp05"
mkdir -p "$EVID" "$ROOT/renders"
DRIVER=(python3 -I "$ROOT/tests/validators/run_checks.py" --mode "$M" --work "$WORK" --evidence "$EVID")

if [ "$INNER" = 1 ] || [ "$M" = quick ]; then
  [ "$INNER" = 1 ] && : > "$WORK.started"
  "${DRIVER[@]}"; exit $?
fi

# ---------------------------------------------------------------- the guarded stage (--all)
# shellcheck disable=SC1091
. "$ROOT/scripts/lj_guard.sh"
AV="$(lj_df_avail_mb)"
if [ -z "$PLANNED" ]; then
  if [ "${AV:-0}" -ge 550 ]; then PLANNED=150; PROFILE=full; else PLANNED=30; PROFILE=lean; fi
else PROFILE=explicit; fi
echo "run_tests.sh --all: one lj_with_disk stage, label wp05-validators, planned ${PLANNED} MB (${PROFILE} profile), Avail ${AV} MB, floor 400 MB."
waited=0
while [ "$(( $(lj_df_avail_mb) - PLANNED ))" -lt 400 ] && [ "$waited" -lt "$WAIT" ]; do
  echo "  waiting: Avail $(lj_df_avail_mb) MB minus planned ${PLANNED} MB is below the 400 MB floor (${waited}s of ${WAIT}s)"; sleep 20; waited=$((waited + 20))
done
rm -f "$WORK.started"
LJ_WP05_PLANNED="$PLANNED" LJ_WP05_PROFILE="$PROFILE" lj_with_disk "$PLANNED" wp05-validators -- bash "$SELF" --all --inner
RC=$?
if [ ! -f "$WORK.started" ]; then
  # the guard refused (or was busy): the stage never started
  AV2="$(lj_df_avail_mb)"
  MSG="the disk guard did not start the stage: Avail ${AV2} MB minus planned ${PLANNED} MB is below the 400 MB floor, or the lock was busy (exit ${RC})"
  if [ "$UNGUARDED" = 1 ]; then
    echo "run_tests.sh --all: $MSG. --unguarded given: running directly under the plan's under-100-MB rule (4.9); the stage is recorded as SKIPPED with this reason."
    LJ_WP05_GUARD=bypassed LJ_WP05_GUARD_WHY="$MSG" bash "$SELF" --all --inner
    RC=$?
    rm -f "$WORK.started"
  else
    echo "BLOCKED  stage.disk_guard  $MSG. Remedy: free space (other jobs write to this volume), wait, or pass --wait S / --unguarded."
    python3 -I - "$EVID/tests_all.jsonl" "$MSG" <<'PY'
import json, sys, datetime
rec = {"schema": "lj-evidence/1", "package": "WP-05", "test": "stage.disk_guard", "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
       "status": "BLOCKED", "env": {"platform": "linux"}, "disk": {"avail_mb_start": 0, "planned_write_mb": 0, "avail_mb_min": 0, "avail_mb_end": 0, "floor_mb": 400, "hard_floor_mb": 250},
       "expected": "stage runs inside lj_with_disk", "actual": sys.argv[2], "notes": "", "unverified_reasons": []}
open(sys.argv[1], "w").write(json.dumps(rec, sort_keys=True) + "\n")
PY
    exit 3
  fi
fi
rm -f "$WORK.started"
# the guard's ledger line (label, planned, start, min, end) is the disk evidence for the stage
lj_ledger_last wp05-validators > "$EVID/guard_stage.json" 2>/dev/null || true
exit $RC
