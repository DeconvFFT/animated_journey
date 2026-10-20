# Kit B: Ken Burns, the archive and the PC colour check

Three small things to run on your Windows PC over the next days. Each one prints what it is about to do, then `ok` or the reason it could not. None of them changes a setting, uses the internet or touches your own photos and documents.

| When | What | Script |
|---|---|---|
| Mon 26 Oct | Ken Burns by script: three slow moves on three stills of your own, joined by dissolves, 1920x1080 at 24 frames a second | `win\kit2\kenburns_24.ps1` |
| Tue 27 Oct | The archive: four folders, two empty record sheets, five practice scans and a checksum list, then a tamper test | `win\kit2\archive_init.ps1` and `win\kit2\archive_verify.ps1` |
| Thu 29 Oct | The PC colour and spec check: tests your ffmpeg's pixels, not just its labels | `win\kit2\run_checks_pc.ps1` |

If anything below is unclear, stop and ask in chat before you run anything. A pause costs nothing.

**Not yet tested on a real Windows PC.** These scripts were built and tested on Linux. Every line that asks Windows a question (where `%TEMP%` is, how the `py` launcher answers, how ffmpeg from winget behaves) is untested until your first run. If something looks wrong, that is useful news, not your fault.

## What these scripts are and what they never do

They **read only what you name** (your three stills; nothing else) and **write only** the files they list in their last line, `files written:`. They never delete or overwrite anything of yours, never use the internet, never need administrator rights and never print your user name, computer name or a folder inside your user folder: paths are printed as `<project>` (the project folder), `%TEMP%` or `%USERPROFILE%`.

Two rules from the project apply to what you feed them:

- **Practice material only until Sat 14 Nov.** For the Ken Burns exercise use your own pictures of things (a street, a plant, a cup, a view), not photos of family or of anyone you know. Her photos wait until the process lock on Sat 14 Nov.
- **The raw colour file is for the chat only.** The Thursday script writes one file into your temporary folder. You read it and paste it into the chat. You never save it in the project folder and never commit it.

## Before you start

1. You need the **whole project folder**, not single files, the same one as for the first kit (the scripts read the project's own tools and checksum scripts and stop if they are missing). Open PowerShell in that folder: open it in File Explorer, click the address bar, type `powershell` and press Enter.
2. Check what is installed. These two lines only read:

```powershell
ffmpeg -version | Select-Object -First 1
```

```powershell
py -3 --version
```

If both print a version, go to "Run a script for one session only". If one says it is not recognised, install it:

## Installing Python and ffmpeg

**UNVERIFIED: these two lines were read from the winget catalogue on 2026-10-18 and have never been run on Windows.** If winget says it cannot find the id, stop and tell the orchestrator in chat what it printed; do not look for another source.

```powershell
winget install --id Gyan.FFmpeg -e
```

```powershell
winget install --id Python.Python.3.13 -e
```

Close the PowerShell window and open a new one in the project folder, so the new programs are found. The Ken Burns tool also needs two Python add-ons, installed for your user only (no administrator rights):

```powershell
py -3 -m pip install --user pillow numpy
```

(UNVERIFIED: the add-ons come as ready-made wheels for current Python on Windows; if pip starts compiling something, stop and tell the orchestrator.) To check that the Ken Burns tool can see them:

```powershell
py -3 -I win\kit2\kenburns_24.py --check-libs
```

It should print `ok: Pillow ..., numpy ...`. (Good to know: the project's tools start Python in a protected mode, `-I`, which does not look in the folder that `pip install --user` fills. The Ken Burns tool adds that folder back for itself, so this works. The optional motion gate further down is not able to do that: see its note.) The archive scripts need neither Python nor ffmpeg. The Thursday script needs Python and ffmpeg but not the add-ons.

## Run a script for one session only, without changing system policy

Windows blocks scripts by default. You do **not** need to change that for the whole PC. These are the same options as in the first kit. Each lasts one run or one window.

**Option A (simplest).** This allows the script for this one run only. Replace the script name with the one you want:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\archive_verify.ps1 -Root C:\lj\standin
```

**Option B.** This relaxes the rule for the current window only. When you close the window everything is back to normal; the machine and user settings are never touched:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\win\kit2\archive_verify.ps1 -Root C:\lj\standin
```

Two read-only helpers if something does not work:

```powershell
Get-ExecutionPolicy -List
```

That shows the policy at each level and changes nothing. Paste the result in chat if you are stuck.

```powershell
Unblock-File .\win\kit2\archive_verify.ps1
```

Files from the internet carry a small "downloaded from the internet" mark. This removes that mark from that one file and does nothing else. (Unblock the file you want to run; the scripts that call other project scripts are covered by Option A or B.)

**If your PC is managed by Group Policy** (a work or school computer), both options may still say the script is blocked. Then **stop and change nothing**. Tell the orchestrator in chat what the message says.

The rest of this page shows Option A. Option B works the same way: after the `Set-ExecutionPolicy` line, type `.\win\kit2\NAME.ps1` and the same words after it.

## Monday 26 Oct: Ken Burns at 24 frames a second

**What it makes.** One video, `renders\ex02\ex02_kenburns.mp4` inside the project folder (`renders\` is ignored by git, so nothing can be committed by accident): three moves of six seconds (a slow push-in, a slow pan, a slow pull-out) joined by one-second dissolves. That is 16 seconds, 384 frames. The picture is 1920x1080, 24 frames a second, H.264, with the project's colour labels, made by the project's own `h264_online` encode recipe. Round things stay round: the tool cuts a 16:9 window out of each still and never stretches it.

**First, a check that needs none of your pictures.** It draws three plain test pictures, runs everything and checks itself (about a minute):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\kenburns_24.ps1 -Selftest
```

You should see the front door's steps 1 to 5, then the tool's own steps 1 to 7, with a list of `PASS` lines (1920, 1080, 24/1, h264, High, yuv420p, the four colour labels, 384 frames, 16.000 seconds), then `PASS disc_aspect ... 1.000` (a drawn circle measures round) and three `PASS colour_...` lines, then `RESULT: PASS`. It writes four files in `renders\wp09\` (the last line lists them). If you see `FAIL`, paste the lines in chat.

**Then your own stills.** Put three pictures somewhere simple, for example `C:\lj\stills\`. Bigger is better: at least 3000 pixels on the long edge gives a sharp close-up; the tool warns you when a still is too small for its move. Then:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\kenburns_24.ps1 C:\lj\stills\a.jpg C:\lj\stills\b.jpg C:\lj\stills\c.jpg
```

The three pictures get the moves in order: push-in, pan, pull-out. Useful extras, all optional:

- `-Moves pull,push,pan` chooses the order (the words are `push`, `pan`, `pull` and `drift`).
- `-Focus 0.5,0.3` decides where the 16:9 window sits in a picture that is taller than 16:9 (0.5,0.5 is the middle; the second number is how far down).
- `-Out C:\lj\ex02\kb.mp4` writes somewhere else (the name must end in `.mp4`).

**How long, how much memory.** The self-test takes about a minute. Your own stills take one to three minutes: the time is mostly the picture cutting, which grows with the size of the stills (about 35 seconds for 3000-pixel stills, about 90 for 6000-pixel ones on the Linux machine the plan was tested on; yours will differ). ffmpeg uses up to about 1 GB of memory while it joins the moves, so close the Claude app and other big programs first (UNVERIFIED on Windows).

**What it prints.** Five numbered steps from the front door (options, Python, Pillow and numpy, ffmpeg, the run), then the tool's own steps (five to seven, depending on the options). Your pictures are named by number and size only, never by file name. At the end: a read-back of the finished file (`PASS` or `FAIL` for width, height, frame rate, codec, pixel format, the four colour labels, frame count and length), `RESULT`, and `files written:`.

**What to look at.** Play the file. Round things (a wheel, a plate, a clock face) should stay round. The slowest move should show no shimmer or crawling on fine detail. To check the label from the exercise yourself:

```powershell
ffprobe -v error -show_entries "stream=width,height,r_frame_rate,codec_name" -of csv=p=0 renders\ex02\ex02_kenburns.mp4
```

It should print `h264,1920,1080,24/1`.

**See why the project does not use zoompan.** Add `-ProofZoompan` to the run. It also writes `ex02_kenburns_zoompan_proof.mp4`, the same kind of push made with ffmpeg's `zoompan` filter. Put the two side by side: zoompan jumps in whole pixels, so fine detail crawls a little. That is why it is a proof tool only.

**Optional: the motion gate.** `-GateWindow` also writes `ex02_kenburns_push_only.mkv`, a lossless 96-frame piece of the push. It is big (100 to 250 MB), so check the free space first and delete it afterwards. Then run the project's gate on it:

```powershell
py -3 -I pipeline\validators\mo8_gate.py renders\ex02\ex02_kenburns_push_only.mkv
```

It should end `RESULT: PASS` with both jitter numbers well under their limits (0.05 and 0.04 pixels). Run it on the zoompan proof's window the same way (`ex02_kenburns_push_only_zoompan.mkv`, made when you use both `-ProofZoompan` and `-GateWindow`): it fails, and that is the point.

**A catch (UNVERIFIED on Windows, and not something you did wrong).** The gate starts its measuring helper in the same protected Python mode, which ignores packages installed with `pip install --user`. If it stops with `environment problem: the audit needs numpy and Pillow` although the check line above printed `ok`, tell the orchestrator in chat: it is a known catch in the gate, not in your install. The gate has been tried only where the add-ons are installed system-wide.

**If the file has no sound** (it has none: sound is added later in the editor), the project's delivery checker needs the video-only profile:

```powershell
py -3 -I pipeline\validators\spec_check.py renders\ex02\ex02_kenburns.mp4 --profile online_h264_video_only --profiles-file win\kit2\profiles_kit2.json
```

It should end `RESULT: PASS`. (With the plain `online_h264` profile it fails on `audio.present` only, because that profile is for finished files with sound.)

**Messages you may see.**

| It says | What it means | What to do |
|---|---|---|
| `Python 3 is needed` | `py`, `python` and `python3` were not found, or only the Microsoft Store stub was | install as above, open a new window |
| `Install them for your user ... pip install --user pillow numpy` | Pillow or numpy is missing | run that line, then run the script again |
| `ffmpeg is needed` | ffmpeg is not on PATH | install as above, open a new window, or add `-Ffmpeg C:\full\path\to\ffmpeg.exe` |
| `its closest window is only N px wide` | a still is too small for the move | use a bigger still or a gentler move; the file is still made |
| `cannot write ... is the old file open in a player?` | Windows will not replace a file that is open | close the player and run again |
| `environment problem: ...` | something the tool needs is not as it expects (ffmpeg, Pillow or numpy, a project file, free disk space, or a folder it cannot make or write); the line names a file at most, never a folder | paste the one line in chat; it names no folder |
| `unexpected error (...)` | something nobody planned for happened; the brackets hold only the kind of error (for example `OSError`), never its text or a folder, and nothing of yours was changed | paste the one line in chat |

## Tuesday 27 Oct: the archive and five practice scans

**What it makes.** A new folder (default `C:\lj\standin`) holding the four folders of Step 0 of the imagery playbook (`01_masters`, `02_work`, `03_exports`, `04_reconstructions`), two empty record sheets (`manifest.csv` and `steps.csv`, header line only, for you to fill), five **synthetic** practice scans in `01_masters` and `checksums.txt`. The practice scans are drawn by the script (a colour gradient, a checker and a ring); nothing of yours is in them. Their ids are `LJ-ST-0001-F` to `LJ-ST-0005-F`: `LJ` for the project, `ST` for "stand-in" where a real box code like `B03` would go, a four-digit number, `F` for the front. A back would end in `B`.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\archive_init.ps1 -Root C:\lj\standin -Count 5
```

It only builds in a folder that is new or empty. If the folder holds anything else it stops and changes nothing; if it already is an archive it says so and changes nothing. A drive root such as `E:\` is refused. Add `-WithBacks` to make a practice back for every front (ten files). The last two lines say what to do next and list every file written. You should see, near the end:

```text
checked 5 files, 0 problems
```

**Check it.**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\archive_verify.ps1 -Root C:\lj\standin
```

It changes nothing, not even a log. It checks the four folders, the two header lines (against the playbook's columns), and every file in `checksums.txt` against its fingerprint, then ends `RESULT: OK, no problems`.

**The tamper test.** This changes one byte of one practice scan to show that the check notices (a fingerprint is only worth having if a change shows up). It touches only the practice file named in the line:

```powershell
$p = 'C:\lj\standin\01_masters\LJ-ST-0003-F.tif'
$b = [System.IO.File]::ReadAllBytes($p); $b[5000] = $b[5000] -bxor 1; [System.IO.File]::WriteAllBytes($p, $b)
```

Run the check again. It should print `MISMATCH LJ-ST-0003-F.tif`, `checked 5 files, 1 problems` and `RESULT: 1 problem(s) found`, and finish with a non-zero exit code. To undo, run the same two lines again (flipping the same bit twice restores the file) and check again: it is clean.

**Fill the record sheet.** Open `manifest.csv` in a spreadsheet or Notepad and add five rows by hand, one per practice scan, as in Exercise 1 of the imagery playbook. The columns are listed in its first line. Nothing in the kit reads the rows yet.

**For the real archive later,** run `archive_init.ps1 -Root <a folder inside the encrypted container> -Count 0` for the empty skeleton. Real scans never go in the project folder.

## Thursday 29 Oct: the PC colour and spec check

**Why.** Colour labels on a video are not proof: a file can say "BT.709" and still carry the wrong colours. The project tests the **pixels** of every encode recipe, and the result depends on the exact ffmpeg build. The container used for the plan has ffmpeg 6.1.1; your PC has a different build (the winget build was 9.0.2 when the plan was read on 2026-10-18; UNVERIFIED). This script runs the test on **your** ffmpeg.

**What it does.** About a minute: it makes a 3-second test clip with your ffmpeg (a built-in test picture and a quiet tone; nothing of yours is read), checks the clip against the project's online delivery profile (`spec_check.py`), then runs the colour-patch test on every project encode recipe and on the two phone recipes (`colour_patch.py --all`), and finally checks what it is about to write against the project's list of identifying-data patterns and against your own user, computer and domain names (read from Windows at that moment, never saved). If the check is clean it writes **one file**, `%TEMP%\colour_patch_pc.json`, and prints a short block to paste. It uses a temporary folder under `%TEMP%` that it deletes at the end.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\kit2\run_checks_pc.ps1
```

If ffmpeg is not on PATH, add `-Ffmpeg C:\full\path\to\ffmpeg.exe`. You will see eleven numbered steps: the pattern file, Python, ffmpeg (its version number is printed, nothing else about the build), the project files, the test clip, the spec check, the joined recipe list, the colour test, the scan, the write, the clean-up. Then the spec lines (27 `PASS` lines if all is well), the colour lines (one per recipe, with `worst N/255`, and the six built-in controls: three of them are *expected* to fail on some builds, and `TRAP PRESENT` just says this build has a known trap, which is information, not a problem), and the paste block.

**Read it, then paste it.** Open the file in Notepad:

```powershell
notepad "$env:TEMP\colour_patch_pc.json"
```

Read it once. It holds the ffmpeg version line, the list of options the build was compiled with, the fingerprint (SHA-256) of the ffmpeg program, and the test numbers. You should **not** see your name, your computer's name, an e-mail address, a number like 192 dot 168 or a path through your user folder. If you do, do not paste it: tell the orchestrator in chat what kind of line it is (not the line itself). Then paste the whole text **into the chat and nowhere else**, together with the short block the script printed. Do **not** save it in the project folder, do not commit it and do not e-mail it: the compile options of a build can carry folder names. The orchestrator turns your paste into a short file of chain names and numbers (no options, no paths) and files only that.

When you are done you can delete the file: type `%TEMP%` in File Explorer's address bar and delete `colour_patch_pc.json`.

**What the result means.** Every project recipe should read `worst 3/255` or less (`PASS`). A recipe above 3 is a finding about the recipe on your build, not a fault of yours: the orchestrator adjusts the recipe. The numbers 1 and 2 are normal. The script exits with 0 when everything passed, 1 when a check failed (the file is still written, because the numbers matter), 2 when it refused to write, 3 when it could not run (Python or ffmpeg missing).

**If it refuses to write.** You may see:

```text
REDACTION CHECK FAILED, nothing was written
category=profile_path_windows field=ffmpeg.configure[12] hit=C:********
```

`category` is the kind of thing it thinks it found, `field` is where in the record (the number in brackets is the position of the flag in the build's list of options, counting from 0, so `[12]` is the thirteenth), `hit` is the first two characters followed by stars. These lines hold only a kind, a place and two characters, so they are **safe to paste into chat**. Nothing was written, and the temporary folder was deleted. **Do not edit the JSON by hand to get past it.** Paste the refusal lines and the output of `ffmpeg -version | Select-Object -First 1`, and the orchestrator adjusts the rule the same day. If it says `REDACTION PATTERNS UNAVAILABLE`, `scripts\redaction_patterns.json` is missing: download the whole project folder again.

## What each script prints and writes

| Script | Prints | Writes | Never touches |
|---|---|---|---|
| `kenburns_24.ps1` | numbered steps, the tool's steps, a read-back with PASS or FAIL per field, `RESULT`, `files written:` | the `.mp4` (and, if asked, `_push_only.mkv`, `_zoompan_proof.mp4`, `_push_only_zoompan.mkv`) in `renders\ex02\`, or where `-Out` says; a temporary folder deleted at the end | your stills, anything outside the output folder |
| `archive_init.ps1` | eight numbered steps, `checked N files, 0 problems`, `files written (under ...)` | the four folders, `manifest.csv`, `steps.csv`, the practice scans, `checksums.txt`, only in a new or empty folder | any existing file, anything outside the folder you name |
| `archive_verify.ps1` | five numbered steps, one line per folder, header and problem, `checked N files, M problems`, `RESULT`, `files written: none` | nothing | everything (read-only) |
| `run_checks_pc.ps1` | eleven numbered steps, the spec and colour lines, the paste block, `files written:` | `%TEMP%\colour_patch_pc.json` (or where `-Out` says) and a temporary folder deleted at the end | your files, the network, your settings |

## What is not verified yet

Everything about how Windows answers: where `%TEMP%` is on your PC (a managed PC may differ), how the `py` launcher and the Microsoft Store `python` stub behave, whether Pillow and numpy install as wheels, the winget ids, how ffmpeg 9.0.2 from winget behaves under the project's recipes (the colour test exists to find out), and every behaviour of Windows PowerShell 5.1 (the scripts were parsed by PowerShell 7.5.4 and checked by a 5.1-compatibility lint, not run on 5.1). The timing figures (about a minute) are from the Linux container.
