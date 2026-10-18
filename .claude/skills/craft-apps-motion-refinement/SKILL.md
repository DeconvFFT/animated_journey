---
name: craft-apps-motion-refinement
description: "Use when building, checking or handing off Life Journey chapters that involve ArtCraft FilmCraft, EffectCraft or SoundCraft. Triggers include computing Ken Burns scale for stills, writing or importing OTIO, FCP7 XML, FCPXML or EDL, pinning a Craft app version, preparing or reading back a hand-off folder for the maker's Windows PC, and planning an EffectCraft title or SVG line-draw. Do not use it for AI imagery, interview work, game mechanics, or for delivering audio through SoundCraft."
---

# Craft Apps Motion Refinement

## Purpose

Let agents build Life Journey chapters in code, then hand the maker a clean, checkable package. The maker refines it by hand in FilmCraft (and sometimes EffectCraft) on Windows. Every step has a fallback that does not need a Craft app. The Craft apps are free, open-source, early-alpha refinement layers. Nothing critical may depend on them.

Human-facing guide: `playbooks/craft-motion.md`. Evidence and gaps: `research/craft-motion.md`.

## When to use

- Planning a chapter's shots, Ken Burns moves, dissolves or titles for a Craft app.
- Writing, emitting, importing or validating OTIO, FCP7 XML, FCPXML or EDL.
- Pinning or testing a Craft app tag.
- Preparing a hand-off folder for the maker, or reading back the maker's edits.
- Planning an EffectCraft title, SVG line-draw or expression-driven motion.

## When not to use

- Generative imagery, restyling or animating photos as such: use `ai-photo-to-animation-pipeline`.
- Story gathering or interviews: use `life-story-interviewing`.
- Game mechanics: use `meaningful-game-mechanics`.
- Delivering audio through SoundCraft. Never. It is pre-alpha, has no sidechain and has MP3/AAC import bugs. Use the ffmpeg recipe (playbook R5) or FilmCraft Essential Sound.
- Any step where real family material would enter the tools before the pipeline is locked and the five-minute test has passed. Use generated test cards.

## Procedure

1. **Load context.** Read `CHARTER.md`, the playbook, and the research notes (recipes R1 to R8 and the gaps list). Look for a written result of spike S1 (tests T1 to T6, for example in `research/` or in a `build_info.json`). If none exists, the Craft command-line tools are unproven in the container. Plan with ffmpeg and code as the primary path, and treat the Craft CLI as optional.

2. **Pin the tools.** Use these unless a newer tag passes the maker's five-minute test. Hashes come from the release `SHA256SUMS.txt` files [40]:
   - FilmCraft v0.8.0, fallback v0.7.2. Windows x64 portable zip SHA-256 `0119afd59dfd6ecb94470ba6b3a48108ade87dabd4972898dd6c04e1db396b0b` (v0.7.2: `8e22fabdf2f802573d3af4ad9993c05212dead5e933efda0fa290e825313cde7`). Linux x86_64 tar.gz SHA-256 `b166877905ae8a1b5505066d6dde60d7ce05831cfb309bacd5d7970f4bb017e1`.
   - EffectCraft v0.11.1, for titles and line-drawing only. Windows zip `78bd7f63c6bd814bc33f07bd523b003a5f8d095244c5f67bd70e902448fd6e34`. Linux tar.gz `b9cb2ce68dd66458cc164437e431376e94e38e33e3b6529fa8fd45f8cf968934`.
   - SoundCraft: not pinned for delivery.
   - Download from `https://github.com/storytold/<repo>/releases/download/<tag>/<asset>` with `curl -L`. Verify with `sha256sum -c` (Linux) or `Get-FileHash -Algorithm SHA256` (Windows). Record tag and hash in `build_info.json`.
   - Unpack Linux tarballs into their own empty directory. Never run a binary from inside a downloaded folder with an interpreter.

3. **Conform media before any Craft app sees it.**
   - Stills: `convert IN.tif -auto-orient -depth 8 -resize 2880x1620^ -gravity center -extent 2880x1620 -strip OUT.png`, with 2880x1620 replaced by the sequence size. If the scan has a non-sRGB ICC profile, convert it to sRGB before `-depth 8`. FilmCraft ignores ICC and EXIF orientation [10]. Keep the 16-bit master untouched.
   - Phone, camcorder or VHS video: `ffmpeg -i IN -vf "yadif=mode=0:deint=interlaced,scale=1920:1080:flags=lanczos,format=yuv422p10le" -fps_mode cfr -r 25 -c:v prores_ks -profile:v 3 -vendor apl0 -c:a pcm_s24le -ar 48000 OUT.mov`. Drop the yadif step for progressive sources. Check with ffprobe.
   - Audio: 48 kHz 24-bit WAV or FLAC only. Never MP3 or AAC for working files [48].
   - One sequence size and frame rate for the whole film (default plan: 1920x1080, 25 fps).
   - Write a manifest row per file: source, conformed path, size, crop or pad decision, SHA-256.
   - Never crop a face silently. The crop decision is recorded per shot.

4. **Compute motion.** For a source of w x h px in a sequence of W x H px, with `scale_to_frame` off:
   - Fit scale = min(W/w, H/h) x 100. Cover scale = max(W/w, H/h) x 100.
   - Ken Burns: start at cover, end at cover x 1.12 to 1.25, with EaseOut.
   - Sanity values: 3600x2400 into 1920x1080 gives fit 45.0 and cover 53.3. 2880x1620 into 1080p gives 66.67 for both [11].
   - Scale 100 means native pixels, and position is in sequence pixels from the top-left [11][4].
   - Ticks (only when driving the CLI): 254,016,000,000 ticks per second. A 5 s still is 1,270,080,000,000 ticks [4].

5. **Write the neutral spec first.** One JSON file per chapter in the repo, the source of truth: frame rate; sequence size; ordered shots `{id, source, duration_frames, motion:{scale:[a,b], position:[[x,y],[x,y]], ease}, transition_out:{type, frames}, markers}`; audio cues `{file, start, gain_db, duck_against}`.

6. **Emit files, never hand-edit them.**
   - E2, OTIO with `metadata.filmcraft`. Dissolves are `Transition.1` objects with `in_offset` and `out_offset`, and consume no timeline time. Motion keyframes sit under `metadata.filmcraft.effects`. Without `metadata.filmcraft.settings` the sequence is 1920x1080 at the file's rate. For any other size, export a template OTIO from FilmCraft once and copy its `settings` object. Malformed effect metadata is dropped silently [6].
   - E3, FCP7 XML: export it from FilmCraft (`file.exportInterchange {format:"xml"}`). This is preferred over hand-written XML, because the exporter was built against what Premiere writes [5][8].
   - E4, bake-motion (use when a move must match in every editor): render each shot to a ProRes intermediate with `ffmpeg -y -loop 1 -framerate 25 -i IMG.png -vf "zoompan=z='min(1+0.12*on/124,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv422p10le" -frames:v 125 -c:v prores_ks -profile:v 3 -vendor apl0 shot.mov`. The OTIO then carries only cuts, dissolves and markers.
   - Never write `.fcproj` or `.ecproj` by hand. The schema moves, and errors are silent [2][3][29].

7. **Validate.**
   - With the CLI in the container: `filmcraft-cli --project ch01.fcproj inspect sequence`. Then `render --seconds 2.5 --out f.png` at the start, mid-dissolve and end frames. Then a draft `export draft.mp4 --preset "High Quality 1080p HD" --start 0 --end 10`. Check that `offlineMedia` is empty, and ffprobe the draft [14].
   - Drive the CLI one command at a time with `--save exec`, reading each result before the next. Confirm parameter names with `filmcraft-cli describe <id>`. Commands used: `file.newProject`, `file.import {paths}`, `file.newSequence {name,width,height,fps,sampleRate}` (set fps yourself; default is 23.976), `timeline.place`, `effects.setParam {clip, effect:"motion", param, value, keyframe:true, time}`, `effects.setInterpolation`, `sequence.applyVideoTransition {clip, effect:"cross_dissolve", frames}`, `markers.add`, `file.save` [9][14].
   - Without the CLI: check the ffmpeg draft with ffprobe. Optionally validate the OTIO with the `opentimelineio` Python package in a venv.
   - Spike check (after import on the maker's side): the `motion` effect must exist with keyframes. If it does not, the metadata was dropped [6].

8. **Build the hand-off bundle.** One folder with `media/`, `chNN.otio`, `chNN.xml`, `build_info.json` (tags, hashes, fps, size, date) and the spec. Use absolute `file:///C:/LifeJourney/...` media paths [5]. Do not hand over a Linux-path `.fcproj` unless the maker will run `media.autoRelink {from, to}` [2]. Include a note telling the maker what to check first: the import report, then the Resolve test.

9. **Read back the maker's edits.** Run `filmcraft-cli --project x.fcproj inspect sequence --compact` on the maker's file, or read the OTIO or XML they exported. Diff against the spec. Update the spec from the maker's change list. Never regenerate a shot the maker edited.

10. **Make the finals.**
    - Archive master: `filmcraft-cli --project x.fcproj export master.mov --preset "Apple ProRes 422 HQ"`. Use ProRes 4444 only for alpha or banding-sensitive gradients [11][18].
    - Venue copy: `ffmpeg -i master.mov -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 320k premiere.mp4`. FilmCraft's own H.264 encoder has no trellis or psy-RD [18].
    - Safety copy: 1080p, CRF 20, `-profile:v high -level 4.1`.
    - Verify: ffprobe (codec, pixel format, frame count against expected duration); `ffmpeg -nostats -i x.wav -af ebur128=peak=true -f null -`; compare three frames against `filmcraft-cli render` output.
    - For EffectCraft renders: `RAYON_NUM_THREADS=2 effectcraft-cli render --comp Main --out out --format png --channels rgba`, one job per process. Check each MP4 with ffprobe. An out-of-memory crash leaves no moov atom [30][47].

11. **Log everything.** Tool tags and SHA-256 values; the commands run; nproc and RAM; wall, CPU and RSS times; exit codes; ffprobe JSON; a one-line verdict. Write the verdict into the repo.

## Checklists

**Before importing media**
- [ ] Stills: orientation applied, 8-bit sRGB, sequence size, metadata stripped, master untouched.
- [ ] Video: constant frame rate, progressive, ProRes intermediate. Not HEVC HLG, not DV [46][13].
- [ ] Audio: WAV or FLAC at 48 kHz. No MP3 or AAC.
- [ ] Manifest row per file with SHA-256.
- [ ] Only test cards, if the pipeline is not yet locked.

**Before a hand-off**
- [ ] Every Ken Burns shot has `metadata.filmcraft.effects` in the OTIO.
- [ ] Read-back inspection shows the keyframes.
- [ ] `offlineMedia` is empty. No Linux-only paths.
- [ ] `build_info.json` has tags, hashes, fps and size.
- [ ] The hand-off note lists what to check first.

**After an export**
- [ ] Frame count matches the expected duration.
- [ ] Audio duration equals video duration within a frame.
- [ ] Loudness matches the decided target (provisional -18 LUFS, -1.5 dBTP).
- [ ] New output name; the last good file is kept [47].
- [ ] Three frames match the CLI render.

## Quality bar

**Good**
- Stills fill the frame at the computed cover scale. On a gridded test card, the grid lines up at start and end within 1 px.
- Dissolves are centred on the cut. A mid-dissolve pixel is within 2 levels of the average of its neighbours.
- The import report lists nothing unexpected, and there is no offline media.
- The ducking shows as volume keyframes, and the music does not clip.
- Every file has a manifest row and a hash. Every claim has a tag or a test behind it.

**Mediocre**
- A still looks cropped, and there is no recorded decision for it.
- Motion is missing after import, because the metadata was dropped silently.
- A tool's output is used as the source of truth, instead of the spec.
- Emitted files were hand-edited.
- The final depends on one unverified app.

**Fail (stop and escalate)**
- Out-of-memory crash, or an MP4 with no moov atom.
- Resolve or Kdenlive cannot open the OTIO.
- A hash mismatch on a download.
- Real material found in a bug report, a log or a synced folder.

## Ethics and privacy guardrails

- Real photos may be restyled, animated and connected. Never invent events, people or words. Reconstructions are visibly labelled (charter, principle 4).
- Never generate speech in a relative's voice, or words they did not say. Text-to-speech is for labelled, neutral text only. FilmCraft lists its speech models as optional and off in release builds [13][19].
- Never paste family names, file names, screenshots or clips into bug reports, issues or forums. The research note reports that a ticket bot relays reports to public GitHub issues.
- Keep working folders outside cloud-synced folders. Sync status on the maker's PC is unverified.
- Use portable zips. FilmCraft's control channel binds loopback without a token, and its MCP server has no folder confinement [14][19]. Run the control channel or MCP only for a session, and never with family material on the maker's PC.
- No telemetry in default builds. Do not enable optional downloads (Whisper, Kokoro, MobileSAM, MediaPipe) with family material without the maker's explicit say [19].
- Follow charter principle 5 for hard chapters. Nothing the proxy reviewer has not approved goes into the shared version.

## References

- Playbook (human guide): `playbooks/craft-motion.md`
- Research notes (evidence and gaps): `research/craft-motion.md`
- Key URLs: `https://github.com/storytold/filmcraft` (README, `docs/agents.md`, `docs/project-files.md`); `https://github.com/storytold/filmcraft/releases`; `https://github.com/storytold/effectcraft` (README, `docs/agents.md`); `https://github.com/storytold/effectcraft/issues/1615`; `https://github.com/storytold/soundcraft` (`docs/gaps.md`); `https://docs.kdenlive.org/user_interface/menu/file_menu.html`; `https://www.blackmagicdesign.com/products/davinciresolve`. The FilmCraft README, the FCPXML source, the KDE bug, the Resolve product page and a secondary Resolve source are cited below as [1], [7], [54], [55] and [56].

Sources cited in this skill (from the research note; not re-opened here):
- [1] github.com/storytold/filmcraft README.md @v0.8.0. Vendor claims.
- [2] filmcraft `docs/project-files.md` @v0.8.0. The schema history there is out of date.
- [3] filmcraft `crates/format/src/lib.rs` and fixtures @v0.8.0. Schema 15.
- [4] filmcraft `crates/project/` and `crates/time/` @v0.8.0. Data model and ticks.
- [5] filmcraft `crates/interchange/` @v0.8.0. Import, path resolution, reports.
- [6] filmcraft `crates/interchange/src/otio.rs` and `tests/otio.rs` @v0.8.0.
- [7] filmcraft `crates/interchange/src/fcpxml.rs` and tests @v0.8.0.
- [8] filmcraft `crates/interchange/src/{edl.rs, fcp7.rs}` @v0.8.0.
- [9] filmcraft `crates/engine/src/{interchange.rs, commands.rs, media_pool.rs}` @v0.8.0.
- [10] filmcraft `crates/media/src/still.rs` @v0.8.0. 8-bit RGBA stills; no EXIF or ICC.
- [11] filmcraft `crates/render/src/lib.rs` and `crates/export/src/` @v0.8.0. Motion and export presets.
- [13] filmcraft `docs/gaps.md`, `docs/target-app-parity.md`, `ROADMAP.md` @v0.8.0.
- [14] filmcraft `docs/agents.md` and `apps/filmcraft-cli/src/main.rs` @v0.8.0.
- [18] filmcraft `crates/h264enc/README.md` and `crates/prores/README.md` @v0.8.0.
- [19] filmcraft network-audit greps @v0.8.0. Optional downloads; control channel; no telemetry found.
- [29] effectcraft `crates/project/src/lib.rs` @v0.11.1. `.ecproj` schema 2.
- [30] effectcraft `apps/effectcraft-cli/src/main.rs` and `crates/export/src/lib.rs` @v0.11.1. Render flags, batch size.
- [40] https://github.com/storytold/filmcraft/releases/download/v0.8.0/SHA256SUMS.txt and the effectcraft v0.11.1 file. Hashes read on 2026-10-18.
- [46] https://github.com/storytold/filmcraft/issues/1998 and related issues. Read through a summarising tool.
- [47] https://github.com/storytold/effectcraft/issues/1615 and related issues. Read through a summarising tool.
- [48] https://github.com/storytold/soundcraft/issues/711 and `/710`. Read through a summarising tool.
- [54] https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1051588.html. KDE bug 503692.
- [55] https://www.blackmagicdesign.com/products/davinciresolve. Resolve free edition limits.
- [56] https://violetflare.ai/blog/davinci-resolve-otio-import/. Secondary source on OTIO in Resolve.
