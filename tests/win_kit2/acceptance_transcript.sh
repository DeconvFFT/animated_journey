#!/usr/bin/env bash
# tests/win_kit2/acceptance_transcript.sh: run the WP-09 acceptance commands of the build plan, in order, and print the real output.
#   bash tests/win_kit2/acceptance_transcript.sh > build/evidence/wp09/acceptance_transcript.txt
# Absolute paths are masked (the repository folder becomes ".", the scratch folder "<scratch>", /tmp paths "<tmp>"). About 4 minutes.
# Everything it writes goes to renders/wp09/ (git-ignored). Synthetic material only.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 3
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
PW="${PWSH:-$SCRATCH/pwsh/pwsh}"
FAKE="zorb""alex"
RW=renders/wp09
mask() { sed -e "s|$ROOT|.|g" -e "s|$SCRATCH|<scratch>|g" -e "s|$FAKE|<invented-user>|g" -e 's|/tmp/[^ "'"'"']*|<tmp>|g'; }
run() { echo; echo "\$ $*" | mask; "$@" 2>&1 | mask; echo "[exit ${PIPESTATUS[0]}]"; }
runsh() { echo; echo "\$ $1" | mask; bash -c "$1" 2>&1 | mask; echo "[exit ${PIPESTATUS[0]}]"; }
echo "WP-09 acceptance transcript, $(date -u +%Y-%m-%d). ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}'), pwsh $($PW -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'), python $(python3 --version | awk '{print $2}')."
echo "Container: Linux. Nothing here ran on Windows: every Windows claim is UNVERIFIED."
echo
echo "## 1. lint and parse"
runsh "python3 -I win/tools/ps_lint.py win/kit2/*.ps1 && bash win/tools/ps_parse.sh | tail -4"
echo
echo "## 2. Ken Burns self-test, spec_check, MO8 gate (sub-pixel push passes; the zoompan proof fails, as documented)"
rm -f $RW/ex02*
run python3 -I win/kit2/kenburns_24.py --selftest --out $RW/ex02.mp4
run ffprobe -v error -show_entries "stream=width,height,r_frame_rate,codec_name" -of csv=p=0 -select_streams v:0 $RW/ex02.mp4
run python3 -I pipeline/validators/spec_check.py $RW/ex02.mp4 --profile online_h264
run python3 -I pipeline/validators/mo8_gate.py $RW/ex02_push_only.mkv
run python3 -I pipeline/validators/mo8_gate.py $RW/ex02_push_only_zoompan.mkv
run python3 -I -B tests/win_kit2/dissolve_check.py $RW/ex02.mp4
echo
echo "## 3. archive_init, archive_verify, the one-byte tamper test"
rm -rf $RW/standin
run $PW -NoProfile -File win/kit2/archive_init.ps1 -Root $RW/standin -Count 5
run $PW -NoProfile -File win/kit2/archive_verify.ps1 -Root $RW/standin
cp $RW/standin/01_masters/LJ-ST-0003-F.tif /tmp/lj_wp09_orig3.tif
python3 -I -B tests/win_kit2/fixtures.py tamper $RW/standin/01_masters/LJ-ST-0003-F.tif 5000
echo; echo "(one bit of one byte of LJ-ST-0003-F.tif flipped)"
run $PW -NoProfile -File win/kit2/archive_verify.ps1 -Root $RW/standin
cp /tmp/lj_wp09_orig3.tif $RW/standin/01_masters/LJ-ST-0003-F.tif; rm -f /tmp/lj_wp09_orig3.tif
echo; echo "(file restored)"
run $PW -NoProfile -File win/kit2/archive_verify.ps1 -Root $RW/standin
echo
echo "## 4. run_checks_pc.ps1: pattern self-test, planted refusal, clean fixture, derive, public_lint"
run python3 -I -B tests/win_kit2/fixtures.py samples $RW/samples.json
runsh "$PW -NoProfile -File win/kit2/run_checks_pc.ps1 -PatternSelfTest $RW/samples.json 2>/dev/null | head -c 260; echo ' ...'"
run python3 -I scripts/public_lint.py --self-test
python3 -I -B tests/win_kit2/fixtures.py raw-clean $RW/cp_raw_clean.json
python3 -I -B tests/win_kit2/fixtures.py raw-planted path $RW/cp_raw_path.json --fake-user "$FAKE"
rm -f $RW/cp_out_*.json
run $PW -NoProfile -File win/kit2/run_checks_pc.ps1 -TestFixture $RW/cp_raw_path.json -FakeUser "$FAKE" -FakeComputer fakehost01 -FakeDomain fakedom -Out $RW/cp_out_path.json
runsh "ls $RW/cp_out_path.json 2>&1 | head -1"
run $PW -NoProfile -File win/kit2/run_checks_pc.ps1 -TestFixture $RW/cp_raw_clean.json -FakeUser "$FAKE" -FakeComputer fakehost01 -FakeDomain fakedom -Out $RW/cp_out_clean.json
run python3 -I pipeline/validators/colour_patch.py --derive-from $RW/cp_out_clean.json --out $RW/cp_derived.json
run python3 -I scripts/public_lint.py --paths $RW/cp_derived.json
echo
echo "## 5. run_checks_pc.ps1, real run on this container's ffmpeg (6.1.1)"
mkdir -p /tmp/lj_wp09_realtemp
run env TEMP=/tmp/lj_wp09_realtemp $PW -NoProfile -File win/kit2/run_checks_pc.ps1 -Out $RW/cp_raw_real.json
run python3 -I pipeline/validators/colour_patch.py --derive-from $RW/cp_raw_real.json --out $RW/cp_derived_real.json
run python3 -I scripts/public_lint.py --paths $RW/cp_derived_real.json
rm -rf /tmp/lj_wp09_realtemp
echo
echo "## 6. the refusal in the real flow (a build whose configure line carries a profile path and the user name)"
python3 -I -B tests/win_kit2/fixtures.py fake-ffmpeg /tmp/lj_wp09_fakeff --fake-user "$FAKE" > /dev/null
mkdir -p /tmp/lj_wp09_realtemp2
run env USERNAME="$FAKE" TEMP=/tmp/lj_wp09_realtemp2 $PW -NoProfile -File win/kit2/run_checks_pc.ps1 -Ffmpeg /tmp/lj_wp09_fakeff/ffmpeg -Out $RW/cp_raw_refused.json
runsh "ls $RW/cp_raw_refused.json 2>&1 | head -1; echo temp entries left: \$(ls -A /tmp/lj_wp09_realtemp2 | wc -l)"
rm -rf /tmp/lj_wp09_realtemp2 /tmp/lj_wp09_fakeff
rm -f $RW/ex02_push_only.mkv $RW/ex02_push_only_zoompan.mkv
