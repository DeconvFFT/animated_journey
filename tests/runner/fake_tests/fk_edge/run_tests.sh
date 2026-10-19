#!/usr/bin/env bash
# Fake EDGE-CASE area for tests/runner; FK_EDGE picks the case:
#   stray    starts a background sleep (pid to $FK_PIDFILE) and exits 0 (the runner must kill what is left)
#   exit3    prints a refusal and exits 3 (environment)
#   longlog  prints 450 lines
#   ansi     prints a carriage return, colour escapes and a NUL byte
#   passfail exits 0 but leaves a FAIL envelope on file
#   badjson  writes a malformed JSON file, an envelope without a disk block, and one with an unknown status
set -u
EV="${LJ_RUNNER_EVIDENCE_DIR:?}"
case "${FK_EDGE:-}" in
  stray) sleep 300 & printf '%s\n' "$!" > "${FK_PIDFILE:-/dev/null}"; echo "stray started"; exit 0 ;;
  exit3) echo "REFUSED: fake disk guard"; exit 3 ;;
  longlog) for i in $(seq 1 450); do echo "line $i"; done; exit 0 ;;
  ansi) printf 'start\r\n\033[31mred text\033[0m\n'; printf 'nul\0byte\n'; echo done; exit 0 ;;
  passfail)
    mkdir -p "$EV/fk-edge"
    printf '%s\n' '{"schema":"lj-evidence/1","package":"FK-6","test":"quiet_fail","date_utc":"2026-10-19","status":"FAIL","disk":{"avail_mb_min":900}}' > "$EV/fk-edge/tests.jsonl"
    echo "exiting 0 with a FAIL envelope"; exit 0 ;;
  badjson)
    mkdir -p "$EV/fk-edge"
    echo '{not json' > "$EV/fk-edge/bad.json"
    printf '%s\n' '{"schema":"lj-evidence/1","package":"FK-6","test":"nodisk","status":"PASS"}' \
                  '{"schema":"lj-evidence/1","package":"FK-6","test":"weird","status":"MAYBE"}' > "$EV/fk-edge/tests.jsonl"
    echo "badjson written"; exit 0 ;;
esac
echo "fk_edge: no case chosen"; exit 0
