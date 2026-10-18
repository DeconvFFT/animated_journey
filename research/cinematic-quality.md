# What makes animation theatrical, and how AI-assisted work avoids looking like AI — research notes

Track `cinematic-quality` · Sonnet researcher · read and measured on Sunday 2026-10-18 · premiere Saturday 2027-02-27 (about 19 weeks).

**How to read this.** Numbers in square brackets point to the Sources list at the end. Labels used throughout:

- **(M)** = a measurement I ran on 2026-10-18 in the cloud container on made-up test material only (ffmpeg 6.1.1, Python with numpy and Pillow). Scripts are in research/cinematic-quality-fixtures/ and described in Sources item [76]. No family material was used.
- **(J)** = my judgment, not a sourced fact. Every (J) threshold is a starting value to be calibrated on the first five slice shots.
- **UNVERIFIED** = I could not confirm it, or I saw it only as a search-result snippet.
- **Vendor** = the source sells the thing it describes, so treat its numbers as marketing until confirmed.
- "Search-result only" in the Sources list means I saw the claim in a search result but the page itself would not load (paywall, 403, 405, 503). Those claims are weaker.
- Project playbooks are cited as [P1] `animated.md`, [P2] `ai-imagery.md`, [P3] `agent-pipeline.md`, [P4] `reviews/02-film-briefs-review.md`, [P5] `CHARTER.md`. Label levels L0 to L5 are the ladder in [P2].
- I could not watch any film. Everything below about films comes from interviews, breakdowns and reviews. No shot-level claim has been checked against footage.
- Dating: AI claims older than six months at the time of writing (before about 2026-04-18) are used only as history or background and are dated where they appear: Air Head [12] and the TechCrunch review [13] (2024), the Critterz pitch [10] (2025-09), FLUX Kontext [62] (2025-06), AgeBooth [60] (2025-10), MIT Technology Review [18] (2025-12), CodeFormer [63] (2022), the AV1 grain paper [42] (2018). Everything else cited for AI tools or festivals is from 2026.

**Context from the maker (relayed this session).** The maker is the only person on this project and the only person who knows about it: "for now only me and I will be the only one on this project." So this note never relies on a relative to check likeness, dignity or taste. The only fresh eyes available are strangers-to-her (protocol D6), and the maker is the proxy for hard chapters with the Fable advisor flagging, as in [P4]. Where [P2] or [P3] say "ask a relative" or "trusted relative", see "Deltas to existing playbooks" near the end.

---

## Summary

1. **The bar is a set of tests, not adjectives.** I deliver six artifacts (per-shot checklist D1, style-bible template D2, dailies rubric D3, banned cheap-tells list D4, projection-truth checklist D5, strangers' test-screening protocol D6). Every item has a frame-level or clip-level pass/fail test. Several tests are machine-checkable and I validated the core ones on synthetic clips (zoom-velocity ease classifier, flicker index, hold-on-twos detector, grain-loop detector, thin-line survival).
2. **Sameness is the bigger risk than glitches.** The default ease in GSAP is `power1.out` [69], agent pipelines default to uniform eases [P3][68], and 2026 critics describe festival AI work as "boring" [4] or pulled toward "the average or the mean" [5]. The defence is specificity: her palette, her objects, her light, sampled from her own scans.
3. **Festival laurels are weak evidence.** Runway's AIF is run by the tool vendor, its jury includes Runway's CEO (general knowledge), its prizes are partly Runway credits, its entries must use generative video, and one of four judging criteria is "creative and skilled use of AI techniques" [1][2]. WAIFF's own prize list shows *Costa Verde* winning the sponsor's "CapCut Prize", while a LinkedIn post (search-result only) calls it Best Film [7]. Cannes' main festival director talked about labelling films "made without artificial intelligence" [9].
4. **What the AI winners actually did is a lot of human work.** Gaudette: reference images and character sheets first, "a few tries" to "dozens" per shot, conventional editing, and reportedly two weeks of 17-hour days alone (about 30 hours per finished minute, my arithmetic on a secondhand figure) [3][4]. Air Head: 2 to 3 seconds kept from 20-second generations, balloon colour fixed in post [12]. Costa Verde: family photos and landscape documentation as references, Midjourney and MiniMax, one real filmed shot (the last shot, per a search-result snippet) [6][20]. TechCrunch's 2024 review (older than six months, historic) found that the human parts (performance, cinematography) carried the films [13], and 2026 coverage still reports several "boring" entries [4].
5. **Non-AI calibration shows what "theatrical" costs.** Away: one person, 3.5 years, 75 minutes (about 140 hours per finished minute, my estimate) [24]. Flow: 15 to 20 people, 3 to 5 at a time, about 5.5 years, no compositing, colour done in shaders, 0.5 to 10 seconds per 4K frame on one PC [23]. Danse Macabre (Annecy 2026): 75 oil paintings over 11 years, 30+ artists, a "fenced" AI stylisation pass trained on the painter's own surfaces, nearly every frame still corrected by hand, global grain as the last unifying step [21][22].
6. **A style bible is short, visual and has a "good / not good" page.** Flee's bible fixed how to draw a hand and an eye and showed "this is good / this is not good" from early tests [27]. Ours locks ten decisions before the slice (D2). Two are specific to this film: the reconstruction marker and the still-to-moving ratio.
7. **A colour script is a shorthand of emotion in colour and light** [31], made early and revised when the story changes ("I had to chuck it and start over" [31]). For a life film I propose one strip per era plus a numeric check of every shot against it (ΔE00 on the shot's dominant colours) and a venue test card (D5). Venue brightness is the hidden variable: a 5,000-lumen projector on an 8 m screen gives about 44 nits (my arithmetic), against the 48 cd/m² cinema reference [35], and ambient light erases shadow detail that the 5 cd/m² reference surround preserves [33].
8. **Gamma assumptions move shadows a lot.** The same dark code value is 37% darker on a 2.6 display than on a 2.4 display and 58% brighter on a 2.2 display (my arithmetic). Decide the playback path (DCP at 2.6 or HDMI at 2.4) in week 2 and grade for it, not for the laptop.
9. **No source I found validates identity for a stylised person across ages.** Research shows an identity-versus-age trade-off [60][61], iterative-edit drift [62], and demographic drift in 2026 portrait editors (62 to 71% of outputs lightened skin in one audit [59]). The honest plan: faces are built by hand from a per-age reference board; the maker alone signs likeness by blind line-up; strangers can test only whether the film reads as one person across ages, not whether it is her.
10. **The ease/hold test works and is cheap.** On synthetic push-ins my zoom-velocity estimator separated linear (coefficient of variation 0.03), ease in-out (ends at 0.16 of peak, peak at 0.48 of the move) and ease-out (peak at 0.00) and detected holds on twos (M). It also found that ffmpeg `zoompan`, which [P2] uses for its push-in example, is about 2.7 times rougher than a sub-pixel resample on a slow 1080p push (roughness 0.35 against 0.13) (M). Ban `zoompan` for final pushes.
11. **Finish is where templates are born.** Real grain is spatially correlated and temporally independent [42]; an 8-frame baked loop on twos repeats every 0.67 s and is perfectly detectable (autocorrelation 1.00 at 16 frames, against 0.00 for fresh grain) (M). Grain cost 20 to 45 times the bits of the clean version at equal CRF on a flat ramp (M, upper bound). A dark 8-bit ramp showed 26 levels against 100 at 10-bit (M). A saturated 1-pixel line kept only 70% of its contrast through H.264 4:2:0 at 1080p, against 91 to 99% for 2 to 4 pixels (M).
12. **The AI-tells catalogue (Q7) has 23 rows**, each with cause, detection, fix, and a status of allowed, allowed with a label (ladder level) or banned. The core rule: nobody deliberately regenerates, restyles-by-model or animates a real face in the public cut. Environment motion with the face region kept from the L1/L2 photo is allowed with an L4b label; whole-frame image-to-video on a face-bearing photo is allowed with an L4b label only if the face survives the 5-of-5 blind line-up (A3), otherwise banned; faces of the dead are never animated [P2].
13. **Projection truth has numbers.** Pan no faster than one frame width per 7 seconds (0.143 frame widths per second, 11.4 px per frame at 1920) at 24 fps [41]. Type: font size at least 5% of picture height (x-height 2.5%) for text read from the back row of a hall where the back row is 5 screen heights away, derived from the 0.2 degree lower edge of fluent reading [47] with a 1.5 times margin (J). Graphics inside 5% safe margins [45]. Speech transmission index at least 0.60 ("good") [48].
14. **One-person review is a ritual set, not a department.** 48-hour rule (practitioner advice; I found no controlled study), blind A/B against the previous version, squint test [73], distance viewing, half and double speed, sound-off and picture-off passes, and an architecture-decision-record style log [72] so taste does not drift. Strangers (D6) test the public room; Gaiman's rule decides how to weigh their notes: believe the diagnosis, discount the fix [71].
15. **Scheduling conflict to resolve.** The brief puts the strangers' screening in week 17 (Sun 2027-02-07 to Sat 2027-02-13). [P4] puts picture lock on Sat 2027-02-06. A week-17 screening can then only drive sound, grade, title and caption changes. I recommend a second, smaller screening of the slice chapter in the week of the slice review (about 2026-12-20) so structural notes arrive while they are cheap.

---

## Findings by question

### Q0. What the earlier playbooks already settle (so this note does not repeat it)

- [P1] owns the disclosure convention (one hand-made material for everything never photographed, said once at the start, replaced by the real thing), time-passing devices and era-by-medium (change the medium on the new layer only; do not age scans that are already aged).
- [P2] owns the label ladder L0 to L5, restoration honesty (reject new teeth, eyelids, jaw), the Route A/B/C/D choices for stylising a face, and the parallax limits (orbit 2 to 3 degrees, push 3 to 8%).
- [P3] owns gates G0 to G6, the validators, shot classes A to D, and the baked-grain rule. It already bans uniform easing in principle 5 and lists template anti-patterns. What it lacks is the measurable test and the chapter-level variety rule. Those are in Q5 and D1/D3.
- [P4] sets picture lock at 2027-02-06, "2K-safe 1080p at 24 fps", and the strangers-to-her screening in week 17.

### Q1. What a style bible contains, with real examples, and the ten decisions to lock

**What I found (and its limits).** I saw descriptions of real bibles, not the documents themselves. No full bible was publicly viewable. That is itself a finding: even studios share them as a few pages, and the useful parts are rules and "good / not good" pairs.

| Example | What it shows | Source |
|---|---|---|
| *Flee* (2021) | A "big art bible where we gathered references"; roughly fifty animators had to keep one character's eyes consistent ("it's super important that they don't draw his eyes differently from one scene to the other"). It specified how to draw a hand or an eye, showed "this is good" and "this is not good" examples built from early tests, and named light and composition references (Edward Hopper for light, Ray K. Metzler for composition and colour). Lines were meant to feel "alive", not "too straight and smooth", and "we couldn't afford to have a lot of detail" shaped the style. | [27] |
| *The Simpsons* early style guide (about 1990) | A "nearly 500-page" guide made of micro-rules, for example Lisa's hair always shows eight points "clustered in groups of two or three" from any angle, and the neck line always connects into the body and arm lines. Shared on social media by a former showrunner. | [29] |
| *Sprite Fright* (Blender Studio, 2021) | A style guide written by the lead animator to onboard new animators. Public summary: "mostly shot on 2s" with ones for ultra-fast motion, plus rules for cartoony posing, bendy limbs, smears and expressions. The full guide is for subscribers, so I saw only the summary. | [26] |
| Generic art-bible structure (Oleander Studios) | Typical sections: artistic guidelines, technical guidelines, colour palette, scale reference, stylisation (shapes, linework), aspect ratio, render quality, value ranges for back/middle/foreground, picture references, how to deliver artwork, "what not to do", naming conventions, proportions. Practical tips: put "Do's" and "Don'ts" side by side, explain why, keep the layout simple, one or two pages is fine for a personal bible. | [28] |
| Character sheet contents (cg-wire, updated 2026-03-26) | Turnaround (front, profile, back, three-quarter), expression sheet, pose sheet, props with scale, colour palette with codes, and written annotations ("you need to write things down to avoid guesswork"). | [30] |

**Lessons that transfer to a one-person, photo-forward film.**

- Keep it to a few pages plus a frozen "good / not good" board. Add a rule only when a test shot failed without it.
- Every rule needs a test (see D2: each decision has a "how we check" line).
- A bible is also the memory that stops taste drifting over sixteen weeks (see Q9).

**The ten decisions to lock before the slice.** Full fillable form in D2. In short:

1. Palette per era, sampled from her scans.
2. The hand-made material (L5) and its rules.
3. Line and edge quality.
4. Typography and licences.
5. Camera grammar.
6. The reconstruction marker.
7. The still-to-moving ratio.
8. The grain and paper system (finish stack).
9. The title system.
10. The "never" list.

### Q2. Colour scripts: how they are made and used, a life-film version, and checking the grade on the venue screen

**How they are made and used.**

- Ralph Eggleston described a colour script as "a shorthand version of the film that covers the emotions of the film in color and light." He started with pastels ("just a shorthand for me"), and for *Inside Out* painted five or six hundred panels and narrowed them to about 200. Panels could be moved around like a storyboard. He gives lighters a goal rather than dictating looks ("What's the bigger picture goal?"). When the story changed he sometimes had to "chuck it and start over" [31].
- Lou Romano made the colour script for *Up* and says he tried to give more lighting detail than the "abstract scripts, which are more for tone." The reported colour arc: the film opens heavily saturated, Ellie brings colour into Carl's life, his life turns "mundane and colorless" after her death, and colour returns with the memory of Ellie and again when Carl sets out with Russell; adventure scenes are bright and danger scenes dark [32]. Colour carries an emotional meaning that the audience learns, which is the same test [P5] principle 2 applies to every device.
- I could not view the *Up* colour script images. The book *The Art of Pixar: The Complete Colorscripts from 25 Years of Feature Films* collects them, reportedly [85 (search-result only)].

**A version for a life film (my synthesis, J).** Do not copy a studio department. One person builds it in about two hours per era:

1. After the animatic (one frame per beat, 30 to 60 beats for 10 to 12 minutes), choose one frame per beat.
2. Reduce each beat to 3 swatches: dominant, secondary, accent. Do it by hand in the first pass; a script can later compute k-means in Lab per shot (colour-scheme extraction from shots is an active research topic [79 (search-result only)]).
3. Lay the swatches in a strip where each beat's width is proportional to its running time. Above the strip draw one line: the emotional temperature (a single curve of "warmth of memory" or whatever the maker chooses as the meaning of colour).
4. Add a second row of light type per beat (window light, lamplight, overcast, flash, none).
5. Freeze it at gate G1 for the slice and revise per chapter, keeping a dated copy (decision log).

Proposed eras for the strip (placeholders until the maker has her material): childhood (0 to 12), youth (13 to 22), early adult and family (23 to 35), middle years (36 to 49), now (50 plus). Each era gets one base palette of six colours or fewer (the [P3] G1 limit), one skin-tone swatch sampled from her face in that era's scans, one accent colour reserved for a recurring object, and one grain/paper treatment (decision 8).

**How the maker checks the final grade against the script.** Three checks, cheapest first:

1. **Numbers (agent-run, pass/fail).** For each shot compute its median colour and three dominant colours in CIELAB. Compare to the era swatches with ΔE00 (CIEDE2000). Reference bands: below 1 generally not perceptible, 1 to 2 perceptible only on close side-by-side inspection, 2 or more an increasingly obvious mismatch [40]. These bands are for flat patches; images tolerate more, so my proposed tolerances (J): era-mean shot colour within ΔE00 of 6 of the era swatch; shots inside one scene within 3 of each other; skin patch within 4 of the era skin swatch. Plot the film as a colour strip next to the script.
2. **Eyes on the TV (maker, weekly).** Squint and greyscale (Q9), then the strip beside the script.
3. **Eyes at the venue (maker, before the premiere, D5).** Play a test card and three skin-tone stills on the actual screen with the lights as they will be at the event.

**Rec.709 at gamma 2.4 in a dim room, and what moves.**

- BT.1886 is the reference EOTF for HD video, approximately a gamma 2.4 power function. Poynton's notes describe mastering at 2.4 gamma, 100 nit reference white and about 1 lux ambient, and say a living-room consumer set measures around gamma 2.2 [36 (search-result only)]. The Wikipedia BT.1886 entry describes it as a gamma 2.4 power function approximating a CRT [77 (search-result only)].
- The UHD Alliance says Filmmaker Mode "has worked great when the viewing conditions of the consumer match the reference viewing environment (a dim-surround color grading suite at 5 cd/m²)." With elevated ambient light, the eye adapts and "shadow detail that is visible in a reference dim surround" falls "below the threshold of visibility," giving "a perceived loss of image detail and a darker overall picture." Their compensation is a gamma below 1 applied to the image: 1.0 at a 5 cd/m² surround, 0.98 at 10, 0.954 at 20, 0.913 at 40, 0.859 at 80 [33].
- Arithmetic for the same code value shown under different display gammas (M-arithmetic, relative luminance): code 0.10 gives 0.0063 at 2.2, 0.0040 at 2.4, 0.0025 at 2.6, so 2.6 is 37% darker than 2.4 and 2.2 is 58% brighter; code 0.50 is 13% darker at 2.6 and 15% brighter at 2.2; code 0.75 is 6% darker at 2.6 and 6% brighter at 2.2. Shadows move most, and shadows are where faces in dark rooms live.

**What changes in a DCP's XYZ conversion.**

- A DCP image is 12-bit X'Y'Z' (gamma-encoded), 2K is 2048 by 1080 at 24 or 48 fps, and the projector converts to its native colour space; maximum picture bit rate is 250 Mbit/s, which is 1,302,083 bytes per 24 fps frame [34 (DCSS 1.4.4, approved 2024-01-03)].
- DCI's reference white is 48.0 cd/m² with a ±3.5 tolerance in the compliance test plan, and ambient light reflected by the screen must stay under 0.01 cd/m² for the test [35 (the 48.0 ± 3.5 figure is from search-result text; the 0.01 figure I fetched)]. I did not read SMPTE RP 431-2, which the specification makes normative for the reference projector and viewing environment [34].
- Practitioner notes (DCP-o-matic mailing list, search-result only): Rec.709 source is often treated as 2.2 and the colour conversion has to account for DCI projection at 2.6; modern gear labelled Rec.709 usually means BT.1886; choosing the wrong input gamma gives a visibly lighter or darker picture; "the only reliable check is a properly calibrated cinema screening" [37]. DCP-o-matic describes itself as "free and open-source" [58].
- My conclusion (J): the maker must decide the playback path in week 2. If the venue plays a DCP, grade for BT.1886 (2.4) and convert with the matching input-gamma setting, then check a test DCP on a real cinema server. If the venue plays an HDMI or USB file, grade for 2.4 in a dim room or 2.2 if the lights stay up, and set the projector's gamma to match. The theatrical-delivery track owns the choice; this note supplies the checks.

**What consumer TV picture modes do.** Filmmaker Mode is a UHD Alliance preset that turns off most post-processing: motion smoothing off, D65 white point, sharpening and noise reduction off, overscan off unless signalled, aspect ratio and frame rate kept [38 (summaries in search results; the UHDA white paper [33] confirms the mode's purpose)]. "Vivid" and "Standard" modes typically add saturation, sharpening and motion interpolation (J; common knowledge, UNVERIFIED here). The test for the TV at 3 m in [P3] G6 should therefore state the mode used and record it.

### Q3. Identity across ages and shots

**Studio practice.** A model sheet or character sheet is the shared reference so every artist keeps a character recognisable: turnaround, expression sheet, pose sheet, props and scale, colour palette, and written annotations [30]. Flee had to stop fifty animators drawing one man's eyes differently [27]. The Simpsons guide encodes identity as micro-rules [29].

**Our equivalent for a real person in a stylised look (ai-imagery L3).** A **per-age reference board** (ages 6, 25, 55 as the brief says; add more only when a chapter needs them). Template in D2b. In short each board holds: 3 to 5 source photos with dates (L0/L1), a list of identity attributes (hair shape and parting, brows, eye set, nose, mouth, ears, glasses, posture, height relative to others), a stylised front, three-quarter and profile in the house material, five expressions only (neutral, smile, laugh, listening, tired), a head-height proportion chart, costume and colour swatches (skin swatch sampled from the scan), and a "do not" list with the failure examples.

**The rules.**

- A photograph stays a photograph: stylisation is a separate asset and never replaces a photo in a factual beat [P2]. Never synthesise a different age of her from a photo.
- **Likeness sign-off by the maker alone.** Protocol, run twice 48 hours apart: (1) the agent prepares a shuffled line-up of 5 stylised faces, one correct and four decoys (the same stylisation of other real people's photos that the maker supplies as stand-ins, or of her at other ages); (2) the maker picks without seeing labels; (3) pass is 5 of 5 correct picks, then pass again 48 hours later; (4) the maker records what feature tipped the choice, which becomes a board attribute. This replaces the relative line-up in [P2] Step 9, because the maker is the only person who may see her. (J)
- **Strangers test a different thing:** whether the audience believes the 6-year-old, the 25-year-old and the 55-year-old are one person, which is what the room will judge (D6). Strangers cannot judge likeness.
- **Embeddings are a screen, not a sign-off.** Face-recognition models score about 98% on the AgeDB-30 cross-age benchmark of real photographs [78 (search-result only; InsightFace mirror pages)], and I found no source reporting their reliability on stylised faces. Use landmark geometry (inter-ocular distance ratios, eye-line, mouth width) as a cheap drift alarm: flag a shot if any ratio moves more than 2% from the board's value (J), and send flagged shots to the line-up.

**Which approaches practitioners use, how they fail, and the honest limits (all dated; most sources are vendors).**

| Approach | How it is used | Documented failure | Status for this film |
|---|---|---|---|
| Reference-image edit models (FLUX.2 multi-reference, Qwen-Image-Edit-2511, FLUX Kontext) | Feed 3 to 6 reference photos (community advice; BFL's docs list FLUX.2 [klein] as "Apache 2.0 / FLUX Non-Commercial" and mention a "FLUX 3" family, undated [67]); BFL's own paper claims better multi-turn character consistency than rivals [62]; community guides recommend always re-anchoring to the original, because "feeding only the latest output back lets small changes accumulate" (search-result only, vendor guide) [65] | A Feb 2026 audit of three open-weight instruction-guided portrait editors on 5,040 edits found 62 to 71% of outputs lightened skin, 72 to 75% for Indian and Black source portraits against 44% for White ones (v3 revised 2026-06-04) [59]. Likeness is "fragile" when the face is small, shadowed or non-frontal [65]. | Route B in [P2]. Allowed with label L3, only with the board as the judge. |
| Identity adapters (InstantID, PuLID, InfiniteYou) | Generate a new picture of the person from a prompt | Invent pose, clothes and scene, so it is a reconstruction (L5) [P2] | Avoid; label L5 if used. |
| Per-person or per-age LoRA | Train on 15 to 30 images; AgeBooth fuses age-specific LoRAs to interpolate ages from one reference [60] | Identity and age trade off: stronger identity limits age change, and looser identity drifts [60][61]; a vendor reports ~96/100 face similarity for a trained LoRA against 80 to 85% for reference-only methods (search-result only, vendor) [65] | Not for the public cut by default. Training a model of her face without her knowledge is exactly what she cannot consent to; [P2] allows it only "with consent, local training, deletion afterwards and labels." Maker's explicit decision required. |
| Video "reference" modes (Veo ingredients, Kling Elements, Seedance reference packs) | Hold a character across shots | Vendor-adjacent comparisons say no single model solves project-wide consistency; one September 2026 vendor test scored 30 single-image attempts (search-result only; the site sells its own tool) [66] | Do not use to generate her face. |
| Age progression research | DiverAge (2026-06-02) adds inference-time guidance to suppress "excessive cross-age identity drift"; the abstract does not say which identity metric it uses [61] | One-to-many problem: one person can plausibly look different at a target age [61] | Research, not a tool I can recommend. |

**Honest limits.** (1) I found no source that validates a stylised, non-photoreal rendering of one specific real person across 6, 25 and 55. (2) Most "character consistency" claims are from vendors. (3) The safest reading of the evidence: treat each age as its own character, build the face by hand from the board, and use generative models only for non-face material.

### Q4. Virtual cinematography for stills-based film

**Principles from practitioners.**

- Poynter reports that Ken Burns treats a still as a filmmaker treats a long shot, with medium shot, close-up, pan, tilt or reveal as options. Burns says "any movement, however dazzling or frenetic, if it doesn't have meaning, it doesn't have a place," while also saying "there are times when you absolutely have to stop and look and drink it in." Another editor: "If it's a powerful image, I wouldn't mess around with it" [54 (Poynter, 2007-06-21)].
- *The Kid Stays in the Picture* separated subjects from backgrounds and panned them at different speeds, "creating a remarkably alive 3-D scene," described as an extension of the Burns move [53]. I could not find shot-level documentation (search results named no vendor or breakdown).
- Murch ranks the criteria for a good cut as emotion, story, rhythm, eye trace, the two-dimensional plane of the screen, and three-dimensional space, and says to sacrifice from the bottom up: "don't ever give up emotion before story" [55].
- The long-take floating camera in *Away* and *Flow* is the 3D cousin: *Away* used "many long takes with a freely floating camera to keep the visuals simple" [24]; Zilbalodis "like[s] to move the camera a lot", handles camera and lighting together, and tested live camera capture but found it "too imprecise," preferring keyframing and layering [23].

**Lens equivalence for 2.5D parallax (derivation, J, standard pinhole geometry).**

- A scan has one fixed perspective. A digital crop or zoom changes framing but not perspective and produces no parallax. A virtual dolly (camera translation) over separated layers produces parallax proportional to 1/distance.
- Pinhole shift between two layers at distances z1 and z2 for a camera translation t, as a fraction of frame width, is (f/W) · t · (1/z1 − 1/z2), where f/W is focal length over sensor width. Example: subject at 3 m, background at 12 m, a 0.15 m dolly:

  | Virtual lens (35 mm equivalent) | Horizontal field of view | Layer shift |
  |---|---|---|
  | 24 mm | 74 degrees | 2.5% of width (48 px at 1920) |
  | 28 mm | 65 degrees | 2.9% (56 px) |
  | 35 mm | 54 degrees | 3.6% (70 px) |
  | 50 mm | 40 degrees | 5.2% (100 px) |

- So the "3 to 8% push, 2 to 3 degree orbit" limits in [P2] correspond to small real dollies, and wide virtual lenses make less parallax per metre but stretch faces near the frame edge.
- **Defaults (J):** set the virtual camera to the photo's own 35 mm-equivalent focal length. Digital photos carry it in EXIF tag 0xA405 (zero means unknown) [52]. Film prints do not; assume 35 mm equivalent for snapshot prints and 50 mm for portraits unless the perspective clearly says otherwise. Keep faces central and use 35 mm or longer for any shot with a face in the frame's outer third.

**Staging a photograph in a 3D move without the paper-doll look.**

- Use at least three depth planes plus a ground-contact cue (shadow or occlusion). The "paper doll" is flat slabs with visible cut edges. Fixes seen in sources and practice: separate subjects and paint in the hidden background [80 (search-result only: tutorial summaries)]; use smooth depth maps for rounded form but flatten them across faces because depth maps bulge faces [P2]; blur far planes by layer, not per pixel, because per-pixel defocus produces halos at depth edges [51 (search-result only)]; add small atmospheric contrast loss per plane back (J, 10 to 20% per plane).
- **Tests:** freeze-frame the middle of every move at 100% and at 200% around cut-out edges; fail if an edge, a hole, a colour fringe or a flat slab is visible. Composite the cut-out over black, white and mid-grey; fail on any fringe (D1 item FN4).

**When to cut rather than move (decision rules, J).** Move only for one of four reasons, written in the shot brief as `because:` reveal, link, isolate, or time. Cut instead of moving when: the photograph is already a strong single image [54]; the emotion peaks and a move would add rhythm noise [55]; the needed shot size is not in the photograph (do not invent it); or the previous two photo shots both moved. Target at least 35% of photo shots as locked-off holds per chapter.

**Shot-size grammar for emotion (J, conventional film grammar, UNVERIFIED as a cited rule).** Wide shots for place and time, medium for relationship, close for feeling. For our film: first appearance of her in each era at medium or wider; close-ups reserved and counted (at most two per chapter) so they stay expensive; a chapter closes on a different size from the one it opened on.

**Screen direction and continuity across photographs decades apart.**

- Subjects facing screen-left in 1975 and screen-right in 1995 will reverse on a cut. In a time-skip montage that is acceptable; inside one sequence it jars. Fix by choosing camera drift direction rather than by flipping the photo. **Never mirror a photograph**: it changes a hair parting, a wedding ring hand, and any text, which breaks "real memories stay real" [P5]. Test: manifest field `mirrored: false` and text in the frame reads correctly.
- Eye-line continuity for portrait sequences: in a ladder of portraits, align the eye centre of consecutive portraits within 3% of frame width and height of each other (J); [P1] cites the five-point alignment used in the long-running daily-photo videos.
- Motion direction: push toward where the subject looks ("look room"), or hold; never drift away from the gaze without a `because`.

**Exemplars at shot level.** I could not verify any shot. The honest deliverable is an exercise: the maker (or an agent) logs shot size, duration, move and cut reason for 5 minutes each of three reference films (suggested: a Burns documentary sequence, *The Kid Stays in the Picture*, and a *Flow* long take) into the D1 table's columns, so our ranges come from measured examples rather than from this note's judgment. Marked as an open question.

### Q5. Motion quality for code-driven and agent-made animation

**Frame rate and twos.** 24 fps; drawn or paper layers on twos (12 drawings per second), camera and type on ones. Evidence: *Spider-Verse* animators chose twos because it is "crisper, it's pop art," modulated it within shots as "strictly a creative call", and had to make hair, cloth simulation and camera work cooperate with it [25 (Gizmodo, 2018-12-18)]. Secondary summaries (search-result only) say backgrounds and lens animation stayed on ones. *Sprite Fright* was "mostly shot on 2s", with ones for ultra-fast motion [26]. The pipeline craft guide says "Hold drawings on twos for characters... keep camera and type on ones" and "Subtle reads as nothing at 24 fps in a 3-second shot" [68].

**Easing families.** GSAP's core families are none, power1 to power4, back, bounce, circ, elastic, expo, sine, steps, with in, out and inOut variants; the default is `power1.out`. Extras: RoughEase, SlowMo, ExpoScaleEase, CustomEase [69]. So "I did not choose an ease" means `power1.out` everywhere, which is a tell. For our film I group moves into six **families** (J):

| Family | Velocity shape | Typical use |
|---|---|---|
| In-out | bell, zero at both ends | slow reveal, push on a held portrait |
| Out (decelerate) | fast start, long tail | arrival, settling onto a face |
| In (accelerate) | ramps up, ends at speed | leaving a shot (rare) |
| Settle | out with a small overshoot and return | physical objects, paper, titles |
| Drift | near-constant with micro-variation | environment, deliberate and declared |
| Hold-snap | steps | cut-paper animation on twos |

**Timing chart per move (needed by the test).** For every move write displacement at 10%, 25%, 50%, 75%, 90% and 100% of its duration, and the frames at which 10%, 50% and 90% of displacement are reached. The classic timing-and-spacing chart and the "ones and twos" chapter exist in Richard Williams' *Animator's Survival Kit* (table of contents seen; I did not read the chapter) [74].

**Settle, anticipation, hold.**

- Camera moves rarely anticipate; they do need a settle: velocity in the last 15% of the move decays to 5% of peak or less in the spec, 10% in a pixel audit, without a snap (D1 item MO3).
- A shot "plays its action to its conclusion, then holds"; the craft guide's numbers are at least 0.75 s after a payoff, at least 1.0 s after a punchline, reaction or reveal, a card held at least 1.5 s once fully legible, shots at least about 1.5 s except impact frames [68]. [P3] G2 already adopts 0.75 s.
- **How long a hold reads on a big screen.** I found no empirical source (UNVERIFIED). Heuristics (J): a big screen takes longer to scan, so scale laptop holds by about 1.25 times; hold a new photograph at least 0.5 s before any move starts and at least 2.5 s in total unless in a flagged montage cadence; hero portraits 4 to 8 s; Burns says duration itself can carry meaning, citing a 33-second zoom [82 (search-result only)]. Calibrate in the first screening (D6, question on pacing).

**The measurable test for uniform easing and repeated move families (agent-pipeline principle 5 and gate G4).** Two levels.

*Level 1: from the timeline spec (cheap, exact).* Parse `brief.yaml` or the OTIO keyframes. Fail if: any move has `ease: linear` without `drift: declared`; more than 40% of eased tweens in a chapter share one ease string; stagger offsets are evenly spaced; or the framework default ease string appears at all (`power1.out` for GSAP [69], `ease` for CSS).

*Level 2: from the rendered frames (audit, independent of how the shot was made).* I built and tested a small estimator (M). For each consecutive frame pair it fits the zoom about the frame centre by least squares (a linearised Lucas-Kanade step on the image gradient), then classifies the velocity curve. Results on 4-second, 24 fps, 960 by 540 synthetic push-ins from one textured still (10% total zoom, sub-pixel renders):

| Synthetic move | Measured ends / peak position / variation (CV) | Classified as |
|---|---|---|
| Linear | ends 0.94 / peak 0.13 / CV 0.03 | LINEAR (flag) |
| Cosine in-out | 0.17 / 0.48 / 0.49 | ease in-out |
| Cubic ease-out | 0.45 / 0.00 / 0.92 | ease-out |
| Back-out (settle) | 0.45 / 0.00 / 1.20 | ease-out (the small overshoot was inside the noise floor, so settle is not separable) |
| Linear on twos | 0.94 / 0.13 / 0.03, twos detected | LINEAR, twos |
| Cosine in-out on twos | 0.16 / 0.48 / 0.48, twos detected | ease in-out, twos |

Here "ends" is the mean speed in the first and last 12% of the drawings divided by peak speed, "peak position" is where the maximum falls from 0 to 1, and twos are detected when every other frame-to-frame step is nearly zero. Noise floor: frame-to-frame jitter of the estimate was about 0.12 (in units of 1e-3 log-zoom per frame) against peaks of 1.1 to 5.2, that is 2 to 11% of peak, so overshoots and tails below about 10% of peak are not reliably detectable from pixels. Proposed rules (J):

- Flag LINEAR if CV is under 0.12 over the move.
- A move with a settle has an end-speed ratio under 0.3 and a monotone decay over the last 15% of its duration (spec-level; the pixel audit cannot see small overshoots).
- **Family key** = (ease class, axis, duration bucket, magnitude bucket). Axis = push, pull, pan left, pan right, tilt up, tilt down, none. Duration buckets: under 3 s, 3 to 6 s, over 6 s. Magnitude buckets: under 3%, 3 to 6%, over 6% of frame.
- **Chapter rule:** over any run of 8 consecutive moving shots, at least 3 distinct family keys, no key above 40%, no key repeated more than twice in a row, and Shannon entropy of keys at least 1.5 bits. These numbers are a starting point to calibrate on the slice.
- Held shots count as their own family (`none`) and should be at least 35% of photo shots.

*Limits.* Tested on synthetic pushes only. Settle and overshoot checks therefore belong to the spec-level test (Level 1), with the pixel audit using a 10% tolerance. Pans should use phase correlation (not tested). Multi-plane parallax has one velocity per layer, so measure layers from the timeline spec and use pixels only as an audit. Run on the render before grain, because grain and compression noise raise the noise floor.

*A related finding that changes a recommendation.* On a slow 4% in-out push at 1080p from a 4K source, ffmpeg `zoompan` showed a frame-to-frame velocity roughness of 0.35 against 0.13 for a sub-pixel bicubic resample (M, same estimator, relative to mean speed). On a faster 10% push at 540p the gap was 0.26 against 0.08. `zoompan` snaps its crop window to whole pixels, which shows up as shimmer on slow moves. [P2] Step 8 uses `zoompan` in its example; keep it for proofs, not finals.

### Q6. Compositing finish and its limits, and the projector cautions

**Real grain versus synthetic.**

- Real film grain is spatially correlated (grains can be more than one sample in size), temporally independent (new each frame), and its strength depends on image intensity; independent per-pixel noise from a digital sensor has different statistics [42]. Plain per-pixel Gaussian noise therefore tends to read as "digital noise," not film (J).
- Danse Macabre's compositor applied "a global film grain over the entire composition" as the final unifying step [22]. Flow used no compositing at all; all colour was tweaked in shaders [23]. Two valid answers: finish once at the end, or design the finish into the render.
- **Matching rule that needs no taste (J):** measure the standard deviation of luminance in a flat patch of each era's scans; set grain on new (L5) layers within ±30% of that value, so the new layers sit with the photographs [P1] ("put the era on the new layer only").
- **Baked overlays.** [P3] bakes an 8-frame grain loop on twos. My test of that design (M): a loop of 8 distinct grain frames held on twos repeats exactly every 16 frames (0.67 s); frame-to-frame correlation at lag 16 is 1.00, against 0.00 for fresh grain at every lag. A viewer may not name it, but flat areas will "breathe" in a pattern. Use at least 48 distinct grain frames (4 s at 12 fps), start each shot at a different seeded offset, and test for a repeat with the same autocorrelation.

**Grain versus compression.**

- "Film grain... is difficult to compress using traditional coding tools"; prohibitively high bit rates are often needed to reconstruct it [42]. AV1's film-grain synthesis removes grain before encoding and re-adds it on playback, saving up to 50% on grainy material in the original paper and about 36% on average bit rate at 1080p and above in Netflix's report [42][43 (search-result only)].
- Measured here (M): a flat dark gradient, 2 seconds, H.264 CRF 18 — 7.8 KB clean, 162 KB with light noise (strength 4), 220 KB at 8, 282 KB at 16, 356 KB at 32. That is 20 to 45 times the bits for the same CRF on near-empty content, so treat the ratio as an upper bound; the direction is the point.
- DCP picture is JPEG 2000 with a 250 Mbit/s ceiling [34]. Rule (J): after encoding the DCP or the screening file, re-measure grain standard deviation in the same flat patch; if it fell below 70% of the master's, reduce master grain or raise the bit rate, because the grain is being smeared rather than preserved.

**Banding and 10-bit intermediates.**

- Banding comes from too few levels and from quantisation, and "film grain and sensor noise normally mask this by acting as natural dithering." Full-reference metrics largely miss it; Netflix's CAMBI is a no-reference banding score (around 5 "slightly annoying") [44]. Do not add dither immediately before a lossy encode, because the encoder removes it; add grain/dither as close to the final bitstream as possible [44].
- Measured (M): a smooth dark ramp spanning 100 ten-bit codes showed 26 distinct values in an 8-bit H.264 encode, with steps of one 8-bit level, against 100 distinct values in a 10-bit H.264 encode. Our masters are ProRes 422 HQ (10-bit) [P3]; a DCP is 12-bit [34]. The access copy is 8-bit H.264, so the risk is in the file played at the venue. Keep gradients out of dark, large, empty areas (sky, wall, vignette falloff) or give them real texture. Design fix first, grain second. Because the venue file is 8-bit H.264, invisible dither added just before the encode will be quantised away [44]; use visible grain or paper texture that survives, or a 10-bit encode if the venue playback machine accepts it (software players do; many hardware players do not, per a forum summary, search-result only). Test both at the venue.

**Depth of field on stills, atmosphere, light wrap, cut-out edges, vignette.**

- Depth-of-field: blur each plane as a layer, back to front; per-pixel depth defocus makes halos at occlusion boundaries [51]. Never blur faces for depth. Cap far-plane blur at about 1.2% of frame width (J).
- Light wrap paints a soft halo of the new background colour onto the subject's edge so a cut-out does not look pasted on. It belongs last in the chain, after the key and spill suppression; running it before spill suppression amplifies the spill. Core penetration should stay low [50]. For us: wrap only on L5 composites over photographs, edge only, and verify by the three-background test.
- Atmosphere: one tone shift per plane back, not a global haze.
- Vignette and letterbox: part of the stacked-finish count (below).

**The "stacked finish" failure.** Grain plus vignette plus letterbox plus flare reads as a template [P4]. It also hides weak design. Tests (D1 items FN1 to FN3):

1. **Count:** list global finishing layers on a shot (grain, vignette, letterbox bars, flare or bloom, halation, dust or scratches, light leaks, colour filter, camera shake, chromatic aberration). Pass is two or fewer, and every layer must appear in the era's finish stack in the bible.
2. **Finish-off test:** render the shot with all finish layers off. If silhouette, value structure and colour no longer hold, the design failed and finish is compensating.
3. **Frequency:** each finish layer appears on no more than 80% of shots in a chapter (J), because a layer on every shot reads as a template.

**Projector cautions with measurements.**

- *Thin lines and small type.* Measured (M): a saturated red 1-pixel vertical line on mid-grey kept 70% of its contrast after H.264 CRF 18 at 1920 by 1080 in 4:2:0; red lines 2 and 4 pixels wide kept 99%, 3 pixels 91% (position-dependent). Near-black lines of any width kept 99 to 100%. Chroma is stored at half resolution in 4:2:0 files; a DCP is 4:4:4 XYZ [34], so the loss is in the access copy and projector-PC files. Rule: strokes at least 2 px at 1080p (0.19% of picture height), no saturated hairlines.
- *Judder on pans at 24 fps.* "Pan no faster than a full image width every seven seconds"; the rule is not all-or-nothing; larger shutter angles pan smoother but more smeared; contrast steps and near subjects make strobing more likely [41]. In our synthetic frames there is no camera shutter, so motion blur must be added (sub-frame accumulation at 180 degrees) for moves above 4 px per frame. If the venue plays 24 fps through a 60 Hz chain without a DCP, expect uneven frame cadence; test it.

### Q7. The AI-tells catalogue

Status key: **ALLOWED** = fine under Principle 4 and the ladder; **LABEL Lx** = allowed with the ladder label and a `steps.csv` note [P2]; **BANNED** = not in the public cut.

Dates: sources for tells are mostly 2026 vendor and trade pieces (weak) plus the primary research cited. The tells list in [19] is dated 2026-04-17 and is vendor-written; [18] is dated 2025-12-23 (older than six months, background only). Detection methods are mine unless cited.

| # | Tell | Cause | Detection | Fix | Status |
|---|---|---|---|---|---|
| 1 | **Face drift** (face changes across frames or shots) | Generators re-synthesise faces per clip; iterative edits accumulate change [62][59][65] | Step frames at 0, 25, 50, 75, 100% at 100% zoom; side-by-side with the L1 source; landmark ratio alarm (2%); maker's 5-of-5 blind line-up (D1 A3) | Do not generate faces: keep the original face region, use 2.5D from the photo; clips 3 to 5 s; fixed seed; pick the take with least change [P2]; always re-anchor to the original, never the last output | Environment motion with the face region kept from the L1/L2 photo: **LABEL L4b**. Whole-frame image-to-video on a face-bearing photo: **LABEL L4b only if A3 passes**, otherwise **BANNED**. Deliberate face regeneration or animation: **BANNED**. Faces of the dead: **BANNED** (delta, see end) |
| 2 | **Flicker** (luminance, colour or texture shimmer) | Per-frame generation or frame-by-frame upscaling without temporal coherence | Flicker index = std of the second difference of per-frame mean luma (ffmpeg `signalstats` YAVG) over a static region divided by √6 (M: static 0.000 levels; injected flicker 2.58 levels). View at half speed. Warp-error metrics exist in the research literature [64] | Non-generative deflicker; composite the static background from one frame; lower generative strength; avoid frame-by-frame upscalers | Non-generative deflicker **ALLOWED (L1)**; generative deflicker **LABEL L4b** |
| 3 | **Morphing** (shapes melt between frames; objects appear and vanish) | No persistent 3D; clip-level sampling | Step every 6th frame at 100%; count objects and fingers; compare first and last frames | Shorter clips, mask the moving region, re-roll | Visible morphing **BANNED**. Morph between two different people **BANNED**. Classic morph of two real photos **ALLOWED (L4a)** [P2] |
| 4 | **Plastic skin** from upscalers and face restorers | Restorers "reconstruct features that may no longer exist in the input" [63 (a 2026 guide, search-result only)]; CodeFormer trades fidelity for quality via a coefficient [63]; GFPGAN "may slightly change identity" [P2] | 100% crop A/B against a plain bicubic upscale of the L1: check pores, freckles, creases, specular sheen; high-frequency energy of a skin patch (Laplacian variance) outside 60 to 140% of the plain upscale is suspicious (J) | Prefer no restoration; plain upscale; if restored, w 0.7 to 1.0 and blend 40 to 60% back over the plain upscale [P2]; never mask plastic with grain | Restoration **LABEL L2**. Skin smoothing or beauty filters **BANNED** |
| 5 | **Invented detail**: pores, wrong teeth, new eyelids, changed jaw, ears, jewellery | Face prior fills missing detail | Landmark overlay; count teeth and jewellery; compare with source at 200% | Reject the result | **BANNED** ("Reject any result with new teeth, new eyelids or a changed jaw" [P2]) |
| 6 | **Warped hands** | High-variance anatomy [19] | Step frames; count digits on every visible hand | Crop or hide; in L5 hands are hand-made by the bible's rule (Flee-style hand rule [27]) | Generative hands in photo shots **BANNED**; L5 hands are hand-made, never generated |
| 7 | **Warped or gibberish text** (signs, shirts, labels) | Diffusion text rendering [19] | Read every visible word at 100% and compare to the source | Typeset all text deterministically; leave source text soft rather than "fix" it | Generated text **BANNED**. Restored text must match the source or stay soft |
| 8 | **Over-smooth motion** (too stable, linear, weightless) | Model priors; raw lerp in code | Velocity CV under 0.12 (M); "A raw lerp over time is a bug" [68]; absence of settle | Authored easing with settle; holds; Danse Macabre's team "repeatedly reintroduced imperfections when frames looked too stable" [21] | **BANNED** (lint) |
| 9 | **Uncanny eyes** (no blinks, wandering gaze, glassy highlights) | Weak eye modelling; animated stills | Stop on the eyes at 100%; compare gaze to source; any blink in a clip made from a still | Keep eyes from the photo; stylised eyes drawn by bible rules | Animating eyes, blinks or gaze of a real face **BANNED** (dignity, Principle 4) |
| 10 | **Generic AI lighting** (soft elevated key, no hard shadows, same everywhere) [19] | Model mean [5][17] | Lighting-tag lint across a chapter; compare light direction to the photo's own shadows | Per-era lighting spec taken from the photographs; L5 lit to match | Allowed only if it matches the source light; otherwise fails review |
| 11 | **Generic composition** (centred, symmetrical, epic wide, shallow DOF everywhere) | Training average | Subject-position histogram across a chapter; swap test (D3) | Layout comes from the photo and the cut-or-move rules | Fails review |
| 12 | **Synthetic palette** (over-saturated greens and skies, teal-orange) [19] | Model grading defaults | ΔE00 to era swatches; chroma percentile | Grade to the script | Fails review |
| 13 | **Texture crawl** in flat areas of generated video | Diffusion noise per frame | Flicker index on a flat patch; step 3 consecutive frames | Composite a static plate; use L4a instead | Fix or cut |
| 14 | **Hallucinated background** (extra people, invented objects, signs) | Inpaint or outpaint, restoration | Diff mask against the source; every changed region listed in `steps.csv` | Clone only (L1); crop instead of outpaint | Invented people **BANNED**; invented objects **LABEL L2/L4b with an "invents" note** |
| 15 | **Upscaler artefacts** (halos, waxy texture, tiled patterns) [19] | Over-strong sharpening or generation | 200% crop at edges and in large textured areas | Lower strength; avoid repeats | **LABEL L2** |
| 16 | **Colourisation errors** (orange skin, wrong clothes) [P2] | Guess of colour | Compare to family memory or other colour photos; era skin swatch ΔE00 | Mute skin; caption "colours estimated" | **LABEL L2** |
| 17 | **Age blending** (young face looks older, or reverse) | Identity-age trade-off [60][61] | Age line-up against the board | One reference set per age; never "age up" | Synthesising a different age of her **BANNED** |
| 18 | **Speech or lip-sync from a still** | Audio-driven models | Any mouth movement in an I2V clip | Never request it [P2] | **BANNED** (Principle 4) |
| 19 | **Voice tells** (TTS plateau, no breaths) [19] | TTS prosody | Listen with picture off | Real recordings only | Voice cloning **BANNED** (charter) |
| 20 | **Mirror, reflection and physics errors** [19] | No world model | Check every reflection | Remove reflection or hand-make | Fix or cut |
| 21 | **Soft 720p to 1080p generative video on a 2K screen** | Native model resolution; upscaled | Compare at 100% on the venue screen. Veo 3.1 prices in [P2] are for 720p clips | Use generative video for small inserts only; L4a for key shots | **LABEL L4b**, small inserts only |
| 22 | **Finish used as a mask** (grain, halation or flare to hide defects) | Over-finishing | Finish-off test (D1 FN2) | Fix the defect or cut the shot | Fails review |
| 23 | **Repeated pattern grain** (8-frame loop) | Short baked loops | Autocorrelation at the loop length (M: 1.00 at lag 16) | At least 48 distinct frames, seeded offsets | Fix |

**Blind reads.** In the screenings (D6) ask every stranger before any briefing: "Mark any moment that looked wrong, fake or computer-made." Count marks per minute; more than two per minute from independent viewers on any chapter sends the chapter back to the tell list.

### Q8. 2023-2026 AI film festival winners and AI-assisted shorts, read critically

**Who runs the festivals and the incentive.**

| Festival | Who runs it | Incentive | Evidence |
|---|---|---|---|
| Runway AIF (2026 was its fourth edition: New York 2026-06-11, Los Angeles 06-18, Tokyo 07-30; $135k+ prizes) | Runway, which sells generative video. Partners: Lionsgate, Tribeca, The Gotham, Monks, Adobe, Roku, Nvidia. Jury includes Cristobal Valenzuela (Runway's CEO, from general knowledge; the page lists only the name) [1] | Showcase for the tool; Grand Prix $50,000 plus 1,000,000 Runway credits; entries must use generative video; judges score "creative and skilled use of AI techniques" among four 1 to 10 criteria [1][2] | Gaudette said the project began as a personal experiment "to use for marketing his AI services" [3] |
| WAIFF (Cannes, 2026-04-21/22) | EuropIA Institute with local government partners (search-result only); sponsors on the prize page include MiniMax and CapCut (logos only) [7] | Visibility for sponsors, tool vendors; submissions rose from about 1,000 to 5,000 [8] | One shortlisted film was withdrawn for "a strong resemblance to an existing work" (said to look like Wallace and Gromit); screenings called "patchy" [8] |
| Cannes main festival | Thierry Frémaux, who said films may one day be labelled like organic food ("this film has been made without artificial intelligence"), while also announcing a multi-year Meta sponsorship [9] | Mixed | Shows that a mostly public audience may include people hostile to AI. Honest labelling matters |

**What the makers did (selection ratios, hand passes, live plates, hours).**

| Work | Process as published | Hours per finished minute | Reception | 2K projection risk (J, I have not seen the films) |
|---|---|---|---|---|
| *A Face Only A Mother Could Love*, Robert Gaudette (Runway Grand Prix 2026, about 8 min) | Reference images and still character designs first, then motion; early rough assembly; "several generative tools, conventional image editing, a standard editing program" plus stock assets, sound and music; "Sometimes a usable shot appears after a few tries. Sometimes it takes dozens"; rejected "technically strong shots" when the character moved wrongly; scenes of 30 s or more built from many generations [3][4]. Reportedly alone over two weeks of 17-hour days; a $5,000 budget appears only on a festival listing (search-result only) | about 30 (14 days × 17 h ÷ 8 min = 238 h; my arithmetic on a secondhand figure) | Crowd "practically erupting"; Business Insider's reporter found several films "boring" [4]; Fast Company's reviewer found no slop and that no two films resembled each other (search-result only) [14] | Medium: reference-driven character holds, but all-generated video is native-resolution limited and voice is synthetic (ElevenLabs, per a listing) |
| *Costa Verde*, Léo Cannone (about 11:35; Runway honoree; WAIFF CapCut Prize per the prize page) | "Created with AI (bar one shot)" [6]; family photos and Corsican landscape documentation as visual references; Midjourney and MiniMax; last shot filmed on a Fujifilm X100V (search-result only) [20] | Not stated | Highlighted by THR for its "distinctive use of AI imagery" [4]. The laurel "Best Film at WAIFF" appears on a LinkedIn post (search-result only); the festival's prize list shows the CapCut Prize and lists *A Dollar Story* as Best WAIFF Film [7] | Best of the group: a child's-eye, handheld, remembered look forgives softness, and it starts from real family photographs, which is our approach too |
| *Get Me Out*, Daniel Antebi (Runway Grand Prix 2024) | Shot on an ARRI Alexa Mini; Luma AI to capture environments; Runway video-to-video; ComfyUI to re-skin a second actor [83 (search-result only)]; TechCrunch: the AI graphics were "less effective than the cinematography" [13] | Not stated | Mixed [13] | Good: a real plate carries it |
| *Total Pixel Space*, Jacob Adler (Runway Grand Prix 2025, 9:28) | Midjourney, Runway animations, ElevenLabs voice; reportedly over a year and tens of thousands of images [84 (search-result only)] | Not stated | Ars Technica, quoted second-hand: "compelling images... touching on some really interesting ideas" [84 (search-result only)] | Medium-good: abstract imagery forgives artefacts |
| *Air Head*, shy kids with Sora (2024-04) | 20-second generations with 2 to 3 seconds kept; many balloons the wrong colour, recoloured in compositing; conventional edit, voice-over, sound, a shy kids song; "a little over a week" [12] | Not stated | Initially presented without noting the post work; later interviews corrected that [12] | Not assessed |
| *Critterz* (OpenAI-backed feature) | Pitch: "a film in nine months for under $30 million" with much of the design and animation generated, voice actors and "a handful of artists" [10]. Per search results, the film did not debut at Cannes 2026 after Sora was shut down, and the team went looking for a new AI partner (Bloomberg, 2026-05-22; search-result only) [11] | n/a | Cartoon Brew called the "democratizing" defence "disingenuous", noting *Flow* was made by a small team on free software [10] | n/a |

**Tool-vendor volatility is a finding.** If the Bloomberg headline is accurate, a tool a studio-scale project depended on was shut down mid-production [11]. Our pipeline already treats every tool as replaceable [P3]; keep that.

**Animator reception (2026).** Annecy: Euronews' headline calls AI "the elephant in the room"; Leo Neumann (studio of about 30) said for his small team "they would have been faster without AI"; Henry Daubrez warned lazy use pulls output toward "the average or the mean" [5]. SCAD AnimationFest panel: the best defence against generic AI imagery is to be "more specific, not less" (search-result only) [17]. MIT Technology Review (2025-12-23, background): the repeated "fake surveillance" look and "formulaic derivativeness" [18].

**Non-AI calibration with published breakdowns.**

| Work | What the breakdown shows | Lesson for us |
|---|---|---|
| *Flow* (Gints Zilbalodis, 2024) | Blender and EEVEE; roughly 15 to 20 people in total but usually 3 to 5 at once; about 5.5 years; 0.5 to 10 seconds per 4K frame on his own PC, no render farm; "no compositing, all the colors were tweaked and adjusted using shaders"; camera and lighting handled together; the director was the only lighting artist [23] | Fast previews and one person owning light make a coherent look. Our Route A gets the same benefit by owning one palette and one light spec |
| *Away* (Zilbalodis, 2019) | Solo; Maya; real-time viewport playblasts; no script or storyboard, story found by editing rough animation; 75 min; 3.5 years, 8 to 10 hours a day, 6 to 7 days a week; many long takes with a floating camera; characters without shadows; copied animation across identical cats [24] | Constraints chosen early (no shadows, identical crowd) are what made a solo feature finishable. The shortcut is declared in the bible |
| *Danse Macabre* (Hisko Hulsing, Annecy 2026) | 75 oil paintings over more than a decade; 30+ artists; the surface of the paintings kept uneven; AI shader systems trained on the painter's own surfaces, "fenced and used in moderation", nearly every frame corrected manually; Fusion compositing with ProRes pre-comps, alpha divide, polygon masks, a colour corrector to match the painted palette, global film grain last; a Stable Diffusion stylisation pass operated by a named artist [21][22] | The strongest model for "AI in service of a human-made material." Keep AI inside our own material, grain last, correct by hand |
| *Sprite Fright* (Blender Studio, 2021) | A written style guide for animators; mostly on twos [26] | A single-page rule on twos and ones is worth writing before animation |
| *Flee* (2021) | Art bible, closed-eyes interviews, archive footage [27] | Already in [P1] |

**Vendor selection-ratio data (weak).** invideo.io's July 2026 FAQs, drawn from about five productions of its own tooling, plan on about 3 generations per usable shot on average, report one 3-minute animated episode that kept 41 of 164 clips (about 25%) with about 5 s kept from each 15 s clip, and estimate 55 to 270 generations per finished minute [15]. Treat these as vendor marketing; they are the only published ratios I found besides Air Head's 2 to 3 s kept from 20 s.

**Calibration of effort (my arithmetic, treat as order of magnitude).** Gaudette about 30 hours per finished minute with generation; *Away* about 140 hours per finished minute by one person in Maya; *Flow* on the order of several hundred person-hours per finished minute (3 to 5 people at a time over about 5.5 years is roughly 16 to 27 person-years; at 1,800 hours a year and an 85-minute runtime, which is general knowledge and not from my sources, that is about 340 to 570 hours per finished minute). The schedule track owns what our film can afford; this note only warns that theatrical polish on photo-forward work is a human-hours problem, not a generation-credits problem.

### Q9. Review practice for one maker

**Dailies rituals (one-person versions).** Studios review work in progress in dailies (general practice, J); Pixar's HBR essay is summarised as giving authority to project leaders and building a culture of sharing work-in-progress among peers [81 (summary seen in search results; the fetched page showed only the opening)]. The one-person version:

| Ritual | How | Why / evidence | Time |
|---|---|---|---|
| **48-hour rule** | No shot is approved or rejected the day it is made. Review the draft 48 hours later | Familiarity makes errors invisible; "if you're familiar with the story, your eye will glide right by the error" is practitioner advice for text [75]. I found no controlled study (UNVERIFIED) | 0 extra |
| **Blind A/B against the previous version** | Agent renames the two versions X and Y at random; maker picks; the key is revealed after | [68] uses blind shuffled ranking for AI critics; [P3] step 9 asks for blind comparison on template-risk shots | 3 min per shot |
| **Distance viewing** | Watch the shot on the TV from 3 m [P3 G6] and, from week 14, on the venue-class projector | A laptop at 50 cm hides type, banding and judder | 5 min per chapter |
| **Squint test** | View blurred and greyscale (blur about 1% of frame width); the primary subject and the main light/dark shapes must still read | A standard painter's check of value structure [73 (search-result only)] | 1 min |
| **Half and double speed** | Half speed to see stutter, flicker, edges; double speed to see rhythm and repeats | Standard editing practice (J) | 3 min |
| **Sound-off, picture-off** | Sound off: does the picture carry the beat? Picture off: does the sound carry it? | [P3] pitfall 2: nobody listens (a 22-agent run opened 604 images and played 0 sounds, as reported in [P3]) | 4 min |
| **Reverse-order pass** | Watch a chapter's shots from last to first | Breaks order bias (J) | 5 min per chapter |
| **Frozen anchor frames** | Five frames from the approved style frames pinned beside every review | Stops taste drifting (below) | 0 |

**Decision log so taste does not drift across sixteen weeks.** Use short architecture-decision-record style entries [72]: title, date, status (proposed, accepted, superseded), context ("the forces in tension"), decision ("We will..."), consequences ("not just the positive ones"). Keep each to a page, never delete, mark superseded; "numbers will not be reused" [72]. Add two fields (J): `evidence` (frame or file name) and `reversible: yes/no`. Add a **drift check** at weeks 5, 9, 13 and 17: re-score six frozen shots from the slice on the D3 rubric without looking at old scores; a change of more than one point on any criterion means taste has moved and the bible must be updated deliberately or the new shots corrected.

**This advisor's rubric at G1, G2 and G4.** Full text in D3. The gates in [P3] are: G1 style frames, G2 shot draft, G4 chapter. A fresh-context reviewer can score stills but not motion or sound, and "treat any AI critic as a noisy sensor: vary the order, anonymise and aggregate"; one review found "about one checkable claim in four held up" [68]. So the rubric makes machine-checkable items the evidence and uses the reviewer for judgment items only.

**Test-screening protocol for three to five strangers-to-her.** Full protocol in D6. Key findings:

- Practitioner guidance for test screenings: 4 to 10 people, limit industry people to a couple, level the sound first ("Bad sound is so distracting that it often can ruin a regular screening"), slate over missing parts, watch without pausing, ask the basics on a questionnaire first and project-specific worries last "so as not to sway their opinions" [70].
- Weigh notes by repetition, decode the note behind the note ("I was a little bored" may mean weak stakes or pacing) [70], and follow Gaiman's rule, paraphrased: people are almost always right that something is wrong or does not work for them, and almost always wrong about how to fix it (search results confirmed the first half of his sentence verbatim and the second half in paraphrase) [71].
- With 3 to 5 viewers you cannot estimate rates; you can only find problems. Use thresholds on counts (D6).
- Recruitment must not reveal her identity beyond the film, and must not be possible to leak back to her circle. See D6 for the redacted-cut option and the truthful pretext.

### Q10. Projection truth

See D5 for the full checklist. Key derived numbers (my arithmetic unless cited):

- **Type.** The fluent reading range for x-height runs from about 0.2 degrees to 2 degrees [47]. At 0.2 degrees the minimum x-height as a fraction of picture height is about 0.0035 × (farthest seat distance ÷ picture height): 1.4% at 4 screen heights, 1.75% at 5, 2.1% at 6. With a 1.5 times margin for projected, lower-contrast text: 2.1%, 2.6%, 3.1%, which corresponds to a font size of roughly 4.2%, 5.2%, 6.3% of picture height (45, 57, 68 px at 1080). Rule: **x-height at least 2.5% of picture height and font size at least 5% for any text the audience must read; below 2% x-height the text is decorative and must not carry information.** (J, scale to the venue's real seat distances.)
- **Safe areas.** EBU R95 (revised 2016): action safe 3.5% and graphics safe 5% margins, top, bottom and sides [45]; SMPTE ST 2046-1 uses 93% for action [46]. Rule: all text inside 5% margins.
- **Pan speed.** At most one frame width per 7 seconds at 24 fps (0.143 frame widths per second; 11.4 px per frame at 1920 wide) [41], on the fastest textured layer.
- **Brightness.** Screen luminance in nits ≈ lumens × gain ÷ (π × screen area in m²). Screen 6 m wide: 3,000 lm gives about 47 nits, 5,000 lm about 79. Screen 8 m: 27 and 44 nits. Screen 10 m: 17 and 28 nits (ideal, before lamp, lens and ageing losses). DCI reference is 48 nits [35]. Most public-gathering projectors will be dimmer than a cinema and the room will not be as dark, so shadow detail is at risk [33].
- **Black level and ambient light.** DCI requires reflected ambient light under 0.01 cd/m² for the test [35]; a hall will not come close. One measured example (search-result only): a screen's contrast with room lights on was 57:1 on a 1.0-gain screen and 194:1 on a dark optical screen, against over 8000:1 projector contrast with lights off [49]. Rule: no story-critical information below about 10% signal level unless the venue test (D5 item 5) passes.
- **Speech.** Speech transmission index bands under IEC 60268-16: 0 to 0.30 bad, 0.30 to 0.45 poor, 0.45 to 0.60 fair, 0.60 to 0.75 good, 0.75 to 1.00 excellent; "an STI of at least 0.5 is desirable for most applications" [48]. Rule: aim for 0.60 or better at the back row; keep a caption fallback for any line that matters.

---

## Exemplars and what they teach us

| Exemplar | What it is | What it teaches | Source |
|---|---|---|---|
| *Danse Macabre* (2026) | Hand-painted oil backgrounds, 3D character, fenced AI pass, global grain last | Keep AI inside a human material; re-introduce imperfection; finish once at the end | [21][22] |
| *Flow* (2024) | Blender, EEVEE, small team, shader-based colour | One owner of camera and light; previews fast enough to iterate | [23] |
| *Away* (2019) | Solo feature, floating camera, no shadows | Choose constraints early and declare them | [24] |
| *Spider-Verse* (2018) | Twos as a performance choice | Twos is a decision per shot, modulated within a shot | [25] |
| *Sprite Fright* style guide | One-page rule on twos and ones | Write the timing rule before animating | [26] |
| *Flee* | Art bible with good/not good, hand and eye rules | The single most transferable bible tactic | [27] |
| *Up* colour script | Emotion mapped to colour and light | Colour carries a learnable meaning | [31][32] |
| Gaudette, *A Face Only A Mother Could Love* | Reference-first AI film, many takes | Taste is rejection: he rejected strong-looking shots that moved wrongly | [3] |
| *Costa Verde* | Family photos as references, remembered look, one real shot | Closest in spirit to our photo-forward approach; note its laurel is sponsor-flavoured | [6][7][20] |
| *Air Head* | AI clips plus heavy post | Any AI film that looks finished has human compositing behind it | [12] |
| *The Kid Stays in the Picture* | Separated subjects panned at different speeds | The ancestor of our 2.5D | [53] |
| Burns on photographs | Move only for meaning | The cut-or-move rule | [54] |

---

## Templates and deliverables

### D1. Per-shot quality checklist (every item has a pass/fail test)

Severity: **Crit** = critical (any fail blocks the shot), **Maj** = major (fix before chapter assembly), **Min** = minor (log). "Agent" = machine-checkable by the pipeline; "Maker" = needs eyes. Gate = where it is scored.

| ID | Item | Test | Pass | Sev | Who | Gate |
|---|---|---|---|---|---|---|
| **A. Identity and honesty** | | | | | | |
| A1 | Label matches the ladder | `output_level` in brief equals XMP/`steps.csv` level; every changed region listed | Match, no unlisted change | Crit | Agent | G2 |
| A2 | Face geometry intact (L1/L2/L4a) | Landmark ratios (inter-ocular, eye-line, mouth width) of the shot's first and last frame against the source | All within 2% | Crit | Agent | G2 |
| A3 | Face never regenerated (L4b/L3) | Maker's blind line-up: five frames from the shot (0, 25, 50, 75, 100%) mixed with four decoys | 5 of 5 chosen as the same face, twice 48 hours apart | Crit | Maker | G2 |
| A4 | No animated eyes, blinks, mouth or speech on a real face | Step frames on eyes and mouth at 100% | None | Crit | Maker | G2 |
| A5 | No invented people or text | Diff mask against source; read all text | None | Crit | Agent + Maker | G2 |
| A6 | Photograph not mirrored | Manifest `mirrored: false`; text reads correctly | True | Crit | Agent | G2 |
| **B. Layout and camera** | | | | | | |
| B1 | Move has a reason | `because:` is one of reveal, link, isolate, time, or `hold` | Present | Maj | Agent | G0/G2 |
| B2 | Move magnitude | Zoom-velocity estimator or spec: total zoom and translation | Push/pull up to 8%, pan/orbit up to 5% of width and 3 degrees, unless class C | Maj | Agent | G2 |
| B3 | No disocclusion holes | Alpha of the layered composite after fill; step the extreme frames | Zero hole pixels at 100% | Crit | Agent | G2 |
| B4 | Shot size progression | Adjacent shots differ in size class or angle (30 degrees); at most two close-ups per chapter | True | Min | Agent | G4 |
| B5 | Direction | Move follows or holds the gaze; no more than 2 consecutive same-direction drifts | True | Min | Agent | G4 |
| B6 | Portrait ladder alignment | Eye centre of consecutive portraits within 3% of frame | True | Maj | Agent | G2 |
| B7 | Safe area | All text and faces inside 5% margins (faces may bleed only when the brief says CU) | True | Maj | Agent | G2 |
| B8 | Hold before move | New photo holds at least 0.5 s before any move | True | Min | Agent | G2 |
| **C. Colour and light** | | | | | | |
| C1 | Palette | Median and three dominant colours in Lab within ΔE00 of 6 of the era swatches | True | Maj | Agent | G1/G2 |
| C2 | Scene continuity | Shots in one scene within ΔE00 of 3 of each other (median colour) | True | Min | Agent | G4 |
| C3 | Skin patch | Skin ROI within ΔE00 of 4 of the era skin swatch sampled from the scan | True | Maj | Agent | G2 |
| C4 | Value structure | Squint test (blur 1% of width, greyscale): face reads from background | Face-to-surround mean luma difference of at least 10 L* | Maj | Agent | G2 |
| C5 | Clip and crush | Pixels below 16 or above 235 (8-bit video range) | Under 0.5% of the frame unless declared | Maj | Agent | G2 |
| C6 | Dark-detail rule | Story-critical regions' luma | Above 10% signal unless the venue test passed | Maj | Agent | G2/G6 |
| C7 | Light direction | Composited L5 elements share the key direction of the photo they sit on | Within 30 degrees | Maj | Maker | G2 |
| C8 | Light variety | Chapter has at least 3 distinct lighting types (hard side, backlit, window, lamp, overcast) | True | Min | Agent | G4 |
| **D. Motion** | | | | | | |
| MO1 | Not linear, not default | Level 2 estimator: CV over 0.12; spec contains no default ease | True | Crit | Agent | G2 |
| MO2 | Ease class declared and measured | Measured class equals brief `ease_family` | True | Maj | Agent | G2 |
| MO3 | Settle | Velocity in the last 15% of the move decays monotonically to 5% of peak or less in the spec (10% or less in the pixel audit) | True | Maj | Agent | G2 |
| MO4 | Hold after payoff | Velocity at 0 in the spec (under 10% of peak in the pixel audit) for at least 18 frames after the payoff, 24 frames after a face reveal | True | Maj | Agent | G2 |
| MO5 | Twos and ones | Drawn layers show alternating zero steps (twos); camera and type show none (ones) | True | Min | Agent | G2 |
| MO6 | Pan speed | Fastest textured layer at most 11.4 px per frame at 1920 wide (0.143 frame widths per second) unless blurred or a declared whip | True | Maj | Agent | G2 |
| MO7 | Motion blur | Any layer above 4 px per frame has sub-frame blur at 180 degrees | True | Maj | Agent | G2 |
| MO8 | Sub-pixel smoothness | Velocity roughness (std of residual from a 9-frame mean, relative to mean speed) | 0.15 or less (M: Pillow 0.08 to 0.13; zoompan 0.26 to 0.35) | Maj | Agent | G2 |
| MO9 | Chapter variety | 8-shot windows: 3 or more family keys, none above 40%, entropy 1.5 bits or more, held shots 35% or more | True | Maj | Agent | G4 |
| **E. Finish** | | | | | | |
| FN1 | Stacked finish count | Global finishing layers (grain, vignette, letterbox, flare/bloom/halation, dust/scratch, light leak, colour filter, shake) | Two or fewer, all in the era's finish stack | Maj | Agent | G2 |
| FN2 | Finish-off test | Render with finish off | Silhouette, value and colour still hold | Maj | Maker | G2 |
| FN3 | Frequency | No finishing layer on more than 80% of shots in a chapter | True | Min | Agent | G4 |
| FN4 | Cut-out edges | Composite over black, white and mid-grey, view at 200% | No fringe, no hole | Crit | Maker | G2 |
| FN5 | Light wrap | Edge only, last in chain, halo within 3 px at 1080p, none on the side away from the key | True | Maj | Maker | G2 |
| FN6 | Grain match | Std of flat-patch luma on L5 layers within ±30% of the scan's flat-patch std | True | Maj | Agent | G2 |
| FN7 | Grain loop | Autocorrelation at the loop length under 0.3 | True | Maj | Agent | G2 |
| FN8 | DOF | Blur by plane; no blur on faces; far-plane blur at most 1.2% of width | True | Maj | Agent | G2 |
| **F. AI tells** | | | | | | |
| AI1 | Tells 1 to 23 swept | Q7 table walked at 100% on key frames, with 5 frames per second of a moving shot | None present | Crit | Maker | G2 |
| AI2 | Flicker | Flicker index on a static region | 0.3 levels or less (M: static 0.000, injected 2.58) | Maj | Agent | G2 |
| AI3 | Hands, text, reflections | Every visible instance checked | Correct or absent | Crit | Maker | G2 |
| **G. Type and titles** | | | | | | |
| TY1 | Legibility | Font at least 5% of picture height; x-height at least 2.5%; strokes at least 2 px | True | Crit | Agent | G2 |
| TY2 | Hold | Card held at least 36 frames once fully legible; caption within reading-speed limits from [format] | True | Maj | Agent | G2 |
| TY3 | Licence | Font, texture and plate have licence files | True | Crit | Agent | G1/G2 |
| **H. Projection** | | | | | | |
| PR1 | Banding | Dark-ramp test: no visible steps in dark gradients at the venue; masters 10-bit | True | Maj | Maker | G6 |
| PR2 | Thin lines | No saturated 1-px lines; contrast retained 90% or more after the access-copy encode | True | Maj | Agent | G6 |
| PR3 | Grain survival | Flat-patch grain std after encode at least 70% of the master's | True | Maj | Agent | G6 |

### D2. Style-bible template, and the ten decisions to lock before the slice

Format: one document, four to eight pages, a "good / not good" board, owned by the maker, versioned, referenced from every `brief.yaml`. Each decision has a lock, a test and a gate. Fill in brackets.

```yaml
# style_bible.yaml  (version, date, author)
1_palette_per_era:
  how: "sample from L0 scans: k-means in Lab on non-face regions + paper border; record sRGB hex and Lab"
  limit: "six colours or fewer per era (G1)"
  eras:
    - {id: era_1, years: "[ ]", colours: ["#", "#", "#", "#", "#", "#"], skin_swatch: "#", accent: "#", light: "[window | lamp | flash | overcast]"}
  test: "shot dominant colours within dE00 6 of the era swatches; skin within 4"
2_hand_made_material:
  material: "[cut paper | clay | voxel | other]"
  rules: ["layer count max [ ]", "shadow direction [ ]", "edge: [torn | cut | scalloped]", "hand rule: [ ]", "eye rule: [ ]", "what never animates: [ ]"]
  good_not_good_board: "path/to/board.png"
  test: "at least 80% of strangers can say which shots are reconstructed before any card (for example 4 of 5, 3 of 4, 3 of 3)"
3_line_and_edge:
  min_stroke_px_1080: 2
  cutout_edge: "feather 0.5 to 1 px, colour decontaminated"
  test: "three-background test at 200%; thin-line retention 90% or more"
4_typography:
  families: ["display: [ ]", "text: [ ]", "handwriting: only words she actually wrote"]
  licence: "OFL permits video titling and embedding [56]; commercial fonts need a film/public-exhibition licence checked per font"
  min_size: "font 5% of picture height, x-height 2.5%"
5_camera_grammar:
  moves: ["push", "pull", "pan", "tilt", "orbit up to 3 degrees", "hold"]
  ranges: "push/pull up to 8%, pan up to 5% of width"
  virtual_lens: "35 mm equivalent default; 50 for portraits"
  cut_or_move: "move only for reveal, link, isolate, time"
  direction: "follow or hold gaze; never mirror a photo"
6_reconstruction_marker:
  signature: "[material + paper frame + persistent mark]"
  disclosure_card: "[wording] (see animated.md)"
  test: "blind stranger identification by at least 80% of viewers"
7_still_to_moving_ratio:
  target: "35% or more of photo shots are holds; no more than 25% have more than one plane moving"
  test: "counted from briefs"
8_grain_and_paper_system:
  finish_stack_per_era: {era_1: ["grain"], era_2: ["grain", "[ ]"]}
  max_global_layers: 2
  grain: "spatially correlated, temporally independent; at least 48 distinct frames; seeded offset; std within 30% of scan"
  paper: "scan of her print backs or ambientCG CC0 texture; source recorded"
  applied: "once, last, on the 10-bit master; the 8-bit access copy relies on grain or texture of at least one 8-bit level, because invisible dither is quantised away by the encoder [44]"
9_title_system:
  types: ["chapter card", "date line", "end credits cue sheet"]
  rules: ["no lower thirds", "no typewriter reveal", "centre only if the layout calls for it", "hold 1.5 s once legible"]
10_never_list: "see D4"
```

The ten decisions in one line each, with the one failure each prevents:

| # | Decision | Lock | Failure prevented |
|---|---|---|---|
| 1 | Palette per era | Six colours per era from her scans, plus skin and accent | Generic decade palettes and teal-orange |
| 2 | Hand-made material | Material, layer, hand, eye rules | Reconstruction mistaken for a photograph |
| 3 | Line and edge | Minimum stroke, feather, fringe test | Paper-doll cut-outs, aliasing |
| 4 | Typography | Two faces plus her handwriting for her words only; licence files | Illegible or unlicensed type |
| 5 | Camera grammar | Move list, ranges, lens, cut-or-move | Same slow zoom on every photo |
| 6 | Reconstruction marker | Visible signature and disclosure card | Charter principle 4 breach |
| 7 | Still-to-moving ratio | Hold share and plane limits | Slideshow rhythm |
| 8 | Grain and paper | Stack per era, at most 2 layers, matched to scans | Stacked finish, looped grain |
| 9 | Title system | Three title types and rules | Template titles |
| 10 | Never list | D4 | Cheap tells |

Brand caution for decision 2 and 10 if the voxel look is used: the saved Minecraft usage excerpt says the name may not be the primary title, and gameplay must not be "displayed or projected publicly within physical locations"; events were limited to about 150 participants. The theatrical-delivery and games tracks own the answer; do not make a voxel look the reconstruction marker until they resolve it [57].

### D2b. Per-age reference board (template)

```yaml
age_board:
  age: 25   # also 6, 55
  sources: [{photo: LJ-B03-0042-F__L1, date: "1999-06", note: "front, even light"}]   # 3 to 5
  attributes: {hair: "", parting: "", brows: "", eyes: "", nose: "", mouth: "", ears: "", glasses: "", posture: "", height_vs_others: ""}
  stylised: {front: path, three_quarter: path, profile: path}
  expressions: [neutral, smile, laugh, listening, tired]
  proportions: {head_heights: , inter_ocular_over_head_width: , mouth_width_over_inter_ocular: }
  costume_and_swatches: {skin: "#", hair: "#", clothes: ["#"]}
  do_not: ["no teeth unless in source", "..."]
  signoff: {maker_pass_1: "date", maker_pass_2: "date (48 h later)", lineup_score: "5/5"}
```

### D3. Dailies review rubric mapped to G1, G2 and G4

Scoring uses the charter's six criteria (1 to 5), with this note's craft tests as the evidence. A gate passes only when every score is 4 or more and nothing critical is open [P5][P3]. Evidence column says what to attach.

**G1 style frames (three frames per era slice; the maker scores, the advisor reads).**

| Check | Test | Pass |
|---|---|---|
| Not any family's film | **Swap test**: replace her photographs with stock family photographs; does the frame still work unchanged? | It should not; it should depend on her specifics |
| Palette | Six or fewer colours, sampled from her prints, swatches attached | True |
| Reconstruction visibly stylised | Stranger test (later) / maker now: can a reconstruction be mistaken for a photograph? | No |
| Finish stack | Count of global layers | Two or fewer |
| Squint and distance | Blur+greyscale; TV at 3 m | Subject and mood read |
| Type | Size, licence file | D1 TY1, TY3 |
| Hand/eye rules | Shown on the board | Present |
| Era identifiable | Hide the date; does the frame say which era? | Yes |
| Likeness | Age board line-up for any stylised face | 5 of 5 twice |

**G2 shot draft (per shot).** Use D1. Scoring map:

| Criterion | Evidence | Score 4 or 5 means |
|---|---|---|
| Meaning | Brief `beat` and the blind read: what did the maker feel first? | The beat lands at the first blind viewing, 48 hours later |
| Specificity | Swap test; named object or place visible | The shot could not be about another woman |
| Accuracy | A1 to A6, label and `steps.csv` | All critical items pass |
| Feasibility | Time spent against the class budget | Within budget or replanned |
| Ethics | A3 to A5, hard-topic flag, public-room test ("would she tell this to people she has never met" [P4]) | Clear |
| Craft / usability | D1 sections B to PR, AI1 sweep, template-risk lint output | No critical fail; majors fixed |

Automatic fail: any critical item in D1; any BANNED tell from Q7/D4; unlisted changed regions.

**G4 chapter (assembled).**

| Check | Test | Pass |
|---|---|---|
| Move-family variety | MO9 | True |
| Holds and silence | Share of held shots at least 35%; at least one picture-led silence of 3 s or more per chapter | True |
| Rhythm | Shot-length coefficient of variation at least 0.4 (J); no run of 4 shots within 20% of the same length | True |
| Palette and type continuity | C2, type spec identical | True |
| Finish frequency | FN3 | True |
| AI-tell sweep | 1 frame per second of the chapter at 100% in contact sheets, plus full-speed viewing | No banned tell |
| Captions | Reading-speed and length limits from the format track | True |
| Loudness plan | Present | True |
| Strangers' evidence | After the screenings, count of independent marks per minute (D6) | Two or fewer per minute |

### D4. Banned "cheap tells" list

Banned in the public cut. Each is detectable by the test shown.

1. **Default or uniform ease** (`power1.out` everywhere; one spring config; evenly spaced stagger). Test D1 items MO1, MO9.
2. **Same slow zoom-in on every photograph.** Test MO9 (family key).
3. **Stacked finish**: more than two global finishing layers, or any layer on more than 80% of shots. Test FN1, FN3.
4. **Letterbox bars, vignette, lens flare, bloom or halation added to hide weak design.** Test FN2.
5. **Stock dust, scratch, light-leak or film-burn overlays** and fake date stamps; also never age material that is already aged [P1].
6. **Looped grain under 48 frames.** Test FN7.
7. **Live full-frame grain filters** (slow, not repeatable [P3]); grain is baked.
8. **Beat-synced zoom punches, whip pans and trending transitions** [P1][P3].
9. **Lower-thirds grammar for people outside the credits**; typewriter reveals; centred glowing titles [P3].
10. **Generated text, signs, logos** (Q7 row 7).
11. **Generative hands in photographic shots** (row 6).
12. **Animated eyes, blinks, lip movement, speech from stills** (rows 9, 18).
13. **Regenerated or "improved" faces; skin smoothing; invented teeth** (rows 4, 5).
14. **Mirrored photographs** (A6).
15. **Morphs between different people** (row 3).
16. **Teal-orange default grade; over-saturated skies and greens** (row 12).
17. **Generic AI lighting and centred epic compositions** (rows 10, 11).
18. **Paper-doll cut-outs**: visible slab edges, fringes, no ground contact (FN4, B3).
19. **Depth-of-field blur on faces; per-pixel depth defocus halos** (FN8).
20. **Cloned voices; AI-sung words; new sentences in her handwriting font** [P3 pitfall 16][P5].
21. **Sepia or "old film" filters over everything**; stacked era filters [P1].
22. **The Minecraft name as a title, or unlicensed brand marks** [57].
23. **Saturated 1-px lines; text under 2.5% x-height** (PR2, TY1).
24. **ffmpeg `zoompan` for a final push** (MO8).
25. **Phone "memory"-style themes and auto-music** [P1].

### D5. Projection-truth checklist

Run once at the premiere venue (or an equivalent hall) with the real projector, at least two weeks before 2027-02-27, and again on the day. A "test card" file is a short 24 fps video with: PLUGE and a 21-step grey ramp, a dark gradient, colour bars, three skin-tone stills, a type-size ladder (x-height 1.5% to 4% in 0.5% steps), a line ladder (1, 2, 3 px, black and red), a moving-texture pan at 0.10, 0.143, 0.2 and 0.3 frame widths per second, a speech passage with numbers, and 30 seconds from the actual film. Agents can generate it; I have not.

| # | What passes on a laptop and fails on a 6 to 10 m screen | Check | Threshold | Source |
|---|---|---|---|---|
| 1 | Small type | Type ladder read from the back row | All lines marked "carries information" readable; font 5%+ of height, x-height 2.5%+ at 5 screen heights | [47] with derivation above |
| 2 | Text near the edge | Safe-area overlay | Inside 5% margins; faces not clipped | [45] |
| 3 | Fast pans | Pan test | No visible strobe at 0.143 frame widths per second; any faster needs blur or a declared whip | [41] |
| 4 | Crushed shadows | PLUGE and 21-step ramp with lights as for the event | First two steps above black distinguishable from black (J); story-critical detail above 10% signal | [39][33] |
| 5 | Brightness | Lumens and screen area, or a meter | About 45 nits or more at the screen centre for a cinema-like feel; below 30 nits, lift the grade using the venue's measured shadow compensation (J) | [35][33], lumen formula above |
| 6 | Gamma/colour | Skin-tone stills side by side with the laptop; reference gamma from the playback path | Faces not orange or grey; shadows not milky; decision recorded | [33][37] |
| 7 | Banding | Dark-gradient frame, full screen | No visible steps in a dark gradient at normal seat distance | (M) 26 vs 100 levels; [44] |
| 8 | Aliasing and thin lines | Line ladder | 2 px lines stable; 1 px red line visibly weaker (expected) | (M) |
| 9 | Grain vs compression | 30 s film sample at the venue's actual file/DCP | Grain visible but not smeared; no mosquito noise around type | [42][34] |
| 10 | Judder | Pan test at 24 fps through the venue chain | Even cadence | [41] |
| 11 | Resolution scaling | 1-px checker pattern | No moire from the projector's scaler; text sharp | [34] |
| 12 | Picture modes | Menu inspection | Motion smoothing, sharpening, noise reduction and dynamic contrast off; overscan off | [38] |
| 13 | Speech intelligibility | Number passage read-back at the back row; STI if a meter is available | STI 0.60 or higher; read-back correct | [48] |
| 14 | Captions | Back-row read | Readable without leaning | [47] |
| 15 | Faces in group photos | Back-row identification of the featured person | Featured person's head at least 8% of picture height, or a move that brings it there (J) | J |

### D6. Strangers-to-her test-screening protocol

**Purpose.** Find problems the maker cannot see and check that the public room reads the film. Strangers cannot judge truth or likeness. The maker keeps a veto on facts about her.

**Timing (decision needed).** [P4] sets picture lock at Sat 2027-02-06. The brief's week 17 is Sun 2027-02-07 to Sat 2027-02-13. A screening then can drive only sound, grade, titles, captions and trims of about 2%. Recommend two sessions: **S1** with 3 strangers on the slice chapter in the slice-review week (about 2026-12-20, when changes are cheapest), and **S2** with 3 to 5 strangers on the locked cut in week 17. If the maker prefers one session, move picture lock to Sat 2027-02-13.

**Recruitment without revealing who she is.**

- Who: adults, 3 to 5, who have never met her and will not meet her, are not in her social circle, and do not share close acquaintances with the family. At least one should be film-literate (a local film club or animation student), because the others will be too kind.
- Pretext (truthful and partial): "I'm finishing a short animated film about one woman's life that will be shown at a gathering. I need people who don't know her to watch it and tell me where it fails. It takes about 90 minutes. Please don't share anything about it before it's shown." Do not say whose life; do not say it is a surprise.
- Privacy: show on the maker's own laptop or a borrowed projector in a neutral place; no copy leaves the room; phones away; no recording of video. Consider showing a **redacted cut**: surname, street names and phone numbers blurred or bleeped; everything else unchanged. State openly that details have been hidden. If redaction hurts specificity too much, choose strangers in a different city.
- Dignity: show only what is cleared for the public cut. Hard chapters default OUT [P4]; the strangers see the film as the public will.
- Thank-you, not payment (cost UNVERIFIED, J: a meal or $10 to $20 each).
- Written consent to view and to the privacy request, one page, kept offline.

**Sequence (about 90 minutes).**

1. Room: lights as at the event, sound levelled first, slates over missing parts [70].
2. Brief (30 seconds): "Please watch without talking. I will not answer questions until the end. I am looking for problems."
3. Screen the whole cut with no pauses [70].
4. Silence: two minutes to write, alone.
5. **Written sheet (before any discussion; anonymous; paper):**
   - A. One word for how it felt.
   - B. On a printed timeline, mark each moment you drifted, got confused or noticed something that looked wrong, fake or computer-made.
   - C. In three sentences, who is she?
   - D. Which scenes do you think were re-creations rather than real photographs? How could you tell?
   - E. Were the girl, the young woman and the older woman the same person? Where did you doubt it?
   - F. Was there anything you could not read or hear?
   - G. Which moment will you remember tomorrow?
   - H. Was any part too long or too short?
6. Group discussion, round-robin, moderator silent except "say more". Ask project-specific worries last (for example about a transition) so as not to sway opinions [70].
7. Close: thank them, repeat the privacy request.

**What not to ask.** "Did you like it?" (invites politeness); "Would she love it?" (they cannot know); "Should I cut X?" (invites fixes); anything revealing the family, the surprise, or the venue; leading questions about the tells ("did the faces look fake?") before the unprompted marks.

**How to weigh notes.**

- Independent counts: a problem marked by 3 or more of 5 (or 2 of 3) is a fix. Marked by 2 of 5, investigate. One viewer's taste is logged and not acted on unless it confirms a doubt the maker already had [70].
- Believe the diagnosis, discount the prescription [71]. Translate each note into the thing behind it ("I was bored" may be pacing or stakes [70]).
- Comprehension failures (C, D, E answers wrong) outrank taste.
- AI-tell marks: more than two independent marks per minute in a chapter sends it back to the Q7 table.
- The maker's veto: strangers cannot override facts about her, and anything about dignity is decided by the maker and flagged by the advisor [P4].
- Everything goes in the decision log with the action taken or the reason for no action.

**Pass/fail for the cut.** At least 80% of viewers (4 of 5, 3 of 4, 3 of 3) identify the reconstructions correctly (D) and say it is one person across ages (E); no unread text (F); no chapter above 2 tell-marks per minute.

### D7. Supporting templates

**Decision-log entry (ADR style [72])**

```markdown
## DL-014 Hold on twos for paper layers, ones for camera
Date: 2026-12-04 · Status: accepted · Supersedes: none
Context: slice shots 3 and 7 shimmered when the paper wobble ran on ones; Sprite Fright-style twos rule noted.
Decision: We will run paper wobble on twos and keep camera and type on ones.
Consequences: calmer texture; camera can still feel smooth; D5 test needs twos detection on drawn layers.
Evidence: LJ-C01-S003_v004, S007_v005 · Reversible: yes · Review at: week 9 drift check
```

**Chapter motion lint output (spec, not code)**

```json
{"shot": "LJ-C01-S014", "ease_class": "out", "axis": "push", "duration_s": 5.2, "magnitude_pct": 4.1,
 "cv": 0.92, "ends_ratio": 0.45, "peak_pos": 0.0, "settle_ok": true, "twos": false, "roughness": 0.11, "family_key": "out|push|3-6|3-6"}
```

**Weekly review card (one page).** Date; shots reviewed; 48-hour passes done; blind A/B results; three tells found; one decision logged; one anchor-frame comparison (better, same, worse).

### Deltas to existing playbooks (for the scribes)

| File and item | Change |
|---|---|
| `ai-imagery.md` Step 8, pure 2D push-in command | `zoompan` is 2.7 times rougher than sub-pixel resampling on slow 1080p pushes (M). Keep for proofs; use a Pillow or Blender sub-pixel render for finals |
| `ai-imagery.md` Step 9 line-up test and Step 11 "ask a relative who knew her" | Replace with the maker-alone blind line-up (Q3) plus the strangers' continuity question (D6 written question E). No relative sees drafts |
| `ai-imagery.md` Step 8 generated image-to-video | Tighten: no deliberate face regeneration or animation in the public cut; whole-frame image-to-video on a face-bearing photo only if A3 passes (5 of 5, twice, 48 hours apart); no eyes, blinks or mouth movement ever |
| `agent-pipeline.md` Step 6 baked grain, "8-frame loop on twos" | Use at least 48 distinct frames with seeded offsets; add the autocorrelation check (FN7) to the validators |
| `agent-pipeline.md` G2 and G4 | Add D1 sections and the MO9 chapter-variety rule with the ease estimator as an audit; add the stacked-finish count; add the swap test to G1 |
| `agent-pipeline.md` Decision 11 and G5 "trusted relative" proxy | Maker is the proxy with the 72-hour rule and advisor flagging [P4]; G5 is the maker plus advisor |
| `animated.md` Decision 9 | Same as above |
| `reviews/02` week 17 | Resolve the picture-lock clash (two sessions, or lock on 2027-02-13) |
| `agent-pipeline.md` G6 TV check | Record the TV picture mode (Filmmaker Mode or equivalent) [38] |

---

## Tools, services and costs (as of 2026-10-18)

| Item | Use | Cost / licence | Note |
|---|---|---|---|
| ffmpeg 6.1.1 (`signalstats`, `vidstabdetect`, `tblend`, `deband`, `gradfun`) | Flicker index, banding fixes, encodes | Free | Verified present in the cloud container (M). Windows build not checked |
| Python with numpy and Pillow | The estimator, grain-loop, ΔE00 and line tests | Free | I ran everything with `python3 -I`; scripts described under [76] |
| Blender | Hero shots, sub-pixel camera renders, EEVEE previews | Free | *Flow* and *Away* calibration [23][24] |
| DCP-o-matic | Test DCP and colour-conversion checks | "Free and open-source" [58] | Licence and Windows build not confirmed |
| DaVinci Resolve | Grade, scopes, Fusion light wrap | Free edition; Studio $295 per [P1] | Free-edition feature split unconfirmed [P1] |
| GSAP | Authored eases (RoughEase, CustomEase) | Licence may be revised; pin the version [P3] | Default ease `power1.out` [69] |
| OFL fonts | Titles and captions | Free; OFL allows video titling and embedding [56] | Check each font's licence file; commercial fonts need a film-exhibition licence (UNVERIFIED per vendor) |
| Generative image/video (Veo, Kling, Runway, Seedance, FLUX, Qwen) | Optional non-face inserts, stylisation of non-face material | Prices in [P2] dated 2026-10-18 (Veo 3.1 $0.25 to $2.00 per 5 s clip at 720p) | Tool volatility: a vendor shutdown was reported in May 2026 [11] |
| Colorimeter or lux meter | Optional venue check | Price UNVERIFIED | A phone lux app is a rough substitute (accuracy UNVERIFIED) |
| Test-screening costs | Meals or small thanks | $0 to $100 total (J) | Neutral venue assumed |

---

## Risks, pitfalls and ethics (with mitigations)

1. **Treating laurels as proof.** Vendor-run festivals reward novelty [1][2]; official prize lists can disagree with social posts [7]. Mitigation: calibrate on the non-AI films and on our own projection test; use laurels only to find process interviews.
2. **Studio-scale practice transplanted.** No daily reviews with twenty people; no colour-script department. Each ritual above has a one-person version.
3. **Detecting only what is easy.** My motion test was validated on synthetic pushes at 540p; it cannot see overshoots or tails below about 10% of peak, pans were not tested, and grain raises the noise floor. Mitigation: run on pre-finish renders; keep the maker's blind A/B as the final word.
4. **Over-finishing as a substitute for design.** Mitigated by FN1 to FN3 and the finish-off test.
5. **Identity.** No validated method for stylised cross-age identity [Q3]. Mitigation: hand-built faces from boards; maker-alone line-up twice; strangers test continuity only.
6. **Training a model on her face without her knowledge.** She cannot consent. Mitigation: default no; if the maker decides yes, local training, deletion afterwards, label, and never in the public cut without the maker's explicit sign-off [P2].
7. **Test-screening leak and privacy.** Strangers still know the maker, and may see her name and face. Mitigations: pretext, no copies, neutral venue, redacted cut, choose people outside the family's social graph, written promise.
8. **Dignity.** Strangers see only what is cleared for the public cut; hard chapters default OUT [P4].
9. **Picture lock clash.** The week-17 screening comes after lock; see D6.
10. **Unknown venue.** Brightness, ambient light, projector and sound are unknown. The maker should supply: venue type, screen size, projector model, who runs AV. Until then the numbers above are scenarios.
11. **Honest labelling will be read by a mixed public.** Frémaux's "made without AI" remark [9] and the Annecy mood [5] show some viewers are hostile. Mitigation: the disclosure card and end-credit cue sheet [P1][P2], and a film whose AI use is visibly small and in service of a human material.
12. **Brand risk if a voxel look is used** [57].
13. **Vendor-sourced numbers.** invideo.io, Saga, Opus Pro and seeddance.io all sell AI video tools [15][16][19][66]; I used them only to find themes and flagged them.
14. **Disk.** The shared cloud container reached 100% full during this session (other sessions' data). My spike files were deleted after use; nothing personal was involved.

---

## Open questions / gaps

1. **No film watched.** All shot-level claims for the festival films and for *The Kid Stays in the Picture*, *Up* and the Burns films are unverified. A stopwatch breakdown of three reference films would give the camera ranges in D2 an evidence base.
2. **Up colour script images not seen.** The book *The Art of Pixar* is the source; the maker may own or borrow it.
3. **SMPTE RP 431-2 and ST 428-1 not read.** DCI's normative reference for luminance, contrast and gamma is behind them. The 48 cd/m² figure and tolerance come from a compliance test plan seen only as search-result text.
4. **No empirical source for hold lengths on large screens, or for the 48-hour rule.** Both are practitioner heuristics (J).
5. **STI measurement for a non-expert.** I did not find a trustworthy phone-based method (UNVERIFIED).
6. **Cross-age identity.** No validated method; the research I found covers photographs, not stylisation.
7. **Real scanned grain libraries and their licences** were not researched.
8. **Venue and playback path** unknown (DCP, HDMI, USB; frame rate; screen size; ambient light).
9. **Hours per finished minute for AI films** exist only as secondhand figures (Gaudette) or vendor FAQs [15]; no independent audit found.
10. **Estimator validation on real photographs** (faded, low-resolution) has not been done; synthetic textured stills only.
11. **Costa Verde's "Best Film" claim.** The prize list shows the CapCut Prize and a different Best WAIFF Film [7]; the LinkedIn claim is unconfirmed. The Nowness page (503) might clear it up.
12. **Fast Company, Variety, Bloomberg, Deadline and THR pieces** were paywalled or blocked; cited from search-result text only.
13. **Minecraft projection rule** needs the games and theatrical-delivery tracks [57].
14. **Whether strangers should see a redacted cut** is a trade-off the maker must decide.

---

## Sources

Format: [n] title — URL — date — note. "Fetched" means I opened the page. "Search-result only" means I saw the claim in a search result but the page did not load or I did not open it.

**AI film festivals, AI-assisted films, critics**
- [1] AIF 2026 (Runway AI Festival) — https://aif.runwayml.com/ — fetched 2026-10-18 — fourth edition, winners, prizes, jury, partners.
- [2] Runway AI Film Festival 2026: Winners and Films (hollywood.ai) — https://hollywood.ai/awards/runway-ai-film-festival — fetched 2026-10-18 — third-party aggregator; runtimes, entry rule, judging criteria.
- [3] "Prompting is not directing" (Robert Gaudette interview, Envato Elements Learn) — https://elements.envato.com/learn/a-face-only-a-mother-could-love — 2026-07-29 — process, no selection ratio stated.
- [4] Runway Showcases AI-Generated Shorts to Packed Audience (letsdatascience, summarising THR and Business Insider) — https://letsdatascience.com/news/runway-showcases-ai-generated-shorts-to-packed-audience-3825c8ad — 2026-06-19 — audience, "boring", two weeks of 17-hour days.
- [5] "What's left is you": AI is the elephant in the room of Europe's biggest animation festival (Euronews) — https://www.euronews.com/2026/07/12/whats-left-is-you-ai-is-the-elephant-in-the-room-of-europes-biggest-animation-festival — 2026-07-12 — Annecy, "faster without AI", "the average or the mean".
- [6] Costa Verde (Short Shorts Film Festival & Asia 2026 programme) — https://www.shortshorts.org/2026/en/program/costa-verde/ — fetched 2026-10-18 — "Created with AI (bar one shot)", runtime 11:35.
- [7] WAIFF prize list — https://worldaifilmfestival.com/prize-list/ — fetched 2026-10-18 — 2026 winners, CapCut Prize; organiser and sponsor names read from logos (low confidence).
- [8] Cannes hosts first World AI film festival as copyright row erupts (Resultsense, citing The Guardian) — https://www.resultsense.com/news/2026-04-27-cannes-world-ai-film-festival-debut — 2026-04-27 — submissions, pulled film.
- [9] Cannes 2026 rolls out red carpet amid AI spat (France 24) — https://www.france24.com/en/culture/20260512-cannes-film-festival-opens-grappling-with-ai-and-hollywood — 2026-05-12 — Frémaux on labelling, Meta sponsorship.
- [10] OpenAI-Backed Animated Film 'Critterz' Aims For Cannes (Cartoon Brew) — https://www.cartoonbrew.com/feature-film/critterz-ai-feature-openai-cannes-254237.html — 2025-09-18 — pitch, "democratizing" critique.
- [11] Critterz at Cannes 2026 (Deadline; Bloomberg "misses Cannes debut after OpenAI shut Sora") — https://deadline.com/2026/05/open-ai-produced-animated-family-film-critterz-cannes-1236879586/ and https://www.bloomberg.com/news/articles/2026-05-22/ai-cartoon-critterz-misses-cannes-debut-after-openai-shut-sora — 2026-05 — search-result only (paywalled).
- [12] How Good is Sora Actually? Interview with the filmmakers behind Air Head (No Film School) — https://nofilmschool.com/sora-ai-filmmaker-interview — 2024-04-02 — 2 to 3 seconds kept from 20-second generations; post work.
- [13] At the AI Film Festival, humanity triumphed over tech (TechCrunch) — https://techcrunch.com/2024/05/11/at-the-ai-film-festival-humanity-triumphed-over-tech — 2024-05-11 — critical review of AIFF 2024 (older than six months; historic).
- [14] This film festival left me feeling better about AI moviemaking (Fast Company) — https://www.fastcompany.com/91565229/runway-ai-film-festival — 2026 — search-result only (403).
- [15] AI Video Generations Per Usable Shot (invideo.io FAQ) — https://invideo.io/faq/how-many-ai-video-generations-do-you-need-per-usable/ — July 2026 — vendor; search-result only.
- [16] State of AI Filmmaking 2026 (Saga/CyberFilm) — https://www.createsagas.com/post/state-of-ai-filmmaking-2026-what-40-ai-film-leaders-told-us-may-surprise-you — 2026 — vendor; fetched; no selection-ratio data.
- [17] 10 Animators to Watch Discuss AI, the Future and the Human Hand (Variety) — https://variety.com/2026/film/awards/10-animators-to-watch-ai-animation-future-scad-1236894996/ — 2026 — search-result only.
- [18] How I learned to stop worrying and love AI slop (MIT Technology Review) — https://www.technologyreview.com/2025/12/23/1130396/how-i-learned-to-stop-worrying-and-love-ai-slop/ — 2025-12-23 — fetched; older than six months, background.
- [19] The AI Slop Aesthetic: 12 Tells That a Video Was Made by AI (Opus Pro) — https://www.opus.pro/blog/ai-slop-aesthetic-12-tells — 2026-04-17 — vendor; fetched.
- [20] NOWNESS Experiments: Costa Verde — http://amp.nowness.com/story/costa-verde-leo-cannone — search-result only (503); Midjourney, MiniMax, one filmed shot.

**Non-AI calibration and style/identity practice**
- [21] This Annecy animated short took 11 years and 75 oil paintings (Creative Bloq via Yahoo) — https://www.yahoo.com/entertainment/movies/articles/annecy-animated-short-took-11-120000725.html — 2026-06-09 — Danse Macabre, fenced AI.
- [22] How Fusion Studio and expert compositing skills brought Danse Macabre to life (Creative Bloq via Yahoo Tech) — https://tech.yahoo.com/general/articles/fusion-studio-expert-compositing-skills-090000004.html — 2026-09-23 — global grain last, compositing steps.
- [23] Making Flow – Interview with director Gints Zilbalodis (blender.org) — https://www.blender.org/?p=93732 — fetched 2026-10-18 — team, render times, no compositing.
- [24] Yes, one animator made the CG animated feature Away on his own (Cartoon Brew) — https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html — 2019-06-06 — solo workflow, shortcuts.
- [25] How Spider-Man: Into the Spider-Verse's technical wizardry works (Gizmodo) — https://gizmodo.com/how-spider-man-into-the-spider-verses-technical-wizard-1831179866 — 2018-12-18 — twos as a creative call.
- [26] Sprite Fright style guide (Blender Studio blog; BlenderNation 2021-06-20) — https://studio.blender.org/blog/sprite-fright-style-guide and https://www.blendernation.com/2021/06/20/sprite-frights-style-guide-published/ — 2021 — summary only.
- [27] Flee interview (Seventh Row) — https://seventh-row.com/?p=45371 — fetched 2026-10-18 — art bible, good/not good, eyes.
- [28] What is an art bible? (Oleander Studios) — https://www.oleanderstudios.com/what-is-an-art-bible-examples-practical-tips/ — fetched 2026-10-18 — typical sections.
- [29] Early 'The Simpsons' Style Guide (Slashfilm) — https://www.slashfilm.com/573760/the-simpsons-style-guide/ — 2020-04-26 — 500-page guide, micro-rules.
- [30] Character Sheets: The Blueprint for Consistent Animation (cg-wire) — https://blog.cg-wire.com/character-sheet-animation — updated 2026-03-26 — sheet contents.

**Colour, projection, finish**
- [31] Ralph Eggleston talks Inside Out (Animation World Network) — https://www.awn.com/animationworld/ralph-eggleston-talks-inside-out — fetched 2026-10-18 — colour script as shorthand of emotion.
- [32] Lou Romano's colour script for Pixar's Up (Slashfilm) — https://www.slashfilm.com/503975/cool-stuff-lou-romanos-color-script-for-pixars-up/ — 2009-06-02 — colour arc; fetched.
- [33] White Paper on Ambient Light Compensation for Filmmaker Mode (UHD Alliance) — https://alliance.experienceuhd.com/wp-content/uploads/2025/10/UHDA-White-Paper-on-Ambient-Light-Compensation-for-Filmmaker-Mode-v4-clean.pdf — file dated 2025-10-08 — 5 cd/m² reference surround; gamma table; I read the whole 4 pages.
- [34] Digital Cinema System Specification v1.4.4 (DCI) — https://documents.dcimovies.com/DCSS/42cfeb997ae72dd484f7b027547e6e0bfad43ecf/Digital%20Cinema%20System%20Specification.pdf — approved 2024-01-03 — 12-bit XYZ, 2K 2048x1080 at 24/48 fps, 250 Mbit/s; I read the relevant sections; RP 431-2 is normative but not read.
- [35] DCSS Compliance Test Plan 1.4.1 (DCI) — https://documents.dcimovies.com/CTP/release/1.4.1/ — ambient under 0.01 cd/m² fetched; "48.0 ± 3.5 cd/m²" white seen in search-result text only.
- [36] Poynton notes on BT.1886 — https://poynton.ca/notes/misc/flummoxed.html — search-result only (page 404 on fetch); reference conditions.
- [37] DCP-o-matic user mailing list, colour conversion threads — https://lists.dcpomatic.com/hyperkitty/list/users@lists.dcpomatic.com/message/27TBTWCAFUWRT73LEI2VANYMJOQWDXWL — search-result only; practitioner opinion.
- [38] Filmmaker Mode feature summaries (Tom's Guide and others) — https://tomsguide.com/features/what-is-filmmaker-mode-heres-why-you-should-use-this-picture-perfect-setting — search-result only; launch-era (2019 to 2020) descriptions.
- [39] Black Level (PLUGE) test (TestUFO) — https://www.testufo.com/blacklevels — fetched 2026-10-18 — how to read a PLUGE.
- [40] Delta-E CIEDE2000 documentation (MetricGate) — https://metricgate.com/docs/delta-e-ciede2000/ — fetched 2026-10-18 — interpretation bands for flat patches.
- [41] Camera panning speed (RED) — https://www.reddigitalcinema.com/red-101/camera-panning-speed — undated, copyright 2004 to 2026 — seven-second rule, shutter angle.
- [42] Film Grain Synthesis for AV1 Video Codec (Norkin and Birkbeck, Netflix/Google) — https://norkin.org/pdf/DCC_2018_AV1_film_grain.pdf — 2018 — grain statistics and compression difficulty; read locally.
- [43] Netflix film grain synthesis saves on the bitrate (Broadband TV News) — https://www.broadbandtvnews.com/2025/07/04/netflix-film-grain-synthesis-saves-on-the-bitrate/ — 2025-07-04 — search-result only (307).
- [44] Banding in gradients (Fora Soft) — https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps — fetched 2026-10-18 — causes, CAMBI, dither advice.
- [45] EBU R 95: Safe areas for 16:9 television production — https://tech.ebu.ch/docs/r/r095.pdf — revised 2016 — action 3.5%, graphics 5%; read locally.
- [46] SMPTE RP 218 and ST 2046-1 safe areas — https://pub.smpte.org/pub/rp218/rp0218-2009.pdf — 2009 — search-result only (93% figure from ST 2046-1 descriptions).
- [47] Does size matter for reading? (Legge and Bigelow, Journal of Vision 11(5):8) — https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf — 2011 — fluent range 0.2 to 2 degrees x-height; read locally.
- [48] Speech transmission index (Wikipedia) — https://en.wikipedia.org/wiki/Speech_transmission_index — fetched 2026-10-18 — IEC 60268-16 bands.
- [49] Ambient-light contrast measurements (Sound and Vision, Planar Xscreen) — https://soundandvision.com/node/82167 — search-result only (403): 57:1 and 194:1 with lights on.
- [50] Light Wrap operator (Vindral Composer docs) — https://composer-docs.vindral.com/operators/operators-light-wrap.html — fetched 2026-10-18 — chain order, parameters.
- [51] BokehDiff: Neural Lens Blur with One-Step Diffusion (arXiv 2507.18060) — https://arxiv.org/pdf/2507.18060 — 2025 — search-result only; halos at depth edges.
- [52] TIFF/EXIF tag FocalLengthIn35mmFilm (0xA405) — https://awaresystems.be/imaging/tiff/tifftags/privateifd/exif/focallengthin35mmfilm.html — search-result only.
- [53] The Kid Stays in the Picture (kottke) — https://kottke.org/03/07/the-kid-stays-in-the-picture — 2003 — fetched; technique.
- [54] Meaning in Motion: Ken Burns and His 'Effect' (Poynter) — https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect — 2007-06-21 — fetched.
- [55] 6 'Rules' for Good Cutting According to Walter Murch (No Film School) — https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch — 2016 — fetched.
- [56] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — fetched 2026-10-18 — video titling and embedding allowed.
- [57] Minecraft Usage Guidelines excerpt (local, captured 2026-10-18) — research/sources/minecraft-usage-guidelines-2026-10-18.txt — physical locations, name as title.
- [58] DCP-o-matic — https://dcpomatic.com/ — fetched 2026-10-18 — "Free and open-source"; licence not stated on the page.

**Identity and AI technique**
- [59] Toward Trustworthy Portrait Editing: Evaluation of Demographic Misrepresentation in I2I Models (arXiv 2602.16149) — https://arxiv.org/abs/2602.16149 — v1 2026-02-18, v3 2026-06-04 — 62 to 71% skin lightening; fetched.
- [60] AgeBooth (arXiv 2510.05715) — https://arxiv.org/abs/2510.05715 — 2025-10-07 — age-specific LoRA fusion; fetched. (Identity-versus-age trade-off wording is from a search-result summary of the paper, not the abstract.)
- [61] DiverAge (arXiv 2606.04881) — https://arxiv.org/abs/2606.04881 — 2026-06-02 — cross-age identity drift; fetched.
- [62] FLUX.1 Kontext (arXiv 2506.15742) — https://arxiv.org/abs/2506.15742 — 2025-06 — claims improved multi-turn consistency; no limits listed on the abstract page.
- [63] CodeFormer (NeurIPS 2022) — https://proceedings.neurips.cc/paper_files/paper/2022/hash/c573258c38d0a3919d8c1364053c45df-Abstract.html — 2022 — fidelity/quality coefficient; the "features that may no longer exist" line is from a 2026 guide seen only in search results.
- [64] World Consistency Score (arXiv 2508.00144) and EvalCrafter (arXiv 2310.11440) — https://arxiv.org/pdf/2508.00144 — 2025/2023 — search-result only; warp-error flicker metrics.
- [65] Qwen-Image-Edit-2511 likeness LoRA guide (RunComfy) and community FLUX guides — https://www.runcomfy.com/trainer/ai-toolkit/qwen-image-edit-2511-likeness-custom-lora — 2026 — vendor; search-result only.
- [66] Best AI Video Generators for Character Consistency in 2026 (seeddance.io) — https://www.seeddance.io/blog/best-ai-video-generators-character-consistency-2026 — 2026 — vendor; search-result only.
- [67] Black Forest Labs documentation — https://docs.bfl.ai/ — fetched 2026-10-18 — undated; mentions FLUX.2 [klein] under "Apache 2.0 / FLUX Non-Commercial" and a "FLUX 3" model family.

**Craft and review practice**
- [68] CRAFT.md (bishpls/animation-pipeline) — https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md — fetched 2026-10-18 — timing, holds, review rules.
- [69] GSAP eases — https://gsap.com/docs/v3/Eases/ — fetched 2026-10-18 — families; default `power1.out`.
- [70] Six Tips for a Successful Test Screening (Frame.io) — https://blog.frame.io/2017/07/06/successful-test-screening-tips/ — 2017-07-06 — fetched.
- [71] Neil Gaiman's rule on feedback (Goodreads mirror of his blog) — https://www.goodreads.com/author_blog_posts/9436922-remember-when-people-tell-you-something-s-wrong-or-doesn-t-work-for-th — search-result only; originally in the Guardian "Ten rules for writing fiction", 2010-02-20 (the Guardian page was not fetchable).
- [72] Documenting Architecture Decisions (Michael Nygard) — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions — 2011-11-15 — fetched.
- [73] In praise of the squint (Painter's Keys) — https://painterskeys.com/praise-squint/ — search-result only.
- [74] The Animator's Survival Kit, table of contents (Internet Archive text) — https://dn721807.ca.archive.org/0/items/taskav-01/The__Animator%27s_Survival_Kit%5B1%5D_text.pdf — search-result only; chapter on timing and spacing and "ones and twos".
- [75] Proofreading guidance on delay and fresh eyes (Ragan) — https://www.prdaily.com/?p=256303 — search-result only; practitioner advice, no controlled study.
- [76] My measurements, 2026-10-18, cloud container, synthetic material only. M-C1 zoom-velocity classifier (least-squares zoom per frame pair; 4 s, 24 fps, 960x540 push-ins; six clips); M-C2 flicker index from `signalstats` YAVG (static 0.000, injected 2.58 levels); M-C3 grain-loop autocorrelation (8-frame loop on twos, r = 1.00 at lag 16); M-C4 dark-ramp banding (26 vs 100 levels, 8-bit vs 10-bit H.264); M-C5 grain bit cost at CRF 18 (7.8 KB to 356 KB); M-C6 thin-line survival (1920x1080, H.264 4:2:0, CRF 18); M-C7 `zoompan` vs sub-pixel roughness (0.35 vs 0.13 slow 1080p; 0.26 vs 0.08 faster 540p). The scripts are kept in research/cinematic-quality-fixtures/ with a README; media files were deleted after use; the shared disk reached 100% during the session for reasons outside this task.
- [77] ITU-R BT.1886 (Wikipedia) — https://en.wikipedia.org/wiki/ITU-R_BT.1886 — search-result only; gamma 2.4 reference EOTF.
- [78] InsightFace mirror pages (ArcFace, LFW and AgeDB-30 accuracies) — https://github.com/Soldie/insightface-Rec.Face — search-result only; community mirror, not the official repository.
- [79] Automatic Color Scheme Extraction from Movies (KAIST, ICMR 2020) — https://dspace.kaist.ac.kr/handle/10203/274604 — search-result only (page did not resolve).
- [80] Creating Motion in Stills: How to Animate a Photo in Post with the Parallax Effect (PetaPixel) — https://petapixel.com/2013/11/19/creating-motion-stills-animate-photo-post-parallax-effect — 2013 — search-result only.
- [81] How Pixar Fosters Collective Creativity (Ed Catmull, Harvard Business Review) — https://hbr.org/2008/09/how-pixar-fosters-collective-creativity — 2008-09 — opening and summary read; body paywalled.
- [82] Ken Burns on the 33-second zoom (CineD) — https://www.cined.com/?p=406363 — search-result only.
- [83] New Tech Offers An 'Ear To The Weird' at AI Film Festival (Yahoo Malaysia, wire copy) — https://malaysia.news.yahoo.com/tech-offers-ear-weird-ai-200000765.html — 2024 — search-result only; Get Me Out tools.
- [84] Total Pixel Space coverage — https://laughingsquid.com/total-pixel-space/ , https://wbgsv0a.gigazine.net/gsc_news/en/20250630-runway-ai-movie-festival-aiff-2025 , https://www.yourvalley.net/stories/paradise-valley-native-wins-2025-runway-ai-film-festival,594100 — 2025 — search-result only; I could not tell which of these pages carried which detail (tools, "more than a year", the Ars Technica quote).
- [85] The Art of Pixar: the complete colorscripts from 25 years of feature films (library record) — https://search.ub.tum.de/vufind/Record/DE-604.BV047101435 — search-result only.
- [P1] `playbooks/animated.md`; [P2] `playbooks/ai-imagery.md`; [P3] `playbooks/agent-pipeline.md`; [P4] `reviews/02-film-briefs-review.md`; [P5] `CHARTER.md` — all under , read 2026-10-18.
