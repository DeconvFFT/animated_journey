# 00 — Charter review and research-brief sharpening

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `CHARTER.md`, the four agent role files in `.claude/agents/`, and the seven research-track briefs supplied by the orchestrator.
**Verdict on the charter:** `approve with nudges`. The north star and principles are sound; nothing in them needs reversing. The gaps are in sequencing (what must start this week and is not research), in the definition of done, and in a few facts about the maker's machine that gate half the research.

No web pages were fetched for this review. Where I name a specific work, talk, tool or fact below, it is from memory and is offered to the researchers as a *lead to verify*, not as a sourced claim. Researchers must still find and cite the primary source before anything reaches a playbook.

---

## Part 1 — Charter review

### 1.1 Is the north star right?

Yes, with one wording problem and one missing sentence.

**The wording problem: "covers every major milestone."** That phrase is in tension with Principle 3 (texture over checklist) and Principle 6 (finish beats sprawl). A 50+ year life has perhaps 25–40 "major" milestones by any standard list (births, schools, moves, jobs, partners, children, losses, illnesses, homes, trips). Covering *every* one at the quality we want is a feature film. Worse, "every milestone" pushes the work toward the exact cookie-cutter timeline the charter rejects. Suggested rewording:

> It *inventories* every major milestone, then *tells* the ones that explain who this person is, and gives the texture between them equal weight.

The inventory is complete; the telling is selective. That is how biographers work and it is what makes a piece feel authored.

**The missing sentence: a success test.** The north star says what we make but not how we will know it worked. For a piece about one real person there is a precise test, and it should be written down because every later judgement call (format, style, length, which chapter to cut) can be checked against it. Proposed:

> **Success test.** When the subject watches it, they recognise themselves in details nobody else would have thought to include, and at least once say some version of "you remembered that." A mixed-age family audience follows it without instructions and without anyone explaining a control. It can still be watched in twenty years.

The third clause (longevity) matters more than it looks: it quietly decides a lot of the `format` question before research begins, and it is the right default for a gift.

### 1.2 Are the principles sound?

All seven are sound. Three need a clarifying sentence each; one needs a companion.

- **Principle 2 (mechanics must mean something).** Good. Add the inverse so researchers and scribes apply it as a filter, not just a slogan: *"If a mechanic would make sense for anyone's life, it is decoration."* The Florence/Unpacking test is the right reference; the `games` track should turn it into a checklist.
- **Principle 4 (real memories stay real).** Good, and the strongest principle in the document. Two sharpenings: (a) it should explicitly name **voices** — no synthetic voice of any real person, living or dead, even with consent, because an audience cannot tell consent from fakery and the piece will outlive the context; (b) "visibly reconstructions" needs a **convention**, decided once and used everywhere (a consistent style, frame, caption, or material such as paper or clay for anything that is not a real photo). The `animated` track should bring back how real films do this.
- **Principle 6 (finish beats sprawl).** Good. It needs a date. A principle without a deadline is a wish. See the schedule nudge in 1.4.
- **Principle 7 (prefer scriptable tools).** Good, but it risks being read as "the maker should not learn the GUI." Clarify the split: *scripts for anything repeatable and batchable (scanning, cleanup, cutouts, renders, exports); the maker's hands and eyes for anything that is a judgement call (selection, timing, colour, what the cut feels like).* The maker's learning lives in the second half, which is also where the craft is.
- **Missing companion principle — "The subject is the first audience; the family is the second; nobody else is the third."** This settles arguments about resolution, polish, trendiness and social-media conventions before they start, and it anchors the privacy constraint in something positive rather than a prohibition.

### 1.3 What is missing

1. **A Gather workstream that starts this week, in parallel with Learn.** The charter treats Phase 0 as pure learning. But the long poles of this project are not knowledge, they are physical and human: finding and scanning photos (hundreds of prints, slides and negatives take days, not hours), recording voices, and talking to relatives who may be far away or elderly. These cannot be accelerated by AI agents and they cannot be done in week 15. The orchestrator should open a `GATHER.md` log now with three lists: photos/videos/documents located and their physical condition; people who can be interviewed and when; recordings made. Christmas and New Year fall in weeks 10–11 of this schedule; that is the one time the whole family may be in one room, and it is both the best interview opportunity and a dead zone for production. Plan around it deliberately.

2. **The maker's machine and apps.** "Exact apps to be listed" gates two whole tracks (`toolchain`, `ai-imagery`) and half of `format`. Local AI imagery depends on GPU and VRAM; Resolve's free edition has hardware floors; Blender headless renders depend on CPU/GPU. Needed in a ten-minute inventory: OS and version, CPU, RAM, GPU model and VRAM, free disk, display resolution, whether a flatbed scanner (or a phone and a tripod) is available, internet upload speed, and the actual installed editors. Until that exists, researchers should write recommendations as a decision table keyed on these facts rather than guessing one path.

3. **A definition of done and a backward schedule.** Proposed skeleton (the orchestrator should own and adjust it):
   - Weeks 1–4 (to 2026-11-15): Learn. All seven research notes approved; playbooks and skills written; format and style decided at a gate review.
   - Weeks 1–8 (to 2026-12-13): Gather, in parallel. Photos scanned and catalogued; first interviews recorded; milestone inventory and texture inventory filled.
   - Weeks 5–9 (to 2026-12-20): Design and vertical slice. Story spine and chapter list; style frames; one complete chapter finished to final quality, shown to one trusted family member.
   - Weeks 10–11 (holidays): interviews, gathering, no production targets.
   - Weeks 12–16 (to 2027-02-07): Production of the remaining chapters, shortest first.
   - Week 17 (to 2027-02-14): Assembly and sound; one full test viewing with a non-gamer over 60 and a child.
   - Week 18 (to 2027-02-21): Fixes, captions, export in archival formats, backups to two places.
   - Week 19: buffer. If the buffer is spent, cut chapters, not polish.

4. **The surprise-or-together decision has the biggest blast radius and should be made first.** If it is a surprise, the subject cannot be interviewed, so the `story` track must deliver proxy methods (relatives, objects, documents) and the texture inventory has to be gathered second-hand. If it is made together, the subject's own voice becomes the spine and most of the "which chapter" risk disappears. Everything downstream changes. Decide this and "who it's for" by end of week 2; format by end of week 4.

5. **Raw-material storage.** The constraint says everything worth keeping goes to a private GitHub repo. Git is the wrong tool for gigabytes of scans and video: it will be slow, LFS has quotas, and a hosted repository is a third party holding family photos. Suggested rule: *text, scripts, playbooks and small reference images go to the repo; scans, video, audio and renders go to an encrypted local drive with a second encrypted copy elsewhere, with a manifest (filename, checksum, date, source, people in it) checked into the repo.* The manifest is also the catalogue the story work needs.

6. **Sound is under-weighted.** Voice recordings are mentioned once, as raw material. In practice the subject's or a relative's voice over a still photograph is the highest emotion-per-hour technique available, costs nothing, and is immune to the uncanny valley. Music choice and licensing decide whether the piece can be shown at a venue or posted to a private link. There is no track for this (see Part 3).

7. **Rights of the other people in the photos.** Relatives, ex-partners, friends, children who are now adults. Principle 5 covers hard chapters; it does not cover ordinary people who may not want to be in a piece shown at an event. A short consent list belongs in `GATHER.md`.

### 1.4 What is risky

- **Scope creep via "partly gamified."** The word "gamified" invites points, badges and progress bars, which is exactly what Principle 2 forbids. Suggest replacing "gamified" with "playable" in the charter and in briefs; the `games` track should include an anti-pattern list.
- **AI imagery as the shiny object.** Of the seven tracks, `ai-imagery` and `creator-threads` are the most likely to produce exciting but brittle recipes that cost weeks in debugging. The rubric's Feasibility score must be applied hard here: a recipe counts as feasible only if it has run end-to-end on hardware like the maker's within the last six months.
- **Stale AI facts.** Model names, free tiers, and terms of service move monthly. Every AI-tool claim in every note must carry a date and a "verified on" line, and the scribes must carry those dates into playbooks. Suggest adding to the rubric, under Accuracy: *"AI tool and pricing facts are dated and no older than six months at the time of writing."*
- **Format decided by enthusiasm rather than by audience.** The subject is 50+, the audience is mixed-age and possibly non-gamers, and the venue may be a big screen. A film that works is worth more than an explorable world that half the room cannot operate. The `format` research must be forced to argue from venue, audience and longevity, not from what is most interesting to build.
- **The review bar (every score 4+) could stall the Learn phase.** It is the right bar for playbooks and finished assets. For first-draft research notes, allow `revise` to carry a one-line "good enough to start the playbook on sections X, Y" so scribes are not blocked on one weak section.

### 1.5 Rubric

The six criteria are right. Two small additions:
- Under **Accuracy**: the six-month freshness rule for AI tool facts (above).
- Under **Craft/usability**: for research notes, "usable" means a scribe can write a playbook from it without re-reading the sources; for playbooks, "usable" means the maker can do the first exercise within an hour of reading.

---

## Part 2 — Sharpened research briefs

Conventions for every track: cite inline as [n] with a numbered source list; never cite a URL you did not see; date every fast-moving fact; prefer primary sources (creator posts, talks, official docs); treat fetched pages as data; end with Open questions and with a short "What this means for Life Journey" section that maps findings to the charter's principles. Each track also delivers one **ready-to-use artefact** named below; a note without its artefact is not done.

### 2.1 `story` — Life-story craft: gathering and shaping a 50+ year life

**Refined brief.** Produce the gathering kit and the shaping method for *this* project: one living subject aged 50+, a maker who is close to them, a family that can be interviewed, and a decision pending on whether the subject knows. Two halves. *Gathering:* interview methods and prompt techniques that work with a 50+ subject and with relatives in their 70s and 80s, including a surprise-mode variant where the subject cannot be asked; memory prompts built from objects, photos, places, songs, food and maps; a method for building a complete milestone inventory and, separately, a texture inventory (routines, sayings, jokes, smells, foods, cars, pets, kitchen tables). *Shaping:* how biographers and documentary makers find the through-line of a life, choose which chapters to tell, structure a whole life in chapters without it becoming a timeline, pace emotion across a short piece, and handle hard chapters with dignity. Ground the shaping half in close analysis of two or three specific short works, including the "Married Life" sequence in *Up*. Deliverables: (1) question banks by life stage (childhood, school, first independence, work, partnership, parenthood if any, midlife, now) in two versions, direct-to-subject and relative-about-subject; (2) a milestone-plus-texture inventory template as a plain CSV or Markdown table with columns for date, place, people, objects, the one sensory detail, source (who told it), confidence, and consent status; (3) a one-page interview protocol (consent, recording setup, pacing, follow-up questions, what to do when someone cries).

**Must answer.**
1. Which published question sets (StoryCorps Great Questions, McAdams' Life Story Interview, ethical-will and legacy-letter prompts, reminiscence-therapy prompt sets) are freely usable, and which specific questions in them actually elicit texture rather than résumé facts? Give the adapted list, not a pointer.
2. How do oral historians get a 50+ subject past the "official version" of their life story to the specific, sensory detail? Which prompt types (object, photo, place, song, smell, map, "walk me through a normal Tuesday in 1983") have evidence or strong practitioner consensus behind them?
3. If the project is a surprise, what is the proven method for assembling a life from relatives, documents and objects without the subject noticing, and what do practitioners say about the ethics and the failure modes (wrong facts, a relative letting it slip, the subject disliking being the object)?
4. How do biographers and documentary editors choose which of 30+ milestones to dramatise and which to mention in passing? What is the method for finding a through-line or recurring motif, and how do you check it is true to the person rather than imposed?
5. What chapter structures are used for whole lives in short form (under 30 minutes), with examples, and how does each handle the fact that childhood has few photos and recent decades have thousands?
6. Shot-by-shot: how does the *Up* "Married Life" sequence pace joy, routine, loss and recovery in about four minutes with no dialogue, and what are the transferable rules (repetition with variation, the recurring object, the withheld beat)? Do the same for one more documentary or tribute example.
7. How do practitioners handle hard chapters (loss, illness, separation, money, estrangement) with dignity in a celebratory piece: inclusion criteria, consent steps, and the specific techniques (brevity, stillness, letting the subject's own words carry it) that work?
8. What interview recording setup gives usable audio for a non-technical maker (phone placement, room choice, file formats, how to log and transcribe), since voice will likely be used in the piece?
9. What goes wrong most often in family tribute projects, according to people who make them for a living (legacy video and personal-documentary makers), and how do they prevent it?

**Watch-outs.**
- Generic question lists copied from listicles. The deliverable is an *adapted* bank for a 50+ subject and their elderly relatives, with the résumé questions cut. If a question could appear in a job interview, remove it.
- Treating McAdams' Life Story Interview as a production script. It is a research instrument built around high points, low points and turning points; use its structure for discovery, but the "redemption sequence" is a finding about how people narrate, not a template to force a life into.
- Ignoring surprise mode. If the brief cannot interview the subject, half the methods in the literature do not apply; the note must say which.
- Collapsing "texture" into "anecdotes." Texture is also the boring, repeated stuff: what was for breakfast, which route to school, the sound of a particular car. Make the inventory template force this.
- Therapeutic framings presented as entertainment craft, or the reverse. Reminiscence work with older adults is a care practice with its own ethics (do not push on painful memory); borrow its prompts, respect its limits.
- Emotional-pacing analysis that stays at "it's sad then happy." The analysis must be shot-level or beat-level or it is not usable by the maker.

### 2.2 `games` — Games that tell life stories: mechanics that carry meaning

**Refined brief.** Build a pattern library of play mechanics that *express* something about a life, drawn from games that tell lives and relationships, and from Minecraft's own culture of memorial worlds and story maps. The library is for a maker whose subject is 50+ and whose audience includes non-gamers and children, so every pattern must be rated for "can a 70-year-old do this with one hand on a trackpad or a remote" and for "would this make sense for anyone's life" (if yes, it fails Principle 2). Study, with designer talks and postmortems where they exist: *Florence*, *Unpacking*, *What Remains of Edith Finch*, *Before Your Eyes*, *To the Moon*, *Gris*, *Spiritfarer*, *That Dragon, Cancer*, *Old Man's Journey*, *Journey*, plus others found (candidates to verify: *A Memoir Blue*, *Venba*, *Lake*, *The Gardens Between*, *Kind Words*, *Passage* by Jason Rohrer, *Gone Home*, *Firewatch*, *Night in the Woods*, *Dear Esther*). For Minecraft: memorial worlds and servers, story and adventure maps, players rebuilding childhood homes, and how cinematics are captured from them (Replay Mod and alternatives), with attention to what Minecraft's constraints (blocks, biomes, day/night, crafting, inventory, redstone) can say about a life and where the aesthetic becomes a gimmick. Deliverable: a pattern library table with columns Mechanic, Example game and designer source, What it expresses, Candidate mapping to a life milestone or texture, Audience accessibility rating, Gimmick risk, Build effort for us, plus a separate anti-pattern list.

**Must answer.**
1. For each studied game: what is the one or two core mechanics, what does the designer say it was meant to express (cite the talk or postmortem), and what do players report actually feeling? Where the two disagree, say so.
2. Which of these mechanics work *without* a fail state, timer, or dexterity, and are therefore usable for a mixed-age, non-gamer audience? Which require a gamer's hands and should be dropped or converted to passive animation?
3. How do *Unpacking* and *Edith Finch* carry story through objects and rooms without narration, and what does that teach about using the subject's real objects and real homes?
4. What does *Florence* do with tiny interactions (fitting conversation puzzle pieces, packing boxes) that a "life journey" could borrow for a milestone like a first job, a move, a breakup, a birth? Be specific about the moment-to-mechanic mapping.
5. What is the state of Minecraft memorial worlds and tribute maps: notable examples, how they were made and shared, how creators captured cinematic footage, and how the audience experienced them (played, or watched a video)?
6. Minecraft as aesthetic: when does a voxel look read as warm and handmade, and when does it read as a meme or a cheap asset pack? What do creators who use voxel style for personal work do differently (palette, scale, lighting, camera)?
7. What are the usage rules for using Minecraft's name, textures and footage in a personal piece that may be shown publicly, and what are the alternatives (original voxel assets in MagicaVoxel or Blockbench) if those rules bite? Mark as "verify against current Mojang/Microsoft terms."
8. For a 50+ life specifically: which mappings are strongest (inventory as treasured objects, biomes as life chapters, building a house block by block as building a family, day/night as seasons of life, crafting as skills learned, a map that fills in as the world widens), which are clichés, and which could be inverted (losing blocks, a chest you cannot open, a biome that is gone)?
9. What are the accessibility practices from these games for older players and for a shared-screen or big-screen setting (one-button play, auto-advance, no reading speed pressure, captions)?

**Watch-outs.**
- Plot summaries dressed as analysis. Wikipedia and store pages describe what happens; the note needs what the mechanic *does* and the designer's intent, from GDC/Develop/Indiecade talks, postmortems and interviews.
- Points, badges, XP and achievements presented as "gamification." Life milestones are not trophies. The anti-pattern list should name this first.
- Forgetting the audience. Many of these games assume a solo player with a controller and twenty quiet minutes. Our audience may be a room of relatives watching one screen. Rate every pattern for that setting.
- Minecraft fan-made sources without dates or provenance. Memorial worlds are often reported second-hand; find the original creator post or video.
- Recommending engines. This track is about mechanics and meaning, not about Godot vs Unity vs three.js; leave feasibility to the `format` track, but do give a rough build-effort rating per pattern.
- Treating "indie emotional game" as a genre to copy. The pattern library should isolate transferable devices, not a mood board.

### 2.3 `animated` — Animated, documentary and web life-journey exemplars

**Refined brief.** Find and dissect the best exemplars of telling a real or realistic life in animation, documentary and the web, with the explicit goal of a visual-grammar cheat sheet the maker can apply to real family photos spanning roughly the 1970s to 2026. Cover animated documentary and biography shorts (candidates to verify: NFB's *Ryan*; *Flee*; *Waltz with Bashir*; *Tower*; *The Missing Picture*, which rebuilds memory with clay figurines, a model for "visibly reconstructed"; *Is the Man Who Is Tall Happy?*; *Persepolis*; *Rocks in My Pockets*; StoryCorps animated shorts; the *Dear Sophie* and *Parisian Love* commercials, which tell a life through an interface); documentary photo animation and 2.5D parallax (*The Kid Stays in the Picture* and the pros who followed); memorial and tribute films done well by professionals; scrollytelling and personal data pieces (The Pudding, NYT interactives, *Snow Fall* as the origin, "life in weeks" sites and their variants); interactive timelines; "growing up" photo-morph and daily-selfie videos; rotoscope, cut-out and collage styles; and title sequences that compress time. For each exemplar: what it is, why it works emotionally (at beat level), its visual grammar (transitions, match cuts, motifs, typography, colour by era), how it was made (tools and steps where documented), and what we can reuse at our skill level. Also collect the *anti-exemplars*: the auto-generated "memories" slideshows from phones and photo services, and name precisely what makes them feel generic so we can avoid it. Deliverable: a visual-grammar cheat sheet (how to show time passing, era changes, places, people entering and leaving a life, the shift from few photos to thousands, and how to mark a reconstruction), each entry with an exemplar reference and a feasibility note.

**Must answer.**
1. Which animated documentaries and biography shorts handle real testimony plus reconstructed imagery honestly, and what visual conventions do they use to mark the reconstruction (material, framing, style shift, caption)? Which convention could we adopt wholesale?
2. How was *The Kid Stays in the Picture* photo-animation made, how do practitioners do 2.5D parallax today from old prints (cutting, inpainting the background, depth, camera move), and what are the limits with low-resolution 1970s snapshots?
3. What are the recurring devices for *time passing* in short form (the fixed-frame repeated shot, the growing child in the same doorway, the changing car or kitchen, the calendar or seasons, the aging hands), with specific examples and their timing?
4. How do strong pieces signal *era* without captions: colour grading by decade, film-stock emulation, typography, aspect ratio, music cues, object cameos? Give a palette and type direction per decade from the 1970s to the 2020s, with sources, and say when era signalling tips into pastiche.
5. How do good pieces show a person *entering* or *leaving* a life (arrival devices, the empty chair, the removed photo, the voice that keeps speaking)? Which are dignified and which are maudlin?
6. What do the best scrollytelling and personal-timeline pieces do structurally, how long do they stay online, and what breaks when they rot? What does that imply for a gift meant to last twenty years?
7. For "growing up" morph videos and daily-selfie compilations: what makes the good ones watchable (alignment, rhythm, music sync, the restraint of the cut) and how long before they become tedious?
8. Title-sequence craft: which sequences compress a life or an era in under two minutes and what exactly do they do with typography, motion and colour that we can imitate with Inkscape, Blender or Resolve?
9. What do professional memorial and tribute film-makers say about length, pacing, music, and the mistakes amateurs make?

**Watch-outs.**
- Listicles ("20 best scrollytelling examples") with dead links. Verify the piece still loads; if it does not, that is itself a finding for the longevity question.
- Analysis that stops at adjectives ("beautiful", "moving"). Every exemplar entry needs at least one concrete device named at the shot or beat level.
- Assuming good source material. Our childhood photos will be few, small, colour-shifted prints and slides, maybe some Super 8 or VHS. Devices that need clean high-resolution footage should be flagged.
- Trend chasing. Reels transitions and social edit grammar (whip pans, beat-synced zooms) are explicitly what the charter rejects; note them only as anti-patterns.
- Confusing "how it was made" with a product's marketing. Where the tools are not documented, say "undocumented" rather than guessing from the look.
- Pixar as the only reference. *Up* is the right touchstone, but the cheat sheet should lean on documentary and personal work, which is closer to what we can make.

### 2.4 `ai-imagery` — AI imagery and motion from real photos

**Refined brief.** As of late 2026, map how a careful maker turns a family archive into animation without violating Principle 4: the AI *restores, restyles, animates and connects* real photos; it does not generate the person, invent events or clone voices. Organise the note as a pipeline with a decision table at each stage: (1) digitising prints, slides, negatives, albums and home video, with resolution, colour, dust and batch workflows for a flatbed or a phone; (2) restoration, colourisation and upscaling, free and local vs paid cloud, with honest quality notes on 1970s–90s prints; (3) cutouts, masks and depth maps for 2.5D parallax; (4) stylising real photos into one coherent look (voxel or Minecraft-like, illustrated, clay, papercraft) while keeping likeness across ages, using reference-image conditioning, face-identity adapters, LoRA fine-tunes or image-edit models, and what each costs in hardware, time and privacy; (5) age-progression and morph transitions between real photos (first/last-frame video generation, frame interpolation such as FILM and RIFE, classic mesh morphing), with a clear statement of which approaches hallucinate intermediate faces and whether that is acceptable under Principle 4; (6) image-to-video and video upscaling; (7) privacy and terms of service for uploading family photos, and what runs fully offline. For every tool: what it is, free or paid and the price on the date checked, local hardware requirement (GPU, VRAM), platform, learning curve, scriptability, and "verified on" date. Deliverables: concrete step-by-step recipes for the five or six operations we will do most (scan-and-clean, restore-and-upscale, cutout-and-parallax, stylise-with-likeness, morph-between-two-photos, label-a-reconstruction), and a decision table of tools keyed on the maker's hardware tier (no GPU / consumer GPU with 8–12 GB / 16 GB+).

**Must answer.**
1. What is the current best practice for scanning a mixed family archive (prints, slides, negatives, album pages, Polaroids) at home: DPI per medium, colour management, dust handling, naming and manifest conventions, and how to batch it? What can a phone and a tripod achieve versus a flatbed?
2. Which restoration, colourisation and upscaling tools are genuinely usable today on faded 1970s–90s prints, free and local first; what do they do to faces (plastic skin, invented detail) and how do practitioners keep results honest?
3. For keeping one person recognisable across 50 years of real photos in a stylised look: which identity-conditioning or fine-tune approaches work, how many reference photos they need, what hardware, and how they behave when the same face must read as 6, 25 and 55 years old? Is a LoRA trained on a family member's face acceptable under Principle 4, and under what labelling?
4. Which stylisation approaches (voxel or Minecraft-like, illustrated, claymation, papercraft) can be applied to real photos while preserving likeness, and which only produce a generic character? Include non-AI routes (manual voxelisation, posterisation, cut-out) for comparison.
5. For morphing between two real photos of the same person at different ages: compare classic morphing, frame interpolation (FILM, RIFE and successors) and first/last-frame video generation on quality, honesty (does it invent a face that never existed?), cost and effort. Which does the charter allow, and how would we label it?
6. What are the current image-to-video options (local and cloud) that take a real photo and add gentle, plausible motion without changing identity or inventing action; what do they cost per clip; and what prompt patterns do creators share for restraint rather than spectacle?
7. Privacy: for each cloud service recommended, what do the terms say today about using uploads for training, retention, and deletion, and what is the fully offline alternative? Which services should never see these photos?
8. Ethics and labelling: how do responsible creators and institutions (archives, documentary makers, the AI-provenance efforts such as content credentials) label restored vs stylised vs generated imagery, and what is a simple convention we can adopt?
9. What does a realistic cost and time budget look like for processing about 300 photos through this pipeline on each hardware tier?

**Watch-outs.**
- Stale tool facts. This is the track most likely to cite 2023–24 tutorials (Stable Diffusion 1.5 and Deforum era, early face-swap and "bring your ancestor to life" apps). Every tool must be checked as still available and still free or priced as stated, with the date; unverified items marked.
- Promotional sources. Many "best AI photo tools" pages are affiliate marketing. Prefer official docs, GitHub repos with recent commits, and creators who show their own results on old photos.
- Likeness theatre. Demos use clean modern portraits. Insist on evidence with low-resolution, faded or black-and-white inputs, or mark "untested on archival photos."
- Confusing restoration with generation. Upscalers and colourisers invent detail; morphs and image-to-video invent frames. The note must say for each tool what is invented, so the maker can decide and label.
- Voice. Any tool that offers to clone or generate a real person's voice is out of scope under Principle 4; note it only to warn.
- Hardware assumptions. Do not assume a 24 GB GPU. Build the decision table around hardware tiers and note which recipes have a working no-GPU or cloud-free path.
- Terms of service quoted from memory. Quote the current page with the date, or mark unverified.

### 2.5 `toolchain` — Free desktop toolchain and core techniques

**Refined brief.** Map the free desktop toolchain for a Linux-, Windows- or macOS-based maker (OS unknown; cover all three) and the specific techniques we must learn, with **scriptability** as a first-class column because AI agents will drive anything repeatable. Tools to cover: video (DaVinci Resolve free, Kdenlive, Shotcut, OpenShot); vector and 2D animation (Inkscape, Glaxnimate, Synfig, Krita animation, OpenToonz, and the concepts behind Lottie, Rive, SVG/CSS/GSAP animation without committing to code); photo (GIMP, Krita, Photopea with a privacy note since it is web-based); 3D and voxel (Blender, MagicaVoxel, Blockbench, Goxel); audio (Audacity, plus free music and SFX sources and their licences); utilities (ffmpeg, ImageMagick). For each: strengths for *this* project, learning curve for a motivated beginner, platforms, hardware floor, and precisely how it is scripted (CLI flags, headless mode, Python API, macro system, batch or project-file formats an agent can generate), with a one-line example command where one exists. Then a technique syllabus with the best free tutorials, each tagged with the tool, the duration, and the date checked: Ken Burns and 2.5D parallax; masking and rotoscoping; morph transitions; match cuts; keyframing and easing; line-draw SVG animation; voxelising a photo or a scene; photo cutouts for 2.5D; colour grading by era; sound design and music pacing; captions; export settings for big-screen playback and for archival. Also a short "recognise your apps" checklist so the maker can report what is installed. Deliverables: the tool matrix (with a Scriptability column and a "verified on" date), the technique syllabus, and a "first 10 exercises" learning path, each exercise under two hours with a concrete output file and a self-check.

**Must answer.**
1. For each video editor: what does the free edition actually include and exclude today (Resolve free vs Studio limits on resolution, effects and hardware; Kdenlive and Shotcut's MLT underpinnings), and which ones can an agent drive without a GUI (Resolve's scripting API availability in the free edition, MLT `melt` command line, project-file generation)? Mark each claim with a date.
2. Which tools can render or export headless from a script, with the exact entry point (Blender `--background --python`, Inkscape `--actions` and export flags, ImageMagick and ffmpeg, Synfig CLI, Glaxnimate's Python, GIMP's Python API after GIMP 3, Krita's Python, Audacity macros or scripting pipe)? Which cannot (MagicaVoxel) and what the workaround is?
3. What is the simplest reliable 2.5D parallax and Ken Burns pipeline using only free tools, and which steps can be batched (cutouts, depth, camera moves, renders)?
4. For an SVG-centred look (line-draw reveals, maps, timelines, hand-drawn titles): what is the practical path from Inkscape to video without writing a web app, and where does Glaxnimate or Blender's grease pencil fit?
5. For a voxel or Minecraft-like look: which free tool makes it fastest to build a recognisable room, house or object from a photo reference, how to light and render it warmly (Blender, or in-app renderers), and how to export for video?
6. What are the correct export settings for (a) a big-screen premiere from a laptop or a USB stick, (b) a private web link, and (c) a twenty-year archive master, including captions? Which codecs and containers are safe across TVs and projectors?
7. Which free music and SFX sources have licences that clearly permit a public, non-commercial screening and a private online link, and what attribution they need? Where do AI music generators stand, and what should we avoid?
8. Which free tutorial creators are reliable for each tool (current versions, no clickbait), and which tutorials specifically cover our techniques?
9. What is the minimum hardware for the recommended stack, and what degrades gracefully on a weak laptop?

**Watch-outs.**
- Version drift. GIMP, Inkscape, Blender, Resolve and Kdenlive have all changed their scripting and UI substantially in the last two years; tutorials from before 2024 may describe menus and APIs that no longer exist. Date every tutorial and note the version it shows.
- Claiming scriptability from a feature list. Verify with the actual docs or a working command; "has a Python API" is not the same as "can run headless from a cron job."
- Free-edition fine print. Resolve free is powerful but has hardware and feature limits that matter for a laptop; note them rather than assuming Studio features.
- Tool sprawl. The maker can learn perhaps three tools well in nineteen weeks. The matrix may be wide, but the recommendation and the exercise path must be narrow.
- Web tools presented as desktop. Photopea and similar run in the browser; flag the privacy implication for family photos.
- Music "royalty-free" claims. Many libraries forbid public performance or require attribution; read the licence page, not the search result.

### 2.6 `format` — Delivery format and experience architecture

**Refined brief.** Compare delivery formats for a life journey due 2027-02-27, made by a learner plus AI agents, for a 50+ subject and a mixed-age, possibly non-gamer audience, with a likely premiere on a big screen at an event and a private link afterwards, and with a twenty-year horizon. Formats: (a) a linear animated film; (b) an explorable world (a Minecraft map with cinematic capture, a web voxel world such as a three.js-based scene, or a Godot build); (c) a scroll-driven web story; (d) hybrids (a film with short playable interludes; a playable "world map" whose chapters open short films; a film plus a printed or web companion). For each: the experience for the subject and for the room; venue fit (big screen at an event, private gift link, a kiosk or tablet at a party); effort and learning curve for *this* maker; risk; tools; longevity, hosting and archiving, including who hosts private family material and what happens when a service dies; accessibility (older viewers, captions, one-button or no controls, reading speed); and what free templates or engines can be reused without writing code in Phase 0. Include real examples of each format with how they were made, a decision matrix scored against the charter's success test and principles, and a recommended default with reasons and a named fallback. Deliverable: the decision matrix and a one-page recommendation the maker can accept or reject.

**Must answer.**
1. For each format, what is the audience experience in a room of 10–40 people of mixed ages watching one screen, and what breaks (who holds the controller, who reads, who waits)?
2. What are documented examples of each format used for a real person's life or memorial, how were they made, how long did they take, and are they still viewable today?
3. What is the honest effort estimate for each format for a learner with AI help, in weeks, and which have a working vertical slice achievable by week 9 of our schedule?
4. Longevity: which formats survive twenty years with minimal maintenance (a video file on several drives and a disc, versus a web build with dependencies, versus a Minecraft world tied to a game version)? What is the archival plan for each?
5. Privacy and hosting: for web formats, how would private family material be hosted so only invited people can see it, at what cost, and with what single point of failure?
6. Accessibility for older viewers: captions, pacing, font size on a TV, no time pressure, and how each format can be experienced passively (auto-play) by someone who will not touch a control.
7. For hybrids: how is a film with playable interludes actually presented at an event (who plays, how long, what if it fails), and is there an example that worked?
8. What is reusable now without code: slideshow and video templates, Minecraft cinematic tooling, scroll-story templates, Godot or three.js starter projects; and what hidden coding each really needs?
9. Which format best lets the maker *learn* (Principle on learning, Constraint on scriptable tools) while still finishing, and what is the recommended default plus fallback if the vertical slice slips?

**Watch-outs.**
- Choosing by what is exciting to build. The matrix must be scored from the audience, venue and success test outward; the maker can overrule, but the research should make the default a film unless evidence says otherwise.
- "No code yet" misread as "no code ever." The question is feasibility by the deadline for a learner; estimate the coding honestly for (b), (c) and (d) rather than hiding it behind "templates."
- Minecraft edition confusion. Java and Bedrock differ in maps, mods, capture tools (Replay Mod is Java-only, to verify) and platforms; say which one every example used.
- Longevity hand-waving. Web projects rot and private hosting costs money or depends on one person's account; make the archiving plan a scored column, not a footnote.
- Hybrids as a way to avoid deciding. If a hybrid is recommended, it must come with a presentation plan for the event and a fallback if the interactive part fails on the night.
- Examples without evidence of audience reaction. A memorial Minecraft world that got press is not evidence that a family of non-gamers enjoyed it; look for creator reflections on how it landed.

### 2.7 `creator-threads` — Creator recipes from X/Twitter threads, Reddit, YouTube and blogs

**Refined brief.** Sweep creator sources for concrete, reproducible recipes relevant to this project and turn them into recipe cards we can test: viral "my life in N seconds/years" morph edits; age-progression and growing-up transitions; AI photo-animation threads; "my life in Minecraft" builds and tributes; life-story animations made for a parent's birthday or anniversary; scrapbook and collage motion styles; stop-motion with printed photos; and AI music for tributes, with licensing caveats. Sources: X/Twitter (login-walled; locate threads via web search, mirrors, or the creator's own blog or YouTube, and record what is known when a page cannot be fetched), Reddit (r/editors, r/VideoEditing, r/StableDiffusion, r/comfyui, r/Minecraft, r/blender, r/DataIsBeautiful for life-timeline posts, r/genealogy for scanning and restoration), YouTube tutorials, Substack, Medium and personal blogs. For each recipe: source URL and date, creator, goal, tools and their cost on the date checked, exact steps, time and cost to reproduce, quality notes with a frank "does it look generic", what it violates or respects in our principles, and how we would adapt it with free tools. Favour recipes with free tools and with visible results on real family photos. Deliverable: a set of recipe cards in a consistent template, ranked by relevance and feasibility, plus a short list of creators worth following during the build phase.

**Must answer.**
1. Which "my life in N seconds" or growing-up morph edits have creators documented step by step (alignment method, frame rate, music sync, software), and which of those steps are reproducible with free desktop tools?
2. Which AI photo-animation threads from 2025–2026 show the full workflow with real old photos, which tools do they use, and what did they cost at the time? Which are still reproducible today?
3. What have people actually made for a parent's 50th, 60th or anniversary (animations, Minecraft worlds, scroll pages, printed books with QR codes to video), how long did it take, and what did they say afterwards about what the parent responded to?
4. What do "my life in Minecraft" and memorial-build creators do to make a build read as a specific real place or life, how do they capture it on video, and what tooling (Java or Bedrock, shaders, Replay Mod or alternatives) did they use?
5. What are the documented scrapbook, collage and paper-cutout motion techniques (in Resolve, Kdenlive, Blender or After Effects, with free equivalents) that keep real photos as real photos while adding warmth?
6. How do hobbyists do stop-motion with printed photographs, objects and hands, and what does that give us for marking reconstructions visibly?
7. For AI music: what do creators report about Suno, Udio and alternatives for tribute pieces, what do the current terms say about ownership and public performance, and what are the free human-made alternatives with clear licences? Date everything.
8. What do experienced editors on r/editors and r/VideoEditing say are the common mistakes in family tribute videos (length, music, transitions, text), and what do they recommend instead?
9. Which recipes should we *not* follow because they rely on paid mobile apps, discontinued services, or techniques that fabricate (face swaps, synthetic voices)?

**Watch-outs.**
- Promotional threads. A large share of viral AI threads are written to sell a tool or a course; prefer threads that show process and failures, and note the incentive where it is visible.
- Undated or re-posted content. Many morph-edit and AI tutorials circulate for years after the tool changed; record the original date and check the tool's current state.
- Login walls and mirrors. Record what could be verified and what could not; never cite a thread you did not actually see on some mirror or the creator's own site.
- Reel grammar. Beat-synced zooms, whip transitions and trending sounds are exactly what the charter rejects; harvest the technique (alignment, rhythm) and discard the style.
- Paid mobile-app recipes. Many "life in 60 seconds" videos are made in phone apps with subscriptions; the card must give the free desktop equivalent or mark it not reproducible.
- Music licensing from hearsay. Read the licence or terms page as of the date checked; "it's royalty-free" in a comment is not a source.

---

## Part 3 — Missing tracks (for the orchestrator's awareness; not added now)

1. **`sound-and-voice`** — Recording the subject's and relatives' voices well with a phone; interview audio cleanup in Audacity; music selection and licensing for a public screening and a private link; sound design for stills; the ethics line on synthetic voice. Currently scattered across `story`, `toolchain` and `creator-threads`; it is the highest emotion-per-hour asset we have and deserves its own note.
2. **`era-reference`** — How to research the texture of the subject's decades and places: what the kitchen, the car, the school uniform, the TV, the typefaces, the music charts and the prices looked and sounded like in their specific country and years, with free archives and reference sources, so that reconstructed scenes are true even when stylised. `animated` covers colour by era; nobody covers finding the facts.
3. **`production-plan`** — Project management for a nineteen-week solo-plus-agents project: the backward schedule, the vertical slice definition, test-screening protocol with a non-gamer over 60 and a child, backups, archival export, and the premiere-night checklist (file formats, playback device, captions, a fallback copy). The orchestrator may own this directly rather than researching it, but it should exist as a document by week 3.
4. **`rights-and-privacy`** — Consent from the other people in the photos; what may be shown at an event versus a private link; storage of family material (encrypted local copies versus a hosted repository); and a plain-language family consent note. Small, but it is the kind of thing that is painful to fix in week 18.

---

## Part 4 — Advisor insight

The most distinctive thing this piece can do is not visual. It is to let the subject's *own* ordinary language carry the structure. Fifty-plus years of a life leave a person with a handful of phrases they say without noticing: a way of answering the phone, a saying from their own parent, a joke they have told two hundred times. If the `story` track gathers those phrases from relatives first, each can become the title and the mechanic of a chapter, and the piece will be unmistakably about this one person before a single photo appears. No AI tool, no engine and no template can produce that; it is also the cheapest thing on the whole plan.

---

## Changelog
- 2026-10-18: initial review written by the Fable advisor before research start.
