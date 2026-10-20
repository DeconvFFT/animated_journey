<#
.SYNOPSIS
  Life Journey Ken Burns at 24 fps (Exercise 2, WP-09 kit B). Reads the stills you name, writes ONE video file (and, if you ask,
  a few proof files beside it). Never changes your stills.

.DESCRIPTION
  A thin front door for win\kit2\kenburns_24.py: it finds Python 3, checks that Pillow and numpy are installed, finds ffmpeg, and
  then runs the Python tool, whose own output you see live. The video is 1920x1080, 24 fps, H.264 High, yuv420p, with BT.709
  colour tags, made through the project's h264_online encode chain: three moves of about six seconds (push-in, pan, pull-out)
  joined by one-second dissolves. A round thing in your still stays round (the tool cuts a 16:9 window, it never stretches).

  Use your own stills of things that are NOT family photos (D-13: her photos wait until the P-LOCK gate on Sat 14 Nov).
  It installs nothing, uses no network and needs no administrator rights.

.PARAMETER Stills
  Two or more still pictures (JPEG, PNG or TIFF), in the order of the moves. Three for the exercise.

.PARAMETER Out
  The .mp4 to write. Default: renders\ex02\ex02_kenburns.mp4 inside the project folder (renders\ is ignored by git).

.PARAMETER Selftest
  Instead of your stills, draw three synthetic ones and check the whole chain (nothing of yours is read). Writes renders\wp09\ex02.mp4.

.PARAMETER ProofZoompan
  Also make the ffmpeg zoompan version of the push (proof only: it jitters), so you can see the difference.

.PARAMETER GateWindow
  Also write a lossless 96-frame window of the push (100 to 250 MB; delete it afterwards) so mo8_gate.py can judge the motion.

.PARAMETER Moves
  Comma list, one move per still: push, pan, pull, drift. Default push,pan,pull.

.PARAMETER Focus
  Where the 16:9 window sits in a still that is not 16:9, as X,Y between 0 and 1 (0.5,0.5 is the middle).

.PARAMETER Ffmpeg
  The ffmpeg to use (full path). Default: the one found on PATH.

.NOTES
  Exit codes: 0 done and the read-back passed; 1 the read-back failed; 2 the options or a still were not acceptable;
  3 Python, Pillow, numpy or ffmpeg is missing, or ffmpeg failed. Windows PowerShell 5.1 and PowerShell 7.
  Run for one session only, without changing system policy:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\kenburns_24.ps1 a.jpg b.jpg c.jpg
  Every claim about Windows behaviour in this script is UNVERIFIED until the maker's first real run.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Stills = @(),
    [string]$Out = '',
    [switch]$Selftest,
    [switch]$ProofZoompan,
    [switch]$GateWindow,
    [string]$Moves = 'push,pan,pull',
    [string]$Focus = '',
    [string]$Ffmpeg = ''
)

$ErrorActionPreference = 'Continue'
$ScriptVersion = '1.0.0'

# Anything unexpected that would otherwise print a red error (which can carry a folder name): say it in scrubbed words and stop.
trap {
    Write-Host ''
    Write-Host ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    Write-Host 'files written: none'
    exit 3
}
$TotalSteps = 5
$script:StepNo = 0
$PipLine = 'py -3 -m pip install --user pillow numpy'

$script:ProjectRoot = ''
try { $script:ProjectRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent (Split-Path -Parent $PSScriptRoot))).TrimEnd([char]92, [char]47) } catch { $script:ProjectRoot = '' }

function Say([string]$text) { Write-Host $text }

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

function Quote-Arg([string]$a) {
    # One argument for a Windows command line (the CommandLineToArgvW rules): quote only when needed.
    if ($null -eq $a) { return '""' }
    if ($a.Length -gt 0 -and $a -notmatch '[\s"]') { return $a }
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append('"')
    $bs = 0
    foreach ($ch in $a.ToCharArray()) {
        if ($ch -eq [char]92) { $bs++ }
        elseif ($ch -eq [char]34) { [void]$sb.Append(('\' * ($bs * 2 + 1))); [void]$sb.Append('"'); $bs = 0 }
        else {
            if ($bs -gt 0) { [void]$sb.Append(('\' * $bs)); $bs = 0 }
            [void]$sb.Append($ch)
        }
    }
    if ($bs -gt 0) { [void]$sb.Append(('\' * ($bs * 2))) }
    [void]$sb.Append('"')
    return $sb.ToString()
}

function Invoke-Tool([string]$exe, [string[]]$arguments, [int]$timeoutSec) {
    # Runs one program with a time limit and returns its text. Only programs found by this script are run.
    $r = @{ ok = $false; exit = $null; stdout = ''; stderr = ''; timedout = $false }
    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $exe
        $psi.Arguments = (($arguments | ForEach-Object { Quote-Arg $_ }) -join ' ')
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.RedirectStandardInput = $true
        $psi.CreateNoWindow = $true
        $p = New-Object System.Diagnostics.Process
        $p.StartInfo = $psi
        [void]$p.Start()
        $p.StandardInput.Close()
        $tOut = $p.StandardOutput.ReadToEndAsync()
        $tErr = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit($timeoutSec * 1000)) {
            try { $p.Kill() } catch { }
            $r.timedout = $true
            return $r
        }
        $p.WaitForExit()
        $r.exit = $p.ExitCode
        $r.stdout = ($tOut.Result -replace "`0", '')
        $r.stderr = ($tErr.Result -replace "`0", '')
        $r.ok = $true
    } catch {
        $r.ok = $false
    }
    return $r
}

function Find-Exe([string]$name) {
    $c = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c -and $c.Source) { return $c.Source }
    if ($c -and $c.Path) { return $c.Path }
    return $null
}

function Find-Python {
    # Returns @{ exe; prefix } or $null. The Windows Store "python" stub prints a message instead of "Python 3.x": rejected.
    $cands = @(@('py', @('-3')), @('python', @()), @('python3', @()))
    foreach ($c in $cands) {
        $exe = Find-Exe $c[0]
        if (-not $exe) { continue }
        $t = Invoke-Tool $exe (@($c[1]) + @('--version')) 30
        if ($t.ok -and -not $t.timedout -and $t.exit -eq 0 -and (($t.stdout + $t.stderr) -match 'Python 3\.[0-9]+')) {
            return @{ exe = $exe; prefix = @($c[1]) }
        }
    }
    return $null
}

function Step([string]$label) {
    $script:StepNo++
    Write-Host ("[{0}/{1}] {2} ... " -f $script:StepNo, $TotalSteps, $label) -NoNewline
}

# ---- step 1: the options
Step 'Checking the options'
if (-not $Selftest -and $Stills.Count -lt 2) {
    Say 'REFUSED'
    Say 'Give at least two stills (three for the exercise), for example:  .\win\kit2\kenburns_24.ps1 a.jpg b.jpg c.jpg   (or use -Selftest)'
    Say 'files written: none'
    exit 2
}
if ($Selftest -and $Stills.Count -gt 0) { Say 'REFUSED'; Say '-Selftest makes its own stills; do not give any.'; Say 'files written: none'; exit 2 }
if (-not $Selftest) {
    foreach ($s in $Stills) {
        if (-not (Test-Path -LiteralPath $s -PathType Leaf)) { Say 'REFUSED'; Say 'One of the stills was not found (check the spelling and the folder).'; Say 'files written: none'; exit 2 }
    }
}
Say 'ok'

# ---- step 2: Python
Step 'Looking for Python 3 (py -3, python or python3)'
$py = Find-Python
if (-not $py) {
    Say 'NOT FOUND'
    Say 'Python 3 is needed. README-KIT2.md has the install line (winget id UNVERIFIED). Nothing was written.'
    Say 'files written: none'
    exit 3
}
Say 'ok'

# ---- step 3: Pillow and numpy (checked by the tool itself, in the same isolated mode the real run uses)
Step 'Checking that Pillow and numpy are installed'
$toolForCheck = Join-Path $PSScriptRoot 'kenburns_24.py'
if (-not (Test-Path -LiteralPath $toolForCheck)) { Say 'MISSING'; Say 'kenburns_24.py is missing: download the WHOLE project folder, not single files.'; Say 'files written: none'; exit 3 }
$t = Invoke-Tool $py.exe (@($py.prefix) + @('-I', $toolForCheck, '--check-libs')) 120
if (-not ($t.ok -and $t.exit -eq 0)) {
    Say 'MISSING'
    Say ('Install them for your user (no administrator rights needed) with:  ' + $PipLine)
    Say 'Then run this again. Nothing was written.'
    Say 'files written: none'
    exit 3
}
Say 'ok'

# ---- step 4: ffmpeg
Step 'Looking for ffmpeg'
$ffmpegExe = $null
if ($Ffmpeg) { if (Test-Path -LiteralPath $Ffmpeg -PathType Leaf) { $ffmpegExe = (Resolve-Path -LiteralPath $Ffmpeg).ProviderPath } }
else { $ffmpegExe = Find-Exe 'ffmpeg' }
if (-not $ffmpegExe) {
    Say 'NOT FOUND'
    Say 'ffmpeg is needed. README-KIT2.md has the install line (winget id UNVERIFIED). Nothing was written.'
    Say 'files written: none'
    exit 3
}
Say 'ok'

# ---- step 5: the Python tool, with its own output shown live
$script = Join-Path $PSScriptRoot 'kenburns_24.py'
if (-not (Test-Path -LiteralPath $script)) { Step 'Finding kenburns_24.py'; Say 'MISSING (download the WHOLE project folder, not single files)'; Say 'files written: none'; exit 3 }
$outPath = $Out
if (-not $outPath) {
    if ($Selftest) { $outPath = Join-Path (Join-Path (Join-Path $script:ProjectRoot 'renders') 'wp09') 'ex02.mp4' }
    else { $outPath = Join-Path (Join-Path (Join-Path $script:ProjectRoot 'renders') 'ex02') 'ex02_kenburns.mp4' }
}
$argList = @('-I', $script, '--ffmpeg', $ffmpegExe, '--out', $outPath)
if ($Selftest) { $argList += '--selftest' }
else {
    $argList += '--moves'
    $argList += $Moves
    if ($Focus) { $argList += '--focus'; $argList += $Focus }
    if ($ProofZoompan) { $argList += '--proof-zoompan' }
    if ($GateWindow) { $argList += '--gate-window' }
    foreach ($s in $Stills) { $argList += ((Resolve-Path -LiteralPath $s).ProviderPath) }
}
Step 'Making the video (the tool prints its own steps below; about a minute)'
Say ''
$code = 3
$callArgs = @($py.prefix) + $argList
$started = Get-Date
try {
    & $py.exe @callArgs
    $code = $LASTEXITCODE
} catch {
    Say ('could not run the Python tool: ' + (Clean-Message $_.Exception.Message))
    $code = 3
}

$written = @()
$stem = [System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($outPath), [System.IO.Path]::GetFileNameWithoutExtension($outPath))
foreach ($cand in @($outPath, ($stem + '_push_only.mkv'), ($stem + '_zoompan_proof.mp4'), ($stem + '_push_only_zoompan.mkv'))) {
    if ((Test-Path -LiteralPath $cand -PathType Leaf) -and ((Get-Item -LiteralPath $cand).LastWriteTime -ge $started.AddSeconds(-2))) { $written += (Show-Path $cand) }
}
if ($code -ge 2) { Say ('The tool stopped with exit code ' + $code + ' (see its message above).') }
if ($written.Count -gt 0) { Say ('files written: ' + ($written -join '; ')) } else { Say 'files written: none' }
exit $code
