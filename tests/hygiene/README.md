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
bash tests/hygiene/run_tests.sh --all       # about 2 min: + stale tests, lint tests, the acceptance commands on the real tree
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

Exit codes follow 4.3. `public_lint.py`: `0` clean, `1` a hygiene or theme finding, `2` identifying data found (or the pattern file is missing: fail closed, or bad usage, or the local deny list sits in the clone without being git-ignored), `3` not a git repository (use `--paths`). A finding prints the category, `file:line` and the first two characters of the hit plus asterisks, never the value.

- **`--paths` reads files inside the repository only.** A file or folder outside the clone (outside `--root`) is a usage error: the run prints `USAGE: a path given to --paths is outside the repository root (--root); run the lint from the clone, or pass --root` and exits `2`, with or without `--theme`. It used to scan nothing and exit `0`, which a script that reads only the exit code (`lj.ps1 close`) took for "clean". An absolute path inside the clone is fine. To check a file that lives elsewhere, copy it into the clone first (or pass the folder that holds it as `--root`).
- **The local deny list** (`scripts/public_lint.deny.local.txt`, the maker's real names, one per line, on the maker's machine only) must be git-ignored. Until `.gitignore` carries `scripts/public_lint.deny.local.txt` (or `*.local.*`) the default run and `--all` report `local_deny_file ... exists but is not git-ignored` and exit `2`, so `git add -A` cannot stage it unnoticed; the lint never reads that file's words into its output. (The `.gitignore` line is the orchestrator's to add; report F-6.)
- Both Python tools replace a character the console code page cannot print (an arrow, a dash) with `?` instead of stopping, so a Windows PowerShell capture or pipe still gets the verdict. Windows itself stays UNVERIFIED.

## Using the disk guard (4.9)

Any step that writes more than 100 MB (a download, an extraction, a venv, a render run, an export, an encode set) goes through it:

```bash
. scripts/lj_guard.sh
lj_with_disk 350 "WP-07 filmcraft lean" -- bash -c 'cd "$STAGE" && ./fetch_and_test.sh'
lj_bench node pipeline/bin/render.mjs ...   # a timed run that writes under 100 MB: no disk lock
```

- It takes `disk.lock` (waits up to 90 minutes, then `BUSY: held by <label>`), refuses unless `Avail - PLANNED >= 400 MB`, and watches `df` every 5 s while the command runs. Below **250 MB** it sends TERM to the command's whole process group (your cleanup trap runs), waits up to 20 s, runs `LJ_ON_ABORT` if you set it, and exits `3 DISK-FLOOR`. The lock is held until the cleanup has finished.
- A step that writes under 100 MB takes no disk lock (4.9): call `lj_bench` alone and record `df` in its envelope with `lj_df_avail_mb`. `lj_with_disk 0` is still refused whenever Avail is under 400 MB (verified: fake `df` 390 MB, planned 0, exit 3), which is intended for writes and a trap for timed runs. A timed step that also writes over 100 MB nests the other way round: `lj_with_disk N LABEL -- lj_bench CMD...` (disk first, then bench; the reverse is refused).
- The command may be an executable or a shell function. Your own `timeout` works: the TERM is forwarded to the command's group and the lock is released.
- One ledger line per run goes to `<scratch>/disk-ledger.jsonl` (label, planned, start, min, end, date): copy it into your evidence envelope (`lj_ledger_last LABEL`). The label is sanitised (no slash, no at sign), so no path or host can reach the ledger.
- `PLANNED_MB` is a whole number of MB, at most 12 digits (a longer number would wrap in bash arithmetic to a small one and let the stage run): anything else is a usage error, exit 2, and the command never starts. It is computed where possible (tarball size + `tar -tvzf` member sizes + the stills and exports the stage writes), not guessed.
- **At the time of writing the volume has about 480 MB free**, so the guard refuses any stage above roughly 80 MB. That is the guard doing its job; see the open questions Q-1 and Q-2 in the plan.

## What the tools cannot do

- `public_lint.py --theme` is a **keyword scan of text**. It cannot judge iconography. A person (and the Fable review) must look at every picture against D-28 (no Mughal or other Islamic motifs, no Christian motifs, deities with correct iconography). Existing playbooks, skills and research are reported as INFO only; a **new or changed** playbook (and `skills-staging/`, `ops/GATHER.md`, `pipeline/scenes/`, the phone test strings) is scanned on its added lines. The keywords are Mughal, Islamic, mosque, Taj Mahal, Red Fort, church, crucifix, Christmas, Christian, and (review r4) Easter, Eid, steeple, jali, arabesque, muezzin; `jali` is there because a lattice screen is mostly Mughal work but can be Rajput or temple work, so a person decides the origin and leaves it out when it is ambiguous. In a prose file (`.md`) a line that names a keyword **and** has an exclusion cue (no, never, not, excluded, avoid, forbidden, out of scope, left out, leave out, default out) within 40 characters **before** it is a statement of the rule and is printed as a NOTE to read, not as a finding. Anything else is a finding: a cue after the keyword ("Mughal garden, not too dark", "Christmas lights left out on the porch"), the animation words `out` and `without` ("fade out to a Taj Mahal silhouette", "a church without a steeple"), and every line under `pipeline/scenes/` or in `pipeline/phone/test_strings.json`, where every string is rendered and nothing is demoted.
- A masked finding still tells you the file and line; look at the line yourself, locally. Do not paste a flagged value into chat or a report.
- Everything here ran on Linux with PowerShell 7 for the `.ps1` consumer. **Windows PowerShell 5.1 and Windows itself are UNVERIFIED**: on the maker's PC, `py -3 -I scripts/public_lint.py --self-test` will use Windows PowerShell 5.1 if no `pwsh` is installed and says which one it used.
- `stale_check.py` finds the phrasings it knows. A row with zero hits is clean for those phrases, not proof that no reworded copy exists; rows S-02, S-34, S-36, S-44, S-48, S-52, S-56, S-60, S-64 and S-65 are only partly machine-checkable and S-53 not at all; the report says so ("Not machine-checkable"). A hit on a Table 4 row that a scribe already marked applied is a REGRESSION, and a hit whose line says the old value is retired is flagged as a retirement note but still listed: only the W-29 allowlist suppresses a hit, and only the orchestrator adds to it.

## Adding to the shared files

- `redaction_patterns.json` is frozen at version 1. Only WP-03 changes it, with a negative and a positive sample for whatever is added, and every change reruns `python3 -I scripts/public_lint.py --self-test` (the cross-consumer disagreement test) and `tests/hygiene/test_patterns.py`.
- `stale_allowlist.json` is **exactly** the W-29 allowlist. A new entry is an orchestrator decision, and `--audit-allowlist` fails on any entry that suppresses nothing, except one marked `"structural": true` with a `structural_reason`, which is printed as `unused by design` while it suppresses nothing on today's tree (AL-4: since `S-05.ring-1` became `\bRings? [12]\b`, `gathering 14` no longer hits; AL-2d, AL-2f and AL-5: W-29 names the context but no scanned line carries it today). The self-test and `test_stale.py` take the entry count from the file, so a new W-29 context is a JSON edit.
- `stale_patterns.json` keeps a copy of the Table 4 statuses (applied, applied today, outstanding). When Table 4 changes, change the row's `status` there (`status_table4` holds the register's own Status cell for the record). A pattern may choose the Table 4 row by file (`attribute`, for example the D-29 terms) or apply to some files only (`only_files`).
- When Table 4 grows, WP-03 adds the rows and their patterns in the same pass as the register edit and re-cuts the baseline (`python3 -I scripts/stale_check.py --baseline`) the same day, so the register and the check never drift; the self-test fails when a Table 4 id has no row (it reads `DECISIONS.md`, or the file given with `--register`), when a row's status disagrees with Table 4, and when the O-row pattern stops short of the register's last O-row.
- `public_lint.config.json` `allow` is deliberately short and only for public identifiers that are about no person or machine. E-mail addresses, creator handles and session ids are not allowed there.
