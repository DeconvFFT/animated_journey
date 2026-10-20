# Report: package c3-evidence-verdicts (week-2 close-out)

*Sonnet implementor, Tue 20 Oct 2026, branch `build/process-lock`. Synthetic material only; nothing committed or pushed; nothing under `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` touched. Nothing is approved yet (D-32: Fable reads this next).*

Source of the five items: `reviews/build/w2-gate-r1.md` nudge 6, nudge 5 (size watch) and issues 14, 20 and 21 of `build/BUILD-STATUS.md`. The restart checkpoint `3a500dd` held none of this package's work (it holds the FilmCraft ruling and the phone wording); I started from the tree as it stood and kept what other packages had written.

Where this report says `<session scratchpad>`, the orchestrator's text had the full scratch path with the cloud session's id in it. The repo is public and `scripts/public_lint.config.json` says session ids are "reported to the orchestrator, or removed from the text", so the path with the id is not written anywhere in the repo.

## 1. What changed

| Item | Files | What |
|---|---|---|
| (a) disk work on record | `spikes/verdicts/template.md` (so `spikes/VERDICTS-W2.md`) | Disk-decision step 1 now carries the orchestrator's sentence, **Done Tue 20 Oct (orchestrator)**: about 14 GB freed, about 15 GB free, `bpyenv`, the Whisper environment, `vendor/` and `fc_dl` kept, about 11 GB of older scratch remains. A table under the disk table gives one line to rebuild each kept environment, after opening each one. SP3 step 3 no longer says the pip fetches are outside the ledger. |
| (b) pip fetches on the ledger, hash-pinned install | new `spikes/sp3_blender/requirements-bpy.txt`, `spikes/sp3_blender/ledger_row.py`; changed `spikes/sp3_blender/run_sp3.sh`, `test_cleanup.sh`, `README.md`, `spikes/sp1b_readback/check_ledger.py`, `build/evidence/wp10/download_ledger.jsonl` (+2 rows), `tests/integration/run_checks.py` and `README.md`, `tests/spikes/run_tests.sh` | See 2.2. |
| (c) size | deleted 6 files under `build/evidence` | See 2.3. |
| (d) one writer per verdict file | new `spikes/verdicts/{README.md,assemble.py,template.md,SP1.md,SP2.md,SP3.md,SP4.md,SP5.md}`; `spikes/VERDICTS-W2.md` is now generated; `tests/spikes/run_tests.sh` (2 tests) | See 2.4. |
| (e) win_kit2 limit | `scripts/run_week2_checks.sh`, `tests/runner/test_runner.sh`, `tests/win_kit2/run_tests.sh` (header), `build/run_all_checks.sh` (header comment) | See 2.5. |

## 2. What was done, with the commands and results

### 2.1 (a) The disk record and the rebuild lines

I opened both kept environments before writing their lines.

* `bpyenv` (2.0 GB): a Python 3.13.16 venv; `import bpy` prints Blender **5.2.2 LTS**. It holds numpy 2.5.4, Cython 3.3.0, zstandard, requests and others (certifi 2026.7.22, from 18 Oct). It also holds a **second, nested copy `bpyenv/venv` (1,008 MB, same `bpy`)** that the outer environment does not need. Rebuild: `python3.13 -m venv <dir> && <dir>/bin/python -m pip install --no-cache-dir --require-hashes -r spikes/sp3_blender/requirements-bpy.txt`.
* Whisper `venv` (461 MB): a venv with **faster-whisper 1.2.1** (ctranslate2 4.8.3, onnxruntime 1.31.0, av 19.0.1, tokenizers 0.23.3, huggingface_hub 2.2.0); `import faster_whisper` works. The weights are **not** in it: the Systran `base` and `small` models are in the Hugging Face cache (605 MB, outside the scratchpad and the repo). Rebuild: `python3.13 -m venv <dir> && <dir>/bin/python -m pip install faster-whisper==1.2.1`.
* `vendor/` is 0.6 MB now (fonts and gsap; `vendor/craft` and `craft-sp1b` are empty): `bash pipeline/lib/fetch_libs.sh --check` says "all files match the lock"; rebuild `bash pipeline/lib/fetch_libs.sh`.
* `fc_dl` (273 MB) is a download folder, not an environment (0.8.0 Linux tarball, 0.9.0 Windows x64 zip, the 0.9.0 sums file, one extracted 0.8.0 tree); a fresh fetch is a second fetch and needs a ledger exception.

### 2.2 (b) Ledger and hash-pinned install

* `requirements-bpy.txt`: 12 wheels (bpy plus 11), each `==` and one sha256, a `--require-hashes` line, a size comment per wheel. The 12 digests are those in `build/evidence/w2-sp3/run2_pip_summary.json`; **I also read the PyPI JSON metadata for all 12 files (metadata only, no wheel downloaded) and all 12 digests equal PyPI's**. Total 428,225,665 bytes per fetch (the bpy wheel 401,697,653; the other 11 together 26,528,012, which the report had put at "roughly 30 MB").
* `ledger_row.py check | count | append`: `check` validates the file against the run-2 pip report (12 of 12 compared); `append` writes one row (`kind` `pip-wheel-set`) and refuses a second fetch without a reason (exit 3), as for a Craft tarball.
* Two rows back-filled in `build/evidence/wp10/download_ledger.jsonl` (run 1 at 01:19 UTC; run 2 at 02:05 UTC with the recorded reason: the run-1 venv was deleted and the cleanup fix had to be confirmed on a real install, after a restart, on a different host). `python3 -I spikes/sp1b_readback/check_ledger.py` now reads **1506.9 of 2048 MB** (it read 623.6 MB), exit 0. `check_ledger.py` lists the set, counts it in the total and holds a repeat fetch to the exception rule; `tests/integration/run_checks.py::t_ledger` was updated because it demanded exactly five non-fallback assets (a bpy row would have failed it) and `disk.downloads_under_2gb_allowance` now reads **1667 MB of 2048 MB** (ledgers 1580 + PowerShell 75.4 + npm 11 + 1).
* `run_sp3.sh --run`: installs with `pip install --no-cache-dir --require-hashes -r spikes/sp3_blender/requirements-bpy.txt`; prints the bpy digest it compared against; appends its own ledger row right after the install; **refuses before downloading** when the ledger already holds a fetch and `SP3_FETCH_REASON='why'` is not set (exit 3, "Nothing was started"); `--check` prints the wheel-set check and the fetch count; the dry run says what a real run would need. `LJ_SP3_LEDGER` and `LJ_SP3_REQ` exist for the tests only.
* **A defect I introduced and the regression test caught:** my first edit ended `run_inner` with `[[ ... ]] && return 1`, which made a clean run exit 1. `spikes/sp3_blender/test_cleanup.sh` failed it, I fixed it (`if ...; then return 1; fi`), and the test now copies the two new files into its temporary root. It is also wired into the spikes quick suite (`sp3.cleanup_regression`, which is SP3 review nudge 2); the pre-fix script still FAILS it, as before.
* G1: a third fetch (428,225,665 bytes) would bring the ledger to about 1,915 MB of 2,048, so the allowance holds with about 130 MB to spare; the allowance decision stays the orchestrator's.

### 2.3 (c) The size, measured with the integration test's own method (same baseline, same roots; the test itself printed 7.34 MB at the start)

| Moment | New text |
|---|---|
| Gate round 1 (as reported) | 7.70 MB in 624 files |
| Start of this package | **7,342,087 bytes (7.34 MB) in 610 files** (`build/evidence` 2.838 MB) |
| After the prune alone | 7.434 MB in 614 files (other packages were adding files at the same time) |
| End of this package, after the quick pass and this report | **7.52 MB in 621 files** (`build/evidence` 2.820 MB) |

I deleted 6 files, **52,805 bytes**: `wp11a/area_{hygiene,render,runner,integration}_all.txt` (each the same stdout as the area's own `tests_all.txt` from the same `--all` run, or, for `integration`, an older run than `wp11b/tests_all.txt`; none cited by name) and the two partial-run leftovers `wp11b/tests_quick_only.jsonl` and `summary_quick_only.json` (docs name them only as the by-product of a `--only` run; `run_checks.py` says nothing reads `_only` files as evidence, and `BUILD-STATUS.md` says they were meant to be restored or removed). Everything else is kept for one of three reasons, checked file by file: a review or report cites it, by path or by folder plus bare name (the WP reports list `tests_all.txt`, `tests_quick.txt` and so on under their evidence folder, which a first scan by full path missed, so I re-checked every candidate by name before deleting); it is the latest run of its kind (`area_win_all`, `area_validators_all`, `area_roundtrip_all`, `area_sp1_all`, `area_win_kit2_all`, `area_spikes_all` are newer than the cited package transcripts, so both stay); or the next `--quick` pass rewrites it anyway (`area_*_quick.txt`, `tests_quick.*`).

**Honest result:** under "never delete a cited file" almost nothing in `build/evidence` is a removable duplicate, and what I added (the verdict parts, the ledger tool, the tests, the 4 KB of ledger rows and this report, about 0.1 MB) is larger than what I could remove (0.05 MB). The new text is **7.52 MB of 8.00 MB, 0.48 MB (6 percent) of headroom**, down from the 7.70 the gate saw only because other packages' rewrites shrank it. The next review round (one review file is 30 to 50 KB) and one `--all` pass (the `area_*_all.txt` files I deleted come back, about 130 KB with the rest) will use most of it. Decision for the orchestrator in section 6.

### 2.4 (d) One writer per verdict file

The mechanism is per-spike files plus a script (the first of the two options). `spikes/verdicts/README.md` states the rule and the table of who writes what. In short: `SPn.md` holds spike n's row, rule line, "does not say" bullet (and SP1's six test rows), written only by the package that runs the spike; `template.md` holds everything else, written only by the orchestrator; `spikes/VERDICTS-W2.md` is generated by `python3 -I spikes/verdicts/assemble.py` and nobody edits it. `assemble.py check` exits 1 on a hand edit or a stale assembly; `assemble.py import` splits a hand-edited file back into parts (the recovery path, used once for the migration).

* The migration changed nothing but three things (diffed against a copy taken immediately before): a first line saying the file is generated, one new paragraph under "How to check this file", and the SP3 and SP4 "does not say" bullets now in spike order.
* SP4 in week 3 is one file: `SP4.md` (the row, and the bullet that says it is armed, not run).
* `tests/spikes/run_tests.sh` gained `verdicts.assembled` (the real tree) and `verdicts.assemble_machinery` (on a copy: split and join lose no line, a hand edit is refused with exit 1, a row in the wrong file, test rows outside SP1 and a rule in the wrong file each exit 2 and write nothing).
* **A concurrent writer was live while I did this.** At 04:04 to 04:08 UTC the FilmCraft-ruling package (`w2c-c1-...`) rewrote the header, the SP1 and T2 rows and step 2 of `VERDICTS-W2.md` in place. My edits were exact-string and atomic, both sets survived, and I migrated from the file as it then stood. The cost of that is section 6, item 1.

### 2.5 (e) win_kit2

I profiled it before deciding. `tests/win_kit2/run_tests.sh --quick` took 37 s in my profiling run and 40 s in the final quick pass (39 s in the `INDEX.md` before, 47 s at the gate): about 80 CPU-seconds on 4 vCPUs, with five pwsh workers and `kb_checks.py` (22 s of its own; its one-second render is 8.8 s and the helper checks 4.3 s) running at once. It is CPU-bound, and the tests are the quick pass's coverage, so a trim would mean cutting checks; I raised the limit instead.

The runner now accepts an optional sixth field on an area line, a quick-mode limit in seconds. `win_kit2` has `90`, with a dated comment above `DEFAULT_AREAS` (47 s times 1.4 to 2x is 66 to 94 s, so 90 s covers a 1.9x host and a hang is still killed). It applies to `--quick` only, and an explicit `--timeout` or `LJ_RUNNER_TIMEOUT_S` switches it off. The console line, `INDEX.md` ("per-area limit 60 s; own limit: win_kit2 90 s") and `week2_summary.json` (`timeout_s` per area) say so. Six runner tests were added (and two that run in `--all` mode only, which I checked by hand): `tests/runner/test_runner.sh quick` 89 PASS, 0 FAIL, 34.9 s (it was about 34 s).

The same exposure at a smaller margin sits on four other areas (last pass: validators 33 s, phone 30 s, runner 38 s, integration 29 s; the gate saw 45, 38, 37 and 36). I left them on 60 s on purpose; each is a one-field edit if a measured run says so.

## 3. Checks run

| Command | Result |
|---|---|
| `python3 -I spikes/sp3_blender/ledger_row.py check` | OK: 12 pinned, 12 compared with the pip report; three planted defects (changed digest, no `--require-hashes` line, a requirement without a hash) each exit 1 |
| `python3 -I spikes/sp1b_readback/check_ledger.py` | exit 0, 1506.9 of 2048 MB, the bpy set listed with 2 fetches |
| `bash tests/spikes/run_tests.sh --quick` | 41 PASS, **1 FAIL (`verdicts.complete`, not mine, below)**, 0 BLOCKED, 1 UNVERIFIED; 11 tests are new (hash pin and its defects, an offline `pip --require-hashes` run on a tiny local wheel: right digest installs, wrong digest and missing hash refused; second-fetch rule; ledger counting; refusal without `SP3_FETCH_REASON`; the install step of `run_inner` offline with a wrong and a right digest; `sp3.cleanup_regression`; the two verdict tests). Area time rose from about 15 s to 28 s |
| `bash spikes/sp3_blender/test_cleanup.sh` | PASS (and the pre-fix script still FAILS it) |
| `bash tests/runner/test_runner.sh quick` | 89 PASS, 0 FAIL |
| `python3 -I tests/integration/run_checks.py --only disk.each_tarball_downloaded_once,disk.downloads_under_2gb_allowance` | both PASS (run into a scratch evidence folder) |
| `python3 -I scripts/public_lint.py --paths ...` over every file I touched | 0 identifying-data and 0 hygiene findings; the theme guard 0 findings; `stale_check.py --new-only` 0 new FAIL, 0 new WARN |
| `bash build/run_all_checks.sh --quick` (04:19 to 04:24 UTC) | **exit 1.** Part A 13 PASS, 1 FAIL; Part B 13 landed, 10 PASS, 3 FAIL, 0 TIMEOUT, **321 s of the 450 s budget**; envelopes PASS 1048, FAIL 9, UNVERIFIED 28, SKIPPED 2, BLOCKED 1. The three failing areas fail for reasons outside this package (section 4) |

## 4. The three failures in the quick pass, and why none is this package's

1. `stale.self_test` (Part A, and the `hygiene` area through the same self-test): "row S-65 has status 'outstanding' but Table 4 says 'applied'". The register flipped S-65 at `f474039`; the copy in `scripts/stale_patterns.json` was not updated. Already diagnosed in `build/reports/w2c-c2-phone-wording.md` item 1, with the fix.
2. Integration `parity.phone_profile_vs_register` and `ctrl.checkers_fail_on_planted_defects`: the test's PH2 pattern (`tests/integration/run_checks.py`, `register_phone_facts`) no longer matches because the register's W-63 row carries its in-row "Amended 2026-10-20" marker. Same report, items 2 and 3, with the fix. I did not apply either fix: both are the orchestrator's open items there.
3. `verdicts.complete` (spikes area): the SP1 row cites `build/reports/w2c-c1-filmcraft-dissolve.md`, which the FilmCraft-ruling package has not written yet (its edits of the SP1 and T2 rows are already in). The check will pass when that report exists; nothing in my change touches the evidence-path rule.

## 5. UNVERIFIED

* **Nothing was downloaded.** The hash-pinned install was exercised offline (a tiny local wheel, this machine's pip 24.0 and the venv's pip), and every digest was compared with PyPI's published metadata, but a real 428 MB `--require-hashes` install has not run; the first one is G1's. If PyPI withdraws one of the twelve files the install stops, by design.
* The rebuild lines for `bpyenv` and the Whisper environment were **not run** (both import today). A rebuild of `bpyenv` differs by a newer certifi; the Whisper line does not pin its dependencies.
* Whether another job of the earlier session uses the nested `bpyenv/venv`.
* win_kit2's new limit is arithmetic on the recorded spread (1.4 to 2x), not a measurement on a slower host; the 90 s was never needed here (37 to 47 s).
* The size figures are the integration test's method replicated; the test's own line in the last pass read 7.49 MB in 620 files, and it changes with every run.
* `spikes/verdicts/assemble.py import` classifies a "does not say" bullet by the spike name it contains (SP4, SP3 or "hero frame", SP1 or "T2 and T4", SP2, SP5); a reworded bullet that names none stays in the template. It is a recovery tool and was exact on the one migration.

## 6. For the orchestrator

1. **`VERDICTS-W2.md` is generated from now on, and one package was editing it when I migrated.** If the FilmCraft-ruling package (or anyone) writes to `spikes/VERDICTS-W2.md` again, `verdicts.assembled` goes red. Fix without losing the edit: `python3 -I spikes/verdicts/assemble.py check` (shows the difference), then `python3 -I spikes/verdicts/assemble.py import` followed by `python3 -I spikes/verdicts/assemble.py`, **as long as no `spikes/verdicts/SPn.md` has been edited since the last assembly**; otherwise move the edit into the right part by hand. Please tell that package to use `spikes/verdicts/SP1.md` (rows `T2`, SP1) from now on.
2. **Roadmap:** I need no change. `ROADMAP.md` row 135 stays with the SP1 ruling; the SP3 allowance question (a third fetch at G1 fits, 1,915 of 2,048 MB) is yours to settle, as the SP3 review said.
3. **The new-text limit (decision):** 7.52 of 8.00 MB. Either raise `NEW_TEXT_LIMIT_BYTES` and the plan text to 9 MB with a dated note (the gate's own alternative; I did not do it silently), or accept that the next review round and one `--all` pass will cross 8. The files that are large and cited, so not mine to delete: `wp03/stale_check_report.json` and `.md` (276 KB, a 19 Oct snapshot of a stale-check run), `wp03/tests.jsonl` (114 KB), `wp02/transcript.txt` (87 KB), `wp09/tests_all.jsonl` (105 KB). If you want those pruned, the citing reports must be reworded first.
4. **Disk:** the nested `<session scratchpad>/bpyenv/venv` (1,008 MB) looks redundant; about 11 GB of older scratch remains. Not touched.
5. **BUILD-STATUS items this closes or changes:** 21 (disk record and rebuild lines) closed; 20 (WP-10: the two wheel fetches on the ledger, the hash-pinned install, `test_cleanup.sh` in the quick suite) closed for those three parts, the four report corrections, per-run result files and the 19 Oct strings are still open; 14 (win_kit2 watch) closed by the 90 s limit; 19 (last sentence, one writer per verdict file) closed by `spikes/verdicts/`. The spikes quick area now runs about 28 s, not 15 s.
6. **Second writer on the template header:** the long italic header of `template.md` still lists per-spike update histories ("the SP3 row updated ... again after a second run"). That is shared prose now owned by you; I suggest cutting it to one line, since each row has its own date.
7. The three failures in section 4 are open; the two one-line fixes are in `w2c-c2-phone-wording.md`.
8. Files I created, untracked: `spikes/verdicts/` (8 files), `spikes/sp3_blender/ledger_row.py`, `spikes/sp3_blender/requirements-bpy.txt`, this report. The six files I deleted are all tracked, so `git status` shows them as deleted and unstaged (the four `build/evidence/wp11a/area_*_all.txt` files and `build/evidence/wp11b/tests_quick_only.jsonl` and `summary_quick_only.json`).
