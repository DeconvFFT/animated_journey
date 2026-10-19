# Review: `devotional-sound-script`, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `research/devotional-sound-script.md` (846 lines, v0.2 with the "Follow-up research (round 1)" section), `playbooks/devotional-sound-script.md` (716 lines, v0.2), `skills-staging/devotional-music-and-indic-scripts/SKILL.md` (111 lines), the fixture folder `research/devotional-sound-script-fixtures/` (README as revised, `ab.srt`, `shaping_fixture.srt`, the uncommitted diff of the README), against `CHARTER.md`, `DECISIONS.md` (D-01 to D-31 re-read; W-01 to W-22), `reviews/04-hindu-mobile-briefs-review.md` Part 3 (the brief) and `reviews/devotional-sound-script-round1.md` (the eight nudges).
**Verdict:** **approve.** Scores: meaning 4, specificity 5, accuracy 5, feasibility 4, ethics 5, craft 4. All eight round 1 nudges are applied in place; ten of ten spot checks hold; nothing critical is open.

Nothing personal is added by this review. Every household fact referred to is in `DECISIONS.md` D-31 and `CHARTER.md` Known facts, cited as D-31. The city the register names is not repeated here, and the artifacts do not repeat it either.

---

## 1. The eight nudges, checked in place

| # | Nudge (round 1) | Where it now sits | In place? |
|---|---|---|---|
| 1 | Brief: "short private tribute film" becomes "short tribute film"; last line adds "It will be shown to an audience; the signed letter covers public exhibition." | Playbook T-6 (the brief's first and last lines); research Template H lines 415 and 420 | **Yes.** No "private" remains in either brief (grep). D-18 and D-08 are now satisfied. |
| 2 | A/B cue `ab.srt` as non-sacred test syllables only, plus "never run the FAIL or `shaping=simple` render on a mantra, a deity's name, an aarti line or a Vedic verse" | Playbook T-8 item 6 and Exercise 2; SKILL.md Guardrails "Respect" and Procedure step 9; fixture README commands 3 (new CAUTION) and 3b; research Template K items 2 and 8; `ab.srt` exists (two lines: `શ્રી ક્ષ જ્ઞ ધર્મ કિ ક્ષિ` and `क्ष त्र ज्ञ धर्म कि क्षि`) | **Yes.** The README also gained the right caution on command 3 (the full fixture SRT holds sacred strings; run 3b first; on a failing build burn only through `ass`). The research note's Follow-up 8 records that `ab.srt` separates the cases on 6.1.1 (545 px simple against 386 px ass). |
| 3 | Skill step 4: shehnai and Carnatic violin move to `ASK`; the skill's two lists equal T-4 | SKILL.md step 4: "Sitar, sarod, santoor and khayal default to out. Harmonium, tabla, bansuri, tanpura, ektara, the shehnai and the Carnatic violin default to `ASK`." Playbook T-4 header states the same two lists; D4 agrees | **Yes.** An agent on the skill and the maker on the playbook now reach the same default. |
| 4 | Navaratri and garba re-cited to [93]; Pushtimarg page [89] cited for Holi, Janmashtami, Nagapanchami, Annakuta | Playbook T-11 row "O-39 festivals she keeps"; research D-31 update table row "Festivals"; Follow-up 5 confirms the tail of [89] was read and Navaratri is absent | **Yes.** Confirmed today against [89] (section 2 below). |
| 5 | Strings table: TODO(research) cells replaced with the fixture strings; changelog corrected | Playbook "Sanskrit and regional-language strings" table: `श्री कृष्णः शरणं मम` / `શ્રી કૃષ્ણઃ શરણં મમ` (cues 1 and 7), `मातृदेवो भव` (cue 1), `यमुनाष्टकम्` / `યમુનાષ્ટકમ્` (cues 1 and 7), each with its fixture cue and source; Changelog v0.1 bullet "Fixtures" now says the implementor read the README and `shaping_fixture.srt` (v0.2) | **Yes.** No "TODO(research)" remains in that table (the only TODO left in the playbook is the honest Gaps list). |
| 6 | `COMMON_OPTIONS` becomes `SHAPING_OPTIONS` macro expanded into both option tables at n9.0 and n9.0.2 (default -1, `auto`) | Research Summary 1(a) and Q10 first bullet; playbook T-8 "Why the ffmpeg version matters"; source [96] records the re-read | **Yes.** No `COMMON_OPTIONS` remains except inside [96]'s list of search terms, which is correct. |
| 7 | Split `CHURCH_COLONIAL` into `CHURCH` and `COLONIAL_EUROPEAN`; harmonium `COLONIAL_EUROPEAN` ("missionary channel: 'possibly' per [44]; unproven"); Carnatic violin `COLONIAL_EUROPEAN (UNVERIFIED)`; `ASK` kept | Research Template A (line 224) and Template C (header and rows I-19, I-21); playbook T-1 and T-4 (header, I-19, I-21); SKILL.md step 4 defines both flags | **Yes.** No `CHURCH_COLONIAL` remains anywhere except in the two changelog lines that record the split. Template C's header adds the honest line "no instrument in this sheet carries CHURCH". |
| 8 | Restore the S-13 caveat: asking a temple's permission tells someone a recording is being made; default record from the public hall only where openly allowed without asking; otherwise skip S-13 and use S-02 | Playbook T-3 row S-13 and Step 7; SKILL.md "Capture" guardrail; research Template I row S-13 and Follow-up 7 (which adds "a posted sign, not a person's say-so" and "never inside a sanctum") | **Yes.** The duplicated sentence in Step 7 is also gone. |

The two smaller edits of round 1 were handled honestly: Step 7's repetition is removed; the tanpura one-liner for the Sun 25 Oct sitting and the advisor insight were **not** applied, and the changelog says so rather than claiming otherwise. Neither was a nudge; they stay as suggestions (section 6 carries the insight forward).

The follow-up answers live in a new, clearly labelled section at the end of the research note ("Follow-up research (round 1)"), with a "Sections changed by round 1" table that names every in-place edit by file and section. New research in a new section, corrections in place: that is the right shape.

---

## 2. Spot checks (opened 2026-10-19 by WebFetch and one local PDF extraction; ten claims, ten hold)

| Claim in the artifacts | Source opened today | Result |
|---|---|---|
| `मातृदेवो भव` is in the Taittiriya Upanishad, Shiksha Valli, eleventh anuvaka, rendered "Be one to whom a mother is as god" (playbook strings table; research [104]) | `en.wikipedia.org/wiki/Taittiriya_Upanishad` (first 100,000 characters) | **Holds.** Eleventh Anuvāka of the Shiksha Valli, the convocation address; translation "Be one to whom a mother is as god, be one to whom a father is as god" (I.11.2). |
| "Sukhakarta Dukhaharta" is a Marathi Ganesh aarti credited to Samarth Ramdas (1608 to 1682), citing Golesar (Lokprabha, 2012) and Shanbag, *Prarthana* (2007) (T-2 N7; research Follow-up 2 [103]) | `en.wikipedia.org/wiki/Sukhakarta_Dukhaharta` | **Holds** on composer, dates, deity, language and both references. |
| Garba: a circle dance round an image of Amba or a clay pot with a flame; "the dhol and dholak (Indian drums), cymbals and shehnai"; part of Navaratri (T-2 N8 [93]) | `en.wikipedia.org/wiki/Garba_(dance)` | **Holds** on all three. (The page's infobox also lists sitar and singing, which the artifacts do not cite; no change needed.) |
| Pushtimarg page: festivals Holi, Janmashtami, Nagapanchami, Annakuta; Navaratri, garba and Diwali not named; the aṣṭākṣara mantra `śrī Kṛṣṇaḥ śaraṇaṃ mama` repeated 3 times in the first ceremony; eight darśanas Maṅgalā to Śayana; dhol songs sung by lay Gujarati devotees, particularly women (T-2 N2, N3, N11; T-11 O-39; research D-31 table) | `en.wikipedia.org/wiki/Pushtimarg` | **Holds** on every point, and the round 1 re-citation (nudge 4) is confirmed: Navaratri is not on the page. The fixture strings `श्री कृष्णः शरणं मम` and `શ્રી કૃષ્ણઃ શરણં મમ` match the page's IAST letter for letter (visarga, anusvāra). |
| Vallabhacharya died 1530; the Yamunashtakam is the first of the sixteen treatises, "an esoteric hymn to the river goddess Yamuna which is recited daily by followers" (T-2 N4 [90]) | `en.wikipedia.org/wiki/Vallabhacharya` | **Holds** (page: 7 May 1478 to 7 July 1530; a 1473 birth per Gokulanātha's followers). The note's "1478 or 1479" is close; the page's variant is 1473. Cosmetic. |
| Stability AI Community Licence: free commercial use under USD 1M annual revenue; Stable Audio 3.0 is a listed model; outputs owned by the user; footer "© Stability AI Ltd, 2026" (playbook D14, Pitfalls [61]) | `stability.ai/license` | **Holds** on all four. The page shows no licence version or effective date, as the artifacts say. |
| The independent portal: "Mobile phones, electronic cameras, smart watches" strictly prohibited; "not operated by, affiliated with, sponsored by, or endorsed by the Nathdwara Temple Board"; eight darshans with hours and ragas (Mangla Bhairav, Vibhas, Ramkali; Gwal Todi, Devgandhari; Utthapan Multani, Dhani; Shayan Bihag, Kedar, Darbari Kanada) (T-2 N1, N2; research Follow-ups 1, 5, 7 [100]) | `shrinathdwara.in/darshan/` | **Holds** word for word, including the raga sets the note attributes to it and the hours it says differ from [97]. |
| Freesound 466652: CC0 temple bell, 30.5 s (T-3 S-02 stand-in [37]) | `freesound.org/people/ganiket/sounds/466652/` | **Holds** ("Indian Temple Bell.WAV", 0:30.544, "Creative Commons 0", recorded in Himachal Pradesh 2019). Correctly a labelled generic stand-in, not hers. |
| "Vaishnava Jana To": Narayan Khare, musician at Gandhi's Sabarmati ashram, set it in the 1920s in Mishra Khamaj; the page gives no dates for him (T-2 N6; research Follow-up 3 [92]) | `en.wikipedia.org/wiki/Vaishnava_Jana_To` | **Holds**; no dates for the arranger, so UNVERIFIED on his death year is the right label and the Follow-up 3 term table is the right shape. |
| The 2026 paper [97]: "Melodic support is often provided by the Harmonium"; "during Mangla seva, tanpura is played only"; Haveli Sangeet "performed without rhythm instruments" in its soft form; Murali in the list of instruments of divine service; talas "Chautal, Dhamar, Sooltal, ..." (T-2 N1, T-4 I-11 and I-19; research Follow-up 1) | `sangeetgalaxy.co.in/.../29.-Rohit-Kumar.pdf` (the fetch tool could not read the PDF stream; the file was saved and its text extracted locally with pdftotext: Sangeet Galaxy vol. 15 no. 2, July 2026, pp. 191 to 199, ISSN 2319-9695, Rohit Kumar, Central University of Punjab) | **Holds** on every quoted phrase. The harmonium's presence in her sampradaya's temple music therefore rests on a non-Wikipedia source as the note says; the bansuri "contested" label is right: Murali is in the paper's list and the paper states no exclusion. |

Not re-checked and left as the artifacts mark them: the round 1 checks (FFmpeg source at n8.1.1 and n9.0, Great 78, Suno, ElevenLabs, Cornell term table, Gyan page, Haveli Sangeet page, Om Jai Jagdish Hare, Phillauri), the Copyright Act section numbers, the IPRS and PPL facts, and the fixture measurements. Festival dates belong to `hindu-frameworks` and this track correctly defers to it.

---

## 3. The Hindu-only rule (D-28) and respect, checked again

- **No Mughal, Islamic or Christian motif enters.** Unchanged from round 1 and still correct: ghazal and qawwali out; khayal, sitar, sarod, santoor out as showpieces; Ragamala images out while the raga-by-hour idea is a label only; no raga name on screen; Desh avoided; Gurbani, Jain and Buddhist material "dharmic, not Hindu; ask"; Tagore and Nazrul kept out of the Shakta line.
- **The flags now say exactly what the sources say.** The `CHURCH` flag is defined and carried by nothing; the harmonium is `COLONIAL_EUROPEAN` with the "possibly" caveat quoted from [44]; the Carnatic violin is `COLONIAL_EUROPEAN (UNVERIFIED)`. The harmonium's place inside her own sampradaya's temple music is now sourced to a peer-reviewed paper and a field study, which makes the O-41 question to the maker sharper and more honest, not softer.
- **Sacred text is protected in the instruction, not only in the exhibits.** The maker's own A/B now runs on `ab.srt` (test syllables), the full fixture SRT carries a CAUTION, and the never-run-FAIL rule is in the playbook, the skill, the README and the note. The committed exhibit PNGs still carry only test syllables.
- **The temple is never told.** S-13 now defaults to skip; "a posted sign, not a person's say-so" is the right reading of D-03.
- **The brief no longer says something untrue.** D-18 is met.
- **Voices (D-05)** unchanged and correct: only instrumentals before April; the 1906 record and the 1963 Suprabhatam routed to T10, lean out.

No soft spot remains that rises to a nudge.

---

## 4. Critical issues

None.

---

## 5. Nudges

None required for approval. Three cosmetic edits the scribe may make in the next pass, not counted and not blocking:

- `research/devotional-sound-script.md` Template C header lists the flags as "NONE, SHARED, COURT, SUFI, CHURCH, COLONIAL_EUROPEAN, UNVERIFIED"; Template A and the playbook's T-1 also carry `DHARMIC_NOT_HINDU`. Add it to Template C's header so the three vocabularies are identical.
- `research/devotional-sound-script.md` Template N row N1 and D-31 table: "dated 1478 or 1479 to 1530 [90]" could read "1478 (or 1473 per Gokulanātha's followers) to 1530 [90]", which is what the page gives.
- `playbooks/devotional-sound-script.md` T-4 header says "The skill's two lists equal the Default column"; the Default column also carries the conditional rows I-08 (chenda, ask only if Kerala) and I-09 (dhak, not hers). Say "equal the Default column's out and ASK rows" so the sentence is exact.

---

## 6. Research follow-ups (questions needing new facts)

1. **The printed source for haveli sangeet is identified, not read:** Gaston, *Krishna's Musicians* (Manohar 1997; 2023 edition per [97]) and Sharma (2010, Hindi, pp. 105 and 134, per [97]) for the instrument list and the raga set per darshan. Reading either would close I-11's "contested" and give the sound sheet a sourced `tradition_set:<darshan>:<source>`.
2. **Authorship and date of "Jai Adhya Shakti"** and of the Shiva, Lakshmi and "Jai Ganesh Deva" aartis (still not found; "Shivanand Swami, 18th century" stays UNVERIFIED). Until then only "Om Jai Jagdish Hare" and, if hers, "Sukhakarta Dukhaharta" may be captioned.
3. **The death year of Narayan Khare**, arranger of the common "Vaishnav Jan To" tune (1938 UNVERIFIED); the term table in Follow-up 3 is ready to be keyed on it.
4. **Her Android model, OS version and the player she watches in (O-43)**, then the cable test of `ab.srt` as sidecar and burn-in on her device class (Follow-up 4).
5. **The PC A/B on the maker's Gyan 9.0.2 build** (README command 3b) with `ffmpeg -version`, the `Raster: FreeType` line and PASS or FAIL recorded in a T8 note, by Sun 1 Nov.
6. **A Gujarati reader's judgement on Mukta Vaani's half-form conjuncts** before it captions anything; the maker can be that reader.
7. **Which of the eight darshans her household keeps at home, and at what hour she rings the bell** (the round 1 insight; one question on Sun 25 Oct, answered from the maker's own knowledge, D-03).
8. **The sound of a Pushtimarg home's own daily sevā** (not read in either pass): what a household shelf's morning actually sounds like in her tradition, from a printed or scholarly source, so S-01 to S-03 are keyed to her practice and not to a generic puja.

---

## 7. Advisor insight: the women's songs are the one sound in her tradition that is hers to hum

The note found it and then filed it under "none (D-05)": the dhoḷ songs of Gujarat, which [89] and Mallison (1986) describe as sung by lay devotees, "essentially if not exclusively by women", at daily work, in leisure groups, and **at marriages and births**, outside the formal temple liturgy. Everything else in Template N is the temple's or a label's. This is the one genre that belongs to the women of a household like hers, sung in the kitchen and at the cradle, in Gujarati, with no instrument and no priest.

D-05 bars a recording of living voices, but W-44's first source after silence is `HER_TUNE_HUMMED`: the maker's own hum of a tune she sang. So the question for the maker on Sun 25 Oct, under O-41, is not "which bhajan does she play" but: *"Which song did the women of the house sing at a birth or a wedding you were present for, and can you hum it?"* If the maker can, that hum is the MOTIF cue of the whole film: a melody she herself sang at the maker's own birth or at a wedding in the family, carried by the maker's voice (no living voice of anyone else, no instrument to flag, no label to clear if the tune is traditional, with `composition_status` to be settled per rule 5), and its first line on a two-line verse card in Gujarati with the maker's plain line beneath. It is the sound of her tradition that nobody has to ask a temple for, and it answers Principle 2 better than any raga: a stranger in the room will not know what a dhoḷ is, but will hear a son humming his mother's song.

Two guards: the maker confirms the tune is traditional and not a film or album setting before it enters the cue map (Pitfalls, "a hum is not free"); and the card text is copied from a source or from the family's own book, never from memory (Guardrails, "Respect").

---

## 8. Scores and what moves them

| Rubric | Score | Why |
|---|---|---|
| Meaning | 4 | Re-keyed to D-31 throughout; the harmonium question is now sourced inside her own sampradaya; the darshan clock and the dhoḷ songs are both in the tables and both wait on one maker question each. A 5 needs the maker's Sun 25 Oct answers, which no artifact can supply. |
| Specificity | 5 | Measured, hashed, cue-numbered; every nudge landed on the exact line; the follow-ups report what was and was not found. |
| Accuracy | 5 | Ten of ten spot checks hold, including the one macro and the one citation that slipped in round 1; every unread source is named as unread; UNVERIFIED and "contested" are used exactly. |
| Feasibility | 4 | Free tools; a ten-minute A/B and an hour on the PC; fonts are a download; nothing waits on a person outside the project. Holds. |
| Ethics | 5 | D-18 met in the brief; sacred text protected in the instruction; the temple never told; flags say no more than the sources; D-05, D-16, D-17, D-02, D-03, D-07 applied to every row. |
| Craft / usability | 4 | Skill and playbook now agree on every default; no TODO the fixture answers; changelog truthful about what was and was not applied; README commands carry the right caution. The playbook is long but navigable by its T-numbers; a condensing pass is still worth doing when the maker starts using it, not before approval. |

**Approved.** Round 3 is not needed for approval; it may be used, if the orchestrator wishes, to fold in the maker's Sun 25 Oct answers (O-38, O-39, O-41, O-43) and the PC A/B result, and to apply the two advisor insights (the darshan clock and the hummed dhoḷ) if the maker takes them.
