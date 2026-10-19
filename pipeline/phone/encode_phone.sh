#!/usr/bin/env bash
# encode_phone.sh MASTER CAPTIONS.srt OUTPUT.mp4 [more encode_phone.py options]     WP-08 (D-27)
#
# The usual way to make the phone file in the container: the same as `python3 -I pipeline/phone/encode_phone.py ...`, but run inside the disk guard
# (build plan 4.9): lj_with_disk 100 wp08-encode. The guard takes the disk lock, refuses unless Avail minus the planned MB stays at or above 400 MB,
# stops the encode if Avail falls under 250 MB, and puts one non-identifying line in <scratch>/disk-ledger.jsonl.
#
#   bash pipeline/phone/encode_phone.sh renders/wp08/master10s.mov renders/wp08/caps.srt renders/wp08/phone.mp4
#   bash pipeline/phone/encode_phone.sh MASTER.mov caps.srt out.mp4 --profile phone_720_share
#   bash pipeline/phone/encode_phone.sh MASTER.mov caps.srt out.mp4 --style venue_fs23     (REFERENCE style, not a phone deliverable)
#
# Environment: LJ_PLANNED_MB (default 100: right for a clip of a few seconds; a 12-minute PH1 can reach 737 MB, so plan 800 for the film),
#              FFMPEG / FFPROBE (a specific build), LJ_SCRATCH (see scripts/lj_guard.sh).
# File names stay RELATIVE inside ffmpeg's filter string: encode_phone.py runs ffmpeg in its own work folder (so a Windows drive-letter colon can never
# reach the filter). On Windows (UNVERIFIED) run the Python file directly:  py -3 -I pipeline\phone\encode_phone.py MASTER CAPTIONS.srt OUTPUT.mp4
# Exit codes: 0 done; 1 the file was made but a check failed; 2 bad usage or input; 3 environment problem (tool missing, disk guard refused or tripped).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
if [ "$#" -lt 2 ]; then
  sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
fi
if [ ! -f "$ROOT/scripts/lj_guard.sh" ]; then echo "ENVIRONMENT PROBLEM: scripts/lj_guard.sh is missing (WP-03); not running unguarded." >&2; exit 3; fi
# shellcheck disable=SC1091
. "$ROOT/scripts/lj_guard.sh"
PLANNED="${LJ_PLANNED_MB:-100}"
echo "encode_phone.sh: running inside lj_with_disk ${PLANNED} (label wp08-encode)"
lj_with_disk "$PLANNED" wp08-encode -- python3 -I "$HERE/encode_phone.py" "$@"
