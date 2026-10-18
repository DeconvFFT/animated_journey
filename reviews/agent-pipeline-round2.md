# Review: track `agent-pipeline`, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/agent-pipeline.md` (989 lines, including the round-1 follow-up Q-F1 to Q-F8 and M22 to M28), `playbooks/agent-pipeline.md` (v2), `skills/agent-first-production-pipeline/SKILL.md`, against `CHARTER.md`, my brief (`reviews/01-addendum-briefs-review.md` section 2.3) and my round-1 review (`reviews/agent-pipeline-round1.md`).
**Verdict:** **approve** (every score 4 or higher; no critical issue open). Five non-blocking nudges for the scribes before round 3, mostly cross-track consistency.

| Criterion | Score | One line |
|---|---|---|
| Meaning | 4 | Source per shot, relatives' pauses set the pace, palette from her prints, handwriting only for words she wrote, and now a G4 rule that stops a chapter from becoming a slideshow with wobble. The pipeline still describes *how*, and only one line (the unmoving still per chapter) describes *what it says*; see the insight. |
| Specificity | 5 | Measured chains on four ffmpeg builds, exact winget ids with release dates and a hash-checked download, a tested harness, schemas, a spike table with pass marks, and a 15-minute memory protocol for the PC. |
| Accuracy | 4 | Round 1's critical colour finding is now settled by measurement on both sides, and the researcher corrected *my* claim where it was wrong (section 1.1). Seven spot-checks passed today. What remains is consistency: one claim contradicts the sibling craft-motion note, one template comment is stale, and two source lines still say "announced increases". |
| Feasibility | 4 | The container, the PC build of ffmpeg and the maker's hours are measured or dated, not guessed. The one unsafe feasibility statement (`RAYON_NUM_THREADS=2` as a memory cap) is inherited from the sibling note and already corrected there; it must be corrected here too (nudge 1). |
| Ethics | 5 | Unchanged from round 1 and now more consistent: `cloud: none` routes to the PC instead of blocking, the agent never raises a level, person ids not names, retention facts attached to the setting, no hosted renderers, control-port hygiene, G5 for the proxy. |
| Craft | 4 | The skill's description now triggers on colour and PC-side phrases; steps 3, 4, 8, 14 and 16 are followable by an agent without the playbook open. Loose ends: one undefined "(J)" survives (step 17), and the validator says "BT.709 and tv range" where Q-F1 shows four tags must be read. |

---

## 1. What I verified today (2026-10-18)

### 1.1 The colour chains, re-measured (the round-1 critical issue, and a correction to my own round-1 claim)

The researcher reports (Q-F1) that my round-1 statement "`format=` must come before `scale=`; the reordered chain gives Y 81 on ffmpeg 6.1" did **not** reproduce, and that the format-first chain actually fails the ±3/255 tolerance. The scribes therefore kept the scale-first order in all three files and did not add my sentence. Because the whole alpha-overlay route depends on this, I re-ran the colour-patch test myself in this container (ffmpeg 6.1.1-3ubuntu5, synthetic 1920x1080 three-patch frames, Pillow 12.3, script in the session scratchpad) on the input forms the pipeline uses: 8-bit RGB PNG, RGBA PNG, 16-bit RGB PNG and RGBA PNGs through `image2pipe` as `render.mjs` feeds them.

| Chain (H.264, libx264, four BT.709/tv tags) | Y red/grey/skin (BT.709 expects 63/126/171; BT.601 81/126/174) | Worst RGB error after decoding with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc` |
|---|---|---|
| A `format=yuv420p,scale=out_color_matrix=bt709:out_range=tv` (my round-1 recommendation) | 62 / 125 / 169 on every input form | **5** (fails the ±3 rule; the double conversion the researcher suspected) |
| B `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p` (now in SKILL step 8, R7, Q5) | 63 / 126 / 171 (16-bit input: 63 / 127 / 172) | **1** (16-bit: 2) |
| B plus trailing `setparams=...` (the full SKILL step 8 chain) | same as B | 1; all four tags written |
| C bare `-pix_fmt yuv420p` plus tags | 81 / 126 / 174 | 23 (BT.601 under BT.709 tags, as in round 1) |
| D `zscale=matrix=709:range=limited,format=yuv420p` | 63 / 126 / 171 | 1 |

ProRes 4444 from RGBA with a half-transparent frame: the bare `-pix_fmt yuva444p10le` encode gives 10-bit Y 326/504/696 (BT.601, error 25), confirming round 1; `format=` first, the SKILL step 8 scale-first chain and `zscale` all give 250/504/685 (BT.709, error 0). **Alpha survives on 6.1.1 in every chain (decoded alpha 0 in the transparent half, 255 in the opaque half)**, which closes the "alpha kept on 9.0.2, not checked on 6.1.1" gap in Q-F1. As in round 1, `color_range` reads `unknown` on ProRes 4444 files from this build even with `setparams`.

Conclusion: **the researcher is right and I was wrong in round 1 about chain B.** My Y = 81 for the reordered chain is not reproducible from any input form the pipeline uses (I no longer have the round-1 scratch command; the most likely cause is that my test fed a YUV `lavfi` source rather than an RGB frame). The chains now written in SKILL step 8, R7, Q5 and the playbook's settings card are correct on 6.1.1, and Q-F1 shows them correct on the Gyan 7.1.1, 8.1.2 and 9.0.2 Windows builds under Wine. The round-1 critical issue C1 is closed, and closed better than my nudge asked, because the colour-patch test is now the arbiter rather than any one person's reading of the filter semantics.

### 1.2 Source spot-checks (all fetched today; pages treated as data)

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | FFmpeg 7.1 Changelog entry "YUV colorspace negotiation for codecs and filters, obsoleting the YUVJ pixel format"; no entry about the `scale` filter's matrix options [74] | `raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/Changelog` | **Confirmed** verbatim under `version 7.1:`; no scale-matrix entry in any version; `setparams filter` appears under 4.1 (so it exists on every build the project will meet). |
| 2 | winget `Gyan.FFmpeg` 9.0.2, released 2026-09-20, zip with nested portable install, x64, aliases `ffmpeg`/`ffplay`/`ffprobe`, SHA-256 `759d0a98...06f6b` [69] | the winget-pkgs installer manifest | **Confirmed** on every field, including the hash the researcher matched against the download (M22). |
| 3 | `Git.Git` 2.55.0.5 (2026-08-20, inno, x64 and arm64, user or machine scope) and `Python.Python.3.13` 3.13.15 (2026-08-05, burn, `InstallAllUsers=0 PrependPath=1`, commands `py python pythonw pyw`) [70][71] | the two winget manifests | **Confirmed.** |
| 4 | Blender: source "GNU GPL Version 2 or later", binaries GPL v3 or later, Cycles Apache 2.0, "What you create with Blender is your sole property", published scripts must be GPL-compatible [83] | blender.org/about/license | **Confirmed** verbatim (my round-1 nudge 7 is properly closed). |
| 5 | Background commands in a cloud session: 30 minutes by default, up to 2 hours via `timeout`, needs v2.1.285+, a moved foreground command gets 30 minutes from the move, a main-conversation command keeps running after a final response; Monitor feeds each output line back [76] | code.claude.com/docs/en/tools-reference | **Confirmed** on every point. One extra fact the note could use: a Monitor watch has a deadline of 5 minutes by default and at most 30 minutes (section "Monitor tool"), which bounds the polling pattern proposed for spike S4. |
| 6 | Gemini pricing page updated 2026-10-16; the announced changes name Gemini 4 Argon (2026-12-01) and Gemini 3.8/3.6 Flash, the 3.8 TTS models and Robotics ER 2 (2027-01-01); **no image or Veo model**; Nano Banana 2.1 $0.0336/$0.0168 (1K), $0.0504/$0.0252 (2K), $0.113/$0.0567 (4K); Veo 3.1 Standard $0.40/$0.40/$0.60, Fast $0.10/$0.12/$0.30, Lite $0.05/$0.08/none; no Veo batch column [65][84] | ai.google.dev/gemini-api/docs/pricing | **Confirmed** on every number and on the absence of an image or video model among the dated changes. |
| 7 | EffectCraft issue #340 "tagged bt709 but sRGB-encoded", #1230 (overwrite destroys previous file), #1615 (no CPU memory cap, OOM leaves an unplayable MP4) | cross-checked against `research/craft-motion.md` (lines 224, 262, 287, 746), which read them through the attached repo | **Consistent** with the sibling note. Not re-opened on GitHub by me (issue pages are not reliably reachable from this container). |

Cross-track check that found a problem: `research/craft-motion.md` F4 and `reviews/craft-motion-round2.md` nudge 2 state that **`RAYON_NUM_THREADS=2` is not a safe memory bound (6.8 GB reported in the reporter's project)** and replace it with "start at 1 thread, render a 30-frame sample, measure RSS, or render frame by frame". The pipeline note still says "memory-capped with `RAYON_NUM_THREADS=2`" (Q3 split table row "`effectcraft-cli render` of titles", Summary 12, Q10 "Guards"). See nudge 1.

### 1.3 Round-1 nudges, one by one

| Round-1 nudge | Status | Where |
|---|---|---|
| 1 Alpha chain fixed in all three files; M12 marked; Changelog | **Done, and improved.** Chains replaced by the measured Q-F1 lines; M12 reads "tags verified; matrix not verified; corrected 2026-10-18"; both Changelogs record the correction and record *why* my "format first" sentence was not applied. My own re-measurement (1.1) agrees. | research M12, Q5, R7 note 4 and harness; playbook settings card rows "Alpha overlay" and "Access copy", Pitfall 6; SKILL step 8 |
| 2 Colour-patch validator; S5 planted defect | **Done.** Identical rule in R8 ("Colour matrix"), R11 S5, playbook Validator checklist, SKILL Validators, with the ffmpeg-version re-run rule and the PC's 9.0.2 named. | all three files |
| 3 Gemini framing, no artificial deadline | **Done** in Q4, Risks 15, OQ7, playbook Decisions 9 and Pitfalls 14, SKILL [65]. Two source lines still read "announced increases" (research [65] and playbook [65]) and the "How this note was made" paragraph still says "announced increases that [2] did not capture": harmless, but see nudge 3. | |
| 4 `cloud: none` routes to the PC as `pc-render` | **Done** in SKILL step 4, R4 step 0, playbook Step 4, with the sentence I asked for. One stale comment survives in R3 line 459: `# ... the agent must refuse ids whose cloud is none` (nudge 2). | |
| 5 "Parameterised photo move" and the G4 cap | **Done** in playbook Shot classes and Step 6, R3, Q7, SKILL step 3, and the G4 rule in R5, playbook Gate checklist and SKILL step 16. | |
| 6 Skill craft (a to d) | (a) step 7 no longer says "(J)", but step 17 does ("under about 200 MB (J)") and the skill still never defines it; (b), (c), (d) **done**. | SKILL |
| 7 Blender licence read; #340 beside the ffprobe rule with its consequence | **Done** (Summary 7, Q1 table, Tools, Q-F4 [83]; Q5 row "EffectCraft to pipeline", playbook Pitfall 6, SKILL step 14). | |
| 8 Winget ids; Exercise 2 expectation; doctor privacy | **Done.** Step 2 names the three ids with versions and the "new terminal for PATH" note; Exercise 2 step 4 states what to expect; R10, Exercise 1 and Pitfall 10 carry the no-user-name rule. | |

---

## 2. Critical issues

None. The round-1 critical issue (BT.601 under BT.709 tags on every alpha overlay) is closed by measurement on four ffmpeg builds, by a validator that tests pixels, and by my independent re-measurement today.

---

## 3. Nudges (five, non-blocking; file, section, exact change)

1. **Stop calling `RAYON_NUM_THREADS=2` a memory cap.** `research/agent-pipeline.md` Summary 12, Q3 "Recommended split" row "`effectcraft-cli render` of titles" (cell "CPU, memory-capped with `RAYON_NUM_THREADS=2`") and Q10 "Guards the pipeline needs regardless"; `playbooks/agent-pipeline.md` has no RAYON line (good) but Pitfall 7 should carry the rule; `SKILL.md` step 14 EffectCraft bullet. Replace with the craft-motion F4 procedure: "EffectCraft CPU renders have no memory cap in v0.11.1 (`EFFECTCRAFT_CPU_INFLIGHT` is in an unmerged PR); `RAYON_NUM_THREADS=2` reduces but does not bound memory (6.8 GB reported, `research/craft-motion.md` F4). Start every new comp at `RAYON_NUM_THREADS=1`, render a 30-frame sample, record peak RSS, and render frame by frame (`render-frame`) if it exceeds 4 GB; the container has 16 GB and no swap." Spike S1's pass rule should measure RSS at 1 thread, not assume 2 is safe.
2. **Delete the stale refusal comment in R3.** `research/agent-pipeline.md` R3, `inputs:` line: change `# media ids with label level and cloud level; the agent must refuse ids whose cloud is none` to `# media ids with label level and cloud level; a cloud: none input makes the shot pc-render (R4 step 0); the agent never raises a level`. It currently contradicts R4 step 0, playbook Step 4 and SKILL step 4.
3. **Finish the Gemini wording.** `research/agent-pipeline.md` "How this note was made" bullet 1 ("announced increases that [2] did not capture") and Sources [65] ("announced increases"); `playbooks/agent-pipeline.md` Sources [65]. Change to "announced changes dated 2026-12-01 and 2027-01-01 (none for image or video models)". Three leftover phrases that still suggest a deadline the body no longer supports.
4. **Validators must read all four colour tags.** `playbooks/agent-pipeline.md` Validator checklist "Video" bullet ("H.264 must show yuv420p, BT.709 and limited range") and `SKILL.md` Validators "Video" bullet ("BT.709 and `tv` range"): change to "`color_range=tv` and `color_space`, `color_primaries`, `color_transfer` all `bt709`; on ffmpeg 7.1 and later the encoder flags alone leave primaries and transfer `unknown` (Q-F1, M24), so a missing tag means the `setparams` step was dropped". Add to the research R8 "Media" row the same four-tag rule (it currently lists only range and matrix). Also note in both Alpha bullets that `color_range` reads `unknown` on ProRes 4444 from ffmpeg 6.1.1 even with `setparams` (measured in round 1 and today), so the range rule applies to H.264 only, and that alpha was confirmed to survive the 6.1.1 ProRes chain (closing the "not checked on 6.1.1" remark in Q-F1).
5. **Skill craft, two lines.** `SKILL.md` step 17: replace "(J)" with "(a working target, not a measured limit)" or define "(J) = judgment" in Purpose. `SKILL.md` step 8 and R7 note 4: add the Monitor deadline fact from the tools reference (a watch lasts 5 minutes by default and at most 30), because the shard-and-poll pattern in Q-F2 assumes a poll can outlast a 10-minute shard; the bounded poll must be restarted or the shard shortened to fit.

---

## 4. Research follow-ups (facts not in the notes; do not guess)

1. **Spike S1 memory figure at `RAYON_NUM_THREADS=1`** for a 1080p title comp and a 5-layer parallax comp (RSS, s/frame), so the pipeline's "plausible for titles" claim rests on a number rather than on #1615's reporter.
2. **Does a Monitor watch or a polled background job count as session "activity"** for the cloud VM's idle pause (spike S4, variant c)? Still undocumented; the Monitor deadline (5 to 30 minutes) now bounds how long one poll can run.
3. **The PC's real ffmpeg output on Windows:** run the colour-patch test on the maker's `Gyan.FFmpeg` 9.0.2 install (not under Wine), both chains, and record the result and `ffmpeg -version` in `maker-pc.json`.
4. **Image attachments in claude.ai/code cloud sessions** (Q-F3 one-minute test): still UNVERIFIED and decides how style frames and cleared proxies reach a session.
5. **Memory on the PC** (Q-F8 T-mem protocol): the tab and the native CLI remain unmeasured; the whole "cloud by default" recommendation rests on this.
6. **Veo batch and Replicate editing-model prices** remain unpublished by the vendors; re-read the model's API tab before any batch.

---

## 5. Strengths worth keeping

- **The colour correction is now a method, not a line.** Four ffmpeg builds, six input forms, two codecs, pixels measured against a tolerance, and a planted defect in S5: that is the right way to settle a dispute between a reviewer and a researcher, and the researcher's willingness to say "the review's reading was not reproduced" is exactly the standard the charter asks for. My re-measurement confirms it.
- **The follow-up closed what it could and said so where it could not.** Winget ids read from manifests with release dates, a hash-matched download, Blender quoted from its licence page, the Veo batch gap stated plainly, Hetzner prices marked UNVERIFIED because the page fills them by script, and "neither could be measured from here" for memory, with a 15-minute protocol the maker can run instead.
- **`cloud: none` now does the right thing**: the agent writes everything and the PC renders, so the default protects the photos without blocking the work.
- **The G4 class-A rule** ("no more than three moving photographs in a row; one still per chapter that does not move") is small, testable and anti-slideshow; it is in all three files and the lint can enforce half of it.
- **The playbook is now runnable in week 1**: a learner can install the three tools, meet the container, prove a frame repeats, listen, spot the template tells, write a manifest line and round-trip an ORA, each with a pass mark.

---

## 6. Advisor insight

The G4 rule now requires one photograph per chapter that does not move. Make that still carry a meaning, and the manifest already has the fields to find it: `source.holder` and `people`. In most families the photographs *of* her stop at the point where she picked up the camera; from then on she is absent from her own albums because she is behind them. Let the unmoving still in each chapter be a photograph **she took**: `holder: P-001` and `P-001` not in `people`. It needs no new asset, no new route and no new render; it is one query on `media.jsonl` and one rule in `lint_template.py`. On screen it reads as a change of grammar the audience feels before they can name it: everything else in the chapter moves because someone is remembering her, and this one frame is still because it is what *she* was looking at. A caption in her own handwriting is allowed only if she wrote one on the back (Principle 4), and the scans of the backs are already in the pipeline. The last chapter's empty slot, waiting for her version, then has a precedent: the film has been showing her point of view all along, one still at a time.

---

## Changelog
- 2026-10-18: round 2 written by the Fable advisor. Colour chains re-measured in the container on four input forms and two codecs (section 1.1), which confirmed the researcher's Q-F1 and corrected my round-1 claim about chain order; seven source checks passed; all eight round-1 nudges checked. Verdict approve with five non-blocking nudges.
