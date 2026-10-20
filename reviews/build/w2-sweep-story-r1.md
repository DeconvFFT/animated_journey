# Fable review: stale-wording sweep, group sweep-story, round 1

Reviewed Tue 20 Oct 2026 on branch `build/process-lock`. Refs D-03, D-04, D-06, D-08, D-26, D-29, W-01 to W-05, W-10, W-77 and Table 4 rows S-05, S-08, S-09, S-10, S-18, S-26, S-38, S-45, S-50, S-56, S-61 of `DECISIONS.md`.
Files in scope: `playbooks/story.md`, `playbooks/film-story.md`, `playbooks/surprise-ops.md`, `playbooks/games.md`, `playbooks/hindu-frameworks.md`, `playbooks/saurashtra-world.md`, and the staged skill copies `skills-staging/life-story-interviewing/SKILL.md`, `skills-staging/life-story-interviewing/surprise-runbook.md`, `skills-staging/life-film-story-structure/SKILL.md`, `skills-staging/surprise-tribute-operations/SKILL.md`, `skills-staging/meaningful-game-mechanics/SKILL.md`.
Read: `git diff` of the five changed playbooks in full (`saurashtra-world.md` has no diff), `diff -u` of each staged skill file against its installed copy, the Table 4 rows above and D-06, D-23, D-29, W-02, W-10 in the register, `scripts/stale_patterns.json` for the cited rows, `research/surprise-ops.md` Table C and item 13, `research/games.md` sources, the installed `life-story-interviewing` files (`beat-sheet.md`, `question-bank.md`, `surprise-runbook.md`). `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and `.claude/` are unchanged; HEAD is still `bd8377a`, so nothing was committed.

**Verdict: approve** (correctness 5, safety/privacy 5, maker usability 4, fidelity 5, maintainability 4). Every stale hit in the group's files is gone, each reword matches the register row it cites, no citation moved and no value changed. Four small nudges below, none blocking; the orchestrator can install the five staged files as they stand.

## 1. What I re-ran (real output, this container)

| # | Command | Result |
|---|---|---|
| 1 | `python3 -I scripts/stale_check.py` (default), then `--json` to a scratch file and filtered by path | 377 files scanned, 81 FAIL and 2 WARN repo-wide; **0 hits in the six playbooks and 0 in the five staged files**. The remaining hits sit in `research/sources/*`, `research/*-fixtures/*`, `spikes/*` and the installed `.claude/skills/*` copies (not this group's files to edit) |
| 2 | Installed-skill hits that this group's staged copies are meant to replace | 10 hits: `life-film-story-structure/SKILL.md` 31 and 225 (S-18), `life-story-interviewing/SKILL.md` 181 (S-08 FAIL and WARN, S-38), `life-story-interviewing/surprise-runbook.md` 54 (S-10), `meaningful-game-mechanics/SKILL.md` 142 (S-45 twice), `surprise-tribute-operations/SKILL.md` 192 (S-05 twice). The staged diffs touch exactly those lines and nothing else except one appended changelog line per skill; the staged tree scans clean |
| 3 | `python3 -I scripts/stale_check.py --new-only` | exit 0: 0 new FAIL, 0 new WARN, 105 baseline hits no longer present (no regression introduced by the sweep) |
| 4 | `python3 -I scripts/public_lint.py --paths` over the six playbooks and five staged files | 11 files, 0 identifying-data findings, 0 hygiene findings |
| 5 | Citation count, HEAD against working copy (`[n]`, `[Pn]` tokens) | story 208 → 208, film-story 261 → 261, surprise-ops 364 → 364, games 110 → 110, hindu-frameworks 127 → 127. Register-ID tokens only rise (new changelog lines): 167 → 171, 217 → 222, 349 → 358, 95 → 98, 315 → 317 |
| 6 | `grep` for the retired literals across the eleven files (L1 lock, 25-minute private cut, closest insider, co-keeper, two proxy keys, Key 1, living room for four to eight, 6 to 10 minutes, 20 to 30 minutes, Contributors confirm, told only their part, the eight placeholder observances, Minecraft, voxel, MagicaVoxel, Replay Mod, Flashback, Java Edition) | Only negations remain ("there is no co-keeper", "no co-keeper to tell"), the "20 to 30 minutes" session length of W-49 (a live value, not S-18), the `story.md` 243 retirement note (section 3, nudge 1) and "Modrinth" in `games.md` v0.2 (nudge 3) |

## 2. Each change against the register

| File | Change | Row | Matches | Substance and citations |
|---|---|---|---|---|
| `film-story.md` header, runtime sketch, scenario table, retired-length note, Decision 1, changelog 0.4 | "no 25-minute private cut" → "no separate longer private cut"; "There is no 25-minute plan" → "There is no plan at that length" | D-06, S-18, S-16 | yes: D-06 says the former private cut is re-purposed into the April version | the 25-minute table row keeps *Mama Micra* [48a][48b][48c] and "Not planned"; changelog 0.2 and 0.3 keep "25-minute first hard beat" and "25-minute ending to 1:30" as history, which the pattern does not target |
| `film-story.md` changelog 0.3 | "Decision 7 insider-read wording" → "the Decision 7 wording on who reads drafts first" | S-08 | yes | history line, nothing dropped |
| `story.md` Step 16 | "The older 25-minute budget in beat-sheet.md" → "The earlier, longer budget formerly in beat-sheet.md" | D-06, S-18 | yes; `beat-sheet.md` 9 now carries the 9-or-12 budget and marks the ~25-minute one retired, so "formerly" is accurate | the old budget's shape (60 s cold open, five or six chapters, three Tuesdays, close, thanks) is kept as the superseded description |
| `story.md` changelog v0.3, v0.4, v0.5 | "the closest insider" → "the earlier first-reader role"; "L1 lock" → "the Sat 14 Nov process lock (now named P-LOCK)"; "'L1 process lock' becomes P-LOCK" → "The earlier name for the Sat 14 Nov process lock becomes P-LOCK" | S-08, S-38 | yes; no L1 honesty label was touched | — |
| `surprise-ops.md` Decision 0 | "week 2 (Oct 25 to 31)" → "the last week of October" | no row cited (nudge 4) | accurate: `research/surprise-ops.md` Table C row 2 is Oct 25 to 31; the register's week numbering (today Tue 20 Oct is build week 2) made the old label ambiguous | the "ran them to week 8" and the Table C citation stay |
| `surprise-ops.md` Key dates Mon 8 Feb, Checklist E | "contributors confirm their clip" → "each contributor checks their own clip"; "told only their part" → "told only the part they need" | S-09 | yes: both stay marked void under only-me, firing only if TD-L2c brought someone in (D-03, W-08) | — |
| `surprise-ops.md` Decision 8 | "(shared 6 to 10 minutes with a hard cap of 12; private 20 to 30 minutes)" → "(a short shared cut with a hard cap of 12, and a much longer private cut)" | S-18 | yes | the retired figures survive in `research/surprise-ops.md` item 13 (nudge 2) |
| `surprise-ops.md` Decision 12 | "a living room for four to eight" → "a small living-room reveal for a handful of people" | S-26 | yes | — |
| `surprise-ops.md` changelog v2 to v6 | the holiday name of the placeholder observance, "the co-keeper, the two proxy keys", "L1 lock" / "L1 process lock" generalised | S-05, S-38, S-56, S-61 | yes | sources [72], [73], [169] and the "[135] already taken" note stay |
| `games.md` changelog v0.2 to v0.5 | the game, the two replay mods, the asset tool and the edition question named generically | D-29, S-45, S-50 | yes; the research note keeps the names as a historical record, as v0.5 already said | [14], [15], [41], [59], [76] stay |
| `hindu-frameworks.md` changelog v3 | "are no longer schedule constraints" → "no longer shape the schedule" | W-77, S-61 | yes | — |
| `saurashtra-world.md` | no change needed; scans clean and carries none of the retired literals | — | — | — |
| staged `life-story-interviewing/SKILL.md` 181 | the S-08, S-38 and 25-minute wording generalised, P-LOCK named | S-08, S-18, S-38 | yes | — |
| staged `surprise-runbook.md` 54 | "a spoken consent that names the Feb 27 use" → "the consent card (which names the premiere use)" | S-10 | yes: the sentence still routes any early Door A recording to TD-L2c; the S-10 literal is the one the row lists for runbook 54 | [87] and the W-49 citation stay |
| staged `life-film-story-structure/SKILL.md` 31, 225 | "no 25-minute private cut" → "no separate longer private cut" | S-18 | yes | — |
| staged `surprise-tribute-operations/SKILL.md` 192 | "the co-keeper, the two proxy keys and the partner role" → "the earlier extra-key arrangement and the partner role" | S-05 | yes | — |
| staged `meaningful-game-mechanics/SKILL.md` 142 | "Original voxel assets only" → "Original assets only for the earlier game-world look"; "the Minecraft chapter" → "the game-edition chapter" | D-29, S-45 | yes | O-05, W-30, D-23 references stay |

Each changed file ends with a dated sweep line that names the rows and says "No value changed", which is true of every diff I read. The hard rules hold: no family media, nothing identifying (lint row 4), nothing under `.claude/` edited (the staged copies carry the change), nothing committed.

## 3. Nudges (none blocking)

1. **`playbooks/story.md` line 243, the "Note" on the retired phrase.** Its last sentence still says the runbook, question bank and beat sheet "still carry 'insider' and consent-card lines and are patched in a separate pass". That pass has happened: S-08 and S-10 read "applied today", `question-bank.md` has no "insider", and `surprise-runbook.md` 9 and `beat-sheet.md` 23 carry only the negation "there is no insider". The line passes the checker (it is a retirement note) but tells a reader to expect work that is done; rewrite the last sentence to say those files now carry the only-me wording (S-08, S-10 applied 2026-10-19).
2. **`playbooks/surprise-ops.md` Decision 8.** The retired lean lost its figures ("6 to 10", "20 to 30"). That is what S-18 asks for, and the numbers survive in `research/surprise-ops.md` item 13; add that pointer in the sentence or in the v7 line so the history stays findable.
3. **`playbooks/games.md` changelog v0.2.** With the neighbouring names generalised, "Modrinth telemetry confirmed" is now an orphaned proper noun from the retired ecosystem (it is the host of the replay mod, `research/games.md` [46], [47]). Either generalise it ("the mod host's telemetry confirmed") or leave it with a pointer to the research note; the checker does not flag it either way.
4. **`playbooks/surprise-ops.md` changelog v2 and v7.** v2 now begins a sentence in lower case ("a placeholder observance moved to weeks 7 and 8"). v7 lists the Decision 0 reword ("the last week of October") without a reason or row; one clause saying the notes' own week numbering differs from the register's (build week 2 is the week of Mon 19 Oct) would keep the next sweep from re-opening it.

Optional, not a nudge: the staged skills carry no `CHANGES.md` as WP-11b's did. For one-line changelog diffs this is fine; the appended changelog line in each `SKILL.md` serves the same purpose.

## 4. Scores

| Criterion | Score | Why |
|---|---|---|
| Correctness | 5 | 0 hits in the eleven files; `--new-only` clean; the ten installed-skill hits are covered line for line; every reword checked against its row |
| Safety and privacy | 5 | `public_lint` 0 findings; no names, dates of her life, places or media; `.claude/` untouched; nothing committed; nothing left the repo |
| Maker usability | 4 | the prose still reads as plain instructions; one stale "still to be patched" note and one lower-case sentence start are the only rough edges |
| Fidelity to plan | 5 | the sweep did only what the group asked: wording, cited by row, with no value, date or citation changed; `saurashtra-world.md` correctly left alone |
| Maintainability | 4 | dated sweep lines in every file; one reword (Decision 0) lacks its reason, and the `story.md` 243 note will mislead the next sweeper until fixed |

Approve. Nothing critical is open.
