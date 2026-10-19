#!/usr/bin/env bash
# tests/sp1/run_tests.sh [--quick|--all] [--real-all] [--skip-network]    WP-07: SP1a, the Craft CLIs in the container
#
#   --quick  (at most 60 s, no downloads, no timed runs): syntax, the library self-test, the asset table, `--list` (live, and with the fake 900 MB and
#            600 MB df lines), the ledger check, the guide (regenerated, then check_guide.py), the memory watchdog, the public-repo lint.
#   --all    everything in --quick, plus
#            the real network lines: `--sums-only` (six small text files), the deliberately wrong asset (blocked_proof.json, exit 3), and
#            `--only effectcraft v0.11.1 --t1-only` (a real 64 MB download if the disk guard allows it, else BLOCKED with the guard's exact message);
#            the full staged run `--all` is ATTEMPTED only through its guard check here (it takes hours: start it by hand in the background, or pass --real-all);
#            and the MECHANISM tests: the same run_sp1.sh against a local fake release server and stand-in CLIs (tiny, fake df): a full FilmCraft and EffectCraft
#            stage, the keep rule, reuse of the kept tarball, a corrupted tarball rejected before extraction, the guard's refusal, a disk-floor abort that cleans up,
#            and planted defects (each must make exactly its own criterion FAIL). The stand-ins are not FilmCraft or EffectCraft and prove nothing about them.
# Options: --skip-network  skip the real network lines (for a machine without the proxy); --real-all  run the real hours-long `--all` if the guard allows it.
#
# One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail.  Exit 0 only if no line is FAIL or BLOCKED; exit 1 if a line FAILs; exit 3 if a line is
# BLOCKED (the disk guard refused a real stage: that is an environment fact, not a defect). Every line also writes an evidence envelope (build plan 4.2) to
# build/evidence/wp07/tests.jsonl (--all) or tests_quick.jsonl (--quick). Writes only under build/evidence/wp07/, vendor/craft/ (real stages) and a scratch folder it removes again.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
MODE=--quick; REAL_ALL=0; NET=1
while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick|--all) MODE="$1";;
    --real-all) REAL_ALL=1;;
    --skip-network) NET=0;;
    *) echo "usage: run_tests.sh [--quick|--all] [--real-all] [--skip-network]" >&2; exit 2;;
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
: > "$JSONL"
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
lean_need=$(( $(jq -r '.stages[0].planned_mb.lean' "$SP1/config.json") + 400 ))
want_rc=$([ "${avail:-0}" -ge "$lean_need" ] && echo 0 || echo 3)
check list.live "$([ "$rc" = "$want_rc" ] && grep -q 'Planned downloads' <<<"$out" && echo 1 || echo 0)" "Avail ${avail} MB: exit $rc (expected $want_rc: lean needs Avail of at least ${lean_need} MB); $(grep -E '^(Chosen profile|REFUSED)' <<<"$out" | head -2 | tr '\n' ' ')" "--list prints the plan and refuses (exit 3) exactly when Avail minus planned is under 400 MB"
out="$(LJ_DF_CMD="$SP1/tests/fake_df_900.sh" bash "$SP1/run_sp1.sh" --list 2>&1)"; rc=$?
check list.fake_900 "$([ $rc = 0 ] && grep -q 'full: filmcraft-v0.9.0 plans 600 MB, Avail 900 MB, leaves 300 MB: REFUSED' <<<"$out" && grep -q 'Chosen profile: lean' <<<"$out" && echo 1 || echo 0)" "exit $rc; $(grep -E 'full: filmcraft|Chosen profile' <<<"$out" | tr '\n' ' ' | cut -c1-300)" "at a fake 900 MB the full profile is refused and lean is chosen"
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
  out="$(FORCE_BAD_ASSET=1 bash "$SP1/run_sp1.sh" --only filmcraft v0.9.0 2>&1)"; rc=$?
  st="$(jq -r '.http_status' "$EVID/blocked_proof.json" 2>/dev/null)"; er="$(jq -r '.curl_stderr_verbatim' "$EVID/blocked_proof.json" 2>/dev/null)"
  check blocked.force_bad_asset "$([ $rc = 3 ] && [ "$st" = 404 ] && grep -q 'The requested URL returned error: 404' <<<"$er" && echo 1 || echo 0)" "exit $rc; blocked_proof.json: HTTP $st, curl said: $er" "a wrong asset name gives 404 -> blocked_proof.json with the exact status and curl stderr; exit 3"
  rm -f "$EVID/stage_filmcraft-v0.9.0.json"
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

# ------------------------------------------------------------------ ALL: the mechanism tests with stand-ins
W="$(mktemp -d "$SCRATCH_ROOT/wp07-fake.XXXXXX")"
SRV=""
cleanup() { [ -n "$SRV" ] && kill "$SRV" 2>/dev/null; rm -rf "$W"; }
trap cleanup EXIT
python3 -I "$T/make_fake_release.py" --out "$W/ok" >/dev/null && python3 -I "$T/make_fake_release.py" --out "$W/flip" --flip-byte filmcraft >/dev/null
python3 -u -m http.server 0 --bind 127.0.0.1 --directory "$W" > "$W/srv.log" 2>&1 9>&- &
SRV=$!
for _ in 1 2 3 4 5 6 7 8 9 10; do PORT="$(grep -oE 'port [0-9]+' "$W/srv.log" | head -1 | awk '{print $2}')"; [ -n "$PORT" ] && break; sleep 0.5; done
if [ -z "${PORT:-}" ]; then rec FAIL fake.server "the local fake release server did not start" "stand-in server"; echo "SUMMARY all: $NPASS PASS, $((FAILS)) FAIL"; exit 1; fi
fkrun() {  # fkrun REL NAME args...   (own vendor, evidence and scratch folders per NAME; the fake df says 2000 MB unless FAKE_DF is set)
  local rel="$1" name="$2"; shift 2
  mkdir -p "$W/v_$name" "$W/e_$name" "$W/s_$name"
  ( export LJ_RELEASE_BASE="http://127.0.0.1:$PORT/$rel/www" LJ_SP1_ASSETS="$W/$rel-assets.json" LJ_SP1_R8="$W/$rel/r8.json" LJ_SP1_VENDOR="$W/v_$name" \
      LJ_SP1_EVIDENCE="$W/e_$name" LJ_SCRATCH="$W/s_$name" SP1_FAKE_MINI=1 LJ_DF_CMD="${FAKE_DF:-$T/fake_df_2000.sh}"; bash "$SP1/run_sp1.sh" "$@" 2>&1 )
}
out="$(fkrun ok sums --sums-only)"; rc=$?
fkrun flip sums_flip --sums-only >/dev/null
check fake.sums_only "$([ $rc = 0 ] && grep -q 'R8 comparison: all match' <<<"$out" && echo 1 || echo 0)" "exit $rc: $(tail -1 <<<"$out" | sed "s#$W#<fake>#g")" "the sums path works end to end against a local server (fake hashes)"
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
with_retry fake.effectcraft_stage scn_effectcraft "an EffectCraft stage runs T1+T4 and deletes everything"
# a corrupted tarball
out="$(fkrun flip bad --only filmcraft v0.9.0 --profile lean)"; rc=$?
left="$(ls -A "$W/v_bad" | tr '\n' ' ')"
check fake.corrupt_tarball_rejected "$([ $rc = 1 ] && grep -q 'REJECTED' <<<"$out" && ! grep -q 'extracting' <<<"$out" && ! grep -q '\[3/6\]' <<<"$out" && [ -z "$left" ] && echo 1 || echo 0)" "exit $rc; REJECTED shown: $(grep -c REJECTED <<<"$out"); extraction started: $(grep -c 'extracting' <<<"$out"); leftovers: ${left:-none}" "a tarball with one flipped byte is rejected before it is listed or extracted, and nothing is left behind"
# the guard refuses
out="$(FAKE_DF="$SP1/tests/fake_df_600.sh" fkrun ok ref --only filmcraft v0.9.0)"; rc=$?
nled="$(nlines "$W/e_ref/download_ledger.jsonl")"
check fake.guard_refuses_at_600 "$([ $rc = 3 ] && grep -q 'REFUSED: Avail 600 MB minus planned 350 MB leaves 250 MB' <<<"$out" && [ "$nled" = 0 ] && jq -e '.status=="BLOCKED"' "$W/e_ref/stage_filmcraft-v0.9.0.json" >/dev/null && echo 1 || echo 0)" "exit $rc; downloads recorded: $nled; stage envelope BLOCKED: $(jq -r .status "$W/e_ref/stage_filmcraft-v0.9.0.json" 2>/dev/null)" "at 600 MB the stage is refused before any download, with the exact message and a BLOCKED envelope"
# the disk floor appears mid-run: the guard stops the group, the stage cleans up
FLAG="$W/floor.flag"; ( sleep 7; touch "$FLAG" ) 9>&- &
out="$(LJ_FAKE_DF_FLAG="$FLAG" LJ_POLL_S=1 LJ_TERM_GRACE_S=15 FAKE_DF="$T/fake_df_flag.sh" fkrun ok flo --only filmcraft v0.9.0 --profile lean)"; rc=$?
left="$(ls -A "$W/v_flo" | tr '\n' ' ')"; stat="$(tail -1 "$W/s_flo/disk-ledger.jsonl" 2>/dev/null | jq -r '.status' 2>/dev/null)"
check fake.disk_floor_abort_cleans_up "$([ $rc = 3 ] && grep -q 'DISK-FLOOR' <<<"$out" && [ "$stat" = floor ] && [ -z "$left" ] && echo 1 || echo 0)" "exit $rc; guard status ${stat}; leftovers in vendor/craft: ${left:-none}" "when Avail falls under 250 MB mid-stage the guard stops the stage (exit 3) and the stage's trap removes its folders"
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
bugrun filmcraft leak T2.rss_slope
bugrun filmcraft offset T2.kenburns_positions
bugrun filmcraft dropframe T2.h264_frame_count,T2.prores_frame_count
bugrun filmcraft dissolve T2.mid_dissolve
bugrun filmcraft offline has:T2.offline_media_empty
bugrun filmcraft crash T2.no_crash_n12_conformed,T2.rss_n12
bugrun effectcraft noalpha T4.title_png_has_alpha,T4.line_png_has_alpha
bugrun effectcraft nondeterministic T4.determinism
bugrun effectcraft nodecode T4.prores4444_decodes
bugrun effectcraft slow T4.parallax_speed --parallax-max-s 0.05
# the flipped-byte check on the Linux side by itself
good="$(ls "$W/ok/www/filmcraft/releases/download/v0.9.0/"*.tar.gz)"; cp "$good" "$W/good.tgz"; cp "$good" "$W/bad.tgz"
python3 -I - "$W/bad.tgz" <<'PY'
import sys
b = bytearray(open(sys.argv[1], "rb").read()); b[len(b) // 2] ^= 1; open(sys.argv[1], "wb").write(bytes(b))
PY
o1="$(LJ_SP1_ASSETS="$W/ok-assets.json" LJ_SP1_R8="$W/ok/r8.json" bash "$SP1/run_sp1.sh" --verify-tarball "$W/good.tgz" filmcraft v0.9.0 2>&1)"; r1=$?
o2="$(LJ_SP1_ASSETS="$W/ok-assets.json" LJ_SP1_R8="$W/ok/r8.json" bash "$SP1/run_sp1.sh" --verify-tarball "$W/bad.tgz" filmcraft v0.9.0 2>&1)"; r2=$?
check fake.verify_flipped_byte "$([ $r1 = 0 ] && [ $r2 = 1 ] && grep -q 'Nothing was extracted' <<<"$o2" && echo 1 || echo 0)" "intact -> exit $r1; one byte flipped -> exit $r2: $(cut -c1-90 <<<"$o2")" "--verify-tarball accepts the intact copy and rejects the copy with one byte flipped"

echo "SUMMARY all: $NPASS PASS, $FAILS FAIL, $BLOCKED BLOCKED, $UNV UNVERIFIED, $(grep -c SKIPPED "$JSONL") SKIPPED"
python3 -I "$T/make_summary.py" all >/dev/null 2>&1
[ "$FAILS" -gt 0 ] && exit 1; [ "$BLOCKED" -gt 0 ] && exit 3; exit 0
