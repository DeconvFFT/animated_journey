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
3. **Festival laurels are weak evidence.** Runway's AIF is run by the tool vendor, its jury includes Runway's co-founder and CEO, Cristobal Valenzuela [1], its prizes are partly Runway credits, its entries must use generative video, and one of four judging criteria is "creative and skilled use of AI techniques" [1][2]. WAIFF's own prize list shows *Costa Verde* winning the sponsor's "CapCut Prize", while a LinkedIn post (search-result only) calls it Best Film [7]. Cannes' main festival director talked about labelling films "made without artificial intelligence" [9].
4. **What the AI winners actually did is a lot of human work.** Gaudette: reference images and character sheets first, "a few tries" to "dozens" per shot, conventional editing, and reportedly two weeks of 17-hour days alone (about 30 hours per finished minute, my arithmetic on a secondhand figure) [3][4]. Air Head: 2 to 3 seconds kept from 20-second generations, balloon colour fixed in post [12]. Costa Verde: family photos and landscape documentation as references, Midjourney and MiniMax, one real filmed shot (the last shot, per a search-result snippet) [6][20]. TechCrunch's 2024 review (older than six months, historic) found that the human parts (performance, cinematography) carried the films [13], and 2026 coverage still reports several "boring" entries [4].
5. **Non-AI calibration shows what "theatrical" costs.** Away: one person, 3.5 years, 75 minutes (about 140 hours per finished minute, my estimate) [24]. Flow: 15 to 20 people, 3 to 5 at a time, about 5.5 years, no compositing, colour done in shaders, 0.5 to 10 seconds per 4K frame on one PC [23]. Danse Macabre (Annecy 2026): 75 oil paintings over 11 years, 30+ artists, a "fenced" AI stylisation pass trained on the painter's own surfaces, nearly every frame still corrected by hand, global grain as the last unifying step [21][22].
6. **A style bible is short, visual and has a "good / not good" page.** Flee's bible fixed how to draw a hand and an eye and showed "this is good / this is not good" from early tests [27]. Ours locks ten decisions before the slice (D2). Two are specific to this film: the reconstruction marker and the still-to-moving ratio.
7. **A colour script is a shorthand of emotion in colour and light** [31], made early and revised when the story changes ("I had to chuck it and start over" [31]). For a life film I propose one strip per era plus a numeric check of every shot against it (ΔE00 on the shot's dominant colours) and a venue test card (D5). Venue brightness is the hidden variable: a 5,000-lumen projector on an 8 m screen gives about 44 nits (my arithmetic), against the 48 cd/m² cinema reference [35], and ambient light erases shadow detail that the 5 cd/m² reference surround preserves [33].
8. **Gamma assumptions move shadows a lot.** The same dark code value is 37% darker on a 2.6 display than on a 2.4 display and 58% brighter on a 2.2 display (my arithmetic). Decide the playback path (DCP at 2.6 or HDMI at 2.4) in week 2 and grade for it, not for the laptop.
9. **No source I found validates identity for a stylised person across ages.** Research shows an identity-versus-age trade-off [60][61], iterative-edit drift [62], and demographic drift in 2026 portrait editors (62 to 71% of outputs lightened skin in one audit [59]). The honest plan: faces are built by hand from a per-age reference board; the maker alone signs likeness by blind line-up; strangers can test only whether the film reads as one person across ages, not whether it is her.
10. **The ease/hold test works and is cheap.** On synthetic push-ins my zoom-velocity estimator separated linear (coefficient of variation 0.03), ease in-out (ends at 0.16 of peak, peak at 0.48 of the move) and ease-out (peak at 0.00) and detected holds on twos (M). It also found that ffmpeg `zoompan`, which [P2] uses for its push-in example, is 1.7 to 2.7 times rougher than a sub-pixel resample on synthetic stills (M; 2.7 on the original slow 1080p push, roughness 0.35 against 0.13; 1.7 on the advisor's 2026-10-18 reproduction). Ban `zoompan` for final pushes.
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
- Reference white is 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2), ST 431-1 Table 1 [92]; gamma 2.6 ±5% in a theatre [91]. Ambient light on the screen with the projector off must be below 0.01 cd/m² (Review Room) or 0.03 cd/m² (Exhibition Theater), SMPTE RP 431-2 s6.1 [91]. [35] is superseded by [91][92][93] for these figures. RP 431-2 is the normative reference for the reference projector and viewing environment [34][91].
- Practitioner notes (DCP-o-matic mailing list, search-result only): Rec.709 source is often treated as 2.2 and the colour conversion has to account for DCI projection at 2.6; modern gear labelled Rec.709 usually means BT.1886; choosing the wrong input gamma gives a visibly lighter or darker picture; "the only reliable check is a properly calibrated cinema screening" [37]. DCP-o-matic describes itself as "free and open-source" [58].
- My conclusion (J): the maker must decide the playback path in week 2. If the venue plays a DCP, grade for BT.1886 (2.4) and convert with the matching input-gamma setting, then check a test DCP on a real cinema server. If the venue plays an HDMI or USB file, grade for 2.4 in a dim room or 2.2 if the lights stay up, and set the projector's gamma to match. The theatrical-delivery track owns the choice; this note supplies the checks.

**What consumer TV picture modes do.** Filmmaker Mode is a UHD Alliance preset that turns off most post-processing: motion smoothing off, D65 white point, sharpening and noise reduction off, overscan off unless signalled, aspect ratio and frame rate kept [38 (summaries in search results; the UHDA white paper [33] confirms the mode's purpose)]. "Vivid" and "Standard" modes typically add saturation, sharpening and motion interpolation (J; common knowledge, UNVERIFIED here). The test for the TV at 3 m in [P3] G6 should therefore state the mode used and record it.

### Q3. Identity across ages and shots

**Studio practice.** A model sheet or character sheet is the shared reference so every artist keeps a character recognisable: turnaround, expression sheet, pose sheet, props and scale, colour palette, and written annotations [30]. Flee had to stop fifty animators drawing one man's eyes differently [27]. The Simpsons guide encodes identity as micro-rules [29].

**Our equivalent for a real person in a stylised look (ai-imagery L3).** A **per-age reference board** (ages 6, 25, 55 as the brief says; add more only when a chapter needs them). Template in D2b. In short each board holds: 3 to 5 source photos with dates (L0/L1), a list of identity attributes (hair shape and parting, brows, eye set, nose, mouth, ears, glasses, posture, height relative to others), a stylised front, three-quarter and profile in the house material, five expressions only (neutral, smile, laugh, listening, tired), a head-height proportion chart, costume and colour swatches (skin swatch sampled from the scan), and a "do not" list with the failure examples.

**The rules.**

- A photograph stays a photograph: stylisation is a separate asset and never replaces a photo in a factual beat [P2]. Never synthesise a different age of her from a photo.
- **Likeness sign-off by the maker alone.** Protocol, run twice 48 hours apart: (1) the agent prepares a shuffled line-up of 5 stylised faces, one correct and four decoys (decoy set A: the same stylisation applied to public-domain stand-in portraits already listed in `ai-imagery.md`, NARA 546220 and US Navy 80-G-27208 among them, or to the maker's own face; never a relative's photo, who cannot be told why. Decoy set B: the same stylisation applied to her at other ages. Set A tests likeness; set B tests age discrimination); (2) the maker picks without seeing labels; (3) pass is 5 of 5 correct picks, then pass again 48 hours later; (4) the maker records what feature tipped the choice, which becomes a board attribute. This replaces the relative line-up in [P2] Step 9, because the maker is the only person who may see her. (J)
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

- **MO1 (spec, Crit, every move).** No framework default ease (`power1.out` for GSAP, `ease` for CSS), and no `linear` ease unless the brief declares `drift: declared`. This is checked from the timeline spec, so it also covers pans, tilts, orbits and multi-plane moves.
- **MO1b (pixels, Maj, pushes and pulls only).** A move passes when its CV is over 0.12, or when it declares `drift: declared`. Pan, tilt, orbit and multi-plane moves report `unknown`, never `pass`, because the estimator was validated on push-ins only.
- A move with a settle has an end-speed ratio under 0.3 and a monotone decay over the last 15% of its duration (spec-level; the pixel audit cannot see small overshoots).
- **Family key** = (ease class, axis, duration bucket, magnitude bucket). Axis = push, pull, pan left, pan right, tilt up, tilt down, none. Duration buckets: under 3 s, 3 to 6 s, over 6 s. Magnitude buckets: under 3%, 3 to 6%, over 6% of frame.
- **Chapter rule:** over any run of 8 consecutive moving shots, at least 3 distinct family keys, no key above 40%, no key repeated more than twice in a row, and Shannon entropy of keys at least 1.5 bits. These numbers are a starting point to calibrate on the slice.
- Held shots count as their own family (`none`) and should be at least 35% of photo shots.

*Limits.* Tested on synthetic pushes only. Settle and overshoot checks therefore belong to the spec-level test (Level 1), with the pixel audit using a 10% tolerance. Pan speed is validated (M-C9); pan ease is not. Multi-plane parallax has one velocity per layer, so measure layers from the timeline spec and use pixels only as an audit. Run on the render before grain, because grain and compression noise raise the noise floor.

*A related finding that changes a recommendation.* On a slow 4% in-out push at 1080p from a 4K source, ffmpeg `zoompan` showed a frame-to-frame velocity roughness of 0.35 against 0.13 for a sub-pixel bicubic resample (M, same estimator, relative to mean speed). On a faster 10% push at 540p the gap was 0.26 against 0.08. `zoompan` snaps its crop window to whole pixels, which shows up as shimmer on slow moves. [P2] Step 8 uses `zoompan` in its example; keep it for proofs, not finals. Reported as a range, M-C7 is **1.7 to 2.7 times rougher on two synthetic stills**: 2.7 on the original (0.35 against 0.13) and 1.7 on the advisor's reproduction of 2026-10-18 (Pillow 0.19, zoompan 0.33). A scribe check on 2026-10-18, with a third still generated by numpy (FFT-filtered noise, 1920 by 1080, `ZV_SIZE=1920x1080`), gave 3.6 (zoompan 0.277 against Pillow 0.076). The ratio depends on the content, so report a range, not one number. The follow-up round measured 4 to 20 times on three real scanned prints (FQ2). MO8 therefore passes when roughness is no more than 1.3 times a Pillow sub-pixel reference render of the same move **and** centre jitter is at most 0.05 px at 1080p on the delivered file (MO8a, `analyse()` in `zoompan_vs_subpixel_prints.py`; edge jitter at most 0.04 px, MO8b, decides ties). There is no absolute roughness threshold: the Pillow floor read 0.13, 0.19, 0.076 and 0.064 on four synthetic stills and 0.03 to 0.08 on three real prints, so an absolute number is meaningless without the reference. The nine-frame-residual roughness is in `zoom_velocity_classifier.py` (set `ZV_SIZE`), so the number can be reproduced from the saved scripts. The FQ2 jitter proposal is adopted (review round 2, 2026-10-18).

### Q6. Compositing finish and its limits, and the projector cautions

**Real grain versus synthetic.**

- Real film grain is spatially correlated (grains can be more than one sample in size), temporally independent (new each frame), and its strength depends on image intensity; independent per-pixel noise from a digital sensor has different statistics [42]. Plain per-pixel Gaussian noise therefore tends to read as "digital noise," not film (J).
- Danse Macabre's compositor applied "a global film grain over the entire composition" as the final unifying step [22]. Flow used no compositing at all; all colour was tweaked in shaders [23]. Two valid answers: finish once at the end, or design the finish into the render.
- **Matching rule that needs no taste (J):** measure the standard deviation of luminance in a flat patch of each era's scans; set grain on new (L5) layers within ±30% of that value, so the new layers sit with the photographs [P1] ("put the era on the new layer only").
- **Baked overlays.** The baked-grain template `grain-8f-on-twos` in `research/agent-pipeline.md` (M6) uses an 8-frame grain loop on twos. My test of that design (M): a loop of 8 distinct grain frames held on twos repeats exactly every 16 frames (0.67 s); frame-to-frame correlation at lag 16 is 1.00, against 0.00 for fresh grain at every lag. A viewer may not name it, but flat areas will "breathe" in a pattern. Use at least 48 distinct grain frames (4 s at 12 fps), start each shot at a different seeded offset, and test for a repeat with the same autocorrelation.

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
| 1 | **Face drift** (face changes across frames or shots) | Generators re-synthesise faces per clip; iterative edits accumulate change [62][59][65] | Step frames at 0, 25, 50, 75, 100% at 100% zoom; side-by-side with the L1 source; landmark ratio alarm (2%); maker's 5-of-5 blind line-up (D1 A3) | Do not generate faces: keep the original face region, use 2.5D from the photo; clips 3 to 5 s; fixed seed; pick the take with least change [P2]; always re-anchor to the original, never the last output | Environment motion with the face region kept from the L1/L2 photo: **LABEL L4b**. Whole-frame image-to-video on a face-bearing photo: **LABEL L4b only if A3 passes**, otherwise **BANNED**. Deliberate face regeneration or animation: **BANNED**. Faces of the dead: **BANNED by default in the public cut** (delta to `ai-imagery.md` principle 7, Step 8 and Decision 4: under the sole keeper nobody can be asked before the premiere, so environment and parallax motion only; revisit after the reveal with written consent from next of kin) |
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
| Runway AIF (2026 was its fourth edition: New York 2026-06-11, Los Angeles 06-18, Tokyo 07-30; $135k+ prizes) | Runway, which sells generative video. Partners: Lionsgate, Tribeca, The Gotham, Monks, Adobe, Roku, Nvidia. Jury includes Cristobal Valenzuela (co-founder and CEO of Runway, as the page lists him) [1] | Showcase for the tool; Grand Prix $50,000 plus 1,000,000 Runway credits; entries must use generative video; judges score "creative and skilled use of AI techniques" among four 1 to 10 criteria [1][2] | Gaudette said the project began as a personal experiment "to use for marketing his AI services" [3] |
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
| *Away* (Zilbalodis, 2019) | Solo; Maya; real-time viewport playblasts; no script or storyboard, story found by editing rough animation; 75 min; 3.5 years, 8 to 10 hours a day, seven days a week; many long takes with a floating camera; characters without shadows; copied animation across identical cats [24] | Constraints chosen early (no shadows, identical crowd) are what made a solo feature finishable. The shortcut is declared in the bible |
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

- Practitioner guidance for test screenings: 4 to 10 people, limit industry people to a couple, level the sound before the audience sees it (the source does it after the makers' own first viewing) [70] ("Bad sound is so distracting that it often can ruin a regular screening"), slate over missing parts, watch without pausing, ask the basics on a questionnaire first and project-specific worries last "so as not to sway their opinions" [70].
- Weigh notes by repetition, decode the note behind the note ("I was a little bored" may mean weak stakes or pacing) [70], and follow Gaiman's rule, paraphrased: people are almost always right that something is wrong or does not work for them, and almost always wrong about how to fix it (search results confirmed the first half of his sentence verbatim and the second half in paraphrase) [71].
- With 3 to 5 viewers you cannot estimate rates; you can only find problems. Use thresholds on counts (D6).
- Recruitment must not reveal her identity beyond the film, and must not be possible to leak back to her circle. See D6 for the redacted-cut option and the truthful pretext.

### Q10. Projection truth

See D5 for the full checklist. Key derived numbers (my arithmetic unless cited):

- **Type.** The fluent reading range for x-height runs from about 0.2 degrees to 2 degrees [47]. At 0.2 degrees the minimum x-height as a fraction of picture height is about 0.0035 × (farthest seat distance ÷ picture height): 1.4% at 4 screen heights, 1.75% at 5, 2.1% at 6. With a 1.5 times margin for projected, lower-contrast text: 2.1%, 2.6%, 3.1%, which corresponds to a font size of roughly 4.2%, 5.2%, 6.3% of picture height (45, 57, 68 px at 1080). Rule: **applies to type we set; text inside photographs and her handwriting is exempt; below 2% x-height text is decorative and must not carry information.** For type we set (titles, cards, date lines, captions, credits), x-height is at least 2.5% of picture height and font size at least 5%. (J, scale to the venue's real seat distances.) Captions follow `format.md` Step 8 (7 to 8% line height), which at 1080p is `FontSize=23`: x-height 3.2 to 3.8% of picture height across five fonts, line pitch 7.96% (M-C8). Caption x-height floor 3.1% (6 screen heights, J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font; TY1 is a floor, not a caption size.
- **Safe areas.** EBU R95 (June 2017, Ver. 1.1, with 2016 errata): action safe 3.5% and graphics safe 5% margins, top, bottom and sides [45]; SMPTE ST 2046-1 uses 93% for action [46]. Rule: all text inside 5% margins.
- **Pan speed.** At most one frame width per 7 seconds at 24 fps (0.143 frame widths per second; 11.4 px per frame at 1920 wide) [41], on the fastest textured layer.
- **Brightness.** Screen luminance in nits ≈ lumens × gain ÷ (π × screen area in m²). Screen 6 m wide: 3,000 lm gives about 47 nits, 5,000 lm about 79. Screen 8 m: 27 and 44 nits. Screen 10 m: 17 and 28 nits (ideal, before lamp, lens and ageing losses). DCI reference is 48 nits [35]. Most public-gathering projectors will be dimmer than a cinema and the room will not be as dark, so shadow detail is at risk [33].
- **Black level and ambient light.** SMPTE RP 431-2 s6.1: ambient on the screen with the projector off below 0.01 cd/m² (Review Room) or 0.03 cd/m² (Exhibition Theater) [91]; a hall will not come close. One measured example (search-result only): a screen's contrast with room lights on was 57:1 on a 1.0-gain screen and 194:1 on a dark optical screen, against over 8000:1 projector contrast with lights off [49]. Rule: no story-critical information below about 10% signal level unless the venue test (D5 item 5) passes.
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

**Maker review time (J, to time on the slice).** Estimated maker minutes per shot, by shot class (A to D, as used in `production-scale.md`). Only items that apply to the class count.

| Maker item | A: photo move (about 60% of shots) | B: designed graphic (about 25%) | C: hero composite (about 10%) | D: title or caption |
|---|---|---|---|---|
| A3 blind line-up, two sittings 48 hours apart | 0 (L3 and L4b only) | 0 | 10 per L3 or L4b face shot | 0 |
| A4 eyes and mouth at 100% | 0 | 0 | 1 | 0 |
| AI1 tell sweep at 5 frames per second | 2 | 1 on moving graphics | 2 | 0 |
| AI3 hands, text and reflections | 1 where visible | 1 where text | 1 | 1 where text |
| FN2 finish-off test | 1 | 1 | 1 | 1 |
| FN4 cut-out edges at 200% | 0 | 0 | 2 | 0 |
| FN5 light wrap | 0 | 0 | 1 where used | 0 |
| C7 light direction | 0 | 0 | 1 | 0 |
| **Typical shot, excluding A3** | **about 3 to 4** | **about 2 to 3** | **about 9** | **about 1 to 2** |

**Minimum set for class A.** Every Crit item that applies to the shot, plus B1, B8, C1 and FN1. MO9 and FN3 are checked once per chapter, not per shot.

**Per finished minute (J).** Weighting the typical minutes by the class mix (A 60%, B 25%, C 10%, D about 5%) gives about 3.7 maker minutes per shot before A3. At about 12 shots per finished minute (about 120 shots per 10 minutes, `playbooks/agent-pipeline.md`), that is about 45 maker minutes per finished minute, plus 10 for each L3 or L4b face shot. The total goes to `production-scale` as a delta.

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
| MO1 | No default ease, no undeclared linear (spec) | Spec lint on every move: no framework default ease (`power1.out` for GSAP, `ease` for CSS); no `linear` ease unless the brief declares `drift: declared` | True | Crit | Agent | G2 |
| MO1b | Push and pull, pixels | Level 2 estimator on pushes and pulls only: CV over 0.12, unless `drift: declared`. Pan, tilt, orbit and multi-plane moves report `unknown`, never `pass` | True, or `unknown` for uncovered moves | Maj | Agent | G2 |
| MO2 | Ease class declared and measured | Measured class equals brief `ease_family` | True | Maj | Agent | G2 |
| MO3 | Settle | Velocity in the last 15% of the move decays monotonically to 5% of peak or less in the spec (10% or less in the pixel audit) | True | Maj | Agent | G2 |
| MO4 | Hold after payoff | Velocity at 0 in the spec (under 10% of peak in the pixel audit) for at least 18 frames after the payoff, 24 frames after a face reveal | True | Maj | Agent | G2 |
| MO5 | Twos and ones | Drawn layers show alternating zero steps (twos); camera and type show none (ones) | True | Min | Agent | G2 |
| MO6 | Pan speed | Pixel audit: `python3 -I research/cinematic-quality-fixtures/pan_estimator.py clip.mp4 24` on the delivered 1080p file (M-C9: 22 of 22 verdicts right away from the limit; error at most 0.018 px per frame on constant pans). Fastest textured layer at most 11.4 px per frame at 1920 wide (0.143 frame widths per second): PASS at the limit plus 0.3 px per frame or less; INCONCLUSIVE on flat or fading frames; borderline within 0.5 px. Unless blurred or a declared whip stays a human call, because the estimator measures content shift, not blur. Vertical pans use `vy` against frame height | True | Maj | Agent | G2 |
| MO7 | Motion blur | Any layer above 4 px per frame has sub-frame blur at 180 degrees | True | Maj | Agent | G2 |
| MO8 | Sub-pixel smoothness | Velocity roughness (std of residual from a 9-frame mean, relative to mean speed; `zoom_velocity_classifier.py` with `ZV_SIZE` set) | Roughness no more than 1.3 times a Pillow sub-pixel reference render of the same move (`zoom_velocity_classifier.py`, `ZV_SIZE=1920x1080`) **and** centre jitter at most 0.05 px at 1080p on the delivered file (MO8a, `analyse()` in `zoompan_vs_subpixel_prints.py`; edge jitter at most 0.04 px as MO8b decides ties). No absolute roughness threshold: the floor read 0.13, 0.19, 0.076 and 0.064 on four synthetic stills and 0.03 to 0.08 on three real prints (M: zoompan 1.7 to 2.7 times the sub-pixel reference on two synthetic stills; Pillow 0.19, zoompan 0.33 on the 2026-10-18 reproduction) | Maj | Agent | G2 |
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
| TY1 | Legibility, type we set | Titles, cards, date lines, captions and credits: font at least 5% of picture height; x-height at least 2.5%; strokes at least 2 px. Applies to type we set; text inside photographs and her handwriting is exempt; below 2% x-height text is decorative and must not carry information. Captions follow `format.md` Step 8 (7 to 8% line height); TY1 is a floor, not a caption size | True | Crit | Agent | G2 |
| TY2 | Hold | Card held at least 36 frames once fully legible; caption within reading-speed limits from [format] | True | Maj | Agent | G2 |
| TY3 | Licence | Font, texture and plate have licence files | True | Crit | Agent | G1/G2 |
| TY4 | Text in photographs | Any text inside a photograph that the audience must read (sign, letter, label, her handwriting) is repeated on a card or caption | True where the text carries information | Min | Maker | G2 |
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
  licence: "video titling is a listed OFL permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video [56]; commercial fonts need their EULA read for film titling and public exhibition"
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
| 1 | Small type | Type ladder read from the back row | All lines marked "carries information" readable; font 5%+ of height, x-height 2.5%+ at 5 screen heights. Captions: x-height 3.1%+ of picture height at 6 screen heights (J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans | [47] with derivation above |
| 2 | Text near the edge | Safe-area overlay | Inside 5% margins; faces not clipped | [45] |
| 3 | Fast pans | Pan test | No visible strobe at 0.143 frame widths per second; any faster needs blur or a declared whip | [41] |
| 4 | Crushed shadows | PLUGE and 21-step ramp with lights as for the event. Count the RP 431-2 dark steps you cannot tell from black with the event lights on: 0.5 lux hides steps 1 to 3, 2 lux hides 1 to 5, 5 lux hides 1 to 8 (M, FQ5) | First two steps above black distinguishable from black (J); story-critical detail above 10% signal | [39][33][91] |
| 5 | Brightness | Lumens and screen area, or a meter | About 45 nits or more at the screen centre for a cinema-like feel; below 30 nits, lift the grade using the venue's measured shadow compensation (J). Reference white: 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2), ST 431-1 Table 1 [92]; gamma 2.6 ±5% in a theatre [91] | [91][92][33], lumen formula above; [35] superseded for these figures |
| 6 | Gamma/colour | Skin-tone stills side by side with the laptop; reference gamma from the playback path | Faces not orange or grey; shadows not milky; decision recorded | [33][37] |
| 7 | Banding | Dark-gradient frame, full screen | No visible steps in a dark gradient at normal seat distance | (M) 26 vs 100 levels; [44] |
| 8 | Aliasing and thin lines | Line ladder | 2 px lines stable; 1 px red line visibly weaker (expected) | (M) |
| 9 | Grain vs compression | 30 s film sample at the venue's actual file/DCP | Grain visible but not smeared; no mosquito noise around type | [42][34] |
| 10 | Judder | Pan test at 24 fps through the venue chain | Even cadence | [41] |
| 11 | Resolution scaling | 1-px checker pattern | No moire from the projector's scaler; text sharp | [34] |
| 12 | Picture modes | Menu inspection | Motion smoothing, sharpening, noise reduction and dynamic contrast off; overscan off | [38] |
| 13 | Speech intelligibility | Number passage read-back at the back row; STI if a meter is available | STI 0.60 or higher; read-back correct | [48] |
| 14 | Captions | Back-row read | Readable without leaning. Caption x-height 3.1%+ of picture height at 6 screen heights (J; see item 1). Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font | [47] |
| 15 | Faces in group photos | Back-row identification of the featured person | Featured person's head at least 8% of picture height, or a move that brings it there (J) | J |

### D6. Strangers-to-her test-screening protocol

**Purpose.** Find problems the maker cannot see and check that the public room reads the film. Strangers cannot judge truth or likeness. The maker keeps a veto on facts about her. The maker's line-up (Q3) asks two different questions: public-domain stand-in decoys test likeness, and her-at-other-ages decoys test age discrimination. Strangers answer a third question, whether the 6-, 25- and 55-year-old read as one person (Q3).

**Timing (decision needed).** [P4] sets picture lock at Sat 2027-02-06. The brief's week 17 is Sun 2027-02-07 to Sat 2027-02-13. A screening then can drive only sound, grade, titles, captions and trims of about 2%. Recommend two sessions: **S1** with 3 strangers on the slice chapter in the slice-review week (about 2026-12-20, when changes are cheapest), and **S2** with 3 to 5 strangers on the locked cut in week 17. If the maker prefers one session, move picture lock to Sat 2027-02-13. The stranger count is 3 (S1) and 3 to 5 (S2); the written sheet below (questions A to H) is the instrument for both. If the maker declines strangers, the fallback is a cold self-read, and then the Fable advisor's rubric pass is mandatory in that slot. production-scale.md (Decision 8) still says two or three; see the Deltas table.

**Recruitment without revealing who she is.**

- Who: adults, 3 to 5, who have never met her and will not meet her, are not in her social circle, and do not share close acquaintances with the family. At least one should be film-literate (a local film club or animation student), because the others will be too kind.
- Pretext (truthful and partial): "I'm finishing a short animated film about one woman's life that will be shown at a gathering. I need people who don't know her to watch it and tell me where it fails. It takes about 90 minutes. Please don't share anything about it before it's shown." Do not say whose life; do not say it is a surprise.
- Privacy: show on the maker's own laptop or a borrowed projector in a neutral place; no copy leaves the room; phones away; no recording of video. Consider showing a **redacted cut**: surname, street names and phone numbers blurred or bleeped; everything else unchanged. State openly that details have been hidden. If redaction hurts specificity too much, choose strangers in a different city.
- Dignity: show only what is cleared for the public cut. Hard chapters default OUT [P4]; the strangers see the film as the public will.
- Thank-you, not payment (cost UNVERIFIED, J: a meal or $10 to $20 each).
- Written consent to view and to the privacy request, one page, kept offline.

**Sequence (about 90 minutes).**

1. Room: lights as at the event, sound levelled before the audience sees it (the source does it after the makers' own first viewing) [70], slates over missing parts [70].
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
| `ai-imagery.md` Step 8, pure 2D push-in command | `zoompan` is 4 to 20 times rougher than sub-pixel resampling on real prints (FQ2; 1.8 times worse from a 1080p source than from 4K, and pre-upscaling does not fix it), and 1.7 to 2.7 times on synthetic stills (M). Its centre jitter on real prints is 0.13 to 0.59 px against the MO8a limit of 0.05 px. The MO8 pass is the pixel rule with no absolute roughness threshold (review round 2). Keep for proofs; use a Pillow or Blender sub-pixel render for finals |
| `ai-imagery.md` Step 9 line-up test and Step 11 "ask a relative who knew her" | Replace with the maker-alone blind line-up (Q3) plus the strangers' continuity question (D6 written question E). No relative sees drafts |
| `ai-imagery.md` Step 8 generated image-to-video | Tighten: no deliberate face regeneration or animation in the public cut; whole-frame image-to-video on a face-bearing photo only if A3 passes (5 of 5, twice, 48 hours apart); no eyes, blinks or mouth movement ever |
| `agent-pipeline.md` Step 6 baked grain, "8-frame loop on twos" | Use at least 48 distinct frames with seeded offsets; add the autocorrelation check (FN7) to the validators |
| `agent-pipeline.md` G2 and G4 | Add D1 sections and the MO9 chapter-variety rule with the ease estimator as an audit; add the stacked-finish count; add the swap test to G1 |
| `agent-pipeline.md` Decision 11 and G5 "trusted relative" proxy | Maker is the proxy with the 72-hour rule and advisor flagging [P4]; G5 is the maker plus advisor |
| `animated.md` Decision 9 | Same as above |
| `reviews/02` week 17 | Resolve the picture-lock clash (two sessions, or lock on 2027-02-13) |
| `agent-pipeline.md` G6 TV check | Record the TV picture mode (Filmmaker Mode or equivalent) [38] |
| `ai-imagery.md` principle 7, Step 8 and Decision 4 (faces of the dead) | BANNED by default in the public cut. Under the sole keeper nobody can be asked before the premiere, so environment and parallax motion only; revisit after the reveal with written consent from next of kin. [P2] Decision 4 says to leave them alone unless the family has said yes first |
| `production-scale.md` (maker review time) | About 45 maker minutes per finished minute before A3 (J): 3.7 minutes a shot by class mix, times about 12 shots a minute. Add 10 minutes per L3 or L4b face shot. See the D1 preamble |
| `format.md` line 77 (and line 674, which the round-1 list also gives; TODO(research): format.md has 451 lines, so locate the second caption-size line) | Caption size: at 1080p, `FontSize=23` is the caption size, with line pitch 7.96% (M-C8). x-height at 1080p is 2.7 to 3.3% / 3.2 to 3.8% / 3.5 to 4.3% at `FontSize=20/23/26` across five fonts. Caption x-height floor 3.1% (6 screen heights, J): `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font. Applied to the playbook (step 12, T1 TY1, T6) and the skill (step 10) in review round 2 |
| `production-scale.md` Decision 8 and T3 | The stranger count is 3 (S1, slice chapter, about 2026-12-20) and 3 to 5 (S2, locked cut, week 17), not "two or three". The written sheet (T7 questions A to H) replaces the three-question read. The cold self-read is the fallback only if the maker declines strangers, and then the Fable advisor's rubric pass is mandatory in that slot. Decision 8 already holds the W9 and W17 slots, so no new date is needed. Applied to the playbook T7 and Decision 4 in review round 2 |
| This track: research D1 and D5, playbook T1 and T6, skill steps 7 and 10 (round-1 items 3, 4 and 6, dark-step part) | MO6 is a pixel audit (`pan_estimator.py`; pan speed validated, pan ease not; M-C9). MO8 is the pixel rule with no absolute threshold. Projection figures cite RP 431-2, ST 431-1 and ST 428-1, with [35] superseded. D5 item 4 gets the dark-step count. Captions carry the 3.1% floor. Applied in review round 2 (2026-10-18): MO6, MO8, projection figures, dark-step count, caption floor, and the pan clip on the playbook T6 card. Not yet applied (TODO): the RP 431-2 Table A.2 and A.3 grey scales and the pan clip on the research D5 test card |
| `theatrical-delivery.md` rights log, `fonts` sheet (round-1 item 5) | Add "subscription renewal date" and "dates the film is shown" columns. Rule (FQ13): a commercial font is used only while its subscription is in force on every showing date. OFL fonts need nothing for rendered text, and a font file shipped with the film needs `OFL.txt` beside it (FQ4). Monotype Create + Pitch: the video grant is for pitching only, with no public deployment. Monotype Create + Deploy: names Video Content and grants up to 5,000 Units of Video Content a year, with no clause on output after the term (FQ4, FQ13). Commercial fonts need a written yes naming the film and public screening |
| `surprise-ops.md` "ask the venue" step (round-1 item 6) | No step with that label exists in the file (TODO(research): locate or create it). Add the six venue questions (FQ7) and the scenario table there; every brightness figure carries "scenario until answered". The six questions are in playbook step 1 |
| `theatrical-delivery.md` T9 form 4g and the per-shot "dead person" flag in `timeline.json` (round-1 item 7) | Keep the rule: no animation of the dead in the public cut. Add the second-relative rule to form 4g (FQ6). Add a separable flag per shot in the timeline, so a later "no" costs a re-render, not a re-edit |
| Research D5 item 13 and playbook T6 item 13 (round-1 item 8, FQ8) | Not applied in review round 2 (TODO). Replace "STI if a meter is available" with the three routes, and the 100-word read-back with its pass rule, marked UNVERIFIED against a meter |

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
| OFL fonts | Titles and captions | Free; video titling is a listed OFL permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video [56] | Check each font's licence file; commercial fonts need their EULA read for film titling and public exhibition |
| Generative image/video (Veo, Kling, Runway, Seedance, FLUX, Qwen) | Optional non-face inserts, stylisation of non-face material | Prices in [P2] dated 2026-10-18 (Veo 3.1 $0.25 to $2.00 per 5 s clip at 720p) | Tool volatility: a vendor shutdown was reported in May 2026 [11] |
| Colorimeter or lux meter | Optional venue check | Price UNVERIFIED | A phone lux app is a rough substitute (accuracy UNVERIFIED) |
| Test-screening costs | Meals or small thanks | $0 to $100 total (J) | Neutral venue assumed |
| Maker review time (estimate, J) | Maker items in D1: A3, A4, AI1, AI3, FN2, FN4, FN5, C7 | $0 (the maker's own time) | Minutes per shot by class are in the D1 preamble; the per-finished-minute total goes to `production-scale` as a delta |

---

## Risks, pitfalls and ethics (with mitigations)

1. **Treating laurels as proof.** Vendor-run festivals reward novelty [1][2]; official prize lists can disagree with social posts [7]. Mitigation: calibrate on the non-AI films and on our own projection test; use laurels only to find process interviews.
2. **Studio-scale practice transplanted.** No daily reviews with twenty people; no colour-script department. Each ritual above has a one-person version.
3. **Detecting only what is easy.** My motion test was validated on synthetic pushes at 540p; it cannot see overshoots or tails below about 10% of peak, pan speed is validated (M-C9) and pan ease is not, and grain raises the noise floor. Mitigation: run on pre-finish renders; keep the maker's blind A/B as the final word.
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
3. **SMPTE RP 431-2, ST 431-1 and ST 428-1 read in full (FQ5, 2026-10-18).** Their figures are used in Q2, Q10, D5 and the playbook [91][92][93]; the DCI compliance test plan [35] is superseded for these figures.
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
- [24] Yes, one animator made the CG animated feature Away on his own (Cartoon Brew) — https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html — 2019-06-06 — solo workflow, shortcuts; the article says Away was worked 'seven days a week'.
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
- [35] DCSS Compliance Test Plan 1.4.1 (DCI) — https://documents.dcimovies.com/CTP/release/1.4.1/ — ambient under 0.01 cd/m² fetched; "48.0 ± 3.5 cd/m²" white seen in search-result text only. Superseded for these figures by [91][92][93] (review round 2, 2026-10-18).
- [36] Poynton notes on BT.1886 — https://poynton.ca/notes/misc/flummoxed.html — search-result only (page 404 on fetch); reference conditions.
- [37] DCP-o-matic user mailing list, colour conversion threads — https://lists.dcpomatic.com/hyperkitty/list/users@lists.dcpomatic.com/message/27TBTWCAFUWRT73LEI2VANYMJOQWDXWL — search-result only; practitioner opinion.
- [38] Filmmaker Mode feature summaries (Tom's Guide and others) — https://tomsguide.com/features/what-is-filmmaker-mode-heres-why-you-should-use-this-picture-perfect-setting — search-result only; launch-era (2019 to 2020) descriptions.
- [39] Black Level (PLUGE) test (TestUFO) — https://www.testufo.com/blacklevels — fetched 2026-10-18 — how to read a PLUGE.
- [40] Delta-E CIEDE2000 documentation (MetricGate) — https://metricgate.com/docs/delta-e-ciede2000/ — fetched 2026-10-18 — interpretation bands for flat patches.
- [41] Camera panning speed (RED) — https://www.reddigitalcinema.com/red-101/camera-panning-speed — undated, copyright 2004 to 2026 — seven-second rule, shutter angle.
- [42] Film Grain Synthesis for AV1 Video Codec (Norkin and Birkbeck, Netflix/Google) — https://norkin.org/pdf/DCC_2018_AV1_film_grain.pdf — 2018 — grain statistics and compression difficulty; read locally.
- [43] Netflix film grain synthesis saves on the bitrate (Broadband TV News) — https://www.broadbandtvnews.com/2025/07/04/netflix-film-grain-synthesis-saves-on-the-bitrate/ — 2025-07-04 — search-result only (307).
- [44] Banding in gradients (Fora Soft) — https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps — fetched 2026-10-18 — causes, CAMBI, dither advice.
- [45] EBU R 95: Safe areas for 16:9 television production — https://tech.ebu.ch/docs/r/r095.pdf — June 2017, Ver. 1.1 (2016 errata) — action 3.5%, graphics 5%; read locally.
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
- [56] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — fetched 2026-10-18 — video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video; commercial fonts need their EULA read for film titling and public exhibition.
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
- [76] My measurements, 2026-10-18, cloud container, synthetic material only. M-C1 zoom-velocity classifier (least-squares zoom per frame pair; 4 s, 24 fps, 960x540 push-ins; six clips); M-C2 flicker index from `signalstats` YAVG (static 0.000, injected 2.58 levels); M-C3 grain-loop autocorrelation (8-frame loop on twos, r = 1.00 at lag 16); M-C4 dark-ramp banding (26 vs 100 levels, 8-bit vs 10-bit H.264); M-C5 grain bit cost at CRF 18 (7.8 KB to 356 KB); M-C6 thin-line survival (1920x1080, H.264 4:2:0, CRF 18); M-C7 `zoompan` vs sub-pixel roughness (0.35 vs 0.13 slow 1080p; 0.26 vs 0.08 faster 540p), reported as 1.7 to 2.7 times rougher on two synthetic stills (advisor reproduction 2026-10-18: Pillow 0.19, zoompan 0.33); the roughness function is in `zoom_velocity_classifier.py` (set `ZV_SIZE`). The scripts are kept in research/cinematic-quality-fixtures/ with a README; media files were deleted after use; the shared disk reached 100% during the session for reasons outside this task.
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


---

## Follow-up research (round 1)

Sunday 2026-10-18 · Sonnet researcher · eight targeted follow-up questions on the `cinematic-quality` track. Labels as at the top of this note: **(M)** my measurement in the cloud container (new ones are M-C7b, M-C8 and M-C9, described in source [108]), **(J)** my judgment, **UNVERIFIED**. New sources are numbered [86] onward in the list at the end of this section; [P6] to [P8] are project files.

**Context from the maker (relayed this session).** "For now only me and I will be the only one on this project." No relative is in on the surprise and none can approve a hard chapter in advance; the maker is the proxy, with the Fable advisor flagging sensitive material. Where this section talks about relatives (FQ6) it means asking them after the reveal.

**Limits of this round.** The web-search budget for the run was used up before FQ4 to FQ8, so those answers rest on pages I fetched by address (the fetch tool refuses most news sites, and some publishers' edge servers return "Access Denied"). Each such gap is named in the answer. Nothing here was viewed on a screen or heard in a room.

### Summary of round 1

1. **FQ1, caption and type size.** At 1080p, ffmpeg `.srt` `FontSize=20/23/26` gives x-height 2.7 to 3.3% / 3.2 to 3.8% / 3.5 to 4.3% of picture height across five fonts (line pitch 6.94 / 7.96 / 9.07%). One shared number: x-height 3.5% (about 38 px) at `FontSize=23`. TY1's floor of 2.5% is cleared by all three sizes; a 3.1% caption floor (6 screen heights) is cleared by `FontSize=23` in every font tested. (M-C8)
2. **FQ2, M-C7 on real prints.** `zoompan` is about 4 to 20 times rougher than a sub-pixel resample on three public-domain scans (typically 5 to 10 times against the old reference), about 1.8 times worse from native 1080p than from 4K, and pre-upscaling halves the error without removing it. Its pixel jitter is the same on every print. MO8 is rebuilt on pixels: centre jitter at most 0.05 px, edge jitter at most 0.04 px. (M-C7b)
3. **FQ3, MO6 pixel audit.** A phase-correlation pan estimator reads constant-speed pans to within 0.018 px per frame and gets 22 of 22 verdicts right away from the limit; the six synthetic clips exactly at 0.1429 all read 11.35 to 11.57 against 11.43, and two integer-step pans at the limit read 11.60 and 11.80, flagged borderline. (M-C9)
4. **FQ4, fonts.** OFL FAQ 1.1, 1.11 to 1.13 read: video titling needs no permission; a font file shipped with the film needs `OFL.txt` beside it. Monotype's Create + Deploy names Video Content and counts views (5,000 a year); Create + Pitch excludes public screenings; Enterprise never mentions video. Adobe Fonts' terms could not be read (UNVERIFIED).
5. **FQ5, SMPTE.** Read from the documents: 48 cd/m2 is in ST 431-1, with +/- 3.5 for a Review room and **+/- 10.2 for a Theater**; ambient is 0.01 (Review) or **0.03 cd/m2 (Theater)**; gamma 2.6 +/- 5% in a theatre; ST 428-1 encodes 12-bit with a 52.37 cd/m2 normaliser. Two earlier figures corrected.
6. **FQ6, the dead.** No independent first-hand family account of an objection found (access-limited); reactions that exist are strong and mixed. Post-premiere written next-of-kin consent is realistic for stills and recordings in a small reachable family, not as cover for the premiere, and not a legal gate I can confirm.
7. **FQ7, the maker's venue answers.** Six questions, a scenario table and the arithmetic of what ambient light hides (2 lux hides everything below 19% signal). OPEN until the maker answers.
8. **FQ8, speech intelligibility.** Three routes: an iOS STIPA app ($49.99, vendor-claimed compliance), Room EQ Wizard's indirect STI, or a 100-word read-back scored against the IEC bands (90 or more words right at the back row passes; under 80 fails). None checked against a meter.

### FQ1. x-height of `FontSize=20/23/26` at 1080p, so TY1 and the caption rule share one number

**Answer.** On a 1080p frame, ffmpeg's `subtitles` filter on an `.srt` gives these figures. One number to share: **x-height 3.5% of picture height (about 38 px) at `FontSize=23`, with a range of 3.2% to 3.8% across five fonts.** (M-C8)

| `FontSize` | Line pitch (% of height) | x-height, 5 fonts (% of height) | Cap height (%) | Em size (%) |
|---|---|---|---|---|
| 20 | 6.94 | 2.72 to 3.28 | 3.65 to 4.38 | 5.7 to 6.2 |
| 23 | 7.96 (FreeSans 8.06) | 3.17 to 3.81 | 4.26 to 5.00 | 6.5 to 7.2 |
| 26 | 9.07 (Inter 8.98) | 3.54 to 4.26 | 4.75 to 5.67 | 7.4 to 8.1 |

Per font at 1080p (x-height % at `FontSize` 20 / 23 / 26): Liberation Sans (Arial metrics) 3.28 / 3.81 / 4.26; DejaVu Sans 3.27 / 3.80 / 4.26; Inter 3.18 / 3.64 / 4.09; FreeSans 3.06 / 3.52 / 3.93; Carlito (Calibri metrics) 2.72 / 3.17 / 3.54. Font px at 1080p for `FontSize=23`: x-height 34 to 41 px.

- **How I measured it (M-C8).** ffmpeg 6.1.1 with libass; a one-cue `.srt` rendered on a black 1920x1080 frame and again on a 3840x2160 frame, `force_style='FontName=...,FontSize=N,Outline=0,Shadow=0,PrimaryColour=&HFFFFFF&'`. I measured the vertical extent of white pixels for `xxxxxxxxxxxxxxxx` (x-height), `HHHHHHHHHHHH` (cap height) and the top-to-top pitch of a two-line `HHHHHHHH` block (line pitch), counting partly covered edge rows. The 1080p and 2160p percentages agree within 0.05 points (the first run of the script had a 2 px edge error that showed up as a 0.1 point mismatch between the two sizes; fixed, and the script is in the fixtures folder).
- **The formula, checked.** x-height % of picture height = 100 x `FontSize` / `PlayResY` x xHeight / (ascender + descender), with `PlayResY` = 288 for `.srt` through ffmpeg (the 288-line canvas that `format.md` found) and the font's own `hhea` metrics (identical to the OS/2 win metrics in all five fonts). It predicts the measured x-height of every font and size within 0.05 points. For an `.ass` file the same formula holds with that file's `PlayResY`: DejaVu Sans, `PlayResY: 1080`, `FontSize: 75` measured 3.27%, the same as `.srt` `FontSize=20`.
- **Line pitch matches `format.md`.** 6.94%, 7.96% and 9.07% (75, 86 and 98 px) are the same figures `format.md` measured with DejaVu Sans [P6]. So the BBC line-height rule and the TY1 x-height rule are two views of one setting.
- **Against TY1.** TY1 asks for font size at least 5% of height and x-height at least 2.5% (derived in Q10 for a back row at 5 screen heights) [47]. All three sizes clear both floors in all five fonts (lowest: Carlito at `FontSize=20`, x-height 2.72%, em 5.69%). The smallest `FontSize` that reaches x-height 2.5% is 15.2 (Liberation) to 18.4 (Carlito). At 6 screen heights Q10 needs 3.1%: that takes `FontSize` 18.9 (Liberation) to 22.8 (Carlito); `FontSize=23` clears it in every font tested, `FontSize=20` does not for Carlito (2.72%) or FreeSans (3.06%).
- **Proposed shared rule (J).** Captions: x-height at least 3.1% of picture height, measured on a rendered frame; `FontSize=23` gives 3.2% to 3.8% in the fonts tested. Titles and other must-read text keep the TY1 floor of 2.5%. Target 3.5%. Both are scenario numbers until the maker gives the farthest seat distance (FQ7).
- **Limits.** Only the five fonts on this machine were measured, not the maker's chosen font. libass hinting and font fallback differ between ffmpeg builds, so run `caption_xheight.py` once on the maker's Windows ffmpeg and caption font. A font with a larger x-height than Arial (Verdana, for example) will measure larger at the same `FontSize`. UNVERIFIED: the Windows build's numbers.

### FQ2. M-C7 on three scanned prints: `zoompan` against sub-pixel resampling, from 4K and from native 1080p, and MO8

**Answer.** On three public-domain scanned prints, ffmpeg `zoompan` is **about 4 to 20 times rougher than a sub-pixel resample** (typically 5 to 10 times against the M-C7 reference), against the 2.7 times from the synthetic texture in M-C7. Starting from a native 1080p source makes `zoompan` about 1.8 times worse than starting from a 4K source. Pre-upscaling the input 2x or 4x halves the error and does not remove it. The error is a fixed property of the filter, not of the picture: **its jitter in pixels is the same on all three prints to three decimals.** The old MO8 test (relative roughness at most 0.15) cannot be kept as written, because relative roughness falls as the push gets faster while the pixel error does not. **New MO8: rms jitter of the zoom centre at most 0.05 px, and edge-equivalent zoom jitter at most 0.04 px, at 1080p, measured on the delivered file.** (M-C7b, 2026-10-18)

**The three prints** (public domain or CC0; all archival, used only for measurement; sources in `prepare_prints.py`) [106][107]:

| Print | What it is | Native pixels in the 16:9 crop | Character |
|---|---|---|---|
| P1 faded colour | Library of Congress photochrom print, "South of India. Women Grinding and Children", about 1890 to 1910, 21 x 27 cm; LoC states "No known restrictions on publication" | 6400 x 3600 (real 4K detail) | Pastel, mean saturation 0.40, luminance spread 0.20, sharpest of the three (Laplacian variance 378) |
| P2 small black-and-white | Smithsonian NMAAHC albumen print on a card mount, "Photograph of A. J. Wiseman", about 1895, 11.1 x 8.6 cm; Open Access CC0 | 2080 x 1170 (the 4K file is a 1.8x up-sample) | Faded sepia, luminance 1st to 99th percentile only 133 to 180, Laplacian variance 51 |
| P3 soft group | Smithsonian NMAAHC albumen print, "Colored Troops at Ft. Douglas", 1896 to 1899, 9.5 x 11.8 cm; CC0 | 2510 x 1412 (a 1.5x up-sample) | Out-of-focus group and foreground chain, Laplacian variance 45 |

A true faded colour family print (a 1970s or 1980s chromogenic print with dye fade) was not available as public domain here. The photochrom is a pastel lithographic colour print, not a dye-faded one, so P1 stands in for "colour print with low saturation"; P2 carries the "faded" tonal range. I did not synthesise any fading. 4K and 1080p versions of each print were cut from the same crop (Lanczos).

**Method.** A 4% push-in, cosine in-out, 96 frames at 24 fps, output 1920x1080, as in M-C7. Methods: Pillow `transform(EXTENT, BICUBIC)` (the M-C7 reference), Pillow `resize(box=...)` with Lanczos (a better reference: float box, antialiased), ffmpeg `zoompan` directly, and `zoompan` after a `scale=...:flags=lanczos` of 2x (and 4x for the 1080p source), so the 4K source goes to an 8K intermediate and the 1080p source to 4K or 8K. 27 clips, each encoded H.264 CRF 14 yuv420p and measured both before and after the codec. Estimators: (a) the M-C7 estimator, rebuilt from the saved description (zoom-only least squares at 240x135 on the encoded file; it is not in the saved scripts, so this is my reconstruction) and (b) a new three-parameter fit (zoom plus x and y translation, Lucas-Kanade on a blurred 480x270 frame, so it also reports sub-pixel position jitter). Roughness = standard deviation of the zoom rate minus its 9-frame running mean, divided by the mean zoom rate (as MO8). Centre jitter = the same residual for the x and y translation, combined, in 1080p pixels. Edge jitter = the zoom-rate residual times half the frame width (960 px), the same error seen at the picture edge.

**Results** (range over the three prints; the 10% rows are below):

| Method | Source | Roughness, new estimator, H.264 | Roughness, M-C7 estimator, H.264 | Centre jitter, px | Edge jitter, px |
|---|---|---|---|---|---|
| Pillow `resize(box)`, Lanczos | 4K | 0.035 to 0.056 | 0.032 to 0.062 | 0.000 to 0.001 | 0.009 |
| Pillow `resize(box)`, Lanczos | 1080p | 0.034 to 0.057 | 0.032 to 0.060 | 0.001 to 0.004 | 0.010 to 0.012 |
| Pillow `transform` EXTENT | 4K | 0.038 to 0.060 | 0.037 to 0.060 | 0.003 to 0.008 | 0.013 to 0.016 |
| Pillow `transform` EXTENT | 1080p | 0.047 to 0.076 | 0.049 to 0.085 | 0.004 to 0.019 | 0.018 to 0.035 |
| `zoompan` direct | 4K | 0.247 to 0.272 | 0.274 to 0.484 | 0.292 to 0.295 | 0.112 to 0.117 |
| `zoompan` direct | 1080p | 0.448 to 0.507 | 0.519 to 1.071 | 0.589 to 0.592 | 0.202 to 0.224 |
| `zoompan`, 2x pre-upscale | 4K | 0.124 to 0.128 | 0.144 to 0.254 | 0.145 | 0.051 to 0.054 |
| `zoompan`, 2x pre-upscale | 1080p | 0.248 to 0.269 | 0.273 to 0.483 | 0.292 to 0.294 | 0.112 to 0.117 |
| `zoompan`, 4x pre-upscale | 1080p | 0.124 to 0.135 | 0.144 to 0.257 | 0.145 | 0.051 to 0.054 |

(Centre and edge jitter are measured before the codec. H.264 changes them by up to 0.012 px (centre) and 0.015 px (edge); after H.264 the Pillow centre jitter reads 0.004 to 0.015 px and `zoompan` 0.133 to 0.590 px.)

**Ratio range** (`zoompan` direct divided by the Pillow value, over 3 prints x 2 sources = 6 clips each):

| Reference | New estimator, H.264 | New estimator, before codec | M-C7 estimator, H.264 |
|---|---|---|---|
| Pillow `transform` EXTENT (the M-C7 reference) | 4.1 to 10.7 | 5.8 to 12.2 | 4.6 to 19.8 |
| Pillow `resize(box)` | 4.4 to 14.9 | 12.4 to 21.3 | 4.4 to 33.2 |

By source type, `zoompan` over EXTENT with the new estimator on H.264: 4.1 to 7.1 from 4K, 5.9 to 10.7 from native 1080p.

- **Why the old ratio was 2.7 and this one is larger.** The estimator's noise floor sets the roughness of a perfectly smooth push. On the synthetic plasma the Pillow floor was 0.08 to 0.13; on these prints the same kind of estimator reads 0.03 to 0.09, so the same `zoompan` error gives a larger ratio. The pixel jitter is the number that does not move: `zoompan`'s centre jitter was 0.292 to 0.295 px on all three prints from 4K and 0.589 to 0.592 px from 1080p. It tracks the intermediate size: about 0.59 px at 1,920 wide, 0.29 at 3,840, 0.145 at 7,680 (it halves each time the size doubles).
- **Content makes a small difference to roughness, none to jitter.** The faintest print (P2, luminance spread 133 to 180) reads highest on the Pillow references after the codec (0.056 to 0.076, against 0.034 to 0.070 for P1 and P3) because the estimator has less texture to work with.
- **Pre-upscaling is not a fix.** A 2x pre-upscale (to 8K from a 4K source) gives a centre jitter of 0.145 px, 7 to 30 times Pillow's 0.000 to 0.019. Reaching 0.05 px would need an intermediate about 22,000 px wide (extrapolated from the halving: UNVERIFIED, not run).
- **Relative roughness depends on speed, so it cannot be the only MO8 test.** I repeated a faster 10% push on all three prints (24 more clips, every method except the 4x pre-upscale; 51 clips in all). `zoompan` direct from 4K read 0.094 to 0.098 relative roughness (new estimator, H.264), already below the old limit of 0.15 and below the 0.10 I would otherwise have set, while its centre jitter was 0.31 px and its edge jitter 0.10 px, the same as at 4%. Native-1080p `zoompan` read 0.203 to 0.215; Pillow read 0.026 to 0.034. A relative test would pass a shimmering fast push from a 4K source.

**MO8 as revised (replaces the "roughness 0.15 or less" row).** *Status (review round 2, 2026-10-18): adopted (review round 2). The D1, T1 and SKILL MO8 pass is the pixel rule (MO8a and MO8b) together with roughness no more than 1.3 times a Pillow sub-pixel reference render of the same move, and no absolute roughness threshold.*

| ID | Check | Pass | Evidence |
|---|---|---|---|
| MO8a | Centre jitter: rms of the residual of the fitted x and y translation of a push or pull, in pixels at 1080p, on the delivered file | 0.05 px or less | Pillow family 0.000 to 0.019 (0.004 to 0.015 after H.264); `zoompan` 0.133 to 0.592 even with 2x to 4x pre-upscale; the limit sits near the geometric middle of the gap (0.019 to 0.133) |
| MO8b | Edge-equivalent zoom jitter: rms of the zoom-rate residual times 960, in pixels per frame | 0.04 px or less | Pillow family 0.009 to 0.035 over both pushes, before and after H.264; `zoompan` 0.051 to 0.230. The margin is narrower here, so MO8a decides ties |
| MO8c (informational) | Relative roughness at a 4% push over 4 s only | 0.10 or less (new estimator) | Pillow 0.034 to 0.076 after H.264; `zoompan` 0.124 to 0.507 |

Tools: `analyse()` in `zoompan_vs_subpixel_prints.py` returns `rough`, `tx_jit_px1080`, `ty_jit_px1080` and `edge_jit_px1080` for a set of frames. Thresholds are (J) set from the measured gap; **whether 0.1 to 0.3 px of random jitter is visible on a 6 to 10 m screen was not tested**, so add a 4-second A/B push (Pillow against `zoompan`) to the D5 test card and judge it on the venue screen. D4 item 24 stands: no `zoompan` for a final push, with or without pre-upscaling.

**Limits.** Three prints and one push profile; the two small prints are up-samples to 4K (as real family scans of small prints will be); I measured geometry and the H.264 encode, not a projector; the original M-C7 estimator is a reconstruction, so the first row of its column should be read as comparable, not identical, to the old 0.13 and 0.35.

### FQ3. A phase-correlation pan estimator, validated, so MO6 can move from spec-only to a pixel audit

**Answer.** `pan_estimator.py` (numpy only) measures the speed of the fastest textured layer in a clip and gives PASS, FAIL or INCONCLUSIVE against 0.143 frame widths per second. I validated it on 28 synthetic pans cut from the three scans at 0.10, 0.1429 (the limit), 0.20 and 0.30 frame widths per second, on 4 pans generated by ffmpeg's own `crop` filter, and on 5 control clips. **On 20 constant-speed clips the speed error was -0.003 px per frame on average and at most 0.018 px per frame (0.0002 frame widths per second); the verdict was right on all 22 clips that are not exactly at the limit; the six synthetic clips exactly at the limit all read 11.35 to 11.57 px per frame against the limit of 11.43, and two integer-step pans at the limit read 11.60 and 11.80, all of them flagged borderline.** MO6 can become a pixel audit. (M-C9)

**Speeds.** At 1920 wide and 24 fps: 0.10 is 8.00 px per frame, 0.1429 (1/7) is 11.43, 0.20 is 16.00, 0.30 is 24.00. Frame widths per second = px per frame x fps / width.

**How it works.**
- Luma frames, 3 x 3 grid of 640 x 360 tiles. Each tile pair gets a Tukey window, a normalised cross-power spectrum with a Gaussian band-limit (0.22 cycles per pixel), an inverse FFT for the integer peak, then an upsampled-DFT search over plus or minus 1 px at 0.05 px with a parabolic polish.
- Two peaks per tile, so a slow background does not hide a fast foreground: the second must be a true local maximum outside a 9 px exclusion zone and at least half the first. (My first version took the skirt of the first peak as a second peak and reported speeds 4 px off; fixed.)
- A peak counts when its peak-to-sidelobe ratio is at least 10 and the tile has texture. Calibration: independent noise tiles scored 4.5 to 5.9; real peaks scored 26 to 255 (so the gate has a wide margin).
- The speed for a frame pair is the fastest counted peak over all tiles. The clip's peak is the maximum of a 5-frame running mean, so an integer-rounded path of 11 and 12 px steps is judged on its average. The per-frame list is kept.
- Footage on twos is detected (every second frame difference is near zero) and then frames two apart are compared and halved.
- Verdict: PASS if the peak is at most the limit plus 0.3 px per frame (a 2.6% tolerance); FAIL above; INCONCLUSIVE if fewer than half the frame pairs have any confident textured tile (fades, flat frames); a `borderline` flag if the peak is within 0.5 px of the limit.

**Validation (28 synthetic clips, 40 frames each, 1:1 windows cut from the 4K scans; P1, P2 and P3 are the prints from FQ2).**

| Variant (prints) | 0.10 (truth 8.00) | 0.1429 (truth 11.43) | 0.20 (truth 16.00) | 0.30 (truth 24.00) |
|---|---|---|---|---|
| Clean, linear (P1, P2, P3) | 8.000, 7.999, 7.999 | 11.435, 11.470, 11.574 | 15.999, 15.997, 15.998 | 23.999, 23.995, 23.996 |
| Grain (sigma 2) + H.264 CRF 18 (P1) | 8.000 | 11.473 | 16.000 | 24.000 |
| On twos (P2), detected as twos in 4 of 4 | 7.999 | 11.453 | 15.997 | 23.996 |
| Cosine ease, peak of the move (P3) | 7.935 | 11.345 | 15.792 | 23.685 |
| Two layers: background 0.10, foreground blob at the speed shown (P1, P2) | not run | not run | 15.993, 15.999 | 23.992, 24.017 |

(Estimated peak speed in px per frame; verdicts: PASS at 0.10, FAIL at 0.20 and 0.30 in every row; PASS in all six clips at 0.1429. Footage on twos was flagged in every twos clip and in none of the 24 others.)
- **Error.** Constant-speed clips (20): mean error of the clip median -0.003, largest 0.018 px per frame; largest error of the peak 0.145 px per frame. Eased pans: the peak reads 0.07 to 0.31 px per frame low (up to 1.3%), because the 5-frame mean flattens a bell that is only 40 frames long; the shortfall shrinks on longer moves. Two-layer clips: the foreground speed is found within 0.017 px per frame while a slower layer fills the rest of the frame.
- **An independent generator.** ffmpeg's `crop` filter (integer positions) at the same four speeds (P3): 8.00 -> 7.999 PASS; 11.43 truth, steps alternating 11 and 12 px (`first_steps` in the file), peak 11.80, **FAIL**; 16.00 -> 15.998; 24.00 -> 23.996. Run through the command line on an H.264 file of the same kind of path (48 frames, a different start phase), the 11.43 case read 11.60 and PASSED. Both are flagged `borderline`: an integer-rounded path exactly at the limit lands on either side of the line depending on where the 11 and 12 px steps fall. That is a fair result (a 12 px step is over 11.43) and MO8's business too, because sub-pixel paths do not do this.
- **Controls.** Static texture: 0.000 px per frame, PASS. Flat grain only: INCONCLUSIVE (no speed invented). A pan of 8 px per frame fading to black: 7.999 and PASS, with 92% of frame pairs valid. A 10% push-in with no pan: 2.9 px per frame (the zoom shows as translation in the outer tiles; the true edge speed at the peak is about 3.9). A pan of 8 px per frame with a 5% push-in: 9.56 (8 plus the zoom's edge speed).

**Use in the gates (G2).**
- MO6 becomes: `pan_audit(luma_frames)` on the delivered 1080p file; PASS, or a declared exception for a whip pan or a blurred layer. The estimator measures content shift, so it cannot see motion blur: the "unless blurred" exemption stays a human call. It returns the signed vector, so for a vertical pan use `vy` and the frame height (the rule as written is for horizontal pans).
- Add to the D5 test card a pan clip at 0.10, 0.1429, 0.20 and 0.30 generated by the same code that makes the footage, and audit it before it is played at the venue: the estimator then checks the test card as well.
- Command line: `python3 -I pan_estimator.py clip.mp4 24` prints one JSON line (verdict, peak in px per frame and frame widths per second, per-pair speeds). I checked it end to end on two real H.264 files made by ffmpeg `crop` (CRF 20, 48 frames): 8 px per frame read 7.9996 (PASS), 16 px per frame read 15.9995 (FAIL).
- Cost: with the machine idle a 40-frame clip took about 12 s including making it, roughly 0.25 s per frame pair; a 10-second clip (240 pairs) is about a minute or two (J, extrapolated). It needs no GPU and runs on Windows with numpy, plus ffmpeg for the command line.

**Limits.** Rigid translation inside a tile is assumed; strong zoom, rotation and perspective lower the peaks and, as the push-in control shows, appear as speed at the edges. A fast object smaller than a tile (an 11% area) can be missed; the two-layer test used a blob of about 1040 x 760 px. Tested on prints cut at 1:1 (so sub-pixel shifts come from Lanczos resampling), not on hand-drawn layers or on a real family pan; the grain-plus-H.264 clip is one print. The 0.3 px tolerance and the PSR gate of 10 are (J) set from these runs. `moving_frac` and the per-frame list are returned for audit; nothing here has been viewed on a screen.

### FQ4. Fonts in a film shown in public: SIL OFL FAQ 1.12 to 1.13, and two commercial licences

**Answer in one line.** OFL fonts are safe for burned-in titles and captions in a film shown in public, with nothing to attach or credit. Commercial licences are not uniform: Monotype's Create + Deploy agreement names "Video Content" and caps it at 5,000 views a year, its Enterprise agreement never mentions video, and I could not read Adobe Fonts' terms at all (UNVERIFIED). Use OFL fonts for everything on screen, and get a written yes from the vendor before using a commercial font. Read 2026-10-18.

**SIL Open Font License (read in full from the raw page; FAQ version 1.1-update7, November 2023; site footer "Last updated on 12 January 2026") [86][87].**
- **FAQ 1.12 and 1.13, verbatim.** "So can I embed OFL fonts in my document? Yes, either in full or a subset. The restrictions regarding font modification and redistribution do not apply, as the font is not intended for use outside the document." "Does embedding alter the license of the document itself? No. Referencing or embedding an OFL font in any document does not change the license of the document itself. ... Similarly, creating any kind of graphic using a font under the OFL does not make the resulting artwork subject to the OFL."
- **The video case is named, in FAQ 1.1.** Permitted uses "for design work" include "video titling", and "No additional license or permission is required, unlike with some other licenses." FAQ 1.1.1: "You remain the author and copyright holder of that newly derived graphic or object." FAQ 1.1.2: no acknowledgement is required. FAQ 1.26 says AI-based design tools are fine "as long as the resulting work is not intended to be a font".
- **What counts as "embedding" (FAQ 1.11).** Inclusion "in a way that makes extraction (and redistribution) difficult or clearly discouraged". "Any other means of delivering a font to another person is considered 'distribution', and needs to be accompanied by any copyright notices and licensing information available in OFL.txt."
- **What the licence text asks (OFL 1.1).** Permission to "use, study, copy, merge, embed, modify, redistribute, and sell"; the font may not be sold by itself; each copy that is redistributed carries the copyright notice and licence; a modified font may not use the Reserved Font Name; the "requirement for fonts to remain under this license does not apply to any document created using the Font Software".
- **For this project.** (1) Burned-in titles and captions are pixels, so FAQ 1.1 applies: nothing to ship. (2) If a font file travels with the film (an MKV attachment, an `.ass` file with its font, or timed-text subtitles inside a DCP package), I read that as "distribution" unless extraction is clearly discouraged (1.11): keep `OFL.txt` and the copyright line beside it in the delivery folder (J, my reading). (3) Neither the FAQ nor the licence mentions film exhibition or public screening and neither limits it; I read that as no limit (J). The existing line in the playbook ("OFL fonts allow video titling and embedding") holds.

**Monotype Fonts (three service and licence agreements read in full from the publisher's own content feed, 2026-10-18; the texts carry no revision date, so I cannot say which version binds a given account) [88][89].**
- **Create + Deploy.** Defines "Video Content" as "Moving and/or dynamic visual content containing Production Font data and/or output generated through Use of the Production Fonts". The grant covers using the fonts "to create Static Materials, Video Content, Promotional Materials, Logos, and Internal Documents" and, under DEPLOY, to "Distribute up to five thousand (5,000), or such other amount as may be provided in your Account, Units of Video Content annually", where a Unit for Video Content is "each full or partial view and/or playback". One public screening is far below 5,000. The same agreement says "NO CLIENT WORK: The license grants provided in this agreement are personal in nature and not for external or client work", and every right runs "during the Term".
- **Create + Pitch.** Video content may go "to Clients ... solely for Pitching, Prototyping & Promoting; no license is granted to deploy or distribute such materials to the general public (or a subset thereof)". A public screening is outside it.
- **Enterprise ("Large brands").** No mention of video, film, motion, broadcast or exhibition. It grants the right to "create, edit, view, print and distribute materials, provided that ... if you distribute such materials, the materials do not contain the Font Software", and states "All rights not expressly granted in this Agreement are reserved to Monotype." A rendered film arguably counts as "materials", but nothing says so. Ask in writing.
- **Not checked.** What happens to a finished film if the subscription ends (no matching clause found with a keyword search; UNVERIFIED). Render and archive the master while the subscription is active.

**Adobe Fonts (UNVERIFIED).** The licensing FAQ (`helpx.adobe.com/fonts/using/font-licensing.html`) and Adobe's terms pages returned "Access Denied" (an Akamai edge block) to both `curl` and the fetch tool, so I could not read them; I did not try to get around the block. What I did see is the vendor's own summary on `fonts.adobe.com` (footer "(c) 2026 Adobe"): "Simplified licensing: The full Adobe Fonts library can be used for both personal and commercial projects", with "Video and Broadcast: Use fonts to create in-house or commercial video content", and "Visit the Adobe Fonts Licensing FAQ for full details" [90]. That is marketing text, not the terms. Public exhibition and cinema are not mentioned there.

**Decision rule (J).** All on-screen text in OFL fonts (for example Google Fonts). If the maker wants a commercial font, email the vendor from the rights log (T8 `fonts` sheet): "Rendered into video frames; shown once at a public venue on 27 February 2027, possibly later in a cinema; no font file leaves my computer." Keep the reply with the font's licence file (TY3).

### FQ5. SMPTE RP 431-2 and ST 428-1 read from the documents

**Answer.** I read the three documents from SMPTE's own publication site, full text, on 2026-10-18: RP 431-2:2011 (approved 6 April 2011; the site lists it as "stabilized") [91], ST 431-1:2006 (approved 18 April 2006; listed "active") [92] and ST 428-1:2019 (approved 12 February 2019) [93]. The "48 cd/m2 +/- 3.5" figure is real but sits in **ST 431-1, not RP 431-2, and it is the Review Room tolerance. The Theater tolerance is +/- 10.2 cd/m2.** That changes the earlier notes.

| Figure | Where it is | Value |
|---|---|---|
| Reference white luminance | ST 431-1 s5.1 and Table 1; RP 431-2 Annex C.3 | 48.0 cd/m2 (14.0 fL) at the screen centre, white x = 0.314, y = 0.351 |
| Luminance tolerance, centre | ST 431-1 Table 1 | Review room +/- 3.5 cd/m2 (+/- 1.00 fL), i.e. 44.5 to 51.5. **Theater +/- 10.2 cd/m2 (+/- 3.00 fL), i.e. 37.8 to 58.2.** |
| Luminance at the sides | ST 431-1 Table 1 | 75% to 90% of centre (Theater); 80% to 90% (Review room); corners are specified for Review rooms only |
| Meter | ST 431-1 s4.3 to 4.4 | at the centre of the seating row nearest the middle, 1.1 m above the floor; spot photometer, acceptance angle 2 degrees or less, accuracy +/- 0.5 cd/m2 or better |
| Transfer function | RP 431-2 Table A.1 (7.7), Annex C | Gamma 2.6, +/- 2% (Review room), +/- 5% (Theater); tolerance is a least-squares fit of the log-log slope from peak white down to 5% of peak white |
| Sequential contrast | RP 431-2 s7.5, Table A.1 | 2000:1 nominal, at least 1500:1 (Review room), at least 1200:1 (Theater), measured in place including ambient light |
| Intra-frame (checkerboard) contrast | RP 431-2 s7.6 | 150:1 nominal, 100:1 minimum for both classes |
| Ambient light on the screen with the projector off | RP 431-2 s6.1 | below 0.01 cd/m2 (0.0029 fL) for Review rooms, **below 0.03 cd/m2 (0.01 fL) for Exhibition Theaters**; exit and access lights may raise it, "this will reduce the contrast of the projected image" |
| Grading viewing distance | RP 431-2 s6.3 | 1.5 to 3.5 screen heights |
| Encoding (DCDM) | ST 428-1 s4.2 to 4.3 | 12-bit code values; CV = INT(4095 x (L x X / 52.37)^(1/2.6)) for X, Y, Z; L = reference luminance 48 cd/m2; 52.37 cd/m2 is the headroom peak that allows D55, D61 and D65 whites |
| Worked example | ST 428-1 Annex B.1 | white (0.314, 0.351, 48.00) gives X = 42.94, Y = 48.00, Z = 45.82 and codes 3794, 3960, 3890 (I recomputed all three from the formula: they match) |

- **Notes on the numbers (M).** Theater class at the screen centre spans 37.8 to 58.2 cd/m2, so the D5 target of "about 45 nits or more" is inside the SMPTE Theater class, not outside it. An ambient figure of 0.03 cd/m2 is only 0.09 lux of stray light on a matte gain-1 screen (L = E / pi), which no hall with house lights or exit signs on will meet.
- **Test patterns the D5 test card can copy (RP 431-2 Annex B, informative, and Tables A.2 and A.3).** The standard gives a 10-step black-to-white grey scale (0.14, 0.75, 2.12, 4.45, 7.94, 12.74, 19.01, 26.89, 36.52 and 48.02 cd/m2, steps 1 to 10) and a 10-step black-to-dark-grey scale (0.030, 0.063, 0.135, 0.254, 0.442, 0.695, 1.026, 1.442, 1.950 and 2.557 cd/m2, which include a 0.024 cd/m2 screen black). Each pattern fills 20% of the picture height and 80% of the width, each step is 8% of the width, on a background of 4.80 cd/m2 (code values 1565, 1633, 1604) for the white scale and 0.030 cd/m2 (122, 128, 125) for the dark scale. For banding, Annex B asks for ramps with steps "no less than 4 pixels" wide and one code value per step, "placed on a background equal to the minimum value in the ramp", and adds that "a dynamic test pattern that fades slowly to black is another useful approach"; nothing may show "contouring (step in luminance), or color deviation from the neutral gray". For a display at 48 cd/m2 and gamma 2.6 the dark steps are 8-bit full-range signal levels 15, 20, 27, 34, 42, 50, 58, 66, 74 and 83, from (Y / 48)^(1/2.6) (M).
- **A meter-free read of the room (J, from my arithmetic).** Ambient light of E lux on a matte gain-1 screen is E / pi cd/m2. The dark steps at or below that are lost: 0.5 lux hides steps 1 to 3, 2 lux hides steps 1 to 5, 5 lux hides steps 1 to 8 (M). So the number of dark steps the maker cannot tell from black, standing at the back row with the real lights on, is a rough ambient reading without a lux meter.
- **Corrections to the earlier notes.** (1) Q10 and D5 said "DCI requires reflected ambient light under 0.01 cd/m2 for the test [35]". RP 431-2 says 0.01 for Review rooms and 0.03 for Exhibition Theaters. (2) The "+/- 3.5" tolerance belongs to the mastering-room class. (3) The earlier note used gamma 2.6 as a single figure; the standard allows +/- 5% for a theatre.
- **Scope.** These are the cinema reference conditions. They apply to a DCP played on a conforming projector. HDMI to a venue projector or TV follows no SMPTE document here; the gamma to grade for is a decision (FQ7). I did not read the DCI Digital Cinema System Specification (`dcimovies.com` served an empty JavaScript page). UNVERIFIED: whether a 2026 revision of RP 431-2 or ST 431-1 exists; the site lists these as the latest versions.

### FQ6. Published reactions to animated portraits of the dead, and whether post-premiere next-of-kin consent is realistic for a later cinema cut

**Answer in short.** I found published first-hand reactions only inside one vendor-curated post, plus press headlines and peer-reviewed commentary that treat the reactions as strong and mixed. I found **no independent first-hand account by a relative who objected to a portrait of their dead being animated**, and I could not read the main news pieces. The absence is a limit of my access (see "What I could not read"), not evidence that no objection exists. Written consent from next of kin after the premiere is **realistic for a small family circle and for stills or recordings**, but it is not a legal gate I can confirm, it cannot cover the premiere cut, and it cannot be retroactive cover for animating faces. The existing rule (no face animation of the dead) stays. Read 2026-10-18.

**What exists.**
- **Vendor-curated first-hand quotes** (MyHeritage blog, 2021-03-04: "Over 10 million faces have been animated so far") [94]. Named users, selected by the vendor, so skewed positive. Emotional: Natasha says her grandmother, shown her great-grandfather, "broke down crying"; Jean McKenney (mother died in 1992): "It brought tears to my eyes"; Tracy Iglesias: "Seeing his face move after decades was mind-blowing"; Diego R. Cáceres (father died when he was seven months old): "Even for a few seconds, today you were mine!" (translated). Mixed or uncanny, same post: Jason Glisson (grandfather's WWII photo): seeing it move "really shocked me"; a Spanish-language user (translated): "my heart falls to the floor every time he blinks". The post says nothing about consent from the person depicted or from relatives; it says the technology is licensed from D-ID. (Earlier round: `ai-imagery.md` Q8 read the same post [P8].)
- **Press framing, headlines only.** Three pieces that the Kopelman and Frosh paper cites, as listed in its Crossref reference record: Hern, The Guardian, 1 March 2021, "Deep Nostalgia: 'creepy' new service uses AI to animate old family photos"; Wakefield, BBC News, 26 February 2021, "MyHeritage offers 'creepy' deepfake tool to reanimate dead"; Cuthbertson, The Independent, 1 March 2021, "Deep Nostalgia AI brings old photos to life with 'creepy' accuracy" [95]. I did not read the articles (the fetch tool refuses these hosts).
- **Peer-reviewed.** Kopelman and Frosh (*New Media & Society* 27(4), online 10 November 2023; abstract and reference list only) call it a "magical and affective space for realizing impossible longings"; their evidence is press and social media, not interviews [95]. **"Synthetic Heritage" (*Memory, Mind & Media*, 2024, open access, read in full) [96]** says most images animated by Deep Nostalgia and DeepStory "are of users' deceased relatives", asks "whether a deceased person can be considered to have consented to a (remediated) algorithmic afterlife", and says the "manipulation of grief in this context can elicit negative emotional reactions of family and other members of the mourning community that also lay claim to the deceased relative" (it cites a different paper for that; I did not read it, so this is a scholar's claim, not a measured result). It also records that MyHeritage asks users to upload only "own historical photos" and never photos of living people without permission: **the product has no next-of-kin step for the dead**.
- **Surveys of intention, not family reactions.** OpenAlex lists 26 works citing Kopelman and Frosh [97]. The relevant empirical ones: a 470-person survey (*International Journal of Consumer Studies*, 2026, open access; abstract read; the PDF returned 403) found realism raises perceived authenticity and relief, and that "perceived desecration does not significantly affect adoption intention"; an interview-based grounded-theory study (*International Journal of Human-Computer Interaction*, 2025; abstract only). They measure willingness to use, not how a bereaved relative feels when shown an animation someone else made, which is our case. A 2026 conference paper on realism and "ethical acceptance" of AI recreations of the dead has no abstract in OpenAlex and was not read.
- **Adjacent, voice rather than portrait.** In the 2021 *Roadrunner* dispute over an AI-generated Anthony Bourdain voice, his estate executor Ottavia Busia said, in a tweet: "I certainly was NOT the one who said Tony would have been cool with that", and in an email reported on 17 July 2021: "I do believe Morgan thought he had everyone's blessing to go ahead" [98]. The critics quoted (as summarised on Wikipedia, not read at source) objected to non-disclosure; David Leslie of the Alan Turing Institute is quoted as saying AI-recreated voices should not be ruled out if the subject consented and audiences were told in advance. The charter already bars synthetic voices.
- **Design guidance for "deadbots".** Cambridge's 9 May 2024 press page on Hollanek and Nowaczyk-Basińska (*Philosophy & Technology*; I read the press page, not the paper) recommends seeking consent from data donors before death, considering the rights of those who must interact with the simulation, opt-out and "dignified retirement" [99]. It is about chatbots, not portraits.

**What it means for this film (M for the readings, J for the judgments).**
1. Reactions are real and strong, and they can split inside one family: the same post has tears of joy and "really shocked me". The risk in the premiere room is the mother seeing her own late parent move, in public, with no warning. That supports the standing default: no face or expression animation of the dead, parallax and environment motion only [P8][P7].
2. "Closest family" may be many people. The scholar's point about a "mourning community" that also lays claim means one yes is not everyone's yes: ask the mother and at least one sibling or the next closest relatives, and treat any "no" as a no (J). The mother is probably herself the closest family of her late parents, so her own release (T9 4e) is the first ask, not the last.
3. **Post-premiere written consent is realistic where the circle is small and reachable.** The playbook already plans written releases between 28 February and 6 March 2027 and closes the consent ledger on 29 March 2027 (TD-L15, TD-L16) with form 4g for the family of the dead [P7]. After the reveal, secrecy no longer blocks the ask (J). Make it specific and shown, not general: send the exact still or clip, say what is and is not done to it, and say it may be removed later.
4. **It is easier to ask first than later.** The International Documentary Association's practical guide to appearance releases says "it's generally better practice to get a release signed before an interview begins, rather than ask for it after it's over", that asking late can make a subject feel the producer needs it and so invite refusal, that "A verbal release should cover at least the most basic elements of a written release" as a fallback, and that "E&O carriers may require releases as a condition of coverage" [100]. Its 2012 E&O guide says "Written releases must be obtained for faces and likenesses of any recognizable living persons" [101]. Neither article addresses deceased people or their estates. So for a cinema cut I can confirm an insurer or exhibitor will want a clearance file, and I cannot confirm what it will want for the dead.
5. **The law depends on where.** The Wikipedia summary of personality rights gives California 70 years after death, Indiana and Oklahoma 100 years, Tennessee without expiry while use continues, and a federal ruling that New York protects no post-mortem right of publicity; it gives no duration for Germany or France and does not cover the UK [102]. The earlier delivery note had Germany at 10 years of relatives' consent [P7]. The premiere country is still an open decision, so treat next-of-kin consent as ethical practice and insurer prudence until the one-hour consult (TD-L5; T10 question 8) answers it.
6. **Failure modes and fixes (J).** (a) A relative refuses or does not reply: the shot stays out of the cinema cut. (b) Relatives disagree: the "no" wins. (c) Consent is asked for the premiere cut: it is not, because the premiere runs on the Tier rules, and a later yes never covers the earlier showing. (d) Rework cost: tag every shot that shows or voices a dead person with a flag in `timeline.json` and keep a stills-only or cut-away fallback for it, so a "no" costs a re-render and not a re-edit.

**What I could not read.** The Guardian, BBC, Independent, The Verge and New Yorker pieces (the fetch tool refuses those hosts); the Kopelman and Frosh body and the Wiley survey PDF (403); the Hollanek and Nowaczyk-Basińska paper (a Springer login redirect); California Civil Code 3344.1 (the legislature's site returned 403). The web-search budget for this run was used up before this question, so I could not look for further first-hand accounts. A later pass with search should look for interviews with relatives, grief-counsellor commentary, and the Parkland and Arizona court cases where families authorised an AI likeness. All UNVERIFIED until then.

### FQ7. What only the maker can answer (venue and playback), and the scenario numbers until then

**Status: OPEN, and not researchable on the web.** Until the maker answers, every brightness, gamma, black-level, type-size and sound number in this note and in D5 is a scenario. Context from the maker this session: the maker is the only person on the project, so there is nobody else to ask; the venue's AV person is the one outside contact the maker needs, and asking them "what projector and cable is in the room" does not reveal the film. Six answers, in the order they unlock the most:

| # | Ask the maker | Why it matters | What it unlocks | Default used until answered |
|---|---|---|---|---|
| 1 | **Playback path:** a DCP on a cinema server, a laptop or media player over HDMI, or a USB stick into the venue's own player or TV | Decides the grading gamma and the master | 2.6 (DCP, SMPTE class) or 2.4 (BT.1886 reference for HDMI) or 2.2 (a typical TV or laptop panel), and whether the DCP track is needed at all | HDMI, 2.4, 1080p H.264 plus ProRes master (scenario B) |
| 2 | **Venue type and screen:** hall, theatre, restaurant or community room; screen width and picture height in metres (tape-measure the lit area); is it a projector screen or a TV, and its size in inches | Screen area sets nits; screen height sets seat distance in screen heights | Brightness from lumens (table below), the farthest-seat distance, the type-size floor | 6 m wide, 16:9 |
| 3 | **Projector or display model** (photograph its label), lamp or laser hours, and whether it is 1080p or 4K native | Lumens, native resolution, scaler and picture modes | Nits at the screen, whether UHD is worth the render time, which menu settings to turn off (D5 item 12) | 3,000 lm, 1080p |
| 4 | **Can the room be darkened,** and how dark: lights fully off, exit signs, windows or blinds, and a lux reading on the screen with a phone app with the lights as they will be (the phone sensor is not calibrated: UNVERIFIED, so use it for ratios, not absolutes) | Ambient light lifts the black and hides shadows | The signal level below which detail is lost (table below) and how much to lift the grade | 2 lux on the screen (a dim hall) |
| 5 | **Who runs AV** and whether they will do a test on a weekday, with the real chain, at least two weeks before 27 February | The only way D5 gets run | A venue test slot; which person to send the test card to | The maker runs it |
| 6 | **Sound:** is there a PA the room already uses, who controls it, can the film go in as stereo or 5.1, is there a hearing loop, and how many seats | Speech intelligibility and captions | The FQ8 test; the loudness target; whether captions are essential | Stereo through the room PA; captions burned in |

**Scenario table, by playback path (arithmetic, my formulas; (J) where marked).**

| Scenario | Reference | Gamma to grade for | Brightness reference | Notes |
|---|---|---|---|---|
| A. DCP on a conforming cinema projector | SMPTE RP 431-2 and ST 431-1 (FQ5) | 2.6 +/- 5% (Theater class) | 48 cd/m2 nominal; 37.8 to 58.2 in class | Ambient below 0.03 cd/m2 |
| B. HDMI to a venue projector in a dim room | BT.1886 (J) | 2.4 | lumens x gain / (pi x screen area) | The usual case for a public hall |
| C. A TV, or a laptop on a TV | none (J) | 2.2 to 2.4 | typically far brighter than 48 cd/m2, which I could not source (UNVERIFIED) | Banding and judder matter more, black is better |

- **Lumens needed for 48 cd/m2** on a matte gain-1 screen (L = lumens x gain / (pi x area), picture 16:9): width 3 m about 760 lm; 4 m 1,360; 6 m 3,050; 8 m 5,430; 10 m 8,480; 12 m 12,200 (M). Spec-sheet lumens are usually ANSI or peak; lamp ageing and lens loss lower them, so treat these as optimistic. At 3,000 lm a 6 m screen gives 47 cd/m2, 8 m gives 27, 10 m gives 17 (M).
- **How much ambient light hides.** A matte gain-1 screen reflects L = E / pi, with E the lux falling on it. At 48 cd/m2 peak and gamma 2.6, signal below this level is under the ambient wash (M): 0.1 lux, 6%; 0.5 lux, 11%; 2 lux, 19%; 5 lux, 27%; 20 lux, 46%; 50 lux, 65%. Peak contrast falls to about 75:1 at 2 lux and 8:1 at 20 lux. So the earlier D5 rule "no story-critical detail below about 10% signal" is only safe in a room at about 0.4 lux or darker on the screen. In a hall with some light on, grade the dark scenes up or avoid them.
- **Gamma moves shadows (M).** A signal at 10% gives a relative luminance of 0.0025 at 2.6, 0.0040 at 2.4 and 0.0063 at 2.2, so grading for 2.6 and showing on a 2.4 display makes shadows 58% brighter than intended (1 / 0.63), and grading for 2.4 and showing on 2.2 makes them 58% brighter again. Decide the path in week 2 (TD-1).
- **Type size follows distance.** With the farthest seat at 5 screen heights the x-height floor is 2.6% (Q10); at 6 screen heights, 3.1%; at 7, about 3.7%. Seat distance in screen heights = distance to the screen in metres divided by picture height in metres.

### FQ8. Estimating speech transmission index (D5 item 13) without a meter

**Answer.** Three routes, in order of evidence. None is verified against a calibrated meter here, so every STI figure below is **UNVERIFIED** until it is compared with one.
1. **A phone app that implements the standard's STIPA method (iOS only).** Studio Six Digital's AudioTools has a "STIPA Basic" module at $49.99 in the US App Store (vendor's page, copyright 2025), which the vendor says is "fully compliant with v4 of the standard" and works with the iPhone's built-in microphone, while recommending an external measurement mic for fire-code work. The STIPA test signal is a downloadable file you play through the room's own chain; a separate "STIPA Compliance Study" is offered (I did not read it, and it is the vendor's own document) [103]. The IEC standard itself (IEC 60268-16, the edition in force is 2020) is paywalled and I did not read it. I found no Android equivalent (UNVERIFIED).
2. **Free software on the maker's Windows PC.** Room EQ Wizard's features page (copyright 2026) lists "Calculation of Speech Transmission Index (STI) by the indirect method per IEC 60268-16:2020" [104]. The help index I scanned (copyright to 2022, 58 pages) never mentions STI, and its revision history does not say which version added it, so check that the installed version shows it (UNVERIFIED). It needs an impulse response of the room-plus-PA path. REW's offline-measurement help says the sweep made in its Signal Generator can be played back through the system and the response "recorded by other means" (a phone or handheld recorder), then imported with File > Import Sweep Recordings; a timing-reference signal is required, and the recording must be at the sweep's sample rate or an integer multiple or fraction of it [104]. So the sweep can ride in the film's own audio track on the test card, and the maker records it from the back row. A phone microphone's automatic gain and processing could corrupt the result (UNVERIFIED; use a recorder or a measurement mic if one is borrowable). Caveats from the standard as quoted on Wikipedia: indirect measurement can mislead where loudspeakers behave non-linearly or background noise is present, and the standard warns "Critical analysis is therefore required of how the impulse response is obtained" [105]. Direct STIPA is preferred for PA systems.
3. **A read-back proxy with scoring, which needs nothing but listeners.** Use unpredictable words, not sentences. The STI bands in IEC 60268-16, as tabulated on Wikipedia for native, normal-hearing listeners, map to these scores [105]:

| STI | Band | Syllables correct | Words correct | Sentences correct |
|---|---|---|---|---|
| 0.60 to 0.75 | good | 67 to 90% | 87 to 94% | 95 to 96% |
| 0.45 to 0.60 | fair | 48 to 67% | 78 to 87% | 92 to 95% |
| 0.30 to 0.45 | poor | 34 to 48% | 67 to 78% | 89 to 92% |
| 0 to 0.30 | bad | 0 to 34% | 0 to 67% | 0 to 89% |

Sentences are a poor test: they sit at 92% to 96% from STI 0.45 upward, so a sentence list cannot tell fair from excellent. Words are the sensitive measure. The table is for native speakers, and "other probabilities hold" for non-native, hard-of-hearing or speech-disordered listeners, which describes part of a public audience (J).

**Proposed protocol for D5 item 13 (J, built on that table).**
- **Material.** A 100-word list of unrelated one- and two-syllable common words, read in the narrator's voice at the film's own level and mixed as in the film, plus the number passage D5 already lists. Rhyme-test lists (MRT, ANSI S3.2 and ISO 4870 are the usual standards; not read) are better if the maker can get a copy; otherwise any unpredictable list the maker writes is acceptable as a screening test.
- **Listeners and places.** At least one listener who has not heard the list, at the back row and one at the front; the maker does not score their own ears. Ideally someone over 60, because that is the audience. Same room state as the event (lights, doors, fans).
- **Scoring.** Words correct out of 100, spelling errors ignored, homophones accepted.
- **Pass rule (J).** 90 or more correct at the back row: consistent with the "good" band; fewer than 80: below "good", fix the sound or rely on captions; 80 to 89: inconclusive, repeat with a different list or use an app. Why the wide middle: with n = 100, a 95% Wilson interval is about plus or minus 7 points (87 of 100 gives 79% to 92%; 94 of 100 gives 88% to 97%) (M), and the band edges (78, 87, 94) are only 7 to 9 points apart.
- **Conversion if a number is wanted.** Common Intelligibility Scale CIS = 1 + log10(STI): STI 0.45 is 0.65, 0.50 is 0.70, 0.60 is 0.78, 0.75 is 0.88 (M, from the formula quoted on Wikipedia [105]).
- **Noise.** Record the room's background level with a phone SPL app at the back row with the film stopped (phone SPL readings are uncalibrated: UNVERIFIED); STI falls fast as the speech-to-noise ratio drops.
- **What it does and does not test.** STI describes the sound path (room, PA, any processing). A read-back on the film's real dialogue also tests the mix and the narrator's diction, which STI would not.
- **Fallback.** Captions burned in (FQ1) cover any line that matters.

### Tools, services and costs added this round (as of 2026-10-18)

- OFL fonts, free. Monotype Fonts and Adobe Fonts are subscriptions (prices not read).
- Studio Six Digital AudioTools STIPA Basic, $49.99 US App Store (vendor page, copyright 2025), iOS only. Room EQ Wizard, free, Windows; an external measurement microphone is a purchase (price not researched).
- No new paid services were used in the measurements. Library of Congress and Smithsonian Open Access were queried through their public interfaces (the Smithsonian API with the shared `DEMO_KEY`).

### Open items after round 1

1. **Maker:** answer the six venue questions in FQ7; run `caption_xheight.py` on the Windows ffmpeg with the caption font; try the free REW route or the iOS app on the venue's PA, or run the 100-word read-back.
2. **Search pass needed** (the web-search budget was used up before FQ4 to FQ8): first-hand family accounts of animated portraits of the dead; Adobe Fonts' licensing FAQ (blocked at the edge for the fetch tools; the maker can read it in a browser); the Kopelman and Frosh body text (the maker can read it free at its DOI); California Civil Code 3344.1 and the 2024 digital-replica amendment; the IEC 60268-16 mapping from a primary source; an Android STIPA app, if one exists.
3. **Run once at the venue:** the A/B push clip (Pillow against `zoompan`) and the pan-speed clip, to decide whether MO8's 0.05 px and MO6's 0.143 are visible limits on that screen.
4. **Scribe:** apply the deltas above; `format.md` line 77 and line 674 take the x-height figures.

### New sources (round 1), continuing the numbering

Labels as above. "Read in full" means I read the whole document or page text as served; "abstract only" and "headline only" are limits. All retrieved on 2026-10-18.

- [86] SIL OFL FAQ (version 1.1-update7, November 2023; footer "Last updated on 12 January 2026") — https://openfontlicense.org/ofl-faq/ — read in full (raw page): items 1.1, 1.1.1, 1.1.2, 1.11 to 1.13, 1.26.
- [87] SIL Open Font License 1.1, official text — https://openfontlicense.org/open-font-license-official-text/ — read: permission and conditions.
- [88] Monotype Fonts "Service & License Terms" (Enterprise, "Large brands") — page https://www.monotype.com/legal/eula (redirects to https://www.monotypefonts.com/pages/eula); text loaded from the publisher's content feed `https://cms.monotypefonts.com/getcontent/block?type=text&id=612` — read in full; no revision date in the text.
- [89] Monotype Fonts Create + Deploy EULA (feed `id=807`) and Create + Pitch EULA (feed `id=795`) — same site — read in full; no revision date; Trial EULA (`id=926`) fetched, not read in detail.
- [90] Adobe Fonts home page — https://fonts.adobe.com/ — "Simplified licensing" text, footer "(c) 2026 Adobe"; vendor summary only. The licensing FAQ `https://helpx.adobe.com/fonts/using/font-licensing.html` returned "Access Denied"; not read.
- [91] SMPTE RP 431-2:2011, D-Cinema Quality, Reference Projector and Environment (approved 6 April 2011; state "stabilized") — https://pub.smpte.org/latest/rp431-2/rp0431-2-2011.pdf — read in full (14 pages).
- [92] SMPTE ST 431-1:2006, D-Cinema Quality, Screen Luminance Level, Chromaticity and Uniformity (approved 18 April 2006; listed "active") — https://pub.smpte.org/latest/st431-1/st0431-1-2006.pdf — read in full (5 pages).
- [93] SMPTE ST 428-1:2019, D-Cinema Distribution Master, Image Characteristics (approved 12 February 2019) — https://pub.smpte.org/latest/st428-1/st428-1-2019.pdf — read in full (8 pages).
- [94] MyHeritage blog, "Deep Nostalgia is an Internet Sensation!" (2021-03-04) — https://blog.myheritage.com/2021/03/deep-nostalgia-is-an-internet-sensation/ — read; vendor-curated user posts.
- [95] Kopelman and Frosh, "The 'algorithmic as if': Computational resurrection and the animation of the dead in Deep Nostalgia", New Media & Society 27(4), DOI 10.1177/14614448231210268 — record and reference list from https://api.crossref.org/works/10.1177/14614448231210268; the publisher page returned 403. The Guardian, BBC and Independent pieces are known from its reference list only.
- [96] "Synthetic Heritage: Online platforms, deceptive genealogy and the ethics of algorithmically generated memory", Memory, Mind & Media (2024), DOI 10.1017/mem.2024.10, open access (CC BY 4.0) — https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7833DF6D1DAEDFFA5518DBE17965024D/S2635023824000109a.pdf/div-class-title-synthetic-heritage-online-platforms-deceptive-genealogy-and-the-ethics-of-algorithmically-generated-memory-div.pdf — read in full (18 pages); consent and "mourning community" passage on page 9.
- [97] OpenAlex records of works citing [95] — https://api.openalex.org/works?filter=cites:W4388568632 — titles for 26 works; abstracts read for six (International Journal of Consumer Studies 2026, DOI 10.1111/ijcs.70253; International Journal of Human-Computer Interaction 2025, DOI 10.1080/10447318.2025.2596855; Journal of Family Communication 2025, DOI 10.1080/15267431.2025.2485911; two Memory, Mind & Media papers; a 2026 scoping review). Abstracts only.
- [98] Wikipedia, "Roadrunner: A Film About Anthony Bourdain" — https://en.wikipedia.org/wiki/Roadrunner:_A_Film_About_Anthony_Bourdain — secondary summary of The New Yorker (2021-07-15, 2021-07-17), Deadline (2021-07-16) and BBC News (2021-07-16); the originals were not readable.
- [99] University of Cambridge, press page on Hollanek and Nowaczyk-Basińska, Philosophy & Technology (published 2024-05-09), DOI 10.1007/s13347-024-00744-w — https://www.cam.ac.uk/research/news/call-for-safeguards-to-prevent-unwanted-hauntings-by-ai-chatbots-of-dead-loved-ones — press page only; the paper redirected to a Springer login.
- [100] Steven Beer, "A Practical Discussion of Appearance Releases", International Documentary Association (2018-08-30) — https://www.documentary.org/column/practical-discussion-appearance-releases — read.
- [101] Winnie Wong, "Errors & Omissions: Rights Oh My! A Guide to Protecting Your Film", International Documentary Association (2012-04-06) — https://www.documentary.org/feature/errors-omissions-rights-oh-my-guide-protecting-your-film — read.
- [102] Wikipedia, "Personality rights" — https://en.wikipedia.org/wiki/Personality_rights — secondary; first 100,000 of 131,700 characters read.
- [103] Studio Six Digital, AudioTools "STIPA Basic" — https://studiosixdigital.com/audiotools-modules-2/speaker-test-modules/stipa-basic/ — read (copyright 2025); vendor page; its "STIPA Compliance Study" not read.
- [104] Room EQ Wizard, features page https://www.roomeqwizard.com/features.html (copyright 2026) and help pages `https://www.roomeqwizard.com/help/help_en-GB/html/offlinemeasurements.html` and the help index (58 pages scanned for "STI": none) — read.
- [105] Wikipedia, "Speech transmission index" — https://en.wikipedia.org/wiki/Speech_transmission_index — secondary; the STI band and intelligibility table is attributed there to IEC 60268-16; the standard itself was not read (paywalled).
- [106] Library of Congress, "South of India. Women Grinding and Children" (photochrom print, Photoglob, about 1890 to 1910) — https://www.loc.gov/item/2017657625/ — item record read (rights: "No known restrictions on publication"); master TIFF https://tile.loc.gov/storage-services/master/pnp/ppmsca/41400/41470u.tif.
- [107] Smithsonian Open Access (usage "CC0"), National Museum of African American History and Culture items NMAAHC-2011_36_119_001 ("Photograph of A. J. Wiseman", about 1895) and NMAAHC-2013_244_36_001 ("Albumen print of U. S. Colored Troops at Ft. Douglas", 1896 to 1899), found through https://api.si.edu/openaccess/api/v1.0/search and fetched from `https://ids.si.edu/ids/deliveryService?id=<ID>&max=6000`.
- [108] My measurements, 2026-10-18, cloud container (ffmpeg 6.1.1, Python 3.13, numpy, Pillow). **M-C8** caption x-height (FQ1); **M-C7b** `zoompan` against sub-pixel resampling on three prints (FQ2); **M-C9** pan estimator validation (FQ3). Scripts and result files are in research/cinematic-quality-fixtures/ (see its README). Print images were downloaded to a temporary folder, used and deleted; no family material was used. One run of the third print was killed by the container's memory limit and was re-run alone; the partial first run was discarded.
- [P6] `research/format.md`, FQ2 "Caption size gotcha" and FQ5 — read.
- [P7] `playbooks/theatrical-delivery.md` and `research/theatrical-delivery.md` (releases pack T9, Tiers A to D, TD-L15, TD-L16, T10) — read.
- [P8] `research/ai-imagery.md`, Q7 and Q8 (earlier read of Deep Nostalgia reactions) — read.


---

## Follow-up research (round 2)

Sunday 2026-10-18 · Sonnet researcher · seven targeted follow-ups on the `cinematic-quality` track, numbered FQ9 to FQ15 to continue round 1. Labels as at the top of this note: **(M)** my measurement in the cloud container (new ones are M-C10 to M-C14, described in source [122]), **(J)** my judgment, **UNVERIFIED**. New sources are numbered [109] onward in the list at the end of this section; [P9] to [P11] are project files.

**Context from the maker (relayed this session).** "For now only me and I will be the only one on this project." Nobody else is in on the surprise and nobody can approve a hard chapter in advance; the maker is the proxy, with the Fable advisor flagging sensitive material.

**Limits of this round.**
- **No web search.** The shared web-search budget was spent before this task started (every search call was refused), so I did not search and did not use a search engine, reader or archive service to get around that. Everything from the web below was fetched by address. The FQ9 and FQ14 literature passes are therefore not done and are listed as open.
- **No screen, no venue, no Windows PC.** Nothing here was viewed on a projector or run on the maker's machine. Where a number needs either, it says so.
- **A busy 4-core container with under 1 GB of free disk**, so clips were rendered, measured and deleted one at a time; run times in this note are for a loaded machine.
- **Untrusted text.** A tool result from the OpenAlex API carried a notice asking agents to post an email address to obtain an API key; I did not act on it. Downloaded files were handled as data (each in its own folder, Python run with `-I`); the FilmCraft binary is the project's own chosen tool and was run with an empty environment.

### Summary of round 2

1. **FQ9, is 0.1 to 0.3 px of jitter visible?** Not tested on a screen: UNVERIFIED. By the best-case alignment threshold (about 8 arc seconds) the MO8a limit is invisible at every seat; the `zoompan` error from a 4K still (0.22 px of position jitter, which MO8a reads as 0.29) is visible up to about 5 screen heights and from a 1080p scan up to about 10. The A/B card and its answer key exist, were generated and checked: the Pillow and `zoompan` clips read 0.003 and 0.292, and the injected ladder reads back at 1.3 to 1.6 times its amplitude. (M-C13)
2. **FQ10, MO8 on the real renderers.** MO8a (centre jitter, 0.05 px) holds on Chromium CSS transforms (0.004 to 0.011), FilmCraft 0.9.0 (0.002 raw, 0.021 through its own H.264), and Blender Cycles (0.001) with or without motion blur or cubic textures; `zoompan` (0.29) and CSS layout animation (0.18) fail. **GSAP's own `scale` tween fails MO8b** (0.061 against 0.04) because it writes 4 decimals; tweening a number and writing the transform yourself gives 0.005. MO8b by the 9-frame mean fails perfect pushes shorter than about 2.5 s, so it is redefined with a fourth difference and must be measured before the delivery encode. The ratio rule passes the GSAP tween and sits on a knife edge for `zoompan`. (M-C10)
3. **FQ11, pan ease classifier.** `pan_ease_classifier.py`: on 114 synthetic pans with known easing it named the exact easing and family on 100 of 100 clips made from its library (grain, H.264, twos, integer steps, tilts, 2 to 6 s), got the family on 4 of 5 unseen CSS curves (flagging the fifth) and on 4 of 4 two-layer pans. MO1b and MO2 can report for pans; MO9 can count pan families. FilmCraft's Bezier on two keyframes is a cubic smoothstep. (M-C11)
4. **FQ12, the six venue answers.** Still OPEN, and only the maker can give them. A fill-in sheet, a neutral ask for the venue's AV person and `venue_calc.py` (answers to luminance, hidden shadow level, seat distances, type floors, jitter in arc seconds) are ready. (M-C14)
5. **FQ13, fonts after the subscription ends.** Adobe's binding terms (7 Oct 2024) were found and read: the licence is "only for as long as you maintain an uninterrupted Adobe Subscription Plan" and says nothing about video or finished work; the FAQ is still unreadable (403). Monotype's three agreements grant "during the Term" and keep no rights after it, except a clause for software applications that a film is not. Rule: a commercial font only if the subscription is in force on every showing date, or use OFL fonts.
6. **FQ14, relatives who objected.** No search was possible. No first-hand relative's objection to an *animated photograph* found; adjacent first-hand objections to AI likenesses of famous dead people (Kelly Carlin, Zelda Williams) found through secondary pages. Kopelman and Frosh and the best Deep Nostalgia tweet study (Kidd and Nieto McAvoy) are open access but blocked to the tools; the maker can read both free. Rule unchanged.
7. **FQ15, Windows check.** Not run on the maker's PC (no access). `caption_xheight.py` made Windows-safe and able to test the maker's own font (output identical to round 1 on Linux), `pan_estimator.py` made memory-lean (identical output), and `windows_check.py` runs everything in one command with versions recorded. Its container run: all five steps PASS (x-height 3.27 / 3.80 / 4.26% at `FontSize` 20 / 23 / 26 in DejaVu Sans; `zoompan` 16 times rougher than Pillow; pan estimator within 0.04 px; cosine pan read as in-out).
8. **Side result for craft-motion.** The FilmCraft 0.9.0 Linux CLI runs in this container (spike S1 T1 passed): headless project, import, keyframes, ProRes and H.264 export, 96 frames of 1080p in 24 to 37 s.

### FQ9. Is 0.1 to 0.3 px of random frame-to-frame jitter visible on a 6 to 10 m screen? (prediction from arithmetic; the screen test is still the maker's)

**Answer.** **Not tested on a screen, so MO8a's 0.05 px is still a derived limit, not an observed one. UNVERIFIED.** What I could do from here: (1) work out what each jitter amount subtends from each seat, (2) build the venue test as a blind, randomised card with a known-jitter ladder, so the visible limit comes out of one 15-minute session, and (3) run the card's generator and check its answer key against the estimator. The venue session has not happened; no visibility result is recorded. **One correction came out of step 3:** MO8a is the rms of the *frame-to-frame displacement residual*, which reads about **1.3 to 1.6 times** the random *position* jitter that causes it. The `zoompan` figure of 0.29 px is therefore a position error of about 0.22 px rms, and the 0.05 px limit is about 0.038 px of white position jitter. FQ2's numbers are unchanged; what they mean in pixels on the screen is smaller than I implied.

**The arithmetic (M).** For a 1080-line picture seen from *d* picture heights, one pixel subtends 206,265 / (1080 x d) arc seconds. One pixel is 3.1 mm on a 6 m screen, 4.2 mm on 8 m and 5.2 mm on 10 m, so 0.3 px is 0.9 to 1.6 mm on the screen. Rows are random *position* jitter (rms, 1080p pixels); the MO8a reading on the card file is in brackets.

| Position jitter, rms (MO8a reading) | 1.5 H (front rows) | 3 H | 5 H | 7 H | Falls under 8 arc seconds beyond |
|---|---|---|---|---|---|
| 0.038 (0.05, the MO8a limit) | 4.8" | 2.4" | 1.5" | 1.0" | 0.9 H |
| 0.05 (0.073) | 6.4" | 3.2" | 1.9" | 1.4" | 1.2 H |
| 0.10 (0.144) | 12.7" | 6.4" | 3.8" | 2.7" | 2.4 H |
| 0.20 (0.325) | 25.5" | 12.7" | 7.6" | 5.5" | 4.8 H |
| 0.22 (0.29: `zoompan`, 4K still) | 28.0" | 14.0" | 8.4" | 6.0" | 5.3 H |
| 0.30 (0.453) | 38.2" | 19.1" | 11.5" | 8.2" | 7.2 H |
| 0.44 (0.59: `zoompan`, 1080p scan) | 56.0" | 28.0" | 16.8" | 12.0" | 10.5 H |
| 0.47 (0.63: `zoompan`, 4K still, yuv420p chain, the usual command line) | 59.8" | 29.9" | 17.9" | 12.8" | 11.2 H |

(1 H = one picture height from the screen; for a 6 m wide 16:9 screen 1.5 H, 3 H, 5 H and 7 H are 5, 10, 17 and 24 m. One pixel is 1 arc minute at 3.18 H.)

**What the numbers are compared with.** Wikipedia's "Visual acuity" gives vernier (alignment) acuity of "about 8 arc seconds", a sentence tagged [citation needed], cone spacing at the fovea of about 28 arc seconds (the Webvision chapter agrees and cites Curcio et al. 1990), and 1 arc minute for 20/20 [115][117]. Wikipedia's "Hyperacuity" says alignment can be judged "five or ten times better than acuity" and edge position "better than 0.1 pixels", both uncited [116]. I found no source on the visibility of *random frame-to-frame* position jitter in moving imagery; no web search was possible this round, so that literature is unread.

**Reading it (J).**
- By the best-case static alignment threshold, **the MO8a limit (0.038 px of position jitter) is under 8 arc seconds from 0.9 H outward, which is the whole room.** 0.1 px is under it beyond 2.4 H (everything but the very front rows). The `zoompan` error from a 4K still through an RGB path (0.22 px) is over it up to 5.3 H; in the usual yuv420p command line it doubles (0.47 px, up to 11.2 H, see FQ10), and from a 1080p scan it is 0.44 px (10.5 H) or more. The family print will be a 1080p-class scan more often than a 4K one. So the *direction* of FQ2's conclusion holds (zoompan should show on a big screen, Pillow should not), but the margin is smaller than I stated: at 7 H the 4K-still error is about 6" and may not be seen.
- It is a weak prediction. The 8" figure is for a static, ideal, high-contrast alignment task, not 24 fps moving texture, and I could not read the primary sources. And an eye that cannot see an offset can still see what it does to the pixels: a hard edge moved by *r* px changes the value of its boundary pixel by *r* times the edge step (exact for a box-sampled edge). That is a random flicker of 22% on a hairline for the `zoompan` 4K error, 10% for 0.1 px and 4% for the MO8a limit, with energy up to 12 Hz where flicker sensitivity is highest; it averages out when a pixel subtends well under an arc minute (back rows) and is resolved when it subtends more (front rows). I have no threshold for it I can cite.
- So MO8a stays at 0.05 as a **conservative bound ("below the best-case alignment threshold at every seat") until the venue card says otherwise.** If the card shows nothing up to the 0.20 rung from the front row, MO8a can be relaxed to about 0.15; every sub-pixel renderer tested already passes at 0.001 to 0.011 (FQ10), so a relaxation buys little.

**The venue test, built and run once (M-C13).** `ab_push_card.py` writes one H.264 file, an answer key and a recording sheet.
- *Part 1, three A/B pairs:* the same 4% cosine push-in (from 1.03x to 1.07x, so there is margin for the jitter) rendered by Pillow `resize(box)` Lanczos and by ffmpeg `zoompan`, in random order inside each pair, 4 s each.
- *Part 2, a ladder of seven clips:* the Pillow push with random per-frame centre position jitter *added* at rms 0, 0.05, 0.10, 0.20, 0.30, 0.50 and 1.00 px (x and y independent, Gaussian, seeded), in random order. The cards say only "PAIR 2 B" or "LADDER 5", never the amount.
- *Output of the run here:* 1920 x 1080, 24 fps, 85 s, H.264 CRF 14, yuv420p, BT.709 tags, 130 MB, about 7 minutes to generate on a loaded 4-core container. The still defaults to a generated worst-case chart (1/f noise, 300 random hairlines of 1 px at 1080p, small text; an earlier version with a regular grid of lines fooled the estimator, so the chart is deliberately aperiodic). Pass `--still` with any 16:9 image of at least 3840 x 2160 for a real print.
- *The key is true on the decoded file* (measured with `mo8_audit.py` on each clip decoded from the card): the Pillow clips read MO8a 0.0032 and the `zoompan` clips 0.2923 (in the pairs, in whatever order they fell). Ladder, injected position rms to measured MO8a: 0 to 0.0032; 0.05 to 0.073; 0.10 to 0.144; 0.20 to 0.325; 0.30 to 0.453; 0.50 to 0.818; 1.00 to 1.333. The ratio is 1.33 at the top (the square root of two from differencing times 0.94 from the running-mean residual) and 1.4 to 1.6 at the bottom, where the codec's own 0.003 floor adds. Edge jitter reads 0.013 to 0.022 on every rung (the push is unaffected).
- *Reading the result:* the lowest rung marked "yes" from the front row and from the back row, and the lowest "maybe". Rule (J): MO8a = half the **measured** MO8a of the lowest front-row "yes" (the key lists it), never above the measured value of the lowest "maybe". Run it on the real projector, in the room as it will be, at least two weeks before 27 February; it needs a 15-minute slot on the same venue ask as the rest of T6 (FQ12).

### FQ10. MO8 (ratio plus jitter) on the renderers the pipeline will actually use: Chromium CSS/GSAP, Blender, FilmCraft

**Answer.** **The pixel rule separates the renderers cleanly; the ratio rule does not, and one limit (MO8b) needs a new definition.** Every sub-pixel renderer tested has centre jitter (MO8a) of 0.001 to 0.011 px on its raw output against the 0.05 limit (two exceptions that still pass: FilmCraft's own H.264 export at 0.021 and GSAP with `force3D` at 0.044), so MO8a works on all of them. `zoompan` (0.29 through RGB, **0.63 in the usual yuv420p command line**) and CSS layout animation (0.18) fail it. **Three things to change in the playbook.** (1) GSAP's own `scale` tween fails MO8b (0.061 px, limit 0.04) because GSAP writes the transform with 4 decimals; using GSAP only for the ease and writing the transform yourself fixes it (0.005). (2) MO8b as defined (residual from a 9-frame running mean) contains the ease curve's own curvature, so a *perfect* render fails it for any 4% push shorter than about 2.5 s (0.052 px at 2 s); a 4th-difference version does not. (3) After x264 at CRF 14 even a perfect render sits at 0.025 to 0.039 px on MO8b, next to the 0.04 limit: measure MO8b on the render *before* the delivery encode (MO8a survives the codec at 0.01). (M-C10, all on one public-domain print, 2026-10-18)

**Set-up (so the numbers can be repeated).** One still: a Smithsonian NMAAHC albumen print (CC0), cut to 3840 x 2160. A cosine in-out push of 4% over 96 frames at 24 fps, 1920 x 1080 output, as in FQ2 (Blender: 48 frames and 2%, which has the same peak speed per frame, because Blender at 96 frames did not fit in the time). Every row is measured with `mo8_audit.py`: MO8a = rms of the fitted x,y translation residual, MO8b = rms of the zoom-rate residual times 960, both in 1080p pixels; "9fr" is the FQ2 definition (residual from a 9-frame running mean), "d4" is the new one (fourth difference divided by sqrt(70), exact for white jitter, curvature-free), MO8c = FQ2's relative roughness. "Raw" is the renderer's own output (PNG frames or ProRes); "x264" is the same frames after CRF 14, yuv420p, decoded.

| Renderer and setting | MO8a raw (x264) | MO8b d4 raw (x264) | MO8b 9fr raw | MO8c raw | MO8 pixel rule (0.05 / 0.04) | Ratio rule (1.3 x reference, or 0.25) |
|---|---|---|---|---|---|---|
| **References** | | | | | | |
| Pillow `resize(box)`, Lanczos | 0.0012 (0.0100) | 0.0028 (0.0294) | 0.0090 | 0.0208 | pass | the reference itself (limit 0.027) |
| Pillow `transform` EXTENT, bicubic | 0.0029 (0.0101) | 0.0096 (0.0259) | 0.0126 | 0.0290 | pass | 1.4 x: fails the ratio, passes the 0.25 floor |
| ffmpeg `zoompan` from the 4K still, RGB path through the filter (the FQ2 case) | 0.2918 (0.2814) | 0.1400 (0.1318) | 0.1121 | 0.2575 | **fail** | 12 x; 0.2575 is over 0.25 by 0.0075: a knife edge |
| ffmpeg `zoompan` from the 4K still, chain ending in yuv420p (the usual command line: `-pix_fmt yuv420p` or `format=yuv420p`) | **0.6274** | 0.1511 | 0.1300 | 0.2982 | **fail** | 14 x; 0.298 fails the 0.25 floor too |
| **Chromium, 1920 x 1080, stepped screenshots of the running page** | | | | | | |
| CSS `transform: scale()`, `will-change: transform` | 0.0037 (0.0108) | 0.0046 (0.0246) | 0.0091 | 0.0210 | pass | 1.0 x: pass |
| CSS `transform: scale()`, no `will-change` | 0.0108 (0.0134) | 0.0100 (0.0300) | 0.0122 | 0.0282 | pass | 1.4 x: passes by the floor |
| GSAP 3.12.5 `scale` tween, `will-change` | 0.0032 (0.0108) | **0.0608** (0.0728) | 0.0479 | 0.1106 | **MO8b fails** | 5.3 x: passes by the floor |
| GSAP 3.15.0, same | 0.0032 | (same as 3.12.5 to 4 decimals) | 0.0479 | 0.1106 | **MO8b fails** | same |
| GSAP `scale` tween with `force3D: true` | 0.0440 (0.0431); d4 0.0621 | **0.0613** (0.0671) | 0.0478 | 0.1104 | **MO8a borderline, MO8b fails** | 5.3 x: passes by the floor |
| GSAP supplies only the ease; page writes `scale(...)` itself | 0.0037 (0.0109) | 0.0046 (0.0269) | 0.0091 | 0.0210 | pass | 1.0 x: pass |
| CSS layout properties (`width`, `height`, `left`, `top`) | **0.1788** (0.1773) | **0.6113** | 0.4347 | 1.006 | **fail** | fails both |
| **FilmCraft 0.9.0 (Linux CLI, CPU export)** | | | | | | |
| Linear keyframes, ProRes 422 HQ | 0.0021 | (9fr 0.0025) | 0.0025 | 0.0057 | pass | pass |
| Bezier, `autoBezier`, `continuousBezier` or `easeOut:easeIn`, ProRes | 0.0020 (0.0112) | 0.0036 (0.0324) | 0.0097 | 0.0224 | pass | 1.1 x: pass |
| Built-in "High Quality 1080p HD" (H.264, 20 Mbps VBR, 1 pass), linear | 0.0212 | (9fr 0.0199) | 0.0199 | 0.0460 | pass | pass |
| **Blender 5.2.2 LTS, Cycles CPU, 32 samples (48 frames, 2%; reference: Pillow `resize(box)` at 48 frames, 2%)** | | | | | | |
| Pillow reference, same length and amount | 0.0014 (0.0103) | 0.0021 (0.0390) | 0.0253 | 0.0573 | pass | reference |
| Linear texture interpolation, no motion blur | 0.0009 (0.0106) | 0.0011 (0.0362) | 0.0262 | 0.0592 | pass | 1.03 x: pass |
| Linear, motion blur (sub-frame sampling, shutter 0.5) | 0.0008 (0.0091) | 0.0011 (0.0320) | 0.0262 | 0.0591 | pass | 1.03 x: pass |
| Cubic texture interpolation, no motion blur | 0.0008 (0.0109) | 0.0012 (0.0344) | 0.0262 | 0.0593 | pass | 1.03 x: pass |
| Closest (nearest-neighbour) texture, no motion blur | 0.0019 (0.0112) | 0.0024 (0.0251) | 0.0249 | 0.0564 | pass | 0.98 x: pass |
| `zoompan` at the same length and amount | 0.2843 (0.2729) | 0.1637 (0.1525) | 0.1102 | 0.2465 | **fail** | fails |

(The M-C7b measurements of FQ2 are the same two references on three other prints: `zoompan` 0.29 and Pillow 0.001 to 0.019. This print agrees.)

**What each renderer does and why.**
- **Chromium (Playwright 1.56.1 with its Chromium build 1194, headless, device scale factor 1).** A transform set per frame and a screenshot taken after two animation frames is as smooth as Pillow: Chromium resamples the image at sub-pixel positions on the compositor. `will-change` makes no difference to quality here (0.004 against 0.011). This is a *stepped* capture: the page is advanced by code and photographed, frame by frame. **Do not record the running page in real time.** I tried it once (Playwright's `recordVideo`, a CSS push started 0.5 s after load, VP8 at 25 fps conformed to 24 fps, on a machine with a load of about 5): the picture position is fine (MO8a 0.031) but the timing is not (MO8b 0.35 px, MO8c 0.78; 11 of 88 frame pairs barely moved and the largest step was 5.6 times the median), a visible stutter. That depends on the machine, so treat it as one observation, but it is why the pipeline steps the page.
- **GSAP.** It writes `scale(1.0203, 1.0203)` (4 decimals, read from the element's style in the capture log); a 4% push moves the scale by only 0.0004 per frame, so rounding at 0.0001 puts a random 0.03 to 0.05 px error at the picture edge. 3.12.5 and 3.15.0 (the current npm release) behave the same. The fix costs nothing: tween a plain number and write `el.style.transform = 'scale(' + (1 + 0.04 * p) + ')'` in `onUpdate`. That gives exactly the numbers of hand-written CSS (0.0046). `force3D: true` also adds a compositing-layer position error (centre jitter 0.044, d4 0.062 against 0.05): leave it at the default for slow pushes.
- **Blender.** With the image texture on Linear, sub-pixel placement is as good as Pillow (centre 0.0009, edge 0.0011 px on the raw frames). **Motion blur (sub-frame sampling) neither helps nor hurts**: 0.0008 and 0.0011 against 0.0009 and 0.0011. The smear across a half-frame shutter of a push that moves the picture edge by under 0.7 px per frame is below the jitter floor; it would matter on a fast pan, not here. (Cycles CPU took 16 to 30 s per 1080p frame at 32 samples while other jobs shared the 4 cores, so an 8-second push at 24 fps is roughly an hour of render here; I did not time it on an idle machine.) Cubic and nearest-neighbour texture sampling also pass (0.0008 and 0.0019): with a 2:1 reduction from a 4K texture the pixel filter averages about four texels, so the choice hardly shows on this move; it may on a magnified or 1:1 texture (not tested). The zoom estimator and the frames were checked against the Pillow 1080p crop: Blender's first frame differs from it by 0.6 grey levels on average, so the colour pipeline (view transform Standard, dither off) is neutral.
- **FilmCraft.** The CPU compositor places the picture at sub-pixel positions as well as Pillow does (0.002 px on ProRes). Its **built-in H.264 export** adds more than the geometry does: centre 0.021 px at 20 Mbps against 0.010 for x264 at CRF 14, still under 0.05. For a final film use the ProRes master (R6) and encode with x264, as the craft-motion note already recommends. Keyframe behaviour found on the way (0.9.0): a new keyframe's interpolation is **linear**, so an untouched Ken Burns reads `LINEAR/uniform` on MO1b; `bezier`, `autoBezier` and `continuousBezier` on two keyframes all give the same in-out curve, which the pan classifier identifies as a cubic smoothstep (FQ11); `easeIn` and `easeOut` behave like Premiere's temporal ease (J, by analogy; the observations are measured): a segment is shaped by the first keyframe's `easeOut` (leave slowly) and the last keyframe's `easeIn` (arrive slowly), so `easeIn` on the first and `easeOut` on the last do nothing and the move stays linear (the exported file was byte-identical to a linear one). `easeOut:easeIn` on the two keyframes gives the same curve as `bezier`; `easeOut:linear` and `linear:easeIn` give half-eased curves that the zoom classifier reads as `other`.

**The two rules, compared.**
- **MO8a (centre jitter, 0.05 px) holds on every renderer**: sub-pixel ones 0.001 to 0.011 raw and under 0.022 after the codec; zoompan 0.28 to 0.29; CSS layout 0.18. It does not depend on push length (Pillow: 0.0060 at 1 s, 0.0013 at 4 s, 0.0009 at 6 s) or on the codec by more than 0.01. Keep it as the primary test.
- **MO8b by the 9-frame mean depends on push length, not only on jitter.** A perfect Pillow push of 4% (generated chart still, raw frames): 0.304 px at 1 s, 0.052 at 2 s, 0.019 at 3 s, 0.009 at 4 s, 0.004 at 6 s. The d4 version of the same pushes reads 0.016, 0.0035, 0.0025, 0.0019 and 0.0014. `zoompan` reads 0.11 to 0.17 by d4 at every length (generated chart still, raw frames, `mo8_push_length.py`). **Replace the MO8b estimator by d4** (curvature-free); keep 0.04 px as the limit; it separates GSAP's `scale` tween (0.061), force3D (0.061), `zoompan` (0.14) and CSS layout (0.61) from everything else (at most 0.0100 raw). **Measure it on the master before the delivery encode:** after x264 CRF 14 perfect renders read 0.025 to 0.039 by d4.
- **MO8c and the ratio rule are fragile** (confirming FQ2). The reviewer's rule (no more than 1.3 times a sub-pixel reference's roughness, or 0.25 absolute) passes the GSAP tween that MO8b fails, and puts `zoompan` at 0.2575 against 0.25, a 0.0075 margin. Relative roughness also changes with push length and codec (the Pillow reference reads 0.021 raw and 0.056 after x264 at 4 s, 0.057 and 0.087 at 2 s), so "1.3 times the reference" has to be measured per shot length and per codec. Use it as a screening aid only.
- **`zoompan` doubles in the usual command line.** With the input a PNG and the chain ending in yuv420p, ffmpeg negotiates the pixel format back through `zoompan`, which then crops a chroma-subsampled picture at even source pixels; centre jitter 0.6274 against 0.2903 when the filter works in RGB (`zoompan_pixel_format.py`; the cause is my reading, the two numbers are measured). FQ2's 0.29 is therefore the *best* case for `zoompan`.
- **Estimator check.** The zoom estimator reads a 4% push as 4.27 to 4.31% on every renderer, Pillow included (a 7% over-read common to all), so it is a relative tool, not a ruler. It classifies every cosine push as `ease in-out`, and FilmCraft's linear keyframes as `LINEAR/uniform (flag)`.

**Limits.** One print, one push profile (cosine, 4% in 4 s; Blender 2% in 2 s). I did not test: Blender at 96 frames or with an orthographic camera, EEVEE (no GPU here), Chromium with a GPU, a Windows build of any of them (FilmCraft's Windows build is the same Rust engine; run `filmcraft_push.py` with `FILMCRAFT_CLI=...\filmcraft-cli.exe` to confirm), a pan or an orbit, or anything projected. The `will-change` and `force3D` differences are observations on this software-rendered headless Chromium; the cause (compositor raster scale) is my reading, not tested.

### FQ11. A pan ease classifier: velocity curve from the phase-correlation vectors to an ease class (MO1b, MO2, MO9 for pans)

**Answer.** `pan_ease_classifier.py` (numpy only, beside `pan_estimator.py`) turns the vectors that the MO6 estimator already produces into an ease class, a six-way family and a playbook family key. On **114 synthetic pans with known easing** it named the exact easing template and the family on **100 of 100 single-layer clips built from named eases** (clean, grain plus H.264, footage on twos, integer-step camera paths, tilts and the opposite direction, slow 3 px/frame drifts, 2 s, 4 s and 6 s clips, two different prints), never raised its low-confidence flag on them, and recovered the pan's total travel to a mean of 1.3 px (at most 5.2 px) out of 100 to 1,570. On curves it does not have in its library (five CSS `cubic-bezier` timing functions) it got the family right on 4 of 5 and flagged the fifth as low confidence. With two layers moving at different speeds it still got the family on 4 of 4 and the exact template on 3 of 4. MO1b and MO2 can therefore report pass or fail for translation-only pans instead of `unknown`; MO9 can count pan families from pixels. (M-C11)

**How it works.**
1. `estimate_pan` gives, for every frame pair, the fastest textured layer's vector (3 x 3 tiles of phase correlation; twos handled by comparing frames two apart).
2. The vectors are projected on their principal axis to a signed speed per frame; a 3-point median removes one-frame dropouts.
3. The speed is summed into a position curve, normalised to 0 to 1. Summing is the point: the 0.02 px/frame speed noise of FQ3 averages out in the position, which is why shapes that differ by 1% of travel can be told apart.
4. Nineteen named curves (linear; `sine`, `power1` to `power4` in, out and in-out as GSAP names them; `expo.out`; `smoothstep` = 3u^2 - 2u^3; `smootherstep`; `back.out(1.7)`) are fitted by least squares, each allowed a hold at the start and at the end (`p(t) = T(clip((t - a) / (b - a), 0, 1))`). The best fit is the class. Its family comes from a table: in-out, out, in, settle, linear. `mo_verdicts` maps a hold of 25% or more at either end to the `hold-snap` family.
5. A second, template-free rule (start and end speed against peak, where the peak falls, reverse travel) votes on the family. If it disagrees with the fit, or the fit's rms error is over 0.05, or the next-best curve of another family is within 15%, the result is flagged `low_confidence` and MO1b and MO2 say `unknown` for that move only.
6. The family key is the playbook's: (ease family, axis, duration bucket, magnitude bucket). Axis is `pan left` when the content moves right (the estimator's convention), `pan right`, `tilt up` or `tilt down`; magnitude is the total travel as a percentage of the frame width (pans) or height (tilts); durations under 3 s, 3 to 6 s, over 6 s. `mo9_check(keys)` applies the chapter rule to a list of keys (8-shot windows: at least 3 distinct keys, none above 40%, no key more than twice in a row, entropy of at least 1.5 bits) and `mo_verdicts(c, brief_family, drift_declared)` gives MO1b and MO2. Unit-checked on made-up chapters: eight varied keys pass (7 distinct, 2.75 bits); eight of the same key fail (1 distinct, 0 bits).

**Validation.** Each clip is a 1080p window sliding 1:1 over a 3840 x 2160 print (Smithsonian NMAAHC, CC0), so every sub-pixel step is a Lanczos resample, normalised to a peak of 11 px per frame (0.1375 frame widths per second, under the MO6 limit) unless noted. The truth easings are the library's own, so the first table measures whether the *measurement chain* (resampling, grain, codec, rounding, twos) keeps the shapes apart, not whether the library is right for curves outside it; the second table is that.

| Group | Clips | Exact template | Family | Axis | Low-confidence flags | Mean error in total travel |
|---|---|---|---|---|---|---|
| Clean, Lanczos sub-pixel (16 curves, plus 4 smoothstep-library runs) | 20 | 20 | 20 | 20 | 0 | 0.9 px |
| Grain (sigma 2) plus H.264 CRF 18 | 20 | 20 | 20 | 20 | 0 | 2.0 px |
| On twos (one drawing per two frames) | 16 | 16 | 16 | 16 | 0 | 0.4 px |
| Integer-step camera path (what ffmpeg `crop` gives) | 16 | 16 | 16 | 16 | 0 | 1.2 px |
| Tilt (vertical) and opposite direction | 8 | 8 | 8 | 8 | 0 | 0.5 and 0.8 px |
| 2 s (48 frames), 6 s (144 frames), slow (3 px/frame peak), second print | 20 | 20 | 20 | 20 | 0 | 0.3 to 3.8 px |
| **Total, in-library single layer** | **100** | **100** | **100** | **100** | **0** | **1.3 px (max 5.2)** |
| Two layers (background half the speed of a foreground blob) | 4 | 3 | 4 | 4 | 0 | the fast layer is tracked only part of the time: error 146 px of about 1,000 |
| CSS timing functions (`ease`, `ease-in`, `ease-out`, `ease-in-out`, a back-out), clean and grain plus H.264 | 10 | 0 of 10 by design (nearest curve named) | 8 | 10 | 2 (both `ease`) | 1 to 2 px |

The 16 curves were: linear; `sine.inOut`, `power1.inOut`, `power2.inOut`, `power3.inOut`, `smootherstep`; `sine.out`, `power1.out`, `power2.out`, `power3.out`, `expo.out`; `sine.in`, `power2.in`; `back.out(1.7)`; a 25% hold then `power2.inOut`; `power2.out` then a 25% hold. The holds were recovered to within 0.06 of the clip in every case. Detail worth knowing:
- **Near-twins are separated.** `smoothstep` and `sine.inOut` differ by at most 1.0% of travel; both clean and with grain plus H.264 they were told apart (fit error 0.0002 to 0.0005 against 0.0067 for the twin). I would not rely on that on real, parallaxed footage; the *family* is the dependable answer and the template name is a bonus.
- **CSS `ease`** (`cubic-bezier(0.25, 0.1, 0.25, 1)`, the browser default) has a quick start and a long tail; the fit says `power1.out` (out) and the template-free rule says in-out, so the clip is flagged `low_confidence` and the verdict is `unknown`, not a wrong pass. `ease-in` came back `sine.in`, `ease-out` `sine.out`, `ease-in-out` `sine.inOut` and the back-out `back.out(1.7)` (settle).
- **Two layers.** The classifier follows "the fastest textured layer" because MO6 does. When the fast layer is only intermittently matched, the speed curve mixes the two layers and the fit error rises from 0.0002 or 0.0005 (one layer) to between 0.0105 and 0.044, with the travel under-estimated. The family was still right in all four. Layers with *different* eases are not handled (measure those from the timeline spec).

**Real renderers' pans.** FilmCraft 0.9.0, a 760 px pan from keyframes at 1:1 on a 3840-wide still (ProRes, then x264 CRF 14): linear reads `none (linear)`, error 0.0, total 759.8 px (truth 760); `autoBezier` reads `smoothstep`, in-out, fit error 0.0003, peak 12.0 px/frame (1.5 times the mean, the Hermite smoothstep's peak), total 763 px. So **FilmCraft's Bezier on two keyframes is a cubic smoothstep** and its default keyframe interpolation is linear (see FQ10). Its 12 px/frame peak is over the MO6 limit of 11.43 for a 760 px pan in 4 s, which the estimator reported as FAIL, as it should.

**Limits (what this does not show).**
- The truth curves come from the same library the classifier fits, except the five CSS curves; a human-authored spring or a hand-drawn curve is out of the tested set and will be named after the nearest library curve (check `rmse`: under 0.02 is a good fit, over 0.05 sets the low-confidence flag).
- Translation only. A zoom or rotation mixed into the pan reads as speed at the tile edges (FQ3); orbits and multi-plane moves with different eases per layer stay `unknown` (use the spec).
- Pans under 0.5 px/frame report `static` (nothing to classify). The clips here are 2 to 6 s; shorter than 1 s was not tested.
- Pan *segments* cut from a longer move classify the segment, not the move.
- Real hand-drawn layers, real family scans with film grain and a real parallax pan were not used; the two prints are 1.5 to 1.8 times up-sampled archival scans.
- Speed: 10 to 140 s per clip depending on how loaded the container was (mean 42 s); that is the estimator, not the classifier, which takes milliseconds. The estimator's memory was cut so that 144-frame clips fit (a first 144-frame run was killed by the container's memory limit; the rerun after the fix completed).

### FQ12. The six venue answers (FQ7): still OPEN, now a fill-in sheet and a calculator

**Status: OPEN. Only the maker can answer; nothing here was invented.** Until they arrive, every brightness, gamma, black-level, type-size, jitter-in-arc-seconds and STI number in this note and in D5 stays a scenario. The maker is the only person on the project, so the venue's AV contact is the one outside person to ask, and the questions below say nothing about the film. A neutral ask, usable as written: "We are planning to show a short video at a family event on 27 February 2027. Could someone tell me the projector or display model, how it is connected (HDMI, USB, other), the width and height of the lit picture, and whether the room can be darkened? Could we do a 30-minute test with our own laptop on a weekday, two to three weeks before?"

| # | Ask (and how the maker gets it) | Fills in |
|---|---|---|
| 1 | **Playback path:** DCP on a cinema server, laptop or player over HDMI, or USB into the venue's player or TV. Ask the AV person. | `playback` (gamma 2.6, 2.4 or 2.2) |
| 2 | **Screen:** lit picture width and height in metres (tape measure), projector screen or TV and its size in inches. | `screen_width_m`, `picture_height_m` |
| 3 | **Projector or display:** photograph its label (model, lamp or laser hours, native 1080p or 4K). | `projector_lumens`, `native_height_px` |
| 4 | **Darkening:** can it be darkened; a lux reading on the screen with the lights as at the event (phone app; the sensor is uncalibrated, use it for ratios). | `ambient_lux_on_screen` |
| 5 | **Who runs AV** and whether a weekday test is possible at least two weeks before 27 February (also the slot for the A/B card, FQ9). | the test date |
| 6 | **Sound and seats:** the PA, who controls it, stereo or 5.1, a hearing loop, **seat count and the nearest and farthest seat distance in metres.** | `nearest_seat_m`, `farthest_seat_m` |

**`venue_calc.py` (M-C14).** Put the answers in a small JSON file and run `python3 -I venue_calc.py venue.json`. It prints peak luminance (lumens x 0.75 lamp derate x gain / (pi x area)), the grading gamma, the signal level hidden by the ambient light, the nearest and farthest seats in screen heights, the type-size floors (x-height 0.525% of picture height per screen height of distance, from Q10), arc seconds per pixel at both seats, and what 0.05, 0.1 and 0.3 px of jitter subtend there. It lists the defaults it still used. Worked example (a scenario, not the venue): 6 m wide, 3,000 lm, 2 lux, seats at 5 m and 16.9 m gives 35 cd/m2 (0.74 of the 48 reference), gamma 2.4, signal below 19% hidden, x-height floor 2.6% and font floor 57 px at 1080p, and 0.3 px of jitter is 39 arc seconds at the front and 11 at the back.

**What the maker should send back:** the filled sheet (or the six answers in a line each), plus a phone photo of the projector label. The scribes then replace every "scenario" tag in D5 with the venue's numbers.

### FQ13. Adobe Fonts and Monotype: do the rights to a rendered film survive the subscription ending?

**Answer in one line.** **Neither vendor's terms say a finished film may still be shown after the subscription ends, and both tie the licence to the subscription.** Adobe's licensing FAQ is still unreadable to the fetch tool (HTTP 403 again), but I found and read Adobe's binding terms by another route. Treat the film's rights to a commercial font as ending with the subscription, keep paying through the last planned screening, or use OFL fonts (FQ4) for everything on screen. Read 2026-10-18; I am not a lawyer.

**Adobe Fonts (binding terms read in full: "Adobe Fonts Service Product Specific Terms", effective 7 October 2024, "Replaces all prior versions") [109].** The FAQ page `helpx.adobe.com/fonts/using/font-licensing.html`, which the Adobe Fonts home page links as "Adobe Fonts Licensing FAQ", returned 403 again [90]. Adobe's General Terms page links the real terms through `adobe.com/go/adobe-fonts-terms`; that redirects to a PDF that the fetch tool saved and I read as text [109][110].
- **3.1, the grant.** "a nonexclusive, non-assignable, non-transferable, limited right and license to access and use the Licensed Fonts in and in connection with the design and development of Media according to the permissions assigned to the Licensed Fonts on the Adobe Fonts website, and **only for as long as you maintain an uninterrupted Adobe Subscription Plan**."
- **1.5 and 1.11, what "Media" is.** "Media" is a "Document or Website"; a "Document" is "any form of electronic document, whether or not publicly distributed, that uses Desktop Fonts, whether or not embedded". A rendered video file is not named. The terms never use the words video, film, broadcast or exhibition. The home page's marketing line "Video and Broadcast: Use fonts to create in-house or commercial video content" is the only video statement I have, and it is not in the terms [90]. Whether an MP4 counts as a "Document" is unclear (J).
- **2.2(C), what cancelling does.** Cancelling a paid plan moves the account to the free plan; "you will continue to have access to the Marketplace Fonts that you purchased" (only those). Fonts offered only on paid plans (2.2(A)) go.
- **3.4(E)(2) and (3).** No "including, bundling, embedding, or otherwise distributing any Licensed Content within your Media" except under 3.1(A) (documents, subset and obfuscated); no "external output of the Licensed Fonts". A font file must not travel with the film.
- **4.2(A), the only survival-type clause, and it is about Adobe's suppliers.** "If the relevant agreements between us and our Licensors terminate, you will still be able to use the Licensed Content in your Media, unless we provide you with notice of termination." It does not cover the user's own subscription ending.
- **Not answered anywhere I could read:** what happens to a film rendered while subscribed and shown after cancelling. The FAQ may answer it. **Maker (5 minutes, in a browser):** open the FAQ and find (a) whether "video" use includes a public showing in a hall or cinema, (b) whether exported video made while subscribed may still be shown after the subscription ends. Paste the two sentences into the rights log.

**Monotype Fonts (three agreements re-read from the publisher's feed for the term and termination clauses) [88][89].**
- **Create + Deploy.** The Term is one year from acceptance and "shall automatically renew for subsequent one (1) year renewal terms ... (unless terminated pursuant to Section 5)". Every grant, including "Distribute up to five thousand (5,000) ... Units of Video Content annually", is "during the Term". Section 5 lets either party terminate only for an uncured breach. **There is no clause saying what happens to output after the Term, and none that preserves it.**
- **Create + Pitch.** The same Term and termination text; its video grant is for pitching only and excludes public deployment (FQ4).
- **Enterprise.** "The rights of a recipient of a Licensed Application generated pursuant to this Agreement shall survive the termination of this Agreement. **All other license rights granted to you in this Agreement shall end with the termination of this Agreement.**" A film is not a "Licensed Application" (defined as "Any Application up to the number of Applications indicated in your Account"), so on this text the film's font rights end with the agreement. Expiry at the end of a term is covered by "terminate" in the same paragraph (J), and the paragraph allows reinstatement "in its sole discretion".

**Decision rule (J), replacing the FQ4 line "render and archive the master while the subscription is active".**
1. Prefer OFL fonts for everything on screen. Nothing expires.
2. A commercial font is used only if the subscription is in force on **every date the film will be shown**: 27 February 2027, any rehearsal, and any later screening. Put the renewal date in the rights log (T8 `fonts` sheet) with the screening dates beside it; renew, do not lapse.
3. Burned-in text is pixels, so the archived master keeps looking right whatever happens to the account, but showing it may be outside the licence after lapse. That is a licence risk, not a technical one. Keep a version of the cinema cut with OFL replacements ready to re-render.
4. Ask each vendor, in writing, the one question the terms leave open: "May a film rendered with your font during my subscription be shown publicly after the subscription ends?" Keep the answer with the font's licence file (TY3).

### FQ14. First-hand accounts by relatives who objected to an animated portrait of their dead; the Kopelman and Frosh body text

**Answer in short.** **The search pass could not be run** (the shared web-search budget was spent before this task started, and I did not work around it), so this is a direct-fetch pass. Result: **still no first-hand account by a relative who objected to a *photograph* of their own dead being animated.** I did find first-hand objections by relatives to AI likenesses of famous dead people (voice and generated video), through secondary pages only; these are adjacent, not the same case. The Kopelman and Frosh body text is not readable by the tools here, and the paper that would help most (Kidd and Nieto McAvoy, 6,935 posts) is blocked the same way. The standing rule is unchanged: no face animation of the dead in the premiere cut. Read 2026-10-18.

**Where the body texts are, and why I could not read them.**
- **Kopelman and Frosh, *New Media & Society* 27(4)** is open access ("hybrid", licence CC-BY-NC, published version, one location only) per its OpenAlex record [111]. `doi.org` redirects to `journals.sagepub.com/doi/10.1177/14614448231210268`; both that page and `/doi/pdf/...` returned HTTP 403 to the fetch tool [95]. **Maker: it is free to read in a browser at the DOI.** Look for quoted tweets and press comments from people who found the animations disturbing or disrespectful, and note who they are (relative, stranger, journalist).
- **Kidd and Nieto McAvoy, "Deep Nostalgia: Remediated memory, algorithmic nostalgia and technological ambivalence", *Convergence* 29(3), 2023** [112]: analyses 6,935 Twitter posts from the two weeks after launch, on "emotional resonances" and "ambivalence". OpenAlex lists it as open access (CC-BY-NC) at SAGE and at Cardiff ORCA; the SAGE PDF and the ORCA PDF and record both returned 403, and the King's College London page has no file. This is probably the best published source of first-hand tweets, and it is unread. Maker: free in a browser at `doi.org/10.1177/13548565221149839`.
- Five other open-access papers that cite Kopelman and Frosh were downloaded and keyword-checked for objection language (objected, uncomfortable, disrespect, offended, refus-, upset, creepy) and for relatives, interviews and consent [113]: "Yearning for a You" (MedieKultur 2024), "Synthetic afterlives" (Kidd and Nieto McAvoy, *Memory, Mind & Media* 2025), "Co-construction with deathbots" (*Humanities and Social Sciences Communications* 2025), "Technonecromancy" (*Trilogía* 2026) and a 2026 paper on generative AI and relational archives. They are about deathbots, platforms and ethics frameworks; none quotes a relative objecting to an animated photograph. "Technonecromancy" argues for "consent-first defaults" and "data wills" for the dead, which is design guidance, not evidence of family reactions.

**First-hand objections by relatives to AI likenesses of the dead (adjacent cases; every news original was blocked, so these come through Wikipedia's summaries of them) [114].**
- *George Carlin, 2024.* His daughter Kelly Carlin is quoted (TheStreet, Ian Krietzberg, 11 January 2024, as listed in Wikipedia's reference): "My dad spent a lifetime perfecting his craft from his very human life, brain and imagination", "No machine will ever replace his genius", and "Humans are so afraid of the void that we can't let what has fallen into it stay there." The estate sued over an AI-voiced special and settled after the hosts removed the video (Hollywood Reporter, 2 April 2024, per Wikipedia).
- *Robin Williams, October 2025.* His daughter Zelda Williams "has spoken out against AI-generated" videos of her father after OpenAI's Sora launched; the Guardian headline she is quoted in is "stop doing this to him" (7 October 2025, per Wikipedia). I did not read her words. Wikipedia's Sora article says families of Robin Williams, Kobe Bryant, Paul Walker and George Carlin urged OpenAI to act against "hurtful videos" (Axios, 8 October 2025), and that estates threatened legal action (BBC Bitesize, 10 October 2025).
- These are famous dead people, generated video and voice rather than an animated still, and mostly public statements to a company. They show that relatives do object, publicly and in strong terms, when someone else makes the likeness. They do not show how a mother reacts to her own parent animated by her child at a surprise premiere.

**What it means for this film (J).** Nothing changes: the mother is the next of kin of her own late parents, nobody can ask her in advance, and the one first-hand pattern in the record (relatives object when the likeness is made without them) is the situation a surprise creates. Environment and parallax motion only; no animated faces, eyes or mouths of the dead. A follow-up message with search available should look for: first-hand relatives' posts on Deep Nostalgia (Reddit, Twitter archives, genealogy forums), grief-counsellor commentary, and Zelda Williams's own words from a source that can be fetched.

### FQ15. Windows check: `caption_xheight.py`, `zoom_velocity_classifier.py` and `pan_estimator.py` on the maker's PC (M-C12)

**Status: NOT RUN on the maker's PC, and it cannot be from here** (no access to the machine, GUI control is not connected, and the container has no Windows or Wine). What is ready: **one command that runs all of it, records every version, and says PASS or CHECK for each step**, tested end to end in the container. The maker runs it once and sends back one JSON file. UNVERIFIED on Windows until then.

**What the maker does (about 5 minutes of set-up, then 2 to 5 minutes of running on a 4-core machine; the container's five steps took 114 s in total).**
1. Have Python 3.10 or later (python.org or the Microsoft Store), then `py -3 -m pip install numpy pillow`. Have an ffmpeg with libass and libx264 (the report says whether yours has them). Choose the caption font file (for example `C:\Windows\Fonts\arial.ttf`) and its family name as Windows shows it ("Arial").
2. Copy the fixtures folder (`research/cinematic-quality-fixtures`) to the PC, open PowerShell in it, and run:
   `py -3 -I windows_check.py C:\LJ\check --font "C:\Windows\Fonts\arial.ttf" --font-name "Arial" --ffmpeg "C:\tools\ffmpeg\bin\ffmpeg.exe"`
   (`--quick` halves the clip lengths.) Nothing personal is used: it generates its own test picture.
3. Send back `C:\LJ\check\windows_check_report.json`.

**What it checks and what a pass means.**

| Step | Script | Pass means |
|---|---|---|
| 1 | `caption_xheight.py` with the maker's font | x-height of `FontSize` 20, 23 and 26 at 1080p is within 0.25 points of what the font's own metrics predict, i.e. libass used that font and not a substitute. Gives the caption sizes for TY1 in the maker's font (container, DejaVu Sans: 3.27 / 3.80 / 4.26%). |
| 2 | `zoom_velocity_classifier.py` (with `ZV_SIZE=1920x1080`) | A `zoompan` push reads at least 1.5 times rougher than a Pillow push on the maker's ffmpeg and numpy |
| 3 | `mo8_audit.py` | Pillow push centre jitter at most 0.05 px and `zoompan` at least 0.15 px |
| 4 | `pan_estimator.py` | Pans of 8, 11.43 and 16 px/frame read within 0.3 px |
| 5 | `pan_ease_classifier.py` | A cosine in-out pan reads as the in-out family |

Versions recorded: Windows build, Python, numpy, Pillow with its FreeType version and whether it has Raqm, ffmpeg's version line, its full configuration line (libass, fontconfig, libx264, harfbuzz), library versions, whether the `subtitles` and `zoompan` filters exist, SHA-256 and size of the ffmpeg executable and of the font file, the font's family and style names. The SHA-256 values identify the exact build in the repo log.

**Changes made so that it works on Windows (each verified on Linux).**
- `caption_xheight.py` put the absolute path of the `.srt` file into the `subtitles=` filter string; on Windows `C:\...` has a colon that ffmpeg's filter parser takes as an option separator, so it would very likely have failed (expected from ffmpeg's filter-escaping rules, not tested on Windows). It now runs ffmpeg inside the work folder with relative names, accepts `FONT_FILE FONT_NAME` (copied to `fonts/` and passed with `fontsdir=`), and compares the measurement with the font's metrics so a silent fall-back to another font is reported. Its default output over the five Linux fonts is identical to round 1 (36 of 36 rows equal); a deliberately wrong family name is caught (measured 3.18% against 2.72% expected for Carlito).
- `pan_estimator.py` computed the FFTs of all frames before using any (about 17 MB a frame, so 2 to 4 GB for 96 frames, and a 144-frame run was killed by the container's memory limit). It now keeps only the frames in use; output is bit-identical on a test clip (both `dt` values), a 144-frame clip that was killed before now completes.
- `mo8_audit.py` converts to luma and downsamples one frame at a time (about 3 GB less for 96 frames; identical numbers). `windows_check.py` and `ab_push_card.py` stream frames to ffmpeg one at a time.
- The runner makes the ffmpeg path absolute (the sub-scripts change directory), puts the maker's ffmpeg first on `PATH` for the scripts that call plain `ffmpeg`, sets `ZV_SIZE` itself, and uses `sys.executable -I` for every sub-script.

**Container result for comparison (Linux, full length, ffmpeg 6.1.1-3ubuntu5, Python 3.13.16, numpy 2.5.3, Pillow 12.3.0 with FreeType 2.14.3, DejaVu Sans):** all five steps PASS in the full-length run (steps took 6, 44, 10, 29 and 25 s). (1) x-height 3.27 / 3.80 / 4.26% for `FontSize` 20 / 23 / 26, gap to the font's metrics at most 0.05 points. (2) Zoom classifier roughness Pillow 0.020, `zoompan` 0.321 (ratio 16). (3) MO8 audit: Pillow centre jitter 0.0033 px, `zoompan` 0.6274 px (the runner's chain ends in yuv420p, which doubles `zoompan`'s error; FQ10), 4th-difference edge jitter 0.0095 against 0.1511. (4) Pan estimator: 8.0, 11.43 and 16.0 px/frame read 8.001, 11.462 and 16.001. (5) Cosine in-out pan read as `sine.inOut`, family in-out, fit error 0.0002. The report (`r2_windows_check_container_report.json`) also records ffmpeg 6.1.1-3ubuntu5 with libass, fontconfig, harfbuzz and libx264, SHA-256 of the ffmpeg binary and of the font file. An earlier quick run caught a real fault in the runner: a regular grid of lines in the generated test picture made the translation estimator read 0.053 px of jitter on a perfect push, so the picture is now aperiodic.

**Windows hazards still open (UNVERIFIED).** (a) libass on Windows builds may select fonts through DirectWrite or fontconfig; `fontsdir=` should make the choice moot but the report's step 1 is the proof. (b) A font with a different `hhea` and OS/2 metric disagreement (Verdana, some Calibri versions) can make the "expected" figure differ from what libass draws; step 1 will then say CHECK even though the measurement is right, so read the measured numbers first. (c) 8 GB machines: the push steps hold a 96-frame clip in memory (about 0.6 GB as 8-bit RGB, plus the copies the encoder needs), so expect 1 to 2 GB at the peak; close other programs. (d) `py -3 -I` ignores `PYTHONPATH`; if numpy lives in a virtual environment, activate it first.

### Deltas for the scribes (follow-up round 2)

1. **MO8 (FQ9, FQ10).** (a) MO8a stays: centre jitter at most 0.05 px, now described as "below the best-case alignment threshold at every seat (8 arc seconds, UNVERIFIED for moving pictures) until the venue card says otherwise". (b) Redefine MO8b with the fourth-difference estimator (`mo8_audit.py`: `mo8b_d4_px`), limit 0.04 px, measured **on the master before the delivery encode**; the 9-frame version fails perfect 4% renders shorter than about 2.5 s. (c) Keep MO8c (relative roughness) informational only; the reviewer's "1.3 x reference or 0.25 absolute" rule passes the GSAP tween that MO8b fails and cannot tell `zoompan` from a pass at 0.2575 against 0.25. (d) The pipeline tool for MO8 is `mo8_audit.py` for any renderer's output; add its one-line run to the G2 gate.
2. **Renderer rules (FQ10).** GSAP: use it for the ease only and write `style.transform` yourself (GSAP's own `scale` tween writes 4 decimals and fails MO8b); no `force3D` on slow pushes; never animate `width`, `height`, `left` or `top` for a push. Chromium capture is by stepping the page and screenshotting, never by real-time recording. Blender: image texture on Linear, motion blur optional (no effect on a slow push). FilmCraft: new keyframes are linear, so set `bezier` (or `autoBezier`) on both keyframes of every Ken Burns; `easeOut` on the first and `easeIn` on the last also work; its built-in H.264 export is fine for proofs only (final: ProRes then x264).
3. **Pan checks (FQ11).** MO1b and MO2 for translation-only pans: use `pan_ease_classifier.py` (`mo_verdicts`); report `unknown` only when it sets `low_confidence`, for orbits, rotations, mixed zoom and pan, and layers with different eases. MO9: pans get family keys from `family_key`; `mo9_check(keys)` applies the chapter rule. Add the pan classifier to the Level 2 audit list in the SKILL.
4. **T6 / D5 (FQ9, FQ12).** Add `ab_push_card.py` output to the test card and the sheet it writes to the venue procedure; add the six venue answers and `venue_calc.py` to the surprise-ops "ask the venue" step; every brightness, gamma and type-size figure keeps the "scenario until answered" tag.
5. **Fonts (FQ13).** Rights playbook `fonts` sheet: add columns "subscription renewal date" and "dates the film is shown"; rule: a commercial font is used only if the subscription is in force on every showing date, because neither Adobe's Product Specific Terms (7 Oct 2024) nor Monotype's Create + Deploy, Create + Pitch or Enterprise agreements preserve any right after the subscription or term ends. Adobe: the maker reads the FAQ in a browser and pastes the two answers.
6. **The dead (FQ14).** Rule unchanged. Add to the reading list for the maker: Kopelman and Frosh (free at the DOI) and Kidd and Nieto McAvoy 2023 (free at its DOI). Add the adjacent first-hand objections (Kelly Carlin 2024; Zelda Williams 2025) as context for why the mother, not the maker, is the first person to ask after the reveal.
7. **Windows (FQ15).** Add `windows_check.py` to the maker's setup list (after Python, numpy, Pillow and ffmpeg are installed); record its JSON in the repo as `build_info`. Note for the toolchain playbook: `caption_xheight.py` now takes a font file and name, and fails loudly if libass substituted another font.
8. **craft-motion (spike S1).** The FilmCraft Linux CLI 0.9.0 runs in the cloud container: SHA-256 matches the release list (`ea67953c...1632`), `--version`, project, import, sequence, place, keyframes, ProRes and H.264 export all worked headless, 96 frames of 1080p ProRes in 24 to 37 s on 4 cores (2.6 to 4 fps, while other jobs ran). Update R8: T1 and parts of T2 are done; Windows parity is untested.

### Tools, services and costs added this round (as of 2026-10-18)

- All free. FilmCraft 0.9.0 (Linux CLI, 70 MB tarball, MIT or Apache-2.0 per the project), GSAP 3.12.5 and 3.15.0 from npm, Playwright-core 1.56.1 with the Chromium build 1194 that is installed in the container, Blender through the `bpy` 5.2.2 LTS wheel (installed in the container earlier in this session). Nothing was bought and no personal material left the container; the fetches were public pages and public-domain images.
- A Windows PC needs Python 3.10 or later with numpy and Pillow (all free) and an ffmpeg build with libass and libx264 for `windows_check.py`; `fontTools` is optional.
- Disk: the container had under 1 GB free throughout, which limited how many frames could be kept; every clip was deleted after measurement.

### Open items after round 2

1. **Maker, venue:** answer the six questions in FQ12 (and send the label photo). Book the weekday test slot and run `ab_push_card.py`'s card with the real projector from the front and back rows (15 minutes); fill in the sheet; send the sheet and the key back.
2. **Maker, Windows PC:** run `windows_check.py` once (FQ15) and send `windows_check_report.json`.
3. **Maker, browser reads (free):** Adobe Fonts licensing FAQ (two answers, FQ13); Kopelman and Frosh and Kidd and Nieto McAvoy (FQ14).
4. **Search pass still needed** (the web-search budget was spent before this task): the literature on the visibility of random frame-to-frame position jitter and of sub-arc-minute edge flicker in moving imagery; first-hand relatives' posts on animated portraits of the dead; Zelda Williams's own words from a fetchable source; California Civil Code 3344.1 and the 2024 digital-replica amendment; the IEC 60268-16 mapping from a primary source; an Android STIPA app.
5. **Run once with a GPU or on Windows, not done:** FilmCraft and Chromium on the maker's PC through `filmcraft_push.py` and `css_gsap_capture.js` (the latter needs Node and Playwright; skip unless a browser-made shot is planned).
6. **Scribe:** apply the deltas above; update `ai-imagery.md` / `agent-pipeline.md` MO8 text; put `mo8_audit.py`, `pan_ease_classifier.py`, `ab_push_card.py` and `windows_check.py` into the `cinematic-quality-bar` skill's tool list.

### New sources (round 2), continuing the numbering

Labels as above. "Read in full" means I read the whole document or page text as served; "summary only" means the fetch tool returned its own summary of the page; "403" means the tool or `curl` was refused and the page is unread. All retrieved on 2026-10-18. Sources [88] to [90], [95], [97] and [107] were used again (Monotype terms and term clauses re-read, Adobe Fonts home page, Kopelman and Frosh record, the OpenAlex citing list, the two Smithsonian prints).

- [109] Adobe Fonts Service Product Specific Terms, effective 7 October 2024, "Replaces all prior versions" — https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Adobe-Fonts-Product-Specific-Terms-en_US-20241007.pdf — reached through `https://www.adobe.com/go/adobe-fonts-terms` (301 redirect); the PDF was saved by the fetch tool and read in full as text with `pdftotext` (sections 1.5, 1.11, 2.2, 3.1, 3.4, 4.2).
- [110] Adobe General Terms of Use page — https://www.adobe.com/legal/terms.html — summary only; used to find the links to [109] and to the Creative Cloud fonts FAQ (`adobe.com/go/cc-fonts-faq`, which redirects to a page about uploaded customer fonts and was not read). The Adobe Fonts licensing FAQ `https://helpx.adobe.com/fonts/using/font-licensing.html` (linked from [90]) returned 403 again.
- [111] OpenAlex record for Kopelman and Frosh (DOI 10.1177/14614448231210268): hybrid open access, licence cc-by-nc, published version, one location — https://api.openalex.org/works/doi:10.1177/14614448231210268 — read. `https://doi.org/10.1177/14614448231210268` redirects to `https://journals.sagepub.com/doi/10.1177/14614448231210268`; that page and `.../doi/pdf/10.1177/14614448231210268` returned 403.
- [112] Kidd and Nieto McAvoy, "Deep Nostalgia: Remediated memory, algorithmic nostalgia and technological ambivalence", *Convergence* 29(3), 2023, DOI 10.1177/13548565221149839 — OpenAlex record https://api.openalex.org/works/doi:10.1177/13548565221149839 (open access, cc-by-nc; 6,935 Twitter posts) and the King's College London record https://kclpure.kcl.ac.uk/portal/en/publications/0134ea9b-6f1f-41c0-836a-9c68411b837b (abstract; no file). The SAGE PDF and `https://orca.cardiff.ac.uk/id/eprint/155369/6/13548565221149839.pdf` returned 403; body unread.
- [113] Five open-access papers citing [95], downloaded and keyword-checked (full text, not read line by line): "Yearning for a You", *MedieKultur* 2024, DOI 10.7146/mk.v40i76.141132; "Synthetic afterlives: Deathbots as affective infrastructures of memory", *Memory, Mind & Media* 2025, DOI 10.1017/mem.2025.10013; "Co-construction with deathbots: a form of existentialist practice", *Humanities and Social Sciences Communications* 2025, DOI 10.1057/s41599-025-04876-y; "Technonecromancy: Simulacra of Presence and the Politics of Death in the Age of Generative Artificial Intelligence", *Trilogía* 2026, DOI 10.22430/21457778.3723; "How generative AI transforms relational archives into simulations of living persons", *Discover Artificial Intelligence* 2026, DOI 10.1007/s44163-026-02249-1. The URLs are the `open_access.oa_url` values in the OpenAlex citing list [97]. The Wiley survey [97] and the MDPI "postmortem avatar" paper returned 403.
- [114] Wikipedia, "Sora (text-to-video model)", "George Carlin: I'm Glad I'm Dead" and "Zelda Williams" (secondary): https://en.wikipedia.org/wiki/Sora_(text-to-video_model) (first 100,000 of 124,573 characters read), https://en.wikipedia.org/wiki/George_Carlin:_I%27m_Glad_I%27m_Dead, https://en.wikipedia.org/wiki/Zelda_Williams. They cite TheStreet (Ian Krietzberg, 11 January 2024, `thestreet.com/technology/george-carlin-resurrected-without-permission-by-self-described-comedy-ai`, 403), The Guardian (Dee Jefferson, 7 October 2025, `theguardian.com/film/2025/oct/07/robin-williams-daughter-zelda-hits-out-at-ai-generated-videos-of-her-dead-father`, refused by the tool), Axios (8 October 2025, 403), BBC Bitesize (10 October 2025), The Hollywood Reporter (2 April 2024); none was readable, so the quotations come through Wikipedia's text.
- [115] Wikipedia, "Visual acuity" — https://en.wikipedia.org/wiki/Visual_acuity — summary of the first 100,000 of 107,937 characters; vernier acuity "about 8 arc seconds" is tagged [citation needed]; "minimum angular resolution of the human eye is 28 arc seconds" is cited there to D. F. Deering, "The Limits of Human Vision".
- [116] Wikipedia, "Hyperacuity" — https://en.wikipedia.org/wiki/Hyperacuity — summary; no arc-second value; "five or ten times better than acuity" and "better than 0.1 pixels" are uncited.
- [117] Webvision (Kalloniatis and Luu), "Visual Acuity" — https://www.webvision.pitt.edu/book/part-viii-psychophysics-of-vision/visual-acuity/ (moved from `webvision.med.utah.edu`) — summary; cone spacing at the fovea about 2.5 um or 28 arc seconds (Curcio et al., 1990); no vernier value.
- [118] FilmCraft 0.9.0 release — checksum list https://github.com/storytold/filmcraft/releases/download/v0.9.0/SHA256SUMS.txt and the asset `filmcraft-0.9.0-linux-x86_64.tar.gz` (69,756,500 bytes; SHA-256 `ea67953cc754bfd8272e0e5fa940518e16068ae96f6b72a2dce566ed69a61632`, equal to the list and to the value recorded in `research/craft-motion.md`). Downloaded, verified, unpacked in its own folder and run (`filmcraft-cli`, empty environment).
- [119] GSAP 3.12.5 (tarball SHA-256 `134ab4f04f6d98d5fd55f89b6f07726a3b9660c483d4ca31acc0efec62fd5236`) and 3.15.0, the current npm release (SHA-256 `d2e33ad202d4811e9084883f7ff9a27967ac4095caef51ca4c9d20697a253b1c`) — `npm pack gsap@...` from the npm registry.
- [120] playwright-core 1.56.1 and Chromium build 1194 (headless shell), both pre-installed in the container (`/opt/node-tools`, `/opt/pw-browsers`).
- [121] `bpy` 5.2.2 LTS (Blender as a Python module), PyPI wheel for Python 3.13, installed earlier in this session in its own virtual environment.
- [122] My measurements, 2026-10-18, cloud container (ffmpeg 6.1.1, Python 3.13, numpy 2.5, Pillow 12.3, 4 cores, no GPU). **M-C10** renderers against MO8 (FQ10); **M-C11** pan ease classifier (FQ11); **M-C12** Windows-safe scripts and the runner (FQ15); **M-C13** the A/B push card and the injected-jitter ladder (FQ9); **M-C14** the venue calculator (FQ12). Scripts and result files (`r2_*.jsonl`, `r2_*.json`) are in research/cinematic-quality-fixtures/ (see its README). The prints are the two Smithsonian NMAAHC items of [107]; no family material was used. Frames were deleted after measurement.
- [P9] `playbooks/cinematic-quality.md` (MO1 to MO9, family key, T6, D5) and `research/cinematic-quality.md` round 1 — read.
- [P10] `research/craft-motion.md` (FilmCraft recipes R2, R6, R8, Q7; checksums) — read.
- [P11] `CLAUDE.md` and `CHARTER.md` of the repository — read (secrecy and privacy rules: nothing personal left the container).
