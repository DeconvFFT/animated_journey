# Package k2-pr4-skill-parity: the PR4 photo rule in the installed skills, the guard, and the counts

Sonnet implementor, Tue 2026-10-20, branch `build/process-lock`. Synthetic material only. Nothing committed or pushed. No binaries. `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and everything under `.claude/` were not touched: the five skill edits are staged copies in `skills-staging/` for the orchestrator to install. Fable has not read any of this yet (D-32).

## The sentence

PR4, the seva-article rule, is read by the guard from the Codes line of `DECISIONS.md` (307 bytes, ASCII; W-61 and W-70 read the same):

> her Thakorji, chitraji, any picture of hers and anything inside the mandir are never photographed without her knowing; a seva article outside the mandir (the jhari in its cloth, the lamp, the closed doors) may be photographed by sight, untouched, on an unsynced phone (O-58), each logged as a G5 flag (O-48)

The Codes line adds a pointer after it, "(touching or handling any seva article without her knowing is PR10/PR14, W-70)"; as in the playbooks (t4), that pointer is not part of the sentence and is not copied.

## What changed

### 1. Staged skill copies (the orchestrator installs them; `diff .claude/skills/<name>/SKILL.md skills-staging/<name>/SKILL.md` shows exactly these lines and no others)

| Staged file | Lines | Change |
|---|---|---|
| `skills-staging/pushtimarg-seva-and-pichwai/SKILL.md` | 98; 131 | Guardrails, Surprise: "Never photograph her picture, her pichwai or her Thakorji without her knowing (PR4; D-02; D-17)" is now "PR4 (D-02; D-17), as the register states it:" plus the sentence. One dated changelog line. |
| `skills-staging/hindu-visual-language/SKILL.md` | 39, 40, 95; 145 | Step 4 (39): "photographs no svarupa, no picture of hers and nothing inside the mandir without her knowing (PR4, step 5)"; this is the prohibition-only form, with a pointer to step 5. Step 5 (40): the route "her own photograph of seva objects that are not a svarupa (...), `cloud: none`, under PR4 as the register states it:" plus the sentence, then "(W-70; `research/pushtimarg-world.md` PR4, F6: a picture may be pusht and in seva)"; the old "by sight and untouched ... on an unsynced phone" and "never the Thakorji, Lalan, chitraji ..." wording is replaced by the sentence, which says both. Guardrails, Privacy (95): the same sentence after "and only seva objects that are not a svarupa (...)". One changelog line. |
| `skills-staging/ai-photo-to-animation-pipeline/SKILL.md` | 54, 120; 191 | Route A deities line (54): "... a possible seva object (PR3, PR4). PR4, as the register states it:" plus the sentence (the layout of `playbooks/ai-imagery.md` line 207). Ethics guardrails, Deities (120): "PR4, as the register states it:" plus the sentence. One changelog line. |
| `skills-staging/mobile-phone-delivery/SKILL.md` | 130; 227 | Guardrails, Deities: "nothing in her seva space is photographed without her knowing (PR4)" is now "PR4, as the register states it:" plus the sentence (the layout of `playbooks/mobile-delivery.md` line 322). One changelog line. |
| `skills-staging/agent-first-production-pipeline/SKILL.md` | 153; 156 | The 2026-10-19 change-log entry ended "See `skills-staging/agent-first-production-pipeline/CHANGES.md`", a folder the install removed; it now ends "See `CHANGES.md` in this skill's folder." One changelog line. |
| `skills-staging/agent-first-production-pipeline/CHANGES.md` | new | A 1.5 KB staging note. It is there because the check `docs.staged_skill_update` reads a staged folder only when it holds both files, and falls back to the installed skill otherwise; the installed `SKILL.md` still has the dangling pointer, and `skills-staging/` is a code folder again while it exists (issue 26), so the fallback would fail on that pointer until the install. |

The changelog lines are not in your list ("change only those lines"); they follow the repo's rule that every skill edit has a dated line, and each can be dropped by deleting one line.

The three lines with the sentence in `hindu-visual-language` are two verbatim copies (40, 95) and one prohibition-only restatement (39): a third copy of a 307-byte sentence two lines above the first would only add a place to drift. If you want 39 verbatim too, it is one line and the table in the guard changes from 2 to 3.

### 2. The parity guard (issue 28 item 1)

- `scripts/pr4_parity.py` (new, read-only, stdlib). Reads the sentence from the Codes line, counts it byte for byte in each file of its table, prints one line per file (found / expected), and exits 1 on any difference. It also fails on a near copy (a line with the sentence's first words, or its second clause, but not the whole sentence: a copy that drifted), on a copy in a file the table does not list (`playbooks/`, `.claude/skills/`, `skills-staging/`, root `*.md`), and when the clause-aligned family of `playbooks/hindu-visual.md` does not have its expected lines. A skill is read from `skills-staging/<name>/SKILL.md` while that staged copy exists, otherwise from `.claude/skills/<name>/SKILL.md`; the output says which. `--self-test` builds a synthetic tree and plants 16 cases (one changed word, one changed character, a lost copy, a lost file, one copy too many, an unlisted file with a copy, an unlisted half-copy, a lost clause-aligned line, the changelog not counted, a wrong staged copy beating a right installed one, a superseded installed copy not being a stray, the Codes line with and without its pointer, no Codes line).
- `tests/integration/run_checks.py`: new test `parity.pr4_sentence` (quick and all) that runs the guard and its self-test; the header docstring and a row in `tests/integration/README.md` say so.

What the guard prints today:

```
verbatim copies in all: 21 / 21 in 12 files
  DECISIONS.md 3, QUESTIONS-SUN-25-OCT.md 3, ROADMAP.md 1, PLAN-ON-A-PAGE.md 1,
  playbooks: pushtimarg-world.md 4, hindu-visual.md 1, ai-imagery.md 1, mobile-delivery.md 1,
  skills (staged, waiting to be installed): pushtimarg-seva-and-pichwai 1, hindu-visual-language 2, ai-photo-to-animation-pipeline 2, mobile-phone-delivery 1
clause-aligned lines in playbooks/hindu-visual.md: 6 / 6 at lines 36, 82, 219, 303, 370, 507
PR4 parity: PASS (21 verbatim copies in 12 files, 6 clause-aligned lines)
```

### 3. The count

The "eleven clause-aligned lines" are **six**: `playbooks/hindu-visual.md` has 1 verbatim copy (line 56) and 6 lines that say "untouched" and "each logged as a G5 flag (O-48)" without the whole sentence (36, 82, 219, 303, 370, 507; the dated changelog entry at 671 is history). The t4 report's own list is those 6 plus 5 prohibition-only lines (43, 51, 84, 178, 240) that add "anything inside the mandir" only, which is where "eleven" came from. The gate review's "seven" is the 6 plus the verbatim copy. Corrected in `build/BUILD-STATUS.md` issues 24 and 28 (issue 24 also now lists the four skills, 21 copies in all) and in `build/reports/w2t-t4-pr4-row.md` (a new bullet under `hindu-visual.md`, since that report never wrote the word "eleven"; the word is in `reviews/build/w2t-t4-pr4-row-r1.md` and `w2t-gate-r1.md`, which are records and were not edited).

### 4. `scripts/stale_patterns.json`

The two lines that gave "nothing in seva is photographed without her knowing (PR4)" as canonical text now say "PR4 the seva-article rule as the Codes state it": line 659 (the S-60 row) and line 2160 (the pattern `S-60.murti-photograph`). Both belong to S-60; S-61 (placeholder observances) carries no PR4 text, so the t4 report's "S-60 and S-61" was one row and its pattern. The `negative_samples` entry at 2155 ("nothing in seva is photographed without her knowing") was left: it is a string the regex must not match, not a canonical value.

### 5. An addition outside the list: the theme guard and staged copies

`scripts/public_lint.py --theme` (in the default scope: Part A `lint.theme_guard` and `hygiene.theme_guard` part 1) scans an untracked file whole, so a staged skill copy is judged on every line, including the installed skill's own rule statements and source titles ("Mughal-court layer", a book title with "Mughal", a "no Christian" clause). With the three staged skills in place it printed 8 findings, all on lines the installed skills already have, and the quick pass would stay red until the orchestrator installs or commits the copies. `theme_scan` now, in the default scope only (explicit `--paths` still scan whole), drops from a `skills-staging/<x>` file the lines that `.claude/skills/<x>` also has, the same rule `staged_skill_changes` already applies in the third leg of `hygiene.theme_guard`; a staged file with no installed counterpart is still scanned whole. An eight-line block with a three-line comment in `theme_scan` and one docstring line; three new results in `tests/hygiene/test_lint.py`. Undo: delete the block marked "package k2-pr4-skill-parity" in `theme_scan` and the three results. No keyword, path, cue or allow-list entry was changed, so a new line that uses an excluded motif is still a finding.

## Commands and results

| Command | Result |
|---|---|
| `python3 -I scripts/pr4_parity.py` (real tree) | exit 0, PASS: 21 / 21 verbatim copies in 12 files, 6 / 6 clause-aligned lines (36, 82, 219, 303, 370, 507) |
| `python3 -I scripts/pr4_parity.py --self-test` | exit 0, PASS, 16 cases. A first run of the real tree failed on my own changelog line in `mobile-phone-delivery` (it listed the sentence's first words), which showed the near-copy test works; the line was reworded and the staged copy regenerated |
| `pr4_parity.py --root <copy>` on an isolated copy with the staged files moved over the installed ones and `skills-staging/` removed (the orchestrator's install, simulated in the `<session scratchpad>`, deleted afterwards) | exit 0, PASS, the same counts, the skills read `[installed]`. The same copy with two skills put back to HEAD: FAIL, "holds 0 copies; expected 2" and "expected 1" |
| `python3 -I tests/hygiene/test_lint.py --quick` | 0 failed, 95 RESULT PASS, including the three new theme-guard results |
| `python3 -I scripts/public_lint.py --theme` | exit 0, 7 files scanned (the five staged skills and two staged notes), 0 findings; before the `theme_scan` change it printed 8 findings, all on lines the installed skills already have |
| `python3 -I scripts/stale_check.py --self-test` / `--new-only` | 1,076 checks, 0 problems; 0 new FAIL, 0 new WARN |
| `python3 -I scripts/public_lint.py --paths` over the guard, `public_lint.py`, `stale_patterns.json`, `skills-staging`, `tests/hygiene/test_lint.py`, `tests/integration`, this status page and the t4 report | exit 0, 17 files, 0 findings |
| `python3 -I scripts/ops_lint.py`; `json.load` of `stale_patterns.json` | PASS, 0 warnings; parses |
| `python3 -I -B tests/integration/run_checks.py --mode quick --only parity.pr4_sentence,docs.staged_skill_update,hygiene.theme_guard,hygiene.public_lint_over_the_diff,hygiene.public_lint_over_the_build_folders,hygiene.stale_check_new_only` into a scratch evidence folder | 6 PASS, 0 FAIL in 26 s. (An earlier run with the staged copies and without the `theme_scan` change: `hygiene.theme_guard` FAIL; and with a staged note that quoted the old pointer: `docs.staged_skill_update` FAIL on "skills-staging/.../CHANGES.md"; both fixed) |
| `bash build/run_all_checks.sh --quick` (foreground, 590 s timeout), last step of the pass, 07:24 to 07:31 UTC | **exit 0, PASS**: Part A 14 PASS of 14; Part B 13 of 13 areas PASS (hygiene 213 PASS, integration 46 PASS and 1 UNVERIFIED, including `parity.pr4_sentence`); 362 s against the 450 s budget; envelopes 1,065 PASS, 6 FAIL, 28 UNVERIFIED, 2 SKIPPED, 1 BLOCKED. The 6 FAIL envelopes are the recorded ones of the status page (WP-07 holds 2, WP-10 holds 4), unchanged; the 28 UNVERIFIED need the maker's Windows PC. Console copy `build/evidence/run_all_checks_quick.txt` |

## UNVERIFIED

- The staged skills were not loaded into an agent to see whether their triggers still fire; the edits touch rule sentences and change-log lines, not descriptions or headings.
- Whether the shelf the maker photographs is inside or outside the mandir (the same open point as t4): "outside the mandir" is now in the skills as the register has it, which allows almost nothing if the shelf is the mandir; O-38 and Q3 will show.
- Whether the thali and the folded cloth, which the hindu-visual-language route list keeps as shelf examples, sit outside the mandir. The register's parenthetical names only the jhari in its cloth, the lamp and the closed doors; the skill's longer list is kept but now sits under the sentence.
- Nothing here needs the maker's Windows PC.

## For the orchestrator

1. **Install the five staged skills, then remove `skills-staging/`.** For each of `pushtimarg-seva-and-pichwai`, `hindu-visual-language`, `ai-photo-to-animation-pipeline`, `mobile-phone-delivery` and `agent-first-production-pipeline`: `diff .claude/skills/<name>/SKILL.md skills-staging/<name>/SKILL.md` (it should show the lines in the table above and no others; if another package has changed the installed copy since, merge by hand), then copy `SKILL.md` over the installed one. Do not install the staged `CHANGES.md`; the installed skill has its own, which `docs.staged_skill_update` reads once the folder is gone. Then `python3 -I scripts/pr4_parity.py` must still print 21 / 21 in 12 files (the skills then read `[installed]`), and `bash build/run_all_checks.sh --quick` is the final check. I simulated the install in an isolated copy outside the repository: the guard printed PASS with the same counts.
2. **Decide on the `public_lint.py` theme-guard change** (section 5). If you would rather not carry it, revert it and install the staged skills before the next quick run; the quick pass is red on `lint.theme_guard` and `hygiene.theme_guard` only while untracked staged copies with keyword lines sit in `skills-staging/`.
3. **Issue 24 (keep or drop "O-58" and "G5 flag" in the sentence)**: the places to move together are now the table in `scripts/pr4_parity.py` (`COPIES`, `SKILLS`, `CLAUSE_EXPECTED`), which fails until all agree. Dropping the parentheticals also touches the six clause-aligned lines in `hindu-visual.md`.
4. **`build/BUILD-STATUS.md` sections 1 and 6 and issue 16 are yours.** I changed only issues 24 and 28. The counts in section 1 are from the earlier run (integration area 46 PASS now with `parity.pr4_sentence`; hygiene 213; envelopes 1,065 / 6 / 28 / 2 / 1; elapsed 362 s); issue 16's last sentence (the dangling `skills-staging` pointer in the installed skill) is closed by the install in item 1, and issue 26's remark that the staged-skill checks come back by themselves when a staged skill is put into the folder now describes what happened: the folder is back, the checks read it, and `docs.staged_skill_update` needs the staged `CHANGES.md` beside the staged `SKILL.md`.
5. **The wider short form stays in six other skills**, as issue 28 item 2 said it may: `agent-first-production-pipeline` 117, `animated-biography-patterns` 143, `cinematic-quality-bar` 119, `craft-apps-visual-refinement` 14, 96, 108, `hindu-life-story-frameworks` 98, 134, `surprise-tribute-operations` 8, 41, 105, 193 (line numbers as of this pass). The guard does not see them (they carry neither the sentence's first words nor its second clause); a note in the next skill pass should bring them to the register's sentence or to W-70 and PR10 alone. The staged `agent-first-production-pipeline` copy still has line 117 in the short form, on purpose (this package's list).
6. **Roadmap and register**: nothing to change for this package. `ROADMAP.md` and `PLAN-ON-A-PAGE.md` already carry the sentence (1 each, counted by the guard).
7. **Shared tree.** Other packages were editing the tree while this pass ran (`spikes/sp1_craft_cli/`, `research/craft-motion-fixtures/`, `scripts/public_lint.config.json`, `playbooks/craft-motion.md`, `build/evidence/wp07/`); the final quick run covers the tree as it stood then. `build/evidence/` was rewritten by that run (`INDEX.md`, `week2_summary.json`, `run_all_checks_quick.txt`, the per-area files); decide at commit time which evidence to keep.
