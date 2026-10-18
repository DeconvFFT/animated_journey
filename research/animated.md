# Animated, documentary and web life-journey exemplars — research notes

Track: `animated` · Researcher: Sonnet · Written 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline 2027-02-27.

How to read this file.
- Evidence tiers appear in the Sources list: **[P]** creator, official or academic statement; **[S]** journalism, review or critical analysis; **[T]** Wikipedia, aggregator, forum, or a search-result snippet I could not open in full; **[V]** verified by my own HTTP or oEmbed probe on 2026-10-18.
- Anything I could not verify is marked **UNVERIFIED**. Where I give a recommendation, a rating, a palette or an arithmetic result, it is **my judgment** or **my arithmetic** unless a citation sits next to it.
- I could not watch video. Every "beat-level" note comes from written breakdowns, interviews and essays, not from frame-by-frame viewing. The Open questions section lists clips the team should watch with a stopwatch.
- The web-search budget ran out near the end of the session. Topics I could not finish are listed under gaps.
- Charter rule 4 (real memories stay real; reconstructions are visibly reconstructions) is the lens for the honesty questions.

---

## Summary

1. **The most useful honesty convention is "one hand-made material for everything with no photograph, disclosed up front, and a reveal of the real person."** The Missing Picture uses clay figures and miniature dioramas for the years no camera recorded [5][6][7][9]; Flee opens with a title card saying names and places were altered and shows the subject reviewed the edit [1]; Tower lets the real survivor replace the actress who played her [13]. Adopting all three together costs a learner little (see cheat sheet, section G).
2. **The Missing Picture's origin story is a template for a "Minecraft-style rebuilt home."** Panh did not want to visit his childhood home alone; when he did, it had changed, so he asked his assistant Sarith Mang to build a model, telling him "go to the river, use the clay" [6]. A vanished home rebuilt by hand, in blocks or in paper, is a reconstruction that is honest because the hand shows.
3. **Flee's most reusable technique is the interview, not the animation.** Rasmussen had Amin lie with his eyes closed and speak in the present tense, describing environments, materials, colours and feelings; the animators worked from those details [2]. His team also kept an "art bible" of good and not-good examples down to how to draw a hand or an eye [1][2]. Both are free and need no software.
4. **Audio first is the shared spine.** Ryan was built on about 20 hours of recorded interviews [11]; Rocks in My Pockets recorded the voice-over first and used the script as the blueprint [21]; Flee assembled a sound-and-storyboard master like a radio documentary before animating [3]; StoryCorps animates only recordings that "lend themselves to pictures" [20]. For us: record the person's voice and the family's voices before designing anything.
5. **How The Kid Stays in the Picture was made is only partly documented.** What is sourced: subjects are separated from backgrounds and panned at different speeds [24]; the directors say they cut things out and put them over backgrounds, mostly with a "fairly accessible program" and some 3D (search snippets of interviews I could not open) [22][23]. Software and animators are **undocumented** in anything I could open. The manual recipe is well documented by practitioners (Photoshop cut-outs, content-aware fill, After Effects 3D layers and a 28mm camera, slow push, tiny layer moves) [28][29].
6. **Automatic depth-map parallax is now free and scriptable.** DepthFlow 1.0.1 (PyPI upload 2026-08-25) is AGPL-3.0, needs Python 3.10 or newer, and renders locally with no watermark [30][31]. The 2019 Adobe-linked "3D Ken Burns" paper is the academic ancestor [27]. Neither source says how they cope with tiny, grainy 1970s prints; plan a spike test on the worst photos (Q2).
7. **Low-resolution reality.** 110-film prints (1972 onward) from a 13 x 17 mm negative are "often rather grainy and unsharp" [93]; cyan dye fades most in Ektachrome-type material and dark fading is proportional to dye, so a single colour filter will not fix it [89]. Genealogy-society guidance is 400 ppi minimum for prints, 2000-3000 dpi for slides [96]. My arithmetic says a 1080p push-in with parallax margin wants roughly 3,000 px on the long side, so scan small prints at 600 ppi.
8. **Time-passing devices that carry numbers.** Fixed-frame repetition: Kalina's original ran six photos per second [70]; the 21-year "7777 Days" recut ages him two months per second by averaging the last 60 aligned faces and runs about two minutes [72][73]. Interface as clock: Google's Parisian Love is 11 searches in about 52 seconds [54]; Dear Sophie is about 90 seconds [49]. Objects with a clock: Up's coin jar is broken open early by a flat tire, a broken leg and storm damage; Ellie ties Carl's ties over the years [57]; the sequence runs about 4.5 minutes and was cut from 30-40 minutes of material [56].
9. **Era is signalled mostly by medium, not palette.** Grain, handheld sway, waving at the camera and a black frame make "fake home video" read as Super 8 [62]; 1.33:1 for the 1988 Wonder Years open [61]; Super 8 ran 12-18 fps and about 3.3 minutes per cartridge [88][91]; VHS is 240 TVL with low-resolution colour [92]; appliance colours are dated (Coppertone 1964, Avocado 1966, Harvest Gold 1968) [87]. The decade palette and type table below is partly my synthesis; the best palette source is the maker's own scans.
10. **People entering and leaving: restraint wins.** Pixar cut the montage's dialogue and sound effects because "the less we had the more emotional it felt," and restored a painful beat after removing it hurt the film [56][58]. The Missing Picture's figures grow thinner as rations dwindle [6]. The voice keeps speaking in Ryan (real interview audio) [11] and in StoryCorps [20]. The risk case is the sentimental score-led montage; one French review called Dear Sophie "a bit too much" like an American soap opera [52].
11. **Scrollytelling longevity is better than the pessimists say, if you ship plain files.** Snow Fall (2012) still returns HTTP 200 on 2026-10-18 and its own CSS, jQuery 1.7.1 and more than 30 self-hosted MP4 and WebM files all resolve [39][V]. Its third-party Brightcove script now redirects (301) [39][V]. Flash-based interactives from CNN, ABC and the Washington Post broke when Flash support ended on 2020-12-31 [47]; the NYT revived some with the Ruffle emulator [47]. A 2017 Pudding piece still loads, with libraries from versioned cdnjs URLs (200) and a Typekit font script (200) [42][V].
12. **"Life in weeks" pieces are structurally simple and privacy-sensitive.** Urban's 2014 essay zooms years to months to weeks to a grid of about 4,680 boxes, then personalises [43]. Trapani's 2025 version colour-codes weeks by place and activity, labels approximate dates "Around this time," omits private details, and is on GitHub [44]. Another author built his version and did not publish it: "My life is mine, their lives are theirs" [45].
13. **Title sequences that compress time use in-scene type or fake artefacts.** Watchmen (1939-1985) integrates type "in 3D into each scene" [60]; The Addams Family titles cover 13 years with a gallery of illustrated portraits where the children visibly grow [63]; the Wonder Years open is a fake Super 8 montage whose footage was refreshed as the actors aged [62]; Blue Spill filmed a hand-cut title card on real Super 8 stock to sit with family cine film [64].
14. **Memorial-film advice is thin and mostly from funeral-industry sites.** Typical figures: 3-8 minutes; 3-4 seconds per photo (5-7 for group shots and title cards); one to three songs; 60-100 photos in one guide versus 25-30 in another; "cramming 200 photos into five minutes forces one-second flashes no one can absorb" [78][79]. I found no interview with a professional tribute film-maker (gap).
15. **Anti-exemplar anatomy.** Phone and photo-service memories are generic because of how they select (popularity, recency, faces; Facebook's 2014 Year in Review picked posts by likes and comments with no sense of grief [81][82]), how they style (themes that swap title, music and editing style [83]), how they move (the same motion on every photo [79][80]) and who bears the burden (opt-out buried [81]).

---

## Findings by question

### Q1. Animated documentaries and biography shorts that combine real testimony with reconstructed imagery honestly; what marks the reconstruction; what could we adopt wholesale?

Evidence by film, strongest honesty conventions first.

**Flee (2021).** Real testimony: about 20 interviews with Amin over three to four years [3]; per a search snippet of an AWN interview I could not open, he filmed them all but used only the audio, the animators mined the video for mannerisms, and they did not rotoscope (**UNVERIFIED** beyond the snippet). Marks of reconstruction: the opening title card says the story is true and "names and locations have been altered to protect its subjects" [1]. Archival footage supplements the animation "at every stage," sourced mainly from YouTube and European public broadcasters by requesting material for a specific place and date [2]. Style shift: warm childhood Kabul memories are vivid and true-to-life; trauma becomes more abstract and evocative, "looser and less defined" [2][3]. The opening uses grey-and-blue silhouettes [2]. A claim that archive clips are shown in a rounded-edge 8mm frame came from one search snippet and I could not confirm it on pages I opened: **UNVERIFIED**. Subject control: Amin saw a transcript, a document of intended content and the edit, which Rasmussen called "a symbiotic process" [1]. Method: the editing process is reversed from normal documentary; scenes are built from scratch [3]; ten animators and cleanup artists in Denmark and a colouring team in France, with inky, sketchy cleanup like a graphic novel [4]; about fifty people worked on the animation at once [2]. Software: not named in any source I opened.

**Tower (2016).** Real testimony: about 20 interviews boiled down to eight characters [14]. Reconstruction: actors performed the survivors' recollections on camera and were rotoscoped; Maitland says the animation is "an additive layer" [13]. He used first-hand accounts only, "so he could defend each frame" [15]. Archival 16mm footage lacked close and medium shots, so animation fills the gaps [14]. Honesty move: the actress playing 1966 Claire Wilson gives way to the real Claire, a reminder that this happened to a real person [13]. The last half-hour of the film is in a standard documentary approach [13]. Tools: TVPaint for rotoscoping, iPhone 6 reference footage; the production could not shoot on campus, so a backyard palm tree stood in for the tower [13]. Maitland's test is that viewers should not remember whether a key moment came from archive or animation [13] - which is the opposite of visible marking; his honesty comes from the reveal and the first-hand-only rule, not from a visual tell. Colour: search snippets describe mostly black-and-white with colour accents; I did not open a source: **UNVERIFIED**.

**The Missing Picture (2013).** Real testimony: narration is based on the autobiographical sections of Panh's book *The Elimination*, read by a narrator who is not Panh [7]. Reconstruction: more than 500 clay figures sculpted by Sarith Mang over about eight months, miniature scenes "down to tiny paper lilies" [5][6]; the camera pans across still "tableaux morts" [7]; the figures change with the story, thinner as rations dwindle [6]. About half the film is news and documentary footage and half is clay [9]. Panh used Khmer Rouge propaganda footage and noted "even in propaganda films you can find some traces of reality" [5]. A search summary says Panh rejected animating the figures because that would lose "the poetic sense and the sense of memory" [10] - single-source, **UNVERIFIED**. The clay is a material that cannot be mistaken for a photograph. This is the clearest "visibly reconstructed" model in the set.

**Waltz with Bashir (2008).** Real testimony: interviews with real friends and soldiers were first shot as a 90-minute video in a sound studio from a 90-page script; nine interviewees were filmed, two of them played by actors [16][18]. All redrawn: not rotoscoped, "drawn again from scratch"; about 2,300 illustrations, Flash cut-outs sliced into hundreds of pieces plus classic animation and 3D [16][18]. Honesty move: the animation dissolves into real news footage of the massacre's aftermath at the very end [16]. Folman's reason for animation: memory, dreams, hallucinations and the subconscious [17].

**Ryan (2004).** Real testimony: about 20 hours of audio and video interviews with Ryan Larkin; voices in the film come from them, including street people; an interview about alcohol was used nearly verbatim [11]. Reconstruction made explicit by distortion: characters are photoreal in skin texture but deliberately warped to show inner state (gouges for Chris's demons, a neon halo when he gets preachy, Ryan's face hollowed out); the cafeteria degrades as the talk heats up [11]. Larkin's own films and drawings are quoted: Derek and Felicity were modelled from Larkin's drawings so they look sketchy "as Ryan perceives them" [11]. The NFB page listed only rental or purchase options when I checked (digital $3.95 SD or $5.95 HD) [12].

**StoryCorps animated shorts.** Real testimony: the recorded conversation. Visual concept invented per story to fit tone (a quilt structure for a folk-art storyteller; memories mapped over a musical score for another); animators and producers talk to storytellers throughout to capture mannerisms, voices and feelings [20]. Software: not stated.

**Persepolis (2007).** Not testimony-based documentary but an autobiographical comic adaptation: hand-drawn, about 80,000 drawings by 20 animators; Satrapi acted out every scene as animator reference [19]. Mostly black and white; the choice is tied to the source comic and to universalising the story ("live action would have made it a story of people living in a distant land") [19]. How colour is used in the framing scenes: **UNVERIFIED**.

**Counter-example: Stories We Tell (2012).** Super 8 re-creations starring an actress as the mother were mixed with real home movies and not labelled for most of the film; Polley wanted the format to "mirror those questions" and says "there is actually something irresponsible with painting things as black and white" [66]. Critics split between audacity and discomfort [67]. Under Charter rule 4 this is the model **not** to copy for factual chapters, though its Super 8 fidelity is a good lesson in how convincing fakes are.

**Conventions that mark reconstruction (what we found, ranked by how easily we can copy them):**
1. A different *material* (clay, paper, hand-drawn line) that no one could mistake for a photograph [6][7][21].
2. A disclosure card at the start [1].
3. A style shift tied to certainty: vivid where memory is solid, looser where it is not [2][3].
4. A reveal that swaps the stand-in for the real person [13] or dissolves into real footage [16].
5. Distortion that announces subjectivity [11].
6. Archive as anchor beside the drawing [2][3].

**Adopt wholesale (my recommendation):** items 1 + 2 + 4 together. Concretely: every unphotographed scene is made in one visible hand-made style (cut paper drawn in Inkscape, or built blocks), introduced by a short opening card, and each reconstructed person or place is eventually answered by a real photograph, voice or object. Feasibility: high for stills and slow camera moves; low if you try to match Flee's full-animation volume. Rocks in My Pockets shows how one person can combine papier-mâché sets with hand-drawn characters (about 30,000 drawings, five assistants, a post-production artist doing colour in Photoshop and compositing in After Effects) [21], but that took years; use far less motion.

### Q2. How was The Kid Stays in the Picture photo-animation made; how do practitioners do 2.5D parallax from old prints today; what are the limits with low-resolution 1970s snapshots?

**What is documented about the film (2002).**
- The film separates the subjects of photos from their backgrounds and pans each at a different speed [24].
- Burstein told Filmmaker Magazine they used 3D images, cut things out and put them over backgrounds; told IndieWire that some shots were high-end with some 3D animation but most were made with "a fairly accessible program" (both are search snippets; the pages refused my fetch) [22][23].
- A montage of over 800 photographs in about a minute is described in the Filmmaker piece (snippet) [23].
- Review snippets describe a "paper-doll" or cardboard-cut-out quality, and Ebert says the graphics and juxtaposition make the stills feel like moving pictures [101] (snippets).
- Wikipedia has no production details [25]. A Grokipedia page claims After Effects with a 2.5D multiplane effect; it is an aggregator and I did not use it: **UNVERIFIED**.
- Software, studio and animators: **undocumented** in everything I could open.
- Tradition: a search snippet (source not opened) says Ken Burns credits Jerome Liebling and the 1957 NFB film *City of Gold* for the pan-and-zoom on stills; the layered "3D Ken Burns" version is laborious by hand: "hours of manual layer segmentation, clone-brushing," positioning layers in 3D and adjusting each layer's pan speed [26].

**Manual recipe (documented by practitioners).**
1. Pen-tool outline each element, feather 0.5-1 px, cut to its own layer [29].
2. Expand the selection 10-15 px and use Content-Aware Fill to rebuild what was behind it; or clone-stamp by hand [28][29].
3. Import the layered PSD into After Effects, turn on 3D for each layer, add a 28mm camera, spread layers in depth with foreground closer [29].
4. Keyframe a slow camera push or pull; add tiny layer moves; for people use the Puppet tool pins; foreground moves more than background [29].
5. Restraint: "any movement should be really subtle"; "pick 2-3 sections and make them perfect"; shallow depth of field and clean edges make the cut easier [28][29].
6. Free alternative in the same spirit: Fusion's ImagePlane3D, Camera3D, Merge3D and Renderer3D tools in DaVinci Resolve (a tutorial covers faking perspective on a still) [33]. Whether the free edition includes Fusion's 3D tools was not stated on the Blackmagic page I opened: **UNVERIFIED** [34]. Blender camera projection is another route (a 2020 BlenderNation article covers camera mapping) [104].

**Automatic recipe.**
- DepthFlow: a depth map drives a ray-marching shader so near parts move faster; local, "no watermarks, unlimited usage, mass production with scripts"; v1.0.1 uploaded 2026-08-25; AGPL-3.0; Python 3.10+; claims up to 8k50fps on an RTX 3060-class GPU (self-reported); depth estimators are external [30][31]. I could not open its documentation (HTTP 403), so the CLI syntax is **UNVERIFIED**.
- Niklaus, Mai, Yang and Liu (2019, Adobe-linked): predicts depth, builds a point cloud, inpaints disocclusions in colour and depth, renders a camera path; admits the hard parts are "inaccurate object boundaries" and geometric distortion, which their segmentation-aware network addresses [27].
- SAM + LaMa ("Inpaint Anything" and Lama Cleaner): click an object, segment it, fill the hole; free, Python, command-line [32] (snippets).
- Hosted: Immersity AI (formerly LeiaPix) reviews describe a watermarked 720p free tier and paid plans from about $4.99 per month, with the reviews disagreeing on tiers: pricing **UNVERIFIED** [35]. EZdepth (Blender add-on, Depth Anything Small) is sold, not free; price not verified [36].

**Limits with low-resolution 1970s snapshots.** None of the parallax sources gives resolution guidance (the PictureCorrect and Motion Array tutorials explicitly give none) [28][29]. What I can say from other sources and arithmetic:
- Source degradation is real: 110 prints are "often rather grainy and unsharp" [93]; dye loss is proportional to dye present, so shadows lose most and a uniform filter does not restore them [89]; cyan fades first in Ektachrome-type material [89].
- Scanning guidance (genealogy-society handout and Library of Congress comments): at least 400 ppi for prints up to 8 x 10; 600 ppi for small originals or enlargement; 2000-3000 dpi optical for film and slides [96] (snippets).
- My arithmetic: a 1080p frame is 1,920 px wide. Push in 1.5x and keep 15% parallax margin: about 3,300 px across the displayed width. A 3.5 x 5 in print at 600 ppi is 3,000 px on the long side, a 4 x 6 is 3,600. So small prints need 600 ppi; anything scanned at 300 ppi will soften on a push-in.
- Layer cut-outs need gaps filled. Shallow depth of field hides gaps [28][29]; old flash snapshots are the opposite (everything sharp), so gaps show. The "flash snapshots have deep focus" part is my background knowledge, not sourced.
- AI depth maps struggle with thin objects and edges (the paper's own words [27]); faces in tiny photos are where artefacts are least forgivable.
- Recommended spike (1 day, my judgment): pick the three worst and three best photos from the family set; run each through (a) a manual 3-layer cut in GIMP or Krita plus a Resolve or Blender camera, and (b) DepthFlow; compare at 1080p; keep the move under about 3-5% of frame width and the shot under 8-10 seconds. If the worst photo only works as a slow flat push, accept that and reserve parallax for the best 20.

### Q3. Recurring devices for time passing in short form (with examples and timing)

| Device | Exemplar and timing | Notes |
|---|---|---|
| Fixed frame, repeated | Kalina's original: photos at six per second [70]; 6 years of daily photos is about 2,190 images, so about 6 minutes (my arithmetic) [69][70]. "7777 Days": 60 fps, each frame the average of the last 60 aligned faces, so 2 months per second, 10 years per minute, about 2 minutes total [72][73]. Hofmeester's Portrait of Lotte: a 15-second clip recorded every week against a plain cloth backdrop, 0-20 years [74][75]. | Needs a consistent frame across years; cannot be reproduced for a life with sparse photos, but can be approximated with a "portrait ladder" (see Q7). |
| Interface as clock | Parisian Love: 11 searches in about 52 seconds, so about 4.7 s each (my arithmetic from [54]); from "study abroad paris france" to "how to assemble a crib" [54]. Dear Sophie: about 90 seconds, a father's Gmail and photos, based on a true story with actors [49][50]. | Time passes through what a person typed or wrote, not through photos. Good for a person whose old letters or emails exist. |
| Object with a clock | Up: the coin jar broken open early (flat tire, broken leg, storm), ties tied over the years, the house repainted; about 4.5 minutes [56][57]. | Chosen objects repeat and change; Docter: "every shot is a setup for elements we use later" [58]. |
| Hard cuts on sensory triggers | Up: a balloon pop and a camera flash cut forward to the wedding [56]. | Cuts hidden inside a motivated sound or flash. |
| Camera behaviour changes | Up: camera still until after the marriage, then gentle lateral tracking and panning "they're going through life" [56]. | A grammar shift instead of a caption. |
| Portrait gallery | The Addams Family titles: 13 years in a gallery of illustrated portraits, camera moving in and out, the children visibly growing [63]. | Works with a handful of portraits. |
| Refreshed fake footage | The Wonder Years open was re-shot as the actors aged [62]. | Not available to us; but "update the framing device each chapter" is. |
| Scale zoom | Urban: years, months, weeks, then the grid [43]. | Time as a physical quantity. |
| Duration as meaning | Burns: a 33-second zoom into a portrait of John Roebling; "all real meaning in this world accrues in duration" [37][38]. | The slowest device; use once per chapter at most. |
| Speed ramps by density | Kid Stays: 800+ photographs in about a minute (snippet) [23]. | Faster = more photos exist; see cheat sheet F. |

Not found with a source: seasons as a repeated establishing shot; aging hands. Up's tie-tying is the nearest hands-and-time device [57]. The "child in the same doorway" device was not documented by anything I opened; Hofmeester's plain-backdrop weekly clip is the nearest documented fixed-frame growth device [74]. Boyhood is the obvious long-span fiction (12 years, 39 shooting days, annual re-editing of everything shot so far) but I found no source on its time cues (pop songs, haircuts) [98 snippet]: **UNVERIFIED**.

### Q4. How do strong pieces signal era without captions? Palette and type direction per decade; when does it tip into pastiche?

**What the sources support (facts):**
- Medium cues. Super 8 was released 1965; a cartridge holds 50 ft, about 3.33 minutes at 18 fps; the original system was silent, magnetic sound arrived in 1973; frame 5.46 x 4.01 mm (about 1.36:1, my calculation); video replaced it in the 1980s [91]. Practitioner Super 8 emulation: 12-18 fps, 4:3, turn off stabilisation, f/8 or smaller aperture so everything is sharp, reduce sharpness, add grain, magenta, blue and yellow tints [88]. VHS: introduced 1976 in Japan, 240 TVL, chroma recorded "colour under" (about 40 x 480 pixels in NTSC), dropouts and generation loss; DVD overtook rental in the US in 2003 and blank-tape production ended 2019 [92]. 110 film launched 1972; small negative; grainy [93].
- Objects. GE appliance colours: Coppertone 1964, Avocado 1966 (1965 possible), Harvest Gold 1968, "Fresh Avocado" 1976; Avocado reissued 2020 [87]. Retro Renovation is a hobbyist site; dates are sourced from GE and readers.
- Film stock. Kodak 5247 II returned 1974 and shaped late-70s/early-80s cinema: punchy reds, deep greens, bronzed skin under tungsten, dense shadows, about 7-8 stops [85]. A forum thread: Kodachrome 64 strong reds, yellowish greens, magenta-leaning skies; 1970s Ektachrome cooler and bluer (anecdotal) [86]. Bleach bypass revived on *1984* [84]; teal-and-orange spread with the digital intermediate in the 2000s [84].
- Type. Cooper Black appeared on the Beach Boys' *Pet Sounds* cover in 1966 and phototypesetting spawned variants in the 1960s-70s [90]; ITC Souvenir was a 1970s staple and a cliché by the mid-1980s; hippie and funk faces faded a few years into the 1980s (typography.guru and a 70s typography portfolio snippet) [94]. The sources disagree on dates for Arial (1982 vs 1990) [94].
- Studio approach: Blue Spill gave different eras' family photos "distinct looks" (1930s through 1970s to now), set titles and lower thirds in "fonts of 70s cinema," added glow, diffusion and analogue camera movement, filmed a hand-cut title card on Super 8 stock developed at Cinelab, and used 1970s-style split screens [64].
- Music: Wonder Years uses Joe Cocker's "With a Little Help from My Friends" [61]; Watchmen uses Dylan [59][60]; relicensing killed the Cocker version on Netflix (Quartz, via a snippet) [105].

**Starting kit by decade (palette and type are my synthesis, anchored where sourced; test against the family's own prints).**

| Decade | Medium and format cues (sourced) | Palette direction (judgment) | Type direction (judgment, partly sourced) | Pastiche trap |
|---|---|---|---|---|
| 1970s | Square or 3.5 x 5 white-bordered colour prints [103 snippet]; Instamatic 126 (1963) and 110 (1972) [93][103]; Super 8 silent then sound [91]; 5247-era cinema [85] | Warm amber highlights, olive/avocado greens, brown shadows, rust and harvest-gold accents [85][87] | Rounded, chunky display (Cooper Black, Souvenir) for titles only [90][94]; "fonts of 70s cinema" with glow [64] | Stacking avocado, gold and Cooper Black on every frame |
| 1980s | VHS and camcorder arrive [92]; Super 8 declines [91]; 1.33:1 TV [61]; 110 and disc grain [93] | Saturated yet muddy; magentas and teals; video chroma smear on reds (forum, anecdotal) | Geometric sans (ITC Avant Garde) and early digital faces [94] | Neon-synth cliché; apply to TV-sourced material only |
| 1990s | Camcorder and VHS-C 4:3; DVD from 1997 [92]; date-stamped minilab prints (UNVERIFIED) | Flat consumer-video colour, flash-lit prints | System sans (Arial), goofy pop display [94] | Fake date stamps on photos that never had them |
| 2000s | First digital cameras; Kalina started 2000 and used a Coolpix S10 from 2008 [70]; teal-orange grade in cinema [84]; DIY desktop fonts [94] | Harsh flash, green-cool fluorescents (judgment); do not apply cinema teal-orange to snapshots | Default system fonts; web-era UI chrome | Over-pixelating - the low resolution is already there |
| 2010s | Smartphones: about 94% of all photos by 2024 (estimate) [95] | Filter look, high local contrast | Neutral grotesques (Suisse Int'l was the most popular font released in 2015 per Identifont, a narrow measure) [94] | Instagram square frames on non-square originals |
| 2020s | About 1.9 trillion photos in 2024, 2.1 trillion projected 2025 (estimates) [95]; vertical video | Clean, high-resolution, screen-native | Native UI type | Mixing vertical crops and 16:9 without a rule |

**Rules for when it tips into pastiche (my judgment, with sources):**
1. Do not "age" material that is already aged: the print's own dye shift is the era signal [89]. Restore to a neutral base first, then leave it.
2. Apply period cues to the *new* layer only: title cards, captions, reconstructions - as Blue Spill did with its Super 8 title card [64].
3. Keep nostalgia generic enough to be shared: the Wonder Years credits work because the action is "sufficiently generic to belong to any family," which makes viewers project their own memories - and its nostalgia is built in the present, not found in 1968 [62]. For a real person's life, generic is the failure mode; use their specific objects (kitchen colour, car) instead.
4. One grain level, one grade, applied to every decade makes eras indistinguishable: vary the medium, not just the filter.
5. Check licensing before choosing the era-defining song: Tarnation's budget rose from $218.32 to about $400,000 mainly for music and TV clip clearance [65].

**Better than a decade table:** sample the dominant colours and the dye cast from the maker's own scans, per era, and build the palette from those. Treat the generic table as a sanity check.

### Q5. Showing a person entering or leaving a life: devices; dignified versus maudlin

**Arrival devices found.**
- The first message: Dear Sophie begins with an email address being created and the first photos sent [49][51][52].
- The query that starts a relationship: Parisian Love introduces the partner through "impress a French girl" and the baby through "how to assemble a crib" [54] - arrival by task, not by portrait.
- The cut on a flash or balloon pop, in Up [56].
- The stand-in figure: Tower's actress, replaced by the real person [13]; the clay figure for a person who has no picture [6].
- The voice first: in Ryan and StoryCorps the person is introduced by what they say [11][20].

**Departure devices found.**
- Quiet physical details instead of dialogue: Up's last beats are a blue balloon brought to a hospital bed, a funeral with pink flowers and balloons, a barely perceptible pullback, and the pink light dimming [56]; later, the same lateral move and push-in return when Carl looks at the adventure book [56].
- Material change: the Missing Picture's clay figures thin as rations dwindle; one raises its hands to its cheeks in a wail [6].
- The voice that keeps speaking: Ryan is told through recorded voice [11]; StoryCorps animates a recording and consults the storyteller [20]; the Missing Picture's narrator is a stand-in voice, not Panh's [7].
- Staging with consent: Dick Johnson Is Dead stages the father's "deaths" with him playing himself, as a way for both to approach his decline (NPR, snippet) [68].
- A refusal to show the harm: Tower keeps the shooter mostly offscreen and unnamed (search summary of reviews; not opened) [UNVERIFIED].
- Not sourced in anything I opened: an empty chair, a removed photograph. These are common devices but I can only offer them as options, not evidence-backed.

**Dignified versus maudlin (my judgment, grounded in the above).**
- Dignified signs: the person's own voice or objects carry it; the camera or cut does less; sound effects and dialogue are stripped (Docter: "the less we had the more emotional it felt" [58]); a painful beat is kept only if the story needs it (Up's miscarriage was tried out, then restored [56][58]); the family agreed.
- Maudlin signs: a swelling score that does the work (a French review judged Dear Sophie "a bit too much" like American soap opera [52]); repeated slow dissolves to the same portrait; showing the dying.
- Facebook's 2014 Year in Review is the cautionary tale for algorithmic or default handling of loss: a photo of Eric Meyer's late six-year-old daughter was put under party graphics because it had many likes and comments [81][82].
- Charter-specific: do not animate a dead person's face or invent speech. AI face-reanimation reactions (e.g. MyHeritage Deep Nostalgia) were not researched because my search budget ran out: gap.

### Q6. What do the best scrollytelling and personal-timeline pieces do structurally; how long do they stay online; what breaks; what does this imply for a 20-year gift?

**Structure.**
- Snow Fall (NYT, launched 2012-12-20 per a search snippet): a reporter's long text first; multimedia used as "a much-needed pause at critical moments"; short airbag animation, a skier-path graphic "driven by the user's scrolling motion," a slow Cascades flyover, an avalanche simulation following real-time data; flashy transitions toned down because they cause fatigue; separate builds for modern browsers, iPad/iPhone/touch, and a simplified IE8 version; stack: jQuery, Underscore, jPlayer, HTML5 video, jQuery Reel, jQuery Address [40]. Reach: snippets say more than 3.5 million page views in the first six days and an average 12-minute read for 3 million readers; **UNVERIFIED** against a primary source [102].
- The Pudding: scrollytelling is content revealed or changed as the user scrolls; it "monitors scrolling rather than altering it"; "scrolljacking" is "generally bad practice"; libraries compared (Waypoints, ScrollStory, ScrollMagic, graph-scroll.js, in-view.js, roll-your-own); the post's author later made scrollama.js on IntersectionObserver [41]. A secondary summary says Pudding pieces often pin a visual and step the text beside it, and start with a question and move from big to small (snippet) [UNVERIFIED in primary].
- Life in weeks: Urban zooms years to months to weeks, each row a year (about 4,680 boxes for 90 years), overlays an average life with five numbered footnotes, applies it to famous people, to "You in Weeks," then to a physical metaphor (each week a 2 mm diamond) and a printable 24 x 36 in calendar; the argument is that each week should be enjoyed, build the future, or both [43]. Trapani (2025-02-14): rows by year, 90+ events compiled from photos, calendars and memory, some labelled "Around this time," colour-coded by place and activity "like layers of sedimentary rock," decades navbar, mobile layout, Hugo, code on GitHub, private details omitted or generalised [44].
- Felton's Annual Reports: began with a 2004 "Best of 04," first full report 2005 from memory, calendar, photos and last.fm data; the hardest step is "keeping meticulous records"; the 2010 report reconstructed his late father's life from estate papers (search snippets) [48].

**Longevity probes on 2026-10-18 (my own HTTP checks; HTTP 200 does not prove it renders in a current browser; I did not render any page).**
- Snow Fall page: 200, 177 KB, title intact, jQuery 1.7.1 from the publisher's own host, the stylesheet and more than 30 self-hosted MP4 and WebM videos all 200 [39][V]. Dead or changed: the Brightcove script returned 301; a slideshow script returned 403 (possibly user-agent gating); the analytics beacon did not resolve. The archive.nytimes.com copy returned 404 [39][V].
- Pudding "film dialogue" (2017): 200; its dependencies jQuery 2.1.3, d3 3.5.12, ScrollMagic 2.0.5 on cdnjs all 200; Typekit script 200 [42][V]. Waveforms (2018): 200 [V].
- Urban's 2014 post: 200; Noah Kalina's site: 200; NFB's Ryan page: 200 [V][12][43].
- Wayback Machine access was blocked in this environment, so I could not test archival copies.

**What rots.** Flash. CNN, ABC News and the Washington Post 9/11 interactives broke after Adobe's 2020-12-31 end of Flash support; many now show a still image or a grey "Flash is no longer supported" box; the NYT revived some with Ruffle and keeps originals on archive.nytimes.com [47]. Earlier, in 2016, Kosara documented broken Flash pieces, broken CSS that made tooltips unusable, and pages that had disappeared; suggestions included freezing visualisations with their CSS, JavaScript and data archived alongside [46]. Shared resources that keep evolving are the deeper cause [46].

**Implications for a gift meant to last twenty years (my judgment, grounded in the above).**
1. Ship a self-contained folder: HTML, CSS, JavaScript, images, video, fonts, all local. No CDN, no third-party video host, no web-font service, no analytics. Snow Fall's own files lasted 14 years; the third-party embed is what changed first.
2. Prefer boring, standard formats: H.264 MP4 (and WebM if wanted), JPEG, PNG, SVG, plain JS. Avoid plugins and anything that needs a service.
3. Always ship a plain film file as well. A video file plays without a browser framework; every interactive piece in Q6 that died, died through a runtime.
4. Keep an archive of masters and sources separate from the delivery build, with a README that says how to rebuild it.
5. Make a static fallback (a university scrollytelling guide recommends offering a static version or transcript) [100].
6. Treat privacy as a longevity feature: a public URL outlives the family's consent. Werd built his life-in-weeks and chose not to publish it [45].

### Q7. Growing-up morph and daily-selfie videos: what makes the good ones watchable; how long before they become tedious?

**What works (documented).**
- Alignment is the craft. Kalina's classic needed the face in a fixed position; his app has a grid for nose, mouth and eyes and an overlay of the first photo to line up each shot [71]. The 2021 "7777 Days" detects five landmarks per photo (both eyes, nose, mouth corners) with dlib and custom Python, aligns, evens brightness, upscales to 4K and averages the last 60 faces per frame [72][73].
- Rhythm is fixed: six photos per second in the original [70]; constant two months per second in the recut [73].
- Sound: the original has an original piano score by Carly Comando [70]; "7777 Days" has sound by Paul O'Mara [72].
- Restraint: the same plain backdrop for Hofmeester's weekly clips; he stalled reluctant children with questions to finish the shot; several versions were released at ages 12, 14, 16, 18, 20 and 23 [74].
- Precedent: Ed Emshwiller's *Family Focus* (1975) is a collage of home movies and photographs in which children "grow" over twenty years (snippet) [97].

**How long before tedious.** No source gave a tedium threshold: **UNVERIFIED**. What the numbers show: the 6-year original runs about 6 minutes at six photos per second (my arithmetic) [69][70]; when the same project spanned 21 years, the makers moved to averaged blending and about two minutes [72][73]; Lotte's 0-20 cut is billed as about five minutes (snippet), which implies under about 0.3 second per weekly clip if it holds all 1,040 clips (my arithmetic, **UNVERIFIED**) [75]. My judgment: any single morph or portrait-ladder passage inside our film should be 20-90 seconds, one idea, with a change of rhythm halfway.

**What we can do with sparse photos (my synthesis).**
- A "portrait ladder": 8-15 portraits across 50 years, aligned on the eyes, same crop, 1-2 seconds each, cross-dissolved. dlib's landmark alignment is free and scriptable [72][77].
- If morphing between portraits: RIFE and FILM frame interpolation are free command-line options; the sources say interpolation can produce ghosting and artefacts, especially between very different faces (snippets) [77]. Mark it on screen as a morph, not a photograph (Charter rule 4).
- Alternatively skip the morph: a hard cut on the aligned eyes is more honest and cheaper.

### Q8. Title sequences that compress a life or an era in under two minutes; what can we imitate with Inkscape, Blender or Resolve?

| Sequence | What it compresses | Typography, motion, colour (as documented) | Imitation path |
|---|---|---|---|
| Google Search Stories: Parisian Love (2009; Super Bowl 2010) | A relationship, 11 queries in about 52 s [54] | Almost no people; the Google logo and on-screen text carry the story; music cited as a key factor [54][55] | Inkscape UI mockup of a search box; animate typing and results in Resolve |
| Chrome "Dear Sophie" (2011) | A childhood in email, about 90 s [49] | A browser point of view; real-event basis with actors [49][50] | Same method with the person's real letters, emails or voicemails |
| The Wonder Years main title (1988) | A family summer, fake Super 8 [61][62] | Grain, handheld, waving, black frame, 1.33:1; footage refreshed as actors aged; Joe Cocker [61][62] | Resolve grain and 4:3 crop; film a few seconds on a phone, handheld, no stabilisation [88] |
| The Addams Family titles (1991) | 13 years of a marriage [63] | Illustrated portraits in a gallery, camera passing in and out, lightning shadows, playful type [63] | Draw 4-6 portraits in Inkscape; Blender or Resolve camera moves through frames |
| Watchmen titles (2009) | 1939-1985 alternate history [59][60] | Type integrated "in 3D into each scene"; dynamic slow motion; Dylan; 2.35:1; the studio was yU+co [59][60] | Blender text objects with camera projection on stills; Resolve Fusion 3D text |
| Blue Spill, *Stiller & Meara: Nothing Is Lost* (documentary) | Decades of showbusiness family photos [64] | Era-specific looks per decade, 70s cinema fonts, glow and diffusion, split screens, hand-cut title filmed on Super 8 [64] | Physically print a title card on paper, film it on a phone, grade to 4:3 |
| Up, "Married Life" (not a title; 4.5 min) | A marriage [56] | Wordless, music-led, dialogue and effects cut [56][58] | Study, don't copy; our version has real voices |

Runtimes: Parisian Love is 52 s per one analysis and 60 s per comScore (conflict) [54][55]; Watchmen's titles exceed two minutes (Motionographer says the titles were built into an already-edited six-minute sequence; shipped runtime **UNVERIFIED**) [60]; Wonder Years runtime not stated on the page I opened [61].

### Q9. What do professional memorial and tribute film-makers say about length, pacing, music and amateur mistakes?

I found **no interviews with professional tribute film-makers**; what follows is from funeral-industry guides and a photojournalism pacing note.
- Length: 3-8 minutes typical; about 4-5 minutes for a tribute within a service; loops at receptions can be longer [78].
- Count and timing: one guide says 3-4 s per photo, 5-7 s for group shots and title cards, 60-100 photos; "cramming 200 photos into five minutes forces one-second flashes that no one can absorb" [78]. Another (written for funeral professionals) says 25-30 photos per video work best and a longer video is not a better one [79]. Different guides conflict; the shape is: fewer photos, held long enough to read faces and text.
- Music: one to three songs, slow to mid-tempo, songs the person loved; check public-performance licensing with the venue; end transitions on musical phrases [78][79].
- Order: chronological; captions with name, year or place only; large plain high-contrast type for a projector [78].
- Amateur mistakes: overloading photos; the same motion effect on every photo; "don't look like you threw it together in PowerPoint" [79]; skipping a test on the venue's equipment; low-resolution screenshots that blur on a projector - collect the highest-resolution originals [78]; first-time editors apply movement to every photo, fixed by alternating still and moving segments and keeping motion slow, small, smooth (photojournalism pacing note, snippet) [80].
- Ken Burns on motion: "mindless, anxious movement for the sake of movement" is the enemy; "if it doesn't have meaning, it doesn't have a place" [37].
- Export: MP4 H.264, 1080p, 16:9; two copies; send the file to the venue a day ahead [78].

### Q10. Anti-exemplars: what makes automatic "memories" generic

What the products do (from their own documentation and coverage):
- Apple Photos creates up to three memories a day; Memory Movies come with theme music, titles and cinematic transitions; you can change mood and duration, and on the iPad swiping through moods changes title, music and editing style [83] (snippet).
- Google Photos: users can hide people or time periods and choose memory types; reviewers called the added music "clichéd whistling instrumental" [83] (snippets).
- Facebook Year in Review (2014): chose posts by likes and comments, did not distinguish sad from happy; Meyer's critique: "The design is for the ideal user, the happy, upbeat, good-life user"; opt-out required insider knowledge [81][82].

Precisely what makes them generic (synthesis, with sources):
1. **Selection by popularity or recency**, not by meaning [81].
2. **One pipeline, many skins**: theme = title style + music + transitions [83].
3. **Uniform motion**: the same effect on every photo is dull [79][80].
4. **Stock music** chosen by mood tag [83].
5. **No testimony**: no voice, no place names, no objects; captions are dates.
6. **No consent step**: Meyer's recommended fix is opt-in preview with a simple yes or no, and honouring the answer [81].
7. **No point of view**: the piece cannot say "this mattered because".

Reel grammar (whip pans, beat-synced zooms, trending transitions) is listed here only as an anti-pattern per the Charter. I did not research it further.

### Q11. Visual-grammar cheat sheet

Each entry: device, exemplar reference, feasibility for a learner with free tools by 2027-02-27 (my rating, High/Medium/Low), and a flag if it needs high-resolution footage.

**A. Time passing**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| Portrait ladder: same crop, eyes aligned, one portrait per few years | Kalina [70][72], Lotte [74] | High | Medium: faces need 600 ppi scans |
| Object with a clock (a jar, a tie, a car, a kitchen) that changes across chapters | Up [56][57] | High | No |
| Interface as timeline (messages, search queries, handwritten notes) | Search Stories [54], Dear Sophie [49] | High, if the person left text | No |
| Camera grammar change at a life stage | Up [56] | Medium | No |
| Zoom through scales (years, months, weeks) | Urban [43] | High | No |
| One long hold per chapter | Burns [37][38] | High | Yes for a 20-30 s move |

**B. Era change**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| Change the medium: Super 8 look, 4:3, VHS smear | Wonder Years [62], VHS facts [92] | High (grain, crop, tint) | No (degradation is the point) |
| Title card made physically and filmed | Blue Spill [64] | High | No |
| Dated objects in frame (appliance colours, cars) | GE colours [87] | High | No |
| Era-specific type, titles only | Cooper Black example [90] | High | No |
| Period song as a cue | Wonder Years [61] | Medium (licensing) | No |

**C. Places**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| Build a model of a place that has changed | Missing Picture [6] | High (paper, clay, blocks) | No |
| Rebuild a street from thousands of photos, then distort it painterly | Ryan [11] | Low | Yes |
| Stand-in location, honestly told | Tower's backyard palm tree [13] | Medium | No |
| Map or flyover for scale | Snow Fall [40] | Low-Medium | No |
| Light and composition references from painters | Flee: Hopper, Metzler, Gronsky [2] | High | No |

**D. People entering a life**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| First message, first query, first voice | Dear Sophie [52], Parisian Love [54], Ryan [11] | High | No |
| Flash or sound cut to the new chapter | Up [56] | High | No |
| Stand-in replaced by the real person | Tower [13] | Medium | No |

**E. People leaving a life**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| Strip dialogue and effects; let one object and one sound carry | Up [56][58] | High | No |
| Voice persists after the image changes | Ryan [11], StoryCorps [20] | High | No |
| Material change in the figure | Missing Picture [6] | Medium | No |
| Return of the same camera move later | Up [56] | High | No |
| Ask first; staged with consent or left out | Dick Johnson [68]; Charter rule 5 | n/a | n/a |

**F. From few photos to thousands**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| Early decades: one photo held 8-30 s with slow moves; later decades: contact-sheet grids and count-ups | Burns [37][38]; Kid Stays 800 photos/min [23]; photo stats [95] | High | Yes for early holds |
| The weeks grid fills in as the years go on | Urban [43], Trapani [44] | High | No |
| Sparse years shown as sparse: black frames or a single object | Wonder Years' black frame as a home-movie marker [62] | High | No |
| Pace by medium: slow prints, quick burst of digital | Kalina six per second [70] | High | No |

**G. Marking a reconstruction**
| Device | Exemplar | Feasibility | Hi-res needed? |
|---|---|---|---|
| A single hand-made material for all reconstructions | Missing Picture [6][7], Rocks in My Pockets [21] | High (static) / Low (animated) | No |
| Opening disclosure card | Flee [1] | High | No |
| Vivid for solid memory, looser for uncertain | Flee [2][3] | Medium | No |
| Reveal: stand-in to real, drawing to archive | Tower [13], Waltz [16] | High | Yes for the real item |
| Distortion for inner state | Ryan [11] | Low | No |

---

## Exemplars / recipes

Format for each: what it is; why it works at beat level; how it was made (where documented); what we can reuse; link. Links are sources I saw, not guesses.

**E1. The Missing Picture (Rithy Panh, 2013, 92 min).** Clay-figure reconstruction of Phnom Penh's evacuation and the Khmer Rouge years, narrated from Panh's book, with half the film propaganda and news footage [7][9]. Why it works: the figures cannot be mistaken for photographs, and they change with the story (thinner as rations dwindle) [6]; Panh called them a way to resist the regime's erasure of individuals; "Each figurine has a unique expression" [8]. How made: Sarith Mang sculpted more than 500 figurines over eight months; river clay; Panh worked 1.5 years with a Khmer Rouge cinematographer before changing direction [5][6]; the idea started with a clay model of his changed childhood home [6]. Reuse: a handmade model of a vanished home; a static clay or paper figure for each person with no photograph. Links: https://www.mprnews.org/story/2014/03/30/cambodias-missing-pictures-molded-from-directors-own-life · https://www.aljazeera.com/amp/features/2014/3/1/qa-meeting-cambodias-oscar-nominee

**E2. Flee (Jonas Poher Rasmussen, 2021, 90 min).** Anonymous refugee's life, animated, with archive. Why: the memory-trauma style dial; the disclosure card; a friendship story rather than a "refugee story" ("being a refugee is not an identity; it's a circumstance") [1]. How: interviews, closed-eyes present-tense sessions, art bible, light references from Hopper [1][2]; Danish animation team plus French colourists [4]. Reuse: the interview method, the art bible, the disclosure card. Links: https://hyperallergic.com/697967/jonas-poher-rasmussen-interview-flee/ · https://seventh-row.com/?p=45371

**E3. Tower (Keith Maitland, 2016).** Rotoscoped re-enactment of the 1966 UT Austin shooting. Why: close shots archive lacked; a reveal of the real survivor [13][14]. How: actors, TVPaint, iPhone reference, stand-in locations [13]. Reuse: reveal and first-hand-only rule; not the rotoscope workload. Link: https://stanforddaily.com/2016/11/11/tower-director-keith-meithland-talks-his-unique-documentary/

**E4. Waltz with Bashir (Ari Folman, 2008).** Memory search through interviews, drawn from scratch, dissolving to real footage at the end [16]. How: studio video first, storyboards, 2,300 illustrations, Flash cut-outs [16][18]. Reuse: cut-out puppets (slice drawings into parts) and the final dissolve to the real. Links: https://en.wikipedia.org/wiki/Waltz_with_Bashir · https://www.europeanfilmawards.eu/efa-movie/waltz-with-bashir/

**E5. Ryan (Chris Landreth, 2004).** NFB film about animator Ryan Larkin. Why: real voices, distorted bodies for inner state; the cafeteria degrading as the talk heats [11]. How: Maya, Photoshop, Combustion, Final Cut, SyFlex; 20 hours of interviews [11]. Reuse: real audio as spine; sketchy re-rendering of people from their own drawings. Link: https://www.nfb.ca/film/ryan/ (rental price as of fetch) and https://cgw.com/Publications/CGW/2004/Volume-27-Issue-7-July-2004-/Psychorealism.aspx

**E6. Persepolis (Satrapi and Paronnaud, 2007).** Hand-drawn black-and-white memoir [19]. Reuse: a limited palette and flat graphic style are easier than rendering a world; Satrapi's acting out of scenes as reference [19]. Link: https://web.library.yale.edu/node/173274

**E7. Rocks in My Pockets (Signe Baumane, 2014).** Papier-mâché sets, hand-drawn characters, voice-over recorded first [21]. Reuse: tactile sets plus drawn people - the most learner-friendly "visibly handmade" pipeline, at much lower volume. Link: https://www.bu.edu/bostonia/2016/from-sketch-to-screen/

**E8. StoryCorps animated shorts.** Real recorded conversations, a different visual idea per story [20]. Reuse: choose a visual structure from the storyteller's own world (a quilt, a score). Link: https://storycorps.org/inside-storycorps-turning-words-into-visuals/

**E9. Is the Man Who Is Tall Happy? (Michel Gondry, 2013).** Hand-drawn animation over conversations with Noam Chomsky; search snippets say pencil drawings build while he speaks. I could not open a source on visible erasures: **UNVERIFIED**. Reuse: drawing on screen in time with the voice.

**E10. Stories We Tell (Sarah Polley, 2012).** Unlabelled Super 8 re-creations beside real home movies [66][67]. Reuse as a counter-example and as a fidelity lesson.

**E11. Dick Johnson Is Dead (Kirsten Johnson, 2020).** Staged deaths with the father's consent as a way to approach loss [68] (snippet). Reuse: consent and rehearsal as part of the form.

**E12. Tarnation (Jonathan Caouette, 2003).** Home video, photographs, audio diaries and answering-machine messages edited in iMovie; started as a $218.32 project; editing based on cutting around the beat; pairing a single cello note with one word or image; first cut 3 hours [65]. Reuse: proof that a personal archive plus consumer software can make a feature; also a warning on clearance costs [65].

**E13. The Kid Stays in the Picture (Morgen and Burstein, 2002).** See Q2 [22][23][24][25]. Link: https://en.wikipedia.org/wiki/The_Kid_Stays_in_the_Picture

**E14. Up, "Married Life" (Pixar, 2009).** See Q3 and Q5 [56][57][58]. Link: https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of

**E15. Google Search Stories: Parisian Love (2009).** Link: https://www.youtube.com/watch?v=nnsSUqgkDwU [V]. Analysis: https://corridors.sites.umassd.edu/?p=213 [54]. How made: undocumented in what I opened.

**E16. Chrome "Dear Sophie" (2011).** Link (a mirror posted by CannesPredictions, verified by oEmbed; I could not confirm an official Google upload): https://www.youtube.com/watch?v=pzOBOuyr-EU [50]. Credits: Google Creative Lab and Bartle Bogle Hegarty [49].

**E17-E20. Title sequences.** Watchmen https://www.artofthetitle.com/title/watchmen [59]; The Wonder Years https://www.artofthetitle.com/title/the-wonder-years/ [61]; The Addams Family https://www.yuco.com/works/the-addams-family [63]; Stiller & Meara https://bluespill.co.uk/project/stiller-meara-i-nothing-is-lost/ [64].

**E21. Noah Kalina, "Everyday" and "7777 Days".** Link: https://www.youtube.com/watch?v=6B26asyGKDo [69][V]. Method in Q7.

**E22. Portrait of Lotte (Frans Hofmeester).** See Q3 and Q7 [74][75].

**E23. Snow Fall (NYT, 2012).** Link: https://www.nytimes.com/projects/2012/snow-fall/index.html [V][39]. Method write-up: https://source.opennews.org/articles/how-we-made-snow-fall/ [40].

**E24. The Pudding.** Link: https://pudding.cool/process/how-to-implement-scrollytelling [41]; a 2017 piece https://pudding.cool/2017/03/film-dialogue/ [V][42].

**E25. Life-in-weeks sites.** Urban https://waitbutwhy.com/2014/05/life-weeks.html [43]; Trapani https://notetoself.studio/post/my-life-in-weeks/ [44]; Werd https://werd.io/life-in-weeks/ [45].

**E26. Nicholas Felton's Annual Reports.** Personal data as design; years of a life documented through meticulous records [48] (snippets).

**E27. Phone and service "memories".** Anti-exemplar; see Q10 [81][82][83].

---

## Tools

As of 2026-10-18. "Verified" means I checked that day; "background" means common knowledge I did not re-verify in this session.

| Tool | Cost / free tier | Platform | Learning curve | Scriptable / CLI | Notes |
|---|---|---|---|---|---|
| DepthFlow 1.0.1 | Free, open source, AGPL-3.0; verified [30][31] | Python 3.10+, GPU recommended (self-reported 8k50fps on RTX 3060-class) [30][31] | Low-medium | Yes: described as scriptable, mass production with scripts; exact CLI syntax UNVERIFIED (docs gave 403) | Depth from external estimators; local, no watermark; AGPL matters only if you host it as a service |
| Inpaint Anything / Lama Cleaner | Free, open source (snippets) [32] | Python | Medium | Yes (command-line scripts, pip install) | Click-to-segment, then fill holes; check licence per component |
| Niklaus et al. 3D Ken Burns | Research code and paper [27] | Python | High | Possible | Reference for automatic parallax; DepthFlow is easier to use |
| DaVinci Resolve (free) and Studio 21 | Free version; Studio $295 as listed on the Blackmagic page [34] | Win/Mac/Linux | Medium-high | Python scripting (background; not verified) | Fusion 3D tools (ImagePlane3D, Camera3D) used in a tutorial [33]; whether free edition includes Fusion's 3D tools: UNVERIFIED. Magic Mask is listed under Studio [34] |
| Blender | Free (background) | Win/Mac/Linux | High | Yes, Python and CLI rendering (background) | Camera-projection 2.5D; 2020 BlenderNation article covers camera mapping (snippet) [104] |
| EZdepth (Blender add-on) | Paid; price UNVERIFIED [36] | Blender | Low | Via Blender | Depth Anything Small to displacement; commercial |
| Immersity AI (formerly LeiaPix) | Freemium; watermark and 720p on free tier; paid from about $4.99/month; reviews conflict - UNVERIFIED [35] | Web | Low | No | Not recommended as a core dependency; hosted, credit-based |
| Inkscape | Free (background) | Win/Mac/Linux | Medium | CLI export (background) | Vector cut-out figures, UI mockups, title cards |
| GIMP / Krita | Free (background) | Win/Mac/Linux | Medium | Script-Fu / Python (background) | Layer cut-outs and cleanup, instead of Photoshop |
| Photoshop + After Effects | Paid subscription (background; price not verified) | Win/Mac | Medium | Partial | What tutorials use [28][29]; not required |
| RIFE (rife-ncnn-vulkan), FILM | Free (snippets) [77] | Win/Mac/Linux (ncnn-vulkan portable build) | Low-medium | Yes (CLI, folder batch) | In-betweening; artefacts on very different faces |
| dlib face alignment | Free (background; example page seen in a snippet) [77] | Python | Medium | Yes | Five-landmark alignment as in "7777 Days" [72][73] |
| Ruffle | Free, open source Flash emulator [47] | Browser/desktop | Low | n/a | For old Flash material; NYT used it [47] |
| Scrollama / ScrollMagic / Waypoints | Free JS libraries [41] | Browser | Medium | n/a | Pudding warns against scrolljacking [41]; ScrollMagic and cdnjs links still resolve [V][42] |
| TVPaint, Toon Boom | Paid (background) | Win/Mac | High | Limited | Used on Tower and in studio work [13] |

---

## Techniques

1. **Closed-eyes, present-tense sensory interview.** Ask the person to lie back, close their eyes and describe a place in the present tense: materials, colours, light, sounds, feelings. Record it. The animators of Flee worked from these descriptions [2]. Learner-doable with a phone.
2. **Art bible.** A short document of "this is good / this is not good" images, down to how to draw a hand or an eye [1][2]. In our case: a one-page style sheet before any asset is made.
3. **Audio first.** Record the voice, cut a rough audio edit, storyboard to it [3][21].
4. **Single-material reconstruction.** One look for everything invented: clay, paper cut-out, or Minecraft-style blocks. Disclosed on screen once [1][6].
5. **Reveal.** Replace the stand-in with the real person, or the drawing with the archive [13][16].
6. **2.5D layer parallax (manual).** Steps in Q2 [28][29].
7. **Depth-map parallax (automatic).** DepthFlow, 3D Ken Burns [27][30].
8. **Ken Burns as master shot.** Treat each photo as a master shot with long shots, close-ups, tilts and reveals inside it; pick start and end frames deliberately; long holds [37][38] (snippets).
9. **Face-landmark alignment and sliding-window averaging.** dlib, five landmarks, average of the last N frames [72][73].
10. **Interface as timeline.** Mock a search box, inbox or handwritten letter, and let queries or lines carry the years [49][54].
11. **In-scene type.** Type that sits in the world (3D text with shadows, lit like the scene) instead of an overlay [60].
12. **Fake-home-video markers.** Grain, handheld sway, waving at camera, black frame, 4:3 [62][88].
13. **Cut-out puppets.** Slice a drawing into parts and move them against each other [16].
14. **Scale zoom and grid.** Years to months to weeks [43].
15. **Static fallback and self-contained build.** See Q6 [39][100].
16. **Per-channel dye correction.** Dye loss is proportional to dye, so correct layers or channels separately, not with one filter; keep corrections simple and trackable [89].

---

## Pitfalls and ethics

- **Honesty versus fidelity.** Stories We Tell proves how convincing fake Super 8 can be and also how it divides audiences [66][67]. Under Charter rule 4 every reconstruction is visibly one.
- **Consent and control.** Flee: the subject saw the edit [1]. Dick Johnson: the father played himself [68]. Trapani omitted private details [44]; Werd did not publish [45].
- **Algorithmic cruelty.** Never auto-select. Meyer's rules: do not pre-fill, ask for consent, honour the answer, design for the worst case [81].
- **Music licensing.** Tarnation's budget went from $218.32 to about $400,000 mainly for clearances [65]; the Wonder Years' Joe Cocker theme was replaced for streaming because relicensing was ruinously expensive (snippet) [105]; funeral guides warn that venues need public-performance licences [78]. A private gift is safer than a public premiere.
- **Listicle and dead-link risk.** I verified liveness only for Snow Fall, the Pudding pieces, Urban's post, Kalina's site and the NFB page (all HTTP 200). I did not verify Dear Sophie's official upload, DepthFlow's docs (403), or any streaming availability of the films.
- **High-resolution dependency.** Flagged in the cheat sheet. Devices that assume clean source: Ryan's street rebuilt from thousands of photographs [11]; 3D Ken Burns on a single high-quality image [27]; long holds.
- **Faces.** Faded, small prints plus AI depth maps or interpolation produce artefacts on faces first [27][77]. AI face "restoration" invents detail; not researched here (gap).
- **Reel grammar.** Whip pans and beat-synced zooms are an anti-pattern here; they were not researched beyond that.
- **Pastiche.** Do not double-age material; keep the era signal in the medium (see Q4).
- **Source quality.** Several sources are forum posts, hobby blogs, marketing-adjacent funeral platforms, Wikipedia or search snippets; flagged in the tier tags.

---

## Open questions / gaps

1. **The Kid Stays in the Picture tooling** is undocumented in the pages I could open; the IndieWire page returned HTTP 402 and Filmmaker Magazine 403. The team can read both directly (URLs in Sources 22 and 23) or check the DVD commentary.
2. **I could not watch any film or clip.** Needs a team watch session with a timing sheet for: Up's 4.5-minute montage; Parisian Love; Dear Sophie; Watchmen titles; Wonder Years open; Addams titles; Tower's switch from actress to real survivor; Flee's archive inserts (to confirm or refute the 8mm-frame claim); The Missing Picture's clay-to-archive cuts.
3. **Decade type direction** rests on thin sources (Cooper Black, Souvenir, snippets). A typographer or a book such as *20th-Century Type* (named in a search snippet) would improve it. 2010s-2020s palettes have no source.
4. **Tedium threshold for morph videos** is undocumented.
5. **Professional tribute film-makers** (length, pacing, music) - no interviews found; the funeral.com page returned HTTP 429 and mulinblog failed to resolve (DNS) in my session.
6. **Deep Nostalgia and AI face-animation reactions** were not researched (search budget exhausted).
7. **Flee's 8mm rounded frame**, **Tower's colour accents**, **Persepolis's colour framing**, **Gondry's visible erasures**, **Boyhood's time cues**: all UNVERIFIED.
8. **Resolve free versus Studio feature split** for Fusion 3D and Depth Map: the Blackmagic page I opened did not answer it.
9. **DepthFlow CLI syntax** and its depth-model options: docs gave HTTP 403.
10. **Snow Fall rendering.** HTTP 200 and resolving assets do not prove it plays in a 2026 browser; test with a real browser.
11. **Wayback Machine** was blocked, so archive-level survival of interactives was not tested.
12. **Immersity pricing** conflicts across third-party reviews.
13. **StoryCorps tools** and **Dear Sophie / Parisian Love production methods** are undocumented in my sources.
14. **Seasons-as-repeated-establishing-shot** and **aging hands** devices: no sourced exemplar beyond Up's ties.

---

## Sources

Tier key: [P] creator/official/academic; [S] journalism, review, essay; [T] Wikipedia, forum, aggregator or search-result snippet only; [V] verified by my own probe on 2026-10-18. "fetched" means I opened the page with WebFetch; "snippet" means seen only in search results.

1. Hyperallergic — How a Documentary Used Animation to Protect the Identity of Its Main Character (Flee interview) — https://hyperallergic.com/697967/jonas-poher-rasmussen-interview-flee/ — undated — [S] fetched: art bible, title card, Amin reviewed edit.
2. Seventh Row — Flee interview — https://seventh-row.com/?p=45371 — undated — [S] fetched: archive sources, Hopper/Metzler/Gronsky references, closed-eyes interviews, ~50 animators.
3. Documentary.org — Flee feature — https://documentary.org/node/36985 — undated — [S] fetched: reversed editing, looser trauma style, sound-and-storyboard master.
4. Wikipedia — Flee (film) — https://en.wikipedia.org/wiki/Flee_(film) — accessed 2026-10-18 — [T] fetched: team structure, release and awards.
5. Al Jazeera — Q&A: Meeting Cambodia's Oscar nominee — https://www.aljazeera.com/amp/features/2014/3/1/qa-meeting-cambodias-oscar-nominee — 2014-03-01 — [S] fetched: clay model of childhood home, 500+ figures, propaganda traces.
6. MPR News — Cambodia's 'missing pictures' molded from director's own life — https://www.mprnews.org/story/2014/03/30/cambodias-missing-pictures-molded-from-directors-own-life — 2014-03-30 — [S] fetched: paper lilies, thinning figures, composer detail.
7. Cinema Scope — TIFF 2013: The Missing Picture — https://cinema-scope.com/cinema-scope-online/tiff-2013-the-missing-picture-rithy-panh-cambodiafrance/ — 2013 — [S] fetched: narrator not Panh, tableaux morts.
8. Documentary.org — Cambodian Night and Fog: Rithy Panh — https://www.documentary.org/column/cambodian-night-and-fog-filmmaker-rithy-panh-takes-khmer-rouge-genocide — undated — [P] fetched: Panh's own words on figurines.
9. Wikipedia — The Missing Picture (film) — https://en.wikipedia.org/wiki/The_Missing_Picture_(film) — accessed 2026-10-18 — [T] fetched: half archive/half clay, 92 min, narrators.
10. Jerusalem Post — The man behind The Missing Picture — https://www.jpost.com/israel-news/culture/the-man-behind-the-missing-picture-395107 — undated — [T] snippet only: claim that Panh rejected animating the figures; UNVERIFIED.
11. Computer Graphics World — Psychorealism (Ryan) — https://cgw.com/Publications/CGW/2004/Volume-27-Issue-7-July-2004-/Psychorealism.aspx — 2004-07 — [S] fetched: Maya, Photoshop, Combustion, 20 hours of interviews.
12. NFB — Ryan — https://www.nfb.ca/film/ryan/ — [V] HTTP 200; fetched: rental $3.95 SD / $5.95 HD at fetch time; credits.
13. Documentary.org — Life Animated: how doc makers heighten perception through animation — https://documentary.org/feature/life-animated-how-doc-makers-heighten-perception-and-solve-problems-through-animation — undated — [S] fetched: Tower additive layer, TVPaint, actress-to-real-Claire.
14. Stanford Daily — Interview: Tower director Keith Maitland — https://stanforddaily.com/2016/11/11/tower-director-keith-meithland-talks-his-unique-documentary/ — 2016-11-11 — [S] fetched: archive lacked close-ups; Staggs/Minnow Mountain.
15. Michael J Cinema — Keith Maitland on Tower — https://michaeljcinema.com/2016/12/01/keith-maitland-on-tower/ — 2016-12-01 — [S] fetched: first-hand accounts only.
16. Wikipedia — Waltz with Bashir — https://en.wikipedia.org/wiki/Waltz_with_Bashir — accessed 2026-10-18 — [T] fetched: Flash cut-outs, ending dissolve into news footage, structure.
17. Festival de Cannes — Press conference: Waltz with Bashir — https://www.festival-cannes.com/en/2008/press-conference-waltz-with-bashir/ — 2008 — [P] fetched: Folman on memory and animation.
18. European Film Awards — Waltz with Bashir — https://www.europeanfilmawards.eu/efa-movie/waltz-with-bashir/ — undated — [T] fetched: 2,300 illustrations, studio video first, two actors.
19. Yale Library — Film Notes: Persepolis — https://web.library.yale.edu/node/173274 — undated — [S] fetched: 80,000 drawings, 20 animators, B/W style.
20. StoryCorps — Inside StoryCorps: turning words into visuals — https://storycorps.org/inside-storycorps-turning-words-into-visuals/ — undated — [P] fetched: story-by-story style, storyteller consultation.
21. Bostonia (Boston University) — From Sketch to Screen (Rocks in My Pockets) — https://www.bu.edu/bostonia/2016/from-sketch-to-screen/ — 2016 — [S] fetched: papier-mâché sets, 30,000 drawings, Photoshop/After Effects.
22. IndieWire — Interview: Nanette Burstein and Brett Morgen on The Kid Stays in the Picture — https://www.indiewire.com/features/general/interview-nanette-burstein-and-brett-morgen-on-their-robert-evans-doc-the-kid-stays-in-the-pictur-80275/ — undated — [T] snippet only (fetch returned HTTP 402 via redirect): "fairly accessible program".
23. Filmmaker Magazine — Last Tycoon (Kid Stays), Summer 2002 — https://filmmakermagazine.com/archives/issues/summer2002/features/last_tycoon.php — 2002 — [T] snippet only (fetch returned 403): 3D images, cut-outs, 800 photos in a minute.
24. kottke.org — The Kid Stays in the Picture — https://kottke.org/03/07/the-kid-stays-in-the-picture — 2003-07 — [S] fetched: subjects separated from backgrounds, different pan speeds.
25. Wikipedia — The Kid Stays in the Picture — https://en.wikipedia.org/wiki/The_Kid_Stays_in_the_Picture — accessed 2026-10-18 — [T] fetched: no production details.
26. Swirski, Richardt, Dodgson — Layered Photo Pop-Up — https://richardt.name/photopopup/ — 2011 — [P] fetched: manual 3D Ken Burns is laborious.
27. Niklaus, Mai, Yang, Liu — 3D Ken Burns Effect from a Single Image — https://arxiv.org/abs/1909.05483 — 2019-09-12 — [P] fetched: depth, point cloud, inpainting.
28. PictureCorrect — Parallax Animation: Bringing Still Photographs to Life — https://www.picturecorrect.com/parallax-animation-bringing-still-photographs-to-life/ — undated — [S] fetched: Fellows' workflow.
29. Motion Array — Animate flat 2D images in After Effects (2.5D parallax) — https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/ — undated — [S] fetched: content-aware fill, 28mm camera, Puppet tool.
30. PyPI — depthflow — https://pypi.org/project/depthflow/ (JSON API https://pypi.org/pypi/depthflow/json) — [V] 2026-10-18: version 1.0.1, uploaded 2026-08-25, AGPL-3.0, Python >=3.10.
31. GitHub — BrokenSource/DepthFlow — https://github.com/BrokenSource/DepthFlow — fetched 2026-10-18: description, AGPL-3.0; docs https://depth.tremeschin.com/ returned HTTP 403.
32. arXiv — Inpaint Anything — https://arxiv.org/pdf/2304.06790 ; PyPI lama-cleaner — https://pypi.org/project/lama-cleaner/ — [T] snippets only.
33. Mixing Light — Introduction to Resolve Fusion's 3D Camera, Part 1 — https://mixinglight.com/color-tutorial/introduction-3d-camera-fusion-part1 — [T] snippet only.
34. Blackmagic Design — DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — 2026-10-18 — [P] fetched: Studio 21 $295, features list.
35. The Rundown — Immersity AI — https://www.therundown.ai/tools/immersity-ai — [T] snippet only; pricing from third-party reviews, conflicting; UNVERIFIED.
36. Superhive — EZdepth — https://superhivemarket.com/products/ezdepth--ai-depth-map-generator-for-blender/docs — [T] snippet only.
37. Poynter — Meaning in Motion: Ken Burns and His 'Effect' — https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect — undated — [S] fetched: "mindless, anxious movement," "all real meaning accrues in duration."
38. CineD — Ken Burns effect article — https://www.cined.com/?p=406363 — undated — [S] fetched (partial): 33-second Roebling zoom.
39. The New York Times — Snow Fall — https://www.nytimes.com/projects/2012/snow-fall/index.html — [V] 2026-10-18: HTTP 200, 177,243 bytes; own CSS, jQuery 1.7.1 and 30+ MP4/WebM assets 200; Brightcove script 301.
40. OpenNews Source — How We Made Snow Fall — https://source.opennews.org/articles/how-we-made-snow-fall/ — 2013 — [P] fetched: stack, constraints, reader fatigue.
41. The Pudding — How to implement scrollytelling with six different libraries — https://pudding.cool/process/how-to-implement-scrollytelling — undated — [P] fetched.
42. The Pudding — The Largest Ever Analysis of Film Dialogue by Gender — https://pudding.cool/2017/03/film-dialogue/ — 2017-03 — [V] HTTP 200; cdnjs dependencies 200; Typekit script 200.
43. Wait But Why — Your Life in Weeks (Tim Urban) — https://waitbutwhy.com/2014/05/life-weeks.html — 2014-05-07 — [P][V] fetched, HTTP 200.
44. Note to Self — My Life in Weeks (Gina Trapani) — https://notetoself.studio/post/my-life-in-weeks/ — 2025-02-14 — [P] fetched.
45. werd.io — Life in Weeks — https://werd.io/life-in-weeks/ — undated — [P] fetched: author built it, did not publish; blog author not named on the fetched page.
46. eagereyes (Robert Kosara) — The bits are rotting in the state of data journalism — https://eagereyes.org/blog/2016/the-bits-are-rotting-in-the-state-of-data-journalism — 2016-07-14 — [S] fetched.
47. CNN (via KTVZ) — So much digital 9/11 coverage has disappeared — https://ktvz.com/lifestyle/technology/cnn-social-media-technology/2021/09/10/so-much-digital-9-11-coverage-has-disappeared-heres-why/ — 2021-09-10 — [S] fetched: Flash end 2020-12-31, NYT Ruffle.
48. It's Nice That — Nicholas Felton releases final ever personal Annual Report — https://www.itsnicethat.com/articles/nicholas-felton-releases-final-ever-personal-annual-report ; Berkeley iSchool — https://courses.ischool.berkeley.edu/i202/f11/node/696.html — [T] snippets only.
49. Adweek — Google Chrome Spot Captures Girl's Entire Life in 90 Seconds — https://www.adweek.com/?p=131368 — 2011 — [S] fetched: credits, true-story-with-actors.
50. YouTube (CannesPredictions mirror) — Google Chrome "Dear Sophie" — https://www.youtube.com/watch?v=pzOBOuyr-EU — [V] oEmbed 2026-10-18: video exists; official Google upload not confirmed.
51. TechCrunch — Dear Sophie follow-up — https://techcrunch.com/?p=301618 — 2011 — [T] snippet only.
52. Blog du Modérateur — Une vie entière sur Google : la vidéo Dear Sophie — https://www.blogdumoderateur.com/une-vie-entiere-sur-google-la-video-dear-sophie/ — 2011 — [S] fetched: "a bit too much like American soap operas."
53. YouTube (Google) — Parisian Love — https://www.youtube.com/watch?v=nnsSUqgkDwU — [V] oEmbed 2026-10-18: video exists, uploaded by Google channel.
54. UMass Dartmouth Corridors — John Michael Bell, Analysis of Google's 'Parisian Love' — https://corridors.sites.umassd.edu/?p=213 — undated — [S] fetched: 11-query sequence, 52 s.
55. comScore — Why Parisian Love was one of 2010's best ads — https://www.comscore.com/Insights/Blog/Scoring-with-Super-Bowl-Advertising-Why-Google-s-Parisian-Love-Was-One-of-2010-s-Best-Ads — 2011-02-04 — [T] snippet only.
56. The Ringer — Up's first 10 minutes, making of — https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of — 2022-06-14 — [S] fetched: beats, ~4.5 min, 30-40 minutes cut, dialogue removed.
57. Wikipedia — Up opening sequence — https://en.wikipedia.org/wiki/Up_opening_sequence — accessed 2026-10-18 — [T] fetched: jar, ties, reception.
58. /Film — Up opening, multiple last-minute changes — https://slashfilm.com/1582050/up-opening-emotionally-devastating-pixar-multiple-last-minute-changes-exclusive — undated — [S] fetched.
59. Art of the Title — Watchmen — https://www.artofthetitle.com/title/watchmen — [S] fetched: credits, 2.35:1, "situational type."
60. Motionographer — yU+Co: The Watchmen Titles — https://motionographer.com/2009/03/06/yuco-the-watchmen-titles/ — 2009-03-06 — [S] fetched: in-scene 3D type, 1939-1985.
61. Art of the Title — The Wonder Years — https://www.artofthetitle.com/title/the-wonder-years/ — [S] fetched: Super 8 montage, 1.33:1, Cocker.
62. Alphaville — Kathleen Williams on The Wonder Years credits — https://www.alphavillejournal.com/Issue12/HTML/ArticleWilliams.html — undated — [S] fetched: home-video markers, refreshed footage, generic action.
63. yU+co — The Addams Family titles — https://www.yuco.com/works/the-addams-family — [P] fetched: 13 years of portraits.
64. Blue Spill — Stiller & Meara: Nothing Is Lost — https://bluespill.co.uk/project/stiller-meara-i-nothing-is-lost/ — [P] fetched.
65. Independent magazine — Mind the Gap (Tarnation) — https://independent-magazine.org/2004/10/01/mind-gap/ — 2004-10-01 — [S] fetched: iMovie, $218.32, ~$400,000 clearance, cutting around the beat.
66. Documentary.org — Sarah Polley on Stories We Tell — https://documentary.org/node/33754 — undated — [P] fetched.
67. The A.V. Club — Stories We Tell — https://www.avclub.com/stories-we-tell-1798176746 — [T] snippet only.
68. NPR — Filmmaker Faces Her Father's Mortality By Staging His 'Death' Again And Again — https://www.npr.org/2020/09/30/918129488/filmmaker-faces-her-fathers-mortality-by-staging-his-death-again-and-again — 2020-09-30 — [T] snippet only.
69. YouTube — Noah takes a photo of himself every day for 6 years — https://www.youtube.com/watch?v=6B26asyGKDo — [V] oEmbed 2026-10-18: exists, channel Noah Kalina.
70. Wikipedia — Noah Kalina — https://en.wikipedia.org/wiki/Noah_Kalina — accessed 2026-10-18 — [T] fetched: six per second, piano score, Coolpix S10 since 2008.
71. TechCrunch — Everyday app — https://techcrunch.com/2011/03/21/everyday-iphone-app — 2011-03-21 — [S] fetched: alignment grid and overlay.
72. kottke.org — Half a Life in 2 Minutes — https://kottke.org/21/07/half-a-life-in-2-minutes — 2021-07 — [S] fetched: dlib, landmarks, 4K, Paul O'Mara.
73. Laughing Squid — Noah Kalina ages over 7,777 days — https://laughingsquid.com/noah-kalina-ages-over-7777-days/ — 2021 — [S] fetched: 60-face average, two months per second.
74. Wikipedia — Portrait of Lotte — https://en.wikipedia.org/wiki/Portrait_of_Lotte — accessed 2026-10-18 — [T] fetched: 15-second weekly clips, versions at ages.
75. Upworthy / PetaPixel — Lotte — https://www.upworthy.com/dad-films-daughter-each-week-for-20-years/?nb=1 ; https://petapixel.com/2019/11/21/dad-captures-time-lapse-portrait-of-his-daughter-from-birth-to-age-20 — [T] snippets only: 5-minute cut, 1,040 clips.
76. Salon — Ahree Lee — https://www.salon.com/2006/09/06/ahree/ — 2006-09-06 — [T] snippet only.
77. vladmandic/rife — https://github.com/vladmandic/rife ; dlib face_alignment — https://dlib.net/face_alignment.py.html — [T] snippets only.
78. Parting Stone — How to Make a Slideshow for a Funeral — https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/ — undated — [S] fetched: length, timing, licensing, export.
79. funeralOne — 22 Tips For Creating Tribute Videos — https://blog.funeralone.com/funeralone-products/life-tributes/tribute-video-tips/ — 2013-09-12 — [S] fetched: 25-30 photos, vary effects; vendor blog.
80. Funeral.com — https://funeral.com/blogs/the-journal/planning-a-memorial-slideshow-photo-selection-music-and-technical-tips (HTTP 429 when fetched) ; Mulin Blog — https://www.mulinblog.com/sound-photo-slideshow-editing-tips-on-pacing-and-photo-movement (DNS error when fetched) — [T] snippets only.
81. meyerweb (Eric Meyer) — Inadvertent Algorithmic Cruelty — https://meyerweb.com/eric/thoughts/2014/12/24/inadvertent-algorithmic-cruelty/ — 2014-12-24 — [P] fetched.
82. Engadget — Facebook's 'Year In Review' shows tragic side of software's shortcomings — https://www.engadget.com/2014-12-27-facebooks-year-in-review-shows-tragic-side-of-software.html — 2014-12-27 — [T] snippet only.
83. Apple Support — Photos memories — https://support.apple.com/guide/photos/pht96259d626/mac ; Google — redesigned Google Photos — https://blog.google/products/photos/redesigned-google-photos/ ; Trusted Reviews — https://www.trustedreviews.com/news/google-photos-update-makes-your-memories-better-than-you-remember-4267091 — [T] snippets only.
84. PremiumBeat — 100 Years of Color Grading — https://www.premiumbeat.com/blog/100-years-of-color-grading/ — undated — [S] fetched: bleach bypass, teal-orange.
85. InDepth Cine — Kodak 5247 — https://indepthcine.com/videos/kodak-5247 — undated — [S] fetched.
86. Cinematography.net — Kodachrome look thread — https://cinematography.net/edited-pages/kodachrome_look.htm — [T] fetched: forum, opinions.
87. Retro Renovation — When was avocado introduced as an appliance colour — https://retrorenovation.com/2020/12/26/when-was-avocado-introduced-as-a-color-on-kitchen-appliances/ — 2020-12-26 — [S] fetched.
88. No Film School — How to get the Super 8 film look — https://nofilmschool.com/get-super-8-film-look — [S] fetched.
89. AIC (Wallace) — Topics in Photographic Preservation 1989, Vol 3, Art 17 — https://resources.culturalheritage.org/pmgtopics/1989-volume-three/03_17_Wallace.html — 1989 — [P] fetched: dye loss, restoration.
90. Wikipedia — Cooper Black — https://en.wikipedia.org/wiki/Cooper_Black — accessed 2026-10-18 — [T] fetched.
91. Wikipedia — Super 8 film — https://en.wikipedia.org/wiki/Super_8_film — accessed 2026-10-18 — [T] fetched.
92. Wikipedia — VHS — https://en.wikipedia.org/wiki/VHS — accessed 2026-10-18 — [T] fetched.
93. Wikipedia — 110 film — https://en.wikipedia.org/wiki/110_film — accessed 2026-10-18 — [T] fetched.
94. Typeface-by-decade snippets: Creative Bloq — https://creativebloq.com/design/fonts-typography/iconic-typefaces-that-defined-each-decade ; Icons8 — https://blog.icons8.com/articles/retro-fonts-part-2/amp ; typography.guru — https://typography.guru/forums/topic/109244-picture-of-letterpress-souvenir/ — [T] snippets only (Creative Bloq and Icons8 fetches returned no body or 403).
95. Photutorial — https://photutorial.com/photos-statistics ; PetaPixel — https://petapixel.com/2025/06/18/the-number-of-photos-taken-in-2025-is-expected-to-exceed-two-trillion — [T] snippets only; estimates.
96. American Ancestors — scanning handout — https://www.americanancestors.org/sites/default/files/2022-01/scanning%20handout.pdf ; Library of Congress Signal — https://blogs.loc.gov/thesignal/2013/01/scanning-diy-or-outsource/ — [T] snippets only.
97. Electronic Arts Intermix — Family Focus — https://www.eai.org/titles/family-focus — [T] snippet only.
98. The Film Stage — Linklater and Coltrane on Boyhood — https://thefilmstage.com/features/richard-linklater-and-ellar-coltrane-discuss-the-twelve-year-journey-of-boyhood — [T] snippet only.
99. YouTube (Creators Project) — How To Animate a Photo | The 2.5D Effect — https://www.youtube.com/watch?v=ZVrYyX3bHI8 — [V] oEmbed title only; I did not watch it.
100. University of Mary Washington DKC — Building a Scrollytelling Website — https://dkc.umw.edu/tools/building-a-scrollytelling-website/ — undated — [S] fetched: static fallback.
101. RogerEbert.com — The Kid Stays in the Picture review — https://www.rogerebert.com/reviews/the-kid-stays-in-the-picture-2002 — 2002 — [T] snippet only.
102. Lehigh University news — Snow Fall snowballed — https://news.lehigh.edu/news/new-york-times-editor-shares-how-%E2%80%9Csnow-fall%E2%80%9D-snowballed — [T] snippet only: reach figures UNVERIFIED.
103. Family Tree Magazine — Dating Color Photographs — https://familytreemagazine.com/article/Dating-Color-Photographs — [T] snippet only (page paywalled when fetched).
104. BlenderNation — Combining 2D and 3D to create a parallax effect in Blender — https://www.blendernation.com/2020/10/11/combining-2d-and-3d-to-create-a-parallax-effect-in-blender/ — 2020-10-11 — [T] snippet only: camera projection mapping.
105. Quartz — Why Joe Cocker's Wonder Years theme song is missing on Netflix — https://qz.com/316860/why-joe-cockers-wonder-years-theme-song-is-missing-on-netflix — [T] snippet only: relicensing cost.


---

## Follow-up research (round 1)

Written 2026-10-18 by a Sonnet researcher in answer to the nine research follow-ups in `reviews/animated-round1.md`. New sources continue the numbering above ([106] onward, listed at the end of this section). Tier tags are as defined at the top of this file.

**How this round was done.** The WebSearch tool refused every query in this session (its per-turn budget was already used up), and I did not route around it. Everything below comes from pages fetched directly by URL: Blackmagic's own pages and PDFs, PyPI JSON, repositories cloned read-only through the session's git proxy, a few aggregator pages, and tests I ran in the cloud container (Linux, no GPU) on 2026-10-18. Where an answer needs a search or the maker's own machine, it says so. Test inputs were synthetic (a generated picture and depth map); no personal material was used and no AI model weights were downloaded.

### Bottom line

| # | Question | Short answer | Status |
|---|---|---|---|
| 1 | Fusion 3D nodes in free Resolve 21 on Windows | Very probably yes. The Resolve 21 Reference Manual documents Image Plane 3D, Camera 3D, Merge 3D and Renderer3D with no "Studio Version Only" tag, while it tags other Fusion features that are Studio-only. No Blackmagic page says "free includes the 3D nodes" in so many words. | Probable; a 5-minute test on the PC settles it |
| 2 | Resolve 21 minimum/recommended RAM and GPU; does it run on the maker's PC | Blackmagic's requirement numbers could not be retrieved. The maker's hardware is still unknown. | UNVERIFIED; needs the maker |
| 3 | DepthFlow CLI, depth models, Windows install | Verified by running DepthFlow 1.0.1 in the container. One-line CLI chain works, but a CLI-only render has a static camera; motion needs a small Python subclass. Depth models `da1`/`da2` (small to giant). All compiled dependencies have Windows wheels. | Verified on Linux; Windows untested |
| 4 | dlib on Windows | No: PyPI `dlib` 20.0.1 is source-only. Use OpenCV's YuNet (`cv2.FaceDetectorYN`, five landmarks, one wheel) instead. | API verified; accuracy and Windows run untested |
| 5 | ArtCraft capability matrix | See the table in F5. FilmCraft and EffectCraft cover camera move, title cards and H.264 MP4; PhotoCraft covers cutout/fill and crop; none is proven on Windows. | From source and docs, not from running the apps |
| 6 | Flatbed or phone | Unknown; ask the maker. A phone on a tripod or copy stand is an accepted route. | Needs the maker |
| 7 | Where to watch the four films | US only: all four for about 4 USD in total (three are free with a library card or ads). Maker's country unknown. | US per aggregator; country unknown |
| 8 | Kalina "six per second"; Watchmen runtime | No primary source for the phrase. Kalina's own upload gives 5:45 for 2,356 days (6.8 days per second). Watchmen main title: studio says "6-minute sequence"; its own reel runs 5:35. | Partly resolved |
| 9 | Consent for people in photographs | No standard wording for photographed third parties was found. Closest sourced practice: documentary makers let subjects reconsider after signing; oral-history ethics adds review and withdrawal. A drafted notice and three audience tiers follow. | Draft; not legal advice |

### F1. Fusion 3D in free DaVinci Resolve 21

- **Current versions (dated).** Blackmagic's support-site data lists DaVinci Resolve 21 on 3 Jun 2026, 21.0.1 on 24 Jun, 21.0.2 on 2 Jul, 21.0.3 on 22 Jul, 21.0.4 on 5 Aug, 21.1 on 8 Sep and 21.1.1 on 2 Oct 2026, each for Mac, Windows, Linux and Windows ARM. Each notice says technical support for the free version is only via the Blackmagic community forums. The 21.1 notice mentions "over 25 new Krokodove shape and 3D tools" in Fusion. [111] (an undocumented JSON endpoint behind the support page, fetched today.)
- **What the product pages say.** The Resolve 21 page says Fusion has "hundreds of 2D and 3D tools", and separately that Studio "adds tons of additional effects, 3D and more". The Studio page lists "stereoscopic 3D" tools, multi-GPU and the Neural Engine as Studio-only, and does not name ImagePlane3D, Camera3D, Merge3D or Renderer3D. The `/compare` URL serves the same page and has no comparison table, and the What's New page has no free/Studio split. The 150-page Resolve 21 New Features Guide (created 2026-04-10) has no free-versus-Studio table either; its extracted text never uses the word "Studio". [106][107][108][110] So the Blackmagic marketing pages do not answer the question.
- **What the manual says (the strongest evidence I found).** The Resolve 21 Reference Manual (4,444 pages; PDF created 2026-07-09) documents the Fusion page inside DaVinci Resolve. Chapter 84 ("3D Compositing Basics", from printed page 1873) and Chapter 88 ("3D Nodes", from page 1970) cover Image Plane 3D [3Im], Camera 3D [3Cm], Merge 3D [3Mg] and Renderer3D [3Rn], and Chapter 63 ("Exploring the Fusion Interface", around printed page 1344) lists "seven 3D nodes" (ImagePlane3D, Shape3D, Text3D, Merge3D, Camera3D, SpotLight, Renderer3D) among the basic toolbar nodes. None of these carries a Studio tag. The same manual does tag Studio-only items explicitly: "Using Multilayer Nodes (Studio Version Only)", "Deep Image Compositing Toolset (Studio Version Only)", "Cryptomatte [Cry] (Studio Version Only)", "Vector Warping Toolset (Studio Version Only)" and "AI Animated Subtitles (Studio Version Only)". [109] The inference (mine): the four nodes we need are not Studio-gated. It is an inference from absence of a tag, not an explicit "free includes 3D" statement.
- **Depth Map node.** The manual lists "Depth Map [DMp]" under Matte nodes without a Studio tag, but Blackmagic's Studio page shows "3D Depth Map" inside its Neural Engine section. Free-edition availability of Depth Map is UNVERIFIED. It does not matter for our route, because DepthFlow makes its own depth map (F3). [107][109]
- **Windows hardware caveat from the manual.** Fusion's 3D settings tell users that "OpenGL hardware varies widely in capabilities" and that driver revisions can introduce bugs, and that more GPU memory makes Renderer3D supersampling faster. A working OpenGL driver is therefore part of "Fusion 3D works". [109]
- **Five-minute test for the maker (settles it).** On the PC: open Resolve free, open the Fusion page, open the Effects Library > Tools > 3D (or press Shift+Space in the node editor and type each name; menu paths from general knowledge, not from a fetched page). Check that Image Plane 3D, Camera 3D, Merge 3D and Renderer3D are present and not greyed out, then wire Image Plane 3D > Merge 3D (+ Camera 3D) > Renderer3D with a photo and view the result. Record the Resolve build number from Help > About.
- **Consequence (my judgment).** Even if the nodes are free, the Fusion route needs Resolve installed and running on a machine the charter calls memory-constrained, while DepthFlow does the same parallax in the cloud (F3). Keep Fusion 3D in the playbook only as the "if you already know Resolve" appendix.

### F2. Resolve 21 requirements and the maker's PC

- **Not retrievable today.** Blackmagic's `techspecs` page lists hardware products only. The support family page renders its downloads dynamically and showed no requirements to my fetch. Guessed URLs for the Configuration Guide and the Read Me returned 404. [106][112] I did not find a Windows RAM, GPU or VRAM figure for Resolve 21 and will not quote one from memory. UNVERIFIED.
- **Fragments from the Reference Manual (not requirements).** Voice Convert needs "a minimum of 8 GB of video RAM before it will activate". The Apple Immersive workflow lists 64 GB of system memory on macOS. Preferences include a "Limit Resolve Memory Usage" setting, and the GPU processing mode is chosen between CUDA, OpenCL and Metal. [109]
- **Free-edition limits that are stated.** "Virtually all 8-bit video formats at up to 60fps" and "Ultra HD 3840 x 2160". [106]
- **Maker's hardware: still unknown.** Nothing in the charter or reviews records RAM, GPU, VRAM, free disk or Windows build. I cannot say whether Resolve is usable there. What the maker should send (general Windows knowledge, not sourced): total RAM (Settings > System > About), GPU model and dedicated GPU memory (Task Manager > Performance > GPU, or run `dxdiag`), free space on the drive that will hold the project, Windows version, and whether Python or `uv` is installed.
- **Rule of thumb for the playbook (my judgment).** Do not put Resolve on the critical path. The cloud container renders parallax and stills-to-video (F3), FilmCraft or a free NLE assembles, and Resolve is optional. Revisit once the inventory arrives.

### F3. DepthFlow: CLI, depth models and Windows install

All of this was read from the repository (commit 32725b7, 2026-10-10: `readme.md`, `pyproject.toml`, `depthflow/__main__.py`, `scene.py`, `estimators/`, `website/*.md`, `examples/batch.py`), then run: DepthFlow 1.0.1 and ShaderFlow 0.11.3 installed from PyPI into a venv in the container (Python 3.13, Linux, no GPU). [113][114] The docs site returned 403 earlier, but the same pages live in the repo under `website/`.

- **Entry points.** `depthflow` or `depth` (both installed by the package), `python -m depthflow`, or `uvx depthflow ...`. Python >= 3.10 (pyproject). Licence AGPL-3.0. The `examples/batch.py` script header asks for Python >= 3.14. [113]
- **How the CLI is built.** Commands chain on one line, in any order, before the final `main`: `input` (image, optional depth map), an estimator (`da1` or `da2`), `state` (camera parameters), a video encoder (`h264`, `h265`, `av1-svt`, `av1-rav1e`, NVENC variants) and an audio encoder, then `main` (render). Verified `--help` output in the container:
  - `depthflow input -i IMAGE [-d DEPTH]` (URL or path; no `-d` means "estimate").
  - `depthflow main` options: `-w/--width` (default 1920), `-h/--height` (1080), `-x/--scale`, `-r/--ratio` (for example 4:3), `-f/--fps` (60), `-q/--quality` (50), `-s/--ssaa` (1.0), `-o/--output`, `-t/--time` (seconds), `--speed`.
  - `depthflow h264 --preset (default slow) --crf (default 20) --tune --profile --bitrate`.
  - `depthflow da2 --model small|base|large|giant` (default small); `da1` takes the same sizes.
  - `depthflow state` flags: `--height` (0.2, the parallax strength), `--steady`, `--focus`, `--zoom`, `--isometric` (0.3), `--dolly`, `--offset`, `--center`, `--origin`, `--vignette.*`, `--lens.*`, `--inpaint.limit`, `--color.saturation/contrast/brightness/sepia`, `--blur.*`.
- **Verified one-line render (container, 2026-10-18).** `depthflow input -i photo.png -d depth.png state --height 0.25 --isometric 0.6 h264 --crf 23 --preset veryfast main -o out.mp4 -t 2 -f 24 -w 640 -h 480` rendered 48 frames in 3.7 s on a GPU-less Linux container through Mesa software OpenGL ("llvmpipe"), with and without a virtual display. ffprobe: H.264 High, yuv420p, 640x480, 24 fps, 4:3. [113]
- **Important caveat: CLI-only means no camera motion.** `state` sets fixed values. In my test the first and last frames of the CLI render were identical (mean difference 0.0), while a render with a subclass was not (mean difference 6.1 on a 0-255 scale). The docs say the same: animation is done by subclassing `DepthScene` and writing `update()`, and a simple built-in animation system is "a future release". [113] The verified minimal script (synthetic inputs) was:
  - subclass `DepthScene`; in `update()` set `self.state.offset = (0.25 * math.sin(self.tau * math.pi), 0.0)` and `self.state.zoom = 1.0 - 0.08 * self.tau`; create it with `backend="headless"`, call `scene.ffmpeg.h264(preset="veryfast", crf=23)`, `scene.input(image=..., depth=...)`, then `scene.main(output=..., time=2, fps=24, width=640, height=480)`. `tau` runs 0 to 1 over the clip; `cycle` runs 0 to 2*pi.
  - Speed: 12.3 frames/s at 640x480 in the container. A 1080p frame has 6.75 times the pixels, so a 10 s clip at 24 fps (240 frames) would take roughly two minutes there (my extrapolation, UNVERIFIED).
- **Depth models.** Default is Depth Anything V2 (`da2`), loaded through Hugging Face `transformers` as `depth-anything/Depth-Anything-V2-{size}-hf`; Depth Anything V1 (`da1`) is also wired. The docs mark Depth Anything V3 as waiting on a transformers release, and DepthPro, Marigold and ZoeDepth as "not implemented" or unmaintained. Licences: the Small checkpoint is Apache-2.0 (model card: 24.8M parameters); the docs warn that the other sizes are CC BY-NC 4.0 (non-commercial with attribution), which a private gift is, but Small is the safe default. [113][116] You can also pass your own depth map with `-d` (near is white), which I used in the test and which needs no torch. Estimated depth maps are cached on disk (default limit 32 MB). By code reading, the estimator runs locally and the only download is the model weights; the image is not uploaded. First-use download time and CPU speed of estimation are UNVERIFIED (I did not install torch).
- **Quality notes from the docs.** Use images with a clear central subject and smooth or distant backgrounds; wires, fences, hair and small details cause artefacts; match output resolution to the input; SSAA 2.0 is "plenty" for final exports and doubling SSAA is exactly 4x GPU cost; depth precision matters more than silhouette precision. [113]
- **Windows install steps (from the docs, plus my wheel check).** (1) Install Python (3.13 or 3.14) or install `uv` from astral.sh. (2) Install FFmpeg and put it on PATH (the docs say to have it "available in PATH" or to drop the executables in the working directory). (3) In a fresh venv: `python -m pip install depthflow`, then run `python -m depthflow --help`; or with uv: `uvx depthflow main`. (4) Make a first test with a supplied depth map (no model download), then one with the estimator. The repo's Windows help page says "No known frequently asked questions at the moment", the portable (Pyaket) build and Docker images are marked work in progress, so there is no Windows-specific guidance and no Windows test report in the repo. [113] PyPI JSON shows win_amd64 wheels for cp313 and cp314 for every compiled dependency (glcontext, moderngl, glfw, imgui-bundle, turbopipe, numpy-quaternion, scipy, torch, torchvision), and pure-Python wheels for the rest, so no C++ toolchain should be needed. [115] The 121 MB Windows `torch` wheel on PyPI is consistent with a CPU-only build; CUDA builds are served from PyTorch's own index (my inference, UNVERIFIED). Rendering needs a working OpenGL driver; Windows behaviour with an integrated GPU or with no GPU is UNVERIFIED.
- **Where to run it.** The container run proves the cloud path works without a GPU. Photos then have to be uploaded to the container, which conflicts with the charter's rule on personal material; so for real family photos the run happens on the PC, and the container is used for synthetic or already-cleared test material. This is a decision for the maker and the pipeline track.

### F4. Face alignment on Windows without dlib's toolchain

- **dlib from PyPI.** Version 20.0.1 (2026-03-29) is a source distribution only (3.2 MB, no wheels). dlib's own page says the Python install needs "CMake and a working C++ compiler". On Windows that means installing Visual Studio's C++ build tools (my reading; the page's Windows section is about C++ programs). Avoid on a memory-constrained PC. [117][119]
- **dlib-bin.** Version 20.0.1.post1 (2026-10-02) ships win_amd64 wheels for Python 3.10 to 3.15. It is built by a third party (the `alesanfra/dlib-wheels` GitHub project, which does not claim to be official) while its PyPI metadata lists Davis King as author. It would install without a compiler, but it is an unofficial binary going onto the machine that holds the family photographs. If used: pin the version and hash, use a throwaway venv. [117][118]
- **The model file is separate.** dlib's five-point predictor `shape_predictor_5_face_landmarks.dat` was trained on 7,198 faces and is released into the public domain (repo CC0-1.0). dlib's README describes it as the corners of the eyes and the bottom of the nose, whereas the earlier note [72] (kottke) says eyes, nose and mouth corners; for eye-line alignment only the two eye positions matter. [120]
- **Recommended: OpenCV YuNet.** `opencv-python` 5.0.0.93 (2026-07-02) has a single abi3 win_amd64 wheel (43 MB). I installed OpenCV 5.0.0 in the container and confirmed `cv2.FaceDetectorYN` exists; its docstring says each detected face is a row of 15 numbers: box (x, y, w, h), right eye, left eye, nose tip, right and left mouth corners, and a score. That is exactly the five-landmark set, from one function call, no compiler. The YuNet model is MIT-licensed in `opencv_zoo`; the README's default file is `face_detection_yunet_2026may.onnx` (dynamic input shape), detecting faces from about 10x10 to 300x300 pixels. [122] I could not download the model (GitHub raw is blocked from the container, HTTP 403), so there is no accuracy test on any image. Its behaviour on small, faded or tilted prints is UNVERIFIED; try it on the eight worst portraits of the maker's own set.
- **Second option: MediaPipe Face Landmarker.** `pip install mediapipe` (1.1.1, 2026-10-14, Apache-2.0) has a Python-version-independent win_amd64 wheel of 22 MB; Google's guide shows 478 landmarks per face, with the model bundle downloaded separately. Heavier than YuNet but gives eye contours; EffectCraft already uses it for face tracking as an optional 3.8 MB download. [121][126]
- **Fallback.** Manual two-click eye marking on each portrait (the earlier note's manual grid fallback [71]) for the 8 to 15 portraits of a ladder is faster than debugging an install, and is the right plan if both libraries fail.
- **Where.** Alignment touches personal photographs, so it runs on the PC. All three options are CPU-only and local.

### F5. What the ArtCraft apps can do today (from source and docs, not from running the apps)

Versions read (shallow clones, 2026-10-18): FilmCraft 0.9.0 (release commit 2026-10-17), EffectCraft 0.12.0 (2026-10-17), VectorCraft 0.13.1 (2026-10-18), PhotoCraft 0.10.0 per `Cargo.toml` (main as of 2026-10-17). These are newer than the tags recorded in the craft tracks earlier today, so the pins there should be refreshed. [123][124][125][126] "Present in source" is not "works well": the craft-visual track's own rule is to rate by tests and oracles, and I ran none of these apps (no GUI, no Windows).

| Capability | PhotoCraft | VectorCraft | FilmCraft | EffectCraft |
|---|---|---|---|---|
| Layer cutout and fill | Yes. Marquee, lasso, magic wand, Quick Selection, Object Selection, Select Subject/Sky (`select.quick/object/subject/sky`), layer masks, Select and Mask; fill with `edit.fill` and Content-Aware Fill (`edit.contentAwareFill`, PatchMatch-style; the vendor scorecard marks its 10 MP speed budget, P21, as pass). The vendor says Select Subject is "classical", there is no ML runtime, the Remove tool is non-generative and Content-Aware Fill is basic. | No (vector tool; Image Trace only) | No | Roto Brush with an optional MobileSAM download (40 MB) for video; use on stills UNVERIFIED |
| Keyframed camera move on a still | No | No | Yes. Motion on every clip: position, scale, rotation, anchor; Bezier/ease/hold keyframes with value and velocity graphs; the README shows an eased Scale push-in. | Yes. Layer transforms with keyframes and 3D cameras (orbit, pan, dolly); stills import as footage |
| Grain | Yes, Filter > Noise > Add Noise (`filter.noise.addNoise`) | No | Partial. Only a "Noise" effect (per-frame random noise with a grain-size control) and Light Leaks; no film-grain emulation found | Yes. "Add Grain" (GPU), "Match Grain" and "Remove Grain" in Noise and Grain |
| 4:3 crop | Yes. Crop tool with ratio and W x H fields; `image.crop`; scorecard TOOL-214-9 "done" | Artboards of any size | Yes. Sequences of any size (`file.newSequence {width, height, fps}`, so 1440x1080 is 4:3); a Crop effect | Yes. Composition size, and Crop in Render Settings |
| Title cards | Type tool exists (vendor rates type at about 40 percent; a Type tool freeze on macOS is issue #2518) | Yes. Type, live effects such as glow; export art for placing in an edit | Yes. Type, Shape and Pen tools; graphic clips with text and shape layers, keyframable | Yes. Text and shape layers (`layer.newText`), Essential Graphics |
| Export to H.264 MP4 | n/a (stills) | n/a (SVG, PDF, images) | Yes. Own H.264+AAC encoder to MP4 (`file.exportMedia {format: "h264", crf, width, height, fps}`); README: a 6 s 960x540 render takes 1.3 s | Yes. Render queue with H.264 MP4; CLI `effectcraft-cli render --comp Main --out main.mp4` |

- **Agent-drivable.** All four ship CLI/MCP front ends (`photocraft-cli run|batch|mcp`, `filmcraft-cli mcp`, `effectcraft-cli render|exec|set|mcp`). [123][124][126]
- **Stability warnings stated by the vendors.** FilmCraft: routine runtime testing off macOS is missing (`docs/gaps.md`). EffectCraft: "macOS is the most tested platform. Linux and Windows users have hit basic interaction bugs". PhotoCraft: no-GPU start failures (#2519, #2412) and GPU panics are listed in its parity assessment. [123][124][126]
- **What the playbook can say now (my judgment).** Cutout and gap fill: agent first (SAM + LaMa [32]), PhotoCraft's Select Subject/Object and Content-Aware Fill as the by-hand refinement and fallback. Camera move on a still: DepthFlow in a Python subclass for parallax, FilmCraft Motion keyframes for flat pushes. Grain: EffectCraft Add Grain or LightCraft grain (craft-visual), not FilmCraft's Noise unless it looks right on the test. 4:3: set the FilmCraft sequence to 1440x1080 or crop in PhotoCraft first. Title cards: FilmCraft Type tool inside the edit; VectorCraft only when a card needs drawn lettering. Export: FilmCraft H.264 MP4 with an ffmpeg-in-the-cloud fallback. Mark every row `TODO(maker test)` until the maker has run the same photo through it on the PC.
- **Five-minute acceptance test for the maker.** Pick one public-domain photo. In PhotoCraft: Select Subject, cut to a layer, Content-Aware Fill the hole, add noise, crop 4:3. In FilmCraft: new 1440x1080 sequence, place the photo, keyframe scale 100 to 108 percent with ease, add a title with the Type tool, export H.264 MP4. Note app versions, crashes and times.

### F6. Flatbed scanner or phone

- **Answer: unknown.** Nothing in the charter or reviews says. Ask the maker two questions: "Do you own or can you borrow a flatbed scanner (model, if known)?" and "What phone do you have, and is there a tripod or a way to hold it steady above a table?"
- **A phone route is an accepted method.** A genealogy society's digitising handout (PDF modified 2022-01-05; its table is based on the ALCTS 2013 minimum capture recommendations) says "the best options for home digitization projects are a flatbed scanner or a camera with a tripod or copy stand". Scanners: at least 600 dpi optical. Cameras: at least 10 megapixels, with control of ISO, shutter, white balance; RAW and a macro lens recommended; ISO 100 to 200, f/8 to f/11. Targets: photographs up to 8 x 10 in at 400 ppi (about 4,000 px on the long edge); 8 x 10 to 11 x 14 in at 400 to 600 ppi (6,000 px); larger at 600 ppi (8,000 px). [127] The Library of Congress Signal post says 4 x 6 and 5 x 7 prints "can be scanned at 300 dpi" and 8 x 10 and larger "at 600 dpi or greater", and TIFF is the archival format. [128]
- **What this does to the plan.** The earlier note asks for 600 ppi on small prints because a push-in with a parallax margin needs about 3,300 px across (my arithmetic, above); that is stricter than both references. A phone shot of a 4 x 6 print that reaches about 4,000 px on its long edge clears the 3,300 px need, so Exercise 5 does not depend on owning a flatbed. A flatbed matters for flatness, glare and speed over a few hundred prints. Not decided: which route; that is the maker's answer.

### F7. Watching Up, Flee, Tower and The Missing Picture legally

The maker's country is not recorded anywhere in the charter or reviews, so this is the United States only, from JustWatch listings that state they were checked on 17 October 2026; prices move. For another country the same pages exist under `justwatch.com/<country code>/movie/<title>`. [129]

| Film | Cheapest legal way (US) | Other options (US) |
|---|---|---|
| Up (2009) | Rent 3.99 USD on Amazon Video | Disney+ subscription (listed 12.49 USD per month); rent 5.99 USD on Apple TV or Fandango At Home; buy 10.99 to 19.99 USD |
| Flee (2021) | Free with ads on Tubi | Rent 3.99 USD on Amazon, Apple TV or Fandango At Home; buy 9.99 USD |
| Tower (2016) | Free on Kanopy or Hoopla | Kino Film Collection subscription 5.99 USD per month; rent 2.99 USD on Amazon, Apple TV or Fandango At Home |
| The Missing Picture (2013) | Free on Kanopy (SD) | Rent 3.99 USD on Amazon or Apple TV (HD), 2.99 USD on Fandango At Home (SD, French); Strand Releasing channel on Amazon 4.99 USD per month |

- **Total for week 2 in the US:** about 4 USD (Up rental) if Kanopy or Hoopla works for you. Kanopy and Hoopla are usually reached through a public-library card and may cap monthly plays; the listings do not say, so that is UNVERIFIED.
- **Reading the listing.** The Fandango listing for The Missing Picture is marked French and SD. I did not check audio language or subtitles on any platform. Streaming on Amazon "channels" and Disney+ is subscription-bound; buying a DVD is also on the pages.
- **Ask the maker:** country, and whether they have library cards.

### F8. Kalina's "six photos per second" and the shipped Watchmen title length

- **Kalina.** The original 2006 upload on his own YouTube channel is 345 seconds long (5:45), published 2006-08-27, with the description "January 11, 2000 - July 31, 2006. 2356 Days. A work in progress ... original music by Carly Comando". [130] Arithmetic (mine): 2,356 days in 345 s is at most 6.8 photos per second if every day is shown and the title and end take no time; with missed days and a title it is plausibly about 6. So "about six per second" is consistent with his own numbers. The phrase itself ("shows the photos chronologically, six per second") appears in Wikipedia, cited there to a Gothamist article "Noah Kalina, Photographer" by Jen Carlson dated 2008-01-09. [131] I did not open that article: its address redirects to a bot-gating service and I did not follow it. Kalina's own site pages (the home page, `everyday.noahkalina.com`, now `everyday.photo`, and its FAQ) do not state a rate. **Verdict: no primary statement of "six per second" found; use "about six or seven a second (5:45 for 2,356 days)" with the YouTube page as the source, and keep [70] as the source for the Wikipedia phrase.** Note: the 2,356-day figure is for the first video only; later videos differ.
- **Watchmen titles.** The title studio's own work page for the sequence says "This 6-minute sequence was conceived and directed by Zack Snyder". [132] The "Main Title" video on that page is hosted on Vimeo as "WATCHMEN - MT" by yU+co, 335 seconds (5:35) long, uploaded 2016-09-26 (Vimeo oEmbed). [133] Motionographer's six-minute figure [60] is the same object: "an already edited six-minute sequence that was built without the placement of titles in mind". So the shipped main-title sequence is about 5.5 to 6 minutes, and the studio's reel is 5:35. What I could not establish: how much of that is the Bob Dylan "Times They Are a-Changin'" montage and how much is the preceding Comedian scene (my guess is that the six minutes include both; UNVERIFIED). Wikipedia gives the film's theatrical runtime as 162 minutes and says the opening credits montage reviews costumed heroes from 1939 to 1977, with no length. The playbook should say "about 6 minutes including the fight scene, UNVERIFIED how much is the montage" or avoid a number.

### F9. Consent and opt-out for people in the photographs

**What I found.** No standard release or notice wording for photographed third parties (relatives, friends, ex-partners) in a personal documentary turned up in anything I could fetch. The nearest sourced practice has three parts:

1. Documentary makers' own account (26-page study of 41 directors, Center for Media and Social Impact, 2009): most subjects signed releases giving the maker "complete editorial control and ownership", but release terms were often dictated by insurers, and makers "often felt that subjects had a right to change their minds ... or to see the material involving them or even the whole film in advance of public screenings". Core principles were "do no harm" and "protect the vulnerable". Example: a mother objected to a scene of her minor son even though releases were signed; the maker let the family deliberate, and said "legally I could have put it in ... but hey, I want to sleep at night". Only one of the directors put fine-cut approval in a legal document, with the limit that subjects could not object merely to how they looked, but could object on grounds of "hurting their family". [134]
2. Oral-history ethics (Oral History Association): consent is documented before the interview; narrators get to review and approve what is released; options include the right to delete, restrict or redact portions, or to decline public release; do not promise what you cannot keep. [135] Our `surprise-ops` track already uses this for contributors; it does not cover people who only appear in a photograph.
3. One tension to avoid: in the same study a director says he used stand-in family footage without disclosure ("Saying 'this blurry figure is not our guy' would ruin the scene"). That conflicts with Charter Principle 4 (reconstructions are visibly reconstructions); do not copy it. [134]

I also checked Documentary.org's Polley interview [66] and Doc Society's ethics page [136]; neither says anything about consent from people shown in archive photographs.

**Proposed rule (my design, not legal advice; a lawyer should check anything public).** Three audiences, with consent depending on how far the film travels.

| Audience | Who is in the room | Rule for a living, identifiable person in a photo |
|---|---|---|
| A. Private link: family only, password, time-limited, not searchable | Family she chose | Notice plus easy removal. Ask anyone likely to mind (ex-partners, estranged relatives) first, or leave them out. Everyone else: the notice below goes to them after the reveal, with a removal window. |
| B. One-off event screening | Family and friends in a room, no copies handed out | As A, plus a printed opt-out line on the invitation or programme, and the same removal window. Do not show a person at an event who has said no; a removal request after the event is honoured in any later copy. |
| C. Anything public or forwardable (open link, social media, festival) | Anyone | Written permission from each identifiable living person, or obscure or omit them; minors only with a guardian's permission. This is outside the current plan. |

- **Default (mine, aligned with `surprise-ops` T1.4 "ex-partner: default do not approach").** Ex-partners: omit or obscure unless the proxy says they are on good terms. Deceased people: no consent step, but the proxy decides on dignity. Children in old photos who are now adults: they are people to ask, not "kids". People the maker cannot reach: leave out of any version beyond A.
- **Notice wording (draft).** "We are making a film for [NAME]'s [occasion] from family photographs, and a photo of you ([thumbnail or description]) is in it. It will be [shown once, to about [N] family and friends on [DATE] at [PLACE] / sent as a private, password-protected link to [family list] until [DATE]]. It will not be put on social media or sent to anyone else. If you would rather not be in it, tell [CONTACT] by [DATE] and we will remove or blur the photo, no reason needed, and also later for any copy we make. Reply: YES / NO / ONLY IF I SEE IT FIRST." Elements and sources: what, where, who sees it, how long, and an easy exit [135]; the right to change one's mind and to see it first [134]. Sending it is limited by the surprise: it goes only to people already in the secret, and to everyone else after the reveal; see the `surprise-ops` withdrawal window (it ends 2027-02-19 there, so align the dates).
- **The `consent status` field (suggested values).** `asked-yes`, `asked-no`, `asked-if-seen`, `not-asked-private-only` (shown to audience A only), `not-asked-omit`, `deceased-proxy-ok`, `minor-guardian-yes`. A photo's scene card also records which audience tier it is cleared for. This vocabulary is my design; nothing in the sources defines it.
- **Open:** a legal check for any use beyond audience A or B (laws on images of people vary by country, and the maker's country is unknown); no UK/EU rule was checked here.

### Still UNVERIFIED after this round

- Resolve 21 Windows RAM, GPU and VRAM requirements; whether Resolve runs on the maker's PC; free-edition status of the Depth Map node. Whether the Fusion 3D nodes appear in the free edition (probable, not confirmed by test).
- DepthFlow: Windows run; depth-estimator speed on CPU and first-use download; behaviour with an integrated GPU or none.
- YuNet and MediaPipe accuracy on faded or tilted prints; the YuNet model download.
- Every ArtCraft capability in F5 as lived behaviour on Windows; whether FilmCraft's Noise looks like grain.
- Kanopy and Hoopla access limits; subtitles on any platform; prices outside the US; the maker's country.
- Primary statement of Kalina's "six per second"; the length of the Dylan montage within the Watchmen sequence.
- Legal sufficiency of any consent wording.

### Questions only the maker can answer

1. Hardware: RAM, GPU model and dedicated memory, free disk space, Windows version, whether Python or `uv` is installed, and whether Resolve is installed (and which build).
2. Flatbed scanner or phone (and tripod).
3. Country (for streaming, recording and image law) and whether library cards are available.
4. Which ArtCraft versions are installed (Launcher > table view), and whether the installers are MSI or portable.

### Playbook and note consequences

- Tools table, Resolve row: add "Fusion 3D nodes (Image Plane 3D, Camera 3D, Merge 3D, Renderer3D) are documented without a Studio tag in the Resolve 21 manual [109]; confirm in 5 minutes on the PC (F1)". Open question 8 is partly closed (F1), question 9 is closed for syntax and install (F3), with the static-camera caveat.
- Summary item on parallax: DepthFlow can be driven from one command line, but camera motion needs a small Python subclass; the cloud container can render it without a GPU (F3).
- Exercises: replace "dlib" in Exercise 6 with "OpenCV YuNet; manual fallback" (F4); add the phone-and-tripod route to Exercise 5 (F6); the stopwatch exercise in week 2 costs about 4 USD in the US (F7).
- Pin refresh: FilmCraft 0.9.0, EffectCraft 0.12.0, VectorCraft 0.13.1, PhotoCraft 0.10.0 (F5).
- Rights and privacy: adopt the three-tier rule and notice in F9 for the scene card; the Haiku scribe should keep it marked "draft, not legal advice".

### Sources (continued from [105])

106. Blackmagic Design — DaVinci Resolve 21 product page (the `/compare` address serves the same page) — https://www.blackmagicdesign.com/products/davinciresolve ; https://www.blackmagicdesign.com/products/davinciresolve/compare — fetched 2026-10-18 (footer copyright 2026; no release date) — [P] free vs Studio blurb, "hundreds of 2D and 3D tools", Studio "adds tons of additional effects, 3D and more".
107. Blackmagic Design — DaVinci Resolve Studio page — https://www.blackmagicdesign.com/products/davinciresolve/studio — fetched 2026-10-18 — [P] Studio-only: stereoscopic 3D tools, multi-GPU, Neural Engine ("3D Depth Map" image shown there).
108. Blackmagic Design — What's New in DaVinci Resolve 21 — https://www.blackmagicdesign.com/products/davinciresolve/whatsnew — fetched 2026-10-18 — [P] Fusion/Photo page items; no free/Studio table.
109. Blackmagic Design — DaVinci Resolve 21 Reference Manual (PDF, 187 MB, 4,444 pages, created 2026-07-09 per PDF metadata) — https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf — downloaded and text-extracted 2026-10-18 — [P] Fusion 3D chapters (84 and 88), explicit "(Studio Version Only)" tags, Fusion 3D OpenGL notes.
110. Blackmagic Design — DaVinci Resolve 21 New Features Guide (PDF, 150 pages, created 2026-04-10) — https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_New_Features_Guide.pdf — downloaded 2026-10-18 — [P] no free/Studio comparison found in the extracted text.
111. Blackmagic Design — support downloads data (undocumented JSON behind the support page) — https://www.blackmagicdesign.com/api/support/us/downloads.json — fetched 2026-10-18 — [P] Resolve 21 to 21.1.1 release dates and notes.
112. Blackmagic Design — techspecs page and support family page — https://www.blackmagicdesign.com/products/davinciresolve/techspecs ; https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion — fetched 2026-10-18 — [P] no Resolve software requirements on either.
113. BrokenSource — DepthFlow repository, commit 32725b7 (2026-10-10): `readme.md`, `pyproject.toml`, `depthflow/*.py`, `website/*.md`, `examples/batch.py` — https://github.com/BrokenSource/DepthFlow — cloned and read 2026-10-18; version 1.0.1 installed and run in the container — [P].
114. PyPI — shaderflow 0.11.3 (wheel downloaded; `main()` options and dependency pins read) — https://pypi.org/project/shaderflow/ — [P].
115. PyPI JSON metadata for DepthFlow's dependencies (wheel lists for glcontext, moderngl, glfw, imgui-bundle, turbopipe, numpy-quaternion, scipy, torch, torchvision, transformers and others) — https://pypi.org/pypi/<package>/json — fetched 2026-10-18 — [V].
116. Hugging Face — depth-anything/Depth-Anything-V2-Small-hf model card — https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf — fetched 2026-10-18 — [P] Apache-2.0, 24.8M parameters.
117. PyPI — dlib 20.0.1 (source only) and dlib-bin 20.0.1.post1 (wheels) JSON — https://pypi.org/pypi/dlib/json ; https://pypi.org/pypi/dlib-bin/json — fetched 2026-10-18 — [V].
118. alesanfra — dlib-wheels (third-party build automation for dlib wheels) — https://github.com/alesanfra/dlib-wheels — fetched 2026-10-18 — [P] not claimed official; Python 3.10 to 3.15.
119. dlib — compiling dlib — https://dlib.net/compile.html — fetched 2026-10-18 — [P] "CMake and a working C++ compiler" for the Python install.
120. davisking — dlib-models README — https://github.com/davisking/dlib-models — fetched 2026-10-18 — [P] 5-point model, 7,198 faces, public domain / CC0-1.0.
121. Google AI Edge — Face Landmarker for Python — https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python ; PyPI mediapipe 1.1.1 JSON — https://pypi.org/pypi/mediapipe/json — fetched 2026-10-18 — [P] 478 landmarks, `pip install mediapipe`, Windows wheel.
122. OpenCV — `FaceDetectorYN` (docstring from OpenCV 5.0.0 installed from PyPI; opencv-python 5.0.0.93 JSON https://pypi.org/pypi/opencv-python/json) ; opencv_zoo YuNet README — https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet — fetched 2026-10-18 — [P] 15-value face rows, MIT licence, default model file. The OpenCV class documentation page returned HTTP 403.
123. storytold — FilmCraft repository, release 0.9.0 (commit 4a69a03, 2026-10-17) — https://github.com/storytold/filmcraft — cloned and read 2026-10-18 — [P].
124. storytold — PhotoCraft repository, `Cargo.toml` 0.10.0, commit 2d0f3b6 (2026-10-17) — https://github.com/storytold/photocraft — cloned and read 2026-10-18 — [P].
125. storytold — VectorCraft repository, release 0.13.1 (commit 904f0fe, 2026-10-18) — https://github.com/storytold/vectorcraft — cloned and read 2026-10-18 — [P].
126. storytold — EffectCraft repository, release 0.12.0 (commit f36b2b3, 2026-10-17) — https://github.com/storytold/effectcraft — cloned and read 2026-10-18 — [P].
127. American Ancestors — scanning (digitising) class handout, PDF modified 2022-01-05, table based on ALCTS Minimum Digitization Capture Recommendations (2013) — https://www.americanancestors.org/sites/default/files/2022-01/scanning%20handout.pdf — fetched 2026-10-18 (text extracted with pdftotext) — [P] flatbed or camera-on-copy-stand; ppi table (this upgrades the snippet-only citation in [96]).
128. Library of Congress, The Signal — Scanning: DIY or Outsource — https://blogs.loc.gov/thesignal/2013/01/scanning-diy-or-outsource/ — 2013-01 — fetched 2026-10-18 — [S] 300 dpi for 4x6 and 5x7; 600 dpi or more for 8x10 and larger (this upgrades the snippet-only citation in [96]).
129. JustWatch (US) — Up https://www.justwatch.com/us/movie/up-2009 ; Flee https://www.justwatch.com/us/movie/flee ; Tower https://www.justwatch.com/us/movie/tower-2016 ; The Missing Picture https://www.justwatch.com/us/movie/the-missing-picture — fetched 2026-10-18 (pages state "checked on October 17, 2026") — [T] aggregator listings; prices change.
130. YouTube — Noah Kalina, "Noah takes a photo of himself every day for 6 years." (same video as [69]) — https://www.youtube.com/watch?v=6B26asyGKDo — page data read 2026-10-18: length 345 s, published 2006-08-27, description with date span and music credit — [V].
131. Wikipedia — Noah Kalina (footnote 15: Gothamist, "Noah Kalina, Photographer", Jen Carlson, 2008-01-09) — https://en.wikipedia.org/wiki/Noah_Kalina — fetched 2026-10-18 — [T]; the Gothamist article itself was not opened. Kalina's site pages checked: https://noahkalina.com ; https://everyday.photo/ ; https://everyday.photo/faq — [P] no rate stated.
132. yU+co — Watchmen title sequence work page — https://www.yuco.com/works/watchmen — fetched 2026-10-18 — [P] "This 6-minute sequence ...".
133. Vimeo oEmbed — "WATCHMEN - MT" by yU+co (the "Main Title" video on [132]) — https://vimeo.com/184379938 — probed 2026-10-18: 335 s, uploaded 2016-09-26, 640x360 — [V].
134. Pat Aufderheide, Peter Jaszi, Mridu Chandra — Honest Truths: Documentary Filmmakers on Ethical Challenges in Their Work (Center for Media and Social Impact, American University) — https://cmsimpact.org/wp-content/uploads/2016/08/Honest-Truths-Documentary_Filmmakers_on_Ethical_Challenges_in_Their_Work-.pdf — 2009-09 — downloaded and read 2026-10-18 — [P] releases, right to change one's mind, do-no-harm, family example, undisclosed stand-in footage.
135. Oral History Association — Statement on Ethics (Principles and Best Practices, 2018; PDF 2025) — https://oralhistory.org/wp-content/uploads/2025/12/2025-OHA-PrinciplesBP_Statement-on-Ethics.pdf — downloaded and read 2026-10-18 — [P] consent, narrator review and approval, delete/restrict/redact options. (Same document as [8] in `surprise-ops.md`.)
136. Doc Society — Philosophy and ethics — https://docsociety.org/philosophy-ethics/ — fetched 2026-10-18 — [P] general ethical statement; no consent process described.
