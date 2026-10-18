# Run from inside the archive folder. Writes ..\SHA256SUMS.txt in sha256sum format (lowercase hash, space, asterisk, relative path with /), LF line endings, no BOM.
$root = (Get-Location).ProviderPath
$lines = Get-ChildItem -Recurse -File -LiteralPath $root | ForEach-Object {
    $h = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
    $rel = $_.FullName.Substring($root.Length).TrimStart('\','/').Replace('\','/')
    "$h *$rel"
}
$out = Join-Path (Split-Path $root -Parent) 'SHA256SUMS.txt'
[System.IO.File]::WriteAllText($out, (($lines | Sort-Object) -join "`n") + "`n", (New-Object System.Text.UTF8Encoding $false))
"wrote $out ($($lines.Count) files)"
