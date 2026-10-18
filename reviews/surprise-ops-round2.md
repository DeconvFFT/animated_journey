# Review: `surprise-ops` — round 2 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; reveal Saturday 2027-02-27)
**Reviewed:** `research/surprise-ops.md` (1226 lines, now including the round-1 follow-up F1–F5 and sources [93]–[134]), `playbooks/surprise-ops.md` (draft v2, 779 lines), `.claude/skills/surprise-tribute-operations/SKILL.md` (164 lines), against `CHARTER.md`, my brief (`reviews/01-addendum-briefs-review.md` §2.4) and my round-1 review (`reviews/surprise-ops-round1.md`).
**Verdict:** **revise**, narrowly. All eight round-1 nudges landed and every spot-check that reached its source held. What remains is one integration gap that reaches the schedule (the researcher's own follow-up F1–F5 is written but not carried into the plan, the playbook or the skill) plus six small text fixes. One scribe pass, no new research run, and round 3 should approve.

---

## 0. Round-1 nudges: were they addressed?

| # | Nudge | Status | Where I checked |
|---|---|---|---|
| 1 | Hanukkah to Dec 4–12 (weeks 7–8); delete Dec 25 TODO; retitle Table E / Holiday rules; week-8 note on the Dec 11 soft deadline | **Done** | Research Table C weeks 7, 8, 10; Table E title and closing note; playbook Step 1.4, Key dates row, Holiday rules title and note. Still carries "no URL recorded; TODO(research): add a numbered source" — I supply one in nudge 4 |
| 2 | "receive-by" → "ship-by" everywhere, with the definition | **Done** | Research Summary 7, Q3 closing paragraph, Table D heading and assumptions; playbook heading, Step 8.2, Key dates rows Oct 30 / Nov 13 / Nov 27 / Dec 4 / Dec 11 / Dec 18; skill Procedure 9 and "Before each lab order". The only remaining "receive-by" is in the playbook changelog v1, which is history |
| 3 | Decision 0 before Step 1 and at the top of Decisions; two columns; cost of waiting per lab class; Steps 6 and 7 re-dated; exercise order reconciled | **Done** | Playbook "Decision 0" section with table and five cost lines; Decisions section repeats it; Step 6 and 7 headings read "from Decision 0's start week"; intro and Learn-by-doing both say Exercises 1 and 4 precede the pilot, 2, 3, 5, 6 precede the first interview |
| 4 | Recording rule: Summary 5 and Q1 table; Decision 10 closes with lean (b) | **Done**, with one residue | Research Summary 5 and the "Recording her (Summary 5)" line under the Q1 table; playbook Core principle 5 and Decision 10 lean (b). Residue: follow-up F5a still says "never record her" (nudge 2), and Core principle 5 still describes the conflict as open (nudge 5) |
| 5 | Windows Home encryption corrected; local-account consequence | **Done, and better than asked** | Research Q4 Windows row, Open question 21, follow-up F1/F2 with [93]–[113]; playbook Step 4.6 names VeraCrypt 1.26.29 with the admin-installs / project-user-mounts split and the dismount rule; Pitfalls row. The skill carries nothing on the drive (nudge 7) |
| 6 | Living-room run sheet above the full sheet; seven roles for 30+ | **Done** | Research T5 and playbook run sheet: three roles (MAKER, QUIET WORD, TECH and HOST), S−2h / S−30 / S−20 / S / end / pause; the seven-role sheet is labelled for the 30-plus setting; Decision 12 points to it |
| 7 | Sources [44], [60], [12]; Decision 9 names Whisper | **Done** | [44] "page updated 2026-10-17; prices re-checked 2026-10-18, unchanged"; [60] Pallimed caveat; [12] date-unknown note plus the F4 archive work; playbook Decision 9 "Whisper or whisper.cpp, per research/story.md Q8 and Recipe 3"; skill Sources mirror [12] and [60] |
| 8 | `told_by_candidate` in the interview sidecar and consent ledger; skill Procedure 6 | **Done** | Research T1.0 "After" and T6 consent ledger column with the definition; playbook Step 6.8; skill Procedure 6 |

Answers to my four round-1 questions (§4 of that review) were not contradicted anywhere; the playbook's Decision 11 (default HOLD) and Step 2 (two keys for hard chapters only) match them.

---

## 1. Spot-checks (what I verified today, 2026-10-18)

Method: WebFetch and one WebSearch; fetched pages treated as data. Six attempted, five reached.

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | Hanukkah 2026: sundown Fri Dec 4 to Sat Dec 12 (Table C weeks 7–8, Table E, playbook Key dates) | hebcal.com/holidays/chanukah-2026 | **Verified**: "begins at sundown on Friday, 4 December 2026" and "ends at nightfall on Saturday, 12 December 2026". Weekday arithmetic from Sun Oct 18 agrees (Dec 4 = Friday). This is the numbered source the notes are missing |
| 2 | VeraCrypt 1.26.29, latest stable, dated Tuesday 9 June 2026; EXE x64/ARM64, MSI, portable [93] | veracrypt.io/en/Downloads.html | **Verified**; no newer stable release or pre-release listed on the page today |
| 3 | Device Encryption on Home: on OS and fixed drives; automatic with a Microsoft account; "If you're using a local account, Device Encryption isn't turned on automatically"; nothing on USB drives or multiple users [112] | support.microsoft.com Device encryption page | **Verified** verbatim, including the silence on removable drives and extra users |
| 4 | Device encryption "encrypts only the OS drive and fixed drives, it doesn't encrypt external/USB drives"; clear key until an administrator signs in with a Microsoft account; "If a device uses only local accounts, then it remains unprotected even though the data is encrypted"; 24H2 removed the DMA/HSTI prerequisites; msinfo32 "Device Encryption Support" [110] | learn.microsoft.com BitLocker overview (ms.date 2026-08-24, updated 2026-10-08) | **Verified** verbatim, dates match |
| 5 | Capture comparison: Capture $19.99 SD / $29.99 FHD / $39.99 4K, 2–3 weeks; iMemories about 1 week; ScanDigital and ScanCafe $28, 3–4 weeks; Legacybox and Southtree 4–6 weeks; Forever Studios from $12, 2–4 weeks; article 2026-08-07, prices checked 2026-08-26; Capture ranks itself first [43] | capture.com blog | **Verified.** One refinement: iMemories is $29.99 per tape and Legacybox publishes kit prices (2-item kit $69.98), not a per-tape price; the notes' "$28 to $29.99" bracket for that group is fine but Legacybox should read "kit-priced" |
| 6 | German StGB §201: unauthorised recording of private speech, up to three years or a fine, no participant exception; translation current to 7 Nov 2024 [119] | gesetze-im-internet.de English translation (HTML and PDF) | **Not reachable today** (HTTP 503 twice). Not contradicted; the researcher reports a local text extraction. Keep "High for the text" but re-verify when the site is up (research follow-up) |

Internal checks: the ship-by arithmetic in Table D still works (ship-by = Jan 24 − lab weeks − 4 weeks, taken as the Friday on or before: 8-week class → Sun Nov 1 → Fri Oct 30 ✓; 6-week → Nov 15 → Fri Nov 13 ✓; 4-week → Nov 29 → Fri Nov 27 ✓; 3-week → Dec 6 → Fri Dec 4 ✓; 1–2-week → Dec 13–20 → Fri Dec 11–18 ✓). Every weekday/date pair added since round 1 (Dec 4 Fri, Dec 12 Sat, Mar 6 Sat, Mar 29 Mon, Apr 24 Sat) is correct. The seven new source numbers used in the playbook ([93][94][95][97][98][110][112]) all exist in its Sources list.

---

## 2. Scores (1–5)

| Criterion | Notes | Playbook | Skill | Track |
|---|---|---|---|---|
| Meaning | 4 | 4 | 4 | **4** |
| Specificity | 5 | 5 | 4 | **5** |
| Accuracy | 4 | 4 | 4 | **4** |
| Feasibility | 4 | 4 | 4 | **4** |
| Ethics | 5 | 5 | 5 | **5** |
| Craft / usability | 4 | 4 | 4 | **4** |

**Why these numbers.**

- *Meaning 4.* `told_by_candidate` now links gathering to the told-by structure; her agency still sits at the centre (quiet word, stop signal, private cut, "her turn", ledger she closes). It stays at 4 because the Card A handwriting idea from round 1 (her own labels as the film's only text in her hand) is not yet in the playbook; that is optional, not a defect.
- *Specificity 5.* Unchanged: eight kits, dated plan, scripts, decision sheet, two run sheets, and now a drive-encryption recipe with the exact admin/standard-user split.
- *Accuracy 4 (up from 3).* The two errors that reached the schedule and the device checklist are fixed and re-verified. Five of five reachable spot-checks held. What keeps it from 5: the follow-up's findings (F3 Pro8mm unit, F5a non-US law, F5b cassettes) contradict the body's Open questions 13, 16, 19, Table A, the playbook's Step 1.2 / Decision 1 / Gaps, and the skill's Law guardrail, all of which still say "unverified" or "not researched"; F5a repeats "never record her"; Hanukkah still has no numbered source.
- *Feasibility 4 (up from 3).* Decision 0 puts the start-now / wait trade-off in front of the maker with the cost per lab class, and the exercise order no longer contradicts the Oct 30 pilot. Note for the orchestrator: Exercise 4 ("lab dates in writing, plus waiting for replies") must be sent this week for the pilot to ship on Oct 30; the playbook says so by implication only.
- *Ethics 5 (up from 4).* The headline rule is now consistent across Summary 5, the pretext test, Decision 10 and the skill. The residual "never record her" in F5a is stricter, not laxer, so it is a craft slip not an ethics one. The follow-up asks two ethics questions (file container versus device; answering-machine voices); answers in §5.
- *Craft 4.* The skill's description triggers on the right verbs and nouns and the procedure is followable by an agent; it now has the ship-by rule and the told-by field. The playbook reads cleanly. Deductions: Core principle 5 still narrates a conflict that Decision 10 has closed; Holiday rule 7 points to "Card E's line" where it means the "If she asks" answers; the skill has no line on the encrypted drive even though Step 4.6 now has a procedure; and the follow-up's "Suggested edits (not applied here)" were, as it says, not applied.

---

## 3. Critical issue (one, narrow)

1. **The round-1 follow-up research (F1–F5) is written but not integrated, and one piece reaches the schedule.** F5b gives audio cassettes, microcassettes and answering-machine tapes a capture plan and two dates (pilot Fri Oct 30, mid-lab ship-by Fri Nov 27, or DIY in weeks 2–8), yet Table A still says "Not researched here", Table C/D and the playbook's Key dates have no audio row, Decision 0's pilot line says only "tape", and the Gaps list still says cassettes "were not researched". With the pilot date twelve days away, a maker following the playbook would leave found voice (which `story.md` Q3 calls precious) out of the pilot decision. The same non-integration leaves the playbook and skill saying UK/EU law is unverified when F5a now has a UK statute reading, the German §201 text and GDPR Art. 2(2)(c). Fix by applying the follow-up's own "Suggested edits" list plus nudges 1–3 below.

---

## 4. Nudges (at most 8, each with file, section and exact change)

1. **Audio tapes into the plan.** `research/surprise-ops.md` T4 Table A, row "Audio cassettes, answering-machine tapes, old voicemails": replace "Not researched here / UNVERIFIED" with "Deck + audio interface into Audacity, 48 kHz/24-bit WAV master, real time plus handling [124][125]; do not play squealing, shedding or mouldy tapes, ask a lab [123]; UK lab example £26 per cassette ex VAT [129], US prices snippet only [133]; absent from her home 4–10 weeks if mailed; pilot one tape by Fri Oct 30, volume to a lab by Fri Nov 27 or DIY in weeks 2–8 (F5b)". Add "audio tape" to Table C week 2 ("choose a pilot tape (video or audio)") and a Table D note "audio labs: turnaround UNVERIFIED; treat as mid class". `playbooks/surprise-ops.md`: Key dates Oct 30 row → "Pilot tape (video or audio) to a fast lab"; Step 8.1 → "one pilot tape, video or audio"; Gaps bullet "Audio cassettes…" → "covered in research F5b; lab turnaround for audio still UNVERIFIED". `skills/surprise-tribute-operations/SKILL.md` Procedure 9, after "Send only items she will not miss": add "Audio cassettes and microcassettes count as lab items; a tape that squeals, sheds or smells musty is not played [123]."
2. **Apply the follow-up's own suggested edits to the research body.** `research/surprise-ops.md` Open question 13: "Pro8mm's unit price" → "Pro8mm's unit is not stated; per foot is likely (F3); budget 400 ft at $248–$800 only after a written quote". Open question 16: replace the sentence from "cross-state and cross-border calls, the UK, EU…" with "see F5a: UK IPA 2016 s.3/s.4 (participant recording unlikely to be interception, inference) [117][118]; Germany StGB §201 (no participant exception; consent mandatory) [119]; EU GDPR Art. 2(2)(c) household exemption (untested) [120]; other countries and non-US cross-border still UNVERIFIED". Open question 19: "replaced by F5b". F5a first paragraph: "never record her" → "no recording of her without her knowledge and a spoken yes". Tools table: add a VeraCrypt row as F1 suggests. Q4 Windows row: append "Device Encryption is theft protection, not family-privacy protection [110]".
3. **Carry F5a into the playbook and skill.** `playbooks/surprise-ops.md` Step 1.2, Decision 1, Pitfalls "Unverified law", Gaps "Recording law"; `skills/surprise-tribute-operations/SKILL.md` guardrail "Law": replace "UK, EU and cross-border rules are unverified (TODO(research))" with "UK: a participant's own recording is unlikely to be unlawful interception under IPA 2016 s.3/s.4 (the notes' reading, inference) [117][118]; Germany: StGB §201 makes an unauthorised recording of private speech an offence with no participant exception, so a spoken yes is mandatory [119]; EU: GDPR Art. 2(2)(c) household exemption is likely but untested [120]; other countries and non-US cross-border calls UNVERIFIED (TODO(research))." Also add `country` of the contributor to the sidecar fields in skill Procedure 6 and playbook Step 6.8 (F5a's practical consequence).
4. **Give Hanukkah a numbered source.** `research/surprise-ops.md` Table E closing note and Sources (new [135]); `playbooks/surprise-ops.md` Key dates Hanukkah row, Holiday rules closing note, Gaps "Hanukkah timing": replace "Fable advisor's web check of 2026-10-18; no URL recorded. TODO(research): add a numbered source" with "[135] Hebcal, 'Chanukah 2026' — https://www.hebcal.com/holidays/chanukah-2026 — fetched 2026-10-18 by the Fable advisor — 'begins at sundown on Friday, 4 December 2026'; 'ends at nightfall on Saturday, 12 December 2026'". Delete the TODO in all three places.
5. **Close the narrated conflict.** `playbooks/surprise-ops.md` Core principle 5: delete "The research notes' summary once said 'never any recording of her', which conflicts with their own plan. Settle the rule in Decision 10 before the first interview." Replace with "Decision 10 settles this as lean (b); write the choice into the consent card before the first interview."
6. **Fix the wrong pointer.** `playbooks/surprise-ops.md` Holiday rules item 7: "use Card E's line or the no-lie floor" → "use the truthful line (the 'If she asks' answers under the Truthful pretext cards) and the no-lie floor". Card E is the announced recording, not an answer to her question. The research Table E item 7 already says "the truthful line (T7)".
7. **Decide the drive form and put the drive in the skill.** `research/surprise-ops.md` F1 "Design choice" and `playbooks/surprise-ops.md` Step 4.6: state the decision as "file container, not whole-device: a standard user can mount it, an accidental format prompt is avoided, and the one visible large file is named with the code name" (my answer to F1's question; the format-prompt behaviour stays (M)). `skills/surprise-tribute-operations/SKILL.md`, checklist "Before any collection": add "- [ ] External project drive holds a VeraCrypt container created from the administrator account; the project account mounts it only while working and dismounts before leaving the desk or switching users; mount, copy, dismount, unplug tested once [93][97][98]". Add [93], [97], [98] to the skill's Sources.
8. **Answer the found-voice question as a decision.** `playbooks/surprise-ops.md` Decisions, new Decision 18 "Voices found on tapes and voicemails" (mirror in research F5b ethics and the T6 treatment cheat-sheet as a row "Found voice"): "Her own greeting or message: strongest candidate, top drawer, but she has not agreed to its reuse, so it is listed in the T9 ledger for her post-reveal decision and never opens a hard chapter. A family member's message: ask them as a contributor (consent card, withdrawal date). A non-family caller: private cut only, or out; never in the shared cut. The dead: a voice, yes, if the closest family says yes; never a synthetic version [63]." Lean: as stated.

---

## 5. Answers to the researcher's two follow-up questions

1. *File container or whole-device volume?* **File container.** The admin creates it once; the project standard user can mount and dismount it [97][98]; a plugged-in drive on another PC shows a plain file rather than a "format this disk?" prompt that invites destruction. The cost (one large visible file) is acceptable when the file name is the code name and the drive lives in the maker's bag, not on a shared desk. Whole-device is the better answer only if the drive would ever be left where she might plug it in, which the playbook already forbids.
2. *Are answering-machine voices usable at all?* **Yes, with the ladder in nudge 8.** The callers never consented to a film, so non-family callers do not reach the shared cut. Her own greeting is the one piece of found voice that is unambiguously hers to decide, which makes it the ideal item to hand to her in the "her turn" conversation: "we found this; do you want it in?" That converts a consent gap into the first collaborative decision.

---

## 6. Research follow-ups (facts not in the notes)

- StGB §201 English translation: gesetze-im-internet.de returned 503 twice today (HTML and PDF); re-verify the quoted subsection (1) and the "no participant exception" reading, and note whether German case law treats a participant's own recording of a call differently from a third party's.
- Pro8mm's unit for "$0.62 – $2": still unstated; a written quote for a named tier and 400 ft is the only way to budget (F3).
- Lab holiday cut-offs for 2026 (video and audio): none published; Exercise 4 collects them, and the first two replies should be logged against Table D before Oct 30.
- Audio-lab turnaround (cassette and microcassette) and whether labs accept answering-machine microcassettes; which speed answering machines recorded at (F5b leaves both UNVERIFIED).
- iPhone voicemail export: the Share button's output file type (the Apple page body was cut off) [134].
- Legacybox: confirm whether a per-tape price exists or only kits (Capture's page shows kits only).
- Still open from round 1 if a route opens: first-hand Reddit accounts; MetaFilter threads read directly.

---

## 7. Strengths worth keeping exactly as they are

- **Decision 0** as written: two columns, five cost lines, the maker decides, and the exercises reconciled to it. This is how to respect the maker's sequencing without hiding the schedule's cost.
- **Step 4.6** encryption recipe: the admin-installs / project-user-mounts split, "dismount before you leave the desk", "never the boot drive", and the one-time mount-copy-dismount-unplug test. It is the first device procedure in the repo that an agent could hand to a learner without caveats.
- **F2's reading**: "theft protection, not family-privacy protection" is the sentence that keeps the maker from false comfort.
- The **living-room run sheet**: three roles, six timeline points, and an honest line that there is no camera unless a second person exists.
- **`told_by_candidate`** defined once, in the same words, in all three artefacts.
- The follow-up's **honesty about reach**: 503s, 403s, archive API versus archived pages, "UNVERIFIED on the page" for a date it could not read.
- Everything listed as a strength in round 1 (six-condition pretext test, no-lie floor, make every pretext real, two keys, default HOLD, Mum-test, "only you" question, chain of custody) is intact.

---

## 8. Advisor insight

The "only you" question produces something the notes have not noticed they are collecting: a **coverage map**. Every contributor's answer to "when were you alone with her?" pins a span of years in which someone other than her was in the room. Before any editing, draw her fifty-plus years as a strip and mark each contributor's first-hand window on it (one `years_covered` field per interview, ten seconds to fill). The strip will have dark stretches, years where nobody now living, or nobody in the rings, was in the room with her. Those stretches are not failures of gathering; they are the exact chapters that can only be hers, and they tell the maker three things at once: which decades to ask about in the pretext windows (Card A photos from a dark stretch are worth more than any others), where the film should visibly admit "we were not there" (a closed door, a photograph with no caption, a title card in her handwriting with nothing under it), and what the "her turn" conversation on March 6 should open with ("nobody could tell us about 1991 to 1994; will you?"). It makes the empty last chapter from review 01 specific, named by years rather than by sentiment, and it costs one column in the consent ledger.

---

## Changelog
- 2026-10-18: round 2 review by the Fable advisor. All eight round-1 nudges confirmed applied; six spot-checks attempted, five reached and held, one (StGB §201) unreachable; verdict revise with one narrow critical issue (follow-up research not integrated; audio tapes absent from the dated plan) and eight nudges.
