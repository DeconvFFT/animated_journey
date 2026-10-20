# SP3: Blender for hero shots (prepared, not run)

*WP-10, Mon 19 Oct 2026. Status: **Deferred** (a justified deferral, below). Nothing was installed or downloaded for this spike.*

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

`run_sp3.sh --check` on this container: **"NOT RUN: needs >= 3.5 GB free"**, exit 3 (Avail is far below 3,500 MB). The script reuses the research scripts by path and does not copy them.
`followup2-s3-run-sweep.sh` is referenced as the record of the sweep, but not executed: its first lines hold a path of an earlier session. `run_sp3.sh --run` runs the same four
configurations itself (`8 0 0`, `64 0 0`, `64 1 0`, `128 1 0` as SAMPLES DENOISE ADAPTIVE), each in a fresh process under `lj_bench`, inside one `lj_with_disk 3100` stage, and deletes the venv afterwards.
`SP3_DRYRUN=1 bash spikes/sp3_blender/run_sp3.sh --run` (with a df that reports enough room) prints the plan and does none of it; the tests use that to check the logic without the disk.

## Justified deferral

* The disk is the blocker, not the method: the 402 MB wheel plus the 1 GB venv is more than the container has free, and the guard (rightly) refuses a stage that would leave under 400 MB.
* The pass mark needs the real kitchen, which does not exist before G1 (Sun 15 Nov). A stand-in timing is useful for planning, not for the verdict.
* Where it runs (chosen Tue 20 Oct 2026, gate review r1; the reasons and dates are in `spikes/VERDICTS-W2.md`, "Disk decision"): (1) **this container after at least 3.5 GB is free**, by Fri 30 Oct:
  `bash spikes/sp3_blender/run_sp3.sh --check`, then `--run`, because the question is the container route; (2) **only if `df` on Fri 23 Oct shows less than 4,000 MB free**: the maker's PC in Mon 2 to Thu 5 Nov,
  Blender parallax timed with the Claude app closed (`playbooks/toolchain.md` Exercise 5), where the 4090-class numbers of `playbooks/production-scale.md` apply. Neither needs a photograph; the scene is the stand-in.
* The decision on the evidence of the run is the orchestrator's, with Fable: "A route that fails its spike is dropped, or moved to the PC."

## UNVERIFIED

`--run` has never executed here (it cannot: the guard refuses it), so its venv, pip and `lj_bench` steps are checked only by `bash -n`, the dry run and reading. The first real run may need a
fix. Nothing about Blender on Windows is tested by it; the PC route is the maker's.
