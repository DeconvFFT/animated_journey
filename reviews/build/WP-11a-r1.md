# Fable review: WP-11a round 1 (check-runner skeleton, INDEX.md writer, scratch cleanup)

Reviewed Mon 19 Oct 2026 on branch `build/process-lock`. Refs W-06, W-26, W-29, D-26, D-30; build plan section WP-11a and 4.2, 4.3, 4.9.
Read: `build/reports/WP-11a.md`, `scripts/run_week2_checks.sh`, `scripts/cleanup_scratch.sh`, everything under `tests/runner/`, `build/evidence/INDEX.md`, `wave1_quick.txt`, `week2_summary.json`, `build/evidence/wp11a/*`.

**Verdict: approve** (correctness 4, safety/privacy 4, maker usability 4, fidelity 5, maintainability 4). No critical issue. Four nudges below are for round 2 or WP-11b; none blocks the Fri 23 Oct bundle.

## 1. What I re-ran (real output, this container)

| # | Command | Result |
|---|---|---|
| 1 | `bash tests/runner/run_tests.sh --all` | PASS: `SUMMARY mode=all failures=0`, 127 envelopes, 40 s |
| 2 | `bash scripts/run_week2_checks.sh --list` | PASS: 13 areas in the fixed order, `Landed: 8 of 13`, exit 0, wrote nothing |
| 3 | `bash scripts/run_week2_checks.sh --quick` (real tree) | mechanism PASS, exit 1: `Areas: 13 \| landed 8 \| PASS 6 \| FAIL 2 \| TIMEOUT 0 \| NOT LANDED 5`, 148 s of the 300 s budget; `INDEX.md`, `week2_summary.json`, `wave1_quick.txt` rewritten. The two FAILs are `ops` (WP-02: `decisions.csv` behind `DECISIONS.md`, D-31 missing) and `roundtrip` (WP-06: a `__pycache__` under `tests/roundtrip`). Both are other packages' findings, as the report says. |
| 3b | a second real `--quick` started while the first ran | `BUSY: another run_week2_checks.sh is already running for this evidence folder; nothing was run`, exit 3 (lock works on the real tree) |
| 4 | `bash scripts/cleanup_scratch.sh` (dry run, real tree) | lists pwsh 184.9 MB, venv-otio 15.6 MB, `vendor/craft`, `renders/wp01a`, `renders/wp04`; hash of exactly those items `ea3f67ea1e108385` before and after; exit 0 |
| 5 | `public_lint.py --paths` on every owned path plus the three regenerated outputs | 40 files, 0 findings, exit 0 |

## 2. Tests of my own, designed to break it

**A. Runner redaction with awkward input** (fake area, test hooks only): an e-mail-shaped string with a colour escape in the middle, one with a NUL inside, one with a zero-width space inside, a Windows profile path, and a `(at)` spelling. Result: ANSI and NUL cases masked (`zz********`), the profile path masked (`C:********\Desktop\x.txt`), the zero-width-space case masked from the point the scanner recognised it (`zz.<zwsp>sp********`, five characters kept instead of two, but the address is gone), the `(at)` spelling untouched (not an e-mail shape; correct by the pattern file, and the masker is a net, not a licence, as the report says). No raw address in any stored file.

**B. Evidence subfolder `..` through `LJ_RUNNER_AREAS_FILE`.** The area-line check allows `..` as an evidence subfolder, so the index reads envelopes from the parent of the evidence folder and `INDEX.md` links `[../](../)`. Only reachable through a test hook that also forces a separate evidence dir, so it is a hardening nudge, not a defect (nudge 3).

**C. `cleanup_scratch.sh --root` pointed at the home folder.** With `HOME` set to a fake home and `--root` set to that same folder (scratch elsewhere), `--yes` deleted `<home>/vendor/craft-precious` and `<home>/renders/wp-thesis`. The script vets the scratch folder thoroughly (`/`, `$HOME`, parents, depth, name, links) but does not vet `--root` at all beyond "exists". The default root (the repo this script sits in) is safe, and the plan's acceptance tests pass, but the written promise "refuses to touch anything outside `<scratch>`, `vendor/` and `renders/`" should hold for any root given (nudge 1).

**D. Usability of a FAIL in `wave1_quick.txt`.** The console excerpt for a failing area is the last 12 non-blank lines. For `ops` those 12 lines are nine `PASS` lines, one `UNVERIFIED` and the summary; the seven failing test names appear only in `build/evidence/wp11a/area_ops_quick.txt`. The reader of the Fri 23 Oct bundle has to open a second file to learn what failed (nudge 2).

## 3. Scores

- **Correctness 4.** Everything in the plan's acceptance list holds and is tested, including process-group kill, stray-process kill, fail-closed redaction, the lock, abort-removes-stale-outputs and rerun stability. Items B and C above are the reasons it is not a 5.
- **Safety and privacy 4.** Redaction by design: no regex of its own, scanner proven live before anything runs, exit 2 without running when it cannot be, three finished texts masked twice, planted strings never stored or printed (verified with my own split-string cases). No family media, nothing that could tip off the mother, no names, hosts or user paths in any owned file. Not a Windows script; marked UNVERIFIED correctly. The `--root` gap (C) costs the point.
- **Maker usability 4.** Commands are exact, the `--list` and `--quick` output read well, exit codes are explained in the usage line, `cleanup_scratch.sh` is dry-run by default and prints sizes and `df`. The FAIL excerpt (D) is the weak spot.
- **Fidelity to plan 5.** Fixed order, result words, exit codes (4.3), envelope reading (4.2), the lowest `avail_mb_min` column, `wave1_quick.txt` only for `--quick`, the `public_lint --text` hook with an explicit fail-closed assumption. Every deviation is listed with its reason in section 5 of the report, and none changes a planned behaviour.
- **Maintainability 4.** One 675-line bash file with embedded stdlib Python is dense but well sectioned and commented; the tests (127) use fake areas and never touch the real `INDEX.md`; `tests/runner/README.md` explains the fakes. Tests reuse `public_lint.py` and `lj_guard.sh`'s `LJ_DF_CMD` convention rather than re-implementing them.

## 4. Nudges (non-blocking; apply in round 2 or hand to WP-11b)

1. `scripts/cleanup_scratch.sh`, after line 71 (`refuse "the repo root does not exist"`): vet `R_REAL` too. Refuse when it is `/`, equals or contains `$H_REAL`, or does not hold `CLAUDE.md` and `.git` (so `--root` can only ever name a checkout of this repo). Add one test to `tests/runner/test_cleanup.sh` GROUP refusals: `--root "$D/home"` with a scratch elsewhere must exit 2 and change nothing.
2. `scripts/run_week2_checks.sh` line 621 (the non-PASS excerpt): show up to 12 lines matching `FAIL|BLOCKED|TIMEOUT|REFUSED|Error` from `$masked.body` first, then the last 3 lines, so `wave1_quick.txt` names the failing tests. Keep the 170-character cut. Update test `console_fail_row` or add one asserting the fake failing test name `deliberate failure` appears in `wave1_quick.txt`.
3. `scripts/run_week2_checks.sh` line 467: tighten the evidence-subfolder check to `^[A-Za-z0-9][A-Za-z0-9._-]*$` and reject `.` and `..` explicitly, so a hook-driven areas file can never index or link outside the evidence folder.
4. `INDEX.md` Owner column (line 307 of the runner, `"sonnet-implementor (tests/%s/)"`): the same text in all 13 rows carries no information. Either drop the column (the Entry column already names the package) or take the owner from the area table so WP-11b can mark its own rows and Windows-run rows ("maker's PC, UNVERIFIED").

## 5. Notes for the orchestrator (not WP-11a's to fix)

- The real `--quick` exits 1 until WP-02 regenerates `ops/decisions.csv` (D-31) and WP-06 removes `tests/roundtrip/__pycache__`. Rerun `--quick` after those land so the Fri 23 Oct bundle shows the true state.
- Running `--quick` makes every landed area rewrite its own evidence files: 74 files under `build/evidence/` show as modified after my run. Expected, but commit them deliberately.
- `build/evidence/wp11a/area_ops_quick.txt` carries the string `she is from Bhavnagar, Gujarat, D-31`, quoted by WP-02's lint from `DECISIONS.md` O-02. It is already public in `DECISIONS.md` by the orchestrator's own choice, and the pattern file has no place-name category, so the runner could not have caught it. A home town is a quasi-identifier in a public repo (D-26); worth a conscious decision rather than an accident of logging.
- `public_lint.py --text` still does not exist. Tell WP-03 the contract the runner assumes (text on stdin, exit 0 = clean) or tell WP-11a the real one; the runner fails closed (exit 2, `WITHHELD`) if the command line differs.
