# Animated and documentary exemplars: how to make a life look honest and alive

Track: animated · Draft v0.1 · 2026-10-18 · For the maker (a motivated learner)
Built from research/animated.md (Sonnet researcher, 2026-10-18) and CHARTER.md. Numbers in brackets, like [1], point to the Sources list at the end. Anything marked TODO(research) is still open. The research team read written breakdowns, not the films, so no beat-level claim here has been checked against footage.

## Why this matters for our life journey

Your mother's life has years with no camera in them. Some years have a shoebox of prints. Others have nothing at all. Filmmakers have faced this problem for decades, and several have solved it in ways that are moving and honest.

Our charter sets the rule: real memories stay real. We may restore, restyle, animate and connect real photos and stories. We may not invent events or put words in anyone's mouth. Any scene we draw or build must be visibly a reconstruction. The films in this playbook follow that rule on purpose. Most of their methods are cheap: interviews, one drawing material, a clear card at the start, and restraint.

Some methods are expensive. Flee had about fifty people working on its animation at once [2]. Rocks in My Pockets took years [21]. We are a learner with an AI team and a deadline of 27 February 2027. So we copy the cheap methods and treat the expensive ones as references only.

## Core principles

1. **Her voice comes first.** Record the people who knew her before you design a single frame. Flee's team built a sound-and-storyboard master before animating [3]. Ryan was built on about 20 hours of recorded interviews [11]. Rocks in My Pockets recorded its voice-over first and used the script as its blueprint [21].

2. **One hand-made material for everything that was never photographed.** The Missing Picture's clay figures are a material that is hard to mistake for a photograph [6][7]. Pick one material for our piece (cut paper, clay or blocks) and use it for every invented scene.

3. **Say so once, at the start.** Flee opens with a card saying that names and places were changed to protect its subjects [1]. Ours should say which scenes are reconstructed and what material marks them.

4. **Replace the stand-in with the real thing.** Tower lets the real survivor replace the actress who played her [13]. Waltz with Bashir ends by dissolving into real news footage [16]. Every reconstructed person or place should eventually meet a real photo, voice or object, or stay clearly labelled.

5. **Restraint is the craft.** Ken Burns called "mindless, anxious movement for the sake of movement" the enemy [37]. Pick two or three moments and make them perfect [28][29]. Where the picture can carry the feeling, drop the dialogue and sound effects. The Up team cut both from its montage and said the sequence felt more emotional for it [56][58].

6. **Objects and interfaces keep time.** Up's coin jar is broken open early by a flat tire, a broken leg and a storm [57]. Google's Parisian Love moves through eleven searches in about 52 seconds [54]. If she left letters, messages or a notebook of recipes, those can be the clock.

7. **Specific beats generic.** The Wonder Years' fake home movies work because the action is generic enough for any family to see itself in [62]. For a real person, generic is the failure mode. Use her kitchen, her car, her sayings and her songs (after a licence check).

8. **Change the medium, not just the filter. Build it to last.** Era shows most in grain, frame shape, tint and crop, more than in palette alone [88][91]. Snow Fall's own files still resolved fourteen years after launch, while its third-party video script had been redirected [39]. Plan for a self-contained build and a plain video file.

## How to do it, step by step

Steps 1 to 4 can start now. Steps 5 to 11 are the production pattern. The exercises in the next section teach each step on practice material.

**Tools.** We do not yet know which free editors are installed on your PC. TODO(research): confirm the exact apps and versions you have. The notes name these options: Inkscape for vector cut-outs, GIMP or Krita for photo layers, DaVinci Resolve for editing and its Fusion 3D tools, Blender for camera projection, and ffmpeg for converting files. Their free status is background knowledge and was not re-checked this session. TODO(research): confirm licences and download links from each official site. The Blackmagic page lists DaVinci Resolve Studio 21 at $295 [34]. The page does not say whether the free edition includes Fusion's 3D tools. TODO(research): confirm that.

1. **Check the rules before you touch any material.** We are still in the LEARN phase. Use practice images only: public-domain pictures, or your own photos that have nothing to do with her. Family photographs wait until the pipeline is locked, as the charter requires. Keep practice and family files off shared computers, phones and auto-syncing photo libraries, because family members may see them.

2. **Inventory each chapter.** For each chapter, list what exists: photographs (with date and place), letters, messages, recordings, objects, and who can confirm each fact. Mark the gaps. This list is the input to every choice below. The story gathering itself belongs to the story and surprise-ops tracks, and it stays covert.

3. **Record the voices, later and carefully.** When gathering starts, record the people who knew her. Use the closed-eyes method: the speaker lies back, closes their eyes and describes a place in the present tense, covering materials, colours, light, sounds and feelings [2]. Keep the original audio untouched. Do not start any real interviews until the surprise-ops track has set the covert process.

4. **Cut the audio, then storyboard to it.** Cut the best 60 to 90 seconds and leave the natural pauses in. Sketch six to ten frames, one per phrase, and let the voice set the timing [3][21]. A sketch that needs music to work is not ready yet.

5. **Choose the time-passing device for each chapter.** Use the material you have.
   - An object that appears across years, such as a jar, a tie, a car or a kitchen table: this is Up's device [56][57].
   - Letters, messages or other written words: show them, one line per year [49][54].
   - Eight or more portraits across years: a portrait ladder, with the eyes aligned in the same frame [70][72].
   - Places but no people: a scale zoom, or a model of the place [6][43].
   - One strong photograph: one long, slow hold, used once per chapter at most [37][38].
   - Nothing at all: show the gap with a black frame or a single object [62].
   Every device must say something true about her life. If it does not, cut it.

6. **Set the reconstruction look.** Choose one material for every invented image. The options are cut paper drawn in a vector editor, clay or paper sets photographed [6][21], or simple blocks. Write a one-page art bible with three "good" and three "not good" examples, and a rule for how hands and faces are drawn [1][2]. Flee's team kept a document like this, down to how to draw a hand or an eye [1][2].

7. **Animate with restraint.** The default is a still photo with one slow move (a push, a pull or a pan) across about 3 to 5 percent of the frame width, held for no more than 8 to 10 seconds. These limits are the researcher's judgment from the notes, not a tested rule. Alternate still and moving shots so the motion keeps its meaning. For depth, use one of two routes:
   - Manual layers, the classic method. Outline each element with the pen tool, feather the edge slightly, expand the selection by 10 to 15 pixels, fill the gap behind it with content-aware fill or cloning, place the layers in 3D with a 28mm-style camera, and keyframe a slow push [28][29]. Free routes in the same spirit include Fusion's 3D tools in Resolve [33] and Blender camera projection [104].
   - Automatic depth parallax. DepthFlow is free and open source under AGPL-3.0. It runs locally, needs Python 3.10 or newer, adds no watermark, and uses a depth map so near things move faster [30][31]. Its documentation was blocked for the researcher. TODO(research): confirm the command syntax and the Windows setup.
   Use parallax only on your best photographs (see Exercise 5).

8. **Prepare the sources.** Old prints are soft and grainy. The 110 film of 1972 was small and is often "rather grainy and unsharp" [93]. Scan small prints at 600 ppi. The handout minimum is 400 ppi for prints, and slides and film need 2000 to 3000 dpi [96]. By the notes' arithmetic, a 3.5 by 5 inch print at 600 ppi gives about 3,000 pixels on the long side, which is enough for a 1080p push-in. Dye fades unevenly, and shadows and cyan lose the most [89]. Correct each colour channel separately rather than with one filter, and keep the print's own character.

9. **Put the era on the new layer only.** Apply grain, a 4:3 crop or a tint to title cards and reconstructions, not to the family photographs themselves. Blue Spill filmed a hand-cut title card on real Super 8 stock so it would sit with the family's cine film [64]. A typical Super 8 look uses 12 to 18 frames a second, a 4:3 frame, reduced sharpness, grain and a slight colour tint, with stabilisation turned off [88]. Do not add fake date stamps. Do not age material that is already aged [89].

10. **Build the honesty layer.** Write the disclosure card: one short paragraph at the start that names which scenes are reconstructed and what material marks them [1]. For each reconstructed person or place, write the reveal: which real photo, voice or object replaces it, and at which point in the piece. If no real item exists, the stand-in stays labelled.

11. **Test, deliver, and check it works.** Watch on the screen she will actually use, such as a TV, tablet or laptop. Ask a viewer who has not been briefed to name the reconstructed scenes. Export H.264 MP4 at 1080p [78]. Keep a plain video file as the master delivery, even if an interactive version also exists. Interactives that died in the research died through a runtime or a third party, not through their files [46][47]. For any web version, build a self-contained folder: no content-delivery-network scripts, no third-party video host and no analytics [39][46]. Offer a static fallback [100]. Keep masters separate, with a README that explains how to rebuild the delivery files. Test any web version in a current browser, because an HTTP 200 response does not prove that it plays [39]. TODO(research): run that browser test on the Snow Fall page.

## Learn-by-doing exercises

Every exercise uses practice material. The time estimates are ours, not sourced. Each exercise ends with a "good" line you can check yourself. If your PC struggles with memory, run practice renders in the cloud session, but only with practice images.

### Exercise 1: Watch one beat sheet with a stopwatch

- **Goal:** learn how three pieces time their beats. Use Up's opening montage (about 4.5 minutes [56]), Parisian Love (about 52 seconds in one analysis, and 60 seconds in a comScore snippet [54][55]) and Dear Sophie (about 90 seconds [49]).
- **Steps:** (1) Watch once with no notes. (2) Watch again with a stopwatch. Log every beat with a timestamp, what changes (an object, the camera or the sound) and the type of cut. (3) Compare your log with the written breakdown in the notes and list every disagreement. (4) Find out where each piece can be watched legally. TODO(research): verify streaming availability, which the research did not check. The Dear Sophie link in the notes is a mirror; no official upload was confirmed [50].
- **Time estimate:** 2 to 3 hours.
- **Good:** one beat sheet per piece, with at least ten beats for Up. You can say which beat carries the feeling and why, and whether the sound was stripped. Your disagreement list goes to the team watch session the research asked for. TODO(research): schedule that session with a stopwatch.

### Exercise 2: Closed-eyes interview, practice round

- **Goal:** learn to draw out sensory detail in the present tense [2].
- **Steps:** Ask a friend who knows this is practice, and who is not one of her relatives, to sit back and close their eyes. Ask them to describe a room from their own childhood in the present tense, for example "I'm at the table. What is on it?" Ask about materials, colours, light, sounds, smells and feelings. Do not interrupt. Record it, then transcribe the first five minutes.
- **Time estimate:** 1 hour for the session and 1 hour for the transcript.
- **Good:** at least 15 concrete details in the transcript. You can name three that you could draw. The speaker says afterwards that they felt listened to.

### Exercise 3: Audio-first cut

- **Goal:** let the voice set the picture.
- **Steps:** Using the recording from Exercise 2, or a public-domain speech clip, cut a 60-second piece that keeps its pauses. Write six storyboard frames, one for each phrase. Add one object that appears twice.
- **Time estimate:** 3 hours.
- **Good:** the 60 seconds stand up without music. The frames follow the phrasing. The repeated object appears twice and changes between the two appearances.

### Exercise 4: One material, one disclosure card

- **Goal:** build an invented scene in one visible material and disclose it.
- **Steps:** Invent a small room or street and label it clearly as invented. Make it in cut paper drawn in a vector editor, or as a simple block build. Film a slow move of about 8 seconds across it. Write a three-sentence disclosure card that names what is invented.
- **Time estimate:** 4 hours.
- **Good:** a viewer can tell the scene is drawn or built without being told. The card names what is invented. Every invented scene in the piece uses this same material.

### Exercise 5: Parallax spike on practice snapshots

- **Goal:** find out what photo animation can do with small, soft prints.
- **Steps:** Pick three small, soft practice snapshots that are public-domain or otherwise non-personal. Scan each at 600 ppi [96]. Method A: outline three layers in GIMP or Krita, fill the gaps, bring the layers into Resolve (Fusion) or Blender, place them in depth, and keyframe a push of 3 to 5 percent over about eight seconds [28][29][33]. Method B: run DepthFlow, if your PC has Python 3.10 or newer and a suitable graphics card [30][31]. TODO(research): confirm the DepthFlow syntax and Windows setup. Compare both methods at 1080p on a full screen.
- **Time estimate:** 6 to 8 hours for the first pass.
- **Good:** no gaps show at 1080p, and faces are clean at the push-in. You can name the snapshot that fails and say why. If only a slow flat push works for a snapshot, that is a valid result, and the notes suggest it (researcher's judgment). The spike on her own photographs is a production step, to be done after the lock.

### Exercise 6: Portrait ladder with practice portraits

- **Goal:** learn alignment and rhythm across years.
- **Steps:** Gather eight portraits of one practice person taken across several years. Mark both eyes on each one. Align every portrait to the same eye positions and the same crop, using a grid in your photo editor, the same idea as the overlay grid in the Everyday app [71]. Hold each portrait for one to two seconds, with a short dissolve of about half a second (our judgment). Keep the total under 30 seconds. Automatic five-point landmark alignment, as used on Kalina's "7777 Days", is free to run with dlib, but its setup was not tested [72][77].
- **Time estimate:** 3 hours.
- **Good:** the eyes do not jump between frames. The rhythm changes once. You can explain why you cut rather than morphed.

### Exercise 7: A title card on paper

- **Goal:** make an era cue physically, then film it.
- **Steps:** Print or hand-letter a title card on paper. Film it with a phone, held by hand, with stabilisation off, in ordinary room light [88]. Grade it to a 4:3 frame with grain and a slight tint, using Resolve or another free editor. Put it side by side with a digital title card and compare.
- **Time estimate:** 2 hours.
- **Good:** the card looks filmed, not added. The grade touches only this card.

## Decisions you'll need to make

For each decision, the options come first, then our current lean. A lean is a starting point, not a decision. Each one stays open until you decide.

1. **How invented scenes look.**
   - Options: (a) one hand-made material, such as cut paper, clay or blocks; (b) full character animation in the style of Flee; (c) actors re-performing on camera and traced frame by frame, as in Tower.
   - Our lean: (a), with slow moves, a disclosure card and reveals [1][6][13]. Option (b) is far too large for this schedule [2]. Option (c) needs actors and a rotoscope workflow, so we do not recommend it.

2. **How much motion.**
   - Options: a still with one slow move; parallax on the best photographs; full animation.
   - Our lean: a still with one slow move as the default, and parallax only for the photographs that pass Exercise 5. The notes suggest picking a few sections and making them perfect [28][29].

3. **Which device carries each chapter.**
   - Options: an object clock, an interface timeline, a portrait ladder, a scale zoom, or a long hold (see step 5 above).
   - Our lean: a repeating object as the main clock across the whole piece; a portrait ladder for the years that have photographs; an interface timeline only if she left written messages. This is judgment and has not been tested.

4. **Hard cut or morph between portraits.**
   - Options: a hard cut on aligned eyes, or a morph made with free frame-interpolation tools such as RIFE or FILM, marked on screen as a morph [77].
   - Our lean: a hard cut. It is cheaper and more honest, and interpolation shows artefacts between very different faces [77]. TODO(research): establish the tedium threshold for morphs, which the notes could not find. Our judgment is to keep any single morph or ladder between 20 and 90 seconds, with one idea and a change of rhythm halfway.

5. **Where personal files get processed.**
   - Options: your own PC; a cloud container, which the charter prefers for heavy work; or a hosted web tool.
   - Our lean: practice material can go anywhere. Family photographs stay on your machine until you decide otherwise. The charter forbids uploading personal material to a third party without your explicit say, so we use no hosted tool for family photographs. Immersity AI, for example, has a watermarked 720p free tier, and reviews disagree on its paid prices. TODO(research): confirm current pricing [35].

6. **Music.**
   - Options: a song she loved (which needs a licence); an original piece; the voice and the room sound alone.
   - Our lean: voice and sound first. Clear a licence before any song is used. Clearance can cost a great deal: Tarnation's budget rose from $218.32 to about $400,000, mainly for music and clips [65]. A private gift carries less risk than a public showing [78].

7. **The era look.**
   - Options: change the medium for each decade; a generic decade palette; a palette sampled from her own scans.
   - Our lean: sample the palette from her own scans, era by era, once you have them. Use the decade table only as a sanity check. The notes have no source for 2010s and 2020s palettes. TODO(research): find one.

8. **Format.**
   - Options: a film file, a web or scroll piece, or both.
   - Our lean: a plain MP4 always, plus a self-contained web version if the format track recommends one [46][47]. The charter lists format as an open decision for you.

9. **The trusted proxy for hard chapters.**
   - Options: name one close relative who sees the hard chapters first; or leave hard chapters out.
   - Our lean: name the proxy before drafting any hard chapter. The charter says a trusted close relative acts as her proxy for loss, illness, separation, money and conflict. Until then, those chapters stay on hold.

10. **How to show the hardest moments.**
    - Options: show them directly; imply them through an object or a voice; leave them out.
    - Our lean: imply them through an object or a voice, not through an image of harm. Dick Johnson Is Dead staged deaths with its subject's consent [68] (search snippet). Any staging of her life needs her proxy's agreement first.

## Pitfalls

- **Reel grammar.** Whip pans, beat-synced zooms and trending transitions are the anti-pattern the charter names. The notes list them but did not research them further. TODO(research): find a source on reel-grammar anti-patterns before anyone copies or rejects them.
- **The same move on every photo.** Uniform motion turns a memory into a slideshow. Alternate still and moving segments [79].
- **A swelling score doing the work.** One French review said Dear Sophie was "a bit too much like American soap operas", in the notes' translation [52]. Let the picture carry the feeling, and cut the music early.
- **Unlabelled fakes.** Stories We Tell mixed unlabelled Super 8 re-creations with real home movies, and critics split between praise and discomfort [66][67]. Its fake Super 8 is a good lesson in how convincing a fake can look. For factual chapters, do not copy the unlabelled approach, because charter rule 4 requires every reconstruction to be visibly one.
- **Selection by popularity.** Facebook's 2014 Year in Review put a photo of Eric Meyer's late six-year-old daughter under party graphics, because it had many likes and comments [81][82]. Select her photographs by hand, with the proxy.
- **Stacked era filters.** Avocado appliances, Cooper Black and heavy grain on every frame look like a costume [87][90]. Change the medium on the new layer only, and do not age scans that are already aged [89].
- **Faces at small sizes.** Depth maps and interpolation fail first on thin objects and on faces [27][77]. Keep push-ins gentle near faces, or cut instead.
- **AI face animation and restoration.** Not researched. TODO(research): research AI face-animation reactions, such as Deep Nostalgia, before any such tool is considered. Until then, do not use AI on any real person's face, and do not let restoration invent facial detail. The charter forbids animating a dead person's face and inventing speech (principle 4).
- **Runtime dependencies.** Flash-based interactives from several news sites broke when Flash support ended on 31 December 2020 [47]. Shared resources and third-party scripts also rot [46]. Self-contain the build.
- **Music clearance.** The Wonder Years' theme song disappeared from Netflix because relicensing was costly (search snippet) [105]. Check every song before you use it.
- **Surprise leaks.** Relatives' group chats, shared computers and cloud photo libraries can show her the work too early. The charter names all three. Keep drafts off them.
- **Phone "memory" features.** Phone and photo services add music, titles and transitions by theme, so every memory looks alike [83]. Do not run her photographs through them.
- **Tools that may not last.** DepthFlow is new: version 1.0.1 was published on 25 August 2026 [30]. Its documentation was blocked for the researcher. TODO(research): confirm the Resolve free-edition feature split. Keep a manual route working for every shot, so no single tool is a single point of failure.

## Best references (top 8)

1. **Flee, directed by Jonas Poher Rasmussen (2021).** Read the Hyperallergic interview at https://hyperallergic.com/697967/jonas-poher-rasmussen-interview-flee/ [1], and the Seventh Row interview at https://seventh-row.com/?p=45371 [2]. Worth your time for the disclosure card, the art bible, the closed-eyes interviews and the subject's review of the edit. TODO(research): confirm legal access to the film, and verify the unconfirmed 8mm-frame claim.

2. **The Missing Picture, directed by Rithy Panh (2013).** Read the Al Jazeera Q&A at https://www.aljazeera.com/amp/features/2014/3/1/qa-meeting-cambodias-oscar-nominee [5], the Documentary.org interview at https://www.documentary.org/column/cambodian-night-and-fog-filmmaker-rithy-panh-takes-khmer-rouge-genocide [8], and the MPR News piece at https://www.mprnews.org/story/2014/03/30/cambodias-missing-pictures-molded-from-directors-own-life [6]. Worth your time for a changed childhood home rebuilt in clay, and figures that thin as rations run out. TODO(research): watch the clay-to-archive cuts with a stopwatch.

3. **Tower, directed by Keith Maitland (2016).** Read the Documentary.org piece at https://documentary.org/feature/life-animated-how-doc-makers-heighten-perception-and-solve-problems-through-animation [13], and the Stanford Daily interview at https://stanforddaily.com/2016/11/11/tower-director-keith-meithland-talks-his-unique-documentary/ [14]. Worth your time for first-hand accounts only [15], and for the reveal of the real survivor. Note: the Stanford Daily link slug spells the director's name differently from the notes. We copy the link as recorded and have not re-checked it.

4. **Up, opening montage (Pixar, 2009).** Read The Ringer's making-of piece at https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of [56], and /Film's account of the late changes at https://slashfilm.com/1582050/up-opening-emotionally-devastating-pixar-multiple-last-minute-changes-exclusive [58]. Worth your time for objects that keep time, sound stripped away, and a camera that changes as the life changes. The Wikipedia page on the sequence [57] is a secondary list of beats.

5. **Ken Burns on restraint.** Read Poynter at https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect [37], and CineD at https://www.cined.com/?p=406363 [38] for the 33-second zoom (partial read). Worth your time for the rules on slow moves and on meaning.

6. **The Kid Stays in the Picture (2002).** Read kottke's summary at https://kottke.org/03/07/the-kid-stays-in-the-picture [24]. Worth your time for separated subjects panned at different speeds. TODO(research): read the DVD commentary, or the IndieWire interview at https://www.indiewire.com/features/general/interview-nanette-burstein-and-brett-morgen-on-their-robert-evans-doc-the-kid-stays-in-the-pictur-80275/ [22] and the Filmmaker piece at https://filmmakermagazine.com/archives/issues/summer2002/features/last_tycoon.php [23]. Both fetches were refused, so the tooling is still undocumented.

7. **Noah Kalina, "Everyday" and "7777 Days".** Watch the video at https://www.youtube.com/watch?v=6B26asyGKDo [69]. Read Laughing Squid at https://laughingsquid.com/noah-kalina-ages-over-7777-days/ [73] and kottke at https://kottke.org/21/07/half-a-life-in-2-minutes [72]. Worth your time for alignment on five face points, averaging the last 60 frames, and how the rhythm changes across 21 years. The original app's alignment grid is covered by TechCrunch at https://techcrunch.com/2011/03/21/everyday-iphone-app [71].

8. **Snow Fall (The New York Times, 2012).** Read the project at https://www.nytimes.com/projects/2012/snow-fall/index.html [39] and OpenNews's account at https://source.opennews.org/articles/how-we-made-snow-fall/ [40]. Worth your time for how a long web piece pauses for its media, and for where it broke: third-party video and analytics. TODO(research): test the page in a current browser. An HTTP 200 response is not proof of playback.

## Sources

Tier key: [P] creator, official or academic statement; [S] journalism, review or critical analysis; [T] Wikipedia, aggregator, forum, or a search-result snippet the researcher could not open in full; [V] verified by the researcher's own HTTP or oEmbed probe on 2026-10-18. Numbers match research/animated.md. Only the sources cited above are copied here, in the notes' wording.

- [1] Hyperallergic — How a Documentary Used Animation to Protect the Identity of Its Main Character (Flee interview) — https://hyperallergic.com/697967/jonas-poher-rasmussen-interview-flee/ — undated — [S] fetched: art bible, title card, Amin reviewed edit.
- [2] Seventh Row — Flee interview — https://seventh-row.com/?p=45371 — undated — [S] fetched: archive sources, Hopper/Metzler/Gronsky references, closed-eyes interviews, ~50 animators.
- [3] Documentary.org — Flee feature — https://documentary.org/node/36985 — undated — [S] fetched: reversed editing, looser trauma style, sound-and-storyboard master.
- [5] Al Jazeera — Q&A: Meeting Cambodia's Oscar nominee — https://www.aljazeera.com/amp/features/2014/3/1/qa-meeting-cambodias-oscar-nominee — 2014-03-01 — [S] fetched: clay model of childhood home, 500+ figures, propaganda traces.
- [6] MPR News — Cambodia's 'missing pictures' molded from director's own life — https://www.mprnews.org/story/2014/03/30/cambodias-missing-pictures-molded-from-directors-own-life — 2014-03-30 — [S] fetched: paper lilies, thinning figures, composer detail.
- [7] Cinema Scope — TIFF 2013: The Missing Picture — https://cinema-scope.com/cinema-scope-online/tiff-2013-the-missing-picture-rithy-panh-cambodiafrance/ — 2013 — [S] fetched: narrator not Panh, tableaux morts.
- [8] Documentary.org — Cambodian Night and Fog: Rithy Panh — https://www.documentary.org/column/cambodian-night-and-fog-filmmaker-rithy-panh-takes-khmer-rouge-genocide — undated — [P] fetched: Panh's own words on figurines.
- [11] Computer Graphics World — Psychorealism (Ryan) — https://cgw.com/Publications/CGW/2004/Volume-27-Issue-7-July-2004-/Psychorealism.aspx — 2004-07 — [S] fetched: Maya, Photoshop, Combustion, 20 hours of interviews.
- [13] Documentary.org — Life Animated: how doc makers heighten perception through animation — https://documentary.org/feature/life-animated-how-doc-makers-heighten-perception-and-solve-problems-through-animation — undated — [S] fetched: Tower additive layer, TVPaint, actress-to-real-Claire.
- [14] Stanford Daily — Interview: Tower director Keith Maitland — https://stanforddaily.com/2016/11/11/tower-director-keith-meithland-talks-his-unique-documentary/ — 2016-11-11 — [S] fetched: archive lacked close-ups; Staggs/Minnow Mountain.
- [15] Michael J Cinema — Keith Maitland on Tower — https://michaeljcinema.com/2016/12/01/keith-maitland-on-tower/ — 2016-12-01 — [S] fetched: first-hand accounts only.
- [16] Wikipedia — Waltz with Bashir — https://en.wikipedia.org/wiki/Waltz_with_Bashir — accessed 2026-10-18 — [T] fetched: Flash cut-outs, ending dissolve into news footage, structure.
- [21] Bostonia (Boston University) — From Sketch to Screen (Rocks in My Pockets) — https://www.bu.edu/bostonia/2016/from-sketch-to-screen/ — 2016 — [S] fetched: papier-mâché sets, 30,000 drawings, Photoshop/After Effects.
- [22] IndieWire — Interview: Nanette Burstein and Brett Morgen on The Kid Stays in the Picture — https://www.indiewire.com/features/general/interview-nanette-burstein-and-brett-morgen-on-their-robert-evans-doc-the-kid-stays-in-the-pictur-80275/ — undated — [T] snippet only (fetch returned HTTP 402 via redirect): "fairly accessible program".
- [23] Filmmaker Magazine — Last Tycoon (Kid Stays), Summer 2002 — https://filmmakermagazine.com/archives/issues/summer2002/features/last_tycoon.php — 2002 — [T] snippet only (fetch returned 403): 3D images, cut-outs, 800 photos in a minute.
- [24] kottke.org — The Kid Stays in the Picture — https://kottke.org/03/07/the-kid-stays-in-the-picture — 2003-07 — [S] fetched: subjects separated from backgrounds, different pan speeds.
- [27] Niklaus, Mai, Yang, Liu — 3D Ken Burns Effect from a Single Image — https://arxiv.org/abs/1909.05483 — 2019-09-12 — [P] fetched: depth, point cloud, inpainting.
- [28] PictureCorrect — Parallax Animation: Bringing Still Photographs to Life — https://www.picturecorrect.com/parallax-animation-bringing-still-photographs-to-life/ — undated — [S] fetched: Fellows' workflow.
- [29] Motion Array — Animate flat 2D images in After Effects (2.5D parallax) — https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/ — undated — [S] fetched: content-aware fill, 28mm camera, Puppet tool.
- [30] PyPI — depthflow — https://pypi.org/project/depthflow/ (JSON API https://pypi.org/pypi/depthflow/json) — [V] 2026-10-18: version 1.0.1, uploaded 2026-08-25, AGPL-3.0, Python >=3.10.
- [31] GitHub — BrokenSource/DepthFlow — https://github.com/BrokenSource/DepthFlow — fetched 2026-10-18: description, AGPL-3.0; docs https://depth.tremeschin.com/ returned HTTP 403.
- [33] Mixing Light — Introduction to Resolve Fusion's 3D Camera, Part 1 — https://mixinglight.com/color-tutorial/introduction-3d-camera-fusion-part1 — [T] snippet only.
- [34] Blackmagic Design — DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — 2026-10-18 — [P] fetched: Studio 21 $295, features list.
- [35] The Rundown — Immersity AI — https://www.therundown.ai/tools/immersity-ai — [T] snippet only; pricing from third-party reviews, conflicting; UNVERIFIED.
- [37] Poynter — Meaning in Motion: Ken Burns and His 'Effect' — https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect — undated — [S] fetched: "mindless, anxious movement," "all real meaning accrues in duration."
- [38] CineD — Ken Burns effect article — https://www.cined.com/?p=406363 — undated — [S] fetched (partial): 33-second Roebling zoom.
- [39] The New York Times — Snow Fall — https://www.nytimes.com/projects/2012/snow-fall/index.html — [V] 2026-10-18: HTTP 200, 177,243 bytes; own CSS, jQuery 1.7.1 and 30+ MP4/WebM assets 200; Brightcove script 301.
- [40] OpenNews Source — How We Made Snow Fall — https://source.opennews.org/articles/how-we-made-snow-fall/ — 2013 — [P] fetched: stack, constraints, reader fatigue.
- [43] Wait But Why — Your Life in Weeks (Tim Urban) — https://waitbutwhy.com/2014/05/life-weeks.html — 2014-05-07 — [P][V] fetched, HTTP 200.
- [46] eagereyes (Robert Kosara) — The bits are rotting in the state of data journalism — https://eagereyes.org/blog/2016/the-bits-are-rotting-in-the-state-of-data-journalism — 2016-07-14 — [S] fetched.
- [47] CNN (via KTVZ) — So much digital 9/11 coverage has disappeared — https://ktvz.com/lifestyle/technology/cnn-social-media-technology/2021/09/10/so-much-digital-9-11-coverage-has-disappeared-heres-why/ — 2021-09-10 — [S] fetched: Flash end 2020-12-31, NYT Ruffle.
- [49] Adweek — Google Chrome Spot Captures Girl's Entire Life in 90 Seconds — https://www.adweek.com/?p=131368 — 2011 — [S] fetched: credits, true-story-with-actors.
- [50] YouTube (CannesPredictions mirror) — Google Chrome "Dear Sophie" — https://www.youtube.com/watch?v=pzOBOuyr-EU — [V] oEmbed 2026-10-18: video exists; official Google upload not confirmed.
- [52] Blog du Modérateur — Une vie entière sur Google : la vidéo Dear Sophie — https://www.blogdumoderateur.com/une-vie-entiere-sur-google-la-video-dear-sophie/ — 2011 — [S] fetched: "a bit too much like American soap operas."
- [54] UMass Dartmouth Corridors — John Michael Bell, Analysis of Google's 'Parisian Love' — https://corridors.sites.umassd.edu/?p=213 — undated — [S] fetched: 11-query sequence, 52 s.
- [55] comScore — Why Parisian Love was one of 2010's best ads — https://www.comscore.com/Insights/Blog/Scoring-with-Super-Bowl-Advertising-Why-Google-s-Parisian-Love-Was-One-of-2010-s-Best-Ads — 2011-02-04 — [T] snippet only.
- [56] The Ringer — Up's first 10 minutes, making of — https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of — 2022-06-14 — [S] fetched: beats, ~4.5 min, 30-40 minutes cut, dialogue removed.
- [57] Wikipedia — Up opening sequence — https://en.wikipedia.org/wiki/Up_opening_sequence — accessed 2026-10-18 — [T] fetched: jar, ties, reception.
- [58] /Film — Up opening, multiple last-minute changes — https://slashfilm.com/1582050/up-opening-emotionally-devastating-pixar-multiple-last-minute-changes-exclusive — undated — [S] fetched.
- [62] Alphaville — Kathleen Williams on The Wonder Years credits — https://www.alphavillejournal.com/Issue12/HTML/ArticleWilliams.html — undated — [S] fetched: home-video markers, refreshed footage, generic action.
- [64] Blue Spill — Stiller & Meara: Nothing Is Lost — https://bluespill.co.uk/project/stiller-meara-i-nothing-is-lost/ — [P] fetched.
- [65] Independent magazine — Mind the Gap (Tarnation) — https://independent-magazine.org/2004/10/01/mind-gap/ — 2004-10-01 — [S] fetched: iMovie, $218.32, ~$400,000 clearance, cutting around the beat.
- [66] Documentary.org — Sarah Polley on Stories We Tell — https://documentary.org/node/33754 — undated — [P] fetched.
- [67] The A.V. Club — Stories We Tell — https://www.avclub.com/stories-we-tell-1798176746 — [T] snippet only.
- [68] NPR — Filmmaker Faces Her Father's Mortality By Staging His 'Death' Again And Again — https://www.npr.org/2020/09/30/918129488/filmmaker-faces-her-fathers-mortality-by-staging-his-death-again-and-again — 2020-09-30 — [T] snippet only.
- [69] YouTube — Noah takes a photo of himself every day for 6 years — https://www.youtube.com/watch?v=6B26asyGKDo — [V] oEmbed 2026-10-18: exists, channel Noah Kalina.
- [70] Wikipedia — Noah Kalina — https://en.wikipedia.org/wiki/Noah_Kalina — accessed 2026-10-18 — [T] fetched: six per second, piano score, Coolpix S10 since 2008.
- [71] TechCrunch — Everyday app — https://techcrunch.com/2011/03/21/everyday-iphone-app — 2011-03-21 — [S] fetched: alignment grid and overlay.
- [72] kottke.org — Half a Life in 2 Minutes — https://kottke.org/21/07/half-a-life-in-2-minutes — 2021-07 — [S] fetched: dlib, landmarks, 4K, Paul O'Mara.
- [73] Laughing Squid — Noah Kalina ages over 7,777 days — https://laughingsquid.com/noah-kalina-ages-over-7777-days/ — 2021 — [S] fetched: 60-face average, two months per second.
- [77] vladmandic/rife — https://github.com/vladmandic/rife ; dlib face_alignment — https://dlib.net/face_alignment.py.html — [T] snippets only.
- [78] Parting Stone — How to Make a Slideshow for a Funeral — https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/ — undated — [S] fetched: length, timing, licensing, export.
- [79] funeralOne — 22 Tips For Creating Tribute Videos — https://blog.funeralone.com/funeralone-products/life-tributes/tribute-video-tips/ — 2013-09-12 — [S] fetched: 25-30 photos, vary effects; vendor blog.
- [81] meyerweb (Eric Meyer) — Inadvertent Algorithmic Cruelty — https://meyerweb.com/eric/thoughts/2014/12/24/inadvertent-algorithmic-cruelty/ — 2014-12-24 — [P] fetched.
- [82] Engadget — Facebook's 'Year In Review' shows tragic side of software's shortcomings — https://www.engadget.com/2014-12-27-facebooks-year-in-review-shows-tragic-side-of-software.html — 2014-12-27 — [T] snippet only.
- [83] Apple Support — Photos memories — https://support.apple.com/guide/photos/pht96259d626/mac ; Google — redesigned Google Photos — https://blog.google/products/photos/redesigned-google-photos/ ; Trusted Reviews — https://www.trustedreviews.com/news/google-photos-update-makes-your-memories-better-than-you-remember-4267091 — [T] snippets only.
- [87] Retro Renovation — When was avocado introduced as an appliance colour — https://retrorenovation.com/2020/12/26/when-was-avocado-introduced-as-a-color-on-kitchen-appliances/ — 2020-12-26 — [S] fetched.
- [88] No Film School — How to get the Super 8 film look — https://nofilmschool.com/get-super-8-film-look — [S] fetched.
- [89] AIC (Wallace) — Topics in Photographic Preservation 1989, Vol 3, Art 17 — https://resources.culturalheritage.org/pmgtopics/1989-volume-three/03_17_Wallace.html — 1989 — [P] fetched: dye loss, restoration.
- [90] Wikipedia — Cooper Black — https://en.wikipedia.org/wiki/Cooper_Black — accessed 2026-10-18 — [T] fetched.
- [91] Wikipedia — Super 8 film — https://en.wikipedia.org/wiki/Super_8_film — accessed 2026-10-18 — [T] fetched.
- [93] Wikipedia — 110 film — https://en.wikipedia.org/wiki/110_film — accessed 2026-10-18 — [T] fetched.
- [96] American Ancestors — scanning handout — https://www.americanancestors.org/sites/default/files/2022-01/scanning%20handout.pdf ; Library of Congress Signal — https://blogs.loc.gov/thesignal/2013/01/scanning-diy-or-outsource/ — [T] snippets only.
- [100] University of Mary Washington DKC — Building a Scrollytelling Website — https://dkc.umw.edu/tools/building-a-scrollytelling-website/ — undated — [S] fetched: static fallback.
- [104] BlenderNation — Combining 2D and 3D to create a parallax effect in Blender — https://www.blendernation.com/2020/10/11/combining-2d-and-3d-to-create-a-parallax-effect-in-blender/ — 2020-10-11 — [T] snippet only: camera projection mapping.
- [105] Quartz — Why Joe Cocker's Wonder Years theme song is missing on Netflix — https://qz.com/316860/why-joe-cockers-wonder-years-theme-song-is-missing-on-netflix — [T] snippet only: relicensing cost.

## Changelog

- v0.1 · 2026-10-18 · First draft, written by the Haiku scribe from research/animated.md. Not yet reviewed by the advisor or by the maker.

### Open TODO(research) items at v0.1

- Watch sessions with a stopwatch for Up, Parisian Love, Dear Sophie, the Watchmen, Wonder Years and Addams titles, Tower's reveal, Flee's archive inserts and The Missing Picture's clay-to-archive cuts. Also confirm legal access to each clip.
- The Kid Stays in the Picture tooling: the DVD commentary or the two interviews.
- Unverified claims: Flee's 8mm frame; Tower's colour accents; Persepolis's colour framing; Gondry's visible erasures; Boyhood's time cues; Panh's reported rejection of animating the figures.
- Pricing and features: Immersity AI pricing (reviews conflict); Resolve free-edition versus Studio, including Fusion 3D tools.
- DepthFlow command syntax and Windows setup (documentation returned HTTP 403).
- Snow Fall in a current browser; Dear Sophie's official upload (only a mirror was verified).
- AI face animation (for example Deep Nostalgia); reel-grammar anti-patterns; the tedium threshold for morphs.
- Interviews with professional tribute film-makers (funeral.com returned HTTP 429; mulinblog failed DNS).
- Palettes for the 2010s and 2020s, and the type direction for each decade (thin sources).
- Free status and official download links for Blender, Inkscape, GIMP, Krita and ffmpeg (background knowledge, not checked).
- Wayback Machine survival of the interactives (access was blocked).
- The maker's installed apps: exact names and versions.
- ArtCraft equivalents of these steps: see the craft-visual and craft-motion tracks.
