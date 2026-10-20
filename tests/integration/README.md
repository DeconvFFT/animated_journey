# tests/integration (WP-11b)

Do the pieces of build weeks 1 and 2 fit together? Every other package tests itself; this one tests the **seams**: two packages' files that must say the same thing,
the redaction rule across all its consumers, the disk budget as the evidence envelopes recorded it, three end-to-end runs, and the hygiene of the whole build.

```bash
bash tests/integration/run_tests.sh --quick    # about 25 s: parity, redaction, disk, hygiene, docs, readiness map, INDEX.md, negative controls (no render, no download)
bash tests/integration/run_tests.sh --all      # about 3 minutes: --quick plus the whole-tree audit and the three end-to-end tests
bash tests/integration/run_tests.sh --list     # the tests and which set each belongs to
bash tests/integration/run_tests.sh --all --only parity,e2e.a11     # development: tests whose name starts with one of these (writes the _only files, see below)
bash tests/integration/make_evidence.sh        # both suites and every acceptance command of the work package -> build/evidence/wp11b/
```

Output: one line per test `PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED name detail`, an envelope per test in `build/evidence/wp11b/tests_<mode>.jsonl` (build plan 4.2, with the `disk`
object), `summary_<mode>.json`, and the console copy `tests_<mode>.txt`. Exit 0 if no line is FAIL or BLOCKED, 1 if a line FAILs, 3 if the disk guard blocked a heavy step.
**A partial run (`--only`) never replaces the mode's evidence.** It writes `tests_<mode>_only.jsonl`, `tests_<mode>_only.txt` and `summary_<mode>_only.json` and leaves
`tests_<mode>.jsonl` and `summary_<mode>.json` alone (they were truncated by a partial run before). Nothing reads an `_only` file as evidence (the disk tests skip them) and
`make_evidence.sh` deletes any it finds and uses no `--only` step; delete them by hand when you are done developing, by these exact patterns only
(`tests_*_only.*` and `summary_*_only.json`; `e2e_spec_check_video_only.json` is a real evidence file of the end-to-end test and must stay).
UNVERIFIED means a Windows behaviour nobody has observed; it is listed, never counted as a pass. Work files go to `renders/wp11b/` (git-ignored) and are removed at the end.
Linux only; nothing here is a Windows script. It never calls `scripts/run_week2_checks.sh` (the runner refuses a nested run); the runner calls it as area 13.

## The tests

| Group | Test | What it proves | Fails when |
|---|---|---|---|
| parity | `settings_card_vs_settings_json` | every number in the card rows TD-1 to TD-4, Colour and Sound is the one in `pipeline/settings.json` and the venue chains of `chains.json` | a card value or a profile value changes in one place only |
| | `phone_row_md_vs_profile_json` | `PHONE-ROW.md` states what `profile.json` says, and the caption block it quotes is the one `build/evidence/wp08/fill_20x9_phone.json` measured | the row and the profile disagree |
| | `phone_profile_vs_register` | `pipeline/phone/profile.json` states the figures `DECISIONS.md` states for the phone files (W-63: PH1 CRF and cap, PH2 CRF, cap and level; W-18: phone caption FontSize, MarginV, characters a line), read from the register the way `pins_vs_release_assets_vs_w22` reads W-22. The register wins | `profile.json` differs from the register (today: PH2 cap 3.5 against 4 Mb/s, 32 against 36 characters; owner WP-08, its round-1 nudge 3) or a register row no longer states a figure in the shape read |
| | `card_phone_row_vs_phone_row_md` | the card's Phone row carries the register's figures and, for every other fact, those of `PHONE-ROW.md` and `profile.json`. When `profile.json` disagrees with the register it says so, names `profile.json` as the file that differs, and prints the fix: regenerate `profile.json` to W-63/W-18, or log the profile's figures in `DECISIONS.md`, and only then paste. It never tells anyone to move the card against the register | the card lacks a measured fact (today: the caption block 68.2 to 85.4%) |
| | `card_language_note_vs_scripts_tested` | the card's language line names the scripts tested and the date | placeholder left, or a script missing |
| | `render_builtin_chain_vs_chains_json` | `render.mjs` `BUILTIN_CHAINS.h264` equals `h264_venue` (video side) | the built-in default drifts from the file |
| | `profiles_vs_chains` | every delivery profile of `settings.json` and `phone/profile.json` names a chain that exists and promises the pixel format, codec, alpha and BT.709 tags the profile demands | a chain and a profile disagree |
| | `pins_vs_release_assets_vs_w22` | `win/pins.json` = `release_assets.json` = the W-22 row | a pin changes in one of the three |
| | `decisions_csv_vs_register` | `ops/decisions.csv` is the current mirror of `DECISIONS.md` | the register moved and the mirror was not regenerated |
| | `pc_report_fields_in_schema` | every field `windows_check.py` reads (traced at run time on 19 fixtures, not guessed from the source) is in `pc_report.schema.json` | the tool reads a field the PC script never writes |
| | `lj_close_v0_names_and_switches`, `_refusals_and_help` | `lj.ps1` calls `stale_check.py --new-only` and `public_lint.py`, names only scripts that exist, has no deleting, writing, committing or downloading option, and its code shows no mutating cmdlet, alias (`rm`, `rd`, `md`, `iex` ...), file redirection (`>`, `>>`) or git verb (also after options, `git -C $r commit`) to a **static scan**; `-Apply`, `-Commit`, `-IncludeWindowsRecent` exit 2 (PowerShell 7 on Linux). Commands invoked from a string or variable (`& 'Remove-Item'`, `& $c`) cannot be seen by any scan: `tests/win_lj/` (nothing changes, nothing is written, on fake trees) proves those absent | a v1 switch or a mutating command slips into v0 |
| | `noto_family_per_script_with_strings` | every script with test strings has a fetched Noto family in `libs.lock.json` | a script gets strings but no font |
| | `phone_row_scripts_tested_vs_json` | the `Scripts tested:` line = `scripts_tested.json` = the scripts with strings | the three drift |
| redaction | `self_test_zero_skipped_consumers` | `public_lint.py --self-test --fail-on-skip`: all four consumers agree, none skipped (Windows PowerShell 5.1 is a separate UNVERIFIED line) | a consumer is missing or disagrees |
| | `path_denylist` | no file anywhere in the tree is named like a raw PC report, outside `tests/win/fixtures/` (a `*.schema.json` is exempt) | a raw report name appears |
| | `pc_evidence_folder` | `build/evidence/pc/` holds only schema-valid derived files with none of the fixtures' GPU, CPU or driver strings | a raw or leaky file is filed |
| | `derivation_tools_leak_nothing` | `windows_check.py --tier-json-out` on all fixtures and `colour_patch.py --derive-from` on a raw file with a planted configure flag leak nothing | a derivation keeps a model name, a path or a flag |
| | `no_raw_report_shapes_in_evidence`, `gitignore_backstop_for_raw_reports` | nothing under `build/evidence/` looks like a raw report; `.gitignore` carries the Q-3 backstop | |
| disk | `stage_budget_rule_from_envelopes`, `every_envelope_carries_df_figures`, `hard_floor_crossings_are_explained` | the 400 MB rule and the 250 MB hard floor, read from every envelope; an envelope may raise its own floors but never lower the plan's (`floor_mb 0` is read as 400); the reviewed exceptions are in `disk_exceptions.json` | a stage over 100 MB broke the rule, or an unexplained crossing |
| | `each_tarball_downloaded_once`, `downloads_under_2gb_allowance` | the ledgers show each of the five pinned Craft tarballs once (a second fetch needs a recorded exception) and the FilmCraft 0.8.0 fallback, which is not a pin, at most once (SP1 T2 fetches it when T2 fails on 0.9.0); the fortnight's downloads stay under 2 GB (the PowerShell tarball's size is read from the guarded fetch's evidence, `build/evidence/wp01a/fetch_pwsh_guarded_run.txt`, and checked against `EXPECT_SIZE` of `win/tools/fetch_pwsh.sh`, not typed here) | a second fetch without a recorded exception, or a size that cannot be read from evidence |
| | `cleanup_scratch_dry_run_and_df`, `_yes_reports_df_after` | the dry run frees what it says and deletes nothing; `--yes` on a faithful fake tree removes exactly the listed items and prints `df` before and after | |
| hygiene | `stale_check_new_only`, `public_lint_over_the_diff`, `_over_the_build_folders`, `_whole_tree_audit` (all), `theme_guard` | the repo checks of the build plan; the diff mode is the default mode (there is no `--diff` flag). `theme_guard` scans the new or changed theme-bearing files, `pipeline/scenes`, the phone test strings and `ops/GATHER.md`, and, for `skills-staging/`, only the lines a staged copy adds or changes against its installed skill (the lines they share are INFO, as in `.claude/skills/`); a skill with no installed copy is scanned whole | |
| | `no_file_over_1mb`, `no_binary_file`, `new_text_under_8mb`, `no_ignored_file_tracked_or_staged` | size, binary, the 8 MB budget of new text (raised from the plan's 5 MB at gate review r1), and no ignored file tracked or staged | |
| docs | `pipeline_readme`, `staged_skill_update` | `pipeline/README.md` is one page and true; the staged skill keeps every heading and names the real scripts | |
| readiness | `map_statuses_and_evidence` | every row of `build/evidence/P-LOCK-readiness-W2.md` has one status from the four, no Windows row reads PASS, `lj.ps1 close` reads "v0 dry-run done; v1 not started (week 4)", every evidence path exists. A row's id is M or C and one or two digits; any other first cell under a `# ... Status` header (an added `M9` is fine and is checked; `M 9`, `m9`, a merged cell are reported) is a problem, so no row can hide a PASS | |
| index | `thirteen_rows_with_existing_links` | `build/evidence/INDEX.md` has the thirteen rows and every link exists | |
| | `runner_lists_thirteen_areas_landed` | `run_week2_checks.sh --list` shows 13 of 13 areas landed and every `tests/<area>/run_tests.sh` exists | |
| ctrl | `checkers_fail_on_planted_defects` | each checker above fails on a planted defect in a copy of its input (and passes the known-good state): the register against the profile, 22 planted `lj.ps1` lines and 7 harmless ones, envelopes with floors lowered to 0, an added `M9` row, a `--only` run that would replace the evidence | a checker that cannot fail |
| e2e (all) | `testcard_through_chain_checked_by_spec_check` | the WP-04 test card through `--chain h264_venue` passes `spec_check.py` (video-only view and, with a tone, the full `venue_h264`); a 25 fps / 720p view fails | |
| | `a11_mo8_pair` | `?push=transform` passes `mo8_gate.py`, `?push=layout` fails it | |
| | `phone_encode_from_harness_master_incl_fill_20x9` | a harness-rendered ProRes master passes `master_prores422hq`; PH1 passes `phone_1080` and the colour test; `fill_20x9` puts the caption at or above the 88% line and the venue-margin clip fails it | |

## Two things this suite does not do

* It does not run `scripts/cleanup_scratch.sh --yes` on the real tree: that deletes the PowerShell the Windows-script tests need. The orchestrator runs it as the last step.
* It does not judge pictures. The theme guard is a keyword scan; Fable reads the frames against D-28.
