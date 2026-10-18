# Production scale: how much film can a learner plus AI team finish to the theatrical bar? — research notes

*Track `production-scale`. Researcher: Sonnet. Written 2026-10-18 (Sunday, week 1 of 19). Research only; nothing was built except the editable model and templates in `research/production-scale-fixtures/`.*

*How to read the labels.* [n] points to the Sources list. **[J]** is my judgement, not a measurement. **ESTIMATE** is arithmetic on measured or sourced numbers. **UNVERIFIED** means I could not confirm it. **Snippet-only** means the URL appeared in search results but I could not open the page, so I only saw a search summary of it; I treat those as hearsay. **Hearsay** is any forum, résumé or unnamed-source number. (M1) to (M21) are the container measurements in `research/agent-pipeline.md` [3]; I did not repeat them. "Prior" means the numbers already written in the project's playbooks [2][5]. "Base" is my evidence-adjusted case. "Stress" is a plausible bad run.

*The user's note for this session.* The maker is the only person on the project, and the only person who knows. The schedule therefore contains no second-person gate: every approval, including the hard chapters, is the maker's own, with the Fable advisor flagging sensitive material [1]. Where the earlier plans relied on a proxy, this note uses the maker plus a waiting period instead (see Q8 and Risks).

---

## Summary (the most important things we learned)

1. **The runtime is decided by four design choices and by when the material arrives, more than by raw hours.** My model (CSV, every assumption visible) says a 12-minute film needs about **9.8 maker-hours a week** on the playbooks' own numbers (Prior), **19.6** on my evidence-adjusted numbers (Base), and **13.9** if five design levers are adopted (Base plus levers; **15.5** with the four that need no purchase, because lever 3, bought finishing, waits for two quotes). The best case, Prior speeds plus the levers, is **8.1**. For 25 minutes: 15.2, 31.5, 21.1, best case 11.9. For 45 minutes: 23.6, 49.6, 32.0, best case 17.9. For 90 minutes: 42.5, 90.3, 56.5, best case 31.3. These are averages over the 17 usable weeks and include story, gathering, finishing, learning and rehearsals (Q5). These 'h/week needed' figures are the total-hours check only; the largest-feasible-runtime figures (Summary 2) and the Q7 slice table include the post-holiday check, so the Q7 table is the stricter, operative one.
2. **Largest feasible runtime by weekly hours** (total-hours check plus the post-holiday production check, Q5): at 10 h/week about 12 min (Prior), 3 min (Base), 6 min (Base plus levers) and 18 min (best case); at 20 h/week 27, 9, 21 and 44 min; at 30 h/week 42, 15, 33 and 68 min. Hours per week are unknown, and the answer moves by a factor of three to five between the optimistic and the cautious case. **The one question to ask the maker now is how many hours a week they can reliably give.**
3. **Nothing in the published benchmarks supports our speed.** Festival-quality animated features made by one person run **1.1 to 3.7 finished minutes per person-month**; small teams run **0.06 to 0.3**; a documented solo feature cost the maker an estimated **114 hours per finished minute** (*Sita Sings the Blues*, 9,360 hours for 82 minutes) [14]. Our Base case implies 6.8 minutes per person-month and the Prior 13.6 (Q2). That is only believable because 85 percent of our screen time is photo moves and designed graphics rather than drawn or posed character animation. The pipeline's per-shot minutes are the single biggest unmeasured number, and the vertical slice exists to measure them.
4. **Traditional output is 1 to 7 seconds of finished animation per animator-week for feature quality** (Coraline 2 to 7, Boxtrolls 1 to 2 [26]; Wallace & Gromit 4.2 [25]; 3D feature 3 to 4, hearsay [28]), and about 14 to 30 seconds for classic or limited 2D (Disney about 14, hearsay [28]; Walter Lantz 1944, 25 feet or about 17 seconds with three assistants [29]; TV quotas of 25 to 30, hearsay [28]). One stop-motion feature claims 5 to 10 seconds a day per animator [22], which is 25 to 50 a week on a five-day week and up to ten times Laika; I treat that as a single-interview outlier (Q1).
5. **Hero shots are 10 percent of the shots but about 60 percent of the shot-hours** in the Base case (class C at 120 minutes each against 7, 15 and 6 for the others). Halving the hero share, cutting shots per minute from 12 to 8, buying the mix and grade, triaging photos and gathering earlier take the 12-minute requirement from 19.6 to 13.9 hours a week (15.5 without the bought finishing) and the 25-minute requirement from 31.5 to 21.1 (Q5).
6. **The calendar compresses the work harder than the totals show.** With Sunday-start weeks, production after the holidays is **five weeks (2027-01-03 to 02-06)**, finishing is **two weeks (02-07 to 02-20)** and the buffer week (02-21 to 02-27) already holds the rehearsals. At 20 h/week the finishing weeks hold only about 34 usable hours, so the master chain must be rehearsed inside the slice and the mix and grade partly outsourced or locked earlier chapter by chapter. The review-02 week numbers (12 to 15, 16 to 17, 18 to 19) are off by one against Sunday-start weeks; the dates are right (Q5).
7. **2024 to 2026 AI work gives no credible hours per finished minute.** The best-documented case, *Air Head*, took "a little over a week" for about a minute and a half, with hundreds of 10 to 20 second generations, a 300:1 ratio assumed by its post-production lead, and a large share of compositing and grading [41][42]. Vendor numbers (3 generations per usable shot, 25 percent kept, $315 to $750 per finished minute [47]) are not finished minutes to the bar. No source I found splits prompting, editing and fixing by measurement (Q3).
8. **Survivorship is large.** *Critterz* (about 30 people, 9 to 12 months planned, under $30M [43]) lost its video model when OpenAI shut Sora down in 2026 [45], missed its Cannes slot [45] and is now aimed at Q1 2027 [44]; [45] gives no date for the target. *Copán La Leyenda*, a 74-minute AI-finished feature, took about 15 years of development and was heavily panned [46]. *On This Day... 1776* drew public backlash for "repetitive camera movements" and "waxen characters" [50]. Tool volatility is itself a schedule risk (Q3, Risks).
9. **Vertical slice first, and make it include sound, grade and a master.** The slice chapter (C01 = first built, not first in the film) is a 100-second piece of module M1 (acceptance 90 to 120 seconds), mid-life, at final quality, played on the venue-class playback. It yields the measured maker-hours that replace the guesses. A table in Q7 converts the measured slice hours (`h_slice`, plus `h_slice_fin` for finishing) into the longest runtime that still fits at 10, 20 and 30 h/week. This is the basis for the **2026-12-20 kill-or-cut gate**.
10. **Picture lock:** lock chapter by chapter from 2027-01-17, hard lock Saturday **2027-02-06**. After lock only sound, grade, captions and equal-length text or photo swaps are allowed. A solo maker enforces it with a timeline hash, `locked=1` in `status.csv`, a git tag and a 24-hour unlock rule (Q8).
11. **Render cost is not the constraint, but the render route is.** Container Cycles takes 17.5 s per 1080p frame on one lit Suzanne scene and 204 s on Blender's 'classroom' scene at 24 samples plus denoise (F3). The stylised kitchen set will fall between them; spike S3 measures it. So a 12-minute film is about 18 CPU-hours at Suzanne speed and about 150 at classroom speed, almost all of it hero finals, which take 76 ten-minute jobs at Suzanne speed and 883 at classroom speed. A stand-in kitchen built from primitives with no photographs measured 112 s per frame at 64 samples and 204 s at 128, with denoise, on the container (round 2, G2; the GPU half was not run). Hero finals are therefore GPU work by default: the maker's own PC (Exercise 1), or a rented RTX 4090 at $0.34 to $0.89 an hour (RunPod page dated 2026-10-08) [54] for scenes with no family imagery only; a set textured with her photographs is family imagery and needs the maker's explicit say. On a 4090 a classroom-class hero frame takes 1.6, 3.0 and 5.6 seconds at 64, 128 and 256 samples at 1080p [82][83][84], so the 12-minute film's finals cost 1.2 to 4.0 GPU-hours, about $0.4 to $3.6 (ESTIMATE). The cost that matters is the maker's time and keeping family material off third-party machines (Q9).
12. **Shot tracking:** use plain text in the repo, `shots/status.csv` next to `brief.yaml`. Kitsu is AGPL-3.0 and mature (Blender Studio uses it) but costs €20 to €35 per user per month hosted or a Postgres, Redis, Nginx stack to self-host, and stores previews on a server; for one person it is not worth it (Q10, templates in the fixtures folder).
13. **Recommended runtime** (for reconciliation with `film-story`'s floor 12, target 15, cap 18, private stretch 25): commit to a **12-minute public cut built as a wrapper (cold open about 1:15 plus ending about 1:45) and three 3:00 modules** if the maker can give **about 16 hours a week or more** and adopts the four levers that need no purchase (about 14.5 if mix, grade and captions are bought after two quotes); plan **9 minutes (wrapper plus two modules)** if it is nearer 10 hours (at 10 hours, 9 minutes fits only with all five levers and a slice of about 13 hours or less; see Q7); treat **15 to 18** as unlocked only by a Dec 20 slice that measures at or below the thresholds in Q7; treat **25 as a post-premiere private cut**; do not plan 45 or 90. The schedule excludes them under Base at 30 h/week or less; they reopen arithmetically only in the best case (Prior speeds, all levers) at about 30 h/week for 45 and 40 for 90, and `film-story` excludes them on story grounds [7]. The orchestrator decides.
14. **Two things in the earlier plans do not survive contact with the numbers.** (a) `film-story`'s 12-minute floor is not safe at 10 h/week on any case except the Prior with zero slippage. (b) The "one week is buffer" is not free: the rehearsal calendar uses 8 to 12 hours of it.

---

## Findings by question

### Q1. Benchmarks: seconds of finished animation per person-week, by style and quality tier

Quality tier is the tier the source declares or the film's reception implies. "Hearsay" means no named, checkable source.

| Style | Output | Tier | Source and grade |
|---|---|---|---|
| Feature CG, studio | about 3 to 4 s per animator-week; 5 s "feature quality" on a forum | theatrical | "about 3-4 seconds of animation per week", no named source [28] (hearsay). Pixar 4 s, ILM 6 to 10 s appear in a forum thread (snippet-only [72]; not opened). The 5 s figure is a forum post (snippet-only [75]) |
| Stop-motion feature, Laika | *Coraline* 2 to 7 s per animator-week; *Boxtrolls* 1 to 2 s | theatrical | Annecy 2014 conference summary [26] (dated, studio talk) |
| Stop-motion feature, Laika, *Missing Link* | target 4.3 s; real average 2.5 to 3.5 s; 31 animators over 92 weeks | theatrical | trade article; page returned 403, quotes seen only in a search summary [27] (snippet-only) |
| Stop-motion feature, Aardman | **4.2 s per animator-week** on *Wallace & Gromit: Vengeance Most Fowl*; up to 30 animators at peak; shoot just over a year | theatrical | *Post* magazine, Nov-Dec 2024 [25] (supervising animator) |
| Stop-motion feature, indie | claim: seven animators doing 5 to 10 s **a day** over a 33-week shoot. Derived: 94 to 95 min / (7 x 32 to 33 weeks) = **24 to 25 s per animator-week** | festival, Annecy Cristal [23] | interview in the Austin Chronicle [22]; review says 32 weeks [24]. Single-interview outlier, 6 to 10 times Laika. Plausibly explained by simple sets and shots of only 5 to 10 s [70] (my inference) |
| Classic hand-drawn 2D feature | about 14 s per week; fastest 23 to 24 s | theatrical | animator blog, derived from "3.75 feet a day", no source [28] (hearsay) |
| Hand-drawn theatrical shorts, 1944 | **25 feet per animator-week, with three assistants**; at 24 fps (1.5 feet per second) that is about 17 s | studio | *Motion Picture Herald* 1944-11-04 via Lantern, Walter Lantz [29] (primary, old). The OCR text reads "25 feet or 37>4 seconds"; 25 feet cannot be 37 seconds at sound speed, so I trust the feet and treat the OCR seconds as unreliable |
| TV 2D, limited style | 25 to 30 s per week "some studios request" | broadcast | same blog [28] (hearsay). A Toon Boom forum thread said 12 to 18 s for hand-drawn TV (snippet-only [73]; the page now shows a closure notice) |
| Cut-out or After Effects style | no reliable benchmark found | various | One animator's résumé reports about 5 s a day on a cut-out feature (snippet-only [74], hearsay). Baumane is reported to draw 30 to 70 drawings a day (interview summary, source page not identified; UNVERIFIED) |
| Limited TV special, 1965 | 30 minutes in four months on $76,000 (*A Charlie Brown Christmas*) | broadcast, beloved | Wikipedia [30]; team size not given |
| Photo-animation documentary | simple parallax move on one photo "around 30 minutes"; an elaborate 4 s multi-layer shot "could easily take me a week" | pro desktop work | Adobe community expert, 2020-08-03 [37] (hearsay; a named expert) |
| Animated documentary shorts | StoryCorps: 3 min 15 s average, about 8 weeks of animation, 13 weeks total, 6 to 8 people (10 to 12 with audio). Derived: **about 3.5 s per person-week of animation** (195 s / 56 person-weeks); 2.1 s over the whole 13 weeks | broadcast (PBS) | Storybench interview [31] |
| Explainer-style motion graphics | agency rule of thumb **40 to 60 hours per finished minute**, longer with feedback | commercial | agency blog [40] (vendor, hearsay) |
| AI-assisted | *Air Head*: about 82 s in "a little over a week" by three people. Derived: **about 21 s per person-week** (my arithmetic; the three were not necessarily full time) | viral demo, not a theatrical film | [41][42]. Do not generalise: one concept, many reshoots, heavy compositing |

**What this tells us.** For work where every second is posed or drawn, feature quality is **1 to 7 seconds per person-week** and the quality bar does not make the number rise, it makes it fall. Classic and limited styles reach **about 14 to 30**. Our pipeline claims **101 s per person-week on Base (204 s on Prior)** for a 12-minute film (720 s / (284 h / 40 h) and 720 / (141 / 40)). That is 3 to 8 times the fastest traditional rates (TV quotas of 25 to 30 s, *Memoir* 25 s) and 20 to 100 times a feature rate. It is only credible because most of our seconds are not animation in this sense. It is the reason the share of hero shots, and the time per photo move, must be measured before anything is promised.

### Q2. Solo and small-team animated films: runtime, team, calendar, tools, tier; minutes per person-month and the spread

Person-months are team size times calendar months and are **upper-bound effort** where the source gives the team only as a range or says people were part time. "Min/pm" is finished minutes per person-month.

| Film | Runtime | Team | Calendar | Tools | Declared or reviewed tier | Min/pm |
|---|---|---|---|---|---|---|
| *Away* (2019) | 75 min | 1 | 3.5 years (Aug 2015 to Jan 2019); "seven days a week, maybe eight to 10 hours a day" | Maya, Premiere, Logic; long continuous takes; identical cats with copied animation to save time | Annecy Contrechamp Best Feature; Rotten Tomatoes 100% (31), Metacritic 78 [10][11] | **1.8** (about 150 h per finished minute, ESTIMATE: 41 months x 4.3 weeks x 7 days x 9 h / 75) |
| *Sita Sings the Blues* (2008) | 82 min | 1 (plus sound design, one helper on one scene) | about 5 years [J; not on the cited page, [14]] | 2D computer graphics, Flash, vector; $290,000 | Berlin premiere; the maker estimated **9,360 hours** | **1.4** (114 h per finished minute) [14] |
| *Is the Man Who Is Tall Happy?* (2013) | about 88 min (reported, not opened) | Gondry (two more animators credited per festival listing, snippet-only) | "three year period" (Vice [35]); other reviews say 2 years (snippet-only) | hand-drawn, shot on 16 mm | Berlinale 2014 programme | **2.4 solo over 3 years; 3.7 over 2; 0.8 if three people** |
| *Rocks in My Pockets* (2014) | 88 min | Baumane plus 5 assistants and interns | script 2010, premiere July 2014 | paper drawings, 28 built sets, Photoshop, After Effects; 30,000 drawings | festival feature, $1.03M box office [15][16] | **0.3** with six people over 4 years; 1.8 if counted as one person |
| *My Love Affair with Marriage* (2022) | 108 min | Baumane animated all but ~13 min herself; a Riga team coloured and composited | 7 years including funding (writing 2015) | pencil on paper, sets, Photoshop, After Effects; ~60,000 drawings | Tribeca and Annecy 2022 [17][18] | **1.1** (95 min by one animator over 84 months; time includes fundraising) |
| *Waltz with Bashir* (2008) | 90 min | art director with three assistants and two animation teams per interview coverage (snippet-only); headcount not stated | 4 years | Flash cut-outs, classic animation, 3D; 2,300 illustrations; $1.3M | acclaimed | not computable (team unknown) [19] |
| *Flee* (2021) | 90 min | "between 10 and 12 animators" plus clean-up, compositors; 50 to 60 at peak | from about 2013 (my inference from "eight years ago") to Jan 2021 including development | hand-drawn on computer; edit before animating; $3.4M | Sundance Grand Jury, Annecy Best Feature, three Oscar nominations; RT 98%, MC 91 [20][21] | about 0.25 on a rough guess (12 animators over ~30 months); UNVERIFIED |
| *Memoir of a Snail* (2024) | 95 min | 7 animators; larger crew not stated | script 3 years (16 drafts), storyboard 5 months by one person, preproduction 16 weeks, **shoot 33 weeks**, post 6 months | stop-motion clay; $4.5M | Annecy Cristal, BFI Best Film; RT 95% (140), MC 81 [22][23] | 1.8 animator-only (7 x 7.6 months); whole crew unknown |
| *Flow* (2024) | 85 min | 15 to 20 over the project, 3 to 5 at any time; director alone at first | 5.5 years (2019 to 2024) | Blender, EEVEE | Oscar winner; €3.5M [12][13] | **0.3** at four people on average; 0.06 at twenty |
| *Spring* (2019) | 8 min | 7 | 1.5 years including preproduction; about 100 shots; one shot took 2 to 3 weeks to animate | Blender | open movie [33][34] | **0.06** |
| *Sprite Fright* (2021) | about 10 min | about 10 | about 1 year (planned); about 220 shots | Blender | open movie, in production when written [33] | **0.08** |
| StoryCorps animated shorts | 3 min 15 s | 6 to 8 (10 to 12 with audio) | 13 weeks | 2D animation | broadcast [31] | **0.10 to 0.15** |
| *Sintel* (2010) | 14 min 48 s | not stated | 16 months (May 2009 to Sept 2010); €400,000 | Blender | open movie [32] | 0.9 per calendar month (team unknown) |
| *Consuming Spirits* (2012) | about 129 min | essentially one maker, two credited animators | "nearly 15 years" | cut-out, pencil, collage, stop-motion on 16 mm | festival listings (snippet-only; page not retrievable) | UNVERIFIED, part time |

**The spread, not the mean.**
- Solo auteur features: **1.1 to 3.7 min/pm** (Away 1.8, Sita 1.4, My Love Affair 1.1, Gondry 2.4 to 3.7). Median about 1.6. These are the people who made every frame themselves, full time, for years.
- Small-team features: **0.25 to 0.3** (Flow 0.3, Rocks 0.3, Flee about 0.25; 0.06 if all twenty of Flow's people are counted).
- Short films with a 3D pipeline: **0.06 to 0.08**. Broadcast animated shorts: **0.10 to 0.15**.
- Total spread: **about 40 to 60 times** (0.06 to 3.7). The mean of the numbers above (about 0.9) and the median (about 0.3) would both hide that it is two clusters: solo auteurs near 1 to 4 and everyone else below 0.4.
- Hours per finished minute: 114 (Sita), about 150 (Away, ESTIMATE). Agency motion graphics: 40 to 60 [40].
- Our model at 160 maker-hours a month: **6.8 min/pm (Base) and 13.6 (Prior)** for a 12-minute film. That is about 2 to 12 times the best solo results and 20 to 200 times the small-team results. Read it as a claim that must be proved by the slice, not as a forecast.

**What the best films have in common that we can copy.** The speed of the solo features came from design, not stamina: *Away* is a few very long takes through one built world with copy-paste cats [10]; *Sita* mixed styles and recycled whole sequences [14]; *Flee* edited the film before animating a frame, so the animators never drew a shot that would be cut [20]; *Memoir of a Snail* spent three years scripting, five months storyboarding and 16 weeks in preproduction before a 33-week shoot [22]. Everything that could be decided on paper was.

### Q3. 2024 to 2026 AI-assisted projects: breakdowns, selection ratios, reception, survivorship

| Project | What exists | Time and effort (as reported) | Selection ratio and fixing | Reception | Grade |
|---|---|---|---|---|---|
| *Air Head* (shy kids, Sora, 2024) | about 1.5 minutes (secondary coverage says 1:22; not on pages I opened) | "the film took us about maybe a little over a week from start to finish" [41] | generations of 10 to 20 seconds, "pulling two to three seconds out of it" [41]; "hundreds of generations"; **post-production lead "assumes a ratio of 300:1"** [42]; most clips looked like slow motion, balloon colour wrong, a face removed, upscaled, stabilised, graded, re-framed [42]; "a big chunk of it was in VFX ... compositing and color grading" [41] | viral; later coverage that it "wasn't all AI" (snippet-only) | interview with the makers: good. The ratio is "assumed", not logged |
| *Dear Upstairs Neighbors* (Google DeepMind with Pixar alumni, Sundance 2026) | about 6 minutes (search summary) | no durations given [49] | "none of our final shots were created in a single one-click generation"; artists made rough animation in Maya and TVPaint; fine-tuned Veo and Imagen turned it into the look; localized refinement; upscaled to 4K; text-only prompting was "random, uncontrolled" [49] | premiered at Sundance | the closest thing to a studio-grade AI-assisted animation workflow, and it needs animation skill and bespoke research tools; the page names about a dozen people, including researchers [49] |
| *Critterz* (OpenAI-backed, Vertigo, Native Foreign) | **not released** as of the latest report; first-look footage shown to buyers at the Cannes market | planned about 9 months, about 30 people, under $30M [43]; Kleverov: compress a multi-year build into about a year [44] | not published | missed an in-festival Cannes slot; Sora was shut down (app dark 2026-04-26, API scheduled to end 2026-09-24); new target Q1 2027 [44] ([45] gives no date) | trade press, two independent reports |
| *Copán La Leyenda* (Honduras, 2026) | released 2026-05-07 in theatres, 74 min | "about 15 years to develop", about 10 of them on traditional 3D, then AI tools "to largely finish the film" [46] | not published; Gemini watermarks seen in promotional material | **heavily panned** by critics and audiences; a "long commercial"; comments reportedly deleted [46] | Wikipedia with cited reviews |
| *On This Day... 1776* (Primordial Soup with TIME, 2026) | weekly shorts through 2026 | not published | humans wrote, voiced and scored; AI "in part" [50] | backlash; "repetitive camera movements", "waxen characters"; Aronofsky says later episodes improved | trade press |
| *Total Pixel Space* (Runway AI Film Festival Grand Prix, 2025) | 9:28 | not published | Midjourney, Runway, ElevenLabs; about 6,000 entries (snippet-only [53]) | festival winner | winner of a vendor's own festival |
| *The Frost* (Waymark, 2023) | 12 minutes | not published | every shot generated with DALL-E 2 then animated with D-ID (search summary) | novelty | no hours published |
| *Catacombs* (one filmmaker, Seedance 2.0) | runtime not found | claim: **3,229 generations, 242 hours, one filmmaker** (search summary of a Creative Bloq interview; the page would not load, [51]) | about 1 usable shot in how many is not stated | not found | **UNVERIFIED**; do not use as a planning number |
| *El Eternauta* (Netflix, 2025) | one building-collapse shot sequence | "ten times faster" said by a co-CEO on an earnings call (snippet-only [52]) | not published | reception not checked | self-reported, one sequence |

**Vendor and generic numbers.** One AI-video vendor's own FAQ gives about 3 generations per usable shot, a 25 percent selection rate (164 clips generated, 41 kept in a 3-minute episode), 55 to 267 generations per finished minute and $315 to $750 per finished minute. The page is vendor-authored and says the figures are "planning numbers" from a handful of productions [47]. A how-to blog's table (20 to 40 hours for a 3 to 5 minute film) names no production and is generic [48]. Neither says anything about the theatrical bar, hero-shot fixing, or real photographs.

**Share of time prompting versus editing versus fixing.** **No credible measured split exists in anything I found.** Qualitative evidence: a large share of *Air Head*'s effort was compositing, grading and correction [41][42]; the DeepMind short took animators plus researchers plus review "dailies" [49]. Treat any percentage as a guess.

**Image-to-video from real photographs.** I found no selection ratio. A project-specific complication already recorded: Veo image-to-video accepts only `allow_adult`, so photos with children are probably refused, and her childhood photos are the likeliest [8].

**Survivorship check.**
- Posts of the form "a feature with AI in three weeks" were not verified. One aggregator claims a 90-minute AI feature made in three months with a 48 percent Rotten Tomatoes score; its dates, runtime and quotes conflict and I discarded it as UNVERIFIED.
- Confirmed non-shipped or poorly received: *Critterz* unreleased and without its model [44][45]; *Copán La Leyenda* panned [46]; *1776* criticised [50].
- Confirmed shipped and praised: none with a published hours breakdown. The DeepMind short is the nearest and relied on a research team [49].
- Cross-reference: the reception evidence belongs to `cinematic-quality` Q8. That note does not exist yet; reconcile when it does.

**Read-across for us.** (1) The only usable planning range is the vendor's 3 to 4 generations per usable clip at the low end and shy kids' assumed 300:1 for text-to-video with one consistent character at the high end; use the low end as a floor until our slice logs real `gens_tried` and `gens_kept`. (2) Whatever we generate must still be graded, matched and fixed. (3) A service can vanish (Sora): never let one hosted model be the only route for a shot class. (4) AI-generated hero shots are an option for class C, not a plan: in the Base case they would need a measured keep rate from the slice.

### Q4. Our pipeline's own numbers: maker-hours and agent-hours per finished minute at the theatrical bar

**Inputs from the playbook [2].** About 120 shots per 10 minutes (12 per minute); class A templated photo move 60 percent at about 2 maker-minutes; class B designed graphic 25 percent at about 12; class C hero shot 10 percent at about 60; class D title 5 percent at about 5; chapter of about 100 seconds and about 20 shots; chapter pass 1 to 2 hours; agent time 10 to 40 minutes per shot; at most 3 fix loops and 2 revision rounds. All marked ESTIMATE [J]. The 100 to 150 maker-hours for 8 to 12 minutes in `format.md` and "6 to 10 hours per finished minute" are also [J] [5].

**Why I adjust them (Base).**
- *Planning fallacy.* The classic thesis study found people finished in 55.5 days against a prediction of 33.9, a factor of 1.64; only about 30 percent finished in the time they predicted [65]. I use a rework factor of 1.25 on top of already-padded minutes (1.0 in the Prior, 1.4 in Stress).
- *Class A is not 2 minutes if the photo needs hand prep.* A professional estimates a simple parallax move at about 30 minutes and an elaborate one at about a week [37]. If 20 percent of photos need 25 minutes of cut-out or inpaint decisions, the average class A shot is 7 minutes, not 2.
- *Class C at 60 minutes assumes the agent builds the scene and the maker only looks.* Real hero work is expensive: one *Spring* shot took 2 to 3 weeks to animate [34]. I use 120 minutes (reused-set camera moves only).
- *The learning curve.* Repeating a task cuts unit time by roughly 10 to 25 percent per doubling of output (Wright's law, 80 percent curve) [66]. I model chapter *k* as `max(floor, L1 x k^(log2 phi))` with L1 = 2.5 (first chapter 2.5 times steady state), phi = 0.80, floor 1.15. Base chapter multipliers: 2.50, 2.00, 1.75, 1.60, 1.49, 1.41, 1.34, 1.28. A 12-minute film (7 chapters) averages 1.73; 25 minutes 1.44; 45 minutes 1.31; 90 minutes 1.23.

**Cases (the CSV's three columns).**

| Parameter | Prior | Base | Stress |
|---|---|---|---|
| maker min per shot: A / B / C / D | 2 / 12 / 60 / 5 | 7 / 15 / 120 / 6 | 10 / 18 / 180 / 8 |
| weighted maker min per shot (60/25/10/5 mix) | 10.45 | 20.25 | 28.9 |
| rework factor | 1.0 | 1.25 | 1.4 |
| chapter pass hours per chapter | 1.5 | 2.0 | 2.5 |
| sound integration during production, h/min | 0.3 | 0.6 | 0.8 |
| story + animatic, h/min | 0.5 | 1.0 | 1.4 |
| gathering (scans, low-key asks, labelling, clearances), h/min | 0.6 | 1.2 | 1.8 |
| learning multiplier L1 / floor / phi | 2.0 / 1.10 / 0.80 | 2.5 / 1.15 / 0.80 | 3.2 / 1.25 / 0.88 |
| reuse saving on shot hours | 15% | 10% | 3% |
| one-off reuse build / learning + lock hours | 15 / 20 | 20 / 30 | 40 / 50 |
| finishing: h/min + fixed hours | 1.5 + 16 | 2.7 + 24 | 3.5 + 32 |
| rehearsal hours (W19) | 8 | 10 | 12 |
| risk reserve | 5% | 10% | 15% |

**Steady-state maker hours per finished minute** (shots + chapter pass + sound, after the first chapters): **Prior 2.98, Base 6.36, Stress 10.15.** Plus story 0.5 / 1.0 / 1.4 and gathering 0.6 / 1.2 / 1.8, plus finishing 1.5 / 2.7 / 3.5.

**Hero-shot warning.** In the Base case, class C is 10 percent of shots and **59 percent of the shot-minutes** (12 of 20.25 minutes per average shot). It is where the schedule is won or lost.

**Hours by stage for a 12-minute film at the Base case** (total 284 hours): shot production including learning and rework 94 (33%), chapter passes 24, sound integration 7 (production side 126 hours, 44%); story and animatic 12; gathering 14; risk reserve 15; finishing 56 (20%); one-off learning, reuse build and rehearsals 60 (21%).

**Pipeline stages and who does them (script to master).**

| Stage | Output | Who | Base maker h/min |
|---|---|---|---|
| Treatment, narration, beats (`film-story`) | slot-based beat sheet, VO script | agent drafts, maker decides | 0.5 |
| Storyboard and animatic | timed boards with temp sound | agent assembles, maker reviews | 0.5 |
| Gathering, scanning, labelling, clearances | manifest lines, consents | maker (covert asks) | 1.2 |
| Layout and shot brief (G0, G1) | `brief.yaml`, three style frames | agent writes, maker approves | in shot minutes |
| Animation, comp (Routes A/B, Blender) | draft renders (G2) | agent builds, maker reviews | 4.6 incl. rework and reuse |
| Hand refinement (G3, class B/C only) | Craft-app passes | maker | in shot minutes |
| Chapter assembly and passes (G4 to G6) | chapter master | maker plus agent | 1.2 |
| Score, VO, sound integration | cue sheet, stems | maker spots; composer or library; agent assembles | 0.6 |
| Grade, mix, captions, QC | final audio and picture | maker (or hired) | 2.7 |
| Master, access copies, DCP or file, verification | ProRes 422 HQ, H.264, checksums | agent scripts, maker checks | 24 fixed |

**Agent-hours per finished minute.** At 10, 25, 60 and 10 agent-minutes for classes A to D (my reading of "10 to 40 minutes per shot" [2]), times 1.5 for rework: **about 5.6 supervised agent-hours per finished minute**, so 68, 141, 253 and 506 hours for 12, 25, 45 and 90 minutes. At three agents in parallel (the playbook's cap) that is 23 to 169 wall-clock hours; the maker's review latency is the real bottleneck. How much of a Claude plan allowance this uses is UNVERIFIED. For scale, an unattended 22-agent run cost $207.58 at API prices for a 90-second film [2][3]; do not extrapolate from it, and do not run unattended studios.

**Container compute per finished minute** (measurements M4 to M21 [3]): Route B photo moves 7.8 fps at 1080p, one process; SVG scenes 12.9 fps flat, 5.7 with a wobble filter; Blender Workbench about 1 s per frame; Cycles CPU with 24 samples and denoise 17.4 to 19.0 s per frame on the Suzanne scene, and 204 s per frame on the classroom scene (F3); software EEVEE 34 to 36 s per frame (slower than Cycles). Using 4 iterations for photo and graphic shots, 1.5 final renders plus 4 Workbench drafts for hero shots, and 0.1 hour for grain, grade and encodes: **about 1.5 CPU-hours per finished minute** at Suzanne speed, 1.2 of it hero shots (Cycles finals and Workbench drafts); at classroom speed the same plan is about 13 CPU-hours per finished minute, nearly all of it hero finals (F3; 153 CPU-hours for 12 minutes). The depth-parallax route measured 12.3 fps at 640 x 480 [4]; scaled by pixels (6.75 times) it is about 1.8 fps at 1080p (ESTIMATE, UNVERIFIED), about 66 seconds per 5-second shot.

**Theatrical finishing cost per minute** (grade, mix, captions, master). Rules of thumb I found are hearsay: audio post "one hour per finished minute" and "six hours per linear minute" from forum posts (snippet-only, [68]); iZotope's advice for short-film mixes is to "take the amount of time you think you need, and double it" and to add days of buffer [62]; one freelancer lists post mixing at $150 and dialogue editing at $100 per minute (snippet-only). My Base: grade 0.5 + mix 1.5 + captions 0.3 + QC 0.4 = **2.7 maker-hours per minute plus 24 fixed hours** (master, DCP or file, verification, backups). DCP encoding is CPU-bound JPEG2000; DCP-o-matic's own page gives GPU (Grok) benchmarks of 85 and 180 frames per second on its Sintel test, no CPU number, and no resolution [61]. At an assumed 4 fps CPU-only a 12-minute 2K DCP (17,280 frames) would take about 70 minutes (ESTIMATE, UNVERIFIED); 4K takes 3 to 4 times as long (developer statement, snippet-only). `theatrical-delivery` owns the DCP decision.

**Formulas (also in the CSV).**
```
n        = round(T*60 / chapter_s)                       # chapters
L_k      = max(floor, L1 * k^(log2 phi))                  # learning multiplier, chapter k
L_avg    = average of L_1..L_n
shots    = spm * T
min/shot = sA*mA + sB*mB + sC*mC + sD*mD
shot_h   = shots*min/shot/60 * rho * (1-reuse) * mu * L_avg
chapter_h= n * chap_h * L_avg * mu
sound_h  = T * sound * mu
prod     = shot_h + chapter_h + sound_h
total    = prod + T*(story+gather) + reserve*(prod+T*(story+gather))
           + T*fin_var + fin_fix + learn + setup + reh
capacity = H * u * (W_pre + W_post + W_fin + W_buf)       # 9+5+2+1 = 17 weeks, u = 0.85
need_H   = total / (u * 17)
```

### Q5. The schedule model

**Calendar, worked backward from Saturday 2027-02-27 (weeks start on Sunday; verified with a script).**

| Weeks | Dates | Use | In the model |
|---|---|---|---|
| W1 to W4 | 2026-10-18 to 11-14 | learn; spikes S1 to S5; style bible; **lock Sun 2026-11-15** | pool W1-W9 |
| W5 to W9 | 2026-11-15 to 12-19 | real photos start arriving, unevenly; slice; early chapters; gathering | pool W1-W9 |
| (gate) | **Sun 2026-12-20** | slice approved (G-SLICE) | decision |
| W10, W11 | 2026-12-20 to 2027-01-02 | **holidays: dead zone, no production** | 0 hours |
| W12 to W16 | 2027-01-03 to 02-06 | production; **picture lock Sat 2027-02-06** | pool W12-W16 (5 weeks) |
| W17, W18 | 2027-02-07 to 02-20 | finishing only; strangers-to-her screening in W17 if held (otherwise the cold self-read); master verified by Sat 02-20 | pool W17-W18 (2 weeks) |
| W19 | 2027-02-21 to 02-27 | buffer, rehearsals (Mon 02-22 playback, Wed 02-24 room brief, Thu-Fri cold starts) | pool W19 |

Correction to review 02: its list "weeks 12 to 15 (to 02-06), 16 to 17 (to 02-20), 18 to 19" is off by one against Sunday-start weeks; production after the holidays is **five** weeks, W12 to W16, and finishing is W17 to W18 [6]. Total usable weeks are **17** (19 minus two dead). Jurisdiction is unknown, so other observances are unknown; the model carries only the stated dead zone (see Open questions).

**Usable hours** (u = 0.85, [J]): H = 10 gives 144.5 hours; 20 gives 289; 30 gives 433.5. (`schedule.csv` reproduces these.)

**Four checks, per scenario.**
1. *Total hours:* hours required (Q4) against capacity.
2. *Post-holiday production:* only a share of production can be built before 2026-12-20 because material arrives from week 5 and unevenly. I cap it at **40 percent of production hours** [J]. The rest must fit in W12 to W16 after story, gathering and rolling finishing take their share. This check usually fails first.
3. *Finishing weeks:* finishing hours that cannot be done earlier (50 percent of the fixed hours stay after picture lock, 75 percent of the variable hours do, given the slice rehearsal and rolling locks) against W17 to W18 capacity.
4. *Buffer:* W19 hours left after rehearsals.

**Results.** Hours required (total), hours per week needed, and verdicts, for four cases. "Levers" means the five changes below applied together. **Best case** means Prior speeds plus the structural levers (hero share 5%, 8 shots per minute, finishing bought at 0.8 h/min, 50% of production buildable before 12-20); to reproduce it in the CSV choose case 1 and change those four inputs (photo triage is not needed because Prior class A is already 2 minutes). Verdict codes: OK (checks 1 and 2 pass), post (total passes, post-holiday production does not), SHORT (total fails); "/fin" means the finishing weeks are a crunch and need outsourcing or earlier locks.

| Runtime | Hours required: Prior / Base / Base+levers / Best | Weekly hours needed: Prior / Base / Base+levers / Best | H = 10 | H = 20 | H = 30 |
|---|---|---|---|---|---|
| **12 min** (144 shots at 12 per min) | 141 / 284 / 201 / 116 | **9.8 / 19.6 / 13.9 / 8.1** | Prior +4 h OK/fin; Base -139 SHORT; levers -57 SHORT; Best +28 OK | Prior +148 OK; Base +5 post/fin; levers +88 OK; Best +173 OK | all OK (+293, +150, +232, +317) |
| **25 min** (300 shots) | 220 / 456 / 305 / 173 | **15.2 / 31.5 / 21.1 / 11.9** | all SHORT (-75, -311, -161, -28) | Prior +69 OK/fin; Base -167 SHORT; levers -16 SHORT; Best +116 OK | Prior +214 OK; Base -22 SHORT/fin; levers +128 OK; Best +261 OK |
| **45 min** (540 shots) | 341 / 717 / 462 / 259 | **23.6 / 49.6 / 32.0 / 17.9** | all SHORT | Prior -52; Base -428; levers -173 SHORT; Best +30 post/fin | Prior +92 but post-holiday short; Base -284; levers -29 SHORT; Best +175 OK |
| **90 min** (1,080 shots) | 614 / 1,305 / 816 / 452 | **42.5 / 90.3 / 56.5 / 31.3** | all SHORT | all SHORT (Best -163) | all SHORT (-180, -871, -383; Best -18) |

**Largest feasible runtime (minutes), by weekly hours** (checks 1 and 2; the model solves it directly):

| | H = 10 | H = 20 | H = 30 | H = 40 |
|---|---|---|---|---|
| Stress | 0 | 3.5 | 6.0 | |
| Base | 2.9 | 9.4 | 15.5 | |
| Base + levers | 5.5 | 20.7 | 32.7 | |
| Prior | 12.4 | 27.5 | 42.2 | |
| Best (Prior + levers) | 18.4 | 44.3 | 67.5 | 90.8 |

**How to read the spread.** The gap between Base and Best is the gap between "the playbook's per-shot minutes are right" and "they are about 2.2 times too low". Nothing in the published benchmarks (Q1, Q2) supports the Best column; it is the case the slice must earn. Planning to Base and hoping for Best costs a few unused hours. Planning to Best and getting Base costs the premiere.

The Base number at 10 h/week is small because fixed work (learning 30, reuse build 20, rehearsals 10, fixed finishing 24: 84 hours) uses 58 percent of the 144.5 usable hours before a single minute is made. If you only have 10 hours a week, skip the reuse program, outsource the master chain, and plan for **9 minutes (wrapper plus two modules)** if the slice comes in near Prior speed (about 10 hours); otherwise add hours or buy finishing.

**The five levers (Base case, effect on weekly hours needed for 12 and 25 minutes, and on the largest runtime at 20 and 30 h/week).** Each is an input in the CSV.

| Lever | 12 min | 25 min | Largest runtime at 20 / 30 h |
|---|---|---|---|
| none | 19.6 | 31.5 | 9.4 / 15.5 |
| hero share 10% to 5% (shift it to class A) | 17.6 | 28.1 | 11.8 / 19.3 |
| 8 shots per minute instead of 12 (longer holds) | 17.2 | 27.4 | 12.4 / 20.2 |
| pay for mix, grade and captions (finishing 2.7 to 0.8 h/min) | 18.1 | 28.3 | 10.1 / 16.7 |
| triage photos (class A 7 to 4.5 min) | 19.1 | 30.6 | 10.0 / 16.4 |
| front-load gathering so 60% of production can be built before 12-20 | 19.6 | 31.5 | 12.0 / 22.6 |
| four levers that need no purchase: hero share 5%, 8 shots per minute, photo triage, front-loaded gathering (pre-holiday share 50%) | **15.5** | **24.4** | **18.2 / 29.0** |
| **all five together** (pre-holiday share 50%; lever 3 waits for two quotes) | **13.9** | **21.1** | **20.7 / 32.7** |

Sensitivity of the Base largest runtime to the pre-holiday share: 0.3 gives 8.0 / 13.3 min at 20 / 30 h; 0.5 gives 11.3 / 18.5; 0.6 gives 12.0 / 22.6. Sensitivity to utilisation: u = 0.7 gives 7.4 / 12.2; u = 1.0 gives 11.5 / 19.0. **The thing the maker can influence most before 12-20 is how much real material is in hand and how many hours go into the slice.**

**What reuse buys.** In the Base case the full reuse program (20 hours to build recurring sets and motifs, 10 percent saving on shot hours) *loses* 8.5 hours at 12 minutes, breaks even at 25, and gains 13 at 45 and 42 at 90. A lite program (8 hours, 6 percent) is about neutral at 12 and gains 4 at 25 (Q6).

**Kill-or-cut calendar (generic gates; `gates.csv` holds the same).**

| Date | Gate | Test | If not met |
|---|---|---|---|
| Sun 2026-11-15 | G-READY | settings card; spikes S1 to S5 pass or fallbacks named; style bible and three style frames approved; **H confirmed in writing** | one week of grace (to 11-22); then drop one tier |
| Sun 2026-12-06 | G-SLICE-0 | slice animatic with real photos and temp sound; first logged hours | cut one tier now |
| **Sun 2026-12-20** | **G-SLICE** | slice approved at the bar, including mix, grade, captions and a master played on venue-class playback; stranger-read passed if you decide to hold one (Decision 8), otherwise the cold self-read passed; **h_slice and h_slice_fin measured**; material-in-hand known | compare h_slice with the Q7 thresholds; red = next shorter scenario |
| Sun 2027-01-03 | G-RESTART | H and material reconfirmed | if H fell by more than 25 percent, recompute and cut now |
| Sun 2027-01-17 | G-MID | at least 45% of runtime at "approved" (5.4 min of 12; 11 of 25; 20 of 45) | 12 min: cut the lowest-priority module now (to 9 minutes); a second module only at G-DRAFT, if not at draft. 25 and 45 min: cut the lowest-priority modules now |
| Sun 2027-01-31 | G-DRAFT | all kept modules at "draft", at least 60% rolling-locked, finishing chain rehearsed | replace unfinished modules with a held-still plus voice-over fallback or cut |
| **Sat 2027-02-06** | **G-LOCK** | every shot `locked=1`, timeline hash recorded, git tag | unlock rule only (Q8) |
| Sat 2027-02-13 | G-MIX | mix v1 and grade v1; strangers-to-her screening held in W17 if decided (Decision 8), otherwise the cold self-read of the whole film | fix list only |
| Sat 2027-02-20 | G-MASTER | master and access copy verified, two backups verified | buffer week is for fixing |
| Mon 2027-02-22 | G-REHEARSE | plays end to end on venue-class playback | USB access copy as fallback |

**Kill-or-cut by scenario.**

| Scenario | Decision | Named date | Rule |
|---|---|---|---|
| **90 min** | **Kill now.** | 2026-10-18 | Needs 42.5 h/week at Prior speeds, 31.3 even in the best case (short by 18 hours at 30 h/week) and 90 at Base; `film-story` also says the story supplies perhaps 8 to 24 scene-grade memories against the 36 it would need [7]. Re-open only if H of 40 or more is confirmed in writing by 2026-11-15 and the slice measures at most about 10 hours. Cut to 45. |
| **45 min** | Kill at the lock unless H is at least 30 | **2026-11-15** | At 12-20, continue only if h_slice is at most about 10 hours (Prior speed) and every lever is adopted (best case needs 17.9 h/week); Base needs 49.6. Otherwise cut to 25. In practice treat 45 as a post-premiere project. |
| **25 min** | Decide at the slice | **2026-12-20**; second chance **2027-01-17** | Continue only if the Q7 table says it fits your H (for example H = 30 with h_slice at most 15 without levers or 37 with levers; H = 20 only with all levers and h_slice at most 21). At 01-17, below 45% approved (11 of 25 min): cut to 15 to 18. |
| **12 min** | Decide at the slice | **2026-12-20**; **2027-01-17**; **2027-01-31** | At 12-20, if the table says it does not fit your H, cut to **9 minutes (wrapper plus two modules)**. At 01-17, below 5.4 minutes approved: cut the lowest-priority module (to 9 minutes); a second module is cut only at 01-31, if it is not at draft. At 01-31, any unfinished module becomes a fallback chapter. |

All kill-or-cut dates fall on Sundays or Saturdays, so the maker can act on them at the weekend.

### Q6. Shots per minute by style, our shot counts, and the reuse plan

| Style | Shots per minute | Basis |
|---|---|---|
| Documentary feature (live action) | about 5 to 6 | the average documentary has 491 shots [38]; runtime is not given on the page; 80 to 100 minutes gives 4.9 to 6.1 (inference) |
| Photo-montage tribute | 15 to 20 | 3 to 4 seconds per photo, funeral-industry guidance recorded in `format.md` [5] |
| Animated short, dense 3D | about 22 | *Sprite Fright*: about 220 shots in about 10 minutes [33] |
| Animated short, moderate 3D | about 12.5 | *Spring*: about 100 shots in 8 minutes [33][34] |
| Stop-motion feature | 6 to 12 | *Memoir of a Snail*: shots "only five to 10 seconds long" [70] |
| Solo long-take features | well under 3 (inference) | *Away* and *Flow* use very long camera moves through one built world [10][71] (snippet-only for *Flow*) |
| Dialogue scene, TV-style cutting | 8 to 15 [J] | no source |
| **Ours (default)** | **12** | playbook [2]; **8 is the documentary-pace lever** |

The standard shot-length study of 160 Hollywood films treats animation as one of five genres but reports no animation average, so I could not source a feature-animation shots-per-minute figure from it [39].

Our shot counts: at 12 per minute, **144 / 300 / 540 / 1,080** shots for 12 / 25 / 45 / 90 minutes (hero shots at 10 percent: 14 / 30 / 54 / 108); at 8 per minute, **96 / 200 / 360 / 720** (hero at 5 percent: 5 / 10 / 18 / 36). The average shot is 5 seconds (120 frames) at 12 per minute and 7.5 seconds (180 frames) at 8.

**Reuse plan, with honest savings.** The plan in the brief (recurring sets such as the kitchen and the street, one world map, the object clock, a title system, a portrait ladder) saves less time than it sounds, but buys coherence:

| Element | Shots using it (12 min) [J] | Build hours [J] | Time saved | Why keep it |
|---|---|---|---|---|
| Kitchen set (3D or layered 2.5D) | 8 to 12, mostly class C | 8 to 10 | about 40 min per class C reuse; about 5 min per class B | returns of the same place carry time; recurring sets are the biggest saving |
| Street set | 4 to 6 | 6 to 8 | about 5 h only if used for 6+ hero shots | same |
| One world map | 4 to 6 | 4 to 6 | 8 min per map shot | coherence of "where are we" |
| Object clock | 4 to 6 | 4 | 6 min per use | the time device |
| Title system | 8 to 10 | 3 to 4 | 3 to 4 min per title | consistency, template-risk control |
| Portrait ladder (same framing of her across ages) | 8 to 12 | 2 to 3 | 2 min per use | the emotional through-line |

Documented reuse in the benchmarks is real but modest: *Away* made the cats identical and copied animation between them to save time on its hardest scene [10]; limited animation reuses cycles and still backgrounds by definition [30]; a 2026 AI storyboarding study found a shared asset library cut model builds by about 12 percent (501 requests down to 440 unique; a count of builds, not hours; snippet-only [69]). My estimate: **3 to 15 percent of shot-hours**, positive only above about 20 to 25 minutes in Base unless the element appears in many hero or class B shots. For 12 minutes build the title system and one set (kitchen) only: `setup` 8 hours, `reuse` 6 percent. **Sameness cost:** reused sets and motion read as a template (Pitfall 1 in the playbook [2]). Mitigations already in the playbook: seeded variety, at least one non-moving photo per chapter, no more than three class A shots in a row.

### Q7. The vertical slice

**Which chapter.** Decided in round 2: the slice is a **100-second piece of module M1** (acceptance 90 to 120 seconds; the model's 100-second unit and about 20 shots [2]). It contains the kitchen hero shot, at least 10 class A, 4 class B and 1 class D shots, a VO line, one music cue, one still where the photo does not move, and the transition into the next module's motif. The remaining ~80 seconds of M1 is built after the gate, as the second learning-curve unit. T2 and model row 174 are per 100-second unit and stay as they are. (The alternative, the whole 180-second module as the slice, would scale row 174 to about 1.64 times 26.5, about 43 hours in Base, and regenerate T2; this note chooses the 100-second piece.) The piece is chosen on production grounds so it de-risks the most:
- A **mid-life chapter with the most material already in hand** (photos and a recorded voice), so the 40 percent pre-holiday assumption is tested honestly.
- **Not a hard chapter**, so the slice cannot be blocked by a dignity decision; the 72-hour double-decision rule from `film-story` applies to hard chapters and would eat the calendar.
- **Not the childhood chapter** (least material, strongest pull toward invented content, Principle 4) and **not the most recent decade** (most living people, most rights questions).
- It must contain **all four shot classes**, as listed above: the kitchen hero shot (class C on the reusable set), class A, B and D shots, the voice-over line, the music cue, the still and the transition.
- The story track picks the actual chapter; this is the production brief for that choice.

**Why this de-risks the most.** It exercises, in one pass: the real class-by-class maker minutes (the unmeasured numbers in Q4); the first-chapter learning multiplier L1; the review loop latency; the Craft-app hand-offs; sound and grade, which are normally discovered last; the master chain; the template look; and the gathering lag. Game developers use the same logic: a vertical slice is a case where "some subset of the final game now exists, which is fully reflective of the final product", it may be only a tiny part of the content, and it is the milestone commercial games use to judge whether pre-production is complete [64]. A proof of concept is a different, smaller thing: weeks, one core question, aimed at the team (search summary of game-industry guides, UNVERIFIED). Animation studios do the cheap version first: Pixar's look tests were "super quick and dirty, just with a few days of work for each" so that the team agreed on direction [67]. So: **days for look tests (three style frames), weeks for the slice.** *Flee*'s director says "you actually edit before you start animating", so the animators drew only shots that survived [20].

**Acceptance test (all must pass; record each in `reviews/C01/` and `decisions.csv`).**
1. **Length and frames:** 100 s (accept 90 to 120 s), frame count exactly duration times 24, ffprobe clean (the playbook's validators [2]).
2. **Picture at the bar:** full-resolution crops of faces and type clean; no invented faces; reconstructions visibly stylised; template check passes (no more than 60 percent of tweens share one ease); no more than three class A shots in a row; at least one still.
3. **Sound:** a real mix, not a temp: VO, music cue, room tone, transitions; loudness measured with `ebur128` against the target set by `theatrical-delivery`; **a person listened on the venue-class speakers** (the 22-agent run opened 604 images and played no sound [2]).
4. **Grade:** one look applied through the same chain for every shot; the colour-patch test passes within plus or minus 3/255 on the final encode [2].
5. **Captions:** inside the reading-speed and length limits in the format track.
6. **Master:** ProRes 422 HQ and H.264 access copy produced, plus a DCP test file if a DCP is in scope; played end to end on a TV or projector at about 3 m.
7. **Strangers read it, or the cold self-read.** If the maker decides to hold a stranger read (Decision 8), two or three people who do not know her and cannot reach the family see it cold and answer: who is she, what did she want, what did you feel (protocol from `cinematic-quality`; I only schedule it, in W9 for the slice and W17 for the whole). If the maker does not, the cold self-read below passes instead, in the same slot.
8. **Hours logged** in `hours.csv` by stage and class: `h_slice` (production side) and `h_slice_fin` (finishing), with learn and admin reported against the 30-hour allowance, agent hours, render seconds, rework counts and (if AI clips were used) generations tried and kept.
9. **Surprise safety:** repo, folder and commit names harmless; no personal data in any cloud service; `cloud` levels respected [2].
10. **Verdict:** apply the table below and write the decision in `decisions.csv`.

**The cold self-read (the substitute).** You show the cut to no one. Leave it unopened for 48 hours. Then watch it once on venue-class playback at about 3 m with the sound on. Before taking any notes, answer three questions in writing: who is she, what did she want, and what did you feel. The Fable advisor applies the `cinematic-quality` rubric to the same version.

**Converting measured slice hours into a runtime.** `h_slice` is the production-side hours for the slice: the sum of hours.csv minutes for the slice with activity in brief_G0, style_G1, review_G2, craft_refine_G3, chapter_G4, dignity_G5, tech_G6, sound and rework, for one 100-second unit. The model's prediction is shots, chapter pass and sound only: 9.9 (Prior), **26.5 (Base)** and 54 (Stress). `h_slice_fin` is the sum for grade, mix, captions, master and qc. Its Base prediction is **16.5 hours**: 2.7 hours per finished minute for 1.67 minutes (4.5), plus the half of the 24 fixed finishing hours pre-built in the slice (12). The measured-to-predicted finishing ratio gives `mu_fin`, which scales the finishing rows. Learn and admin are excluded from both and compared with the 30-hour allowance. G0 and G1 work is priced inside the per-shot minutes (Q4 stage table: 'Layout and shot brief: in shot minutes'), so brief_G0 and style_G1 belong in `h_slice` and are already in the prediction; `story` is the activity priced separately. A scribe's LibreOffice recalculation of `model.csv` gives 23.9 at h_slice 26 and 19.5 at 20 for 12 minutes; the table shows 24.1 and 19.6. The gap is under 1 percent and is the same small offset the other cells show (0.1 to 0.2 hour). Rounding the prediction to 26.5 does not explain it (that gives 24.3), so the table is unchanged and the offset is noted here. The table shows the **weekly hours needed** (total plus post-holiday checks), keeping Base values for story, gathering and finishing (so it holds with `mu_fin` = 1), and the **largest `h_slice` that still fits** each H.

| Runtime | Needed h/week at h_slice = 10 / 15 / 20 / 26 / 35 / 45 | Max h_slice that fits, no levers: H = 10 / 20 / 30 | Max h_slice that fits, with all five levers (lever 3, bought finishing, included): H = 10 / 20 / 30 |
|---|---|---|---|
| 8 min | 11.3 / 12.7 / 14.0 / 17.3 / 22.1 / 27.5 | 5 / 31 / 50 | 16 / 69 / 107 |
| 9 min (wrapper plus two modules) | 11.9 / 13.3 / 15.4 / 18.9 / 24.2 / 30.1 | 3 / 28 / 45 | 13 / 63 / 99 |
| 10 min | 12.6 / 14.1 / 16.9 / 20.7 / 26.5 / 33.0 | 2 / 25 / 40 | 11 / 56 / 89 |
| 12 min | 13.7 / 15.9 / 19.6 / 24.1 / 30.8 / 38.2 | none / 21 / 34 | 7 / 47 / 76 |
| 15 min | 15.5 / 19.2 / 23.6 / 28.8 / 36.8 / 45.5 | none / 16 / 27 | 3 / 38 / 61 |
| 18 min | 17.3 / 22.3 / 27.4 / 33.4 / 42.5 / 52.6 | none / 13 / 23 | none / 31 / 52 |
| 25 min | 23.0 / 29.6 / 36.1 / 43.9 / 55.7 / 68.8 | none / 8 / 15 | none / 21 / 37 |

Read it like this: with 20 hours a week, a slice that took 26 hours makes 12 minutes fit only with the levers (without them the limit is 21 hours); with 30 hours a week and a 26-hour slice, 15 minutes fits without levers and 25 does not; at 10 hours a week, 9 minutes fits only if the slice took about 13 hours or less and all five levers are pulled, lever 3 included (8 and 10 minutes need 16 and 11 hours); that is about half the Base prediction. Without levers, the limit at 10 hours is 3 hours of slice. Paste `h_slice` and `h_slice_fin` into the CSV (`SLICE CALIBRATION`, rows 173 and 176), copy the suggested `mu` and `mu_fin`, and the whole model recomputes.

**What practitioners say a proof must prove before scaling** (synthesis): that the end-to-end chain works at the final bar (picture, sound, grade, master) and not just one stage [64]; that the look is agreed cheaply and early [67]; that the edit is settled before expensive work [20]; and that the time per unit is known so the rest can be budgeted (the vertical slice's purpose [64]).

### Q8. Picture lock

**What it means.** "Picture lock is the moment in post-production when the video edit is finalized"; sound editors, colourists, effects and mastering then build on a stable cut. "Any change after picture lock creates a domino effect"; "changes to shot order, timing, or duration should be treated as an unlock"; "we recommend locking picture only after everyone ... has signed off" [63]. Changing even one frame breaks sync with music, VO and effects [63].

**Allowed after lock:** sound editing, design, ADR and mixing; score fitting to the locked cut; grade; titles and captions **in text, style and position, at equal duration**; finishing effects; mastering and delivery [63]. **Equal-frame-count swaps** of a photo or clip (a better scan, a corrected crop) keep every sync point.

**Not allowed:** adding, removing or reordering shots; changing any shot's duration by one frame; moving a cut point; changing a music or VO sync point.

**When to lock, per scenario** [J, because finishing hours scale with runtime and only about 34 hours fit the finishing weeks at 20 h/week].

| Scenario | Rolling chapter locks begin | Final picture lock |
|---|---|---|
| 12 min | Sun 2027-01-17 | **Sat 2027-02-06** (as fixed) |
| 25 min | Sun 2027-01-10 | **Sat 2027-01-30**, because 2 finishing weeks hold about 12 min of finishing at 20 h/week |
| 45 min (not planned) | Sun 2027-01-03 | Sat 2027-01-23 |
| 90 min (not planned) | n/a | n/a |

**How a team of one enforces it on itself.**
1. **Rolling chapter locks:** a chapter locks when it passes G4 and G5. Sound and grade start on locked chapters while others are still being built. This is how finishing overlaps production (the model assumes 25 percent of variable finishing happens before 02-06).
2. **A lock is a file, not a feeling:** the OTIO timeline hash, frame count and duration of each chapter are written to `chapters.csv`; `status.csv` gets `locked=1` per shot; a git tag `picture-lock-2027-02-06` is made. A validator in the repo refuses a commit that changes the duration or order of a locked shot (the playbook already uses validators at every hand-off [2]).
3. **Agents are told:** locked shots are read-only; the agent must refuse a request to change them and point to the unlock rule.
4. **Unlock rule:** a written reason, the cost in hours (what sound, score and grade passes must redo), a 24-hour wait, and only for a factual, dignity or rights error. At most two unlocks after 02-06. Any unlock adds a row to `decisions.csv`.
5. **Parking lot:** ideas after lock go in `parking-lot.md` and are read after the premiere.
6. **Fresh eyes before lock:** the stranger-read (W17 for the whole film) belongs before sound is final; the schedule puts it in the first finishing week, so a bad finding costs one unlock at most. If no stranger read is held, the cold self-read (Q7 item 7) takes that slot.

Counter-example: *Away* was made, according to a search summary of [10], without a complete script or storyboards, by one person who could review a real-time Maya playblast cheaply [10]. A solo maker with real-time rendering and no sound dependency can edit late. We cannot: our renders are shared with agents, the score is fitted to the cut, and the surprise leaves no time for a second pass.

### Q9. Render budgets: cloud versus the maker's PC versus a rented GPU

**Measured in the container (4 vCPU Xeon 2.1 GHz, 16 GB, no GPU, 24 to 28 GB free disk; 2026-10-18) [3].**

| Route | 1080p speed | Wall s per frame (4 vCPU) | Notes |
|---|---|---|---|
| Blender Workbench | 0.72 to 1.16 s per frame | about 1 | drafts |
| Blender Cycles, 24 samples + denoise | 17.4 to 19.0 s per frame | 17.5 | one lit Suzanne scene (the low end; see the next rows) |
| Blender Cycles, 'classroom' scene, 24 samples + denoise | 204.3 s (one run) | 204 | F3 (follow-up round 1); spike S3 measures the kitchen set |
| Blender Cycles, stand-in kitchen with no photographs, 64 and 128 samples + denoise | 112 s and 204 s | 112 / 204 | G2 (round 2); container only, GPU half not run |
| Blender EEVEE (software GL) | 34 to 36 s per frame | 35 | worse than Cycles here |
| Photo move, Pillow (Route B) | 7.8 fps one process (6.6 piping to x264); about 20 fps with 3 to 4 processes (ESTIMATE) | 0.13 | M21 |
| SVG/DOM scene (Route A) | 12.9 fps flat; 5.7 with wobble filter; 1.2 with full-frame grain (avoid) | 0.08 to 0.8 | M10 |
| three.js, 400 lit cubes | 3.2 to 3.5 fps | 0.3 | M9 |
| Remotion 150-frame comp | 7 fps cold, 14 warm | 0.07 to 0.14 | M13 |
| Depth-parallax (DepthFlow) | 12.3 fps at 640 x 480; about 1.8 fps at 1080p (ESTIMATE, UNVERIFIED) | about 0.55 | animated.md [4] |
| x264 CRF 18 / ProRes 422 HQ | 47 fps / 19 fps | 0.02 / 0.05 | M4, M5 |
| Baked grain overlay | 9.5 s per 10 s of film (against 32.7 s for live `noise`) | | M6 |

**Totals per scenario** (ESTIMATE from the CSV: 4 iterations for non-hero shots, 4 Workbench drafts plus 1.5 Cycles finals for hero shots; 10 percent hero shots).

| Runtime | Total frames | Hero frames | Container CPU-hours, Suzanne / classroom speed | 10-min Cycles jobs for finals, Suzanne / classroom | ProRes master | Rented 4090 GPU-hours for hero finals at 128 samples (F3) | Cash at $0.34 / $0.89 |
|---|---|---|---|---|---|---|---|
| 12 min | 17,280 | 1,728 | 18 / 153 | 76 / 883 | 7 GB | 2.2 | $0.7 / $1.9 |
| 25 min | 36,000 | 3,600 | 38 / 318 | 158 / 1,839 | 15 GB | 4.5 | $1.5 / $4.0 |
| 45 min | 64,800 | 6,480 | 68 / 572 | 284 / 3,310 | 27 GB | 8.1 | $2.8 / $7.2 |
| 90 min | 129,600 | 12,960 | 136 / 1,145 | 567 / 6,620 | 53 GB | 16.2 | $5.5 / $14.4 |

With a 5 percent hero share the Suzanne-speed CPU-hours fall to 11, 23, 41 and 83. The GPU columns use F3's classroom-scene figure for an RTX 4090 at 128 samples, 3.0 s per 1080p frame (1.6 s at 64 samples and 5.6 s at 256), in place of the old 5 s UNVERIFIED assumption; a third-party site's 3.5 to 7.5 s estimate [56] is consistent, but its settings are unstated. The cash columns are for 128 samples; the 64 and 256 sample cases are in the paragraph above and in F3.

**Dated prices.**
- RunPod, page "Updated October 8, 2026": RTX 4090 **$0.89 per hour** on the visible table and **$0.34** in the page's community-cloud metadata; RTX 5090 $1.19 / $0.69; L4 $0.59 / $0.44; A40 $0.59 / $0.35; H100 PCIe $2.89 / $1.99; volume disk $0.10 per GB-month while running. The page does not explain which rate is which tier; I used the range [54].
- Gemini API (page "Last updated 2026-10-16 UTC"): Veo 3.1 Lite $0.05 per second at 720p, Fast $0.10, Standard $0.40; Nano Banana Pro $0.134 per 1K or 2K image [55]. A 5-second clip is $0.25 to $2.00; at 4 tries per kept clip that is $1 to $8 per kept 5-second shot.
- SheepIt, a free distributed Blender render farm ("free forever", Blender 5.2 listed): the page says nothing about confidential content [57]. **Do not use it for anything that contains family imagery**; the charter requires explicit consent before personal material reaches a third party [1].
- The maker's PC is unknown. FilmCraft export estimate on 4 cores without an NVIDIA GPU: 0.25 to 1.0 CPU-seconds per 1080p frame, so 9,000 frames take 9 to 37 minutes [9] (ESTIMATE); a 12-minute film is 17,280 frames, about 18 to 72 minutes; ProRes similar. Blender on the PC depends entirely on its CPU or GPU; Exercise 1 in the playbook collects the facts [2].

**What the 10-minute limit implies.** The container's foreground command limit is 10 minutes; background commands get 30 minutes by default and up to 2 hours with `timeout`, and a reclaimed VM does not restore running jobs [3] (Q-F2 there). At 17.5 s a frame that is **34 Cycles frames (1.4 seconds of film) per foreground job** or 103 per 30-minute background job. At 204 s a frame (classroom) it is 2 frames per foreground job and 8 per 30-minute job, so the 2,592 finals need about 290 half-hour background jobs (ESTIMATE from F3 and G2). So: shard by frame range; write each frame as it finishes; skip frames that exist; keep a manifest; encode each chunk and delete its frames (loose 2 MB PNGs for a 12-minute film would be 35 GB, more than the free disk [3]). Use Workbench for drafts and send final Cycles frames of hero shots to a rented GPU only if the scene contains no family imagery. **Render hours are not the bottleneck; the maker's attention and the number of hero shots are.**

### Q10. Shot tracking: Kitsu, a spreadsheet, or plain text in the repo

| | Kitsu | Spreadsheet | **Plain text in the repo (recommended)** |
|---|---|---|---|
| Licence and cost | AGPL-3.0 [59]. Hosted: Agency €20, Production €30, Studio €35 per user per month billed annually; two-week trial on low-end hardware [58] | Excel or Sheets | free |
| Install weight | Self-host needs Ubuntu 22.04+, Python 3.12, PostgreSQL, Redis, Nginx (Meilisearch optional); recommended 2 cores and 4 GB RAM for 1 to 10 users; disk 2.5 to 3 times the uploaded files; the Docker image is "not aimed at production usage" [60] | none | none |
| Fit for one person | A production tracker built for studios (its plans cover 1 to 300 users); Blender Studio publishes its own "Blender Kitsu" pipeline add-on, listed in its site navigation [76] | fine for a human | agents read and write it directly; Git history is the audit trail |
| Privacy | previews and files live on a server (hosted or your own) | a shared Google account can leak the surprise [1] | stays in the private repo |
| Agent access | an API, but a service to run and secure | agents cannot edit without connectors | `status.csv` next to `brief.yaml`, validated by a script |

**Recommendation: plain text.** One row per shot in `shots/status.csv`, one row per chapter in `chapters.csv`, an `hours.csv` log, a `gates.csv` calendar and a `decisions.csv` ledger. They share names with the playbook: shot `LJ-C01-S014`, chapter `C01`, version `v007` with kinds `draft` and `appr`, asset `LJ-B03-0042-F`, label level `L1` to `L4c`, `cloud` level `none|preview|full`, gates G0 to G6. The columns and an example are in the Templates section; the files are in `production-scale-fixtures/`. Kitsu becomes worth reconsidering only if a second person joins and the shot count passes about 500.

---

## Exemplars and what they teach us

- ***Away* (Zilbalodis, 2019):** 75 minutes alone in 3.5 years, long takes, copied cats, 8 to 10 hours a day, 7 days a week [10]. Teaches: solo speed comes from design (few shots, one world), and the price is lifestyle. Not repeatable on a job.
- ***Sita Sings the Blues*:** one maker, 9,360 hours for 82 minutes, mixed styles, and a music-rights bill of about $50,000 negotiated down from about $220,000 [14]. Teaches: clear music early; the finishing and rights work can cost more than the animation.
- ***Flee* and *Waltz with Bashir*:** edit first, animate only what survives; a big team (10 to 12 animators, 50 to 60 at peak) for a 90-minute film [19][20]. Teaches: animatic lock before expensive work.
- ***Memoir of a Snail*:** 3 years of scripting, 5 months of storyboards, 16 weeks of preproduction, a 33-week shoot, 6 months of post [22]. Teaches: the shoot is a third of the elapsed time; pre-production is the schedule.
- ***Flow*:** 5.5 years, a team that grew from one to 15 to 20 [12]. Teaches: even a Blender, EEVEE, long-take feature by a gifted solo director became a team project.
- ***Spring* and *Sprite Fright* (Blender Studio):** 8 and 10 minutes in 1 to 1.5 years with 7 to 10 people, 100 and 220 shots [33]; the studio also publishes a Kitsu add-on [76]. Teaches: small teams with a pipeline make 0.06 to 0.08 minutes per person-month.
- **StoryCorps animated shorts:** a 13-week process for 3 minutes of interview-based animation with 6 to 8 people [31]. The nearest relative to our subject (a real voice, drawn life). Teaches: even a small broadcast team needs months per few minutes when characters are drawn; our model replaces character drawing with photographs.
- ***Tarnation* (2003):** a 91-minute feature built from decades of home footage, photos and answering-machine messages on free iMovie, for $218 in direct cost [36]. Teaches: a personal film made from existing material is cheap to produce, but the editing time was not recorded; a distributor later paid about $400,000 for sound, prints, score and clearances. Clearances, not animation, were the large cost.
- ***Air Head*:** a week, hundreds of generations, 300:1, heavy compositing [41][42]. Teaches: AI shots are cheap to start and costly to fix.
- ***Critterz*, *Copán La Leyenda*, *1776*:** what slipped, shipped badly, or drew backlash [44][46][50]. Teaches: a hosted model can disappear; "AI-finished" is not a quality tier.

---

## Templates and deliverables

All files below are in `research/production-scale-fixtures/`.

### 1. Throughput and schedule model (editable)

- `model.csv`: the full model with formulas (about 180 rows). Inputs are marked `(INPUT)`: weekly hours `H`, case 1/2/3 (Prior/Base/Stress), utilisation, shots per minute, class shares, calendar weeks, pre-holiday share, rolling-finish share, calibration multiplier `mu`, render speeds, GPU price, agent minutes; the case table; a learning-curve helper; four scenario columns (12, 25, 45, 90 minutes, editable); results; render, agent and cash; and the slice calibration block. I recalculated it in LibreOffice and checked it against an independent Python model on four parameter sets; the totals, margins and phase checks matched to the decimal.
- `schedule.csv`: weeks W1 to W19 with dates, phase, productive flag and hours at three values of `H`; totals 144.5 / 289 / 433.5.
- The formulas are in Q4; the assumptions are the case table in Q4; the results are in Q5.

**Reading the model in one line each.** Total = production side + story + gathering + reserve + finishing + one-off work. Capacity = H x 0.85 x 17. Need = total / (0.85 x 17). The post-holiday check fails when production left after the 40 percent pre-holiday cap does not fit in W12 to W16.

### 2. Runtime scenarios

Cases: Prior = the playbooks' numbers; Base = evidence-adjusted; Levers = Base with the five levers (lever 3 counted only once two quotes are recorded); Four = Base with the four levers that need no purchase; Best = Prior speeds with the structural levers. Story support from `film-story` [7]: the covert plan yields perhaps 8 to 24 scene-grade, cleared, non-hard memories.

| | 12 min | 25 min | 45 min | 90 min |
|---|---|---|---|---|
| Shots (12 per min / 8 per min) | 144 / 96 | 300 / 200 | 540 / 360 | 1,080 / 720 |
| Scene-grade memories needed [7] | about 5 | about 10 | about 18 | about 36 |
| Maker hours: Prior / Base / Levers / Best | 141 / 284 / 201 / 116 | 220 / 456 / 305 / 173 | 341 / 717 / 462 / 259 | 614 / 1,305 / 816 / 452 |
| Hours per week needed: Prior / Base / Levers / Best | 9.8 / 19.6 / 13.9 / 8.1 | 15.2 / 31.5 / 21.1 / 11.9 | 23.6 / 49.6 / 32.0 / 17.9 | 42.5 / 90.3 / 56.5 / 31.3 |
| Feasible at 10 h/week | Prior and Best only (+4 and +28 h); 9 min otherwise | no | no | no |
| Feasible at 20 h/week | Levers (+88 h) and Best (+173); Base on the edge (+5 h, post-holiday short) | Prior (+69) and Best (+116); Levers 16 h short | Best only, with a post-holiday squeeze (+30 h) | no |
| Feasible at 30 h/week | all four cases | Levers (+128), Prior (+214), Best (+261); Base 22 h short | Best only (+175); Prior is short after the holidays | no (Best 18 h short) |
| Container CPU-hours / agent-hours | 18 / 68 | 38 / 141 | 68 / 253 | 136 / 506 |
| Quality trade-off | room for 2 to 3 true hero shots per chapter and a real mix | hero share must fall to 5% or less; mix and grade outsourced; fewer re-edits; photo triage | montage and held stills; template look likely; a long list of clearances | would need a studio |
| Kill-or-cut | 2026-12-20, 2027-01-17, 2027-01-31 (Q5) | 2026-12-20, 2027-01-17 | 2026-11-15 | 2026-10-18 |
| Rolling locks / final lock | 2027-01-17 / **2027-02-06** | 2027-01-10 / 2027-01-30 | 2027-01-03 / 2027-01-23 | n/a |

The 'Hours per week needed' row is the total-hours check only. The 'Feasible at' rows, and the largest-feasible-runtime figures in Summary 2, include the post-holiday check; the Q7 slice table is the stricter, operative one.

### 3. Shot-tracking template (consistent with `agent-pipeline` naming)

`shots/status.csv` header (one row per shot; the playbook's `brief.yaml` holds the full brief, this file holds state):

```
shot_id,chapter,module,class,route,beat,target_s,actual_s,status,gate,ver,kind,inputs,cloud_max,consent,hard_flag,label_level,reuse_set,seed,maker_est_min,maker_act_min,agent_est_min,agent_act_min,render_s,render_where,rework_n,gens_tried,gens_kept,owner_next,priority,locked,updated,note
```

| Column | Allowed values and meaning |
|---|---|
| `shot_id` | `LJ-C01-S014` (pattern `^LJ-(C\d{2}|W\d)-S\d{3}$`, so wrapper shots such as `LJ-W1-S001` validate) |
| `chapter`, `module` | `C01`; `M1` module for cut order |
| `class` | `A` photo move, `B` designed graphic, `C` hero shot, `D` title or caption |
| `route` | `A` code scene, `B` photo move, `blender`, `craft` |
| `beat` | one short sentence, no names; use person IDs `P-001` |
| `status` | `idea, briefed, style_ok, drafting, draft, in_review, revise, approved, refine, final, locked, cut` |
| `gate` | last gate passed `G0` to `G6` |
| `ver`, `kind` | `v007`; `draft` or `appr` (renders are `LJ-C01-S014_v007_draft.mov`, `_v007_appr.mov`) |
| `inputs` | semicolon-separated asset IDs such as `LJ-B03-0042-F__L1` |
| `cloud_max` | `none, preview, full` (set by the maker, never by the agent) |
| `consent` | `ok, pending, na`; `hard_flag` `0, 1, HOLD` |
| `label_level` | label ladder `L1` to `L4c` [8] |
| `reuse_set` | `kitchen, street, map, clock, titles, ladder, none` |
| `seed` | the shot's integer seed (repeatable renders) |
| `maker_est_min`, `maker_act_min`, `agent_*` | estimates and actuals; actuals feed `mu` |
| `render_s`, `render_where` | CPU seconds; `container, pc, gpu, none` |
| `rework_n`, `gens_tried`, `gens_kept` | revision rounds; AI generations tried and kept (selection ratio) |
| `owner_next` | `agent, maker, craft` |
| `priority`, `locked`, `updated` | `must, should, nice`; `0` or `1`; ISO date |

Example row (synthetic): `LJ-C01-S003,C01,M1,C,blender,"hero camera move through the kitchen set, test",8.0,,drafting,G1,v001,draft,LJ-S-KITCHEN-01,none,na,0,L4a,kitchen,20261122,60,,60,,2150,container,0,,,agent,should,0,2026-11-23,"TEST ROW - delete"`.

Validator rules for an agent (a short script; not written here): IDs match the pattern; every `status` and `class` value is in the list; `approved`, `final` and `locked` need a `ver`, `kind=appr` and `gate` of `G2` or higher; `locked=1` needs `status` of `final` or `locked` and, after 2027-02-06, the target duration cannot change; no more than three consecutive class A shots in a chapter without a still, B, C, D or voice-only beat (gate G4); `cloud_max` never raised by an agent; no non-ASCII or name-like strings in `beat` and `note`.

Other files: `chapters.csv` (`chapter, module, title_code, target_s, priority, cut_order, material_in_hand_pct, status, approved_pct_of_runtime, rolling_lock_date, locked, hard_flag, note`), `hours.csv` (`date, shot_or_chapter, activity, minutes, who, note`, activities `gather|scan|story|brief_G0|style_G1|review_G2|craft_refine_G3|chapter_G4|dignity_G5|tech_G6|sound|grade|mix|captions|master|qc|admin|learn|rework`), `gates.csv` (the ten gates with dates and weekdays), `decisions.csv` (kill-or-cut ledger).

**Burn-down.** An agent computes, from `status.csv`: approved runtime = sum of `target_s` for `status` in (approved, refine, final, locked) divided by total target; compare with 45 percent on 2027-01-17 and 100 percent drafted on 2027-01-31. Selection ratio = `gens_kept / gens_tried`. Real `mu` = (sum of `maker_act_min` for done shots) / (sum of `maker_est_min` for the same shots) after the first 20 shots.

### 4. Recommended runtime, written for reconciliation with `film-story`

**Position.** Do not let feasibility quietly decide the runtime. The numbers say that runtime is a function of four things the maker controls (hero share, pacing, what to buy, when the material arrives) and one thing the maker must tell us (hours per week). `film-story`'s story argument (floor 12, target 15 with cap 18, private stretch 25, no 45 or 90 [7]) and the schedule argument agree on the shape; they differ in how safe the floor is.

| Question | Schedule answer | Story answer [7] | Reconciled |
|---|---|---|---|
| Is 90 minutes possible? | no; 42.5 h/week at Prior speed, 31 in the best case, 90 at Base | no; needs about 36 scene-grade memories against 8 to 24 | **not planned** |
| Is 45? | not under Base at 30 h/week or less; only in the best case (Prior speed, all levers) at about 30 h/week | at the top of the memory range | **not planned**; revisit as a post-premiere project |
| Is 25? | only with 21 h/week and all levers (Base), 15 at Prior speed, 12 in the best case | needs about 10 scene-grade memories; inside the range | **private cut after the premiere**, unlocked at 12-20 only if the Q7 table says it fits and the maker agrees |
| Is 15 to 18 (target and cap)? | needs about 16 to 18 h/week with levers (Base) or 29 to 33 without | needs about 6 to 7 memories | the **target** if H is 20 or more and the slice is at or below the Q7 thresholds |
| Is 12 (floor)? | needs 15.5 h/week with the four levers that need no purchase (Base; 13.9 with bought finishing), 19.6 without, 9.8 at Prior speed | needs about 5 memories | **committed** if H is about 16 or more with the four levers; otherwise the floor is 9 |

**Recommendation.** **Commit to a 12-minute public cut built as a wrapper (cold open about 1:15, ending about 1:45) and three 3:00 modules** (consistent with the film-story floor), with the levers adopted from today (hero shots at most 5 percent; 8 to 10 shots per minute; photo triage; gathering front-loaded so at least half of the chapters have material in hand by 2026-12-19; mix and grade bought only after two quotes are recorded, and until then at 2.7 hours per minute). Add one more module (15 minutes, the wrapper plus four) or two (18, the cap) as a **stretch that is unlocked, not promised, at 2026-12-20** by the Q7 table. The model's 100-second 'chapter' is the learning-curve unit, not the cut structure; seven units for 12 minutes stays valid. Treat 25 as a private cut after the premiere. Do not plan 45 or 90.

**If H is about 10:** plan **9 minutes (wrapper plus two modules)** if the slice comes in near Prior speed; otherwise add hours or buy finishing (after two quotes). 12 minutes at 10 h/week works only on Prior numbers with no slippage, no reuse program and a bought master chain. The film-story floor of 12 conflicts with this; that conflict belongs to the orchestrator, and the options are to lower the floor to 9, to buy more of the finishing, or to accept a templated look.

**If H is 30:** plan 15 to 18 minutes and keep 25 as the private cut.

**What would change this:** the slice measurement (Q7); the maker's hours (ask now); a decision to buy mix, grade, composer; the DCP decision from `theatrical-delivery`; a loss of material.

---

## Tools, services and costs (as of 2026-10-18)

| Item | Cost and terms | Date and source | Note |
|---|---|---|---|
| Cloud container | included in the Claude plan; 4 vCPU, 16 GB, 24 to 28 GB free disk | measured 2026-10-18 [3] | how much plan allowance a day of agent work uses is UNVERIFIED |
| RunPod RTX 4090 | $0.34 (community) to $0.89 (secure) per hour; volume disk $0.10 per GB-month | page "Updated October 8, 2026" [54] | tier mapping unclear on the page |
| RunPod RTX 5090 / L4 / A40 / H100 PCIe | $0.69-$1.19 / $0.44-$0.59 / $0.35-$0.59 / $1.99-$2.89 per hour | same [54] | |
| Vast.ai | dynamic, "set by supply and demand"; no numbers retrievable | page fetched, price grid empty [UNVERIFIED] | |
| Veo 3.1 Lite / Fast / Standard | $0.05 / $0.10 / $0.40 per second at 720p | Gemini pricing, "Last updated 2026-10-16 UTC" [55] | children's photos probably refused [8] |
| Veo 3.1 Lite / Fast / Standard at 1080p | $0.08 / $0.12 / $0.40 per second | same page [55], re-read 2026-10-18 | the project renders at 1080p |
| Veo 3.1 Lite / Fast / Standard at 4K | Lite not supported / $0.30 / $0.60 per second | same page [55], re-read 2026-10-18 | only if a 4K master is chosen (`theatrical-delivery`) |
| Nano Banana Pro image | $0.134 (1K/2K), $0.24 (4K) | same [55] | 2.5 Flash Image shuts down October 2, 2026 |
| SheepIt render farm | free; Blender 5.2 listed | [57] | not for family imagery |
| Kitsu hosted | €20 / €30 / €35 per user per month, billed annually; two-week trial | cg-wire pricing page, footer 2026 [58] | not recommended for one person |
| Kitsu self-host | AGPL-3.0; Ubuntu 22.04+, PostgreSQL, Redis, Nginx | [59][60] | Docker image not for production |
| DCP-o-matic | free, open source; GPU encoder Grok benchmarked at 85 to 180 fps | [61] | CPU speed not published |
| Audio post (hearsay) | "one hour per finished minute" to "six hours per linear minute"; one freelancer $100 to $150 per minute | snippet-only [68] | UNVERIFIED |
| Music rights (cautionary) | *Sita* rights holders asked about $220,000 and settled at $50,000 | [14] | `music-sound` owns this |
| Sora | consumer app dark 2026-04-26 [45]; API removed 2026-09-24 per OpenAI's deprecations page [97] (read 2026-10-18; notice given 2026-03-24) | [45][97] | route risk: a hosted video model was withdrawn with six months' notice and no replacement named |

---

## Risks, pitfalls and ethics (with mitigations)

1. **Optimism bias.** The playbook minutes are judgement, and people finish in about 1.6 times their prediction [65]. Mitigation: the Base case, the slice measurement, the 2026-12-20 gate.
2. **The first-time maker.** Chapter one takes about 2.5 times the steady state in Base (2.0 to 3.2 across cases). Mitigation: put the learning in the slice, not in the final chapters; protect weeks 5 to 9 for it; never schedule an unfamiliar technique into the last two production weeks.
3. **Holidays and calendar blindness.** W10 and W11 are dead and the jurisdiction is unknown. Examples that could add dead time: US Thanksgiving falls on Thursday 2026-11-26 (computed), Diwali 2026-11-08 and Hanukkah from the evening of 2026-12-04 to 12-12 [92][93], and Lunar New Year 2027 on Saturday 2027-02-06 [94], the same day as picture lock; Ramadan from 2027-02-08 overlaps the premiere [95]. Mitigation: ask the maker; if a family observance falls in a production week, treat that week as half.
4. **Heroes decide the schedule.** 59 percent of shot-hours are 10 percent of shots (Base). Mitigation: a hero budget in seconds per chapter (at most 6 s per minute); heroes only on reused sets; Workbench drafts first.
5. **Material arrival (the gathering lag) is calendar time, not hours.** Covert access to albums and recordings is the constraint, not scanning speed. Mitigation: a gathering plan that front-loads two or three chapters before 2026-12-20; the model's `pre_share` input.
6. **One pair of hands.** Scanning, labelling, consent notes, the lab and the review loop are all the maker. Mitigation: `gather` hours in the model (1.2 per minute in Base); batch scanning sessions; agents do manifests and checks; no second person means no second review, so use the stranger-read (W9, W17) and the 72-hour double decision for hard chapters from `film-story`.
7. **Alpha Craft apps.** Early alpha, frequent releases; failures cost days [2]. Mitigation: 10 percent risk reserve in Base; every step has a non-Craft fallback; render to new file names.
8. **Finishing crunch.** Two finishing weeks hold about 17, 34 or 51 hours at H = 10, 20, 30. Mitigation: rehearse the master chain inside the slice (50 percent of fixed finishing is pre-built in the model); roll chapter locks; buy mix and grade; decide the DCP question early.
9. **AI tool volatility.** Sora was shut down mid-production of a funded feature [44][45]. Mitigation: no shot class depends on a single hosted model; keep every generated clip, its prompt and its seed in the manifest; budget a selection ratio, not a price per clip.
10. **Privacy and consent.** Personal photos stay `cloud: none` unless the maker raises the level [2]; no family imagery to SheepIt, Kitsu cloud, or a rented GPU pod; Veo is likely to refuse photos with children [8]. Real memories stay real: AI restyles and connects, it does not invent events or faces [1].
11. **Honest labelling.** Anything generated is labelled on the ladder (`L4a` to `L4c`) in `status.csv` [8]; reconstructions are visibly stylised.
12. **Music rights can cost more than animation** (the *Sita* settlement [14]). Schedule clearance before the mix, not after.
13. **Survivorship in what we read.** Every AI hours-per-minute number I found came from a vendor, an unnamed production, or a winner. Mitigation: use only logged numbers from our own slice.
14. **The surprise.** Notifications, repo names and shared devices are the leak routes [1][2]. The schedule adds no outside collaborator; the stranger-read audiences must not be connected to her family.
15. **Feasibility must not quietly decide the runtime.** This note presents scenarios and a recommendation; `film-story` and the orchestrator reconcile in the open.

---

## Open questions / gaps

1. **Hours per week.** The model is only as good as H. Ask the maker for the number they can reliably give in each phase (and whether the holidays are really dead).
2. **Jurisdiction and observances** for 2026-11 to 2027-02 (see Risks).
3. **Measured class minutes.** All maker minutes per shot are judgement. The slice replaces them. No published source measures maker-hours for a photo-forward documentary at the theatrical bar; I found no editor or studio interview that gives hours per minute for photo-animation documentary work beyond two forum-level figures [37].
4. **AI hours per finished minute, selection ratios for image-to-video from real photographs, and the prompt/edit/fix split:** not found in any credible source. `Catacombs` (242 hours, 3,229 generations) is UNVERIFIED.
5. **Rented GPU Cycles speed on the real kitchen:** not yet measured on a GPU. F3 gives a classroom-scene table and G2 measured a stand-in on the container; measure one real hero frame in spike S3 (pass: within 2 times the table).
6. **Vast.ai prices:** the live grid did not load.
7. **The maker's PC:** CPU, RAM, GPU, free disk, Windows edition. Needed for the local render and FilmCraft export estimates (Exercise 1 in the playbook).
8. **Cash:** is there a budget to buy a mix, a grade or a composer? It is the largest lever on finishing hours. Two dated quotes are needed before lever 3 is counted (F1, G1).
9. **DCP versus a file** at the venue: `theatrical-delivery` owns it; it moves 8 to 16 fixed hours.
10. **Quality of the "theatrical bar" for a photo-forward film:** defined by `cinematic-quality` (note not yet written; its Q8 reception evidence should be added here).
11. **Whether any outside person can be the stranger-read audience** without touching the surprise; the maker has said nobody else is involved. The named substitute is the cold self-read (Q7 item 7).
12. **Whether the container's usage allowance** supports 70 to 500 agent-hours; UNVERIFIED.
13. **Week numbering:** please adopt Sunday-start weeks and dates as the authority (W12 to W16 production, W17 to W18 finishing).
14. **Which Claude plan** (Pro, Max 5x or Max 20x), and a weekly usage-bar reading before and after the slice week (F4).

---

## Sources

Project files read for this note
- [1] Life Journey Project Charter — `CHARTER.md` — 2026-10-18 — roles, principles, constraints, open decisions.
- [2] Agent-First Production Pipeline playbook — `playbooks/agent-pipeline.md` — 2026-10-18 — shot classes, minutes per shot [J], gates, validators, naming, rhythm.
- [3] Agent-first production pipeline research notes — `research/agent-pipeline.md` — 2026-10-18 — measurements M1 to M21, Q-F2 job limits.
- [4] Animated, documentary and web life-journey research — `research/animated.md` — 2026-10-18 — DepthFlow 12.3 fps at 640 x 480 (around line 614).
- [5] Delivery format playbook — `playbooks/format.md` — 2026-10-18 — 100 to 150 maker-hours for 8 to 12 minutes [J]; 6 to 10 hours per finished minute [J]; pacing guidance.
- [6] Film briefs review — `reviews/02-film-briefs-review.md` — 2026-10-18 — schedule prior, refined brief, week numbering.
- [7] Writing a biographical animated film research notes — `research/film-story.md` — 2026-10-18 — runtime recommendation, scene-grade memory counts.
- [8] AI imagery and motion research notes — `research/ai-imagery.md` — 2026-10-18 — Veo and Kling prices, children's photos, label ladder, RunPod.
- [9] ArtCraft motion and sound research notes — `research/craft-motion.md` — 2026-10-18 — FilmCraft export estimate for the maker's PC.

Benchmarks, indie films and documentaries (pages opened unless marked)
- [10] Cartoon Brew, "Yes, One Animator Made the CG Animated Feature *Away* on His Own" — https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html — 2019-06-06 — 75 min, one person, Aug 2015 to Jan 2019, Maya, 8 to 10 h a day.
- [11] Wikipedia, *Away* (2019 film) — https://en.wikipedia.org/wiki/Away_(2019_film) — read 2026-10-18 — Annecy Contrechamp, RT 100% (31), MC 78.
- [12] Blender.org, "Making Flow, interview with Gints Zilbalodis" — https://www.blender.org/?p=93732 — undated — 5.5 years, 15 to 20 people, 3 to 5 at a time, Blender and EEVEE.
- [13] Wikipedia, *Flow* (2024 film) — https://en.wikipedia.org/wiki/Flow_(2024_film) — read 2026-10-18 — 85 min, €3.5M, awards.
- [14] Wikipedia, *Sita Sings the Blues* — https://en.wikipedia.org/wiki/Sita_Sings_the_Blues — read 2026-10-18 — 82 min, $290,000, Paley's estimate of 9,360 hours, music rights $220,000 reduced to $50,000.
- [15] Wikipedia, *Rocks in My Pockets* — https://en.wikipedia.org/wiki/Rocks_in_My_Pockets — read 2026-10-18 — 88 min, 2010 script to 2014 premiere, 30,000 drawings, 28 sets.
- [16] Boston University CFA, "From Sketch to Screen" — https://www.bu.edu/cfa-magazine/2015/08/06/from-sketch-to-screen/ — 2015-08-06 — Baumane plus five assistants and interns.
- [17] Wikipedia, *My Love Affair with Marriage* — https://en.wikipedia.org/wiki/My_Love_Affair_with_Marriage — read 2026-10-18 — 108 min, 7 years, team split.
- [18] Morung Express, "60,000 drawings makes My Love Affair with Marriage" — https://morungexpress.com/60000-drawings-makes-my-love-affair-with-marriage — undated — 60,000 drawings, seven years.
- [19] Wikipedia, *Waltz with Bashir* — https://en.wikipedia.org/wiki/Waltz_with_Bashir — read 2026-10-18 — 90 min, four years, 2,300 illustrations, $1.3M.
- [20] Behind the Lens (mande.net), interview with Jonas Poher Rasmussen on *Flee* — https://mande.net/btl/crafts/direction/flee-jonas-poher-rasmussen?amp=1 — undated — 10 to 12 animators, 50 to 60 at peak, edit before animating.
- [21] Wikipedia, *Flee* (film) — https://en.wikipedia.org/wiki/Flee_(film) — read 2026-10-18 — 90 min, $3.4M, RT 98%, MC 91, awards.
- [22] Austin Chronicle, "How *Memoir of a Snail* Came Out of Its Shell" — https://www.austinchronicle.com/screens/how-memoir-of-a-snail-came-out-of-its-shell-13286572/ — undated (2025) — 3 years scripting, 5 months boards, 16 weeks preproduction, 33-week shoot, seven animators at 5 to 10 s a day, 6 months post.
- [23] Wikipedia, *Memoir of a Snail* — https://en.wikipedia.org/wiki/Memoir_of_a_Snail — read 2026-10-18 — 95 min, $4.5M, Annecy Cristal, RT 95%, MC 81.
- [24] The Blurb, *Memoir of a Snail* review — https://theblurb.com.au/wp/memoir-of-a-snail-movie-review/ — undated — seven animators, 32 weeks, 94 minutes (secondary).
- [25] *Post* magazine, "Animation: Wallace & Gromit: Vengeance Most Fowl" — https://postmagazine.com/Publications/Post-Magazine/2024/November-December-2024/Animation-I-Wallace-Gromit-Vengeance-Most-Fowl-I.aspx — Nov-Dec 2024 — 4.2 s per animator per week, up to 30 animators, shoot just over a year.
- [26] Annecy Festival, 2014 conference summaries — https://www.annecyfestival.com/about/archives/2014/meetings-2014/2014-conference-summaries/summary:100000301652 — 2014 — Laika: *Coraline* 2 to 7 s per animator per week, *Boxtrolls* 1 to 2 s.
- [27] Box Office Pro, "No Stopping LAIKA" — https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/ — undated — **snippet-only** (page returned 403): *Missing Link* target 4.3 s, real 2.5 to 3.5, 31 animators, 92 weeks.
- [28] Animator Island, "How Fast Should You Animate?" — https://www.animatorisland.com/how-fast-should-you-animate/ — undated — hearsay rates: 3D feature 3 to 4 s per week, Disney 14, TV 25 to 30.
- [29] *Motion Picture Herald* 1944-11-04 via Lantern — https://lantern.mediahist.org/catalog/motionpictureher157unse_0017 — 1944-11-04 — "Each animator, with the help of three assistants, draws 25 feet or 37>4 seconds of animation each week" (OCR text; 25 feet is about 17 s at 24 fps, so the seconds are garbled).
- [30] Wikipedia, "Limited animation" — https://en.wikipedia.org/wiki/Limited_animation — read 2026-10-18 — cycles and reused frames; *A Charlie Brown Christmas*: $76,000, four months, 30 minutes.
- [31] Storybench, StoryCorps animated shorts interview — https://www.storybench.org/?p=13125 — undated — 8 weeks animation, 13 weeks total, 6 to 8 people, 3:15 average.
- [32] Wikipedia, *Sintel* — https://en.wikipedia.org/wiki/Sintel — read 2026-10-18 — 14:48, May 2009 to Sept 2010, €400,000.
- [33] Blender Studio blog, "A big short film: Andy Goralczyk on Blender's most ambitious movie yet" — https://studio.blender.org/blog/a-big-short-film-art-director-andy-goralczyk-on-blenders-most-ambitious-movie-yet — 2021 — *Sprite Fright* about 10 min, about a year, about 10 people, about 220 shots; *Spring* 1.5 years, 7 people, about 100 shots.
- [34] Wikipedia, *Spring* (2019 film) — https://en.wikipedia.org/wiki/Spring_(2019_film) — read 2026-10-18 — 8 min; one shot took 2 to 3 weeks to animate.
- [35] Vice, "Michel Gondry turns one man's life into art" — https://vice.com/en/article/michel-gondry-turns-one-mans-life-into-art — undated — hand-drawn "over a three year period", 16 mm.
- [36] Wikipedia, *Tarnation* (2003 film) — https://en.wikipedia.org/wiki/Tarnation_(2003_film) — read 2026-10-18 — iMovie, $218.32, 91 min, $400,000 of later costs.
- [37] Adobe Community, "Animate old photos" (Rick Gerard) — https://community.adobe.com/questions-529/animate-old-photos-28461 — 2020-08-03 — hearsay: about 30 min for a simple parallax move; "easily a week" for a 4 s elaborate shot.
- [38] Stephen Follows, "How many shots are in the average movie?" — https://stephenfollows.com/many-shots-average-movie/ — undated — average 1,045 shots per film; documentary 491; ASL by genre (no documentary or animation ASL).
- [39] Cutting et al., "Quicker, faster, darker: changes in Hollywood film over 75 years" — https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/ — 2011 — no animation-specific ASL given.
- [40] Raka Creative, "How long does it take to complete a video marketing animation?" — https://rakacreative.com/blog/video-marketing/video-marketing-animation-how-to — undated — agency rule of thumb of 40 to 60 hours per minute (vendor).
- [70] VFX Voice, *Memoir of a Snail* — https://vfxvoice.com/?p=13144738 — undated — nine stages, bedroom set up for 16 weeks, shots "only five to 10 seconds long".
- [71] Skwigly, interview with Gints Zilbalodis on *Flow* — https://skwigly.co.uk/gints-zilbalodis-flow — undated — **snippet-only**: no storyboards, long camera moves worked out in 3D.
- [72] Blender Artists forum, "Professional animation workflow in Pixar, DreamWorks etc" — https://blenderartists.org/t/professional-animation-workflow-in-pixar-dreamworks-etc/1334879 — undated — **snippet-only** (not opened): unsourced claims of Pixar about 4 s and ILM 6 to 10 s per animator-week (hearsay).
- [73] Toon Boom forum, "Help: timeframes for production" — https://forums.toonboom.com/t/help-timeframes-for-production/15738 — undated — **snippet-only**: 12 to 18 s per week for hand-drawn TV; the page I opened is a forum-closure notice, so UNVERIFIED.
- [74] Animator résumé on Twine — https://www.twine.net/BeckaR — undated — **snippet-only**: about 5 s a day on a cut-out feature (hearsay).
- [75] CG Cookie forum, "time for each stage" — https://blog.cgcookie.com/?p=11052 — undated — **snippet-only** (page returned 403): "feature quality is roughly 5 seconds of finished animation a week" (hearsay).
- [76] Blender Studio, *Charge* project page — https://studio.blender.org/projects/charge/ — read 2026-10-18 — 3-minute short; site navigation lists the "Blender Kitsu" add-on.

AI-assisted projects
- [41] No Film School, "How good is Sora actually? An interview with the filmmakers behind *Air Head*" — https://nofilmschool.com/sora-ai-filmmaker-interview — 2024 — "a little over a week", 20 s generations with 2 to 3 s used, VFX and grading.
- [42] heise, "Sora's Air Head: plenty of human post-processing" — https://heise.de/-9707198 — 2024 — "assumes a ratio of 300:1"; post steps.
- [43] The Decoder, "OpenAI backs Critterz" — https://the-decoder.com/openai-backs-critterz-to-show-generative-ai-can-deliver-on-the-big-screen/ — 2025-09-08 — about nine months, under $30M, about 30 people.
- [44] Forbes via Yahoo, "Why Critterz is the real test of AI filmmaking" — https://www.yahoo.com/entertainment/movies/articles/why-critterz-real-test-ai-212613673.html — updated 2026-05-26 — Q1 2027 target, Sora discontinued, first-look footage at the Cannes market.
- [45] The Next Web, "Sora shutdown leaves Critterz at the Cannes market without its model" — https://thenextweb.com/news/critterz-misses-cannes-openai-sora-shutdown — 2026-05-22 — Sora app dark 2026-04-26, API scheduled for 2026-09-24, in-festival slot missed.
- [46] Wikipedia, *Copán La Leyenda* — https://en.wikipedia.org/wiki/Cop%C3%A1n_La_Leyenda — read 2026-10-18 — 74 min, 15 years of development, panned.
- [47] invideo, "How many AI video generations do you need per usable shot?" — https://invideo.io/faq/how-many-ai-video-generations-do-you-need-per-usable/ — undated — vendor numbers (3 per usable shot, 25% kept, $315 to $750 per minute).
- [48] MindStudio, "How to use AI for one-person short film production" — https://www.mindstudio.ai/blog/ai-one-person-short-film-production-workflow — undated — generic estimates, no named production.
- [49] Google blog, "Dear Upstairs Neighbors" — https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/ — January 2026 — workflow, "none of our final shots ... one-click".
- [50] The Playlist, "On This Day... 1776 trailer" — https://theplaylist.net/on-this-day-1776-trailer-darren-aronofskys-ai-animated-revolution-series-drops-and-the-backlash-arrives-right-on-schedule-20260130/ — 2026-01-30 — backlash.
- [51] Creative Bloq, "A director generated 3,229 AI shots to make one film" — https://www.creativebloq.com/ai/how-a-filmmaker-turned-a-10-year-old-unmakeable-movie-idea-into-reality-with-ai — undated — **snippet-only** (page returned an unrelated headline); UNVERIFIED.
- [52] CO/AI, "Netflix deploys AI to create visual effects 10x faster for The Eternaut" — https://getcoai.com/news/netflix-deploys-ai-to-create-visual-effects-10x-faster-for-the-eternauts — 2025 — **snippet-only**; co-CEO's own claim.
- [53] NewsLab, on Jacob Adler and Runway's festival — https://newslab.org/?p=6461 — 2025 — **snippet-only**: *Total Pixel Space*, 9:28, about 6,000 submissions.

Tools, prices and process
- [54] RunPod pricing — https://www.runpod.io/pricing — "Updated October 8, 2026" — GPU rates and storage.
- [55] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing — "Last updated 2026-10-16 UTC" — Veo 3.1 and image prices.
- [56] Renderjuice RTX 4090 comparison — https://www.renderjuice.com/gpus/compare/rtx-4090-vs-rtx-5050 — "Checked Oct 14, 2026" — estimated 3.5 to 7.5 s per frame on three benchmark scenes (Blender 5.2.0).
- [57] SheepIt Render Farm — https://www.sheepit-renderfarm.com/ — read 2026-10-18 — free distributed Blender farm; no confidentiality statement.
- [58] CGWire Kitsu pricing — https://www.cg-wire.com/pricing — footer 2026 — hosted plan prices.
- [59] GitHub, cgwire/kitsu — https://github.com/cgwire/kitsu — read 2026-10-18 — AGPL-3.0.
- [60] Zou documentation — https://zou.cg-wire.com/ — undated — self-host prerequisites and hardware guidance.
- [61] DCP-o-matic speed page — https://dcpomatic.com/learn-more-speed — undated — Grok GPU benchmarks.
- [62] iZotope, "Tips for mixing short films" — https://www.izotope.com/community/blog/tips-for-mixing-short-films — undated — "double it"; add days.
- [63] ECG Productions, "What is picture lock and why does it matter?" — https://www.ecgprod.com/what-is-picture-lock-why-does-it-matter — undated — definition, effects of change.
- [64] Unity Learn, "Production and post-release" — https://learn.unity.com/course/game-development-in-a-nutshell/tutorial/production-and-post-release — undated — vertical slice definition.
- [65] Wikipedia, "Planning fallacy" — https://en.wikipedia.org/wiki/Planning_fallacy — read 2026-10-18 — thesis study 33.9 predicted, 55.5 actual days.
- [66] Wikipedia, "Learning curve" — https://en.wikipedia.org/wiki/Learning_curve — read 2026-10-18 — Wright's law, 80 percent curve.
- [67] PremiumBeat, "A masterclass in making a Pixar animated short" — https://www.premiumbeat.com/blog/a-masterclass-in-making-a-pixar-animated-short — undated — look tests "super quick and dirty, just with a few days of work".
- [68] Indietalk and ZHdK audio-post pages — https://indietalk.com/goto/post?id=348469 and https://medienarchiv.zhdk.ch/files/f693e5ef-5249-491e-8bfa-ae379306539a?lang=en — undated — **snippet-only** (both returned errors): "one hour per finished minute", "six hours per linear minute".
- [69] arXiv 2604.03315, "StoryBlender" — https://arxiv.org/pdf/2604.03315 — 2026 — **snippet-only**: shared asset library cut model builds by about 12%.


---

## Follow-up research (round 1)

*Researcher: Sonnet, 2026-10-18 (Sunday, week 1 of 19). Answers five open items from the playbook. Labels as above: **ESTIMATE** is arithmetic on sourced numbers, **UNVERIFIED** is not checked, **[J]** is judgement. Source numbers continue from [76]; the list is at the end of this section.*

**Limits of this round, stated up front.** The shared web-search budget ran out (200 searches per turn across all agents) before I reached the mix and grade quotes. After that I used only direct fetches of pages I already knew by address. That is why F1 has captions prices but no mix or grade quote. Nothing here is a guessed URL that I cite. Failed fetches are listed in F1.

### F0. What the maker has now told us (relayed request)

- **Who is in on the secret: only the maker.** The maker is the only person on the project, and for now also the only person who can approve hard chapters for her. The maker said this can wait until the plan is ready, so no second approver is being recruited yet.
- Effect on the schedule model: open question 11 (an outside stranger-read audience) stays closed. There is no second pair of eyes at the G-SLICE stranger read or on hard chapters, so the maker's own decisions are the only check, with the Fable advisor flagging sensitive material. That is a risk to record, not a number to change.
- **Still open, not answered:** hours per week per phase (H); whether the holiday weeks are dead or the maker's freest fortnight; country and observances; the PC's CPU, RAM, GPU and free disk. The playbook's Exercise 1 and the PowerShell lines in `playbooks/craft-visual.md` already collect the PC facts in about two minutes. The dated calendar in F5 lets the maker answer the observance question with yes or no.

### F1. What does buying the mix, grade and captions cost in 2026?

**Result: captions priced from two pages I read. Mix and grade: no quote obtained, so the Decision 4 cash figure stays UNVERIFIED.**

*Captions (a 12 to 18 minute film), prices seen on 2026-10-18:*

| Vendor and service | Price seen | Turnaround stated | 12 min | 18 min | Source |
|---|---|---|---|---|---|
| Rev, human-made captions | "Starting at $1.99/min"; English and Spanish only | "delivered in 12 hours or less" | $23.88 | $35.82 | [77] |
| HappyScribe, human-made subtitles | "From $2.00/min" ($1.90/min on its Business plan) | "Delivery in 4h+" | $24.00 | $36.00 | [78] |
| HappyScribe, machine subtitles | credits at "$0.20/min" | not stated | $2.40 | $3.60 | [78] |
| DaVinci Resolve (free) or a local speech-to-text tool | $0 cash; the maker's review time | none | $0 | $0 | [79] |

Both pages carry no visible date. HappyScribe's page data says it was modified 2026-10-13 [78]; Rev's page shows none [77]. Both prices are list prices for a transcript-to-captions job, not a quote for a particular film. They are small enough not to matter: **captions cost about $25 to $36 bought, or nothing if done by the maker.** Do not treat captions as a finishing hours problem beyond review time (the Base figure of 0.3 h per minute is review, not typing) [J].

*Mix and grade:* I did not find a rate card or quote that I saw with my own eyes. Pages tried and what they gave:

- Fiverr audio mixing category: HTTP 403. Upwork audio-mixing cost page: HTTP 403. ProductionHub: HTTP 403.
- SoundBetter home page: category links only, no prices on the part I could read.
- PeopleperHour: empty page. Freelancer colorist page: 404. StudioBinder cost article (guessed address): 404. BECTU rates page (guessed address): 404.
- Color Grading Central: no prices published.

Hearsay already in the note stays hearsay: one freelancer at $150 per minute for post mixing and $100 per minute for dialogue editing (snippet-only, earlier round) [68]. Do not use it as a quote.

*What I can state about the cash floor:* DaVinci Resolve's free version lists edit, colour, VFX, motion graphics and audio (Fairlight) in one app; Resolve Studio is "$295" with "Resolve 21" and a 2026 copyright notice on the page [79]. So a do-it-yourself mix and grade costs $0 to $295 in cash. The cost is the maker's hours, at the Base 2.7 hours per finished minute (grade 0.5, mix 1.5, captions 0.3, QC 0.4) plus 24 fixed hours.

*What to do with this:*

1. **Do not adopt lever 3 (buy mix, grade and captions) in the model until two quotes are in hand.** Until then run the model with finishing at 2.7 h/min (Base), not 0.8. If the quotes arrive, set it to 0.8 plus the maker's review time.
2. **Ask for quotes at the G-READY week (Sun 15 Nov), not at picture lock.** The slice (G-SLICE, Sun 20 Dec) already needs a mix, a grade and captions on the slice (C01), so one vendor can price the slice and the full film together.
3. **Request for quote, five lines, with no personal detail** (the project is covert; call it "a 15-minute documentary short, animated"): runtime 12 to 18 min; stereo mix from supplied stems (voice, music, effects) to a stated loudness; grade of a finished animated picture to a stated delivery (ProRes or DCP-ready); captions as a file or burned in; fixed price with two revision rounds; turnaround in working days **from picture lock on Sat 6 Feb 2027**, with the premiere on Sat 27 Feb. The finishing weeks are 7 to 20 Feb, so anything over about 10 working days including revisions does not fit.
4. Ask three vendors. Record each as: date seen, quoted price, turnaround, what is excluded. Add them as sources [97] onward in the next round.

*Owner:* `music-sound` and `theatrical-delivery` own the mix and delivery spec; `production-scale` only consumes the number.

### F2. Veo 3.1 image-to-video on a photo with a child

**Result: I could not run the test. The documents point to a refusal. Status stays UNVERIFIED.**

- **Why no test:** this session has no Gemini or Vertex access (I checked the environment variable names for Gemini, Google, Veo, RunPod and Vast and none were set) and the maker has not approved a spend. The `ai-imagery` note also says "No test planned" (its Q4), so the two notes disagree on whether a test is wanted; see the recommendation below.
- **What the documents say (re-read 2026-10-18, two independent reads, same result as `ai-imagery`):**
  - Gemini API Veo page: for Veo 3.1, Veo 3.1 Fast, Veo 3.1 Lite, Veo 3 and Veo 3 Fast, `personGeneration` for **image-to-video, interpolation and reference images is `allow_adult` only**; text-to-video is `allow_all` only. No default is stated. The page says nothing about children or minors. Per-model "Latest update" dates: 3.1 and 3.1 Fast January 2026, 3.1 Lite March 2026 [80].
  - Vertex AI responsible-AI page, "Last updated 2026-10-15 UTC": the **Child** category "Rejects requests to generate content depicting children if `personGeneration` isn't set to `"allow_all"` or if the project isn't on the allowlist for this feature." Support codes **58061214** and **17301594**. The page says its filters "aim to filter out input images and videos" that violate its policies and gives a sample message: "Veo could not generate videos because the input image violates Agent Platform's usage guidelines." It does not say what happens to an input image that contains a child [81].
- **Reading across (M, UNVERIFIED):** image-to-video can only run at `allow_adult`, and the child category rejects when the setting is not `allow_all`. So a photo that shows a child is most likely **refused**, not quietly altered. The Gemini API page does not confirm this for its own product.
- **Decision for class A childhood shots:** plan as if cloud image-to-video is **not available** for any photo with a child. Use depth-parallax, camera moves on stills, or local models. The plan has this fallback already, so nothing waits on the test.
- **Recommendation:** run the test only if the maker wants cloud image-to-video for childhood shots anyway. It is cheap: Veo 3.1 Lite is $0.05 per second at 720p [55], so a 4 second clip is $0.20, and three clips are $0.60. Use **public-domain photos only, never a family photo**: (a) a public-domain photo of a child, (b) a public-domain adult portrait as control, (c) a landscape or object as control. `ai-imagery` already lists one in its note: US National Archives item 546220, a 1972 EPA photograph that shows children. Record per clip: accepted or blocked, the support code or message, any charge, and whether faces or ages changed. If (a) is blocked, close the item. If (a) is accepted and faithful, still do not send a family photo without the maker's explicit say (charter, constraints). Delete every generated clip from the test; a generated video of a real child's photograph, public domain or not, is never kept or reused.

### F3. Cycles seconds per frame on an RTX 4090

**Result: the 5 second assumption is inside the measured range. I could not rent a GPU, so this is derived from the community benchmark, not a run on the maker's scene.**

*Method.* I downloaded the Blender Open Data daily snapshot (file dated Sun 18 Oct 2026 00:01:21 GMT, 101,626,337 bytes; licence Creative Commons 0 per the archive's own README and LICENSE [99] and the Download page [98]) [83] and filtered to records whose only compute device is "NVIDIA GeForce RTX 4090" (not Laptop, not "D"), device type OptiX, Blender 5.2.0 LTS: 81 runs per scene, dated 2026-07-20 to 2026-10-15. The benchmark script (version 3.1.2) renders each scene for a **fixed 30 seconds** with adaptive sampling off and counts samples, so the score is **samples per minute, with no denoising** [82][84]. I opened the three scene files with `bpy` 5.2.0 (installed from PyPI) to read their settings [84]. Scripts and outputs are saved in `research/production-scale-fixtures/followup1-*`.

| Scene (Blender Studio benchmark) | Frame | Triangles (approx.) | 4090 samples per minute: median (p10 to p90) | Seconds per sample at its own size | Seconds per sample at 1080p (computed) |
|---|---|---|---|---|---|
| classroom | 1920 x 1080 | 241,000 | 2,881 (2,615 to 2,983) | 0.0208 | 0.0208 |
| junkshop | 2000 x 1000 | 3,149,000 | 3,549 (3,196 to 3,713) | 0.0169 | 0.0175 |
| monster | 1024 x 1024 | 1,602,000 | 5,184 (4,735 to 5,394) | 0.0116 | 0.0229 |

*Seconds per frame for the same three scenes, computed* (samples times 1080p seconds per sample; the spread is the scenes' spread; add about 10 percent for a slower rented card, since the p10 runs are about 9 to 10 percent below the median):

| Samples | 1080p | 2K DCI 2048 x 1080 | 4K UHD 3840 x 2160 |
|---|---|---|---|
| 24 | 0.4 to 0.6 s | 0.5 to 0.6 s | 1.7 to 2.2 s |
| 64 | 1.1 to 1.5 s | 1.2 to 1.6 s | 4.5 to 5.9 s |
| 128 | 2.2 to 2.9 s | 2.4 to 3.1 s | 9.0 to 11.7 s |
| 256 | 4.5 to 5.9 s | 4.8 to 6.3 s | 18.0 to 23.4 s |
| 512 | 9.0 to 11.7 s | 9.6 to 12.5 s | 35.9 to 46.9 s |

*What is not in these numbers:* denoising (a fraction of a second at 1080p on a GPU; not measured, UNVERIFIED); scene load and BVH build, which the benchmark reports as 0.6 s (classroom), 0.8 s (monster) and 2.6 s (junkshop) per run (median of total minus sampling time) and which you pay once per Blender process, not per frame, if one process renders a range; pod start-up, Blender install and file transfer; and the maker's own scenes, which are probably simpler than these three (the benchmark's own scenes are interiors and creatures, not stylised or voxel looks) [J].

*Reading it.* The old 5 second assumption equals about **220 to 290 samples at 1080p**, or **64 samples at 4K**. The third-party estimate of 3.5 to 7.5 seconds [56] is consistent with that, though its settings are still unstated. A hero frame at 128 samples and 1080p is about 3 seconds including a guessed 0.3 second denoise.

*Container cross-check.* I rendered the classroom scene on this container (4 vCPU, no GPU) at 1080p, one run each: 8 samples 63.9 s; 24 samples 176.0 s; 24 samples plus denoise 204.3 s. That is about 7.0 s per sample and about 28 s of CPU denoise. The 4090 median is 0.0208 s per sample on the same scene, **about 336 times faster** (ESTIMATE from single runs). The earlier 17.5 s per frame figure was a one-light Suzanne scene, which is why a real scene is far slower on CPU: a classroom-class hero frame at 24 samples plus denoise is 204 s on this container, so 2,592 such frames would take about 147 CPU-hours. **A Cycles hero plan needs a GPU: the maker's own, or a rented one.**

*Updated GPU budget for the 12 minute film* (2,592 hero final frames = 1,728 hero frames at 1.5 finals each, from Q9; classroom-class scene at 1080p; 0.3 s guessed denoise; RunPod $0.34 to $0.89 an hour [54]):

| Samples | Seconds per frame | GPU-hours | Cash |
|---|---|---|---|
| 64 | 1.6 | 1.2 | $0.4 to $1.0 |
| 128 | 3.0 | 2.2 | $0.7 to $1.9 |
| 256 | 5.6 | 4.0 | $1.4 to $3.6 |
| 512 | 11.0 | 7.9 | $2.7 to $7.0 |

For scale, rendering all 17,280 frames of the 12 minute film with Cycles at 128 samples would be about 14 GPU-hours, roughly $5 to $13 (ESTIMATE). **Render cash is not a constraint at any runtime in the note.** The constraints are the privacy rule (a rented GPU is a third party; a scene that uses her photos as textures counts as family imagery and needs the maker's explicit say) and the maker's time to set up the pod. If neither the maker's PC nor a rented GPU is allowed, hero shots must use Workbench, EEVEE or 2D routes.

*What spike S3 now has to prove.* It no longer has to discover the speed. It passes if one real hero frame on a rented or maker-owned GPU lands **within 2 times** of the table above for its samples and size, and the notes record: pod start to first frame, per-process load time, denoise time, bytes transferred. That is the number that replaces "UNVERIFIED" in the playbook. Cost of the spike: under $1 of GPU time.

### F4. Does the Claude plan cover 70 to 140 supervised agent-hours over 17 weeks?

**Result: cannot be settled from published numbers. UNVERIFIED. The plan limits are counted in tokens in rolling windows, not in hours, and Anthropic's pages give no hours figure.**

What the pages say (all read 2026-10-18):

- **Prices:** Pro $20 a month ($17 on annual billing, "$200 billed up front"); Max "From $100" a month, in a 5x or 20x choice "more usage than Pro" [85]; the Max article gives Max 5x $100 and Max 20x $200 a month [86]. "Price and plans are subject to change" [85].
- **Limits:** "Both Pro and Max plans have a five-hour session limit and a weekly limit." Claude and Claude Code draw from the same limits [87]. Max also has a separate weekly limit for the Fable model [87][85]. No page I read gives hours or prompts per week.
- **What uses more:** longer conversations, tool use and "multi-step tasks, like running code, creating files, or browsing websites" [88]. Subagents and workflows "send their own requests on top of the main conversation's" [90]. A workflow "can use meaningfully more tokens" than the same task in conversation, and "runs count toward your plan's usage and rate limits" [91]. Agent teams use "approximately 7x more tokens than standard sessions" [90], a figure the page gives "when teammates run in plan mode".
- **A sign that Pro is tight for fan-out work:** the default workflow size is "medium, or small when you're signed in on a Pro plan", where small means fewer than 5 agents [91].
- **What happens at the limit:** work pauses until the window resets (a workflow run waits if the limit resets within 24 hours and the session is interactive; a weekly limit can be further out) [91]. Or the maker turns on **usage credits**, which are "billed at standard API rates", with a monthly spend limit the maker sets, and apply to Claude Code [89].
- **Dollar scale:** Anthropic's own cost page says the average is about **$13 per developer per active day** and **$150 to $250 per developer per month**, below $30 per active day for 90 percent of users (enterprise deployments, API list prices) [90].

*Rough bound on the overflow cost (ESTIMATE, low confidence).* Take 70 to 140 supervised hours. If an active day is about 5 hours [J], that is 14 to 28 active days. At $13 a day that is about $180 to $360; at the $30 ninety-percent ceiling, about $420 to $840. Compare Max 5x at $100 a month for the 4.3 months to 27 Feb, about $430. So **if the plan covers none of it, the usage-credit overflow is in the same range as a Max 5x subscription**, not a thousand-dollar problem. This does not count fan-out waves such as the 16-track learn phase, which are far heavier than a supervised session.

*What this changes.*

1. **Agent-hours are not yet a constraint, but they could become one in specific weeks.** The risk is not the 70 to 140 supervised hours; it is the parallel waves (research, shot generation batches, review passes). Plan those as bursts, and check the usage bars before and after each.
2. **The unit should be a plan-percentage, not hours.** Record the weekly usage bar (Settings > Usage on claude.ai, or `/usage` in Claude Code, which also shows what share went to subagents) before and after the G-SLICE week and each build week [88][90]. After two weeks the maker has a real figure.
3. **Ask the maker which plan this is** (Pro, Max 5x or Max 20x). Nothing in the project files says. If it is Pro, plan on a Max 5x upgrade for the 17 weeks, or usage credits with a monthly cap, and keep workflow size at "small" or "medium".
4. The charter's cloud-first choice means the **Claude plan is the real engine budget**; the render cash above is trivial next to it.

### F5. From the maker: still open, with the dated calendar to make the answer easy

Only the maker can supply H per phase, the holiday-week answer, the country, and the PC facts. I can supply the calendar. All dates below are for 2026-11 to 2027-02. Weekdays and the two computed holidays are my arithmetic; the rest are from the sources.

| Date | What | Weekday | Note | Source |
|---|---|---|---|---|
| 2026-11-08 | Diwali main day (Lakshmi Puja); festival runs 6 to 10 Nov | Sunday | Wikipedia lists "8 (Lakshmi Puja...)" | [92] |
| 2026-11-26 | US Thanksgiving | Thursday | fourth Thursday of November (computed) | none |
| 2026-12-04 evening to 2026-12-12 | Hanukkah | Fri to Sat | "Sunset, 4 December - nightfall, 12 December" | [93] |
| 2026-12-20 | Planned G-SLICE | Sunday | five days before Christmas | playbook |
| 2026-12-25 | Christmas Day | Friday | computed | none |
| 2027-01-01 | New Year's Day | Friday | computed | none |
| 2027-02-06 | Lunar (Chinese) New Year, year of the Goat | Saturday | **same day as picture lock** | [94] |
| 2027-02-08 to 2027-03-08 | Ramadan (Umm al-Qura calendar; local moon sighting can move it by about a day) | Mon to Mon | **the Sat 27 Feb premiere falls on about day 20 of Ramadan**, so an evening screening at a mostly public gathering would need to follow sunset and iftar if the audience observes it | [95] |
| 2027-02-10 | Ash Wednesday, start of Lent | Wednesday | Easter 28 March 2027 is computed from the page's "46 days before Easter" rule | [96] |
| 2027-02-27 | Premiere | Saturday | | charter |

Questions that would settle it: Which of these does the household or the expected audience observe? Is the holiday fortnight (about 20 Dec to 3 Jan) free time or family time? Which country, and what hours a week can be given in each of: Nov (learning, slice), Dec (slice), Jan (production), Feb (finishing)?

### Impact summary (for the orchestrator and scribe)

1. **Finishing cash (Decision 4):** captions $25 to $36 or free [77][78]; mix and grade quotes not found. Keep finishing at 2.7 h/min until two quotes are seen; ask at G-READY.
2. **Veo and childhood photos:** documents say refusal is likely; not tested [80][81]. Keep parallax or local for class A. Optional $0.60 test with public-domain photos only.
3. **Render budget:** the 5 s per hero frame assumption is inside a derived 2 to 6 s range at 1080p (128 to 256 samples) for a 4090 [82][83][84]. Cash for the 12 minute film is $0.4 to $7 for hero finals. The real constraint is the privacy rule and a GPU being available at all.
4. **Claude plan:** the unit is tokens in 5-hour and weekly windows. No published hours. Overflow at API rates is roughly a Max 5x subscription in size. Ask the maker for the plan; record usage-bar readings each week [85][86][87][88][89][90][91].
5. **Calendar:** Ramadan overlaps the premiere; Lunar New Year is picture-lock day. Ask the maker about observances before the schedule is finalised [94][95].
6. **Sole maker:** confirmed for now; no second approver or outside reader.

### Sources added in round 1

Captions, mix and grade
- [77] Rev pricing — https://www.rev.com/pricing — read 2026-10-18, page undated — human captions "Starting at $1.99/min", "delivered in 12 hours or less", English and Spanish only; AI captions are bundled in monthly plan minutes.
- [78] HappyScribe pricing — https://www.happyscribe.com/pricing — read 2026-10-18; page data dateModified 2026-10-13 — human subtitles "From $2.00/min" (Business $1.90), "Delivery in 4h+"; machine credits "$0.20/min".
- [79] Blackmagic Design, DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — read 2026-10-18, no pricing date, copyright 2026, "DaVinci Resolve 21" — free version with edit, colour, VFX, motion graphics and audio; Studio "$295"; Fairlight audio.

Veo
- [80] Gemini API, Veo — https://ai.google.dev/gemini-api/docs/veo — read 2026-10-18 (same page as `ai-imagery` [114]) — `personGeneration` by model and mode, Limitations, model update dates.
- [81] Vertex AI, Responsible AI for Veo — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines — "Last updated 2026-10-15 UTC" (same page as `ai-imagery` [116]; the text sits after a 100,000 character navigation block) — Child category and support codes, input-image message.

Cycles
- [82] Blender Open Data, About — https://opendata.blender.org/about/ — read 2026-10-18 — score definition (samples per minute, summed over scenes), snapshot address.
- [83] Blender Open Data daily snapshot — https://opendata.blender.org/snapshots/opendata-latest.zip — Last-Modified Sun, 18 Oct 2026 00:01:21 GMT, 101,626,337 bytes, Creative Commons 0 (the licence text is inside the archive, see [99]; the About page [82] states no licence) — analysed locally; 433,541 records; RTX 4090 OptiX rows used.
- [84] Blender Benchmark 2.0 files (the open-data CDN address redirects here) — https://mirrors.ocf.berkeley.edu/blender/release/BlenderBenchmark2.0/ — read 2026-10-18 — scenes classroom (65.2 MiB), junkshop (336.2 MiB), monster (73.0 MiB), script version 3.1.2 (listed 2026-Mar-11); script sets samples to 1<<24, time limit 30 s, adaptive sampling off.

Claude plan
- [85] Claude pricing — https://claude.com/pricing — read 2026-10-18, no date — Pro $17 and $20, Max from $100, 5x or 20x, paid plans add weekly limits.
- [86] Claude Help Center, "What is the Max plan?" — https://support.claude.com/en/articles/11049741-what-is-the-max-plan — "Updated this week" — Max 5x $100, 20x $200, five-hour and weekly limits.
- [87] Claude Help Center, "Using Claude Code with your Pro or Max plan" — https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan — "Updated this week" — shared limits, session and weekly limits, Fable weekly limit on Max.
- [88] Claude Help Center, "Usage limit best practices" — https://support.claude.com/en/articles/9797557-usage-limit-best-practices — "Updated over 3 weeks ago" — what consumes usage; progress bars under Settings > Usage.
- [89] Claude Help Center, "Extra usage for paid Claude plans" — https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans — read 2026-10-18 — usage credits "billed at standard API rates", monthly limit, applies to Claude Code.
- [90] Claude Code docs, "Manage costs effectively" — https://code.claude.com/docs/en/costs — read 2026-10-18 — about $13 per developer per active day, $150 to $250 per month, below $30 for 90 percent; agent teams about 7x tokens; `/usage` breakdown.
- [91] Claude Code docs, "Orchestrate subagents at scale with dynamic workflows" — https://code.claude.com/docs/en/workflows — read 2026-10-18 — cost section, size guideline default (small on Pro), usage-limit wait.

Calendar
- [92] Wikipedia, Diwali — https://en.wikipedia.org/wiki/Diwali — read 2026-10-18 — 2026 dates 6 to 10 November.
- [93] Wikipedia, Hanukkah — https://en.wikipedia.org/wiki/Hanukkah — read 2026-10-18 — 2026: sunset 4 December to nightfall 12 December.
- [94] Wikipedia, Chinese New Year — https://en.wikipedia.org/wiki/Chinese_New_Year — read 2026-10-18 — 2027: Saturday 6 February, Goat.
- [95] Wikipedia, Ramadan — https://en.wikipedia.org/wiki/Ramadan — read 2026-10-18 — Umm al-Qura table: 2027 from 8 February to 8 March; moon-sighting caveat.
- [96] Wikipedia, Ash Wednesday — https://en.wikipedia.org/wiki/Ash_Wednesday — read 2026-10-18 — 2027: 10 February.

*Fixtures saved:* `research/production-scale-fixtures/followup1-rtx4090-benchmark-summary.py` and `.txt`, `followup1-read-benchmark-scene.py`, `followup1-classroom-cpu-timing.py` and `.txt`.


## Follow-up research (round 2)

*Researcher: Sonnet, 2026-10-18 (Sunday, week 1 of 19). Answers the six items left open after round 1. Labels as before: **ESTIMATE** is arithmetic on sourced or measured numbers, **UNVERIFIED** is not checked, **[J]** is judgement. Source numbers continue from [96]; the list is at the end of this section.*

**Limits of this round, stated up front.**
1. The shared web-search budget was already spent when this round began (the search tool answered that its budget was used up). Everything below comes from direct fetches of pages I could name by address, plus local measurement. I did not search by any other route. Nothing guessed is cited; pages that failed are listed in G1.
2. The container has no GPU and no GPU rental has been approved, so the GPU half of spike S3 was **not run**. The container's environment holds cloud credentials that were set up for the sandbox, not by the maker for this project. I did not use them.
3. I sent no email to any vendor. The request for quote (RFQ) is written out in G1 for the maker to send.

| Item | Result | Status |
|---|---|---|
| G1 Mix and grade quotes | 0 of 3 dated quotes. No published rate card found; the one marketplace I could read quotes per project [101][102]. RFQ and quote log ready. | OPEN. Lever 3 stays OFF (needs 2 recorded). |
| G2 Spike S3 on the kitchen | Container CPU measured on a **stand-in** kitchen (the real set does not exist yet): about 112 s per frame at 64 samples and 204 s at 128 (1080p, denoised). GPU half not run. | PART DONE. Container Cycles finals are viable for a few hundred frames, not for the planned hero share. |
| G3 From the maker | Nothing new received. One-message answer sheet below. | OPEN |
| G4 film-story 12-minute shape | One answer: cold open 1:15, three modules of 3:00, ending 1:45. Patch list below. | CLOSED (scribe to patch) |
| G5 Sora API | OpenAI's own deprecations page lists the Videos API and the sora-2 models with a shutdown date of 2026-09-24, under Past deprecations [97]. | CLOSED |
| G6 CC0 for the Blender snapshot | On the Download page under Raw Data, License [98], and in README.txt and LICENSE.txt inside the zip [99]. | CLOSED |

### G1. Mix and grade quotes (owners: `music-sound` and `theatrical-delivery`; `production-scale` only consumes the number)

**Result: none obtained. Decision 4 cash stays UNVERIFIED. Lever 3 (buy mix, grade, captions) stays OFF, because it switches on only when two quotes are recorded and zero are.**

*What I tried on 2026-10-18 (direct fetches only):*

| Page | Result |
|---|---|
| SoundBetter home page | No prices in the part I could read (the first 100,000 of 472,675 characters). Links to "Mixing Engineers" and "Mastering Engineers" [101] |
| SoundBetter, Mixing Engineers listing | No prices. One profile says "Inquire for rates on Recording, Mixing, Mastering and more...". Menus list Post Mixing and Dialogue Editing. The home page navigation offers "Post a job" and "Create a Project" [101], so quotes are per project (inference) [102] |
| Thumbtack video colour grading and audio mixing cost pages (addresses guessed) | pages returned no content |
| PremiumBeat and StudioBinder colour-grading cost articles (addresses guessed) | 404 |
| Fiverr video colour grading category | 403 |

The round-1 failures (Fiverr audio, Upwork, ProductionHub: 403; PeopleperHour, Freelancer, StudioBinder, BECTU guesses: empty or 404) still stand. The "$100 to $150 a minute" freelancer figure stays hearsay [68]. Rate cards for film audio post and colour grading are mostly "on request", so **the only way to get a dated quote is to ask**.

*What the quotes must fit (dates from the roadmap and F1):* picture lock Sat 6 Feb 2027; mix 6 to 12 Feb; mix v1 and grade v1 on every locked chapter in week 17 (8 to 14 Feb); master verified Sat 20 Feb; premiere Sat 27 Feb. From Mon 8 Feb to Fri 19 Feb there are 10 working days (computed). So: **first version back in 5 working days (by Fri 12 Feb), final including two revision rounds by Fri 19 Feb.** Lunar New Year falls on lock day (Sat 6 Feb) [94] and US Presidents' Day is Mon 15 Feb (computed, third Monday of February), so ask each vendor about both.

*The five-line RFQ (no names, no personal detail, no family detail; the film is "an animated documentary short"). Send the same text to three vendors:*

1. Job: a 12 to 18 minute animated documentary short in English, for one public screening on Sat 27 Feb 2027. Please quote two prices separately: (a) a stereo mix and (b) a colour grade.
2. Mix (a): stereo, 48 kHz, 24-bit, from supplied stems (voice, music, effects, ambience); venue version at about -16 LUFS integrated and -1 dBTP true peak, plus a second online version; deliver WAV masters and the stems back [theatrical-delivery playbook].
3. Grade (b): finished animation, 1920 x 1080, 24 fps, Rec.709, ProRes 422 HQ in and out; grade for look and consistency across about 8 to 10 shots per minute, checked for a projector [ROADMAP settings card].
4. Price: a fixed price for each of (a) and (b) with two revision rounds included; say what is excluded (dialogue repair, music clearance, extra formats, rush fees) and what you need from us.
5. Dates: files arrive Sat 6 Feb 2027; first version back within how many working days; final by Fri 19 Feb 2027 at the latest; your earliest start date; whether Lunar New Year (6 Feb) or Presidents' Day (15 Feb) affects you.

*Quote log (one row per vendor; add each as a source [103] onward when it arrives):* `vendor, channel, date_asked, date_answered, price_mix, price_grade, first_version_working_days, final_working_days, excluded, revisions_included, source_id`. **Rule:** two rows with both prices and a turnaround of 10 working days or less switch lever 3 on and finishing drops from 2.7 h/min to 0.8 h/min plus the maker's review time (F1). Fewer than two: finishing stays at 2.7 h/min.

*Who sends it:* the maker, from an address that does not tie the film to the household, or an agent only if the maker says so. Candidate channel I actually saw: a SoundBetter "Post a job" request for the mix [101]. For the grade and a second mix vendor I have no named page; a search-enabled round, or the maker's own contacts, must supply them. Timing: ask by the G-READY week (Sun 15 Nov), as F1 said, so one vendor can price the slice (C01) and the full film together.

### G2. Spike S3 on a stylised kitchen: seconds per frame at 1080p, container CPU measured, GPU not run

**What was possible, said plainly.** There is no real kitchen set yet (the slice C01 builds it; the roadmap has the animatic on Sun 6 Dec and the final on Sun 20 Dec). So I built a **stand-in**: a voxel-style kitchen from primitives only (checker floor, window with sun and a sky card, two counter runs, shelf, table, two chairs, rug, plant, pendant light, a chrome ball), 2,938 faces, default Cycles light paths, no photographs, no textures, no family imagery. Files: `research/production-scale-fixtures/followup2-s3-kitchen-standin.py` (builds and renders it) and `followup2-kitchen-standin.blend`. A 1080p frame of it reads clearly as a stylised kitchen. **It is much lighter than a real set** (the classroom benchmark scene has about 241,000 triangles; this has about 3,000 faces and no textures, glass, volumes, hair, motion blur or depth of field). Treat the numbers as the **best case** for the container.

*Measured on the container* (4 vCPU Intel Xeon 2.1 GHz, 15 GB RAM, no GPU; Blender 5.2.2 LTS from the PyPI `bpy` package; Cycles CPU; 1920 x 1080 at 100 percent; one fresh process per line; adaptive sampling off unless stated; denoise is OpenImageDenoise on CPU):

| Samples | Denoise | Wall seconds, each run | Typical |
|---|---|---|---|
| 8 | no | 13.3 | 13 |
| 24 | yes | 59.3, 50.7 | about 55 |
| 64 | no | 95.2 | 95 |
| **64** | **yes** | 115.1, 109.8 | **about 112** |
| 128 | no | 231.5, 191.9 | about 190 to 230 |
| **128** | **yes** | 208.1, 200.5 | **about 204** |
| 128, adaptive sampling on (Blender default threshold) | yes | 203.2 | 203 (no saving on this scene) |

Derived: **about 1.5 s per sample**, about 1.6 s fixed (load and BVH), denoise about 12 to 17 s at 1080p, memory 0.6 GB without denoise and 2.2 GB with. Run-to-run spread is 5 to 20 percent (the two 128-sample no-denoise runs differ by 21 percent), so read every figure as plus or minus 15 percent. Raw lines are in `followup2-s3-container-results.txt`. For scale: the round-1 classroom scene cost 7.0 s per sample on the same container, so this stand-in is about 4.8 times cheaper per sample.

*What it means for container finals* (12-minute film; Q9 counts: 2,592 hero finals at a 10 percent hero share, 1,296 at the 5 percent lever; ESTIMATE):

| Samples, denoised | Seconds per frame | Container-hours for 2,592 finals | for 1,296 finals | Finals in 24 container-hours | Frames per 10-minute foreground command | per 30-minute background job |
|---|---|---|---|---|---|---|
| 24 | 55 | 39.6 | 19.8 | 1,570 | 10 | 32 |
| 64 | 112 | 80.6 | 40.3 | 771 | 5 | 16 |
| 128 | 204 | 146.9 | 73.4 | 423 | 2 | 8 |

**Verdict [J]: container Cycles finals are viable for a few hundred hero frames, not for the planned hero share.** I set the line at "all Cycles finals fit in 24 container-hours" (one day of background shards). At 64 samples that is 771 frames, 60 percent of the 5-percent plan and 30 percent of the 10-percent plan; at 128 samples it is 423 frames, 33 percent and 16 percent. The full 5-percent plan at 128 samples is 73 container-hours, about 37 two-hour background jobs, and a reclaimed container loses a running job (Q9). The real set will be heavier, so these are optimistic. Use the container for stills, key frames and short hero moves (class C shots of a few seconds) and plan the rest for a GPU or for a non-Cycles route.

*GPU half (NOT RUN; ESTIMATE only).* If the stand-in scales like the classroom scene (CPU to GPU ratio 336, one scene, F3), a 4090-class card needs about 0.0043 s per sample, so about **0.6 s per frame at 64 samples and 0.9 s at 128** including the guessed 0.3 s denoise. The heavier classroom-scene figures from F3 are **1.1 to 1.5 s and 2.2 to 2.9 s**. The real kitchen could land anywhere in that span. On that range 1,296 finals take 20 minutes to 1.1 hours and 2,592 finals 39 minutes to 2.1 hours (ESTIMATE, UNVERIFIED for any GPU).

*What the maker or a pod must run for the GPU half (about 5 minutes, under $1 on a pod):* Blender (free) on the PC or on a rented pod, the stand-in `.blend` only, never a family file:

`blender -b followup2-kitchen-standin.blend -P followup2-s3-gpu-run.py -- OUT_DIR`

The script tries OptiX, CUDA, HIP, oneAPI and Metal, then renders 8 samples (cold, pays kernel load), 64 with denoise, 128 with denoise and 128 without, and writes `OUT_DIR/s3_gpu_result.txt`. I tested it end to end on the container's CPU fallback at 480 x 270 (it ran and printed "NO GPU FOUND"); **its GPU branches are untested**. **Pass:** every warm figure within 2 times of the estimate span above; the notes also record pod start to first frame, the cold-minus-warm gap and bytes transferred. **Then repeat on the real C01 kitchen as soon as its first Cycles hero shot exists** (round-1 criterion unchanged: within 2 times of the table for the real scene). **UNVERIFIED until then.**

*Design consequence [J]:* build the kitchen set from primitives and hand-made textures only, with no photograph used as a texture. Then its Cycles passes may go to a rented GPU without breaking the charter's rule on personal material, and her photos are composited in 2D afterwards. A set that wears her photos as textures counts as family imagery and keeps rendering on the maker's own PC.

### G3. From the maker: still open (the answer sheet)

Unchanged since F0: the maker is the only person on the project and the only approver for hard chapters; nobody is in on the secret; the maker said this can wait until the plan is ready. **Nothing else has arrived**, so H, the holiday answer, country, observances, PC facts and Claude plan are all still unknown, and the model stays on its stated defaults. Answer sheet, one reply, a number or yes/no per line:

1. Hours per week you can reliably give: Nov (learning and slice) __, Dec (slice) __, Jan (production) __, Feb (finishing) __.
2. Holiday fortnight, about 20 Dec to 3 Jan: dead time (0 hours) or your freest time (how many hours a week)?
3. Country (and state) of the premiere.
4. Which of these does your household or the expected audience keep: Diwali (6 to 10 Nov) [92]; Hanukkah (4 to 12 Dec) [93]; Christmas (25 Dec); **Lunar New Year, Sat 6 Feb, which is picture-lock day** [94]; **Ramadan, 8 Feb to 8 Mar** [95]; Ash Wednesday, 10 Feb [96].
5. If Ramadan: will guests be fasting on Sat 27 Feb (about day 20)? Then the screening must start after sunset and iftar. Approximate sunset on 27 Feb (my own astronomical calculation, ESTIMATE, plus or minus about 10 minutes; use a local prayer-times table for the real figure): London 17:35; New York 17:43; Chicago 17:37; Los Angeles 17:46; Toronto 18:02; Dubai 18:19; Delhi 18:19; Karachi 18:32; Singapore 19:20; Sydney 19:35 (local clock, `followup2-sunset-27feb.py`). Add iftar and prayer time, so a start between about 19:00 and 20:30 is typical [J].
6. The PC: CPU model, RAM, GPU model and its memory, free disk (the playbook's Exercise 1 and the PowerShell lines in `playbooks/craft-visual.md` collect this in about two minutes). The GPU answer decides whether G2's GPU half can run on the maker's own PC.
7. Claude plan: Pro, Max 5x or Max 20x.
8. Also useful: is there any cash for buying a mix and a grade (yes, no, or up to how much)? It decides whether G1 matters.

### G4. film-story's 12-minute shape: one answer

**The conflict, exactly.** Both shapes add up to 12:00 and both have the same 1:15 cold open and 1:45 ending. They differ in the 9:00 between: **four chapters of 2:15** (research Q8 table, `research/film-story.md` line 313; `playbooks/film-story.md` Template 4, line 271; `skills/life-film-story-structure/SKILL.md` line 84) against **modules of 3:00** (the same note's recommendation, items 2 and 6: "Four modules plus the wrapper make 15:00", "Cost is per module"), which makes 12 minutes the wrapper plus **three** 3:00 modules.

**Decision: 12 minutes = cold open 1:15 + three modules of 3:00 + ending 1:45.** Timeline: cold open 0:00 to 1:15; module 1 1:15 to 4:15; module 2 4:15 to 7:15; module 3 7:15 to 10:15; ending 10:15 to 12:00. Reasons:
1. **One unit for every cut.** With 3:00 modules, 9 minutes is the wrapper plus two, 12 the wrapper plus three, 15 the wrapper plus four, and each cut differs by whole modules. With 2:15 chapters, going from 12 to 15 minutes re-cuts every chapter, which breaks film-story's own rule that the 12 "is the same film as the longer cut minus modules, not a separate film" (item 1) and the kill-or-cut dates that count modules at S4 (item 5).
2. **The note argues against 2:15 itself.** Item 2 says texture "needs more than the 2:15 chapters of the 12-minute plan".
3. **It is already the plan of record.** `ROADMAP.md` section 4 and decision row 5 use wrapper plus three 3:00 modules, and its own text says film-story's 2:15 row "is superseded" and that the scribe patches Template 4.
4. **Hard-beat timing still works.** First hard beat "no earlier than about 3:00 to 4:00" (12 minutes) and "about 4:00" (15 minutes): put it in module 2, which starts at 4:15.
5. **Cost model unchanged.** 12:00 is 720 seconds, 7.2 of the model's 100-second learning units; seven units stays valid.

**Two consequences to carry.** (a) `playbooks/format.md` Decision 7 counts "4 to 8 told chapters of 90 to 150 seconds". A 3:00 module holds about two 90-second beats, so three modules is about six chapters in format's unit and inside its range, but the word "chapter" now means two different sizes; the scribe should say "module" in both files and state the conversion once [J]. (b) The older `ROADMAP-ADDENDUM.md` lines 179 and 210 say "six two-minute chapters (12 minutes)", a third shape that predates `ROADMAP.md`; mark it superseded.

**Scribe patch list (I did not edit these files):**
- `research/film-story.md` line 313: 12-minute budget cell to "Cold open 1:15; three modules of 3:00 = 9:00; ending 1:45; total 12:00". Line 320: delete "more than the 2:15 chapters of the 12-minute plan" or reword to "more than a thin 2:15 chapter".
- `playbooks/film-story.md` line 271: same budget. 
- `skills/life-film-story-structure/SKILL.md` line 84: same budget.
- `skills/animation-production-planning/SKILL.md` line 119 and `playbooks/production-scale.md` line 665 (Decision 13): close the "film-story's own 12-minute row lists four 2:15 chapters" option and the TODO(research) that says to reconcile.
- `ROADMAP.md` line 65: the parenthetical "the scribe patches film-story Template 4" can be dropped once the above are done.
- `ROADMAP-ADDENDUM.md` lines 179 and 210: mark "six two-minute" as superseded.

### G5. Sora API after 2026-09-24: 'shut down' or 'ended'?

**One dated source settles it: OpenAI's own deprecations page [97].** Under the heading **Past deprecations** (read 2026-10-18; the page shows no last-updated date) the entry "2026-03-24: Sora 2 video generation models and Videos API" has a table headed "Shutdown date | Model / system | Recommended replacement" with **2026-09-24** against the Videos API, `sora-2`, `sora-2-pro`, `sora-2-2025-10-06`, `sora-2-2025-12-08` and `sora-2-pro-2025-10-06`, and "---" (no replacement) in every row. Its one sentence of prose: "On March 24th, 2026, we notified developers using the Videos API and Sora 2 video generation model aliases and snapshots of their deprecation and removal from the API on September 24, 2026." (The old address platform.openai.com/docs/deprecations answers with a 301 to the address in [97].)

**Wording to use:** OpenAI's own word in the table is **"Shutdown date"** and in the prose **"removal from the API"**. So: "the Sora API was **shut down** (removed from the API) on 2026-09-24 [97]; the consumer app went dark on 2026-04-26 [45]". "Ended" is not OpenAI's word; do not use it. Caveat: I read the page and did not call the API (no key), so the evidence is that the entry sits under Past deprecations on 2026-10-18, not that I saw a failed call. The playbook line "API scheduled to end 2026-09-24 (already past; current status UNVERIFIED)" can change to "removed 2026-09-24 per [97]", and the route-risk example becomes: "a hosted video model was withdrawn, with 6 months' notice and no replacement named".

### G6. Where the CC0 statement for the Blender Open Data snapshot lives

Three places, none of them the About page:
1. **The Download page, under the heading "Raw Data", in a "License" section** [98], https://opendata.blender.org/download/: "The data in this archive is licensed under the CC0 - Creative Commons Zero license", followed by "For more details and legal text refer to LICENSE.txt included in the downloaded archive."
2. **`README.txt` inside the zip** [99]: "The data in this archive is licensed under the *Creative Commons 0* license. For more details and legal text refer to `LICENSE.txt`." (This is the wording round 1 saw; [83] gave only the file and its date.)
3. **`LICENSE.txt` inside the zip** [99]: the full "CC0 1.0 Universal" legal code (7,049 bytes). I opened the archive of 2026-10-18 (101,626,337 bytes, Last-Modified Sun, 18 Oct 2026 00:01:21 GMT): three entries, `LICENSE.txt`, `README.txt` and one `.jsonl` data file.

The **About page** [82] does not say CC0. It lists "License-free" among its open-data principles ("Data is not subject to any copyright, patent, trademark or trade secret regulation") and links to a daily snapshot; the **home page** [100] has no licence text, only a footer link to Blender's general licence page, which I did not open. For a citation, use [98] with [99]. This only concerns the benchmark data; it says nothing about the benchmark scene files or Blender itself.

### Impact summary (round 2, for the orchestrator and scribe)

1. **Finishing cash (Decision 4):** still no quote. Lever 3 stays off and finishing stays at 2.7 h/min until two logged quotes arrive. The RFQ is in G1; the maker must send it (ideally by Sun 15 Nov).
2. **Render route (S3):** container Cycles gives about 112 s (64 samples) and 204 s (128) per 1080p frame on a light stand-in, so it covers a few hundred hero frames in a day and not the planned hero share. Plan the hero share for the maker's GPU or a pod, build the set photo-free so a pod is allowed, and run the 5-minute GPU test (G2).
3. **Chapter plan:** one answer, wrapper plus three 3:00 modules; patch list in G4. Flag to `format`: "chapter" now means two sizes.
4. **Sora:** say "shut down 2026-09-24 per OpenAI's deprecations page", no longer UNVERIFIED.
5. **Open Data:** cite the Download page and the archive's own README and LICENSE.
6. **Maker's answers:** G3 sheet; nothing new has arrived. Unchanged: only the maker is in on it.

### Sources added in round 2

OpenAI
- [97] OpenAI API docs, Deprecations — https://developers.openai.com/api/docs/deprecations — read 2026-10-18; the page shows no last-updated date (the old address https://platform.openai.com/docs/deprecations answers 301 to this one). Under "Past deprecations", entry "2026-03-24: Sora 2 video generation models and Videos API": column "Shutdown date" 2026-09-24 for the Videos API and five sora-2 models, replacement "---", prose "of their deprecation and removal from the API on September 24, 2026".

Blender Open Data
- [98] Blender Open Data, Download — https://opendata.blender.org/download/ — read 2026-10-18 — "License" section under "Raw Data": CC0 wording and the pointer to LICENSE.txt in the archive.
- [99] Blender Open Data daily snapshot, `README.txt` and `LICENSE.txt` inside the archive — https://opendata.blender.org/snapshots/opendata-latest.zip (the file of [83]) — Last-Modified Sun, 18 Oct 2026 00:01:21 GMT, 101,626,337 bytes; opened locally 2026-10-18: README.txt 374 bytes ("Creative Commons 0"), LICENSE.txt 7,049 bytes ("CC0 1.0 Universal"), data file `opendata-2026-10-18-000000+0000.jsonl` 1,891,255,083 bytes.
- [100] Blender Open Data, home page — https://opendata.blender.org/ — read 2026-10-18 — no licence statement; footer "License" link to https://www.blender.org/about/license/ (not opened); "345728 openly accessible benchmarks" (count as of the read).
- (Re-read [82], About, on 2026-10-18: no CC0 statement; "License-free" principle wording only.)

Mix and grade
- [101] SoundBetter, home page — https://www.soundbetter.com/ — read 2026-10-18, undated — no prices in the first 100,000 of 472,675 characters; category links "Mixing Engineers" and "Mastering Engineers".
- [102] SoundBetter, Mixing Engineers — https://soundbetter.com/s/mixing-engineers — read 2026-10-18, undated — no prices; "Inquire for rates on Recording, Mixing, Mastering and more..." on one profile; menus list Post Mixing and Dialogue Editing; first 100,000 of 125,684 characters read.

*Not sources (failed or empty fetches, listed in G1):* Thumbtack video colour grading and audio mixing cost pages, PremiumBeat and StudioBinder colour-grading cost articles, Fiverr video colour grading category.

*Fixtures saved (round 2):* `research/production-scale-fixtures/followup2-s3-kitchen-standin.py`, `followup2-kitchen-standin.blend`, `followup2-s3-container-results.txt`, `followup2-s3-run-sweep.sh` (holds scratch-folder paths from this session), `followup2-s3-gpu-run.py`, `followup2-sunset-27feb.py` and `.txt`.
