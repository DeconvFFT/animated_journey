# WP-01b report: `lj.ps1` doctor and close v0 (dry run only)

Package: WP-01b (wave 2, both). Branch `build/process-lock`. Date of this run: Mon 2026-10-19.
Decisions: W-26, W-06, W-29, D-12, D-15, D-25. Assumption A-04.

## Result in one paragraph

All six acceptance tests and all three extra bullets pass when run by hand, and the package's own suite is green: `bash tests/win_lj/run_tests.sh --all` gives **127 PASS, 0 FAIL, 10 UNVERIFIED, 0 SKIPPED, 0 BLOCKED** (137 evidence envelopes); `--quick` gives 45 PASS, 0 FAIL, 10 UNVERIFIED in 17 s. The package was already built and committed by an earlier, interrupted run of this work package. That run's committed evidence had **2 FAIL** lines. I found the cause (a test-harness artefact, not a defect in `lj.ps1`), fixed it, added one safety test, made the UNVERIFIED list appear in quick runs too, re-ran everything and wrote this report. `lj.ps1` and the README and config example were audited line by line against the spec and needed no change.

W-26 and W-06 "written and run once" is **not** satisfied by v0. The readiness map should say `v0 done, v1 not started`.

## What exists (owner paths only)

| Path | What it is |
|---|---|
| `win/lj.ps1` | `doctor`, `close` (always a dry run), `help`. 971 lines, no `param()` block on purpose, so `-Apply` and friends get a clear "not in v0" answer instead of a binding error. No write, delete, move, network, git-write or process-start code anywhere (36 banned patterns, grep-tested). |
| `win/lj.config.example.json` | `root`, `tools_root`, work and never-touch lists, six apps (photocraft, vectorcraft, lightcraft, filmcraft, effectcraft, soundcraft) with **empty** `recent_files` and `cache` lists, each marked `UNVERIFIED`, plus a `note` quoting what our notes say (the note is never used to find anything). |
| `win/README-LJ.md` | Plain-language README. 7 PowerShell fences, all parse-tested. Section names tested: "What it never does", "doctor: what kind of computer is this?", "close: what would a clean-up remove?", "How to read the list", "If it says REFUSED", "What comes next", "UNVERIFIED". Its pointer to WP-07's "Where did it write?" section and its path-rewrite rules were checked against `spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md` and match. |
| `tests/win_lj/` | `run_tests.sh` (`--quick`, `--all`), `make_trees.py` (synthetic trees on Linux paths), `tree_hash.py` (SHA-256 over path, kind, mode, size, mtime in ns, link target and content, without following links), `check_close.py`, four configs (`planted`, `root_is_slash`, `root_is_repo`, `root_is_home`). |
| `build/evidence/wp01b/` | `tests.jsonl` (one `lj-evidence/1` envelope per test) and `summary.json`. |

## What `lj.ps1` does

- **`doctor [-FromReport PATH] [-SaveTier PATH]`**: reads a report (or runs sibling `step0_pc_tests.ps1`), finds Python (`py -3 -I -B`, then `python -I -B`; version-probed so the Microsoft Store stub is rejected), runs `scripts/windows_check.py`, prints the tier table. `-SaveTier` is validated before anything is collected (must be a `.json` file name, not a folder, not a raw-report name, never over an existing non-tier file) and the derived file is written by `windows_check.py`, never by `lj.ps1`.
- **`close [-Config PATH] [-SkipChecks]`**: validates the root first (refuses with exit 2: drive root, bare drive letter, repo root or anything inside it, profile root or a folder containing it, Windows system folders, a link, another git repo, missing root, unset variable, `tools_root` outside the root), then walks read-only and prints: numbered WOULD REMOVE list with files and sizes and a total, HELD BACK (with reasons), NOT ON THE LIST, SKIPPED (link), NEVER TOUCHED (`media`, `archive`, `masters`, `originals`, repos, `.hc`/`.tc` container files; these folders are not even opened), PER-APP LISTS (UNVERIFIED), the two read-only repo checks, `BACKUP: not implemented in v0 (week 4)`, reminders, and `files written: none`. Exit 0 done, 1 partial (unreadable folder or the 250,000-entry limit), 2 refused, 3 something missing.
- **`-Apply`, `-Commit`, `-IncludeWindowsRecent`**: any case, abbreviated to three or more letters, `--double-dash`, `:` or `=` forms, on either command, with or without a config: `-Apply: not in v0: planned for v1 in week 4; nothing was done`, `files written: none`, exit 2.
- **Targets in v0**: `*.xmp` under folders named `work` (names configurable), folders named `Recovery`, `Auto-Save`, `cache` (case-insensitive, plus any extra names in the config) under the tools root only, and the per-app lists. A per-app entry is accepted only inside the tools root, `%APPDATA%` or `%LOCALAPPDATA%`, with a path segment containing the app name, no `..`, no protected name and no link on the way; otherwise it is shown as REFUSED with the reason.

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
| 1 | `python3 -I win/tools/ps_lint.py win/lj.ps1 && bash win/tools/ps_parse.sh` | **PASS** | `win/lj.ps1: 0 error(s), 0 warning(s)`; `PARSED 34 item(s), 0 parse error(s)` (2 scripts, 32 README fences, including `README-LJ.md` fences at lines 29, 35, 49, 55, 70, 91, 97); the README alone: `7 powershell fence(s): 0 error(s)` |
| 2 | `pwsh -NoProfile -File win/lj.ps1 doctor -FromReport tests/win/fixtures/report_gpu12_pro_16gb.json` | **PASS**, exit 0 | Prints the tier table (`gpu_tier gpu-8-12`, `ram_tier 16+`, `edition pro-or-higher`, `disk roomy`, `display fhd`, ffmpeg, python, git, craft pins) and `RESULT: exit 0`; last line `files written: none`. Hash before `cf565e57...4fc708 entries=60`, after the same: IDENTICAL |
| 3 | same plus `-SaveTier renders/wp01b/tier.json` | **PASS**, exit 0 | Output ends `files written: .../renders/wp01b/tier.json (derived tier file)`. `renders/wp01b/` held no files before and exactly one (911 bytes) after; repo hash identical. The file is `lj-pc-tier/1` with buckets and verdict words only. Searching it for every fixture hardware string (`cpu.name`, `gpus[0].name`, `vendor`, `vram_source`, `driver_version`) found none. The only fixture value that reappears is the ffmpeg build SHA-256, which the derived-file schema carries on purpose (WP-01a); the file is git-ignored under `renders/` |
| 4 | `pwsh -NoProfile -File win/lj.ps1 close -Config tests/win_lj/planted.config.json` | **PASS**, exit 0 | 12 items, 16 files, 10.9 KB: 5 `*.xmp` under `work` (including a name with spaces, brackets, `$` and a backtick, an upper-case `.XMP`, a non-ASCII name), and 7 folders or entries (Recovery, Auto-Save, `cache`, `Cache`, a per-app recent-file and a per-app cache). Planted tree hash before and after: `99654d59...87b18f0 entries=115`, identical. `BACKUP: not implemented in v0 (week 4)` printed. Run again under `unshare -rn`: same 12 items, exit 0 |
| 5 | `close -Apply`, `close -Commit`, `close -IncludeWindowsRecent` | **PASS**, each exit 2 | `-Apply: not in v0: planned for v1 in week 4; nothing was done` / `files written: none`. Also exit 2 for `close -Apply -Config planted`, `doctor -Apply`, `close "-Apply:$true"`. `close -Ap` is an unknown option (also exit 2, nothing done). Hash of repo sets and synthetic trees identical afterwards |
| 6 | `close -Config` with root `/`, the repo root, `%HOME%`, and an absolute `$HOME` path | **PASS**, each exit 2 | `REFUSED: the root is a drive root (/).`, `...is the project repository folder.`, `...is the user profile folder.` (twice). Each ends `Nothing was done.` / `files written: none` |
| 7 | Canaries and the outside symlink | **PASS** | Under `media/`, `archive/`, `masters/`, `originals/` (each also holding a `Recovery` folder and a `work/*.xmp` canary) and `otherrepo/`: none is listed as removable; `media`, `archive`, `masters`, `originals`, `otherrepo` (git repo) and `vault.hc` appear under NEVER TOUCHED. `work/link-out` (symlink to a folder outside the root), `work/link-file.xmp`, `work/broken.xmp`, `tools/vectorcraft-0.13.1/Recovery` and a link inside `effectcraft/Recovery` appear as `SKIPPED (link)`; the outside `secret.xmp` is never named. A Recovery folder that holds a link or a protected `media` folder is HELD BACK, not listed |
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

## What I changed in this run

- `tests/win_lj/run_tests.sh`:
  - **Fix.** `close.root_containing_the_profile_refused` and `close.root_equal_to_the_profile_refused` set `HOME` to a fake profile inside the hashed synthetic trees; pwsh itself then wrote `.cache/powershell` and `.local/share/powershell` there, so the tree hash "changed" (115 to 123 entries). That is why the earlier run's evidence showed 2 FAIL. Those two runs now point `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME` at the temp folder and set `POWERSHELL_TELEMETRY_OPTOUT=1` and `POWERSHELL_UPDATECHECK=Off`. `lj.ps1` was never the writer: the refusal text and exit 2 were already PASS.
  - **Added** the two repo-inside-the-root tests.
  - **Changed** the UNVERIFIED block to run in `--quick` as well (it costs nothing, and the quick evidence is what the week-2 runner collects).
- `build/evidence/wp01b/*` regenerated by the final `--all` run. No other file was touched; nothing was committed or pushed.

## For the orchestrator (outside my owner paths, not changed)

- `public_lint.py` run by `close` flags four **tracked** `.pyc` files: `.claude/skills/free-creative-toolchain/recipes/__pycache__/r2_param.cpython-313.pyc`, `research/sources/__pycache__/check_mojang_quotes.cpython-313.pyc`, `research/toolchain-fixtures/__pycache__/derive_album_look.cpython-313.pyc`, `research/toolchain-fixtures/__pycache__/make_venue_test_kit.cpython-313.pyc` (`git ls-files` lists them; they match `.gitignore`). They are binaries in a public repo and need `git rm --cached` by the owner of those paths.
- `stale_check.py --new-only` currently reports about 18 NEW FAIL lines in `.claude/skills/*/SKILL.md`, `playbooks/production-scale.md` and `scripts/decisions_to_csv.py` (retired-value phrases quoted inside "retired" notes). They are in files the orchestrator or other packages own.
- Disk: 1.1 GB free at the end (98% used). This package adds under 1 MB (evidence, `renders/wp01b/tier.json`) plus a few KB of synthetic trees in the scratch folder; nothing was downloaded.
- Evidence now in `build/evidence/wp01b/` is from `--all` (127 PASS, 10 UNVERIFIED). A later `--quick` run by `scripts/run_week2_checks.sh` overwrites it with the 45 PASS and 10 UNVERIFIED version, which is fine.
