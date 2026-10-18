# Review: `surprise-ops` — round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; reveal Saturday 2027-02-27)
**Reviewed:** `research/surprise-ops.md` (researcher: Sonnet, 1046 lines), `playbooks/surprise-ops.md` (scribe draft v1, 716 lines), `.claude/skills/surprise-tribute-operations/SKILL.md` (165 lines), against `CHARTER.md` and my brief in `reviews/01-addendum-briefs-review.md` §2.4.
**Verdict:** **revise** (round 1). This is the strongest track so far on ethics and specificity; the revisions are narrow and all are fixable by the scribe in one pass. Nothing here needs a new research run except two small follow-ups.

---

## 0. Spot-checks (what I verified today, 2026-10-18)

Method: WebFetch, one WebSearch, one `curl` (Pro8mm rate-limited WebFetch twice), and local `pdftotext` on the OHA PDF. Fetched pages treated as data.

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | Legacy Digital: $19.95 special / $28.50 regular per two-hour tape, ~6 weeks "anticipated, not a hard date", $50 minimum, $35 kit, ~12.5 GB MP4 per tape; page dated 2026-09-05 [44] | legacydigital.net/legacy-video-transfer/ | **Verified**, except the page now shows **updated October 17, 2026** (prices unchanged). Still no holiday cut-off. Update the source date. |
| 2 | Pro8mm: standard 5–7 business days "schedule & volume permitting"; rush 1–3 days for $250 per film type; unscheduled home-movie discount 4–8 weeks (20% off); film held 30 days then recycled unless storage is bought; return shipping only if purchased; price shown "$0.62 - $2" with no unit [46] | pro8mm.com/products/scan-super-8mm-8mm-to-digital (curl) | **Verified verbatim** ("All film unclaimed after 30 days will automatically be recycled"). Price unit still not stated on the page. |
| 3 | OHA Statement on Ethics: adopted October 2018, PDF © 2025; narrator may delete, restrict, redact, add clarifications, correct mistakes, keep closed until a date [8] | oralhistory.org PDF (text extracted locally) | **Verified** (lines 11–17 and 133–134 of the extracted text). Consent "be recorded prior to the beginning of the interview" is also there (line 57). |
| 4 | Surrogates predict patient preferences ~68% of the time; 16 studies; designated no better than default; prior discussion did not help [60] | pallimed.org 2006-03-13 | **Verified.** Pallimed adds that the "discussion doesn't help" finding rests on two uncontrolled trials, which the notes should carry. |
| 5 | Windows 11 DND can turn on automatically "when duplicating the display"; per-app "Hide content when notifications are on lock screen" [24] | support.microsoft.com (notifications page) | **Verified**, Windows 11 section. |
| 6 | Ramadan 2027 projected to begin about Feb 8, 2027, UAE Astronomy Centre, subject to moon sighting; Eid ~Mar 9–10 [72] | thenationalnews.com, published 2026-09-09, updated 2026-10-06 | **Verified.** |
| 7 | "BitLocker is only on Pro, Enterprise or Education, not Home… Home users need a third-party tool, UNVERIFIED" [26] | support.microsoft.com (BitLocker page) and the "Device encryption in Windows" page | **Partly wrong by omission.** The BitLocker page says exactly that, but Microsoft's Device-encryption page says Device Encryption is "available on a wider range of devices, including those running Windows Home", "enables BitLocker encryption automatically for the Operating System drive and fixed drives", turns on automatically on first sign-in with a Microsoft account, and **is not turned on automatically for a local account**. It says nothing about removable drives, so the external project drive on Home is the real gap, not the whole PC. |
| 8 | Hanukkah "in this week" (week 10, Dec 20–26) marked (M) in the notes and TODO in the playbook | WebSearch (My Jewish Learning, Farmers' Almanac and others agree) | **Wrong.** Hanukkah 2026 begins at sundown **Friday Dec 4** and ends **Saturday Dec 12, 2026**: weeks 7–8 of the plan, where the notes schedule "last big interviews" and the **Fri Dec 11 contributor soft deadline**. The holiday rules (Table E) only cover weeks 10–11. |

Internal checks (no web needed): every weekday/date pair in the Key-dates table is correct (Jan 1 2027 Fri, Jan 24 Sun, Feb 6 Sat, Feb 27 Sat, Mar 6 Sat, Mar 29 Mon, Apr 24 Sat, Thanksgiving Thu Nov 26, Christmas Fri). Ash Wednesday 2027 = Feb 10 and Easter = Mar 28 are also correct, but keep them marked (M) until a source is cited. `life-story-interviewing` and `playbooks/ai-imagery.md`, both referenced, exist. Whisper is the local transcriber named in `research/story.md` Q8, so playbook Decision 9's "tool is not named here (TODO)" can simply point there.

---

## 1. Scores (1–5)

| Criterion | Notes | Playbook | Skill | Track |
|---|---|---|---|---|
| Meaning | 4 | 4 | 4 | **4** |
| Specificity | 5 | 5 | 4 | **5** |
| Accuracy | 3 | 3 | 3 | **3** |
| Feasibility | 3 | 3 | 4 | **3** |
| Ethics | 4 | 4 | 5 | **4** |
| Craft / usability | 4 | 4 | 4 | **4** |

**Why these numbers.**

- *Meaning 4.* The track keeps her agency at the centre (quiet word, stop signal, private cut, "her turn" conversation, consent ledger she closes), which is exactly Principle 5. The "only you" question is the one gathering device that feeds the *piece* rather than the operation; nothing yet connects what is gathered to the chapter structure.
- *Specificity 5.* Eight relationship kits with scene-coded prompts, a dated week-by-week plan, scripts for the quiet word and the no-lie floor, a decision sheet, a run sheet with roles. This is the most usable set of templates any track has produced.
- *Accuracy 3.* Seven of eight spot-checks held, labelling of snippets and inference is exemplary, and the scribe flagged conflicts rather than hiding them. But two errors reach the schedule and the device checklist (Hanukkah in the wrong week; Windows Home encryption misdescribed), one internal contradiction reaches the headline ethics rule (Summary 5 says "never any recording of her"; Q2 test 6, Card E and the reveal say "not without her knowledge"), and one mislabel reaches the skill: the lab formula computes a **ship** date (transit sits inside the two-week allowance), yet Summary 7, the playbook's table heading and skill Procedure 9 call it "receive-by". A maker following the skill literally could post a slow-lab batch a week late.
- *Feasibility 3.* The plan ships a pilot tape on **Fri Oct 30** (twelve days from now) and starts interviews in week 2, while the maker has said material gathering waits until the pipeline is locked, and the playbook itself says "do the six exercises before you ask a real relative for anything". All three cannot be true. My brief (§1.6) argued the covert slow parts must start now; that is still right, but the playbook must put the trade-off in front of the maker as a decision, not schedule over the maker's stated preference. Separately, the run sheet needs seven named roles (MAKER, QUIET WORD, TECH, HOST, CAMERA, DISTRACTOR, PROXY) even though Decision 12 leans to a living room or family dinner.
- *Ethics 4.* The six-condition pretext test, the no-lie floor, "make every pretext real", two keys with substituted judgment, default HOLD, her post-reveal veto, no synthetic voice, no face animation of the dead: this is a careful reading of Principles 4 and 5 and I endorse it (answers to the researcher's four questions are in §4). The one point off is the unresolved rule in the notes' own summary; the skill already states the right rule ("any secret recording" is unacceptable).
- *Craft 4.* The skill's description names the triggers an agent will actually meet (contributor brief, pretext card, auditing a shared device, sending items to a lab, running the reveal) and the "When not to use" list is sharp. The procedure is followable. It inherits the receive-by mislabel and could carry a one-line "told-by" field (nudge 8).

---

## 2. Critical issues (block approval)

1. **Hanukkah is in the wrong week.** It is Dec 4–12, 2026 (weeks 7–8), not week 10. The notes' "last big interviews" week and the Fri Dec 11 soft deadline fall inside it, and the holiday rules do not apply there. Fix the dates and make the holiday rules apply to *any observance the family keeps*, by name, not only to weeks 10–11.
2. **"Receive-by" versus "ship-by".** Table D's formula (Jan 24 − lab weeks − 2 weeks transit and handling − 2 weeks holiday margin) yields the Friday the parcel must *leave*; the notes' Summary 7, the playbook's table heading and Step 8.2, and skill Procedure 9 and its checklist call it the date "the lab must have the item". Pick "ship-by", define it once, and propagate.
3. **The schedule overrides the maker's stated sequencing without saying so.** The maker said collection comes after the pipeline is locked. The plan must state, as Decision 0, which four things cannot wait (insider suitability check; rings, code name and project email; the Mum-test; the lab pilot and ship-by dates) and what is lost if everything waits (slow and mid labs drop out after Nov 13 / Nov 27; interviews compress into weeks 6–13). Then the maker chooses.

---

## 3. Nudges (at most 8, each with file, section and exact change)

1. **`research/surprise-ops.md`, T4 Table C and Table E; `playbooks/surprise-ops.md`, Key dates and Holiday rules.** Move Hanukkah to "Fri Dec 4 (sundown) to Sat Dec 12, 2026" in weeks 7–8; delete the TODO on the Dec 25 row; retitle Table E / Holiday rules "weeks 10 and 11, Thanksgiving week, and any observance this family keeps (ask in Step 1)"; add a note under week 8 that the Dec 11 soft deadline may need to move a week either way for a family that keeps Hanukkah.
2. **Terminology: "ship-by".** `research/surprise-ops.md` Summary 7 and Table D heading ("Latest send-by dates" → "Latest ship-by dates"; keep the "leaves her house" column); `playbooks/surprise-ops.md` heading "Receive-by dates for labs" → "Ship-by dates for labs", Step 8.2 (delete the TODO; replace with "ship-by = the Friday the parcel leaves; the lab's confirmed receipt date is what you log"), Key dates rows for Oct 30, Nov 13, Nov 27, Dec 4, Dec 11, Dec 18; `skills/surprise-tribute-operations/SKILL.md` Procedure 9 and "Before each lab order" ("Receive-by date computed" → "Ship-by date computed; lab's receipt date logged when confirmed").
3. **`playbooks/surprise-ops.md`, new "Decision 0" placed before Step 1 and mirrored at the top of "Decisions you'll need to make".** Title: "What starts now, and what waits for the pipeline." Two columns: *cannot wait* (insider check; rings, code name, project email; Mum-test; lab terms in writing and the pilot) and *can wait for pipeline lock* (interviews proper, album sessions, contributor wave 1). State the cost of waiting in one line per lab class using the ship-by table. Then rewrite Step 6's "weeks 2 to 12" and Step 7's "weeks 2 to 13" as "from Decision 0's start week". Also reconcile "do the six exercises first" with the Oct 30 pilot: Exercises 1 and 4 are the prerequisites for the pilot; the other four precede the first real interview.
4. **`research/surprise-ops.md`, Summary 5 and the Q1 channel table; `playbooks/surprise-ops.md`, Decision 10.** Replace "never any recording of her" with "no recording of her without her knowledge and a spoken yes; the only two planned cases are an announced recorder at a family-stories evening (Card E) and a wide shot of the room at the reveal if she agrees in the quiet word". Close Decision 10 with lean (b) and point to the consent card, which already matches. The skill needs no change.
5. **`research/surprise-ops.md`, Q4 "Windows PC in a shared room" row and Open questions 21; `playbooks/surprise-ops.md`, Step 4.6 and Pitfalls.** Correct the encryption line to: "Windows Home lacks BitLocker Drive Encryption and BitLocker To Go [26], but has **Device Encryption** for the OS and fixed drives, turned on automatically on first sign-in with a Microsoft account and *not* for a local account (Microsoft, 'Device encryption in Windows'). So the internal drive can be protected on Home; the external project drive cannot be, without a third-party tool (see research follow-up)." Add the consequence: the recommended separate project Windows user, if created as a local account, does not get Device Encryption by itself.
6. **`playbooks/surprise-ops.md`, Reveal-day run sheet; `research/surprise-ops.md`, T5.** Add a "living-room version" above the full sheet: three roles at most (maker; the quiet-word person; one person who is tech and host), S−2h / S−30 / S−20 / S / end / pause, and state that the seven-role sheet is for the 30+ setting. Decision 12 leans to a small room, so the default sheet should fit it.
7. **`research/surprise-ops.md`, Sources [44], [60] and [12]; `playbooks/surprise-ops.md` and the skill's Sources mirror.** [44]: "page updated 2026-10-17; prices re-checked 2026-10-18, unchanged." [60]: add "Pallimed notes the 'discussion did not help' finding rests on two uncontrolled trials." [12]: add "the page shows a 2026 publish date on a 2023 URL; treat the date as unknown." Also, in playbook Decision 9, replace "the tool is not named here (TODO(research))" with "Whisper or whisper.cpp, per `research/story.md` Q8 and Recipe 3".
8. **`research/surprise-ops.md`, T6 consent ledger and T1.0 "After"; `skills/surprise-tribute-operations/SKILL.md`, Procedure 6.** Add one field to the interview sidecar and one column to the consent ledger: `told_by_candidate` — "could this be the one story this person tells, in their voice, as the spine of a chapter?" (yes / maybe / no, plus the chapter). This is the only change needed for the gathering to feed the "told by" structure proposed in review 01 §4, and it costs the maker ten seconds per interview.

---

## 4. Answers to the researcher's four questions for the advisor

1. *Is the six-condition pretext test a sufficient reading of Principle 5, or should she be told a project exists (hybrid)?* The test is sufficient for the surprise the maker has chosen, **provided condition 4 holds strictly**: nothing she says under a pretext enters a hard chapter. The no-lie floor plus the partial-reveal line ("Yes, something for you…") is in effect a *latent* hybrid: the moment she asks, she knows a project exists. That is the right design. Do not add an unprompted disclosure; the maker chose full surprise and story.md's deadline to change mode (Nov 1) stands.
2. *Should the reveal offer a private viewing first by default?* Not by default: offer it as the first of the two questions in the quiet word, as drafted. Make it the default only if the insider check (Step 1) reports that she dislikes being the centre, or if any chapter is SHARED-LIGHT rather than top-drawer.
3. *Is "default HOLD" right given that it costs contributors their moment?* Yes. The asymmetry argument is correct. Soften the cost, not the rule: a HOLD item can still carry a contributor's *voice* in the shared cut on a top-drawer story, and the full item waits in the private cut. Tell contributors at the Feb 15 confirmation which cut their clip is in, so no one is surprised in the room.
4. *Do two keys overcomplicate a small family?* Keep two keys for hard chapters only; in a family of three or four adults the second key may be her oldest friend rather than a relative. One key for everything else. The playbook already says this in Step 2; make it explicit that the second key sees only hard-chapter drafts, not the film.

---

## 5. Research follow-ups (facts not in the notes)

- Free, open-source encryption for an **external** drive on Windows 11 Home (VeraCrypt is the obvious candidate): current version, licence, Windows 11 24H2 status and whether a non-admin project user can mount it. Only then can nudge 5 name a tool.
- Whether Device Encryption on Home covers a second **local** user's profile once it is on for the machine (Microsoft's page says automatic enablement needs a Microsoft-account sign-in; it does not say what happens for additional local users).
- Pro8mm's price unit for "$0.62 – $2" (per foot is likely but the page never says).
- Baylor [12] publication date (the page shows 2026 on a 2023 URL).
- Already open and still needed: UK/EU/cross-border recording-consent baseline; audio-cassette and answering-machine capture; one or two first-hand Reddit accounts if a route to them opens.

---

## 6. Strengths worth keeping exactly as they are

- The **six-condition pretext test** and the **no-lie floor** with its two scripted answers: this is the clearest statement of the project's ethics anywhere in the repo.
- **"Make every pretext real"** (she gets the labelled photos, the family page, the playlist).
- **Two keys, substituted judgment, default HOLD, her veto after the reveal**, with the consent ledger as the mechanism that closes Principle 5's gap.
- The **Mum-test** as a repeatable audit with sourced controls (shared libraries, Family calendars, Alexa order read-outs, Dropbox notifications, OneDrive folder backup).
- The **"only you" question** with its ladder and exit.
- **Honesty about evidence**: fetched vs snippet, (M), UNVERIFIED and inference labels used consistently; the scribe surfaced conflicts instead of resolving them silently.
- The **chain-of-custody** rule: photograph the shelf, spine and every spread *before* touching anything.

---

## 7. Advisor insight

Card A (photo labelling) is written as cover. It is also the one place in the whole plan where she **knowingly contributes to the film with her own hand**. Have her write the names, places and years on paper slips or archival labels herself, in pen, during the labelling afternoon, and photograph each slip at 600 ppi beside its photo. Those slips become the film's title cards and captions: the only text in the piece in her handwriting, acquired truthfully, disclosed at the reveal ("you labelled your own film"). It satisfies Principle 4 (real, hers), Principle 5 (she chose every word on screen that is hers), and the "told by" structure from review 01: every chapter is told by someone else in their voice, but every chapter is *named* by her. The final chapter's card is then a blank slip in the keepsake, with a pen, waiting for her version. Operationally it changes one thing: Card A must happen early (it is the first truthful window anyway) and the slips must be scanned, not typed.

---

## Changelog
- 2026-10-18: round 1 review written by the Fable advisor. Eight spot-checks (§0); verdict revise with three critical issues and eight nudges.
