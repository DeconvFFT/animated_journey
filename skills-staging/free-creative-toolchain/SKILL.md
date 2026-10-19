---
name: free-creative-toolchain
description: Chooses, scripts, checks and exports the free desktop toolchain for Life Journey shots (Blender 5.2 LTS for parallax and hero-shot renders; Inkscape for SVG and line-draw; Kdenlive or Resolve Free for assembly; ffmpeg and ImageMagick as glue). Use it when a shot needs a Ken Burns or parallax move, an SVG line reveal such as a floor-art line-draw card, an era grade, loudness, captions, or phone-file, screening and archive exports, or when someone asks which free tool or command to use. Do not use it to choose story content, give licence legal advice, or handle the ArtCraft apps.
---

# Free Creative Toolchain

## Purpose

Turn the toolchain research into repeatable, checked production steps, using free tools and scripts that an AI agent can run and repair. The human version is `playbooks/toolchain.md`. The research notes are `research/toolchain.md`, which explain each technique. The runnable recipes are in `.claude/skills/free-creative-toolchain/recipes/`: `r1_kenburns.sh`, `r2_parallax.py`, `r2_param.py`, `r3_linedraw.py`, `r5_story.mlt`, `r7_era_looks.txt`, `r8_vse_xfade.py` and `r9_deliver.sh` (the two `r4_*` recipes are retired under D-29, S-46, and the orchestrator removes them from the skill folder). Each file's header names the tool versions and the date it ran. Charter principles 1, 4, 5 and 7 apply [1]. The decisions register `DECISIONS.md` wins where this skill disagrees (D-21).

**Reconciled with DECISIONS.md (2026-10-18, and again 2026-10-19 after the her-world merge).** The look comes from her Hindu world (D-28, D-31, W-72) and there is no game-world chapter (D-29). Frame rate is 24 fps (W-14): the recipes still carry the 25 fps values they were tested at (`r1_kenburns.sh`, `r2_parallax.py`, `r5_story.mlt` with `atsc_1080p_25`), so treat every 24 fps value in this skill as UNVERIFIED until those recipes and the colour-patch test are re-run at 24 and the files are patched by hand. Loudness is -1 dBTP everywhere (W-19). Real photos enter after the P-LOCK process lock, Sat 14 Nov 2026; covert collection starts Sun 15 Nov (D-13). The repo is public (D-26): text, scripts and ID-keyed manifests only. Only-me (D-03): the maker is the proxy and nobody else is asked or told before the premiere.

## When to use

- A shot needs a Ken Burns push or pan, or layered parallax from a photo.
- A route, map, timeline or title must draw itself (an SVG line reveal).
- A floor-art line-draw card must be drawn and revealed at the phone floor (W-72).
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
| New shot: Ken Burns, parallax, line reveal, floor-art card, album look | 5 to 12 |
| Captions | 14 |
| Export or stick test | 15 to 16 |
| Archive | 17 |
| "Which tool?" | Checklist A |

### Once per project (steps 1 to 4)

1. **Check the app inventory.** Read the maker's latest "Recognise your apps" result. If there is none, write `TODO(research): app inventory` in the shot notes, work only on stock or synthetic images, and do not fix a tool choice. The maker has decided on a Windows PC (D-10); its numbers stay UNVERIFIED until `windows_check_report.json` is in the repo (W-28) [1].
2. **Pin versions.** Use Blender 5.2 LTS for the whole build [24]. Record every tool's version in the project README: ffmpeg, ImageMagick, melt, Blender, the editor, Inkscape.
3. **Probe before running remembered code.** Before any Blender, Inkscape or editor call written from memory, list what exists first. For example, `dir(bpy.context.scene.sequence_editor_create())` on a throwaway scene (`bpy.context.scene.sequence_editor` is `None` on a fresh scene), or `[s for s in dir(bpy.context.scene) if 'seq' in s]`, or read the program's help. Use the names the probe returns [100].
4. **Confirm the shell (playbook Decision 0).** Recipes are Unix-style and were tested only on Ubuntu [100]. The lean is native PowerShell with the Windows-native programs. Use Git Bash only if it is already installed, and WSL2 only with 16 GB of RAM or more (research Follow-up F3). On the maker's machine, run a one-line echo test, record the shell in the README, and mark any untested Windows command `TODO(verify on the maker's PC)`. The playbook gives PowerShell forms of the four bash self-checks, in Exercises 1, 2, 6 and 10, each marked the same way.

### Per shot (steps 5 to 12)

5. **Prepare the still.** Practise on stock or synthetic images. Real photos enter only after the P-LOCK process lock (Sat 14 Nov 2026), and covert collection starts Sun 15 Nov (D-13, W-10); the maker agrees each set and the `cloud` level stays `none` unless the maker raises it (W-24) [1]. Crop to 16:9 in an ImageMagick batch [64][100]. Never overwrite originals.
6. **Choose the move route.**
   - One still, one move: ffmpeg `zoompan`, `recipes/r1_kenburns.sh` [63]. `zoompan` is for proofs only (W-41): a delivered move is rendered by the sub-pixel route and must pass MO8a at or below 0.05 px and MO8b at or below 0.04 px on the pre-encode master (`mo8_audit.py`, `playbooks/cinematic-quality.md`).
   - Layered parallax for hero shots: Blender planes, `recipes/r2_parallax.py`, with view transform Standard [100].
   - Layered parallax for simple shots: editor keyframes on separate tracks, with near layers moving further.
7. **Cut layers.** Cut by hand in GIMP 3.2 or Krita [46][51], or assisted with `rembg` [73] or SAM 2 [74]. For depth, use Depth Anything V2 Small only (Apache-2.0). Base and Large are CC-BY-NC-4.0 and need the maker's approval [72]. Log every filled background as a reconstruction [1].
8. **Put the script in the repo.** Copy the tested recipe verbatim first, then change parameters. Keep the exact command lines in the repo, not only in chat. Every output of this track is a PNG sequence with alpha, an MP4, an SRT or a plain SVG, so either layer can take it; exact import formats belong to craft-visual/craft-motion. FilmCraft 0.9.0 does not import plain SVG, so rasterise to PNG with alpha first (`recipes/r3_linedraw.py`) (research Follow-up F5).
9. **Draft, then final.** Draft at 640×360 or 960×540 with few samples. Render PNG sequences, not one long video, so a crash costs one frame [100]. Measure with `recipes/r2_param.py` before the first final render. Run finals from the command line overnight [25][26].
10. **Line reveals.** Draw one centre-line stroked path per reveal in Inkscape [35]. Run `recipes/r3_linedraw.py`, which computes the real path length. Do not rely on `pathLength="1"`, which the tested renderer ignored [66][100]. Use single-line fonts for titles. For a floor-art card draw at the phone floor: 4 px meaning lines, 3 px decoration, 6 px dots, 4 px holes, no hairlines (W-38 decision 3, W-72); a card carries no deity and no sathiyo (swastika) form until O-66 is answered (W-61). Her script on titles and verse cards travels as shaped outlines, never live text (W-21). The PowerShell frame loop is in playbook Exercise 6.
11. **Assemble.** Pass the profile explicitly to `melt`, `-profile atsc_1080p_24` for the 24 fps project (the tested form was `atsc_1080p_25`; UNVERIFIED at 24 until `recipes/r5_story.mlt` is re-run), because the default is 720×576 [17][100]. Crop 3:2 photos first. Do the final cut by hand in Kdenlive [8][11].
12. **Grade by album.** Derive one look per album from three of her prints. In each print, sample a known-white object and a skin midtone. Derive the lift, cast and grain from those samples, and save the look in `looks/`, named after her chapter. Apply that same string to every photo from the album [63][100]. The stock era chains in `recipes/r7_era_looks.txt` are practice material, not for the film. The derivation method is written and tested on three stock prints (research Follow-up F14; `research/toolchain-fixtures/derive_album_look.py`). It stays TODO(research) until it has run on her prints and on Windows Python.

### Per delivery (steps 13 to 18)

13. **Sound.** The premiere's honest sound is objects, rooms, the sea's surf and the maker's hum; sung devotion waits for April (W-44). Start from the maker's own captures in her empty house (W-10, W-70) and the hummed tune in two takes, closed-mouth and open vowel, both kept uncleaned in `originals/` (W-65); room tone is the bed under them and never a first sound, because it vanishes on a phone speaker (W-36, W-76). Any music is a CC0 or CC BY stand-in, labelled, and only if the sound is hers (O-72); there is no AI bed. If one passed one-key-three-guards, her HER-PUBLIC line goes on top. The premiere cut has no other recorded living voice (D-05); relatives' voices are April-version items (D-06). The final mix is made in REAPER, with Resolve Free's Fairlight as the fallback (W-20). Use only sources that pass Checklist C. Online copy: `loudnorm=I=-16:TP=-1:LRA=11`; every file holds -1 dBTP. Render three venue masters (-23, -18, -16 LUFS integrated) and choose at the Mon 22 Feb venue run; if no reading can be taken, load -18 first. Use two-pass `loudnorm`, the second pass linear (W-19); the phone files are the online row, measured on the final MP4 after the AAC encode. The broadcast reference is −23 LUFS [63][97][100].
14. **Captions.** Draft with Kdenlive's speech-to-text [13] or local Whisper [75]. Kdenlive's Whisper needs Python 3 installed first and downloads about 2 GB plus a model on first use, so set it up while online; transcription runs offline after that. On an 8 GB PC use `tiny`, `base` or `small` (`small` peaks at about 2.1 GiB and is the default). `medium` and `turbo` (about 5.1 to 5.4 GiB) only fit with other apps closed, and `large` does not fit. Check where the first `.pt` lands: the script reads `~\.cache\whisper`, and the manual names `%AppData%\kdenlive\opencvmodels` [116][117][118]. Test on one old phone recording or an older voice, not only a clean clip (a public-domain oral-history clip or the maker's own voice; not hers, not a relative's, and nothing gathered for the film; D-02, D-05). Caption layout per W-18: two lines, at most 20 characters a second, `FontSize=23` for Latin with `MarginV` 20 or more inside the 90% box ("42 characters a line" is a guide; a line must fit the box in its face), OFL fonts only (W-21). Gujarati is sized by the height of KA: Noto Sans Gujarati passes the venue at 23 and needs 26.2 for the phone's 3.8% target, so the phone file carries its own setting (`FontSize=28`, `MarginV` 40, two lines, at most 36 characters, block at 68 to 86% of height). On any ffmpeg older than n9.0 burn Indic text with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in its header), never `subtitles` or `drawtext`; the shaping A/B is a P-LOCK condition (W-75, W-06). The human proofreads every name and place. Resolve Free imports SRT and burns it in; automatic subtitles are Studio [110][111][112]. Mark the Windows run `TODO(verify on the maker's PC)`. Burn in captions for the screening file and always keep a sidecar `.srt` [12][13].
15. **Export the profiles from one master.** Screening MP4 (the venue file, W-17): 1080p24 H.264 High, level 4.1, yuv420p, CRF 18 with a 20 Mbps cap, AAC-LC 48 kHz stereo at 256 kbps, `+faststart`, BT.709 tags, captions burned in, a neutral file name and stripped metadata; plus a Main 4.0 backup at about 8 Mbps and a 60 to 90 second test clip with no personal content that carries a tone ladder from 100 Hz to 3.2 kHz. Phone files (W-63): PH1 is 1920×1080p24 H.264 High 4.1, yuv420p, BT.709 tags on the master before the burn-in, CRF 20 with an 8 Mb/s cap, AAC-LC 192 kbps, `+faststart`, `-map_metadata -1`, phone captions burned, -16 LUFS and -1 dBTP on the final MP4; PH2 is 1280×720, CRF 22, 4 Mb/s cap, level 3.1, captions burned on the 1080 frame before the downscale; SDR only, no HEVC; `playbooks/mobile-delivery.md` owns the commands. Web MP4: CRF 20 with a 12 Mbps cap, made for the April version and not uploaded or linked anywhere before the consent ledger closes (Mon 29 Mar) and the rights log is green (D-15, W-48). Archive: ProRes 422 HQ in `.mov`, and/or FFV1 v3 in `.mkv` with FLAC [91][92][93][94][100]. Use `recipes/r9_deliver.sh` [100].
16. **Verify.** Run ffprobe on every output and compare it with the profile. Check file size against the stick's format; FAT32 caps a file at 4 GB minus one byte [96]. Play the screening file from a USB stick on the venue or test screen before calling it done.
17. **Archive.** Keep masters, SRT/VTT, project files, originals, source SVG and Blender files, a README with versions, the licence and credits file, and SHA-256 checksums. Keep two physical copies and one off-site, where off-site is a second encrypted SSD kept elsewhere; there is no cloud copy of family media (W-25) [92][100].
18. **Report back.** List every `TODO(research)` the step touched, the tool versions used, and the exact command lines run.

## Checklists

### A. App and machine inventory (blocks the plan)

- OS and version; CPU; RAM; graphics card and video memory; free disk; pen tablet.
- Resolve edition (Free or Studio), version, and whether the External scripting setting is present. The 21 and 21.1 manuals make it Studio-only [110][111][112]; older notes [6][7] read the other way.
- Versions of Kdenlive, Shotcut, OpenShot, Inkscape, GIMP, Krita, Blender, Audacity.
- `ffmpeg -version` and `magick -version` output.
- Platform rules: Blender 5 on macOS needs Apple Silicon [30].

### B. Before any render

- Input is at least 1.5 times the output width; the crop matches the output shape before any zoom [100].
- View transform is Standard [100].
- A short draft run passed; time per frame is written down.
- Output is a PNG sequence with a fixed frame count and frame rate.
- Line length is read from the file, not typed in.
- A model exported from a Z-up tool is imported with forward axis Y and up axis Z [100].

### C. Music and sound licences

- Allowed: CC0 (Freesound CC0 [80]; Kenney game assets [83], audio packs not checked); Sonniss bundles, which need no credit and forbid AI training [82]; CC BY with credit (incompetech [76]; Freesound CC BY [80]); the maker's own recording. Freesound CC0 only as a labelled stand-in and only if the sound is hers (O-72, W-79).
- Not allowed for a film that may travel: CC BY-NC [78][80].
- Not allowed: YouTube Audio Library outside YouTube [77]; FreePD, which has closed [84].
- Save each licence page to `licences/` with the date. Put the credit text in `credits.txt`, worded as the licence requires.
- AI music: closed for the premiere (W-44, W-79). There is no AI bed, and never an AI voice of any devotional text in Gujarati, Braj or Sanskrit, nor of her songs or an imitation of a real singer. Suno free output may not be shown; Udio cannot supply a file (downloads disabled 2025-10-29); MusicGen weights are non-commercial [88][90][121].
- Unread sources (Musopen, Zapsplat, Openverse, ccMixter, Free Music Archive, BBC Sound Effects [85]): mark `TODO(research)` and do not use. Zapsplat and Musopen refused our requests with HTTP 403 [141].
- Mixkit: sound effects are allowed in a film [119]. Music is for the private link only, unless Mixkit confirms in writing for a venue [119].
- Pixabay: allowed for a film; keep the download record; avoid shield-icon (Content ID) tracks for the online copy [120].
- Her favourite commercial songs: the lean under only-me is none; use a substitute, silence plus kitchen sound, or the maker's own hum when the hum case (HC-1 to HC-7) allows it (W-65, W-79). At most two licensed songs, with sync and master, and only if the maker accepts that publishers and labels learn a film exists (W-44). The premiere is a mostly public gathering (D-08), so every cue is cleared for public screening; one paid rights-consult hour is booked by Fri 4 Dec once the country is known (W-55), every cue is decided by Mon 14 Dec, and any song without a written answer is replaced.

### D. Export and archive

- Every ffprobe result matches the profile table.
- FAT32 stick: each file under 4 GB, or the stick is exFAT and a screen test has passed [96].
- Loudness measured against the chosen target, not assumed.
- Captions in sync at three spot checks; names and places proofread.
- Archive holds masters, caption files, project files, originals, a versioned README, licences, and SHA-256 checksums.

### E. Privacy

- Scripts travel, photos don't. Agents build and test each script in the cloud on stock or synthetic images. The identical script runs on the maker's PC against the real photos, from a terminal with the Claude desktop app closed. Every photo set carries `cloud: none` by default and only the maker raises it. Preview proxies (about 768 px) go to the container only after the account's model-improvement setting is off, and no full-size family photo, scan or master ever leaves the VeraCrypt container except to the second SSD (D-15, W-24). A rented GPU is for non-family imagery only, Secure Cloud with an encrypted volume and the maker's recorded OK, never Community Cloud (W-23) [1][100].
- Working files stay on an encrypted local drive; the repo is public (D-26) and holds only text, scripts and ID-keyed manifests.
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
- An imported model lying flat or sideways because the axes were not converted [100].
- A floor-art card with a hairline, a stroke under 4 px or a dot under 6 px at 1080p (the phone floor, W-38).
- Parallax where only one layer moves, or every layer moves the same distance.
- A look built by eye and not saved, so it cannot be repeated.
- A file over 4 GB on FAT32, or a screen that was never tested.
- Captions taken from the tool without proofreading.
- A track whose licence was never read.

**Stop and escalate.**
- Any real photo sent to a web tool or uploaded without the maker's say-so.
- A synthetic voice or "performance" of a real person, living or dead, even with consent (D-16), or any synthetic voice in the premiere cut (W-46) [1].
- A reconstruction presented as real footage.
- Any step that would require asking the subject, or that would surface the project on a device, library or chat she can see.

## Ethics guardrails

- Real memories stay real. Keep originals untouched, log every step that changes pixels, and label reconstructions visibly [1].
- Inpainting, colourising and upscaling change or invent pixels. Treat each output as a reconstruction.
- No tool in this track draws, generates or photographs a deity; AI never touches a deity (W-61).
- No invented events, faces or voices [1].
- Rights and consent under only-me (D-03, W-46, W-48): nobody is asked before the premiere. Tier A is in; Tier B stills of adults (no voice, no sensitive context) are in with documented risk, ratified after; Tier C is out unless a yes is on file; Tier D is out; an identifiable minor without a yes on file is out. Written releases 4d to 4g go out after the premiere. The subject cannot be asked (the piece is a surprise): the maker is her proxy, and chapters on loss, illness, separation, money or conflict go through one-key-three-guards before any shot is built (a decision sheet, Fable's written flag, the maker's two decisions 72 hours apart, default OUT of the public cut on any doubt; D-04) [1].
- Credit music wherever the licence requires it. Disclose any AI-made music.
- Surprise: nothing syncs to a shared device or a cloud photo library [1]. The routine is a separate Windows account, OneDrive backup off for Desktop, Documents and Pictures, caches and recent-file lists cleared after every session, and the Mum-test on every shared device (W-26). Whether she shares the PC or the room is pending (O-03).

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

## Changelog

- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): P-LOCK name for the Sat 14 Nov lock; the game-world object route and its recipes retired and replaced by the floor-art line-draw card at the phone floor (D-29, W-72, S-46); repo stated as public (D-26); sound step follows the W-44 spine with the two-take hum (W-65); AI music closed for the premiere (W-44, W-79); caption step carries the Gujarati KA sizing, the phone setting and the `ass` path before ffmpeg n9.0 (W-18, W-75); PH1 and PH2 added to the export step (W-63); the venue test clip carries the tone ladder (W-17); no deity from any tool (W-61).
- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18): frame rate 24 fps (W-14), `atsc_1080p_24` and the recipes' 25 fps values flagged UNVERIFIED until re-run; `zoompan` proofs only and MO8a/MO8b (W-41); loudness -1 dBTP with three venue masters and two-pass linear `loudnorm` (W-19); venue file CRF 18 with a 20 Mbps cap and a Main 4.0 backup (W-17); sound order and REAPER mix for only-me (D-05, W-20); cloud policy (D-15, W-23, W-24); second encrypted SSD, no cloud copy (W-25); real photos after the L1 lock Sat 14 Nov and collection from Sun 15 Nov (D-13); music rules (W-44, W-55); consent rewritten as rights tiers with nobody asked before the premiere and the maker as proxy (D-03, D-04, W-46, W-48); no private link before the consent ledger closes (W-48).
