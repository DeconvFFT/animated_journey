#!/usr/bin/env bash
# test_cleanup.sh: tests of scripts/cleanup_scratch.sh on FAKE trees (build plan WP-11a). Prints GROUP and RESULT lines.
#   bash tests/runner/test_cleanup.sh quick|all
# Every deletion test runs on a fake scratch folder and a fake repo root under the real scratch folder's own temp
# area (removed on exit), with HOME pointed at a fake home. In "all" mode it also dry-runs the script on the REAL
# tree and proves by hash that nothing changed there. The script is never run with --yes on the real tree.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO" || exit 3
MODE="${1:-quick}"
CLEAN="$REPO/scripts/cleanup_scratch.sh"
BASE="$(cd "$REPO/.." && pwd)/build-scratch"
mkdir -p "$BASE"
T="$(mktemp -d "$BASE/wp11a-clean.XXXXXX")" || exit 3
trap 'rm -rf "$T"' EXIT

res() { echo "RESULT $1 $2 :: ${3:-}"; }
chk() { if [[ "$3" -eq 0 ]]; then res PASS "$1" "$2"; else res FAIL "$1" "$2"; fi; }   # chk NAME DETAIL EXITCODE
dirhash() { [[ -e "$1" ]] || { echo absent; return; }; (cd "$1" && { find . -type f -exec sha256sum {} + 2>/dev/null | sort; find . -printf '%p %y %l\n' | sort; }) | sha256sum | cut -c1-16; }
# mk_tree DIR: a fake home, a fake scratch folder, a fake repo with vendor/ and renders/
mk_tree() {
  local d="$1"
  mkdir -p "$d/home" "$d/build-scratch/pwsh/bin" "$d/build-scratch/venv-otio/lib" "$d/build-scratch/venv2" "$d/build-scratch/myenv" \
           "$d/build-scratch/keep-dir" "$d/build-scratch/downloads" "$d/repo/vendor/craft/_keep" "$d/repo/vendor/craft-sp1b" \
           "$d/repo/vendor/fonts" "$d/repo/vendor/js" "$d/repo/renders/wp04" "$d/repo/renders/wp01a" "$d/repo/renders/final" "$d/repo/media" "$d/other"
  echo x > "$d/home/keep.txt"; echo x > "$d/build-scratch/pwsh/bin/pwsh"; echo x > "$d/build-scratch/venv-otio/lib/a"
  echo cfg > "$d/build-scratch/venv2/pyvenv.cfg"; echo cfg > "$d/build-scratch/myenv/pyvenv.cfg"; echo x > "$d/build-scratch/keep-dir/f"
  echo x > "$d/build-scratch/downloads/f"; echo x > "$d/build-scratch/pwsh-notes.txt"; echo holder > "$d/build-scratch/disk.lock"
  echo '{}' > "$d/build-scratch/disk-ledger.jsonl"; echo x > "$d/repo/vendor/craft/_keep/t.tgz"; echo x > "$d/repo/vendor/craft-sp1b/b"
  echo x > "$d/repo/vendor/craft-x.tgz"; echo x > "$d/repo/vendor/fonts/c"; echo x > "$d/repo/vendor/js/d"; echo x > "$d/repo/renders/wp04/f"
  echo x > "$d/repo/renders/wp01a/f"; echo x > "$d/repo/renders/final/f"; echo x > "$d/repo/renders/notes.txt"; echo x > "$d/repo/media/photo.txt"
  echo x > "$d/other/f"
  # a 1 MB file (only when asked) so that the size column is not all zeros; the disk is nearly full, so trees stay tiny
  if [[ "${2:-}" == big ]]; then head -c 1048576 /dev/zero > "$d/build-scratch/pwsh/bin/big.bin" 2>/dev/null || true; fi
}
# cc DIR [ENV=VAL ...] -- ARGS...   runs the script with the fake home; output -> $T/co, exit -> RC
cc() {
  local d="$1"; shift
  local envs=()
  while [[ $# -gt 0 && "$1" != "--" ]]; do envs+=("$1"); shift; done
  shift
  RC=0
  env HOME="$d/home" "${envs[@]}" bash "$CLEAN" "$@" > "$T/co" 2>&1 || RC=$?
}
has() { grep -Eq -- "$1" "$2"; }

echo "GROUP dry_run"
D="$T/t1"; mk_tree "$D" big
h0="$(dirhash "$D")"; cc "$D" -- --scratch "$D/build-scratch" --root "$D/repo"; h1="$(dirhash "$D")"
[[ "$RC" -eq 0 && "$h0" == "$h1" ]]; chk default_is_a_dry_run_and_deletes_nothing "exit $RC; tree hash $h0 -> $h1" $?
has 'DRY RUN' "$T/co" && has 'would delete .*<scratch>/pwsh' "$T/co" && has 'would delete .*vendor/craft-sp1b' "$T/co" && has 'would delete .*renders/wp04' "$T/co"; chk dry_run_lists_the_items "pwsh, vendor/craft-sp1b, renders/wp04 listed" $?
has 'would delete +1\.[0-9] MB +<scratch>/pwsh' "$T/co"; chk dry_run_prints_sizes "pwsh shows its 1 MB file" $?
n="$(grep -c '^would delete' "$T/co")"
[[ "$n" -eq 9 ]]; chk dry_run_lists_exactly_the_listed_items "9 items: pwsh, 3 venvs, 3 craft*, 2 wp* (counted $n)" $?
! has 'would delete .*(fonts|js|keep-dir|downloads|final|photo|disk)' "$T/co"; chk dry_run_never_lists_kept_items "no fonts, js, keep-dir, downloads, final, media, lock in the list" $?
has 'df before: Avail [0-9]+ MB' "$T/co"; chk dry_run_prints_df "df line printed" $?
! grep -q -e "$T" -e '/home/' -e '/root' "$T/co"; chk output_has_no_absolute_paths "only <scratch>/..., vendor/..., renders/..." $?
h0="$(dirhash "$D")"; cc "$D" -- --dry-run --scratch "$D/build-scratch" --root "$D/repo"; h1="$(dirhash "$D")"
[[ "$RC" -eq 0 && "$h0" == "$h1" ]]; chk explicit_dry_run_deletes_nothing "exit $RC" $?
cc "$D" LJ_SCRATCH="$D/build-scratch" -- --root "$D/repo"
[[ "$RC" -eq 0 ]] && has 'would delete .*<scratch>/pwsh' "$T/co"; chk scratch_from_LJ_SCRATCH "exit $RC" $?
rm -rf "$D"

echo "GROUP yes_deletes_only_the_list"
D="$T/t2"; mk_tree "$D"; kept_before="$(cd "$D" && find home other build-scratch/keep-dir build-scratch/downloads build-scratch/pwsh-notes.txt build-scratch/disk.lock build-scratch/disk-ledger.jsonl repo/vendor/fonts repo/vendor/js repo/renders/final repo/renders/notes.txt repo/media -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-16)"
cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 0 ]]; chk yes_exit_0 "exit $RC" $?
gone=0; for x in build-scratch/pwsh build-scratch/venv-otio build-scratch/venv2 build-scratch/myenv repo/vendor/craft repo/vendor/craft-sp1b repo/vendor/craft-x.tgz repo/renders/wp04 repo/renders/wp01a; do [[ -e "$D/$x" ]] || gone=$((gone + 1)); done
[[ "$gone" -eq 9 ]]; chk yes_removes_every_listed_item "$gone of 9 gone" $?
kept_after="$(cd "$D" && find home other build-scratch/keep-dir build-scratch/downloads build-scratch/pwsh-notes.txt build-scratch/disk.lock build-scratch/disk-ledger.jsonl repo/vendor/fonts repo/vendor/js repo/renders/final repo/renders/notes.txt repo/media -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-16)"
[[ "$kept_before" == "$kept_after" && -d "$D/repo/vendor" && -d "$D/repo/renders" && -d "$D/build-scratch" ]]; chk yes_keeps_everything_else_byte_for_byte "kept files hash $kept_before -> $kept_after; folders themselves kept" $?
has 'df before: Avail' "$T/co" && has 'df after: +Avail' "$T/co" && has '^free space: [0-9]+ MB before, [0-9]+ MB after' "$T/co"; chk yes_prints_df_before_and_after "df before, df after, free space line" $?
has '^deleted +[0-9.]+ MB +<scratch>/pwsh' "$T/co"; chk yes_reports_each_deletion_with_size "deleted ... <scratch>/pwsh" $?
! grep -q -e "$T" -e '/home/' -e '/root' "$T/co"; chk yes_output_has_no_absolute_paths "clean" $?
cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 0 ]] && has 'nothing on the list exists' "$T/co"; chk yes_twice_is_harmless "second run: exit $RC, nothing to delete" $?
rm -rf "$D"

echo "GROUP refusals"
D="$T/t3"; mk_tree "$D"; h0="$(dirhash "$D")"
refuses() {  # name detail -- args...   (exit must be 2, REFUSED printed, tree unchanged)
  local name="$1" detail="$2"; shift 3
  cc "$D" -- "$@"
  local reason; reason="$(grep -m1 '^REFUSED' "$T/co" | cut -c1-90)"
  [[ "$RC" -eq 2 ]] && has '^REFUSED: ' "$T/co" && [[ "$(dirhash "$D")" == "$h0" ]]; local ok=$?
  chk "$name" "$detail (exit $RC: $reason)" "$ok"
}
refuses refuses_root "--scratch /" -- --yes --scratch / --root "$D/repo"
refuses refuses_home "--scratch is the fake HOME" -- --yes --scratch "$D/home" --root "$D/repo"
refuses refuses_parent_of_home_and_repo "--scratch is the folder that holds home and repo" -- --yes --scratch "$D" --root "$D/repo"
refuses refuses_parent_of_the_real_repo "--scratch is the real repo's parent folder" -- --yes --scratch "$(dirname "$REPO")" --root "$D/repo"
refuses refuses_a_folder_not_named_scratch "--scratch is a folder without 'scratch' in its name" -- --yes --scratch "$D/other" --root "$D/repo"
refuses refuses_scratch_inside_the_repo "--scratch inside the repo" -- --yes --scratch "$D/repo/vendor/build-scratch" --root "$D/repo"
refuses refuses_a_shallow_path "--scratch /scratch (one level deep)" -- --yes --scratch /scratch --root "$D/repo"
refuses refuses_empty_scratch "--scratch ''" -- --yes --scratch "" --root "$D/repo"
refuses refuses_missing_root "--root that does not exist" -- --yes --scratch "$D/build-scratch" --root "$D/no-such-root"
ln -s "$D/home" "$D/link-scratch"; h0="$(dirhash "$D")"
refuses refuses_a_scratch_link_that_points_home "link-scratch -> HOME" -- --yes --scratch "$D/link-scratch" --root "$D/repo"
cc "$D" LJ_SCRATCH=/ -- --yes --root "$D/repo"
[[ "$RC" -eq 2 ]] && has '^REFUSED' "$T/co"; chk refuses_root_from_LJ_SCRATCH "exit $RC" $?
cc "$D" LJ_SCRATCH="$D/home" -- --yes --root "$D/repo"
[[ "$RC" -eq 2 ]] && has '^REFUSED' "$T/co"; chk refuses_home_from_LJ_SCRATCH "exit $RC" $?
cc "$D" -- --yes --dry-run --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 2 ]]; chk yes_with_dry_run_is_a_usage_error "exit $RC" $?
cc "$D" -- --frobnicate; [[ "$RC" -eq 2 ]]; chk unknown_option_exit_2 "exit $RC" $?
cc "$D" -- --scratch; [[ "$RC" -eq 2 ]]; chk option_without_value_exit_2 "exit $RC" $?
[[ "$(dirhash "$D")" == "$h0" ]]; chk refusals_changed_nothing "tree hash unchanged after all refusals" $?
rm -rf "$D"

echo "GROUP links_lock_and_odd_trees"
D="$T/t4"; mk_tree "$D"; mkdir -p "$D/outside/inner" "$D/outside-vendor/craft-out"; echo precious > "$D/outside/inner/f"; echo precious > "$D/outside-vendor/craft-out/f"
rm -rf "$D/build-scratch/pwsh" "$D/build-scratch/venv-otio"; ln -s "$D/outside" "$D/build-scratch/pwsh"; ln -s "$D/outside" "$D/build-scratch/venv-link"
oh="$(dirhash "$D/outside")"
cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 0 && "$(dirhash "$D/outside")" == "$oh" && -L "$D/build-scratch/pwsh" ]] && has 'skipped \(is a link' "$T/co"; chk listed_links_are_skipped_never_followed "outside folder intact, link left in place (exit $RC)" $?
rm -rf "$D"
D="$T/t5"; mk_tree "$D"; mkdir -p "$D/outside-vendor/craft-out"; echo precious > "$D/outside-vendor/craft-out/f"; rm -rf "$D/repo/vendor"; ln -s "$D/outside-vendor" "$D/repo/vendor"
oh="$(dirhash "$D/outside-vendor")"; cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 0 && "$(dirhash "$D/outside-vendor")" == "$oh" ]] && has 'vendor/ is a link' "$T/co" && [[ ! -e "$D/repo/renders/wp04" ]]; chk vendor_that_is_a_link_is_skipped_whole "outside intact; renders still cleaned (exit $RC)" $?
rm -rf "$D"
D="$T/t6"; mk_tree "$D"; h0="$(dirhash "$D")"
( flock -x 9; sleep 4 ) 9>>"$D/build-scratch/disk.lock" &
holder=$!; sleep 0.5
cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 3 && "$(dirhash "$D")" == "$h0" ]] && has '^BUSY' "$T/co"; chk yes_waits_for_nobody_when_the_disk_lock_is_busy "exit $RC, BUSY printed, nothing deleted" $?
cc "$D" -- --scratch "$D/build-scratch" --root "$D/repo"
[[ "$RC" -eq 0 ]]; chk dry_run_ignores_the_lock "exit $RC" $?
kill "$holder" 2>/dev/null; wait "$holder" 2>/dev/null
rm -rf "$D"
D="$T/t7"; mk_tree "$D"
cc "$D" -- --scratch "$D/nothing-scratch" --root "$D/repo"
[[ "$RC" -eq 0 ]] && has 'would delete .*vendor/craft' "$T/co" && ! has 'would delete .*<scratch>' "$T/co"; chk scratch_folder_that_does_not_exist_is_fine "exit $RC; only vendor/ and renders/ listed" $?
rm -rf "$D"
D="$T/t8"; mk_tree "$D"; chmod -R a-w "$D/build-scratch/pwsh"
cc "$D" -- --yes --scratch "$D/build-scratch" --root "$D/repo"
chmod -R u+w "$D/build-scratch" 2>/dev/null
[[ "$RC" -eq 0 && ! -e "$D/build-scratch/pwsh" ]]; ok=$?
chk read_only_tree_is_still_deleted "exit $RC; a folder with no write permission is removed" "$ok"
rm -rf "$D"

echo "GROUP static"
bash -n "$CLEAN"; chk cleanup_syntax_bash_n "bash -n scripts/cleanup_scratch.sh" $?
if [[ "$MODE" == "all" ]]; then
  echo "GROUP real_tree_dry_run"
  snap() { { [[ -d "$BASE" ]] && find "$BASE" -maxdepth 3 -not -path "$T" -not -path "$T/*" -not -path "$BASE/.wk2run*" -not -path "$BASE/wp11a-*" -not -path "$BASE/.ljg*" -not -name '*.lock' -not -name '*.jsonl' -printf '%p %s %T@\n'; find "$REPO/vendor" "$REPO/renders" -printf '%p %s %T@\n' 2>/dev/null; } | sort | sha256sum | cut -c1-16; }
  h0="$(snap)"; env -u LJ_SCRATCH bash "$CLEAN" > "$T/real.out" 2>&1; rc=$?; h1="$(snap)"
  [[ "$rc" -eq 0 && "$h0" == "$h1" ]]; chk real_tree_dry_run_changes_nothing "exit $rc; names, sizes and times of scratch (3 levels), vendor/, renders/: $h0 -> $h1" $?
  has 'DRY RUN' "$T/real.out" && has 'Dry run: nothing was deleted' "$T/real.out" && ! grep -q -e "$REPO" -e '/home/' -e '/root' "$T/real.out"; chk real_tree_dry_run_output_is_clean "no absolute path; says nothing was deleted" $?
fi
