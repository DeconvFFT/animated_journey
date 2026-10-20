#!/usr/bin/env bash
# run_sp1b.sh: SP1b, T1 and the read-backs on PhotoCraft, VectorCraft and LightCraft, and T3 on FilmCraft, on their LINUX CLIs. Build plan WP-10.
#
#   bash spikes/sp1b_readback/run_sp1b.sh --list                 sizes (release_assets.json), df, the stage plan; exit 3 if any stage's Avail minus planned is under 400 MB
#   bash spikes/sp1b_readback/run_sp1b.sh --all [--again]        the four stages, one app at a time (FilmCraft T3 first, from the tarball WP-07 kept); a refused stage is BLOCKED, not failed
#   bash spikes/sp1b_readback/run_sp1b.sh --only APP [--again]   one stage: photocraft | vectorcraft | lightcraft | filmcraft
#   bash spikes/sp1b_readback/run_sp1b.sh --ledger-check         python3 -I spikes/sp1b_readback/check_ledger.py: each of the five tarballs fetched once
#
# EACH STAGE is ONE lj_with_disk call (scripts/lj_guard.sh) that contains:
#   photocraft, vectorcraft, lightcraft:  curl into a NEW EMPTY folder under vendor/craft-sp1b/  ->  SHA-256 against release_assets.json (a mismatch stops: nothing is extracted)
#       ->  tar -tvzf (a listing writes nothing)  ->  the exact need (CLI member + outputs) against live Avail  ->  tar -xzf of the ONE member the CLI is  ->  the tarball is deleted
#       ->  T1 and the read-backs (visual_app.py) while the tree is on disk  ->  the tree is deleted
#   filmcraft:  the verified tarball WP-07 kept in vendor/craft/_keep/ (SHA-256 re-checked; if it is missing, ONE re-fetch with a recorded ledger exception)  ->  listing  ->  the one
#       CLI member  ->  T3 (t3_filmcraft.py)  ->  the tree AND the kept tarball are deleted (the one deliberate cross-package deletion: _keep/ is a git-ignored hand-off folder),
#       but only when T3 ran to a verdict (exit 0 or 1); after a harness problem (exit 2) or a block the tarball stays, so a retry needs no second download.
# The planned MB is computed (spikes/sp1b_readback/drivers/stage_budget.py): tarball + CLI member + outputs; the guard REFUSES unless Avail minus planned stays at or above 400 MB and
# stops the stage if Avail falls under 250 MB. A refused stage ends BLOCKED with the guard's exact message and the remedy (answer Q-1, or move the read-back to the maker's PC).
# Nothing is ever forced. Every result is labelled linux-cli: "Linux CLI result; not evidence for Windows".
# A stage whose envelope is already PASS or FAIL is not run again (its tarball is gone and a second fetch would need a recorded exception); --again runs it anyway and records
# the exception in the download ledger ("re-fetch: the earlier copy ... was deleted with its tree").
#
# Exit codes (build plan 4.3): 0 every stage PASS; 1 a stage FAILed (a finding) or its harness could not drive the CLI; 2 bad usage; 3 environment only (a stage BLOCKED by the disk guard,
# a busy lock, a blocked download, or an exact need that did not fit), and nothing failed.
# Test overrides (used by tests/spikes/run_tests.sh): LJ_RELEASE_BASE LJ_SP1_ASSETS LJ_SP1_R8 LJ_SP1_EVIDENCE LJ_SP1B_VENDOR LJ_SP1B_KEEP_DIR LJ_DF_CMD LJ_SCRATCH.
# It reads df and the network; it writes only under vendor/craft-sp1b/, build/evidence/wp10/ and (via the guard) the scratch ledgers; it deletes vendor/craft/_keep/ after T3.
# It never runs anything from a download outside the sandbox, and never touches anything of the maker's.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
SELF="${BASH_SOURCE[0]}"
SP="$(cd "$(dirname "$SELF")" && pwd)"
ROOT="$(cd "$SP/../.." && pwd)"
DRV="$SP/drivers"
SP1DRV="$ROOT/spikes/sp1_craft_cli/drivers"
CFG="$SP/config.json"
VENDOR="${LJ_SP1B_VENDOR:-$ROOT/vendor/craft-sp1b}"
KEEP="${LJ_SP1B_KEEP_DIR:-$ROOT/vendor/craft/_keep}"
EVID="${LJ_SP1_EVIDENCE:-$ROOT/build/evidence/wp10}"
export LJ_SP1_EVIDENCE="$EVID" LJ_SP1B_KEEP_DIR="$KEEP" LJ_SP1_ASSETS="${LJ_SP1_ASSETS:-$ROOT/spikes/sp1_craft_cli/release_assets.json}"
# shellcheck disable=SC1091
. "$ROOT/scripts/lj_guard.sh"

say() { printf '%s\n' "$*"; }
die() { printf 'run_sp1b: %s\n' "$*" >&2; exit "${2:-2}"; }
py() { python3 -I "$@"; }
need_tools() { local t; for t in jq curl tar sha256sum python3 readelf timeout xmllint; do command -v "$t" >/dev/null 2>&1 || die "missing tool: $t" 3; done; }
mb_up() { echo $(( ($1 + 1048575) / 1048576 )); }
stage_field() { jq -r --arg a "$1" --arg f "$2" '.stages[]|select(.app==$a)|.[$f]' "$CFG"; }
asset_field() { jq -r --arg a "$1" --arg t "$2" --arg f "$3" '.pins[]|select(.app==$a and .tag==$t)|.linux_x86_64_tarball[$f]' "$LJ_SP1_ASSETS"; }
env_status() { [[ -f "$EVID/$1.json" ]] && jq -r '.status' "$EVID/$1.json" 2>/dev/null || echo ""; }
FLOOR="$(jq -r '.disk.floor_mb' "$CFG")"
REMEDY="$(jq -r '.remedy' "$CFG")"

# ----------------------------------------------------------------------------- the stage (runs inside lj_with_disk)
stage_inner() {
  local app="$1" tag asset sha source plan_json rc_t=0 avail chk
  tag="$(stage_field "$app" tag)"; id="$app-$tag"; source="$(stage_field "$app" source)"
  asset="$(asset_field "$app" "$tag" name)"; sha="$(asset_field "$app" "$tag" sha256)"
  # globals on purpose (id, work, kept, ...): the EXIT trap runs after this function has returned
  work="$VENDOR/$id"; tree="$work/tree"; home="$work/home"; tb="$work/$asset"; kept="$KEEP/$asset"
  rc=0; reused=0; fetched=0; ran_tests=0; kept_deleted=0
  trap 'trap "" TERM INT HUP; exit 143' TERM INT HUP
  stage_cleanup() {
    trap "" TERM INT HUP
    rm -rf -- "$work" 2>/dev/null
    if (( reused )) && (( ran_tests )) && [[ "$rc" -le 1 ]]; then
      rm -f -- "$kept" && kept_deleted=1
      rmdir -- "$KEEP" 2>/dev/null
      say "kept tarball deleted after T3 (the hand-off folder ${KEEP#"$ROOT"/} is consumed)"
    fi
    if [[ -n "${SAMPLER:-}" ]]; then kill "$SAMPLER" 2>/dev/null; wait "$SAMPLER" 2>/dev/null; fi
    return 0
  }
  trap 'stage_cleanup' EXIT
  # the guard polls df every 5 s, which can miss the peak of a stage that lasts 13 s; this sampler reads it every 0.25 s and keeps the minimum (finalize_stage.py merges it)
  SAMPLER=""
  ( m=999999999; while :; do a="$(lj_df_avail_mb)"; if [[ "$a" =~ ^[0-9]+$ ]] && (( a < m )); then m="$a"; echo "$m" > "$EVID/.stage_$id.min"; fi; sleep 0.25; done ) &
  SAMPLER=$!
  mkdir -p "$VENDOR" || die "cannot create vendor/craft-sp1b" 3
  if [[ -e "$work" ]]; then say "  removing a leftover folder of an earlier killed run: ${work#"$ROOT"/}"; rm -rf -- "$work"; fi
  mkdir "$work" || die "cannot create a new empty folder" 3
  [[ -z "$(ls -A "$work")" ]] || die "the stage folder is not empty" 3

  fetch_tarball() {  # $1: ledger exception text or empty. Sets rc.
    local exc="$1"
    if [[ -z "$exc" ]]; then exc="$(py "$SP1DRV/asset_tool.py" ledger --refetch-exception "$app" "$tag")"; fi
    say "[1/7] curl -> new empty folder ${work#"$ROOT"/}"
    [[ -n "$exc" ]] && say "      this tarball is already in the download ledger; the second fetch is recorded with the exception: $exc"
    py "$SP1DRV/asset_tool.py" get "$app" "$tag" --dest "$tb"; rc=$?
    (( rc != 0 )) && return "$rc"
    if [[ -n "$exc" ]]; then py "$SP1DRV/asset_tool.py" ledger --add "$app" "$tag" --stage "$id" --exception "$exc" >/dev/null
    else py "$SP1DRV/asset_tool.py" ledger --add "$app" "$tag" --stage "$id" >/dev/null; fi
    fetched=1
    return 0
  }
  verify_tarball() {  # sets rc; rejected=1 only for a REJECTED answer
    local vout; rejected=0
    vout="$(py "$SP1DRV/asset_tool.py" verify "$tb" "$app" "$tag" 2>&1)"; rc=$?
    say "$vout"
    (( rc == 1 )) && [[ "$vout" == REJECTED:* ]] && rejected=1
    return "$rc"
  }
  local rejected=0
  if [[ "$source" == kept && -f "$kept" ]]; then
    say "[1/7] the tarball WP-07 kept is in ${KEEP#"$ROOT"/} (re-verified in the next step; no download)"
    tb="$kept"; reused=1
  else
    if [[ "$source" == kept ]]; then fetch_tarball "WP-07 could not keep the tarball (keep rule); one re-fetch" || return "$rc"
    else fetch_tarball "" || return "$rc"; fi
  fi
  say "[2/7] SHA-256 before anything is extracted"
  verify_tarball
  if (( rc != 0 )) && (( reused )) && (( rejected )); then
    rm -f -- "$kept"; rmdir -- "$KEEP" 2>/dev/null
    say "      the kept tarball was corrupt and has been removed from the hand-off folder; it is downloaded again in this stage (recorded as a ledger exception)"
    reused=0; tb="$work/$asset"
    fetch_tarball "kept tarball rejected" || return "$rc"
    say "[2/7] SHA-256 of the new download, before anything is extracted"
    verify_tarball
  fi
  if (( rc != 0 )); then
    if (( rejected )); then
      py "$DRV/finalize_stage.py" --id "$id" --note "tarball rejected before extraction: hash or size mismatch (stop and report)" >/dev/null
      rm -f -- "$tb"; return 4
    fi
    return "$rc"
  fi
  say "[3/7] listing the tarball (tar -tvzf writes nothing)"
  tar -tvzf "$tb" > "$work/listing.txt" 2>"$work/tar.err" || { say "tar could not list the tarball: $(head -c 300 "$work/tar.err")"; return 1; }
  plan_json="$(py "$DRV/stage_budget.py" plan "$work/listing.txt" "$app")" || { say "no CLI member in the tarball: $plan_json"; return 1; }
  say "      plan: $(jq -c '{files_total,all_mb,cli_member,cli_mb}' <<<"$plan_json")"
  say "[4/7] the exact need after the download (CLI member + outputs) against live Avail"
  avail="$(lj_df_avail_mb)"
  chk="$(py "$DRV/stage_budget.py" after-download "$work/listing.txt" "$app" "$avail")"
  say "      $chk"
  if [[ "$(jq -r '.ok' <<<"$chk")" != true ]]; then
    say "BLOCKED: after the download Avail is ${avail} MB and the CLI plus the outputs need $(jq -r '.need_mb' <<<"$chk") MB, which would leave $(jq -r '.leaves_mb' <<<"$chk") MB, below the ${FLOOR} MB floor. Nothing was extracted$( (( fetched )) && echo ', the tarball is deleted (a retry needs a recorded ledger exception)' || echo ', the kept tarball stays'). Remedy: $REMEDY."
    py "$DRV/finalize_stage.py" --id "$id" --note "BLOCKED after the download: $chk" >/dev/null
    return 3
  fi
  say "[5/7] extracting the one member the CLI is, into ${tree#"$ROOT"/}"
  mkdir -p "$tree" "$home"
  tar -xzf "$tb" -C "$tree" --no-same-owner "$(jq -r '.cli_member' <<<"$plan_json")" 2>"$work/tar.err"; rc=$?
  if (( rc != 0 )); then say "tar extraction failed: $(head -c 300 "$work/tar.err")"; return 1; fi
  cli="$tree/$(jq -r '.cli_member' <<<"$plan_json")"
  [[ -f "$cli" ]] || { say "the CLI member was not extracted"; return 1; }
  chmod u+x -- "$cli"
  if (( ! reused )); then rm -f -- "$tb"; say "      the tarball is deleted now that its one member is out (the ledger keeps the fetch)"; fi
  say "[6/7] tests (the CLI by absolute path; env -i, throw-away HOME, timeout, unshare -rn when it works, 10 GB RSS watchdog)"
  ran_tests=0
  if [[ "$source" == kept ]]; then
    py "$DRV/t3_filmcraft.py" --tag "$tag" --cli "$cli" --home "$home" --work "$work"; rc_t=$?
  else
    py "$DRV/visual_app.py" --app "$app" --tag "$tag" --cli "$cli" --home "$home" --work "$work" --plan-json "$plan_json"; rc_t=$?
  fi
  (( rc_t <= 1 )) && ran_tests=1
  say "[7/7] cleanup (tree, home, outputs$( (( reused )) && echo ', and the kept tarball' ))"
  rm -rf -- "$tree" "$home" "$work/t" "$work/t3" "$work/pc" "$work/vc" "$work/lc"
  rc="$rc_t"
  return "$rc_t"
}

# ----------------------------------------------------------------------------- one stage, from outside
run_stage() {  # run_stage APP AGAIN
  local app="$1" again="$2" tag id source planned bud rc head before after prev msgf reason="" fetch_flag
  tag="$(stage_field "$app" tag)"; id="$app-$tag"; source="$(stage_field "$app" source)"
  [[ -n "$tag" ]] || die "unknown app: $app (photocraft, vectorcraft, lightcraft, filmcraft)"
  [[ -f "$LJ_SP1_ASSETS" ]] || die "release_assets.json is missing; run spikes/sp1_craft_cli/run_sp1.sh --sums-only first" 3
  jq -e '.usable==true' "$LJ_SP1_ASSETS" >/dev/null || die "release_assets.json says usable=false (R8 or size mismatch): STOP AND REPORT; nothing is downloaded against this table" 1
  prev="$(env_status "stage_$id")"
  if [[ ( "$prev" == PASS || "$prev" == FAIL ) && "$again" != 1 ]]; then
    say "== stage $id: already run (status $prev, $EVID/stage_$id.json); not run again, because its tarball is gone and a second fetch needs a recorded exception. Use --again to run it anyway." | sed "s#$ROOT/##"
    [[ "$prev" == PASS ]] && return 0 || return 1
  fi
  bud="$(py "$DRV/stage_budget.py" budget "$app")" || die "cannot compute the budget for $app" 3
  planned="$(jq -r '.planned_mb' <<<"$bud")"; fetch_flag="$(jq -r '.fetch' <<<"$bud")"
  say "== stage $id: planned ${planned} MB ($(jq -r '"\(.cli_mb) MB CLI (\(.cli_basis)) + \(.outputs_mb) MB outputs"' <<<"$bud")$( [[ "$fetch_flag" == true ]] && echo " + $(jq -r '.tarball_mb_downloaded' <<<"$bud") MB tarball"))"
  if [[ "$fetch_flag" == true ]]; then
    say "   preflight HEAD (a wrong name or a blocked proxy ends here with blocked_proof.json and exit 3, before any disk is planned)"
    head="$(py "$SP1DRV/asset_tool.py" head "$app" "$tag")"; rc=$?
    say "   $head"
    if (( rc != 0 )); then
      py "$DRV/finalize_stage.py" --id "$id" --app "$app" --tag "$tag" --exit 3 --reason "download blocked or asset missing: see blocked_proof.json" --planned "$planned" >/dev/null
      return 3
    fi
  fi
  before="$(lj_df_avail_mb)"
  ledger_before="$(py "$SP1DRV/asset_tool.py" ledger --count "$app" "$tag")"
  kept_file="$KEEP/$(asset_field "$app" "$tag" name)"; kept_before=0; [[ "$source" == kept && -f "$kept_file" ]] && kept_before=1
  mkdir -p "${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
  msgf="$(mktemp "${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}/sp1b-msg.XXXXXX")"
  lj_with_disk "$planned" "sp1b-$id" -- timeout --kill-after=60 "$(jq -r '.budget.stage_timeout_s' "$CFG")" bash "$SELF" --stage-inner "$app" 2> >(tee "$msgf" >&2)
  rc=$?
  sleep 0.3   # let the tee behind the process substitution finish
  if (( rc == 124 )); then reason="TIMEOUT: the stage ran over the time limit and was stopped"; rc=3; fi
  if (( rc == 3 )) && [[ -z "$reason" ]]; then
    reason="$(grep -h -E '^lj_guard: (REFUSED|BUSY|DISK-FLOOR|cannot)' "$msgf" | head -1 | sed -e 's/^lj_guard: //')"
    [[ -z "$reason" ]] && reason="$(grep -h '^BLOCKED:' <(cat "$msgf") | head -1)"
  fi
  rm -f "$msgf"
  after="$(lj_df_avail_mb)"
  if (( rc == 3 )) && [[ -n "$reason" ]]; then say "BLOCKED: $reason"; [[ "$reason" == REFUSED* || "$reason" == BUSY* ]] && say "Remedy: $REMEDY."; fi
  (( rc == 4 )) && say "STOP AND REPORT: the $id tarball did not match its SHA-256 (or its listed size). Nothing was extracted, the bad file is deleted and nothing was forced."
  # what actually happened, not what was planned: a fetch is a new ledger line; the kept tarball is deleted only if it was there before and is gone now
  ledger_after="$(py "$SP1DRV/asset_tool.py" ledger --count "$app" "$tag")"
  fetched=0; [[ "$ledger_after" =~ ^[0-9]+$ && "$ledger_before" =~ ^[0-9]+$ ]] && (( ledger_after > ledger_before )) && fetched=1
  kept_deleted=0; (( kept_before )) && [[ ! -f "$kept_file" ]] && kept_deleted=1
  py "$DRV/finalize_stage.py" --id "$id" --app "$app" --tag "$tag" --exit "$rc" --planned "$planned" --label "sp1b-$id" --df-before "${before:-0}" --df-after "${after:-0}" --reason "$reason" --fetched "$fetched" \
     --kept-deleted "$kept_deleted" --kept-applies "$( [[ "$source" == kept ]] && echo 1 || echo 0 )" || true
  return "$rc"
}

# ----------------------------------------------------------------------------- arguments
MODE=""; ONLY=""; AGAIN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) MODE=list;;
    --all) MODE=all;;
    --only) MODE=only; ONLY="${2:-}"; shift;;
    --again) AGAIN=1;;
    --ledger-check) MODE=ledger;;
    --stage-inner) MODE=inner; ONLY="${2:-}"; shift;;
    -h|--help) awk 'NR > 1 && /^#/ { print; next } NR > 1 { exit }' "$SELF"; exit 0;;
    *) die "unknown argument: $1 (try --help)";;
  esac
  shift
done
mkdir -p "$EVID"
case "$MODE" in
  list)   need_tools; py "$DRV/stage_budget.py" list; exit $?;;
  ledger) py "$SP/check_ledger.py"; exit $?;;
  inner)  need_tools; stage_inner "$ONLY"; exit $?;;
  only)   need_tools; run_stage "$ONLY" "$AGAIN"; rc=$?; (( rc == 4 || rc == 2 )) && rc=1; exit "$rc";;   # 4 is internal (a rejected hash) and 2 is a harness problem: both are exit 1 for the caller
  all)
    need_tools
    start_avail="$(lj_df_avail_mb)"; kept_mb=0
    for f in "$KEEP"/*.tar.gz; do [[ -f "$f" ]] && kept_mb=$((kept_mb + $(mb_up "$(stat -c %s "$f")"))); done
    say "run_sp1b.sh --all: FilmCraft T3, then PhotoCraft, VectorCraft and LightCraft T1 and read-backs. Linux CLIs only: every result below is a Linux CLI result, not evidence for Windows."
    say "df at start: Avail ${start_avail} MB (the kept FilmCraft tarball on disk: ${kept_mb} MB)."
    n_fail=0; n_block=0; n_pass=0
    for app in $(jq -r '.stages|sort_by(.order)[].app' "$CFG"); do
      run_stage "$app" "$AGAIN"; rc=$?
      st="$(env_status "stage_$app-$(stage_field "$app" tag)")"
      say "RESULT $app $(stage_field "$app" tag): ${st:-none} (label: linux-cli; Linux CLI result; not evidence for Windows)"
      case "$rc" in 0) n_pass=$((n_pass + 1));; 3) n_block=$((n_block + 1));; *) n_fail=$((n_fail + 1));; esac
    done
    end_avail="$(lj_df_avail_mb)"
    left="$(ls -A "$VENDOR" 2>/dev/null | tr '\n' ' ')"; keepleft="$(ls -A "$KEEP" 2>/dev/null | tr '\n' ' ')"
    say "== after the run: ${n_pass} PASS, ${n_fail} FAIL or harness problem, ${n_block} BLOCKED. vendor/craft-sp1b holds: ${left:-nothing}; the hand-off folder holds: ${keepleft:-nothing (gone or empty)}."
    say "== df now: Avail ${end_avail} MB (start ${start_avail} MB; the kept tarball's ${kept_mb} MB is expected back; delta without it: $(( end_avail - start_avail - kept_mb )) MB; other writers move this figure)."
    lmsg="$(py "$SP/check_ledger.py" 2>&1)"; lrc=$?
    say "== ledger: $(head -1 <<<"$lmsg")"
    (( lrc != 0 )) && { say "== LEDGER PROBLEM: $lmsg"; n_fail=$((n_fail + 1)); }
    (( n_fail > 0 )) && exit 1
    (( n_block > 0 )) && exit 3
    exit 0;;
  *) die "give one of --list --all --only APP --ledger-check (try --help)";;
esac
