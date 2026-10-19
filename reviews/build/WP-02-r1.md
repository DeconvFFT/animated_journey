# Fable review: WP-02 ops files, round 1 of 3

*Fable advisor, Mon 19 Oct 2026, branch `build/process-lock`. Reviewed against `DECISIONS.md` as it stands now (167 rows: D 31, W 60, O 35, S 41, with D-31 added at 03:42 after the package was written) and against the real `scripts/redaction_patterns.json` (landed 03:39). Nothing committed; the evidence folder was backed up before the test run and restored afterwards.*

**Verdict: revise.** The scripts are well built and privacy-minded, the maker-facing pages are clear, and most of the package is a one-command fix away from passing. But as delivered three acceptance lines fail, the report describes a state the evidence folder no longer shows, and one privacy claim in the report is not true of the code.

## 1. What I re-ran

| Command | Result |
|---|---|
| `python3 -I scripts/decisions_to_csv.py --check ops/decisions.csv` | **exit 1**: `D-31 is in DECISIONS.md but missing from the CSV`; O-02 `short_title` and `note` differ. The committed CSV is the 166-row snapshot; the register moved. |
| `--write` into a scratch copy, twice | 167 rows (D 31, W 60, O 35, S 41); byte-identical; `--check` exit 0 on the fresh file. The generator is right; the committed file is stale. |
| `python3 -I scripts/ops_lint.py` | **exit 1**, the same four `decisions_mismatch` / `id_set` failures, nothing else. |
| `hours_report.py` on `ops/hours.csv`, `hours_9h30.csv`, `hours_7h30.csv`, `hours_bad_activity.csv` | all as specified: `no rows yet` exit 0; `9.5 h (570 minutes)` and the 9-minute reading; `7.5 h` and the F-0 reading; `line 3: activity 'Ga*******'` exit 1. |
| `make_fixtures.py && ops_lint.py --hours tests/ops/fixtures/hours_bad_note.csv` | exit 1 with masked hits for profile path (line 3), deny-list name (4), IPv4 (5), handle (6) and the length warning (7). **The planted e-mail on line 2 is not flagged.** |
| `bash tests/ops/run_tests.sh --all` | `8 FAIL, 34 PASS, 1 UNVERIFIED`, exit 1 (the report says `36 PASS, 5 BLOCKED`; the evidence folder, re-run at 06:25, already says `7 FAIL`). |
| `public_lint.py --paths ops scripts/ops_lint.py ... tests/ops build/evidence/wp02` | 0 findings. |

## 2. Tests of my own designed to break it

1. **Shifted columns in an hours file** (a row missing its date, a name landing in `date` or `minutes`). `hours_report.py` and `ops_lint.py --hours` both echo the `date` cell (`d[:20]`) and the `minutes` cell (`m[:12]`) **unmasked**: `date 'Zqxname Surname' must look like 2026-10-19`, `minutes 'Zqxname Full' must be a whole number`. `activity`, `shot_or_chapter` and `who` are masked as the report says; the other two columns are not. In a public repository whose test transcripts are committed, every echoed cell must be masked.
2. **A three-digit register ID.** A copy of the register with a `| W-100 | ... |` row: `decisions_to_csv.py --write` produced 167 rows and no warning, and `ops_lint`'s independent scan agreed, because all four regexes (`ROW_RE`, `REGISTER_ROW_RE`, `REG_ID_RE`, `SUPERSEDED_BY_RE`/`REPLACES_RE`) require exactly two digits. A row can vanish from the mirror in silence. Not urgent at 60 W-rows, but the fix is four characters.
3. **The planted e-mail against the real pattern file.** `make_fixtures.py` builds `...@mailbox-nowhere.example`, and `lint_neg_planted_text` plants `invalid@mailbox...example`. WP-03's file exempts the reserved domains (`reserved_example_email_domains`: `.example`, `.invalid`, `.test`, `.localhost`, `example.com/org/net`), so the `email` category never fires in either test. This is why `lint_bad_note` and `lint_neg_planted_text` fail in the evidence folder: the fixture, not the lint, is wrong. The pattern file's own positive sample (`ja`+`ne.doe+t`+`@`+`mailbox-`+`test`+`.io`) is the shape to use, ideally read from the file so the fixture follows WP-03.

## 3. Findings by rubric

**Correctness (3).** The three scripts do what the docstrings say and the boundary tests are thorough (W-02 thresholds, encodings, carry-over, malformed registers, fail-closed). Three acceptance lines nonetheless fail as delivered: `--check` exit 0, `ops_lint.py` exit 0, and the planted-e-mail line. The first two are the stale CSV (D-31, O-02); the third is the fixture's reserved TLD. `decisions_register_growth` hard-codes `"167 rows"` (run_checks.py:355) and so fails now that the register itself has 167; it will fail again at every register edit.

**Safety and privacy (3).** Good by design: the note column is never printed, only base names appear, the owner account name is written `<owner>` in the mirror (the register and charter still carry it; correctly left to the orchestrator), the deny list is local and git-ignored, the bad fixture is built from fragments and removed by a trap, `ops_lint` carries no identifying-data regex and fails closed. Nothing here could tip off the mother and no family media is touched. The gap is the unmasked `date` and `minutes` echo above, which contradicts the report's "free text echoed in an error ... is masked".

**Maker usability (4).** `HOURS-HOWTO.md` is one honest page a learner can follow: what counts, the twenty words, three examples, the Excel date tip, the "no names in note" sentence that also closes the `who` slot. `GATHER.md` reads as a checklist with blanks and tells the maker where each answer lives. The settings card explains every row in plain words with a proving command and the cost of changing it, and keeps `signed: no`. One line to fix: the card's status paragraph says the Devanagari placeholder "says nothing about her language" when D-31 now names Gujarati (and `pipeline/phone/test_strings.json` has Gujarati with zero strings, `pending_O-10`), so the maker should read that the Gujarati run is the one that counts.

**Fidelity to the plan and DECISIONS.md (3).** Every deliverable exists in its owner path, the status vocabulary, D-14/D-23 notes, O-05/O-13 answers, the phone row (D-27, proposed (J), to be replaced by `PHONE-ROW.md`), the Language-and-script line and the stand-in IDs `LJ-ST-0001..0005` are all as planned; the deviations in report §4 are sound (exit 1 per the acceptance line; the `.example` fixture choice was reasonable before the pattern file existed). But the register wins over the plan's "166 rows", and the package has not been brought up to it; the report (03:28) predates both the register change and the pattern file, so §3's PASS/BLOCKED table and §5's "not run" are no longer true, and the evidence folder (06:25) disagrees with the report in the same repository.

**Maintainability (4).** Small, readable, commented where it matters (KNOWN_SUPERSEDED with its exit condition, the owner placeholder, masking rationale), fixtures reused from `research/production-scale-fixtures`, the enum checked against them. Two snapshot numbers baked into tests (166 at run_checks.py:184 is already a soft note; 167 at :355 is a hard assertion) and the two-digit ID regexes are the only smells.

## 4. Critical issues (block approval)

1. `ops/decisions.csv` is stale against `DECISIONS.md` (D-31 missing; O-02 title and note changed): `decisions_to_csv.py --check` and `ops_lint.py` exit 1, so two acceptance lines fail as delivered, and `build/reports/WP-02.md` still reports them as PASS.
2. The planted e-mail acceptance test does not detect an e-mail against the real pattern file: the fixture uses the reserved `.example` domain that `redaction_patterns.json` exempts, so `lint_bad_note` and `lint_neg_planted_text` fail and the `email` category is unproven.
3. `hours_report.py` (and `ops_lint --hours` through it) echo the `date` and `minutes` cells unmasked in problem messages, so a name in a shifted row is printed in full; the report's masking claim does not hold for those two columns.

## 5. Nudges (at most six, concrete)

1. **Regenerate and re-report.** `python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv` (expect `167 rows (D 31, W 60, O 35, S 41)`), then re-run `bash tests/ops/run_tests.sh --all` and rewrite `build/reports/WP-02.md` §1 (row counts), §3 (the acceptance table from the real pattern file, no BLOCKED left) and §5 (what was actually run against `redaction_patterns.json`), so the report matches `build/evidence/wp02/summary.json`. State that the register, not the plan's 166, sets the count.
2. **`tests/ops/make_fixtures.py` line `EMAIL = ...` and `tests/ops/run_checks.py` lines 556 and 667:** replace the `.example` TLD with a non-reserved shape. Best: load `scripts/redaction_patterns.json`, join `categories[email].positive_samples[0]`, and use that string for the fixture and the planted text, so the fixture can never drift from WP-03's exemptions again. Keep the `.example` row at line 773 as the negative case it already is.
3. **`scripts/hours_report.py` `check_row`:** lines 159 and 165 echo `masked(d)` instead of `d[:20]` / `d`; line 179 echoes `masked(m)` instead of `m[:12]`; in `parse()` lines 125-126 drop the `found: ...` header echo or pass it through `masked()` per cell. Add a `hours_validation` assertion that a planted token in `date` and in `minutes` never appears in the output (the `hours_note_never_printed` test is the model).
4. **`tests/ops/run_checks.py` line 355:** compute the expectation from the live register (`"%d rows" % (len(current_rows) + 1)`) instead of the literal `"167 rows"`; turn the 166 snapshot at line 184 into the same live comparison or delete it.
5. **`ops/SETTINGS-CARD.md` Language-and-script status paragraph (line 21):** cite D-31: her language is Gujarati (Gujarati script; Android phone), `pipeline/phone/test_strings.json` has no Gujarati strings yet (`pending_O-10`), so the Devanagari run is a placeholder and the Gujarati caption and font test is the one that must pass before signing. Add `D-31` to the GATHER A1 O-10 row's Register cell for the same reason. Keep `<date>` and the `Scripts tested:` paste-over convention as they are.
6. **Two-digit IDs:** in `scripts/decisions_to_csv.py` (`ROW_RE`, `SUPERSEDED_BY_RE`, `REPLACES_RE`) and `scripts/ops_lint.py` (`REGISTER_ROW_RE`, `REG_ID_RE`), change `[0-9]{2}` to `[0-9]{2,3}`, and add a one-line negative test that a `W-100` row in a register copy appears in the CSV (my break test 2 is the recipe).

## 6. Scores

| Rubric | Score |
|---|---|
| correctness | 3 |
| safety_privacy | 3 |
| maker_usability | 4 |
| fidelity_to_plan | 3 |
| maintainability | 4 |

Round 2 should be short: items 1 to 4 are mechanical, and the design of the package does not need to change.
