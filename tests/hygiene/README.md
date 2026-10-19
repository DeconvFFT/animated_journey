# Hygiene tools and tests (WP-03)

Shared checks that every other package leans on. One owner (WP-03); everyone else reads them through the frozen interfaces in `build/BUILD-PLAN-W1-2.md` section 4 (4.9 guard, 4.13 redaction patterns). The repository is **public** (D-26): these tools exist so that nothing identifying, personal or stale reaches it.

## What is here

| Tool | What it is for | Run it |
|---|---|---|
| `scripts/redaction_patterns.json` | The **one** definition of "identifying data" (4.13). Read by `scripts/windows_check.py`, `win/step0_pc_tests.ps1`, `win/kit2/run_checks_pc.ps1` (when it lands), `scripts/public_lint.py` and `scripts/ops_lint.py`. No other file carries its own copy of these expressions. | `python3 -I tests/hygiene/test_patterns.py` |
| `scripts/lj_guard.sh` | The disk and timing guard (4.9): `lj_with_disk PLANNED_MB LABEL -- CMD...`, `lj_bench CMD...`, `lj_df_avail_mb`. | `. scripts/lj_guard.sh` or `bash scripts/lj_guard.sh with_disk 350 LABEL -- CMD...` |
| `scripts/stale_check.py` (+ `stale_patterns.json`, `stale_allowlist.json`, `stale_baseline.json`) | The W-29 stale-copy check against Table 4 of `DECISIONS.md`. Read-only: it reports, it fixes nothing. | `python3 -I scripts/stale_check.py` |
| `scripts/public_lint.py` (+ `public_lint.config.json`) | "Is it safe to publish this?" Identifying data (the 4.13 categories only), binary files, files over 1 MB, ignored-but-staged media, raw PC report file names, the local deny list, and the D-28 theme guard. | `python3 -I scripts/public_lint.py` |

## Run the tests

```
bash tests/hygiene/run_tests.sh --quick     # about 30 s: pattern test, guard tests, both self-tests
bash tests/hygiene/run_tests.sh --all       # about 1 min: + stale tests, lint tests, the acceptance commands on the real tree
bash tests/hygiene/acceptance_transcript.sh # the plan's acceptance commands verbatim; writes the stale report and baseline
```

Every test prints `RESULT PASS|FAIL name :: detail`. `--all` writes `build/evidence/wp03/tests.jsonl` (one `lj-evidence/1` envelope per test, disk figures in each), `summary.json` and `unverified.txt`.

## Before every commit

```
python3 -I scripts/public_lint.py                 # added lines of the diff against HEAD + untracked files
python3 -I scripts/public_lint.py --paths <your owned paths>      # definition of done, item 2
python3 -I scripts/stale_check.py --new-only      # no NEW stale line (until the Haiku passes land)
python3 -I scripts/public_lint.py --theme         # new theme-bearing files against the D-28 exclusions
```

Exit codes follow 4.3. `public_lint.py`: `0` clean, `1` a hygiene or theme finding, `2` identifying data found (or the pattern file is missing: fail closed), `3` not a git repository (use `--paths`). A finding prints the category, `file:line` and the first two characters of the hit plus asterisks, never the value.

## Using the disk guard (4.9)

Any step that writes more than 100 MB (a download, an extraction, a venv, a render run, an export, an encode set) goes through it:

```bash
. scripts/lj_guard.sh
lj_with_disk 350 "WP-07 filmcraft lean" -- bash -c 'cd "$STAGE" && ./fetch_and_test.sh'
lj_with_disk 0 "WP-04 speed marks" -- lj_bench node pipeline/bin/render.mjs ...   # disk first, then bench; never the reverse
```

- It takes `disk.lock` (waits up to 90 minutes, then `BUSY: held by <label>`), refuses unless `Avail - PLANNED >= 400 MB`, and watches `df` every 5 s while the command runs. Below **250 MB** it sends TERM to the command's whole process group (your cleanup trap runs), waits up to 20 s, runs `LJ_ON_ABORT` if you set it, and exits `3 DISK-FLOOR`. The lock is held until the cleanup has finished.
- The command may be an executable or a shell function. Your own `timeout` works: the TERM is forwarded to the command's group and the lock is released.
- One ledger line per run goes to `<scratch>/disk-ledger.jsonl` (label, planned, start, min, end, date): copy it into your evidence envelope (`lj_ledger_last LABEL`). The label is sanitised (no slash, no at sign), so no path or host can reach the ledger.
- `PLANNED_MB` is computed where possible (tarball size + `tar -tvzf` member sizes + the stills and exports the stage writes), not guessed.
- **At the time of writing the volume has about 480 MB free**, so the guard refuses any stage above roughly 80 MB. That is the guard doing its job; see the open questions Q-1 and Q-2 in the plan.

## What the tools cannot do

- `public_lint.py --theme` is a **keyword scan of text**. It cannot judge iconography. A person (and the Fable review) must look at every picture against D-28 (no Mughal or other Islamic motifs, no Christian motifs, deities with correct iconography). Existing playbooks and research are reported as INFO only. A line that names a keyword **and** says it is excluded (no, never, excluded, out, avoid, without) is a statement of the rule and is printed as a NOTE to read, not as a finding; "Mughal garden, not too dark" is still a finding.
- A masked finding still tells you the file and line; look at the line yourself, locally. Do not paste a flagged value into chat or a report.
- Everything here ran on Linux with PowerShell 7 for the `.ps1` consumer. **Windows PowerShell 5.1 and Windows itself are UNVERIFIED**: on the maker's PC, `py -3 -I scripts/public_lint.py --self-test` will use Windows PowerShell 5.1 if no `pwsh` is installed and says which one it used.
- `stale_check.py` finds the phrasings it knows. A row with zero hits is clean for those phrases, not proof that no reworded copy exists; rows S-02, S-34 and S-36 are only partly machine-checkable and say so in the report.

## Adding to the shared files

- `redaction_patterns.json` is frozen at version 1. Only WP-03 changes it, with a negative and a positive sample for whatever is added, and every change reruns `python3 -I scripts/public_lint.py --self-test` (the cross-consumer disagreement test) and `tests/hygiene/test_patterns.py`.
- `stale_allowlist.json` is **exactly** the W-29 allowlist. A new entry is an orchestrator decision, and `--audit-allowlist` fails on any entry that suppresses nothing.
- `stale_patterns.json` keeps a copy of the Table 4 statuses (applied, applied today, outstanding). When Table 4 changes, change the row's `status` there; `--self-test` checks that every row S-01 to S-41 and W-29 is present.
- `public_lint.config.json` `allow` is deliberately short and only for public identifiers that are about no person or machine. E-mail addresses, creator handles and session ids are not allowed there.
