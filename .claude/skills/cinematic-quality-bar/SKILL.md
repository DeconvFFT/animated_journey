---
name: cinematic-quality-bar
description: Checks and builds the theatrical quality bar for the Life Journey film, with per-shot and per-chapter tests for AI tells, motion and ease variety, colour, finish, type, reconstruction honesty and venue projection. Use when a shot brief, style frame, chapter, render, grade or screening plan for the film is planned, generated, reviewed or signed off, or when someone asks whether AI-assisted work looks like AI.
---

# Cinematic Quality Bar

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

1. **Read the sources.** Read `CHARTER.md` and the playbook. The style bible's default path is `style/style_bible.yaml`; use it unless the brief names another path. That path does not exist yet, so the first run stops here. If the file is missing, or it does not lock the ten decisions (T2), stop before generating or rendering, and report that. The measurement scripts that back the checks are in `research/cinematic-quality-fixtures/`; steps 6 and 7 name them.
2. **Check the shot brief.** Required fields: `output_level` (L0 to L5, the ladder in `playbooks/ai-imagery.md`), `because` (reveal, link, isolate, time or hold), `ease_family`, `mirrored: false`, `virtual_lens`, `era`, `beat`, the source photo IDs, and the `steps.csv` path. A missing field fails A1 or B1.
3. **Screen against the banned list (playbook T5).** Refuse any brief that asks for: a regenerated, restyled or animated real face in the public cut; blinks, mouth movement or speech from a still; generated hands in a photo shot; generated text or logos; a morph between two different people; a mirrored photograph; a cloned voice; AI-sung words; an invented person; skin smoothing; or invented teeth or eyelids.
4. **Pick only the allowed route for the label.** For restoration, prefer a plain upscale. If you restore, never change teeth, eyelids or jaw. For motion, environment movement that keeps the face region from the L1 or L2 photo is L4b. Whole-frame image-to-video on a face-bearing photo is L4b only if the maker's line-up passes; otherwise it is banned. Keep generated clips to 3 to 5 seconds. Re-anchor every generation to the original photo, never to the last output.
5. **Write the motion timing chart.** For each move, record displacement at 10, 25, 50, 75, 90 and 100% of its duration. Assign one of six families: in-out, out, in, settle, drift or hold-snap. Limits: push or pull up to 8% of frame; pan or orbit up to 5% of width and 3 degrees; pan no faster than 0.143 frame widths per second (11.4 px per frame at 1920) unless blurred or declared as a whip. Holds: at least 0.75 s after a payoff, 1.0 s after a punchline or reveal, and at least 1.5 s on a legible card.
6. **Run the spec lint (MO1, Crit).** Fail any move with a `linear` ease and no `drift: declared` in the brief. Fail any framework default: `power1.out` for GSAP, `ease` for CSS. Fail a chapter where more than 40% of eased moves share one ease string. Fail evenly spaced stagger offsets. Output one JSON line per shot with exactly these keys, in this order: `shot`, `ease_class`, `axis`, `duration_s`, `magnitude_pct`, `cv`, `ends_ratio`, `peak_pos`, `settle_ok`, `twos`, `roughness`, `family_key` (the T8 lint line in playbook T8). Fill the spec fields first (`ease_class`, `axis`, `duration_s`, `magnitude_pct`, `family_key`). The pixel fields (`cv`, `ends_ratio`, `peak_pos`, `settle_ok`, `twos`, `roughness`) come from step 7, or are `unknown` for any move the estimator does not cover. The T8 line has no field for the drift declaration or the framework-default check, so record those results under MO1 in the step 12 report.
7. **Audit the pixels before grain (MO1b, MO6, MO8).** Run the zoom-velocity estimator on pushes and pulls only: `ZV_SIZE=1920x1080 python3 -I research/cinematic-quality-fixtures/zoom_velocity_classifier.py shot.mp4`. It reads an mp4 and prints `ends`, `cv`, `peak`, `twos` and `roughness`; without `ZV_SIZE` it runs at 240 by 135. It was validated on synthetic push-ins at 540p and, as a reconstruction, on three public-domain scanned prints at 1080p from 4K and native sources (M-C7b, 51 clips); on faint prints the floor rises (0.056-0.076 after H.264 on the faintest), so always render the Pillow reference from the same source file. For pan speed (MO6), run `python3 -I research/cinematic-quality-fixtures/pan_estimator.py clip.mp4 24` on the delivered 1080p file. Pan speed is validated (M-C9); pan ease is not, so keep `cv`, `ends_ratio` and `peak_pos` as `unknown` for pans. Report tilts, orbits and multi-plane moves as `unknown`, never `pass`. MO8 passes only when roughness is no more than 1.3 times a Pillow sub-pixel reference render of the same move and centre jitter is at most 0.05 px at 1080p on the delivered file (MO8a; edge jitter at most 0.04 px, MO8b, decides ties). There is no absolute roughness threshold: the floor read 0.13, 0.19, 0.076 and 0.064 on four synthetic stills and 0.03 to 0.08 on three real prints. The reference is a Pillow render of the same move; `zoompan_vs_subpixel.py` makes one for its 4% push (copy it out, put `still.png` in its folder, run it with `python3 -I`, and use `pil_slow.mp4`). Do not use ffmpeg `zoompan` for finals. Unless-blurred and declared-whip pans stay a human call, because the estimator measures content shift, not blur. The flicker index and the grain autocorrelation are not saved as scripts yet; mark them `unknown` until they are.
8. **Finish once.** Add only layers from the era's finish stack. Count the global layers: grain, vignette, letterbox, flare, bloom, halation, dust, scratch, light leak, colour filter and shake. The limit is two or fewer. Run the finish-off test: silhouette, value and colour must still hold without the finish. Bake grain as at least 48 distinct frames with a seeded start per shot. Autocorrelation at the loop length must be under 0.3. Grain spread on new layers must sit within 30% of the scan's flat patch. Blur depth planes per layer, never per pixel, and never blur faces for depth.
9. **Check colour numerically.** Compute the median and three dominant colours in CIELAB. Compare with the era swatches using ΔE00. Limits: within 6 for the shot, within 4 for skin, and within 3 across shots in one scene (J; calibrate on the first five slice shots). Plot the chapter as a colour strip beside the script.
10. **Check type and graphics (TY1, TY3, TY4).** For type we set (titles, cards, date lines, captions and credits): font at least 5% of picture height, x-height at least 2.5%, strokes at least 2 px at 1080p. Text inside photographs and her handwriting is exempt. Below 2% x-height, text is decorative and must not carry information. If text inside a photograph carries information, repeat it on a card or caption (TY4). Captions follow `format.md` Step 8 (7 to 8% line height), which at 1080p is `FontSize=23`: x-height 3.2 to 3.8% of picture height across five fonts, line pitch 7.96% (M-C8). Caption x-height floor 3.1% (6 screen heights, J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font; TY1 is a floor, not a caption size. No saturated 1 px lines. Text and graphics inside 5% margins. A licence file for every font, texture and plate.
11. **Check the venue risks.** Story-critical detail must sit above 10% signal. After the access-copy encode, thin lines keep at least 90% of their contrast, and flat-patch grain stays at 70% or more of the master's. Record the playback path the shot was graded for.
12. **Write the shot report.** Use one table with every T1 item from the playbook: pass, fail or unknown, plus the evidence file name. Mark each item Agent or Maker. Estimated maker minutes per shot (J, to time on the slice): class A about 3 to 4 (AI1 2, AI3 1 where visible, FN2 1); class B about 2 to 3 (AI1 1 on moving graphics, AI3 1 where there is text, FN2 1); class C about 9 (A4 1, AI1 2, AI3 1, FN2 1, FN4 2, FN5 1, C7 1), plus 10 for each L3 or L4b face shot (A3, two sittings 48 hours apart); class D about 1 to 2 (AI3 1 where there is text, FN2 1). For class A the minimum set is every Crit item that applies to the shot, plus B1, B8, C1 and FN1; MO9 and FN3 are checked once per chapter. The per-minute total (about 45 maker minutes per finished minute before A3, J) goes to `production-scale.md` as a delta.
13. **Leave maker items open.** Never mark these as passed: A3 (blind line-up), A4 (eyes and mouth), AI1 (tell sweep), AI3 (hands, text, reflections), FN2 (finish-off test), FN4 (cut-out edges), FN5 (light wrap), C7 (light direction) and PR1 (banding). Write "maker to check" beside each.
14. **Assemble and check the chapter (G4).** In every run of eight moving shots: at least three move families, none above 40%, no family more than twice in a row, and entropy of at least 1.5 bits. Held shots should be at least 35% of photo shots. Include at least one picture-led silence of 3 s or more. Shot-length coefficient of variation should be at least 0.4 (J). No finish layer on more than 80% of shots. Make a contact sheet at one frame per second for the AI-tell sweep. Captions stay within reading limits. A loudness plan must exist.
15. **Log deviations.** For any rule you bend, add a decision-log entry in the T8 format, with `evidence` and `reversible` filled in.
16. **Hand off.** Return the report and the list of open maker items. Do not publish, share or upload anything. Do not send personal material to a third-party service without the maker's explicit say (charter).

## Checklists

**Per shot, before handing off**

- [ ] Brief has every required field, and the label matches the ladder.
- [ ] No banned tell is present (playbook T5).
- [ ] Every move has a reason, its limits are met, the spec lint passes, and no default ease is used.
- [ ] Pixel audit run on pushes and pulls (MO1b, MO8), and `pan_estimator.py` run on pans (MO6). Pan ease, tilts, orbits and multi-plane moves reported `unknown`, never `pass`. MO8 passes only on the pixel rule and the 1.3 times reference check.
- [ ] Finish layers counted: two or fewer. Finish-off test queued for the maker.
- [ ] Grain baked with 48 or more distinct frames, seeded, and loop autocorrelation under 0.3.
- [ ] ΔE00 within limits for the shot and for skin.
- [ ] Type size, stroke width, margins and licence files pass.
- [ ] Every maker item is listed as open.

**Per chapter (G4).** The checks in step 14. After screenings, the independent marks per minute must be two or fewer.

**Before a venue screening (playbook T6).**

- [ ] Test card made: PLUGE, grey ramp, colour bars, skin stills, type ladder, line ladder, pan at four speeds, speech passage, and 30 seconds of the film.
- [ ] Run at least two weeks before 27 February 2027, and again on the day.
- [ ] Brightness, gamma and picture modes recorded. Motion smoothing, sharpening, noise reduction and dynamic contrast off; overscan off.
- [ ] Reference figures written down (SMPTE RP 431-2 s6.1, ST 431-1 Table 1): white 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2); gamma 2.6 ±5% in a theatre; ambient on the screen with the projector off below 0.01 cd/m² (Review Room) or 0.03 cd/m² (Exhibition Theater) [91][92].
- [ ] Back-row checks done for type and captions. Speech checked at STI 0.60 or higher if a meter is available.

## Quality bar: theatrical or mediocre?

Signs of theatrical work:

- The frame still works with the finish switched off.
- The frame could be about no one but her: her objects, her light and her palette.
- Camera moves are rare. Each has a reason, and each settles.
- Faces are unchanged from the source, or built by hand from the board.
- Type reads at the back row, and dark detail survives on the venue screen.
- Grain looks like film: spatially varied, not a repeating texture.
- A chapter varies its shot sizes, lighting, holds and move families.

Signs of mediocre, AI-looking work:

- Default ease, uniform stagger, or the same slow zoom on every photo.
- Stacked finish: grain, vignette, letterbox and flare on most shots.
- Generic lighting, centred epic compositions, a teal-orange grade, or over-saturated skies.
- Plastic skin, warped hands or text, morphing, or flicker in flat areas.
- Checks done only on a laptop.

The bar: a shot passes when every critical item passes, every major item is fixed or logged, no banned tell is present, and the maker has signed the maker items. A chapter passes at G4 when its checks pass and the strangers' marks are two or fewer per minute. Every rubric score (meaning, specificity, accuracy, feasibility, ethics, craft) must be 4 or higher.

## Ethics, rights and privacy guardrails

- **Real memories stay real.** Never regenerate, restyle with a model, or animate a real face in the public cut. Never animate the faces of the dead. A reconstruction must look like one and carry the disclosure marker.
- **Likeness belongs to the maker.** Agents never mark the blind line-up as passed. The maker signs five of five correct, twice, 48 hours apart. Decoy set A is the same stylisation applied to public-domain stand-in portraits listed in `ai-imagery.md` (NARA 546220 and US Navy 80-G-27208 among them, licences read on their Commons pages, re-check before use), or to the maker's own face. Never a relative's photo, who cannot be told why. Decoy set B is the same stylisation applied to her at other ages. Set A tests likeness; set B tests age discrimination.
- **No model of her face without her knowledge.** The default is no. Training happens only with the maker's explicit decision, local training, deletion afterwards and labels.
- **No invented events, people or words.** No voice cloning, no AI-sung words, and no new sentences in her handwriting. Her handwriting is used only for words she actually wrote.
- **No mirrored photographs.** A flip changes a parting, a ring hand and any text.
- **Dignity.** Hard chapters (loss, illness, separation, money, conflict) stay out by default. The Fable advisor flags sensitive material for the maker's decision.
- **Privacy.** Do not upload personal material to any third-party service without the maker's explicit say (charter). Screening material stays in the room.
- **Strangers.** Recruit with the truthful, partial pretext in the playbook. Never reveal who she is, or that it is a surprise. Show only what is cleared for the public cut.
- **Brand.** Do not use the Minecraft name as a title, and do not use unlicensed marks. Do not make a voxel look the reconstruction marker until the games and theatrical-delivery tracks resolve the usage rules [57].
- **Labels.** List every changed region in `steps.csv`. Colourised shots carry "colours estimated."

## References

- Playbook (reasons, exercises and full templates): `playbooks/cinematic-quality.md`
- Research notes (evidence and limits): `research/cinematic-quality.md`
- Charter: `CHARTER.md`
- Measurement scripts: `research/cinematic-quality-fixtures/` (README there). `zoom_velocity_classifier.py` reads an mp4 and prints `ends`, `cv`, `peak`, `twos` and `roughness`. `pan_estimator.py` reads a clip and prints the pan speed verdict (MO6; `python3 -I pan_estimator.py clip.mp4 24`; speed is validated, ease is not). `gen_synthetic_pushins.py` and `zoompan_vs_subpixel.py` need `still.png` in the working directory; copy each out and run it with `python3 -I`. The flicker index and the grain autocorrelation are not saved as scripts yet.
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
- [56] SIL Open Font License FAQ: https://openfontlicense.org/ofl-faq/ (fetched). Video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video; commercial fonts need their EULA read for film titling and public exhibition.
- [57] Minecraft usage guidelines excerpt (local): research/sources/minecraft-usage-guidelines-2026-10-18.txt
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

**Open gaps (TODO(research)).** The style bible is not written yet; its default path is `style/style_bible.yaml`, which does not exist yet. No film was watched for the notes, so shot-level camera ranges are unverified. Pan speed is validated (M-C9); pan ease is not. Parallax is untested for the motion estimator. No validated method exists for cross-age identity on stylised faces. Hold lengths and the 48-hour rule are heuristics to calibrate on the first five slice shots. The venue, playback path and projector are unknown, so every brightness number is a scenario.
