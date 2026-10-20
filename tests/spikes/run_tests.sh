#!/usr/bin/env bash
# tests/spikes/run_tests.sh [--quick|--all]    WP-10: SP1b (PhotoCraft, VectorCraft, LightCraft T1 and read-backs; FilmCraft T3), SP3 prepared, SP4 armed, the spike verdict table
#
#   --quick  (at most 60 s, no downloads, no timed runs): syntax, the library and driver self-tests, `run_sp1b.sh --list` (live and with fake df lines), the stage budget arithmetic, the
#            ledger check (the real ledgers and planted ones), `run_sp3.sh --check` (live, READY with a fake df, the dry run, the refusal), the py_compile of the reused research script,
#            a 6 s SP4 job and `gaps.py` on the synthetic logs, `check_verdicts.py`, the evidence labels and disk figures, the hygiene after SP1b, the public-repo lint.
#   --all    everything in --quick, plus
#            the 60 s SP4 acceptance run (job.sh --seconds 60 --interval 2, then gaps.py: exit 0), the real `run_sp1b.sh --all` (re-runnable: a stage that already ran is not run again, so it
#            downloads nothing a second time; if a stage was never run and the guard allows it, it runs it, once), and the MECHANISM tests: the same run_sp1b.sh against a local fake release
#            server and stand-in CLIs (tiny, fake df): three full stages, a rerun that downloads nothing and a --again that records its exception, planted defects (each makes exactly its own
#            criterion FAIL), the guard's refusal (BLOCKED, the exact message, no download), --all with everything refused (exit 3), a blocked download (blocked_proof.json), a hash mismatch
#            (stop and report), the disk-floor abort that cleans up, the exact need after the download (BLOCKED, tarball deleted), and the FilmCraft stage's rules (a harness problem keeps the kept
#            tarball; a corrupt kept tarball is replaced with a recorded exception; a missing one is re-fetched once with a recorded exception). The stand-ins are not Craft apps and prove nothing about them.
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail.  Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line is BLOCKED.
# Every line also writes an evidence envelope (build plan 4.2) to build/evidence/wp10/tests.jsonl (--all) or tests_quick.jsonl (--quick); each mode has its own lock and file, because another
# runner (WP-11a's run_week2_checks.sh) may call --quick while an --all is running. Writes only under build/evidence/wp10/, vendor/craft-sp1b/ (the real stages) and a scratch folder it removes again.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
MODE=--quick
while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick|--all) MODE="$1";;
    *) echo "usage: run_tests.sh [--quick|--all]" >&2; exit 2;;
  esac
  shift
done
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SP="$ROOT/spikes/sp1b_readback"; DRV="$SP/drivers"; T="$ROOT/tests/spikes"; FX="$T/fixtures"
EVID="$ROOT/build/evidence/wp10"
SCRATCH_ROOT="${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
mkdir -p "$EVID" "$SCRATCH_ROOT"
JSONL="$EVID/tests.jsonl"; [ "$MODE" = "--quick" ] && JSONL="$EVID/tests_quick.jsonl"
exec 9>"$SCRATCH_ROOT/wp10-tests-${MODE#--}.lock"; flock -w 1800 9 || { echo "BUSY: another run_tests.sh $MODE holds the lock"; exit 3; }
: > "$JSONL"
WORK="$(mktemp -d "$SCRATCH_ROOT/wp10-tests.XXXXXX")"
SRV_PIDS=""
cleanup() { for p in $SRV_PIDS; do kill "$p" 2>/dev/null; done; rm -rf "$WORK"; }
trap cleanup EXIT
FAILS=0; BLOCKED=0; UNV=0; NPASS=0
rec() {  # STATUS NAME DETAIL [EXPECTED]
  local st="$1" name="$2" detail="$3" exp="${4:-the check passes}"
  printf '%-10s %s  %s\n' "$st" "$name" "$detail" | cut -c1-900
  local extra=(); [ "$st" = UNVERIFIED ] && extra=(--unverified "see the detail")
  python3 -I "$T/record.py" "$st" "$name" "$exp" "$detail" "${extra[@]}" --out "$JSONL" >/dev/null 2>&1
  case "$st" in FAIL) FAILS=$((FAILS + 1));; BLOCKED) BLOCKED=$((BLOCKED + 1));; UNVERIFIED) UNV=$((UNV + 1));; PASS) NPASS=$((NPASS + 1));; esac
}
LAST_OUT=""
check() {
  local name="$1" cond="$2" detail="$3" exp="${4:-}"
  if [ "$cond" = 1 ]; then rec PASS "$name" "$detail" "$exp"
  else
    rec FAIL "$name" "$detail" "$exp"
    [ -n "$LAST_OUT" ] && tail -n 8 <<<"$LAST_OUT" | sed -e 's/^/    | /' | cut -c1-240
  fi
  LAST_OUT=""
}
df_mb() { df -BM -P / | awk 'NR==2{gsub("M","",$4); print $4}'; }
fakedf() {  # fakedf N -> path of a script that reports N MB available
  local f="$WORK/fake_df_$1.sh"
  if [ ! -f "$f" ]; then printf '#!/usr/bin/env bash\nprintf "Filesystem     1M-blocks  Used Available Use%%%% Mounted on\\n"\nprintf "fake           258020M 250000M %%5sM  100%%%% /\\n" "%s"\n' "$1" > "$f"; chmod +x "$f"; fi
  echo "$f"
}
jqe() { jq -r "$1" "$2" 2>/dev/null; }

echo "tests/spikes/run_tests.sh $MODE   (df now: Avail $(df -BM / | awk 'NR==2{print $4}'))"

# ------------------------------------------------------------------ QUICK
bad=""; for f in "$SP/run_sp1b.sh" "$ROOT/spikes/sp3_blender/run_sp3.sh" "$ROOT/spikes/sp4_idle/job.sh" "$T/run_tests.sh"; do bash -n "$f" 2>/dev/null || bad="$bad $(basename "$f")"; done
check syntax.bash "$([ -z "$bad" ] && echo 1 || echo 0)" "bash -n on run_sp1b.sh, run_sp3.sh, job.sh and run_tests.sh; failing:${bad:- none}" "every shell script parses"
bad=""; for f in $(find "$SP" "$ROOT/spikes/sp4_idle" "$T" \( -name '*.py' -o -name '*-cli' \) | sort); do python3 -I -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" 2>/dev/null || bad="$bad $(basename "$f")"; done
check syntax.python "$([ -z "$bad" ] && echo 1 || echo 0)" "ast.parse on every .py file and the four stand-in CLIs; failing:${bad:- none}" "every Python file parses"
out="$(python3 -I "$DRV/sp1b_lib.py" --selftest 2>&1)"; rc=$?
check lib.selftest "$([ $rc = 0 ] && echo 1 || echo 0)" "sp1b_lib --selftest: $(grep -c '^PASS' <<<"$out") PASS, $(grep -c '^FAIL' <<<"$out") FAIL (synthetic inputs build, layer-name reading)" "the helpers behave"
out="$(python3 -I "$ROOT/spikes/sp1_craft_cli/drivers/sp1_lib.py" --selftest 2>&1)"; rc=$?
check lib.reused_sp1_lib_selftest "$([ $rc = 0 ] && echo 1 || echo 0)" "the reused WP-07 library: $(grep -c '^PASS' <<<"$out") PASS, $(grep -c '^FAIL' <<<"$out") FAIL" "the scrubber and the df parser behave"
out="$(python3 -I "$DRV/t3_filmcraft.py" --selftest 2>&1)"; rc=$?
check t3.selftest "$([ $rc = 0 ] && echo 1 || echo 0)" "t3_filmcraft --selftest: $(grep -c '^PASS' <<<"$out") PASS, $(grep -c '^FAIL' <<<"$out") FAIL (planted differences in clips, frames, dissolves and keyframes are found)" "the comparison functions have teeth"

# --list: live, and with fake df lines (the FilmCraft tarball WP-07 kept may or may not be on disk, so the fake runs use an empty hand-off folder)
out="$(bash "$SP/run_sp1b.sh" --list 2>&1)"; rc=$?
want=$(grep -q 'REFUSED' <<<"$out" && echo 3 || echo 0)
check list.live "$([ "$rc" = "$want" ] && grep -q 'Stages, in this order' <<<"$out" && grep -q 'photocraft' <<<"$out" && grep -q '83,037,328 bytes' <<<"$out" && echo 1 || echo 0)" "exit $rc (expected $want: exit 3 exactly when a stage's Avail minus planned is under 400 MB); $(grep -E '^(OK|Disk:)' <<<"$out" | head -1 | cut -c1-160)" "--list prints sizes, df and the stage plan, and refuses (exit 3) for a stage that does not fit"
mkdir -p "$WORK/keep_empty" "$WORK/ev_fresh"
out="$(LJ_SP1_EVIDENCE="$WORK/ev_fresh" LJ_SP1B_KEEP_DIR="$WORK/keep_empty" LJ_DF_CMD="$(fakedf 650)" bash "$SP/run_sp1b.sh" --list 2>&1)"; rc=$?
check list.fake_650 "$([ $rc = 3 ] && grep -q 'REFUSED: Avail 650 MB minus planned 286 MB leaves 364 MB, below the 400 MB floor (vectorcraft-v0.13.1).' <<<"$out" && grep -q 'REFUSED: Avail 650 MB minus planned 254 MB leaves 396 MB, below the 400 MB floor (lightcraft-v0.9.1).' <<<"$out" && ! grep -q 'photocraft-v0.10.0).' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E '^REFUSED' <<<"$out" | tr '\n' ' ' | cut -c1-300)" "at a fake 650 MB VectorCraft and LightCraft are refused with the exact message, PhotoCraft fits, exit 3"
LAST_OUT="$out"
out="$(LJ_SP1_EVIDENCE="$WORK/ev_fresh" LJ_SP1B_KEEP_DIR="$WORK/keep_empty" LJ_DF_CMD="$(fakedf 2000)" bash "$SP/run_sp1b.sh" --list 2>&1)"; rc=$?
check list.fake_2000 "$([ $rc = 0 ] && ! grep -q 'REFUSED' <<<"$out" && grep -q '^OK: every stage that has not run yet fits' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E '^OK' <<<"$out" | cut -c1-120)" "at a fake 2000 MB every stage fits, exit 0"
out="$(LJ_SP1_EVIDENCE="$WORK/ev_fresh" LJ_SP1B_KEEP_DIR="$WORK/keep_empty" LJ_DF_CMD="$(fakedf 450)" bash "$SP/run_sp1b.sh" --list 2>&1)"; rc=$?
check list.fake_450 "$([ $rc = 3 ] && [ "$(grep -c '^REFUSED' <<<"$out")" = 4 ] && grep -q '^Remedy: answer Q-1' <<<"$out" && grep -q 'move this read-back to the maker.s PC' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -c '^REFUSED' <<<"$out") REFUSED lines; remedy: $(grep -E '^Remedy' <<<"$out" | cut -c1-160)" "at a fake 450 MB all four stages are refused, with the remedy (Q-1 or the maker's PC)"
out="$(LJ_DF_CMD="$(fakedf 450)" bash "$SP/run_sp1b.sh" --list 2>&1)"; rc=$?
nran=$(grep -c 'already run: ' <<<"$out")
check list.ran_stages_not_counted "$([ "$nran" = "$(ls "$EVID"/stage_*.json 2>/dev/null | wc -l)" ] && { [ "$nran" = 0 ] || ! grep -q '^REFUSED' <<<"$out"; } && echo 1 || echo 0)" "$nran stage(s) shown as already run and not counted against the disk (a fake 450 MB would refuse them if they were); exit $rc" "--list does not plan a stage that already ran"
out="$(python3 -I "$DRV/stage_budget.py" budget photocraft; python3 -I "$DRV/stage_budget.py" budget vectorcraft; python3 -I "$DRV/stage_budget.py" budget lightcraft)"
p1=$(jq -r '.planned_mb' <<<"$(sed -n 1p <<<"$out")"); p2=$(jq -r '.planned_mb' <<<"$(sed -n 2p <<<"$out")"); p3=$(jq -r '.planned_mb' <<<"$(sed -n 3p <<<"$out")")
check budget.numbers "$([ "$p1" = 202 ] && [ "$p2" = 286 ] && [ "$p3" = 254 ] && echo 1 || echo 0)" "planned MB: PhotoCraft $p1 (80 tarball + 92 CLI + 30), VectorCraft $p2 (119 + 137 + 30), LightCraft $p3 (104 + 120 + 30); the plan table's estimates were 300, 450, 350" "the planned figure is computed from the tarball size in release_assets.json, not guessed"
printf -- '-rwxr-xr-x u/g 95000000 2026-10-18 02:56 app-1/bin/app-cli\n-rwxr-xr-x u/g 140000000 2026-10-18 02:56 app-1/bin/app\n-rw-r--r-- u/g 100 2026-10-18 02:56 app-1/share/x\n' > "$WORK/listing.txt"
a="$(python3 -I "$DRV/stage_budget.py" plan "$WORK/listing.txt" app)"; b1="$(python3 -I "$DRV/stage_budget.py" after-download "$WORK/listing.txt" app 700)"; b2="$(python3 -I "$DRV/stage_budget.py" after-download "$WORK/listing.txt" app 500)"
check budget.after_download "$([ "$(jq -r '.chosen|length' <<<"$a")" = 1 ] && [ "$(jq -r '.cli_member' <<<"$a")" = app-1/bin/app-cli ] && [ "$(jq -r '.ok' <<<"$b1")" = true ] && [ "$(jq -r '.ok' <<<"$b2")" = false ] && echo 1 || echo 0)" "plan picks only the CLI member ($(jq -r '.cli_mb' <<<"$a") MB); the exact need ($(jq -r '.need_mb' <<<"$b1") MB) fits at 700 MB and does not at 500 MB" "extract only the one member; the exact need is checked against live Avail after the download"

# the ledger
out="$(python3 -I "$SP/check_ledger.py" 2>&1)"; rc=$?
check ledger.real "$([ $rc = 0 ] && grep -q 'each fetched once or with a recorded exception: OK' <<<"$out" && echo 1 || echo 0)" "$(head -1 <<<"$out" | cut -c1-260)" "each of the five tarballs fetched once; any exception listed with its reason"
LAST_OUT="$out"
L="$WORK/ledger"; mkdir -p "$L/wp10" "$L/wp07" "$L/scratch"
row() { printf '{"app":"%s","asset":"%s-%s-linux-x86_64.tar.gz","bytes":%s,"date_utc":"2026-10-19","exception":"%s","fetch":%s,"sha256":"x","stage":"%s","tag":"v1"}\n' "$1" "$1" "$2" "$3" "$4" "$5" "$6"; }
row photocraft 0.10.0 83037328 "" 1 s1 > "$L/wp10/download_ledger.jsonl"; row photocraft 0.10.0 83037328 "" 2 s2 >> "$L/wp10/download_ledger.jsonl"
out="$(python3 -I "$SP/check_ledger.py" --wp10 "$L/wp10/download_ledger.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$L/wp10" 2>&1)"; rc=$?
check ledger.planted_double_fetch "$([ $rc = 1 ] && grep -q 'photocraft-0.10.0-linux-x86_64.tar.gz was fetched 2 times and a later fetch has no recorded exception' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(head -1 <<<"$out" | cut -c1-200)" "a second fetch without an exception is a problem (exit 1)"
row photocraft 0.10.0 83037328 "" 1 s1 > "$L/wp10/download_ledger.jsonl"; row photocraft 0.10.0 83037328 "re-fetch: test reason" 2 s2 >> "$L/wp10/download_ledger.jsonl"
out="$(python3 -I "$SP/check_ledger.py" --wp10 "$L/wp10/download_ledger.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$L/wp10" 2>&1)"; rc=$?
check ledger.planted_exception_listed "$([ $rc = 0 ] && grep -q '^exceptions: .*test reason' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep '^exceptions' <<<"$out" | cut -c1-200)" "a second fetch with a recorded exception passes and the reason is printed"
out="$(python3 -I "$SP/check_ledger.py" --require-all --wp10 "$L/wp10/download_ledger.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$L/wp10" 2>&1)"; rc=$?
check ledger.require_all "$([ $rc = 1 ] && grep -q 'was not fetched (--require-all)' <<<"$out" && echo 1 || echo 0)" "exit $rc" "--require-all makes an unfetched tarball a failure"
printf '{"app":"soundcraft","asset":"soundcraft-0.8.0-linux-x86_64.tar.gz","bytes":16384149,"date_utc":"2026-10-19","exception":"","fetch":1,"stage":"s9","tag":"v0.8.0"}\n' > "$L/wp10/download_ledger.jsonl"
out="$(python3 -I "$SP/check_ledger.py" --wp10 "$L/wp10/download_ledger.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$L/wp10" 2>&1)"; rc=$?
check ledger.planted_soundcraft "$([ $rc = 1 ] && grep -q 'SoundCraft tarball was fetched' <<<"$out" && echo 1 || echo 0)" "exit $rc" "a SoundCraft fetch is a problem (T5 is cut, D-12)"
: > "$L/wp10/download_ledger.jsonl"; printf '{"schema":"lj-evidence/1","status":"PASS","detail":{"stage":"lightcraft-v0.9.1","fetched":true}}\n' > "$L/wp10/stage_lightcraft-v0.9.1.json"
out="$(python3 -I "$SP/check_ledger.py" --wp10 "$L/wp10/download_ledger.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$L/wp10" 2>&1)"; rc=$?
check ledger.planted_fetch_not_recorded "$([ $rc = 1 ] && grep -q 'says it fetched, but no ledger holds the fetch' <<<"$out" && echo 1 || echo 0)" "exit $rc" "a stage that says it fetched must have its ledger line"

# SP3
out="$(bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --check 2>&1)"; rc=$?
avail="$(sed -n 's/^  free disk          Avail \([0-9]*\) MB now.*/\1/p' <<<"$out")"
want=$([ "${avail:-0}" -ge 3500 ] && echo 0 || echo 3)
check sp3.check_live "$([ "$rc" = "$want" ] && grep -q '401,697,653 bytes' <<<"$out" && grep -q '383,295,504 bytes' <<<"$out" && ( [ "$want" = 0 ] || grep -q 'NOT RUN: needs >= 3.5 GB free' <<<"$out" ) && echo 1 || echo 0)" "Avail ${avail} MB: exit $rc (expected $want); $(grep -E '^(NOT RUN|READY)' <<<"$out" | cut -c1-120)" "prints df, the wheel size, the tarball size and 'NOT RUN: needs >= 3.5 GB free' (exit 3) when under 3,500 MB"
LAST_OUT="$out"
: > "$WORK/empty_ledger.jsonl"
out="$(LJ_SP3_LEDGER="$WORK/empty_ledger.jsonl" LJ_DF_CMD="$(fakedf 5000)" SP3_DRYRUN=1 bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run 2>&1)"; rc=$?
check sp3.dry_run_ready "$([ $rc = 0 ] && grep -q '^READY: Avail 5000 MB' <<<"$out" && grep -q 'lj_with_disk 3100 sp3-blender' <<<"$out" && grep -q 'pip install --no-cache-dir --require-hashes -r spikes/sp3_blender/requirements-bpy.txt' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E '^(READY|SP3_DRYRUN)' <<<"$out" | tr '\n' ' ' | cut -c1-240)" "with enough (fake) room the dry run prints the stage it would run and does none of it"
LAST_OUT="$out"
out="$(LJ_DF_CMD="$(fakedf 3499)" bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run 2>&1)"; rc=$?
check sp3.run_refused_under_3500 "$([ $rc = 3 ] && grep -q 'NOT RUN: needs >= 3.5 GB free (Avail 3499 MB; short by 1 MB)' <<<"$out" && grep -q 'Nothing was started and nothing was forced' <<<"$out" && [ ! -d "$SCRATCH_ROOT/sp3" ] && echo 1 || echo 0)" "exit $rc; $(grep -E '^NOT RUN' <<<"$out" | cut -c1-120)" "--run at 3,499 MB is refused (exit 3), nothing started, no scratch folder made"
cf="$WORK/kitchen.pyc"
python3 -c "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)" "$ROOT/research/production-scale-fixtures/followup2-s3-kitchen-standin.py" "$cf" 2>/dev/null; rc=$?
check sp3.py_compile "$([ $rc = 0 ] && echo 1 || echo 0)" "py_compile of research/production-scale-fixtures/followup2-s3-kitchen-standin.py (reused, not copied; the acceptance line python3 -m py_compile gives the same answer)" "the reused scene script parses"
bash -n "$ROOT/research/production-scale-fixtures/followup2-s3-run-sweep.sh" 2>/dev/null; rc=$?
check sp3.sweep_referenced "$([ $rc = 0 ] && ! grep -q 'run_sp3.*followup2-s3-run-sweep.sh --run' "$ROOT/spikes/sp3_blender/run_sp3.sh" && echo 1 || echo 0)" "followup2-s3-run-sweep.sh parses (bash -n) and is referenced, not executed" "the stale sweep script is documented, not run"

# SP3: the cleanup regression (test_cleanup.sh: run_inner runs to its end against a stand-in python; PASS means exit 0, the work folder gone, no "unbound variable"). It needs no disk and no network; it also catches a
# clean run that ends with a non-zero status, which the edit of 20 Oct (the hash-pinned install and the ledger row) once did.
out="$(bash "$ROOT/spikes/sp3_blender/test_cleanup.sh" 2>&1)"; rc=$?
check sp3.cleanup_regression "$([ $rc = 0 ] && grep -q '^PASS: the work folder is removed' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(head -1 <<<"$out" | cut -c1-160)" "run_sp3.sh --run-inner removes its work folder and exits 0 when it runs to the end"
LAST_OUT="$out"
# SP3: the pip install is hash-pinned and its fetches are on the download ledger (gate w2, nudge 6; SP3 review nudge 1)
out="$(python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" check 2>&1)"; rc=$?
check sp3.requirements_pinned "$([ $rc = 0 ] && grep -q '12 pinned requirements, --require-hashes line present' <<<"$out" && grep -q '12 compared with the pip report' <<<"$out" && grep -q 'OK$' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(cut -c1-230 <<<"$out")" "requirements-bpy.txt: the --require-hashes line, 12 requirements pinned with == and one sha256 each, the same names, versions, files and digests as the pip report of 20 Oct 2026"
LAST_OUT="$out"
R="$ROOT/spikes/sp3_blender/requirements-bpy.txt"
sed 's/6ffa07666f8da0eef81d149934a626d0d95fbd6838432a33e66245423a9062c0/6ffa07666f8da0eef81d149934a626d0d95fbd6838432a33e66245423a9062c1/' "$R" > "$WORK/req_digest.txt"
grep -v '^--require-hashes$' "$R" > "$WORK/req_noflag.txt"
awk '/^numpy==/ { print "numpy==2.5.4"; getline; next } { print }' "$R" > "$WORK/req_nohash.txt"
bad=""
for v in digest noflag nohash; do python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" check --requirements "$WORK/req_$v.txt" >/dev/null 2>&1; [ $? = 1 ] || bad="$bad $v"; done
check sp3.requirements_planted_defects "$([ -z "$bad" ] && echo 1 || echo 0)" "a changed digest, a missing --require-hashes line and a requirement without a hash each make the check exit 1; not caught:${bad:- none}" "each planted defect is refused"
FW="$WORK/pipfake"; mkdir -p "$FW"
python3 -I - "$FW" <<'PY'
import hashlib, sys, zipfile
d = sys.argv[1]
whl = d + "/ljfake-1.0-py3-none-any.whl"
with zipfile.ZipFile(whl, "w") as z:
    z.writestr("ljfake/__init__.py", "X = 1\n")
    z.writestr("ljfake-1.0.dist-info/METADATA", "Metadata-Version: 2.1\nName: ljfake\nVersion: 1.0\n")
    z.writestr("ljfake-1.0.dist-info/WHEEL", "Wheel-Version: 1.0\nGenerator: lj\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
    z.writestr("ljfake-1.0.dist-info/RECORD", "")
h = hashlib.sha256(open(whl, "rb").read()).hexdigest()
open(d + "/good.txt", "w").write("--require-hashes\nljfake==1.0 \\\n    --hash=sha256:%s\n" % h)
open(d + "/bad.txt", "w").write("--require-hashes\nljfake==1.0 \\\n    --hash=sha256:%s\n" % ("0" * 64))
open(d + "/nohash.txt", "w").write("--require-hashes\nljfake==1.0\n")
PY
pipx() { python3 -m pip install --dry-run --no-index --find-links "$FW" --disable-pip-version-check --require-hashes -r "$FW/$1.txt" 2>&1; }
g="$(pipx good)"; grc=$?; b="$(pipx bad)"; brc=$?; n="$(pipx nohash)"; nrc=$?
check sp3.pip_require_hashes_mode "$([ $grc = 0 ] && [ $brc != 0 ] && [ $nrc != 0 ] && grep -q 'DO NOT MATCH THE HASHES' <<<"$b" && grep -q 'Hashes are required' <<<"$n" && echo 1 || echo 0)" "offline, a tiny local wheel and this machine's pip: the right digest installs (exit $grc), a wrong digest is refused (exit $brc, DO NOT MATCH THE HASHES), a requirement with no hash is refused (exit $nrc); so the line run_sp3.sh uses does what it says" "pip --require-hashes accepts the pinned digest and refuses a mismatch or a missing hash"
L2="$WORK/ledger_pip.jsonl"; : > "$L2"
a1="$(python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" append --ledger "$L2" --stage t1 --date 2026-10-20 2>&1)"; r1=$?
a2="$(python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" append --ledger "$L2" --stage t2 --date 2026-10-21 2>&1)"; r2=$?; n2="$(wc -l < "$L2")"
a3="$(python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" append --ledger "$L2" --stage t3 --date 2026-10-21 --exception "test reason: confirm a fix" 2>&1)"; r3=$?; n3="$(wc -l < "$L2")"
check sp3.second_fetch_needs_a_reason "$([ $r1 = 0 ] && [ $r2 = 3 ] && [ "$n2" = 1 ] && [ $r3 = 0 ] && [ "$n3" = 2 ] && [ "$(python3 -I "$ROOT/spikes/sp3_blender/ledger_row.py" count --ledger "$L2")" = 2 ] && [ "$(jq -r '.fetch' <<<"$(sed -n 2p "$L2")")" = 2 ] && [ "$(jq -r '.bytes' <<<"$(sed -n 2p "$L2")")" = 428225665 ] && echo 1 || echo 0)" "first fetch recorded (exit $r1); a second without a reason is refused (exit $r2, ledger still $n2 line); with a reason it is recorded as fetch 2 (exit $r3, $n3 lines, 428,225,665 bytes a row)" "a later fetch of the bpy wheel set needs a recorded exception, as for a Craft tarball"
PE="$WORK/pip_ev"; mkdir -p "$PE"      # an empty evidence folder: the stage envelope planted by the test above must not leak into this one
out="$(python3 -I "$SP/check_ledger.py" --wp10 "$L2" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$PE" 2>&1)"; rc=$?
sed -e 's/"exception": "test reason: confirm a fix"/"exception": ""/' "$L2" > "$WORK/ledger_pip_bad.jsonl"
out2="$(python3 -I "$SP/check_ledger.py" --wp10 "$WORK/ledger_pip_bad.jsonl" --wp07 "$L/wp07/none.jsonl" --disk-ledger "$L/scratch/none.jsonl" --evidence "$PE" 2>&1)"; rc2=$?
check ledger.pip_rows_counted_and_held_to_the_rule "$([ $rc = 0 ] && grep -q ' 816\.[0-9] MB of the 2560 MB' <<<"$(sed -n 1p <<<"$out")" && grep -q 'bpy-5.2.2-wheelset-cp313-linux-x86_64 .*pip wheel set from PyPI, 2 fetch' <<<"$out" && [ $rc2 = 1 ] && grep -q 'bpy-5.2.2-wheelset-cp313-linux-x86_64 was fetched 2 times and a later fetch has no recorded exception' <<<"$out2" && echo 1 || echo 0)" "two pip fetches count 816.7 MB toward the total (exit $rc, $(sed -n 1p <<<"$out" | cut -c1-150)); the same ledger with the reason removed exits $rc2" "pip fetches count toward the 2,560 MB allowance (raised from 2,048 on 2026-10-20) and a repeat without a reason is a problem"
LAST_OUT="$out"
out="$(python3 -I "$SP/check_ledger.py" 2>&1)"; rc=$?
mb="$(sed -n '1s/.*, \([0-9.]*\) MB of the 2560 MB allowance.*/\1/p' <<<"$out")"
check ledger.real_includes_pip_fetches "$([ $rc = 0 ] && grep -q 'bpy-5.2.2-wheelset-cp313-linux-x86_64 .*pip wheel set from PyPI, 2 fetch' <<<"$out" && awk -v m="${mb:-0}" 'BEGIN { exit !(m >= 1400 && m < 2560) }' && echo 1 || echo 0)" "the real ledgers: exit $rc, ${mb:-?} MB of the 2560 MB allowance, the bpy wheel set listed with its 2 fetches (it read 623.6 MB before the pip fetches were put on the ledger)" "the allowance check reads about 1.5 GB, not 0.6 GB"
LAST_OUT="$out"
printf '%s\n' '{"app":"bpy","asset":"bpy-5.2.2-wheelset-cp313-linux-x86_64","bytes":428225665,"date_utc":"2026-10-20","exception":"","fetch":1,"kind":"pip-wheel-set","sha256":"x","stage":"t1","tag":"5.2.2"}' > "$WORK/ledger_one.jsonl"
out="$(LJ_SP3_LEDGER="$WORK/ledger_one.jsonl" LJ_DF_CMD="$(fakedf 5000)" bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run 2>&1)"; rc=$?
out2="$(LJ_SP3_LEDGER="$WORK/ledger_one.jsonl" LJ_DF_CMD="$(fakedf 5000)" SP3_DRYRUN=1 SP3_FETCH_REASON="test reason" bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run 2>&1)"; rc2=$?
check sp3.run_refused_without_a_reason "$([ $rc = 3 ] && grep -q 'NOT RUN: the download ledger already holds 1 fetch(es) of the bpy wheel set' <<<"$out" && grep -q 'Nothing was started and nothing was forced' <<<"$out" && [ ! -d "$SCRATCH_ROOT/sp3" ] && [ $rc2 = 0 ] && grep -q '^READY: Avail 5000 MB' <<<"$out2" && echo 1 || echo 0)" "with one fetch already on the ledger, --run at a fake 5,000 MB is refused without SP3_FETCH_REASON (exit $rc, nothing started) and the dry run with a reason is READY (exit $rc2)" "a further fetch of the bpy wheel set needs a reason before anything is downloaded"
LAST_OUT="$out"
# the install step of run_inner itself, offline: a tiny local wheel stands in for bpy (PIP_NO_INDEX and PIP_FIND_LINKS point pip at it, LJ_SP3_REQ at a hash-pinned file for it);
# no network, no 402 MB wheel, no bpy. A wrong digest must stop the install and leave nothing behind; the right digest installs, the fetch goes on the (temporary) ledger, and the run then stops at the bpy import
# because the stand-in is not bpy (exit 1).
SCR="$WORK/sp3scr"; mkdir -p "$SCR"; : > "$WORK/inner_ledger.jsonl"
out="$(PIP_NO_INDEX=1 PIP_FIND_LINKS="$FW" LJ_SP3_REQ="$FW/bad.txt" LJ_SP3_LEDGER="$WORK/inner_ledger.jsonl" LJ_SCRATCH="$SCR" bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run-inner 2>&1)"; rc=$?
out2="$(PIP_NO_INDEX=1 PIP_FIND_LINKS="$FW" LJ_SP3_REQ="$FW/good.txt" LJ_SP3_LEDGER="$WORK/inner_ledger.jsonl" LJ_SCRATCH="$SCR" bash "$ROOT/spikes/sp3_blender/run_sp3.sh" --run-inner 2>&1)"; rc2=$?
check sp3.inner_install_is_hash_checked "$([ $rc = 3 ] && grep -q 'pip install (hash-pinned) failed' <<<"$out" && [ ! -d "$SCR/sp3" ] && [ $rc2 = 1 ] && grep -q 'pip compared every download with the sha256' <<<"$out2" && grep -q 'the fetch is on the download ledger' <<<"$out2" && grep -q 'bpy did not import' <<<"$out2" && [ ! -d "$SCR/sp3" ] && [ "$(wc -l < "$WORK/inner_ledger.jsonl")" = 1 ] && echo 1 || echo 0)" "run_inner with a wrong digest: exit $rc (the install stopped, no work folder left); with the right digest: the install ran, the fetch was recorded (ledger $(wc -l < "$WORK/inner_ledger.jsonl") row), then exit $rc2 at the bpy import because the stand-in is not bpy, and the work folder was removed" "the install step of run_sp3.sh uses --require-hashes, records its fetch on the ledger and cleans up on both paths"
LAST_OUT="$out
$out2"

# SP4
L1="$WORK/job_quick.log"
out="$(bash "$ROOT/spikes/sp4_idle/job.sh" --seconds 6 --interval 1 --out "$L1" 2>&1)"; rc=$?
g="$(python3 -I "$ROOT/spikes/sp4_idle/gaps.py" "$L1" --gap-limit 5 2>&1)"; grc=$?
check sp4.job_quick "$([ $rc = 0 ] && [ $grc = 0 ] && grep -q 'VERDICT: kept awake' <<<"$g" && [ "$(grep -c '^[0-9]' "$L1")" = 6 ] && echo 1 || echo 0)" "job.sh 6 s at 1 s: exit $rc, 6 ticks; gaps.py exit $grc: $(grep -E '^(maximum gap|VERDICT)' <<<"$g" | tr '\n' ' ' | cut -c1-120)" "the job writes one epoch line per interval and gaps.py says kept awake"
v=""; ok=1
for spec in "log_clean.txt:0:kept awake" "log_with_5min_gap.txt:1:paused" "log_killed.txt:1:killed" "log_term.txt:1:killed" "log_hiccup_19s.txt:0:kept awake" "log_unreadable.txt:2:" ; do
  f="${spec%%:*}"; rest="${spec#*:}"; ec="${rest%%:*}"; vd="${rest#*:}"
  o="$(python3 -I "$ROOT/spikes/sp4_idle/gaps.py" "$FX/$f" --now 1792402000 2>&1)"; r=$?
  if [ "$r" != "$ec" ] || { [ -n "$vd" ] && ! grep -q "VERDICT: $vd" <<<"$o"; }; then ok=0; v="$v $f(exit $r)"; fi
done
o="$(python3 -I "$ROOT/spikes/sp4_idle/gaps.py" "$FX/log_running.txt" --now 1792400310 2>&1)"; r=$?
[ "$r" = 3 ] && grep -q 'VERDICT: running' <<<"$o" || { ok=0; v="$v log_running(exit $r)"; }
check sp4.fixture_verdicts "$ok" "clean 0 kept awake; 5-minute gap 1 paused; killed 1; ended by TERM 1 killed; 19 s hiccup 0 kept awake; unreadable 2; still running 3; wrong:${v:- none}" "gaps.py gives the right verdict and exit code on each synthetic log"
o="$(python3 -I "$ROOT/spikes/sp4_idle/gaps.py" "$FX/log_with_5min_gap.txt" 2>&1)"; r=$?
check sp4.planted_gap_exit1 "$([ $r = 1 ] && grep -q 'maximum gap: 310 s' <<<"$o" && grep -q 'gap of 310 s after tick 60' <<<"$o" && echo 1 || echo 0)" "exit $r; $(grep -E '^(maximum gap|  gap)' <<<"$o" | tr '\n' ' ' | cut -c1-160)" "the planted 5-minute gap is found and located (acceptance line: exit 1)"
LAST_OUT="$o"

# the verdict table and the evidence
out="$(python3 -I "$T/check_verdicts.py" 2>&1)"; rc=$?
check verdicts.complete "$([ $rc = 0 ] && echo 1 || echo 0)" "$out" "VERDICTS-W2.md has five SP rows, six T lines under SP1 (T5 and T6 not run) and no row without an existing evidence path"
# one writer per verdict file (gate w2, nudge 6): VERDICTS-W2.md is generated from spikes/verdicts/ (template.md and SP1.md to SP5.md)
AS="$ROOT/spikes/verdicts/assemble.py"
out="$(python3 -I "$AS" check 2>&1)"; rc=$?
check verdicts.assembled "$([ $rc = 0 ] && echo 1 || echo 0)" "$(head -1 <<<"$out" | cut -c1-200)" "VERDICTS-W2.md is exactly what spikes/verdicts/template.md and the five spike files assemble to (nobody edited the generated file by hand, and no part changed without a new assembly)"
LAST_OUT="$out"
VT="$WORK/verdicts_try"; mkdir -p "$VT"
cp "$ROOT/spikes/VERDICTS-W2.md" "$VT/V.md"
python3 -I "$AS" import --verdicts "$VT/V.md" --dir "$VT/parts" >/dev/null 2>&1; i1=$?
python3 -I "$AS" --verdicts "$VT/V2.md" --dir "$VT/parts" >/dev/null 2>&1; i2=$?
# the round trip keeps every line of the file except the generated-file banner (and the order of the SP3 and SP4 "does not say" bullets)
rt="$(diff <(grep -v '^<!-- GENERATED by' "$VT/V.md" | sort) <(grep -v '^<!-- GENERATED by' "$VT/V2.md" | sort) | wc -l)"
python3 -I "$AS" check --verdicts "$VT/V2.md" --dir "$VT/parts" >/dev/null 2>&1; c0=$?
sed -e 's/^| \*\*SP2\*\* | /| **SP2** | HAND EDIT /' "$VT/V2.md" > "$VT/V3.md"
python3 -I "$AS" check --verdicts "$VT/V3.md" --dir "$VT/parts" >/dev/null 2>&1; c1=$?
cp -r "$VT/parts" "$VT/parts_bad1"; sed -i 's/^| \*\*SP2\*\* /| **SP3** /' "$VT/parts_bad1/SP2.md"
python3 -I "$AS" --verdicts "$VT/V4.md" --dir "$VT/parts_bad1" >/dev/null 2>&1; b1=$?
cp -r "$VT/parts" "$VT/parts_bad2"; printf '<!-- part: tests -->\n| **T1** x |\n' >> "$VT/parts_bad2/SP2.md"
python3 -I "$AS" --verdicts "$VT/V5.md" --dir "$VT/parts_bad2" >/dev/null 2>&1; b2=$?
cp -r "$VT/parts" "$VT/parts_bad3"; printf '<!-- part: rule -->\n* SP1, a rule in the wrong spike file.\n' >> "$VT/parts_bad3/SP2.md"
python3 -I "$AS" --verdicts "$VT/V6.md" --dir "$VT/parts_bad3" >/dev/null 2>&1; b3=$?
check verdicts.assemble_machinery "$([ $i1 = 0 ] && [ $i2 = 0 ] && [ "$rt" = 0 ] && [ $c0 = 0 ] && [ $c1 = 1 ] && [ $b1 = 2 ] && [ $b2 = 2 ] && [ $b3 = 2 ] && [ ! -e "$VT/V4.md" ] && echo 1 || echo 0)" "on a copy: import $i1, assemble $i2, the round trip differs in $rt sorted line(s) (0 expected: the banner is set aside, and the SP3 and SP4 bullets may swap places, which sorting hides), check of the clean result $c0, of a hand-edited result $c1 (1 expected), a row in the wrong file $b1, test rows outside SP1 $b2, a rule in the wrong file $b3 (2 expected each, nothing written)" "the assembler splits and joins without losing a line, refuses a hand edit and refuses a part in the wrong file"
LAST_OUT=""
bad="$(python3 -I - "$EVID" <<'PY'
import glob, json, os, sys
d = sys.argv[1]; bad = []
for f in sorted(glob.glob(os.path.join(d, "t1_*.json")) + glob.glob(os.path.join(d, "readback_*.json")) + glob.glob(os.path.join(d, "t3_*.json")) + glob.glob(os.path.join(d, "stage_*.json"))):
    try: r = json.load(open(f))
    except ValueError: bad.append(os.path.basename(f) + " (not JSON)"); continue
    n = os.path.basename(f)
    if r.get("package") != "WP-10": bad.append(n + " package")
    if r.get("schema") != "lj-evidence/1": bad.append(n + " schema")
    if (r.get("detail") or {}).get("label") != "linux-cli": bad.append(n + " label")
    if "Linux CLI result; not evidence for Windows" not in (r.get("notes") or ""): bad.append(n + " notes")
    dk = r.get("disk") or {}
    if "avail_mb_start" not in dk or "floor_mb" not in dk: bad.append(n + " disk")
    if isinstance(dk.get("avail_mb_min"), int) and dk["avail_mb_min"] < 250: bad.append(n + " avail_mb_min %d under 250" % dk["avail_mb_min"])
    if not r.get("unverified_reasons"): bad.append(n + " unverified_reasons")
print(len(glob.glob(os.path.join(d, "stage_*.json"))), "stage envelopes;", "problems:", bad or "none")
sys.exit(1 if bad else 0)
PY
)"; rc=$?
check evidence.labelled_and_disk "$([ $rc = 0 ] && echo 1 || echo 0)" "$bad" "every wp10 envelope is labelled linux-cli ('Linux CLI result; not evidence for Windows'), carries the disk object, and none shows avail_mb_min under 250"
left="$(ls -A "$ROOT/vendor/craft-sp1b" 2>/dev/null | tr '\n' ' ')"
nstage=$(ls "$EVID"/stage_*.json 2>/dev/null | wc -l)
if [ "$nstage" -ge 4 ]; then
  check hygiene.after_sp1b "$([ -z "$left" ] && [ ! -e "$ROOT/vendor/craft/_keep" ] && echo 1 || echo 0)" "vendor/craft-sp1b holds: ${left:-nothing}; vendor/craft/_keep: $([ -e "$ROOT/vendor/craft/_keep" ] && echo present || echo gone)" "after SP1b vendor/craft-sp1b is empty and vendor/craft/_keep is gone"
else
  rec SKIPPED hygiene.after_sp1b "only $nstage of the 4 stages have run, so the post-SP1b state is not asserted" "after SP1b vendor/craft-sp1b is empty and vendor/craft/_keep is gone"
fi
out="$(python3 -I "$ROOT/scripts/public_lint.py" --paths spikes/sp1b_readback spikes/sp3_blender spikes/sp4_idle spikes/VERDICTS-W2.md tests/spikes build/evidence/wp10 2>&1 | tail -1)"
check lint.public "$(grep -q ' 0 identifying-data finding(s), 0 hygiene finding(s)' <<<"$out" && echo 1 || echo 0)" "$out" "public_lint.py finds no identifying data in the owned paths"
out="$(python3 -I "$ROOT/scripts/public_lint.py" --theme --paths spikes/sp1b_readback spikes/sp3_blender spikes/sp4_idle spikes/VERDICTS-W2.md tests/spikes 2>&1)"; rc=$?
line="$(grep '^theme guard' <<<"$out" | head -1)"
check lint.theme "$([ $rc = 0 ] && grep -q ' 0 finding(s)' <<<"$line" && echo 1 || echo 0)" "exit $rc; $line" "the D-28 theme guard finds nothing in the owned paths (the test content is geometric: test cards, grids, digits; a keyword scan cannot judge pictures)"

rec UNVERIFIED windows.craft_behaviour "no Windows PC here: every Craft result of this package is a Linux CLI result. Whether PhotoCraft, VectorCraft, LightCraft and FilmCraft on Windows keep the same layer names, ids, keyframes and exports, what the apps write to the profile folders, and every PowerShell step are for the maker's Sat 24 Oct five-minute tests (spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md)" "Windows behaviour is marked UNVERIFIED, never PASS"

if [ "$MODE" = "--quick" ]; then
  echo "SUMMARY quick: $NPASS PASS, $FAILS FAIL, $BLOCKED BLOCKED, $UNV UNVERIFIED"
  [ "$FAILS" -gt 0 ] && exit 1; [ "$BLOCKED" -gt 0 ] && exit 3; exit 0
fi

# ------------------------------------------------------------------ ALL: the 60 s SP4 run
L2="$WORK/job_60.log"
out="$(bash "$ROOT/spikes/sp4_idle/job.sh" --seconds 60 --interval 2 --out "$L2" 2>&1)"; rc=$?
g="$(python3 -I "$ROOT/spikes/sp4_idle/gaps.py" "$L2" --json "$EVID/sp4_job_60s_gaps.json" 2>&1)"; grc=$?
mg="$(sed -n 's/^maximum gap: \([0-9]*\) s.*/\1/p' <<<"$g")"
check sp4.acceptance_60s "$([ $rc = 0 ] && [ $grc = 0 ] && [ "${mg:-99}" -le 5 ] && echo 1 || echo 0)" "job.sh --seconds 60 --interval 2: exit $rc, $(grep -c '^[0-9]' "$L2") ticks; gaps.py exit $grc, maximum gap ${mg} s (no gap over 5 s), $(grep VERDICT <<<"$g")" "no gap > 5 s -> exit 0"
LAST_OUT="$g"

# ------------------------------------------------------------------ ALL: the real run_sp1b.sh --all (re-runnable: a stage that already ran is not run again)
out="$(bash "$SP/run_sp1b.sh" --all 2>&1)"; rc=$?
res="$(grep '^RESULT' <<<"$out" | sed -e 's/ (label.*//' | tr '\n' ';')"
nb=$(grep -c '^RESULT.*: BLOCKED' <<<"$out"); nf=$(grep -cE '^RESULT.*: (FAIL|UNVERIFIED)' <<<"$out"); np=$(grep -c '^RESULT.*: PASS' <<<"$out")
want=0; [ "$nb" -gt 0 ] && want=3; [ "$nf" -gt 0 ] && want=1
allrun=$([ "$(grep -c '^RESULT' <<<"$out")" = 4 ] && echo 1 || echo 0)
labelled=$([ "$(grep -c '^RESULT.*label: linux-cli; Linux CLI result; not evidence for Windows' <<<"$out")" = 4 ] && echo 1 || echo 0)
if [ "$nb" -gt 0 ] && [ "$np$nf" = 00 ]; then st=BLOCKED; else st=PASS; fi
if [ "$allrun" = 1 ] && [ "$labelled" = 1 ] && [ "$rc" = "$want" ]; then
  if [ "$nb" -gt 0 ] && [ "$((np + nf))" = 0 ]; then rec BLOCKED sp1b.real_all "every stage was refused by the disk guard (BLOCKED, not failed; exit $rc): $res" "--all: a refused stage is BLOCKED"
  else rec PASS sp1b.real_all "exit $rc as the stage results require ($np PASS, $nf measured FAIL or harness, $nb BLOCKED; a measured FAIL is a finding about the app, not a defect of the harness): $res" "--all: staged, each result labelled linux-cli, a refused stage is BLOCKED not failed"; fi
else
  LAST_OUT="$out"; check sp1b.real_all 0 "exit $rc (expected $want), RESULT lines $(grep -c '^RESULT' <<<"$out") of 4, labelled $labelled: $res" "--all: staged, each result labelled linux-cli, a refused stage is BLOCKED not failed"
fi
for app in filmcraft:T3 photocraft:T1 vectorcraft:T1 lightcraft:T1; do
  a="${app%%:*}"; tag="$(jq -r --arg a "$a" '.stages[]|select(.app==$a)|.tag' "$SP/config.json")"
  f="$EVID/stage_$a-$tag.json"; s="$(jqe .status "$f")"
  if [ "$s" = PASS ] || [ "$s" = FAIL ]; then rec PASS "sp1b.real_$a" "stage ran to a verdict: $s ($(jq -r '.detail.reason // empty' "$f" | cut -c1-80)); the measured status is a finding about the app, recorded in $(basename "$f" | sed 's/stage_//')" "the stage ran once and left evidence"
  elif [ "$s" = BLOCKED ]; then rec BLOCKED "sp1b.real_$a" "$(jq -r '.detail.reason' "$f" | cut -c1-200)" "the stage ran once and left evidence"
  else rec FAIL "sp1b.real_$a" "no usable stage envelope (status '${s}')" "the stage ran once and left evidence"; fi
done
out="$(python3 -I "$SP/check_ledger.py" 2>&1)"; rc=$?
check ledger.after_real_all "$([ $rc = 0 ] && echo 1 || echo 0)" "$(head -1 <<<"$out" | cut -c1-240)" "after the real run each tarball is still fetched once (exceptions listed)"

# ------------------------------------------------------------------ ALL: the mechanism tests against a local fake release server
mkcase() {  # mkcase NAME [make_fake_release args] -> sets C (case dir) and starts the server; exports the LJ_* overrides
  C="$WORK/case_$1"; shift
  mkdir -p "$C/evid" "$C/vendor" "$C/scratch" "$C/keep"
  python3 -I "$T/make_fake_release.py" --out "$C/rel" "$@" >/dev/null || return 1
  python3 -u -m http.server 0 --bind 127.0.0.1 --directory "$C/rel/www" > "$C/http.log" 2>&1 &
  CSRV=$!; SRV_PIDS="$SRV_PIDS $CSRV"
  local i port=""
  for i in $(seq 1 50); do port="$(sed -n 's/.*port \([0-9][0-9]*\).*/\1/p' "$C/http.log" | head -1)"; [ -n "$port" ] && break; sleep 0.1; done
  [ -n "$port" ] || return 1
  export LJ_RELEASE_BASE="http://127.0.0.1:$port" LJ_SP1_ASSETS="$C/rel/release_assets.json" LJ_SP1_R8=none LJ_SP1_EVIDENCE="$C/evid" LJ_SP1B_VENDOR="$C/vendor" LJ_SP1B_KEEP_DIR="$C/keep" LJ_SCRATCH="$C/scratch" LJ_DF_CMD="$(fakedf 2000)"
}
endcase() { kill "$CSRV" 2>/dev/null; unset LJ_RELEASE_BASE LJ_SP1_ASSETS LJ_SP1_R8 LJ_SP1_EVIDENCE LJ_SP1B_VENDOR LJ_SP1B_KEEP_DIR LJ_SCRATCH LJ_DF_CMD FORCE_BAD_ASSET LJ_POLL_S LJ_FAKE_DF_FLAG; }
failed_ids() { jq -r '[.detail.checks[]|select(.pass==false)|.id]|sort|join(",")' "$1" 2>/dev/null; }
ledger_n() { if [ -f "$C/evid/download_ledger.jsonl" ]; then wc -l < "$C/evid/download_ledger.jsonl"; else echo 0; fi; }
vend() { ls -A "$C/vendor" 2>/dev/null | tr '\n' ' '; }

# M1 three stages
if mkcase three; then
  o1="$(bash "$SP/run_sp1b.sh" --only photocraft 2>&1)"; r1=$?; o2="$(bash "$SP/run_sp1b.sh" --only vectorcraft 2>&1)"; r2=$?; o3="$(bash "$SP/run_sp1b.sh" --only lightcraft 2>&1)"; r3=$?
  lab=1; for a in photocraft-v0.10.0 vectorcraft-v0.13.1 lightcraft-v0.9.1; do [ "$(jqe .detail.label "$C/evid/stage_$a.json")" = linux-cli ] && [ "$(jqe .status "$C/evid/stage_$a.json")" = PASS ] || lab=0; done
  LAST_OUT="$o1$o2$o3"
  check mech.three_stages_pass "$([ $r1 = 0 ] && [ $r2 = 0 ] && [ $r3 = 0 ] && [ "$lab" = 1 ] && [ "$(ledger_n)" = 3 ] && [ -z "$(vend)" ] && [ "$(ls "$C/evid"/t1_*.json "$C/evid"/readback_*.json | wc -l)" = 6 ] && echo 1 || echo 0)" "exits $r1 $r2 $r3; 3 stage envelopes PASS and labelled linux-cli; 3 T1 + 3 read-back envelopes; ledger $(ledger_n) lines; vendor holds: ${C:+$(vend)}nothing" "each app: one fetch, SHA-256 first, one member extracted, T1 and read-backs, tarball and tree deleted"
  # M2 rerun downloads nothing; --again records the exception
  o4="$(bash "$SP/run_sp1b.sh" --only photocraft 2>&1)"; r4=$?; n_before=$(ledger_n)
  o5="$(bash "$SP/run_sp1b.sh" --only photocraft --again 2>&1)"; r5=$?; n_after=$(ledger_n)
  lo="$(python3 -I "$SP/check_ledger.py" 2>&1)"; lr=$?
  check mech.rerun_no_second_download "$([ $r4 = 0 ] && grep -q 'already run' <<<"$o4" && [ "$n_before" = 3 ] && [ $r5 = 0 ] && [ "$n_after" = 4 ] && grep -q 'exception: re-fetch' <<<"$o5" && [ $lr = 0 ] && grep -q '^exceptions: .*re-fetch' <<<"$lo" && echo 1 || echo 0)" "second run: 'already run', ledger $n_before lines (no download); --again: ledger $n_after lines with the exception; check_ledger exit $lr and lists it" "a stage that ran is not run again; --again records the exception in the ledger"
  LAST_OUT="$o4$o5"
  endcase
else rec FAIL mech.three_stages_pass "could not start the fake release server" "the fake server starts"; fi

# M3 planted defects (each makes exactly its own criterion fail)
defect() {  # defect NAME app flag_value expected_failed_ids
  local name="$1" app="$2" bugs="$3" want="$4" tag flag
  case "$app" in photocraft) tag=v0.10.0; flag=--bug-photo;; vectorcraft) tag=v0.13.1; flag=--bug-vector;; lightcraft) tag=v0.9.1; flag=--bug-light;; esac
  if mkcase "d_$name" "$flag" "$bugs"; then
    o="$(bash "$SP/run_sp1b.sh" --only "$app" 2>&1)"; r=$?
    got="$(failed_ids "$C/evid/readback_${app}_$tag.json")"
    LAST_OUT="$o"
    check "mech.defect_$name" "$([ $r = 1 ] && [ "$got" = "$want" ] && [ "$(jqe .status "$C/evid/stage_$app-$tag.json")" = FAIL ] && echo 1 || echo 0)" "stand-in with '$bugs': exit $r, failed criteria: ${got:-none} (expected $want)" "exactly the planted defect's criterion FAILs (the stage is FAIL, exit 1)"
    endcase
  else rec FAIL "mech.defect_$name" "could not start the fake release server" "the fake server starts"; fi
}
defect photo_dropnames photocraft dropnames "RB.photocraft.at.layer_names,RB.photocraft.at.ora_roundtrip_names,RB.photocraft.at.psd_names,RB.photocraft.wp06.layer_names,RB.photocraft.wp06.ora_roundtrip_names,RB.photocraft.wp06.psd_names"
defect photo_nopsd photocraft nopsd "RB.photocraft.at.psd_names,RB.photocraft.wp06.psd_names"
defect photo_badsize photocraft badsize "RB.photocraft.at.convert_png,RB.photocraft.wp06.convert_png"
defect vector_dropids vectorcraft dropids "RB.vectorcraft.at.check_ids_exit0,RB.vectorcraft.at.wp06_gate_exit0,RB.vectorcraft.wp06.check_ids_exit0,RB.vectorcraft.wp06.wp06_gate_exit0"
defect vector_droppivot vectorcraft droppivot "RB.vectorcraft.at.check_ids_exit0,RB.vectorcraft.at.wp06_gate_exit0,RB.vectorcraft.wp06.check_ids_exit0,RB.vectorcraft.wp06.wp06_gate_exit0"
defect vector_nopdf vectorcraft nopdf "RB.vectorcraft.at.export_png_pdf"
defect light_nobright lightcraft nobright "RB.lightcraft.render_brighter"
defect light_noresize lightcraft noresize "RB.lightcraft.render_written"
defect light_idclash lightcraft idclash "RB.lightcraft.preset_id_kept"
defect light_dupall lightcraft dupall "RB.lightcraft.exports_written,RB.lightcraft.import_all_distinct_prints"

# M4 the guard refuses: BLOCKED with the exact message and the remedy, no download
if mkcase refused; then
  export LJ_DF_CMD="$(fakedf 420)"   # the stand-in tarballs are tiny, so the planned figure is 32 MB (1 tarball + 1 CLI + 30 outputs); 420 - 32 = 388 is under the 400 MB floor
  o="$(bash "$SP/run_sp1b.sh" --only vectorcraft 2>&1)"; r=$?
  gets=$(grep -c 'GET .*tar.gz' "$C/http.log")
  LAST_OUT="$o"
  check mech.guard_refusal_blocked "$([ $r = 3 ] && grep -q 'REFUSED: Avail 420 MB minus planned 32 MB leaves 388 MB, below the 400 MB floor (sp1b-vectorcraft-v0.13.1)' <<<"$o" && grep -q '^Remedy: answer Q-1' <<<"$o" && [ "$(jqe .status "$C/evid/stage_vectorcraft-v0.13.1.json")" = BLOCKED ] && [ "$gets" = 0 ] && [ "$(ledger_n)" = 0 ] && [ -z "$(vend)" ] && echo 1 || echo 0)" "exit $r; $(grep -E '^BLOCKED' <<<"$o" | cut -c1-170); envelope $(jqe .status "$C/evid/stage_vectorcraft-v0.13.1.json"); tarball GETs $gets; ledger $(ledger_n)" "a refused stage is BLOCKED (not failed) with the guard's exact message and the remedy; nothing was downloaded"
  export LJ_DF_CMD="$(fakedf 420)"
  o="$(bash "$SP/run_sp1b.sh" --all 2>&1)"; r=$?
  gets=$(grep -c 'GET .*tar.gz' "$C/http.log")
  LAST_OUT="$o"
  check mech.all_refused_exit3 "$([ $r = 3 ] && [ "$(grep -c '^RESULT.*: BLOCKED' <<<"$o")" = 4 ] && [ "$gets" = 0 ] && [ "$(ledger_n)" = 0 ] && ! grep -q 'LEDGER PROBLEM' <<<"$o" && [ "$(jq -r '.detail.fetched' "$C/evid/stage_vectorcraft-v0.13.1.json")" = false ] && echo 1 || echo 0)" "--all at a fake 420 MB: exit $r, $(grep -c '^RESULT.*: BLOCKED' <<<"$o") of 4 RESULT lines BLOCKED, tarball GETs $gets" "--all with every stage refused exits 3 and downloads nothing"
  endcase
else rec FAIL mech.guard_refusal_blocked "could not start the fake release server" "the fake server starts"; fi

# M5 a blocked download leaves blocked_proof.json
if mkcase blocked; then
  export FORCE_BAD_ASSET=1
  o="$(bash "$SP/run_sp1b.sh" --only lightcraft 2>&1)"; r=$?
  LAST_OUT="$o"
  check mech.blocked_download_proof "$([ $r = 3 ] && grep -q 'BLOCKED: lightcraft-0.9.1-linux-x86_64.tar.gz -> HTTP 404, curl exit 22' <<<"$o" && [ "$(jqe .http_status "$C/evid/blocked_proof.json")" = 404 ] && [ "$(jqe .curl_exit_code "$C/evid/blocked_proof.json")" = 22 ] && [ "$(jqe .status "$C/evid/stage_lightcraft-v0.9.1.json")" = BLOCKED ] && [ "$(ledger_n)" = 0 ] && echo 1 || echo 0)" "exit $r; blocked_proof.json http_status $(jqe .http_status "$C/evid/blocked_proof.json"), curl exit $(jqe .curl_exit_code "$C/evid/blocked_proof.json"); envelope $(jqe .status "$C/evid/stage_lightcraft-v0.9.1.json")" "a wrong asset name: blocked_proof.json with the exact status and curl stderr, the stage BLOCKED, exit 3"
  endcase
else rec FAIL mech.blocked_download_proof "could not start the fake release server" "the fake server starts"; fi

# M6 a corrupted download is rejected before extraction
if mkcase flip --flip-byte lightcraft; then
  o="$(bash "$SP/run_sp1b.sh" --only lightcraft 2>&1)"; r=$?
  LAST_OUT="$o"
  check mech.hash_mismatch_stops "$([ $r = 1 ] && grep -q 'REJECTED' <<<"$o" && grep -q 'STOP AND REPORT' <<<"$o" && ! grep -q 'extracting the one member' <<<"$o" && [ -z "$(vend)" ] && [ "$(ledger_n)" = 1 ] && jq -e '.status=="FAIL" and (.detail.reason|test("hash mismatch"))' "$C/evid/stage_lightcraft-v0.9.1.json" >/dev/null 2>&1 && echo 1 || echo 0)" "exit $r; $(grep -E '^REJECTED' <<<"$o" | cut -c1-120); envelope $(jqe .status "$C/evid/stage_lightcraft-v0.9.1.json"): $(jqe .detail.reason "$C/evid/stage_lightcraft-v0.9.1.json")" "one flipped byte: REJECTED before extraction, stop and report, nothing left behind, one ledger line"
  endcase
else rec FAIL mech.hash_mismatch_stops "could not start the fake release server" "the fake server starts"; fi

# M7 the disk floor aborts a running stage and the stage cleans up
if mkcase floor --bug-photo slow; then
  export LJ_FAKE_DF_FLAG="$C/flag" LJ_POLL_S=0.5 LJ_DF_CMD="$ROOT/tests/sp1/fake_df_flag.sh"
  ( sleep 3; : > "$C/flag" ) &
  o="$(bash "$SP/run_sp1b.sh" --only photocraft 2>&1)"; r=$?
  LAST_OUT="$o"
  check mech.disk_floor_abort_cleans_up "$([ $r = 3 ] && grep -q 'DISK-FLOOR' <<<"$o" && [ -z "$(vend)" ] && [ "$(jqe .status "$C/evid/stage_photocraft-v0.10.0.json")" = BLOCKED ] && ! pgrep -f "$C/vendor" >/dev/null && echo 1 || echo 0)" "exit $r; $(grep -E 'DISK-FLOOR' <<<"$o" | head -1 | cut -c1-140); vendor holds: ${C:+$(vend)}nothing; envelope $(jqe .status "$C/evid/stage_photocraft-v0.10.0.json")" "Avail falls under 250 MB mid-stage: the guard stops the group, the stage's trap removes every folder, BLOCKED, exit 3"
  endcase
else rec FAIL mech.disk_floor_abort_cleans_up "could not start the fake release server" "the fake server starts"; fi

# M8 the exact need after the download does not fit: BLOCKED, tarball deleted
if mkcase after --cli-pad-mb 60; then
  export LJ_DF_CMD="$(fakedf 450)"
  o="$(bash "$SP/run_sp1b.sh" --only photocraft 2>&1)"; r=$?
  LAST_OUT="$o"
  check mech.after_download_block "$([ $r = 3 ] && grep -q 'BLOCKED: after the download Avail is 450 MB and the CLI plus the outputs need' <<<"$o" && grep -q 'the tarball is deleted' <<<"$o" && [ -z "$(vend)" ] && [ "$(ledger_n)" = 1 ] && [ "$(jqe .status "$C/evid/stage_photocraft-v0.10.0.json")" = BLOCKED ] && echo 1 || echo 0)" "exit $r; $(grep -E '^BLOCKED' <<<"$o" | cut -c1-200); ledger $(ledger_n) line; vendor holds: ${C:+$(vend)}nothing" "the guard let the stage in on the estimate, the exact figure after the listing does not fit: BLOCKED, nothing extracted, tarball deleted"
  endcase
else rec FAIL mech.after_download_block "could not start the fake release server" "the fake server starts"; fi

# M9 the FilmCraft stage: a harness problem keeps the kept tarball (no second download)
if mkcase kept; then
  cp "$C/rel/kept/"*.tar.gz "$C/keep/"
  o="$(bash "$SP/run_sp1b.sh" --only filmcraft 2>&1)"; r=$?
  LAST_OUT="$o"
  check mech.kept_harness_error_keeps_tarball "$([ $r = 1 ] && grep -q 'HARNESS ERROR' <<<"$o" && [ "$(jqe .status "$C/evid/stage_filmcraft-v0.9.0.json")" = UNVERIFIED ] && [ -f "$C/keep/filmcraft-0.9.0-linux-x86_64.tar.gz" ] && [ "$(ledger_n)" = 0 ] && [ "$(jqe .detail.fetched "$C/evid/stage_filmcraft-v0.9.0.json")" = false ] && [ -z "$(vend)" ] && echo 1 || echo 0)" "exit $r; envelope $(jqe .status "$C/evid/stage_filmcraft-v0.9.0.json"); kept tarball $([ -f "$C/keep/filmcraft-0.9.0-linux-x86_64.tar.gz" ] && echo kept || echo deleted); ledger $(ledger_n)" "T3 could not drive the CLI (a harness problem): the kept tarball stays, nothing is fetched, UNVERIFIED, exit 1"
  endcase
else rec FAIL mech.kept_harness_error_keeps_tarball "could not start the fake release server" "the fake server starts"; fi

# M10 a corrupt kept tarball is replaced, with a recorded exception
if mkcase keptbad --flip-kept; then
  cp "$C/rel/kept/"*.tar.gz "$C/keep/"
  o="$(bash "$SP/run_sp1b.sh" --only filmcraft 2>&1)"; r=$?
  lo="$(python3 -I "$SP/check_ledger.py" 2>&1)"; lr=$?
  LAST_OUT="$o"
  check mech.kept_corrupt_refetch "$([ "$(ledger_n)" = 1 ] && jq -e '.exception=="kept tarball rejected"' "$C/evid/download_ledger.jsonl" >/dev/null && grep -q 'REJECTED' <<<"$o" && grep -q 'recorded as a ledger exception' <<<"$o" && [ $lr = 0 ] && grep -q 'kept tarball rejected' <<<"$lo" && [ ! -f "$C/keep/filmcraft-0.9.0-linux-x86_64.tar.gz" ] && echo 1 || echo 0)" "ledger $(ledger_n) line, exception '$(jq -r '.exception' "$C/evid/download_ledger.jsonl" 2>/dev/null)'; check_ledger exit $lr and lists it" "a kept tarball that fails SHA-256 is removed and fetched once, with the exception 'kept tarball rejected'"
  endcase
else rec FAIL mech.kept_corrupt_refetch "could not start the fake release server" "the fake server starts"; fi

# M11 a missing kept tarball is fetched once, with a recorded exception
if mkcase keptgone; then
  o="$(bash "$SP/run_sp1b.sh" --only filmcraft 2>&1)"; r=$?
  lo="$(python3 -I "$SP/check_ledger.py" 2>&1)"; lr=$?
  LAST_OUT="$o"
  check mech.kept_missing_refetch "$([ "$(ledger_n)" = 1 ] && jq -e '.exception|test("WP-07 could not keep the tarball")' "$C/evid/download_ledger.jsonl" >/dev/null && [ $lr = 0 ] && grep -q 'WP-07 could not keep the tarball' <<<"$lo" && echo 1 || echo 0)" "ledger $(ledger_n) line, exception '$(jq -r '.exception' "$C/evid/download_ledger.jsonl" 2>/dev/null)'" "no kept tarball: one re-fetch, recorded as a ledger exception (the plan's keep-rule fallback)"
  endcase
else rec FAIL mech.kept_missing_refetch "could not start the fake release server" "the fake server starts"; fi

echo "SUMMARY all: $NPASS PASS, $FAILS FAIL, $BLOCKED BLOCKED, $UNV UNVERIFIED"
[ "$FAILS" -gt 0 ] && exit 1; [ "$BLOCKED" -gt 0 ] && exit 3; exit 0
