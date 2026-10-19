#!/usr/bin/env bash
# fetch_pwsh.sh DEST
#   Fetches PowerShell 7.5.4 (Linux x64 tarball) into DEST so the Windows kit can be parse-tested and
#   dry-run on Linux. Used only by tests. Nothing here touches the maker's PC.
#
# Run it inside the disk guard (planned peak 275 MB: 75 MB tarball + about 200 MB extracted tree):
#   source scripts/lj_guard.sh
#   lj_with_disk 275 wp01a-pwsh -- bash win/tools/fetch_pwsh.sh /home/user/build-scratch/pwsh
#
# What it does, in order (and prints each step):
#   1. refuses unless Avail minus 275 MB stays at or above 400 MB (the plan's disk rule, 4.9);
#   2. downloads the tarball into its OWN new empty folder next to DEST (untrusted data);
#   3. verifies SHA-256 against the release's hashes.sha256 asset (UTF-16 file, decoded here);
#      if that file cannot be reached it records the hash and says "recorded, NOT verified";
#   4. extracts with tar into a fresh folder, then moves it to DEST; deletes the tarball;
#   5. runs `pwsh -Version` from a neutral working folder (never from inside the downloaded tree).
# Idempotent: if DEST already holds a verified install of this version it only prints it and exits 0.
# Never touches: the repo, git, any file outside DEST and its temporary sibling folder.
# Exit codes: 0 ok, 2 bad usage, 3 environment (disk guard, download blocked, hash mismatch).
set -u
VER="7.5.4"
TARBALL="powershell-${VER}-linux-x64.tar.gz"
BASE="https://github.com/PowerShell/PowerShell/releases/download/v${VER}"
EXPECT_SIZE=75396784
PLANNED_MB=275
FLOOR_MB=400

die() { echo "fetch_pwsh: $2" >&2; exit "$1"; }

if [ $# -ne 1 ] || [ -z "${1:-}" ]; then die 2 "usage: fetch_pwsh.sh DEST  (a path that does not exist yet, or an earlier verified install)"; fi
DEST="${1%/}"
case "$DEST" in /*) ;; *) die 2 "DEST must be an absolute path (got a relative one)";; esac

# One df reader for the whole repo: the disk guard's, when it exists (scripts/lj_guard.sh, build plan 4.9).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [ -f "$ROOT/scripts/lj_guard.sh" ]; then . "$ROOT/scripts/lj_guard.sh"; fi
avail_mb() {
  if declare -F lj_df_avail_mb >/dev/null 2>&1; then lj_df_avail_mb; return; fi
  # fallback with the guard's convention: LJ_DF_CMD is a command line that prints df -P style output, or just a number of MB
  local out
  if [ -n "${LJ_DF_CMD:-}" ]; then out="$(LC_ALL=C $LJ_DF_CMD 2>/dev/null)"; else out="$(LC_ALL=C df -BM -P / 2>/dev/null)"; fi
  if printf '%s' "$out" | grep -Eq '^[[:space:]]*[0-9]+[[:space:]]*$'; then printf '%s\n' "$out" | tr -d ' \n'; echo; return; fi
  printf '%s\n' "$out" | awk 'NR==1{next} NF>=4{v=$4; gsub(/[^0-9]/,"",v); if(v!=""){print v; exit}}'
}
show_df() { echo "df ($1): Avail $(avail_mb) MB"; }

MARK="$DEST/.lj-verified"
if [ -x "$DEST/pwsh" ] && [ -f "$MARK" ] && grep -q "^version=${VER}\$" "$MARK"; then
  echo "[1/1] already installed and verified in the scratch folder: nothing to do"
  cat "$MARK"
  ( cd / && "$DEST/pwsh" -NoProfile -Version )
  show_df "unchanged"
  exit 0
fi
if [ -e "$DEST" ]; then die 2 "DEST exists but holds no verified install of ${VER}; refusing to write into it (choose a new path)"; fi

PARENT="$(dirname "$DEST")"
mkdir -p "$PARENT" || die 3 "cannot create $PARENT"

echo "[1/6] Disk rule: Avail minus ${PLANNED_MB} MB must stay at or above ${FLOOR_MB} MB"
show_df "before"
A="$(avail_mb)"
if [ -z "$A" ] || [ $((A - PLANNED_MB)) -lt "$FLOOR_MB" ]; then
  die 3 "DISK: Avail ${A:-unknown} MB minus ${PLANNED_MB} MB is below ${FLOOR_MB} MB; nothing was downloaded"
fi
START_AVAIL="$A"

DL="$(mktemp -d "$PARENT/pwsh-dl.XXXXXX")" || die 3 "cannot create a download folder"
XT="$(mktemp -d "$PARENT/pwsh-x.XXXXXX")" || die 3 "cannot create an extraction folder"
cleanup() { rm -rf "$DL" "$XT" 2>/dev/null; }
trap cleanup EXIT

echo "[2/6] Downloading ${TARBALL} (expected ${EXPECT_SIZE} bytes) into a new empty folder"
curl -fsSL --retry 2 --max-time 900 -o "$DL/$TARBALL" "${BASE}/${TARBALL}" || die 3 "DOWNLOAD BLOCKED or failed: ${BASE}/${TARBALL}"
GOT_SIZE="$(stat -c %s "$DL/$TARBALL")"
echo "      size ${GOT_SIZE} bytes"
[ "$GOT_SIZE" = "$EXPECT_SIZE" ] || die 3 "size ${GOT_SIZE} differs from the expected ${EXPECT_SIZE}; stopping before extraction"

echo "[3/6] SHA-256"
GOT_SHA="$(sha256sum "$DL/$TARBALL" | awk '{print $1}')"
echo "      computed: ${GOT_SHA}"
VERIFIED="no (recorded only: hashes.sha256 was not reachable)"
if curl -fsSL --retry 2 --max-time 60 -o "$DL/hashes.raw" "${BASE}/hashes.sha256" 2>/dev/null; then
  # the release file is UTF-16 with a byte-order mark: decode before reading it
  if head -c2 "$DL/hashes.raw" | od -An -tx1 | grep -qi "ff fe"; then
    iconv -f UTF-16 -t UTF-8 "$DL/hashes.raw" > "$DL/hashes.txt" 2>/dev/null || tr -d '\000' < "$DL/hashes.raw" > "$DL/hashes.txt"
  else
    cp "$DL/hashes.raw" "$DL/hashes.txt"
  fi
  WANT="$(tr -d '\r' < "$DL/hashes.txt" | awk -v f="$TARBALL" '{ n=$2; sub(/^\*/,"",n); if (n==f) print $1 }' | head -1)"
  if [ -z "$WANT" ]; then
    echo "      hashes.sha256 reached but has no line for ${TARBALL}: recorded only"
  elif [ "$(echo "$WANT" | tr 'A-F' 'a-f')" = "$GOT_SHA" ]; then
    echo "      published:  ${WANT}"
    echo "      MATCH"
    VERIFIED="yes (matches the release's hashes.sha256)"
  else
    die 3 "SHA-256 MISMATCH: published ${WANT}, computed ${GOT_SHA}; nothing extracted"
  fi
else
  echo "      hashes.sha256 not reachable: hash recorded, NOT verified"
fi

echo "[4/6] Extracting into a fresh folder (tar only; nothing from the archive is run)"
tar -xzf "$DL/$TARBALL" -C "$XT" || die 3 "tar failed"
rm -f "$DL/$TARBALL"
[ -f "$XT/pwsh" ] || die 3 "the archive has no pwsh file at its top level"
chmod +x "$XT/pwsh"
{ echo "version=${VER}"; echo "tarball=${TARBALL}"; echo "sha256=${GOT_SHA}"; echo "verified=${VERIFIED}"; } > "$XT/.lj-verified"
mv "$XT" "$DEST" || die 3 "cannot move the extracted tree to DEST"
XT=""

echo "[5/6] Smoke test from a neutral working folder"
( cd / && DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1 "$DEST/pwsh" -NoProfile -Version ) || die 3 "pwsh did not start"

echo "[6/6] Done"
show_df "after"
echo "disk used by this step: about $((START_AVAIL - $(avail_mb))) MB (tarball already deleted)"
cat "$DEST/.lj-verified"
exit 0
