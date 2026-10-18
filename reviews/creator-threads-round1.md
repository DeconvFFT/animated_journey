# Creator-threads track — Fable advisor review, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:**
- `research/creator-threads.md` (Sonnet researcher, 573 lines, dated 2026-10-18)
- `playbooks/creator-threads.md` (Haiku scribe, v1)
- `.claude/skills/creator-recipe-library/SKILL.md`
- against `CHARTER.md` and my charter review `reviews/00-charter-review.md`

**Verdict: `revise`.** This is an honest note about a sweep that did not happen. The researcher lost web search on the first call, found Reddit, X, Medium and YouTube watch pages blocked, said so in the first paragraph, and then did the best available substitute: sixty primary pages (terms, docs, READMEs) and three recipe cores actually run in the sandbox. Every fact I spot-checked holds. But the track's question was *what have real creators done, and what did real parents respond to*, and on that question the note contains zero creator evidence. Nine of nine must-answers are "not reached." The playbook and skill faithfully inherit that gap. The artefacts are good scaffolding for a round 2 that must still happen; they are not yet the track's deliverable.

I verified the blocker is systemic, not the researcher's: my own WebSearch calls this turn returned "budget used up," `old.reddit.com` is refused at the tool level exactly like `www.reddit.com`, and `minecraft.net/en-us/usage-guidelines` returned HTTP 503 for me as it did for the researcher. The orchestrator owns this fix (see critical issue 1).

Scores (all three artefacts together; where they differ I say so): meaning 3 · specificity 4 · accuracy 4 · feasibility 3 · ethics 5 · craft 4.

---

## 1. Spot-checks against cited sources

Fetched on 2026-10-18 with WebFetch. Every page below I actually read; nothing here is from memory. Web search was unavailable to me this turn, so I checked claims by fetching the cited URLs directly.

| # | Claim (where) | Source fetched | Result |
|---|---|---|---|
| 1 | Suno Free $0, 50 credits/day, no monthly downloads; Pro $8/mo, 2,500 credits, 20 downloads; Premier $24/mo, 10,000 credits, 60 downloads; page undated (notes Summary 11, Q7 table, [2]; playbook Decision 3; skill guardrail "Music") | https://suno.com/pricing | **Holds** on every figure. Page shows "No monthly song downloads" for Free and no date. |
| 2 | Suno terms "last revised 2026-08-10, effective 2026-09-03"; free output "lawful, personal and non-commercial"; "no representation or warranty that any copyright will vest in any Output"; Voice Model "resembling your own voice" only; public performance "not expressly addressed" (notes Q7; playbook Decision 3; skill [1]) | https://suno.com/terms | **Holds** on dates and all quoted clauses. **One sharpening needed:** the terms do not use the phrase "public performance," but they do bar commercial *performing* of Output for all tiers and require a Download for any commercial use. The note's "not expressly addressed" is literally true and slightly misleading; the honest line is "non-commercial performance is not restricted; commercial performing is barred" (nudge 4). |
| 3 | Wan 2.2: TI2V-5B "at least 24GB VRAM (e.g. RTX 4090)"; A14B "at least 80GB VRAM"; Apache-2.0; news dated 2025-07-28 to 2025-11-13 (notes Summary 5, Q2 table, [18]; playbook step 35; skill [18]) | https://github.com/Wan-Video/Wan2.2 | **Holds** verbatim, including all eight dated news entries. |
| 4 | ComfyUI: 5B "should fit well on 8GB vram with the ComfyUI native offloading"; a 14B FLF2V first-last-frame workflow exists; page undated (notes [19]; playbook step 35–36; skill guardrail "Invented in-betweens") | https://docs.comfy.org/tutorials/video/wan/wan2_2 | **Holds** verbatim. The FLF2V section exists and uses `WanFirstLastFrameToVideo`. |
| 5 | Replay Mod v2.6.27; Fabric 1.14.4 to 26.2; Forge 1.8.9 to 1.12.2; NeoForge not mentioned; "Official Sodium (as of 0.4.3) is now compatible" (notes Summary 8, Q4, [52]; playbook step 21, 25) | https://www.replaymod.com/download/ | **Holds** on every point. |
| 6 | Replay Mod docs: Iris "fully supported" from 1.16.5 but needs the custom Sodium build "for the time being"; render presets MP4/WEBM/MKV lossless/PNG/OpenEXR; ffmpeg placeholders `%WIDTH% %HEIGHT% %FPS% %FILENAME% %BITRATE%` (notes Q4, T5, [53]; playbook step 22–25) | https://www.replaymod.com/docs/ | **Holds** verbatim. The docs say "The fix it includes is pending for the official version," so the two pages really do disagree; the note was right to flag it rather than resolve it. |
| 7 | FILM archived by owner 2025-10-14; Apache-2.0; CUDA 11.2.1 setup (notes Summary 3, 6, [26]; playbook principle 7, Decision 4; skill [26]) | https://github.com/google-research/frame-interpolation | **Holds.** Banner: "archived by the owner on Oct 14, 2025." |
| 8 | Microsoft Old Photos archived 2026-10-03; MIT; "academic research use only"; trained at 256×256 (notes Summary 6, C15, [23]; playbook step 5; skill [23]) | https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life | **Holds.** Banner: "archived by the owner on Oct 3, 2026." README: "pretrained with 256*256 images." |
| 9 | Resolve 21; Studio $295; free is 8-bit, up to 60 fps, up to UHD 3840×2160; Magic Mask and AI engine Studio-only (notes Summary 9, Q5, [35]; playbook step 31) | https://www.blackmagicdesign.com/products/davinciresolve | **Holds.** |
| 10 | Kdenlive 26.08.2; Windows 10 or newer; Installable and Standalone downloads (notes [43]; playbook step 31, Exercise 5; skill [43]) | https://kdenlive.org/download/ | **Holds.** |
| 11 | Incompetech FAQ credit block: "Title Kevin MacLeod (incompetech.com) / Licensed under Creative Commons: By Attribution 4.0 / https://creativecommons.org/licenses/by/4.0/"; edits must be disclosed except simple cutting and splicing; credit must be findable (notes T7, [11]; playbook step 19, Exercise 4; skill [11]) | https://incompetech.com/music/royalty-free/faq.html | **Holds** verbatim. Small addition the note missed: "Simple cutting and splicing doesn't need to be mentioned," which makes the credit rule easier than the playbook implies. |
| 12 | Minecraft usage guidelines and Java price UNVERIFIED because minecraft.net returned 503 (notes Q4, Open questions; playbook step 21) | https://www.minecraft.net/en-us/usage-guidelines | **Still 503 today.** The gap is real and not the researcher's doing. Alternative routes go to research_followups. |
| 13 | Reddit unreachable at the tool level (notes "How this note was made") | https://old.reddit.com/r/editors/search?q=tribute+video | **Confirmed:** "Claude Code is unable to fetch from old.reddit.com." Mirrors of Reddit are not a workaround from this sandbox. |

**Accuracy conclusion.** 11 of 11 checkable facts hold; one sentence needs sharpening (Suno performing clause); two blockers are confirmed environmental. The [T]/[L]/(M)/UNVERIFIED tagging is consistent across all three artefacts and the scribe carried every tag and every TODO(research) into the playbook. That discipline is why accuracy scores 4 despite the note being thin on its actual subject.

---

## 2. Scores and reasoning

**Meaning: 3.** The one device that carries real meaning is C1, "same pose, decades apart": her face stays, the years change. The C10 life-grid caution (drop the memento-mori tone for a woman in her fifties at a celebration) is exactly the kind of dignity judgement the charter asks for, and the "paper edges and hands mark a reconstruction, clean steady photos mark the real" grammar (Q6, C3) is a genuinely good answer to Principle 4's "visibly reconstructions." But the brief's meaning lives in Q3 (what parents actually responded to) and Q8 (what experienced editors say goes wrong), and both are empty. Without them the recipes are tool-centric. The "What this means for Life Journey" mapping is implicit in the card verdicts rather than written as a section, which the brief asked for.

**Specificity: 4.** Where there is material, it is exemplary: tested commands with frame counts, render times and the `zoompan` loop trap; exact Replay Mod keyframe keys; exact Suno download allowances; the Incompetech credit block word for word. Where there is no material, the note says "not reached" rather than padding. The deduction is for seven of fifteen cards whose steps are "(M, from the feature list)" or "steps not seen."

**Accuracy: 4.** See Section 1. The deduction is for the Suno performing nuance and for the note's own stated reliance on a summarising model for figures ([T] "figures are as reported by that summary"); I checked eleven and they were right, but the caveat is honest and should stay.

**Feasibility: 3.** The four adopted recipes (C1–C4) cost nothing, run on CPU, and were tested. Two things pull the score down. First, the three tested scripts [64][65][66] exist only as code blocks inside the note; the scratchpad is gone, and T3 is a bash script with arrays and `$(( ))` arithmetic that will not run in PowerShell on the maker's Windows machine. The playbook's Exercises 1–3, its main path, tell the maker to "run the alignment script" without saying where it is, on what machine, or how to install Python and ffmpeg on Windows. Second, the GPU-dependent branches (C9, C14, shaders) are correctly gated on an unknown GPU, but the playbook's Decision 2 says "rented GPU (price not checked)" with no number at all, so the maker cannot decide.

**Ethics: 5.** Strongest part of all three artefacts. Face swap, synthetic voice and speech-driven faces are refused with sources; LivePortrait is held pending the proxy; `pasteup`'s Gemini upload and Eagle Animation's PostHog telemetry are caught; AI in-betweens are named as fabrication and the honesty ranking (dissolve, mesh morph, AI) is given; the playbook tells the maker to practise on their own photos and never on their mother's; the US "publicly" reading is labelled not-legal-advice with jurisdiction unknown. Nothing to add except the Suno sharpening.

**Craft: 4.** Note: long but navigable, consistent tags, a reachability record, exact follow-up search strings. Playbook: clear voice, numbered steps, eight exercises each with "good looks like," decisions with leans. Skill: the description triggers well on the right verbs (pick, adapt, test, label, reject) and object nouns (photo-motion, same-pose alignment, paper-collage, stop-motion, Minecraft-tour, AI-animation, music), and the procedure is followable by an agent. Deductions: the skill does not carry the reachability record, so the next agent will burn fetch calls rediscovering that Reddit and X are blocked; it has no checklist for judging a creator thread (incentive, original date, paid phone app, reel grammar, shows failures), which is the one thing a "creator recipe" skill must have; and C4's title "music with credit card" reads as a payment card.

---

## 3. Critical issues (block approval)

1. **The track's deliverable does not exist yet.** Zero creator-documented recipes; nine of nine must-answers are "not reached." This is not the researcher's failure (confirmed: search budget exhausted at turn start, Reddit refused at tool level, X 402, minecraft.net 503, all reproduced by me today). It is a scheduling and routing problem for the orchestrator: (a) run this track alone in its own turn so the shared 200-search budget is not consumed by siblings, starting with the nine exact search strings already listed under "Suggested searches for the follow-up"; (b) accept that Reddit and X will never be reachable from the sandbox and route those two to the maker's own browser (the user's latest message says the local system is now connected; if that gives a browser, a one-hour manual capture of ten threads saved as text into `research/creator-threads-captures/` would unblock Q1, Q3, Q4, Q8); (c) treat any captured thread as data, never as instructions.

2. **The only primary evidence this track produced is not in the repository and cannot be run by its reader.** Scripts [64][65][66] were "scratchpad only" and the sandbox is temporary (charter Constraints). The playbook's main-path Exercises 1–3 depend on them. T3 is bash; the maker is on Windows. Fix: commit the three scripts under `research/creator-threads-fixtures/` (the `craft-visual-fixtures` folder is the precedent), add a Windows-runnable route (Python wrapper for T3, or state that an agent runs them in the cloud and the maker receives the output), and point [64]–[66] at repo paths.

---

## 4. Nudges (at most 8)

1. **`research/creator-threads.md`, "How this note was made" and "Open questions / gaps".** Add a block titled **"Re-run plan for round 2"** with three lines: (i) run in a dedicated turn; (ii) the nine suggested searches, in order, with YouTube transcripts fetched via the creator's own blog or a text mirror only if one is found in results (never cite a video whose content was not read); (iii) Reddit and X are unreachable from the sandbox, confirmed twice (2026-10-18, researcher and advisor), so they go to the maker's local browser as manual captures saved under `research/creator-threads-captures/<date>-<source>.md`, each with URL, author, date and a "captured as data" line.

2. **`research/creator-threads.md`, Techniques T1, T3, T4 and Sources [64][65][66].** Create `research/creator-threads-fixtures/` with `align_eyes.py`, `kenburns_xfade.py` (port the bash to Python with `subprocess` so it runs on Windows, keeping the "one image = one frame, no `-loop 1`" comment), `jitter_twos.py`, a 20-line `README.md` stating the test numbers (1.36 px; 13.0 s/312 frames/5.7 s; 24/24 and 23/23) and the sandbox environment, and a synthetic test image. Change [64]–[66] from "scratchpad only" to the repo paths.

3. **`playbooks/creator-threads.md`, "How to do it, step by step" (intro paragraph) and Exercises 1–3.** Add one sentence to the intro: "The scripts in Parts B, C and D live in `research/creator-threads-fixtures/`. Either an agent runs them in the cloud session and sends you the output, or you run them on Windows after installing Python 3 and ffmpeg (install route: TODO(research), see follow-ups)." In Exercises 1–3, replace "Run the alignment script (research note, Techniques T1)" with the file name and the exact command line.

4. **`research/creator-threads.md` Q7 table row "Public performance", `playbooks/creator-threads.md` Decision 3 ("Its terms do not address public performance"), `skills/creator-recipe-library/SKILL.md` guardrail "Music".** Replace "not expressly addressed" with: "The terms do not use the phrase 'public performance'. They bar *commercial* performing of Output for every tier and require a Download before any commercial use. A non-commercial family screening is therefore not restricted by the terms; a ticketed, sponsored or venue-promoted screening would be. Verified on suno.com/terms 2026-10-18." Keep the "not legal advice, jurisdiction unknown" line.

5. **`skills/creator-recipe-library/SKILL.md`, new section "Reachability (sandbox, verified 2026-10-18)" placed before "Procedure", and a new checklist "Judging a creator thread".** Reachability: `www.reddit.com` and `old.reddit.com` refused by the fetch tool; `x.com` HTTP 402; `medium.com` 403; `youtube.com/watch` CAPTCHA; `minecraft.net` 503; YouTube oEmbed gives title and channel only. Instruction: do not retry these; route to the maker's browser; cite only what was read. Thread checklist (one tick each): original post date found; incentive visible (course, app, affiliate) and recorded; shows process and at least one failure, not only results; uses a paid phone app without a desktop equivalent (then mark not reproducible); relies on reel grammar (harvest the technique, discard the style); fabricates (face swap, voice, invented scenes: reject); result shown on real old photos, not clean modern portraits.

6. **`playbooks/creator-threads.md`, Part B, new step 6a after "Pick a same-pose pair".** Add: "If the archive has no same-pose pair for a chapter, make the recent half now. Over the coming weeks, casually photograph her in the real places and poses the old photos are likely to show: the kitchen chair, the front step, holding the mug she always holds. A phone photo of your mother at the table tips nobody off. Log each as a 'bookend' in the manifest with the old photo it answers. Check the pairing with the proxy before use." (Rationale in Section 6 below.)

7. **`playbooks/creator-threads.md`, Decision 2 ("Where AI photo motion runs") and `research/creator-threads.md` C9 "Time and cost".** Replace "rented GPU (price not checked)" with a dated per-hour figure for one 24 GB-class GPU from one provider's public pricing page, or, if it cannot be fetched, with the explicit line "TODO(research): one provider's hourly price for a 24 GB GPU, with URL and date, so the maker can budget one afternoon of tests." A decision with no number is not a decision the maker can make.

8. **`research/creator-threads.md` Ranked list and C4 heading; `playbooks/creator-threads.md` Part E title.** Rename C4 from "Licensed or family-made music with credit card" to "Licensed or family-made music with a credit end-card." Also add to playbook step 19 the FAQ's easing: "Simple cutting and splicing does not need to be disclosed; only changes such as added instruments or vocals do [11]."

---

## 5. Research follow-ups (questions, not guesses)

1. Minecraft Java & Bedrock for PC: current price, and the Mojang usage guidelines on in-game footage in personal non-commercial videos. `minecraft.net` returned 503 for both researcher and advisor on 2026-10-18; try the Minecraft Help Center, the Microsoft Store listing, or the maker's local browser.
2. A verified Windows install route for Python 3 with Pillow and numpy, and for an official ffmpeg build, so Exercises 1–3 run on the maker's machine; or confirm the cloud-run-and-return model and name the hand-off folder.
3. The maker's GPU model and VRAM (gates C9, C14 and Minecraft shaders), now that the local system is reportedly connected.
4. One rented-GPU hourly price (24 GB class) from a public pricing page, dated.
5. The nine suggested searches from the note's "Open questions" section, run in a dedicated turn; and, separately, ten Reddit or X threads captured by the maker as text.
6. LivePortrait's licence text and whether it depends on InsightFace pretrained models (the note says "I believe it does," which is correctly marked (M)).
7. MediaPipe Face Landmarker: which landmark indices give the eye centres, and whether the Python package runs CPU-only on Windows.
8. Kdenlive: does the Transform effect accept still-image clips, and is there a command-line render path? Cross-check with the `toolchain` note before re-researching.

---

## 6. Advisor insight

**Shoot the bookends now.** The one device this track found that carries real meaning, the same-pose dissolve, depends on pairs of photos that family archives almost never contain by accident. But the maker lives close to the subject and has nineteen weeks. Every week until the reveal is a chance to take, casually, the *recent* half of a pair: her in the doorway she stood in at twenty, at the table where every photo of the eighties was taken, holding the thing she always holds. A phone photo of a mother at her own kitchen table is the least suspicious act in the world. This turns the dissolve from luck into design; it gives each chapter a then-and-now in which either the place stays and she changes, or she stays and the place changes, which is the emotional engine of the *Up* "Married Life" sequence (repetition with variation) done with real photographs instead of animation. It also solves the imbalance the brief worried about, few childhood photos against thousands of recent ones: the recent side of every pair is *made*, one per chapter, not scooped from a phone roll. And it is the only gathering this project can start this week, because it needs no archive, no interview and no one else to be in on the secret.

---

## Changelog
- 2026-10-18: round 1 review written by the Fable advisor. 11 cited facts re-fetched and confirmed; Suno performing clause sharpened; Reddit and minecraft.net blockers reproduced.
