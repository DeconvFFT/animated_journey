# Toolchain track — Fable advisor review, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:**
- `research/toolchain.md` (Sonnet researcher, 636 lines, dated 2026-10-18)
- `playbooks/toolchain.md` (Haiku scribe, draft v0.1)
- `.claude/skills/free-creative-toolchain/SKILL.md`
- against `CHARTER.md` and my charter review `reviews/00-charter-review.md`

**Verdict: `revise`.** This is the strongest research note I expect to see in Phase 0: the researcher ran the commands instead of quoting feature lists, flagged every unverified claim, and all twelve facts I spot-checked held. The revisions are not about the facts. They are about three things the artefacts inherited from a brief written before the charter was updated: the maker is on **Windows**, the piece is a **surprise**, and the charter's production approach is **"agents generate, ArtCraft apps refine, free tools are the proven fallback."** None of the three documents has fully absorbed those facts yet, and one line in the skill would, if an agent followed it literally, blow the surprise.

Scores (all three artefacts together; where they differ I say so): meaning 4 · specificity 5 · accuracy 4 · feasibility 3 · ethics 4 · craft 4.

---

## 1. Spot-checks against cited sources

Fetched on 2026-10-18 with WebFetch. Every page below I actually read; nothing here is from memory.

| # | Claim (where) | Source fetched | Result |
|---|---|---|---|
| 1 | Resolve Free = 8-bit, up to 60 fps, up to UHD 3840×2160; Studio $295; Studio adds 10-bit/120 fps/32K, multi-GPU, hardware H.264/H.265, Neural Engine, noise reduction, film grain, "remote scripting API" (notes Summary 3, Q1; playbook Decision 1) | https://www.blackmagicdesign.com/products/davinciresolve/studio | **Holds.** $295 "excludes sales tax and shipping"; free edition "up to 60 fps", "up to Ultra HD, 3840 x 2160", 8-bit; Studio lists "remote scripting API", AI UltraNR, Film Look Creator grain, hardware H.264/H.265. Current version shown: 21. One nuance: the Studio page lists *advanced* HDR grading, Dolby Vision and HDR10+ as Studio; the notes' Summary 3 says Free "includes … HDR grading". Qualify (nudge 8). |
| 2 | Resolve scripting README: API is a "common superset for both the Free and Studio versions"; Studio-only calls fail in Free; `-nogui` headless; `ImportTimelineFromFile` formats; "Last Updated 24 Jul 2026" (notes Summary 4, Q1, Q2) | https://gist.githubusercontent.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8/raw (two reads, the superset sentence is past character 100,000) | **Holds**, exact wording: "The DaVinci Resolve scripting APIs cover a common superset of functions for both the Free and Studio versions"; "-nogui"; "(AAF/EDL/XML/FCPXML/DRT/ADL/OTIO)"; "Last Updated: 24 Jul 2026". The README's own preamble says it introduces the API "for DaVinci Resolve Studio", which supports the notes' cautious "best reading" that external scripting is Studio territory. Still **[UNVERIFIED]** on a real Free install, as the notes say. |
| 3 | Blender minimum 4 cores/8 GB/2 GB VRAM, OpenGL 4.3 / Vulkan 1.3; Blender 5.0+ needs Apple Silicon; 4.5 LTS last Intel release; pen tablets recommended for Grease Pencil (notes Summary 15, Q9; playbook Step 0, Pitfalls; skill Checklist A) | https://www.blender.org/download/requirements/ | **Holds** verbatim: "4 cores with SSE4.2 support", "8 GB", "2 GB VRAM with OpenGL 4.3, Vulkan 1.3"; "Blender 5.0 and later require Apple Silicon"; "Blender 4.5 LTS is the last release to support Intel". |
| 4 | Blender 5.2 LTS released 2026-07-14; 5.1 2026-03-17; 5.0 2025-11-18; 4.5 LTS 2025-07-15 (notes [24]; the "pin 5.2 LTS" recommendation) | https://www.blender.org/download/releases/ | **Holds** on all four dates. 5.2 is the newest LTS listed. |
| 5 | Suno terms revised 2026-08-10, effective 2026-09-03; free/basic outputs "lawful, personal and non-commercial"; Suno assigns rights only to paid tiers; "no representation … that any copyright will vest"; commercial use needs a download (notes Summary 13, Q7; playbook Decision 6) | https://suno.com/terms | **Holds** verbatim on every point, including "You may not commercially exploit Output that has not been downloaded by you." One precision: the free-tier clause restricts *use*; it does not literally say "assigns no ownership" (that is the correct inference from the paid-tier assignment clause). Fine as written. |
| 6 | Library of Congress RFS: file-based video preference order IMF, FFV1 v3 (RFC 9043) in Matroska, ProRes 4444 XQ/4444/422 HQ in QuickTime, MPEG-2, XDCAM; MP4 is a "viewing proxy" (notes Summary 10, Q6; playbook Step 12 and Best references 8) | https://www.loc.gov/preservation/resources/rfs/moving.html | **Holds** on order and wording ("Viewing proxy such as MPEG-4 (.mp4)"). **Does not hold:** the page shows **no edition year**, so "RFS 2025-2026" in [92] and the playbook is unsupported by the cited page (nudge 8). |
| 7 | incompetech: CC BY 4.0; three-line credit format; "live productions: Yes. Be sure to credit me"; monetised YouTube yes; "something else? Probably" (notes Q7; playbook Decision 6; skill Checklist C) | https://incompetech.com/music/royalty-free/faq.html | **Holds** verbatim, including the credit block. The FAQ adds that credits for live productions go in the programme or are announced by voice; the end-credits advice in the notes is consistent. |
| 8 | Depth Anything V2: Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0 (notes Q3; playbook Step 5; skill step 7) | https://raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md | **Holds** verbatim. Giant checkpoint is "Coming soon". |
| 9 | Kdenlive 26.08.2; Windows 10+, macOS 13+, AppImage/Flatpak (notes [8]; playbook Decision 1) | https://kdenlive.org/download/ | **Holds.** Release date is not on the download page (the notes attribute 2026-10-13 to the News page [9], which I did not re-fetch). |
| 10 | Sonniss GDC bundles: royalty-free, commercial use, no attribution, no resale as SFX, no AI/ML training, latest bundle GDC 2024, no 2025 bundle (notes Q7; skill Checklist C) | https://sonniss.com/gameaudiogdc/ | **Holds** verbatim: "Use for AI/ML training is strictly prohibited". The full licence is on a separate page the researcher did not cite; the summary page suffices for our use. |
| 11 | MagicaVoxel 0.99.7.2 of 2025-07-12; Windows/Mac only; "free to use for any project", no redistribution; no external CLI, in-app console only (notes Summary 9, Q2, Q5; playbook Decision 3) | https://ephtracy.github.io/mv_main.html | **Holds** on all points. The page labels the download "Beta". |
| 12 | Blender 5.2 LTS as the pinned version is still the newest LTS (feasibility of "do not upgrade mid-build") | same as #4 | **Holds.** The next LTS on the historical cadence would land around July 2027, after our deadline, so pinning 5.2 carries no risk of a forced upgrade. |

**Accuracy conclusion.** 12 of 12 facts check out; two citations need tightening (LoC edition year; HDR in Free). The [RUN]/[DOC]/[UNVERIFIED] flag system is exactly what the charter's Accuracy criterion asks for, and the scribe carried the flags into the playbook and skill. This is the standard every other track should be held to.

---

## 2. Scores and reasoning

### Meaning — 4
The notes and playbook tie every tool choice back to a charter principle (scriptable tools, real memories stay real, privacy, surprise) and the playbook's opening paragraph is the right one ("the kitchen table, the drive to work, the song she sang badly on purpose"). Two gaps keep it from 5:
- **Era looks are decade-generic.** Step 9 / Exercise 7 / R7 build "a 1970s look" and "a 1950s black-and-white look". My charter review (2.3, Q4) warned that era signalling tips into pastiche. Her albums have their *own* fade, cast and grain, and that is the texture Principle 3 asks for. See nudge 5.
- **The charter's production approach is absent.** The charter says agents generate, the ArtCraft apps refine, and free tools are the proven fallback. The playbook presents Kdenlive and GIMP as the editor and raster tool "of record" without saying that they are the fallback layer the charter requires, and without naming the hand-off formats the ArtCraft layer will need. See nudge 4.

### Specificity — 5
Exact commands, exact versions, measured timings (66 s for 50 frames, 1.9 s for 48 SVG frames, 8 s for a voxel still), measured traps (18 % stretch, 720×576 default, AgX desaturation, Z-up vs Y-up, `pathLength` ignored, SVG scale 0.000282 m/px). The tool matrix has the Scriptability column the brief demanded, graded A to W, with the exact entry point. The ten exercises each have an output file and a numeric self-check. Nothing to add.

### Accuracy — 4
See Section 1. Deductions: [92] carries an edition year the page does not show; Summary 3 implies HDR grading is in Free while the Studio page lists advanced HDR/Dolby Vision as Studio; the skill cites [90] (Meta AudioCraft README) for "no invented … voices", which that README does not say. All three are one-line fixes (nudge 8). The research honestly records that the search budget was exhausted and that YouTube rate-limited it, which is why the tutorial section is thin; that honesty is worth more than a padded tutorial list.

### Feasibility — 3 (playbook 3, notes 4, skill 3)
This is where the revision is needed.
- **Windows.** The charter now says the maker is on a Windows PC. Every recipe was run on Ubuntu; every self-check is written in bash (`identify -format '%f %wx%h\n'`, `for f in frames/f_*.svg`, `sha256sum -c`, `xvfb-run`). Exercise 1 cannot be completed as written in PowerShell. My charter review set the usability bar for a playbook as "the maker can do the first exercise within an hour of reading"; today they cannot. The playbook knows this (Step 0 "Shell warning", TODO list) but defers it. It should decide (nudge 2).
- **Where real photos get processed is a TODO.** Decision 5 leaves cloud-versus-local open. It is the central architecture question for "agents generate" on a memory-constrained PC, and it collides with the privacy constraint. There is a clean rule available that resolves both (nudge 3).
- **Blender for a learner in 19 weeks.** The stack is admirably narrow (three tools plus glue), but Blender is the steep one and the `blender` binary itself was never run, only `bpy`. The playbook's lean (Blender for three or four hero moves, editor keyframes for the rest) is right; the fallback should be stated as the *default* until Exercise 5 proves the maker's machine can do it.
- **Pace.** Ten exercises at two a week end on 2026-11-22 (week 5). My charter schedule closes Learn at week 4 and starts the vertical slice in week 5, and the Gather workstream competes for the same evenings. Twenty hours of exercises fit in three weeks at three or four a week; recommend compressing so that Exercise 10 (the mini-chapter) lands by 2026-11-08 and becomes the dress rehearsal for the vertical slice. Not a nudge, a scheduling note for the orchestrator.

### Ethics — 4
Very strong: originals untouched, every pixel-changing step logged, reconstructions labelled, no synthetic voices, music licences read not assumed, Photopea's claim labelled as a vendor claim, "surprise leaks" pitfall with concrete habits (no render notification in the family chat, neutral file names). The deduction is one sentence in the skill's Ethics guardrails: *"Consent: each living person shown agrees before the cut uses them."* The subject is a living person who is shown in every shot and who must not be asked. An agent following the skill literally either blocks or asks. The charter's proxy mechanism must be written into the skill (nudge 1). This is the one item I count as critical on ethics grounds.

### Craft / usability — 4
- **Research notes (5).** A scribe wrote a playbook from them without re-reading sources, which is the test. Recipes are reproducible. The evidence flags are a model.
- **Playbook (4).** Clear voice, right order, decisions separated from steps, TODOs collected at the end. It would be a 5 once the Windows forms exist and the recipes are files rather than pointers into a 636-line note.
- **Skill (3).** The description triggers well: it names the concrete shot types (Ken Burns, parallax, SVG line reveal, voxel object, era grade, loudness, captions, exports) and has an explicit "do not use" clause, so routing is unambiguous. The procedure, however, is 18 linear steps mixing once-per-project setup (1 to 4), per-shot work (5 to 12) and per-delivery work (13 to 17); an agent asked only to "burn in captions" has to read all 18 to find step 14. The probe example in step 3, `dir(bpy.context.scene.sequence_editor)`, returns `dir(None)` on a fresh scene (R8 itself calls `sequence_editor_create()` first). The recipes it depends on (R1 to R9) exist only inside the research note, not as files the agent can run; the researcher's own notes warn the sandbox copies are lost. The 45-entry Sources block makes the skill long for what an agent needs at run time. See nudges 6 and 7.

---

## 3. Critical issues (block approval)

1. **Skill consent line conflicts with the surprise.** `skills/free-creative-toolchain/SKILL.md`, Ethics guardrails, "Consent" bullet. As written it requires the subject's agreement. Fix per nudge 1.
2. **Playbook is not executable on the maker's stated platform.** `playbooks/toolchain.md`, Step 0 "Shell warning" and Exercises 1, 2, 6, 10: the charter says Windows; all commands and self-checks are bash-only and untested there, so the first exercise cannot be done within an hour of reading. Fix per nudge 2; facts needed are in Research follow-ups 1 to 3.

Everything else below is a nudge, not a blocker.

---

## 4. Nudges (at most 8; file, section, exact change)

1. **`skills/free-creative-toolchain/SKILL.md` → Ethics guardrails → "Consent" bullet.** Replace with: *"Consent: every living person shown, other than the subject, agrees before the cut uses them. The subject cannot be asked (the piece is a surprise); her trusted proxy decides for her, and chapters on loss, illness, separation, money or conflict go to the proxy before any shot is built [1]."* Add to "Stop and escalate": *"Any step that would require asking the subject, or that would surface the project on a device, library or chat she can see."*

2. **`playbooks/toolchain.md` → Step 0 "Shell warning" and Exercises 1, 2, 6, 10 self-checks.** The charter states Windows, so stop treating the OS as unknown. Make the shell a numbered decision ("Decision 0: which shell") with two options and a lean: (a) Git Bash or WSL2 so the tested Unix recipes run unchanged; (b) native PowerShell with rewritten recipes. For whichever is chosen, give the four self-checks that are currently bash-only a stated equivalent: the `identify` loop (PowerShell `Get-ChildItem | ForEach-Object { magick identify -format ... }`), the R3 frame loop, and `sha256sum -c` (PowerShell `Get-FileHash -Algorithm SHA256`). Mark each `TODO(verify on the maker's PC)` until run. Carry the same note into SKILL.md step 4.

3. **`playbooks/toolchain.md` → Decision 5 "Where do heavy renders run?"** Replace the TODO with a rule and a lean: *"Scripts travel, photos don't."* Agents write and test every script in the cloud on stock or synthetic images; the identical script then runs on the maker's PC against the real photos, from a terminal with the Claude desktop app closed (the memory problem the charter records is the app, not ffmpeg or Blender; overnight CLI renders do not need the app running). Cloud rendering of real photos happens only after the maker's explicit decision for a named batch, and never for the raw scans. Mirror the rule in SKILL.md Checklist E.

4. **`playbooks/toolchain.md` → Decision 1 and Decision 4.** Add a line to each that restates the charter's production approach: the ArtCraft apps (FilmCraft, PhotoCraft) are the maker's refinement layer, these free tools are the *proven fallback* the charter requires, and nothing critical may depend on an alpha app. Then add one sentence on hand-off: *"Every output of this track is a PNG sequence with alpha, an MP4, an SRT or a plain SVG, so either the ArtCraft layer or the fallback can take it; the exact import formats are the craft-visual and craft-motion tracks' job."* Add the same hand-off sentence to SKILL.md step 8.

5. **`playbooks/toolchain.md` → Step 9 "Give each decade its own look" and Exercise 7; `research/toolchain.md` → R7.** Change the unit from "decade" to "album". Procedure: pick three prints from one of her real albums (after the pipeline is locked), sample a known-white object and a skin midtone in each, derive the lift, cast and grain *from those samples*, and save that as the look for every photo from that album. Keep the generic 1970s/1950s chains in R7 as practice material only, labelled "stock practice, not for the film". Name the saved looks after her chapters, not after decades. This is Principle 3 (texture) applied to colour and it is the cheapest guard against pastiche.

6. **`skills/free-creative-toolchain/SKILL.md` → Procedure.** (a) Add a five-row routing table at the top: *request → steps* (new shot → 5 to 12; captions → 14; export or stick test → 15 to 16; archive → 17; "which tool?" → Checklist A). (b) Group the 18 steps under three headings: "Once per project" (1 to 4), "Per shot" (5 to 12), "Per delivery" (13 to 18). (c) Fix the step 3 probe example to `dir(bpy.context.scene.sequence_editor_create())` or `[s for s in dir(bpy.context.scene) if 'seq' in s]`, since `sequence_editor` is `None` on a fresh scene. (d) Move the 45-entry "Sources cited in this skill" block into `skills/free-creative-toolchain/references.md` and keep only the eight Key URLs in the skill body.

7. **`research/toolchain.md` → Exemplars / recipes R1 to R9; `skills/free-creative-toolchain/SKILL.md` → References.** Extract each recipe into a runnable file under `skills/free-creative-toolchain/recipes/` (`r1_kenburns.sh`, `r2_parallax.py`, `r3_linedraw.py`, `r4_photo2vox.py`, `r4_render_voxel.py`, `r5_story.mlt`, `r7_era_looks.txt`, `r8_vse_xfade.py`, `r9_deliver.sh`), each with a header naming the tool versions it ran on and the date. Point the skill and the playbook at the files, not at "recipe R2 in the research notes". The research itself says the sandbox copies are lost; the repo copy is the only one that survives.

8. **Three accuracy fixes.** (a) `SKILL.md` → Ethics guardrails → "No invented events, faces or voices [1][90]": drop [90]; the AudioCraft README says nothing about voices; cite [1] alone or add the charter review's voice sentence. (b) `research/toolchain.md` [92] and `playbooks/toolchain.md` Step 12 archive row and Best references 8: the LoC page shows no edition year; write "current Recommended Formats Statement (undated on the page, read 2026-10-18)" or name the page where "2025-2026" was read. (c) `research/toolchain.md` Summary 3 and Q1 row: qualify "includes … HDR grading" to "basic HDR grading; Dolby Vision, HDR10+ and advanced HDR tools are Studio", per the Studio page.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. Does the Kdenlive **Windows** installer ship `melt.exe`, and can it be called from PowerShell or Git Bash with `-profile atsc_1080p_25` and the `avformat` consumer? If not, what is the Windows route to the MLT engine (standalone MLT build, or Shotcut's bundled `melt`)?
2. Does `pip install bpy` for Blender 5.2 publish a **Windows** wheel, for which Python versions, and does `blender.exe -b -P script.py` run R2 within 8 GB of RAM? Measure seconds per frame at 640×360 and 1920×1080 on the maker's actual PC once Step 0 returns.
3. Which shell will the maker use (PowerShell, Git Bash, WSL2), and does WSL2 fit the memory budget on the maker's machine alongside the Craft apps?
4. On a real **Resolve 21 Free** install: does `Preferences > System > General > External scripting using` exist and accept "Local"; do subtitle tracks and caption export work in Free; what is Blackmagic's stated hardware floor (the configuration guide was not read)?
5. **ArtCraft hand-off formats** (owned by craft-visual and craft-motion, but this track needs the answer): do FilmCraft and PhotoCraft import PNG sequences with alpha, MP4 (H.264), SRT and plain SVG, and what do they export? Is there a CLI or project-file format an agent can write?
6. Can the Windows build of Kdenlive's speech-to-text download and run the Whisper model offline, and which model sizes fit in 8 GB of RAM?
7. Still open from the notes and worth a slow re-fetch of channel listings: one verified, current (2025 or later) video tutorial each for Ken Burns in Kdenlive, photo-layer parallax in Blender, and SVG line-draw in Blender, with upload date and software version read from the video page.
8. Music: Mixkit terms (pop-up), Pixabay's Content ID clause, Musopen and Zapsplat licences, and whether a Suno paid-tier output may be shown at a public, non-commercial premiere. Flag all with the date read.

---

## 6. Strengths (keep these)

- **Verification by running, not by reading.** Seven tools proven headless with timings, and the [RUN]/[DOC]/[UNVERIFIED] flags carried faithfully into the playbook and skill. Every other track should adopt this legend.
- **Traps found the hard way and written down**: the 18 % `zoompan` stretch, `melt`'s 720×576 default, AgX desaturation, Y-up/Z-up, `pathLength` ignored by librsvg, SVG import scale, five Blender 5.2 API drifts. These will save the maker days.
- **A genuinely narrow stack** (Blender, Inkscape, one editor, ffmpeg and ImageMagick) with everything else explicitly parked. The brief's "tool sprawl" watch-out was heard.
- **Delivery engineering is complete**: three export profiles with tested commands, FAT32 arithmetic, burn-in captions with sidecar, LoC-grade archive package with checksums, and "rehearse on the real screen" repeated where it matters.
- **Music licences read, not assumed**, with the person's favourite songs handled honestly (sync and master licences, substitute or own performance, informed-risk private viewing).
- **Surprise-awareness in the playbook**: neutral file names, no render notifications in the family chat, a test viewer who would not mention it to her.
- **The ethics section treats inpainting, colourising, upscaling and voxelising as reconstructions**, which is exactly the charter's Principle 4 made operational.

---

## 7. Advisor insight

The parallax pipeline gives us a mechanic nobody will notice as a mechanic, and it can carry meaning. Every 2.5D shot forces one decision: which part of the photo is the foreground layer. Do not let depth decide it. Before cutting each photo, ask the relative who gave it one question: *"What is the first thing Mum would point at in this picture?"* Cut *that* out as the foreground, whether it is a child, a teapot, a coat she loved or a dog in the corner, and let the camera move so that it leads. The parallax then encodes her attention, not the geometry of the scene, and across fifty photos the film quietly shows the audience what she looks at in her own life. It costs one question per photo, it uses a pipeline we already have, and it passes the Principle 2 test: it would be a different film for anyone else.

---

## Changelog
- 2026-10-18: round 1 review written by the Fable advisor after reading all three artefacts and spot-checking twelve claims against their cited pages.
