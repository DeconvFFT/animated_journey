# Fable review — `hindu-visual`, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `CHARTER.md` (Known facts of 2026-10-19), `DECISIONS.md` D-01 to D-31 and the W/O rows the track cites (W-32, W-33, W-38, W-40, W-46, W-55, O-04, O-24, O-27), `reviews/04-hindu-mobile-briefs-review.md` Parts 0 and 1, `research/hindu-visual.md` (700 lines, read in full), `playbooks/hindu-visual.md` (659 lines, read in full), `skills-staging/hindu-visual-language/SKILL.md` (read in full), `research/hindu-visual-fixtures/README.txt` and the licence-excerpt file `research/sources/hindu-visual-licence-excerpts-2026-10-19.txt` (grepped), and `playbooks/cinematic-quality.md` for the decision-5 check.
**Verdict:** **revise** (one critical issue; otherwise close to approval).

Nothing in `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited. No code was written. Nothing was committed.

---

## 1. Spot-checks against the sources (ten claims, all opened today)

The brief asked for at least three. I opened ten, choosing the load-bearing ones: licence terms the film would rely on, iconography a shot would be drawn from, the Sanskrit etymology on a possible card, the respect precedents, and the law the commission paper depends on.

| # | Claim in the artifacts | Source opened (2026-10-19) | Result |
|---|---|---|---|
| 1 | Wellcome plate `phr7cv3d` ("Lakshmi lustrated by two elephants") is CC BY-NC 4.0, ref 26778i, so it is ASK not yes | Wellcome Catalogue API, work `phr7cv3d` | **Confirmed.** Item licence id `cc-by-nc`, label "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)", reference 26778i |
| 2 | Cleveland Open Access: CC0 for images and data, launched January 2019, with exclusions (not digitised, under copyright or artist/donor/lender restriction, not fully owned) | clevelandart.org/open-access | **Confirmed** verbatim on all three exclusions |
| 3 | HAF commercial-use "don't" tier includes footwear "of any type", door mats and rugs, "intended to be stepped upon", alcohol and meat, yoga mats and skateboards; "caution" tier includes non-traditional objects in Nataraja's hands; "outside India" the standards may not be known | hinduamerican.org/?p=2408 | **Confirmed.** Exact phrases present; the "outside India" line is in the introduction, as the research says |
| 4 | Ganesha: usually four arms, axe or goad and noose above, broken tusk and sweet below; trunk turned to his left; one tusk broken; mouse, peacock (Mayureshvara), lion (Vakratunda) as mounts | Wikipedia, Ganesha (first 100,000 characters) | **Confirmed.** "sharply to his left"; broken tusk in the lower right hand; the three mounts named. The article adds that forms range from two to sixteen arms, which T3's "usually four" already allows |
| 5 | Pichwai: Pushtimarg, Shrinathji, Nathdwara, commissioned by the chief priest; no Mughal influence stated in the page read | Wikipedia, Pichhwai | **Confirmed**, with one addition the research missed: the page says the form "originated in the Deccan" and names Aurangabad, and says nothing of Mughal or Rajput court influence. The "origin question" in the playbook is therefore the team's, not the source's (nudge 3) |
| 6 | SJTA complaint at Singhadwar police station, 20 Jan 2026, over AI video of milk poured "with the help of a crane" | Sambad English, 20 Jan 2026 | **Confirmed** on date, station and crane. **Not confirmed:** the article does not say "the first known instance"; that phrase, if anywhere, is in [84] only (nudge 6) |
| 7 | Kangra began when "a family of Kashmiri painters trained in the Mughal painting style sought shelter" at Guler; Sansar Chand a Krishna devotee; "porcelain-like delicacy" | Wikipedia, Kangra painting | **Confirmed** verbatim, so the E10 flag is honestly sourced |
| 8 | Swastika: *su* + *asti*, "all is well"; hakenkreuz; early English *Mein Kampf* substituted the word; drawn at thresholds, washed and redrawn at Diwali, in rangoli, from diyas; orientation not on the HAF page | hinduamerican.org/swastika-reporters-guide | **Confirmed**, including that the page gives no orientation, which the research correctly marks as digest-only from WION |
| 9 | Copyright Act 1957 s.19: writing signed by the assignor; work, rights, duration and territory specified; five years if unstated; India if unstated; lapse after one year unused. s.17(b) and the cinematograph proviso | indiankanoon.org/doc/1136195 (7 June 2012 text) | **Confirmed** verbatim on 19(1), (2), (4), (5), (6) and 17(b) with its proviso. Currency of the text remains UNVERIFIED, as the research says |
| 10 | Tamil Nadu HR&CE eased phone rules 11 Oct 2026 (phones allowed switched off) but "continues to prohibit photography and video recording within temple premises", with a fine | The Star, 11 Oct 2026 | **Confirmed** |

Also checked locally: the scribe's correction 8 ("decision 5's 8% range", left unchecked) is resolved: `playbooks/cinematic-quality.md` `5_camera_grammar` reads "push/pull up to 8%, pan up to 5% of width", so T11 is right and the changelog line can be closed.

**Accuracy reading.** Ten of ten hold; one over-attribution (the "first known instance" phrase). The labelling discipline (S, M, J, UNVERIFIED, digest only) is the best I have seen in this repo, and the three "assumptions the brief made that the sources did not support" at the top of the research note are exactly what a researcher should hand back to an advisor who wrote from memory.

## 2. The Hindu-only rule (D-28), applied with care?

Yes, and kindly. The exclusion list E1 to E26 names an origin for every entry, defaults out, and puts one question to the maker; "the rule governs motifs, not people" is the right reading and protects the commissioning route; dharmic-not-Hindu and Adivasi are flagged as categories, not quietly included; the Mattancherry and church sites of Kerala murals are separated from the style; the Togalu costume flag is specific. The colonial-Christian layer in popular prints is honestly marked UNVERIFIED rather than asserted. Two small inconsistencies: E17 mehndi's default reads "Flag" while every other shared entry reads "Out" (nudge 5), and the pichwai, which is the temple art of her own sampradaya, is held under an origin question that no source read raises (nudge 3). Neither lets a non-Hindu motif in; both make the rule look less sure of itself than it is.

## 3. Deities treated with respect?

The twenty shot rules R1 to R20 are the strongest piece of the track: checkable, sourced where a source exists, (J) where it does not, and with the maker as proxy and default OUT (D-04). "Never mirror" because handedness changes the form is a real craft insight. The ban on any generated or AI-altered deity, with the Puri complaint and HAF's position as evidence, is right and matches D-16.

One slip, and it is the critical issue below: the playbook's Template H3 writes of Mahaprabhuji (Shri Vallabhacharya) "Treat as a person, not a deity, until ruled." The register's D-31 lists him among "the deities of her life", and in her sampradaya his image receives seva. In a public repo that line reads as the team deciding her theology. The fix is easy and must be made before the playbook is approved.

A second, softer slip in the same direction: the Bal Krishna row bans "the clothes-stealing episode and butter gags on screen". Makhan Chor is a svarupa in Pushtimarg homes and the butter lila is painted with vatsalya, not as a gag. R6 (no comic timing, no joke sound) is the right rule; banning the lila itself is a generic restraint placed over her tradition. (Lead from background knowledge; the Pushtimarg sprint confirms.)

## 4. Scores (1 to 5)

| Rubric | Score | Why |
|---|---|---|
| Meaning | 3 | The decision tables are keyed on the unknowns as asked, and "hers beats generic" is stated. But where D-31 is already known, the artifacts still answer pan-Hindu: Mahaprabhuji demoted, the Makhan Chor lila banned, pichwai scored Meaning 2 "if hers" although she is Pushtimarg, Nagara given as her architecture where a Pushtimarg family's temple is a haveli, and sathiyo (the Gujarati threshold swastika) left as a TODO when it is the one floor drawing her hands most likely make. These are the five places the film would stop being hers |
| Specificity | 5 | Form-first iconography sheet, twenty shot rules with the field each validator checks, a measured 4 px floor with the fixture and CSV in the repo, per-record rights routes with the licence text saved, a worked shot brief, YAML block, name-free commission brief, numbered deltas by file and section |
| Accuracy | 4 | Ten of ten spot-checks hold; honest UNVERIFIED and digest-only labelling throughout; one over-attribution ("first known instance") and one source addition missed (pichwai's Deccan origin). The scribe's eight corrections to the research are all right, and I closed the eighth |
| Feasibility | 4 | Symbols-first default, Route A SVG for floor art and symbols, the maker's proxy approval sized to "cut deity shots, not the approval" (Decision 12), commission timing computed against lock and consult. The only strain is hours: screening plates and double-counting attributes is real maker time, correctly surfaced as V8 |
| Ethics | 4 | Respect rules, no generated deity, rights per record, NC and SA as ASK, nothing asked of relatives, shelf photographed only unseen on an unsynced phone, framed prints not photographed. Held back from 5 by the Mahaprabhuji wording and by the mehndi default inconsistency |
| Craft / usability | 4 | The playbook is usable by the maker: templates H1 to H10, exercises with times, decisions with leans and dates, pitfalls, a changelog that separates brief from register. Numbering collisions (S/SW, T/H) caught. The research note is long but every section is reachable from the templates. The skill is tight and points at the right tables |

## 5. Critical issue (blocks approval)

**C1. `playbooks/hindu-visual.md` Template H3, row "Mahaprabhuji (Shri Vallabhacharya)", and Decision 11.** "Treat as a person, not a deity, until ruled" contradicts D-31 (the register lists him among the deities of her life; the register wins) and the respect intent of D-28. Replace with: "Revered in her sampradaya; apply the deity respect rules R1 to R20 *and* the real-person rules of D-16 (no AI, no animated face), whichever is stricter. Form, mark and image convention come from `research/pushtimarg-*`; until then symbol only (P1)." Carry the same wording into the skill's Guardrails and into Decision 11's lean.

## 6. Nudges (at most eight; file, section, exact change)

1. **`playbooks/hindu-visual.md` Template H3, Bal Krishna row; `research/hindu-visual.md` T3, Krishna row.** Change the "Don't" from "the clothes-stealing episode and comic butter gags on screen" to "comic timing, joke sound or slapstick on any lila (R6); the Makhan Chor lila itself is hers if it is on her shelf or in her pichwai (lead: a Pushtimarg svarupa; confirm in `research/pushtimarg-*`)".
2. **`playbooks/hindu-visual.md` Template H1 row 10 and the collapse rule; Decision 1.** Re-score pichwai's Meaning for a Pushtimarg household (the "hers if" is satisfied by D-31); state that the matrix scores were set before D-31 and which rows change. In Decision 1, make the lean "(a) floor art plus (c) set, with (b) pichwai as the painted register for the one shrine moment if O-42 allows P2 or P4", instead of "check-first".
3. **`playbooks/hindu-visual.md` Decision 1, Template H3 pichwai row, Pitfalls; `skills-staging/hindu-visual-language/SKILL.md` Guardrails ("Pichwai origins are unverified [38]").** Resolve the pichwai flag to OK-note on the evidence: the page read [38] states no Mughal or Rajput influence and gives a Deccan origin (Aurangabad named); it is temple art commissioned by the chief priest of her own sampradaya. Keep the two real cautions: it depicts Shrinathji (needs P2 or P4), and it is dense (phone floor).
4. **`playbooks/hindu-visual.md` Template H2 and Step 4; `research/hindu-visual.md` K1 Gujarat row.** Add a "Haveli (Pushtimarg house-temple)" row with silhouette, film use and a TODO keyed to `research/pushtimarg-*`; and a one-line "set leads for her named deities, Saurashtra" row (the Shiva, Krishna and Harsiddhi pilgrimage temples of her region) keyed to `research/saurashtra-*`, marked (J) until that sprint reports. Replace the Tamil Nadu-only photography sentence in Step 4 and in the skill's Privacy guardrail with "temple photography rules are per temple; Tamil Nadu bans it [86]; her temples' rules: TODO(research)".
5. **`playbooks/hindu-visual.md` Template H8 and Template H1 row 1; `research/hindu-visual.md` T9 and the floor-arts row; exclusion list E17.** State plainly (as a lead to verify) that *sathiyo* is the Gujarati word for the swastika drawn at the threshold and on the Lakshmi-puja ledger, so for her Decision 4 is not "a symbol in a mixed room" but "her own hands' threshold drawing, shown or not": phrase the maker's question that way. Change E17 mehndi's default from "Flag" to "Out; ask" so every shared entry reads the same.
6. **`research/hindu-visual.md` Summary item 9 and F5 table; `playbooks/hindu-visual.md` "Why this matters" item 2.** Attribute "the first known instance" to [84] alone (Sambad [83] does not say it) or drop the phrase. In Template H3's Shiva row, replace "Whether a Shiva image sits in a Vaishnava home is TODO(research)" with "D-31 answers it: Shiva is hers; which form is on her shelf is O-38".
7. **`playbooks/hindu-visual.md` Changelog, corrections 7 and 8.** Close 8: cinematic-quality `5_camera_grammar` gives "push/pull up to 8%". For 7, record the lead that T. A. Gopinatha Rao died in 1919 (verify), which settles the public-domain status of the 1914 to 1916 volumes in India and the US without relying on "J".
8. **`skills-staging/hindu-visual-language/SKILL.md` Inputs and Procedure step 1.** Add `research/pushtimarg-*`, `research/saurashtra-*` and `research/gujarati-*` as inputs the skill reads before it defaults, and add to step 1: "where D-31 already answers a key, do not ask again; where a sibling sprint owns the answer (tilak, haveli, sathiyo, Yamunaji's form), cite it rather than guess".

## 7. Research follow-ups (facts the track still needs)

- Pushtimarg visual conventions for a home: the tilak of the sampradaya, the svarupas kept in a Vaishnav home (Lalan/Bal Krishna, Shrinathji chhavi, Yamunaji, Mahaprabhuji's image), their iconography and the seva register (shringar, bhog, Annakut); whether Yamunaji is shown on a tortoise and with what attributes; the haveli as temple form. Keyed to `research/pushtimarg-*`.
- Saurashtra and Bhavnagar-region crafts that her hands may have made: Kathiawar embroidery and mirror (abhla) work, bead work, bandhani, embroidered door torans and chakla wall pieces; and the regional floor art (sathiyo, rangoli at Diwali) with its actual forms. Keyed to `research/saurashtra-*`, feeding K4 and O-40.
- Confirm from a Gujarati source that *sathiyo* denotes the swastika, and record how it is drawn (colour, dots, orientation) so Template H8's SW1 describes her form rather than a generic one.
- Photography and image rules at the temples of her named deities in Saurashtra (Shiva, Krishna, Harsiddhi), for the "her temple" set and for any photograph the maker takes.
- Rao's death year (lead: 1919) to settle public-domain status; and whether the archive.org scans of volumes I.1, I.2 and II.2 are complete.
- Pichwai: the Deccan and Aurangabad origin named in [38], and whether a Gujarat Pushtimarg household's pichwai follows Nathdwara conventions or a Gujarati workshop idiom.
- A measured WhatsApp, Telegram and Signal recompression on an Android phone of her device class (O-43) to replace the two proxies; the mobile-delivery track owns this.
- Whether the Makhan Chor and Navnit Priya forms count as deity figures (P2 to P4) or as symbols (P1) under the maker's policy, since a butter-pot and a tiny footprint may be the honest P1 register for Bal Krishna.

## 8. Advisor insight

Her tradition already has the film's visual grammar, and it is domestic, not monumental: Pushtimarg seva is a day of dressing, feeding and putting a child-god to sleep, with the cloth behind him changed for the season and the festival. That is a pichwai's whole purpose, and it is also the structure of a mother's day. If the shrine moment in the film is her shelf seen at the hours of its seva, with the backcloth changing behind the same small lamp as the chapters pass, the deity policy can stay at P1 (cloth, lamp, butter-pot, tulsi, the folded cloth) and the film still carries her devotion exactly, in her own tradition's register, with no figure drawn, nothing generated, and nothing a stranger in the room could mistake for decoration.

## 9. What is already good enough to carry forward unchanged

The 4 px phone floor and its fixture; R1 to R20; the per-record rights table with the saved licence text; the exclusion list's origin notes; the L0 to L3 deity labelling; the commission paper rule (worldwide, term to the archive, all media including the phone file); the H-numbering and SW-renaming; the deltas table by file and section. Round 2 should touch only the items in sections 5 and 6 and the Pushtimarg and Saurashtra joins.
