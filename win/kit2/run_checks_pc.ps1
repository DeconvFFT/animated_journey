<#
.SYNOPSIS
  Life Journey PC colour and spec check (WP-09, kit B). Runs two project tools on THIS PC's ffmpeg and writes ONE small file to
  your temporary folder. Never touches your photos, documents or settings.

.DESCRIPTION
  1. makes a 3-second test clip with this PC's ffmpeg (a built-in test picture and a quiet tone; nothing of yours is read),
  2. checks that clip against the online delivery profile with pipeline\validators\spec_check.py,
  3. runs pipeline\validators\colour_patch.py --all with this PC's ffmpeg: it encodes a three-patch test picture through every
     project encode chain (and the two phone chains, if the phone file is present) and reads the PIXELS back (W-16),
  4. scans the result against scripts\redaction_patterns.json (the project's one list of "identifying data" patterns) and your own
     user, computer and domain names, which it reads from the system at that moment and never stores,
  5. only if the scan is clean, writes the raw record to %TEMP%\colour_patch_pc.json and prints a short block to paste.

  The raw file holds the ffmpeg version line, the build's configure flags, the binary's SHA-256 and the chain results. YOU READ IT
  (open it in Notepad) AND PASTE IT IN THE CHAT. It is not saved in the project folder, not committed and not filed: the project
  keeps only a derived form (version, SHA-256, chain names and numbers), made from your paste.

  If the scan finds something that looks like identifying data it REFUSES: it prints the kind of thing (category), where
  (field) and the first two characters (hit), writes nothing and exits 2. It also refuses to start if the pattern file is missing,
  so download the WHOLE project folder, not single files.

  Works in Windows PowerShell 5.1 and PowerShell 7. Needs no administrator rights. Needs Python 3 (the "py" launcher or python)
  and ffmpeg; it installs nothing and uses no network.

.PARAMETER Out
  Where to write the raw record. Default: %TEMP%\colour_patch_pc.json (printed in that unexpanded form).

.PARAMETER Ffmpeg
  The ffmpeg to test (full path). Default: the ffmpeg found on PATH.

.NOTES
  Exit codes: 0 everything passed and the file was written; 1 a check failed (the file is still written, the numbers matter);
  2 the redaction check refused, the pattern file is missing or invalid, or the options were wrong (nothing written);
  3 an environment problem (Python, ffmpeg or a project file missing, a tool could not run, the file could not be written).
  Run for one session only, without changing system policy:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\run_checks_pc.ps1
  Every claim about Windows behaviour in this script is UNVERIFIED until the maker's first real run.
  The parameters that start with Test or Pattern are for the project's own tests on a different computer; they collect nothing
  from this machine. Pattern engine ported from win\step0_pc_tests.ps1 (WP-01a); the patterns themselves live only in
  scripts\redaction_patterns.json.
#>
[CmdletBinding()]
param(
    [string]$Out = '',
    [string]$Ffmpeg = '',
    [string]$TestFixture = '',
    [string]$FakeUser = '',
    [string]$FakeComputer = '',
    [string]$FakeDomain = '',
    [string]$PatternSelfTest = ''
)

$ErrorActionPreference = 'Continue'
$ScriptVersion = '1.0.0'
$TotalSteps = 11

# Anything unexpected that would otherwise print a red error (which can carry a folder name): say it in scrubbed words, clean up, stop.
trap {
    Write-Host ''
    Write-Host ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    if ($script:WorkDir -and (Test-Path -LiteralPath $script:WorkDir)) { try { [System.IO.Directory]::Delete($script:WorkDir, $true) } catch { } }
    Write-Host 'files written: none'
    exit 3
}
$isWin = ($env:OS -eq 'Windows_NT')
$TestMode = ($TestFixture -ne '') -or ($PatternSelfTest -ne '')
$script:StepNo = 0
$script:FilesWritten = New-Object System.Collections.ArrayList
$script:Pat = $null
$script:WorkDir = ''

# ------------------------------------------------------------------ small helpers
function Say([string]$text) { Write-Host $text }

function Get-Utf8NoBom { return (New-Object System.Text.UTF8Encoding($false)) }

function Read-TextFile([string]$path) {
    # UTF-8 or UTF-8 with BOM or UTF-16 with BOM; the BOM is stripped
    return [System.IO.File]::ReadAllText($path)
}

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

function Mask-Value([string]$value, [int]$keep, [string]$fill, [int]$cap) {
    if ($value.Length -le $keep) { return ($fill * [Math]::Max(1, $value.Length)) }
    $n = [Math]::Min($value.Length - $keep, $cap)
    return ($value.Substring(0, $keep) + ($fill * $n))
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

function Run-Python($py, [string]$script, [string[]]$more, [int]$timeoutSec) {
    return (Invoke-Tool $py.exe (@($py.prefix) + @('-I', $script) + @($more)) $timeoutSec)
}

function Step([string]$label) {
    $script:StepNo++
    Write-Host ("[{0}/{1}] {2} ... " -f $script:StepNo, $TotalSteps, $label) -NoNewline
}

# ------------------------------------------------------------------ the shared pattern file (fail closed)
function Norm-Spec([string]$spec) { return [regex]::Replace($spec, '\[[^\]]*\]', '[]') }
function Norm-Path([string]$path) { return [regex]::Replace($path, '\[[0-9]+\]', '[]') }
function Spec-ToRegex([string]$spec) {
    $e = [regex]::Escape((Norm-Spec $spec))
    $e = $e.Replace('\*', '.*')
    return (New-Object System.Text.RegularExpressions.Regex(('^' + $e + '$')))
}

function Load-Patterns {
    $root = $PSScriptRoot
    if (-not $root) { throw 'run this from the file, not pasted text (the folder it sits in is unknown)' }
    $repo = Split-Path -Parent (Split-Path -Parent $root)
    $path = Join-Path (Join-Path $repo 'scripts') 'redaction_patterns.json'
    if (-not (Test-Path -LiteralPath $path)) { throw 'scripts\redaction_patterns.json is missing (download the WHOLE project folder, not single files)' }
    $data = (Read-TextFile $path) | ConvertFrom-Json
    if (-not $data -or -not $data.categories -or @($data.categories).Count -eq 0) { throw 'scripts\redaction_patterns.json has no categories' }
    $required = @('email', 'ipv4', 'ipv6', 'mac', 'profile_path_windows', 'profile_path_linux', 'token_shape', 'guid_serial', 'handle')
    $have = @($data.categories | ForEach-Object { $_.id })
    foreach ($id in $required) { if ($have -notcontains $id) { throw ('scripts\redaction_patterns.json lacks the category ' + $id) } }

    $pat = @{}
    $pat.Version = $data.version
    $pat.Categories = New-Object System.Collections.ArrayList
    foreach ($c in @($data.categories)) {
        $opt = [System.Text.RegularExpressions.RegexOptions]::None
        if ($c.flags -and ([string]$c.flags).Contains('i')) { $opt = [System.Text.RegularExpressions.RegexOptions]::IgnoreCase }
        $scope = 'both'
        if ($c.scope) { $scope = [string]$c.scope }
        if ($scope -eq 'report' -or $scope -eq 'both') {
            $rx = New-Object System.Text.RegularExpressions.Regex([string]$c.regex, $opt)
            [void]$pat.Categories.Add(@{ id = [string]$c.id; rx = $rx })
        }
    }
    $pat.Exemptions = New-Object System.Collections.ArrayList
    foreach ($e in @($data.exemptions)) {
        if (-not $e) { continue }
        $cats = $null
        foreach ($k in @('category', 'categories', 'applies_to', 'category_id')) { if ($e.$k) { $cats = @($e.$k); break } }
        $opt = [System.Text.RegularExpressions.RegexOptions]::None
        if ($e.flags -and ([string]$e.flags).Contains('i')) { $opt = [System.Text.RegularExpressions.RegexOptions]::IgnoreCase }
        [void]$pat.Exemptions.Add(@{ cats = $cats; rx = (New-Object System.Text.RegularExpressions.Regex([string]$e.regex, $opt)) })
    }
    $pat.FieldExemptions = New-Object System.Collections.ArrayList
    foreach ($fe in @($data.field_exemptions)) {
        if (-not $fe) { continue }
        $cats = $null
        foreach ($k in @('category', 'categories', 'id', 'applies_to')) { if ($fe.$k) { $cats = @($fe.$k); break } }
        $fields = $null
        foreach ($k in @('fields', 'field', 'paths', 'path')) { if ($fe.$k) { $fields = @($fe.$k); break } }
        if (-not $cats -or -not $fields) { throw 'a field_exemptions entry has no category or no fields' }
        $rxs = @()
        foreach ($f in $fields) { $rxs += , (Spec-ToRegex ([string]$f)) }
        [void]$pat.FieldExemptions.Add(@{ cats = $cats; rxs = $rxs })
    }
    $nc = $data.name_checks
    $pat.MinNameLen = 3
    $pat.FragmentLen = 4
    $pat.FragmentMinNameLen = 5
    if ($nc) {
        if ($nc.min_name_len) { $pat.MinNameLen = [int]$nc.min_name_len }
        if ($nc.fragment_len) { $pat.FragmentLen = [int]$nc.fragment_len }
        if ($nc.fragment_min_name_len) { $pat.FragmentMinNameLen = [int]$nc.fragment_min_name_len }
    }
    $pat.Placeholders = @()
    if ($data.placeholders) { $pat.Placeholders = @($data.placeholders | ForEach-Object { [string]$_ }) }
    $pat.MaskKeep = 2
    $pat.MaskFill = '*'
    $pat.MaskCap = 8
    if ($data.mask) {
        if ($data.mask.keep) { $pat.MaskKeep = [int]$data.mask.keep }
        if ($data.mask.fill) { $pat.MaskFill = [string]$data.mask.fill }
        if ($data.mask.cap) { $pat.MaskCap = [int]$data.mask.cap }
    }
    $denyName = 'public_lint.deny.local.txt'
    if ($data.local_deny) {
        $ld = $data.local_deny
        if ($ld -isnot [string]) { if ($ld.path) { $ld = $ld.path } elseif ($ld.file) { $ld = $ld.file } }
        if ($ld -is [string]) { $denyName = Split-Path -Leaf $ld.Replace('\', '/') }
    }
    $pat.DenyPath = Join-Path (Join-Path $repo 'scripts') $denyName
    $pat.Repo = $repo
    return $pat
}

function Test-FieldRx($rxs, [string]$path) {
    $np = Norm-Path $path
    foreach ($rx in $rxs) { if ($rx.IsMatch($np)) { return $true } }
    return $false
}

function Get-Leaves($obj, [string]$path, $sink) {
    # Collects every string leaf of a finished record with its field path. Keys are never searched.
    if ($null -eq $obj) { return }
    if ($obj -is [string]) { [void]$sink.Add(@{ path = $path; text = $obj }); return }
    if ($obj -is [System.Collections.IDictionary]) {
        foreach ($k in @($obj.Keys)) {
            $child = $k
            if ($path) { $child = $path + '.' + $k }
            Get-Leaves $obj[$k] $child $sink
        }
        return
    }
    if ($obj -is [System.Management.Automation.PSCustomObject]) {
        foreach ($prop in $obj.PSObject.Properties) {
            $child = $prop.Name
            if ($path) { $child = $path + '.' + $prop.Name }
            Get-Leaves $prop.Value $child $sink
        }
        return
    }
    if ($obj -is [System.Collections.IEnumerable]) {
        $i = 0
        foreach ($item in $obj) {
            Get-Leaves $item ($path + '[' + $i + ']') $sink
            $i++
        }
    }
}

function Test-Exempt($pat, [string]$cat, [string]$path, [string]$text, $match) {
    foreach ($fe in $pat.FieldExemptions) {
        if ($fe.cats -contains $cat -and (Test-FieldRx $fe.rxs $path)) { return $true }
    }
    foreach ($ex in $pat.Exemptions) {
        if ($ex.cats -and ($ex.cats -notcontains $cat)) { continue }
        foreach ($m in $ex.rx.Matches($text)) {
            if ($m.Index -le $match.Index -and ($match.Index + $match.Length) -le ($m.Index + $m.Length)) { return $true }
        }
    }
    return $false
}

function Find-NameHit([string]$text, [string]$name, [bool]$fragments, $pat) {
    $low = $text.ToLower()
    $nl = $name.ToLower()
    $rx = '(?<![a-z0-9])' + [regex]::Escape($nl) + '(?![a-z0-9])'
    if ([regex]::IsMatch($low, $rx)) { return $name }
    if ($fragments -and $name.Length -ge $pat.FragmentMinNameLen) {
        $n = $pat.FragmentLen
        for ($i = 0; $i -le ($name.Length - $n); $i++) {
            $frag = $nl.Substring($i, $n)
            if ($low.Contains($frag)) { return $name.Substring($i, $n) }
        }
    }
    return $null
}

function Get-NameSources($pat) {
    # Returns a list of @{ cat; value; frag }. Real names are read here, used for the scan, never stored or printed.
    $list = New-Object System.Collections.ArrayList
    $seen = @{}
    $add = {
        param($cat, $val, $frag)
        if ($val -and -not $seen.ContainsKey($cat + '|' + $val.ToLower())) {
            $seen[$cat + '|' + $val.ToLower()] = $true
            [void]$list.Add(@{ cat = $cat; value = [string]$val; frag = $frag })
        }
    }
    if ($TestMode) {
        & $add 'user_name' $FakeUser $true
        & $add 'computer_name' $FakeComputer $true
        & $add 'domain_name' $FakeDomain $true
    } else {
        $profileLeaf = $null
        if ($env:USERPROFILE) { $profileLeaf = Split-Path -Leaf $env:USERPROFILE }
        elseif ($HOME) { $profileLeaf = Split-Path -Leaf $HOME }
        & $add 'user_name' ([Environment]::UserName) $true
        & $add 'user_name' $env:USERNAME $true
        & $add 'user_name' $profileLeaf $true
        & $add 'computer_name' ([Environment]::MachineName) $true
        & $add 'computer_name' $env:COMPUTERNAME $true
        & $add 'domain_name' $env:USERDOMAIN $true
        & $add 'domain_name' $env:USERDNSDOMAIN $true
        if ($pat.DenyPath -and (Test-Path -LiteralPath $pat.DenyPath)) {
            foreach ($line in (Read-TextFile $pat.DenyPath).Split("`n")) {
                $w = $line.Trim()
                if ($w -and -not $w.StartsWith('#')) { & $add 'local_deny' $w $false }
            }
        }
    }
    return $list
}

function Invoke-SelfScan($pat, $record) {
    # Returns @{ refusals; skipped } where each hit is @{ category; field; hit }. A name hit anywhere refuses.
    $leaves = New-Object System.Collections.ArrayList
    Get-Leaves $record '' $leaves
    $names = Get-NameSources $pat
    $usable = New-Object System.Collections.ArrayList
    $skipped = New-Object System.Collections.ArrayList
    foreach ($n in $names) {
        if ($n.value.Length -lt $pat.MinNameLen) { [void]$skipped.Add(@{ category = $n.cat; length = $n.value.Length }) }
        else { [void]$usable.Add($n) }
    }
    $refusals = New-Object System.Collections.ArrayList
    $seen = @{}
    foreach ($leaf in $leaves) {
        foreach ($c in $pat.Categories) {
            foreach ($m in $c.rx.Matches($leaf.text)) {
                if ($pat.Placeholders -contains $m.Value) { continue }
                if (Test-Exempt $pat $c.id $leaf.path $leaf.text $m) { continue }
                $key = $c.id + '|' + $leaf.path + '|' + $m.Value
                if ($seen.ContainsKey($key)) { continue }
                $seen[$key] = $true
                [void]$refusals.Add(@{ category = $c.id; field = $leaf.path; hit = (Mask-Value $m.Value $pat.MaskKeep $pat.MaskFill $pat.MaskCap) })
            }
        }
        foreach ($n in $usable) {
            $matched = Find-NameHit $leaf.text $n.value $n.frag $pat
            if ($null -eq $matched) { continue }
            $key = $n.cat + '|' + $leaf.path
            if ($seen.ContainsKey($key)) { continue }
            $seen[$key] = $true
            [void]$refusals.Add(@{ category = $n.cat; field = $leaf.path; hit = (Mask-Value $matched $pat.MaskKeep $pat.MaskFill $pat.MaskCap) })
        }
    }
    return @{ refusals = $refusals; skipped = $skipped }
}

function Write-ScanOutcome($scan) {
    foreach ($s in $scan.skipped) {
        Say ("NOTE name check skipped for a {0} of {1} character(s): shorter than the minimum, so it would match ordinary words (the pattern checks still ran)" -f $s.category, $s.length)
    }
    if ($scan.refusals.Count -gt 0) {
        Say 'REDACTION CHECK FAILED, nothing was written'
        foreach ($h in $scan.refusals) { Say ("category={0} field={1} hit={2}" -f $h.category, $h.field, $h.hit) }
    }
}

function Resolve-OutPath {
    $shown = ''
    $full = ''
    if ($Out) {
        $full = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).ProviderPath, $Out))
        $shown = Show-Path $Out
    } else {
        $tmp = $env:TEMP
        if (-not $tmp) { $tmp = [System.IO.Path]::GetTempPath() }
        $full = [System.IO.Path]::Combine($tmp, 'colour_patch_pc.json')
        $shown = '%TEMP%\colour_patch_pc.json'
    }
    return @{ full = $full; shown = $shown }
}

function Write-RawFile([string]$text, [string]$outPath, [string]$outShown) {
    $dir = Split-Path -Parent $outPath
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        [void][System.IO.Directory]::CreateDirectory($dir)
        Say ('created folder: ' + (Show-Path $dir))
        [void]$script:FilesWritten.Add(('folder ' + (Show-Path $dir)))
    }
    [System.IO.File]::WriteAllText($outPath, $text, (Get-Utf8NoBom))
    [void]$script:FilesWritten.Add($outShown)
}

function Remove-WorkDir {
    if ($script:WorkDir -and (Test-Path -LiteralPath $script:WorkDir)) {
        try { [System.IO.Directory]::Delete($script:WorkDir, $true) } catch { }
    }
    $script:WorkDir = ''
}

function Note-Location([string]$outFull) {
    # The raw file is for the chat only: say so if it was put somewhere inside the project folder.
    try {
        $repo = $script:Pat.Repo
        if ($repo -and $outFull.ToLower().StartsWith(([System.IO.Path]::GetFullPath($repo)).ToLower())) {
            Say 'NOTE this file is inside the project folder. The raw record is for the chat only: do not commit it and do not move it into the project. (renders\ is ignored by git; the project also refuses files named colour_patch_pc*.json.)'
        }
    } catch { }
}

# ---- step 1: the pattern file, before anything is collected (fail closed)
$script:StepNo++
if ($PatternSelfTest -eq '') { Write-Host ("[{0}/{1}] Loading the identifying-data patterns (scripts\redaction_patterns.json) ... " -f $script:StepNo, $TotalSteps) -NoNewline }
try {
    $script:Pat = Load-Patterns
    if ($PatternSelfTest -eq '') { Write-Host 'ok' }
} catch {
    if ($PatternSelfTest -eq '') { Write-Host 'FAILED' }
    $why = 'REDACTION PATTERNS UNAVAILABLE, nothing was collected and nothing was written: ' + (Clean-Message $_.Exception.Message)
    if ($PatternSelfTest -ne '') { [Console]::Error.WriteLine($why) } else { Say $why; Say 'files written: none' }
    exit 2
}

# ---- pattern self-test mode: nothing is collected
if ($PatternSelfTest -ne '') {
    [Console]::Error.WriteLine('TEST MODE: nothing was collected')
    try {
        $samples = (Read-TextFile $PatternSelfTest) | ConvertFrom-Json
    } catch {
        [Console]::Error.WriteLine('cannot read the samples file')
        exit 2
    }
    $items = $samples
    if ($samples -isnot [System.Array] -and ($samples.PSObject.Properties.Name -contains 'samples')) { $items = $samples.samples }
    $results = [ordered]@{}
    $pairs = New-Object System.Collections.ArrayList
    if ($items -is [System.Array]) {
        $i = 0
        foreach ($it in $items) {
            if ($it -is [string]) { [void]$pairs.Add(@{ id = [string]$i; text = $it }) }
            else {
                $t = $it.text
                if ($null -eq $t) { $t = $it.value }
                if ($null -eq $t -and $it.parts) { $t = -join @($it.parts | ForEach-Object { [string]$_ }) }
                [void]$pairs.Add(@{ id = [string]$it.id; text = [string]$t })
            }
            $i++
        }
    } else {
        foreach ($prop in $items.PSObject.Properties) {
            $v = $prop.Value
            if ($v -is [System.Array]) { $v = -join $v }
            elseif ($v -isnot [string] -and $v.parts) { $v = -join @($v.parts | ForEach-Object { [string]$_ }) }
            elseif ($v -isnot [string] -and $v.text) { $v = $v.text }
            [void]$pairs.Add(@{ id = $prop.Name; text = [string]$v })
        }
    }
    foreach ($pr in $pairs) {
        $ids = New-Object System.Collections.ArrayList
        foreach ($c in $script:Pat.Categories) {
            foreach ($m in $c.rx.Matches($pr.text)) {
                if (-not (Test-Exempt $script:Pat $c.id '' $pr.text $m)) {
                    if ($ids -notcontains $c.id) { [void]$ids.Add($c.id) }
                }
            }
        }
        $results[$pr.id] = $ids.ToArray()
    }
    $obj = [ordered]@{ consumer = 'win/kit2/run_checks_pc.ps1'; patterns_version = $script:Pat.Version; results = $results }
    Say (ConvertTo-Json -InputObject $obj -Depth 6 -Compress)
    exit 0
}

# ---- output path (default %TEMP%)
$op = Resolve-OutPath
$OutFull = $op.full
$OutShown = $op.shown

# ---- test mode: scan a fixture record as if it were the finished raw record
if ($TestFixture -ne '') {
    Say 'TEST MODE: nothing was collected'
    $fixtureText = ''
    $fixture = $null
    try {
        $fixtureText = Read-TextFile $TestFixture
        $fixture = $fixtureText | ConvertFrom-Json
    } catch {
        Say 'cannot read the fixture file'
        Say 'files written: none'
        exit 2
    }
    $scan = Invoke-SelfScan $script:Pat $fixture
    Write-ScanOutcome $scan
    if ($scan.refusals.Count -gt 0) {
        Say 'files written: none'
        exit 2
    }
    try {
        Write-RawFile $fixtureText $OutFull $OutShown
    } catch {
        Say ('could not write the file: ' + (Clean-Message $_.Exception.Message))
        Say 'files written: none'
        exit 3
    }
    Say 'redaction check passed'
    Note-Location $OutFull
    Say ('files written: ' + ($script:FilesWritten -join '; '))
    exit 0
}

# ====================================================================== the real run
$exitCode = 0
$refused = $false
$kitRoot = $script:Pat.Repo
$val = Join-Path (Join-Path $kitRoot 'pipeline') 'validators'
$cpScript = Join-Path $val 'colour_patch.py'
$specScript = Join-Path $val 'spec_check.py'
$helpScript = Join-Path $PSScriptRoot 'pc_helpers.py'
$chainsFile = Join-Path (Join-Path (Join-Path $kitRoot 'pipeline') 'lib') 'chains.json'
$phoneFile = Join-Path (Join-Path (Join-Path $kitRoot 'pipeline') 'phone') 'profile.json'
$py = $null
$ffmpegExe = $null
$ffmpegVersion = ''
$specOk = $null
$specText = ''
$cpText = ''
$cpExit = $null
$rawText = ''
$rawObj = $null
$specLine = 'not run'

try {
    # ---- step 2: Python
    Step 'Looking for Python 3 (py -3, python or python3)'
    $py = Find-Python
    if ($py) { Say 'ok' } else { Say 'NOT FOUND'; Say 'Python 3 is needed. README-KIT2.md has the install line (winget id UNVERIFIED). Nothing was written.'; $exitCode = 3 }

    # ---- step 3: ffmpeg
    Step 'Looking for ffmpeg (the one this PC will use)'
    if ($Ffmpeg) { if (Test-Path -LiteralPath $Ffmpeg -PathType Leaf) { $ffmpegExe = (Resolve-Path -LiteralPath $Ffmpeg).ProviderPath } }
    else { $ffmpegExe = Find-Exe 'ffmpeg' }
    if ($ffmpegExe) {
        $v = Invoke-Tool $ffmpegExe @('-hide_banner', '-version') 60
        $first = ''
        if ($v.ok -and $v.stdout) { $first = ($v.stdout -split "`n")[0] }
        if ($first -match 'ffmpeg version ([^\s]+)') { $ffmpegVersion = $Matches[1] }
        if ($ffmpegVersion -match '^([0-9]+(\.[0-9]+){1,3})') { $ffmpegVersion = $Matches[1] }
        elseif ($ffmpegVersion.Length -gt 24) { $ffmpegVersion = $ffmpegVersion.Substring(0, 24) }
        if ($v.ok -and $v.exit -eq 0) { Say ('ok (ffmpeg ' + $ffmpegVersion + ')') } else { Say 'FOUND BUT IT DID NOT RUN'; $ffmpegExe = $null; $exitCode = 3 }
    } else { Say 'NOT FOUND'; Say 'ffmpeg is needed. README-KIT2.md has the install line (winget id UNVERIFIED). Nothing was written.'; $exitCode = 3 }

    # ---- step 4: the project's own files
    Step 'Checking the project files this script uses'
    $missing = @()
    foreach ($f in @($cpScript, $specScript, $helpScript, $chainsFile)) { if (-not (Test-Path -LiteralPath $f)) { $missing += (Split-Path -Leaf $f) } }
    if ($missing.Count -eq 0) { Say 'ok' } else { Say ('MISSING: ' + ($missing -join ', ') + ' (download the WHOLE project folder, not single files)'); $exitCode = 3 }

    if ($exitCode -eq 0) {
        $name = 'lj_kit2_' + ([guid]::NewGuid().ToString('N')).Substring(0, 8)
        $tmpRoot = $env:TEMP
        if (-not $tmpRoot) { $tmpRoot = [System.IO.Path]::GetTempPath() }
        $script:WorkDir = [System.IO.Path]::Combine($tmpRoot, $name)
        [void][System.IO.Directory]::CreateDirectory($script:WorkDir)
        $clip = Join-Path $script:WorkDir 'clip.mp4'
        $specJson = Join-Path $script:WorkDir 'spec.json'
        $chainsAll = Join-Path $script:WorkDir 'chains_all.json'
        $candidate = Join-Path $script:WorkDir 'raw_candidate.json'

        # ---- step 5: the test clip
        Step 'Making a 3-second test clip with this ffmpeg (a temporary folder under %TEMP%, deleted at the end)'
        $clipOk = $false
        try {
            $r = Run-Python $py $helpScript @('clip', '--ffmpeg', $ffmpegExe, '--out', $clip) 300
            if ($r.ok -and $r.exit -eq 0 -and (Test-Path -LiteralPath $clip)) { Say 'ok'; $clipOk = $true }
            else { Say ('failed: ' + (Clean-Message ($r.stderr + ' ' + $r.stdout))); $exitCode = 3 }
        } catch { Say ('failed: ' + (Clean-Message $_.Exception.Message)); $exitCode = 3 }

        # ---- step 6: spec_check
        Step 'Checking the clip against the online delivery profile (spec_check.py --profile online_h264)'
        if ($clipOk) {
            try {
                $r = Run-Python $py $specScript @($clip, '--profile', 'online_h264', '--ffmpeg', $ffmpegExe, '--json', $specJson) 600
                $specText = $r.stdout
                if ($r.ok -and ($r.exit -eq 0 -or $r.exit -eq 1)) {
                    $specOk = ($r.exit -eq 0)
                    if ($specOk) { Say 'ok (all checks passed)' } else { Say 'ran; a check FAILED (see the lines below)'; if ($exitCode -eq 0) { $exitCode = 1 } }
                } else { Say ('failed: ' + (Clean-Message ($r.stderr + ' ' + $r.stdout))); $exitCode = 3 }
            } catch { Say ('failed: ' + (Clean-Message $_.Exception.Message)); $exitCode = 3 }
        } else { Say 'skipped (no test clip)' }

        # ---- step 7: one chain file with the project chains and the phone chains
        Step 'Joining the project chain file and the phone chain file for one run'
        $chainArg = $chainsFile
        try {
            $r = Run-Python $py $helpScript @('merge-chains', '--out', $chainsAll, '--extra', $phoneFile) 120
            if ($r.ok -and $r.exit -eq 0 -and (Test-Path -LiteralPath $chainsAll)) {
                $chainArg = $chainsAll
                if ($r.stdout -match 'was not found') { Say 'ok (the phone chain file was not found: the project chains are still tested)' } else { Say 'ok' }
            } else { Say ('failed: ' + (Clean-Message ($r.stderr + ' ' + $r.stdout)) + ' (the project chains alone will be tested)') }
        } catch { Say ('failed: ' + (Clean-Message $_.Exception.Message) + ' (the project chains alone will be tested)') }

        # ---- step 8: colour_patch
        Step 'Colour-patch test on this ffmpeg (colour_patch.py --all; this takes about a minute)'
        try {
            $r = Run-Python $py $cpScript @('--ffmpeg', $ffmpegExe, '--chain-file', $chainArg, '--all', '--json', $candidate) 1500
            $cpText = $r.stdout.Replace('wrote the RAW record raw_candidate.json.', 'wrote the raw record (step 10 names the file).')
            $cpExit = $r.exit
            if ($r.ok -and ($r.exit -eq 0 -or $r.exit -eq 1) -and (Test-Path -LiteralPath $candidate)) {
                if ($r.exit -eq 0) { Say 'ok (every chain within 3/255)' } else { Say 'ran; a chain is ABOVE the tolerance or could not be measured (see the lines below)'; if ($exitCode -eq 0) { $exitCode = 1 } }
            } else { Say ('failed: ' + (Clean-Message ($r.stderr + ' ' + $r.stdout))); $exitCode = 3 }
        } catch { Say ('failed: ' + (Clean-Message $_.Exception.Message)); $exitCode = 3 }

        # ---- step 9: scan everything that will be printed or written, before any of it is
        Step 'Scanning the record and the text below for identifying data (patterns file plus your own names)'
        if (Test-Path -LiteralPath $candidate) {
            $rawText = Read-TextFile $candidate
            $rawObj = $rawText | ConvertFrom-Json
            # the record is scanned with its own field names (as in the file you will read); the printed text is scanned as two fields
            $scan = Invoke-SelfScan $script:Pat $rawObj
            $scanText = Invoke-SelfScan $script:Pat ([ordered]@{ spec_check_output = $specText; colour_patch_output = $cpText })
            foreach ($h in $scanText.refusals) { [void]$scan.refusals.Add($h) }
            if ($scan.refusals.Count -gt 0) {
                Say 'REFUSED'
                Write-ScanOutcome $scan
                $refused = $true
                $exitCode = 2
            } else {
                Say 'ok (nothing matched)'
                foreach ($s in $scan.skipped) { Say ("NOTE name check skipped for a {0} of {1} character(s): shorter than the minimum, so it would match ordinary words (the pattern checks still ran)" -f $s.category, $s.length) }
            }
        } else { Say 'skipped (no colour-patch record)' }

        # ---- the tool output, only after the scan passed
        if (-not $refused) {
            if ($specText) { Say ''; foreach ($ln in ($specText -split "`n")) { if ($ln.Trim()) { Say ('  ' + $ln.TrimEnd()) } } }
            if ($cpText) { Say ''; foreach ($ln in ($cpText -split "`n")) { if ($ln.Trim()) { Say ('  ' + $ln.TrimEnd()) } } }
            Say ''
        }

        # ---- step 10: write the raw record
        Step ('Writing the raw record (' + $OutShown + ')')
        if ($refused) { Say 'skipped (the scan refused)' }
        elseif (-not $rawText) { Say 'skipped (no colour-patch record)' }
        else {
            try {
                Write-RawFile $rawText $OutFull $OutShown
                Say 'ok'
                Note-Location $OutFull
            } catch {
                Say ('failed: ' + (Clean-Message $_.Exception.Message))
                $exitCode = 3
            }
        }
    }
} catch {
    Say ''
    Say ('FAILED: ' + $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message))
    $exitCode = 3
} finally {
    # ---- step 11: the temporary folder
    Step 'Deleting the temporary folder'
    Remove-WorkDir
    Say 'ok'
}

# ---- the paste block (only when the record exists and the scan passed)
if (-not $refused -and $rawObj -and $script:FilesWritten.Count -gt 0) {
    $verdict = 'not run'
    if ($specOk -eq $true) { $verdict = 'PASS' } elseif ($specOk -eq $false) { $verdict = 'FAIL' }
    $rows = @()
    foreach ($c in @($rawObj.chains)) { $rows += ('{0}={1}' -f $c.name, $c.worst_error) }
    $ctl = @()
    foreach ($c in @($rawObj.controls)) { $ctl += ('{0}={1}' -f $c.name, $c.worst_error) }
    Say '----- PASTE THIS IN THE CHAT, AFTER YOU HAVE READ IT -----'
    Say ('ffmpeg ' + $ffmpegVersion + '  sha256 ' + $rawObj.ffmpeg.sha256)
    Say ('spec_check online_h264: ' + $verdict)
    Say ('colour_patch worst error per chain (limit 3, out of 255): ' + ($rows -join ' '))
    Say ('controls: ' + ($ctl -join ' '))
    Say ('raw record: ' + $OutShown + '  (open it in Notepad, read it, and paste its whole text in the chat too)')
    Say 'Do not save it in the project folder and do not commit it. The project keeps only a short derived form made from your paste.'
    Say '----- END -----'
}
if ($script:FilesWritten.Count -gt 0) { Say ('files written: ' + ($script:FilesWritten -join '; ')) } else { Say 'files written: none' }
exit $exitCode
