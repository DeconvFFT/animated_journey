#!/usr/bin/env bash
# run_sp1.sh: SP1a, the Craft CLIs in the container (FilmCraft 0.9.0, EffectCraft 0.11.1), one app at a time. Build plan WP-07.
#
#   bash spikes/sp1_craft_cli/run_sp1.sh --list                         planned downloads, sizes, df, the profile it would choose; exit 3 if it refuses
#   bash spikes/sp1_craft_cli/run_sp1.sh --sums-only                    fetch the six SHA256SUMS.txt, write release_assets.json, compare with the independent hashes
#   bash spikes/sp1_craft_cli/run_sp1.sh --only APP TAG [--t1-only]     one stage (filmcraft v0.9.0 | effectcraft v0.11.1 | filmcraft v0.8.0)
#   bash spikes/sp1_craft_cli/run_sp1.sh --all                          FilmCraft then EffectCraft (0.8.0 only if 0.9.0 fails T1 or T2); hours; run it in the background
#   bash spikes/sp1_craft_cli/run_sp1.sh --verify-tarball FILE APP TAG  SHA-256 check only (what every stage does BEFORE it extracts)
#   bash spikes/sp1_craft_cli/run_sp1.sh --ledger-check                 each tarball fetched once, under 2 GB
# Options: --profile full|lean|auto (default auto)   --wait SECONDS (poll for free disk before a stage; default 0)
#
# EACH STAGE (build plan 4.9, WP-07 item 3) is ONE lj_with_disk call that contains:
#   HEAD the asset (a wrong name or a blocked proxy ends here with blocked_proof.json and exit 3, before any disk is planned)
#   curl into a NEW EMPTY folder under vendor/craft/  ->  SHA-256 against release_assets.json and the independent value (a mismatch stops: nothing is extracted)
#   tar -tvzf (a listing writes nothing)  ->  the extraction plan  ->  tar -xzf of the planned members  ->  the tests  ->  cleanup
# The tests run the Craft binary by absolute path with env -i, a throw-away HOME, timeout, unshare -rn (when it works) and a 10 GB resident-memory watchdog.
# Profile (chosen from live Avail): full ~600 MB for FilmCraft (400 for EffectCraft) only if Avail minus planned stays at or above 400 MB; else lean
# ~350 MB (300): CLI members only, ProRes 1 second. Else exit 3 with the shortfall. Lean changes sizes and durations, never a pass criterion.
# KEEP RULE: the verified FilmCraft 0.9.0 tarball is moved to vendor/craft/_keep/ for WP-10's T3 when Avail after cleanup is at least 700 MB; WP-10 deletes it.
#
# Exit codes (build plan 4.3): 0 all done and passing; 1 a test failed or a hash did not match (a finding); 2 bad usage; 3 environment: the disk guard
# refused or tripped, the lock was busy, or a download was blocked.
# Test overrides (used by tests/sp1/run_tests.sh, never needed otherwise): LJ_RELEASE_BASE LJ_SP1_ASSETS LJ_SP1_VENDOR LJ_SP1_EVIDENCE LJ_DF_CMD LJ_SCRATCH
#   SP1_FAKE_MINI=1 (smaller test content for the fake CLIs). FORCE_BAD_ASSET=1 asks for a deliberately wrong asset name.
# It reads df and the network; it writes only under vendor/craft/, build/evidence/wp07/ and (via the guard) the scratch ledgers. It never runs anything
# outside the sandbox from a download, and never touches anything of the maker's.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
SELF="${BASH_SOURCE[0]}"
SP1="$(cd "$(dirname "$SELF")" && pwd)"
ROOT="$(cd "$SP1/../.." && pwd)"
DRV="$SP1/drivers"
CFG="$SP1/config.json"
ASSETS="${LJ_SP1_ASSETS:-$SP1/release_assets.json}"
VENDOR="${LJ_SP1_VENDOR:-$ROOT/vendor/craft}"
EVID="${LJ_SP1_EVIDENCE:-$ROOT/build/evidence/wp07}"
export LJ_SP1_EVIDENCE="$EVID" LJ_SP1_ASSETS="$ASSETS"
# shellcheck disable=SC1091
. "$ROOT/scripts/lj_guard.sh"

say() { printf '%s\n' "$*"; }
die() { printf 'run_sp1: %s\n' "$*" >&2; exit "${2:-2}"; }
py() { python3 -I "$@"; }
need_tools() { local t; for t in jq curl tar sha256sum python3 ffmpeg ffprobe; do command -v "$t" >/dev/null 2>&1 || die "missing tool: $t" 3; done; }

FLOOR="$(jq -r '.disk.floor_mb' "$CFG")"
KEEP_MIN="$(jq -r '.disk.keep_threshold_mb' "$CFG")"
stage_field() { jq -r --arg id "$1" --arg f "$2" '.stages[]|select(.id==$id)|.[$f]' "$CFG"; }
stage_planned() { jq -r --arg id "$1" --arg p "$2" '.stages[]|select(.id==$id)|.planned_mb[$p]' "$CFG"; }
asset_field() { jq -r --arg a "$1" --arg t "$2" --arg f "$3" '.pins[]|select(.app==$a and .tag==$t)|.linux_x86_64_tarball[$f]' "$ASSETS"; }
mb_up() { echo $(( ($1 + 1048575) / 1048576 )); }
commas() { printf '%s\n' "$1" | sed -e ':a' -e 's/\([0-9]\)\([0-9]\{3\}\)\($\|,\)/\1,\2\3/' -e 'ta'; }

# ----------------------------------------------------------------------------- --list
do_list() {
  need_tools
  local avail id app tag bytes name sha keepmb a pr ok planned left refusals="" chosen="" want="$1" full_ok=0
  avail="$(lj_df_avail_mb)"; [[ "$avail" =~ ^[0-9]+$ ]] || die "cannot read free disk space (df gave no number)" 3
  say "run_sp1.sh --list    (build plan 4.9 and WP-07; nothing is downloaded or written)"
  say ""
  say "Planned downloads (each tarball once in the fortnight; the six SHA256SUMS.txt are fetched separately by --sums-only):"
  local n=0 total=0
  for id in $(jq -r '.stages[].id' "$CFG"); do
    app="$(stage_field "$id" app)"; tag="$(stage_field "$id" tag)"
    bytes="$(asset_field "$app" "$tag" bytes)"; name="$(asset_field "$app" "$tag" name)"; sha="$(asset_field "$app" "$tag" sha256)"
    [[ "$bytes" =~ ^[0-9]+$ ]] || die "release_assets.json has no size for $app $tag; run --sums-only first" 3
    n=$((n + 1))
    if [[ "$(stage_field "$id" only_if)" == "null" ]]; then total=$((total + bytes)); say "  $n. $name  $(commas "$bytes") bytes  sha256 ${sha:0:12}...  ($(stage_field "$id" tests | jq -r 'join("+")' ))"
    else say "  ($n) $name  $(commas "$bytes") bytes  sha256 ${sha:0:12}...  only if $(stage_field "$id" only_if)"; fi
  done
  say "  total for the two stages: $(mb_up "$total") MB of the $(jq -r '.disk.download_allowance_mb' "$CFG") MB allowance (the fallback adds about 70 MB, only if it is needed)"
  say "  not fetched here: PhotoCraft, VectorCraft, LightCraft (WP-10); SoundCraft (not pinned, not fetched: D-12, T5 cut)"
  say ""
  say "Disk: df says Avail ${avail} MB now. Floor ${FLOOR} MB (Avail minus planned must stay at or above it), hard floor $(jq -r '.disk.hard_floor_mb' "$CFG") MB, keep rule ${KEEP_MIN} MB."
  say "Stage budgets (planned peak MB, from build plan 4.9; the FilmCraft tarball, ~70 MB, stays on disk for the EffectCraft stage if kept):"
  keepmb="$(mb_up "$(asset_field filmcraft v0.9.0 bytes)")"
  for pr in full lean; do
    a="$avail"; ok=1
    for id in $(jq -r '.stages[]|select(.only_if==null)|.id' "$CFG"); do
      planned="$(stage_planned "$id" "$pr")"; left=$((a - planned))
      if (( left < FLOOR )); then
        say "  $pr: $id plans ${planned} MB, Avail ${a} MB, leaves ${left} MB: REFUSED (needs Avail of at least $((planned + FLOOR)) MB)"
        refusals="${refusals}REFUSED: Avail ${a} MB minus planned ${planned} MB leaves ${left} MB, below the ${FLOOR} MB floor ($id, $pr profile).
"
        ok=0; break
      fi
      say "  $pr: $id plans ${planned} MB, Avail ${a} MB, leaves ${left} MB: ok"
      [[ "$(stage_field "$id" keep_tarball)" == "true" ]] && a=$((a - keepmb))
    done
    [[ "$pr" == full ]] && full_ok="$ok"
    if (( ok )) && [[ -z "$chosen" ]] && { [[ "$want" == auto || "$want" == "$pr" ]]; }; then chosen="$pr"; fi
  done
  say ""
  if [[ -n "$chosen" ]]; then
    local note=""; [[ "$chosen" == lean && "$full_ok" == 0 && "$want" == auto ]] && note=" (the full profile is refused at this Avail)"
    say "Chosen profile: ${chosen}${note}"
    say "OK: a $chosen run fits. Start it with: bash spikes/sp1_craft_cli/run_sp1.sh --all --profile $chosen"
    return 0
  fi
  local f1 l1
  f1=$(( $(stage_planned "$(jq -r '.stages[0].id' "$CFG")" full) + FLOOR )); l1=$(( $(stage_planned "$(jq -r '.stages[0].id' "$CFG")" lean) + FLOOR ))
  say "Chosen profile: none"
  printf '%s' "$refusals"
  say "Neither profile fits: the first stage needs Avail of at least ${f1} MB for full or ${l1} MB for lean, and Avail is ${avail} MB."
  say "Remedy: answer Q-1 (the regenerable pip cache may be cleared), or free space, or use --wait SECONDS to poll; nothing was started and nothing was forced."
  return 3
}

# ----------------------------------------------------------------------------- the stage
choose_profile_for() {  # $1 stage id, $2 requested profile -> prints full|lean, or nothing (refused)
  local id="$1" want="$2" avail pr
  avail="$(lj_df_avail_mb)"
  for pr in full lean; do
    [[ "$want" != auto && "$want" != "$pr" ]] && continue
    (( avail - $(stage_planned "$id" "$pr") >= FLOOR )) && { echo "$pr"; return 0; }
  done
  return 1
}

run_stage() {  # run_stage APP TAG PROFILE_REQUEST T1ONLY WAIT
  local app="$1" tag="$2" want="$3" t1only="$4" wait_s="$5" id="$1-$2" prof avail planned rc head waited=0 before after
  jq -e --arg id "$id" '.stages[]|select(.id==$id)' "$CFG" >/dev/null 2>&1 || die "$app $tag is not a stage of this spike (filmcraft v0.9.0, effectcraft v0.11.1, filmcraft v0.8.0)"
  [[ -f "$ASSETS" ]] || die "release_assets.json is missing; run --sums-only first" 3
  say "== stage $id: preflight HEAD (no disk planned yet)"
  head="$(py "$DRV/asset_tool.py" head "$app" "$tag")"; rc=$?
  say "$head"
  if (( rc != 0 )); then
    py "$DRV/finalize_stage.py" --id "$id" --status BLOCKED --reason "download blocked or asset missing: see blocked_proof.json" --profile none >/dev/null
    return 3
  fi
  while :; do
    prof="$(choose_profile_for "$id" "$want")" && break
    avail="$(lj_df_avail_mb)"
    if (( waited >= wait_s )); then
      local pl lp
      pl="$(stage_planned "$id" full)"; lp="$(stage_planned "$id" lean)"
      local msg
      if [[ "$want" == full ]]; then msg="REFUSED: Avail ${avail} MB minus planned ${pl} MB leaves $((avail - pl)) MB, below the ${FLOOR} MB floor ($id, full profile)."
      else msg="REFUSED: Avail ${avail} MB minus planned ${lp} MB leaves $((avail - lp)) MB, below the ${FLOOR} MB floor ($id, lean profile); full would need Avail of at least $((pl + FLOOR)) MB and lean at least $((lp + FLOOR)) MB."; fi
      say "$msg Remedy: answer Q-1 (clear the regenerable pip cache) or free space, or pass --wait SECONDS. Nothing was downloaded and nothing was forced."
      py "$DRV/finalize_stage.py" --id "$id" --status BLOCKED --reason "$msg" --profile none --planned "$lp" >/dev/null
      return 3
    fi
    say "  waiting for disk: Avail ${avail} MB, $id needs Avail of at least $(( $(stage_planned "$id" lean) + FLOOR )) MB for lean (${waited}s of ${wait_s}s)"
    sleep 20; waited=$((waited + 20))
  done
  planned="$(stage_planned "$id" "$prof")"
  say "== stage $id: profile $prof, planned ${planned} MB (live Avail $(lj_df_avail_mb) MB)"
  before="$(lj_df_avail_mb)"
  # a locked stage is at most 60 minutes (build plan 4.9): timeout ends it, and its cleanup trap runs on the TERM
  lj_with_disk "$planned" "sp1-$id-$prof" -- timeout --kill-after=60 "${SP1_STAGE_TIMEOUT_S:-3600}" bash "$SELF" --stage-inner "$app" "$tag" "$prof" "$t1only"
  rc=$?
  if (( rc == 124 )); then
    say "TIMEOUT: stage $id ran for more than ${SP1_STAGE_TIMEOUT_S:-3600} s and was stopped; the disk lock is released and its folders removed. Split the work into shorter stages."
    rc=3
  fi
  after="$(lj_df_avail_mb)"
  py "$DRV/finalize_stage.py" --id "$id" --profile "$prof" --planned "$planned" --exit "$rc" --df-before "${before:-0}" --df-after "${after:-0}" \
     --label "sp1-$id-$prof" --vendor "$VENDOR" || true
  return "$rc"
}

stage_inner() {  # runs inside lj_with_disk
  # these are globals on purpose: the EXIT trap runs after this function has returned
  local app="$1" tag="$2" prof="$3" t1only="$4" sha plan_json rc_t=0 cli listing
  id="$1-$2"; rc=0
  asset="$(asset_field "$app" "$tag" name)"; sha="$(asset_field "$app" "$tag" sha256)"
  work="$VENDOR/$id"; tree="$work/tree"; home="$work/home"; tb="$work/$asset"; keepdir="$VENDOR/_keep"; kept="$keepdir/$asset"
  reused=0; verified=0; KEEP_OK=0; AVAIL_AFTER_CLEAN=""
  # The first TERM (from the disk guard, and again from `timeout`) ends the stage; further TERMs must not cut the cleanup short.
  trap 'trap "" TERM INT HUP; exit 143' TERM INT HUP
  stage_cleanup() {
    trap "" TERM INT HUP
    rm -rf -- "$tree" "$home" "$work/stills" "$work/exports" "$work/t" "$work/listing.txt" "$work/members.txt" 2>/dev/null
    if (( verified )) && (( ! reused )) && [[ "$id" == "filmcraft-v0.9.0" && "$rc" -ne 143 && "${KEEP_OK:-0}" == 1 ]]; then
      mkdir -p "$keepdir" && mv -f -- "$tb" "$kept" 2>/dev/null && say "keep rule: $asset moved to ${kept#"$ROOT"/} for WP-10's T3 (Avail after cleanup ${AVAIL_AFTER_CLEAN:-?} MB, at least ${KEEP_MIN} MB)"
    fi
    rm -rf -- "$work" 2>/dev/null
  }
  trap 'stage_cleanup' EXIT
  mkdir -p "$VENDOR" || die "cannot create vendor/craft" 3
  if [[ -e "$work" ]]; then say "  removing a leftover folder of an earlier killed run: ${work#"$ROOT"/}"; rm -rf -- "$work"; fi
  mkdir "$work" || die "cannot create a new empty folder" 3
  [[ -z "$(ls -A "$work")" ]] || die "the stage folder is not empty" 3

  if [[ "$id" == "filmcraft-v0.9.0" && -f "$kept" ]]; then
    say "[1/6] a kept, verified tarball exists in _keep/; using it in place (no second download)"
    tb="$kept"; reused=1
  else
    say "[1/6] curl -> new empty folder ${work#"$ROOT"/}"
    py "$DRV/asset_tool.py" get "$app" "$tag" --dest "$tb"; rc=$?
    if (( rc != 0 )); then return "$rc"; fi
    py "$DRV/asset_tool.py" ledger --add "$app" "$tag" --stage "$id" >/dev/null
  fi
  say "[2/6] SHA-256 before anything is extracted"
  py "$DRV/asset_tool.py" verify "$tb" "$app" "$tag"; rc=$?
  if (( rc != 0 )); then
    py "$DRV/finalize_stage.py" --id "$id" --note "tarball rejected before extraction: hash or size mismatch (stop and report)" >/dev/null
    (( reused )) || rm -f -- "$tb"
    return 1
  fi
  verified=1
  say "[3/6] listing the tarball (tar -tvzf writes nothing)"
  listing="$work/listing.txt"
  tar -tvzf "$tb" > "$listing" 2>"$work/tar.err" || { say "tar could not list the tarball: $(head -c 300 "$work/tar.err")"; return 1; }
  plan_json="$(py "$DRV/asset_tool.py" plan "$listing" "$app" "$prof")" || { say "extraction plan failed: $plan_json"; return 1; }
  say "      plan: $(jq -c '{profile,files_total,all_mb:(.all_bytes/1048576|floor),chosen_count,chosen_mb,cli_member}' <<<"$plan_json")"
  local need_mb budget_mb tbmb
  tbmb="$(mb_up "$(stat -c %s "$tb")")"; need_mb="$(jq -r '(.chosen_mb|ceil)' <<<"$plan_json")"; budget_mb="${LJ_DISK_PLANNED_MB:-0}"
  if (( budget_mb > 0 )) && (( (reused ? 0 : tbmb) + need_mb + 60 > budget_mb )); then
    say "BLOCKED: the extraction would need $(( (reused ? 0 : tbmb) + need_mb + 60 )) MB (tarball ${tbmb} + members ${need_mb} + 60 for stills and exports), over the planned ${budget_mb} MB. Nothing was extracted. Use a smaller profile or ask for disk."
    py "$DRV/finalize_stage.py" --id "$id" --note "extraction exceeds the planned budget" >/dev/null
    return 3
  fi
  say "[4/6] extracting ${need_mb} MB into ${tree#"$ROOT"/}"
  mkdir -p "$tree" "$home"
  if [[ "$prof" == full ]]; then tar -xzf "$tb" -C "$tree" --no-same-owner 2>"$work/tar.err"; rc=$?
  else jq -r '.chosen[]' <<<"$plan_json" > "$work/members.txt"; tar -xzf "$tb" -C "$tree" --no-same-owner -T "$work/members.txt" 2>"$work/tar.err"; rc=$?; fi
  if (( rc != 0 )); then say "tar extraction failed: $(head -c 300 "$work/tar.err")"; return 1; fi
  cli="$tree/$(jq -r '.cli_member' <<<"$plan_json")"
  [[ -f "$cli" ]] || { say "the CLI member was not extracted"; return 1; }
  chmod u+x -- "$cli"
  say "[5/6] tests (Craft binary by absolute path; env -i, throw-away HOME, timeout, unshare -rn when it works, 10 GB RSS watchdog)"
  local dargs=(--app "$app" --tag "$tag" --cli "$cli" --home "$home" --work "$work" --profile "$prof" --plan-json "$plan_json")
  [[ "${SP1_FAKE_MINI:-}" == 1 ]] && dargs+=(--mini)   # tests only: small content for the stand-in CLIs
  py "$DRV/t1_smoke.py" "${dargs[@]}"; rc_t=$?
  if [[ "$t1only" != 1 && "$rc_t" -le 1 ]]; then
    local drv="t2_filmcraft.py"; [[ "$app" == effectcraft ]] && drv="t4_effectcraft.py"
    if (( rc_t == 0 )); then
      lj_bench py "$DRV/$drv" "${dargs[@]}"; local rc2=$?
      (( rc2 > rc_t )) && rc_t=$rc2
    else
      say "      T1 failed, so $drv is not run (it would only repeat the failure)"
    fi
  fi
  say "[6/6] cleanup (tree, home, stills, exports; the keep rule decides about the FilmCraft tarball)"
  rm -rf -- "$tree" "$home" "$work/stills" "$work/exports" "$work/t"
  AVAIL_AFTER_CLEAN="$(lj_df_avail_mb)"
  if [[ "$id" == "filmcraft-v0.9.0" ]]; then
    if (( reused )); then say "      (the kept tarball stays where it is for WP-10)"
    elif [[ "$AVAIL_AFTER_CLEAN" =~ ^[0-9]+$ ]] && (( AVAIL_AFTER_CLEAN >= KEEP_MIN )); then KEEP_OK=1
    else
      say "      keep rule: Avail after cleanup is ${AVAIL_AFTER_CLEAN} MB, below ${KEEP_MIN} MB, so the tarball is deleted and WP-10 will fetch it once more (a recorded ledger exception)"
      py "$DRV/finalize_stage.py" --id "$id" --note "keep refused: Avail ${AVAIL_AFTER_CLEAN} MB after cleanup is below ${KEEP_MIN} MB; WP-10 re-fetches once (ledger exception)" >/dev/null
    fi
  fi
  rc="$rc_t"
  return "$rc_t"
}

# ----------------------------------------------------------------------------- argument parsing
MODE=""; ONLY_APP=""; ONLY_TAG=""; T1ONLY=0; PROFILE=auto; WAIT=0; V_FILE=""; V_APP=""; V_TAG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) MODE=list;;
    --sums-only) MODE=sums;;
    --only) MODE=only; ONLY_APP="${2:-}"; ONLY_TAG="${3:-}"; shift 2 2>/dev/null || die "usage: --only APP TAG";;
    --t1-only) T1ONLY=1;;
    --all) MODE=all;;
    --profile) PROFILE="${2:-}"; shift;;
    --wait) WAIT="${2:-0}"; shift;;
    --ledger-check) MODE=ledger;;
    --verify-tarball) MODE=verify; V_FILE="${2:-}"; V_APP="${3:-}"; V_TAG="${4:-}"; shift 3 2>/dev/null || die "usage: --verify-tarball FILE APP TAG";;
    --stage-inner) MODE=inner; ONLY_APP="${2:-}"; ONLY_TAG="${3:-}"; PROFILE="${4:-}"; T1ONLY="${5:-0}"; shift 4;;
    -h|--help) sed -n '2,32p' "$SELF"; exit 0;;
    *) die "unknown argument: $1 (try --help)";;
  esac
  shift
done
case "$PROFILE" in full|lean|auto) ;; *) die "--profile must be full, lean or auto";; esac
[[ "$WAIT" =~ ^[0-9]+$ ]] || die "--wait needs a whole number of seconds"
mkdir -p "$EVID"

case "$MODE" in
  list)   do_list "$PROFILE"; exit $?;;
  sums)   need_tools; py "$DRV/fetch_sums.py"; exit $?;;
  ledger) py "$DRV/asset_tool.py" ledger --check; exit $?;;
  verify) [[ -f "$V_FILE" ]] || die "no such file: $V_FILE"; py "$DRV/asset_tool.py" verify "$V_FILE" "$V_APP" "$V_TAG"; exit $?;;
  inner)  need_tools; stage_inner "$ONLY_APP" "$ONLY_TAG" "$PROFILE" "$T1ONLY"; exit $?;;
  only)   need_tools; run_stage "$ONLY_APP" "$ONLY_TAG" "$PROFILE" "$T1ONLY" "$WAIT"; exit $?;;
  all)
    need_tools
    start_avail="$(lj_df_avail_mb)"; overall=0
    say "run_sp1.sh --all: FilmCraft 0.9.0 then EffectCraft 0.11.1 (profile $PROFILE, wait ${WAIT}s per stage). df at start: Avail ${start_avail} MB."
    run_stage filmcraft v0.9.0 "$PROFILE" 0 "$WAIT"; rc1=$?
    if (( rc1 == 1 )); then
      say "== FilmCraft 0.9.0 failed T1 or T2 (exit 1), so the fallback 0.8.0 is fetched (the only reason it ever is)"
      run_stage filmcraft v0.8.0 "$PROFILE" 0 "$WAIT"; rc1b=$?
      (( rc1b > rc1 )) && rc1=$rc1b
    fi
    run_stage effectcraft v0.11.1 "$PROFILE" 0 "$WAIT"; rc2=$?
    (( rc1 > overall )) && overall=$rc1; (( rc2 > overall )) && overall=$rc2
    say "== after the run: $(py "$DRV/asset_tool.py" ledger --check)"
    left="$(ls -A "$VENDOR" 2>/dev/null | grep -v '^_keep$' | tr '\n' ' ')"
    say "== vendor/craft holds: ${left:-nothing but _keep/ (or nothing)}; df now Avail $(lj_df_avail_mb) MB (start ${start_avail} MB)"
    py "$DRV/verdict.py" >/dev/null 2>&1 || true
    exit "$overall";;
  *) die "give one of --list --sums-only --only --all --verify-tarball --ledger-check (try --help)";;
esac
