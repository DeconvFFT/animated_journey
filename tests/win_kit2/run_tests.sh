#!/usr/bin/env bash
# tests/win_kit2/run_tests.sh [--quick|--all]    WP-09: Windows kit B (Ken Burns at 24 fps, archive init and verify, PC colour and spec runner)
#
#   --quick  (37 to 47 s measured on the 4-vCPU container, about 80 CPU-seconds; the runner gives this area 90 s instead of the common 60 s, since Tue 20 Oct 2026, because the hosts differ by 1.4x to 2x:
#            DEFAULT_AREAS in scripts/run_week2_checks.sh; no downloads, no timed runs) lint and parse, the archive scripts, the runner's test modes and refusals,
#            quoting, the wrappers' error paths, geometry, loading and a one-second render
#   --all    everything in --quick plus the acceptance lines of the build plan (the full Ken Burns self-test, spec_check, the MO8
#            gate on the sub-pixel push and on the zoompan proof), the real run of run_checks_pc.ps1 on this container's ffmpeg and
#            the refusal with a planted build flag in the real flow, the derived file, and public_lint --self-test
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
# Exit 0 only if no line is FAIL or BLOCKED; 1 if a line FAILs; 3 if a line is BLOCKED (pwsh, ffmpeg or the pattern file is
# missing, or the disk is below its floor). UNVERIFIED lines (Windows-only behaviour) and SKIPPED lines are listed and never
# counted as a pass. Every test writes one evidence envelope (build plan 4.2) to build/evidence/wp09/tests_<mode>.jsonl.
#
# Environment: PWSH  path to pwsh 7.5.4 (default <scratch>/pwsh/pwsh, see win/tools/fetch_pwsh.sh)
# Nothing here uses the network. Everything the tests write goes to renders/wp09/ (git-ignored), a temporary folder under
# <scratch>, and build/evidence/wp09/. All pictures are synthetic; every planted value is built from fragments at run time.
set -u
MODE="${1:---quick}"
case "$MODE" in --quick|--all) ;; *) echo "usage: run_tests.sh [--quick|--all]" >&2; exit 2;; esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 3
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
PWSH="${PWSH:-$SCRATCH/pwsh/pwsh}"
PY="python3 -I -B"
EVID="$ROOT/build/evidence/wp09"
T="tests/win_kit2"
K="win/kit2"
RW="renders/wp09"
mkdir -p "$EVID" "$RW" 2>/dev/null
TMP="$(mktemp -d "$SCRATCH/wp09-test.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
JSONL="$EVID/tests_${MODE#--}.jsonl"
: > "$JSONL"
NPASS=0; NFAIL=0; NUNV=0; NSKIP=0; NBLOCK=0
T0=$(date +%s)

avail_mb() { df -BM -P / | awk 'NR==2 { gsub("M","",$4); print $4 }'; }
START_MB="$(avail_mb)"
MIN_MB="$START_MB"

# ------------------------------------------------------------------ recording
record() {  # record NAME STATUS EXPECTED ACTUAL [UNVERIFIED_REASON]
  local name="$1" status="$2" exp="$3" act="$4" unv="${5:-}"
  if [ -n "${RECORD_TO:-}" ]; then   # inside a parallel worker: queue the result; the parent replays it in order
    exp="${exp//$'\n'/ }"; act="${act//$'\n'/ }"; unv="${unv//$'\n'/ }"; exp="${exp//$'\t'/ }"; act="${act//$'\t'/ }"
    printf '%s\t%s\t%s\t%s\t%s\n' "$status" "$name" "$exp" "$act" "$unv" >> "$RECORD_TO"
    return 0
  fi
  case "$status" in PASS) NPASS=$((NPASS+1));; FAIL) NFAIL=$((NFAIL+1));; UNVERIFIED) NUNV=$((NUNV+1));; SKIPPED) NSKIP=$((NSKIP+1));; BLOCKED) NBLOCK=$((NBLOCK+1));; esac
  printf '%-10s %-52s %s\n' "$status" "$name" "$(printf '%s' "$act" | head -c 170 | tr '\n' ' ')"
  local now; now="$(avail_mb)"; [ "$now" -lt "$MIN_MB" ] && MIN_MB="$now"
  EV_NAME="$name" EV_STATUS="$status" EV_EXP="$exp" EV_ACT="$act" EV_UNV="$unv" EV_START="$START_MB" EV_END="$now" EV_MIN="$MIN_MB" \
  EV_ROOT="$ROOT" EV_SCRATCH="$SCRATCH" EV_PY="$(python3 --version 2>&1 | awk '{print $2}')" \
  EV_FF="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}' | cut -d- -f1)" EV_JSONL="$JSONL" \
  python3 -I - <<'PYEOF'
import json, os, re, datetime
e = os.environ
def clean(s):
    s = s.replace(e["EV_ROOT"], ".").replace(e["EV_SCRATCH"], "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return s[:600]
s, en, mn = int(e["EV_START"] or 0), int(e["EV_END"] or 0), int(e["EV_MIN"] or 0)
env = {"platform": "linux", "ffmpeg": e["EV_FF"], "nproc": os.cpu_count(), "python": e["EV_PY"], "node": "22.x"}
rec = {"schema": "lj-evidence/1", "package": "WP-09", "test": e["EV_NAME"],
       "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), "status": e["EV_STATUS"], "env": env,
       "disk": {"avail_mb_start": s, "planned_write_mb": 0, "avail_mb_min": min(s, en, mn), "avail_mb_end": en, "floor_mb": 400, "hard_floor_mb": 250},
       "expected": clean(e["EV_EXP"]), "actual": clean(e["EV_ACT"]), "notes": "",
       "unverified_reasons": [e["EV_UNV"]] if e["EV_UNV"] else []}
open(e["EV_JSONL"], "a").write(json.dumps(rec, sort_keys=True) + "\n")
PYEOF
}

# run CMD... in $ROOT; sets OUT (stdout+stderr) and RC
runin() { OUT="$("$@" 2>&1)"; RC=$?; }

# expect NAME EXPECTED_RC [-m REGEX | -n REGEX | -s SHOW_REGEX]... -- CMD...    (-m must match OUT, -n must not, -s picks the lines shown as evidence)
expect() {
  local name="$1" want="$2"; shift 2
  local must=() mustnot=() show='RESULT|category=|NOTE|PASS|FAIL|PARSED|TOTAL|checked|MISMATCH|MISSING|files written|REFUSED|exit'
  while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
    case "$1" in -m) must+=("$2");; -n) mustnot+=("$2");; -s) show="$2";; esac; shift 2
  done
  shift
  runin "$@"
  local why="" rx
  [ "$RC" -eq "$want" ] || why="exit $RC, wanted $want"
  for rx in "${must[@]+"${must[@]}"}"; do printf '%s' "$OUT" | grep -Eq -- "$rx" || why="$why; missing /$rx/"; done
  for rx in "${mustnot[@]+"${mustnot[@]}"}"; do printf '%s' "$OUT" | grep -Eq -- "$rx" && why="$why; found /$rx/"; done
  if [ -z "$why" ]; then record "$name" PASS "exit $want${must[*]:+ matching ${must[*]}}" "exit $RC; $(printf '%s' "$OUT" | grep -E "$show" | head -3 | tr '\n' '|')"
  else record "$name" FAIL "exit $want${must[*]:+ matching ${must[*]}}" "$why :: $(printf '%s' "$OUT" | head -8 | tr '\n' '|')"; fi
}

# check NAME CONDITION_RC DETAIL  (records PASS when CONDITION_RC is 0)
check() { if [ "$2" -eq 0 ]; then record "$1" PASS "$3" "$3"; else record "$1" FAIL "$3" "$3 (not met) ${4:-}"; fi; }

hash_tree() { find "$@" -type f -not -name '*.pyc' -print0 2>/dev/null | sort -z | xargs -0 sha256sum 2>/dev/null | sha256sum | cut -c1-16; }

FAKE="zorb""alex"       # an invented user name, built from two pieces so no file holds it whole
need_pwsh() { [ -x "$PWSH" ]; }
FFV="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
echo "WP-09 tests ($MODE). pwsh: $(need_pwsh && echo present || echo MISSING)  ffmpeg: ${FFV:-MISSING}  patterns file: $([ -f scripts/redaction_patterns.json ] && echo present || echo MISSING)  disk avail: ${START_MB} MB"

if ! need_pwsh || [ -z "$FFV" ] || [ ! -f scripts/redaction_patterns.json ]; then
  record start_gate BLOCKED "pwsh, ffmpeg and scripts/redaction_patterns.json present" "a start gate is not met (run win/tools/fetch_pwsh.sh; install ffmpeg; WP-03 delivers the pattern file)"
  exit 3
fi
if [ "$START_MB" -lt 250 ]; then
  record disk_gate BLOCKED "Avail at least 250 MB" "Avail ${START_MB} MB is under the hard floor; nothing was run"
  exit 3
fi

# the kb_checks run in the background while the pwsh tests run (they use different resources); read at the end
KBOUT="$TMP/kb_checks.out"
( $PY "$T/kb_checks.py" "$MODE" > "$KBOUT" 2>&1; echo "RC=$?" >> "$KBOUT" ) &
KBPID=$!

sec_static() {
# ================================================================== lint, parse, hygiene
expect lint.kit2_ps1_scripts 0 -m 'TOTAL: 0 error' -- $PY win/tools/ps_lint.py $K/*.ps1
expect lint.readme_fences 0 -m 'TOTAL: 0 error' -m '[0-9]+ powershell fence' -- $PY win/tools/ps_lint.py --allow-write $K/README-KIT2.md
expect parse.scripts_and_readme_fences 0 -m 'PARSED [0-9]+ item\(s\), 0 parse error' -n 'parse error:' -- env PWSH="$PWSH" bash win/tools/ps_parse.sh
FENCES="$(grep -c '^```powershell' $K/README-KIT2.md)"
OKFENCES="$(printf '%s' "$OUT" | grep -c 'README-KIT2.md (fence')"
OKSCRIPTS="$(printf '%s' "$OUT" | grep -cE '^OK +win/kit2/[a-z_0-9]+\.ps1')"
check parse.every_readme_fence_and_every_kit2_script_was_parsed $([ "$FENCES" -ge 15 ] && [ "$FENCES" = "$OKFENCES" ] && [ "$OKSCRIPTS" -eq 4 ] && echo 0 || echo 1) "$FENCES powershell fences in README-KIT2.md, $OKFENCES parsed OK; $OKSCRIPTS of 4 kit2 scripts parsed OK"
printf '# planted\n[System.IO.File]::WriteAllText("x", "y")\nSet-Content -Path x -Value y\n' > "$TMP/plant_write.ps1"
expect lint.read_only_mode_catches_a_planted_write_cmdlet 1 -m 'RO-write' -- $PY win/tools/ps_lint.py "$TMP/plant_write.ps1"
if grep -nE 'WriteAll|CreateDirectory|\.Delete\(|\.Move\(|New-Item|Out-File|Set-Content|Add-Content|Copy-Item|Move-Item|Remove-Item|\.Close\(\)' $K/archive_verify.ps1 >/dev/null; then
  check archive_verify.contains_no_write_or_delete_call 1 "archive_verify.ps1 has no file-writing call (.NET writes are not seen by ps_lint, so this greps for them)" "$(grep -nE 'WriteAll|CreateDirectory|\.Delete\(|\.Move\(|New-Item|Out-File' $K/archive_verify.ps1 | head -2)"
else check archive_verify.contains_no_write_or_delete_call 0 "archive_verify.ps1 has no file-writing or deleting call (checked by grep, because .NET writes are not seen by ps_lint)"; fi
for f in $K/kenburns_24.py $K/pc_helpers.py $T/kb_checks.py $T/fixtures.py $T/dissolve_check.py $T/drift_guard.py; do python3 -I -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read(), feature_version=(3, 9))" "$f" || { check py.parse 1 "$f"; }; done
check py.all_python_files_parse 0 "kenburns_24.py, pc_helpers.py, kb_checks.py, fixtures.py, dissolve_check.py and drift_guard.py parse with the Python 3.9 grammar (no match statement, no X | Y types)"
# drift guard (review r1): the maker's scripts are self-contained, so six helpers are pasted into several of them; the copies must stay byte-identical
expect drift.shared_ps1_helpers_are_byte_identical_in_every_copy 0 -m 'RESULT: OK, 4 scripts, 6 shared functions identical' -n 'DRIFT' -s 'RESULT|copies' -- $PY $T/drift_guard.py $K
mkdir -p "$TMP/drift_a" "$TMP/drift_b"; cp $K/*.ps1 "$TMP/drift_a/"; cp $K/*.ps1 "$TMP/drift_b/"
sed -i 's/-gt 140/-gt 141/' "$TMP/drift_a/archive_verify.ps1"                       # negative control 1: one character changed in ONE copy of Clean-Message
expect drift.guard_catches_a_one_character_change_in_one_copy 1 -m 'DRIFT +Clean-Message .*DIFFERENT VERSIONS: .*\| archive_verify\.ps1$' -m 'RESULT: DRIFT: Clean-Message differs' -- $PY $T/drift_guard.py "$TMP/drift_a"
sed -i '/^# Shared helpers/d' "$TMP/drift_b/archive_init.ps1"                         # negative control 2: the sibling-copies note removed from one script
expect drift.guard_catches_a_missing_sibling_note 1 -m 'DRIFT +header note in archive_init\.ps1' -m 'RESULT: DRIFT' -- $PY $T/drift_guard.py "$TMP/drift_b"

}

sec_stale() {
# stale values (25 fps and friends) and the identifying-data lint on the owned paths
BADRX='d=12[5]|fps=2[5]\b|-r 2[5]\b|-framerate 2[5]\b|\bat 2[5] fps|2[5] frames (a|per) second|atsc_1080p_2[5]|Timebase 2[5]|-1\.5 dBTP'
if grep -rEn "$BADRX" $K $T --include='*' -I 2>/dev/null | grep -v 'Binary' | grep -q .; then
  check hygiene.no_stale_25fps_value_in_any_new_file 1 "none of the retired 25-frame values (the old zoompan frame count, the old frame-rate options, the old atsc profile) or the retired loudness ceiling in win/kit2 or tests/win_kit2" "$(grep -rEn "$BADRX" $K $T -I | head -2)"
else check hygiene.no_stale_25fps_value_in_any_new_file 0 "none of the retired 25-frame values (the old zoompan frame count, the old frame-rate options, the old atsc profile) or the retired loudness ceiling in win/kit2 or tests/win_kit2"; fi
if [ "$MODE" = "--all" ]; then   # the full-tree stale scan takes about 15 s of CPU: --all only (the grep above is in --quick)
runin $PY scripts/stale_check.py --quiet --json "$TMP/stale.json"
STALE_N="$($PY -c "
import json,sys
d=json.load(open(sys.argv[1]))
rows=[]
def walk(o):
    if isinstance(o,dict):
        if 'path' in o and isinstance(o.get('path'),str) and (o['path'].startswith('win/kit2') or o['path'].startswith('tests/win_kit2')): rows.append(o['path'])
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d); print(len(rows))
" "$TMP/stale.json" 2>/dev/null || echo ERR)"
check hygiene.stale_check_has_no_hit_in_the_new_files $([ "$STALE_N" = "0" ] && echo 0 || echo 1) "scripts/stale_check.py finds no stale-copy hit under win/kit2 or tests/win_kit2 (hits: $STALE_N)"
fi
expect hygiene.public_lint_clean_on_owned_paths 0 -m '0 identifying-data finding' -m '0 hygiene finding' -- $PY scripts/public_lint.py --paths $K $T

}

sec_archive() {
# ================================================================== the archive scripts
SA="$RW/standin"
rm -rf "$SA"
expect archive.init_builds_skeleton_and_5_standins 0 -m 'checked 5 files, 0 problems' -m 'files written' -n 'FAILED' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$SA" -Count 5
[ -d "$SA" ] && ARCH_OK=0 || ARCH_OK=1
LISTING="$(cd "$SA" 2>/dev/null && find . -mindepth 1 | sort | tr '\n' ' ')"
check archive.tree_is_the_four_folders_two_csvs_checksums_and_5_tifs $([ "$LISTING" = "./01_masters ./01_masters/LJ-ST-0001-F.tif ./01_masters/LJ-ST-0002-F.tif ./01_masters/LJ-ST-0003-F.tif ./01_masters/LJ-ST-0004-F.tif ./01_masters/LJ-ST-0005-F.tif ./02_work ./03_exports ./04_reconstructions ./checksums.txt ./manifest.csv ./steps.csv " ] && echo 0 || echo 1) "the exact tree; ids LJ-ST-0001-F to 0005-F (box code ST)" "$LISTING"
$PY - "$SA" "$ROOT" <<'PYEOF' > "$TMP/arch.out" 2>&1
import sys, re, os
root, repo = sys.argv[1], sys.argv[2]
play = open(os.path.join(repo, "playbooks", "ai-imagery.md"), encoding="utf-8").read()
step0 = play[play.index("### Step 0"):play.index("### Step 1")]
folders = re.search(r"Create four folders: (.*?)\.", step0).group(1)
folders = re.findall(r"`([^`]+)`", folders)
cols = {}
for key in ("manifest.csv", "steps.csv"):
    m = re.search(r"`%s`.*?Columns: ([^\n]*?)\.(?: `| \n|\n)" % re.escape(key), step0)
    cols[key] = [c.strip() for c in re.split(r",\s*", re.sub(r"\(.*?\)", "", m.group(1)))] if m else None
problems = []
for key in cols:
    raw = open(os.path.join(root, key), "rb").read()
    first = raw.split(b"\n")[0].decode()
    if first.split(",") != cols[key]:
        problems.append("%s header %s != playbook %s" % (key, first, cols[key]))
    if raw.count(b"\n") != 1 or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        problems.append("%s is not exactly one LF-ended BOM-less line" % key)
for f in folders:
    if not os.path.isdir(os.path.join(root, f)):
        problems.append("folder %s missing" % f)
if len(folders) != 4:
    problems.append("playbook folders: %s" % folders)
src = open(os.path.join(repo, "win", "kit2", "archive_init.ps1")).read() + open(os.path.join(repo, "win", "kit2", "archive_verify.ps1")).read()
for f in folders:
    if src.count("'%s'" % f) < 2:
        problems.append("script does not carry folder %s in both scripts" % f)
for key in cols:
    for c in cols[key] or []:
        if src.count("'%s'" % c) < 2:
            problems.append("script does not carry column %s in both scripts" % c)
print("playbook folders %s; manifest columns %d; steps columns %d" % (folders, len(cols["manifest.csv"] or []), len(cols["steps.csv"] or [])))
print("PROBLEMS: " + ("; ".join(problems) if problems else "none"))
PYEOF
check archive.folders_and_columns_equal_step0_of_the_playbook_and_csvs_are_header_only $(grep -q '^PROBLEMS: none' "$TMP/arch.out" && echo 0 || echo 1) "folder names and the 17 + 13 columns read from playbooks/ai-imagery.md Step 0 equal the scripts' and the files'; header-only, one LF line, no BOM" "$(tail -2 "$TMP/arch.out" | tr '\n' ' ')"
# checksums.txt: sha256sum format, LF, no BOM, and GNU sha256sum agrees
CS="$SA/checksums.txt"
GNU="$( (cd "$SA/01_masters" && sha256sum -c ../checksums.txt 2>&1) | tail -1)"
FIRST3="$(head -c 3 "$CS" | od -An -tx1 | tr -d ' ')"
check archive.checksums_are_sha256sum_format_lf_no_bom_and_gnu_agrees $( (cd "$SA/01_masters" && sha256sum -c ../checksums.txt >/dev/null 2>&1) && ! grep -q $'\r' "$CS" && [ "$FIRST3" != "efbbbf" ] && [ "$(wc -l < "$CS")" -eq 5 ] && grep -Eq '^[0-9a-f]{64} \*LJ-ST-000[1-5]-F\.tif$' "$CS" && echo 0 || echo 1) "five lines 'hash *name', lowercase, LF, no BOM; GNU sha256sum -c accepts the file" "$GNU"
IDOUT="$(identify "$SA/01_masters/LJ-ST-0001-F.tif" 2>&1)"; PILOUT="$(python3 -I -c "
from PIL import Image
im=Image.open('$SA/01_masters/LJ-ST-0001-F.tif'); print(im.size, im.mode, im.info.get('dpi'))" 2>&1)"
check archive.standins_are_valid_16_bit_600ppi_tiffs $(printf '%s' "$IDOUT" | grep -q '16-bit' && printf '%s' "$PILOUT" | grep -q '(300, 200) RGB (600.0, 600.0)' && echo 0 || echo 1) "ImageMagick reads 16-bit TIFF 300x200; Pillow reads (300, 200) RGB at 600 dpi" "$IDOUT / $PILOUT"
check archive.standins_differ_from_each_other_and_are_not_empty $(( [ "$(sha256sum "$SA"/01_masters/*.tif | awk '{print $1}' | sort -u | wc -l)" -eq 5 ] && [ "$(stat -c %s "$SA/01_masters/LJ-ST-0001-F.tif")" -gt 300000 ] && echo 0 ) || echo 1) "5 distinct checksums; each file is about 360 KB"
H0="$(hash_tree "$SA")"
expect archive.verify_clean_reports_checked_5_files_0_problems 0 -m 'checked 5 files, 0 problems' -m 'RESULT: OK' -m 'files written: none' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
check archive.verify_changes_nothing $([ "$H0" = "$(hash_tree "$SA")" ] && echo 0 || echo 1) "the archive tree hashes the same before and after archive_verify.ps1 (read-only)"
cp "$SA/01_masters/LJ-ST-0003-F.tif" "$TMP/orig3.tif"
$PY "$T/fixtures.py" tamper "$SA/01_masters/LJ-ST-0003-F.tif" 5000
expect archive.verify_after_one_byte_flip_names_the_file 1 -m 'MISMATCH LJ-ST-0003-F\.tif' -m 'checked 5 files, 1 problems' -m 'RESULT: 1 problem' -n 'MISMATCH LJ-ST-000[1245]' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
$PY "$T/fixtures.py" tamper "$SA/01_masters/LJ-ST-0003-F.tif" 5000
check archive.flipping_the_same_bit_again_restores_the_file $(cmp -s "$TMP/orig3.tif" "$SA/01_masters/LJ-ST-0003-F.tif" && echo 0 || echo 1) "the README's undo works: the second flip gives back the original bytes"
mv "$SA/01_masters/LJ-ST-0002-F.tif" "$TMP/gone2.tif"
expect archive.verify_names_a_missing_file 1 -m 'MISSING +LJ-ST-0002-F\.tif' -m 'checked 5 files, 1 problems' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
mv "$TMP/gone2.tif" "$SA/01_masters/LJ-ST-0002-F.tif"
cp "$SA/01_masters/LJ-ST-0001-F.tif" "$SA/01_masters/LJ-ST-0009-F.tif"
expect archive.verify_reports_an_unlisted_file_as_information 0 -m 'UNLISTED LJ-ST-0009-F\.tif' -m 'unlisted files in 01_masters: 1' -m 'RESULT: OK' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
rm -f "$SA/01_masters/LJ-ST-0009-F.tif"
cp "$SA/manifest.csv" "$TMP/manifest.bak"; printf 'id,box\n' > "$SA/manifest.csv"
expect archive.verify_flags_a_wrong_manifest_header 1 -m 'PROBLEM HEADER manifest.csv' -m 'RESULT: 1 problem' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
cp "$TMP/manifest.bak" "$SA/manifest.csv"
printf 'id,box,medium,scan_date,device,ppi,bit_depth,profile,date_est,date_confidence,people,place,caption_source,interview_date,consent_note,sha256,notes\nLJ-ST-0001-F,ST,print,2026-10-27,flatbed,600,16,sRGB,,,,,,,,,row added by hand\n' > "$SA/manifest.csv"
expect archive.verify_accepts_a_manifest_with_rows_added_by_hand 0 -m 'manifest.csv header' -m 'RESULT: OK' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
cp "$TMP/manifest.bak" "$SA/manifest.csv"
rm -f "$SA/checksums.txt"
expect archive.verify_flags_a_missing_checksums_file 1 -m 'PROBLEM MISSING checksums.txt' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$SA"
if [ "$MODE" = "--all" ]; then   # edge cases of archive_init: --all only
rm -rf "$RW/standin_empty"
expect archive.init_count_0_makes_an_empty_skeleton_and_verifies 0 -m 'checked 0 files, 0 problems' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/standin_empty" -Count 0
expect archive.verify_of_the_empty_skeleton_is_clean 0 -m 'checked 0 files, 0 problems' -m 'RESULT: OK' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$RW/standin_empty"
H1="$(hash_tree "$RW/standin_empty")"
expect archive.init_on_an_existing_archive_changes_nothing 0 -m 'already is an archive' -m 'files written: none' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/standin_empty" -Count 5
check archive.init_on_an_existing_archive_left_the_tree_unchanged $([ "$H1" = "$(hash_tree "$RW/standin_empty")" ] && echo 0 || echo 1) "tree hash identical after the second run"
mkdir -p "$RW/standin_other"; echo keep > "$RW/standin_other/mine.txt"; H2="$(hash_tree "$RW/standin_other")"
expect archive.init_refuses_a_folder_that_holds_other_things 2 -m 'already holds other things' -m 'nothing was changed' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/standin_other"
check archive.refusal_left_the_other_folder_untouched $([ "$H2" = "$(hash_tree "$RW/standin_other")" ] && echo 0 || echo 1) "tree hash identical after the refusal"
rm -rf "$RW/standin_other"
expect archive.init_refuses_a_drive_root 2 -m 'drive root' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "/" -Count 0
expect archive.init_refuses_the_project_folder_itself 2 -m 'project folder itself' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$ROOT" -Count 0
expect archive.init_refuses_count_51 2 -m 'between 0 and 50' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/standin_x" -Count 51
check archive.refusals_created_no_folder $([ ! -e "$RW/standin_x" ] && echo 0 || echo 1) "no folder was made by the refused runs"
rm -rf "$RW/standin_back"
expect archive.init_with_backs_makes_front_and_back 0 -m 'checked 4 files, 0 problems' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/standin_back" -Count 2 -WithBacks
check archive.backs_are_named_LJ_ST_nnnn_B $([ -f "$RW/standin_back/01_masters/LJ-ST-0002-B.tif" ] && [ -f "$RW/standin_back/01_masters/LJ-ST-0001-F.tif" ] && echo 0 || echo 1) "LJ-ST-0001-F, -0001-B, -0002-F and -0002-B exist"
rm -rf "$RW/standin_back" "$RW/with space"
expect archive.init_works_in_a_folder_name_with_a_space 0 -m 'checked 3 files, 0 problems' -- "$PWSH" -NoProfile -File $K/archive_init.ps1 -Root "$RW/with space/standin" -Count 3
expect archive.verify_works_in_a_folder_name_with_a_space 0 -m 'checked 3 files, 0 problems' -- "$PWSH" -NoProfile -File $K/archive_verify.ps1 -Root "$RW/with space/standin"
rm -rf "$RW/with space" "$RW/standin_empty"
fi
check archive.reused_scripts_are_called_in_place_and_unmodified $( (grep -q 'mk_manifest.ps1' $K/archive_init.ps1 && grep -q 'verify_manifest.ps1' $K/archive_init.ps1 && grep -q 'verify_manifest.ps1' $K/archive_verify.ps1 && [ -z "$(git status --porcelain research/sources/format-round1 2>/dev/null)" ] && [ ! -e $K/mk_manifest.ps1 ]) && echo 0 || echo 1) "archive_init.ps1 calls research/sources/format-round1/mk_manifest.ps1 and verify_manifest.ps1 where they sit; git shows them unmodified; no copy in win/kit2"
check archive.output_prints_no_profile_path_or_user_name $( (! printf '%s' "$OUT" | grep -Eq 'C:\\Users|/home/[a-z]+/' ) && echo 0 || echo 1) "no profile path in the last output (paths are printed as <project>, %TEMP% or %USERPROFILE%)"

}

sec_runner() {
# ================================================================== the PC runner: test modes, patterns, refusals
$PY "$T/fixtures.py" raw-clean "$RW/cp_raw_clean.json"
for kind in path name_only hex65 ip email ip_doc; do $PY "$T/fixtures.py" raw-planted $kind "$RW/cp_raw_$kind.json" --fake-user "$FAKE"; done
rm -f "$RW"/cp_out_*.json
RC1="$PWSH -NoProfile -File $K/run_checks_pc.ps1"
expect runner.planted_flag_with_profile_path_and_user_name_is_refused 2 -m 'REDACTION CHECK FAILED, nothing was written' -m 'category=profile_path_windows field=ffmpeg\.configure\[[0-9]+\] hit=C:\*+' -m 'category=user_name field=ffmpeg\.configure\[[0-9]+\] hit=zo\*+' -m 'files written: none' -n "$FAKE" -- $RC1 -TestFixture "$RW/cp_raw_path.json" -FakeUser "$FAKE" -FakeComputer fakehost01 -FakeDomain fakedom -Out "$RW/cp_out_path.json"
check runner.refusal_wrote_nothing $([ ! -e "$RW/cp_out_path.json" ] && echo 0 || echo 1) "no output file after the refusal; the fake user name never appears in the output (checked by -n above)"
expect runner.user_name_alone_is_refused_with_a_masked_hit 2 -m 'category=user_name field=ffmpeg\.configure\[[0-9]+\] hit=zo\*+' -n "$FAKE" -- $RC1 -TestFixture "$RW/cp_raw_name_only.json" -FakeUser "$FAKE" -FakeComputer fakehost01 -FakeDomain fakedom -Out "$RW/cp_out_name.json"
expect runner.a_65_hex_run_is_refused_as_guid_serial 2 -m 'category=guid_serial field=ffmpeg\.version_line hit=cc\*+' -- $RC1 -TestFixture "$RW/cp_raw_hex65.json" -FakeUser "$FAKE" -Out "$RW/cp_out_hex.json"
expect runner.a_public_ipv4_is_refused 2 -m 'category=ipv4 field=ffmpeg\.configure\[[0-9]+\] hit=10\*+' -- $RC1 -TestFixture "$RW/cp_raw_ip.json" -FakeUser "$FAKE" -Out "$RW/cp_out_ip.json"
expect runner.an_email_is_refused 2 -m 'category=email field=ffmpeg\.configure\[[0-9]+\]' -- $RC1 -TestFixture "$RW/cp_raw_email.json" -FakeUser "$FAKE" -Out "$RW/cp_out_email.json"
expect runner.a_documentation_ipv4_is_not_refused 0 -m 'redaction check passed' -- $RC1 -TestFixture "$RW/cp_raw_ip_doc.json" -FakeUser "$FAKE" -Out "$RW/cp_out_ipdoc.json"
expect runner.a_user_name_shorter_than_3_is_skipped_with_a_note 0 -m 'name check skipped for a user_name of 2 character' -m 'redaction check passed' -- $RC1 -TestFixture "$RW/cp_raw_clean.json" -FakeUser ab -Out "$RW/cp_out_short.json"
FROZEN="$K $T win/tools scripts/redaction_patterns.json pipeline/validators pipeline/lib research/sources/format-round1"
H3="$(hash_tree $FROZEN)"
expect runner.clean_fixture_writes_the_raw_file_and_says_test_mode 0 -m 'TEST MODE: nothing was collected' -m 'redaction check passed' -m 'files written: ' -n 'FAILED' -- $RC1 -TestFixture "$RW/cp_raw_clean.json" -FakeUser "$FAKE" -FakeComputer fakehost01 -FakeDomain fakedom -Out "$RW/cp_out_clean.json"
check runner.written_file_is_byte_identical_to_the_fixture_and_has_no_bom $(cmp -s "$RW/cp_raw_clean.json" "$RW/cp_out_clean.json" && [ "$(head -c 3 "$RW/cp_out_clean.json" | od -An -tx1 | tr -d ' ')" != "efbbbf" ] && echo 0 || echo 1) "the raw record is written as read (no re-serialisation), BOM-less UTF-8"
check runner.test_mode_changed_nothing_else_in_the_tree $([ "$H3" = "$(hash_tree $FROZEN)" ] && echo 0 || echo 1) "win/kit2, tests/win_kit2, win/tools, the pattern file, pipeline/validators, pipeline/lib and research/sources/format-round1 hash the same before and after the test-mode runs (only the -Out files are new)"
expect runner.derive_from_gives_a_filed_form_without_build_flags 0 -m 'wrote the derived record' -m 'No build flags, no paths' -- $PY pipeline/validators/colour_patch.py --derive-from "$RW/cp_out_clean.json" --out "$RW/cp_derived.json"
check runner.derived_file_has_no_configure_flags_and_a_known_schema $($PY -c "
import json,sys
d=json.load(open(sys.argv[1])); t=open(sys.argv[1]).read()
ok = d['schema']=='lj-pc-chains/1' and 'configure' not in t and '--enable' not in t and 'version_line' not in t and set(d['ffmpeg'])=={'version','sha256'} and d['ffmpeg']['version']=='9.0.2'
sys.exit(0 if ok else 1)" "$RW/cp_derived.json" && echo 0 || echo 1) "lj-pc-chains/1: ffmpeg version 9.0.2 and sha256 only; no configure text, no version line"
expect runner.derived_file_passes_public_lint 0 -m '1 file\(s\) scanned' -m '0 identifying-data finding' -- $PY scripts/public_lint.py --paths "$RW/cp_derived.json"
# the derived file from the planted record must not exist: derive refuses nothing here, but the planted raw is refused by the runner before it is ever written
$PY "$T/fixtures.py" samples "$RW/samples.json" > /dev/null
expect runner.pattern_self_test_prints_one_json_object 0 -m '^\{"consumer":"win/kit2/run_checks_pc.ps1","patterns_version":' -- $PWSH -NoProfile -File $K/run_checks_pc.ps1 -PatternSelfTest "$RW/samples.json"
$PWSH -NoProfile -File $K/run_checks_pc.ps1 -PatternSelfTest "$RW/samples.json" > "$TMP/ps_mine.json" 2> "$TMP/ps_mine.err"
$PWSH -NoProfile -File win/step0_pc_tests.ps1 -PatternSelfTest "$RW/samples.json" > "$TMP/ps_step0.json" 2>/dev/null
$PY scripts/windows_check.py --pattern-self-test "$RW/samples.json" > "$TMP/ps_wc.json" 2>/dev/null
$PY scripts/public_lint.py --pattern-self-test "$RW/samples.json" > "$TMP/ps_lint.json" 2>/dev/null
$PY - "$TMP" > "$TMP/agree.out" 2>&1 <<'PYEOF'
import json, sys, os
d = sys.argv[1]
def load(n):
    t = open(os.path.join(d, n), encoding="utf-8").read().strip().splitlines()
    return json.loads(t[-1])
mine, s0, wc, lint = load("ps_mine.json"), load("ps_step0.json"), load("ps_wc.json"), load("ps_lint.json")
bad = []
for sid, ans in mine["results"].items():
    for name, other in (("step0_pc_tests.ps1", s0), ("windows_check.py", wc), ("public_lint.py", lint)):
        o = sorted(other["results"].get(sid, ["<none>"]))
        if sorted(ans) != o and not (name == "public_lint.py"):
            bad.append("%s: run_checks_pc says %s, %s says %s" % (sid, sorted(ans), name, o))
# public_lint answers for every scope: compare on the report-scope categories only, as its own self-test does
rep = {"email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux", "token_shape", "guid_serial"}
for sid, ans in mine["results"].items():
    o = sorted(c for c in lint["results"].get(sid, []) if c in rep)
    if sorted(c for c in ans if c in rep) != o:
        bad.append("%s: run_checks_pc says %s, public_lint says %s" % (sid, sorted(ans), o))
print("samples: %d; versions: %s" % (len(mine["results"]), {mine["patterns_version"], s0["patterns_version"], wc["patterns_version"], lint["patterns_version"]}))
print("DISAGREEMENTS: " + ("; ".join(bad[:3]) if bad else "none"))
PYEOF
check runner.agrees_with_step0_windows_check_and_public_lint_on_every_sample $(grep -q '^DISAGREEMENTS: none' "$TMP/agree.out" && echo 0 || echo 1) "three-way comparison on the shared samples file" "$(tr '\n' ' ' < "$TMP/agree.out")"
check runner.pattern_self_test_banner_goes_to_stderr_and_nothing_is_written $(grep -q 'TEST MODE: nothing was collected' "$TMP/ps_mine.err" && [ "$(wc -l < "$TMP/ps_mine.json")" -eq 1 ] && echo 0 || echo 1) "stdout is the one JSON line; 'TEST MODE: nothing was collected' is on stderr"
# fail closed
mkdir -p "$TMP/tree1/win/kit2"; cp $K/run_checks_pc.ps1 "$TMP/tree1/win/kit2/"
expect runner.without_the_pattern_file_it_fails_closed 2 -m 'REDACTION PATTERNS UNAVAILABLE, nothing was collected and nothing was written' -m 'files written: none' -- $PWSH -NoProfile -File "$TMP/tree1/win/kit2/run_checks_pc.ps1" -TestFixture "$RW/cp_raw_clean.json" -Out "$TMP/tree1/out.json"
check runner.fail_closed_wrote_nothing $([ ! -e "$TMP/tree1/out.json" ] && echo 0 || echo 1) "no output file when the pattern file is missing"
mkdir -p "$TMP/tree2/win/kit2" "$TMP/tree2/scripts"; cp $K/run_checks_pc.ps1 "$TMP/tree2/win/kit2/"; echo '{ not json' > "$TMP/tree2/scripts/redaction_patterns.json"
expect runner.a_corrupt_pattern_file_fails_closed 2 -m 'REDACTION PATTERNS UNAVAILABLE' -- $PWSH -NoProfile -File "$TMP/tree2/win/kit2/run_checks_pc.ps1" -TestFixture "$RW/cp_raw_clean.json" -Out "$TMP/tree2/out.json"
mkdir -p "$TMP/tree3/win/kit2" "$TMP/tree3/scripts"; cp $K/run_checks_pc.ps1 "$TMP/tree3/win/kit2/"; echo '{"categories":[{"id":"email","regex":"x","scope":"both"}]}' > "$TMP/tree3/scripts/redaction_patterns.json"
expect runner.a_pattern_file_lacking_required_categories_fails_closed 2 -m 'lacks the category' -- $PWSH -NoProfile -File "$TMP/tree3/win/kit2/run_checks_pc.ps1" -TestFixture "$RW/cp_raw_clean.json" -Out "$TMP/tree3/out.json"
check runner.contains_no_private_identifying_data_regex $( (! grep -nE '\[A-Za-z0-9\._%\+-\]\+@|\\d\{1,3\}\\\.\\d\{1,3\}|\(\?:\[0-9A-Fa-f\]\{2\}[:-]\)|[0-9a-fA-F]\{8\}-' $K/run_checks_pc.ps1 $K/archive_init.ps1 $K/archive_verify.ps1 $K/kenburns_24.ps1 $K/kenburns_24.py $K/pc_helpers.py >/dev/null) && echo 0 || echo 1) "no e-mail, IPv4, MAC or GUID expression in win/kit2: the one pattern file is the only definition"

# ================================================================== quoting of arguments (Quote-Arg and Invoke-Tool, tested on .NET here)
$PY - "$K/run_checks_pc.ps1" "$TMP/psfuncs.ps1" <<'PYEOF'
import re, sys
src = open(sys.argv[1]).read()
out = []
for name in ("Quote-Arg", "Invoke-Tool"):
    m = re.search(r"^function %s\b.*?\n\}\n" % re.escape(name), src, re.S | re.M)
    out.append(m.group(0))
open(sys.argv[2], "w").write("\n".join(out))
PYEOF
cat > "$TMP/argdump.ps1" <<'PSEOF'
foreach ($a in $args) { Write-Output ('[' + $a + ']') }
PSEOF
cat > "$TMP/quote_test.ps1" <<PSEOF
. '$TMP/psfuncs.ps1'
\$cases = @('plain', 'two words', 'quote"inside', 'trailing backslash\\', 'C:\\dir with space\\', 'both "q" and \\ b', '', 'tab	tab')
\$r = Invoke-Tool '$PWSH' (@('-NoProfile', '-File', '$TMP/argdump.ps1') + \$cases) 60
\$got = @(\$r.stdout -split "\`n" | ForEach-Object { \$_.TrimEnd("\`r") } | Where-Object { \$_ -ne '' })
\$want = @(\$cases | ForEach-Object { '[' + \$_ + ']' })
\$bad = 0
for (\$i = 0; \$i -lt \$want.Count; \$i++) { if (\$got[\$i] -ne \$want[\$i]) { \$bad++; Write-Output ('DIFF want ' + \$want[\$i] + ' got ' + \$got[\$i]) } }
Write-Output ('cases ' + \$want.Count + ' lines ' + \$got.Count + ' bad ' + \$bad + ' exit ' + \$r.exit)
PSEOF
expect quoting.arguments_with_spaces_quotes_and_backslashes_round_trip 0 -m 'cases 8 lines 7 bad 0 exit 0|cases 8 lines 8 bad 0 exit 0' -n 'DIFF' -- $PWSH -NoProfile -File "$TMP/quote_test.ps1"
cat > "$TMP/quote2.ps1" <<PSEOF
. '$TMP/psfuncs.ps1'
\$t = Invoke-Tool '$PWSH' @('-NoProfile', '-Command', 'Start-Sleep -Seconds 30') 2
Write-Output ('timedout ' + \$t.timedout)
\$t2 = Invoke-Tool '/no/such/program' @('x') 5
Write-Output ('missing ok=' + \$t2.ok)
PSEOF
expect quoting.a_run_over_its_time_limit_is_killed_and_a_missing_program_is_reported 0 -m 'timedout True' -m 'missing ok=False' -- $PWSH -NoProfile -File "$TMP/quote2.ps1"

}

sec_wrappers() {
# ================================================================== the wrappers' error paths (a PATH without Python, without ffmpeg, without Pillow)
mkdir -p "$TMP/fb_nopil" "$TMP/fb_pyonly" "$TMP/fb_empty"
REALPY="$(command -v python3)"
printf '#!/bin/sh\nexec %s -S "$@"\n' "$REALPY" > "$TMP/fb_nopil/python3"; chmod +x "$TMP/fb_nopil/python3"   # -S hides every site-packages folder: Pillow and numpy are really missing
ln -sf "$REALPY" "$TMP/fb_pyonly/python3"
printf 'a\n' > "$TMP/a.png"; cp "$TMP/a.png" "$TMP/b.png"
expect wrapper.kenburns_without_stills_is_exit_2 2 -m 'Give at least two stills' -m 'files written: none' -- $PWSH -NoProfile -File $K/kenburns_24.ps1
expect wrapper.kenburns_with_a_missing_still_is_exit_2 2 -m 'was not found' -- $PWSH -NoProfile -File $K/kenburns_24.ps1 "$TMP/a.png" "$TMP/nope.png"
expect wrapper.kenburns_selftest_with_stills_is_exit_2 2 -m 'makes its own stills' -- $PWSH -NoProfile -File $K/kenburns_24.ps1 -Selftest "$TMP/a.png" "$TMP/b.png"
expect wrapper.kenburns_without_python_is_exit_3_with_the_install_hint 3 -m 'Python 3 is needed' -m 'winget id UNVERIFIED' -m 'files written: none' -- env PATH="$TMP/fb_empty" "$PWSH" -NoProfile -File $K/kenburns_24.ps1 "$TMP/a.png" "$TMP/b.png"
expect wrapper.kenburns_without_pillow_is_exit_3_with_the_pip_line 3 -m 'py -3 -m pip install --user pillow numpy' -m 'files written: none' -- env PATH="$TMP/fb_nopil" "$PWSH" -NoProfile -File $K/kenburns_24.ps1 "$TMP/a.png" "$TMP/b.png"
expect wrapper.kenburns_without_ffmpeg_is_exit_3 3 -m 'ffmpeg is needed' -m 'files written: none' -- env PATH="$TMP/fb_pyonly" "$PWSH" -NoProfile -File $K/kenburns_24.ps1 "$TMP/a.png" "$TMP/b.png"
expect wrapper.runner_without_python_is_exit_3_and_writes_nothing 3 -m 'NOT FOUND' -m 'Python 3 is needed' -m 'files written: none' -- env PATH="$TMP/fb_empty" "$PWSH" -NoProfile -File $K/run_checks_pc.ps1 -Out "$TMP/never.json"
expect wrapper.runner_without_ffmpeg_is_exit_3_and_writes_nothing 3 -m 'ffmpeg is needed' -m 'files written: none' -- env PATH="$TMP/fb_pyonly" "$PWSH" -NoProfile -File $K/run_checks_pc.ps1 -Out "$TMP/never.json"
# an unexpected error must come out as scrubbed words and exit 3 (the trap), never as a red error carrying a folder name: a throw is injected before step 1
mkdir -p "$TMP/inj/win/kit2"
for f in archive_init archive_verify kenburns_24 run_checks_pc; do
  $PY - "$K/$f.ps1" "$TMP/inj/win/kit2/$f.ps1" "$FAKE" <<'PYEOF'
import re, sys
src = open(sys.argv[1]).read()
m = re.search(r"^# ---- step 1", src, re.M)
boom = "throw ('boom C:' + [char]92 + 'Users' + [char]92 + '%s' + [char]92 + 'x.txt')\n" % sys.argv[3]
open(sys.argv[2], "w", newline="\n").write(src[:m.start()] + boom + src[m.start():])
PYEOF
  case "$f" in archive_init|archive_verify) XA="-Root $TMP/inj/none";; run_checks_pc) XA="-Out $TMP/inj/none.json";; *) XA="";; esac
  expect wrapper.unexpected_error_in_$f.ps1_is_scrubbed_and_exit_3 3 -m 'FAILED: RuntimeException - boom <path>' -m 'files written' -n "$FAKE" -n 'Users' -- $PWSH -NoProfile -File "$TMP/inj/win/kit2/$f.ps1" $XA
done
check wrapper.refused_runs_wrote_no_file $([ ! -e "$TMP/never.json" ] && echo 0 || echo 1) "no output file from the refused runner runs"

}

# run the sections as parallel workers (they use different folders), then replay their results in a fixed order
replay() {  # replay FILE
  [ -f "$1" ] || return 0
  while IFS=$'\t' read -r st nm ex ac un; do [ -n "$st" ] && record "$nm" "$st" "$ex" "$ac" "$un"; done < "$1"
}
WORKERS="static stale archive runner wrappers"
if [ "${LJ_SERIAL:-0}" = "1" ]; then
  for w in $WORKERS; do ( RECORD_TO="$TMP/w_$w.tsv"; "sec_$w" ); done
else
  for w in $WORKERS; do ( RECORD_TO="$TMP/w_$w.tsv"; W0=$(date +%s); "sec_$w"; [ -n "${LJ_TIMING:-}" ] && echo "worker $w: $(( $(date +%s) - W0 )) s" >&2 ) & done
fi
wait
for w in $WORKERS; do replay "$TMP/w_$w.tsv"; done

# ================================================================== Ken Burns geometry, loading, refusals, small render (in-process and CLI)
KBRC="$(grep '^RC=' "$KBOUT" | tail -1 | cut -d= -f2)"
while IFS= read -r line; do
  case "$line" in
    PASS\ *|FAIL\ *|SKIPPED\ *|UNVERIFIED\ *|BLOCKED\ *)
      st="${line%% *}"; rest="${line#* }"; nm="${rest%% | *}"; dt="${rest#* | }"
      record "$nm" "$st" "see kb_checks.py" "$dt";;
  esac
done < "$KBOUT"
check kb_checks.exit_code $([ "${KBRC:-1}" = "0" ] && echo 0 || echo 1) "tests/win_kit2/kb_checks.py $MODE exited ${KBRC:-?}"

# ================================================================== the Windows-only claims, listed (never passed)
record windows.ps1_scripts_on_windows_powershell_5_1 UNVERIFIED "the scripts run on Windows PowerShell 5.1" "parsed on PowerShell 7.5.4 and linted for 5.1 syntax; nothing ran on Windows" "no Windows host here (build plan 4.7)"
record windows.py_launcher_and_python_store_stub UNVERIFIED "Find-Python finds py -3 and rejects the Microsoft Store stub" "the stub check is a text match on 'Python 3.x'; tested here with python3 and a fake python only" "no Windows host"
record windows.temp_folder_and_unexpanded_paths UNVERIFIED "%TEMP% is the default for the raw file and is printed unexpanded" "Show-Path logic exercised on Linux; the %TEMP% default on a managed PC is unknown" "no Windows host"
record windows.argument_quoting_for_processes UNVERIFIED "Quote-Arg follows the CommandLineToArgvW rules on Windows" "round trip proven on .NET on Linux, which parses Arguments by the same rules" "no Windows host"
record windows.winget_ids_and_pip_wheels UNVERIFIED "winget ids Gyan.FFmpeg and Python.Python.3.13 exist; Pillow and numpy install as wheels" "ids read from winget manifests on 2026-10-18; never run" "no Windows host"
record windows.ffmpeg_9_0_2_pixels_and_spec UNVERIFIED "the project chains and the online profile pass on ffmpeg 9.0.2" "measured on 6.1.1 only; the maker's run of run_checks_pc.ps1 is the test" "only ffmpeg 6.1.1 here"
record windows.tiff_standins_open_in_windows_photos UNVERIFIED "the 16-bit stand-in TIFFs open in Windows apps" "valid per ImageMagick and Pillow; no Windows viewer here" "no Windows host"

if [ "$MODE" = "--all" ]; then
  . "$T/all_part.sh"
fi

T1=$(date +%s)
echo
echo "WP-09 ${MODE#--}: PASS=$NPASS FAIL=$NFAIL UNVERIFIED=$NUNV SKIPPED=$NSKIP BLOCKED=$NBLOCK ($((T1-T0)) s)  disk: start ${START_MB} MB, min ${MIN_MB} MB, end $(avail_mb) MB"
printf '{"package":"WP-09","mode":"%s","pass":%d,"fail":%d,"unverified":%d,"skipped":%d,"blocked":%d,"seconds":%d,"avail_mb_start":%d,"avail_mb_min":%d,"avail_mb_end":%d}\n' "${MODE#--}" "$NPASS" "$NFAIL" "$NUNV" "$NSKIP" "$NBLOCK" "$((T1-T0))" "$START_MB" "$MIN_MB" "$(avail_mb)" > "$EVID/summary_${MODE#--}.json"
[ "$NBLOCK" -gt 0 ] && exit 3
[ "$NFAIL" -gt 0 ] && exit 1
exit 0
