#!/usr/bin/env python3
"""build_guide.py: write MAKER-CRAFT-ZIPS.md from release_assets.json (so no file name, size or hash is ever typed by hand).

USAGE  python3 -I spikes/sp1_craft_cli/build_guide.py [--out FILE]
The guide text lives in this file; the table and the PowerShell lists are filled from the asset table. Change a pin in config.json, run --sums-only,
run this, then check_guide.py. check_guide.py reads the written guide again and compares every name, size and hash with release_assets.json on its own.
ASCII only: the guide is pasted into Windows PowerShell 5.1, which reads text as ANSI.
"""
import argparse
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "drivers"))
import sp1_lib as L  # noqa: E402

APPS = ["photocraft", "vectorcraft", "lightcraft", "filmcraft", "effectcraft"]
TITLES = {"photocraft": "PhotoCraft", "vectorcraft": "VectorCraft", "lightcraft": "LightCraft", "filmcraft": "FilmCraft", "effectcraft": "EffectCraft"}

TEMPLATE = r"""# Craft apps on your PC: download, check, unzip and test (Saturday 24 October)

*For the maker. Written Mon 19 Oct 2026 by the build team; the table below is filled in by a script from the release lists on GitHub, so no name or number in it was typed by hand. Not yet run on a real Windows PC: every line that asks Windows a question is UNVERIFIED until you run it.*

This takes about 90 minutes, and most of that is waiting for downloads. You will download five small programs (the Craft apps), check that each file is exactly the one GitHub published, unzip them into one folder, and run a five-minute test of each. Nothing is installed. Nothing leaves your PC.

## What this is and what it never does

- It uses the **portable zip** of each app. A portable app keeps its own settings and working files in its own folder, so it leaves fewer traces on the PC.
- It **never installs** anything. Do not run the `.msi` files. **Never install or open the ArtCraft Launcher.** It updates the apps on its own, and the plan needs the versions to stay fixed.
- It uses **test files only**: the small made-up files in the project folder. **No family photo, scan, video or letter goes anywhere near these tests.** That comes later, after the process is locked.
- Windows PowerShell 5.1 (the blue window that comes with Windows) and PowerShell 7 both work. The grey boxes below are lines to paste. Each one says what it does first. Some only **read** and print; the boxes marked "this one writes" create folders or unzip files, and nothing else.
- If any line prints something you do not understand, **stop and paste it in chat**. A pause costs nothing.

**Which versions.** These are the versions the plan pinned (decision W-22): PhotoCraft @@V_photocraft@@, VectorCraft @@V_vectorcraft@@, LightCraft @@V_lightcraft@@, FilmCraft @@V_filmcraft@@ (with @@V_filmcraft_fb@@ as the fallback), EffectCraft @@V_effectcraft@@. If the orchestrator names a newer version in chat before you start, use that one instead and ask for its table. The pins are frozen on Sunday 25 October, after your tests.

**Space.** The five zips are about @@TOTAL_MB@@ MB. Keep at least 3 GB free on drive C: to be safe (the unzipped size is not known yet).

## The five files

All five are the **windows-x64-portable.zip** file of the release. Most PCs are x64. (If your PC inventory said ARM, stop and tell me: those need a different file.) Do not pick the `.msi`, the `x86` file or the `arm64` file.

| App | Version | File to download | Size (MB) | SHA-256 (what the file must match) |
|---|---|---|---|---|
@@FILE_TABLE@@

Download link for each file: `https://github.com/storytold/<app>/releases/download/<version>/<file>`. For example, the first one is
`@@EXAMPLE_URL@@`. Paste a link into your browser's address bar and the download starts. Or open the release page, `https://github.com/storytold/<app>/releases/tag/<version>` (for PhotoCraft that is `https://github.com/storytold/photocraft/releases/tag/@@V_photocraft@@`), scroll to "Assets" and click the file there. The page also lists installers and other builds; ignore them. (The fallback FilmCraft @@V_filmcraft_fb@@ is only needed if @@V_filmcraft@@ fails its test; skip it for now.)

## Step 1. Make the folders (this one writes)

This creates three empty folders and prints their names. `C:\lj\tools` is where the apps will live, `C:\lj\dl` holds the downloaded zips, `C:\lj\at` holds the test files.

<!-- lj:mode=setup -->
```powershell
New-Item -ItemType Directory -Force -Path 'C:\lj\tools', 'C:\lj\dl', 'C:\lj\at' | Out-Null
'folders ready: C:\lj\tools   C:\lj\dl   C:\lj\at'
```

## Step 2. Download the five zips

Use your browser and the five links above. When a download finishes, leave the file where the browser put it (normally the Downloads folder). Then move the zips into `C:\lj\dl`. If you prefer, drag them in File Explorer instead.

<!-- lj:mode=setup -->
```powershell
# This one writes: it moves the five zips from your Downloads folder to C:\lj\dl and prints only file names.
$names = @(
@@NAME_LIST@@
)
foreach ($n in $names) {
    $src = Join-Path $env:USERPROFILE ('Downloads\' + $n)
    if (Test-Path -LiteralPath $src) {
        try {
            Move-Item -LiteralPath $src -Destination 'C:\lj\dl\' -Force -ErrorAction Stop
            'moved          ' + $n
        } catch {
            'could not move:  ' + $n
        }
    } else {
        'not in Downloads: ' + $n
    }
}
```

If a line says "not in Downloads", the browser saved it somewhere else or you have not downloaded it yet. If a line says "could not move", the file is still in Downloads (for example because it is still downloading or `C:\lj\dl` is missing). Move it by hand. This box prints file names only, never a folder path.

## Step 3. Check each zip against the table

This only **reads**. It computes the SHA-256 fingerprint of each zip and compares it with the table above. It prints `OK`, `MISSING` or `MISMATCH`, then the file name. A mismatch also prints the fingerprint it got (a fingerprint is just a long number, safe to paste).

<!-- lj:mode=readonly -->
```powershell
$want = [ordered]@{
@@WANT_LINES@@
}
foreach ($name in $want.Keys) {
    $f = Join-Path 'C:\lj\dl' $name
    if (-not (Test-Path -LiteralPath $f)) { 'MISSING   ' + $name; continue }
    $got = (Get-FileHash -Algorithm SHA256 -LiteralPath $f).Hash.ToLower()
    if ($got -eq $want[$name]) { 'OK        ' + $name } else { 'MISMATCH  ' + $name + '   got ' + $got }
}
```

What the answers mean:

- **OK** for all five: the files are complete and are the ones GitHub published. (This shows the file was not damaged or swapped on the way. It cannot show who published it, because the list and the file come from the same place. For FilmCraft and EffectCraft the same fingerprints were also read on a different day, and they matched.)
- **MISMATCH**: do not open that zip. Delete it, download it again, and run this step again. If it mismatches twice, paste the line in chat and wait.
- **MISSING**: you have not downloaded or moved that file yet.

## Step 4. Unzip into C:\lj\tools (this one writes)

Each app goes into its own folder named after the app and its version, for example `C:\lj\tools\filmcraft-@@V_filmcraft@@`. The PC inventory script looks for folders named exactly like this. If a folder already exists the line leaves it alone.

<!-- lj:mode=setup -->
```powershell
# This one writes: it unblocks each zip (removes the "downloaded from the internet" mark from that one file) and unzips it.
$apps = @(
@@APP_LINES@@
)
foreach ($a in $apps) {
    $zip  = 'C:\lj\dl\' + $a[0] + '-' + $a[2] + '-windows-x64-portable.zip'
    $dest = 'C:\lj\tools\' + $a[0] + '-' + $a[1]
    if (Test-Path -LiteralPath $dest) { 'exists, left alone: ' + $dest; continue }
    if (-not (Test-Path -LiteralPath $zip)) { 'zip not found:       ' + $zip; continue }
    Unblock-File -LiteralPath $zip
    Expand-Archive -LiteralPath $zip -DestinationPath $dest
    'unzipped to          ' + $dest
}
```

Now look at what came out. This only **reads** and prints each program file's place inside `C:\lj\tools`:

<!-- lj:mode=readonly -->
```powershell
$root = 'C:\lj\tools\'
Get-ChildItem -LiteralPath $root -Recurse -Filter '*.exe' -File | ForEach-Object { $_.FullName.Substring($root.Length) }
```

You should see two programs per app, for example `filmcraft.exe` and `filmcraft-cli.exe`. If every program sits inside one extra folder (for example `filmcraft-@@V_filmcraft@@\filmcraft-@@V_filmcraft@@\filmcraft.exe`), that is fine; just use the longer path below.

## Step 5. The portable marker (this one writes)

A portable app looks for a small empty file called `portable.txt` next to its program. FilmCraft and EffectCraft ship with it. This line adds it where it is missing and prints what it did. An app that does not know the file simply ignores it.

<!-- lj:mode=setup -->
```powershell
$apps = 'photocraft', 'vectorcraft', 'lightcraft', 'filmcraft', 'effectcraft'
foreach ($a in $apps) {
    foreach ($d in (Get-ChildItem -LiteralPath 'C:\lj\tools' -Directory -Filter ($a + '-*'))) {
        $exe = Get-ChildItem -LiteralPath $d.FullName -Recurse -Filter ($a + '.exe') -File | Select-Object -First 1
        if (-not $exe) { 'no ' + $a + '.exe found in ' + $d.Name; continue }
        $marker = Join-Path $exe.DirectoryName 'portable.txt'
        if (Test-Path -LiteralPath $marker) { 'already there: portable.txt for ' + $d.Name }
        else { New-Item -ItemType File -Path $marker | Out-Null; 'created:       portable.txt for ' + $d.Name }
    }
}
```

## Step 6. Copy the test files into C:\lj\at (this one writes)

The test files are in the project folder you downloaded for the PC inventory (the README for that step suggested `C:\lj\project`). If yours is elsewhere, change the first line.

<!-- lj:mode=setup -->
```powershell
$proj = 'C:\lj\project'
$src  = Join-Path $proj 'research\craft-visual-fixtures'
$files = 'at-layers.ora', 'at-rig.svg', 'faded-print-a.lcpreset', 'at-lightcraft-steps.jsonl', 'check_ids.py'
foreach ($n in $files) {
    $f = Join-Path $src $n
    if (Test-Path -LiteralPath $f) { Copy-Item -LiteralPath $f -Destination 'C:\lj\at\' -Force; 'copied    ' + $n }
    else { 'NOT FOUND ' + $n + '   (look in the project folder, under research\craft-visual-fixtures)' }
}
```

The LightCraft test also needs one ordinary JPEG that is **yours and not a family photo** (a picture of a shelf or a plant will do). Put it at `C:\lj\at\print.jpg` and two or three more in `C:\lj\at\prints\`. The checker `check_ids.py` needs Python 3 (the PC inventory said whether you have it).

## Step 7. The five-minute tests

Do **one app at a time**, then do the "where did it write" step below for that app. The exact steps already exist; they are not repeated here, so they cannot drift apart:

| App | Where the steps are |
|---|---|
| PhotoCraft | `playbooks/craft-visual.md`, Exercise 1, step 3 |
| VectorCraft | `playbooks/craft-visual.md`, Exercise 1, step 4 |
| LightCraft | `playbooks/craft-visual.md`, Exercise 1, step 5 |
| FilmCraft | `playbooks/craft-motion.md`, Exercise 1, and the checklist "B. Five-minute acceptance test (FilmCraft, Windows)" |
| EffectCraft | `playbooks/craft-motion.md`, Exercise 8, steps 1 to 4 (the title, font and alpha check) |

Those playbooks were written before this guide and name other folders (`C:\Program Files\...` or `C:\LifeJourney\tools\...`). **Use the folder from Step 4 in their place**, for example `C:\lj\tools\filmcraft-@@V_filmcraft@@` instead of `C:\LifeJourney\tools\filmcraft-v0.9.0`.

Open each program from its own folder in File Explorer by double-clicking the program file (not from the Start menu, and never from the Launcher). Watch Task Manager (Ctrl+Shift+Esc) for the memory it uses. The first time you open each one, Windows may show a blue box, "Windows protected your PC". That is expected for these five programs; what you may do about it is in the last section, "If something goes wrong".

**If a window flashes and closes** (the program starts and exits at once), try the three graphics fallbacks, one after the other, and write down which one worked. Open a PowerShell window in the app's folder first. For FilmCraft:

<!-- lj:mode=setup -->
```powershell
$env:WGPU_BACKEND = 'vulkan'; .\filmcraft.exe
```

then, if that also closes at once:

<!-- lj:mode=setup -->
```powershell
$env:WGPU_BACKEND = 'dx12'; .\filmcraft.exe
```

and last:

<!-- lj:mode=setup -->
```powershell
.\filmcraft.exe --graphics software
```

For EffectCraft the first of these (`$env:WGPU_BACKEND = 'vulkan'; .\effectcraft.exe`) is the one to try: the DirectX 12 mode is a known failure there. (Setting `$env:WGPU_BACKEND` lasts only for that PowerShell window.)

## What to write down for each app

One line per app, in chat or in your own notes. Never in the project folder.

1. The version printed by the command-line program (the lines below print it), and that you used the **portable zip**.
2. **Signed or not.** The lines below print `Valid`, `NotSigned` or another word for each program.
3. Each step of the five-minute test: **pass or fail**, and any warning **word for word**.
4. The most memory you saw in Task Manager (MB or GB).
5. Which graphics setting worked, if you needed one.
6. The two "where did it write" outputs below.

This prints the version of each command-line program. It starts each one with `--version`, which only prints a line and quits:

<!-- lj:mode=readonly -->
```powershell
$root = 'C:\lj\tools\'
Get-ChildItem -LiteralPath $root -Recurse -Filter '*-cli.exe' -File | ForEach-Object {
    $_.Name + '   ' + (& $_.FullName --version 2>&1 | Select-Object -First 1)
}
```

This prints whether each program file is digitally signed (it prints the file name and one word):

<!-- lj:mode=readonly -->
```powershell
$root = 'C:\lj\tools\'
Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object { $_.Name -in 'photocraft.exe', 'vectorcraft.exe', 'lightcraft.exe', 'filmcraft.exe', 'effectcraft.exe' } | ForEach-Object {
    $_.Name + '   ' + (Get-AuthenticodeSignature -LiteralPath $_.FullName).Status
}
```

## Where did it write? (read-only, run it right after each app's test)

Craft apps keep working copies, recovery files and lists of recent files. For a surprise, you and I need to know exactly where each app puts them. These two lines only **read**. They print folder and file names with the start of your own user folder replaced by `%USERPROFILE%`, so the output is safe to paste. Please run both **within an hour of the test**, once per app, and paste both outputs in chat with the app's name above them.

Line 1: the folders under `%APPDATA%` and `%LOCALAPPDATA%` that changed in the last hour, down to three levels (up to 80 lines for each of the two; it may take a minute; the Temp folder is left out because every program touches it; any folder name that contains an `@`, such as an e-mail address, is printed as `<redacted>`):

<!-- lj:mode=readonly lj:kind=where_appdata -->
```powershell
$since = (Get-Date).AddHours(-1); foreach ($r in @(@('%USERPROFILE%\AppData\Roaming', $env:APPDATA), @('%USERPROFILE%\AppData\Local', $env:LOCALAPPDATA))) { Get-ChildItem -LiteralPath $r[1] -Directory -Recurse -Depth 2 -Force -ErrorAction SilentlyContinue | ForEach-Object { $rel = $_.FullName.Substring($r[1].Length) -replace '[^\\/]*@[^\\/]*', '<redacted>'; if ($_.LastWriteTime -gt $since -and $rel -notmatch '^[\\/]Temp([\\/]|$)') { $r[0] + $rel } } | Select-Object -First 80 }
```

Line 2: the files under the app's own folder that changed in the last hour (programs and libraries are left out). **Change the folder on the first line to the app you just tested**:

<!-- lj:mode=readonly lj:kind=where_appfolder -->
```powershell
$app = 'C:\lj\tools\filmcraft-@@V_filmcraft@@'; $since = (Get-Date).AddHours(-1); Get-ChildItem -LiteralPath $app -File -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $since -and $_.Extension -notin '.exe', '.dll' } | ForEach-Object { '<app folder>' + $_.FullName.Substring($app.Length) } | Select-Object -First 80
```

An empty answer is an answer: it means the app wrote nothing there. Read the lines before you paste. If one shows a name that is yours or your family's, delete that line.

## If something goes wrong

- **A MISMATCH twice, a missing file, or a message you do not understand:** stop and paste the exact text in chat. Do not try to fix it.
- **Windows shows a blue box, "Windows protected your PC" (SmartScreen), when you open one of the five programs:** this is expected. The programs are unsigned alpha software (the signature lines under "What to write down" print `NotSigned`, and that is normal here, not a fault), and files that came from the internet carry a "from the internet" mark. For these five programs only you may click **More info** and then **Run anyway**, and only when all three are true: the file is one of the five programs inside `C:\lj\tools`; Step 3 printed `OK` for the zip it came from; and you unzipped that zip yourself in Step 4. Write down which program you did it for. For any other file, or if the box looks different from this, stop and paste what it says.
- **The antivirus removes, quarantines or blocks a file:** stop. Do not turn the antivirus off, do not restore the file and do not click past the warning. Paste what it says; we decide together.
- **A group policy blocks scripts or the zip** (a work or school PC): stop and change nothing.
- **An app crashes:** that is a result, not your mistake. Write down the exact words. When you report a bug anywhere, use the test files only (a report can be relayed to a public page).

## When you are done

Paste in chat, in this order: the Step 3 lines (five `OK`), the version lines, the signature lines, your pass or fail notes for each app, and the "where did it write" outputs. Then the plan can freeze the versions on Sunday 25 October. Delete nothing yet; `C:\lj\dl` can stay.

*What is verified and what is not: the table and every file name come from GitHub's own lists and match them (checked by `check_guide.py`). The PowerShell lines were parsed with PowerShell 7 and checked against the Windows PowerShell 5.1 rules by a script; the hash check and the "where did it write" lines were also run on Linux against made-up files. None has run on Windows yet. Where the zips put their files, whether each app honours `portable.txt`, and what each app writes are all UNVERIFIED until your first run; your pasted output is the evidence.*
"""


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(HERE, "MAKER-CRAFT-ZIPS.md"))
    a = ap.parse_args(argv)
    assets = L.load_assets()
    want, rows, names, apps = [], [], [], []
    total = 0
    ver = {}
    for app in APPS:
        pin = next(p for p in assets["pins"] if p["app"] == app and p["role"] == "pin")
        z = pin["windows_x64_portable_zip"]
        ver[app] = pin["tag"]
        mb = round(z["bytes"] / 1048576.0, 1)
        total += z["bytes"]
        rows.append("| %s | %s | `%s` | %s | `%s` |" % (TITLES[app], pin["tag"], z["name"], mb, z["sha256"]))
        names.append("    '%s'" % z["name"])
        want.append("    '%s' = '%s'" % (z["name"], z["sha256"]))
        apps.append("    @('%s', '%s', '%s')" % (app, pin["tag"], pin["version"]))
    fb = next(p for p in assets["pins"] if p["role"] == "fallback")
    fz = fb["windows_x64_portable_zip"]
    rows.append("| FilmCraft (fallback, only if %s fails) | %s | `%s` | %s | `%s` |" % (ver["filmcraft"], fb["tag"], fz["name"], round(fz["bytes"] / 1048576.0, 1), fz["sha256"]))
    text = TEMPLATE
    for app in APPS:
        text = text.replace("@@V_%s@@" % app, ver[app])
    text = text.replace("@@V_filmcraft_fb@@", fb["tag"])
    text = text.replace("@@FILE_TABLE@@", "\n".join(rows))
    text = text.replace("@@NAME_LIST@@", ",\n".join(names))
    text = text.replace("@@WANT_LINES@@", "\n".join(want))
    text = text.replace("@@APP_LINES@@", ",\n".join(apps))
    text = text.replace("@@TOTAL_MB@@", str(int(round(total / 1048576.0, -1))))
    first = next(p for p in assets["pins"] if p["app"] == "photocraft")
    text = text.replace("@@EXAMPLE_URL@@", L.asset_url("photocraft", first["tag"], first["windows_x64_portable_zip"]["name"]).replace(L.RELEASE_BASE, "https://github.com/storytold"))
    if "@@" in text:
        print("ERROR: an unfilled placeholder is left in the guide")
        return 2
    text.encode("ascii")  # raises if a non-ASCII character slipped in
    with open(a.out, "w", encoding="ascii", newline="\n") as f:
        f.write(text)
    print("wrote %s (%d lines)" % (L.rel(a.out), text.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
