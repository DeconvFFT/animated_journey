<#
.SYNOPSIS
  Life Journey session helper, version 0. DRY RUN ONLY: it shows things, it never changes anything.

.DESCRIPTION
  Commands
    doctor   Reads a PC inventory report and prints the hardware tier table.
    close    Lists exactly what an end-of-session clean-up WOULD remove. Removes nothing.
    help     Prints this summary.

  Version 0 has no way to delete, move, rename, commit, push or write a file. The switches that would
  do that (-Apply, -Commit, -IncludeWindowsRecent) do not exist until version 1 (week 4). If you type
  one, the script says so, does nothing, and exits with code 2.

  doctor [-FromReport PATH] [-SaveTier PATH]
    Without -FromReport it runs the sibling step0_pc_tests.ps1 (read-only inventory). THAT script writes
    its own report to %TEMP%\lj_pc_report.json (one file, outside the project folder). lj.ps1 itself
    writes nothing. With -FromReport it only reads the report you name (nothing is collected).
    It then runs scripts\windows_check.py (py -3 -I -B or python -I -B) and prints the tier table.
    -SaveTier PATH additionally writes the DERIVED tier file (buckets and verdict words only, no
    hardware names or exact sizes). That file is written by windows_check.py, never by this script.

  close [-Config PATH] [-SkipChecks]
    Reads the config (default: lj.config.local.json beside this script), checks the root folder is a safe
    place to look, walks it read-only (links are listed and never followed) and prints:
      the numbered WOULD-REMOVE list with file counts and sizes, what is held back and why, links that
      were skipped, what is never touched, the per-app lists (UNVERIFIED until filled from a real paste),
      the read-only repo checks (stale_check.py --new-only and public_lint.py, if Python exists),
      the backup line (not implemented in v0) and the reminders.
    It writes nothing, not even a log. -SkipChecks leaves out the two repo checks.

.NOTES
  Exit codes: 0 done; 1 done, but the answer is partial or the checker found something for a human;
  2 refused or wrong usage (nothing was done); 3 the environment is missing something.
  Works in Windows PowerShell 5.1 and PowerShell 7. Needs no administrator rights and no network.
  Every claim about Windows behaviour in this file (reparse points on NTFS, py -3, the Microsoft Store
  python stub, env-variable names, 8.3 short names) is UNVERIFIED until the maker's first real run.
  There is deliberately no param() block: it lets this script answer -Apply and friends with a clear
  "not in v0" message instead of a PowerShell binding error.
#>

$ErrorActionPreference = 'Continue'
$script:LjVersion = '0.1.0'
$script:IsWin = ($env:OS -eq 'Windows_NT')
$script:MaxEntries = 250000
$script:Sep = [string][System.IO.Path]::DirectorySeparatorChar
if ($script:IsWin) { $script:PathCmp = [System.StringComparison]::OrdinalIgnoreCase } else { $script:PathCmp = [System.StringComparison]::Ordinal }
$script:StepNo = 0
$script:StepTotal = 0

# ------------------------------------------------------------------ small helpers
function Say([string]$text) { Write-Host $text }

function Begin-Step([string]$label) {
    $script:StepNo++
    Write-Host ('[{0}/{1}] {2} ... ' -f $script:StepNo, $script:StepTotal, $label) -NoNewline
}
function End-Step([string]$result) { Write-Host $result }

function Clean-Message([string]$msg) {
    # Make an error message safe to print: no paths, no names, short.
    if (-not $msg) { return '' }
    $m = $msg -replace '[A-Za-z]:\\[^''"\s]*', '<path>'
    $m = $m -replace '(/[^/\s''"]+)+', '<path>'
    foreach ($n in @([Environment]::UserName, $env:USERNAME, $env:COMPUTERNAME, [Environment]::MachineName, $env:USERDOMAIN)) {
        if ($n -and $n.Length -ge 3) { $m = [regex]::Replace($m, [regex]::Escape($n), '<name>', 'IgnoreCase') }
    }
    $m = ($m -replace '\s+', ' ').Trim()
    if ($m.Length -gt 100) { $m = $m.Substring(0, 100) }
    return $m
}

function Convert-Sep([string]$p) {
    if ($script:IsWin) { return $p.Replace('/', '\') }
    return $p.Replace('\', '/')
}

function Trim-Sep([string]$p) {
    $t = $p.TrimEnd([char[]]@('\', '/'))
    return $t
}

function Test-SamePath([string]$a, [string]$b) {
    if (-not $a -or -not $b) { return $false }
    return ([string]::Equals((Trim-Sep $a), (Trim-Sep $b), $script:PathCmp))
}

function Test-Inside([string]$child, [string]$parent) {
    # true when $child is strictly below $parent (both full paths)
    if (-not $child -or -not $parent) { return $false }
    $p = Trim-Sep $parent
    $c = Trim-Sep $child
    $p = $p + $script:Sep
    return ($c.Length -gt $p.Length -and $c.StartsWith($p, $script:PathCmp))
}

function Test-SameOrInside([string]$child, [string]$parent) {
    return ((Test-SamePath $child $parent) -or (Test-Inside $child $parent))
}

function Get-EnvList {
    # bases that are replaced by their unexpanded name when a path is printed (longest first)
    $pairs = New-Object System.Collections.ArrayList
    foreach ($v in @('TEMP', 'LOCALAPPDATA', 'APPDATA', 'USERPROFILE')) {
        $val = [Environment]::GetEnvironmentVariable($v)
        if ($val) { [void]$pairs.Add(@($val, ('%' + $v + '%'))) }
    }
    if ($HOME) { [void]$pairs.Add(@($HOME, '%USERPROFILE%')) }
    return , @($pairs | Sort-Object -Property @{ Expression = { $_[0].Length } } -Descending)
}

function Show-Path([string]$p) {
    # Never echo a profile path: print the unexpanded form instead.
    if (-not $p) { return '' }
    foreach ($pair in (Get-EnvList)) {
        $base = [string]$pair[0]
        if ((Test-SameOrInside $p $base)) {
            return ([string]$pair[1] + $p.Substring((Trim-Sep $base).Length))
        }
    }
    return $p
}

function Format-Size([long]$bytes) {
    $inv = [System.Globalization.CultureInfo]::InvariantCulture
    if ($bytes -lt 1024) { return ([string]$bytes + ' B') }
    if ($bytes -lt 1048576) { return (([double]$bytes / 1024).ToString('N1', $inv) + ' KB') }
    if ($bytes -lt 1073741824) { return (([double]$bytes / 1048576).ToString('N1', $inv) + ' MB') }
    return (([double]$bytes / 1073741824).ToString('N1', $inv) + ' GB')
}

function Get-FullPath([string]$p, [string]$baseDir) {
    $q = Convert-Sep $p
    if (-not [System.IO.Path]::IsPathRooted($q)) { $q = [System.IO.Path]::Combine($baseDir, $q) }
    return [System.IO.Path]::GetFullPath($q)
}

function Get-CurrentDir { return (Get-Location).ProviderPath }

function To-List($v) {
    # a JSON value (null, string or array) -> list of non-empty strings
    $list = New-Object System.Collections.ArrayList
    if ($null -eq $v) { return , $list }
    foreach ($x in @($v)) {
        if ($null -ne $x -and ([string]$x).Trim() -ne '') { [void]$list.Add(([string]$x).Trim()) }
    }
    return , $list
}

function Expand-EnvText([string]$text) {
    # %NAME% -> value. Returns @{ text; unset } where unset is the first variable that has no value.
    $unset = ''
    $out = [regex]::Replace($text, '%([A-Za-z_][A-Za-z0-9_()]*)%', {
            param($m)
            $val = [Environment]::GetEnvironmentVariable($m.Groups[1].Value)
            if ($val) { return $val }
            if (-not $script:UnsetVar) { $script:UnsetVar = $m.Groups[1].Value }
            return $m.Value
        })
    $unset = $script:UnsetVar
    $script:UnsetVar = ''
    return @{ text = $out; unset = $unset }
}

function Show-Help {
    Say ('lj.ps1 version ' + $script:LjVersion + ' (v0: DRY RUN ONLY. Nothing here deletes, moves, commits, pushes or writes.)')
    Say ''
    Say 'Commands'
    Say '  doctor [-FromReport PATH] [-SaveTier PATH]'
    Say '      Prints the hardware tier table. Without -FromReport it runs step0_pc_tests.ps1, which writes'
    Say '      its own report to %TEMP%\lj_pc_report.json. -SaveTier PATH writes the derived tier file only.'
    Say '  close [-Config PATH] [-SkipChecks]'
    Say '      Lists what an end-of-session clean-up WOULD remove. Removes nothing and writes nothing.'
    Say '      -Config defaults to lj.config.local.json beside this script (copy lj.config.example.json).'
    Say '  help'
    Say '      This text.'
    Say ''
    Say 'Not in v0 (planned for v1 in week 4): -Apply, -Commit, -IncludeWindowsRecent. They print a message and exit 2.'
    Say 'Exit codes: 0 done; 1 done but partial or a checker has a finding; 2 refused or wrong usage; 3 something is missing.'
    Say 'Run it for one session only, without changing system policy:'
    Say '  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 help'
}

# ------------------------------------------------------------------ Python lookup and runner (read-only)
function Find-Python {
    $cands = New-Object System.Collections.ArrayList
    if ($script:IsWin) {
        [void]$cands.Add(@{ exe = 'py'; pre = @('-3'); shown = 'py -3' })
        [void]$cands.Add(@{ exe = 'python'; pre = @(); shown = 'python' })
    } else {
        [void]$cands.Add(@{ exe = 'python3'; pre = @(); shown = 'python3' })
        [void]$cands.Add(@{ exe = 'python'; pre = @(); shown = 'python' })
    }
    foreach ($c in $cands) {
        $cmd = Get-Command $c.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $cmd) { continue }
        try {
            $probe = @($c.pre) + @('-I', '-B', '-c', 'import sys; sys.stdout.write(str(sys.version_info[0]))')
            $out = & $cmd.Source @probe 2>$null
            if ($LASTEXITCODE -eq 0 -and ([string]$out).Trim() -eq '3') {
                return @{ exe = $cmd.Source; pre = @($c.pre); shown = $c.shown }
            }
        } catch { }
    }
    return $null
}

function Invoke-Py($py, [string[]]$pyArgs) {
    $all = @($py.pre) + @('-I', '-B') + @($pyArgs)
    $lines = New-Object System.Collections.ArrayList
    $rc = 3
    try {
        $out = & $py.exe @all 2>&1
        $rc = $LASTEXITCODE
        foreach ($o in @($out)) { [void]$lines.Add(([string]$o).TrimEnd()) }
    } catch {
        [void]$lines.Add('could not run Python: ' + (Clean-Message $_.Exception.Message))
        $rc = 3
    }
    return @{ lines = $lines; rc = $rc }
}

# ------------------------------------------------------------------ doctor
function Invoke-Doctor($opt) {
    $repo = Split-Path -Parent $PSScriptRoot
    $wc = [System.IO.Path]::Combine([System.IO.Path]::Combine($repo, 'scripts'), 'windows_check.py')
    $script:StepNo = 0
    $script:StepTotal = 4
    Say 'lj doctor (v0, read-only). lj.ps1 itself writes nothing unless you pass -SaveTier.'

    # -SaveTier checks first, so a bad request stops before anything is collected
    $tierOut = ''
    if ($opt.ContainsKey('savetier')) {
        $raw = [string]$opt['savetier']
        $leaf = [System.IO.Path]::GetFileName($raw)
        $bad = ''
        if (-not $raw) { $bad = '-SaveTier needs a file name' }
        elseif ($raw.TrimEnd().EndsWith('\') -or $raw.TrimEnd().EndsWith('/')) { $bad = '-SaveTier must name a file, not a folder' }
        elseif (-not $leaf.ToLower().EndsWith('.json')) { $bad = '-SaveTier file name must end in .json' }
        elseif ($leaf -match '^(?i)(pc_report|colour_patch_pc|maker-pc)') { $bad = 'that file name is reserved for raw PC reports, which must never be filed' }
        if (-not $bad) {
            $tierOut = Get-FullPath $raw (Get-CurrentDir)
            if ([System.IO.Directory]::Exists($tierOut)) { $bad = '-SaveTier names a folder' }
            elseif ([System.IO.File]::Exists($tierOut)) {
                $head = ''
                try { $head = [System.IO.File]::ReadAllText($tierOut) } catch { }
                if ($head.Length -gt 4096) { $head = $head.Substring(0, 4096) }
                if ($head -notmatch 'lj-pc-tier/1') { $bad = 'that file exists and is not a tier file; it will not be overwritten' }
            }
        }
        if ($bad) {
            Say ('REFUSED: ' + $bad + '. Nothing was done.')
            Say 'files written: none'
            return 2
        }
    }

    # 1. the report
    $report = ''
    $step0Wrote = ''
    if ($opt.ContainsKey('fromreport')) {
        Begin-Step 'Reading the report you named (nothing is collected from this computer)'
        $report = Get-FullPath ([string]$opt['fromreport']) (Get-CurrentDir)
        if (-not [System.IO.File]::Exists($report)) {
            End-Step 'failed'
            Say 'REFUSED: that report file was not found. Nothing was done.'
            Say 'files written: none'
            return 2
        }
        End-Step ('ok (' + (Show-Path $report) + ')')
    } else {
        $script:StepNo++
        Say ('[1/4] Running step0_pc_tests.ps1, the read-only inventory. It writes ONE file of its own: %TEMP%\lj_pc_report.json')
        $step0 = [System.IO.Path]::Combine($PSScriptRoot, 'step0_pc_tests.ps1')
        if (-not [System.IO.File]::Exists($step0)) {
            Say '      failed: step0_pc_tests.ps1 was not found next to lj.ps1. Download the whole project folder, not single files.'
            Say 'files written: none'
            return 3
        }
        $report = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), 'lj_pc_report.json')
        $step0rc = 3
        try {
            & $step0 -Out $report | Out-Host
            $step0rc = $LASTEXITCODE
        } catch {
            Say ('step0_pc_tests.ps1 failed: ' + (Clean-Message $_.Exception.Message))
        }
        if ($step0rc -ne 0) {
            Say ('[1/4] step0_pc_tests.ps1 stopped with exit code ' + $step0rc + '; no tier table was made.')
            Say 'files written by lj.ps1: none (see the step0_pc_tests.ps1 lines above for what it wrote)'
            if ($step0rc -eq 2) { return 2 }
            return 3
        }
        Say '[1/4] step0_pc_tests.ps1 finished ... ok'
        $step0Wrote = '%TEMP%\lj_pc_report.json'
    }

    # 2. Python
    Begin-Step 'Looking for Python (py -3 -I, or python -I)'
    $py = Find-Python
    if (-not $py) {
        End-Step 'not found'
        Say 'Python 3 was not found, so the tier table cannot be made on this PC.'
        Say 'That is fine: paste the report in chat (see README-MAKER.md) and the tier table is made for you.'
        if ($step0Wrote) { Say ('files written by step0_pc_tests.ps1: ' + $step0Wrote) } else { Say 'files written: none' }
        return 3
    }
    End-Step ('ok (' + $py.shown + ')')

    # 3. the checker
    Begin-Step 'Running scripts\windows_check.py (read-only; masks anything that looks like identifying data)'
    if (-not [System.IO.File]::Exists($wc)) {
        End-Step 'failed'
        Say 'scripts\windows_check.py was not found. Download the whole project folder, not single files.'
        if ($step0Wrote) { Say ('files written by step0_pc_tests.ps1: ' + $step0Wrote) } else { Say 'files written: none' }
        return 3
    }
    $pyArgs = @($wc)
    if ($tierOut) { $pyArgs += @('--tier-json-out', $tierOut) }
    $pyArgs += $report
    $res = Invoke-Py $py $pyArgs
    $rc = [int]$res.rc
    End-Step ('exit ' + $rc)
    foreach ($ln in $res.lines) { Say ('  ' + $ln) }
    Say '  (This table is for you and for chat only. It shows exact sizes. Do not copy it into the project folder.)'

    # 4. summary
    Begin-Step 'Summary'
    $written = @()
    if ($step0Wrote) { $written += ($step0Wrote + ' (written by step0_pc_tests.ps1)') }
    if ($tierOut -and ($rc -eq 0 -or $rc -eq 1) -and [System.IO.File]::Exists($tierOut)) { $written += ((Show-Path $tierOut) + ' (derived tier file)') }
    if ($rc -eq 0) { End-Step 'ok (valid; nothing needs a human)' }
    elseif ($rc -eq 1) { End-Step 'valid, but a finding needs a human (see FINDING lines above)' }
    elseif ($rc -eq 2) { End-Step 'the checker refused the report (invalid or identifying data); no tier file was written' }
    else { End-Step ('the checker could not finish (exit ' + $rc + ')') }
    if ($written.Count -gt 0) { Say ('files written: ' + ($written -join '; ')) } else { Say 'files written: none' }
    return $rc
}

# ------------------------------------------------------------------ close: file-system helpers (all read-only)
function Test-LinkInfo($fsi) {
    return ([int]($fsi.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Get-Kids([string]$dir) {
    try {
        $di = New-Object System.IO.DirectoryInfo($dir)
        return , @($di.GetFileSystemInfos())
    } catch {
        [void]$script:Unreadable.Add($dir)
        return , @()
    }
}

function Test-NeverName([string]$name) {
    foreach ($n in $script:NeverNames) { if ([string]::Equals($n, $name, [System.StringComparison]::OrdinalIgnoreCase)) { return $true } }
    return $false
}

function Test-NeverPath([string]$full) {
    foreach ($p in $script:NeverPaths) { if (Test-SameOrInside $full $p) { return $true } }
    return $false
}

function Test-IsGitFolder([string]$dir) {
    $g = [System.IO.Path]::Combine($dir, '.git')
    return ([System.IO.Directory]::Exists($g) -or [System.IO.File]::Exists($g))
}

function Test-ToolsTarget([string]$name) {
    foreach ($n in $script:ToolsFolderNames) {
        if ($n.Contains('*') -or $n.Contains('?')) {
            $rx = '^' + [regex]::Escape($n).Replace('\*', '.*').Replace('\?', '.') + '$'
            if ([regex]::IsMatch($name, $rx, 'IgnoreCase')) { return $n }
        } elseif ([string]::Equals($n, $name, [System.StringComparison]::OrdinalIgnoreCase)) { return $n }
    }
    return $null
}

function Show-Item([string]$full) {
    if (Test-Inside $full $script:Root) { return ('<root>' + $script:Sep + $full.Substring((Trim-Sep $script:Root).Length + 1)) }
    if (Test-SamePath $full $script:Root) { return '<root>' }
    return (Show-Path $full)
}

function Add-LinkSkip([string]$full) {
    $shown = Show-Item $full
    if (-not $script:LinkSeen.ContainsKey($full)) {
        $script:LinkSeen[$full] = $true
        [void]$script:Links.Add($shown)
    }
}

function Add-Never([string]$full, [string]$why) {
    [void]$script:NeverFound.Add(@{ shown = (Show-Item $full); why = $why })
}

function Measure-Tree([string]$dir) {
    # counts what is inside a folder without following links; reports a protected name or a link if found
    $r = @{ files = 0; folders = 0; bytes = [long]0; links = 0; protectedHit = ''; unreadable = 0 }
    $stack = New-Object System.Collections.Stack
    $stack.Push($dir)
    while ($stack.Count -gt 0) {
        if ($script:Visited -ge $script:MaxEntries) { $script:Incomplete = $true; break }
        $d = [string]$stack.Pop()
        $before = $script:Unreadable.Count
        $kids = Get-Kids $d
        if ($script:Unreadable.Count -gt $before) { $r.unreadable++ }
        foreach ($k in $kids) {
            $script:Visited++
            if (Test-LinkInfo $k) { $r.links++; Add-LinkSkip $k.FullName; continue }
            if ($k -is [System.IO.DirectoryInfo]) {
                if (Test-NeverName $k.Name) { if (-not $r.protectedHit) { $r.protectedHit = $k.Name }; continue }
                if ($k.Name -eq '.git') { if (-not $r.protectedHit) { $r.protectedHit = '.git' }; continue }
                $r.folders++
                $stack.Push($k.FullName)
            } else {
                $r.files++
                try { $r.bytes += [long]$k.Length } catch { }
            }
        }
    }
    return $r
}

function Measure-Candidate([string]$what, [string]$full, [string]$app) {
    # classify one path that is a candidate for removal and measure it (read-only)
    $shown = Show-Item $full
    $rec = [pscustomobject]@{ what = $what; app = $app; full = $full; shown = $shown; files = 0; folders = 0; bytes = [long]0
        state = 'WOULD REMOVE'; why = ''; isDir = $false }
    $fi = $null
    if ([System.IO.Directory]::Exists($full)) { $fi = New-Object System.IO.DirectoryInfo($full) }
    elseif ([System.IO.File]::Exists($full)) { $fi = New-Object System.IO.FileInfo($full) }
    else {
        # a broken link is neither a file nor a folder to .NET; look at the parent listing
        $parent = [System.IO.Path]::GetDirectoryName($full)
        $leaf = [System.IO.Path]::GetFileName($full)
        if ($parent -and [System.IO.Directory]::Exists($parent)) {
            foreach ($k in (Get-Kids $parent)) { if ([string]::Equals($k.Name, $leaf, $script:PathCmp)) { $fi = $k } }
        }
    }
    if ($null -eq $fi) { $rec.state = 'NOT PRESENT'; $rec.why = 'nothing there'; return $rec }
    if (Test-LinkInfo $fi) { Add-LinkSkip $full; $rec.state = 'SKIPPED (link)'; $rec.why = 'a link is never followed'; return $rec }
    if ($fi -is [System.IO.DirectoryInfo]) {
        $rec.isDir = $true
        $m = Measure-Tree $full
        $rec.files = $m.files; $rec.folders = $m.folders; $rec.bytes = $m.bytes
        if ($m.links -gt 0) { $rec.state = 'HELD'; $rec.why = ('contains ' + $m.links + ' link(s), which are never followed') }
        elseif ($m.protectedHit) { $rec.state = 'HELD'; $rec.why = ("contains a protected item named '" + $m.protectedHit + "'") }
        elseif ($m.unreadable -gt 0) { $rec.state = 'HELD'; $rec.why = 'part of it could not be read' }
    } else {
        $rec.files = 1
        try { $rec.bytes = [long]$fi.Length } catch { }
    }
    return $rec
}

# ------------------------------------------------------------------ close: per-app entries
function Resolve-AppEntry([string]$app, [string]$listName, [string]$entry) {
    # returns a list of records (possibly one NOT PRESENT or REFUSED record) for one config entry
    $recs = New-Object System.Collections.ArrayList
    $what = $app + '/' + $listName
    $refuse = {
        param([string]$why)
        return [pscustomobject]@{ what = $what; app = $app; full = ''; shown = $entry; files = 0; folders = 0; bytes = [long]0; state = 'REFUSED'; why = $why; isDir = $false }
    }
    $ex = Expand-EnvText $entry
    if ($ex.unset) {
        [void]$recs.Add([pscustomobject]@{ what = $what; app = $app; full = ''; shown = $entry; files = 0; folders = 0; bytes = [long]0; state = 'SKIPPED'; why = ('the variable %' + $ex.unset + '% is not set here'); isDir = $false })
        return , $recs
    }
    $text = Convert-Sep $ex.text
    if (-not [System.IO.Path]::IsPathRooted($text)) { $text = [System.IO.Path]::Combine($script:ToolsRoot, $text) }
    foreach ($seg in $text.Split([char[]]@('\', '/'))) {
        if ($seg -eq '..') {
            [void]$recs.Add((& $refuse "'..' is not allowed in a path"))
            return , $recs
        }
    }
    # which allowed base does the text start with?
    $bases = New-Object System.Collections.ArrayList
    [void]$bases.Add($script:ToolsRoot)
    foreach ($v in @('APPDATA', 'LOCALAPPDATA')) {
        $val = [Environment]::GetEnvironmentVariable($v)
        if ($val -and [System.IO.Directory]::Exists($val)) { [void]$bases.Add([System.IO.Path]::GetFullPath((Convert-Sep $val))) }
    }
    $base = ''
    foreach ($b in $bases) {
        $bt = (Trim-Sep $b) + $script:Sep
        if ($text.StartsWith($bt, $script:PathCmp) -and $bt.Length -gt $base.Length) { $base = $bt }
    }
    if (-not $base) {
        [void]$recs.Add((& $refuse 'outside the tools folder and the app-data folders'))
        return , $recs
    }
    $segs = @($text.Substring($base.Length).Split([char[]]@('\', '/')) | Where-Object { $_ -ne '' -and $_ -ne '.' })
    if ($segs.Count -eq 0) {
        [void]$recs.Add((& $refuse 'it names a whole base folder'))
        return , $recs
    }
    $hasApp = $false
    foreach ($s in $segs) { if ($s.IndexOf($app, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) { $hasApp = $true } }
    if (-not $hasApp) {
        [void]$recs.Add((& $refuse ("no folder in the path contains the app name '" + $app + "'")))
        return , $recs
    }
    foreach ($s in $segs) {
        if (Test-NeverName $s) { [void]$recs.Add((& $refuse ("'" + $s + "' is a protected folder name"))); return , $recs }
    }
    # walk segment by segment below the base (no GetFullPath on text that may hold wildcards)
    $cur = New-Object System.Collections.ArrayList
    [void]$cur.Add((Trim-Sep $base))
    $blocked = $false
    foreach ($s in $segs) {
        $next = New-Object System.Collections.ArrayList
        foreach ($c in $cur) {
            if ($s.Contains('*') -or $s.Contains('?')) {
                $rx = '^' + [regex]::Escape($s).Replace('\*', '.*').Replace('\?', '.') + '$'
                foreach ($k in (Get-Kids $c)) {
                    if ([regex]::IsMatch($k.Name, $rx, 'IgnoreCase')) {
                        if (Test-LinkInfo $k) { Add-LinkSkip $k.FullName; $blocked = $true; continue }
                        [void]$next.Add($k.FullName)
                    }
                }
            } else {
                foreach ($k in (Get-Kids $c)) {
                    if ([string]::Equals($k.Name, $s, $script:PathCmp)) {
                        if (Test-LinkInfo $k) { Add-LinkSkip $k.FullName; $blocked = $true } else { [void]$next.Add($k.FullName) }
                    }
                }
            }
        }
        $cur = $next
    }
    if ($cur.Count -eq 0) {
        if ($blocked) {
            [void]$recs.Add([pscustomobject]@{ what = $what; app = $app; full = ''; shown = (Show-Path $text); files = 0; folders = 0; bytes = [long]0; state = 'SKIPPED (link)'; why = 'a link on the way is never followed'; isDir = $false })
        } else {
            [void]$recs.Add([pscustomobject]@{ what = $what; app = $app; full = ''; shown = (Show-Path $text); files = 0; folders = 0; bytes = [long]0; state = 'NOT PRESENT'; why = 'nothing there'; isDir = $false })
        }
        return , $recs
    }
    foreach ($c in $cur) {
        if (Test-SameOrInside $c $script:RepoRoot) { [void]$recs.Add((& $refuse 'inside the project repository')); continue }
        [void]$recs.Add((Measure-Candidate $what $c $app))
    }
    return , $recs
}

# ------------------------------------------------------------------ close
function Invoke-Close($opt) {
    $repo = Split-Path -Parent $PSScriptRoot
    $script:RepoRoot = $repo
    $script:StepNo = 0
    $script:StepTotal = 8
    $script:Unreadable = New-Object System.Collections.ArrayList
    $script:Links = New-Object System.Collections.ArrayList
    $script:LinkSeen = @{}
    $script:NeverFound = New-Object System.Collections.ArrayList
    $script:Visited = 0
    $script:Incomplete = $false
    $script:UnsetVar = ''
    Say 'lj close (v0): DRY RUN. Nothing will be removed, committed, pushed or written.'

    # 1. config
    Begin-Step 'Reading the config'
    $cfgArg = ''
    if ($opt.ContainsKey('config')) { $cfgArg = [string]$opt['config'] }
    else { $cfgArg = [System.IO.Path]::Combine($PSScriptRoot, 'lj.config.local.json') }
    $cfgPath = Get-FullPath $cfgArg (Get-CurrentDir)
    if (-not [System.IO.File]::Exists($cfgPath)) {
        End-Step 'failed'
        Say 'REFUSED: no config file. Copy win\lj.config.example.json to win\lj.config.local.json, set "root", and run again (or pass -Config PATH). Nothing was done.'
        Say 'files written: none'
        return 2
    }
    $cfg = $null
    try {
        $fi = New-Object System.IO.FileInfo($cfgPath)
        if ($fi.Length -gt 1048576) { throw 'config file is over 1 MB' }
        $cfg = [System.IO.File]::ReadAllText($cfgPath) | ConvertFrom-Json
    } catch {
        End-Step 'failed'
        Say ('REFUSED: the config could not be read as JSON (' + (Clean-Message $_.Exception.Message) + '). Nothing was done.')
        Say 'files written: none'
        return 2
    }
    if ($null -eq $cfg -or [string]$cfg.schema -ne 'lj-config/1') {
        End-Step 'failed'
        Say 'REFUSED: the config must have "schema": "lj-config/1". Nothing was done.'
        Say 'files written: none'
        return 2
    }
    $known = @('schema', 'root', 'tools_root', 'work_folder_names', 'never_touch_names', 'never_touch_paths', 'extra_tools_folder_names', 'apps')
    $unknownKeys = @()
    foreach ($p in $cfg.PSObject.Properties) {
        if ($known -notcontains $p.Name -and -not $p.Name.StartsWith('_')) { $unknownKeys += $p.Name }
    }
    End-Step 'ok'
    foreach ($u in $unknownKeys) { Say ("      NOTE: config key '" + $u + "' is not used by v0 and was ignored") }

    # 2. root validation (refuse, exit 2, before any walk)
    Begin-Step 'Checking the root folder is a safe place to look'
    $cfgDir = [System.IO.Path]::GetDirectoryName($cfgPath)
    $rootRaw = ''
    if ($null -ne $cfg.root) { $rootRaw = ([string]$cfg.root).Trim() }
    $refuseRoot = {
        param([string]$why)
        End-Step 'REFUSED'
        Say ('REFUSED: ' + $why + ' Nothing was done.')
        Say 'files written: none'
    }
    if (-not $rootRaw) { & $refuseRoot 'the config has no "root".'; return 2 }
    $rootEx = Expand-EnvText $rootRaw
    if ($rootEx.unset) { & $refuseRoot ('the root uses the variable %' + $rootEx.unset + '%, which is not set.'); return 2 }
    if ($rootEx.text -match '^[A-Za-z]:$') { & $refuseRoot 'the root is a bare drive letter.'; return 2 }
    $rootFull = ''
    try { $rootFull = Get-FullPath $rootEx.text $cfgDir } catch { & $refuseRoot 'the root is not a valid path.'; return 2 }
    $rootNorm = Trim-Sep $rootFull
    $driveRoot = [System.IO.Path]::GetPathRoot($rootFull)
    if ($rootNorm -eq '' -or (Test-SamePath $rootFull $driveRoot)) { & $refuseRoot ('the root is a drive root (' + (Show-Path $rootFull) + ').'); return 2 }
    $script:Root = $rootNorm
    if (Test-SamePath $script:Root $repo) { & $refuseRoot 'the root is the project repository folder.'; return 2 }
    if (Test-Inside $script:Root $repo) { & $refuseRoot 'the root is inside the project repository folder; the repository is never touched.'; return 2 }
    $profiles = @()
    foreach ($pr in @($env:USERPROFILE, $HOME, [Environment]::GetFolderPath('UserProfile'))) {
        if ($pr) { $profiles += (Trim-Sep ([System.IO.Path]::GetFullPath((Convert-Sep $pr)))) }
    }
    foreach ($pr in $profiles) {
        if (Test-SamePath $script:Root $pr) { & $refuseRoot 'the root is the user profile folder.'; return 2 }
        if (Test-Inside $pr $script:Root) { & $refuseRoot 'the root contains the user profile folder.'; return 2 }
    }
    foreach ($sv in @($env:windir, $env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:ProgramData)) {
        if ($sv -and (Test-SameOrInside $script:Root (Trim-Sep ([System.IO.Path]::GetFullPath((Convert-Sep $sv)))))) { & $refuseRoot 'the root is a Windows system folder.'; return 2 }
    }
    if (-not [System.IO.Directory]::Exists($script:Root)) { & $refuseRoot ('the root folder does not exist (' + (Show-Path $script:Root) + ').'); return 2 }
    $rootInfo = New-Object System.IO.DirectoryInfo($script:Root)
    if (Test-LinkInfo $rootInfo) { & $refuseRoot 'the root is a link; point "root" at the real folder.'; return 2 }
    if (Test-IsGitFolder $script:Root) { & $refuseRoot 'the root is itself a git repository.'; return 2 }
    $toolsRaw = 'tools'
    if ($null -ne $cfg.tools_root -and ([string]$cfg.tools_root).Trim() -ne '') { $toolsRaw = ([string]$cfg.tools_root).Trim() }
    $toolsEx = Expand-EnvText $toolsRaw
    if ($toolsEx.unset) { & $refuseRoot ('tools_root uses the variable %' + $toolsEx.unset + '%, which is not set.'); return 2 }
    try { $script:ToolsRoot = Trim-Sep (Get-FullPath $toolsEx.text $script:Root) } catch { & $refuseRoot 'tools_root is not a valid path.'; return 2 }
    if (-not (Test-Inside $script:ToolsRoot $script:Root)) { & $refuseRoot 'tools_root must be a folder inside the root.'; return 2 }
    End-Step 'ok'
    Say ('      root:       ' + (Show-Path $script:Root))
    Say ('      tools root: ' + (Show-Item $script:ToolsRoot))

    # built-in protections (the config can only add to them)
    $script:NeverNames = New-Object System.Collections.ArrayList
    foreach ($n in @('media', 'archive', 'masters', 'originals')) { [void]$script:NeverNames.Add($n) }
    foreach ($n in (To-List $cfg.never_touch_names)) { if ($n -notmatch '[\\/*?]') { [void]$script:NeverNames.Add($n) } }
    $script:NeverPaths = New-Object System.Collections.ArrayList
    foreach ($n in (To-List $cfg.never_touch_paths)) {
        $e = Expand-EnvText $n
        if ($e.unset) { continue }
        try { [void]$script:NeverPaths.Add((Trim-Sep (Get-FullPath $e.text $script:Root))) } catch { }
    }
    $script:WorkNames = New-Object System.Collections.ArrayList
    $wn = To-List $cfg.work_folder_names
    if ($wn.Count -eq 0) { [void]$script:WorkNames.Add('work') } else { foreach ($n in $wn) { [void]$script:WorkNames.Add($n) } }
    $script:ToolsFolderNames = New-Object System.Collections.ArrayList
    foreach ($n in @('Recovery', 'Auto-Save', 'cache')) { [void]$script:ToolsFolderNames.Add($n) }
    foreach ($n in (To-List $cfg.extra_tools_folder_names)) { if ($n -notmatch '[\\/]') { [void]$script:ToolsFolderNames.Add($n) } }

    # 3. the walk
    Begin-Step 'Walking the root, read-only (links are listed and never followed)'
    $items = New-Object System.Collections.ArrayList
    $stack = New-Object System.Collections.Stack
    $stack.Push(@($script:Root, $false, $false))
    while ($stack.Count -gt 0) {
        if ($script:Visited -ge $script:MaxEntries) { $script:Incomplete = $true; break }
        $cur = $stack.Pop()
        $dir = [string]$cur[0]
        $inWork = [bool]$cur[1]
        $inTools = [bool]$cur[2]
        foreach ($k in (Get-Kids $dir)) {
            $script:Visited++
            if (Test-LinkInfo $k) { Add-LinkSkip $k.FullName; continue }
            if ($k -is [System.IO.DirectoryInfo]) {
                $full = $k.FullName
                if (Test-NeverName $k.Name) { Add-Never $full 'protected folder name'; continue }
                if (Test-NeverPath $full) { Add-Never $full 'listed in never_touch_paths'; continue }
                if (Test-SamePath $full $repo) { Add-Never $full 'the project repository'; continue }
                if (Test-IsGitFolder $full) { Add-Never $full 'another git repository'; continue }
                $kTools = ($inTools -or (Test-SamePath $full $script:ToolsRoot))
                $kWork = $inWork
                foreach ($w in $script:WorkNames) { if ([string]::Equals($w, $k.Name, [System.StringComparison]::OrdinalIgnoreCase)) { $kWork = $true } }
                if ($kTools) {
                    $hit = $null
                    if (-not (Test-SamePath $full $script:ToolsRoot)) { $hit = Test-ToolsTarget $k.Name }
                    if ($hit) { [void]$items.Add((Measure-Candidate $k.Name $full '')); continue }
                }
                $stack.Push(@($full, $kWork, $kTools))
            } else {
                $ext = [System.IO.Path]::GetExtension($k.Name).ToLower()
                if ($inWork -and $ext -eq '.xmp') {
                    $rec = [pscustomobject]@{ what = 'xmp'; app = ''; full = $k.FullName; shown = (Show-Item $k.FullName); files = 1; folders = 0; bytes = [long]0; state = 'WOULD REMOVE'; why = ''; isDir = $false }
                    try { $rec.bytes = [long]$k.Length } catch { }
                    [void]$items.Add($rec)
                } elseif ($ext -eq '.hc' -or $ext -eq '.tc') {
                    Add-Never $k.FullName 'possible encrypted container file'
                }
            }
        }
    }
    if ($script:Incomplete) { End-Step ('STOPPED at the limit of ' + $script:MaxEntries + ' entries; the list is INCOMPLETE') }
    else { End-Step ('ok (' + $script:Visited + ' entries looked at)') }

    # 4. per-app lists
    Begin-Step 'Reading the per-app lists (recent-file lists and caches)'
    $appSummary = New-Object System.Collections.ArrayList
    $entryCount = 0
    if ($null -ne $cfg.apps) {
        foreach ($ap in $cfg.apps.PSObject.Properties) {
            $appName = $ap.Name.ToLower()
            $a = $ap.Value
            $nRecent = 0; $nCache = 0
            foreach ($ln in @('recent_files', 'cache')) {
                $entries = To-List $a.$ln
                if ($ln -eq 'recent_files') { $nRecent = $entries.Count } else { $nCache = $entries.Count }
                foreach ($e in $entries) {
                    $entryCount++
                    foreach ($r in (Resolve-AppEntry $appName $ln $e)) { [void]$items.Add($r) }
                }
            }
            $st = 'UNVERIFIED'
            if ($null -ne $a.status -and ([string]$a.status).Trim().ToUpper() -eq 'FROM_PASTE') { $st = 'FROM_PASTE' }
            $note = ''
            if ($null -ne $a.note) { $note = [string]$a.note }
            [void]$appSummary.Add(@{ name = $appName; recent = $nRecent; cache = $nCache; status = $st; note = $note })
        }
    }
    End-Step ('ok (' + $entryCount + ' entries in ' + $appSummary.Count + ' app list(s))')

    # 5. settle the list: nothing is counted twice, then number it
    Begin-Step 'Settling the list and counting sizes'
    $sorted = @($items | Sort-Object -Property @{ Expression = { $_.full.Length } }, @{ Expression = { if ($_.app) { 1 } else { 0 } } })
    $removeDirs = New-Object System.Collections.ArrayList
    $would = New-Object System.Collections.ArrayList
    $other = New-Object System.Collections.ArrayList
    foreach ($it in $sorted) {
        if ($it.state -eq 'WOULD REMOVE') {
            $coveredBy = ''
            foreach ($rd in $removeDirs) { if (Test-SameOrInside $it.full $rd.full) { $coveredBy = $rd.shown; break } }
            if ($coveredBy) { $it.state = 'ALREADY LISTED'; $it.why = ('already counted above, inside or the same as ' + $coveredBy); [void]$other.Add($it); continue }
            [void]$would.Add($it)
            if ($it.isDir) { [void]$removeDirs.Add($it) }
        } else { [void]$other.Add($it) }
    }
    $would = @($would | Sort-Object -Property @{ Expression = { $_.shown.ToLower() } })
    $totFiles = 0; $totBytes = [long]0; $totFolders = 0
    foreach ($w in $would) { $totFiles += $w.files; $totFolders += $w.folders; $totBytes += $w.bytes }
    End-Step ('ok (' + $would.Count + ' item(s))')

    # ---------------- the report
    Say ''
    Say 'WOULD REMOVE (v0 removes nothing; this is only the list)'
    if ($would.Count -eq 0) {
        Say '  nothing: no sidecar, Recovery, Auto-Save or cache item was found under this root.'
    } else {
        Say ('  {0,3}  {1,-28} {2,7}  {3,10}  {4}' -f '#', 'what', 'files', 'size', 'where')
        $n = 0
        foreach ($w in $would) {
            $n++
            $what = $w.what
            if ($w.isDir) { $what = $what + ' (folder)' }
            Say ('  {0,3}  {1,-28} {2,7}  {3,10}  {4}' -f $n, $what, $w.files, (Format-Size $w.bytes), $w.shown)
        }
        Say ('  TOTAL: ' + $would.Count + ' item(s), ' + $totFiles + ' file(s), ' + (Format-Size $totBytes))
        Say '  A folder is one line: its files are counted, not listed by name.'
    }

    $held = @($other | Where-Object { $_.state -eq 'HELD' -or $_.state -eq 'REFUSED' })
    Say ''
    Say 'HELD BACK (listed, but not on the list above; v1 will not remove these without a human)'
    if ($held.Count -eq 0) { Say '  none' }
    foreach ($h in $held) { Say ('  - [' + $h.state + '] ' + $h.what + ': ' + $h.shown + ' - ' + $h.why) }

    $notes = @($other | Where-Object { $_.state -eq 'NOT PRESENT' -or $_.state -eq 'SKIPPED' -or $_.state -eq 'ALREADY LISTED' })
    Say ''
    Say 'NOT ON THE LIST (nothing to remove, or already counted above)'
    if ($notes.Count -eq 0) { Say '  none' }
    foreach ($h in $notes) { Say ('  - [' + $h.state + '] ' + $h.what + ': ' + $h.shown + ' - ' + $h.why) }

    Say ''
    Say 'SKIPPED (link): links are never followed and never listed as removable'
    if ($script:Links.Count -eq 0) { Say '  none' }
    foreach ($l in @($script:Links | Sort-Object)) { Say ('  - SKIPPED (link) ' + $l) }

    Say ''
    Say 'NEVER TOUCHED'
    Say '  by rule: anything under a folder named media, archive, masters or originals (plus any names you add in the config);'
    Say '           the project repository and any other git repository; any mounted encrypted container; any drive root;'
    Say '           anything outside the root. These folders are not even opened, so their file names are not shown.'
    if ($script:NeverFound.Count -eq 0) { Say '  found under this root: none' }
    else {
        Say '  found under this root:'
        foreach ($nf in @($script:NeverFound | Sort-Object -Property @{ Expression = { $_.shown.ToLower() } })) { Say ('  - ' + $nf.shown + '  (' + $nf.why + ')') }
    }
    Say '  mounted containers: v0 cannot detect a mounted container (UNVERIFIED); list its mount folder under never_touch_paths in the config.'

    Say ''
    Say 'PER-APP LISTS (recent-file lists and caches of the Craft apps)'
    if ($appSummary.Count -eq 0) { Say '  no apps in the config. UNVERIFIED.' }
    foreach ($s in $appSummary) {
        $flag = $s.status
        if ($s.recent -eq 0 -and $s.cache -eq 0) { $flag = 'UNVERIFIED, no entries yet' }
        Say ('  ' + $s.name.PadRight(12) + ' recent_files: ' + $s.recent + '   cache: ' + $s.cache + '   [' + $flag + ']')
        if ($s.note) { Say ('      note: ' + $s.note) }
    }
    Say '  These lists are filled from the where-did-it-write output you paste after the five-minute tests. Until then they stay UNVERIFIED.'

    if ($script:Unreadable.Count -gt 0) {
        Say ''
        Say ('COULD NOT READ: ' + $script:Unreadable.Count + ' folder(s), so the list may be incomplete.')
        foreach ($u in @($script:Unreadable | Select-Object -First 10)) { Say ('  - ' + (Show-Item $u)) }
    }

    # ---------------- read-only repo checks
    Say ''
    Say 'CHECKS (read-only)'
    $checkRc = @{}
    $skipChecks = $opt.ContainsKey('skipchecks')
    if ($skipChecks) {
        foreach ($t in @('Looking for Python', 'stale_check.py --new-only', 'public_lint.py')) {
            Begin-Step $t; End-Step 'SKIPPED (you passed -SkipChecks)'
        }
    } else {
        Begin-Step 'Looking for Python (py -3 -I, or python -I)'
        $py = Find-Python
        if (-not $py) {
            End-Step 'not found'
            Begin-Step 'stale_check.py --new-only'; End-Step 'SKIPPED (no Python)'
            Begin-Step 'public_lint.py'; End-Step 'SKIPPED (no Python)'
        } else {
            End-Step ('ok (' + $py.shown + ')')
            $oldLocks = $env:GIT_OPTIONAL_LOCKS
            $env:GIT_OPTIONAL_LOCKS = '0'
            try {
                $sc = [System.IO.Path]::Combine([System.IO.Path]::Combine($repo, 'scripts'), 'stale_check.py')
                $pl = [System.IO.Path]::Combine([System.IO.Path]::Combine($repo, 'scripts'), 'public_lint.py')
                Begin-Step 'stale_check.py --new-only (read-only)'
                if (-not [System.IO.File]::Exists($sc)) { End-Step 'SKIPPED (scripts\stale_check.py not found)' }
                else {
                    $r = Invoke-Py $py @($sc, '--root', $repo, '--new-only')
                    $checkRc['stale_check'] = $r.rc
                    End-Step ('exit ' + $r.rc)
                    foreach ($ln in @($r.lines | Select-Object -First 12)) { Say ('      ' + $ln) }
                    if ($r.lines.Count -gt 12) { Say ('      ... ' + ($r.lines.Count - 12) + ' more line(s) not shown') }
                }
                Begin-Step 'public_lint.py (read-only; findings are masked)'
                if (-not [System.IO.File]::Exists($pl)) { End-Step 'SKIPPED (scripts\public_lint.py not found)' }
                else {
                    $r = Invoke-Py $py @($pl, '--root', $repo)
                    $checkRc['public_lint'] = $r.rc
                    End-Step ('exit ' + $r.rc)
                    $shownLines = @($r.lines | Select-Object -First 10)
                    foreach ($ln in $shownLines) { Say ('      ' + $ln) }
                    if ($r.lines.Count -gt 10) {
                        Say ('      ... ' + ($r.lines.Count - 10) + ' more line(s) not shown; last line:')
                        Say ('      ' + $r.lines[$r.lines.Count - 1])
                    }
                }
            } finally {
                [Environment]::SetEnvironmentVariable('GIT_OPTIONAL_LOCKS', $oldLocks)
            }
        }
    }
    if ($checkRc.Count -gt 0) {
        $parts = @()
        foreach ($key in @($checkRc.Keys | Sort-Object)) { $parts += ($key + '=' + $checkRc[$key]) }
        Say ('  check results: ' + ($parts -join ', ') + ' (0 = clean). In v0 they are advice and do not change the exit code of close.')
    }

    Say ''
    Say 'BACKUP: not implemented in v0 (week 4)'
    Say ''
    Say 'REMINDERS'
    Say '  - Dismount the encrypted container (VeraCrypt) when you are finished.'
    Say '  - Close the Craft apps (and turn their control ports off).'
    Say '  - Nothing was removed. Clear recent-file lists and Recovery items by hand until v1 exists.'
    Say ''
    Say 'files written: none'
    Say 'Nothing was removed, moved, committed, pushed or written. (v0 is a dry run.)'
    if ($script:Incomplete -or $script:Unreadable.Count -gt 0) { return 1 }
    return 0
}

# ------------------------------------------------------------------ main: read the command line by hand
$tokens = @()
foreach ($a in $args) { $tokens += [string]$a }

if (-not $PSScriptRoot) {
    Say 'REFUSED: run this as a file (powershell.exe -File .\win\lj.ps1 ...), not pasted into a window. Nothing was done.'
    exit 2
}

function Get-OptionName([string]$tok) {
    $t = $tok.TrimStart([char[]]@('-'))
    $i = $t.IndexOfAny([char[]]@(':', '='))
    if ($i -ge 0) { $t = $t.Substring(0, $i) }
    return $t.ToLower()
}

# 1. switches that do not exist in v0: answer first, whatever else was typed
$notInV0 = @{ 'apply' = '-Apply'; 'commit' = '-Commit'; 'includewindowsrecent' = '-IncludeWindowsRecent' }
foreach ($t in $tokens) {
    if ($t.StartsWith('-')) {
        $n = Get-OptionName $t
        foreach ($f in @('apply', 'commit', 'includewindowsrecent')) {
            if ($n.Length -ge 3 -and $f.StartsWith($n)) {
                Say ($notInV0[$f] + ': not in v0: planned for v1 in week 4; nothing was done')
                Say 'files written: none'
                exit 2
            }
        }
    }
}

# 2. the command
if ($tokens.Count -eq 0) { Show-Help; exit 0 }
$command = $tokens[0].ToLower()
if ($command.StartsWith('-')) {
    $hn = Get-OptionName $command
    if ($hn -eq 'h' -or $hn -eq 'help' -or $hn -eq '?') { Show-Help; exit 0 }
    Say ("Unknown option '" + $tokens[0] + "'. Nothing was done. Try: lj.ps1 help")
    exit 2
}
if ($command -ne 'doctor' -and $command -ne 'close' -and $command -ne 'help') {
    Say ("Unknown command '" + $tokens[0] + "'. Nothing was done. Try: lj.ps1 help")
    exit 2
}

# 3. the options of that command
$valueOpts = @()
$flagOpts = @()
if ($command -eq 'doctor') { $valueOpts = @('fromreport', 'savetier') }
if ($command -eq 'close') { $valueOpts = @('config'); $flagOpts = @('skipchecks') }
$opt = @{}
$i = 1
while ($i -lt $tokens.Count) {
    $t = $tokens[$i]
    if (-not $t.StartsWith('-')) {
        Say ("Unexpected argument '" + $t + "'. Nothing was done. Try: lj.ps1 help")
        exit 2
    }
    $n = Get-OptionName $t
    $inline = $null
    $cut = $t.TrimStart([char[]]@('-')).IndexOfAny([char[]]@(':', '='))
    if ($cut -ge 0) { $inline = $t.TrimStart([char[]]@('-')).Substring($cut + 1) }
    if ($valueOpts -contains $n) {
        if ($null -ne $inline -and $inline -ne '') { $opt[$n] = $inline; $i++ }
        elseif ($i + 1 -lt $tokens.Count -and -not $tokens[$i + 1].StartsWith('-')) { $opt[$n] = $tokens[$i + 1]; $i += 2 }
        else { Say ("The option '" + $t + "' needs a value. Nothing was done. Try: lj.ps1 help"); exit 2 }
    } elseif ($flagOpts -contains $n) {
        $opt[$n] = $true; $i++
    } else {
        Say ("Unknown option '" + $t + "' for " + $command + ". Nothing was done. Try: lj.ps1 help")
        exit 2
    }
}

if ($command -eq 'help') { Show-Help; exit 0 }
$result = @()
if ($command -eq 'doctor') { $result = @(Invoke-Doctor $opt) }
if ($command -eq 'close') { $result = @(Invoke-Close $opt) }
if ($result.Count -eq 0) { exit 2 }
if ($result.Count -gt 1) { Say 'NOTE: internal: a function printed unexpected output (ignored)' }
exit ([int]$result[$result.Count - 1])
