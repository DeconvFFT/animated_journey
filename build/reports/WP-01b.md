# WP-01b report: `lj.ps1` doctor and close v0 (dry run only)

Package: WP-01b (wave 2, both). Branch `build/process-lock`. Date of this run: Mon 2026-10-19.
Decisions: W-26, W-06, W-29, D-12, D-15, D-25. Assumption A-04.

## Result in one paragraph

Round 0 built and tested the package; Fable's review r1 (`reviews/build/WP-01b-r1.md`, verdict REVISE, correctness 3) found one critical defect: a wildcard per-app entry such as `photocraft-*/*` resolved to, opened and listed as WOULD REMOVE a folder named `media` and a folder listed in `never_touch_paths`, because the never-touch guards ran only on the config text and in the main walk. **Fixed in "Changes after review r1" below.** After the fix, all six acceptance tests and all three extra bullets pass when run by hand, and the package's own suite is green: `bash tests/win_lj/run_tests.sh --all` gives **143 PASS, 0 FAIL, 10 UNVERIFIED, 0 SKIPPED, 0 BLOCKED** (153 evidence envelopes); `--quick` gives 45 PASS, 0 FAIL, 10 UNVERIFIED in 17 s. Before the fix, the same suite with the new planted canaries gave 2 FAIL (15 rows listed against 12 expected; the two wildcard refusals missing), which is the proof that the canaries catch the defect.

W-26 and W-06 "written and run once" is **not** satisfied by v0. The readiness map should say `v0 done, v1 not started`.

## What exists (owner paths only)

| Path | What it is |
|---|---|
| `win/lj.ps1` | `doctor`, `close` (always a dry run), `help`. 1,019 lines, no `param()` block on purpose, so `-Apply` and friends get a clear "not in v0" answer instead of a binding error. No write, delete, move, network, git-write or process-start code anywhere (36 banned patterns, grep-tested). |
| `win/lj.config.example.json` | `root`, `tools_root`, work and never-touch lists, six apps (photocraft, vectorcraft, lightcraft, filmcraft, effectcraft, soundcraft) with **empty** `recent_files` and `cache` lists, each marked `UNVERIFIED`, plus a `note` quoting what our notes say (the note is never used to find anything). |
| `win/README-LJ.md` | Plain-language README (148 lines). 7 PowerShell fences, all parse-tested. Section names tested: "What it never does", "doctor: what kind of computer is this?", "close: what would a clean-up remove?", "How to read the list", "If it says REFUSED", "What comes next", "UNVERIFIED". Its pointer to WP-07's "Where did it write?" section and its path-rewrite rules were checked against `spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md` and match. |
| `tests/win_lj/` | `run_tests.sh` (`--quick`, `--all`), `make_trees.py` (synthetic trees on Linux paths), `tree_hash.py` (SHA-256 over path, kind, mode, size, mtime in ns, link target and content, without following links), `check_close.py`, four configs (`planted`, `root_is_slash`, `root_is_repo`, `root_is_home`). |
| `build/evidence/wp01b/` | `tests.jsonl` (one `lj-evidence/1` envelope per test) and `summary.json`. |

## What `lj.ps1` does

- **`doctor [-FromReport PATH] [-SaveTier PATH]`**: reads a report (or runs sibling `step0_pc_tests.ps1`), finds Python (`py -3 -I -B`, then `python -I -B`; version-probed so the Microsoft Store stub is rejected), runs `scripts/windows_check.py`, prints the tier table. `-SaveTier` is validated before anything is collected (must be a `.json` file name, not a folder, not a raw-report name, never over an existing non-tier file) and the derived file is written by `windows_check.py`, never by `lj.ps1`.
- **`close [-Config PATH] [-SkipChecks]`**: validates the root first (refuses with exit 2: drive root, bare drive letter, repo root or anything inside it, profile root or a folder containing it, Windows system folders, a link, another git repo, missing root, unset variable, `tools_root` outside the root), then walks read-only and prints: numbered WOULD REMOVE list with files and sizes and a total, HELD BACK (with reasons), NOT ON THE LIST, SKIPPED (link), NEVER TOUCHED (`media`, `archive`, `masters`, `originals`, repos, `.hc`/`.tc` container files; these folders are not even opened), PER-APP LISTS (UNVERIFIED), the two read-only repo checks, `BACKUP: not implemented in v0 (week 4)`, reminders, and `files written: none`. Exit 0 done, 1 partial (unreadable folder or the 250,000-entry limit), 2 refused, 3 something missing.
- **`-Apply`, `-Commit`, `-IncludeWindowsRecent`**: any case, abbreviated to three or more letters, `--double-dash`, `:` or `=` forms, on either command, with or without a config: `-Apply: not in v0: planned for v1 in week 4; nothing was done`, `files written: none`, exit 2.
- **Targets in v0**: `*.xmp` under folders named `work` (names configurable), folders named `Recovery`, `Auto-Save`, `cache` (case-insensitive, plus any extra names in the config) under the tools root only, and the per-app lists. A per-app entry is accepted only inside the tools root, `%APPDATA%` or `%LOCALAPPDATA%`, with a path segment containing the app name, no `..`, no protected name and no link on the way; otherwise it is shown as REFUSED with the reason. Since r1 the never-touch rules (protected folder name, `never_touch_paths`, git repository, inside the project repository) are also applied to every folder a wildcard resolves to, on the way and at the end, and again as the first lines of `Measure-Candidate`.

## How to run (exact commands)

On the maker's PC, from the project folder (UNVERIFIED on Windows, see below):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 help
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 doctor
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 doctor -FromReport "$env:TEMP\lj_pc_report.json" -SaveTier .\pc_tier.json
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 close
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 close -Config .\win\lj.config.local.json -SkipChecks
```

In the container (pwsh 7.5.4 lives in the git-ignored scratch folder `<scratch>/pwsh`, put it on `PATH` or set `PWSH`):

```bash
cd /home/user/animated_journey
bash tests/win_lj/run_tests.sh --quick     # 17 s
bash tests/win_lj/run_tests.sh --all       # 80 s, exit 0 only if no FAIL or BLOCKED
```

## Acceptance tests (run by hand, outside the suite; every one also has a suite test)

`pwsh` below is pwsh 7.5.4 from the scratch folder. "Hash" means `tests/win_lj/tree_hash.py` over `win`, `tests/win/fixtures`, `tests/win_lj`, `scripts` (and the synthetic trees for `close`).

| # | Command | Result | Proof |
|---|---|---|---|
| 1 | `python3 -I win/tools/ps_lint.py win/lj.ps1 && bash win/tools/ps_parse.sh` | **PASS** | `win/lj.ps1: 0 error(s), 0 warning(s)`; `PARSED 58 item(s), 0 parse error(s)` (the count includes fences of other packages' docs); the README alone: `7 powershell fence(s): 0 error(s)`; the suite's own parse test reports `0 parse error(s)` for `lj.ps1` and the 7 README fences |
| 2 | `pwsh -NoProfile -File win/lj.ps1 doctor -FromReport tests/win/fixtures/report_gpu12_pro_16gb.json` | **PASS**, exit 0 | Prints the tier table (`gpu_tier gpu-8-12`, `ram_tier 16+`, `edition pro-or-higher`, `disk roomy`, `display fhd`, ffmpeg, python, git, craft pins) and `RESULT: exit 0`; last line `files written: none`. Hash before `9433b565...e5737 entries=60`, after the same: IDENTICAL |
| 3 | same plus `-SaveTier renders/wp01b/tier.json` | **PASS**, exit 0 | Output ends `files written: .../renders/wp01b/tier.json (derived tier file)`. `renders/wp01b/` held no files before and exactly one (911 bytes) after; repo hash identical. The file is `lj-pc-tier/1` with buckets and verdict words only. Searching it for every fixture hardware string (`cpu.name`, `gpus[0].name`, `vendor`, `vram_source`, `driver_version`) found none. The only fixture value that reappears is the ffmpeg build SHA-256, which the derived-file schema carries on purpose (WP-01a); the file is git-ignored under `renders/` |
| 4 | `pwsh -NoProfile -File win/lj.ps1 close -Config tests/win_lj/planted.config.json` | **PASS**, exit 0 | 12 items, 16 files, 10.9 KB: 5 `*.xmp` under `work` (including a name with spaces, brackets, `$` and a backtick, an upper-case `.XMP`, a non-ASCII name), and 7 folders or entries (Recovery, Auto-Save, `cache`, `Cache`, a per-app recent-file and a per-app cache). `check_close.py` against the manifest: `rows: 12 expected: 12 listed-and-expected: 12`, `problems: 0`. Planted trees hash before and after: `d03c35de...a5c02b80 entries=123`, identical (123 entries since r1: the canaries below were added). `BACKUP: not implemented in v0 (week 4)` printed. Run again under `unshare -rn`: same 12 items, exit 0 |
| 5 | `close -Apply`, `close -Commit`, `close -IncludeWindowsRecent` | **PASS**, each exit 2 | `-Apply: not in v0: planned for v1 in week 4; nothing was done` / `files written: none`. Also exit 2 for `close -Apply -Config planted`, `doctor -Apply`, `close "-Apply:$true"`. `close -Ap` is an unknown option (also exit 2, nothing done). Hash of repo sets and synthetic trees identical afterwards |
| 6 | `close -Config` with root `/`, the repo root, `%HOME%`, and an absolute `$HOME` path | **PASS**, each exit 2 | `REFUSED: the root is a drive root (/).`, `...is the project repository folder.`, `...is the user profile folder.` (twice). Each ends `Nothing was done.` / `files written: none` |
| 7 | Canaries and the outside symlink | **PASS** | Under `media/`, `archive/`, `masters/`, `originals/` (each also holding a `Recovery` folder and a `work/*.xmp` canary) and `otherrepo/`: none is listed as removable; `media`, `archive`, `masters`, `originals`, `otherrepo` (git repo) and `vault.hc` appear under NEVER TOUCHED. `work/link-out` (symlink to a folder outside the root), `work/link-file.xmp`, `work/broken.xmp`, `tools/vectorcraft-0.13.1/Recovery` and a link inside `effectcraft/Recovery` appear as `SKIPPED (link)`; the outside `secret.xmp` is never named. A Recovery folder that holds a link or a protected `media` folder is HELD BACK, not listed. Since r1: the wildcard entry `photocraft-*/*` finds `tools/photocraft-0.10.0/media` and `.../vault` (listed in `never_touch_paths`); both are `REFUSED` under HELD BACK with their own path, appear under NEVER TOUCHED, are not opened, and neither canary file name appears anywhere in the output |
| 8 | No network | **PASS** | `unshare -rn` (only `lo`, no DNS): `doctor` exit 0 and `close` exit 0 with identical lists. The suite also runs the full `close` with both repo checks on read-only mounts and no network (exit 0, `read_only_mounts_really_block_writes` proves the mounts block writes). No network, write, delete or process-start code in the script (grep, 36 patterns, no match) |
| 9 | Evidence lists UNVERIFIED Windows behaviours | **PASS** | 10 `UNVERIFIED` envelopes (list below), each with a reason; no envelope holds a path outside the placeholders, e-mail or IP-shaped string. `public_lint.py --paths` over all owned paths: 13 files, 0 identifying-data findings, 0 hygiene findings |

Extra probe (now a permanent `--all` test): `close` with the root set to the repo's **parent** folder, so the repo sits inside the root: the repo is listed as `<root>/animated_journey  (the project repository)` under NEVER TOUCHED, is not opened, and no line of it is in WOULD REMOVE; hash identical; 3 s.

## UNVERIFIED (nothing below has run on Windows)

Ten evidence envelopes, recorded in `--quick` and `--all`:

1. `windows.path_rules_on_ntfs`: drive and UNC roots, case-insensitive compares, 8.3 short names, long paths, `GetPathRoot` and `GetFullPath` on Windows.
2. `windows.reparse_points_on_ntfs`: symlinks and junctions carry the `ReparsePoint` attribute and are skipped; OneDrive placeholders and other reparse tags are skipped the same way. Tested with Linux symlinks only.
3. `windows.py_launcher_and_python`: `py -3 -I -B` and `python -I -B`, and the Microsoft Store stub being rejected by the version probe.
4. `windows.powershell_5_1_runtime`: parse-tested on 7.5.4 and checked against the 5.1 rules by `ps_lint.py`; nothing has been executed on Windows PowerShell 5.1 (scriptblock as `MatchEvaluator`, `Sort-Object` on calculated properties, `ConvertFrom-Json` arrays, `exit` inside a script run with `&`).
5. `windows.doctor_runs_step0_in_process`: `doctor` runs `step0_pc_tests.ps1` with `&` and reads its exit code; tested on Linux only.
6. `windows.environment_variables`: `APPDATA`, `LOCALAPPDATA`, `USERPROFILE`, `windir`, `ProgramFiles`, `ProgramData` on the maker's PC, including a managed PC.
7. `windows.per_app_lists_not_from_a_paste`: **no "where did it write" paste has arrived** (expected: it is a Sat 24 Oct item). Every shipped per-app list is empty and marked `UNVERIFIED`. If it has not arrived by Mon 26 Oct this is how the package ships; when it arrives, fill the lists in `win/lj.config.example.json` and re-run the suite.
8. `windows.mounted_container_detection`: v0 cannot detect a mounted VeraCrypt container; `never_touch_paths` in the config is the only guard (the README says so).
9. `windows.argument_binding_5_1`: checked on 7.5.4 only; PowerShell drops a trailing-colon argument such as `-Apply:` with no value before the script sees it, so that one form runs as a plain (harmless) dry run.
10. `windows.console_encoding`: non-ASCII names in a Windows console.

## Deviations from the plan, and why

1. **`doctor` without `-FromReport` writes one file, through `step0_pc_tests.ps1`, not through `lj.ps1`.** The plan says `doctor` "writes nothing unless -SaveTier". `step0_pc_tests.ps1` (WP-01a, not mine to edit) has no no-write mode; it always writes its report, by default `%TEMP%\lj_pc_report.json`. `lj.ps1` itself writes nothing, says before running it which file step0 will write, and ends with `files written by step0_pc_tests.ps1: %TEMP%\lj_pc_report.json` (the README says the same). Every acceptance test uses `-FromReport`, which writes nothing. If a strictly no-write `doctor` is wanted, WP-01a would need a `-NoWrite`/`-Print` mode first; I did not work around it.
2. **`close` exit code 0 even when the two repo checks report findings.** In v0 `stale_check.py --new-only` and `public_lint.py` are advice; the exit code only reflects the dry run itself (the README says so). In this checkout they exit 1 on files owned by other packages (below), and `close` still exits 0 as the acceptance test requires.
3. **Tests I added beyond the plan** (all inside `tests/win_lj/`): the repo-inside-the-root probe above; the `-SaveTier` refusal cases; no-Python and `-SkipChecks` paths; env-variable lists; empty root; read-only mounts; abbreviation and form variants of the three v1 switches.

## What I changed in the first run (round 0)

- `tests/win_lj/run_tests.sh`:
  - **Fix.** `close.root_containing_the_profile_refused` and `close.root_equal_to_the_profile_refused` set `HOME` to a fake profile inside the hashed synthetic trees; pwsh itself then wrote `.cache/powershell` and `.local/share/powershell` there, so the tree hash "changed" (115 to 123 entries). That is why the earlier run's evidence showed 2 FAIL. Those two runs now point `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME` at the temp folder and set `POWERSHELL_TELEMETRY_OPTOUT=1` and `POWERSHELL_UPDATECHECK=Off`. `lj.ps1` was never the writer: the refusal text and exit 2 were already PASS.
  - **Added** the two repo-inside-the-root tests.
  - **Changed** the UNVERIFIED block to run in `--quick` as well (it costs nothing, and the quick evidence is what the week-2 runner collects).
- `build/evidence/wp01b/*` regenerated by the final `--all` run. No other file was touched; nothing was committed or pushed.

## Changes after review r1

Review: `reviews/build/WP-01b-r1.md` (REVISE; nudges 1 and 2 had to land). Every item was applied in place and every acceptance test re-run (results above and below).

| # | Review item | What was done | Proof |
|---|---|---|---|
| 1 | `Resolve-AppEntry` / `Measure-Candidate`: never-touch guards on resolved matches | New function `Get-ProtectedReason` (leaf is a protected name, `Test-NeverPath`, `Test-IsGitFolder`, inside the project repository) with the reasons the review named. It runs (a) on every resolved match in the loop before `Measure-Candidate`, shown with the match's own path (`<root>/tools/photocraft-0.10.0/media - 'media' is a protected folder name`), (b) as the first lines of `Measure-Candidate`, so no caller can skip it, and (c) on each folder a wildcard matches **on the way** (not only at the last level), so `photocraft-*/*/cache` never opens `media` or `vault` either. When every match on the way was refused, no extra NOT PRESENT line is added. | `close.held_back_with_reasons`, `close.planted_list_is_exactly_the_manifest`, `close.wildcard_in_the_middle_of_a_path_does_not_open_protected_folders` |
| 2 | Canaries in `make_trees.py` and `planted.config.json`; `held_back_with_reasons` | Planted `tools/photocraft-0.10.0/media/CANARY-app-media.dat` and `.../vault/CANARY-vault.dat`; config now has `never_touch_paths ["tools/photocraft-0.10.0/vault"]` and photocraft `cache ["photocraft-*/*"]`. `expected.json` is unchanged (still 12 rows), so `check_close.py` fails on any extra row or canary name. `held_back_with_reasons` gained the two lines the review gave (`REFUSED\] photocraft/cache: .*media - 'media' is a protected folder name` and `... .*vault - listed in never_touch_paths`). **Before the fix** these tests failed: 15 rows listed against 12 (`media`, `vault`, and the nested `Auto-Save` folder described as item 1 under "beyond the six items"). | before: `FAIL close.planted_list_is_exactly_the_manifest`, `FAIL close.held_back_with_reasons`; after: both PASS |
| 3 | README line 66 | Now reads "The copy is for your PC only: never add it to git, and never paste it in chat." | `data.example_config_test_configs_and_readme` |
| 4 | Echoed raw tokens (old lines 928, 932, 946, 960) | New `Show-Token`: an option is shown by its name only (cut at `:` or `=`), anything else goes through `Show-Path`, long text is cut at 60 characters. Used for all five echoes (the "needs a value" line too). Checked against the old script: `-Bogus=<profile path>` printed the full path before, prints `'-Bogus'` now; a profile path as a command or argument prints as `%USERPROFILE%/x`. | `usage.unknown_command_echo_hides_the_profile_path`, `usage.unexpected_argument_echo_hides_the_profile_path`, `usage.unknown_option_echo_shows_the_name_only`, `usage.unknown_first_option_echo_shows_the_name_only` |
| 5 | `extra_tools_folder_names` made only of `*` and `?` | Ignored with a `NOTE:` in the style of the unknown-key note. The rule I used is slightly wider than the review's: an entry with **no letter and no digit** is ignored, so `*`, `?*` and also `*.*` (which would match every versioned app folder) are caught. No sensible folder name is lost. | `close.wildcard_only_extra_tools_folder_name_is_ignored`, `..._adds_no_row` (12 of 12 rows, no extras), `close.named_extra_tools_folder_name_still_works` (a normal name is still honoured) |
| 6 | README, UNVERIFIED section | Added: "Typing `-Apply:` with nothing after the colon is dropped by PowerShell before the script sees it, so that one form runs as a plain dry run" (seen on PowerShell 7; 5.1 unchecked; type the switch without a colon). Evidence item `windows.argument_binding_5_1` already carries it. | README data test |
| orch. | `.gitignore` | **Not changed here** (outside the owner paths). `git check-ignore win/lj.config.local.json` still says not ignored: the orchestrator needs to add `win/lj.config.local.json`. | see "For the orchestrator" |

Three small things I did beyond the six items, each one only able to make the dry run more cautious:

1. **A `never_touch_paths` folder nested inside a removal candidate holds the candidate back.** The review's guards cover the candidate itself. The mirror case (a candidate such as an `Auto-Save` folder that has a `never_touch_paths` folder inside it) was not covered, and the suite showed it: with the planted `tools/effectcraft-0.11.1/Auto-Save/keep/` (listed in `never_touch_paths`) the old code put the whole `Auto-Save` folder in WOULD REMOVE, counting the protected folder's file. `Measure-Tree` now treats such a child like a protected name, so the candidate is `HELD` ("contains a protected item named 'keep'"). That one line is the only change to `Measure-Tree`. Tests: `close.nested_never_touch_path_holds_the_candidate_back`, `close.nested_never_touch_path_candidate_not_in_would_remove`.
2. **A stray `.xmp` plant moved.** The old planted `tools/photocraft-0.10.0/stray.xmp` ("an xmp under tools is not a target") would now be matched by the wildcard `photocraft-*/*` (a `*` also matches files) and become a 13th row, which `expected.json` must not have. The plant moved to `tools/soundcraft-0.8.0/stray.xmp`, which no entry matches, and the absence test follows it.
3. **README** also says that a `*` entry is re-checked for every folder it finds, that a candidate with a `never_touch_paths` folder inside is HELD BACK as a whole, and what `extra_tools_folder_names` does with a name that has no letter or digit.

Test changes: `close.per_app_lists_are_marked_unverified` now expects `photocraft ... cache: 1 [UNVERIFIED]` (the planted config has one entry; the empty-list case is still covered by `close.empty_root_lists_nothing`). New tests are in `--all` only (16 more PASS lines: 127 to 143); `--quick` is unchanged at 45 PASS because the planted-tree tests already ran there with the new canaries.

UNVERIFIED on Windows after r1 (nothing here ran on Windows): the new code uses only .NET calls and cmdlets that the old code used, plus `[regex]` with `\p{L}\p{N}` and a `for` loop; it is parse-tested on PowerShell 7.5.4 and checked against the 5.1 rules by `ps_lint.py` only. The same ten evidence items stay UNVERIFIED.

## For the orchestrator (outside my owner paths, not changed)

- **`.gitignore`: add `win/lj.config.local.json`** (review r1, item 3). It is the file the README tells the maker to create inside the public repo's `win\` folder, and `git check-ignore -v win/lj.config.local.json` still reports it as not ignored.
- `public_lint.py` run by `close` flags four **tracked** `.pyc` files: `.claude/skills/free-creative-toolchain/recipes/__pycache__/r2_param.cpython-313.pyc`, `research/sources/__pycache__/check_mojang_quotes.cpython-313.pyc`, `research/toolchain-fixtures/__pycache__/derive_album_look.cpython-313.pyc`, `research/toolchain-fixtures/__pycache__/make_venue_test_kit.cpython-313.pyc` (`git ls-files` lists them; they match `.gitignore`). They are binaries in a public repo and need `git rm --cached` by the owner of those paths.
- `stale_check.py --new-only` currently reports about 18 NEW FAIL lines in `.claude/skills/*/SKILL.md`, `playbooks/production-scale.md` and `scripts/decisions_to_csv.py` (retired-value phrases quoted inside "retired" notes). They are in files the orchestrator or other packages own.
- Disk: 768 MB free at the end of r1 (99% used; r1 added a few KB of synthetic trees and rewrote the evidence, nothing was downloaded). Earlier run: 1.1 GB free (98% used). This package adds under 1 MB (evidence, `renders/wp01b/tier.json`) plus a few KB of synthetic trees in the scratch folder; nothing was downloaded.
- Evidence now in `build/evidence/wp01b/` is from `--all` (143 PASS, 10 UNVERIFIED, 153 envelopes). A later `--quick` run by `scripts/run_week2_checks.sh` overwrites it with the 45 PASS and 10 UNVERIFIED version, which is fine.
