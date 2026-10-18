# Review: track `agent-pipeline`, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/agent-pipeline.md` (Sonnet, 2026-10-18, 787 lines), `playbooks/agent-pipeline.md` (Haiku draft v1), `skills/agent-first-production-pipeline/SKILL.md`, against `CHARTER.md` and my brief in `reviews/01-addendum-briefs-review.md` section 2.3.
**Verdict:** **revise** (one critical issue, confirmed by measurement in the container today; accuracy scored 3).

| Criterion | Score | One line |
|---|---|---|
| Meaning | 4 | The pipeline carries her story (source_ref per shot, relatives' pauses set the pace, palette from her prints, handwriting rule), but 60% of shots are still called "templated photo moves" and nothing stops a chapter from becoming a slideshow with wobble. |
| Specificity | 5 | Measured numbers (M1 to M21), exact commands, a tested harness, schemas, a decision table and a spike scope with pass marks. |
| Accuracy | 3 | Twelve spot-checks passed (below). One load-bearing chain is wrong in substance while its tags are right, and the note calls it "verified by ffprobe". One price-change claim is overstated and has become a schedule deadline. |
| Feasibility | 4 | Container and maker time are measured, not guessed. One procedural contradiction would block most real-photo shots in practice (nudge 4). |
| Ethics | 5 | `cloud` levels, retention facts, no voice cloning, handwriting only for words she wrote, proxy gate G5, person ids not names, no hosted renderers, control-port rules. |
| Craft | 4 | Playbook reads well and the exercises teach the right lessons. Skill description triggers on the right phrases and the procedure is followable; a few loose ends (undefined "(J)", S1 as a PC gate, "stop the shot"). |

---

## 1. What I verified today (2026-10-18)

Method: WebFetch of each cited page; `raw.githubusercontent.com` for the EffectCraft CLI source at tag `v0.11.1`; ffmpeg 6.1.1 and ImageMagick 6.9.12 in this container for the colour tests (synthetic 64x64 frames only). Fetched pages were treated as data.

| # | Claim in the notes | Source checked | Result |
|---|---|---|---|
| 1 | GSAP Standard "no charge" licence, effective 2025-04-30, last modified 2025-05-30, plugins included, AI-generated code "is not a Prohibited Use", Webflow may revise and old versions stay usable [15] | gsap.com/standard-license | **Confirmed** word for word. |
| 2 | Remotion free for an individual, for-profits up to 3 employees, non-profits, evaluators; "In Remotion 5.0, the license will slightly change" [9] | raw LICENSE.md on GitHub main | **Confirmed.** |
| 3 | CLI computer use is macOS-only; Windows needs the Desktop app; Pro or Max, claude.ai login, interactive session [48] | code.claude.com/docs/en/computer-use | **Confirmed** ("Computer use in the CLI is not available on Linux or Windows. On Windows, use computer use in Desktop instead"). |
| 4 | Pro/Max retention 5 years with model improvement on, 30 days off; Remote Control transcript stored on Anthropic servers for sync [51] | code.claude.com/docs/en/data-usage | **Confirmed.** |
| 5 | Git LFS: Free and Pro 10 GiB + 10 GiB, Team and Enterprise Cloud 250 GiB, data packs removed, metered overage, no dollar figures on the page [54] | docs.github.com billing page | **Confirmed**, including the absence of prices. |
| 6 | Container ceilings 4 vCPU, 16 GB, 30 GB; default network level Trusted; `*.googleapis.com` on the Trusted allowlist; network secrets do not appear in env or files; setup cached if under about five minutes, cache expires after about seven days [49] | code.claude.com/docs/en/cloud-environments | **Confirmed** on every point. |
| 7 | Remote Control: `claude remote-control`, `--remote-control`/`--rc`, `/remote-control`; Pro, Max, Team, Enterprise; API keys not supported; `--capacity` default 32; resume for about four hours; attachments from phone or browser; transcript stored while connected [47] | code.claude.com/docs/en/remote-control | **Confirmed.** The page lists no Windows restriction, as the note says. |
| 8 | Playwright `recordVideo` defaults to the viewport scaled to fit 800x800; no frame-rate guarantee [31] | playwright.dev/docs/videos | **Confirmed.** |
| 9 | Gemini pricing page updated 2026-10-16; Nano Banana 2.1 $0.0336 / $0.0168 at 1K, $0.0504 / $0.0252 at 2K, $0.113 / $0.0567 at 4K; Flash Image $0.067 / $0.034; Pro Image $0.134 / $0.067, $0.24 / $0.12 at 4K; Veo 3.1 $0.40, Fast $0.10 / $0.12, Lite $0.05 / $0.08; Batch 50%; 2.5 Flash Image shutdown 2026-10-02 [65] | ai.google.dev pricing | **Numbers confirmed.** But the scheduled changes name **Gemini 4 Argon** (2026-12-01) and **Gemini 3.8/3.6 Flash, the 3.8 TTS models and Robotics ER 2** (2027-01-01). **No image or video model is named.** See nudge 3. |
| 10 | `effectcraft-cli render` flags (`--format h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|gif|wav|aiff`, `--prores proxy|lt|standard|hq|4444|4444xq`, `--channels rgb|rgba`, `--template`, `--values`, `--queue`), `bench`, `mcp`, "headless: renders on the CPU unless started with --gpu" [68] | raw `apps/effectcraft-cli/src/main.rs` at `v0.11.1` | **Confirmed**, with one precision: `--gpu` is a global option, not a `render` flag. |
| 11 | Backblaze B2 $6.95 per TB-month, free egress to 3x stored, $0.01 per GB beyond, first 10 GB free, footer 2024 [59] | backblaze.com pricing | **Confirmed.** |
| 12 | Claude Code on Windows: `irm https://claude.ai/install.ps1 \| iex`, CMD and winget routes, Windows 10 1809+, 4 GB+ RAM, Git for Windows optional, sandboxing not supported on native Windows (WSL 2 supported) [46] | code.claude.com/docs/en/setup | **Confirmed.** |

Cross-track consistency also checked: the "2.5 weeks old" Craft claim matches `craft-motion.md` (first commits 2026-10-01/02) and `craft-visual.md` (2026-09-30); issues #1230 and #1615 are cited with content in `craft-motion.md`; PhotoCraft token and VectorCraft/LightCraft "no authentication" match `craft-visual.md`; `make_ora.py` and `check_ids.py` exist in `research/craft-visual-fixtures/`.

### 1.1 The colour test (the critical finding)

The notes rely on ffprobe tags to prove colour correctness (M12, M13, R8, skill validators). Tags say what a file *claims*; they do not say which matrix the encoder *used*. I encoded a pure-red frame with the exact chains in the notes and read back the first luma sample. Reference values for pure red at 8-bit limited range: **Y = 63 with BT.709, Y = 81 with BT.601**.

| Chain (as written in the notes) | ffprobe tags | Measured Y | Verdict |
|---|---|---|---|
| H.264, skill step 8 and R7: `-vf "format=yuv420p,scale=out_color_matrix=bt709:out_range=tv" ... -colorspace bt709 -color_range tv` | yuv420p, tv, bt709 | **62** | Correct (1 LSB off from a double 8-bit conversion). Decodes back as (251, 0, 0). |
| The "obvious" reorder `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p` | yuv420p, tv, bt709 | **81** | **Wrong matrix, right tags.** Decodes back as (255, 23, 0). Reason: in ffmpeg 6.1 the `scale` filter applies its matrix options only on YUV-to-YUV conversions; on RGB input it passes through and `format=` then converts with the BT.601 default. Nobody must "tidy" this line. |
| Plain `-pix_fmt yuv420p` with tags only | yuv420p, tv, bt709 | 81 | Wrong, as expected. |
| **ProRes 4444 alpha, skill step 8, playbook Templates, R7 note 4, M12:** `-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -colorspace bt709 -color_primaries bt709 -color_trc bt709` (no filter) | yuva444p12le, primaries bt709 | **326 (10-bit) = BT.601** | **Wrong.** Every alpha overlay (titles, EffectCraft hand-backs, Route A overlays) would carry BT.601 colours under BT.709 tags, shifted against the opaque Route A and Route B renders composited next to them. M12's "verified by ffprobe" verified the tags only. |
| Fixed alpha chain: `-vf "format=yuva444p10le,scale=out_color_matrix=bt709:out_range=tv"` before the same encoder flags | yuva444p12le | **250 (10-bit) = BT.709** | Correct. `zscale=matrix=709:range=limited,format=...` also gives 62 at 8-bit and is the cleaner single-step conversion (zscale is compiled into this ffmpeg). |

Note also that `-colorspace bt709` on the ProRes stream showed `color_space=unknown` in ffprobe here; the matrix tag in ProRes lives in the frame header and the container atom, so the validator's "bt709 tag" rule would already have failed for 4444 files on this build. Either way, the rule must become a measurement.

---

## 2. Critical issue

**C1. The ProRes 4444 alpha chain encodes with the BT.601 matrix while tagging BT.709, and the validators cannot see it.** Confirmed in the container today (section 1.1). It appears identically in `research/agent-pipeline.md` (Q5 row "Route A capture to editing", R7 note 4, M12, R8 "Alpha"), `playbooks/agent-pipeline.md` (Templates: project settings card and Validator checklist "Alpha") and `skills/agent-first-production-pipeline/SKILL.md` (Procedure step 8; Checklists "Alpha"). Because every title, caption and EffectCraft hand-back travels this route, the error would reach the master and show as a hue shift wherever an overlay sits on a photo. Fix in nudges 1 and 2.

---

## 3. Nudges (eight, each with file, section and change)

1. **Fix the alpha chain in all three files.** `research/agent-pipeline.md` R7 note (4), Q5 row "Route A capture to editing", M12; `playbooks/agent-pipeline.md` Templates (settings card row "Master" note and Validator "Alpha"); `skills/.../SKILL.md` Procedure step 8. Replace the bare `-pix_fmt yuva444p10le` encode with `-vf "format=yuva444p10le,scale=out_color_matrix=bt709:out_range=tv" -c:v prores_ks -profile:v 4444 -colorspace bt709 -color_primaries bt709 -color_trc bt709` (or `zscale=matrix=709:range=limited,format=yuva444p10le`). Add one sentence under the H.264 chain: "`format=` must come before `scale=` here: in ffmpeg 6.1 the matrix options act only on YUV-to-YUV; reordering gives BT.601 under BT.709 tags (measured Y 81 against 62)." Record the correction in the Changelog of the research note and mark M12 as "tags verified; matrix not verified; corrected 2026-10-xx".

2. **Add a colour-patch validator; tags are not evidence.** `research/agent-pipeline.md` R8 (new row "Colour matrix"), R11 spike S5 (new planted defect: "ProRes 4444 or H.264 encoded with BT.601 under BT.709 tags"); `playbooks/agent-pipeline.md` Validator checklist (new bullet); `skills/.../SKILL.md` Checklists → Validators (new bullet). Rule: encode a 3-patch frame (pure red, 50% grey, one skin tone such as (224, 172, 140)) through the same command line as the shot, decode it with the tagged matrix (`scale=in_color_matrix=bt709:in_range=tv` to `rgb24`), and require every channel within ±3/255. Run it once per command-line template, and again whenever ffmpeg's version changes (the PC's ffmpeg will differ from 6.1.1; see research follow-up 1).

3. **Correct the Gemini price-change framing and remove the artificial deadline.** `research/agent-pipeline.md` Q4 first row and Risks 15; `playbooks/agent-pipeline.md` Decisions row 9 and Pitfalls 14; `skills/.../SKILL.md` References, the [65] line. The page (updated 2026-10-16) names Gemini 4 Argon for 2026-12-01 and Gemini 3.8/3.6 Flash, the 3.8 TTS models and Robotics ER 2 for 2027-01-01; it names **no image or video model**. Replace "Run the image batch before 2026-12-01" with "No image or video model is named in the announced changes; re-read the page in the week the batch runs." The current wording pushes a paid generation batch into November, before the covert collection plan (`surprise-ops`) can have delivered cleared photos, which would be the wrong order for Principle 1.

4. **A `cloud: none` input routes to the PC; it does not stop the shot.** `skills/.../SKILL.md` Procedure step 4 ("stop the shot and write the reason"); `research/agent-pipeline.md` R4 step 0 ("any `none` input stops the shot until M changes it"); `playbooks/agent-pipeline.md` Step 4 last sentence. This contradicts the recommended split in Q3 and R0 ("PC for real full-resolution photos, the same scripts, run by the maker or a local agent") and, since the default is `none`, would block the majority of real-photo shots in the written procedure. Change to: "If an input is `cloud: none`, the agent still writes the brief, the script and the expected `render.json`, commits them, and marks the shot `pc-render`; the maker runs `lj.ps1 run <shot>` on the PC and pushes the validator JSON and the preview; only the cloud render is skipped. Raising the level is never the agent's move."

5. **Rename and cap the "templated photo move".** `playbooks/agent-pipeline.md` Templates → Shot classes (class A) and Step 6; `research/agent-pipeline.md` R3 (`class: A # A templated photo move`), Q7 cadence paragraph; `skills/.../SKILL.md` Procedure step 3. Call it a "parameterised photo move" (the lint exists precisely so it is not a template), and add one G4 rule to R5/playbook Gate checklist/skill step 16: "no more than three class-A shots in a row without a held still, a class B/C/D shot, or a voice-only beat; at least one shot per chapter where the photo does not move at all." Sixty percent of a ten-minute film as moving photographs is the slideshow the charter rejects, however varied the wobble.

6. **Skill craft fixes.** `skills/.../SKILL.md`: (a) Procedure step 7, remove "(J)" or define the label in the Purpose paragraph (the skill never explains it); (b) Procedure step 3 and step 14 EffectCraft bullet, say "`craft` in the **container** only after spike S1 passes; on the maker's PC the EffectCraft template route is available once the five-minute test in `craft-motion.md` R7 passes"; (c) description: add the phrases "ProRes 4444 alpha overlay", "BT.709 colour tags" and "lj.ps1" so colour and PC-side questions trigger this skill rather than the toolchain skill; (d) Procedure step 8, state the resume rule explicitly: "a shard job re-run after a reclaim skips frames that exist; never pass `--ffmpeg` to a sharded run".

7. **Two accuracy tidy-ups the scribes should carry.** `research/agent-pipeline.md` Summary 7 and the Tools table ("Blender is GPL (J, not re-read)"): a licence must be read or marked UNVERIFIED like the others; Blender's own licence page takes one fetch. And Q5 row "EffectCraft to pipeline" should cite `craft-motion.md`'s open issue #340 (ProRes 4444 "tagged bt709 but sRGB-encoded") beside the ffprobe rule and state the consequence already drawn there: prefer the RGBA PNG sequence from EffectCraft, use 4444 only when the colour-patch test (nudge 2) passes. Mirror in `playbooks/agent-pipeline.md` Pitfalls 6 and `skills/.../SKILL.md` step 14 (EffectCraft bullet: "RGBA PNG sequence preferred; ProRes 4444 only after the patch test").

8. **Make the maker's week-1 steps runnable.** `playbooks/agent-pipeline.md` Step 2 and Exercise 2: Step 2 sends the maker to install Git, ffmpeg and Python but marks the package names TODO; either name verified winget ids (research follow-up 1) or replace with "the agent will give you a checked install list in `pipeline/win/README`" so a learner is not left guessing. Exercise 2 step 4 should say what to expect ("the session shows as paused; files are there; any job that was running is gone") so the maker learns the S4 lesson by observation. Also, in R10 and the playbook, note that `lj.ps1 doctor` output must not contain the PC's user name or machine name if the repo name must look harmless (Pitfall 10 applies to `maker-pc.json` too).

---

## 4. Research follow-ups (facts not in the notes; do not guess)

1. Windows install list with verified package ids (winget: ffmpeg, Python 3.13, Git for Windows) and which ffmpeg major version they install; then re-run the colour-patch test on the PC build, because ffmpeg 7.x changed colour negotiation in the `scale` filter and the "format first" trick may behave differently there.
2. Does a running background job keep a cloud VM awake (spike S4 as scoped)? Not in the docs read.
3. Do claude.ai/code cloud sessions accept image attachments (Remote Control does; cloud not stated)?
4. Blender's licence text (GPL-2.0-or-later) from blender.org, for the Tools table.
5. Veo batch pricing and Replicate prices for the editing models that matter (Kontext, Qwen-Image-Edit), both absent from the pages read.
6. Whether `cdn.playwright.dev` is blocked from the container (HTTP 400 seen) or was a transient; it decides whether Playwright can ever be upgraded past 1.56.x in the container.
7. Hetzner Storage Box monthly prices (blank on the fetched page) if the European-location option matters to the family.
8. A measured memory figure for the claude.ai/code browser tab and for a short native Claude Code CLI session on Windows, since the maker's constraint is memory and both are currently unmeasured.

---

## 5. Strengths worth keeping

- The container is measured, not assumed (M1 to M21), and the harness in R7 was actually run: shards, resume and a cross-process identity check. That is the first piece of this project that is code-proven rather than read-proven.
- The frame-accuracy ladder (seek capture, renderer-owned stepping, faked clock, free-running rAF, screen capture) is the right mental model and is backed by measurements, including the honest filter-nondeterminism finding.
- Honesty about evidence: "no multi-minute, emotionally paced film made by a coding agent, and no family tribute" is stated in the summary, the playbook and the skill, and the cautionary case (604 images opened, 0 sounds played) becomes a rule: a person listens.
- The `cloud` field (`none`/`preview`/`full`) with the retention facts attached to it, the person-id rule, the handwriting rule (only words she wrote), and the control-port hygiene are exactly the ethics the charter asks for, written as procedure rather than sentiment.
- Licences were read, dated and are correct on every point I checked; vendoring GSAP and rough.js so the film builds in 2046 is the right instinct.
- The everyday loop (R4), the shot brief (R3), the comment file (R6) and the gate checklist (R5) are ready to be used by both humans and agents, and the playbook's seven exercises teach the five lessons that matter (determinism, baked textures, listening, the template tells, the manifest).

---

## 6. Advisor insight

The track's core property, "a frame is a pure function of `t`", is being used only to render a film. It is also the cheapest way to settle the charter's open format question (film, explorable, or hybrid) without choosing. Every Route A scene already has `seekTo(t)`; Route B shots are clips with known in and out points. The same chapter source can therefore be emitted twice from one timeline spec: the linear ProRes master for the room on Feb 27, and an **offline, seekable page on the USB stick she takes home**, where the only control is her own hand on a scrubber shaped like the photo strip of that chapter, with the relatives' voices playing at whatever pace she drags. No new assets, no new renders: the page loads the same vendored scene code and the same encoded clips, and the "gift after the gift" (the empty last chapter waiting for her version) becomes a place she can literally stop and stay. The film is what the family gives her; the scrubber is what lets her give herself time. It costs the pipeline one extra emitter and one rule: Route A scenes must stay light enough to seek in a browser on the PC in real time, which the S2 fps numbers already measure.

---

## Changelog
- 2026-10-18: round 1 written by the Fable advisor. Twelve claims verified online and in the container; one critical finding (BT.601 under BT.709 tags on the alpha chain) measured directly.
