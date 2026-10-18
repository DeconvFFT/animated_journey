# ArtCraft Visual Apps as Refinement Layers

> **Status, 2026-10-18.** Built from the research notes for track `craft-visual`. Nothing in this playbook has been run on a Windows PC yet. Steps marked **Untested** are read from code, tests and docs. Exercise 1 is how we turn them into facts. Evidence tags, as in the notes: **[T]** a named test in the repo covers it, **[C]** code or docs only, **[V]** vendor claim, **[U]** unverified. Open items are marked **TODO(research)**.

**Reconciled with DECISIONS.md (2026-10-18). The register wins (D-21).** Pins are the register's defaults, frozen Sun 25 Oct: PhotoCraft v0.10.0, VectorCraft v0.13.1, LightCraft v0.9.1, with no upgrade mid-chapter and no Launcher ever (W-22, D-12). A Craft app touches only a copy in `work\`, never holds the only copy of anything, and is never a step in the week before the premiere (D-12). Her photos and scans stay on the PC, inside the VeraCrypt container, and every photo set is `cloud: none` unless the maker raises it (D-15, W-24, W-25). Real family material enters after the L1 process lock, Sat 14 Nov, with covert collection from Sun 15 Nov (D-13); until then every exercise uses the maker's own prints or stand-ins. The scan tool is whichever wins the ten-print pilot, decided by Sun 15 Nov (W-27, O-23). Only-me: the maker alone judges every touch-up and every hard chapter (D-03, D-04). Each Decision below carries its register status: decided (`DECISIONS.md` Table 1), default with a decide-by date (Table 2), or open for the maker (Table 3).

## Why this matters for our life journey

Claude and the agent team will do most of the heavy work. They will generate layered files, build the animation art, write the scripts and do the rendering. But some things still need a human hand. A speck of dust on a print needs a touch. A hand-drawn sun needs to sit a little higher. Forty faded prints need one colour cast removed, without losing the warmth of their decade. Those quick, human touches are what the three ArtCraft apps are for:

- **PhotoCraft** for layered pictures: restored stills, title layers, colour tints.
- **VectorCraft** for vector drawings: the SVG art we will animate.
- **LightCraft** for developing and grading scans, including the batch of about 300 faded prints.

All three are free, open source and in early alpha. The whole suite is 18 days old. So the apps are good quick hands, but the project must never depend on just one of them. Each app works through a narrow, checkable hand-off, and each one has a fallback.

VectorCraft's trace presets (Sketched Art, Line Art and Black and White Logo) turn a scan of her handwriting, a recipe card or a letterhead into SVG lettering. Her hand is used only for words she actually wrote (the Card A slips, a recipe card); chapter titles and cards of the maker's own words are in the maker's hand (W-35, W-38). LightCraft presets are authored and named per album batch, from the measured paper-border cast (`border_rgb`), so each era keeps its own colour instead of every print getting one uniform restored look (charter principle 3; W-27, W-39).

Her photos and scans stay on your PC for these steps, inside the VeraCrypt container. The cloud container never receives a full-size family photo or scan (D-15, W-24). A `preview` proxy of about 768 px goes there only after the account's model-improvement setting is off, and only if the maker raised that set's `cloud` level.

## Core principles

1. **Three narrow hand-offs, nothing more.** Stills go out and come back as OpenRaster files (`.ora`). Animation art goes out and comes back as SVG with stable names. Scan batches run through a LightCraft script and a preset file. Anything else is an experiment, not part of the pipeline.
2. **Claude makes the start, you make the touch.** Claude generates the file with clear, stable names. You open a copy, make the human fix, and save. Claude then reads the result back and checks it.
3. **Never save over an original.** Work on a copy in a `work` folder, and mark the originals read-only too. Do not count on the app to refuse a save over a read-only file. The v0.10.0 release notes list that guard (#6643) and "ask before overwriting a file another app changed" (#6652); treat both as vendor claims until Exercise 6 shows them (research R3d, [65]).
4. **Test first, then pin the version.** A build that passes the five-minute tests is the only build you use until you decide, on purpose, to change it.
5. **Let the checkers vote too.** Run the SVG id checker after every save. Compare the paper-border colour numbers in the scan pilot. Your eye matters, but it is one vote among several.
6. **Keep her material private, traces included.** Nothing personal goes to a cloud service, a cloud photo library, a synced folder or a group chat. The apps leave traces on the PC, so clean them up (see Pitfalls).
7. **Switch off what you are not using.** Auto-update, face recognition, model downloads, network features and control ports stay off unless you are using them at that moment.
8. **Label anything restored or generated.** When an app or a script changes a real photo, the hand-off log says so. This is charter principle 4, and it follows the labelling rules in `playbooks/ai-imagery.md`.
9. **Stay inside the Craft boundary (D-12).** A Craft app may touch only a copy in a `work\` folder, a chapter whose spec and OTIO are in the repo, or a title whose SVG fallback exists. It is never the only writer or reader of a format, never the holder of the only copy of anything, and never a step in the week before the premiere (Sat 20 to Sat 27 Feb 2027).

## How to do it, step by step

### Step 0. Make the folders

Create these on the PC. They match the research recipes, so use the same names.

- `C:\lj\at\` for the test files in Exercise 1.
- `C:\lj\ch01\in`, `C:\lj\ch01\work` and `C:\lj\ch01\out` for one chapter. Repeat for each chapter (`ch02`, `ch03`, and so on).
- `C:\lj\lib\` for the LightCraft library. It must be on a local NTFS disk. [36]
- `D:\scans\raw\` for the scanned originals and `D:\scans\out\` for exports. The drive letter is an example. Use a local disk, not a network share, and keep family originals inside the mounted VeraCrypt container (W-25), dismounted before you leave the desk.
- A hand-off log file (Template A). Keep it on the PC. It uses shot ids and person IDs, never names or original file names, and it is committed to the private repo at the end of each session (D-14).

None of these folders should sit inside a cloud-synced folder, such as a synced Pictures folder.

### Step 1. Record what you have

1. Find each command-line program and ask it for its version. The programs are not on the PATH, so use the full path. The recipes assume the MSI default folders. VectorCraft's MSI default is `C:\Program Files\VectorCraft\vectorcraft-cli.exe`, which is not on the PATH. That path is read from `docs/mcp.md`, so confirm it on the maker's PC in Exercise 1. [11][25][29][41]

```powershell
# Untested. Adjust the folders if you used the portable zip.
& "C:\Program Files\PhotoCraft\photocraft-cli.exe" --version
& "C:\Program Files\LightCraft\lightcraft-cli.exe" --version
& "C:\Program Files\VectorCraft\vectorcraft-cli.exe" --version
```

2. Write down each app's version, whether you installed the MSI or the portable zip, and whether the main program is signed. To check the signature, right-click the program, choose Properties, then open the Digital Signatures tab. The READMEs say the installers are signed. The vendor's own gap list says the signing material was not obtained. Expect Windows warnings, and write down what you actually see. [13]
3. Write down your PC's memory, graphics card and free disk space. None of the three apps has been measured on Windows at low memory. Run the read-only PowerShell block below (from research R2) and paste its output into Template B. Then answer by hand: Launcher or website; MSI or zip; stock Windows or a stripped image (PhotoCraft and its CLI fail to start without `Windows.Data.Pdf.dll`, #6249 [70]); scanner model; whether she shares the PC or the room (O-03, still pending).
4. Use Windows 10 or later and the 64-bit builds. Do not use the 32-bit builds, because PhotoCraft caps one decode allocation at 2 GiB on 32-bit systems. LightCraft states no minimum Windows version. [6][11][29][41]

**Read-only block for item 3** (research R2; not run in the container; it prints to the screen and sends nothing anywhere):

```powershell
# Versions and install type
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -match 'craft' } | Select-Object DisplayName, DisplayVersion, InstallLocation
foreach ($a in 'PhotoCraft','VectorCraft','LightCraft') {
  $cli = "$env:ProgramFiles\$a\$($a.ToLower())-cli.exe"
  if (Test-Path $cli) { "$a CLI: " + (& $cli --version) } else { "$a CLI not at $cli (portable or other folder?)" }
}
# Windows and hardware
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, @{n='RAM_GB';e={[math]::Round($_.TotalPhysicalMemory/1GB,1)}}
Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{n='Free_GB';e={[math]::Round($_.Free/1GB,1)}}
Test-Path "$env:SystemRoot\System32\Windows.Data.Pdf.dll"
```

### Step 2. Choose the version and pin it

- **Do not install PhotoCraft from the website.** Its page shows version 0.7.0. That build has ORA support but not the guard against overwriting an ORA with less content. [43][44]
- **Pick the newest tag on the day you pass the five-minute test, but no later than 2026-10-25.** The provisional pins are PhotoCraft v0.10.0, VectorCraft v0.13.1 and LightCraft v0.9.1, the newest tags as of 2026-10-18. Each main branch had 300 to 600 newer commits at the first pass, including save-safety and Windows fixes, so check for newer tags before you freeze. [43] These pins are the register's defaults, frozen Sun 25 Oct (W-22).
- **Install the portable zip.** It keeps program data beside the program, which makes traces easier to find and clean (see Pitfalls). [11][29][41]
- **Record the version and the SHA-256 hash of the portable zip.** Download the zip for the pinned tag from `github.com/storytold/<app>/releases/tag/<tag>`, and check its SHA-256 against the `SHA256SUMS.txt` in that same release (`photocraft/docs/releasing.md` line 26; Launcher README). Write both hashes in the log. [11][81]

### Step 3. Keep the Launcher out of production

The Craft Launcher checks each app's GitHub releases and updates the ones you have installed [81]. The Launcher README documents no off switch for updates. **Never install or run the Launcher (D-12).** Download the portable zip for the pinned tag from `github.com/storytold/<app>/releases/tag/<tag>` and check its SHA-256 against the `SHA256SUMS.txt` in that same release (`photocraft/docs/releasing.md` line 26; Launcher README). [11][81]

### Step 4. Set up each app before the first real file

- **PhotoCraft.** Autosave is on by default: every 10 minutes, with recovery on launch. Keep it on. [15] Memory Usage defaults to 8192 MB. On an 8 GB PC, lower it, and keep working canvases around 8.6 megapixels (3600 by 2400 pixels). The only measured baseline is a Mac with an M4 Pro, which is not your PC. [13]
- **VectorCraft.** Nothing to change for the SVG work. The save settings are in Step 7.
- **LightCraft.** For batch runs, set `LIGHTCRAFT_GPU=0`. This keeps the batch on the CPU and avoids graphics-driver risk. The vendor's tests show the CPU and GPU paths agree within 1/255, but the Windows DX12 path is unverified. [37] The memory budget defaults to the smaller of 25 percent of RAM and 1.5 GiB. `LIGHTCRAFT_MEMORY_MB` overrides it. [37] Keep face recognition off. Open Settings, tab **Faces**, and leave **Recognise faces (experimental)** unticked. It is off by default, and the box stays greyed out until a recognition model is installed. If `%APPDATA%\LightCraft\models\settings.json` exists, it should say `"enabled": false`. Do not use **Photo > Detect Faces**: with no detector installed it opens the model terms, so press Escape. In the app, a face-model download starts only after you tick "I accept" in those terms and press OK. Keep the control ports off, because a control-port client can also request a download. Never drop a `.onnx` file on the window, which installs a model. [82]
- **Control ports.** VectorCraft and LightCraft each have a `--control` port with no password. Turn it on only while you are using it, and decline any Windows firewall prompt for it. [26][34]

### Step 5. Run the five-minute acceptance tests

Do Exercise 1. A failed step is a finding. Write it down word for word and tell Claude. Do not fix it by hand, and do not carry on as if it passed.

### Step 6. Stills: the PhotoCraft hand-off

1. **Claude writes the layered file.** The format is OpenRaster (`.ora`), which is a zip of PNG layers plus an XML list of them. PhotoCraft reads and writes layer names, visibility, opacity, blend modes, nested groups, offsets (even off-canvas) and 8-bit or 16-bit colour. It is the only layered format with a third-party check on record. Krita 5.2.9, on 2026-10-09 (run on v0.9.0; not re-run on v0.10.0), matched 32 of 35 files within 3/255. [T][4] Layer names are the pipeline's ids, for example `L10_sky` and `L20_figure`. Claude writes the file with the standard-library script `make_ora.py` in the fixtures folder. Prefer a flat layer list. If you use a `<stack>` group, write `isolation="isolate"` or `"auto"` explicitly: v0.10.0 changed how a group is read when the file declares version 0.0.6 or newer (an omitted `isolation` then means isolate, and only `"auto"` gives pass-through). `make_ora.py` declares 0.0.3, which PhotoCraft v0.9.0 and v0.10.0 both read the old way. Layer locks do not round-trip exactly (#7018), so never encode anything in a lock. [58][70]
2. **What an ORA cannot hold.** Adjustment layers, layer styles, vector masks, live text and non-sRGB colour profiles. If you add one of these and save, PhotoCraft will not overwrite the ORA. It offers a PSD with the same name instead. [T][4]
3. **Copy, then open.** Copy `in\ch01_scene.ora` to `work\`, and open the copy in PhotoCraft. Never edit the original.
4. **Make the touch.** Paint, erase masks, move layers or adjust them. Keep the pipeline's layer names unless Claude tells you to change them.
5. **Save.** If PhotoCraft offers a PSD, accept it. Treat that PSD as PhotoCraft's private working file. The pipeline takes PNG exports from it.
6. **Claude reads it back.** From the command line, Claude reads the layer tree as JSON, makes a flattened PNG, and exports one PNG per layer. [7][8] **Untested.**

**Headless assembly (untested).** Claude can also build the layered file without opening the app, by sending JSON lines to `photocraft-cli serve`. The command names come from the code and the tests, not from a run. [8][9][10]

```powershell
# Untested. Keep the JSON in a here-string piped to the program, not typed inline.
$cli = "C:\Program Files\PhotoCraft\photocraft-cli.exe"
@'
{"id":1,"method":"doc.new","params":{"width":3600,"height":2400,"background":"transparent","depth":16,"resolution":300,"name":"ch01"}}
{"id":2,"method":"doc.place","params":{"path":"L10_sky.png","smartObject":false,"fit":false,"scale":100}}
{"id":3,"method":"engine.execute","params":{"command":"layer.setProps","params":{"name":"L10_sky","opacity":1}}}
{"id":4,"method":"doc.place","params":{"path":"L20_figure.png","smartObject":false,"fit":false,"scale":100}}
{"id":5,"method":"engine.execute","params":{"command":"layer.setProps","params":{"name":"L20_figure","opacity":0.9,"blend":"Multiply"}}}
{"id":6,"method":"doc.save","params":{"path":"ch01_scene.ora"}}
'@ | & $cli serve --automation-read-root C:\lj\ch01\in --automation-write-root C:\lj\ch01\out
```

If an adjustment layer is added before the save, PhotoCraft chooses a PSD target and the ORA is refused. [9]

Rules for `serve` (research R6, [61]):

- Create `C:\lj\ch01\in` and `C:\lj\ch01\out` before you start `serve`. It fails if a root folder is missing (`Dir::open_ambient_dir`).
- Use relative request paths with forward slashes, as the script does (`L10_sky.png`). Backslashes in a relative path are refused. An absolute path is compared case-sensitively after the drive letter, so `C:\LJ\ch01\in\...` is refused, although Windows accepts it.
- `doc.exportLayers` refuses to overwrite a file, so give each run a fresh `dir`.
- Write each root without a trailing backslash in PowerShell 5.1. This is general PowerShell knowledge, not from the sources.

### Step 7. Animation art: the VectorCraft hand-off

1. **Claude writes the SVG source.** Every element that will move gets a unique id. Use letters, digits, `-`, `_` and `.`, start with a letter, and avoid spaces. Pivots go in `data-pivot` and stacking order in `data-z`. The viewBox starts at `0 0 W H`. [20][21][22]
2. **Claude runs a pre-flight.** It converts the SVG to a round-trip copy with `vectorcraft-cli convert`, reads the import warnings, and runs `check_ids.py` on both files. [22][24] **Untested.**
3. **You touch it up.** Open `work\ch01_rig.svg` in VectorCraft. Edit shapes and colours. **Do not rename objects.** In VectorCraft the Layers panel name becomes the id.
4. **Save As, not Export.** Save As SVG with these settings: Styling = Presentation Attributes; Object IDs = Layer Names (never Minimal); Fonts = SVG for live text, or Convert to Outlines for final art; Images = Embed; Decimals = 3; Responsive = off, unless the web page scales the art; Preserve editing = off. [31][22] Export drops hidden objects, so use Save As for any rig with hidden alternates. [22]
5. **Run the checker.** Run `check_ids.py` on the source file and the touched file. Exit code 0 is the gate. Any lost id or changed `data-*` attribute fails it. [22]
6. **Claude re-adds the animation hooks.** Classes, a `<style>` block and the timeline go back in by id and data attribute, because the app does not keep them. Claude then exports the PNG and PDF from the command line. [24] **Untested.**

### Step 8. Scan batches: the LightCraft hand-off

LightCraft runs scans through the same develop pipeline it uses for raw files, but no faded-print test corpus exists yet. [35] So the pilot in Exercise 5 is not optional. It decides the scan tool by Sun 15 Nov (W-27, O-23): borrow a flatbed for the batch, use a phone on a stand for album pages, and buy nothing before the bake-off.

1. **Scan to 16-bit TIFF.** Put the originals in `D:\scans\raw\`. Use the scanner settings from `playbooks/ai-imagery.md`. The register's scan standard (W-27) is: masters as 16-bit TIFF at 600 ppi, fronts and backs at the same sitting (a `back` column in `manifest.csv`), the as-found frame photographed before anything moves and again when it is back, and `L00_asfound` as the first layer of every restored still. Mark the originals read-only.

1a. **Check the strip layout before LightCraft imports anything.** LightCraft refuses a TIFF whose single strip or tile is larger than 128 MiB (134,217,728 bytes), with "decoder limits exceeded". This includes v0.9.1. The issues are #2198 and #1983; the fix, PR #1989, was still open on 2026-10-18 [72]. The limit applies to each strip's compressed size as the file declares it in `StripByteCounts`, not to the decoded image [83]. A 16-bit RGB 8x10 inch scan at 600 ppi is 172.8 MB, so it fails if the scanner writes it as one strip. Before the first import, check one worst-case scan with exiftool: `exiftool -RowsPerStrip -StripByteCounts -Compression -ImageSize -BitsPerSample <file.tif>` (standard tag names; not run in the container). ExifTool may print several strip sizes, so look for the largest. Pass if it is below 134,217,728. Do this before the first album is borrowed, because scanning happens once. If a scan fails, in this order: lower the scan resolution; or set the scanner software to small strips or tiles, if it offers that (TODO(research): we have not found what Epson Scan 2, VueScan, NAPS2 or SilverFast write); or rewrite a copy, never the master, with `magick in.tif -define tiff:rows-per-strip=64 -compress None out.tif`. That define was tested in the container with ImageMagick 6.9.12 (as `convert`), where it split a 108 MB one-strip file into 94 strips [84]. ImageMagick 7 on Windows uses `magick`; that is not tested on Windows. On a 134 MB one-strip input the command aborted in the container (cause not diagnosed), so test with the real worst-case file. LZW or ZIP compression helps only when each strip compresses below the limit, which grainy scans often do not. Put the largest planned scan into the 10-print pilot (Exercise 5).
2. **Claude writes the preset and the script.** The preset is a plain JSON `.lcpreset` file that holds only the settings it changes. The script is a JSON-lines file, which avoids Windows quoting trouble. [33][42]
3. **The script does five things.** It imports the originals with `mode: "add"`, which references them in place. It imports the preset, selects all, applies the preset, and exports 16-bit TIFF and JPEG files with a naming template. Never use `move`, which deletes the source after verification. [34][42]
4. **Run it on your PC with the GPU off.**

```
set LIGHTCRAFT_GPU=0
"C:\Program Files\LightCraft\lightcraft-cli.exe" run --library C:\lj\lib --script C:\lj\steps.jsonl
```

   Every result line must say `"ok": true`. A non-zero exit code is a failure. **Untested** in the container. [34][42]

5. **Pick the colour in the app.** Close the command-line run first. Only one process may use a library at a time. [36] Open the library in LightCraft, sort by date, and select a batch of similar prints. Click a neutral patch of the unprinted paper border with the white-balance picker. Sync those settings to the batch, and nudge colour if needed.
6. **Export again from the same library.** This writes the 16-bit masters (`out\*.tif`) and the JPEGs. Record their checksums. [34][42]
7. **Do not trust the result yet.** LightCraft is the scan tool only after the 10-print pilot against darktable (Exercise 5). [37][53]

### Step 9. Log every hand-off

Every hand-off gets a line in the log (Template A). The log tells us which parts were restored, which were generated and which were touched by hand. It also lets us go back if a version turns out to be wrong.

## Learn-by-doing exercises

### Exercise 1. Install, pin and run the five-minute tests

**Goal.** Know that each app runs on your PC at the version you chose, and write down anything that fails.

**Steps.**
1. Do Steps 1 to 4 for all three apps. Run the read-only block after Step 1, item 3, and paste its output into Template B.
2. Copy these files from the project's fixtures folder (`research/craft-visual-fixtures/` in the project repo) into `C:\lj\at\`: `at-layers.ora`, `at-rig.svg`, `at-lightcraft-steps.jsonl`, `faded-print-a.lcpreset` and `check_ids.py`. Also put one JPEG that **you own** and that is **not** a family photo in `C:\lj\at\print.jpg`, and two or three more such JPEGs in `C:\lj\at\prints\`. The checker is a Python script, so install Python 3 first: install 64-bit Python 3 from python.org and tick "Add python.exe to PATH". Any current 3.x works, because the checker uses only the standard library (general knowledge, not from our sources).
3. **PhotoCraft (about 5 minutes).** Run `--version` and check the Digital Signatures tab. Open `at-layers.ora`. Expect two layers: "Photo" at the bottom, and "Title tint" on top at 60 percent, in Multiply, offset 24,24, with no warning. Set Title tint to 40 percent, add a Curves adjustment layer, and press Save. **Pass:** PhotoCraft refuses to overwrite the ORA and offers a PSD. **Fail:** if it overwrites silently, the build is older than v0.9.0. Stop, and do not use it for ORA work. Then Save As `at-layers-edited.psd`, close, reopen, and check that the layers and the Curves layer are there. Export a PNG. Last, run `photocraft-cli info` and `photocraft-cli convert` on the PSD. [4][7][8]
4. **VectorCraft (about 5 minutes).** Run `vectorcraft-cli --version`. Run `vectorcraft-cli convert at-rig.svg at-rig.rt.svg` and read the import warnings. Expect a warning that a filter was ignored. Run `check_ids.py at-rig.svg at-rig.rt.svg`. **Pass:** no lost ids, and `data-pivot` and `data-z` unchanged. The viewBox changing from `100 50 400 300` to `0 0 400 300` is expected. Open `at-rig.svg`, move the sun a little, and Save As with the Step 7 settings to `at-rig.touchup.svg`. Run the checker again. **Pass** is exit code 0. Then run `vectorcraft-cli run --in at-rig.svg --export at-rig.png --export at-rig.pdf --scale 2`. Both files must open. [22][24] If VectorCraft crashes before its window opens on an Intel UHD 605, start it a second time. The next start skips the adapter that crashed (PR #2298 for issue #2243; untested on that GPU). Record both results. [71]
5. **LightCraft (about 5 minutes).** Run `set LIGHTCRAFT_GPU=0`, then render your JPEG:

```
"C:\Program Files\LightCraft\lightcraft-cli.exe" render C:\lj\at\print.jpg -o C:\lj\at\print.out.jpg --set light.exposure=0.3 --set color.vibrance=25 --size 2048 --quality 92
```

   **Pass:** the file is written, it is brighter, and its long edge is 2048 px. Then run `"C:\Program Files\LightCraft\lightcraft-cli.exe" run --library C:\lj\at\lib --script C:\lj\at\at-lightcraft-steps.jsonl` on the prints folder. Each result line must say `"ok": true`. The script exports a 16-bit TIFF master and a JPEG for each print, so `C:\lj\at\out\` must hold both. Then open LightCraft on the same library, change one photo's white balance, quit, run the export again, and check that the picture changed. Last, start the CLI while the app holds the library. **Expected:** a clear "library in use" error, not corruption. [33][34][36][42]

**Time.** 60 to 90 minutes, including installs. The tests themselves take about 5 minutes each.

**What good looks like.** Three entries in the log, one per app, each with its version and a pass or fail for every step. Every warning is copied word for word. The PhotoCraft save refusal happened. The VectorCraft checker returned 0 after your edit. Every LightCraft result line said `"ok": true`, and each print has a TIFF master and a JPEG in `C:\lj\at\out\`.

### Exercise 2. Round-trip a layered still

**Goal.** Feel where the ORA hand-off holds and where it breaks.

**Steps.**
1. Copy `at-layers.ora` to `work\` and open the copy in PhotoCraft.
2. Change "Title tint" to 40 percent and save. Close and reopen. Check that the change held.
3. Add a Curves layer and save. Note the refusal and the PSD offer, and accept the PSD.
4. Reopen the PSD. Check that the layers and the Curves layer are there.
5. Export a PNG and compare it with what you see on screen.

**Time.** About 45 minutes.

**What good looks like.** You can name each layer. The opacity change survived. The PSD reopens with the Curves layer. You can say, in one sentence, which action turned the hand-off from ORA into PSD.

### Exercise 3. Touch up one SVG and keep its hooks

**Goal.** Move an object in VectorCraft and keep its id and `data-pivot`.

**Steps.**
1. Run `vectorcraft-cli convert` on `at-rig.svg` to a round-trip file, and read the warnings.
2. Open `at-rig.svg` in VectorCraft. Move the sun, change one colour, and do not rename anything.
3. Save As `at-rig.touchup.svg` with the Step 7 settings. Do not use Export.
4. Run `check_ids.py` on the two SVG files.
5. Export PNG and PDF with `vectorcraft-cli run`, and open both.
6. Write down which setting you changed and why.

**Time.** About 60 minutes.

**What good looks like.** The checker returns 0. The sun sits where you moved it. The PNG and PDF open. You can explain each save setting from the log.

### Exercise 4. Grade three of your own non-family prints

**Goal.** Run the scan script end to end on a small batch, and see what a preset does.

**Steps.**
1. Put three JPEG or TIFF images that you own in `C:\lj\at\prints\`. None should be a family photo.
2. Run the script with `LIGHTCRAFT_GPU=0`. Check every result line for `"ok": true`.
3. Open the library in LightCraft. Pick a neutral patch on the border with the white-balance picker. Sync the setting to the other two.
4. Export again. Compare the before and after files side by side. On one output, run the by-hand ImageMagick border line from Exercise 5, step 4, and compare its numbers with the script's. That confirms the by-hand line before Template C relies on it.
5. Open `faded-print-a.lcpreset` in a text editor. List the changes it makes.

**Time.** About 60 to 90 minutes.

**What good looks like.** Every result line says `"ok": true`. The neutral border looks neutral to you. You can list the preset's changes, such as the curve, contrast, saturation and grain, from the settings file rather than from memory.

### Exercise 5. The ten-print pilot: LightCraft against darktable

**Goal.** Choose the scan tool on evidence, not preference.

**Steps.**
1. Practise on ten non-family prints first. Include the largest planned scan, and check its strip layout first (Step 8, item 1a). Use her prints only after the L1 lock (Sat 14 Nov), from Sun 15 Nov, once the rules for handling them are agreed and the log is set up (D-13). Family prints stay on the PC.
2. For each print, process it twice. Once in LightCraft (the preset, then the white-balance pick). Once in darktable, using a style. The darktable command line needs a config folder and a styles database, so set those up in the desktop app first. [53]
3. Export each result as 16-bit TIFF.
4. Measure the mean RGB of the unprinted paper border in each output. Claude's pilot script measures it. For a by-hand check, use ImageMagick: `magick out.tif -crop WxH+X+Y +repage -format "%[fx:mean.r*255] %[fx:mean.g*255] %[fx:mean.b*255]" info:` (general knowledge; confirm it in Exercise 4). Write the numbers down.
5. Score each output by eye, from 1 to 5, for overall colour and for skin tone.
6. Write one decision: which tool, and why, citing the two numbers and the two scores.

**Time.** About 3 to 4 hours, spread over two sessions.

**What good looks like.** A table with ten rows and both tools' numbers. A decision that cites the numbers, not just the scores. A note of any crash, missing step or unclear setting.

### Exercise 6. Break it on purpose

**Goal.** Learn the failure messages before the deadline does.

**Steps.**
1. Mark a test file read-only, open it in an app, and try to save over it. Write down what happens.
2. Open a LightCraft library in the app, then start the CLI on the same library. Write down the message.
3. Open a test document, make an unsaved change, and wait for the 10-minute autosave. Then find the autosave entry. In v0.9.0 and earlier the path is `%APPDATA%\Photocraft\Recovery`, which is the roaming profile (#5648). From v0.10.0 the documented Windows path is `%LOCALAPPDATA%\Photocraft\Recovery`, and v0.10.0 moves autosaves left by earlier versions to that folder at startup, so check both folders (`docs/control-protocol.md` line 249; see Pitfalls). Note where the portable zip keeps its data.

**Time.** 30 to 45 minutes.

**What good looks like.** You can describe each failure in one sentence. You know where the traces go, and how to clear them.

## Templates and checklists

### Template A. Hand-off log (one row per step)

| Date | Chapter and file | App and version | Install (MSI or portable) | Playbook step | Input file and SHA-256 | Output file and SHA-256 | Changes by hand | AI-restored or generated? (label) | Result and warnings (word for word) | Checked by |
|---|---|---|---|---|---|---|---|---|---|---|

### Template B. Acceptance-test record

| App | Version (`--version`) | Install type | Windows.Data.Pdf.dll present? / GPU | Signed? (Digital Signatures tab) | Steps passed (1 to 5) | Warnings, word for word | Verdict (pass, fail or finding) |
|---|---|---|---|---|---|---|---|

### Template C. Scan pilot scoring sheet

| Print | Tool | Border mean R, G, B | Eye score: colour (1 to 5) | Eye score: skin tone (1 to 5) | Notes |
|---|---|---|---|---|---|

### Checklist 1. Before you open any file

- [ ] The file is a copy in `work\`. The original is read-only.
- [ ] The app version matches the pin in the log.
- [ ] PhotoCraft autosave is on.
- [ ] No other program has the same LightCraft library open.
- [ ] The folder is not inside a cloud-synced folder.
- [ ] Control ports (`--control`) are off.
- [ ] Face recognition is off.

### Checklist 2. Saving in PhotoCraft

- [ ] Did you add an adjustment layer, text, a layer style or a vector mask? If so, expect a PSD, not an ORA.
- [ ] Did you save to `work\`, not `in\`?
- [ ] Did you reopen the saved file to check the layers?
- [ ] Are the layer names unchanged?
- [ ] Were the PNG exports made from the saved file?

### Checklist 3. Saving in VectorCraft

- [ ] Did you use Save As, not Export?
- [ ] Settings: Presentation Attributes; Object IDs = Layer Names; Decimals = 3; Responsive off; Preserve editing off; Images = Embed; Fonts = SVG or Outlines.
- [ ] Did you rename any object? (Do not.)
- [ ] Did `check_ids.py` return 0?

### Checklist 4. Scan batch

- [ ] Originals are read-only, and the import mode is `add` (never `move`).
- [ ] Largest scan opens in LightCraft (strip layout checked).
- [ ] `LIGHTCRAFT_GPU=0` is set for the batch.
- [ ] Every result line has `"ok": true`.
- [ ] The neutral border point is recorded.
- [ ] Masters (16-bit TIFF) and JPEGs have checksums in the log.

### Checklist 5. End of session

- [ ] Recent-file lists cleared.
- [ ] Recovery autosaves reviewed and cleared in `%APPDATA%\Photocraft\Recovery` and `%LOCALAPPDATA%\Photocraft\Recovery` (see Pitfalls).
- [ ] Control ports off.
- [ ] LightCraft thumbnail caches and XMP sidecars cleared (W-26).
- [ ] Hand-off log updated, with ids only, and committed to the private repo (D-14).

## Decisions you'll need to make

Each decision gives the options and our current lean. The lean may change after Exercise 1 or Exercise 5.

1. **Which version to pin.**
   - Options: the newest tag on test day (no later than 2026-10-25), or the three provisional tags (PhotoCraft v0.10.0, VectorCraft v0.13.1, LightCraft v0.9.1, as of 2026-10-18).
   - **Lean:** the newest tag that passes Exercise 1. If none does, use the provisional tags.
   - **Register status (W-22):** default. PhotoCraft v0.10.0, VectorCraft v0.13.1, LightCraft v0.9.1, or the newest tag that passes the five-minute test on test day; pins frozen Sun 25 Oct, portable zips verified against `SHA256SUMS.txt`, no upgrade mid-chapter.
2. **Install type.**
   - Options: MSI (installs under Program Files, and keeps recovery files in your user profile), or portable zip (keeps data beside the program).
   - **Lean:** the portable zip, as the pin rule says. It makes traces easier to find and delete. [11]
   - **Register status (W-22, W-26):** default. Craft apps as portable zips with data folders beside the program.
3. **Editor for layered stills.**
   - Options: PhotoCraft; Krita (ORA is its native layered format, but the only check so far is the vendor's own Krita test, which we have not repeated); GIMP 3.0.4 had a reproduced `.ora` export bug (GitLab #14168: layers and text scrambled on reopen; a forum reply says Krita and MyPaint also showed it; the issue is now closed and the fix version was not found). Current GIMP 3.x behaviour is not tested; Krita remains the verified ORA fallback. [4][52][74]-[76]
   - **Lean:** PhotoCraft. Krita is the fallback, once we have tested it on our own files.
4. **Scan tool.**
   - Options: LightCraft (script plus app); darktable; RawTherapee; ImageMagick as a rough pre-pass. [51][53][55]
   - **Lean:** LightCraft, but only if it wins the 10-print pilot against darktable.
   - **Register status (W-27, O-23):** default, decide by Sun 15 Nov. Whichever tool wins the pilot; LightCraft only if it wins and the TIFF strip-layout check passes; borrow a flatbed before buying.
5. **Where the scans and library live.**
   - Options: a local disk, or a network share. On a share, LightCraft opens the library without locking it, and two computers can silently drop each other's edits. [36]
   - **Lean:** a local NTFS disk on your PC, never a synced cloud folder, with the originals inside the VeraCrypt container (W-25).
6. **SVG touch-up tool.**
   - Options: VectorCraft with the checker; Inkscape 1.2.2 or 1.4.4, Plain SVG. On the fixture `at-rig.svg`, Inkscape 1.2.2 Plain SVG kept all 11 ids, `data-pivot`, `data-z`, `class`, `<style>` and the original viewBox, and `check_ids.py` returned exit code 0 (research R5, [63]). Inkscape 1.4.4 gave the same result (research R15, [92]). Inkscape 1.3.x is not tested. Never use Optimized SVG: its "Remove unused IDs" default stripped `leaf-1` and `leaf-2` in 1.4.4 [92]. A moved group gets a `transform` in either mode, so never move an animated group: re-author it, or move its children in Optimized mode, and re-check `data-pivot` after any Inkscape edit [92]. For command-line export on Windows use `inkscape.com`, not `inkscape.exe`. The Windows installers we read did not add Inkscape to PATH by default, so give the full path (TODO(research): confirm on a real install) [93][94].
   - **Lean:** VectorCraft, with the checker on every save.
   - **Register status (W-38, D-12, W-21):** titles are traced from the Card A slips in VectorCraft with Inkscape as the fallback; a title needs its SVG fallback; any live type uses an OFL font.
7. **Face recognition.**
   - Options: on, or off.
   - **Lean:** off. Faces of relatives are biometric data. [39]
8. **The apps' own AI features** (masks, content-aware fill, subject selection).
   - Options: use them, or avoid them. The research notes say these run locally, as classical or user-installed models. They have no numbered source.
   - **Lean:** non-AI fixes first, then these where they help, and log each use at its honesty-ladder level (L0 to L5) in the log and the manifest.
   - **Register status (W-40, D-16):** decided. Faces stay at L2: non-generative, or CodeFormer at `w` of 0.7 or more blended back. Any generative face change moves that image to L3 or is rejected. There is no AI animation of a real face and no model trained on her face.
9. **Web build for screenshots.**
   - Options: the desktop build, or the web build.
   - **Lean:** the desktop build. Use the web build only if the desktop build will not start in the container, and only with test cards (D-15). That is a week-1 check, not a decision for now. [12][38]

## Pitfalls

- **Old builds.** The website's PhotoCraft 0.7.0 has ORA support but not the no-overwrite guard. A save after adding an adjustment layer could drop it. Check the version first. [43][44]
- **Autosaves may land in the roaming profile.** On v0.9.0 and earlier, autosaves can go to the roaming profile (#5648). From v0.10.0 the documented Windows path is `%LOCALAPPDATA%\Photocraft\Recovery`. Check the Recovery folder after every session. [13][15]
- **Save is not Export.** VectorCraft's plain Export drops hidden objects. PhotoCraft writes a copy when the target format cannot hold everything. [22]
- **SVG hooks that do not survive.** VectorCraft keeps ids and `data-*` attributes. It drops `class` attributes, `<style>` text, most filters, SMIL and CSS animation, and transforms on groups, which are baked into the geometry. Re-add what you need after the touch-up. [22] Make PDFs with `vectorcraft-cli run --export x.pdf`, not the GUI Save As PDF (open crash reports #2141, #2196, #2460) [71].
- **Filters.** VectorCraft keeps only Gaussian blur, drop shadow, glow and feather. Other filters, such as colour matrices and turbulence, are ignored with a warning. [22]
- **The viewBox moves.** Export always rewrites the viewBox to start at `0 0`. If your original origin was not 0,0, the coordinates shift. [22]
- **Anonymous groups.** Plain groups without an id are not guaranteed to survive VectorCraft's import. Give any group that matters a name or id. TODO(research): the grouping rules come from a dependency that was not vendored. [22]
- **Gradient ids change.** Do not target gradient ids for animation. [22]
- **Big rigs skip recovery copies.** VectorCraft skips its recovery copies for documents above 20,000 objects. Save by hand more often on large rigs. [25]
- **PSD may not open in Photoshop.** PhotoCraft's own gap list says PSDs it writes are not always accepted by Photoshop, and no test opens its exports in another editor. Use ORA or PNG for hand-offs. [2]
- **Numbers that sound better than they are.**
  - "307 of 309 render the same" is a round-trip self-check, not fidelity to Photoshop. [3]
  - Against Photoshop-authored files, PhotoCraft's render matches the file's own merged image for 145 of about 256 files, which is 56 percent. [3]
  - The website's "134 of 135 byte for byte" has no counterpart in the repo. [44]
  - VectorCraft's "88 percent" counts menu items, tools and formats that exist, not behaviour. [30]
  - LightCraft's "61 percent of Lightroom" is self-assessed. [44]
- **Memory.** PhotoCraft's default budget is 8192 MB. The only measured baseline is a Mac, where a 20-megapixel layered PSD took 2.2 GB of memory. Nobody has measured the Windows PC at low memory. [13]
- **GPU traps.**
  - NVIDIA's "Shader Cache Size = Disabled" can hang the window for minutes. Do not set it. [13][37]
  - Intel: VectorCraft uses DX12, then OpenGL. It does not use Vulkan unless you set `WGPU_BACKEND=vulkan`. [27]
  - PhotoCraft's `--safe-gpu` option and start marker exist, but are untested on Windows. [14]
- **Control ports have no password.** The VectorCraft and LightCraft control ports accept connections without authentication. Turn them on only while you use them, and never on a network. PhotoCraft uses a bearer token. [8][26][34]
- **Code signing.** The READMEs say the installers are signed. The vendor's gap list says the signing material was not obtained. Expect Windows warnings, and check the Digital Signatures tab. [13]
- **Never `move` or `--in-place` on scans.** LightCraft's `move` import deletes the source after verification. PhotoCraft's batch `--in-place` writes back over the inputs. Never point either at original scans. [7][34]
- **One process per library, and no network shares.** Only one process may open a LightCraft library at a time. On a network share the library opens without locking, and edits can be lost. Keep it local. [36]
- **ORA is a small format with few checks.** Krita is the only third-party check so far. GIMP 3.0.4 had a reproduced `.ora` export bug (GitLab #14168, now closed; the fix version was not found), and current GIMP 3.x is not tested. Check every ORA round trip. [4][74]-[76]
- **Windows command-line quoting.** Passing JSON to native programs from Windows PowerShell 5.1 can strip inner double quotes. This comes from general knowledge, not from our sources. Use JSON-lines files or stdin, and test first. TODO(research): verify on the maker's PC.
- **Preview size.** The `serve` previews are capped at a 2048-pixel long edge and 5 MiB PNG, unless a trusted local session lifts the cap. Check the size of a final export yourself. [8]
- **Traces on the PC.** The apps leave recent-file lists, recovery autosaves, LightCraft thumbnail caches, logs and XMP sidecars next to scans. The places to look are `%APPDATA%\Photocraft\Recovery` (v0.9.0 and earlier), `%LOCALAPPDATA%\Photocraft\Recovery` (v0.10.0 and later), `%APPDATA%\VectorCraft`, `%APPDATA%\LightCraft`, and the thumbnail cache. Portable zips keep their data in `PhotoCraftData`, `VectorCraftData` and `LightCraftData` beside the program. Clear them after sessions. If this PC is shared with her, this matters even more. The charter says nothing may tip her off, and whether she shares the PC is still pending (O-03). The register's routine is a separate Windows account for the project, OneDrive backup off for Desktop, Documents and Pictures, and the Mum-test on every shared device now and monthly (W-26). [13][33][36]
- **Cloud sync.** If your Pictures or Documents folder syncs to a cloud service, the scans and the library could be copied to it. Keep these folders outside the synced area, or pause sync. (This comes from the charter, not from the research notes.)
- **The Launcher updates on its own.** It polls GitHub and can change the apps behind your back. Its README documents no off switch, so do not install or run it during production. Use the portable zip for the pinned tag instead. [81]
- **Everything here is untested.** The commands come from code, tests and docs. Exercise 1 is the first real test.

## Best references

1. **PhotoCraft product page**, https://getartcraft.com/apps/photocraft. Read it first for what the app claims and its status. The version it shows (0.7.0) is older than our pin. [44]
2. **VectorCraft product page**, https://getartcraft.com/apps/vectorcraft. The same, for VectorCraft. It shows 0.9.0, and the newest tag is v0.13.1 (2026-10-18). [44][43]
3. **LightCraft product page**, https://getartcraft.com/apps/lightcraft. The same, for LightCraft. It shows 0.6.0, and the newest tag is v0.9.1 (2026-10-17). [44][43]
4. **PhotoCraft's ORA notes** (constructed locator, see Sources), https://github.com/storytold/photocraft/blob/v0.9.0/docs/ora.md. The table of what ORA keeps and loses, the no-overwrite rule and the Krita check. Read it before any ORA work. [4]
5. **VectorCraft's file-format parity notes** (constructed locator), https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/file-format-parity.md. What the vendor says it has not tested: no real-world file corpus and no field records. Read it before trusting an SVG round trip. [30]
6. **LightCraft's XMP and preset notes** (constructed locator), https://github.com/storytold/lightcraft/blob/v0.8.0/docs/xmp-interop.md. The `.lcpreset` format, and which XMP fields are read only approximately. [33]
7. **darktable's command-line reference**, https://docs.darktable.org/usermanual/development/en/special-topics/program-invocation/darktable-cli/. You need it for the pilot, and it is the scan fallback. [53]
8. **Krita's command-line reference**, https://docs.krita.org/en/reference_manual/linux_command_line.html. The export command for Krita, the ORA fallback. [52]

## Sources

*Link status.* The GitHub addresses below are **constructed locators**. They were built from the tag and the file path. The research container could not open github.com (it returned 403), so the researcher read each file in a local clone. Open each link yourself before you cite it outside this project. Items [65] to [76] were read with WebFetch, which summarises pages, so re-open any item that drives a decision. [63], [83], [84] and [92] are container runs, not web links. The getartcraft.com pages, the darktable docs and the Krita docs were fetched by the researcher on 2026-10-18. Two items were seen only in search results, and they are marked as such.

- [2] photocraft `docs/file-format-parity.md`: PSD, ORA and SVG support table, oracle floors. https://github.com/storytold/photocraft/blob/v0.9.0/docs/file-format-parity.md (constructed locator)
- [3] photocraft `crates/io/tests/corpus.rs`: floors 146/169, 236/308 and 145/258 (or /256), and what "oracle pass" and "round trip" mean. https://github.com/storytold/photocraft/blob/v0.9.0/crates/io/tests/corpus.rs (constructed locator)
- [4] photocraft `docs/ora.md`: ORA kept and lost table, no-overwrite rule (#3806), Krita 5.2.9 verification (32/35, 33/34). https://github.com/storytold/photocraft/blob/v0.9.0/docs/ora.md (constructed locator)
- [6] photocraft `book/src/formats/` (overview, psd-psb, pcraft, raster-formats, svg): `.pcraft` layout, PSD limits, layered TIFF, SVG import table, 32-bit allocation limit. https://github.com/storytold/photocraft/tree/v0.9.0/book/src/formats (constructed locator, folder)
- [7] photocraft `apps/photocraft-cli/src/lib.rs` and `book/src/automation/cli.md`: subcommands, `run --new`, `batch --actions`, usage text. https://github.com/storytold/photocraft/blob/v0.9.0/apps/photocraft-cli/src/lib.rs (constructed locator)
- [8] photocraft `docs/control-protocol.md`, `docs/mcp.md` and `book/src/automation/security-model.md`: bearer token, loopback, headless `serve` methods, limits, MCP tools, bridge. https://github.com/storytold/photocraft/blob/v0.9.0/docs/control-protocol.md (constructed locator)
- [9] photocraft `crates/engine/src/commands.rs` (with `file_cmds.rs` and `layer_multi_cmds.rs`): `file.new`, `file.placeEmbedded` (smartObject parameter), `loadFilesIntoStack`, `layer.setProps`, `layer.renameLayer`, `layer.moveTo`. https://github.com/storytold/photocraft/blob/v0.9.0/crates/engine/src/commands.rs (constructed locator)
- [10] photocraft `crates/automation/tests/openraster.rs` (with `agent_tasks.rs` and `src/headless.rs`): save by extension, trusted-local versus workspace, tests of the layered ORA save and scripted tasks. https://github.com/storytold/photocraft/blob/v0.9.0/crates/automation/tests/openraster.rs (constructed locator)
- [11] photocraft `packaging/windows/photocraft.wxs` (with `package.ps1`, `portable.txt` and `docs/releasing.md`): MSI components including the CLI, PE checks, static CRT, "Windows 10+", portable mode. https://github.com/storytold/photocraft/blob/v0.9.0/packaging/windows/photocraft.wxs (constructed locator)
- [12] photocraft `packaging/web/README.md` and `apps/photocraft-web/src/web.rs`: web zip contents, headers, `?cpu` and `?webgl`, no autosave. https://github.com/storytold/photocraft/blob/v0.9.0/packaging/web/README.md (constructed locator)
- [13] photocraft `docs/scorecard.md` (with `gaps.md`, `target-app-parity.md` and `hardware-parity.md`): scorecard rows, gap G1 and G17, readiness numbers, 1,230 issues, performance baseline on macOS M4 Pro. https://github.com/storytold/photocraft/blob/v0.9.0/docs/scorecard.md (constructed locator)
- [14] photocraft `docs/development.md`: graphics startup and device loss, environment variables, logs. https://github.com/storytold/photocraft/blob/v0.9.0/docs/development.md (constructed locator)
- [15] photocraft `crates/format/src/autosave.rs` (and `crates/engine/src/prefs.rs`): autosave every 10 minutes, Memory Usage 8192 MB, scratch disks. https://github.com/storytold/photocraft/blob/v0.9.0/crates/format/src/autosave.rs (constructed locator)
- [20] vectorcraft `crates/svg/src/import.rs`: usvg options, labels, layer mode, `data-*` handling. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/src/import.rs (constructed locator)
- [21] vectorcraft `crates/svg/src/export.rs`: `sanitize_id`, `id_attr`, the viewBox line, classes. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/src/export.rs (constructed locator)
- [22] vectorcraft `crates/svg/tests/ids.rs` (with `symbols_layers.rs`, `roundtrip.rs`, `options.rs`, `gradients.rs` and `prop_svg.rs`): id and name, animation rig, nested groups, class and style tests. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/tests/ids.rs (constructed locator)
- [24] vectorcraft `apps/vectorcraft-cli/src/main.rs`: usage, `convert` (with importWarnings), `run`, `info`. https://github.com/storytold/vectorcraft/blob/v0.12.0/apps/vectorcraft-cli/src/main.rs (constructed locator)
- [25] vectorcraft `docs/mcp.md`: tools, roots, modes, the Windows MSI path, Data Recovery. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/mcp.md (constructed locator)
- [26] vectorcraft `docs/control-protocol.md`: loopback, "no authentication", limits. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/control-protocol.md (constructed locator)
- [27] vectorcraft `docs/development.md`: web build, GPU selection and crash markers, logs, robustness. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/development.md (constructed locator)
- [29] vectorcraft `packaging/windows/vectorcraft.wxs` (with `package.ps1`, `docs/releasing.md` and `docs/windows7.md`): installers, Windows requirements, web packaging. https://github.com/storytold/vectorcraft/blob/v0.12.0/packaging/windows/vectorcraft.wxs (constructed locator)
- [30] vectorcraft `docs/file-format-parity.md` (with `target-app-parity.md`, `hardware-parity.md` and `gaps.md`): the 88 percent breakdown, no real-world corpus, robustness row. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/file-format-parity.md (constructed locator)
- [31] vectorcraft `crates/engine/src/cmd/fileio/svg.rs` (with `mod.rs` and `save.rs`): writable formats, SVG option defaults, `.ai` embedding. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/engine/src/cmd/fileio/svg.rs (constructed locator)
- [33] lightcraft `docs/xmp-interop.md`: sidecars, `crs:` mapping table, `.lcpreset` format, import formats. https://github.com/storytold/lightcraft/blob/v0.8.0/docs/xmp-interop.md (constructed locator)
- [34] lightcraft `apps/lightcraft-cli/src/main.rs` (with `docs/mcp.md` and `docs/control-protocol.md`): CLI usage, `run`, `render`, `snapshot`, the port without authentication. https://github.com/storytold/lightcraft/blob/v0.8.0/apps/lightcraft-cli/src/main.rs (constructed locator)
- [35] lightcraft `crates/pipeline/src/lib.rs` (with `auto.rs`, `tests.rs` and `docs/file-format-parity.md`): stage order, `SourceInfo.raw`, rendered-source tests, TIFF and JPEG support. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/pipeline/src/lib.rs (constructed locator)
- [36] lightcraft `crates/catalog/src/journal.rs` (with `lock.rs` and the torn-append, lock and repair tests): operation log, recovery rules, locking on shares. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/catalog/src/journal.rs (constructed locator)
- [37] lightcraft `docs/gpu-pipeline.md` (with `gaps.md` and `hardware-parity.md`): backends, memory budget, NVIDIA issue, gap #27, Windows Radeon datum. https://github.com/storytold/lightcraft/blob/v0.8.0/docs/gpu-pipeline.md (constructed locator)
- [38] lightcraft `docs/web.md` and `apps/lightcraft-web/index.html`: web bundle, headers, OPFS storage, `lightcraft.command`. https://github.com/storytold/lightcraft/blob/v0.8.0/docs/web.md (constructed locator)
- [39] lightcraft `crates/fetch/src/lib.rs` (with `crates/engine/src/model_download.rs`, `face_download.rs` and `cmd/geocode.rs`): the network paths and the opt-in downloads. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/fetch/src/lib.rs (constructed locator)
- [41] lightcraft `packaging/windows/lightcraft.wxs` (with `package.ps1` and `docs/releasing.md`): x64, x86 and arm64 MSI and portable builds. https://github.com/storytold/lightcraft/blob/v0.8.0/packaging/windows/lightcraft.wxs (constructed locator)
- [42] lightcraft `crates/engine/src/export.rs` (with `cmd/develop.rs`, `cmd/preset_files.rs` and `presets.rs`): export options, naming-token tests, preset commands, shipped preset shapes. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/engine/src/export.rs (constructed locator)
- [43] Git data for `storytold/photocraft`, `storytold/vectorcraft` and `storytold/lightcraft`, read on 2026-10-18 with `git ls-remote --tags` and blobless bare clones: tag list, tag dates, commit counts, commit subjects, `git tag --contains`. This is a method, not a web link. Commit subjects are untrusted data.
- [44] getartcraft.com product pages, fetched 2026-10-18: https://getartcraft.com/apps/photocraft , https://getartcraft.com/apps/vectorcraft , https://getartcraft.com/apps/lightcraft . Versions 0.7.0, 0.9.0 and 0.6.0, status badges, file names, and the vendor's "134 of 135" claim.
- [51] ImageMagick command-line options: `-auto-level`, `-auto-gamma`, `-contrast-stretch`, `-color-matrix`, `-clut`, with `-channel`. https://imagemagick.org/command-line-options/
- [52] Krita command-line reference, fetched 2026-10-18: `--export` and `--export-filename`. https://docs.krita.org/en/reference_manual/linux_command_line.html
- [53] darktable `darktable-cli` reference, fetched 2026-10-18: usage, XMP sidecars, `--style`. https://docs.darktable.org/usermanual/development/en/special-topics/program-invocation/darktable-cli/
- [55] RawTherapee command-line options (https://rawpedia.pixls.us/command-line_options/, also man.archlinux.org/man/rawtherapee.1.en). **Seen only in search results**, so the content is known only through the search summary.
- [58] photocraft `crates/io/src/ora.rs`, `crates/io/src/ora/tests.rs` and `docs/ora.md` at `v0.10.0`, diffed against `v0.9.0`: group isolation by file version (round 2, R3a). https://github.com/storytold/photocraft/blob/v0.10.0/crates/io/src/ora.rs (constructed locator)
- [61] photocraft at `v0.10.0`: `crates/automation/src/workspace.rs` and `headless.rs`, `apps/photocraft-cli/src/lib.rs`, `docs/control-protocol.md` (lines 336 to 395): roots, request paths, `doc.place`, `doc.exportLayers` (round 2, R6). https://github.com/storytold/photocraft/blob/v0.10.0/docs/control-protocol.md (constructed locator)
- [63] First-hand run in the research container, 2026-10-18: Inkscape 1.2.2 Plain SVG on the fixture `at-rig.svg`, checked with `check_ids.py` (round 1, R5). Not a web link.
- [65] https://github.com/storytold/photocraft/releases/tag/v0.10.0 — read with WebFetch (summarised), 2026-10-18: the vendor's release notes. Vendor claims.
- [70] https://github.com/storytold/photocraft/issues/6249 , `/issues/7252` , `/issues/7018` — read with WebFetch (summarised), 2026-10-18. Issue text is untrusted data.
- [71] https://github.com/storytold/vectorcraft/issues (lists), `/issues/2414`, `/issues/2243`, `/issues/2141`, and https://github.com/storytold/vectorcraft/pull/2480 — WebFetch (summarised), 2026-10-18. #2196 and #2460 are from the issue list.
- [72] https://github.com/storytold/lightcraft/issues (lists), `/issues/2198`, `/issues/1983`, `/issues/2090`, and https://github.com/storytold/lightcraft/pull/1989 — WebFetch (summarised), 2026-10-18.
- [74] https://www.gimp-forum.net/Thread-ora-export (posts of 2025-05-31 and 2025-06-01) — WebFetch (summarised). Forum claims, unverified.
- [75] https://www.gimp-forum.net/Thread-ora-format-it-really-works?pid=45536 (posts of 2025-09-17) — WebFetch (summarised). A forum guess.
- [76] https://gitlab.gnome.org/GNOME/gimp/-/issues/14168 and its `.json` — WebFetch: title, versions, state closed, updated 2025-07-06.
- [81] craft-launcher README, `https://raw.githubusercontent.com/storytold/craft-launcher/main/README.md`, read 2026-10-18 by the round-1 review (row 15); not re-opened for this round. It documents no setting, flag or file that disables updates, and it confirms that every release has a `SHA256SUMS.txt`.
- [82] storytold/lightcraft at `v0.9.1`, read from a local clone (round 2, R11): `crates/ui-egui/src/panels/faces.rs`, `crates/engine/src/cmd/face_models.rs`, `crates/engine/src/face_download.rs`, `crates/faces/src/known.rs`, `crates/engine/src/config.rs`, `docs/faces.md`. https://github.com/storytold/lightcraft/blob/v0.9.1/docs/faces.md (constructed locator). Static read, not run.
- [83] First-hand test, 2026-10-18: the `tiff` crate 0.11.3 (the version pinned in LightCraft's `Cargo.lock`; source at https://static.crates.io/crates/tiff/0.11.3/download) with the harness in `research/craft-visual-fixtures/tiff-limit/`. Not the LightCraft binary.
- [84] First-hand test, 2026-10-18: ImageMagick 6.9.12 `convert -define tiff:rows-per-strip=64 -compress None`, read back with Pillow. Container only; not run on Windows.
- [92] First-hand run, 2026-10-18: Inkscape 1.4.4 on `at-rig.svg` (Plain SVG, Optimized SVG with scour, and the "Store transformation" test), with 1.2.2 as the control (round 2, R15). Container only.
- [93] https://gitlab.com/inkscape/inkscape/-/raw/INKSCAPE_1_2_2/src/ui/dialog/inkscape-preferences.cpp, and the INKSCAPE_1_3 and 1_4_2 CMake and WiX files, read with curl. Source only; the Windows installer was not run.
- [94] https://gitlab.kitware.com/cmake/cmake/-/raw/v3.31.0/Modules/Internal/CPack/NSIS.InstallOptions.ini.in, read with curl: the PATH default of the NSIS template. Source only.

## Changelog

- **v0.1, 2026-10-18.** First version, written from `research/craft-visual.md` for track `craft-visual`. Nothing has been executed yet. Open items are marked TODO(research).
- **v0.2, 2026-10-18.** Round 1 Fable review applied (`reviews/craft-visual-round1.md`): the Launcher updater step is replaced by a manual portable-zip and `SHA256SUMS.txt` check, provisional pins moved to v0.10.0, v0.13.1 and v0.9.1, Recovery paths qualified by version, VectorCraft's MSI path, the Python version and the TIFF master export in the LightCraft fixture added, and two story-serving uses added to "Why this matters".
- v0.3, 2026-10-18. Round 2 Fable review applied (`reviews/craft-visual-round2.md`): LightCraft TIFF strip check added (Step 8 item 1a, Exercise 5, Checklist 4, skill step 13); `serve` path rules and the ORA group rule added; GIMP and Inkscape verdicts, the Windows hardware block, the Faces menu path and the border-measurement method updated from research rounds 1 and 2; save-guard and autosave wording and the Launcher citation corrected.
- v0.4, 2026-10-18. Reconciled with DECISIONS.md (2026-10-18): pins stated as the register's defaults, frozen Sun 25 Oct (W-22); the Launcher is never installed and the Craft boundary added (D-12); title lettering only for words she wrote, with the maker's hand for cards (W-35, W-38); LightCraft looks per album batch, not per decade (W-27, W-39); scan standard added (W-27); family originals inside the VeraCrypt container with no cloud copy and `cloud: none` by default (D-15, W-24, W-25); her prints only from Sun 15 Nov after the L1 lock (D-13); the AI-features lean restated with the honesty ladder (W-40, D-16); the log carries ids only and is committed to the private repo (D-14); shared-PC routine (W-26, O-03 pending). Decisions carry their register status.
