#!/usr/bin/env bash
# make_evidence.sh: regenerates build/evidence/wp01a/ (transcripts the Fable read needs). Run from the repo root.
#   bash tests/win/make_evidence.sh            uses this repo's scripts/redaction_patterns.json
#   LJ_TEST_TREE=<tree> bash tests/win/make_evidence.sh    uses another tree (only while the WP-03 file has not landed)
# Writes: tests_quick.txt, tests_all.txt (+ tests.jsonl, summary.json, unverified.txt from run_tests.sh),
#         acceptance_transcript.txt, tier_gpu12_pro_16gb.json, hardware_gpu12_pro_16gb.md, environment.json
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EV="$ROOT/build/evidence/wp01a"
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
mkdir -p "$EV"
scrub() { sed -e "s#$SCRATCH#<scratch>#g" -e "s#${LJ_TEST_TREE:-__none__}#<alternate-tree>#g" -e "s#$ROOT#.#g" -e 's#/tmp/[^ ]*#<tmp>#g'; }
bash "$ROOT/tests/win/run_tests.sh" --quick 2>&1 | scrub > "$EV/tests_quick.txt"
bash "$ROOT/tests/win/run_tests.sh" --all 2>&1 | scrub > "$EV/tests_all.txt"
bash "$ROOT/tests/win/acceptance_transcript.sh" 2>&1 | scrub > "$EV/acceptance_transcript.txt"
TREE="${LJ_TEST_TREE:-$ROOT}"
( cd "$TREE" && python3 -I scripts/windows_check.py --tier-json-out "$EV/tier_gpu12_pro_16gb.json" --hardware-md "$EV/hardware_gpu12_pro_16gb.md" tests/win/fixtures/report_gpu12_pro_16gb.json > /dev/null )
python3 -I - "$EV" "$TREE" "$ROOT" <<'PYEOF'
import json, os, subprocess, sys, hashlib
ev, tree, root = sys.argv[1:]
pat = os.path.join(tree, "scripts", "redaction_patterns.json")
env = {"schema": "lj-wp01a-environment/1",
       "pattern_file": "repo scripts/redaction_patterns.json" if os.path.abspath(tree) == os.path.abspath(root) else "STAND-IN in an alternate tree (WP-03 file had not landed)",
       "pattern_file_sha256_first12": hashlib.sha256(open(pat, "rb").read()).hexdigest()[:12] if os.path.isfile(pat) else None,
       "pwsh": subprocess.run([os.environ.get("PWSH", "/home/user/build-scratch/pwsh/pwsh"), "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"], capture_output=True, text=True).stdout.strip(),
       "python": sys.version.split()[0]}
json.dump(env, open(os.path.join(ev, "environment.json"), "w"), indent=1)
PYEOF
echo "evidence written to build/evidence/wp01a/"; ls "$EV"
