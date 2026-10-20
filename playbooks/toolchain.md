# Free Desktop Toolchain: A Small Stack for the Life Journey

Track: toolchain · Draft v0.5 · 2026-10-19 · For the maker (a motivated learner)
Built from research/toolchain.md (Sonnet researcher, 2026-10-18) and CHARTER.md. Numbers in brackets, like [1], point to the Sources list at the end. Anything marked TODO(research) is still open.

**Status: provisional.** We do not fix the plan until you return the app checklist in Step 0. Your computer and the apps you already have decide which tools make sense.

**Reconciled with DECISIONS.md (2026-10-18). The register wins (D-21).** The Windows PC is decided (D-10); its numbers stay UNVERIFIED until `windows_check_report.json` is in the repo (W-28). The project frame rate is 24 fps (W-14), so the 25 fps values the research tested are now 24 (`d=120`, `fps=24`, `-framerate 24`, `atsc_1080p_24`). They are UNVERIFIED at 24 until `recipes/r1_kenburns.sh`, `recipes/r2_parallax.py`, `recipes/r5_story.mlt` and the colour-patch test are re-run at 24; those recipe files still carry 25 until then. Loudness is -1 dBTP everywhere, with three venue masters chosen at the Mon 22 Feb run (W-19). Real photos enter after the P-LOCK process lock (Sat 14 Nov), and covert collection starts Sun 15 Nov (D-13). Family media stays on the PC and the encrypted drive, with no cloud copy (D-15, W-23, W-24, W-25). The maker alone decides every hard call (D-03, D-04). Each Decision below carries its register status: decided (`DECISIONS.md` Table 1), default with a decide-by date (Table 2), or open for the maker (Table 3). **Re-reconciled 2026-10-19 after the her-world merge:** the film's look comes from her Hindu world (D-28, D-31, W-72), so the game-world route is gone (D-29) and Exercise 8 and Decision 3 are now about the floor-art line; the phone files are PH1 and PH2 (W-63); the repo is public, so only text, scripts and ID-keyed manifests are committed (D-14, D-26); Indic text is burned with the `ass` filter before ffmpeg n9.0 and set in OFL families (W-21, W-75).

## Why this matters for our life journey

Most of your mother's life happened between the big moments: the kitchen table, the drive to work, the song she sang badly on purpose. Those gaps are what will make the film feel like her. The toolchain is how we turn those gaps into moving pictures and sound without a studio.

The charter asks us to prefer scriptable tools [1]. A script can be re-run, repaired and handed to an AI agent. A menu click cannot. So this track picked a small stack. Blender handles depth, camera moves and renders. Inkscape handles maps, timelines and drawn lines. One video editor does the finishing pass. Two command-line tools, ffmpeg and ImageMagick, sit under all of it, and every shot passes through them [62][64].

Fewer tools, learned well, will finish the film. We have about 19 weeks until Saturday, 27 February 2027. The ten practice exercises below take about three weeks at four a week, so Exercise 10 can be the delivery rehearsal, on synthetic material, ahead of the P-LOCK process lock on Saturday 14 November 2026, the end of week 4 (W-06). The vertical slice is a separate job: 100 seconds of chapter C01, briefed Sunday 15 November, animatic Sunday 6 December, final Sunday 20 December (W-07). That leaves about fifteen weeks after the lock for the real work (ROADMAP-ADDENDUM.md).

## Core principles

1. **Story before software.** Pick the scene first and the tool second. Before you open any program, say what the shot must show about her life. Tools are the last decision, not the first [1].

2. **Scripts are the master, the editor is the finishing pass.** Anything you will repeat (crops, camera moves, renders, encodes, loudness, captions) lives in a script you can re-run. Use the editor for choices that need your eyes: framing, timing to music, the final cut. The research ran most batch steps from the command line, and a few under a virtual display [100].

3. **Pin versions and write them down.** Use Blender 5.2 LTS for the whole project, and do not upgrade in the middle of the build [24]. Record every tool and version in the project README. The research hit several Blender changes between versions inside one session [100].

4. **Probe before you trust a remembered snippet.** Before you run a code example from memory or from an old tutorial, check what the program actually offers. List the attributes, or run the program's help. On the first attempt, two remembered Blender calls failed. The research avoided a third failure only by listing the attributes first [100].

5. **Make a cheap draft first.** Keep a 960×540 draft of every shot. Render Blender frames as PNG sequences, so a crash costs one frame, not an hour. Render the final overnight [100].

6. **Measure, do not guess.** Check every export with ffprobe, every loudness with a loudness report, and every archive with checksums [63][91]. Eyes and ears miss things that numbers catch.

7. **Real memories stay real.** Keep original scans untouched. Log every filter or AI step that changes a pixel. Label any reconstructed material visibly, so the audience can tell what is real [1].

8. **Keep working files private and local by default.** Nothing goes to a web tool, a cloud photo library or a shared family device without a decision by the maker [1]. Local tools keep files on your machine once their models are downloaded [72][73][74][75]. A web app's "nothing is uploaded" claim is the vendor's word, not an audit [55].

## How to do it, step by step

Do the steps in order. Do not skip Step 0.

### Step 0: Recognise your apps (this blocks the plan)

Run the checks in the research checklist (see the table in the research notes, "Recognise your apps") and paste the output back to the team. The research wrote one script that runs these checks and both timed Blender runs and writes one report: `research/toolchain-fixtures/step0_pc_tests.ps1` (research Follow-up F9). We need:

- Your operating system and version. The maker has decided on a Windows PC (D-10; charter [1]). The research did not measure it, so every Windows number stays UNVERIFIED until the report from your PC is in the repo (W-28).
- Which of these apps are installed, with versions: DaVinci Resolve (Free or Studio), Kdenlive, Shotcut, OpenShot, Inkscape, GIMP, Krita, Blender, Audacity.
- Whether ffmpeg and ImageMagick run from a terminal.
- CPU, RAM, graphics card and its video memory, free disk space, and whether you have a pen tablet.

Two answers change the plan. Blender 5 needs Apple Silicon on a Mac [24][30]. Resolve's External scripting setting is Studio-only in Blackmagic's manuals [110][111][112], so on the Free edition note whether it is missing or greyed out (see Decision 1).

The charter also names the ArtCraft Crafting Apps as refinement layers [1]. This track does not cover them. The craft-visual and craft-motion tracks do.

**Shell.** The commands in this playbook use Unix-style syntax. The research ran them on Ubuntu in a sandbox, not on your computer [100]. Which shell you use is Decision 0 below. Windows forms are marked `TODO(verify on the maker's PC)` where they exist; the rest are not yet written.

### Step 1: Make the project folder

Keep the project in the GitHub repository the charter names [1]. It is public by the maker's choice (D-14, D-26), so it holds only text, scripts and ID-keyed manifests. The cloud session is temporary, so the repo is the safe copy of those [1]. The research proposes these folders: `exercises/` (one folder per exercise, `ex01`, `ex02` and so on), `looks/` (saved colour recipes), `layers/` (cut-out PNG files), `licences/` (a saved copy of each licence page, with the date you saved it), and `credits.txt`. Add a `README.md` that names every tool and its version. Commit only text, scripts and manifests with IDs (D-14): scans, audio, video and renders never enter git, so `layers/` holds only stock or synthetic exercise cut-outs, never a cut-out of one of her photos. The repo stays public (D-26; O-13 is answered), so nothing personal is ever committed: no names, no addresses, no photos, no audio, no video.

### Step 2: Install or find ffmpeg and ImageMagick

ffmpeg is the glue that most steps depend on [62][63]. The ffmpeg project ships source code only. Windows builds come from third parties such as gyan.dev or BtbN [62]. Some projects warn about look-alike download sites [45], so download from official sites only. ImageMagick has Windows binaries [64]. Check what runs with `ffmpeg -version` and `magick -version` (older ImageMagick installs use `convert`), and write the results in your README. The Kdenlive 26.08.2 Windows package ships `bin\melt.exe` (MLT 7.43.0) and `bin\ffmpeg.exe` (FFmpeg 8.1.1 with libx264, libx265, libass), so no separate ffmpeg or MLT install is needed on Windows; the standalone download unpacked anywhere is enough to render [104].

### Step 3: Prepare photos in a batch

Practise with stock or synthetic images now. Real photos come in only after the pipeline is locked [1]: the P-LOCK process lock is Sat 14 Nov 2026 and covert collection starts Sun 15 Nov (D-13, W-10).

When real photos arrive, scan at the highest resolution you can. The research's rule of thumb is at least 1.5 times your output width, so a camera move can crop without going soft: 2880 px wide for 1080p [100]. The register prepares stills at 3840 px on the long edge (W-15) and the master is 1080p, so the research's 5760 px figure for 4K is dropped (4K is not needed). Scan masters follow W-27: 16-bit TIFF at 600 ppi, fronts and backs at the same sitting.

Crop every photo to 16:9 in one ImageMagick batch [64]. A 3000×2000 test photo came out at 3840×2160 this way [100]:

```
mogrify -path out/ -resize 3840x -gravity center -crop 3840x2160+0+0 +repage -quality 92 in/*.jpg
```

On ImageMagick 7 the command starts with `magick mogrify` [100]. Keep the originals in their own folder and never overwrite them. Check the result with `identify -format '%f %wx%h\n' out/*.jpg`.

### Step 4: Make a Ken Burns move by script

A Ken Burns move is a slow push-in or pan across a still photo. Two rules come from the tests [100]:

- **Crop to the output shape first.** On a 3:2 photo, ffmpeg's `zoompan` stretched the picture by about 18 percent. A circle came out 641 by 541 pixels.
- **Upscale before you zoom.** `zoompan` moves in whole pixels, so a larger source keeps the motion smooth. This is the usual workaround. The research did not test the case without the upscale [63].

A five-second push-in at 24 frames a second is the command below. The recipe file was tested at 25, UNVERIFIED at 24: its `fps` and its `d` (the frame count of the five seconds) still hold the 25 values, and the 24 values (`d=120`, `fps=24`) stay UNVERIFIED until `recipes/r1_kenburns.sh` is re-run at 24 (W-14). It is a proof tool: `zoompan` snaps to whole pixels, so it is not used for delivered shots (W-41; `playbooks/cinematic-quality.md`) [100]:

```
ffmpeg -loop 1 -i photoA.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z='min(1+0.0008*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1920x1080:fps=24,format=yuv420p" -t 5 -c:v libx264 -crf 18 kbA.mp4
```

Join two clips with a one-second dissolve using ffmpeg's `xfade` filter [63]. `recipes/r1_kenburns.sh` has the full set [100]; the file was tested at 25, UNVERIFIED at 24, so its `fps` and `d` values are the 25 ones until it is re-run and patched by hand to the 24 values (`fps=24`, and `d=120` for five seconds).

### Step 5: Cut out layers for parallax

To move a foreground differently from a background, cut the photo into layers. There are three routes:

- **By hand** in GIMP 3.2 or Krita: a selection, a layer mask, then export a PNG with transparency. This gives the most control, and nothing leaves the machine [46][51].
- **Assisted, locally.** `rembg` removes the background of a main subject (MIT licence) [73]. SAM 2 can click out several objects (Apache-2.0) [74].
- **Depth.** Depth Anything V2 Small is Apache-2.0. The Base and Large models are CC-BY-NC-4.0 [72], so ask the maker before using them.

Filling in the background behind a cut-out invents pixels. Keep the fill minimal, keep the original, and label the result as a reconstruction [1].

### Step 6: Parallax in Blender by script

Put each layer on a flat plane at its own distance, slide the camera, and render the frames. The near layers then move more than the far ones, which is parallax [71]. The tested script is `recipes/r2_parallax.py` [100]. `recipes/r2_param.py` is the same scene, with its frame count, resolution, samples and folders set by environment variables, for the timed runs in Exercise 5. Three settings matter most:

- **Set the view transform to Standard.** Blender's default, AgX, washed out the test photos. Standard kept their colours [100].
- **Draft at 640×360 with four samples; finish at 1080p.** Fifty frames at 640×360 took about 64 to 66 seconds on four CPU cores with no graphics card [100]. A 1080p frame has about nine times the pixels. Measured in the sandbox, a 1080p frame took about 11 seconds, so a 30-second shot at 24 frames a second (720 frames) would take about 2.2 hours (research notes, Follow-up F2; the research counted 750 frames, its count at the rate its tests ran at, 25). Your PC is not measured yet; Exercise 5 measures it.
- **Run it from a terminal with no window.** Blender's own command line is `blender -b -P script.py` [25]. The Windows `blender.exe` (under Wine, not on Windows itself) ran R2 in its parameterised form, `recipes/r2_param.py`, and the Linux `blender` program and the `bpy` module ran the same scene in the same sandbox (research notes, Follow-up F2). On Windows use `blender.exe`, not `blender-launcher.exe`. `pip install bpy` on Windows needs Python 3.13 exactly [102][103]. Sandbox measurements: peak memory about 0.9 GB at 640×360 and 2.5 GB at 1080p, and about 11 seconds per 1080p frame on four cores with no graphics card. Your PC's numbers come from Exercise 5.

Turn the PNG frames into a movie with `ffmpeg -framerate 24 -i renders/p_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p parallax.mp4` [100].

### Step 7: Draw lines that reveal (maps, routes, titles)

To make a route or a signature draw itself, draw it in Inkscape as one stroked centre-line path [35][36]. Inkscape does not animate on its own [35], so a script does it. The script writes one SVG file per frame, with a dash pattern that shrinks from full length to nothing, then renders each frame [65]. `recipes/r3_linedraw.py` reads the path's real length from the file. Do not type the length in by hand. The renderer used in testing ignored `pathLength="1"`, so every frame looked finished until the length was computed [66][100].

Forty-eight frames at 1280×720 took 1.9 seconds on the research machine [100]. Titles set in outline fonts will not "write" with this method, because outline fonts are filled shapes, not single lines. Use a single-line font, or trace a handwritten title with Inkscape's tracing or calligraphy tools [36]. Her script on titles and verse cards travels as shaped outlines, never live text (W-21): a Gujarati title is drawn or traced as a path, and the shaping is checked on the PC before any Gujarati string goes into a frame (W-75).

Blender can also reveal a curve or a Grease Pencil drawing with a build effect [28][29][100].

### Step 8: Assemble the chapter in the editor

Kdenlive 26.08 is the default editor [8][9]. It is built on MLT, the same engine that sits under Shotcut [14][20]. Kdenlive can save a render script that you run with `melt` [11], and an agent can write MLT XML directly and render it with `melt` [17][18].

Two traps from the tests [100]:

- **Always set the profile.** Without `-profile`, `melt` uses a PAL standard-definition frame (720×576). For the 24 fps project the profile is `atsc_1080p_24` (W-14). `recipes/r5_story.mlt` was tested at 25, UNVERIFIED at 24, so it still names the 25 profile (the same name, ending in 25) until it is re-run at 24 and patched by hand to end in 24.
- **Crop photos to 16:9 before you place them.** A 3:2 photo otherwise letterboxes.

On Windows, the same `melt.exe` is in the Kdenlive package, so the render can run from PowerShell or Git Bash. The command ran under Wine (research notes, Follow-up F10); the two shell lines below have not run on Windows. The default install folder was not verified, so the PowerShell line finds `melt.exe` first (TODO(verify on the maker's PC)).

```powershell
# PowerShell, written but NOT run on Windows. Find melt.exe first; the default install folder was not verified.
$melt = (Get-ChildItem "C:\Program Files*" -Filter melt.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
& $melt story.mlt -silent -profile atsc_1080p_24 -consumer avformat:story.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p an=1
```

```bash
# Git Bash, written but NOT run on Windows. Use the standalone download unpacked anywhere to avoid the install-folder question.
MSYS2_ARG_CONV_EXCL='*' "/c/Tools/kdenlive-26.08.2_standalone/bin/melt.exe" story.mlt -silent -profile atsc_1080p_24 -consumer avformat:story.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p an=1
```

Do the final cut by hand: timing to music, framing and the last pass.

### Step 9: Give each album its own look

Every album gets one saved colour look, so every photo from that album matches. The look comes from the album itself, not from a decade. Pick three prints from one of her real albums (from Sun 15 Nov, after P-LOCK). In each print, sample a known-white object and a skin midtone. Derive the lift, cast and grain from those samples, save the result in `looks/`, and name it after her chapter. Apply that one look to every photo from the album [1].

The research's two ffmpeg chains (a 1970s-style and a 1950s-style chain) are stock practice, not for the film. They are kept in `recipes/r7_era_looks.txt` for exercises only [63][100]. Do not colourise black-and-white photos with AI unless you label the result as a reconstruction [1]. The step from sampled values to filter settings is written and was tested on three stock prints: `research/toolchain-fixtures/derive_album_look.py` (research notes, Follow-up F14). It has not run on your prints or on Windows Python, so it stays TODO(research) until it has.

### Step 10: Sound

Build the sound in this order (W-44): the premiere's honest sound is objects, rooms, the sea's surf and the maker's hum, and sung devotion waits for April. Start from the maker's own captures in her empty house (W-10, W-70) and the hummed tune, recorded in two takes (closed-mouth and open vowel), both kept uncleaned in `originals/` (W-65). Room tone is the bed under them and never a first sound, because it vanishes on a phone speaker (W-36, W-76). Any music is a CC0 or CC BY stand-in, labelled, and only if the sound is hers (O-72); there is no AI bed. If one passed one-key-three-guards, her HER-PUBLIC line goes on top. The premiere cut has no other recorded voice of a living person (D-05, W-35); relatives' voices are April-version items (D-06). Make the final mix in REAPER, with Resolve Free's Fairlight as the fallback (W-20); the ffmpeg chain below is for proofs and the delivery check. Use only music whose licence allows public screening (see Decision 6).

Set the loudness with ffmpeg's loudness filter. The online copy is `-af loudnorm=I=-16:TP=-1:LRA=11` (-16 LUFS, -1 dBTP), and every file in the project holds -1 dBTP (W-19) [63][100]. The phone files are that online row, measured on the final MP4 after the AAC encode (W-19, W-63). The research ran its test file with an earlier, looser true-peak ceiling, so re-measure at `TP=-1`. On that test file the filter moved the level from −22.1 to −16.0 LUFS [100]. The broadcast reference is −23 LUFS [97]. A projector room with small speakers often needs something louder. Render three venue masters (-23, -18 and -16 LUFS integrated) and choose at the Mon 22 Feb venue run against sixty seconds of the hall's own room tone from the back row; if no reading can be taken, load -18 first (W-19). Use two-pass `loudnorm` with a linear second pass.

### Step 11: Captions

Draft the captions with Kdenlive's speech-to-text, which can use VOSK or Whisper [13]. Whisper is also available on its own. It runs locally after its model is downloaded, and it can print SRT files from the command line [75]. Then proofread every name and place by hand.

**Whisper on Windows.** Kdenlive's Whisper needs Python 3 installed first. On first use it downloads about 2 GB of dependencies plus a model, so set it up while online; transcription itself runs offline. On an 8 GB PC use `tiny`, `base` or `small`: `small` peaks at about 2.1 GiB and is the sensible default. `medium` and `turbo` peak at about 5.1 and 5.4 GiB and only fit with other apps closed; `large` does not fit. Check where the first `.pt` model file lands. The script reads `~\.cache\whisper`, and the manual names `%AppData%\kdenlive\opencvmodels` [116][117][118]. Offline transcription was tested on Linux with the models already in place. The Windows run is TODO(verify on the maker's PC).

**Resolve Free and captions.** Resolve Free imports an SRT and burns it in. Automatic subtitles from audio are Studio, so use Whisper for the draft [110][111][112]. Not yet seen on a real Free install.

Burn the captions into the screening file, because burned-in text is the one kind every screen shows [12][13]. Keep a sidecar `.srt` file for the archive. The research's burn-in command names a font that may not be installed on your computer. Use an OFL font (W-21): a Windows system font is fine rasterised into the video, but never embedded in a DCP subtitle track [100]. Caption layout follows W-18: two lines, at most 20 characters a second (slower for a room over 70), `FontSize=23` for Latin (about 8% line height at 1080p) with `MarginV` 20 or more inside the 90% box, with a sidecar SRT and VTT (UTF-8, single script per cue) in the archive; "42 characters a line" is a guide, and the rule is that a line fits the box in its face. Gujarati is sized by the height of its KA, not by `FontSize`: Noto Sans Gujarati passes the venue at 23 and needs 26.2 for the phone's 3.8% target, so the phone file carries its own setting (`FontSize=28`, `MarginV` 40, two lines, at most 32 characters, which fits the 90% box in both scripts, block at 68 to 86% of height). On any ffmpeg older than n9.0 burn Indic text with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in its header), never `subtitles` or `drawtext`, because the simple shaper breaks conjuncts without a warning; the ten-minute A/B on test syllables decides the PC's path and is a P-LOCK condition (W-75, W-06). Fonts are the OFL families of W-21. TODO(research): verify burn-in on Windows.

### Step 12: Export the versions from one master

From one master file, make these versions [91][95][92]; the phone files are PH1 and PH2 (W-63):

| Version | Container and codec | Main settings |
|---|---|---|
| **Screening** (TV, USB stick, projector) | MP4, H.264 High profile | Level 4.1, yuv420p, 1080p, AAC-LC 48 kHz stereo, `+faststart`, BT.709 tags |
| **Private web link** (made for the April version; not uploaded anywhere before the maker says so, D-15, W-48) | MP4, H.264 High profile | CRF 20, 12 Mbps cap at 1080p. YouTube recommends 8 Mbps for 1080p at 24 to 30 frames a second [91] |
| **Archive** | ProRes 422 HQ in `.mov`, and/or FFV1 version 3 in Matroska | Audio PCM 24-bit or FLAC. The Library of Congress lists both in its current preferred formats for moving images (the statement is undated on the page; read 2026-10-18). An MP4 counts only as a viewing copy [92][93][94] |
| **Phone files** (PH1 and PH2; for her phone by cable after her yes, and for relatives after the ledger closes, W-73, W-74) | MP4, H.264 | PH1: 1920×1080p24, High 4.1, yuv420p, BT.709 tags on the master before the burn-in, CRF 20 with an 8 Mb/s cap, AAC-LC 192 kbps, `+faststart`, `-map_metadata -1`, captions burned at the phone setting, -16 LUFS and -1 dBTP on the final MP4. PH2: 1280×720, CRF 22, 3.5 Mb/s cap, level 3.1, captions burned on the 1080 frame before the downscale. SDR only, no HEVC (its saving is the grain). `playbooks/mobile-delivery.md` owns the commands |

The screening command, as tested [100]:

```
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart deliver_usb.mp4
```

The research tested this without the `-maxrate` and `-bufsize` pair. Those two are the register's 20 Mbps cap (W-17). The register's venue file (W-17) is this command at 1080p24 with captions burned in, a neutral file name and metadata stripped, plus a Main profile, level 4.0 backup at about 8 Mbps, a 60 to 90 second venue test clip with no personal content that carries a tone ladder from 100 Hz to 3.2 kHz, and a 3-minute sound-and-stills fallback. There is no online link, cinema or festival copy until the consent ledger closes (Mon 29 Mar) and the rights log is green (W-48).

**Watch the file size.** A FAT32 USB stick cannot hold a single file over 4 GB minus one byte [96]. At about 12 Mbps video plus 256 kbps audio, that is about 46 minutes. At 20 Mbps, it is about 28 minutes [100] (the research's arithmetic). A 12-minute film at 20 Mbps is about 1.8 GB, so the premiere cut fits FAT32; the register's two sticks are FAT32 if under 4 GiB, else exFAT, in different pockets (W-52). Format the stick as exFAT, or keep each file under the limit, and test on the screen. Whether your screen takes exFAT, MKV or soft subtitles is unknown. TODO(research): no TV or projector format specification was readable.

### Step 13: Check every file

Run ffprobe on each output. For the screening file, expect H.264 High, level 4.1 (ffprobe prints it as 41), yuv420p, 1920×1080, AAC-LC at 48,000 Hz, two channels [100]:

```
ffprobe -v error -show_entries stream=codec_name,profile,level,pix_fmt,width,height,sample_rate,channels -of csv=p=0 file.mp4
```

Then check the file size against the stick's limit, and check the loudness again.

### Step 14: Rehearse on the real screen

Play the screening file from a USB stick on the actual TV or projector, with the venue's cable or adapter if you can. Keep a laptop backup: play the master in VLC or mpv, set the laptop to 1920×1080, mirror the displays, and turn off notifications and sleep [100]. The charter fixes the occasion (a mostly public gathering on 2027-02-27; D-08). The venue's screen, cable and USB behaviour are still unknown: the venue is asked by Fri 6 Nov and its written answer is due Sun 15 Nov (W-17); the venue visit uses a test clip, never the film, by Sun 17 Jan (W-56); the full rehearsal is Mon 22 Feb (W-52).

### Step 15: Archive

Keep the master file or files, the SRT and VTT caption files, the project files, the original scans and audio, the source SVG and Blender files, a README that names every tool and version, a licence and credits file, and SHA-256 checksums. Keep two physical copies and one off-site copy, where the off-site copy is a second encrypted SSD kept elsewhere; there is no cloud copy of family media (W-25). Check the checksums every year, and migrate formats before they die (research archive checklist). The preferred archive formats above come from the Library of Congress [92].

## Learn-by-doing exercises

Each exercise has a cap of about two hours, from the research notes. The research did not time the exercises one by one [100]. Practise on synthetic or stock images and your own photos, never hers: no photo of hers is used before P-LOCK on Sat 14 Nov (D-13). Keep the real hero material for the vertical slice [1]. Put each exercise in `exercises/exNN/` in the repo (public, D-26: text and scripts only, nothing of hers), and keep every command line you run.

### Exercise 1: Inventory and dry run

- **Goal:** Know what you have, and prove the batch crop works.
- **Steps:** Fill in the Step 0 table. Install or locate ffmpeg and ImageMagick (Step 2). Batch-crop five stock photos to 3840×2160 (Step 3).
- **Time:** Under 2 hours.
- **Good looks like:** `ffmpeg -version` and `magick -version` both print. Every output reads 3840×2160, a 16:9 ratio.
- **Self-check.** Bash (Git Bash or WSL2): `identify -format '%f %wx%h\n' photos_16x9/*.jpg` (on ImageMagick 7 use `magick identify`). PowerShell: `Get-ChildItem photos_16x9\*.jpg | ForEach-Object { magick identify -format '%f %wx%h\n' $_.FullName }`. TODO(verify on the maker's PC).

### Exercise 2: Ken Burns by script

- **Goal:** Three moves by script, joined by dissolves.
- **Steps:** Make a push-in on one photo, a pan on another, and a third move of your choice, each about six seconds, using Step 4. Join them with one-second `xfade` dissolves.
- **Time:** Under 2 hours.
- **Good looks like:** ffprobe reports 1920×1080, 24 frames a second (`r_frame_rate` 24/1; the project rate, W-14), H.264. If you run `recipes/r1_kenburns.sh` unchanged it writes 25, so patch it to 24 by hand first. A round object is not squashed. The slowest move shows no shimmer.
- **Self-check.** `ffprobe -v error -show_entries "stream=width,height,r_frame_rate,codec_name" -of csv=p=0 ex02_kenburns.mp4` has no shell syntax, so it runs the same in Git Bash and PowerShell. The bash-only part is the three ffmpeg lines in `recipes/r1_kenburns.sh`; in PowerShell run them one at a time, since they use no shell variables. TODO(verify on the maker's PC).

### Exercise 3: The same in the editor, with easing

- **Goal:** Rebuild Exercise 2 in Kdenlive, with keyframes that ease in and out.
- **Steps:** Keyframe the position and scale of each clip. Add one-second dissolves. Export the screening version (Step 12). Check it with ffprobe.
- **Time:** Under 2 hours.
- **Good looks like:** The speed curve starts and ends gently when you scrub it. ffprobe shows High profile, level 4.1, yuv420p, and AAC at 48 kHz. The file plays from a USB stick.

### Exercise 4: Cut-outs and fake parallax

- **Goal:** Turn one photo into foreground, middle and background PNG layers. Animate them so the near layers move more. Add one hard match cut to a second photo.
- **Steps:** Make the layers in GIMP 3.2 or Krita, or use `rembg` and then fix the edges by hand. Save each layer as a PNG with transparency. Put the layers on separate tracks in the editor and keyframe them with different distances. Cut to a second photo where a shape or colour lines up [71].
- **Time:** Up to 2 hours.
- **Good looks like:** The foreground moves at least twice as far as the background. No light halo shows on the cut edge at 100 percent zoom. The edges are feathered by one or two pixels.

### Exercise 5: Parallax in Blender by script

- **Goal:** Measure how long the Blender parallax render takes on your PC, using `recipes/r2_param.py` on the Exercise 4 layers.
- **Steps:** Put `bg.png`, `mid.png` and `fg.png` from Exercise 4 in a `layers/` folder next to `r2_param.py`. Close the Claude desktop app. Run the two timed renders below: a 640×360 draft and a 1920×1080 frame, 10 frames each at four samples. Keep the view transform at Standard. Turning the frames into a movie with ffmpeg is optional.
- **Time:** Up to 2 hours, plus render time.
- **Good looks like:** Both runs finish. A colour patch in the render matches the source photo. The render runs from a terminal with no window open.
- **Output:** Paste back both `R2_RESULT` lines and the peak working set from each run. Decisions 2 and 5 wait on these numbers.

```powershell
# PowerShell, NOT run on Windows (TODO(verify on the maker's PC)). The D:\ path is the example from research Follow-up F2; use your unzipped Blender folder.
$env:R2_DIR=(Get-Location).Path; $env:R2_NF=10; $env:R2_SPP=4; $env:R2_LAYERS='layers'
$env:R2_RX=640;  $env:R2_RY=360;  $env:R2_OUT='r640';  & "D:\blender-5.2.2-windows-x64\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r2_param.py
$env:R2_RX=1920; $env:R2_RY=1080; $env:R2_OUT='r1080'; & "D:\blender-5.2.2-windows-x64\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r2_param.py
# Peak working set (TODO(verify on the maker's PC)): run this in a second window while each render is going.
Get-Process blender | Select PeakWorkingSet64
```

If Blender does not create the output folder, make `r640` and `r1080` first (TODO(verify on the maker's PC)).

### Exercise 6: A line-draw route or title

- **Goal:** Draw a route or a signature as one stroked centre-line path in Inkscape, then make it draw itself.
- **Steps:** Draw the path. Copy its `d` attribute from Inkscape's XML editor into `recipes/r3_linedraw.py`. Run it. The Blender version, R3b, is still only in the research notes. Add easing [65][100].
- **Time:** Under 2 hours.
- **Good looks like:** The line starts, finishes and eases as designed. The last frame matches the static SVG exported from Inkscape. The script reads the length from the file, not from a number you typed.
- **Self-check (rendering the frames).** Bash: `for f in frames/f_*.svg; do rsvg-convert -w 1280 "$f" -o "${f%.svg}.png"; done`. PowerShell: `Get-ChildItem frames\f_*.svg | ForEach-Object { $png = $_.FullName -replace '\.svg$', '.png'; rsvg-convert -w 1280 $_.FullName -o $png }`. TODO(verify on the maker's PC): `rsvg-convert` may not be installed on Windows; Inkscape's command line is the alternative.

### Exercise 7: Album looks

- **Goal:** Derive one saved look from three prints of one album.
- **Steps:** Take three prints from one album (or three stock images standing in for prints). Sample a known-white object and a skin midtone in each, and write the numbers down. Derive the lift, cast and grain from them with `research/toolchain-fixtures/derive_album_look.py` (method in the research notes, Follow-up F14; on Windows it needs Python 3 with numpy and Pillow). Fill in the template in `recipes/r7_era_looks.txt` and save the filled file in `looks/`. Apply the look to one modern clip as a control and save it as `ex07_album.mp4`. Outputs: `looks/<chapter>.txt` and `ex07_album.mp4`.
- **Time:** Under 2 hours.
- **Good looks like:** The look file records the sampled values and the three prints they came from. The same look applied twice gives identical output. TODO(research): the derivation is tested on three stock prints only, so the first run on your own prints is still to do.

### Exercise 8: One floor-art line-draw card

- **Goal:** Draw one floor-art line, the primary idiom of her region (W-72), on a dark ground, and make it draw itself at the phone floor. Synthetic material only; nothing of hers.
- **Steps:** Build a dot grid (pulli) of at least 5 by 5 dots in Inkscape, or have the agent write it as a Route A seekable SVG. Draw one closed stroke round each dot, then one continuous rangoli-style line through the grid with round line caps. Stroke widths at 1080p: 4 px for the meaning line, 3 px for decoration, 6 px for dots and the repeat unit, 4 px for holes, no hairlines (W-38 decision 3). Colours: cream on indigo, or kumkum on cream (W-72). Reveal it over six seconds with an ease using `recipes/r3_linedraw.py`, the SVG line-reveal recipe of Step 7 [35][36][65][66]. Use a plain rangoli pattern: no deity, no sathiyo (swastika) form, which stays SW0 until O-66 is answered, and nothing copied from a museum scan.
- **Time:** About 2 hours. TODO(research): drawing time per card was not measured.
- **Good looks like:** The line starts, finishes and eases as designed, and the last frame matches the static SVG. Every stroke measures at least 4 px (dots 6 px) at 1080p, and the card still reads on the phone-floor chart (`mobile-delivery` Exercise 5). Use a test viewer who does not know the subject, and who would not mention it to her.

### Exercise 9: Sound and captions

- **Goal:** Forty seconds of narration over a licensed music bed, ducked, levelled and captioned.
- **Steps:** Record narration with a phone voice memo, using your own voice on a practice script. Add a CC BY or CC0 track (Decision 6). Save the credit text from the licence page into `credits.txt`. Duck the music under the voice. Apply loudness normalisation (Step 10). Draft the captions and proofread them (Step 11). Test the captions on one old phone recording of an older speaker, as well as on the clean clip: a clean clip does not test old recordings or elderly voices. Use a public-domain oral-history clip or your own voice on an old phone: not hers, not a relative's, and nothing gathered for the film (D-02, D-05). Keep that file private and do not publish it.
- **Time:** Under 2 hours.
- **Good looks like:** The loudness report is within 1 LU of the target. Captions line up within about 0.2 seconds at three spot checks. Every name is spelled right. The credit text matches the wording the licence asks for.

### Exercise 10: Mini-chapter and delivery rehearsal

- **Goal:** A 60 to 90 second chapter, exported three ways, then played on the real screen.
- **Steps:** Cut Exercises 2 to 9 into one chapter. Export the screening, web and archive versions (Step 12; `recipes/r9_deliver.sh`). Play the screening file from a USB stick on the TV or projector. Write the archive README and the SHA-256 checksums (Step 15).
- **Time:** Up to 2 hours, plus playback time.
- **Good looks like:** The file plays from the stick with sound and captions. The ffprobe output matches the profile. A checksum check passes. The archive file opens in a second player.
- **Self-check (checksums).** Bash (Git Bash or WSL2): `sha256sum chapter_usb.mp4 chapter_web_1080.mp4 chapter_archive.mov > SHA256SUMS`, then `sha256sum -c SHA256SUMS`; every file must print OK. (The three names are the research's Exercise 10 names; use your own.) PowerShell: `Get-ChildItem chapter_usb.mp4, chapter_web_1080.mp4, chapter_archive.mov | ForEach-Object { '{0}  {1}' -f (Get-FileHash $_.Name -Algorithm SHA256).Hash.ToLower(), $_.Name } | Set-Content SHA256SUMS -Encoding ascii`. Verify with `Get-Content SHA256SUMS | ForEach-Object { $h, $f = $_ -split '\s+', 2; if ((Get-FileHash $f -Algorithm SHA256).Hash -eq $h.ToUpper()) { "OK   $f" } else { "FAIL $f" } }`. TODO(verify on the maker's PC).

**Pace.** Three or four exercises a week. Four a week finishes the set by 8 November 2026, so Exercise 10 is the delivery rehearsal ahead of the process lock; three a week finishes it by 14 November 2026. Either way, the P-LOCK process lock is Sat 14 November and the slice is briefed Sun 15 November (W-06, W-07; ROADMAP-ADDENDUM.md). Re-time after Exercise 5, the first Blender render, because that is where a weak computer shows [100].

## Decisions you'll need to make

Each decision lists the options and our current lean. The lean is a suggestion for you to confirm, not a decision.

### Decision 0: Which command shell?

The tested recipes are Unix commands. Every program they call (ffmpeg, ImageMagick, Blender, Inkscape, `melt`) has a Windows build, so either route below can run them [100].

- **A. Git Bash or WSL2: the tested recipes run unchanged,** provided their programs are on that shell's path. Git Bash rewrites arguments that look like Unix paths, so set `MSYS2_ARG_CONV_EXCL='*'`. WSL2 takes about half of your RAM by default, so use it only on a PC with 16 GB or more (research notes, Follow-up F3). Windows builds of ImageMagick, Inkscape and GIMP ran under Wine but not yet from PowerShell (research notes, Follow-up F11).
- **B. Native PowerShell: the recipes need a PowerShell copy.** Every program in the stack has a Windows console program, so no Linux layer is needed (research notes, Follow-up F1 to F3). So far only the four self-checks (Exercises 1, 2, 6 and 10), the `melt.exe` call and the Blender call have a Windows form, each marked `TODO(verify on the maker's PC)`. The rest of the recipe files still need a PowerShell copy. TODO(research).

**Lean: B, PowerShell with the Windows-native programs,** which is the research's recommendation (research notes, Follow-up F3). Choose A only if Git Bash is already installed. Choose WSL2 only at 16 GB of RAM or more. Step 0 asks for your RAM and whether `wsl --status` works, which settles it.

### Decision 1: Which video editor?

- **Kdenlive 26.08.** Free and open source, on Windows, macOS and Linux [8]. Its engine can be driven by a script [11][17]. It has speech-to-text and proxies [12][13].
- **DaVinci Resolve 21 Free.** Strong colour and sound tools, with official training [2][5]. Free is limited to 8-bit footage up to 60 frames a second and UHD [2]. Studio adds more, including noise reduction, film grain and hardware encoding [3].
- **Shotcut 26.9.27.** Free, with MLT XML projects [19][20]. Less tested here.
- **OpenShot 4.0.1.** The gentlest option, but it is not built on MLT [22][23]. Not recommended for this stack.

**Lean:** Kdenlive, unless you already work fluently in Resolve. If you do, use Resolve for colour and sound, and Kdenlive for batch assembly and captions. Resolve's external scripting is Studio-only [110][111][112] (see Pitfalls).

**Where this sits in the charter's approach.** Agents generate, and the ArtCraft apps (FilmCraft, PhotoCraft and others) are the maker's refinement layer. This editor is the proven fallback the charter requires, so nothing critical may depend on an alpha app [1]. **Hand-off:** every output of this track is a PNG sequence with alpha, an MP4, an SRT or a plain SVG, so either layer can take it; exact import formats belong to craft-visual/craft-motion. FilmCraft 0.9.0 does not import plain SVG, so rasterise it to PNG first (research notes, Follow-up F5).

### Decision 2: Where do parallax moves get built?

- **Blender planes (`recipes/r2_parallax.py`).** Tested and precise, but slow to render [100].
- **Keyframes in the editor.** Quicker to learn, but not tested by the research [100].

**Lean:** Blender for the hero moves (hero shots are 5% of shots, about five in the film and four at 9 minutes, and the kitchen is the only built set; W-34), and editor keyframes for the rest. Time per route on your machine: pending the two `r2_param.py` runs from Exercise 5.

### Decision 3: Which tool draws the floor-art line?

- **Inkscape plus `recipes/r3_linedraw.py`.** The SVG line-reveal recipe of Step 7: one stroked centre-line path per line, its length read from the file, one SVG per frame, rendered from the command line [35][36][65][66]. Tested, no window.
- **An agent-written seekable SVG (Route A).** The agent writes the scene as SVG, drives `stroke-dashoffset` against `pathLength` from a seekable time function, and renders it in the cloud container (`playbooks/agent-pipeline.md`; W-72). Best for the cards in the film, because the drawing is code and can be re-run.
- **VectorCraft** (pinned v0.13.1). The maker's hand-touch layer for stable ids and data attributes (`playbooks/craft-visual.md`); never the only writer of the file (D-12).

**Lean:** Inkscape and the recipe for the exercise; an agent-written SVG for the cards in the film, with the Inkscape drawing as the fallback. **Register status (D-29, W-72, S-46):** decided. The game-world route is retired; the look is her region's floor-art line drawn at the phone floor, and no deity is drawn (W-61).

### Decision 4: Which raster editor for cut-outs?

- **GIMP 3.2.6.** Layer masks, and a standard Python 3 interface since 3.0 [46][47][48]. The batch procedure name is unverified.
- **Krita 5.3.4.1.** Painting, masks and frame-by-frame animation. Its Python runs only inside the open program [51][54].
- **Photopea.** A web app. Avoid it for family photos [55].
- **ImageMagick.** Batch work only [64].

**Lean:** GIMP 3.2 or Krita, whichever you already have. ImageMagick for every batch.

**Where this sits in the charter's approach.** The ArtCraft apps (PhotoCraft and others) are the maker's refinement layer. GIMP, Krita and ImageMagick are the proven fallback the charter requires, so nothing critical may depend on an alpha app [1]. **Hand-off:** every output of this track is a PNG sequence with alpha, an MP4, an SRT or a plain SVG, so either layer can take it; exact import formats belong to craft-visual/craft-motion. PhotoCraft 0.9.0 reads single PNGs and SVG, not image sequences (research notes, Follow-up F5).

### Decision 5: Where do heavy renders run?

- **On your laptop.** The research measured this on a four-core CPU with no graphics card, so it is slow [100]. Blender's stated minimum includes a graphics card with 2 GB of video memory [30]. Your machine's time per frame is pending the two `r2_param.py` runs from Exercise 5.
- **In the cloud.** The charter asks for heavy work in the cloud wherever possible, because memory is tight on the maker's Windows PC [1]. The research did not test a cloud render path. A cloud route moves your files off your machine, and the charter says nothing personal is uploaded without your explicit say [1].

**Rule: Scripts travel, photos don't.** Agents write and test every script in the cloud on stock or synthetic images. The identical script then runs on your PC against the real photos, from a terminal with the Claude desktop app closed. The memory problem the charter records is the app, not ffmpeg or Blender, and overnight command-line renders do not need the app running [1]. Every photo set carries `cloud: none` by default and only the maker raises it; preview proxies (about 768 px) go to the container only after the account's model-improvement setting is off, and no full-size family photo, scan or master ever leaves the VeraCrypt container except to the second SSD (D-15, W-24) [1]. A rented GPU is for non-family imagery only, Secure Cloud with an encrypted volume and the maker's recorded OK, never Community Cloud (W-23). The numbers support the rule: Blender at 1080p peaks near 2.5 GB, which fits an 8 GB PC once the Claude app is closed (research notes, Follow-up F2).

### Decision 6: Which music?

- **Free licences that clearly allow public screening and a private link.** Kevin MacLeod's incompetech tracks are CC BY 4.0. You must give credit, and his FAQ allows live productions and monetised YouTube [76][79]. Freesound sounds licensed CC0 or CC BY are fine. Avoid CC BY-NC [78][80]. The Sonniss GDC bundles are royalty-free, need no credit, and forbid AI training [82]. Kenney's game assets are CC0; its audio packs were not checked [83].
- **AI-generated music.** Suno's free tier is for personal, non-commercial use, and Suno assigns no ownership to free users [88]. Meta's MusicGen weights are non-commercial [90]. The US Copyright Office has published on AI and copyright, but the research did not read its conclusions [89]. **Closed for the premiere (W-44, W-79), and no AI voice of any devotional text in Gujarati, Braj or Sanskrit, ever.**
- **Commercial songs from her life.** These need a recording licence and a publishing licence for any public or online showing. An unlisted YouTube link can still be flagged. Options, safest first: a licensed substitute with a similar mood; your own performance of the tune, only when the hum case (HC-1 to HC-7) allows it (W-65, W-79); or no music at all [100]. An offline private showing is not an option for the premiere, because the occasion is a public screening (D-08). Under only-me the lean is no licensed song; at most two, with sync and master, and only if the maker accepts that publishers and labels learn a film exists (W-44).

**What the licence texts say** (read 2026-10-18; research notes, Follow-up F8; not legal advice):
- **Mixkit music** (free licence) [119]: public performance is granted "on any web or social media platform", and no venue screening is listed. Use Mixkit music for the private link only, unless Mixkit confirms in writing.
- **Mixkit sound effects** [119]: allowed in filmmaking, including films shown on TV, on DVD or by video on demand.
- **Pixabay** [120]: allowed for a film. Keep the download record. For the online copy, avoid tracks with the shield icon: they are registered with Content ID and can trigger claims.
- **Zapsplat and Musopen** [141]: both sites refused our requests (HTTP 403). Their licences are not read.
- **Suno** [121][140]: paid-tier downloads may be shown at a non-commercial premiere under the terms as read. Pro allows 20 song downloads a month and Premier 60; Free allows none, and free-tier output may not be shown. Kept as a record: AI music is closed for the premiere (W-44, W-79).
- **For the premiere**, prefer licences that name public performance: CC BY 4.0, whose "Share" includes public performance [79]; Freesound CC0 or CC BY items [80], only as labelled stand-ins and only if the sound is hers (O-72, W-79). The Suno reading above is a record, not a route.

**Lean:** under W-44 the premiere has no licensed song (lean none, O-29) and no AI bed; CC0 or CC BY only as a labelled stand-in and only if the sound is hers (O-72). No CC BY-NC. For her favourite songs, use a substitute, or silence plus kitchen sound; a hummed tune is a performance of the work, so the hum case (HC-1 to HC-7) is placed first (W-65, W-79). The premiere is a mostly public gathering (charter), so every track must clear public performance; one paid rights-consult hour, asked as a hypothetical, is booked by Fri 4 Dec once the country is known (W-55), and every cue is decided by Mon 14 Dec (W-44). TODO(research): several licences were not read (see the open items list below).

**Register status (W-44, W-65, W-79):** default. The premiere's honest sound is objects, rooms, the sea's surf and the maker's hum; sung devotion waits for April. The spine is, in order: silence and room tone (never as a first sound); the tune she sang to the maker, hummed by the maker in week 1, uncleaned, in two takes (closed-mouth and open vowel), both used; the maker's own captures in her empty house; CC0 or CC BY only as a labelled stand-in and only if the sound is hers (O-72). No AI bed, no licensed song (lean none, O-29), no sung recording of any kind before April, no commissioned musician for the premiere (name-free briefs, April only), and no raga name on screen or in credits. Route decided by Mon 30 Nov; every cue and the hum case decided by Mon 14 Dec; substitutes locked Fri 8 Jan. Udio cannot supply a file (downloads disabled 2025-10-29), so treat it as closed; Suno and every other AI music route are closed for the premiere. Never use AI for her songs, for any devotional text, or for an imitation of a real singer.

### Decision 7: Which export set?

- **Screening MP4** (H.264 High, level 4.1, 1080p) [91][95].
- **Private web link** (12 Mbps cap at 1080p; made for the April version, with no link before the consent ledger closes, W-48) [91].
- **Archive** (ProRes 422 HQ in MOV, or FFV1 in MKV) [92].
- **Phone files** (PH1 at 1080p, PH2 at 720p; W-63) [91].

**Lean:** All four, from one master, plus the laptop HDMI backup (Step 14); the phone files are never a second edit (W-63). **Register status (W-15, W-17):** decided as the working default. The master is 1080p ProRes 422 HQ and a 2K Flat DCP is derived from it if the venue needs one; 4K is not needed (UHD only for single hero shots if a 4K cinema is booked). The screening MP4 is the 1080p24 venue file with the Main 4.0 backup described in Step 12.

### Decision 8: Burned-in captions or soft subtitles?

- **Burned-in.** Every screen shows them, and nobody can switch them off [12][13].
- **Soft subtitles** (a separate track the screen can switch on or off). TV support is unverified [100].

**Lean:** Burned-in captions for the screening file. A sidecar `.srt` for the archive. Soft subtitles only after a test on the real screen. **Register status (W-18):** decided as the working default. Burned-in open captions in the venue file, with a DCP subtitle track only for a later cinema, using an OFL font; three sizes (20, 23, 26) are tested from 3 m in week 9 and from the venue's back row at the visit (by Sun 17 Jan). The phone files carry their own caption burn (`FontSize=28`, `MarginV` 40), and Indic text goes through the `ass` filter before ffmpeg n9.0 (W-18, W-75).

### Decision 9: The venue and screen (the charter's open decision)

The charter fixes the occasion: a mostly public gathering on 2027-02-27 (D-08). The venue's screen, cable and USB behaviour are still unknown, and they decide the final export [1]. **Register status (W-17, O-21):** default. The venue is asked by Fri 6 Nov with the neutral FQ12 ask; its written answer, due Sun 15 Nov, decides file or DCP. Until then, build the 1080p24 venue file and the Main 4.0 backup, and treat the archive master as the one source. If no venue is booked by Sun 17 Jan, assume the worst case (laptop, HDMI, TV) from 15 Nov. **Lean:** Do not choose the final export until the venue and screen are known. The venue test kit (research notes, Follow-up F15) turns the screen questions into a short check.

## Pitfalls

**Version drift.** Blender 5.2 changed several calls from the older tutorials. The sequencer is `strips`, not `sequences`. `new_effect()` takes `length`, not `frame_end`. Video output needs the media type set to video before the file format is set to FFMPEG [100]. The Grease Pencil build effect's Python names are GROW, SHRINK and FADE, but the manual says Grow, Shrink and Vanish [28][100]. GIMP 3.0 replaced Python-fu with standard Python 3, and GIMP 2.10 plug-ins and scripts break [47][48]. Inkscape removed pre-1.0 options such as `--without-gui`, so old forum answers mislead [34][37]. Kdenlive's keyframes were reworked in versions 25 and 26 [12][99]. Treat any tutorial older than 2024 as concept only.

**Colour and geometry traps (all measured).**

- Blender's default view transform desaturates photos. Set Standard [100].
- A 3:2 photo stretches in `zoompan` and letterboxes in `melt` unless you crop it first [100].
- `melt` defaults to a PAL frame (720×576) unless you set the profile [100].
- Blender's OBJ importer assumes Y-up, so a model exported from a Z-up tool arrives on its side unless you set forward axis Y and up axis Z [100].
- An SVG imported into Blender comes in at about 0.000282 metres per pixel, so a bevel of 0.02 metres swamps the drawing [100].
- A renderer that ignores `pathLength` will show every line as finished [66][100].

**"Has a Python interface" does not mean "runs without a window."** Krita, Audacity and Resolve Free run their scripts inside the open program [54][61]. The research ran these headless only: ffmpeg, ImageMagick, Blender's Python module, Inkscape's command line, `melt` and Synfig's command line [100]. Glaxnimate's pip package would not import on Ubuntu 24.04 without extra libraries [39][100].

**Resolve's external scripting is Studio-only.** The 21 and 21.1 Reference Manuals say "External Scripting Using: (Resolve Studio only)", and the 21.1 features guide lists "Scripting API: Studio" [110][111][112]. The 21.1 MCP server for AI assistants is also Studio. On Free, agents hand the maker timeline files (OTIO, FCPXML, FCP7 XML, EDL, DRT, AAF) plus ffmpeg post-processing. Subtitle tracks, SRT/VTT import and export and burn-in carry no Studio mark; speech-to-subtitle does. Not yet seen on a real Free install: check `Preferences > System > General > External scripting using` on yours. The README mirror [6] and a third-party README [7] read the other way; the 21 and 21.1 manuals are the more specific source, so this playbook follows them.

**Free-tool limits.** Kdenlive's hardware-accelerated presets are marked experimental [11]. Resolve Free lacks the Studio-only tools, such as the AI Neural Engine features, noise reduction and film grain [2][3]. Shotcut's licence is not named on its download page [19]. TODO(research): confirm it.

**Hardware floors.** Blender 5 needs at least four cores, 8 GB of RAM, and a graphics card with 2 GB of video memory and OpenGL 4.3 or Vulkan 1.3 [30]. Shotcut asks for four cores and 8 GB for HD [20]. Keep originals on an external drive, never edit straight from a USB stick, and plug the laptop in with sleep turned off for overnight renders [100].

**Export and screens.**

- FAT32 cannot hold a file over 4 GB [96]. Format the stick as exFAT, or split the file (Step 12).
- Variable-frame-rate phone clips can drift against the timeline. Convert them to constant frame rate first. The research's command for this is untested [100].
- 4K needs HEVC, or H.264 at level 5.1, and must be tested on the real screen [95]. The register does not need 4K (W-15).
- TODO(research): no TV or projector format specification was readable. Test exFAT, MKV, soft subtitles and HDMI on the real hardware.

**Look-alikes and web tools.**

- A YouTube channel named "ShotCut Video Editor" is not the official Shotcut. Its listing shows AI-template adverts. Use the official site [21][98].
- Photopea runs in a browser. Its "nothing is uploaded" claim is the vendor's statement, not an audit [55].
- "AI photo animator" websites upload your photos to someone else's servers. That needs the consent of you and of everyone pictured [1].

**Music.** "Royalty-free" does not mean free to show in public, and it does not mean no credit. Read the licence page, not the search result. The YouTube Audio Library is safe only on YouTube [77]. Pixabay's licence needs no credit, but it does not allow selling or distributing the content alone [81]. FreePD closed in 2025 [84]. BBC Sound Effects' stated terms mention personal or educational projects, or a paid licence. A public screening is not confirmed [85]. Zapsplat and Musopen were not read: both sites refused our requests [141]. Openverse and ccMixter were not read.

**Surprise leaks.** The charter forbids anything that could tip her off, including shared devices, cloud photo libraries and family group chats [1]. Do not let your project folder sync to a cloud photo library. Do not post a "render finished" message in a family chat. Use neutral file names on any shared machine. The register adds the rest of the routine (W-26): a separate Windows account for the project, OneDrive backup off for Desktop, Documents and Pictures, recent-file lists and caches cleared after every session, and the Mum-test on every shared device now and monthly. Whether she shares the PC or the room is still pending (O-03).

## Best references (top 8)

1. **Blender 5.2 LTS Manual: Rendering From The Command Line.** https://docs.blender.org/manual/en/latest/advanced/command_line/render.html [26]. Read it before your first overnight render. It gives the order of the command-line flags, which matters.
2. **Kdenlive 26.08 Manual: Rendering.** https://docs.kdenlive.org/en/exporting/render.html [11]. Render presets and "Generate Script", which is how you queue overnight renders.
3. **Kdenlive Manual: Speech to Text.** https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html [13]. Captions with VOSK or Whisper, inside the editor.
4. **MLT: melt documentation.** https://www.mltframework.org/docs/melt/ [17]. What Kdenlive does underneath, and how to render a project with no window.
5. **FFmpeg Filters Documentation.** https://ffmpeg.org/ffmpeg-filters.html [63]. Read the `zoompan`, `xfade`, `subtitles` and `loudnorm` sections before Steps 4, 10 and 11.
6. **Inkscape Tutorials.** https://inkscape.org/learn/tutorials/ [36]. The official index, including the Interpolate, Tracing and Calligraphy tutorials.
7. **CSS-Tricks: How SVG Line Animation Works** (Chris Coyier, 2014). https://css-tricks.com/svg-line-animation-works/ [65]. Still the clearest plain explanation of the dash-offset trick. The date is old, but the method still holds.
8. **Library of Congress: Recommended Formats Statement, Moving Image Works** (the current statement; undated on the page, read 2026-10-18). https://www.loc.gov/preservation/resources/rfs/moving.html [92]. Which archive formats to keep, and why an MP4 is a viewing copy only.

**Video tutorials are thin.** The research could not verify any video for a Ken Burns move in an editor, 2.5D parallax in Blender, SVG line-drawing, photo morphing or era grading [98][99]. The one video with a readable date and length is the Nuxttux "Keyframe Interpolation" tutorial, 5 minutes 34 seconds, uploaded 29 May 2025. The research read only its page details, not its content, so the title is all we know [99]. https://www.youtube.com/watch?v=F1h6Kg-WLDE. The Arkengheist rotoscoping video is from 2020 and shows an older Kdenlive, so use it for ideas only [99]. Blender Guru's 2026 beginner course runs over four hours, and its exact Blender version is unverified [98]. TODO(research): re-fetch the channel listings slowly, and open the shortlisted videos.

## Sources
[1] Project charter — CHARTER.md — undated (local file) — principles incl. "prefer scriptable tools", real memories stay real, dignity and consent.

[2] DaVinci Resolve (product page) — https://www.blackmagicdesign.com/products/davinciresolve — Resolve 21 / "What's New in 21.1" — Free = 8-bit up to 60 fps, UHD; Studio adds 10-bit 120 fps and >4K. (also WebFetch)

[3] DaVinci Resolve Studio — https://www.blackmagicdesign.com/products/davinciresolve/studio — Studio $295 excl. tax/shipping; Studio feature list incl. remote scripting API, multi-GPU, H.264/H.265 hardware acceleration, Neural Engine.

[5] DaVinci Resolve — Training — https://www.blackmagicdesign.com/products/davinciresolve/training — official video series with durations; Resolve 20 training books (PDF).

[6] DaVinci Resolve Scripting README (mirror of Blackmagic's README.txt by X-Raym) — https://gist.githubusercontent.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8/raw — "Last Updated: 24 Jul 2026" — Console/Scripts menu, `-nogui`, API superset for Free and Studio, `ImportTimelineFromFile` formats, render functions.

[7] pydavinci README — https://raw.githubusercontent.com/pedrolabonia/pydavinci/main/README.md — undated, Resolve 18 era, third party — "External scripting … requires Resolve Studio (Free version does not allow API access)".

[8] Kdenlive — Downloads — https://kdenlive.org/download/ — 26.08.2; Windows 10+, macOS 13+, AppImage/Flatpak.

[9] Kdenlive — News — https://kdenlive.org/news/ — 26.08.2 (2026-10-13); 26.12 in development; 26.04.3 (2026-07-06) MLT command-execution hardening.

[11] Kdenlive manual — Rendering — https://docs.kdenlive.org/en/exporting/render.html — manual 26.08 — presets (ProRes, FFV1, H.264, H.265, AV1), Generate Script, `melt script.mlt`, proxies, experimental hardware presets.

[12] Kdenlive manual — What's New — https://docs.kdenlive.org/en/more_information/whats_new.html — keyframe easing modes, curve editor, subtitles, mask effects, proxies in preview.

[13] Kdenlive manual — Speech to Text — https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html — VOSK and Whisper subtitles.

[14] Kdenlive manual — Introduction — https://docs.kdenlive.org/en/getting_started/introduction.html — MLT, Glaxnimate integration (22.08), nested timelines (23.04).

[17] MLT — melt documentation — https://www.mltframework.org/docs/melt/ — (WebFetch) producers, filters, consumers, `xml` consumer.

[18] MLT — XML documentation — https://www.mltframework.org/docs/mltxml/ — producers, playlists, multitracks, filters, consumers.

[19] Shotcut — Download — https://www.shotcut.org/download/ — (WebFetch) 26.9.27; platforms.

[20] Shotcut — FAQ — https://www.shotcut.org/FAQ/ — minimum requirements; projects saved as MLT XML; Preview Scaling and Proxy.

[21] Shotcut — home and news — https://www.shotcut.org/ ; https://www.shotcut.org/blog/ — 26.9 "Auto Duck and Adjustment Clip" (2026-09-27), 26.8, 26.6, 26.4; releases about every two months.

[22] OpenShot — Download and User Guide — https://www.openshot.org/download/ ; https://www.openshot.org/user-guide/ — v4.0.1; GPL v3 or later.

[23] libopenshot C++ API — https://www.openshot.org/files/libopenshot/ — version 0.7.0; Timeline, Clip, Keyframe, FFmpegReader/Writer.

[24] Blender — Releases — https://www.blender.org/download/releases/ — (WebFetch) 5.2 LTS 2026-07-14; 5.1 2026-03-17; 5.0 2025-11-18; 4.5 LTS 2025-07-15.

[25] Blender 5.2 LTS Manual — Command Line Arguments — https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html — `-b`, `-P/--python`, `--python-exit-code`, `-E`, `--factory-startup`.

[26] Blender 5.2 LTS Manual — Rendering From The Command Line — https://docs.blender.org/manual/en/latest/advanced/command_line/render.html — page "Last updated on 2026-10-17"; argument order; `-f`, `-a`, `-o`, `-F`.

[28] Blender 5.2 LTS Manual — Grease Pencil Build Modifier — https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html

[29] Blender 5.2 LTS Manual — Trim Curve Node — https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/trim_curve.html

[30] Blender — System Requirements — https://www.blender.org/download/requirements/ — minimum/recommended; Apple Silicon only from 5.0; pen tablets recommended for Grease Pencil.

[32] Inkscape 1.4.4 release page — https://inkscape.org/release/ (redirects to /release/inkscape-1.4.4/) — released 2026-05-06; Windows on Arm; macOS extension-CLI known issue (CVE-2025-15523).

[34] Inkscape Wiki — Using the Command Line — https://wiki.inkscape.org/wiki/Using_the_Command_Line — (WebFetch) `--actions` needs `--batch-process`; shell mode.

[35] Inkscape — Learn: Animation — https://inkscape.org/learn/animation/ — "Inkscape does not support animation natively".

[36] Inkscape — Tutorials index and Interpolate tutorial — https://inkscape.org/learn/tutorials/ ; https://inkscape.org/doc/tutorials/interpolate/tutorial-interpolate.html — official tutorials (Basic, Shapes, Advanced, Tracing, Calligraphy, Interpolate…).

[37] Inkscape Wiki — Release notes 1.4 — https://wiki.inkscape.org/wiki/Release_notes/1.4 — "Many new actions have been added", new command line options.

[39] Glaxnimate — Scripting — https://glaxnimate.org/contributing/scripting/ — console, plugins, `pip install glaxnimate`, example.

[45] OpenToonz — https://opentoonz.github.io/e/ ; https://raw.githubusercontent.com/opentoonz/opentoonz/master/README.md ; https://opentoonz.readthedocs.io/en/latest/ — free for commercial and non-commercial use; manual 1.7.1; "official source only" warning.

[46] GIMP — Downloads — https://www.gimp.org/downloads/ — 3.2.6 (2026-09-10); macOS 11+; AppImage needs Debian 13+.

[47] GIMP 3.0 Release Notes — https://www.gimp.org/release-notes/gimp-3.0.html — new API, Python 3, plug-in breakage.

[48] GIMP 3.2 Release Notes — https://www.gimp.org/release-notes/gimp-3.2.html — scripting API additions; API stable across 3.x.

[51] Krita — Download — https://krita.org/en/download/ — 5.3.4.1 released 2026-10-07; system requirements.

[54] Krita Manual — Introduction to Python Scripting — https://docs.krita.org/en/user_manual/python_scripting/introduction_to_python_scripting.html — Scripter inside Krita.

[55] Photopea — Learn: Introduction — https://www.photopea.com/learn/ — vendor statement on local processing.

[56] Withdrawn 2026-10-19 (D-29): a game-world modelling tool page. The number is kept so that other citations resolve.

[58] Withdrawn 2026-10-19 (D-29): a game-world modelling tool page. The number is kept so that other citations resolve.

[59] Withdrawn 2026-10-19 (D-29): a game-world modelling tool page. The number is kept so that other citations resolve.

[61] Audacity Manual — Scripting; Macros — https://manual.audacityteam.org/man/scripting.html ; https://manual.audacityteam.org/man/macros.html — legacy development manual.

[62] FFmpeg — Download — https://ffmpeg.org/download.html — (WebFetch) 9.0.2 (2026-09-18), 8.1.3 (2026-09-21); source only, Windows/macOS builds from third parties.

[63] FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html — zoompan, xfade, subtitles, lut3d, colorbalance, curves, loudnorm.

[64] ImageMagick — Download; Command-line Processing — https://imagemagick.org/download/ ; https://imagemagick.org/command-line-processing/ — 7.1.2-34 AppImage; `magick`.

[65] CSS-Tricks — How SVG Line Animation Works (Chris Coyier) — https://css-tricks.com/svg-line-animation-works/ — 2014-02-18.

[66] MDN — stroke-dashoffset — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/stroke-dashoffset — resolved against `pathLength`.

[71] Wikipedia — Match cut; Ken Burns effect; Parallax scrolling; Twelve basic principles of animation — https://en.wikipedia.org/wiki/Match_cut ; https://en.wikipedia.org/wiki/Ken_Burns_effect ; https://en.wikipedia.org/wiki/Parallax_scrolling ; https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation — concept definitions (match cut and "graphic match"; panning/zooming over stills; layer parallax; slow in/slow out).

[72] Depth Anything V2 README — https://raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md — Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0.

[73] rembg README — https://raw.githubusercontent.com/danielgatis/rembg/main/README.md — MIT; CLI `rembg i`.

[74] SAM 2 README — https://raw.githubusercontent.com/facebookresearch/sam2/main/README.md — Apache-2.0 model and code.

[75] Whisper README; whisper.cpp README — https://raw.githubusercontent.com/openai/whisper/main/README.md ; https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/README.md — MIT; `whisper audio.flac --model turbo`.

[76] incompetech — Music FAQ — https://incompetech.com/music/royalty-free/faq.html — CC BY 4.0; credit format; live productions allowed.

[77] YouTube Help — Use music and sound effects from the Audio Library — https://support.google.com/youtube/answer/3376882 — attribution; Content-ID-safe; no off-platform legal guidance.

[78] Creative Commons — FAQ — https://creativecommons.org/faq/ — meaning of NonCommercial.

[79] Creative Commons Attribution 4.0 legal code — https://creativecommons.org/licenses/by/4.0/legalcode.en — (WebFetch) "Share" includes public performance; attribution rules.

[80] Freesound — FAQ — https://freesound.org/help/faq/ — (WebFetch) CC0, CC BY, CC BY-NC; attribution wording.

[81] Pixabay — Content License summary — https://pixabay.com/service/license-summary/ — (WebFetch) no attribution; no standalone redistribution.

[82] Sonniss — GDC Game Audio Bundles — https://sonniss.com/gameaudiogdc/ — (WebFetch) royalty-free, no attribution, no AI training; GDC 2024 latest on that page.

[83] Kenney — Support (licence FAQ) — https://kenney.nl/support — CC0.

[84] FreePD — https://freepd.com/ — closure notice (2008–2025).

[85] BBC Sound Effects — https://sound-effects.bbcrewind.co.uk/licensing — "personal/educational projects, or licence them for use".

[86] Mixkit — License — https://mixkit.co/license/ — per-item-type licences; terms not extractable in round 1; read in round 2 as [119].

[88] Suno — Terms of Service — https://suno.com/terms — (WebFetch) revised 2026-08-10, effective 2026-09-03.

[89] US Copyright Office — Copyright and Artificial Intelligence — https://www.copyright.gov/ai/ — (WebFetch) Part 2 (Copyrightability) published 2025-01-29.

[90] Meta AudioCraft README — https://raw.githubusercontent.com/facebookresearch/audiocraft/main/README.md — (WebFetch) code MIT; weights CC-BY-NC 4.0.

[91] YouTube Help — Recommended upload encoding settings — https://support.google.com/youtube/answer/1722171 — MP4, H.264 High, AAC-LC 48 kHz, bitrates, BT.709.

[92] Library of Congress — Recommended Formats Statement, Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — current RFS, undated on the page, read 2026-10-18; FFV1 v3/Matroska, ProRes/QuickTime, MP4 as viewing proxy.

[93] RFC 9043 — FFV1 Video Coding Format Versions 0, 1, and 3 — https://www.rfc-editor.org/rfc/rfc9043.html

[94] RFC 9559 — Matroska Media Container Format Specification — https://www.rfc-editor.org/rfc/rfc9559.html

[95] Wikipedia — Advanced Video Coding (levels table) — https://en.wikipedia.org/wiki/Advanced_Video_Coding — level 4.1 ≈ 1080p30; 4.2 ≈ 1080p64; 5.1 ≈ 4K31.7.

[96] Wikipedia — File Allocation Table — https://en.wikipedia.org/wiki/File_Allocation_Table — FAT32 max file 4 GB − 1.

[97] Wikipedia — EBU R 128 — https://en.wikipedia.org/wiki/EBU_R_128 — target −23 LUFS.

[98] YouTube channel listings read on 2026-10-18 (titles, lengths, relative ages only) — https://www.youtube.com/@BlenderGuru/videos ; https://www.youtube.com/@DefaultCube/videos ; https://www.youtube.com/@BlenderStudio/videos ; https://www.youtube.com/@grabbitt/videos ; https://www.youtube.com/@CaseyFaris/videos ; https://www.youtube.com/@nuxttux/videos ; https://www.youtube.com/@LogosByNick/videos ; https://www.youtube.com/@DaviesMediaDesign/videos ; https://www.youtube.com/@Audacity/videos ; https://www.youtube.com/@ShotcutVideoEditor/videos (look-alike, not official).

[99] YouTube video pages with readable metadata — https://www.youtube.com/watch?v=gcIKU4KxfLk (Arkengheist 2.0, Rotoscoping, 16:09, 2020-11-21) ; https://www.youtube.com/watch?v=F1h6Kg-WLDE (Nuxttux Creative Studio, Keyframe Interpolation, 5:34, 2025-05-29).

[100] Sandbox verification runs, 2026-10-18 — local, not a URL — ffmpeg 6.1.1, ImageMagick 6.9.12, Blender `bpy` 5.2.2 (Python 3.13), Inkscape 1.2.2, MLT melt 7.22.0, Synfig 1.5.1, librsvg 2.58.0, svgpathtools, Pillow; outputs inspected with `ffprobe` and by eye. Runnable copies of research recipes R1 to R5 and R7 to R9 are in skills/free-creative-toolchain/recipes/.

[102] PyPI, `bpy` — https://pypi.org/pypi/bpy/json (JSON of https://pypi.org/project/bpy/) — release list, wheel file names and sizes, `requires_python`, README text; 5.2.2 uploaded 2026-09-15.

[103] Blender 5.2 downloads — https://download.blender.org/release/Blender5.2/ — `blender-5.2.2-windows-x64.zip` (404,453,484 B, SHA-256 `3849d17a…b535`) and `blender-5.2.2-linux-x64.tar.xz` (383,295,504 B, SHA-256 `84098912…a168`), both matching `blender-5.2.2.sha256` on the same page.

[104] Kdenlive download page and installers — https://kdenlive.org/download/ ; https://download.kde.org/stable/kdenlive/26.08/windows/kdenlive-26.08.2.exe ; https://download.kde.org/stable/kdenlive/26.08/windows/kdenlive-26.08.2_standalone.exe — sizes and hashes in F1; contents listed with 7-Zip.

[105] MLT source, `mlt_factory.c` — https://raw.githubusercontent.com/mltframework/mlt/master/src/framework/mlt_factory.c — Windows module and data folder rule (`MLT_APPDIR`, `\lib\mlt`, `\share\mlt`).

[106] Shotcut 26.9.27 for Windows — https://github.com/mltframework/shotcut/releases/download/v26.9.27/shotcut-win64-26.9.27.zip (213,335,062 B), linked from https://www.shotcut.org/download/ (SourceForge links there answered 403).

[107] Microsoft Learn, "Advanced settings configuration in WSL" — https://learn.microsoft.com/en-us/windows/wsl/wsl-config — `ms.date` 2026-10-16: `memory` default 50 % of Windows RAM, `swap` 25 %, `processors`, `autoMemoryReclaim`, `.wslconfig` location.

[108] Microsoft Learn, "about_Parsing" (PowerShell 7.6) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing — `ms.date` 2026-06-29: argument mode metacharacters, native-command arguments, `--%`, 7.3 change.

[109] MSYS2, "Filesystem Paths" — https://www.msys2.org/docs/filesystem-paths/ — undated (read through WebFetch): automatic path conversion and `MSYS2_ARG_CONV_EXCL`.

[110] DaVinci Resolve 21 Reference Manual (PDF, 4,444 pages, created 2026-07-09) — https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf — pages 109 (External Scripting), 804 (Voice Convert 8 GB VRAM), 3910 (pointer to a Configuration Guide), 4363.

[111] DaVinci Resolve 21.1 Reference Manual (PDF, 4,351 pages, created 2026-09-04) — https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21.1_Reference_Manual.pdf (address as listed by Blackmagic, with `?_v=1788850812000`) — pages 106, 1227 to 1248 (subtitles), 4318 (AI assistants / MCP).

[112] "DaVinci Resolve 21.1 Studio and iPad Features" (PDF, 12 pages, September 2026) — https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_Studio_21_Features.pdf — Free/Studio feature table.

[113] Blackmagic support listings (JSON) — https://www.blackmagicdesign.com/api/support/us/downloads.json and https://www.blackmagicdesign.com/api/support/us/documents.json — Resolve 21.1.1 dated 02 Oct 2026; newest "Configuration Guide" is Resolve 15; manuals 21, 21.1, Studio features (28 Sep 2026).

[114] FilmCraft v0.9.0 — https://github.com/storytold/filmcraft (tag `v0.9.0`, commit `4a69a03`, 2026-10-17): `README.md`, `docs/file-format-parity.md`, `docs/agents.md`, `crates/media/src/sequence.rs`, `crates/captions/src/lib.rs`, `apps/filmcraft-cli/src/main.rs`; release file https://github.com/storytold/filmcraft/releases/download/v0.9.0/filmcraft-0.9.0-windows-x64-portable.zip (70,686,984 B, SHA-256 `d370cac8…a5e`, matches the release's `SHA256SUMS.txt`).

[115] PhotoCraft v0.9.0 — https://github.com/storytold/photocraft (tag `v0.9.0`; reading clone at `main` commit `2d0f3b6`): `README.md`, `docs/file-format-parity.md`, `docs/scorecard.md` (FILE-215-9), `docs/ora.md`; release files `photocraft-0.9.0-windows-x64-portable.zip` (83,169,235 B, SHA-256 `e87bbe26…c97`) and `photocraft-0.9.0-linux-x86_64.tar.gz` (81,541,649 B, SHA-256 `91300c14…b90d`), both matching `SHA256SUMS.txt`.

[116] Kdenlive manual, "Configure Kdenlive: Plugins" (Speech to Text) — https://docs.kdenlive.org/en/getting_started/configure_kdenlive/configuration_plugins.html — undated; read through WebFetch (a summary, so exact figures such as "about 2 GB" and "1.4 GB" are as that summary stated).

[117] Kdenlive 26.08.2 Windows payload, Whisper helpers — inside [104]: `bin/data/kdenlive/scripts/whisper/whispertosrt.py`, `whispertotext.py`, `whisperquery.py`, `requirements-whisper.txt`, `requirements-cuda118|124|126|128.txt`.

[118] OpenAI Whisper — https://raw.githubusercontent.com/openai/whisper/main/README.md (model, VRAM and speed table) ; https://raw.githubusercontent.com/openai/whisper/main/whisper/__init__.py (model download URLs, SHA-256 in the path) ; https://raw.githubusercontent.com/openai/whisper/main/tests/jfk.flac (test clip).

[119] Mixkit — https://mixkit.co/license/ (index); https://mixkit.co/license/modal/musicFree/ and https://mixkit.co/license/modal/sfxFree/ (licence pop-ups; paths found in the site's script `controllers-1a0cdfcb….js`); https://mixkit.co/terms/ ("Last revised: October 2, 2025").

[120] Pixabay — https://pixabay.com/service/terms/ ("Last updated: November 18, 2024"); https://pixabay.com/service/license-summary/ (undated); https://pixabay.com/service/faq/ (undated); all read through WebFetch, so quotations are as that tool returned them.

[121] Suno — https://suno.com/terms (date of last revision August 10, 2026; effective September 3, 2026; read in full) and https://help.suno.com/en/articles/2746945 (undated).

[122] YouTube, read 2026-10-18 — channel listings https://www.youtube.com/@nuxttux/videos, `@BlenderGuru`, `@DefaultCube`, `@BlenderStudio`, `@grabbitt`, `@PolyFjord`, `@Ducky3d`, `@CGMatter`, `@BlenderOfficial`, `@JoshGambrell`, `@GlebAlexandrov`, `@Imphenzia`, `@SouthernShotty`, `@BlenderDaily` (all `/videos`); oEmbed for https://www.youtube.com/watch?v=B8ZPoWaxQrA ; watch page https://www.youtube.com/watch?v=vNzt3fYTnDk (title, "Apr 17, 2025", views, description).

[123] Sandbox runs for this round, 2026-10-18 (local, not a URL): Ubuntu 24.04, 4 vCPU, 16 GB, no GPU; Wine 9.0; 7-Zip 23.01; `bpy` 5.2.2; Blender 5.2.2 Linux and Windows builds; Kdenlive `melt.exe` 7.43.0 and Shotcut `melt.exe` 7.41.0; `filmcraft-cli.exe` 0.9.0; `photocraft-cli` 0.9.0 (Linux); `torch` 2.14.1+cpu with `openai-whisper` 20250625. Outputs inspected with `ffprobe`, Pillow and by eye.

[124] `/home/user/animated_journey/CLAUDE.md` (local project file, added to the session on 2026-10-18; undated): "premiering Saturday, Feb 27, 2027 at a mostly public gathering", "theatrical bar", "everything shown in public must be cleared".

[140] Suno — https://suno.com/pricing (undated; plans, credits, downloads; read through WebFetch) and https://help.suno.com/en/articles/2746945 ("Do I have the copyrights to songs I made?", no date).

[141] Zapsplat and Musopen, tried again — https://www.zapsplat.com/license-type/standard-license/ and https://musopen.org/about/faq/ — HTTP 403 through WebFetch; UNVERIFIED.

## Changelog

- v0.1 · 2026-10-18 · First draft, written by the Haiku scribe from research/toolchain.md and CHARTER.md. Not yet reviewed by the advisor or by the maker. The plan is provisional until the Step 0 checklist comes back.
- v0.2 · 2026-10-18 · Round 1 advisor revisions applied by the Haiku scribe: Decision 0 (shell) with PowerShell forms of the four self-checks; Decision 5 rule "Scripts travel, photos don't"; album looks replace decade looks (Step 9, Exercise 7); ArtCraft and hand-off lines in Decisions 1 and 4; recipes moved to skills/free-creative-toolchain/recipes/; Library of Congress edition year corrected to "current, undated on the page".
- v0.3 · 2026-10-18 · Round 2 advisor revisions applied by the Haiku scribe: `recipes/r2_param.py` added as the timed-run script, and Exercise 5 now produces the two R2_RESULT timings; Resolve external scripting restated as Studio-only per the 21 and 21.1 manuals; Mixkit, Pixabay, Suno and public-premiere licence readings added to Decision 6, Pitfalls and Sources; Windows run lines and melt.exe lines added; Whisper memory guidance added to Step 11 and Exercise 9; pace set to three or four exercises a week; open TODO items rewritten as open items at v0.2.
- v0.5 · 2026-10-19 · Reconciled with DECISIONS.md after the her-world merge (2026-10-19): the P-LOCK name for the Sat 14 Nov lock (Codes); Exercise 8 and Decision 3 re-based on the floor-art line at the phone floor (D-29, W-72, S-46) with the retired tool sources withdrawn; repo stated as public, text and ID-keyed manifests only (D-14, D-26); Step 10 and Decision 6 follow the W-44 spine (objects, rooms, surf, the two-take hum; no AI bed, no licensed song, no sung recording before April; W-65, W-79); Step 11 and Decision 8 carry the W-18 Gujarati caption rules, the phone caption setting and the `ass` path before ffmpeg n9.0 (W-75); the phone files PH1 and PH2 added to Step 12 and Decision 7 (W-63); the venue test clip carries the tone ladder (W-17).
- v0.4 · 2026-10-18 · Reconciled with DECISIONS.md (2026-10-18): frame rate 24 fps (W-14) in Step 4, Step 6, Step 8 and Exercise 2, with the 24 fps values marked UNVERIFIED until r1, r2 and r5 and the colour-patch test are re-run (the recipe files still carry 25); `zoompan` as a proof tool only (W-41); loudness -1 dBTP with three venue masters and a two-pass linear `loudnorm` (W-19); venue file per W-17 with a Main 4.0 backup; 4K dropped (W-15); sound order and mix tool for only-me (D-05, W-20, W-35); cloud policy (D-15, W-23, W-24); second encrypted SSD, no cloud copy (W-25); real photos after the process lock (P-LOCK) Sat 14 Nov and collection from Sun 15 Nov (D-13); music spine, Udio closed, no offline-private option for a public screening (D-08, W-44); the earlier block-model route conditional on O-05 and original assets only (D-23, since retired under D-29); no private link before the consent ledger closes (W-48). Decisions carry their register status.
- v0.6 · 2026-10-20 · Stale-wording sweep (2026-10-20): the recipe lines in Steps 4, 6 and 8 use the register's own form, "tested at 25, UNVERIFIED at 24", and say which values the maker changes by hand after the re-run (`fps`, `d`, the ending of the MLT profile name), with the 24 values still UNVERIFIED until then (W-14, S-01); Step 10 names the earlier, looser true-peak ceiling instead of quoting it (W-19, S-28); Step 11 and Step 12 carry the register's phone figures, a 3.5 Mb/s cap on PH2 and at most 32 characters a phone caption line (W-63, W-18); the v0.4 entry names the process lock as P-LOCK and the retired block-model route without its retired spelling (S-38, S-46).

### Open items at v0.2

- **Step 0 on your PC.** Run `research/toolchain-fixtures/step0_pc_tests.ps1` (research Follow-up F9). It writes one report with your inventory, the Windows tool checks and both R2 timings. The plan stays provisional until it comes back.
- **The two R2 timings.** Exercise 5: `r2_param.py` at 640×360 and 1920×1080, with peak working set. Decisions 2 and 5 wait on them.
- **PowerShell and Git Bash on Windows.** Each command that ran under Wine or in PowerShell 7 on Linux (research Follow-up F10) still needs one run in Windows PowerShell 5.1 or 7, and in Git Bash if you have it. That includes the `melt.exe` call (Step 8) and `pip install bpy` on Python 3.13.
- **ImageMagick, Inkscape and GIMP on Windows.** These ran under Wine, not from PowerShell (research Follow-up F11). GIMP's Python batch failed under Wine while Script-Fu worked, so treat GIMP Python as untested on Windows.
- **Resolve 21 Free.** A real install: whether the External scripting dropdown is missing or greyed out, whether subtitle tracks and burn-in work, and the hardware floor in the installer's Read Me (Decision 1; research Follow-up F4 and F12).
- **Kdenlive Whisper, fully offline.** A pre-staged install with no internet, and the real model folder on Windows (Step 11).
- **Burn-in fonts on Windows.** Kdenlive's `ffmpeg.exe` has no `drawtext` filter and draws subtitles through libass, and under Wine libass found no fonts (research Follow-up F10, F15). Test the burn-in on the real PC.
- **Verified 2025+ videos.** None yet for Ken Burns in Kdenlive or SVG line-draw in Blender (research Follow-up F7, F16). Cite the written sources until one is verified.
- **Licences still unread.** Zapsplat and Musopen: the sites refused automated reads, so the maker can paste the licence text from a browser (research Follow-up F13). Also unread: Openverse, ccMixter, Free Music Archive per-track terms, BBC Sound Effects' full terms, the YouTube Audio Library outside YouTube [77], and Stable Audio and Lyria terms (Udio cannot supply a file, so it is closed; W-44). The US Copyright Office Part 2 conclusions are unread [89]. Suno's download allowance on your own account (Decision 6).
- **Album look on your prints.** `derive_album_look.py` was tested on three stock prints (Step 9, Exercise 7). Run it on three prints from one of your albums, and on Windows Python.
- **Venue facts.** The screen, cable, USB format (FAT32 or exFAT), MKV and soft subtitles, HEVC, 50 frames a second (a 25 fps access copy is made only if a 50 Hz-only venue judders, W-14), and the country of the premiere (O-02, pending). Run the venue test kit on the real screen (research Follow-up F15; Decisions 7 to 9).
- **Floor-art line-draw card.** Drawing time per card on the maker's PC, and the agent-written Route A version against the Inkscape recipe (Decision 3, Exercise 8).
- **Cloud rendering.** No cloud render path was tested (Decision 5).
- **Hardware floors.** Kdenlive and Inkscape minimums were not found [8][32]. Resolve Free's floor is in its installer Read Me (above).
- **Headless claims not run.** Krita headless Python; Glaxnimate's pip package on your OS; the Audacity 4 scripting pipe; OpenShot bindings and `.osp`; hand-writing a native `.kdenlive`; EEVEE with no graphics card; Synfig's ffmpeg target syntax [100].
- **ArtCraft.** Not covered by this track. See the craft-visual and craft-motion tracks [1].
- **Time estimates.** Per-exercise times were not measured. Exercise 8 (the floor-art card) may run longer than two hours; its drawing time was not measured [100].
- **Search budget.** The shared search budget ran out in both research rounds. Better tutorials and tools may exist [100].
