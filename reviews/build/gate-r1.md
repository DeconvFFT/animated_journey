# Fable review: week-1/2 build gate (round 1)

*Fable advisor, Mon 19 Oct 2026 (late evening), branch `build/process-lock`. Read: `build/BUILD-STATUS.md`, `build/BUILD-PLAN-W1-2.md` (sections 0, 2, 4.12, 4.14, 6, 8, 10), `build/evidence/P-LOCK-readiness-W2.md`, the thirteen latest package reviews in `reviews/build/`, the maker-facing pages (`win/README-MAKER.md`, `ops/HOURS-HOWTO.md`, `ops/GATHER.md`, `ops/SETTINGS-CARD.md`, `spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md`, `win/kit2/README-KIT2.md`, `pipeline/phone/PHONE-TEST.md`, `QUESTIONS-SUN-25-OCT.md`), the uncommitted diffs of `.gitignore` and `tests/hygiene/test_lint.py`, and `DECISIONS.md` rows D-26, D-27, D-28, D-30, D-32, W-06, W-18, W-26, W-29, W-63. I ran `bash build/run_all_checks.sh` (full mode) myself; its console copy is `build/evidence/run_all_checks_all.txt`. I also ran my own hygiene scan of the tree (tracked-but-ignored paths, NUL bytes, files over 500 KB, e-mail, IPv4, UUID, session-id and home-folder shapes). All material is synthetic; no family media exists in the container. Windows behaviour is UNVERIFIED throughout.*

## Verdict: REVISE

| Rubric axis | Score |
|---|---|
| Correctness | 4 |
| Safety and privacy | 4 |
| Maker usability | 4 |
| Fidelity to the plan and `DECISIONS.md` | 4 |
| Maintainability | 4 |

**In one line.** The build is ahead of its own calendar (all thirteen packages landed and were approved on day 1 against a plan that spread them to Fri 30 Oct), every maker-facing page is safe to hand over this week, and the build folders are clean; but the integrated tree does not pass its own runner (exit 1), and the plan's definition of done (4.12, item 1) says a package is done when its tests pass. Every failure is a small, named debt of the orchestrator or of one owner, and I verified the main one is a single command away. Fix the list in nudge 1, re-run `--quick`, and this gate goes to round 2 for a short read. **The revise does not hold up the maker:** the Tue 20 Oct inventory, the hours page and the Sat 24 Oct Craft guide may go out now (section 3).

## 1. What I ran (real output, this container)

### 1.1 Part A, the fifteen global checks

9 PASS, 6 FAIL, matching `BUILD-STATUS.md` exactly. The six failures and their causes:

| Check | Cause (issue number in `BUILD-STATUS.md` section 4) |
|---|---|
| `lint.diff_mode` | 9 hygiene findings: five tracked-but-ignored paths (four `__pycache__/*.pyc`, `srv.pid`), four NUL-byte binaries (the same `.pyc`); **0 identifying-data findings** (issue 4) |
| `stale.new_only` | 15 new FAIL and 2 WARN: 11 in installed skills under `.claude/`, 2 in `playbooks/production-scale.md`, 4 in `scripts/` where WP-02's comments use the invented example IDs `O-95`, `O-96` (issue 3) |
| `ops.lint`, `ops.decisions_mirror` | `ops/decisions.csv` lacks D-32 (issue 1) |
| `repo.size_and_binary` | the four `.pyc` (issue 4); nothing over 1 MB; the two reviewed fixtures (`.ora`, `.blend`) are allowed by name |
| `repo.gitignore_coverage` | the five tracked-but-ignored paths (issue 4) |

Passing: the redaction self-test across all consumers including PowerShell 7 (5.1 UNVERIFIED, stated in the output), `public_lint --paths` over the build folders (571 files, 0 findings), the theme guard, the stale self-test (1,004 checks), the hours report (header only, as expected before the maker types), `ps_parse` (0 errors), `ps_lint` on the read-only scripts and on the two writer guides (0 errors, 0 warnings), and the cleanup dry run (208.8 MB would be freed; nothing deleted).

**Issue 1 verified as a one-liner.** I copied `ops/decisions.csv` to scratch, ran `decisions_to_csv.py --write` on the copy and then `--check`: 250 rows, `OK: matches the register`, and the only difference from the committed file is the one added D-32 row. Nothing else in the mirror moves.

### 1.2 Part B, the thirteen package areas (`run_week2_checks.sh --all`)

**Status of my run at the time of writing (23:46Z):** Part A had finished and Part B was in progress (the `hygiene`, `win`, `ops`, `validators` and `render` areas had written fresh evidence; the full pass takes about 38 minutes). The runner writes its console copy to `build/evidence/run_all_checks_all.txt` and refreshes `build/evidence/INDEX.md` and `week2_summary.json` when it ends; round 2 reads those. The Part B figures below are therefore the integration implementor's run as recorded in `build/BUILD-STATUS.md` section 1, which I cross-checked against the thirteen package reviews and the readiness map rather than re-measured:

| Area | PASS / FAIL / UNV | Why red, where red |
|---|---|---|
| hygiene (WP-03), win (WP-01a), win_lj (WP-01b), validators (WP-05), render (WP-04), roundtrip (WP-06), phone (WP-08), win_kit2 (WP-09), spikes (WP-10), runner (WP-11a) | all green: 213/0/1, 95/0/1, 143/0/10, 72/0/3, 27/0/0 (1 skipped), 109/0/2, 32/0/1, 162/0/7, 59/0/1, 127/0/0 | - |
| ops (WP-02) | 40 / 6 / 1 | issue 1 only (the CSV mirror lacks D-32; five tests compare the mirror with the register) |
| sp1 (WP-07) | 47 / 1 / 1 (2 blocked) | issue 6 and 12: `list.live` expects exit 0 at 750 MB free while the two-stage plan needs about 770; T2/T4 never ran for real |
| integration (WP-11b) | 36 / 9 / 1 | red on purpose: it finds issues 1 to 5 |

Envelope totals as recorded: PASS 1,169, FAIL 20 (16 are the issues above, 4 are recorded Craft findings), UNVERIFIED 29, BLOCKED 2. The Part A half of my run reproduced the recorded state line for line, so I have no reason to expect Part B to differ except where the shared volume's free space (749 MB at my start, against about 760 for the recorded run) moves the `sp1` `list.live` result.

### 1.3 My own hygiene scan of the whole tree (not only the build folders)

* **Binaries and stray files tracked:** exactly the five paths the runner names (`.claude/skills/free-creative-toolchain/recipes/__pycache__/r2_param.cpython-313.pyc`, `research/sources/__pycache__/check_mojang_quotes.cpython-313.pyc`, two under `research/toolchain-fixtures/__pycache__/`, and `srv.pid`, a file holding one process number). No tracked file over 500 KB. Nothing else has a NUL byte. The four renders over 1 MB sit under git-ignored `renders/`.
* **Identifying-data shapes outside the build:** the e-mail-shaped hits are public vendor, museum, mailing-list and rights-office addresses quoted in Learn-phase research and playbooks, plus `*.example`/`*.invalid` test strings; none is a person's private address. The IPv4-shaped hits are software version numbers. The UUID-shaped hits are public URLs (IDFA, Microsoft support, a KCL repository), with **one exception: a cloud-session id inside scratch paths** in `research/craft-motion.md:657`, `research/production-scale-fixtures/followup1-classroom-cpu-timing.py:11` and `followup2-s3-run-sweep.sh:2,4` (BUILD-STATUS issue 7 names these and two reviews). It is not family data, but it links a public file to a private session and has no reason to be there. No user name, host name, serial or home-folder path appears outside test fixtures and `/home/user`-style placeholders in test code.
* **Build folders:** 0 identifying-data findings over 571 files (confirmed by the runner and by my own grep for the repo owner's handle and the maker's address shapes: nothing).

## 2. Is the build on track for P-LOCK (Sat 14 Nov)?

**Yes, with two constraints the orchestrator must settle this week.**

What is ahead: the plan's wave 3 was due Fri 30 Oct; all thirteen packages exist, each with a Fable approval on record, a `run_tests.sh --quick/--all`, evidence envelopes with `df` figures, and a readiness map whose statuses obey the rule "nothing that needs Windows reads PASS" (I checked the eight M rows and the nineteen C rows: no Windows row reads PASS, `lj.ps1 close` reads "not started (week 4)" as W-06/W-26 require). The container halves of M3, M5, M6, M8, C1, C3 and C6 are proven. The eight open P-LOCK items that are "not started" are correctly placed in weeks 3-4 (`lj.ps1 close` v1, the three W-31 skills, the MO8 scribe pass, the manifest schema, the cue map, the scrubber page, SP3, SP4).

What binds:

1. **Disk, not people, is the week-3 critical path.** The shared volume shows 252 GB with 749 MB free (99% used) and it fell by about 5 MB during my run. SP1 T2/T4 (R8: may agents render with the Craft CLIs?) need about 770 MB for the lean profile; SP3 (Blender hero shot) needs 3.5 GB. Neither can start until something frees space or the spike moves to the PC. `cleanup_scratch.sh --yes` frees 209 MB but removes the PowerShell and OTIO venv that every `win*` area and the self-test's PowerShell consumers need (WP-11b r2 nudge 3). This is a decision, not a chore.
2. **Week 4 is her Diwali week.** `QUESTIONS-SUN-25-OCT.md` Q8 and Q11 place Dhanteras to Bhai Beej on Fri 6 to Wed 11 Nov, and Q11 asks what that week can hold. The readiness map puts the maker-owed Windows round trips on Mon 9 to Fri 13 Nov and the encrypted-drive and phone tests in the same week, right before P-LOCK on Sat 14 Nov. If the maker's honest answer to Q11 is "little", the maker-owed subset of P-LOCK slips and the plan has no fallback written for it.

Also open before Sun 1 Nov, and not a chore either: `pipeline/phone/profile.json` and `PHONE-ROW.md` hold PH2 at 3.5 Mb/s and 32 characters a line (WP-08's measurement, which fits the 90% box in both scripts); `DECISIONS.md` W-63 and W-18 say 4 Mb/s and 36. WP-11b correctly makes the register win, so the card cannot take the measured row until the register is amended or the profile regenerated. The card's language line still reads `<date>` and lacks `latin`.

## 3. Are the maker's instructions safe and followable by a learner?

**Yes.** I read every maker-facing page end to end as the maker would, and checked the scripts behind them.

* **Read-only where they say so.** `win/step0_pc_tests.ps1` and `win/lj.ps1` contain no `Set-ItemProperty`, `New-ItemProperty`, `Remove-Item`, `Invoke-WebRequest`, `Set-ExecutionPolicy`, `Out-File` or `Start-Process`; the one `New-Item` in the inventory creates the output folder only when the maker passes `-Out` to a folder that does not exist, and it is listed under `files written:`. The writer guides (`MAKER-CRAFT-ZIPS.md`, `README-KIT2.md`) mark every box that writes ("this one writes") and name the folder (`C:\lj\...`, `%TEMP%`, `renders\`). `ps_lint` passes the read-only set with 0 errors and the writer set under `--allow-write`.
* **No PowerShell-7-only syntax** (`??`, ternary, `&&`/`||`, `-AdditionalChildPath`, `-Parallel`) in any `win/*.ps1` or `win/kit2/*.ps1`; `-Depth`, `Get-FileHash`, `Expand-Archive` and `[ordered]` are Windows PowerShell 5.x features. Still UNVERIFIED on a real 5.1, and every page says so in its first screen.
* **Secrecy and privacy by design.** The inventory refuses to write when its own report matches the pattern file or the live user and computer name; the maker is told to paste into chat only, never into the repo, e-mail or a synced note, and why (a hardware fingerprint of one machine in a public repo). `GATHER.md` and the Sunday questions put every name, place and the birthday question in offline notes and take only IDs and yes/no into chat; they repeat D-02, D-13, D-15, D-17 in one line each. `HOURS-HOWTO.md` bans names in the note column and `ops_lint` enforces it.
* **Plain, dated, one page each.** Every page opens with what it is, what it never does, how long it takes, and "if unclear, stop and ask; a pause costs nothing". The weekly list in `BUILD-STATUS.md` section 2 is the right hand-over text.
* **One usability gap worth closing before Saturday.** `MAKER-CRAFT-ZIPS.md` tells the maker to stop at any "Windows protected your PC" dialog. Five unsigned alpha portable executables will almost certainly raise SmartScreen on first launch, so the Saturday session would stop at the first app and wait for chat. The guide already prints `Valid`/`NotSigned` per program and checks the SHA-256 against the release list, which is the information needed for a pre-decided rule (nudge 4).
* **Minor.** `README-MAKER.md` says "notepad `$env:TEMP\lj_pc_report.json`" and `README-KIT2.md` installs Python and ffmpeg through winget ids read on 2026-10-18 and marked UNVERIFIED; both are fine as written. `MAKER-CRAFT-ZIPS.md` Step 7 points into playbooks that still name `C:\Program Files` and `C:\LifeJourney\tools` paths and tells the maker to substitute; acceptable until the Table 4 patch (plan C-04) lands.

## 4. Is the public repo clean?

**Clean of identifying data; not clean of stray files.** Section 1.3 has the detail. The debts are: the five tracked-but-ignored paths (four small bytecode caches and a pid file; harmless in content, but they are the only binaries in the tree and they fail four checks); the cloud-session id in three Learn-phase files and two reviews; and the orchestrator's once-over of the 32 whole-tree `public_lint --all` hits (public contact addresses and creator handles quoted in research; one individual's handle with a quoted reaction at `research/ai-imagery.md:870` deserves a human look under D-26). The `.gitignore` additions are correct and additive, `!pc_report.schema.json` keeps the tracked schema visible, and `repo.gitignore_coverage` confirms nothing tracked was newly hidden. The 5-line edit to `tests/hygiene/test_lint.py` is benign and well explained: it strips the three new backstop lines from the throw-away repo's copy so WP-03's "refuse by name" tests keep modelling a clone without the backstop.

## 5. Fidelity to the plan and the register

Deviations are all declared, none silent: SP1 T5 cut (plan nudge 7, D-12); `lj.ps1 close` as a dry run in v0 with v1 in week 4 (plan C-13; the readiness map says "never PASS"); the Craft read-backs reported as Linux CLI results and not Windows evidence; the phone numbers marked (J) and UNVERIFIED. The plan's acceptance line `public_lint.py --diff` does not exist (the default mode is the diff), a text fix. The new text is 7.06 MB against the plan's 5 MB, of which `build/evidence` is 2.8 MB (my own count of untracked files is 2.1 MB plus the modified evidence); this is a plan constant to raise or a pruning decision, not a defect.

## 6. Critical issues (both must close before round 2 can approve)

1. **The integrated tree is red for orchestrator-owned reasons**: 6 of 15 global checks and 3 of 13 areas fail on issues 1, 3, 4, 5 and 6 of `BUILD-STATUS.md` section 4 (D-32 missing from the CSV mirror; five tracked-but-ignored files, four of them binaries; 15 stale hits, 11 of them in `.claude/`; the 5 MB new-text limit; WP-07's `list.live` threshold between 750 and 770 MB free). None is a defect in a checker, and I verified the D-32 fix is one command.
2. **One source of truth for the phone row before Sun 1 Nov**: `profile.json`/`PHONE-ROW.md` (3.5 Mb/s, 32 characters, measured) against `DECISIONS.md` W-63/W-18 (4 Mb/s, 36). Either value is defensible; two values are not. The card cannot be signed, and `parity.phone_profile_vs_register` stays red, until the orchestrator picks one.

## 7. Nudges (at most six)

1. **Go green, then round 2.** In this order: `python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv`; `git rm --cached` the five paths named in `run_all_checks_all.txt`; change the example IDs `O-95`/`O-96` in `scripts/decisions_to_csv.py` and `scripts/ops_lint.py` to a shape W-29 does not flag, rewrite or allowlist the 11 skill and 2 playbook stale hits, then `stale_check.py --baseline`; raise `hygiene.new_text_under_5mb` to 8 MB or prune the duplicate per-run transcripts under `build/evidence`; raise WP-07's `list.live` threshold to the two-stage figure. Then `bash build/run_all_checks.sh --quick` (about 5 minutes) and hand me the console copy. Do **not** run `cleanup_scratch.sh --yes` before that run: it removes the PowerShell the `win*` areas need.
2. **Settle the phone row in `DECISIONS.md` now, not on Sun 1 Nov.** My recommendation: amend W-63 and W-18 to the measured values (PH2 3.5 Mb/s cap; at most 32 characters a line for the phone burn-in, 36 stays the venue guide), because WP-08 measured 32 as what fits the 90% box in both scripts at `FontSize=28`, and a cap a learner's phone player must survive should be the stricter one. Then WP-08's `PHONE-ROW.md` can be pasted over the card as the plan intended, with the `Scripts tested:` line and a real date, and the card gains `latin`.
3. **Decide the disk question before any week-3 spike starts.** Either the orchestrator frees at least 4 GB on the shared volume (then `run_sp1.sh --all --profile lean` first, SP3 after), or SP3 moves to the maker's PC after the Tue 20 Oct inventory reports the tier, and SP1 T2/T4 run in the container at the lean profile once 15 MB more is free. Write the choice into `spikes/VERDICTS-W2.md` so the R8 rule (may agents render with the Craft CLIs?) has a date.
4. **Pre-decide SmartScreen for Sat 24 Oct.** Add one paragraph to `MAKER-CRAFT-ZIPS.md` "If something goes wrong": for the five portable programs only, in `C:\lj\tools`, after Step 3 printed `OK` for that zip, a "Windows protected your PC" dialog may be answered with "More info", then "Run anyway"; any other file, and any antivirus removal or quarantine, remains "stop and paste". Record the `NotSigned` lines as expected for alpha software. Without this, the day stops at the first app.
5. **Plan week 4 around her Diwali week.** When the Q11 answer arrives (Sun 25 Oct), move the maker-owed Windows items that do not depend on week-3 agent output (the ORA/OTIO round trips on Windows, the encrypted container's mount/dismount test, the phone-floor look) into Mon 2 to Sun 8 Nov where possible, and write the explicit fallback for P-LOCK if the maker has no hours Fri 6 to Wed 11 Nov: which maker-owed rows may stay `maker-owed` through P-LOCK without failing it, and which may not.
6. **Finish the public-tree once-over (issue 7).** Remove the cloud-session id from `research/craft-motion.md`, the two fixture scripts under `research/production-scale-fixtures/` and the two reviews (replace with `<scratch>`); look once at `research/ai-imagery.md:870`; allowlist the public vendor and mailing-list addresses in `scripts/public_lint.config.json` so `--all` becomes a usable weekly check instead of a 32-hit list.

## 8. What may go out now, regardless of the verdict

The maker's week as written in `BUILD-STATUS.md` section 2: the hours page today, the PC inventory Tue 20 Oct (WP-01a approved r1; the README's six paste-in commands are the fallback), `GATHER.md` Part A1 Wed 21 Oct, the Craft-zip guide Sat 24 Oct (with nudge 4 applied first), and the Sunday questions. None of these depends on the red checks, and none touches family material.

*Nothing in this review was committed; the orchestrator commits. Scores are 4 across the board: every package is approved and sound, the integration correctly exposes the debts above, and the only thing standing between this tree and an approve is the orchestrator's own short list.*
