# Spike verdicts, wave 2 (SP1 to SP5)

*WP-10, Mon 19 Oct 2026, branch `build/process-lock`; the SP3 row updated Tue 20 Oct 2026 after its first real run and again after a second run the same night (`build/reports/w2-sp3.md`). The SP1 row and its T2 and T4 lines updated Tue 20 Oct 2026 after their first real run (`build/reports/w2-sp1-t2t4.md`) and again the same day after the `T2.mid_dissolve` ruling and the one FilmCraft 0.9.0 re-run (`build/reports/w2c-c1-filmcraft-dissolve.md`). One row per spike, with status, evidence, justification, next step and date. The decision rules are quoted from the files that state
them, not reworded. Fable reads this at the P-LOCK process lock, Sat 14 Nov (W-06).*

**Every Craft result below is a Linux CLI result; it is not evidence for Windows.** The maker's Sat 24 Oct five-minute tests (`spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md`) are the Windows
evidence. **Status words:** *Done* (the spike ran to a verdict on the container side), *Partial* (some of it ran, the rest is named), *Deferred* (justified, with the condition that ends the deferral),
*Not run* (not run, with the reason). Nothing counts as done until `fable-advisor` approves it.

## The five spikes

| SP | What it decides | Status | Evidence | Justification | Next step | Date |
|---|---|---|---|---|---|---|
<!-- insert: rows -->

**Decision rules, quoted.**
<!-- insert: rules -->
* All five, `playbooks/agent-pipeline.md` Step 3: "A route that fails its spike is dropped, or moved to the PC. Do not argue with the result."

## SP1, tests T1 to T6 one by one

| Test | Status | Evidence | Justification | Next step | Date |
|---|---|---|---|---|---|
<!-- insert: tests -->

## Disk decision (gate review r1, nudge 3; chosen Tue 20 Oct 2026)

**Choice: free the space in the container. SP3 does not move to the PC.** The reasons: (1) SP3's question is whether Blender is a usable hero-shot route *in the container*; a run on the maker's PC answers a different question (Exercise 5, the PC's own timing), so moving it would leave the container question open. (2) Space is not scarce in fact: the volume shows 749 MB free, but about 25 GB of it is working folders left by the earlier Learn-phase session in its scratch area outside the repository (the largest: a Whisper environment of 2.1 GB, a Blender Python environment of 2.0 GB, benchmark outputs of 1.8 GB, two more Python environments of 1.8 and 1.3 GB, a test folder of 1.2 GB, a Blender Linux download of 1.2 GB; about 6 GB are Blender downloads and environments alone, and about 21 GB look regenerable). Only the orchestrator owns that area, so **nothing was deleted by this step**; it is a list for the orchestrator to prune, keeping the Whisper environment until the week-3 local-Whisper route is built. (3) Waiting for the PC would put SP3 into her Diwali week.

| Step | What | Needs (free) | By | If it does not happen |
|---|---|---|---|---|
| 1 | The orchestrator frees at least 4,000 MB on the shared volume (prune the earlier session's scratch; do not run `cleanup_scratch.sh --yes` yet, it removes the PowerShell the `win*` areas need). **Done Tue 20 Oct (orchestrator): about 14 GB of regenerable Learn-phase scratch freed; about 15 GB free; kept the bpy 5.2.2 environment (`<session scratchpad>/bpyenv`), the Whisper environment (`<session scratchpad>/venv`), `vendor/` and the FilmCraft downloads (`<session scratchpad>/fc_dl`); about 11 GB of older scratch remains in that session scratchpad** (`<session scratchpad>` is the cloud session's scratch folder; its full path carries a session id, which stays out of this public repo; one line to rebuild each kept environment is under the table) | n/a | Wed 21 Oct | go to the fallback row |
| 2 | SP1 T2 and T4: `bash spikes/sp1_craft_cli/run_sp1.sh --all --profile lean`, then `python3 -I spikes/sp1_craft_cli/drivers/verdict.py`; rewrite the T2 and T4 rows above and apply the R8 rule **Done Tue 20 Oct, in the container, after the orchestrator freed the space** (Avail 14,547 MB before, 14,545 MB after, lowest 13,294 MB seen with SP3 running alongside; T2 FAIL on its first wording, T4 PASS; `build/reports/w2-sp1-t2t4.md`; T2 re-run the same day after the mark amendment: PASS, `build/reports/w2c-c1-filmcraft-dissolve.md`) | 767 MB (two lean stages with the FilmCraft tarball kept: 350 + 400, then 300 + 400 + 67); the full profile would need 1,000 | **Fri 23 Oct, the R8 decision date** (before the maker's Sat 24 Oct tests and the Sun 25 Oct pin freeze) | R8 stays undecided and the plan's default stands (FilmCraft stays maker-side, the container renders with ffmpeg, Pillow and Chromium); the pin freeze is not delayed |
| 3 | SP3: `bash spikes/sp3_blender/run_sp3.sh --check`, then `--run` (a neutral stand-in scene only; the pass mark waits for the real kitchen at G1, Sun 15 Nov, so this run gives timings for planning, not the verdict). **Done Tue 20 Oct, in the container, after the orchestrator freed the space** (Avail 14.4 GB), twice (01:19 and 02:05 UTC): all four timings within 2x the table both times (0.81 to 0.86x, then 1.65 to 1.72x on a slower host); each run peaked at 1,408 MB, not 3,100; both pip fetches (428 MB each, the bpy wheel and its 11 dependency wheels) are on the download ledger since the same night (`build/evidence/wp10/download_ledger.jsonl`, rows of kind `pip-wheel-set`; `check_ledger.py` reads 1,506.9 of 2,048 MB), and `run_sp3.sh` now installs from `spikes/sp3_blender/requirements-bpy.txt` with `--require-hashes`; a third fetch at G1 would bring the ledger to about 1,915 MB, which fits with about 130 MB to spare and needs `SP3_FETCH_REASON` | 3,500 MB (entry); 1,900 MB would do | Fri 30 Oct | none; the fallback row is not needed |
| fallback | If `df` on Fri 23 Oct shows less than 4,000 MB free: SP3 moves to the maker's PC (Exercise 5, Blender parallax timed with the Claude app closed) in Mon 2 to Thu 5 Nov, before her Diwali week; the Tue 20 Oct inventory reports the PC tier that says whether that is realistic. The container half is then dropped, not retried, and this section gets the new date | n/a | Fri 23 Oct | none; this is the date by which the choice is final |

**Kept environments, one line to rebuild each.** Checked Tue 20 Oct 2026 by opening them: both environments import. A container restart can clear a session scratchpad, so each line below rebuilds one; no line was run, because nothing needed rebuilding. `<dir>` is any empty folder outside the repository.

| Kept | What it actually holds | One-line rebuild |
|---|---|---|
| `bpyenv` (2.0 GB) | a Python 3.13.16 venv with `bpy` 5.2.2 (it imports as Blender 5.2.2 LTS) and its dependencies (numpy 2.5.4, Cython 3.3.0, zstandard, requests and others). It also holds a second, nested copy (`bpyenv/venv`, 1,008 MB, the same `bpy`) that the outer environment does not need; whether another job of the earlier session uses the nested one is UNVERIFIED. Its dependencies date from 18 Oct (certifi 2026.7.22), so a rebuild differs by a newer certifi | `python3.13 -m venv <dir> && <dir>/bin/python -m pip install --no-cache-dir --require-hashes -r spikes/sp3_blender/requirements-bpy.txt` (a 428 MB download; put it on the ledger with `python3 -I spikes/sp3_blender/ledger_row.py append --stage <name> --exception "<why>"`, or let `run_sp3.sh --run` do the install and the ledger row together) |
| Whisper environment `venv` (461 MB) | a Python 3.13.16 venv with `faster-whisper` 1.2.1 (ctranslate2 4.8.3, onnxruntime 1.31.0, av 19.0.1, tokenizers 0.23.3, huggingface_hub 2.2.0, numpy 2.5.4; it imports). The model weights are not in it: the Systran `base` and `small` models sit in the Hugging Face cache (605 MB, `~/.cache/huggingface`, outside the scratchpad and outside the repo); keep that cache until the week-3 local-Whisper route is built | `python3.13 -m venv <dir> && <dir>/bin/python -m pip install faster-whisper==1.2.1` (its dependencies are not hash-pinned; the models download again on first use if the cache is gone) |
| `vendor/` (0.6 MB: fonts and gsap, git-ignored) | verified against `pipeline/lib/libs.lock.json` on Tue 20 Oct (`fetch_libs.sh --check`: all files match the lock) | `bash pipeline/lib/fetch_libs.sh` |
| `fc_dl` (273 MB) | not an environment but a download folder: the FilmCraft 0.8.0 Linux tarball, the 0.9.0 Windows x64 portable zip, the 0.9.0 release sums file and one extracted 0.8.0 tree | nothing to rebuild; a fresh fetch is a second fetch and needs a recorded exception on the download ledger (`spikes/sp1b_readback/check_ledger.py` reads it) |

One shortcut for the orchestrator to weigh: the earlier session's scratch already holds a Python environment with the same `bpy` 5.2.2 wheel SP3 needs (about 2 GB) and a Blender 5.2.2 Linux tree. Reusing the environment in place would cut SP3's need from 3,500 MB to a few hundred, but `run_sp3.sh` always makes its own venv and nothing proves the old environment is intact (UNVERIFIED), so it is an option, not part of this decision. (Moot since Tue 20 Oct: SP3 ran with its own venv and the old environment was not touched.)

## How to check this file

**This file is generated.** Do not edit it: each spike's row, rule line, test rows and "does not say" bullet are in that spike's own file under `spikes/verdicts/` (`SP1.md` to `SP5.md`), written only by the package that runs the spike, and the prose around them is in `spikes/verdicts/template.md`, written only by the orchestrator. After a change run `python3 -I spikes/verdicts/assemble.py`; `python3 -I spikes/verdicts/assemble.py check` says whether this file is exactly what the parts assemble to (`spikes/verdicts/README.md` has the rule).

`python3 -I tests/spikes/check_verdicts.py` checks the shape: five SP rows with a status word, six T lines under SP1 with T5 and T6 "Not run", and no row without an evidence path that exists.
`bash tests/spikes/run_tests.sh --all` runs it with the rest of the WP-10 suite; the report is `build/reports/WP-10.md`.

## What this file does not say

* Nothing about Windows: no Craft app was started on Windows, and no Linux CLI result here substitutes for the maker's five-minute tests.
<!-- insert: not-said -->
