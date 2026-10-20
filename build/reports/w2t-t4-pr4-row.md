# Package t4-pr4-row: PR4 in the playbooks, brought to the register's sentence

Sonnet implementor, Tue 2026-10-20, branch `build/process-lock`. Synthetic material only. Nothing committed or pushed. No binaries. `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and `.claude/` were not touched.

## The sentence

PR4, the seva-article rule, copied byte for byte from `DECISIONS.md` (the Codes block; W-61 and W-70 read the same, checked by a script: 3 exact occurrences in `DECISIONS.md`, and the same 3 in `QUESTIONS-SUN-25-OCT.md`, 1 in `ROADMAP.md`, 1 in `PLAN-ON-A-PAGE.md`):

> her Thakorji, chitraji, any picture of hers and anything inside the mandir are never photographed without her knowing; a seva article outside the mandir (the jhari in its cloth, the lamp, the closed doors) may be photographed by sight, untouched, on an unsynced phone (O-58), each logged as a G5 flag (O-48)

The Codes block adds a trailing cross-reference "(touching or handling any seva article without her knowing is PR10/PR14, W-70)"; that is a pointer, not part of the sentence (W-61 and W-70 omit it), so it was not copied. PR10 and PR14 stay cited where they already were.

## What changed (4 playbooks, 24 insertions, 19 deletions)

### `playbooks/pushtimarg-world.md` (the package's named target; the sentence now occurs 4 times)
- Line 158, T2 rule row **PR4**: now `**The seva-article rule:**` followed by the register's sentence, then the old note "Any picture may be pusht". Check column unchanged (`maker`). Basis keeps `[2] Seva Q35; [16] Q81; D-02; D-17` and gains `Codes (PR4)` as a pointer to the verbatim copy.
- Line 371, Reverence norms, "The home Thakorji's privacy": the last sentence "Photographing her Thakorji without her knowing is out (PR4; D-02; D-17)" is now "PR4 (D-02; D-17), as the register states it:" plus the sentence.
- Line 412, Q4 note: "Nothing in the seva space, and no picture or pichwai of hers, is photographed without her knowing (PR4; D-02; D-17); the default is none" is now the sentence under the same citations; "the default is none" and the G5-flag line for a wall or room photograph are kept.
- Line 443, Pitfall 14: lead now "A photograph of her Thakorji, her pictures or anything inside the mandir without her knowing"; the body carries the sentence; PR4, D-02, D-17 and the Q4 pointer kept.
- Line 575, Changelog: one line added.

### `playbooks/hindu-visual.md` (the rule is welded to this playbook's own examples, so only Step 6 carries the sentence verbatim; the other restatements carry the same three elements in the playbook's own words)
- Line 56, Step 6 route (3): the register's sentence verbatim, after the playbook's own object list; `W-70`, `research/pushtimarg-world.md PR4, F6` and the "pusht" reason kept.
- Clause-aligned (adds "anything inside the mandir" to the prohibited set; where the same sentence allows shelf photographs it adds "outside the mandir" and "each logged as a G5 flag (O-48)"; "Lalan" and the example lists are kept): lines 36 (principle 8), 82 (exercise steps), 219 (R17), 303 (rights table), 370 (checklist), 507 (Privacy).
- Prohibition-only restatements, "anything inside the mandir" added: lines 43 (Step 1), 51 (Step 5), 84 ("What good looks like"), 178 (H3 how-to-use), 240 (YAML comment).
- Line 434, Decision options P3: "never without her knowing" replaced by "anything inside the mandir is never photographed without her knowing"; "of seva objects outside the mandir now"; the O-64 and April-version condition for a svarupa or a picture of hers is unchanged.
- Line 671, Changelog: one line added at the top (this file's changelog runs newest first).

### `playbooks/ai-imagery.md`
- Line 207, Deities paragraph: "nothing of the Thakorji, Lalan, chitraji or any picture of hers is photographed without her knowing" replaced by "PR4, as the register states it:" plus the sentence; "(PR3, PR4 in `playbooks/pushtimarg-world.md`)" kept.
- Line 589, Changelog: one line added.

### `playbooks/mobile-delivery.md`
- Line 322, surfaces table, "Her own deities ... on a phone surface": "so nothing in seva is photographed without her knowing (PR4, W-61)" replaced by "so, as the register states PR4 (W-61)," plus the sentence; the "pusht" reason, UNVERIFIED note and O-64 text kept.
- Line 494, Changelog: one line added.

### Reviewed and left as they were (a citation of PR4 for a different claim, or a different rule)
`playbooks/pushtimarg-world.md` 366 (what goes on screen, PR2/PR4) and 449 (Pitfall 20, "the temple or her picture", T6; PR4); `hindu-frameworks.md` 182, 184, 187, 249, 301, 332, 348; `craft-visual.md` 5, 32, 401, 484 and `craft-motion.md` 35 (scan and file handling); `cinematic-quality.md` 680 ("staged"); `surprise-ops.md` 5, 124, 605, 870 (borrow, touch and move rules that go beyond PR4, cited to PR4, PR10, W-70); `film-story.md` 465 and `games.md` 181 (no PR4 sentence); `saurashtra-world.md` 398 and 420 (the O-48 and O-58 questions); `hindu-visual.md` 498 (copyright note) and the dated history in its changelog (677).

## Commands and results

| Command | Result |
|---|---|
| script: exact register sentence in `DECISIONS.md` | 3 occurrences; same sentence confirmed in the Sunday sheet, `ROADMAP.md`, `PLAN-ON-A-PAGE.md` |
| script: exact sentence per playbook after the edits | `pushtimarg-world.md` 4, `hindu-visual.md` 1, `ai-imagery.md` 1, `mobile-delivery.md` 1 |
| script: every playbook line with "chitraji" or "picture(s) of hers" lacking "inside the mandir" | none left except non-rule uses (kinds of svarupa, sources, the dated changelog entry at `hindu-visual.md` 677, and the borrow rule at `surprise-ops.md` 124 which names "the home mandir and its cloth") |
| `python3 -I scripts/public_lint.py` (diff mode) | exit 0, 130 files, 0 findings |
| `python3 -I scripts/public_lint.py --paths playbooks` | exit 0, 23 files, 0 findings (12 suppressed by the existing allow list) |
| `python3 -I scripts/public_lint.py --theme` | exit 0, 4 files scanned (the four changed playbooks), 0 findings |
| `python3 -I scripts/stale_check.py --new-only` | exit 0, 0 new FAIL, 0 new WARN |
| `python3 -I scripts/ops_lint.py` | PASS, 0 warnings |
| `bash build/run_all_checks.sh --quick` (foreground, 580 s timeout), real tree | **exit 1, FAIL**: 317 s of the 450 s budget; Part A 13 PASS and 1 FAIL; Part B 12 of 13 areas PASS and `integration` FAIL (38 PASS, 3 FAIL, 1 UNVERIFIED) |
| same command in an isolated copy of the working tree (outside the repo, in the `<session scratchpad>`), with `skills-staging/` restored from the installed skills and the PowerShell 7 folder copied across | **exit 0, PASS**: Part A 14 of 14, Part B 13 of 13 areas, 330 s. The copy was deleted afterwards |

### Why the real-tree quick run is red (not caused by this package)

All four red items name a folder that is not in this checkout, `skills-staging/`:
- `lint.build_folders`: exit 2, "USAGE: a path given to --paths does not exist" (`build/run_all_checks.sh` line 93 still lists `skills-staging`).
- `integration` `hygiene.public_lint_over_the_build_folders`: the same usage error.
- `integration` `hygiene.theme_guard`: its default scope (which scans the four changed playbooks) and its explicit scope both exit 0 with 0 findings; only the third leg, which scans `skills-staging/`, fails.
- `integration` `docs.staged_skill_update`: "paths that do not exist: skills-staging/agent-first-production-pipeline/CHANGES.md".

`git log` shows the cause: `f474039` deleted the staged `agent-first-production-pipeline` files and `04a5504` deleted `skills-staging/mobile-phone-delivery/SKILL.md` when the three staged skills were installed under `.claude/skills/`; `build/run_all_checks.sh` and `tests/integration/run_checks.py` (`BUILD_ROOTS`, `staged_skill_changes`, `docs.staged_skill_update`) still expect the folder. The week-2 gate's green quick run (committed evidence, 14 of 14 and 13 of 13) pre-dates that install. The isolated run is the evidence that the playbook edits themselves keep every check green. A first isolated attempt (before PowerShell was copied in, and with a third synthetic staged copy) showed two further reds that were artefacts of the experiment (no PowerShell in the copy; the theme guard reading the D-28 exclusion-statement line at `mobile-phone-delivery/SKILL.md` line 129 as new text in an untracked copy); the second attempt removed both and passed.

The runner always rewrites `build/evidence/` (`INDEX.md`, `week2_summary.json`, `run_all_checks_quick.txt`, `wave1_quick.txt`, `wp11a/area_*_quick.txt` and the per-package JSON). Those tracked files were already modified before this package (earlier runs); the run for this package left them recording the red state above.

## UNVERIFIED

- Whether the shelf photographed under `hindu-visual.md` principle 8 and Step 6 is inside or outside the home mandir in her house. I added "outside the mandir" to those clauses because the register's permission is limited to articles outside it. If the shelf is the mandir, those clauses allow almost nothing, which is what PR4 says; O-38 and Q3 will show.
- Whether the thali and the folded cloth, which `hindu-visual.md` lists as shelf examples, sit outside the mandir. The register's parenthetical names only the jhari in its cloth, the lamp and the closed doors; I kept the playbook's longer example list and made it conditional on "outside the mandir" rather than removing it.
- Nothing in this package needs the maker's Windows PC.

## For the orchestrator

1. **Quick check is red on this checkout; decide the fix.** The two places to change are `build/run_all_checks.sh` (the `lint.build_folders` path list, line 93) and `tests/integration/run_checks.py` (`BUILD_ROOTS` line 55; the third leg of `hygiene.theme_guard`; `docs.staged_skill_update`, around lines 1458 to 1640). Either drop `skills-staging` from both and retire the staged-skill checks, or have them skip when the folder is absent. `tests/integration/run_checks.py` already carries uncommitted edits from another package, so I did not touch it. After the fix, re-run `bash build/run_all_checks.sh --quick`; the isolated run says it will be green.
2. **Installed skills still carry the short form** (I may not edit `.claude/`): `.claude/skills/hindu-visual-language/SKILL.md` lines 39, 40, 95 (same wording as the old playbook lines, with "Lalan"); `.claude/skills/ai-photo-to-animation-pipeline/SKILL.md` lines 54 and 120; `.claude/skills/pushtimarg-seva-and-pichwai/SKILL.md` line 98; `.claude/skills/mobile-phone-delivery/SKILL.md` line 130 ("nothing in her seva space is photographed without her knowing"). Broader "nothing in seva is photographed ... (PR4)" lines, which may be intended as stricter, are in `agent-first-production-pipeline` 117, `animated-biography-patterns` 143, `cinematic-quality-bar` 119, `craft-apps-visual-refinement` 14, 96, 108, `hindu-life-story-frameworks` 98, 134 and `surprise-tribute-operations` 8, 41, 105, 193. Suggested wording for the four named files: the sentence in the "Sentence" section above, as in `playbooks/pushtimarg-world.md` T2.
3. **`scripts/stale_patterns.json` lines 659 and 2160** (S-60 and S-61) give "nothing in seva is photographed without her knowing (PR4)" as the canonical wording in their finding text. It is not matched as a stale pattern, but it is the older short form; the register's S-60 row now says "PR4 the seva-article rule as the Codes state it". Out of this package; I did not edit it.
4. **`build/BUILD-STATUS.md` row 18** still lists "the PR4 row of `playbooks/pushtimarg-world.md` line 158 (still the short form)". That item is done; the row is yours to update. Row 24 (the "O-58" and "G5 flag" parentheticals inside the sentence): if you drop them from the register's sentence, the copies to change together are `DECISIONS.md` (3), the Sunday sheet (3), `ROADMAP.md` (1), `PLAN-ON-A-PAGE.md` (1) and now the playbooks (7: `pushtimarg-world.md` 4, `hindu-visual.md` 1, `ai-imagery.md` 1, `mobile-delivery.md` 1). The medium-form lines in `hindu-visual.md` mention "each logged as a G5 flag (O-48)" and would need the same edit.
5. **Research notes keep the short form on purpose** (`research/*.md` is a historical record, W-29): `research/pushtimarg-world.md` 282 and 567, and `research/hindu-visual.md` (many lines). No change made.
6. Not done, by scope: `hindu-visual.md` principle 8 and the exercise lines could carry the sentence verbatim too; I kept them clause-aligned so the playbook's own examples and "Lalan" stay. Say so if you want them byte-identical.
