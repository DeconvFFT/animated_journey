# build/evidence/wp10: what each file is

*WP-10, 19 Oct 2026. All Craft results are **Linux CLI results; not evidence for Windows**. No file here holds a host name, user name, IP address or absolute path (checked by `scripts/public_lint.py`).*

| File | What it is |
|---|---|
| `t1_<app>_<tag>.json` | T1 smoke of PhotoCraft, VectorCraft, LightCraft: version, usage, command listing, stderr, linked libraries, the binary's size and SHA-256 (public build identity) |
| `readback_<app>_<tag>.json` | the read-back criteria (`detail.checks`) and findings (`detail.findings`) of those three apps |
| `t3_filmcraft_v0.9.0.json` | T3 on FilmCraft: 35 criteria, 10 findings, the per-format matrix (`detail.formats`) |
| `stage_<app>-<tag>.json` | one per stage: status, the exit code, the reason (for a BLOCKED stage the guard's exact message), the disk object with the guard's start, minimum and end Avail, the 0.25 s sampled minimum, whether it fetched |
| `download_ledger.jsonl` | the fetches made by WP-10 (PhotoCraft, VectorCraft, LightCraft). WP-07's two (FilmCraft, EffectCraft) are in `build/evidence/wp07/download_ledger.jsonl`; `spikes/sp1b_readback/check_ledger.py` reads both |
| `tests.jsonl`, `tests_quick.jsonl`, `tests_all.txt`, `tests_quick.txt` | the `tests/spikes/run_tests.sh` envelopes and console output |
| `acceptance_transcript.txt` | each acceptance command of WP-10 with its real output and exit code |
| `sp4_job_60s_gaps.json` | `gaps.py` on the 60 s mechanism run of the SP4 job |
| `summary.json` | counts |

## Things to know before reading the envelopes

1. **Two stages are FAIL and both are findings, not harness defects.**
   *VectorCraft*: all authored ids survive, but `rect`, `circle` and `ellipse` become paths (9 of 17 rig elements, 5 of 11 in `at-rig.svg`), and the `data-*` of the rig's `<text>` element changed, so `check_ids.py` exits 1 on the rig.
   *LightCraft*: 4 of 5 read-back criteria pass; the exports criterion failed because **the three synthetic scans of the first (and only) real run were byte-identical** and LightCraft's `library.import` skips content duplicates
   (imported 1, duplicates 2). The driver now writes three different cards and records the import counts; the real LightCraft stage was **not** repeated (a repeat is a second fetch of 109 MB, and the exactly-once rule was kept).
2. **`kept_tarball_deleted` is `true` in `stage_photocraft`, `stage_vectorcraft` and `stage_lightcraft`: a bookkeeping bug in the first version of the harness, since fixed (it now exists only for the FilmCraft stage and is `null` elsewhere).**
   It has no meaning for those three. The facts are: the FilmCraft kept tarball was deleted by the FilmCraft stage (`stage_filmcraft-v0.9.0.json`), and `vendor/craft-sp1b/` and `vendor/craft/_keep/` are gone (test `hygiene.after_sp1b`).
3. **`avail_mb_min` of a stage** is the smaller of the guard's 5 s poll and, from the second version of the harness on, the 0.25 s sampler. The three fetch stages were run with the first version, so their minimum is the guard's: a stage of about
   13 s with a download of 4 s can fall between two polls. Their real peak is better estimated from sizes: tarball + CLI member + outputs = PhotoCraft 79 + 64 + a few = about 150 MB, VectorCraft 119 + 95 = about 215 MB, LightCraft 104 + 98 = about 205 MB
   (guard-polled drops: 79, 119, 104 MB). All were under their planned figures (202, 286, 254 MB) and far under the plan table's estimates (300, 450, 350 MB). The lowest `avail_mb_min` in any stage envelope is 610 MB (FilmCraft).
4. **df before and after.** FilmCraft stage start Avail 690 MB (with the 67 MB kept tarball on disk); LightCraft stage end 776 MB. The difference is the kept tarball plus other jobs' writes and frees on the shared volume; the per-stage deltas of the three fetch
   stages are 0, -3 and 0 MB.
5. A stage that already ran is not run again by `run_sp1b.sh --all` (its tarball is deleted and a second fetch would need a recorded ledger exception), so `tests/spikes/run_tests.sh --all` is re-runnable without any download.
6. **"all resolve from the file's own folder" in the T3 findings** means, for a relative reference, that the file exists at that path resolved from the exported file's folder; for an absolute `file://` reference (FCP7 XML and FCPXML) it only
   means the file exists at that absolute path on the machine that exported it, which says nothing about portability: the `forms` field is what tells them apart.
