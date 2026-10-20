<#
.SYNOPSIS
  Life Journey archive check (Exercise 1 of playbooks\ai-imagery.md, WP-09 kit B). READ-ONLY: it changes nothing.

.DESCRIPTION
  Checks an archive made by archive_init.ps1 (or by hand in the same shape):
    * the four folders of Step 0 exist,
    * manifest.csv and steps.csv exist and start with the header lines the playbook defines,
    * every file listed in checksums.txt still has the SHA-256 recorded for it (the project's own
      research\sources\format-round1\verify_manifest.ps1 does this, called where it sits in the project folder),
    * files in 01_masters that checksums.txt does not list are reported (information: a new scan needs its checksum added).
  A changed file is reported as MISMATCH with its file name, a deleted one as MISSING. The last lines say how many files were
  checked and how many problems there were. It writes nothing, not even a log. It does not touch the network or your settings.

.PARAMETER Root
  The archive folder. Default C:\lj\standin.

.NOTES
  Exit codes: 0 no problems; 1 at least one problem (a mismatch, a missing file or folder, a wrong header);
  2 the folder is not an archive or the options were wrong; 3 a project file is missing. Windows PowerShell 5.1 and PowerShell 7.
  Run for one session only, without changing system policy:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\archive_verify.ps1 -Root C:\lj\standin
  Every claim about Windows behaviour in this script is UNVERIFIED until the maker's first real run.
#>
[CmdletBinding()]
param(
    [string]$Root = 'C:\lj\standin'
)

$ErrorActionPreference = 'Stop'
$ScriptVersion = '1.0.0'

# Anything unexpected that would otherwise print a red error (which can carry a folder name): say it in scrubbed words and stop.
trap {
    Write-Host ''
    Write-Host ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    Write-Host 'files written: none'
    exit 3
}
$TotalSteps = 5

# The same names and columns as archive_init.ps1 (Step 0 of playbooks\ai-imagery.md; tests/win_kit2 compares both with the playbook).
$FolderNames = @('01_masters', '02_work', '03_exports', '04_reconstructions')
$ManifestColumns = @('id', 'box', 'medium', 'scan_date', 'device', 'ppi', 'bit_depth', 'profile', 'date_est', 'date_confidence', 'people', 'place', 'caption_source', 'interview_date', 'consent_note', 'sha256', 'notes')
$StepsColumns = @('derivative_id', 'parent_id', 'step_no', 'tool', 'version', 'settings', 'seed', 'invents', 'label_level', 'reviewer', 'approved', 'deity_form', 'deity_source')
$script:StepNo = 0
$script:Problems = 0

function Say([string]$text) { Write-Host $text }

$script:ProjectRoot = ''
try { $script:ProjectRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent (Split-Path -Parent $PSScriptRoot))).TrimEnd([char]92, [char]47) } catch { $script:ProjectRoot = '' }

# Shared helpers: identical copies, so change all copies together (tests/win_kit2/run_tests.sh checks they match). Show-Path, Clean-Message: archive_init.ps1, archive_verify.ps1, kenburns_24.ps1, run_checks_pc.ps1. Quote-Arg, Invoke-Tool, Find-Exe, Find-Python: kenburns_24.ps1, run_checks_pc.ps1.
function Show-Path([string]$p) {
    # Never echo a profile path: print the project folder as <project> and the profile and temp folders in unexpanded form.
    $s = $p
    $full = $p
    try { $full = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).ProviderPath, $p)) } catch { $full = $p }
    $pr = $script:ProjectRoot
    if ($pr -and $full.Length -ge $pr.Length -and $full.Substring(0, $pr.Length).ToLower() -eq $pr.ToLower()) {
        if ($full.Length -eq $pr.Length -or $full[$pr.Length] -eq [char]92 -or $full[$pr.Length] -eq [char]47) { return ('<project>' + $full.Substring($pr.Length)) }
    }
    foreach ($pair in @(@($env:TEMP, '%TEMP%'), @($env:USERPROFILE, '%USERPROFILE%'), @($HOME, '%USERPROFILE%'))) {
        $base = $pair[0]
        if ($base -and $s.Length -ge $base.Length -and $s.Substring(0, $base.Length).ToLower() -eq $base.ToLower()) {
            $s = $pair[1] + $s.Substring($base.Length)
            break
        }
    }
    return $s
}

function Clean-Message([string]$msg) {
    # Make an error message safe to print: no paths, no names, short.
    if (-not $msg) { return '' }
    $m = $msg -replace '[A-Za-z]:\\[^''"\s]*', '<path>'
    $m = $m -replace '(/[^/\s''"]+)+', '<path>'
    foreach ($n in @([Environment]::UserName, $env:USERNAME, $env:COMPUTERNAME, [Environment]::MachineName, $env:USERDOMAIN)) {
        if ($n -and $n.Length -ge 3) { $m = [regex]::Replace($m, [regex]::Escape($n), '<name>', 'IgnoreCase') }
    }
    $m = ($m -replace '\s+', ' ').Trim()
    if ($m.Length -gt 140) { $m = $m.Substring(0, 140) }
    return $m
}

function Step([string]$label) {
    $script:StepNo++
    Write-Host ("[{0}/{1}] {2} ... " -f $script:StepNo, $TotalSteps, $label) -NoNewline
}

function Problem([string]$text) {
    $script:Problems++
    Say ('  PROBLEM ' + $text)
}

function Test-Header([string]$file, [string[]]$cols) {
    $lines = [System.IO.File]::ReadAllLines($file)
    if ($lines.Count -eq 0) { return 'the file is empty' }
    $first = ($lines[0] -replace '"', '').Trim()
    $want = ($cols -join ',')
    if ($first -ne $want) { return 'the first line is not the playbook header' }
    return $null
}

# ---- step 1: the folder
Step 'Checking the folder you named'
if (-not $Root -or -not $Root.Trim()) { Say 'REFUSED'; Say '-Root is empty.'; exit 2 }
$full = ''
try { $full = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).ProviderPath, $Root)) }
catch { Say 'REFUSED'; Say '-Root is not a usable folder name.'; exit 2 }
$shownRoot = Show-Path $full
if (-not (Test-Path -LiteralPath $full -PathType Container)) { Say 'NOT FOUND'; Say ('There is no folder ' + $shownRoot + '. Run archive_init.ps1 first.'); exit 2 }
Say ('ok (' + $shownRoot + ')')

# ---- step 2: the project script that does the checking
Step 'Finding the project checksum script (verify_manifest.ps1)'
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$vfScript = Join-Path (Join-Path (Join-Path (Join-Path $repo 'research') 'sources') 'format-round1') 'verify_manifest.ps1'
if (-not (Test-Path -LiteralPath $vfScript)) { Say 'MISSING'; Say 'research\sources\format-round1\verify_manifest.ps1 is missing: download the WHOLE project folder, not single files.'; exit 3 }
Say 'ok'

$checkedLine = ''
try {
    # ---- step 3: folders and record files
    Step 'Checking the four folders and the two record files'
    Say ''
    foreach ($f in $FolderNames) {
        if (Test-Path -LiteralPath (Join-Path $full $f) -PathType Container) { Say ('  ok      folder ' + $f) } else { Problem ('MISSING folder ' + $f) }
    }
    foreach ($pair in @(@('manifest.csv', $ManifestColumns), @('steps.csv', $StepsColumns))) {
        $p = Join-Path $full $pair[0]
        if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { Problem ('MISSING ' + $pair[0]); continue }
        $bad = Test-Header $p $pair[1]
        if ($bad) { Problem ('HEADER ' + $pair[0] + ': ' + $bad) } else { Say ('  ok      ' + $pair[0] + ' header (' + $pair[1].Count + ' columns)') }
    }

    # ---- step 4: the checksums
    Step 'Checking every file in checksums.txt against its SHA-256 (verify_manifest.ps1, run inside 01_masters)'
    Say ''
    $sums = Join-Path $full 'checksums.txt'
    $masters = Join-Path $full '01_masters'
    $listed = @{}
    if (-not (Test-Path -LiteralPath $sums -PathType Leaf)) { Problem 'MISSING checksums.txt' }
    elseif (-not (Test-Path -LiteralPath $masters -PathType Container)) { Problem 'cannot check checksums.txt without the folder 01_masters' }
    else {
        foreach ($ln in [System.IO.File]::ReadAllLines($sums)) {
            if ($ln.Trim()) {
                $parts = $ln -split ' \*', 2
                if ($parts.Count -eq 2) { $listed[$parts[1].Replace('/', '\').ToLower()] = $true }
            }
        }
        Push-Location -LiteralPath $masters
        $lines = @()
        try { $lines = @(& $vfScript -Manifest $sums) } finally { Pop-Location }
        foreach ($ln in $lines) {
            $t = [string]$ln
            if ($t -match '^checked [0-9]+ files, [0-9]+ problems$') { $checkedLine = $t; Say ('  ' + $t) }
            elseif ($t -match '^(MISSING|MISMATCH)') { Say ('  ' + $t) }
            else { Say ('  ' + $t) }
        }
        if (-not $checkedLine) { Problem 'verify_manifest.ps1 did not print its summary line' }
        elseif ($checkedLine -match 'checked [0-9]+ files, ([0-9]+) problems') { $script:Problems += [int]$Matches[1] }
    }

    # ---- step 5: files nobody listed
    Step 'Looking for files in 01_masters that checksums.txt does not list'
    Say ''
    $unlisted = 0
    if ((Test-Path -LiteralPath $masters -PathType Container) -and (Test-Path -LiteralPath $sums -PathType Leaf)) {
        $mastersFull = (Resolve-Path -LiteralPath $masters).ProviderPath.TrimEnd('\', '/')
        foreach ($f in @(Get-ChildItem -LiteralPath $masters -Recurse -File -Force)) {
            $rel = $f.FullName.Substring($mastersFull.Length).TrimStart('\', '/').Replace('/', '\')
            if (-not $listed.ContainsKey($rel.ToLower())) { $unlisted++; Say ('  UNLISTED ' + $rel + '  (not in checksums.txt: a new scan needs its checksum added)') }
        }
    }
    Say ('  unlisted files in 01_masters: ' + $unlisted + ' (information, not counted as a problem)')
} catch {
    Say ''
    Say ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    Say 'files written: none'
    exit 3
}

if ($script:Problems -eq 0) { Say 'RESULT: OK, no problems' } else { Say ('RESULT: ' + $script:Problems + ' problem(s) found, see the PROBLEM, MISSING and MISMATCH lines above') }
Say 'files written: none'
if ($script:Problems -eq 0) { exit 0 } else { exit 1 }
