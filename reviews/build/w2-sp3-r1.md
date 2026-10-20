# Fable review: W2 spike SP3 (Blender bpy route, first real run), round 1

*Reviewed Tue 20 Oct 2026 on branch `build/process-lock`. Package: `build/reports/w2-sp3.md`, the SP3 row and closing bullets of `spikes/VERDICTS-W2.md`, `spikes/sp3_blender/{README.md,run_sp3.sh,test_cleanup.sh}`, `build/evidence/w2-sp3/*`, `build/evidence/wp10/sp3_results.txt`. Every figure in the package is a Linux container result on a neutral stand-in scene (primitives only) and is labelled so; nothing in it is evidence for Windows or for a GPU.*

**Verdict: APPROVE.** Scores: correctness 4, safety and privacy 4, maker usability 4, fidelity to the plan 4, maintainability 4. No critical issue open. Four non-blocking nudges below. The SP3 row stays **Partial**, which is the right word: the route works in the container, and the pass mark ("one real hero frame within 2x the table") is not judged until the real kitchen exists at G1.

## 1. What I re-ran myself (repository root, Avail 14,479 MB)

| Test | My result | Matches the report |
|---|---|---|
| `bash spikes/sp3_blender/test_cleanup.sh --script <run_sp3.sh at HEAD, before the fix>` | `work folder left behind: yes; 'unbound variable' in the output: yes`, FAIL, exit 1 | yes (the defect is real and the old script reproduces it) |
| `bash spikes/sp3_blender/test_cleanup.sh` (the fixed script) | `work folder left behind: no`, PASS, exit 0 | yes |
| `bash spikes/sp3_blender/run_sp3.sh --check` | wheel 401,697,653 bytes read from PyPI, tarball 383,295,504 bytes, Python 3.13.16, `py_compile ok`, `READY: Avail 14479 MB is at least 3500 MB`, exit 0 | yes |
| `--run` under a fake `df` of 3,499 MB (`LJ_DF_CMD`) | `NOT RUN: needs >= 3.5 GB free (Avail 3499 MB; short by 1 MB)`, `Nothing was started and nothing was forced.`, exit 3, no scratch folder made | yes (the refusal still works after the edit) |
| PyPI metadata for `bpy==5.2.2` (`pypi.org/pypi/bpy/5.2.2/json`, read now) | `bpy-5.2.2-cp313-cp313-manylinux_2_28_x86_64.whl`, 401,697,653 bytes, sha256 `3dfd1a9e...666d45`, uploaded 2026-09-15 | yes: the size and digest in `summary.json` are PyPI's published ones |
| `python3 -I tests/spikes/check_verdicts.py` | `5 main rows, 6 SP1 test rows; complete` | yes |
| `python3 -I scripts/public_lint.py --paths` over the report, the evidence folder, the spike folder and `VERDICTS-W2.md` | 11 files, 0 identifying-data findings, 0 hygiene findings; my own grep for home paths, `user@`, IPs and session ids: none | yes |
| `git status` and `file --mime-type` over tracked and untracked files | no binary, no image, no render in the working tree; the new evidence is 40 KB of text and JSON | yes |
| Arithmetic | table means 112.45 and 204.3; ratios 0.812, 0.860, 0.834, 0.862; peak use 14,480 - 13,072 = 1,408 MB; sampler minimum 13,072 MB at 01:22:10; largest folder 1,021 MB at 01:28:20 | yes, every figure recomputes |

**Are the results real, not stale or simulated?** Yes. The independent `lj_guard` ledgers outside the repository corroborate the run: `disk-ledger.jsonl` has one `sp3-blender` line (planned 3100, start 14480, min 13077, end 13459, lock wait 281 s, status ok, exit 0; 01:19:59 to 01:28:19) and `bench-ledger.jsonl` has four back-to-back lines whose start and end stamps (01:22:12, 01:22:24, 01:23:47, 01:25:22, 01:28:19) and load figures (0.58, 1.21, 3.63, 4.01) are exactly the ones the report and `summary.json` quote; the gaps between them are the RESULT wall times plus about one second of scene load. The 2 s `df` sampler (707 lines) shows the 1,021 MB folder appearing during pip and staying until 01:38, which is the T8 defect seen from the outside. Nothing in the evidence could have been produced by the 19 Oct dry run.

**My own full render re-run did not complete.** I started a review copy (own empty folder in my scratchpad, `pip download` of the wheel, a SHA-256 comparison against the PyPI digest, then one 8-sample and one 64-sample-plus-denoise render under `lj_bench`), but the 402 MB fetch through the proxy had moved about 1 MB in several minutes when the review window closed, so I stopped it and removed every folder it made (nothing landed in the repository or in `build-scratch`; no bench or disk ledger line was written by me). So the wheel's digest is still compared only by pip's own index-fragment check at install time, not by a recorded `sha256sum`; the implementor flagged exactly this under UNVERIFIED, and nudge 1 turns it into a recorded check next time. The timings themselves I accept on the strength of the ledgers above and on their agreement (0.81x to 0.86x, two runs of one line within 0.9 percent) with the 18 Oct table, which was a different session.

## 2. Tests designed to break it

1. **Does the fix survive a failing step as well as a successful one?** With the old script the trap only worked when `die` fired inside the function; with the fix `S` is global and the trap text falls back to `/nonexistent-sp3-scratch`, so both paths delete the right folder and neither can delete `/`. `lj_guard.sh` defines no `S` of its own, so the global does not collide. **Held.**
2. **Does the old test suite still see what it expects?** The dry run at a fake 5,000 MB prints the stage and does nothing; the refusal at 3,499 MB exits 3 with no scratch folder (above). **Held.** (I did not run the full `tests/spikes/run_tests.sh`; see nudge 2 for why that matters.)
3. **Do the verdict words follow from the evidence?** "Partial" is right on both counts the file defines: the spike ran to a result here, and the stated pass mark cannot be applied before G1. The row's "Next step" names the date, the real figure (about 1.9 GB) and the rule to apply ("dropped, or moved to the PC"). The closing bullets no longer say SP3 is unrun. **Held.**
4. **Retired spellings.** The stand-in scene file and the 18 Oct table call the scene a "voxel kitchen" (both predate D-29 and are allowlisted as research record); none of the new SP3 files uses "voxel" or "Minecraft". `stale_check.py --new-only` reports two new hits, both in `spikes/sp1_craft_cli/VERDICT-SP1A.md` (not this package; handed to the orchestrator in section 9). **Held for SP3.**

## 3. Correctness (4)

Eight tests, one honest FAIL in the script and not the route, the defect found, explained (an EXIT trap outliving a `local`), fixed in the smallest way and regression-tested against both the old and the new script. The table is read correctly as the mean per configuration, the 2x limits are right, and the contamination flags are explained with the data that explains them (the previous line's own load; the clean first line and the clean repeat agree within 2 percent). Not a 5 because the digest comparison is still missing from the record and because the report leaves two bench-ledger entries after the run unexplained (nudge 3).

## 4. Safety and privacy (4)

No family media: the scene is primitives, the renders were never added to git and were deleted. The repository is public and nothing identifying landed in it: machine class only ("Intel Xeon 2.10 GHz (class only)"), scratch paths written as `<scratch>`, no hostnames, no session ids, no emails. The download was a pinned PyPI wheel into a fresh venv in the scratch folder, installed with `--no-cache-dir`, and the 402 MB counted against the 2 GB allowance in prose. Not a 5 because that fetch is not on any download ledger row (the WP-07 ledger holds the Craft tarballs; the fortnight's total now sits near 1.1 GB with the WP-07 re-fetches and this wheel, and nobody can read that from one file), and because the run installed without `--require-hashes`, so the digest check rests on pip rather than on a line the orchestrator can read (nudge 1).

## 5. Maker usability (4)

The maker never touches this spike; what she gets is the planning sentence in section 6 (about 94 s a Cycles frame here, about 4 s a Workbench draft, so drafts in the container and finals on her PC, which is W-23 as decided) and the clear statement that her Exercise 5 timings are the Windows and GPU evidence. The README's first-run table reads at a glance. The UNVERIFIED lists in the report and the README are complete and match each other.

## 6. Fidelity to the plan and DECISIONS.md (4)

Build plan WP-10 item 2 asked for exactly this: `--check`, then `--run`, on the neutral stand-in, with the pass mark held for G1. The disk decision step 3 in `VERDICTS-W2.md` is updated in place with the real peak (1,408 MB) and the planned figures left for the orchestrator, as the rules say. The quoted decision rule gained one clarifying sentence rather than a reword. W-23 (hero shots as Workbench drafts and sharded Cycles finals, no family imagery) is respected and the pixel-identical repeat is the right test for sharding. No CHARTER, DECISIONS, ROADMAP, PLAN-ON-A-PAGE, CLAUDE.md or `.claude/` file was touched; nothing was committed.

## 7. Maintainability (4)

The fix carries a comment that says why `S` is global; `test_cleanup.sh` documents the defect and how the shim works, and runs in seconds with no network. Two things keep it from a 5: the regression test is not called from `tests/spikes/run_tests.sh`, so the next sweep can miss a relapse (nudge 2), and a few header and output strings still describe the spike as unrun (nudge 4).

## 8. Nudges (non-blocking)

1. **Put the fetch and its digest on the record.** Add one download-ledger row for the `bpy` wheel (asset, 401,697,653 bytes, the PyPI sha256, date, fetch 1, stage `sp3-blender`) in a file the allowance check reads, and make `run_sp3.sh` install from a one-line requirements file with `--require-hashes` carrying that digest, so the next run (G1) compares the download against its sum and prints it.
2. **Wire `test_cleanup.sh` into `tests/spikes/run_tests.sh`** (quick suite; it needs no disk or network) and re-run the suite once when the CPU is free, so the WP-10 assertions on the 3,100 and 3,500 figures and the new regression test are checked together.
3. **Account for the two `py` bench-ledger lines after the run** (01:28:27, exit 1 after 313 s; 01:33:49, 20 s). They are the load behind the Workbench line's contamination flag, and the report should say what they were (the device probe, the compares, or an aborted attempt).
4. **Retire the stale "not run" strings**: `do_check` still prints "prepared, NOT run" in its first line; the script header still says "SP3 runs in week 3 either on the maker's PC ... or here after at least 3.5 GB is free"; the README still lists "Earlier numbers" as if no later ones existed. One pass by the scribe.

## 9. For the orchestrator

* The two decisions the report hands up are real and both are yours: whether to lower the planned and entry figures (1,408 MB peak measured; about 1,900 MB would do) with the WP-10 test assertions updated in the same change, and whether `lj_bench` should ignore load left by the stage's own previous process.
* Outside this package: `stale_check.py --new-only` flags two new `S-01.at-25-fps` hits in `spikes/sp1_craft_cli/VERDICT-SP1A.md` (the SP1 lean run's regenerated verdict), not in SP3's files.
* My aborted review re-fetch moved about 1 MB and left nothing; it does not change the allowance arithmetic.
* G1 (Sun 15 Nov): re-time the four configurations on the real kitchen frame with the hash check from nudge 1 in place, then apply "dropped, or moved to the PC".
