# build/evidence/pc: derived PC evidence only

This folder holds the only form of the maker's PC data that may be filed in this public repository (build plan 4.16, D-26).
The raw reports stay with the maker and are pasted in chat only (4.4). Nothing in them is ever copied here.

What may be filed, and nothing else:

| File name | Made by | Schema | Holds |
|---|---|---|---|
| `pc_tier*.json` | `python3 -I scripts/windows_check.py --tier-json-out PATH RAW_REPORT` (the raw report is a scratch file outside the repo) | `win/schema/pc_tier.schema.json` | buckets and verdict words: GPU tier, VRAM bucket, RAM tier, disk tier, display class, ffmpeg version and binary SHA-256, Python and Git ok, Craft pin status. No CPU or GPU model, no driver, no exact size, no account count |
| `pc_chains*.json` | `python3 -I pipeline/validators/colour_patch.py --derive-from RAW --out DERIVED` | `pipeline/validators/pc_chains.schema.json` | ffmpeg version, binary SHA-256, chain names, worst errors, pass flags. No configure flags, no paths |

A bucketed `decisions/hardware.md` draft (`windows_check.py --hardware-md`) is placed where the ai-photo skill reads it, not here.

Checks (run by `bash tests/integration/run_tests.sh --quick`): every `.json` here validates against its schema, none holds a GPU, CPU or driver string of the synthetic fixtures in `tests/win/fixtures/`, and no file anywhere in the repo is named like a raw report (`pc_report*.json`, `colour_patch_pc*.json`, `maker-pc*.json`) outside those fixtures.
Orchestrator, not an agent, files into this folder after the maker has pasted a report. Until then the folder is empty apart from this note.
