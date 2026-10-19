#!/usr/bin/env bash
# tests/validators/make_evidence.sh [--wait SECONDS] [--unguarded] [--planned-mb N]     WP-05: run everything and file the evidence
#
# Runs run_tests.sh --quick, then run_tests.sh --all (the guarded stage; the options are passed on), then the acceptance commands of
# the work package on their own, and writes build/evidence/wp05/{tests_quick.txt,tests_quick.jsonl,tests_all.txt,tests_all.jsonl,
# acceptance_transcript.txt,summary.json,environment.json,colour_patch_ffmpeg-<version>.derived.json}. Each mode writes its own .jsonl,
# so the --quick run can not overwrite the --all envelopes. Exit code: that of the --all run (0 only if no test failed and the disk
# stage was not blocked).
#
# The RAW colour-patch record (it holds the ffmpeg build's configure flags) is kept in the scratch folder beside the repository
# (LJ_SCRATCH, default ../build-scratch), never in build/evidence: only the derived form is filed.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EV="$ROOT/build/evidence/wp05"
SCR="${LJ_SCRATCH:-$(cd "$ROOT/.." && pwd)/build-scratch}/wp05"
mkdir -p "$EV" "$SCR"
cd "$ROOT" || exit 2
FFV="$(ffmpeg -version 2>/dev/null | awk 'NR==1{print $3}' | sed 's/-.*//')"
RAW="$SCR/colour_patch_ffmpeg-$FFV.raw.json"
bash tests/validators/run_tests.sh --quick 2>&1 | tee "$EV/tests_quick.txt"
bash tests/validators/run_tests.sh --all "$@" 2>&1 | tee "$EV/tests_all.txt"
RC="${PIPESTATUS[0]}"
{
  echo "# WP-05 acceptance commands, run on their own (the same commands run_tests.sh --all runs inside its stage)"
  echo "# The raw record goes to <scratch> (it holds build flags); only the derived form is filed."
  echo
  echo "\$ python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json <scratch>/wp05/colour_patch_ffmpeg-$FFV.raw.json"
  python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json "$RAW"; echo "exit=$?"
  echo
  echo "\$ python3 -I pipeline/validators/colour_patch.py --derive-from <scratch>/wp05/colour_patch_ffmpeg-$FFV.raw.json --out build/evidence/wp05/colour_patch_ffmpeg-$FFV.derived.json"
  python3 -I pipeline/validators/colour_patch.py --derive-from "$RAW" --out "$EV/colour_patch_ffmpeg-$FFV.derived.json"; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080 --chain phone_720_share   # WP-08 acceptance line; the 1280x720 chain is read at its own size'
  python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080 --chain phone_720_share; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/colour_patch.py --selftest'
  python3 -I pipeline/validators/colour_patch.py --selftest; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/spec_check.py --selftest'
  python3 -I pipeline/validators/spec_check.py --selftest; echo "exit=$?"
  echo
  echo '$ python3 -I pipeline/validators/spec_check.py --list-profiles'
  python3 -I pipeline/validators/spec_check.py --list-profiles; echo "exit=$?"
} > "$EV/acceptance_transcript.txt" 2>&1
python3 -I tests/validators/make_evidence.py
exit "$RC"
