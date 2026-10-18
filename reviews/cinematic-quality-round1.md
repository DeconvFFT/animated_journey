# cinematic-quality — round 1 review (Fable advisor)

**Date:** Sunday 2026-10-18 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `research/cinematic-quality.md` (886 lines, 85 sources, 7 measurements), `playbooks/cinematic-quality.md` (v1), `skills/cinematic-quality-bar/SKILL.md`, against `CHARTER.md`, my brief review `reviews/02-film-briefs-review.md` section 1.2, and the owning playbooks `ai-imagery.md`, `agent-pipeline.md`, `animated.md`, `format.md`.
**Maker context honoured:** "for now only me and I will be the only one on this project." The note, playbook and skill all assume the sole keeper; no relative sees drafts; the maker is the proxy with this advisor flagging. Correct.

**Verdict: REVISE.** Scores: meaning 4, specificity 5, accuracy 4, feasibility 4, ethics 4, craft 4. Two critical items are open in the per-shot checklist (both are mechanical false-fails that an agent applying the skill would enforce), so the set cannot be approved yet. Everything else is nudges. This is the strongest craft note the project has produced; the fixes are small and exact.

---

## 1. Spot-checks against sources (9 fetched, 1 measurement reproduced)

| Claim in the note | Source | Result |
|---|---|---|
| GSAP's default ease is `power1.out`; families none, power1–4, back, bounce, circ, elastic, expo, sine, steps; extras RoughEase, SlowMo, ExpoScaleEase, CustomEase | [69] gsap.com/docs/v3/Eases, fetched | **Confirmed verbatim** ("GSAP uses a default ease of `"power1.out"`"). |
| "Pan no faster than a full image width every seven seconds", shutter angle, contrast and near subjects | [41] RED 101, fetched | **Confirmed verbatim.** The page ties the rule to "traditional theatrical viewing at 24 fps with a 180° shutter angle", which supports MO6/MO7 as written. |
| EBU R95: action safe 3.5%, graphics safe 5%, "revised 2016" | [45] tech.ebu.ch r095.pdf, text extracted | **Numbers confirmed** (note 5: "The action safe area is 3.5% and the graphics safe area is 5%, at the top, bottom and lateral parts"). **Date wrong:** the document is June 2017, Ver. 1.1 (March and July 2016 were errata). |
| UHDA white paper: 5 cd/m² reference surround, shadow detail "below the threshold of visibility", gamma table 1.0 / 0.980 / 0.954 / 0.913 / 0.859 at 5/10/20/40/80 | [33] PDF dated 2025-10-08, text extracted | **Confirmed verbatim.** The table also has a 160 cd/m² row (0.794) the note omits; harmless. |
| Runway AIF 2026: fourth edition, Grand Prix $50,000 plus 1,000,000 credits, entries must use generative video, partners, jury includes Runway's CEO "(from general knowledge)"; four 1–10 judging criteria incl. "creative and skilled use of AI techniques" | [1] aif.runwayml.com and [2] hollywood.ai, fetched | **Confirmed.** The AIF page itself lists "Cristobal Valenzuela (Co-founder and CEO of Runway)" as a juror, so the "general knowledge" hedge can go. The four criteria are on [2] only (not on [1]); the note cites both, fine. Gaudette's runtime is 7:50/7:51 ("about 8 min" is fair). |
| Flow: 15–20 people total, 3–5 at a time, about 5.5 years, 0.5–10 s per 4K frame on his own PC, "no compositing", colour in shaders, live camera capture "too imprecise", director the only lighting artist | [23] blender.org interview, fetched | **Confirmed verbatim.** |
| Away: one person, 3.5 years, 8–10 h a day, "6 to 7 days a week", 75 min, Maya, no script or storyboards, floating long takes, no shadows, copied cat animation | [24] Cartoon Brew, fetched | **Confirmed except one detail:** the article says "seven days a week", not "6 to 7". The 140 h per finished minute estimate still holds (it is an order-of-magnitude figure). |
| WAIFF: *Costa Verde* won the CapCut Prize; *A Dollar Story* is Best WAIFF Film; CapCut and MiniMax are sponsors | [7] worldaifilmfestival.com/prize-list, fetched | **Confirmed.** The note's scepticism about the LinkedIn "Best Film" claim is right. |
| Flee: "big art bible where we gathered references", about fifty animators, eyes drawn consistently, "this is good / this is not good", precise on how to draw a hand or an eye, Hopper for light, Metzker for composition and colour, lines not "too straight and smooth", "couldn't afford to have a lot of detail" | [27] Seventh Row, fetched | **Confirmed.** The source spells the photographer "Metzler" (it is Ray K. Metzker); the interview also names Aleksander Gronsky. Trivial. |
| OFL "allows video titling and embedding" | [56] OFL FAQ, fetched | **Half confirmed.** Q1.1 lists "video titling" among permitted uses. The embedding answer (Q1.12) is about "a document or file"; video is not named. The playbook's wording overreaches slightly (nudge 5). |
| `zoompan` is "about 2.7 times rougher" than a sub-pixel resample on a slow 4% 1080p push (0.35 vs 0.13); MO8 threshold 0.15 | [76] M-C7, fixture scripts | **Direction reproduced, magnitude not.** I re-ran `zoompan_vs_subpixel.py` on a fresh plasma still and computed roughness as the README defines it: Pillow 0.19, zoompan 0.33, ratio 1.7×. Two findings: (a) the ratio is content-dependent, so "2.7×" should be reported as a range; (b) a correct sub-pixel render scored 0.19, which would **fail** MO8's absolute pass mark of 0.15. Also, the saved classifier script does not compute roughness at all, so the README's claim that M-C7 came from it is not reproducible as saved (nudge 3). |
| "8-frame grain loop on twos" attributed to [P3] `agent-pipeline.md` | grep of both agent-pipeline files | The playbook never says "8 frames"; the detail is in `research/agent-pipeline.md` (M6 and the baked-grain template row). The finding is right; the citation should point to the research note or to the template id `grain-8f-on-twos`. |
| "Faces of the dead: BANNED [P2]" | grep of `playbooks/ai-imagery.md` | **Not in [P2].** [P2] says "Leave the faces of people who have died alone, unless the family has said yes first" (principle 7, Step 8, Decision 4). The note promises a delta "(see end)" and the Deltas table has none; the playbook correctly flags this as TODO. Under the sole keeper the family cannot be asked before the premiere, so the effective rule is a ban by default, but it must be written as a delta, not cited as existing (nudge 4). |

Arithmetic I checked by hand and found correct: lumens-to-nits (8 m screen, 5,000 lm → 44 nits), the gamma 2.2/2.4/2.6 shadow ratios (−37%, +58% at code 0.10), the 11.4 px per frame pan limit, the x-height derivation from 0.2° at 5 screen heights (1.75%, ×1.5 → 2.6%, font ≈ 5.2%), the lens-shift table (24 mm → 2.5%, 50 mm → 5.2%), Gaudette's ≈30 h per minute, Away's ≈140 h per minute, the 16-frame (0.67 s) repeat of an 8-frame loop on twos.

---

## 2. Scores

| Criterion | Score | Why |
|---|---|---|
| Meaning | 4 | The swap test ("could this frame be about another woman?") at G1 and G2 is the right first question and matches the stranger-in-row-seven stance from review 02. The palette, skin swatch, accent colour and grain are all sampled from *her* scans. One point short because the L5 hand-made material is still chosen from a menu ("cut paper, clay, voxel, other") rather than from her life (see the insight). |
| Specificity | 5 | 47 per-shot items, each with a test and a threshold; a measurable version of the uniform-ease ban that `agent-pipeline` lacked; a 23-row tells catalogue with allowed/label/banned status; a venue test card spec; a 90-minute screening run sheet. Every (J) is labelled and tied to a calibration moment. |
| Accuracy | 4 | Nine of ten fetched claims held verbatim; the misses are a date, a "6 to 7 days", an OFL overreach and a misattributed rule. Measurements are honest about scope (synthetic, 540p, push-ins only). Deductions: the `zoompan` ratio is reported as a single number from one still; the roughness metric is not in the saved scripts; one rule is cited to a playbook that does not contain it. |
| Feasibility | 4 | The one-person rituals are real one-person rituals, not studio practice shrunk. Deduction: the note never totals maker review time per shot or per chapter (A3 twice 48 h apart, AI1 at 5 fps, FN2, FN4 at 200%, half/double speed, reverse pass), and applies the full 47-item list to class A templated photo moves, which are about 60% of shots. Production-scale needs that number (nudge 6). Two agent-side tools (landmark ratios, ΔE00 strip) do not exist yet; that is fine in Learn phase if the skill says so. |
| Ethics | 4 | Strong: no model of her face without her knowledge (default no), no face regeneration or animation in the public cut, no mirrored photographs, strangers see only the public cut, written consent to view, redacted-cut option, the maker's veto on facts. Deductions: "decoys from other real people's photos that the maker supplies" would stylise relatives' faces without their knowledge (nudge 8); the faces-of-the-dead rule is asserted without the decision it needs (nudge 4). |
| Craft / usability | 4 | Holds the theatrical bar: every item is testable on a projected frame, projection truth has numbers, and stacked finish is penalised as hard as AI tells, as the brief asked. The skill's description triggers on the right events (brief, style frame, chapter, render, grade, screening) and its procedure is sequenced correctly (stop if no bible; leave maker items open; never upload). Deductions are the two critical mechanical false-fails below, and the skill not naming the fixture scripts it tells an agent to run. |

---

## 3. Critical issues (block approval)

**C1. MO1 is a Crit item that fails legitimate shots and cannot run on half the move list.** `research` D1 / `playbook` T1 row MO1 ("Level 2 estimator: CV over 0.12; spec contains no default ease", Crit, Agent) and `SKILL.md` steps 6–7 and the per-shot checklist. The note's own Level 1 rule allows `ease: linear` when `drift: declared`, and the "drift" family is defined as "near-constant with micro-variation", which by construction has CV under 0.12. MO1 as written fails every declared drift. Separately, the estimator "was validated on synthetic push-ins at 540p" and "pans should use phase correlation (not tested)", yet MO1 is Crit for all moves. An agent following the skill will either block pans and drifts or mark them passed without a measurement. Fix: MO1 = "spec contains no default ease and no undeclared linear" (Crit, spec-level, all moves); the pixel CV test becomes a Maj audit for push/pull only, with declared drift exempt, and pans, tilts and multi-plane moves reported as `unknown` until a pan estimator exists.

**C2. TY1 is a Crit item that fails every photograph containing text.** `research` D1 / `playbook` T1 row TY1 ("Font at least 5% of picture height; x-height at least 2.5%; strokes at least 2 px", Crit, Agent), playbook step 12, `SKILL.md` step 10. The note's Q10 carves out decorative text ("below 2% x-height the text is decorative and must not carry information"), but the checklist and the skill drop the carve-out. As written, a scan of a shop sign, a letter, a recipe card or her handwriting on the back of a print fails a Crit item. Fix: scope TY1 to type we set (titles, cards, date lines, captions, credits); add TY4 (Min): "text inside photographs or her handwriting is exempt; if it carries information the audience must read, a card or caption repeats it". Also say which rule governs captions, because `format.md` Step 8 sets caption line height at 7–8% of picture height (ffmpeg `FontSize=23` at 1080p) and TY1's 5% font minimum must not be read as a caption target.

---

## 4. Nudges (at most 8, each with file, section and exact change)

1. **MO1 split (C1).** `research/cinematic-quality.md` D1 and Q5 "Proposed rules"; `playbooks/cinematic-quality.md` T1 and step 8–9; `skills/cinematic-quality-bar/SKILL.md` steps 6–7 and the per-shot checklist. Replace MO1 with: *MO1 (Crit, Agent, spec): no framework default ease; no `linear` without `drift: declared`.* Add *MO1b (Maj, Agent, pixels): push/pull only, CV over 0.12 unless `drift: declared`; pan, tilt, orbit, multi-plane → `unknown`.* In the skill's step 7 add "report `unknown`, never `pass`, for any move the estimator does not cover".

2. **TY1 scope (C2).** Same three files, rows TY1 and step 12 / step 10. Insert the Q10 sentence as the rule: "applies to type we set; text inside photographs and her handwriting is exempt; below 2% x-height, text is decorative and must not carry information". Add one line reconciling with `format.md` Step 8 (captions use the format track's 7–8% line height; TY1 is a floor, not a caption size). In `research` Q10 add the x-height of `FontSize=23` at 1080p once measured (research follow-up 1).

3. **MO8 as a ratio, and put roughness in the script.** `research` Q5 "A related finding", D1 row MO8, Sources [76], and `research/cinematic-quality-fixtures/README.txt`; `playbook` T1 MO8, step 9, Exercise 4; `SKILL.md` step 7. Report M-C7 as "1.7–2.7× rougher on two synthetic stills (advisor reproduction 2026-10-18: Pillow 0.19, zoompan 0.33)". Change MO8's pass from "0.15 or less" to "roughness no more than 1.3× a sub-pixel reference render of the same move, or 0.25 absolute until calibrated on the slice (J)". Add the nine-frame-residual roughness function to `zoom_velocity_classifier.py` so the (M) number is reproducible from the saved scripts, and say in the README that `still.png` content changes the absolute values.

4. **Write the faces-of-the-dead delta.** `research` Q7 row 1 (status column) and "Deltas to existing playbooks"; `playbook` T9 row 1 and the Open gaps bullet. Replace "BANNED [P2]" with "BANNED by default in the public cut (delta to `ai-imagery.md` principle 7, Step 8 and Decision 4: [P2] says 'ask the family first'; under the sole keeper nobody can be asked before the premiere, so environment and parallax motion only; revisit after the reveal with written consent from the next of kin)". Add that row to the Deltas table. Remove the TODO from the playbook once written.

5. **Source precision.** `research` Sources [45], [24], [56], and the [P3] attribution in Q6 "Baked overlays"; `playbook` T2 decision 4 `licence:` line, step 12, Sources [45]; `SKILL.md` references. Changes: EBU R95 "June 2017, Ver. 1.1 (2016 errata)"; Away "seven days a week"; OFL "video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video; commercial fonts need their EULA read for film titling and public exhibition"; cite the 8-frame loop to `research/agent-pipeline.md` M6 / template `grain-8f-on-twos`; drop "(from general knowledge)" for Valenzuela since [1] lists him as Runway's co-founder and CEO.

6. **A review-time budget and a class-A minimum set.** `research` D1 preamble and a new row in "Tools, services and costs"; `playbook` T1 preamble and "Decisions you'll need to make" (new row 16); `SKILL.md` step 12. Add: estimated maker minutes per shot for the Maker items (A3 ×2, A4, AI1, AI3, FN2, FN4, FN5, C7) by shot class, and a stated minimum set for class A templated photo moves (Crit items + B1, B8, C1, FN1; MO9/FN3 at chapter level). Hand the per-minute total to `production-scale` as a delta.

7. **Make the skill runnable by an agent.** `SKILL.md` Procedure steps 1, 6, 7 and References. Name the scripts and inputs: `research/cinematic-quality-fixtures/zoom_velocity_classifier.py` (reads an mp4, prints `ends`, `cv`, `peak`, `twos`), `gen_synthetic_pushins.py` and `zoompan_vs_subpixel.py` (need `still.png` in the working directory; copy the script out and run `python3 -I`), and state that the flicker index and grain autocorrelation are not saved as scripts yet. Replace "TODO: the bible's path is not set" with a default location (`style/style_bible.yaml`) and the stop rule if it is absent. State the exact JSON keys of the T8 lint line as the required output.

8. **Decoys without new faces.** `research` Q3 "Likeness sign-off" and D6 "Purpose"; `playbook` T3 "The likeness protocol" step 1; `SKILL.md` "Likeness belongs to the maker". Replace "other real people's photos that the maker supplies as stand-ins" with "public-domain stand-in portraits already listed in `ai-imagery.md` (NARA 546220, US Navy 80-G-27208, and others whose licence was read), or the maker's own face; never a relative's photo, who cannot be told why". Keep "her at other ages" as a second decoy set and say what each answers: public-domain decoys test likeness; her-at-other-ages decoys test age discrimination.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. Measure the x-height, as a percentage of picture height, of `format.md`'s `FontSize=20/23/26` at 1080p, so TY1 and the caption rule can be reconciled with one number.
2. Reproduce M-C7 (`zoompan` vs sub-pixel roughness) on three public-domain scanned prints (faded colour, small black-and-white, soft group) at 1080p from 4K and from native 1080p sources; report the ratio range and set MO8.
3. Build and validate a pan estimator (phase correlation) on synthetic pans at 0.10, 0.143, 0.2 and 0.3 frame widths per second, so MO6 can move from spec-only to audit.
4. SIL OFL FAQ wording on embedding in video (1.12–1.13) and two commercial font EULAs (for example Adobe Fonts and Monotype) on film titling and public exhibition, dated.
5. SMPTE RP 431-2 reference luminance and gamma, and ST 428-1 transfer function, from the documents themselves (the 48 cd/m² ± 3.5 figure is still search-result text only).
6. Any published reaction of families to animated portraits of the dead (the `ai-imagery` TODO), and whether post-premiere written consent from next of kin is a realistic step for a later cinema cut (ties to `theatrical-delivery`'s releases pack).
7. From the maker, not the web: venue type, screen width, projector model or TV size, who runs AV, whether the room can be darkened, and whether playback is DCP, HDMI or USB. Every brightness and gamma number in this note is a scenario until then.
8. A phone-based or free-software method to estimate speech transmission index (or an accepted proxy such as a read-back test with scoring) for D5 item 13.

---

## 6. Strengths (keep these)

- The uniform-ease ban now has a measurable form: a spec lint plus a validated pixel estimator, a family key, and a chapter entropy rule. This is exactly what `agent-pipeline` G4 lacked.
- The picture-lock clash (strangers' screening in week 17 after lock on 2027-02-06) was caught and resolved with two sessions, S1 on the slice in the week of 2026-12-20. Adopt S1; it is the only cheap structural feedback the sole keeper can get.
- Festival laurels are read critically and the prize list was checked against the social claim; the Runway incentive structure is named with its evidence; the non-AI calibration (*Flow*, *Away*, *Danse Macabre*) is used as the quality reference.
- The likeness protocol accepts that nobody but the maker can judge likeness and gives strangers a different, answerable question (one person across ages).
- The grain-loop autocorrelation finding, the 8-bit banding measurement and the thin-line survival numbers each convert a vague caution into a threshold, and each names the playbook it changes.
- The skill refuses to mark maker items as passed and stops when no style bible exists. That is the right failure mode for an agent.
- Honesty labels: (M), (J), UNVERIFIED, Vendor, "search-result only" are applied consistently, and the "no film watched" limit is stated up front rather than buried.

---

## 7. Advisor insight

Choose the hand-made material (ladder level L5, bible decision 2) from her own hands, not from a style menu. Whatever she actually makes with her hands over fifty years (dough, thread, a garden, a ledger in her handwriting, a classroom blackboard, a mechanic's rag) is the material in which everything we never photographed gets reconstructed. The disclosure convention from `animated.md` then stops being a legal footnote and becomes characterisation: "the parts of her life nobody photographed are shown in the stuff she made." It solves three problems in this note at once. The swap test passes by construction, because no other woman's film would be built from her tablecloth. The generic-AI-aesthetic risk collapses, because no model has a prior on her particular kitchen surface, and the material is scanned, not generated (an L0/L1 asset used as a texture). And the "reconstruction marker" (decision 6) writes itself: the grain and paper system of decision 8 is literally the paper she wrote on and the cloth she used. The maker can find the material in week 1 without telling anyone anything: it is in the house. Ask the maker: what did her hands do most, in each era?

---

## 8. Notes for the orchestrator

- The container disk was at 99% (421 MB free) when I ran the reproduction; the fixture scripts write 3 MB clips and a 4K BMP. Clean up before the next measurement task or it will fail mid-run.
- `agent-pipeline.md` Step 5 and G5 still say "trusted relative"; `animated.md` Decision 9 still says "name one close relative". The note's Deltas table lists them; the scribes should patch them in the same pass as this round's fixes.
- The maker's own words settle Decision 12 in the playbook ("Who else is in on the project": no one, for now). Leave it as written; it is correct and can wait until the plan is ready, as the maker asked.

---

## Changelog
- 2026-10-18: round 1 written by the Fable advisor. Nine sources fetched (gsap.com, RED, EBU R95 PDF, UHDA PDF, aif.runwayml.com, hollywood.ai, blender.org, Cartoon Brew, WAIFF prize list, Seventh Row, OFL FAQ); M-C7 reproduced from the fixture scripts on synthetic material in the scratchpad; no family material touched.
