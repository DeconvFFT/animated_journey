# Fable review: package t3-limits-scratch, round 1

*Fable advisor, Tue 20 Oct 2026, branch `build/process-lock`. Reviewed: `build/reports/w2t-t3-limits-scratch.md`, the diffs of the files it names, and the regenerated `spikes/VERDICTS-W2.md`. Synthetic material only; nothing committed or pushed; nothing under `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited by the package or by me. Where this review says `<session scratchpad>`, the real folder carries the cloud session's id and stays out of this public repository (D-26).*

**Verdict: approve.** Scores: correctness 5, safety and privacy 5, maker usability 4, fidelity to plan 5, maintainability 4. Nothing critical is open. Five nudges, none blocking; the items only the orchestrator can do are in section 6.

## 1. What I re-ran myself (foreground, each under a timeout)

| Check | Result |
|---|---|
| `python3 -I spikes/sp1b_readback/check_ledger.py` | exit 0: 11 fetches, 5 of 5 pinned tarballs, **1506.9 MB of the 2560 MB allowance** |
| `tests/integration/run_checks.py --mode quick --only disk.each_tarball_downloaded_once,disk.downloads_under_2gb_allowance,hygiene.new_text_under_8mb` into a scratch evidence folder (the `_only` files; the mode's evidence untouched) | 3 PASS: 1,667 MB (decimal) against the 2560 MiB allowance; new text **7.63 MB in 631 files** (the other packages' reports and reviews landed since the report's 7.58) |
| `python3 -I spikes/verdicts/assemble.py check` | "exactly what the parts assemble to (73 lines)" |
| `python3 -I tests/spikes/check_verdicts.py` | 5 main rows, 6 SP1 test rows, complete |
| `bash tests/spikes/run_tests.sh --quick` | exit 0; the two edited assertions (`ledger.pip_rows_counted_and_held_to_the_rule`, `ledger.real_includes_pip_fetches`) PASS on 2560 |
| `bash tests/sp1/run_tests.sh --quick` | exit 0; `ledger.check` prints "allowance 2560 MB" read from `config.json` |
| `python3 -I scripts/public_lint.py --paths` over the 18 files the package touched plus its report | 0 identifying-data findings, 0 hygiene findings |
| `python3 -I scripts/stale_check.py --new-only` | 0 new FAIL, 0 new WARN |
| `git grep` for the session id and the `/tmp/claude-0` root over the tree and the untracked reports and reviews | nothing new (the three old WP-03 mentions of the generic scratch root are the ones `gate-r2.md` already cleared) |
| The two Whisper environments, opened with their own interpreters (`-B -I`, nothing installed) | `venv`: faster-whisper 1.2.1, ctranslate2 4.8.3, imports. `whisperenv_dir/venv`: openai-whisper 20250625, torch 2.14.1+cpu, imports, `cuda False`. `~/.cache/whisper` does not exist. All as the rows say |
| The SP4 dating evidence | `2fdbdb4` 01:57:24 UTC "before container restart"; `3a500dd` 03:39:09 UTC "before second container restart"; `uptime -s` 03:38:26 UTC. The row's "about 01:56" and "about 03:38" hold |
| `config.json` still parses; its `disk` consumers (`asset_tool.py` line 195, `run_sp1.sh` line 82, `stage_budget.py`) read named keys, so the added `download_allowance_note` key breaks nothing | confirmed by the two green suites above |

## 2. The arithmetic, recomputed

The margins the report, the plan and `template.md` quote are consistent once the unit is kept in mind (the ledger check counts MiB and prints "MB"; the integration test prints decimal MB and compares against MiB):

* Third `bpy` fetch: 428,225,665 bytes = 408.4 MiB. Ledgers 1,506.9 + 408.4 = **1,915.3 MiB**. Old allowance 2,048 MiB leaves 132.7 MiB ("133 MB in `check_ledger.py`"); new 2,560 MiB leaves 644.7 MiB ("about 645 MB to spare" in `template.md` step 3).
* Integration test: 1,667 MB decimal today + 428.2 MB = 2,095.5 MB decimal. Old limit 2,147.5 MB decimal leaves **52 MB**; new limit 2,684.4 MB decimal leaves **589 MB** (562 MiB). The report's figures, the plan's 4.9 note and the `run_checks.py` constant comment (about 1,998 MiB in all, 562 MiB to spare) all agree.
* The report's correction of its own first wording ("would have been stopped" became "left about 52 MB, so any other fetch would have stopped it") is the honest version; the plan carries the corrected form.

## 3. Item by item against the orchestrator's decisions

| Item | Done as decided | Notes |
|---|---|---|
| (a) new-text limit 8 to 9 MB, dated note | yes | constant, docstring, printed expectation, README row, `run_tests.sh` header and the plan's hygiene item 5 all carry the note (7.59 MB in 627 files; weeks 3 and 4; prune at 8.5 MB). The 8.5 MB trigger is advice in text, as the report says (nudge 2) |
| (b) allowance 2,048 to 2,560 MB, dated note wherever defined and documented | yes | the three homes (`config.json`, `check_ledger.py`, `run_checks.py`) each name the other two; the integration test now compares against the constant instead of a hard-coded `2 * 1024 ** 3` and prints its figure in the right unit; eleven text spots updated. `spikes/verdicts/SP1.md`'s "388.2 MB of the 2,048 MB allowance" is a dated record of that day and rightly left alone; `BUILD-STATUS.md` was correctly not edited (section 6) |
| (c) template header to one line | yes | the per-spike history is one clause; agrees with rule 3 of `spikes/verdicts/README.md`. `template.md` has one writer (the orchestrator); the implementor edited it on the orchestrator's explicit instruction for (c) and (d), which is the right reading |
| (d) kept-environment rows, checked before writing | yes | the task said "the per-spike row file"; the kept-environments table lives in `template.md` and `assemble.py` has no part for it, so putting the rows there is the only place they could go. Both environments were opened before the lines were written, and I opened them again. The faster-whisper row's new `ctranslate2==4.8.3` pin and the openai-whisper line are both marked not run; the openai-whisper row says the checkpoint fetch is UNVERIFIED and that a rebuild is not on the ledger. The sentence that resolves c3's confusion (the 2.1 GB Whisper environment is the openai-whisper one) is there |
| (e) SP4 observations | yes | dated, attributed to the orchestrator's sessions, kept apart from the verdict in three places (row, "does not say" bullet, `PROTOCOL.md` section), with the nearest table reading named as "killed" and the idle question left open. The five render-shard rules match what the harness actually does: `render.mjs` writes through `.tmp` and rename, skips finished frames and clears stale `.tmp` (lines 16 to 28, 480); SP2 `a4` proved SIGKILL-and-resume; `README-render.md` line 67 says video mode is one process with no `--shard`; the 10-minute figure is the ROADMAP's own (rows 119 and 345) and the protocol table's. No overnight run was started |
| assemble and quick checks | yes | `VERDICTS-W2.md` regenerated, not hand-edited; the full `--quick` run's only reds are the four `skills-staging` references, which `w2t-t1` and `w2t-t2` found first and which are not this package's |

The three things the report asked me to look at (section 5 item 8): the SP3 step-3 sentence matches the figures (section 2 above); both Whisper rows say "not run" and the preamble says every rebuild line is UNVERIFIED until run; the SP4 wording nowhere turns a restart into an idle-test result.

## 4. Scores

| Dimension | Score | Why |
|---|---|---|
| Correctness | 5 | every figure recomputed holds; every check re-run passes; the dating evidence and both environments confirmed |
| Safety and privacy | 5 | no session id or scratch root in the repo; lint clean; network use was four read-only listings, no wheel downloaded, nothing personal sent; nothing in the deliverables names a person |
| Maker usability | 4 | nothing here is maker-facing; the one wrinkle is that the regenerated evidence index now reads FAIL for a cause outside the package (section 6 item 1), which a reader of `INDEX.md` has to decode |
| Fidelity to plan | 5 | the five items done exactly as decided, nothing beyond them; the test-id rename, the status page and the overnight run correctly left to the orchestrator |
| Maintainability | 4 | one figure in three homes (cross-commented, not read from one source); the ledger check still prints "MB" for MiB; two test ids now carry stale names by a documented decision |

## 5. Nudges (none blocks the approval)

1. **Unit label in `check_ledger.py`.** It counts MiB and prints "MB" (line 124), and the prose now copies that ("1,915 MB", "645 MB to spare"). One word in the printed line ("MiB") would end the ambiguity the integration test already removed on its side; the two assertions in `tests/spikes/run_tests.sh` that grep the line would move with it.
2. **A soft line at the prune trigger.** `t_new_text` could print "near the 8.5 MB prune trigger" (still PASS) once `tot` passes 8.5 MB, so the trigger is read by the runner and not only by whoever reads the comment.
3. **`config.json` line 3** still says "nothing else holds these figures", untrue of `check_ledger.py` and `run_checks.py` for the allowance; delete the clause or point it at the new `download_allowance_note`.
4. **`template.md` step 3** now carries the old margins (52 and 133) and the new one (645) in one sentence; once the status page closes the allowance item, the old margins can live in the plan's 4.9 note alone.
5. **The report's "about 50 MiB" (run_checks comment) against "52 MB" elsewhere** are the same margin in two units; the comment says so, but a reader comparing files may stumble. Pick one unit per file where it can be done cheaply.

## 6. For the orchestrator (only you can do these)

1. **Evidence state before commit.** The package's final `--quick` run rewrote `build/evidence/INDEX.md` and the `wp11b` files: the index now records a 06:24 UTC run that reads **FAIL** (integration 38 PASS, 3 FAIL, 1 UNVERIFIED), the only cause being the four `skills-staging` references (`build/run_all_checks.sh` line 93, `tests/integration/make_evidence.sh` line 44, `BUILD_ROOTS` and the theme guard in `tests/integration/run_checks.py`, and `docs.staged_skill_update`). `BUILD-STATUS.md` still cites the 05:14 UTC PASS run. Either drop those references and re-run `--quick` before committing, or restore the 05:14 evidence; do not commit an index that says FAIL for a reason the status page does not name.
2. **`BUILD-STATUS.md`.** Close issue 5 (limit now 9 MB; 7.63 MB in 631 files at this review), change the WP-11b row's "of the 8 MB limit", the c3 row's "1,506.9 of 2,048 MB" and the SP3 row's "about 1,915 of 2,048 MB", and close the open G1 allowance item (section 6 item 6 of `w2c-gate-r1.md`).
3. **Test ids.** `hygiene.new_text_under_8mb` and `disk.downloads_under_2gb_allowance` keep their names by the implementor's documented choice. My recommendation: keep them until the week-3 evidence is regenerated anyway, then rename in that one pass (`hygiene.new_text_under_limit`, `disk.downloads_under_allowance`) and let the reviews cite the old names as history.
4. **ROADMAP rows 119 and 345** say "frames piped into ffmpeg in shards of ≤10 minutes". The built harness has no `--shard` in video mode (`README-render.md` line 67), and the new SP4 section rightly says PNG shard mode and `--encode`, never one piped video process. Reconcile the ROADMAP wording when you next touch it; the 10-minute figure itself stands.
5. **Register.** `DECISIONS.md` carries neither limit, so no register change is forced; if you want the two raises on the change log, one dated line each is enough.
6. **Scratch, still yours.** The openai-whisper environment (2.1 GB) is now a kept item with a row; the scratch `vendor/filmcraft` tree (76 MB), the nested `bpyenv/venv` (1,008 MB) and about 11 GB of older scratch still have no row or "droppable" line. The SP4 overnight run remains yours per `PROTOCOL.md`.

## 7. What this review does not say

* Nothing about whether either rebuild line installs today: neither was run, by the package or by me (a rebuild is a download).
* Nothing about the OpenAI checkpoint fetch from the container.
* Nothing about the cause of the two restarts, or about what the container does when idle: SP4 is still armed, not run.
* Nothing about Windows.
