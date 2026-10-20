#!/usr/bin/env bash
# job.sh: SP4 idle-container probe. Appends one line with the current epoch second every INTERVAL seconds for SECONDS seconds, to a log under the scratch folder.
#
#   bash spikes/sp4_idle/job.sh                                 25 minutes (1500 s), one line every 10 s: the real protocol (see PROTOCOL.md)
#   bash spikes/sp4_idle/job.sh --seconds 60 --interval 2       the quick mechanism test
#   bash spikes/sp4_idle/job.sh --out FILE                      write to FILE (a new file; default <scratch>/sp4/job-<date>.log)
#   nohup bash spikes/sp4_idle/job.sh > /dev/null 2>&1 &         how the orchestrator starts the real run, so it outlives the shell
# Prints one line: where the log is (as <scratch>/... when it is under the scratch folder), then nothing until it ends.
#
# WHAT THE LOG HOLDS (text, no personal data, nothing but numbers):  '# start epoch=E interval=I seconds=S df_avail_mb=N', then 'E SEQ' per tick, then '# end epoch=E reason=done|term df_avail_mb=N'.
# A missing end line means the job was killed from outside (SIGKILL, container stop), which is exactly what gaps.py reports as "killed".
# Ticks are scheduled against the start time (tick k at start + k*INTERVAL), so a slow tick does not drift the rest, and a frozen container shows up as one long gap.
# WHAT IT NEVER TOUCHES. It reads df and the clock, writes the one log file (and creates <scratch>/sp4/), makes no network call, reads no personal file, and uses no more than 1 MB of disk.
# EXIT CODES (build plan 4.3)  0 the job ran to its end   2 bad usage / the log exists already   3 environment (cannot create the log folder or file)
set -u
export LC_ALL=C
SECONDS_TOTAL=1500; INTERVAL=10; OUT=""
SELF="${BASH_SOURCE[0]}"
ROOT="$(cd "$(dirname "$SELF")/../.." && pwd)"
SCRATCH="${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
die() { printf 'job.sh: %s\n' "$*" >&2; exit "${2:-2}"; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --seconds) SECONDS_TOTAL="${2:-}"; shift;;
    --interval) INTERVAL="${2:-}"; shift;;
    --out) OUT="${2:-}"; shift;;
    -h|--help) awk 'NR > 1 && /^#/ { print; next } NR > 1 { exit }' "$SELF"; exit 0;;
    *) die "unknown argument: $1 (try --help)";;
  esac
  shift
done
[[ "$SECONDS_TOTAL" =~ ^[0-9]{1,6}$ && "$INTERVAL" =~ ^[0-9]{1,4}$ ]] || die "--seconds and --interval need whole numbers"
(( INTERVAL >= 1 && SECONDS_TOTAL >= INTERVAL )) || die "--interval must be at least 1 and --seconds at least --interval"
if [[ -z "$OUT" ]]; then OUT="$SCRATCH/sp4/job-$(date -u +%Y%m%d-%H%M%S).log"; fi
mkdir -p "$(dirname "$OUT")" 2>/dev/null || die "cannot create the log folder" 3
[[ -e "$OUT" ]] && die "the log file exists already: it is never overwritten"
avail() { df -BM -P / 2>/dev/null | awk 'NR==2{gsub("M","",$4); print $4}'; }
shown="$OUT"; [[ "$OUT" == "$SCRATCH"/* ]] && shown="<scratch>${OUT#"$SCRATCH"}"
start="$(date +%s)"
printf '# start epoch=%s interval=%s seconds=%s df_avail_mb=%s\n' "$start" "$INTERVAL" "$SECONDS_TOTAL" "$(avail)" > "$OUT" || die "cannot write the log" 3
printf 'log: %s\n' "$shown"
reason=done
trap 'reason=term' TERM INT HUP
k=0
n=$(( SECONDS_TOTAL / INTERVAL ))
while (( k < n )) && [[ "$reason" == done ]]; do
  k=$((k + 1))
  target=$(( start + k * INTERVAL ))
  now="$(date +%s)"
  d=$(( target - now ))
  (( d > 0 )) && { sleep "$d" & wait $!; }
  [[ "$reason" == done ]] || break
  printf '%s %s\n' "$(date +%s)" "$k" >> "$OUT"
done
printf '# end epoch=%s reason=%s df_avail_mb=%s\n' "$(date +%s)" "$reason" "$(avail)" >> "$OUT"
exit 0
