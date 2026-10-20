# The spike verdicts: one writer per file

*Set up Tue 20 Oct 2026 (week-2 gate round 1, nudge 6): `spikes/VERDICTS-W2.md` had been overwritten once by a second implementor, and week 3 adds the SP4 row. From now on that file is **generated**; nobody edits it.*

## The rule

| File | Who writes it | What it holds |
|---|---|---|
| `spikes/verdicts/SP1.md` | the package that runs SP1 (the Craft CLI tests) | the SP1 row, the SP1 line of "Decision rules, quoted", the six T1 to T6 rows, the SP1 "does not say" bullet |
| `spikes/verdicts/SP2.md` | the package that runs SP2 (Route A) | the SP2 row and rule line |
| `spikes/verdicts/SP3.md` | the package that runs SP3 (Blender) | the SP3 row, rule line and "does not say" bullet |
| `spikes/verdicts/SP4.md` | the package that runs SP4 (the idle test; week 3) | the SP4 row and "does not say" bullet |
| `spikes/verdicts/SP5.md` | the package that runs SP5 (validators and round trips) | the SP5 row |
| `spikes/verdicts/template.md` | the orchestrator only | the title and status words, the table headers, the "All five" rule, the disk decision, "How to check this file", the general "does not say" bullets |
| `spikes/VERDICTS-W2.md` | **nobody** (generated) | the template with every spike's parts put in order |

1. **Edit only your spike's file.** Never edit `spikes/VERDICTS-W2.md`, and never another spike's file. If you need a change in the shared prose (the header, the disk decision, a general bullet), put it in your report under "For the orchestrator"; `template.md` has one writer.
2. **After a change, run** `python3 -I spikes/verdicts/assemble.py`, then `python3 -I tests/spikes/check_verdicts.py` (the shape check of the assembled file). The assembly is a pure function of the files: running it twice, or two packages running it at the same moment, writes the same bytes (the write is atomic).
3. **Do not put an update history in the header.** A spike's date column and its package report say when it changed; the header line of `template.md` is the orchestrator's.
4. **A part file** is plain text with sections introduced by a line `<!-- part: NAME -->`, NAME being `row` (exactly one table row that starts `| **SPn** |`), `rule` (bullets `* SPn, ...`), `tests` (SP1 only: rows `| **Tn** ...`) or `not-said` (bullets for "What this file does not say"). A comment line `<!-- ... -->` is ignored.
5. **SP4 in week 3:** edit `SP4.md` (the row, and the "does not say" bullet that now says it is armed, not run), run the assembler. Nothing else changes.

## The check

`python3 -I spikes/verdicts/assemble.py check` exits 1 if `VERDICTS-W2.md` is not exactly what the parts assemble to, which catches a hand edit of the generated file and a part changed without a new assembly. It runs in the spikes quick suite (`verdicts.assembled` in `tests/spikes/run_tests.sh`) and so in `bash build/run_all_checks.sh --quick`.

If it fails because someone edited the generated file by hand: move the edit into the right part file, or, while no part file has been changed since the last assembly, run `python3 -I spikes/verdicts/assemble.py import` (it splits the current `VERDICTS-W2.md` back into `template.md` and the five spike files; a "does not say" bullet is given to the spike whose name it uses, and one that names none stays in the template) and then `python3 -I spikes/verdicts/assemble.py`.

## What the migration changed

The text of `VERDICTS-W2.md` is the same line for line, with two differences: a first line that says it is generated, and the "does not say" bullets for SP3 and SP4 now come in spike order (SP3 before SP4). Nothing else moved.
