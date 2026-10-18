# story — Round 1 review (of 3)

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/story.md` (928 lines), `playbooks/story.md` (v0.1), `skills/life-story-interviewing/SKILL.md`, against `CHARTER.md` and `reviews/00-charter-review.md`.
**Verdict:** `revise`. This is strong work, among the best research-to-playbook chains I expect to see on this project, and it is close. It fails the bar on two things that are structural rather than cosmetic: the playbook's gate and its timeline contradict each other, and the skill cannot be executed by an agent without loading a 49,000-token research file. Everything else is a nudge.

Scores: meaning 4 · specificity 5 · accuracy 4 · feasibility 3 · ethics 4 · craft 3.

---

## 1. Spot-checks (9 claims, fetched 2026-10-18)

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | Whisper: MIT; `pip install -U openai-whisper`; `turbo` ~6 GB VRAM, ~8x `large`; needs ffmpeg [39] | github.com/openai/whisper | **Confirmed** word for word, including the models table. |
| 2 | whisper.cpp: MIT; 16-bit WAV; `ffmpeg -i in.mp3 -ar 16000 -ac 1 -c:a pcm_s16le out.wav`; `./build/bin/whisper-cli -f file.wav`; cmake [40] | github.com/ggml-org/whisper.cpp | **Confirmed.** Windows is listed as a supported platform (MSVC and MinGW), so the playbook's "Windows steps UNVERIFIED" is honest but could say "Windows is supported; build via cmake; untested here." |
| 3 | StoryCorps Archive terms: last modified 2023-09-14; perpetual, irrevocable, worldwide licence; private interviews "may still be retained" and accessed by StoryCorps and partners; Library of Congress named [4] | archive.storycorps.org/?p=35 | **Confirmed**, with one precision: the Library of Congress language is in the termination clause (XIV.3), not the privacy-settings clause (III.2). The warning stands. |
| 4 | StoryCorps: a life cannot be covered in one 40-minute conversation; prepare 5-10 questions [2] | support.storycorps.org | **Confirmed.** |
| 5 | UDayton: closets as studios; Lossless setting; Android 128 kbps or higher; Do Not Disturb; 5-6 inches from the mouth [37] | libguides.udayton.edu | **Confirmed** for all of those. **Not found:** "6-12 inches from each mouth" and "hands off the mic" are not on this page (it says place the phone on a table to avoid handling noise). The 6-12 inch figure is attributed to [10][37][38] in Q8 and is unsourced as far as I can see. |
| 6 | Songs from the reminiscence bump: ~70% evoked a memory vs 44% for other songs, older adults, López-Cano et al. 2020 [46] | frontiersin.org (Martínez-Saez et al., 2024) | **Confirmed.** But the paper's bump is **15-30**. The notes say 15-30 in Q2 and then the prompt kit, the playbook (Step 7) and the skill (step 4) all say **12-30** with no inference flag. Small, but it is exactly the kind of drift the charter review warned about. |
| 7 | *This Is Your Life*: Blanchflower 6 Feb 1961 "Oh no it's not"; Barker suspected an affair; Lipman's opt-out; Davison finale dropped; Mullard 1996 report [30] | en.wikipedia.org | **Confirmed** in every particular, including that the Mullard allegations are reported, not verified. |
| 8 | Cultural life scripts: "few anchor events after about age 35 and those are mostly negative" [47] | pmc.ncbi.nlm.nih.gov/PMC3972131 | **Overstated.** The paper says few *positive* events are expected after 30 (8.4%); about half of *negative and neutral* events (51.7%) are expected at 31+; events expected after 35 are rated negative on average. The middle decades are not thin in the script; they are expected to be unhappy. This matters because the finding is used to design Stage 7. |
| 9 | Odour-cued memories: older (first decade), more vivid, more emotional, rarer, and naming the odour helps [41] | frontiersin.org (Larsson et al., 2014) | **Confirmed.** |

Net: 7 of 9 exact, 1 misattributed figure, 1 overstatement. The epistemic labelling (fetched / snippet only / UNVERIFIED / inference) is honest and was carried faithfully into the playbook and skill. That is rare and it is why Accuracy scores 4, not 3.

---

## 2. Critical issues (must be fixed before approval)

### C1. The playbook's gate and its timeline contradict each other, and the contradiction hides the project's longest pole.

`playbooks/story.md` says "The gate comes first... real photos and stories are gathered only after the pipeline and process are locked." Its timeline then schedules "First two relative interviews" for Oct 25 - Nov 7 and six to ten more by Dec 12. The charter puts the Learn phase at roughly weeks 1-4 (to mid-November). Both cannot be true. A learner reading this will either break the gate or lose the five weeks that the oldest relatives and the Christmas window depend on. The charter review (§1.3.1) already argued that gathering is the long pole and cannot be done in week 15; this playbook is where that argument has to become a concrete rule, and it does not.

**Fix:** split "gather" into two classes and give each its own gate. *Locate and protect* starts now and needs no recording: list relatives oldest first with age, health, hearing, distance; list documents and where they physically are; list **found voice** (voicemails, answering-machine tapes, home videos, clips on relatives' phones), since phones get replaced and these are the only source of her own voice in surprise mode; write the consent script; run the practice exercises. *Recorded sessions* wait for the gate, and the playbook names the gate date explicitly as a maker decision, with a stated reason to pull it earlier (an elderly relative, a relative visiting only at Christmas). The timeline table then shows both tracks.

### C2. The skill is not executable by an agent as written.

`SKILL.md` steps 4, 5, 14, 17 and 20 say "from Recipe 1 / Recipe 2 / Recipe 4 / Recipe 5 of `research/story.md`." That file is 928 lines and about 49,000 tokens; the question banks alone run from line 369 to 585. An agent that loads the skill to prepare one session must then read, or search blindly through, the entire research file to find 154 questions, the CSV header, the relative script and the time budget. The playbook has the same dependency (Steps 4, 7, 8). The charter rubric's definition of craft for a skill is "usable by an agent"; this is not, yet.

**Fix:** move the deliverables out of the research file into standalone files beside the skill, and reference them by path: `skills/life-story-interviewing/question-bank.md` (Recipe 1 with the prompt kits and résumé cut list), `inventory-template.csv` plus `inventory-rules.md` (Recipe 2), `session-protocol.md` (Recipe 3), `surprise-runbook.md` (Recipe 4 with the relative script), `beat-sheet.md` (Recipe 5 and 6). The research file keeps the evidence and points at them. Inline in SKILL.md itself: the CSV header line, the slate line, the relative script and the three-doors line, because those are what an agent needs at the moment of use.

---

## 3. Nudges (8)

1. **`research/story.md` Summary §4, Q2 "Two cautions", Stage 7 heading; `playbooks/story.md` Step 6.** Replace "few anchor events after about age 35 and those are mostly negative" with what [47] says: "the cultural script expects few *positive* events after 30 (8.4%) and rates events after 35 as negative on average; about half of the negative and neutral script events fall at 31+." Then draw the right design conclusion: the middle years are not empty, they are culturally expected to be grey, which is precisely why relatives must be asked for the ordinary *good* texture of those years (R7.1, R7.4, R7.8 already do this; say why).

2. **`research/story.md` Recipe 1 prompt kit "Song set"; `playbooks/story.md` Step 7 "Songs"; `SKILL.md` step 4.** Change "ages 12 to 30" to "ages 15 to 30 per [46]; we extend the lower bound to 12 to catch first records (inference)."

3. **`research/story.md` Q8 "Placement" and Summary §11; `playbooks/story.md` Step 2; `SKILL.md` step 6.** The UDayton page gives 5-6 inches for one speaker and does not give 6-12 inches or "hands off the mic." Either cite the source that does (perhaps one of the [73] guides) or mark "6-12 inches between two speakers" as inference to be settled in Exercise 2, which is built for exactly that.

4. **`research/story.md` Recipe 3 step 20; `playbooks/story.md` Step 11; `SKILL.md` step 12.** "Keep recording until they have left the room" and "say goodbye off-tape" records people who believe the interview is over. OHA's consent principle [8], which the same documents cite, does not allow that. Change to: "At the close, say 'I'm going to leave the recorder running for a minute while we wrap up, is that all right?' or stop it visibly. Never record someone who thinks they are off-tape." The thing you want (the unguarded last remark) is better obtained by asking S10.4 / R10.2 as the final question.

5. **`playbooks/story.md` Decision 10; `SKILL.md` Ethics guardrails, voice line; `research/story.md` Pitfalls §4.** "No voice cloning or synthetic voice unless that person explicitly agrees" is weaker than the charter review's sharpening of Principle 4 (no synthetic voice of any real person, living or dead, even with consent, because an audience cannot tell consent from fakery and the piece will outlive the context). Either adopt the stricter line as the lean or list it as an open charter decision for the maker. Do not present the weaker line as settled.

6. **`research/story.md` §"What this means for Life Journey" 1-3.** The hybrid recommendation was written before the charter fixed surprise mode (Oct 18). Add a dated addendum at the top of the section saying so; re-order the mode table so "Full surprise" is the operating column; move the hybrid to an "if the maker reopens the decision" note; lead "Minimum viable gather" with the surprise-mode figures (8-12 relatives, 2 insiders, documents, found voice). The playbook's Decision 1 handles this correctly; the notes must not contradict it, because agents will read both.

7. **`playbooks/story.md` Step 4 and Timeline; `SKILL.md` step 3.** Add "found voice" as a first-class source class with its own list in the inventory `source` codes (the notes' `V` code exists but nothing tells the maker to go and collect it). In surprise mode this is the only route to her own voice, and the charter review's insight (her repeated phrases as chapter titles) depends on it. Ask relatives at briefing time: "Do you have any video or voice message of her on your phone? Please don't delete anything." This belongs in the relative script in Recipe 4.

8. **`research/story.md` Exemplar 2 (Danny & Annie).** The brief asked for a second shot-level analysis. This one is a transcript beat map; the visual choices and runtime are UNVERIFIED and the analyst did not watch it. The short is publicly viewable on StoryCorps' own page [20]. Watch it with a stopwatch, add the time column and the visual device column, and the exemplar becomes usable by the `animated` and `format` tracks too. If it cannot be watched, swap in a viewable documentary short and say why.

---

## 4. What is strong (keep all of this)

- **The *Up* beat table with phase percentages** is exactly the shot-level analysis the brief demanded, and the eleven transferable rules each carry their evidence. The honesty about Wozny being a student essay, and the instruction to re-time, is right. Exercise 1 operationalises it.
- ***This Is Your Life* as the surprise-mode precedent** is an inspired choice: seventy years of documented covert gathering, with named failure modes (grandson at lunch, the note with the phone number, Barker's suspicion, Blanchflower's refusal), and it verified cleanly. The feasibility report, the pre-agreed opt-out question (R10.5) and "reveal as consent point" are directly usable.
- **The inventory template** does what the charter review asked: it forces texture through a mandatory `sensory_detail`, a `recurrence` field and a quota; it separates confidence (A-D) from consent and drawer; it shows how a held row is logged without detail; and it gives AI agents a hard rule (quote and timestamp or no row).
- **The question banks are adapted, not copied.** The résumé cut-and-rewrite table is the single best page in the notes. R2.8 ("one time you thought 'that is exactly who they are going to be'") and R7.8 ("what did they do for you that nobody noticed") are the kind of questions that produce the "you remembered that" moment the success test needs.
- **Privacy is handled seriously:** the StoryCorps terms warning verified, local Whisper with exact commands, "no source, no row," and the reminder that cloud transcription must be disclosed to narrators.
- **The epistemic labelling survived three hand-offs** (researcher to scribe to skill) intact. That almost never happens.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. The maker's Windows machine: CPU, RAM, GPU and VRAM. Whisper `turbo` needs ~6 GB VRAM; whisper.cpp runs on CPU. Which one, and how many minutes to transcribe a 10-minute file, cannot be answered until the hardware inventory from the charter review exists.
2. The family's language(s). Whisper accuracy varies a great deal by language and on older voices; Exercise 3 should be run in the language the relatives will actually speak.
3. Who the oldest relatives are, their health, and where they live. This decides whether the recorded-sessions gate can hold until mid-November or must be pulled earlier (C1).
4. What recordings of the mother already exist (relatives' phone videos, voicemails, home video, answering-machine tapes). This is the found-voice inventory (nudge 7) and only the family can answer it.
5. A source for two-speaker phone placement (nudge 3), or settle it empirically in Exercise 2 and record the result as the project's own finding.
6. *Danny & Annie*: actual runtime and visual beats, by watching it (nudge 8).
7. Music licensing for a private screening versus a public one, which the notes correctly leave open; it belongs to the proposed `sound-and-voice` track, not here, but someone must own it by week 4.

---

## 6. Advisor insight

**Leave three locked rooms, and let her hold the key.**

Surprise mode's great weakness is that the one voice the piece most needs is the one it cannot record. Turn that into the piece's central mechanic. The inventory already produces a list of "ten things only she can confirm." Pick three that matter (why she kept the blue suitcase; what the song in the car was; what her mother said to her the day she left home) and build them into the piece as visibly unfinished places: a chest that will not open, a room with the light off, a caption in a relative's voice saying "Nobody knows. Only she does." At the reveal, the piece stops there and waits. She answers, in the room, in her own words, to the people she loves. With her consent, that is recorded, and the archival cut gets the one thing the surprise could never gather: her voice, telling the part only she knows.

It passes every charter test at once. The mechanic means something (Principle 2: a locked chest is a gimmick for anyone's life except a life assembled behind the subject's back). It invents nothing (Principle 4: the gaps are real gaps). It gives her agency at the one moment the surprise format denies it (Principle 5: she decides what the room hears, and she can say "that one stays shut"). And it converts the covert-gathering constraint, which every other track will experience as a cost, into the moment the family will remember.

---

## Changelog
- 2026-10-18: round 1 of 3 written by the Fable advisor. Nine claims spot-checked online; two critical issues, eight nudges, seven follow-ups.
