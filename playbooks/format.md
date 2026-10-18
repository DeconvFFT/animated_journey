# Delivery format and experience architecture

*Track: format. Written 2026-10-18 by the Haiku scribe from the research notes in `research/format.md` and the charter in `CHARTER.md`. Phase: LEARN, no code yet. Bracketed numbers such as [15] point to the Sources section. [J] marks judgment, not a sourced fact. TODO(research) marks a gap.*

## Why this matters for our life journey

The format decides who sees the piece, how they see it, and whether it still works in twenty years. A film shown to a room of 10 to 40 people is a different job from a web page that a grandchild opens alone on a phone.

The research points the same way for this project. In a room with one screen, a paced, captioned film works for everyone at once. Nobody has to hold a controller, and nobody has to wait. The explorable options (a Minecraft tour, a Godot build, a three.js world) scored lowest on room fit, access, finish and failure resilience [J, decision matrix in the notes]. Every group-interactive precedent the notes found needed a host, a vote or a default [65][66][68].

Three things need your decision before anything else.

First, the charter describes the project as "animated, partly playable" [C]. The research default is a linear film, with a playable interlude added only if an early gate passes. That default departs from the charter's wording unless you accept it. See Decision 2.

Second, the charter says the piece is a surprise and that nothing may tip her off [C]. Some steps in the notes would reveal the piece to her, such as showing hard chapters to the subject first. Those steps have changed: hard chapters go to the proxy and to the relatives in them, and the subject sees nothing before the reveal. See Decisions 5 and 6.

Third, time. From Sunday 2026-10-18 to Saturday 2027-02-27 is 132 days, about 19 weeks. 19 weeks minus 2 holiday weeks minus the buffer week = **16 production weeks**: about 160 hours at 10 hours a week, about 320 hours at 20 hours a week [J]. The film's 100 to 150 hours now leaves 10 to 60 hours of margin, which is why F-0 exists.

## Core principles

1. **The default path plays if nobody acts.** Any moment that waits for a choice finishes on its own after about 20 seconds with no input [J]. Bandersnatch works the same way, with a default path after about ten seconds [68]. Nobody in the room should ever feel timed out.

2. **Passive first.** The room should be able to watch without anyone holding a controller. Older players in one study found the rules hard and the time limits stressful [10]. W3C also notes reduced dexterity and short-term memory among older users [1]. A film asks nothing of anyone.

3. **Captions are part of the picture.** Use burned-in captions, which are always on and cannot be turned off [4]. Also make a separate caption file for players that can use one. Netflix's adult guideline is 42 characters per line, two lines, and up to 20 characters per second [5]. For viewers aged 70 and over, aim slower and larger: the BBC recommends 160 to 180 words per minute and DCMP 130 to 160 by level, both for hearing audiences [105][107]. For a room with viewers over 70, aim for 130 to 145 words per minute, never above 160 [J]. No source tested older viewers, so test it.

4. **Files outlive accounts.** The master should be a video file with a standards path, not a link on someone's account. For file-based video masters, the Library of Congress prefers FFV1 in Matroska or ProRes in QuickTime (IMF comes first on its list). It lists MP4 only as a viewing proxy [15]. Hosted links are a convenience, not an archive [34]. Keep three copies on two kinds of storage, with one copy off-site [22].

5. **Capture every interactive as video.** Any playable moment also exists as a clean recording, edited into the master. The Library of Congress lists "video of the software in use" as its last-resort way to keep interactive software [16]. The recording is also your fallback on the night.

6. **Finish before you expand.** Build one chapter at final quality first, then the rest. The week-9 gate tests this [J]. The charter also says nothing critical may depend on one alpha app, and every step needs a proven fallback [C].

7. **Mechanics must mean something.** An interlude has one verb, such as place, open or find. It has no score, no timer and no fail state [J]. The charter's test is that every device says something true about the life [C]. The developer of *That Dragon, Cancer* used one filter for every scene: "Does this scene help the player love Joel more?" [72].

8. **Real memories stay real, and the living subject is protected.** A reconstruction, such as a captured interlude or a Minecraft recreation, must look like one [C, principle 4]. Hard chapters go through the trusted proxy the charter names [C, principle 5]. Older players in one study disliked stories that promoted "depression and gloom" [10]. She is alive, so the tone matters.

## How to do it, step by step

**Step 1. Answer the open questions (week 1).** The format cannot be locked without these answers [notes]. The charter already settles the surprise, the premiere, Windows and the ArtCraft apps [C], so do not ask again:
- How many hours a week can you give?
- Where is the venue, and who runs its sound and projector?
- How many people are expected, and what ages?
- Do you own Minecraft Java Edition, and does she play games?
- Is "partly playable" a must?

The charter names 2027-02-27 as the premiere, at a mostly public gathering [C]. If the event is earlier, move every date up by the same amount [notes].

**Step 2. Lock the format (weeks 1 to 3).** Accept, change or reject the default: a linear, captioned, photo-forward film in chapters, each with room for one optional interlude. If "partly playable is a must," use the hybrid instead, a film with two or three host-driven interludes. In the round-1 matrix the hybrid scores lower, at 3.80 against 4.55 for the film [J].

**Step 3. Define 'pipeline locked' (weeks 1 to 3).** The charter says real photos and stories are gathered only after the pipeline and process are locked [C]. Definition: 'pipeline locked' means Step 8 has passed on Chapter 1. The vertical slice uses only material the maker already possesses (their own digital photos and any existing home video), plus surprise-mode voices in Step 7. No new covert collection starts until G9 passes or the orchestrator opens GATHER.md.

**Step 4. Set up the archive folder and the hash list (weeks 1 to 3).** Create folders for masters, access copies, captions, source photos and audio, and a README. Make a SHA-256 list of every file, and keep the list outside the folder [18]. On Windows, use PowerShell `Get-FileHash`, which is built in and uses SHA-256 by default [100]. The notes' script `research/sources/format-round1/mk_manifest.ps1` writes a `sha256sum`-format list one level above the folder (lowercase hashes, LF line endings). It was tested on PowerShell 7.5.4 on Linux, not on Windows PowerShell 5.1, so check it there first (UNVERIFIED). Do not write the list with `>` or `Out-File`: Windows PowerShell 5.1 writes UTF-16LE, which `sha256sum -c` rejects [102].

**Step 5. Run the look test (weeks 1 to 3).** Run the look test defined in `playbooks/cinematic-quality.md` when it exists; until then the slice is the look test. TODO(research): as of 2026-10-18 that file does not yet define a look test.

**Step 6. Build the chapter structure (weeks 1 to 3).** Each chapter runs 90 to 150 seconds, with a visible breath before the next one. Each chapter has a labelled slot of 60 to 90 seconds for an interlude. By default the slot holds a captured video [notes]. The durations are judgment [J].

**Step 7. Make Chapter 1 as a vertical slice (weeks 4 to 6).** Aim for about two minutes at final quality, with real audio, music, captions and export. Use photos with simple movement, voices in surprise mode (below), and a little selective animation. Templates help, but avoid the floor-level slideshow look the charter rejects [C].

**Toolchain.** FilmCraft is installed (ArtCraft, early alpha, Windows) [C]. It is a refinement layer, not the assembly engine, so the slice must also build from a scripted route with a fallback editor named by the `toolchain` track. The scripted route is the notes' route A: a Python script that writes one ffmpeg command from `timeline.json`, `captions.srt` and an `assets/` folder. It ran in the container: 9 s for a 20 s test film, and 63 s for a 30-shot, 120 s version (notes FQ2). OpenTimelineIO can carry the same cut into FilmCraft or Kdenlive for hand fixes. DaVinci Resolve is free for a film master [63], but the notes treat it as refinement and the final eye, not the assembly engine. The notes estimate 6 to 10 hours per finished minute with templates, AI imagery and parallax [J]. StoryCorps' animators talked with the storytellers during production [77]. With a surprise, any such consultation has to go through the proxy (Decision 6). The format notes do not test the ArtCraft apps. See the craft-visual and craft-motion tracks [C]. FilmCraft's README says Windows and Linux "get far less testing than macOS" [96]; the maker's Windows build is one of the least-tested platforms, which is one more reason route A is the engine and FilmCraft the refinement layer.

**Voices in surprise mode.** The surprise rules out her real voice unless a recording already exists. Use, in this order of preference:
- (i) her existing recorded voice from home video, voicemail or voice notes, if any survive and the proxy agrees;
- (ii) relatives speaking about her, recorded one at a time from the people the maker has decided to bring in (OPEN (maker): nobody is in on it yet, so this source waits on that decision [C]);
- (iii) her own letters and cards, read by a relative and shown attributed.

No synthetic or cloned voice of anyone [C, principle 4].

**Threshold (notes FQ1, [J]).** The slice needs about 45 to 90 seconds of clearly her speech per chapter, roughly 3 to 5 minutes in all, or one clip of 60 seconds or more. If the family can produce under about 2 minutes in all, F-0 uses sources (ii) and (iii) instead of her voice.

**The six questions, for people the maker brings in.** Ask by phone or in person, and put nothing in writing that she could see. (1) Do you have any video or voice message of her, on your phone or on old tapes? Please do not delete anything, and do not forward it to me. (2) Roughly when was each made, and who else is speaking? (3) Is it still on a phone or card, or only on a tape, disc or old computer? Is the player still around? (4) Is she talking for a minute or more at a stretch, or only in short bits? (5) Who else might hold something? (6) Are you happy for me to copy it and use it in a film that will be shown at a public gathering and kept by the family afterwards; is there anything she, or you, would not want shown in a room that is not all family? Record each answer with holder, device or format, rough date, who speaks, length, quality, whether the original is in hand, copies and consent. Do not clean or force a magnetic tape; one careful transfer pass, by a lab or a machine in good order [93].

**Step 8. Harden the slice (weeks 7 to 9).**
- Export the master (FFV1 in Matroska, or ProRes in QuickTime) and an H.264 MP4 at 1080p as the access copy [15][85].
- Make three caption versions: burned-in, a clean picture, and `.srt` and `.vtt` sidecar files [4][5].
- Check that nothing flashes more than three times a second [3].
- Caption size: line height 7 to 8% of picture height (BBC [105]). In ffmpeg's subtitles filter, `FontSize=23` gives about 8.0% at 1080p (notes FQ2). Render FontSize 20, 23 and 26, and test them on the venue screen from three metres (notes FQ5).
- Play the slice from a USB stick on a TV-class screen. This is the fallback test (Decision 3); the real test is the venue screen. Have a viewer aged 60 or over watch from three metres and say whether the text is comfortable to read [notes].
- The venue projection master (DCP, or ProRes at the projector's resolution and frame rate) is decided by the `theatrical-delivery` track by G13; the H.264 MP4 is the access and fallback copy. TODO(research): RQ2 found that for a venue taking HDMI from a laptop, the 1080p24 H.264 file can be the venue master; reconcile before G13.

**Step 9. Optional: prototype one interlude (weeks 7 to 9, at most 20 hours).** See Exercise 4.

**Step 10. Gate G9, Sunday 2026-12-20.** Pass if Chapter 1 is at final quality (T14) and logged hours are at least 60% of plan. If an interlude was prototyped in Step 9, it must also have run ten times in a row to stay in the plan; if not, it is dropped and the film continues. No interlude is never a fail. On a fail, switch to the fallback F-0 (below).

**Step 11. Rough-cut the other chapters (weeks 12 to 15, 2027-01-03 to 2027-01-30).** Weeks 10 and 11 (2026-12-20 to 2027-01-02) are the holidays: interviews and gathering, with no production targets (charter review 1.3). Gate G13 falls on Sunday 2027-01-17 (Step 12). Add a second interlude only after G13.

**Step 12. Gate G13, Sunday 2027-01-17.** (Moved from 2027-01-10: two further chapters at rough cut one week after production resumes on 2027-01-03 is not credible.) At least two further chapters (beyond Chapter 1) must be at rough cut. If not, drop all live interludes and keep their captured videos as film scenes [notes]. An interlude that is not stable after ten consecutive dry runs by this date is dropped in the same way [notes].

**Step 13. Picture lock, captions, music and mastering (weeks 16 and 17, 2027-01-31 to 2027-02-13).** Lock the picture. Finish the captions. Settle the music (Decision 12). Master the files. The venue projection master (DCP, or ProRes at the projector's resolution and frame rate) is decided by the `theatrical-delivery` track by G13; the H.264 MP4 is the access and fallback copy.

**Step 14. Rehearse and copy (week 18, 2027-02-14 to 2027-02-20).** Hold two rehearsals on the real screen and speakers. Make three archive copies, and check each one against the hash list [notes]. One copy may be a BD-R: buy blanks in January 2027, rehearse a small burn in December, burn the real disc in February from the final `archive.iso`, and verify it by reading it back with `verify_manifest.ps1` (0 problems expected) [110][notes FQ7].

**Step 15. Event kit and delivery (week 19, 2027-02-21 to 2027-02-27).**
- Send the file to the venue a day before. Ask which format, resolution and aspect ratio they want [85].
- Bring a USB stick and, only with the maker's explicit yes, a cloud copy [85][C].
- Have the laptop open at the start point, a second USB stick, and a printed running order [notes].
- Keep this week as buffer.

**If an interlude is in the show, use the failure ladder.**
- Level 0: the live interlude runs.
- Level 1: it hangs. Press one hotkey to start its captured video.
- Level 2: the laptop fails. Play the linear MP4 from USB on the venue's own player.
- Level 3: there is no AV. Show the MP4 on a tablet or phone, with the printed companion.

Rehearse each level once on the real screen [notes]. A host, never the subject, presses start, because web builds cannot play sound until someone clicks [11][12]. Expect talk from the room. Viewers of other people's play often narrate their own lives as they watch [83].

**Fallback F-0, "voice and photos."** This is a 5 to 6 minute film of three or four chapters. It has restored photos with simple movement, voices in surprise mode (Step 7), music, burned-in captions, and an optional timeline page for the private link [notes]. It is a strict subset of the default, so no work is wasted. Switch to it if the slice is not at final quality at G9, if logged hours are under 60% of plan at G9, or if any chapter costs more than twice its budget two times in a row [notes].

## Learn-by-doing exercises

### Exercise 1: The caption test on a real screen

**Goal.** Find a caption size and line length that a viewer aged 60 or over can read from three metres, on the real screen.

**Steps.**
1. Take 60 seconds of test footage with a voice and a picture.
2. Make three versions with burned-in captions at three sizes. Keep each line to 42 characters or fewer, and use at most two lines [5].
3. Play each version on the screen and speakers you will use on the night.
4. Seat a viewer aged 60 or over three metres away. Ask which version they could read without leaning in.
5. Write down the characters per line and the characters per second for the winner.

**Time.** About 2 to 3 hours, mostly setting up the screen [J].

**What good looks like.** The viewer reads every line without leaning in. The speed is under 20 characters per second, and slower if they struggle [5][J]. No controlled study of caption speed for hearing viewers over 70 was found (notes FQ5), so this test is the only evidence. Also try FontSize 20, 23 and 26.

### Exercise 2: The three-copy restore test

**Goal.** Prove that the archive can be restored from a copy held somewhere else.

**Steps.**
1. Create the archive folders: masters, access copies, captions, source material, and a README.
2. Make a SHA-256 list of every file. Save the list outside the folder [18].
3. Copy the folder to two drives or devices. Give one copy to a relative who keeps it in a different place [notes].
4. Check each copy against the list. Restore one file from the relative's copy into a clean folder and play it.
5. Put a yearly reminder in your calendar to power up the drives and check the hashes [18].

**Time.** About 2 to 3 hours the first time, plus copy time [J].

**What good looks like.** Every copy matches the list. A relative can open the README and play the film without you.

### Exercise 3: The failure-ladder dry run

**Goal.** Show that one failure on the night costs seconds, not the show.

**Steps.**
1. Before the start, open the film and the interlude app on the laptop you will use.
2. Level 0: run the interlude live from start to finish.
3. Level 1: close the interlude app, then start its captured video with the hotkey. Time the switch.
4. Level 2: stop the laptop. Play the linear MP4 from USB on the screen's own player, or on a second laptop. Time the switch.
5. Level 3: play the MP4 on a tablet or phone. Note what you would have to hold, and where you would stand.

**Time.** A few hours, including setup [J]. The notes budget 15 to 25 hours for rehearsal and polish across a full hybrid [notes].

**What good looks like.** Each level is reached within seconds, on the real screen. A helper who did not build the piece can run the ladder from the printed running order [J].

### Exercise 4: One interlude, captured first (weeks 7 to 9, optional, at most 20 hours; its ten-run result feeds G9)

**Goal.** Learn one interactive craft with one verb. Keep a captured copy, so the film is safe if the live version fails.

**Steps.**
1. Choose an engine: Bitsy, GDevelop or Godot. Check the open facts first. Bitsy's export format is unverified [59], and GDevelop's free HTML5 export was not clear on its page [61]. Godot's core plays only Ogg Theora video, and its docs advise 720p or less for the web [41].
2. Write the one verb (place, open or find), and a three-line host script such as "Whose kitchen is this?" [notes].
3. Build it with no score, no timer and no fail state.
4. Make the default path finish the interlude on its own after about 20 seconds with no input [J].
5. Record one clean run as video, 60 to 90 seconds long.
6. Run it ten times in a row on the real screen.

**Time.** Cap at 20 hours [notes]. The notes estimate 15 to 30 hours for a Bitsy or GDevelop interlude, and 30 to 50 hours for Godot [J].

**What good looks like.** Ten dry runs in a row with no crash and no stuck state. The captured video matches the live version. A relative who is in on the project can say what to do after one look [J]. If the interlude misses the gate, drop it and keep the video as a film scene.

### Exercise 5: The three-person test

**Goal.** Get reactions from three people of different ages, without tipping off the subject.

**Steps.**
1. Choose three people the maker has decided to bring in. Nobody is in on the project yet, and bringing anyone in is the maker's open decision [C]. Show them only what you are happy for them to see.
2. Make a 60-second captured clip from the slice or the interlude.
3. Show each person the clip on a real screen, one at a time or in a small group.
4. Ask three questions: What did you notice? Who did you want to talk to? What was hard to see or follow? The first two come from the notes [notes]. The third is ours [J].
5. Write the answers in the project notes. Do not send the clip or the answers through a family group chat or a shared cloud album [C].

**Time.** About half a day, most of it spent finding the right three people [J].

**What good looks like.** Each person answers all three questions. At least one answer changes something in the plan. Three people are not evidence about a room, but they are a cheap first check. TODO(research): the notes found no reaction evidence from a mixed-age, non-gamer room for any explorable or hybrid format.

### Exercise 6 (optional): One Minecraft diorama, only if Java is owned

**Goal.** Learn whether Minecraft capture is worth doing for one chapter.

**Only if.** You own Minecraft Java Edition [notes]. For a whole chapter, the notes also want 20 or more hours a week and a subject who loves the game [notes].

**Steps.**
1. Write the pre-flight list: Java or Bedrock; the edition you own; your operating system; the exact version. Java has used year-based versions since 26.1, and it needs Java 25 [48]. The Replay Mod needs Fabric for 1.14 and later, or Forge for 1.12.2 and earlier [44]. Check that FFmpeg is installed [44]. Back up the world. Re-read Mojang's terms.
2. Build one small diorama. The notes estimate 8 to 15 hours per diorama [notes].
3. Plan the route first. Replay Mod records only chunks that were loaded, and it cannot start in the middle of a session [44].
4. Record about 60 seconds on a camera path, then render to MP4 with FFmpeg [44].
5. Archive the world folder, the version list and the render together [notes].

**Time.** The notes estimate 8 to 15 hours for the diorama, plus capture and render time [notes][J].

**What good looks like.** The 60-second render plays on a second computer without help. The archive holds the exact version list. The Mojang terms check is written down with its date. The Usage Guidelines excerpt of 2026-10-18 is saved (notes FQ6). Re-save it before any showing, because the page reserves the right to change.

## Decisions you'll need to make

For each decision: the options, our current lean, and what would change it.

### Decision 1: The format

**Options.**
- (a) A linear, captioned film, built to take interludes later. This is the lean.
- (b) A film with two or three host-driven interludes.
- (c) A scroll story, such as a timeline page or a Closeread page.
- (d) An explorable world (Minecraft, Godot or three.js) as the main piece.

**Our lean.** (a) for the main piece. In the round-1 decision matrix, the film scores 4.55 out of 5, the film plus companion 4.40, the hybrid 3.80, and the explorable options between 2.45 and 2.95 [J]. The matrix weights are judgment, and round 1 moved them: agent-generability and texture capacity now carry 10 each, and learning value carries none. The scribe rechecked the totals and the five sensitivity tests. The film stays first under each of them, and the hybrid overtakes it only if charter fit carries about 31% of the total weight. The middle of the table moves: the scroll story (3.55) now ties the Minecraft film (3.55).

**Effort.** Budget = 19 weeks minus 2 holiday weeks minus the buffer week = **16 production weeks**: about 160 h at 10 h/week, about 320 h at 20 h/week. The film's 100 to 150 h now leaves 10 to 60 h of margin, which is why F-0 exists. The table below is at 10 hours a week. These are the notes' judgments, not measured hours [J].

| Format | Maker-hours | Slice ready by week 9 |
|---|---|---|
| Linear film | 100 to 150 | about 90% |
| Film rendered from Minecraft | 130 to 220 | about 70% (one diorama plus one 60-second shot) |
| Scroll story | 70 to 100 | about 85% |
| Godot explorable | 120 to 200 | about 55% (one room) |
| three.js voxel world | 200 to 300 | about 40% (one diorama viewer); the course alone is 93 hours of video [53] |
| Film plus 2 to 3 interludes | 150 to 240 | film about 85%; first interlude about 55% |

**What would change it.** "Partly playable is a must" (Decision 2). Or 20 or more hours a week, a Java copy, and a subject who loves Minecraft. In that case, use Minecraft for one or two chapters, not the whole piece [notes].

### Decision 2: Is "partly playable" a must?

**Options.** Yes: go with the hybrid (b). Nice to have: a film with an optional interlude, added only if G9 passes (a).

**Our lean.** Nice to have, decided at G9. This departs from the charter's wording [C]. Decide it on purpose, and make the charter say what you decided.

### Decision 3: The venue and its screen

**Options.** A hired hall with a projector. A community room or restaurant with a screen. TODO(research): the venue, the date and the AV operator are not known.

**Our lean.** A hall, cinema or community room with a projector and a sound system, operated by someone the maker has briefed. The film design needs a screen the whole room can see and speakers that carry the voice. If the venue has neither, the room argument weakens [notes]. Choose the screen first, then test the captions on it. The 3-metre TV test in Step 8 becomes the fallback test (failure ladder level 2); the real caption test happens on the venue screen, from its back row.

### Decision 4: Premiere or delivery date

**Options.** 2027-02-27 is the event. Or it is only the delivery date, and the event is earlier or later.

**Our lean.** Settled by the charter; keep only the rule that if the event moves, every date moves by the difference [notes].

### Decision 5: Surprise, and who is brought in

**Options.** The surprise, as the charter says [C]. This is a Known fact, so it is settled, not a question. Still open: whether to bring anyone else in, for example to give a recording or a letter (charter open decisions).

**Our lean.** Keep the surprise. Bring people in one at a time, only when the maker decides. Until then the in-on-it list is empty, so voice sources (ii) and the six-question ask in Step 7 wait on that decision. OPEN (maker).

### Decision 6: Who sees the hard chapters before the room?

The notes advised showing hard chapters to the subject and relevant family first. In a surprise, that step would reveal the piece to her, so it is replaced. The charter names the maker as her proxy for hard chapters, with the Fable advisor flagging sensitive material for a deliberate decision [C, principle 5 and Known facts]. Hard chapters go to that proxy and to the relatives in them; the subject sees nothing before the reveal.

**Options.** (i) The maker decides as proxy, with the advisor flagging sensitive material. (ii) Show her the hard chapter in advance, and accept the spoiler. (iii) Leave the hard chapters out.

**Our lean.** (i), and (iii) for anything the proxy is unsure about [C]. Name the proxy in the plan: the maker.

### Decision 7: How many chapters, and which

**Options.** Inventory every milestone first (the `story` track's template), then choose which to tell. Tell 4 to 8 chapters of 90 to 150 seconds each; the rest appear as texture or in the companion [C, review 1.1].

**Our lean.** 4 to 8 told chapters. Running time follows from the chapter count, not the other way round: 4 chapters run 6 to 10 minutes, and 8 chapters run 12 to 20 minutes [J]. The notes' 8 to 12 minute plan sits at the 90 to 120 second end of that range [notes]. The funeral-slideshow figure of 3 to 8 minutes [85] is the floor's convention, not evidence about a life story; the chapter count is the story track's call. A full life will run longer than a standard tribute film [85], so this is a deliberate choice, not an accident.

The charter leaves runtime open (short, mid-length, feature). At the notes' 6 to 10 hours per finished minute, which is a build-only figure [J] and not an all-in rate: 4 to 8 chapters (6 to 20 minutes) cost 40 to 200 hours on that figure and fit the 16-week budget; a 40-minute mid-length piece costs 240 to 400 hours and fits only at 20 hours a week with nothing else; an 80-minute feature costs 480 to 800 hours and does not fit before 2027-02-27 at any realistic rate. On `production-scale`'s all-in model, a 12-minute film costs 116 to 284 hours (9.7 to 23.7 hours per finished minute). It fits the 160-hour budget on that model's Best and Prior cases (116 and 141 hours), not its Base case (284 hours) [research RQ3]. The `production-scale` track owns the per-minute figure; until it reports, the default is a short film of 4 to 8 chapters, and feature is a scope decision, not a format decision. TODO(research): replace with the measured figure at G-SLICE (2026-12-20).

### Decision 8: Where it lives

Every hosting option has a single point of failure: one account, one card, or one person's goodwill [notes].

| Option | Cost | Privacy | Watch out for |
|---|---|---|---|
| YouTube Private, with email invites | Free [34] | Invite by email; no comments [34] | One Google account; YouTube systems and human reviewers may review private videos [34], so a third party sees family footage |
| YouTube Unlisted | Free [34] | Anyone with the link can view it, and can reshare it [34] | Not private against forwarding |
| Static page with StaticCrypt | Free [35] | One shared password per page [35] | Guessable offline if the password is weak [35]; not for large video |
| Cloudflare Pages behind Access | Access Free plan: $0; 50-user limit on the Free plan: confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91] | Deny by default; email allow-list [30] | Pages caps each file at 25 MiB, so the film must live elsewhere [31] |
| itch.io Restricted page | Free [36] | Password or download key [36] | Whether the password covers the HTML5 embed: TODO(research) |
| GitHub Pages | Free, but public | Private sites need GitHub Enterprise Cloud [26] | Not suitable for family material |

**Our lean.** YouTube Private only after the maker's explicit yes to Google reviewers seeing family footage; otherwise a copy on a drive or account she cannot open (never a shared family cloud library, which the charter names as a tip-off risk [C]); until the reveal, USB drives held by in-on-it relatives only (OPEN (maker): the in-on-it list is empty until the maker decides) [J, from the notes]; any shared online copy is created after 2027-02-27. Before any upload, get your own explicit yes. The charter says nothing personal goes to a third-party service without your explicit say [C]. Do not send the link through a family group chat, a shared device or a shared photo album [C].

### Decision 9: Minecraft in the piece

**Options.** None. One or two chapters rendered from Minecraft, which needs Java. A live Minecraft tour, which the notes do not recommend, because the room waits while someone drives.

**Our lean.** None, unless Exercise 6 passes and its conditions are met. Mojang's rules for showing gameplay in venues are a grey area [50][88]. The Usage Guidelines were read on 2026-10-18 (HTTP 200 on the second attempt; dated excerpt [92]). They say gameplay may not be displayed or projected publicly in physical locations in the two commercial cases quoted; whether a family showing counts as 'public' is not defined. They reserve the right to change at any time, so re-save the excerpt the week of any showing.

### Decision 10: The interlude engine (only if G9 passes)

**Options.** Bitsy, which is free and HTML5 [59]. GDevelop, which has a free plan with limits [61]. Godot, which is free and MIT-licensed [42].

**Our lean.** Bitsy or GDevelop, because the notes estimate fewer hours for them [J]. Godot has more power, but it has web-export limits [40] and video limits [41]. Check Bitsy's export format and GDevelop's free HTML5 export first (TODO(research)).

### Decision 11: A companion

**Options.** A printed photo book. A timeline page, such as TimelineJS [54]. A Closeread page [56].

**Our lean.** Optional. It is not on the critical path [notes]. Photo book prices and lead times are unverified (TODO(research)). TimelineJS needs a public Google Sheet, and the notes say never to delete that sheet [54].

### Decision 12: Music

**Options.** Original or licensed music. Commercial songs.

**Our lean.** The premiere is a public screening [C], so Principle 7 applies in full: every piece of music is licensed for public exhibition or original; a personal streaming subscription authorises nothing [85]; the `music-sound` track owns the licence recipe; the private-link copy needs the same clearance because YouTube may block or mute it [J]. There is no lower-risk private-showing case. The licence figures in the funeral-industry guide come from a vendor blog and are unverified [85] (TODO(research)).

### Decision 13: Languages and audience

The charter lists this as open [C]. The format notes do not cover translated or subtitled versions. TODO(research): decide whether subtitles in other languages are needed, and test them.

### What the research could not settle

- No creator threads (X, Reddit, YouTube), no learner-made life-journey films, and no Replay Mod or Flashback memorials were found. The search budget ran out. TODO(research): run this search when budget is available.
- No reaction evidence from a mixed-age, non-gamer room exists for any explorable or hybrid format. Treat those formats as untested for this audience.
- Caption speed for viewers aged 70 and over is untested; the BBC and DCMP figures are for hearing audiences. The "under 20 characters per second" aim, and 130 to 145 words per minute for a room with 70+ viewers, are judgment.
- Effort hours, week-9 probabilities and matrix scores are judgment. They depend on hours per week, the venue, the audience, the surprise, and whether "partly playable" is a must.
- Could not be verified: Chunker (HTTP 429); Vimeo plan details; Canva; Kdenlive; PlayCanvas; the Mozilla Hubs end-of-support page; VLC kiosk flags; Bitsy's export format; GDevelop's free HTML5 export; private-object handling in R2; and whether itch.io's Restricted password protects the HTML5 embed. Read in round 1: the Minecraft Usage Guidelines (dated excerpt) and the BBC subtitle guidelines (v1.2.5). Ofcom's subtitle guidance was blocked (HTTP 403).
- Whether the Late Shift cinema screenings used audience voting is unverified [69].
- Snow Fall [80], Pine Point [82] and the TimelineJS example links were checked for liveness only. Nobody has checked that they render in a 2026 browser.
- Prices are not verified for photo books, Vimeo, custom domains, or any paid hosting beyond the free tiers listed.

## Pitfalls

- **Choosing by what is fun to build.** The explorable formats score highest on charter fit and learning, and lowest on room fit, access, finish and failure resilience [notes]. Start from the room and the charter.
- **"No code yet" is not "no code ever."** No-code tools hide code in macros, event sheets and interfaces. AI can write that code, but you still have to run it and judge it [notes].
- **Minecraft edition confusion.** The Replay Mod and Flashback are Java-only in practice [44][45]. Bedrock has its own camera command [46]. Java's year-based numbering began with 26.1 on 2026-03-24 [48]. The Java launcher needs a Microsoft account and a purchased licence [49]. Do not plan a capture pipeline until the edition and version are known.
- **Links are not archives.** Unlisted is not private [34]. A TimelineJS sheet is public to the web [54]. A StaticCrypt page can be guessed offline if the password is weak [35]. Netlify's password protection is a paid feature [33].
- **Platforms die.** Flash content was blocked from 2021-01-12 [24]. Glitch ended project hosting on 2025-07-08 [25]. YouTube's 2019 removal of annotations broke an interactive series [66]. Spline's free web exports are watermarked, and self-hosted export is Enterprise-only [62].
- **One owner, one account.** Apple's Legacy Contact needs an access key and a death certificate, and it excludes purchases and Keychain [38]. Google's Inactive Account Manager lets you name up to 10 trusted contacts. Google reserves the right to delete accounts that have been inactive for at least two years [39].
- **Running over time.** *Snow Fall* took about 5 to 6 months with long idle stretches [79]. Unpacking's studio planned about 1.5 years and took about twice that [84]. *That Dragon, Cancer* took about four years [70]. Plan slack into every chapter.
- **Sound on the web needs a click.** Chrome and iOS Safari block sound until the user acts [11][12]. Godot's web export has the same limit [40].
- **Scroll stories fight presenters.** Hijacking the scroll is "generally considered bad practice" [58]. A presenter mode needs hidden code.
- **Flashing and fast moves.** Keep to no more than three flashes per second [3]. Anything on a web page that moves for more than five seconds needs a pause control [2]. Fast pans in a voxel fly-through can cause discomfort on a big screen [7][J].
- **A weak mechanic gets noticed.** The creator of *That Dragon, Cancer* said critics fixated on a minigame that "didn't play very well" [73]. Cut a weak interlude rather than defend it [J].
- **Press is not audience evidence.** The Minecraft memorials in the notes are second-hand and mostly solitary [74][75][76]. Treat them as examples, not proof.
- **Tip-offs.** Shared devices, cloud photo libraries and family group chats can reveal the piece [C], including the archive and test copies.
- **A film is curated; a world is not.** A film shows only what was approved. A world lets viewers open any door, which makes consent harder [notes].

## Best references

1. **Library of Congress, Recommended Formats: Moving Image** [15]. https://www.loc.gov/preservation/resources/rfs/moving.html. Worth the time to see which video files count as masters, and why MP4 is only a copy.
2. **NIST IR 8387** [18]. https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8387.pdf. How long unpowered drives hold data, the copy-every-20-years rule, and why hash lists live apart from the files.
3. **Library of Congress, Software and Video Games** [16]. https://www.loc.gov/preservation/resources/rfs/software-videogames.html. Why every interactive piece needs a video of it.
4. **Netflix English Timed Text Style Guide** [5]. https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide. Line length, number of lines and reading speed for captions. Use it as a starting point, then test with older viewers.
5. **Lee et al., JMIR Serious Games (2021)** [10]. https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/. What 40 middle-aged and older players found hard. The researcher read it from a saved copy.
6. **Black Mirror: Bandersnatch, Wikipedia** [68]. https://en.wikipedia.org/wiki/Black_Mirror:_Bandersnatch. A clear example of the default-path design and the linear fallback. Encyclopedic, so use it for the pattern, not for facts about the production.
7. **Parting Stone, "How to Make a Slideshow for a Funeral"** [85]. https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/. A practical checklist for export, timing and venue checks. It is a vendor blog, and its licence figures are unverified.
8. **Knight Lab, TimelineJS** [54]. https://timeline.knightlab.com/. The simplest companion timeline, and its warning about the public Google Sheet.

## Sources

Tags, as used in the research notes: [P] official or primary; [S] journalism quoting a creator, or a vendor blog; [T] Wikipedia or encyclopedic; [L] a sibling-saved copy, read as data; [V] liveness checked by the researcher on 2026-10-18; all pages fetched on 2026-10-18 unless another date is given. [C] is the charter.

The scribe did not re-open any of these pages. Each entry is copied from the research notes, including the researcher's verification status.

**[C]** Life Journey — Project Charter — CHARTER.md — read 2026-10-18 — principles, rubric, constraints.

**Accessibility and audience**
[1] W3C WAI — Web Accessibility for Older Users — https://www.w3.org/WAI/older-users/ — undated (notes it is partly out of date) — [P] barriers and recommendations for older users.
[2] W3C — Understanding SC 2.2.2 Pause, Stop, Hide (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html — [P] five-second rule.
[3] W3C — Understanding SC 2.3.1 Three Flashes or Below Threshold (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html — [P].
[4] W3C — Understanding SC 1.2.2 Captions (Prerecorded) (WCAG 2.2) — https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html — [P] open vs closed captions.
[5] Netflix — English Timed Text Style Guide — https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide — undated — [P] 42 characters, two lines, 20 cps adult.
[7] MDN — prefers-reduced-motion — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — [P] vestibular triggers.
[10] Lee S, Oh H, Shi C-K, Doh YY — Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population, JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ — 2021 — [P][L] 40 participants; read from the sibling's saved text.
[11] Chrome for Developers — Autoplay policy in Chrome — https://developer.chrome.com/blog/autoplay — last updated 2017-09-13 — [P] gesture, engagement, flag, enterprise policy.
[12] WebKit — New video policies for iOS — https://webkit.org/blog/6784/new-video-policies-for-ios/ — 2016-07-25 — [P].

**Preservation, hosting, privacy**
[15] Library of Congress RFS — Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — [P] FFV1/MKV, ProRes; MP4 as proxy.
[16] Library of Congress RFS — Software and Video Games — https://www.loc.gov/preservation/resources/rfs/software-videogames.html — [P] source, build, video of use.
[18] NIST IR 8387 — Digital Evidence Preservation, Guttman, White, Walraven — https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8387.pdf (DOI https://doi.org/10.6028/NIST.IR.8387) — September 2022 — [P] media longevity Table 1; text extracted locally with pdftotext.
[22] Backblaze — Why the 3-2-1 Backup Strategy is the Best, Yev Pusin — https://www.backblaze.com/blog/the-3-2-1-backup-strategy/ — 2024-05-23 — [S] vendor.
[24] Wikipedia — Adobe Flash — https://en.wikipedia.org/wiki/Adobe_Flash — [T] end of life dates; Ruffle, Flashpoint.
[25] Wikipedia — Glitch, Inc. — https://en.wikipedia.org/wiki/Glitch,_Inc. — [T] hosting ended 2025-07-08 (announced May 2025).
[26] GitHub Docs — Changing the visibility of your GitHub Pages site — https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site — [P].
[28] Cloudflare — Access product and pricing page — https://www.cloudflare.com/zero-trust/products/access/ — fetched with a plain HTTP request — [P] Free plan $0; 50-user limit on the Free plan: confirmed on [28]'s comparison table (Core capabilities > Usage), read twice on 2026-10-18; what counts as a user is UNVERIFIED; a card is needed at onboarding even on Free [91] (notes FQ3).
[29] Cloudflare Docs — Zero Trust account limits — https://developers.cloudflare.com/cloudflare-one/account-limits/ — updated 2026-10-16 — [P] 1,000 emails per rule; no 50-user cap found in its text (notes FQ3).
[30] Cloudflare Docs — Access policies — https://developers.cloudflare.com/cloudflare-one/policies/access/ — [P] deny by default; email selectors.
[31] Cloudflare Docs — Pages limits — https://developers.cloudflare.com/pages/platform/limits/ — [P] 25 MiB per file.
[33] Netlify Docs — Password protection — https://docs.netlify.com/manage/security/secure-access-to-sites/password-protection/ — [P].
[34] YouTube Help — Change video privacy settings — https://support.google.com/youtube/answer/157177 — [P].
[35] StaticCrypt — https://github.com/robinmoisson/staticrypt — [P] README.
[36] itch.io — Access control — https://itch.io/docs/creators/access-control — [P].
[38] Apple Support — Legacy Contact — https://support.apple.com/en-us/102631 — [P].
[39] Google Account Help — About Inactive Account Manager — https://support.google.com/accounts/answer/3036546 — [P].

**Engines and tools**
[40] Godot Docs — Exporting for the Web — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html — [P].
[41] Godot Docs — Playing videos — https://docs.godotengine.org/en/stable/tutorials/animation/playing_videos.html — [P] Ogg Theora only in core.
[42] Godot Docs — FAQ — https://docs.godotengine.org/en/stable/about/faq.html — [P] MIT, GDScript, exports.
[44] Replay Mod — Documentation — https://www.replaymod.com/docs — [P] versions, recording, keyframes, FFmpeg.
[45] Modrinth — Flashback — https://modrinth.com/mod/flashback — [P] Java, Fabric, ARR, versions.
[46] Minecraft Wiki — Commands/camera — https://minecraft.wiki/w/Commands/camera — [T] Bedrock and Education only; play_spline 26.0.
[48] Minecraft Wiki — Java Edition 26.1 — https://minecraft.wiki/w/Java_Edition_26.1 — [T] released 2026-03-24; year-based naming.
[49] Minecraft Wiki — Minecraft Launcher — https://minecraft.wiki/w/Minecraft_Launcher — [T] Microsoft account; offline after download.
[50] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 on the second attempt (HTTP 200); quotes from the dated excerpt [92]. Earlier attempts returned HTTP 503 and a timeout.
[53] Three.js Journey — https://threejs-journey.com/ — [P] 93 h, $95, JS prerequisite.
[54] Knight Lab — TimelineJS — https://timeline.knightlab.com/ — [P] fetched with a plain HTTP request; tips, FAQ, privacy.
[56] Closeread — https://closeread.dev/ — [P].
[58] The Pudding — How to implement scrollytelling with six different libraries — https://pudding.cool/process/how-to-implement-scrollytelling — [P].
[59] Bitsy on itch.io — https://ledoux.itch.io/bitsy — [P] devlog v8.15 2026-02-12.
[61] GDevelop — Pricing — https://gdevelop.io/pricing — [P] undated; Free plan limits.
[62] Spline — Pricing — https://spline.design/pricing — [P].
[63] Blackmagic Design — DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — [P] Resolve 21 free; Studio $295.

**Examples and case studies**
[65] Wikipedia — Kinoautomat — https://en.wikipedia.org/wiki/Kinoautomat — [T]. kinoautomat.cz did not respond on 2026-10-18 [V].
[66] Wikipedia — Interactive film — https://en.wikipedia.org/wiki/Interactive_film — [T] My One Demand, Kinoautomat, YouTube annotations; final 10k characters unread.
[68] Wikipedia — Black Mirror: Bandersnatch — https://en.wikipedia.org/wiki/Black_Mirror:_Bandersnatch — [T] first 100,000 characters read.
[69] Wikipedia — Late Shift (video game) — https://en.wikipedia.org/wiki/Late_Shift_(video_game) — [T] 2017; cinema voting not mentioned.
[70] Wikipedia — That Dragon, Cancer — https://en.wikipedia.org/wiki/That_Dragon,_Cancer — [T].
[72] Game Developer — Game as memorial: That Dragon, Cancer developer reflects — https://gamedeveloper.com/design/game-as-memorial-i-that-dragon-cancer-i-developer-reflects — 2014-11-12 — [S].
[73] The Spinoff — "Death is the thing we all share" (Ryan Green) — https://thespinoff.co.nz/pop-culture/02-06-2017/death-is-the-thing-we-all-share-why-one-father-made-a-video-game-about-his-sons-cancer-battle — 2017-06-02 — [S].
[74] SooToday — Son builds virtual Minecraft zoo and memorial to honour his deceased father — https://www.sootoday.com/great-stories/son-builds-virtual-minecraft-zoo-and-memorial-to-honour-his-deceased-father-9-photos-707477 — 2017-09-01 — [S][L] my WebFetch got 403; read from the sibling's saved copy.
[75] The Harvard Crimson — A House, Pixelated, Can Stand — https://www.thecrimson.com/article/2020/4/30/minecraft-pfo/ — 2020-04-30 — [S].
[76] Minecraft.net — Remembering Pendar2 (Tom Stone) — https://www.minecraft.net/en-us/article/remembering-pendar2 — 2019-04-06 — [P][L] my WebFetch got 503; read from the sibling's saved copy.
[77] StoryCorps — Inside StoryCorps: turning words into visuals — https://storycorps.org/inside-storycorps-turning-words-into-visuals/ — [P].
[79] OpenNews Source — How We Made Snow Fall — https://source.opennews.org/articles/how-we-made-snow-fall/ — undated in my fetch (the sibling gives 2013) — [P].
[80] The New York Times — Snow Fall — https://www.nytimes.com/projects/2012/snow-fall/index.html — [V] HTTP 200, 177,243 bytes; rendering not tested.
[82] NFB — Welcome to Pine Point — https://pinepoint.nfb.ca/ — [V] HTTP 200, 53,014 bytes; no flash/swf strings found; rendering not tested.
[83] Eurogamer — The creators of Unpacking on developing a "weird", queer, BAFTA-winning game — https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game — April 2022 — [S][L] fetch tool blocked this domain; read from the sibling's saved copy.
[84] Wikipedia — Unpacking (video game) — https://en.wikipedia.org/wiki/Unpacking_(video_game) — [T].
[85] Parting Stone — How to Make a Slideshow for a Funeral — https://blog.partingstone.com/how-to-make-a-slideshow-for-a-funeral/ — undated (mentions 2026 prices) — [S] vendor blog; length, timing, export, venue tips; licensing figures UNVERIFIED.
[88] Sibling notes — research/games.md — read 2026-10-18 — Minecraft terms (Q7, source [42] there), memorial worlds (Q5), design devices.

**Round 1 additions (research notes, follow-up, 2026-10-18)**
[90] Cloudflare — Zero Trust plans page — https://www.cloudflare.com/plans/zero-trust-services/ — [P][V] HTTP 200; no plan table in the served HTML.
[91] Cloudflare Docs — Set up Cloudflare Zero Trust — https://developers.cloudflare.com/cloudflare-one/setup/ — dateModified 2026-10-12 — [P] Free plan still needs payment details.
[92] Mojang/Microsoft — Minecraft Usage Guidelines (dated excerpt) — https://www.minecraft.net/en-us/usage-guidelines — [P] HTTP 200 over HTTP/1.1 at about 05:16 GMT; excerpt saved in research/sources/minecraft-usage-guidelines-2026-10-18.txt.
[93] Library of Congress — Care, Handling, and Storage of Audio Visual Materials — https://www.loc.gov/preservation/care/record.html — undated — [P].
[95] PyPI — OpenTimelineIO adapter packages — https://pypi.org/pypi/otio-kdenlive-adapter/json ; https://pypi.org/pypi/otio-mlt-adapter/json ; https://pypi.org/pypi/otio-cmx3600-adapter/json — [P] names, versions, homepages; installed and run in the container.
[96] FilmCraft README at v0.8.0 — https://raw.githubusercontent.com/storytold/filmcraft/v0.8.0/README.md — [P] CLI, captions, interchange.
[97] FilmCraft docs/project-files.md at v0.8.0 — https://raw.githubusercontent.com/storytold/filmcraft/v0.8.0/docs/project-files.md — [P] .fcproj is UTF-8 JSON.
[99] FilmCraft Linux CLI release asset v0.8.0 — https://github.com/storytold/filmcraft/releases/download/v0.8.0/filmcraft-0.8.0-linux-x86_64.tar.gz — [P][RUN] SHA-256 b166877905ae8a1b5505066d6dde60d7ce05831cfb309bacd5d7970f4bb017e1.
[100] Microsoft Learn — Get-FileHash (Windows PowerShell 5.1) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-5.1 — updated 2025-03-24 — [P].
[102] Microsoft Learn — about_Character_Encoding (5.1) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1 — updated 2025-09-29 — [P] > and Out-File write UTF-16LE.
[105] BBC — Subtitle Guidelines, version 1.2.5, March 2026 — https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles — [P] 160-180 wpm; line height 7-8% of picture height.
[107] DCMP — Captioning Key, Presentation Rate — https://dcmp.org/learn/601-captioning-key---presentation-rate — [P] 130, 140 and 160 wpm by level.
[110] Verbatim America — Blu-ray and M-DISC product pages — https://www.verbatim.com/en/blu-ray ; https://www.verbatim.com/en/m-disc/products/43825-m-disc-bd-r-25gb-4x-limited-archival-10pk — [P] catalogue entries; no prices shown.

## Changelog

- **2026-10-18, v0.1.** First draft by the Haiku scribe, from `research/format.md` (the researcher's notes, same date) and `CHARTER.md`. The scribe recomputed the decision-matrix totals and sensitivity tests from the scores. They match the notes, except one rounding difference: the film under "room and access halved" recomputes to 4.18, and the notes say 4.17. The ranking is unchanged. Superseded by v0.2 (now 4.50 under both).
- **2026-10-18, flags for the maker.** Three conflicts with the charter: (1) the film default against "partly playable" (Decision 2); (2) showing hard chapters to the subject first, against the surprise (Decision 6); (3) recording voices in weeks 1 to 3, against "gather only after the pipeline is locked" (Step 3).
- **2026-10-18, gaps.** Open gaps are marked TODO(research) in the text and listed under "What the research could not settle."
- **2026-10-18, v0.2, Fable round 1 applied.** Surprise propagated: hard chapters go to the proxy (the maker, per the charter, not a relative), voices in surprise mode replace "her real voice" in Step 7 and F-0, and who is brought in is OPEN (maker). Agent-generability and texture capacity added to the matrix (film 4.55, companion 4.40, hybrid 3.80, explorable 2.45-2.95). Cloudflare 50-user figure and YouTube Private lean restated. Holidays in weeks 10-11 with Step 11 from 2027-01-03; "pipeline locked" defined; Decision 7 rewritten as the chapter count; hashing, caption speed, Minecraft terms and the FilmCraft route closed from the round-1 follow-up; URL for [10] updated.
- **2026-10-18, v0.3, Fable round 2 applied.** Public premiere and Principle 7 propagated (Decisions 3, 8 and 12, Steps 7, 8 and 13); G9 pass condition rewritten and its TODO closed, with interlude timing aligned (Exercise 4 and the second interlude after G13); G13 moved to Sunday 2027-01-17; budget restated as 16 production weeks (about 160 h at 10 h/week) with runtime arithmetic in Decision 7; private copies kept off shared family cloud libraries; Cloudflare 50-user limit confirmed on the product page; consistency sweep (Decision 4 settled, five sensitivity tests, look test, FilmCraft Windows caveat).
