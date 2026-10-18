---
name: free-creative-toolchain
description: Chooses, scripts, checks and exports the free desktop toolchain for Life Journey shots (Blender 5.2 LTS for parallax, voxel and line-draw renders; Inkscape for SVG; Kdenlive or Resolve Free for assembly; ffmpeg and ImageMagick as glue). Use it when a shot needs a Ken Burns or parallax move, an SVG line reveal, a voxel object, an era grade, loudness, captions, or screening and archive exports, or when someone asks which free tool or command to use. Do not use it to choose story content, give licence legal advice, or handle the ArtCraft apps.
---

# Free Creative Toolchain

## Purpose

Turn the toolchain research into repeatable, checked production steps, using free tools and scripts that an AI agent can run and repair. The human version is `playbooks/toolchain.md`. The research notes are `research/toolchain.md`, which explain each technique. The runnable recipes are in `.claude/skills/free-creative-toolchain/recipes/`: `r1_kenburns.sh`, `r2_parallax.py`, `r2_param.py`, `r3_linedraw.py`, `r4_photo2vox.py`, `r4_render_voxel.py`, `r5_story.mlt`, `r7_era_looks.txt`, `r8_vse_xfade.py` and `r9_deliver.sh`. Each file's header names the tool versions and the date it ran. Charter principles 1, 4, 5 and 7 apply [1].

## When to use

- A shot needs a Ken Burns push or pan, or layered parallax from a photo.
- A route, map, timeline or title must draw itself (an SVG line reveal).
- A voxel or Minecraft-style object must be modelled, converted or rendered.
- An album's look, loudness, captions, or screening or archive files are needed.
- Someone asks which free tool or command to do one of these jobs.

## When not to use

- Deciding what a scene says, or whether a memory belongs in the film. That is the story track.
- Restoring or inventing imagery with generative AI. That is the ai-imagery track. This skill only sets the rules that work must respect.
- Licence questions. Quote the licence text and list the open question for the maker. Do not give legal advice.
- The ArtCraft apps (PhotoCraft, VectorCraft, FilmCraft and others). Use the craft-visual and craft-motion tracks [1].
- Game mechanics. Use the meaningful-game-mechanics skill.

## Procedure

Route by request first:

| Request | Steps |
|---|---|
| New shot: Ken Burns, parallax, line reveal, voxel object, album look | 5 to 12 |
| Captions | 14 |
| Export or stick test | 15 to 16 |
| Archive | 17 |
| "Which tool?" | Checklist A |

### Once per project (steps 1 to 4)

1. **Check the app inventory.** Read the maker's latest "Recognise your apps" result. If there is none, write `TODO(research): app inventory` in the shot notes, work only on stock or synthetic images, and do not fix a tool choice. The charter records a Windows PC; confirm it [1].
2. **Pin versions.** Use Blender 5.2 LTS for the whole build [24]. Record every tool's version in the project README: ffmpeg, ImageMagick, melt, Blender, the editor, Inkscape.
3. **Probe before running remembered code.** Before any Blender, Inkscape or editor call written from memory, list what exists first. For example, `dir(bpy.context.scene.sequence_editor_create())` on a throwaway scene (`bpy.context.scene.sequence_editor` is `None` on a fresh scene), or `[s for s in dir(bpy.context.scene) if 'seq' in s]`, or read the program's help. Use the names the probe returns [100].
4. **Confirm the shell (playbook Decision 0).** Recipes are Unix-style and were tested only on Ubuntu [100]. The lean is native PowerShell with the Windows-native programs. Use Git Bash only if it is already installed, and WSL2 only with 16 GB of RAM or more (research Follow-up F3). On the maker's machine, run a one-line echo test, record the shell in the README, and mark any untested Windows command `TODO(verify on the maker's PC)`. The playbook gives PowerShell forms of the four bash self-checks, in Exercises 1, 2, 6 and 10, each marked the same way.

### Per shot (steps 5 to 12)

5. **Prepare the still.** Practise on stock or synthetic images. Real photos enter only after the pipeline is locked and the maker agrees [1]. Crop to 16:9 in an ImageMagick batch [64][100]. Never overwrite originals.
6. **Choose the move route.**
   - One still, one move: ffmpeg `zoompan`, `recipes/r1_kenburns.sh` [63].
   - Layered parallax for hero shots: Blender planes, `recipes/r2_parallax.py`, with view transform Standard [100].
   - Layered parallax for simple shots: editor keyframes on separate tracks, with near layers moving further.
7. **Cut layers.** Cut by hand in GIMP 3.2 or Krita [46][51], or assisted with `rembg` [73] or SAM 2 [74]. For depth, use Depth Anything V2 Small only (Apache-2.0). Base and Large are CC-BY-NC-4.0 and need the maker's approval [72]. Log every filled background as a reconstruction [1].
8. **Put the script in the repo.** Copy the tested recipe verbatim first, then change parameters. Keep the exact command lines in the repo, not only in chat. Every output of this track is a PNG sequence with alpha, an MP4, an SRT or a plain SVG, so either layer can take it; exact import formats belong to craft-visual/craft-motion. FilmCraft 0.9.0 does not import plain SVG, so rasterise to PNG with alpha first (`recipes/r3_linedraw.py`) (research Follow-up F5).
9. **Draft, then final.** Draft at 640×360 or 960×540 with few samples. Render PNG sequences, not one long video, so a crash costs one frame [100]. Measure with `recipes/r2_param.py` before the first final render. Run finals from the command line overnight [25][26].
10. **Line reveals.** Draw one centre-line stroked path per reveal in Inkscape [35]. Run `recipes/r3_linedraw.py`, which computes the real path length. Do not rely on `pathLength="1"`, which the tested renderer ignored [66][100]. Use single-line fonts for titles. The PowerShell frame loop is in playbook Exercise 6.
11. **Assemble.** Pass the profile explicitly to `melt`, `-profile atsc_1080p_25`, because the default is 720×576 [17][100]. Crop 3:2 photos first. Do the final cut by hand in Kdenlive [8][11].
12. **Grade by album.** Derive one look per album from three of her prints. In each print, sample a known-white object and a skin midtone. Derive the lift, cast and grain from those samples, and save the look in `looks/`, named after her chapter. Apply that same string to every photo from the album [63][100]. The stock era chains in `recipes/r7_era_looks.txt` are practice material, not for the film. The derivation method is written and tested on three stock prints (research Follow-up F14; `research/toolchain-fixtures/derive_album_look.py`). It stays TODO(research) until it has run on her prints and on Windows Python.

### Per delivery (steps 13 to 18)

13. **Sound.** Voice first, then the ducked music bed, then effects. Use only sources that pass Checklist C. Set loudness with `loudnorm=I=-16:TP=-1.5:LRA=11`, then test in the room. The broadcast reference is −23 LUFS [63][97][100].
14. **Captions.** Draft with Kdenlive's speech-to-text [13] or local Whisper [75]. Kdenlive's Whisper needs Python 3 installed first and downloads about 2 GB plus a model on first use, so set it up while online; transcription runs offline after that. On an 8 GB PC use `tiny`, `base` or `small` (`small` peaks at about 2.1 GiB and is the default). `medium` and `turbo` (about 5.1 to 5.4 GiB) only fit with other apps closed, and `large` does not fit. Check where the first `.pt` lands: the script reads `~\.cache\whisper`, and the manual names `%AppData%\kdenlive\opencvmodels` [116][117][118]. Test on one old phone recording or an older voice, not only a clean clip. The human proofreads every name and place. Resolve Free imports SRT and burns it in; automatic subtitles are Studio [110][111][112]. Mark the Windows run `TODO(verify on the maker's PC)`. Burn in captions for the screening file and always keep a sidecar `.srt` [12][13].
15. **Export three profiles from one master.** Screening MP4: H.264 High, level 4.1, yuv420p, 1080p, AAC-LC 48 kHz stereo, `+faststart`, BT.709 tags. Web MP4: CRF 20 with a 12 Mbps cap. Archive: ProRes 422 HQ in `.mov`, and/or FFV1 v3 in `.mkv` with FLAC [91][92][93][94][100]. Use `recipes/r9_deliver.sh` [100].
16. **Verify.** Run ffprobe on every output and compare it with the profile. Check file size against the stick's format; FAT32 caps a file at 4 GB minus one byte [96]. Play the screening file from a USB stick on the venue or test screen before calling it done.
17. **Archive.** Keep masters, SRT/VTT, project files, originals, source SVG and Blender files, a README with versions, the licence and credits file, and SHA-256 checksums. Keep two physical copies and one off-site [92][100].
18. **Report back.** List every `TODO(research)` the step touched, the tool versions used, and the exact command lines run.

## Checklists

### A. App and machine inventory (blocks the plan)

- OS and version; CPU; RAM; graphics card and video memory; free disk; pen tablet.
- Resolve edition (Free or Studio), version, and whether the External scripting setting is present. The 21 and 21.1 manuals make it Studio-only [110][111][112]; older notes [6][7] read the other way.
- Versions of Kdenlive, Shotcut, OpenShot, Inkscape, GIMP, Krita, Blender, MagicaVoxel, Goxel, Blockbench, Audacity.
- `ffmpeg -version` and `magick -version` output.
- Platform rules: MagicaVoxel runs on Windows and macOS only [56]; Blender 5 on macOS needs Apple Silicon [30].

### B. Before any render

- Input is at least 1.5 times the output width; the crop matches the output shape before any zoom [100].
- View transform is Standard [100].
- A short draft run passed; time per frame is written down.
- Output is a PNG sequence with a fixed frame count and frame rate.
- Line length is read from the file, not typed in.
- Voxel models imported with forward axis Y and up axis Z [100].

### C. Music and sound licences

- Allowed: CC0 (Freesound CC0 [80]; Kenney game assets [83], audio packs not checked); Sonniss bundles, which need no credit and forbid AI training [82]; CC BY with credit (incompetech [76]; Freesound CC BY [80]); the maker's own recording.
- Not allowed for a film that may travel: CC BY-NC [78][80].
- Not allowed: YouTube Audio Library outside YouTube [77]; FreePD, which has closed [84].
- Save each licence page to `licences/` with the date. Put the credit text in `credits.txt`, worded as the licence requires.
- AI music: Suno paid-tier downloads only, after the maker's decision; never free tier for the premiere [88][121]. MusicGen weights are non-commercial [90].
- Unread sources (Musopen, Zapsplat, Openverse, ccMixter, Free Music Archive, BBC Sound Effects [85]): mark `TODO(research)` and do not use. Zapsplat and Musopen refused our requests with HTTP 403 [141].
- Mixkit: sound effects are allowed in a film [119]. Music is for the private link only, unless Mixkit confirms in writing for a venue [119].
- Pixabay: allowed for a film; keep the download record; avoid shield-icon (Content ID) tracks for the online copy [120].
- Her favourite commercial songs: never in a shared cut. Use a substitute or the maker's own performance. The premiere is a mostly public gathering, so a rights professional reviews the final music list before the master is locked.

### D. Export and archive

- Every ffprobe result matches the profile table.
- FAT32 stick: each file under 4 GB, or the stick is exFAT and a screen test has passed [96].
- Loudness measured against the chosen target, not assumed.
- Captions in sync at three spot checks; names and places proofread.
- Archive holds masters, caption files, project files, originals, a versioned README, licences, and SHA-256 checksums.

### E. Privacy

- Scripts travel, photos don't. Agents build and test each script in the cloud on stock or synthetic images. The identical script runs on the maker's PC against the real photos, from a terminal with the Claude desktop app closed. Cloud rendering of real photos happens only after the maker's explicit decision for a named batch, never for the raw scans [1][100].
- Working files stay in the private repo or on an encrypted local drive.
- Nothing is uploaded to a web tool, cloud render or AI service without the maker's explicit say [1].
- The project folder does not sync to a cloud photo library. No render notification goes into a family group chat. Use neutral file names on shared machines [1].
- Web editors such as Photopea are not used for family photos [55].

## Quality bar

**Good.**
- A colour patch in the render matches its source photo; the view transform has not desaturated it.
- A round object stays round through a zoom.
- A line reveal starts, finishes and eases, and its last frame matches the static SVG.
- Each album has one saved look, named after its chapter, and applying it twice gives identical output.
- Loudness is measured, captions are proofread, and credits match their licences.
- Every export passes ffprobe and plays from the screening medium.
- Every reconstruction is labelled, and the originals are untouched.

**Mediocre (fix before review).**
- A 3:2 photo zoomed without cropping, so it stretches [100].
- A voxel model lying flat or sideways because the axes were not converted [100].
- Parallax where only one layer moves, or every layer moves the same distance.
- A look built by eye and not saved, so it cannot be repeated.
- A file over 4 GB on FAT32, or a screen that was never tested.
- Captions taken from the tool without proofreading.
- A track whose licence was never read.

**Stop and escalate.**
- Any real photo sent to a web tool or uploaded without the maker's say-so.
- A synthetic voice or "performance" of a real person, living or dead [1].
- A reconstruction presented as real footage.
- Any step that would require asking the subject, or that would surface the project on a device, library or chat she can see.

## Ethics guardrails

- Real memories stay real. Keep originals untouched, log every step that changes pixels, and label reconstructions visibly [1].
- Inpainting, colourising, upscaling and voxelising change or invent pixels. Treat each output as a reconstruction.
- No invented events, faces or voices [1].
- Consent: every living person shown, other than the subject, agrees before the cut uses them. The subject cannot be asked (the piece is a surprise); her trusted proxy decides for her, and chapters on loss, illness, separation, money or conflict go to the proxy before any shot is built [1].
- Credit music wherever the licence requires it. Disclose any AI-made music.
- Surprise: nothing syncs to a shared device or a cloud photo library [1].

## References

- Playbook: `playbooks/toolchain.md`
- Research notes (technique explanations, Follow-up research, TODO list): `research/toolchain.md`
- Runnable recipes: `.claude/skills/free-creative-toolchain/recipes/`
- Charter: `CHARTER.md`
- Full source list (69 entries, with the numbers used above): `.claude/skills/free-creative-toolchain/references.md`
- Key URLs:
  - Blender render from the command line: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html [26]
  - FFmpeg filters: https://ffmpeg.org/ffmpeg-filters.html [63]
  - MLT melt: https://www.mltframework.org/docs/melt/ [17]
  - Kdenlive rendering: https://docs.kdenlive.org/en/exporting/render.html [11]
  - Inkscape tutorials: https://inkscape.org/learn/tutorials/ [36]
  - ImageMagick command-line processing: https://imagemagick.org/command-line-processing/ [64]
  - Library of Congress formats (current statement, undated on the page; read 2026-10-18): https://www.loc.gov/preservation/resources/rfs/moving.html [92]
  - YouTube upload settings: https://support.google.com/youtube/answer/1722171 [91]
