# Craft Motion and Sound Apps as Refinement Layers

*Draft v1.4, 2026-10-19. Track `craft-motion`. Built from `research/craft-motion.md` (researcher Sonnet, 2026-10-18) and `CHARTER.md`, reconciled with [DECISIONS.md](../DECISIONS.md) (2026-10-18, and again 2026-10-19 after the her-world merge). Not yet reviewed. Open items are marked TODO(research).*

**Reconciled with DECISIONS.md (2026-10-18). The register wins (D-21).** What changed here:

- **Frame rate is 24 fps** (W-14), signed on the settings card Sun 1 Nov (W-16). Every guard value that said 25 now says 24: Timebase 24, `media.indeterminateTimebase` the string `"24"`, `zoompan d=120` for a 5 s proof. The research tested these at 25, so they are **UNVERIFIED at 24** until r1, r5 and the colour-patch test are re-run at 24 (container ffmpeg 6.1.1 and the PC's winget build) and the values are confirmed by hand. The recipe files under `skills/free-creative-toolchain/recipes/` still carry 25 until then.
- **Loudness is -1 dBTP everywhere** with three venue masters chosen at the Mon 22 Feb run (W-19). **The venue file is CRF 18 with a 20 Mbps cap, AAC-LC 256 kbps** (W-17).
- **Real material enters the tools after the P-LOCK process lock, Sat 14 Nov 2026; covert collection starts Sun 15 Nov** (D-13, W-10).
- **Only-me** (D-03): there is no co-keeper, no proxy reviewer and no second reader. The maker is the proxy, and hard chapters follow one-key-three-guards (D-04). The premiere cut has no recorded voice of a living person (D-05), no synthetic voice (W-46), and the April version carries the relatives' voices (D-06).
- **Added 2026-10-19 (her-world merge).** Cards in the pichwai manner and floor-art cards keep the motion limits of W-72, which are tighter than the default weights in Step 9. Her script on a title or card arrives as shaped outlines, never live text typed into a Craft app (W-21, W-75). Must-read type clears the phone floor (W-63). No deity and no seva article is in any file a Craft app opens (W-61, W-70). The spike name is SP1 (Codes). The id-to-original map stays offline, because the repo is public (D-14, D-26).
- Each Decision below carries its register status: decided (`DECISIONS.md` Table 1), default with a decide-by date (Table 2), or open for the maker (Table 3).

## Why this matters for our life journey

The agent team makes most of the film. It cuts the chapters, lays out the photos, writes the slow pans and zooms, and mixes the sound from code. Because the work is code, any chapter can be rebuilt quickly.

ArtCraft's apps are where your hands come in. FilmCraft is where you pick up a finished chapter and change it: adjust a pan that feels wrong, move a dissolve by a few frames, add a title, duck the music under a voice, and export. EffectCraft is for a few titles and perhaps one line-drawing. SoundCraft is not part of the delivery path.

Be careful with all three. They are free, open source and early alpha. They are about two and a half weeks old, and a new release tag appears every one to three days [39]. So nothing critical may depend on one of them. Every step has a fallback built from files the agents write. Those files open in DaVinci Resolve (free) or Kdenlive.

Where things stand: the research reads the code, the vendors' claims and public issue reports. Nothing has been built or run yet. The container test (spike SP1) is written but not run. Any number marked as a vendor claim or an estimate is not a measurement on your PC.

## Core principles

1. **The agents build, you refine.** The source of truth is text in the repo: the chapter spec, the OTIO file and the scripts. If you change a shot in FilmCraft, save, export the interchange files and write down what you changed. The agents read your changes back. They never rebuild a shot you have edited.
2. **Pin a version by testing it, not by its date.** A newer FilmCraft can open files saved by an older one, but not the reverse [3]. Choose a tag, run the five-minute test, write down the tag and its SHA-256, and do not upgrade in the middle of a chapter.
3. **Prepare media before an app touches it.** FilmCraft decodes each still whole into 8-bit colour and does not read EXIF rotation or ICC colour profiles [10]. So stills are rotated, converted to 8-bit sRGB and sized to the sequence before import. Phone and camcorder video is converted first.
4. **Learn on test cards.** Until the P-LOCK process lock (Sat 14 Nov 2026), use generated test cards (grids with numbers), not family photos. Real material comes in only after the pipeline is locked: covert collection starts Sun 15 Nov (charter; D-13, W-10).
5. **Every step has a fallback without a Craft app.** A Ken Burns move can be baked into plain video. Cuts and markers travel in OTIO, which Resolve and Kdenlive can read. Basic dissolves survive into Resolve [56]. In Kdenlive, cuts, gaps, markers and dissolves (as luma mixes, by code) survive; effects, metadata and image sequences do not; `file://` URLs are not decoded; the project profile is taken from the first still's pixel size [72]. Resolve's manual says FCP 7 XML Opacity, Position, Scale and Rotation keyframes import, with FilmCraft's numbers untested [74].
6. **Know what each format drops, and read the import report every time.** Plain OTIO carries no Ken Burns moves, no opacity and no audio gain [6]. FilmCraft's own metadata inside an OTIO file keeps them, but only FilmCraft reads that part.
7. **Keep the work private.** FilmCraft and EffectCraft write auto-save copies, caches and recent-file lists, next to the project or under AppData [2][31][33][38]. Use the portable zips, keep one encrypted working folder (inside the VeraCrypt container, W-25) that does not sync to the cloud, and never install or run the Launcher (D-12).
8. **Real memories stay real.** You can restyle, animate and connect real photos. You cannot invent events or people, or put words in anyone's mouth. Reconstructed scenes are visibly labelled. No synthetic or cloned voice of any real person, living or dead, is ever used, even with consent (charter, principle 4; D-16), and the premiere cut carries no synthetic voice at all (W-46).
9. **Stay inside the Craft boundary (D-12).** A Craft app may touch only a copy in a `work\` folder, a chapter whose spec and OTIO are in the repo, or a title whose SVG fallback exists. It is never the only writer or reader of a format, never the holder of the only copy of anything, and never a step in the week before the premiere (Sat 20 to Sat 27 Feb 2027). SoundCraft is learning-only and never in the delivery path.
10. **No deity, and nothing from her seva space, in a Craft file (W-61, W-70).** No deity is drawn, generated or photographed, so none is ever in a chapter bundle, a graphic clip or an EffectCraft comp; a deity can appear only as a symbol or a seva object that is not a svarupa. Her morning sounds are captured under the W-70 rule and arrive as WAV; nothing here handles a seva article.

## How to do it, step by step

Steps 1 to 6 are set-up, for weeks 1 and 2. Steps 7 to 12 are the chapter loop, repeated for each chapter.

**Step 1. Make the folders.** Suggested layout on the Windows PC, on one encrypted drive if you have one:
- `C:\LifeJourney\tools\` holds one folder per app and tag, named `filmcraft-<tag>`, for example `filmcraft-v0.9.0`.
- `C:\LifeJourney\work\stills\` and `C:\LifeJourney\work\audio\` hold the media the agents hand you. Keep these paths, because the OTIO files point to them.
- `C:\LifeJourney\projects\` holds your FilmCraft project files. (Our suggestion.)
- `C:\LifeJourney\exports\` holds renders. (Our suggestion.)

**Step 2. Download the pinned version.** Get the portable x64 zip for the tag you are testing (v0.9.0 first, then v0.8.0; see Template A) from that tag's GitHub release page. The pins are frozen Sun 25 Oct and nothing is upgraded mid-chapter (W-22). Never install or run the ArtCraft Launcher (D-12), because it installs and updates the apps on its own [63]. Do not use the MSI installer for production either. Its command-line tool is not on the PATH [14], and its data goes to AppData [2].

**Step 3. Check the download.** In PowerShell, run:

    Get-FileHash -Algorithm SHA256 "C:\Users\<you>\Downloads\<zip name>"

Compare the result with the pin table in the Templates section. If it does not match, do not run the file. Download it again. If it still differs, tell the agent team. Optionally, run `Get-AuthenticodeSignature` on the `.exe`. TODO(research): whether the downloaded portable binaries are code-signed as the release implies.

**Step 4. Unzip.** Unzip into `C:\LifeJourney\tools\filmcraft-<tag>\`. The zip holds `filmcraft.exe`, `filmcraft-cli.exe` and a file called `portable.txt` [15]. That file keeps the data folder beside the program, not in AppData [2].

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

If spike SP1 fails, the bundle has no `ch01.xml`. After Step 8 the maker makes both interchange files from FilmCraft, each saved into the bundle folder: File > Export > Final Cut Pro XML… (`file.exportFcp7Xml`) writes the FCP7 XML as `ch01.xml`, and File > Export > OpenTimelineIO… (`file.exportOtio`) writes the OTIO as `ch01.otio`. FCPXML… and EDL… sit beside them in the same menu and are not part of this hand-off (Pitfall 8 covers FCPXML). The FCP7 XML is what goes into Resolve in Exercise 6.

Copy it into `C:\LifeJourney\work\`. Keep the folder layout exactly as delivered. The OTIO points to its media with relative paths (`media/ch01_s01.png`), resolved against the `.otio` file's own folder [5]. Kdenlive does not decode `file://` URLs, so the OTIO must never carry one [72]. The FCP7 XML keeps absolute `file://localhost/C:/...` paths [8]. Keep `media/` beside `ch01.otio`. If you must move the folder, ask the agents first.

**Step 8. Import and read the report.** First make the sequence yourself, as Template B says, and never drop a still onto an empty timeline. Then, in FilmCraft, choose File > Import and open `ch01.otio`. Read the import report before you touch anything [9]. Look for three things: no red "MEDIA NOT FOUND" slates, the Ken Burns keyframes present, and no unexpected "not supported" lines. Write any problem in your change list and tell the agents.

**Step 9. Refine what FilmCraft is good at.**

**Story pass first.** Before you touch a keyframe, watch the chapter once with its sound playing (her-world sound, the hummed tune in its venue or phone take (W-65) and, if one passed one-key-three-guards, one HER-PUBLIC line; the premiere cut has no other recorded voice, D-05). Then ask four things. (a) Which photo carries this chapter? It is the weight-3 shot the agents marked (see below). Check they chose the right photo, then decide whether it needs more time than the full voice line gives it. (b) Is there a hard moment, such as a loss or a leaving? Cut there, do not dissolve. A dissolve softens the moment, and a cut states it. (c) Does every move end before the sentence it sits under ends? If not, shorten the move, not the sentence. (d) Is any face partly cropped? Check it against the crop decision recorded for that shot in the manifest (Template C).

By default the agents set each still's time and move from its `weight`, unless the spec overrides it. Weight 1: 3 to 4 seconds, with a 6 to 8 percent push. Weight 2: 5 to 6 seconds, with a 10 to 12 percent push that alternates between push-in and drift. Weight 3 (the photo that carries the chapter, at most one per chapter): the full voice line about it, at least 7 seconds, with no move or a push under 4 percent, and hard cuts on both sides. Every move ends on or before the end of the voice line under it. In the premiere cut a "voice line" is a card, an attributed-text beat or a sound cue, or the one HER-PUBLIC clip if it passed; recorded relatives' voices are April-version items (D-05, D-06), so read "voice line" as the card or cue under the shot. The agents mark the weight-3 shot in the spec; your first job is to check they chose the right photo.

**Cards in her idiom move less (W-72).** The default weights above are for photographs. A card in the pichwai manner or a floor-art card is moved only by a push or pull of up to 8% or a pan of up to 5% over a still field, plus leaf sway, a water ripple on a band, a lamp flame, falling petals, or a gulal puff over hands and table (never over a deity or a face). Borders and bands never move, nothing with a face moves (cow friezes included), gold and silver stay flat, and there is no dissolve, wipe, burn or shatter on such a card. So the weight-2 push of 10 to 12 percent does not apply to it, and FilmCraft's default dissolve is retimed to a cut.

Then work in this order:
- **Ken Burns moves.** Drag the scale and position keyframes in Effect Controls. Use the value and velocity graphs to check the easing.
- **Dissolves.** Retime them, or re-centre them on the cut.
- **Titles.** Use the Type tool for simple Latin titles and lower thirds. Gujarati and Devanagari titles and cards arrive from the agents as shaped outlines and are placed as graphics, never typed as live text (W-21, W-75). Must-read type clears the phone floor: x-height 3.8% of picture height as the target, 3.2% as the hard floor (W-63).
- **Sound under a voice.** Use Essential Sound > Music > Ducking against Dialogue. It writes volume keyframes [17]. In the premiere cut the only voice is a HER-PUBLIC clip if one passed (D-05) and there is no music bed (W-44), so ducking is used for her-world sound under that clip; music under voice is April-version work.
- **Save** into the project folder. At the end of each session, choose File > Save a Copy as a second copy [2].

**Step 10. Hand back the changes.** Export the interchange files (File > Export > OpenTimelineIO… and File > Export > Final Cut Pro XML…) and the marker list (Markers > Export Markers as CSV…, command `markers.exportCsv`, which needs an open sequence; the code places it under the Markers menu [83], so confirm the location on first use). Return them with a short change list: shot number, what you changed and why. The agents read the file, compare it with the spec, and update only the parts you did not touch.

**Step 11. Make the final files.** Who runs this depends on Decision 1.
- **Archive master.** Export with the preset "Apple ProRes 422 HQ", at the sequence size and frame rate, with 48 kHz 24-bit audio [11]. Use "Apple ProRes 4444" only if the film has transparency or smooth gradients that band.
- **Phone files (W-63).** PH1 and PH2 are encoded from the ProRes master by the mobile-delivery recipes (`playbooks/mobile-delivery.md`), never from FilmCraft's own encoder and never from the venue file; they differ from the venue file only in Trim P, their caption burn-in and their encode.
- **Venue copy (W-17).** Encode the master to a 1080p24 H.264 file with ffmpeg: `-c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart`, with AAC-LC at 256 kbps, 48 kHz stereo. Captions are burned in, the file name is neutral and the metadata is stripped. The research note tested CRF 16 with AAC at 320 kbps; the register's venue file is CRF 18 with a 20 Mbps cap. The research note gives this reason for not using FilmCraft's own encoder: it lacks several quality tools, such as trellis and psy-RD [18]. Also make a Main profile, level 4.0 backup at about 8 Mbps for the venue laptop (W-17). If the venue's written answer (due Sun 15 Nov) says it is a cinema with a DCP server, the 2K Flat DCP becomes the primary deliverable and is made on the PC, never in the container.
- **Check.** Run ffprobe on each file: codec, pixel format, frame rate, and frame count against the expected duration. Measure the sound with `ebur128` [61] against the Decision 5 targets (W-19).

**Step 12. Archive.** Keep two copies: the working drive, and a second encrypted SSD kept elsewhere. There is no cloud copy of family media (W-25). Each copy holds the master, the project file, the OTIO, the FCP7 XML, `build_info.json`, and a media list with a SHA-256 for every file.

## Learn-by-doing exercises

Times are our estimates, not measurements. Do Exercises 1 to 6 in order. Exercises 7 and 8 are optional.

### Exercise 1. Install, verify and start FilmCraft

- **Goal:** a verified, running portable copy of the candidate FilmCraft tag, with a log entry.
- **Steps:**
  1. Download the portable x64 zip of v0.9.0 (the candidate) from its release page. If it fails the five-minute test, use v0.8.0 (Template A).
  2. Run the hash check in Step 3 and compare it with the pin table.
  3. Unzip into `C:\LifeJourney\tools\filmcraft-<tag>\`, for example `filmcraft-v0.9.0`.
  4. Start `filmcraft.exe`. If needed, try the graphics fallbacks in Step 5.
  5. Run `filmcraft-cli.exe --version`.
  6. Open an empty project and note the RAM use.
- **Time (estimate):** 45 minutes, plus download time.
- **What good looks like:** the hash matches. The app opens and stays open. The CLI prints a version. Your log says which graphics setting worked and gives the RAM use with an empty project.

### Exercise 2. Pan and zoom a test card

- **Goal:** learn the scale numbers that make a still fill the frame.
- **Steps:**
  1. Ask the agents for two test cards: a 3600x2400 gridded still, and its 2880x1620 conformed copy.
  2. In the New Sequence dialog, set Timebase to 24 frames/second (the project rate, W-14; the research ran this step at 25, so the 24 setting is untested) and keep 1920 x 1080. The dialog has no preset list. Read the frame rate back before you press OK. The engine's default for a new sequence is 23.976 (`file.newSequence` @v0.8.0), so never accept a default.
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
  1. If the agents did not deliver `ch01.xml`, export it first as Step 7 says (File > Export > Final Cut Pro XML…). In DaVinci Resolve (free), choose File > Import Timeline (Media Pool right-click > Timelines > Import also works) and import `ch01.xml` first. In the dialog, tick **Use sizing information** and leave **Mixed frame rate format** on **DaVinci Resolve**. Check: the stills are online; each still is 5 seconds (not one frame, not 29.97-based); Inspector > Edit Sizing shows Zoom and Position keyframes at the right frames; Opacity keyframes appear in Composite; dissolves are present. Then import `ch01.otio` and note what is lost (motion is expected to be lost). Record the version in Help > About.
  2. Fill in Template F, one row per feature.
  3. Note any warnings Resolve shows, and copy them in.
  4. Open the OTIO in Kdenlive too. Note whether the still-image clips arrive.
  5. Copy `ch01.otio` alone into an empty folder and import it. Note whether Resolve asks for the media folder. This tests how Resolve reads the relative paths (TODO(research): Resolve's handling of relative `target_url`s is unverified; the manual documents the folder prompt for OTIO [74]). If it cannot link them, a Resolve-only `chNN.otioz` bundle is the candidate fallback, not yet part of the hand-off.
6. Send the table to the agents. They use your result for Decision 2.
- **Time (estimate):** 1.5 to 2 hours.
- **What good looks like:** a complete table, with yes, partial or no in each cell, and any warnings copied in. The Resolve 21 manual says FCP 7 XML keyframes for Opacity, Position, Scale and Rotation import when 'Use sizing information' is ticked [74], but FilmCraft's numbers in Resolve are untested, so this test is the only real check we have [55][74]. If Ken Burns does not survive into Resolve, the baked-motion fallback becomes the plan for every chapter.

### Exercise 7 (optional). Duck music under a voice in Essential Sound

- **Goal:** learn how FilmCraft ducks music under speech. This is mostly April-version work: the premiere cut has no music bed (W-44) and at most one HER-PUBLIC clip (D-05).
- **Steps:**
  1. Ask the agents for a 30-second synthetic "voice" test track (tones with pauses), and a 30-second music bed. Use synthetic test material only.
  2. Import both onto separate tracks.
  3. Apply Essential Sound > Music > Ducking against Dialogue.
  4. Play it. Note the dip and the recovery.
- **Time (estimate):** 1 hour.
- **What good looks like:** the music dips while the voice speaks and comes back in the gaps, with no clicks. The ducking shows up as volume keyframes [17].

### Exercise 8 (optional). One EffectCraft title with alpha

- **Goal:** learn the title path, and the font trap. The test title is Latin, in an OFL font. EffectCraft's shaping of Gujarati and Devanagari has not been tested, so a title in her script is never typed into a comp: it arrives as shaped outlines (an SVG path) and is imported as a shape (W-21, W-75).
- **Steps:**
  1. Ask the agents for a title spec (text, font, size, timing) and an EffectCraft project.
  2. Open the `.ecproj`. Check the font in the text layer's properties is the one you intended. If it shows Inter, the font is missing and was replaced [47][23]. Install the font first.
  3. Render 5 seconds as an RGBA PNG sequence, into a new folder name. Never reuse an old output name [47].
  4. Check that the PNGs have alpha.
  5. Import the sequence into FilmCraft as an image sequence: File > Import Image Sequence…, then pick the first numbered frame (or tick Import as Image Sequence in the Media Browser) [83]. Before the import, set Edit > Preferences > Media > Indeterminate Media Timebase to the comp's frame rate, because that setting, not the comp's rate, sets the imported rate. Keep 'Import numbered stills as image sequences' off for the stills chapters (Pitfall 23).
- **Time (estimate):** 2 hours.
- **What good looks like:** the right font, a transparent background, and the sequence plays over a colour in FilmCraft. The must-read type clears the phone floor (x-height 3.8% of picture height as the target, 3.2% as the hard floor; W-63).

## Templates and checklists

### A. Version pin record

Hashes are copied from each release's `SHA256SUMS.txt`, read on 2026-10-18 [40] (the v0.9.0 hashes from its own file [66]). Check them against the release page again before you rely on them.

| App | Tag | Use | Windows x64 portable zip SHA-256 | Tested on | Result | RAM observed |
|---|---|---|---|---|---|---|
| FilmCraft | v0.9.0 | candidate for production (test first) | `d370cac8ed2edd729c8129aa55f75d0123716ba3cddbf9c5e4e3f0fdaa101a5e` | | | |
| FilmCraft | v0.8.0 | fallback | `0119afd59dfd6ecb94470ba6b3a48108ade87dabd4972898dd6c04e1db396b0b` | | | |
| FilmCraft | v0.7.2 | retired (not pinned) | `8e22fabdf2f802573d3af4ad9993c05212dead5e933efda0fa290e825313cde7` | | | |
| EffectCraft | v0.11.1 | titles and line-drawing only | `78bd7f63c6bd814bc33f07bd523b003a5f8d095244c5f67bd70e902448fd6e34` | | | |

SoundCraft is not pinned for delivery. Do not use it for finished audio.

### B. Five-minute acceptance test (FilmCraft, Windows)

- [ ] The zip hash matches the pin table.
- [ ] `filmcraft.exe` starts. The working graphics setting is written down.
- [ ] `filmcraft-cli.exe --version` prints the expected tag.
- [ ] Create the sequence first: File > New > Sequence. Write down what the dialog shows (expected 23.976, 1920 x 1080, 48000 Hz). Set Timebase to 24 frames/second (W-14), keep 1920 x 1080 and 48000 Hz, name it `ch01`, OK.
- [ ] Never drop the first clip on an empty timeline. A still makes a sequence at its own pixel size and at 29.97 fps.
- [ ] Set Edit > Preferences > Media > Indeterminate Media Timebase to 24 before importing stills, then check that Sequence Settings still says 24. (Re-run this test at 24 before trusting the guard; it was written at 25.)
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
- [ ] Working copies named by shot id (`chNN_sNN.png`). No original file name appears in the working files.

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

| Feature | Plain OTIO (expected) | OTIO with FilmCraft metadata (expected) | FCP7 XML (expected) | Resolve free (manual says supported; your result) | Kdenlive (your result) |
|---|---|---|---|---|---|
| Still clips with duration | kept | kept | kept | | |
| Ken Burns (scale and position keyframes) | lost | kept, with easing | kept (easing handles not preserved) | | |
| Dissolves | kept | kept | kept | | |
| Opacity | lost | kept | kept | | |
| Audio clip level | lost | kept | kept | | |
| Markers | kept | kept | kept | | |
| Titles and graphic clips | lost | lost | lost | | |
| Image sequences | degraded | degraded | degraded | | |

Sources: [6] for OTIO, [8] for FCP7 XML, [51], [52] and [72] for Kdenlive, [55], [56] and [74] for Resolve. The Resolve 21 manual says FCP 7 XML Opacity, Position, Scale and Rotation keyframes import with 'Use sizing information' ticked [74]; whether FilmCraft's own numbers survive is untested, and your Exercise 6 test answers it. Resolve's FCPXML results remain open (TODO(research); [57] is a search summary only).

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
- [ ] Working copies are named by shot id. The id-to-original map stays offline on the maker's PC, never in the repo, which is public (D-14, D-26).
- [ ] From v0.9.0, FilmCraft opens stored media paths only on local drives or the document's own share. Do not put the project on a NAS or UNC path [65].

## Decisions you'll need to make

Each decision lists the options and our current lean. The lean can change after the tests.

### Decision 1. Where heavy rendering runs

- **Options:** (a) the Linux container, using the Craft command-line tools, if spike SP1 passes; (b) the container, using ffmpeg and code only; (c) your Windows PC.
- **Our lean:** (b) is the safe default. Use (a) only if SP1 passes. Use (c) for interactive work and short exports. Revisit after SP1, in weeks 1 and 2.
- **Register status (W-23, W-24, D-15):** decided. The container renders test cards, synthetic material and Route A drawn scenes only. Real family stills render on the PC (`lj.ps1 run <shot>`), because scripts travel to the photos and photos stay home. Every photo set carries `cloud: none` by default, and only the maker raises it.
- **What we know:** the container has 4 CPUs, 16 GB of RAM and no GPU [62]. No minimum RAM, disk or GPU is published for any of the three apps [58]. At 24 fps a 12-minute film is 17,280 frames, a 9-minute film is 12,960 and the 6-minute F-0 fallback is 8,640. At our 4-to-16 fps estimate (tested at 25, UNVERIFIED at 24: made at the research's rate and not re-measured), that is about 18 to 72 minutes for the 12-minute film and 9 to 36 minutes for F-0 at 1080p [E]. The vendor's own figures are on other hardware [12].

### Decision 2. Ken Burns: editable, or baked into video?

- **Options:** (a) keep the moves as editable keyframes in FilmCraft; (b) bake each move into video, so every editor shows the same move; (c) a mix.
- **Our lean:** (a) for the first chapter, because you can then adjust the moves by hand. Use (b) for any shot that must look the same in Resolve or Kdenlive [6][7].
- **Register status (W-41):** `zoompan` is for proofs only. A move baked into a delivered shot is rendered by the sub-pixel route (Pillow, or Chromium with GSAP writing `style.transform` for the ease only) and must pass MO8a at or below 0.05 px and MO8b at or below 0.04 px on the master before the delivery encode, measured with `mo8_audit.py` (`playbooks/cinematic-quality.md`). Roughness and the 1.3x ratio are informational only.

### Decision 3. Which second editor to test

- **Options:** DaVinci Resolve (free), which reads OTIO, FCPXML, FCP7 XML and EDL [55][56][74]; or Kdenlive, which reads OTIO. In Kdenlive, cuts, gaps, markers and dissolves (as luma mixes, by code) survive; effects, metadata and image sequences do not; `file://` URLs are not decoded; the project profile is taken from the first still's pixel size [51][72].
- **Our lean:** Resolve (free) for the one-time test in Exercise 6, and Kdenlive as a cut-and-dissolve backup without motion. The Resolve 21 manual marks no XML, OTIO or EDL import as Studio-only, but it has no free-versus-Studio table, so that is an absence of a restriction, not a statement that none exists [74]. TODO(research) for any free-edition limit on import. The current Kdenlive release is 26.08.2 [49]. OTIO support in Kdenlive dates from version 25.04 per search summaries [64].

### Decision 4. Frame size and rate for the whole film

- **Register status (W-14, W-15, W-16):** decided as the working default: 1920x1080 at **24 fps**, signed on the settings card Sun 1 Nov. It is no longer open.
- **Options (kept for the record):** 1920x1080 at the research's rate of 25 (its tests ran there; tested at 25, UNVERIFIED at 24; kept for the record); 1920x1080 at 24 or 30 fps; 3840x2160.
- **Our lean:** 1920x1080 at 24 fps, which is DCP-native, and stills held on twos give 12 drawings a second. The research tests and the time estimates ran at 25 fps, so they are UNVERIFIED at 24. Re-run r1, r5 and the colour-patch test at 24, then patch the guard values by hand: `zoompan d=120` for 5 s, Timebase 24, and `media.indeterminateTimebase` set to the string `"24"`. A 25 fps access copy is made with `fps=25` only if a 50 Hz-only venue judders (W-14). 4K is not needed; UHD is for single hero shots only if a 4K cinema is booked (W-15). A 4K film is estimated at about four times the render time [E].

### Decision 5. Loudness target

- **Register status (W-19):** decided as the working default: **-1 dBTP everywhere.** Render three venue masters (-23, -18 and -16 LUFS integrated) and choose at the Mon 22 Feb venue run against sixty seconds of the hall's own room tone recorded from the back row; if no reading can be taken, load -18 first. The online copy is -16 LUFS, -1 dBTP. Use two-pass `loudnorm`, the second pass linear. The earlier provisional lean (-18 LUFS with a looser true-peak ceiling) is superseded.
- **Options (kept for the record):** -23 LUFS (the broadcast standard); about -16 to -18 LUFS (home and online stereo). FilmCraft's export default is -23 LUFS with a -2 dBTP limit, and it is off by default [11].
- **Our lean:** the W-19 stack above. Decide the venue master on the night, not now.

### Decision 6. Which FilmCraft tag to pin

- **Options:** v0.9.0 (the newest tag, released 2026-10-18); v0.8.0 (the fallback); v0.7.2 (retired, not pinned).
- **Our lean:** test v0.9.0 first (per the v0.9.0 diff, its interchange code is unchanged and it fixes a UTF-8 `file:` prefix panic that Unicode paths can hit [65]); v0.8.0 as the fallback; v0.7.2 retired. Test again before any upgrade.
- **Register status (W-22):** default. FilmCraft v0.9.0 (fallback v0.8.0), EffectCraft v0.11.1 (it stays until a tagged 0.12.0 passes the five-minute test), SoundCraft not pinned; or the newest tag that passes the five-minute test on test day. Pins frozen Sun 25 Oct; no upgrade mid-chapter; no Launcher.

### Decision 7. How much EffectCraft to use

- **Options:** none; titles only; titles and one line-drawn sequence; 3D parallax as well.
- **Our lean:** FilmCraft's own graphic clips for static titles and lower thirds. EffectCraft only for one SVG line-drawn sequence, and for text with expressions if it is needed. Skip classic 3D parallax for now, because there are no CPU timings for it and there is a known memory issue [47][22]. Any EffectCraft render uses the thread procedure in Pitfall 10, not `RAYON_NUM_THREADS=2`. Register (W-38, W-21, D-12): chapter titles come from the Card A slips traced in VectorCraft (Inkscape fallback), a title needs its SVG fallback, and fonts are OFL only; her script travels as shaped outlines, never live text, and the line-drawn sequence is the floor-art line at the phone floor (W-72).

### Decision 8. Who cleans up voice recordings

- **Options:** FilmCraft's Essential Sound (repair and ducking); Audacity with its noise reduction; ffmpeg filters; SoundCraft.
- **Our lean:** Essential Sound for repair and ducking, with Audacity as the backup. Never SoundCraft for delivery. Its MP3 and AAC import can silently shorten or shift audio [48], and it has no sidechain input [34]. Register (W-20, D-05): found-voice cleanup is level, high-pass, hum and denoise only, never re-cut; the mix is made in REAPER (Resolve Free's Fairlight is the fallback); the premiere cut carries at most one HER-PUBLIC clip, and relatives' recorded voices arrive in the April version (D-06).

### Decision 9. The venue playback file

- **Options:** H.264 MP4 encoded with ffmpeg; ProRes MOV; FilmCraft's built-in H.264 preset.
- **Our lean:** H.264 MP4 from ffmpeg for the venue, with the 1080p safety copy. Keep ProRes for the archive. The research note assumes a projector PC plays H.264 MP4 reliably. Test that on the venue machine. TODO(research): colour management end to end (sRGB stills, Rec.709 sequence, ProRes tags, venue projector) needs a test-card pass.
- **Register status (W-17):** default is the 1080p24 H.264 venue file described in Step 11, plus a Main 4.0 backup and a 3-minute sound-and-stills fallback. The venue is asked by Fri 6 Nov; its written answer, due Sun 15 Nov, decides file or DCP. The venue visit (TD-L2b) uses a test clip, never the film, by Sun 17 Jan (W-56).

### Decision 10. When real material enters the tools

- **Options:** only after the pipeline is locked and every test in this playbook passes (charter); or earlier, for learning.
- **Our lean:** test cards only until the five-minute test and Exercises 1 to 6 pass, plus the Resolve check. Then the first real chapter, as a trial, in the encrypted working folder.
- **Register status (D-13, W-06, W-07):** decided. "Locked" means the P-LOCK process lock on Sat 14 Nov 2026, tested on synthetic material. Covert collection starts Sun 15 Nov, and the first real chapter is the slice, C01 (100 s, final Sun 20 Dec).

## Pitfalls

1. **Stills import at their native size.** Scale 100 means native pixels. A 3600x2400 still in a 1080p sequence shows a crop at 100. Use the cover scale, or conform the still first [5][6][11].
2. **Stills use a lot of memory.** FilmCraft decodes each still whole, about 34.6 MB for a 3600x2400 still. The decoded copy stays in a media pool that the research found has no memory-pressure eviction. Importing 300 such stills could hold about 10 GB [10][9][E]. Conform the stills first, and cut the film into chapters of one to two minutes.
3. **Render previews fill the disk.** One report of a 1080x1920 timeline gave 0.7 to 1.1 GB of preview per 30 to 47 seconds. Budget several GB. Do not play the Program monitor during an export; one reported export ran out of RAM and disk this way [45].
4. **Plain OTIO drops features without a loud error.** Ken Burns, opacity and audio gain disappear. Read the import report every time [6].
5. **Malformed metadata is dropped silently.** If the agent's motion data has the wrong shape, FilmCraft imports a plain cut with no motion. Check after each import that the keyframes exist [6].
6. **Kdenlive aborts on missing media, and does not decode `file://` URLs.** An OTIO whose media is missing aborts the import, and Kdenlive flipped the video tracks when its OTIO went to Resolve, in one reported bug [54]. By code reading (`otioimport.cpp` lines 390-399 at v26.08.2; not run), a `file:///` `target_url` is treated as a path, so every clip is reported missing [72][73]. Agent-written OTIO therefore uses relative `target_url`s, and the folder layout stays fixed.
7. **Scale means different things in other editors.** FilmCraft's Scale 100 is native pixels. Resolve and Final Cut use 1.0 for fitted. Stills conformed to exactly the sequence size agree at 100 [11][7].
8. **FCPXML `<video>` items are skipped by FilmCraft.** FilmCraft skips an FCPXML `<video>` or `<title>` that sits directly in a storyline (`fcpxml.rs` @v0.8.0 line 402), but reads a `<video ref=…>` nested inside a `<clip>` (line 386) [7][69]. One FCPXML 1.13 sample from a third-party repository shows Final Cut writing a still as a bare `<video>` [76], so FilmCraft would skip Final Cut's stills in that form. Whether Resolve writes stills the skipped way is unverified, and FilmCraft's tests use only its own output and hand-written examples [7]. Do not plan a return path through FCPXML; use FCP7 XML. Whether Resolve accepts stills written as FCPXML asset-clips is TODO(research).
9. **The project format changes often.** FilmCraft's project schema moved from 13 to 15 in five days, and older builds refuse newer files [2][3]. Do not hand-write project files. Let the tool write them.
10. **EffectCraft's CPU renders have no memory cap.** In one reported case, an out-of-memory crash left an MP4 without its index, so it would not play [47]. `RAYON_NUM_THREADS=2` is not a bound: the #1615 reporter measured 6.8 GB with it in their project [71]. Start every new comp at `RAYON_NUM_THREADS=1`. Render a 30-frame sample under `/usr/bin/time -v` (Task Manager on Windows) and record its peak memory. Raise the thread count only while peak memory stays under half of free RAM. Where that is too slow, render frame by frame with `render-frame` to PNG and encode with ffmpeg, which is what the reporter did [71]. `EFFECTCRAFT_CPU_INFLIGHT` exists only in open PR #1763 (no reviews on 2026-10-18) and does nothing in v0.11.1 [70]. Render one job at a time, and check each output with ffprobe [30]. One search summary, not opened by the research, reports heavy memory use on Windows 11 with an Intel Arc card [60].
11. **EffectCraft can overwrite the previous output.** A cancelled or failed overwrite destroyed the previous file, in one open issue [47]. Always use a new file name.
12. **Fonts fall back silently.** If a font is not installed, EffectCraft uses Inter instead [47][23]. A silent fallback is worse for Gujarati, where the wrong face can drop conjuncts or digits (W-21); her script is outlines, not live text.
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
23. **Image sequences need care in FilmCraft.** Our stills end in digit runs (`ch01_s01.png`). With Edit > Preferences > Media > 'Import numbered stills as image sequences' on, importing one still alone is taken as a sequence, so keep that preference off for the stills chapters [83].
24. **FilmCraft's defaults break the card motion limits of W-72.** The weight-2 push (10 to 12 percent), a one-second dissolve and a graphic clip's default entrance are all outside what a pichwai-manner or floor-art card may do. Set the card's move and cut by hand and check the import report.

## Best references

1. **FilmCraft repository** (github.com/storytold/filmcraft). Start with the README for formats, export and vendor status [1], then `docs/agents.md` for the command-line tool [14] and `docs/project-files.md` for saves, auto-save and recovery [2]. Worth your time because every step in this playbook runs through these three files.
2. **FilmCraft release notes** (github.com/storytold/filmcraft/releases). Shows what changed in each tag, including save-safety and Windows fixes [42]. Read it before any upgrade.
3. **EffectCraft repository** (github.com/storytold/effectcraft). The README gives the project's own status statement and the list of features [20]. `docs/agents.md` is the command-line cookbook for titles and renders [21].
4. **EffectCraft issue 1615** (github.com/storytold/effectcraft/issues/1615). The clearest published numbers for CPU render memory and the out-of-memory risk [47]. Re-read it before quoting.
5. **SoundCraft gaps list** (github.com/storytold/soundcraft, `docs/gaps.md`). Read it to see why SoundCraft is not in the delivery path [34].
6. **Kdenlive file menu documentation** (docs.kdenlive.org/user_interface/menu/file_menu.html). What Kdenlive does with OTIO files [51]. Pair it with the KDE forum post on OTIO metadata being dropped (discuss.kde.org/t/opentimelineio-metadata-and-effects/45813) [52].
7. **DaVinci Resolve product page** (blackmagicdesign.com/products/davinciresolve). The free edition's limits, such as 8-bit video up to UHD at 60 fps [55]. The Resolve 21 Reference Manual is the primary source for the import dialogs and the supported-effects tables [74]: read its pages 482, 484 and 521-523 first, then test the rest yourself.
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
- [68] github.com/storytold/filmcraft, `crates/ui-egui/src/panels/sequence_settings.rs`, `crates/ui-egui/tests/sequence_ui.rs` and `crates/engine/src/commands.rs` @v0.8.0 and @v0.9.0. New Sequence dialog defaults (23.976, no preset list). Research follow-up F5.
- [69] github.com/storytold/filmcraft, `crates/interchange/src/fcpxml.rs` lines 383-406 @v0.8.0. FCPXML elements read and skipped. Research follow-up F1.
- [76] github.com/andrewarrow/cutlass at commit `4dbe20d` (2025-07-06), `samples/png.fcpxml`. Third-party FCPXML 1.13 sample with a bare `<video>` still; provenance inferred, not stated. Research follow-up F1.

- [65] github.com/storytold/filmcraft at tag `v0.9.0` (commit `4a69a038`, 2026-10-17 21:43 -04:00): `git diff --stat` against v0.8.0 and the interchange, engine and project-file diffs. Stored media-path restriction; interchange importers unchanged. Research follow-up F7.
- [66] `https://github.com/storytold/filmcraft/releases/download/v0.9.0/SHA256SUMS.txt` (curl, HTTP 200, 2026-10-18). Hashes of the v0.9.0 assets. Research follow-up F7.
- [70] `https://github.com/storytold/effectcraft/pull/1763` and `git ls-remote` of the EffectCraft tags, 2026-10-18 about 05:20-05:30 UTC. PR open, no reviews, not in any tag. Research follow-ups F4 and G6.
- [71] `https://github.com/storytold/effectcraft/issues/1615`, read through a summarising tool on 2026-10-18: the reporter's 6.8 GB figure with `RAYON_NUM_THREADS=2` and the frame-by-frame workaround. Research follow-up F4.
- [72] Kdenlive source at tag `v26.08.2` (`https://invent.kde.org/multimedia/kdenlive.git`): `src/otio/otioimport.cpp` (`resolveFile`, lines 390-399), `clipcreator.cpp`, `kdenlivesettings.kcfg`. Read as code, not run. Research follow-up F3.
- [73] `https://doc.qt.io/qt-6/qurl.html`: `QUrl::fromLocalFile` "expects path, not url with scheme" (summarised by a small model; re-read the exact wording). Research follow-up F3.
- [74] DaVinci Resolve 21 Reference Manual, `https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf` (187,277,990 bytes, 4,444 pages; searched as text). Pages 168, 482, 484, 486, 521-523 and 544-547. Research follow-ups F2 and G2.
- [83] FilmCraft v0.9.0 `README.md`, `docs/agents.md`, `crates/engine/src/commands.rs` (`markers.exportCsv`, `file.importImageSequence`) and `crates/ui-egui/src/menus.rs`: menu locations. Research follow-up G3.
- [84] FilmCraft v0.9.0 `crates/engine/src/{autosave.rs, settings.rs}` and `apps/filmcraft-cli/src/main.rs`: the Indeterminate Media Timebase key and value type; headless CLI runs do not load or save preferences. Research follow-up G4.

## Changelog

- **2026-10-18, v1 draft.** First version, written by a Haiku scribe from `research/craft-motion.md` and `CHARTER.md`. Not yet reviewed. Open items are marked TODO(research): maker's hardware and export speed; minimum system requirements (none published); whether DaVinci Resolve (free) limits imports; whether Resolve keeps Ken Burns keyframes from FCP7 XML or FCPXML; whether Resolve accepts stills as FCPXML asset-clips; how Kdenlive treats still-image OTIO clips; proxies and memory release for stills in FilmCraft (spike SP1); EffectCraft CPU timings for 3D, text animators and Trim Paths; Lottie in a real player; code signing of the downloads; colour management end to end; sync status of the maker's PC; the marker-list and image-sequence menu paths; release cadence over eight weeks (repos were 17 days old at the time of the research).
- **2026-10-18, v1.1 (round 1 review nudges applied).** Added a story pass to Step 9; added the SP1-failure fallback for `ch01.xml` to Step 7; corrected Exercise 2 sequence setup (no preset list, engine default 23.976); rewrote Pitfall 8 from the FCPXML evidence; working copies named by shot id (Templates C and H); Sources [68], [69] and [76] added.
- **2026-10-18, v1.2 (round 2 review nudges applied).** Replaced the absolute `file:///` OTIO paths with relative ones and recorded Kdenlive's `file://` limit (Step 7, Pitfall 6, Core principle 5, Decision 3); replaced `RAYON_NUM_THREADS=2` with the thread-measure procedure and the 6.8 GB and PR #1763 facts (Pitfall 10, Decision 7); pinned FilmCraft v0.9.0 (test first, v0.8.0 fallback, v0.7.2 retired) with `filmcraft-<tag>` folder names (Steps 1 and 4, Exercise 1, Templates A and H, Decision 6); replaced the TODO export paths with File > Export > Final Cut Pro XML… and OpenTimelineIO… and the marker CSV under Markers (Steps 7 and 10); replaced the Resolve test with the 'Use sizing information' test, changed Template F's Resolve header and removed the 'manual not reachable' sentences (Exercise 6, Best references 7, Decision 3); added the sequence-first steps and the Indeterminate Media Timebase check to Template B and Step 8; added the default weight mapping and the weight-3 photo check to the Step 9 story pass; closed the Exercise 8 image-sequence TODO from the code (Exercise 8, Pitfall 23).
- **2026-10-19, v1.4.** Reconciled with DECISIONS.md after the her-world merge (2026-10-19): the Sat 14 Nov lock is named P-LOCK and the Craft CLI spike is SP1 (Codes); card motion limits for her idiom (W-72); Indic titles as shaped outlines, never live text, with the phone type floor (W-21, W-75, W-63); the premiere sound under a voice (W-44, D-05) and the hum takes (W-65); PH1 and PH2 named in Step 11 (W-63); no deity and no seva article in a Craft file (W-61, W-70); the id-to-original map stays offline because the repo is public (D-14, D-26).
- **2026-10-18, v1.3.** Reconciled with DECISIONS.md (2026-10-18). Frame rate 24 fps (W-14, W-16) in Exercise 2, Template B and Decisions 1 and 4, with the guard values marked UNVERIFIED at 24 until r1, r5 and the colour-patch test are re-run; loudness -1 dBTP with three venue masters (W-19); venue file CRF 18 with a 20 Mbps cap and a Main 4.0 backup (W-17); real material after the process lock (P-LOCK) Sat 14 Nov and collection from Sun 15 Nov (D-13); `zoompan` proofs only and MO8a/MO8b on the pre-encode master (W-41); Launcher never installed and the Craft boundary (D-12); second encrypted SSD, no cloud copy (W-25); cloud policy for family stills (D-15, W-23, W-24); no recorded living voice in the premiere cut (D-05). Decisions 1 to 10 carry their register status.
- **2026-10-20, v1.5.** Stale-wording sweep (2026-10-20): Decision 1 and Decision 4 use the register's own form, "tested at 25, UNVERIFIED at 24", for the research's rate, with the 24 fps guard values still UNVERIFIED until r1, r5 and the colour-patch test are re-run (W-14, S-01); Decision 5 names the earlier, looser true-peak ceiling instead of quoting it (W-19, S-28); the v1 and v1.1 entries use the spike name SP1 (S-39) and the v1.3 entry names the process lock as P-LOCK (S-38).
