#!/usr/bin/env bash
# Fake FAILING area for tests/runner. Writes a FAIL, a BLOCKED and a SKIPPED envelope and exits 1.
set -u
EV="${LJ_RUNNER_EVIDENCE_DIR:?}/fk-fail"; mkdir -p "$EV"
one() { printf '{"schema":"lj-evidence/1","package":"FK-2","test":"%s","date_utc":"2026-10-19","status":"%s","disk":{"avail_mb_min":%s},"expected":"x","actual":"y","notes":"","unverified_reasons":[]}\n' "$1" "$2" "$3"; }
{ one a FAIL 800; one b BLOCKED 700; one c SKIPPED 900; } > "$EV/tests.jsonl"
echo "fk_fail: mode=${1#--}"
echo "RESULT FAIL fk_fail :: deliberate failure"
exit 1
