#!/usr/bin/env bash
# tests/phone/run_tests.sh [--quick|--all|--list|--only name,name]    WP-08: the phone deliverable (profile, encode, legibility and fill-crop check, sharing simulation)
#
#   --quick  (about a minute, no render, no download, under 20 MB) static checks, the allowlist lint and its negative controls, the encode plan (relative names only), refusals,
#            phone_check.py --selftest (mechanisms only: no assertion about FontSize=23) and the phone style over every script that has strings
#   --all    everything in --quick plus the heavy steps: the synthetic ProRes master (the WP-04 harness, inside lj_with_disk 150), the encodes (encode_phone.sh, inside lj_with_disk 100),
#            spec_check.py and colour_patch.py on the phone chains, the sharing simulation, the fill_20x9 check (the phone style passes, a clip burned with the venue margin fails), the
#            FontSize=23 finding, the candidate sizes, the shaping paths, PHONE-ROW.md, public_lint.py. Writes the evidence files named in the build plan to build/evidence/wp08/.
#   --list   print the tests and the set each belongs to
#   --keep   (with --all) keep the 120 MB master and the encoded files under renders/wp08/ for the individual acceptance commands (the default removes the master)
#
# One line per test: PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED name detail. Exit 0 if no line is FAIL or BLOCKED, 1 if a line FAILs, 3 if the disk guard blocked a heavy step.
# Evidence: one lj-evidence/1 envelope per test in build/evidence/wp08/tests_quick.jsonl or tests_all.jsonl. Work files go under renders/wp08/ (git-ignored) and the big ones are removed at the end.
set -u
cd "$(dirname "$0")/../.." || exit 3
MODE="${1:---quick}"
ONLY=""
KEEP=0
case "$MODE" in
  --quick|--all|--list) ;;
  *) echo "usage: bash tests/phone/run_tests.sh [--quick|--all|--list] [--only name,name] [--keep]" >&2; exit 2 ;;
esac
shift
while [ "$#" -gt 0 ]; do
  case "$1" in
    --only) ONLY="${2:-}"; shift;;
    --keep) KEEP=1;;
    *) echo "usage: bash tests/phone/run_tests.sh [--quick|--all|--list] [--only name,name] [--keep]" >&2; exit 2;;
  esac
  shift
done
for t in python3 ffmpeg ffprobe node; do
  command -v "$t" >/dev/null 2>&1 || { echo "run_tests: $t not found" >&2; exit 3; }
done
if [ "$MODE" = "--list" ]; then
  python3 -I - <<'PY'
import re
src = open("tests/phone/run_checks.py", encoding="utf-8").read()
for m in re.finditer(r'@test\("([^"]+)"(?:, modes=\(([^)]*)\))?\)', src):
    print("%-38s %s" % (m.group(1), "all" if m.group(2) and "quick" not in m.group(2) else "quick + all"))
PY
  exit 0
fi
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
mkdir -p build/evidence/wp08 renders/wp08
ARGS=(--mode "${MODE#--}")
[ -n "$ONLY" ] && ARGS+=(--only "$ONLY")
[ "$KEEP" = 1 ] && ARGS+=(--keep)
exec python3 -I tests/phone/run_checks.py "${ARGS[@]}"
