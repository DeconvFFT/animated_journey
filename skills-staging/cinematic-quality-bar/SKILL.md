---
name: cinematic-quality-bar
description: Checks and builds the theatrical quality bar for the Life Journey film, with per-shot and per-chapter tests for AI tells, motion and ease variety, colour, finish, type, reconstruction honesty, venue projection, the phone-safe frame and the Hindu-world checks. Use when a shot brief, style frame, chapter, render, grade or screening plan for the film is planned, generated, reviewed or signed off, or when someone asks whether AI-assisted work looks like AI.
---

# Cinematic Quality Bar

Reconciled with [DECISIONS.md](../../DECISIONS.md) (2026-10-18, and again on 2026-10-19 after the her-world merge), the single source of truth. Where this skill disagrees with a register row, the register wins. D-nn rows are decided by the maker; W-nn rows are working defaults. Her Hindu world sets the look (D-28, D-31), the phone is a first-class screen (D-27), and the game-world rule is retired (D-29).

## Purpose

Make every shot, chapter and screening for the Life Journey film meet the theatrical bar in the charter (principle 6), without looking like AI-made work. This skill gives the procedure, the checklists, the quality bar, and the limits of each automatic check.

It does not replace the maker's judgement on likeness, dignity, meaning or taste. The maker is the only person on this project and the only one who may see her.

For reasons and worked exercises, read the playbook: `playbooks/cinematic-quality.md`. The evidence and its limits are in `research/cinematic-quality.md`.

## When to use

- A shot brief is being written or reviewed.
- A generative, restoration or motion step is about to touch a photograph.
- A style frame, era colour strip, chapter cut, grade or venue test is being planned or checked.
- A D1 (shot), D3 (review), D4 (banned tells), D5 (venue) or D6 (screening) check is requested.

## When not to use

- Choosing the story, the chapters or what to include. Use the story and film-story tracks. This skill checks craft, not content.
- Gathering stories, photos or interviews. Use the surprise-ops and story tracks.
- Music, voices and the final mix. Use the music-sound track. This skill only checks that a loudness plan exists.
- DCP packaging and delivery mechanics. Use the theatrical-delivery track. This skill gives the venue checks only.
- Likeness, dignity or sensitive-chapter decisions. The maker decides, and the Fable advisor flags. Never mark a maker item as passed.
- Any fact about a tool, price, festival or URL that is not in the notes. Research it first. Never cite a URL you have not seen.

## Procedure

1. **Read the sources.** Read `CHARTER.md`, `DECISIONS.md` (the decision register; it wins over any value in this skill) and the playbook. The style bible's default path is `style/style_bible.yaml`; use it unless the brief names another path. That path does not exist yet, so the first run stops here. If the file is missing, or it does not lock the twelve decisions (T2: decision 11 is `hindu_idiom` and decision 12 is moving footage; a card-and-set sheet may stand in for decision 11 if the household keys are not answered, O-67), stop before generating or rendering, and report that. The measurement scripts that back the checks are in `research/cinematic-quality-fixtures/` (README there; the tool list is under References); copy a script out and run it with `python3 -I`. If `windows_check_report.json` for the maker's PC is not in the repo, every Windows number in a report is marked UNVERIFIED.
2. **Check the shot brief.** Required fields: `output_level` (L0 to L5, the ladder in `playbooks/ai-imagery.md`), `because` (reveal, link, isolate, time or hold), `ease_family`, `mirrored: false`, `virtual_lens`, `era`, `beat`, the source photo IDs, and the `steps.csv` path. A missing field fails A1 or B1. The Hindu-world and phone fields of W-42 are required wherever they apply: `motif_check` (hindu, Hindu-Gujarati, flagged, excluded, jain_flag, adivasi_flag or political-room, with a source), `deity_form` and `deity_source` on a deity shot, `respect_check` (R1 to R20, VR-1 to VR-3, PR1 to PR25), `phone_stroke_ok`, `phone_safe`, `hands_box`, `object_box`, `caption_zone`, `place_id`, `political_room`, `kitchen_hour` (a sheet field, never a card), `hands_making` and `seat_check`. A missing one fails HW1 to HW5, B9 or TY5.
3. **Screen against the banned list (playbook T5).** Refuse any brief that asks for: a regenerated, restyled or animated real face in the public cut; blinks, mouth movement or speech from a still; generated hands in a photo shot; generated text or logos; a morph between two different people; a mirrored photograph; a cloned voice; AI-sung words; an invented person; skin smoothing; invented teeth or eyelids; a deity that is drawn, generated, photographed, mirrored or moved (P1 is the default, W-61); a motif that is `excluded` or unflagged shared-origin (W-66); or a darshan name on a card (PR16). The Hindu-world and Gujarat tells are T5 items 28 to 39. For a push, also refuse the renderer bans in step 7 (playbook T5 items 24, 26 and 27).
4. **Pick only the allowed route for the label.** For restoration, prefer a plain upscale. If you restore, never change teeth, eyelids or jaw. For motion, environment movement that keeps the face region from the L1 or L2 photo is L4b. Whole-frame image-to-video on a face-bearing photo is L4b only if the maker's line-up passes; otherwise it is banned. Keep generated clips to 3 to 5 seconds. Re-anchor every generation to the original photo, never to the last output.
5. **Write the motion timing chart.** For each move, record displacement at 10, 25, 50, 75, 90 and 100% of its duration. Assign one of six families: in-out, out, in, settle, drift or hold-snap. Limits: push or pull up to 8% of frame; pan or orbit up to 5% of width and 3 degrees; pan no faster than 0.143 frame widths per second (11.4 px per frame at 1920) unless blurred or declared as a whip. Holds: at least 0.75 s after a payoff, 1.0 s after a punchline or reveal, and at least 1.5 s on a legible card.
6. **Run the spec lint (MO1, Crit).** Fail any move with a `linear` ease and no `drift: declared` in the brief. Fail any framework default: `power1.out` for GSAP, `ease` for CSS. Fail a chapter where more than 40% of eased moves share one ease string. Fail evenly spaced stagger offsets. Output one JSON line per shot with exactly these keys, in this order: `shot`, `ease_class`, `axis`, `duration_s`, `magnitude_pct`, `cv`, `ends_ratio`, `peak_pos`, `settle_ok`, `twos`, `roughness`, `mo8a_px`, `mo8b_d4_px`, `family_key` (the T8 lint line in playbook T8). Fill the spec fields first (`ease_class`, `axis`, `duration_s`, `magnitude_pct`, `family_key`). The pixel fields (`cv`, `ends_ratio`, `peak_pos`, `settle_ok`, `twos`, `roughness`, `mo8a_px`, `mo8b_d4_px`) come from step 7 (`mo8a_px` is `mo8a_centre_jit_px` and `mo8b_d4_px` is `mo8b_d4_px` from `mo8_audit.py`), or are `unknown` for any move the tools do not cover. The T8 line has no field for the drift declaration or the framework-default check, so record those results under MO1 in the step 12 report.
7. **Audit the pixels before grain (MO1b, MO2, MO6, MO8).**
   - **Pushes and pulls (MO1b, MO2).** `ZV_SIZE=1920x1080 python3 -I research/cinematic-quality-fixtures/zoom_velocity_classifier.py shot.mp4`. It reads an mp4 and prints `ends`, `cv`, `peak`, `twos` and `roughness`; without `ZV_SIZE` it runs at 240 by 135. It was validated on synthetic push-ins at 540p and, as a reconstruction, on three public-domain scanned prints at 1080p from 4K and native sources (M-C7b, 51 clips); on faint prints the floor rises (0.056-0.076 after H.264 on the faintest), so always render the Pillow reference from the same source file.
   - **Pans and tilts (MO6, MO1b, MO2).** Speed: `python3 -I research/cinematic-quality-fixtures/pan_estimator.py clip.mp4 24` on the delivered 1080p file (validated, M-C9). Ease: `python3 -I research/cinematic-quality-fixtures/pan_ease_classifier.py clip.mp4 24` on translation-only pans and tilts (validated, M-C11: exact easing and family on 100 of 100 in-library clips through grain, H.264, twos and integer steps; family on 4 of 5 unseen CSS curves, the fifth flagged; the truth curves were the library's own except those five). Fill the pixel fields from its output (`features` holds `start`, `end`, `peak_pos` and `cv`; `family_key` is given). Report `unknown` only when it sets `low_confidence`, and for orbits, rotations, mixed zoom-and-pan and layers with different eases (measure those from the spec); never `pass` for them. Pan family keys for MO9 come from `family_key`, and `mo9_check(keys)` applies the chapter rule. Unless-blurred and declared-whip pans stay a human call, because the estimator measures content shift, not blur.
   - **Smoothness (MO8).** `python3 -I research/cinematic-quality-fixtures/mo8_audit.py clip.mp4` on the output of any renderer, or on a folder of PNG frames for the master (it then also reports the result after x264). MO8 passes when MO8a, centre jitter (`mo8a_centre_jit_px`), is at most 0.05 px at 1080p on the delivered file **and** MO8b, edge jitter by the fourth-difference estimator (`mo8b_d4_px`), is at most 0.04 px, measured on the master **before** the delivery encode (x264 CRF 14 alone reads 0.025 to 0.039 on perfect renders). Roughness (MO8c) and the ratio to a Pillow reference are informational only: Pillow EXTENT and a plain CSS transform read 1.4 times the Pillow box reference (M-C10), and relative roughness changes with push length and codec (advisor reproduction 2026-10-18: a perfect Pillow 4% push after x264, MO8c 0.069 at 2 s against 0.038 at 4 s; nine-frame MO8b 0.060 against 0.016; fourth-difference 0.026 against 0.017). There is no absolute roughness threshold. MO8a reads about 1.3 to 1.6 times the position jitter behind it, so 0.05 px is about 0.038 px of position error, under a best-case static alignment threshold of 2 to 5 arc seconds [123] beyond about 1.4 to 3.6 screen heights (UNVERIFIED for moving pictures until the venue A/B card says otherwise).
   - **Renderers (M-C10).** Do not use ffmpeg `zoompan` for finals: it reads 0.63 px, not 0.29, in the usual `-pix_fmt yuv420p` command line. Keep it for proofs. Pillow (`resize` with the box filter, or `transform` EXTENT) passes. GSAP: use it for the ease only and write `style.transform` yourself in `onUpdate`; its own `scale` tween writes four decimals and fails MO8b (0.061 px). No `force3D` on slow pushes (centre jitter 0.044). Never animate `width`, `height`, `left` or `top` for a push (0.18 px). Capture a Chromium page by stepping it and screenshotting, never by real-time recording. Blender: image texture on Linear; motion blur makes no difference on a slow push. FilmCraft 0.9.0: a new keyframe is linear, so set `bezier` or `autoBezier` on both keyframes of every Ken Burns (or `easeOut` on the first and `easeIn` on the last); its built-in H.264 export is for proofs only, finals go ProRes then x264.
   - The flicker index and the grain autocorrelation are not saved as scripts yet; mark them `unknown` until they are.
8. **Finish once.** Add only layers from the era's finish stack. Count the global layers: grain, vignette, letterbox, flare, bloom, halation, dust, scratch, light leak, colour filter and shake. The limit is two or fewer. Run the finish-off test: silhouette, value and colour must still hold without the finish. Bake grain as at least 48 distinct frames with a seeded start per shot. Autocorrelation at the loop length must be under 0.3. Grain spread on new layers must sit within 30% of the scan's flat patch. Blur depth planes per layer, never per pixel, and never blur faces for depth.
9. **Check colour numerically.** Compute the median and three dominant colours in CIELAB. Compare with the era swatches using ΔE00. Limits: within 6 for the shot, within 4 for skin, and within 3 across shots in one scene (J; calibrate on the first five slice shots). Plot the chapter as a colour strip beside the script.
10. **Check type and graphics (TY1, TY3, TY4).** For type we set (titles, cards, date lines, captions and credits): font at least 5% of picture height, x-height at least 2.5%, strokes at least 2 px at 1080p. Text inside photographs and her handwriting is exempt. Below 2% x-height, text is decorative and must not carry information. If text inside a photograph carries information, repeat it on a card or caption (TY4). Captions follow `format.md` Step 8 (7 to 8% line height), which at 1080p is `FontSize=23`: x-height 3.2 to 3.8% of picture height across five fonts, line pitch 7.96% (M-C8). Caption x-height floor 3.1% (6 screen heights, J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font; TY1 is a floor, not a caption size. Those are Latin figures: Gujarati is sized by the height of its base letter KA (3.33% of picture height at `FontSize=23` in Noto Sans Gujarati; 26.2 for the phone's 3.8% target), and the phone file carries `FontSize=28`, `MarginV` 40, two lines of at most 36 characters, the block at 68 to 86% of height (W-18). In every file, must-read type has an x-height of 3.2% or more as a hard floor and 3.8% as the target, and a phone file's meaning lines are 4 px or more (TY5, PR2b; W-38 decision 3, W-63). No saturated 1 px lines. Text and graphics inside 5% margins (a phone file's text box inside 5 to 95% across and 12 to 88% down). A licence file for every font, texture and plate. Fonts: OFL only for titles, cards and captions (W-21), with the Indic families of T2 decision 4 and her script on title and verse cards as shaped outlines, never live text (W-75); commercial fonts under an Adobe or Monotype subscription are out, because Adobe's terms (effective 7 October 2024) grant use "only for as long as you maintain an uninterrupted Adobe Subscription Plan" and never mention video, film, broadcast or exhibition [109].
11. **Check the venue risks.** Story-critical detail must sit above 10% signal. After the access-copy encode, thin lines keep at least 90% of their contrast, and flat-patch grain stays at 70% or more of the master's (PH1 at CRF 20 keeps 73%; PH2 and any HEVC fail the same test and are exempt or measured at equal viewing scale, W-63, W-64). For a phone file, run the chart through the two chat proxies (PR2b). Record the playback path the shot was graded for, and which of Trim V, Trim C and Trim P applies.
12. **Write the shot report.** Use one table with every T1 item from the playbook: pass, fail or unknown, plus the evidence file name. Mark each item Agent or Maker. Estimated maker minutes per shot (J, to time on the slice): class A about 3 to 4 (AI1 2, AI3 1 where visible, FN2 1); class B about 2 to 3 (AI1 1 on moving graphics, AI3 1 where there is text, FN2 1); class C about 9 (A4 1, AI1 2, AI3 1, FN2 1, FN4 2, FN5 1, C7 1), plus 10 for each L3 or L4b face shot (A3, two sittings 48 hours apart); class D about 1 to 2 (AI3 1 where there is text, FN2 1). For class A the minimum set is every Crit item that applies to the shot, plus B1, B8, C1 and FN1; MO9 and FN3 are checked once per chapter. The per-minute total (about 45 maker minutes per finished minute before A3 at the unlevered 12 shots a minute, and about 27 at 8 shots a minute with hero shots at 5%, W-34 and W-51; J) goes to `production-scale.md` as a delta.
13. **Leave maker items open.** Never mark these as passed: A3 (blind line-up), A4 (eyes and mouth), AI1 (tell sweep), AI3 (hands, text, reflections), FN2 (finish-off test), FN4 (cut-out edges), FN5 (light wrap), C7 (light direction), PR1 (banding), and HW2 and HW3 (the maker approves every deity drawing as her proxy, and Fable reads every deity shot and every flagged brief, W-42). Write "maker to check" beside each.
14. **Assemble and check the chapter (G4).** In every run of eight moving shots: at least three move families, none above 40%, no family more than twice in a row, and entropy of at least 1.5 bits (`mo9_check(keys)` in `pan_ease_classifier.py` applies this rule to a list of `family_key` values). Held shots should be at least 35% of photo shots. Include at least one picture-led silence of 3 s or more. Shot-length coefficient of variation should be at least 0.4 (J). No finish layer on more than 80% of shots. Make a contact sheet at one frame per second for the AI-tell sweep. Captions stay within reading limits. A loudness plan must exist: -1 dBTP everywhere, three venue masters (-23, -18 and -16 LUFS) chosen at the Mon 22 Feb run, the phone files and any online copy -16 LUFS and -1 dBTP measured on the final MP4 after the AAC encode (W-19, W-63). A `card_text` scan finds no darshan name on any card (HW5, PR16). **Gated** at G4: MO8a and MO8b, captions inside the 90% box, -1 dBTP, the colour-patch test, the L-label present, the AI-tell sweep including the Hindu tells, one still-still, the strangers' first question, and the card_text scan. **Reported, not gated until G-DRAFT (Sun 31 Jan):** shot-length coefficient of variation, move-family mix, holds share, the ΔE00 thresholds, half- and double-speed passes, sound-off and picture-off passes (W-42).
15. **Log deviations.** For any rule you bend, add a decision-log entry in the T8 format, with `evidence` and `reversible` filled in.
16. **Hand off.** Return the report and the list of open maker items. Do not publish, share or upload anything. Do not send personal material to a third-party service without the maker's explicit say (charter).

## Checklists

**Per shot, before handing off**

- [ ] Brief has every required field, and the label matches the ladder.
- [ ] No banned tell is present (playbook T5).
- [ ] Every move has a reason, its limits are met, the spec lint passes, and no default ease is used.
- [ ] Pixel audit run: the zoom classifier on pushes and pulls (MO1b, MO2), `pan_estimator.py` and `pan_ease_classifier.py` on pans and tilts (MO6, MO1b, MO2), and `mo8_audit.py` on every push and pull (MO8). Orbits, rotations, mixed zoom-and-pan and layers with different eases reported `unknown`, never `pass`. MO8 passes only when MO8a is at most 0.05 px and MO8b (`mo8b_d4_px`) at most 0.04 px on the master before the delivery encode; roughness and the Pillow reference ratio are informational.
- [ ] Finish layers counted: two or fewer. Finish-off test queued for the maker.
- [ ] Grain baked with 48 or more distinct frames, seeded, and loop autocorrelation under 0.3.
- [ ] ΔE00 within limits for the shot and for skin.
- [ ] Type size, stroke width, margins and licence files pass; phone files also pass TY5, PR2b and B9.
- [ ] Hindu-world items HW1 to HW5 filled for any motif, deity, seva object, place or card in the shot; no deity drawn, generated or photographed under P1.
- [ ] Every maker item is listed as open.

**Per chapter (G4).** The checks in step 14. After screenings, the independent marks per minute must be two or fewer.

**Before a venue screening (playbook T6).**

- [ ] Six venue answers (playbook step 1; neutral ask sent by Fri 6 Nov, answers due Sun 15 Nov, W-17) in `venue.json` and `venue_calc.py` run; every brightness, gamma and type-size figure is a scenario until then.
- [ ] Test card made: PLUGE, grey ramp, the RP 431-2 grey step scales (Tables A.2 and A.3, generated by the same code and audited before they are played), colour bars, skin stills, type ladder, line ladder, pan at four speeds, speech passage, and, at the venue visit, the 60 to 90 s venue test clip with no personal content (30 seconds of the film only at the Mon 22 Feb rehearsal; W-17, W-52, W-56).
- [ ] A/B push card (`ab_push_card.py`, 15 minutes) run on the real projector from the front and back rows, with its answer key and recording sheet. Reading rule: MO8a = half the measured MO8a of the lowest front-row "yes", never above the lowest "maybe". Until it has run, 0.05 px is a derived bound, not an observed one.
- [ ] Run at the venue visit by Sun 17 Jan 2027 (TD-L2b, W-56) with the test clip only, again at the Mon 22 Feb rehearsal (G-REHEARSE, W-52), and on the day.
- [ ] Brightness, gamma and picture modes recorded. Motion smoothing, sharpening, noise reduction and dynamic contrast off; overscan off.
- [ ] Reference figures written down (SMPTE RP 431-2 s6.1, ST 431-1 Table 1): white 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2); gamma 2.6 ±5% in a theatre; ambient on the screen with the projector off below 0.01 cd/m² (Review Room) or 0.03 cd/m² (Exhibition Theater) [91][92].
- [ ] Back-row checks done for type and captions. Speech checked at STI 0.60 or higher by a STIPA app or Room EQ Wizard's indirect method if available; otherwise the 100-word read-back at the back row (90 or more correct passes, under 80 fails, 80 to 89 repeat with a new list; FQ8, UNVERIFIED against a meter) [103][104][105].

## Quality bar: theatrical or mediocre?

Signs of theatrical work:

- The frame still works with the finish switched off.
- The frame could be about no one but her: her objects, her light and her palette.
- Camera moves are rare. Each has a reason, and each settles.
- Faces are unchanged from the source, or built by hand from the board.
- Type reads at the back row and on a phone, and dark detail survives on the venue screen.
- Grain looks like film: spatially varied, not a repeating texture.
- A chapter varies its shot sizes, lighting, holds and move families.

Signs of mediocre, AI-looking work:

- Default ease, uniform stagger, or the same slow zoom on every photo.
- Stacked finish: grain, vignette, letterbox and flare on most shots.
- Generic lighting, centred epic compositions, a teal-orange grade, or over-saturated skies.
- Plastic skin, warped hands or text, morphing, or flicker in flat areas.
- Checks done only on a laptop.
- A generic-India or generic-Gujarat look that would work for any family (T5 items 28 to 39), or a line that only a laptop can show.

The bar: a shot passes when every critical item passes, every major item is fixed or logged, no banned tell is present, and the maker has signed the maker items. A chapter passes at G4 when its checks pass and the strangers' marks are two or fewer per minute. Every rubric score (meaning, specificity, accuracy, feasibility, ethics, craft) must be 4 or higher.

## Ethics, rights and privacy guardrails

- **Real memories stay real.** Never regenerate, restyle with a model, or animate a real face in the public cut. Never animate the faces of the dead. A reconstruction must look like one and carry the disclosure marker.
- **Likeness belongs to the maker.** Agents never mark the blind line-up as passed. The maker signs five of five correct, twice, 48 hours apart. Decoy set A is the same stylisation applied to public-domain stand-in portraits listed in `ai-imagery.md` (NARA 546220 and US Navy 80-G-27208 among them, licences read on their Commons pages, re-check before use), or to the maker's own face. Never a relative's photo, who cannot be told why. Decoy set B is the same stylisation applied to her at other ages. Set A tests likeness; set B tests age discrimination.
- **No model of her face.** No model is trained on her face (D-16, decided). Style LoRAs train only on the maker's own hand-made frames.
- **No invented events, people or words.** No voice cloning, no AI-sung words, and no new sentences in her handwriting. Her handwriting is used only for words she actually wrote.
- **No mirrored photographs.** A flip changes a parting, a ring hand and any text.
- **Dignity.** Hard chapters (loss, illness, separation, money, conflict) stay out by default. The Fable advisor flags sensitive material in writing and never passes G5; the maker decides twice, 72 hours apart (D-04, one-key-three-guards).
- **Privacy.** Do not upload personal material to any third-party service without the maker's explicit say (charter). Screening material stays in the room.
- **Strangers.** Two sessions are decided (W-43): S1 with one or two strangers to her on the slice about Sun 20 Dec (or the cold self-read with Fable's rubric pass) and S2 with three to five on the locked cut in week 17, both on a redacted copy. Recruit strangers to her with the truthful, partial pretext in the playbook. Never reveal who she is, or that it is a surprise. Show only what is cleared for the public cut.
- **Brand.** Do not use unlicensed marks, logos or trademarks. The game-style look is retired (D-29). The reconstruction marker is her own hand-made material, filled at G1 (Sun 15 Nov); where it is seva craft it is the making, never the finished seva article (W-38).
- **Her Hindu world (D-28, W-61, W-66, W-70).** No deity is drawn, generated or photographed under the default policy P1; no AI route touches a deity; shared or ambiguous motifs are out by default and the maker overrules one line at a time in a log; nothing in seva is photographed, touched or handled without her knowing (PR4); the three places (Somnath, Dwarka, Ayodhya) appear only under the three-places rule (W-71).
- **Labels.** List every changed region in `steps.csv`. Colourised shots carry "colours estimated."

## References

- Decision register (source of truth): `DECISIONS.md`
- Playbook (reasons, exercises and full templates): `playbooks/cinematic-quality.md`
- Hindu visual language (respect rules, the `hindu_idiom` block, the phone floor table): `playbooks/hindu-visual.md`; phone files and the phone-safe frame: `playbooks/mobile-delivery.md`
- Research notes (evidence and limits): `research/cinematic-quality.md`
- Charter: `CHARTER.md`
- Measurement scripts: `research/cinematic-quality-fixtures/` (README there). Copy a script out and run it with `python3 -I`.
  - `zoom_velocity_classifier.py` reads an mp4 and prints `ends`, `cv`, `peak`, `twos` and `roughness` (push and pull ease, MO1b and MO2).
  - `mo8_audit.py` audits MO8 on any renderer's output, a video file or a folder of PNG frames (`mo8a_centre_jit_px`, `mo8b_d4_px`, `mo8c_rough`; it needs `zoompan_vs_subpixel_prints.py` and `zoom_velocity_classifier.py` beside it).
  - `pan_estimator.py` reads a clip and prints the pan speed verdict (MO6; `python3 -I pan_estimator.py clip.mp4 24`; validated, M-C9).
  - `pan_ease_classifier.py` reads a clip and prints the ease class, family and family key of a translation-only pan or tilt (MO1b, MO2, MO9; `python3 -I pan_ease_classifier.py clip.mp4 24`; validated, M-C11).
  - `ab_push_card.py` writes the venue A/B push card, its answer key and a recording sheet (`python3 -I ab_push_card.py OUTDIR`).
  - `venue_calc.py` turns the six venue answers into luminance, grading gamma, hidden shadow level, seat distances, type floors and jitter in arc seconds (`python3 -I venue_calc.py venue.json`).
  - `windows_check.py` runs the checks on the maker's PC and records versions and hashes (`py -3 -I windows_check.py C:\LJ\check --font ... --font-name ... --ffmpeg ...`).
  - `caption_xheight.py` measures caption x-height in the maker's font. `gen_synthetic_pushins.py` and `zoompan_vs_subpixel.py` need `still.png` in the working directory; copy each out and run it with `python3 -I`.
  - The flicker index and the grain autocorrelation are not saved as scripts yet.
- Baked grain: the 8-frame loop on twos is the `grain-8f-on-twos` template, described in `research/agent-pipeline.md` (M6).
- Label ladder and gates: `playbooks/ai-imagery.md` [P2] and `playbooks/agent-pipeline.md` [P3]

Key sources, numbered as in the playbook and the research notes:

- [23] Making Flow, interview with Gints Zilbalodis: https://www.blender.org/?p=93732 (fetched)
- [27] Flee interview: https://seventh-row.com/?p=45371 (fetched)
- [31] Ralph Eggleston on Inside Out: https://www.awn.com/animationworld/ralph-eggleston-talks-inside-out (fetched)
- [33] UHD Alliance, ambient light compensation for Filmmaker Mode: https://alliance.experienceuhd.com/wp-content/uploads/2025/10/UHDA-White-Paper-on-Ambient-Light-Compensation-for-Filmmaker-Mode-v4-clean.pdf
- [34] DCI Digital Cinema System Specification v1.4.4: https://documents.dcimovies.com/DCSS/42cfeb997ae72dd484f7b027547e6e0bfad43ecf/Digital%20Cinema%20System%20Specification.pdf
- [35] DCI Compliance Test Plan 1.4.1: https://documents.dcimovies.com/CTP/release/1.4.1/ (superseded for the reference white and ambient figures by [91][92][93]; the 48 cd/m² figure was search-result text only)
- [39] TestUFO black levels: https://www.testufo.com/blacklevels (fetched)
- [40] CIEDE2000 documentation: https://metricgate.com/docs/delta-e-ciede2000/ (fetched)
- [41] RED, camera panning speed: https://www.reddigitalcinema.com/red-101/camera-panning-speed
- [42] Film grain synthesis for AV1 (Norkin and Birkbeck): https://norkin.org/pdf/DCC_2018_AV1_film_grain.pdf
- [44] Banding in gradients: https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps (fetched)
- [45] EBU R 95, safe areas: https://tech.ebu.ch/docs/r/r095.pdf (June 2017, Ver. 1.1, with 2016 errata)
- [47] Legge and Bigelow, does size matter for reading: https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf
- [54] Poynter on Ken Burns: https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect (fetched)
- [56] SIL Open Font License FAQ: https://openfontlicense.org/ofl-faq/ (fetched). Video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video. Commercial fonts follow step 10 [109].
- [57] Retired under D-29 (a game-licence excerpt); no longer cited.
- [59] Portrait editing demographic audit: https://arxiv.org/abs/2602.16149
- [60] AgeBooth: https://arxiv.org/abs/2510.05715
- [61] DiverAge: https://arxiv.org/abs/2606.04881
- [68] CRAFT.md, timing and review rules (third-party guide): https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md (fetched)
- [69] GSAP eases: https://gsap.com/docs/v3/Eases/ (fetched)
- [70] Six tips for a test screening (Frame.io): https://blog.frame.io/2017/07/06/successful-test-screening-tips/ (fetched)
- [72] Documenting architecture decisions (Nygard): https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions (fetched)
- [91] SMPTE RP 431-2:2011, D-Cinema Quality, Reference Projector and Environment (approved 6 April 2011; state "stabilized") — https://pub.smpte.org/latest/rp431-2/rp0431-2-2011.pdf — read in full (14 pages).
- [92] SMPTE ST 431-1:2006, D-Cinema Quality, Screen Luminance Level, Chromaticity and Uniformity (approved 18 April 2006; listed "active") — https://pub.smpte.org/latest/st431-1/st0431-1-2006.pdf — read in full (5 pages).
- [93] SMPTE ST 428-1:2019, D-Cinema Distribution Master, Image Characteristics (approved 12 February 2019) — https://pub.smpte.org/latest/st428-1/st428-1-2019.pdf — read in full (8 pages).
- [103] AudioTools STIPA Basic (Studio Six Digital; iOS only; vendor page): https://studiosixdigital.com/audiotools-modules-2/speaker-test-modules/stipa-basic/
- [104] Room EQ Wizard features, STI by the indirect method (free): https://www.roomeqwizard.com/features.html
- [105] Speech transmission index, bands and scores (Wikipedia; the standard was not read): https://en.wikipedia.org/wiki/Speech_transmission_index
- [109] Adobe Fonts Service Product Specific Terms, effective 7 October 2024 (read in full as text): https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Adobe-Fonts-Product-Specific-Terms-en_US-20241007.pdf
- [123] Hu, Ayton and Jolly, vernier threshold "as low as 2 to 5 arcseconds", Frontiers in Neuroscience 15:714843 (2021) (fetched): https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.714843/full

**Open gaps (TODO(research)).** The style bible is not written yet; its default path is `style/style_bible.yaml`, which does not exist yet. No film was watched for the notes, so shot-level camera ranges are unverified. Pan speed is validated (M-C9); pan ease is validated on translation-only pans (M-C11); orbits and per-layer eases are spec-only, and two-layer pans get the family right (4 of 4) but under-read travel. The visibility of 0.1 to 0.3 px of jitter on a screen is untested (FQ9). The Windows run is pending (FQ15). No validated method exists for cross-age identity on stylised faces. Hold lengths and the 48-hour rule are heuristics to calibrate on the first five slice shots. The venue, playback path and projector are unknown until the venue's written answer (due Sun 15 Nov, W-17), so every brightness number is a scenario. The phone numbers (PH1 grain at CRF 20, the 4 px floor, Gujarati KA sizing) rest on stand-in chat proxies and a Linux container; they are UNVERIFIED on the maker's PC and project Android until `windows_check_report.json` and `mobile-delivery` Exercises 2 and 5 are in.

## Changelog

- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18): OFL fonts only (W-21); venue ask, venue visit and rehearsal dated (W-17, W-52, W-56) with the test clip only at the visit; two stranger sessions (W-43); no model trained on her face (D-16); hard-chapter wording per D-04; voxel never the marker (D-23, W-38); maker minutes restated at 8 shots a minute (W-34, W-51). MO8 wording already matched W-41.
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): twelve-decision style bible (W-38, W-59); W-42 shot-brief fields and the gated versus reported split for chapter checks; phone-safe frame, Gujarati sizing, the 4 px floor and the PH1 grain rule added to steps 10 and 11 (W-18, W-63, W-64); Hindu-world checks HW1 to HW5 and T5 items 28 to 39; S1 at one or two strangers (W-43); the game-style brand rule retired (D-29).
