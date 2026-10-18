# Life-Story Craft: Gathering and Shaping a 50+ Year Life

*Track: story · Version 0.3 (draft; Fable rounds 1 and 2 applied) · Written 2026-10-18 · Built from `research/story.md` (researcher notes, 2026-10-18) and `CHARTER.md`.*

*Reading key: [17] points to a source in the Sources list at the end. "(inference)" marks our own suggestion, not something a source says. "UNVERIFIED" means we could not confirm a fact from a source we opened. "snippet only" means we saw the source in search results but did not open it. "TODO(research)" marks a gap that still needs filling.*

## Why this matters for our life journey

The piece is only as true as the material under it. Your mother's real voice, real places, the objects she kept and the turning points she lived through carry the story. The software comes second (charter, principle 1).

Most of what makes a life feel like a life is not on the list of big events. It is the kitchen table, a saying that got repeated, a song in the car. The research calls this *texture*. Milestones give the skeleton. Texture is where the life actually lives (charter, principle 3).

Three facts from the charter shape every step here. First, this is a surprise. She does not know, so she cannot be asked directly, and most of the gathering goes through relatives, friends, documents and objects. Second, only the maker knows about the project. Relatives and friends can still be sources through low-key asks that do not reveal it, unless the maker later decides to bring someone in (charter, Known facts). Third, some of the story is hard, so the maker acts as her proxy for those chapters, with the Fable advisor flagging anything sensitive (charter, principle 5). The premiere is at a mostly public gathering, which Decision 3 sets out.

This playbook covers how to gather that material and shape it into something that holds together. It does not cover animation, games or the software. Those are other tracks.

## Core principles

1. **Her life, in the words of the people who lived it.** Quote exactly. Nobody, human or AI, rewrites someone's speech or puts words in their mouth (charter, principle 4; notes, Pitfalls 3).
2. **Texture before résumé.** Ask about a Tuesday morning, a smell, a saying, a Sunday. Job titles and achievements get rebuilt as scenes or cut. [1][3]
3. **Ask for a scene, not a summary.** "Tell me about one time..." gets more than "What was she like?" [3][36]
4. **Sample, don't exhaust.** A life has thirty or more milestones. Pick the few that change the story, give some a glimpse, and leave the rest as a line. Strachey called "a brevity which excludes everything that is redundant and nothing that is significant" the first duty of a biographer [48]. Woolf set the vivid "moments of being" against the "nondescript cotton wool" of ordinary days [49]. Texture is that cotton wool, made visible as a pattern.
5. **Keep conflicting versions apart.** Relatives remember the same event differently. Store each version as its own row with a confidence grade. Do not average them [55][64].
6. **Silence is part of the method.** Ask one question, then wait. Do not correct the narrator in the room. Check facts afterwards [10][36].
7. **Real memories stay real.** AI may restore, restyle, animate and connect real photos and stories. It may not invent events or people. Every reconstruction is visibly marked as one. The Rauch brothers visited their storytellers, gathered family photos and photographed landmarks before they animated, and said "there is some imagining we have to do along the way" [24][26].
8. **Hard chapters need a gate, not a feeling.** Sort material into three drawers. Top: freely shared. Middle: shared inside a trusting relationship. Bottom: family secrets and trauma, never asked for [34]. In StoryCorps' short *Danny & Annie*, the couple set up two rituals first, then tell the hard chapter in their own words [20][21]. (Our reading. We did not watch the animation, so its visual choices are UNVERIFIED.)

## How to do it, step by step

**The gate comes first, and it splits gathering in two.** The charter says real photos and stories are gathered only after the pipeline and process are locked, and the Learn phase runs to about mid-November (Fable round-1 review, C1). Gathering has two tracks:

- **Track A, locate and protect (starts now; no recording).** Make the relative list, oldest first, with age, health, hearing, distance and language. List the documents and where they physically are. Make the found-voice list (her voicemails, tapes, home video, clips on relatives' phones), because phones get replaced and this is the only route to her own voice in surprise mode. Write the consent script. Run the practice exercises. Nothing in Track A records a real person, and copying an existing file (Step 4) does not touch the gate.
- **Track B, recorded sessions (behind the gate).** No recorded session with a real person until the gate is passed. The maker sets the gate date in writing (Decision 11). Reasons to pull it earlier are named in advance: a relative in Door A (Step 6), a serious illness, or a relative who is only in town at Christmas. Pulling it early is the maker's written decision, and the Fable advisor reviews it.

Practice tests with your own voice, or with a friend who agrees to practise, are fine before the gate.

**Step 1. Confirm the mode and the proxy.** Write down the mode the charter sets: a surprise. The proxy for hard chapters is the maker (charter, principle 5). A relative second check is optional, and counts as bringing that person in. See Decisions 1 and 2.

**Step 2. Set up the recording.** Use a quiet room with soft things in it: rugs, curtains, cushions. Turn off the fridge and any chiming clocks if you can [10][37]. Put the phone on Do Not Disturb and plug it in. Stand it on a table, a stand or a folded cloth, not in your hand. For one speaker, 5 to 6 inches from the mouth [37], or 6 to 12 inches [89]. For two speakers no source gives a distance: the layout is inference, and Exercise 2 settles it. A table keeps handling noise off the recording [37]. Use lossless recording (iPhone: Settings > Voice Memos > Audio Quality > Lossless) or at least 128 kbps on Android [37]. Run a second phone as a backup [10].

**Step 3. Set up local transcription.** Keep private audio on your own computer. Two free options are OpenAI's Whisper (MIT licence; install with `pip install -U openai-whisper`; needs ffmpeg) [39], and whisper.cpp (MIT licence; runs on the CPU; takes 16-bit WAV) [40]. Test both on one recording before you rely on either (Exercise 3). Which one fits depends on your PC. With an NVIDIA graphics card that has about 6 GB of video memory, Whisper's `turbo` model is the simplest route (inference from the research notes' Q1 table) [39]. Without one, whisper.cpp on the CPU is the likely fit [40]. The notes' published timings put `small` on a fast desktop CPU at about 1.5 minutes per 10 minutes of audio; a slow CPU can take several times longer (our own slow-CPU bracket with faster-whisper was about nine minutes [100]). Prebuilt Windows builds of whisper.cpp were not confirmed [83]. Cloud transcription is not an option without the maker's explicit say (charter). TODO(research): accuracy on older voices, accents and non-English speech is untested.

**Step 4. Build the inventory sheet.** Use one table, saved as CSV so any spreadsheet app opens it. It has two kinds of row. A `milestone` is a one-off event. A `texture` row is a repeated pattern: a routine, a meal, a saying, a car, the kitchen table. The full column list is in `skills/life-story-interviewing/inventory-rules.md`, and the CSV template is `inventory-template.csv` beside it. Four rules matter most:

- Every row has a source code: `S` subject, `R` relative, `D` document, `O` object, `P` photo, `V` found voice (existing audio or video of her). Name the person or item, and add a timestamp such as `@00:14:30`. No source, no row.
- Every texture row has one concrete sensory detail: a smell, a sound, a texture, a taste or a light.
- Every row has a confidence grade. **A**: a dated original record, and at least one person agrees. **B**: two or more independent people agree, with no record. **C**: one first-hand memory. **D**: second-hand, a family legend, or conflicting accounts. The grades follow standard genealogy practice [79] (snippet only).
- Every row has a consent status, an `allowed_use` and a drawer. Consent values: `asked-ok`, `asked-ok-with-limits`, `not-asked (surprise hold)`, `declined`, `third-party-needs-check`, `bottom-drawer (do not use)`. `allowed_use` is the widest screening the person has agreed to: `hall`, `private-link`, `family-only` or `none` (`inventory-rules.md`).

**Found voice is a source class of its own (Track A).** In surprise mode it is the only route to her own voice, and phones get replaced, so start the list now. Her voicemails, answering-machine tapes, home video and clips on relatives' phones are where her voice may be. Ask each relative, as an ordinary family request (Tier 1, Step 8): "Do you have any video or voice message of her on your phone? Please don't delete anything." Ask them not to forward it or post it: they should just tell you what exists and roughly when it was made. For each item, record who holds it, the device or format, a rough date, who speaks, the length, the quality, whether the original is in hand, and the consent status of everyone heard. Copy each original as soon as the relative agrees, by cable or direct transfer, never through a chat app, and never edit it [38]. The file plan is in `skills/life-story-interviewing/surprise-runbook.md` (Found voice). Found voice may be restored and used as itself. It may not be extended or imitated (Decision 10).

**Step 5. Choose the vertical-slice chapter.** Pick one chapter from one life stage that you can make in full. Every method in this playbook gets tested on it first. The charter asks for one great chapter before expansion (charter, principle 6).

**Step 6. Plan the order.** List the relatives oldest first, since their memories and their time are the most at risk (inference). Sort each one into a door. **Door A (protect now):** aged 75 or older; a serious or progressive illness or any memory change; a hearing or speech problem that makes a later phone call impractical; or reachable in person only at one gathering before mid-November, or only abroad. **Door B:** everyone else, who waits for the gate. These thresholds are judgement calls (inference). Keep the people tab, with its health notes, private to the maker. The full door rule and people-tab fields are in `skills/life-story-interviewing/surprise-runbook.md`.

Her middle years, roughly 35 to 55, are where the cultural life script expects the fewest positive events. Janssen and Rubin report that few positive events are expected after age 30 (8.4%), that events expected after 35 are rated negative on average, and that about half of the negative and neutral script events (51.7%) fall at 31 or later [47]. This is a pattern across people, not a finding about her (inference). It does not mean those years are empty: the script expects them to be grey. So do not read a thin memory of those years as a thin life. Ask relatives for the ordinary good texture of those years: the routines, the good Sundays, the jokes (`question-bank.md`, R7.1, R7.4 and R7.8). Use a life-history calendar, a grid of years by where she lived, work, relationships and children, to pin down dates. It improves recall in research [67] (snippet only).

**Step 7. Prepare each session.** Choose one life stage and 5 to 10 questions from `skills/life-story-interviewing/question-bank.md`. Choose 1 to 3 prompts and keep the rest in reserve. StoryCorps itself advises 5 to 10 starter questions for a session of about 40 minutes [2]. The prompts, with the evidence we have:

- **Smell.** Memories cued by smell are older, more vivid and more emotional than other memories, but they are rare [41]. Ask "what did it smell like?" in words.
- **Songs.** Music from ages 15 to 30 works best, per [46]. We extend the lower bound to 12 to catch first records (inference). In one older-adult study, about 70% of those songs evoked a memory, against 44% of other songs (as reported in [46]). Use 20 to 30 second clips, and ask "where were you?"
- **Photos.** Pick six, not sixty. Ask what is outside the frame, who took it, and what happened just before and after. Include two photos that are not celebrations, because family photos over-represent celebration [58].
- **Objects and maps.** Ask each relative to bring one object and say where it lived. For a memory map, draw your own childhood street first, then ask them to draw theirs and mark "where something memorable happened" [65] (snippet only).
- **The Tuesday walkthrough.** Ask for one ordinary day, from the alarm to lights out. This adapts Mass-Observation's day diaries, which asked volunteers to record everything they did on 12 May 1937 [50] (snippet only). It fits the middle years best, but no experiment has tested it against other prompts.
- **"I remember" lists.** Ten short fragments in five minutes, with no explanation [52] (snippet only).
- **House tour.** Walking with relatives in their seventies or eighties may not be practical. Do the tour at their kitchen table instead (inference, adapted from the go-along method [44]).

**Step 8. Ask each relative in one of two tiers.** Nobody is briefed about the project by default. Decide the tier for each person.

- **Tier 1: low-key and unrecorded (allowed now; reveals nothing).** Ask the found-voice question (Step 4) as an ordinary family request, for example: "Do you still have that video of Mum from the wedding? Please don't delete it." Ask where the albums and papers are. Stories heard in normal conversation are written up afterwards by the maker as `R` rows with `consent_status = not-asked (surprise hold)`, and are never quoted in the film without later consent. Copying an existing file is also a Tier 1 ask.
- **Tier 2: brought in (only by a written maker decision under Decision 2).** Use the honest script in `skills/life-story-interviewing/surprise-runbook.md`: the piece is a gift; it is a secret from your mother until a set date; it will be shown at a gathering on Feb 27 that is partly public, and may be shared with family afterwards by private link; you can restrict any part; they can skip anything; nothing they say will be used without their OK; please do not mention it to her or to anyone who might. Log a dated `told_on` line and a `scripted_line_if_asked` in the people tab. Then ask the found-voice question (Step 4). Do not invent a cover story. Tell them that remembering can hurt, and let them ask questions first [33]. Keep the pre-talk to logistics and consent. If the story is told before the recorder starts, there is little left to record [11].

**Step 9. Run the session.** Keep it to 45 to 60 minutes, with a break [10][35].

- Open with an easy, present-tense or object question. Go in order at first, then let the relative wander [11].
- Ask one question, then wait. If you need to, count to ten in silence [10].
- Nod. Do not say "uh-huh", because sounds like that show up on the recording [10][11].
- Follow up with "tell me more", "and then what happened?", "what did it look, smell or sound like?", or repeat their last words [3][36].
- Ask for the scene: "Tell me about one time."
- Do not correct. Note contradictions with a timestamp, to check later [10].
- Note unusual names and words, and check the spellings afterwards [10].
- Watch for tiredness: fidgeting, repetition, flat answers. Wrap up [35].
- Optional: some interviewers have the narrator lie down, close their eyes and speak in the present tense, a radio technique the *Flee* director used. Use it only if the relative chooses it (snippet only) [27].

**Step 10. If someone cries or goes quiet.** Stay. Say nothing for a few seconds. Offer a tissue. Say something plain, such as "That's a lot.", not "How do you feel?" [32]. Offer three doors: stay with it, take a break, or move on. Do not change the subject for them [36]. Keep recording unless they ask you to stop, and note the time [32]. Afterwards, ask whether that passage should be kept, restricted or removed [8]. If they seem far away or overwhelmed, stop [32].

**Step 11. Close well.** Ask a reflective question, such as "What was it like to talk about this today?" [5]. Then say the recorder is still running and ask if that is all right, or stop it visibly. Never record someone who believes they are off-tape: that breaks the consent they gave [8]. If they agree, ask the last question, S10.4 ("What have you never been asked that you wish someone would?") or R10.2 ("What do they always do that shows who they are?"). It is the likeliest place for an unguarded remark (inference). Then thank them. Aim to leave them no worse off than when you met them [54].

**Step 12. Within 24 hours.**

- Copy the original to two places. Never edit the original [10][38].
- Name the files by date, person and session, for example `YYYY-MM-DD_relative-name_session01.wav`.
- Make a time-coded index, every five minutes or less, and a list of spellings [10].
- Run the local transcript (Step 3) [39][40].
- Add inventory rows with quotes and timestamps. Put anything hard in its drawer and set its consent status.
- Send a thank-you, and say when they will hear or see what you make [10][32].
- Review. Did they tire? What did you miss? What comes next?

**Step 13. Triage the milestones.** Score each milestone on six tests, then give it one treatment. The method is our own assembly from the notes. It is untested, so test it on the vertical slice (TODO(research)).

| Test | The question | If yes |
|---|---|---|
| Turn | Did it change what she did or believed, or who was around her? | A candidate to dramatise |
| Motif | Does it touch the through-line: a recurring object, place, phrase or tension? | Dramatise or glimpse |
| Scene | Can we render a concrete scene: a place, people, an object, one sensory detail? | Needed for dramatise. Otherwise glimpse or mention. |
| Voice | Do we have her or a relative's own words or sound for it? | Strongly favours dramatise |
| Dignity | Is it middle or bottom drawer? Has the right person said yes? | A gate: no yes, no use |
| Variety | Does the piece already have a scene like this? | Glimpse or merge |

The four treatments:

- **Dramatise:** a scene of 45 to 120 seconds, with a place, people, an object and a sound.
- **Glimpse:** 3 to 10 seconds, one image, one sound or one line of voice.
- **Mention:** a label, a date on a map or a line in a list. A mention layer can carry 15 to 25 milestones cheaply.
- **Hold:** left out for now, on purpose. Not forgotten.

Walter Murch's Rule of Six puts emotion first when cutting, and advises not to give up emotion before story. Secondary sites report this; we did not open the book [56]. Use it as a tie-breaker.

**Step 14. Find the through-line.** Look for four things:

1. What she keeps doing: verbs and objects that recur across interviews and decades.
2. A standing tension: what she wanted, and what got in the way.
3. The same trait, named without prompting by two or more relatives who describe different scenes.
4. Her own chapter titles, if she gives them [5][6].

Write three candidate through-lines. Each is one sentence, with three timestamped quotes and one counter-example. Craft writing on documentaries names the spine and the point of attack as the entry (snippet only) [57]. A song can carry a through-line too. In *Coco*, "Remember Me" is sung four times in different contexts, and means something different each time [77].

**Step 15. Test the through-line.** Run five checks on each candidate.

1. **Own words.** Do the key words appear in the transcripts, not only in our notes?
2. **Independence.** Are there at least two witnesses, with different scenes?
3. **Counter-example.** Find the scene that contradicts it. If you cannot find one, you have not looked hard enough.
4. **Would she say it?** Ask her, if the mode allows. In surprise mode, ask the closest insider: "Does this sound like her? What's missing?" [53]
5. **No default redemption arc.** Many people narrate a move from hardship to gain, and in some studies that pattern is linked to well-being. The evidence is mixed, and it is not a template. Her life may not run that way [7].

**Step 16. Build the beat sheet and check the time budget.** Watch a reference piece with a stopwatch. For each beat, log the time, what happens, the emotion, the recurring image, and what is withheld. Then draw a mood graph, with time across and mood up and down [17]. For a 25-minute piece, the starting budget is in `skills/life-story-interviewing/beat-sheet.md`. It is our heuristic and untested: cold open about 60 seconds; five or six chapters of about 3 minutes, each with one dramatised scene, two or three glimpses, one texture sequence and a chapter card; three "Tuesday" interludes of about 40 seconds; present-day close about 90 seconds; thanks about 60 seconds. Keep the first hard beat no earlier than about a quarter to a third of the way in. This comes from the timing of *Up*'s first blow [17] (inference).

**Step 17. Check consent at each stage, then run the veto window.** Re-confirm consent at the rough cut and again at the lock. In surprise mode, the closest insider sees the piece first. At the reveal, your mother sees it somewhere she can say "stop", and nothing goes beyond that room until she agrees (inference, from the notes' runbook) [8][32].

### Timeline (19 weeks, draft)

These dates come from the researcher's plan, adjusted in round 1 (Fable review, C1). The week numbers in the notes overlap, so use the dates. Track A starts now. Track B waits for the gate, unless the maker pulls the gate earlier for a Door A relative in writing (Decision 11). In surprise mode there are no sessions with your mother: the notes' hybrid and together sessions are dropped.

| Dates | Track A: locate and protect (no recording) | Track B: recorded sessions (only after the gate) |
|---|---|---|
| Oct 18 – Oct 24 | Confirm the mode (surprise, fixed by the charter) and the proxy (the maker, per the charter). Decide whether anyone is brought in; if nobody yet, Track A is Tier 1 only. Start the relative list, oldest first, with age, health, hearing, distance and language. Write the consent script. Test recording and transcription on your own voice (tests, not gathering). | Set the gate date in writing (Decision 11). |
| Oct 25 – Nov 7 | Finish the people tab and the Door A and Door B sort. Start the found-voice list, asking each relative the found-voice question. Do the practice exercises (2, 3, 5, 7). Ask the closest insider the suitability question. | Door A only, and only if the maker has pulled the gate for that relative in writing: one short, audio-only session each, with the consent script. Log and transcribe it. |
| Nov 1 – Dec 12 | Document inventory: where the photos, letters and records physically are. Complete the found-voice list. Copy each original as soon as the relative agrees (Step 4). | Recorded relative interviews after the gate: six to ten at about 45 minutes, some together and some alone. One object, photo or map session. Place visits. |
| Nov 15 – Dec 12 | Draft inventory v1 from documents and found voice. | Inventory v1 from the recorded sessions. Through-line workshop. Pick the vertical-slice chapter. |
| Dec 20 – Jan 2 | Visits to the oldest relatives, one at a time (inference): documents, found-voice copies, the consent script. | Recorded sessions with the oldest relatives in the holiday window, only where the gate has passed for them. Freeze inventory v1. |
| Jan 3 – Feb 6 | Check facts against documents. Corrections and gaps. | Hard-chapter conversations with relatives, under the proxy rule. Second interviews. Consent check at the rough cut. |
| Feb 7 – Feb 20 | Review with the proxy. Veto window. | Lock. |
| Feb 21 – Feb 27 | Final consent confirmations. | Premiere preparation. |

The minimum for full surprise (the operating mode) is 8 to 12 sources, of whom N are brought in, with N starting at the Door A count (Decision 2), plus document work and a found-voice inventory. Documents to look for in the middle years include wall calendars, diaries, address books, school reports, phone camera rolls, receipts, car papers, holiday brochures and work ID photos (the notes' list, marked as inference).

## Learn-by-doing exercises

### Exercise 1: Time a montage (*Up*, "Married Life")

- **Goal.** See how a wordless montage paces joy, routine, loss and recovery.
- **Steps.** (a) Watch the opening on a copy you have legal access to, with a stopwatch. Log time, description, emotion, recurring image and what is withheld, as in Step 16. Compare your times with the student's table [17]. Draw the mood graph. (b) *Danny & Annie*, combined cut, 5:52 (352 s), from the embed `WNfvuJr9164` that StoryCorps' page carries [92]. Fill the 13-row table in `research/story.md`, follow-up round 2, Q6: 10 beats and 3 cards, each cued by its opening words. Watch once with a stopwatch for the time column. Watch again with the table in hand for the on-screen, emotion, recurring-image and withheld columns. That is about 27 seconds a row.
- **Time.** About 2 hours for part (a); about 15 minutes for part (b).
- **What good looks like.** Your times match the big moves to within a few seconds. Check these against [17]: the wedding flash at about 7:03; the first blow, from nursery to clinic, at about 8:20 to 8:30; the window turn at about 9:45 to 10:09; the hospital goodbye at about 10:23 to 10:50; the fade at about 11:08. The montage runs about 4 minutes 5 seconds, and about 77 seconds pass before the first blow [17]. The Ringer says "about four and a half minutes" [14]. You can name the withheld beat (the death is never shown; the cut goes from the hospital to the church steps) and at least three motifs that come back. Treat the timings as approximate. The essay is a student's work (TODO(research): re-time on your own copy). For part (b), your 13 time-in values should rise down the table, and the last card should fall near the end of the 5:52 run.

### Exercise 2: Record a practice conversation

- **Goal.** Find a setup where every word, from the furthest speaker, is clear.
- **Steps.** Pair up with a friend who agrees to practise. Both of you read the same 60-second passage, alternating sentences, with the phone on a folded towel between you, centred, at about 6, 12 and 24 inches from the nearer mouth. Then try one phone each, a few inches from each mouth per [90]; we test at about 6 inches (inference). Say a slate before each take ("test A, 6 inches"). Listen on headphones. Note hiss, echo and any speaker who fades. Write your placement rule. This exercise settles the two-speaker distance, which is inference until then (Step 2).
- **Time.** About 90 minutes.
- **What good looks like.** You can state the placement rule in one sentence, and the backup file plays back as cleanly as the main one.

### Exercise 3: Transcribe one recording on your own computer

- **Goal.** Get one working transcription command on your PC, and measure its speed and its errors.
- **Steps.** First, inventory the PC. In PowerShell, run these and keep the output:

  ```
  Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
  [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)
  Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion
  nvidia-smi --query-gpu=name,memory.total --format=csv
  ```

  Task Manager's GPU tab also shows dedicated video memory, and DxDiag ("dxdiag" in the search box, then Save All Information) is the fallback [85]. Then install Whisper [39] or whisper.cpp [40] by its README. On Windows the Whisper README suggests `choco install ffmpeg` or `scoop install ffmpeg` [39]. If you need to convert audio, the whisper.cpp README gives this example: `ffmpeg -i in.mp3 -ar 16000 -ac 1 -c:a pcm_s16le out.wav` [40]. Set the language explicitly rather than trusting auto-detect (inference; check `whisper --help`). Run it in the family's language, on the hardest voice you have. Time a run on a 10-minute recording. Check ten random lines of the transcript against the audio and count the wrong words. If the language has high error on the Whisper paper's read-speech test (for example Hindi 21.5% and Arabic 16.0% word error for `large-v2` [82]), or the family switches languages mid-sentence, budget a human correction pass for every transcript.
- **Time.** Two to three hours, mostly installation.
- **What good looks like.** You have one command that works, a timed run, and a list of the errors it made. The Windows steps stay untested until you have run them. The Whisper README says the `turbo` model needs about 6 GB of video memory [39]; the PowerShell lines above tell you what your graphics card has. Your PC's speed is a result of this exercise, not an assumption (TODO(research): record it as a project finding).

### Exercise 4: Triage your own milestones

- **Goal.** Practise the six tests on your own life, not hers.
- **Steps.** List fifteen milestones from your own life. Score each on Turn, Motif, Scene, Voice, Dignity and Variety. Give each a treatment: dramatise, glimpse, mention or hold. Write one reason per row, pointing to a test. Compare your list with a friend's.
- **Time.** About 90 minutes.
- **What good looks like.** Every row has a treatment and a reason. No row is "dramatise" without a scene and at least one sensory detail. At least one "hold" has a reason you can defend.

### Exercise 5: Build the inventory sheet

- **Goal.** Fill a CSV with real rows, from your own early childhood or from a family photo you own, and feel the rules.
- **Steps.** Create the CSV with the header in `skills/life-story-interviewing/inventory-template.csv`. Enter six texture rows and two milestone rows. For each, set the source with a timestamp, the confidence grade, and the consent status. Enter one event that you remember in two different ways, as two separate rows.
- **Time.** About 60 minutes.
- **What good looks like.** No row lacks a source. Every texture row has one concrete sensory detail. The two versions of the event are two rows, linked in the notes column, and neither is averaged away.

### Exercise 6: Run a practice session and draft three through-lines

- **Goal.** Run one 45-minute session with the Tuesday walkthrough, then test a through-line against what you heard.
- **Steps.** With the friend from Exercise 2, run the Tuesday walkthrough from `skills/life-story-interviewing/question-bank.md`: "It's a Tuesday in [year]. Start from the alarm, or whatever woke you..." Use silence, "tell me about one time", and no "why" questions. Afterwards, count your "why" questions, your interruptions, and any silence you filled too early. Then write three candidate through-lines from what you heard. Give each three timestamped quotes and one counter-example.
- **Time.** A 45-minute session, plus 90 minutes of review.
- **What good looks like.** Your friend described a specific morning, with at least three sensory details. You waited a full ten seconds at least once. Each through-line has a counter-example you found in the transcript.

### Exercise 7: Dry-run the consent paragraph and the relative script

- **Goal.** Write the consent paragraph and the relative script, then check them for honesty.
- **Steps.** Write a one-paragraph release. It should say what the piece is for, who will see it, and the use in one sentence: "It will be shown at a gathering on Feb 27 that is partly public, and may be shared with family afterwards by private link; you can restrict any part." It should also say that AI tools will transcribe and may help tidy or restyle real photos but will not invent events or voices, that the relative can skip, stop, restrict or withdraw, and until when they can withdraw (`skills/life-story-interviewing/session-protocol.md`, steps 2 and 3, and [8]). Then write the relative script from `skills/life-story-interviewing/surprise-runbook.md`. Give both to a friend who has not read this playbook, and ask them, in their own words, what they would do after reading.
- **Time.** About 60 minutes.
- **What good looks like.** The script contains no cover story that needs your mother to act on camera. It says the relative can skip anything. Your friend can say, in their own words, what happens to the recording and what they can stop.

## Decisions you'll need to make

Each decision lists the options, then our current lean. A lean is a suggestion for you to accept, change or reject.

### 1. Surprise, together, or hybrid

- **Options.**
  - *Full surprise:* she knows nothing. Gathering is covert, through relatives, documents and objects.
  - *Hybrid ("consent-light"):* she knows a project exists and gives two or three story sessions. The form and the content stay secret.
  - *Together:* she knows everything and takes part in the telling.
- **Our current lean: full surprise.** The charter records it as a known fact: she does not know, and all gathering is covert. The research notes recommend the hybrid, because her own voice and her consent for hard chapters are the strongest assets, and surprise cannot provide them. That is a fair point. But the hybrid means telling her that a project exists, which changes a fact the charter already sets. We are not adopting it. If you decide to change that fact, use the hybrid column in the notes and ask the Fable advisor to re-check the plan.
- **The cost of full surprise.** It needs more relatives and more checking. It also carries the highest risk that she will dislike being the centre of attention. The notes cite a live programme where the subject walked away [30].
- Resolved in round 1: the notes now carry a dated addendum, and their mode table puts full surprise first. Re-check the hybrid only if the maker reopens the decision.

### 2. Whom to bring in, if anyone, and when

- **The proxy.** The maker, per the charter (principle 5). The Fable advisor flags anything sensitive. A relative second check is optional, and counts as bringing that person in.
- **Options** (research Q1, options A to D).
  - *A. Nobody yet:* Tier 1 asks only. No recorded relative voice in the film, and no relative second check.
  - *B. One person, a Door A relative:* told the purpose, and recorded once, before the gate.
  - *C. Door A relatives only,* each told and logged; Door B waits for the gate.
  - *D. A helper who is not a narrator,* to find albums and tapes only. A leak path with no recording benefit.
- **The trade-off.** Zero brought in means no recorded relative voice in the film, and no relative second check. Each person brought in adds a recorded voice and a second check, and a leak path for the whole 19 weeks (research Q1, rule 5). Door A relatives are the natural first candidates; the order is in research Q1.
- **Our current lean: not chosen (charter open decision: "whether to bring anyone else in later").** Until the maker decides, Track A runs as Tier 1 only, and nobody is recorded (Step 8). Any first person brought in gets a written maker decision, reviewed by the Fable advisor like a gate pull, with the Door A reason, what they were told, the scripted line and who must not be told. A suggested test for that person is to pick the one who knows her best and whom she would trust with a hard story. Ask them early: "Would she love this or hate this? Has she ever said?" [30] Keep the circle as small as the work allows. Use a neutral project name, one shared folder and no group chats [28][29].
- **Note.** Wherever the playbook, the skill or the runbook says "the closest insider" (playbook Steps 15 and 17 and the Oct 25 timeline row; SKILL steps 19 and 21; runbook Gates 0 and 5; `beat-sheet.md`), it means a person brought in under this decision. TODO(advisor): round 3 to decide whether those lines are rephrased while nobody is brought in.

### 3. Occasion, venue, and whether it is public

- **Known fact (charter, Known facts, updated Oct 18, 2026).** A premiere at a mostly public gathering on Saturday, Feb 27, 2027. Treat it as a film with a public audience, not a family slideshow. Every cue is cleared for public screening or cut (charter, principle 7). A cue that cannot be cleared is cut, not quietly kept.
- **Open for the maker.** (a) The country or jurisdiction of the premiere, which sets the music and image rights (charter open decision; research Q4 and Q7). (b) The venue type: a licensed hall or a private room (research Q4). (c) Whether a private link follows the gathering. The relative script already says the piece may be shared with family by private link, so any consent given must cover it. (d) Whether Feb 27 is her birthday.
- **Our current lean.** None is needed on whether it is public: it is. A public screening needs music rights [70]. TODO(research): the music rights for a public premiere depend on the jurisdiction and are not resolved (research Q7).

### 4. Format

- **Options.** Film, explorable world, scroll story, or a hybrid (charter open).
- **Our current lean: none from this track.** The story track decides what goes in, not how it is shown. Whatever format you choose, lead with the voice. Design the visuals around the strongest recordings, not the other way round. The *Flee* team edited a master assembly of sound and storyboards before animating [26].

### 5. Chapter structure

- **Options.**
  - A: five to seven chapters, titled in her words, each opening on a texture beat and ending on a turn [5][6].
  - B: one ordinary Tuesday, shown at several ages, broken by three or four turning points [17].
  - C: rooms of a house, with objects showing the years. Life-story work with older people can also be built around themes rather than a timeline (snippet only) [35].
- **Our current lean: none yet.** Test all three on the vertical-slice chapter (inference). Then pick the one in which her voice carries the scene best.

### 6. Which hard chapters exist, and who may speak to them

- **Options.** Leave the chapter out. Mention it in one neutral line. Tell it in full, in the words of the people who lived it.
- **Our current lean: none chosen (charter open).** Use the drawers. Top: freely shared. Middle: only with the proxy's say. Bottom: never asked for [34]. For any chapter you do tell, be brief. Name the hard fact in a line or two, and give the time to who she was. *Up* gives its central loss about ten seconds, then moves on [17].

### 7. Language and audience

- **Options.** One language, or several. A family of all ages, or adults only. Gamers, or not.
- **Our current lean: none chosen (charter open).** Keep in mind that transcription accuracy in other languages, and on older voices, is untested (TODO(research)).

### 8. Phone only, or an external microphone

- **Options.** A phone with a backup phone. A clip-on (lavalier) microphone. A phone with an external microphone.
- **Our current lean: a phone, with a backup phone.** Guides call an external microphone the biggest single upgrade [73] (snippet only). Decide after Exercise 2. Model recommendations are UNVERIFIED.

### 9. Where transcription runs

- **Options.** On your own computer (Whisper or whisper.cpp). Or a cloud service.
- **Our current lean: on your own computer.** Private audio then stays with you (inference). The charter says nothing personal goes to a third-party service without your explicit say. Do not use the StoryCorps app or archive for private family material. Its terms give StoryCorps a perpetual licence, and say private interviews "may still be retained" [4].

### 10. Consent for AI processing of voices and photos

- **Options.** Tell each narrator that AI is used, and get their agreement. Or do not mention it. For voices: no synthetic voice at all, or voice cloning only with explicit agreement.
- **Our current lean.** Tell every narrator, in the pre-talk, that AI tools will transcribe and may help tidy and restyle real photos, and that the tools will not invent events or voices. No synthetic voice of any real person, living or dead, even with their consent: no cloned voice and no voice generated to sound like someone. This is stricter than "unless that person explicitly agrees". The charter's principle 4 says "no cloned voices", and the charter review sharpens it to cover any synthetic voice and consent (`reviews/00-charter-review.md`, Principle 4), because an audience cannot tell consent from fakery and the piece will outlive its context (inference).
- **Open charter decision for the maker:** whether consent could ever permit a synthetic voice of a real person in the piece. Until the maker decides, the lean above stands.
- TODO(research): the legal position is unresolved. This is not legal advice.

### 11. When the gate for recorded sessions opens

- **Options.** One fixed gate date, which the maker sets in writing. Or a separate, earlier date for a relative whose situation requires it (Door A).
- **Our current lean: not chosen; the maker sets the date.** The Learn phase runs to about mid-November (`reviews/story-round1.md`, C1). If the maker has no reason to decide otherwise, the end of week 4, Saturday 2026-11-14, is a reasonable latest date (inference). Reasons to pull it earlier, named in advance: a Door A relative; a serious illness; a relative who is only in town at Christmas. Any early pull is the maker's written decision, and the Fable advisor reviews it.

## Pitfalls

1. **Treating the McAdams interview as a script.** It is a research instrument. Her chapters can stand even if they never resolve [6][7].
2. **Turning a gift into therapy, or therapy into entertainment.** Life-review work has care rules: do not push, and let people stop [34][35]. We are making a gift, not providing care. If someone is in serious distress, stop and get appropriate help (inference). The evidence for reminiscence work is mixed. A 2023 meta-analysis of 37 trials reports better quality of life and life satisfaction, with very high variation and signs of publication bias [42]. The Cochrane review of reminiscence for dementia reports small, inconsistent effects (snippet only) [43].
3. **Rewriting speech.** Quote exactly. Do not tidy someone's words into a better sentence. The Oral History Association asks interviewers to keep "the integrity of the narrator's perspective" [8].
4. **Cold-contacting a relative with a difficult history.** Check with the insider first. A reported 1996 case, in which a planned edition was pulled after researchers contacted a relative, shows the risk. The report's other claims are reported, not verified [30].
5. **Asking for bottom-drawer material.** Secrets, trauma and the cause of an estrangement are never asked for. If one is volunteered, log it as "bottom-drawer (do not use)" and move on [34].
6. **Leaks.** Documented in the *This Is Your Life* record. A six-year-old grandson revealed the plan at lunch. A note with a phone number was found, and a programme was shelved for more than a decade [28]. In our case, the likely leak paths are children, shared devices, group chats and shared cloud photo libraries (charter). Keep the project name off paper, and use a neutral folder (inference).
7. **Cover stories that make the subject act on camera.** In 1961, a surprise on live television used a false pretext and failed. The subject walked away [30]. Use the honest script instead (Step 8).
8. **Treating distress as footage.** Do not use tears or anger as material. Ask before using any emotional moment [32].
9. **Treating memory as a record.** Family legends harden. Keep the confidence grade, and a list of "ten things only she can confirm" for a corrections round (inference) [55][64].
10. **Photo bias.** Family snapshots favour celebration and under-represent sorrow and routine [58]. Ask relatives for ordinary photos: a car, a kitchen, a corner shop.
11. **Long, tired sessions.** Keep to 45 to 60 minutes, with a break. For narrators with memory difficulties, the notes suggest 30 to 45 minutes [35]. Some people find emotional memories exhausting, and may need to end a session early (snippet only) [76].
12. **Over-fitting to Pixar.** *Up* was made by a large team over years, with test screenings [14]. Borrow its rules, not its scale.
13. **Music rights.** Unresolved for the public premiere; the answer depends on the jurisdiction (Decision 3). Every cue is cleared for public screening or cut (charter, principle 7). Platform takedown behaviour is UNVERIFIED [70].
14. **AI on real memories.** No invented events, faces or voices. Mark every reconstruction.

### Things we have not checked yet

- **No prompt test for people over 50.** No experiment compares prompt types for narrators in this age range. Our ranking of prompts comes from small studies, practitioner guides and judgement [41][46].
- **No survey of family-tribute failures.** The failure list in the notes is our synthesis from vendor guides, oral-history manuals and memoir-ethics writing [70][71].
- **Our own method.** The milestone tests, the time budget and the through-line checks are our own assembly. Test them on the vertical slice.
- **Timings.** The *Up* timings come from a student essay. Re-time them on your own copy (TODO(research)).
- **Tools on your PC.** Whisper speed and accuracy on your PC, with older voices and non-English speech, are untested. Prebuilt Windows builds of whisper.cpp were not confirmed [83], so the build route is the likeliest hard step for a learner (inference) (TODO(research)).
- **Legal.** Reuse terms for the StoryCorps question lists, the Dignity Therapy and McAdams wording, music rights, and consent for AI processing are unresolved (TODO(research)). This is not legal advice.
- **Sources not opened.** Several primary sources were not opened. The McAdams interview page returned a 404, and the Library of Congress field kit returned a 403. Where a source is marked "snippet only", treat its claim as unconfirmed.
- **Craft texts.** We did not retrieve craft texts by biographers (Lee, Holmes, Hamilton, Caro). We have only Strachey and Woolf commentary (TODO(research)).
- **Danny & Annie.** Combined cut 5:52 (352 s), from the YouTube page metadata of the embed `WNfvuJr9164` carried by [92], seen 2026-10-18 by the Fable advisor; visual beats still UNVERIFIED. We did not watch the animation. The maker's table is Exercise 1, part (b). Swap date: Saturday 2026-11-14 (the gate). If the table is still empty that day, replace Exemplar 2 in the research notes with one of the other StoryCorps animated shorts whose durations are listed on [92] (3:21, 1:47, 3:23), and record the swap in a dated line here.

## Best references

1. **Baylor University Institute for Oral History, *Introduction to Oral History* (2016).** https://www.thetexasfreedomcoloniesproject.com/wp-content/uploads/2022/07/Intro_manual_2016.pdf. A practical manual on setup, silence, indexing and preservation. It is a third-party copy, and the notes record permission to duplicate it for educational purposes [10].
2. **Oral History Association, *Principles and Best Practices: Best Practices*.** https://oralhistory.org/wp-content/uploads/2025/12/2025-OHA-PrinciplesBP_Best-Practices.pdf. Consent, narrator approval, slates and releases. Read it before the first session [8].
3. **StoryCorps, "Tips for a Great Conversation".** https://storycorps.org/?p=99902. Ten short tips, including sensory detail and the reflective close. The quickest useful read [3].
4. **University of Dayton Libraries, "Oral history recording: phone tips".** https://libguides.udayton.edu/oral-history-recording/phone-tips. Phone settings, placement and room choice. Use it for Step 2 [37].
5. **Dart Center (GCJT), "Interviewing in the aftermath of trauma".** https://gcjt.org/resources/interviewing-aftermath-trauma. What to do when someone is upset, and how to keep control of the interview. Read it before any hard chapter [32].
6. **McKeown, Ryan, Ingleton and Clarke (2015), "'You have to be mindful of whose story it is'".** https://eprints.whiterose.ac.uk/96489/8/WRRO_96489.pdf. The chest-of-drawers sorting, and a case where private disclosures were kept out of the book [34].
7. **Wozny, "Creating an emotional impact without dialogue: the case study of Pixar's Up" (student journal).** https://studentjournals.shu.ac.uk/index.php/enquiry/article/download/125/125/398. A timecoded beat table for the *Up* montage. Its timings are approximate, so check them yourself [17].
8. **The Ringer, "Pixar's Up first ten minutes" making-of.** https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of. Pete Docter on overwriting, cutting dialogue, and "every shot is a setup" [14].

Tool READMEs are linked from Step 3: Whisper [39] and whisper.cpp [40].

## Sources


- [1] StoryCorps, "Great Questions" — https://storycorps.org/participate/great-questions/ — undated; fetched — full question lists by theme; no licence text; "use the ones you like".
- [2] StoryCorps Help Center, "How will I know what questions to ask?" — https://support.storycorps.org/help-center/how-will-i-know-what-questions-to-ask-does-storycorps-have-suggested-questions-for-my-interview — undated; fetched — 40-minute limit; 5-10 starter questions.
- [3] StoryCorps, "Tips for a Great Conversation" — https://storycorps.org/?p=99902 — undated; fetched — ten tips incl. sensory details, context, reflective close.
- [4] StoryCorps Archive, Terms of Use — https://archive.storycorps.org/?p=35 — last modified 2023-09-14; fetched — licence and retention terms.
- [5] Adapted McAdams Life Story Interview scheme, supplementary file to a Cambridge *Ageing & Society* article (ID S0144686X23000715; PDF author per metadata: Lise Switsers) — https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0144686X23000715/resource/name/S0144686X23000715sup001.pdf — file dated 2023-09-25; fetched — chapters, high/low points, pride/motto, next chapter, reflection; cites McAdams (2008).
- [6] Northwestern Magazine, "So, What's Your Story?" (sidebar to the Winter 2005 feature on redemption) — https://www.northwestern.edu/magazine/winter2005/feature/redemption/sidebar1.html — 2005; fetched — lay version of the LSI: chapters, eight key scenes, challenge, characters, future, theme.
- [7] McAdams, D. P. and McLean, K. C., "Narrative Identity", *Current Directions in Psychological Science* — https://journals.sagepub.com/doi/10.1177/0963721413475622 — 2013; snippet only (abstract) — redemptive meaning linked with better well-being; causation open.
- [8] Oral History Association, *Principles and Best Practices: Best Practices* — https://oralhistory.org/wp-content/uploads/2025/12/2025-OHA-PrinciplesBP_Best-Practices.pdf — adopted Oct 2018; 2025 reprint; fetched via PDF — consent, narrator approval, slate, release, preservation.
- [10] Baylor University Institute for Oral History, *Introduction to Oral History* — https://www.thetexasfreedomcoloniesproject.com/wp-content/uploads/2022/07/Intro_manual_2016.pdf — 2016; fetched via PDF (third-party copy; permission to duplicate for educational purposes) — questions, setup, recorders, indexing, preservation.
- [11] GVSU Veterans History Project, "Guidelines and Instructions for Interviewers" — https://www.gvsu.edu/cms5/asset/62fbfafc-9845-4bc5-b57e-72b3bd7c1c85/27d58c55-78ac-460d-897a-41fe4221f295/veterans_history_project_interview_instructions.pdf — PDF metadata 2026-07-31; fetched via PDF — pre-interview, camera placement, length, upset narrators.
- [14] The Ringer, Pixar's *Up* first ten minutes, making-of — https://www.theringer.com/movies/2022/6/14/23166006/up-first-10-minutes-making-of — 2022-06-14; fetched — Docter on overwriting, dialogue removal, "every shot is a setup", about 4.5 minutes, camera moves.
- [17] Wozny, M., "Creating an emotional impact without dialogue: the case study of Pixar's Up", *Enquiry* (Sheffield Hallam University student journal) — https://studentjournals.shu.ac.uk/index.php/enquiry/article/download/125/125/398 — undated (cites a 2014 access date); fetched via PDF — timecoded Appendix 1; mood graph; motifs. A student essay: treat timings as approximate.
- [20] StoryCorps, "Danny & Annie" animation page — https://storycorps.org/?p=20626 — published 2012-08-12, modified 2024-10-01; fetched — summary, dates, Annie's daily letters.
- [21] StoryCorps, transcript of Danny and Annie Perasa (2004 interview) — https://storycorps.org/?p=14587 — fetched (summary of transcript) — beats 1-10.
- [24] Documentary Association, "Meet DocuWeeks Filmmakers Mike and Tim Rauch" — https://www.documentary.org/online-feature/meet-docuweeks-filmmakers-mike-and-tim-rauch-storycorps-animated-shorts — 2012; fetched — process: visit storytellers, family photos, landmarks, After Effects.
- [26] Documentary Association feature on *Flee* — https://documentary.org/node/36985 — undated; fetched — interview method, anonymity, audio-first assembly.
- [27] NPR transcript of an interview with *Flee* director Jonas Poher Rasmussen — https://www.npr.org/transcripts/1061483678 — undated; fetch returned 503; snippet only (via search) — lying down, eyes closed, present tense.
- [28] Big Red Book, "Behind the scenes" — https://www.bigredbook.info/behind_the_scenes.html — undated; fetched — feeza, codenames, leaks, refusals.
- [29] Big Red Book article on Eamonn Andrews (search title "The secret life of Eamonn Andrews") — https://www.bigredbook.info/article13.03.html — undated; fetched — code names, shredding, near-misses; the page flags one account of Andrews' 1955 surprise as incorrect.
- [30] Wikipedia, "This Is Your Life (British TV series)" — https://en.wikipedia.org/wiki/This_Is_Your_Life_(British_TV_series) — fetched — Blanchflower 1961, Barker, Lipman, Davison, Mullard (reported).
- [32] Dart Center (GCJT), "Interviewing in the aftermath of trauma" — https://gcjt.org/resources/interviewing-aftermath-trauma — undated; fetched — before/during/after tips, distress, control, review.
- [33] Poynter, "5 tips for interviewing people who've been through trauma" — https://www.poynter.org/reporting-editing/2014/5-tips-for-interviewing-people-whove-been-through-trauma/ — 2014-08-14; fetched — pre-talk about the pain of remembering (Ochberg).
- [34] McKeown, J., Ryan, T., Ingleton, C. and Clarke, A., "'You have to be mindful of whose story it is'", *Dementia* 14(2) — https://eprints.whiterose.ac.uk/96489/8/WRRO_96489.pdf — 2015; fetched via PDF — private disclosures; Brooker's chest of drawers.
- [35] Storii, "Tips for Doing Life Story Work With Someone Who Has Dementia" — https://storii.com/blog/tips-for-doing-life-story-work-with-someone-who-has-dementia — undated; fetched — 30-45 minute sessions, prompts, fatigue (vendor).
- [36] Institute of Southern Jewish Life, "Oral History: Technique" — https://www.isjl.org/oral-history-guide---technique.html — undated; fetched — specific questions, silence, handling emotion.
- [37] University of Dayton Libraries, "Oral history recording: phone tips" — https://libguides.udayton.edu/oral-history-recording/phone-tips — undated; fetched — phone settings, placement, room.
- [38] Library of Congress, Personal Digital Archiving: audio — https://www.digitalpreservation.gov/personalarchiving/audio.html — undated; fetched — two copies, yearly checks.
- [39] OpenAI Whisper README — https://github.com/openai/whisper — fetched 2026-10-18 — MIT, install, CLI, models.
- [40] whisper.cpp README — https://github.com/ggml-org/whisper.cpp — fetched 2026-10-18 — MIT, CPU/Apple Silicon, WAV requirement.
- [41] Larsson, M., Willander, J., Karlsson, K. and Arshamian, A., "Olfactory LOVER", *Frontiers in Psychology* — https://www.frontiersin.org/articles/10.3389/fpsyg.2014.00312/full — 2014; fetched — odour-evoked memories: limbic, old, vivid, emotional, rare.
- [42] Zhong, Q., Chen, C. and Chen, S., meta-analysis of life review and reminiscence therapy, *Behavioral Sciences* 13(10):830 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10603902/ — 2023; fetched — 37 RCTs, effects, heterogeneity.
- [43] Woods et al., Cochrane review, reminiscence therapy for dementia (2018 update) — https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD001120.pub3/pdf/CDSR/CD001120/CD001120_abstract.pdf — 2018; fetch returned 403; snippet only — small, inconsistent effects.
- [44] Kusenbach, M., "Street Phenomenology: The go-along as ethnographic research tool", *Ethnography* 4(3) — https://www.citedrive.com/en/discovery/street-phenomenology — 2003; fetched (abstract page) — five themes.
- [46] Martinez-Saez, M. C. et al., songs from the reminiscence bump as autobiographical memory cues in aging (EEG), *Frontiers in Neuroscience* 17 — https://frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1300751/full — 2024; fetched (introduction) — bump songs evoke memories: about 70% vs 44% (López-Cano et al., 2020).
- [47] Janssen, S. M. J. and Rubin, D. C., "Age effects in cultural life scripts", *Applied Cognitive Psychology* — https://pmc.ncbi.nlm.nih.gov/articles/PMC3972131 — 2010; fetched — life-script content across ages.
- [48] Strachey, L., *Eminent Victorians*, Preface (1918) — https://standardebooks.org/ebooks/lytton-strachey/eminent-victorians/text/single-page — 1918; fetched — brevity; the bucket image.
- [49] Urquhart, N. L., "Moments of Being in Virginia Woolf's Fiction" (quoting Woolf's "A Sketch of the Past") — https://writing.colostate.edu/gallery/matrix/urquhart.htm — undated; fetched — moments of being / non-being / cotton wool.
- [50] Mass-Observation Day Surveys (University of Sussex; Mass Observation Archive) — https://www.sussex.ac.uk/library/special-collections/mass-obs-search/day-surveys and https://massobs.org.uk/the-archive/12th-may — undated; snippet only — 12 May 1937 and the 12th-of-the-month diaries.
- [52] Wikipedia, "I Remember (book)" — https://en.wikipedia.org/wiki/I_Remember_(book) — undated; snippet only — Brainard, Perec, Koch.
- [53] Birt, L. et al., "Member Checking: A Tool to Enhance Trustworthiness or Merely a Nod to Validation?", *Qualitative Health Research* 26(13) — https://ueaeprints.uea.ac.uk/id/eprint/59602/ — 2016; snippet only (abstract) — synthesized member checking.
- [54] Aufderheide, P., reflection on the *Honest Truths* study — https://documentary.org/node/33815 — undated (study 2009); fetched — three principles: honor vulnerable subjects, viewers, production partners.
- [55] Barnwell, A., "Friday essay: Can you keep a secret? Family memoirs break taboos — and trust", *The Conversation* — https://theconversation.com/friday-essay-can-you-keep-a-secret-family-memoirs-break-taboos-and-trust-52699 — 2016-01-14; fetched — consent, disputes, practices.
- [56] No Film School, "6 'Rules' for Good Cutting According to Oscar-Winning Editor Walter Murch" — https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch — 2016-11; fetched. Also The Script Lab, Murch's Rule of Six — https://thescriptlab.com/features/screenwriting-101/10523-what-screenwriters-can-learn-from-academy-award-winner-walter-murch-rule-of-6 — 2019-03-18; snippet only (percentages). Primary: Murch, *In the Blink of an Eye* (1995), not opened.
- [57] Curran Bernard, S., *Documentary Storytelling* (5th ed.) — https://www.routledge.com/Documentary-Storytelling-Creative-Nonfiction-on-Screen/CurranBernard/p/book/9781032267296 and https://csic.georgetown.edu/?p=5193 — undated; snippet only — spine, point of attack.
- [58] West, N. M., *Kodak and the Lens of Nostalgia* (University Press of Virginia, 2000) — https://upress.virginia.edu/title/1967/ — 2000; snippet only — snapshots and nostalgia.
- [64] Portelli, A., "What Makes Oral History Different" (1979; in *The Death of Luigi Trastulli and Other Stories*, 1991) — https://ebooks.jgu.edu.in/Record/ebsco_acadsubs_ocm42855671?lng=en — record for the book; quotation as summarised in search results; snippet only.
- [65] Memory-map examples — https://carleton.ca/history/2014/history-students-create-living-archive/ and https://www.cbc.ca/news/canada/newfoundland-labrador/memory-maps-1.5345084 — 2014 / undated; snippet only — sketch-map elicitation.
- [67] University of Michigan ISR, life history calendar — https://api.isr.umich.edu/?p=196256 — undated; fetch returned 403; snippet only — calendar improves retrospective recall.
- [70] FuneralOne, "22 Tips For Creating Tribute Videos Your Families Will Cherish Forever" — https://blog.funeralone.com/funeralone-products/life-tributes/tribute-video-tips/ — undated; fetched — vendor guidance incl. common mistakes.
- [71] Hutchison Funeral Home, "How To Make The Perfect Tribute Video For A Funeral?" — https://www.hutchisonfuneralhome.com/how-to-make-the-perfect-tribute-video-for-a-funeral — undated; snippet only — ~30 photos, under 10 minutes.
- [73] Phone-recording guides — https://libguides.marquette.edu/podcasting/diy , https://gotranscript.com/blog/transcribe-interviews-recorded-on-a-phone , https://sonix.ai/resources/how-to-record-great-audio-on-your-mobile-phone-for-accurate-transcription/ — undated; snippet only — external mic, distances.
- [76] Family History Interviewing Tips (Idaho GenWeb) — https://idaho.idgenweb.org/Genealogy/family_history_interviewing_tips.htm — undated; snippet only — fatigue, timelines.
- [77] uDiscover Music, "'Remember Me': The Song That Gave Coco Its Heart" — https://www.udiscovermusic.com/stories/remember-me-coco-song-feature/ — undated; fetched — four performances, writers' intent.
- [79] BYU Family History Library, evidence analysis handout — https://fh.lib.byu.edu/wp-content/uploads/2023/07/Evidence-Analysis_-Handout-July-2023-.pdf — 2023-07; snippet only — original vs derivative, primary vs secondary, direct vs indirect.
- [82] Radford, A. et al., "Robust Speech Recognition via Large-Scale Weak Supervision" (the Whisper paper) — https://arxiv.org/pdf/2212.04356 — 2022; fetched as a PDF — FLEURS word error rates by language (Table 13, read speech). The researcher recovered the column order from the PDF text; spot-check any figure you rely on.
- [83] whisper.cpp releases page — https://github.com/ggml-org/whisper.cpp/releases — fetched 2026-10-18 — asset file names not shown; prebuilt Windows builds not confirmed.
- [85] Microsoft Support, "Open and run DxDiag.exe" — https://support.microsoft.com/en-us/windows/open-and-run-dxdiag-exe-dad7792c-2ad5-f6cd-5a37-bf92228dfd85 — undated; fetched — how to open and save the report.
- [89] GoTranscript, "Transcribe interviews recorded on a phone" — https://gotranscript.com/blog/transcribe-interviews-recorded-on-a-phone — undated; fetched — "6-12 inches from the speaker's mouth"; vendor.
- [90] Marquette University Libraries, podcasting DIY guide — https://libguides.marquette.edu/podcasting/diy — undated; fetched — "a few inches" from the mouth; one phone per person.
- [100] Own measurement, 2026-10-18 (not a web source) — faster-whisper, `small` model, int8, on a 4-vCPU cloud VM with 10 minutes of synthetic test audio (looped sample speech); about nine minutes of processing; one run; not Windows; no family audio used.

## Changelog

- 2026-10-18, v0.1: First draft, written by the Haiku scribe from `research/story.md` (researcher notes, 2026-10-18) and the charter. The charter's surprise fact is used. The notes' hybrid recommendation is flagged as a conflict, not adopted. The gate on real gathering is kept. Not yet tested on the vertical-slice chapter.
- 2026-10-18, v0.2: Fable round-1 review applied. Gathering split into Track A (locate and protect, now) and Track B (recorded sessions behind a gate the maker sets, Decision 11), with a two-track timeline; Janssen and Rubin [47] restated and the middle years framed as grey, not empty; song ages 15 to 30 per [46]; placement distances sourced for one speaker, two-speaker layout left to Exercise 2; the record-to-close rule changed; found voice made a source class; voice line stricter (Decision 10); Recipes 1 to 6 moved to `skills/life-story-interviewing/`.
- 2026-10-18, v0.3: Fable round-2 review applied (C1, C2, nudges 1 to 6). The premiere is public and is a known fact (Decision 3; every cue cleared or cut; the relative script, the Tier 2 script and the release name the use). The proxy is the maker. Relative asks are Tier 1 (unrecorded, nobody briefed) or Tier 2 (brought in, by written maker decision; Step 8; Decision 2 retitled). Counts restated as sources, of whom N are brought in. `allowed_use` added to the inventory. The file plan is written and the copy instruction changed (Step 4). Exercise 1 part (b) is the Danny & Annie viewing (5:52 from page metadata; visual beats UNVERIFIED). Exercise 2 distance is sourced, with the 6-inch test value marked as inference. "The closest insider" wording in the playbook, skill and runbook is flagged for round 3.
