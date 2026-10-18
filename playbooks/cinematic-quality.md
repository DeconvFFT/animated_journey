# Cinematic Quality: Making It Theatrical Without Looking Like AI

**Track:** `cinematic-quality` · **Version:** 5 (2026-10-18) · **Built from:** `research/cinematic-quality.md` and `CHARTER.md`

**How to read this.** Numbers in [brackets] point to the Sources list at the end. (M) means we measured it on made-up test material [76]. (J) means it is a judgement call to calibrate on the first five slice shots. TODO(research) marks a gap.

Nothing here uses her photos or stories yet. Real material comes in only after the pipeline and process are locked: the L1 process lock is Sat 14 Nov 2026 and covert collection starts Sun 15 Nov (D-13, W-06).

Reconciled with [DECISIONS.md](../DECISIONS.md) (2026-10-18), the single source of truth. Where a lean below disagrees with a register row, the register wins. D-nn rows are decided by the maker; W-nn rows are working defaults.

---

## Why this matters for our film

The charter sets the bar for every shot. It must be art-directed, consistent across the whole film, free of AI artifacts, and paired with a real sound mix and a proper master. "Good for a party" is not the bar.

The bigger risk is sameness, not glitches. Default settings make work look the same. The default ease in GSAP, a common animation library, is `power1.out` [69]. Agent pipelines lean toward uniform eases too [P3]. In 2026, critics described festival AI work as "boring" [4] and as pulled toward "the average or the mean" [5]. Our defence is specificity: her colours, her objects and her light, taken from her own scans.

Festival prizes are weak evidence. The best-known AI film festival is run by Runway, which sells generative video. Its Grand Prix is $50,000 plus 1,000,000 Runway credits. Entries must use generative video, and one of four judging criteria is "creative and skilled use of AI techniques" [1][2]. Read its winners as examples of process, not proof of quality. A 2024 TechCrunch review, older than six months and kept here as history, found that the human parts, performance and cinematography, carried the films [13].

The winners did a lot of human work. Robert Gaudette started with reference images and still character designs. A usable shot sometimes came after "a few tries" and sometimes after "dozens," and he used conventional editing [3]. Air Head, another AI-generated film, kept 2 to 3 seconds from each 20-second generation and fixed the balloon colours in post [12]. Any AI film that looks finished has human compositing behind it. A secondhand report says he worked two weeks of 17-hour days alone [4]. By our arithmetic that is about 30 hours per finished minute. For comparison, Away was made by one animator over about 3.5 years, about 140 hours per finished minute by our estimate [24]. Theatrical polish is a human-hours problem, not a generation-credits problem.

Our film is photo-forward. The photographs are the real base, so the rules are about respect for them. Move a camera only for a reason. Never mirror a photograph. Never regenerate or animate a real face in the public cut. Build faces by hand from a board for each age. These rules keep the film honest and keep it recognisably hers.

The venue is the hidden variable. A 5,000-lumen projector on an 8 m wide screen gives about 44 nits at its rated output, by our arithmetic, and about 33 once `venue_calc.py` takes 25% off for lamp age. The cinema reference is 48 cd/m² (SMPTE ST 431-1 Table 1) [92]. A lit hall also hides shadow detail that a dark cinema keeps [33]. What looks right on a laptop can fail at the premiere.

---

## Core principles

1. **Specificity beats polish.** Do the swap test. Put stock family photos where hers are. If the frame still works unchanged, it is not yet hers (gate G1).
2. **Every move needs a reason.** Move over a photograph only to reveal, link, isolate or mark time. Otherwise hold, or cut. Walter Murch ranks emotion first among the criteria for a good cut [55]. Ken Burns says movement "if it doesn't have meaning, it doesn't have a place" [54].
3. **Real memories stay real.** Never regenerate, restyle with a model, or animate a real face in the public cut. Never animate the faces of the dead. A reconstruction must look like a reconstruction [P2][P5].
4. **Finish once, last, and count it.** A stack of effects reads as a template, and it hides weak design. Keep global finishing layers to two or fewer. Check every shot with the finish switched off. The Annecy 2026 film *Danse Macabre* put a global film grain over the whole composition as its last unifying step [22].
5. **Author the motion.** Nothing moves on a default ease. Use settle, holds and deliberate ease families, and vary them across a chapter.
6. **Judge on the venue, not the laptop.** Type, shadows, pans and speech all change on a big screen. Test on that screen before you lock anything.
7. **Machines count, your eyes decide.** Scripts can measure ease, flicker, colour distance and grain. They cannot judge meaning, dignity or likeness. You sign those off.
8. **Write it down so taste does not drift.** Keep a short decision log and frozen reference frames. Then week 17 is judged against week 1 on purpose.

---

## How to do it, step by step

Work in this order. Each step ends in a check or a gate, so no shot moves on by feel alone.

1. **Get the venue facts.** Ask for the venue type, screen size, projector model, who runs AV, whether the room can be darkened, and whether playback is a DCP or an HDMI or USB file. The notes cannot know these. The neutral ask below goes to the venue by Fri 6 Nov, and its written answer, due Sun 15 Nov, decides file or DCP (W-17, O-21); grade for that path (see Decisions).
   Ask the venue these six questions, in this order (FQ7):
   - Playback path: a DCP on a cinema server, a laptop or media player over HDMI, or a USB stick into the venue's own player or TV.
   - Venue type and screen: hall, theatre, restaurant or community room; screen width and picture height in metres; a projector screen or a TV, and its size in inches.
   - Projector or display model (photograph its label), lamp or laser hours, and whether it is 1080p or 4K native.
   - Can the room be darkened, and how dark: lights off, exit signs, windows or blinds, and a lux reading on the screen with the event lights as they will be.
   - Who runs AV, and will they run a test on a weekday with the real chain by Sun 17 Jan 2027 (the venue visit, TD-L2b, W-56), and give access for a rehearsal on Mon 22 Feb (G-REHEARSE, W-52).
   - Sound and seats: is there a PA the room already uses, who controls it, can the film go in as stereo or 5.1, is there a hearing loop, how many seats, and how far the nearest and the farthest seat are from the screen in metres.

   Open with this neutral ask, which says nothing about the film (FQ12), and send it by Fri 6 Nov (W-17): "We are planning to show a short video at a gathering on 27 February 2027. Could someone tell me the projector or display model, how it is connected (HDMI, USB, other), the width and height of the lit picture, and whether the room can be darkened? Could we do a 30-minute test with our own laptop on a weekday before mid-January?"

   Put the six answers in a small `venue.json` and run `python3 -I research/cinematic-quality-fixtures/venue_calc.py venue.json` (with no argument it prints the template). It prints peak luminance, the grading gamma, the signal level the ambient light hides, the nearest and farthest seat in screen heights, the type-size floors, and what 0.05, 0.1 and 0.3 px of jitter subtend in arc seconds (M-C14), and it lists the defaults it still used. The same weekday test is the slot for the A/B push card (T6). Until the answers are in, every brightness, gamma, black-level and type-size figure in this playbook is a scenario, not the venue.
2. **Write the style bible.** It is one document of four to eight pages, with the ten decisions locked before the slice (T2). Add a good / not good board. Add a rule only when a test shot fails without it [27][28].
3. **Build the era colour strip.** From the animatic, pick one frame per beat. Reduce each frame to three swatches: dominant, secondary and accent. Lay them in a strip where each beat's width equals its running time. Draw one line above for emotional temperature, and a row below for the light (window, lamp, overcast, flash or none). Budget about two hours per era (J). Freeze the strip at gate G1 for the slice [31][32].
4. **Set the camera grammar.** Allowed moves are push, pull, pan, tilt, a small orbit of up to 3 degrees, and hold. Push or pull up to 8% of the frame. Pan up to 5% of frame width. For the virtual lens, use the photo's own 35 mm-equivalent focal length if the file has one [52]. Otherwise use 35 mm for snapshots and 50 mm for portraits (J). Keep faces central.
5. **Write each shot brief.** Every shot needs its label (L0 to L5, defined in the AI imagery playbook [P2]), a `because:` reason (reveal, link, isolate, time or hold), an ease family, `mirrored: false`, its lens, and its source photos. A shot with no reason fails check B1.
6. **Set the face rules before anything is generated.** Faces are built by hand from a per-age board (T3). Do not regenerate, restyle or animate a real face. Do not add teeth or eyelids, do not smooth skin, and never animate eyes or a mouth. The maker alone signs likeness: five of five correct in a shuffled line-up, passed twice, 48 hours apart (J). Strangers test something else (step 16).
7. **Author the motion.** For each move, write a timing chart: displacement at 10, 25, 50, 75, 90 and 100% of the duration. Pick one of six families: in-out, out, in, settle, drift or hold-snap. Let camera moves settle at the end. Hold after the payoff: at least 0.75 s after a payoff, 1.0 s after a punchline or reveal, and a legible card for at least 1.5 s [68][P3]. Twos can be a creative choice rather than a rule. Spider-Verse's animators chose twos for a pop-art look and changed them within shots [25]. For the timing chart itself, the classic reference is the timing-and-spacing chapter of Richard Williams' *Animator's Survival Kit*. We read its table of contents only [74].
8. **Run the spec check first (MO1).** It is cheap and exact, and it covers every move, including pans, tilts, orbits and multi-plane moves. Fail a framework default such as `power1.out` in GSAP [69] or `ease` in CSS. Fail a move that uses `linear` without `drift: declared`. Fail a chapter where more than 40% of eased moves share one ease, or where stagger offsets are evenly spaced.
9. **Render before grain, then audit the pixels (MO1b, MO2, MO6, MO8).** Work in `research/cinematic-quality-fixtures/`: copy a script out and run it with `python3 -I`.
   - **Pushes and pulls (MO1b, MO2).** `ZV_SIZE=1920x1080 python3 -I zoom_velocity_classifier.py shot.mp4`. It was tested on synthetic push-ins at 540p and, as a reconstruction, on three public-domain scanned prints at 1080p from 4K and native sources (M-C7b, 51 clips); on faint prints the floor rises (0.056-0.076 after H.264 on the faintest), so always render the Pillow reference from the same source file (M). It reads a 4% push as about 4.3% on every renderer, Pillow included, so it is a relative tool, not a ruler (M-C10). Do not trust it for settle or overshoot below about 10% of peak.
   - **Pans and tilts (MO6, MO1b, MO2).** `python3 -I pan_estimator.py clip.mp4 24` for speed (validated, M-C9). `python3 -I pan_ease_classifier.py clip.mp4 24` for the ease of translation-only pans and tilts (validated, M-C11). Report orbits, rotations, mixed zoom-and-pan and layers with different eases as `unknown`, never `pass`: measure those from the spec. A pan the classifier flags `low_confidence` is also `unknown`.
   - **Smoothness (MO8).** `python3 -I mo8_audit.py clip.mp4` on the output of any renderer, or on a folder of PNG frames for the master (it then also reports the result after x264). MO8 passes when MO8a, centre jitter, is at most 0.05 px at 1080p on the delivered file **and** MO8b, edge jitter by the fourth-difference estimator (`mo8b_d4_px`), is at most 0.04 px, measured on the master **before** the delivery encode (x264 CRF 14 alone reads 0.025 to 0.039 on perfect renders). Roughness (MO8c) and the ratio to a Pillow reference are informational only. Pillow `transform(EXTENT)` and a plain CSS transform without `will-change` read 1.4 times the Pillow box reference (M-C10), and relative roughness changes with push length and codec (advisor reproduction 2026-10-18: a perfect Pillow 4% push after x264 reads MO8c 0.069 at 2 s against 0.038 at 4 s, the nine-frame MO8b 0.060 against 0.016, the fourth-difference MO8b 0.026 against 0.017). There is no absolute roughness threshold. MO8a reads about 1.3 to 1.6 times the position jitter that causes it, so 0.05 px is about 0.038 px of position error. That subtends 4.8 arc seconds at 1.5 screen heights, against a best-case static alignment threshold of 2 to 5 arc seconds [123] (about 8 in a Wikipedia summary, [115]): under 5 arc seconds beyond about 1.4 screen heights and under 2 beyond about 3.6 (M, arithmetic). UNVERIFIED for moving pictures: the venue A/B card (T6) decides.
   - **Renderers (M-C10: one print, one push profile).** Do not use ffmpeg `zoompan` for finals: its centre jitter is 0.29 px through an RGB path and 0.63 px, not 0.29, in the usual `-pix_fmt yuv420p` command line, against 0.05 allowed. Keep it for proofs. Use sub-pixel rendering for finals.
     - Pillow (`resize` with the box filter, or `transform` EXTENT) passes.
     - GSAP: use it for the ease only and write `style.transform` yourself in `onUpdate`; its own `scale` tween writes four decimals and fails MO8b (0.061 px, the same in 3.12.5 and 3.15.0; a 2020 GSAP forum reply on a jerky pan-zoom calls it "just a decimal precision thing" and names no setting [124]). No `force3D` on slow pushes (centre jitter 0.044). Never animate `width`, `height`, `left` or `top` for a push (0.18 px).
     - Capture a Chromium page by stepping it and screenshotting, never by real-time recording (the one recording tried stuttered).
     - Blender: image texture on Linear; motion blur makes no difference on a slow push.
     - FilmCraft 0.9.0: a new keyframe is linear, so set `bezier` or `autoBezier` on both keyframes of every Ken Burns (or `easeOut` on the first and `easeIn` on the last; `easeIn` on the first and `easeOut` on the last do nothing). Its built-in H.264 export is for proofs only: finals go ProRes, then x264.
   - **Staging.** Stage photographs with at least three depth planes and a ground-contact cue, such as a shadow, so they do not look like paper dolls [80] (search-result only).
10. **Finish the shot.** Count the global layers: grain, vignette, letterbox, flare or bloom, halation, dust, light leak, colour filter and shake. Keep it to two or fewer, all from the era's finish stack (FN1). Run the finish-off test. Bake grain as at least 48 distinct frames, with a different seeded start for each shot. Keep the grain's luminance spread on new layers within 30% of the scan's flat patch (FN6). Light wrap goes last in the chain, on the edge only, after spill suppression [50]. Blur each depth plane as a layer, not per pixel, because per-pixel depth blur makes halos at depth edges [51]. Never blur faces for depth.
11. **Check colour with numbers.** Compute each shot's median colour and its three dominant colours in Lab. Compare them with the era swatches using ΔE00 [40]. A difference below 1 is generally not visible. From 1 to 2 it shows only in close side-by-side viewing. Above 2 it is an increasingly obvious mismatch. Our tolerances (J): within 6 for the shot, within 4 for skin, and within 3 between shots in one scene.
12. **Check type and graphics (TY1, TY3, TY4).** Applies to type we set: titles, cards, date lines, captions and credits. Font at least 5% of picture height, x-height at least 2.5%, and strokes at least 2 px at 1080p. Text inside photographs and her handwriting is exempt. Below 2% x-height, text is decorative and must not carry information. If text inside a photograph carries information, repeat it on a card or caption (TY4). Captions follow `format.md` Step 8 (7 to 8% line height), which at 1080p is `FontSize=23`: x-height 3.2 to 3.8% of picture height across five fonts, line pitch 7.96% (M-C8). Caption x-height floor 3.1% (6 screen heights, J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font; TY1 is a floor, not a caption size. Keep all text and graphics inside 5% margins [45]. Every font needs a licence file (TY3). OFL: video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video [56]. OFL fonts only (W-21): commercial fonts under an Adobe or Monotype subscription are out (T2 decision 4).
13. **Do the maker's eye checks.** These cannot be automated: eyes, mouth, hands, text, reflections, cut-out edges on black, white and mid-grey at 200%, and the AI-tell sweep (T9). The numbers help, but they never sign anything off.
14. **Check the chapter.** In every run of eight moving shots, look for at least three move families, none above 40%, no family more than twice in a row, and an entropy of at least 1.5 bits (MO9). Held shots should be at least 35% of photo shots. Include at least one picture-led silence of 3 s or more. Shot lengths should vary, with a coefficient of variation of at least 0.4 (J). No finishing layer on more than 80% of shots. Captions stay within reading limits.
15. **Run the review ritual.** Wait 48 hours before you approve or reject a shot. This is practitioner advice with no controlled study behind it [75]. Then do a blind A/B against the previous version, a squint test [73], distance viewing, half and double speed, sound-off and picture-off passes, and a reverse-order pass.
16. **Run the strangers' tests.** Two sessions are decided (W-43): S1 with three strangers to her on the slice about Sun 20 Dec, and S2 with three to five on the locked cut in week 17 (Mon 8 to Sun 14 Feb). Each time, people who have never met her, and never will, watch a redacted copy once with no pauses. Then they fill in the written sheet before any discussion (T7). Strangers judge whether the film reads and whether it looks computer-made. They cannot judge likeness or truth.
17. **Test on the venue.** Run the projection-truth checklist (T6) on the real projector at the venue visit by Sun 17 Jan 2027 (TD-L2b, W-56), with the test clip only and never the film. Run it again at the Mon 22 Feb rehearsal with the three masters (G-REHEARSE, W-52), and on the day.
18. **Log every decision.** Write one short entry per decision (T8). Record what was decided, why, the evidence file, and whether it can be reversed.

---

## Learn-by-doing exercises

**Test material.** Use only material with nothing to do with her: the synthetic fixtures in `research/cinematic-quality-fixtures/`, or any image you have the rights to use. Do not use family photos or stories yet. Ask an agent to run the scripts in the cloud container. For the maker's own Windows PC, install Python 3.10 or later, numpy, Pillow and an ffmpeg with libass and libx264, then run `py -3 -I windows_check.py C:\LJ\check --font "C:\Windows\Fonts\arial.ttf" --font-name "Arial" --ffmpeg "C:\tools\ffmpeg\bin\ffmpeg.exe"` from a copy of the fixtures folder (about 5 minutes to set up and 2 to 5 to run; step 1 is `caption_xheight.py` with the chosen caption font) and keep `windows_check_report.json` in the repo. It generates its own test picture and uses nothing personal. Until that report is in the repo, every Windows number is UNVERIFIED (FQ15).

### Exercise 1: Measure three reference films with a stopwatch

- **Goal:** Replace guesses about camera ranges with numbers from real films. TODO(research): no film was watched for the notes, so every shot-level claim about these films is still unverified.
- **Steps:**
  1. Pick five minutes each from: a Ken Burns documentary sequence, *The Kid Stays in the Picture* [53], and a *Flow* long take [23].
  2. For every shot, write its shot size, duration, move (if any) and reason for the cut.
  3. Use the same columns as T1 section B.
  4. At the bottom, count the held shots, the longest move and the most common move.
- **Time:** about 2 hours (J).
- **What good looks like:** a complete row for every shot, with counts at the bottom. You can say whether the ranges in T2 match what you measured.

### Exercise 2: Find the dark steps on your screen

- **Goal:** Learn how much shadow detail your screen keeps, before the venue does.
- **Steps:**
  1. Open the black-level test at https://www.testufo.com/blacklevels [39]. Learn how to read the bars.
  2. Find the first grey step you can see above black on your laptop.
  3. Repeat on the TV from about 3 m, our standard viewing distance (gate G6).
- **Time:** about 30 minutes (J).
- **What good looks like:** you can name the first visible step on each screen. Keep both numbers to compare with the venue later.

### Exercise 3: The squint test

- **Goal:** Check that a picture reads as light and dark shapes before any finish is added.
- **Steps:**
  1. Pick three test images with a clear subject. None of them is her.
  2. Make a copy of each, blurred by about 1% of the frame width and in greyscale, using any image editor.
  3. Look at each copy for ten seconds.
  4. Name the subject and the two or three main shapes you see.
- **Time:** about 30 minutes (J).
- **What good looks like:** the subject and the main shapes read in all three copies. If one fails, fix the composition before adding finish. The squint is a long-standing painter's check [73].

### Exercise 4: See the ease by eye

- **Goal:** Learn to see linear, ease in-out and ease-out motion.
- **Steps:**
  1. The fixture script `gen_synthetic_pushins.py` needs a textured test still named `still.png` in its working folder. The notes do not include that still, so ask an agent to make one first. Then ask for the push-ins to be made again with the script, because the media files were deleted after the tests.
  2. Watch each clip at half speed. Note where the motion is fastest.
  3. Call each clip linear, in-out or out.
  4. Compare your calls with the output of `zoom_velocity_classifier.py`.
  5. For the MO8 check, copy `zoompan_vs_subpixel.py`, `mo8_audit.py`, `zoompan_vs_subpixel_prints.py` and `zoom_velocity_classifier.py` into one folder, put a textured `still.png` beside them, and run `python3 -I zoompan_vs_subpixel.py`. Then run `python3 -I mo8_audit.py pil_slow.mp4 zp_slow.mp4` from that folder. Each clip prints one JSON line. The Pillow clip should pass (`mo8a_centre_jit_px` at most 0.05 and `mo8b_d4_px` at most 0.04); the zoompan clip should fail MO8a at about 0.6 px. Both clips are already encoded, so `mo8b_d4_px` here is the after-x264 reading; on real work measure MO8b on the master. `mo8c_rough` will also read higher for zoompan, but it is informational. (Checked 2026-10-18 on a numpy-made still: Pillow 0.0046 and 0.0203, zoompan 0.6245 and 0.1325.)
- **Time:** about 1 hour (J).
- **What good looks like:** your calls match the classifier. Where they do not, write down why.

### Exercise 5: A blind A/B round

- **Goal:** Practise a blind pick and notice your own habits.
- **Steps:**
  1. Ask an agent to make two versions of a practice shot and name them X and Y at random.
  2. Pick the better one and write one reason.
  3. Ask for the key to be revealed.
  4. Repeat five times with different shots.
  5. Count how often you picked the newer version.
- **Time:** about 15 minutes per round (J).
- **What good looks like:** five picks, each with a reason in your own words. A pattern, such as always choosing the newer version, is useful information, not failure.

### Exercise 6: Catalogue ten AI tells

- **Goal:** Learn to name tells at 100% zoom.
- **Steps:**
  1. Watch one short AI-made film that you are allowed to view. The notes did not check the festival films, so treat what you find as your own observation.
  2. Pause on faces, hands, text and motion. Match what you see against the catalogue (T9).
  3. For each mark, write the tell number, the cause, how you detected it and the fix.
- **Time:** about 1 hour (J).
- **What good looks like:** at least five marks, each with a tell number from T9.

### Exercise 7: Fill a style bible for a practice subject

- **Goal:** Learn the ten decisions by using them.
- **Steps:**
  1. Pick a practice subject: a made-up character, or a photo of someone who is not in the film.
  2. Fill in the T2 template with values.
  3. For each decision, write its "how we check" line.
  4. Make a good / not good board with four pairs. Add one line on why each is good or not.
- **Time:** about 3 to 4 hours (J).
- **What good looks like:** all ten decisions have a value and a test, and the board has four pairs.

### Exercise 8: Build a practice colour strip

- **Goal:** Practise swatches and a strip whose widths follow running time.
- **Steps:**
  1. Choose 12 frames from a practice sequence, one per beat.
  2. For each frame, pick three swatches: dominant, secondary and accent.
  3. Lay the swatches in a strip. Make each one as wide as its beat's running time.
  4. Add one temperature line above and a light row below.
  5. Squint at the strip and read it as a story.
- **Time:** about 2 hours (J). The notes estimate about two hours per era.
- **What good looks like:** the strip shows an emotional arc when you squint, and the swatches match the frames by eye.

### Exercise 9: Thin lines and small type

- **Goal:** See what survives compression.
- **Steps:**
  1. Ask an agent to make a test image. It should have black and red lines 1, 2, 3 and 4 px wide on mid-grey, and three sizes of type.
  2. Encode it as H.264 at CRF 18, the setting the notes used (M).
  3. Watch it full screen, then on the TV from 3 m.
  4. Note which lines and type stay clear.
- **Time:** about 1 hour (J).
- **What good looks like:** near-black lines stay clear at every width. In the notes' test, 2 px and 4 px red lines kept about 99% of their contrast, and a 1 px red line kept about 70% (M). That is why our strokes are at least 2 px.

### Exercise 10: Find where pans strobe

- **Goal:** See strobing at pan speeds around our limit.
- **Steps:**
  1. Ask an agent for a pan test with a textured layer. Make it at 0.10, 0.143, 0.2 and 0.3 frame widths per second, at 24 fps.
  2. Watch each one on the TV from 3 m.
  3. Note where the strobing starts for you.
- **Time:** about 30 minutes (J).
- **What good looks like:** you have a number for where strobing starts for you. Keep the rule of no more than 0.143 frame widths per second, which is one frame width every seven seconds [41]. The exception is a move that is blurred or declared as a whip.

### Exercise 11: Write one decision-log entry

- **Goal:** Learn the decision-record habit [72].
- **Steps:**
  1. Pick a real decision from this playbook. Good options are "twos on paper layers, ones on camera," or the playback path.
  2. Write one entry using the T8 template.
  3. Include at least one negative consequence.
- **Time:** about 20 minutes (J).
- **What good looks like:** one page, with at least one cost named.

---

## Templates and checklists

### T1. Per-shot checklist (from D1)

Severity: **Crit** = any fail blocks the shot. **Maj** = fix before chapter assembly. **Min** = log it. Who: **Agent** = the pipeline checks it. **Maker** = needs your eyes. Gate = where it is scored.

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

**Per finished minute (J).** Weighting the typical minutes by the class mix (A 60%, B 25%, C 10%, D about 5%) gives about 3.7 maker minutes per shot before A3. At about 12 shots per finished minute (about 120 shots per 10 minutes, `playbooks/agent-pipeline.md`), that is about 45 maker minutes per finished minute, plus 10 for each L3 or L4b face shot. That is the unlevered figure. The register's levers set hero shots at 5% and the film at 8 shots a minute (W-34, W-51): with the class mix A 65%, B 25%, C 5%, D about 5% it is about 3.4 maker minutes per shot and about 27 per finished minute, plus the same 10 for each face shot. The total goes to `production-scale` as a delta.

| ID | Item | Test | Pass | Sev | Who | Gate |
|---|---|---|---|---|---|---|
| **A. Identity and honesty** | | | | | | |
| A1 | Label matches the ladder | `output_level` in brief equals the XMP or `steps.csv` level; every changed region listed | Match, no unlisted change | Crit | Agent | G2 |
| A2 | Face geometry intact (L1, L2, L4a) | Landmark ratios (inter-ocular, eye-line, mouth width) of first and last frame against source | All within 2% | Crit | Agent | G2 |
| A3 | Face never regenerated (L4b, L3) | Maker's blind line-up: five frames from the shot (0, 25, 50, 75, 100%) mixed with four decoys | 5 of 5 chosen as the same face, twice, 48 hours apart | Crit | Maker | G2 |
| A4 | No animated eyes, blinks, mouth or speech on a real face | Step frames on eyes and mouth at 100% | None | Crit | Maker | G2 |
| A5 | No invented people or text | Diff mask against source; read all text | None | Crit | Agent + Maker | G2 |
| A6 | Photograph not mirrored | Manifest `mirrored: false`; text reads correctly | True | Crit | Agent | G2 |
| **B. Layout and camera** | | | | | | |
| B1 | Move has a reason | `because:` is reveal, link, isolate, time or hold | Present | Maj | Agent | G0/G2 |
| B2 | Move magnitude | Estimator or spec: total zoom and translation | Push or pull up to 8%, pan or orbit up to 5% of width and 3 degrees, unless class C | Maj | Agent | G2 |
| B3 | No disocclusion holes | Alpha of layered composite after fill; step the extreme frames | Zero hole pixels at 100% | Crit | Agent | G2 |
| B4 | Shot size progression | Adjacent shots differ in size class or angle (30 degrees); at most two close-ups per chapter | True | Min | Agent | G4 |
| B5 | Direction | Move follows or holds the gaze; no more than 2 consecutive same-direction drifts | True | Min | Agent | G4 |
| B6 | Portrait ladder alignment | Eye centre of consecutive portraits within 3% of frame | True | Maj | Agent | G2 |
| B7 | Safe area | All text and faces inside 5% margins (faces may bleed only when the brief says close-up) | True | Maj | Agent | G2 |
| B8 | Hold before move | New photo holds at least 0.5 s before any move | True | Min | Agent | G2 |
| **C. Colour and light** | | | | | | |
| C1 | Palette | Median and three dominant colours in Lab within ΔE00 of 6 of the era swatches | True | Maj | Agent | G1/G2 |
| C2 | Scene continuity | Shots in one scene within ΔE00 of 3 of each other (median colour) | True | Min | Agent | G4 |
| C3 | Skin patch | Skin region within ΔE00 of 4 of the era skin swatch from the scan | True | Maj | Agent | G2 |
| C4 | Value structure | Squint test (blur 1% of width, greyscale): face reads from background | Face-to-surround mean luma difference of at least 10 L* | Maj | Agent | G2 |
| C5 | Clip and crush | Pixels below 16 or above 235 (8-bit video range) | Under 0.5% of frame unless declared | Maj | Agent | G2 |
| C6 | Dark-detail rule | Story-critical regions' luma | Above 10% signal unless the venue test passed | Maj | Agent | G2/G6 |
| C7 | Light direction | Composited L5 elements share the key direction of the photo they sit on | Within 30 degrees | Maj | Maker | G2 |
| C8 | Light variety | Chapter has at least 3 distinct lighting types (hard side, backlit, window, lamp, overcast) | True | Min | Agent | G4 |
| **D. Motion** | | | | | | |
| MO1 | No default ease, no undeclared linear (spec) | Spec lint on every move: no framework default ease (`power1.out` for GSAP, `ease` for CSS); no `linear` ease unless the brief declares `drift: declared` | True | Crit | Agent | G2 |
| MO1b | Push, pull, pan and tilt, pixels | Pushes and pulls: `zoom_velocity_classifier.py`, CV over 0.12 unless `drift: declared`. Translation-only pans and tilts: `pan_ease_classifier.py clip.mp4 24` (`mo_verdicts(c, brief_family, drift_declared)`; M-C11: exact easing and family on 100 of 100 in-library clips through grain, H.264, twos and integer steps; family on 4 of 5 unseen CSS curves, the fifth flagged; the truth curves were the classifier's own library except those five). Report `unknown` only when the classifier sets `low_confidence`, and for orbits, rotations, mixed zoom-and-pan and layers with different eases (measure those from the spec); never `pass` for them | True, or `unknown` for the moves named | Maj | Agent | G2 |
| MO2 | Ease class declared and measured | Measured class equals brief `ease_family`: `zoom_velocity_classifier.py` for pushes and pulls, `pan_ease_classifier.py` for translation-only pans and tilts, the spec for everything else | True | Maj | Agent | G2 |
| MO3 | Settle | Velocity in the last 15% of the move decays monotonically to 5% of peak or less in the spec (10% or less in the pixel audit) | True | Maj | Agent | G2 |
| MO4 | Hold after payoff | Velocity at 0 in the spec (under 10% of peak in the pixel audit) for at least 18 frames after the payoff, 24 frames after a face reveal | True | Maj | Agent | G2 |
| MO5 | Twos and ones | Drawn layers show alternating zero steps (twos); camera and type show none (ones) | True | Min | Agent | G2 |
| MO6 | Pan speed | Pixel audit: `python3 -I research/cinematic-quality-fixtures/pan_estimator.py clip.mp4 24` on the delivered 1080p file (M-C9: 22 of 22 verdicts right away from the limit; error at most 0.018 px per frame on constant pans). Fastest textured layer at most 11.4 px per frame at 1920 wide (0.143 frame widths per second): PASS at the limit plus 0.3 px per frame or less; INCONCLUSIVE on flat or fading frames; borderline within 0.5 px. Unless blurred or a declared whip stays a human call, because the estimator measures content shift, not blur. Vertical pans use `vy` against frame height | True | Maj | Agent | G2 |
| MO7 | Motion blur | Any layer above 4 px per frame has sub-frame blur at 180 degrees | True | Maj | Agent | G2 |
| MO8 | Sub-pixel smoothness | `python3 -I research/cinematic-quality-fixtures/mo8_audit.py clip.mp4`, or a folder of PNG frames for the master (it also reports the result after x264). Keys: `mo8a_centre_jit_px` (MO8a), `mo8b_d4_px` (MO8b), `mo8c_rough` (informational) | MO8a at most 0.05 px at 1080p on the delivered file **and** MO8b (fourth-difference estimator, `mo8b_d4_px`) at most 0.04 px, measured on the master **before** the delivery encode (x264 CRF 14 alone reads 0.025 to 0.039 on perfect renders). Roughness (MO8c) and the ratio to a Pillow reference are informational only: Pillow EXTENT and a plain CSS transform read 1.4 times the Pillow box reference (M-C10), and relative roughness changes with push length and codec (advisor reproduction 2026-10-18: perfect Pillow 4% push after x264, MO8c 0.069 at 2 s against 0.038 at 4 s; nine-frame MO8b 0.060 against 0.016; fourth-difference 0.026 against 0.017). No absolute roughness threshold. MO8a reads 1.3 to 1.6 times the position jitter behind it, so 0.05 px is about 0.038 px of position error: under a best-case static alignment threshold of 2 to 5 arc seconds [123] beyond about 1.4 to 3.6 screen heights (M, arithmetic; UNVERIFIED for moving pictures until the venue A/B card says otherwise) | Maj | Agent | G2 |
| MO9 | Chapter variety | 8-shot windows: 3 or more family keys, none above 40%, entropy 1.5 bits or more, held shots 35% or more. Pan family keys come from `family_key`, and `mo9_check(keys)` in `pan_ease_classifier.py` applies the chapter rule | True | Maj | Agent | G4 |
| **E. Finish** | | | | | | |
| FN1 | Stacked finish count | Global finishing layers (grain, vignette, letterbox, flare, bloom, halation, dust, scratch, light leak, colour filter, shake) | Two or fewer, all in the era's finish stack | Maj | Agent | G2 |
| FN2 | Finish-off test | Render with finish off | Silhouette, value and colour still hold | Maj | Maker | G2 |
| FN3 | Frequency | No finishing layer on more than 80% of shots in a chapter | True | Min | Agent | G4 |
| FN4 | Cut-out edges | Composite over black, white and mid-grey; view at 200% | No fringe, no hole | Crit | Maker | G2 |
| FN5 | Light wrap | Edge only, last in chain, halo within 3 px at 1080p, none on the side away from the key | True | Maj | Maker | G2 |
| FN6 | Grain match | Std of flat-patch luma on L5 layers within ±30% of the scan's flat-patch std | True | Maj | Agent | G2 |
| FN7 | Grain loop | Autocorrelation at the loop length under 0.3 | True | Maj | Agent | G2 |
| FN8 | Depth of field | Blur by plane; no blur on faces; far-plane blur at most 1.2% of width | True | Maj | Agent | G2 |
| **F. AI tells** | | | | | | |
| AI1 | Tells 1 to 23 swept | Catalogue (T9) walked at 100% on key frames, with 5 frames per second of a moving shot | None present | Crit | Maker | G2 |
| AI2 | Flicker | Flicker index on a static region | 0.3 levels or less (M: static 0.000, injected 2.58) | Maj | Agent | G2 |
| AI3 | Hands, text, reflections | Every visible instance checked | Correct or absent | Crit | Maker | G2 |
| **G. Type and titles** | | | | | | |
| TY1 | Legibility, type we set | Titles, cards, date lines, captions and credits: font at least 5% of picture height; x-height at least 2.5%; strokes at least 2 px. Text inside photographs and her handwriting is exempt; below 2% x-height, text is decorative and must not carry information. Captions follow `format.md` Step 8 (7 to 8% line height), which at 1080p is `FontSize=23`: x-height 3.2 to 3.8% of picture height across five fonts, line pitch 7.96% (M-C8). Caption x-height floor 3.1% (6 screen heights, J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans. Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font; TY1 is a floor, not a caption size | True | Crit | Agent | G2 |
| TY2 | Hold | Card held at least 36 frames once fully legible; captions within reading-speed limits from the format track | True | Maj | Agent | G2 |
| TY3 | Licence | Font, texture and plate each have a licence file | True | Crit | Agent | G1/G2 |
| TY4 | Text in photographs | Any text inside a photograph that the audience must read (sign, letter, label, her handwriting) is repeated on a card or caption | True where the text carries information | Min | Maker | G2 |
| **H. Projection** | | | | | | |
| PR1 | Banding | Dark-ramp test: no visible steps in dark gradients at the venue; masters 10-bit | True | Maj | Maker | G6 |
| PR2 | Thin lines | No saturated 1 px lines; contrast retained at 90% or more after the access-copy encode | True | Maj | Agent | G6 |
| PR3 | Grain survival | Flat-patch grain std after encode at least 70% of the master's | True | Maj | Agent | G6 |

### T2. Style bible (from D2)

Format: one document of four to eight pages, with a good / not good board. The maker owns it, it is versioned, and every shot brief refers to it. Each decision has a lock, a test and a gate. Fill in the brackets.

```yaml
# style_bible.yaml  (version, date, author)
1_palette_per_era:
  how: "sample from L0 scans: k-means in Lab on non-face regions + paper border; record sRGB hex and Lab"
  limit: "six colours or fewer per era (G1)"
  eras:
    - {id: era_1, years: "[ ]", colours: ["#", "#", "#", "#", "#", "#"], skin_swatch: "#", accent: "#", light: "[window | lamp | flash | overcast]"}
  test: "shot dominant colours within dE00 6 of the era swatches; skin within 4"
2_hand_made_material:
  material: "[her own hand-made material, from the maker's week-1 answer and filled at G1 (W-38): dough | thread | garden | ledger | other; never a voxel marker (D-23)]"
  rules: ["layer count max [ ]", "shadow direction [ ]", "edge: [torn | cut | scalloped]", "hand rule: [ ]", "eye rule: [ ]", "what never animates: [ ]"]
  good_not_good_board: "path/to/board.png"
  test: "at least 80% of strangers can say which shots are reconstructed before any card (for example 4 of 5, 3 of 4, 3 of 3)"
3_line_and_edge:
  min_stroke_px_1080: 2
  cutout_edge: "feather 0.5 to 1 px, colour decontaminated"
  test: "three-background test at 200%; thin-line retention 90% or more"
4_typography:
  families: ["display: [ ]", "text: [ ]", "handwriting: only words she actually wrote"]
  licence: "OFL fonts for titles, cards and captions (video titling is a listed permitted use, FAQ 1.1; embedding is answered for documents and files, 1.12, not video [56]). OFL fonts only (W-21, confirmed at G1, Sun 15 Nov): commercial fonts under an Adobe or Monotype subscription are out, for the reasons that follow. Adobe Fonts Product Specific Terms (effective 7 Oct 2024, confirmed by the advisor from the PDF 2026-10-18 [109]): the grant lasts 'only for as long as you maintain an uninterrupted Adobe Subscription Plan' and the terms never mention video, film, broadcast or exhibition. Monotype Create + Deploy, Create + Pitch and Enterprise likewise tie every grant to the term and keep no right for a finished film after it [88][89]. No Adobe Fonts FAQ lookup is needed while OFL fonts only stands (W-21); do it only if a commercial font is ever reconsidered"
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
  paper: "scan of her print backs, or a CC0 texture (the notes name ambientCG; its licence is TODO(research)); source recorded"
  applied: "once, last, on the 10-bit master; the 8-bit access copy relies on grain or texture of at least one 8-bit level, because invisible dither is quantised away by the encoder [44]"
9_title_system:
  types: ["chapter card", "date line", "end credits cue sheet"]
  rules: ["no lower thirds", "no typewriter reveal", "centre only if the layout calls for it", "hold 1.5 s once legible"]
10_never_list: "see T5"
```

The ten decisions in one line each:

| # | Decision | Lock | Failure it prevents |
|---|---|---|---|
| 1 | Palette per era | Six colours per era from her scans, plus skin and accent | Generic decade palettes and teal-orange |
| 2 | Hand-made material | Material, layer, hand and eye rules | A reconstruction mistaken for a photograph |
| 3 | Line and edge | Minimum stroke, feather, fringe test | Paper-doll cut-outs, aliasing |
| 4 | Typography | Two faces, plus her handwriting for her words only; licence files | Illegible or unlicensed type |
| 5 | Camera grammar | Move list, ranges, lens, cut-or-move | The same slow zoom on every photo |
| 6 | Reconstruction marker | Visible signature and disclosure card | A breach of charter principle 4 |
| 7 | Still-to-moving ratio | Hold share and plane limits | Slideshow rhythm |
| 8 | Grain and paper | Stack per era, at most two layers, matched to scans | Stacked finish, looped grain |
| 9 | Title system | Three title types and their rules | Template titles |
| 10 | Never list | T5 | Cheap tells |

Brand rule for decisions 2 and 10 if a voxel (Minecraft-style) look is used: decided (D-23, W-38, [DECISIONS.md](../DECISIONS.md)). No Mojang textures, sounds, UI or footage in the public cut; original voxel assets only; the name at most as a secondary description with the disclaimer; and a voxel look is never the reconstruction marker. The saved usage excerpt says why: the name may not be the primary title, gameplay must not be "displayed or projected publicly within physical locations," and events were limited to about 150 participants [57].

### T3. Per-age reference board (from D2b)

Use one board for each age in the brief: 6, 25 and 55. Add more only when a chapter needs them. A board is the shared reference that keeps one face recognisable, much as a model sheet does for animators [30].

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

**The likeness protocol (J).**

1. The agent prepares a shuffled line-up of five stylised faces. One is correct and four are decoys. Decoy set A is the same stylisation applied to public-domain stand-in portraits already listed in `ai-imagery.md` (NARA 546220 and US Navy 80-G-27208 among them, licences read on their Commons pages, re-check before use), or to your own face. Never use a relative's photo, because they cannot be told why. Decoy set B is the same stylisation applied to her at other ages. Set A tests likeness; set B tests age discrimination.
2. You pick without seeing labels.
3. A pass is five of five correct. Then repeat the test 48 hours later.
4. Record which feature decided each pick. That feature becomes a board attribute. The one or two features that survive all three age boards (6, 25 and 55; for example the parting, the tilt of the head when she listens, the hand she rests her chin on) are your own unspoken knowledge of her face, written down for the first time. Make them the film's visual leitmotif: the hand-made material always gets them right, and a cut between eras can land on a match of the same tilt of the head, which answers the strangers' question E without a caption. Nothing is invented, because the features come from her photographs.

The notes found no validated method for a stylised, cross-age face. Face-recognition models score about 98% on the AgeDB-30 benchmark for real photographs [78], but we found no report on stylised faces. Use landmark ratios as a cheap drift alarm. Flag any shot whose ratio moves more than 2% from the board (J). Send flagged shots to the line-up. Never synthesise a different age of her from a photo. Stylisation is a separate asset, and it never replaces a photo in a factual beat [P2].

### T4. Review rubric (from D3)

Score each criterion from 1 to 5, using the charter's six criteria: meaning, specificity, accuracy, feasibility, ethics, and craft and usability [P5]. A gate passes only when every score is 4 or higher and nothing critical is open. Attach the evidence named below.

**G1, style frames (three per era; you score, the advisor reads)**

| Check | Test | Pass |
|---|---|---|
| Not any family's film | Swap test: replace her photos with stock family photos. Does the frame still work unchanged? | It should not. It depends on her specifics. |
| Palette | Six or fewer colours, sampled from her prints, with swatches attached | True |
| Reconstruction visibly stylised | Could a reconstruction be mistaken for a photograph? | No |
| Finish stack | Count of global layers | Two or fewer |
| Squint and distance | Blur and greyscale; TV at 3 m | Subject and mood read |
| Type | Size and licence file | T1 TY1 and TY3 |
| Hand and eye rules | Shown on the board | Present |
| Era identifiable | Hide the date. Does the frame say which era it is? | Yes |
| Likeness | Age board line-up for any stylised face | 5 of 5, twice |

**G2, shot draft (per shot; use T1)**

| Criterion | Evidence | Score 4 or 5 means |
|---|---|---|
| Meaning | Brief `beat`, and the blind read: what did you feel first? | The beat lands at the first blind viewing, 48 hours later |
| Specificity | Swap test; a named object or place is visible | The shot could not be about another woman |
| Accuracy | A1 to A6, the label and `steps.csv` | All critical items pass |
| Feasibility | Time spent against the class budget | Within budget, or replanned |
| Ethics | A3 to A5, hard-topic flag, public-room test ("would she tell this to people she has never met" [P4]) | Clear |
| Craft and usability | T1 sections B to PR, AI1 sweep, template-risk output | No critical fail; majors fixed |

Automatic fail: any critical item in T1, any banned tell from T5, or any unlisted changed region.

**G4, chapter (assembled)**

| Check | Test | Pass |
|---|---|---|
| Move-family variety | MO9 | True |
| Holds and silence | Held shots at least 35%; at least one picture-led silence of 3 s or more per chapter | True |
| Rhythm | Shot-length coefficient of variation at least 0.4 (J); no run of four shots within 20% of the same length | True |
| Palette and type continuity | C2; type spec identical | True |
| Finish frequency | FN3 | True |
| AI-tell sweep | One frame per second of the chapter at 100%, in contact sheets, plus full-speed viewing | No banned tell |
| Captions | Reading-speed and length limits from the format track | True |
| Loudness plan | Present: -1 dBTP everywhere; three venue masters (-23, -18 and -16 LUFS) chosen at the Mon 22 Feb run; online copy -16 LUFS (W-19) | True |
| Strangers' evidence | Independent marks per minute (T7) | Two or fewer per minute |

### T5. Banned cheap tells (from D4)

Banned in the public cut. Each one can be detected with the test named in T1 or T9.

1. Default or uniform ease: `power1.out` everywhere, one spring setting, or evenly spaced stagger. (MO1, MO9)
2. The same slow zoom-in on every photograph. (MO9)
3. Stacked finish: more than two global finishing layers, or any layer on more than 80% of shots. (FN1, FN3)
4. Letterbox bars, vignette, lens flare, bloom or halation added to hide weak design. (FN2)
5. Stock dust, scratch, light-leak or film-burn overlays, and fake date stamps. Never age material that is already aged [P1].
6. Looped grain under 48 frames. (FN7)
7. Live, full-frame grain filters. They are slow and not repeatable [P3]. Grain is baked.
8. Beat-synced zoom punches, whip pans and trending transitions [P1][P3].
9. Lower-third captions for people outside the credits, typewriter reveals, and centred glowing titles [P3].
10. Generated text, signs or logos. (T9 row 7)
11. Generative hands in photographic shots. (T9 row 6)
12. Animated eyes, blinks, lip movement or speech from stills. (T9 rows 9 and 18)
13. Regenerated or "improved" faces, skin smoothing, invented teeth. (T9 rows 4 and 5)
14. Mirrored photographs. (A6)
15. Morphs between two different people. (T9 row 3)
16. Teal-orange default grade, or over-saturated skies and greens. (T9 row 12)
17. Generic AI lighting or centred, epic compositions. (T9 rows 10 and 11)
18. Paper-doll cut-outs: visible slab edges, fringes, no ground contact. (FN4, B3)
19. Depth-of-field blur on faces, or per-pixel depth defocus halos. (FN8)
20. Cloned voices, AI-sung words, or new sentences in her handwriting font [P3][P5].
21. Sepia or "old film" filters over everything, or stacked era filters [P1].
22. The Minecraft name as a title, or unlicensed brand marks [57].
23. Saturated 1 px lines, or text under 2.5% x-height. (PR2, TY1)
24. ffmpeg `zoompan` for a final push. (MO8)
25. Phone-style "memory" themes and auto-music [P1].
26. CSS layout-property animation (`width`, `height`, `left`, `top`) or a real-time screen recording for a push: centre jitter 0.18 px, and stutter. (MO8)
27. GSAP's own `scale` tween on a slow push: it writes four decimals and reads MO8b 0.061 px against 0.04. (MO8)

### T6. Projection-truth checklist (from D5)

Run this at the premiere venue, or in an equivalent hall, with the real projector. Do it at the venue visit by Sun 17 Jan 2027 (TD-L2b, W-56) with the test clip only, never the film. Run the film-specific items again at the Mon 22 Feb rehearsal (G-REHEARSE, W-52), and on the day.

**The test card.** It is a short 24 fps video with:

- PLUGE (black-level bars) and a 21-step grey ramp [39].
- The two grey step scales of SMPTE RP 431-2 Tables A.2 and A.3 [91]: 10 steps from black to white and 10 steps from black to dark grey, each pattern 20% of the picture height by 80% of the width, generated by the same code and audited before they are played.
- A dark gradient.
- Colour bars.
- Three skin-tone stills.
- A type-size ladder, with x-height from 1.5% to 4% in 0.5% steps.
- A line ladder: 1, 2 and 3 px lines, in black and red.
- A textured pan at 0.10, 0.143, 0.2 and 0.3 frame widths per second, generated by the same code and audited before it is played (`pan_estimator.py`; FQ3).
- A speech passage with numbers.
- At the TD-L2b visit, the 60 to 90 s venue test clip with no personal content (W-17, W-56). Thirty seconds from the actual film are played only at the Mon 22 Feb rehearsal (W-52).
- The A/B push card, as its own file: `python3 -I research/cinematic-quality-fixtures/ab_push_card.py OUTDIR` (add `--still` with any 16:9 image of at least 3840 by 2160 for a real print). It has three Pillow-against-`zoompan` pairs and a seven-rung injected-jitter ladder, 85 s, with its measured answer key and a recording sheet (M-C13). Run it on the real projector from the front and back rows at the TD-L2b venue visit (15 minutes; the roadmap has it on Sunday 17 January 2027). Reading rule (J): MO8a = half the measured MO8a of the lowest front-row "yes", never above the lowest "maybe". Until it has been run, MO8a's 0.05 px is a derived bound, not an observed one.

The A/B push card exists and its answer key was checked on the decoded file; the rest of the card is still to build, and none of it has been run at a venue (TODO(research)).

| # | What passes on a laptop and fails on a 6 to 10 m screen | Check | Threshold | Source |
|---|---|---|---|---|
| 1 | Small type | Type ladder read from the back row | Every line marked "carries information" is readable; font 5% or more of height, x-height 2.5% or more, at 5 screen heights. Captions: x-height 3.1% or more at 6 screen heights (J); `FontSize=23` meets it in every font tested, `FontSize=20` does not for Carlito or FreeSans | [47] with the derivation in the notes |
| 2 | Text near the edge | Safe-area overlay | Inside 5% margins; faces not clipped | [45] |
| 3 | Fast pans | Pan test | No visible strobe at 0.143 frame widths per second. Faster needs blur or a declared whip | [41] |
| 4 | Crushed shadows | PLUGE and 21-step ramp, with the lights as they will be at the event. Count the RP 431-2 dark steps you cannot tell from black with the event lights on: 0.5 lux hides steps 1 to 3, 2 lux hides 1 to 5, 5 lux hides 1 to 8 (M, FQ5) | The first two steps above black are distinguishable from black (J). Story-critical detail above 10% signal | [39][33][91] |
| 5 | Brightness | Lumens and screen area, or a meter | About 45 nits or more at screen centre for a cinema-like feel. Below 30 nits, lift the grade using the venue's measured shadow compensation (J). Reference white: 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2), ST 431-1 Table 1 [92]; gamma 2.6 ±5% in a theatre [91] | [91][92][33] and the lumen arithmetic in `venue_calc.py`; [35] superseded for these figures |
| 6 | Gamma and colour | Skin-tone stills beside the laptop; reference gamma from the playback path | Faces not orange or grey; shadows not milky; decision recorded | [33][37] |
| 7 | Banding | Dark gradient, full screen | No visible steps at normal seat distance | (M): 26 vs 100 levels; [44] |
| 8 | Aliasing and thin lines | Line ladder | 2 px lines stable; 1 px red line visibly weaker (expected) | (M) |
| 9 | Grain against compression | 30 s sample in the venue's actual file or DCP (the test clip at TD-L2b; 30 s of the film at the Mon 22 Feb rehearsal) | Grain visible but not smeared; no mosquito noise around type | [42][34] |
| 10 | Judder | Pan test through the venue chain | Even cadence | [41] |
| 11 | Resolution scaling | 1 px checker pattern | No moiré from the projector's scaler; text sharp | [34] |
| 12 | Picture modes | Menu inspection | Motion smoothing, sharpening, noise reduction and dynamic contrast off; overscan off. Record the mode used | [38] |
| 13 | Speech intelligibility | Number passage read back at the back row; and STI by a STIPA app (AudioTools STIPA Basic, iOS only [103]) or Room EQ Wizard's indirect method (free [104]) if available; otherwise the 100-word read-back at the back row, scored in words correct | STI 0.60 or higher; otherwise the 100-word read-back at the back row: 90 or more correct passes, under 80 fails, 80 to 89 repeat with a new list (FQ8; UNVERIFIED against a meter) | [48][103][104][105] |
| 14 | Captions | Back-row read | Readable without leaning. Caption x-height 3.1% or more at 6 screen heights (J; see item 1). Run `caption_xheight.py` once on the maker's Windows ffmpeg with the chosen caption font | [47] |
| 15 | Faces in group photos | Back-row identification of the featured person | Featured person's head at least 8% of picture height, or a move that brings it there (J) | (J) |

### T7. Test-screening protocol (from D6)

**Purpose.** Find problems you cannot see yourself, and check that a public room reads the film. Strangers cannot judge truth or likeness. You keep a veto on facts about her.

**Timing (decided, W-43 and W-08).** Picture lock is set for Saturday 6 February 2027 [P4]. The brief's week 17 is 7 to 13 February 2027 (Mon 8 to Sun 14 Feb in the register). A screening that late can change only sound, grade, titles, captions and trims of about 2%. The register decides two sessions:

- **S1:** three strangers, the slice chapter, in the slice-review week (about 20 December 2026). Changes are cheapest then.
- **S2:** three to five strangers, the locked cut, in week 17, with one viewer over 65 and, if possible, one teenager with a guardian (W-43).

There is no one-session option: Sat 13 Feb is G-MIX, the latest acceptable lock, not a choice (W-08, W-43). The stranger count is three (S1) and three to five (S2); the written sheet (questions A to H) replaces a three-question read. The production-scale calendar already holds the W9 and W17 slots, so no new date is needed. If you decline strangers, the fallback is the cold self-read (48 hours unopened), and then the Fable advisor's rubric pass is mandatory in that slot.

**Recruitment without revealing who she is.**

- **Who:** adults, three to five, who have never met her and will not meet her. They are not in her social circle and do not share close acquaintances with the family. At least one should be film-literate, because the others may be too kind.
- **Pretext (truthful and partial):** "I'm finishing a short animated film about one woman's life that will be shown at a gathering. I need people who don't know her to watch it and tell me where it fails. It takes about 90 minutes. Please don't share anything about it before it's shown." Do not say whose life. Do not say it is a surprise.
- **Privacy:** show it on your own laptop or a borrowed projector, in a neutral place. No copy leaves the room. Phones are away. No video is recorded.
- **Redacted cut (your decision):** surname, street names and phone numbers are blurred or bleeped, and you say openly that details have been hidden. If redaction hurts the specificity too much, choose strangers in a different city.
- **Dignity:** show only what is cleared for the public cut. Hard chapters stay out by default [P4].
- **Thanks, not payment.** The notes suggest a meal or $10 to $20 each. The cost is unverified (J).
- **Consent:** a one-page written consent to view, and to the privacy request. Keep it offline.

**Sequence (about 90 minutes).**

1. Room: lights as they will be at the event. Level the sound before the audience sees it (the source does it after the makers' own first viewing) [70]. Use slates over any missing parts [70].
2. Brief (30 seconds): "Please watch without talking. I will not answer questions until the end. I am looking for problems."
3. Screen the whole cut with no pauses [70].
4. Two minutes of silence to write, alone.
5. **Written sheet (before any discussion; anonymous; on paper):**
   - A. One word for how it felt.
   - B. On a printed timeline, mark each moment you drifted, got confused, or noticed something that looked wrong, fake or computer-made.
   - C. In three sentences, who is she?
   - D. Which scenes do you think were re-creations rather than real photographs? How could you tell?
   - E. Were the girl, the young woman and the older woman the same person? Where did you doubt it?
   - F. Was there anything you could not read or hear?
   - G. Which moment will you remember tomorrow?
   - H. Was any part too long or too short?
6. Round-robin group discussion. You stay silent except to say "say more". Ask project-specific worries last, for example about a transition, so you do not sway opinions [70].
7. Close: thank them, and repeat the privacy request.

**What not to ask.** "Did you like it?" invites politeness. "Would she love it?" nobody can know. "Should I cut X?" invites fixes. Anything that reveals the family, the surprise or the venue. Leading questions about tells, such as "did the faces look fake?", before the unprompted marks.

**How to weigh the notes.**

- A problem marked by three or more of five viewers (or two of three) is a fix. Marked by two of five, investigate. One person's taste is logged and not acted on, unless it confirms a doubt you already had [70].
- Believe the diagnosis and discount the prescription. Gaiman's rule, paraphrased: people are almost always right that something is wrong, and almost always wrong about how to fix it [71]. Translate each note into the thing behind it. "I was bored" may mean pacing or stakes [70].
- Failed comprehension (C, D or E answered wrongly) outranks taste.
- More than two independent AI-tell marks per minute in a chapter sends that chapter back to the tell catalogue (T9).
- You keep the veto on facts about her. Dignity decisions are yours, flagged by the Fable advisor [P4].
- Log everything in the decision log, with the action taken or the reason for no action.

With three to five viewers you cannot estimate rates. You can only find problems. Use counts, not percentages.

**Pass or fail for the cut.** At least 80% of viewers (four of five, three of four, or three of three) identify the reconstructions correctly (D) and say it is one person across ages (E). No unread text (F). No chapter above two tell-marks per minute.

### T8. Logs and sheets (from D7)

**Decision-log entry (architecture-decision-record style [72])**

```markdown
## DL-014 Hold on twos for paper layers, ones for camera
Date: 2026-12-04 · Status: accepted · Supersedes: none
Context: slice shots 3 and 7 shimmered when the paper wobble ran on ones; Sprite Fright-style twos rule noted [26].
Decision: We will run paper wobble on twos and keep camera and type on ones.
Consequences: calmer texture; camera can still feel smooth; the T6 test needs twos detection on drawn layers.
Evidence: LJ-C01-S003_v004, S007_v005 · Reversible: yes · Review at: week 9 drift check
```

Rules for the log: keep each entry to one page. Never delete an entry. Mark superseded ones instead. Do not reuse numbers [72]. Taste drifts over sixteen weeks, so run a drift check at weeks 5, 9, 13 and 17 (J). Re-score six frozen slice shots on the T4 rubric without looking at the old scores. A change of more than one point on any criterion means taste has moved. Update the bible on purpose, or correct the new shots.

**Chapter motion lint output (a spec, not code)**

```json
{"shot": "LJ-C01-S014", "ease_class": "out", "axis": "push", "duration_s": 5.2, "magnitude_pct": 4.1,
 "cv": 0.92, "ends_ratio": 0.45, "peak_pos": 0.0, "settle_ok": true, "twos": false, "roughness": 0.11,
 "mo8a_px": 0.004, "mo8b_d4_px": 0.005, "family_key": "out|push|3-6|3-6"}
```

**Weekly review card (one page).** Date. Shots reviewed. 48-hour passes done. Blind A/B results. Three tells found. One decision logged. One anchor-frame comparison: better, same or worse.

### T9. AI-tells catalogue (from Q7)

Status key: **ALLOWED** is fine under the principles and the label ladder. **LABEL Lx** is allowed with that ladder label and a `steps.csv` note [P2]. **BANNED** is not allowed in the public cut.

The sources for tells are mostly 2026 vendor and trade pieces, which are weak evidence [19]. The detection methods are ours unless a source is named.

| # | Tell | Cause | Detection | Fix | Status |
|---|---|---|---|---|---|
| 1 | **Face drift** | Generators re-synthesise faces per clip; iterative edits accumulate change [62][59][65] | Frames at 0, 25, 50, 75, 100% at 100%; landmark alarm at 2%; maker's line-up (A3) | Do not generate faces. Keep the original face region; 2.5D from the photo; clips 3 to 5 s; fixed seed; always re-anchor to the original | Environment motion with face kept from L1/L2: **LABEL L4b**. Whole-frame image-to-video on a face-bearing photo: **LABEL L4b only if A3 passes**, otherwise **BANNED**. Deliberate face regeneration or animation: **BANNED**. Faces of the dead: **BANNED by default in the public cut** (delta to `ai-imagery.md` principle 7, Step 8 and Decision 4: under the sole keeper nobody can be asked before the premiere, so environment and parallax motion only; revisit after the reveal with written consent from next of kin) |
| 2 | **Flicker** | Per-frame generation or frame-by-frame upscaling | Flicker index on a static region (M: 0.000 static; 2.58 injected) | Non-generative deflicker; composite the static background from one frame; lower generative strength | Non-generative deflicker **ALLOWED (L1)**; generative deflicker **LABEL L4b** |
| 3 | **Morphing** | No persistent 3D; clip-level sampling | Step every 6th frame; count objects and fingers | Shorter clips; mask the moving region; re-roll | Visible morphing **BANNED**. Morph between two different people **BANNED**. Classic morph of two real photos **ALLOWED (L4a)** [P2] |
| 4 | **Plastic skin** | Restorers can "reconstruct features that may no longer exist" (a 2026 guide, search-result only) [63]; CodeFormer trades fidelity for quality via a coefficient [63] | 100% crop A/B against a plain upscale; skin high-frequency energy outside 60 to 140% of the plain upscale is suspicious (J) | No restoration if possible; plain upscale; if restored, weight 0.7 to 1.0 and blend 40 to 60% back | Restoration **LABEL L2**. Skin smoothing or beauty filters **BANNED** |
| 5 | **Invented detail** (teeth, eyelids, jaw, ears, jewellery) | Face prior fills in missing detail | Landmark overlay; count teeth and jewellery; compare at 200% | Reject the result | **BANNED** ("reject any result with new teeth, new eyelids or a changed jaw" [P2]) |
| 6 | **Warped hands** | High-variance anatomy [19] | Step frames; count digits on every visible hand | Crop or hide. L5 hands are hand-made by the bible's rule | Generative hands in photo shots **BANNED**. L5 hands hand-made, never generated |
| 7 | **Gibberish text** | Diffusion text rendering [19] | Read every visible word at 100% and compare with source | Typeset all text; leave source text soft rather than "fix" it | Generated text **BANNED** |
| 8 | **Over-smooth motion** | Model priors; a raw lerp in code | CV under 0.12 (M); no settle | Authored easing with settle; holds. Danse Macabre's team "repeatedly reintroduced imperfections when frames looked too stable" [21] | **BANNED** (lint) |
| 9 | **Uncanny eyes** | Weak eye modelling; animated stills | Stop on the eyes at 100%; compare gaze with source; any blink in a clip made from a still | Keep eyes from the photo; stylised eyes drawn by the bible's rules | Animating a real face's eyes, blinks or gaze **BANNED** |
| 10 | **Generic AI lighting** | Model average [5][17] | Lighting-tag lint across a chapter; compare light direction with the photo's own shadows | Per-era lighting spec taken from the photographs | Allowed only if it matches the source light. Otherwise fails review |
| 11 | **Generic composition** | Training average | Subject-position histogram across a chapter; swap test | Layout comes from the photo and the cut-or-move rules | Fails review |
| 12 | **Synthetic palette** | Model grading defaults [19] | ΔE00 to era swatches; chroma percentile | Grade to the script | Fails review |
| 13 | **Texture crawl** | Diffusion noise per frame | Flicker index on a flat patch; step three consecutive frames | Composite a static plate; use L4a | Fix or cut |
| 14 | **Hallucinated background** | Inpainting, outpainting, restoration | Diff mask against source; list every changed region in `steps.csv` | Clone only (L1); crop instead of outpaint | Invented people **BANNED**. Invented objects **LABEL L2 or L4b**, with an "invents" note |
| 15 | **Upscaler artefacts** (halos, waxy texture) [19] | Over-strong sharpening or generation | 200% crop at edges and in large textured areas | Lower strength; avoid repeats | **LABEL L2** |
| 16 | **Colourisation errors** [P2] | A guess at colour | Compare with family memory or other colour photos; skin ΔE00 against the era swatch | Mute skin; caption "colours estimated" | **LABEL L2** |
| 17 | **Age blending** | Identity-age trade-off [60][61] | Age line-up against the board | One reference set per age; never "age up" | Synthesising a different age of her **BANNED** |
| 18 | **Speech or lip-sync from a still** | Audio-driven models | Any mouth movement in an image-to-video clip | Never request it [P2] | **BANNED** |
| 19 | **Voice tells** (TTS plateau, no breaths) [19] | TTS prosody | Listen with the picture off | Real recordings only | Voice cloning **BANNED** (charter) |
| 20 | **Mirror, reflection and physics errors** [19] | No world model | Check every reflection | Remove the reflection or hand-make it | Fix or cut |
| 21 | **Soft generated video, scaled up to a 2K screen** | Native model resolution | Compare at 100% on the venue screen | Use generated video for small inserts only; L4a for key shots | **LABEL L4b**, small inserts only |
| 22 | **Finish used as a mask** | Over-finishing | Finish-off test (FN2) | Fix the defect or cut the shot | Fails review |
| 23 | **Repeated pattern grain** | Short baked loops | Autocorrelation at the loop length (M: 1.00 at lag 16) | At least 48 distinct frames; seeded offsets | Fix |

---

## Decisions you'll need to make

Our current lean is marked. Where the notes give no lean, it says so.

| # | Decision | Options | Our current lean |
|---|---|---|---|
| 1 | **Runtime** (short, mid-length or feature) | Short, mid-length, feature | Defaulted in the register (W-01, W-02, W-03; [DECISIONS.md](../DECISIONS.md)): plan 9 minutes until H is in writing (Sun 15 Nov), then 12 if H is 16 or more, 9 if H is under 14, and 12 between 14 and 16 only if the maker adds hours or buys captions. 15 to 18 is a stretch confirmed only at G-SLICE (Sun 20 Dec). F-0 is 6. The charter calls it the biggest lever on quality and schedule. |
| 2 | **Playback path** | (a) DCP: grade for BT.1886 at 2.4, convert with the matching input-gamma setting, test with a real cinema server. DCP-o-matic is described as free and open-source [58]. (b) HDMI or USB file: grade at 2.4 in a dim room, or 2.2 if the lights stay up, and set the projector's gamma to match. | The venue's written answer, due Sun 15 Nov, decides file or DCP (W-17); the default is the 1080p24 H.264 venue file. For a dim room, the notes default to 2.4. The DCP path allows a test DCP on a real cinema server, which the notes recommend before lock. Practitioners say "the only reliable check is a properly calibrated cinema screening" [37]. The theatrical-delivery track owns the choice. |
| 3 | **Venue facts** | You supply: venue type, screen size, projector model, who runs AV, ambient light | The neutral ask goes out by Fri 6 Nov and the six answers are due Sun 15 Nov (W-17, O-21). Until you supply them, every brightness number here is a scenario, not a fact. |
| 4 | **Strangers' screenings** | Decided (W-43; [DECISIONS.md](../DECISIONS.md)): two sessions. S1 with three strangers to her on the slice chapter (about 20 Dec 2026), S2 with three to five strangers to her on the locked cut (week 17). The written sheet (T7 questions A to H) replaces a three-question read. There is no one-session option: Sat 13 Feb is G-MIX, the latest acceptable lock (W-08). | Two sessions. S1 arrives early enough that structural notes are still cheap. If you decline strangers, the fallback is the cold self-read (48 hours unopened), and the Fable advisor's rubric pass is mandatory in that slot. |
| 5 | **Redacted cut for strangers** | Redacted (blurred names, streets and numbers, stated openly), or the full cut with strangers from another city | Defaulted to a redacted copy (W-43). Redaction may cost specificity. |
| 6 | **Reconstruction marker** (bible decision 6) | Material, paper frame and a persistent mark, or other | Set by the register: her own hand-made material, filled at G1 (Sun 15 Nov) from the maker's week-1 answer (W-38). Original voxel assets only and never the marker (D-23); the Minecraft rule is settled [57]. |
| 7 | **Grain and paper source** | Scan of her print backs, or a CC0 texture | Her print backs (W-38, decision 8). Use a CC0 texture only after its licence is checked (TODO(research)). |
| 8 | **8-bit or 10-bit venue file** | Design visible grain or paper that survives 8-bit, or use a 10-bit encode if the venue's playback machine accepts it | Design for visible texture, and test both at the venue. The register's default venue file is 8-bit yuv420p H.264 (W-17), made from the 10-bit master (W-15). Software players usually accept 10-bit. A forum summary, seen only in search results, says many hardware players do not. |
| 9 | **Training a model on her face** | No, or yes with local training, deletion afterwards, labels, and your explicit sign-off | Decided: no (D-16). She cannot consent to a model trained on her face without knowing about it. |
| 10 | **Who signs likeness** | You alone, or someone else | Decided: you alone (W-40; charter and notes). Five of five, passed twice, 48 hours apart (J). |
| 11 | **Sensitive chapters** (loss, illness, separation, money, conflict) | In, handled carefully, or out | Decided (D-04): one-key-three-guards. Out by default [P4]; you decide each one twice, 72 hours apart, on a decision sheet with the Fable advisor's written flag. |
| 12 | **Who else is in on the project** | No one, or bring someone in later | Decided (D-03): only-me, recorded 2026-10-18. You are the only person on the project; the one re-open point is TD-L2c, Sun 3 Jan 2027. |
| 13 | **Hold lengths and the 48-hour rule** | Use the notes' starting values, or others | Start with the notes' values and calibrate on the first five slice shots (J). Burns argues that duration can carry meaning, citing a 33-second zoom [82] (search-result only). |
| 14 | **Life eras for the colour strip** | Five placeholder eras: 0 to 12, 13 to 22, 23 to 35, 36 to 49, and 50 plus | Use them as placeholders until we see her material (W-39). |
| 15 | **Motion estimator scope** | Push-ins only; push-ins and translation-only pans; or also orbits and multi-layer moves | Push and pull ease by `zoom_velocity_classifier.py`, and MO8 by `mo8_audit.py` on any renderer's output. Pans: speed by `pan_estimator.py` (validated, M-C9) and ease by `pan_ease_classifier.py` (validated on translation-only pans, M-C11; the truth curves were the classifier's own library except five CSS curves). Orbits, rotations, mixed zoom-and-pan and layers with different eases are spec-only and reported `unknown`. |
| 16 | **Maker review time per shot** | Budget the maker minutes by shot class (T1 preamble), or cut the Maker items for class A | The minimum set for class A and the full set for classes B to D. All minutes are estimates (J) to time on the slice. The per-minute total goes to `production-scale.md` as a delta. |

---

## Pitfalls

1. **Default settings.** `power1.out` everywhere, uniform stagger, the same slow zoom on every photo [69][P3].
2. **Stacked finish.** Grain, vignette, letterbox and flare together read as a template and hide weak design [P4].
3. **The laptop check.** A shot that passes on a 50 cm laptop can fail on a 6 to 10 m screen. Type, banding and judder show up first on the big screen.
4. **Gamma.** The same dark code value is 37% darker on a 2.6 display than on a 2.4 display, and 58% brighter on a 2.2 display (our arithmetic). Shadows, where faces in dark rooms live, move most. The playback path is decided by the venue's written answer, due Sun 15 Nov (W-17).
5. **Looped grain.** An 8-frame grain loop held on twos repeats every 16 frames (0.67 s). Autocorrelation is 1.00 at that lag, against 0.00 for fresh grain (M). Flat areas will "breathe" in a pattern.
6. **Plain digital noise.** Real film grain is spatially correlated, and independent noise per pixel reads as digital (J) [42].
7. **Banding.** A smooth dark ramp in 8-bit video showed 26 levels, against 100 at 10-bit (M). Encoders remove invisible dither, so add visible texture instead [44].
8. **Thin lines.** A saturated 1 px red line kept about 70% of its contrast after H.264 at 1080p (M). Keep strokes at least 2 px, with no saturated hairlines.
9. **ffmpeg `zoompan` for finals.** It snaps to whole pixels, so slow moves shimmer (M). On real prints its centre jitter is 0.13 to 0.59 px against the MO8a limit of 0.05 px, and 0.63 px in the usual `-pix_fmt yuv420p` command line (M-C7b, M-C10). A relative roughness test alone would pass a fast push from a 4K source (M-C7b) and the GSAP `scale` tween that MO8b fails (M-C10), which is why roughness is informational only. Use `zoompan` for proofs only.
10. **Mirroring a photograph.** It flips a hair parting, a wedding ring hand, and any text. That breaks "real memories stay real" [P5].
11. **Trusting laurels.** Runway's festival is run by a tool vendor, and its prizes include credits [1][2]. The "Best Film" claim for *Costa Verde* is unconfirmed. The WAIFF prize list shows *Costa Verde* with the CapCut Prize, and it names a different film as Best WAIFF Film [7]. The Nowness page returned a 503 error [20] (TODO(research)).
12. **Trusting vendor numbers.** Shot-ratio figures from tool vendors are marketing. Treat them as themes, not data [15].
13. **Identity.** No validated method exists for a stylised, cross-age face. Identity models trade age change against identity [60][61]. Iterative edits drift [62]. In one audit of 5,040 edits by three open-weight portrait editors, 62 to 71% of outputs lightened skin [59]. Likeness is fragile when the face is small, shadowed or turned away [65] (a vendor guide, search-result only). Face-recognition scores come from real photographs, not stylised faces [78].
14. **Trusting AI critics.** One review found "about one checkable claim in four held up" [68]. Vary the order, anonymise, and aggregate. Use a critic only for judgement items.
15. **Tool shutdowns.** Critterz, an OpenAI-backed feature, reportedly missed its Cannes 2026 debut after OpenAI shut down Sora, and its team went looking for a new AI partner (Bloomberg, 22 May 2026; search-result only) [11]. Keep every tool replaceable.
16. **Three strangers cannot give rates.** They can only find problems. Use counts.
17. **Redaction costs.** Blurring names and places may remove specificity, which is the thing that makes the film hers.
18. **Estimator limits.** The zoom estimator was tested on synthetic push-ins at 540p and, as a reconstruction, on three public-domain prints at 1080p (M, M-C7b). It cannot see overshoot or tails below about 10% of peak, and it reads a 4% push as about 4.3% on every renderer, so it is a relative tool, not a ruler (M-C10). Pan speed is validated (M-C9), and pan ease on translation-only pans (M-C11, truth curves from the classifier's own library except five CSS curves). Two-layer pans: family right in 4 of 4, travel under-read (M-C11); layers with different eases stay spec-only.
19. **Venue unknown.** The brightness and contrast numbers here are scenarios. A hall with the lights on can cut contrast far below a cinema's. One measured example (search-result only) gave 57:1 for a standard 1.0-gain screen with the room lights on, against over 8,000:1 for the projector with the lights off [49]. The cinema reference is ambient on the screen with the projector off below 0.01 cd/m² in a Review Room and below 0.03 cd/m² in an Exhibition Theater (SMPTE RP 431-2 s6.1) [91]; a hall with the lights on will not come close.
20. **Honest labelling will be read by a mixed public.** Cannes' main festival director has talked about films one day being labelled "made without artificial intelligence" [9]. Some viewers at a public screening will be hostile to AI. The disclosure card, the end-credit cue sheet and a visibly small, human-led AI use are our answer [P1][P2].
21. **The 48-hour rule is untested.** It is practitioner advice, not a controlled study [75]. Treat it as a habit to test, not as proof.

---

## Best references

1. **Making Flow, interview with director Gints Zilbalodis** (blender.org), https://www.blender.org/?p=93732. Fetched. Why: the team size, render times, and "no compositing" approach behind a coherent look [23].
2. **Flee interview** (Seventh Row), https://seventh-row.com/?p=45371. Fetched. Why: the art bible in practice, with "this is good" and "this is not good" examples and the rule about eyes [27].
3. **Ralph Eggleston talks Inside Out** (Animation World Network), https://www.awn.com/animationworld/ralph-eggleston-talks-inside-out. Fetched. Why: how a colour script is made, and why it changes when the story does [31].
4. **White Paper on Ambient Light Compensation for Filmmaker Mode** (UHD Alliance), https://alliance.experienceuhd.com/wp-content/uploads/2025/10/UHDA-White-Paper-on-Ambient-Light-Compensation-for-Filmmaker-Mode-v4-clean.pdf. The notes read all four pages. Why: why a lit room hides shadows, with a gamma table for compensation [33].
5. **Banding in gradients** (Fora Soft), https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps. Fetched. Why: why dark gradients band, and why dither must sit close to the final encode [44].
6. **Does size matter for reading?** (Legge and Bigelow, *Journal of Vision*), https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf. Read locally. Why: the basis for the type-size rule for a big screen [47].
7. **CRAFT.md** (bishpls/animation-pipeline), https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md. Fetched. Why: timing, holds and review rules. It is a third-party guide, so check its numbers before using them [68].
8. **Six Tips for a Successful Test Screening** (Frame.io), https://blog.frame.io/2017/07/06/successful-test-screening-tips/. Fetched. Why: room setup, sound levels and question order for a test screening [70].

---

## Sources

Format: [n] title, URL, date, note. "Fetched" means the page was opened. "Search-result only" means the claim was seen only in a search result, or the page did not load. Numbers follow the research note; [123] and [124] were found while closing review round 3 and are listed here first.

**AI film festivals, AI-assisted films, critics**
- [1] AIF 2026 (Runway AI Festival), https://aif.runwayml.com/. Fetched 2026-10-18. Fourth edition, winners, prizes, jury, partners.
- [2] Runway AI Film Festival 2026: Winners and Films (hollywood.ai), https://hollywood.ai/awards/runway-ai-film-festival. Fetched 2026-10-18. Third-party aggregator; runtimes, entry rule, judging criteria.
- [3] "Prompting is not directing" (Robert Gaudette interview, Envato Elements Learn), https://elements.envato.com/learn/a-face-only-a-mother-could-love. 2026-07-29. Process; no selection ratio stated.
- [4] Runway Showcases AI-Generated Shorts to Packed Audience (letsdatascience, summarising THR and Business Insider), https://letsdatascience.com/news/runway-showcases-ai-generated-shorts-to-packed-audience-3825c8ad. 2026-06-19. Audience, "boring", two weeks of 17-hour days.
- [5] "What's left is you": AI is the elephant in the room of Europe's biggest animation festival (Euronews), https://www.euronews.com/2026/07/12/whats-left-is-you-ai-is-the-elephant-in-the-room-of-europes-biggest-animation-festival. 2026-07-12. Annecy; "faster without AI"; "the average or the mean".
- [7] WAIFF prize list, https://worldaifilmfestival.com/prize-list/. Fetched 2026-10-18. 2026 winners and the CapCut Prize. Organiser and sponsor names read from logos (low confidence).
- [9] Cannes 2026 rolls out red carpet amid AI spat (France 24), https://www.france24.com/en/culture/20260512-cannes-film-festival-opens-grappling-with-ai-and-hollywood. 2026-05-12. Frémaux on labelling; Meta sponsorship.
- [11] Critterz at Cannes 2026 (Deadline; Bloomberg "misses Cannes debut after OpenAI shut Sora"), https://deadline.com/2026/05/open-ai-produced-animated-family-film-critterz-cannes-1236879586/ and https://www.bloomberg.com/news/articles/2026-05-22/ai-cartoon-critterz-misses-cannes-debut-after-openai-shut-sora. 2026-05. Search-result only (paywalled).
- [12] How Good is Sora Actually? Interview with the filmmakers behind Air Head (No Film School), https://nofilmschool.com/sora-ai-filmmaker-interview. 2024-04-02. Two to three seconds kept from 20-second generations; post work.
- [13] At the AI Film Festival, humanity triumphed over tech (TechCrunch), https://techcrunch.com/2024/05/11/at-the-ai-film-festival-humanity-triumphed-over-tech. 2024-05-11. Critical review of the 2024 festival; older than six months, historic.
- [15] AI Video Generations Per Usable Shot (invideo.io FAQ), https://invideo.io/faq/how-many-ai-video-generations-do-you-need-per-usable/. July 2026. Vendor; search-result only.
- [17] 10 Animators to Watch Discuss AI, the Future and the Human Hand (Variety), https://variety.com/2026/film/awards/10-animators-to-watch-ai-animation-future-scad-1236894996/. 2026. Search-result only. The SCAD panel's advice to be "more specific, not less."
- [19] The AI Slop Aesthetic: 12 Tells That a Video Was Made by AI (Opus Pro), https://www.opus.pro/blog/ai-slop-aesthetic-12-tells. 2026-04-17. Vendor; fetched.
- [20] NOWNESS Experiments: Costa Verde, http://amp.nowness.com/story/costa-verde-leo-cannone. Search-result only (503).

**Non-AI calibration and style and identity practice**
- [21] This Annecy animated short took 11 years and 75 oil paintings (Creative Bloq via Yahoo), https://www.yahoo.com/entertainment/movies/articles/annecy-animated-short-took-11-120000725.html. 2026-06-09. Danse Macabre; fenced AI pass.
- [22] How Fusion Studio and expert compositing skills brought Danse Macabre to life (Creative Bloq via Yahoo Tech), https://tech.yahoo.com/general/articles/fusion-studio-expert-compositing-skills-090000004.html. 2026-09-23. Global grain last; compositing steps.
- [23] Making Flow, interview with director Gints Zilbalodis (blender.org), https://www.blender.org/?p=93732. Fetched 2026-10-18. Team, render times, no compositing.
- [24] Yes, one animator made the CG animated feature Away on his own (Cartoon Brew), https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html. 2019-06-06. Solo workflow; shortcuts. The article says Away was worked 'seven days a week'.
- [25] How Spider-Man: Into the Spider-Verse's technical wizardry works (Gizmodo), https://gizmodo.com/how-spider-man-into-the-spider-verses-technical-wizard-1831179866. 2018-12-18. Twos as a creative call.
- [26] Sprite Fright style guide (Blender Studio blog; BlenderNation 2021-06-20), https://studio.blender.org/blog/sprite-fright-style-guide and https://www.blendernation.com/2021/06/20/sprite-frights-style-guide-published/. 2021. Summary only.
- [27] Flee interview (Seventh Row), https://seventh-row.com/?p=45371. Fetched 2026-10-18. Art bible; good and not good examples; eyes.
- [28] What is an art bible? (Oleander Studios), https://www.oleanderstudios.com/what-is-an-art-bible-examples-practical-tips/. Fetched 2026-10-18. Typical sections.
- [30] Character Sheets: The Blueprint for Consistent Animation (cg-wire), https://blog.cg-wire.com/character-sheet-animation. Updated 2026-03-26. Contents of a character sheet.
- [31] Ralph Eggleston talks Inside Out (Animation World Network), https://www.awn.com/animationworld/ralph-eggleston-talks-inside-out. Fetched 2026-10-18. Colour script as shorthand of emotion.
- [32] Lou Romano's colour script for Pixar's Up (Slashfilm), https://www.slashfilm.com/503975/cool-stuff-lou-romanos-color-script-for-pixars-up/. 2009-06-02. Colour arc; fetched.

**Colour, projection and finish**
- [33] White Paper on Ambient Light Compensation for Filmmaker Mode (UHD Alliance), https://alliance.experienceuhd.com/wp-content/uploads/2025/10/UHDA-White-Paper-on-Ambient-Light-Compensation-for-Filmmaker-Mode-v4-clean.pdf. File dated 2025-10-08. 5 cd/m² reference surround; gamma table; all four pages read.
- [34] Digital Cinema System Specification v1.4.4 (DCI), https://documents.dcimovies.com/DCSS/42cfeb997ae72dd484f7b027547e6e0bfad43ecf/Digital%20Cinema%20System%20Specification.pdf. Approved 2024-01-03. 12-bit XYZ; 2K 2048x1080 at 24 or 48 fps; 250 Mbit/s. Relevant sections read; SMPTE RP 431-2 is normative but not read.
- [35] DCSS Compliance Test Plan 1.4.1 (DCI), https://documents.dcimovies.com/CTP/release/1.4.1/. Ambient under 0.01 cd/m² fetched. Superseded for these figures by [91][92][93]: reference white 48.0 cd/m² (14.0 fL), ±3.5 Review Room, ±10.2 Theater (37.8 to 58.2), ST 431-1 Table 1 [92]; gamma 2.6 ±5% in a theatre [91]; ambient 0.01 cd/m² Review Room and 0.03 cd/m² Exhibition Theater, RP 431-2 s6.1 [91].
- [37] DCP-o-matic user mailing list, colour conversion threads, https://lists.dcpomatic.com/hyperkitty/list/users@lists.dcpomatic.com/message/27TBTWCAFUWRT73LEI2VANYMJOQWDXWL. Search-result only; practitioner opinion.
- [38] Filmmaker Mode feature summaries (Tom's Guide and others), https://tomsguide.com/features/what-is-filmmaker-mode-heres-why-you-should-use-this-picture-perfect-setting. Search-result only; launch-era descriptions (2019 to 2020).
- [39] Black Level (PLUGE) test (TestUFO), https://www.testufo.com/blacklevels. Fetched 2026-10-18. How to read a PLUGE.
- [40] Delta-E CIEDE2000 documentation (MetricGate), https://metricgate.com/docs/delta-e-ciede2000/. Fetched 2026-10-18. Interpretation bands for flat patches.
- [41] Camera panning speed (RED), https://www.reddigitalcinema.com/red-101/camera-panning-speed. Undated. Seven-second rule; shutter angle.
- [42] Film Grain Synthesis for AV1 Video Codec (Norkin and Birkbeck, Netflix and Google), https://norkin.org/pdf/DCC_2018_AV1_film_grain.pdf. 2018. Grain statistics and compression difficulty; read locally.
- [44] Banding in gradients (Fora Soft), https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps. Fetched 2026-10-18. Causes; CAMBI; dither advice.
- [45] EBU R 95: Safe areas for 16:9 television production, https://tech.ebu.ch/docs/r/r095.pdf. June 2017, Ver. 1.1 (2016 errata). Action 3.5%, graphics 5%; read locally.
- [47] Does size matter for reading? (Legge and Bigelow, *Journal of Vision* 11(5):8), https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf. 2011. Fluent range 0.2 to 2 degrees of x-height; read locally.
- [48] Speech transmission index (Wikipedia), https://en.wikipedia.org/wiki/Speech_transmission_index. Fetched 2026-10-18. IEC 60268-16 bands.
- [49] Ambient-light contrast measurements (Sound and Vision, Planar Xscreen), https://soundandvision.com/node/82167. Search-result only (403): 57:1 and 194:1 with lights on.
- [50] Light Wrap operator (Vindral Composer docs), https://composer-docs.vindral.com/operators/operators-light-wrap.html. Fetched 2026-10-18. Chain order; parameters.
- [51] BokehDiff: Neural Lens Blur with One-Step Diffusion (arXiv 2507.18060), https://arxiv.org/pdf/2507.18060. 2025. Search-result only; halos at depth edges.
- [52] TIFF/EXIF tag FocalLengthIn35mmFilm (0xA405), https://awaresystems.be/imaging/tiff/tifftags/privateifd/exif/focallengthin35mmfilm.html. Search-result only.
- [53] The Kid Stays in the Picture (kottke), https://kottke.org/03/07/the-kid-stays-in-the-picture. 2003. Fetched; technique.
- [54] Meaning in Motion: Ken Burns and His 'Effect' (Poynter), https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect. 2007-06-21. Fetched.
- [55] 6 'Rules' for Good Cutting According to Walter Murch (No Film School), https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch. 2016. Fetched.
- [56] SIL Open Font License FAQ, https://openfontlicense.org/ofl-faq/. Fetched 2026-10-18. Video titling is a listed permitted use (FAQ 1.1); embedding is answered for documents and files (1.12), not video. Commercial fonts are out (W-21; T2 decision 4) [88][89][109].
- [57] Minecraft Usage Guidelines excerpt (local, captured 2026-10-18), research/sources/minecraft-usage-guidelines-2026-10-18.txt. Physical locations; name as title.
- [58] DCP-o-matic, https://dcpomatic.com/. Fetched 2026-10-18. "Free and open-source"; licence not stated on the page.

**Identity and AI technique**
- [59] Toward Trustworthy Portrait Editing: Evaluation of Demographic Misrepresentation in I2I Models (arXiv 2602.16149), https://arxiv.org/abs/2602.16149. v1 2026-02-18; v3 2026-06-04. 62 to 71% skin lightening; fetched.
- [60] AgeBooth (arXiv 2510.05715), https://arxiv.org/abs/2510.05715. 2025-10-07. Age-specific LoRA fusion; fetched. The identity-versus-age wording comes from a search-result summary, not the abstract.
- [61] DiverAge (arXiv 2606.04881), https://arxiv.org/abs/2606.04881. 2026-06-02. Cross-age identity drift; fetched.
- [62] FLUX.1 Kontext (arXiv 2506.15742), https://arxiv.org/abs/2506.15742. 2025-06. Claims improved multi-turn consistency; no limits on the abstract page.
- [63] CodeFormer (NeurIPS 2022), https://proceedings.neurips.cc/paper_files/paper/2022/hash/c573258c38d0a3919d8c1364053c45df-Abstract.html. 2022. Fidelity and quality coefficient. The "features that may no longer exist" line is from a 2026 guide seen only in search results.
- [65] Qwen-Image-Edit-2511 likeness LoRA guide (RunComfy), https://www.runcomfy.com/trainer/ai-toolkit/qwen-image-edit-2511-likeness-custom-lora. 2026. Vendor; search-result only.
- [68] CRAFT.md (bishpls/animation-pipeline), https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md. Fetched 2026-10-18. Timing, holds, review rules.
- [69] GSAP eases, https://gsap.com/docs/v3/Eases/. Fetched 2026-10-18. Ease families; default `power1.out`.
- [70] Six Tips for a Successful Test Screening (Frame.io), https://blog.frame.io/2017/07/06/successful-test-screening-tips/. 2017-07-06. Fetched.
- [71] Neil Gaiman's rule on feedback (Goodreads mirror of his blog), https://www.goodreads.com/author_blog_posts/9436922-remember-when-people-tell-you-something-s-wrong-or-doesn-t-work-for-th. Search-result only. Originally in the Guardian's "Ten rules for writing fiction", 2010-02-20; that page was not fetchable.
- [72] Documenting Architecture Decisions (Michael Nygard), https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions. 2011-11-15. Fetched.
- [73] In praise of the squint (Painter's Keys), https://painterskeys.com/praise-squint/. Search-result only.
- [74] The Animator's Survival Kit, table of contents (Internet Archive text), https://dn721807.ca.archive.org/0/items/taskav-01/The__Animator%27s_Survival_Kit%5B1%5D_text.pdf. Search-result only. Contents seen; the timing chapter not read.
- [75] Proofreading guidance on delay and fresh eyes (Ragan), https://www.prdaily.com/?p=256303. Search-result only. Practitioner advice; no controlled study.
- [76] Measurements, 2026-10-18, cloud container, synthetic material only. Scripts are in research/cinematic-quality-fixtures/ with a README. M-C1 zoom-velocity classifier; M-C2 flicker index; M-C3 grain-loop autocorrelation; M-C4 dark-ramp banding; M-C5 grain bit cost; M-C6 thin-line survival; M-C7 `zoompan` against sub-pixel roughness, reported as 1.7 to 2.7 times rougher on two synthetic stills (advisor reproduction 2026-10-18: Pillow 0.19, zoompan 0.33). M-C7b to M-C9 are in [108] and M-C10 to M-C14 in [122].
- [78] InsightFace mirror pages (ArcFace, LFW and AgeDB-30 accuracies), https://github.com/Soldie/insightface-Rec.Face. Search-result only. A community mirror, not the official repository.
- [80] Creating Motion in Stills: How to Animate a Photo in Post with the Parallax Effect (PetaPixel), https://petapixel.com/2013/11/19/creating-motion-stills-animate-photo-post-parallax-effect. 2013. Search-result only.
- [82] Ken Burns on the 33-second zoom (CineD), https://www.cined.com/?p=406363. Search-result only.
- [88] Monotype Fonts "Service & License Terms" (Enterprise), https://www.monotype.com/legal/eula (redirects to https://www.monotypefonts.com/pages/eula). Read in full 2026-10-18; no revision date. Enterprise rights other than those for a Licensed Application end with the agreement.
- [89] Monotype Fonts Create + Deploy and Create + Pitch EULAs, same site (publisher content feed). Read in full 2026-10-18; no revision date. Every grant is "during the Term"; nothing says what happens to output after it. The Pitch video grant excludes public deployment.
- [91] SMPTE RP 431-2:2011, D-Cinema Quality, Reference Projector and Environment (approved 6 April 2011; state "stabilized") — https://pub.smpte.org/latest/rp431-2/rp0431-2-2011.pdf — read in full (14 pages).
- [92] SMPTE ST 431-1:2006, D-Cinema Quality, Screen Luminance Level, Chromaticity and Uniformity (approved 18 April 2006; listed "active") — https://pub.smpte.org/latest/st431-1/st0431-1-2006.pdf — read in full (5 pages).
- [93] SMPTE ST 428-1:2019, D-Cinema Distribution Master, Image Characteristics (approved 12 February 2019) — https://pub.smpte.org/latest/st428-1/st428-1-2019.pdf — read in full (8 pages).
- [103] Studio Six Digital, AudioTools "STIPA Basic", https://studiosixdigital.com/audiotools-modules-2/speaker-test-modules/stipa-basic/. Vendor page, copyright 2025; iOS only; not checked against a meter.
- [104] Room EQ Wizard, features page https://www.roomeqwizard.com/features.html (copyright 2026) and its offline-measurement help. Lists STI by the indirect method per IEC 60268-16:2020; check that the installed version shows it.
- [105] Speech transmission index (Wikipedia), https://en.wikipedia.org/wiki/Speech_transmission_index. Fetched 2026-10-18. STI bands and the word, syllable and sentence scores; the standard itself was not read (paywalled). The 100-word read-back rule in T6 item 13 is built on this table (J).
- [108] Measurements, 2026-10-18, cloud container, public-domain prints only. M-C7b `zoompan` against sub-pixel resampling on three prints; M-C8 caption x-height; M-C9 pan estimator validation. Scripts and result files in research/cinematic-quality-fixtures/.
- [109] Adobe Fonts Service Product Specific Terms, effective 7 October 2024, "Replaces all prior versions", https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Adobe-Fonts-Product-Specific-Terms-en_US-20241007.pdf. Read in full as text; section 3.1 grant "only for as long as you maintain an uninterrupted Adobe Subscription Plan"; the words video, film, broadcast and exhibition do not appear. The licensing FAQ returned 403 and is unread.
- [115] Visual acuity (Wikipedia), https://en.wikipedia.org/wiki/Visual_acuity. Summary read 2026-10-18; vernier acuity "about 8 arc seconds" is tagged [citation needed] there. Superseded in this playbook by [123].
- [122] Measurements, 2026-10-18, cloud container, public-domain prints only. M-C10 renderers against MO8; M-C11 pan ease classifier; M-C12 Windows-safe scripts and runner; M-C13 the A/B push card; M-C14 the venue calculator. Scripts and `r2_*` result files in the fixtures folder.
- [123] Hu, Ayton and Jolly, The Clinical Use of Vernier Acuity: Resolution of the Visual Cortex Is More Than Meets the Eye, Frontiers in Neuroscience 15:714843 (2021), https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.714843/full. Fetched 2026-10-18 (first 100,000 of 137,794 characters). Introduction: "The vernier threshold (smallest detectable offset) for humans is as low as 2 to 5 arcseconds", citing Westheimer and McKee (1977) and Westheimer (1987), whose papers were not read. A static, best-case figure; nothing on moving pictures.
- [124] GSAP community forum, "Laggy jerky animation pan zoom test v3 vs v2", https://gsap.com/community/forums/topic/22980-laggy-jerky-animation-pan-zoom-test-v3-vs-v2/. Fetched 2026-10-18. A GSAP maintainer (20 February 2020) calls the jerk "just a decimal precision thing" and adds a decimal in a later release; no setting is named. The measured fix is to write the transform yourself (M-C10).

**Project playbooks and charter**
- [P1] `playbooks/animated.md`, playbooks/animated.md. Disclosure convention; era-by-medium rules.
- [P2] `playbooks/ai-imagery.md`, playbooks/ai-imagery.md. The label ladder L0 to L5; restoration and motion routes.
- [P3] `playbooks/agent-pipeline.md`, playbooks/agent-pipeline.md. Gates G0 to G6; baked grain; banned easing.
- [P4] `reviews/02-film-briefs-review.md`, reviews/02-film-briefs-review.md. Picture lock on 2027-02-06; the strangers' screening in week 17; hard chapters default out.
- [P5] `CHARTER.md`, CHARTER.md. Principles and review rubric.

---

## Changelog

- **v1, 2026-10-18.** First version. Built from `research/cinematic-quality.md` (researcher's note, same day) and `CHARTER.md`. Written by a scribe agent. Reviewed for consistency with the labels and gates in `playbooks/ai-imagery.md` and `playbooks/agent-pipeline.md`.
- **v2, 2026-10-18.** Round-1 review nudges applied (Fable advisor): MO1 split into MO1 (spec, Crit) and MO1b (pixels, Maj, `unknown` for uncovered moves); MO8 given its first pass rule, with M-C7 reported as 1.7 to 2.7 times (rule replaced in v4); TY1 scoped to type we set, with the Q10 exemption, TY4 added and captions tied to `format.md` Step 8; maker review minutes by class added (Decision 16); source citations corrected (EBU R95, Away, OFL, grain-loop origin); faces of the dead written as a delta; likeness decoys changed to public-domain stand-ins or the maker's own face; Exercise 4 and the fixtures README updated for the roughness check.
- **v3, 2026-10-18.** Review round 2 (Fable advisor) applied: MO8 became a pixel rule on centre and edge jitter (since refined in v4); MO6 is a pixel audit with `pan_estimator.py` (pan speed validated), with a pan clip on the test card; projection figures cite SMPTE RP 431-2, ST 431-1 and ST 428-1, with [35] superseded for them; caption x-height is tied to `FontSize=23` (3.1% floor) in step 12, TY1 and T6; the six venue questions are in step 1; the stranger count is three to five (T7, Decision 4); the sound-levelling wording keeps the Frame.io citation exact; the estimator's provenance now includes the M-C7b prints.
- **v4, 2026-10-18.** Review round 3 (Fable advisor) applied in place: MO8 is MO8a centre jitter at most 0.05 px on the delivered file and MO8b fourth-difference edge jitter at most 0.04 px on the master before the encode, with roughness and the reference ratio informational (T1, step 9, Pitfall 9, Exercise 4, Open gaps, T8 lint keys); renderer rules in step 9 and T5 items 26 and 27; pan ease validated on translation-only pans (MO1b, MO2, MO9, step 9, Decision 15, Pitfall 18); venue neutral ask, `venue_calc.py`, the A/B push card and the RP 431-2 grey scales in step 1 and T6; the STI routes in T6 item 13; Adobe and Monotype font terms in T2 decision 4 and step 12; the 48 cd/m² reference cited to [92]; the Windows check, the leitmotif from the line-up, and the open gaps brought up to date; the "proposed changes" list for other playbooks removed (the same rows are in the research note's Deltas table).
- **v5, 2026-10-18.** Reconciled with DECISIONS.md (2026-10-18): playback path and venue ask dated (ask by Fri 6 Nov, answer Sun 15 Nov, W-17); venue visit by Sun 17 Jan with the test clip only and the Mon 22 Feb rehearsal (W-52, W-56); two stranger sessions decided and the one-session option removed (W-43, W-08); OFL fonts only (W-21); reconstruction marker is her own hand-made material and voxel is never the marker (W-38, D-23); decisions 1, 2, 3, 9, 10, 11 and 12 marked decided or defaulted; maker minutes restated at 8 shots a minute and 5% hero shots (W-34, W-51).

**Open gaps (TODO(research)).**

- No film was watched. Shot-level claims about the festival films, *The Kid Stays in the Picture*, *Up*, and the Burns films are unverified. See Exercise 1.
- SMPTE RP 431-2, ST 431-1 and ST 428-1 were read in full on 2026-10-18 [91][92][93]. Their figures replace the search-result figures attributed to [35].
- Venue facts are unknown: type, screen size, projector, ambient light, playback path, seat distances. The maker supplies the six answers (step 1) and a photo of the projector label; until then every brightness, gamma and type-size figure is a scenario, and MO8a's 0.05 px is a derived bound, not an observed one.
- Hold lengths on large screens and the 48-hour rule have no empirical source. Both are practitioner heuristics (J).
- No validated method exists for stylised cross-age identity. Face-recognition reliability on stylised faces is unknown.
- The zoom estimator was validated on synthetic zoom push-ins at 540p and, as a reconstruction, on three public-domain prints at 1080p (M-C7b). Pan speed is validated (M-C9), and pan ease on translation-only pans (M-C11; the truth curves were the classifier's own library except five CSS curves). Orbits, rotations and layers with different eases are spec-only; two-layer pans: family right in 4 of 4, travel under-read. Real hand-drawn layers, real family scans with film grain and a real parallax pan were not used. The zoom estimator cannot see settle or overshoot below about 10% of peak.
- The renderer results (M-C10) come from one print and one push profile (cosine, 4% in 4 s; Blender 2% in 2 s). Untested: Blender at 96 frames or with an orthographic camera, EEVEE on a GPU, Chromium with a GPU, FilmCraft's Windows build through `filmcraft_push.py`, and a pan or orbit on each renderer.
- Several 2026 festival and trade sources were paywalled or blocked: THR, Fast Company, Variety, Bloomberg, Deadline and Screen Daily. They are cited from search-result text only.
- Gaudette's hours rest on a secondhand report. The *Costa Verde* "Best Film" laurel is unconfirmed. The Nowness page returned 503.
- Not yet researched: real scanned grain libraries and their licences; the *Up* colour script images; DCP-o-matic and DaVinci Resolve on Windows (the free edition's features are unconfirmed); and the ambientCG licence. The Windows run of `windows_check.py` has not happened (FQ15). All three STI routes (T6 item 13) are unverified against a calibrated meter (FQ8).
- MO8 limits: centre jitter at most 0.05 px and fourth-difference edge jitter at most 0.04 px (FQ9, FQ10, M-C10) are derived, not observed. The visibility of 0.1 to 0.3 px of random frame-to-frame jitter on a screen is untested (FQ9): the A/B card has been generated and its key checked, but not run on a projector. The best-case static alignment threshold is 2 to 5 arc seconds [123]; no source on random jitter in moving imagery has been read. The limits are still to be confirmed on the slice (J).
- Decisions now in the register ([DECISIONS.md](../DECISIONS.md)): the Minecraft rule (D-23: original voxel assets only, never the marker); the runtime (W-01 to W-03); the playback path (W-17, venue answer due Sun 15 Nov); strangers on a redacted copy at S1 and S2 (W-43).
