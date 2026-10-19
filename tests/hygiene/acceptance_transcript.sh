#!/usr/bin/env bash
# acceptance_transcript.sh: runs the WP-03 acceptance commands exactly as the build plan lists them and
# records the real output and exit codes in build/evidence/wp03/acceptance_transcript.txt.
#
# Unlike run_tests.sh this DOES write the deliverables the acceptance list asks for:
#   build/evidence/wp03/stale_check_report.json and .md   (the first stale_check run; exit 1 is expected)
#   scripts/stale_baseline.json                             (today's hits)
#   build/evidence/wp03/LANDED-4.13.txt                     (by the pattern test)
# Everything else is read-only. Run from anywhere:  bash tests/hygiene/acceptance_transcript.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 3
OUT=build/evidence/wp03/acceptance_transcript.txt
mkdir -p build/evidence/wp03
: > "$OUT"
n=0
step() {  # label command...
  local label="$1"; shift
  n=$((n + 1))
  { printf '\n===== [%d] %s\n$ %s\n' "$n" "$label" "$*"; } >> "$OUT"
  local o rc
  o="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$o" | head -n 60 >> "$OUT"
  local lines; lines="$(printf '%s\n' "$o" | wc -l)"
  [[ $lines -gt 60 ]] && printf '... (%d more lines)\n' $((lines - 60)) >> "$OUT"
  printf '[exit %d]\n' "$rc" >> "$OUT"
  LAST_RC=$rc
}
echo "WP-03 acceptance transcript. Paths are repo-relative. Avail at start: $(LC_ALL=C df -BM -P / | awk 'NR==2{print $4}')" >> "$OUT"

step "pattern file is internally consistent (writes LANDED-4.13.txt)" python3 -I tests/hygiene/test_patterns.py
step "guard, stale and lint tests (--all)" bash tests/hygiene/run_tests.sh --all
step "stale_check self-test" python3 -I scripts/stale_check.py --self-test
step "stale_check allowlist audit (no dead entries)" python3 -I scripts/stale_check.py --audit-allowlist
step "stale_check first run: report written, exit 1 expected" python3 -I scripts/stale_check.py --json build/evidence/wp03/stale_check_report.json --md build/evidence/wp03/stale_check_report.md
step "stale_check --baseline then --new-only (exit 0 straight after)" bash -c "python3 -I scripts/stale_check.py --baseline && python3 -I scripts/stale_check.py --new-only"
step "public_lint self-test (4.13 disagreement test)" python3 -I scripts/public_lint.py --self-test
step "public_lint --self-test --fail-on-skip (WP-11b's final form; a skip is a failure)" python3 -I scripts/public_lint.py --self-test --fail-on-skip
step "public_lint on WP-03's own files and evidence" python3 -I scripts/public_lint.py --paths scripts/redaction_patterns.json scripts/lj_guard.sh scripts/stale_check.py scripts/stale_patterns.json scripts/stale_allowlist.json scripts/stale_baseline.json scripts/public_lint.py scripts/public_lint.config.json tests/hygiene build/evidence/wp03
step "public_lint whole-tree audit of the real repository (findings are for the orchestrator, nothing is fixed here)" python3 -I scripts/public_lint.py --all --json build/evidence/wp03/public_lint_all_tree.json
step "public_lint default mode: diff against HEAD plus untracked files" python3 -I scripts/public_lint.py
step "theme guard on the real tree (new or changed theme-bearing files; existing text is INFO only)" python3 -I scripts/public_lint.py --theme
step "disk guard smoke test on the real volume (planned 0 MB, label only)" bash scripts/lj_guard.sh with_disk 0 wp03-smoke -- true
step "bench guard smoke test (nproc and load recorded)" bash scripts/lj_guard.sh bench true
echo "transcript written to $OUT"
