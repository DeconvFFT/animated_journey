# Free Desktop Toolchain: A Small Stack for the Life Journey

Track: toolchain · Draft v0.1 · 2026-10-18 · For the maker (a motivated learner)
Built from research/toolchain.md (Sonnet researcher, 2026-10-18) and CHARTER.md. Numbers in brackets, like [1], point to the Sources list at the end. Anything marked TODO(research) is still open.

**Status: provisional.** We do not fix the plan until you return the app checklist in Step 0. Your computer and the apps you already have decide which tools make sense.

## Why this matters for our life journey

Most of your mother's life happened between the big moments: the kitchen table, the drive to work, the song she sang badly on purpose. Those gaps are what will make the film feel like her. The toolchain is how we turn those gaps into moving pictures and sound without a studio.

The charter asks us to prefer scriptable tools [1]. A script can be re-run, repaired and handed to an AI agent. A menu click cannot. So this track picked a small stack. Blender handles depth, camera moves and renders. Inkscape handles maps, timelines and drawn lines. One video editor does the finishing pass. Two command-line tools, ffmpeg and ImageMagick, sit under all of it, and every shot passes through them [62][64].

Fewer tools, learned well, will finish the film. We have about 19 weeks until Saturday, 27 February 2027. The ten practice exercises below take about five weeks at two a week, which leaves about fourteen weeks for the real work [100].

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

Run the checks in the research checklist (see the table in the research notes, "Recognise your apps") and paste the output back to the team. We need:

- Your operating system and version. The charter records a Windows PC [1]. The research did not know this, so please confirm.
- Which of these apps are installed, with versions: DaVinci Resolve (Free or Studio), Kdenlive, Shotcut, OpenShot, Inkscape, GIMP, Krita, Blender, MagicaVoxel, Goxel, Blockbench, Audacity.
- Whether ffmpeg and ImageMagick run from a terminal.
- CPU, RAM, graphics card and its video memory, free disk space, and whether you have a pen tablet.

Two answers change the plan. MagicaVoxel runs only on Windows and macOS, and Blender 5 needs Apple Silicon on a Mac [24][30][56]. Resolve has an External scripting setting, which is the place to check whether outside programs can drive it [6][7] (see Decision 1).

The charter also names the ArtCraft Crafting Apps as refinement layers [1]. This track does not cover them. The craft-visual and craft-motion tracks do.

**Shell warning.** The commands in this playbook use Unix-style syntax. The research ran them on Ubuntu in a sandbox, not on your computer [100]. Windows forms are untested. TODO(research): confirm which command shell you will use, then re-test the recipes there.

### Step 1: Make the project folder

Keep the project in the private GitHub repository the charter names [1]. The cloud session is temporary, so the repo is the safe copy [1]. The research proposes these folders: `exercises/` (one folder per exercise, `ex01`, `ex02` and so on), `looks/` (saved colour recipes), `layers/` (cut-out PNG files), `licences/` (a saved copy of each licence page, with the date you saved it), and `credits.txt`. Add a `README.md` that names every tool and its version.

### Step 2: Install or find ffmpeg and ImageMagick

ffmpeg is the glue that most steps depend on [62][63]. The ffmpeg project ships source code only. Windows builds come from third parties such as gyan.dev or BtbN [62]. Some projects warn about look-alike download sites [45], so download from official sites only. ImageMagick has Windows binaries [64]. Check what runs with `ffmpeg -version` and `magick -version` (older ImageMagick installs use `convert`), and write the results in your README.

### Step 3: Prepare photos in a batch

Practise with stock or synthetic images now. Real photos come in only after the pipeline is locked [1].

When real photos arrive, scan at the highest resolution you can. The research's rule of thumb is at least 1.5 times your output width, so a camera move can crop without going soft: 2880 px wide for 1080p, 5760 px for 4K [100].

Crop every photo to 16:9 in one ImageMagick batch [64]. A 3000×2000 test photo came out at 3840×2160 this way [100]:

```
mogrify -path out/ -resize 3840x -gravity center -crop 3840x2160+0+0 +repage -quality 92 in/*.jpg
```

On ImageMagick 7 the command starts with `magick mogrify` [100]. Keep the originals in their own folder and never overwrite them. Check the result with `identify -format '%f %wx%h\n' out/*.jpg`.

### Step 4: Make a Ken Burns move by script

A Ken Burns move is a slow push-in or pan across a still photo. Two rules come from the tests [100]:

- **Crop to the output shape first.** On a 3:2 photo, ffmpeg's `zoompan` stretched the picture by about 18 percent. A circle came out 641 by 541 pixels.
- **Upscale before you zoom.** `zoompan` moves in whole pixels, so a larger source keeps the motion smooth. This is the usual workaround. The research did not test the case without the upscale [63].

A five-second push-in at 25 frames a second is the tested command [100]:

```
ffmpeg -loop 1 -i photoA.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z='min(1+0.0008*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 kbA.mp4
```

Join two clips with a one-second dissolve using ffmpeg's `xfade` filter [63]. Recipe R1 in the research notes has the full set [100].

### Step 5: Cut out layers for parallax

To move a foreground differently from a background, cut the photo into layers. There are three routes:

- **By hand** in GIMP 3.2 or Krita: a selection, a layer mask, then export a PNG with transparency. This gives the most control, and nothing leaves the machine [46][51].
- **Assisted, locally.** `rembg` removes the background of a main subject (MIT licence) [73]. SAM 2 can click out several objects (Apache-2.0) [74].
- **Depth.** Depth Anything V2 Small is Apache-2.0. The Base and Large models are CC-BY-NC-4.0 [72], so ask the maker before using them.

Filling in the background behind a cut-out invents pixels. Keep the fill minimal, keep the original, and label the result as a reconstruction [1].

### Step 6: Parallax in Blender by script

Put each layer on a flat plane at its own distance, slide the camera, and render the frames. The near layers then move more than the far ones, which is parallax [71]. The tested script is recipe R2 in the research notes [100]. Three settings matter most:

- **Set the view transform to Standard.** Blender's default, AgX, washed out the test photos. Standard kept their colours [100].
- **Draft at 640×360 with four samples; finish at 1080p.** Fifty frames at 640×360 took about 64 to 66 seconds on four CPU cores with no graphics card [100]. A 1080p frame has about nine times the pixels. A 30-second shot at 25 frames a second, at about 12 seconds a frame, would take about 2.5 hours [100] (the research's extrapolation).
- **Run it from a terminal with no window.** Blender's own command line is `blender -b -P script.py` [25]. The research ran the Blender Python module, not the Blender program [100], so check the program on your machine.

Turn the PNG frames into a movie with `ffmpeg -framerate 25 -i renders/p_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p parallax.mp4` [100].

### Step 7: Draw lines that reveal (maps, routes, titles)

To make a route or a signature draw itself, draw it in Inkscape as one stroked centre-line path [35][36]. Inkscape does not animate on its own [35], so a script does it. The script writes one SVG file per frame, with a dash pattern that shrinks from full length to nothing, then renders each frame [65]. Recipe R3 in the notes reads the path's real length from the file. Do not type the length in by hand. The renderer used in testing ignored `pathLength="1"`, so every frame looked finished until the length was computed [66][100].

Forty-eight frames at 1280×720 took 1.9 seconds on the research machine [100]. Titles set in outline fonts will not "write" with this method, because outline fonts are filled shapes, not single lines. Use a single-line font, or trace a handwritten title with Inkscape's tracing or calligraphy tools [36].

Blender can also reveal a curve or a Grease Pencil drawing with a build effect [28][29][100].

### Step 8: Assemble the chapter in the editor

Kdenlive 26.08 is the default editor [8][9]. It is built on MLT, the same engine that sits under Shotcut [14][20]. Kdenlive can save a render script that you run with `melt` [11], and an agent can write MLT XML directly and render it with `melt` [17][18].

Two traps from the tests [100]:

- **Always set the profile.** Without `-profile atsc_1080p_25`, `melt` uses a PAL standard-definition frame (720×576).
- **Crop photos to 16:9 before you place them.** A 3:2 photo otherwise letterboxes.

Do the final cut by hand: timing to music, framing and the last pass.

### Step 9: Give each decade its own look

Every decade gets one saved colour recipe, so every photo from that decade matches. The research wrote two examples as ffmpeg filter chains [63][100]. One is a warm, lifted, slightly faded 1970s look with grain and a vignette. The other is a 1950s black-and-white look with lifted blacks and grain. Save the exact text of each recipe in `looks/`. Do not colourise black-and-white photos with AI unless you label the result as a reconstruction [1].

### Step 10: Sound

Build the sound in this order: voice first, then the music bed ducked underneath it, then room tone and effects. Use only music whose licence allows public screening and a private link (see Decision 6).

Set the loudness with ffmpeg's loudness filter, `-af loudnorm=I=-16:TP=-1.5:LRA=11` [63][100]. On a test file it moved the level from −22.1 to −16.0 LUFS [100]. The broadcast reference is −23 LUFS [97]. A projector room with small speakers often needs something louder. Test it in the room.

### Step 11: Captions

Draft the captions with Kdenlive's speech-to-text, which can use VOSK or Whisper [13]. Whisper is also available on its own. It runs locally after its model is downloaded, and it can print SRT files from the command line [75]. Then proofread every name and place by hand.

Burn the captions into the screening file, because burned-in text is the one kind every screen shows [12][13]. Keep a sidecar `.srt` file for the archive. The research's burn-in command names a font that may not be installed on your computer. Pick a font you have [100]. TODO(research): verify burn-in on Windows.

### Step 12: Export three versions from one master

From one master file, make three versions [91][95][92]:

| Version | Container and codec | Main settings |
|---|---|---|
| **Screening** (TV, USB stick, projector) | MP4, H.264 High profile | Level 4.1, yuv420p, 1080p, AAC-LC 48 kHz stereo, `+faststart`, BT.709 tags |
| **Private web link** | MP4, H.264 High profile | CRF 20, 12 Mbps cap at 1080p. YouTube recommends 8 Mbps for 1080p at 24 to 30 frames a second [91] |
| **Archive** | ProRes 422 HQ in `.mov`, and/or FFV1 version 3 in Matroska | Audio PCM 24-bit or FLAC. The Library of Congress lists both in its 2025–2026 preferred formats for moving images. An MP4 counts only as a viewing copy [92][93][94] |

The screening command, as tested [100]:

```
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart deliver_usb.mp4
```

The research tested this without the `-maxrate` and `-bufsize` pair. Those two are a safety margin.

**Watch the file size.** A FAT32 USB stick cannot hold a single file over 4 GB minus one byte [96]. At about 12 Mbps video plus 256 kbps audio, that is about 46 minutes. At 20 Mbps, it is about 28 minutes [100] (the research's arithmetic). Format the stick as exFAT, or keep each file under the limit, and test on the screen. Whether your screen takes exFAT, MKV or soft subtitles is unknown. TODO(research): no TV or projector format specification was readable.

### Step 13: Check every file

Run ffprobe on each output. For the screening file, expect H.264 High, level 4.1 (ffprobe prints it as 41), yuv420p, 1920×1080, AAC-LC at 48,000 Hz, two channels [100]:

```
ffprobe -v error -show_entries stream=codec_name,profile,level,pix_fmt,width,height,sample_rate,channels -of csv=p=0 file.mp4
```

Then check the file size against the stick's limit, and check the loudness again.

### Step 14: Rehearse on the real screen

Play the screening file from a USB stick on the actual TV or projector, with the venue's cable or adapter if you can. Keep a laptop backup: play the master in VLC or mpv, set the laptop to 1920×1080, mirror the displays, and turn off notifications and sleep [100]. Venue and screen are still open decisions in the charter [1].

### Step 15: Archive

Keep the master file or files, the SRT and VTT caption files, the project files, the original scans and audio, the source SVG and Blender files, a README that names every tool and version, a licence and credits file, and SHA-256 checksums. Keep two physical copies and one off-site copy. Check the checksums every year, and migrate formats before they die (research archive checklist). The preferred archive formats above come from the Library of Congress [92].

## Learn-by-doing exercises

Each exercise has a cap of about two hours, from the research notes. The research did not time the exercises one by one [100]. Practise on synthetic or stock images and a few non-sensitive family photos. Keep the real hero material for the vertical slice [1]. Put each exercise in `exercises/exNN/` in the private repo, and keep every command line you run.

### Exercise 1: Inventory and dry run

- **Goal:** Know what you have, and prove the batch crop works.
- **Steps:** Fill in the Step 0 table. Install or locate ffmpeg and ImageMagick (Step 2). Batch-crop five stock photos to 3840×2160 (Step 3).
- **Time:** Under 2 hours.
- **Good looks like:** `ffmpeg -version` and `magick -version` both print. Every output reads 3840×2160, a 16:9 ratio.

### Exercise 2: Ken Burns by script

- **Goal:** Three moves by script, joined by dissolves.
- **Steps:** Make a push-in on one photo, a pan on another, and a third move of your choice, each about six seconds, using Step 4. Join them with one-second `xfade` dissolves.
- **Time:** Under 2 hours.
- **Good looks like:** ffprobe reports 1920×1080, 25 frames a second, H.264. A round object is not squashed. The slowest move shows no shimmer.

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

- **Goal:** Run recipe R2 on the Exercise 4 layers.
- **Steps:** Render a 480p draft, then a 1080p final. Set the view transform to Standard. Turn the frames into a movie with ffmpeg. Write the time per frame in your notes.
- **Time:** Up to 2 hours, plus render time.
- **Good looks like:** A colour patch in the render matches the source photo. The render runs from a terminal with no window open. The time per frame is written down.

### Exercise 6: A line-draw route or title

- **Goal:** Draw a route or a signature as one stroked centre-line path in Inkscape, then make it draw itself.
- **Steps:** Draw the path. Copy its `d` attribute from Inkscape's XML editor. Run recipe R3 (or the Blender version, R3b). Add easing [65][100].
- **Time:** Under 2 hours.
- **Good looks like:** The line starts, finishes and eases as designed. The last frame matches the static SVG exported from Inkscape. The script reads the length from the file, not from a number you typed.

### Exercise 7: Era looks

- **Goal:** One saved colour recipe for each of three decades.
- **Steps:** Take three photos from three decades (or stock images) and one modern clip. Build a look for each decade with recipe R7 or the editor's colour page. Save each as a text file in `looks/`.
- **Time:** Under 2 hours.
- **Good looks like:** The old looks have lifted blacks and lower saturation, which the scopes or histogram show. The same recipe applied twice gives identical output.

### Exercise 8: One voxel hero object

- **Goal:** Model one household object from a reference photo as voxels.
- **Steps:** Model it in MagicaVoxel (Windows or Mac) or Goxel or Blockbench [56][58][59]. Export OBJ or PLY. Import it into Blender with forward axis Y and up axis Z [100]. Add warm light (recipe R4). Render a five-second turntable.
- **Time:** TODO(research): modelling time per object was not measured. This exercise may run longer than two hours.
- **Good looks like:** Someone who has not seen the photo names the object. The model uses 32 colours or fewer. It stands the right way up. Each frame renders in under 30 seconds at 960×540 on your machine. That is the research's target. Its four-core test machine took 8 seconds for one still [100]. Use a test viewer who does not know the subject, and who would not mention it to her.

### Exercise 9: Sound and captions

- **Goal:** Forty seconds of narration over a licensed music bed, ducked, levelled and captioned.
- **Steps:** Record narration with a phone voice memo, using your own voice on a practice script. Add a CC BY or CC0 track (Decision 6). Save the credit text from the licence page into `credits.txt`. Duck the music under the voice. Apply loudness normalisation (Step 10). Draft the captions and proofread them (Step 11).
- **Time:** Under 2 hours.
- **Good looks like:** The loudness report is within 1 LU of the target. Captions line up within about 0.2 seconds at three spot checks. Every name is spelled right. The credit text matches the wording the licence asks for.

### Exercise 10: Mini-chapter and delivery rehearsal

- **Goal:** A 60 to 90 second chapter, exported three ways, then played on the real screen.
- **Steps:** Cut Exercises 2 to 9 into one chapter. Export the screening, web and archive versions (Step 12). Play the screening file from a USB stick on the TV or projector. Write the archive README and the SHA-256 checksums (Step 15).
- **Time:** Up to 2 hours, plus playback time.
- **Good looks like:** The file plays from the stick with sound and captions. The ffprobe output matches the profile. A checksum check passes. The archive file opens in a second player. TODO(research): checksum commands on Windows are untested.

**Pace.** Two exercises a week finishes the set by about 22 November 2026, which is week five. That leaves about fourteen of the nineteen weeks for the vertical slice and the chapters. Re-time after Exercise 5, the first Blender render, because that is where a weak computer shows [100].

## Decisions you'll need to make

Each decision lists the options and our current lean. The lean is a suggestion for you to confirm, not a decision.

### Decision 1: Which video editor?

- **Kdenlive 26.08.** Free and open source, on Windows, macOS and Linux [8]. Its engine can be driven by a script [11][17]. It has speech-to-text and proxies [12][13].
- **DaVinci Resolve 21 Free.** Strong colour and sound tools, with official training [2][5]. Free is limited to 8-bit footage up to 60 frames a second and UHD [2]. Studio adds more, including noise reduction, film grain and hardware encoding [3].
- **Shotcut 26.9.27.** Free, with MLT XML projects [19][20]. Less tested here.
- **OpenShot 4.0.1.** The gentlest option, but it is not built on MLT [22][23]. Not recommended for this stack.

**Lean:** Kdenlive, unless you already work fluently in Resolve. If you do, use Resolve for colour and sound, and Kdenlive for batch assembly and captions. Resolve's scripting from outside is disputed (see Pitfalls).

### Decision 2: Where do parallax moves get built?

- **Blender planes (recipe R2).** Tested and precise, but slow to render [100].
- **Keyframes in the editor.** Quicker to learn, but not tested by the research [100].

**Lean:** Blender for the three or four hero moves, and editor keyframes for the rest. TODO(research): compare the time each route takes on your machine.

### Decision 3: Which voxel tool?

- **MagicaVoxel.** The research's judgement is that it is the quickest hand-modelling tool. It has a path-tracing renderer. It runs on Windows and macOS only, and it has no command line [56]. Its licence allows free use for any project, but not redistribution of the software [56].
- **Goxel.** Runs on Windows, macOS and Linux. Exports OBJ, PLY and glTF. It opens a window even for export [58].
- **Blockbench.** Cuboid models in a Minecraft style, free and open source, also a web app [59]. Its command line is unverified.

**Lean:** MagicaVoxel for modelling, if Step 0 confirms Windows. Goxel for converting the model to OBJ. TODO(research): run a timed modelling test.

### Decision 4: Which raster editor for cut-outs?

- **GIMP 3.2.6.** Layer masks, and a standard Python 3 interface since 3.0 [46][47][48]. The batch procedure name is unverified.
- **Krita 5.3.4.1.** Painting, masks and frame-by-frame animation. Its Python runs only inside the open program [51][54].
- **Photopea.** A web app. Avoid it for family photos [55].
- **ImageMagick.** Batch work only [64].

**Lean:** GIMP 3.2 or Krita, whichever you already have. ImageMagick for every batch.

### Decision 5: Where do heavy renders run?

- **On your laptop.** The research measured this on a four-core CPU with no graphics card, so it is slow [100]. Blender's stated minimum includes a graphics card with 2 GB of video memory [30].
- **In the cloud.** The charter asks for heavy work in the cloud wherever possible, because memory is tight on the maker's Windows PC [1]. The research did not test a cloud render path. TODO(research): test one. Note that a cloud route moves your files off your machine, and the charter says nothing personal is uploaded without your explicit say [1].

**Lean:** Follow the charter. Drafts stay on the laptop. Finals go to the cloud once a tested path exists, and only with your agreement about the files.

### Decision 6: Which music?

- **Free licences that clearly allow public screening and a private link.** Kevin MacLeod's incompetech tracks are CC BY 4.0. You must give credit, and his FAQ allows live productions and monetised YouTube [76][79]. Freesound sounds licensed CC0 or CC BY are fine. Avoid CC BY-NC [78][80]. The Sonniss GDC bundles are royalty-free, need no credit, and forbid AI training [82]. Kenney's game assets are CC0; its audio packs were not checked [83].
- **AI-generated music.** Suno's free tier is for personal, non-commercial use, and Suno assigns no ownership to free users [88]. Meta's MusicGen weights are non-commercial [90]. The US Copyright Office has published on AI and copyright, but the research did not read its conclusions [89].
- **Commercial songs from her life.** These need a recording licence and a publishing licence for any public or online showing. An unlisted YouTube link can still be flagged. Options, safest first: a licensed substitute with a similar mood; your own performance of the tune; an offline private showing only, which is your informed risk; or no music at all [100].

**Lean:** CC0 or CC BY tracks. No CC BY-NC. No AI music until its terms are read for public use. For her favourite songs, use a substitute or your own performance. Ask a rights professional if the film will be shown beyond the family. TODO(research): several licences were not read (see the TODO list below).

### Decision 7: Which export set?

- **Screening MP4** (H.264 High, level 4.1, 1080p) [91][95].
- **Private web link** (12 Mbps cap at 1080p) [91].
- **Archive** (ProRes 422 HQ in MOV, or FFV1 in MKV) [92].

**Lean:** All three, from one master, plus the laptop HDMI backup (Step 14). Use 4K only after the venue screen is confirmed. TODO(research): check HEVC 4K support on the real screen.

### Decision 8: Burned-in captions or soft subtitles?

- **Burned-in.** Every screen shows them, and nobody can switch them off [12][13].
- **Soft subtitles** (a separate track the screen can switch on or off). TV support is unverified [100].

**Lean:** Burned-in captions for the screening file. A sidecar `.srt` for the archive. Soft subtitles only after a test on the real screen.

### Decision 9: The venue and screen (the charter's open decision)

The charter has not yet fixed the occasion, the venue or the format [1]. These decide the final export. **Lean:** Do not choose the final export until the venue and screen are known. Until then, build all three versions.

## Pitfalls

**Version drift.** Blender 5.2 changed several calls from the older tutorials. The sequencer is `strips`, not `sequences`. `new_effect()` takes `length`, not `frame_end`. Video output needs the media type set to video before the file format is set to FFMPEG [100]. The Grease Pencil build effect's Python names are GROW, SHRINK and FADE, but the manual says Grow, Shrink and Vanish [28][100]. GIMP 3.0 replaced Python-fu with standard Python 3, and GIMP 2.10 plug-ins and scripts break [47][48]. Inkscape removed pre-1.0 options such as `--without-gui`, so old forum answers mislead [34][37]. Kdenlive's keyframes were reworked in versions 25 and 26 [12][99]. Treat any tutorial older than 2024 as concept only.

**Colour and geometry traps (all measured).**

- Blender's default view transform desaturates photos. Set Standard [100].
- A 3:2 photo stretches in `zoompan` and letterboxes in `melt` unless you crop it first [100].
- `melt` defaults to a PAL frame (720×576) unless you set the profile [100].
- Blender's OBJ importer assumes Y-up, but voxel tools are Z-up [56][100].
- An SVG imported into Blender comes in at about 0.000282 metres per pixel, so a bevel of 0.02 metres swamps the drawing [100].
- A renderer that ignores `pathLength` will show every line as finished [66][100].

**"Has a Python interface" does not mean "runs without a window."** Krita, Blockbench, Audacity, MagicaVoxel and Resolve Free run their scripts inside the open program [54][56][59][61]. The research ran these headless only: ffmpeg, ImageMagick, Blender's Python module, Inkscape's command line, `melt`, Synfig's command line and Goxel's export [100]. Glaxnimate's pip package would not import on Ubuntu 24.04 without extra libraries [39][100]. Goxel opens a window even when it exports [58].

**Resolve Free scripting is disputed.** The Blackmagic README mirror says the scripting interface is common to Free and Studio [6]. A third-party README says outside scripting needs Studio [7]. Studio's page lists a remote scripting API [3]. Check the setting `Preferences > System > General > External scripting using` on your install [6][7]. TODO(research): confirm on Resolve 21.1.

**Free-tool limits.** Kdenlive's hardware-accelerated presets are marked experimental [11]. Resolve Free lacks the Studio-only tools, such as the AI Neural Engine features, noise reduction and film grain [2][3]. Shotcut's licence is not named on its download page [19]. TODO(research): confirm it.

**Hardware floors.** Blender 5 needs at least four cores, 8 GB of RAM, and a graphics card with 2 GB of video memory and OpenGL 4.3 or Vulkan 1.3 [30]. Shotcut asks for four cores and 8 GB for HD [20]. Keep originals on an external drive, never edit straight from a USB stick, and plug the laptop in with sleep turned off for overnight renders [100].

**Export and screens.**

- FAT32 cannot hold a file over 4 GB [96]. Format the stick as exFAT, or split the file (Step 12).
- Variable-frame-rate phone clips can drift against the timeline. Convert them to constant frame rate first. The research's command for this is untested [100].
- 4K needs HEVC, or H.264 at level 5.1, and must be tested on the real screen [95].
- TODO(research): no TV or projector format specification was readable. Test exFAT, MKV, soft subtitles and HDMI on the real hardware.

**Look-alikes and web tools.**

- A YouTube channel named "ShotCut Video Editor" is not the official Shotcut. Its listing shows AI-template adverts. Use the official site [21][98].
- Photopea runs in a browser. Its "nothing is uploaded" claim is the vendor's statement, not an audit [55].
- "AI photo animator" websites upload your photos to someone else's servers. That needs the consent of you and of everyone pictured [1].

**Music.** "Royalty-free" does not mean free to show in public, and it does not mean no credit. Read the licence page, not the search result. The YouTube Audio Library is safe only on YouTube [77]. Pixabay's licence needs no credit, but it does not allow selling or distributing the content alone [81]. FreePD closed in 2025 [84]. BBC Sound Effects' stated terms mention personal or educational projects, or a paid licence. A public screening is not confirmed [85]. Mixkit, Musopen, Zapsplat, Openverse and ccMixter were not read [86].

**Surprise leaks.** The charter forbids anything that could tip her off, including shared devices, cloud photo libraries and family group chats [1]. Do not let your project folder sync to a cloud photo library. Do not post a "render finished" message in a family chat. Use neutral file names on any shared machine.

## Best references (top 8)

1. **Blender 5.2 LTS Manual: Rendering From The Command Line.** https://docs.blender.org/manual/en/latest/advanced/command_line/render.html [26]. Read it before your first overnight render. It gives the order of the command-line flags, which matters.
2. **Kdenlive 26.08 Manual: Rendering.** https://docs.kdenlive.org/en/exporting/render.html [11]. Render presets and "Generate Script", which is how you queue overnight renders.
3. **Kdenlive Manual: Speech to Text.** https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html [13]. Captions with VOSK or Whisper, inside the editor.
4. **MLT: melt documentation.** https://www.mltframework.org/docs/melt/ [17]. What Kdenlive does underneath, and how to render a project with no window.
5. **FFmpeg Filters Documentation.** https://ffmpeg.org/ffmpeg-filters.html [63]. Read the `zoompan`, `xfade`, `subtitles` and `loudnorm` sections before Steps 4, 10 and 11.
6. **Inkscape Tutorials.** https://inkscape.org/learn/tutorials/ [36]. The official index, including the Interpolate, Tracing and Calligraphy tutorials.
7. **CSS-Tricks: How SVG Line Animation Works** (Chris Coyier, 2014). https://css-tricks.com/svg-line-animation-works/ [65]. Still the clearest plain explanation of the dash-offset trick. The date is old, but the method still holds.
8. **Library of Congress: Recommended Formats Statement, Moving Image Works.** https://www.loc.gov/preservation/resources/rfs/moving.html [92]. Which archive formats to keep, and why an MP4 is a viewing copy only.

**Video tutorials are thin.** The research could not verify any video for a Ken Burns move in an editor, 2.5D parallax in Blender, photo-to-voxel, SVG line-drawing, photo morphing or era grading [98][99]. The one video with a readable date and length is the Nuxttux "Keyframe Interpolation" tutorial, 5 minutes 34 seconds, uploaded 29 May 2025. The research read only its page details, not its content, so the title is all we know [99]. https://www.youtube.com/watch?v=F1h6Kg-WLDE. The Arkengheist rotoscoping video is from 2020 and shows an older Kdenlive, so use it for ideas only [99]. Blender Guru's 2026 beginner course runs over four hours, and its exact Blender version is unverified [98]. TODO(research): re-fetch the channel listings slowly, and open the shortlisted videos.

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

[56] MagicaVoxel — https://ephtracy.github.io/mv_main.html ; https://ephtracy.github.io/mv_renderer.html ; https://ephtracy.github.io/mv_commands.html — 0.99.7.2 [7/12/2025]; licence; renderer; export; console; FAQ.

[58] Goxel — https://goxel.xyz/ ; https://raw.githubusercontent.com/guillaumechereau/goxel/master/README.md ; https://raw.githubusercontent.com/guillaumechereau/goxel/master/src/main.c — README "Version 0.15.1", GPL-3, formats; CLI `--export`, `--script`.

[59] Blockbench — https://www.blockbench.net/ — low-poly/cuboid models, animation, plugins, web app, GPL.

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

[86] Mixkit — License — https://mixkit.co/license/ — per-item-type licences; terms not extractable.

[88] Suno — Terms of Service — https://suno.com/terms — (WebFetch) revised 2026-08-10, effective 2026-09-03.

[89] US Copyright Office — Copyright and Artificial Intelligence — https://www.copyright.gov/ai/ — (WebFetch) Part 2 (Copyrightability) published 2025-01-29.

[90] Meta AudioCraft README — https://raw.githubusercontent.com/facebookresearch/audiocraft/main/README.md — (WebFetch) code MIT; weights CC-BY-NC 4.0.

[91] YouTube Help — Recommended upload encoding settings — https://support.google.com/youtube/answer/1722171 — MP4, H.264 High, AAC-LC 48 kHz, bitrates, BT.709.

[92] Library of Congress — Recommended Formats Statement, Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — RFS 2025-2026; FFV1 v3/Matroska, ProRes/QuickTime, MP4 as viewing proxy.

[93] RFC 9043 — FFV1 Video Coding Format Versions 0, 1, and 3 — https://www.rfc-editor.org/rfc/rfc9043.html

[94] RFC 9559 — Matroska Media Container Format Specification — https://www.rfc-editor.org/rfc/rfc9559.html

[95] Wikipedia — Advanced Video Coding (levels table) — https://en.wikipedia.org/wiki/Advanced_Video_Coding — level 4.1 ≈ 1080p30; 4.2 ≈ 1080p64; 5.1 ≈ 4K31.7.

[96] Wikipedia — File Allocation Table — https://en.wikipedia.org/wiki/File_Allocation_Table — FAT32 max file 4 GB − 1.

[97] Wikipedia — EBU R 128 — https://en.wikipedia.org/wiki/EBU_R_128 — target −23 LUFS.

[98] YouTube channel listings read on 2026-10-18 (titles, lengths, relative ages only) — https://www.youtube.com/@BlenderGuru/videos ; https://www.youtube.com/@DefaultCube/videos ; https://www.youtube.com/@BlenderStudio/videos ; https://www.youtube.com/@grabbitt/videos ; https://www.youtube.com/@CaseyFaris/videos ; https://www.youtube.com/@nuxttux/videos ; https://www.youtube.com/@LogosByNick/videos ; https://www.youtube.com/@DaviesMediaDesign/videos ; https://www.youtube.com/@Audacity/videos ; https://www.youtube.com/@ShotcutVideoEditor/videos (look-alike, not official).

[99] YouTube video pages with readable metadata — https://www.youtube.com/watch?v=gcIKU4KxfLk (Arkengheist 2.0, Rotoscoping, 16:09, 2020-11-21) ; https://www.youtube.com/watch?v=F1h6Kg-WLDE (Nuxttux Creative Studio, Keyframe Interpolation, 5:34, 2025-05-29).

[100] Sandbox verification runs, 2026-10-18 — local, not a URL — ffmpeg 6.1.1, ImageMagick 6.9.12, Blender `bpy` 5.2.2 (Python 3.13), Inkscape 1.2.2, MLT melt 7.22.0, Synfig 1.5.1, Goxel 0.11.0 (Xvfb), librsvg 2.58.0, svgpathtools, Pillow; outputs inspected with `ffprobe` and by eye. Scripts reproduced in "Exemplars / recipes".

## Changelog

- v0.1 · 2026-10-18 · First draft, written by the Haiku scribe from research/toolchain.md and CHARTER.md. Not yet reviewed by the advisor or by the maker. The plan is provisional until the Step 0 checklist comes back.

### Open TODO(research) items at v0.1

- **Your apps and computer.** The Step 0 checklist has not come back. The charter says Windows [1]; the research assumed the OS was unknown. Confirm the OS, the installed apps and the hardware.
- **Resolve Free.** External scripting on 21.1, its hardware floor, Linux codec limits, whether captions and subtitle tracks work in Free, and which Photo-page tools are Free [2][3][6][7].
- **Headless claims not run.** GIMP 3 batch Python procedure name; Krita headless Python; Glaxnimate's pip package on your OS; Audacity 4 scripting pipe; OpenShot bindings and `.osp`; running a Shotcut-saved `.mlt` through `melt`; hand-writing a native `.kdenlive`; the Blender program itself (the research used the Python module); EEVEE with no graphics card; Goxel's `--script` option (read from source only); Synfig's ffmpeg target syntax [100].
- **Windows commands.** Which shell you will use; Blender's Python module on Windows; the `xvfb-run` step (needed only on servers); checksum commands; the burn-in font [100].
- **Cloud rendering.** No cloud render path was tested (Decision 5).
- **Tutorials.** Re-fetch channel listings slowly for Ken Burns, parallax, photo-to-voxel, SVG line-draw, photo morphing and era grading. Open the shortlisted videos [98][99].
- **Screen and format.** TV and projector format support: exFAT or FAT32, MKV, soft subtitles, HEVC 4K, 4:3 or 16:9 projectors, audio path, and venue HDMI and USB behaviour [95][96].
- **Licences not read.** Mixkit terms; Musopen; Zapsplat; Openverse; ccMixter and Free Music Archive per-track terms; BBC Sound Effects full terms; Pixabay's Content ID clause; the YouTube Audio Library licence outside YouTube; Udio, Stable Audio and Lyria terms in 2026; the US Copyright Office Part 2 conclusions [81][85][86][89]. Venue music licences and film synchronisation need a rights professional.
- **Voxel route.** Human modelling time per object; Blender-native voxel routes (Geometry Nodes, remesh); depth-map displacement and camera-projection parallax; the Goxel and MagicaVoxel results on your machine [56][58].
- **Hardware floors.** Kdenlive, Inkscape and Resolve Free minimums were not found [8][32].
- **ArtCraft.** Not covered by this track. See the craft-visual and craft-motion tracks [1].
- **Time estimates.** Per-exercise times were not measured. Exercise 8 may take longer than two hours [100].
- **Search budget.** The shared search budget was used up before the research began. Better tutorials and tools may exist [100].
