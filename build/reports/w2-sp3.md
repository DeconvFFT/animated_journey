# W2 SP3 report: Blender (bpy) hero-shot route, first real run in the container

Run Tue 20 Oct 2026 (due Fri 30 Oct; early) by a Sonnet implementor on branch `build/process-lock`. Nothing was committed or pushed. **Every figure is a Linux container result on a neutral stand-in scene (primitives only, no photograph, no family media). None of it is evidence for Windows.** Nothing counts as done until `fable-advisor` approves it.

**Verdict: SP3 is Partial, and the container route works.** All four timed configurations came in within 2x the table (0.81x to 0.86x of it); `bpy` 5.2.2 LTS installs, imports and renders here. The pass mark proper, **one real hero frame within 2x the table**, cannot be judged before the real kitchen exists (G1, Sun 15 Nov), so it is re-run then. One test FAILED, and it is the script and not the route: the cleanup trap never deleted the venv (found, fixed, regression-tested).

## 1. What ran (exact commands, from the repository root)

```bash
df -BM -P /                                              # 01:14:24 UTC, before
bash spikes/sp3_blender/run_sp3.sh --check               # exit 0, READY
bash spikes/sp3_blender/run_sp3.sh --run                 # 01:15:15 start; waited 281 s for the disk lock (another spike's stage held it); guarded stage ran 01:19:59 to 01:28:19; exit 0
```
`--run` is `lj_with_disk 3100 sp3-blender` around: `python3 -m venv <scratch>/sp3/venv`; `pip install --no-cache-dir bpy==5.2.2`; then four fresh processes, each under `lj_bench`:
`<venv>/bin/python research/production-scale-fixtures/followup2-s3-kitchen-standin.py -- <scratch>/sp3/out 1920 1080 SAMPLES DENOISE ADAPTIVE` for `8 0 0`, `64 0 0`, `64 1 0`, `128 1 0`.
Side checks, same venv (all read-only or in the scratch folder): a device probe (`python -I`, `import bpy`, list devices for NONE, CUDA, OPTIX, HIP, ONEAPI); `identify -format` and `compare -metric RMSE|AE` on the PNGs; a df and folder-size sampler every 2 s.
Supplementary, each under `lj_bench`: a Workbench draft (`sed 's/scene.render.engine = "CYCLES"/scene.render.engine = "BLENDER_WORKBENCH"/'` on a scratch copy of the scene, 1920x1080) and a repeat of `64 1 0` after the load had settled.
After: `bash spikes/sp3_blender/test_cleanup.sh` (new, section 4), `rm -rf <scratch>/sp3` by hand, `python3 -I tests/spikes/check_verdicts.py`, `python3 -I scripts/public_lint.py --paths ...` (and `--theme`).

## 2. Results, PASS or FAIL (evidence: `build/evidence/wp10/sp3_results.txt`, `build/evidence/w2-sp3/{run_transcript.txt,summary.json,supp_results.txt,df_samples.txt,cleanup_regression.txt}`)

| # | Test | Result | Output that proves it |
|---|---|---|---|
| T0 | Entry check `--check` | **PASS** | `READY: Avail 14390 MB is at least 3500 MB`, exit 0; wheel 401,697,653 bytes read from PyPI, scene `py_compile ok`, Python 3.13.16 |
| T1 | Guarded stage | **PASS** | `lj_guard: sp3-blender: finished with exit 0; Avail start 14480 MB, min 13077 MB, end 13459 MB`; ledger status `ok`, lock wait 281 s |
| T2 | venv and `pip install bpy==5.2.2` | **PASS** | 130 s (01:20:02 to 01:22:12); `pip check`: "No broken requirements found" |
| T3 | `import bpy` is Blender 5.2.x | **PASS** | `bpy 5.2.2 LTS`, build hash `d13f752e3b9c`, build date 2026-09-15, Python 3.13.16, background mode |
| T4a | 8 samples, no denoise | **PASS** | `wall_s=10.8` against table 13.3 (limit 26.6): 0.81x; `peak_rss_mb=594` |
| T4b | 64 samples, no denoise | **PASS** | `wall_s=81.9` against 95.2 (limit 190.4): 0.86x; 594 MB |
| T4c | 64 samples + denoise | **PASS** | `wall_s=93.8` against 112.4 (limit 224.9): 0.83x; 2,209 MB; repeat 93.0 s (0.83x) |
| T4d | 128 samples + denoise | **PASS** | `wall_s=176.2` against 204.3 (limit 408.6): 0.86x; 2,209 MB |
| T5 | Renders are real images | **PASS** | four 1920x1080 sRGB PNGs, mean level 172 to 177 of 255, min 0, max 255; looked at the 128-sample frame: the kitchen, lit, no artefacts; 8 against 128 samples RMSE 0.087 (noise), 64 against 128 with denoise 0.0046 |
| T6 | Same settings, same pixels | **PASS** | repeat of `64 1 0`: `compare -metric AE` = 0 differing pixels, RMSE 0 (the PNG bytes differ in metadata only) |
| T7 | Memory | **PASS** | 594 and 2,209 MB peak of 16,093 MB, equal to the 18 Oct figures; no out-of-memory |
| T8 | The script cleans up after itself | **FAIL** | the last line of the run was `run_sp3.sh: line 1: S: unbound variable`; the venv (1,008 MB) and the renders (14 MB) were still on disk afterwards; deleted by hand, 01:38 |

"Table" is `research/production-scale-fixtures/followup2-s3-container-results.txt` (18 Oct, same stand-in, 1080p, Cycles CPU, 4 vCPU): the mean of the recorded runs per configuration (13.3; 95.2; 115.1 and 109.8; 208.1 and 200.5). Machine: 4 vCPU Intel Xeon at 2.10 GHz, 16 GB, **no GPU device of any type** (the probe lists none for CUDA, OPTIX, HIP or ONEAPI; the CUDA and HIP libraries fail to load, harmlessly).
Supplementary, no pass mark: **Workbench draft 4.1 s per 1080p frame**, 801 MB (indicative only: its start was flagged contaminated, load 3.89 from the previous job's tail; three `EGL_BAD_MATCH` lines printed; it completed, mean level 116).
**The `lj_bench` flag "contaminated=yes" on T4b to T4d is the run's own load**: load1 at start was 1.21, 3.63 and 4.01 because the line before had just used all four cores; the first line started at 0.58 (clean), the clean repeat at 0.59, and all agree to 1 to 2 percent. A `ps` snapshot at about 01:27 showed only the render running, and the bench ledger has no other entry between 01:22:12 and 01:28:19 (this stage's four lines are back to back). No timing here rests on a number I think was disturbed, except the Workbench one, which is labelled.

## 3. Disk, before and after (`df -BM -P /`, Avail; the volume is shared and other jobs write to it)

| When (UTC) | Avail | Note |
|---|---|---|
| 01:14:24 before the check | **14,547 MB** | |
| 01:15:15 run start | 14,390 MB | other jobs wrote 157 MB in 51 s |
| 01:19:59 guard start | 14,480 MB | after the 281 s lock wait |
| 01:22:10 lowest | 13,072 MB (guard saw 13,077) | **peak use 1,408 MB**: the 402 MB wheel while pip unpacks it, plus the venv |
| 01:28:19 run end | 13,459 MB | venv still there (T8) |
| 01:38:16 after `rm -rf <scratch>/sp3` | **14,476 MB** | 71 MB under the start: other jobs, not this run; the SP3 folder is gone |

Steady footprint 1,021 MB (venv 1,008, of which the `bpy` package is 881; renders 14). **The real need was 1,408 MB at peak, not the 3,100 planned**; an entry of about 1,900 MB (peak plus the 400 MB floor) would have been enough. I did not change the 3,100 and 3,500 figures (build plan 4.9, and the WP-10 tests assert them); that is the orchestrator's call.

## 4. Defect found and fixed: cleanup (T8)

`run_inner` kept its folder in a local `S` and cleaned up with `trap 'rm -rf -- "$S"' EXIT`. The trap runs when the script exits, after the function has returned, so under `set -u` it died with "S: unbound variable" and `rm` never ran. A failing step hides it (the trap then runs inside the function), so only a successful run shows it, and the 19 Oct dry run and tests could not. Fix in `spikes/sp3_blender/run_sp3.sh`: `S` is no longer local and the trap reads `${S:-...}`. New `spikes/sp3_blender/test_cleanup.sh` runs `run_inner` to the end with a stand-in python (no Blender, no download, a few seconds) and checks exit 0, folder gone, no "unbound variable":
`--script <the script as committed before the fix>`: `FAIL` (folder left behind: yes; "unbound variable": yes). The fixed script: `PASS` (`cleanup_regression.txt`).
Also touched in `run_sp3.sh`: two stale header comments ("PREPARED, NOT RUN"; the 19 Oct disk paragraph, now marked historical). The dry run (fake 5,000 MB) and the refusal (fake 3,499 MB, exit 3) still behave as the WP-10 tests expect (re-checked by hand; the full `tests/spikes/run_tests.sh` was not re-run, to keep CPU off the timed Craft stages that were running).

## 5. UNVERIFIED

* **Everything on Windows**: `pip install bpy` there needs Python 3.13 exactly; the PC's own timings (Exercise 5, Claude app closed), its GPU (CUDA, OptiX or HIP) and every number in section 2 on the PC; `blender.exe` against `bpy`; where files land. No Windows script was written or run.
* **The real kitchen**: the stand-in has 2,938 faces and no photographic texture; a real frame may cost more per sample. The pass mark is judged on it at G1.
* **GPU time**: none here. The plan's hero finals on a rented or owned GPU are untested by this run.
* **The wheel's SHA-256 was not compared** with the download (no `--require-hashes`, no cache, the wheel is gone). PyPI's published digest is in `summary.json`.
* **The cleanup fix on a second real install**: proved with the stand-in python only (another real run is a 402 MB fetch).
* The Workbench time (above) and the 801 MB for it.

## 6. What the numbers mean for planning (arithmetic on the stand-in, not a promise)

At about 94 s a frame (64 samples with denoise) a 5 s hero move of 120 frames is about 3.1 CPU-hours here; as Workbench drafts at about 4 s it is about 8 minutes. That agrees with W-23: **drafts in the container, finals on the PC's GPU**. The same frame rendered twice is pixel-identical, which is what splitting finals by frame needs (one frame twice is the only repeat tested). The two runs of the same line differ by 0.9 percent (the 18 Oct note allowed 10 to 20 percent; the quieter machine and the exclusive bench lock are the likely reason, UNVERIFIED).

## 7. Downloads and clean-up

Fetched: the `bpy` wheel, 401,697,653 bytes, plus small dependency wheels (numpy and others, inside the 1,008 MB venv); about 402 MB plus a little against the 2 GB allowance, once. **Deleted: everything** (the venv and renders in `<scratch>/sp3`; pip's temporary copy of the wheel, which pip removed itself, no pip cache written; my scratch renders). **Kept for later spikes: nothing**: no later spike needs `bpy` (SP1 is the Craft apps, SP4 part (d) needs no Blender), and the venv rebuilds in about 130 s with `bash spikes/sp3_blender/run_sp3.sh --run` or `pip install bpy==5.2.2`. If the G1 kitchen build wants it at once, one re-fetch is 402 MB. Kept in the repository (text only): the evidence files above (about 24 KB; `df_samples.txt` is the largest) and `build/evidence/wp10/sp3_results.txt`. No image was added to git.

## 8. Files changed

`spikes/sp3_blender/run_sp3.sh` (the fix and two comments), `spikes/sp3_blender/test_cleanup.sh` (new), `spikes/sp3_blender/README.md` (first-run table, UNVERIFIED), `spikes/VERDICTS-W2.md` (SP3 row now **Partial**, the quoted rule, the disk-decision step 3, the closing bullets), `build/reports/w2-sp3.md` (this), `build/evidence/w2-sp3/*` (new), `build/evidence/wp10/sp3_results.txt` (written by the script). `python3 -I tests/spikes/check_verdicts.py`: "5 main rows, 6 SP1 test rows; complete". `public_lint` (with `--theme`): 0 findings.
No CHARTER, DECISIONS, ROADMAP, PLAN-ON-A-PAGE, CLAUDE.md or `.claude/` file was touched; no commit.

## 9. For the orchestrator

1. Fable review of this report and the SP3 row (D-32). Nothing here is approved yet.
2. Decide whether to lower SP3's planned and entry disk figures (peak 1,408 MB); and whether the `lj_bench` contamination heuristic should ignore the stage's own previous process (back-to-back sweeps flag themselves). Neither was changed.
3. At G1 (Sun 15 Nov) re-run the four configurations on the real kitchen frame, then apply "dropped, or moved to the PC" to that result. The maker's Exercise 5 timings remain the Windows and GPU evidence.
