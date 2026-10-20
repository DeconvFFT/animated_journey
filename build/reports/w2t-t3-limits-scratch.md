# Report: package t3-limits-scratch (week-2 close-out, small items)

*Sonnet implementor, Tue 20 Oct 2026, branch `build/process-lock`. Synthetic material only; nothing committed or pushed; nothing under `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited. Where this report says `<session scratchpad>`, the real folder has the cloud session's id in its path; that path stays out of this public repo.*

Source: the orchestrator's decisions after `reviews/build/w2c-gate-r1.md` (section 6, items 4 and 6) and `reviews/build/w2c-c3-evidence-verdicts-r1.md` (nudge 1, section 9). Five items, (a) to (e) below.

## 1. What changed

| Item | Files | What |
|---|---|---|
| (a) new-text limit 8 to 9 MB | `tests/integration/run_checks.py` (`NEW_TEXT_LIMIT_BYTES`, docstring, the check's expectation text), `tests/integration/README.md`, `tests/integration/run_tests.sh` (header), `build/BUILD-PLAN-W1-2.md` (acceptance item 5 of the hygiene line) | Limit is 9,000,000 bytes. Dated note (2026-10-20): measured 7.59 MB in 627 files; the review rounds of weeks 3 and 4 will add more; prune duplicate evidence first if it reaches 8.5 MB. The note is in the code comment, in the check's expectation text (so it prints), in the README row and in the plan. The 8.5 MB trigger is advice in text; nothing warns at 8.5 automatically. |
| (b) download allowance 2,048 to 2,560 MB | `spikes/sp1_craft_cli/config.json` (`download_allowance_mb`, plus a `download_allowance_note` key), `spikes/sp1b_readback/check_ledger.py` (`ALLOWANCE_MB`), `tests/integration/run_checks.py` (new `DOWNLOAD_ALLOWANCE_MB`, the comparison, the printed figure, the docstring), `tests/spikes/run_tests.sh` (5 spots: three `2048` texts, the `m < 2048` bound and one label), `tests/sp1/run_tests.sh` (a label), `spikes/sp1_craft_cli/run_sp1.sh`, `drivers/asset_tool.py`, `FALLBACK.md` (wording; the numbers they print come from `config.json`), `spikes/sp3_blender/run_sp3.sh` (2 messages), `spikes/sp3_blender/README.md`, `build/BUILD-PLAN-W1-2.md` (4.9, the ledger heading, C-10), `spikes/verdicts/template.md` (SP3 step 3) | 2,560 MB is 2.5 GiB, in MiB as the ledger check counts. Dated note 2026-10-20 in each place that defines it. The integration test now prints its figure in the right unit ("against the 2560 MiB allowance (2684354560 bytes; 1017 MB to spare)"); it used to print decimal MB against a hard-coded "2048 MB". |
| (c) template header | `spikes/verdicts/template.md` | The italic header's two sentences of per-spike update history are one clause: "each row carries its own date, and the report it cites says what changed." The header keeps its other sentences. |
| (d) kept environments | `spikes/verdicts/template.md` (the kept-environments table and the sentence above it; step 1 of the disk table names which Whisper environment) | A row for `<session scratchpad>/whisperenv_dir/venv` (openai-whisper 20250625, torch 2.14.1+cpu) with a one-line rebuild; the faster-whisper `venv` row is renamed, rechecked and its rebuild line pins `ctranslate2==4.8.3`. See 2.4. The table is in `template.md`, not in a per-spike file (`assemble.py` has no part for it, and the orchestrator's item (c) already names `template.md`). |
| (e) SP4 observations | `spikes/verdicts/SP4.md` (row, date 2026-10-20, "does not say" bullet), `spikes/sp4_idle/PROTOCOL.md` (new section "Observations while the test is still not run") | Dated observations, kept apart from the verdict, and what they mean for render shards. See 2.5. No overnight run was started. |
| generated | `spikes/VERDICTS-W2.md` | Regenerated with `python3 -I spikes/verdicts/assemble.py`, never edited by hand. |

## 2. What was done, with the commands and results

### 2.1 The limits (a) and (b)

* `python3 -I spikes/sp1b_readback/check_ledger.py` now reads **1506.9 of 2560 MB**, exit 0.
* A third `bpy` fetch, simulated on a scratch copy of the ledger (`ledger_row.py append --ledger <copy>`; the real ledger file is unchanged): `check_ledger.py` reads **1915.3 of 2560 MB, exit 0**. The pre-edit copy of the script also passes on that copy (1915.3 of 2048), so the old guard did not stop G1 outright. What the raise buys is margin: measured against the real ledgers, a third fetch plus PowerShell, npm packs and the OTIO wheel is 2,095.5 MB decimal. Against the old 2,048 MiB that left about **52 MB** in the integration test (133 MB in `check_ledger.py`), so any other fetch (the 70 MB FilmCraft fallback, a PowerShell re-fetch) would have stopped the Sun 15 Nov run. Against 2,560 it leaves about **589 MB** (562 MiB). The first wording I wrote in the plan ("would have been stopped") was too strong; I corrected it to these figures.
* `python3 -I tests/integration/run_checks.py --mode quick --only disk.each_tarball_downloaded_once,disk.downloads_under_2gb_allowance,hygiene.new_text_under_8mb` (into a scratch evidence folder): 3 PASS. The new-text check read 7.56 MB in 626 files then, 7.58 MB in 628 files in the full run below.
* `bash tests/spikes/run_tests.sh --quick`: 42 PASS, 0 FAIL, 1 UNVERIFIED (Windows). `bash tests/sp1/run_tests.sh --quick`: 15 PASS, 0 FAIL, 1 UNVERIFIED. These contain the edited assertions (`ledger.pip_rows_counted_and_held_to_the_rule`, `ledger.real_includes_pip_fetches`).
* **Test ids kept.** `hygiene.new_text_under_8mb` and `disk.downloads_under_2gb_allowance` keep their old names: the evidence, `INDEX.md`, the readiness map and four reviews cite them. The figure is in the check text, and a comment at each constant says so. Renaming is a decision for the orchestrator (section 5, item 1).

### 2.2 (c) The header

Before: two sentences of dated history (the SP3 row "updated Tue 20 Oct ... again after a second run", the SP1 row "updated ... after the `T2.mid_dissolve` ruling and the one FilmCraft 0.9.0 re-run") with three report paths. After: "each row carries its own date, and the report it cites says what changed." This agrees with rule 3 of `spikes/verdicts/README.md` (no update history in the header).

### 2.3 Assembly and verdict checks

* `python3 -I spikes/verdicts/assemble.py` wrote 73 lines; `assemble.py check`: exactly what the parts assemble to.
* `python3 -I tests/spikes/check_verdicts.py`: 5 main rows, 6 SP1 test rows, complete (the SP4 date cell is a bare `2026-10-20`, as the checker requires).
* `python3 -I scripts/public_lint.py --paths` over the changed folders and files: 27 files, 0 findings. No session id or scratch path was written into the repo by this package.

### 2.4 (d) The two Whisper environments, checked before the lines were written

Real folder: `<session scratchpad>/venv` and `<session scratchpad>/whisperenv_dir/venv`. Opened with their own interpreters, bytecode writing off (`-B -I`), nothing installed or changed.

| | `venv` (461 MB, `du`) | `whisperenv_dir/venv` (2,090 MB for `whisperenv_dir`) |
|---|---|---|
| Python | 3.13.16 | 3.13.16 |
| Packages (from `importlib.metadata`) | faster-whisper 1.2.1, ctranslate2 4.8.3, onnxruntime 1.31.0, av 19.0.1, tokenizers 0.23.3, huggingface_hub 2.2.0, numpy 2.5.4 | openai-whisper 20250625, torch 2.14.1+cpu, numba 0.68.0, tiktoken 0.14.0, triton 3.8.0, numpy 2.5.4 |
| Import | `import faster_whisper, ctranslate2` prints 1.2.1 and 4.8.3 | `import whisper, torch` works; `torch.cuda.is_available()` is False |
| Biggest parts | ctranslate2 + libs, onnxruntime, av.libs | triton 897 MB, torch 769 MB, llvmlite 173 MB |
| Weights | none in it; the Systran `base` and `small` models are in the Hugging Face cache (605 MB, outside the repo) | none, and none on the disk (`~/.cache/whisper` does not exist) |
| Rebuild line written | `python3.13 -m venv <dir> && <dir>/bin/python -m pip install faster-whisper==1.2.1 ctranslate2==4.8.3` | `python3.13 -m venv <dir> && <dir>/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.14.1 && <dir>/bin/python -m pip install openai-whisper==20250625` |

How the second line was chosen: the CPU torch goes first, as on 18 Oct (`pip_torch.log` and `pip_whisper.log` in that folder both end `rc=0`, torch then whisper), so pip does not take the CUDA build from PyPI. Without installing anything I checked three facts with small requests: the CPU index page lists `torch-2.14.1+cpu` for cp313 manylinux x86_64 (HEAD request: 196,253,851 bytes, 187 MiB); PyPI lists triton 3.8.0 for cp313 x86_64 at 247,975,122 bytes; `openai-whisper` 20250625 is a source-only package (803 KB) whose requirements are more-itertools, numba, numpy, tiktoken, torch, tqdm and triton. The row says all of this, says the line was not run, and says the installs are not hash-pinned and not on the download ledger, so a rebuild should be weighed against the allowance first. The row also states the disk-decision prose's "Whisper environment of 2.1 GB" is this one, which answers the c3 review's confusion between the two.

### 2.5 (e) SP4 observations

What I could check from the repo and the machine:

* Checkpoint commits `2fdbdb4` (Tue 20 Oct 01:57, "WIP checkpoint: week-2 sweep and spikes before container restart") and `3a500dd` (03:39, "...before second container restart"); `w2-sp3-r1.md` dates the first restart "about 01:56 UTC" and `w2-sp3.md` records the different CPU model after it; `uptime -s` on the running container reads 03:38 UTC, so the second restart was at about 03:38.
* The kept environments (created 18 Oct) are still in the scratchpad, so the disk survived both.

What is taken from the orchestrator's account and cannot be checked from files: that the workflows and detached background jobs were lost at each restart, and that work resumed from the committed checkpoints. They are recorded as observations, attributed to the orchestrator's sessions.

The record (SP4 row, the "does not say" bullet and `PROTOCOL.md`) says plainly that these are not the SP4 verdict: the sessions were active, not idle; the cause is unknown; the nearest reading in the protocol's table is "killed", with the same consequence (long jobs restartable from files on disk); whether a running job keeps an idle container awake is still open. Container lifetimes seen: about 1 h 40 min and at least 2 h 19 min (still running at 05:57 UTC), two points and no pattern.

For render shards the section states: (1) short shards, 10 minutes or less; (2) resumable frames, PNG shard mode (`render.mjs` writes `.tmp` and renames, clears stale `.tmp`, re-renders incomplete PNGs; SP2 `a4` proved kill-and-resume), never one long piped video process, which cannot resume (`pipeline/bin/README-render.md`); (3) the shard plan, commands and progress in committed text files, finished renders copied out because a reclaimed container may start empty; (4) a WIP commit before any run longer than a shard; (5) time a shard on the host it will run on, since SP3 run 2 was 1.96 to 2.06 times slower after the first restart. No overnight run was started.

### 2.6 The final quick run

`bash /home/user/animated_journey/build/run_all_checks.sh --quick`, foreground, started 06:18:59 UTC after waiting for other packages' runs to finish (the runner allows one run at a time; my first attempt at 06:00:52 printed BUSY for Part B and is not counted): **exit 1, 335 s**. Part A 13 PASS, 1 FAIL; Part B 12 of 13 areas PASS, `integration` FAIL (38 PASS, 3 FAIL, 1 UNVERIFIED). Every FAIL has one cause, and it is not this package: **`skills-staging/` no longer exists** (the orchestrator installed the staged skills and removed the folder), but `lint.build_folders` (`build/run_all_checks.sh` line 93), `hygiene.public_lint_over_the_build_folders`, `hygiene.theme_guard` and `docs.staged_skill_update` (all in `tests/integration/run_checks.py`) still name it. `w2t-t1-saturday-guide.md` and `w2t-t2-wording.md` found the same four failures and left them alone for the same reason. The checks this package changed pass in that run: `disk.each_tarball_downloaded_once` (1506.9 of 2560 MB), `disk.downloads_under_2gb_allowance` (1,667 MB decimal against 2560 MiB, 1,017 MB to spare), `hygiene.new_text_under_8mb` (7.58 MB in 628 files), `verdicts.assembled`, `verdicts.complete`, and the `spikes` and `sp1` areas (PASS; the "2 FAIL" and "4 FAIL" envelope counts in the summary are the recorded real results of the Craft tests, such as `T2.mid_dissolve` on 0.8.0 and the LightCraft and VectorCraft read-backs, already in the evidence, not new). The run rewrote the usual generated files under `build/evidence/`, as it always does.

## 3. UNVERIFIED

* **Both rebuild lines were not run** (a rebuild is a download, and nothing needed rebuilding). The faster-whisper line adds the `ctranslate2==4.8.3` pin, which is new and untested. For the openai-whisper line, what was checked is that the pinned CPU torch wheel exists on the index and the two largest wheel sizes; the sizes of the other dependencies, the total download, and whether the install completes today are not known.
* Whether the OpenAI checkpoint download works from the container (`~/.cache/whisper` does not exist; no fetch was tried).
* The SP4 facts that come from the orchestrator's account (jobs lost at each restart; work resumed from the checkpoints), and the exact restart minutes (about 01:56 and about 03:38 UTC).
* G1's third fetch was simulated on a scratch copy of the ledger only; no wheel was downloaded.
* Nothing here concerns Windows.

## 4. Notes on method

Network use: one 414 KB index page (`download.pytorch.org/whl/cpu/torch/`), one HEAD request for a wheel, and two PyPI JSON reads, all listings, no wheel downloaded and nothing personal sent. Scratch files (backups for diffing, the simulation ledger, the run output) are in the session scratchpad.

## 5. For the orchestrator

1. **Test ids.** `hygiene.new_text_under_8mb` and `disk.downloads_under_2gb_allowance` now check 9 MB and 2,560 MiB under their old names. Renaming (for example `hygiene.new_text_under_limit`, `disk.downloads_under_allowance`) touches `run_checks.py`, the README, `INDEX.md`, the readiness map and the generated evidence, and the four reviews that cite them could not follow. I kept the names; say if you want them changed.
2. **One figure, three homes.** The allowance lives in `spikes/sp1_craft_cli/config.json`, `spikes/sp1b_readback/check_ledger.py` and `tests/integration/run_checks.py`; each carries a comment naming the other two. `config.json` says "nothing else holds these figures", which was already untrue of `check_ledger.py`. Reading one from the other would remove the drift risk; I did not refactor.
3. **Status page.** `build/BUILD-STATUS.md` still has issue 5 ("New text against the limit", open, "decide before the next review round"), the c3 row ("1,506.9 of 2,048 MB") and the open G1 allowance item; they can close or change now. I did not edit it (not in this package). `spikes/verdicts/SP1.md` keeps its dated line "388.2 MB of the 2,048 MB allowance", which was true on the day; `check_ledger.py` now prints 2560.
4. **The `skills-staging` red (section 2.6).** Drop `skills-staging` from `build/run_all_checks.sh` line 93, from `tests/integration/make_evidence.sh` line 44 and from `BUILD_ROOTS` in `tests/integration/run_checks.py`; make the theme guard's staged-skills part skip when the folder is missing; retire or retarget `docs.staged_skill_update`. Until then `--quick` exits 1 for every package.
5. **New-text headroom.** 7.58 MB before this report; this report and the next review add about 20 to 50 KB each. The 9 MB limit leaves about 1.4 MB; the prune trigger is 8.5 MB.
6. **Scratch, still yours.** The scratch `vendor/filmcraft` source tree (76 MB) from c3's nudge 1 still has no row or "droppable" line; the nested `bpyenv/venv` (1,008 MB, the same `bpy`) and about 11 GB of older scratch are untouched. The openai-whisper environment is now a kept item (2.1 GB); if you decide later that only the faster-whisper route stays, delete its row and the folder together.
7. **SP4.** The overnight run is still the orchestrator's, per `spikes/sp4_idle/PROTOCOL.md`. The new section lets the render-shard rules be quoted from there when the week-3 shard plan is written.
8. **Fable's read** is needed before this counts as done (D-32). Worth checking: that the SP3 step-3 sentence in `template.md` (it now carries the new allowance and the 52 MB and 133 MB margins of the old one) matches the figures in 2.1; that the Whisper rows say "not run" where they must; and that the SP4 wording never turns a restart into an idle-test result.
