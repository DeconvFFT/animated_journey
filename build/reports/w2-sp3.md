# W2 SP3 report: Blender (bpy) hero-shot route, two real runs in the container

Run 1 Tue 20 Oct 2026 01:14 to 01:41 UTC, run 2 the same day 02:05 to 02:21 UTC (after the container restarted), both by a Sonnet implementor on branch `build/process-lock` (due Fri 30 Oct; early). Nothing was committed or pushed. **Every figure is a Linux container result on a neutral stand-in scene (primitives only, no photograph, no family media). None of it is evidence for Windows.** Nothing counts as done until `fable-advisor` approves it.

**Verdict: SP3 is Partial, and the container route works.** All four timed configurations passed "within 2x the table" in both runs. Run 1: 0.81x to 0.86x of the table. Run 2, on a different and slower host: 1.65x to 1.72x. The pass mark proper, **one real hero frame within 2x the table**, cannot be judged before the real kitchen exists (G1, Sun 15 Nov), so it is re-run then.
Two things are new in run 2. (1) **The same script, scene and settings ran 1.96 to 2.06 times slower on every line** after the restart, because the container landed on a different CPU model (class: Xeon 2.80 GHz; run 1 recorded 2.10 GHz). The 2x mark therefore has only 16 to 21 percent headroom on a slow host. (2) The run-1 cleanup defect is confirmed fixed on a real install.

## 1. What ran (exact commands, from the repository root)

```bash
# run 1 (01:14 UTC; the earlier container)
df -BM -P /
bash spikes/sp3_blender/run_sp3.sh --check               # exit 0, READY
bash spikes/sp3_blender/run_sp3.sh --run                 # waited 281 s for the disk lock (another spike held it); guarded stage 01:19:59 to 01:28:19; exit 0
bash spikes/sp3_blender/test_cleanup.sh                  # new regression test, after the fix

# run 2 (02:05 UTC; after the restart; the machine idle, no lock wait)
df -BM -P /                                              # 02:05:22
bash spikes/sp3_blender/run_sp3.sh --check               # exit 0, READY
PIP_REPORT=<scratch>/pip_report.json bash spikes/sp3_blender/run_sp3.sh --run     # 02:05:36 to 02:18:42, exit 0, a 2 s df sampler beside it
bash spikes/sp3_blender/test_cleanup.sh                  # PASS again
df -BM -P /                                              # 02:20:40
```
`--run` is `lj_with_disk 3100 sp3-blender` around: `python3 -m venv <scratch>/sp3/venv`; `pip install --no-cache-dir bpy==5.2.2`; then four fresh processes, each under `lj_bench`:
`<venv>/bin/python research/production-scale-fixtures/followup2-s3-kitchen-standin.py -- <scratch>/sp3/out 1920 1080 SAMPLES DENOISE ADAPTIVE` for `8 0 0`, `64 0 0`, `64 1 0`, `128 1 0`; the script then deletes its folder.
`PIP_REPORT` is a pip option that writes a JSON list of what pip fetched; it changes nothing about the install. Run 1 also did side checks in the venv it left behind (a device probe, `identify`/`compare` on the PNGs, a Workbench draft, a clean repeat); run 2 did not, because the fixed script now deletes the venv and the renders at the end.

## 2. Results, PASS or FAIL

Evidence: `build/evidence/wp10/sp3_results.txt` (both runs' RESULT lines), run 1 `build/evidence/w2-sp3/{summary.json,run_transcript.txt,supp_results.txt,df_samples.txt,cleanup_regression.txt,run1_sp3_results.txt}`, run 2 `build/evidence/w2-sp3/{summary_run2.json,run2_transcript.txt,run2_sp3_results.txt,run2_ledgers.txt,run2_df_samples.txt,run2_pip_summary.json,run2_cleanup_regression.txt}`.

| # | Test | Run 1 | Run 2 | Output that proves it |
|---|---|---|---|---|
| T0 | Entry check `--check` | PASS | **PASS** | `READY: Avail 14546 MB is at least 3500 MB` (run 1: 14390 MB), exit 0; wheel 401,697,653 bytes read from PyPI; scene `py_compile ok`; Python 3.13.16 |
| T1 | Guarded stage | PASS | **PASS** | `lj_guard: sp3-blender: finished with exit 0; Avail start 14546 MB, min 13140 MB, end 14545 MB`; ledger status `ok`, lock wait 0 s (run 1: 281 s) |
| T2 | venv and `pip install bpy==5.2.2` | PASS, 130 s | **PASS**, 59 s | guard start 02:05:36 to the first timed line 02:06:35; 12 files installed (`run2_pip_summary.json`); run 1 also ran `pip check`: "No broken requirements found" |
| T3 | `import bpy` is Blender 5.2.x | PASS | **PASS** | `[3/5] bpy imports: Blender 5.2.2 LTS` |
| T4a | 8 samples, no denoise | PASS 10.8 s | **PASS 22.2 s** | table 13.3 s, limit 26.6 s: run 1 0.81x, run 2 1.67x; 594 MB |
| T4b | 64 samples, no denoise | PASS 81.9 s | **PASS 160.3 s** | table 95.2 s, limit 190.4 s: 0.86x, 1.68x; 594 MB |
| T4c | 64 samples + denoise | PASS 93.8 s (repeat 93.0 s) | **PASS 185.3 s** | table 112.4 s, limit 224.9 s: 0.83x, 1.65x; 2,209 MB |
| T4d | 128 samples + denoise | PASS 176.2 s | **PASS 351.7 s** | table 204.3 s, limit 408.6 s: 0.86x, 1.72x; 2,209 MB |
| T5 | Renders are real images | PASS | not re-checked | run 1: four 1920x1080 sRGB PNGs, mean level 172 to 177 of 255, min 0, max 255, looked at the 128-sample frame. Run 2: the script deletes the renders, and no image was inspected; the `RESULT` lines show each render finished |
| T6 | Same settings, same pixels | PASS | not run | run 1: repeat of `64 1 0`, `compare -metric AE` = 0 differing pixels. Run 2 had no repeat line. Cross-host pixel identity is untested |
| T7 | Memory | PASS | **PASS** | 594 and 2,209 MB peak of 16,093 MB in both runs, identical on different hardware; no out-of-memory |
| T8 | The script cleans up after itself | **FAIL** | **PASS** | run 1: last line `run_sp3.sh: line 1: S: unbound variable`, venv (1,008 MB) and renders (14 MB) left behind, deleted by hand. Run 2: `[5/5] cleanup: ...`, driver line `sp3 scratch folder after: gone`, no "unbound" anywhere in the transcript, `df` back to 14,545 MB; `test_cleanup.sh`: `PASS: the work folder is removed when run_inner runs to the end` |
| T9 | The wheel is the published one | not checked | **PASS (indirect)** | the pip report's sha256 for the bpy wheel is `3dfd1a9e7a5aec0f0fe95a1b01d10cd66e212b16ea38b77d132159dc9a666d45`, equal to the digest PyPI published (recorded in run 1's `summary.json`). pip checks a download against the digest its index advertises; I did not hash the bytes myself and the wheel is deleted |

"Table" is `research/production-scale-fixtures/followup2-s3-container-results.txt` (18 Oct, same stand-in, 1080p, Cycles CPU, 4 vCPU): the mean of the recorded runs per configuration (13.3; 95.2; 115.1 and 109.8; 208.1 and 200.5). Both runs: 4 vCPU, 16 GB, **no GPU device** (run 1's probe listed none for CUDA, OPTIX, HIP or ONEAPI).
Run 1 supplementary, no pass mark: a Workbench draft took 4.1 s per 1080p frame and 801 MB (indicative only: its start was flagged for load; three `EGL_BAD_MATCH` lines printed; it completed).

## 3. Finding from run 2: the same job took twice as long on another host

| Config | Table | 2x limit | Run 1 | Run 2 | Run 2 / run 1 | Limit / run 2 (headroom) |
|---|---|---|---|---|---|---|
| 8, 0, 0 | 13.3 s | 26.6 s | 10.8 s | 22.2 s | 2.06 | 1.20 |
| 64, 0, 0 | 95.2 s | 190.4 s | 81.9 s | 160.3 s | 1.96 | 1.19 |
| 64, 1, 0 | 112.4 s | 224.9 s | 93.8 s | 185.3 s | 1.98 | 1.21 |
| 128, 1, 0 | 204.3 s | 408.6 s | 176.2 s | 351.7 s | 2.00 | 1.16 |

* The factor is the same on every line (1.96 to 2.06), which says a whole-machine speed difference, not something in one configuration. After the restart `lscpu` reports a different CPU model (class "Xeon Processor 2.80 GHz", with AVX-512 flags; run 1 recorded "Xeon 2.10 GHz"), same 4 vCPU and 16 GB.
* It is not load from my own work and not a noisy neighbour that shows up as steal: a 10 s `/proc/stat` sample during line 2 gave user 92.8 percent, system 5.7, **steal 1.1**, idle 0.3. The first line started at load 0.56 (clean) and was already 2.06x run 1's clean first line. The `lj_bench` "contaminated=yes" flag on lines 2 to 4 (load1 1.96, 4.75, 4.89) is the previous render's own load average, the same self-flagging as in run 1 (`run2_ledgers.txt`).
* **Why the new host is slower is UNVERIFIED** (I did not isolate CPU generation, memory bandwidth or a vCPU quota; I did not run a separate benchmark, and there is no baseline for one).
* **What it means for the pass mark.** A real kitchen frame costing more than about 1.16 to 1.21 times the stand-in per sample would fail "within 2x the table" on a run-2-class host, while on a run-1-class host it could cost about 2.3 to 2.5 times as much and pass. The table and the mark do not name a host. **Suggestion for Fable and the orchestrator (not applied):** at G1 re-time the stand-in's `64 1 0` line (93.8 s on the fast host, 185.3 s on the slow one) in the same container session as the real frame, record the CPU model in the evidence, and judge the real frame against the stand-in measured beside it on that host, as well as against the table.

## 4. Disk, before and after (`df -BM -P /`, Avail; the volume is shared and other jobs write to it)

| When (UTC) | Run 1 Avail | Run 2 Avail | Note |
|---|---|---|---|
| before the check | 14,547 MB (01:14:24) | **14,546 MB** (02:05:22) | |
| guard start | 14,480 MB (01:19:59) | 14,546 MB (02:05:36) | run 1 lost 157 MB to other jobs before it |
| lowest | 13,072 MB | **13,136 MB** (sampler, 02:06:32; the guard saw 13,140) | **peak use 1,408 MB in both runs**: the 402 MB wheel while pip unpacks it, plus the venv |
| run end | 13,459 MB, venv still there (T8) | 14,545 MB (02:18:42) | in run 2 the script had already deleted its folder |
| after | 14,476 MB (01:38, after the hand delete) | **14,545 MB** (02:20:40) | run 2 ends 1 MB under its start |

Steady footprint 1,021 MB in both runs (venv 1,008, of which the `bpy` package is 881; renders 14). **The real need was 1,408 MB at peak, not the 3,100 planned**; an entry of about 1,900 MB would do. The 3,100 and 3,500 figures (build plan 4.9, asserted by the WP-10 tests) were not changed; that is the orchestrator's call. Run 2 took 13 min 6 s start to finish.

## 5. The cleanup defect (T8): found in run 1, fixed, confirmed in run 2

`run_inner` kept its folder in a local `S` and cleaned up with `trap 'rm -rf -- "$S"' EXIT`. The trap runs when the script exits, after the function has returned, so under `set -u` it died with "S: unbound variable" and `rm` never ran. A failing step hides it, so only a successful run shows it. Fix in `spikes/sp3_blender/run_sp3.sh`: `S` is no longer local and the trap reads `${S:-...}`. `spikes/sp3_blender/test_cleanup.sh` (stand-in python, no download) FAILS the old script and PASSES the fixed one (`cleanup_regression.txt`, `run2_cleanup_regression.txt`). **Run 2 is the first real-install confirmation.** The script was not edited in run 2.

## 6. UNVERIFIED

* **Everything on Windows**: `pip install bpy` there needs Python 3.13 exactly; the PC's own timings (`playbooks/toolchain.md` Exercise 5, Claude app closed), its GPU (CUDA, OptiX or HIP) and every number above on the PC; `blender.exe` against `bpy`; where files land. No Windows script was written or run.
* **The real kitchen**: the stand-in has 2,938 faces and no photographic texture; a real frame may cost more per sample. The pass mark is judged on it at G1.
* **GPU time**: none here. The plan's hero finals on a rented or owned GPU are untested.
* **Why the second host is about twice as slow**, and whether the next restart lands on the fast or the slow one.
* **Run 2's render content and cross-host pixel identity** (T5, T6): not re-checked.
* **The wheel's bytes** were not hashed independently (T9 is pip's own check against the index digest).
* The Workbench time (4.1 s) is indicative only.

## 7. Planning numbers (arithmetic on the stand-in, not a promise)

At 94 s (fast host) to 185 s (slow host) a frame, a 5 s hero move of 120 frames at 64 samples with denoise is about 3.1 to 6.2 CPU-hours here; as Workbench drafts at about 4 s it is about 8 minutes (fast host; the slow host is untimed). That agrees with W-23: **drafts in the container, finals on the PC's GPU**, and the container's finals are a stretch on a slow host.

## 8. Downloads and clean-up

* Fetched in run 2: the `bpy` wheel, 401,697,653 bytes, plus 11 small dependency wheels (numpy, Cython, zstandard, requests and others; their sizes were not measured, roughly 30 MB). Run 1 fetched the same. **SP3 has therefore used two fetches, about 860 MB.** pip fetches are not in the Craft download ledger (`check_ledger.py` reads 623.6 MB of 2,048 MB); counted together that is about 1.5 GB of the 2 GB allowance, so **a third fetch at G1 would sit at the allowance**: the orchestrator should decide whether to raise it or to keep a venv until then (1,008 MB on a volume with 14.5 GB free).
* **Deleted: everything.** The script removed the venv and renders itself; pip's temporary copy of the wheel went with it; no pip cache was written (`--no-cache-dir`); `<scratch>/sp3` does not exist; `build-scratch` is 202 MB, as before. The pip report (143 KB, with environment details) stayed in the session scratchpad, not the repository, and is reduced to `run2_pip_summary.json` (file names, versions, sha256).
* **Kept for later spikes: nothing.** No later spike needs `bpy` (SP1 is the Craft apps; SP4 part (d) needs no Blender). The venv rebuilds in 1 to 2 minutes with `bash spikes/sp3_blender/run_sp3.sh --run` or `pip install bpy==5.2.2`. Kept in the repository (text only): the evidence files above (about 60 KB; `df_samples` files are the largest). No image was added to git.

## 9. Files changed (run 2)

New: `build/evidence/w2-sp3/{summary_run2.json,run2_transcript.txt,run2_sp3_results.txt,run2_ledgers.txt,run2_df_samples.txt,run2_pip_summary.json,run2_cleanup_regression.txt,run1_sp3_results.txt}`. Changed: `build/evidence/wp10/sp3_results.txt` (the script overwrites it on every run; it now holds run 1 then run 2 under two headings), `build/reports/w2-sp3.md` (this), `spikes/VERDICTS-W2.md` (SP3 row, disk-decision step 3, closing bullet), `spikes/sp3_blender/README.md` (second-run table, UNVERIFIED). `run_sp3.sh` was not touched in run 2. No CHARTER, DECISIONS, ROADMAP, PLAN-ON-A-PAGE, CLAUDE.md or `.claude/` file was touched; no commit.

## 10. For the orchestrator

1. Fable review of this report and the SP3 row (D-32). Nothing here is approved yet.
2. Decide how the G1 pass mark treats the host spread (section 3): add the same-session stand-in line and the CPU model to the G1 evidence, or keep the plain table comparison and accept that the result depends on the host.
3. Decide the download allowance for the G1 re-run (section 8), and whether to lower SP3's planned and entry disk figures (peak 1,408 MB). Neither was changed.
4. Whether the `lj_bench` contamination heuristic should ignore the stage's own previous process (back-to-back sweeps flag themselves, in both runs). Not changed.
5. At G1 (Sun 15 Nov) re-run the four configurations on the real kitchen frame, then apply "dropped, or moved to the PC" to that result. The maker's Exercise 5 timings remain the Windows and GPU evidence.
