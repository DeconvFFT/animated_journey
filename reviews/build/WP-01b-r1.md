# Fable review: WP-01b, `lj.ps1` doctor and close v0 (round 1 of 3)

Reviewed Mon 19 Oct 2026, branch `build/process-lock`. Package report: `build/reports/WP-01b.md`. Decisions checked against: W-26, W-06, W-29, D-12, D-15, D-25, D-26 and assumption A-04; plan sections 4.7, 4.9, 4.12 and the WP-01b row of the build plan.

**Verdict: REVISE.** Scores: correctness 3, safety and privacy 4, maker usability 4, fidelity to plan 4, maintainability 4. One critical issue (section 3, test A): a wildcard per-app entry walks straight past the never-touch rules, so a folder named `media` and a folder listed in `never_touch_paths` both appear in WOULD REMOVE. Everything else is in very good shape; the fix is about ten lines plus one planted canary, and I expect round 2 to approve.

**What this verdict means for the calendar.** Nothing in v0 can delete anything, so the maker may run `doctor` and `close` from this build without risk. The revision must land before the per-app lists are filled from the Sat 24 Oct paste (that is when wildcard entries first exist in a real config) and before any v1 work starts on this code path. W-26 / W-06 "written and run once" is not satisfied by v0; the report says so, and the readiness map should read `v0 done, v1 not started`.

## 1. What I read

Every file in the owner paths: `win/lj.ps1` (971 lines, read in full), `win/lj.config.example.json`, `win/README-LJ.md`, `tests/win_lj/run_tests.sh`, `make_trees.py`, `tree_hash.py`, `check_close.py`, the four test configs, `build/evidence/wp01b/summary.json` and `tests.jsonl` (137 envelopes). The report. Plan section 4.7 (Windows scripts), 4.9 (disk), 4.12 (definition of done) and the W-26 / W-29 rows of `DECISIONS.md`.

## 2. What I ran (from the repo root; pwsh 7.5.4 from the scratch folder; disk 775 MB available, 99% used, unchanged after)

| # | Test | Result |
|---|---|---|
| 1 | `python3 -I win/tools/ps_lint.py win/lj.ps1 && bash win/tools/ps_parse.sh` | **PASS**: `0 error(s), 0 warning(s)`; `PARSED 58 item(s), 0 parse error(s)` (the README-LJ fences are among them). The script is pure ASCII, so the 5.1 ANSI-vs-UTF-8 question does not arise. |
| 2 | `lj.ps1 doctor -FromReport tests/win/fixtures/report_gpu12_pro_16gb.json` with `tree_hash.py` over `win tests/win/fixtures tests/win_lj scripts` before and after | **PASS**, exit 0, tier table printed, `files written: none`, hash identical. |
| 3 | same with `-SaveTier renders/wp01b/tier.json` | **PASS**: exactly one file appears under `renders/wp01b/`; its top-level keys are the twelve `lj-pc-tier/1` keys; no GPU, CPU or vendor string from the fixture is in it. |
| 4 | `lj.ps1 close -Config tests/win_lj/planted.config.json -SkipChecks` with the planted tree hashed before and after | **PASS**, exit 0: 12 items, 16 files, 10.9 KB, as the manifest says; HELD, NOT ON THE LIST, SKIPPED (link), NEVER TOUCHED and PER-APP sections all as described; `BACKUP: not implemented in v0 (week 4)`; hash identical (`entries=115`). No canary, no `outside/`, no `secret.xmp` anywhere in the output. |
| 5 | `close -Apply`, `close -Commit`, `close -IncludeWindowsRecent` | **PASS**: each prints `<switch>: not in v0: planned for v1 in week 4; nothing was done` and `files written: none`, exit 2. |
| 6 | `close` with root `/`, the repo root, `%HOME%` | **PASS**: `REFUSED: the root is a drive root (/).`, `...the project repository folder.`, `...the user profile folder.`; exit 2 each; `Nothing was done.` |
| 7 | `public_lint.py --paths` over the owner paths plus the evidence folder and the report | 14 files, 0 identifying-data findings, 0 hygiene findings. A grep of `tests.jsonl` for `/home/`, e-mail shapes and IPv4 shapes: 0 hits. |

The committed evidence (`--all`: 127 PASS, 0 FAIL, 10 UNVERIFIED) is consistent with what I saw. I did not re-run the whole suite (80 s and it rewrites the evidence); the hand runs above cover the six acceptance bullets.

## 3. Tests of my own, designed to break it

Synthetic trees only, built in a new folder under the scratch area and deleted afterwards.

**A. Wildcard per-app entry against a protected name and a `never_touch_paths` folder. FAILED (critical).**
Tree: `root/tools/photocraft-0.10.0/{media/CANARY-media.dat, Recovery/a.dat, vault/CANARY-vault.dat}`. Config: `never_touch_paths: ["tools/photocraft-0.10.0/vault"]` and photocraft `cache: ["photocraft-*/*"]`. Output:

```
    1  photocraft/cache (folder)          1         7 B  <root>/tools/photocraft-0.10.0/media
    2  Recovery (folder)                  1         2 B  <root>/tools/photocraft-0.10.0/Recovery
    3  photocraft/cache (folder)          1         2 B  <root>/tools/photocraft-0.10.0/vault
```

Both `media` and the `never_touch_paths` folder are listed as WOULD REMOVE, and `media` was opened and its file counted, which the README promises never happens ("It does not open those folders"). Cause: `Resolve-AppEntry` checks `Test-NeverName` only on the *segments of the config text* (line 507) and never checks `Test-NeverName`, `Test-NeverPath` or `Test-IsGitFolder` on the *resolved* matches (line 543); `Measure-Candidate` checks protected names only among a folder's children, not on the folder itself. The main walk (lines 683 to 686) has all four guards, which is why the acceptance canaries pass: they only exercise the walk. The shipped example config has empty lists, so no maker is exposed today; the exposure begins the moment the Sat 24 Oct paste produces an entry with a `*` in it, and the README itself recommends `lightcraft-*/...`. A link matched by a wildcard *is* handled (SKIPPED), so the pattern for the fix is already there.

**B. `extra_tools_folder_names: ["*"]`.** Every folder under the tools root becomes a candidate. In my tree `photocraft-0.10.0` ended up HELD only because it happened to contain a `media` child; in a tree without one it would be a WOULD REMOVE line for the whole app folder. Config footgun rather than a defect (the config is the maker's own and v0 lists only); worth a one-line refusal of a name that is nothing but wildcards.

**C. `-Apply:` (trailing colon, no value).** pwsh drops the token before the script sees it and `close` runs as a plain dry run, exit 0. Already recorded honestly as UNVERIFIED #9 in the evidence; harmless in v0. It should be in the README's UNVERIFIED list too, because in v1 the same form would silently *not* apply.

**D. Root under the profile.** `root: "%HOME%/lj"` with a fake HOME: the root prints as `%USERPROFILE%/lj`, items as `<root>/...`, and the expanded home path appears nowhere. **PASS.**

**E. Echoed tokens.** `Unknown option '...'` and `Unexpected argument '...'` (lines 928, 932, 946, 960) echo the raw token. A maker who types a profile path in the wrong place sees it expanded on a console the plan calls "safe to paste". Console only, nothing written; a small nudge.

## 4. Findings by criterion

**Correctness (3).** Everything in the acceptance list works and the dedup, sizing, numbering and exit codes are right. The one defect (A) sits exactly on the safety rule the package exists to enforce, so I cannot score it 4 until the resolved-path guards exist and a planted canary proves them.

**Safety and privacy (4).** Read-only by construction: no write, delete, move, network or process-start call in the script (36 banned patterns, grep-tested; the only `.NET` IO calls are reads), proven under `unshare -rn` and on read-only bind mounts. Paths under a profile print unexpanded; error text passes through `Clean-Message`; the derived tier file holds buckets only. No name, host, e-mail or IP in any owned file or in the evidence. Nothing here could tip off the mother and no family media exists. One housekeeping gap: `win/lj.config.local.json`, the file the README tells the maker to create, lives inside the public repo's `win\` folder and is **not** git-ignored (`git check-ignore` says so). The README says the copy "is not for the project folder" but then puts it there. The content is not identifying today (`C:/lj`), but `never_touch_paths` is where the maker will list a mounted container folder, and v1's `-Commit` will commit text. Needs a `.gitignore` line from the orchestrator and one plain sentence in the README.

**Maker usability (4).** `README-LJ.md` is plain, ordered, and tells the maker exactly what each section of the output means and what REFUSED means. The exit codes are explained twice (doctor and close) in the maker's words. The "known gap" paragraph about FilmCraft's Auto-Save next to a project is the right kind of honesty. Two small things: the local-config placement sentence above, and the `-Apply:` note.

**Fidelity to plan (4).** Targets, root refusals, reparse handling, `-Apply`/`-Commit`/`-IncludeWindowsRecent` answered with exit 2, `BACKUP: not implemented in v0 (week 4)`, reminders, UNVERIFIED per-app lists, evidence envelopes with disk figures, UNVERIFIED Windows claims in evidence and README, nothing committed, nothing under `.claude/` touched: all as specified. The documented deviation (plain `doctor` lets `step0_pc_tests.ps1` write its own `%TEMP%` report) is inherent in the plan's own wording and is said in three places. The reading of W-26 / W-06 is correct: v0 is not the "written and run once" run.

**Maintainability (4).** One file, sectioned, with a comment where a choice is non-obvious (no `param()` block, why links are not followed, why `GetFullPath` is avoided on wildcard text). It reuses `windows_check.py`, the WP-01a fixtures, `ps_lint.py`, `ps_parse.sh`, `public_lint.py` and `stale_check.py` instead of duplicating them. The test runner is dense but every test has a name and an evidence envelope, and `check_close.py` compares against a generated manifest rather than hard-coded strings. `run_tests.sh` hard-codes `/home/user/build-scratch` as a default (overridable through `LJ_SCRATCH`); acceptable for a container-only runner.

## 5. Nudges (at most six; the first two must land for approval)

1. **`win/lj.ps1`, `Resolve-AppEntry`, the loop at line 543.** Before `Measure-Candidate`, refuse any resolved match `$c` where `Test-NeverName ([System.IO.Path]::GetFileName($c))`, `Test-NeverPath $c`, or `Test-IsGitFolder $c` is true, with the reasons `'<name>' is a protected folder name`, `listed in never_touch_paths`, `a git repository`. Add the same three guards (plus `Test-SameOrInside $full $script:RepoRoot`) as the first lines of `Measure-Candidate` so no future caller can skip them.
2. **`tests/win_lj/make_trees.py` and `planted.config.json`.** Plant `tools/photocraft-0.10.0/media/CANARY-app-media.dat` and `tools/photocraft-0.10.0/vault/CANARY-vault.dat`, add `never_touch_paths: ["tools/photocraft-0.10.0/vault"]` and a photocraft `cache` entry `photocraft-*/*` to the planted config; `expected.json` stays as it is, so `check_close.py` fails on any extra row or canary name. In `run_tests.sh` extend `close.held_back_with_reasons` with `-m "REFUSED\] photocraft/cache: .*media - 'media' is a protected folder name"` and a `never_touch_paths` line.
3. **`win/README-LJ.md` line 66, and the orchestrator.** Replace "The copy stays on your PC (it is not for the project folder)" with "The copy is for your PC only: never add it to git, and never paste it in chat." Orchestrator: add `win/lj.config.local.json` to `.gitignore` (outside this package's owner paths).
4. **`win/lj.ps1` lines 928, 932, 946, 960.** Print the echoed token through `Show-Path` (or print only `Get-OptionName $t`) so a mistyped profile path never appears expanded on the console.
5. **`win/lj.ps1` line 665.** Skip an `extra_tools_folder_names` entry that contains no character other than `*` and `?`, and print a `NOTE:` saying it was ignored (same style as the unknown-key note at line 600).
6. **`win/README-LJ.md`, the UNVERIFIED section.** Add: "Typing `-Apply:` with nothing after the colon is dropped by PowerShell before the script sees it, so that one form runs as a plain dry run."

## 6. For the orchestrator (outside the owner paths, not changed here)

- `.gitignore`: `win/lj.config.local.json` (nudge 3).
- The report's two notes stand: four tracked `.pyc` files flagged by `public_lint.py`, and about 18 NEW stale lines in orchestrator-owned files. Neither is this package's.
- Disk: 775 MB available at review time (99% used), below the 1.1 GB the report saw; `cleanup_scratch.sh` is due.
