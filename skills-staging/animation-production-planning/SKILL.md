---
name: animation-production-planning
description: "Plans and checks the Life Journey film schedule. It turns the maker's weekly hours, the runtime and the shot classes into feasibility verdicts, runtime tiers, gate dates, the picture-lock procedure and the vertical-slice decision. Use it when someone asks whether a runtime fits the hours, how long a chapter or the slice will take, which gate or lock date applies, or before updating shots/status.csv, chapters.csv, hours.csv, gates.csv or decisions.csv."
---

# Animation Production Planning

## Purpose

Run the production-scale model for the Life Journey film and keep its files honest. Given the maker's hours, the runtime and the shot mix, compute the hours needed, run the four feasibility checks, set the gate and lock dates, and record the slice decision. The planning numbers are judgement until the slice measures them. Do not present them as measurements. The vertical slice is the milestone that measures them [64].

Human guide: `playbooks/production-scale.md`. Evidence, Q1 to Q10 and the model's formulas: `research/production-scale.md`. Model and file templates: `research/production-scale-fixtures/` (`model.csv`, `schedule.csv`, `status.csv`, `chapters.csv`, `hours.csv`, `gates.csv`, `decisions.csv`). Charter: `CHARTER.md`. Decisions register (source of truth; it wins over this skill and the playbook): `DECISIONS.md`.

## When to use / when not to

Use it for:
- whether a runtime (6 for F-0, 9, 12, or 15 to 18 as a stretch) fits the maker's weekly hours; 25, 45 and 90 minutes are not production targets (`DECISIONS.md` W-03, D-24);
- the slice verdict on 20 December 2026, and any later kill or cut;
- gate dates, the burn-down, the picture-lock steps and the unlock rule;
- creating or validating `shots/status.csv`, `chapters.csv`, `hours.csv`, `gates.csv` or `decisions.csv`.

Do not use it for:
- story structure, narration or the choice of chapters (use the story track and `life-film-story-structure`);
- interviews and gathering (use `life-story-interviewing`);
- render setup and hand-offs to Craft apps (use `agent-first-production-pipeline`);
- consent or labels on AI-altered photos (use `ai-photo-to-animation-pipeline`);
- music rights (the music-sound track) or the DCP decision (the theatrical-delivery track).

## Procedure

1. **Read the inputs from the repo, not from memory.** Required: H (weekly hours per phase, written by the maker), the runtime tier, shots per minute (12 or 8), hero share (10 or 5 percent), which of the five levers are adopted, `mu` and `mu_fin` (1.0 until measured), `h_slice` and `h_slice_fin` (if measured) and whether mix, grade and captions are bought (off for the premiere cut under only-me, so finishing stays at 2.7 hours per minute; `DECISIONS.md` W-50, D-07; research F1 and G1). If H is missing, stop and ask the maker. Never assume 10, 20 or 30 hours.
2. **Name the case you are using.** Prior uses the older playbook minutes. Base is the evidence-adjusted case, which allows for people finishing about 1.6 times their predicted time [65]. Levers is Base with the five levers, lever 3 (bought finishing) included; lever 3 is off under only-me (W-50), so do not report this case as the plan. Four is Base with the four levers that need no purchase, and it is the planning case. Best is Prior speeds with the structural levers. Stress is a bad run. Report Base unless the maker asks for another, and always state which case a number came from.
3. **Count the shots.** `shots = shots_per_min x T`. Hero shots are `hero_share x shots`. The mix is 60 percent class A, 25 percent B, 10 percent C and 5 percent D [2].
4. **Weight the minutes per shot.** Base: A 7, B 15, C 120, D 6. Prior: 2, 12, 60, 5. Stress: 10, 18, 180, 8. Weighted minutes = sum of share times minutes. Base gives 20.25.
5. **Compute the hours.** Use these formulas, with Base constants where none is given.
   - `n = round(T x 60 / chapter_s)`, where chapter_s is about 100 seconds (the learning-curve unit, not the cut structure).
   - `L_k = max(floor, L1 x k^(log2 phi))`, with Base L1 = 2.5, phi = 0.80, floor = 1.15. `L_avg` is the mean over the n chapters. This is the learning curve, Wright's 80 percent curve [66].
   - `shot_h = shots x minutes_per_shot / 60 x rho x (1 - reuse) x mu x L_avg`, with rho = 1.25 (rework) and reuse = 0.10 in Base.
   - `chapter_h = n x 2.0 x L_avg x mu`.
   - `sound_h = T x 0.6 x mu`.
   - `prod = shot_h + chapter_h + sound_h`.
   - `total = prod + T x (1.0 + 1.2) + 0.10 x (prod + T x 2.2) + T x 2.7 + 24 + 30 + 20 + 10`. The last four terms are fixed finishing, learning and lock, reuse build and rehearsals. Base check: a 12-minute film gives about 284 hours.
   - `need_H = total / (0.85 x 17)`. Usable hours are H x 0.85 per week over 17 weeks.
6. **Run the four checks.**
   - Check 1, total: total hours at most H x 0.85 x 17.
   - Check 2, post-holiday production: only 40 percent of production hours can be built before 20 December. The rest must fit in weeks W12 to W16 (3 January to 6 February), after story, gathering and rolling finishing take their share. This check usually fails first.
   - Check 3, finishing: 50 percent of fixed finishing and 75 percent of variable finishing fall after picture lock. They must fit in W17 and W18 (7 to 20 February), which hold H x 0.85 x 2 hours.
   - Check 4, buffer: hours left in W19 (21 to 27 February) after the rehearsal hours.
7. **Give a verdict.** OK means checks 1 and 2 pass. `post` means check 1 passes but check 2 fails. SHORT means check 1 fails. Add `/fin` when check 3 is a crunch.
8. **Set the runtime tier with the slice table.** Use the slice table in the playbook (T2), or the model's SLICE CALIBRATION block, to turn `h_slice` into a weekly need. `h_slice` is production side: the minutes for the slice with activity brief_G0, style_G1, review_G2, craft_refine_G3, chapter_G4, dignity_G5, tech_G6, sound and rework. `h_slice_fin` is grade, mix, captions, master and qc, and it gives `mu_fin` against its own prediction. Derive `mu` and `mu_fin` from the block. Do not work it out by hand unless you check it against the block. Predicted `h_slice` is 9.9 (Prior), 26.5 (Base) and 54 (Stress); predicted `h_slice_fin` is 16.5 (Base). Learn and admin are excluded from both and compared with the 30-hour allowance. T2 holds finishing at Base, so read it only with `mu_fin` = 1. Its all-levers column includes bought finishing, so while lever 3 is off under only-me (`DECISIONS.md` W-50) read the no-levers column as the conservative bound. G0 and G1 work is priced inside the per-shot minutes (research Q4), so brief_G0 and style_G1 belong in `h_slice` and are already in the prediction; `story` is priced separately. A recalculation gives 23.9 at h_slice 26 (the table shows 24.1); under 1 percent, table unchanged.
9. **Apply the tier rules** (`DECISIONS.md` W-01 to W-05). H 16 or more with the four levers: 12 minutes (wrapper plus three 3:00 modules). H 14 to under 16: 12 minutes only if the maker adds hours or buys captions, otherwise 9. H under 14: 9 minutes (wrapper plus two modules) from Sunday 15 November, not from 20 December; at 10 hours, 9 minutes only if the slice comes in near Prior speed, otherwise add hours (a bought mix is off, W-50). Before H is written, the plan is 9 minutes. At 12 minutes the G-MID rule is: below 5.4 minutes approved on 17 January, cut the lowest-priority module (to 9 minutes); a second module is cut only at G-DRAFT if it is not at draft. 15 to 18 only at G-SLICE, if H is 20 or more and the slice fits T2; not recommended under only-me. F-0 is 6 minutes. There is no extended private cut: the April version is the same locked picture with voices on (D-06). Do not plan 45 or 90 [7].
10. **Compute the burn-down weekly.** Approved runtime is the sum of `target_s` for shots at approved, refine, final or locked, divided by the total target. The checkpoints are 45 percent by 17 January (for 12 minutes, 5.4 minutes) and 100 percent drafted by 31 January.
11. **Compute the selection ratio and `mu` only from logged data.** Selection ratio is `gens_kept / gens_tried`, for AI clips only. `mu` is the sum of `maker_act_min` over finished shots divided by the sum of `maker_est_min` over the same shots, after the first 20 shots. Vendor ratios are not our ratios [47].
12. **Write decisions, not guesses.** Add a row to `decisions.csv` only when the maker has made the decision. Record the runtime before and after, the measured value, H and the decision in words. Agents recommend. The maker decides. Gate dates and lock dates change only with the maker's approval.
13. **Enforce the lock.** At picture lock (Saturday 6 February 2027), set `locked=1` for every shot, record the timeline hash and frame count per chapter, and create the git tag `picture-lock-2027-02-06`. Refuse any change to a locked shot's duration or order, and point to the unlock rule. A change to shot order, timing or duration after lock is an unlock, because it breaks sync with music, sound and effects [63]. Sat 13 Feb (G-MIX) is the latest acceptable lock, not an option to pick (`DECISIONS.md` W-08).
14. **Apply the unlock rule when asked.** Require a written reason, the cost in hours (which sound, score and grade passes must redo), and a 24-hour wait. Allow only factual, dignity or rights errors. Allow at most two unlocks after lock. Log each in `decisions.csv`.
15. **Validate the status file.** Check the shot ID pattern `^LJ-(C\d{2}|W\d)-S\d{3}$` (wrapper shots W1 and W2 validate), the allowed status and class values, and the rule that `approved`, `final` and `locked` need a version, `kind=appr` and a gate of G2 or higher. No more than three class A shots in a row in a chapter without a still, B, C, D or voice-only beat. Never let an agent raise `cloud_max`.

## Checklists

**Inputs check (before any number is quoted)**
- [ ] H is written by the maker, with its phase and date.
- [ ] The runtime tier and the case are named.
- [ ] Shots per minute, hero share and the list of adopted levers are recorded.
- [ ] `mu` and `h_slice` are marked "measured" or "assumed".
- [ ] The holiday weeks (20 December to 2 January) are counted as zero hours.

**Gate calendar check** (weeks start on Sunday and the dates are the authority; review 02's week list is off by one [6]; check the weekday)
- [ ] P-LOCK Sat 14 Nov 2026 (the process lock, `DECISIONS.md` W-06): spikes SP1 to SP5 reviewed, the process proven on synthetic material. G-READY Sun 15 Nov 2026 confirms it: H in writing; spikes SP1 to SP5 pass or fallbacks named; style frames approved.
- [ ] G-SLICE-0 Sun 6 Dec 2026: animatic with real photos and temporary sound.
- [ ] G-SLICE Sun 20 Dec 2026: slice at the bar, mix, grade, captions and master on venue-class playback; h_slice and h_slice_fin measured.
- [ ] G-RESTART Sun 3 Jan 2027; G-MID Sun 17 Jan (12 minutes: below 5.4 minutes approved, cut the lowest-priority module to 9 minutes; a second only at G-DRAFT, if not at draft); G-DRAFT Sun 31 Jan.
- [ ] G-LOCK Sat 6 Feb (Maha vad Amas in her calendar; lock Fri 5 Feb only if she keeps it and the PC work needs the house, W-08, O-45); G-MIX Sat 13 Feb; G-MASTER Sat 20 Feb; G-REHEARSE Mon 22 Feb.

**Slice acceptance (all must pass; record each in `reviews/C01/`)**
- [ ] The 100-second slice (accept 90 to 120 seconds) of module M1, containing the kitchen hero shot, at least 10 class A, 4 class B and 1 class D shots, one sound line from her world (and one HER-PUBLIC line if it passed; `DECISIONS.md` W-07, W-35), a music cue (the maker's hum in the take each file needs, W-44, W-65), one still and the transition into the next module's motif; frame count equals duration x 24; ffprobe clean. The rest of M1 is built after the gate.
- [ ] Faces and type are clean at full resolution; no invented faces; reconstructions are visibly stylised; no more than 60 percent of tweens share one ease.
- [ ] Real mix (her-world sound, music cue, room tone, transitions; no recorded voice of a living person except a HER-PUBLIC line if it passed, D-05); loudness measured with `ebur128` at -1 dBTP against the theatrical-delivery target (W-19); a person listened on venue-class speakers.
- [ ] One grade through the same chain; colour-patch test within plus or minus 3 out of 255 on the final encode [2].
- [ ] Captions within the reading-speed limits; master verified; DCP test file only if a DCP is in scope [61].
- [ ] S1, the stranger screening on the slice (one or two strangers to her, redacted copy, truthful partial pretext; `DECISIONS.md` W-43); if the maker declines, the cold self-read (playbook T3): 48 hours unopened, one viewing on venue-class playback at about 3 m with sound, three questions answered in writing first, and the cinematic-quality rubric applied by the Fable advisor to the same version.
- [ ] Hours logged by stage and class, including `h_slice` and `h_slice_fin`, with learn and admin reported against the 30-hour allowance.
- [ ] Repo, folder and commit names harmless; no personal data in any cloud service; `cloud_max` respected.

**Weekly update**
- [ ] `hours.csv` has every session, including learning and rework [J].
- [ ] `status.csv` is validated and the burn-down is computed.
- [ ] The four checks are re-run if H, the material or `mu` changed.

## Quality bar

Theatrical work holds up on a big screen and in a dark room. Use these tests to tell it from mediocre work.

- **One look.** Every shot passes through the same grade chain. The colour-patch test passes [2]. Agree the look with cheap look tests first. A few days of work each is enough [67].
- **No template tells.** No uniform easing (no more than 60 percent of tweens on one ease). No stock transitions. No centred titles. No identical slow zoom on every photo. Seeded variety is used on purpose, and at least one still appears per chapter [2].
- **Clean faces.** Full-resolution crops of faces and type are clean. No AI artifacts. Any reconstruction is visibly stylised, so it is never mistaken for a photograph.
- **A real sound mix.** Dialogue, music, room tone and transitions are mixed. Loudness is measured and a person has listened to it on the speakers it will play on. Sound and grade are not treated as the last thing done [62].
- **A proper master.** The picture and sound are verified end to end on venue-class playback. The frame count is exact. Backups are checked.
- **A story an outsider can read.** At S1 and S2 the strangers can say who she is, what she wanted and what they felt, and their first question is about her (`DECISIONS.md` W-43). If the maker declines, the cold self-read (playbook T3) tests it. Until a read has passed, treat this as untested.

## Ethics, rights and privacy guardrails

- **The surprise.** The maker is the only person in on the project (only-me, `DECISIONS.md` D-03; re-opened once, at TD-L2c, Sunday 3 January 2027). Do not add anyone to a file, share, tool, notification or thread without the maker's explicit decision. Do not contact any relative or friend to test or source the film. Keep repo, folder and commit names harmless [1].
- **Cloud levels.** Personal material defaults to `cloud_max=none`. Only the maker raises it. Never send family imagery to a free render farm [57], a hosted tracker or a rented GPU. Rented GPU pricing is at [54]. Cycles speed is 17.5 s (Suzanne) to 204 s (classroom) per 1080p frame on the container, and 1.6 to 5.6 s per frame on an RTX 4090 at 64 to 256 samples [82][83][84]; spike SP3 measures the kitchen set and passes if one real hero frame lands within 2 times the table. Hero finals are GPU work by default: the maker's PC, or a rented pod only for scenes with no family imagery. A scene that uses her photographs as textures counts as family imagery and needs the maker's explicit say.
- **Refusals.** Veo probably refuses photos of children, which is UNVERIFIED [8]. If a provider refuses, accept the refusal. Do not resubmit the photo through another route.
- **Real memories.** AI may restore, restyle, animate and connect real photos and stories. It must not invent events, people, faces or cloned voices, or put words in anyone's mouth [1].
- **Labels.** Mark AI-altered or generated content on the label ladder (L1 to L4c) in `status.csv` [8].
- **Hard chapters.** One-key-three-guards (`DECISIONS.md` D-04): a decision sheet per candidate; the Fable advisor's written flag for a deliberate decision [1][6]; the maker decides, waits 72 hours, and decides again (review 02 section 0.3's rule, adopted by the story track [6][7]); and default OUT of the public cut on any doubt. HOLD or PRIVATE stays out, and the her-turn conversation after the reveal (Sunday 7 March 2027 after about 14:00, else Monday 8 March, moved off Maha Shivaratri; `DECISIONS.md` W-48) is how she can put it back [6]. Fable flags and never passes G5.
- **Rights.** Music, photos taken by others, archival footage, fonts and voices of people who appear must be cleared for public screening [1]. Music rights can cost more than the animation: one rights bill was asked at about $220,000 and settled at $50,000 [14]. Clear before the mix.
- **Tool volatility.** Never let one hosted model be the only route for a shot class. A hosted service can be shut down mid-project [44][45].
- **Hearsay numbers.** Do not quote vendor, forum or unnamed-source hours as planning facts [47][68].

## References

- Playbook (human guide): `playbooks/production-scale.md`
- Research notes (evidence, Q1 to Q10, formulas, gaps): `research/production-scale.md`
- Charter: `CHARTER.md`
- Decisions register: `DECISIONS.md`
- Related skill: `.claude/skills/agent-first-production-pipeline/SKILL.md`
- Open before relying on the model: H (the maker's weekly hours, pending, `DECISIONS.md` O-01); the spike list SP1 to SP5 (SP3 measures the real kitchen); her festival calendar row by row (`kept_by_her`, O-39, O-56; `playbooks/production-scale.md` Decision 16) and the premiere country's public holidays as logistics rows (the country is pending, O-02); the budget ceiling (O-04); and the Claude plan (O-12, research F4). Settled by the register: the chapter count (the wrapper plus three 3:00 modules for 12 minutes, W-04; film-story's 2:15 row is superseded; seven 100-second learning-curve units in the model, which are not the cut structure); the frame rate (24 per second, signed on the settings card on Sunday 1 November, W-14, W-16); the DCP-or-file decision (the venue's written answer, due Sunday 15 November, W-17); and buying the mix and grade (off for the premiere cut, W-50). The playbook's Decisions section gives the current lean for each.

### Sources

- [1] Life Journey Project Charter — `CHARTER.md` — 2026-10-18 — roles, principles, constraints, open decisions.
- [2] Agent-First Production Pipeline playbook — `playbooks/agent-pipeline.md` — 2026-10-18 — shot classes, minutes per shot [J], gates, validators, naming, rhythm.
- [6] Film briefs review — `reviews/02-film-briefs-review.md` — 2026-10-18 — schedule prior, refined brief, week numbering.
- [7] Writing a biographical animated film research notes — `research/film-story.md` — 2026-10-18 — runtime recommendation, scene-grade memory counts, 72-hour double-decision rule.
- [8] AI imagery and motion research notes — `research/ai-imagery.md` — 2026-10-18 — Veo and Kling prices, children's photos, label ladder, RunPod.
- [14] Wikipedia, *Sita Sings the Blues* — https://en.wikipedia.org/wiki/Sita_Sings_the_Blues — read 2026-10-18 — 82 min, $290,000, Paley's estimate of 9,360 hours, music rights $220,000 reduced to $50,000.
- [44] Forbes via Yahoo, "Why Critterz is the real test of AI filmmaking" — https://www.yahoo.com/entertainment/movies/articles/why-critterz-real-test-ai-212613673.html — updated 2026-05-26 — Q1 2027 target, Sora discontinued, first-look footage at the Cannes market.
- [45] The Next Web, "Sora shutdown leaves Critterz at the Cannes market without its model" — https://thenextweb.com/news/critterz-misses-cannes-openai-sora-shutdown — 2026-05-22 — Sora app dark 2026-04-26, API scheduled for 2026-09-24, in-festival slot missed.
- [47] invideo, "How many AI video generations do you need per usable shot?" — https://invideo.io/faq/how-many-ai-video-generations-do-you-need-per-usable/ — undated — vendor numbers (3 per usable shot, 25% kept, $315 to $750 per minute).
- [54] RunPod pricing — https://www.runpod.io/pricing — "Updated October 8, 2026" — GPU rates and storage.
- [56] Renderjuice RTX 4090 comparison — https://www.renderjuice.com/gpus/compare/rtx-4090-vs-rtx-5050 — "Checked Oct 14, 2026" — estimated 3.5 to 7.5 s per frame on three benchmark scenes (Blender 5.2.0).
- [57] SheepIt Render Farm — https://www.sheepit-renderfarm.com/ — read 2026-10-18 — free distributed Blender farm; no confidentiality statement.
- [61] DCP-o-matic speed page — https://dcpomatic.com/learn-more-speed — undated — Grok GPU benchmarks.
- [62] iZotope, "Tips for mixing short films" — https://www.izotope.com/community/blog/tips-for-mixing-short-films — undated — "double it"; add days.
- [63] ECG Productions, "What is picture lock and why does it matter?" — https://www.ecgprod.com/what-is-picture-lock-why-does-it-matter — undated — definition, effects of change.
- [64] Unity Learn, "Production and post-release" — https://learn.unity.com/course/game-development-in-a-nutshell/tutorial/production-and-post-release — undated — vertical slice definition.
- [65] Wikipedia, "Planning fallacy" — https://en.wikipedia.org/wiki/Planning_fallacy — read 2026-10-18 — thesis study, 33.9 predicted days, 55.5 actual.
- [66] Wikipedia, "Learning curve" — https://en.wikipedia.org/wiki/Learning_curve — read 2026-10-18 — Wright's law, 80 percent curve.
- [67] PremiumBeat, "A masterclass in making a Pixar animated short" — https://www.premiumbeat.com/blog/a-masterclass-in-making-a-pixar-animated-short — undated — look tests "super quick and dirty, just with a few days of work".
- [68] Indietalk and ZHdK audio-post pages — https://indietalk.com/goto/post?id=348469 and https://medienarchiv.zhdk.ch/files/f693e5ef-5249-491e-8bfa-ae379306539a?lang=en — undated — **snippet-only** (both returned errors): "one hour per finished minute", "six hours per linear minute".
- [82] Blender Open Data, About — https://opendata.blender.org/about/ — read 2026-10-18 — score definition (samples per minute, summed over scenes), snapshot address.
- [83] Blender Open Data daily snapshot — https://opendata.blender.org/snapshots/opendata-latest.zip — Last-Modified Sun, 18 Oct 2026 00:01:21 GMT — licence Creative Commons 0 stated in the archive's README.txt and LICENSE.txt.
- [84] Blender Benchmark 2.0 files — https://mirrors.ocf.berkeley.edu/blender/release/BlenderBenchmark2.0/ — read 2026-10-18 — scenes classroom, junkshop, monster; script sets samples to 1<<24, 30-second time limit, adaptive sampling off.

## Changelog

- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18). 9-or-12 rule and no 25-minute tier (W-01 to W-03, D-06); lever 3 off under only-me (W-50); one-key-three-guards replaces the "fourth guard" wording (D-04); no voice-over in the slice or the mix (D-05, W-07); S1 and S2 stranger screenings (W-43); frame rate, DCP-or-file and chapter count marked settled (W-04, W-14, W-17). Superseded values S-19, S-34, S-35, S-36 and S-37 patched.
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19). Spikes are SP1 to SP5 and the process lock is P-LOCK, with a P-LOCK line in the gate check (W-06; S-39); G-LOCK note re-keyed from the placeholder observance to Maha vad Amas (W-08, O-45; S-61); S1 is one or two strangers (W-43); the her-turn conversation is Sun 7 Mar after about 14:00, else Mon 8 Mar (W-48; S-64); the slice's music cue is the hum (W-44, W-65); source [94] retired. Patched copy staged in `skills-staging/`; the orchestrator installs it.
- 2026-10-20: Stale-wording sweep (2026-10-20). Step 9 of the procedure names the April version as the same locked picture with voices on, not an extended private cut (D-06), matching the playbook; no value changed.
