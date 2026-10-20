# Fable review: package t1-saturday-guide, round 1

*Fable advisor, Tue 20 Oct 2026, branch `build/process-lock`. Package report: `build/reports/w2t-t1-saturday-guide.md`. Decision that raised it: `reviews/build/w2c-gate-r1.md`, section 6, item 3 (the orchestrator said YES to the dissolve line), following `w2-sp1-t2t4-r1.md` nudge 2 and the c1 report section 5, item 5. Synthetic material only; nothing committed or pushed; `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and `.claude/` are untouched (`git status` is empty for all six). Where this review says `<session scratchpad>`, the path holds the cloud session's id and is not written here.*

## Verdict: APPROVE

| Rubric | Score | Why |
|---|---|---|
| Correctness | 5 | The step is in the guide's source, the guide regenerates from it byte for byte (I regenerated into `<session scratchpad>` and `cmp` was silent), `check_guide.py` is 8 PASS, 0 FAIL, 0 UNVERIFIED, and every key the step names is what FilmCraft v0.9.0's own source binds (section 1, rows 4 to 6). The two additions beyond the orchestrator's sentence (the "could not tell" line and the button fallback) are both true to the source and both make a false finding less likely, not more. |
| Safety / privacy | 5 | `public_lint.py --paths` over the guide, its source and the report: 0 identifying-data, 0 hygiene findings. No non-ASCII character in either file (the guide is pasted into PowerShell 5.1). The report writes the scratch path as `<session scratchpad>` and the FilmCraft commit in its short form. The step asks her to paste two timecodes, nothing else; nothing personal, nothing contacted. |
| Maker usability | 4 | The block reads in the guide's voice for someone who has never opened a video editor: it names the playhead, the timecode and the Space key in plain words, says what a finding is and what to paste, and gives an answer she can give when she cannot tell. Two small things remain for her (nudges 1 and 2), and one larger thing that is not this package's doing: the five-minute test's test chapter is not in anything the guide copies to her PC (section 3, orchestrator item 1). |
| Fidelity to plan | 4 | Exactly the package: source edited, `build_guide.py` then `check_guide.py`, the SmartScreen bullet and the Step 3 checksum box unchanged (I diffed both sections against HEAD: identical), five hunks and nothing outside them, nothing protected touched, nothing committed. The orchestrator's rule is item 3 of the block in its own words. Items 4 and 5 go a little beyond the wording; the report says so and gives the two-command undo, which is the right way to add to a decided sentence. |
| Maintainability | 5 | The text lives only in the template string; no code outside it changed; `guide.in_sync_with_assets` still proves the guide is what the script writes; the footer records where the keys came from and that they are UNVERIFIED on Windows, so the next person knows what Saturday's paste settles. |

Nothing critical is open.

## 1. What I checked myself

| # | Command | Result |
|---|---|---|
| 1 | `git diff -- spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md spikes/sp1_craft_cli/build_guide.py` | 5 hunks in each, 12 insertions and 4 deletions in each; no hunk touches a table row, a 64-hex string, a PowerShell fence or a mode marker |
| 2 | `diff` of the Step 3 section and of the "If something goes wrong" section, HEAD against the working tree | Step 3 identical; the goes-wrong section differs only in the italic footer that follows it (the one sentence the report describes); the SmartScreen bullet is byte for byte what the gate approved |
| 3 | `timeout 120 python3 -I spikes/sp1_craft_cli/check_guide.py` (foreground) | 8 PASS, 0 FAIL, 0 UNVERIFIED; exit 0. G1 14 fences, 0 non-ASCII; G2 pwsh 7 parses all 14; G4 6 table rows, 6 hashes, no problem; G6 the made-up `x@y` folder prints as `<redacted>` |
| 4 | `python3 -I spikes/sp1_craft_cli/build_guide.py --out <session scratchpad>/guide-regen.md` then `cmp` against the tracked guide | byte-identical, 284 lines |
| 5 | `grep -P '[^\x00-\x7F]'` over the guide and `build_guide.py` | no match |
| 6 | `python3 -I scripts/public_lint.py --paths` on the guide, `build_guide.py` and the report | 3 files, 0 identifying-data, 0 hygiene findings |
| 7 | `timeout 200 bash tests/sp1/run_tests.sh --quick` (foreground, about 15 s) | 15 PASS, 0 FAIL, 0 BLOCKED, 1 UNVERIFIED (`guide.windows_behaviour`, as always); `guide.in_sync_with_assets` PASS, `guide.check_guide` PASS; exit 0 |
| 8 | FilmCraft clone at tag `v0.9.0` (commit `4a69a03`): `crates/engine/src/commands.rs` lines 2514 to 2521 | `playhead.stepForward` on `Right`, `playhead.stepBack` on `Left`, the many-frame versions on `Shift+Right` and `Shift+Left` reading `prefs.playback.step_many_frames` |
| 9 | same clone, `crates/engine/src/autosave.rs` line 110 and `settings_tests.rs` line 189 | `step_many_frames` defaults to 5, so "Shift moves five" is right unless she has changed a preference she has never seen |
| 10 | same clone, `crates/engine/src/shortcut_presets.rs` lines 166, 353, 387 | `playback.toggle` is `Space` in every preset |
| 11 | same clone, `crates/ui-egui/src/panels/monitor.rs` lines 925 to 927 and 323 to 339 | the Program monitor's transport row is Step Back, Play-Stop, Step Forward, with the tooltip "Step Forward 1 Frame (Right)"; the timecode field sits in the monitor's controls row |
| 12 | same clone, `crates/ui-egui/src/lib.rs` lines 1465 to 1473 | shortcuts are dropped while a text field or other widget has keyboard focus, which is exactly the dead-key case item 5 of the block sends her round with the button |
| 13 | `git status` on the six protected paths | empty |

## 2. The block, line by line

* **Item 1** (stop, move the playhead to a few frames before the dissolve): true to the app; the one thing it does not say is how to move the playhead (nudge 1).
* **Item 2** (Right once and look, Left back, do not hold Shift): matches rows 8 and 9.
* **Item 3** (every frame should differ; two identical frames while the timecode moves on are a finding; paste both timecodes): the orchestrator's rule, with the one qualifier that makes it testable by eye, "while the timecode moves on", which rules out a key that simply did not register.
* **Item 4** ("could not tell" at the ends): the c1 measurement had the first steps at about six levels of 255, which is below what an eye finds on a gridded card. Without this line the maker is pushed to call a true frame pair "identical" and the Sunday review gets a false finding. Keep it.
* **Item 5** (the button, and write down that the keys did not work): row 12 is the mechanism; the tooltip text in row 11 is what she will see. Keep it.
* **The three other edits** (the opening parenthesis, the "one exception" clause, the "What to write down" sentence, the footer) each close a sentence that would otherwise be untrue or leave the paste with no place to go. Right.

## 3. What this review does not cover

Nothing about Windows: the keys, the focus behaviour and what she sees are all v0.9.0 source read on Linux, and the footer says so. Nothing about v0.8.0's bindings (the clone holds only the `v0.9.0` tag; the fallback's shortcuts stay unchecked). Nothing about whether the exported dissolve steps on her build, which is the point of the line.

One thing outside the package that the package made visible: the FilmCraft five-minute test (`playbooks/craft-motion.md` checklist B and the research note's R7 line 502) imports "the agent's `ch01.otio`", a test chapter with one dissolve and one Ken Burns move, and plays it. **No `.otio` file is tracked in the repo** (`find` over the tree finds none), and the guide's Step 6 copies only the five `craft-visual-fixtures` files (PhotoCraft, VectorCraft and LightCraft). The SP1b driver `t3_filmcraft.py` writes a `ch01.otio` into a hand-off folder in scratch, not into the tree. So as the guide stands, on Saturday she reaches the FilmCraft row of Step 7, opens checklist B, and has no chapter to import, play or step through; the new block inherits that gap. It was already true of the approved guide ("Play 10 seconds" needs the same file), so it is not this package's defect, but it is the one thing between the guide and "ready before Sat 24 Oct" (orchestrator item 1).

## 4. Nudges (none blocking)

1. **Item 1 of the block: how to move the playhead.** She has just played 10 seconds, so the playhead is past the dissolve. One clause makes the line self-contained for someone who has never dragged a playhead: "press Left until the timecode is a few frames before the dissolve, or click in the time ruler above the clips". The first half is safe on the source (row 8); the second is the usual editor convention and would carry the same UNVERIFIED mark as the rest.
2. **Item 3, "beside the picture".** The monitor's timecode field is in the controls row of the Program monitor (row 11), which lays out under the picture in the default dock. "the time number under the picture" is a one-word change if the orchestrator wants it; "beside" will still find it.
3. **Reading time.** The guide still says "about 90 minutes". The block adds a few minutes of stepping; either leave it (the number was always an estimate dominated by downloads) or make it "about 90 to 100 minutes" in the same pass as nudge 1.
4. **The playbook is behind the guide** (the report's item 2). `playbooks/craft-motion.md` checklist B line 229 still stops at "Play 10 seconds". The guide calls its block "the one exception" to the no-drift rule, which is honest but makes two homes. The smaller fix is one checklist line in the playbook in the orchestrator's words, after which the guide's clause and its block can shrink to a pointer. Not protected, but outside the package, and a playbook change wants its own `stale_check.py --new-only` and `public_lint.py` run.
5. **Footer sentence.** "Shift moves five" is a preference default (row 9), not a fixed binding. If the footer is touched again, "Shift moves five by default" is the exact statement; today's wording is right for a fresh unzip.

## 5. For the orchestrator

1. **Before Sat 24 Oct: give her the test chapter.** Decide one of: (a) track a small synthetic test chapter under `research/craft-motion-fixtures/` (two gridded test-card PNGs at the conformed size, `ch01.otio` with one 12-frame cross dissolve and one Ken Burns move, metadata version; the SP1b T3 driver already builds the equivalent in scratch, and generated non-personal images may be added with `git add -f` after review) and add those names to the guide's Step 6 copy list via `build_guide.py` then `check_guide.py`; or (b) hand the SP1b hand-off folder to her PC by the route the PC inventory used, and say so in Step 6; or (c) accept that Saturday's FilmCraft test covers start, version, new sequence, save and export only, and move the play and dissolve lines to the first chapter pass. Without one of these the new block has nothing to look at.
2. **Keep or cut items 4 and 5** of the block (the report's item 1). My reading: keep both; the undo is two commands.
3. **One home for the checklist** (nudge 4): a playbook edit is outside both this package and the protected set; it is yours to assign.
4. **`run_all_checks.sh --quick` is red for the `skills-staging/` reason only**, as the report's section 3 and the t2 review's orchestrator item 2 both record: `build/run_all_checks.sh` line 93, `tests/integration/run_checks.py` `BUILD_ROOTS` and the theme guard's staged part, and `docs.staged_skill_update`. Not this package's files. The `sp1` area, the only one that reads the guide, is green.
5. **Evidence churn.** My quick SP1 run rewrote `build/evidence/wp07/guide_check.json`, `summary_quick.json` and `tests_quick.jsonl`, on top of the implementor's two quick runs; 95 paths under `build/evidence/` are modified in the tree from all packages today. Decide at commit time which evidence to keep; `wp07/tests.jsonl` (the `--all` envelopes) is unchanged.
6. **Sunday 25 Oct.** If her paste has an identical pair, or a "could not tell" that is more than the two end frames, it belongs in the same review as the `T2.dissolve_steps` ruling (c1 report, section 4), not in a new thread.
