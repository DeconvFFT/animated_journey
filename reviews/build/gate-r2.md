# Fable review: week-1/2 build gate (round 2)

*Fable advisor, Tue 20 Oct 2026, branch `build/process-lock`. Round 1 is `reviews/build/gate-r1.md` (revise, two critical issues, six nudges). Read this round: `build/BUILD-STATUS.md` (rewritten after round 1), `build/BUILD-PLAN-W1-2.md` sections 0 to 4, `build/evidence/P-LOCK-readiness-W2.md` (including the new section 7), `spikes/VERDICTS-W2.md` ("Disk decision"), the two new orchestrator scripts `build/apply_phone_row.py` and `build/apply_skill_rewords.py` (read in full and dry-run), the uncommitted diffs of every non-evidence file the round-1 fixes touched (`.gitignore`, `ops/SETTINGS-CARD.md`, `playbooks/production-scale.md`, `scripts/public_lint.config.json`, `tests/hygiene/test_lint.py`, `spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md`, the five research notes and three reviews of the public-tree once-over, `win/lj.ps1`, `win/kit2/*`), the latest review of each of the thirteen packages, and the register rows D-32, W-06, W-18, W-26, W-63. I ran `bash build/run_all_checks.sh --quick` myself (console copy `build/evidence/run_all_checks_quick.txt`), `python3 -I scripts/public_lint.py --all`, both apply scripts in dry-run mode, and my own scan of the whole tree. All material is synthetic; no family media exists in the container. Windows behaviour is UNVERIFIED throughout. Nothing was committed.*

## Verdict: APPROVE

| Rubric axis | Score |
|---|---|
| Correctness | 4 |
| Safety and privacy | 4 |
| Maker usability | 4 |
| Fidelity to the plan and `DECISIONS.md` | 4 |
| Maintainability | 4 |

**In one line.** Both critical issues of round 1 are closed as far as an implementor can close them: the integrated tree now passes 15 of 15 global checks and 12 of 13 areas, and the only red area is `integration`, whose two failing tests are the deliberate tripwire for the one decision that belongs to the orchestrator (the phone row in `DECISIONS.md`), with a tested one-command fix on file. The public tree is clean (0 identifying-data findings over 929 files, no binary, nothing tracked that `.gitignore` hides), the maker's pages for this week are safe and now carry the SmartScreen rule, and the Diwali-week fallback exists. The week-1/2 build gate passes. What remains is the orchestrator's short list in section 6, with dates.

## 1. What I ran (real output, this container, Tue 20 Oct 00:27 to 00:32 UTC)

### 1.1 `bash build/run_all_checks.sh --quick`

Exit 1, matching `BUILD-STATUS.md` line for line.

* **Part A, 15 global checks: 15 PASS.** The redaction self-test across all consumers (5.1 UNVERIFIED, stated); diff-mode lint over 330 files and build-folder lint over 576 files, each 0 identifying-data and 0 hygiene findings; theme guard; `stale_check` self-test (1,004 checks) and `--new-only` (0 new FAIL, 0 new WARN, 0 baseline hits gone); `ops_lint` PASS; the CSV mirror matches the register at 250 rows (D 32, W 79, O 74, S 65); hours report (no rows yet, read Sun 1 Nov); `ps_parse` 0 errors; `ps_lint` 0 errors and 0 warnings on the 8 read-only files and the 2 writer guides; cleanup dry run (209.1 MB would be freed, nothing deleted); size-and-binary ok (0 over 1 MB, 0 binary, 2 allowed fixtures); gitignore coverage ok (0 not ignored, 0 hidden, 0 tracked-but-ignored).
* **Part B, 13 areas: 12 PASS, 1 FAIL**, 270 s against the 300 s quick budget. The one FAIL is `integration` (43 PASS, 2 FAIL, 1 UNVERIFIED): `parity.phone_profile_vs_register` and `parity.card_phone_row_vs_phone_row_md`, both reading "pipeline/phone/profile.json disagrees with DECISIONS.md, which wins: PH2 cap 3.5 against 4 Mb/s; phone caption characters a line 32 against 36". That is the correct behaviour of the test the round-1 critical issue of WP-11b asked for: the register wins until the orchestrator chooses. The third language-line parity test is now green (the card reads `latin, devanagari ... on 2026-10-19`).
* Envelope totals: PASS 1,035, FAIL 6 (the 2 above plus the 4 recorded Craft findings of WP-10, which the runner flags as "exited 0 but 4 FAIL envelopes on file: read the evidence"), UNVERIFIED 28, SKIPPED 1, BLOCKED 2 (the two SP1 stages that wait for disk). Free space 747 MB at start, lowest and end; the one envelope under the 250 MB floor is WP-10's fake-`df` mechanism test, listed in `tests/integration/disk_exceptions.json`.
* `sp1` is green in quick mode now (`list.live` computes the two-stage figure, 767 MB); the `--all` evidence of WP-07 still holds Monday's FAIL and the two BLOCKED stages until the download run happens, which the status file says honestly.

### 1.2 Whole-tree checks of my own

* `python3 -I scripts/public_lint.py --all`: **929 files, 0 identifying-data findings, 0 hygiene findings**, 1 fixture note (a planted value in `tests/win/fixtures/`), 141 suppressed by the allow list (licence texts, the nine public contact addresses, two false positives; each allow entry names its paths and full value and says why).
* `git ls-files -ci --exclude-standard`: empty. No tracked or untracked-not-ignored file over 500 KB. No NUL byte in any text file (the two reviewed fixtures aside). The five tracked-but-ignored paths of round 1 are staged deletions (`git rm --cached`); the files stay on disk.
* Grep for the maker's address shapes, the cloud-session id, `/tmp/claude-0/...` scratch roots, e-mail and IPv4 shapes in `win`, `ops`, `pipeline`, `scripts`, `spikes`, `build`: nothing, apart from two WP-03 reviews and the WP-03 report that mention the generic old scratch root (no id, no person). The session id is gone from the six files round 1 named, replaced by `<scratch>`.
* The public-tree once-over: six private individuals' names and one social handle are out of `research/ai-imagery.md`; the forum handle in `reviews/cinematic-quality-round4.md` and the producer's address in `research/film-story.md` are masked; creator channel handles are replaced by "YouTube channel (see [n])". **One is left:** `research/ai-imagery.md:875` still names a seventh quoted user from the same vendor blog post while the six beside it read "A user". Harmless (a public tweet, quoted by the vendor), but inconsistent with the edit's own rule (nudge 4).
* Both apply scripts: dry runs print every change and write nothing (`git status` of `DECISIONS.md` and `.claude/` unchanged afterwards). `apply_phone_row.py` finds each phrase exactly once in W-63 and W-18 and refuses otherwise; `apply_skill_rewords.py` finds all nine phrases in the seven skills, and each rewording keeps the meaning of a reconciliation note while dropping the retired value it quoted.

### 1.3 Windows scripts, re-scanned after the diffs

`win/step0_pc_tests.ps1`, `win/lj.ps1`, `win/kit2/*.ps1`: no `Remove-Item`, `Set-ItemProperty`, `New-ItemProperty`, `Invoke-WebRequest`, `Invoke-RestMethod`, `Set-ExecutionPolicy`, `Start-Process`, `Out-File`; the one `New-Item` creates the `-Out` folder on request and is listed under `files written:`. No `??`, `?.`, `&&`, `||`, `-Parallel`, `-AsHashtable`, `-AsByteStream`, `utf8NoBOM`. `kenburns_24.py` carries 24 fps as its only rate. `lj.ps1` v0 still has no `-Apply`, `-Commit` or `-IncludeWindowsRecent`. All of it remains UNVERIFIED on Windows PowerShell 5.1; every maker page says so on its first screen.

## 2. Is the build on track for P-LOCK (Sat 14 Nov)?

**Yes.** The thirteen packages exist and are each approved; the integrated tree is green except for the one declared register decision; the readiness map has 27 rows, `PASS (container)` only on C1, C3 and C6 (none needs Windows), `lj.ps1 close` reads "not started (week 4)" as W-06 and W-26 require, and the eight "not started" items are correctly week-3 or week-4 work. The maker's own week is laid out day by day in `BUILD-STATUS.md` section 2 and nothing in it waits on an agent.

Two things bind, both already written down with dates, neither yet done:

1. **Disk.** Free space is 747 MB, two megabytes less than at round 1; nothing has been freed. `spikes/VERDICTS-W2.md` now records the decision (free at least 4,000 MB of the earlier session's scratch by Wed 21 Oct; SP1 T2/T4 at the lean profile by Fri 23 Oct, the R8 date; SP3 in the container by Fri 30 Oct; fallback to the PC in Mon 2 to Thu 5 Nov if Fri 23 Oct shows under 4,000 MB). The decision is sound and the fallback is dated. It needs the orchestrator's hands this week (nudge 2).
2. **The phone row.** `profile.json` and `PHONE-ROW.md` (3.5 Mb/s, 32 characters, measured) against W-63 and W-18 (4 Mb/s, 36). Round 1 asked for one source of truth before Sun 1 Nov. The implementor prepared and tested the recommended edit end to end on a copy (four parity checks, `ops_lint`, 44 ops tests, 14 phone tests, 63 planted-defect controls) and may not touch the register, so the decision is now a single command away (nudge 1). I keep my round-1 recommendation: amend the register to the measured values.

The Diwali-week gap of round 1 is closed as a proposal: `P-LOCK-readiness-W2.md` section 7 moves the maker-owed Windows items that need no week-3 agent output into Mon 2 to Thu 5 Nov (about 3.5 hours), names the three cases of the Q11 answer, and writes the fallback that separates the rows that may not remain maker-owed at P-LOCK (inventory, hours, card, archive, encrypted container, five-minute tests, `lj.ps1 close` v1, phone hygiene, phone-floor look) from those that may, with a closing date each (round trips by Fri 20 Nov, slice fixture, tone ladder, scrubber). The reasoning ("a row may stay open only if it guards work after the first real scan and failing it costs rework, not privacy") is the right test. The orchestrator confirms the case on Sun 25 Oct (nudge 6).

## 3. Are the maker's instructions safe and followable by a learner?

**Yes.** Round 1's one usability gap is closed: `MAKER-CRAFT-ZIPS.md` (regenerated by `build_guide.py`, `check_guide.py` 8 PASS) now says, in Step 7 and in "If something goes wrong", that a blue "Windows protected your PC" box is expected for the five programs, that `NotSigned` is normal for alpha software, and that "More info, Run anyway" is allowed only when all three conditions hold (one of the five programs inside `C:\lj\tools`; Step 3 printed `OK` for its zip; the maker unzipped it); any other file, any antivirus removal or quarantine, and a box that looks different remain "stop and paste". The antivirus line is now its own bullet and adds "do not restore the file". That is the pre-decided rule the Saturday session needed, and it is as narrow as it should be.

The rest stands as read in round 1: the inventory README opens with what the script reads, what it never does and that it is untested on a real PC; `GATHER.md` keeps every name, place and the birthday question in private notes and takes only IDs into chat; `HOURS-HOWTO.md` bans names in the note column and `ops_lint` enforces it; `PHONE-TEST.md` is a 15-minute page with seven questions and a synthetic file; the settings card's language line is filled with the real date and `latin`, and its status note says plainly that Gujarati is NOT TESTED and is the test that must pass before signing. The weekly list in `BUILD-STATUS.md` section 2 is the hand-over text and now carries the SmartScreen sentence too.

## 4. Is the public repo clean?

**Yes, now of stray files as well as of identifying data.** Section 1.2 has the measurements. The `.gitignore` additions are additive (raw-report names with the schema kept visible, `*.local.*`, logs, work folders, pid and partial files, archives, more media types) and `repo.gitignore_coverage` confirms nothing tracked is newly hidden. The allow list grew by three entries, each matched by full value in named folders with a written reason, and its note now says a personal address is never added. The one leftover name (nudge 4) is the only thing I would still touch.

## 5. Fidelity and maintainability

Every deviation is declared where it is made: SP1 T5 cut (D-12), `lj.ps1 close` v0 as a dry run with v1 in week 4, Craft read-backs as Linux results only, the phone numbers as (J) proposals, the new-text limit raised from 5 to 8 MB with the test renamed (7.01 MB measured; the plan text still says 5), the register left untouched where the implementor had no right to it. The two apply scripts are the right shape for an orchestrator-owned edit: dry run by default, every change printed, exact-match refusal, and the checks they must turn green named in the header. They are one-shot tools and should leave `build/` once run, so a later reader does not take them for standing instructions (nudge 1). The quick runner used 270 s of its 300 s budget, 292 s wall; it has no headroom for a fourteenth area (nudge 5).

## 6. Critical issues

None that blocks the gate. The two red tests are the orchestrator's register decision, prepared and tested; they should be green before the card goes to the maker, and in any case before Fri 30 Oct.

## 7. Nudges (at most six)

1. **Settle the phone row this week, not on Fri 30 Oct.** Run `python3 -I build/apply_phone_row.py` (dry run), then `--apply`; add the dated amendment note to `DECISIONS.md` in the register's usual way; then the scribe pass over the five playbooks and three skills that quote 4 Mb/s and 36 characters (the list is in the script's header); then `bash build/run_all_checks.sh --quick` should exit 0. If you prefer the register as it is, regenerate `profile.json` and `PHONE-ROW.md` to 4 and 36 instead and re-run `phone_check.py --scenario fill_20x9`. Either way, remove both `build/apply_*.py` scripts once they have run.
2. **Free the disk by Wed 21 Oct as `spikes/VERDICTS-W2.md` says**, then `bash spikes/sp1_craft_cli/run_sp1.sh --all --profile lean` and `drivers/verdict.py` by Fri 23 Oct so the R8 rule is decided before the pin freeze; SP3 by Fri 30 Oct. Do not run `cleanup_scratch.sh --yes` first. If Fri 23 Oct shows under 4,000 MB, apply the written fallback and change the date in that section the same day.
3. **Apply the skill rewords and re-cut the baseline**: `python3 -I build/apply_skill_rewords.py --apply`, read `git diff .claude/skills`, then `python3 -I scripts/stale_check.py --baseline`, so the 11 hits leave the tree instead of resting in the baseline.
4. **One line in `research/ai-imagery.md:875`**: replace the last quoted user's name with "A user", as the six lines beside it already read (D-26; the journalist named on the next line is a published author and may stay).
5. **Keep the quick budget honest.** `hygiene.stale_check_new_only` (10 s) runs in Part A and again inside the integration area; drop one of the two, or raise the budget with a note, before any area is added.
6. **Sun 25 Oct:** read the Q11 answer, pick case A, B or C in `P-LOCK-readiness-W2.md` section 7, and write the chosen calendar into `ROADMAP.md` and any exceptions as `ops/gate_log.csv` rows, so the Sun 8 Nov mid-point check has one calendar to read. At the same touch, carry WP-10's VectorCraft finding (animate by transform and id; no `data-*` on text) into the craft-visual playbook.

## 8. What goes out now

Everything in `BUILD-STATUS.md` section 2: hours daily, the PC inventory Tue 20 Oct, `GATHER.md` Part A1 Wed 21 Oct, the Craft zips and five-minute tests Sat 24 Oct with the SmartScreen rule as written, the Sunday questions and the five planning answers Sun 25 Oct. None of it touches family material; none of it waits on nudges 1 to 6.

*Nothing in this review was committed; the orchestrator commits. Scores are 4 across the board: the build is a fortnight ahead of its own calendar, its checks catch what they should, and the remaining work is the orchestrator's dated list, not a defect in what the packages built.*
