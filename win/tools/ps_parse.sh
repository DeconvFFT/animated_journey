#!/usr/bin/env bash
# ps_parse.sh [EXTRA_FILE ...]
#   Parses every PowerShell script and README fence of the Windows kit with the real PowerShell parser
#   (System.Management.Automation.Language.Parser::ParseFile on pwsh 7.5.4). Parsing runs nothing.
#   Targets (those that exist):
#     every *.ps1 under win/
#     every fenced powershell block (``` powershell, pwsh or ps1) in win/README*.md, win/kit2/*.md and
#       spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md, plus any EXTRA_FILE (.ps1 or .md) given on the command line.
#   pwsh is looked up in $PWSH, then <scratch>/pwsh/pwsh (see fetch_pwsh.sh), then PATH.
#   Note: pwsh 7 accepts syntax that Windows PowerShell 5.1 does not; ps_lint.py covers that gap.
# Prints one line per item and a total. Exit codes: 0 no parse errors, 1 a parse error, 3 pwsh not available
# (printed as "PENDING: pwsh not yet fetched": then ps_lint.py alone gates the work and this check is run later).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="${LJ_SCRATCH:-/home/user/build-scratch}"

PW=""
for c in "${PWSH:-}" "$SCRATCH/pwsh/pwsh" "$(command -v pwsh 2>/dev/null || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then PW="$c"; break; fi
done
if [ -z "$PW" ]; then
  echo "PENDING: pwsh not yet fetched (run win/tools/fetch_pwsh.sh); the parse check did not run"
  exit 3
fi

W="$(mktemp -d "$SCRATCH/ps_parse.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$W"' EXIT
MAN="$W/manifest.tsv"
: > "$MAN"

add_script() { printf '%s\t%s\n' "$1" "$2" >> "$MAN"; }
extract_fences() {
  # $1 = markdown file, $2 = label prefix
  awk -v dir="$W" -v label="$2" -v man="$MAN" '
    BEGIN { infence = 0; n = 0 }
    {
      if (!infence && match($0, /^[ \t]*```[ \t]*(powershell|pwsh|ps1)[ \t]*$/)) { infence = 1; n++; start = NR + 1; file = sprintf("%s/fence_%s_%d.ps1", dir, "f" NR, n); printf "" > file; next }
      if (infence && $0 ~ /^[ \t]*```[ \t]*$/) { infence = 0; close(file); printf "%s\t%s (fence starting at line %d)\n", file, label, start >> man; next }
      if (infence) { print $0 >> file }
    }' "$1"
}

count_scripts=0; count_fences=0
while IFS= read -r f; do
  add_script "$f" "${f#$ROOT/}"; count_scripts=$((count_scripts + 1))
done < <(find "$ROOT/win" -type f -name '*.ps1' 2>/dev/null | sort)

md_list=()
for m in "$ROOT"/win/README*.md "$ROOT"/win/kit2/*.md "$ROOT/spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md"; do
  [ -f "$m" ] && md_list+=("$m")
done
for x in "$@"; do
  case "$x" in
    *.md)  [ -f "$x" ] && md_list+=("$x") ;;
    *.ps1) [ -f "$x" ] && { add_script "$x" "$x"; count_scripts=$((count_scripts + 1)); } ;;
  esac
done
for m in "${md_list[@]}"; do
  before=$(wc -l < "$MAN")
  extract_fences "$m" "${m#$ROOT/}"
  after=$(wc -l < "$MAN")
  count_fences=$((count_fences + after - before))
done

cat > "$W/parse.ps1" <<'PS'
param([string]$Manifest)
$bad = 0
$n = 0
foreach ($line in [System.IO.File]::ReadAllLines($Manifest)) {
    if (-not $line) { continue }
    $parts = $line.Split("`t")
    $tokens = $null
    $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($parts[0], [ref]$tokens, [ref]$errors)
    if ($errors -and $errors.Count -gt 0) {
        foreach ($e in $errors) { Write-Output ("{0}: line {1}: parse error: {2}" -f $parts[1], $e.Extent.StartLineNumber, $e.Message) }
        $bad += $errors.Count
    } else {
        Write-Output ("OK   " + $parts[1])
    }
    $n++
}
Write-Output ("PARSED {0} item(s), {1} parse error(s)" -f $n, $bad)
if ($bad -gt 0) { exit 1 } else { exit 0 }
PS

echo "parser: $("$PW" -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')  scripts: $count_scripts  readme fences: $count_fences"
( cd / && "$PW" -NoProfile -File "$W/parse.ps1" -Manifest "$MAN" )
rc=$?
if [ "$rc" -eq 0 ]; then echo "ps_parse: 0 parse errors"; fi
exit "$rc"
