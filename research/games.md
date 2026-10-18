# Games that tell life stories: mechanics that carry meaning — research notes

Track: `games` · Researcher: Sonnet · Written 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline 2027-02-27.
Evidence tiers used below: **[P]** designer/creator/official statement, **[S]** journalism quoting designers, **[T]** Wikipedia/aggregator or search-snippet only (treat as a lead, not proof). Anything I could not verify is marked **UNVERIFIED**. Where I rate things (accessibility, gimmick risk, build effort) that is **my judgment**, not a sourced fact, unless a citation sits next to it.

---

## Summary

1. **The best "life" games make the mechanic *be* the meaning, and almost none use points.** Unpacking (placing a life's objects into successive homes), Florence (a conversation that is a jigsaw that gets easier as two people relax), Passage (a whole life on a 100x16 screen in five minutes) and A Memoir Blue (moving the trophies aside to reveal photographs) all express something with one small verb. [1][3][5][23][30]
2. **Unpacking is the closest model for us, and its designers say why it works for everyone.** It was built under "subtractive design" (cut anything not serving the core); the GDC talk title is literally "Designing a Game Without Fail States or Scores"; Brier says it is playable and enjoyable from age 5 to 75. No timer, no fail, no score, no words. [1][2]
3. **Objects carry story when they are specific, recurring and in context.** Unpacking's team invents either the item or the story first and "cross-pollinates"; they track every item in spreadsheets (new, repeated, variant); and a *mechanic* (moving the boyfriend's things to make space) became a *story beat*. Edith Finch rewrote bedroom decor late because Lewis's room told his story with no narration. Lesson for us: real objects and real rooms beat invented ones, and one object that survives every move is worth more than fifty props. [3][12][13]
4. **Florence's trick is "friction that tracks the relationship."** Speech-bubble puzzles start hard (nervous first dates), get easier as comfort grows, and turn sharp in arguments; tooth-brushing stands for routine; packing up when a partner moves in and handing things back when they move out are mini-games. These map cleanly to a first meeting, a move, a breakup; a first job and a birth need our own inventions (see Q4). [5][6][9]
5. **Before Your Eyes teaches the best accessibility lesson in the set, by accident.** Its blink-to-advance-time idea nearly sank the project because involuntary blinks skipped story; the fix was a metronome that tells the player *when* input counts. For a shared screen, copy the principle (the screen announces when you may act or pause), not the webcam. [14][15]
6. **Most of these games need a gamer's hands somewhere.** Drag/swipe/double-tap/long-press, analog sticks, two-stick control (Edith Finch's Lewis), webcam blinking, platforming and base-management mini-games should be dropped or converted to click-once or passive animation. An older-adult study found slides in the wrong direction, fingers not lifted, mistimed double taps, and that many 50+ players dislike time limits. [12][13][41]
7. **Achievements/points/badges for life events are the first anti-pattern.** Robertson ("pointsification", points are "the thing that is least essential to games") and Bogost ("Just add points") give the case; Passage itself mocks score by floating it above a tombstone; A Memoir Blue's trophies are the thing you *remove*. [23][30][37][38]
8. **Minecraft memorials are real but mostly small, personal and second-hand reported.** Verified examples: a 10-year-old's zoo built from his dead father's loves (2017), a student/tutor replica of a Harvard house (10,000+ brick blocks, three weeks, 2020), a server hub covered in signs for a dead server owner (Mojang's own 2019 article), and a "towering bust" tribute shared as a YouTube video (2014; original not found). Audiences mostly *watched* (video, live tour, screenshots); playing was for the maker and the closest circle. [57][59][60][61]
9. **Voxel/blocky reads warm when it is hand-specific; it reads meme/asset-pack when it is generic.** Craft evidence: restricted palette with shading painted in, constant voxel resolution, no stair-step noise ("greebles"), warm key light with cool soft fill, modular hand-built assets. The strongest single device in the memorial examples is *specificity of subject* (an octopus aquarium because Dad fished). [59][64][65][66]
10. **Minecraft's terms: "very relaxed" for yourself; sharing counts as "commercial"; the rules that bite us are the public big-screen clause, no selling copies, no implied endorsement, and "we can change this anytime."** Mojang explicitly will not advise on a specific project. **Verify against current Mojang/Microsoft terms before 2027-02-27.** Safest route: original voxel assets in MagicaVoxel/Blockbench. [42][43][49][50]
11. **Strong mappings for a 50+ life:** a map that fills in (and can be *frozen*), inventory limited to a few real objects, biomes replaced by *actual* places, crafting shown as the person's real hands/recipes. **Clichés:** generic biomes, "life as a day", house-equals-family without the real house, redstone. **Inversions worth trying:** lost items that despawn, a locked vault, a chapter gone from the map, trophies moved aside. [31][52][53][54][55]
12. **The subject is alive and 50+, so avoid elegy by default.** A 2021 older-adult game study advises against depicting older adults' lives in static, passive, negative or depressed tones; death-forward games (Passage, Spiritfarer, That Dragon, Cancer) are sources of devices, not of register. [41]
13. **Design for a room, not a loner.** Brier reports Twitch viewers narrating their own lives as they watch Unpacking; Harvard's Minecraft house was toured live with people logging on to watch. Build a host-friendly, pause-and-talk experience, not a solo test of skill. [3][61]
14. **Do not copy the mood board.** Unpacking's makers call clones "hollow"; isolate the device (e.g., "friction tracks relationship") and re-ground it in the person's facts. [3]
15. **Recommended vertical-slice shortlist (all at most Medium effort):** trophies-aside reveal; unpack-and-place across 3 homes with one surviving object; SVG map that fills in; Florence-style first-meeting conversation pieces; one real room as a shrine with click hotspots; a "pause chime" pacing device; one warm-lit voxel diorama.

---

## Findings by question

### Reading guide for the two deliverables

**Rating scales (my judgment).**
- **Access (A) 1-5.** Two tests at once: (a) could a 70-year-old do it with one hand on a trackpad or remote, with no timer, no fail, no reading-speed pressure; (b) does it still work when a room of relatives watches one screen. 5 = fine as is; 4 = fine with click-to-act or auto-advance; 3 = redesign needed; 2 = convert to passive animation; 1 = drop.
- **Gimmick risk (G).** L / M / H = chance it reads as decoration or a trend borrowed from a game.
- **Build effort (B), engine-free.** S = about a day for a learner with AI help; M = 2-5 days; L = 1-3 weeks (rough guess, no engine assumed; the `format` track decides feasibility).
- **Principle 2 test ("Swap-the-subject").** If the device works unchanged for anyone's life, it fails the charter. The mapping column says what makes each pattern pass.

### Deliverable A: Pattern library

**A1. Objects, rooms, homes**

| # | Mechanic | Example and designer source | What it expresses | Candidate mapping (passes Principle 2 only if...) | A | G | B |
|---|---|---|---|---|---|---|---|
| 1 | Unpack-and-place objects into successive homes; no score, timer or fail | *Unpacking*: Brier GDC 2023 talk, "Designing a Game Without Fail States or Scores"; Eurogamer 2022 [1][2][3] | Identity as a trail of belongings; continuity (the thing that survives every move) vs change; intrusion/making space | Childhood room, first flat, shared home, kids' rooms, empty nest, downsizing. Passes if every object is the person's *real* one (photographed/voxelised) and one recurring object is chosen with the family | 5 (viewers can call out where things go; replace drag with click-pick, click-place) | M (cozy-sim cloning; Brier calls clones "hollow") | M |
| 2 | Mechanic doubles as story beat | *Unpacking* boyfriend's flat: his items take up as much space as possible so you feel you must "make space"; Brier and Dawson [3] | A relationship shown by *how much room one person leaves another* | A partner's, landlord's, parent's home where there was no room: show it as crowded shelf space | 5 | L | S |
| 3 | Rooms as preserved shrines; objects reveal the person before any narration | *Edith Finch* bedrooms of the dead; Lewis's room (lighting, Murphy bed, computers) conveys him; decor was revised late for this [12][13] | A person as a room others keep exactly as left | Childhood bedroom, father's workshop, grandmother's kitchen. Passes with the real room (photos, measurements, family memory). Sealed vs "preserved" differs between sources: either way a memorial | 3 (walk-around is dexterity; use guided camera plus click hotspots) | L-M | M-L |
| 4 | Text placed physically in the world, stepped through at the reader's pace | *Edith Finch* floating captions that draw the eye to objects [12][13]; guideline "dismiss on action, not timer" [40] | Writing as a trace left by a person | The subject's real sayings, notes, recipe cards, labels, on the objects they belong to | 3-4 (needs large text, advance-on-click or narrated auto-advance) | M | S-M |
| 5 | Object as aperture: touch an object, enter a memory | *Hindsight* "apertures" with a house-clearing premise (McDonald, via Screen Rant) [34]; *Dordogne* collects photos, sounds, scents (store text only) [32] | The way a thing unlocks a scene | Each treasured object (watch, ladle, bike bell) opens a 10-30 second scene: photo, voice, clip | 5 | M | M |
| 6 | Inventory as treasured objects | Spiritfarer: belongings are "only a trace"; the person is what remains; Guérin kept the houses on the ship despite playtest pressure [27] | What a life leaves in hands | A *very small* shelf of real objects (5-9), each with a story; not an RPG grid | 5 | H if generic icons; L if real photos | S |
| 7 | Chosen object display (museum wall) | Minecraft item frames show any item or a map on a wall; a renamed item shows its name [56] | Curation | A wall of five real things in a voxel room | 5 | L | S |
| 8 | Specific-love architecture | A 10-year-old built a zoo for his late father: octopus aquarium because Dad fished, smoked salmon in the zoo cafe; still tweaked years later [59] | A person encoded as the things they loved, built *for* them | A structure assembled only from the subject's real loves (garden, boat, record shelf), built in the maker's chosen look | 4 (viewer watches) | L | M |

**A2. Time, life arc, place**

| # | Mechanic | Example and source | What it expresses | Candidate mapping | A | G | B |
|---|---|---|---|---|---|---|---|
| 9 | Whole life on one strip; future ahead, past accumulating behind | *Passage*: five minutes, 100x16 px; screen is the lifetime; you see only the future at first, later a growing past (Rohrer's own statement) [23][24] | Time as horizontal space; memory as growing wake | Animated left-to-right walk through decades. For a living 50+ subject: **stop at "now" with open road ahead**, do not walk to the edge | 4 (auto-walk, no input) | M (memento-mori register wrong for a celebration) | S |
| 10 | A companion who joins and changes how you move | *Passage*: spouse joins; you move together, narrow gaps block her, her death slows you (Rohrer) [23] | Partnership as a physical fact (pace, access, grief) | Show how THIS person's pace changed when they paired up or had children, with the family's say. Dignity: never make a living spouse the "obstacle" without consent | 5 as animation | M | S |
| 11 | Time as a scrubber the audience turns | *The Gardens Between*: time mechanic built first; story told with no words; passive storytelling means rushing yields less (Pettersson) [33] | Memory as something you move back and forth through | One dial moves a room between ages 6, 16, 46 | 4 (one slider or arrow keys) | M | M |
| 12 | Blink or hold to advance time, gated by a metronome | *Before Your Eyes*: blinks advance time; involuntary blinks skipped story until a metronome showed when blinking counts [14][15] | Time passing without consent | Convert: the screen announces "you may pause" with a soft chime; drop the webcam | 1 as designed; 5 converted | M | S |
| 13 | Map that fills in as the world widens (and can be frozen) | Minecraft Map item draws what you have explored; zoom levels; copies stay in sync; a glass pane locks a copy so it stops changing [52] | A widening circle of life; memory fixed at a moment | Hand-drawn SVG map revealing childhood street, school, first city, abroad. Inversions: radius shrinking; a locked copy of a place as it was | 5 | L-M | S-M |
| 14 | Chapters as distinct worlds with their own palette | *Gris*: colour restored area by area (Cuevas: "the most important thing in the game are the colours") [25]; *Journey*: desert-to-snow arc [20][22] | Emotional state of a period | Palette per era drawn from real photo stock (Kodachrome, faded Polaroid, early digital), not generic biomes | 5 | M | S |
| 15 | Locations picked because the story needs them | *Dordogne*: art director spent childhood summers there; "the story came first and the real-world locations... were picked based on our story's needs" [32] | Truth of place | Use the real streets/rooms, sketch on site (the team sketched locations to capture feel) | 5 | L | M |

**A3. Tiny interactions (Florence-style)**

| # | Mechanic | Example and source | What it expresses | Candidate mapping | A | G | B |
|---|---|---|---|---|---|---|---|
| 16 | Conversation as a puzzle that eases with comfort; sharper pieces in arguments | *Florence* (Ken Wong): "what if her speaking is a puzzle... and it gets easier over time?" Aimed at first-meeting nervousness; arguments use increasingly sharp bubbles [5][6][9] | The effort of talking; intimacy as friction removed | First meeting with partner (many pieces, then few); a hard talk with a parent (sharp pieces); kids' first words (one piece, huge target) | 3 on touch gestures; 4 with big click targets or passive animation | M (Florence-clone risk) | S-M |
| 17 | Routine micro-action that changes when another person enters | *Florence* tooth-brushing: easy, pleasant; later signals a settled couple [6] | Routine as intimacy | Making breakfast, walking the dog: the same 3-second loop that gets a second pair of hands after a move-in or birth | 5 | L | S |
| 18 | Packing boxes in and out | *Florence* packing her things when he moves in and returning his when he moves out [9]; *Unpacking* [3] | Moves, arrival, separation | A move; leaving the parental home; (with consent) a breakup; clearing a parent's house. Passes only with the real items | 5 (click item, click box) | M-H (box-packing is now common) | S |
| 19 | Embodied viewpoint at a life event | *Edith Finch* pregnancy ending: Edith's belly visible in first person (tech artist Chelsea Hash insisted) [13] | A body going through change | Birth/children: show the parent's own hands or a room acquiring a cot, not a stock newborn | 5 | L | S |
| 20 | Wordless, unspecified emotion | Wong: "we don't specify what the argument is about because that's not important"; the soundtrack stands in for voices [7] | Feeling without plot | Hard chapters shown through music and room, with the family's say (Principle 5) | 5 | L | S |

**A4. Love, loss, care, reversal**

| # | Mechanic | Example and source | What it expresses | Candidate mapping | A | G | B |
|---|---|---|---|---|---|---|---|
| 21 | Trophies/achievements removed to reveal photographs | *A Memoir Blue* final puzzle: move aside Miriam's trophies to find happy photos with her mother (Inverse); Chen's context on a medal ceremony (AV Club) [29][30] | The achievement list hides what mattered | Career awards, diplomas, titles lifted away to show the kitchen table, the holiday photo. **Top pick: it turns the "milestone checklist" into an argument** | 5 (one click or drag) | L | S |
| 22 | Care as the loop; building for others | *Spiritfarer*: "you build those things, but not for you, you build them for others"; chores mirror a nurse's work; farewells at the Everdoor (Guérin) [27][28] | Caring labour and letting go | Caregiving years, hosting, raising kids: show the *work* of care rather than the achievement. Farewell scenes only with consent | 2 (base-management mini-games) -> 4 as montage | M | L (do not build the game; borrow the idea) |
| 23 | Recipe restoration | *Venba*: Abhi: "To measure if something is changing, you need something that stays constant... food seemed like the perfect fit" [31] | Culture and family as constants measured against change | The person's real recipe card, the hands doing it (video), the step nobody remembers marked as lost, not invented | 4 | M | S-M |
| 24 | Per-person idiom: each key person gets their own look and control | *Edith Finch*: 13 stories, about 13 control schemes; the GDC listing describes heavy prototyping and discarding, and playtest emotion decided which stories stayed [10][11] | Each person sees the world differently | Three to five key people each get a chapter style (a mother's chapter as recipe cards, a brother's as a cassette). Scope: the studio built and discarded many prototypes to land 13 stories, so keep ours to 3-5 | 5 as motion design | L-M | L |
| 25 | Ambiguity / unreliable accounts | *Edith Finch*: player left unsure how accurate each account is; Dallas expects players to wrestle with their own interpretations [11][13] | Memory and family versions of a story | "Dad's version / Mum's version" scenes, visibly restyled. Directly serves Principle 4 (reconstructions look like reconstructions) | 5 | L | S |
| 26 | Evaluation question as design filter | Green: "Does this scene help the player love Joel more?"; scenes that didn't were cut or rewritten [17] | Purpose over spectacle | Ask of every scene: does it help the audience love *this person* more? | n/a | n/a | S |
| 27 | Metaphor that doesn't "play well" on purpose | *That Dragon, Cancer* racing minigame with treatment beads: Green: "metaphor, not how the game plays" [18] | Helplessness | Rare; avoid for a celebration. Note criticism that it "didn't play very well" | 2 | M | M |
| 28 | Anonymous companion; sing-only communication | *Journey* (Chen): everyone the same, no chat, can leave anytime, "the co-op is more real and sincere" [20][21][22] | Strangers who walked part of the way | Silhouettes who join and leave at each stage (teachers, neighbours). Optional: relatives "call out" a memory in the room | 3-4 | M | M-L |
| 29 | Reshaping terrain to walk on | *Old Man's Journey*: shape hills, walk their silhouettes; prototypes kept only if the mechanic already carried an emotional association [19] | Travel/wanderlust; a path made by decisions | Moves between cities as hills that lift under the walker: auto-animation, not drag | 2 as built; 5 as animation | M | M |
| 30 | Slow walking, narration varies | *Dear Esther*: remove traditional gameplay so story alone engages; voice-overs partly randomised [35] | Presence | A slow camera drift through a place with the family's voice-over; keep narration **fixed** (Principle 4) | 4 | L | S |

**A5. Minecraft-specific patterns**

| # | Mechanic | Example and source | What it expresses | Candidate mapping | A | G | B |
|---|---|---|---|---|---|---|---|
| 31 | Scale replica of a shared home, built together | "Minecrapft" Pforzheimer House: 10,000+ brick blocks, survival mode, floor plans + Google Maps, three weeks; live tour by the deans on 2020-04-10 [61] | A place as a shared memory; blocks give the right amount of "fuzziness" (the writer's own reflection) | The family home at scale; a slow camera walks room to room. Family can add rooms | 4 (watch) | M | L |
| 32 | Monument + plaque + candles | "Gas Bandit": towering bust holding a pickaxe over the ocean, torches, underground room with candles, moat, music, plaque; shared as a YouTube video (2014) [57]; Everplans describes a minecart-riding avatar (partner, Reddit; same man, different build or telling) [58] | Grief as monument-building | Probably not needed; shows the monument default | 4 (watch) | H | M |
| 33 | Hub of signs: the community's voice as architecture | Emenbee server hub covered in sign messages for Pendar2; Mojang's writer: "couldn't stop wandering around the hub, trying to read them all" [60] | Collective tribute | A "wall of voices": every relative writes a line; shown as signs in a room | 4 (reading: allow time) | L | M |
| 34 | Books as carriers of real text | The Uncensored Library: about 300 in-game books in 12 wings, downloadable [62] | Documents inside a world | Letters, speeches, recipes as "books" on lecterns | 3 (reading) | L-M | M |
| 35 | Inventory loss: dropped items scatter and despawn after five minutes; keepInventory changes it | Minecraft Death [54] | What cannot be carried | Inversion: the things that did *not* make it through a move or a loss, shown fading | 5 as animation | L | S |
| 36 | A chest/vault that only opens with its own key; each player opens once | Minecraft Vault (added 1.21): keyhole, trial key; each player unlocks once [55] | A chapter the subject chooses not to open | A locked door on the timeline for sensitive chapters (Principle 5) | 5 | L | S |
| 37 | Day/night with a 20-minute cycle; sleeping skips the night | Minecraft Daylight cycle: 10 min day, 50 s dusk, about 8m20s night, 50 s dawn [53] | Time of day as mood | Lighting keyframes per chapter; "a bed that skips the night" for years that vanished | 5 | M-H ("circle of life" cliché) | S |
| 38 | Bed as home / respawn | Minecraft respawn at last-used bed [54] | Home as where you return | Use only as an image: the bed you always come back to | 5 | M | S |
| 39 | Redstone logic | **Not researched; UNVERIFIED** | Machinery | Passes only if the subject truly worked with circuits/wiring/clockwork | 3 | H | M |

### Deliverable B: Anti-pattern list (first item is the most important)

1. **Points, XP, badges, achievements, "level up", leaderboards for life events.** Life milestones are not trophies. Robertson calls the points-and-badges layer "the thing that is least essential to games" and "pointsification" a misuse of the word gamification; Bogost: it keeps the easy, boring parts of games (points) and drops the hard, meaningful ones. Passage even floats the score above a tombstone, and A Memoir Blue ends by moving trophies aside. Test: if a toast could read "Achievement unlocked: Married", delete it. [23][30][37][38]
2. **Progress bars and "completion percentage" for a life.** Same family as 1; also implies the person is unfinished.
3. **Generic stock vocabulary:** "circle of life" day/night, generic biomes, treasure chests, hearts/hunger bars, mobs as hardships. Fails Principle 2 (swap-the-subject).
4. **Monsters or enemies as stand-ins for illness, divorce, money.** Dignity risk (Principle 5); also puts the family in the position of fighting a person's real pain. (My judgment; consistent with Green's insistence that mechanics be metaphor, not spectacle [18].)
5. **A fail state, game-over, or timer in a gift for relatives.** The sources that work for a mixed-age audience remove them (Unpacking; Gris; Edith Finch deaths cannot be failed). 50+ players dislike time limits [1][2][12][26][41].
6. **Precision gestures as the only way to proceed:** drag, swipe, double-tap, long-press, rhythm taps, eye-blinks, webcam tracking. [41][69]
7. **Walls of text on a timer.** Advance on action, not on a timer; allow replay. [40]
8. **Elegy as default register for a living 50+ subject.** Passage, Spiritfarer, TDC and Edith Finch are about death. The older-adult study advises against portraying older adults' lives in static, passive, negative or depressed tones. [41]
9. **Inventing events, people or quotes to fill a mechanic.** Breaks Principle 4. Edith Finch makes ambiguity visible; we must make reconstruction visible. [11][13]
10. **Cloning a famous game's surface** (Florence couch colours, Unpacking cardboard boxes) without the person's facts. Brier on clones: "hollow." [3]
11. **Minecraft UI cosplay and default textures** (hotbar overlays, creeper, default skins, "achievement" pop-ups): cheapens the piece and walks into Mojang's brand rules. [42]
12. **Solo-player assumptions** (one controller, quiet twenty minutes). Design for a host and a room. [3][61]

---

### Q1. For each studied game: core mechanics, stated intent, what players report, and where they disagree

Conventions: "Says" = designer statement (cited). "Players" = reported feelings (cited). **Gap** = I could not verify.

| Game | Core mechanics | Designer says (source) | Players report | Disagreement / caveat |
|---|---|---|---|---|
| **Unpacking** (Witch Beam, 2021) | Take items from unlabelled boxes, place them in rooms across successive homes; no dialogue, score, timer or fail state | Brier GDC 2023: three pillars (contemplation, discovery, expression); "subtractive design" [1][2]. Inspired by Amanda Palmer's "The Bed Song" (a couple's life through the beds they owned); items and stories invented in both directions; tutorial moves become story beats; rules loosened so players "come up with" their own [3] | "Very heartfelt letters" about their own moves; during the pandemic people moved back with parents and recognised themselves; Twitch viewers narrate their own stories as they watch [3]; Brier's stats: 14% of players flushed every toilet [1] | The team feared people would be "sick of being at home" and it didn't happen [3]. Reportedly 1997-2018, eight stages, 35 rooms (search summary; UNVERIFIED) |
| **Florence** (Mountains, 2018) | Short, linear interactions: speech-bubble jigsaws, tooth-brushing, packing/returning things, finding Krish by following a cello; about 20 chapters, 30 min [9] | Wong: conversation puzzle eases with comfort to portray first-meeting nervousness; calls them "interactions" not puzzles; "short, linear games that aren't very difficult" focused on empathy [5][6]. Cut chapters: "Autumn of Our Love" failed because it was visual not interactive; "Reunion" cut so the ending is about letting go [6] | Players cried and played on public transport [8]; critics compared it to WarioWare and some felt the ending favoured art over love (Wikipedia summary of reviews) [9] | Wong says the argument topic is unimportant [7] while critics read the ending as a statement about art vs love [9]. Wong has faced public allegations (see Pitfalls) |
| **What Remains of Edith Finch** (Giant Sparrow, 2017) | First-person house exploration; each dead Finch's room triggers a vignette with its own mechanic and control scheme; text appears in the world | Dallas: began with awe; 13 stories, about 13 control schemes; stories culled by watching playtesters' emotional reactions; "I expect that players will wrestle with their own interpretations" [10][11]; weird-fiction ambiguity [11] | Polygon: "The final farewell left me crying" (via Wikipedia) [13] | Sealed vs "preserved" bedrooms differ across secondary sources [12][70]; originally titled *The Nightmares of Edith Finch*, but widely received as moving, not scary [13] |
| **Before Your Eyes** (GoodbyeWorld, 2021) | Webcam blinks advance time; mouse alternative; metronome gates when blinking counts; ferryman framing | Lewin: blinking is "linked so harmoniously with time passing, like an editing technique"; Parkes: "What if we make a game about losing?" [14][15]; script drawn from the team's childhood locations and Parkes's hospitalisation [14] | Prototype players "leaving the booth crying" [14]; reviewers: some moved, some felt the blink mechanic undercut the emotion; calibration complaints [69] | Parkes says the early game "really wasn't good enough" for the tears it got [14]; eye-dryness/other discomfort comments in review aggregation (UNVERIFIED) [69] |
| **To the Moon** (Freebird, 2011) | Point-and-click RPG Maker story; "memory traversal" | Gao: "more like an interactive story"; music written first; idea from his grandfather's illness; scenes that moved people were "happy... or maybe more accurately, bittersweet" [16] | Same source (designer's observation of players) [16] | Designer intended a serious story about regret; players were most moved by happy beats [16] |
| **That Dragon, Cancer** (Numinous, 2016) | Point-and-click vignettes: hospital, racing with treatment beads, a redwood "cathedral", the sea | Green: filter "Does this scene help the player love Joel more?" [17]; a game suited "choice, free will, and feeling powerless" better than film [18]; racing game is "metaphor" [18] | Interviewer found the racing scene "absolutely heartbreaking"; a critic said it "didn't play very well"; a commenter read life as meaningless, which Green rejects [18] | Direct disagreement between critic reading and designer on whether a mechanic must "play well." Claim that Joel is depicted without distinguishing features: UNVERIFIED (The Spinoff names Joel) |
| **Gris** (Nomada, 2018) | Platform-adventure; colour restored in areas; abilities from star-like lights; no fail state | Cuevas: "The most important thing in the game are the colours"; Roset wanted colour-unlocking as a mechanic; "what we want you is to feel what Gris is feeling" [25]; team consulted a psychologist; no fail state designed for accessibility [26] | **Gap**: no player-report source fetched | The "five stages of grief = specific colours" mapping appears in fan essays and Wikipedia; Cuevas's interview as fetched doesn't use the word "grief" and describes sorrow turning to hope. Treat the stage-colour table as UNVERIFIED [25][26] |
| **Spiritfarer** (Thunder Lotus, 2020) | Boat-building on a grid, resource gathering, cooking/caring for spirits, farewells at the Everdoor; co-op | Guérin: death is "misused" in games; farm-sim mechanics show kindness; "you build them for others"; chores mirror a nurse's work; only 10-15% of the game is dramatic: "a spike of drama, or a spice of sadness"; co-op kept partly so families could talk about death [27][28] | **Gap** (no direct player reports fetched) | Playtesters pressed to remove the ship-houses; Guérin kept them (they came from his mother clearing a relative's belongings) [27] |
| **Old Man's Journey** (Broken Rules, 2017) | Reshape hills, walk their silhouettes, switch at intersections; memory scenes | Bohatsch/Scott: a photo of receding hills suggested depth and wanderlust; prototypes kept only if mechanic already had an emotional association; story from balancing creative work with parenting; "feel different depending on the player's stage of life" [19] | **Gap** | One reviewer reads the bending as the world yielding to the old man's determination (search snippet; my paraphrase; UNVERIFIED) |
| **Journey** (thatgamecompany, 2012) | Walk, jump, a single "call" button; anonymous two-player encounters; no text | Chen: "I wanted to see a world where everyone is the same"; wanted awe and smallness; can leave a partner anytime because "the co-op is more real and sincere"; multiplayer simple enough for non-gamers [20][21][22] | Chen at D.I.C.E. 2013: 3 of 25 testers cried at the end (via Wikipedia citing Variety) [22] | One-button claim is Wikipedia-sourced [22] |
| **Passage** (Rohrer, 2007) | 5-minute life in a 100x16 maze; spouse, chests, score | Rohrer: aging moves you toward the right edge; chests are pursuits (most empty); spouse slows and blocks you; grief slows you; score floats over a tombstone; "memento mori" [23][24] | Widely cited as emotionally potent; Marcus Richter's parody mocked the reverence (Wikipedia) [24] | Rohrer opens his statement by saying viewers' interpretation matters more than his intent (snippet, UNVERIFIED) |

**Candidates verified in part:** *A Memoir Blue* (water = memory; trophies to photographs; Chen thanks her mother) [29][30]; *Venba* (food as the constant; restoring recipes) [31]; *Dordogne* (real places, watercolour) [32]; *The Gardens Between* (time scrubber; wordless) [33]; *Hindsight* (objects as apertures) [34]; *Dear Esther* (no gameplay; partly randomised narration) [35]; *Gone Home* (GDC 2014 "Why is Gone Home a game": interactivity and meaning; talk is free on GDC Vault) [36][68]. *Lake*, *Night in the Woods*, *Firewatch*: **no designer interview or postmortem obtained**; I only have store-page-grade summaries, so I do not rate them. **Firewatch was not searched at all.**

### Q2. Which mechanics work without a fail state, timer or dexterity, and which don't

**Work as-is for a mixed-age non-gamer audience (no fail/timer/precision):**
- Unpacking's placing (no score, timer, fail; "five-year-olds and 75-year-olds") [1][2], once drag is replaced with click-pick/click-place. Evidence that drag is risky: in the older-adult study, 50+ participants slid objects in the wrong direction, forgot to lift fingers, and failed double-taps [41] (touch evidence; trackpad drag is plausible but UNVERIFIED).
- Edith Finch's deaths "cannot be failed or reset" [12], but several vignettes use dual-stick and rapid inputs; keep the *structure* (room -> object -> scene), not the controls.
- Gris has no fail state [26]; the platforming still needs hands.
- Gardens Between's time dial (one control, no text) [33]; Dear Esther's walk with story [35]; To the Moon's point-and-click "interactive story" [16].
- Florence's tooth-brushing and speech bubbles are not hard by Wong's own account [5], but are touch gestures [41].
- Journey: simple enough for non-gamers on the multiplayer side per Chen [20]; controls need analog stick and jump [22].

**Need a gamer's hands: drop or convert to passive animation:**
- Webcam blinking (Before Your Eyes) [14][15]; analog-stick flight, two-stick control, quick-time sequences (Edith Finch Lewis; Journey) [12][22]; dragging terrain (Old Man's Journey) [19]; Spiritfarer's management and mini-games [28]; Passage's maze under arrow keys and a five-minute clock [24]; Minecraft survival (monsters appear at night [53]) and adventure-map genres (parkour, droppers, boss fights, puzzle rooms, "complete the monument") [63]; That Dragon, Cancer's racing minigame [18].

**Rule of thumb for our piece (my synthesis):** any interaction must (a) work as a single click, (b) have a visible next step, (c) work if nobody touches it (auto-advance), and (d) let a host pause. The metronome idea from Before Your Eyes is the template for (b)-(d). [14]

### Q3. How Unpacking and Edith Finch carry story through objects and rooms without narration, and what this teaches about real objects and homes

**Unpacking.**
- Design logic: snapshots, not a full story. Dawson: "You can learn a lot from snapshots, you can fill in the blanks." Items and story cross-pollinate; characters are built from character profiles; a recurring D&D game among housemates shows a bond without a scene. [3]
- Mechanic as meaning: the boyfriend's flat is a tutorial for "you can move other people's things," and the designers made his items fill the space, so the player feels intrusive and the story gets "he didn't make space for you." [3]
- Authenticity from real life: the game is personal to Brier; the pandemic made players recognise themselves. Foley: about 14,000 recorded sounds across objects and surfaces. Spreadsheets tracked new, repeated, and variant items per level. [3]
- Players complete the character with themselves: "I can put these bits of myself into her, and it becomes part of her." [3]

**Edith Finch.**
- Rooms as portraits: the core loop is find a Finch's room, learn personality from its objects, then play their death. Lewis's room (colored lighting, Murphy bed, paraphernalia, computers) signals him; a therapist's letter triggers the scene. [12]
- The decor was *revised late* after the team saw that Lewis's room conveyed his story without narration (Wikipedia citing developer interviews; verify). [13]
- Text lives on the objects; it directs attention and frames each scene as a recreation of a document. [12]
- Accounts may be unreliable; the player is unsure how accurate each is. [13]

**What it teaches for real objects and homes (my synthesis, grounded in the above):**
1. Use **few real objects, repeated** (the pig that follows the protagonist through moves in Unpacking is reported by reviews: UNVERIFIED) rather than many props.
2. Let **arrangement carry the relationship** (space left or not left for someone).
3. **Write nothing the room can say.** Where words are needed, set them on the object (a label on the jar), at reader-controlled pace.
4. **Photograph the real room as designed evidence**: the lived-in clutter, lighting, the wear on the doorframe; reconstruct that in your chosen style.
5. **Keep an object ledger** (spreadsheet: item, first/last appearance, room, story, who can confirm). This is how Witch Beam managed volume. [3]
6. **Make reconstructions look different from documents** (Edith Finch varies medium per account). [13]

### Q4. What Florence does with tiny interactions, mapped to a first job, a move, a breakup, a birth

What Florence actually does (sourced): speech-bubble jigsaws that ease as comfort grows and sharpen in arguments; tooth-brushing as routine; packing her things when Krish moves in and returning his when he moves out; a couch that is yellow when they are joyful; his music lifts her off her feet; her messy hair as a hard-to-control life; a cut level (visual only, not interactive) and a cut reunion chapter. [5][6][7][9]

| Moment | Specific mechanic for us (borrowed idea) | Why it is true to the idea | Needs from the family |
|---|---|---|---|
| **First job** | A repeated micro-action in the real job (stamp, till, keyboard, tool) that is clumsy at first and smooth by the end of the chapter; wake-up and commute loop before it | Florence's "routine rendered as a loop" (tooth-brushing, spreadsheets, take-out opening) [9]; *friction eases with skill*, mirroring how conversation eased. **My inference; Florence's job scenes were not detailed in the sources I read** | Real first-job object or uniform; one sentence on what the first week felt like |
| **A move** | Box-packing: click each real item into a box; one item refuses to be boxed (the thing carried everywhere) | Packing mini-games in Florence and Unpacking [3][9] | Photos of the actual items; the surviving object |
| **A breakup (only with consent)** | Hand things back: click to return a partner's items; the shared shelf empties by two slots. Argument expressed as sharper conversation pieces | Florence returns his things; arguments get sharp pieces [6][9]. Wong's cut "walled-up" level failed because it was only visual: **make it do something** [6] | Explicit permission from the person; likely the first chapter to cut (Principle 5) |
| **A birth** | Routine loop gains a second hand: the nightly loop (lights, kettle) gets slower and smaller with a new rhythm; viewpoint shows the parent's own hands | Florence routine changes with a partner [6]; Edith Finch's embodied body in first person [13]. **My inference** | The actual night-time routine; a sound of the real house |

### Q5. State of Minecraft memorial worlds and tribute maps (with provenance)

| Example | When | Who | What | How shared | Played or watched? | Provenance quality |
|---|---|---|---|---|---|---|
| JP Memorial Zoo | Built Nov 2016; article 2017-09-01 | Kirtland Menard, 10 (mother quoted) | Stone memorial with poppy, plus a zoo with every animal; octopus aquarium because Dad fished; smoked salmon in the cafe; he adds new animals as Minecraft adds them | Offline on his iPad, not published | Personal; shown to reporter | Local news interview [59]; maker quoted |
| "Gas Bandit" tribute | 2013-14 | Gas Bandit (name as given) | Towering bust of his wife Pauline (died 2013, age 41) holding a pickaxe, torches, underground room with candles/moat/music, plaque | YouTube video tour | **Watched** (condolences posted) | Salon/Daily Dot 2014 [57]; Everplans describes a minecart statue of "a woman he loved" via Reddit [58]; **original Reddit post/video not found** |
| Pendar2 / Emenbee hub | 2019 | Community of a server (over 1,500 concurrent at peak, over a million visitors) | Hub covered in sign messages | World download sent by server staff to Mojang's writer | Played/explored by the writer; community authored | Mojang's own article, 2019-04-06 [60] |
| Minecrapft (Pforzheimer House) | April 2020 | Harvard tutors and students | Scale replica of a house: 10,000+ brick blocks, survival mode, three weeks | Live server; virtual tour led by Faculty Deans on 2020-04-10; screenshots | **Both: people logged on to watch; creators played** | Student newspaper interviews [61] |
| The Uncensored Library | 2020; updated 2023 | Reporters Without Borders and BlockWorks | About 300 books in 12 wings | Server plus local download | Visitors read; designed to circulate offline | Mojang article, 2023-11-01 [62] (not a memorial; example of a text-heavy world) |

**Cinematic capture:** none of the above sources document how footage was shot. Standard tools are Replay Mod (record in a world, then fly a camera with keyframes and render via FFmpeg) and its successor Flashback, plus Mineways for static scenes. No memorial creator is documented using them (UNVERIFIED). [44][46][48]

**Adventure/story maps:** Mojang's feature on Diversity/Diversity 2 shows the genre's dominant forms (puzzle rooms, parkour, droppers, mazes, boss fights, "complete the monument" objectives); Diversity 2 holds a Guinness record for most downloaded map on Curse (as of the 2017 article). [63] I **found no notable story map that tells a real person's life**; the form is gamer-oriented. A novel-adventure-map commission (the *Gift* map built by Vechs) exists (GamesBeat snippet; date not verified). [72]

### Q6. When does a voxel look read as warm and handmade, versus meme or cheap asset pack?

No source directly studies this. What follows is **my synthesis from craft write-ups plus the memorial examples**; the craft facts are sourced, the conclusion is an inference.

| Lever | What the handmade-warm side does | What reads as meme/cheap |
|---|---|---|
| Subject | Hyper-specific personal subject (octopus aquarium for a fisherman; the actual dining hall) [59][61] | Generic builds; a famous landmark; default skins |
| Palette | Few colours; one base per material plus a highlight; reduce noise; shading painted into voxels; test mood by shifting the whole palette [64][65] | Default Minecraft textures; unplanned colour; busy noise |
| Resolution/scale | Constant voxel size across the scene; choose the smallest recognisable object first and size the scene to it (characters around 5 voxels wide) [65] | Mixed resolutions; Minecraft blocks beside fine-detail props |
| Silhouette | Avoid stair-stepped diagonals and surface bumps ("greebles") so shapes read [64] | Jaggies and noise |
| Light | Warm key light with sharp shadows plus softer cool fill; lighting rebuilt in Blender or Cinema 4D [65][66] | Flat default lighting |
| Build method | Block out with cubes, build modular assets, composite last; paint last to avoid rework [65][66] | One-click asset pack |
| Camera | **Inference:** diorama/isometric or a slow dolly rather than first-person "let's play"; no HUD overlays | Hotbar and hearts on screen, "achievement" popups |
| Honest approximation | A writer toured a Minecraft house replica and noted blocks permit only stylised recreation, yet memory is fuzzy anyway [61] | Claiming photo-accuracy |

Community criticism that Minecraft-style voxel art is "overused" appears in itch.io threads (snippet only; links not individually verified). [67] The Voxel Agents (the studio behind *The Gardens Between*) is a studio name; I have no evidence that game uses a voxel look.

### Q7. Current usage rules for Minecraft's name, textures and footage, and alternatives

**Verify against current Mojang/Microsoft terms before any public showing. I fetched the official pages on 2026-10-18; the Usage Guidelines page carries no visible date, and says the rules may change at any time. A third-party summary (ConductAtlas, snippet only) claims "last updated April 19, 2026": UNVERIFIED.** [42][43][71]

What the official pages say (paraphrase unless quoted):
- **Personal use:** "We are very relaxed about things you create for yourself. Pretty much anything goes there." [42]
- **Sharing counts as "commercial":** if you share your creation "with the community" (even free), Mojang treats it as a commercial thing and the Commercial Use guidelines apply. [42] A private family gift is not obviously "the community" (UNVERIFIED reading).
- **Videos, streams, screenshots:** allowed, may earn ad revenue if free to view with "enough of your own unique content"; you may not sell copies; distribution via paid services is "not cool." [42]
- **Public display of gameplay:** not allowed "within physical locations", e.g., promoting big-screen gameplay in a commercial venue like a restaurant, or charging for it in theatres. [42] A family premiere in a hired venue is a grey area: **ask a lawyer if it matters; Mojang says it can't advise on specific projects.** [42]
- **Name/brand/assets:** "assets" include textures, models, sounds, and videos or screenshots from the games. Do not imply it is official; use a disclaimer like "NOT AN OFFICIAL MINECRAFT [PRODUCT/SERVICE/EVENT/etc.]. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT"; "Minecraft" may appear only as a secondary descriptor, not the dominant title. [42]
- **Do not redistribute** the game, its files, or modified versions; the EULA also says not to give copies of content or make commercial use of anything they made. Original mods you build are yours, but you cannot distribute Modded Versions. [43]
- **Withdrawable:** all permissions "may be revoked at any time." [42][43]
- **Edition note:** Replay Mod docs don't mention Bedrock; Flashback is a Java/Fabric mod. Which edition the maker owns is unknown. [44][46]
- **Version note:** mod pages in October 2026 list Minecraft Java versions 26.1-26.3 alongside 1.21.x; Minecraft's version numbering appears to have changed (UNVERIFIED beyond those listings). [46][48]

**Practical positions (my recommendation):**
1. **Safest:** build the visuals as *original* voxel/low-poly assets: **MagicaVoxel** (free; license text not verified here; third-party sources say free for personal and commercial use) or **Blockbench** (open source GPL-3.0; its README says assets you create "are your own"; has a Minecraft-style cuboid mode). No Mojang textures, so no brand questions. [49][50][51]
2. **If Minecraft itself is wanted:** private screening, no payment, no advertising, no Mojang logo, own textures where possible, unique content on top of footage, disclaimer in credits; re-check the guidelines on the week of the premiere.
3. **Worlds as keepsakes:** do not share a modified install; sharing a bare world save is common practice (Mojang itself received one from Emenbee staff [60]) but its status under the EULA is **UNVERIFIED**.

### Q8. Which mappings are strongest for a 50+ life, which are clichés, which can be inverted

| Mapping | Verdict | Why | Inversion/specific twist |
|---|---|---|---|
| **Map fills in as world widens** | Strong | Minecraft map item records only where you have been; copies sync; lock freezes a copy [52]; the family's SVG skills fit | Radius shrinks in later years; a locked copy of a place that no longer exists |
| **Inventory as treasured objects** | Strong if 5-9 *real* things; cliché as a grid of icons | Spiritfarer: objects are a trace, the person is what remains [27] | A shelf slot that stays empty; an object that was lost in a move (despawn after five minutes in Minecraft [54]) |
| **Biomes as chapters** | Weak if generic; strong as *real places*; Dordogne chooses actual places by story [32] | Generic desert/forest fails swap-the-subject | **A biome that is gone:** a demolished house, closed factory, a country whose name changed; draw it as empty/fog. Minecraft does not despawn dropped items in unloaded chunks [54] (poetic: things persist where nobody looks; my gloss) |
| **Building a house = building a family** | Cliché unless it is *the* house; Kirtland shows building *for* someone from their loves [59] | "Home sweet home" is a stock image | Tear it down as the children leave (reverse unpacking); the same door fitted into the next house |
| **Day/night = seasons of life** | Cliché ("circle of life") | Minecraft day is 20 minutes [53] | Night as the best-remembered time (night shifts, new-baby nights); a bed that skips the night = vanished years [53] |
| **Crafting = skills learned** | Strong if the real hands and recipe; cliché as a 3x3 grid | Venba: recipes as the constant that measures change [31] | A recipe with a step nobody remembers, marked as lost, not invented (Principle 4) |
| **Achievements = milestones** | **No** (anti-pattern 1) | [37][38] | Trophies moved aside to photographs [30] |
| **Redstone** | Gimmick unless the subject worked with circuits | **UNVERIFIED** | Light switches in a real house, if true |
| **Chest you cannot open** | Strong for sensitive chapters | Minecraft Vault needs its own key; each player opens once [55] | A locked door that the family chooses to leave locked (Principle 5) |
| **Death/respawn** | Avoid for a living subject | Respawn at bed [54] | Use the bed image only |
| **Passage-style strip** | Strong | Lifetime as a horizontal strip [23] | End at "now," road continues |

### Q9. Accessibility practices for older players and a shared big-screen setting

Sourced practices:
- **No time pressure.** Older-adult study design guide DG25: "eliminate time limits or provide alternatives"; participants felt nervous and stressed by time limits. [41]
- **Reading pace.** Dismiss text when the player acts, not on a timer; allow replay or pause. [40]
- **Simple controls.** "Ensure controls are as simple as possible, or provide a simpler alternative"; "avoid multiple button controls at the same time" (DG7); important buttons easy to find and touch (DG9). [39][41]
- **Do not make precise timing essential;** offer alternatives, pausable actions or a skip. [39]
- **Subtitles/captions.** Provide subtitles for all important speech; clear presentation; customisable; readable default font size; high contrast text; no information in sound alone. [39]
- **Size.** Options for font and object size (DG3); distinguishable important objects (DG1); step-by-step presentation instead of dense screens (DG5). [41]
- **Touch pitfalls.** Older participants slid in the wrong direction, failed double-taps, forgot to lift fingers; highlight touch areas (DG11) and limit the operating area (DG14). [41]
- **Story tone.** Don't show older adults' lives in static, passive, negative or depressed tones; avoid simple/clichéd stories (participants disliked those). [41]
- **Co-play.** Consider co-play in single-player modes (DG32). [41]
- **Skip/assist.** Offer a bypass for non-core gameplay; assist modes. [39]
- **Gris** designed with accessibility in mind by removing fail states. [26]
- **Brier** says Unpacking works from 5 to 75. [1]
- **Big-screen additions (my synthesis):** host controls (space = pause), auto-advance with chimes, large text sized for the back of the room, no flashing, no hover-only UI, audio plus caption together, sound levels for hearing loss, a "play from here" resume point, and a remote-friendly single "next" key.

**Evidence limits:** the older-adult study had 40 participants, mobile games, mean age 66.75, and is qualitative; Game Accessibility Guidelines are a community checklist, not a standard; trackpad-specific data for older adults is **not found**. [39][41]

---

## Exemplars / recipes

Each: what it is, why it works, how it was made, what we can reuse, link.

**E1. Unpacking (Witch Beam, 2021).** *What:* wordless life story as objects in rooms. *Why it works:* tiny verb (place), no fail/score/timer; mechanic becomes narrative; player projects self. *How made:* "subtractive design" at prototype; object/story cross-pollination; spreadsheets for items and levels; 14,000 foley sounds; loosened puzzle rules. *Reuse:* object ledger, "one surviving object", arrangement-as-relationship, 8 snapshot years rather than 50. [1][2][3] Links: https://www.gamedeveloper.com/design/unpacking-the-design-pillars-of-a-chill-puzzle-game ; https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game

**E2. Florence (Mountains, 2018).** *What:* a relationship as 20 short interactions. *Why:* friction mirrors feeling; music replaces voices; cut ideas that were only visual. *How:* chapters pinned to a wall and replaced as ideas failed; hand-sketched art scanned; composer Kevin Penkin's music stands in for the characters. *Reuse:* friction budget; interaction-over-puzzle; cut what doesn't act. [5][6][7] Links: https://www.player.one/florence-game-ken-wong-interview-123975 ; https://milanote.com/the-work/lead-designer-of-monument-valley-deconstructs-his-latest-game-florence

**E3. What Remains of Edith Finch (Giant Sparrow, 2017).** *What:* house of preserved rooms with a different mechanic per person. *Why:* room first, then story; each person gets own idiom; ambiguity respected. *How:* many prototypes; culled by playtest emotion; late decor rewrite to carry character. *Reuse:* room-as-portrait; per-person style (limit to 3-5); visible reconstruction. [10][11][12][13] Links: https://gdcvault.com/play/1025016/Weaving-13-Prototypes-into-1 ; https://gamesbeat.com/the-story-behind-the-haunting-what-remains-of-edith-finch/

**E4. Passage (Jason Rohrer, 2007).** *What:* lifetime in five minutes. *Why:* every element is a statement (screen = life; chests = pursuits; spouse = joint travel; score = pointless at the end). *How:* made for a 256x256, five-minute competition; shown at 100x16. *Reuse:* a horizontal life strip; companion changes movement; score refused. [23][24] Link: https://hcsoftware.sourceforge.net/passage/statement.html

**E5. A Memoir Blue trophy-to-photograph ending.** *What:* the last puzzle lifts aside trophies to reveal photos with her mother. *Why:* turns achievements into obstacles to intimacy. *How:* Chen's autobiographical thesis project; water as memory. *Reuse:* the single most transferable "anti-checklist" device. [29][30] Links: https://www.avclub.com/shelley-chen-a-memoir-blue ; https://www.inverse.com/gaming/memoir-blue-ending-explained

**E6. Before Your Eyes metronome fix.** *What:* blink input only counts when the metronome shows. *Why:* removes involuntary-skip frustration while keeping time-passing metaphor. *How:* lead designer Bela Messex's "language to differentiate blinks"; team nearly collapsed over years. *Reuse:* chime-gated pacing for a shared screen; locations from the team's own childhoods. [14][15] Link: https://www.gamedeveloper.com/marketing/a-seven-year-blink-of-an-eye-before-your-eyes-s-dev-woes-deconstructed

**E7. Kirtland's zoo (2016-2017).** *What:* a boy's offline Minecraft memorial. *Why:* every element is a fact about the father (animals, fishing, smoked salmon); alive, still tweaked. *How:* started the same day he heard the news. *Reuse:* build from loves, not from "memorial vocabulary"; a living, updated piece. [59] Link: https://www.sootoday.com/great-stories/son-builds-virtual-minecraft-zoo-and-memorial-to-honour-his-deceased-father-9-photos-707477

**E8. Minecrapft (2020).** *What:* shared replica of a house. *Why:* scale, floor plans, live tour, recognisable rooms; visitors "recognition in students' voices." *How:* floor plans + Google Maps, survival mode, 10,000+ bricks, three-week crunch to a hard deadline (Housing Day). *Reuse:* deadline as a social event; a host leading a tour; a deadline-driven build. [61] Link: https://www.thecrimson.com/article/2020/4/30/minecraft-pfo/

**E9. Pendar2 / Emenbee (2019).** *What:* a hub of signs. *Why:* many small human voices; the reader "couldn't stop wandering." *How:* community-written, preserved as a downloadable world. *Reuse:* a wall of short messages from relatives. [60] Link: https://www.minecraft.net/en-us/article/remembering-pendar2

**E10. Spiritfarer's belongings and care loop.** *What:* a cozy management game about helping the dying. *Why:* mundane tasks sit beside the hardest moment; building for others. *How:* Guérin researched end-of-life facilities for a month; drew on his own losses. *Reuse:* show caring labour; farewell scenes only with consent. [27][28] Link: https://www.pockettactics.com/spiritfarer/interview

---

## Tools

All prices/versions as of 2026-10-18, as seen on the cited pages. Maker's OS and Minecraft edition are **unknown** (apps not yet listed).

| Tool | Cost / license | Platform | Learning curve | Scriptability / CLI | Notes |
|---|---|---|---|---|---|
| **Minecraft Java Edition** | Paid; price not verified | Win/Mac/Linux | Low to play; building takes time | Worlds are folders; commands in game; external scripting **UNVERIFIED here** | Official terms in Q7 [42][43] |
| **Minecraft Education** | Account-based; cloud saving rules change (older versions lose cloud saving from 2026-10-01, snippet) | Win/Mac/iPad/Chromebook | Low | Export as .mcworld (Education help, snippet) | Cannot convert Education worlds to Bedrock (snippet) [75] |
| **Replay Mod** | Free, GPL-3.0 | Java; Fabric for 1.14+, Forge for 1.12.2 and below | Medium; keyframe UI like a video editor | GUI; FFmpeg required for rendering; headless use **UNVERIFIED** | Records loaded chunks around you; client-side only; camera path keyframes: position, time, spectator; cubic spline default; no Bedrock mention [44][45] |
| **Flashback** | Free; source license All Rights Reserved; Fabric client mod; 12.8M downloads; supports Java 26.1-26.3 and 1.21.x listings | Java/Fabric | Medium | GUI; add-ons FlashBatch (queue renders), Flashback Extras (export presets), FlashPlus (VFX camera export) are snippet-only [72] | Described as the modern Replay Mod successor; page lists record/playback; editor/export features were not confirmed from the page [46] |
| **Mineways** | Free, open source (version 14.01, updated 2026-10-03) | Windows main download; Mac/Linux help sections | Medium | Command-line options **UNVERIFIED** | Exports Java worlds (up to 26.3) to OBJ and USD for Blender, Houdini, Cinema 4D; Bedrock worlds need conversion; resource-pack licensing not stated [48] |
| **MagicaVoxel** | Free; "free for personal and commercial use" per third-party sites; official license text not verified | Windows, macOS (per third-party) | Low | GUI; exports OBJ, sprites, isometric renders; internal GPU path-tracing renderer with emission/glass, DOF, bloom (snippet) | Download and read LICENSE.txt before relying on this [51] |
| **Blockbench** | Free; GPL-3.0; assets you make are yours | Web app + desktop (Electron) | Low-Medium | Plugin API; no CLI found | Cuboid "Minecraft-style" modelling and mesh tools; animation with keyframes [49][50] |
| **Blender** | Not researched in this track | | | Python scriptable (known from general knowledge; confirm in `toolchain`) | Used in voxel diorama pipelines for lighting [65] |
| **FFmpeg** | Free | All | Medium | CLI | Required by Replay Mod rendering [44] |

---

## Techniques

1. **Subtractive design (Brier).** Before building, list what each chapter does NOT need; cut anything "that isn't serving the core ideas." Apply at the storyboard stage. [1]
2. **Three adjectives, then three pillars.** Brier's team listed feelings, then refined to contemplation, discovery, expression. Do the same for our piece before choosing patterns. [1]
3. **"Does this scene help the audience love X more?" (Green).** Run every scene through it. [17]
4. **Object ledger.** Spreadsheet columns: item, source photo, room/chapter, first/last appearance, recurring?, story, who confirmed, ok to show? (Unpacking used spreadsheets for items and levels.) [3]
5. **Two-direction invention.** Start from an object, ask what story it tells; start from a story, ask what object it needs; keep only those confirmed by the family. [3]
6. **Mechanic-as-beat.** Let a constraint of the interaction carry meaning (crowded shelf = no room made). [3]
7. **Friction budget (Florence).** Make small interactions harder in nervous or conflict moments and easier in settled ones. [5][6]
8. **Pause chime / metronome gating (Before Your Eyes).** The screen tells the room when to pause or interact; otherwise it plays on. [14]
9. **Playtest for emotion, not comprehension (Dallas).** Show a rough cut to two relatives and keep what makes them talk. [11]
10. **Per-person idiom, capped.** At most 3-5 chapters get their own visual style. [10][11]
11. **Label reconstructions.** Different medium or texture for reconstructed scenes versus documents. [13]
12. **Real-location selection.** Choose settings the story needs; sketch on site. [32]
13. **Voxel diorama pipeline.** Block out scene with cubes; model each asset separately in MagicaVoxel (255-colour palette adjustable globally); import to Blender; add bevels and PBR materials; warm key light with sharp shadows plus softer cool fill; paint last. [65][66]
14. **Voxel readability.** Few colours; paint shading into voxels with hue and brightness contrast; avoid stair-stepped diagonals; keep one resolution. [64]
15. **Replay Mod capture.** Install the Fabric/Forge-appropriate mod and FFmpeg; start a recording when joining the world; pause the replay; add position keyframes (and time keyframes for speed changes); preview; render to video. Only chunks loaded on your client are recorded. [44]
16. **Static Minecraft scenes to Blender.** Mineways export (OBJ/USD) -> Blender; match scale; apply your own textures (not Mojang's) if the piece will be public. [48]
17. **Watch-first design.** Assume a narrator in the room; add "pause and ask" cards such as "Who remembers this kitchen?" Twitch viewers already tell stories while watching Unpacking. [3]
18. **Inversion toolbox.** Lost item (despawn), locked vault, vanished biome, trophies removed. [30][54][55]

---

## Pitfalls and ethics

- **Gamification rhetoric.** Points and badges are the weakest part of games; building a milestone scoreboard turns a person into a leaderboard. [37][38]
- **Mood-board copying.** Unpacking's team reports clones are "hollow" despite looking easy. Reuse devices; re-ground in facts. [3]
- **Death register.** The subject is alive. Passage's "memento mori", Spiritfarer's farewells, TDC's grief and Edith Finch's deaths are devices, not tone. [23][27][41]
- **Consent and dignity (Principle 5).** Green asked himself whether to release a story "when we weren't the winners here"; he also faced critics asking why he should memorialise his son this way. Treat any hard chapter with the family's say. [17][18]
- **Reconstruction honesty (Principle 4).** Edith Finch's accounts may be unreliable and are styled differently; do the same so reconstructions are visibly reconstructions. [13]
- **Minecraft IP.** See Q7; permissions are revocable; Mojang won't evaluate a specific project. [42]
- **Second-hand memorial stories.** Several are reported by third parties; original posts weren't found (Gas Bandit). Do not repeat them as fact without the original. [57][58]
- **Creator context.** Florence's director faced public allegations of emotional abuse (2019, with a March 2022 *People Make Games* video) per Wikipedia, and apologised. If we credit the game publicly, decide knowingly. (Not verified against primary reporting here.) [9]
- **Link hygiene.** `hideandseek.net/2010/10/06/cant-play-wont-play/` (the original Robertson essay) now **redirects to an unrelated gambling domain**; I did not follow it and used the Kotaku republication. Treat the old URL as unsafe. [37]
- **Webcam/eye-tracking.** Privacy and discomfort; some players reported dry-eye issues (aggregation, UNVERIFIED). [69]
- **Assets from Minecraft in a public screening.** If Mojang textures/mobs appear on a big screen at a venue, re-read the clause on public display. [42]
- **Quoting.** Keep quotes short; paraphrase talks; credit games and designers in the piece.

---

## Open questions / gaps

1. **GDC Vault talks not watched.** Dallas (2018), Brier (2023), Chen (2013), Gaynor (2014 is free). I used write-ups and listings. The orchestrator or maker should watch the Brier "Fail States or Scores" and Gaynor talks. [2][10][36]
2. **Original Gas Bandit post or video** not located. [57][58]
3. **No story map about a real person's life** found in Minecraft culture; the genre is challenge-based. [63]
4. **How memorial creators captured footage** is undocumented in what I found. [44][46]
5. **Redstone** not researched (UNVERIFIED).
6. **Firewatch not searched; Lake and Night in the Woods had no designer interview or postmortem** retrieved.
7. **Player-report evidence** for Gris, Spiritfarer and Old Man's Journey missing.
8. **MagicaVoxel official license text** not seen; verify in the download.
9. **Minecraft terms date** unknown; recheck in the week of the premiere. A family premiere in a hired space needs a decision. [42]
10. **Trackpad drag for older adults:** no direct study found; recommend a 10-minute test with a real 70-year-old on the actual hardware.
11. **Which Minecraft edition and OS the maker has** (Java vs Bedrock changes capture options).
12. **Principle 2 testing** needs the subject's real facts from the `story` track; this note provides devices, not the content.
13. **Hand-offs:** `format` track decides engine and delivery; `animated` track compares documentary precedents; `toolchain` checks Blender, FFmpeg and scripting; `ai-imagery` covers restoring real photos used inside these patterns.

---

## Sources

Tier tags: [P] primary designer/creator/official; [S] journalism quoting designers; [T] Wikipedia/aggregator; [snippet] seen only in search results, not read. All pages fetched 2026-10-18 unless noted.

**Designer talks, interviews, postmortems**
[1] Danielle Riendeau — "'Unpacking' the design pillars of a chill puzzle game" — https://www.gamedeveloper.com/design/unpacking-the-design-pillars-of-a-chill-puzzle-game — 2023-04-21 — [S] summary of Wren Brier's GDC 2023 talk.
[2] GDC Vault — "'Unpacking' Zen: Designing a Game Without Fail States or Scores" (Wren Brier, GDC 2023) — https://www.gdcvault.com/play/1029400/-Unpacking-Zen-Designing-a — 2023 — [P] listing seen via search; video not viewed.
[3] Eurogamer — "The creators of Unpacking on developing a 'weird', queer, BAFTA-winning game" — https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game — April 2022 — [S] Brier and Dawson; read in full.
[4] GoNintendo — "Unpacking devs reveal how they crafted a near-wordless story" — https://gonintendo.com/contents/1958-unpacking-devs-reveal-how-they-crafted-a-near-wordless-story — 2022-04-12 — [S] summary of [3]; used for date.
[5] Player.One — Ken Wong interview, "Florence Tells A Love Story With Actions, Not Words" — https://www.player.one/florence-game-ken-wong-interview-123975 — 2018-02-12 — [S] puzzle easing, "interactions".
[6] Milanote / Ollie Campbell — "The Lead Designer of Monument Valley Deconstructs His Latest Game, Florence" — https://milanote.com/the-work/lead-designer-of-monument-valley-deconstructs-his-latest-game-florence — undated (post-2018) — [S] mechanics, cut chapters.
[7] MCV/DEVELOP — "Florence: How game design can tell love stories" — https://mcvuk.com/?p=23751 — 2018-03-14 — [S] unspecified argument; soundtrack.
[8] PocketGamer.biz — "Mountains' Ken Wong on moving on from Monument Valley to Florence" — https://www.pocketgamer.biz/asia/interview/69925/mountains-ken-wong-on-moving-on-from-monument-valley-to-florence/ — 2019-01-31 — [S] players cried; wider audience.
[9] Wikipedia — "Florence (video game)" — https://en.wikipedia.org/wiki/Florence_(video_game) — fetched 2026-10-18 — [T] chapters, packing mini-games, reception, allegations.
[10] GDC Vault — "Weaving 13 Prototypes into 1 Game: Lessons from 'Edith Finch'" (Ian Dallas, GDC 2018) — https://gdcvault.com/play/1025016/Weaving-13-Prototypes-into-1 — 2018 — [P] listing only.
[11] GamesBeat — "The story behind the haunting What Remains of Edith Finch" — https://gamesbeat.com/the-story-behind-the-haunting-what-remains-of-edith-finch/ — 2017-07-21 (updated 2025-06-19) — [S] Dallas quotes.
[12] RPGFan — Aleks Franiczek, "Narrative Design Analysis: What Remains of Edith Finch?" — https://www.rpgfan.com/feature/narrative-design-analysis-what-remains-of-edith-finch/ — 2024-12-15 — [S] rooms, vignette mechanics.
[13] Wikipedia — "What Remains of Edith Finch" — https://en.wikipedia.org/wiki/What_Remains_of_Edith_Finch — fetched 2026-10-18 — [T] development notes, decor revision, reception.
[14] Game Developer — Sam Machkovech, "A seven-year blink of an eye: Before Your Eyes' woes deconstructed at GDC" — https://www.gamedeveloper.com/marketing/a-seven-year-blink-of-an-eye-before-your-eyes-s-dev-woes-deconstructed — 2023-03-22 — [S] Graham Parkes's GDC 2023 talk.
[15] MCV/DEVELOP — Vince Pavey, "When We Made… Before Your Eyes" — https://mcvuk.com/business-news/when-we-made-before-your-eyes/ — 2023-05-18 — [S] Oliver Lewin.
[16] Alternative Magazine — Martin Mulrooney, "In Conversation With Kan Gao" — https://alternativemagazineonline.co.uk/2011/12/30/interview-in-conversation-with-kan-gao-freebird-games-to-the-moon/ — 2011-12-30 — [P/S].
[17] Game Developer — Christian Nutt, "Game as memorial: That Dragon, Cancer developer reflects" — https://gamedeveloper.com/design/game-as-memorial-i-that-dragon-cancer-i-developer-reflects — 2014-11-12 — [S].
[18] The Spinoff — Tof Eklund, "'Death is the thing we all share'" — https://thespinoff.co.nz/pop-culture/02-06-2017/death-is-the-thing-we-all-share-why-one-father-made-a-video-game-about-his-sons-cancer-battle — 2017-06-02 — [S] Ryan Green.
[19] Game Developer — Joel Couture, "Road to the IGF: Broken Rules' Old Man's Journey" — https://www.gamedeveloper.com/design/road-to-the-igf-broken-rules-i-old-man-s-journey-i- — 2017-02-08 — [S].
[20] Adventure Gamers — "GDC 2013: Designing Journey" — https://adventuregamers.com/article/designing_journey — 2013-04-05 — [S] Jenova Chen's talk.
[21] Destructoid — Steven Hansen, notes on Jenova Chen's GDC talk — https://www.destructoid.com/journey-inspired-by-world-of-warcraft-loneliness/ — 2013-03-29 — [S].
[22] Wikipedia — "Journey (2012 video game)" — https://en.wikipedia.org/wiki/Journey_(2012_video_game) — fetched 2026-10-18 — [T] controls, no text, testers crying (page text partially read).
[23] Jason Rohrer — Passage statement — https://hcsoftware.sourceforge.net/passage/statement.html — undated (c. 2007) — [P].
[24] Wikipedia — "Passage (video game)" — https://en.wikipedia.org/wiki/Passage_(video_game) — fetched 2026-10-18 — [T].
[25] Gamereactor — David Caballero, "What does GRIS mean? We talk to Nomada Studio" — https://www.gamereactor.eu/what-does-gris-mean-we-talk-to-nomada-studio/ — 2018-12-04 — [S] Adrián Cuevas.
[26] Wikipedia — "Gris" — https://en.wikipedia.org/wiki/Gris — fetched 2026-10-18 — [T] no fail state, grief, accessibility.
[27] Pocket Tactics — "Love, Death, and Margot Tenenbaum — the many inspirations of Spiritfarer" — https://www.pockettactics.com/spiritfarer/interview — updated 2021-08-13 — [S] Nicolas Guérin.
[28] Wikipedia — "Spiritfarer" — https://en.wikipedia.org/wiki/Spiritfarer — fetched 2026-10-18 — [T].
[29] The A.V. Club — George Yang, Shelley Chen on A Memoir Blue — https://www.avclub.com/shelley-chen-a-memoir-blue — 2021-12-07 — [S].
[30] Inverse — Jess Reyes, "What happened with Miriam and her mom at the end of A Memoir Blue?" — https://www.inverse.com/gaming/memoir-blue-ending-explained — 2022-04-06 (updated 2024-02-20) — [S] trophies-to-photographs ending.
[31] Game Developer — Joel Couture, on Venba — https://www.gamedeveloper.com/design/how-venba-uses-food-to-explore-connections-and-disconnections-with-culture-for-immigrants — 2024-03-22 — [S] Abhi.
[32] Xbox Wire — Cédric Babouche, Dordogne real-world locations — https://news.xbox.com/en-us/2023/05/30/dordogne-france-real-world-locations/ — 2023-05-30 — [P].
[33] WellPlayed — Zach Jackson, The Voxel Agents on The Gardens Between — https://www.well-played.com.au/made-in-australia-we-talk-the-gardens-between-with-the-voxel-agents/ — 2018-09-21 — [S] Henrik Pettersson.
[34] GoNintendo — "Hindsight dev explains how the game pulls from their real-life experiences" — https://gonintendo.com/contents/8255-hindsight-dev-explains-how-the-game-pulls-from-their-real-life-experiences — 2022-08-23 — [S] quotes Joel McDonald.
[35] Game Informer — Adam Biessener, Q&A with Dan Pinchbeck — https://gameinformer.com/games/dear_esther/b/pc/archive/2011/04/17/in-depth-q-amp-a-with-creator-dr-dan-pinchbeck — 2011-04-17 — [S].
[36] Game Developer — "Video: Why is Gone Home a game?" — https://www.gamedeveloper.com/design/video-why-is-i-gone-home-i-a-game- — 2014-05-26 — [P] Steve Gaynor GDC 2014; free video on GDC Vault.

**Critique of gamification, accessibility**
[37] Kotaku (republished with permission) — Margaret Robertson, "Can't Play, Won't Play" — https://kotaku.com/cant-play-wont-play-5686393 — 2010-11-10 — [P] pointsification.
[38] Ian Bogost — "Gamification is Bullshit" — https://www.bogost.com/blog/gamification_is_bullshit/ — 2011 — [P].
[39] Game Accessibility Guidelines — full list — https://gameaccessibilityguidelines.com/full-list/ — fetched 2026-10-18 — community checklist.
[40] Game Accessibility Guidelines — "Allow players to progress through text prompts at their own pace" — https://gameaccessibilityguidelines.com/allow-players-to-progress-through-text-prompts-at-their-own-pace — fetched 2026-10-18.
[41] Lee S, Oh H, Shi C-K, Doh YY — "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8176340/ (text retrieved via NCBI E-utilities) — 2021 — [P] 40 participants, mean age 66.75.

**Minecraft rules and tools**
[42] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18; no visible date — [P].
[43] Mojang/Microsoft — Minecraft End User License Agreement — https://www.minecraft.net/en-us/eula — fetched 2026-10-18 — [P].
[44] Replay Mod documentation — https://www.replaymod.com/docs — fetched 2026-10-18 — [P].
[45] ReplayMod on GitHub — https://github.com/ReplayMod/ReplayMod — fetched 2026-10-18 — [P] GPL-3.0.
[46] Modrinth — Flashback — https://modrinth.com/mod/flashback — fetched 2026-10-18 — [P] license ARR, Fabric, 12.8M downloads.
[47] Modrinth — Flashback Settings — https://modrinth.com/project/mOIDKWOa — fetched 2026-10-18 — [P] note: add-on; PolyForm Noncommercial; telemetry on by default.
[48] Mineways — https://erich.realtimerendering.com/minecraft/public/mineways/ — fetched 2026-10-18 — [P] version 14.01, updated 2026-10-03.
[49] Blockbench — https://blockbench.net/ — fetched 2026-10-18 — [P].
[50] Blockbench README — https://cdn.jsdelivr.net/gh/jannisx11/blockbench@master/README.md — fetched 2026-10-18 — [P] GPL-3.0; assets are yours.
[51] VoxelFans — MagicaVoxel page (third-party) — https://voxelfanscom.nuxt.dev/magicaVoxel — fetched 2026-10-18 — [T] "free for personal and commercial use"; official license unverified.
[52] Minecraft Wiki — Map — https://minecraft.wiki/w/Map — fetched 2026-10-18.
[53] Minecraft Wiki — Daylight cycle — https://minecraft.wiki/w/Daylight_cycle — fetched 2026-10-18.
[54] Minecraft Wiki — Death — https://minecraft.wiki/w/Death — fetched 2026-10-18.
[55] Minecraft Wiki — Vault — https://minecraft.wiki/w/Vault — fetched 2026-10-18.
[56] Minecraft Wiki — Item Frame — https://minecraft.wiki/w/Item_Frame — fetched 2026-10-18.

**Memorials and worlds**
[57] Salon (from The Daily Dot) — "Gamer uses 'Minecraft' to pay tribute to his wife" — https://salon.com/2014/03/13/gamer_uses_minecraft_to_pay_tribute_to_his_wife_partner — 2014-03-13 — [S] second-hand; original not found.
[58] Everplans — Adam Seifer, "Minecraft video game memorial honors loved one" — https://everplans.com/articles/minecraft-video-game-memorial-honors-loved-one — undated — [S] cites a Reddit post (not found).
[59] SooToday — Jeff Klassen, "Son builds virtual Minecraft zoo and memorial to honour his deceased father" — https://www.sootoday.com/great-stories/son-builds-virtual-minecraft-zoo-and-memorial-to-honour-his-deceased-father-9-photos-707477 — 2017-09-01 — [S] interview.
[60] Minecraft.net — Tom Stone, "Remembering Pendar2" — https://www.minecraft.net/en-us/article/remembering-pendar2 — 2019-04-06 — [P].
[61] The Harvard Crimson — Olivia Gopnik-Parker, "A House, Pixelated, Can Stand" — https://www.thecrimson.com/article/2020/4/30/minecraft-pfo/ — 2020-04-30 — [S].
[62] Minecraft.net — "The Uncensored Library" — https://www.minecraft.net/en-us/article/uncensored-library — 2023-11-01 — [P].
[63] Minecraft.net — Alex Wiltshire, "The Making of Diversity" — https://minecraft.net/article/making-diversity — 2017-02-02 — [P].

**Voxel craft**
[64] Game Developer — Zach Soares, "Voxel Art: Reducing the Greebles" — https://www.gamedeveloper.com/design/voxel-art-reducing-the-greebles — 2017-06-05.
[65] 80.lv — Gabriel de Laubier, "Using Voxels for Simple Dioramas" — https://80.lv/articles/using-voxels-for-simple-dioramas — 2017-07-26.
[66] 80.lv — Thibault Simar, "Voxel Dioramas: Tips and Tricks" — https://80.lv/articles/voxel-dioramas-tips-and-tricks/ — 2017-06-22.

**Seen only in search results (snippet, not read; treat as leads)**
[67] itch.io community threads on "overused" Minecraft-style voxel art — e.g., https://itch.io/post/7116282 — undated — [snippet].
[68] PC Gamer — Gone Home interview with Steve Gaynor — https://pcgamer.com/gone-home-steve-gaynor-interview — fetch returned paywall only — [snippet].
[69] Before Your Eyes reviews — https://fingerguns.net/reviews/2021/04/06/before-your-eyes-review-blink-back-tears/ ; https://www.thesixthaxis.com/2021/05/05/before-your-eyes-review/ ; https://gamingtrend.com/reviews/dont-blink-or-youll-miss-it-before-your-eyes-review/ — 2021 — [snippet] mouse alternative, calibration, emotional reactions.
[70] Giant Bomb wiki (Edith Finch; secondhand GameSpot interview on closed doors) — https://giantbomb.com/wiki/Games/What_Remains_of_Edith_Finch ; Hypercritic review https://hypercritic.org/collection/what-remains-of-edith-finch-2021-review — [snippet].
[71] ConductAtlas third-party summary of Minecraft Usage Guidelines — https://conductatlas.com/platform/minecraft/minecraft-usage-guidelines/commercial-use-and-monetization-restrictions/ — [snippet]; claims "last updated April 19, 2026": UNVERIFIED.
[72] Flashback add-ons and Blender bridges (FlashBatch https://modrinth.com/mod/flashbatch ; Flashback Extras https://modrinth.com/mod/flashback-extras ; ModRig https://www.curseforge.com/minecraft/mc-mods/modrig ; Replay Mod exporter https://github.com/Sam54123/mc-world-export) and the *Gift* adventure map (https://gamesbeat.com/minecraft-makes-multimedia-history/) — [snippet].
[73] games.gg To the Moon overview (claims "no game-over states") — https://games.gg/to-the-moon/ — [snippet, low tier].
[74] Midlothian Advertiser — Robert Burns's Ellisland Farm rebuilt in Minecraft by Glasgow students — https://www.midlothianadvertiser.co.uk/heritage-and-retro/heritage/former-home-of-robert-burns-brought-to-virtual-life-on-minecraft-3788412 — [snippet] (heritage example, not a family memorial).
[75] Minecraft Education support — Import, Export, and Manage Worlds — https://edusupport.minecraft.net/hc/en-us/articles/360047555391-Import-Export-and-Manage-Worlds — [snippet].

---

## Follow-up research (round 1)

Researcher: Sonnet · 2026-10-18 (Sunday) · answers the seven follow-ups in `reviews/games-round1.md`. Sources continue the numbering at [76]; [3], [14], [15], [42], [43], [48], [51], [71] are re-read, not re-numbered. Dated excerpts and file hashes for later change detection are in `research/excerpts/games-round1-followup-2026-10-18.txt`.

**Three honest caveats first.**
1. **This session ran in the cloud Linux container, not on the maker's Windows PC.** I found no `.minecraft` folder, no Windows mount and nothing in `/mnt/user-data`. So nothing below was checked on the maker's machine, and Q5 (ownership) cannot be answered by research.
2. **The web-search tool refused after my first call** ("this turn's budget is used up", shared by all agents). I used direct page fetches only. Q7 (older adults and TV remotes) therefore got **no fresh literature search**; it is marked NOT RESEARCHED below, not "no evidence exists".
3. **Eurogamer and minecraft.net were reachable today** (HTTP 200), so Q4 and Q6 did not need the maker's PC.

### F1. MagicaVoxel: licence and command-line or batch mode

**Premise corrected: there is no `LICENSE.txt` in the Windows download.** I downloaded the current Windows build (`MagicaVoxel-0.99.7.2-win64.zip`, 3,794,277 bytes, 70 entries, sha256 `58320b90...e4d873`) and listed it. It holds `MagicaVoxel.exe`, `config/`, `ibl/`, `palette/`, `shader/`, `vox/` and a `readme.txt` (version, date 10/31/2025, credits for Open Image Denoise, HDRI-Hub, icon sets and the Mini Mike's Metro Minis sample). The 0.99.7.1 and 0.99.6.4 zips also have only a `readme.txt`. A string search of the `.exe` found no licence text. [78]

**Where the licence actually is.** The home page is a shell: it loads `mv_main.html` into itself with JavaScript, so a plain fetch shows only navigation and the footer "Copyright © ephtracy 2011-2021". The loaded fragment has a **License** block, quoted in full: [76]
- "Free to use for any project."
- "Credits to the software are appreciated."
- "Selling or distributing the software (original or modified) in other packages are disallowed."

What this means for us (my reading, not legal advice):
- The words "personal" and "non-commercial" **do not appear**; "any project" covers a private family film and, on its face, commercial work too. This upgrades the second-hand claim in [51] to a primary source.
- Add a credit line for MagicaVoxel in the end credits. Do not bundle the app itself on a USB stick or in a package for relatives.
- Nothing is said about exported models, images or video. Exports are plainly meant to be used ("any project"), but there is no explicit sentence. UNVERIFIED as a legal matter.
- The licence is a few lines on a web page, not a signed-off file; screenshot or save the page (hash in the excerpt file) in case it changes.
- Version on the site: "0.99.7.2" with badge date "7/12/2025", while the zip's readme says 10/31/2025. The site date looks stale. Platforms listed: Win/Mac. [76][78]

**Command line or batch mode: no OS-level one is documented.** The "Commands" page describes an **in-app console**: "Press TAB to Enable/Enter Commands", Enter to confirm, Up/Down for history. [77] It is a text way to drive the GUI, with these batch-relevant pieces:
- `o obj` (or other types) exports the current model; **`odir obj` exports every model in the current folder's model list**. That is the closest thing to batch export.
- `xs [shader] [args]` runs a GLSL-based voxel shader from the `shader/` folder (examples shipped: gear, mandelbulb, sphere, torus, stair). A scripted way to *generate* models, still run inside the GUI.
- `hotkey.txt` in `config/` binds keys to commands. Export settings (scale, axis, merging faces; OBJ default `axis: XZ-Y` meaning Y-up, `scale 0.1`, `merge 1`) live in `config/config.txt`, so an agent can pre-set them by editing a text file. [78]
- The changelog itself warns the command feature "is not robust. Use it carefully." [76]
- **No command-line arguments, headless mode or script-file runner are documented anywhere I read.** The exe imports the standard Windows `GetCommandLine` calls, which proves nothing either way. If a hidden CLI exists: UNVERIFIED.

**Consequence for Principle 7 (prefer scriptable tools).** MagicaVoxel is a GUI tool with a console, not a pipeline stage. The scriptable route is to have agents **write `.vox` files directly** (the site links a public ".vox format" repo, `ephtracy/voxel-model`, whose page labels its licence "MIT"; I saw only that label, not the file) and let the maker open, tweak and export them. I did not test writing a `.vox`. Treat this as a lead. [79]

### F2. Mineways "Scripting" page: what it allows

Page last updated 9/1/2026 (its footer); the Windows build is 14.01, updated 2026-10-03. [80][48]

**What a script is.** A plain text file, usually `*.mwscript`, loaded through File > Import Settings or passed on the command line. The page's summary: you can perform "almost every Mineways operation by using a command instead of the user interface". [80]

**Batch export: yes.** A script can load a world, pick a level, set a selection box by coordinates, choose a format and export, then repeat. Example from the page: `Set render type: Wavefront OBJ absolute indices` / `View Nether` / `Selection location min to max: -38, 83, 16 to -31, 127, 30` / `Export for Rendering: C:\...\nether.obj`. The distribution ships `hunk_output.mwscript` and a Python generator, `hunk_maker.py`, for exporting many adjacent chunks of terrain; the page also names it as the fix for out-of-memory on large areas. [80][81]
- Formats in `Set render type`: Wavefront OBJ (absolute or relative indices), **USD 1.0**, binary STL (two variants), ASCII STL, VRML 2.0. Other export commands: `Export schematic` (`.schematic` or `.schem`) and `Export map` (PNG). [80]
- Material choices include no materials, solid colours, noise textures, "three large images" and individual textures per block face. [80]
- Script-only extras: temporary block changes on export only ("None of these functions will affect your original Minecraft world"). Note the block-swap command still uses the pre-1.13 numeric format. [80]

**Command line and headless.** Syntax from the page: `mineways.exe [-headless] [-w X Y] [-m] [-s UserSaveDirectory|none] [-t terrainExt...png] [-l log] [-suppress] [-zl #] [files...]`. [80]
- With script files on the command line, Mineways runs them and exits when done.
- **`-headless`** shows no window, suppresses dialogs and is "ideal for batch processing or calling Mineways from build scripts", but the page says: "BEWARE! This is all a bit experimental and can be wifty!"
- Without script files, `-headless` reads commands from standard input and answers `READY`, `OK`, `ERROR: ...` or `CLOSING`. The page includes a Python `subprocess` example. So an agent on the same machine can drive it as a long-running helper. Not tested by me.
- Quirk for Windows users: in `cmd.exe` use `start /wait mineways.exe -headless` for interactive typing. [80]

**Which worlds.** Java Edition only: the home page says "Minecraft: Java Edition, versions 26.3 and earlier"; Bedrock saves must be converted to Java first. [48][81] The scripting page also covers schematics (full path needed) and 1.13+ block names. Modded worlds: unknown blocks become bedrock blocks unless configured. [80] (Minecraft's year-based versions began with 26.1; see `playbooks/format.md`.)

**Windows only?** In practice yes. The page calls it a Windows GUI program; the downloads page says Mac users get the Windows version wrapped in Wine (the Mac download is **12.09**, older than 14.01) or a community native ARM64 branch for 13.00, and Linux users "download the Windows version and then use WINE". [81] The script examples use Windows paths. Whether `-headless` works under Wine in our Linux container: **UNVERIFIED, not tested**. Plan for it to run on the maker's Windows PC, fed by agent-written `.mwscript` files (the "script-drop" pattern in `agent-pipeline.md`).

### F3. Bela Messex and the Before Your Eyes metronome

**Verdict: keep the name for one claim only, and detach it from the metronome.**
- **[15] (MCV/DEVELOP, Vince Pavey, published 2023-05-18, modified 2023-06-06)** quotes Oliver Lewin: "Ultimately it was our lead designer Bela Messex who figured out that we could set up a language to differentiate blinks that would trigger a scene change from ones that wouldn't." The article **never mentions a metronome**. [15]
- **[14] (Game Developer, Sam Machkovech, 2023-03-22)** is the source for the metronome: "a new idea: to turn off the ability to blink game-time forward unless a metronome appeared on screen." It says the project "add[ed] a new lead designer" but **names no inventor for the metronome and never mentions Messex or a "language"**. [14]
- So no primary source in hand credits Messex with the metronome. Whether the "language to differentiate blinks" and the metronome gate are the same device is **UNVERIFIED** (plausible, since both solve involuntary blinks, but no source says so).

Wording for the scribe (E6 in "Exemplars", currently "How: lead designer Bela Messex's 'language to differentiate blinks'" under the metronome fix): "Per Lewin, lead designer Bela Messex devised a 'language to differentiate blinks' that change scenes from ones that don't [15]. Separately, the team's rescue included a rule that blinks only move time forward while a metronome is on screen [14]. No source says who proposed it or that the two are the same." Summary item 5 and pattern 12 name nobody, so they stand.

### F4. Minecraft Usage Guidelines: dated version and the "physical locations" clause

Fetched [42] on 2026-10-18 at 04:48 GMT (HTTP 200); also the EULA [43], and the store/download pages. [82]

**Is there a dated version? No.**
- The page text carries no "last updated" date, and its `article:published_time` meta is empty. The EULA is the same: it says it may change "from time to time", no date.
- The server sends `last-modified: Fri, 16 Oct 2026 17:56:11 GMT`. That is a file stamp, not a policy revision date (any site rebuild can bump it), so it only tells us the file served today was written two days ago. [82]
- The page's own change clause: "We reserve the right to change our mind at any time." [42]
- **The ConductAtlas "last updated April 19, 2026" claim [71] could not be reproduced and its source has withdrawn it.** The clause page (it redirects to a new URL) now says the clause "is no longer published", and its correction log lists, for the Usage Guidelines, a 2026-10-12 correction ("26 provision(s) ... had no source in any capture") and a 2026-10-06 one ("1 quotation(s) ... omitted the condition they depend on"). Treat [71] as unusable: do not cite the date. [83]
- Recommended habit instead: store the text hash from the excerpt file (`6c00e292...` for my extraction) and re-fetch in the premiere week. A changed hash means re-read.

**The clause itself.** It is one bullet in the list of conditions for putting Minecraft footage on YouTube, Twitch or another website (the "Videos, streams, and screenshots" section): "The gameplay is not displayed or projected publicly within physical locations, for example:" followed by two examples: "Promoting or advertising big-screen Minecraft gameplay inside any commercial venue like restaurants" and "Charging money for Minecraft gameplay, leagues, or competitions in theaters where gameplay is projected onto movie screens". [42]

**Does it distinguish a free private family screening from a commercial venue?** Not explicitly. What the text does and does not say:
- It never mentions private, family or invited audiences, and it does not define "publicly" or "commercial venue".
- Both examples involve commerce (advertising in a commercial venue, charging in theatres). A free, invite-only showing in your own home is neither "public" nor commercial, and falls under "Personal use": "We are very relaxed about things you create for yourself." My reading, not legal advice.
- A separate trap: "When you decide to share your content with the community (whether you plan to make money off it or not), you are doing what we consider to be a commercial thing." "The community" is undefined; a gift to one's mother and relatives is not obviously that. [42]
- **A hired room is a real grey zone**, and a second section points both ways. "In-person events" allows gatherings of "no more than approximately 150 participants", no profit sponsorship, Minecraft's name only as a secondary descriptor, no Minecraft brand or assets on marketing materials, and gives "a casual meet up in your favorite pizza place" as fine. But it is written for Minecraft community meetups, not for showing a personal film that uses Minecraft footage. [42]
- Mojang says it cannot advise on specific projects (already in Q7). Our safe line is unchanged: private, free, invitation-only, no ads or sponsor, no Mojang logo or textures, a disclaimer in the credits; and **original voxel assets (MagicaVoxel/Blockbench) remove the question entirely.**

### F5. Does the maker own Minecraft, and which edition?

**Cannot be determined by research or from this session**; it is a question for the maker. (Nothing is on the file system here, and the project notes show no answer. The earlier decision list still has it as a TODO.)

What I verified that makes the question quick to settle:
- The current PC product is "Minecraft: Java & Bedrock Edition for PC", which "now includes both Java and Bedrock Edition". Anyone who bought the current PC edition has both. [84] The download page is titled "Download Minecraft Java & Bedrock Edition" and offers a single launcher download. [85] The price is not in the page's static text: UNVERIFIED.
- A Java check on Windows: Java worlds live in `%appdata%\.minecraft\saves`; Bedrock worlds on Windows 10/11 sit under `...\AppData\Local\Packages\Microsoft.Minecraft...` (Mineways' own help says so). [81][80]
- Decision rule: patterns 31-38 are **buildable** only with Java (Replay Mod, Flashback, Mineways all need Java worlds); on Bedrock they are reference-only unless worlds are converted (Mineways says conversion is easy; not tested); with no Minecraft at all they are reference-only. Do not ask the subject. The maker, or a relative on the "in on it" list, can check.

### F6. Eurogamer [3]: verification and dated excerpt

The page loaded from the container today (HTTP 200, 244,576 bytes; article dated **2022-04-12**, byline **Ed Nightingale**; neither is in our source line for [3]). All four items are **confirmed**:
- **14,000 foley:** "there are 14,000 foley sounds in the game comprising different objects and surface types." This is the journalist's statement, not a quote from the developers; it names Witchbeam sound designer Jeff van Dyck as the recorder.
- **Spreadsheets:** Brier: "We had spreadsheets keeping track of what items showed up in which levels, which items were new in each level, and which items were repeat items, which ones were variants on existing items." The article adds that Dawson automated the cataloguing of sprites and sounds into levels.
- **"The Bed Song":** Brier: "There's a song called The Bed Song by Amanda Palmer," a series of "snapshots in this couple's life, just depicted through the different beds that they've had over the years".
- **"Hollow":** Brier, about clones: "So you end up with this sort of hollow experience." **Brier alone says it.** Our notes say "Unpacking's makers call clones hollow" (summary item 14, line 23) and "Unpacking's team reports" (pitfalls); change to "Brier says".

The excerpt file holds these quotes, the page hash and the capture date.

### F7. Older adults (70+) with a TV remote or single-button clicker: NOT RESEARCHED

- No search was possible (budget refused), so this is **a gap in my work, not a finding of absence**. Nothing in our existing sources covers it: [41] is about mobile games, and [39] is a community checklist.
- Leads from my own background knowledge, **UNVERIFIED, not fetched, do not cite until opened**: Carmichael's 1999 ITC style guide for interactive TV services for elderly viewers; Rice and Alm's work on digital interactive TV interfaces for older adults (about 2008). Search terms for the next researcher with a working search: "older adults television remote control usability", "elderly smart TV interaction study", "single switch input older adults", "presenter clicker accessibility". Prefer studies with participants aged 70 and over.
- **Rule from the review stands: if round 3 finds nothing, Exercise 9 (ten-minute click test) becomes our evidence.** Use the actual clicker or remote, a consenting older tester who is not the subject, and the tallies already in the exercise.

### Corrections and updates for the scribe (do not change the evidence tiers)

1. Tools table, MagicaVoxel row: licence now verified from the website, not the zip: "Free to use for any project; credit appreciated; no selling or redistributing the software." No CLI or headless mode; in-app console only [76][77].
2. Tools table, Mineways row: replace "Command-line options UNVERIFIED" with "`.mwscript` scripts; `-headless` flag (experimental); stdin protocol; Windows GUI app; Java worlds up to 26.3" [80][48].
3. Q7 "Practical positions" 1 and Open questions 8: MagicaVoxel licence resolved (see F1). Open question 9: Minecraft terms still undated; see F4.
4. Q7 header and source [71]: mark the "April 19, 2026" claim as withdrawn by its source [83].
5. Exemplar E6 and Open question 10 (older-adult devices): see F3 and F7.
6. Summary item 14 and the pitfalls line: "hollow" is Brier's word (anti-pattern 10 already says Brier). Source [3] gains: Ed Nightingale, 2022-04-12.
7. Open question 11 (edition and OS): still open; the check is in F5.

### Sources (continued)

Tier tags as above. All fetched 2026-10-18.

[76] MagicaVoxel official site, main page fragment (the licence block and changelog) — https://ephtracy.github.io/mv_main.html — [P] version 0.99.7.2.
[77] MagicaVoxel official site, Commands page — https://ephtracy.github.io/mv_commands.html — [P].
[78] MagicaVoxel 0.99.7.2 Windows release zip (listed and read: `readme.txt`, `config/config.txt`) — https://github.com/ephtracy/ephtracy.github.io/releases/download/0.99.7/MagicaVoxel-0.99.7.2-win64.zip — [P]; release page https://github.com/ephtracy/ephtracy.github.io/releases/tag/0.99.7 (asset list would not load; filename found by URL probe).
[79] ephtracy/voxel-model (".vox format" repository linked from [76]) — https://github.com/ephtracy/voxel-model — [snippet] licence label "MIT" only; licence text and README not read in full.
[80] Mineways Scripting Language — https://erich.realtimerendering.com/minecraft/public/mineways/scripting.html — page footer "Last updated 9/1/2026" — [P].
[81] Mineways downloads and help (Windows, Mac, Linux, Bedrock note) — https://erich.realtimerendering.com/minecraft/public/mineways/downloads.html — footer "Last updated 9/1/2026" — [P].
[82] Minecraft Usage Guidelines, re-fetched with HTTP headers (same URL as [42]) — https://www.minecraft.net/en-us/usage-guidelines — 2026-10-18 04:48 GMT, `last-modified: Fri, 16 Oct 2026 17:56:11 GMT` — [P].
[83] ConductAtlas, withdrawn clause page (redirect target) — https://conductatlas.com/platform/minecraft/minecraft-usage-guidelines/provision/CA-P-002831/commercial-use-and-monetization-restrictions/ — [T] shows "This clause is no longer published" and a correction log; no "April 19, 2026" date found.
[84] Minecraft: Java & Bedrock Edition for PC (store page) — https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc — [P] "now includes both Java and Bedrock Edition"; price not in static text.
[85] Minecraft Java & Bedrock download page — https://www.minecraft.net/en-us/download — [P].
