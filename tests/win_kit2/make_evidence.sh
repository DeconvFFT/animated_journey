#!/usr/bin/env bash
# tests/win_kit2/make_evidence.sh: regenerate build/evidence/wp09/ (about 8 minutes).
#   quick run, all run, the acceptance transcript, the derived colour-patch file of the container run, environment and unverified lists.
# The raw colour-patch record of the container run stays in renders/wp09/ (git-ignored); only the derived form is copied here (build plan 4.16).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 3
EVID=build/evidence/wp09
mkdir -p "$EVID"
bash tests/win_kit2/run_tests.sh --quick > "$EVID/tests_quick.txt" 2>&1; echo "quick exit $?"
LJ_KEEP_RENDERS=1 bash tests/win_kit2/run_tests.sh --all > "$EVID/tests_all.txt" 2>&1; echo "all exit $?"
bash tests/win_kit2/acceptance_transcript.sh > "$EVID/acceptance_transcript.txt" 2>&1; echo "transcript exit $?"
python3 -I -B - <<'PYEOF'
import json, os, platform, subprocess
def first(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]
    except Exception:
        return "unknown"
env = {"platform": "linux", "python": platform.python_version(), "ffmpeg": first(["ffmpeg", "-version"]), "ffprobe": first(["ffprobe", "-version"]),
       "pwsh": first(["/home/user/build-scratch/pwsh/pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]),
       "nproc": os.cpu_count(), "machine": platform.machine()}
json.dump(env, open("build/evidence/wp09/environment.json", "w"), indent=2)
PYEOF
python3 -I -B - <<'PYEOF'
import json
out = {"schema": "lj-wp09-summary/1", "package": "WP-09"}
for m in ("quick", "all"):
    try:
        out[m] = json.load(open("build/evidence/wp09/summary_%s.json" % m))
    except (OSError, ValueError):
        out[m] = None
json.dump(out, open("build/evidence/wp09/summary.json", "w"), indent=2)
PYEOF
if [ -f renders/wp09/cp_derived_real.json ]; then cp renders/wp09/cp_derived_real.json "$EVID/run_checks_pc_container.derived.json"; fi
rm -f renders/wp09/ex02_push_only.mkv renders/wp09/ex02_push_only_zoompan.mkv
python3 -I scripts/public_lint.py --paths win/kit2 tests/win_kit2 "$EVID" | tail -2
