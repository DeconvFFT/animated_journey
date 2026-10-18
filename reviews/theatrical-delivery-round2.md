# theatrical-delivery — round 2 of 3 (Fable advisor)

**Date:** Sunday 2026-10-18 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `research/theatrical-delivery.md` (952 lines), `playbooks/theatrical-delivery.md` (v2, 682 lines), `.claude/skills/theatrical-delivery-and-rights/SKILL.md` (166 lines), against `CHARTER.md`, my brief review `reviews/02-film-briefs-review.md` §1.5 and my round-1 review `reviews/theatrical-delivery-round1.md`.
**Maker's standing instruction (relayed verbatim):** "for now only me and i will only bne the one on this project"; who else is in on the secret and who approves the hard chapters "can wait until the plan is ready". Binding on this review: nothing below asks the maker to bring anyone in. The v2 playbook now treats that as a mode with a dated decision point, which is what round 1 asked for.

**Verdict: revise (light).** Scores: meaning 4, specificity 5, accuracy 4, feasibility 4, ethics 4, craft 4.

All eight round-1 nudges were applied, and the one critical issue from round 1 (the contributor-ring assumption) is closed. What keeps this from approval is one new cross-track error that a learner would act on: the run sheet labels **Friday 19 February 2027 as picture lock**, while `production-scale.md` (Step 14, G-LOCK), `music-sound.md`, `cinematic-quality.md` and my own schedule in review 02 fix picture lock at **Saturday 6 February 2027**. Everything else below is tidy-up.

---

## 1. Round-1 nudges: were they addressed?

| # | Nudge (round 1) | Where it landed | Status |
|---|---|---|---|
| 1 | "Only-me mode (current)" box: card 4a not read to anyone; Tier A before the premiere = own material, her appearances by proxy, original/CC0/licensed assets; relatives' voices to the private cut or after 4d; decision point Sun 3 Jan 2027 | Playbook Step 11 (boxed paragraph), T9 4a header, T4 new row TD-L2c, "Other decisions"; SKILL.md step 16 (indented paragraph), Rights gate checklist, "When not to use", Ethics guardrails | **Done.** The box also says what the public cut *can* contain and that any contributor confirm/sign step (TD-L6) waits for the same decision. Better than asked. |
| 2 | Replace "exact command is TODO(research); do not invent one" with the verified ffprobe command; mark `lut3d` and `-map_metadata -1` as run in the container, confirm once on the PC | Playbook Step 8 (command plus the container output), Step 4 (lut3d), Exercise 5; SKILL.md steps 3, 4, 9 | **Done.** The `encoder` tag note is present in both files. |
| 3 | TD-L2b, by Sun 17 Jan 2027: venue visit with the test clip only; record settings, caption sizes 20/23/26, PLUGE, tone; set Trim V and TD-3 from the visit | Playbook T4 (new row with a fail branch), Step 10 (bullet), Step 4 (Trim V "set on site at TD-L2b"), T1; SKILL.md step 4 | **Done.** |
| 4 | Branch: venue is a cinema with a DCP server → DCP primary, Exercise 3 to Sun 29 Nov 2026, January test slot, MP4 over HDMI becomes rung 1; content type feature/short places the film in the projectionist's interface | Playbook Step 9 ("Branch" paragraph and setting 3), Decisions TD-4 and TD-6 "What would change it", T3 backup-ladder header; SKILL.md step 11 | **Done.** Content-type wording verified against ch07 today (below). |
| 5 | UK IPO fee wording: £20 for one work, sliding scale, non-refundable, plus a separate licence fee, 7 years, UK only, page updated 1 Dec 2025 | Playbook Step 11 photos bullet and T8 sample row PH-0107; SKILL.md step 18 | **Done, with a TODO the scribe left open** ("confirm the £24 two-work step against [62]; the research table lists £40 for ten works and £60 for twenty"). I fetched the page today: both are right and complementary (£20/1, £24/2, £30/5, £40/10, £60/20, £80/30). The TODO can be closed (nudge 2 below). |
| 6 | ext2 (DCP-o-matic guarantee; ISDCF also allows ext3), 128-byte inode, MBR with one primary 0x83, re-partition retail sticks ("almost certainly incorrect"), MBR ≤ 2 TB; cite Flat 1998x1080 to [12][31] not [15] | Playbook Step 9.10, T2 Media row, T2 Picture row now [12][22][31]; SKILL.md step 13 and DCP checklist | **Done.** |
| 7 | Advisor-flag mechanism: `rights/flags/<asset_id>.md` (why, undo, exposed, draft date), request a Fable review, no RISK status or Tier C admission until a dated advisor line and 48 hours | SKILL.md step 16, Ethics guardrails, Rights gate checklist; playbook Step 11 "Accepted risk", T8 column guide (`advisor_flag`) | **Done.** |
| 8 | Restore the Sundance FAQ 31 Closed Caption and Open Caption note (document dated 2026-09-08, "subject to change"); settle the dBTP conflict in one line | Playbook T2 Cinema Captions row, Pitfall 19, Step 6; Step 5 "Settled" line and T1; SKILL.md step 5 | **Done.** |

Eight of eight addressed. The changelog v2 entry records them honestly.

---

## 2. Spot-checks (five claims fetched today, 2026-10-18)

| # | Claim in the artefacts | Source checked | Result |
|---|---|---|---|
| 1 | UK IPO orphan works: application fee £20 for one work, sliding scale (£24 for two, £30 for five, £80 for thirty), non-refundable, plus a separate licence fee if granted; licence up to 7 years; UK use only; page updated 1 Dec 2025; film and photographs are covered [62] (playbook Step 11, SKILL.md step 18) | https://www.gov.uk/guidance/copyright-orphan-works (WebFetch) | **Confirmed verbatim.** Table: 1 work £20, 2 works £24, 5 works £30, 10 works £40, 20 works £60, 30 works £80. "This is non-refundable." "At this stage you do not need to pay the licence fee." "can last up to 7 years"; "applies only for use in the UK"; last updated "1 December 2025". The playbook's open TODO about the £24 step is therefore closable; the research's £40/£60 figures are also correct (they are the 10- and 20-work steps). |
| 2 | DCP-o-matic ch07: content type "will affect where your content appears in the projector's server user interface"; "Use 2K unless you have content that is of high enough resolution to be worth presenting in 4K"; bandwidth 50 to 250 Mbit/s, commercial 75 to 125; SMPTE "if in doubt"; Container pads with black; FAT32 4 GB reel note [15] (playbook Step 9.3, SKILL.md step 11) | https://dcpomatic.com/manual/html/ch07.html (WebFetch) | **Confirmed.** Content type: "'feature', 'trailer' or whatever", and on some systems it "will affect where your content appears in the projector's server user interface". The page still gives no 1998x1080 figure, so the T2 citation move to [12][22][31] was right. |
| 3 | EBU R128: Programme Loudness target -23.0 LUFS; Maximum True Peak Level -1 dBTP [36] (playbook Step 5 "Settled" line, T1) | https://tech.ebu.ch/docs/r/r128.pdf (downloaded, pdftotext) | **Confirmed.** "h) ... normalised to a Target Level of −23.0 LUFS"; "m) ... the True Peak Level of a programme shall not exceed −1 dBTP (dB True Peak)". R128 also notes that "Maximum True Peak Levels may be lower for different distribution systems and data reduction rates", which is why the toolchain's -1.5 was a legitimate loudnorm example and not a target; the playbook's settlement sentence is accurate. |
| 4 | ISDCF Doc 3: MBR only (excludes GPT), one partition record, type 0x83, EXT3 or EXT2 with 128-byte inode, `mkfs -t ext3 -I 128 -m 0`, 2 TB MBR limit, retail USB sticks' partition tables "almost certainly ... incorrect", assume USB 2.0 type A [26] (playbook Step 9.10, T2 Media, SKILL.md step 13) | https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf (downloaded, pdftotext) | **Confirmed verbatim.** "This partition type can only be used on hard-drives no larger than 2TB. This is an intrinsic limit of MBR"; "NOTE 3: Storage device purchased at retail, particularly USB sticks, may have existing partition tables. If so, the partition table will almost certainly be incorrect for the purpose". |
| 5 | SIL OFL FAQ: output is unrestricted; "video titling" listed; embedding allowed in full or as a subset; notices kept when redistributing [75] (playbook Step 6, SKILL.md step 7) | https://openfontlicense.org/ofl-faq/ (WebFetch) | **Confirmed.** 1.1 lists "logos, posters, business cards, stationery, video titling, signage"; 1.12 "Yes, either in full or a subset"; 1.7 and 1.20 on notices. One nuance for a later DCP subtitle track: the OFL treats a subset delivered as a *webfont* as a modification (2.6), but a subset embedded in a document is not (1.12); a DCP subtitle MXF is the document case. No change needed. |

No fetched claim failed. Round 1 checked twelve others (DCP-o-matic version, ch12, ch17, ch20, ch06s04, EBU R95, Microsoft font FAQ, Sundance FAQ 8/12/18/31, 17 U.S.C. 101, Minecraft hash); none of those passages has been altered in v2 except as the nudges asked.

---

## 3. Scores and reasoning

**Meaning: 4** (was 3). The only-me box now says the thing the maker most needs to hear: before the premiere the public cut carries no recorded voice of a living person, and that is a narrative decision with a date (Sun 3 Jan 2027), not a legal footnote. Her release (4e) with the per-scene ledger remains the most dignified answer in the project to "she cannot approve it in advance". One point short because the playbook still treats the post-premiere release step purely as paperwork (see Advisor insight for how it can be part of the gift).

**Specificity: 5.** Unchanged: dialog names, commands with their container output, dates, line IDs, a CSV header, a question list.

**Accuracy: 4.** All five fetched claims hold verbatim, as did all twelve in round 1. Deductions: (a) TD-L7 says "Fri 19 Feb 2027 (picture lock)" in both the playbook and the research (lines 316 and 470), contradicting `production-scale.md` G-LOCK Sat 6 Feb 2027 and review 02; (b) a TODO(research) left open on the £24 step when the source settles it; (c) `TODO(research)` used in Step 6 for a *test* ("confirm this on the real screen with the test clip"), while the playbook's own header says TODO(research) items "must not be treated as facts", so the tag now means two different things.

**Feasibility: 4.** TD-L2b removes the premiere-week re-export risk; the DCP-server branch exists; the DCP stays optional and PC-side. The 19 Feb lock label is the one feasibility hazard: a maker who believes the picture can still move until 19 Feb has eaten the two finishing weeks (score, mix, grade, master, captions, exports on 20–21 Feb) that the theatrical bar needs.

**Ethics (incl. rights): 4.** Only-me mode, tiers A–D, the advisor-flag file, the 48-hour gap, the dead, minors, the estranged, no synthetic voice, truthful omission not falsehood, personal data in the private repo: all present and consistent across playbook and skill. Held at 4 rather than 5 because the T4 TD-L6 row still reads "contributors confirm their clip" without a marker that it is parked under only-me; an agent reading the table alone would try to act on it.

**Craft / usability: 4** (was 3). The skill's description triggers on the right nouns (masters, venue playback, captions, loudness, DCP, rights-log rows, releases, "showing the film publicly") and the 22-step procedure no longer stalls an agent: step 3 has a command, step 4 and 9 say what was run and where. The theatrical bar is held (one grade, two trims, judged on the real screen at TD-L2b, Verify DCP, hashes, mono-fold). Remaining friction: T4 is ordered by ID rather than date (TD-L2b on 17 Jan and TD-L2c on 3 Jan sit among December rows), which matters because the table is meant to merge into the surprise-ops key-dates list; SKILL.md step 22 still cites "the venue loudness ceiling" as its example of a playbook conflict after that conflict was settled; and the playbook lacks the "Deltas to existing playbooks" section review 02 asked every new note to carry (the research has one as Deliverable 6; the playbook, which the scribes patch from, does not).

---

## 4. Critical issues (must be fixed before approval)

1. **Picture lock is dated wrong in the run sheet.** `playbooks/theatrical-delivery.md` T4 row TD-L7 reads "Fri 19 Feb 2027 (picture lock)"; `research/theatrical-delivery.md` says the same at line 316 ("before the Fri 19 Feb picture lock") and line 470. The project's picture lock is **Saturday 6 February 2027 (G-LOCK)** in `playbooks/production-scale.md` Step 14 and its gate table, `playbooks/music-sound.md` (G-LOCK 2027-02-06), `playbooks/cinematic-quality.md` ("Picture lock is set for Saturday 6 February 2027 [P4]") and `reviews/02-film-briefs-review.md` §0.1. The 19 Feb date was inherited from `playbooks/surprise-ops.md` key dates ("Fri 19 Feb 2027 | Withdrawals close; picture lock"), which predates the production-scale decision. 19 February is correctly the *withdrawals-close* date (it is also the date in consent card 4a), so TD-L7's *action* (freeze the rights log, cue sheets and credits) can stay on 19 Feb; only the label is wrong. Fix: relabel TD-L7 "Fri 19 Feb 2027 (withdrawals close, per surprise-ops; picture lock itself is Sat 6 Feb 2027, production-scale G-LOCK; after 6 Feb only sound, grade, titles, captions and trims may change)", make the same change at research lines 316 and 470, and add a delta telling the surprise-ops scribe to split its 19 Feb row.

---

## 5. Nudges (6, each file + section + exact change)

1. **`playbooks/theatrical-delivery.md`, T4 row TD-L7; `research/theatrical-delivery.md`, lines 316 and 470 (Finding 7 "Premiere-week routine" and Deliverable 3 run sheet)** — change "Fri 19 Feb 2027 (picture lock)" to "Fri 19 Feb 2027 (withdrawals close, surprise-ops; picture lock is Sat 6 Feb 2027, production-scale G-LOCK)". In the research line 316 write "(after the Sat 6 Feb picture lock, before the Fri 19 Feb withdrawals close)". Add to the new Deltas section (nudge 6): "`playbooks/surprise-ops.md` key dates: split the row 'Fri 19 Feb 2027 | Withdrawals close; picture lock' into 'Sat 6 Feb 2027 | Picture lock (G-LOCK, production-scale)' and 'Fri 19 Feb 2027 | Withdrawals close'."

2. **`playbooks/theatrical-delivery.md`, Step 11 photos bullet and T8 sample row PH-0107; `skills/theatrical-delivery-and-rights/SKILL.md`, Procedure step 18; `research/theatrical-delivery.md`, lines 509 and 549 and the Finding 6.2 orphan-works bullet** — delete the sentence "TODO(research): confirm the £24 two-work step against [62]; the research table lists £40 for ten works and £60 for twenty" and write the full scale once: "UK IPO application fee £20 for one work, £24 for two, £30 for five, £40 for ten, £60 for twenty, £80 for thirty; non-refundable; a separate licence fee is payable only if the licence is granted; licence up to 7 years; UK use only; film and photographs are covered; page updated 1 Dec 2025, read 2026-10-18 [62]". In the research, replace the two remaining "from £20 per work" / "from £20 for one work" phrasings with "£20 application fee for one work (sliding scale) plus a licence fee".

3. **`playbooks/theatrical-delivery.md`, Step 6 "Venue file" bullet and "Still unknown" last bullet** — replace "**TODO(research):** confirm this on the real screen with the test clip" with "Confirmed at TD-L2b (by Sun 17 Jan 2027) from caption sizes 20, 23 and 26 on the venue screen; until then 23 is the working value." Move "Trim values, the cinema caption size (5.5 to 6%) and the venue caption size need a real-screen test" out of "Still unknown (TODO(research) items to close)" into a two-line "Scheduled tests" list (TD-L2b for the venue; the first real-cinema slot for Trim C and the cinema caption size), so TODO(research) keeps the single meaning the header gives it: a fact not yet sourced.

4. **`playbooks/theatrical-delivery.md`, T4 run-sheet table** — order the rows by date, not ID (TD-L1 1 Nov; TD-L2 6 Nov; TD-L5 4 Dec; TD-L3 and TD-L4 20 Dec; TD-L2c 3 Jan; TD-L2b 17 Jan; TD-L6 15 Feb; TD-L7 19 Feb; TD-L8 20–21 Feb; TD-L9 to TD-L16), keeping the IDs, so the table merges into surprise-ops' key dates in sequence. In the TD-L6 row change "contributors confirm their clip" to "contributors confirm their clip (parked under only-me mode; applies only if TD-L2c brought someone in)".

5. **`skills/theatrical-delivery-and-rights/SKILL.md`, Procedure step 22** — replace "(for example the venue loudness ceiling)" with "(for example a date that disagrees with another playbook, such as picture lock, which is Sat 6 Feb 2027 per production-scale G-LOCK)". The loudness conflict is settled in step 5, so the example now points an agent at a non-conflict.

6. **`playbooks/theatrical-delivery.md`, new section "Deltas to existing playbooks" placed before "Pitfalls"** — copy the research's Deliverable 6 into the playbook in the file-and-decision-number form review 02 asked for, including at minimum: `surprise-ops.md` consent card → T9 4a version 2 and the only-me box; `surprise-ops.md` key dates 19 Feb row (nudge 1) and the new TD-L2b, TD-L2c lines; `toolchain.md` Step 10 `TP=-1.5` → "-1 dBTP target; -1.5 was an example"; `agent-pipeline.md` settings card → "stills prepared at 3840 px or more on the long edge; 2K Flat DCP derived, never re-authored"; `format.md` Decision 12 and hosting table → T3 gate (releases signed, explicit yes) before any online link; `ai-imagery.md` cue sheet → the six extensions in Finding 10 (pre-roll line, tool name/version/date, human-contribution note, deepfake marker, no-synthetic-voice line, metadata-stripping note). The scribes patch from the playbook, not the research.

---

## 6. Research follow-ups (facts not in the notes; do not guess)

- Which gamma each DCP-o-matic colour preset applies (Rec. 709 vs Rec. 1886), from the source tree or a test frame; whether a ProRes 422 HQ `.mov` imports cleanly; DCP-o-matic 2.18.51 memory use and encode speed on the maker's Windows PC (Exercise 3 measures it; a forum or release-note figure would set expectations earlier).
- What the ISDCF name shows when only L and R are mapped in a 6-channel container ("20" vs "51"), from DCP-o-matic's naming code or a test build.
- Windows 11 Settings path for a 24 Hz refresh rate on an external display, and which rates the maker's laptop GPU offers over HDMI.
- Venue-licence coverage statements from PRS/PPL (UK), ASCAP/BMI (US) and IPRS (India) on music inside a film shown at a hired hall (pages returned 403 last round).
- Public-liability and E&O expectations for a one-off four-wall hire in the maker's country (TD-7 first); a 2026 E&O premium range for a short from at least one broker page.
- Whether the EU AI Omnibus (in force 27 Jul 2026) changed the Article 50 transparency timeline, and whether a private individual showing a film at a public gathering is a "deployer".
- Current text of India Copyright Act s.17(b) from an official, dated source; UK and India post-mortem image and privacy rules.
- Family-film clearance practice: one or two documented accounts of how personal-documentary makers handle relatives' old photographs and voices, to test the Tier B synthesis.
- For the orchestrator rather than a researcher: a repo-wide check of which playbooks still carry "Fri 19 Feb 2027 picture lock" from the early surprise-ops key-dates table (`story.md`, `format.md`, `surprise-ops.md` at least), so the G-LOCK date is patched everywhere at once.

---

## 7. Strengths (keep these)

- Every round-1 nudge landed where it was asked, in both the playbook and the skill, and the changelog says so plainly.
- The only-me box is better than the nudge: it states what the public cut can and cannot contain, names the decision point, and reaches into the run sheet (TD-L2c) and the skill's "When not to use".
- Commands now carry the date, the ffmpeg version, the container output and the "confirm once on the PC" line; an agent can run step 3 without inventing anything.
- The DCP-server branch is a one-paragraph decision with dates, not a vague "if the venue is a cinema".
- The dBTP settlement is one sentence in Step 5, repeated in T1, so the settings card asks the maker only real questions.
- Spot-checks continue to hold verbatim (17 claims across two rounds); the UNVERIFIED and (inference) tagging is still honest and the researcher's search-outage note is still in the header.
- The rights log's `advisor_flag` column, the flag file path and the 48-hour rule now form a loop an agent can run and a human can audit.

---

## 8. Advisor insight

The only-me rule has quietly designed two films, and the playbook should say so out loud because it turns the rights constraint into a device that means something (Principle 2). Before the premiere, the public cut cannot carry a living relative's recorded voice; so the public cut is, by necessity, the film *as strangers meet her*: the maker's narration, her own found voice as recorded, photographs, text. After the premiere, the post-premiere release step (T9 4d) is currently paperwork. Make it the second act of the gift instead: each relative who has now seen the film and signs 4d records their one memory *in response to the film they just watched*, and "her version" on Saturday 24 April 2027 is the same picture with the voices turned on, a chorus added to a film that was first shown in silence. Technically it is cheap (the picture is locked; only the dialogue stem and the mix change, and the surprise-ops schedule already holds the 24 April delivery). Ethically it is cleaner than anything gathered under a pretext: every voice in her version was recorded by someone who knew exactly what the film was and had seen it. And it gives the premiere its shape in reverse: the public room gets the film about her; she later gets the film in which the people who love her answer it. The playbook needs one line in Step 12 and one row in the consent ledger to carry this; the music-sound and film-story tracks should know the dialogue stem has a second life.

---

## Changelog
- 2026-10-18: round 2 by the Fable advisor. All eight round-1 nudges confirmed applied; five further claims fetched and confirmed (gov.uk orphan works fee table, DCP-o-matic ch07 content type, EBU R128 -1 dBTP, ISDCF Doc 3 2 TB and retail-partition note, OFL FAQ video titling and embedding). Verdict revise (light): one critical issue (picture lock mislabelled 19 Feb vs G-LOCK 6 Feb); six nudges.
