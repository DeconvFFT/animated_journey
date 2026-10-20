# Package k4-week3-plan: report

*Tue 20 Oct 2026, a Sonnet implementor on branch `build/process-lock` (HEAD `7805c1d`). The task was to write the week-3 work packages for Mon 26 Oct to Sun 1 Nov, modelled on `build/BUILD-PLAN-W1-2.md` but much shorter, with every dependency on the maker's Sun 25 Oct answers marked TO-CONFIRM and given a default, so the orchestrator can finalise the plan in one pass on Mon 26 Oct. Everything is text; nothing is built, committed or pushed; `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` and `.claude/` are untouched. Where this report says `<session scratchpad>`, the path holds the cloud session's id and is not written out (D-26).*

## 1. What changed (files)

| File | What |
|---|---|
| `build/BUILD-PLAN-W3.md` | **new**, 248 lines. Section 0 states the week numbering and maps it (the build's "week 3" is `ROADMAP.md`'s "Wk 2" by dates and the Wk 3 row by agent work), lists eight packages W3-01 to W3-08, and gives the maker's week. Section 1 is the TO-CONFIRM table (T-1 to T-7, each with its default, what it touches and an empty "Answer (Mon 26 Oct)" column). Section 2 maps the W-06 must-pass list. Section 3 holds the few conventions that are new. Section 4 has the eight packages (waves, owner paths, deliverables, acceptance commands, UNVERIFIED). Sections 5 to 8: day table with Fable read dates and the critical path, assumptions A-1 to A-7, what is not in the plan, risks. |
| `build/reports/w3k-k4-week3-plan.md` | this report |
| `build/evidence/**` | rewritten by the final `--quick` run (timestamps, available-disk figures); see section 3 |

No other file was edited. The plan's checker script lives in `<session scratchpad>` and is not part of the repository.

## 2. The plan in brief, and the judgment calls inside it

Eight packages. W3-01 reads the Saturday paste and freezes the pins; W3-02 prepares the Mon 2 - Thu 5 Nov hand-offs (a round-trip guide and the Gujarati slice fixture); W3-03 is the local Whisper route and the error counter; W3-04 holds `derive_album_look.py` on stock prints, `venue.json` with `venue_calc.py` and the coverage-strip script; W3-05 is the r1 re-run at 24 fps and `r10_conform_footage` (due Fri 6 Nov, planned Thu 29 Oct); W3-06 is the three W-31 skill drafts; W3-07 is the W-58 researcher matrix plus the Haiku templates, treatment skeleton and polish; W3-08 is the 14th test area, the readiness-map refresh and the status page.

1. **Week numbering.** The gate (`reviews/build/w2t-gate-r1.md`, orchestrator item 6) says the build calls Mon 26 Oct "week 3" and `ROADMAP.md` calls it "Wk 2". I reconciled it as: build week N does the agent rows of ROADMAP row N, and from week 3 the build runs one calendar week ahead of the table, so the Wk 3 agent rows (derive_album_look, Whisper, coverage strip, venue, r10, three skills, templates) are done Mon 26 Oct - Sun 1 Nov, while the maker's rows and the gates of those days stay Wk 2's. This is read from the readiness map's "week 4 (ROADMAP row 4)" wording and is assumption A-1.
2. **Default for the Diwali-week case is A.** Case A is the superset for agents (every hand-off for Mon 2 - Thu 5 Nov is ready by Fri 30 Oct); B and C only defer maker rows. Default for hours is "H unknown, the 9-minute plan stands" (ROADMAP section 7, W-02).
3. **Seven TO-CONFIRM rows.** The brief named five answers; hours and the Diwali-week case are split into two rows (T-1, T-2) because they touch different fields, and the house's languages are added (T-7, Q5/O-10) because the Whisper route and the captions draft need a language code and D-31 only gives the default.
4. **W3-02 is my addition (J).** The readiness map says the Mon 2 - Thu 5 Nov items need no week-3 agent output, but no pasteable Windows guide exists for the three round trips, and the Gujarati slice fixture for the project Android (C15) has to be made after the Sat 31 Oct reader confirmation. Saturday's guide already runs `check_ids.py` on the saved SVG, so the new part is the ORA and OTIO read-back; the plan says the guide shrinks if the Saturday paste covers more.
5. **The real venue file is `venue.local.json`, not `venue.json`** (O-21 names `venue.json`), because the repo is public and the venue is where the surprise happens; `*.local.*` is already ignored. Assumption A-3.
6. **r10 lives in `pipeline/recipes/`**, because W-59's `recipes/` folder is inside the installed skill. A staged copy of `free-creative-toolchain` points to it (A-5).
7. **One new test area (`tests/wk3/`), quick capped at 45 s**, with the budget rule: 374 s (slow host) plus 45 s stays under the 450 s budget; the budget is raised with a dated note only if the Fri 30 Oct run is over 420 s.
8. **Hand-overs are named.** Where a package must touch a file a week 1-2 package owned (`win/pins.json`, three comment lines, `check_ledger.py`, one integration check), the plan lists it as the only edit.
9. **No tracked media.** Fixtures are generated at test time; the plan adds no image to Git.
10. **Not taken:** build week 4's rows (`lj.ps1 close` v1, manifest schema, MO8 scribe pass, cue map header, scrubber page, `timeline.json` validator and emitters), and the orchestrator-owned items (SP4 overnight run, SP3 figures, G1 re-time, installs). Section 7 of the plan lists them.

## 3. Commands and results

| # | Command (foreground, with a timeout) | Result |
|---|---|---|
| 1 | read `CLAUDE.md`, `build/BUILD-STATUS.md`, `build/evidence/P-LOCK-readiness-W2.md`, `build/BUILD-PLAN-W1-2.md`, `reviews/build/w2t-gate-r1.md`, `QUESTIONS-SUN-25-OCT.md`, `ROADMAP.md` sections 6 and 7, the W-06, W-22, W-31, W-58, W-59 and W-63 rows, the k1 and k2 reports | done; the facts the plan cites were checked against them |
| 2 | a session-scratchpad script over the plan: line count, ASCII, register-ID existence, weekday of every "Mon 26 Oct"-style date, every backticked path | 248 lines; no non-ASCII character; 43 register IDs cited and all exist in `DECISIONS.md`; 0 weekday mismatches (2026 dates); 31 cited paths exist; the remaining backticked names are planned new files or bare names of existing files (checked with `find`: `check_ids.py`, `at-layers.ora`, `ch01.otio`, `derive_album_look.py`, `venue_calc.py`, `r1_kenburns.sh` and the rest) |
| 3 | `spec_check.py --list-profiles` (with and without `--profiles-file pipeline/phone/profile.json`), `colour_patch.py --help`, `phone_check.py --help` | the profile names `master_prores422hq` and `phone_1080`, the `--derive-from` option and the `fill_20x9` scenario that the plan's acceptance lines use all exist; `windows_check.py - --tier-json-out` is in its own usage text |
| 4 | `python3 -I scripts/pr4_parity.py` | PASS (21 verbatim copies in 12 files, 6 clause-aligned lines); the plan's W3-07 line asks for it to stay green |
| 5 | `python3 -I scripts/public_lint.py --paths build/BUILD-PLAN-W3.md` | 1 file, 0 identifying-data, 0 hygiene findings |
| 6 | `python3 -I scripts/stale_check.py --new-only` | exit 0: 0 new FAIL, 0 new WARN, 0 baseline hits gone |
| 7 | `bash build/run_all_checks.sh --quick` **exit 0** (07:53 to 07:59 UTC, foreground, 4 vCPU, 14.5 GB free). Part A, global checks: 14 PASS, 0 FAIL, 0 BLOCKED of 14. Part B: 13 of 13 areas PASS, 0 timed out, **352 s against the 450 s budget (within)**; 367 s with Part A. Envelopes 1,105 counted: PASS 1,068, FAIL 6, UNVERIFIED 28, SKIPPED 2, BLOCKED 1. The 6 FAIL and the 1 BLOCKED are the recorded ones the runner names itself (WP-07's two 0.8.0 fallback envelopes, WP-10's four read-back findings, the deliberate disk-guard proof); the "lowest `avail_mb_min` 100 MB (WP-10)" line is the deliberate disk-floor test, not a reading (disk never fell below 14,456 MB). Six more PASS envelopes than the status page's 1,099, from other packages' new tests in the shared tree (`roundtrip` 111, `sp1` 57, `spikes` 79 and `integration` 46, against 109, 56, 77 and 45 on the status page). This package added no test and changed no code |
| 8 | `python3 -I scripts/public_lint.py --paths` over both files of this package, after the report was final | 2 files, 0 identifying-data, 0 hygiene findings, exit 0 (also after the quick run; `stale_check.py --new-only` exit 0 again) |

The acceptance blocks inside the plan for packages that do not exist yet (`tests/wk3/...`, `read_paste.py`, `transcribe_local.py` and the rest) were not run; they are proposals for the implementors. Only the existing tools they call (`spec_check.py`, `colour_patch.py`, `phone_check.py`, `windows_check.py`, `public_lint.py`, `stale_check.py`, `pr4_parity.py`) were confirmed to exist with those options.

## 4. UNVERIFIED

* Everything Windows (the plan's PC halves are proposals, as in every earlier plan).
* That the week-4 row of the mapping is what the orchestrator means (A-1).
* The new thresholds in the plan (cast angle 1 degree, black and white 0.02, the 20 ms sync mark, 2-year dark stretches, the 45 s area cap, about 140 MB peak for the r10 matrix, 2 hours for the round-trip sittings) are the planner's (J), not measured.
* That the kept faster-whisper environment still imports, and that the container can make speech for the Whisper test: not checked here (the plan falls back to a tone-and-noise clip and marks accuracy UNVERIFIED).
* That the Saturday paste will follow the guide's line formats closely enough for `read_paste.py`; the plan names the fallback.
* Whether the 14th area keeps the quick pass under 450 s on a slower host: 374 + 45 is arithmetic, not a run.

## 5. For the orchestrator

1. **Mon 26 Oct, one pass.** Open `build/BUILD-PLAN-W3.md` section 1 and fill the last column for T-1 to T-7 from the Sun 25 Oct answers; where the answer equals the default, write "as default". Edit only the fields the "touches" column names. Nothing else in the plan depends on an answer. If the Diwali case is C (T-2), W3-08 drafts the exception rows of the readiness map 7.3 as text; writing them into `ops/gate_log.csv` is yours.
2. **Confirm or veto the assumptions** in section 6 of the plan, especially A-1 (week mapping and build week 4 = ROADMAP Wk 4 agent rows), A-3 (`venue.local.json`), A-5 (`pipeline/recipes/` for r10) and the (J) addition W3-02.
3. **Register and roadmap, only if you want them (I did not touch them):** W-59 names `recipes/r10_conform_footage`; the file will be `pipeline/recipes/r10_conform_footage.py`. O-21 says "put the six answers in `venue.json`"; the tracked file is `venue.example.json` and the real one `venue.local.json`. `ROADMAP.md` row 196 could carry "agent rows done in build week 3, Mon 26 Oct - Sun 1 Nov" so the table and the build agree; the dates stay.
4. **Skills to install later (not now):** `skills-staging/free-creative-toolchain/` (W3-05, r10 row and 24 fps forms) and the three W-31 drafts (W3-06) arrive staged with a `CHANGES.md` each; `docs.staged_skill_update` reads that file. The five skills staged by k2 are still waiting for your install.
5. **Open items I left where they were** (BUILD-STATUS): issue 8 (`svg_rig.py gate`), 9 and 20 (SP4, SP3 figures), 24 (the two register codes in the Sunday sheet, decide by Sun 25 Oct), 25 (scratch), 28 items 4 and 5, and the code-touching half of issue 29, which W3-08 takes by name. The plan does not repeat the issue table; `build/BUILD-STATUS.md` stays yours until W3-08 writes its section on Sun 1 Nov.
6. **Early start.** The core of W3-03 to W3-07 needs no answer, so you may start it before Mon 26 Oct if the agents are idle; mind the bench and disk locks.
7. **Evidence churn.** The final `--quick` run rewrote `build/evidence/run_all_checks_quick.txt`, `INDEX.md`, `week2_summary.json`, `wave1_quick.txt` and the per-area files, as every package's run does; decide at commit time which evidence to keep. Other packages were editing the shared tree while this ran.
