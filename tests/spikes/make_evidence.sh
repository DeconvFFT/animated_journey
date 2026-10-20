#!/usr/bin/env bash
# tests/spikes/make_evidence.sh: run the WP-10 suite and every acceptance command, and write build/evidence/wp10/{tests_quick.txt,tests_all.txt,acceptance_transcript.txt,summary.json}.
# USAGE  bash tests/spikes/make_evidence.sh        (about 4 minutes; downloads nothing: a stage that already ran is not run again)
# Writes only under build/evidence/wp10/. The console output is passed through a scrubber that replaces the repository and scratch paths, so the files hold no absolute path.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCR="${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
EV="$ROOT/build/evidence/wp10"
cd "$ROOT" || exit 3
scrub() { sed -e "s#$ROOT#<repo>#g" -e "s#$SCR#<scratch>#g"; }
TR="$EV/acceptance_transcript.txt"
: > "$TR"
say() { printf '%s\n' "$*" | tee -a "$TR" >/dev/null; }
run() {  # run LABEL COMMAND...
  local label="$1"; shift
  say ""; say "\$ $label"
  "$@" 2>&1 | scrub >> "$TR"; local rc=${PIPESTATUS[0]}
  say "[exit $rc]"
  return 0
}
say "WP-10 acceptance transcript. Date $(date -u +%Y-%m-%d). Every Craft result is a Linux CLI result; not evidence for Windows."
say "df at start: Avail $(df -BM / | awk 'NR==2{print $4}')"
bash tests/spikes/run_tests.sh --quick 2>&1 | scrub > "$EV/tests_quick.txt"; rcq=${PIPESTATUS[0]}
bash tests/spikes/run_tests.sh --all 2>&1 | scrub > "$EV/tests_all.txt"; rca=${PIPESTATUS[0]}
say ""; say "\$ bash tests/spikes/run_tests.sh --quick   [exit $rcq; output in tests_quick.txt]"; tail -1 "$EV/tests_quick.txt" >> "$TR"
say ""; say "\$ bash tests/spikes/run_tests.sh --all   [exit $rca; output in tests_all.txt]"; tail -1 "$EV/tests_all.txt" >> "$TR"
run "bash spikes/sp1b_readback/run_sp1b.sh --list" bash spikes/sp1b_readback/run_sp1b.sh --list
run "bash spikes/sp1b_readback/run_sp1b.sh --all   (every stage already ran, so nothing is downloaded)" bash spikes/sp1b_readback/run_sp1b.sh --all
run "python3 -I spikes/sp1b_readback/check_ledger.py" python3 -I spikes/sp1b_readback/check_ledger.py
run "bash spikes/sp3_blender/run_sp3.sh --check" bash spikes/sp3_blender/run_sp3.sh --check
run "python3 -m py_compile research/production-scale-fixtures/followup2-s3-kitchen-standin.py" python3 -m py_compile research/production-scale-fixtures/followup2-s3-kitchen-standin.py
rm -rf research/production-scale-fixtures/__pycache__
L="$SCR/sp4/acceptance-$(date -u +%H%M%S).log"
say ""; say "\$ bash spikes/sp4_idle/job.sh --seconds 60 --interval 2 && python3 -I spikes/sp4_idle/gaps.py <log>"
bash spikes/sp4_idle/job.sh --seconds 60 --interval 2 --out "$L" 2>&1 | scrub >> "$TR"; rc1=${PIPESTATUS[0]}
python3 -I spikes/sp4_idle/gaps.py "$L" --json "$EV/sp4_job_60s_gaps.json" 2>&1 | scrub >> "$TR"; rc2=${PIPESTATUS[0]}
say "[exit job.sh $rc1, gaps.py $rc2]"; rm -f "$L"
run "python3 -I spikes/sp4_idle/gaps.py tests/spikes/fixtures/log_with_5min_gap.txt" python3 -I spikes/sp4_idle/gaps.py tests/spikes/fixtures/log_with_5min_gap.txt
run "python3 -I tests/spikes/check_verdicts.py" python3 -I tests/spikes/check_verdicts.py
say ""; say "\$ after SP1b: ls -A vendor/craft-sp1b ; ls vendor/craft/_keep ; lowest avail_mb_min in the stage envelopes"
say "vendor/craft-sp1b holds: $(ls -A vendor/craft-sp1b 2>/dev/null | tr '\n' ' ')(nothing if blank)"
say "vendor/craft/_keep: $([ -e vendor/craft/_keep ] && echo present || echo gone)"
python3 -I - >> "$TR" <<'PY'
import glob, json
rows = []
for f in sorted(glob.glob("build/evidence/wp10/stage_*.json")):
    d = json.load(open(f)); k = d["disk"]
    rows.append((f.split("stage_")[1][:-5], d["status"], k["avail_mb_start"], k["avail_mb_min"], k["avail_mb_end"], k["planned_write_mb"]))
for r in rows: print("  stage %-20s %-10s Avail start %s, min %s, end %s MB, planned %s MB" % r)
print("  lowest avail_mb_min: %s MB (the hard floor is 250)" % min(r[3] for r in rows if isinstance(r[3], int)))
PY
python3 -I - "$EV" <<'PY'
import glob, json, os, sys
ev = sys.argv[1]
def counts(path):
    c = {}
    if os.path.exists(path):
        for ln in open(path):
            if ln.strip():
                s = json.loads(ln)["status"]; c[s] = c.get(s, 0) + 1
    return c
out = {"schema": "lj-evidence-summary/1", "package": "WP-10", "quick_run": counts(os.path.join(ev, "tests_quick.jsonl")), "all_run": counts(os.path.join(ev, "tests.jsonl")),
       "stages": {os.path.basename(f)[6:-5]: json.load(open(f))["status"] for f in sorted(glob.glob(os.path.join(ev, "stage_*.json")))},
       "label": "Linux CLI result; not evidence for Windows"}
json.dump(out, open(os.path.join(ev, "summary.json"), "w"), indent=2, sort_keys=True)
print(json.dumps(out))
PY
exit 0
