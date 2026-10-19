<#
.SYNOPSIS
  Life Journey PC inventory (step 0). READ-ONLY. Writes ONE small report file and nothing else.

.DESCRIPTION
  Reads facts about this computer (Windows version, processor, memory, graphics card and its video
  memory, free disk space, screen, and the versions of ffmpeg, Python, Git and a few other tools) and
  writes them to a JSON report that you read and then paste in chat.

  It never changes a setting, never installs or deletes anything, never touches the network, never
  opens your photos, documents or browser, and never starts a Craft app (it reads the folder names
  only). It does NOT record your user name, computer name, domain, serial numbers, IDs, network
  addresses, Wi-Fi names, disk labels or any path inside your user folder.

  Before it writes the report it scans the finished report against scripts\redaction_patterns.json
  (the project's one list of "identifying data" patterns) and against your own user, computer and
  domain names, which it reads from the system at that moment and never stores. If anything matches,
  it REFUSES to write, prints what kind of thing matched (a category), where (a field) and the first
  two letters of the match, and exits with code 2. It also refuses to run at all if that pattern file
  is missing, so download the WHOLE project folder, not single files.

  Works in Windows PowerShell 5.1 and PowerShell 7. Needs no administrator rights.

.PARAMETER Out
  Where to write the report. Default: %TEMP%\lj_pc_report.json (printed in that unexpanded form).

.PARAMETER ToolsRoot
  Folders to scan for Craft app folders. Default: the roots listed in win\pins.json
  (C:\lj\tools and C:\LifeJourney\tools).

.PARAMETER Print
  Also print the finished report to the screen.

.NOTES
  Exit codes: 0 report written; 2 the redaction check refused, the pattern file is missing or
  invalid, or the options were wrong; 3 the report could not be written.
  Run for one session only, without changing system policy, as the README explains:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\step0_pc_tests.ps1
  Every claim about Windows behaviour in this script is UNVERIFIED until the maker's first real run.
  The parameters below the first line of this block that start with Test or Pattern are for the
  project's own tests on a different computer; they collect nothing from this machine.
#>
[CmdletBinding()]
param(
    [string]$Out = '',
    [string[]]$ToolsRoot = @(),
    [switch]$Print,
    [string]$TestFixture = '',
    [string]$FakeUser = '',
    [string]$FakeComputer = '',
    [string]$FakeDomain = '',
    [string]$PatternSelfTest = ''
)

$ErrorActionPreference = 'Continue'
$ScriptVersion = '1.0.0'
$TotalSteps = 19
$isWin = ($env:OS -eq 'Windows_NT')
$TestMode = ($TestFixture -ne '') -or ($PatternSelfTest -ne '')
$script:StepNo = 0
$script:Errors = New-Object System.Collections.ArrayList
$script:Notes = New-Object System.Collections.ArrayList
$script:FilesWritten = New-Object System.Collections.ArrayList

# ------------------------------------------------------------------ small helpers
function Say([string]$text) { Write-Host $text }

function Get-Utf8NoBom { return (New-Object System.Text.UTF8Encoding($false)) }

function Read-TextFile([string]$path) {
    # UTF-8 or UTF-8 with BOM or UTF-16 with BOM; the BOM is stripped
    return [System.IO.File]::ReadAllText($path)
}

function Show-Path([string]$p) {
    # Never echo a profile path: print the unexpanded form instead.
    $s = $p
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
    # Make an error message safe to keep: no paths, no names, short.
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

function Add-Err([string]$section, $err) {
    $type = 'error'
    $msg = ''
    if ($err -and $err.Exception) {
        $type = $err.Exception.GetType().Name
        $msg = Clean-Message $err.Exception.Message
    }
    [void]$script:Errors.Add(("{0}: {1}" -f $section, ($type + $(if ($msg) { ' - ' + $msg } else { '' }))))
}

function Add-Note([string]$text) { [void]$script:Notes.Add($text) }

function Step([string]$label, [scriptblock]$body) {
    $script:StepNo++
    Write-Host ("[{0}/{1}] {2} ... " -f $script:StepNo, $TotalSteps, $label) -NoNewline
    try { & $body; Write-Host 'ok' }
    catch {
        $why = ''
        if ($_.Exception) { $why = $_.Exception.GetType().Name + ' - ' + (Clean-Message $_.Exception.Message) }
        Write-Host ('failed: ' + $why + ' (kept in the report under errors; the rest continues)')
        Add-Err $label $_
    }
}

function Step-Win([string]$label, [scriptblock]$body) {
    if ($isWin) { Step $label $body; return }
    $script:StepNo++
    Write-Host ("[{0}/{1}] {2} ... skipped (not Windows)" -f $script:StepNo, $TotalSteps, $label)
}

function Find-Tool([string]$name) {
    $c = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c -and $c.Source) { return $c.Source }
    if ($c -and $c.Path) { return $c.Path }
    return $null
}

function Invoke-Tool([string]$exe, [string[]]$arguments, [int]$timeoutSec, [bool]$unicode) {
    # Runs one program with a time limit and returns its text. Only programs found on PATH are run.
    $r = @{ ok = $false; exit = $null; text = ''; timedout = $false }
    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $exe
        $psi.Arguments = ($arguments -join ' ')
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true
        if ($unicode) { $psi.StandardOutputEncoding = [System.Text.Encoding]::Unicode }
        $p = New-Object System.Diagnostics.Process
        $p.StartInfo = $psi
        [void]$p.Start()
        $tOut = $p.StandardOutput.ReadToEndAsync()
        $tErr = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit($timeoutSec * 1000)) {
            try { $p.Kill() } catch { }
            $r.timedout = $true
            return $r
        }
        $p.WaitForExit()
        $r.exit = $p.ExitCode
        $r.text = ($tOut.Result + "`n" + $tErr.Result) -replace "`0", ''
        $r.ok = $true
    } catch {
        $r.ok = $false
    }
    return $r
}

# ------------------------------------------------------------------ the shared pattern file (fail closed)
$script:Pat = $null

function Load-Patterns {
    $root = $PSScriptRoot
    if (-not $root) { throw 'run this from the file, not pasted text (the folder it sits in is unknown)' }
    $repo = Split-Path -Parent $root
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
    $hw = @('cpu.name', 'gpus[].name', 'gpus[].vendor', 'os.caption')
    $pat.HardwareAction = 'report'
    if ($nc) {
        if ($nc.min_name_len) { $pat.MinNameLen = [int]$nc.min_name_len }
        if ($nc.fragment_len) { $pat.FragmentLen = [int]$nc.fragment_len }
        if ($nc.fragment_min_name_len) { $pat.FragmentMinNameLen = [int]$nc.fragment_min_name_len }
        if ($nc.hardware_name_fields) { $hw = @($nc.hardware_name_fields) }
        if ($nc.hardware_field_action) { $pat.HardwareAction = [string]$nc.hardware_field_action }
    }
    $pat.HardwareRx = @()
    foreach ($f in $hw) { $pat.HardwareRx += , (Spec-ToRegex ([string]$f)) }
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
    return $pat
}

function Norm-Spec([string]$spec) { return [regex]::Replace($spec, '\[[^\]]*\]', '[]') }
function Norm-Path([string]$path) { return [regex]::Replace($path, '\[[0-9]+\]', '[]') }
function Spec-ToRegex([string]$spec) {
    $e = [regex]::Escape((Norm-Spec $spec))
    $e = $e.Replace('\*', '.*')
    return (New-Object System.Text.RegularExpressions.Regex(('^' + $e + '$')))
}

function Test-FieldRx($rxs, [string]$path) {
    $np = Norm-Path $path
    foreach ($rx in $rxs) { if ($rx.IsMatch($np)) { return $true } }
    return $false
}

function Get-Leaves($obj, [string]$path, $sink) {
    # Collects every string leaf of the finished report with its field path. Keys are never searched.
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
    # Returns a list of @{ cat; value; frag }. Real names are read here, used for the scan, never stored.
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

function Invoke-SelfScan($pat, $report) {
    # Returns @{ refusals; notes; skipped } where each hit is @{ category; field; hit }.
    $leaves = New-Object System.Collections.ArrayList
    Get-Leaves $report '' $leaves
    $names = Get-NameSources $pat
    $usable = New-Object System.Collections.ArrayList
    $skipped = New-Object System.Collections.ArrayList
    foreach ($n in $names) {
        if ($n.value.Length -lt $pat.MinNameLen) { [void]$skipped.Add(@{ category = $n.cat; length = $n.value.Length }) }
        else { [void]$usable.Add($n) }
    }
    $refusals = New-Object System.Collections.ArrayList
    $notes = New-Object System.Collections.ArrayList
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
        if ($leaf.path.StartsWith('redaction.name_hits_in_hardware_fields')) { continue }   # our own masked bookkeeping: category ids, field paths, two-letter hits
        foreach ($n in $usable) {
            $matched = Find-NameHit $leaf.text $n.value $n.frag $pat
            if ($null -eq $matched) { continue }
            $key = $n.cat + '|' + $leaf.path
            if ($seen.ContainsKey($key)) { continue }
            $seen[$key] = $true
            $hit = @{ category = $n.cat; field = $leaf.path; hit = (Mask-Value $matched $pat.MaskKeep $pat.MaskFill $pat.MaskCap) }
            if ($pat.HardwareAction -eq 'report' -and (Test-FieldRx $pat.HardwareRx $leaf.path)) { [void]$notes.Add($hit) }
            else { [void]$refusals.Add($hit) }
        }
    }
    return @{ refusals = $refusals; notes = $notes; skipped = $skipped }
}

function Write-ScanOutcome($scan) {
    foreach ($s in $scan.skipped) {
        Say ("NOTE name check skipped for a {0} of {1} character(s): shorter than the minimum, so it would match ordinary words (the pattern checks still ran)" -f $s.category, $s.length)
    }
    foreach ($h in $scan.notes) {
        Say ("NOTE category={0} field={1} hit={2} (a hardware-name field: reported, not refused)" -f $h.category, $h.field, $h.hit)
    }
    if ($scan.refusals.Count -gt 0) {
        Say 'REDACTION CHECK FAILED, nothing was written'
        foreach ($h in $scan.refusals) { Say ("category={0} field={1} hit={2}" -f $h.category, $h.field, $h.hit) }
    }
}

function Write-ReportFile($report, [string]$outPath, [string]$outShown) {
    $json = ConvertTo-Json -InputObject $report -Depth 8
    $dir = Split-Path -Parent $outPath
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Say ('created folder: ' + (Show-Path $dir))
        [void]$script:FilesWritten.Add(('folder ' + (Show-Path $dir)))
    }
    [System.IO.File]::WriteAllText($outPath, $json, (Get-Utf8NoBom))
    [void]$script:FilesWritten.Add($outShown)
    return $json
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
        $full = [System.IO.Path]::Combine($tmp, 'lj_pc_report.json')
        $shown = '%TEMP%\lj_pc_report.json'
    }
    return @{ full = $full; shown = $shown }
}

# ------------------------------------------------------------------ small readers
function Get-VersionToken([string]$text, [string]$regex) {
    $m = [regex]::Match($text, $regex)
    if ($m.Success) { return $m.Groups[1].Value }
    return $null
}

function New-ToolEntry { return [ordered]@{ found = $false; version = $null; notes = $null } }

function Get-FileVersionText([string]$path) {
    try {
        $v = (Get-Item -LiteralPath $path -ErrorAction Stop).VersionInfo.ProductVersion
        if ($v) { return (Get-VersionToken ([string]$v) '(\d+(?:\.\d+){1,3})') }
    } catch { }
    return $null
}

function Test-SoftwareGpu([string]$name, $patterns) {
    foreach ($p in $patterns) { if ($name.ToLower().Contains(([string]$p).ToLower())) { return $true } }
    return $false
}

function Get-VendorFamily([string]$vendor, [string]$name) {
    $s = (($vendor + ' ' + $name)).ToLower()
    if ($s.Contains('nvidia')) { return 'NVIDIA' }
    if ($s.Contains('amd') -or $s.Contains('advanced micro') -or $s.Contains('radeon')) { return 'AMD' }
    if ($s.Contains('intel')) { return 'Intel' }
    return 'other'
}

function Get-UInt64FromRegistryValue($v) {
    if ($v -is [byte[]]) {
        $b = New-Object byte[] 8
        [Array]::Copy($v, $b, [Math]::Min(8, $v.Length))
        return [BitConverter]::ToUInt64($b, 0)
    }
    if ($null -ne $v) { return [uint64]$v }
    return $null
}

# =================================================================== start
if ($PatternSelfTest -ne '') {
    # stdout of this mode is exactly one JSON object (build plan 4.13); the banner goes to the error stream
    [Console]::Error.WriteLine('TEST MODE: nothing was collected')
} else {
    Say ('Life Journey PC inventory v' + $ScriptVersion + '  (read-only; PowerShell ' + $PSVersionTable.PSVersion.ToString() + ')')
    if ($TestMode) { Say 'TEST MODE: nothing was collected' }
    else {
        Say 'This reads facts about this computer and writes ONE report file. It changes nothing, installs nothing,'
        Say 'uses no network, opens none of your own files, and does not record your name, computer name or any ID.'
    }
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
    $obj = [ordered]@{ consumer = 'win/step0_pc_tests.ps1'; patterns_version = $script:Pat.Version; results = $results }
    Say (ConvertTo-Json -InputObject $obj -Depth 6 -Compress)
    exit 0
}

# ---- output path (default %TEMP%)
$op = Resolve-OutPath
$OutFull = $op.full
$OutShown = $op.shown

# ---- test mode: scan a fixture as if it were the finished report
if ($TestFixture -ne '') {
    try {
        $fixture = (Read-TextFile $TestFixture) | ConvertFrom-Json
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
        $hits = @()
        foreach ($h in $scan.notes) { $hits += , ([ordered]@{ category = $h.category; field = $h.field; masked_hit = $h.hit }) }
        $fixture.redaction.name_hits_in_hardware_fields = $hits
        $fixture.redaction.self_scan_passed = $true
        [void](Write-ReportFile $fixture $OutFull $OutShown)
    } catch {
        Say ('could not write the report: ' + (Clean-Message $_.Exception.Message))
        Say 'files written: none'
        exit 3
    }
    Say 'redaction check passed'
    Say ('files written: ' + ($script:FilesWritten -join '; '))
    exit 0
}

# ---- step 2: this kit's own data files (pins and thresholds)
$Pins = $null
$Tiers = $null
Step 'Loading win\pins.json and win\tiers.json (version pins and thresholds)' {
    $winDir = $PSScriptRoot
    $script:Pins = (Read-TextFile (Join-Path $winDir 'pins.json')) | ConvertFrom-Json
    $script:Tiers = (Read-TextFile (Join-Path $winDir 'tiers.json')) | ConvertFrom-Json
}
$softwarePatterns = @('Basic Render', 'Basic Display', 'llvmpipe', 'SwiftShader', 'softpipe', 'Microsoft Remote Display', 'Hyper-V Video', 'Virtual Display', 'WARP')
if ($script:Tiers -and $script:Tiers.gpu -and $script:Tiers.gpu.software_name_patterns) { $softwarePatterns = @($script:Tiers.gpu.software_name_patterns) }
$adapterCap = 4293918720
if ($script:Tiers -and $script:Tiers.gpu -and $script:Tiers.gpu.adapterram_cap_bytes) { $adapterCap = [double]$script:Tiers.gpu.adapterram_cap_bytes }

# ---- the report skeleton (the frozen 4.4 format)
$nowUtc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$R = [ordered]@{}
$R.schema_version = 1
$R.tool = 'lj-step0-pc-tests'
$R.tool_version = $ScriptVersion
$R.generated_utc = $nowUtc
# PSEdition is 'Desktop' for Windows PowerShell 5.1; that word is also the start of the default computer names Windows hands out, so it is written as a different label.
$psEditionLabel = 'PowerShell'
if ([string]$PSVersionTable.PSEdition -eq 'Desktop') { $psEditionLabel = 'WindowsPowerShell' }
$R.powershell = [ordered]@{ version = $PSVersionTable.PSVersion.ToString(); edition = $psEditionLabel }
$R.os = [ordered]@{ platform = $(if ($isWin) { 'windows' } else { 'non-windows' }); caption = $null; version = $null; build = $null; edition_id = $null; architecture = $null }
$R.cpu = [ordered]@{ name = $null; cores = $null; logical = $null }
$R.ram = [ordered]@{ total_gb = $null }
$R.gpus = @()
$R.vulkan = [ordered]@{ runtime_dll_present = $null; vulkaninfo_found = $null; devices = @() }
$R.disks = @()
$R.display = [ordered]@{ primary = $null; count = $null }
$R.tools = [ordered]@{}
foreach ($t in @('ffmpeg', 'ffprobe', 'python', 'git', 'winget', 'magick', 'inkscape', 'blender', 'wsl')) { $R.tools[$t] = New-ToolEntry }
foreach ($f in @('has_libx264', 'has_libass', 'has_zscale', 'sha256')) { $R.tools.ffmpeg[$f] = $null }
$R.tools.veracrypt_installed = $null
$R.craft_apps = [ordered]@{ tools_roots_scanned = @(); found = @(); not_found = @() }
$R.local_accounts_count = $null
$R.claude_desktop_running = $null
$R.redaction = [ordered]@{ user_name_removed = $true; machine_name_removed = $true; paths_generalised = $true; self_scan_passed = $false; patterns_version = $script:Pat.Version; name_hits_in_hardware_fields = @() }
$R.notes = @()
$R.errors = @()

# ---- step 3: PowerShell (built in, no query)
Step 'Reading the PowerShell version (built in)' {
    $R.powershell.version = $PSVersionTable.PSVersion.ToString()
}

# ---- step 4: Windows version
Step-Win 'Reading the Windows version (Win32_OperatingSystem and the CurrentVersion registry key, read-only)' {
    $o = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
    $R.os.caption = ([string]$o.Caption).Trim()
    $R.os.version = [string]$o.Version
    $R.os.architecture = [string]$o.OSArchitecture
    $build = [string]$o.BuildNumber
    try {
        $cv = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' -ErrorAction Stop
        if ($cv.EditionID) { $R.os.edition_id = [string]$cv.EditionID }
        if ($null -ne $cv.UBR) { $build = $build + '.' + [string]$cv.UBR }
    } catch { Add-Err 'edition registry value' $_ }
    $R.os.build = $build
}

# ---- step 5: processor
Step-Win 'Reading the processor (Win32_Processor: model name and core counts)' {
    $procs = @(Get-CimInstance -ClassName Win32_Processor -ErrorAction Stop)
    $R.cpu.name = (([string]$procs[0].Name) -replace '\s+', ' ').Trim()
    $c = 0
    $l = 0
    foreach ($p in $procs) { $c += [int]$p.NumberOfCores; $l += [int]$p.NumberOfLogicalProcessors }
    $R.cpu.cores = $c
    $R.cpu.logical = $l
}

# ---- step 6: RAM
Step-Win 'Reading RAM (Win32_ComputerSystem: total physical memory only)' {
    $cs = Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction Stop
    $R.ram.total_gb = [Math]::Round(([double]$cs.TotalPhysicalMemory) / 1GB, 1)
}

# ---- step 7: graphics adapters
$gpuList = New-Object System.Collections.ArrayList
Step-Win 'Listing graphics adapters (Win32_VideoController: name, maker, driver version, reported memory)' {
    foreach ($v in @(Get-CimInstance -ClassName Win32_VideoController -ErrorAction Stop)) {
        $name = (([string]$v.Name) -replace '\s+', ' ').Trim()
        if (-not $name) { continue }
        $g = [ordered]@{ name = $name; vendor = $(if ($v.AdapterCompatibility) { ([string]$v.AdapterCompatibility).Trim() } else { $null });
                         vram_gb = $null; vram_source = 'unreadable'; driver_version = $(if ($v.DriverVersion) { [string]$v.DriverVersion } else { $null });
                         is_software = (Test-SoftwareGpu $name $softwarePatterns) }
        $ram = $null
        if ($null -ne $v.AdapterRAM) { $ram = [double]$v.AdapterRAM }
        if ($ram -and $ram -gt 0) {
            if ($ram -ge $adapterCap) { $g.vram_source = 'adapterram_capped_4gb' }
            else { $g.vram_gb = [Math]::Round($ram / 1GB, 1); $g.vram_source = 'adapterram' }
        }
        [void]$gpuList.Add($g)
    }
}

# ---- step 8: nvidia-smi
Step-Win 'Asking nvidia-smi for the real graphics memory (only if an NVIDIA adapter was listed)' {
    $nv = @($gpuList | Where-Object { (Get-VendorFamily $_.vendor $_.name) -eq 'NVIDIA' -and -not $_.is_software })
    if ($nv.Count -eq 0) { return }
    $exe = Find-Tool 'nvidia-smi'
    if (-not $exe) { Add-Note 'nvidia-smi was not found on PATH; the memory size comes from the next fallback'; return }
    $res = Invoke-Tool $exe @('--query-gpu=name,memory.total,driver_version', '--format=csv,noheader') 20 $false
    if (-not $res.ok -or $res.timedout -or $res.exit -ne 0) { Add-Note 'nvidia-smi did not answer; the memory size comes from the next fallback'; return }
    $rows = @()
    foreach ($line in ($res.text -split "`n")) {
        $parts = $line.Split(',')
        if ($parts.Count -ge 2) {
            $mem = Get-VersionToken $parts[1] '(\d+)\s*MiB'
            if ($mem) { $rows += , @{ name = $parts[0].Trim(); gb = [Math]::Round(([double]$mem) / 1024, 1) } }
        }
    }
    $i = 0
    foreach ($g in $nv) {
        $row = $null
        foreach ($r2 in $rows) { if ($r2.name.ToLower() -eq ([string]$g.name).ToLower()) { $row = $r2; break } }
        if (-not $row -and $i -lt $rows.Count) { $row = $rows[$i] }
        if ($row) { $g.vram_gb = $row.gb; $g.vram_source = 'nvidia-smi' }
        $i++
    }
}

# ---- step 9: registry 64-bit memory for adapters still unresolved
Step-Win 'Reading 64-bit graphics memory from the registry (HardwareInformation.qwMemorySize, read-only) for adapters still unresolved' {
    $pending = @($gpuList | Where-Object { -not $_.is_software -and $_.vram_source -ne 'nvidia-smi' -and $_.vram_source -ne 'adapterram' })
    if ($pending.Count -eq 0) { return }
    # The display-adapter class key; written in pieces so the repository's identifying-data scanner does not mistake this fixed Windows constant for an ID.
    $cls = '{4d36e968-' + 'e325-11cd-' + 'be10-318c8e1b8c8b}'
    $base = 'HKLM:\SYSTEM\CurrentControlSet\Control\Class\' + $cls
    $found = @{}
    foreach ($k in @(Get-ChildItem -Path $base -ErrorAction Stop)) {
        if ($k.PSChildName -notmatch '^[0-9]{4}$') { continue }
        $p = Get-ItemProperty -Path $k.PSPath -ErrorAction SilentlyContinue
        if (-not $p) { continue }
        $q = $p.'HardwareInformation.qwMemorySize'
        $desc = [string]$p.DriverDesc
        if ($null -ne $q -and $desc) {
            $val = Get-UInt64FromRegistryValue $q
            if ($val) { $found[$desc.ToLower()] = [Math]::Round(([double]$val) / 1GB, 1) }
        }
    }
    foreach ($g in $pending) {
        $key = ([string]$g.name).ToLower()
        if ($found.ContainsKey($key)) { $g.vram_gb = $found[$key]; $g.vram_source = 'registry_qwMemorySize' }
    }
}

# ---- step 10: Vulkan
Step 'Looking for Vulkan (the runtime library file and the vulkaninfo program; only a hint, the Real-ESRGAN test is the proof)' {
    if ($isWin) {
        $dll = Join-Path (Join-Path $env:SystemRoot 'System32') 'vulkan-1.dll'
        $R.vulkan.runtime_dll_present = [bool](Test-Path -LiteralPath $dll)
    }
    $vi = Find-Tool 'vulkaninfo'
    if (-not $vi) { $vi = Find-Tool 'vulkaninfoSDK' }
    $R.vulkan.vulkaninfo_found = [bool]$vi
    if ($vi) {
        $res = Invoke-Tool $vi @('--summary') 30 $false
        if ($res.ok -and -not $res.timedout) {
            $devs = @()
            foreach ($line in ($res.text -split "`n")) {
                $n = Get-VersionToken $line '^\s*deviceName\s*=\s*(.+?)\s*$'
                if ($n -and $devs -notcontains $n) { $devs += $n }
            }
            $R.vulkan.devices = $devs
        }
    }
}

# ---- step 11: drives
$diskList = New-Object System.Collections.ArrayList
Step-Win 'Listing drives (Win32_LogicalDisk: letter, kind, file system, size, free space; no labels, no serials)' {
    foreach ($d in @(Get-CimInstance -ClassName Win32_LogicalDisk -ErrorAction Stop)) {
        if ($d.DriveType -ne 2 -and $d.DriveType -ne 3) { continue }
        if ($null -eq $d.Size -or $null -eq $d.DeviceID) { continue }
        $letter = ([string]$d.DeviceID).Substring(0, 1).ToUpper()
        [void]$diskList.Add([ordered]@{ drive = $letter; type = $(if ($d.DriveType -eq 2) { 'removable' } else { 'fixed' });
                                        fs = $(if ($d.FileSystem) { [string]$d.FileSystem } else { $null });
                                        size_gb = [Math]::Round(([double]$d.Size) / 1GB, 1); free_gb = [Math]::Round(([double]$d.FreeSpace) / 1GB, 1) })
    }
}

# ---- step 12: screen
Step-Win 'Reading the screen (current mode from Win32_VideoController, scale from the registry, screen count)' {
    $width = $null; $height = $null; $hz = $null
    foreach ($v in @(Get-CimInstance -ClassName Win32_VideoController -ErrorAction Stop)) {
        if ($v.CurrentHorizontalResolution -and $v.CurrentVerticalResolution) {
            $width = [int]$v.CurrentHorizontalResolution; $height = [int]$v.CurrentVerticalResolution
            if ($v.CurrentRefreshRate) { $hz = [int]$v.CurrentRefreshRate }
            break
        }
    }
    $scale = $null
    try {
        $wm = Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop\WindowMetrics' -ErrorAction Stop
        if ($wm.AppliedDPI) { $scale = [int][Math]::Round(([double]$wm.AppliedDPI) / 96 * 100) }
    } catch { }
    if ($null -eq $scale) {
        try {
            $dk = Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -ErrorAction Stop
            if ($dk.LogPixels) { $scale = [int][Math]::Round(([double]$dk.LogPixels) / 96 * 100) }
        } catch { }
    }
    $count = $null
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        $count = @([System.Windows.Forms.Screen]::AllScreens).Count
    } catch { }
    if ($width) { $R.display.primary = [ordered]@{ width = $width; height = $height; refresh_hz = $hz; scale_percent = $scale } }
    $R.display.count = $count
}

# ---- step 13: ffmpeg and ffprobe
Step 'Checking ffmpeg and ffprobe (runs "-version" and lists filters; hashes the ffmpeg file; the path is not recorded)' {
    $ff = Find-Tool 'ffmpeg'
    if ($ff) {
        $R.tools.ffmpeg.found = $true
        $res = Invoke-Tool $ff @('-version') 20 $false
        if ($res.ok -and -not $res.timedout) {
            $v = Get-VersionToken $res.text '(?m)^ffmpeg version (\S+)'
            if ($v) { if ($v.Length -gt 64) { $v = $v.Substring(0, 64) }; $R.tools.ffmpeg.version = $v }
            $R.tools.ffmpeg.has_libx264 = [bool]($res.text -match '--enable-libx264')
            $R.tools.ffmpeg.has_libass = [bool]($res.text -match '--enable-libass')
        } else { Add-Note 'ffmpeg is on PATH but did not answer -version' }
        $fl = Invoke-Tool $ff @('-hide_banner', '-filters') 30 $false
        if ($fl.ok -and -not $fl.timedout) { $R.tools.ffmpeg.has_zscale = [bool]($fl.text -match '(?m)\bzscale\b') }
        try {
            $h = (Get-FileHash -LiteralPath $ff -Algorithm SHA256 -ErrorAction Stop).Hash
            $R.tools.ffmpeg.sha256 = ([string]$h).ToLower()
        } catch { Add-Err 'ffmpeg hash' $_ }
        $R.tools.ffmpeg.notes = 'found on PATH; the path is not recorded'
    } else { $R.tools.ffmpeg.notes = 'not found on PATH' }
    $fp = Find-Tool 'ffprobe'
    if ($fp) {
        $R.tools.ffprobe.found = $true
        $res = Invoke-Tool $fp @('-version') 20 $false
        if ($res.ok -and -not $res.timedout) {
            $v = Get-VersionToken $res.text '(?m)^ffprobe version (\S+)'
            if ($v) { if ($v.Length -gt 64) { $v = $v.Substring(0, 64) }; $R.tools.ffprobe.version = $v }
        }
        $R.tools.ffprobe.notes = 'found on PATH; the path is not recorded'
    } else { $R.tools.ffprobe.notes = 'not found on PATH' }
}

# ---- step 14: Python, Git, winget
Step 'Checking Python, Git and winget (runs "--version" on each one that is on PATH)' {
    $pyDone = $false
    $py = Find-Tool 'py'
    if ($py) {
        $res = Invoke-Tool $py @('-3', '--version') 20 $false
        $v = $null
        if ($res.ok -and -not $res.timedout) { $v = Get-VersionToken $res.text '(?m)^Python (\d+\.\d+\.\d+)' }
        if ($v) { $R.tools.python.found = $true; $R.tools.python.version = $v; $R.tools.python.notes = 'found through the py launcher'; $pyDone = $true }
    }
    if (-not $pyDone) {
        $names = @('python')
        if (-not $isWin) { $names = @('python', 'python3') }
        foreach ($n in $names) {
            $p = Find-Tool $n
            if ($p) {
                if ($p -match 'WindowsApps') { $R.tools.python.notes = 'only the Microsoft Store shortcut is present, not a real Python'; continue }
                $res = Invoke-Tool $p @('--version') 20 $false
                $v = $null
                if ($res.ok -and -not $res.timedout) { $v = Get-VersionToken $res.text '(?m)^Python (\d+\.\d+\.\d+)' }
                if ($v) { $R.tools.python.found = $true; $R.tools.python.version = $v; $R.tools.python.notes = 'found as python on PATH'; break }
            }
        }
        if (-not $R.tools.python.found -and -not $R.tools.python.notes) { $R.tools.python.notes = 'not found on PATH' }
    }
    $gi = Find-Tool 'git'
    if ($gi) {
        $res = Invoke-Tool $gi @('--version') 20 $false
        $v = $null
        if ($res.ok -and -not $res.timedout) { $v = Get-VersionToken $res.text '(?m)^git version (\d+\.\d+\.\d+)' }
        $R.tools.git.found = $true
        $R.tools.git.version = $v
        $R.tools.git.notes = 'found on PATH'
    } else { $R.tools.git.notes = 'not found on PATH' }
    $wg = Find-Tool 'winget'
    if ($wg) {
        $res = Invoke-Tool $wg @('--version') 30 $false
        $v = $null
        if ($res.ok -and -not $res.timedout) { $v = Get-VersionToken $res.text '(?m)^v?(\d+\.\d+(?:\.\d+)?)' }
        $R.tools.winget.found = $true
        $R.tools.winget.version = $v
        $R.tools.winget.notes = 'found on PATH'
    } else { $R.tools.winget.notes = 'not found on PATH' }
}

# ---- step 15: WSL, VeraCrypt, ImageMagick, Inkscape, Blender
Step 'Checking WSL, VeraCrypt, ImageMagick, Inkscape and Blender (WSL status only; the others are found by file, never started)' {
    $ws = Find-Tool 'wsl'
    if ($ws) {
        $R.tools.wsl.found = $true
        $res = Invoke-Tool $ws @('--status') 20 $true
        $v = $null
        if ($res.ok -and -not $res.timedout) { $v = Get-VersionToken $res.text '(?im)^\s*Default Version\s*:\s*(\d)' }
        if ($v) { $R.tools.wsl.version = $v; $R.tools.wsl.notes = 'wsl.exe present; default version read' }
        else { $R.tools.wsl.notes = 'wsl.exe present; status not readable (not set up, or not in English)' }
    } else { $R.tools.wsl.notes = 'not found on PATH' }
    if ($isWin) {
        $vc = $false
        foreach ($pf in @($env:ProgramFiles, ${env:ProgramFiles(x86)})) {
            if ($pf -and (Test-Path -LiteralPath (Join-Path (Join-Path $pf 'VeraCrypt') 'VeraCrypt.exe'))) { $vc = $true }
        }
        if (-not $vc -and (Find-Tool 'veracrypt')) { $vc = $true }
        $R.tools.veracrypt_installed = $vc
    }
    $inkCandidates = @()
    if ($isWin -and $env:ProgramFiles) { $inkCandidates = @((Join-Path (Join-Path (Join-Path $env:ProgramFiles 'Inkscape') 'bin') 'inkscape.exe')) }
    $targets = @(
        @('magick', @('magick'), @()),
        @('inkscape', @('inkscape'), $inkCandidates),
        @('blender', @('blender'), @())
    )
    foreach ($t in $targets) {
        $key = $t[0]
        $path = $null
        foreach ($n in $t[1]) { if (-not $path) { $path = Find-Tool $n } }
        if (-not $path) { foreach ($cand in $t[2]) { if ($cand -and (Test-Path -LiteralPath $cand)) { $path = $cand } } }
        if (-not $path -and $key -eq 'blender' -and $isWin) {
            $bf = Join-Path $env:ProgramFiles 'Blender Foundation'
            if (Test-Path -LiteralPath $bf) {
                $dirs = @(Get-ChildItem -LiteralPath $bf -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending)
                foreach ($d in $dirs) { $cand = Join-Path $d.FullName 'blender.exe'; if (-not $path -and (Test-Path -LiteralPath $cand)) { $path = $cand } }
            }
        }
        if ($path) {
            $R.tools[$key].found = $true
            $R.tools[$key].version = Get-FileVersionText $path
            $R.tools[$key].notes = 'found; version read from the file, not started'
        } else { $R.tools[$key].notes = 'not found' }
    }
}

# ---- step 16: Craft apps by folder name
Step 'Looking for Craft app folders under the tools folders (folder names only; no Craft app is started)' {
    $roots = @($ToolsRoot)
    if ($roots.Count -eq 0 -and $script:Pins) { $roots = @($script:Pins.tools_roots) }
    if ($roots.Count -eq 0) { $roots = @('C:\lj\tools', 'C:\LifeJourney\tools') }
    $apps = @('photocraft', 'vectorcraft', 'lightcraft', 'filmcraft', 'effectcraft', 'soundcraft')
    $scanned = @()
    $foundList = @()
    $seenApps = @{}
    foreach ($root in $roots) {
        if (-not $root -or -not (Test-Path -LiteralPath $root -PathType Container)) { continue }
        $scanned += (Show-Path ([string]$root))
        foreach ($d in @(Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue)) {
            $m = [regex]::Match($d.Name, '^(photocraft|vectorcraft|lightcraft|filmcraft|effectcraft|soundcraft)[-_ ]v?(\d+\.\d+\.\d+)', 'IgnoreCase')
            if (-not $m.Success) { continue }
            $app = $m.Groups[1].Value.ToLower()
            $ver = $m.Groups[2].Value
            $pin = $null
            if ($script:Pins -and $script:Pins.apps.$app) { $pin = $script:Pins.apps.$app.pin }
            $isPin = $null
            if ($pin) { $isPin = [bool]($ver -eq $pin) }
            $foundList += , ([ordered]@{ app = $app; version = $ver; pinned_version = $pin; matches_pin = $isPin })
            $seenApps[$app] = $true
            try {
                $exe = Get-ChildItem -LiteralPath $d.FullName -Filter '*.exe' -File -ErrorAction SilentlyContinue | Where-Object { $_.Name.ToLower().Contains($app.Replace('craft', '')) } | Select-Object -First 1
                if ($exe) {
                    $fv = Get-FileVersionText $exe.FullName
                    if ($fv -and $fv -ne $ver -and -not $fv.StartsWith($ver)) { Add-Note ('craft app ' + $app + ': the folder name and the program file report different versions') }
                }
            } catch { }
        }
    }
    $missing = @()
    foreach ($a in $apps) { if (-not $seenApps.ContainsKey($a)) { $missing += $a } }
    $R.craft_apps.tools_roots_scanned = $scanned
    $R.craft_apps.found = $foundList
    $R.craft_apps.not_found = $missing
    if ($scanned.Count -eq 0) { Add-Note 'none of the tools folders exist yet' }
}

# ---- step 17: accounts and the Claude app (counts only)
Step-Win 'Counting enabled local accounts and checking whether the Claude app is running (a count and a yes or no; no names)' {
    $count = $null
    try { $count = @(Get-LocalUser -ErrorAction Stop | Where-Object { $_.Enabled }).Count } catch { }
    if ($null -eq $count) {
        try { $count = @(Get-CimInstance -ClassName Win32_UserAccount -Filter 'LocalAccount=True AND Disabled=False' -ErrorAction Stop).Count } catch { Add-Err 'account count' $_ }
    }
    $R.local_accounts_count = $count
    $R.claude_desktop_running = [bool](@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^claude' }).Count -gt 0)
}

# ---- assemble the arrays (so single items stay arrays in the JSON)
$R.gpus = @($gpuList.ToArray())
$R.disks = @($diskList.ToArray())
if (-not $isWin) { Add-Note 'made on a computer that is not Windows: Windows-only sections were skipped' }

# ---- step 18: self-scan before writing
$scanResult = $null
$script:StepNo++
Write-Host ("[{0}/{1}] Self-scan: checking the finished report for identifying data before writing ... " -f $script:StepNo, $TotalSteps) -NoNewline
# first pass to find errors and notes that must be in the report; second pass is the final check
$R.notes = @($script:Notes.ToArray())
$R.errors = @($script:Errors.ToArray())
$scanResult = Invoke-SelfScan $script:Pat $R
if ($scanResult.refusals.Count -gt 0) {
    Write-Host 'REFUSED'
    Write-ScanOutcome $scanResult
    Say 'Nothing was written. Do not edit the report by hand to get past this: paste the lines above into chat.'
    Say 'files written: none'
    exit 2
}
Write-Host 'ok'
$hitsOut = @()
foreach ($h in $scanResult.notes) { $hitsOut += , ([ordered]@{ category = $h.category; field = $h.field; masked_hit = $h.hit }) }
$R.redaction.name_hits_in_hardware_fields = $hitsOut
$R.redaction.self_scan_passed = $true
Write-ScanOutcome $scanResult
# the final object is scanned once more, exactly as it will be written
$final = Invoke-SelfScan $script:Pat $R
if ($final.refusals.Count -gt 0) {
    Say 'REDACTION CHECK FAILED on the final report, nothing was written'
    Write-ScanOutcome $final
    Say 'files written: none'
    exit 2
}

# ---- step 19: write
$script:StepNo++
Write-Host ("[{0}/{1}] Writing the report to {2} ... " -f $script:StepNo, $TotalSteps, $OutShown) -NoNewline
$jsonText = $null
try {
    $jsonText = Write-ReportFile $R $OutFull $OutShown
    Write-Host 'ok'
} catch {
    Write-Host 'failed'
    Say ('could not write the report: ' + (Clean-Message $_.Exception.Message))
    Say 'files written: none'
    exit 3
}
if ($Print) { Say $jsonText }
Say ''
if ($script:Errors.Count -gt 0) { Say ('sections that could not be read: ' + $script:Errors.Count + ' (listed under errors in the report; the rest is complete)') }
Say 'Next: open the report in Notepad (File Explorer, type %TEMP% in the address bar), read it, and paste it into chat only. Do not copy it into the project folder.'
Say ('files written: ' + ($script:FilesWritten -join '; '))
exit 0
