#!/usr/bin/env bash
# cleanup_scratch.sh: remove the regenerable build leftovers from the scratch folder, vendor/ and renders/ (build plan
# WP-11a; refs W-06, W-26, D-26, D-30; sizes in 4.9). DRY RUN BY DEFAULT.
#
#   bash scripts/cleanup_scratch.sh                  dry run: lists what it WOULD delete, with sizes, and deletes nothing
#   bash scripts/cleanup_scratch.sh --dry-run        the same, spelled out
#   bash scripts/cleanup_scratch.sh --yes            deletes the listed items, prints the free disk space before and after
#   options: --scratch DIR   scratch folder (default: LJ_SCRATCH, else build-scratch beside the repo folder)
#            --root DIR      repo root that holds vendor/ and renders/ (default: the repo this script is in)
#
# WHAT IS ON THE LIST (and only this; anything else is kept, always)
#   <scratch>/pwsh                 the PowerShell used for parse tests (WP-01a)
#   <scratch>/venv*                Python virtual environments, e.g. venv-otio (WP-06); also any folder in <scratch>
#                                  that has a pyvenv.cfg at its top
#   vendor/craft*                  Craft app downloads and extracted trees, e.g. vendor/craft, vendor/craft-sp1b (WP-07, WP-10)
#   renders/wp*                    per-package render output, e.g. renders/wp04 (WP-04)
# NOT on the list, so never touched: vendor/fonts, vendor/js (the fetched libraries), the lock files and ledgers in
# <scratch>, media/, exports/, and every tracked file.
#
# SAFETY (it prints REFUSED and exits 2 before touching anything)
#   - the scratch folder must exist as a real folder whose own name contains "scratch", must be outside the repo,
#     must be at least two levels deep, and must not be "/", $HOME, or a parent of $HOME or of the repo; a scratch
#     that is a link is judged by where it really points
#   - every item is resolved with realpath and must sit strictly inside <scratch>, vendor/ or renders/ (checked
#     against the real paths); a link on the list is skipped, never followed; vendor/ or renders/ that is a link
#     elsewhere is skipped whole
#   - --yes takes the disk lock (<scratch>/disk.lock, the one lj_guard.sh uses) without waiting: if a guarded job is
#     running it prints BUSY and exits 3 so a download or render is never pulled out from under it
# Paths are printed as <scratch>/..., vendor/... and renders/... only. No absolute path, user or host name appears.
# EXIT 0 done (also when there was nothing to delete) | 2 bad usage or REFUSED | 3 environment (lock busy, df
# unreadable, a deletion failed). Requires bash 4+, realpath, du, df, flock. UNVERIFIED on Windows (Linux script).
set -u

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SELF_DIR/.." && pwd)"
SCRATCH="${LJ_SCRATCH:-$(cd "$ROOT/.." && pwd)/build-scratch}"
MODE="dry"
SEEN_DRY=0; SEEN_YES=0

usage() {
  cat <<'EOF'
usage: bash scripts/cleanup_scratch.sh [--dry-run | --yes] [--scratch DIR] [--root DIR]
  (no option)  dry run: list what would be deleted and the sizes; delete nothing
  --yes        delete <scratch>/pwsh, <scratch>/venv*, vendor/craft*, renders/wp*; print free disk before and after
EOF
}
refuse() { printf 'REFUSED: %s\nNothing was deleted.\n' "$1"; exit 2; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) SEEN_DRY=1 ;;
    --yes) SEEN_YES=1 ;;
    --scratch) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; SCRATCH="$2"; shift ;;
    --root) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; ROOT="$2"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
  shift
done
if (( SEEN_DRY && SEEN_YES )); then usage >&2; echo "--dry-run and --yes contradict each other" >&2; exit 2; fi
(( SEEN_YES )) && MODE="yes"

command -v realpath >/dev/null 2>&1 || { echo "realpath is not installed; nothing was done" >&2; exit 3; }

# --------------------------------------------------------------------------- vet the scratch folder and the repo root
[[ -n "$SCRATCH" ]] || refuse "the scratch folder is empty"
[[ -n "$ROOT" ]] || refuse "the repo root is empty"
S_ABS="$(realpath -m -- "$SCRATCH")"
S_REAL="$(realpath -e -- "$SCRATCH" 2>/dev/null || true)"
R_REAL="$(realpath -e -- "$ROOT" 2>/dev/null || true)"
[[ -n "$R_REAL" && -d "$R_REAL" ]] || refuse "the repo root does not exist"
H_REAL="$(realpath -m -- "${HOME:-/nonexistent-home}")"

is_under() { [[ "$1" == "$2" || "$1" == "$2"/* ]]; }   # $1 equals or is below $2
depth_of() { local p="${1#/}" a; [[ -z "$p" ]] && { echo 0; return; }; IFS=/ read -ra a <<<"$p"; echo "${#a[@]}"; }

vet_scratch() {  # $1 = a resolved path to judge
  local s="$1" base
  [[ "$s" != "/" ]] || refuse "the scratch folder is '/'"
  [[ "$s" != "$H_REAL" ]] || refuse "the scratch folder is your home folder"
  is_under "$H_REAL" "$s" && refuse "the scratch folder contains your home folder"
  is_under "$R_REAL" "$s" && refuse "the scratch folder is, or contains, the repo folder"
  is_under "$s" "$R_REAL" && refuse "the scratch folder must be outside the repo folder"
  (( $(depth_of "$s") >= 2 )) || refuse "the scratch folder is too close to the top of the disk (at least two levels deep)"
  base="${s##*/}"
  [[ "${base,,}" == *scratch* ]] || refuse "the scratch folder's own name must contain 'scratch' (it is a safety check; use --scratch with such a folder)"
}
vet_scratch "$S_ABS"
if [[ -z "$S_REAL" || ! -d "$S_REAL" ]]; then
  S_REAL=""   # no scratch folder yet: nothing to list there
else
  vet_scratch "$S_REAL"
fi

# --------------------------------------------------------------------------- build the list
shopt -s nullglob
ITEMS=(); LABELS=(); KEPT_NOTE=()
add_item() {  # path container_real label_prefix_for_display
  local p="$1" cont="$2" shown="$3" real
  if [[ -L "$p" ]]; then KEPT_NOTE+=("skipped (is a link, never followed): $shown"); return; fi
  [[ -e "$p" ]] || return
  real="$(realpath -e -- "$p" 2>/dev/null || true)"
  if [[ -z "$real" || "$real" == "$cont" || "$real" != "$cont"/* ]]; then KEPT_NOTE+=("skipped (not strictly inside its folder): $shown"); return; fi
  ITEMS+=("$real"); LABELS+=("$shown")
}
if [[ -n "$S_REAL" ]]; then
  add_item "$S_REAL/pwsh" "$S_REAL" "<scratch>/pwsh"
  for d in "$S_REAL"/*/ ; do
    d="${d%/}"; n="${d##*/}"
    if [[ "$n" == venv* || -f "$d/pyvenv.cfg" ]]; then add_item "$d" "$S_REAL" "<scratch>/$n"; fi
  done
fi
for sub in vendor renders; do
  [[ -e "$R_REAL/$sub" ]] || continue
  if [[ -L "$R_REAL/$sub" ]]; then KEPT_NOTE+=("skipped ($sub/ is a link, never followed)"); continue; fi
  C_REAL="$(realpath -e -- "$R_REAL/$sub" 2>/dev/null || true)"
  [[ "$C_REAL" == "$R_REAL/$sub" ]] || { KEPT_NOTE+=("skipped ($sub/ does not resolve inside the repo)"); continue; }
  if [[ "$sub" == vendor ]]; then pat="craft*"; else pat="wp*"; fi
  for p in "$C_REAL"/$pat; do add_item "$p" "$C_REAL" "$sub/${p##*/}"; done
done
# de-duplicate (a venv folder named pwsh would otherwise be listed twice)
declare -A SEEN=(); U_ITEMS=(); U_LABELS=()
for ((i = 0; i < ${#ITEMS[@]}; i++)); do
  [[ -n "${SEEN[${ITEMS[i]}]:-}" ]] && continue
  SEEN["${ITEMS[i]}"]=1; U_ITEMS+=("${ITEMS[i]}"); U_LABELS+=("${LABELS[i]}")
done

# --------------------------------------------------------------------------- report
df_line() {
  LC_ALL=C df -BM -P / 2>/dev/null | awk 'NR==2{a=$4; s=$2; u=$5; gsub(/[^0-9]/,"",a); gsub(/[^0-9]/,"",s); if(a!="") printf "Avail %s MB of %s MB (%s used)\n", a, s, u}'
}
df_avail() { LC_ALL=C df -BM -P / 2>/dev/null | awk 'NR==2{a=$4; gsub(/[^0-9]/,"",a); print a}'; }
mb_of_kb() { awk -v k="$1" 'BEGIN{printf "%.1f", k/1024}'; }

if [[ "$MODE" == "dry" ]]; then echo "cleanup_scratch: DRY RUN (nothing will be deleted; add --yes to delete)"; else echo "cleanup_scratch: DELETING the items below (--yes)"; fi
echo "scope: <scratch>/pwsh, <scratch>/venv*, vendor/craft*, renders/wp*; everything else is kept"
BEFORE="$(df_avail)"
echo "df before: $(df_line)"
TOTAL_KB=0
SIZES=()
for ((i = 0; i < ${#U_ITEMS[@]}; i++)); do
  kb="$(du -sk -- "${U_ITEMS[i]}" 2>/dev/null | awk '{print $1}')"; [[ "$kb" =~ ^[0-9]+$ ]] || kb=0
  SIZES+=("$kb"); TOTAL_KB=$((TOTAL_KB + kb))
done
if (( ${#U_ITEMS[@]} == 0 )); then
  echo "nothing on the list exists: there is nothing to delete"
fi
if [[ "$MODE" == "dry" ]]; then
  for ((i = 0; i < ${#U_ITEMS[@]}; i++)); do printf 'would delete  %9s MB  %s\n' "$(mb_of_kb "${SIZES[i]}")" "${U_LABELS[i]}"; done
  for n in "${KEPT_NOTE[@]}"; do echo "$n"; done
  printf 'total that --yes would free: %s MB in %d item(s). Dry run: nothing was deleted.\n' "$(mb_of_kb "$TOTAL_KB")" "${#U_ITEMS[@]}"
  exit 0
fi

# --------------------------------------------------------------------------- --yes: take the disk lock without waiting, then delete
LOCKFD=""
if [[ -n "$S_REAL" ]]; then
  if { exec {LOCKFD}<>"$S_REAL/disk.lock"; } 2>/dev/null; then   # (a bare "exec ... 2>/dev/null" would silence stderr for the rest of the run)
    if ! flock -n "$LOCKFD"; then
      holder="$(head -n 1 "$S_REAL/disk.lock" 2>/dev/null | tr -d '\r' | cut -c1-60)"
      echo "BUSY: the disk lock is held by ${holder:-an unknown job}; nothing was deleted. Try again when that stage has finished."
      exit 3
    fi
  fi
fi
FAILED=0; DONE_KB=0
for ((i = 0; i < ${#U_ITEMS[@]}; i++)); do
  p="${U_ITEMS[i]}"
  # re-check right before the delete: still a real path, still not a link
  if [[ -L "$p" ]]; then echo "skipped (became a link): ${U_LABELS[i]}"; continue; fi
  chmod -R u+rwX -- "$p" 2>/dev/null
  if rm -rf --one-file-system -- "$p" 2>/dev/null && [[ ! -e "$p" ]]; then
    printf 'deleted       %9s MB  %s\n' "$(mb_of_kb "${SIZES[i]}")" "${U_LABELS[i]}"; DONE_KB=$((DONE_KB + SIZES[i]))
  else
    printf 'FAILED to delete          %s\n' "${U_LABELS[i]}"; FAILED=$((FAILED + 1))
  fi
done
for n in "${KEPT_NOTE[@]}"; do echo "$n"; done
AFTER="$(df_avail)"
echo "df after:  $(df_line)"
if [[ "$BEFORE" =~ ^[0-9]+$ && "$AFTER" =~ ^[0-9]+$ ]]; then
  printf 'free space: %s MB before, %s MB after (this script freed about %s MB; other jobs may be writing at the same time)\n' "$BEFORE" "$AFTER" "$(mb_of_kb "$DONE_KB")"
else
  echo "free space: could not be read from df"
fi
(( FAILED > 0 )) && { echo "$FAILED item(s) could not be deleted"; exit 3; }
exit 0
