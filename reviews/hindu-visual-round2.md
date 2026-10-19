# Fable review — `hindu-visual`, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `CHARTER.md` (Known facts of 2026-10-19), `DECISIONS.md` (D-01 to D-31, W-14 to W-60, O-01 to O-35, Table 4), `reviews/04-hindu-mobile-briefs-review.md` Parts 0 and 1, `reviews/hindu-visual-round1.md`, `research/hindu-visual.md` (Summary, F1 to F6, T3, T9, K1, E17, the full "Follow-up research (round 1)" A1 to A8 and the new sources), `playbooks/hindu-visual.md` (691 lines, read in full), `skills-staging/hindu-visual-language/SKILL.md` (read in full). Also read, because the playbook keys rows to them and they have since landed in the working tree (untracked, dated today): `research/pushtimarg-world.md` (Summary items 2 to 12, F6, F7, F8, PR1 to PR25) and `research/saurashtra-world.md` (Summary, T1 rows P01 to P09, T5, T12, the photography note). `reviews/05-her-world-briefs-review.md` O-46 to O-54 were grepped.
**Verdict:** **revise** (one critical issue; the round-1 work is done and done well).

Nothing in `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited. No code was written. Nothing was committed.

---

## 1. Were the round-1 nudges applied in place?

Yes, all nine, in place and not appended. Checked line by line:

| Round-1 item | Where it now lives | Applied in place? |
|---|---|---|
| C1 Mahaprabhuji "person, not a deity" | Playbook Template H3 row; Decision 11 lean; SKILL Guardrails | **Yes**, the exact wording asked for, in all three places |
| 1 Bal Krishna "Don't" | Playbook H3 Bal Krishna row; research T3 Krishna row (and A8) | **Yes**; the row also adds the honest P1 register (his things) and the footprint R1 check |
| 2 Pichwai re-score; Decision 1 lean | Playbook H1 "scores predate D-31" paragraph, row 10 (4, was 2; 27, was 23), collapse rule; Decision 1 lean "(a) plus (c), with (b) for the one shrine moment if O-42 allows P2 or P4" | **Yes**; the arithmetic (4×2 + 3×2 + 2×1.5 + 2 + 5 + 3 = 27) is right |
| 3 Pichwai flag to OK-note | Playbook Why item, H3 pichwai row, Pitfalls, Decision 1; research F1 row and A6; SKILL Guardrails | **Yes** (one wording caution, nudge 4 below) |
| 4 Haveli row; set leads; photography sentence | Playbook H2 two new rows; Step 4; Pitfalls; research K1 two new rows and A4; SKILL Privacy | **Yes**; Somnath's own FAQ was opened and is now [118] |
| 5 Sathiyo as her word; E17 | Playbook Why, H1 row 1, H8 "Her word", Decision 4, E24; research T9, F1 floor-arts row, A3; E17 now "Out; ask" in both files | **Yes**; honestly labelled a dictionary-level lead, with the Gujarati-Wikipedia null results recorded |
| 6 "first known instance" to [84] alone; Shiva row | Playbook Why item 2; research Summary 9 and F5 table; H3 Shiva row "D-31 answers it" | **Yes** |
| 7 Changelog 7 and 8 | Changelog correction 7 (Rao 1872 to 1919 [127]; II.2 is a reprint) and 8 "Closed" | **Yes**; A5 goes further and finds the II.2 scan is a Motilal Banarsidass reprint whose uploader's CC0 field clears nothing |
| 8 SKILL Inputs and Procedure step 1 | Inputs bullet 4; Procedure step 1 last sentence | **Yes**, verbatim |

The follow-up research section (A1 to A8) is the right shape: each answer says what was opened, what it says, what stays UNVERIFIED, and which playbook sections changed. The implementor was honest that the search allowance was spent and worked from direct fetches only.

## 2. Spot-checks against the sources (eleven, all opened today)

| # | Claim in the artifacts | Source opened (2026-10-19) | Result |
|---|---|---|---|
| 1 | *Sathiyo* is a Gujarati masculine noun, "(Hinduism) swastika, a religious symbol", from Sanskrit *svastika*, doublet of સ્વસ્તિક; entry last edited 1 March 2023 | English Wiktionary, સાથિયો | **Confirmed** on every point |
| 2 | T. A. Gopinatha Rao (1872–1919); *Elements* 1914 | Wikipedia, T. A. Gopinatha Rao | **Confirmed**; the page gives only "1914" for the book, so "1916" for Vol. II stays unconfirmed, as A5 says |
| 3 | Wikipedia's Tilaka page lists "Vallabha Sampradaya Tilaka" by name with no description; urdhva pundra "two or three vertical lines ... intercepted in the middle by an elongated U"; tripundra "three horizontal bands ... with a single vertical band or circle in the middle" | Wikipedia, Tilaka | **Confirmed** verbatim (the playbook's "crossed in the middle" paraphrases "intercepted"; harmless) |
| 4 | Pushtimarg: icons installed "not in temples (mandir) but in mansions (havelī)" (Barz; Ho disagrees); nine major svarupas including Navanītapriya; the initiate is given a *kaṇṭhī* of tulasi | Wikipedia, Pushtimarg (to the 100,000-character cut and its tail) | **Confirmed** verbatim; no tilak description anywhere on the page (see research follow-up 1) |
| 5 | Yamuna, per the Agni Purana: "black in complexion, standing on her mount, the tortoise, and holding a water pot in her hand" | Wikipedia, Yamuna (goddess) | **Confirmed**; the page's own source is Vettam Mani's *Puranic Encyclopaedia* p. 894, worth adding to [113] |
| 6 | Somnath Trust: "Photography is strictly prohibited"; "All the Electronic/Electric Equipment, Gadgets are strictly prohibited" (mobile, camera, smartwatch, laptop, tablets, calculators); lockers in the cloak room | somnath.org/faq | **Confirmed** verbatim |
| 7 | Bala Krishna "a small child crawling on his hands and knees, or dancing with a piece of butter in his hand" | Wikipedia, Balakrishna | **Confirmed**; the page does not name Makhan Chor, Navanitapriya or Pushtimarg, so the svarupa link rests on [109], as A8 says |
| 8 | Pichwai: "originated in the Deccan, but are now mainly associated with Western India"; Aurangabad "another area associated with them"; made "only on commission by the chief priest"; no Mughal or Rajput influence mentioned | Wikipedia, Pichhwai (redirected from "Pichwai") | **Confirmed**. The page names Udaipur, Jaipur and Jodhpur only as the artisan sub-castes' places of origin |
| 9 | (Not claimed by the track; checked because it bears on the OK-note) | Wikipedia, Nathdwara painting | "The Nathdwara school is a subset of the Mewar school of painting"; Mughal rule appears only as the reason the image moved to Nathdwara. So "no Rajput influence stated" is true of [38] alone; the track's own [114] already places Nathdwara painters in the Mewar school (nudge 4) |
| 10 | Harsiddhi: present temple at the foot of Koyla Dungar near Miyani, near Porbandar; Jagadu, 13th-century Kutch merchant; page tagged as needing citations | Wikipedia, Harsidhhi | **Confirmed** on location, builder and tag. The page's kuldevi sentence reads "Kshatriya and Rajputs from Kathiyawad or Saurashtra"; A4's "many Kshatriya, Brahmin, and Vaishya" was not on the page as served today (research follow-up 5) |
| 11 | Takhteshwar 1893, on a hill, "high shikhara rising above the pillared rectangular mandapa"; Gangajalia white marble in a former tank | Wikipedia, Bhavnagar | **Confirmed**. Note for E4: the page calls Gangajalia a Ganga-Devi temple "with a chhatri": a Hindu temple pavilion in her own city, exactly the "named Hindu" exception E4's question anticipates |

**Accuracy reading.** Ten of eleven hold verbatim; one paraphrase drifts (the kuldevi list). The OK-note wording "no Mughal or Rajput influence stated" is true of the page it cites and is contradicted by nothing read, but the track's own source [114] says Mewar school, and Mewar is the one Rajput idiom E10 does *not* flag ("the most traditionalist", pre-Mughal Chaurapanchasika group [37]). The honest sentence is slightly longer (nudge 4); the resolution itself stands.

## 3. The Hindu-only rule (D-28), applied with care?

Yes. Nothing non-Hindu was let in by round 1's changes. The pichwai resolution rests on the page read; E27 (mirror work) was added with its "citation needed" origin honestly shown; E17 now reads like every other shared entry; the haveli row borrows no jharokha, jaali, chhatri or cusped arch; the sathiyo is treated as her hands' drawing and still left to the maker and the room. The saurashtra sibling independently reached the same E2 position (a multifoil lintel of five lobes or more stays out) and offers the Kashmir-and-Chaulukya argument as one question to the maker, which is the right way to carry an ambiguous motif.

## 4. Deities treated with respect?

Round 1's slips are fixed: Mahaprabhuji is revered under the stricter of R1 to R20 and D-16; the Makhan Chor lila is hers, not a gag; Shiva is hers by D-31. R1 to R20 stand.

The new problem is a join, not a slip. Since the follow-up was written, `research/pushtimarg-world.md` has landed in the working tree. It is the sprint this playbook keys to, and the playbook still says in three places that it "is not in the repo on 2026-10-19". That sprint's reverence rules (PR1 to PR25), sourced to the sampradaya's own FAQ and a Nathdwara painter's account, contradict the playbook in three places that are about respect, and the playbook's own new rule (SKILL step 1: "where a sibling sprint owns the answer, cite it rather than guess") now binds it. That is the critical issue below.

## 5. Scores (1 to 5)

| Rubric | Score | Why |
|---|---|---|
| Meaning | 4 | The five places where the film stopped being hers are repaired: Mahaprabhuji, the lila, pichwai re-scored for a Pushtimarg home, the haveli and her region's temples in H2, sathiyo as her hands' drawing. Held from 5 because the shrine moment, the one place her sampradaya's grammar matters most, is still written against the sibling that now describes it |
| Specificity | 5 | Unchanged from round 1 and sharper: A5's folio counts, A7's ffprobe method for the maker's own run, the P1 object list for Bal Krishna, the per-temple photography table |
| Accuracy | 4 | Ten of eleven spot-checks verbatim; labels honest throughout; one over-tight sentence (OK-note "no Rajput influence") and one paraphrase drift (Harsiddhi's kuldevi list); the "not in the repo" lines are now stale |
| Feasibility | 4 | Nothing added costs maker hours beyond round 1's estimate; the P1-first default keeps deity work small; the commission remains (a) or (d) |
| Ethics | 3 | Step 6 route (3), Pitfalls "Privacy", Exercise 1 and SKILL Privacy still instruct the maker to photograph "her shelf" unseen on an unsynced phone. For a Pushtimarg shelf the served Thakorji, Lalan or chitraji is, in her tradition's own words, a living child in the house, and the sibling that owns this answer says firmly no (PR4, F6). A maker following this playbook as written could do the one thing her sampradaya would find presumptuous, in secret. The fix is small; the score reflects the consequence, not the size |
| Craft / usability | 4 | Playbook, research and skill agree with each other; templates are usable; the changelog is honest. Held from 5 by the stale "not in the repo" statements, which would send an agent to a TODO that is now answered |

## 6. Critical issue (blocks approval)

**C1. Join the playbook to `research/pushtimarg-world.md` where its reverence rules contradict this track.** The sibling now exists (untracked in the working tree, dated 2026-10-19); the playbook's SKILL step 1 rule applies. Three contradictions, each with the exact change:

(a) **The unseen shelf photograph (P3).** `playbooks/hindu-visual.md` Step 6 route (3), Decision 2 option P3, Pitfalls "Privacy", Exercise 1 step 4 wording, and `skills-staging/hindu-visual-language/SKILL.md` Procedure step 5 and Guardrails "Privacy". Replace "her own photograph of a three-dimensional murti or lamp on her shelf, taken on an unsynced phone" with: "her own photograph of seva *objects* that are not a svarupa (the lamp, the jhari in its red cloth, the thali, the folded cloth) on an unsynced phone; **never the Thakorji, Lalan, chitraji or any picture of hers without her knowing** (`research/pushtimarg-world.md` PR4, F6: a picture may be *pusht* and in seva, and the film cannot tell by looking). A svarupa still enters only if O-52 says yes and she knows, which under D-02 means the April version at the earliest." Carry the same sentence into the H6 route table row "The maker's own photograph of her shelf" and the H10 checklist.

(b) **Pichwai without its deity.** H3 pichwai row ("shown without him it changes meaning (J)"; Don't: "a pichwai shown without its deity under P1"), Decision 1 ("under P1 it drops out"), Pitfalls "A pichwai without Shrinathji". The sibling's sourced finding is the reverse: in the temple "Shrinathji himself is never painted into the pichwai"; the cloth is cut where he stands [its 35, 32]. So the usable register under P1 is the pichwai-*manner* border, bands and night sky, and what must never appear is the niche or opening around or behind a person (PR5) or a face in the centre. Rewrite the three places: "Under P1, the pichwai register is border, bands and sky with an object of hers or text at the centre; never the niche; never behind a face (PR5). The figure, not the cloth, is what P1 drops." Add the season rule as one line in H1 row 10 and Decision 1: painted pichwai only for Sharad and Gopashtami chapters; white-and-gold for Diwali and Annakut; none in winter (PR23, its Summary 2). Decision 1's lean then reads "(a) floor art plus (c) set, with (b) the pichwai-manner frame for cards and the shrine moment under P1; a painted svarupa only as P4 by a hereditary painter who paints the day's shringar".

(c) **R3 versus padukaji.** Template H4 R3 ("no footwear in a frame with a shrine ... unless it lies at the threshold") would fail the one Pushtimarg seva object the P1 list already names (padukas). Add to R3: "Padukaji (Mahaprabhuji's and Gusainji's footwear and footprints) are seva objects, not footwear: never below the knee, never worn; R3 does not apply to them (`research/pushtimarg-world.md` PR11)". Mirror it in SKILL Guardrails "Respect".

Also replace, in Gaps "Added by this draft" (two bullets), Changelog, research A-section header and SKILL Inputs, the sentence "is named in CHARTER.md but is not in the repo on 2026-10-19" with "`research/pushtimarg-world.md` and `research/saurashtra-world.md` are in the working tree (untracked) as of 2026-10-19; `research/gujarati-*` is not yet"; and key each TODO(research) to the sibling's section (tilak T8; haveli F2 and T3; Yamunaji F8; Mahaprabhuji F7; Takhteshwar and Harsiddhi `saurashtra-world.md` T1 P01, P08).

## 7. Nudges (at most eight; file, section, exact change)

1. **`playbooks/hindu-visual.md` Template H3, Yamuna Maharani row.** Replace the P1 candidate "the dark line of the river" with "the jhari holding Yamunajal, covered in red cloth (`pushtimarg-world.md` F8, PR20); never a local sea, gulf or river standing in for her, and never a Ganga-like white figure". Keep the tortoise and pot as the Agni Purana form; add that in the haveli's own pictures she is dressed like Shrinathji (its [15], UNVERIFIED against print).
2. **`playbooks/hindu-visual.md` Template H3, Mahaprabhuji row, "Ask her image" cell, and Decision 11.** Cite the sibling's leads instead of "no description": rosary in the right hand and lotuses in the other (a devotee gallery, its [9]), white garment and counting beads (a c. 1750 portrait, digest); never on one seat or level with a svarupa (its PR19, from the FAQ's Seva Q35); padukas and footprints as seva objects (PR11). Keep P1 until the maker rules.
3. **`playbooks/hindu-visual.md` Template H3, Marks paragraph.** After "its shape is UNVERIFIED", add: "`research/pushtimarg-world.md` T8 proposes a double vertical red line rounded at the base, attributed to Wikipedia citing Brill; I could not find that sentence on the Pushtimarg, Vallabhacharya or Tilaka pages today (research follow-up 1); treat T8 as the drawn reference for the maker's own sighting, never as settled."
4. **`playbooks/hindu-visual.md` Why item (last paragraph), H3 pichwai row, Decision 1, Pitfalls; `SKILL.md` Guardrails "Hindu only".** Change "no Mughal or Rajput influence stated" to "the page read names no Mughal or Rajput influence [38]; the Nathdwara school is a subset of the Mewar school [114 and Wikipedia, Nathdwara painting], the one Rajput idiom E10 does not flag [37]". Same meaning, honest about [114].
5. **`playbooks/hindu-visual.md` Template H2, "Set leads" row, and research K1 third Gujarat row.** Takhteshwar is a Shiva temple on `saurashtra-world.md` T1 P01 (two pages, one of them the city tourism page): change "(a Shiva temple is J)" to "(S, `saurashtra-world.md` P01)". Add the sibling's photography line: no page states a rule for Takhteshwar, Nishkalank, Gopnath or Harsiddhi (UNVERIFIED); Somnath [118] stays the one read rule.
6. **`playbooks/hindu-visual.md` Template H3, Maa Ambe and Harsiddhi row.** Add from `saurashtra-world.md` T1 P07 and T4: Ambaji's worship centres on the Visa Yantra with no anthropomorphic murti (so P1 is not a compromise there, it is the form), and Mata ni Pachedi names neither Ambe nor Harsiddhi (never present that cloth as theirs). Correct A4's kuldevi phrase to the page's wording ("Kshatriya and Rajputs of Kathiawad") or mark it UNVERIFIED.
7. **`playbooks/hindu-visual.md` Decision 2 options and Template H5 `deities_on_a_public_screen`.** Add the sibling's sharper tier wording so the two tracks ask the maker one question, not two: P2 and P4 for a *svarupa* only as a hereditary painter's work in the day's shringar (its PR2); O-52 (review 05) is the Pushtimarg form of O-42 and should be cited beside it.
8. **`playbooks/hindu-visual.md` Sources [38] and [113]; `SKILL.md` [38].** Title the page as served, "Pichhwai" (redirected from "Pichwai"), and add to [113] that Wikipedia's Yamuna description cites Vettam Mani, *Puranic Encyclopaedia*, p. 894, so R19's printed-source rule has a lead.

## 8. Research follow-ups (facts the track still needs)

1. **The tilak sentence.** `research/pushtimarg-world.md` item 9 attributes "double vertical red line which is rounded at the base" to Wikipedia citing Brill; `research/hindu-visual.md` A1 and my own reads of the Pushtimarg (to its tail), Vallabhacharya and Tilaka pages found no such text today. Which page, which revision, and does the Census of India 1911 image (Commons `Vallabhachari_tilak.png`) agree? To be opened in the maker's own browser.
2. **Photographing a home svarupa at all.** The sibling's "no" rests on reverence and D-02/D-17 with "no norm found against photographing" on record. One sampradaya FAQ page or printed seva guide that speaks to photographing Thakorji would settle whether the April version may include her own picture with her yes, or never.
3. **Mewar conventions inside the pichwai manner.** Since Nathdwara is a subset of the Mewar school, which Mewar conventions (flat ground, bold line, the pre-Mughal idiom E10 admits) do the border, bands and sky carry, so the E10 line can be drawn per element rather than per cloth?
4. **E4 test case.** Gangajalia in Bhavnagar is a Ganga-Devi temple with a chhatri (Wikipedia, Bhavnagar). Is it hers (O-38), and if so is its chhatri the kind of named Hindu pavilion E4's question allows?
5. **Harsiddhi's kuldevi communities.** Reconcile A4's "many Kshatriya, Brahmin, and Vaishya" with the page's "Kshatriya and Rajputs from Kathiyawad or Saurashtra"; find a second source for the Koyla Dungar image itself (stone, murti or other), which no page read describes.
6. **Shrinathji's Patotsav on Sat 27 Feb 2027** (`pushtimarg-world.md` Summary 1, from the sampradaya's tippani). This track's seasonal register for the title and end card (white, colour only at Gwal, no painted pichwai in Vasant) should be checked against that day once `hindu-frameworks` rules on it.
7. **Carried from round 1:** a measured WhatsApp, Telegram and Signal recompression on her device class (the mobile-delivery track; A7 gives the maker's method); the Gujarati-language confirmation of *sathiyo* and how her hand draws it (TODO_maker, never guessed).

## 9. Advisor insight

Her tradition has already solved the film's hardest deity question, and the answer is a closed door. A Pushtimarg home mandir keeps its doors shut between darshans; the sibling records that the two doors are read as the eyelids of Swaminiji, and that closed doors on screen are allowed where an opening onto a person is not (PR6). A haveli's Anavasara, the three hours after Rajbhog when the doors close, is a true, quiet state of both a temple and a home. If the film's shrine moment is the closed doors of her own mandir at the hours her household closes them, with the jhari in its red cloth and the lamp outside, then the audience sees devotion kept, nothing in seva is shown, no figure is drawn or generated, and she is the one person in the room who knows what is behind the doors. That is also the exact grammar of W-37's locked rooms: a place the film visibly does not open. The deity policy can stay at P1 and the shot still belongs to her alone.

## 10. What is already good enough to carry forward unchanged

Everything round 1 listed, plus the follow-up research's method (fetch, quote, label, say what changed), A5's reprint finding, A7's maker-run protocol, A8's P1 object register for Bal Krishna, the two new H2 rows, and the sathiyo handling. Round 3 should touch only C1 (a) to (c), the eight nudges above and the "not in the repo" lines; nothing else needs reopening.
