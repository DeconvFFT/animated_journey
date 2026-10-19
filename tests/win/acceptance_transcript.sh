#!/usr/bin/env bash
# acceptance_transcript.sh: runs the WP-01a acceptance commands exactly as the build plan lists them and prints
# command, exit code and output. Used to make build/evidence/wp01a/acceptance_transcript.txt for the Fable read.
# Run from the repo root (or set LJ_TEST_TREE to another tree with the same layout; the report says so when used).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${LJ_TEST_TREE:-$ROOT}" || exit 2
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
PWSH="${PWSH:-$SCRATCH/pwsh/pwsh}"
mkdir -p renders/wp01a
show() {  # show "label" command...
  local label="$1"; shift
  echo "---- $label"
  echo "\$ $*"
  "$@" 2>&1 | sed -e "s#$SCRATCH#<scratch>#g"
  echo "exit=${PIPESTATUS[0]}"
}
F=tests/win/fixtures
show "lint step0" python3 -I win/tools/ps_lint.py win/step0_pc_tests.ps1
show "parse script and README fences" bash win/tools/ps_parse.sh
show "Linux dry run (os.platform non-windows)" "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -Out renders/wp01a/linux_report.json
show "checker on the Linux report: NOT A WINDOWS REPORT" python3 -I scripts/windows_check.py renders/wp01a/linux_report.json
for f in gpu12_pro_16gb nogpu_home_8gb software_gpu vram_nvidia_over_cap vram_capped_only ffmpeg9 craft_pins_mixed identifying bom; do
  show "checker: report_$f" python3 -I scripts/windows_check.py $F/report_$f.json
done
show "forbid exampleperson (absent)" python3 -I scripts/windows_check.py --forbid exampleperson $F/report_gpu12_pro_16gb.json
show "forbid zeta, collision" python3 -I scripts/windows_check.py --forbid zeta $F/report_short_username_collision.json
show "forbid zeta, leak" python3 -I scripts/windows_check.py --forbid zeta $F/report_short_username_leak.json
show "version strings that look like IPv4" python3 -I scripts/windows_check.py $F/report_version_strings_not_ip.json
show "64-hex hash" python3 -I scripts/windows_check.py $F/report_sha256_ok.json
show "65-hex leak" python3 -I scripts/windows_check.py $F/report_hex65_leak.json
show "tier file" python3 -I scripts/windows_check.py --tier-json-out renders/wp01a/pc_tier.json $F/report_gpu12_pro_16gb.json
echo "---- renders/wp01a/pc_tier.json"; cat renders/wp01a/pc_tier.json
rm -f renders/wp01a/none.json
show "script self-scan: identifying fixture with invented names" "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $F/report_identifying.json -FakeUser tamsinwrex -FakeComputer BRAMBLE-Q7 -FakeDomain bramblenet -Out renders/wp01a/none.json
echo "renders/wp01a/none.json exists: $( [ -e renders/wp01a/none.json ] && echo yes || echo no )"
show "script self-scan: collision fixture, user zeta" "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $F/report_short_username_collision.json -FakeUser zeta -Out renders/wp01a/collision.json
echo "renders/wp01a/collision.json exists: $( [ -e renders/wp01a/collision.json ] && echo yes || echo no )"
show "script self-scan: leak fixture, user zeta" "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $F/report_short_username_leak.json -FakeUser zeta -Out renders/wp01a/leak.json
echo "renders/wp01a/leak.json exists: $( [ -e renders/wp01a/leak.json ] && echo yes || echo no )"
rm -f renders/wp01a/collision.json renders/wp01a/none.json renders/wp01a/leak.json
