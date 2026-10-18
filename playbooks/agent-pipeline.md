# Agent-First Production Pipeline: What the Agents Make, Where It Renders, How It Comes Back

*Draft v3, 2026-10-18. Track `agent-pipeline`. Built from `research/agent-pipeline.md` (researcher Sonnet, 2026-10-18) and `CHARTER.md`, reconciled with [DECISIONS.md](../DECISIONS.md) (2026-10-18). Not yet reviewed. Open items are marked TODO(research).*

*How to read the labels: [n] points to the Sources list at the end. (M1) to (M21) are measurements taken on 2026-10-18 in the project's cloud container, using made-up test material only. (J) is the researcher's judgment. ESTIMATE is arithmetic on measured numbers. UNVERIFIED means nobody has checked it yet.*

**Reconciled with DECISIONS.md (2026-10-18). The register wins (D-21).** The frame rate is settled at 24 fps on the settings card, Sun 1 Nov (W-14, W-16). The film is 9 or 12 minutes (W-01, W-02): a 12-minute film is a wrapper plus three 3:00 modules and a 9-minute film a wrapper plus two, so "chapter" below means a module of about 3:00 (W-04); the vertical slice is 100 seconds of C01 (W-07). Only-me (D-03): the maker is the proxy and nobody else reviews; hard chapters follow one-key-three-guards (D-04). Gathering starts Sun 15 Nov, after the L1 process lock on Sat 14 Nov (D-13, W-06). Family media stays on the PC and the encrypted drive: `cloud: none` by default, a second encrypted SSD, no cloud copy (D-15, W-24, W-25). Each row of the Decisions table carries its register status.

## Why this matters for our life journey

Our deadline is Saturday 27 February 2027, about 19 weeks from today. Your mother does not know the film is being made, so every step has to work the first time it is shown to her. There is no second take on the day.

The plan lets the agents do the repeated work: placing photos, timing moves, drawing simple scenes, rendering and checking files. Your hands go on the parts that need a person. Those are whether a face looks like her, whether a pause is long enough, whether a joke lands, and what the sound feels like.

The Craft apps (PhotoCraft, VectorCraft, FilmCraft, EffectCraft and the others) are where you make quick changes by hand. They are free, open-source and early alpha. So nothing critical may depend on them [1].

Be honest about the evidence. We found no multi-minute, emotionally paced film made by a coding agent, and no family tribute made that way. The examples we found run from 18 seconds to 3 minutes 30 seconds, and most of them are promotional [36][37][38][43]. This process is therefore built on evidence about the plumbing and the review loop. It is not proof that the film will move her. The answer is to test the feeling early, with one real viewer, on one chapter first.

The first real checkpoint is the one-chapter slice (G-SLICE: 100 seconds of C01, briefed Sun 15 Nov, animatic Sun 6 Dec, final Sun 20 Dec; W-07), reviewed in week 9 on Sunday 20 December 2026 [7].

## Core principles

1. **Story before software.** Her voice, places and objects decide what goes on screen. Tools come second [1].
2. **The agents build, you refine.** The source of truth is text in the private repo: scene code, shot briefs and the timeline. If you change a shot in a Craft app, export it and write down what you changed. The agents read your change back. They do not rebuild over it.
3. **A frame must be a function of time.** Ask for frame 48 twice and you must get the same picture both times. This lets an agent fix one shot without disturbing the others. In the probes, two runs of the same scene gave identical frames (M9, M10). Real-time animation did not repeat (M11). Any method that cannot step frame by frame is a prototype only.
4. **Scripts travel to the photos. Photos stay home.** Each set of photos has a `cloud` level: `none`, `preview` or `full`. The default is `none`. Full-size scans stay on the PC and on the encrypted drive [2][4][5]. `full` is for non-family material only: no full-size family photo is ever raised to `full` or leaves the PC (D-15, W-24).
5. **Avoid the template look on purpose.** Uniform easing, stock transitions, centred titles and the same slow zoom on every photo make any film look like a template. Random noise does not fix this. Deliberate variety, seeded so it can be repeated, and some asymmetry do [37].
6. **A person listens.** Agents can measure loudness. They cannot judge whether a sound feels right. One 22-agent run made a 90-second film and never listened to its audio. It opened 604 images and played 0 sounds [38]. Every chapter gets a listening pass on the TV or speakers it will play on.
7. **Finish beats sprawl.** If a review gate cannot be passed in time, shorten the film. Do not skip the gate (charter principle 8; D-24) [1].
8. **Keep the surprise in one piece.** Repo names, commit messages, folder names, cloud sessions and phone notifications must look harmless. Family group chats and cloud photo libraries are the usual ways a surprise leaks [1].

## How to do it, step by step

**Words first.**
- **Shot:** one continuous picture between two cuts.
- **Chapter:** a group of shots about one period of her life, told as a module of about 3:00 (W-04). The vertical slice builds 100 seconds of the first chapter, C01, which is 2,400 frames at 24 frames per second (W-07) [7].
- **Route A:** scenes drawn in web code (SVG, GSAP animation, rough.js for hand-drawn edges, three.js for simple 3D). A headless browser (a browser with no window) captures them one frame at a time [22][24][25][26].
- **Route B:** real photos moved and finished with ImageMagick, Pillow and ffmpeg.
- **Hand-off:** a file given to a Craft app, in a format both sides can read.
- **Gate:** a review that ends with a written decision saved in `reviews/`.

**Step 1. Lock the settings (propose in week 1; the maker signs the settings card Sun 1 Nov, W-16).** Write them in the repo and never change them per shot once signed.
- Picture: 1920 by 1080 pixels.
- Frame rate: 24 frames per second, settled (W-14, W-16; see Decisions).
- Colour: Rec. 709 and sRGB (Rec. 709 / BT.1886 for video, sRGB for stills; W-16).
- Sound: 48 kHz, 24-bit.
- Master: ProRes 422 HQ. Access copy: H.264 (details in Templates).

**Step 2. Learn your PC (week 1).** Do Exercise 1. Then install and test the tools on the Windows PC. The list is Git, ffmpeg with ffprobe, Python 3.13 or `uv`, and the Craft apps as portable zips pinned to a version (W-22; the Launcher is never installed, D-12) [3][4]. Install the first three from PowerShell with winget. These IDs were read from the winget manifests on 2026-10-18 and have not been run on Windows yet: `winget install --id Git.Git -e` (Git 2.55.0.5), `winget install --id Gyan.FFmpeg -e` (ffmpeg 9.0.2; this is not the 6.1.1 build the container uses, so the colour-patch test must run on it), and `winget install --id Python.Python.3.13 -e` (3.13.15) [69][70][71]. Open a new terminal afterwards so PATH refreshes. The Craft app download steps are TODO(research). Run the five-minute tests described in `research/craft-visual.md` and `research/craft-motion.md` (R7) [3][4].

Optional: Claude Code can run natively on Windows with a PowerShell one-liner. It needs Windows 10 version 1809 or later and at least 4 GB of RAM. Sandboxing is not supported on native Windows [46]. Do not use the Claude desktop app for this work. The charter records that it uses too much memory on this PC [1].

**Step 3. Run the spikes (week 1).** Five short tests decide which routes are real. Each has a pass mark. Fable reviews the results at the L1 process lock, Sat 14 Nov (W-06).
- **S1:** the Craft command-line tools inside the container. The scope is in `research/craft-motion.md` (R8) [3].
- **S2:** frame capture for Route A.
- **S3:** Blender, for hero shots.
- **S4:** how the cloud container behaves when idle. Open question: does a running background job keep it awake? TODO(research), not documented in the pages read.
- **S5:** the validators (Templates).

A route that fails its spike is dropped, or moved to the PC. Do not argue with the result.

**Step 4. Write the shot brief (gate G0).** The agent drafts one short brief per shot. It says what the shot is for, where the material comes from (an album-session excerpt, a Card A slip or a document ID), how long it lasts, which route builds it, each input and its `cloud` level, the palette, the motion family, the seed, the audio cues and the checks it must pass. You approve or comment in `feedback/<shot>.md`. If an input is `cloud: none`, the agent still writes the brief, the script and the expected `render.json`, commits them and marks the shot `pc-render`. You run `lj.ps1 run <shot>` on the PC and push the validator JSON and the preview; only the cloud render is skipped. Raising the level is never the agent's move.

**Step 5. Approve three style frames (gate G1).** Before any motion, the agent makes three still frames that show the look. The palette is six colours or fewer, sampled from her prints. Type and textures are recorded with their licence files. You approve them; the first approved set is G1, Sun 15 Nov (W-38). Under only-me nobody else looks, and a hard chapter follows one-key-three-guards (D-04).

**Step 6. Build and render a draft (agent, 10 to 40 minutes per shot).**
- Route A: the scene exposes `seekTo(t)`. That function sets the picture for time `t` and does nothing else. A repo script captures the frames in sharded, resumable jobs of 10 minutes or less, writing each frame to disk as it goes [49][50].
- Route B, a parameterised photo move: a seeded generator picks direction, duration, easing, hold and drift for each photo, so no two photos move alike. Pillow moves each still. Grain and paper are pre-made overlays, not live filters, because live filters are slow and do not repeat exactly (M6, M10). ffmpeg does the grade, the dissolves and the encode.

**Step 7. Self-check (agent, at most three fix loops).** The validators in Templates run before anything is handed on. A failure goes into the shot's review file. It is never hidden.

**Step 8. Review pack and critic (gate G2).** The agent makes a contact sheet of eight timed frames, frame strips for key moments, full-resolution crops of faces and type, and a preview of 20 MB or less. It also writes `render.json`, which records the inputs, the seed, the tool versions and the file hashes. A fresh-context reviewer scores the six charter criteria. Run the critic twice with different frame orders and compare the answers. A critic that sees only stills cannot judge smoothness or sound [43].

**Step 9. Your review (5 to 10 minutes per production day, W-42).** Watch the day's review packs with sound on, for no more than 5 to 10 minutes. Drop markers only (red cut, yellow hold, green breath, blue wrong photo) and approve nothing until 48 hours have passed. Write the comment file (Templates) from your markers. For any shot flagged for template risk, compare the draft with a variant. Do not be told which one the agent made.

**Step 10. Revise, then freeze.** The agent gets at most two rounds of revision. After that the scene is frozen. Further changes happen in a Craft app, not in the code.

**Step 11. Refine by hand (gate G3, class B and C shots only).** Pull the hand-off files. Open them in PhotoCraft (layered `.ora` files), VectorCraft (SVG), EffectCraft (titles) or FilmCraft (editing). Make your changes, then export under a new file name. Run the validator on the export. Never save over the only copy of anything. A Craft app touches only a copy in `work\`, a chapter whose spec and OTIO are in the repo, or a title whose SVG fallback exists, and is never a step in the week before the premiere (D-12).

**Step 12. Hand back and render the final (agent).** The agent validates the export, re-attaches the animation to the shapes by their IDs, renders at full resolution and saves a new approved version. Version numbers only go up.

**Step 13. Assemble the chapter (you and the agents, 1 to 2 hours per chapter pass).** The agents write the timeline file. You open it in FilmCraft on the PC, adjust it and export ProRes 422 HQ. ffmpeg makes the access copy. Then three gates run.
- G4: a reviewer checks pacing, variety of moves, continuity and captions.
- G5: dignity and facts. Fable flags in writing and the maker decides under one-key-three-guards (a decision sheet per item, the written flag, the maker's two decisions 72 hours apart, default OUT of the public cut on any doubt). Fable never passes G5 (D-04).
- G6: a technical check. Run ffprobe and loudness measurement, check captions, test the file on a TV at about 3 metres [7], and make a safety copy.

**Step 14. Close the day (agent, about 10 minutes).** Update the manifests and the ledger. Commit text only. Run the backup on the PC. Delete old drafts. Write the day's note.

**Rhythm and budget (ESTIMATE, J).** The maker's reliable hours per week, H, are still pending (O-01; in writing by Sun 15 Nov). The format track's early figure of about 10 hours a week and about 190 hours to the deadline is superseded: the film's effort comes from the production-scale model (12 minutes: 141, 284, 201 and 116 hours for Prior, Base, Base plus levers and Best), measured by `h_slice` on Sun 20 Dec (W-02) [7]. A workable week is three weekday sessions of 30 to 45 minutes, where you look at one contact sheet and one short preview and write comments (the register's O-01 recommendation). Add one 3 to 4 hour weekend block in the Craft apps on two or three hero shots. A module costs you about 4.5 to 5.5 hours of review and hand work; the wrapper counts as one unit, so a 12-minute film is four units, about 18 to 22 hours, and a 9-minute film is three, about 14 to 17 hours.

## Learn-by-doing exercises

Do these in order. Use only made-up or test material. No family photos until the L1 process lock (Sat 14 Nov); covert collection starts Sun 15 Nov (D-13). Times are for a first attempt (J).

**Exercise 1. Know your PC.**
- **Goal:** write down the five facts that decide the encryption route, the local model options and the export speed.
- **Steps:**
  1. Open PowerShell from the Start menu.
  2. Run `Get-ComputerInfo` and note the Windows edition (Home, Pro or other) and the physical memory.
  3. Run `Get-CimInstance Win32_VideoController` to get the graphics card name. If it is an NVIDIA card, also run `nvidia-smi`. If not, run `dxdiag` [R10 in the research].
  4. In File Explorer, check the free space on the drive you plan to use.
  5. Ask: does anyone else use this PC? Write the answer down (O-03, still pending). A shared family device changes the surprise risk.
  6. Save the answers in a text note. Later, the `lj.ps1 doctor` script is meant to write them to `maker-pc.json`. That script is designed but not written yet [TODO(research)]. Its output must not contain your Windows user name or the PC's name, because `maker-pc.json` lives in the repo (Pitfall 10).
- **Time:** 20 minutes.
- **What good looks like:** five answers written down, each with the command that produced it. You can say whether the edition is Home or Pro. That matters because BitLocker needs Pro or higher, and Home's device encryption does not cover USB drives [61].

**Exercise 2. Meet the cloud container.**
- **Goal:** see the agent's machine and its limits, with no private material in it.
- **Steps:**
  1. Open claude.ai/code in a browser tab. This needs a Pro, Max, Team or Enterprise plan [50].
  2. Start a session on a private repo that holds no personal files.
  3. Ask the agent: "Report the CPU count, total memory, free disk, the Playwright and Chromium versions and the ffmpeg version. Change nothing."
  4. Close the tab. Come back after 10 minutes and check that the session and its files are still there. Expect the files to be there. A background job that was running when the machine was reclaimed is gone, and whether a pause alone ends one is still open (spike S4).
- **Time:** 30 minutes.
- **What good looks like:** you can write down the four numbers. The research measured about 4 vCPU, 16 GB of RAM, 24 to 28 GB of free disk, Playwright 1.56.1, Chromium 141 and ffmpeg 6.1.1 on 2026-10-18 (M1 to M3) [67]. The numbers can change. You understand that idle sessions pause, and that a reclaimed machine does not restore background work that was still running [49][50].

**Exercise 3. Prove that a frame repeats.**
- **Goal:** see why every frame must be a pure function of time.
- **Steps:**
  1. Ask the agent to build a one-page SVG scene with five shapes, one paused GSAP timeline, a `window.seekTo(t)` function, and rough.js shapes with a fixed seed for each shape [22][24][25][26].
  2. Ask it to render frames 0 to 47 (two seconds at 24 frames per second) in two separate runs. Ask it to compare the file hashes.
  3. Ask it to add an unseeded random number to one shape and repeat the test. Expect differences.
  4. Restore the seed. Ask it to add a full-frame grain filter and repeat. Note how much slower it runs.
- **Time:** about 1 hour.
- **What good looks like:** the first two runs match exactly. The random version does not. You can explain in one sentence why baked grain is faster and more repeatable than a live filter (M6, M10).

**Exercise 4. Hear the difference.**
- **Goal:** learn that loudness numbers are not enough for sound.
- **Steps:**
  1. Ask the agent for a 20-second 48 kHz, 24-bit WAV test file. It should have a soft tone that starts at 5 seconds and a single click at 10 seconds.
  2. Ask it to measure loudness and true peak with `ebur128` and report the results.
  3. Listen on headphones. Write down what the numbers did not tell you, such as whether the click is harsh or whether the start is abrupt.
  4. Ask for a second version with a 0.5-second fade in and out. Listen to it.
- **Time:** 45 minutes.
- **What good looks like:** you can say what the numbers reported and what your ears reported, and why they differ. You know that the agent cannot make this judgment for you [43][38].

**Exercise 5. Spot the template.**
- **Goal:** learn to see the tells that make a film look generated.
- **Steps:**
  1. Pick two short motion-graphics videos to study. Watch each once with the sound off and once with it on. Watch them only for study.
  2. For each one, write down the easing (does everything start and stop the same way?), the transitions (is it always the same one?), whether all photos move the same way, and whether text is centred and typed on.
  3. Compare your list with the anti-patterns in the research: uniform easing, stagger that is evenly spaced, one stock transition, lower-third labels, the same zoom on every photo, centred text with constant-speed typing, neon-on-dark gradients [37].
  4. Ask the agent to write a simple check that flags more than 60% of tweens sharing one ease string [R8 in the research].
- **Time:** 45 minutes.
- **What good looks like:** you can name at least four tells in each video. You can say which tell you most want to avoid in ours.

**Exercise 6. Write one manifest line.**
- **Goal:** practise the consent and label fields before real photos arrive.
- **Steps:**
  1. Ask the agent to create one made-up test image and one manifest line for it, in the schema from the research (R2). Use a placeholder person ID such as `P-001`, and a placeholder date with precision `unknown`.
  2. Set `consent.status` to `pending` and `cloud` to `none`.
  3. Choose a label level by reading the ladder in `research/ai-imagery.md` [2]. Do not guess at a level.
  4. Ask the agent to check that the line matches the schema.
- **Time:** 30 minutes.
- **What good looks like:** every field is filled or set to a placeholder on purpose. The line contains no real name, and it passes the check.

**Exercise 7. Hand a file to a Craft app and back.**
- **Goal:** test the hand-off contract on a file nobody cares about.
- **Steps:**
  1. Ask the agent to make a 1920 by 1080 OpenRaster file (`.ora`) with three transparent PNG layers. Name the layers by ID, for example `L10_sky`, `L20_table`, `L30_title`. The file also needs a `stack.xml` [4].
  2. Open it in PhotoCraft on the PC. Move one layer and lower another layer's opacity to 60%.
  3. Save it under a new name, `..._v002`. Export a flattened PNG.
  4. Put the export back in the repo folder and ask the agent to validate it: the zip opens, `stack.xml` parses, and the layer names match the ID pattern.
- **Time:** about 1 hour.
- **What good looks like:** the layer names survive the round trip. The original `v001` file is untouched. You know why adjustment layers, layer styles and live text must not be relied on across a hand-off [4].

## Templates and checklists

**Project settings card**

| Setting | Value | Note |
|---|---|---|
| Picture | 1920 x 1080 | Fixed for the whole film [3][7] |
| Frame rate | 24 (settled) | Signed on the settings card Sun 1 Nov (W-14, W-16). A 25 fps access copy only if a 50 Hz-only venue judders |
| Colour | Rec. 709 / BT.1886 (video), sRGB (stills) | Tag BT.709 on every H.264 file |
| Sound | 48 kHz, 24-bit WAV | Measure loudness with `ebur128` |
| Master | ProRes 422 HQ | About 590 MB per minute on a test pattern (M5) |
| Alpha overlay | ProRes 4444, yuva444p10le, BT.709 | Not a master. Encode with the ProRes 4444 chain in `skills/agent-first-production-pipeline/SKILL.md` step 8 (measured in research Q-F1). Tags are not enough: the colour-patch test must pass (Validator checklist). An RGBA PNG sequence from EffectCraft is preferred (`research/craft-motion.md`, issue #340) |
| Access copy | H.264 High, yuv420p, BT.709, limited range, faststart, CRF 16 to 18 | [3]. Encode with the chain in SKILL step 8, then pass the colour-patch test (Validator checklist). The venue file is CRF 18 with a 20 Mbps cap and AAC-LC 256 kbps (W-17) |
| Safety copy | 1080p24 H.264, Main profile, level 4.0, about 8 Mbps | The register's backup copy (W-17) [3] |

**Shot brief** (one file per shot, `brief.yaml`)

```yaml
id: LJ-C01-S014
chapter: C01
class: A            # A photo move | B designed graphic | C hero shot | D title or caption
beat: "One sentence: what the viewer should feel or learn."
source_ref: "album-session excerpt id, Card A slip id or document id"
duration_s: 6.0
fps: 24             # project rate; never changed per shot
route: B            # A | B | blender | craft
inputs:
  - {id: LJ-B03-0042-F__L1, role: main, cloud: preview, crop: "keep both faces; no silent crop"}
look:
  palette: [paper-cream, tomato-red, ink-brown, faded-green]   # six or fewer
  type: {family: Caveat, license: OFL-1.1, use: "captions only"}
motion:
  camera: "slow push, drift left, settle at 4.8 s"   # a family, not a recipe
  ease_family: asymmetric-settle
  hold_on_twos: true
  seed: 20261024
audio: {voice: none, room: LJ-A02-0007, music_cue: m03, sync_points: ["3.2 s: the kettle clicks off"]}   # premiere cut: no recorded living voice except one HER-PUBLIC line if it passed (D-05)
constraints: [no invented faces, no lower thirds, no beat-synced zoom, reconstructions visibly stylised]
acceptance: ["first and last 0.3 s clean", "face never cropped", "hold 0.75 s or more after the click"]
output_level: L4a   # label ladder level of the result [2]
```

**Feedback comment file** (`feedback/LJ-C01-S014.md`, written by you)

```markdown
---
shot: LJ-C01-S014
version: v007_draft
approve: no            # yes | no | with-changes
---
- 00:01.2  hold longer on her face; the push starts too soon  [should]
- 00:03.2  the click lands, but the music is already loud  [blocker]
- whole    camera drifts the same way as S013  [nice]
craft-app-needed: no
```

Severity words are `blocker`, `should` and `nice`. The agent answers each line in `render.json` with `done`, `declined (reason)` or `question`.

**Gate checklist** (each gate is a file in `reviews/<chapter>/`)
- **G0 brief:** Does the beat come from a named source? Is the camera, ease, palette, type and seed named? Does every input have a consent status, and is its `cloud` level allowed for this use? Are the acceptance checks testable?
- **G1 style frames:** Could this be any family's film? Six colours or fewer, sampled from her prints? Every font and texture has a licence file? Reconstructions visibly stylised?
- **G2 shot draft:** Validators green, with the JSON attached? Hold of 0.75 s or more after each payoff? No loops or stretches to fill a slot? Faces and type checked on full-resolution crops? Template-risk output reviewed? Open items listed, not hidden?
- **G3 refine:** Your changes pass the hand-back validators? Nothing you did was lost? Labelled as yours?
- **G4 chapter:** Varied move families, holds and silence? Palette and type continuous? Captions within the length and reading-speed limits in the format track [7]? Loudness plan? No more than three class-A shots in a row without a held still, a class B, C or D shot, or a voice-only beat? At least one shot per chapter where the photo does not move at all?
- **G5 dignity (the maker, under one-key-three-guards):** Each hard topic (loss, illness, separation, money, conflict) has a decision sheet, Fable's written flag and the maker's two decisions 72 hours apart, and is cleared or OUT? Anything HOLD or PRIVATE, and anything she might not want seen in front of a public room, is out of the public cut? Fable flags and never passes G5 (D-04).
- **G6 technical:** Master is ProRes 422 HQ. Access copy is H.264, yuv420p, BT.709, limited range. Frame count, duration and 48 kHz audio are right. Loudness holds -1 dBTP, with the venue master chosen at the Mon 22 Feb run (W-19). The file plays on the venue-class TV. Checksums are logged. The second copy is a second encrypted SSD kept elsewhere, verified (W-25).

A gate passes only when every score is 4 or higher and nothing critical is open [1].

**Validator checklist** (before any hand-off)
- **Video:** run `ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,color_space,color_range,color_primaries,color_transfer -of json <file>`. The frame rate must equal the project rate. H.264 must show yuv420p, BT.709 and limited range. The frame count must equal duration times frame rate. Then run `ffmpeg -v error -i <file> -f null -`, which must print nothing. [R8]
- **Alpha:** ProRes 4444 files must show an alpha pixel format (`yuva444p12le` was reported in testing, M12).
- **Colour matrix (pixels, not tags):** encode a 3-patch frame (pure red 255,0,0; 50% grey 128,128,128; skin tone 224,172,140) through the shot's exact command line, decode it to `rgb24` with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`, and require every channel within ±3/255. Run it once per command-line template, and again whenever the ffmpeg version differs (the PC build is ffmpeg 9.0.2 from winget, not 6.1.1). Tags alone are not evidence: a BT.601 matrix under BT.709 tags passes every tag check.
- **SVG:** renders without being blank. Every ID survives. Do not run the default optimiser preset, because it strips every ID (M17).
- **ORA:** the zip opens, `stack.xml` parses, every layer file exists, and names match the ID pattern.
- **Timeline (OTIO):** parses, every media file exists, every clip sits inside its available range, and the rate matches the project.
- **Audio:** 48 kHz, 24-bit. Record loudness and true peak with `ffmpeg -i <file> -af ebur128=peak=true -f null -`; true peak must be at or below -1 dBTP (W-19).
- **Fonts and textures:** each has a licence file. Handwriting fonts are OFL or Apache licensed [29]. Textures from ambientCG are CC0 [28]. Each texture has a source URL and a date.
- **Pacing and repeat:** no shot under 1.5 seconds except impact frames. Two renders of one frame compare equal, or within the agreed tolerance.

**Before anything goes to the cloud**
- The set's `cloud` level is set by you, not by the agent.
- Before the first `preview` level, your account's model-improvement setting is off. With it on, data is kept for 5 years and may be used for training. With it off, data is kept for 30 days [51].
- Only made-up or stock images, or proxy-sized images of a set the maker raised to `preview`, are used (D-15, W-24).
- No family photo goes to a hosted renderer or to any hosted "memorial video" service.
- API keys go in the environment's network secrets, never in chat, in environment variables or in the repo [49].
- The repo holds person IDs such as `P-001`, not names. The key that maps IDs to names stays offline.

**Shot classes and maker time (ESTIMATE, J)**

| Class | What it is | Share of shots (research estimate; see below) | Your time per shot |
|---|---|---|---|
| A | Parameterised photo move (seeded; capped by gate G4) | about 60% | about 2 minutes |
| B | Designed graphic | about 25% | about 12 minutes |
| C | Hero shot (3D or Blender) | about 10% | about 60 minutes |
| D | Title or caption | about 5% | about 5 minutes |

At 8 shots a minute (W-34, W-51) a 12-minute film has about 96 shots, about 24 per module, and a 9-minute film about 72; the research counted a 10-minute film at about 120 shots. Under the register, hero shots (class C) are 5% of shots, about five in the film and four at 9 minutes, and the kitchen is the only built set (W-34), so the class C share in the table (about 10%) is the research's pre-lever estimate, not the plan [R4 and Q7 in the research]. No more than three class-A shots in a row without a held still, a class B, C or D shot, or a voice-only beat. At least one shot per chapter where the photo does not move at all (gate G4).

**Names**
- Assets: `LJ-<set>-<seq>-<side>`, for example `LJ-B03-0042-F` [2].
- People: `P-001`. Chapters: `C01`. Shots: `LJ-C01-S014`. Generated pieces: `LJ-C01-S014-A03`.
- Renders: `LJ-C01-S014_v007_draft.mov`. Approved: `LJ-C01-S014_v007_appr.mov`. Chapter master: `LJ-C01_v003_master.mov`.
- Versions only go up and are never overwritten. A failed overwrite once destroyed a file in the EffectCraft CLI (issue #1230) [3].

## Decisions you'll need to make

For each decision: the options, then our current lean and why. The lean is a starting point, not a verdict.

| # | Decision | Options | Our current lean |
|---|---|---|---|
| 1 | Format of the film | Film, explorable world, scroll story, or a hybrid [1] | **Register: default (W-30, W-01, W-02).** A linear, captioned film in chapters, 1080p, of 9 or 12 minutes: 12 if H is 16 or more, 9 if H is under 14, and the 8-minute tier is replaced by 9. This playbook assumes a film [7]. |
| 2 | Frame rate | 24, 25 or 30 frames per second | **Register: settled (W-14, W-16).** 24, signed on the settings card Sun 1 Nov. Holding on twos then gives 12 drawings per second. A 25 fps access copy is made only if a 50 Hz-only venue judders. |
| 3 | Carrying routes | Route A, Route B, Blender, Craft CLI | Route A and Route B carry the slice. Blender is for the hero shots: about five in the whole film (four at 9 minutes), with the kitchen the only built set (W-34). HyperFrames is compared with our own harness in experiment E1 [22]. Remotion is a further alternative, pinned if used, and its licence changes in version 5.0 [9][10]. |
| 4 | Where renders run | Cloud container, your PC, rented GPU | **Register: decided (W-23, D-15).** Drawn scenes in the container. Real full-size photos on the PC. Blender hero shots for scenes with no family imagery, as Workbench drafts and sharded Cycles finals in the container; a rented GPU hour (cost UNVERIFIED) only for non-family imagery, Secure Cloud with an encrypted volume and the maker's recorded OK, never Community Cloud [6][R0 in the research]. |
| 5 | Cloud level per photo set | `none`, `preview`, `full` | **Register: decided (W-24, D-15).** `none` by default, and only the maker raises it. Move to `preview` only after your model-improvement setting is off [51]. |
| 6 | Encryption on the drive | BitLocker (Windows Pro or higher) or VeraCrypt volume | **Register: default (W-25).** A VeraCrypt file container on the external drive, created by an administrator account, mounted only while working and dismounted before leaving the desk; BitLocker may be added if the PC is Pro. Decide the rest after Exercise 1 [61][63]. |
| 7 | Second copy off-site | Encrypted cloud copy (Backblaze B2 with rclone crypt, or Cryptomator [62]), Hetzner Storage Box, or a second SSD kept elsewhere | **Register: decided (W-25, D-15).** A second encrypted SSD kept elsewhere; no cloud copy of family media. The cloud options in this row are not used for family media; the research's B2 price of $6.95 per TB-month [59][60] and Hetzner's unpriced page [64] are kept for the record. |
| 8 | Git LFS for media | Yes or no | **Register: decided (W-25, D-14).** No. Media lives on the encrypted drive, with checksums in the repo. LFS rates for personal accounts are UNVERIFIED [54][57]. Plain Git warns above 50 MiB and blocks above 100 MiB [56]. |
| 9 | Paid image and video generation | Gemini API paid tier, Replicate [66], none | Paid tier only, and only for non-family imagery or `preview` proxies of a set the maker has raised, with the maker's recorded OK for each batch (D-15, W-23, W-24); never full-size family photos, and no AI animation of a real face (D-16). Budget about $3 to $40 per chapter (ESTIMATE) [65]. No image or video model is named in the announced changes of 2026-12-01 and 2027-01-01, so no date forces the batch: run it when cleared photos exist, and re-read the page in the week it runs [65]. |
| 10 | Local agent on your PC | None, a local Claude Code session with Remote Control [47], or only the script | Script only, plus cloud agents. A local session only for chapters that need live driving of a Craft app. Watch its memory: several GitHub reports describe `claude.exe` growing very large on Windows (search results only) [53]. |
| 11 | Who is in on it, and the proxy for hard chapters | Decided 2026-10-18: only the maker | **Register: decided (D-03, D-04).** The maker is the sole producer and the proxy for hard chapters; nobody else is in on it and nobody else reviews. Hard chapters follow one-key-three-guards (charter principle 5) [1]. The one scheduled re-opening is TD-L2c, Sun 3 Jan. |
| 12 | Venue and screening | Party, private screening, or both | **Register: decided (D-08), venue dated (W-17).** A mostly public gathering, treated as a public screening [1]. The venue is asked by Fri 6 Nov and its written answer, due Sun 15 Nov, decides file or DCP. Plan one playback test on a TV at about 3 metres from a USB-playable file [7], and the venue visit with a test clip by Sun 17 Jan (W-56). |

## Pitfalls

1. **The template feel.** Agents default to uniform easing, stock transitions and tidy symmetry. Fix: seeded variety per shot, a look-lock before motion, the template check, and your blind comparison at G2. If it still looks generic, cut the effect or hold the shot longer.
2. **Nobody listens.** Loudness numbers are not a listening test. Fix: you listen at G2 and G4, on the TV or speakers the film will use [38][43].
3. **Live filters are slow and not repeatable.** A full-frame grain filter ran at 1.2 frames per second, and two runs with two filters differed in 5 of 36 frames by 12 to 80 pixels (M10). Fix: bake grain and paper into overlays. The cause of the small differences is UNVERIFIED (TODO(research)).
4. **The container pauses and can be reclaimed.** Work that was still running is not restored [49][50]. Whether a running job keeps it awake is unknown (spike S4). Fix: jobs of 10 minutes or less, resumable frames, state kept in Git. Fallback: run long jobs on the PC or on a rented machine.
5. **Disks fill up.** A 12-minute film at 24 frames per second is 17,280 frames (the research counted a 10-minute film, 14,400 frames). Textured PNG frames are about 2 MB each, so loose frames would need about 35 GB. The container has about 24 to 28 GB free (M1, M10). Fix: pipe frames straight into ffmpeg, or encode each chunk and delete its frames.
6. **Colour range mistakes.** Remotion's default output was full-range and tagged `bt470bg` (M13). Fix: set BT.709 and limited range explicitly, and check with ffprobe. The ffmpeg chains are not interchangeable across builds: the bare `-pix_fmt yuva444p10le` ProRes 4444 encode gave BT.601 pixels under BT.709 tags on ffmpeg 6.1.1 (10-bit luma 326 against 250) and correct pixels on 9.0.2 (Q-F1). On the Gyan 7.1.1, 8.1.2 and 9.0.2 builds tested, `-color_primaries` and `-color_trc` did not reach the stream, so the `setparams` filter restores them. Check the pixels with the colour-patch test, not only the tags. EffectCraft's ProRes 4444 is "tagged bt709 but sRGB-encoded" (open issue #340, `research/craft-motion.md`): prefer the RGBA PNG sequence, and use ProRes 4444 only after the colour-patch test passes.
7. **Alpha software.** The Craft apps are early alpha and release often [3][4]. EffectCraft's command-line syntax is read from its source at tag v0.11.1 [68]. Fix: every step has a non-Craft fallback. Render to a new file name each time. Read the import report. Keep the source files regenerable.
8. **Stills at the wrong size in FilmCraft.** FilmCraft reads neither EXIF rotation nor colour profiles, and it decodes whole files to 8-bit [3]. A 3600 by 2400 still in a 1080p sequence needs a scale of 53.3%, or a pre-made 2880 by 1620 copy. Fix: convert stills before import.
9. **Cloud privacy.** Anything Claude sees in a session, including a photo, becomes part of the transcript [51]. Remote Control also stores the transcript on Anthropic's servers to sync it [51]. Fix: the `cloud` level and the setting in Templates.
10. **Surprise leaks.** Phone notifications can show on a shared screen. So can repo names, commit messages, backup folder names and bucket names. Fix: innocuous names, notifications off on shared devices, a separate browser profile for this project [1][3]. The output of `lj.ps1 doctor` must not contain your user name or the PC's name, because `maker-pc.json` is in the repo.
11. **The CLI cannot click apps on Windows.** Computer use in the CLI is macOS only. On Windows only the Desktop app can do it [48]. Fix: use the Craft apps' own control channels, or files, or your own hands.
12. **Loopback control ports.** VectorCraft and LightCraft's `--control` ports have no authentication. Start them only for a session and close them afterwards [4].
13. **Cost creep.** An unattended 22-agent run cost $207.58 and about 8 hours for a 90-second film [38]. Fix: no unattended multi-agent studios on this project. Use one shot per agent, at most three in parallel, and two revision rounds.
14. **Licence and price drift.** Remotion says its licence changes in version 5.0 [9]. GSAP's licence may be revised, though earlier versions stay usable [15]. Google's pricing page announces changes on 2026-12-01 and 2027-01-01 for Gemini 4 Argon, Gemini 3.8 and 3.6 Flash, the 3.8 TTS models and Robotics ER 2, and names no image or video model among them [65]. Fix: pin versions, keep vendored copies with the licence files, and re-read each page before you upgrade.
15. **Memory on Windows.** Several reports describe the Claude Code process on Windows growing to very large sizes (search results only). One was closed as fixed in version 2.1.74, according to its reporter [53]. Fix: keep most work in the cloud, keep local sessions short, and watch Task Manager in week 1.
16. **Words in her mouth.** Do not clone a voice, do not have an agent sing a relative's words, and do not type new sentences in her handwriting font. Her handwriting may be used only for words she actually wrote [2][1].

## Best references

Eight sources, in the order you should read them. Each was opened on the date shown in the Sources list.

1. **bishpls/animation-pipeline** (https://github.com/bishpls/animation-pipeline) [36]. A real repository of short films made with Claude Code. Read it to see how the parts are organised: parallel builds against one craft guide, resumable renders, and separate audio work.
2. **CRAFT.md from the same repository** (https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md) [37]. The best short list of craft rules for code-made motion. Read the rules on timing: "a raw lerp over time is a bug", hold on twos, and "subtle reads as nothing at 24 fps in a 3-second shot".
3. **scuti.asia, 18-second intro write-up** (https://scuti.asia/?p=23313) [43]. Shows the storyboard, the `seekTo(t)` pattern and the fresh-context critic. Read its warning: "a human must check smoothness and sound".
4. **claude-code-film-studio** (https://github.com/MorShahrezaye/claude-code-film-studio) [38]. The cautionary case. Read the logs yourself: 604 images opened, 0 sounds played, $207.58 spent.
5. **rough.js options wiki** (https://github.com/rough-stuff/rough/wiki) [25]. Read the `seed` option. A seed per shape is what makes the hand-drawn wobble repeat exactly.
6. **HyperFrames** (https://github.com/heygen-com/hyperframes) [22]. An off-the-shelf version of seek-based capture, Apache-2.0. You will compare it with our own harness in experiment E1. Its determinism rules are not yet documented in the pages read [TODO(research)].
7. **Claude Code setup** (https://code.claude.com/docs/en/setup) [46]. Windows install routes, memory requirements, and what sandboxing does and does not support on native Windows.
8. **Claude Code data usage** (https://code.claude.com/docs/en/data-usage) [51]. Read this before any photo goes near a cloud session: retention periods, training settings, and what Remote Control syncs.

Also useful, though not in the top eight: Louise de Sadeleer's note that "the bottleneck shifts from technical skill to taste" [41], and the Remotion licence page [9][10].

## Sources

Project files (read 2026-10-18)
- [1] Life Journey Project Charter, `CHARTER.md`, 2026-10-18. Roles, rubric, principles, constraints, open decisions.
- [2] AI imagery and motion from real photos, `research/ai-imagery.md`, 2026-10-18. Verified privacy terms, label ladder, scanning rules, GPU tiers.
- [3] ArtCraft motion and sound apps as refinement layers, `research/craft-motion.md`, 2026-10-18. FilmCraft, EffectCraft and SoundCraft facts, conform rules, interchange, spike S1.
- [4] ArtCraft visual apps as refinement layers, `research/craft-visual.md`, 2026-10-18. PhotoCraft OpenRaster contract, VectorCraft id contract, control channels.
- [5] Charter review 00, `reviews/00-charter-review.md`, 2026-10-18. Raw-material storage rule.
- [6] Free desktop toolchain and core techniques, `research/toolchain.md`, 2026-10-18. Blender recipes and era grades.
- [7] Delivery format and experience architecture, `research/format.md`, 2026-10-18. Film length, dual master, captions, week-9 slice, hours budget.

Frameworks, licences and techniques
- [9] Remotion LICENSE.md, https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md, read 2026-10-18. Free categories; the licence changes in Remotion 5.0.
- [10] Remotion Company License and pricing, https://www.remotion.pro/license, read 2026-10-18. Per-seat prices as listed on the page.
- [15] GSAP Standard "no charge" License, https://gsap.com/standard-license/, effective 2025-04-30, last modified 2025-05-30. Free including plugins. AI-generated code is not a prohibited use.
- [22] HyperFrames, https://github.com/heygen-com/hyperframes and https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md, read 2026-10-18. Apache-2.0, seek-based capture.
- [24] rough.js, https://github.com/rough-stuff/rough, read 2026-10-18. MIT.
- [25] rough.js options, https://github.com/rough-stuff/rough/wiki, read 2026-10-18. The `seed`, `roughness` and `bowing` options.
- [26] GSAP RoughEase, https://gsap.com/docs/v3/Eases/RoughEase/, read 2026-10-18. The `strength`, `taper`, `clamp` and `randomize` options.
- [28] ambientCG licence, https://docs.ambientcg.com/license/, read 2026-10-18. CC0.
- [29] SIL Open Font License FAQ, https://openfontlicense.org/ofl-faq/, FAQ 1.1-update7, page updated 2026-01-12. Video titling is welcome; the font may not be sold on its own.

Real examples
- [36] bishpls/animation-pipeline, https://github.com/bishpls/animation-pipeline, read 2026-10-18. Films, stack, five parallel subagents.
- [37] bishpls `docs/CRAFT.md`, https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md, read 2026-10-18. Timing, look, review loop, rendering rules.
- [38] claude-code-film-studio (MorShahrezaye), https://github.com/MorShahrezaye/claude-code-film-studio and https://github.com/MorShahrezaye/claude-code-film-studio/tree/main/films/the-multiplane-camera, read 2026-10-18. About 8 hours, 22 agents, $207.58, "nothing was auditioned by ear".
- [41] "How I make custom motion graphics using Claude Code + Remotion" (Louise de Sadeleer), https://louisedesadeleer.substack.com/p/how-i-make-custom-motion-graphics, read 2026-10-18. "The bottleneck shifts from technical skill to taste."
- [43] scuti.asia 18-second intro write-up, https://scuti.asia/?p=23313, read 2026-10-18. Storyboard, build, critic; `window.seekTo(t)`.

Claude Code and environment (docs read 2026-10-18)
- [46] Advanced setup, https://code.claude.com/docs/en/setup. Windows install routes, requirements, sandboxing support.
- [47] Remote Control, https://code.claude.com/docs/en/remote-control. Commands, requirements, limitations.
- [48] Computer use in the CLI, https://code.claude.com/docs/en/computer-use. macOS only.
- [49] Cloud environments, https://code.claude.com/docs/en/cloud-environments. Resources, network levels, network secrets, caching.
- [50] Claude Code on the web, https://code.claude.com/docs/en/claude-code-on-the-web. Cloud sessions, idle pause, limits.
- [51] Data usage, https://code.claude.com/docs/en/data-usage. Retention of 5 years versus 30 days, training, Remote Control sync.
- [53] Windows memory reports, https://github.com/anthropics/claude-code/issues/24840, /issues/42169, /issues/32304, /issues/25545, /issues/33356. Search results only, not opened.

Git, storage and encryption
- [54] GitHub Docs, Git LFS billing, https://docs.github.com/en/billing/concepts/product-billing/git-lfs, read 2026-10-18. Quotas; data packs removed; overage metered. No dollar figures on the page.
- [56] GitHub Docs, About large files, https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github, read 2026-10-18. 50 MiB warning, 100 MiB block, 1 GB guidance.
- [57] GitHub changelog, https://github.blog/changelog/2024-06-03-new-enterprise-accounts-have-metered-billing-for-git-lfs/, 2024-06-03. $0.07 per GiB-month storage and $0.0875 per GiB bandwidth, for new enterprise accounts.
- [59] Backblaze B2 pricing, https://www.backblaze.com/cloud-storage/pricing, read 2026-10-18. $6.95 per TB-month. Footer shows 2024.
- [60] rclone crypt, https://rclone.org/crypt/, read 2026-10-18. Encryption of contents and, by default, names.
- [61] BitLocker overview, https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/, page date 2026-08-24, updated 2026-10-08. Editions; device encryption does not cover USB drives.
- [62] Cryptomator, https://cryptomator.org/, read 2026-10-18. Client-side vaults.
- [63] VeraCrypt, https://veracrypt.io/en/Home.html, read 2026-10-18. Version 1.26.29, 2026-06-09.
- [64] Hetzner Storage Box, https://www.hetzner.com/storage/storage-box/, read 2026-10-18. Protocols and locations; prices not shown on the page.

Generation prices
- [65] Gemini API pricing, https://ai.google.dev/gemini-api/docs/pricing, page updated 2026-10-16. Image and video prices, batch discount, announced increases.
- [66] Replicate pricing, https://replicate.com/pricing, read 2026-10-18 (undated). GPU and per-output rates.

First-hand
- [67] Container measurements M1 to M21, 2026-10-18. Method and numbers are in the research notes, Findings Q3. Scratch files were not kept in the repo.
- [68] EffectCraft v0.11.1 source (read only), https://github.com/storytold/effectcraft, tag `v0.11.1`, read 2026-10-18. Exact CLI syntax for render and template commands.
- [69] winget manifest for Gyan.FFmpeg 9.0.2, https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Gyan/FFmpeg/9.0.2/Gyan.FFmpeg.installer.yaml, read 2026-10-18. Package id and version only; not run on Windows.
- [70] winget manifest for Python.Python.3.13 3.13.15, https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/Python/Python/3/13/3.13.15/Python.Python.3.13.installer.yaml, read 2026-10-18. Package id and version only; not run on Windows.
- [71] winget manifest for Git.Git 2.55.0.5, https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Git/Git/2.55.0.5/Git.Git.installer.yaml, read 2026-10-18. Package id and version only; not run on Windows.

## Changelog

- **2026-10-18, v1.** First draft, written by the Haiku scribe from `research/agent-pipeline.md` (researcher Sonnet, 2026-10-18) and `CHARTER.md`. Not yet reviewed against the rubric.
- **Corrections applied from the research notes:**
  - The project container has Playwright 1.56.1 and Chromium 141 preinstalled (M3). Earlier notes in `research/craft-motion.md` (R8) and `research/ai-imagery.md` said it did not. Corrected here.
  - Headless EEVEE rendered in the container through bpy 5.2.2 (M14). Earlier notes marked it unverified. It is now "works, slow, not yet proven across images".
  - The Gemini 2.5 Flash Image shutdown date (2026-10-02) has passed [65].
  - Spike S1 is still the gate for any Craft command-line use inside the container.
- **Open items (TODO(research)):** the maker's PC specifications; whether a running job keeps the cloud container awake (S4); whether cloud sessions accept image attachments; Remote Control on native Windows; memory of a browser tab and the local CLI; plan usage limits for 19 weeks; GitHub LFS personal rates; which Gemini models change price and whether Veo has a batch discount; prices for external SSDs, Hetzner Storage Box and Replicate editing models (Kontext, Qwen-Image-Edit); Remotion 5.0 licence text; the cause of SVG filter differences; cloud Cycles and EEVEE stability across container images; HyperFrames determinism rules; the Manim apt route; the Windows package IDs for ffmpeg and Python; `rclone` is not installed in the container, so backups run from the PC.
- **2026-10-18, v2 (round-1 review nudges).** Colour chains replaced with the measured Q-F1 lines (the review's "`format=` before `scale=`" sentence was not applied, because the follow-up could not reproduce it); colour-patch validator added; M12 marked "tags verified, matrix not verified, corrected"; Gemini wording corrected (no image or video model named, no batch date forced); `cloud: none` now routes to the PC as `pc-render` instead of stopping the shot; class A renamed "parameterised photo move" with a G4 cap; winget ids added to Step 2; `lj.ps1 doctor` must not print user or machine names.
- **2026-10-18, v3.** Reconciled with DECISIONS.md (2026-10-18): frame rate settled at 24 fps on the Sun 1 Nov settings card (W-14, W-16); runtime 9 or 12 minutes, chapters as 3:00 modules, the 100-second slice and the hours model replace "8 to 12 minutes", "100 seconds a chapter" and "10 hours a week, 190 hours" (W-01, W-02, W-04, W-07); proxy and G5 restated for only-me and one-key-three-guards (D-03, D-04); Decision 11 closed; Decision 12 restated as a mostly public gathering with the venue dated (D-08, W-17); second copy is a second encrypted SSD with no cloud copy, VeraCrypt container (W-25); cloud level and paid-generation guards (D-15, W-23, W-24); hero shots about five in the film (W-34); review is 5 to 10 minutes a production day with markers only (W-42); the example brief and feedback no longer assume a recorded living voice (D-05); gathering from Sun 15 Nov after the L1 lock (D-13); venue file and backup per W-17; true peak -1 dBTP (W-19); Craft boundary and no Launcher (D-12); charter principle number for "finish beats sprawl" corrected to 8 (D-24).
