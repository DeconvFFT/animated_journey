#!/usr/bin/env bash
# tests/win_lj/run_tests.sh [--quick|--all]    WP-01b: lj.ps1 doctor and close v0 (dry run only)
#
#   --quick  (at most 60 s, no downloads, no timed runs) lint, parse, static "no write code" checks, data checks, help,
#            the not-in-v0 switches, doctor on a fixture, close on the planted tree, the three root refusals, and the Windows-only claims
#            listed as UNVERIFIED
#   --all    everything in --quick plus the rest of doctor and close (SaveTier guards, step0 on Linux, no Python,
#            every root and config refusal, links, env-variable lists, empty root), the full close with the repo checks
#            under a read-only mount and no network, and the Windows-only claims listed as UNVERIFIED
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
# Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line is BLOCKED. UNVERIFIED (Windows-only
# behaviour) and SKIPPED are listed and are never counted as a pass.
# Every test also writes one evidence envelope (build plan 4.2) to build/evidence/wp01b/tests.jsonl.
#
# Environment: PWSH  path to pwsh 7.5.4 (default <scratch>/pwsh/pwsh, see win/tools/fetch_pwsh.sh)
# The synthetic trees are built by tests/win_lj/make_trees.py into the folder build-scratch beside the repository
# (that is where tests/win_lj/planted.config.json points). Nothing here uses the network, and nothing is written
# inside the repository except renders/wp01b/ (git-ignored) and build/evidence/wp01b/.
set -u
MODE="${1:---quick}"
case "$MODE" in --quick|--all) ;; *) echo "usage: run_tests.sh [--quick|--all]" >&2; exit 2;; esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"
SIBLING="$(cd "$ROOT/.." && pwd)/build-scratch"      # where planted.config.json's relative root points
PWSH="${PWSH:-$SCRATCH/pwsh/pwsh}"
PY="python3 -I -B"
EVID="$ROOT/build/evidence/wp01b"
TREES="$SIBLING/wp01b-trees"
PL="$TREES/planted"
T="tests/win_lj"
FIX="tests/win/fixtures"
mkdir -p "$EVID" "$ROOT/renders/wp01b" "$SIBLING" 2>/dev/null
TMP="$(mktemp -d "$SCRATCH/wp01b-test.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
JSONL="$EVID/tests.jsonl"
: > "$JSONL"
NPASS=0; NFAIL=0; NUNV=0; NSKIP=0; NBLOCK=0

avail_mb() { df -BM / | awk 'NR==2 { gsub("M","",$4); print $4 }'; }
START_MB="$(avail_mb)"

record() {  # record NAME STATUS EXPECTED ACTUAL [UNVERIFIED_REASON]
  local name="$1" status="$2" exp="$3" act="$4" unv="${5:-}"
  case "$status" in PASS) NPASS=$((NPASS+1));; FAIL) NFAIL=$((NFAIL+1));; UNVERIFIED) NUNV=$((NUNV+1));; SKIPPED) NSKIP=$((NSKIP+1));; BLOCKED) NBLOCK=$((NBLOCK+1));; esac
  printf '%-10s %-52s %s\n' "$status" "$name" "$(printf '%s' "$act" | head -c 150 | tr '\n' ' ')"
  EV_NAME="$name" EV_STATUS="$status" EV_EXP="$exp" EV_ACT="$act" EV_UNV="$unv" EV_START="$START_MB" EV_END="$(avail_mb)" \
  EV_ROOT="$ROOT" EV_SCRATCH="$SCRATCH" EV_SIB="$SIBLING" EV_PY="$(python3 --version 2>&1 | awk '{print $2}')" \
  EV_FF="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}' | cut -d- -f1)" EV_JSONL="$JSONL" \
  python3 -I - <<'PYEOF'
import json, os, re, datetime
e = os.environ
def clean(s):
    s = s.replace(e["EV_ROOT"], ".")
    s = s.replace(e["EV_SIB"], "<scratch>").replace(e["EV_SCRATCH"], "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return s[:700]
s, en = int(e["EV_START"] or 0), int(e["EV_END"] or 0)
env = {"platform": "linux", "ffmpeg": e["EV_FF"], "nproc": os.cpu_count(), "python": e["EV_PY"], "node": "22.x"}
rec = {"schema": "lj-evidence/1", "package": "WP-01b", "test": e["EV_NAME"],
       "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), "status": e["EV_STATUS"], "env": env,
       "disk": {"avail_mb_start": s, "planned_write_mb": 0, "avail_mb_min": min(s, en), "avail_mb_end": en, "floor_mb": 400, "hard_floor_mb": 250},
       "expected": clean(e["EV_EXP"]), "actual": clean(e["EV_ACT"]), "notes": "",
       "unverified_reasons": [e["EV_UNV"]] if e["EV_UNV"] else []}
open(e["EV_JSONL"], "a").write(json.dumps(rec, sort_keys=True) + "\n")
PYEOF
}

# run CMD... in $ROOT; sets OUT (stdout+stderr) and RC
runin() { OUT="$(cd "$ROOT" && "$@" 2>&1)"; RC=$?; }

# expect NAME EXPECTED_RC [-m REGEX | -n REGEX]... -- CMD...
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
  if [ -z "$why" ]; then record "$name" PASS "exit $want${must[*]:+ matching ${must[*]}}" "exit $RC; $(printf '%s' "$OUT" | grep -E 'RESULT|REFUSED|not in v0|TOTAL|files written|problems:|PARSED|parse error|WOULD REMOVE|exit [0-9]|HASH|Unknown|BACKUP' | head -4 | tr '\n' '|')"
  else record "$name" FAIL "exit $want${must[*]:+ matching ${must[*]}}" "$why :: $(printf '%s' "$OUT" | head -6 | tr '\n' '|')"; fi
}

need_pwsh() { [ -x "$PWSH" ]; }
LJ() { "$PWSH" -NoProfile -File win/lj.ps1 "$@"; }
# hashed sets: nothing in them may change during a read-only command (win without kit2, which another package writes)
hash_set() { ( cd "$ROOT" && $PY $T/tree_hash.py win tests/win/fixtures $T scripts --exclude kit2 --exclude __pycache__ ); }
hash_trees() { $PY "$ROOT/$T/tree_hash.py" "$TREES"; }

# expect_still NAME RC ... -- CMD : like expect, and the hashed sets (repo files and the synthetic trees) must be identical before and after
expect_still() {
  local name="$1"; shift
  local h0 h1 g0 g1
  h0="$(hash_set)"; g0="$(hash_trees)"
  expect "$name" "$@"
  h1="$(hash_set)"; g1="$(hash_trees)"
  if [ "$h0" = "$h1" ] && [ "$g0" = "$g1" ]; then record "$name.tree_hash_identical" PASS "repo set and synthetic trees unchanged" "$g0 / $h0"
  else record "$name.tree_hash_identical" FAIL "repo set and synthetic trees unchanged" "changed: trees $g0 -> $g1; repo $h0 -> $h1"; fi
}

echo "WP-01b tests ($MODE). pwsh: $(need_pwsh && echo present || echo MISSING)  patterns file: $( [ -f "$ROOT/scripts/redaction_patterns.json" ] && echo present || echo MISSING)  public_lint: $( [ -f "$ROOT/scripts/public_lint.py" ] && echo present || echo MISSING)"

# ================================================================== QUICK: lint, parse, static checks, data
expect lint.lj_script 0 -m 'TOTAL: 0 error' -- $PY win/tools/ps_lint.py win/lj.ps1
expect lint.readme_fences 0 -m 'TOTAL: 0 error' -m '[1-9][0-9]* powershell fence' -- $PY win/tools/ps_lint.py win/README-LJ.md
# planted write / delete / network code must make the read-only lint fail: this is what keeps v0 unable to change anything
for plant in 'Remove-Item -LiteralPath $x -Recurse:RO-delete' 'Set-Content -Path $x -Value 1:RO-write' 'Out-File $x:RO-write' 'Invoke-WebRequest http://example.invalid:RO-network' 'Set-ExecutionPolicy -Scope LocalMachine Bypass:R13'; do
  code="${plant%:*}"; rule="${plant##*:}"
  { cat "$ROOT/win/lj.ps1"; printf '\n%s\n' "$code"; } > "$TMP/lj_planted.ps1"
  expect "lint.planted_${rule}_is_caught_$(printf '%s' "${code%% *}" | tr 'A-Z' 'a-z')" 1 -m "$rule" -- $PY win/tools/ps_lint.py "$TMP/lj_planted.ps1"
done
# static: no write, delete, move, network, git-write or process-start code anywhere in the script
BAN='Remove-Item|Set-Content|Add-Content|Out-File|Move-Item|Copy-Item|Rename-Item|New-Item|Clear-Content|Set-ItemProperty|Invoke-WebRequest|Invoke-RestMethod|Start-BitsTransfer|WebClient|Invoke-Expression|Start-Process|Set-ExecutionPolicy|git +(commit|push|add|rm|clean|reset|checkout)|\[System\.IO\.(File|Directory)\]::(Write|Delete|Move|Copy|Create|Append|Replace|Set)|Export-Csv|Export-Clixml|Tee-Object|Start-Transcript'
if grep -nE "$BAN" "$ROOT/win/lj.ps1" > "$TMP/ban.txt"; then record static.no_write_delete_network_code FAIL "no match" "$(head -3 "$TMP/ban.txt" | tr '\n' '|')"
else record static.no_write_delete_network_code PASS "no write, delete, move, network, git-write or process-start code" "no match for $(printf '%s' "$BAN" | tr '|' '\n' | wc -l) patterns in win/lj.ps1"; fi
# the only .NET file calls are reads
CALLS="$(grep -oE '\[System\.IO\.(File|Directory|Path)\]::[A-Za-z]+' "$ROOT/win/lj.ps1" | sort -u | tr '\n' ' ')"
if printf '%s' "$CALLS" | grep -Eq '::(Write|Delete|Move|Copy|Create|Append|Replace|Set|Open)'; then record static.only_read_calls_into_dotnet_io FAIL "reads only" "$CALLS"
else record static.only_read_calls_into_dotnet_io PASS "reads only" "$CALLS"; fi

if need_pwsh; then
  expect parse.ps_parse_sh_all_files 0 -m 'PARSED [0-9]+ item\(s\), 0 parse error' -n 'parse error:' -- env PWSH="$PWSH" bash win/tools/ps_parse.sh
  cat > "$TMP/parse_own.ps1" <<'PS'
param([string]$Root)
$bad = 0; $n = 0
$files = @((Join-Path $Root 'win/lj.ps1'))
foreach ($f in $files) {
    $t = $null; $e = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$t, [ref]$e)
    $n++; $bad += $e.Count
}
$md = [System.IO.File]::ReadAllText((Join-Path $Root 'win/README-LJ.md'))
$m = [regex]::Matches($md, '(?ms)^```powershell\s*\r?\n(.*?)^```\s*$')
foreach ($x in $m) {
    $t = $null; $e = $null
    [void][System.Management.Automation.Language.Parser]::ParseInput($x.Groups[1].Value, [ref]$t, [ref]$e)
    $n++; $bad += $e.Count
}
Write-Output ("PARSED {0} item(s) of lj.ps1 and README-LJ.md ({1} fence(s)), {2} parse error(s)" -f $n, $m.Count, $bad)
if ($bad -gt 0) { exit 1 } else { exit 0 }
PS
  expect parse.own_files_and_readme_fences 0 -m 'PARSED [0-9]+ item\(s\) of lj.ps1 and README-LJ.md \([1-9][0-9]* fence\(s\)\), 0 parse error' -- "$PWSH" -NoProfile -File "$TMP/parse_own.ps1" -Root "$ROOT"
else
  record parse.ps_parse_sh_all_files SKIPPED "0 parse errors" "PENDING: pwsh not yet fetched; ps_lint alone gates"
fi

# data: the example config, the test configs, the README
cat > "$TMP/data_test.py" <<'PYEOF'
import json, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
problems = []
ex = json.loads((root / "win/lj.config.example.json").read_text(encoding="utf-8"))
if ex.get("schema") != "lj-config/1": problems.append("example schema")
known = {"schema", "root", "tools_root", "work_folder_names", "never_touch_names", "never_touch_paths", "extra_tools_folder_names", "apps"}
for k in ex:
    if k not in known and not k.startswith("_"): problems.append("unknown key " + k)
apps = ex.get("apps", {})
if sorted(apps) != sorted(["photocraft", "vectorcraft", "lightcraft", "filmcraft", "effectcraft", "soundcraft"]): problems.append("apps differ from the six Craft apps: %r" % sorted(apps))
for name, a in apps.items():
    if a.get("recent_files") != [] or a.get("cache") != []: problems.append(name + ": shipped lists must be empty until a real paste")
    if a.get("status") != "UNVERIFIED": problems.append(name + ": status must be UNVERIFIED")
    if "not checked on this PC" not in a.get("note", "") and "learning only" not in a.get("note", "").lower(): problems.append(name + ": note must say the locations are unconfirmed")
if "\\" in ex.get("root", ""): problems.append("root should use forward slashes")
for p in sorted((root / "tests/win_lj").glob("*.json")):
    try: json.loads(p.read_text(encoding="utf-8"))
    except ValueError: problems.append("not JSON: " + p.name)
# README
md = (root / "win/README-LJ.md").read_text(encoding="utf-8")
need = ["What it never does", "doctor: what kind of computer is this?", "close: what would a clean-up remove?", "How to read the list", "If it says REFUSED", "What comes next", "UNVERIFIED"]
missing = [h for h in need if h not in md]
for h in missing: problems.append("README lacks: " + h)
for sw in ("-Apply", "-Commit", "-IncludeWindowsRecent"):
    if sw not in md: problems.append("README does not mention " + sw)
if "not in v0" not in md: problems.append("README does not quote the not-in-v0 message")
fences = re.findall(r"(?ms)^```json\s*\r?\n(.*?)^```\s*$", md)
for f in fences:
    try: json.loads(f)
    except ValueError: problems.append("a json fence does not parse")
ps = re.findall(r"(?ms)^```powershell\s*\r?\n", md)
# files named in the README must exist
for ref in sorted(set(re.findall(r"`((?:win|scripts)\\[A-Za-z0-9_.\\-]+)`", md))):
    if "local" in ref or "lj_pc_report" in ref: continue
    if not (root / ref.replace("\\", "/")).exists(): problems.append("README names a file that does not exist: " + ref)
# the README must never tell the maker to use a switch that does not exist in v0
for l in md.splitlines():
    if re.search(r"powershell\.exe .*(-Apply|-Commit|-IncludeWindowsRecent)", l): problems.append("README command line uses a v1 switch")
print("example apps: %d; test configs checked; README headings found: %d/%d; powershell fences: %d; json fences: %d; problems: %d" % (len(apps), len(need) - len(missing), len(need), len(ps), len(fences), len(problems)))
for p in problems: print("PROBLEM " + p)
sys.exit(1 if problems else 0)
PYEOF
expect data.example_config_test_configs_and_readme 0 -m 'example apps: 6' -m 'headings found: 7/7' -m 'problems: 0' -- $PY "$TMP/data_test.py" "$ROOT"
if [ -f "$ROOT/scripts/public_lint.py" ]; then
  expect lint.public_lint_on_owned_paths 0 -m 'public_lint' -- $PY scripts/public_lint.py --paths win/lj.ps1 win/lj.config.example.json win/README-LJ.md tests/win_lj
else
  record lint.public_lint_on_owned_paths SKIPPED "public_lint clean" "scripts/public_lint.py has not landed"
fi

# the synthetic trees
expect trees.build 0 -m 'built synthetic trees' -- $PY $T/make_trees.py "$TREES"

if ! need_pwsh; then
  record pwsh.runs SKIPPED "pwsh available" "PENDING: pwsh not yet fetched (win/tools/fetch_pwsh.sh); only the static checks ran"
else
# ================================================================== QUICK: behaviour
expect help.prints_summary 0 -m 'DRY RUN ONLY' -m 'doctor' -m 'close' -m 'not in v0|Not in v0' -- LJ help
expect help.no_arguments_is_help 0 -m 'DRY RUN ONLY' -- LJ
for cmd in close doctor; do
  for sw in -Apply -Commit -IncludeWindowsRecent; do
    expect_still "not_in_v0.$cmd$sw" 2 -m 'not in v0: planned for v1 in week 4; nothing was done' -m 'files written: none' -n 'WOULD REMOVE|TIER TABLE' -- LJ $cmd $sw
  done
done
expect_still not_in_v0.close_apply_with_config 2 -m 'not in v0.*nothing was done' -n 'WOULD REMOVE' -- LJ close -Config $T/planted.config.json -Apply
expect_still not_in_v0.lowercase_and_abbreviations 2 -m 'not in v0.*nothing was done' -- LJ close -apply -com
expect_still not_in_v0.double_dash_and_equals 2 -m 'not in v0.*nothing was done' -- LJ close --apply -Commit=1

expect_still doctor.fixture_prints_tier_table 0 -m 'TIER TABLE' -m 'gpu_tier +gpu-8-12' -m 'ram_tier +16\+' -m '\[4/4\] Summary' -m 'files written: none' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json

expect_still close.planted_lists_the_planted_items 0 -m 'WOULD REMOVE' -m 'xmp ' -m 'Recovery \(folder\)' -m 'Auto-Save' -m 'cache \(folder\)' -m 'BACKUP: not implemented in v0 \(week 4\)' -m 'files written: none' -m 'SKIPPED \(link\)' -m 'UNVERIFIED' -n 'CANARY|OUTSIDE' -- LJ close -Config $T/planted.config.json -SkipChecks
printf '%s\n' "$OUT" > "$TMP/planted_out.txt"
expect close.planted_list_is_exactly_the_manifest 0 -m 'rows: 12 expected: 12 listed-and-expected: 12' -m 'problems: 0' -- $PY $T/check_close.py "$TMP/planted_out.txt" "$TREES/expected.json"

expect_still close.root_is_slash_refused 2 -m 'REFUSED: the root is a drive root' -m 'Nothing was done' -n 'WOULD REMOVE' -- LJ close -Config $T/root_is_slash.config.json -SkipChecks
expect_still close.root_is_repo_refused 2 -m 'REFUSED: the root is the project repository folder' -n 'WOULD REMOVE' -- LJ close -Config $T/root_is_repo.config.json -SkipChecks
expect_still close.root_is_home_refused 2 -m 'REFUSED: the root is the user profile folder' -n 'WOULD REMOVE' -- LJ close -Config $T/root_is_home.config.json -SkipChecks
fi

# ================================================================== ALL
if [ "$MODE" = "--all" ] && need_pwsh; then
  # ---- doctor
  expect_still doctor.vram_unreadable_is_exit_1 1 -m 'FINDING' -m 'valid, but a finding needs a human' -- LJ doctor -FromReport $FIX/report_vram_capped_only.json
  expect_still doctor.low_tier_is_information 0 -m 'gpu_tier +none' -- LJ doctor -FromReport $FIX/report_nogpu_home_8gb.json
  expect_still doctor.identifying_report_exit_2 2 -m 'category=email field=tools.git.notes hit=ta\*\*' -m 'the checker refused the report' -n '@[a-z]' -- LJ doctor -FromReport $FIX/report_identifying.json
  expect_still doctor.missing_report_exit_2 2 -m 'REFUSED: that report file was not found' -- LJ doctor -FromReport $TMP/nope.json
  expect_still doctor.unknown_option_exit_2 2 -m "Unknown option '-Config' for doctor" -- LJ doctor -Config x
  rm -f "$ROOT/renders/wp01b/tier.json"
  find win tests/win/fixtures $T scripts renders/wp01b -type f -not -path 'win/kit2/*' -not -name '*.pyc' 2>/dev/null | sort > "$TMP/files_before.txt"
  expect doctor.savetier_writes_the_derived_file 0 -m 'wrote: tier-json-out' -m 'files written: .*renders/wp01b/tier.json \(derived tier file\)' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json -SaveTier renders/wp01b/tier.json
  find win tests/win/fixtures $T scripts renders/wp01b -type f -not -path 'win/kit2/*' -not -name '*.pyc' 2>/dev/null | sort > "$TMP/files_after.txt"
  NEWF="$(diff "$TMP/files_before.txt" "$TMP/files_after.txt" | grep '^[<>]' | tr '\n' ' ')"
  if [ "$NEWF" = "> renders/wp01b/tier.json " ]; then record doctor.savetier_only_the_derived_file_appears PASS "the only new file is renders/wp01b/tier.json" "$NEWF"
  else record doctor.savetier_only_the_derived_file_appears FAIL "the only new file is renders/wp01b/tier.json" "diff: $NEWF"; fi
  cat > "$TMP/leak_test.py" <<'PYEOF'
import json, sys
rep = json.load(open(sys.argv[1], encoding="utf-8"))
tier_text = open(sys.argv[2], encoding="utf-8").read()
tier = json.loads(tier_text)
needles = set()
needles.add(rep["cpu"]["name"])
for g in rep["gpus"]:
    for k in ("name", "driver_version"):
        if g.get(k): needles.add(str(g[k]))
for k in ("version", "build", "caption"):
    if rep["os"].get(k): needles.add(str(rep["os"][k]))
needles.add(str(rep["ram"]["total_gb"]))
for d in rep["disks"]:
    needles.add(str(d["size_gb"])); needles.add(str(d["free_gb"]))
needles = {n for n in needles if len(n) >= 3}
found = sorted(n for n in needles if n in tier_text)
allowed_top = {"schema", "date", "windows", "gpu_tier", "vram_bucket", "ram_tier", "disk_tier", "display_class", "shared_pc_hint", "ffmpeg", "python_ok", "git_ok", "craft_pins"}
extra = sorted(set(tier) - allowed_top)
print("needles checked: %d; found in the tier file: %d; unexpected top-level keys: %d" % (len(needles), len(found), len(extra)))
for f in found: print("LEAK " + f)
sys.exit(1 if (found or extra) else 0)
PYEOF
  expect doctor.savetier_file_has_no_hardware_strings 0 -m 'needles checked: [1-9][0-9]*; found in the tier file: 0; unexpected top-level keys: 0' -- $PY "$TMP/leak_test.py" $FIX/report_gpu12_pro_16gb.json renders/wp01b/tier.json
  rm -f "$ROOT/renders/wp01b/tier_id.json"
  expect doctor.savetier_identifying_report_writes_nothing 2 -m 'the checker refused the report' -m 'files written: none' -- LJ doctor -FromReport $FIX/report_identifying.json -SaveTier renders/wp01b/tier_id.json
  [ ! -e "$ROOT/renders/wp01b/tier_id.json" ] && record doctor.savetier_refusal_created_no_file PASS "no tier file after a refusal" "absent" || record doctor.savetier_refusal_created_no_file FAIL "no tier file after a refusal" "exists"
  printf 'precious notes, not a tier file\n' > "$TMP/decoy.json"; D0="$(sha256sum "$TMP/decoy.json" | cut -c1-16)"
  expect doctor.savetier_refuses_to_overwrite_a_non_tier_file 2 -m 'REFUSED: that file exists and is not a tier file' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json -SaveTier "$TMP/decoy.json"
  [ "$(sha256sum "$TMP/decoy.json" | cut -c1-16)" = "$D0" ] && record doctor.savetier_decoy_untouched PASS "decoy file unchanged" "$D0" || record doctor.savetier_decoy_untouched FAIL "decoy file unchanged" "changed"
  expect doctor.savetier_refuses_reserved_name 2 -m 'REFUSED: that file name is reserved for raw PC reports' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json -SaveTier "$TMP/pc_report_tier.json"
  expect doctor.savetier_refuses_non_json_name 2 -m 'REFUSED: -SaveTier file name must end in .json' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json -SaveTier "$TMP/tier.txt"
  mkdir -p "$TMP/adir.json"
  expect doctor.savetier_refuses_a_folder 2 -m 'REFUSED: -SaveTier names a folder' -- LJ doctor -FromReport $FIX/report_gpu12_pro_16gb.json -SaveTier "$TMP/adir.json"
  [ ! -e "$TMP/tier.txt" ] && [ ! -e "$TMP/pc_report_tier.json" ] && record doctor.savetier_refusals_created_nothing PASS "nothing created by the refusals" "absent" || record doctor.savetier_refusals_created_nothing FAIL "nothing created" "exists"
  # doctor without -FromReport runs the sibling inventory (on Linux: a non-Windows report, exit 1), writing only its own temp report
  mkdir -p "$TMP/tmpdir"
  expect doctor.runs_the_sibling_inventory_on_linux 1 -m 'Running step0_pc_tests.ps1' -m 'NOT A WINDOWS REPORT' -m 'files written: %TEMP%.lj_pc_report.json \(written by step0_pc_tests.ps1\)' -- env TMPDIR="$TMP/tmpdir" "$PWSH" -NoProfile -File win/lj.ps1 doctor
  NT="$(ls -A "$TMP/tmpdir" | tr '\n' ' ')"
  case "$NT" in "lj_pc_report.json ") record doctor.step0_wrote_only_its_own_temp_report PASS "only lj_pc_report.json in the temp folder" "$NT";; *) record doctor.step0_wrote_only_its_own_temp_report FAIL "only lj_pc_report.json" "$NT";; esac
  # no Python on the PATH
  NOPY="$TMP/nopy-bin"; mkdir -p "$NOPY"
  expect doctor.no_python_is_exit_3_and_says_so 3 -m 'Python 3 was not found' -m 'paste the report in chat' -m 'files written: none' -- env PATH="$NOPY" "$PWSH" -NoProfile -File win/lj.ps1 doctor -FromReport $FIX/report_gpu12_pro_16gb.json

  # ---- close: refusals
  mk_cfg() { printf '%s\n' "$2" > "$TMP/$1.json"; }
  mk_cfg inside_repo "{\"schema\":\"lj-config/1\",\"root\":\"$ROOT/tests\"}"
  expect_still close.root_inside_repo_refused 2 -m 'REFUSED: the root is inside the project repository folder' -- LJ close -Config "$TMP/inside_repo.json" -SkipChecks
  mk_cfg root_link "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/root-link\"}"
  expect_still close.root_is_a_link_refused 2 -m 'REFUSED: the root is a link' -- LJ close -Config "$TMP/root_link.json" -SkipChecks
  mk_cfg git_root "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/gitroot\"}"
  expect_still close.root_is_a_git_repo_refused 2 -m 'REFUSED: the root is itself a git repository' -- LJ close -Config "$TMP/git_root.json" -SkipChecks
  mk_cfg ancestor_of_home "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/fakehome\"}"
  # pwsh itself writes a cache, a data folder and a telemetry id under HOME when it starts; with HOME set to a fake profile
  # inside the hashed trees that would look like a change made by lj.ps1. So pwsh's own folders go to the temp folder.
  PWHOME=(env HOME="$TREES/fakehome/user1" XDG_CACHE_HOME="$TMP/xdg/cache" XDG_DATA_HOME="$TMP/xdg/data" XDG_CONFIG_HOME="$TMP/xdg/config" POWERSHELL_TELEMETRY_OPTOUT=1 POWERSHELL_UPDATECHECK=Off)
  expect_still close.root_containing_the_profile_refused 2 -m 'REFUSED: the root contains the user profile folder' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 close -Config "$TMP/ancestor_of_home.json" -SkipChecks
  mk_cfg profile_root "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/fakehome/user1\"}"
  expect_still close.root_equal_to_the_profile_refused 2 -m 'REFUSED: the root is the user profile folder' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 close -Config "$TMP/profile_root.json" -SkipChecks
  mk_cfg tools_outside "{\"schema\":\"lj-config/1\",\"root\":\"$PL\",\"tools_root\":\"../outside\"}"
  expect_still close.tools_root_outside_the_root_refused 2 -m 'REFUSED: tools_root must be a folder inside the root' -- LJ close -Config "$TMP/tools_outside.json" -SkipChecks
  mk_cfg tools_is_root "{\"schema\":\"lj-config/1\",\"root\":\"$PL\",\"tools_root\":\".\"}"
  expect_still close.tools_root_equal_to_the_root_refused 2 -m 'REFUSED: tools_root must be a folder inside the root' -- LJ close -Config "$TMP/tools_is_root.json" -SkipChecks
  mk_cfg missing_root "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/does-not-exist\"}"
  expect_still close.missing_root_refused 2 -m 'REFUSED: the root folder does not exist' -- LJ close -Config "$TMP/missing_root.json" -SkipChecks
  mk_cfg no_root '{"schema":"lj-config/1"}'
  expect_still close.no_root_refused 2 -m 'REFUSED: the config has no "root"' -- LJ close -Config "$TMP/no_root.json" -SkipChecks
  mk_cfg drive_letter '{"schema":"lj-config/1","root":"C:"}'
  expect_still close.bare_drive_letter_refused 2 -m 'REFUSED: the root is a bare drive letter' -- LJ close -Config "$TMP/drive_letter.json" -SkipChecks
  mk_cfg unset_var '{"schema":"lj-config/1","root":"%LJ_NO_SUCH_VARIABLE%/x"}'
  expect_still close.unset_variable_in_root_refused 2 -m 'REFUSED: the root uses the variable' -- LJ close -Config "$TMP/unset_var.json" -SkipChecks
  printf '{ this is not json' > "$TMP/bad.json"
  expect_still close.bad_json_refused 2 -m 'REFUSED: the config could not be read as JSON' -- LJ close -Config "$TMP/bad.json" -SkipChecks
  mk_cfg bad_schema '{"schema":"other/9","root":"/tmp"}'
  expect_still close.wrong_schema_refused 2 -m 'REFUSED: the config must have "schema"' -- LJ close -Config "$TMP/bad_schema.json" -SkipChecks
  expect_still close.no_config_file_refused 2 -m 'REFUSED: no config file' -- LJ close -Config "$TMP/there-is-no-config.json" -SkipChecks
  expect_still close.option_needs_a_value 2 -m "needs a value" -- LJ close -Config
  expect_still close.unknown_command 2 -m "Unknown command 'bogus'" -- LJ bogus

  # ---- close: the project repository sitting INSIDE the configured root is listed as never touched, not opened, never removable
  mk_cfg parent_of_repo "{\"schema\":\"lj-config/1\",\"root\":\"$(dirname "$ROOT")\"}"
  expect_still close.repo_inside_the_root_is_never_touched 0 -m "<root>/$(basename "$ROOT")  \(the project repository\)" -- LJ close -Config "$TMP/parent_of_repo.json" -SkipChecks
  if printf '%s\n' "$OUT" | sed -n '/^WOULD REMOVE/,/^HELD BACK/p' | grep -qF -- "<root>/$(basename "$ROOT")"; then record close.repo_inside_the_root_not_in_the_would_remove_list FAIL "no line of the repository in WOULD REMOVE" "present"
  else record close.repo_inside_the_root_not_in_the_would_remove_list PASS "no line of the repository in WOULD REMOVE" "absent"; fi

  # ---- close: what is listed, what is not
  expect close.canaries_and_links_never_listed_as_removable 0 -n 'CANARY|OUTSIDE|secret' -m 'SKIPPED \(link\) <root>/work/link-out' -m 'SKIPPED \(link\) <root>/work/link-file.xmp' -m 'SKIPPED \(link\) <root>/work/broken.xmp' -m 'SKIPPED \(link\) <root>/tools/vectorcraft-0.13.1/Recovery' -m '<root>/media  \(protected folder name\)' -m '<root>/archive  \(protected folder name\)' -m '<root>/masters  \(protected folder name\)' -m '<root>/originals  \(protected folder name\)' -m '<root>/work/media  \(protected folder name\)' -m '<root>/otherrepo  \(another git repository\)' -m 'vault.hc  \(possible encrypted container file\)' -- LJ close -Config $T/planted.config.json -SkipChecks
  CL="$OUT"
  for p in "stray.xmp" "link-out/" "tools/soundcraft-0.8.0/stray.xmp" "<root>/cache  "; do
    if printf '%s\n' "$CL" | sed -n '/^WOULD REMOVE/,/^HELD BACK/p' | grep -qF -- "$p"; then record "close.not_in_the_would_remove_list.$(printf '%s' "$p" | tr -c 'A-Za-z0-9\n' '_')" FAIL "absent from WOULD REMOVE" "present: $p"
    else record "close.not_in_the_would_remove_list.$(printf '%s' "$p" | tr -c 'A-Za-z0-9\n' '_')" PASS "absent from WOULD REMOVE" "absent: $p"; fi
  done
  expect close.held_back_with_reasons 0 -m "HELD\] Recovery: <root>/tools/filmcraft-0.9.0/Recovery - contains a protected item named 'media'" -m 'HELD\] Recovery: <root>/tools/effectcraft-0.11.1/Recovery - contains 1 link\(s\), which are never followed' -m "REFUSED\] filmcraft/cache: ../elsewhere/Recovery - '..' is not allowed" -m 'REFUSED\] filmcraft/cache: /etc/hostname - outside the tools folder' -m "REFUSED\] filmcraft/cache: filmcraft-0.9.0/Recovery/media - 'media' is a protected folder name" -m 'SKIPPED\] filmcraft/cache: %LJ_UNSET_VARIABLE%/x' -m 'ALREADY LISTED\] filmcraft/cache: <root>/tools/filmcraft-0.9.0/Auto-Save - already counted above' -m "REFUSED\] photocraft/cache: .*media - 'media' is a protected folder name" -m 'REFUSED\] photocraft/cache: .*vault - listed in never_touch_paths' -m "HELD\] Auto-Save: <root>/tools/effectcraft-0.11.1/Auto-Save - contains a protected item named 'keep'" -n 'photocraft/cache \(folder\)' -- LJ close -Config $T/planted.config.json -SkipChecks
  # r1: the never-touch guards apply to what a wildcard RESOLVES to, not only to the config text (variants of the planted config)
  mk_variant() {  # mk_variant NAME 'python statements that change the dict cfg'
    $PY - "$ROOT/$T/planted.config.json" "$TMP/$1.json" "$PL" "$2" <<'PYEOF'
import json, sys
src, dst, root, code = sys.argv[1:5]
cfg = json.load(open(src, encoding="utf-8"))
cfg["root"] = root
exec(code)
json.dump(cfg, open(dst, "w", encoding="utf-8"))
PYEOF
  }
  mk_variant wild_middle 'cfg["apps"]["photocraft"]["cache"] = ["photocraft-*/*/cache", "photocraft-*/*"]'
  expect_still close.wildcard_in_the_middle_of_a_path_does_not_open_protected_folders 0 -m "REFUSED\] photocraft/cache: .*media - 'media' is a protected folder name" -m 'REFUSED\] photocraft/cache: .*vault - listed in never_touch_paths' -n 'NOT PRESENT\] photocraft|CANARY|photocraft/cache \(folder\)' -- LJ close -Config "$TMP/wild_middle.json" -SkipChecks
  # a never_touch_paths folder nested inside a removal candidate holds the candidate back, whoever found the candidate
  expect close.nested_never_touch_path_holds_the_candidate_back 0 -m "HELD\] Auto-Save: <root>/tools/effectcraft-0.11.1/Auto-Save - contains a protected item named 'keep'" -n 'CANARY' -- LJ close -Config $T/planted.config.json -SkipChecks
  if printf '%s\n' "$OUT" | sed -n '/^WOULD REMOVE/,/^HELD BACK/p' | grep -qF -- "<root>/tools/effectcraft-0.11.1/Auto-Save"; then record close.nested_never_touch_path_candidate_not_in_would_remove FAIL "absent from WOULD REMOVE" "present"
  else record close.nested_never_touch_path_candidate_not_in_would_remove PASS "absent from WOULD REMOVE" "absent"; fi
  # extra_tools_folder_names: an entry with no letter or digit would turn every app folder into a candidate, so it is ignored with a NOTE
  mk_variant wild_extra 'cfg["extra_tools_folder_names"] = ["*", "?*", "*.*", "  "]'
  expect_still close.wildcard_only_extra_tools_folder_name_is_ignored 0 -m "NOTE: extra_tools_folder_names entry '\*' has no letter or digit" -m "NOTE: extra_tools_folder_names entry '\*\.\*' has no letter or digit" -m 'files written: none' -- LJ close -Config "$TMP/wild_extra.json" -SkipChecks
  printf '%s\n' "$OUT" > "$TMP/wild_extra_out.txt"
  expect close.wildcard_only_extra_tools_folder_name_adds_no_row 0 -m 'rows: 12 expected: 12 listed-and-expected: 12' -m 'problems: 0' -- $PY $T/check_close.py "$TMP/wild_extra_out.txt" "$TREES/expected.json"
  mk_variant extra_named 'cfg["extra_tools_folder_names"] = ["LightCraftData"]'
  expect close.named_extra_tools_folder_name_still_works 0 -m 'LightCraftData \(folder\)' -n 'NOTE: extra_tools_folder_names' -- LJ close -Config "$TMP/extra_named.json" -SkipChecks
  # what the maker typed is never echoed expanded: a profile path comes back as %USERPROFILE%, an option comes back by name only
  FH="$TREES/fakehome/user1"
  expect_still usage.unknown_command_echo_hides_the_profile_path 2 -m "Unknown command '%USERPROFILE%/x'" -n 'fakehome|user1' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 "$FH/x"
  expect_still usage.unexpected_argument_echo_hides_the_profile_path 2 -m "Unexpected argument '%USERPROFILE%/x'" -n 'fakehome|user1' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 close "$FH/x"
  expect_still usage.unknown_option_echo_shows_the_name_only 2 -m "Unknown option '-Bogus' for close" -n 'fakehome|user1' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 close "-Bogus:$FH/x"
  expect_still usage.unknown_first_option_echo_shows_the_name_only 2 -m "Unknown option '-Bogus'\. " -n 'fakehome|user1' -- "${PWHOME[@]}" "$PWSH" -NoProfile -File win/lj.ps1 "-Bogus=$FH/x"
  expect close.per_app_lists_are_marked_unverified 0 -m 'photocraft +recent_files: 0 +cache: 1 +\[UNVERIFIED\]' -m 'lightcraft +recent_files: 1 +cache: 1 +\[UNVERIFIED\]' -m 'Until then they stay UNVERIFIED' -- LJ close -Config $T/planted.config.json -SkipChecks
  # a shipped (example-like) config with empty lists, on the empty root, lists nothing
  mk_cfg empty_root "{\"schema\":\"lj-config/1\",\"root\":\"$TREES/empty\",\"apps\":{\"photocraft\":{\"status\":\"UNVERIFIED\",\"recent_files\":[],\"cache\":[]}}}"
  expect_still close.empty_root_lists_nothing 0 -m 'nothing: no sidecar, Recovery, Auto-Save or cache item was found' -m 'photocraft +recent_files: 0 +cache: 0 +\[UNVERIFIED, no entries yet\]' -m 'files written: none' -- LJ close -Config "$TMP/empty_root.json" -SkipChecks
  # env-variable lists (APPDATA / LOCALAPPDATA stand-ins): accepted inside an app folder, refused for a foreign folder, skipped when unset
  expect_still close.appdata_entries_resolve_when_the_variables_are_set 0 -m 'photocraft/recent_files +1 +[0-9]+ B +%APPDATA%.PhotoCraft.recent.json' -m 'photocraft/cache \(folder\) +1 +300 B +%LOCALAPPDATA%.PhotoCraft.Recovery' -m "REFUSED\] photocraft/cache: %APPDATA%/Microsoft - no folder in the path contains the app name 'photocraft'" -n 'CANARY' -- env APPDATA="$TREES/appdata/Roaming" LOCALAPPDATA="$TREES/appdata/Local" "$PWSH" -NoProfile -File win/lj.ps1 close -Config "$TREES/planted_appdata.config.json" -SkipChecks
  expect_still close.appdata_entries_skipped_when_the_variables_are_unset 0 -m 'SKIPPED\] photocraft/recent_files: %APPDATA%/PhotoCraft/recent.json - the variable %APPDATA% is not set here' -- env -u APPDATA -u LOCALAPPDATA "$PWSH" -NoProfile -File win/lj.ps1 close -Config "$TREES/planted_appdata.config.json" -SkipChecks
  # no Python: the checks are skipped and said so
  expect_still close.no_python_skips_the_checks_and_says_so 0 -m 'Looking for Python .* not found' -m 'stale_check.py --new-only \.\.\. SKIPPED \(no Python\)' -m 'public_lint.py \.\.\. SKIPPED \(no Python\)' -m 'BACKUP: not implemented in v0 \(week 4\)' -- env PATH="$NOPY" "$PWSH" -NoProfile -File win/lj.ps1 close -Config $T/planted.config.json
  expect close.skip_checks_says_so 0 -m 'stale_check.py --new-only \.\.\. SKIPPED \(you passed -SkipChecks\)' -m 'public_lint.py \.\.\. SKIPPED \(you passed -SkipChecks\)' -- LJ close -Config $T/planted.config.json -SkipChecks

  # ---- no network, no writes: the full close (with the two repo checks) in a network-less namespace and with the repo and the trees mounted read-only
  if unshare -rn true 2>/dev/null; then
    A="$("$PWSH" -NoProfile -File "$ROOT/win/lj.ps1" close -Config "$ROOT/$T/planted.config.json" -SkipChecks 2>&1)"
    B="$(unshare -rn "$PWSH" -NoProfile -File "$ROOT/win/lj.ps1" close -Config "$ROOT/$T/planted.config.json" -SkipChecks 2>&1)"
    if [ -n "$A" ] && [ "$A" = "$B" ]; then record close.no_network_same_output_in_a_network_less_namespace PASS "identical output under unshare -rn" "$(printf '%s' "$A" | wc -l) lines, identical"
    else record close.no_network_same_output_in_a_network_less_namespace FAIL "identical output under unshare -rn" "outputs differ"; fi
    expect doctor.no_network_in_a_network_less_namespace 0 -m 'TIER TABLE' -m 'files written: none' -- unshare -rn "$PWSH" -NoProfile -File win/lj.ps1 doctor -FromReport $FIX/report_gpu12_pro_16gb.json
  else
    record close.no_network_same_output_in_a_network_less_namespace BLOCKED "unshare -rn works" "unshare -rn is not available here"
  fi
  if unshare -rm true 2>/dev/null; then
    RO='mount --bind "$1" "$1" && mount -o remount,ro,bind "$1" && mount --bind "$2" "$2" && mount -o remount,ro,bind "$2"'
    expect close.full_run_with_checks_on_read_only_mounts_and_no_network 0 -m 'Looking for Python .* ok' -m 'stale_check.py --new-only .*\.\.\. exit [0-9]' -m 'public_lint.py .*\.\.\. exit [0-9]' -m 'check results: ' -m 'files written: none' -m 'Nothing was removed, moved, committed, pushed or written' -- unshare -rmn sh -c "$RO && cd \"$ROOT\" && \"$PWSH\" -NoProfile -File win/lj.ps1 close -Config $T/planted.config.json" sh "$TREES" "$ROOT"
    expect close.read_only_mounts_really_block_writes 0 -m 'Read-only file system' -- unshare -rm sh -c "$RO && (touch \"$TREES/probe\" 2>&1; touch \"$ROOT/probe\" 2>&1; true)" sh "$TREES" "$ROOT"
    expect doctor.fixture_on_a_read_only_repo_writes_nothing 0 -m 'TIER TABLE' -m 'files written: none' -- unshare -rmn sh -c "$RO && cd \"$ROOT\" && \"$PWSH\" -NoProfile -File win/lj.ps1 doctor -FromReport $FIX/report_gpu12_pro_16gb.json" sh "$TREES" "$ROOT"
  else
    record close.full_run_with_checks_on_read_only_mounts_and_no_network BLOCKED "unshare -rm works" "mount namespaces are not available here"
  fi
  # the plain full run (checks included), as the maker will run it; the exit code is the dry run's, not the checkers'
  expect_still close.full_run_exits_0_whatever_the_checkers_say 0 -m 'check results: ' -m 'In v0 they are advice and do not change the exit code of close' -- LJ close -Config $T/planted.config.json
fi

# ================================================================== Windows-only claims stay UNVERIFIED (one evidence line each)
# recorded in --quick as well as --all: it costs nothing, and the quick evidence is what the week-2 runner collects
if true; then
  U() { record "$1" UNVERIFIED "$2" "$3" "no Windows machine in the container; the maker's first run (and what is pasted back) is the evidence"; }
  U windows.path_rules_on_ntfs "drive roots, UNC roots, case-insensitive compares, 8.3 short names and long paths behave as the code assumes" "tested only with Linux paths; Test-SamePath, Test-Inside, GetPathRoot and GetFullPath on Windows are unproven"
  U windows.reparse_points_on_ntfs "symbolic links and junctions have the ReparsePoint attribute and are listed SKIPPED (link), never followed; OneDrive placeholders and other reparse tags are also skipped" "tested with Linux symlinks only"
  U windows.py_launcher_and_python "py -3 -I -B and python -I -B run windows_check.py, stale_check.py and public_lint.py; the Microsoft Store python stub is rejected by the version probe" "no Windows Python here"
  U windows.powershell_5_1_runtime "every cmdlet and .NET call behaves the same in Windows PowerShell 5.1 as in 7.5.4 (scriptblock as MatchEvaluator, Sort-Object on calculated properties, ConvertFrom-Json arrays, exit inside a script run with &)" "parse-tested on 7.5.4 and checked by ps_lint.py against the 5.1 rules only"
  U windows.doctor_runs_step0_in_process "doctor runs step0_pc_tests.ps1 with & and reads its exit code; step0 writes %TEMP%\\lj_pc_report.json" "ran on Linux only (non-Windows report)"
  U windows.environment_variables "APPDATA, LOCALAPPDATA, USERPROFILE, windir, ProgramFiles and ProgramData exist and are the folders the code expects on the maker's PC, including a managed PC" "stand-in variables only"
  U windows.per_app_lists_not_from_a_paste "the recent-file and cache folders of all six Craft apps" "no where-did-it-write paste has arrived; every shipped list is empty and marked UNVERIFIED"
  U windows.mounted_container_detection "a mounted VeraCrypt container is never touched" "v0 cannot detect a mounted container; the config's never_touch_paths is the only guard"
  U windows.argument_binding_5_1 "typing -Apply, -Commit or -IncludeWindowsRecent (any case, abbreviated, or with : or =) is answered with the not-in-v0 message under powershell.exe -File" "checked on pwsh 7.5.4 only; PowerShell drops a trailing colon argument such as -Apply: with no value before the script sees it, which then runs as a plain dry run"
  U windows.console_encoding "non-ASCII file names print correctly in a Windows console" "Linux terminal only"
fi

END_MB="$(avail_mb)"
echo "---"
echo "WP-01b $MODE: PASS=$NPASS FAIL=$NFAIL UNVERIFIED=$NUNV SKIPPED=$NSKIP BLOCKED=$NBLOCK  (df Avail $START_MB -> $END_MB MB)"
$PY - "$JSONL" "$EVID/summary.json" "$MODE" "$NPASS" "$NFAIL" "$NUNV" "$NSKIP" "$NBLOCK" "$START_MB" "$END_MB" <<'PYEOF'
import json, sys
j, out, mode, p, f, u, s, b, a0, a1 = sys.argv[1:]
rows = [json.loads(l) for l in open(j)]
json.dump({"schema": "lj-evidence-summary/1", "package": "WP-01b", "mode": mode, "pass": int(p), "fail": int(f), "unverified": int(u),
           "skipped": int(s), "blocked": int(b), "tests": len(rows), "avail_mb_start": int(a0), "avail_mb_end": int(a1),
           "names": {r["test"]: r["status"] for r in rows}}, open(out, "w"), indent=1, sort_keys=True)
PYEOF
[ "$NFAIL" -ne 0 ] && exit 1
[ "$NBLOCK" -ne 0 ] && exit 3
exit 0
