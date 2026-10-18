---
name: free-creative-toolchain
description: Chooses, scripts, checks and exports the free desktop toolchain for Life Journey shots (Blender 5.2 LTS for parallax, voxel and line-draw renders; Inkscape for SVG; Kdenlive or Resolve Free for assembly; ffmpeg and ImageMagick as glue). Use it when a shot needs a Ken Burns or parallax move, an SVG line reveal, a voxel object, an era grade, loudness, captions, or screening and archive exports, or when someone asks which free tool or command to use. Do not use it to choose story content, give licence legal advice, or handle the ArtCraft apps.
---

# Free Creative Toolchain

## Purpose

Turn the toolchain research into repeatable, checked production steps, using free tools and scripts that an AI agent can run and repair. The human version is `playbooks/toolchain.md`. The research notes are `research/toolchain.md`, which hold the tested recipes R1 to R9. Charter principles 1, 4, 5 and 7 apply [1].

## When to use

- A shot needs a Ken Burns push or pan, or layered parallax from a photo.
- A route, map, timeline or title must draw itself (an SVG line reveal).
- A voxel or Minecraft-style object must be modelled, converted or rendered.
- A decade's look, loudness, captions, or screening or archive files are needed.
- Someone asks which free tool or command to do one of these jobs.

## When not to use

- Deciding what a scene says, or whether a memory belongs in the film. That is the story track.
- Restoring or inventing imagery with generative AI. That is the ai-imagery track. This skill only sets the rules that work must respect.
- Licence questions. Quote the licence text and list the open question for the maker. Do not give legal advice.
- The ArtCraft apps (PhotoCraft, VectorCraft, FilmCraft and others). Use the craft-visual and craft-motion tracks [1].
- Game mechanics. Use the meaningful-game-mechanics skill.

## Procedure

1. **Check the app inventory.** Read the maker's latest "Recognise your apps" result. If there is none, write `TODO(research): app inventory` in the shot notes, work only on stock or synthetic images, and do not fix a tool choice. The charter records a Windows PC; confirm it [1].
2. **Pin versions.** Use Blender 5.2 LTS for the whole build [24]. Record every tool's version in the project README: ffmpeg, ImageMagick, melt, Blender, the editor, Inkscape.
3. **Probe before running remembered code.** Before any Blender, Inkscape or editor call written from memory, list what exists first, for example `dir(bpy.context.scene.sequence_editor)`, or read the program's help. Use the names the probe returns [100].
4. **Confirm the shell.** Recipes are Unix-style and were tested only on Ubuntu [100]. On the maker's machine, run a one-line echo test, record the shell in the README, and mark any untested Windows command `TODO(research)`.
5. **Prepare the still.** Practise on stock or synthetic images. Real photos enter only after the pipeline is locked and the maker agrees [1]. Crop to 16:9 in an ImageMagick batch [64][100]. Never overwrite originals.
6. **Choose the move route.**
   - One still, one move: ffmpeg `zoompan`, recipe R1 [63].
   - Layered parallax for hero shots: Blender planes, recipe R2, with view transform Standard [100].
   - Layered parallax for simple shots: editor keyframes on separate tracks, with near layers moving further.
7. **Cut layers.** Cut by hand in GIMP 3.2 or Krita [46][51], or assisted with `rembg` [73] or SAM 2 [74]. For depth, use Depth Anything V2 Small only (Apache-2.0). Base and Large are CC-BY-NC-4.0 and need the maker's approval [72]. Log every filled background as a reconstruction [1].
8. **Put the script in the repo.** Copy the tested recipe verbatim first, then change parameters. Keep the exact command lines in the repo, not only in chat.
9. **Draft, then final.** Draft at 640×360 or 960×540 with few samples. Render PNG sequences, not one long video, so a crash costs one frame [100]. Run finals from the command line overnight [25][26].
10. **Line reveals.** Draw one centre-line stroked path per reveal in Inkscape [35]. Run recipe R3, which computes the real path length. Do not rely on `pathLength="1"`, which the tested renderer ignored [66][100]. Use single-line fonts for titles.
11. **Assemble.** Pass the profile explicitly to `melt`, `-profile atsc_1080p_25`, because the default is 720×576 [17][100]. Crop 3:2 photos first. Do the final cut by hand in Kdenlive [8][11].
12. **Grade by era.** Save each decade's ffmpeg filter string in `looks/`, as recipe R7 does, and apply the same string to every clip from that decade [63][100].
13. **Sound.** Voice first, then the ducked music bed, then effects. Use only sources that pass Checklist C. Set loudness with `loudnorm=I=-16:TP=-1.5:LRA=11`, then test in the room. The broadcast reference is −23 LUFS [63][97][100].
14. **Captions.** Draft with Kdenlive's speech-to-text [13] or local Whisper [75]. The human proofreads every name and place. Burn in captions for the screening file and always keep a sidecar `.srt` [12][13].
15. **Export three profiles from one master.** Screening MP4: H.264 High, level 4.1, yuv420p, 1080p, AAC-LC 48 kHz stereo, `+faststart`, BT.709 tags. Web MP4: CRF 20 with a 12 Mbps cap. Archive: ProRes 422 HQ in `.mov`, and/or FFV1 v3 in `.mkv` with FLAC [91][92][93][94][100]. Use the R9 commands [100].
16. **Verify.** Run ffprobe on every output and compare it with the profile. Check file size against the stick's format; FAT32 caps a file at 4 GB minus one byte [96]. Play the screening file from a USB stick on the venue or test screen before calling it done.
17. **Archive.** Keep masters, SRT/VTT, project files, originals, source SVG and Blender files, a README with versions, the licence and credits file, and SHA-256 checksums. Keep two physical copies and one off-site [92][100].
18. **Report back.** List every `TODO(research)` the step touched, the tool versions used, and the exact command lines run.

## Checklists

### A. App and machine inventory (blocks the plan)

- OS and version; CPU; RAM; graphics card and video memory; free disk; pen tablet.
- Resolve edition (Free or Studio), version, and the External scripting setting [6][7].
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
- AI music: do not use until the maker has read the tier terms [88][90] and decided on public use.
- Unread sources (Mixkit [86], Musopen, Zapsplat, Openverse, ccMixter, Free Music Archive, BBC Sound Effects [85], Pixabay's Content ID clause [81]): mark `TODO(research)` and do not use.
- Her favourite commercial songs: never in a shared cut. Use a substitute or the maker's own performance. Get a rights professional's view if the film will be shown beyond family.

### D. Export and archive

- Every ffprobe result matches the profile table.
- FAT32 stick: each file under 4 GB, or the stick is exFAT and a screen test has passed [96].
- Loudness measured against the chosen target, not assumed.
- Captions in sync at three spot checks; names and places proofread.
- Archive holds masters, caption files, project files, originals, a versioned README, licences, and SHA-256 checksums.

### E. Privacy

- Working files stay in the private repo or on an encrypted local drive.
- Nothing is uploaded to a web tool, cloud render or AI service without the maker's explicit say [1].
- The project folder does not sync to a cloud photo library. No render notification goes into a family group chat. Use neutral file names on shared machines [1].
- Web editors such as Photopea are not used for family photos [55].

## Quality bar

**Good.**
- A colour patch in the render matches its source photo; the view transform has not desaturated it.
- A round object stays round through a zoom.
- A line reveal starts, finishes and eases, and its last frame matches the static SVG.
- Each decade has one saved string, and applying it twice gives identical output.
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

## Ethics guardrails

- Real memories stay real. Keep originals untouched, log every step that changes pixels, and label reconstructions visibly [1].
- Inpainting, colourising, upscaling and voxelising change or invent pixels. Treat each output as a reconstruction.
- No invented events, faces or voices [1][90].
- Consent: each living person shown agrees before the cut uses them. Chapters on loss, illness, money or conflict go to the proxy process first [1].
- Credit music wherever the licence requires it. Disclose any AI-made music.
- Surprise: nothing syncs to a shared device or a cloud photo library [1].

## References

- Playbook: `playbooks/toolchain.md`
- Research notes, with recipes R1 to R9 and the TODO list: `research/toolchain.md`
- Charter: `CHARTER.md`
- Key URLs: Blender render from the command line https://docs.blender.org/manual/en/latest/advanced/command_line/render.html [26]; FFmpeg filters https://ffmpeg.org/ffmpeg-filters.html [63]; MLT melt https://www.mltframework.org/docs/melt/ [17]; Kdenlive rendering https://docs.kdenlive.org/en/exporting/render.html [11]; Inkscape tutorials https://inkscape.org/learn/tutorials/ [36]; Library of Congress formats https://www.loc.gov/preservation/resources/rfs/moving.html [92]; YouTube upload settings https://support.google.com/youtube/answer/1722171 [91].

### Sources cited in this skill

- [1] Project charter — CHARTER.md — undated (local file) — principles incl. "prefer scriptable tools", real memories stay real, dignity and consent.
- [6] DaVinci Resolve Scripting README (mirror of Blackmagic's README.txt by X-Raym) — https://gist.githubusercontent.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8/raw — "Last Updated: 24 Jul 2026" — Console/Scripts menu, `-nogui`, API superset for Free and Studio, `ImportTimelineFromFile` formats, render functions.
- [7] pydavinci README — https://raw.githubusercontent.com/pedrolabonia/pydavinci/main/README.md — undated, Resolve 18 era, third party — "External scripting … requires Resolve Studio (Free version does not allow API access)".
- [8] Kdenlive — Downloads — https://kdenlive.org/download/ — 26.08.2; Windows 10+, macOS 13+, AppImage/Flatpak.
- [11] Kdenlive manual — Rendering — https://docs.kdenlive.org/en/exporting/render.html — manual 26.08 — presets (ProRes, FFV1, H.264, H.265, AV1), Generate Script, `melt script.mlt`, proxies, experimental hardware presets.
- [12] Kdenlive manual — What's New — https://docs.kdenlive.org/en/more_information/whats_new.html — keyframe easing modes, curve editor, subtitles, mask effects, proxies in preview.
- [13] Kdenlive manual — Speech to Text — https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html — VOSK and Whisper subtitles.
- [17] MLT — melt documentation — https://www.mltframework.org/docs/melt/ — (WebFetch) producers, filters, consumers, `xml` consumer.
- [24] Blender — Releases — https://www.blender.org/download/releases/ — (WebFetch) 5.2 LTS 2026-07-14; 5.1 2026-03-17; 5.0 2025-11-18; 4.5 LTS 2025-07-15.
- [25] Blender 5.2 LTS Manual — Command Line Arguments — https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html — `-b`, `-P/--python`, `--python-exit-code`, `-E`, `--factory-startup`.
- [26] Blender 5.2 LTS Manual — Rendering From The Command Line — https://docs.blender.org/manual/en/latest/advanced/command_line/render.html — page "Last updated on 2026-10-17"; argument order; `-f`, `-a`, `-o`, `-F`.
- [30] Blender — System Requirements — https://www.blender.org/download/requirements/ — minimum/recommended; Apple Silicon only from 5.0; pen tablets recommended for Grease Pencil.
- [35] Inkscape — Learn: Animation — https://inkscape.org/learn/animation/ — "Inkscape does not support animation natively".
- [36] Inkscape — Tutorials index and Interpolate tutorial — https://inkscape.org/learn/tutorials/ ; https://inkscape.org/doc/tutorials/interpolate/tutorial-interpolate.html — official tutorials (Basic, Shapes, Advanced, Tracing, Calligraphy, Interpolate…).
- [46] GIMP — Downloads — https://www.gimp.org/downloads/ — 3.2.6 (2026-09-10); macOS 11+; AppImage needs Debian 13+.
- [51] Krita — Download — https://krita.org/en/download/ — 5.3.4.1 released 2026-10-07; system requirements.
- [55] Photopea — Learn: Introduction — https://www.photopea.com/learn/ — vendor statement on local processing.
- [56] MagicaVoxel — https://ephtracy.github.io/mv_main.html ; https://ephtracy.github.io/mv_renderer.html ; https://ephtracy.github.io/mv_commands.html — 0.99.7.2 [7/12/2025]; licence; renderer; export; console; FAQ.
- [63] FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html — zoompan, xfade, subtitles, lut3d, colorbalance, curves, loudnorm.
- [64] ImageMagick — Download; Command-line Processing — https://imagemagick.org/download/ ; https://imagemagick.org/command-line-processing/ — 7.1.2-34 AppImage; `magick`.
- [66] MDN — stroke-dashoffset — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/stroke-dashoffset — resolved against `pathLength`.
- [72] Depth Anything V2 README — https://raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md — Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0.
- [73] rembg README — https://raw.githubusercontent.com/danielgatis/rembg/main/README.md — MIT; CLI `rembg i`.
- [74] SAM 2 README — https://raw.githubusercontent.com/facebookresearch/sam2/main/README.md — Apache-2.0 model and code.
- [75] Whisper README; whisper.cpp README — https://raw.githubusercontent.com/openai/whisper/main/README.md ; https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/README.md — MIT; `whisper audio.flac --model turbo`.
- [76] incompetech — Music FAQ — https://incompetech.com/music/royalty-free/faq.html — CC BY 4.0; credit format; live productions allowed.
- [77] YouTube Help — Use music and sound effects from the Audio Library — https://support.google.com/youtube/answer/3376882 — attribution; Content-ID-safe; no off-platform legal guidance.
- [78] Creative Commons — FAQ — https://creativecommons.org/faq/ — meaning of NonCommercial.
- [80] Freesound — FAQ — https://freesound.org/help/faq/ — (WebFetch) CC0, CC BY, CC BY-NC; attribution wording.
- [81] Pixabay — Content License summary — https://pixabay.com/service/license-summary/ — (WebFetch) no attribution; no standalone redistribution.
- [82] Sonniss — GDC Game Audio Bundles — https://sonniss.com/gameaudiogdc/ — (WebFetch) royalty-free, no attribution, no AI training; GDC 2024 latest on that page.
- [83] Kenney — Support (licence FAQ) — https://kenney.nl/support — CC0.
- [84] FreePD — https://freepd.com/ — closure notice (2008–2025).
- [85] BBC Sound Effects — https://sound-effects.bbcrewind.co.uk/licensing — "personal/educational projects, or licence them for use".
- [86] Mixkit — License — https://mixkit.co/license/ — per-item-type licences; terms not extractable.
- [88] Suno — Terms of Service — https://suno.com/terms — (WebFetch) revised 2026-08-10, effective 2026-09-03.
- [90] Meta AudioCraft README — https://raw.githubusercontent.com/facebookresearch/audiocraft/main/README.md — (WebFetch) code MIT; weights CC-BY-NC 4.0.
- [91] YouTube Help — Recommended upload encoding settings — https://support.google.com/youtube/answer/1722171 — MP4, H.264 High, AAC-LC 48 kHz, bitrates, BT.709.
- [92] Library of Congress — Recommended Formats Statement, Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — RFS 2025-2026; FFV1 v3/Matroska, ProRes/QuickTime, MP4 as viewing proxy.
- [93] RFC 9043 — FFV1 Video Coding Format Versions 0, 1, and 3 — https://www.rfc-editor.org/rfc/rfc9043.html
- [94] RFC 9559 — Matroska Media Container Format Specification — https://www.rfc-editor.org/rfc/rfc9559.html
- [96] Wikipedia — File Allocation Table — https://en.wikipedia.org/wiki/File_Allocation_Table — FAT32 max file 4 GB − 1.
- [97] Wikipedia — EBU R 128 — https://en.wikipedia.org/wiki/EBU_R_128 — target −23 LUFS.
- [100] Sandbox verification runs, 2026-10-18 — local, not a URL — ffmpeg 6.1.1, ImageMagick 6.9.12, Blender `bpy` 5.2.2 (Python 3.13), Inkscape 1.2.2, MLT melt 7.22.0, Synfig 1.5.1, Goxel 0.11.0 (Xvfb), librsvg 2.58.0, svgpathtools, Pillow; outputs inspected with `ffprobe` and by eye. Scripts reproduced in "Exemplars / recipes".

