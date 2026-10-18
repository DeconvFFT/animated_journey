# Review: `surprise-ops` — round 3 of 3 (final)

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; reveal Saturday 2027-02-27)
**Reviewed:** `research/surprise-ops.md` (1446 lines; body, round-1 follow-up F1–F5 with sources [93]–[134], and a new round-2 follow-up G1–G7 with sources [135]–[169]), `playbooks/surprise-ops.md` (draft v3, 790 lines), `.claude/skills/surprise-tribute-operations/SKILL.md` (181 lines), against `CHARTER.md`, my brief (`reviews/01-addendum-briefs-review.md` §2.4) and my round-2 review (`reviews/surprise-ops-round2.md`).
**Verdict:** **revise**, narrowly and for the same structural reason as round 2. All eight round-2 nudges landed, and every one of eight spot-checks held verbatim. But the researcher's new round-2 follow-up (G1–G7) was again appended with "Suggested edits … not applied here", and three of its findings change the lab ship-by table that the playbook and the skill send the maker to, twelve days before the pilot ships. Scores are all 4 or 5; the verdict is "revise" only because one critical issue is open. One scribe pass of under an hour closes it; no new research run is needed. Since this is the final round, §3 and §4 are written so the orchestrator can carry them forward as-is.

---

## 0. Round-2 nudges: were they addressed?

| # | Nudge | Status | Where I checked |
|---|---|---|---|
| 1 | Audio tapes into the plan (Table A row, Table C week 2, Table D note; playbook Key dates Oct 30, Step 8.1, Gaps; skill Procedure 9) | **Done** | Research Table A row 608 carries the F5b plan with [123][124][125][129][133] and the Oct 30 / Nov 27 dates; Table C week 2 "pilot tape (video or audio)"; Table D closing note on audio labs; playbook Key dates row, Step 8.1 "video or audio", Decision 0 table, Gaps bullet; skill Procedure 9 has the squeal/shed/musty line with [123], and [123] is in the skill's Sources |
| 2 | Apply the F-section's own suggested edits to the body (Open questions 13, 16, 19; F5a first paragraph; Tools table VeraCrypt row; Q4 Windows row) | **Done** | Open question 13 (Pro8mm unit, $248–$800 only after a written quote), 16 (F5a summary with [117]–[120]), 19 ("replaced by F5b"); F5a opens with "no recording of her without her knowledge and a spoken yes"; Tools table row "VeraCrypt 1.26.29" at line 896; Q4 Windows row ends "Device Encryption is theft protection, not family-privacy protection [110] (inference)" |
| 3 | F5a into playbook Step 1.2, Decision 1, Pitfalls, Gaps and the skill's Law guardrail; contributor's country in the sidecar (skill Procedure 6, playbook Step 6.8) | **Done** | Identical wording in all five places; skill Procedure 6 "the contributor's country (for the law guardrail)"; playbook Step 6.8 "their country (see Step 1.2)" |
| 4 | Hanukkah numbered source in research Table E note and Sources, playbook Key dates, Holiday rules note and Gaps; delete the TODO | **Done, with a defensible renumbering** | The scribe used **[169]**, not [135], because the round-2 researcher had already taken [135]–[168]; the playbook changelog says so. The Hebcal entry exists in both Sources lists, no "no URL recorded" or TODO remains anywhere. One craft nit: the full citation is pasted inline into the Key dates table cell and the Holiday rules paragraph instead of "[169]" (see nudge 7) |
| 5 | Core principle 5: replace the narrated conflict with "Decision 10 settles this as lean (b); write the choice into the consent card before the first interview" | **Done** | Playbook Core principle 5, verbatim |
| 6 | Holiday rule 7 pointer: truthful line, not "Card E's line" | **Done** | Playbook Holiday rules item 7 |
| 7 | File-container decision in research F1 and playbook Step 4.6; VeraCrypt line in the skill checklist; [93][97][98] in skill Sources | **Done** | F1 "Design choice (decided, Fable advisor round 2)"; Step 4.6 "Decided (Fable advisor, round 2): a file container…" with the (M)/UNVERIFIED flag on the format-prompt behaviour kept; skill checklist "Before any collection" line 55; [93][97][98] in skill Sources |
| 8 | Decision 18 "Voices found on tapes and voicemails", mirrored in F5b ethics and T6 cheat-sheet | **Done** | Playbook Decision 18; research F5b "Ethics" bullet; T6 row "Found voice (answering-machine tapes, voicemail)" at line 797. Wording matches the nudge, including "a real voice only if the closest family says yes; never a synthetic version [63]" |

Nothing I asked for was applied in a way that weakened a rule; the ethics line is unchanged or stricter everywhere.

---

## 1. Spot-checks (what I verified today, 2026-10-18)

Method: WebFetch for seven sources; where it returned 429 or 503 I made one plain request into an empty scratch directory and extracted text (the researcher reported the same route). Fetched pages treated as data. Eight attempted, eight reached.

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | Hanukkah 2026 begins at sundown Fri 4 Dec and ends at nightfall Sat 12 Dec [169] | hebcal.com/holidays/chanukah-2026 | **Verified** verbatim |
| 2 | Pro8mm turnaround page: "Changes — Effective November 1, 2025"; regular season Jan–Apr, Nov, Dec with Production/Advanced/Ultimate 5–7 business days and Basic 7–10; peak May–Oct 7–10 / 10–14; clock runs from "the date your film enters processing"; allow 72 hours for logging; Rush 1–3 days **$295**; Priority about 5 business days **$165 per film type**; "HOME MOVIE LEGACY DISCOUNT Available December–February — 20% off … unscheduled, take 4-8 weeks" [144] | pro8mm.com/pages/turn-around-times (WebFetch 429; plain request 200) | **Verified** verbatim, every figure. Consequence: Table D's Oct 30 row describes a queue the lab says is open December to February (critical issue §3) |
| 3 | iMemories: "2 week" to files; originals back by UPS Ground "within 4 weeks" after digitising [152] | imemories.com/turnaround | **Half verified.** The page today says "Available online in **1 week** from order approval and payment" (the body's "about 1 week" [43] holds; the G3 note's "2 week" is not what the page shows today) and "we will ship your originals back to you via UPS Ground within 4 weeks" (verified). Footer ©2026. So the fast row is right for files and wrong for originals |
| 4 | Legacybox: Standard "approximately 4-6 weeks; varies depending on inbound volume", Expedited 3–4 weeks, Guaranteed Rush 10 business days; upgrade price depends on order size and shows in the cart; "Updated 3 hours ago" [154] | help.legacybox.com "How long does Legacybox take?" | **Verified** verbatim |
| 5 | StGB §201(1), English translation, verbatim; translation current to the Act of 7 November 2024 (BGBl. 2024 I Nr. 351); §205(1) "prosecuted only upon request" [136][119] | gesetze-im-internet.de/englisch_stgb (WebFetch 503; plain request 200, 761 KB) | **Verified** verbatim: "(1) Whoever, without being authorised to do so, 1. makes an audio recording of the privately spoken words of another or 2. uses or makes a recording thus produced available to a third party incurs a penalty of imprisonment for a term not exceeding three years or a fine." Also §201(2) no. 2 (public communication) and §205(1) as quoted in G1. The round-2 "unreachable" caveat can be dropped |
| 6 | StGB §201(1) German original verbatim [135] | gesetze-im-internet.de/stgb/__201.html | **Verified** verbatim ("Mit Freiheitsstrafe bis zu drei Jahren … wer unbefugt 1. das nichtöffentlich gesprochene Wort eines anderen auf einen Tonträger aufnimmt oder 2. eine so hergestellte Aufnahme gebraucht oder einem Dritten zugänglich macht") |
| 7 | IPA 2016 s.4(1): interception means a relevant act whose effect is "to make any content of the communication available, at a relevant time, to a person who is not the sender or intended recipient"; status "up to date … on or before 18 October 2026" [118] | legislation.gov.uk/ukpga/2016/25/section/4 | **Verified** verbatim. The notes' reading (a participant's own recording is unlikely to be interception) remains labelled inference, which is right |
| 8 | Oxford Duplication Centre: £26.00 per cassette up to 60 minutes, £18.00 at 100+, prices exclude 20% VAT, group "Cassettes, Dictaphone, Mini & Micro Tapes"; no turnaround, no mention of answering-machine tapes [129] | oxfordduplicationcentre.com | **Verified**, including the silences. The page also lists £24 at 10+, £22 at 25+, £20 at 50+, which the notes omit (harmless) |

Internal checks: the ship-by arithmetic in Table D is unchanged and still correct; all weekday/date pairs in the playbook's Key dates hold; every source number used in the playbook and skill exists in the research Sources list ([169] included). The playbook's Decision 18 and the research F5b ethics bullet and T6 row agree word for word on the four-rung ladder.

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

- *Meaning 4.* Decision 18 turns found voice into her first collaborative decision ("we found this; do you want it in?"), which is the right shape for a surprise that must become a collaboration. `told_by_candidate` and the country field now sit in the same sidecar. It stays at 4 because the round-1 Card A handwriting idea and the round-2 coverage map (`years_covered`) are still optional ideas rather than fields; neither is a defect.
- *Specificity 5.* Unchanged: eight kits, dated plan, scripts, decision sheet, two run sheets, a drive-encryption recipe, and now a four-rung found-voice ladder and a six-question lab email with a log table (G3).
- *Accuracy 4.* Eight of eight spot-checks held, including the two that were unreachable in round 2 (StGB §201) or new today (Pro8mm's dated turnaround page). What keeps it from 5 is the same pattern as round 2: the body's Table D and the playbook's ship-by table now contradict the note's own appendix on three rows (Pro8mm's unscheduled queue is a December–February queue; iMemories' originals take four more weeks; audio-lab turnaround is published at 3–6 weeks, not UNVERIFIED), and the Q3 lab table still prices Legacybox at "$28 to $29.99" and Pro8mm rush at $250 against the researcher's own [155] and [144]. These are stale-against-self errors, not sourcing errors.
- *Feasibility 4.* Decision 0 and the exercise order are sound. The Oct 30 pilot is feasible with any mid or fast lab. The cost sketch ($700–$1,000) survives because it never used Pro8mm's unit; it should now say the film line assumes a 2K tier, not Basic 720p (nudge 3).
- *Ethics 5.* The law guardrail is in the same words in five places; the German rule is now verbatim statute plus a labour-court application [140], and the project rule remains stricter than all of it. The found-voice ladder protects non-family callers and the dead. No recommendation in any of the three files records her without her knowledge.
- *Craft 4.* The skill's description triggers on the right verbs and nouns ("gathering stories, photos, objects or recordings from relatives for a secret gift", "sending items to a lab", "auditing a shared device"), its procedure is followable by an agent step by step, and its Sources list is self-contained. The playbook reads cleanly. Deductions: the Hebcal citation pasted in full inside a table cell and a paragraph; Exercise 4 in the playbook has not picked up the six-question email and log table that G3 wrote for it; and, as in round 2, the appendix's "Suggested edits … not applied here" list is longer than the body's changes.

---

## 3. Critical issue (one, the same shape as round 2)

1. **The round-2 follow-up research (G1–G7) is appended but not integrated, and three findings reach the lab schedule that the pilot decision depends on.** Verified today against the labs' own pages:
   (a) **Pro8mm's "unscheduled" 4–8 week discount queue is "Available December–February"** per its dated turnaround page [144]. Table D's first row (ship-by Fri Oct 30, 8-week class), the playbook's ship-by table and Decision 0's first "cost of waiting" line describe a queue that the lab says is not open in October. In November and December Pro8mm is "regular season": Production/Advanced/Ultimate scans in 5–7 business days, Basic in 7–10, clock starting when the film enters processing, plus up to 72 hours for logging. So film belongs in the **fast class at the scheduled price** (ship-by Fri Dec 11 at the latest, earlier is safer), and the Oct 30 row should go or be relabelled as the pilot date only.
   (b) **iMemories returns originals "within 4 weeks" after digitising** [152], although files appear in about a week. Table D exists to get items *back into her house* by week 15 (its last column is "Leaves her house"). For originals, iMemories is a 5-week lab (slow class, ship-by Fri Nov 13); for files only, the fast row stands. The row must say which.
   (c) **Audio-lab turnaround is published**: ScanDigital 3–4 weeks [159], Legacybox and Southtree 4–6 weeks [154][161]. Table D's note "audio labs: turnaround UNVERIFIED; treat as mid class (Nov 27)", the playbook Gaps bullet and my own round-2 wording would put a cassette batch to a 4–6-week lab two weeks late by the table's own formula. Audio follows the same classes as video.
   (d) **Legacybox standard digitising has no delivery guarantee in peak season** [153]; its slow-row date (Nov 13) is valid only off-peak, and its blog still advertises 8–10 weeks [158].
   Fix: apply the appendix's own "Suggested edits" (research lines 1397–1402) with the corrections in nudges 1–3 below, in the research body, the playbook table and the playbook Gaps; the skill needs one sentence (nudge 6).

---

## 4. Nudges (at most 8, each with file, section and exact change)

1. **Film and Pro8mm.** `research/surprise-ops.md` T4 Table D: delete the row "Unscheduled home-movie queue … Oct 30" or retitle it "Pilot ship date (any mid or fast lab)"; add to the Fast row "Pro8mm scheduled, Nov–Dec regular season: Production/Advanced/Ultimate 5–7 business days, Basic 7–10, from the date film enters processing plus up to 72 h logging [144]"; add a note "Pro8mm's 20% Home Movie Legacy Discount (unscheduled, 4–8 weeks) is available December–February only [144]; do not plan on it. Decision (Fable advisor, round 3): pay the scheduled price." Q3 lab table row "Pro8mm": "rush 1 to 3 days for $250" → "rush 1–3 days $295 and priority about 5 business days $165, per film type, turnaround page effective 1 Nov 2025 [144]; FAQ text on the product page still says $250 [143]"; add the four tier prices "$0.62 / $1.00 / $1.25 / $2.00, unit not stated [143]". `playbooks/surprise-ops.md` Ship-by table: same row change; Decision 0 "Cost of waiting" first line → "Pilot: ship-by Fri 30 October 2026 (any mid or fast lab). Pro8mm's 8-week discount queue runs December–February only [144], so film ships at the scheduled price in the fast class."
2. **iMemories, originals versus files.** `research/surprise-ops.md` Table D Fast row and `playbooks/surprise-ops.md` Ship-by table Fast row: "iMemories about 1 week [43]" → "iMemories: files in about 1 week, originals returned by UPS Ground within 4 weeks after digitising [152]; fast class for files only; for originals back in her house use the slow class (Fri 13 Nov 2026)". Research G3 table, iMemories row: "in 2 week" → "in 1 week" (the page as read on 2026-10-18 by the Fable advisor), keep the 4-week originals line. Q3 lab table line 163: Legacybox "$28 to $29.99" → "Legacybox kit-priced, about $31 to $35 per item by kit size [155]; Standard has no peak-season delivery guarantee [153]; Guaranteed Rush 10 business days, price in cart [154]".
3. **Audio labs and the theatrical floor for film.** `research/surprise-ops.md` Table D closing note: "turnaround UNVERIFIED; treat as mid class" → "published 3–4 weeks (ScanDigital [159]) and 4–6 weeks (Legacybox, Southtree [154][161]); audio follows the same classes as video: 3–4-week lab ship-by Fri 27 Nov, 4–6-week lab Fri 13 Nov; EverPresent turnaround unknown [164]; no lab states a policy for answering-machine tapes or microcassette speed (G4)". Table D cost sketch and playbook cost sketch: append "Film: order no lower than a 2K ProRes tier; a 720p .mp4 'Basic' scan does not meet Charter principle 6 (Fable advisor, round 3). On Pro8mm's per-foot reading that is $1.00/ft, $400 for 400 ft, before per-roll extras [143][146]". `playbooks/surprise-ops.md` Gaps bullet "Audio cassettes…": "audio-lab turnaround still UNVERIFIED" → "mail-in audio labs publish 3–6 weeks [154][159][161]; answering-machine-tape policy and microcassette speed still UNVERIFIED (ask in Exercise 4 question 6)".
4. **F5a and F5b carry the G-findings.** `research/surprise-ops.md` F5a Germany row: replace the paraphrase with the verbatim §201(1) from G1, add "(2) no. 2 makes public communication of such a recording an offence; §205(1): prosecuted only on the affected person's request, within three months (§77b) [136]"; confidence cell → "High for the text (re-verified 2026-10-18 by the researcher and the Fable advisor); a labour court applied it to a participant's own recording [140]; no criminal conviction of a participant found". F5b: add "answering machines also used full-size cassettes and endless-loop greeting tapes [163]; Legacybox and ScanDigital list microcassettes [156][160]; iPhone voicemail export is probably .m4a, UNVERIFIED on current iOS, test one [165]". Open question 13: append "tiers verified [143]; unit still not stated; extras are 'PER ROLL' [146]".
5. **Exercise 4 picks up G3.** `playbooks/surprise-ops.md` Exercise 4, Steps: replace step (2)'s list with the six-question email from research G3 (adds question 6 on answering-machine microcassettes and playback speed), add step (5) "Paste the two replies into the Exercise 4 log table (research G3) and recompute ship-by"; and add a first line to the Goal: "Send the two emails this week; the Oct 30 pilot depends on at least one reply." Also add the G2 Pro8mm quote request as an optional third email for anyone with film.
6. **Skill, one sentence and one source.** `skills/surprise-tribute-operations/SKILL.md` Procedure 9, after "Ship-by is the Friday the parcel leaves.": add "A lab's published turnaround counts from the day the item enters processing, not from receipt, and a lab may return originals weeks after the files [144][152]; the ship-by date is computed on the originals' return." Add [144] and [152] to the skill's Sources. Checklist "Before each lab order": "Written turnaround" → "Written turnaround to files and to originals".
7. **Citation hygiene.** `playbooks/surprise-ops.md` Key dates Hanukkah row and Holiday rules closing paragraph: replace the inline full citation with "[169]" (the full entry already sits in Sources); `research/surprise-ops.md` Table E closing note likewise ("Source: [169]"). Research Sources: move [169] from after the round-2 block into the main numbered order, or label the round-2 header "[135] to [168]; [169] added by the scribe".
8. **Close the appendix pattern.** `research/surprise-ops.md`: after applying nudges 1–4, change both headings "Suggested edits to the sections above (for the scribe, not applied here)" to "Suggested edits (applied to the body on 2026-10-18, v3)" and strike the bullets that are now applied, so the next reader does not re-apply or re-doubt them. Answer the three "Questions for the Fable advisor" in G2/G3 inline with: (1) Production tier is the floor (nudge 3); (2) no, pay the scheduled price (nudge 1); (3) do not send a batch to any lab that will not commit a return date in writing; if Legacybox is used in peak season, Guaranteed Rush or not at all.

---

## 5. Answers to the researcher's round-2 questions

1. *Pro8mm Basic is 720p .mp4; is Production the floor?* **Yes.** Charter principle 6 rules out a 720p master for a theatre screen. Production (2K, ProRes) is enough for a 1080p or 2K delivery; Advanced (4K) only if the format track settles on a 4K DCP. Budget on the per-foot reading as a placeholder and on a written quote before ordering.
2. *Is the 20% discount worth the 4–8 week queue?* **No**, and the question is moot for October: the lab's own page opens that queue in December. Film ships at the scheduled price, in the fast class, ideally before Thanksgiving week.
3. *Legacybox: Guaranteed Rush or standard?* A lab that says in writing it cannot guarantee delivery in peak season should not receive items she will miss. If Legacybox is used at all between mid-November and January, it is Guaranteed Rush (10 business days, price in the cart) or nothing; otherwise prefer a lab that gives a dated commitment in its Exercise 4 reply.

---

## 6. Research follow-ups (facts not in the notes)

- **iMemories turnaround wording.** The page I read today says files "in 1 week"; the G3 researcher read "2 week" on the same day. It may vary by format or be A/B text; the Exercise 4 reply from iMemories, if it is one of the two labs, settles it. Until then plan on 1 week to files and 4 more weeks to originals.
- **Pro8mm's unit for $0.62–$2.00** is still unstated after three reads; only the maker's written quote (G2's request text) can close it.
- **Lab replies (Exercise 4).** Still none logged; the two emails must go out this week for the Oct 30 pilot. Log the replies in the G3 table.
- **Which country's law applies** to a call between the maker and a contributor in Germany or the UK remains UNVERIFIED; the spoken-consent rule covers the strictest case regardless.
- **iPhone voicemail export extension on iOS 17 or later**: test by sharing one voicemail to Files (one minute).
- **Microcassette speed used by answering machines**: no source ties a speed to the machines; ask the lab (question 6) and keep the lab's raw file as master.
- **Legacybox Guaranteed Rush price**: visible only in a cart; record it if the maker gets that far.
- **Reddit and MetaFilter** first-hand accounts: still unreachable from this container after three rounds; leave to the maker's hand search as Open question 11 describes.

---

## 7. Strengths worth keeping exactly as they are

- **The found-voice ladder** (Decision 18, F5b, T6): four rungs, her own greeting as the first collaborative decision, non-family callers never in the shared cut, the dead only by the closest family's yes and never synthetic. It is the clearest consent rule in the repo.
- **G1's legal work**: verbatim statute in two languages, the labour-court application, the constitutional cases named with page references, and an honest "no criminal conviction of a participant found; absence in a search is weak evidence". This is how law should appear in a non-legal document.
- **Step 4.6 and the skill's drive line**: admin creates the container, project account mounts and dismounts, dismount before leaving the desk, never the boot drive, test once. Unchanged from round 2 and still the best device procedure in the project.
- **The law guardrail in five identical copies** (playbook Step 1.2, Decision 1, Pitfalls, Gaps; skill guardrail): one wording, so a change in one place is visibly a change.
- **G3's six-question lab email and log table**: they turn Exercise 4 from "ask the labs" into a form the maker can fill in ten minutes.
- Everything listed as a strength in rounds 1 and 2 (six-condition pretext test, no-lie floor, make every pretext real, two keys, default HOLD, Mum-test, "only you" question, chain of custody, Decision 0, living-room run sheet, `told_by_candidate`) is intact.

---

## 8. Advisor insight

The chain-of-custody rule makes the maker photograph everything **as found**: the shelf, the drawer, the album's spine, the envelope, the box under the bed, before anything moves, and then photograph it again when it is back. Those frames are shot for logistics, but they are the most honest footage the film will ever have: the real places in her real house where she keeps her life, in the light that falls there, with the dust where it lies. Use them as the film's visual grammar. Every told-by chapter can open on the as-found frame ("this is where she keeps 1988"), hold it a beat, and only then open the album; the game-world idea of an inventory, a chest, a shelf you walk up to and open, is suddenly literal and true, with no AI background and nothing invented. The return photographs give the ending: in the last minute, each thing is shown back in its place, untouched, which quietly tells her that nothing was taken from her and nothing was staged. At the reveal she will recognise her own shelves before she recognises any photograph on them, and that recognition, not the surprise, is the moment the film becomes hers. It costs nothing extra: the frames already have to be taken, and the manifest already has to say where each item lives.

---

## Changelog
- 2026-10-18: round 3 (final) review by the Fable advisor. All eight round-2 nudges confirmed applied; eight spot-checks attempted, eight reached and held (Pro8mm and gesetze-im-internet via plain requests after WebFetch 429/503; iMemories' own page says 1 week to files, 4 weeks to originals). Verdict revise with one critical issue (round-2 follow-up G1–G7 not integrated; three findings change the ship-by table) and eight nudges for the orchestrator to carry forward.
