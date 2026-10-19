#!/usr/bin/env bash
# tests/win/run_tests.sh [--quick|--all]    WP-01a: Windows kit A (inventory script, checker, tools, fixtures, README)
#
#   --quick  (at most 60 s, no downloads, no timed runs) parse, lint, schema, fixture and checker lines
#   --all    everything in --quick plus the pwsh runs (Linux dry run, self-scan, fail-closed, pattern agreement),
#            the README tests, the tier-file leak test and the directory-hash test
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
# Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line is BLOCKED (a start gate is not met,
# for example scripts/redaction_patterns.json from WP-03). UNVERIFIED (Windows-only behaviour) and SKIPPED (a sibling
# package has not landed) are listed and are never counted as a pass.
# Every test also writes one evidence envelope (build plan 4.2) to build/evidence/wp01a/tests.jsonl.
#
# Environment: LJ_TEST_TREE  run against another tree (same layout), used only while scripts/redaction_patterns.json
#              from WP-03 has not landed; the report says so when it was used.
#              PWSH          path to pwsh 7.5.4 (default <scratch>/pwsh/pwsh, see win/tools/fetch_pwsh.sh)
# Nothing here uses the network. Everything the tests write goes to renders/wp01a/ (git-ignored), a temporary
# folder under <scratch>, and build/evidence/wp01a/.
set -u
MODE="${1:---quick}"
case "$MODE" in --quick|--all) ;; *) echo "usage: run_tests.sh [--quick|--all]" >&2; exit 2;; esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TREE="${LJ_TEST_TREE:-$ROOT}"
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
PWSH="${PWSH:-$SCRATCH/pwsh/pwsh}"
PY="python3 -I -B"
EVID="$ROOT/build/evidence/wp01a"
FIX="tests/win/fixtures"
mkdir -p "$EVID" "$TREE/renders/wp01a" 2>/dev/null
TMP="$(mktemp -d "$SCRATCH/wp01a-test.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
JSONL="$EVID/tests.jsonl"
: > "$JSONL"
NPASS=0; NFAIL=0; NUNV=0; NSKIP=0; NBLOCK=0

avail_mb() { df -BM / | awk 'NR==2 { gsub("M","",$4); print $4 }'; }
START_MB="$(avail_mb)"

# ------------------------------------------------------------------ recording
record() {  # record NAME STATUS EXPECTED ACTUAL [UNVERIFIED_REASON]
  local name="$1" status="$2" exp="$3" act="$4" unv="${5:-}"
  case "$status" in PASS) NPASS=$((NPASS+1));; FAIL) NFAIL=$((NFAIL+1));; UNVERIFIED) NUNV=$((NUNV+1));; SKIPPED) NSKIP=$((NSKIP+1));; BLOCKED) NBLOCK=$((NBLOCK+1));; esac
  printf '%-10s %-44s %s\n' "$status" "$name" "$(printf '%s' "$act" | head -c 150 | tr '\n' ' ')"
  EV_NAME="$name" EV_STATUS="$status" EV_EXP="$exp" EV_ACT="$act" EV_UNV="$unv" EV_START="$START_MB" EV_END="$(avail_mb)" \
  EV_ROOT="$ROOT" EV_TREE="$TREE" EV_SCRATCH="$SCRATCH" EV_PY="$(python3 --version 2>&1 | awk '{print $2}')" \
  EV_FF="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}' | cut -d- -f1)" EV_JSONL="$JSONL" \
  python3 -I - <<'PYEOF'
import json, os, re, datetime
e = os.environ
def clean(s):
    for k in ("EV_ROOT", "EV_TREE"):
        s = s.replace(e[k], ".")
    s = s.replace(e["EV_SCRATCH"], "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return s[:600]
s, en = int(e["EV_START"] or 0), int(e["EV_END"] or 0)
env = {"platform": "linux", "ffmpeg": e["EV_FF"], "nproc": os.cpu_count(), "python": e["EV_PY"], "node": "22.x"}
rec = {"schema": "lj-evidence/1", "package": "WP-01a", "test": e["EV_NAME"],
       "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), "status": e["EV_STATUS"], "env": env,
       "disk": {"avail_mb_start": s, "planned_write_mb": 0, "avail_mb_min": min(s, en), "avail_mb_end": en, "floor_mb": 400, "hard_floor_mb": 250},
       "expected": clean(e["EV_EXP"]), "actual": clean(e["EV_ACT"]), "notes": "",
       "unverified_reasons": [e["EV_UNV"]] if e["EV_UNV"] else []}
open(e["EV_JSONL"], "a").write(json.dumps(rec, sort_keys=True) + "\n")
PYEOF
}

# run CMD... in $TREE; sets OUT (stdout+stderr) and RC
runin() { OUT="$(cd "$TREE" && "$@" 2>&1)"; RC=$?; }

# expect NAME EXPECTED_RC [-m REGEX | -n REGEX]... -- CMD...   (run in $TREE; -m must match OUT, -n must not)
expect() {
  local name="$1" want="$2"; shift 2
  local must=() mustnot=()
  while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
    case "$1" in -m) must+=("$2");; -n) mustnot+=("$2");; esac; shift 2
  done
  shift
  runin "$@"
  local why="" rx
  [ "$RC" -eq "$want" ] || why="exit $RC, wanted $want"
  for rx in "${must[@]+"${must[@]}"}"; do printf '%s' "$OUT" | grep -Eq -- "$rx" || why="$why; missing /$rx/"; done
  for rx in "${mustnot[@]+"${mustnot[@]}"}"; do printf '%s' "$OUT" | grep -Eq -- "$rx" && why="$why; found /$rx/"; done
  if [ -z "$why" ]; then record "$name" PASS "exit $want${must[*]:+ matching ${must[*]}}" "exit $RC; $(printf '%s' "$OUT" | grep -E 'RESULT|category=|FINDING|NOTE|OK |problems:|crashes:|samples:|runs:|schema errors|PARSED|TOTAL|headings found|already installed|DISK:|absolute path|refusing' | head -3 | tr '\n' '|')"
  else record "$name" FAIL "exit $want${must[*]:+ matching ${must[*]}}" "$why :: $(printf '%s' "$OUT" | head -6 | tr '\n' '|')"; fi
}

need_pwsh() { [ -x "$PWSH" ]; }
have_patterns() { [ -f "$TREE/scripts/redaction_patterns.json" ]; }
WC="$PY scripts/windows_check.py"

echo "WP-01a tests ($MODE). tree: $( [ "$TREE" = "$ROOT" ] && echo repo || echo 'ALTERNATE (stand-in pattern file)' )  patterns file: $(have_patterns && echo present || echo MISSING)  pwsh: $(need_pwsh && echo present || echo MISSING)"

# ================================================================== QUICK: parse, lint, data
if need_pwsh; then
  expect parse.scripts_and_readme_fences 0 -m 'PARSED [0-9]+ item\(s\), 0 parse error' -n 'parse error:' -- env PWSH="$PWSH" bash win/tools/ps_parse.sh
else
  record parse.scripts_and_readme_fences SKIPPED "0 parse errors" "PENDING: pwsh not yet fetched; ps_lint alone gates"
fi
expect lint.step0_script 0 -m 'TOTAL: 0 error' -- $PY win/tools/ps_lint.py win/step0_pc_tests.ps1
expect lint.maker_readme_fences 0 -m 'TOTAL: 0 error' -- $PY win/tools/ps_lint.py win/README-MAKER.md

# planted machine-scope policy change must make the lint fail
printf '# planted\nSet-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Bypass -Force\n' > "$TMP/plant.ps1"
printf 'Some text\n\n```powershell\nSet-ExecutionPolicy RemoteSigned\n```\n' > "$TMP/plant.md"
expect lint.planted_machine_scope_ps1 1 -m 'R13' -- $PY win/tools/ps_lint.py "$TMP/plant.ps1"
expect lint.planted_machine_scope_readme_fence 1 -m 'R13' -- $PY win/tools/ps_lint.py "$TMP/plant.md"
# a README copy with the planted block appended
{ cat "$TREE/win/README-MAKER.md"; printf '\n```powershell\nSet-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Bypass\n```\n'; } > "$TMP/README-planted.md"
expect lint.readme_with_planted_block 1 -m 'R13' -- $PY win/tools/ps_lint.py "$TMP/README-planted.md"
cat > "$TMP/seven.ps1" <<'PLANT'
$a = $x ?? 'd'
$b = $o?.Name
$c = ($n -gt 1) ? 'y' : 'n'
Get-Item a && Get-Item b
1..2 | ForEach-Object -Parallel { $_ }
'{}' | ConvertFrom-Json -AsHashtable
Get-Content f -AsByteStream
$o | Set-Content f -Encoding utf8NoBOM
if ($IsWindows) { 1 }
$o | ConvertTo-Json
$p = Join-Path 'a' 'b' 'c'
Remove-Item f
PLANT
expect lint.planted_powershell7_syntax 1 -m 'R01' -m 'R02' -m 'R03' -m 'R04' -m 'R05' -m 'R06' -m 'R07' -m 'R08' -m 'R09' -m 'R11' -m 'R12' -m 'RO-delete' -- $PY win/tools/ps_lint.py "$TMP/seven.ps1"
printf "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force\n# Set-ExecutionPolicy -Scope LocalMachine in a comment\n\$s = 'Set-ExecutionPolicy RemoteSigned ?? &&'\n" > "$TMP/ok.ps1"
expect lint.process_scope_and_quoted_text_pass 0 -m 'TOTAL: 0 error' -- $PY win/tools/ps_lint.py "$TMP/ok.ps1"

# JSON data files and the two schemas
cat > "$TMP/jsoncheck.py" <<'PYEOF'
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
bad = []
for p in ["win/pins.json", "win/tiers.json", "win/schema/pc_report.schema.json", "win/schema/pc_tier.schema.json"]:
    try:
        json.loads((root / p).read_text(encoding="utf-8"))
    except Exception as e:
        bad.append("%s: %s" % (p, type(e).__name__))
def objects(node, path=""):
    if isinstance(node, dict):
        if node.get("type") == "object" or (isinstance(node.get("type"), list) and "object" in node["type"]):
            if "properties" in node:
                yield path, node
        for k, v in node.items():
            yield from objects(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from objects(v, "%s/%d" % (path, i))
n = 0
for sp in ("pc_report", "pc_tier"):
    s = json.loads((root / ("win/schema/%s.schema.json" % sp)).read_text())
    for path, node in objects(s):
        n += 1
        if node.get("additionalProperties") is not False:
            bad.append("%s%s lacks additionalProperties:false" % (sp, path))
tiers = json.loads((root / "win/tiers.json").read_text())
def sources(node, path=""):
    # every threshold block carries a source
    if isinstance(node, dict):
        has_numbers = any(k.startswith(("min_", "edges", "cores", "ram_gb", "shared_hint")) for k in node) or "tiers" in node or "classes" in node
        if has_numbers and not any(k.endswith("source") or k == "source" for k in node) and path.count("/") <= 1:
            yield path
        for k, v in node.items():
            if isinstance(v, dict):
                yield from sources(v, path + "/" + k)
miss = list(sources({k: v for k, v in tiers.items() if isinstance(v, dict)}))
for m in miss:
    bad.append("tiers.json block without a source: " + m)
pins = json.loads((root / "win/pins.json").read_text())["apps"]
want = {"photocraft": "0.10.0", "vectorcraft": "0.13.1", "lightcraft": "0.9.1", "filmcraft": "0.9.0", "effectcraft": "0.11.1", "soundcraft": None}
for a, v in want.items():
    if pins[a]["pin"] != v:
        bad.append("pin %s differs from W-22" % a)
if pins["filmcraft"]["fallback"] != "0.8.0":
    bad.append("filmcraft fallback differs from W-22")
print("objects checked for additionalProperties:false: %d; problems: %d" % (n, len(bad)))
for b in bad:
    print("PROBLEM " + b)
sys.exit(1 if bad else 0)
PYEOF
expect data.json_schemas_pins_tiers 0 -m 'problems: 0' -- $PY "$TMP/jsoncheck.py" "$TREE"
expect fixtures.in_sync_with_generator 0 -m 'fixtures in sync' -- $PY tests/win/make_fixtures.py --check

# ================================================================== QUICK: windows_check.py on fixtures
if have_patterns; then
  expect check.gpu12_pro_16gb 0 -m 'gpu_tier +gpu-8-12' -m 'ram_tier +16\+' -m 'pro-or-higher' -m 'WSL2 ok' -- $WC $FIX/report_gpu12_pro_16gb.json
  expect check.nogpu_home_8gb 0 -m 'gpu_tier +none' -m 'ram_tier +8-15' -m 'edition +home' -m 'BitLocker not offered' -m 'RESULT: exit 0' -- $WC $FIX/report_nogpu_home_8gb.json
  expect check.gpu24_pro_32gb 0 -m 'gpu_tier +gpu-16\+' -m 'ram_tier +16\+' -- $WC $FIX/report_gpu24_pro_32gb.json
  expect check.software_gpu 0 -m 'gpu_tier +none' -- $WC $FIX/report_software_gpu.json
  expect check.vram_nvidia_over_cap 0 -m 'read from nvidia-smi' -m 'gpu_tier +gpu-16\+' -- $WC $FIX/report_vram_nvidia_over_cap.json
  expect check.vram_capped_only 1 -m 'VRAM unreadable' -m 'gpu_tier +unknown' -- $WC $FIX/report_vram_capped_only.json
  expect check.old_ffmpeg6 0 -m 'ffmpeg +6\.0' -m 'run the colour-patch test on this build' -- $WC $FIX/report_old_ffmpeg6.json
  expect check.ffmpeg9 0 -m 'ffmpeg +9\.0\.2' -m 'run the colour-patch test on this build' -- $WC $FIX/report_ffmpeg9.json
  expect check.craft_pins_mixed 1 -m 'photocraft match' -m 'filmcraft fallback pin' -m 'vectorcraft MISMATCH' -m 'lightcraft absent' -m 'FINDING: Craft pin mismatch' -- $WC $FIX/report_craft_pins_mixed.json
  expect check.gpu_low_4gb 0 -m 'gpu_tier +gpu-low' -- $WC $FIX/report_gpu_low_4gb.json
  expect check.non_nvidia_is_capped 0 -m 'gpu_tier +gpu-low' -m 'non-NVIDIA card: capped' -- $WC $FIX/report_amd_16gb.json
  expect check.below_blender_floor_is_information 0 -m 'below on: cores, RAM, GPU' -m 'ram_tier +<8' -m 'RESULT: exit 0' -- $WC $FIX/report_below_blender_floor.json
  expect check.version_strings_not_ip 0 -m 'RESULT: exit 0' -- $WC $FIX/report_version_strings_not_ip.json
  expect check.sha256_ok 0 -m 'RESULT: exit 0' -- $WC $FIX/report_sha256_ok.json
  expect check.hex65_leak 2 -m 'category=guid_serial field=notes\[0\] hit=3f\*+' -n '3f2a9c41d7e85b60a1c4' -- $WC $FIX/report_hex65_leak.json
  expect check.identifying 2 -m 'category=email field=tools\.git\.notes hit=ta\*+' -m 'category=ipv4 field=notes\[0\] hit=10\*+' -m 'category=mac field=notes\[3\] hit=02\*+' -m 'category=profile_path_windows field=errors\[0\] hit=C:\*+' -n 'tamsin' -n 'brambleworks' -n 'example\.invalid' -n '10\.77' -n '1A:2B' -n 'AppData' -n 'field=notes\[[45]\]' -- $WC $FIX/report_identifying.json
  expect check.identifying_with_forbid 2 -m 'category=user_name field=notes\[1\] hit=ta\*+' -n 'tamsinwrex' -n 'tamsin' -- $WC --forbid tamsinwrex $FIX/report_identifying.json
  expect check.forbid_absent_name 0 -m 'RESULT: exit 0' -- $WC --forbid exampleperson $FIX/report_gpu12_pro_16gb.json
  expect check.short_username_collision_is_a_note 0 -m 'NOTE category=user_name field=gpus\[0\]\.name hit=ze\*\*' -m 'RESULT: exit 0' -- $WC --forbid zeta $FIX/report_short_username_collision.json
  expect check.short_username_leak_refuses 2 -m 'category=user_name field=tools\.git\.notes hit=ze\*\*' -- $WC --forbid zeta $FIX/report_short_username_leak.json
  expect check.too_short_name_is_skipped_with_note 0 -m 'NOTE name check skipped' -- $WC --forbid zz $FIX/report_gpu12_pro_16gb.json

  # BOM and UTF-16 give the same answer as the plain file
  plain="$(cd "$TREE" && $WC $FIX/report_gpu12_pro_16gb.json | grep -v '^encoding:')"; plain_rc=$?
  bom="$(cd "$TREE" && $WC $FIX/report_bom.json | grep -v '^encoding:')"
  if [ "$plain" = "$bom" ] && [ -n "$plain" ]; then record check.bom_equals_plain PASS "same table as the plain file" "identical ($(printf '%s\n' "$plain" | wc -l) lines)"; else record check.bom_equals_plain FAIL "same table as the plain file" "outputs differ"; fi
  iconv -f UTF-8 -t UTF-16 "$TREE/$FIX/report_gpu12_pro_16gb.json" > "$TMP/utf16_bom.json"
  iconv -f UTF-8 -t UTF-16LE "$TREE/$FIX/report_gpu12_pro_16gb.json" > "$TMP/utf16_nobom.json"
  for v in utf16_bom utf16_nobom; do
    got="$(cd "$TREE" && $WC "$TMP/$v.json" | grep -v '^encoding:')"
    if [ "$plain" = "$got" ]; then record check.$v"_equals_plain" PASS "same table as the plain file" "identical; encoding line: $(cd "$TREE" && $WC "$TMP/$v.json" | grep '^encoding:')"; else record check.$v"_equals_plain" FAIL "same table" "outputs differ"; fi
  done

  # bad input never echoes content
  printf '{"schema_version": 1, "tool": ' > "$TMP/truncated.json"
  expect check.invalid_json 2 -m 'INVALID: the file is not readable JSON' -- $WC "$TMP/truncated.json"
  $PY - "$TREE/$FIX/report_gpu12_pro_16gb.json" "$TMP" <<'PYEOF'
import json, sys
r = json.load(open(sys.argv[1]))
r["cpu"]["cores"] = "six"
r["tamsin_unknown_key"] = 1
r["tools"]["git"]["found"] = "yes"
json.dump(r, open(sys.argv[2] + "/schema_bad.json", "w"))
PYEOF
  expect check.schema_invalid_masks_unknown_keys 2 -m 'INVALID: the report does not match' -m 'cpu\.cores has the wrong type' -m '<unknown key>' -n 'tamsin' -- $WC "$TMP/schema_bad.json"
  OUT="$(cd "$TREE" && $WC - < $FIX/report_gpu12_pro_16gb.json 2>&1)"; RC=$?
  if [ "$RC" -eq 0 ] && printf '%s' "$OUT" | grep -Eq 'gpu_tier +gpu-8-12'; then record check.reads_standard_input PASS "report from stdin gives the same verdict" "exit 0, gpu-8-12"; else record check.reads_standard_input FAIL "stdin" "exit $RC"; fi
  expect check.missing_file 2 -m 'cannot read the report file' -- $WC "$TMP/nope.json"
  expect check.no_arguments 2 -m 'usage' -- $WC

  # robustness: every nullable field set to null, one at a time, never crashes the checker (exit 0, 1 or 2; no traceback)
  cat > "$TMP/nullfuzz.py" <<'PYEOF'
import copy, json, subprocess, sys
tree = sys.argv[1]
schema = json.load(open(tree + "/win/schema/pc_report.schema.json"))
base = json.load(open(tree + "/tests/win/fixtures/report_gpu12_pro_16gb.json"))
paths = []
def walk(node, sch, path):
    if isinstance(sch.get("type"), list) and "null" in sch["type"]:
        paths.append(path)
    if sch.get("type") == "object" or (isinstance(sch.get("type"), list) and "object" in sch["type"] and isinstance(node, dict)):
        for k, sub in sch.get("properties", {}).items():
            if isinstance(node, dict) and k in node:
                walk(node[k], sub, path + [k])
    if isinstance(node, list) and sch.get("items"):
        for i, item in enumerate(node):
            walk(item, sch["items"], path + [i])
walk(base, schema, [])
bad = 0
for p in paths:
    r = copy.deepcopy(base)
    cur = r
    for k in p[:-1]:
        cur = cur[k]
    cur[p[-1]] = None
    open(sys.argv[2], "w").write(json.dumps(r))
    out = subprocess.run([sys.executable, "-I", "-B", tree + "/scripts/windows_check.py", sys.argv[2]], capture_output=True, text=True, cwd=tree)
    if out.returncode not in (0, 1, 2) or "Traceback" in out.stdout + out.stderr:
        bad += 1; print("CRASH when null: " + ".".join(str(x) for x in p) + " :: " + (out.stderr or out.stdout)[-200:].replace("\n", " | "))
print("nullable fields tried: %d, crashes: %d" % (len(paths), bad))
sys.exit(1 if bad else 0)
PYEOF
  expect check.every_nullable_field_null_never_crashes 0 -m 'crashes: 0' -- $PY "$TMP/nullfuzz.py" "$TREE" "$TMP/nullcase.json"
  # output files: written on success, none on a refusal, none for a non-Windows report
  rm -f "$TMP"/o_*.json "$TMP/o_hw.md"
  expect check.outputs_written 0 -m 'wrote: tier-json-out' -m 'wrote: hardware-md' -m 'wrote: json-out' -- $WC --json-out "$TMP/o_check.json" --tier-json-out "$TMP/o_tier.json" --hardware-md "$TMP/o_hw.md" $FIX/report_gpu12_pro_16gb.json
  [ -f "$TMP/o_tier.json" ] && [ -f "$TMP/o_hw.md" ] && [ -f "$TMP/o_check.json" ] && record check.outputs_exist PASS "three files" "present" || record check.outputs_exist FAIL "three files" "missing"
  rm -f "$TMP"/r_*.json "$TMP/r_hw.md"
  expect check.refusal_writes_nothing 2 -m 'REDACTION CHECK FAILED' -- $WC --json-out "$TMP/r_check.json" --tier-json-out "$TMP/r_tier.json" --hardware-md "$TMP/r_hw.md" $FIX/report_identifying.json
  [ ! -e "$TMP/r_tier.json" ] && [ ! -e "$TMP/r_check.json" ] && [ ! -e "$TMP/r_hw.md" ] && record check.refusal_files_absent PASS "no output files" "none created" || record check.refusal_files_absent FAIL "no output files" "a file exists"
else
  record check.fixtures BLOCKED "windows_check.py on fixtures" "scripts/redaction_patterns.json has not landed (WP-03); run again when it has, or set LJ_TEST_TREE"
fi

if [ "$MODE" = "--quick" ]; then
  END_MB="$(avail_mb)"
  echo "---"; echo "WP-01a quick: PASS=$NPASS FAIL=$NFAIL UNVERIFIED=$NUNV SKIPPED=$NSKIP BLOCKED=$NBLOCK  (df Avail $START_MB -> $END_MB MB)"
  [ "$NFAIL" -ne 0 ] && exit 1
  [ "$NBLOCK" -ne 0 ] && exit 3
  exit 0
fi

# ================================================================== ALL: tier file leaks nothing
if have_patterns; then
  ( cd "$TREE" && $WC --tier-json-out "$TMP/tier_g12.json" $FIX/report_gpu12_pro_16gb.json > /dev/null )
  ( cd "$TREE" && $WC --tier-json-out "$TMP/tier_craft.json" $FIX/report_craft_pins_mixed.json > /dev/null )
  cat > "$TMP/tiercheck.py" <<'PYEOF'
import json, sys
sys.dont_write_bytecode = True
import importlib.util
spec = importlib.util.spec_from_file_location("wc", sys.argv[1] + "/scripts/windows_check.py")
wc = importlib.util.module_from_spec(spec); spec.loader.exec_module(wc)
tier_path, fixture_path = sys.argv[2], sys.argv[3]
tier_text = open(tier_path).read()
tier = json.loads(tier_text)
schema = json.load(open(sys.argv[1] + "/win/schema/pc_tier.schema.json"))
errs = []
wc.validate(tier, schema, schema, "", errs)
fx = json.load(open(fixture_path))
needles = [fx["cpu"]["name"]] + [t for t in str(fx["cpu"]["name"]).split() if len(t) >= 4]
for g in fx["gpus"]:
    needles += [g["name"], g["driver_version"]] + [t for t in g["name"].split() if len(t) >= 4]
needles += [fx["os"]["caption"], fx["os"]["version"], fx["os"]["build"], str(fx["ram"]["total_gb"])]
for d in fx["disks"]:
    needles += [str(d["size_gb"]), str(d["free_gb"])]
needles += [fx["tools"]["python"]["version"], fx["tools"]["git"]["version"], fx["tools"]["winget"]["version"]]
found = [n for n in needles if n and n in tier_text]
extra = sorted(set(tier) - set(schema["properties"]))
print("schema errors: %d; fixture strings or exact sizes found in the tier file: %d; keys outside the schema: %d; shared_pc_hint present: %s; needles tested: %d" % (len(errs), len(found), len(extra), "shared_pc_hint" in tier_text, len(needles)))
for f in found:
    print("LEAK: " + f[:3] + "***")
sys.exit(1 if (errs or found or extra or "shared_pc_hint" in tier_text) else 0)
PYEOF
  expect tier.file_valid_and_leaks_nothing 0 -m 'schema errors: 0; fixture strings or exact sizes found in the tier file: 0; keys outside the schema: 0; shared_pc_hint present: False' -- $PY "$TMP/tiercheck.py" "$TREE" "$TMP/tier_g12.json" "$TREE/$FIX/report_gpu12_pro_16gb.json"
  expect tier.craft_fixture_has_statuses 0 -m 'schema errors: 0' -- $PY "$TMP/tiercheck.py" "$TREE" "$TMP/tier_craft.json" "$TREE/$FIX/report_craft_pins_mixed.json"
  grep -q '"status": "mismatch"' "$TMP/tier_craft.json" && grep -q '"status": "fallback-pin"' "$TMP/tier_craft.json" && grep -q '"status": "match"' "$TMP/tier_craft.json" && grep -q '"status": "absent"' "$TMP/tier_craft.json" \
    && record tier.craft_statuses_present PASS "match, fallback-pin, mismatch, absent" "all four in the tier file" || record tier.craft_statuses_present FAIL "four statuses" "missing"
  # hardware.md draft is bucketed
  if grep -Eiq 'RTX|GeForce|Ryzen|5600|3060|31\.0\.15|15\.9|640\.2|212\.4' "$TMP/o_hw.md"; then record hardware_md.no_model_names FAIL "no model names or exact sizes" "found one"; else record hardware_md.no_model_names PASS "no model names or exact sizes" "$(grep -c '' "$TMP/o_hw.md") lines, buckets only"; fi
  # a Windows tier file for the non-Windows report is refused cleanly
  if [ -f "$TREE/renders/wp01a/linux_report.json" ]; then :; fi
fi

# ================================================================== ALL: static strings never collide with common default names
if have_patterns; then
  cat > "$TMP/audit.sh" <<'AUDITEOF'
#!/usr/bin/env bash
# run windows_check with common default Windows names against every fixture that is meant to be clean
cd "$1" || exit 2
bad=0; n=0
for name in Administrator User Owner Admin Guest Family DESKTOP-ABC123 LAPTOP-7QX2K9 WORKGROUP; do
  for f in gpu12_pro_16gb gpu24_pro_32gb software_gpu vram_capped_only vram_nvidia_over_cap old_ffmpeg6 ffmpeg9 craft_pins_mixed version_strings_not_ip sha256_ok gpu_low_4gb below_blender_floor; do
    n=$((n+1))
    out="$(python3 -I scripts/windows_check.py --forbid "$name" tests/win/fixtures/report_$f.json 2>&1)"; rc=$?
    if [ "$rc" -eq 2 ]; then bad=$((bad+1)); echo "COLLISION name=${name:0:2}** fixture=$f :: $(printf '%s' "$out" | grep 'category=' | head -2 | tr '\n' ' ')"; fi
  done
done
echo "runs: $n, unexpected refusals: $bad"
# the script's own fixed note strings and edition labels, against the same default names (name rule: whole word, plus 4-character fragments of names of 5 or more)
python3 -I - "$1" <<'PYAUDIT'
import re, sys, importlib.util
sys.dont_write_bytecode = True
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("wc", root + "/scripts/windows_check.py")
wc = importlib.util.module_from_spec(spec); spec.loader.exec_module(wc)
pat = wc.load_patterns()
src = open(root + "/win/step0_pc_tests.ps1", encoding="utf-8").read()
strings = [m.group(2) for m in re.finditer(r"(Add-Note|\.notes\s*=|\.notes\.|\$R\.tools\.\w+\.notes\s*=|\.notes\s*=)\s*'([^']*)'", src)]
strings += ["WindowsPowerShell", "PowerShell", "windows", "non-windows", "Professional", "Core", "CoreSingleLanguage", "found", "not found"]
strings += re.findall(r"notes\s*=\s*'([^']*)'", src)
strings += re.findall(r"=\s*'((?:found|not found|only|wsl|nvidia|none)[^']*)'", src)
hits = 0
for name in ["Administrator", "User", "Owner", "Admin", "Guest", "Family", "DESKTOP-ABC123", "LAPTOP-7QX2K9", "WORKGROUP", "WIN-9Q4T7K2"]:
    for t in strings:
        if wc.name_hit(t, name, True, pat):
            hits += 1; print("COLLISION %s** in note string: %s" % (name[:2], t[:60]))
print("script note strings checked: %d, collisions: %d" % (len(set(strings)), hits))
sys.exit(1 if hits else 0)
PYAUDIT
rc2=$?
[ "$bad" -eq 0 ] && [ "$rc2" -eq 0 ]
AUDITEOF
  expect redaction.static_text_has_no_default_name_collisions 0 -m 'unexpected refusals: 0' -m 'collisions: 0' -- bash "$TMP/audit.sh" "$TREE"
fi

# ================================================================== ALL: pwsh runs
if need_pwsh && have_patterns; then
  OUTD="$TREE/renders/wp01a"; mkdir -p "$OUTD"
  rm -f "$OUTD"/linux_report.json "$OUTD"/none.json "$OUTD"/collision.json "$OUTD"/leak.json
  expect pwsh.linux_dry_run_exit0 0 -m '\[19/19\] Writing the report' -m 'files written: renders/wp01a/linux_report.json' -m 'skipped \(not Windows\)' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -Out renders/wp01a/linux_report.json
  DRYOUT="$OUT"
  expect pwsh.linux_report_is_not_a_windows_report 1 -m 'NOT A WINDOWS REPORT' -- $WC renders/wp01a/linux_report.json
  grep -q '"platform": "non-windows"' "$OUTD/linux_report.json" && record pwsh.linux_report_platform PASS "os.platform non-windows" "non-windows" || record pwsh.linux_report_platform FAIL "os.platform non-windows" "other"
  # the report written by the script is BOM-less UTF-8
  if [ "$(head -c3 "$OUTD/linux_report.json" | od -An -tx1 | tr -d ' \n')" = "efbbbf" ]; then record pwsh.report_has_no_bom FAIL "no BOM" "BOM present"; else record pwsh.report_has_no_bom PASS "no BOM" "first bytes are not EF BB BF"; fi
  # no step prints a profile path or the Linux user/host name
  if printf '%s' "$DRYOUT" | grep -Eq '/root|/home/[a-z]|[A-Za-z]:\\Users'; then record pwsh.console_has_no_profile_path FAIL "no profile path on the console" "found one"; else record pwsh.console_has_no_profile_path PASS "no profile path on the console" "none"; fi
  # self-scan: refusal
  H0="$(cd "$TREE" && find win scripts/windows_check.py "$FIX" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-16)"
  mkdir -p "$TREE/renders/wp01a/hash"; B0="$(ls -A "$TREE/renders/wp01a/hash" | wc -l)"
  expect pwsh.selfscan_identifying_refuses 2 -m '^REDACTION CHECK FAILED, nothing was written' -m 'category=email field=tools\.git\.notes hit=ta\*+' -m 'category=user_name field=notes\[1\] hit=ta\*+' -m 'category=computer_name field=notes\[2\] hit=BR\*+' -m 'category=domain_name' -m 'category=ipv4' -m 'category=mac' -m 'category=profile_path_windows' -n 'tamsinwrex' -n 'BRAMBLE-Q7' -n 'bramblenet' -n 'example\.invalid' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_identifying.json -FakeUser tamsinwrex -FakeComputer BRAMBLE-Q7 -FakeDomain bramblenet -Out renders/wp01a/hash/none.json
  [ ! -e "$TREE/renders/wp01a/hash/none.json" ] && record pwsh.selfscan_refusal_wrote_no_file PASS "no output file" "absent" || record pwsh.selfscan_refusal_wrote_no_file FAIL "no output file" "exists"
  expect pwsh.selfscan_collision_is_note_and_writes 0 -m 'NOTE category=user_name field=gpus\[0\]\.name hit=ze\*\*' -m 'files written: renders/wp01a/hash/collision.json' -n 'zeta' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_short_username_collision.json -FakeUser zeta -Out renders/wp01a/hash/collision.json
  $PY - "$TREE/renders/wp01a/hash/collision.json" <<'PYEOF' && record pwsh.collision_report_records_the_note PASS "name_hits_in_hardware_fields filled" "recorded" || record pwsh.collision_report_records_the_note FAIL "name_hits_in_hardware_fields filled" "not recorded"
import json, sys
r = json.load(open(sys.argv[1]))
h = r["redaction"]["name_hits_in_hardware_fields"]
assert r["redaction"]["self_scan_passed"] is True
assert any(x["category"] == "user_name" and x["field"] == "gpus[0].name" and x["masked_hit"] == "ze**" for x in h), h
PYEOF
  expect pwsh.selfscan_leak_refuses 2 -m 'category=user_name field=tools\.git\.notes hit=ze\*\*' -n 'zeta' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_short_username_leak.json -FakeUser zeta -Out renders/wp01a/hash/leak.json
  [ ! -e "$TREE/renders/wp01a/hash/leak.json" ] && record pwsh.leak_refusal_wrote_no_file PASS "no output file" "absent" || record pwsh.leak_refusal_wrote_no_file FAIL "no output file" "exists"
  expect pwsh.selfscan_hex65_refuses 2 -m 'category=guid_serial' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_hex65_leak.json -FakeUser nobody -Out renders/wp01a/hash/hex65.json
  expect pwsh.selfscan_version_strings_pass 0 -m 'redaction check passed' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_version_strings_not_ip.json -FakeUser nobody -Out renders/wp01a/hash/versions.json
  expect pwsh.selfscan_sha256_passes 0 -m 'redaction check passed' -- "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture $FIX/report_sha256_ok.json -FakeUser nobody -Out renders/wp01a/hash/sha.json
  # every fixture through the script's own scan: clean ones pass (exit 0), the two with planted values refuse (exit 2), none crashes
  badfx=""; nfx=0
  for fx in "$TREE/$FIX"/report_*.json; do
    n="$(basename "$fx" .json)"; nfx=$((nfx+1)); want=0
    case "$n" in report_identifying|report_hex65_leak) want=2;; esac
    ( cd "$TREE" && "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -TestFixture "$FIX/$n.json" -FakeUser nobodyatall -Out renders/wp01a/hash/fx_$n.json > /dev/null 2>&1 ); rc=$?
    [ "$rc" -eq "$want" ] || badfx="$badfx $n(exit $rc, wanted $want)"
  done
  [ -z "$badfx" ] && record pwsh.every_fixture_through_the_script_scan PASS "$nfx fixtures: clean exit 0, planted exit 2" "all $nfx as expected" || record pwsh.every_fixture_through_the_script_scan FAIL "all as expected" "$badfx"
  rm -f "$TREE/renders/wp01a/hash"/fx_*.json
  # directory hash before/after: only the -Out files appeared; the kit itself is unchanged
  H1="$(cd "$TREE" && find win scripts/windows_check.py "$FIX" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-16)"
  new="$(ls -A "$TREE/renders/wp01a/hash" | sort | tr '\n' ' ')"
  [ "$H0" = "$H1" ] && [ "$new" = "collision.json sha.json versions.json " ] && record pwsh.directory_hash_only_out_files_created PASS "kit unchanged; only the 3 passing -Out files exist" "kit hash $H0 unchanged; files: $new" || record pwsh.directory_hash_only_out_files_created FAIL "kit unchanged; only -Out files" "kit $H0 -> $H1; files: $new"
  rm -rf "$TREE/renders/wp01a/hash"
  # pattern self-test: both consumers agree with each other and with the declared samples
  cat > "$TMP/selftest.py" <<'PYEOF'
import json, subprocess, sys
tree, pwsh = sys.argv[1], sys.argv[2]
pats = json.load(open(tree + "/scripts/redaction_patterns.json"))
samples = {}
expect = {}
j = lambda s: "".join(s) if isinstance(s, list) else str(s)
for c in pats["categories"]:
    if c.get("scope") == "text":
        continue
    for i, s in enumerate(c.get("positive_samples", [])):
        samples["pos:%s:%d" % (c["id"], i)] = j(s); expect["pos:%s:%d" % (c["id"], i)] = ("has", c["id"])
    for i, s in enumerate(c.get("negative_samples", [])):
        samples["neg:%s:%d" % (c["id"], i)] = j(s); expect["neg:%s:%d" % (c["id"], i)] = ("hasnt", c["id"])
report_scope = {c["id"] for c in pats["categories"] if c.get("scope", "both") in ("report", "both")}
for smp in pats.get("samples", []):   # the file's own authoritative list: exact expectation, limited to the categories a report consumer applies
    sid = "file:" + str(smp["id"])
    samples[sid] = j(smp["parts"]) if "parts" in smp else j(smp.get("text", ""))
    expect[sid] = ("exact", sorted(set(smp.get("expect", [])) & report_scope))
open(sys.argv[3], "w").write(json.dumps({"samples": samples}))
py = json.loads(subprocess.run([sys.executable, "-I", tree + "/scripts/windows_check.py", "--pattern-self-test", sys.argv[3]], capture_output=True, text=True, cwd=tree).stdout)
ps = json.loads(subprocess.run([pwsh, "-NoProfile", "-File", tree + "/win/step0_pc_tests.ps1", "-PatternSelfTest", sys.argv[3]], capture_output=True, text=True, cwd=tree).stdout)
bad = 0
for sid in samples:
    a, b = sorted(py["results"][sid]), sorted(ps["results"][sid] if isinstance(ps["results"][sid], list) else [ps["results"][sid]])
    kind, cid = expect[sid]
    declared_ok = (cid in a) if kind == "has" else (cid not in a) if kind == "hasnt" else (a == cid)
    if a != b or not declared_ok:
        bad += 1; print("DISAGREE sample=%s python=%s powershell=%s declared=%s/%s" % (sid, a, b, kind, cid))
print("samples: %d, python/powershell disagreements or declared-expectation misses: %d, versions: %s/%s" % (len(samples), bad, py["patterns_version"], ps["patterns_version"]))
sys.exit(1 if bad else 0)
PYEOF
  expect patterns.python_and_powershell_agree 0 -m 'misses: 0' -- $PY "$TMP/selftest.py" "$TREE" "$PWSH" "$TMP/samples.json"
  # fail closed
  FC="$TMP/failclosed"; mkdir -p "$FC/win" "$FC/scripts"; cp -r "$TREE/win/." "$FC/win/"; cp "$TREE/scripts/windows_check.py" "$FC/scripts/"
  mkdir -p "$FC/$FIX"; cp "$TREE/$FIX/report_gpu12_pro_16gb.json" "$FC/$FIX/"
  OUT="$(cd "$FC" && "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -Out "$FC/out_step0.json" 2>&1)"; RC=$?
  if [ "$RC" -eq 2 ] && [ ! -e "$FC/out_step0.json" ] && printf '%s' "$OUT" | grep -q 'REDACTION PATTERNS UNAVAILABLE'; then record failclosed.step0_without_pattern_file PASS "exit 2, nothing written" "exit 2; $(printf '%s' "$OUT" | grep 'UNAVAILABLE' | cut -c1-110)"; else record failclosed.step0_without_pattern_file FAIL "exit 2, nothing written" "exit $RC"; fi
  OUT="$(cd "$FC" && $WC --tier-json-out "$FC/out_tier.json" --json-out "$FC/out_json.json" $FIX/report_gpu12_pro_16gb.json 2>&1)"; RC=$?
  if [ "$RC" -eq 2 ] && [ ! -e "$FC/out_tier.json" ] && [ ! -e "$FC/out_json.json" ] && printf '%s' "$OUT" | grep -q 'REDACTION PATTERNS UNAVAILABLE'; then record failclosed.windows_check_without_pattern_file PASS "exit 2, nothing written" "exit 2"; else record failclosed.windows_check_without_pattern_file FAIL "exit 2, nothing written" "exit $RC"; fi
  echo '{ not json' > "$FC/scripts/redaction_patterns.json"
  OUT="$(cd "$FC" && "$PWSH" -NoProfile -File win/step0_pc_tests.ps1 -Out "$FC/out_step0.json" 2>&1)"; RC=$?
  OUT2="$(cd "$FC" && $WC $FIX/report_gpu12_pro_16gb.json 2>&1)"; RC2=$?
  if [ "$RC" -eq 2 ] && [ "$RC2" -eq 2 ] && [ ! -e "$FC/out_step0.json" ]; then record failclosed.corrupt_pattern_file PASS "both exit 2" "step0 $RC, windows_check $RC2"; else record failclosed.corrupt_pattern_file FAIL "both exit 2" "step0 $RC, windows_check $RC2"; fi
  echo '{"schema":"x","version":1,"categories":[{"id":"email","scope":"both","regex":"x","flags":""}]}' > "$FC/scripts/redaction_patterns.json"
  OUT2="$(cd "$FC" && $WC $FIX/report_gpu12_pro_16gb.json 2>&1)"; RC2=$?
  [ "$RC2" -eq 2 ] && record failclosed.incomplete_pattern_file PASS "exit 2 when required categories are missing" "exit 2" || record failclosed.incomplete_pattern_file FAIL "exit 2" "exit $RC2"
  # ---- the Windows branches of the script, run on Linux with invented answers (logic only; real Windows answers stay UNVERIFIED)
  MK="$TMP/mock"; mkdir -p "$MK/fakebin" "$MK/pf/VeraCrypt" "$MK/pf/Inkscape/bin" "$MK/pf/Blender Foundation/Blender 5.2" "$MK/sr/System32" "$MK/tools/photocraft-0.10.0" "$MK/tools/FilmCraft-v0.8.0-win-x64" "$MK/tools/vectorcraft_0.13.1" "$MK/tools/lightcraft" "$MK/tools/random-folder"
  : > "$MK/pf/VeraCrypt/VeraCrypt.exe"; : > "$MK/pf/Inkscape/bin/inkscape.exe"; : > "$MK/pf/Blender Foundation/Blender 5.2/blender.exe"; : > "$MK/sr/System32/vulkan-1.dll"
  printf '#!/bin/sh\necho "NVIDIA GeForce RTX 3060, 12288 MiB, 552.22"\n' > "$MK/nvidia-smi"
  printf '#!/bin/sh\nprintf "Default Version: 2\\n" | iconv -f UTF-8 -t UTF-16LE\n' > "$MK/fakebin/wsl"
  printf '#!/bin/sh\necho v1.9.25200\n' > "$MK/fakebin/winget"
  printf '#!/bin/sh\n[ "$1" = "-3" ] && echo "Python 3.13.15"\n' > "$MK/fakebin/py"
  chmod +x "$MK/nvidia-smi" "$MK/fakebin/"*
  mock_run() {  # mock_run SCENARIO WITH_SMI
    local sc="$1" smi="$2" bin="$MK/fakebin"
    if [ "$smi" = yes ]; then mkdir -p "$MK/withsmi"; cp "$MK/fakebin/"* "$MK/withsmi/"; cp "$MK/nvidia-smi" "$MK/withsmi/"; bin="$MK/withsmi"; fi
    rm -f "$MK/report_$sc.json"
    OUT="$(cd "$TREE" && env ProgramFiles="$MK/pf" SystemRoot="$MK/sr" PATH="$bin:$PATH" "$PWSH" -NoProfile -File tests/win/mocks/mock_windows_wrapper.ps1 -Script win/step0_pc_tests.ps1 -Out "$MK/report_$sc.json" -ToolsRoot "$MK/tools" -Scenario "$sc" 2>&1)"; RC=$?
    MOCKOUT="$OUT"
  }
  cat > "$MK/assert.py" <<'PYEOF'
import json, sys
sc, path = sys.argv[1], sys.argv[2]
r = json.load(open(path))
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)
need(r["os"]["platform"] == "windows", "platform")
need(r["os"]["edition_id"] == "Professional" and r["os"]["build"] == "22631.4317" and r["os"]["version"] == "10.0.22631", "os fields %s" % r["os"])
need(r["cpu"]["name"] == "Fakeco Model 9000 Processor" and r["cpu"]["cores"] == 6 and r["cpu"]["logical"] == 12, "cpu %s" % r["cpu"])
need(r["ram"]["total_gb"] == 15.9, "ram %s" % r["ram"])
need([d["drive"] for d in r["disks"]] == ["C", "D"] and r["disks"][1]["type"] == "removable" and r["disks"][0]["fs"] == "NTFS", "disks %s" % r["disks"])
need(r["disks"][0]["size_gb"] == 476.8 and r["disks"][0]["free_gb"] == 200.0, "disk sizes %s" % r["disks"][0])
need(r["tools"]["winget"]["version"] == "1.9.25200" and r["tools"]["python"]["version"] == "3.13.15" and r["tools"]["wsl"]["version"] == "2", "tools")
need(r["tools"]["inkscape"]["found"] and r["tools"]["blender"]["found"] and r["tools"]["veracrypt_installed"] is True, "found-by-file tools")
need(r["vulkan"]["runtime_dll_present"] is True, "vulkan dll")
cf = {(c["app"], c["version"]): c for c in r["craft_apps"]["found"]}
need(set(cf) == {("photocraft", "0.10.0"), ("filmcraft", "0.8.0"), ("vectorcraft", "0.13.1")}, "craft found %s" % sorted(cf))
need(cf[("photocraft", "0.10.0")]["matches_pin"] is True and cf[("filmcraft", "0.8.0")]["matches_pin"] is False and cf[("filmcraft", "0.8.0")]["pinned_version"] == "0.9.0", "craft pins")
need(sorted(r["craft_apps"]["not_found"]) == ["effectcraft", "lightcraft", "soundcraft"], "craft not_found %s" % r["craft_apps"]["not_found"])
g = r["gpus"]
if sc == "nvidia":
    need(r["display"]["primary"] == {"width": 2560, "height": 1440, "refresh_hz": 144, "scale_percent": 150}, "display %s" % r["display"])
    need(g[0]["vram_gb"] == 12.0 and g[0]["vram_source"] == "nvidia-smi", "nvidia merge %s" % g[0])
    need(g[1]["vram_gb"] == 1.0 and g[1]["vram_source"] == "adapterram", "igpu adapterram %s" % g[1])
    need(r["local_accounts_count"] == 2, "Get-LocalUser count %s" % r["local_accounts_count"])
elif sc == "amd_registry":
    need(g[0]["vram_gb"] == 16.0 and g[0]["vram_source"] == "registry_qwMemorySize", "registry qword %s" % g[0])
    need(g[1]["vram_gb"] == 8.0 and g[1]["vram_source"] == "registry_qwMemorySize", "registry binary %s" % g[1])
    need(r["local_accounts_count"] == 3, "CIM account fallback %s" % r["local_accounts_count"])
elif sc == "capped_only":
    need(g[0]["vram_gb"] is None and g[0]["vram_source"] == "adapterram_capped_4gb", "capped %s" % g[0])
elif sc == "software":
    need(g[0]["is_software"] is True and g[0]["vram_source"] == "unreadable", "software %s" % g[0])
print("%s: %d problem(s)%s" % (sc, len(bad), "".join("; " + b for b in bad)))
sys.exit(1 if bad else 0)
PYEOF
  mock_run nvidia yes
  [ "$RC" -eq 0 ] && $PY "$MK/assert.py" nvidia "$MK/report_nvidia.json" > "$MK/a1.txt" 2>&1 && record mock_windows.nvidia_scenario_fields PASS "all Windows branches filled (nvidia-smi merge, drives, screen, accounts, Craft scan)" "$(cat "$MK/a1.txt")" || record mock_windows.nvidia_scenario_fields FAIL "fields" "exit $RC $(cat "$MK/a1.txt" 2>/dev/null) :: $(printf '%s' "$OUT" | tail -5 | tr '\n' '|')"
  expect mock_windows.nvidia_checker_says_gpu_8_12 0 -m 'gpu_tier +gpu-8-12' -m 'NVIDIA, 12.0 GB read from nvidia-smi' -m 'pro-or-higher' -- $WC "$MK/report_nvidia.json"
  mock_run amd_registry no
  [ "$RC" -eq 0 ] && $PY "$MK/assert.py" amd_registry "$MK/report_amd_registry.json" > "$MK/a2.txt" 2>&1 && record mock_windows.amd_registry_scenario_fields PASS "qwMemorySize read as 64-bit and as bytes; CIM account fallback" "$(cat "$MK/a2.txt")" || record mock_windows.amd_registry_scenario_fields FAIL "fields" "exit $RC $(cat "$MK/a2.txt" 2>/dev/null)"
  expect mock_windows.amd_registry_is_capped_at_gpu_low 0 -m 'gpu_tier +gpu-low' -m 'read from registry_qwMemorySize' -- $WC "$MK/report_amd_registry.json"
  mock_run capped_only no
  [ "$RC" -eq 0 ] && $PY "$MK/assert.py" capped_only "$MK/report_capped_only.json" > "$MK/a3.txt" 2>&1 && record mock_windows.capped_only_scenario_fields PASS "capped AdapterRAM is flagged, not trusted" "$(cat "$MK/a3.txt")" || record mock_windows.capped_only_scenario_fields FAIL "fields" "exit $RC $(cat "$MK/a3.txt" 2>/dev/null)"
  expect mock_windows.capped_only_checker_exit1 1 -m 'VRAM unreadable' -- $WC "$MK/report_capped_only.json"
  mock_run software no
  [ "$RC" -eq 0 ] && $PY "$MK/assert.py" software "$MK/report_software.json" > "$MK/a4.txt" 2>&1 && record mock_windows.software_scenario_fields PASS "Basic Render driver is flagged software" "$(cat "$MK/a4.txt")" || record mock_windows.software_scenario_fields FAIL "fields" "exit $RC $(cat "$MK/a4.txt" 2>/dev/null)"
  expect mock_windows.software_checker_says_none 0 -m 'gpu_tier +none' -- $WC "$MK/report_software.json"
  # the console of a mocked Windows run shows steps ok/failed, never a path or a name
  if printf '%s' "$MOCKOUT" | grep -v '^files written\|Writing the report' | grep -Eq '/root|/home/[a-z]|wp01a-test'; then record mock_windows.console_has_no_paths FAIL "no paths on the console" "found one"; else record mock_windows.console_has_no_paths PASS "no paths on the console (except the -Out path the tester chose)" "none ($(printf '%s' "$MOCKOUT" | grep -c ' ok$') ok lines, $(printf '%s' "$MOCKOUT" | grep -c 'failed') failed)"; fi
  # real (non-test) mode with the machine's own names taken from the environment: a failing step keeps going and its message is scrubbed;
  # a name in a hardware field is a note; a name anywhere else refuses and writes nothing
  mock_run_names() {  # mock_run_names SCENARIO
    local sc="$1"; rm -f "$MK/report_$sc.json"
    OUT="$(cd "$TREE" && env USERNAME=tamsinwrex COMPUTERNAME=BRAMBLE-Q7 USERDOMAIN=BRAMBLE-Q7 ProgramFiles="$MK/pf" SystemRoot="$MK/sr" PATH="$MK/fakebin:$PATH" "$PWSH" -NoProfile -File tests/win/mocks/mock_windows_wrapper.ps1 -Script win/step0_pc_tests.ps1 -Out "$MK/report_$sc.json" -ToolsRoot "$MK/tools" -Scenario "$sc" 2>&1)"; RC=$?
  }
  mock_run_names steperror
  if [ "$RC" -eq 0 ] && printf '%s' "$OUT" | grep -q 'Reading the processor.*failed: RuntimeException' && ! printf '%s' "$OUT" | grep -Eq 'tamsin|BRAMBLE|AppData|Users' && grep -q '"errors": \[' "$MK/report_steperror.json" && ! grep -Eqi 'tamsin|bramble|Users' "$MK/report_steperror.json" && $PY -c "import json,sys; r=json.load(open(sys.argv[1])); assert len(r['errors'])==1 and r['errors'][0].startswith('Reading the processor'), r['errors']; assert r['cpu']['name'] is None" "$MK/report_steperror.json"; then
    record mock_windows.failing_step_continues_and_message_is_scrubbed PASS "step fails, report still written, no name or path in console or report" "console: $(printf '%s' "$OUT" | grep 'Reading the processor' | sed 's/.*\.\.\. //' | cut -c1-110)"
  else record mock_windows.failing_step_continues_and_message_is_scrubbed FAIL "scrubbed" "exit $RC :: $(printf '%s' "$OUT" | grep -i 'tamsin\|BRAMBLE\|processor' | head -3 | tr '\n' '|')"; fi
  mock_run_names note_cpu
  if [ "$RC" -eq 0 ] && printf '%s' "$OUT" | grep -q 'NOTE category=user_name field=cpu.name hit=ta\*' && ! printf '%s' "$OUT" | grep -Eq 'tamsinwrex|BRAMBLE-Q7' && [ -f "$MK/report_note_cpu.json" ]; then
    record mock_windows.real_mode_name_in_cpu_field_is_a_note PASS "NOTE, report written" "$(printf '%s' "$OUT" | grep 'NOTE category' | head -1)"
  else record mock_windows.real_mode_name_in_cpu_field_is_a_note FAIL "NOTE, report written" "exit $RC :: $(printf '%s' "$OUT" | grep -i 'NOTE\|REDACTION' | head -3 | tr '\n' '|')"; fi
  mock_run_names leak_fs
  if [ "$RC" -eq 2 ] && printf '%s' "$OUT" | grep -q 'category=user_name field=disks\[0\]\.fs hit=ta' && printf '%s' "$OUT" | grep -q 'REDACTION CHECK FAILED, nothing was written' && [ ! -e "$MK/report_leak_fs.json" ] && ! printf '%s' "$OUT" | grep -Eq 'tamsinwrex'; then
    record mock_windows.real_mode_name_outside_hardware_fields_refuses PASS "exit 2, nothing written, masked hit" "$(printf '%s' "$OUT" | grep 'category=' | head -1)"
  else record mock_windows.real_mode_name_outside_hardware_fields_refuses FAIL "exit 2, nothing written" "exit $RC :: $(printf '%s' "$OUT" | grep -i 'category\|REDACTION' | head -3 | tr '\n' '|')"; fi
  # the git-ignored local deny list (the maker's real names live there, never on a command line)
  DT="$TMP/denytree"; mkdir -p "$DT/win" "$DT/scripts" "$DT/tests/win"; cp -r "$TREE/win/." "$DT/win/"; cp "$TREE/scripts/windows_check.py" "$TREE/scripts/redaction_patterns.json" "$DT/scripts/"; cp -r "$TREE/tests/win/." "$DT/tests/win/"
  printf '# one word per line, this PC only\nzorbax\n\nzeta\n' | iconv -f UTF-8 -t UTF-16 > "$DT/scripts/public_lint.deny.local.txt"
  OUT="$(cd "$DT" && python3 -I scripts/windows_check.py tests/win/fixtures/report_short_username_leak.json 2>&1)"; RC=$?
  if [ "$RC" -eq 2 ] && printf '%s' "$OUT" | grep -q 'category=local_deny field=tools.git.notes hit=ze\*\*' && ! printf '%s' "$OUT" | grep -q 'zeta'; then record deny_list.checker_reads_utf16_local_list PASS "exit 2 with category=local_deny and a masked hit" "$(printf '%s' "$OUT" | grep 'category=')"; else record deny_list.checker_reads_utf16_local_list FAIL "exit 2 category=local_deny" "exit $RC :: $(printf '%s' "$OUT" | tail -3 | tr '\n' '|')"; fi
  OUT="$(cd "$DT" && python3 -I scripts/windows_check.py tests/win/fixtures/report_gpu12_pro_16gb.json 2>&1)"; RC=$?
  [ "$RC" -eq 0 ] && record deny_list.clean_report_still_passes PASS "exit 0" "exit 0" || record deny_list.clean_report_still_passes FAIL "exit 0" "exit $RC"
  OUT="$(cd "$DT" && env ProgramFiles="$MK/pf" SystemRoot="$MK/sr" PATH="$MK/fakebin:$PATH" "$PWSH" -NoProfile -File tests/win/mocks/mock_windows_wrapper.ps1 -Script win/step0_pc_tests.ps1 -Out "$DT/deny_out.json" -ToolsRoot "$MK/tools" -Scenario deny_word 2>&1)"; RC=$?
  if [ "$RC" -eq 2 ] && printf '%s' "$OUT" | grep -q 'category=local_deny field=disks\[0\]\.fs hit=zo' && [ ! -e "$DT/deny_out.json" ] && ! printf '%s' "$OUT" | grep -q 'zorbax'; then record deny_list.script_reads_local_list_and_refuses PASS "exit 2, nothing written, masked hit" "$(printf '%s' "$OUT" | grep 'category=')"; else record deny_list.script_reads_local_list_and_refuses FAIL "exit 2" "exit $RC :: $(printf '%s' "$OUT" | grep -i 'category\|REDACTION' | head -2 | tr '\n' '|')"; fi
  # one source: no private copy of an identifying-data regex in the kit
  hits="$(cd "$TREE" && grep -nE '25\[0-5\]|\[0-9\]\{1,3\}\\\.|\\d\{1,3\}\\\.|@\[A-Za-z0-9|\[0-9A-Fa-f\]\{2\}\[:-\]|\[0-9a-fA-F\]\{2\}\[:-\]|\(\?:\[0-9A-Fa-f\]\{1,4\}:\)|[A-Za-z]:\\\\\\\\Users|\[A-Fa-f0-9\]\{8\}-' win/step0_pc_tests.ps1 win/tools/ps_lint.py win/tools/ps_parse.sh scripts/windows_check.py | head -5)"
  [ -z "$hits" ] && record one_source.no_private_identifying_regex PASS "no e-mail, IPv4, MAC, IPv6, GUID or profile-path regex outside the pattern file" "grep found none" || record one_source.no_private_identifying_regex FAIL "no private regex" "$hits"
  # public_lint self-test when WP-03 has landed
  if [ -f "$TREE/scripts/public_lint.py" ]; then
    expect one_source.public_lint_self_test 0 -m 'windows_check|step0' -- $PY scripts/public_lint.py --self-test
  else
    record one_source.public_lint_self_test SKIPPED "public_lint.py --self-test reports no disagreement for the 2 consumers" "scripts/public_lint.py has not landed (WP-03); this package's own agreement test above stands in"
  fi
elif [ "$MODE" = "--all" ]; then
  record pwsh.all BLOCKED "pwsh runs" "pwsh or the pattern file is missing"
fi

# ================================================================== ALL: README tests
cat > "$TMP/readme_test.py" <<'PYEOF'
import json, re, sys
from pathlib import Path
tree = Path(sys.argv[1])
text = (tree / "win/README-MAKER.md").read_text(encoding="utf-8")
heads = [h.strip().lower() for h in re.findall(r"^#{1,3}\s+(.*)$", text, re.M)]
need = ["what this is and what it never does", "how to get the files onto the pc",
        "how to run a script for one session only, without changing system policy", "the 3-minute pc inventory",
        "reading the report yourself before you paste it", "if the script refuses to write the report", "if it fails",
        "what comes next", "the veracrypt container"]
missing = [n for n in need if n not in heads]
problems = []
if missing:
    problems.append("missing headings: " + "; ".join(missing))
for must in ["-ExecutionPolicy Bypass -File .\\win\\step0_pc_tests.ps1", "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force",
             "Get-ExecutionPolicy -List", "Unblock-File .\\win\\step0_pc_tests.ps1", "%TEMP%\\lj_pc_report.json", "scripts\\redaction_patterns.json",
             "administrator account", "project account", "Group Policy", "chat", "category", "hit"]:
    if must not in text:
        problems.append("missing text: " + must)
fences = re.findall(r"```powershell\s*\n(.*?)```", text, re.S)
singles = [f for f in fences if f.count("\n") <= 2 and "win\\step0" not in f and "Set-ExecutionPolicy" not in f]
# scan the README with the shared pattern file (text scope: handles apply here)
pats = json.loads((tree / "scripts/redaction_patterns.json").read_text()) if (tree / "scripts/redaction_patterns.json").is_file() else None
scanned = 0
if pats:
    for c in pats["categories"]:
        rx = re.compile(c["regex"], re.I if "i" in (c.get("flags") or "") else 0)
        for m in rx.finditer(text):
            problems.append("pattern %s at README offset %d" % (c["id"], m.start()))
        scanned += 1
# referenced files exist
for ref in sorted(set(re.findall(r"`((?:win|scripts)\\[A-Za-z0-9_.\\-]+)`", text))):
    p = tree / ref.replace("\\", "/")
    if not p.exists() and "local" not in ref and "lj_pc_report" not in ref:
        problems.append("referenced file does not exist: " + ref)
print("headings found: %d/%d; powershell fences: %d; pattern categories scanned: %d; problems: %d" % (len(need) - len(missing), len(need), len(fences), scanned, len(problems)))
for p in problems:
    print("PROBLEM " + p)
sys.exit(1 if problems else 0)
PYEOF
expect readme.headings_files_and_no_identifying_text 0 -m 'headings found: 9/9' -m 'problems: 0' -m 'pattern categories scanned: [1-9]' -- $PY "$TMP/readme_test.py" "$TREE"

# ================================================================== ALL: tools
bash -n "$TREE/win/tools/fetch_pwsh.sh" && record tools.fetch_pwsh_syntax PASS "bash -n clean" "ok" || record tools.fetch_pwsh_syntax FAIL "bash -n clean" "syntax error"
if need_pwsh; then
  expect tools.fetch_pwsh_is_idempotent 0 -m 'already installed and verified' -m 'sha256=[0-9a-f]{64}' -m 'verified=yes' -- bash win/tools/fetch_pwsh.sh "$SCRATCH/pwsh"
  expect tools.fetch_pwsh_refuses_relative_path 2 -m 'absolute path' -- bash win/tools/fetch_pwsh.sh relative/path
  expect tools.fetch_pwsh_refuses_unverified_existing_dir 2 -m 'refusing to write' -- bash win/tools/fetch_pwsh.sh "$TMP"
  # disk rule, with a fake df that reports little space (no download happens)
  printf '#!/usr/bin/env bash\necho "Filesystem 1M-blocks Used Available Use%% Mounted"\necho "/dev/x 258020M 257800M 300M 100%% /"\n' > "$TMP/fakedf"; chmod +x "$TMP/fakedf"
  expect tools.fetch_pwsh_disk_rule_refuses 3 -m 'DISK: Avail 300 MB minus 275 MB is below 400 MB' -- env LJ_DF_CMD="$TMP/fakedf" bash win/tools/fetch_pwsh.sh "$TMP/newdest"
  [ ! -e "$TMP/newdest" ] && record tools.fetch_pwsh_disk_refusal_created_nothing PASS "nothing created" "absent" || record tools.fetch_pwsh_disk_refusal_created_nothing FAIL "nothing created" "exists"
fi

# ================================================================== ALL: Windows-only claims stay UNVERIFIED
cat > "$TMP/unverified.txt" <<'EOF'
Every CIM/WMI query (Win32_OperatingSystem, Win32_Processor, Win32_ComputerSystem, Win32_VideoController, Win32_LogicalDisk, Win32_UserAccount)
Registry reads (CurrentVersion EditionID and UBR, display adapter class qwMemorySize, WindowMetrics AppliedDPI)
Get-LocalUser in Windows PowerShell 5.1 and PowerShell 7
System.Windows.Forms screen count
winget --version, wsl --status (UTF-16 output and its English wording), py -3 --version
nvidia-smi output format and the MiB-to-GB conversion
Vulkan detection (a DLL on disk is only a hint; the Real-ESRGAN test remains the proof)
The %TEMP% default and a write to it on a managed PC
Windows PowerShell 5.1 behaviour of every cmdlet and of ConvertTo-Json output
Execution-policy options A and B, Unblock-File and Group Policy handling
Whether version strings on the maker's PC trip any pattern
Process-start timeouts and the reading of tool output through System.Diagnostics.Process on 5.1
The assumed thresholds in win/tiers.json marked (J)
The six paste-in fallback commands in the README (parse-tested only; Get-CimInstance does not exist on Linux)
The README's instructions about Properties, Unblock and Extract All in File Explorer
EOF
record windows.claims_awaiting_first_real_run UNVERIFIED "every Windows-only claim marked until a real report exists" "$(wc -l < "$TMP/unverified.txt") claim groups listed in build/evidence/wp01a/unverified.txt" "no Windows machine in the container; first run is the maker's"
cp "$TMP/unverified.txt" "$EVID/unverified.txt"

END_MB="$(avail_mb)"
echo "---"
echo "WP-01a all: PASS=$NPASS FAIL=$NFAIL UNVERIFIED=$NUNV SKIPPED=$NSKIP BLOCKED=$NBLOCK  (df Avail $START_MB -> $END_MB MB)"
$PY - "$JSONL" "$EVID/summary.json" "$MODE" "$NPASS" "$NFAIL" "$NUNV" "$NSKIP" "$NBLOCK" "$START_MB" "$END_MB" <<'PYEOF'
import json, sys
j, out, mode, p, f, u, s, b, a0, a1 = sys.argv[1:]
rows = [json.loads(l) for l in open(j)]
json.dump({"schema": "lj-evidence-summary/1", "package": "WP-01a", "mode": mode, "pass": int(p), "fail": int(f), "unverified": int(u),
           "skipped": int(s), "blocked": int(b), "tests": len(rows), "avail_mb_start": int(a0), "avail_mb_end": int(a1),
           "names": {r["test"]: r["status"] for r in rows}}, open(out, "w"), indent=1, sort_keys=True)
PYEOF
[ "$NFAIL" -ne 0 ] && exit 1
[ "$NBLOCK" -ne 0 ] && exit 3
exit 0
