# Check a folder (or a burned disc) against a sha256sum-format list made by mk_manifest.ps1.
# Run from the folder to check:  cd E:\   then   powershell -ExecutionPolicy Bypass -File verify_manifest.ps1 -Manifest D:\LifeJourney\SHA256SUMS.txt
# Prints one line per problem and a summary. PowerShell string comparison with -ne ignores case, so upper- and lower-case hex both match.
param([Parameter(Mandatory = $true)][string]$Manifest)
$bad = 0; $n = 0
Get-Content -LiteralPath $Manifest -Encoding UTF8 | Where-Object { $_.Trim() } | ForEach-Object {
    $parts = $_ -split ' \*', 2
    $want = $parts[0]; $rel = $parts[1].Replace('/', [IO.Path]::DirectorySeparatorChar)
    $n++
    if (-not (Test-Path -LiteralPath $rel -PathType Leaf)) { "MISSING  $rel"; $bad++ }
    elseif ((Get-FileHash -Algorithm SHA256 -LiteralPath $rel).Hash -ne $want) { "MISMATCH $rel"; $bad++ }
}
"checked $n files, $bad problems"
