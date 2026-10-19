#!/usr/bin/env bash
# lj_guard.sh: the disk and timing guard (build plan 4.9). Source it, or run it:
#
#   . scripts/lj_guard.sh
#   lj_df_avail_mb                                   # Avail of / in MB, from df -BM -P
#   lj_with_disk PLANNED_MB LABEL -- COMMAND ARGS... # a write over 100 MB goes through here
#   lj_bench COMMAND ARGS...                         # a timed run (seconds, fps, RSS) goes through here
#   lj_ledger_last LABEL                             # the last ledger line for LABEL (for the evidence envelope)
#
#   bash scripts/lj_guard.sh avail | with_disk PLANNED_MB LABEL -- CMD... | bench CMD... | ledger LABEL
#
# WHY. Everything (the repo, the scratch folder, /tmp, other jobs' files) is one nearly full volume that
# other jobs also write to. A rule four parallel agents must remember does not hold, so the rule is code.
#
# lj_with_disk PLANNED_MB LABEL -- COMMAND...
#   1. takes an exclusive lock on <scratch>/disk.lock and writes LABEL into it, so a waiting job can see
#      who holds it. Waits up to LJ_LOCK_WAIT_S seconds (default 5400 = 90 minutes), then prints
#      "BUSY: held by <label>" and exits 3 instead of hanging.
#   2. reads live Avail and REFUSES (exit 3, exact figures) unless  Avail - PLANNED_MB >= LJ_FLOOR_MB (400).
#   3. runs COMMAND in its own process group under a watchdog that polls df every LJ_POLL_S seconds (5).
#      If Avail drops below LJ_HARD_FLOOR_MB (250), whoever is writing, it sends TERM to COMMAND's whole
#      group (so COMMAND's own cleanup trap runs), waits up to LJ_TERM_GRACE_S (20) for it, then KILLs
#      what is left, runs the optional LJ_ON_ABORT command line, prints "DISK-FLOOR: ..." and exits 3.
#   4. HOLDS the lock until COMMAND, including its cleanup, has finished; then releases it.
#   5. appends one non-identifying JSON line (label, planned, start, min, end, date, status, exit) to
#      <scratch>/disk-ledger.jsonl. The label is sanitised (slashes and at-signs become underscores), so a
#      path or a user@host can not reach the ledger through it.
#   Exit code: COMMAND's own code when it ran to the end; 3 for BUSY, REFUSED, DISK-FLOOR; 2 for bad usage.
#
# lj_bench COMMAND...
#   exclusive lock on <scratch>/bench.lock; records nproc and /proc/loadavg at start (printed, appended to
#   <scratch>/bench-ledger.jsonl, and exported to COMMAND as LJ_BENCH_NPROC, LJ_BENCH_LOAD1_START and
#   LJ_BENCH_CONTAMINATED = yes when the 1-minute load at start was above LJ_BENCH_LOAD_FRAC * nproc, 0.25).
#   Two timed runs never overlap. FIXED NESTING ORDER: disk, then bench. lj_bench inside lj_with_disk
#   works; lj_with_disk inside lj_bench is refused (exit 3) because two waiting jobs could deadlock.
#   A second lj_with_disk inside a running one (or lj_bench inside lj_bench) is refused for the same reason.
#
# Environment knobs (tests use them; the defaults are the plan's numbers):
#   LJ_SCRATCH        folder for the locks and ledgers (default: build-scratch beside the repo folder)
#   LJ_DF_CMD         replaces "df -BM -P /"; must print df -P style output (header, then a line whose 4th
#                     column is Avail with an M suffix) or just an integer number of MB
#   LJ_FLOOR_MB 400   LJ_HARD_FLOOR_MB 250   LJ_POLL_S 5   LJ_LOCK_WAIT_S 5400   LJ_TERM_GRACE_S 20
#   LJ_ON_ABORT       command line run (once, under the lock) after the group was stopped by the floor
#   LJ_LOADAVG_FILE   replaces /proc/loadavg   LJ_NPROC replaces nproc   LJ_BENCH_LOAD_FRAC 0.25
#
# WHAT IT NEVER TOUCHES. It reads df, nproc and /proc/loadavg. It writes only disk.lock, bench.lock,
# disk-ledger.jsonl, bench-ledger.jsonl and one throw-away state folder (removed again) under LJ_SCRATCH.
# It deletes nothing of yours; cleanup is COMMAND's own trap or the LJ_ON_ABORT line you pass.
# It prints no path, no host name and no user name. Sourcing it changes no shell option.
# Requires bash 4+, flock, awk. COMMAND may be an executable or a shell function.

_LJ_GUARD_FILE="${BASH_SOURCE[0]}"
_LJ_GUARD_DIR="$(cd "$(dirname "$_LJ_GUARD_FILE")" && pwd)"

_lj_scratch() {
  if [[ -n "${LJ_SCRATCH:-}" ]]; then printf '%s\n' "$LJ_SCRATCH"; else printf '%s\n' "$(cd "$_LJ_GUARD_DIR/../.." && pwd)/build-scratch"; fi
}

_lj_say() { printf 'lj_guard: %s\n' "$*" >&2; }

# sanitise a label: letters, digits and . _ : + - space only; at most 60 characters
_lj_label() {
  local l="$1"
  l="${l//[^A-Za-z0-9._:+ -]/_}"
  printf '%s\n' "${l:0:60}"
}

lj_df_avail_mb() {
  local out cmd
  if [[ -n "${LJ_DF_CMD:-}" ]]; then
    read -r -a cmd <<<"$LJ_DF_CMD"
    out="$(LC_ALL=C "${cmd[@]}" 2>/dev/null)" || return 1
  else
    out="$(LC_ALL=C df -BM -P / 2>/dev/null)" || return 1
  fi
  if [[ "$out" =~ ^[[:space:]]*([0-9]+)[[:space:]]*$ ]]; then printf '%s\n' "${BASH_REMATCH[1]}"; return 0; fi
  printf '%s\n' "$out" | awk 'NR==1{next} NF>=4{v=$4; gsub(/[^0-9]/,"",v); if(v!=""){print v; exit}}'
}

_lj_now_s()  { date -u +%Y-%m-%dT%H:%M:%SZ; }
_lj_today()  { date -u +%Y-%m-%d; }

_lj_ledger_line() {  # label planned start min end status exit started ended waited
  printf '{"label":"%s","planned_mb":%s,"avail_mb_start":%s,"avail_mb_min":%s,"avail_mb_end":%s,"floor_mb":%s,"hard_floor_mb":%s,"date_utc":"%s","started_utc":"%s","ended_utc":"%s","lock_wait_s":%s,"status":"%s","exit":%s}\n' \
    "$1" "$2" "${3:-null}" "${4:-null}" "${5:-null}" "${LJ_FLOOR_MB:-400}" "${LJ_HARD_FLOOR_MB:-250}" "$(_lj_today)" "$8" "$9" "${10:-0}" "$6" "$7"
}

lj_ledger_last() {
  local f; f="$(_lj_scratch)/disk-ledger.jsonl"
  [[ -f "$f" ]] || return 1
  grep -F "\"label\":\"$(_lj_label "$1")\"" "$f" | tail -n 1
}

# ----------------------------------------------------------------------------- lj_with_disk
lj_with_disk() (
  set +e   # a subshell: the caller's own 'set -e' must not abort the guard half way (wait of a killed watchdog returns 143)
  local planned="${1:-}" label_raw="${2:-}" scratch lock ledger floor hard poll waitmax grace label
  local fd avail_start avail_end avail_min st_dir pid wd_pid rc status started ended t0 t1 waited holder
  if [[ -z "$planned" || -z "$label_raw" || "${3:-}" != "--" || $# -lt 4 ]]; then
    _lj_say "usage: lj_with_disk PLANNED_MB LABEL -- COMMAND [ARGS...]"; exit 2
  fi
  if ! [[ "$planned" =~ ^[0-9]+$ ]]; then _lj_say "usage: PLANNED_MB must be a whole number of MB"; exit 2; fi
  shift 3
  label="$(_lj_label "$label_raw")"
  floor="${LJ_FLOOR_MB:-400}"; hard="${LJ_HARD_FLOOR_MB:-250}"; poll="${LJ_POLL_S:-5}"
  waitmax="${LJ_LOCK_WAIT_S:-5400}"; grace="${LJ_TERM_GRACE_S:-20}"
  if [[ -n "${LJ_HOLDS_BENCH:-}" ]]; then
    _lj_say "REFUSED: lj_with_disk was called inside lj_bench. The lock order is disk, then bench, never the reverse (two waiting jobs could deadlock). Start the timed run inside the disk stage instead."
    exit 3
  fi
  if [[ -n "${LJ_HOLDS_DISK:-}" ]]; then
    _lj_say "REFUSED: lj_with_disk was called inside a running lj_with_disk (it would wait for its own lock forever). Merge the two stages."
    exit 3
  fi
  scratch="$(_lj_scratch)"; lock="$scratch/disk.lock"; ledger="$scratch/disk-ledger.jsonl"
  mkdir -p "$scratch" 2>/dev/null || { _lj_say "cannot create the scratch folder"; exit 3; }
  exec {fd}<>"$lock" || { _lj_say "cannot open the lock file"; exit 3; }
  t0=$SECONDS
  if ! flock -w "$waitmax" "$fd"; then
    holder="$(head -n 1 "$lock" 2>/dev/null | tr -d '\r')"
    _lj_say "BUSY: held by ${holder:-unknown} (waited ${waitmax}s for the disk lock; $label wanted ${planned} MB)"
    exit 3
  fi
  waited=$((SECONDS - t0))
  printf '%s\n' "$label" > "$lock"
  started="$(_lj_now_s)"

  avail_start="$(lj_df_avail_mb)"
  if ! [[ "$avail_start" =~ ^[0-9]+$ ]]; then
    _lj_say "cannot read free disk space (df gave no number); nothing was started"
    ended="$(_lj_now_s)"; _lj_ledger_line "$label" "$planned" null null null "unreadable" 3 "$started" "$ended" "$waited" >> "$ledger"
    exit 3
  fi
  if (( avail_start - planned < floor )); then
    _lj_say "REFUSED: Avail ${avail_start} MB minus planned ${planned} MB leaves $((avail_start - planned)) MB, below the ${floor} MB floor ($label). Lean-profile hint: plan a smaller stage, delete downloads you no longer need, or ask the orchestrator about the regenerable caches (Q-1)."
    ended="$(_lj_now_s)"; _lj_ledger_line "$label" "$planned" "$avail_start" "$avail_start" "$avail_start" "refused" 3 "$started" "$ended" "$waited" >> "$ledger"
    exit 3
  fi

  st_dir="$(mktemp -d "$scratch/.ljg.XXXXXX")" || { _lj_say "cannot create a state folder"; exit 3; }
  printf '%s\n' "$avail_start" > "$st_dir/min"
  export LJ_HOLDS_DISK=1 LJ_DISK_LABEL="$label" LJ_DISK_START_MB="$avail_start" LJ_DISK_PLANNED_MB="$planned"
  _lj_say "$label: planned ${planned} MB, Avail ${avail_start} MB, floor ${floor} MB, hard floor ${hard} MB"

  # job control makes the background command the leader of its own process group (pgid = its pid),
  # so the watchdog can stop the command and everything it started with one signal
  exec 7<&0
  set -m
  "$@" <&7 7<&- {fd}>&- &
  pid=$!
  set +m   # keep the process group, but stop the shell from printing "[1]+ Done" job notices
  exec 7<&-

  # watchdog: polls df; below the hard floor it stops the command's group
  (
    trap '[[ -n "${sl:-}" ]] && kill "$sl" 2>/dev/null; exit 0' TERM
    m="$avail_start"
    while kill -0 "$pid" 2>/dev/null; do
      a="$(lj_df_avail_mb)"
      if [[ "$a" =~ ^[0-9]+$ ]]; then
        if (( a < m )); then m="$a"; printf '%s\n' "$m" > "$st_dir/min"; fi
        if (( a < hard )); then
          printf '%s\n' "$a" > "$st_dir/floor"
          kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null
          exit 0
        fi
      fi
      sleep "$poll" &
      sl=$!
      wait "$sl" 2>/dev/null
    done
  ) {fd}>&- &
  wd_pid=$!

  trap 'kill -TERM -- "-$pid" 2>/dev/null' INT TERM
  wait "$pid"; rc=$?
  # a signal that interrupted wait: keep waiting for the real exit
  while kill -0 "$pid" 2>/dev/null; do wait "$pid"; rc=$?; done
  trap - INT TERM

  if [[ -f "$st_dir/floor" ]]; then
    # the watchdog sent TERM; give the command's own trap time to finish, then stop what is left
    t1=$SECONDS
    while kill -0 -- "-$pid" 2>/dev/null && (( SECONDS - t1 < grace )); do sleep 0.2; done
    kill -KILL -- "-$pid" 2>/dev/null
    status="floor"; rc=3
    if [[ -n "${LJ_ON_ABORT:-}" ]]; then
      _lj_say "$label: running the abort cleanup line"
      bash -c "$LJ_ON_ABORT" {fd}>&- || true
    fi
  else
    status="ok"; [[ $rc -ne 0 ]] && status="command-failed"
  fi
  kill "$wd_pid" 2>/dev/null; wait "$wd_pid" 2>/dev/null
  avail_end="$(lj_df_avail_mb)"; [[ "$avail_end" =~ ^[0-9]+$ ]] || avail_end="$avail_start"
  avail_min="$(cat "$st_dir/min" 2>/dev/null)"; [[ "$avail_min" =~ ^[0-9]+$ ]] || avail_min="$avail_start"
  (( avail_end < avail_min )) && avail_min="$avail_end"
  if [[ "$status" == "floor" ]]; then
    _lj_say "DISK-FLOOR: Avail fell to $(cat "$st_dir/floor") MB, below the ${hard} MB hard floor, while $label was running; its process group was stopped (min ${avail_min} MB, end ${avail_end} MB)"
  else
    _lj_say "$label: finished with exit $rc; Avail start ${avail_start} MB, min ${avail_min} MB, end ${avail_end} MB"
  fi
  ended="$(_lj_now_s)"
  _lj_ledger_line "$label" "$planned" "$avail_start" "$avail_min" "$avail_end" "$status" "$rc" "$started" "$ended" "$waited" >> "$ledger"
  rm -rf "$st_dir"
  exit "$rc"
)

# ----------------------------------------------------------------------------- lj_bench
lj_bench() (
  set +e
  local scratch lock ledger fd waitmax holder nproc_n load1 loadline frac contaminated rc label started ended t0 waited
  if [[ $# -lt 1 ]]; then _lj_say "usage: lj_bench COMMAND [ARGS...]"; exit 2; fi
  if [[ -n "${LJ_HOLDS_BENCH:-}" ]]; then
    _lj_say "REFUSED: lj_bench was called inside a running lj_bench (two timed runs never overlap, and it would wait for its own lock)."
    exit 3
  fi
  waitmax="${LJ_LOCK_WAIT_S:-5400}"
  scratch="$(_lj_scratch)"; lock="$scratch/bench.lock"; ledger="$scratch/bench-ledger.jsonl"
  mkdir -p "$scratch" 2>/dev/null || { _lj_say "cannot create the scratch folder"; exit 3; }
  label="$(_lj_label "${LJ_BENCH_LABEL:-$(basename -- "$1")}")"
  exec {fd}<>"$lock" || { _lj_say "cannot open the lock file"; exit 3; }
  t0=$SECONDS
  if ! flock -w "$waitmax" "$fd"; then
    holder="$(head -n 1 "$lock" 2>/dev/null | tr -d '\r')"
    _lj_say "BUSY: held by ${holder:-unknown} (waited ${waitmax}s for the bench lock)"
    exit 3
  fi
  waited=$((SECONDS - t0))
  printf '%s\n' "$label" > "$lock"
  started="$(_lj_now_s)"
  nproc_n="${LJ_NPROC:-$(nproc 2>/dev/null || echo 1)}"
  loadline="$(cat "${LJ_LOADAVG_FILE:-/proc/loadavg}" 2>/dev/null | awk '{print $1" "$2" "$3}')"
  load1="${loadline%% *}"; [[ -n "$load1" ]] || load1=0
  frac="${LJ_BENCH_LOAD_FRAC:-0.25}"
  contaminated="$(awk -v l="$load1" -v n="$nproc_n" -v f="$frac" 'BEGIN{print (l+0 > n*f) ? "yes" : "no"}')"
  _lj_say "bench: nproc=${nproc_n} loadavg_start=${loadline:-unknown} contaminated=${contaminated} ($label)"
  export LJ_HOLDS_BENCH=1 LJ_BENCH_NPROC="$nproc_n" LJ_BENCH_LOAD1_START="$load1" LJ_BENCH_CONTAMINATED="$contaminated"
  "$@" {fd}>&-
  rc=$?
  ended="$(_lj_now_s)"
  printf '{"label":"%s","nproc":%s,"load1_start":%s,"contaminated":"%s","date_utc":"%s","started_utc":"%s","ended_utc":"%s","exit":%s}\n' \
    "$label" "$nproc_n" "$load1" "$contaminated" "$(_lj_today)" "$started" "$ended" "$rc" >> "$ledger"
  exit "$rc"
)

# ----------------------------------------------------------------------------- run as a program
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  case "${1:-}" in
    avail)     lj_df_avail_mb ;;
    with_disk) shift; lj_with_disk "$@" ;;
    bench)     shift; lj_bench "$@" ;;
    ledger)    shift; lj_ledger_last "$@" ;;
    *) printf 'usage: bash scripts/lj_guard.sh avail | with_disk PLANNED_MB LABEL -- CMD... | bench CMD... | ledger LABEL\n' >&2; exit 2 ;;
  esac
fi
