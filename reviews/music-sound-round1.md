# music-sound — round 1 of 3 review: her voice in a public room, and a schedule that does not match the lock

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `research/music-sound.md` (Sonnet, 692 lines), `playbooks/music-sound.md` (Haiku, v0.1 draft), `skills/life-film-music-and-sound/SKILL.md`, against `CHARTER.md`, my brief in `reviews/02-film-briefs-review.md` §1.4, and the sibling playbooks the track must align with (`surprise-ops.md` Decision 18 and run sheet, `film-story.md` Decision 3 and Step 6, `production-scale.md` Steps 14–15 and gates G-LOCK and G-MIX, `format.md` Step 14, `story.md` Step 2 and Decision 10).
**Maker's standing instruction (verbatim, relayed by the harness):** "for now only me and i will only be the one on this project." Every outreach option below is therefore a trade-off against the secret, never a default. The three documents already honour that; good.

**Verdict: revise.** Two critical issues (one ethics, one feasibility), both fixable in a round without new research. The rights work is the strongest I have seen in this project and should not be rewritten; the fixes are alignment, not substance.

---

## 1. Spot-checks (fetched today; WebSearch budget was exhausted for this run, so direct fetches only)

| # | Claim in the notes | Source | Result |
|---|---|---|---|
| 1 | Suno ToS revised 2026-08-10, effective 2026-09-03; free tier "lawful, personal and non-commercial"; Pro/Premier get "assigns to you all of its right, title and interest in and to any Output owned by Suno"; "no representation or warranty... that any copyright will vest"; commercial use only for a "permitted download"; no public-performance clause; voice model of your own voice only; do not remove watermarks | https://suno.com/terms [11] | **Confirmed**, all six points, wording matches. One addition the notes missed: "Nothing in this paragraph permits commercial use of any Remix." Add to Q3. |
| 2 | ElevenLabs Music Terms updated 2026-10-09; "All online and offline commercial use permitted, except film, TV, radio, and Studio Games" on every plan except Enterprise; Free needs attribution | https://elevenlabs.io/music-terms [19] | **Confirmed**, with one nuance: there is an "Enterprise Music Lite" tier that *also* carries the film/TV/radio exclusion. Only "Enterprise Music" is clean. The notes' "Enterprise Music has no listed exclusions" is right; the skill's "except on Enterprise" is loose. |
| 3 | REAPER 7.82 (2026-10-04); 60-day full-function evaluation; $60 discounted at gross yearly revenue ≤ $20,000; $225 commercial | https://www.reaper.fm/purchase.php [103] | **Confirmed** verbatim. |
| 4 | 17 U.S.C. 110(4) exempts only "nondramatic literary or musical work", not a motion picture | https://www.law.cornell.edu/uscode/text/17/110 [54] | **Confirmed.** The legislative notes under 110(3) add "The scope of the clause does not cover the sequential showing of motion pictures", which strengthens the point. |
| 5 | US public domain 2026: compositions published 1930 ("I Got Rhythm", "Georgia on My Mind", "Body and Soul"); 1925 recordings (Bessie Smith "St. Louis Blues" with Armstrong); later recordings remain copyrighted | https://cspd.law.duke.edu/publicdomainday/2026/ [46] | **Confirmed**, including "the later recordings by Ray Charles and by Tiny Tim are still copyrighted." |
| 6 | Stability AI Community Licence: free under $1M annual revenue; "you own outputs"; Stable Audio 3.0 listed | https://stability.ai/license [21] | **Confirmed.** Stable Audio 3.0 is named under Community. |
| 7 | FFmpeg 9.0.2 released 2026-09-18; 8.1.3 on 2026-09-21; Windows builds from gyan.dev and BtbN | https://ffmpeg.org/download.html [87] | **Confirmed.** |
| 8 | Audacity 4.0.1 on the download page, no release date, Windows x86_64 and ARM64 | https://www.audacityteam.org/download/ [104] | **Confirmed.** |
| 9 | OneMusic Australia Film Screenings licence applies "regardless of whether there's an entry fee"; minimum fee $86.52 for APRA works | OneMusic PDF [51], read with pdftotext from the fetched file | **Confirmed**: "Event organisers require permission to screen the film and to publicly play the music within the film"; "0.462% of Gross Box Office Receipts subject to a minimum fee of $86.52 (For Film Screenings with no Entry Fee, a minimum fee of $86.52 applies)". |
| 10 | ASCAP does not license sync; cue-sheet contents and the 2027-01-01 deadline | https://www.ascap.com/help/ascap-licensing [49], .../cue-sheets [50] | **Not re-verified**: both pages returned HTTP 403 to me today. The sync statement matches ASCAP's long-standing public position; the specific 2027-01-01 deadline is the one dated figure I could not see. Keep it, but tag it "read by researcher 2026-10-18; not re-read". |

Nine of ten load-bearing claims hold with the cited wording. Accuracy is high and the UNVERIFIED tagging is honest throughout. This is the standard the other tracks should copy.

---

## 2. Scores

| Dimension | Score | Why |
|---|---|---|
| Meaning | 4 | The five rules (one motif many weathers; sincere version shorter and later; era songs only when the world plays them; silence takes the hardest beat; real voices lead) are the right rules and are argued from the exemplars rather than asserted. What is missing is the Principle 2 test applied to sound: the cue map has no column for *where in her life this sound comes from*. A MOTIF with no origin in her life is decoration. |
| Specificity | 5 | Tested ffmpeg commands, a 36-column licence log, a spotting sheet with a worked row, a cue sheet with ASCAP fields, phone settings, a cleanup chain with the "listen to what you removed" check, three loudness columns, a T-minus schedule. Nothing vague survives. |
| Accuracy | 4 | 9 of 10 spot-checks confirmed verbatim; everything unread is tagged. Small fixes: ElevenLabs "Enterprise Music Lite" also excludes film; Suno excludes commercial use of Remixes; Table 1A row 5 gives "Y" for a public gathering while naming Musopen, whose terms are UNVERIFIED (should be Y for pre-1926 US recordings and "?" for Musopen). |
| Feasibility | 3 | The sound schedule assumes picture lock on 2027-01-15 and a mix on 02-06 to 02-12. `production-scale.md` sets G-LOCK on **Saturday 2027-02-06** and G-MIX (mix v1) on **Saturday 2027-02-13**, with finishing 7–20 Feb holding "about 34 usable hours at 20 hours a week". `surprise-ops.md` puts the full run on the real playback chain on **Monday 22 Feb**, not in week 18. Under the real lock date, Step 12 ("January, after picture lock"), Step 13 (temp replaced 01-16 to 02-05, before lock) and the 3–5-week composer turnaround all collapse. The plan is doable only with rolling chapter locks, which production-scale offers as a lever and this playbook never mentions. |
| Ethics | 3 | The rights work is excellent. The problem is her own found voice. The playbook calls it "the most important sound in the film" and schedules its cleanup for the premiere; the research names the unresolved question ("May I play a private recording of her voice... to a public audience that includes her, at an event she does not know about?") and then proceeds as if the answer were yes. `surprise-ops.md` Decision 18 puts "her own greeting or message" in the T9 ledger "for her post-reveal decision" and says it "never opens a hard chapter"; `film-story.md` Decision 3 allows it "only if it passes the 72-hour double decision" and keeps "voicemails to a third party" out. Three playbooks, three answers. The default must be the stricter one. |
| Craft / usability | 4 | The mix spec holds the theatrical bar (calibrated cinema level kept apart from LUFS, stems, fold-down, the 6-dB-lower intelligibility test, a story-free calibration reel). The skill's description triggers on the right nouns and its procedure is followable by an agent. Two usability faults: the skill hardcodes dated facts (Udio downloads off, Suno tiers) that will be stale by January, and it has no procedural step for flagging a cue over a hard chapter to this advisor, although the guardrail mentions it. |

Approve requires 4+ everywhere and no critical issue; feasibility and ethics are at 3 with two critical issues open. **Revise.**

---

## 3. Critical issues

**C1 — Her found voice is default-in for the public cut; it must be default-out.** The public room changes the question from "would she share this with family" to "would she play this to strangers" (review 02 §0.2). A voicemail or answering-machine message is addressed to one person; playing it to a public room is a different act from showing a family video in which she speaks knowing a camera is on. The research's own legal note (Q8) says the answer "should be written into the plan before the voice is used"; the plan then uses it. Required change: (a) her found voice in the *public* cut is a hard-chapter-grade decision under review 02 §0.3 (one key plus three guards: decision sheet, advisor flag, 72-hour double yes, default OUT on doubt); (b) recordings addressed to a third party (voicemails, messages, phone calls) are OUT of the public cut and go to the T9 ledger for her post-reveal decision, as surprise-ops already says; (c) the eligible class for the public cut is speech she gave knowing she was recorded (home video at a family event, a toast, singing at a birthday), used as recorded; (d) the found-voice log gains `addressed_to` and `public_cut_eligible` columns. Align the wording in `surprise-ops` Decision 18, `film-story` Decision 3 and this playbook so there is one rule, stated once.

**C2 — The sound schedule is built on the wrong lock date and the wrong rehearsal date.** Rebuild Template J backward from the authoritative gates: G-LOCK Sat 2027-02-06, G-MIX Sat 2027-02-13, finishing 7–20 Feb, full run on the real chain Mon 22 Feb, cold starts Thu 25 and Fri 26 Feb. Consequences the playbook must state: the mix window is one week, not two; the three masters and the venue test move to 13–22 Feb; found-voice cleanup and sound design must run on *rolling chapter locks* from January (production-scale's lever), not after a single lock; a commissioned composer working from lock is not feasible on this calendar and would need a near-lock animatic by mid-January, which makes Decision 2 moot unless the maker changes course now. Say this plainly so the maker does not discover it in February.

---

## 4. Nudges (at most 8; each names the file, the section and the change)

1. **`playbooks/music-sound.md`, Core principle 1 and Step 12; `skills/.../SKILL.md`, Procedure 8 and the "Before any found voice is used" checklist.** Replace "Her voice leads" with a two-tier rule: her voice *as recorded in front of a camera she knew was on* may lead in the public cut after the one-key-three-guards decision; anything addressed to a third party is private-cut-only and sits in the T9 ledger. Add `addressed_to` and `public_cut_eligible` to Template D3 and to the skill's checklist. Cross-reference `surprise-ops.md` Decision 18 and `film-story.md` Decision 3 by name, and state that this playbook adopts their stricter reading. (C1)

2. **`playbooks/music-sound.md`, Template J and Steps 10–16; `research/music-sound.md`, Deliverable 2 workflow table and the T-minus schedule.** Rebuild from G-LOCK 2027-02-06 and G-MIX 2027-02-13 (`production-scale.md` Steps 14–15), with the venue test on Mon 2027-02-22 (`surprise-ops.md` run sheet) and the format.md week-18 dates dropped. Add a "rolling chapter lock" line: sound work on a chapter begins the day that chapter is marked `locked=1` in `status.csv`, so DX cleanup, AMB and FX for the vertical slice start in December. State that a composer-from-lock is out on this calendar. Fix Decision 7 at the same time: with a mix on 13–20 Feb, a REAPER trial started 2026-12-28 ends 2027-02-26 and covers it; the "January mix" wording goes. (C2)

3. **`playbooks/music-sound.md`, Step 5 and Template B; `skills/.../SKILL.md`, Procedure 4.** Add a `source_in_her_life` column to `cue_map.csv` and the spotting sheet (the evidence row in the beat sheet, or the relative who named the sound), and a rule: no MOTIF or CLOCK without one. Add an "object sounds" line to the low-key asks ("what did the house sound like in the mornings?"), feeding the FX and AMB palette in Q7 with her objects instead of the generic 1970s list. This is the Principle 2 test applied to sound.

4. **`playbooks/music-sound.md`, Template D2 and Decision 6; `skills/.../SKILL.md`, guardrails "Secrecy" and "Consent".** Stop carrying the extended consent card as a TODO in two places; decide it. The existing surprise-ops card already tells a contributor that a film exists, so what D2 adds is only the *public* fact. Rewrite D2 to the minimum truthful addition ("the film may also be shown to people outside the family at a gathering in late February; tell me if your voice may be heard there") and remove tier C from the spoken card, because the maker cannot promise festival or cinema use before her own post-premiere release (review 02 §0.3). Tier C becomes a written post-premiere ask. Route the wording through the `surprise-ops` T7 truthful-pretext cards at that track's next round rather than inventing a parallel card here.

5. **`skills/.../SKILL.md`, Procedure 7 and "Ethics" guardrails.** Remove the hardcoded dated facts (Udio downloads off since 2025-10-29, Suno free tier, ElevenLabs tiers) from the procedure and replace with: "Read the AI rows of the licence log and the Q3 table in the research notes, check `last_reread_date`, and re-read any term older than 30 days before use." Keep the two durable rules (never her songs, never a real voice). Correct "except on Enterprise" to "except the Enterprise Music tier; Enterprise Music Lite also excludes film".

6. **`skills/.../SKILL.md`, Procedure (new step between 4 and 5).** Add: "For any beat flagged hard-chapter in the beat sheet, set the cue type to PULL-OUT by default, and write a flag line for the Fable advisor naming the beat, the proposed sound and why it is not silence. No MOTIF or BED over a hard chapter without that flag." The guardrail says the advisor flags; the procedure must make the flag happen.

7. **`research/music-sound.md`, Q3 table and Deliverable 1 Table 1A rows 5, 14, 16.** Row 5: split into "pre-1926 US recordings (Y/Y/y/y/Y)" and "Musopen recordings (?/?/?/?/?) until its terms are read". Row 14 (Suno Pro): add "Remixes excluded from commercial use" from the ToS. Row 16: note the Enterprise Music Lite exclusion. Tag [49] and [50] "not re-read by the advisor on 2026-10-18 (HTTP 403)".

8. **`playbooks/music-sound.md`, Step 15 and Template G.** The -18 LUFS venue start with -23 and -16 alternates is sound. Add the operational line that matters more than the number: the maker, not the venue engineer, holds the master fader during the film, with the level set at the Mon 22 Feb run from the back row on the neutral-voice reel; write the fader position on the run sheet. Add a dialogue-gated check (measure the DX stem alone; if integrated DX sits more than 6 LU under the full mix, the music is too loud for a room of 50+-year-olds).

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. ASCAP cue-sheet pages returned 403 today: confirm the 2027 submission deadlines and usage categories from a readable copy, or from BMI's equivalent.
2. Status of UMG and Sony v. Suno after fact discovery closed 2026-09-30: any summary-judgment ruling or settlement, read on the date.
3. Udio's primary terms as they stand (downloads, commercial use), since the notes rely on secondary reports and one conflicting explainer.
4. Musopen's current Terms of Use (the "personal, non-commercial" wording a guide mentions): read, quote, date.
5. For the premiere country once decided: the collecting society's film-screening practice (PRS, GEMA, SACEM, IPRS) and whether a venue's licence covers music in a guest's film.
6. Jurisdiction-flagged question for a one-hour consult: playing a private recording of a living person's voice, made by a family member, to a public audience without prior consent (personality rights, data protection where a voice is personal data, the household exemption).
7. Rolling chapter lock for sound: how documentary and animation shorts stage sound per reel before full lock, and what it costs in re-conform time.
8. Voice Memos "Lossless" codec on current iOS (assumed ALAC): confirm with `ffprobe` on a real file; and whether WhatsApp, Signal and iMessage re-encode an attached .m4a versus a voice note.
9. Whether Resolve Free's Fairlight page includes the ducker, de-hummer and loudness meters, so the maker's free NLE can host the mix without REAPER.

---

## 6. Strengths (keep these)

- The rights spine is the best-sourced work in the project: primary terms read and quoted, dated, with a Y/y/C/?/N legend that a reviewer can audit from the row alone. Nine of ten spot-checks confirmed verbatim.
- Three loudness practices kept apart, with the cinema column correctly defined as a calibrated playback level and not a LUFS target; the two-pass linear `loudnorm` rule with the "Normalization Type: Linear" check; the story-free calibration reel for the venue engineer.
- The substitute ladder (Q6) is honest and ranked by risk, with the no-music option at the top where it belongs for this film.
- The found-voice *technical* rule is exactly right: restore, never extend; `--denoise_only` only; listen to what you removed; cut only between full utterances; room tone under cuts.
- The cloud-enhancer table (Auphonic, Descript, Adobe) answers the charter's upload rule with quoted terms rather than suspicion.
- The secrecy trade-off is marked on every option, in the maker's own frame, without pretending a second person exists.
- The skill's description triggers on the right nouns (cue, song, AI music, temp, voice recording, mix, rights question, the premiere date) and the quality bar's "mediocre" column is concrete enough to fail a mix against.

---

## 7. Advisor insight

The motif should be a tune she gave you, not one you choose for her. Almost every mother has sung something to a child: a lullaby, a nonsense rhyme, a hymn, a folk song in the first language. The maker knows that tune from the inside and can hum it today, alone, on a phone, into the `originals` folder, with no release, no outsider and no secret at risk. That recording is the one voice in the project that is fully consented and fully the maker's own. If the tune is traditional or public domain, it needs no sync; if it is a copyrighted song, the title on a card and a relative's low-key confirmation ("did she sing that to all of us?") still make it the right *clock* even if the melody must be replaced. Build the film's theme from it: the first time the stranger in row seven hears it, it is a hummed fragment under her childhood; the last time, at the END cue, it is the maker's own voice, plainly recorded, and then nothing. The gift is reversed on the night: the song that went from her to the child comes back from the child to her, in front of people who now know why it matters. Add one line to the maker's week-1 tasks: "Record yourself humming the song she sang to you. Do not clean it."

---

## 8. Notes for the orchestrator

- C1 touches three playbooks. Patch `surprise-ops` Decision 18 and `film-story` Decision 3 with the same wording as nudge 1, so the found-voice rule is stated once and referenced twice.
- C2 is a symptom of the schedule authority question production-scale raised ("adopt Sunday-start weeks with the dates as the authority"). Settle the master calendar (G-LOCK 6 Feb, G-MIX 13 Feb, run 22 Feb, cold starts 25–26 Feb) in `CHARTER.md` or one dated file so no track invents its own week numbering again.
- The composer option is effectively closed by the calendar unless the maker decides this month. Put that in front of the maker now as a yes/no with the date, not as a lean.

## Changelog
- 2026-10-18: round-1 review by the Fable advisor. Ten claims spot-checked by direct fetch (nine confirmed; two ASCAP pages 403). WebSearch budget was exhausted for this run.
