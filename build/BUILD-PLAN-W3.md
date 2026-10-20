# Build plan, week 3: Mon 26 Oct - Sun 1 Nov 2026

*Written Tue 20 Oct 2026 by a Sonnet implementor (package k4-week3-plan) on branch `build/process-lock`. A proposal for the orchestrator to finalise in one pass on Mon 26 Oct, once the maker's Sun 25 Oct answers are in (section 1). Nothing in it has been built. `DECISIONS.md` wins over this file and `ROADMAP.md` wins on dates. Modelled on `build/BUILD-PLAN-W1-2.md`, much shorter: its section 4 (evidence envelope, exit codes, disk and bench locks, the redaction file, definition of done) carries over unchanged and is not repeated. Windows behaviour is UNVERIFIED throughout.*

---

## 0. In one page

**Which week is this?** The build calls Mon 26 Oct - Sun 1 Nov "week 3". `ROADMAP.md` section 7 calls the same days **"Wk 2"** and calls Mon 2 - Sun 8 Nov "Wk 3". Both are right: the build ran its weeks 1-2 in two days (Mon 19 - Tue 20 Oct; gate `reviews/build/w2t-gate-r1.md`) and has since run one calendar week ahead of the table.

| Build week | Runs | Does the agent rows of ROADMAP | That row's own dates |
|---|---|---|---|
| 1-2 (closed) | Mon 19 - Tue 20 Oct (planned to Sun 1 Nov) | Wk 1 and Wk 2 | Mon 19 Oct - Sun 1 Nov |
| **3 (this plan)** | **Mon 26 Oct - Sun 1 Nov** | **Wk 3**, plus the Wk 2 leftovers (W-58 matrix, craft-motion 25 to 24, carry-forward polish) | Mon 2 - Sun 8 Nov, so one week early |
| 4 (next plan) | Mon 2 - Sun 8 Nov | Wk 4 (`lj.ps1 close` v1, manifest schema, MO8 scribe pass, cue map header) | Mon 9 - Sun 15 Nov |

The maker's rows, the gates and the fixed dates of Mon 26 Oct - Sun 1 Nov stay **Wk 2's**. Pulling agent work forward moves no deadline (D-21): r10 stays due Fri 6 Nov, the three skills Sat 14 Nov. The week-4 row is read from the readiness map's "week 4 (ROADMAP row 4)" wording (J); the orchestrator confirms it on Mon 26 Oct.

**What it buys.** Eight packages in three waves. No package adds a task to the maker's week that is not already on the readiness map or in ROADMAP: every Windows item of Mon 26 - Thu 29 Oct was built in weeks 1-2, and the Wk 2 Sonnet rows are done (SP1 results, the Route A spike, the container colour-patch, the first `stale_check.py` run) except the PC colour-patch paste of Thu 29 Oct (W3-01). The packages read the maker's pastes and freeze what they decide (W3-01), prepare the hand-offs for Mon 2 - Thu 5 Nov before her Diwali week (W3-02), build the ROADMAP Wk 3 tools (W3-03 to W3-05), draft the three W-31 skills (W3-06), do the researcher and scribe rows (W3-07), and close the week with a 14th test area, the readiness-map refresh and the Fable bundle (W3-08).

| ID | Title | Wave | Runs | Size | Agent | TO-CONFIRM | Done by |
|---|---|---|---|---|---|---|---|
| W3-01 | Saturday-paste reader, pin freeze, tier filing | 1 | container | S | sonnet | T-4 T-5 T-6 | Tue 27 Oct |
| W3-02 | Hand-offs for Mon 2 - Thu 5 Nov: round-trip guide, Gujarati slice fixture | 2, 3 | both | M | sonnet | T-2 T-4 T-5 | guide Thu 29; fixture Sun 1 Nov |
| W3-03 | Local Whisper route and the correction-test kit | 1 | both | M | sonnet | T-4 T-6 T-7 | Thu 29 Oct (maker's test Sun 8 Nov) |
| W3-04 | Planning tools: album look, venue numbers, coverage strip | 1 | container | M | sonnet | T-3 T-4 | Tue 27 Oct |
| W3-05 | Recipes at 24 fps: r1 re-run and `r10_conform_footage` | 1, 2 | both | M | sonnet | T-3 T-4 T-6 | Thu 29 Oct (**due Fri 6 Nov**, W-59) |
| W3-06 | The three W-31 skill drafts | 2, 3 | container | M | haiku + sonnet checks | T-7 | drafts Fri 30 Oct; captions Sun 1 Nov |
| W3-07 | Researcher matrix (W-58), templates, treatment skeleton, polish | 1-3 | container | M | researcher + haiku | T-1 T-2 T-3 | Fri 30 Oct (matrix **Sun 1 Nov**) |
| W3-08 | The 14th area, readiness map refresh, status page, Fable bundle | 3 | container | S | sonnet | T-2 T-5 | Fri 30 Oct; status Sun 1 Nov |

**The maker's week (Wk 2 rows, all delivered in weeks 1-2):** Mon 26 Ken Burns by script and in the editor; Tue 27 archive and five stand-in scans, `lj.ps1 doctor`; Wed 28 encrypted container, separate account, project phones wiped, phone test; Thu 29 PC colour check and the Gujarati shaping A/B; Fri 30 pilot tape ships; Sat 31 native reader reads the 32 strings, country in the licence log; **Sun 1 Nov settings card signed and the first logged week read**.

---

## 1. TO-CONFIRM: what the maker's Sun 25 Oct answers decide (one pass on Mon 26 Oct)

Every package or field below that depends on an answer carries its `T-n` tag and runs on the **default** until the orchestrator fills the last column. Nothing else in the plan changes with an answer. Defaults are the planner's (J), not the maker's. Questions are numbered as in `QUESTIONS-SUN-25-OCT.md`.

| ID | Answer, and where it comes from | Default used until confirmed | Packages and fields it touches | Answer (Mon 26 Oct) |
|---|---|---|---|---|
| T-1 | Hours a week and rhythm (Q11, O-01) | H unknown: the 9-minute plan stands until H is written (ROADMAP section 7 "Hours"; W-02); F-0 (6 minutes) only if the first logged week, read Sun 1 Nov, is under about 8 h. Load on the maker from this plan: none; Mon 2 - Thu 5 Nov budget 3.5 h (readiness map 7.1) | W3-07 treatment skeleton (runtime slots 9 or 6); W3-02 (length of the two sittings); W3-08 calendar text | |
| T-2 | Her Diwali-week case, A, B or C of readiness map 7.2 (Q8 and Q11, O-56, O-01) | **Case A**, the table of 7.1 as written. Reason: A is the superset for agents; every hand-off the maker could use on Mon 2 - Thu 5 Nov is ready by Fri 30 Oct, and B and C only defer maker rows | W3-02 (sittings fall Mon 2 - Thu 5 Nov in all three); W3-07 (case B moves the week-3 practice tasks to Mon 16 - Sun 22 Nov); W3-08 (case C: draft the `ops/gate_log.csv` exception rows as text only) | |
| T-3 | Country and state of the premiere, countries of relatives (Q12, O-02) | Unknown. Both mains frequencies (50 and 60 Hz) and both interlaced standards are handled, so no tool needs the answer; no country-specific claim is written | W3-04 venue judder note; W3-05 matrix order only; W3-07 the matrix's `country` column stays blank; the licence-log country row (orchestrator, by Sat 31 Oct) | |
| T-4 | Shared PC or room, who runs the family accounts (Q13, O-03) | **Shared**, the worst case: every file the PC writes goes under `C:\lj\` in the project account and then into the container (W-25); every README says "separate account first" | W3-01, W3-02, W3-03, W3-05 README wording and default paths; W3-04 (the coverage strip file stays outside the repo) | |
| T-5 | Craft version pins from the Sat 24 Oct pastes, frozen Sun 25 Oct (W-22) | The pins in `win/pins.json`: PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 (fallback 0.8.0), EffectCraft 0.11.1; SoundCraft unpinned | W3-01 (reader and freeze); W3-02 (folder names `C:\lj\tools\<app>-<tag>`); W3-08 (readiness C7, `parity.pins_vs_release_assets`) | |
| T-6 | PC inventory tier (the Tue 20 Oct paste, filed as `build/evidence/pc/pc_tier.json`) | No tier file: a modest PC by the tiers of `win/tiers.json` (gpu-low so a CPU route, RAM 8-15, disk tight so an external drive, ffmpeg 9.0.2 untested) | W3-03 `models.json` (model and device); W3-05 (PC ffmpeg needs libx264 and libass); W3-01 files the tier | |
| T-7 (extra) | Languages and scripts of the house (Q5, O-10) | Gujarati first, with Hindi and Sanskrit words (D-31, W-57); Devanagari neutral strings until the reader confirms Gujarati (O-62) | W3-03 `--language gu`; W3-06 captions draft (script list) | |

Later inputs that are results, not answers (each is a dependency in section 5, none is TO-CONFIRM): the Thu 29 Oct colour-patch paste, the Thu 29 Oct shaping A/B (C14), the Sat 31 Oct native-reader confirmation.

---

## 2. P-LOCK (W-06): what this plan moves

| W-06 item | State on Tue 20 Oct (readiness map) | This week's agent action | Package |
|---|---|---|---|
| SP1 to SP5 read by Fable | SP1, SP2, SP5 done; SP3 partial (G1 Sun 15 Nov); SP4 armed, the orchestrator runs it overnight | refresh map rows C2, C4, C5 (tail-gate nudge 1); no new spike work | W3-08 |
| Five-minute tests on the five pins | maker Sat 24 Oct | read the paste, freeze the pins | W3-01 |
| ORA, SVG and OTIO round trips | maker Mon 2 - Thu 5 Nov | pasteable guide with the validators on the saved files | W3-02 |
| Settings card, hours log, inventory, Ken Burns, archive, colour-patch | maker on the dates in section 0 | file the derived tier and chain results; verify the card parity tests on Fri 30 Oct | W3-01, W3-08 |
| Encrypted drive, phone hygiene | maker Wed 28 Oct, hard stop Thu 5 Nov | wording only (T-4) | none |
| `lj.ps1 close` written and run once | v0 done; v1 is build week 4 | propose the per-app "writes under" lists from the paste | W3-01 |
| Three W-31 skills | not started | drafts; validators and emitters are build week 4 | W3-06 |
| MO8 scribe pass, manifest schema, cue map header, scrubber page | build week 4 | none (section 7) | none |
| Phone-floor chart, Gujarati burn, slice fixture, tone ladder | maker Wed 28 Oct to Thu 5 Nov | the Gujarati slice fixture (the others exist) | W3-02 |
| Whisper correction test (not a P-LOCK item; Sun 8 Nov mid-point) | maker Sun 8 Nov | the route and the error counter | W3-03 |

---

## 3. What is new in the conventions

* **One new test area, the 14th: `tests/wk3/`.** `tests/wk3/run_tests.sh` (owner W3-08) loops over `tests/wk3/*/run_tests.sh`; each package owns its subfolder and gives it `--quick` and `--all`. Quick is mechanism only: no model run, no ProRes encode, at most **45 s in all**. The runner's quick budget stays 450 s (the quick pass took 270 s and 374 s on two hosts and 342 s on Tue 20 Oct's last run here; 374 + 45 stays under). If the Fri 30 Oct run is over 420 s on a host, W3-08 raises the budget with a dated note in `scripts/run_week2_checks.sh` (status issue 14); it never lets the area drift past 60 s.
* **No tracked image or video.** Fixtures are made at test time into `<session scratchpad>`; only JSON, CSV and text are tracked. A package that thinks it needs a tracked image uses the `git add -f` route after review, under 200 KB, as K1 did.
* **Staging, not installing.** Skill drafts and patched copies of installed skills go to `skills-staging/<name>/SKILL.md` with a `CHANGES.md`; nothing under `.claude/` or any protected file is edited. Anything that would touch `DECISIONS.md`, `ROADMAP.md` or `PLAN-ON-A-PAGE.md` is listed "For the orchestrator".
* **Private data stays private.** Raw pastes live in chat or `<session scratchpad>`, never the repo; only derived files are filed. The real venue answers go in `venue.local.json` (ignored by `*.local.*`), the coverage input and strip are the maker's private data and stay outside the repo, and every new tool refuses a name-shaped ID using `scripts/redaction_patterns.json`.
* **Foreground with a timeout.** Container restarts have orphaned detached jobs; every test run is foreground. Anything writing over 100 MB goes through `scripts/lj_guard.sh`.
* **Hand-overs are named.** Where a package edits a file that a week 1-2 package owned, the edit is listed in its owner paths and is the only edit it makes there.
* **Early start.** The core of W3-03 to W3-07 needs nothing the maker answers; the orchestrator may start them before Mon 26 Oct. Only the TO-CONFIRM fields wait.

---

## 4. Work packages

### W3-01 Saturday-paste reader, pin freeze and tier filing

**Wave 1. Runs: container. Size S. TO-CONFIRM: T-4, T-5, T-6.** **Refs:** W-22, W-06, W-25, W-26, W-28, D-26, D-32. **Owner paths:** `spikes/sp1_craft_cli/read_paste.py`, `spikes/sp1_craft_cli/paste_fixtures/**`, `tests/wk3/paste/**`, `build/evidence/pc/**` (derived files only; WP-11b hands the folder over), `build/evidence/w3-01/**`. `win/pins.json` is edited once, status line only, after the orchestrator says the pins stand.

1. `read_paste.py PASTE|-` reads the text the maker pasted in chat (saved by the orchestrator under `<session scratchpad>`) in the order `MAKER-CRAFT-ZIPS.md` asks for it: five checksum lines, versions, signatures, pass or fail per app with warning words, most memory, two "where did it write" lines per app. The line formats come from `build_guide.py`, not guesswork. It compares each checksum with `release_assets.json` and each version with `win/pins.json`, and fails closed (exit 2) on a redaction hit, printing the masked hit only.
2. It writes `build/evidence/pc/craft_tests_W3.json` (derived: app, tag, verdict word, warning words, memory in 0.5 GB buckets, "writes under" as folder names relative to the app folder; no user or machine name) and prints a proposed `win/pins.json` diff: an app that fails moves to its W-22 fallback (FilmCraft 0.8.0), any other failure is asked of the maker, never chosen by the tool. The per-app table is the proposed list for `lj.ps1 close` v1 (build week 4).
3. Files the tier and the Thursday colour result with the existing tools, no change to them: `python3 -I scripts/windows_check.py - --tier-json-out build/evidence/pc/pc_tier.json` (the raw report through stdin) and `colour_patch.py --derive-from RAW --out DERIVED`. If the orchestrator filed the tier on Tue 20 Oct, this item is a check.

```bash
bash tests/wk3/paste/run_tests.sh --quick    # synthetic pastes built from the guide's formats, under 10 s
# all_pass: exit 0, five OK. one MISMATCH: exit 1, names the app. FilmCraft fail: diff proposes 0.8.0.
# wrong order: exit 2, names the line. planted profile path: exit 2, nothing written, hit masked. two runs byte-identical.
python3 -I scripts/public_lint.py --paths build/evidence/pc/craft_tests_W3.json spikes/sp1_craft_cli/read_paste.py
```
**UNVERIFIED:** the real paste's exact wording (a hand-pasted block may wrap or lose lines; the tool's named error is the fallback and the orchestrator reads by eye); everything Windows.

### W3-02 Hand-offs for Mon 2 - Thu 5 Nov: the round-trip guide and the Gujarati slice fixture

**Wave 2 (guide) and wave 3 (fixture). Runs: both. Size M. TO-CONFIRM: T-2, T-4, T-5.** (J) Readiness map 7.1 says these items need no week-3 agent output; this package supplies the pasteable guide and the one file they still need, on the model of the Saturday guide. **Refs:** W-06, W-22, W-26, W-63, W-75, O-62, D-27, D-28. **Owner paths:** `win/roundtrip/**` (`build_guide.py`, `check_guide.py`, generated `MAKER-ROUNDTRIPS.md`), `pipeline/phone/make_slice_fixture.py`, `tests/wk3/handoff/**`, `build/evidence/w3-02/**`.

1. `MAKER-ROUNDTRIPS.md`, generated like the Saturday guide (ASCII, every box parses on pwsh 7 and passes `ps_lint.py`, writes only under `C:\lj\at\`). Three sittings in the map's order, ORA first: `at-layers.ora` through PhotoCraft, saved as a copy, then `validate_ora.py` on the copy; `at-rig.svg` through VectorCraft with `check_ids.py` (the paste is the finding: rect, circle and ellipse become paths, expected, and `svg_rig.py gate` still fails a kind change, status issue 8); `ch01.otio` (K1) through FilmCraft and Resolve Free with `validate_otio.py` on what FilmCraft saves. Saturday's tests already run `check_ids.py` on the saved SVG but never `validate_ora.py` or `validate_otio.py` on the saved ORA or OTIO, so the ORA and OTIO read-backs are new and the SVG sitting is a short repeat on the pinned build; if the Mon 26 Oct read of the paste shows more was covered, the guide shrinks to a one-box addendum. About 2 hours (J) in two sittings. Test files only.
2. `make_slice_fixture.py` (container, or `py -3` on the PC): a 20-second synthetic slice (test cards, tone ladder, nobody in it) with the caption cues of `pipeline/phone/test_strings.json`, burned by the path the Thu 29 Oct A/B chose (`ass` until then), encoded as PH1 and PH2 by `encode_phone.py`. **It refuses any Gujarati cue whose `checked_by_reader` is false** (O-62) and says so; before the Sat 31 Oct confirmation it makes the Devanagari neutral version only. The file goes to the maker in chat (1 to 2 MB, synthetic, as `phone.mp4` did), never into the repo.

```bash
python3 -I win/roundtrip/build_guide.py && python3 -I win/roundtrip/check_guide.py   # all PASS; the guide equals what the builder writes (cmp)
bash tests/wk3/handoff/run_tests.sh --quick    # fences parse; every file the guide copies exists; a planted unread Gujarati cue is refused
python3 -I pipeline/phone/make_slice_fixture.py --out <session scratchpad>/slice
python3 -I pipeline/validators/spec_check.py <session scratchpad>/slice/ph1.mp4 --profile phone_1080 --profiles-file pipeline/phone/profile.json   # exit 0
```
`phone_check.py` (scenario `fill_20x9`) also passes on the fixture. **UNVERIFIED:** every Windows click, how Resolve Free imports the OTIO, how the Gujarati burn reads on the project phone at 35 cm (C15 is the maker's).

### W3-03 Local Whisper route and the correction-test kit

**Wave 1. Runs: both. Size M. TO-CONFIRM: T-4, T-6, T-7.** **Refs:** W-24 (local only), W-57, D-31, D-17 (never record her), D-26, W-06 (the test is not a P-LOCK item; Sun 8 Nov mid-point), `playbooks/story.md` Step 3 and Exercise 3. **Owner paths:** `pipeline/transcribe/**` (`transcribe_local.py`, `count_errors.py`, `models.json`, `README-MAKER.md`), `tests/wk3/transcribe/**`, `build/evidence/w3-03/**`.

1. `transcribe_local.py AUDIO --language gu --model small --out-dir DIR`: faster-whisper only (the kept container environment, rebuild line in `spikes/verdicts/template.md`; on the PC `py -3 -m pip install faster-whisper`, UNVERIFIED). `--language` is required (no auto-detect, Exercise 3). Offline guard: the model must already be in the local cache, else exit 3 and no network call. It writes only under `--out-dir` and refuses one inside a git working tree that is not ignored. Outputs: `.srt`, `segments.json` with word times, and `lines_sample.csv` with ten seeded random lines and an empty `reference` column for the maker's correction.
2. `count_errors.py REF HYP`: NFC-normalised, whitespace tokens, punctuation and digit forms stripped; prints wrong words per line and in total as "wrong / reference words". It counts and never corrects.
3. `models.json`: tier to model and device (J). Default with no tier file: `small`, CPU, int8 (the slow-CPU bracket of `playbooks/story.md` [100], about 9 minutes for 10 minutes of audio). Container timings for `base` and `small` on a 30-second clip fill the speed column; PC numbers stay UNVERIFIED until the maker's Sun 8 Nov run.
4. `README-MAKER.md`: exact PowerShell lines, outputs under the container only, "audio never goes into the project folder, Git or chat".

```bash
bash tests/wk3/transcribe/run_tests.sh --quick   # no model: missing-model exit 3 with the network blocked, output-dir guard, count_errors on planted pairs and NFC cases, under 10 s
bash tests/wk3/transcribe/run_tests.sh --all     # one `base` run, offline, on a 30 s synthetic clip: seconds and peak RAM recorded
```
Test audio is generated at test time, not tracked, and no voice is cloned. If the container cannot make speech, `--all` uses a tone-and-noise clip: the route is shown to run and the accuracy claim is UNVERIFIED. **UNVERIFIED:** Whisper accuracy on Gujarati, older voices and accents (`playbooks/story.md` TODO), and all PC timings.

### W3-04 Planning tools: album look, venue numbers, coverage strip

**Wave 1. Runs: container (all three also run on the PC with `py -3`). Size M. TO-CONFIRM: T-3, T-4.** **Refs:** W-27 (album look per batch), W-56 and O-21 (venue), W-37 and W-61 (locked rooms, never the mandir doors), D-02, D-03, D-26. **Owner paths:** `pipeline/look/**`, `pipeline/venue/**`, `pipeline/coverage/**`, `tests/wk3/tools/**`, `build/evidence/w3-04/**`. The research originals are called, never copied or edited (a test checks their `git diff` is empty).

* **(a) Album look on stock prints.** `pipeline/look/make_stock_prints.py` builds three synthetic aged stand-in prints with a known cast, black, white and grain (public-domain stock prints are used only if still in scratch, as a cross-check against `research/toolchain-fixtures/album_look_result_loc_stock.json`). `check_look.py` runs `derive_album_look.py` on them and compares with the truth: cast angle within 1 degree, black and white within 0.02 (J), `ONE_ALBUM_LOOK` false on a planted odd print, and the `-vf` string applied to a stand-in lands on the derived black and white.
* **(b) `venue_calc.py` and the venue file.** `pipeline/venue/venue_calc.py` wraps `research/cinematic-quality-fixtures/venue_calc.py`; adds `venue.schema.json` (the six venue answers of O-21, each optional with its scenario default) and `venue.example.json` (invented; no real place). It names every default still in use. With T-3 unknown it prints both 50 and 60 Hz notes. The real answers live in `venue.local.json`, not `venue.json` as O-21 says (A-3).
* **(c) Coverage strip.** `pipeline/coverage/coverage_strip.py COVERAGE.csv --out strip.svg --json strip.json`; columns `person_id,from_age,to_age,first_hand` (IDs, ages, no names, no birth year). Draws her span as one strip and lists the dark stretches of 2 years or more, longest first, as candidates for the three W-37 rooms (the pick stays the maker's) and as the opening of the her-turn conversation. The SVG is responsive: legible at 360 px wide (type 14 px or more) and on a 16:9 screen. Input only from a path outside the repo or git-ignored.

```bash
bash tests/wk3/tools/run_tests.sh --quick      # about 15 s
python3 -I pipeline/look/check_look.py --selftest
python3 -I pipeline/venue/venue_calc.py pipeline/venue/venue.example.json
python3 -I pipeline/coverage/coverage_strip.py pipeline/coverage/fixtures/coverage_synthetic.csv --out <session scratchpad>/strip.svg --json <session scratchpad>/strip.json
git check-ignore -q venue.local.json && echo ignored
```
Tests also: a name-shaped `person_id` is refused; a strip with no dark stretch says so. **UNVERIFIED:** the derived look on real prints, the real venue answers, whether the strip helps the maker.

### W3-05 Recipes at 24 fps: the r1 re-run and `r10_conform_footage`

**Waves 1 and 2. Runs: both (real footage only on the PC). Size M. TO-CONFIRM: T-3, T-4, T-6. Due Fri 6 Nov (W-59); planned Thu 29 Oct.** **Refs:** W-59, W-14, W-16, W-24, W-40, `playbooks/cinematic-quality.md` decision 12. **Owner paths:** `pipeline/recipes/**`, `tests/wk3/r10/**`, `skills-staging/free-creative-toolchain/**`, `build/evidence/w3-05/**`.

1. **r1 at 24 (Haiku's craft-motion item waits on it).** Run the Ken Burns recipe in a scratch copy with the 24 forms (`d=120`, `fps=24`, `on/119`), count 120 frames per 5 s, record it. r5 (the Kdenlive `melt` story) cannot run here: it stays "UNVERIFIED at 24" until a PC re-run. The recipes sit under `.claude/`, so the patched `r1_kenburns.sh` is staged with the skill, not edited.
2. **`r10_conform_footage.py IN --out OUT [--source-class auto|25i|29.97i|18p|24p|vfr] [--interpolate]`** (plus a `.ps1` wrapper and `README-r10.md`): 1920x1080, 24 fps, ProRes 422 HQ through the `prores422hq_master` chain of `pipeline/lib/chains.json`, BT.709 tags, PCM 24-bit 48 kHz. One rule table per class: `bwdif` for the interlaced ones; drop or repeat frames to 24; **duration preserved and audio untouched; no frame interpolation unless `--interpolate`**, which marks the output as having synthesized frames (real memories stay real). `sync_probe.py` measures the offset between a white flash frame and a 1 kHz beep after the conform: **within 20 ms, half a frame at 24 fps (J)**, and duration within one frame.
3. **The matrix** is five synthetic 3-second clips (25i, 29.97i, 18p, 24p, phone VFR) made with ffmpeg `lavfi`; ProRes 422 HQ is about 22 MB a second (176 Mbit/s, `win/tiers.json`, J), so each output is about 66 MB and is deleted after its check (peak about 140 MB, through `lj_guard.sh`). Country (T-3) only orders the matrix; both interlaced standards run either way.
4. Staged `skills-staging/free-creative-toolchain/SKILL.md` with the r10 row, its path (A-5) and the 24 forms, plus `CHANGES.md`.

```bash
bash tests/wk3/r10/run_tests.sh --quick     # refusals and the rule table, no encode, under 10 s
bash tests/wk3/r10/run_tests.sh --all       # the matrix; each class ends with:
python3 -I pipeline/validators/spec_check.py <session scratchpad>/o_CLASS.mov --profile master_prores422hq --no-loudness   # exit 0
```
Real tape never enters the container or any cloud tool (W-24); the pilot's return is not touched before P-LOCK passes, and the re-test on it is build week 4. If r10 is not landed by Wed 4 Nov, nothing is lost: no real footage is opened before Sat 14 Nov. **UNVERIFIED:** PC ffmpeg 9.0.2 (untested), the 20 ms mark on real tape, and r5 at 24.

### W3-06 The three W-31 skill drafts

**Waves 2 and 3. Runs: container. Size M. TO-CONFIRM: T-7.** Haiku drafts; Sonnet writes the checks; Fable reads each (W-06, C10). **Refs:** W-31, W-06, W-63, W-18, W-75, W-24, D-32. **Owner paths:** `skills-staging/timeline-json-and-emitters/`, `skills-staging/transcribe-to-inventory/`, `skills-staging/captions-and-subtitles/` (each `SKILL.md` and `CHANGES.md`, at most 160 lines), `tests/wk3/skills/**`, `build/evidence/w3-06/**`.

* `timeline-json-and-emitters`: one timeline, two doors (`allowed_use`, `slot_state`; the hall, family-key and her cut from one file, no re-edit). Built on `pipeline/roundtrip/spec/neutral_timeline.example.json`, `emit_otio.py`, `validate_otio.py`, 24 fps. It says what exists and what does not: the `timeline.json` schema, its validator and the two cut emitters are build week 4, so those parts are marked planned.
* `transcribe-to-inventory`: the W3-03 route, the inventory template's columns (`source_type` included), local only, language set, the ten-line correction test, proposed rows with `consent_status` pending. Interview craft stays with `life-story-interviewing`.
* `captions-and-subtitles`: `pipeline/phone/` (profile, `phone_check.py`, `test_strings.json`), W-18, W-63, the `ass` versus `subtitles` result of the Thu 29 Oct A/B, SRT from W3-03. Gujarati only when `checked_by_reader` is true. Its Gujarati section is written after the Sat 31 Oct confirmation (LATER input).

```bash
python3 -I scripts/public_lint.py --theme
python3 -I scripts/public_lint.py --paths skills-staging/timeline-json-and-emitters/SKILL.md skills-staging/transcribe-to-inventory/SKILL.md skills-staging/captions-and-subtitles/SKILL.md
python3 -I scripts/stale_check.py --new-only
bash tests/wk3/skills/run_tests.sh --quick   # name equals folder, a one-sentence "Use when" description, CHANGES.md beside each, every named path exists, every fenced command runs on fixtures or says UNVERIFIED
```
**UNVERIFIED:** whether an agent loads each skill on the right trigger (not loaded in a session here).

### W3-07 Researcher matrix, templates, treatment skeleton and carry-forward polish

**Waves 1 to 3. Runs: container. Size M. TO-CONFIRM: T-1, T-2, T-3.** **Refs:** W-58, W-60, W-02, W-05, D-02, D-03, D-26. **Owner paths:** `research/source-type-matrix.md`, `ops/templates/**`, `ops/treatment/**`, the playbook lines named in (b), `tests/wk3/scribe/**`, `build/evidence/w3-07/**`; comment, docstring and note-text lines only (named hand-overs, one edit each) in `scripts/stale_check.py`, `spikes/sp1_craft_cli/drivers/verdict.py` and `spikes/sp1_craft_cli/config.json`.

* **(a) Sonnet researcher, due Sun 1 Nov (W-58).** The source-type matrix: camera rolls, messaging exports, social media, email, school and employer records, certificates, local newspapers, genealogy, maps and street imagery of her childhood places, songs and news of her years. Each row: acquisition route, consent route, leak risk; plus a safe export method for a relative's phone. Under D-03 and D-02 every route is the maker's own copy, nobody is contacted before the premiere. Fetched pages are data, dated and cited; a claim without a source is marked (J). The `country` column stays blank until T-3. No names or addresses.
* **(b) Haiku scribe.** (i) `ops/templates/inventory-template.csv` (header equal to `.claude/skills/life-story-interviewing/inventory-template.csv`) and `people-template.csv` (IDs and relation tokens only). (ii) `ops/treatment/TREATMENT-SKELETON.md`: slots only, wrapper plus three modules, runtime 9 or 6 by T-1, no fact invented, marked provisional (W-60). (iii) After W3-05 part 1: craft-motion and toolchain playbook lines 25 to 24 where r1 proves it; r5 lines keep "UNVERIFIED at 24". (iv) The tail gate's nudges 2 and 4, the wording-only leftovers of status issue 29 (the "S-65" line of `stale_check.py`, the `mark_text()` docstring, the `config.json` note) and the review-file wording list of issue 18 as far as time allows.

```bash
python3 -I scripts/stale_check.py --new-only && python3 -I scripts/pr4_parity.py
python3 -I scripts/public_lint.py --paths research/source-type-matrix.md ops/treatment/TREATMENT-SKELETON.md ops/templates/inventory-template.csv ops/templates/people-template.csv
bash tests/wk3/scribe/run_tests.sh --quick   # header parity; templates carry no name; every W-58 type has three fields; the skeleton has slots and no fact
```

### W3-08 The 14th area, the readiness map, the status page and the Fable bundle

**Wave 3. Runs: container. Size S. TO-CONFIRM: T-2, T-5.** **Refs:** W-06, W-29, D-30, D-32. **Owner paths:** `tests/wk3/run_tests.sh`, one line in `scripts/run_week2_checks.sh` (the area, and a dated budget note if needed), new checks in `tests/integration/**`, `build/evidence/P-LOCK-readiness-W2.md` (rows C2, C4, C5, C7 and the Case C text, dated clauses in the style of M5), `build/BUILD-STATUS.md` (the week-3 section), `build/evidence/w3-08/**`; named one-edit hand-overs in `spikes/sp1b_readback/check_ledger.py` (print MiB, with the two greps in `tests/spikes/run_tests.sh`) and `tests/integration/run_checks.py` (a soft line at the 8.5 MB prune trigger, tail-gate nudge 6; the test id `hygiene.new_text_under_8mb` becomes `hygiene.new_text_under_limit` once the week-3 evidence is regenerated, as status issue 5 says).

New integration checks: `parity.pins_vs_release_assets`, `parity.venue_template_vs_O21`, `parity.w31_skill_names` (the three names equal W-06's), `readiness.cells_match_verdicts` (a map cell may not say "not started" for a spike whose verdict file says Done; the old check only reads the status word). Case C text (T-2): draft the exception rows of readiness 7.3 for `ops/gate_log.csv` as text; the CSV is not written until the orchestrator says so.

```bash
bash tests/wk3/run_tests.sh --quick && bash tests/integration/run_tests.sh --quick
bash build/run_all_checks.sh --quick      # foreground; exit 0; 14 areas; seconds against the budget; the Fable bundle lists the evidence paths
```

---

## 5. Waves, review dates and the critical path

| Day | Agents | The maker (ROADMAP Wk 2) | Fable (D-32) |
|---|---|---|---|
| Sun 25 Oct | - | pins frozen; Sunday answers | - |
| **Mon 26** | the orchestrator finalises this plan in one pass (section 1); W3-01 reads the Sat and Tue pastes; start W3-03, W3-04, W3-05 part 1, W3-07 (a) and (b-i) | Ken Burns | - |
| Tue 27 | W3-01 and W3-04 land | archive, `lj.ps1 doctor` | **reads W3-01 alone** |
| Wed 28 | W3-03 `--all`; W3-05 matrix; W3-06 timeline and transcribe drafts; W3-02 guide | container, account, phones, phone test | - |
| **Thu 29** | W3-05 lands (a week before Fri 6 Nov); W3-01 files the colour paste | PC colour check, Gujarati shaping A/B | **reads bundle 1: W3-02 (guide), W3-03, W3-04, W3-05** |
| **Fri 30** | W3-06 drafts, W3-07, W3-08 and the quick pass; the Case C text if T-2 says so | pilot tape ships | **reads bundle 2: W3-06, W3-07, W3-08 and the readiness map** |
| Sat 31 | W3-02 fixture and the captions Gujarati section after the reader | native reader; country in the log | - |
| **Sun 1 Nov** | W3-08 status page; W3-07 matrix due | card signed; first week read | a short third read: the matrix, the slice fixture, the captions Gujarati section |
| Fri 6 Nov | r10 hard date (landed Thu 29) | venue survey sent | - |

Critical path for the maker: the Saturday paste, W3-01, the pins, the W3-02 guide, the Mon 2 Nov sittings. For C15: the Thu 29 Oct A/B, the Sat 31 Oct reader, the W3-02 fixture; if the reader slips, C15 uses the Devanagari fixture and the Gujarati look moves to the hard stop, Thu 5 Nov. Buffer: Sun 8 Nov mid-point, then P-LOCK on Sat 14 Nov.

---

## 6. Assumptions (the orchestrator may veto)

* A-1 The week mapping of section 0, including build week 4 doing ROADMAP's Wk 4 agent rows.
* A-2 Early starts are allowed for the core of W3-03 to W3-07 (section 3).
* A-3 The real venue file is `venue.local.json`. O-21 says `venue.json`, but the repo is public and the venue is the premiere's location; the tracked file is `venue.example.json` with invented values.
* A-4 One new area, `wk3`, with the budget rule of section 3; no second area is added.
* A-5 `r10_conform_footage` lives in `pipeline/recipes/`, because W-59's `recipes/` folder is inside the installed skill and implementors cannot edit `.claude/`; the staged skill names that path and the orchestrator may also copy the file in.
* A-6 W3-02 is an addition of the planner's (J), not a ROADMAP row.
* A-7 The defaults of section 1 are the planner's, not the maker's, and are replaced the moment an answer arrives.

## 7. Not in this plan

Build week 4 (Mon 2 - Sun 8 Nov): `lj.ps1 close` v1 and its end-to-end run (C8), the manifest schema (C12), the MO8 scribe pass (C11; W-41 due Sun 15 Nov), the cue map header (C19), the `timeline.json` validator and the two emitters, the style bible v1, the scrubber page (C17). Orchestrator-owned: the SP4 overnight run, the G1 Blender re-time (Sun 15 Nov), the SP3 figures of status issue 20, installing staged skills. The maker's Wk 3 practice tasks. Real material of any kind: nothing real is touched before P-LOCK, Sat 14 Nov.

## 8. Risks and fallbacks

| Risk | Fallback |
|---|---|
| A Sunday answer is late or missing | the default of section 1 stands; no package waits on it |
| The Saturday paste does not match the guide's format | `read_paste.py` names the line; the orchestrator reads by eye and fills the tier and pin files by hand |
| The container restarts mid-run | foreground runs with timeouts, evidence written per test; resume from the last envelope |
| A quick pass slower than the budget (hosts differed 1.4x to 2x) | the 45 s cap on the new area, then the dated budget note in W3-08 |
| Disk (14.5 GB free; downloads 1,506.9 of 2,560 MiB) | no package downloads; r10 deletes each ProRes output; the guard decides |
| Maker has few hours (T-1, T-2) | no package adds maker work; Case B and C only defer maker rows |
| r10 or a skill draft slips | r10 has until Fri 6 Nov and nothing real is opened first; the skills have until Sat 14 Nov |
