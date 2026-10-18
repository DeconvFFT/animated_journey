---
name: creator-recipe-library
description: Turns creator recipes from X/Twitter, Reddit, YouTube and blog sources into source-checked, charter-tested recipe cards for the Life Journey project. Use it when an agent must pick, adapt, test, label or reject a photo-motion, same-pose alignment, paper-collage, stop-motion, Minecraft-tour, AI-animation or music recipe, or must judge a creator thread or tutorial before reuse.
---

# Creator Recipe Library

## Purpose

Give Claude agents on the Life Journey project one repeatable way to use creator recipes. The rules come from the charter: real memories stay real, every mechanic must mean something, dignity comes first, and repeatable tools run from the command line. The output is a recipe card that a maker and a team can act on, with its evidence, gaps and gates visible.

## When to use

- A recipe is needed for photo motion, same-pose alignment or morphing, a paper wobble, an editor move, stop-motion, a Minecraft tour, AI image-to-video or music.
- A creator thread, tutorial or tool page must be judged before anyone reuses it.
- A research note has open gaps (TODO(research)) that must be tracked or closed.

## When not to use

- Writing the story, interview questions or gathering plan. Those belong to the story and surprise-ops tracks.
- Building production code for an approved recipe. This skill decides. Implementation comes in a later phase.
- Judging the ArtCraft apps. They have their own tracks: craft-visual and craft-motion.
- Any request to use real family material before the pipeline is locked. The charter forbids it.
- Giving legal conclusions. You may give a reading of a statute, but label it "not legal advice" and name the unknown jurisdiction.

## Reachability (sandbox, verified 2026-10-18)

Check this before any fetch. Do not retry these. Route them to the maker's browser, and cite only what was read.
- `www.reddit.com` and `old.reddit.com`: refused by the fetch tool.
- `x.com`: HTTP 402. `medium.com`: HTTP 403.
- `youtube.com/watch`: redirects to a CAPTCHA. YouTube's oEmbed returns the title and channel only, which shows a video exists, not what it shows.
- `minecraft.net`: HTTP 503 (usage guidelines and store pages).
- Web search: the shared 200-call budget was used up at turn start; siblings in the same turn can exhaust it.

## Procedure

1. Read `CHARTER.md`. Note principle 4 (real memories stay real), principle 5 (dignity and the proxy), and the rule that real photos are gathered only after the pipeline is locked.
2. Read the Summary and the Ranked list in `research/creator-threads.md`. Find the card by its number (C1 to C15).
3. Read the card's evidence tag. [T] means a tool or terms page was read. [L] means it was tested in the sandbox. (M) means judgment. UNVERIFIED means not confirmed.
4. Before you say anything about creator practice, check the Reachability section above and the open-questions list in the note. If the answer is a listed gap, write "not reached" and add a TODO(research) line. Never fill a gap from memory.
5. Check the gates the card depends on: the maker's GPU model, the event's jurisdiction, and the proxy's approval for face work or a hard chapter. If any gate is unknown, set the verdict to hold.
6. Check each tool's status and record it in the card. Install editors and Minecraft helpers only from their official pages, for example Kdenlive [43] and Arnis [56]. Record whether the tool is archived (Microsoft Old Photos [23], FILM [26]), paid-only, telemetry on by default (Eagle Animation [61]), uploads family material (pasteup's Gemini API [60]), or licence limits.
7. If the card has a scriptable part, test it. At the time of the note, the sandbox had CPU only, ffmpeg 6.1.1, Python 3.13, Pillow and numpy, and no GPU. Re-check your own environment. The tested recipes are [64][65][66]. Keep test scripts in a folder the team has agreed on. The runnable scripts are committed at `research/creator-threads-fixtures/` (`align_eyes.py`, `kenburns_xfade.py`, `jitter_twos.py`), with a README.
8. Write or update the card using this template: Source and date; Creator and incentive; Goal; Tools and cost (with the checked date); Steps; Time and cost; Quality (does it look generic?); Charter principles; Free-desktop adaptation; Verdict. Add two scores from 1 to 5: R (relevance to the project) and F (feasibility for a learner plus agents by 2027-02-27).
9. Tag every claim and cite it by its Sources number. Copy each cited source into the document's Sources section. Never cite a URL you have not seen in a fetch or search result.
10. Run the quality bar, then the ethics gate. Set one verdict: adopt, prototype, hold, watch or do not follow.
11. Log the change in the playbook's changelog. Close a TODO(research) only with a source or a test result.

## Checklists

### Judging a creator thread
- [ ] The original post date is found, and the checked date is recorded.
- [ ] The incentive is visible (a course, an app, an affiliate link, a sale) and recorded.
- [ ] It shows the process and at least one failure, not only the result.
- [ ] A paid phone app without a desktop equivalent makes the recipe not reproducible.
- [ ] Reel grammar (beat-synced zooms, whip transitions, trending sounds): harvest the technique, discard the style.
- [ ] Face swap, a synthetic voice or invented scenes: reject.
- [ ] The result is shown on real old photos, not clean modern portraits.

### Before adopting a recipe
- [ ] The source has a date and a checked date.
- [ ] Every claim has a tag and a citation number.
- [ ] The tool is not archived, frozen or blocked as a critical dependency [23][26].
- [ ] The licence was read in full, not just the summary [11][12].
- [ ] Telemetry and upload behaviour were checked and switched off or excluded for family material [60][61].
- [ ] Cost is stated, including any GPU or rental cost, or marked UNVERIFIED [18][19][20].
- [ ] The test was run, or the card says it was not tested.
- [ ] R and F scores are given.

### Ethics gate (before any real family material is used)
- [ ] The maker has confirmed that the pipeline is locked.
- [ ] The chapter is not a hard one, or the proxy has approved it and that is recorded.
- [ ] Face work: the proxy has approved it. No speech or voice is generated [21][22].
- [ ] No family photo goes to a cloud library, a shared device or an uploading tool.
- [ ] Every reconstruction carries a visible label.
- [ ] No event, person or words are invented.
- [ ] Each music licence is saved with its date [11][12].

### Card is complete
- [ ] Steps name the tool and its version.
- [ ] Time and cost are estimated, and marked (M) if they are estimates.
- [ ] At least one failure case or pitfall is listed.
- [ ] Each device has a "why this move" sentence that links it to a principle.

## Quality bar

**Good** (an agent or maker can act on it):
- Names tools, versions and checked dates.
- Numbered steps that can be followed without guessing.
- Test results with numbers, and the limits of the test stated (for example, "synthetic images only" [64]).
- Says what is not known, with TODO(research) lines.
- Links each device to a charter principle and gives a fallback for every step.
- Warns when the result will look generic, and says how to avoid that.

**Mediocre** (rework before use):
- "AI does it", with no tool or settings.
- No date and no version.
- Relies on a summary without saying so.
- Needs a paid app, with no desktop equivalent.
- Says a viral look "works", with no source.

**Reject:**
- No source at all.
- Depends on an archived, paid-only or blocked tool as the critical path.
- Invents a fact, tool, price or URL.
- Breaks an ethics guardrail below.

## Ethics guardrails

- **Real memories.** Restore, restyle, animate and connect only. Do not invent events, people or speech (charter principle 4). Reconstructions must be visibly reconstructions.
- **Invented in-betweens.** First-and-last-frame video creates frames that never existed. Label them or do not use them [19].
- **No face swap.** InsightFace's pretrained models are for non-commercial research only, and its swap models need a licence [22].
- **No synthetic voice of a real person.** Suno's voice models may resemble only the user's own voice [1].
- **Face animation needs the proxy.** LivePortrait-type tools need approval and a visible label. Its authors warn about deepfake misuse [21].
- **Covert gathering.** No cloud photo libraries, shared devices or family group chats (charter).
- **Uploading tools.** Check before use. pasteup sends prompts and images to the Gemini API [60]. Eagle Animation sends telemetry by default; switch it off [61].
- **Music.** Family recording first. Credit library tracks as the licence requires [11][12]. AI music is a scratch track only. Suno's free-plan output is personal and non-commercial [1][5]. The terms do not use the phrase public performance. They bar commercial performing of Output for every tier and require a Download before any commercial use. A non-commercial family screening is therefore not restricted by the terms; a ticketed, sponsored or venue-promoted screening would be. Verified on suno.com/terms 2026-10-18. Not legal advice; jurisdiction unknown [1].
- **Public screening.** The US definition of "publicly" [16] is a reading of a statute, not legal advice. The jurisdiction is unknown.
- **No reel grammar.** Do not copy beat-synced zooms, whip transitions or trending sounds.

## References

- Playbook: `playbooks/creator-threads.md`
- Research notes: `research/creator-threads.md`
- Charter: `CHARTER.md`
- Key URLs, all from the research note's source list:
  - https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/ [27]
  - https://docs.kdenlive.org/en/effects_and_filters/video_effects/transform_distort_perspective/transform.html [39]
  - https://www.replaymod.com/docs/ [53]
  - https://incompetech.com/music/royalty-free/faq.html [11]
  - https://creativecommons.org/licenses/by/4.0/ [12]
  - https://github.com/brick-a-brack/eagle-animation [61]
  - https://docs.comfy.org/tutorials/video/wan/wan2_2 [19]
  - https://github.com/Wan-Video/Wan2.2 [18]

### Sources

- [1] Suno Terms of Service. https://suno.com/terms. Page-dated: revised 2026-08-10, effective 2026-09-03. Free output is personal and non-commercial. No copyright warranty; voice-model limits.
- [5] Suno Help: free plan rights. https://help.suno.com/en/articles/9601601. Undated. Personal and non-commercial; cannot be monetized.
- [11] Incompetech Music FAQ. https://incompetech.com/music/royalty-free/faq.html. Footer dated 2026. Credit wording "Licensed under Creative Commons: By Attribution 4.0"; edits must be disclosed.
- [12] Creative Commons Attribution 4.0 deed. https://creativecommons.org/licenses/by/4.0/. Undated. Adaptation and commercial use allowed, with attribution, a licence link and an indication of changes.
- [16] 17 U.S.C. section 101 (Cornell LII). https://www.law.cornell.edu/uscode/text/17/101. Undated. Definition of "publicly".
- [18] Wan2.2. https://github.com/Wan-Video/Wan2.2. Page-dated 2025-07-28 to 2025-11-13. Apache-2.0; README gives 24 GB for the 5B model and 80 GB for the 14B models.
- [19] ComfyUI Wan 2.2 tutorial. https://docs.comfy.org/tutorials/video/wan/wan2_2. Undated. The 5B model should fit in 8 GB with offloading; first-and-last-frame workflow described.
- [20] WanGP (DeepBeepMeep). https://github.com/deepbeepmeep/Wan2GP. Page-dated v18.17, 15 October 2026. 6 GB for select models.
- [21] LivePortrait (KwaiVGI). https://github.com/KwaiVGI/LivePortrait. Updates to 2025-06-01. Animates a still from a driving video; authors warn of deepfake misuse.
- [22] InsightFace. https://github.com/deepinsight/insightface. Update 2025-11-24. Code MIT; pretrained models for non-commercial research only.
- [23] Bringing Old Photos Back to Life (Microsoft). https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life. Archived 2026-10-03. MIT; academic research use only.
- [26] FILM: Frame Interpolation for Large Motion. https://github.com/google-research/frame-interpolation. Archived 2025-10-14. Apache-2.0; needs an NVIDIA GPU setup.
- [27] Face Alignment with OpenCV and Python (PyImageSearch). https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/. Dated 2017-05-22. Eye-point alignment steps.
- [39] Kdenlive, Transform effect. https://docs.kdenlive.org/en/effects_and_filters/video_effects/transform_distort_perspective/transform.html. Manual 26.08. Position, size, rotation, rotation point, blend modes.
- [43] Kdenlive download. https://kdenlive.org/download/. Undated. Version 26.08.2; Windows installer and standalone.
- [53] Replay Mod documentation. https://www.replaymod.com/docs/. Undated. Recording, keyframes, rendering, shaders.
- [56] Arnis. https://github.com/louis-e/arnis. Copyright 2022-2026. Builds Minecraft worlds from OpenStreetMap; Apache-2.0; official sources are GitHub and arnismc.com only.
- [60] pasteup. https://github.com/tmoody1973/pasteup. Copyright 2026; version 1.1.0. MIT; sends prompts and images to the Gemini image API.
- [61] Eagle Animation. https://github.com/brick-a-brack/eagle-animation. Undated. GPL-3.0; telemetry to PostHog on by default, switchable off in Settings.
- [64] `research/creator-threads-fixtures/align_eyes.py` (committed 2026-10-18). Original run: worst error 1.36 px on three synthetic cases. Same function as research note T1.
- [65] `research/creator-threads-fixtures/kenburns_xfade.py` (Python port of the tested bash, committed 2026-10-18). Original run: 13.0 s, 312 frames, 5.7 s render; the looped-input trap. Research note T3.
- [66] `research/creator-threads-fixtures/jitter_twos.py` (committed 2026-10-18). Original run: 24 of 24 held pairs identical, 23 of 23 pose changes, deterministic for a seed. Research note T4.
