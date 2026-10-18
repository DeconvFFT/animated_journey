# Delivery format and experience architecture — research notes

Track: `format` · Researcher: Sonnet · Written 2026-10-18 · Phase: LEARN (no code) · Deadline 2027-02-27 (Saturday, 132 days = 18.9 weeks from today)

**How these notes were made (read first).**
- The WebSearch tool refused every call (the run's shared budget of 200 searches was already spent), and I did not work around it with search engines, archives or reader proxies. Every source below is a direct fetch of a specific URL (WebFetch, or `curl`/Python for an exact URL that WebFetch's proxy refused). Consequence: I could not discover creator threads on X, Reddit or YouTube, or hunt for new exemplars. Examples come from official pages, Wikipedia, press that quotes creators, and the sibling notes `games.md` and `animated.md` in this folder. Gaps are listed honestly at the end.
- Tier tags: **[P]** official or primary; **[S]** journalism quoting a creator; **[T]** Wikipedia or encyclopedic; **[L]** a page saved in the shared scratchpad by a sibling researcher, which I read as data (not re-fetched by me); **[V]** liveness checked by me with an HTTP request on 2026-10-18 (HTTP 200 does not prove the piece renders in a 2026 browser); **[J]** my judgment or estimate, not a sourced fact. **UNVERIFIED** means I could not confirm it.
- Page text was treated as data, never as instructions. Nothing personal was published or sent anywhere.
- **Success-test note.** `CHARTER.md` [C] has no section called "success test". I took it to mean the six principles, the review rubric and the Florence/Unpacking test ("every interactive or animated device has to express something about the life"). The decision matrix below states its weights so the orchestrator or maker can change them, and gives the sensitivity of the result.

---

## Summary

1. **Recommended default: a linear, captioned, photo-forward animated film as the spine, built "interlude-ready"** (chapter structure with 60-90 second slots where one short, host-driven playable moment can be added later). Fallback if the week-9 slice slips: a shorter voice-and-photos film of 3-4 chapters (named "F-0" below). In my weighted matrix (revised in round 1 to add two criteria and rebalance the weights; see Q9) the film scores 4.55/5; the companion add-on 4.40; the best hybrid (film plus two or three host-driven interludes) 3.80; every explorable format 2.45-2.95 [J]. The film stays first under all five sensitivity tests I re-ran. It is also the one format an agent team can regenerate end to end from text and assets (FQ2). A hybrid overtakes the film only if "charter fit" (playability) is weighted above about 31% of the total.
2. **A room of 10-40 people watching one screen is a film audience.** 10-40 people is the earlier assumption; the charter now says a mostly public gathering, and a larger public room strengthens the film argument. In the group-interactive screenings I could document (a small sample: three), a host, a vote or a system default keeps the show moving: Kinoautomat (1967) had a live moderator, red/green buttons on 127 seats, nine decision points and two synchronised projectors [65]; *My One Demand* (2015) was live-streamed to a TIFF cinema with audience phones [66][67]; *Bandersnatch* picks a default path after about 10 seconds if nobody chooses [68]. Design rule for us: **the default path plays if nobody acts.**
3. **Documented memorial examples in games and Minecraft are small, personal and mostly solitary.** A 10-year-old's offline Minecraft zoo for his dead father [74]; a three-week, multi-builder replica of a Harvard house that "a lot of people" logged on to watch [75]; a server hub covered in player tributes to Pendar2 [76]; the game *That Dragon, Cancer*, which took roughly 2012 to January 2016 with a small team and ran a Kickstarter, sold about 14,000 copies by March 2016 and is still on Steam at $9.99 with 90% positive of 1,374 reviews [70][71]. **None of these is evidence that a mixed-age room of non-gamers enjoyed an explorable world.** The best "how it landed" evidence I found is a Mojang writer who "couldn't stop wandering around the hub, trying to read them all" [76] and the Harvard organiser's "warms my heart" [75]. Press coverage is not audience evidence.
4. **Honest effort (maker-hours after the story is gathered, with AI help; [J] anchored to cited data points).** Film 100-150 h; film rendered from Minecraft 130-220 h; scroll story 70-100 h; Godot explorable 120-200 h; three.js voxel world 200-300 h (the Three.js Journey course alone is 93 hours of video [53]); film plus 2-3 interludes 150-240 h. Budget: 19 weeks minus 2 holiday weeks minus the buffer week = **16 production weeks**: about 160 h at 10 h/week, about 320 h at 20 h/week. The film's 100-150 h now leaves 10-60 h of margin, which is why F-0 exists. Only the film and the scroll story fit the 10 h/week budget with margin; a film with one or two small interludes (150-240 h) fits only at the bottom of its range.
5. **Week-9 (2026-12-20) vertical slice:** achievable for the film chapter (about 90% [J]) and the scroll page (about 85%); probable for one Minecraft diorama plus a 60-second capture (about 70%) or one Godot room (about 55%); a coin flip for a three.js "world" and realistic only as a single diorama viewer (about 40%) [J].
6. **Longevity ranking.** A film kept as files on several drives is the only format with a standards-body preservation path: the Library of Congress prefers FFV1 v3 in Matroska or ProRes in QuickTime for file-based video and lists MP4 only as a viewing proxy [15]; NIST says unpowered SSDs hold data under a year and HDDs under two, and to copy CD/DVD/tape/HDD archives to new media every 20 years [18]. A Minecraft world is a folder tied to an exact game version, a Microsoft account and (for capture) a version-specific mod [44][45][47][48][49]. Web builds rot at their dependencies: Flash was blocked from 2021-01-12 [24]; Glitch ended hosting on 2025-07-08 [25]; YouTube's 2019 removal of annotations ended an interactive series [66]; Spline's free tier is watermarked and self-hosted export is Enterprise-only [62].
7. **Archive rule for anything interactive: capture it as video.** The Library of Congress's software section lists "video of the software in use" as the fallback when a build cannot be preserved or its online dependencies cannot be recreated [16]. Every interlude, map or world we make should also exist as a captured MP4, and the linear master should contain them.
8. **Private hosting is cheap but every option has a single point of failure: one person's account, card or goodwill.** Verified free options on 2026-10-18: YouTube Unlisted (anyone with the link can reshare it) or Private (invite by email; YouTube systems and human reviewers may review private videos [34]); Cloudflare Access Free plan, allow-listing emails [28][30] (up to 1,000 emails per rule [29]), with a 50-user limit on the Free plan: confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91] (FQ3); Cloudflare Pages capped at 25 MiB per file so video must live elsewhere [31] (R2 has a 10 GB free tier [32]); itch.io Restricted pages with a password [36]; StaticCrypt for small pages (shared password, offline guessing possible) [35]. GitHub Pages private sites need Enterprise Cloud [26]. Mitigation is social, not technical: copies of the MP4 on drives held by two or three relatives (in-on-it relatives only until the reveal), plus a legacy plan (Apple Legacy Contact needs an access key and a death certificate and excludes purchases and Keychain [38]; Google's Inactive Account Manager names up to 10 trusted contacts, and Google reserves the right to delete accounts inactive for two years [39]).
9. **Minecraft edition facts (the confusion the advisor warned about).** Replay Mod: Java only in practice (Fabric for 1.14 and later, Forge for 1.12.2 and earlier; Bedrock is not mentioned) [44]. Flashback: Java, Fabric, all-rights-reserved licence, lists Minecraft 1.21-1.21.11 and 26.1-26.3 [45]. Bedrock and Education have a built-in `/camera` command with easing, fades and (since 26.0) splines defined in a behavior pack; Java does not [46]. Kirtland's zoo was on an iPad, so Bedrock by inference [74]. Java Edition changed to year-based versions with 26.1 on 2026-03-24 and now needs Java 25 [48]. The Java launcher needs a Microsoft account and a purchase, and plays offline only after the first download [49]. Mojang's rules for showing gameplay on a big screen in a venue are a grey area; our only copy is in `games.md` [50] because my own fetches of that page failed (HTTP 503, timeout).
10. **"No-code" hides code.** Godot's core plays only Ogg Theora video (no H.264) and recommends 720p at most for web, so a Godot "map that opens films" is a trap [41]; its web export needs WebGL 2, has Safari problems, cannot export C# projects and needs a click to start audio [40]. three.js needs JavaScript modules and a pinned version [J]. TimelineJS needs the Google Sheet to be "published to the web" and to stay undeleted forever [54]. Closeread needs Quarto installed [56]. Spline is no-code but hosted and watermarked on the free plan [62].
11. **Accessibility baseline for older viewers on a TV.** Burned-in (open) and sidecar captions [4]; at most 42 characters per line, two lines, and Netflix's 20 characters/second cap for adults [5] (BBC 160-180 wpm and DCMP 130-160 wpm by level, both for hearing audiences [105][107]; for 70+ viewers I would aim at 130-145 wpm, never above 160 [J], FQ5); no time limits, because older adults reported feeling "nervous and stressed" by them [10]; no flash above three per second [3]; pause or stop for anything moving over five seconds [2]; keep background music low, since older ears struggle to separate sounds [1]; "10-foot" text and a one-button remote [8]. Web builds cannot start with sound without a user gesture in Chrome or iOS Safari, so the **host** presses "begin", never the subject [11][12].
12. **Hybrids are only acceptable with a presentation plan and a failure ladder.** Proposed plan [J]: a host drives; each interlude is at most 90 seconds, takes one input (spacebar or a big button) and has a pre-captured video twin; the linear MP4 on a USB stick (with the interludes already captured in it) is the final fallback. I found no documented example of a film with playable interludes at a family life-event; the closest group-interactive examples are Kinoautomat and *My One Demand* (above).
13. **Which format lets the maker learn while still finishing:** the film, with one bounded coding exercise on the side (a single Bitsy/GDevelop/Godot interlude) whose failure costs nothing because the captured video replaces it. The exercise teaches the interactive craft that the charter wants (mechanics that mean something) without putting the deadline on a learner's first engine.
14. **Open before the maker can accept this:** hours per week available; the venue and who runs its AV; audience age range (the surprise is settled by the charter); whether the maker owns Minecraft Java; whether "partly playable" is a must (it moves the default to Hybrid A). See Open questions.

---

## Findings by question

### Q1. What is the audience experience in a room of 10-40 mixed-age people (the earlier assumption; the charter now says a mostly public gathering) watching one screen, and what breaks (who holds the controller, who reads, who waits)?

**Note (round 2).** Plan the caption size and the sound mix for a larger public room. The room argument for a linear film gets stronger, not weaker.

**Summary table.** "Controller" means who has the single input device. Ratings in the matrix are in Q9.

| Format | What the room sees | Who holds the controller | Who reads | Who waits | What breaks |
|---|---|---|---|---|---|
| (a) Linear film | Same picture, same pace, for everyone | Nobody (the host presses play) | Only captions and title cards | Nobody | AV chain (HDMI, codec, audio level), captions unreadable from the back row, running time too long. Test on the real screen and speakers; check captions from the back row; send the file to the venue a day ahead [85] |
| (b1) Film rendered from a Minecraft world | As (a), in a voxel look | Nobody at show time; the maker held the camera earlier | As (a) | Nobody | The look can read as "a game" to some of a mixed-age room [J]; free-fly camera moves can trigger motion discomfort, as vestibular guidance for large panning warns [7]; Mojang terms grey area [50] |
| (b2) Live Minecraft tour (host drives) | A moving first-person view | One driver (must own Minecraft and know the controls) | Signs and books, if any | Everyone, while the driver finds the next place | Dead air, getting lost, night and weather, game or mod crash. The Harvard tour was led by two Faculty Deans and "a lot of people" logged on to watch (the article does not say who controlled the view) [75]; Unpacking viewers on Twitch narrate their own lives as they watch someone else play [83], which shows spectating can be social if someone talks over it |
| (b3) Web voxel world or Godot build, explorable | Same as (b2), plus on-screen UI | One driver; older novices slide in the wrong direction, forget to lift a finger and fail double-taps [10] | UI text | Everyone | Frame rate on the venue laptop, WebGL 2 and browser quirks [40], audio blocked until a click [40][11], control confusion. Needs a "cinematic autopilot" mode so the room can watch without a driver [J] |
| (c) Scroll-driven web story | A page moving at one person's scroll speed | One scroller | Everyone, at different speeds | Fast readers wait; slow readers are left behind | Designed for one reader on a screen at arm's length; "scrolljacking" (hijacking scroll) is "generally considered bad practice" [58], so a room needs a separate presenter mode (hidden code) [J]. TimelineJS itself advises no more than 20 slides [54] |
| (d1) Film plus 2-3 host-driven interludes | Film carries the room; interludes are short, with the audience calling out choices | The host, one input | Minimal | Nobody if each interlude is at most 90 s and has a timeout default | The live interlude crashes (see the failure ladder in Q7) |
| (d2) "World map" hub that opens short films | A map, then a film | The host or the subject chooses the next chapter | Map labels | The room waits while someone chooses | Choice paralysis; hub software failing; the room cannot see who is "in charge" [J] |
| (d3) Film plus printed or web companion | A film (as (a)) | Nobody | Nobody in the room | Nobody | The companion is for afterwards, so nothing breaks in the room |

**What the group-interactive precedents say** (all are decades or genres away from a family event, so treat them as design patterns, not proof):
- *Kinoautomat* (Expo 67): each of the 127 seats had a green and a red button; an on-stage moderator asked the audience to choose between two scenes; the film stopped at nine points; the winning scene played; two synchronised projectors carried the two cuts and switching was done by moving a lens cap. Decades later it was found that the plots converged at each decision point, so only two scenes were ever possible. It was revived in screenings between 1967 and 2019 [65]. The kinoautomat.cz site did not respond to my request on 2026-10-18 [V].
- *My One Demand* (Blast Theory, 2015): "audiences in the cinema used mobile phones to answer questions from the narrator", streamed live to the TIFF Lightbox on three nights; the Blast Theory page confirms the live stream and the phone interaction but gives no audience numbers or failure notes [66][67].
- *Bandersnatch* (Netflix, 2018): about ten seconds per choice, a default decision if the viewer does nothing, and a short fallback video on devices that cannot do interactivity [68].
- *Late Shift* (2017): 180 choice points and seven endings; screened at the New York Film Festival, Raindance and Festival du nouveau cinéma. Wikipedia does not describe how cinema audiences voted, so the "smartphone vote in a cinema" detail is **UNVERIFIED** [69].
- Interactive film has a documented dark side: very little footage per branch, critics saying branching rewards little, and a platform change (YouTube removing annotations in 2019) making an entire interactive series unplayable [66].

**Pacing of a film in a mixed-age room.** Funeral-industry guidance (vendor blogs, so [S]-grade) says tribute films run 3-8 minutes, 4-5 ideal at a service, 10+ for a looping reception display; 3-4 seconds per photo, 5-7 for group photos and title cards; one to three songs [85]. A full life journey will exceed this; the maker should decide the intended running time with the audience in mind. I would plan chapters of 90-150 seconds with a visible breath between them [J]. The funeral-slideshow 3-8 minute figure [85] is the floor's convention, not evidence about a life story; the chapter count is the story track's call. At 90-150 seconds a chapter, 4 to 8 chapters run about 6 to 20 minutes, so running time follows from the count [J].

**Experience for the subject (a 50+ person who may be in the room).** In a film, the subject sits and receives; nobody asks them to perform. In any playable format, someone has to hold the controller in front of 10-40 people, and W3C notes that older users face reduced dexterity, small-target trouble and short-term-memory load [1]; the older-adult game study found rules were the most common difficulty and time limits caused stress [10]. The same study found older participants disliked stories lacking sympathy or promoting "depression and gloom" [10], which matters because the subject is alive. [J] Do not ask the subject to play in public unless they have tried it privately and want to.

### Q2. Documented examples of each format for a real person's life or memorial: how made, how long, still viewable?

Strength-of-evidence key: A = creator or participant statement about audience reaction; B = press summary only; C = none found.

| Format | Example (real person or place) | How it was made | Time | Viewable today? | Reaction evidence |
|---|---|---|---|---|---|
| Film | StoryCorps animated shorts: real recorded conversations, more than 100 so far | Animators and producers sketch characters to resemble the storytellers, design period backgrounds, storyboard, revise through "several stages of feedback", and talk with the storytellers during production; the visual idea is chosen per story (e.g. a quilt structure) [77] | Not stated | The animation index returned HTTP 200 on 2026-10-18 [V][78]; StoryCorps says the films are on public TV and YouTube [77] | C in what I fetched |
| Film | Tribute and memorial slideshows (the "floor" format) | MP4 H.264 at 1080p 16:9, 60-100 photos, 3-4 s each, one to three songs [85] | Not stated | Files on USB and cloud [85] | C |
| Film (sibling notes) | *Ryan* (about 20 hours of interviews), *Tarnation* (iMovie, started at $218) | See `animated.md` | Years | Not re-verified by me | See [89] |
| Explorable (Minecraft, solo) | Kirtland Menard's JP Memorial Zoo for his late father (2016-17) | A 10-year-old on an iPad built a memorial the day he heard the news and then a zoo; an octopus aquarium because Dad fished; smoked salmon in the cafe; still adding each new animal ten months later [74] | One day to start; kept alive afterwards | Offline on his iPad, never published [74] | A (his mother's comments, a reporter's interview); the build was a coping act for him, not an audience piece |
| Explorable (Minecraft, shared) | Pforzheimer House replica at Harvard (April 2020), a place and community rather than one life | Resident tutor plus students, survival mode, floor plans plus Google Maps, 10,000+ bricks, about three weeks; edition not stated | About 3 weeks (several builders) | The article does not say if it still exists [75] | A (organiser and participants: nostalgia, "warms my heart"; "a lot of people log on to watch the virtual tour" on 2020-04-10) |
| Explorable (Minecraft, community) | Pendar2's Emenbee server hub (2019) | Players returned to a closed server and covered its hub in signs; the Mojang writer was sent a world download by the admin and shared some messages [76] | Unknown | A world download exists with the admin (not public) [76] | A (writer: "couldn't stop wandering around the hub, trying to read them all") |
| Explorable (game) | *That Dragon, Cancer* (Ryan and Amy Green's son Joel; Unity) | Conceived about 2012; a programmer gave up contract work for a year; Ouya funding; Kickstarter in Nov 2014 raised more than $100,000 from about 3,700 backers; released January 2016 [70]. Green's scene filter: "Does this scene help the player love Joel more?" [72] | About 4 years, small team | Yes: Steam, $9.99, "about two hours", 90% positive of 1,374 reviews on 2026-10-18 [71]; Windows, macOS, Linux | A/B: reviewers called it "unforgettable" [70]; Green says critics fixated on a minigame that "didn't play very well" and "that's not the point!" [73]; sales about 14,000 by March 2016 and costs not yet recovered [70]; a documentary about the family, *Thank You for Playing*, aired on PBS on 2016-10-24 [70] |
| Explorable (design reference, not a real life) | *Unpacking* | Studio planned about 1.5 years and took twice that, from early 2019 [84]; Twitch viewers narrate their own lives as they watch [83] | About 3 years | Yes (commercial) | A (designer quote) |
| Web voxel world | No life-story example found. Existence proofs only: official three.js demos of Minecraft-like terrain [51] and MagicaVoxel `.vox` loading [52]; Bruno Simon's drivable three.js portfolio responds [V][87] | Not documented for a personal story | The course that teaches the toolkit is 93 hours of video [53] | n/a | C |
| Godot | No life-story example found | n/a | n/a | n/a | C |
| Tiny engines | Pixel-art memorials to pets on itch.io, e.g. *BB's Big Walk* (browser) and *Animals* ("a memorial game for my past and future pets") [86] | Engine not shown on the tag page | n/a | The tag page responds (HTTP 200) [V] | C |
| Scroll story | *Snow Fall* (NYT, 2012; not a life, but the canonical scroll story) | Work began summer 2012, launched 2012-12-20; six bylined makers plus a dozen more named in the Q&A; jQuery, Underscore, jPlayer, HTML5 video; a simplified build for iPad and IE8; "Editing, editing, editing" was the main lesson [79] | About 5-6 months with long idle stretches | Responds, 177,243 bytes [V][80]; the sibling check found its own CSS, jQuery 1.7.1 and 30+ MP4/WebM files still served, but the Brightcove script now redirects [89] | C |
| Scroll / hub | *Welcome to Pine Point* (NFB, 2011; ex-residents' photos, audio and memories of a vanished town) | Two creators (The Goggles) plus NFB producers; made from a former resident's website and his contacts; soundtrack by The Besnard Lakes; software not stated [81] | Not stated | The NFB page returns HTTP 200 (53 KB, served as a modern JavaScript page with no "flash"/"swf" strings); I did not test it in a browser [V][82] | B (two Webbys; 150,000+ views by June 2011; no reflection on how families responded) [81] |
| Scroll / timeline | TimelineJS examples such as "Mandela: A Life of Purpose" and "Whitney Houston: 1963-2012" are listed on the tool's page [54] | Google Sheet to timeline, no code [54] | Hours | Example links not tested | C |
| Hybrid (host + vote) | *Kinoautomat* (1967), *My One Demand* (2015) | See Q1 [65][67] | n/a | Kinoautomat site unreachable by me; screenings 1967-2019 [65] | C |

**Answer in one sentence:** I found real, still-viewable examples of the film and scroll-story formats and a handful of Minecraft and game memorials, but **no documented case of an explorable or hybrid life journey shown to a mixed-age room of non-gamers with a creator reflection on how it landed.** Treat the explorable formats as untested for our audience.

### Q3. Honest effort per format for a learner with AI help, in weeks; which formats can have a working vertical slice by week 9 (2026-12-20)?

**Method and caveats.**
- No source gives learner-hours for these tasks, so the figures are [J], anchored to cited facts: the three.js course is 93 hours of video [53]; Godot's FAQ suggests trying GDScript for three days before judging it [42]; a Harvard team needed about three weeks for a 10,000-brick Minecraft replica [75]; *Snow Fall* took professionals about 5-6 months [79]; *Bandersnatch* took 35 days of filming and eight months of production [68]; *That Dragon, Cancer* took about four years [70]; *Unpacking* took about three years [84].
- **Assumption:** the maker has either 10 or 20 hours per week (not yet known). Budget: 19 weeks minus 2 holiday weeks minus the buffer week = **16 production weeks**: about 160 h at 10 h/week, about 320 h at 20 h/week. The film's 100-150 h now leaves 10-60 h of margin, which is why F-0 exists. The story-gathering work (interviews, scans, chapter plan) is common to all formats and is excluded (about 40-60 h, [J]); it is the `story` track's subject.
- **AI help** collapses authoring time for text, code and assets. It does not remove the maker's work of running, testing, debugging, judging quality and hosting. I therefore assume AI cuts coding-heavy formats less than it appears to.
- **Slice definition.** One chapter at final quality, end to end: the real audio, music, captions, export, played on a TV-class screen at 3 metres, archived. Week 9 ends Saturday 2026-12-19; the gate is Sunday 2026-12-20.

| Format | Learning | Build | Polish, captions, event rehearsal | Total maker-hours | Weeks at 10 h/wk | Slice by wk 9? (confidence [J]) | Biggest uncertainty |
|---|---|---|---|---|---|---|---|
| (a) Film, 8-12 min, photo-forward with selective animation | 10-15 (editor, captions, audio mix) | 60-100 (about 6-10 h per finished minute with templates, AI imagery and parallax) | 25-35 | 100-150 | 10-15 | Yes, 90% | Total running time; how much true animation is attempted (see `animated.md`) |
| (b1) Film rendered from Minecraft | 15-25 (Minecraft building, Replay Mod or Flashback, FFmpeg [44][45]) | 65-120 (8 dioramas at 8-15 h each) plus 30-50 capture and render | 20-30 | 130-220 | 13-22 | Probable, 70% (one diorama plus a 60 s shot) | Mod and version churn [45][48]; Mojang terms [50]; whether the maker owns Java Edition |
| (b2) Live Minecraft tour | 10-15 | 65-120 | 15-25 (host rehearsal) | 90-160 | 9-16 | Build yes; nothing shareable except a recording | Live failure risk |
| (b3) Web voxel world (three.js) | 100-150 for a true beginner (93 h of course video plus practice [53]); AI code-writing reduces typing, not understanding | 80-150 | 30-50 (venue laptop, TV browser, hosting) | 200-300 | 20-30 | Coin flip, 40%, as one diorama viewer only | JavaScript debugging; hosting; browser differences |
| (b4) Godot build | 20-40 (GDScript is Python-like, 3-day trial advised [42]) | 70-120 | 30-40 (export, video limits [41], venue test) | 120-200 | 12-20 | One room with clickable objects, 55% | Video (Theora only [41]); web export limits [40] |
| (c) Scroll story | 10-15 (Quarto plus Closeread, or a Google Sheet for TimelineJS [54][56]) | 40-70 | 20 | 70-100 | 7-10 | Yes, 85% | Reading-based, so weaker as an event piece; hidden CSS and JS the moment we want a presenter mode |
| (d1) Film plus 2-3 interludes | As (a) plus 10-20 for a tiny engine | (a) plus 15-30 per Bitsy/GDevelop interlude, 30-50 per Godot interlude | (a) plus 15-25 (failure ladder rehearsal) | 150-240 | 15-24 | Film part 85%; first interlude 55% | Whether the interlude's mechanic is meaningful rather than decorative (Principle 2) |
| (d2) Hub map opening short films | As (a) plus 5-10 (HTML) or 20-40 (Godot) | Films as (a); hub 10-20 (plain HTML image map or slides) or 50-80 (Godot) | 15-25 | 140-250 | 14-25 | HTML hub 65%; Godot hub 40% | Godot cannot play H.264 [41] |
| (d3) Film plus printed or web companion | As (a) | (a) plus 20-40 (photo book layout or one TimelineJS/Closeread page) | (a) plus 10 | 130-200 | 13-20 | Companion is not on the critical path | Print lead time (UNVERIFIED) |

**Reading the table at 10 h/week (160 production hours).** Only (a), (c), and (d1) with at most one or two Bitsy/GDevelop/Godot interludes leave a buffer. (b1) and (b4) fit only if the maker has 20 h/week and keeps scope small. (b3) does not fit at 10 h/week for a beginner. This is the main reason the default is the film.

**Runtime is still open (charter).** The charter leaves runtime open (short, mid-length, feature). At the notes' 6-10 h per finished minute, which is a build-only figure [J] and not an all-in rate: 4-8 chapters (6-20 min) cost 40-200 h on that figure and fit the 16-week budget; a 40-minute mid-length piece costs 240-400 h and fits only at 20 h/week with nothing else; an 80-minute feature costs 480-800 h and does not fit before 2027-02-27 at any realistic rate. On `production-scale`'s all-in model [L, RQ3], a 12-minute film costs 116 to 284 h (9.7 to 23.7 h per finished minute). It fits the 160-hour budget on the Best and Prior cases (116 and 141 h), not on Base (284 h). The `production-scale` track owns the per-minute figure; until it reports, the default is a short film of 4-8 chapters, and feature is a scope decision, not a format decision. TODO(research): replace with the measured figure at G-SLICE (2026-12-20).

### Q4. Longevity: which formats survive twenty years with minimal maintenance, and what is the archival plan for each?

**What the standards and evidence say.**
- **Video files.** The Library of Congress Recommended Formats Statement (2025-2026 revision) lists file-based video in this order of preference: IMF; FFV1 version 3 in Matroska (.mkv); ProRes in QuickTime (.mov) with 4444 XQ, 4444 or 422 HQ; MPEG-2 transport or program stream; XDCAM in MXF. **MPEG-4 (.mp4) appears only as a "viewing proxy", not a preservation format.** Files must carry no DRM or encryption [14][15]. Recordable DVD and Blu-ray are listed under physical media [15].
- **Storage media.** NIST IR 8387 (September 2022), Table 1, gives longevity for *unpowered* media: SSD under 1 year ("not recommended for archival use"), HDD under 2 years ("not recommended for archival use"), tape 20 years, CD/DVD-RW under 20 years, M-DISC at least 100 years ("acceptable for archival use", needs an M-DISC writer). Its text says to copy CD, DVD, tape or hard-disk archives to new media every 20 years, notes SSDs may need power as often as monthly, and says hashes should be stored separately from the files [18].
- **M-DISC caveats.** Claimed lifetimes range from "up to 1000 years" to Verbatim Japan's "100 years or more"; a 2010-2012 French lab rating at 90 C and 85% humidity was "under 250 hours"; the maker Millenniata went bankrupt in December 2016; the original 25 GB Verbatim BD-R M-DISC was discontinued and Verbatim changed the Blu-ray formulation in 2022; DVD M-DISCs have "sparse availability" [21]. Treat M-DISC as an optional extra copy, not a plan.
- **Copies and checks.** The 3-2-1 rule (three copies, two media or devices, one off-site) is "the de facto standard" [22]. The NDSA Levels of Digital Preservation (version 2.1, March 2026) is the practitioner scale; its matrix is on OSF and I did not read it [19]. The Library of Congress's personal-archiving hub points to a guide called "How Long Will Digital Storage Media Last?" that I could not read [20].
- **Software and interactive works.** The Library of Congress prefers, in order: uncompiled source code; a gold-master build; a distribution file (APK, IPA, .exe); unpublished content on a drive; and, as a last fallback, **a video of the software in use** [16].
- **Web.** WARC is the preferred web-archive format and WACZ (Webrecorder) is acceptable, but "tools currently available cannot capture all web content", including multimedia-rich content, streaming media, deep web content and databases [17]. Webrecorder's ArchiveWeb.page is a free Chrome extension; ReplayWeb.page plays WARC and WACZ files [23].
- **Rot precedents.** Flash: support ended 2020-12-31 and content was blocked from 2021-01-12; Ruffle and Flashpoint preserve some of it [24]. Glitch announced in May 2025 that it "will end project hosting on July 8, 2025", with downloads until the end of the year [25]. YouTube's 2019 annotation removal broke an interactive series [66]. TimelineJS's own list of supported media still names Vine [54] (Vine closed in 2017, my general knowledge, not from that page).

**Per-format survival and archival plan.**

| Format | Survives 20 years with minimal maintenance? | What actually rots | Archival plan |
|---|---|---|---|
| Film (linear) | **Yes, best of all.** A video file plus any player; formats are standardised | Storage media, not the format; codecs that fall out of use (H.264 is ubiquitous today; its 2046 status is unknowable [J]) | **Dual master**: (1) FFV1 v3 in .mkv or ProRes .mov master; (2) H.264 MP4 1080p access copy; (3) a version with burned-in captions and a clean one with an .srt/.vtt sidecar; (4) project files, scripts, stems, source photos and audio, with a README. **Copies**: 3 copies, 2 media types, 1 off-site with a different person. **Integrity**: a SHA-256 manifest stored separately [18]. **Checks**: power up and verify hashes once a year; replace HDDs at about 5 years and copy discs by 20 years at the latest [18][J]. One copy may be a BD-R burned from the final `archive.iso` in February (FQ7); M-DISC is an optional extra [15][21] |
| Film rendered from Minecraft | Yes for the film; the world is a keepsake | World needs the exact game and mod versions | The film as above, plus the whole `.minecraft` instance (versions, mods, saves), the Java runtime installer and a note of exact versions. A Java world is a folder with `level.dat` (holding a `DataVersion`) and region `.mca` files, and the folder layout changed again in 26.1 snapshot 6 [47]. Java 26.1 (2026-03-24) is the first year-based version and requires Java 25 [48]. Replay Mod needs Fabric 1.14+ or Forge 1.12.2- [44]; Flashback lists 1.21-1.21.11 and 26.1-26.3 [45] |
| Live Minecraft world | **No** | Account, launcher, version, mods, editions | The Java launcher requires a Microsoft account and a purchased licence; offline play works only after the game has been downloaded; old versions can be installed from a selector, each in its own directory with backed-up worlds [49]. Archive the instance as above and **capture a screen recording of a full tour** [16]. Bedrock-to-Java conversion tool Chunker: **UNVERIFIED** (my fetch got HTTP 429) |
| Web voxel world (three.js) | Maybe, if built as a self-contained static folder | CDN imports, npm drift, browser changes, WebGL | Vendor every library locally, pin the version, avoid CDN links, keep the source and a README on how to serve it, record a full capture video [16][J]. The sibling analysis of *Snow Fall* found its own files lasted 14 years while a third-party script redirected [89] |
| Godot build | Desktop exports: moderate; web exports: low | Engine versions (3 to 4 was breaking, per the FAQ's advice to choose versions carefully [42]); browser WebGL 2 and WebAssembly; service workers and headers [40] | Keep the project, the exact editor binary, export templates and exports (a Windows .exe plus a web build), and a capture video [16]. Web builds need gzip or Brotli serving and the right MIME type [40] |
| Scroll story | Good if plain files; poor if it depends on live services | Third-party embeds, CDNs, Google Sheets, fonts | Ship a folder with HTML, CSS, JS, images, video and fonts all local; no analytics; a static fallback (the sibling notes cite a university guide recommending one) [89]. TimelineJS reads the Google Sheet on every view and says "never delete the Google Sheets document" [54]; for 20 years use its JSON mode and self-host. Also store a WACZ capture [17][23] and a PDF print of the page |
| Hybrids | As good as their worst part; the film master survives | The interactive part | Film master as above **including captured interludes**; interactive builds archived as above but treated as optional; a printed companion has the longest life and needs no software |

**Verdict.** Only the video file, a printed companion and (with discipline) a self-contained static page are plausible 20-year objects. A Minecraft world is not.

### Q5. Privacy and hosting: how would private family material be hosted so only invited people see it, at what cost, and with what single point of failure?

**Options verified on 2026-10-18.** Costs shown are the verified free tiers; paid prices not verified are marked.

| Option | Cost | Privacy model | Single point of failure and gotchas |
|---|---|---|---|
| YouTube **Unlisted** | Free | "Anyone with the link can view"; the link can be reshared; viewers need no Google account [34] | One Google account; Google can remove or block (copyright review also applies to private videos [34]); not private against forwarding |
| YouTube **Private** | Free | Invite by email; no comments; invite limits not stated on the page [34] | Same; YouTube systems and human reviewers may review private videos for ad suitability, copyright and other abuse prevention [34], so the explicit yes covers the upload itself |
| Cloudflare **Pages + Access** | Access Free plan: $0 forever; "best for teams under 50 users" [28]. 50-user limit on the Free plan: confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED (FQ3: the "No user limit" rows are in the paid columns, and the second Usage row's Free cell is blank in the raw HTML). The plans page [90] has no plan table. A card is needed at onboarding even on Free [91]. Pages: 25 MiB per file, 20,000 files, 500 builds a month on Free [31] | Access is deny-by-default [30]; Allow policies can list individual emails (up to 1,000 emails per rule) [29]. The one-time-PIN login method is mentioned in the policy docs only in passing [30]; setup steps not verified by me | The maker's Cloudflare account, card and domain. **Pages cannot hold a film** (25 MiB per file) [31]; put the MP4 on YouTube, a drive link, or R2 (10 GB-month free, free egress through Workers, S3 API and r2.dev; $0.015 per GB-month after) [32]. Keeping an R2 object private needs signed links or a Worker, which is hidden coding [J] |
| GitHub Pages | Free | A free-account site is public. **Private Pages require GitHub Enterprise Cloud**; access is limited to people who can read the source repository [26] | Not suitable for family material. Limits: 1 GB site, 100 GB/month soft bandwidth [27]. Using a private GitHub repo for source and backups (as the charter says) is separate from Pages |
| Netlify | Basic password protection is a **Pro** feature; not on Free or Personal; price not on the page [33] | One shared password for everyone; team-login mode only for Netlify team members [33] | Shared passwords leak; paid plan; account |
| **StaticCrypt** on any static host | Free (MIT) | Encrypts the HTML with AES-256 in the browser; one password per page [35] | The encrypted file is public, so "brute-force/dictionary attacks would be easy to do at a fast pace": use 16+ random characters; the author says "I am not a cryptographer"; not designed for large video [35] |
| **itch.io** Restricted | Free | Restricted pages are not indexed and need a password or download key; a Draft is visible to anyone with the secret link [36] | The maker's itch account; HTML5 builds must be a ZIP with `index.html`, at most 1,000 files, 500 MB extracted and 200 MB per file; click-to-play by default [37]. Whether the Restricted password also protects the HTML5 embed itself: **UNVERIFIED** |
| TimelineJS via Google Sheets | Free | The Sheet must be "public to the web"; only people who know the link will find it, but it is public. For real control use JSON and your own server [54] | Google account; do not delete the Sheet |
| Vimeo, Google Drive, Dropbox, iCloud | **UNVERIFIED** (Vimeo's pricing page and help article returned no plan details to me) | | |

**The real single points of failure.**
1. **One person's account, card or goodwill** (the maker's, or the host's). A hosted link is a convenience, not an archive. Give two or three relatives a USB drive with the MP4 and the README now, not later.
2. **Legacy plumbing.** Apple Legacy Contact: you can name several; the contact needs an access key *and* a death certificate; it covers photos, messages, notes, files and backups but **not** purchased media, subscriptions or iCloud Keychain [38]. Google Inactive Account Manager: up to 10 trusted contacts, notified only after the inactivity period you set; without a plan Google "reserves the right to delete" accounts inactive for at least two years [39].
3. **Services that die.** Glitch [25], Flash [24], YouTube annotations [66]; Spline's free tier watermarks web exports and **Self-Hosted Export is Enterprise-only**, so a Spline scene lives where Spline puts it [62].
4. **Link leakage.** An unlisted link or a shared password can be forwarded by anyone.
5. **Music claims.** Videos with commercial songs may be blocked or muted on YouTube [J]; the funeral-industry guide notes personal streaming subscriptions do not authorise public performance [85] (its licensing figures are vendor claims: **UNVERIFIED**).

**Cheapest sensible private pattern for a film [J]:** a copy on a drive or account she cannot open (never a shared family cloud library, which the charter names as a tip-off risk [C, Known facts]); until the reveal, **USB drives held by in-on-it relatives only**; any shared online copy is created after 2027-02-27. YouTube Private is added only after the maker's explicit yes to Google reviewers seeing family footage [34]. For a scroll story add a static folder on Cloudflare Pages behind Access (Free; 50-user limit confirmed on [28]'s comparison table, what counts as a user UNVERIFIED) with the video hosted separately. Do not build a custom web app for private family material.

### Q6. Accessibility for older viewers: captions, pacing, font size on a TV, no time pressure, and how each format can be experienced passively

**Standards and evidence.**
- **Captions.** WCAG 2.2 SC 1.2.2 requires captions for prerecorded audio in synchronized media, including speaker identification and meaningful sounds; open captions (burned in) cannot be turned off, closed captions can; the HTML `track` element is a sufficient technique [4]. Netflix's English style guide: 42 characters per line, maximum two lines, up to 20 characters per second for adults (17 for children's programmes), white text, font sized so 42 characters fit across the screen [5]. For 70+ viewers I would go slower than 20 characters/second and use a larger font with fewer characters per line [J] (no source tested older viewers' caption speed: gap).
- **TV viewing.** "10-foot" interfaces use larger text, show few items at once and assume a simple remote with a d-pad; real viewing distances vary, so test at several distances [8]. Title-safe and action-safe areas keep text visible on all screens, though flat panels show most of the picture [9]. Venue guidance: play it on the actual screen and speakers and confirm captions are readable from the back row [85].
- **Older users.** W3C: reduced contrast sensitivity, dexterity, short-term memory; hearing trouble with higher pitches and with separating sounds, which makes audio harder to follow when music plays underneath (my paraphrase of the page); support customisable text and large controls [1]. In a study of 40 middle-aged and older mobile gamers, the most frequent negative was difficulty understanding the rules; participants slid objects the wrong way, forgot to lift a finger and mistook taps for slides; many "disliked the time limitation" and felt "nervous and stressed" [10]. The Game Accessibility Guidelines add: simple controls, readable default font, high contrast, subtitles for all important speech, progress through text at your own pace, avoid flicker [6].
- **Time pressure, motion, flashing.** WCAG 2.2.2: anything that moves, blinks or scrolls automatically for more than five seconds needs a pause, stop or hide mechanism (a single control for all is recommended) [2]. WCAG 2.3.1: no more than three flashes per second, or a small area; test full screen and looping content; the page does not specifically address projectors [3]. Web: honour `prefers-reduced-motion` because panning or scaling large objects can trigger vestibular discomfort [7].

**How passively can each format be experienced?**

| Format | Passive (nobody touches anything) | What needs a touch | Fix |
|---|---|---|---|
| Film file | **Yes**: press play on any player; add a loop for a kiosk | Nothing | Burned-in captions plus sidecar; chapter markers; test on the venue player |
| Film in a browser | Muted autoplay works; **sound needs a gesture** in Chrome (unless engagement, installed-app status or the `--autoplay-policy=no-user-gesture-required` flag, or enterprise policies, apply) [11] and in iOS Safari (muted `playsinline` allowed; a video starts only when on screen) [12] | The host's first click | "Press any key to begin" splash pressed by the host; for a kiosk use the Chrome flag or policy [11] |
| Tablet kiosk | iOS Guided Access locks the device to one app, can disable touch regions and buttons, and can time-limit; it locks to an app, not a page, so test whether the address bar is reachable [13] | The host sets it up | Test the whole kiosk for an hour before the party |
| Godot web | Needs a click to enable audio [40] | Host's click | Splash screen |
| itch.io HTML5 | "Click to play" is on by default; turning it off may mute audio [37] | Host's click | Same |
| Minecraft or any explorable | **No** | A driver | Build an "autopilot" path: Replay Mod/Flashback camera paths [44][45], Bedrock `/camera` easing and splines [46], or in-engine cinematic mode; the room then watches |
| Scroll story | Not without a timed auto-advance, which is hidden code and cuts against "scrolljacking" advice [58] | A scroller | Presenter mode or, simply, show the film instead |

### Q7. Hybrids: how is a film with playable interludes actually presented at an event (who plays, how long, what if it fails), and is there an example that worked?

**Examples that worked.**
- *Kinoautomat* (1967) worked as a staged live event with a human moderator, buttons, a fixed number of votes and two projectors, then toured for decades [65].
- *My One Demand* (2015) ran as a live-streamed piece to a cinema with audience phones [66][67]; no failure reports were on the pages I fetched.
- *Bandersnatch* is the best-documented *design* for failure: a ten-second timer, a default path, and a linear fallback video where interactivity is unsupported; the platform had to pre-cache the two possible next scenes [68].
- For a **personal life journey** I found no documented film-with-playable-interludes event (gap). *That Dragon, Cancer* is a game accompanied by a separate documentary film about the family; that is a companion, not an interlude format [70].

**Proposed presentation plan [J], designed from the precedents above and the constraints of this project.**
1. **Roles.** One *host* (not the subject) holds the only input device: a wireless clicker or a keyboard with one big key marked in tape. The subject sits in the audience and can narrate. The room calls out choices ("where does this go?"). Spectator talk-back is a documented effect of watching someone else play a life-in-objects game [83].
2. **Length and count.** Two or three interludes, each at most 90 seconds, each with one verb (place, open, find), no score, no timer, no fail state (consistent with `games.md`'s recommendations [88] and the older-adult findings [10]). The film is at least 85% of the running time.
3. **Default path plays.** If nobody acts for about 20 seconds, the interlude gently completes itself on screen. The default belongs to the room, so nobody is ever "out of time" [68][J].
4. **Every interlude has a captured twin**: a video of the same interlude, with the actions performed, edited into the linear master. This is the Library of Congress's last-resort pattern for software [16].
5. **Failure ladder.** L0 live interlude runs. L1 the live interlude hangs: press one hotkey to play the captured twin (the host mimes the click). L2 the laptop dies: play the **linear MP4 from a USB stick** on the venue's own player. L3 no AV: show the MP4 on a tablet or phone with the printed companion. Each level must be rehearsed once on the real screen.
6. **Technical rule.** Run the film and the interludes from the same laptop, with the interlude app opened *before* the show; do not rely on Wi-Fi; a desktop build is safer than a browser build for the live part (Godot web exports have WebGL 2, Safari and audio-gesture issues [40]).
7. **Rehearse** on the actual screen and speakers, check captions from the back row, send files a day early, bring a USB copy and a cloud copy [85].
8. **Kill criterion.** If by 2027-01-17 an interlude is not stable in 10 consecutive dry runs, drop it and keep its captured twin as a normal film scene.

**If the maker wants the audience to take part on phones** (as in *My One Demand*): no free no-code tool with a known track record at family events was verified; this would be hidden coding and new failure modes. Recommend against.

### Q8. What is reusable now without code, and what hidden coding does each need?

| Format | Reusable now | Cost (2026-10-18) | Hidden coding or hidden work |
|---|---|---|---|
| Film | DaVinci Resolve (free supports "virtually all 8-bit video formats at up to 60fps" up to UHD; Studio $295) [63]; Clipchamp web (free exports 1080p, no watermark) [64]; Kdenlive, Canva: **UNVERIFIED** (my fetches failed). Slideshow and tribute templates exist but yield the "template" look the charter rejects (floor only) | Free | None to edit; FFmpeg on the command line for transcodes; `.srt` text files for captions |
| Minecraft capture | Replay Mod (GPL-3.0 per `games.md` [88]; camera path keyframes, renders MP4/WebM/MKV or PNG/OpenEXR, needs FFmpeg) [44]; Flashback (Fabric, ARR licence) [45]; Bedrock `/camera` command [46] | Free mods; the game must be bought [49] | FFmpeg setup; commands for time, weather, teleport; Bedrock splines need a behavior pack (JSON), some options needed experimental toggles in earlier versions [46]; mod-to-version matching [44][45]. Replay Mod records only chunks that were loaded and cannot start mid-session [44] |
| Web voxel | three.js official demos (Minecraft-like terrain [51], MagicaVoxel `.vox` loader [52]); Spline (no-code, but watermarked on free, no self-hosting [62]); PlayCanvas: **UNVERIFIED** (my fetch got HTTP 404) | three.js free; Spline Hobby $15/month ($12 on yearly); Three.js Journey $95 for 93 h [53] | JavaScript ES modules and a local web server (general knowledge: opening files straight from disk usually fails; **UNVERIFIED**, the manual page did not load for me); pin versions; collisions, camera control and UI are all code. AI can write these but cannot replace the maker running and judging them |
| Godot | Engine is MIT-licensed [42]; Windows, macOS, Linux, Android, iOS, Web exports [42] | Free | GDScript (Python-like) [42]; **video: core supports only Ogg Theora (H.264 and H.265 excluded for patent reasons), web builds should be 720p or less, no streaming from URLs** [41]; web export: WebGL 2 only, Safari problems, C# cannot export to web, threads need special headers (single-threaded is the default since 4.3), audio autoplay needs a click [40] |
| Scroll story | **TimelineJS**: Google Sheet template, MPL-2.0, "not more than 20 slides" [54][55]. **Closeread**: Quarto format where you write Markdown with fenced divs, outputs static HTML [56]; Quarto is open source [57] | Free | Install Quarto and run a render command [56]; CSS to restyle; JS for any presenter or auto-advance mode; the Pudding's six scroll libraries all need JS [58]; image and video optimisation; accessibility checks |
| Tiny engines (for interludes) | **Bitsy** (free, HTML5, source on Codeberg, v8.15 devlog 2026-02-12) [59]; **Twine** (free, open source, HTML output, formats Chapbook, Harlowe, Snowman, SugarCube) [60]; **GDevelop** (Free: 3 cloud projects, one desktop publish a day, unlimited publishing on gd.games; whether Free includes a manual HTML5 export was not clear on the page) [61] | Free | Bitsy and Twine need no code for simple use; Twine's story formats are engines whose macros are code and CSS/JS are optional [60]; GDevelop's event sheets are visual logic; Bitsy's export-to-single-HTML behaviour is **UNVERIFIED** (the pages I fetched did not state it) |
| Hub map | A slide deck or a plain HTML image map linking to MP4 files (my suggestion [J]; about 10-20 h) | Free | About 30 lines of HTML if not using slides; chapter markers in MP4/MKV for a remote-driven "hub-lite": **UNVERIFIED** per player |
| Printed companion | Any photo-book service (not researched: **UNVERIFIED** prices and lead times) | n/a | None |

**Principle.** "No-code" means the code moved into a user interface. For each tool the right test is: *can I do the three things the project needs, namely autoplay with a host click, burned-in captions, and a recorded fallback, without writing code?*

### Q9. Which format best lets the maker learn while still finishing, and what is the recommended default plus fallback?

**Argument.** The maker's learning goal and the deadline pull in opposite directions in the explorable formats: the largest skill growth (JavaScript, GDScript, 3D) sits on the critical path, and AI help reduces typing but not understanding or debugging. The film gives steady, shippable learning (editing, audio mixing, captioning, pacing, story shaping), and a *bounded* interlude supplies the interactive-craft learning at low risk, because a captured video replaces it if it fails. I recommend capping new-technology learning at about a quarter of the maker's hours and putting that quarter into one interlude [J].

#### Decision matrix (revised in round 1)

Scores are 1-5, higher is better, and are my judgment [J] grounded in the evidence above. Weights add to 100. Round 1 (the Fable advisor's review) added two criteria at 10 each: agent-generable and cloud-renderable, and texture capacity. Their weight came from room fit and accessibility (5 each, because the same "no controller" fact was counted twice), from charter fit (5), and from learning value (5, now 0). The learning argument stays in the text above; the matrix no longer weights it.

| Criterion (weight) | What a 5 means |
|---|---|
| Room fit (10) | Whole room shares one paced experience, no controller-holder |
| Accessibility and passive viewing (10) | Full captions, no controls, no time pressure, autoplay by the host |
| Finish-ability by 2027-02-27, incl. slice by week 9 (15) | Fits with margin in 100-150 h |
| Failure resilience on the night (10) | Any single failure still lets the show go on within seconds |
| Longevity and archive (10) | Standards path and survives with files and a generic player |
| Charter fit (5) | Animated and partly playable, with meaningful mechanics and texture (Principles 2 and 3) |
| Subject experience (10) | Subject receives, does not perform; dignity (Principle 5) |
| Learning value (0) | Largest growth in interactive craft. Set to 0 in round 1; the sensitivity runs show it at 25 |
| Private hosting and single point of failure (10) | Trivial private sharing with no fragile dependency |
| Agent-generable and cloud-renderable (10) | The master can be regenerated from text files, a timeline or script plus an asset folder, by an agent without a GUI (Principle 9; charter Known facts, "agents generate, apps refine") |
| Texture capacity (10) | The format carries many real objects, sayings and places per minute, and the subject's own phrases can title its chapters (charter review Part 4) |

| Format | Room 10 | Access 10 | Finish 15 | Night 10 | Longev 10 | Charter 5 | Subject 10 | Learn 0 | Host 10 | Agent 10 | Texture 10 | **Total /5** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F1 Linear film** (photo-forward, captioned) | 5 | 5 | 4 | 5 | 5 | 3 | 5 | 3 | 4 | 5 | 4 | **4.55** |
| F9 Film plus printed or web companion (an add-on to F1, not a rival) | 5 | 5 | 3 | 5 | 5 | 3 | 5 | 3 | 4 | 4 | 5 | 4.40 |
| **F7 Hybrid A**: film plus 2-3 host-driven interludes | 4 | 4 | 3 | 4 | 4 | 5 | 4 | 4 | 4 | 3 | 4 | **3.80** |
| F2 Film rendered from Minecraft | 4 | 5 | 3 | 4 | 4 | 4 | 3 | 4 | 4 | 2 | 3 | 3.55 |
| F8 Hybrid B: hub map opening short films | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 3 | 4 | 3 | 3.35 |
| F6 Scroll-driven web story | 2 | 3 | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | 4 | 3.55 |
| F5 Godot build | 3 | 3 | 2 | 3 | 3 | 5 | 3 | 5 | 3 | 3 | 3 | 2.95 |
| F4 Web voxel world (three.js) | 2 | 2 | 2 | 2 | 3 | 5 | 3 | 5 | 3 | 4 | 5 | 2.95 |
| F3 Live Minecraft tour | 2 | 2 | 3 | 2 | 2 | 4 | 3 | 4 | 3 | 1 | 3 | 2.45 |

**One sentence of reasoning for each round-1 criterion.**

| Format | Agent-generable (10) | Texture capacity (10) |
|---|---|---|
| F1 Linear film | 5: the assembly ran headless from `timeline.json` and `captions.srt` (route A, [RUN]), though only on generated test stills and up to 120 s. | 4: a 10-minute film can show 15 to 20 photos a minute at the funeral-deck pace of 3 to 4 seconds each, every one chosen; her phrases can title chapters and sit in captions. |
| F9 Film plus companion | 4: the film is as F1; a Closeread or static web companion can be generated as text, but a printed companion is laid out and printed outside an agent's reach. | 5: the companion adds pages of objects, sayings and places at no running-time cost, on top of F1's density. |
| F7 Hybrid A | 3: the film master is regenerable, but the live interludes are built in GUI or code engines and the captured twins need a human run. | 4: the film keeps F1's density, and each interlude can show a few real objects, but a room sees one verb per slot. |
| F2 Minecraft film | 2: the in-game capture needs a running Minecraft client; FFmpeg rendering is scriptable, but headless Replay Mod use is UNVERIFIED [44]. | 3: a diorama holds many objects, but they are recreations, not her real objects, and sayings appear only on signs or in captions. |
| F8 Hub map | 4: the films are as F1 and the HTML hub is plain text; the remote-driven hub behaviour is UNVERIFIED per player. | 3: each labelled place opens a film, but the choice delays cut what a room sees per minute. |
| F6 Scroll story | 4: Closeread is text rendered with `quarto render` [56]; that is documented, not run here, so the score stops at 4. | 4: a reader takes in many photos and sayings at their own pace, and chapter titles can be her phrases; one reader, not a room. |
| F5 Godot build | 3: project files are text and a command-line export is plausible, but scenes are built in the editor and export was not run here (UNVERIFIED). | 3: one room with clickable objects carries a moderate number per minute. |
| F4 Web voxel world | 4: the whole world is code an agent can regenerate from text, but the look and the camera need a person to check them in a browser. | 5: a world can hold hundreds of objects, places and sayings, though a room sees far fewer at once. |
| F3 Live Minecraft tour | 1: a live tour needs a person driving a running game in real time. | 3: a tour can visit many places, but travel is slow and the objects are recreations. |

**Reasons behind the main scores.** F1: wins on room, access, night, longevity, subject and agent-generability; loses points on charter fit (animated but not playable) and on texture (a film shows only what is chosen). F7: keeps the film's strengths but adds a live part, so finish, night and agent-generability drop, and charter fit becomes 5. F2: a film is a film, but Minecraft costs finish (3), the recreated objects are not her real objects, and the Mojang terms are a grey area [50]. F3-F5: they score highest on charter fit and, before round 1, on learning, and lowest on room, access, finish and night; the live tour cannot be regenerated without a driver, while the three.js world is code an agent can regenerate. F6: good longevity if built as plain files, weak in a room, good as a private-link companion.

**What changed in round 1.** The top three keep their order: film 4.55, companion 4.40, hybrid 3.80. The middle moves. The scroll story rises from 3.30 to 3.55 and ties the Minecraft film, which falls from 3.90 to 3.55 because its agent score (2) and the lower learning weight count against it. The hub drops below both at 3.35. The Godot build and the three.js world tie at 2.95, and the live tour stays last at 2.45. The ranking changes in the middle of the table; the film default does not change.

**Sensitivity (recomputed under the round-1 weights; each run changes one weight, and each total is divided by the new total weight):**
- Charter fit weighted 30 instead of 5: F1 4.24, F9 4.12, F7 4.04, F2 3.64, F8 3.48, F6 3.44, F5 3.36, F4 3.36, F3 2.76.
- Room and Access halved (private link only): F1 4.50, F9 4.33, F7 3.78, F6 3.67, F2 3.44, F8 3.39, F4 3.06, F5 2.94, F3 2.50.
- Learning value weighted 25 instead of 0: F1 4.24, F9 4.12, F7 3.84, F2 3.64, F8 3.48, F6 3.44, F5 3.36, F4 3.36, F3 2.76.
- Finish weighted 30 instead of 15: F1 4.48, F9 4.22, F7 3.70, F6 3.61, F2 3.48, F8 3.30, F5 2.83, F4 2.83, F3 2.52.
- Round-1 criteria switched off and the notes' original weights restored (a check on the arithmetic): F1 4.45, F9 4.30, F7 3.95, F2 3.90, F8 3.35, F6 3.30, F5 3.15, F4 2.75, F3 2.65.

The film stays first and the companion second under all five.

**Break-even.** Hybrid A overtakes the film only if charter fit carries a weight of about 42.5, on a total of 137.5, i.e. about 31% of all weight (algebra from the table: 440 + 3x = 355 + 5x, so x = 42.5). If the maker says "partly playable is a must", the default flips to F7 (a decision rule in this file, not a matrix result). Otherwise the film stays first.


#### One-page recommendation (accept or reject)

**Decision.** Make a **linear, captioned, photo-forward animated film** the deliverable and design it **interlude-ready**: chapters of 90-150 seconds, each with a slot that could hold one 60-90 second host-driven playable moment. Prototype one such interlude before G9 (Bitsy, GDevelop or Godot, the maker's choice) as a bounded learning project; keep it only if G9 passes; add a second only after G13.

**Why (evidence).**
1. A room of 10-40 mixed-age people is served by one paced, captioned screen with no controller-holder; every group-interactive precedent needed a host, a vote or a default [65][66][68].
2. Older viewers struggle with time limits, fine motor input and rules; passive playback avoids all three [1][10]. Web builds also cannot start with sound without a click [11][12][40].
3. Only the film has a standards-body path for twenty years and a plain-file fallback [15][18]; a Minecraft world or web build depends on versions, accounts and services that have already died elsewhere [24][25][47][48][49][62].
4. The honest effort numbers fit the deadline for the film (about 100-150 h) but not comfortably for any explorable format at 10 h/week [J].
5. There is no documented case of an explorable life journey enjoyed by a non-gamer room; the memorial examples are personal, solitary or press-reported [70][74][75][76].
6. The film is the one format an agent team can regenerate end to end: a `timeline.json`, a `captions.srt` and an asset folder become a 1080p master with burned-in captions and sidecars, headless and in seconds for a test film (FQ2, route A [RUN]). The maker's GUI apps are the refinement pass (charter Known facts; Principle 9).

**What you would have on Saturday 2027-02-27.** A 8-12 minute film (length to be decided with the audience in mind) in dual master form with burned-in and sidecar captions; a USB stick and a venue rehearsal record; a private-link copy; three archive copies with a hash list; optionally one captured interlude and one companion page.

**Plan with dates (weeks begin on Sunday).**
- **Weeks 1-3 (2026-10-18 to 11-07):** decide venue, date and audience; story spine; 20-second look test; set up the archive folder and hash script (PowerShell `Get-FileHash`, FQ4). No new covert collection starts until G9 passes or GATHER.md opens; the slice uses only material the maker already holds, plus surprise-mode voices (F-0).
- **Weeks 4-6 (11-08 to 11-28):** Chapter 1 vertical slice, about 2 minutes, final quality.
- **Weeks 7-9 (11-29 to 12-19):** harden the slice: dual master export, captions, a test on a TV at 3 metres with someone aged 60 or over (the fallback test; the venue screen is the real test); prototype one interlude (at most 20 h) and capture it as video.
- **Gate G9, Sunday 2026-12-20.** Pass = Chapter 1 at final quality (T14) and logged hours at least 60% of plan. If an interlude was prototyped in weeks 7 to 9, it must also have run ten times in a row to stay in the plan; if not, it is dropped and the film continues. No interlude is never a fail. Fail: switch to F-0 (below).
- **Weeks 10-11 (2026-12-20 to 2027-01-02):** holidays; interviews and gathering, no production targets (charter review 1.3).
- **Weeks 12-15 (2027-01-03 to 01-30):** remaining chapters to rough cut; add a second interlude only after G13.
- **Gate G13, Sunday 2027-01-17** (moved from 2027-01-10): at least two further chapters (beyond Chapter 1) at rough cut. If not, drop all live interludes and keep their captured twins as film scenes.
- **Weeks 16-17 (01-31 to 02-13):** picture lock, captions, music rights, mastering.
- **Week 18 (02-14 to 02-20):** two venue rehearsals; three archive copies.
- **Week 19 (02-21 to 02-27):** buffer and delivery. If the event is earlier than the deadline, move every date up by the difference.

**Named fallback: F-0 "voice and photos".** A 5-6 minute film of 3-4 chapters: restored photos with simple parallax, voices in surprise mode, music, burned-in captions, plus (optional) a TimelineJS or Closeread page for the private link. Voices in surprise mode: (i) her existing recorded voice from home video, voicemail or voice notes, if any survive and the proxy agrees; (ii) relatives speaking about her, recorded one at a time from the people the maker has decided to bring in (OPEN (maker): nobody is in on it yet, as the charter says); (iii) her own letters and cards read by a relative, shown attributed. No synthetic or cloned voice of anyone (charter review 1.2). Spine threshold: see FQ1. It is a strict subset of the default, so no work is thrown away. Triggers: slice not at final quality at G9; hours logged under 60% of plan at G9; any chapter costing more than twice its budget twice in a row.

**Not doing.** A free-roam world as the deliverable; audience-played interludes; any dependency on a live web service on the night; YouTube as the only copy; Mojang branding or textures in public without re-reading the current terms [50]; asking the subject to play in public unless they want to.

**What would change this recommendation.** "Partly playable is a must" (flips to F7); 20 or more hours per week plus Java Minecraft owned plus a subject who loves Minecraft (use F2 for one or two chapters, not the whole piece); private gift only and no event (add a scroll page as the main companion, F6/F9); no big screen at the venue (the room argument weakens).

**What I need from you to lock this.** (1) Hours per week available. (2) Venue and who runs its AV. (3) Audience size and ages. (4) Whether you own Minecraft Java and whether the subject plays games. (5) Whether "partly playable" is a must. (6) Accept, reject or amend the default and the fallback. Already settled by the charter, not asked: the surprise, the premiere on 2027-02-27, Windows, and the ArtCraft apps (FilmCraft, alpha).

---

## Exemplars / recipes

Format for each: what it is; why it works; how it was made; what we can reuse; link. Links are pages I fetched or checked.

**E1. StoryCorps animated shorts (film).** *What:* more than 100 animations of real recorded conversations, shown on public TV and online. *Why it works:* a real voice carries it; the picture is a visual idea chosen from the storyteller's own world (a quilt structure for a folk-art storyteller). *How:* animators and producers sketch characters to resemble the storytellers, design backgrounds for the era, storyboard, revise through "several stages of feedback", and talk with the storytellers during production; length and timeline not stated [77]. *Reuse:* consult the subject during production; one visual idea per chapter; voice first. Links: https://storycorps.org/inside-storycorps-turning-words-into-visuals/ ; https://storycorps.org/animation/ [V]

**E2. Tribute slideshow as the floor (film).** *What:* the everyday format a family will compare us to. *Why it works:* 3-4 seconds per photo, one to three songs, 3-8 minutes, MP4 H.264 1080p 16:9, tested on the venue screen with captions checked from the back row, a USB copy and a cloud copy [85]. *Reuse:* the event kit (see Techniques T5). Our piece must be clearly more crafted but can borrow the logistics. Link: https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/

**E3. Kinoautomat (1967, hybrid with a live host).** *What:* a film that stopped at nine points so the audience could vote with red/green buttons. *Why it works:* a human moderator keeps the room together; only two options; the branches reconverge so the film stays one film. *How:* two synchronised projectors, a lens cap moved to switch cuts; numbered seat panels showed the votes [65]. *Reuse:* host plus two options plus reconverging structure. Link: https://en.wikipedia.org/wiki/Kinoautomat

**E4. My One Demand (2015, hybrid with phones).** *What:* a single continuous shot streamed to a cinema and online while viewers answered the narrator on their phones. *How:* live stream plus mobile interaction; no failure notes available [66][67]. *Reuse:* caution only; phone voting is new hidden code and risk. Link: https://www.blasttheory.co.uk/projects/my-one-demand/

**E5. Bandersnatch (2018, design pattern).** *What:* an interactive film. *Why it works for our purpose:* choices time out after about ten seconds and a default path plays; unsupported devices get a short fallback video. *How:* 150 minutes of unique footage in 250 segments, 35 days of filming, eight months of production, a bespoke Branch Manager tool, pre-caching of the next two segments [68]. *Reuse:* "default path plays" and "the fallback is a normal video". Link: https://en.wikipedia.org/wiki/Black_Mirror:_Bandersnatch

**E6. That Dragon, Cancer (2016, explorable memorial).** *What:* a roughly two-hour point-and-click game retelling the family's four-year fight with their son Joel's cancer. *Why it works / didn't:* a strict filter ("Does this scene help the player love Joel more?") [72]; criticised for a minigame that "didn't play very well", which Green says is the wrong frame [73]; modest sales [70]; still sold at $9.99 with 90% positive of 1,374 reviews [71]. *How:* about 2012 to January 2016, Unity, a small team, Ouya funding then Kickstarter [70]; a documentary about the family aired in 2016 [70]. *Reuse:* the scene filter; the idea that the mechanic can be a metaphor, not a game. Not a register to copy for a living 50+ subject (see Pitfalls). Links: https://en.wikipedia.org/wiki/That_Dragon,_Cancer ; https://store.steampowered.com/app/419460/That_Dragon_Cancer/ ; https://gamedeveloper.com/design/game-as-memorial-i-that-dragon-cancer-i-developer-reflects

**E7. Kirtland's JP Memorial Zoo (2016-17, solo Minecraft).** *What:* a stone memorial with a poppy and a zoo with every animal, an octopus aquarium (his father fished) and smoked salmon in the cafe, built on an iPad and never published [74]. *Why it works:* every element is a fact about the father; it stays alive (new animals added as the game adds them). *Reuse:* build from the person's loves; one object per fact. Link: https://www.sootoday.com/great-stories/son-builds-virtual-minecraft-zoo-and-memorial-to-honour-his-deceased-father-9-photos-707477 (my WebFetch got HTTP 403; text read from the sibling's saved copy [L])

**E8. Pforzheimer House on Minecraft (2020, shared Minecraft).** *What:* a house replica toured live on 2020-04-10. *Why it works:* it is a specific shared place; participants described nostalgia and comfort. *How:* a resident tutor lead, floor plans plus Google Maps, survival mode, 10,000+ bricks, about three weeks, several builders [75]. *Reuse:* a real place built from plans and memory; a guided live tour with a host who talks. Link: https://www.thecrimson.com/article/2020/4/30/minecraft-pfo/

**E9. Pendar2 hub (2019, community Minecraft).** *What:* a closed server's hub turned into a wall of signs by players. *Why it works:* the messages are personal and the writer reports he could not stop reading them. *How:* players returned and built; the admin sent Mojang a world download [76]. *Reuse:* a "wall of messages" is a reading experience for one person, not for a room. Link: https://www.minecraft.net/en-us/article/remembering-pendar2 (read from saved copy [L])

**E10. Snow Fall (2012, scroll story).** *What/why/how:* see Q2 [79]. *Reuse:* cut flashy transitions that distract or tire readers; keep a simpler build for weaker devices; "Editing, editing, editing" [79]. Own files still served after 14 years in the sibling check [89]. Links: https://www.nytimes.com/projects/2012/snow-fall/index.html [V] ; https://source.opennews.org/articles/how-we-made-snow-fall/

**E11. Welcome to Pine Point (2011, scroll/hub memory piece).** *What:* an NFB interactive documentary about a vanished mining town, assembled from ex-residents' photographs, audio and memories, with a soundtrack by The Besnard Lakes [81]. *Why it matters to us:* it is the nearest relative of a personal-texture project in web form; the NFB page still responds [82]. *Reuse:* memory as the structure; but creators and software are not documented in my sources. Links: https://pinepoint.nfb.ca/ [V] ; https://en.wikipedia.org/wiki/Welcome_to_Pine_Point

**E12. TimelineJS (scroll/timeline template).** *What:* a Knight Lab open-source tool that builds a slide-and-timeline from a Google Sheet. *Why use it:* the fastest no-code route to a companion life timeline; Knight Lab's own tips: keep to 20 slides, tell one chronological narrative, include events that build up to major occurrences [54]. *Limits:* the sheet must be public to the web; for control use JSON and your own server [54]. Link: https://timeline.knightlab.com/

**E13. Unpacking (design reference only).** *What:* a wordless life told through objects in successive homes. *Relevance to formats:* Twitch viewers narrate their own lives as they watch someone else play [83]; a studio planned 1.5 years and took about twice that [84]. *Reuse:* the "audience talks while the host plays" effect for an interlude; the time-overrun warning. Links: https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game (text from saved copy [L]); https://en.wikipedia.org/wiki/Unpacking_(video_game); more in `games.md` [88].

**E14. Closeread (scroll story recipe).** *What:* a Quarto format: a `.qmd` file with `format: closeread-html`, sections marked with fenced divs, rendered by `quarto render` to static HTML that can be hosted anywhere [56]. *Reuse:* a scriptable (command-line) scroll story, in the spirit of Principle 9. Link: https://closeread.dev/

---

## Tools

Costs and free tiers as of 2026-10-18 unless noted. "Scriptable" answers Principle 9 (prefer scriptable tools).

| Tool | Cost / free tier | Platform | Learning curve | Scriptable / CLI | Notes |
|---|---|---|---|---|---|
| DaVinci Resolve 21 | Free (8-bit up to 60 fps, up to UHD); Studio $295 [63] | Mac, Windows, Linux [63] | Medium to high | Page names only "workflow integration and encoding APIs" [63] | GUI for refinement and the final eye; not the assembly engine. Scriptable assembly route: route A in FQ2 (an ffmpeg filtergraph written from `timeline.json`); see `toolchain` and `agent-pipeline` |
| FilmCraft v0.8.0 (ArtCraft, early alpha) | Free, open source (charter) [96][99] | Windows (maker's PC); Linux CLI run in the container [99] | Medium | CLI: `filmcraft-cli` (`captions.*`, `file.import`, `file.exportMedia`); `.fcproj` is UTF-8 JSON [96][97] | Second renderer and bridge to hand fixes (FQ2 route D); alpha; Ken Burns through OTIO not tested. FilmCraft's README says Windows and Linux "get far less testing than macOS" [96]; the maker's Windows build is one of the least-tested platforms, one more reason route A is the engine and FilmCraft the refinement layer |
| Clipchamp | Free: 1080p export, no watermark [64] | Web; Windows app | Low | No | Floor-level editor; plan details beyond export not stated |
| OpenTimelineIO 0.18.1 with adapters | Free, pip [95] | Python | Medium | Python API; EDL, FCPXML, Kdenlive and MLT adapters [95] | Exchange file; all four writers ran [RUN]; give Kdenlive the `.otio` (its adapter is deprecated); captions and Ken Burns do not travel in plain OTIO or EDL |
| Kdenlive, Shotcut, Canva, Animoto | **UNVERIFIED** (fetches failed or not attempted) | | | | See the `toolchain` track |
| FFmpeg | Open source (general knowledge; Replay Mod docs require it) [44] | Win, Mac, Linux | Medium | CLI | Needed for Replay Mod rendering [44] and for Godot's Theora conversion [41]; also for captions burn-in and transcodes. Route A of FQ2 is one ffmpeg command written by a Python script (9 s for a 20 s test film [RUN]) |
| PowerShell `Get-FileHash` | Built in (Windows PowerShell 5.1) [100] | Windows | Low | CLI | SHA-256 by default; `mk_manifest.ps1` writes a sha256sum-format list (FQ4) |
| `sha256sum` or equivalent | Free | All | Low | CLI | NIST: store hashes separately from files [18] |
| Replay Mod | Free; GPL-3.0 per `games.md` [88]; made by CrushedPixel and johni0702, "record, replay and share" with camera paths and a built-in video creator [43] | Java only: Fabric for 1.14+, Forge for 1.12.2 and below; Bedrock not mentioned [44] | Medium (keyframe timeline up to 10 min; position, time, spectator keyframes; cubic spline) | GUI; headless use **UNVERIFIED** | Records only loaded chunks, must start when joining a world; renders MP4/WebM/MKV or image sequences; some launchers unsupported [44] |
| Flashback | Free; licence all rights reserved [45] | Java, Fabric; Minecraft 1.21-1.21.11 and 26.1-26.3 listed [45] | Medium | GUI | 12.8 million downloads; features beyond record and playback not stated on the page [45] |
| Bedrock `/camera` | Part of the game; needs cheats and permission level 1 [46] | Bedrock and Education only [46] | Medium (commands, JSON splines) | Commands in command blocks or functions | Easing, fade, FOV, attach to entity; `play_spline` from a behavior pack, added 26.0 [46] |
| Minecraft Java launcher | Game must be purchased; Microsoft account [49] | Win, Mac, Linux | Low | `launcher_profiles.json` holds installations [49] | Offline only after first download; old versions available [49] |
| Mineways, MagicaVoxel, Blockbench | See `games.md` [88] | | | | MagicaVoxel `.vox` loads in three.js [52] |
| Godot 4 | Free, MIT [42] | Win, Mac, Linux; exports to Android, iOS, Web [42] | Medium (GDScript, Python-like) | Command-line export is common practice (**UNVERIFIED** here) | Web export: WebGL 2, single-threaded default since 4.3, no C# on web [40]; video only Ogg Theora [41] |
| three.js | Free (general knowledge); official examples [51][52] | Browser | High for a beginner (course 93 h) [53] | Build tools (npm) | Pin versions; vendor files |
| Three.js Journey | $95 (course), $120 bundle [53] | Online | n/a | n/a | 93 hours of video, 66 lessons; needs JS basics [53] |
| Spline | Free: watermark, no code export, self-hosted export Enterprise only; Hobby $15/mo ($12 yearly) [62] | Web app | Low | No | Hosting lock-in |
| GDevelop | Free: 3 cloud projects, 1 desktop publish a day, unlimited publishing on gd.games [61] | Web, desktop | Low to medium | Event sheets | Whether Free allows a manual HTML5 export was not clear [61] |
| Bitsy | Free; HTML5; latest devlog v8.15 (2026-02-12); source on Codeberg [59] | Browser | Low | No | Export format **UNVERIFIED** |
| Twine | Free, open source; publishes to HTML [60] | Desktop, browser | Low to medium | Story formats (Chapbook, Harlowe, Snowman, SugarCube) [60] | Macros are code |
| TimelineJS | Free; MPL-2.0 [54][55] | Browser; Google Sheets | Low | JSON mode for self-hosting [54] | Public-to-web sheet; keep it forever [54] |
| Closeread and Quarto | Free; Quarto is open source [56][57] | Needs Quarto installed [56] | Low to medium | `quarto render` [56] | Static HTML output |
| StaticCrypt | Free, MIT [35] | Command line / any static host | Low | CLI | Shared password; guessable offline if weak [35] |
| Cloudflare Pages, Access, R2 | Access Free: $0; 50-user limit on the Free plan confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91]; Pages: 25 MiB per file [31]; R2: 10 GB-month free [32] | Web | Medium | Wrangler CLI (general knowledge) | Single account SPOF |
| GitHub Pages | Free sites public; private needs Enterprise Cloud [26]; 1 GB limit [27] | Web | Low | Git | Not for private family material |
| Netlify | Password protection on Pro [33] | Web | Low | CLI | Shared password |
| YouTube | Free; Unlisted or Private [34] | Web | Low | API | Private videos may be reviewed by YouTube systems and human reviewers [34] |
| itch.io | Free; Restricted pages with password; HTML5 zip limits [36][37] | Web | Low | butler CLI (general knowledge) | Embed privacy **UNVERIFIED** |
| Apple Guided Access | Built in [13] | iPhone and iPad | Low | No | Locks to one app, not to a page [13] |
| Webrecorder (ArchiveWeb.page, ReplayWeb.page) | Free Chrome extension and player; Browsertrix paid [23] | Chrome | Low to medium | Developer tools and CLI [23] | WACZ is acceptable to the Library of Congress [17] |

---

## Techniques

**T1. Interlude-ready chapter structure.** Build each chapter as a self-contained 90-150 second film with a labelled optional slot (60-90 s) before the next chapter. Slot content defaults to a captured video. Pointer: see Q7 plan.

**T2. Default path plays.** Any interactive moment completes itself on screen after about 20 seconds of inactivity, and the film continues. Based on *Bandersnatch*'s default-after-timer [68] but softened so nobody feels timed [10].

**T3. Capture every interactive as video.** Record a clean run of each interlude or world tour; edit it into the linear master. This doubles as the failure-ladder fallback and as the archival "video of the software in use" [16].

**T4. Dual master and caption trio.** Export: (1) FFV1 v3 in .mkv or ProRes .mov master [15]; (2) H.264 MP4 1080p access copy [85]; (3) a burned-in (open) caption version for any player; (4) a clean version with `.srt` and `.vtt` sidecars [4]. Keep captions at 42 characters or fewer per line, two lines at most [5]; for a room with viewers over 70, 130-145 words per minute, never above 160 [105][107][J]. Caption size: line height 7-8% of picture height (BBC [105]); with ffmpeg's subtitles filter, `FontSize=23` gives about 8.0% at 1080p [RUN, FQ2]. The venue projection master (DCP, or ProRes at the projector's resolution and frame rate) is decided by the `theatrical-delivery` track by G13; the H.264 MP4 is the access and fallback copy. TODO(research): RQ2 found that for a venue taking HDMI from a laptop, the 1080p24 H.264 file can be the venue master; reconcile before G13.

**T5. Event kit.** Send the file to the venue a day before; ask which formats, resolutions and aspect ratio it prefers; play it on the real screen and speakers; check captions from the back row; arrive early; bring a USB stick and a cloud copy [85]. Add: the laptop with the film and interlude already open; a second USB with the MP4; the printed running order.

**T6. Self-contained folder.** For anything web: relative paths, no CDN, no analytics, no third-party fonts or embeds, versions pinned, a README saying how to serve it; test on a clean machine with no internet. Reason: the third-party script is what changed first in *Snow Fall* [89], and Glitch and Flash show the platform risk [24][25].

**T7. Host-click start.** For web or Godot-web builds, show a "Press any key to begin" splash that the host presses [11][12][40]; for kiosks use Chrome's `--autoplay-policy=no-user-gesture-required` flag or enterprise policy [11], and on a tablet Guided Access [13] (test the whole setup for an hour).

**T8. Archive and handover.** 3-2-1 [22]; SHA-256 manifest stored separately [18]; yearly power-up and hash check; replace HDDs at about 5 years and copy any disc by 20 years [18][J]; a one-page README (what it is, how to play, which files, passwords) on paper and in the folder; legacy contacts set [38][39]; at least two relatives hold a drive (in-on-it relatives only until the reveal). One copy may be a BD-R burned from the final `archive.iso` in February (buy in January 2027; rehearse a small burn in December; verify with `verify_manifest.ps1`) [FQ7].

**T9. Private-link recipe.** Film: a copy on a drive or account she cannot open, never a shared family cloud library (a tip-off risk the charter names [C]); until the reveal, USB drives held by in-on-it relatives only; any shared online copy is created after 2027-02-27. YouTube Private with an invite list only after the maker's explicit yes to Google reviewers seeing family footage [34]. Page: static folder on Cloudflare Pages behind Access with an email allow-list (Free plan; 50-user limit on the Free plan confirmed on [28]'s comparison table, read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91]) [28][30], with the MP4 hosted separately because of the 25 MiB file cap [31]. Add a long random password only if using StaticCrypt [35].

**T10. Motion and flash pass.** Before any export: no more than three flashes in a second [3]; no auto-moving element longer than five seconds without a pause mechanism on web [2]; honour reduced motion on web [7]; avoid fast pans in a voxel fly-through on a big screen [7][J].

**T11. Pacing in the room.** Chapter-length cards; 3-4 seconds per photo for montage, longer for group photos and titles [85]; a "breath" frame between chapters; background music well below the voice [1][J]; test with one 60+ viewer.

**T12. Host script for an interlude** [J]. Three lines: setup ("Whose kitchen is this?"), call-out ("Where does this go?"), return ("And now back to 1983"). One verb. No score, timer or fail.

**T13. Minecraft pre-flight checklist** (answer before any build): Java or Bedrock; edition owned; OS; exact version (year-based from 26.1 on Java [48]); Fabric or Forge for Replay Mod [44]; Java runtime; FFmpeg present [44]; world backed up; Mojang terms re-read the week of the premiere [50]; use original voxel assets if shown publicly [88].

**T14. Week-9 slice test** (pass all): final-quality audio and picture for one chapter; captions in all three forms; plays from a USB stick on a TV-class screen; a 60+ viewer watches from 3 metres and reports reading comfort; hash manifest exists; hours logged.

---

## Pitfalls and ethics

- **Choosing by what is exciting to build.** The explorable formats score highest on charter fit and learning and lowest on room fit, accessibility, finish and failure resilience (matrix above). Starting from the audience, venue and charter, the film wins; a hybrid needs evidence the audience wants playing.
- **"No code yet" is not "no code ever".** Coding estimates above are honest: three.js and Godot cost real learning; "no-code" tools hide code in UI, in macros or in event sheets (Q8). AI writes code the maker must still run and judge.
- **Minecraft edition confusion.** Replay Mod and Flashback are Java; Bedrock has its own camera command; an iPad world is Bedrock; Java version numbering changed in 2026 [44][45][46][48][74]. Do not plan a capture pipeline before the edition and version are known.
- **Mojang rules.** Per the sibling's reading of the Usage Guidelines: personal use is relaxed; sharing "with the community" is treated as commercial; gameplay may not be shown publicly in physical locations in certain ways; permissions are revocable [50][88]. The round-1 follow-up read the page itself (HTTP 200 on the second attempt; FQ6, [92]). A family premiere in a hired venue is still a grey area, and Mojang says it cannot advise on a specific project [88]. Re-save the excerpt the week of the event, because the page reserves the right to change, and prefer original voxel assets.
- **Longevity hand-waving and single owners.** A link on someone's account is not an archive. Archive is a scored column (matrix) and a handover plan (T8).
- **Hybrids as a way not to decide.** A hybrid is recommended only with a presentation plan, a failure ladder and gates (Q7; recommendation).
- **Press is not audience evidence.** Memorial Minecraft stories are second-hand and solitary; I found no creator reflection from a non-gamer room [74][75][76].
- **Real memories stay real (Principle 4).** Captured interludes and Minecraft recreations are *reconstructions* and must be visibly so (title card or style). AI restoration of photos is for the `ai-imagery` track.
- **Dignity and consent (Principle 5).** A film is curated: the room cannot wander into a chapter the family did not approve. An explorable world lets viewers open any door, which makes consent harder. Hard chapters go to the trusted proxy named under Principle 5 (the maker, per the charter) and to the relatives in them; the subject sees nothing before the reveal (charter Known facts).
- **The subject is alive.** The older-adult study found people dislike stories that promote "depression and gloom" [10]; death-forward games such as *That Dragon, Cancer* are sources of devices, not of register (see `games.md` [88]).
- **Photosensitivity and motion on a big screen.** Follow the three-flash rule and be cautious with large fast pans [3][7].
- **Music rights.** A personal streaming subscription does not authorise public performance [85]; venues may need licences (vendor claims about prices and penalties: UNVERIFIED) [85]; the sibling notes list clearance cost examples [89]. A private gift is lower risk than a public premiere.
- **Privacy.** "Unlisted" is not private [34]; GitHub Pages is public unless Enterprise [26]; a TimelineJS sheet is public to the web [54]; StaticCrypt is guessable offline if the password is weak [35]. Personal material stays private; this report publishes nothing and sends nothing anywhere.
- **GUI-only steps.** The charter says GUI control of the maker's apps is not connected. Replay Mod and Resolve are GUI tools the maker must drive; FFmpeg, Quarto render, hashing and StaticCrypt are scriptable [44][56][35][63].

---

## Open questions / gaps

1. **Search budget.** The shared WebSearch budget was exhausted, so I could not find creator threads (X/Twitter, Reddit, YouTube), learner-made life-journey films, or any memorial made with Replay Mod or Flashback, a Godot or a three.js life story. If more discovery is wanted, a follow-up message can continue the search, or the run's `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` can be raised.
2. **No evidence of mixed-age, non-gamer room reactions** to any explorable or hybrid life journey. Treat all such formats as untested for our audience. A cheap test: show a 60-second captured prototype to three relatives of different ages and ask them what they noticed and who they wanted to talk to.
3. **Pages I could not verify:** Minecraft Usage Guidelines (now read in FQ6), Chunker (429), Vimeo plan details, Canva (403), Kdenlive, PlayCanvas (404), the BBC subtitle guidelines (read in FQ5), the Mozilla Hubs end-of-support page (did not load), VLC kiosk flags (page lists them only via `vlc -H`), Bitsy's export format, GDevelop's Free manual HTML5 export, private-object handling in R2, whether the itch.io Restricted password protects the HTML5 embed, whether *Late Shift* cinema screenings used audience voting, whether *Snow Fall*, *Pine Point* and TimelineJS's example links render in a 2026 browser.
4. **Caption speed for older viewers** has no source for 70+ (FQ5 found BBC and DCMP figures for hearing audiences). Test real captions on 60+ viewers at FontSize 20, 23 and 26.
5. **Unknowns that change the answer:** hours per week; venue and AV; audience size and ages; whether "partly playable" is a must; Minecraft ownership and edition; who is brought in on the project (the charter says nobody yet). Settled by the charter, not open: the surprise; the premiere on 2027-02-27; FilmCraft among the installed ArtCraft apps (alpha, refinement layer); the success test (charter review 1.1).
6. **Phase 0/1 experiments worth running** (each is cheap): (a) a 60-second film chapter with three caption sizes on a real TV; (b) a Closeread or TimelineJS page for one chapter in under two hours; (c) a 10-20 h interlude prototype in Bitsy or GDevelop or Godot, captured to video; (d) a dry-run of the failure ladder; (e) a hash-manifest and three-copy backup rehearsal; (f) only if Java Minecraft is owned, a one-diorama Replay Mod capture.
7. **Prices not verified:** photo-book printing, Vimeo, custom domains, and any paid hosting beyond the free tiers listed.

---

## Sources

Tags: [P] official or primary; [S] journalism quoting a creator; [T] Wikipedia or encyclopedic; [L] a sibling-saved copy read as data; [V] liveness checked by me on 2026-10-18; all pages fetched on 2026-10-18 unless another date is given. [C] is the charter.

**[C]** Life Journey — Project Charter — CHARTER.md — read 2026-10-18 — principles, rubric, constraints.

**Accessibility and audience**
[1] W3C WAI — Web Accessibility for Older Users — https://www.w3.org/WAI/older-users/ — undated (notes it is partly out of date) — [P] barriers and recommendations for older users.
[2] W3C — Understanding SC 2.2.2 Pause, Stop, Hide (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html — [P] five-second rule.
[3] W3C — Understanding SC 2.3.1 Three Flashes or Below Threshold (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html — [P].
[4] W3C — Understanding SC 1.2.2 Captions (Prerecorded) (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html — [P] open vs closed captions.
[5] Netflix — English Timed Text Style Guide — https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide — undated — [P] 42 characters, two lines, 20 cps adult.
[6] Game Accessibility Guidelines — full list — https://gameaccessibilityguidelines.com/full-list/ — [P] community checklist.
[7] MDN — prefers-reduced-motion — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — [P] vestibular triggers.
[8] Wikipedia — 10-foot user interface — https://en.wikipedia.org/wiki/10-foot_user_interface — [T].
[9] Wikipedia — Safe area (television) — https://en.wikipedia.org/wiki/Safe_area_(television) — [T] percentages not confirmed.
[10] Lee S, Oh H, Shi C-K, Doh YY — Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population, JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ — 2021 — [P][L] 40 participants; read from the sibling's saved text.
[11] Chrome for Developers — Autoplay policy in Chrome — https://developer.chrome.com/blog/autoplay — last updated 2017-09-13 — [P] gesture, engagement, flag, enterprise policy.
[12] WebKit — New video policies for iOS — https://webkit.org/blog/6784/new-video-policies-for-ios/ — 2016-07-25 — [P].
[13] Apple Support — Use Guided Access on iPhone/iPad — https://support.apple.com/en-us/111795 — [P].

**Preservation, hosting, privacy**
[14] Library of Congress — Recommended Formats Statement (index, revision 2025-2026) — https://www.loc.gov/preservation/resources/rfs/ — [P].
[15] Library of Congress RFS — Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — [P] FFV1/MKV, ProRes; MP4 as proxy.
[16] Library of Congress RFS — Software and Video Games — https://www.loc.gov/preservation/resources/rfs/software-videogames.html — [P] source, build, video of use.
[17] Library of Congress RFS — Web Archives — https://www.loc.gov/preservation/resources/rfs/webarchives.html — [P] WARC, WACZ, limits.
[18] NIST IR 8387 — Digital Evidence Preservation, Guttman, White, Walraven — https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8387.pdf (DOI https://doi.org/10.6028/NIST.IR.8387) — September 2022 — [P] media longevity Table 1; text extracted locally with pdftotext.
[19] NDSA — Levels of Digital Preservation — https://ndsa.org/publications/levels-of-digital-preservation/ — v2.1 March 2026 — [P] matrix itself not read.
[20] Library of Congress — Personal Archiving — https://www.digitalpreservation.gov/personalarchiving/ — [P] hub page only.
[21] Wikipedia — M-DISC — https://en.wikipedia.org/wiki/M-DISC — [T].
[22] Backblaze — Why the 3-2-1 Backup Strategy is the Best, Yev Pusin — https://www.backblaze.com/blog/the-3-2-1-backup-strategy/ — 2024-05-23 — [S] vendor.
[23] Webrecorder — https://webrecorder.net/ — [P].
[24] Wikipedia — Adobe Flash — https://en.wikipedia.org/wiki/Adobe_Flash — [T] end of life dates; Ruffle, Flashpoint.
[25] Wikipedia — Glitch, Inc. — https://en.wikipedia.org/wiki/Glitch,_Inc. — [T] hosting ended 2025-07-08 (announced May 2025).
[26] GitHub Docs — Changing the visibility of your GitHub Pages site — https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site — [P].
[27] GitHub Docs — GitHub Pages limits — https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits — [P].
[28] Cloudflare — Access product and pricing page — https://www.cloudflare.com/zero-trust/products/access/ — fetched with a plain HTTP request — [P] Free plan $0; 50-user limit on the Free plan: confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91] (FQ3).
[29] Cloudflare Docs — Zero Trust account limits — https://developers.cloudflare.com/cloudflare-one/account-limits/ — updated 2026-10-16 — [P] 1,000 emails per rule; no 50-user cap found in its text (FQ3).
[30] Cloudflare Docs — Access policies — https://developers.cloudflare.com/cloudflare-one/policies/access/ — [P] deny by default; email selectors.
[31] Cloudflare Docs — Pages limits — https://developers.cloudflare.com/pages/platform/limits/ — [P] 25 MiB per file.
[32] Cloudflare Docs — R2 pricing — https://developers.cloudflare.com/r2/pricing/ — updated 2026-10-01 — [P].
[33] Netlify Docs — Password protection — https://docs.netlify.com/manage/security/secure-access-to-sites/password-protection/ — [P].
[34] YouTube Help — Change video privacy settings — https://support.google.com/youtube/answer/157177 — [P].
[35] StaticCrypt — https://github.com/robinmoisson/staticrypt — [P] README.
[36] itch.io — Access control — https://itch.io/docs/creators/access-control — [P].
[37] itch.io — Uploading HTML5 games — https://itch.io/docs/creators/html5 — [P].
[38] Apple Support — Legacy Contact — https://support.apple.com/en-us/102631 — [P].
[39] Google Account Help — About Inactive Account Manager — https://support.google.com/accounts/answer/3036546 — [P].

**Engines and tools**
[40] Godot Docs — Exporting for the Web — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html — [P].
[41] Godot Docs — Playing videos — https://docs.godotengine.org/en/stable/tutorials/animation/playing_videos.html — [P] Ogg Theora only in core.
[42] Godot Docs — FAQ — https://docs.godotengine.org/en/stable/about/faq.html — [P] MIT, GDScript, exports.
[43] Replay Mod — https://www.replaymod.com/ — [P] responds [V].
[44] Replay Mod — Documentation — https://www.replaymod.com/docs — [P] versions, recording, keyframes, FFmpeg.
[45] Modrinth — Flashback — https://modrinth.com/mod/flashback — [P] Java, Fabric, ARR, versions.
[46] Minecraft Wiki — Commands/camera — https://minecraft.wiki/w/Commands/camera — [T] Bedrock and Education only; play_spline 26.0.
[47] Minecraft Wiki — Java Edition level format — https://minecraft.wiki/w/Java_Edition_level_format — [T].
[48] Minecraft Wiki — Java Edition 26.1 — https://minecraft.wiki/w/Java_Edition_26.1 — [T] released 2026-03-24; year-based naming.
[49] Minecraft Wiki — Minecraft Launcher — https://minecraft.wiki/w/Minecraft_Launcher — [T] Microsoft account; offline after download.
[50] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched in round 1 on the second attempt (HTTP 200); see [92]. Earlier attempts returned HTTP 503 and a timeout.
[51] three.js — webgl_geometry_minecraft example — https://threejs.org/examples/webgl_geometry_minecraft.html — [P].
[52] three.js — webgl_loader_vox example — https://threejs.org/examples/webgl_loader_vox.html — [P] page text minimal.
[53] Three.js Journey — https://threejs-journey.com/ — [P] 93 h, $95, JS prerequisite.
[54] Knight Lab — TimelineJS — https://timeline.knightlab.com/ — [P] fetched with a plain HTTP request; tips, FAQ, privacy.
[55] NUKnightLab — TimelineJS3 on GitHub — https://github.com/NUKnightLab/TimelineJS3 — [P] MPL-2.0.
[56] Closeread — https://closeread.dev/ — [P].
[57] Quarto — https://quarto.org/ — [P] open source.
[58] The Pudding — How to implement scrollytelling with six different libraries — https://pudding.cool/process/how-to-implement-scrollytelling — [P].
[59] Bitsy on itch.io — https://ledoux.itch.io/bitsy — [P] devlog v8.15 2026-02-12.
[60] Twine — https://twinery.org/ — [P].
[61] GDevelop — Pricing — https://gdevelop.io/pricing — [P] undated; Free plan limits.
[62] Spline — Pricing — https://spline.design/pricing — [P].
[63] Blackmagic Design — DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — [P] Resolve 21 free; Studio $295.
[64] Clipchamp — Pricing — https://clipchamp.com/en/pricing/ — [P] 1080p free, no watermark.

**Examples**
[65] Wikipedia — Kinoautomat — https://en.wikipedia.org/wiki/Kinoautomat — [T]. kinoautomat.cz did not respond on 2026-10-18 [V].
[66] Wikipedia — Interactive film — https://en.wikipedia.org/wiki/Interactive_film — [T] My One Demand, Kinoautomat, YouTube annotations; final 10k characters unread.
[67] Blast Theory — My One Demand — https://www.blasttheory.co.uk/projects/my-one-demand/ — [P].
[68] Wikipedia — Black Mirror: Bandersnatch — https://en.wikipedia.org/wiki/Black_Mirror:_Bandersnatch — [T] first 100,000 characters read.
[69] Wikipedia — Late Shift (video game) — https://en.wikipedia.org/wiki/Late_Shift_(video_game) — [T] 2017; cinema voting not mentioned.
[70] Wikipedia — That Dragon, Cancer — https://en.wikipedia.org/wiki/That_Dragon,_Cancer — [T].
[71] Steam — That Dragon, Cancer — https://store.steampowered.com/app/419460/That_Dragon_Cancer/ — 2026-10-18 — [P] $9.99; 90% of 1,374 reviews.
[72] Game Developer — Game as memorial: That Dragon, Cancer developer reflects — https://gamedeveloper.com/design/game-as-memorial-i-that-dragon-cancer-i-developer-reflects — 2014-11-12 — [S].
[73] The Spinoff — "Death is the thing we all share" (Ryan Green) — https://thespinoff.co.nz/pop-culture/02-06-2017/death-is-the-thing-we-all-share-why-one-father-made-a-video-game-about-his-sons-cancer-battle — 2017-06-02 — [S].
[74] SooToday — Son builds virtual Minecraft zoo and memorial to honour his deceased father — https://www.sootoday.com/great-stories/son-builds-virtual-minecraft-zoo-and-memorial-to-honour-his-deceased-father-9-photos-707477 — 2017-09-01 — [S][L] my WebFetch got 403; read from the sibling's saved copy.
[75] The Harvard Crimson — A House, Pixelated, Can Stand — https://www.thecrimson.com/article/2020/4/30/minecraft-pfo/ — 2020-04-30 — [S].
[76] Minecraft.net — Remembering Pendar2 (Tom Stone) — https://www.minecraft.net/en-us/article/remembering-pendar2 — 2019-04-06 — [P][L] my WebFetch got 503; read from the sibling's saved copy.
[77] StoryCorps — Inside StoryCorps: turning words into visuals — https://storycorps.org/inside-storycorps-turning-words-into-visuals/ — [P].
[78] StoryCorps — Animation index — https://storycorps.org/animation/ — [V] HTTP 200, 73,712 bytes.
[79] OpenNews Source — How We Made Snow Fall — https://source.opennews.org/articles/how-we-made-snow-fall/ — undated in my fetch (the sibling gives 2013) — [P].
[80] The New York Times — Snow Fall — https://www.nytimes.com/projects/2012/snow-fall/index.html — [V] HTTP 200, 177,243 bytes; rendering not tested.
[81] Wikipedia — Welcome to Pine Point — https://en.wikipedia.org/wiki/Welcome_to_Pine_Point — [T].
[82] NFB — Welcome to Pine Point — https://pinepoint.nfb.ca/ — [V] HTTP 200, 53,014 bytes; no flash/swf strings found; rendering not tested.
[83] Eurogamer — The creators of Unpacking on developing a "weird", queer, BAFTA-winning game — https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game — April 2022 — [S][L] fetch tool blocked this domain; read from the sibling's saved copy.
[84] Wikipedia — Unpacking (video game) — https://en.wikipedia.org/wiki/Unpacking_(video_game) — [T].
[85] Parting Stone — How to Make a Slideshow for a Funeral — https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/ — undated (mentions 2026 prices) — [S] vendor blog; length, timing, export, venue tips; licensing figures UNVERIFIED.
[86] itch.io — memorial tag — https://itch.io/games/tag-memorial — [V] 12 results at fetch time.
[87] Bruno Simon — portfolio — https://bruno-simon.com/ — [V] HTTP 200, 58,809 bytes; existence proof only.
[88] Sibling notes — research/games.md — read 2026-10-18 — Minecraft terms (Q7, source [42] there), memorial worlds (Q5), design devices.
[89] Sibling notes — research/animated.md — read 2026-10-18 — Snow Fall asset check (Q6), tribute-film guidance, exemplars E1-E27.

---

## Follow-up research (round 1)

Researcher: Sonnet, Sunday 2026-10-18, in answer to the seven follow-ups in `reviews/format-round1.md`. Run in the cloud container (Linux, 4 vCPU, no GPU), not on the maker's Windows PC. Every web page was treated as data. New sources continue the numbering at [90]. New tags: **[RUN]** I ran it in the container on 2026-10-18 and inspected the output; **[J]** my judgement. Evidence scripts and the dated Minecraft excerpt are in `research/sources/` (`format-round1/README.txt` lists them).

**Constraints on this round.** The shared web-search budget was used up before I started, so I used no search engine; every page below was fetched from a URL I already knew or saw linked on a page I had read. Blocked or unreadable: Ofcom (HTTP 403), B&H and Newegg (HTTP 403), `bbc.github.io/subtitle-guidelines` (HTTP 404 with a "Moved" page; the live BBC page at bbc.co.uk loaded fine from the container today, so the maker's-machine fetch the review asked for was not needed), the GitHub API for FilmCraft (403; raw files and release assets worked).

### Answers in brief

1. **Her existing voice: UNVERIFIED, and not answerable from the web.** Only the in-on-it family can say. I give the carriers and formats to ask about, a six-question ask, and a threshold for whether F-0 has a spine (FQ1).
2. **Headless film assembly: yes, four free routes ran in the container.** Best default: a ~40-line Python script that turns `timeline.json` + an asset folder + `captions.srt` into one ffmpeg command (20 s film, 1080p25, Ken Burns, crossfades, burned captions, two audio tracks: 9 s on 4 vCPU). FilmCraft's Linux CLI also ran headless: it imported an OTIO, imported the SRT, and exported H.264 with burned captions (21 s for a 20 s film). OTIO can emit EDL, FCPXML, Kdenlive and MLT files from the same timeline (FQ2).
3. **Cloudflare Access Free, 50 users: confirmed on the product page; the contradiction was a blank cell, not a second number.** The plans page itself has no table (FQ3).
4. **Windows hash list: PowerShell `Get-FileHash` (built in, SHA-256 by default).** `certutil -hashfile` does one file at a time. A tested script writes a `sha256sum`-compatible list (FQ4).
5. **Caption speed and size for 70+: no source I could read gives a figure for older viewers.** BBC says 160-180 wpm and line height 7-8% of picture height; DCMP says 130/140/160 wpm by level and cites a study in which age did not predict speed preference. My recommendation for a 70+ room is stated as judgement (FQ5).
6. **Minecraft Usage Guidelines: fetched on the second attempt (HTTP 200); dated excerpt saved** to `research/sources/minecraft-usage-guidelines-2026-10-18.txt` (FQ6).
7. **Recordable Blu-ray: Verbatim still lists BD-R, M-DISC BD-R and a USB-C Blu-ray writer today; street prices are UNVERIFIED; a burn cannot be tested in the cloud.** The ISO image and its checksum verification can be built and tested in the cloud (FQ7).

### FQ1. What recordings of her voice already exist, in what formats, who holds them?

**Answer: UNVERIFIED.** This is a fact about one family. Nobody has been asked, and the surprise rules out asking her. `research/story.md` Q4 already gives the search checklist (who to ask, what is at risk); this section adds what that checklist lacks: formats, handling, and a decision threshold.

**Carriers and formats to ask about.**

| Carrier | File or format you will meet | What I could verify | Handling |
|---|---|---|---|
| iPhone Voice Memos or phone video | `.m4a` for a shared voice memo ("Rendered" gives a single `.m4a`); phone video is usually `.mov` or `.mp4` [J] | Voice Memos sharing: `surprise-ops.md` source [17], snippet only | Ask for the original file, not a forward through a chat app (recompression, leaves a trail), per `story.md` Q4 |
| Chat voice notes (WhatsApp) | Opus audio, `.opus` | Wikipedia: "Since 2016, WhatsApp has been using Opus as its audio file format"; Opus used at 8-16 kHz sampling [94] [T] | Narrow-band and already compressed: usable as a spoken line, poor as a master [J] |
| Saved voicemail | Depends on phone and carrier | Export route for iPhone and Android voicemail **UNVERIFIED** (I did not retrieve a voicemail help page; Google Voice export is a snippet in `surprise-ops.md` [88]) | Ask the holder to keep it and not delete it; copy method is a later step |
| Camcorder tapes (VHS, VHS-C, Hi8, MiniDV), 8 mm film with sound | Tape or film; needs transfer | Lab prices and turnaround: `surprise-ops.md` sources [44][45] (VHS and MiniDV about $20-29 per tape; about 6 weeks at one lab) | Lab transfer is a calendar item: latest send dates are in `surprise-ops.md` |
| Audio cassettes, microcassettes, answering-machine tapes | Magnetic tape | Library of Congress: "Cleaning of magnetic tape and of cylinders is a delicate undertaking and should be carried out only by a preservation specialist"; let cool-stored material acclimate to room temperature before playing; store played tapes without rewinding and rewind just before playing; keep tape away from motors, loudspeakers and television sets [93] [P] | Do not clean or force a tape; one careful transfer pass, by a lab or a machine in good order [J] |

**Ask the in-on-it list only (six questions, by phone or in person; nothing in writing that she could see).** OPEN (maker): the charter says nobody is in on it yet and leaves "whether to bring anyone else in" to the maker, so this list is empty until that decision is made.
1. "Do you have any video or voice message of her, on your phone or on old tapes? Please do not delete anything, and please do not forward it to me."
2. "Roughly when was each made, and who else is speaking?"
3. "Is it still on a phone or card, or only on a tape, disc or old computer? Is the player still around?"
4. "Is she talking for a minute or more at a stretch, or only in short bits?"
5. "Who else might hold something (her friends, siblings, her old workplace or club)?"
6. "Are you happy for me to copy it and use it in a film that will be shown at a public gathering and kept by the family afterwards; is there anything she, or you, would not want shown in a room that is not all family?"

Record each item with the inventory fields in `story.md` Q4 (holder, device or format, rough date, who speaks, length, quality, original in hand, copies, consent).

**F-0 spine threshold [J].** F-0 is a 5-6 minute film of 3-4 chapters (earlier in this file). It needs about 45-90 seconds of clearly her speech per chapter, so roughly 3-5 minutes in total, or at least one clip of 60 seconds or more that can open and close the film. If the family can produce under about 2 minutes in all, F-0's "her real voice" spine fails; use the relatives' own voices (recorded as voice letters) and her letters or handwriting on screen instead. Principle 4 and the Fable review stand: found voice may be restored and used as itself, never extended or imitated.

### FQ2. Which free, headless, cloud-runnable route regenerates a photo-forward film master from a text timeline plus an asset folder, and burns captions from `.srt`?

**Test bed [RUN].** One `timeline.json` (4 stills, 5 s each, move per shot: zoom_in, pan_right, zoom_out; 1 s crossfades; voice and music WAVs), one `captions.srt` (4 cues, one with two lines), 1080p25 target. The photos were generated gradients with a label, so this proves the plumbing, not the look. Same inputs, four routes, each frame-checked at 2, 6, 12 and 17 s with the right cue showing.

| Route | Result [RUN] | Burns `.srt`? | Verdict |
|---|---|---|---|
| **A. ffmpeg 6.1.1 filtergraph written by a Python script** (`zoompan`, `xfade`, `subtitles`, `amix`) | 20 s, 1080p25, H.264 + AAC in **9.0 s** wall. A 30-shot, 120 s version: **63 s, 2.2 GB peak memory**, caption 26 at 102 s and caption 30 at 118 s both correct (no drift). | Yes: `subtitles=captions.srt:force_style='...'` | **Recommended default.** One binary, no GUI, deterministic, text in and file out. Scale beyond 30 shots in one graph is untested: render per chapter and join with the concat demuxer if memory climbs (UNVERIFIED) |
| **B. MLT `melt` 7.22.0** (the engine under Kdenlive and Shotcut) | No Ken Burns: 4 shots with luma crossfades plus subtitles in **6.6 s**; captions right at 2, 6, 12, 17 s. With an `affine` Ken Burns on every shot: **about 105 s** for the same 20 s. | Yes, as `-filter avfilter.subtitles av.filename=captions.srt` applied to the **whole serialised project** (`melt story.mlt -filter ...`) | Works, but slower with motion, needs `xvfb-run -a` because the image producer wants an X display, and photos must be pre-cropped to 16:9 or `affine` letterboxes them. Trap: a `-filter` placed after the last clip attaches to that clip only, and the captions came out at the wrong times |
| **C. Blender VSE in the background**, via `pip install bpy` (5.2.2 LTS) | 20 s at **960x540 draft** in **5.0 s**: image strips, `CROSS` effects, `TEXT` strips for captions, two sound strips, H.264 + AAC out. The virtual environment is about 1 GB. | **Not directly.** `bpy.ops.sequencer` has only `export_subtitles` ("Export .srt file containing text strips"), and the strip types include `TEXT` but no caption type. An agent parses the SRT and adds one `TEXT` strip per cue (my script does this) | Keep Blender for 2.5D parallax shots (see `toolchain.md`), not for assembly. Text defaults to a monospace font until a font file is loaded |
| **D. FilmCraft v0.8.0 Linux CLI** (tarball SHA-256 matches `craft-motion.md` [40]) | `filmcraft-cli` ran with no GPU. A `run` script created a project, imported my OTIO (**5 media linked, 0 offline**), added a caption track, imported the SRT (4 captions, snapped to 25 fps frames), and `export ... --preset "High Quality 1080p HD" --settings '{"burnCaptions":true}'` wrote a 1080p25 H.264/AAC file in **21.0 s** for 20 s of film (23.9 frames per second, CPU only). | Yes: `captions.import` for SRT; `burnCaptions` on export [98] | Viable second renderer and the bridge to the maker's GUI: the same `.otio` opens in FilmCraft on Windows for hand fixes. Default burned style is white text on a translucent box (not an outline). Alpha software; Ken Burns through OTIO was **not** tested (plain OTIO has no transform schema, see `craft-motion.md` Q3) |

**FilmCraft's project file is text.** `.fcproj` is "UTF-8 JSON with an explicit schema version" with the envelope `{"format":"filmcraft.project","schema_version":N,"generator":...,"project":{...}}`; media is referenced by path, never embedded [97]. The docs example says `schema_version` 13 and its history table stops there; the project the v0.8.0 CLI saved for me says `"schema_version":15,"generator":"FilmCraft 0.8.0"`, matching `craft-motion.md` Q2 (the docs are stale; trust the file). It was written compact on one line (11 KB for 4 stills, 1 audio file, 4 captions) and I did not hand-write one. Prefer driving the CLI (`filmcraft-cli commands` lists the commands; `captions.*`, `file.import`, `file.exportMedia` are the ones used) over writing JSON by hand [96][97].

**OpenTimelineIO as the portable contract [RUN].** `pip install opentimelineio` gives 0.18.1 with only three adapters (`otio_json`, `otioz`, `otiod`). Adapters are separate packages: `otio-cmx3600-adapter` 1.0.0 (EDL), `otio-fcpx-xml-adapter` 1.0.0, `otio-kdenlive-adapter` 0.0.3, `otio-mlt-adapter` 0.3.0 [95]. From one Python timeline built out of `timeline.json` all four wrote a file (EDL 4 events; FCPXML 1.8; Kdenlive 5 KB; MLT 2 KB). Notes: the Kdenlive adapter prints "This OpenTimelineIO adapter is deprecated and not maintained anymore! Kdenlive has native support for OpenTimelineIO since version 25.04", so give Kdenlive the `.otio` itself, not the adapter's file; the OTIO-made MLT file rendered under `melt` (20.01 s) but at 720x576 until forced with `-profile atsc_1080p_25`; EDL events for stills get truncated reel names (`p1`). **Not tested:** opening any of these in Resolve or Kdenlive (no GUI here), so "Resolve and Kdenlive import it" stays at the `craft-motion.md` level of evidence. Captions and Ken Burns do not travel in plain OTIO or EDL.

**Recommendation [J].**
1. Make `timeline.json` (plus `captions.srt` and an `assets/` folder) the source of truth in the repo. An agent regenerates the master with route A in the container whenever a chapter changes.
2. Emit an `.otio` from the same JSON so the maker can open the cut in FilmCraft or Kdenlive for hand edits and so FilmCraft's CLI can act as a second renderer (route D). Ask the maker, in the week-1 spike, to open the generated `.otio` once in FilmCraft on Windows.
3. Use route C only to produce parallax shots as PNG sequences or clips that route A then assembles.
4. Use route B only if the maker already edits in Kdenlive or Shotcut and wants a shared MLT project.

**Caption size gotcha that matters for FQ5 [RUN].** With `.srt` input, ffmpeg's `subtitles` filter treats `FontSize` as libass units on a 288-line canvas, not pixels. Measured at 1080p with DejaVu Sans: `FontSize=20` gives a line pitch of 75 px (6.9% of picture height); `FontSize=23` gives 86 px (7.96%). The `toolchain.md` example `FontSize=28` is therefore about 9.7%, larger than the BBC range below. The same percentages hold at 720p and 4K.

**Other traps.** Pass long filtergraphs with `-filter_complex_script` (my script does); Windows limits the command line, and the 30-shot graph was already 10.5 KB. Upscale each still 2x before `zoompan` to avoid shimmer [J]. `--project` in `filmcraft-cli` needs an existing file; start with `--save-as` and `run`.

### FQ3. Does Cloudflare's pricing state a 50-user limit for Access on the Free plan?

**Answer: yes, on the Access product page; the "No user limit" rows are the paid columns.** Read from the raw HTML of the page [28] (it redirected to `cloudflare.com/sase/products/access/`; fetched 2026-10-18 05:16 GMT):
- Pricing cards: "Free Plan $0 forever. Best for teams under 50 users or enterprise proof-of-concept tests." "Pay-as-you-go $7 per user/month (paid annually). Best for teams over 50 users..." "Contract Plan: custom price".
- Comparison table, group **Core capabilities**, row **Usage**: Free "50 user limit" | Pay-as-you-go "No user limit" | Contract "No user limit".
- Comparison table, group **Access controls (included in zero trust platform)**, row **Usage**: the **Free cell is empty**; the other two cells say "No user limit". Plain-text extraction drops the empty cell and makes the two rows look contradictory. They are not.
- The plans page `cloudflare.com/plans/zero-trust-services/` [90] has no plan table in its HTML (only "Start a proof of concept with our free plan today"), so it neither confirms nor denies. The docs account-limits page [29] (dateModified 2026-10-16) lists per-feature limits, some in "Standard users" and "Enterprise users" columns, but I found no 50-user cap in its text.
- New and useful: the docs setup page [91] says that if you chose the Zero Trust Free plan, completing onboarding by "selecting a subscription plan and entering your payment details" is "still needed but you will not be charged". A card on file is needed even for Free; this adds to the single-account, single-card risk already noted for Cloudflare.
- Still UNVERIFIED: what counts as a "user" for the 50 limit (unique identities per month, or enrolled seats). Ten to forty relatives with an email allow-list is well inside 50 either way.

### FQ4. Which built-in Windows tool lists SHA-256 hashes for a folder in one command?

**Answer: PowerShell `Get-FileHash`.** It is part of Windows PowerShell 5.1, which ships with Windows 10 and 11 (general knowledge), and "By default, the Get-FileHash cmdlet uses the SHA256 algorithm" [100]. `certutil -hashfile <file> SHA256` exists [101][103] but takes one file per call, so a folder needs a `for /r` loop (output format UNVERIFIED here: from memory it prints a header line, the hash, then "CertUtil: -hashfile command completed successfully").

**One command for a whole folder.** From inside the archive folder:

```powershell
Get-ChildItem -Recurse -File | Get-FileHash -Algorithm SHA256
```

Output format [RUN, PowerShell 7.5.4 [104]; Microsoft's 5.1 page shows the same three properties [100]]: a table with columns `Algorithm`, `Hash` (**uppercase** hex), `Path` (**absolute** path), one row per file.

```
Algorithm Hash                                                             Path
--------- ----                                                             ----
SHA256    00D75B5176B48CCC71D91BCC1D7B90FC2820429B1629B77FD1D5F4C5DCEE4F6D C:\LifeJourney\archive\README.txt
```

**A list you can check later, on Windows or Linux (`research/sources/format-round1/mk_manifest.ps1`).** It writes `SHA256SUMS.txt` one folder above the archive (NIST says to keep hashes apart from the files [18]) in `sha256sum` format: lowercase hash, space, asterisk, relative path with forward slashes, LF line endings, no BOM. Tested on PowerShell 7.5.4 on Linux with spaces, brackets and an accented letter in file names: `sha256sum -c` reported OK for all six files, and an independent `sha256sum` run produced an identical list. It uses only cmdlets and .NET calls present in Windows PowerShell 5.1, but **I did not run it on 5.1**: UNVERIFIED there. To check a folder or a copy later, use `verify_manifest.ps1` in the same folder: `cd` into the folder to check, then `powershell -ExecutionPolicy Bypass -File verify_manifest.ps1 -Manifest D:\LifeJourney\SHA256SUMS.txt`. It prints `MISSING` or `MISMATCH` for each problem and a count. Tested on PowerShell 7.5.4 on Linux: 6 files, 0 problems; then with one file changed by one byte and one file renamed: both caught; then restored: 0 problems. Also not run on 5.1.

```powershell
cd D:\LifeJourney\archive
powershell -ExecutionPolicy Bypass -File mk_manifest.ps1
```

**Two Windows PowerShell 5.1 traps.** (1) `>` and `Out-File` write **UTF-16LE** (Microsoft: "Out-File and the redirection operators > and >> create UTF-16LE") [102]. I confirmed a UTF-16LE hash list is rejected by GNU `sha256sum -c` ("no properly formatted checksum lines found", coreutils 9.4) [RUN]. Use the script, or `Set-Content -Encoding ascii`. (2) PowerShell ends lines with CRLF on Windows. GNU `sha256sum` 9.4 accepted a CRLF list in my test, so that is not a failure here; other checkers (macOS `shasum`, BusyBox) were not tested and may differ (UNVERIFIED). The script writes LF itself to avoid the question. For a spreadsheet-friendly list, `Get-ChildItem -Recurse -File | Get-FileHash | Export-Csv -NoTypeInformation hashes.csv` works (columns Algorithm, Hash, Path; absolute paths) [RUN].

**This closes `playbooks/format.md` Step 4's TODO:** use `Get-FileHash` through `mk_manifest.ps1`; keep the list outside the folder; re-run after every copy to a new drive or disc.

### FQ5. Reading speed and font size for viewers over 70: BBC, Ofcom, DCMP

**Answer: none of the three states a figure for viewers over 70. Ofcom was not readable (HTTP 403), so Ofcom is UNVERIFIED.** What the BBC and DCMP do say:

| Point | BBC Subtitle Guidelines v1.2.5, March 2026 [105] | DCMP Captioning Key [107][108][109] |
|---|---|---|
| Speed | "The recommended subtitle speed is 160-180 words-per-minute (WPM) or 0.33 to 0.375 second per word. However, viewers tend to prefer verbatim subtitles, so the rate may be adjusted to match the pace of the programme." Minimum about 0.3 s per word. Children's section gives no wpm: "seek advice" | Educational media at most 130 wpm (lower level), 140 (middle), 160 (upper); verbatim only for quotations, famous speakers, verse and lyrics. Min caption duration 1 s 10 frames; max 6 s |
| Size | Authoring line height **7% to 8%** of picture height for 16:9; the displayed size may be reduced, "preferred ... between 0.6 and 0.8 times", **x0.67** for 32-42 inch TVs (range x0.5-x1) and x1 for small phones; "the final size should never be larger than the authored size" | No size figure. Text: white, medium weight, sans serif, drop or rim shadow, proportionally spaced; a translucent box preferred on light backgrounds |
| Lines | Two lines maximum for landscape video; about 71% of picture width for the region; 37 characters per line is the Teletext-era rule | No more than two lines preferred; mixed case; break at natural pauses |
| Older viewers | Not mentioned. Its audience note: subtitles are "primarily intended to serve viewers with loss of hearing" but about 10% of broadcast viewers use them regularly and "the majority ... are not hard of hearing" | Not mentioned. Research appendix: Jensema 1998, 578 viewers, "OK speed" about 145 wpm, most had "little trouble ... until the rate was at least 170 wpm", and "Age and sex were not related to caption speed preference"; Thorn and Thorn 1996 concluded captions for hard-of-hearing people "are too small and too quickly presented" and proposed a second, slower, larger style; in 2003, 36% of 203 deaf, hard-of-hearing and ESL respondents said captions moved too fast |

Viewing distance: BBC R&D WHP 287 (2015) found a median UK viewing distance of 2.63 m, 5.5 screen heights, and that people over 55 were under-represented in its sample [106]. That supports the existing 3 m test, and means the sample says little about 70+ viewers.

**What this means (judgement [J]).**
- The BBC's 160-180 wpm is about 16-18 characters per second (assuming 6 characters per word with the space); the 20 characters per second Netflix adult cap quoted earlier in this file [5] is about 200 wpm, faster than either broadcaster's guide. For a room that includes people over 70, aim for **130-145 wpm** (about 0.41-0.46 s per word, 13-14 characters per second), never above 160, and keep each caption on screen at least 1.5 s.
- Author at the **top of the BBC range, line height 8% of picture height, which is `FontSize=23` in the ffmpeg route** (FQ2), and do **not** apply the BBC's x0.67 TV reduction; that reduction assumes a typical viewer. Keep white text with a dark outline or translucent box (DCMP), two lines at most, mixed case.
- Treat these as starting values for the week-9 test (T14): render the same 20 seconds at `FontSize` 20, 23 and 26 (6.9%, 8.0%, 9.0% line height), play from 3 m on the venue screen, and ask a viewer over 70 which they can read without effort. Their answer outranks every table here.
- Not found: any controlled study of caption speed or size for hearing viewers over 70. The DCMP studies are 1990s-2003 work on deaf and hard-of-hearing viewers.

### FQ6. Minecraft Usage Guidelines, dated excerpt

Saved: `research/sources/minecraft-usage-guidelines-2026-10-18.txt` (fetched Sunday 2026-10-18 about 05:16 GMT; HTTP 200, 407,781 bytes; the first attempt failed with an HTTP/2 error, the retry over HTTP/1.1 succeeded; sha256 of the extracted text is in the file). The page shows no revision date; the `Last-Modified` header (Fri 2026-10-16 17:56:11 GMT) is a server file stamp and not a policy date. It supersedes the "not fetched" note on [50]; see [92]. The `games` track saved its own excerpt earlier the same day (`research/excerpts/games-round1-followup-2026-10-18.txt`), and the quotes agree.

Key points for this track, quoted in the file:
- **Personal use:** "We are very relaxed about things you create for yourself." But "When you decide to share your content with the community (whether you plan to make money off it or not), you are doing what we consider to be a commercial thing." Whether showing a film to relatives is "sharing with the community" is not defined on the page: UNVERIFIED, and not legal advice.
- **Physical locations** (one condition on making money from footage): "The gameplay is not displayed or projected publicly within physical locations", with two examples, both commercial venues (a restaurant promoting big-screen gameplay; a theatre charging for gameplay on movie screens). A private family showing is not an example, but "publicly" and "venue" are undefined.
- **In-person events:** "no more than approximately 150 participants"; "You may not accept sponsorships for purposes of profit".
- **Change clause:** "We reserve the right to change our mind at any time." Re-save the excerpt in the week before the event.
- Do not use "Minecraft" as the primary name or title of the film or world.

### FQ7. Recordable Blu-ray in 2026: media, burners, and a verified burn from the command line

**What NIST actually says [18], re-read from the PDF.** Table 1, row "CD-R and DVD-R / Blu-ray": longevity "<30 years", "Acceptable for archival use", notes "30 years is a conservative minimum longevity. There are reputable claims of 50 or 100 years. Gold disks last longer than silver. CDs last longer than DVDs. Blanks should be used within 5 years." The media cell reads "CD-R and DVD-R Blu-ray"; it never writes "BD-R", so reading it as recordable Blu-ray is an inference. M-DISC (DVD and Blu-ray) is "At least 100 years", and "requires M-DISC writer".

**Availability in 2026 (manufacturer pages, fetched 2026-10-18) [110].** Verbatim America lists: BD-R 25 GB 16X in a 50-pack spindle (silver, printable); BD-R DL 50 GB; BDXL 100 GB; **M DISC BD-R 25 GB 4X "Limited Archival", 10-pack** ("Projected lifetime of several hundred years (based on ISO/IEC 16963 testing)", a vendor claim; earlier in this file [21] notes the original M-DISC BD-R was discontinued and reformulated in 2022); and an **"Ultra HD 4K Blu-ray Writer - USB-C"** that "stores up to 100GB on a BDXL Disc", is "Fully compliant with MDISC archiving technology", bundles Nero Burn and Archive for PC, and lists Windows 7/8/10/11. So media and a Windows-compatible writer are on a manufacturer's current catalogue.
- **Consumer prices: UNVERIFIED.** B&H and Newegg returned 403; Verbatim's pages show no prices; the Verbatim Amazon storefront page returned no BD-R prices. Check a retailer by hand before budgeting.
- **Gold-layer BD-R: I found none.** NIST's "gold lasts longer than silver" sentence is in the CD-R/DVD-R row; whether any current BD-R uses a gold layer is UNVERIFIED. For Blu-ray the realistic choices are standard BD-R from a major maker, or M-DISC BD-R.
- **Supply risk, UNVERIFIED recollection:** I recall that Sony announced in early 2025 that it would stop making recordable Blu-ray media. I could not check it (no search). It is a reason to buy blanks early, but NIST says blanks should be used within 5 years, so buy in January 2027 and burn in February, not in November.

**Can a verified disc be made from the command line?**
- **In the cloud (tested [RUN]):** build the disc image and prove it. `xorriso -as mkisofs -iso-level 3 -J -R -V LJ_ARCHIVE -o archive.iso archive/` (xorriso 1.5.6, installed from apt) produced a 927-sector image holding the six test files; `xorriso -osirrox on -indev archive.iso -extract / out/` followed by `sha256sum -c SHA256SUMS.txt` gave OK for every file, including the bracketed and accented file name; `xorriso -indev archive.iso -check_media` reported "Media region ... + good". xorriso creates ISO 9660 with Rock Ridge and Joliet; I did not test UDF, the filesystem data Blu-rays usually carry [J]; whether a UDF image is needed for files over 4 GB or for a particular player is UNVERIFIED (so test the real disc in the real player).
- **On the maker's PC (not tested; there is no drive here):** the burn itself is the one step I cannot prove. Options: Windows' own disc-image burner (`isoburn.exe`); command-line switches UNVERIFIED (the ss64 page I tried returned 404); the IMAPI v2 API that Windows ships, in which `IDiscFormat2Data` is "Use this interface to write a data stream to a disc" [111], scriptable from PowerShell and **UNVERIFIED as a working recipe**; ImgBurn, a free Windows burner whose homepage lists a Verify feature and shows "Current version: 2.5.8.0 Released: 16th June 2013" [112], so old, with command-line switches UNVERIFIED; or the Nero software bundled with the Verbatim writer [110]. On Linux, `xorriso -as cdrecord -v dev=/dev/sr0 -eject archive.iso` is the usual command (general knowledge, UNVERIFIED here).
- **Verification does not depend on the burner.** After burning, read the finished disc back and compare to the manifest: in PowerShell, `cd E:\` (the disc) and run `verify_manifest.ps1 -Manifest D:\LifeJourney\SHA256SUMS.txt`; it must report 0 problems. The disc must hold the archive folder's contents at its root so the relative paths match. That is the same check I ran on the extracted ISO (with `sha256sum -c`).
- The `toolchain` track has no disc-burning recipe; this section is it. **Recommendation [J]:** treat a BD-R as one of the three archive copies (NIST supports it); do a rehearsal burn of a small folder to a cheap BD-R in December to settle the tool and the read-back check; make the real disc in February from the final `archive.iso`.

### Corrections to carry into earlier text (for the scribe)

1. **Cloudflare (Summary 8, Q5 table, T9, Tools row, playbook Decision 8, SKILL.md):** the 50-user limit is confirmed on [28]'s comparison table (Core capabilities > Usage); the "No user limit" rows are the paid columns, and the second group's Free cell is blank. Remove the "page contradicts itself" caveat from the review's nudge 3, keep "one page only, what counts as a user is UNVERIFIED", and add "a card is needed at onboarding even on Free" [91].
2. **Source [50]:** fetched successfully today; cite [92] and the saved excerpt instead of "not fetched".
3. **Tools table, ffmpeg row, and Resolve row (review critical issue C2):** add the agent-generable route from FQ2 (timeline.json + ffmpeg, OTIO as the exchange file, FilmCraft CLI as a second renderer) and score "agent-generable and cloud-renderable" using it.
4. **Open question 4 (caption speed) and Summary 11:** replace "no source" with FQ5; keep the 70+ recommendation tagged [J].
5. **T4 (caption trio) and T14:** give caption size as line height (8% of picture height) and as the ffmpeg value (`FontSize=23` at default libass scale), not just points or pixels.
6. **Playbook Step 4 TODO(research):** closed by FQ4. **Step 7 and F-0:** add the FQ1 threshold and the six-question ask.
7. **Archive plan (T4, storage):** add the BD-R copy and its read-back check (FQ7) with the buy-late timing.

### Still UNVERIFIED after this round

- Everything in FQ1 about her actual recordings.
- Ofcom guidance or research on subtitle speed and size.
- Retail prices for BD-R media and burners; any gold-layer BD-R; the Sony recollection.
- A working command-line burn on Windows, and UDF requirements.
- `mk_manifest.ps1` and the PowerShell one-liner on Windows PowerShell 5.1; certutil output format.
- Opening the generated `.otio`, EDL, FCPXML or Kdenlive files in Resolve or Kdenlive; Ken Burns through FilmCraft's OTIO import; ffmpeg graphs beyond 30 shots.
- What "user" means for Cloudflare's 50 limit.

### Sources added in round 1

Tags as above; fetched 2026-10-18 unless stated.

[90] Cloudflare — Zero Trust plans page — https://www.cloudflare.com/plans/zero-trust-services/ — [P][V] HTTP 200, 412,979 bytes; no plan table in the served HTML.
[91] Cloudflare Docs — Set up Cloudflare Zero Trust — https://developers.cloudflare.com/cloudflare-one/setup/ — dateModified 2026-10-12 — [P] Free plan still needs payment details.
[92] Mojang/Microsoft — Minecraft Usage Guidelines (dated excerpt) — https://www.minecraft.net/en-us/usage-guidelines — [P] HTTP 200 over HTTP/1.1 at about 05:16 GMT; excerpt in `research/sources/minecraft-usage-guidelines-2026-10-18.txt`.
[93] Library of Congress — Care, Handling, and Storage of Audio Visual Materials — https://www.loc.gov/preservation/care/record.html — undated — [P].
[94] Wikipedia — Opus (audio format) — https://en.wikipedia.org/wiki/Opus_(audio_format) — [T] WhatsApp since 2016, 8-16 kHz.
[95] PyPI — OpenTimelineIO adapter packages — https://pypi.org/pypi/otio-kdenlive-adapter/json ; https://pypi.org/pypi/otio-mlt-adapter/json ; https://pypi.org/pypi/otio-cmx3600-adapter/json — [P] names, versions, homepages; installed and run [RUN]. OpenTimelineIO 0.18.1 from `pip`.
[96] FilmCraft README at v0.8.0 — https://raw.githubusercontent.com/storytold/filmcraft/v0.8.0/README.md — [P] CLI, captions, interchange.
[97] FilmCraft docs/project-files.md at v0.8.0 — https://raw.githubusercontent.com/storytold/filmcraft/v0.8.0/docs/project-files.md — [P] `.fcproj` is UTF-8 JSON; its history table stops at 13.
[98] FilmCraft docs/captions.md at v0.8.0 — https://raw.githubusercontent.com/storytold/filmcraft/v0.8.0/docs/captions.md — [P] SRT import/export, `burnCaptions`.
[99] FilmCraft Linux CLI release asset — https://github.com/storytold/filmcraft/releases/download/v0.8.0/filmcraft-0.8.0-linux-x86_64.tar.gz — [P][RUN] SHA-256 `b166877905ae8a1b5505066d6dde60d7ce05831cfb309bacd5d7970f4bb017e1`, equal to `craft-motion.md` [40]; run as `filmcraft-cli 0.8.0`.
[100] Microsoft Learn — Get-FileHash (Windows PowerShell 5.1) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-5.1 — updated 2025-03-24 — [P].
[101] Microsoft Learn — certutil — https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil — updated 2025-10-22 — [P] `certutil -hashfile InFile [HashAlgorithm]`.
[102] Microsoft Learn — about_Character_Encoding (5.1) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1 — updated 2025-09-29 — [P] `>` and Out-File write UTF-16LE.
[103] SS64 — CertUtil — https://ss64.com/nt/certutil.html — [S] example `CertUtil -hashfile c:\demo\anything.txt SHA256`.
[104] PowerShell 7.5.4 for Linux x64 — https://github.com/PowerShell/PowerShell/releases/download/v7.5.4/powershell-7.5.4-linux-x64.tar.gz — [RUN] used to run `Get-FileHash` and the manifest script.
[105] BBC — Subtitle Guidelines, version 1.2.5, March 2026 — https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles — [P] fetched from the container (HTTP 200); speed, size, lines.
[106] BBC R&D — WHP 287, A Survey of UK Television Viewing Conditions (January 2015) — https://downloads.bbc.co.uk/rd/pubs/whp/whp-pdf-files/WHP287.pdf — [P] median 2.63 m, 5.5 H; ages 18-55 over-represented.
[107] DCMP — Captioning Key, Presentation Rate — https://dcmp.org/learn/601-captioning-key---presentation-rate — [P] 130/140/160 wpm.
[108] DCMP — Captioning Key, Text — https://dcmp.org/learn/597-captioning-key---text — [P] font, lines, duration, placement.
[109] DCMP — Captioning Presentation Rate Research (PDF) — https://dcmp.org/images/learning_center/captioning-key/documents/captioning_presentation_research.pdf — [P] Jensema 1998, Thorn and Thorn 1996, 2003 survey.
[110] Verbatim America — Blu-ray, M Disc and External Optical Drives pages — https://www.verbatim.com/en/blu-ray ; https://www.verbatim.com/en/blu-ray/products/98485-bd-r-25gb-16x-shiny-silver-silk-screen-printable-hub-printable-50pk-spindle ; https://www.verbatim.com/en/m-disc/products/43825-m-disc-bd-r-25gb-4x-limited-archival-10pk ; https://www.verbatim.com/en/external-optical-drives/products/43888-ultra-hd-4k-blu-ray-writer-usb-c — [P] catalogue entries; no prices shown.
[111] Microsoft Learn — IDiscFormat2Data interface (imapi2.h) — https://learn.microsoft.com/en-us/windows/win32/api/imapi2/nn-imapi2-idiscformat2data — updated 2024-02-22 — [P].
[112] ImgBurn — home page — https://www.imgburn.com/ — [P] "Current version: 2.5.8.0 Released: 16th June 2013".
[113] Sibling notes — `research/craft-motion.md` (FilmCraft Q2, Q3, Q7, R8), `research/story.md` (Q4 found voice), `research/surprise-ops.md` (voice-letter formats, tape transfer labs [44][45]), `research/toolchain.md` (ffmpeg, MLT, Blender runs) — read 2026-10-18.


## Follow-up research (round 2)

Researcher: Sonnet, Sunday 2026-10-18, in answer to the five research follow-ups in `reviews/format-round2.md`. Run in the cloud container (Linux), not on the maker's Windows PC. Every web page was treated as data. New sources continue the numbering at [114]. Tags as above; **[RUN]** means I ran it in the container on 2026-10-18; **[L]** means a sibling note I read this session and did not re-fetch.

**Constraints on this round.**
- The shared web-search budget was used up again (three WebSearch calls were refused). I used no search engine, archive or reader proxy. Every page below is a direct fetch of a URL I already knew, found in the site's own sitemap, or saw linked on a page I had read.
- Not readable by me: ASCAP and BMI (HTTP 403, including a Cloudflare challenge), OneMusic's home page, AMC, Regal, Vue, Odeon, Cineworld and Curzon (HTTP 403); PRS for Music's licence pages (they load, but the text is drawn by script, so I got nothing); Picturehouse's hire page (script-only); the DCI site (the specification links I guessed returned 404). Nothing is claimed below about what those sites say.
- Dated excerpts of the key legal and licensing passages are saved in `research/sources/format-round2/clearance-and-venue-excerpts-2026-10-18.txt` (E1 to E12). The page can change; re-save before relying on it.
- I am not a lawyer and nothing here is legal advice. Three of the five answers cannot be finished without a fact only the maker holds (country and venue; the venue's AV; the family's accounts).

### Answers in brief

1. **Music at the venue (RQ1).** A venue's licence never replaces per-work clearance. Putting a pre-existing recording in the film always needs a sync licence from the publisher and a master licence from the label, for every copy that carries it [119][121]. What a venue (or the organiser) can hold is the separate public-performance layer, and whether it reaches a film soundtrack differs by country: United States, cinemas rely on the producer clearing performance "at the source" and PROs license bars, restaurants, hotels and live venues by blanket licence [119][120]; Australia, the event organiser needs a OneMusic Film Screenings licence "regardless of whether there's an entry fee" [121]; UK, a charity's community-cinema guide says the venue's PRS/PPL licence covers the music in a film [125]; Canada, SOCAN's cinema tariff covers "any establishment exhibiting motion pictures" [123]. Whether the maker's likely venue holds such a licence is not knowable from the web. **The jurisdiction and the venue type are needed** (RQ1 lists the one-sentence written question). The safest design is to avoid pre-existing commercial recordings in the premiere cut, which makes the venue question mostly moot.
2. **Venue projection chain (RQ2).** Not answerable without the venue. What the research settles is the decision rule: a DCP is the venue master only if the venue says it ingests DCPs; for a hall, library, club or restaurant (projector or TV plus a laptop or player) the 1080p24 H.264 file is the venue master and the DCP is not needed. Caption-safe: no source I could read defines a different safe area for projectors; the TV rule (EBU R 95) is 5% for graphics, which is 96 px at the sides and 54 px top and bottom at 1080p, and a venue screen can also shrink the picture (a 16:9 picture on a 4:3 screen is 75% of the screen height, computed). Keep text inside the 5% box and judge size on the real screen from the back row.
3. **Hours per finished minute (RQ3).** The measured number does not exist until the slice is done (G-SLICE, Sunday 2026-12-20). What I can give now is the exact measure, tested: **maker-minutes logged for the slice chapter divided by its finished seconds equals hours per finished minute** (units cancel; 913 minutes over 100 seconds is 9.13 h/min in my test). Cross-track finding: the 6-10 h figure in this file is a **build-only** figure; on `production-scale`'s model the all-in cost of a 12-minute film is 9.7 to 23.7 h per finished minute (Best to Base), so nudges 3 and 4 must not carry 6-10 as an all-in rate.
4. **Shared drive or cloud library (RQ4).** A maker-only fact; the web cannot answer it. I give the five questions the maker answers alone, from their own accounts, and what each answer changes. Until answered, assume yes (the subject can reach it).
5. **Cloudflare "user" (RQ5).** Neither of the two readings. Cloudflare's seat-management page says a user consumes **one seat when they perform an authentication event**, holds it **until you remove the user** (no monthly reset unless you turn on seat expiration), and once the seats are used up, **additional users who try to log in are blocked** [114]. The Free plan's 50 comes from the product page [28]; the seat page does not mention the Free plan, so reading "50 users" as "50 seats" is my inference. With 10-40 relatives it fits, provided test logins are removed.

### RQ1. Public-performance music clearance at the venue

**What the maker must tell us first (charter open decision).** The country of the premiere; the venue type (a commercial cinema hired for the night, a hall, club, restaurant or hotel room, or a church, library or school room); whether anyone pays to get in (the charter says non-ticketed); and who is legally the organiser (probably the maker).

**The layers are different rights, not alternatives.**

| Layer | What it permits | Who grants it and how | Needed for which copies |
|---|---|---|---|
| 1 Sync (the composition) | Putting the song in the film | The publisher, per work, by negotiation in the free market. The Copyright Office says the creator of a film "must obtain synchronization licenses from both the owner of the musical work and the owner of the sound recording"; sync is "an aspect of music owners' reproduction and/or derivative work rights" [119 pp.55-56] | Every copy that contains the song: the venue file, the DCP, the access copy, a private-link copy, the archive |
| 2 Master (the recording) | Using that recording in the film | The label or recording owner, per recording [119 p.55][121] | Same |
| 3 Public performance of the composition | Letting the room hear it | A PRO blanket licence held by the venue or organiser, or a "source licence" negotiated together with sync [119 pp.33-34] | The premiere and any other public showing |
| 4 Public performance of the recording | A separate right in some countries | Australia: PPCA, bundled in the OneMusic fee [121]. US: none beyond digital audio transmission [117], and "the sounds accompanying a motion picture" are excluded from "sound recordings" [116]. UK: playing a film's soundtrack to accompany the film is not "playing a sound recording" [124] (my reading) | Depends on the country |

The ASCAP point stands: ASCAP "may not license mechanical or synchronization rights" and, in practice, BMI does not either [119 p.37]. A venue's blanket licence therefore cannot stand in for layers 1 and 2.

**By jurisdiction (what I could read).**

| Country | Who clears the music's public performance in a film | Does the venue's general licence reach a film soundtrack? | Evidence |
|---|---|---|---|
| United States | Cinemas: the producer, "at the source", because "the PROs are prohibited from licensing public performance rights directly to movie theater owners"; "source licenses do not typically encompass non-theatrical performances, such as on television" [119 p.34]. An exhibitor's own words: a theatre takes "a single license from a movie's distributor" and the exemption sits in the ASCAP decree, Sections IV(E) and (G) [120] | **UNVERIFIED.** The 2015 report says "bars, restaurants, live performance venues, and commercial establishments that play background music" can take PRO licences, and "large commercial establishments such as bars, restaurants, concert venues, stores, and hotels often enter into blanket licenses" [119 p.33]; it does not say a blanket licence covers a film soundtrack. ASCAP and BMI were unreadable to me | [119] Copyright Office, 2015: [P], 11 years old; whether the decrees still stand in 2026 is UNVERIFIED. [120] is an exhibitor's view: [S] |
| United Kingdom | Not established from a primary source | A community-cinema guide by the charity Cinema For All says the venue's "PRS (Performing Rights Society) music licence - also known as a PPL" "covers the copyright of any music used in your chosen film, plus any additional music you want to play" and that the venue gets it from "PRS Music or PPL" [125]. PRS and PPL are separate bodies, so the guide is loose; PRS's own pages were unreadable [126] | [125] [S] practice guidance; [124] statute: [P] |
| Canada | SOCAN's Tariff 6 covers "the operations of a motion picture theatre or any establishment exhibiting motion pictures", $1.50 a seat per screen a year, $150 minimum per screen (the 2014-2016 version, published 2017); it "does not authorize any concert or other performance of music" where films are not integral [123] | **UNVERIFIED** for a one-off hall screening. SOCAN's licence list names other tariffs (Receptions, Conventions, Assemblies and Fashion Shows (8); recreational facilities run by municipalities, schools and similar bodies (21)) but the page does not say whether they reach a film [122] | [P] but old; the current tariff year is UNVERIFIED |
| Australia | The event organiser: "you typically need permission to publicly play the music that features in the films ... regardless of whether there's an entry fee". The OneMusic Film Screenings licence bundles APRA and PPCA; APRA works 0.462% of gross box office with a minimum of $86.52 (also the minimum for a free screening); PPCA sound recordings $207.72 per screen for 1-7 screenings; all include GST, for 1 July 2026 to 30 June 2027. For a free screening the pre- and post-screening forms can be completed together before the event [121] | Not addressed for a venue's own general licence. The guide puts the requirement on the event organiser for a "one-off film screening", and says "regular or re-occurring film screenings at permanent cinemas" fall under OneMusic Cinemas instead [121]. One screening on one screen, if both bodies' repertoire is in the film, comes to $294.24 (computed) | [121] [P], July 2026 |
| Other (India, EU, Switzerland and so on) | Not researched. The sibling notes read SUISA (Switzerland) [L] | UNVERIFIED | |

**The US non-profit exemption (17 U.S.C. 110(4)) is a trap to avoid relying on.** It exempts a performance of "a nondramatic literary or musical work" only if it is not a transmission to the public, has no commercial advantage, pays nothing "to any of its performers, promoters, or organizers", and has "no direct or indirect admission charge" (or the proceeds go "exclusively" to educational, religious or charitable purposes) [118]. The statute names literary and musical works; it does not name motion pictures or audiovisual works, which section 106(4) lists as a separate performance right [117]. Whether playing a song inside a film falls within 110(4) is a legal question I cannot settle, so UNVERIFIED. The gathering is "public" in the statute's sense anyway: a place "open to the public", or one where "a substantial number of persons outside of a normal circle of a family and its social acquaintances is gathered" [116].

**Does the likely venue hold one?** Not knowable from the web. The only evidence is general: US bars, restaurants, concert venues, stores and hotels "often" hold PRO blanket licences [119 p.33]; the UK guide treats it as something the venue obtains and tells organisers to ask [125]; Australian rules put the film licence on the organiser, not the venue [121]. No source covers church halls, libraries, schools or community centres. Treat every venue as "unknown until it answers in writing".

**Which copies must be cleared (the answer the format track needs).**
- Every file that contains a pre-existing recording needs layers 1 and 2 cleared for that use: the venue file, the DCP, the 1080p access copy, any private-link copy (YouTube may block or mute it [J]), the archive masters and any companion. A sync licence is a reproduction right [119 p.56], so each copy is a reproduction, and the licence's media, territory and term must cover all of them. The `music-sound` track owns the licence recipe; sibling notes say a festival-only licence "doesn't carry over" to online use [L].
- Layer 3 matters only for the public showing(s). For a US commercial cinema, ask the licensor to include US public performance in the sync licence (the "source licence" pattern the producers use [119 p.34]). For a hall, the venue's licence or the organiser's own licence applies, by country as above.
- Cheapest way to shrink the problem: use commissioned or library music whose licence names public exhibition and online use, or public-domain compositions with public-domain or newly made recordings (`music-sound` Q5 [L]). Then layers 1 and 2 are one signed grant and the venue's licence matters only for performance royalties.

**Written question for the venue (no need to name the subject).** "We are showing a short film at a public gathering on Saturday 27 February 2027 and the film contains music. Which music-licensing bodies do you hold licences with, do those licences cover music inside a film or video we bring, and if not, who is responsible for the licence on the night?"

**Still UNVERIFIED for RQ1.** Whether any PRO's blanket licence covers a film soundtrack in a non-cinema venue (US, UK, Canada); PRS's and PPL's own wording; the current SOCAN tariff and any one-off event tariff; Canada's Re:Sound position; India, the EU and Switzerland beyond what sibling notes read; whether the US consent decrees remain in force; whether 110(4) can apply to music inside a film.

### RQ2. Venue projection chain: DCP, HDMI feed, or the venue's own player

**What is established.**
- **DCP frame rates.** "The only rates that are guaranteed to work on all DCI projectors are 24 frames per second (fps) for video and 48kHz for audio"; 25, 30, 48, 50 and 60 fps are listed under "Other often-supported rates", not guaranteed [127]. DCP-o-matic's advice for a DCP going to an unknown place is to use 24 and 48 kHz [127]. A 25 fps source is played slow with the audio resampled to stay in sync [127].
- **DCP picture and sound.** Use 2K unless the content is high enough to be worth 4K; the Container sets the picture ratio and pads with black; the channel count must be even ("required by the DCI standard") and unused channels are silence; if in doubt choose the SMPTE standard [127]. The sibling's Finding 1 (2K Flat 1998x1080, 24 fps, stereo L/R in a six-channel container) stands [L].
- **Subtitles in a DCP.** DCP-o-matic lists three routes and says burnt-in subtitles are "less likely to go wrong, especially if you are using unusual subtitle positioning or character sets", while projector-rendered subtitles "mostly works well but is not 100% reliable" [127]. This is a DCP matter; an HDMI file always carries its burned-in captions.

**What venues offer (evidence is thin; two examples).**
- A UK cinema chain's private-hire page says hirers can "pick the content: the latest release, a firm favourite or your own content", that corporate hirers can "plug your laptop into our big screens", and that the booking choices include "screen your own or deliver a presentation", with "tech requirements - we'll talk you through it all" [130]. So a commercial cinema screen can take a laptop on HDMI; the page does not say which file formats, frame rates or audio the HDMI path accepts, and does not mention DCPs. Everything else about the cinema path is a question for the venue.
- A UK charity's starter pack for community cinemas lists the chain as a **screen, a projector, a player ("a Blu-ray, DVD player or laptop"), a PA system, and accessibility equipment such as a hearing loop or subtitles**, and advises testing a disc in the venue beforehand [125]. That is the HDMI-or-player chain, with no DCP.

**Decision rule (my synthesis [J] from [125][127][130] and the sibling notes).**

| What the venue says | Venue master | Fallback | Notes |
|---|---|---|---|
| "We ingest DCPs" (a cinema server) | 2K Flat 24p SMPTE DCP, unencrypted, burned-in captions | 1080p24 H.264 on the venue's HDMI or the maker's laptop | A DCP costs encode time (sibling measured 3 to 12 wall minutes per finished minute [L]) and a test at the cinema; do not make one without a test slot |
| "HDMI from a laptop" (hall, club, library, restaurant, a cinema's alternative-content input) | **1080p24 (or the projector's native rate) H.264 file played from the maker's laptop** | A second file on a USB stick, plus the DCP only if the venue later asks | This is the common case for non-cinema venues; 1080p H.264 is the venue master, not a fallback |
| "Our own player or TV with USB" | H.264 High profile, 1080p24, AAC stereo, `+faststart` (sibling Finding 1 row 2 [L]) | The weaker-decoder backup file (row 3 [L]) | Test the exact stick on the exact player |
| Unknown | Carry both; rehearse the H.264 path on the venue's real HDMI input | DCP only when the venue says yes | The decision belongs to the venue's answer, due before the settings lock (see below) |

**Resolution, frame rate and audio layout: what to ask.** Native resolution and aspect ratio of the projector or LED wall (1920x1080, 1920x1200 or 4:3); which refresh rates the HDMI input accepts (24p or only 50/60 Hz); stereo or mono PA, and who sets the fader; whether there is a hearing loop (the Cinema For All list includes one [125]); who operates the AV; a 20-minute test slot the week before. The mono-fold and loudness checks stay as in the sibling Findings 3 and 5 [L].

**Is the caption-safe area different from a TV's?** No source I could read defines a projector or cinema safe area. What I verified:
- EBU R 95 (version 1.1, June 2017) for 16:9 television: "The action safe area is 3.5% and the graphics safe area is 5%, at the top, bottom and lateral parts of the image" [128]. At 1920x1080, 5% is 96 px on each side and 54 lines top and bottom, so a graphics-safe box of 1728x972 (computed). Action safe at 3.5% is 67 px and 38 lines (computed; R 95 itself corrects 3.5% of 1920 to 67 px).
- A flat-panel TV driven over HDMI "can safely assume that all pixels are visible" (uncited sentence on Wikipedia), but "many LCD TVs still come with overscan enabled by default, but it can be disabled by the user" (cited there to Engadget and CNET) [129]. The article does not mention projectors.
- A venue screen can shrink the picture: a 16:9 image on a 4:3 screen fills 75% of the screen height and on a 16:10 screen 90% (computed: 0.5625 / 0.75 and 0.5625 / 0.625), so caption text gets smaller in absolute size.
- A DCP is shown edge to edge in its container, and the cinema's masking can crop the edges (sibling inference [L]; no source).
- **Plan:** one rule for all venues, which is the union of the cases above: keep all text inside the 5% graphics-safe box; set caption size from the sibling's rule (line height 7-8% of picture height, `FontSize=23` at 1080p [L]) and then judge it on the real screen from the back row, with the oldest listener beside you. The TV test at 3 metres is the fallback test only.

**When the venue question must be answered.** The frame rate, aspect ratio and master spec feed the production settings card. The sibling's TD-1 lock is Sunday 2026-11-01 and G-READY is Sunday 2026-11-15 [L]; nudge 1(d) of the round-2 review puts the venue master decision at G13 (now Sunday 2027-01-17). Ask the venue **before 2026-11-15**: if the answer arrives late the defaults (1920x1080, 24 fps, 16:9, stereo, H.264 venue file with a DCP contingency) still hold, and changing them later is the costly case.

**Questions for the venue** (written so the surprise survives; the maker books and asks, not a relative). "We are hiring the room on Saturday 27 February 2027 for a gathering of about [N] people and will play a short film from a laptop or a file. Can you connect a laptop by HDMI, and what are the projector's or screen's native resolution and aspect ratio? Which frame rates does it accept (24p?), is the sound stereo or summed to mono, who operates the equipment, is there a hearing loop, and can we do a 20-minute test the week before? Do you play DCP files?" Add the RQ1 licensing question.

**Still UNVERIFIED for RQ2.** What any real venue accepts; whether projectors commonly apply overscan (no manufacturer manual read); how a cinema's masking affects subtitles; the HDMI frame rates a given cinema's alternative-content input accepts; the DCI specification itself (its site did not serve it to me).

### RQ3. Hours per finished minute for the chosen look

**Answer.** Not available until the slice exists. The charter-phase task is to define the measure, make it computable by an agent from `hours.csv`, and say what to do with it. The look is not yet chosen (style frames are due at G-READY, 2026-11-15), and the rate is specific to a look: if the look changes after G-SLICE, the slice must be redone for the new look.

**The measure.**
- **Formula.** Hours per finished minute = maker-minutes logged ÷ finished seconds. (Hours = minutes ÷ 60 and minutes of film = seconds ÷ 60, so the 60s cancel.)
- **Numerator.** The `minutes` column of `hours.csv` (schema `date, shot_or_chapter, activity, minutes, who, note`, from `production-scale` T6 [L]) for the slice chapter's shot rows and its chapter row, covering the activities from the approved brief to the approved chapter, including sound, grade, mix, captions and master. Leave out `gather`, `scan`, `story` and `admin`: the model counts those as separate adders. Report `learn` and `rework` rows as their own subtotals as well, so the learning share of the first chapter can be read off; `production-scale` defines `h_slice` as all hours from approved brief to approved chapter [L], so use the all-rows total for the model input and the ex-`learn` total as a second figure.
- **Denominator.** The finished duration of the approved chapter master, not the target: `ffprobe -v error -show_entries format=duration -of csv=p=0 chapter.mp4` (a 100 s synthetic clip gave `100.000000`; the frame check `-count_frames -show_entries stream=nb_read_frames,r_frame_rate` gave `2400` frames at `24/1`) [RUN].
- **One-liner (tested on Linux with synthetic rows) [RUN]:**

```
S=$(ffprobe -v error -show_entries format=duration -of csv=p=0 chapter.mp4)
awk -F, -v ch=C01 -v s="$S" 'NR>1 && index($2,ch) && $3!~/^(gather|scan|story|admin)$/ {m+=$4} END {printf "%.2f h per finished minute\n", m/s}' hours.csv
```

  On a synthetic file (913 in-scope minutes, 100 s) it printed `9.13`; excluding 180 `learn` minutes gave 7.33 (computed). The PowerShell form for the maker's PC, **untested** (no PowerShell in the container; Windows PowerShell 5.1 behaviour UNVERIFIED): `$s=[double](ffprobe -v error -show_entries format=duration -of csv=p=0 chapter.mp4); (Import-Csv hours.csv | Where-Object { $_.shot_or_chapter -like '*C01*' -and $_.activity -notin 'gather','scan','story','admin' } | Measure-Object minutes -Sum).Sum / $s`.
- **Per shot class.** Also report the rate per class (A templated photo move, B designed graphic, C hero shot, D title), because class C is 10% of shots and 59% of shot-minutes in the Base case [L]; the full film's mix will differ from the slice's.

**What the number is compared with (`production-scale`, read this session [L]).** Its model predicts `h_slice` for a 100-second first chapter of 9.9 (Prior), 26.5 (Base) and 54 (Stress) hours, i.e. **5.9, 15.9 and 32.4 h per finished minute** for chapter 1 (computed ×0.6). It includes a first-chapter learning multiplier L1 of 2.0, 2.5 and 3.2, so chapter 1 is the most expensive chapter; steady-state maker hours per finished minute are 2.98, 6.36 and 10.15 for shots, chapter pass and sound only [L].

**Cross-track finding for nudges 3 and 4.** The "6-10 h per finished minute [J]" in this file's Q3 table is the **build** line of row (a), 60-100 h for 8-12 minutes, with learning (10-15 h) and polish, captions and rehearsal (25-35 h) added separately to reach 100-150 h. It is not an all-in rate. On `production-scale`'s model [L], a 12-minute film costs:

| Case | Build-side hours (shots with learning and rework, chapter passes, sound) | All-in hours | All-in h per finished minute | Like-for-like with this file's 100-150 h (all-in minus story and gathering, computed) |
|---|---|---|---|---|
| Best | not given | 116 | 9.7 | about 103 |
| Prior | not given | 141 | 11.8 | about 128 |
| Base + levers | not given | 201 | 16.8 | about 175 |
| Base | 125-126 (about 10.4-10.5 h/min) | 284 | 23.7 | about 258 |

The 25-minute row is 6.9 / 8.8 / 12.2 / 18.2 h per finished minute (Best / Prior / Base + levers / Base) and the 45-minute row 5.8 / 7.6 / 10.3 / 15.9 [L, computed], because fixed costs (learning, reuse build, rehearsals, fixed finishing, 84 h at Base) spread over more minutes. So: the build-only 6-10 h band agrees with `production-scale`'s Base production-side figure at its top end, but the **all-in** cost of the 8-12 minute film in this file's budget (100-150 h) matches only the Prior and Best cases, not Base. This does not change the format decision (the film is still the cheapest format), but it does change the restated nudge 3 and 4 arithmetic: at 10 h/week (160 production hours by nudge 3; `production-scale` counts about 145 usable), 12 minutes fits on Prior or Best numbers and not on Base; `production-scale`'s own advice at 10 h/week is to plan 8 minutes [L].

**Suggested replacement text for nudges 3 and 4** (keeps the owner of the number as `production-scale`): "Hours per finished minute is a measured quantity: slice maker-minutes divided by finished seconds, recorded at G-SLICE on Sunday 2026-12-20. Until then carry `production-scale`'s range (12 minutes all-in: 116 to 284 h, 9.7 to 23.7 h per finished minute) and the format default of 4-8 chapters; take the final runtime from `production-scale`'s slice table, not from a per-minute rate."

**How to use the slice figure (steps).**
1. At G-SLICE compute the rate with the one-liner; record `h_slice` (all rows), the ex-`learn` figure, and the per-class rates.
2. Look up `h_slice` at the maker's weekly hours H in `production-scale`'s slice table (it lists the largest `h_slice` that fits each runtime, e.g. 12 minutes fits at 20 h/week up to 21 h without levers and 47 h with them [L]); do not divide by L1 yourself, because one chapter cannot reveal the learning curve and the table already contains it.
3. Re-measure on the second chapter and again at G-MID (Sunday 2027-01-17). The learning curve is a fitted pattern, not a law: Wright's 1936 aircraft figure was a 20% fall in labour time per doubling of output, other industries ranged "from only a couple of percent up to 30%", and the article stresses the exponent "does not exactly predict" any future unit [131]. Use it to forecast a range, and let the second chapter confirm it.
4. Expect the slice to run over: students asked about their own theses predicted 33.9 days and took 55.5, and only about 30% finished in the time they predicted; the remedy is to forecast from actual outcomes of similar work, not from the felt estimate [132]. Here the "similar work" is our own earlier chapters.

**Still UNVERIFIED for RQ3.** Any measured number for this film; the PowerShell one-liner on Windows PowerShell 5.1; any published hours-per-minute for photo-forward documentary animation at a theatrical bar (the `production-scale` track found none [L], and I found none in what I could fetch).

### RQ4. Is the family's shared drive or cloud photo library accessible to the subject?

**Answer: UNVERIFIED, and not answerable from the web. It is a fact about the family's accounts, asked of the maker only** (not of relatives, and never of the subject; any question that reveals the project is itself the leak). The round-2 review's nudge 5 already says the safe default: never use a shared family cloud library for any project copy, including archive and test copies, until after the reveal.

**The five questions for the maker, answered alone from the maker's own accounts and memory.**
1. Which family-shared places exist: iCloud Shared Photo Library, iCloud Shared Albums, Google Photos partner sharing or shared albums, Google Drive, Dropbox, OneDrive or Amazon Photos family folders, a family group chat that stores media?
2. Is the subject a member of any of them (her own login, or a login on a shared device)?
3. Does she look at them (notifications on, "memories" or auto-backup on), or is she a member who never opens them?
4. Does the maker administer any of them, and can the maker see the member list and notification settings without changing anything?
5. Is any device the maker uses for the project signed in to an account she can reach, or backed up to one?

**What each answer changes** (the leak mechanics are in `surprise-ops` [L]: iCloud Shared Library gives every participant add, edit and delete rights and the Camera can auto-share; Google partner sharing shares photos as they are backed up and the partner can save them to her own account).

| Answer | Consequence |
|---|---|
| She is a member of anything shared, or the answer is unknown | Treat as "yes, she can reach it". No project file, scan, test render or archive copy goes there. Use a project-only account on a drive she cannot open; the scanning phone is not in any shared library; USB copies are held by in-on-it relatives only until 2027-02-27 |
| She is a member but never opens it | Still "yes" for planning: notifications, memories and a relative's remark are the usual slips |
| Not a member, but a shared device is signed in | Treat the device as shared; the project stays off it |
| Not a member and no shared device | The maker may use a family-shared drive for non-personal items only (the venue test clip, which has no personal content [L]); personal material still waits until after the reveal |

**For `GATHER.md` (one line to add):** "Before any scan or upload: the maker confirms in writing, from their own accounts, that the subject is not a member of any shared library, drive, album or backup, and that the scanning device is not signed in to one; unknown counts as yes."

### RQ5. Cloudflare Access Free: what counts as a user for the 50 limit

**Answer.** Cloudflare's seat-management page (dateModified 2026-05-01) defines the unit as a **seat** [114]:
- "A user consumes a seat when they perform an authentication event." For Access that is "any Cloudflare Access authentication event, such as a login to the App Launcher or an application." The user's identity is then added as an Active user and "consumes one seat from your plan."
- One seat per identity: "The user will occupy and consume a single seat regardless of the number of applications accessed or login events from their user account."
- It is not a monthly count: "A user who authenticates will hold their seat until you remove the user from your account." By default inactive users are not removed; an admin can enable **seat expiration** (between one month and one year) to remove users who have not logged in, with a daily check. Inactive users do not count towards billing.
- At the cap: "Once the total amount of seats in the subscription has been consumed, additional users who attempt to log in are blocked."
- Revoking a user "will not remove the user's consumption of an active seat"; removing one frees the seat, and a removed user who authenticates again takes a seat again. Removing a user "does not prevent users from accessing resources behind Cloudflare Access", so the allow-list policy remains the real gate.
- Service tokens are listed as a way to give access "without consuming seats" [114].

So it is neither "unique identities per month" nor "enrolled seats" as a pre-registration: it is **unique identities that have actually authenticated, counted persistently until removed**. An email on an Allow rule does not take a seat until that person logs in (my reading of the page; not stated in these words).

**What I could not confirm.** That the Free plan's "50 user limit" [28] is enforced as 50 seats in exactly this way: the seat page never mentions the Free plan, the account-limits page [29] has no user cap (I re-read it: its limits include 50 custom applications and 10 DEX tests on "Zero Trust Free", and "Standard users" and "Enterprise users" columns on list limits), and the general FAQ [115] has no seat text. The mapping is my inference [J].

**What to do.** The family premiere needs 10-40 identities, inside 50. The maker's own test logins (and any helper's) take seats too, so remove test identities after each test (Zero Trust > Team & Resources > Users > Remove) and check the seats-used figure on the Cloudflare One overview [114]. If expecting more than about 45 guests, turn on seat expiration (Zero Trust > Settings > Admin controls > Remove inactive users from seats [114]) or use a different link method.

### Corrections to carry into earlier text (for the scribe)

1. **Cloudflare (Summary 8, Q5 row, T9, Tools row, FQ3 "Still UNVERIFIED", playbook Decision 8, SKILL.md):** replace "what counts as a user is UNVERIFIED" with the seat definition above and cite [114]; keep "the Free plan mapping to 50 seats is inferred".
2. **Summary 4, Q3 table row (a) and nudge 4 text:** label "6-10 h per finished minute" as build-only [J] and point to RQ3; replace it with "measured at G-SLICE, 2026-12-20". Do not use it as an all-in rate. State that the 100-150 h for 8-12 minutes matches `production-scale`'s Prior and Best cases, not its Base case.
3. **Music (Summary 8 item 5, Q5 "Music claims", Pitfalls, playbook Decision 12, SKILL.md):** replace "licensing figures are vendor claims: UNVERIFIED" with the RQ1 layer table; add "which copies must be cleared" (every file carrying a pre-existing recording).
4. **Venue master (T4, Step 8, Step 13, SKILL.md gate e, playbook Decision 3):** add the RQ2 decision rule: the DCP is the venue master only if the venue ingests DCPs; for HDMI-from-laptop venues the 1080p24 H.264 file is the venue master.
5. **Caption safe area (T4, T14):** add "keep text inside the 5% graphics-safe box (96 px sides, 54 px top and bottom at 1080p) at every venue; judge size on the real screen."
6. **Q5 "Cheapest sensible private pattern" and T9:** unchanged by this round; nudge 5 still applies (never a shared family cloud library for project copies).
7. **GATHER.md / surprise-ops:** add the RQ4 line.

### Still UNVERIFIED after round 2

- Everything in RQ1 about whether a venue's blanket licence reaches a film soundtrack outside Australia's published rule; ASCAP, BMI and PRS wording; the current SOCAN tariff; India, the EU and Switzerland.
- Which chain, resolution, frame rate and audio the venue accepts (needs the venue); whether projectors overscan; how cinema masking affects subtitles.
- The measured hours per finished minute (needs the slice); the PowerShell one-liner on Windows PowerShell 5.1.
- The family accounts in RQ4 (needs the maker).
- The Free plan's 50-user limit as exactly 50 seats.

### Sources added in round 2

Tags as above; fetched 2026-10-18 unless stated.

[114] Cloudflare Docs — Seat management — https://developers.cloudflare.com/cloudflare-one/team-and-resources/users/seat-management/ — dateModified 2026-05-01 — [P][V] HTTP 200; read from the raw HTML (E10).
[115] Cloudflare Docs — General FAQ — https://developers.cloudflare.com/cloudflare-one/faq/general-faq/ — dateModified 2026-06-05 — [P][V] checked; no seat or Free-plan text.
[116] 17 U.S.C. 101 (definitions: "publicly", "perform", "motion pictures", "audiovisual works", "sound recordings") — https://www.law.cornell.edu/uscode/text/17/101 — [P] Cornell LII; the tool read the first 100,000 of 110,095 characters, which held these definitions.
[117] 17 U.S.C. 106 — https://www.law.cornell.edu/uscode/text/17/106 — [P] clauses (4) and (6).
[118] 17 U.S.C. 110 — https://www.law.cornell.edu/uscode/text/17/110 — [P] paragraph (4).
[119] U.S. Copyright Office — Copyright and the Music Marketplace (report of the Register of Copyrights), February 2015 — https://www.copyright.gov/docs/musiclicensingstudy/copyright-and-the-music-marketplace.pdf — [P] pp.33-34, 37, 55-56 (printed page numbers); excerpts E1-E4. 11 years old.
[120] ShowBiz Cinemas COO, email to the US Department of Justice on the ASCAP and BMI decrees, 2019-08-09 — https://media.justice.gov/vod/atr/ascapbmi2019/pc-642.pdf — [S] an exhibitor's position, not law; excerpt E6.
[121] OneMusic Australia — Film Screenings (guide) — https://assets.onemusic.com.au/images/PDFs/guides/Film-Screenings.pdf — July 2026 — [P] excerpt E5.
[122] SOCAN — Music licences (tariff list) — https://www.socan.com/music-licenses/ — [P][V] lists Motion Picture Theatres (6), Receptions, Conventions, Assemblies and Fashion Shows (8), recreational facilities (21) and other tariffs by name; no detail on film use.
[123] SOCAN — Tariff No. 6, Motion Picture Theatres (2014-2016), Canada Gazette Part I supplement, 2017-05-06 — https://www.socan.com/wp-content/uploads/2024/05/Tariff-6-GAZETTE-2014-2016-CONDENSED.pdf — [P] excerpt E7; the current tariff year is UNVERIFIED.
[124] UK Copyright, Designs and Patents Act 1988, sections 19 and 5B — https://www.legislation.gov.uk/ukpga/1988/48/section/19 ; https://www.legislation.gov.uk/ukpga/1988/48/section/5B — [P] excerpt E8; the reading of 5B(3)(b) is mine.
[125] Cinema For All — How To Start a Community Cinema starter pack (2024) — https://cinemaforall.org.uk/app/uploads/2024/05/How-to-Start-a-Community-Cinema-2024.pdf — [S] charity guidance; excerpt E9; conflates PRS and PPL.
[126] PRS for Music — sitemap and licence category pages — https://www.prsformusic.com/sitemap.xml ; https://www.prsformusic.com/get-a-music-licence/business-and-commercial — [V] load, but the text is script-rendered; nothing read. Listed so nobody repeats the attempt.
[127] DCP-o-matic manual — Frame rates (ch12, ch12s02), DCP settings (ch07), Timed text (ch06s06), Common tasks (ch17) — https://dcpomatic.com/manual/html/ch12.html ; https://dcpomatic.com/manual/html/ch12s02.html ; https://dcpomatic.com/manual/html/ch07.html ; https://dcpomatic.com/manual/html/ch06s06.html ; https://dcpomatic.com/manual/html/ch17.html — [P] (the manual index at https://dcpomatic.com/manual/ redirects to /manual/html/; paths without /html/ return 404).
[128] EBU — R 95, Safe areas for 16:9 television production, version 1.1, June 2017 — https://tech.ebu.ch/docs/r/r095.pdf — [P] Note 5; excerpt E11. The pixel tables are images; the 96/54/67/38 figures are my arithmetic from the percentages.
[129] Wikipedia — Overscan — https://en.wikipedia.org/wiki/Overscan — [T] digital-input and LCD overscan sentences; no projector content.
[130] Everyman Cinemas — Private hire — https://www.everymancinema.com/private-hire/ (redirects to https://ww2.everymancinema.com/private-hire) — [P] venue marketing page, UK; excerpt E12.
[131] Wikipedia — Experience curve effects — https://en.wikipedia.org/wiki/Experience_curve_effects — [T] Wright's 20% per doubling; "a couple of percent up to 30%"; "does not exactly predict".
[132] Wikipedia — Planning fallacy — https://en.wikipedia.org/wiki/Planning_fallacy — [T] Buehler, Griffin and Ross (1994): predicted 33.9 days, actual 55.5, about 30% on time; reference-class remedy.
[133] Sibling notes read this session [L] — `research/production-scale.md` (Q4 model and cases; Q5 results table; Q7 slice and conversion table; T6 `hours.csv`), `research/theatrical-delivery.md` (Findings 1, 3, 5), `research/music-sound.md` (Q4-Q5 clearance), `research/surprise-ops.md` (shared-library leaks [18][19]), `reviews/format-round2.md` (the five follow-ups and nudges).
[134] Container tests [RUN] — `ffprobe` duration and frame count on a synthetic 100 s 1920x1080 24 fps clip; the `awk` one-liner on a synthetic `hours.csv`. Commands are in RQ3; the synthetic files were in the scratchpad and hold no personal data.
