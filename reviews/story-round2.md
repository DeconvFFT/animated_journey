# story — Round 2 review (of 3)

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/story.md` (831 lines, with the round-1 follow-up section), `playbooks/story.md` (v0.2), `skills/life-story-interviewing/SKILL.md` and its five standalone files (`question-bank.md`, `inventory-rules.md`, `inventory-template.csv`, `session-protocol.md`, `surprise-runbook.md`, `beat-sheet.md`), against `CHARTER.md`, `reviews/00-charter-review.md` and `reviews/story-round1.md`.
**Verdict:** `revise`. Round 1's two critical issues are fixed and seven of the eight nudges were applied cleanly, with the source figures now quoted correctly. The chain is close. It fails the bar on one thing of the same kind that failed it last time: two facts the charter fixed on Oct 18 (the premiere is at a mostly public gathering; only the maker knows, and the maker is the proxy) have not reached the playbook, the skill or the runbook, and the consent script every relative will hear is built on the opposite assumptions.

Scores: meaning 4 · specificity 5 · accuracy 4 · feasibility 3 · ethics 3 · craft 4.

---

## 1. Were the round-1 nudges addressed?

| # | Round-1 nudge | Status | Where I checked |
|---|---|---|---|
| 1 | Janssen & Rubin [47] restated; middle years "grey, not empty"; ask relatives for ordinary good texture | **Done, and now verbatim-accurate** (spot-check 1 below) | research Summary §4, Q2 "Two cautions"; `question-bank.md` Stage 7 heading (line 141); playbook Step 6; SKILL step 4 |
| 2 | Song set 15-30 per [46], lower bound 12 as inference | **Done** | research Q2 table, Techniques 11; `question-bank.md` line 20; playbook Step 7; SKILL step 4 |
| 3 | Placement: source the single-speaker distances, mark two-speaker as inference for Exercise 2 | **Done** ([37] 5-6 in; [89] 6-12 in; [90] "a few inches"; two-speaker = inference). One residual blend, nudge 4 below | research Q8, Summary §11, follow-up Q5; playbook Step 2; SKILL step 6; `session-protocol.md` step 5 |
| 4 | Stop recording people who think they are off-tape; get the unguarded remark via S10.4/R10.2 | **Done** in all three places | playbook Step 11; SKILL step 12; `session-protocol.md` step 20 |
| 5 | Voice line: adopt the stricter lean or list it as an open charter decision | **Done, both:** stricter lean adopted and flagged as an open charter decision | playbook Decision 10; SKILL Ethics guardrails; research Pitfalls §4; `surprise-runbook.md` Found voice |
| 6 | Dated addendum; surprise as the operating column; hybrid as a reopen note; minimum viable gather in surprise figures | **Done.** One stale line survives (nudge 5 below) | research "What this means" addendum, §1 table, §3 |
| 7 | Found voice as a first-class source class, with the relative ask-line | **Done, thoroughly:** `V` code, item fields, search checklist, ask-line in the script, Track A list | playbook Step 4, Timeline; SKILL step 3, step 5; `surprise-runbook.md`; `inventory-rules.md` |
| 8 | Danny & Annie: watch with a stopwatch, add time and visual columns, or swap in a viewable short | **Not done.** Credits, three text cards and beat order were verified from the page; the time and visual columns are still TODO; no swap was made. The researcher's reason (YouTube redirected the automated fetch) is honest. I have closed the runtime question myself (spot-check 7); the rest is a six-minute task for the maker, nudge 3 below | research Exemplar 2, follow-up Q6 |

Round-1 critical issues: **C1** (gate vs timeline) is fixed by the Track A / Track B split, Decision 11 and the Door A rule; the two-track timeline now reads consistently. **C2** (skill not executable) is fixed: the recipes live beside the skill, and the CSV header, slate line, relative script and three-doors line are inline in `SKILL.md`.

---

## 2. Spot-checks (7 claims, fetched 2026-10-18)

| # | Claim | Source | Result |
|---|---|---|---|
| 1 | Cultural life script: few positive events expected after 30 (8.4%); about half of negative and neutral events (51.7%) at 31+; events after 35 rated negative on average [47] | pmc.ncbi.nlm.nih.gov/PMC3972131 | **Confirmed**, each figure verbatim: "hardly nominated any positive events that were expected to take place after the age of 30 (8.4%)"; "Almost half of the negative and neutral events (51.7%) were expected to take place in middle and late adulthood (31+ yrs)"; Discussion: events "after people turn 35 years old were rated on average to be negative." |
| 2 | Reminiscence bump 15-30; about 70% of bump songs evoked a memory vs 44% (López-Cano et al. 2020, older adults) [46] | frontiersin.org, Martínez-Saez et al. 2024, §1.2 | **Confirmed**: "(between 15 and 30 years of age)"; "around 70%" vs "only 44%". |
| 3 | "6-12 inches from the speaker's mouth"; phone centred on a stable surface; seat people across from each other; two lavaliers if possible; no two-speaker distance [89] | gotranscript.com | **Confirmed** in every particular; the page gives no distance for two people sharing one phone. The notes' handling of it as inference is right. |
| 4 | OHA: informed consent; narrator approval before public release where possible; lead-in with names, full date, "narrator's home", subject; right to refuse subjects and restrict access; no "manipulations of the narrator's words"; "integrity of the narrator's perspective" [8] | oralhistory.org PDF (text extracted with pdftotext) | **Confirmed**, verbatim. The new close-of-session rule and the slate template follow it exactly. |
| 5 | faster-whisper benchmark: 13 min of audio; RTX 3070 Ti 8 GB, CUDA 12.4; i7-12700K 8 threads; large-v2 GPU 2m23s / 1m05s / 1m03s; small CPU 6m58s / 2m05s / 2m37s; Windows needs a separate NVIDIA-library archive on PATH [80] | github.com/SYSTRAN/faster-whisper | **Confirmed**, all six timings and the Windows note. The playbook's "about 1.5 minutes per 10 minutes on a fast desktop CPU" (whisper.cpp small, 2m05s scaled) is correct arithmetic. |
| 6 | whisper.cpp releases: v1.9.5 "Latest", 06 Oct, two assets, file names not shown; prebuilt Windows builds unconfirmed [83] | github.com/ggml-org/whisper.cpp/releases | **Consistent with the notes.** The asset list failed to load for me too; the GitHub API is not enabled for this session; the expanded-assets fragment came back empty. Still UNVERIFIED, and the notes say so. |
| 7 | *Danny & Annie* combined cut: runtime UNVERIFIED; YouTube embed `WNfvuJr9164` on StoryCorps' canonical page [92][94] | storycorps.org/animation/danny-and-annie/ (page source) and youtube.com/watch?v=WNfvuJr9164 (page metadata, fetched by curl) | **Embed ID confirmed** from the StoryCorps page source. **Runtime now known:** YouTube's own page metadata gives `lengthSeconds: 352` and `duration PT5M52S`; the oEmbed endpoint returns the title "Danny & Annie" from StoryCorps, channel StoryCorps. So the combined cut is **5 minutes 52 seconds**, and PBS's "37 minutes" [23] is not this film. I did not watch the video; visual beats remain UNVERIFIED. |

Net: 6 of 7 confirmed exactly, 1 unlistable for me as for the researcher, and one UNVERIFIED item (runtime) closed by this review. The epistemic labelling again survived the hand-offs intact.

**Local-machine check (the maker's own message asked for it).** This session is still a Linux cloud VM: no `/mnt/c`, `/mnt/user-data/uploads` is empty, and no remote-device or computer-use tools are present. The hardware inventory, the language question and the people tab still have to come from the maker (follow-ups 1-3).

---

## 3. Critical issues (must be fixed before approval)

### C1. The consent every relative will be asked for does not match what the charter says the film is.

`CHARTER.md` Known facts (Oct 18): "Occasion and venue: a premiere at a mostly public gathering on Feb 27 ... treat it as a film with a public audience, not a family slideshow." Principle 7: "the voices of people who appear are cleared for public exhibition." The story artefacts say the opposite in five places:

- `playbooks/story.md` Decision 3: "A private screening, or a public one? Our current lean: not chosen (charter open)."
- `playbooks/story.md` Pitfall 13 and `research/story.md` Q9 row 10: "Private viewing is the default unless the music is licensed."
- `research/story.md` Open question 4: "Public screening or private gift? ... decision due Sat 2026-11-14", and follow-up Q7 asks the maker to supply "where it will be shown".
- The relative script (`SKILL.md` step 5, `surprise-runbook.md`, playbook Step 8) says only "a piece about [NAME]'s life as a gift"; `session-protocol.md` step 2 says "who will hear it" without saying; Exercise 7's consent paragraph says "who will see it" without saying.

OHA [8] (spot-check 4) makes informed consent and the narrator's right to restrict access the floor. Consent given for "a gift" is not consent for a public screening, and a relative who learns on Feb 27 that their voice played to a hall is exactly the "whose story is it" failure the notes themselves cite [55]. Music is the smaller half of this; the voices are the larger.

**Fix.** (a) Decision 3 becomes a known fact: public premiere, with the open question narrowed to jurisdiction (charter open decision) and whether a private link follows. (b) Pitfall 13 and Q9 row 10: replace "private viewing is the default" with "every cue must be cleared for a public screening (charter Principle 7); a cue that cannot be cleared is cut, not quietly kept." (c) Relative script, `session-protocol.md` step 2 and Exercise 7: name the use in one sentence: "It will be shown at a gathering on Feb 27 that is partly public, and may be shared with family afterwards by private link; you can restrict any part to the family-only version or to nobody." Add `allowed: hall / private link / family-only / none` to `consent_status` or as a new column in `inventory-rules.md`. (d) Research Open Q4 and follow-up Q7: mark the public/private question as settled by the charter and keep only jurisdiction and the cue sheet.

### C2. The playbook assumes a circle of relatives who are "in on it", and a relative proxy, while the charter says only the maker knows and the maker is the proxy.

`CHARTER.md` Known facts: "Only the maker knows. The maker is the sole producer and nobody else is in on it. Relatives and friends can still be sources ... through low-key asks that don't reveal the project, unless the maker later decides to bring someone in. The maker is her proxy for hard chapters." Against that:

- `playbooks/story.md` "Why this matters" and Step 1: "a trusted close relative acts as her proxy"; "Name the one close relative who will act as proxy."
- `playbooks/story.md` Step 8: "In surprise mode, every relative must know about the secret before the session."
- `surprise-runbook.md` Gate 1: "Brief everyone, including the spouse."
- `research/story.md` §3 minimum viable gather: "8-12 relatives, 2 insiders".

Two things follow and the artefacts say neither. First, nothing recorded for a public film can come from someone who was not told what it is for (C1, OHA [8]); so a recorded session *is* bringing that relative in, which the charter leaves to the maker as an open decision ("Whether to bring anyone else in later"). Second, a 10-14 person circle is a large leak surface for a project whose own runbook cites a six-year-old at lunch [28]. The playbook's method is ethically sounder than covert recording, and I am not asking it to be weakened. I am asking it to say plainly that its method requires a decision the charter has not yet made, and to give the maker a way to work before that decision.

**Fix.** (a) Playbook Step 1 and "Why this matters": the proxy is the maker (charter); a relative "second check" is optional and counts as bringing that person in. (b) Split relative asks into two tiers, in playbook Step 8, `SKILL.md` steps 3 and 5, and `surprise-runbook.md` Gates 1-2. *Tier 1, low-key and unrecorded* (allowed now, reveals nothing): the found-voice question asked as an ordinary family request ("do you still have that video of Mum from the wedding? don't delete it"), where the albums and papers are, and stories heard in normal conversation and written up afterwards by the maker as `R` rows with `consent_status = not-asked (surprise hold)`, never quoted in the film without later consent. *Tier 2, brought in* (the honest script, recorded, consented): each person is a dated line in the people tab ("told on", "scripted line if asked"), and the first one is a written maker decision under charter open decision "whether to bring anyone else in", reviewed by the advisor like a gate pull. (c) Decision 2 becomes "Whom to bring in, if anyone, and when", with the trade-off stated: zero brought-in means no recorded relative voice in the film and no relative second check; Door A relatives are the natural first candidates. (d) Research §3 minimum viable gather and the playbook Timeline: give the counts as "8-12 relatives as sources, of whom N brought in" and start N at the Door A count, expanding only by decision. (e) Runbook Gate 1: delete "Brief everyone, including the spouse" and replace with the tiered rule; the spouse is the single largest leak path and the charter currently keeps them out.

---

## 4. Nudges (6)

1. **C1 as edits.** `playbooks/story.md` Decision 3 (rewrite as a known fact), Pitfall 13 (replace the private-default sentence), Exercise 7 (add the use sentence to the release); `skills/life-story-interviewing/SKILL.md` step 5 relative script and `surprise-runbook.md` script (add: "It will be shown at a gathering on Feb 27 that is partly public, and may be shared with family afterwards; you can restrict any part"); `session-protocol.md` step 2 (same); `inventory-rules.md` (add an `allowed_use: hall | private-link | family-only | none` column and put it in the CSV header in `SKILL.md` step 14 and `inventory-template.csv`); `research/story.md` Open Q4 and follow-up Q7 "Decisions the maker supplies" (strike the public/private question; keep jurisdiction and the cue sheet).

2. **C2 as edits.** `playbooks/story.md` para 3 of "Why this matters" and Step 1 (proxy = the maker, per charter; relative second check optional and counts as bringing in), Step 8 (two tiers of ask), Decision 2 (retitle "Whom to bring in, if anyone, and when", with the trade-off), Timeline Oct 18-24 row (add "decide whether anyone is brought in; if nobody yet, Track A is Tier 1 only"); `SKILL.md` step 3 (the found-voice question phrased as an ordinary family ask when the relative is not brought in) and step 5 (the honest script is for brought-in relatives only; log "told on" in the people tab); `surprise-runbook.md` Gate 1 (delete "Brief everyone, including the spouse"; insert the tiered rule) and People tab (add `told_on` and `scripted_line_if_asked`); `research/story.md` "What this means" §3 ("8-12 relatives as sources, of whom N brought in; N starts at the Door A count").

3. **`research/story.md` Exemplar 2 and follow-up Q6; `playbooks/story.md` "Things we have not checked yet" (Danny & Annie bullet); `beat-sheet.md` Beat sheet paragraph.** Record the runtime: "Combined cut 5:52 (352 s), from the YouTube page metadata of the embed `WNfvuJr9164` that [92] carries, seen 2026-10-18 by the Fable advisor; visual beats still UNVERIFIED." Then turn the open columns into a bounded task: 13 rows (10 beats plus 3 cards) in 352 seconds is about 27 seconds a row, so the maker needs one viewing with a stopwatch and a second with the table in hand, about 15 minutes in total; put it in Exercise 1 as part (b), and set the swap date at the gate (Saturday 2026-11-14): if the columns are still empty then, replace Exemplar 2 with one of the other StoryCorps animated shorts whose durations (3:21, 1:47, 3:23) are already listed on [92], and say so in a dated line.

4. **`playbooks/story.md` Exercise 2, step 2 of Steps.** "one phone each, about 6 inches from each mouth, which is the one-phone-per-person ideal [90]" blends two things: [90] says "a few inches" and recommends one phone per person; "about 6 inches" is the project's own test value. Rewrite: "one phone each, a few inches from each mouth per [90]; we test at about 6 inches (inference)."

5. **`research/story.md` "What this means" §5 and §2 table.** §5 still asks "Is the hybrid recommendation right for this relationship?", which the addendum above it retired; replace with the real round-2 questions (whom to bring in, how the consent tiers interact with Door A, whether the 8-12 count survives a small circle). In the §2 table, the row "3-8 | Nov 1 - Dec 12 | Recorded relative interviews (after the gate)" starts two weeks before the latest gate date; write "after the gate (Nov 14 at the latest, Decision 11)".

6. **`playbooks/story.md` Step 4 found-voice paragraph and Track A bullet; `surprise-runbook.md` Found voice; `SKILL.md` step 3.** "Copy the originals once the file plan is written" sits beside a risk column that says "phone replaced or storage cleared". Copying an existing file is not recording a real person and does not touch the gate. Write the file plan now, in one paragraph in the runbook (two copies on two encrypted drives in different places, originals never edited, a manifest line per item with checksum, holder, date and who speaks, the charter-review storage rule), and change the instruction to "copy as soon as the relative agrees, by cable or a direct transfer, never through a chat app." Under C2 this is a Tier 1 ask when phrased as an ordinary family request.

---

## 5. What is strong (keep all of this)

- **The two-track gather (Track A now, Track B behind a dated gate with a Door A exception)** is the best fix in this round. It resolves the round-1 contradiction without pretending the oldest relatives can wait, and the Door A thresholds are honest about being judgement calls.
- **Found voice is now a real method**, not a code in a table: a search checklist with "ask whom" and "risk if not copied now", item fields, an ask-line that avoids forwarding through chat apps, and a handling rule that permits restoration and forbids extension. This is what makes the charter review's "her phrases as chapter titles" possible in surprise mode.
- **The source figures are now right and quoted.** Janssen & Rubin, the bump ages and the placement distances all verified verbatim, and the design conclusion drawn from [47] (grey, not empty; ask for ordinary good texture) is the correct one and is already wired to R7.1, R7.4 and R7.8.
- **The round-1 follow-up section is a model of how to answer when the facts are missing**: a decision table keyed on the hardware, a measured slow-machine bracket with its limits stated, per-language Whisper error bands with the character-level caveat, and an Exercise 2 protocol with tested ffmpeg commands and explicit pass criteria. The scribe carried it into Step 3 and Exercise 3 without losing the caveats.
- **The close-of-session rule and the slate** now match OHA to the letter (spot-check 4), and the three-doors line, the slate and the relative script are inline in `SKILL.md`, which is what an agent needs at the moment of use. The skill description triggers on the right verbs (preparing, running, logging, transcribing, handling a hard chapter, proposing rows) and the "When not to use" list is exactly right.
- **The Decision 10 voice line** is now stricter than the charter and says why, while leaving the maker the decision. That is how an open charter question should be presented.

---

## 6. Research follow-ups (facts not in the notes; do not guess)

1. **Whether the maker will bring anyone in, and whom first.** This is the charter's open decision and it now gates the recorded track (C2). The Door A list is the natural answer; only the maker has it.
2. **The maker's Windows hardware** (CPU, RAM, GPU and VRAM, free disk, Windows version). Still unreachable from this session: no `/mnt/c`, empty uploads folder, no remote-device tools. The PowerShell inventory in playbook Exercise 3 is ready to paste.
3. **The family's language(s) and any code-switching**, to run Exercise 3 on the right voice.
4. **Jurisdiction of the premiere** (charter open decision), since the music and image-rights answer in follow-up Q7 is US-only; belongs to `music-sound` / `theatrical-delivery`.
5. **whisper.cpp v1.9.5 asset names.** Neither the researcher nor I could list them (page failed to load assets; GitHub API not enabled here). The maker can open the release page once and report whether a `whisper-bin-win-*.zip` exists; it decides whether Exercise 3 needs a cmake build.
6. ***Danny & Annie* visual beats:** one maker viewing (5:52) with the 13-row table (nudge 3).
7. **How-tos for transferring answering-machine tapes, microcassettes, camcorder tapes and saved voicemails on Windows**, still "Not done" in the notes; this becomes urgent the moment Tier 1 found-voice asks start returning items.

---

## 7. Advisor insight

**The maker is the best witness to the grey years, and the only one who can be recorded today.**

Two findings in these notes point at the same person. Janssen & Rubin say the culture expects her 35-55 to be grey, so relatives will under-report it. And the charter says only the maker knows, so for now nobody else can be recorded. But the maker was a child in her house during exactly those years. Nobody else watched her at 7 a.m. for a decade.

So start a Track A practice that needs no gate, no circle and no consent but the maker's own: every day for the next hundred days, five minutes into the phone, Brainard's form, "I remember...", about her, in that era. "I remember the sound her keys made." "I remember she always ate standing up." Five hundred fragments by the end of January, each already a texture row with source `R-maker`, confidence C, no drawer problem, the quota for the grey decades met from one witness before a single relative is briefed. It also trains the exact muscle Exercise 6 is trying to build, on real material.

Then use it in the film. The maker's voice is the one voice that is cleared on day one and will still be cleared in twenty years. Let the "I remember" fragments be the connective tissue between the relatives' clips and the found-voice moments: a child telling a mother, in front of the people who love her, what they noticed when she thought nobody was looking. That is the honest frame for a surprise, it is unmistakably about this one person, and it costs nothing but a hundred quiet mornings.

---

## Changelog
- 2026-10-18: round 2 of 3 written by the Fable advisor. Eight round-1 nudges checked (7 done, 1 open); seven claims spot-checked online (6 confirmed, 1 unlistable, 1 UNVERIFIED runtime closed at 5:52); two critical issues, six nudges, seven follow-ups.
