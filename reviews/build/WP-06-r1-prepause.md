# Fable review: WP-06 round-trip emitters and validators (ORA, SVG ids, OTIO), round 1 of 3

Reviewed Mon 19 Oct 2026 on branch `build/process-lock`. Read: `build/reports/WP-06.md`, every file under `pipeline/roundtrip/`, `tests/roundtrip/`
and `build/evidence/wp06/`, the reused fixtures (`make_ora.py`, `check_ids.py`, `at-layers.ora`, `make_otio.py`), build plan 4.2, 4.3, 4.8 to 4.12 and the
WP-06 section, DECISIONS W-06, W-14, W-22, D-11, D-12, D-26, D-28, S-01.

**Verdict: revise** (one critical issue; correctness 3). The work is strong and most of it is ready: every planted defect in the plan is caught by name, the
Inkscape finding is real and well recorded, the reused fixtures are untouched, the evidence carries no identifying data, and the test pictures are plain
geometric cards. What blocks approval is that the headline acceptance test does not pass in the tree as handed over, and the evidence folder now
contradicts the report; two validator holes found by my own break tests should be closed in the same pass.

## What I re-ran

| Test | Result |
|---|---|
| `run_checks.py --mode all` (evidence redirected to my scratch folder so the package's own files were not overwritten) | **101 PASS, 1 FAIL, 2 UNVERIFIED** in 15 s; exit 1. The FAIL is `hygiene.no_pycache`: a git-ignored `tests/roundtrip/__pycache__/plant.cpython-313.pyc` (created 05:36, seconds after `make_evidence.sh` finished) sits in the tree. Everything else passed, including the plug-in adapter probe over the network. |
| `bash pipeline/roundtrip/svg_roundtrip.sh --out <scratch>` | exit 0; clean pass-through 0, three planted defects 1 each with the named reasons, two touch-ups and Inkscape format 0; 18 of 18 `data-*` and 17 of 17 ids survive. |
| `emit_otio.py` then `validate_otio.py --with-otio <scratch>/venv-otio/bin/python` | exit 0; 27 checks, 0 FAIL, 0 WARN; opentimelineio 0.18.1 loads it and `metadata.filmcraft` survives a write and read. |
| `public_lint.py --paths` on the owned paths, the evidence and the report; `--theme` guard; `stale_check.py --new-only` | 0 findings, 0 findings, nothing in the owned paths. |
| Looked at the generated pictures (ORA merged image, test card 01, the rig) | geometric cards, grids, discs, colour bars, the words "TEST CARD", "CH01 S01", "TEST 24"; nothing figurative, no symbol (D-28, build plan 4.10). |

## My break tests (eleven; the four that matter)

| # | Input | Expected | Got |
|---|---|---|---|
| B1 | OTIO whose only Video track has **no children** (a stack marker keeps `markers_present` happy) | a failure: nothing to hand to FilmCraft | **exit 0, 21 checks, 0 FAIL** |
| B3 | the four clips moved into a **nested Stack inside the track** (OTIO allows this; an NLE export can do it) | the clips checked, or a refusal | **exit 0**: the walker only reads a track's direct children, so zero clips are seen and every per-clip rule passes vacuously |
| B2 | `target_url` = `media/../media/ch01_s01.png` | a failure: the emitter refuses `..` in a spec, and a hand-off folder must be copyable as a unit | **exit 0** (`os.path.normpath` resolves it and the file is found) |
| B4 | `at-layers.ora` with `opacity="1.5"` | `layer_value_invalid` | only a **WARN**, exit 0: `values_valid` is soft outside the pipeline profile, which the README's "naming and attribute rules are WARN" does not say |

The rest held: `x="-5"` and `x="12.5"` on a layer fail by name; a single 48 fps RationalTime fails `rate_not_24`; a whitespace-only change to `data-pivot` and a
changed `data-z` value both exit 1 from the raw `check_ids.py`; `kb_scale --seq 1920x1080x5` exits 2; a 300-frame hold on a still is refused with a message
that names `still_available_frames`.

## Scores

| Rubric | Score | Why |
|---|---|---|
| Correctness | **3** | Every rule in the plan works and names its reason; `kb_scale` is exact and rounds cover upward on purpose; template parity at 24 fps is proven. But (a) `run_tests.sh --all` exits 1 in the handed-over tree, and `build/evidence/wp06/tests.jsonl` (103 envelopes, written 06:26 by a later `--quick` run) records that FAIL while `summary.json`, `tests_all.txt` and the report say 102 PASS, 0 FAIL; (b) a timeline with no visible clip (B1, B3) and a `..` media path (B2) pass the OTIO validator. |
| Safety and privacy | **5** | No family media, nothing fetched as if real; every fixture generated at test time and removed; validators read-only, Inkscape run with a throw-away profile; probe JSON and transcripts redact folders by design; lint and theme guard clean; nothing a search could tie to a person. The four adapter plug-ins are extra PyPI code run in `--all` only, pinned, in a throw-away venv: acceptable, and named in the README. |
| Maker usability | **4** | Clear headers, exit codes stated everywhere, PASS/FAIL rows with the reason, two-line run instructions. Gaps: `emit_otio.py` says "see the README for every field" and the README has no field table for the spec; the example spec's marker comment ("start of the third shot's dissolve" at frame 216) is wrong for a 12 + 12 dissolve, which will mislead the first person who writes a real chapter spec. |
| Fidelity to plan | **4** | All deliverables present, fixtures reused unchanged (checked by a test), 24 fps throughout, owner paths respected, nothing committed. Deviations D-1 to D-7 are honest and justified; the venv ran outside the guard under the plan's own under-100 MB rule, with the refusal recorded. |
| Maintainability | **4** | Small, single-purpose tools; shared helpers in `rt_common.py`; planted defects in one table; non-obvious choices commented (why the gate exists, why cover rounds up). `run_checks.py` is long but linear. Evidence file naming lets two runs clobber each other (see nudge 6). |

## Critical issue

1. **The acceptance test `bash tests/roundtrip/run_tests.sh --all` exits 1 in the tree as handed over**, because `hygiene.no_pycache` fails on a stray,
   git-ignored `tests/roundtrip/__pycache__/`, and the package's own evidence now disagrees with its report (`tests.jsonl` holds 1 FAIL; `summary.json`,
   `tests_all.txt` and `build/reports/WP-06.md` say 0). A hygiene test that any later tool can trip by importing `plant.py` without `-B` is not a test of this
   package's behaviour. Fix the test (nudge 1), re-run `make_evidence.sh`, and make the report's numbers match the files.

## Nudges (at most six)

1. `tests/roundtrip/run_checks.py`, `t_pycache` (line 277): record the `__pycache__` folders present at start and fail only on ones that appear during the run
   (or delete pre-existing ones under the owned paths at start, since `git check-ignore` shows they are ignored junk); then re-run `bash tests/roundtrip/make_evidence.sh`
   so `tests.jsonl`, `tests_all.txt`, `summary.json` and the report agree, and remove the leftover `build/evidence/wp06/.counts.json`.
2. `pipeline/roundtrip/validate_otio.py`, `validate()` after the clip loop (about line 180): add a `clips_present` check that FAILs `no_clips` when no Video
   track holds a Clip, and a `track_children_flat` check that FAILs `nested_composition` when a track child is a Stack or Track (B1 and B3 exit 0 today);
   add both to `plant.OTIO_DEFECTS` and the docstring rule table.
3. `pipeline/roundtrip/validate_otio.py`, line 197: treat a `..` segment in `target_url` as a failure (`target_url_escapes_folder`), the same test
   `emit_otio.is_rel` applies (B2 passes today); plant it.
4. `pipeline/roundtrip/validate_ora.py`, lines 199 to 200: make `values_valid` strict in both profiles (opacity, visibility, composite-op and whole-number x, y are
   structural, not naming; `at-layers.ora` still passes), or else say in the README "Two profiles" paragraph that values are soft in the reference profile. Today
   `opacity="1.5"` in a reference file is a WARN (B4).
5. `pipeline/roundtrip/README.md` (OTIO section) and `spec/neutral_timeline.example.json`: add the field table for `lj-neutral-timeline/1` that `emit_otio.py`'s
   docstring promises (`schema`, `name`, `synthetic_media`, `fps`, `sequence`, `still_available_frames`, `markers[]`, `shots[]` with `id`, `source`, `source_size`,
   `duration_frames`, `motion{scale, position, ease}`, `transition_out`, `markers`; `audio[]` with `id`, `source`, `start_frame`, `duration_frames`, `gain_db`,
   `duck_against`), and fix the example's second marker: with a 12 + 12 dissolve the dissolve into shot 3 runs 228 to 252, so either put `at_frame` at 228 or
   reword the comment.
6. `tests/roundtrip/run_checks.py` `main()` (line 856) and `make_evidence.py`: write `tests_<mode>.jsonl` (`tests_quick.jsonl`, `tests_all.jsonl`) instead of one
   `tests.jsonl`, so the shared WP-11a runner's later `--quick` run can no longer overwrite the `--all` evidence the report cites (that is exactly what happened at 06:26).

## Findings worth carrying forward (no change asked of WP-06)

* `check_ids.py` prints an element kind change but exits 0 (D-2 in the report). The one-line fix in the fixture is the orchestrator's; until then every caller
  must go through `svg_rig.py gate`, as the report tells WP-10.
* opentimelineio 0.18.1 alone writes none of EDL, FCPXML, Kdenlive or MLT; the four plug-in packages do, at 24 fps. WP-11b's hand-off choice (FilmCraft's own
  export first) is confirmed by evidence.
* Inkscape 1.2.2 plain-SVG export keeps every `data-*` attribute and every authored id, adds ids of its own to id-less elements, and moves a group by adding a
  `transform` while leaving `data-pivot` as it was. VectorCraft (WP-10) and Windows Inkscape remain UNVERIFIED, correctly.
* The disk guard refused the venv stage at 304 MB Avail; the volume read 446 MB when I started and 485 MB after my run. Q-1 (the pip cache) still needs an answer.

Nothing in this package could tip off the mother; nothing names a person, place or device.
