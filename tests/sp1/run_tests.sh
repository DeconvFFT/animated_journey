#!/usr/bin/env bash
# tests/sp1/run_tests.sh [--quick|--all] [--real-all] [--skip-network]    WP-07: SP1a, the Craft CLIs in the container
#
#   --quick  (at most 60 s, no downloads, no timed runs): syntax, the library self-test, the asset table, `--list` (live, and with the fake 900 MB and
#            600 MB df lines), the ledger check, the guide (regenerated, then check_guide.py), the memory watchdog, the public-repo lint.
#   --all    everything in --quick, plus
#            the real network lines: `--sums-only` (six small text files), the deliberately wrong asset (blocked_proof.json, exit 3), and
#            `--only effectcraft v0.11.1 --t1-only` (a real 64 MB download if the disk guard allows it, else BLOCKED with the guard's exact message; if the
#            download ledger already holds an EffectCraft fetch and t1_effectcraft_v0.11.1.json is PASS, that evidence is reused and nothing is downloaded again:
#            each tarball is fetched once, so this line is re-runnable);
#            the full staged run `--all` is ATTEMPTED only through its guard check here (it takes hours: start it by hand in the background, or pass --real-all);
#            and the MECHANISM tests: the same run_sp1.sh against a local fake release server and stand-in CLIs (tiny, fake df): a full FilmCraft and EffectCraft
#            stage, the keep rule, reuse of the kept tarball, a corrupted tarball rejected before extraction, a hash mismatch that stops `--all` (no 0.8.0 fetch, no
#            EffectCraft), the legitimate 0.8.0 fallback after a failed T2, a --t1-only run followed by --all that leaves the ledger clean (the second EffectCraft fetch
#            carries a recorded exception), a ledger problem that makes --all print LEDGER PROBLEM and exit 1, a usable=false table refused before any download,
#            a corrupt kept tarball that is removed and fetched again, T2's partial envelope surviving a TERM, the guard's refusal, a disk-floor abort that
#            cleans up, and planted defects (each must make exactly its own criterion FAIL). The stand-ins are not FilmCraft or EffectCraft and prove nothing about them.
# Options: --skip-network  skip the real network lines (for a machine without the proxy); --real-all  run the real hours-long `--all` if the guard allows it.
#          --skip-defects / --defects-only  split a full --all in two for a host where it passes 10 minutes (about 13 on the 20 Oct 2026 container): `--all --skip-defects` runs everything
#          except the planted-defect lines (the 12 `fake.defect_*` lines) and writes tests.jsonl; `--defects-only` (it implies --all) runs just those lines and APPENDS them to tests.jsonl, so
#          the two runs together leave the lines of one full --all (the flipped-byte line now runs before the defect lines, in part 1). Run them one after the other, never at the same time.
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail.  Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line is
# BLOCKED (the disk guard refused a real stage: that is an environment fact, not a defect). Every line also writes an evidence envelope (build plan 4.2) to
# build/evidence/wp07/tests.jsonl (--all) or tests_quick.jsonl (--quick). Writes only under build/evidence/wp07/, vendor/craft/ (real stages) and a scratch folder it removes again.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
MODE=--quick; REAL_ALL=0; NET=1; SKIP_DEFECTS=0; DEFECTS_ONLY=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick|--all) MODE="$1";;
    --real-all) REAL_ALL=1;;
    --skip-network) NET=0;;
    --skip-defects) SKIP_DEFECTS=1;;
    --defects-only) DEFECTS_ONLY=1; MODE=--all;;
    *) echo "usage: run_tests.sh [--quick|--all] [--real-all] [--skip-network] [--skip-defects|--defects-only]" >&2; exit 2;;
  esac
  shift
done
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SP1="$ROOT/spikes/sp1_craft_cli"; DRV="$SP1/drivers"; T="$ROOT/tests/sp1"
EVID="$ROOT/build/evidence/wp07"
SCRATCH_ROOT="${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
mkdir -p "$EVID" "$SCRATCH_ROOT"
# Another runner (WP-11a's run_week2_checks.sh) may call this script's --quick while a --all is running: each mode has its own evidence file and its own lock.
JSONL="$EVID/tests.jsonl"; [ "$MODE" = "--quick" ] && JSONL="$EVID/tests_quick.jsonl"
exec 9>"$SCRATCH_ROOT/wp07-tests-${MODE#--}.lock"; flock -w 1200 9 || { echo "BUSY: another run_tests.sh $MODE holds the lock"; exit 3; }
[ "$DEFECTS_ONLY" = 1 ] || : > "$JSONL"   # --defects-only appends to the file the first part wrote
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
    [ -n "$LAST_OUT" ] && tail -n 8 <<<"$LAST_OUT" | sed -e 's/^/    | /' | cut -c1-220
  fi
  LAST_OUT=""
}
nlines() { if [ -f "$1" ]; then wc -l < "$1"; else echo 0; fi; }
avail_mb() { df -BM / | awk 'NR==2{gsub("M","",$4); print $4}'; }

echo "tests/sp1/run_tests.sh $MODE   (df now: Avail $(df -BM / | awk 'NR==2{print $4}'))"

if [ "$DEFECTS_ONLY" != 1 ]; then
# ------------------------------------------------------------------ QUICK
bad=""; for f in "$SP1/run_sp1.sh" "$T/run_tests.sh" "$SP1/tests/fake_df_900.sh" "$SP1/tests/fake_df_600.sh" "$T/fake_df_2000.sh" "$T/fake_df_flag.sh"; do bash -n "$f" 2>/dev/null || bad="$bad $(basename "$f")"; done
check syntax.bash "$([ -z "$bad" ] && echo 1 || echo 0)" "bash -n on run_sp1.sh, run_tests.sh and the fake df scripts; failing:${bad:- none}" "every shell script parses"
bad=""; for f in $(find "$SP1" "$T" -name '*.py' -o -name '*-cli' | sort); do python3 -I -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" 2>/dev/null || bad="$bad $(basename "$f")"; done
check syntax.python "$([ -z "$bad" ] && echo 1 || echo 0)" "ast.parse on every .py file and both stand-in CLIs; failing:${bad:- none}" "every Python file parses"
out="$(python3 -I "$DRV/sp1_lib.py" --selftest 2>&1)"; rc=$?
check lib.selftest "$([ $rc = 0 ] && echo 1 || echo 0)" "sp1_lib --selftest: $(grep -c '^PASS' <<<"$out") PASS, $(grep -c '^FAIL' <<<"$out") FAIL" "scrubber and df parser behave"
out="$(python3 -I "$T/watchdog_test.py" 2>&1)"; rc=$?
check watchdog.rss_and_wall "$([ $rc = 0 ] && echo 1 || echo 0)" "$(tr '\n' ';' <<<"$out" | cut -c1-400)" "the 10 GB watchdog mechanism kills above its limit, spares a quiet process, and the wall clock stops a sleeper"

# the asset table
out="$(python3 -I - "$SP1/release_assets.json" "$EVID/sums" <<'PY'
import json, sys, re, hashlib, os
d = json.load(open(sys.argv[1])); sums = sys.argv[2]
pins = d["pins"]; problems = []
want = [("photocraft","v0.10.0"),("vectorcraft","v0.13.1"),("lightcraft","v0.9.1"),("filmcraft","v0.9.0"),("filmcraft","v0.8.0"),("effectcraft","v0.11.1")]
if [(p["app"],p["tag"]) for p in pins] != want: problems.append("pins differ from the six in W-22")
for p in pins:
    for k in ("linux_x86_64_tarball","windows_x64_portable_zip","windows_x64_msi"):
        e = p[k]
        if not re.fullmatch(r"[0-9a-f]{64}", e["sha256"] or ""): problems.append("%s %s %s: bad hash" % (p["app"],p["tag"],k))
        if k != "windows_x64_msi" and not isinstance(e["bytes"], int): problems.append("%s %s %s: no size" % (p["app"],p["tag"],k))
    f = os.path.join(sums, "%s-%s-SHA256SUMS.txt" % (p["app"],p["tag"]))
    if not os.path.exists(f): problems.append("raw sums file missing for %s %s" % (p["app"],p["tag"]))
    else:
        raw = open(f).read()
        if hashlib.sha256(raw.encode()).hexdigest() != p["sums_file_sha256"]: problems.append("sums file hash differs for %s" % p["app"])
        for k in ("linux_x86_64_tarball","windows_x64_portable_zip"):
            if "%s  %s" % (p[k]["sha256"], p[k]["name"]) not in raw: problems.append("%s %s: %s not in the raw sums file" % (p["app"],p["tag"],k))
if d["r8_comparison"]["status"] != "all match": problems.append("R8 comparison: " + d["r8_comparison"]["status"])
if len(d["r8_comparison"]["rows"]) != 6: problems.append("R8 rows != 6")
if d["soundcraft"]["status"] != "not pinned, not fetched": problems.append("soundcraft entry")
if "integrity" not in d["integrity_note"]: problems.append("integrity note")
print("%d pins, %d independent comparisons (%s), sizes %s; problems: %s" % (len(pins), len(d["r8_comparison"]["rows"]), d["r8_comparison"]["status"], d["size_comparison"]["status"], problems or "none"))
sys.exit(1 if problems else 0)
PY
)"; rc=$?
check assets.table "$([ $rc = 0 ] && echo 1 || echo 0)" "$out" "six pins, names and hashes agree with the raw SHA256SUMS.txt files, R8 values all match, SoundCraft not fetched"

# --list: live, fake 900, fake 600
out="$(bash "$SP1/run_sp1.sh" --list 2>&1)"; rc=$?
avail="$(sed -n 's/^Disk: df says Avail \([0-9]*\) MB.*/\1/p' <<<"$out")"
# --list plans the stages one after the other and the FilmCraft tarball is kept on disk for the EffectCraft stage, so the lean profile needs
# Avail of at least max over the stages of (planned + floor + the tarballs kept so far): 350 + 400 = 750 for FilmCraft, then 300 + 400 + 67 = 767
# for EffectCraft. Computed here the way run_sp1.sh --list computes it (gate review r1: the old one-stage figure of 750 was wrong between 750 and 767 MB).
floor_mb="$(jq -r '.disk.floor_mb' "$SP1/config.json")"
keep_mb=$(( ( $(jq -r '.pins[]|select(.app=="filmcraft" and .tag=="v0.9.0")|.linux_x86_64_tarball.bytes' "$SP1/release_assets.json") + 1048575 ) / 1048576 ))
lean_need=0; kept_mb=0
for sid in $(jq -r '.stages[]|select(.only_if==null)|.id' "$SP1/config.json"); do
  need=$(( $(jq -r --arg id "$sid" '.stages[]|select(.id==$id)|.planned_mb.lean' "$SP1/config.json") + floor_mb + kept_mb ))
  (( need > lean_need )) && lean_need=$need
  [ "$(jq -r --arg id "$sid" '.stages[]|select(.id==$id)|.keep_tarball' "$SP1/config.json")" = true ] && kept_mb=$(( kept_mb + keep_mb ))
done
want_rc=$([ "${avail:-0}" -ge "$lean_need" ] && echo 0 || echo 3)
check list.live "$([ "$rc" = "$want_rc" ] && grep -q 'Planned downloads' <<<"$out" && echo 1 || echo 0)" "Avail ${avail} MB: exit $rc (expected $want_rc: lean needs Avail of at least ${lean_need} MB); $(grep -E '^(Chosen profile|REFUSED)' <<<"$out" | head -2 | tr '\n' ' ')" "--list prints the plan and refuses (exit 3) exactly when Avail minus the planned peak of any lean stage, with the kept FilmCraft tarball counted, is under 400 MB"
out="$(LJ_DF_CMD="$SP1/tests/fake_df_900.sh" bash "$SP1/run_sp1.sh" --list 2>&1)"; rc=$?
check list.fake_900 "$([ $rc = 0 ] && grep -q 'full: filmcraft-v0.9.0 plans 600 MB, Avail 900 MB, leaves 300 MB: REFUSED' <<<"$out" && grep -q 'Chosen profile: lean' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E 'full: filmcraft|Chosen profile' <<<"$out" | tr '\n' ' ' | cut -c1-300)" "at a fake 900 MB the full profile is refused and lean is chosen"
out="$(LJ_DF_CMD="$SP1/tests/fake_df_900.sh" bash "$SP1/run_sp1.sh" --list --profile full 2>&1)"; rc=$?
check list.fake_900_profile_full "$([ $rc = 3 ] && grep -q 'the full profile is refused at this Avail; lean would fit: rerun with --profile lean (or auto)' <<<"$out" && ! grep -q 'Neither profile fits' <<<"$out" && grep -q 'Chosen profile: none' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E 'full profile is refused|Neither' <<<"$out" | cut -c1-150 | tr '\n' ' ')" "--profile full at a fake 900 MB: exit 3 and the message says lean would fit (not 'Neither profile fits')"
out="$(LJ_DF_CMD="$SP1/tests/fake_df_600.sh" bash "$SP1/run_sp1.sh" --list --profile full 2>&1)"; rc=$?
check list.fake_600_profile_full "$([ $rc = 3 ] && grep -q 'Neither profile fits' <<<"$out" && ! grep -q 'lean would fit' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E 'Neither|lean would fit' <<<"$out" | cut -c1-120 | tr '\n' ' ')" "--profile full at a fake 600 MB: neither fits, and the message still says so"
out="$(LJ_DF_CMD="$SP1/tests/fake_df_600.sh" bash "$SP1/run_sp1.sh" --list 2>&1)"; rc=$?
check list.fake_600 "$([ $rc = 3 ] && grep -q 'REFUSED: Avail 600 MB minus planned 600 MB leaves 0 MB, below the 400 MB floor (filmcraft-v0.9.0, full profile)' <<<"$out" && grep -q 'REFUSED: Avail 600 MB minus planned 350 MB leaves 250 MB, below the 400 MB floor (filmcraft-v0.9.0, lean profile)' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E '^REFUSED' <<<"$out" | tr '\n' ' ' | cut -c1-360)" "at a fake 600 MB both profiles are refused with the exact message, exit 3"
out="$(bash "$SP1/run_sp1.sh" --ledger-check 2>&1)"; rc=$?
check ledger.check "$([ $rc = 0 ] && echo 1 || echo 0)" "$out" "each tarball fetched once (a second fetch needs a recorded exception), under the 2 GB allowance"

# the guide
tmpg="$(mktemp "$SCRATCH_ROOT/guide.XXXXXX")"
python3 -I "$SP1/build_guide.py" --out "$tmpg" >/dev/null 2>&1
check guide.in_sync_with_assets "$(cmp -s "$tmpg" "$SP1/MAKER-CRAFT-ZIPS.md" && echo 1 || echo 0)" "build_guide.py regenerates MAKER-CRAFT-ZIPS.md byte for byte from release_assets.json" "the guide was not hand-edited out of sync"
rm -f "$tmpg"
out="$(python3 -I "$SP1/check_guide.py" --json "$EVID/guide_check.json" 2>&1)"; rc=$?
nunv="$(grep -c '^UNVERIFIED' <<<"$out")"
if [ $rc != 0 ]; then rec FAIL guide.check_guide "$(tail -1 <<<"$out") :: $(grep '^FAIL' <<<"$out" | head -2 | tr '\n' ' ' | cut -c1-400)" "check_guide.py"
elif [ "$nunv" != 0 ]; then rec UNVERIFIED guide.check_guide "$(tail -1 <<<"$out"); unverified: $(grep '^UNVERIFIED' <<<"$out" | cut -c12-90 | head -2 | tr '\n' ' ')" "check_guide.py"
else rec PASS guide.check_guide "$(tail -1 <<<"$out")" "check_guide.py"; fi
rec UNVERIFIED guide.windows_behaviour "no Windows PC here: PowerShell 5.1 parsing is covered by ps_lint.py rules and pwsh 7 on Linux only; where the zips unpack, portable.txt handling and each app's writes wait for the maker's Sat 24 Oct paste" "Windows behaviour"

out="$(python3 -I "$ROOT/scripts/public_lint.py" --paths spikes/sp1_craft_cli tests/sp1 build/evidence/wp07 2>&1 | tail -1)"
check lint.public "$(grep -q ' 0 identifying-data finding(s), 0 hygiene finding(s)' <<<"$out" && echo 1 || echo 0)" "$out" "public_lint.py finds no identifying data in the owned paths"
if [ "$MODE" = "--quick" ]; then
  echo "SUMMARY quick: $NPASS PASS, $FAILS FAIL, $BLOCKED BLOCKED, $UNV UNVERIFIED"
  python3 -I "$T/make_summary.py" quick >/dev/null 2>&1
  [ "$FAILS" -gt 0 ] && exit 1; [ "$BLOCKED" -gt 0 ] && exit 3; exit 0
fi

# ------------------------------------------------------------------ ALL: the real network lines
if [ "$NET" = 1 ]; then
  out="$(bash "$SP1/run_sp1.sh" --sums-only 2>&1)"; rc=$?
  check sums.real_six_files "$([ $rc = 0 ] && grep -q 'R8 comparison: all match' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(tail -1 <<<"$out")" "six SHA256SUMS.txt fetched, release_assets.json written, the independent hashes compared"
  rm -f "$EVID/blocked_proof.json"
  vrows() { python3 -I "$DRV/verdict.py" --print 2>/dev/null | grep -E '^\| T[124] (FilmCraft|EffectCraft|FilmCraft stills) '; }
  vbefore="$(vrows)"
  out="$(FORCE_BAD_ASSET=1 bash "$SP1/run_sp1.sh" --only filmcraft v0.9.0 2>&1)"; rc=$?
  st="$(jq -r '.http_status' "$EVID/blocked_proof.json" 2>/dev/null)"; er="$(jq -r '.curl_stderr_verbatim' "$EVID/blocked_proof.json" 2>/dev/null)"
  check blocked.force_bad_asset "$([ $rc = 3 ] && [ "$st" = 404 ] && grep -q 'The requested URL returned error: 404' <<<"$er" && echo 1 || echo 0)" "exit $rc; blocked_proof.json: HTTP $st, curl said: $er" "a wrong asset name gives 404 -> blocked_proof.json with the exact status and curl stderr; exit 3"
  # the forced line leaves a flagged envelope (stage_filmcraft-v0.9.0_forced.json); the verdict must not read it as a real block, and nothing is deleted by hand
  vafter="$(vrows)"
  check blocked.forced_stage_not_in_verdict "$([ -f "$EVID/stage_filmcraft-v0.9.0_forced.json" ] && jq -e '.detail.forced_bad_asset==true and .status=="BLOCKED"' "$EVID/stage_filmcraft-v0.9.0_forced.json" >/dev/null && [ "$vbefore" = "$vafter" ] && ! grep -q 'T[12] FilmCraft.*download blocked' <<<"$vafter" && echo 1 || echo 0)" "forced envelope present and flagged: $([ -f "$EVID/stage_filmcraft-v0.9.0_forced.json" ] && echo yes || echo no); verdict rows identical before and after the forced line: $([ "$vbefore" = "$vafter" ] && echo yes || echo no); FilmCraft rows now: $(grep -E 'T1 FilmCraft' <<<"$vafter" | cut -d'|' -f4 | cut -c1-90)" "FORCE_BAD_ASSET=1 --only filmcraft v0.9.0 leaves a stage envelope flagged forced_bad_asset, and VERDICT-SP1A.md does not say T1/T2 were NOT RUN because the download was blocked"
  # Each tarball is fetched once (the ledger rule). If EffectCraft was fetched already and its T1 envelope is a real PASS for that same hash, reuse that evidence.
  ledf="$EVID/download_ledger.jsonl"; t1ef="$EVID/t1_effectcraft_v0.11.1.json"
  lnum="$(grep -n '"app": "effectcraft"' "$ledf" 2>/dev/null | head -1 | cut -d: -f1)"
  lhash="$(sed -n "${lnum:-0}p" "$ledf" 2>/dev/null | jq -r '.sha256' 2>/dev/null)"; thash="$(jq -r '.pins[]|select(.app=="effectcraft" and .tag=="v0.11.1")|.linux_x86_64_tarball.sha256' "$SP1/release_assets.json" 2>/dev/null)"
  left="$(ls -A "$ROOT/vendor/craft" 2>/dev/null | grep -v '^_keep$' | tr '\n' ' ')"
  if [ -n "$lnum" ] && [ -n "$thash" ] && [ "$lhash" = "$thash" ] && [ -z "$left" ] && jq -e '.status=="PASS" and .detail.mini!=true' "$t1ef" >/dev/null 2>&1; then
    rec PASS effectcraft.t1only_real "fetched once already (ledger line $lnum, $(sed -n "${lnum}p" "$ledf" | jq -r '.date_utc')); evidence reused, no second download: $(jq -r '.actual' "$t1ef"); the recorded sha256 equals the table; vendor/craft leftovers: none" "sha256 equals the R8 table, T1 JSON written, tarball and tree deleted, df back within 10 MB"
  else
  before="$(df -BM / | awk 'NR==2{gsub("M","",$4); print $4}')"
  out="$(bash "$SP1/run_sp1.sh" --only effectcraft v0.11.1 --t1-only 2>&1)"; rc=$?
  after="$(df -BM / | awk 'NR==2{gsub("M","",$4); print $4}')"
  left="$(ls -A "$ROOT/vendor/craft" 2>/dev/null | grep -v '^_keep$' | tr '\n' ' ')"
  if [ $rc = 3 ] && grep -q 'REFUSED:' <<<"$out"; then
    rec BLOCKED effectcraft.t1only_real "$(grep -m1 'REFUSED:' <<<"$out")" "sha256 equals the R8 table, T1 JSON written, tarball and tree deleted, df back within 10 MB"
  elif [ $rc = 0 ]; then
    d=$(( before - after )); [ $d -lt 0 ] && d=$(( -d ))
    check effectcraft.t1only_real "$(grep -q 'also equals the independent value' <<<"$out" && [ -z "$left" ] && [ "$d" -le 10 ] && jq -e '.status=="PASS"' "$EVID/t1_effectcraft_v0.11.1.json" >/dev/null && echo 1 || echo 0)" "exit 0; sha256 matches the independent value: $(grep -c 'also equals the independent value' <<<"$out"); vendor/craft leftovers: ${left:-none}; df moved ${d} MB (Avail ${before} -> ${after})" "sha256 equals the R8 table, T1 JSON written, tarball and tree deleted, df back within 10 MB"
  else
    rec FAIL effectcraft.t1only_real "exit $rc: $(tail -3 <<<"$out" | tr '\n' ' ' | cut -c1-400)" "sha256 equals the R8 table, T1 JSON written, tarball and tree deleted, df back within 10 MB"
  fi
  fi
else
  rec SKIPPED sums.real_six_files "--skip-network" "network"; rec SKIPPED blocked.force_bad_asset "--skip-network" "network"; rec SKIPPED effectcraft.t1only_real "--skip-network" "network"
fi

# ------------------------------------------------------------------ ALL: the staged run, through its guard
out="$(bash "$SP1/run_sp1.sh" --list 2>&1)"; rc=$?
if [ $rc != 0 ]; then rec BLOCKED all.staged_run "$(grep -m1 '^REFUSED' <<<"$out") Neither profile fits at the live Avail; nothing was started." "run_sp1.sh --all runs FilmCraft then EffectCraft, vendor/craft ends with only _keep/, df within 10 MB of start plus the kept 70 MB, no envelope under avail_mb_min 250"
elif [ "$REAL_ALL" = 1 ]; then
  start="$(df -BM / | awk 'NR==2{gsub("M","",$4); print $4}')"
  out="$(bash "$SP1/run_sp1.sh" --all 2>&1)"; rc=$?; end="$(df -BM / | awk 'NR==2{gsub("M","",$4); print $4}')"
  left="$(ls -A "$ROOT/vendor/craft" 2>/dev/null | grep -v '^_keep$' | tr '\n' ' ')"
  minav="$(jq -s '[.[]|select(.schema=="lj-evidence/1")|.disk.avail_mb_min]|min' "$EVID"/*.json 2>/dev/null)"
  check all.staged_run "$([ $rc = 0 ] && [ -z "$left" ] && [ "${minav:-0}" -ge 250 ] && echo 1 || echo 0)" "exit $rc; vendor/craft leftovers: ${left:-none}; Avail $start -> $end MB; lowest avail_mb_min in any envelope: $minav" "full staged run"
else
  rec SKIPPED all.staged_run "the guard would allow it, but it takes hours: run 'bash spikes/sp1_craft_cli/run_sp1.sh --all' in the background, or pass --real-all" "full staged run"
fi

fi   # DEFECTS_ONLY
# ------------------------------------------------------------------ ALL: the mechanism tests with stand-ins
W="$(mktemp -d "$SCRATCH_ROOT/wp07-fake.XXXXXX")"
SRV=""
cleanup() { [ -n "$SRV" ] && kill "$SRV" 2>/dev/null; rm -rf "$W"; }
trap cleanup EXIT
if [ "$DEFECTS_ONLY" != 1 ]; then
python3 -I "$T/make_fake_release.py" --out "$W/ok" >/dev/null && python3 -I "$T/make_fake_release.py" --out "$W/flip" --flip-byte filmcraft >/dev/null
# the 'bug' tree: both FilmCraft tarballs carry the planted dissolve defect (it takes effect only under --profile full); the 'tamper' tree is the ok tree with one
# digit of the independent (R8) FilmCraft 0.9.0 tarball hash changed
python3 -I "$T/make_fake_release.py" --out "$W/bug" --bug dissolve >/dev/null
cp -r "$W/ok" "$W/tamper" && python3 -I - "$W/tamper/r8.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for e in d["expected"]:
    if e["app"] == "filmcraft" and e["tag"] == "v0.9.0" and e["kind"] == "linux_x86_64_tarball":
        e["sha256"] = ("0" if e["sha256"][0] != "0" else "1") + e["sha256"][1:]
json.dump(d, open(sys.argv[1], "w"), indent=1)
PY
python3 -u -m http.server 0 --bind 127.0.0.1 --directory "$W" > "$W/srv.log" 2>&1 9>&- &
SRV=$!
for _ in 1 2 3 4 5 6 7 8 9 10; do PORT="$(grep -oE 'port [0-9]+' "$W/srv.log" | head -1 | awk '{print $2}')"; [ -n "$PORT" ] && break; sleep 0.5; done
if [ -z "${PORT:-}" ]; then rec FAIL fake.server "the local fake release server did not start" "stand-in server"; echo "SUMMARY all: $NPASS PASS, $((FAILS)) FAIL"; exit 1; fi
fkrun() {  # fkrun REL NAME args...   (own vendor, evidence and scratch folders per NAME; the fake df says 2000 MB unless FAKE_DF is set)
  local rel="$1" name="$2"; shift 2
  mkdir -p "$W/v_$name" "$W/e_$name" "$W/s_$name"
  ( export LJ_RELEASE_BASE="http://127.0.0.1:$PORT/$rel/www" LJ_SP1_ASSETS="$W/$rel-assets.json" LJ_SP1_R8="$W/$rel/r8.json" LJ_SP1_VENDOR="$W/v_$name" \
      LJ_SP1_EVIDENCE="$W/e_$name" LJ_SCRATCH="$W/s_$name" LJ_SP1_VERDICT="$W/verdict_$name.md" SP1_FAKE_MINI=1 LJ_DF_CMD="${FAKE_DF:-$T/fake_df_2000.sh}"; bash "$SP1/run_sp1.sh" "$@" 2>&1 )
}
out="$(fkrun ok sums --sums-only)"; rc=$?
fkrun flip sums_flip --sums-only >/dev/null
fkrun bug sums_bug --sums-only >/dev/null
# a tampered independent (R8) value: the sums step says STOP AND REPORT and writes usable=false, and a stage run against that table refuses BEFORE any download
outt="$(fkrun tamper sums_tamper --sums-only)"; rct=$?
outs="$(fkrun tamper tam --only filmcraft v0.9.0 --profile lean)"; rcs=$?
tusable="$(jq -r '.usable' "$W/tamper-assets.json" 2>/dev/null)"; tled="$(nlines "$W/e_tam/download_ledger.jsonl")"
check fake.sums_only "$([ $rc = 0 ] && grep -q 'R8 comparison: all match' <<<"$out" && [ "$rct" = 1 ] && grep -q 'STOP AND REPORT' <<<"$outt" && [ "$tusable" = false ] && [ "$rcs" = 1 ] && grep -q 'usable=false' <<<"$outs" && grep -q 'STOP AND REPORT' <<<"$outs" && ! grep -q 'preflight HEAD' <<<"$outs" && ! grep -q 'curl' <<<"$outs" && [ "$tled" = 0 ] && [ -z "$(ls -A "$W/v_tam" 2>/dev/null)" ] && echo 1 || echo 0)" "exit $rc: $(tail -1 <<<"$out" | sed "s#$W#<fake>#g"); tampered R8 value: sums step exit $rct (usable=$tusable), then a stage on that table: exit $rcs, 'usable=false' shown: $(grep -c 'usable=false' <<<"$outs"), downloads recorded: $tled, vendor leftovers: $(ls -A "$W/v_tam" 2>/dev/null | tr '\n' ' ' | sed 's/^$/none/')" "the sums path works end to end against a local server (fake hashes); a tampered independent value gives usable=false and a stage refuses that table before downloading anything"
# the flip tree has its own table: its sums list the intact hash, the served tarball has one byte flipped

scn_filmcraft() {  # sets R_OK and R_DETAIL
  local sfx="$1" out rc ev kept left fails ncrit hk hs
  FC_SFX="$sfx"
  out="$(fkrun ok fc$sfx --only filmcraft v0.9.0 --profile lean)"; rc=$?; LAST_OUT="$out"
  ev="$W/e_fc$sfx"; kept="$(ls "$W/v_fc$sfx/_keep" 2>/dev/null | tr '\n' ' ')"; left="$(ls -A "$W/v_fc$sfx" | grep -v '^_keep$' | tr '\n' ' ')"
  fails="$(jq -r '[.detail.criteria[]|select(.pass==false)|.id]|join(",")' "$ev/t2_filmcraft_v0.9.0_mini.json" 2>/dev/null)"; ncrit="$(jq -r '.detail.criteria|length' "$ev/t2_filmcraft_v0.9.0_mini.json" 2>/dev/null)"
  hk="$(sha256sum "$W/v_fc$sfx/_keep/"*.tar.gz 2>/dev/null | cut -d' ' -f1)"; hs="$(jq -r '.pins[]|select(.app=="filmcraft" and .tag=="v0.9.0")|.linux_x86_64_tarball.sha256' "$W/ok-assets.json")"
  R_OK=0; [ $rc = 0 ] && [ -z "$fails" ] && [ "${ncrit:-0}" -ge 12 ] && [ -z "$left" ] && [ "$hk" = "$hs" ] && grep -q 'moved to' <<<"$out" && R_OK=1
  R_DETAIL="exit $rc; T2 criteria ${ncrit:-none}, failing: ${fails:-none}; _keep: ${kept:-nothing}; verified kept sha equals the table: $([ "$hk" = "$hs" ] && echo yes || echo no); other leftovers: ${left:-none}"
}
scn_effectcraft() {
  local sfx="$1" out rc ev fails ncrit left
  out="$(fkrun ok ec$sfx --only effectcraft v0.11.1 --profile lean)"; rc=$?; LAST_OUT="$out"
  ev="$W/e_ec$sfx"; fails="$(jq -r '[.detail.criteria[]|select(.pass==false)|.id]|join(",")' "$ev/t4_effectcraft_v0.11.1_mini.json" 2>/dev/null)"; ncrit="$(jq -r '.detail.criteria|length' "$ev/t4_effectcraft_v0.11.1_mini.json" 2>/dev/null)"
  left="$(ls -A "$W/v_ec$sfx" | tr '\n' ' ')"
  R_OK=0; [ $rc = 0 ] && [ -z "$fails" ] && [ "${ncrit:-0}" -ge 9 ] && [ -z "$left" ] && R_OK=1
  R_DETAIL="exit $rc; T4 criteria ${ncrit:-none}, failing: ${fails:-none}; vendor leftovers: ${left:-none} (EffectCraft's tarball is deleted with its tree)"
}
# On a volume that is nearly full another job can make a tiny write fail. A stage scenario that fails while Avail is under 40 MB is run ONCE more, and says so.
with_retry() {  # with_retry NAME FUNCTION EXPECTED
  local name="$1" fn="$2" exp="$3" note=""
  "$fn" ""
  if [ "$R_OK" != 1 ] && [ "$(avail_mb)" -lt 40 ]; then note=" [first attempt failed with Avail $(avail_mb) MB, so it was run once more; first attempt: ${R_DETAIL}]"; "$fn" "_r"; fi
  check "$name" "$R_OK" "$R_DETAIL$note" "$exp"
}
with_retry fake.filmcraft_stage_and_keep scn_filmcraft "a FilmCraft stage runs T1+T2, deletes tree and stills, keeps the verified tarball in _keep/"
n1="$(nlines "$W/e_fc$FC_SFX/download_ledger.jsonl")"
out="$(fkrun ok fc$FC_SFX --only filmcraft v0.9.0 --profile lean --t1-only)"; rc=$?; LAST_OUT="$out"
n2="$(nlines "$W/e_fc$FC_SFX/download_ledger.jsonl")"
check fake.kept_tarball_reused "$([ $rc = 0 ] && [ "$n1" = 1 ] && [ "$n2" -le 1 ] && grep -q 'no second download' <<<"$out" && echo 1 || echo 0)" "exit $rc; ledger lines for the first stage $n1, after the second run $n2; $(grep -c 'no second download' <<<"$out") reuse message" "a second FilmCraft run uses the kept tarball and records no second download"
# a corrupt kept tarball is removed and fetched again (and the run after that reuses the new one)
out1="$(fkrun ok kc --only filmcraft v0.9.0 --profile lean --t1-only)"; rc1=$?
kfile="$(ls "$W/v_kc/_keep/"*.tar.gz 2>/dev/null | head -1)"
if [ -n "$kfile" ]; then python3 -I - "$kfile" <<'PY'
import sys
b = bytearray(open(sys.argv[1], "rb").read()); b[len(b) // 2] ^= 1; open(sys.argv[1], "wb").write(bytes(b))
PY
fi
out2="$(fkrun ok kc --only filmcraft v0.9.0 --profile lean --t1-only)"; rc2=$?; LAST_OUT="$out2"
kled="$W/e_kc/download_ledger.jsonl"; kn2="$(nlines "$kled")"; kex="$(sed -n 2p "$kled" 2>/dev/null | jq -r '.exception' 2>/dev/null)"
khash="$(sha256sum "$W/v_kc/_keep/"*.tar.gz 2>/dev/null | cut -d' ' -f1)"
out3="$(fkrun ok kc --only filmcraft v0.9.0 --profile lean --t1-only)"; rc3=$?; kn3="$(nlines "$kled")"
kleft="$(ls -A "$W/v_kc" | grep -v '^_keep$' | tr '\n' ' ')"
hs_ok="$(jq -r '.pins[]|select(.app=="filmcraft" and .tag=="v0.9.0")|.linux_x86_64_tarball.sha256' "$W/ok-assets.json")"
LJ_SP1_EVIDENCE="$W/e_kc" LJ_SP1_ASSETS="$W/ok-assets.json" python3 -I "$DRV/asset_tool.py" ledger --check >/dev/null 2>&1; lrc=$?
check fake.kept_tarball_corrupt_recovers "$([ "$rc1" = 0 ] && [ -n "$kfile" ] && [ "$rc2" = 0 ] && grep -q 'kept tarball was corrupt and has been removed' <<<"$out2" && grep -q 'REJECTED' <<<"$out2" && [ "$kn2" = 2 ] && [ "$kex" = 'kept tarball rejected' ] && [ "$khash" = "$hs_ok" ] && [ "$rc3" = 0 ] && [ "$kn3" = 2 ] && grep -q 'no second download' <<<"$out3" && [ -z "$kleft" ] && [ "$lrc" = 0 ] && echo 1 || echo 0)" "run 1 exit $rc1 (kept: $([ -n "$kfile" ] && echo yes || echo no)); one byte flipped in _keep/; run 2 exit $rc2 (corrupt-and-removed message: $(grep -c 'kept tarball was corrupt' <<<"$out2")), ledger lines $kn2, second line exception: ${kex:-none}, new _keep tarball equals the table: $([ "$khash" = "$hs_ok" ] && echo yes || echo no); run 3 exit $rc3, ledger lines $kn3, reused without a download: $(grep -c 'no second download' <<<"$out3"); ledger check exit $lrc; other leftovers: ${kleft:-none}" "a kept tarball that fails the SHA-256 check is removed, fetched again in the same stage (recorded ledger exception) and the next run uses the new one"
with_retry fake.effectcraft_stage scn_effectcraft "an EffectCraft stage runs T1+T4 and deletes everything"
# a corrupted tarball
out="$(fkrun flip bad --only filmcraft v0.9.0 --profile lean)"; rc=$?
left="$(ls -A "$W/v_bad" | tr '\n' ' ')"
check fake.corrupt_tarball_rejected "$([ $rc = 1 ] && grep -q 'REJECTED' <<<"$out" && ! grep -q 'extracting' <<<"$out" && ! grep -q '\[3/6\]' <<<"$out" && [ -z "$left" ] && jq -e '.status=="FAIL" and (.actual|contains("hash mismatch (stop and report)")) and .detail.hash_rejected==true' "$W/e_bad/stage_filmcraft-v0.9.0.json" >/dev/null && echo 1 || echo 0)" "exit $rc (a rejected hash is exit 1, never the internal 4); REJECTED shown: $(grep -c REJECTED <<<"$out"); extraction started: $(grep -c 'extracting' <<<"$out"); leftovers: ${left:-none}; stage envelope: $(jq -r '.status + " / " + .actual' "$W/e_bad/stage_filmcraft-v0.9.0.json" 2>/dev/null | cut -c1-90)" "a tarball with one flipped byte is rejected before it is listed or extracted, nothing is left behind, and the stage envelope says FAIL: hash mismatch (stop and report)"
# a hash mismatch in --all is STOP AND REPORT: no 0.8.0 fetch, no EffectCraft stage
out="$(fkrun flip stopall --all --profile lean)"; rc=$?
led="$W/e_stopall/download_ledger.jsonl"; nled="$(nlines "$led")"; n08="$(grep -c 'filmcraft-0.8.0' "$led" 2>/dev/null)"; nec="$(grep -c 'effectcraft' "$led" 2>/dev/null)"
left="$(ls -A "$W/v_stopall" | tr '\n' ' ')"
check fake.hash_mismatch_stops_all "$([ $rc = 1 ] && grep -q 'STOP AND REPORT' <<<"$out" && ! grep -q 'failed T1 or T2' <<<"$out" && ! grep -q '== stage filmcraft-v0.8.0' <<<"$out" && ! grep -q '== stage effectcraft' <<<"$out" && [ "$nled" = 1 ] && [ "${n08:-0}" = 0 ] && [ "${nec:-0}" = 0 ] && [ ! -e "$W/e_stopall/stage_filmcraft-v0.8.0.json" ] && [ ! -e "$W/e_stopall/stage_effectcraft-v0.11.1.json" ] && [ -z "$left" ] && jq -e '.status=="FAIL"' "$W/e_stopall/stage_filmcraft-v0.9.0.json" >/dev/null && echo 1 || echo 0)" "exit $rc; STOP AND REPORT shown: $(grep -c 'STOP AND REPORT' <<<"$out"); ledger lines $nled (0.8.0: ${n08:-0}, EffectCraft: ${nec:-0}); 0.8.0 or EffectCraft stage started: $(grep -c '== stage \(filmcraft-v0.8.0\|effectcraft\)' <<<"$out"); leftovers: ${left:-none}; stage envelope: $(jq -r .status "$W/e_stopall/stage_filmcraft-v0.9.0.json" 2>/dev/null)" "--all with a flipped-byte FilmCraft 0.9.0 tarball stops and reports (exit 1): the 0.8.0 fallback is not fetched and EffectCraft is not started"
# the legitimate 0.8.0 fallback: 0.9.0 passes its hash and fails T2 (planted dissolve defect, full profile only), so 0.8.0 is fetched, then EffectCraft runs anyway
out="$(fkrun bug fb --all --profile full)"; rc=$?; LAST_OUT="$out"
led="$W/e_fb/download_ledger.jsonl"; nled="$(nlines "$led")"; n08="$(grep -c 'filmcraft-0.8.0' "$led" 2>/dev/null)"
left="$(ls -A "$W/v_fb" | grep -v '^_keep$' | tr '\n' ' ')"
check fake.t2_fail_fetches_fallback "$([ $rc = 1 ] && grep -q 'failed T1 or T2 (exit 1), so the fallback 0.8.0 is fetched' <<<"$out" && ! grep -q 'STOP AND REPORT' <<<"$out" && [ "${n08:-0}" = 1 ] && [ "$nled" = 3 ] && [ -f "$W/e_fb/stage_filmcraft-v0.8.0.json" ] && [ -f "$W/e_fb/stage_effectcraft-v0.11.1.json" ] && jq -e '.status=="FAIL"' "$W/e_fb/stage_filmcraft-v0.9.0.json" >/dev/null && [ -z "$left" ] && echo 1 || echo 0)" "exit $rc; fallback line shown: $(grep -c 'so the fallback 0.8.0 is fetched' <<<"$out"); ledger lines $nled (0.8.0: ${n08:-0}); stage envelopes: 0.9.0 $(jq -r .status "$W/e_fb/stage_filmcraft-v0.9.0.json" 2>/dev/null), 0.8.0 $(jq -r .status "$W/e_fb/stage_filmcraft-v0.8.0.json" 2>/dev/null), EffectCraft $(jq -r .status "$W/e_fb/stage_effectcraft-v0.11.1.json" 2>/dev/null); leftovers: ${left:-none}" "--all with a FilmCraft 0.9.0 that passes its hash and fails T2 fetches the 0.8.0 fallback (the only reason it ever is), then still runs EffectCraft, and exits 1"
# the plan's own acceptance order: EffectCraft --t1-only (tree and tarball deleted), then --all fetches it a second time WITH a recorded exception
out1="$(fkrun ok t1all --only effectcraft v0.11.1 --t1-only --profile lean)"; rc1=$?
out2="$(fkrun ok t1all --all --profile lean)"; rc2=$?; LAST_OUT="$out2"
led="$W/e_t1all/download_ledger.jsonl"; nled="$(nlines "$led")"; lex3="$(sed -n 3p "$led" 2>/dev/null | jq -r '.asset + " | " + .exception' 2>/dev/null)"
LJ_SP1_EVIDENCE="$W/e_t1all" LJ_SP1_ASSETS="$W/ok-assets.json" python3 -I "$DRV/asset_tool.py" ledger --check >/dev/null 2>&1; lrc=$?
check fake.t1only_then_all_ledger_clean "$([ "$rc1" = 0 ] && [ "$rc2" = 0 ] && [ "$nled" = 3 ] && [ "$lex3" = 'effectcraft-0.11.1-linux-x86_64.tar.gz | re-fetch: the earlier copy (stage effectcraft-v0.11.1, t1-only) was deleted with its tree' ] && grep -q 'second fetch is recorded with the exception' <<<"$out2" && ! grep -q 'LEDGER PROBLEM' <<<"$out2" && [ "$lrc" = 0 ] && echo 1 || echo 0)" "--t1-only exit $rc1, then --all exit $rc2; ledger lines $nled; line 3: ${lex3:-none}; --ledger-check exit $lrc; LEDGER PROBLEM shown: $(grep -c 'LEDGER PROBLEM' <<<"$out2")" "--only effectcraft --t1-only followed by --all fetches EffectCraft twice with the second fetch recorded as an exception, so --ledger-check stays at exit 0"
# SP1_LEDGER_EXCEPTION: the real reason replaces the generic text on a repeat fetch, and a first fetch stays without an exception (week-2 gate review, nudge 6)
out1="$(SP1_LEDGER_EXCEPTION='re-fetch: stand-in reason, the kept copy was consumed by an earlier test' fkrun ok exc --only effectcraft v0.11.1 --t1-only --profile lean)"; rc1=$?
out2="$(SP1_LEDGER_EXCEPTION='re-fetch: stand-in reason, the kept copy was consumed by an earlier test' fkrun ok exc --only effectcraft v0.11.1 --profile lean)"; rc2=$?; LAST_OUT="$out2"
led="$W/e_exc/download_ledger.jsonl"; nled="$(nlines "$led")"; ex1="$(sed -n 1p "$led" 2>/dev/null | jq -r '.exception' 2>/dev/null)"; ex2="$(sed -n 2p "$led" 2>/dev/null | jq -r '.exception' 2>/dev/null)"
LJ_SP1_EVIDENCE="$W/e_exc" LJ_SP1_ASSETS="$W/ok-assets.json" python3 -I "$DRV/asset_tool.py" ledger --check >/dev/null 2>&1; lrc=$?
check fake.ledger_exception_names_real_reason "$([ "$rc1" = 0 ] && [ "$rc2" = 0 ] && [ "$nled" = 2 ] && [ -z "$ex1" ] && [ "$ex2" = 're-fetch: stand-in reason, the kept copy was consumed by an earlier test' ] && [ "$lrc" = 0 ] && echo 1 || echo 0)" "exit $rc1 then $rc2; ledger lines $nled; first fetch exception: ${ex1:-none}; repeat fetch exception: ${ex2:-none}; --ledger-check exit $lrc" "SP1_LEDGER_EXCEPTION replaces the generic repeat-fetch text with the real reason, leaves a first fetch without an exception, and --ledger-check stays at exit 0"
# a ledger that fails its check makes --all say so and exit 1 (two earlier EffectCraft fetches with no exception are seeded by hand through the ledger tool)
mkdir -p "$W/e_lp"
for _ in 1 2; do LJ_SP1_EVIDENCE="$W/e_lp" LJ_SP1_ASSETS="$W/ok-assets.json" python3 -I "$DRV/asset_tool.py" ledger --add effectcraft v0.11.1 --stage seeded >/dev/null 2>&1; done
out="$(fkrun ok lp --all --profile lean)"; rc=$?; LAST_OUT="$out"
check fake.all_prints_ledger_problem "$([ $rc = 1 ] && grep -q '^== LEDGER PROBLEM: ledger:.*PROBLEMS: effectcraft-0.11.1-linux-x86_64.tar.gz was fetched' <<<"$out" && ! grep -q '== after the run' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -m1 'LEDGER PROBLEM' <<<"$out" | cut -c1-200)" "--all prints 'LEDGER PROBLEM:' and exits 1 when the ledger check fails (it used to print the text and exit 0)"
# T2 writes its envelope after every phase, so a stage that is stopped (the 60-minute timeout, a disk-floor TERM, even a KILL) keeps what was measured
t2_interrupt() {  # t2_interrupt SIGNAL: start the T2 driver on the stand-in, signal it once the scaling phase has been written; sets SIG_RC and SIG_FILE
  local sig="$1" d="$W/t2i_$1" pid i
  mkdir -p "$d/cli" "$d/hw/home" "$d/hw/work" "$d/ev" "$d/sc"
  cp "$T/fake_craft/filmcraft-cli" "$d/cli/"; : > "$d/cli/fake_bug.txt"
  SIG_FILE="$d/ev/t2_filmcraft_v0.9.0_mini.json"
  ( export LJ_SP1_EVIDENCE="$d/ev" LJ_SCRATCH="$d/sc"; exec python3 -I "$DRV/t2_filmcraft.py" --tag v0.9.0 --cli "$d/cli/filmcraft-cli" --home "$d/hw/home" --work "$d/hw/work" --profile lean --mini >/dev/null 2>&1 ) 9>&- &
  pid=$!
  for i in $(seq 1 900); do grep -q '"phase_done": "scaling"' "$SIG_FILE" 2>/dev/null && break; sleep 0.1; done
  kill -"$sig" "$pid" 2>/dev/null; wait "$pid" 2>/dev/null; SIG_RC=$?
  pkill -KILL -f "$d/cli/filmcraft-cli" 2>/dev/null; sleep 0.3
}
t2_interrupt TERM
check fake.t2_envelope_survives_term "$([ "$SIG_RC" = 143 ] && jq -e '.status=="UNVERIFIED" and .detail.partial==true and (.detail.stopped|type)=="string" and (.detail.criteria|length)>=4 and (.detail.phase_done=="scaling" or .detail.phase_done=="export")' "$SIG_FILE" >/dev/null && echo 1 || echo 0)" "driver exit $SIG_RC after TERM; $(jq -r '[.status, (.detail.criteria|length|tostring)+" criteria", "phase "+.detail.phase_done, "stopped: "+(.detail.stopped//"no")]|join("; ")' "$SIG_FILE" 2>/dev/null | cut -c1-200)" "a TERM during T2 (the stage timeout or the disk guard) leaves an UNVERIFIED envelope with the criteria measured so far and a 'stopped' note"
t2_interrupt KILL
check fake.t2_envelope_survives_kill "$([ "$SIG_RC" = 137 ] && jq -e '.status=="UNVERIFIED" and .detail.partial==true and .detail.stopped==null and (.actual|startswith("stage still running")) and (.detail.criteria|length)>=4' "$SIG_FILE" >/dev/null && echo 1 || echo 0)" "driver exit $SIG_RC after KILL; $(jq -r '[.status, (.detail.criteria|length|tostring)+" criteria", .actual]|join("; ")' "$SIG_FILE" 2>/dev/null | cut -c1-200)" "even a KILL (no handler can run) leaves the envelope written after the scaling phase: UNVERIFIED, 'stage still running', its criteria intact"
# the guard refuses
out="$(FAKE_DF="$SP1/tests/fake_df_600.sh" fkrun ok ref --only filmcraft v0.9.0)"; rc=$?
nled="$(nlines "$W/e_ref/download_ledger.jsonl")"
check fake.guard_refuses_at_600 "$([ $rc = 3 ] && grep -q 'REFUSED: Avail 600 MB minus planned 350 MB leaves 250 MB' <<<"$out" && [ "$nled" = 0 ] && jq -e '.status=="BLOCKED"' "$W/e_ref/stage_filmcraft-v0.9.0.json" >/dev/null && echo 1 || echo 0)" "exit $rc; downloads recorded: $nled; stage envelope BLOCKED: $(jq -r .status "$W/e_ref/stage_filmcraft-v0.9.0.json" 2>/dev/null)" "at 600 MB the stage is refused before any download, with the exact message and a BLOCKED envelope"
# a stage that runs over its time limit (SP1_STAGE_TIMEOUT_S, 3600 s by default) is stopped; its envelope says TIMEOUT, not a disk refusal
out="$(SP1_STAGE_TIMEOUT_S=4 fkrun ok tmo --only filmcraft v0.9.0 --profile lean)"; rc=$?
left="$(ls -A "$W/v_tmo" | tr '\n' ' ')"; tact="$(jq -r '.actual' "$W/e_tmo/stage_filmcraft-v0.9.0.json" 2>/dev/null)"
check fake.stage_timeout_reason "$([ $rc = 3 ] && grep -q 'TIMEOUT: stage filmcraft-v0.9.0 ran for more than 4 s' <<<"$out" && jq -e '.status=="BLOCKED"' "$W/e_tmo/stage_filmcraft-v0.9.0.json" >/dev/null && grep -q 'TIMEOUT: the stage ran over 4 s and was stopped' <<<"$tact" && ! grep -qi 'disk guard refused' <<<"$tact" && [ -z "$left" ] && echo 1 || echo 0)" "exit $rc; stage envelope: ${tact:-none}; leftovers: ${left:-none}" "a stage stopped by its time limit exits 3, removes its folders, and its envelope (and so the verdict's disk line) says TIMEOUT instead of reading like a disk refusal"
# the disk floor appears mid-run: the guard stops the group, the stage cleans up
FLAG="$W/floor.flag"; ( sleep 7; touch "$FLAG" ) 9>&- &
out="$(LJ_FAKE_DF_FLAG="$FLAG" LJ_POLL_S=1 LJ_TERM_GRACE_S=15 FAKE_DF="$T/fake_df_flag.sh" fkrun ok flo --only filmcraft v0.9.0 --profile lean)"; rc=$?
left="$(ls -A "$W/v_flo" | tr '\n' ' ')"; stat="$(tail -1 "$W/s_flo/disk-ledger.jsonl" 2>/dev/null | jq -r '.status' 2>/dev/null)"
check fake.disk_floor_abort_cleans_up "$([ $rc = 3 ] && grep -q 'DISK-FLOOR' <<<"$out" && [ "$stat" = floor ] && [ -z "$left" ] && echo 1 || echo 0)" "exit $rc; guard status ${stat}; leftovers in vendor/craft: ${left:-none}" "when Avail falls under 250 MB mid-stage the guard stops the stage (exit 3) and the stage's trap removes its folders"
# the flipped-byte check on the Linux side by itself
good="$(ls "$W/ok/www/filmcraft/releases/download/v0.9.0/"*.tar.gz)"; cp "$good" "$W/good.tgz"; cp "$good" "$W/bad.tgz"
python3 -I - "$W/bad.tgz" <<'PY'
import sys
b = bytearray(open(sys.argv[1], "rb").read()); b[len(b) // 2] ^= 1; open(sys.argv[1], "wb").write(bytes(b))
PY
o1="$(LJ_SP1_ASSETS="$W/ok-assets.json" LJ_SP1_R8="$W/ok/r8.json" bash "$SP1/run_sp1.sh" --verify-tarball "$W/good.tgz" filmcraft v0.9.0 2>&1)"; r1=$?
o2="$(LJ_SP1_ASSETS="$W/ok-assets.json" LJ_SP1_R8="$W/ok/r8.json" bash "$SP1/run_sp1.sh" --verify-tarball "$W/bad.tgz" filmcraft v0.9.0 2>&1)"; r2=$?
check fake.verify_flipped_byte "$([ $r1 = 0 ] && [ $r2 = 1 ] && grep -q 'Nothing was extracted' <<<"$o2" && echo 1 || echo 0)" "intact -> exit $r1; one byte flipped -> exit $r2: $(cut -c1-90 <<<"$o2")" "--verify-tarball accepts the intact copy and rejects the copy with one byte flipped"
fi   # DEFECTS_ONLY
# planted defects: each must fail exactly its own criterion
bugrun() {  # bugrun APP BUGWORD EXPECTED_CRITERION [extra driver args]
  local app="$1" bug="$2" want="$3"; shift 3
  local d="$W/cli_${app}_$bug"; mkdir -p "$d" "$W/hw_${app}_$bug/home" "$W/hw_${app}_$bug/work" "$W/e_bug"
  cp "$T/fake_craft/${app}-cli" "$d/"; echo "$bug" > "$d/fake_bug.txt"
  local drv="t2_filmcraft.py" tag="v0.9.0" ev="t2_filmcraft_v0.9.0_mini.json"
  [ "$app" = effectcraft ] && drv="t4_effectcraft.py" tag="v0.11.1" ev="t4_effectcraft_v0.11.1_mini.json"
  ( export LJ_SP1_EVIDENCE="$W/e_bug" LJ_SCRATCH="$W/s_bug"; mkdir -p "$W/s_bug"; python3 -I "$DRV/$drv" --tag "$tag" --cli "$d/${app}-cli" --home "$W/hw_${app}_$bug/home" --work "$W/hw_${app}_$bug/work" --profile lean --mini "$@" >/dev/null 2>&1 ); local rc=$?
  local got; got="$(jq -r '[.detail.criteria[]|select(.pass==false)|.id]|join(",")' "$W/e_bug/$ev" 2>/dev/null)"
  local okk=0
  if [ "${want#has:}" != "$want" ]; then [ $rc = 1 ] && grep -q "${want#has:}" <<<"$got" && okk=1; else [ $rc = 1 ] && [ "$got" = "$want" ] && okk=1; fi
  check "fake.defect_${app}_$bug" "$okk" "driver exit $rc; failing criteria: ${got:-none} (expected ${want#has:}$([ "${want#has:}" != "$want" ] && echo ' among others'))" "planted defect '$bug' makes $want fail and nothing unrelated"
  rm -rf "$W/hw_${app}_$bug" "$d"
}
if [ "$SKIP_DEFECTS" != 1 ]; then
bugrun filmcraft leak T2.rss_slope
bugrun filmcraft offset T2.kenburns_positions
bugrun filmcraft dropframe T2.h264_frame_count,T2.prores_frame_count
bugrun filmcraft dissolve T2.mid_dissolve
bugrun filmcraft encodedblend T2.mid_dissolve
bugrun filmcraft stepped T2.dissolve_steps
bugrun filmcraft offline has:T2.offline_media_empty
bugrun filmcraft crash T2.no_crash_n12_conformed,T2.rss_n12
bugrun effectcraft noalpha T4.title_png_has_alpha,T4.line_png_has_alpha
bugrun effectcraft nondeterministic T4.determinism
bugrun effectcraft nodecode T4.prores4444_decodes
bugrun effectcraft slow T4.parallax_speed --parallax-max-s 0.05
fi   # SKIP_DEFECTS

echo "SUMMARY all$([ "$SKIP_DEFECTS" = 1 ] && echo " (part 1: the planted-defect lines are skipped; run --defects-only next)")$([ "$DEFECTS_ONLY" = 1 ] && echo " (part 2: the planted-defect lines only; counts are this run's)"): $NPASS PASS, $FAILS FAIL, $BLOCKED BLOCKED, $UNV UNVERIFIED, $(grep -c SKIPPED "$JSONL") SKIPPED"
python3 -I "$T/make_summary.py" all >/dev/null 2>&1
[ "$FAILS" -gt 0 ] && exit 1; [ "$BLOCKED" -gt 0 ] && exit 3; exit 0
