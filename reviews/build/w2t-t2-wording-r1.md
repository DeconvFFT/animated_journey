# Fable review: package t2-wording, round 1

*Fable advisor, Tue 20 Oct 2026, branch `build/process-lock`. Package report: `build/reports/w2t-t2-wording.md`. Gate that raised the items: `reviews/build/w2c-gate-r1.md`, section 5. Synthetic material only; nothing committed or pushed; `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and `.claude/` are untouched (confirmed by `git status`).*

## Verdict: APPROVE

| Rubric | Score | Why |
|---|---|---|
| Correctness | 5 | Every lettered item (a to g) is done as asked and every check I re-ran agrees with the report (section 2). The new `prepare_defects.py` is idempotent on the real `tests.jsonl` copy (49 to 37 lines, second run byte-identical) and refuses without the marker; the marker `fake.verify_flipped_byte` is indeed the last part-1 line in the tracked file (index 36 of 49, followed only by the 12 `fake.defect_*` lines). |
| Safety / privacy | 5 | `public_lint.py --paths` over the 13 changed or new files: 0 identifying-data findings, 0 hygiene findings. No session id, scratch path or account string in any of them (grepped). `prepare_defects.py` prints no machine path. Nothing personal, nothing contacted. |
| Maker usability | 4 | The verdict now shows evidence as recorded, the research note says in one place where dissolve smoothness is judged, and the fixture README points at the one tool that measures MO8. Two small things remain for a reader (nudges 1 and 2). |
| Fidelity to plan | 5 | Scope held: the package named line 266 of `tests/phone/run_checks.py` and the implementor left line 746 alone and reported it; SP1 wording went through `verdict.py` and `assemble.py check`, never `VERDICTS-W2.md` directly; the baseline got exactly one dated re-cut line tied to the pattern change (the only kind the tool's header allows); the AL-7 choice is the first of the two options the package offered, with the undo path written down. |
| Maintainability | 4 | Pattern ids keep their `W-29.` prefix so earlier reports still find them; AL-7 is scoped to one file, one row (S-01) and one literal phrase, with its own positive and negative samples; AL-6a to AL-6e had to follow the patterns to S-66 and the `source` line says so. The one cost is that the allowlist grew by an entry to show a recorded phrase (nudge 3 records the alternative for the future). |

Nothing critical is open.

## 1. What I checked myself

| # | Command | Result |
|---|---|---|
| 1 | `python3 -I scripts/stale_check.py --self-test` | 66 Table 4 ids (S-01 to S-66) read from `DECISIONS.md`; 17 entries (8 structural), 94 patterns, 67 rows; 1076 checks, 0 problems |
| 2 | `python3 -I scripts/stale_check.py --audit-allowlist` | no dead entries (17 entries, 8 unused by design); AL-7 suppresses its hit |
| 3 | `python3 -I scripts/stale_check.py --new-only` | 0 new FAIL, 0 new WARN, 0 baseline hits no longer present; exit 0 |
| 4 | `python3 -I scripts/stale_check.py` (report) | S-29 no longer in the summary; S-01 7 FAIL (20 allowlisted), S-39 11, S-50 41, S-61 2 FAIL 1 WARN; no regression |
| 5 | `python3 -I spikes/verdicts/assemble.py check` | "VERDICTS-W2.md is exactly what the parts assemble to (73 lines)" (73, not the report's 72: another package added a line to a part since; still in sync) |
| 6 | `python3 -I spikes/sp1_craft_cli/drivers/verdict.py --print` diffed against `VERDICT-SP1A.md` | identical except print's trailing newline, so the committed verdict is what the driver generates |
| 7 | `python3 -I tests/phone/lint_strings.py` | 14 files scanned, 0 findings; the third root `.claude/skills/mobile-phone-delivery` exists and is scanned |
| 8 | `python3 -I tests/sp1/prepare_defects.py` on a copy of the tracked `build/evidence/wp07/tests.jsonl` in `<session scratchpad>` | kept 37, dropped 12; second run kept 37, dropped 0, file byte-identical |
| 9 | `timeout 200 bash tests/sp1/run_tests.sh --quick` | 15 PASS, 0 FAIL, 1 UNVERIFIED (`guide.windows_behaviour`), `defects_only.idempotent_and_refuses` PASS; exit 0 |
| 10 | `python3 -I scripts/public_lint.py --paths <the 13 changed or new files>` | 0 identifying-data, 0 hygiene findings |
| 11 | Reading: `DECISIONS.md` line 339 (S-66 row), `ROADMAP.md` row 136, `research/craft-motion.md` headings (R2 at line 378, R8 at line 507, the T2 row inside R8), `spikes/sp1_craft_cli/drivers/t2_filmcraft.py` line 317 | the S-66 status copy in the pattern file matches the register cell; row 136 is the "LightCraft scan batches, FilmCraft chapter pass, master assembly, backups / Never / Yes" row; the "see T2 in R8" and "(R2, step 2)" cross-references in the research note both resolve; the 0.9.0 driver does word the speed mark as "scaled to 2,400 frames at this film's 24 fps", so the `mark_text()` docstring is true |
| 12 | `git diff spikes/VERDICTS-W2.md` | the diff in the tree is other packages' (SP3, SP4 and the kept-environments rows); this package added nothing there directly |

## 2. Item by item

* **(a)** The retired figures are gone from the "Fails when" cell; the dated sentence states the present agreement (3.5 Mb/s, 32 characters, since 2026-10-20). Fine as a dating; see nudge 2 for the placement.
* **(b)** Both default-root sites and the label name `.claude/skills/mobile-phone-delivery`. The lint scans it; it is clean.
* **(c)** The outcome line reads exactly as asked and the row-136 pointer is correct. `SP1.md` quotes no part of the line, so no edit there was right; `assemble.py check` passes.
* **(d1)** Idempotent and refusing, proved three ways (unit, wiring in a copy, quick suite); the marker choice is sound (see Correctness). The script's header documents the new exit 2.
* **(d2)** The display-time reword is gone and the 0.8.0 cell shows the envelope's phrase as recorded. AL-7 is the right call of the two offered: a "(wording as recorded)" suffix would not silence the S-01 hit, and rewording evidence at display time is the worse habit. The entry is as narrow as an entry can be (one file, one row, one literal phrase, window 0). I endorse it under D-32; the orchestrator's confirmation is still listed below because the allowlist header reserves new entries to them.
* **(e)** One dated amendment at the T2 row (linear-light mix, same tolerance, the 28.50-level first failure, `T2.dissolve_steps`, pointer to the T2 row of `VERDICTS-W2.md`) and the probe-versus-export finding at R2 step 2, where `render --seconds` is prescribed, each pointing at the other. Exactly what was asked.
* **(f)** The MO8 sentence now points to W-41 and `mo8_audit.py` with the two jitter marks and calls the roughness informational; the `S-29.mo8-ratio` hit is gone from the report and the baseline.
* **(g)** Both phone patterns carry `row_id` S-66; the S-66 row exists with the register's status; W-29 no longer carries the phone figures; AL-6a to AL-6e follow to S-66 (necessary, as the report explains: a hit is filed under the pattern's row); one dated provenance line covers (f) and (g) with the before and after counts (63 to 62; 1 removed, 0 added), which `--baseline` confirms.

## 3. Nudges (none blocking)

1. **`spikes/sp1_craft_cli/drivers/verdict.py`, `mark_text()` docstring.** "the driver now words the same fact as ..." names no file, and the function sits in `drivers/`, so a reader can take it to mean `verdict.py` still rewords. Say `t2_filmcraft.py` (line 317) there.
2. **`tests/integration/README.md` line 29.** The dated sentence sits in the "Fails when" column, where it reads as a state rather than a failure condition. Either move it to the "Checks" cell of the same row or leave it; the figures are right either way.
3. **For the next time a recorded phrase trips a stale pattern.** AL-7 is fine today, but the pattern is a growing allowlist. The longer-term route is the one gate c1 nudge 3 already asked for: key the amended-mark paragraph and the mark text on the envelope's own fields, so old envelopes are labelled by date rather than allowlisted by phrase. Not for this package.
4. **`tests/phone/run_checks.py` line 746** (reported by the implementor, outside the lines the package named): the `public_lint` test still lists `skills-staging/phone-delivery`; the list is filtered by existence so nothing fails, but the installed skill is not scanned there. One-word change for whoever next opens the file.
5. **`spikes/verdicts/SP1.md`, `not-said` part (optional, from gate c1 nudge 2).** One sentence that dissolve smoothness is judged on the export, not the single-frame probe, would put the rule beside the T2 row that already states the finding. Goes through `assemble.py`, never `VERDICTS-W2.md`.

## 4. For the orchestrator

1. **Confirm AL-7** (`scripts/stale_allowlist.json`), the one new allowlist entry; the header reserves new entries to you. My reading: keep it. Undo path is in the report (delete AL-7 and its `source` sentence, restore the regex in `mark_text()` from git).
2. **`skills-staging/` is gone but three scripts still name it**, outside this package's files: `build/run_all_checks.sh` line 93 (`lint.build_folders` passes it to `public_lint.py --paths`, which exits 2 on a missing path, the only reason that line is red in the quick run), `tests/integration/make_evidence.sh` line 44, and `BUILD_ROOTS` plus the `theme_guard` helper in `tests/integration/run_checks.py` (around lines 55, 1452 to 1500, 1572, 1625). A one-word drop clears it.
3. **`scripts/stale_check.py` line 6** still says "S-01 to S-65 in register v3"; the tool's own self-test now reads 66 ids. A docstring fix for whoever next edits the tool (it is the tool, not a pattern file, so the implementor rightly left it).
4. **Gate c1 nudge 3 still stands** (key the amended-mark paragraph in `verdict.py` on `first-mark/t2_<app>_<tag>.json` for that tag and read the deviation from it); it matters when a T2 run on another pin appears.
5. **Evidence churn.** The quick suites rewrite tracked evidence under `build/evidence/` (`wp07/*_quick.*`, `wp08`, and other packages' `wp02`, `wp04`, `wp11a`); my own quick run of `tests/sp1/run_tests.sh` added to it. Decide at commit time what to keep; `build/evidence/wp07/tests.jsonl` (the `--all` envelopes) is unchanged.
6. **The full 12-defect `--defects-only` run was not repeated** (about 5.5 minutes); the new step is proved on its own, through the wiring and in the quick suite. Run it once before P-LOCK if you want the end-to-end line in evidence.
