# music-sound — round 3 of 3 review: approved; the research has moved ahead of the playbook, and the orchestrator carries the deltas

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `playbooks/music-sound.md` (v0.3, round 2 applied), `skills/life-film-music-and-sound/SKILL.md`, `research/music-sound.md` (1,292 lines, now with the round-1 follow-up F1–F9 and a new round-2 follow-up G1–G8), against `CHARTER.md`, my brief in `reviews/02-film-briefs-review.md` §1.4, my round-2 review, and the sibling files the track joins to (`playbooks/film-story.md` beat-sheet header and `hard_flag` values; `playbooks/agent-pipeline.md` gate files in `reviews/<chapter>/`; `research/surprise-ops.md` T9; `playbooks/surprise-ops.md` consent card).
**Maker's standing instruction (verbatim, relayed by the harness):** "for now only me and i will only bne the one on this project." Honoured in all three documents: no second keeper, no co-approver, the maker signs off the D2 wording and takes the consult alone (research round-2 context note).

**Verdict: approve.** All eight round-2 nudges were applied in the files and sections they named, including the critical consistency issue C1: the project now holds one consent card, one found-voice header and one spotting header. Six of six readable spot-checks confirmed verbatim. Every rubric score is 4 or higher and nothing critical is open. What remains is the opposite of round 2's problem: the researcher's round-2 follow-up (G1–G8) brought primary evidence that the playbook and skill do not yet carry, and the scribe said so in the changelog ("Still open, not applied here"). Those are listed below as carry-forward nudges for the orchestrator. None of them changes a decision; each makes the playbook match its own source.

---

## 1. Round-2 nudges: were they addressed?

| # | Nudge (short) | Status | Evidence |
|---|---|---|---|
| 1 | Research Deliverable 3d and F6: replace the long card with the playbook D2 text; tier C a written ask | **Addressed** | 3d now headed "replaces the long card, withdrawn 2026-10-18; use playbook Template D2", prints the one sentence, answers A and B, removals to Fri 2027-02-19, and "Tier C … is a written ask after the premiere; nothing about them is promised before the maker's own post-premiere release." F6's closing paragraph reads "using the D2 card, answer B; tier C is a written ask after the premiere." No "(C) Wider" line remains anywhere in the file. |
| 2 | Research 3e and Deliverable 2 headers identical to Templates D3 and B | **Addressed** | 3e header is byte-identical to Template D3 (`addressed_to` after `who_speaks`, `public_cut_eligible` before `use_decision`, values `as_recorded | private_only | none`). The spotting header carries `source_in_her_life` after `function`; the worked row C07 is filled with "[beat-sheet evidence ID] (illustrative: a relative named the waltz)". |
| 3 | Summary 13, Q9, tools row, F7 and source [8]: retire the 02-14 rehearsal, "January mix", "unless started late", "S3 … to 02-12" | **Addressed** | Summary 13: "unknown until the Mon 2027-02-22 run on the real chain (surprise-ops run sheet)". Q9: "to cover the 13–20 Feb mix (G-MIX to G-MASTER)". Tools row: "A trial started 2026-12-28 ends 2027-02-26 and covers the mix; buy the $60 licence to remove the timer". F7: "S3 from G-LOCK 2027-02-06 to mix v1 at G-MIX 2027-02-13, masters by G-MASTER 2027-02-20". Source [8] in both lists: "rehearsal dates (2027-02-14 to 02-20) are retired for this track as of 2026-10-18". A grep for `2027-02-14` returns nothing outside those retirement notes. |
| 4 | Skill 4a and playbook Step 5: flag file and `hard_flag`/`advisor_flag_ref` columns | **Addressed** | Step 5: `cue_map.csv` columns `beat_id, cue_type, source_in_her_life, hard_flag, advisor_flag_ref, notes`; `hard_flag` copied from the film-story beat sheet (values NONE, SHARED-LIGHT, PRIVATE, HOLD, OUT, which match `playbooks/film-story.md` line 211); flag line to `reviews/<chapter>/sound-flags.md` as `beat_id | proposed cue | why not silence | date`. Skill 4a mirrors it. The join on `beat_id` is real: film-story's header has `beat_id` and `hard_flag`. |
| 5 | DX-gated check over speech spans only | **Addressed** | Step 15, Template G check row and commands, skill Procedure 13 and the master checklist all say "speech spans only (the `voice_present=yes` rows of `spotting.csv`)", per chapter or concatenated, 6 LU kept as the starting threshold and labelled inference, per-chapter offset recorded; Template H adds the back-row comparison line. Research Deliverable 4 and its venue checklist point to the same rule. |
| 6 | D2 routing: a dated surprise-ops patch, not "next round" | **Addressed** | Template D2 Routing, Decision 6 and the skill's Secrecy guardrail all name "the orchestrator patches `playbooks/surprise-ops.md` … by Saturday 2026-11-07", one week before the 2026-11-14 gate, "until that patch lands, D2 is not read and no relative is recorded for the public cut." Research G4 confirms the owner and date and records that the surprise-ops playbook has not yet been patched (I confirmed: no D2 text in `playbooks/surprise-ops.md` today). |
| 7 | REAPER $60 personal-use condition | **Addressed** | Decision 7, Template J row 2026-12-28, research Q9, the tools row and source [103] all carry "an individual, and REAPER is only for your personal use" plus the $20,000 commercial threshold, and the lean reads "buy the $60 licence (personal use qualifies); start the trial only to defer the spend to 2026-12-28". |
| 8 | HER-PUBLIC / HER-PRIVATE beside tiers 1 and 2; T9 path | **Addressed** | Core principle 1 writes "Tier 1 (HER-PUBLIC)" and "Tier 2 (HER-PRIVATE)", keeps `yes`/`no` as the column values, and gives the T9 path `research/surprise-ops.md` T9 (I confirmed T9 there is the corrections ledger and the post-reveal conversation). Template D3 definitions and skill Procedure 8 use the same words. |

Eight of eight. The research changelog now has the "deltas applied from round 1" line I asked for, so the two documents carry a record of each sync.

---

## 2. Spot-checks (fetched today by direct fetch; PDFs read with pdftotext)

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | EBU R 128 s4 (November 2023): Loudness-to-Dialogue Ratio of Cinematic Content "should not exceed 5 LU"; with LDR ≤ 5 LU and dialogue at -23 the programme "can maximally reach −18.0 LUFS"; "explicitly not intended as production advice for feature films"; cinema playback "explicitly not considered" (research G3) | https://tech.ebu.ch/docs/r/r128s4.pdf | **Confirmed** verbatim: "First published November 2023"; recommendation j) "the Loudness-to-Dialogue Ratio of Cinematic Content should not exceed 5 LU"; "(with LDR ≤ 5 LU, it can maximally reach −18.0 LUFS)"; "It is explicitly not intended as production advice for feature films"; "programmes for playback in cinemas are explicitly not considered". |
| 2 | Udio Terms of Service "Last Revised on November 12, 2025"; "You may not download copies of any Output"; Output "solely for your personal and non-commercial purposes"; Udio "own[s] all right, title and interest in and to the Services and the Output"; licence over Your Content "worldwide, perpetual and irrevocable"; no exploitation "for any commercial purpose" (research G6) | https://www.udio.com/terms-of-service (HTTP 200; text extracted from the server-rendered page data, as the researcher did) | **Confirmed**, all six strings present verbatim. The researcher's method note is accurate: the fetch tool's extractor shows only the title. |
| 3 | GEMA Tarif T version 46, valid from 2026-01-01: 1.3% of net ticket revenue; minimum EUR 30.40 up to 150 people, EUR 60.80 up to 300, EUR 30.40 per further 150; 15% discount for cultural or social events; rates apply only if consent is acquired "rechtzeitig vor Beginn der Nutzung"; consent "unter der Voraussetzung" that the film-music rights were properly acquired; a generative-AI clause putting the burden of proof on the licensee; covers screenings "außerhalb von Filmtheatern" (research G7) | https://www.gema.de/de/musiknutzer/tarifuebersicht/tarif-t and the linked tarif_t_version46.pdf | **Confirmed.** The HTML page links "Tarif T, gültig ab 01.01.2026"; the PDF reads "1,3 % des Nettokartenumsatzes", "bis 150 Personen 30,40", "bis 300 Personen 60,80", "je weitere 150 Personen 30,40", "erhalten einen Nachlass von 15 %", "wenn die Einwilligung der GEMA rechtzeitig vor Beginn der Nutzung erworben wird", "Die Einwilligung wird unter der Voraussetzung erteilt, dass das Recht zur Verwendung der Musik in den vorzuführenden Filmen …", section "6. Generative Künstliche Intelligenz (genKI)". |
| 4 | Stability AI Community Licence: under $1M annual revenue; commercial use allowed; "you own outputs"; Stable Audio 3.0 listed; Enterprise above $1M (playbook Decision 4, research Q3) | https://stability.ai/license | **Confirmed**: "creators with less than $1M in annual revenue"; "allows for research, non-commercial, and commercial use of the Core Models"; "as between you and Stability, you own outputs"; "Stable Audio 3.0" in the Community list; "revocable if you violate its terms". The page shows no effective date (footer "© Stability AI Ltd, 2026"), so the notes' "Undated" tag is right. |
| 5 | REAPER 7.82 (2026-10-04); 60-day evaluation "with full functionality"; $60 discounted licence for "an individual, and REAPER is only for your personal use" or commercial gross revenue ≤ USD $20,000; $225 commercial (Decision 7, Q9, [103]) | https://www.reaper.fm/purchase.php | **Confirmed** verbatim, including the personal-use condition added this round. The page also offers the $60 licence to educational and non-profit organisations, which the notes may ignore. |
| 6 | Freesound FAQ: CC0 no restrictions; CC BY requires credit; CC BY-NC bars earning money; AI-generated uploads permitted "marked with the GenAI tag and the model is indicated in the description" (Exercise 7, Pitfall and source [75]) | https://freesound.org/help/faq/ | **Confirmed** verbatim. |

Six of six confirmed. The ASCAP cue-sheet page stays untested by me, as agreed in round 2 (403 on three attempts; routed to the maker's browser). Accuracy of the sourced material is as high as any track in the project.

---

## 3. Scores

| Dimension | Score | Why |
|---|---|---|
| Meaning | 4 | The Principle 2 test reaches sound (`source_in_her_life`, "no MOTIF or CLOCK without one"), silence is the default under hard chapters, her found voice is gated by "would she play this to strangers", and the object-sound asks make the ambience hers. Held at 4 by what I said in round 2 and did not nudge: the cue map has no field for *why* a non-hard beat got its sound, and the motif brief (Exercise 8) does not name the maker's hummed tune as a candidate source. Neither needs a round; both are notes for the beat-sheet pass in November. |
| Specificity | 5 | Tested commands, a 36-column log, dated gates, a worked spotting row, a two-tier rule with column definitions, a six-column cue map that joins to the beat sheet, three loudness columns with a fader protocol, and now a primary LDR anchor and a GEMA tariff with worked arithmetic. |
| Accuracy | 4 | Six of six spot-checks verbatim; the four stale schedule sentences are gone; UNVERIFIED and "not re-read" tags remain exact. Held at 4 because the playbook and skill still say things their own source has since settled: Decision 4 says Udio's "primary terms could not be read (UNVERIFIED)" and Step 2 says GEMA practice "was not read", while research G6 and G7 read both from primary pages today. The conclusions do not change (Udio is out; the country decides the tariff), so this is staleness, not error. |
| Feasibility | 4 | Schedule runs from the real gates; composer from lock is ruled out and dated; REAPER covers the mix with or without the trial; Resolve Free is a second route with a memory cap and a result sheet (G5); the machine part of a re-conform is measured at under half a minute per chapter (G8), so the human listen-through is the real cost, as F7 assumed. The 13–20 Feb mix week is tight and said so. |
| Ethics | 5 | One consent card across the project; tier C never spoken; removals to 2027-02-19; her found voice default-out for the public cut under one key and three guards; family audio never leaves the PC, now with a primary-source reason for Udio too (a perpetual, irrevocable licence over anything uploaded); AI never sings her songs or imitates a voice; the sole-keeper instruction honoured without inventing a second approver. Up from 4 now that C1 is closed. |
| Craft / usability | 4 | The mix spec holds the theatrical bar: cinema level kept apart from LUFS, stems, fold-down, the fader protocol, the story-free calibration reel, the DX check now measured where dialogue exists. The skill's description triggers on the right nouns (cue, song, AI music, temp, voice recording, mix, rights) and its procedure is followable by an agent, with the flag file and the join key in place. Held at 4 by three usability gaps the research has already solved and the playbook has not absorbed: the LDR aim (5 LU) and the negative-reading caveat, the RapidCue usage vocabulary for Template C, and the G8 dry-run row in Template J. |

All six at 4 or above; nothing critical. **Approve.**

---

## 4. Critical issues

None.

---

## 5. Carry-forward nudges (for the orchestrator; no new research needed except where marked)

The research's own "Changes to earlier notes (for the scribes)" after round 2 lists eight items; item 5 (D2 routing) is done. The seven below are the rest, consolidated, each naming the file, the section and the change.

1. **`playbooks/music-sound.md`, Step 15 "DX-gated check" and Template G check row; `skills/.../SKILL.md`, Procedure 13 and the master checklist.** Replace "Keep 6 LU as the starting threshold (inference; the broadcast anchor in research G3 is not applied here)" with: "Aim for a Loudness-to-Dialogue Ratio of 5 LU or less (EBU R 128 s4, November 2023, recommendation j; broadcast adaptation guidance, 'explicitly not intended as production advice for feature films'); more than 5 LU means look at the music; more than 6 LU is a fail before any master is signed off. Read LDR only when the music is audible: a very quiet bed can make the mix measure *below* the dialogue stem (research G3 sandbox table), and a reading near zero or negative does not mean 'perfect'." Cite [150][151] in the playbook's source list.

2. **`playbooks/music-sound.md`, Decision 4 "Facts that matter" and Pitfall 7; `skills/.../SKILL.md`, "Family audio stays on the maker's PC" guardrail and the Open gaps line.** Replace "Its primary terms could not be read (UNVERIFIED). One June 2026 explainer says paid plans grant commercial use, which conflicts with the other sources [14]" with: "Udio's Terms of Service (Last Revised 2025-11-12, read 2026-10-18 from the page data, research G6) bar downloading any Output, limit use to 'personal and non-commercial purposes', vest Output in Udio and its licensors, and take a 'worldwide, perpetual and irrevocable' licence over anything uploaded. Udio cannot supply a file for the film, and no family audio, photo or humming is ever uploaded to it, even as a style reference." Add Udio by name to the skill's cloud list and remove "Udio's … primary terms" from the skill's Open gaps (keep Lyria).

3. **`playbooks/music-sound.md`, Step 2 and Decision 1; `skills/.../SKILL.md`, "Not legal advice" guardrail and Open gaps.** Change "It did not read the UK PRS, German GEMA, French SACEM or Indian IPRS practice" to "GEMA's Tarif T (version 46, valid from 2026-01-01) was read in full: 1.3% of net ticket revenue, minimum EUR 30.40 per screening up to 150 people (EUR 32.53 with 7% VAT), 15% discount for events with a cultural or social purpose, consent to be acquired before the screening and conditional on the film's music being properly licensed, and a generative-AI clause that puts the burden of proof on the licensee. PRS, SACEM and IPRS remain unread (TODO(research))." Add the three G7 add-on questions to Decision 1 so the one-hour consult starts above the basics.

4. **`playbooks/music-sound.md`, Template C "Usage terms" bullet; `research/music-sound.md`, Deliverables 2 and 5.** Replace "check the template for exact wording" with the RapidCue `CueUsage` and `CueSubUsage` vocabulary (research G1, [154]: 29 and 10 values; the five mappings for this film, including Background Vocal / Humming for a hummed tune with no performer on screen) and add `PublicDomainIndicator`, `PublicDomainTerritory`, `SyncUseIndicator`, `MasterUseIndicator`, `Performer` and `Duration` as HHMMSS to the cue-sheet header. Keep [50] and [110] tagged for the deadline dates.

5. **`playbooks/music-sound.md`, Template J and Step 13.** Add the row "2026-12-21 to 12-27: re-conform dry run on the slice chapter. Lengthen one shot by two seconds, re-conform, time T1–T6 on the stopwatch protocol (research G8), log one row of `unlock_id,…,hours_per_finished_minute`." Add to Step 13: "The first real unlock after 2027-01-17 is timed the same way, and the measured figure replaces F7's inference and goes to `production-scale`'s stage-hours table." This is the only way the 0.6 h/min planning figure becomes a measurement before the February mix week.

6. **`playbooks/music-sound.md`, Step 14 "Tools" and Decision 7; research F9.** Add the Resolve 21 "Limit Resolve Memory Usage to" preference (default and maximum 75% of RAM, Resolve manual chapter 4), the `memlog.ps1` sampler and the fifteen-minute result sheet from research G5, with the acceptance rule (peak working set at or below half the installed RAM, clean playback, PC usable; else cap at 50% and retest once; else REAPER). The charter's memory constraint is why Resolve needs this gate before it is relied on for the mix.

7. **`playbooks/music-sound.md`, Pitfall 10 and Template G "Targets" Venue column.** Add one sentence from the EBU arithmetic (research G3): "A venue master at -18 LUFS integrated with LDR ≤ 5 LU implies dialogue at about -23 LUFS or louder; if the dialogue stem measures quieter than -23 on the speech spans, the -18 master is being reached with music, not voice, and the room will hear it." This turns two numbers the playbook already uses into a single test the maker can run on the spotting-sheet spans.

---

## 6. Research follow-ups (facts not in the notes; do not guess)

1. ASCAP cue-sheet deadline table (2027-01-01, 2027-04-02): still 403 from this container on four attempts across three reviews; maker's browser, only if an ASCAP or BMI writer is in the cut (research G1).
2. Musopen Terms of Use: Cloudflare browser challenge; maker's five-minute read by 2026-10-31 with the log build (research G2 has the paste-ready row).
3. Netflix dialogue-gated loudness section (the -27 LKFS figure): script-rendered page; maker's three-minute browser read, as a second anchor for "dialogue-gated" (research G3).
4. Resolve Free on the installed Windows build: effects present (Ducker, De-Hummer, Noise Reduction, De-Esser, Loudness meter), peak working set over five minutes of Fairlight playback, verdict (research G5 result sheet).
5. PRS, SACEM and IPRS film-screening practice, read only once the premiere country is chosen (Decision 1, 2026-10-31); GEMA's 15% cultural/social discount eligibility and payer, if Germany.
6. Dolby or BBC primary guidance on dialogue level relative to programme level, and any practitioner source for a hall PA; none was readable this round.
7. The measured human-time re-conform figures from the 2026-12-21 to 12-27 dry run and the first January unlock (research G8 protocol), written back into F7 and `production-scale`.
8. Whether `playbooks/surprise-ops.md` receives the D2 sentence by Saturday 2026-11-07 (orchestrator-owned; research G4 confirms it has not landed as of today). If it slips, the 2026-11-14 voice-collection gate must slip with it, or relatives are recorded for the private cut only.
9. Carried from round 1, untouched: Suno docket status after 2026-10-02; a real Voice Memos Lossless file through `ffprobe` (ALAC assumption); WhatsApp and iMessage handling of an attached .m4a.

---

## 7. Strengths (keep these)

- Three rounds, twenty-four nudges, every one landed in the file and section it named, with a changelog line that says what changed and why. The research now records each sync with the playbook, so the drift that cost round 2 cannot happen silently.
- The rights spine is the best-sourced work in the project: six of six verbatim this round, eleven of eleven across rounds 2 and 3, and every blocked host named with what was tried and what the maker can do in five minutes instead.
- The researcher reads primary text when the fetch tool cannot: Udio's server-rendered page data, RapidCue's BMI-copyrighted guide, GEMA's tariff PDF, EBU R 128 s4 and Tech 3343. That is how "UNVERIFIED" becomes "confirmed" without a web search budget.
- The two-tier found-voice rule is stated once, carried by two columns, gated by a procedure step, named in the sibling playbooks' vocabulary, and the clip that fails it goes to a ledger with a path.
- The DX-gated check is now a measurement of dialogue where dialogue exists, with a primary anchor waiting in the research, a measured sandbox curve (about 0.8 LU per dB of music near the limit), and the caveat that a quiet bed can read negative.
- The fader protocol, the story-free calibration reel and the back-row listener who is not told the content turn loudness into something the sole keeper does in the room without showing the film to anyone.
- The sole-keeper instruction is honoured as a design fact, not a disclaimer: the maker signs off D2, takes the consult, times the re-conform, and every option that adds a person is a dated yes/no with a name-free brief and a confidentiality clause.

---

## 8. Advisor insight

The EBU arithmetic in G3 gives the film a quiet rule it did not have: at -18 LUFS with LDR ≤ 5 LU, dialogue must sit at about -23 or louder, so the venue master is reached with voice, not music. Make that the film's ethic as well as its measurement. In a life film, the loudest thing in the room should be a person's voice, and the loudest voice should be hers. Set the venue fader on the neutral reel, then check one thing more at the Monday run: find the single HER-PUBLIC clip that passed the one-key-three-guards decision (if one exists), and confirm from the back row that it is the loudest speech in the film by about one LU, with the maker's narration and the relatives a shade under it. Nobody in the room will measure that. Everybody will feel it: the film keeps stepping back so that she can be heard, and the stranger in row seven learns, without being told, whose film it is. If no HER-PUBLIC clip survives the decision, the same rule says the film's loudest speech belongs to the relative who knew her longest, and her own voice waits for the private cut, at the same level, in a room of one.

---

## 9. Notes for the orchestrator

- Approve the track. The seven carry-forward nudges are a scribe pass on the playbook and skill from research G1–G8, not new research; do them in one commit with the standing rule from round 2 (a change to a research deliverable is applied to the playbook template of the same name, and the reverse).
- The D2 patch to `playbooks/surprise-ops.md` is yours and is due Saturday 2026-11-07. Research G4 suggests the four lines it needs. If it does not land, hold the 2026-11-14 gate to private-cut recording only.
- Put three things in front of the maker now, as yes/no with dates: the premiere country and venue (2026-10-31); composer yes or no (2026-11-30); and the found-voice inventory question (which recordings of her exist and where), which is the one gathering task that needs nobody else.
- The maker's browser reads (Musopen, Netflix loudness section, ASCAP only if needed, Resolve result sheet) total under thirty minutes and close four UNVERIFIED tags. Batch them into one evening.

## Changelog
- 2026-10-18: round-3 review by the Fable advisor. Six claims spot-checked by direct fetch, all confirmed verbatim (EBU R 128 s4, Udio ToS, GEMA Tarif T v46, Stability AI licence, REAPER purchase page, Freesound FAQ). All eight round-2 nudges confirmed applied where named; C1 closed; no critical issue; approved with seven carry-forward nudges for the orchestrator drawn from the researcher's own round-2 "Changes to earlier notes".
