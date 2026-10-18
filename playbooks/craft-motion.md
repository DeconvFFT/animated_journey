# Craft Motion and Sound Apps as Refinement Layers

*Draft v1, 2026-10-18. Track `craft-motion`. Built from `research/craft-motion.md` (researcher Sonnet, 2026-10-18) and `CHARTER.md`. Not yet reviewed. Open items are marked TODO(research).*

## Why this matters for our life journey

The agent team makes most of the film. It cuts the chapters, lays out the photos, writes the slow pans and zooms, and mixes the sound from code. Because the work is code, any chapter can be rebuilt quickly.

ArtCraft's apps are where your hands come in. FilmCraft is where you pick up a finished chapter and change it: adjust a pan that feels wrong, move a dissolve by a few frames, add a title, duck the music under a voice, and export. EffectCraft is for a few titles and perhaps one line-drawing. SoundCraft is not part of the delivery path.

Be careful with all three. They are free, open source and early alpha. They are about two and a half weeks old, and a new release tag appears every one to three days [39]. So nothing critical may depend on one of them. Every step has a fallback built from files the agents write. Those files open in DaVinci Resolve (free) or Kdenlive.

Where things stand: the research reads the code, the vendors' claims and public issue reports. Nothing has been built or run yet. The container test (spike S1) is written but not run. Any number marked as a vendor claim or an estimate is not a measurement on your PC.

## Core principles

1. **The agents build, you refine.** The source of truth is text in the repo: the chapter spec, the OTIO file and the scripts. If you change a shot in FilmCraft, save, export the interchange files and write down what you changed. The agents read your changes back. They never rebuild a shot you have edited.
2. **Pin a version by testing it, not by its date.** A newer FilmCraft can open files saved by an older one, but not the reverse [3]. Choose a tag, run the five-minute test, write down the tag and its SHA-256, and do not upgrade in the middle of a chapter.
3. **Prepare media before an app touches it.** FilmCraft decodes each still whole into 8-bit colour and does not read EXIF rotation or ICC colour profiles [10]. So stills are rotated, converted to 8-bit sRGB and sized to the sequence before import. Phone and camcorder video is converted first.
4. **Learn on test cards.** Until the pipeline is locked, use generated test cards (grids with numbers), not family photos. Real material comes in only after the pipeline is locked (charter).
5. **Every step has a fallback without a Craft app.** A Ken Burns move can be baked into plain video. Cuts and markers travel in OTIO, which Resolve and Kdenlive can read. Basic dissolves survive into Resolve [56]. The Kdenlive documentation does not mention transitions [51].
6. **Know what each format drops, and read the import report every time.** Plain OTIO carries no Ken Burns moves, no opacity and no audio gain [6]. FilmCraft's own metadata inside an OTIO file keeps them, but only FilmCraft reads that part.
7. **Keep the work private.** FilmCraft and EffectCraft write auto-save copies, caches and recent-file lists, next to the project or under AppData [2][31][33][38]. Use the portable zips, keep one encrypted working folder that does not sync to the cloud, and never run the Launcher on a shared machine.
8. **Real memories stay real.** You can restyle, animate and connect real photos. You cannot invent events or people, or put words in anyone's mouth. Reconstructed scenes are visibly labelled. No synthetic voice is ever used for a relative (charter, principle 4).

## How to do it, step by step

Steps 1 to 6 are set-up, for weeks 1 and 2. Steps 7 to 12 are the chapter loop, repeated for each chapter.

**Step 1. Make the folders.** Suggested layout on the Windows PC, on one encrypted drive if you have one:
- `C:\LifeJourney\tools\` holds one folder per app and tag, such as `filmcraft-v0.8.0`.
- `C:\LifeJourney\work\stills\` and `C:\LifeJourney\work\audio\` hold the media the agents hand you. Keep these paths, because the OTIO files point to them.
- `C:\LifeJourney\projects\` holds your FilmCraft project files. (Our suggestion.)
- `C:\LifeJourney\exports\` holds renders. (Our suggestion.)

**Step 2. Download the pinned version.** Get the portable x64 zip for the tag you are testing from that tag's GitHub release page. Do not use the ArtCraft Launcher for production, because it installs and updates the apps on its own [63]. Do not use the MSI installer for production either. Its command-line tool is not on the PATH [14], and its data goes to AppData [2].

**Step 3. Check the download.** In PowerShell, run:

    Get-FileHash -Algorithm SHA256 "C:\Users\<you>\Downloads\<zip name>"

Compare the result with the pin table in the Templates section. If it does not match, do not run the file. Download it again. If it still differs, tell the agent team. Optionally, run `Get-AuthenticodeSignature` on the `.exe`. TODO(research): whether the downloaded portable binaries are code-signed as the release implies.

**Step 4. Unzip.** Unzip into `C:\LifeJourney\tools\filmcraft-v0.8.0\`. The zip holds `filmcraft.exe`, `filmcraft-cli.exe` and a file called `portable.txt` [15]. That file keeps the data folder beside the program, not in AppData [2].

**Step 5. Start it, and fall back if needed.** Double-click `filmcraft.exe`. If the window appears and closes at once, open PowerShell in that folder and try these in order. Write down the one that works.
1. `$env:WGPU_BACKEND="vulkan"` and then `.\filmcraft.exe`
2. `$env:WGPU_BACKEND="dx12"` and then `.\filmcraft.exe`
3. `.\filmcraft.exe --graphics software`

The last option draws on the processor instead of the graphics card, so it is slower [1][13].

**Step 6. Run the five-minute test.** Use the checklist in Template B. Note the RAM use shown in Task Manager.

**Step 7. Receive a chapter bundle.** The agents hand you one folder with:
- `media/` (conformed stills and WAV audio)
- `ch01.otio` (the cut, with FilmCraft's motion data inside)
- `ch01.xml` (an XML timeline in the older Final Cut Pro 7 style, for Resolve)
- `build_info.json` (tool tags, hashes, and the frame rate and size used)
- the spec file (the plain-text description of the chapter)

Copy it into `C:\LifeJourney\work\`. Keep the folder layout exactly as delivered. The files point to absolute `file:///C:/LifeJourney/...` locations [5]. If you must move the folder, ask the agents first.

**Step 8. Import and read the report.** In FilmCraft, choose File > Import and open `ch01.otio`. Read the import report before you touch anything [9]. Look for three things: no red "MEDIA NOT FOUND" slates, the Ken Burns keyframes present, and no unexpected "not supported" lines. Write any problem in your change list and tell the agents.

**Step 9. Refine what FilmCraft is good at.** Work in this order:
- **Ken Burns moves.** Drag the scale and position keyframes in Effect Controls. Use the value and velocity graphs to check the easing.
- **Dissolves.** Retime them, or re-centre them on the cut.
- **Titles.** Use the Type tool for simple titles and lower thirds.
- **Music under voice.** Use Essential Sound > Music > Ducking against Dialogue. It writes volume keyframes [17].
- **Save** into the project folder. At the end of each session, choose File > Save a Copy as a second copy [2].

**Step 10. Hand back the changes.** Export the interchange files (OTIO and FCP7 XML) and the marker list. Return them with a short change list: shot number, what you changed and why. The agents read the file, compare it with the spec, and update only the parts you did not touch. TODO(research): exact menu path for the marker-list export.

**Step 11. Make the final files.** Who runs this depends on Decision 1.
- **Archive master.** Export with the preset "Apple ProRes 422 HQ", at the sequence size and frame rate, with 48 kHz 24-bit audio [11]. Use "Apple ProRes 4444" only if the film has transparency or smooth gradients that band.
- **Venue copy.** Encode the master to H.264 with ffmpeg: `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart`, with AAC at 320 kbps. The research note gives this reason: FilmCraft's own H.264 encoder lacks several quality tools, such as trellis and psy-RD [18]. Also make a smaller 1080p safety copy (CRF 20, high profile, level 4.1) for the venue laptop.
- **Check.** Run ffprobe on each file: codec, pixel format, frame rate, and frame count against the expected duration. Measure the sound with `ebur128` [61].

**Step 12. Archive.** Keep two copies, one of them off the working drive. Each copy holds the master, the project file, the OTIO, the FCP7 XML, `build_info.json`, and a media list with a SHA-256 for every file.

## Learn-by-doing exercises

Times are our estimates, not measurements. Do Exercises 1 to 6 in order. Exercises 7 and 8 are optional.

### Exercise 1. Install, verify and start FilmCraft

- **Goal:** a verified, running portable copy of the candidate FilmCraft tag, with a log entry.
- **Steps:**
  1. Download the portable x64 zip of v0.8.0 from its release page.
  2. Run the hash check in Step 3 and compare it with the pin table.
  3. Unzip into `C:\LifeJourney\tools\filmcraft-v0.8.0\`.
  4. Start `filmcraft.exe`. If needed, try the graphics fallbacks in Step 5.
  5. Run `filmcraft-cli.exe --version`.
  6. Open an empty project and note the RAM use.
- **Time (estimate):** 45 minutes, plus download time.
- **What good looks like:** the hash matches. The app opens and stays open. The CLI prints a version. Your log says which graphics setting worked and gives the RAM use with an empty project.

### Exercise 2. Pan and zoom a test card

- **Goal:** learn the scale numbers that make a still fill the frame.
- **Steps:**
  1. Ask the agents for two test cards: a 3600x2400 gridded still, and its 2880x1620 conformed copy.
  2. Start a new sequence at 1920x1080 and 25 fps. The CLI's default frame rate is 23.976, so check it.
  3. Place the 3600x2400 still. Set Motion scale to 53.3 (the cover value). Play it.
  4. Set scale to 100 and play again. Note the crop.
  5. Back at 53.3, add an end keyframe at 112 percent of cover (about 59.7) with EaseOut. Play it.
  6. Repeat with the 2880x1620 copy, where the cover value is 66.67.
- **Time (estimate):** 1 hour.
- **What good looks like:** at 100 you see a crop of the picture at native size. At 53.3 the grid fills the frame. The move is smooth and ends with the grid still filling the frame.

### Exercise 3. Read what the import keeps

- **Goal:** know exactly what each import format keeps.
- **Steps:**
  1. Ask the agents for a test chapter that includes one dissolve, one Ken Burns move, one opacity change and one audio level change.
  2. Import the plain OTIO version (without FilmCraft metadata). Read the report.
  3. Import the metadata version (`ch01.otio`). Read the report.
  4. For each version, record whether the dissolve, Ken Burns, opacity and audio level survived. Put the results in the first results column of Template F.
- **Time (estimate):** 45 minutes.
- **What good looks like:** for each feature you can say whether it survived, and you can point to the report line that says so.

### Exercise 4. Save, close, reopen, and find the safety copies

- **Goal:** trust the save, and know where the copies are.
- **Steps:**
  1. In a copy of a test project, change one keyframe.
  2. Press Ctrl+S, close the project, and reopen it.
  3. Confirm the change is still there.
  4. Find the `Auto-Save` folder next to the project and look at the timestamped copies in it.
  5. Write down every folder the app uses, in your log.
- **Time (estimate):** 30 minutes.
- **What good looks like:** the change persisted. The Auto-Save folder holds timestamped copies. You can name every folder the app writes to. Never test crashes on a working project.

### Exercise 5. Export two 20-second tests

- **Goal:** learn your export speed, and check the files.
- **Steps:**
  1. Export 20 seconds with "High Quality 1080p HD" (H.264).
  2. Export 20 seconds with "Apple ProRes 422 HQ" (archive).
  3. Note the wall-clock time and the RAM use for each.
  4. Run the export checklist (Template G) on both files.
  5. Play both files from start to finish.
- **Time (estimate):** about 1 hour, plus the export time itself. TODO(research): export speed on the maker's hardware, which is unknown. For scale only: the vendor's benchmark on a 14-core Xeon with an NVIDIA card gave 15 fps for software H.264 [12]. Our estimate for a 4-core PC is 4 to 16 fps at 1080p [E].
- **What good looks like:** both files play. Durations match within a frame. The export shows no missing-media warning. You have one real speed number for your PC.

### Exercise 6. The fallback round trip (once)

- **Goal:** fill in the "what survives" table for DaVinci Resolve (free).
- **Steps:**
  1. In DaVinci Resolve (free), import `ch01.otio`, then `ch01.xml`, using File > Import > Timeline. Do each one once.
  2. Fill in Template F, one row per feature.
  3. Note any warnings Resolve shows, and copy them in.
  4. Open the OTIO in Kdenlive too. Note whether the still-image clips arrive.
  5. Send the table to the agents. They use your result for Decision 2.
- **Time (estimate):** 1.5 to 2 hours.
- **What good looks like:** a complete table, with yes, partial or no in each cell, and any warnings copied in. The research could not read Resolve's manual pages, so this test is the only real check we have [55][56]. If Ken Burns does not survive into Resolve, the baked-motion fallback becomes the plan for every chapter.

### Exercise 7 (optional). Duck music under a voice in Essential Sound

- **Goal:** learn how FilmCraft ducks music under speech.
- **Steps:**
  1. Ask the agents for a 30-second synthetic "voice" test track (tones with pauses), and a 30-second music bed. Use synthetic test material only.
  2. Import both onto separate tracks.
  3. Apply Essential Sound > Music > Ducking against Dialogue.
  4. Play it. Note the dip and the recovery.
- **Time (estimate):** 1 hour.
- **What good looks like:** the music dips while the voice speaks and comes back in the gaps, with no clicks. The ducking shows up as volume keyframes [17].

### Exercise 8 (optional). One EffectCraft title with alpha

- **Goal:** learn the title path, and the font trap.
- **Steps:**
  1. Ask the agents for a title spec (text, font, size, timing) and an EffectCraft project.
  2. Open the `.ecproj`. Check the font in the text layer's properties is the one you intended. If it shows Inter, the font is missing and was replaced [47][23]. Install the font first.
  3. Render 5 seconds as an RGBA PNG sequence, into a new folder name. Never reuse an old output name [47].
  4. Check that the PNGs have alpha.
  5. Import the sequence into FilmCraft as an image sequence. TODO(research): exact menu path for the image-sequence import in the FilmCraft GUI.
- **Time (estimate):** 2 hours.
- **What good looks like:** the right font, a transparent background, and the sequence plays over a colour in FilmCraft.

## Templates and checklists

### A. Version pin record

Hashes are copied from each release's `SHA256SUMS.txt`, read on 2026-10-18 [40]. Check them against the release page again before you rely on them.

| App | Tag | Use | Windows x64 portable zip SHA-256 | Tested on | Result | RAM observed |
|---|---|---|---|---|---|---|
| FilmCraft | v0.8.0 | candidate for production | `0119afd59dfd6ecb94470ba6b3a48108ade87dabd4972898dd6c04e1db396b0b` | | | |
| FilmCraft | v0.7.2 | fallback | `8e22fabdf2f802573d3af4ad9993c05212dead5e933efda0fa290e825313cde7` | | | |
| EffectCraft | v0.11.1 | titles and line-drawing only | `78bd7f63c6bd814bc33f07bd523b003a5f8d095244c5f67bd70e902448fd6e34` | | | |

SoundCraft is not pinned for delivery. Do not use it for finished audio.

### B. Five-minute acceptance test (FilmCraft, Windows)

- [ ] The zip hash matches the pin table.
- [ ] `filmcraft.exe` starts. The working graphics setting is written down.
- [ ] `filmcraft-cli.exe --version` prints the expected tag.
- [ ] The test-card OTIO imports with no MEDIA NOT FOUND slate, and the motion keyframes are present (metadata version).
- [ ] Play 10 seconds. The Ken Burns move and the dissolve both work.
- [ ] Change a scale keyframe, press Ctrl+S, close, reopen. The change persists, and an `Auto-Save` folder exists next to the project.
- [ ] Export 20 seconds with "High Quality 1080p HD". Note the wall time. The MP4 plays.
- [ ] RAM stays under about 4 GB during these steps. (This is the research's pass threshold, not a published minimum. No minimum is published [58].)

### C. Still conform checklist

- [ ] Orientation applied (EXIF rotation baked in).
- [ ] 8-bit sRGB. Any non-sRGB ICC profile converted first.
- [ ] Sized to the sequence. A crop or pad decision is recorded per shot, so no face is cropped silently.
- [ ] Metadata stripped on the working copy. The untouched master is kept.
- [ ] A manifest row: file, source, size, crop decision, SHA-256.
- [ ] Motion scale computed: cover = max(W/w, H/h) x 100.

### D. Video conversion checklist (phone, camcorder, VHS capture)

- [ ] Deinterlaced if interlaced. VHS and MiniDV captures usually are.
- [ ] Constant frame rate.
- [ ] Converted to a ProRes 422 HQ intermediate at the sequence size, with 48 kHz audio.
- [ ] Checked with ffprobe. Manifest row written.
- [ ] HEVC HLG phone files are converted first. They failed to import on Windows 10 [46].
- [ ] DV and camera RAW are not used. FilmCraft does not support them [13].

### E. After each import

- [ ] The import report is read. Nothing unexpected.
- [ ] No offline media.
- [ ] Timeline duration equals the spec's duration.
- [ ] Keyframes are present wherever the spec has them.

### F. What survives: format by feature

The "Expected" columns come from the code and its tests. They are not verified in Resolve or Kdenlive. Fill in the result columns during Exercise 3 and Exercise 6.

| Feature | Plain OTIO (expected) | OTIO with FilmCraft metadata (expected) | FCP7 XML (expected) | Resolve free (your result) | Kdenlive (your result) |
|---|---|---|---|---|---|
| Still clips with duration | kept | kept | kept | | |
| Ken Burns (scale and position keyframes) | lost | kept, with easing | kept (easing handles not preserved) | | |
| Dissolves | kept | kept | kept | | |
| Opacity | lost | kept | kept | | |
| Audio clip level | lost | kept | kept | | |
| Markers | kept | kept | kept | | |
| Titles and graphic clips | lost | lost | lost | | |
| Image sequences | degraded | degraded | degraded | | |

Sources: [6] for OTIO, [8] for FCP7 XML, [51] and [52] for Kdenlive, [55] and [56] for Resolve. Resolve's FCP7 and FCPXML results are the open question, and only your test can answer them [57] (search summary only). TODO(research): whether Resolve keeps Ken Burns keyframes from FCP7 XML.

### G. Export checklist

- [ ] The file plays from start to finish.
- [ ] ffprobe: codec, pixel format, frame rate and frame count match the expected duration.
- [ ] Audio duration equals video duration within a frame.
- [ ] Loudness measured against the target chosen in Decision 5.
- [ ] No missing-media warning in the export.
- [ ] Saved under a new name. The last good file is kept.

### H. Private working folder check

- [ ] The working folder is not inside OneDrive, Dropbox, Google Drive, or a synced Desktop, Documents or Pictures folder. TODO(research): whether any sync is on the maker's PC.
- [ ] Portable app folders, with data kept beside the program.
- [ ] The recent-file list is cleared before anyone else uses the PC.
- [ ] No family names or file names in any bug report or forum post.
- [ ] No cloud photo library connected to the working folder.

## Decisions you'll need to make

Each decision lists the options and our current lean. The lean can change after the tests.

### Decision 1. Where heavy rendering runs

- **Options:** (a) the Linux container, using the Craft command-line tools, if spike S1 passes; (b) the container, using ffmpeg and code only; (c) your Windows PC.
- **Our lean:** (b) is the safe default. Use (a) only if S1 passes. Use (c) for interactive work and short exports. Revisit after S1, in weeks 1 and 2.
- **What we know:** the container has 4 CPUs, 16 GB of RAM and no GPU [62]. No minimum RAM, disk or GPU is published for any of the three apps [58]. A 6-minute film at 25 fps is 9,000 frames. At our 4-to-16 fps estimate, that is about 9 to 37 minutes at 1080p [E]. The vendor's own figures are on other hardware [12].

### Decision 2. Ken Burns: editable, or baked into video?

- **Options:** (a) keep the moves as editable keyframes in FilmCraft; (b) bake each move into video with `zoompan`, so every editor shows the same move; (c) a mix.
- **Our lean:** (a) for the first chapter, because you can then adjust the moves by hand. Use (b) for any shot that must look the same in Resolve or Kdenlive [6][7].

### Decision 3. Which second editor to test

- **Options:** DaVinci Resolve (free), which reads OTIO, FCPXML, FCP7 XML and EDL [55][56]; or Kdenlive, which reads OTIO and, per its file menu, carries tracks, clips and markers, not effects or transitions [51].
- **Our lean:** Resolve (free) for the one-time test in Exercise 6, and Kdenlive as a cut-only backup. The free edition's import limits are not stated anywhere the research could read. TODO(research). The current Kdenlive release is 26.08.2 [49]. OTIO support in Kdenlive dates from version 25.04 per search summaries [64].

### Decision 4. Frame size and rate for the whole film

- **Options:** 1920x1080 at 25 fps; 1920x1080 at 24 or 30 fps; 3840x2160.
- **Our lean:** 1920x1080 at 25 fps. The tests and the time estimates use this setting. A 4K film is estimated at about four times the render time [E].

### Decision 5. Loudness target

- **Options:** -23 LUFS (the broadcast standard); about -16 to -18 LUFS (home and online stereo). True peak at or below -1.5 dBTP for both. FilmCraft's export default is -23 LUFS with a -2 dBTP limit, and it is off by default [11].
- **Our lean:** -18 LUFS integrated and -1.5 dBTP, as a provisional target. Decide when the venue is known.

### Decision 6. Which FilmCraft tag to pin

- **Options:** v0.8.0 (the latest tag at the time of the research); v0.7.2 (the fallback).
- **Our lean:** v0.8.0 if the five-minute test passes. Otherwise v0.7.2. Test again before any upgrade.

### Decision 7. How much EffectCraft to use

- **Options:** none; titles only; titles and one line-drawn sequence; 3D parallax as well.
- **Our lean:** FilmCraft's own graphic clips for static titles and lower thirds. EffectCraft only for one SVG line-drawn sequence, and for text with expressions if it is needed. Skip classic 3D parallax for now, because there are no CPU timings for it and there is a known memory issue [47][22].

### Decision 8. Who cleans up voice recordings

- **Options:** FilmCraft's Essential Sound (repair and ducking); Audacity with its noise reduction; ffmpeg filters; SoundCraft.
- **Our lean:** Essential Sound for repair and ducking, with Audacity as the backup. Never SoundCraft for delivery. Its MP3 and AAC import can silently shorten or shift audio [48], and it has no sidechain input [34].

### Decision 9. The venue playback file

- **Options:** H.264 MP4 encoded with ffmpeg; ProRes MOV; FilmCraft's built-in H.264 preset.
- **Our lean:** H.264 MP4 from ffmpeg for the venue, with the 1080p safety copy. Keep ProRes for the archive. The research note assumes a projector PC plays H.264 MP4 reliably. Test that on the venue machine. TODO(research): colour management end to end (sRGB stills, Rec.709 sequence, ProRes tags, venue projector) needs a test-card pass.

### Decision 10. When real material enters the tools

- **Options:** only after the pipeline is locked and every test in this playbook passes (charter); or earlier, for learning.
- **Our lean:** test cards only until the five-minute test and Exercises 1 to 6 pass, plus the Resolve check. Then the first real chapter, as a trial, in the encrypted working folder.

## Pitfalls

1. **Stills import at their native size.** Scale 100 means native pixels. A 3600x2400 still in a 1080p sequence shows a crop at 100. Use the cover scale, or conform the still first [5][6][11].
2. **Stills use a lot of memory.** FilmCraft decodes each still whole, about 34.6 MB for a 3600x2400 still. The decoded copy stays in a media pool that the research found has no memory-pressure eviction. Importing 300 such stills could hold about 10 GB [10][9][E]. Conform the stills first, and cut the film into chapters of one to two minutes.
3. **Render previews fill the disk.** One report of a 1080x1920 timeline gave 0.7 to 1.1 GB of preview per 30 to 47 seconds. Budget several GB. Do not play the Program monitor during an export; one reported export ran out of RAM and disk this way [45].
4. **Plain OTIO drops features without a loud error.** Ken Burns, opacity and audio gain disappear. Read the import report every time [6].
5. **Malformed metadata is dropped silently.** If the agent's motion data has the wrong shape, FilmCraft imports a plain cut with no motion. Check after each import that the keyframes exist [6].
6. **Kdenlive aborts on missing media.** It also flipped the video tracks when its OTIO went to Resolve, in one reported bug [54]. Keep the folder layout fixed.
7. **Scale means different things in other editors.** FilmCraft's Scale 100 is native pixels. Resolve and Final Cut use 1.0 for fitted. Stills conformed to exactly the sequence size agree at 100 [11][7].
8. **FCPXML `<video>` items are skipped by FilmCraft.** Final Cut often writes stills as `<video>`, and FilmCraft's tests use only its own output and hand-written examples [7]. Whether Resolve accepts stills written as FCPXML asset-clips is TODO(research).
9. **The project format changes often.** FilmCraft's project schema moved from 13 to 15 in five days, and older builds refuse newer files [2][3]. Do not hand-write project files. Let the tool write them.
10. **EffectCraft's CPU renders have no memory cap.** In one reported case, an out-of-memory crash left an MP4 without its index, so it would not play [47]. Limit threads with `RAYON_NUM_THREADS=2`, render one job at a time, and check each output with ffprobe [30]. One search summary, not opened by the research, reports heavy memory use on Windows 11 with an Intel Arc card [60].
11. **EffectCraft can overwrite the previous output.** A cancelled or failed overwrite destroyed the previous file, in one open issue [47]. Always use a new file name.
12. **Fonts fall back silently.** If a font is not installed, EffectCraft uses Inter instead [47][23].
13. **EffectCraft's ProRes 4444 output is tagged as BT.709 but encoded as sRGB** (open issue #340) [22]. Use RGBA PNG sequences for alpha instead.
14. **Windows graphics crashes at start-up.** Reported crash files include AMD `atio6axx.dll` and `amdvlk64.dll`, and Intel `igvk64.dll` [1][13][45][46]. Use the backend settings in Step 5. Do not reinstall the app.
15. **Phone HEVC HLG video failed to import on Windows 10** (issue #1998) [46]. Convert it first.
16. **SoundCraft's MP3 and AAC import can silently shorten or shift audio** (issues #710 and #707) [48]. Use WAV or FLAC only.
17. **`wiggle` will not look like After Effects.** EffectCraft's noise is deterministic but not After Effects' sequence [25]. Do not promise a match with an After Effects tutorial.
18. **A Lottie export that "works" is not a Lottie that plays right.** Blur, glow, video, 3D and layer styles are dropped [26]. Lottie is only for small web pieces.
19. **Bug reports become public.** The research note reports that bug reports sent through the Discord ticket bot are relayed to public GitHub issues. Never include family names, file names, screenshots or clips. Reproduce problems with test cards.
20. **Files you did not expect are kept on the PC.** Auto-saves, recovery copies, previews and recent lists are written to the project folder or AppData [2][31][33][38]. Check them before the PC is shared. No telemetry was found in the default builds. The optional model downloads are off by default [19].
21. **Versions and numbers disagree across sources.** The website shows FilmCraft 0.6.0 while GitHub has v0.8.0. Feature counts also differ between the website and the README [41][1]. Quote tags and tests, not marketing numbers.
22. **Numbers from issue pages are summaries.** The research read them through a summarising tool. Re-read the linked issue before you quote a number [45][46][47][48].

## Best references

1. **FilmCraft repository** (github.com/storytold/filmcraft). Start with the README for formats, export and vendor status [1], then `docs/agents.md` for the command-line tool [14] and `docs/project-files.md` for saves, auto-save and recovery [2]. Worth your time because every step in this playbook runs through these three files.
2. **FilmCraft release notes** (github.com/storytold/filmcraft/releases). Shows what changed in each tag, including save-safety and Windows fixes [42]. Read it before any upgrade.
3. **EffectCraft repository** (github.com/storytold/effectcraft). The README gives the project's own status statement and the list of features [20]. `docs/agents.md` is the command-line cookbook for titles and renders [21].
4. **EffectCraft issue 1615** (github.com/storytold/effectcraft/issues/1615). The clearest published numbers for CPU render memory and the out-of-memory risk [47]. Re-read it before quoting.
5. **SoundCraft gaps list** (github.com/storytold/soundcraft, `docs/gaps.md`). Read it to see why SoundCraft is not in the delivery path [34].
6. **Kdenlive file menu documentation** (docs.kdenlive.org/user_interface/menu/file_menu.html). What Kdenlive does with OTIO files [51]. Pair it with the KDE forum post on OTIO metadata being dropped (discuss.kde.org/t/opentimelineio-metadata-and-effects/45813) [52].
7. **DaVinci Resolve product page** (blackmagicdesign.com/products/davinciresolve). The free edition's limits, such as 8-bit video up to UHD at 60 fps [55]. Resolve's own manual was not reachable for the research, so use this page as the starting point and test the rest yourself.
8. **ArtCraft app page for FilmCraft** (getartcraft.com/apps/filmcraft). The vendor's own description [41]. Read the claims, not the version number, which lags GitHub.

## Sources

Copied from the Sources list of `research/craft-motion.md`. The research read these; the scribe did not re-open them. Items marked "search result only" were not opened.

- [1] github.com/storytold/filmcraft, `README.md` at tag v0.8.0 (repository: https://github.com/storytold/filmcraft). Status, formats, export, Windows `WGPU_BACKEND` note. Vendor claims.
- [2] github.com/storytold/filmcraft, `docs/project-files.md` at v0.8.0. Project format, atomic saves, auto-save, recovery journal, portable data folder. The schema history in this file is out of date.
- [3] github.com/storytold/filmcraft, `crates/format/src/lib.rs` and `tests/fixtures/*.fcproj` at v0.8.0. Schema version 15, migrations.
- [5] github.com/storytold/filmcraft, `crates/interchange/` (`README.md`, `src/lib.rs`, `src/common.rs`) at v0.8.0. Import path resolution, import reports.
- [6] github.com/storytold/filmcraft, `crates/interchange/src/otio.rs` and `tests/otio.rs` at v0.8.0. OTIO mapping and `metadata.filmcraft`.
- [7] github.com/storytold/filmcraft, `crates/interchange/src/fcpxml.rs` and `tests/fcpxml.rs` at v0.8.0. FCPXML support and skipped elements.
- [8] github.com/storytold/filmcraft, `crates/interchange/src/{edl.rs, fcp7.rs}` and tests at v0.8.0. EDL and FCP7 XML support.
- [9] github.com/storytold/filmcraft, `crates/engine/src/{interchange.rs, commands.rs, media_pool.rs}` at v0.8.0. Import and media linking, media pool.
- [10] github.com/storytold/filmcraft, `crates/media/src/{still.rs, lib.rs}` at v0.8.0. Still decoding to 8-bit RGBA; no EXIF or ICC handling.
- [11] github.com/storytold/filmcraft, `crates/render/src/lib.rs` and `crates/export/src/{presets.rs, settings.rs}` at v0.8.0. Motion semantics, export presets, loudness defaults.
- [12] github.com/storytold/filmcraft, `docs/performance.md` at v0.8.0. Vendor benchmarks on other hardware.
- [13] github.com/storytold/filmcraft, `docs/gaps.md`, `docs/target-app-parity.md`, `ROADMAP.md` at v0.8.0. Known gaps, Windows problems, unsupported formats.
- [14] github.com/storytold/filmcraft, `docs/agents.md` and `apps/filmcraft-cli/src/main.rs` at v0.8.0. Command-line tool, MCP, control channel, install locations.
- [15] github.com/storytold/filmcraft, `packaging/` at v0.8.0. Contents of the MSI and portable zip, and dependencies.
- [17] github.com/storytold/filmcraft, `docs/architecture.md` section 5.2, `crates/project/src/essential.rs`, `crates/audio-dsp/tests/loudness_oracle.rs` at v0.8.0. Essential Sound ducking, repair and loudness.
- [18] github.com/storytold/filmcraft, `crates/h264enc/README.md` and `crates/prores/README.md` at v0.8.0. Encoder features and limits.
- [19] github.com/storytold/filmcraft, network-audit greps of `Cargo.lock`, `crates/speech`, and the automation and control code at v0.8.0. Optional downloads and the network surface.
- [20] github.com/storytold/effectcraft, `README.md` at v0.11.1 (repository: https://github.com/storytold/effectcraft). Features, status statement, no telemetry.
- [21] github.com/storytold/effectcraft, `docs/agents.md` at v0.11.1. Command-line and MCP tools, cookbook, pitfalls.
- [22] github.com/storytold/effectcraft, `docs/gaps.md` and `docs/target-app-parity.md` at v0.11.1. Fidelity, open issues, the ProRes 4444 colour-tag issue.
- [23] github.com/storytold/effectcraft, `docs/file-format-parity.md` and `docs/footage.md` at v0.11.1. Import and export formats, fonts, relinking.
- [25] github.com/storytold/effectcraft, `crates/expr/` and related files at v0.11.1. Expression engine, object model, tests, noise.
- [26] github.com/storytold/effectcraft, `crates/lottie/` and its fixtures at v0.11.1. Lottie import and export, and the list of things Lottie cannot express.
- [30] github.com/storytold/effectcraft, `apps/effectcraft-cli/src/main.rs`, `crates/export/src/lib.rs` and `pipeline.rs` at v0.11.1. Render flags, CPU batch size.
- [31] github.com/storytold/effectcraft, `packaging/` and `apps/effectcraft/src/launch_guard.rs` at v0.11.1. CLI in the MSI and zip, `portable.txt`, launch guard.
- [33] github.com/storytold/soundcraft, `README.md` at v0.8.0 (repository: https://github.com/storytold/soundcraft). Pre-alpha status, logs, Windows notes.
- [34] github.com/storytold/soundcraft, `docs/` (`file-format-parity.md`, `gaps.md`, `plugin-parity.md`, `mcp.md`) at v0.8.0. Formats, gaps, sidechain absence, plugins on Windows.
- [38] github.com/storytold/soundcraft, `crates/engine/src/{autosave.rs, io.rs}`, `crates/playback/src/devices.rs`, and `packaging/` at v0.8.0. Auto-save location, packaging.
- [40] https://github.com/storytold/filmcraft/releases/download/v0.8.0/SHA256SUMS.txt, also the v0.7.2 file, and https://github.com/storytold/effectcraft/releases/download/v0.11.1/SHA256SUMS.txt. Downloaded with curl on 2026-10-18. Asset lists and hashes.
- [41] https://getartcraft.com/apps/filmcraft, https://getartcraft.com/apps/effectcraft, https://getartcraft.com/apps/soundcraft. Fetched 2026-10-18. Vendor descriptions; website versions lag GitHub.
- [42] https://github.com/storytold/filmcraft/releases. Release notes v0.4.0 to v0.8.0, read through a summarising tool on 2026-10-18.
- [45] https://github.com/storytold/filmcraft/issues/2216, `/1939`, `/1443`, and a search of open data-loss and still-image issues. Read through a summarising tool; numbers are summaries.
- [46] https://github.com/storytold/filmcraft/issues/1998, `/1959`, `/2099`, `/1390`, and a Windows crash and launch search. Read through a summarising tool.
- [47] https://github.com/storytold/effectcraft/issues/1615, and searches of open Windows and data-loss issues. Read through a summarising tool.
- [48] https://github.com/storytold/soundcraft/issues/711 and `/710`, and a Windows issue search. Read through a summarising tool.
- [49] https://kdenlive.org/news/. Kdenlive 26.08.2, released 2026-10-13.
- [51] https://docs.kdenlive.org/user_interface/menu/file_menu.html. OTIO import and export scope and limits in Kdenlive.
- [52] https://discuss.kde.org/t/opentimelineio-metadata-and-effects/45813. A 2026-03-30 forum post: metadata and effects dropped on import.
- [54] https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1051588.html. KDE bug 503692: missing-media abort, track order flip.
- [55] https://www.blackmagicdesign.com/products/davinciresolve. DaVinci Resolve 21 product page; free edition limits. Fetched 2026-10-18.
- [56] https://violetflare.ai/blog/davinci-resolve-otio-import/. Secondary source: OTIO support in Resolve since 18.5, basic dissolves only.
- [57] https://tryuncle.com/learn/davinci-resolve/switching-from-final-cut-pro-to-davinci-resolve. Search result only, not opened. A guide that recommends FCPXML 1.9 for Resolve 21.0.2.
- [58] https://www.windowsmode.com/?p=47621. A 2026-10-12 article: portable zips; no minimum specifications published for the Craft apps. Not hands-on.
- [60] Search result only, not opened: a summary of an EffectCraft memory-use report on Windows 11 with an Intel Arc card (https://pasqualepillitteri.it/en/news/23653/effectcraft-free-after-effects-alternative-rust).
- [61] First-hand: ffmpeg 6.1.1 on synthetic signals, run by the researcher in the container on 2026-10-18. Ducking, loudness, ebur128 and ProRes commands. Not a public source.
- [62] First-hand: the researcher's container baseline on 2026-10-18 (Ubuntu 24.04.5, 4 CPUs, 16 GB RAM, no GPU, ffmpeg 6.1.1).
- [63] `reviews/01-addendum-briefs-review.md` (Part 0 and Part 2.2) and `CHARTER.md`, as cited in the research note. The review file was not re-opened for this playbook.
- [64] Search result only, not opened: Kdenlive 25.04.0 release notes (https://ubuntuhandbook.org/index.php/2025/04/kdenlive-25-04-0-released/). OTIO import and export rewritten in 25.04.0.
- [39] `git ls-remote --tags` and `git fetch` for each tag of the three repositories, run by the researcher on 2026-10-18. Release cadence.

## Changelog

- **2026-10-18, v1 draft.** First version, written by a Haiku scribe from `research/craft-motion.md` and `CHARTER.md`. Not yet reviewed. Open items are marked TODO(research): maker's hardware and export speed; minimum system requirements (none published); whether DaVinci Resolve (free) limits imports; whether Resolve keeps Ken Burns keyframes from FCP7 XML or FCPXML; whether Resolve accepts stills as FCPXML asset-clips; how Kdenlive treats still-image OTIO clips; proxies and memory release for stills in FilmCraft (spike S1); EffectCraft CPU timings for 3D, text animators and Trim Paths; Lottie in a real player; code signing of the downloads; colour management end to end; sync status of the maker's PC; the marker-list and image-sequence menu paths; release cadence over eight weeks (repos were 17 days old at the time of the research).
