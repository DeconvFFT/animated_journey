# SP3: Blender for hero shots (run once on the stand-in scene; the real-kitchen pass mark waits for G1)

*Prepared in WP-10, Mon 19 Oct 2026 (then **Deferred** for disk). **First real run Tue 20 Oct 2026** (`build/reports/w2-sp3.md`): status **Partial**. Every timing is a Linux container result on a neutral stand-in scene; it is not evidence for Windows.*

## First run, Tue 20 Oct 2026 (stand-in scene, Cycles CPU, 4 vCPU, no GPU, 1920x1080)

| Samples, denoise, adaptive | Table (18 Oct, mean of the recorded runs) | Limit (2x) | Measured 20 Oct | Ratio | Peak memory |
|---|---|---|---|---|---|
| 8, 0, 0 | 13.3 s | 26.6 s | **10.8 s** | 0.81 | 594 MB |
| 64, 0, 0 | 95.2 s | 190.4 s | **81.9 s** | 0.86 | 594 MB |
| 64, 1, 0 | 112.4 s | 224.9 s | **93.8 s** (repeat 93.0 s) | 0.83 | 2,209 MB |
| 128, 1, 0 | 204.3 s | 408.6 s | **176.2 s** | 0.86 | 2,209 MB |

All four are within 2x of the table, so the **container route works** (`bpy` 5.2.2 LTS installs, imports and renders; two renders with the same settings differ in 0 pixels). The real pass mark, **one real hero frame within 2x the table**, is still not judged: the real kitchen does not exist before G1 (Sun 15 Nov). The real disk need was a **peak of 1,408 MB** (the 402 MB wheel while pip unpacks it, plus the 1,008 MB venv), a steady 1,021 MB, not the 3,100 MB planned. **A defect in this script's cleanup** was found by the run (the venv was left behind) and fixed; `bash spikes/sp3_blender/test_cleanup.sh` is its regression test. Evidence: `build/evidence/wp10/sp3_results.txt`, `build/evidence/w2-sp3/`.

## What SP3 decides

`playbooks/agent-pipeline.md` Step 3: "SP3: Blender, for hero shots", with the rule "A route that fails its spike is dropped, or moved to the PC. Do not argue with the result."
The pass mark in the build plan is **one real hero frame within 2x the table** (`research/production-scale-fixtures/followup2-s3-container-results.txt`). That cannot be judged
before the real kitchen exists (gate G1), so what can be done now is to time a NEUTRAL stand-in scene and get the tooling ready.

## Entry conditions and numbers (`bash spikes/sp3_blender/run_sp3.sh --check` prints them live)

| Item | Figure | Source |
|---|---|---|
| Free disk needed | **3,500 MB** = planned 3,100 MB + the 400 MB floor of `scripts/lj_guard.sh` | build plan 4.9, WP-10 item 2 ("at least 3.5 GB is free") |
| `bpy` 5.2.2 wheel | **401,697,653 bytes** (402 MB; 383 MiB), `cp313-cp313-manylinux_2_28_x86_64`, Python 3.13 only | PyPI JSON, read 19 Oct 2026 |
| Venv it makes | about **1 GB** on disk | R9/M14 (`research/toolchain.md`) |
| Blender 5.2.2 Linux tarball | **383,295,504 bytes** by HEAD request (the PC route; not used here) | `download.blender.org`, HEAD 19 Oct 2026 |
| Free disk in the container today | about **700 to 780 MB**, shared with other jobs | `df`, this package's runs |
| Python | 3.13 (the wheel is cp313 only) | `python3 --version` |
| Scene | `research/production-scale-fixtures/followup2-s3-kitchen-standin.py`: primitives only, **no photograph, no family imagery** | reused, `py_compile`d by `--check` |
| Earlier numbers (stand-in, 1080p, Cycles CPU, 4 vCPU) | 64 samples + denoise 110-115 s; 128 samples 192-232 s; 24 samples + denoise 51-59 s; peak RSS 0.6 GB (2.2 GB with denoise) | `followup2-s3-container-results.txt` |

On 19 Oct `run_sp3.sh --check` printed **"NOT RUN: needs >= 3.5 GB free"**, exit 3 (Avail was far below 3,500 MB); on 20 Oct it printed READY (Avail 14,390 MB). The script reuses the research scripts by path and does not copy them.
`followup2-s3-run-sweep.sh` is referenced as the record of the sweep, but not executed: its first lines hold a path of an earlier session. `run_sp3.sh --run` runs the same four
configurations itself (`8 0 0`, `64 0 0`, `64 1 0`, `128 1 0` as SAMPLES DENOISE ADAPTIVE), each in a fresh process under `lj_bench`, inside one `lj_with_disk 3100` stage, and deletes the venv afterwards.
`SP3_DRYRUN=1 bash spikes/sp3_blender/run_sp3.sh --run` (with a df that reports enough room) prints the plan and does none of it; the tests use that to check the logic without the disk.

## Justified deferral (history: this was true on 19 Oct; the disk was freed on 20 Oct and the run happened)

* The disk is the blocker, not the method: the 402 MB wheel plus the 1 GB venv is more than the container has free, and the guard (rightly) refuses a stage that would leave under 400 MB.
* The pass mark needs the real kitchen, which does not exist before G1 (Sun 15 Nov). A stand-in timing is useful for planning, not for the verdict.
* Where it runs (chosen Tue 20 Oct 2026, gate review r1; the reasons and dates are in `spikes/VERDICTS-W2.md`, "Disk decision"): (1) **this container after at least 3.5 GB is free**, by Fri 30 Oct:
  `bash spikes/sp3_blender/run_sp3.sh --check`, then `--run`, because the question is the container route; (2) **only if `df` on Fri 23 Oct shows less than 4,000 MB free**: the maker's PC in Mon 2 to Thu 5 Nov,
  Blender parallax timed with the Claude app closed (`playbooks/toolchain.md` Exercise 5), where the 4090-class numbers of `playbooks/production-scale.md` apply. Neither needs a photograph; the scene is the stand-in.
* The decision on the evidence of the run is the orchestrator's, with Fable: "A route that fails its spike is dropped, or moved to the PC."

## UNVERIFIED

* **Everything on Windows**: `pip install bpy` there needs Python 3.13 exactly; the PC's own timings (Exercise 5, Claude app closed), its GPU (CUDA, OptiX or HIP), `blender.exe` against `bpy`, and where the files land. The container has no GPU device of any type (`bpy` lists none), so no GPU timing exists here either. The maker's PC is the evidence.
* **The real kitchen**: the pass mark (one real hero frame within 2x the table) is judged at G1 on the real set; the stand-in has 2,938 faces and no photographic texture, so a real frame can cost more per sample.
* **The wheel's SHA-256** was not compared with the download (`pip install` without `--require-hashes`, no cache, the wheel is gone). PyPI's published digest is in `build/evidence/w2-sp3/summary.json`; a later run can pass `--require-hashes`.
* **The cleanup fix on the real `bpy` run**: proved with a stand-in python (`test_cleanup.sh`: the old script FAILS it, the fixed one PASSES); not re-proved against a second real install, which would be another 402 MB fetch.
* **The Workbench draft time (4.1 s) is indicative**: its start was flagged contaminated by the 1-minute load average, and it printed three `EGL_BAD_MATCH` messages (it completed and the image is real).
