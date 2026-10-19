#!/usr/bin/env bash
# acceptance_transcript.sh: runs the WP-11a acceptance commands in order and records their real output in
# build/evidence/wp11a/acceptance_transcript.txt (about 4 minutes; it runs the real --quick, which in turn runs every landed area).
#   bash tests/runner/acceptance_transcript.sh
# Nothing is deleted on the real tree: cleanup_scratch.sh is run there as a dry run only; --yes runs on a fake tree.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO" || exit 3
OUT="$REPO/build/evidence/wp11a/acceptance_transcript.txt"
mkdir -p "$(dirname "$OUT")"
BASE="$(cd "$REPO/.." && pwd)/build-scratch"
T="$(mktemp -d "$BASE/wp11a-acc.XXXXXX")" || exit 3
trap 'rm -rf "$T"' EXIT
exec > >(tee "$T/transcript.txt") 2>&1
step() { printf '\n==== %s ====\n' "$*"; }
snap() {  # names, sizes and times of exactly the things cleanup_scratch.sh would delete
  { find "$BASE/pwsh" "$BASE"/venv* "$REPO"/vendor/craft* "$REPO"/renders/wp* -printf '%P %s %T@\n' 2>/dev/null; } | LC_ALL=C sort | sha256sum | cut -c1-16
}

step "1. bash tests/runner/run_tests.sh --all"
bash tests/runner/run_tests.sh --all; echo "[exit $?]"

step "2. bash scripts/run_week2_checks.sh --list"
bash scripts/run_week2_checks.sh --list; echo "[exit $?]"

step "3. bash scripts/run_week2_checks.sh --quick   (the real tree)"
bash scripts/run_week2_checks.sh --quick; echo "[exit $?]"
echo "files written:"; ls -l build/evidence/INDEX.md build/evidence/week2_summary.json build/evidence/wave1_quick.txt | awk '{print $5, $9}'

step "4. the same runner against the FAKE areas (pass, fail, missing, hang, planted e-mail)"
FK="$T/fk-ev"; mkdir -p "$FK"
LJ_RUNNER_AREAS_FILE=tests/runner/fake_areas.txt LJ_RUNNER_EVIDENCE_DIR="$FK" LJ_RUNNER_TESTS_DIR=tests/runner/fake_tests LJ_RUNNER_TIMEOUT_S=2 \
  LJ_RUNNER_KILL_GRACE_S=1 LJ_SCRATCH="$T/scratch" bash scripts/run_week2_checks.sh --quick; echo "[exit $?]  (1 expected: fk_fail fails and fk_hang times out)"
echo "-- INDEX.md rows (fake)"; grep -E '^\| [0-9]+ \|' "$FK/INDEX.md" | cut -d'|' -f2-7
echo "-- planted strings in the saved files (must be none):"
P1="$(printf '%s%s' 'zz.plan' 'ted')"; P2="$(printf '%s%s' 'alice' '-fake')"
grep -rIl -e "$P1" -e "$P2" "$FK" | wc -l
echo "-- masked form in the area log:"; grep -E 'zz\*|/h\*' "$FK/wp11a/area_fk_email_quick.txt"
echo "-- INDEX.md links that do not exist (must be none):"
grep -E '^\| [0-9]+ \|' "$FK/INDEX.md" | grep -o '](\([^)]*\))' | sed 's/^](//;s/)$//' | while read -r l; do [[ -e "$FK/$l" ]] || echo "MISSING $l"; done
echo "(end of list)"

step "5. bash scripts/cleanup_scratch.sh   (dry run on the real tree; hash of the items it would delete, before and after)"
h0="$(snap)"; bash scripts/cleanup_scratch.sh; echo "[exit $?]"; h1="$(snap)"; echo "hash before: $h0"; echo "hash after:  $h1"
[[ "$h0" == "$h1" ]] && echo "dry run changed nothing" || echo "HASH DIFFERS (another job may have written there; see the report)"

step "6. cleanup_scratch.sh --yes on a FAKE tree, and the refusals"
F="$T/fake"; mkdir -p "$F/home" "$F/build-scratch/pwsh" "$F/build-scratch/venv-otio" "$F/build-scratch/keep" "$F/repo/vendor/craft-x" "$F/repo/vendor/fonts" "$F/repo/renders/wp04" "$F/repo/renders/final"
echo x > "$F/build-scratch/pwsh/a"; echo x > "$F/build-scratch/keep/b"; echo x > "$F/repo/vendor/fonts/c"; echo x > "$F/repo/renders/final/d"
echo "-- --yes on the fake tree"
HOME="$F/home" bash scripts/cleanup_scratch.sh --yes --scratch "$F/build-scratch" --root "$F/repo"; echo "[exit $?]"
echo "-- left in the fake tree (must be keep/b, fonts/c, final/d):"; (cd "$F" && find build-scratch repo -type f | sort)
echo "-- refusals (nothing may change)"
HOME="$F/home" bash scripts/cleanup_scratch.sh --yes --scratch / --root "$F/repo"; echo "[exit $?]"
HOME="$F/home" bash scripts/cleanup_scratch.sh --yes --scratch "$F/home" --root "$F/repo"; echo "[exit $?]  (the fake HOME)"
HOME="$F/home" LJ_SCRATCH="$F/home" bash scripts/cleanup_scratch.sh --yes --root "$F/repo"; echo "[exit $?]  (LJ_SCRATCH is the fake HOME)"

step "7. lint of the owned paths"
python3 -I scripts/public_lint.py --paths scripts/run_week2_checks.sh scripts/cleanup_scratch.sh tests/runner build/evidence/wp11a build/evidence/INDEX.md build/evidence/week2_summary.json build/evidence/wave1_quick.txt; echo "[exit $?]"
sleep 0.5   # let tee finish writing before the copy
cp "$T/transcript.txt" "$OUT"
