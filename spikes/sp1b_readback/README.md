# SP1b: PhotoCraft, VectorCraft, LightCraft (T1 and read-backs) and FilmCraft (T3), on their Linux CLIs

*WP-10, Mon 19 Oct 2026. **Every result here is a Linux CLI result; it is not evidence for Windows.** The maker's Sat 24 Oct five-minute tests are the Windows evidence.*

## What it does

One disk stage per app (`scripts/lj_guard.sh`, `lj_with_disk`), in this order: FilmCraft first (it deletes the tarball WP-07 kept, about 67 MB, so the next three have more room), then PhotoCraft, VectorCraft, LightCraft.

| App | Source | Tests |
|---|---|---|
| FilmCraft 0.9.0 | the verified tarball WP-07 kept in `vendor/craft/_keep/` (SHA-256 re-checked; if it is missing or corrupt, **one** re-fetch with a recorded ledger exception) | **T3**, `drivers/t3_filmcraft.py`: import the WP-06 OTIO plain and with `metadata.filmcraft`; `inspect sequence`; export OTIO, FCP7 XML, FCPXML and EDL through `file.exportInterchange`; re-import each and diff; motion keyframes only with the metadata; relative media; `xmllint`; a bare FCPXML `<video>` |
| PhotoCraft 0.10.0 | one download (83,037,328 bytes) | **T1** and `info`/`convert` on the WP-06 ORA and on `at-layers.ora`, layer names compared with `stack.xml` through PNG, ORA and PSD |
| VectorCraft 0.13.1 | one download (124,613,940 bytes) | **T1** and `convert` of the WP-06 rig and `at-rig.svg`, then the reused `check_ids.py` (and WP-06's gate around it), a per-element diff, the PNG and PDF export |
| LightCraft 0.9.1 | one download (108,938,717 bytes) | **T1** and `render` of a synthetic JPEG with `LIGHTCRAFT_GPU=0`, the `faded-print-a.lcpreset` import (exact id kept), the reused `at-lightcraft-steps.jsonl` with this folder's paths, JPEG and 16-bit TIFF exports |

Inside a stage: `curl` into a new empty folder under `vendor/craft-sp1b/` -> SHA-256 against `spikes/sp1_craft_cli/release_assets.json` (a mismatch stops: nothing is extracted) -> `tar -tvzf` (a listing
writes nothing) -> the exact need (CLI member + outputs) against live Avail -> `tar -xzf` of the **one member** the CLI is -> the tarball is deleted -> the tests while the tree is on disk -> the tree is deleted.
The binary runs by absolute path, `env -i` with a throw-away `HOME`, `timeout`, `unshare -rn` when it works, and a 10 GB resident-memory watchdog. All inputs are synthetic (the WP-06 emitters and the reused fixtures).

## Disk: a mechanism, not a rule

The planned MB is computed (`drivers/stage_budget.py`): tarball + CLI member + 30 MB of outputs. The tarball size comes from `release_assets.json`; the CLI size from the listing (exact for FilmCraft, whose tarball is on
disk; assumed 1.15 x the tarball for the other three until their listing exists; **measured afterwards: 0.81, 0.80 and 0.95**, so the assumption held with 21% to spare). The guard refuses unless Avail minus planned stays at or above 400 MB and stops the stage
under 250 MB. A refused stage ends **BLOCKED**, not failed, with the guard's exact message and the remedy (answer Q-1, or move the read-back to the maker's PC). Nothing is forced. A 0.25 s sampler inside the stage
keeps the minimum Avail, because the guard polls every 5 s and a 13-second stage can fall between two polls.

## Run it

```bash
bash spikes/sp1b_readback/run_sp1b.sh --list              # sizes from release_assets.json, df, the stage plan; exit 3 if any stage's Avail minus planned is under 400 MB
bash spikes/sp1b_readback/run_sp1b.sh --all               # the four stages; a stage that already ran is NOT run again (its tarball is gone); exit 0 all PASS, 1 a finding or a harness problem, 3 BLOCKED only
bash spikes/sp1b_readback/run_sp1b.sh --only vectorcraft  # one stage;  --again runs a stage that already ran and records the ledger exception
python3 -I spikes/sp1b_readback/check_ledger.py           # each of the five tarballs fetched once; exceptions listed with their reason (--require-all: an unfetched one is a failure)
bash tests/spikes/run_tests.sh --quick                    # about 15 s, no downloads
bash tests/spikes/run_tests.sh --all                      # about 3 minutes: adds the 60 s SP4 run, the real --all (re-runnable) and the mechanism tests against a local fake release server
```

Exit codes follow build plan 4.3. Evidence goes to `build/evidence/wp10/` (see its `README.md`): `t1_<app>_<tag>.json`, `readback_<app>_<tag>.json`, `t3_filmcraft_<tag>.json`, `stage_<app>-<tag>.json`
(with the guard's start, minimum and end Avail), `download_ledger.jsonl`, `tests.jsonl`.

## Criteria and findings

A **criterion** (`checks[]`) is a pass mark: the playbook's five-minute test, the R8 T3 expectation, or a mechanism check. A **finding** (`findings[]`) is a measured fact the pipeline needs (what a format drops or rewrites);
it never fails a run. A stage is PASS when every criterion passes, FAIL when one fails (a finding about the app), UNVERIFIED when the harness itself could not drive the CLI (exit 2, not a verdict), BLOCKED when the
disk guard, the lock, the download or the exact need after the download stopped it.

## Files

`run_sp1b.sh` (the stages), `config.json` (the numbers), `check_ledger.py`, `drivers/` (`sp1b_lib.py` on top of the WP-07 `sp1_lib.py`, `stage_budget.py`, `finalize_stage.py`, `t1_visual.py`, `readback.py`,
`visual_app.py`, `t3_filmcraft.py`). Reused unchanged: `spikes/sp1_craft_cli/drivers/asset_tool.py` (HEAD, get, verify, ledger), `research/craft-visual-fixtures/{check_ids.py,at-layers.ora,at-rig.svg,faded-print-a.lcpreset,at-lightcraft-steps.jsonl}`,
and the WP-06 tools `emit_ora_layers.py`, `svg_rig.py`, `emit_otio.py`, `validate_otio.py`, `validate_ora.py`.

## UNVERIFIED

Everything about Windows. Whether the apps' windows, graphics drivers or the PC's behaviour match. The stand-in CLIs of `tests/spikes/fake_craft/` are not the apps and prove only that the harness measures, fails and cleans up
as described. A one-evening behaviour (SP4) and a bpy run (SP3) are not covered here.
