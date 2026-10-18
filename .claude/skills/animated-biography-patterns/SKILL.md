---
name: animated-biography-patterns
description: Plans, reviews or cuts the visual devices for animated and documentary-style Life Journey scenes, including honest reconstruction of unphotographed moments, photo-to-parallax shots, portrait ladders and morphs, time-passing devices, era cues and title sequences. Use it whenever a chapter needs invented, drawn or animated imagery, when someone proposes a Flee, Tower, Missing Picture, Up or Kid Stays-style device, or when a scene must pass the disclosure, consent, reveal and delivery checks.
---

# Animated Biography Patterns

## Purpose

Make every animated or documentary-style scene in the Life Journey pass charter rule 4 (real memories stay real, and reconstructions are visibly reconstructions) and principle 7 (prefer scriptable, plain-file delivery), while still carrying the feeling. This skill turns `research/animated.md` into a repeatable procedure. The human-readable version is `playbooks/animated.md`.

## When to use

- A chapter needs an invented, drawn, clay or animated image, or a real photograph that will be animated.
- Someone proposes a device like one of the references: Flee's disclosure card, Tower's reveal, The Missing Picture's model, Up's objects, a portrait ladder, a Kid Stays-style layer move, or a life-in-weeks grid.
- A scene needs a time-passing device, an era cue or a title sequence.
- A scene or device is up for review at a gate.

## When not to use

- Gathering or verifying a chapter's facts. That belongs to the story track. Hand off with `TODO(story): <fact>`.
- Choosing the overall format, engine or screening plan. That belongs to the format track.
- Restoring real photographs with AI tools. That belongs to the ai-imagery track. This skill only sets the rules that restoration must respect.
- Interactive game mechanics. Use the `meaningful-game-mechanics` skill.
- Licence questions. Flag them for the maker. Do not answer them as legal advice.
- Writing code. The project is in the LEARN phase, so this skill decides design only.

## Procedure

1. Read `CHARTER.md` and `playbooks/animated.md`. Confirm the phase. In LEARN, use practice material only. Do not open, process or describe family photographs or interview notes. Family material comes in only after the charter's lock.
2. Check consent and proxy status for the chapter. If the chapter touches loss, illness, separation, money or conflict, and no trusted proxy is named, mark it `HOLD: proxy needed` and stop imagery design for that chapter.
3. Write a scene card with these fields: chapter; one sentence, "This scene shows [what], so the viewer feels [what] about her life"; source inventory (each photo, letter, recording or object, with its date and place); what is photographed and what is invented; time-passing device; reconstruction material; motion; duration; disclosure text; reveal target; consent status; citations as [n]; fallback; open items. Write `TODO(story):` or `TODO(research):` in any empty field. Do not guess.
4. If the sentence in step 3 cannot be finished, the scene has no job. Cut it, or return to the story track for a new idea.
5. Choose the time-passing device from the material you have:
   - An object that recurs across years: an object with a clock [56][57].
   - Written messages, letters or search-like notes: an interface timeline, one line per year [49][54].
   - Eight or more portraits across years: a portrait ladder with aligned eyes [70][72].
   - Places but no people: a scale zoom, or a model of the place [6][43].
   - One strong photograph: one long hold, at most once per chapter [37][38].
   - Nothing: show the gap, with a black frame or one object [62].
6. Choose one reconstruction material for the whole piece: cut paper drawn in a vector editor, clay or paper sets photographed, or blocks [6][21]. Record it in an art bible with three good and three not-good examples, plus a rule for hands and faces [1][2]. Do not use photoreal AI faces for real people in invented scenes.
7. Write the disclosure card: one short paragraph, placed at the start, that names which scenes are reconstructed and the material that marks them [1].
8. Write the reveal. For each reconstructed person or place, name the real photograph, voice or object that replaces it, and where it appears. If none is known, write `TODO(story): no real item known` and keep the stand-in labelled [13][16].
9. Set the motion. The default is a still with one slow move of about 3 to 5 percent of frame width, held for 8 to 10 seconds or less [28][29]. Alternate still and moving shots. Use parallax only on photographs that passed the spike (playbook, Exercise 5). Never put the same move on every photo [79]. No whip pans, beat-synced zooms or trending transitions.
10. Set era cues on new material only: title cards, reconstructions and graphics. Use the medium (grain, frame shape, tint, crop) before any colour filter [88][91]. Sample the palette from her own scans of that decade once they exist, and use the decade table only as a sanity check [89]. Do not age material that is already aged. Do not add fake date stamps.
11. Check the audio. A recorded voice exists or is scheduled. The scene works with voice and room sound alone. Dialogue and effects are dropped where the picture carries the feeling [56][58]. Any song has a recorded licence [65].
12. Score the scene against the charter rubric (meaning, specificity, accuracy, feasibility, ethics, craft), 1 to 5 each. Send the scores and open items to the advisor at the gate. Approve only when every score is 4 or higher and nothing critical is open.
13. Set delivery. Export H.264 MP4 at 1080p [78]. Any web version is a self-contained folder with no external scripts, fonts, video hosts or analytics [39][46]. Include a static fallback [100]. Archive masters separately with a rebuild README. Test any web version in a current browser before calling it finished [39].
14. Log every `TODO(research)` item and every unverified claim in the scene card. Never state an unverified fact in the film, the disclosure card or any guide.

## Checklists

### Per scene (before production)

- [ ] Scene card complete, or every empty field marked TODO.
- [ ] The "This scene shows..." sentence is written and says something true.
- [ ] Proxy named if the chapter is a hard one; otherwise the chapter is on HOLD.
- [ ] Disclosure text written and placed at the start.
- [ ] One reconstruction material used for every invented element.
- [ ] Every real event, person and place in the scene has a source in the scene card.
- [ ] No invented speech. No animated face of a dead person.
- [ ] Duration fits the chapter budget.

### Per photo-animation shot

- [ ] Small prints scanned at 600 ppi; slides and film at 2000 to 3000 dpi [96].
- [ ] Move of about 3 to 5 percent of frame width, held 8 to 10 seconds or less.
- [ ] No gaps visible at 1080p after fill.
- [ ] Faces clean at the full push-in. If not, use a flat push or a cut.
- [ ] Grain and dye cast kept, not hidden.
- [ ] Every long move in the chapter is listed in the scene card with a reason.

### Per portrait ladder or morph

- [ ] Eyes on the same position and crop in every frame; no visible jumps at 1080p.
- [ ] Each portrait held one to two seconds (judgment).
- [ ] Whole sequence 20 to 90 seconds, with one idea and a change of rhythm halfway (judgment). TODO(research): the tedium threshold is undocumented.
- [ ] A morph is marked on screen as a morph, and artefacts on faces are checked [77].
- [ ] Default is a hard cut unless the morph earns its place.

### Per era cue

- [ ] Applied to title cards, reconstructions or graphics only.
- [ ] Medium cue used (grain, frame shape, tint), not only a stacked grade.
- [ ] Palette taken from her own scans of that era; the decade table is only a check.
- [ ] Music used only with a recorded licence.

### Delivery

- [ ] Plain H.264 MP4 at 1080p exists.
- [ ] Any web build loads everything from its own folder.
- [ ] Static fallback exists.
- [ ] Tested in a current browser, or a TODO(research) is recorded.
- [ ] Masters and the rebuild README are archived.

## Quality bar

Ask one question: could a viewer name what the scene is about, and tell which parts are real? A good scene passes. Use this table to check.

| Good | Mediocre |
|---|---|
| The invented part looks drawn or built, is disclosed once, and is answered by a real item later | Drawn or generated faces that could pass for photographs, with no disclosure |
| One idea per shot, slow and purposeful | The same move on every photo, whip pans, beat-synced zooms |
| Time passes through objects, voice or written words | Dates as captions over a stock montage |
| Specific: her kitchen, car, songs, sayings | Generic retro: avocado, Cooper Black, grain stacked on every frame |
| Sparse years look sparse | Every year filled with invented imagery |
| Sound and dialogue dropped where the picture speaks | A swelling score doing the emotional work |
| A plain video master plus a self-contained build | Hosted embeds, external script dependencies, interactives that need a runtime |

Any "mediocre" entry in the first two rows is a critical open item at the gate.

## Ethics guardrails

- Charter rule 4: no invented events, people or words. Reconstructions are visibly reconstructions.
- Charter rule 5: a trusted proxy decides for hard chapters. Anything she might not want shown in front of others stays out of the shared version.
- Never animate a dead person's face, and never invent speech. Until AI face-animation tools are researched (TODO(research)), do not use them on any real person's face.
- AI restoration must not invent facial detail. If a scan is faded or soft, say so on screen [89][93].
- Never leave a reconstruction unlabelled, even when it looks like archive. Stories We Tell shows how convincing an unlabelled fake can be, and how it divides audiences [66][67].
- Never select photographs automatically by popularity, recency or detected faces. Select by hand, with the proxy's input [81][82].
- Surprise rules: keep working files off shared devices, family group chats and auto-syncing photo libraries (charter).
- Licences: no song goes into a scene without a recorded licence. A private gift carries less risk than a public showing [65][78].
- Privacy is a longevity feature. A public URL outlives consent, so default to private [45].

## References

- Playbook: `playbooks/animated.md`
- Research notes: `research/animated.md` (questions Q1 to Q11; sources 1 to 105)
- Charter: `CHARTER.md`

Sources cited in this skill (numbers match the notes and the playbook):

- [1] Hyperallergic — How a Documentary Used Animation to Protect the Identity of Its Main Character (Flee interview) — https://hyperallergic.com/697967/jonas-poher-rasmussen-interview-flee/ — undated — [S] fetched: art bible, title card, Amin reviewed edit.
- [2] Seventh Row — Flee interview — https://seventh-row.com/?p=45371 — undated — [S] fetched: archive sources, Hopper/Metzler/Gronsky references, closed-eyes interviews, ~50 animators.
- [6] MPR News — Cambodia's 'missing pictures' molded from director's own life — https://www.mprnews.org/story/2014/03/30/cambodias-missing-pictures-molded-from-directors-own-life — 2014-03-30 — [S] fetched: paper lilies, thinning figures, composer detail.
- [13] Documentary.org — Life Animated: how doc makers heighten perception through animation — https://documentary.org/feature/life-animated-how-doc-makers-heighten-perception-and-solve-problems-through-animation — undated — [S] fetched: Tower additive layer, TVPaint, actress-to-real-Claire.
- [16] Wikipedia — Waltz with Bashir — https://en.wikipedia.org/wiki/Waltz_with_Bashir — accessed 2026-10-18 — [T] fetched: Flash cut-outs, ending dissolve into news footage, structure.
- [21] Bostonia (Boston University) — From Sketch to Screen (Rocks in My Pockets) — https://www.bu.edu/bostonia/2016/from-sketch-to-screen/ — 2016 — [S] fetched: papier-mâché sets, 30,000 drawings, Photoshop/After Effects.
- [28] PictureCorrect — Parallax Animation: Bringing Still Photographs to Life — https://www.picturecorrect.com/parallax-animation-bringing-still-photographs-to-life/ — undated — [S] fetched: Fellows' workflow.
- [29] Motion Array — Animate flat 2D images in After Effects (2.5D parallax) — https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/ — undated — [S] fetched: content-aware fill, 28mm camera, Puppet tool.
- [37] Poynter — Meaning in Motion: Ken Burns and His 'Effect' — https://www.poynter.org/news/meaning-motion-ken-burns-and-his-effect — undated — [S] fetched: "mindless, anxious movement," "all real meaning accrues in duration."
- [38] CineD — Ken Burns effect article — https://www.cined.com/?p=406363 — undated — [S] fetched (partial): 33-second Roebling zoom.
- [39] The New York Times — Snow Fall — https://www.nytimes.com/projects/2012/snow-fall/index.html — [V] 2026-10-18: HTTP 200, 177,243 bytes; own CSS, jQuery 1.7.1 and 30+ MP4/WebM assets 200; Brightcove script 301.
- [43] Wait But Why — Your Life in Weeks (Tim Urban) — https://waitbutwhy.com/2014/05/life-weeks.html — 2014-05-07 — [P][V] fetched, HTTP 200.
- [45] werd.io — Life in Weeks — https://werd.io/life-in-weeks/ — undated — [P] fetched: author built it, did not publish; blog author not named on the fetched page.
- [46] eagereyes (Robert Kosara) — The bits are rotting in the state of data journalism — https://eagereyes.org/blog/2016/the-bits-are-rotting-in-the-state-of-data-journalism — 2016-07-14 — [S] fetched.
- [49] Adweek — Google Chrome Spot Captures Girl's Entire Life in 90 Seconds — https://www.adweek.com/?p=131368 — 2011 — [S] fetched: credits, true-story-with-actors.
- [54] UMass Dartmouth Corridors — John Michael Bell, Analysis of Google's 'Parisian Love' — https://corridors.sites.umassd.edu/?p=213 — undated — [S] fetched: 11-query sequence, 52 s.
- [56] The Ringer — Up's first 10 minutes, making of — https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of — 2022-06-14 — [S] fetched: beats, ~4.5 min, 30-40 minutes cut, dialogue removed.
- [57] Wikipedia — Up opening sequence — https://en.wikipedia.org/wiki/Up_opening_sequence — accessed 2026-10-18 — [T] fetched: jar, ties, reception.
- [58] /Film — Up opening, multiple last-minute changes — https://slashfilm.com/1582050/up-opening-emotionally-devastating-pixar-multiple-last-minute-changes-exclusive — undated — [S] fetched.
- [62] Alphaville — Kathleen Williams on The Wonder Years credits — https://www.alphavillejournal.com/Issue12/HTML/ArticleWilliams.html — undated — [S] fetched: home-video markers, refreshed footage, generic action.
- [65] Independent magazine — Mind the Gap (Tarnation) — https://independent-magazine.org/2004/10/01/mind-gap/ — 2004-10-01 — [S] fetched: iMovie, $218.32, ~$400,000 clearance, cutting around the beat.
- [66] Documentary.org — Sarah Polley on Stories We Tell — https://documentary.org/node/33754 — undated — [P] fetched.
- [67] The A.V. Club — Stories We Tell — https://www.avclub.com/stories-we-tell-1798176746 — [T] snippet only.
- [70] Wikipedia — Noah Kalina — https://en.wikipedia.org/wiki/Noah_Kalina — accessed 2026-10-18 — [T] fetched: six per second, piano score, Coolpix S10 since 2008.
- [72] kottke.org — Half a Life in 2 Minutes — https://kottke.org/21/07/half-a-life-in-2-minutes — 2021-07 — [S] fetched: dlib, landmarks, 4K, Paul O'Mara.
- [77] vladmandic/rife — https://github.com/vladmandic/rife ; dlib face_alignment — https://dlib.net/face_alignment.py.html — [T] snippets only.
- [78] Parting Stone — How to Make a Slideshow for a Funeral — https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/ — undated — [S] fetched: length, timing, licensing, export.
- [79] funeralOne — 22 Tips For Creating Tribute Videos — https://blog.funeralone.com/funeralone-products/life-tributes/tribute-video-tips/ — 2013-09-12 — [S] fetched: 25-30 photos, vary effects; vendor blog.
- [81] meyerweb (Eric Meyer) — Inadvertent Algorithmic Cruelty — https://meyerweb.com/eric/thoughts/2014/12/24/inadvertent-algorithmic-cruelty/ — 2014-12-24 — [P] fetched.
- [82] Engadget — Facebook's 'Year In Review' shows tragic side of software's shortcomings — https://www.engadget.com/2014-12-27-facebooks-year-in-review-shows-tragic-side-of-software.html — 2014-12-27 — [T] snippet only.
- [88] No Film School — How to get the Super 8 film look — https://nofilmschool.com/get-super-8-film-look — [S] fetched.
- [89] AIC (Wallace) — Topics in Photographic Preservation 1989, Vol 3, Art 17 — https://resources.culturalheritage.org/pmgtopics/1989-volume-three/03_17_Wallace.html — 1989 — [P] fetched: dye loss, restoration.
- [91] Wikipedia — Super 8 film — https://en.wikipedia.org/wiki/Super_8_film — accessed 2026-10-18 — [T] fetched.
- [93] Wikipedia — 110 film — https://en.wikipedia.org/wiki/110_film — accessed 2026-10-18 — [T] fetched.
- [96] American Ancestors — scanning handout — https://www.americanancestors.org/sites/default/files/2022-01/scanning%20handout.pdf ; Library of Congress Signal — https://blogs.loc.gov/thesignal/2013/01/scanning-diy-or-outsource/ — [T] snippets only.
- [100] University of Mary Washington DKC — Building a Scrollytelling Website — https://dkc.umw.edu/tools/building-a-scrollytelling-website/ — undated — [S] fetched: static fallback.
