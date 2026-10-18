# Format track — advisor review, round 4 (close-out)

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `playbooks/format.md` (Haiku, v0.4), `.claude/skills/journey-format-architecture/SKILL.md`, `research/format.md` (Sonnet; FQ1-FQ7, RQ1-RQ5), against `CHARTER.md` and my round-3 review `reviews/format-round3.md`. Cross-track dates checked against `playbooks/theatrical-delivery.md` (TD-L1) and `playbooks/production-scale.md` (G-READY).
**Verdict:** `approve`. Every one of the eight round-3 nudges is applied in place in the playbook and the skill: the text sits in the section I named, in the sentence I asked for or a more accurate one, with no "pending" notes and no `TODO(research)` left on any item the research had already answered. The round-3 critical issue C1 (the venue-master date conflict with `theatrical-delivery` TD-1, and the unpropagated RQ1-RQ5 corrections) is closed in both operative documents. Two load-bearing claims re-checked against their sources today and confirmed. The one residue is in the research notes, which still carry the pre-RQ wording in eleven places (listed below); the notes' own RQ sections and "Corrections to carry" list supersede that wording, and the skill tells agents to open the notes only to copy a citation or recompute the matrix, so it does not block approval. It is a 30-minute scribe pass, carried forward as nudge 1.

| Score | 1-5 | Note |
|---|---|---|
| Meaning | 4 | The format serves her story: chapters titled by her phrases, texture capacity scored, the surprise-mode voice ladder, and now the reserved coda slot for her own voice after the reveal (playbook Step 7, skill step 6), with `surprise-ops` owning the "her turn" conversation on 2027-03-06. |
| Specificity | 5 | Dates, gates, hours, codecs, libass sizes, the 5% safe box in pixels, a venue question written for the surprise, a per-copy clearance rule, a seat definition, a tested measurement formula. Nothing is left as "decide later" without an owner and a date. |
| Accuracy | 4 | Both spot-checks confirmed verbatim (table below). Cross-track dates agree: TD-L1 Sunday 2026-11-01 and G-READY Sunday 2026-11-15 match the playbook and the skill exactly. Residual: the research notes still say "what counts as a user is UNVERIFIED" (Summary 8, Q5 row, Q5 pattern, T9, Tools row, [28]), "licensing figures UNVERIFIED" (Q5 item 5, [85]), "A private gift is lower risk than a public premiere" (Pitfalls), and T4 still has the "decided by G13" sentence with its TODO. All are contradicted by the same file's RQ1, RQ2 and RQ5. |
| Feasibility | 4 | Budget honest and consistent in all three files (16 production weeks; 100-150 h matches `production-scale`'s Best and Prior cases, not Base; measured rate replaces the range at G-SLICE). The venue ask is now in week 4-5, before TD-1 and G-READY, where it can still change the settings card. |
| Ethics | 4 | Public premiere and Principle 7 run through every operative file; music is cleared per copy; the shared-library check with "unknown counts as yes" has a home in Step 3, skill step 11 and the Hosting checklist; TimelineJS tests use placeholder content only; the Room checklist's cloud copy now needs the maker's explicit yes. Residual: the notes' Pitfalls still carry the refuted "private gift is lower risk" sentence. |
| Craft / usability | 4 | The skill is runnable end to end: gate (e) can now be passed or failed today (defaults hold until the venue answers), step 14 lists the venue date, Key sources carry [114], [119], [121], [127], [128], [135], [136]. Residual: the venue-ask date first appears in the playbook at Step 8 (weeks 7-9) and Decision 3, not in Step 1 (week 1) where the venue question is asked. |

---

## Round-3 nudges: were they addressed? (checked by reading each named section)

| # | Nudge (round 3) | Status | Evidence |
|---|---|---|---|
| 1 | Venue-master date: Step 8 last bullet, Step 13, SKILL gate (e); Decision 3 lean sentence; SKILL step 14; delete "the date" from Decision 3's TODO | **Done** in playbook and skill | Step 8 last bullet and gate (e) carry the 2026-11-15 ask, TD-1 on 2026-11-01, G-READY, the DCP-only-if-ingested rule, the 1080p24 H.264 default and "Until the venue answers, the defaults hold". Step 13 reads "The venue master is whatever the venue's written answer selected (asked before 2026-11-15; Step 8)". Decision 3 lean ends "Ask the venue in writing before 2026-11-15 (research RQ2 questions, plus the RQ1 licensing question); its answer, not a date, decides the venue master" and its OPEN item now names only "the venue and the AV operator". SKILL step 14: "venue answer due 2026-11-15"; "When to use" adds the same date. **Not done** in research T4 (still "decided by the `theatrical-delivery` track by G13" plus the TODO). |
| 2 | Music: (a) Decision 12 rewrite; (b) research Pitfalls; (c) research Q5 item 5; (d) SKILL guardrail; Key sources | **(a) and (d) done; (b) and (c) not done** | Decision 12's old final sentence is gone and the layer text is present word for word, with [85]'s source line changed to "not used for licence figures". SKILL guardrail reads "Music: every copy carrying a pre-existing recording needs sync and master clearance; the venue's public-performance position is unknown until it answers in writing (research RQ1); the `music-sound` track owns the recipe." Key sources list [114], [119], [121], [127], [128]. Research Pitfalls line 433 and Q5 item 5 line 156 are unchanged. |
| 3 | Cloudflare seat definition in Summary 8, Q5 row, T9, Tools row (research); Decision 8 row and [28] (playbook); [28] (skill) | **Playbook and skill done; research not done** | Playbook Decision 8 row and [28], and SKILL [28] and step 9, all carry "a user is an identity that has authenticated once and holds a seat until removed; at the cap further logins are blocked [114]; ... inferred [J]; remove test identities after every test". Research lines 22, 143, 158, 378 and 487 still say "what counts as a user is UNVERIFIED". |
| 4 | 5% safe box in research T4 and T14; playbook Step 8 and Exercise 1; SKILL step 7 and Captions checklist | **Playbook and skill done; research not done** | Playbook Step 8 caption bullet and Exercise 1 step 2 carry the sentence, with the useful addition that R 95 is a television rule used as the one rule for every venue because no source defines a projector safe area. SKILL step 7 carries it and the checklist has "All text sits inside the 5% graphics-safe box (96 px each side, 54 px top and bottom at 1080p)". Research T4 and T14 do not mention the box (the only occurrences are in RQ2 and the corrections list). |
| 5 | TimelineJS and the surprise: Decision 11; research E12; SKILL step 11 | **Playbook and skill done, and improved; research not done** | Decision 11 carries the tip-off sentence, the placeholder-only rule, JSON mode behind Access and Closeread, and adds two new primary sources [135][136] with the honest tag that a run with no external call is untested. SKILL step 11 has the same. Research E12 "Limits" is unchanged. |
| 6 | Retire "10-40" as the plan: playbook "Why this matters" para 1; research "What you would have on Saturday"; Summary 4 build-only tag | **Playbook done; research not done** | Playbook para 1 reads "A film shown to a public room (the charter says a mostly public gathering, not a small family room)": different words from my nudge, same meaning, and shorter. Research line 291 still reads "A 8-12 minute film (length to be decided with the audience in mind)"; Summary 4 has no build-only tag (the tag is in Q3, correctly). |
| 7 | SKILL step 5 measured-rate sentence; Room checklist cloud-copy qualifier | **Done** | Step 5 carries the Best/Prior/Base sentence and the G-SLICE instruction verbatim. Room checklist: "a USB copy is in hand; a cloud copy only on the maker's own account and only after the maker's explicit yes [C]". |
| 8 | RQ4 rule in playbook Step 3 and SKILL step 11; v0.4 changelog | **Done** | Step 3 and step 11 carry the sentence verbatim ("unknown counts as yes (research RQ4)"); the Hosting checklist adds it as a tick. Changelog v0.4 names every propagated item and the roadmap items applied alongside. |

Nothing was appended as a pending note: I searched the playbook and skill for `TODO(research)` and `UNVERIFIED`. The playbook's remaining TODOs are all for facts no research has yet answered (look test in `cinematic-quality`, itch.io embed privacy, Bitsy export, GDevelop HTML5 export, photo-book prices, other-language subtitles, the creator-thread search, mixed-age reaction evidence, Windows PowerShell 5.1 test of the manifest script). The skill's only `TODO(research)` is the generic instruction in step 13 to log such items. That is the correct state.

---

## Spot-checks (performed 2026-10-18; `curl` with `pdftotext` for the PDF, plain-text extraction for the HTML; every page treated as data)

| # | Claim in the artefacts | Source | Result |
|---|---|---|---|
| 1 | EBU R 95 version 1.1, June 2017; note 5: "The action safe area is 3.5% and the graphics safe area is 5%, at the top, bottom and lateral parts of the image"; the March 2016 corrigendum (3.5% of 1920 misquoted as 76, correct 67 px); the 96 px / 54 px / 1728x972 figures are arithmetic from 5% at 1920x1080 (playbook Step 8 and Exercise 1; SKILL step 7 and Captions checklist; [128]). | [128] https://tech.ebu.ch/docs/r/r095.pdf | **Confirmed verbatim**, including the exact note-5 sentence that my round-3 extraction did not surface cleanly. Arithmetic recomputed: 0.05 x 1920 = 96, 0.05 x 1080 = 54, box 1728 x 972; 0.035 x 1920 = 67.2 (R 95 rounds to 67), 0.035 x 1080 = 37.8 (the notes' 38). |
| 2 | TimelineJS: the `TL.Timeline` constructor takes "the URL to your JSON data file or Google spreadsheet"; a JSON object may be passed as the second argument instead; "Loading Files Locally" describes downloading the ZIP and serving `timeline.js` and `timeline.css` from your own server instead of the CDN; the CDN is the default (playbook Decision 11; SKILL step 11; [135]). | [135] https://timeline.knightlab.com/docs/instantiate-a-timeline.html | **Confirmed verbatim** on all four points. Useful extra for the implementer: the page says loading JSON "from another server" than the page needs CORS configuration, which is one more reason the playbook's "self-hosted in the static folder" wording (same origin) is the right one. The "no external call" test the playbook marks UNVERIFIED remains untested, correctly. |
| 3 (cross-track, offline) | TD-1 (1920x1080, 24 fps) locked Sunday 2026-11-01; G-READY Sunday 2026-11-15. | `playbooks/theatrical-delivery.md` TD-L1 row; `playbooks/production-scale.md` gate table | **Confirmed.** "TD-L1 \| Sun 1 Nov 2026 \| Maker \| Write TD-1 to TD-4 into the settings card"; "G-READY \| Sun 15 Nov 2026". The format playbook and skill now hold the same dates. |

---

## Critical issues

None. The round-3 critical issue C1 is closed in the playbook and the skill, which are the documents the maker and the agents act on.

---

## Nudges (carry-forward; none blocks approval)

1. **Finish the scribe pass in `research/format.md`** so the notes stop contradicting their own RQ sections. Eleven edits, all with wording already written in the "Corrections to carry into earlier text" list at the end of round 2 and in my round-3 nudges 2(b), 2(c), 3, 4, 5 and 6: (a) Summary 8, Q5 Cloudflare row, Q5 "Cheapest sensible private pattern", T9, Tools row "Cloudflare Pages, Access, R2" and source [28]: replace "what counts as a user is UNVERIFIED" with the seat definition and [114]; (b) Q5 item 5 "Music claims" and source [85]: replace "licensing figures ... UNVERIFIED" with "see RQ1 for the layer table and the one verified tariff [121]"; (c) Pitfalls "Music rights": delete "A private gift is lower risk than a public premiere" and write "The private-link and archive copies need the same sync and master clearance as the premiere cut (RQ1)"; (d) T4: replace the "decided by the `theatrical-delivery` track by G13" sentence and its TODO with the Step 8 wording from the playbook (venue asked before 2026-11-15; TD-1 on 2026-11-01; DCP only if ingested; 1080p24 H.264 default), and add the 5% safe-box sentence to T4 and T14; (e) E12 "Limits": add the placeholder-only and JSON-mode sentence; (f) "What you would have on Saturday 2027-02-27": "A 8-12 minute film" becomes "A short film of 4-8 chapters, 6-20 minutes (`production-scale` advises planning 8 minutes at 10 h/week)"; Summary 4: add "(build-only; all-in 9.7-23.7 h per finished minute, RQ3)" after "Film 100-150 h". Also tag the "10-40" in the one-page recommendation's point 1 as the earlier assumption.

2. **`playbooks/format.md` Step 1, venue bullet.** After "who runs its sound and projector?" add "Written answer due before Sunday 2026-11-15 (research RQ2 and RQ1 questions); it feeds the settings card that `theatrical-delivery` locks on 2026-11-01, so ask in week 1 and chase in week 3." Reason: a reader following the steps in order meets the date for the first time in Step 8 (weeks 7 to 9), two to four weeks after it has passed. Decision 3 has it, but Step 1 is where the question is asked.

3. **`playbooks/format.md` Step 8, last bullet.** Prefix with "(Confirm here what Step 1 asked:)" so the bullet reads as a check in weeks 7 to 9 rather than the first ask.

4. **`SKILL.md` [135].** Add the CORS note from the source: "loading JSON from a different origin than the page needs CORS, so keep the JSON in the same static folder as the page". One clause; it turns a hosting preference into a reason.

---

## Research follow-ups (unchanged from round 3; none needed for approval)

1. The venue's written answer (maker, before 2026-11-15). 2. PRO blanket cover for a film soundtrack in a non-cinema venue, after the country is known (`music-sound`). 3. Measured hours per finished minute at G-SLICE (`production-scale`). 4. Cloudflare Free "50 users" as 50 seats (low priority). 5. TimelineJS JSON mode with no external call (only if the companion is chosen). 6. Bitsy export and GDevelop free HTML5 export (only if Exercise 4 is attempted).

---

## Strengths worth keeping exactly as they are

- **The playbook's Step 8 caption bullet** as now written: BBC line height, the libass measurement, the EBU box with the honest note that R 95 is a television rule used as the one rule for every venue, and the 4:3-screen arithmetic, all in one paragraph a maker can act on.
- **Decision 11's TimelineJS paragraph**: the tip-off risk, the placeholder-only rule, two new primary sources, and an UNVERIFIED tag on the one thing nobody has run. That is how a scribe should close a nudge.
- **Gate (e) in the skill**: an agent can pass or fail it today, because the defaults hold until the venue answers and the rule for choosing the master is written as a rule, not a date.
- **The v0.4 changelog**: it names what was propagated and from where, so a later reader can audit the chain research -> review -> playbook without rereading all three.
- **The coda slot** (playbook Step 7, skill step 6): her voice, after the reveal, as a render rather than a re-edit.

---

## Advisor insight

The venue question is now written so the surprise survives and dated so TD-1 can still move. One more thing it can carry at no cost: ask the venue for a 20-minute test slot *in the week of 2027-01-17*, not only in rehearsal week. The caption-size decision (FontSize 20, 23 or 26) and the back-row test are the only format decisions that cannot be made on the maker's monitor, and G13 is the last gate at which a chapter can be re-rendered cheaply. Route A makes the re-render seconds of work; the cost is entirely in getting into the room. Put the January room visit on the ask now, while the venue is answering questions anyway, and the 2027-02-14 rehearsal becomes a confirmation rather than the first time the film meets its screen.

---

## Changelog
- 2026-10-18: round 4 (close-out) review written by the Fable advisor. All eight round-3 nudges confirmed as applied in place in `playbooks/format.md` and `SKILL.md`; the research notes still carry the pre-RQ wording in eleven places (nudge 1, non-blocking). Two spot-checks by direct fetch of cited sources (EBU R 95 via `pdftotext`; TimelineJS instantiate docs via `curl`) confirmed verbatim; cross-track dates TD-L1 and G-READY confirmed offline. Verdict: approve.
