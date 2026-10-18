# 98 - Integration critic (Sonnet, mechanical check), 2026-10-18

**Scope.** Part 1 greps `playbooks/`, `skills/` (including `recipes/`), `ROADMAP.md` and `PLAN-ON-A-PAGE.md` for every stale value in `DECISIONS.md` Table 4 (S-01 to S-37) and for the six named strings. Part 2 checks each of the 12 gaps in `reviews/99-completeness-critic.md` against `ROADMAP.md` v2. Part 3 lists integration problems found on the way. I read `DECISIONS.md` Table 4, the whole of `ROADMAP.md` and `PLAN-ON-A-PAGE.md`, and the completeness critic. I did not re-read the playbooks line by line; every claim cites a grep or a line I opened. No web page was opened; no code was written. Weekday-date pairs were checked with a script across `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, the playbooks and the skills: 0 mismatches.

---

## Part 1. Residual stale values

### 1.1 Result in one paragraph

Of the 37 Table 4 rows, 34 have no live stale text left in the files they name: S-02 to S-07, S-09 and S-11 to S-37 (every remaining hit for those rows is a reconciliation note, a changelog line, an "Options" list followed by a "Decided" line, or an explicit "superseded" sentence). Three rows still carry live stale text: **S-01** (the recipe code files), **S-08** and **S-10** (the `life-story-interviewing` side files). S-16 is clean in the files Table 4 names but has one unlisted straggler in `beat-sheet.md` (1.2). `PLAN-ON-A-PAGE.md` has no stale value. `ROADMAP.md` has no stale value in its plan text, but its section 14 item 1 is itself out of date (see 1.4). Line numbers in Table 4 have drifted because the playbooks were patched; the rows need a status column.

### 1.2 Live residuals (file:line: text)

**S-01, 25 fps in recipe code.** The playbooks and the skill describe these as "tested at 25, UNVERIFIED at 24, patch by hand after re-run" (`playbooks/toolchain.md` 8, 84, 90, 126, 221; `skills/free-creative-toolchain/SKILL.md` 12, 60, 173), but the files carry no warning of their own, so an agent that runs one unchanged writes 25 fps.
- `skills/free-creative-toolchain/recipes/r1_kenburns.sh:9`: `# Outputs: ... out.mp4 (1920x1080, 25 fps, H.264).`
- `skills/free-creative-toolchain/recipes/r1_kenburns.sh:18`: `# b) push-in 5 s @ 25 fps (crop to the output aspect FIRST; upscale; then zoompan)`
- `skills/free-creative-toolchain/recipes/r1_kenburns.sh:19`: `...zoompan=z='min(1+0.0008*on,1.2)':...:d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 ... kbA.mp4`
- `skills/free-creative-toolchain/recipes/r1_kenburns.sh:22`: `...zoompan=z=1.15:x='(iw-iw/zoom)*on/124':...:d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 ... panB.mp4`
- `skills/free-creative-toolchain/recipes/r2_parallax.py:25`: `sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 640, 360, 25`
- `skills/free-creative-toolchain/recipes/r2_parallax.py:49`: `# Then (bash, tested): ffmpeg -framerate 25 -i renders/p_%04d.png -c:v libx264 ...`
- `skills/free-creative-toolchain/recipes/r2_param.py:30`: `sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = RX, RY, 25` (not listed in Table 4)
- `skills/free-creative-toolchain/recipes/r5_story.mlt:5`: `Result: 200 frames, 1920x1080, 25 fps, H.264.`
- `skills/free-creative-toolchain/recipes/r5_story.mlt:7`: `Render (tested form): melt story.mlt -silent -profile atsc_1080p_25 ...`
- `skills/free-creative-toolchain/recipes/r5_story.mlt:10`: `<mlt LC_NUMERIC="C" version="7.0.0" profile="atsc_1080p_25">`
- `skills/free-creative-toolchain/recipes/r8_vse_xfade.py:18`: `sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 1920, 1080, 25   # TODO(verify): scribe addition` (not listed in Table 4)
- `skills/free-creative-toolchain/recipes/r8_vse_xfade.py:24-25`: a 25-frame overlap and `length=25` CROSS dissolve (a duration in frames, about 1.04 s at 24 fps; check at the re-run, not a rate)

**S-08, "closest insider" (acknowledged unpatched at `skills/life-story-interviewing/SKILL.md:145`).**
- `skills/life-story-interviewing/surprise-runbook.md:9`: `| 0 Suitability | ... Ask the closest insider: would they love it or hate it? ...`
- `skills/life-story-interviewing/surprise-runbook.md:12`: `... Any relative with a difficult history with the subject: ask an insider before approaching ...` (not in Table 4)
- `skills/life-story-interviewing/surprise-runbook.md:14`: `| 5 Reveal | Show it first privately to the closest insider. ... Give a veto window: nothing is shared beyond the room until they say so ...` (also S-10)
- `skills/life-story-interviewing/beat-sheet.md:24`: `4. *Check with a person who loves them* (the subject if collaborative; the closest insider if not) ...`

**S-10, briefing, consent and Tier 2 wording.**
- `skills/life-story-interviewing/question-bank.md:9`: `... in surprise mode the relative is briefed about the secret first).`
- `skills/life-story-interviewing/surprise-runbook.md:17`: Tier 2 script says `a gathering on Feb 27 that is partly public, and may be shared with family afterwards by private link` ("partly public" against the register's "mostly public"; the script is a TD-L2c placeholder, but it should say so in the file)
- `skills/life-story-interviewing/surprise-runbook.md:54`: `Door A sessions are Tier 2. They use the relative script above ... with a spoken consent that names what the audio may be used for, including the Feb 27 use.`
- `skills/life-story-interviewing/session-protocol.md:9`: `2. Pre-talk (Tier 2 only ...) ... "It will be shown at a gathering on Feb 27 that is partly public ..."` (not in Table 4)
- `skills/life-story-interviewing/session-protocol.md:10`: `3. Consent: spoken consent on the recording plus a short written release ...` (generic oral-history step, not in Table 4; conflicts with W-49 if read before the premiere)

**S-16 family, 25-minute budget.**
- `skills/life-story-interviewing/beat-sheet.md:9`: `**Starting time budget for a ~25 minute piece (our heuristic ...)` (flagged superseded at `SKILL.md:146`; the file itself is not marked)

### 1.3 A scribe to-do list that Table 4 and the W-29 grep would miss

- `playbooks/theatrical-delivery.md:522-553`, "Deltas to existing playbooks". Line 524: `These are the changes the other playbooks need ... so that a scribe can patch them from this guide`. 26 rows, none marked applied. Four rows quote superseded values: 529 (`Decision 6 (rings and keys) | Update for "only me": no co-keeper`), 530 (`Split "Fri 19 Feb 2027, Withdrawals close; picture lock"`), 535 (`loudnorm I=-16:TP=-1.5:LRA=11`), 540 (`Change "Use 4K only after the venue screen is confirmed"`). The targets of those four are already patched (`surprise-ops.md` 72, 291, 565; `toolchain.md` 154 and Decision 7), so the quotes are now misleading rather than wrong. Rows that grep shows are **not applied**: 544 (`agent-pipeline.md` G6, line 232, has no mono-fold, trims, safe-area or G6b), 538 (`toolchain.md` has 0 hits for `color_range` and `mono`), 551 (`ai-imagery.md` has 0 hits for "pre-roll" and "deepfake"; the six cue-sheet extensions are absent), 552 (`games.md` has 0 hits for "Finding 7" or "diff result"). The other rows were not individually checked.

### 1.4 `ROADMAP.md` and `PLAN-ON-A-PAGE.md`

- `ROADMAP.md:351` (section 14 item 1): `**Scribe passes not yet applied** ... every row of DECISIONS.md Table 4 (S-01...S-37), in particular the surprise-ops lab table before the pilot ships, the single-key rewrite of surprise-ops and its skill, ... format round 3 C1 (RQ1-RQ5), creator-threads G1-G6 ...`. Out of date: surprise-ops is at v5 with the lab table, single-key rewrite and contributor placeholders applied (`surprise-ops.md` 5, 47-53, 263-321, 871); `skills/surprise-tribute-operations/SKILL.md:8, 192` are reconciled; format, creator-threads, film-story and production-scale carry "Reconciled with DECISIONS.md" notes. Not individually verified: music-sound Template G, theatrical-delivery Step 12 and T8, production-scale T5. Replace item 1 with the three live rows above plus 1.3.
- `ROADMAP.md:306` (risk 14) names `25 fps, two keys, Fri 19 Feb lock` as the stale categories: intentional, not stale.
- `PLAN-ON-A-PAGE.md`: no hit for any Table 4 value or any of the six strings.

### 1.5 The six named strings

| String | Hits | Verdict |
|---|---|---|
| `not applied here` | `playbooks/music-sound.md:136` | False positive: body text, "the broadcast anchor in research G3 is not applied here". It would trip the W-29 grep if the grep is not heading-only; allowlist it or rephrase |
| `for the scribe`, `pending scribe` | none | Clean (but see 1.3 for "so that a scribe can patch them") |
| `Ring 1` | `surprise-ops.md:72`; `production-scale.md:90` | `surprise-ops.md:72` says Ring 1 is empty (intentional). `production-scale.md:90` is a substring false positive ("gathe**ring 1**4") |
| `co-keeper` | `surprise-ops.md` 5, 72, 203, 380, 565, 871; `craft-motion.md:10`; `skills/surprise-tribute-operations/SKILL.md` 8, 38, 48, 192; `theatrical-delivery.md:529` | All are negations ("there is no co-keeper") or the 1.3 delta row. None in `ROADMAP.md` or `PLAN-ON-A-PAGE.md` |
| `25 fps` | `theatrical-delivery.md` 489, 618; `agent-pipeline.md` 174, 279; `toolchain.md` 8, 90, 107, 663; `craft-motion.md` 300, 316, 317; `skills/free-creative-toolchain/SKILL.md` 12; `ROADMAP.md:306`; the recipe files in 1.2 | Playbook and skill prose is intentional: either "25 fps access copy only if a 50 Hz-only venue judders" (W-14) or "tested at 25, UNVERIFIED at 24". Only the recipe files in 1.2 are live |

---

## Part 2. Completeness-critic gaps against `ROADMAP.md` v2

Section numbers are those of `ROADMAP.md` v2.

| # | Gap | Verdict | Where `ROADMAP.md` handles it | What is still open |
|---|---|---|---|---|
| 1 | Premiere not planned as an event | **Handled** | Section 11 in full (venue in writing by Sun 15 Nov; guests, headcount and invitations about Sun 24 Jan; cover story and host by Sun 3 Jan; backup date and room; run sheet; non-technical failure); section 7 weeks 11, 14, 15, 19; section 9 Sun 15 Nov and Sun 3 Jan; section 12 risk 15; section 10 venue and food line | The `event` activity is promised (section 7 Hours, risk 13) but is not in `research/production-scale-fixtures/hours.csv` (activity enum has no `event`) or `model.csv` (0 hits). The occasion itself is never asked as a decision; section 11 writes "a gathering for her" without saying what for |
| 2 | Only-me contradictions; nobody covers the maker | **Handled** | Section 4 heading and 4.1 (maker's cold reads replace proxy viewings); 4.4 and section 9 Sun 1 Nov (sealed envelope, O-16); section 12 risk 4 (F-0 after a ten-day gap, logs kept current); section 11 (roles written by Wed 24 Feb); section 7 weeks 16-17 (cold reads); playbooks purged of co-keeper (1.5) | A new conflict, Part 3 item 2: who hosts and who brings her |
| 3 | Effort model understates gathering and the Learn phase | **Partly** | Section 7 Hours paragraph (re-price gathering from the album-spread timing before Sun 1 Nov; add `gather_per_session` and `event` rows; split the curriculum); section 7 week 2 (time an album spread); section 8 (bold must-pass items); section 12 risk 13; W-06 | Scheduled, not done: `model.csv` row 51 still prices gathering at 0.6 / 1.2 / 1.8 h per finished minute and has no `gather_per_session` row. Section 8 bolds six items, W-06 lists eight (the settings card is a gate, the OTIO bundle is folded into the ORA item); say which |
| 4 | Sequencing inversions | **Handled** | (1) Section 3.4 and section 6 G1 row: hand-made material is answered in week 1 (O-06), filled at G1, one swap on Sun 13 Dec at 6 hours; `cinematic-quality.md:631` agrees. (2) Section 6 rows "Treatment (provisional)", "G-SLICE-0 and beat sheet v1" (provisional), "Inventory v1 frozen ... may revise it once". (3) W-07: slice C01 chosen from the maker's own material. (4) Section 7 weeks 2-4 and section 9 Sun 1 Nov (which tapes ship Fri 13 Nov and how they leave the house, O-18) | None |
| 5 | Local-system access; Windows column untested | **Partly** | Section 14 item 4 (W-28: one read-only probe, Exit A or Exit B, agent-on-PC rules first); section 7 week 1 (probe; `step0_pc_tests.ps1`); section 5.2 and section 12 risk 9 (Windows numbers UNVERIFIED until `windows_check_report.json`); section 8 week 1 (PC inventory re-keys GPU tier, Whisper model, WSL); `PLAN-ON-A-PAGE.md` Tue 20 Oct | A plan, not a result: the probe outcome is not recorded anywhere. The tool list for this seat shows no computer-use, browser or remote-device tool, so it cannot reach the maker's PC either; Exit B stands until the orchestrator's own seat reports. The agent-on-PC rules live in W-28 only, not as a file |
| 6 | Languages, observances, geography, country never asked | **Handled** | Section 9 Sun 25 Oct (O-02 country, O-10 family profile) and Sun 1 Nov (O-15 language, pulled forward from the radio cut); section 7 week 1; `PLAN-ON-A-PAGE.md` Sun 25 Oct; W-57 | Two small items are only in W-57 or nowhere: font and caption tests for non-Latin or code-switched speech (section 6 settings-card row does not mention them); the Whisper non-English correction test (story Ex 3 on the hardest-voice sample by Sun 8 Nov) is in no calendar row or curriculum row |
| 7 | Source types no researcher covered | **Handled** | Section 7 week 2 (Sonnet researcher briefed on the source-type matrix, W-58); section 13 agent table; section 14 item 5 | Not yet done: `inventory-template.csv` has no `source_type` column (header checked); the safe phone-export method is only in W-58 |
| 8 | Moving-image sources; stale frame rate | **Handled** | Section 7 week 2 (Haiku patches craft-motion "25" to "the project rate (24)" by hand after the r1/r5 re-run); section 7 week 4 (`r10_conform_footage`, W-59); section 14 item 5 (style-bible decision 11) | Not yet done: no `r10` recipe file; `cinematic-quality.md` has 0 hits for "moving footage"; recipes still 25 fps (1.2). Timing: W-59 and week 4 put `r10` on Sat 14 Nov, but a pilot tape shipped Fri 30 Oct to a fast lab (1 to 2 weeks) can come back from about Fri 6 Nov |
| 9 | `timeline.json`, transcription, captions have no spec or skill | **Handled** | Section 5.1 row "One timeline, two emitters"; section 6 L1 row; section 7 week 3 (Haiku drafts the three skills); section 13 note "Three skills to write before Sat 14 Nov" (W-31) | Not yet written: `skills/` has no `timeline-json-and-emitters`, `transcribe-to-inventory` or `captions-and-subtitles`. `research/sources/format-round1/timeline.example.json` is still 25 fps (research, not patched by design) |
| 10 | Cookie-cutter guard; no taste input; test misses "template-ness" | **Partly** | Section 3.4 (three "reference moments" and "what this film refuses to look like"); section 7 week 17 (S2 includes one viewer over 65 and, if possible, a teenager with a guardian); section 8 week 3 (two reference films) and weeks 10-11 (three, optional); W-34 (hero moments chosen with the stranger's question first) | (a) W-60 says six exemplar films are watched in weeks 2-3 as G1 input; `ROADMAP.md` shows two in week 3 and three optional in weeks 10-11, so the roadmap contradicts the register. (b) The two added T7 questions ("what does it remind you of?", "name one thing that could only be about her") appear in no file (0 hits in the playbooks, skills, `ROADMAP.md`, `DECISIONS.md`). (c) S1 has no older or young viewer; only S2 does (the week 9 caption test uses a viewer over 60). (d) The hero-shot reservation for the three most specific beats found by Sun 13 Dec is only implicit |
| 11 | No money decision | **Handled** | Section 10 (cost table, core total about $900 to $1,600 before venue and food); section 9 Sun 25 Oct (O-04, pending); section 10 closing line ties the ceiling to lever 3, the songs and the consult; `PLAN-ON-A-PAGE.md` decision table | The maker's number is still pending (O-04) |
| 12 | The same propagation failure keeps recurring | **Partly** | Section 0 (precedence and `stale_check.py`, W-29); section 5.1 "Close the day"; section 7 weeks 1-2 (script written week 1, first run Fri 30 Oct); section 12 risk 14; section 14 item 1 | `stale_check.py` does not exist: there is no `scripts/` directory in `.` or `/home/user/animated_journey`. Section 14 item 1 is out of date (1.4). Three Table 4 rows are still live (1.2). The 1.3 delta table escapes the planned patterns |

Tally: 8 handled, 4 partly, 0 not handled. In most of the "handled" rows (1, 7, 8, 9, 11) the work is scheduled and the artefact (model row, column, recipe, skill, the maker's number) does not exist yet; that is the right state for 18 Oct but each needs a dated check at the Sun 1 Nov or Sat 14 Nov gate.

---

## Part 3. Integration problems found on the way

1. **The git working copy is pre-reconciliation.** `/home/user/animated_journey` (the repo to be made private) has none of `DECISIONS.md`, `PLAN-ON-A-PAGE.md`, `skills/` or `agents/`; its `ROADMAP.md` is v1 (89,721 bytes against 75,507) with `ROADMAP-ADDENDUM.md` and `ROADMAP-ADDENDUM-FILM.md` still at the top level; all 16 playbooks differ from `playbooks/`; they still contain 12 `co-keeper` hits, 2 `Withdrawals close; picture lock` and 2 `fps=25|d=125|-r 25`. Anything an agent loads from the repo is the stale copy. Sync the life-journey tree into the repo, run the stale check there, and commit only after O-13 (private) is confirmed.
2. **Who hosts and who brings her disagree.** `ROADMAP.md` section 11 and `PLAN-ON-A-PAGE.md` (Sun 3 Jan row: "you host") make the maker the host, and section 11 has the maker bring her by a route that avoids the guests. `playbooks/surprise-ops.md:476` says HOST and DISTRACTOR "belong to the true plan that brings her (chosen by Sun 3 Jan, O-32)" and are told only that plan; the run sheet (line 496) has the distractor arrive 45 minutes before and "if late, the host holds the room". If the maker is both, nobody holds the room while the maker fetches her. Decide at O-32 (Sun 3 Jan) and make `ROADMAP.md` section 11, `PLAN-ON-A-PAGE.md` and `surprise-ops.md:476` say the same thing.
3. **"The private cut" is undefined.** The maker's cold read of "the private cut" on Sun 14 Feb appears at `surprise-ops.md:290`, `story.md:154`, `ROADMAP.md:87, 200` and `DECISIONS.md` S-06, while D-06 and S-18 say there is no longer private cut. Presumably it is the family-key cut emitted from `timeline.json` (W-31). Say so once in `DECISIONS.md` Codes.
4. **Table 4 needs a status column.** Its line numbers no longer match the files, and 34 of 37 rows are applied. Add "applied / outstanding" per row so `stale_check.py` and the scribes work from the remaining list.
5. **W-29 pattern list.** Add the 1.3 phrase "so that a scribe can patch" and "Deltas to existing" to the stale-check strings, and allowlist `music-sound.md:136`.

---

## Changelog
- 2026-10-18, v1. Written by the Sonnet integration critic. Table 4: 34 of 37 rows clean, 3 live (S-01, S-08, S-10) plus one unlisted scribe to-do table. Completeness critic: 8 gaps handled, 4 partly, 0 unhandled.
