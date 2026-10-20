<#
.SYNOPSIS
  Life Journey archive skeleton (Exercise 1 of playbooks\ai-imagery.md, WP-09 kit B). CREATES a new folder tree and a few small
  files, only inside the folder you name, and only if that folder is new or empty.

.DESCRIPTION
  Builds the four folders of Step 0 of the imagery playbook (01_masters, 02_work, 03_exports, 04_reconstructions), the two record
  files with their header lines only (manifest.csv and steps.csv; you fill the rows), and checksums.txt for the masters. For the
  practice run it also makes SYNTHETIC stand-in scans (a gradient, a checker and a ring drawn by this script; nothing of yours,
  nothing from a camera) with ids LJ-ST-0001-F, LJ-ST-0002-F ... where ST is the stand-in box code. The checksums are written by
  the project's own research\sources\format-round1\mk_manifest.ps1 and read back with verify_manifest.ps1, both called where they
  sit in the project folder, not copied.

  It never deletes or overwrites anything: if the folder already holds something that is not an archive made by this script it
  stops and changes nothing; if it already is one it says so and changes nothing. It does not touch the network, your photos, your
  settings or the registry, and it needs no administrator rights.

  Real scans go in the encrypted container (W-25), never in the project folder: use -Count 0 there for the empty skeleton.

.PARAMETER Root
  The folder to build. Default C:\lj\standin (later: a folder inside the encrypted container). A drive root such as E:\ is refused.

.PARAMETER Count
  How many stand-in scans (fronts) to make, 0 to 50. Default 5.

.PARAMETER WithBacks
  Also make a stand-in back (-B) for every front.

.NOTES
  Exit codes: 0 done (or already an archive); 2 the options or the folder were not acceptable (nothing changed);
  3 a project file is missing or something could not be written. Windows PowerShell 5.1 and PowerShell 7.
  Run for one session only, without changing system policy:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\archive_init.ps1
  Every claim about Windows behaviour in this script is UNVERIFIED until the maker's first real run.
#>
[CmdletBinding()]
param(
    [string]$Root = 'C:\lj\standin',
    [int]$Count = 5,
    [switch]$WithBacks
)

$ErrorActionPreference = 'Stop'
$ScriptVersion = '1.0.0'

# Anything unexpected that would otherwise print a red error (which can carry a folder name): say it in scrubbed words and stop.
trap {
    Write-Host ''
    Write-Host ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    if ($script:Written.Count -gt 0) { Write-Host ('files written (some, before the stop): ' + ($script:Written -join '; ')) } else { Write-Host 'files written: none' }
    exit 3
}
$TotalSteps = 8

# Names and columns from Step 0 of playbooks\ai-imagery.md (tests/win_kit2 compares them with that playbook).
$FolderNames = @('01_masters', '02_work', '03_exports', '04_reconstructions')
$ManifestColumns = @('id', 'box', 'medium', 'scan_date', 'device', 'ppi', 'bit_depth', 'profile', 'date_est', 'date_confidence', 'people', 'place', 'caption_source', 'interview_date', 'consent_note', 'sha256', 'notes')
$StepsColumns = @('derivative_id', 'parent_id', 'step_no', 'tool', 'version', 'settings', 'seed', 'invents', 'label_level', 'reviewer', 'approved', 'deity_form', 'deity_source')
$BoxCode = 'ST'
$ImgW = 300
$ImgH = 200
$script:StepNo = 0
$script:Written = New-Object System.Collections.ArrayList

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

function Stop-Here([int]$code, [string]$why) {
    Say ''
    Say $why
    if ($script:Written.Count -gt 0) { Say ('files written (some, before the stop): ' + ($script:Written -join '; ')) } else { Say 'files written: none' }
    exit $code
}

function Get-Utf8NoBom { return (New-Object System.Text.UTF8Encoding($false)) }

function New-Tiff16([int]$w, [int]$h, [int]$n, [bool]$back) {
    # A baseline uncompressed 16-bit-per-channel RGB TIFF (little-endian) of a synthetic picture, as bytes.
    $dataLen = $w * $h * 6
    $data = New-Object byte[] $dataLen
    $k = 0
    $cx = [int]($w / 2)
    $cy = [int]($h / 2)
    $r1 = 38 * 38
    $r2 = 46 * 46
    $shade = (($n * 37) % 120) + 40
    for ($y = 0; $y -lt $h; $y++) {
        $g = [int]($y * 255 / ($h - 1))
        for ($x = 0; $x -lt $w; $x++) {
            if ($back) {
                $rr = 238; $gg = 232; $bb = 220
                if (($y % 24) -ge 10 -and ($y % 24) -lt 13 -and $x -gt 30 -and $x -lt ($w - 30 - (($y * 7 + $n * 13) % 80))) { $rr = 60; $gg = 58; $bb = 70 }
            } else {
                $rr = [int]($x * 255 / ($w - 1))
                $gg = $g
                $bb = $shade
                if (((($x -shr 4) + ($y -shr 4)) -band 1) -eq 1) { $bb = $shade + 70 }
                $dx = $x - $cx
                $dy = $y - $cy
                $d2 = $dx * $dx + $dy * $dy
                if ($d2 -ge $r1 -and $d2 -le $r2) { $rr = 250; $gg = 250; $bb = 245 }
            }
            $rr = $rr -band 255; $gg = $gg -band 255; $bb = $bb -band 255
            $data[$k] = $rr; $data[$k + 1] = $rr
            $data[$k + 2] = $gg; $data[$k + 3] = $gg
            $data[$k + 4] = $bb; $data[$k + 5] = $bb
            $k += 6
        }
    }
    $ms = New-Object System.IO.MemoryStream
    $bw = New-Object System.IO.BinaryWriter($ms)
    $bw.Write([byte]73); $bw.Write([byte]73); $bw.Write([uint16]42)
    $ifdOffset = 8 + $dataLen + 6 + 8 + 8
    $bw.Write([uint32]$ifdOffset)
    $bw.Write($data)
    $bitsOffset = 8 + $dataLen
    $bw.Write([uint16]16); $bw.Write([uint16]16); $bw.Write([uint16]16)
    $xresOffset = $bitsOffset + 6
    $bw.Write([uint32]600); $bw.Write([uint32]1)
    $yresOffset = $xresOffset + 8
    $bw.Write([uint32]600); $bw.Write([uint32]1)
    $entries = @(
        @(256, 3, 1, $w),
        @(257, 3, 1, $h),
        @(258, 3, 3, $bitsOffset),
        @(259, 3, 1, 1),
        @(262, 3, 1, 2),
        @(273, 4, 1, 8),
        @(277, 3, 1, 3),
        @(278, 3, 1, $h),
        @(279, 4, 1, $dataLen),
        @(282, 5, 1, $xresOffset),
        @(283, 5, 1, $yresOffset),
        @(284, 3, 1, 1),
        @(296, 3, 1, 2)
    )
    $bw.Write([uint16]$entries.Count)
    foreach ($e in $entries) {
        $bw.Write([uint16]$e[0]); $bw.Write([uint16]$e[1]); $bw.Write([uint32]$e[2])
        if ($e[1] -eq 3 -and $e[2] -eq 1) { $bw.Write([uint16]$e[3]); $bw.Write([uint16]0) } else { $bw.Write([uint32]$e[3]) }
    }
    $bw.Write([uint32]0)
    $bw.Flush()
    $bytes = $ms.ToArray()
    $bw.Close()
    return $bytes
}

function Get-Header([string[]]$cols) { return (($cols -join ',') + "`n") }

# ---- step 1: options and the folder you chose
Step 'Checking the options and the folder you chose'
if ($Count -lt 0 -or $Count -gt 50) { Say 'REFUSED'; Stop-Here 2 '-Count must be between 0 and 50. Nothing was changed.' }
if (-not $Root -or -not $Root.Trim()) { Say 'REFUSED'; Stop-Here 2 '-Root is empty. Nothing was changed.' }
$full = ''
try { $full = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).ProviderPath, $Root)) }
catch { Say 'REFUSED'; Stop-Here 2 ('-Root is not a usable folder name. Nothing was changed.') }
$trimmed = $full.TrimEnd('\', '/')
$shownRoot = Show-Path $full
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$repoFull = [System.IO.Path]::GetFullPath($repo).TrimEnd('\', '/')
$profileFull = ''
if ($env:USERPROFILE) { $profileFull = $env:USERPROFILE.TrimEnd('\', '/') } elseif ($HOME) { $profileFull = $HOME.TrimEnd('\', '/') }
if ($trimmed.Length -le 2 -or $trimmed -eq [System.IO.Path]::GetPathRoot($full).TrimEnd('\', '/')) { Say 'REFUSED'; Stop-Here 2 'That is a drive root. Choose a folder inside it, for example E:\lj\standin. Nothing was changed.' }
if ($trimmed.ToLower() -eq $repoFull.ToLower()) { Say 'REFUSED'; Stop-Here 2 'That is the project folder itself. Choose another folder. Nothing was changed.' }
if ($profileFull -and $trimmed.ToLower() -eq $profileFull.ToLower()) { Say 'REFUSED'; Stop-Here 2 'That is your whole user folder. Choose a folder inside it. Nothing was changed.' }
Say 'ok'
Say ('  folder: ' + $shownRoot)
if ($trimmed.ToLower().StartsWith($repoFull.ToLower() + [System.IO.Path]::DirectorySeparatorChar)) {
    Say '  NOTE this folder is inside the project folder. That is fine for the practice stand-ins (renders\ is ignored by git). Real scans go in the encrypted container, never in the project folder.'
}

# ---- step 2: the reused checksum scripts
Step 'Finding the project checksum scripts (mk_manifest.ps1 and verify_manifest.ps1)'
$mkScript = Join-Path (Join-Path (Join-Path (Join-Path $repo 'research') 'sources') 'format-round1') 'mk_manifest.ps1'
$vfScript = Join-Path (Join-Path (Join-Path (Join-Path $repo 'research') 'sources') 'format-round1') 'verify_manifest.ps1'
if (-not (Test-Path -LiteralPath $mkScript) -or -not (Test-Path -LiteralPath $vfScript)) {
    Say 'MISSING'
    Stop-Here 3 'research\sources\format-round1\mk_manifest.ps1 or verify_manifest.ps1 is missing: download the WHOLE project folder, not single files. Nothing was changed.'
}
Say 'ok'

# ---- step 3: is the folder new or empty?
Step 'Checking that the folder is new or empty'
$alreadyArchive = $false
if (Test-Path -LiteralPath $full) {
    if (-not (Test-Path -LiteralPath $full -PathType Container)) { Say 'REFUSED'; Stop-Here 2 'That name is a file, not a folder. Nothing was changed.' }
    $items = @(Get-ChildItem -LiteralPath $full -Force)
    if ($items.Count -gt 0) {
        $haveAll = $true
        foreach ($f in $FolderNames) { if (-not (Test-Path -LiteralPath (Join-Path $full $f) -PathType Container)) { $haveAll = $false } }
        foreach ($f in @('manifest.csv', 'steps.csv', 'checksums.txt')) { if (-not (Test-Path -LiteralPath (Join-Path $full $f) -PathType Leaf)) { $haveAll = $false } }
        if ($haveAll) { $alreadyArchive = $true }
        else { Say 'REFUSED'; Stop-Here 2 'That folder already holds other things. This script only builds in a new or empty folder, so nothing was changed. Choose another folder.' }
    }
}
if ($alreadyArchive) {
    Say 'it already is an archive'
    Say 'Nothing was changed. Run archive_verify.ps1 to check it.'
    Say 'files written: none'
    exit 0
}
Say 'ok'

try {
    # ---- step 4: the four folders
    Step ('Creating the four folders (' + ($FolderNames -join ', ') + ')')
    [void][System.IO.Directory]::CreateDirectory($full)
    foreach ($f in $FolderNames) { [void][System.IO.Directory]::CreateDirectory((Join-Path $full $f)) ; [void]$script:Written.Add($f + '\') }
    Say 'ok'

    # ---- step 5: the two record files, header line only
    Step 'Writing manifest.csv and steps.csv (the header line only; you fill the rows)'
    [System.IO.File]::WriteAllText((Join-Path $full 'manifest.csv'), (Get-Header $ManifestColumns), (Get-Utf8NoBom))
    [System.IO.File]::WriteAllText((Join-Path $full 'steps.csv'), (Get-Header $StepsColumns), (Get-Utf8NoBom))
    [void]$script:Written.Add('manifest.csv'); [void]$script:Written.Add('steps.csv')
    Say 'ok'

    # ---- step 6: the synthetic stand-in scans
    $masters = Join-Path $full '01_masters'
    if ($Count -gt 0) {
        $what = "$Count"
        if ($WithBacks) { $what = "$Count fronts and $Count backs" }
        Step ("Drawing $what synthetic stand-in scan(s), box code $BoxCode, 16-bit TIFF, " + $ImgW + 'x' + $ImgH + ' (nothing of yours)')
        for ($n = 1; $n -le $Count; $n++) {
            $sides = @('F')
            if ($WithBacks) { $sides = @('F', 'B') }
            foreach ($side in $sides) {
                $id = 'LJ-{0}-{1:0000}-{2}' -f $BoxCode, $n, $side
                $bytes = New-Tiff16 $ImgW $ImgH $n ($side -eq 'B')
                [System.IO.File]::WriteAllBytes((Join-Path $masters ($id + '.tif')), $bytes)
                [void]$script:Written.Add('01_masters\' + $id + '.tif')
            }
        }
        Say 'ok'
    } else {
        Step 'No stand-in scans requested (-Count 0): the skeleton stays empty'
        Say 'ok'
    }

    # ---- step 7: checksums.txt with the reused mk_manifest.ps1
    Step 'Writing checksums.txt for 01_masters with the project mk_manifest.ps1 (paths inside it are relative to 01_masters)'
    Push-Location -LiteralPath $masters
    try { $null = & $mkScript } finally { Pop-Location }
    $made = Join-Path $full 'SHA256SUMS.txt'
    if (-not (Test-Path -LiteralPath $made)) { throw 'mk_manifest.ps1 did not write its list' }
    [System.IO.File]::Move($made, (Join-Path $full 'checksums.txt'))
    [void]$script:Written.Add('checksums.txt')
    Say 'ok'

    # ---- step 8: read it back with the reused verify_manifest.ps1
    Step 'Reading it back with the project verify_manifest.ps1'
    Say ''
    Push-Location -LiteralPath $masters
    $lines = @()
    try { $lines = @(& $vfScript -Manifest (Join-Path $full 'checksums.txt')) } finally { Pop-Location }
    foreach ($ln in $lines) { Say ('  ' + $ln) }
    $summary = ''
    if ($lines.Count -gt 0) { $summary = [string]$lines[$lines.Count - 1] }
    if ($summary -notmatch '^checked [0-9]+ files, 0 problems$') { throw 'the read-back did not report 0 problems' }
} catch {
    Say ''
    Say ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    Say 'What was already made is left as it is (nothing is deleted). Choose a new folder, or look at it and remove it yourself.'
    if ($script:Written.Count -gt 0) { Say ('files written (under ' + $shownRoot + '): ' + ($script:Written -join '; ')) } else { Say 'files written: none' }
    exit 3
}

Say 'Next: fill manifest.csv (one row per scan) in a spreadsheet or Notepad, then run  .\win\kit2\archive_verify.ps1 -Root <the same folder you gave here>'
Say ('files written (under ' + $shownRoot + '): ' + ($script:Written -join '; '))
exit 0
