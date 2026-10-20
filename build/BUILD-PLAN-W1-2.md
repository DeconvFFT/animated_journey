# Build plan, weeks 1-2: Mon 19 Oct - Sun 1 Nov 2026

*Written Mon 19 Oct 2026 by a Sonnet implementor acting as build planner, on branch `build/process-lock`, and **revised the same day (round 2)**: the eight nudges of the Fable advisor's first review (`reviews/build/plan-review-r1.md`) are applied in place, and section 11 says where each one landed. This is a proposal for the orchestrator. Nothing in it has been built. `DECISIONS.md` wins over this file; where this plan found a conflict it says so in section 8 instead of resolving it.*

---

## 0. In one page

**What this plan buys.** Eleven work packages (WP-01 to WP-11) in three waves. Two of them are delivered in two stages that fall in different waves, so the structured result lists **thirteen schedulable entries**: WP-01a (wave 1) and WP-01b (wave 2) per nudge 1, and WP-11a (wave 1, the check-runner skeleton) and WP-11b (wave 3) per nudge 8. Together they put the eight "must pass for P-LOCK" items (W-06) and the week 1-2 calendar rows of `ROADMAP.md` section 7 on track, and they hand the maker what is needed *this* week first:

| Maker needs | By | Package |
|---|---|---|
| A place to log hours, and how (the first logged week is read Sun 1 Nov) | **Mon 19 Oct (today)** | WP-02 (hours part; a CSV and one page, so it can go out on lint and test evidence alone) |
| The PC inventory script, a plain README, and a way to run it without touching Windows settings | **Tue 20 Oct** | WP-01a (Fable reads it first, Tue morning) |
| The week-1 "own material" checklist (hum, object candidates, hands per era, family profile, existing voice recordings) | Wed 21 Oct | WP-02 |
| Craft zip download, checksum and five-minute-test guide, including where each app writes (pins freeze Sun 25 Oct) | Fri 23 Oct (for Sat 24) | WP-07 |
| Ken Burns by script at 24 fps; archive folders, manifest and checksums for five stand-in scans | Fri 23 Oct (for Mon 26 / Tue 27) | WP-09 parts 1-2 (a named early-start exception, section 6) |
| `lj.ps1 doctor` and a dry-run `close` (nothing is deleted yet) | Tue 27 Oct | WP-01b (built after the Sat 24 Oct tests show where each app writes) |
| Colour-patch test to run on the PC's own ffmpeg; the phone test file | Thu 29 Oct (for Sat 31) | WP-09, WP-08 |
| The settings card to sign, with a phone row (D-27) and a language/script note | Fri 30 Oct (for Sun 1 Nov) | WP-02 (+ WP-08 row) |

**What the agents get.** A deterministic Route A harness (`render.mjs`), validators (spec check, colour-patch, MO8 gate), ORA/SVG/OTIO round-trip emitters with validators, one shared redaction pattern file read by every scanner (4.13), a disk and timing guard (4.9), the stale-copy check (W-29) with its first report, a public-repo lint, a check runner that Fable can see on Fri 23 Oct, a Craft CLI spike (SP1) run for real, and Route A (SP2) and validator (SP5) spikes folded into the packages that build them. SP3 (Blender) and SP4 (idle container) are prepared, with honest reasons they are not fully run this fortnight (section 3, F-01 and F-07).

**Four facts that shape everything (all measured today, section 3):**
1. The container has **about 1.1 GB of free disk on a volume other jobs are writing to** (it read 1.3 GB, then 1,137 MB, then 1,084 MB inside twenty minutes). The five Craft Linux builds alone are 450 MB compressed. So disk is a mechanism, not a rule: every write over 100 MB goes through one lock that checks live free space, requires "Avail minus planned write stays above 400 MB", and aborts below a 250 MB floor (4.9). SP3 (Blender, a 402 MB wheel plus about 1 GB venv) cannot run here.
2. The container has **4 vCPUs**. Timing marks (SP1 T2/T4, SP2 fps, MO8) must never overlap: all timed runs go through one `flock` (4.9).
3. **PowerShell is not installed** here. The 75 MB Linux tarball is reachable, so WP-01a parse-checks and dry-runs the Windows scripts on pwsh 7.5.4. Windows PowerShell 5.1 can never be run here: every Windows behaviour is marked **UNVERIFIED** until the maker's first run.
4. **Redaction has one source.** `scripts/redaction_patterns.json` (4.13) is read by the PC inventory script, the PC check runner, the report validator and the public lint, and a self-test fails on any disagreement. The raw PC reports are a hardware fingerprint of the maker's machine: the maker reads them and pastes them in chat; only a derived tier file is ever filed in the repo.

**Needs an answer from the orchestrator today (before wave 1 starts).** The planner could not ask interactively, so the answers are recorded here by the orchestrator.

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| Q-1 | May the regenerable pip cache (418 MB, `/root/.cache/pip`; `python3 -m pip cache purge`) be cleared before wave 1? The 605 MB huggingface cache is probably Whisper weights needed in week 3 and should stay. | With it: Avail is about 1.5 GB and WP-07 can run its full profile (about 600 MB). Without it: Avail is about 1.1 GB; after pwsh (200 MB), the OTIO venv (50 MB) and fetched libraries (25 MB) about 810 MB remain, so a stage may write at most about 410 MB and WP-07 runs its **lean** profile (4.9, WP-07). | **Answer: PENDING.** The planner recommends **yes** (it is regenerable; a later `pip install` simply downloads again). If unanswered: not cleared, lean profile; the plan works either way. |
| Q-2 | Who else writes to this volume right now, and can their outputs be capped or deleted when finished? Observed Mon 19 Oct 02:25 UTC: Avail fell about 28 MB per 20 seconds while a concurrent job wrote two roughly 69 MB `.mov` files under the session scratchpad. | The guard measures live, but a writer that never cleans up eats the whole budget. | **Answer: PENDING.** The guard's 250 MB floor aborts and cleans up the package's own stage; it cannot clean another job's files. |
| Q-3 | Add to `.gitignore`: `logs/`, `*.local.*`, `spikes/**/work/`, `pc_report*.json`, `colour_patch_pc*.json`, `maker-pc*.json` (`vendor/`, `renders/`, `exports/` and the media extensions are already there). | Backstop for the rule that raw PC reports never enter the repo (4.13). `public_lint.py` also refuses these names by path. | **Answer: PENDING.** Not done by this plan. |

**Not in this plan** (and why, with dates): section 9.

---

## 1. Package table

Size: S under half a day of agent time, M about a day, L more. "Done by" is the target for the *maker-facing* part.

| ID | Title | Wave | Runs where | Size | Depends on | Done by |
|---|---|---|---|---|---|---|
| WP-01a | Windows kit A: PC inventory, report checker, tools, pins, schema, fixtures, maker README | 1 | both | L | - (self-scan tests need WP-03's 4.13 file, delivered first) | Ready for Fable Tue 20 Oct 08:00; the maker runs it Tuesday after Fable's pass |
| WP-01b | `lj.ps1` `doctor` and `close` v0, **dry-run only** | 2 | both | S | WP-01a, and the maker's Sat 24 Oct paste of where each Craft app writes | Tue 27 Oct |
| WP-02 | Ops files: `ops/decisions.csv`, `ops/hours.csv`, `GATHER.md`, `SETTINGS-CARD.md` (+ lint and hours report) | 1 | container | M | - | hours part Mon 19; rest Thu 22 Oct |
| WP-03 | Shared checks: redaction patterns (4.13), disk/bench guard (4.9), `stale_check.py` (W-29), `public_lint.py`, theme guard | 1 | container | L | - | patterns and guard first (Mon 19, before WP-01a's self-scan tests); rest Wed 21 Oct |
| WP-04 | Route A harness `render.mjs` + synthetic test scene + the test-strings file (SP2) | 1 | container | L | - | Fri 23 Oct |
| WP-05 | Validators: ffprobe spec checker, colour-patch (W-16), MO8 gate, chains and settings JSON (SP5, media half) | 1 | container | L | - | Fri 23 Oct |
| WP-06 | Round-trip emitters and validators: ORA, SVG ids, OTIO (SP5, hand-off half) | 1 | container | M | - | Fri 23 Oct |
| WP-07 | SP1a: release sums for every pin, FilmCraft and EffectCraft headless tests (T1, T2, T4), the maker's Craft-zip guide | 1 | container | L | - | sums and guide Tue-Thu; results Mon 26 Oct |
| WP-08 | Phone deliverable: encode profile, legibility check incl. fill-crop, maker phone test (D-27) | 2 | both | M | WP-04, WP-05 | Wed 28 Oct |
| WP-09 | Windows kit B: Ken Burns 24 fps, archive init + manifest, PC colour-patch/spec runner | 2 | both | M | WP-01a, WP-05 | parts 1-2 Fri 23 Oct (named exception); parts 3-4 Thu 29 Oct |
| WP-10 | SP1b: PhotoCraft, VectorCraft, LightCraft T1 and read-backs, FilmCraft T3; SP3 prepared; SP4 armed; spike verdict table | 2 | container | L | WP-04, WP-05, WP-06, WP-07 | Wed 28 Oct |
| WP-11a | Check-runner skeleton `run_week2_checks.sh`, `INDEX.md` writer, scratch cleanup script | 1 | container | S | - | Thu 22 Oct (so `--quick` output is in the Fri 23 Oct bundle) |
| WP-11b | Integration and evidence: parity tests, end-to-end, whole-build hygiene, P-LOCK readiness map, staged skill update | 3 | container | M | all | Fri 30 Oct |

**Suggested start order in wave 1** (at most four CPU-heavy agents at once; disk and CPU rules in 4.9):
1. Immediately: **WP-03** (its first two deliverables are the redaction pattern file and the disk/bench guard; everything else in the wave leans on them), **WP-02** hours part, **WP-01a** (script skeleton and tools; its self-scan tests wait for the pattern file), **WP-11a** (light).
2. When 4.13 and the guard land (about two hours): **WP-05**, **WP-06**, **WP-04**, and **WP-07**'s release-sums fetch and guide.
3. Behind the locks: WP-07's FilmCraft and EffectCraft stages and WP-04's speed marks wait for `bench.lock` and `disk.lock`.

**Waves are barriers** only for the dependencies listed. Two start-gate exceptions are named rather than hidden: WP-01a needs the pattern file (4.13) from WP-03 before its self-scan tests can run (it codes against the frozen schema meanwhile), and WP-09 parts 1-2 need only WP-01a's tools, so the orchestrator may start WP-09 on Wed 21 Oct and put those two parts into the Fri 23 Oct review bundle because the maker's Mon 26 / Tue 27 Oct exercises need them. The acceptance lines that call `spec_check.py` or `mo8_gate.py` run when WP-05 lands (plain `ffprobe` checks run immediately).

**Every file has exactly one owner.** Owner paths per package are in section 5 and in the structured result. A package that needs something owned elsewhere reads it through the frozen interfaces in section 4 and never edits it.

---

## 2. P-LOCK must-pass items and calendar rows: coverage

| P-LOCK must-pass item (W-06, ROADMAP 8) | Who | Container-side proof | Package |
|---|---|---|---|
| PC inventory | maker runs; agents validate | script parse-checked and dry-run on pwsh; validator tested on synthetic reports; only a derived tier file is filed | WP-01a |
| Hours log (7 days) | maker types | template + report script + threshold test | WP-02 |
| Ken Burns by script (and in the editor) | maker | script produces 1920x1080 24 fps; MO8 gate passes on the sub-pixel path | WP-09 |
| Archive and five stand-in scans (fronts and backs) | maker | folder/manifest/checksum scripts run on synthetic stand-ins; tamper test | WP-09 |
| Settings card signed (Sun 1 Nov) | maker signs | card parsed against register IDs; machine-readable mirror; phone row and script note from the measured phone check | WP-02, WP-05, WP-08 |
| ORA/OTIO round trip (and SVG ids) | maker (Windows) after agents | emitters + validators + Linux CLI read-backs | WP-06, WP-10 (+ maker Windows tests) |
| Encrypted drive | maker only (admin rights) | none possible; WP-01a reports the Windows edition so the README can say whether BitLocker is even offered, and tells the maker the VeraCrypt container is created from an administrator account and mounted from the project account (W-25) | WP-01a (info only) |
| Colour-patch test | agents (container) and maker (PC ffmpeg) | container ffmpeg 6.1.1 run; PC runner built; only the derived chain results are filed | WP-05, WP-09 |

Also on the P-LOCK list: spikes SP1-SP5 (WP-07 and WP-10 for SP1, WP-04 for SP2, WP-10 for SP3 prep and SP4 armed, WP-05/06 for SP5), five-minute tests on the five pinned apps (maker; guide WP-07), **`lj.ps1 close` written and run once (W-26)**: this fortnight delivers v0, a dry run that lists what it *would* remove and deletes nothing (WP-01b); `-Apply`, `-Commit`, `-IncludeWindowsRecent`, the backup and the log arrive in v1 in week 4 (A-04), and the end-to-end run that satisfies W-26 is a week-4 item, not a week-2 one. MO8 scribe pass (Haiku, not here).

| ROADMAP row | Item | Package |
|---|---|---|
| Week 1, orchestrator | `decisions.csv`, `hours.csv`, `GATHER.md`, settings card | WP-02 |
| Week 1, Sonnet | SP1-SP5 started | WP-07 (SP1), WP-04 (SP2), WP-10 (SP3 prep, SP4 armed), WP-05/06 (SP5) |
| Week 1, Sonnet | `lj.ps1 doctor`, `lj.ps1 close` v0 | WP-01b (dry-run only; built after the Sat 24 Oct tests) |
| Week 1, Sonnet | `render.mjs`, validators, `windows_check.py`, `stale_check.py` | WP-04, WP-05, WP-01a, WP-03 |
| Week 1, maker | PC inventory, 7 days of hours, five-minute Craft tests | WP-01a, WP-02, WP-07 |
| Week 2, Sonnet | SP1 T1-T6 results | WP-07 (T1, T2, T4 on FilmCraft and EffectCraft), WP-10 (T1 and read-backs on the other three apps, T3 on FilmCraft); **T5 SoundCraft not run** (below); T6 web builds not run |
| Week 2, Sonnet | Route A frame-capture spike | WP-04 |
| Week 2, Sonnet | colour-patch on both ffmpeg builds | WP-05 (container), WP-09 (PC build 9.0.2, maker runs) |
| Week 2, Sonnet researcher | source-type matrix (W-58) | **not here**: a researcher task the orchestrator briefs |
| Week 2, Haiku | craft-motion "25" to "24" after re-runs; Table 4 patches | **not here**: WP-03's report is their input; WP-09 supplies the 24 fps re-run for r1 |
| Week 2, maker | Ken Burns by script, archive and five scans, VeraCrypt container, separate account | WP-09 (scripts); the last two are maker-only |
| Fri 30 Oct | first `stale_check.py` run | WP-03 runs it now (baseline) and WP-11b runs it again |
| Sun 1 Nov | settings card signed | WP-02 (card), WP-08 (phone row and script note) |

**SP1 T5 (SoundCraft) is cut from this fortnight** (nudge 7). D-12 bars SoundCraft from the delivery path and leaves it unpinned and learning-only, the five-pin list of W-06 excludes it, and the original plan said T5 "gates nothing". `spikes/VERDICTS-W2.md` (WP-10) records it as "not run: learning-only app, no decision depends on it; re-open only if the maker asks to learn the app". No SoundCraft file is downloaded.

---

## 3. What I found (probed Mon 19 Oct 2026; these shape the plan)

Only HEAD requests and one 0.8 MB wheel (deleted) were fetched. Nothing was built or executed from a download.

- **F-01 Disk (re-measured; this is why disk is now a mechanism).** `df`: 252 GB filesystem, 38 GB used, **1.3 GB available at the first reading, then 1,137 MB, then 1,084 MB within twenty minutes** while a concurrent job wrote two roughly 69 MB `.mov` files under the session scratchpad. The volume is shared and shrinking. Regenerable caches that someone could clear if more room is needed (not touched): pip cache 418 MB (Q-1), huggingface 605 MB (probably Whisper weights, needed again in week 3: keep). `/tmp` is the scratchpad's parent and holds other sessions' files; do not clean it.
- **F-02 CPU/RAM.** 4 vCPU, 15 GB RAM free, load near 0. Ubuntu 24.04-class, Python 3.13.16, Node 22.22.0, ffmpeg 6.1.1 (Ubuntu build; libx264, libass, harfbuzz, zimg present), Playwright 1.56.1 with Chromium build 1194 under `/opt/pw-browsers` (`chromium` symlink works as `executablePath`), Inkscape, ImageMagick 6 (`convert`, `compare`, `identify`; no `magick`), numpy 2.5.3, Pillow 12.3.0 (raqm on), `flock`, `timeout`, `prlimit`, `xmllint`, `zip`. `unshare -rn true` exits 0, so user and network namespaces appear to work (use them to run untrusted binaries without network).
- **F-03 Missing here.** `pwsh`/`powershell`, Blender, `opentimelineio`, scipy, tesseract, exiftool, and any Noto or other OFL Indic font. GNU FreeFont and Unifont do cover Devanagari (`fc-list :lang=hi`), but they are not OFL (W-21), so the harness fetches OFL Noto Sans Devanagari for its tests instead. `pip` works (PyPI reachable): `opentimelineio==0.18.1` is a 0.8 MB wheel.
- **F-04 GitHub release assets.** Direct asset URLs `https://github.com/storytold/<app>/releases/download/<tag>/<asset>` answer **302 then 200**. Release *pages* and the REST API answer **403 Forbidden** from this container, so tag and asset discovery must go through the downloadable `SHA256SUMS.txt` (2.6 KB, present for FilmCraft v0.9.0 and PhotoCraft v0.10.0), not the API. Linux tarball sizes: PhotoCraft 0.10.0 83,037,328 B; VectorCraft 0.13.1 124,613,940; LightCraft 0.9.1 108,938,717; FilmCraft 0.9.0 69,756,500 (fallback 0.8.0: 69,692,976); EffectCraft 0.11.1 64,039,300; SoundCraft 0.8.0 16,384,149 (not fetched: SP1 T5 is cut, nudge 7). Total for the five pinned builds 450,385,785 B (450 MB). So SP1 downloads are **not blocked**; the plan still requires the blocked-download proof path (WP-07) because the proxy may change. The re-waved plan downloads each of the five once (ledger in WP-07).
- **F-05 Other hosts.** PowerShell 7.5.4 Linux tarball 75,396,784 B (302 then 200). `cdn.jsdelivr.net` answers 200. npm registry not probed (WP-04 tests it first).
- **F-06 Local source clones.** `/home/user/storytold/{effectcraft,filmcraft,photocraft,vectorcraft}` (240 MB) are earlier research clones: untrusted data, read only (`grep` for command names), never built or run. There is no LightCraft or SoundCraft clone. `/home/user/life-journey` is a stale pre-reconciliation copy of this repo; ignore it.
- **F-07 SP4 cannot be run by a package.** It measures what the container does while the session is idle (tab closed). A subagent cannot make its own session idle. WP-10 arms it; the orchestrator runs the protocol once, overnight.
- **F-08 Existing assets to reuse unchanged.** `research/cinematic-quality-fixtures/mo8_audit.py` (needs `zoompan_vs_subpixel_prints.py` and `zoom_velocity_classifier.py` beside it; loads every frame into RAM, so at most about 96 frames per call), `research/craft-visual-fixtures/{make_ora.py,check_ids.py,at-layers.ora,at-rig.svg,faded-print-a.lcpreset,at-lightcraft-steps.jsonl}`, `research/sources/format-round1/{make_otio.py,mk_manifest.ps1,verify_manifest.ps1}`, `research/creator-threads-fixtures/kenburns_xfade.py`, `research/toolchain-fixtures/make_venue_test_kit.py`, `research/cinematic-quality-fixtures/caption_xheight.py`. Their stale values (25 fps defaults, absolute paths, a hard-coded `timeline169.json`) are noted per package; **reuse means call or import, never copy a 25 fps value into a new file.**
- **F-09 Known bug in the specified harness.** The R7 static file server in `research/agent-pipeline.md` joins the URL onto the root without checking the result stays inside the root (path traversal from the page). WP-04 must fix and test this.
- **F-10 PowerShell encoding trap.** `command > file` in Windows PowerShell 5.1 writes **UTF-16 LE with BOM**; `Set-Content -Encoding UTF8` writes a **UTF-8 BOM**. The checker must read UTF-8, UTF-8-BOM and UTF-16, and the script must write BOM-less UTF-8 itself.
- **F-11 VRAM trap.** `Win32_VideoController.AdapterRAM` is a 32-bit field and caps at about 4 GB (general knowledge, UNVERIFIED on the maker's PC). VRAM must come from `nvidia-smi` (NVIDIA) or the 64-bit registry value `HardwareInformation.qwMemorySize`, else be reported as unreadable.
- **F-12 The 3-patch colour test does not cover the master chain.** Q-F1 measured H.264 and ProRes 4444. The ProRes 422 HQ master chain (the one that matters most, W-15) was never measured. WP-05 measures it and records the result as a new finding.
- **F-13 Disk arithmetic with the real residents (round 2).** Round 1 budgeted WP-07 at a 600 MB peak and guarded it with "Avail at least twice the planned write". PowerShell 7.5.4 stays resident (about 200 MB extracted, 75 MB tarball deleted), the OTIO venv about 50 MB, fetched libraries and fonts about 25 MB, and one kept FilmCraft tarball 70 MB (WP-07, 4.9). With 1,084 MB available and those residents the 2x rule would stop WP-07 on day one. The replacement rule is "Avail minus planned write stays above 400 MB" with an emergency floor of 250 MB; at today's figure a stage may write at most about 410 MB, so WP-07 has a **lean** profile (low-entropy stills, a trimmed tree, 1-second ProRes) and a **full** profile that is only chosen when Q-1 has been answered yes. The table is in 4.9; the guard is `scripts/lj_guard.sh` (WP-03).
- **F-14 `python -I` and sibling imports (design fact, checked in the container).** Isolated mode (`-I`) does not put the script's own folder on `sys.path`, so a PC-side tool run as `py -3 -I scripts\windows_check.py` cannot `import` a sibling module. That is why the redaction source is a **data file** (4.13) that every consumer reads by path relative to `__file__` or `$PSScriptRoot`, not a shared Python module. A consumer that cannot find the file fails closed (exit 2, nothing written).
- **F-15 Version strings that look like IP addresses (general knowledge, UNVERIFIED on the maker's PC).** Display-driver versions and some tool versions are four dot-separated numbers (for example a driver version with a leading-zero part, or any four-part version whose parts are all below 256). A naive IPv4 pattern flags them, and the inventory would refuse to write on day one. The pattern file therefore rejects leading-zero octets and carries `field_exemptions` for the version fields (4.13), with positive and negative samples for both.

---

## 4. Shared conventions (frozen; every package follows them)

### 4.1 Layout and ownership

```
win/               PowerShell kit for the maker             WP-01a (step0_pc_tests.ps1, README-MAKER.md, pins.json, tiers.json, schema/, tools/)
                                                            WP-01b (lj.ps1, lj.config.example.json, README-LJ.md)
                                                            WP-09 (win/kit2/)
scripts/           repo-level checks, one owner per file    WP-03: redaction_patterns.json, lj_guard.sh, stale_check.py (+ patterns, allowlist, baseline), public_lint.py (+ config)
                                                            WP-01a: windows_check.py
                                                            WP-02: ops_lint.py, decisions_to_csv.py, hours_report.py
                                                            WP-11a: run_week2_checks.sh, cleanup_scratch.sh
pipeline/bin/      render.mjs                               WP-04
pipeline/scenes/   test scene(s)                            WP-04
pipeline/lib/      libs.lock.json, fetch_libs.sh, licences/ WP-04; chains.json WP-05
pipeline/validators/  spec_check.py, colour_patch.py, mo8_gate.py   WP-05
pipeline/settings.json  machine-readable settings card      WP-05
pipeline/roundtrip/ ORA, SVG, OTIO                          WP-06
pipeline/phone/    test_strings.json: WP-04 (frozen, 4.15); every other file there: WP-08
ops/               decisions.csv, gate_log.csv, hours.csv, HOURS-HOWTO.md, GATHER.md, SETTINGS-CARD.md   WP-02
spikes/            sp1_craft_cli (WP-07), sp2_route_a (WP-04), sp1b_readback + sp3_blender + sp4_idle + VERDICTS-W2.md (WP-10)
tests/<area>/      each package's tests, one folder per package; every run_tests.sh takes --quick (at most 60 s, no downloads, no timed runs) and --all
build/evidence/wpNN/   each package's machine-readable results (wp01a, wp01b, ..., wp11a, wp11b)
build/evidence/INDEX.md, week2_summary.json, wave1_quick.txt   WP-11a (generated by the runner)
build/evidence/P-LOCK-readiness-W2.md, build/evidence/pc/       WP-11b (pc/ holds derived PC evidence only, 4.16)
skills-staging/    proposed skills (phone-delivery: WP-08; agent-first-production-pipeline update: WP-11b)
vendor/, renders/, exports/   git-ignored working output (never committed)
/home/user/build-scratch/     outside the repo, on the same volume: pwsh, venvs, downloads in progress, bench.lock, disk.lock.
                              In every committed file this literal path is written <scratch>; public_lint treats /home/user as the
                              generic placeholder it is and /home/user/build-scratch as <scratch> (4.13).
```

Orchestrator actions this implies (not done here): add `logs/`, `*.local.*`, `spikes/**/work/`, `pc_report*.json`, `colour_patch_pc*.json` and `maker-pc*.json` to `.gitignore` (Q-3); decide whether `pipeline/` at repo root is acceptable (the agent-first pipeline skill already uses `pipeline/settings.yaml` and `pipeline/lib`, so this plan follows it, with `settings.json` instead of YAML so every tool can read it with the standard library).

### 4.2 Evidence envelope (every automated test writes one)

```json
{"schema":"lj-evidence/1","package":"WP-05","test":"colour_patch_h264_chain_b",
 "date_utc":"2026-10-21","status":"PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED",
 "env":{"platform":"linux","ffmpeg":"6.1.1","nproc":4,"python":"3.13.x","node":"22.x"},
 "disk":{"avail_mb_start":1084,"planned_write_mb":0,"avail_mb_min":1080,"avail_mb_end":1083,"floor_mb":400,"hard_floor_mb":250},
 "expected":"...","actual":"...","notes":"","unverified_reasons":[]}
```
Rules: written under `build/evidence/wpNN/`; **no host names, user names, absolute paths outside the repo (use repo-relative paths or the literal `<scratch>`), no IP addresses, no timestamps finer than the second**; a test that depends on Windows behaviour is `UNVERIFIED`, never `PASS`. The `disk` object is **required in every envelope** (nudge 2): `avail_mb_start` and `avail_mb_end` from `df`, `planned_write_mb` (0 for a test that writes under 100 MB), `avail_mb_min` from the guard's watchdog when the stage ran under `lj_with_disk` (else equal to the smaller of start and end). WP-11b shows from these that the budget was kept: for every stage with `planned_write_mb` above 100, `avail_mb_start - planned_write_mb >= floor_mb` and `avail_mb_min >= hard_floor_mb`. A stage the guard refused is `BLOCKED` with the exact message.

### 4.3 Exit codes (all new Python and shell tools)

`0` all checks pass; `1` a check failed (a finding, not a crash); `2` bad usage or invalid input, **or identifying data found, or the redaction pattern file is missing or invalid (fail closed)**; `3` environment problem (missing tool, disk guard refused or tripped, download blocked, lock busy).

### 4.4 `pc_report.json` v1 (owner WP-01a; frozen so WP-02, WP-09 and WP-11b can rely on it). **A raw, local-only file.**

Top level: `schema_version` (1), `tool`, `tool_version`, `generated_utc`, `powershell {version, edition}`, `os {platform, caption, version, build, edition_id, architecture}`, `cpu {name, cores, logical}`, `ram {total_gb}`, `gpus[] {name, vendor, vram_gb, vram_source, driver_version, is_software}`, `vulkan {runtime_dll_present, vulkaninfo_found, devices[]}`, `disks[] {drive, type, fs, size_gb, free_gb}` (no labels, no serials), `display {primary {width, height, refresh_hz, scale_percent}, count}`, `tools {ffmpeg, ffprobe, python, git, winget, magick, inkscape, blender, wsl, veracrypt_installed}` (each `{found, version, notes}`; ffmpeg adds `has_libx264, has_libass, has_zscale` and `sha256`, the 64-hex hash of the binary, which is public build identity and is exempt in 4.13), `craft_apps {tools_roots_scanned, found[] {app, version, pinned_version, matches_pin}, not_found[]}`, `local_accounts_count`, `claude_desktop_running`, `redaction {user_name_removed, machine_name_removed, paths_generalised, self_scan_passed, patterns_version, name_hits_in_hardware_fields[] {category, field, masked_hit}}`, `notes[]`, `errors[]`.

Deliberately **not** collected: user name, computer name, domain, serial numbers, UUIDs, MAC or IP addresses, Wi-Fi names, volume labels, monitor model/serial, time zone, locale, keyboard layouts, installed-program lists beyond the named tools, file names, any path under the user profile.

**Where the raw report lives (nudge 3).** The script writes it to `%TEMP%\lj_pc_report.json` by default and prints the path in the unexpanded form `%TEMP%\lj_pc_report.json`, so no profile path is ever echoed to a console the maker might paste from. The maker opens it, reads it, and pastes it **in chat only**. It is never copied into the project folder, never committed, and never filed under `build/evidence/`. A raw inventory (CPU and GPU model, exact RAM and disk sizes, driver versions, Craft versions) is a hardware fingerprint of one machine in a public repository. What the repo may hold is the **derived tier file** (4.16), produced container-side from the pasted report by `windows_check.py --tier-json-out`, which carries buckets and verdict words and no model names or exact sizes. `public_lint.py` refuses files named `pc_report*.json`, `colour_patch_pc*.json` and `maker-pc*.json` anywhere except the synthetic fixtures under `tests/win/fixtures/` (4.13).

### 4.5 `pipeline/lib/chains.json` v1 (owner WP-05; read by WP-04, WP-08, WP-09)

`{"schema":"lj-chains/1","chains":{NAME:{"container","vf","video_args[]","audio_args[]","expect{pix_fmt,color_range,color_space,color_primaries,color_transfer,codec,profile}","notes"}}}`. Initial chains: `h264_venue`, `h264_backup_main40`, `h264_online`, `prores422hq_master`, `prores4444_alpha`, `ffv1_lossless`. Initial `vf` strings are the Q-F1 recommended lines (scale first, then `format=`, then `setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv`); the colour-patch test, not the text, decides whether a chain is accepted. WP-04's `render.mjs` reads this file and carries a built-in default identical to the H.264 chain so it works before WP-05 lands (WP-11b asserts parity). WP-08's phone chain lives in `pipeline/phone/profile.json` in the same schema, and `colour_patch.py --chain-file` can test any file of this shape.

### 4.6 `pipeline/settings.json` (owner WP-05)

Mirror of the settings card: picture 1920x1080, fps 24, colour (Rec.709/BT.1886 video, sRGB stills), audio (48 kHz, 24-bit master), master (ProRes 422 HQ, 10-bit 4:2:2), captions (`FontSize=23`, 42 characters, two lines, inside the 90% box), loudness (-1 dBTP; online -16 LUFS; venue -23/-18/-16 chosen on 22 Feb), profiles (`master_prores422hq`, `venue_h264`, `venue_h264_backup_main40`, `online_h264`), `signed: false`. WP-08 supplies the phone profile as its own file in the same shape; `spec_check.py` accepts `--profiles-file`.

### 4.7 Windows scripts (WP-01a, WP-01b, WP-07 docs, WP-09)

- Must parse and run on Windows PowerShell 5.1 and PowerShell 7. **Forbidden syntax:** `??`, `?.`, ternary `? :`, `&&`/`||` pipeline chains, `ForEach-Object -Parallel`, `ConvertFrom-Json -AsHashtable`, `Get-Content -AsByteStream`, `$IsWindows` without a `Get-Variable` guard (undefined in 5.1), `-Encoding utf8NoBOM`. `ConvertTo-Json` always with `-Depth 6` or more. Write files with `[System.IO.File]::WriteAllText(path, text, (New-Object System.Text.UTF8Encoding($false)))`. Reading the pattern file: `ConvertFrom-Json` (5.1-safe) and `[regex]::new(pattern, options)`.
- No admin rights, no registry writes, no `Set-ExecutionPolicy` at machine or user scope, no installs, no downloads, no network calls. Read-only unless the file name or a documented switch says otherwise. **`lj.ps1` v0 has no write or delete switch at all** (WP-01b); the switches `-Apply`, `-Commit` and `-IncludeWindowsRecent` do not exist until v1 in week 4.
- **Print exactly what they do**: one line before each action (`[3/12] Reading RAM (Win32_ComputerSystem) ...`), one line after (`ok` or the error text), and a final line listing every file written (or `files written: none`). Paths are printed in unexpanded form (`%TEMP%`, `%USERPROFILE%`), never expanded, so that console text is safe to paste.
- Every section in `try/catch`; one failing section never stops the rest; the failure goes into `errors[]`.
- **Fail closed on redaction.** A script that writes a report loads `scripts/redaction_patterns.json` (4.13) relative to `$PSScriptRoot` before it collects anything; if the file is missing or does not parse, the script prints why, writes nothing and exits 2 (the README tells the maker to download the whole project folder, not single files). The self-scan refusal names the **category** and prints the **masked hit** (first two characters plus asterisks), never the full value.
- Non-Windows hosts (pwsh on Linux, used for tests): Windows-only sections are skipped, fields are `null`, `os.platform` is `non-windows`. Such a report is *never* accepted as a Windows report by `windows_check.py`.
- Every claim about Windows behaviour is tagged `UNVERIFIED` in the evidence JSON and in the README until a real report exists. Test by `Parser::ParseFile` on pwsh 7.5.4, by `win/tools/ps_lint.py` (5.1 compatibility rules), and by dry-runs on Linux.
- Test modes (`-TestFixture`, `-PatternSelfTest`) collect nothing from the real machine, print `TEST MODE: nothing was collected`, and are not mentioned in the maker's README.
- No account handle, no repo owner name, no machine name in any file. The README says "the project page" and "the link in your notes"; commands use relative file names.

### 4.8 Python tools

`python3 -I` always (`py -3 -I` on Windows). Standard library first. Allowed extras: numpy and Pillow (needed by the reused MO8 scripts); `opentimelineio` only inside `/home/user/build-scratch/venv-otio` and only for optional checks. Tools that the maker runs on the PC (`windows_check.py`, `spec_check.py`, `colour_patch.py`) are **standard library only**. Each accepts `--ffmpeg PATH` and honours `FFMPEG`, as the reused scripts do. No `Math.random`/`Date.now` equivalents in anything that must be deterministic: seed explicitly.

### 4.9 Resources, downloads and untrusted data

**Disk is a mechanism, not a rule (nudge 2).** Everything (the repo, `<scratch>`, `/tmp`, other jobs' files) is one volume, 98% full, and other jobs write to it (F-01, F-13). A rule that four parallel agents are asked to remember does not hold, so the rule is code.

- **`scripts/lj_guard.sh`** (WP-03; sourced by every package's shell scripts; delivered first) provides:
  - `lj_df_avail_mb`: Avail of `/` in MB from `df -BM`.
  - `lj_with_disk PLANNED_MB LABEL -- COMMAND...`: (1) takes an exclusive lock on `<scratch>/disk.lock`, writing LABEL into it so a waiting job can see who holds it; waits up to 90 minutes, then exits 3 `BUSY: held by <label>` rather than hanging; (2) reads Avail and **refuses unless `Avail - PLANNED_MB >= 400`**, exiting 3 with the exact figures and the lean-profile hint; (3) runs COMMAND under a watchdog that polls `df` every 5 s and, if Avail drops below **250 MB** (the hard floor, whoever is writing), terminates COMMAND's process group, runs its cleanup trap and exits 3 `DISK-FLOOR`; (4) **holds the lock until COMMAND, including its own cleanup, has finished**, then releases it; (5) appends one non-identifying line (label, planned, start, min, end, date) to `<scratch>/disk-ledger.jsonl`, which the package copies into its envelope (4.2).
  - `lj_bench COMMAND...`: exclusive lock on `<scratch>/bench.lock`, recording `nproc` and `/proc/loadavg` at start. The fixed nesting order is **disk, then bench**, never the reverse, so two waiting jobs cannot deadlock.
  - `LJ_DF_CMD` overrides the `df` command in tests (a fake that reports a falling number) so the refusal and the floor are tested without filling the disk.
- **Who must use it:** any step that writes more than 100 MB (a download, an extraction, a venv, a render run, an export, an encode set) runs inside `lj_with_disk`. PLANNED_MB is **computed, not guessed**, wherever it can be: tarball size (HEAD request) + sum of member sizes (`tar -tvzf`, a listing that writes nothing) + the stills and exports the stage will write. Writes under 100 MB take no lock but still record `df` in their envelope.
- **Stages are short and never idle:** a locked stage is at most 60 minutes and never waits on a human while holding the lock; a longer job is split into stages.
- **Budgets** (planned peak; persistent residents are counted by `df` itself, so they shrink every later stage's headroom):

| Package and stage | Planned peak (MB) | Persistent after (MB) | Cleanup |
|---|---|---|---|
| WP-01a `fetch_pwsh.sh` (tarball 75 + extracted tree) | 275 | 200 | `cleanup_scratch.sh` (WP-11a) at the end of the fortnight |
| WP-04 `fetch_libs.sh` (gsap and fonts via `npm pack`) | 30 | 25 | with `cleanup_scratch.sh` |
| WP-04 render tests (A5, A6) | 250 | 0 | each test deletes its frames |
| WP-05 validator tests (six chains, MO8 frames) | 150 | 0 | |
| WP-06 `venv-otio` | 60 | 50 | with `cleanup_scratch.sh` |
| WP-07 FilmCraft stage, **full** (only if Q-1 = yes) | 600 | 70 (kept tarball) | tree, stills and exports deleted |
| WP-07 FilmCraft stage, **lean** (default) | 350 | 70 (kept tarball) | as above |
| WP-07 EffectCraft stage | 400 (lean 300) | 0 | all deleted |
| WP-08 encodes and checks | 100 | 0 | |
| WP-09 kit tests | 80 | 0 | |
| WP-10, one app at a time (estimates; the real figure is computed from the tarball listing): PhotoCraft 300, VectorCraft 450, LightCraft 350, FilmCraft T3 from the kept tarball 300 | 450 max | 0 | tarball and tree deleted after each app; the kept FilmCraft tarball deleted after T3 |

  Persistent residents total about 345 MB once the FilmCraft tarball is kept. At Avail 1,084 MB that leaves about 740 MB before any stage, so with every resident present the largest stage may be about 340 MB (with Q-1 = yes, about 750 MB). Consequences, stated rather than hidden: WP-07 runs its FilmCraft stage **early (Wed 21 Oct), when only pwsh, the libraries and perhaps the OTIO venv exist** (Avail about 810 MB, cap about 410 MB, so the 350 MB lean profile fits); the EffectCraft stage follows with its lean 300 MB figure; and **WP-10 is the package most exposed to the squeeze**: it lists each tarball first, extracts only the members it needs, and if a stage still does not fit it ends `BLOCKED` with the exact message and the remedy (answer Q-1, or move the read-back to the maker's PC). Each stage re-reads `df` live, so this table is a plan and the guard is the authority. A stage whose actual peak exceeds its planned figure by more than 25% records a finding.
- **Keep-tarball rule (each tarball is downloaded once in the fortnight):** WP-07 keeps only the verified FilmCraft v0.9.0 tarball (70 MB) in `vendor/craft/_keep/` for WP-10's T3, **if** Avail after the stage's cleanup is at least 700 MB; otherwise it deletes it and WP-10 re-fetches it once, recorded as a ledger exception. `_keep/` is a git-ignored **hand-off folder**: WP-07 creates it, WP-10 consumes and deletes it, and nothing else crosses that boundary. The download ledger is in WP-07.
- **Always** delete downloads and extracted trees when the test that needed them is done. `scripts/cleanup_scratch.sh --yes` (WP-11a) removes pwsh, venvs and `vendor/craft*` and prints `df`.
- Total downloads for the whole fortnight stay near 540 MB against the 2 GB allowance (ledger in WP-07, plus pwsh 75 MB, npm packs about 10 MB and the OTIO wheel 0.8 MB). **Updated Tue 20 Oct 2026 (week-2 close-out gate): the allowance is now 2,560 MB (2.5 GiB), raised from 2,048 MB.** The two SP3 `bpy` wheel-set fetches (428 MB each, put on the ledger that night) brought the ledgers to 1,506.9 MB, so the third fetch at G1 (Sun 15 Nov) would have left only about 52 MB to spare in the integration test (about 133 MB in the ledger check), and any other fetch (the 70 MB FilmCraft fallback, a PowerShell re-fetch) would have stopped it; with the new allowance the ledgers read about 1,915 MB after it and the whole fortnight about 2,000 MB of 2,560. The figure lives in `spikes/sp1_craft_cli/config.json` (`download_allowance_mb`), `spikes/sp1b_readback/check_ledger.py` (`ALLOWANCE_MB`) and `tests/integration/run_checks.py` (`DOWNLOAD_ALLOWANCE_MB`); the three move together.

**Timed runs:** every measurement that quotes seconds, fps or RSS runs as `lj_bench <command>` (inside `lj_with_disk` when it also writes over 100 MB) and records `nproc` and `/proc/loadavg` at start. Two timed runs never overlap. Results taken while another job's load was visible are marked `contaminated`.

**Untrusted downloads:** each into its own new empty folder (`vendor/craft/<app>-<tag>/`, `<scratch>/pwsh/`); verify SHA-256 before extracting; extract with `tar` into the same fresh folder; **never run a build tool, package manager or interpreter from inside a downloaded tree**; run Python that reads downloaded files with `-I`; use `npm pack` + `tar` instead of `npm install` (no lifecycle scripts). The Craft binaries are *meant* to be executed (that is SP1): run them by absolute path, with `cwd` in a scratch folder outside the tree, `env -i` with a throw-away `HOME`, `timeout`, a memory watchdog, and `unshare -rn` when it works.

**Not committed:** binaries, downloads, renders, fonts, vendored third-party libraries, and **raw PC reports** (4.4). Libraries and fonts are fetched by pinned script and checked against SHA-256 in a lock file (text), licences are kept as text files. At most three small review images (contact sheets, under 200 KB each) may be `git add -f`ed by the orchestrator after review.

**Cross-machine determinism:** frames are identical per machine, Chromium build and font set, not across machines. Cross-environment comparisons use the 100-differing-pixels tolerance (`compare -metric AE -fuzz 1%`), never exact hashes.

### 4.10 Test content (D-28, D-29, D-15)

All test material is synthetic and style-neutral: geometric cards, grids, gradients, digits, frame counters. **No Minecraft or voxel look (D-29). No deity images, names, mantras, shlokas or religious symbols as test content; no Mughal or other Islamic motifs and no Christian motifs (D-28).** The style track, not this plan, decides what the film shows.

**Indic text is parameterised by script, not assumed (nudge 4).** D-28 names "Sanskrit and her regional language", and O-02/O-10 (due Sun 25 Oct) and the proposed O-36 will say which script. W-57 puts the font and caption tests on the Sun 1 Nov card. So Indic text is allowed only as neutral strings from the fixed list `pipeline/phone/test_strings.json` (4.15), **keyed by script**, with **Devanagari as the day-1 entry** (it covers Hindi, Marathi, Nepali and Sanskrit and is the script the plan can supply words for today). Rules:
- Where there is a choice of word, use a Sanskrit-derived (tatsama) neutral word, in the spirit of D-28; avoid words of Persian, Arabic or European origin even when common.
- Nothing devotional, nothing naming a deity, caste, community or place of worship; only digits and plain nouns (test, book, day, number, word).
- Every entry carries `checked_by_reader`. It starts `false`: the planner proposes, and **a person who reads the script (the maker) confirms** before the entry is used in anything the maker sees. Tools may use an unconfirmed entry only for shape tests, never in a file given to anyone.
- Adding a script is three small steps and no new package: one font entry in `libs.lock.json` (the Noto family for that script, fetched with one more `npm pack`), one block in `test_strings.json` with its reader check, and nothing else, because WP-04's font check (A7) and WP-08's shaping, mark and caption checks loop over every script that has strings.
- The settings card's language note records **which script was tested and when** (WP-08's `PHONE-ROW.md` carries the line; WP-02's card shows it).

Fonts are OFL (W-21): Noto Sans, the Noto family for each listed script, and Kalam are used purely as test fonts; no style decision is implied (that is G1). No family media exists or may be created, fetched or simulated as real.

### 4.11 Staged skills

Proposed new or changed skills go to `skills-staging/<skill-name>/SKILL.md` with a `CHANGES.md` saying what changed and why. Nothing under `.claude/` is edited. Only WP-08 and WP-11b stage skills this fortnight.

### 4.12 Definition of done (every package)

1. All acceptance tests pass or are `UNVERIFIED` with a stated reason; evidence JSON written, **each envelope carrying its `disk` figures (4.2)**.
2. `python3 -I scripts/public_lint.py --paths <owned paths>` is clean once WP-03 has landed (before that, the package greps its own output for emails, IPs, `C:\Users`, and handles).
3. No stale value (25 fps defaults, -1.5 dBTP, retired spellings) in any new file.
4. A short `README` section or header comment for every script (what it does, how to run, what it prints, what it never touches).
5. Handed to Fable through the orchestrator **at the wave boundaries in 4.14** (WP-01a alone first; then one bundle per wave; then the readiness map) with the evidence paths; nothing counts as done until `fable-advisor` approves (CLAUDE.md).
6. `tests/<area>/run_tests.sh` exists, takes `--quick` and `--all`, and is listed in WP-11a's runner order.

### 4.13 `scripts/redaction_patterns.json` v1 (owner WP-03; delivered first; frozen)

**One file defines what "identifying data" means, and every scanner reads it** (nudge 3). Round 1 specified the scan four times in three languages by three owners; one scanner would then accept what another rejects (for example a 64-hex ffmpeg hash that WP-09 keeps and an inventory "serial-like" rule would flag). Now no other file in the repo may carry its own copy of these expressions.

| Consumer | Package | Reads the file with | Used for |
|---|---|---|---|
| `win/step0_pc_tests.ps1` | WP-01a | `ConvertFrom-Json` relative to `$PSScriptRoot` | self-scan of the report before it is written (fail closed) |
| `win/kit2/run_checks_pc.ps1` | WP-09 | `ConvertFrom-Json` | self-scan of the PC colour-patch report |
| `scripts/windows_check.py` | WP-01a | `json` by path relative to `__file__` (F-14) | scan of a pasted report; masks every printed hit |
| `scripts/public_lint.py` | WP-03 | `json` | text and path scan of the diff and of untracked files |
| `scripts/ops_lint.py` (reader, not part of the self-test) | WP-02 | `json` | the `note` column of `hours.csv` |

**Content.**
- `schema`, `version`, `dialect`: the common subset of Python `re` and .NET regex: `[0-9]` not `\d`, `\b`, non-capturing groups, character classes, `{m,n}`, lookahead, **fixed-width** lookbehind; no named groups, no possessive quantifiers, no inline flags (the per-category `flags` field is `""` or `"i"`).
- `categories[]`: `{id, scope: "report"|"text"|"both", action: "refuse", regex, flags, description, positive_samples, negative_samples}`. Samples are arrays of string fragments joined at load time, so the file never contains the strings it forbids and does not trip the lint on itself. Required ids: `email`; `ipv4` (documentation ranges 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 and 127.0.0.1 allowed; octets without leading zeros; not flanked by digits or dots); `ipv6` (the 2001:db8::/32 documentation prefix allowed); `mac`; `profile_path_windows` (a Windows profile path, drive then `Users` then a folder name, whose folder name is not the `<user>` placeholder; `%USERPROFILE%` allowed); `profile_path_linux` (a `/home/` or `/Users/` path under any name other than the `user` placeholder); `token_shape` (the GitHub classic and fine-grained token forms, `sk`-style API keys, AWS access-key ids and PEM key-block headers, each with its length rule so a bare prefix in prose is not a hit); `guid_serial` (a GUID in 8-4-4-4-12 form, any hex run of 32 or more characters, and serial-like tokens of 10 to 40 upper-case letters and digits with at least three of each); `handle` (an at-sign social handle; scope `text`, applied to `.md`, `.csv`, `.json` and `.txt` files and never to code, where an at-sign before a variable name is PowerShell splatting).
- `exemptions[]`: `sha256_64hex`, a hex run of **exactly 64** characters not flanked by hex digits, is not a `guid_serial` hit (ffmpeg binary hashes and release checksums are public build identity); a run of 65 or more, or of 32 to 63, still is.
- `field_exemptions[]` (report scope): categories that do not apply to named report fields: `ipv4` in `gpus[].driver_version`, `os.version`, `os.build`, `powershell.version`, `tools.*.version` (version strings, F-15).
- `name_checks`: `sources` (`user`, `computer`, `domain`; read from the environment at run time and never stored); `match` (whole word, case-insensitive, anywhere in the report); `min_name_len` 3 (a shorter name is skipped with a `NOTE`, because it would match ordinary words); `fragment_len` 4 (any 4-character fragment of a name of 5 or more characters); `hardware_name_fields` (`cpu.name`, `gpus[].name`, `gpus[].vendor`, `os.caption`); `hardware_field_action` `report`. **The rule (nudge 1): a name hit anywhere except a hardware-name field refuses the write; a name hit inside a hardware-name field is reported, not refused** (a `NOTE` line with category, field and masked hit, also recorded in `redaction.name_hits_in_hardware_fields[]`), because a short user name will legitimately collide with a vendor name in a GPU string. The pattern categories (e-mail, IP, MAC, path, token, GUID) are never relaxed by this rule.
- `mask`: `{keep: 2, fill: "*"}`. A refusal prints the `category`, the `field` (or `file:line` for the lint) and the masked hit, never the full value.
- `placeholders`: `C:\Users\<user>`, `%USERPROFILE%`, `/home/user`, and `/home/user/build-scratch`, which reads as `<scratch>`.
- `path_denylist[]`: `**/pc_report*.json`, `**/colour_patch_pc*.json`, `**/maker-pc*.json`, refused by `public_lint.py` anywhere in the tree except under `tests/win/fixtures/`, where every file is synthetic.
- `local_deny`: the optional git-ignored `scripts/public_lint.deny.local.txt` (the maker's real names and PC name, loaded on the maker's machine only).

**Required samples** (the minimum; WP-03 writes the regexes and a test per sample). Must be flagged: an e-mail-shaped string on an invented domain; an IPv4 outside the documentation ranges; a full IPv6; a MAC; a Windows profile path under a real-looking user name; a Linux home path under a name other than `user`; a GitHub-token-shaped string of full length; a GUID; a 32-hex run; a 65-hex run; a serial-like token; an at-sign handle in prose. Must not be flagged: `192.0.2.1`, `198.51.100.7`, `203.0.113.9`, `127.0.0.1`; the version strings `10.0.22631.4317`, `31.0.15.5222`, a version ending in a zero-padded part (`23.40.27` then `.06`), `6.1.1`, `9.0.2`; `C:\Users\<user>`, `%USERPROFILE%`, `/home/user`, `<scratch>`; `ffmpeg version 9.0.2-essentials_build-www.gyan.dev` (a domain, not an e-mail); a 64-hex SHA-256; a splatting variable in PowerShell code.

**Consumer contract and the disagreement test.** Each consumer has a pattern self-test that does nothing else: `python3 -I scripts/windows_check.py --pattern-self-test SAMPLES.json`, `python3 -I scripts/public_lint.py --pattern-self-test SAMPLES.json`, `pwsh -File win/step0_pc_tests.ps1 -PatternSelfTest SAMPLES.json`, `pwsh -File win/kit2/run_checks_pc.ps1 -PatternSelfTest SAMPLES.json`. Each reads a samples file (fragments already joined) and prints one JSON object `{consumer, patterns_version, results: {sample_id: [category ids]}}`. **`python3 -I scripts/public_lint.py --self-test`** builds the samples file in `<scratch>`, runs every consumer that exists, and compares each answer with the file's declared expectation and with the other consumers: **any disagreement exits 1 naming the consumer, the sample and the two answers.** A consumer that has not landed is reported `SKIPPED: not landed`, which is not a failure in wave 1 but **is** a failure in WP-11b's final run (zero skips allowed).

### 4.14 Review cadence (nudge 8)

| When | What Fable reads | Evidence attached | What it releases |
|---|---|---|---|
| **Tue 20 Oct, morning, before the maker runs anything** | WP-01a alone | `bash tests/win/run_tests.sh --all`, the parse and lint results, the self-scan refusal transcript (category and masked hit), both short-user-name fixtures, the rendered README, the list of UNVERIFIED Windows claims | The Tuesday drop. If not approved by noon, the maker gets only the README's six paste-in read-only commands (already-approved text), never an unreviewed script |
| **Fri 23 Oct** | Wave 1 as **one bundle**: WP-02, WP-03, WP-04, WP-05, WP-06, WP-07 (guide, sums, T1; T2/T4 may still be running), WP-11a, and WP-09 parts 1-2 as the named exception | `bash scripts/run_week2_checks.sh --quick` output (`build/evidence/wave1_quick.txt` and `INDEX.md`) | The Sat 24 Oct Craft guide and the Mon 26 Oct Ken Burns and archive kit |
| **Wed 28 Oct** | Wave 2 as one bundle: WP-01b, WP-08, WP-09 parts 3-4, WP-10, plus WP-07's T1/T2/T4 results | `run_week2_checks.sh --quick`, and `--all` for the wave-2 areas | The PC colour runner and the phone test file (Thu 29 Oct) |
| **Fri 30 Oct** | WP-11b's `P-LOCK-readiness-W2.md`, the final settings card with its phone row and script note | `run_week2_checks.sh --all` | The card for Sun 1 Nov; the readiness map is the input to the Sun 8 Nov mid-point check |

Definition-of-done item 5 stays: nothing is done until `fable-advisor` approves. What changes is the cadence: one read of WP-01a, one read per wave, then the readiness map, instead of eleven separate package reviews.

### 4.15 `pipeline/phone/test_strings.json` v1 (owner WP-04 for the day-1 entry; frozen; read by WP-04, WP-08, WP-02 and the theme guard)

```json
{"schema":"lj-teststrings/1",
 "rules":"only these strings may appear as test text; neutral; Sanskrit-derived where there is a choice (4.10)",
 "scripts":{
  "latin":{"font_script_tag":"Latn","strings":[{"id":"lat-test","text":"Test 0123","kind":"word"}]},
  "devanagari":{"font_script_tag":"Deva","noto_family":"Noto Sans Devanagari","headline":true,
    "strings":[
      {"id":"dev-digits","text":"०१२३४५६७८९","kind":"digits","marks":[],"checked_by_reader":false},
      {"id":"dev-pariksha","text":"परीक्षण","gloss":"test","kind":"word",
       "marks":[{"codepoints":["U+0940"],"kind":"post_base"},{"codepoints":["U+094D"],"kind":"conjunct"}],
       "checked_by_reader":false}]},
  "tamil":{"status":"pending_O-10","strings":[]}, "telugu":{"status":"pending_O-10","strings":[]},
  "kannada":{"status":"pending_O-10","strings":[]}, "malayalam":{"status":"pending_O-10","strings":[]},
  "bengali":{"status":"pending_O-10","strings":[]}, "gujarati":{"status":"pending_O-10","strings":[]}}}
```
Day-1 Devanagari entries (the planner's proposal; the maker confirms): the ten digits; `परीक्षण` (test: a long vowel sign and a conjunct), `पुस्तक` (book: a below-base vowel sign and a conjunct), `दिन` (day: a pre-base vowel sign), `संख्या` (number: an above-base dot and a conjunct), `शब्द` (word: a conjunct with a halant). All five words are plain nouns of Sanskrit origin. `marks[]` lists, per string, each mark's codepoints and its `kind` (`above`, `below`, `pre_base`, `post_base`, `split`, `conjunct`); WP-08 strips those codepoints to derive the mark's zone by differential rendering, so **no zone coordinate is stored or assumed**. The scripts differ in where marks sit and how they stack (Tamil, Telugu, Kannada, Malayalam, Bengali and Gujarati each have their own conventions), and a reader of the script fills their `marks[]`. A script whose `strings` is empty is skipped by every test and listed as `NOT TESTED` in `PHONE-ROW.md`. `libs.lock.json` (WP-04) names the Noto family per script (day 1: Noto Sans Devanagari; the others as `pending_O-10`, package names to be confirmed at fetch time, UNVERIFIED).

### 4.16 Derived PC evidence: the only PC data that may be filed (owner of the folder: WP-11b)

The raw reports (4.4) stay with the maker. The orchestrator writes a pasted raw report to a file in `<scratch>` (never in the repo) and derives:
- **`pc_tier.json`** (`windows_check.py --tier-json-out`; schema `win/schema/pc_tier.schema.json`, `additionalProperties: false`): `{schema: "lj-pc-tier/1", date (day only), windows {edition_family, build_major}, gpu_tier, vram_bucket, ram_tier, disk_tier, display_class, shared_pc_hint, ffmpeg {version, sha256, has_libx264, has_libass, has_zscale}, python_ok, git_ok, craft_pins [{app, status}]}`. No CPU or GPU model, no exact sizes, no driver versions, no account counts.
- **`pc_chains.json`** (`colour_patch.py --derive-from RAW --out DERIVED`, WP-05): `{schema: "lj-pc-chains/1", ffmpeg {version, sha256}, chains [{name, worst_error, pass}]}`. No configure flags, no paths.

Both are filed under `build/evidence/pc/`. A test greps them for every GPU, CPU and driver string in the synthetic fixtures and finds none. `windows_check.py --hardware-md PATH` writes the draft of `decisions/hardware.md` (the file the ai-photo skill reads) in the same bucketed terms: tier words, VRAM, RAM and free-disk buckets, Vulkan yes or no, and **no model names**; that bucketed draft is what the orchestrator may place in the repo (conflict C-11).

---

## 5. Work packages

### WP-01a Windows kit A: PC inventory, report checker, tools, pins, schema, fixtures, maker README

**Wave 1. Runs: both** (container tests with pwsh and fixtures; the maker runs the real thing). **Refs:** W-06, W-22, W-25, W-28, D-02, D-10, D-15, D-25, D-26, O-03.

**Owner paths:** `win/step0_pc_tests.ps1`, `win/README-MAKER.md`, `win/tiers.json`, `win/pins.json`, `win/schema/pc_report.schema.json`, `win/schema/pc_tier.schema.json`, `win/tools/**`, `scripts/windows_check.py`, `tests/win/**`, `build/evidence/wp01a/**`.

**Goal.** By Tue 20 Oct the maker can run one read-only script, get a redacted `pc_report.json` in `%TEMP%`, read it and paste it in chat, and the agents can validate it and read the hardware tier the playbooks key on. **Fable reads this package alone, Tuesday morning, before the maker runs anything** (4.14). WP-01a deletes nothing, commits nothing, installs nothing and changes no setting; `lj.ps1`, the only tooling that can remove a file, is **not in this package** (nudge 1, now WP-01b), so the first thing a learner downloads contains nothing destructive.

**Start gate.** `scripts/redaction_patterns.json` from WP-03 (4.13). The script, the checker, the tools and the README can be written against the frozen schema at once; only the self-scan tests wait for the file.

**Deliverables**
1. `win/step0_pc_tests.ps1`: read-only inventory producing the 4.4 schema. Params: `-Out` (default `%TEMP%\lj_pc_report.json`, printed in that unexpanded form), `-ToolsRoot` (scan list defaults to `C:\lj\tools` and `C:\LifeJourney\tools`; see conflict C-04), `-Print`. Prints each step before it runs. Does not execute any Craft binary (versions come from the folder name and the file's version resource); does run `ffmpeg -version`, `ffprobe -version`, `git --version`, `python --version`, `wsl --status`, `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader` and `vulkaninfo --summary` when present, and takes the SHA-256 of the ffmpeg binary (the hash is recorded, the path is not). VRAM order: `nvidia-smi`, then registry `qwMemorySize`, then `AdapterRAM` flagged `adapterram_capped_4gb` when it equals 4294967295 or 4 GB (F-11).
   **Self-scan before writing** (one source, nudge 3): loads `scripts/redaction_patterns.json` relative to `$PSScriptRoot` (missing or unparsable: exit 2, nothing written); reads the current user name, computer name and domain from the environment (never stored); scans every string leaf of the finished object with the 4.13 categories (honouring `field_exemptions`) and the name checks (whole name, and 4-character fragments of names of 5 or more characters). **On a refusal it prints `REDACTION CHECK FAILED, nothing was written` and one line per hit: `category=<id> field=<json path> hit=<first two characters plus asterisks>`, and exits 2** (nudge 1: the maker is told what kind of thing matched and where, without the value). **A name hit inside a hardware-name field (4.13) is printed as `NOTE category=... field=... hit=...`, recorded in `redaction.name_hits_in_hardware_fields[]`, and does not refuse**, so a short user name that is also a vendor name does not block the maker on day one. Test modes `-TestFixture PATH -FakeUser X -FakeComputer Y -FakeDomain Z` (collects nothing, self-scans the fixture as if it were the finished report) and `-PatternSelfTest SAMPLES.json` (4.13).
2. `scripts/windows_check.py`: standard-library validator. Reads UTF-8, UTF-8-BOM and UTF-16. Validates against the schema, runs the identifying-data scan **from the same pattern file** (plus any `--forbid WORD` given on the command line, so the maker's real name or PC name can be checked on the PC without ever being stored; the same hardware-name-field rule applies), and prints the **tier table**: `gpu_tier` (`none` / `gpu-low` / `gpu-8-12` / `gpu-16+` / `unknown`; a software device such as llvmpipe, SwiftShader or "Basic Render" counts as none), `ram_tier` (`<8` below the Blender floor, `8-15` WSL2 not advised, `16+`), `edition` (BitLocker offered only on Pro or higher; VeraCrypt file container works on all), `disk` (free space on the project drive against thresholds), `ffmpeg` (version; the colour-patch test must be run on exactly this build), Python, Git, Craft pins (`match`, `fallback pin`, `mismatch`, `absent`), `shared_pc_hint` from `local_accounts_count` (O-03). Thresholds live in `win/tiers.json` with a `source` for each (Blender floor 4 cores/8 GB/2 GB VRAM from `research/toolchain.md`; GPU tiers from `playbooks/ai-imagery.md` Decision 2; WSL2 at 16 GB from `research/toolchain.md` F3; disk thresholds are the planner's proposal, marked (J)). Exit meaning: `0` the report is valid and nothing needs a human; `1` valid but a finding needs a human (VRAM unreadable, ffmpeg or Python missing, a Craft pin mismatch, not a Windows report); `2` invalid, identifying data found, or the pattern file missing. **A low tier (no GPU, 8 GB RAM, Home edition) is information, not a failure.** Options: `--json-out`; **`--tier-json-out PATH`** (the derived file of 4.16, the only form of PC data that may be filed in the repo); `--hardware-md PATH` (a bucketed draft of `decisions/hardware.md`, no model names; conflict C-11); `--pattern-self-test SAMPLES.json` (4.13). Never prints a flagged value back in full (first two characters plus asterisks).
3. `win/README-MAKER.md`: plain-language, no jargon, exact copy-paste lines in fenced `powershell` blocks (every block parse-tested). Sections: what this is and what it never does; how to get the files onto the PC (**the whole project folder** from the link in your notes, by browser download or `git clone`; single files will not work because the script reads `scripts\redaction_patterns.json` and stops without it); **how to run a script for one session only without changing system policy** (three options below); the 3-minute PC inventory; **reading the report yourself before you paste it** (open `%TEMP%\lj_pc_report.json` in Notepad; it goes into the chat and nowhere else, never into the project folder or git); **if the script refuses to write the report** (new, nudge 1): what `category`, `field` and `hit` mean, that the refusal text carries only a category and two letters and is safe to paste, that a short user name can collide with a vendor name (a hit inside the processor or graphics-card name is only a note and the report is still written), that you must not edit the JSON by hand to get past it, and what to paste (the refusal lines plus the six commands below) so the orchestrator can adjust the rule the same day; "if it fails": six one-line read-only commands to paste; what comes next, **by title and without links to files that do not exist yet** (the hours page, the Craft-zip guide, the Ken Burns and archive kit, `lj.ps1` on Tue 27 Oct); and one paragraph that the VeraCrypt container (Wed 28 Oct) is created from an administrator account and mounted from the project account (W-25).
   - Option A: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\step0_pc_tests.ps1` (policy bypassed for that one process only).
   - Option B: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force` then `.\win\step0_pc_tests.ps1` (lasts until the window closes; machine and user policy unchanged).
   - Read-only diagnostics: `Get-ExecutionPolicy -List`; `Unblock-File .\win\step0_pc_tests.ps1` explained as affecting only that file's "downloaded from the internet" mark.
   - If Group Policy overrides both: stop, change nothing, tell the orchestrator; the "wrap the pasted text in `& { ... }`" fallback is **UNVERIFIED** on 5.1 and must be tested on pwsh before it is written down.
4. `win/tools/`: `fetch_pwsh.sh` (idempotent: runs under `lj_with_disk 275`, downloads the 7.5.4 Linux tarball into a new empty folder, verifies SHA-256 against the release's `hashes.sha256` asset if reachable else records the hash, prints `df` before and after), `ps_parse.sh` (runs `Parser::ParseFile` on every `.ps1` under `win/` and every `powershell` fence in the READMEs of WP-01a, WP-01b, WP-07 and WP-09 that exist), `ps_lint.py` (5.1-compatibility rules from 4.7, including "no machine- or user-scope `Set-ExecutionPolicy`").
5. `win/pins.json` (versions from W-22: PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 with fallback 0.8.0, EffectCraft 0.11.1, SoundCraft none), `win/tiers.json`, `win/schema/pc_report.schema.json` and `win/schema/pc_tier.schema.json`.
6. `tests/win/`: synthetic fixtures only (all names and addresses invented, using reserved example domains and documentation IP ranges): `report_nogpu_home_8gb`, `report_gpu12_pro_16gb`, `report_gpu24_pro_32gb`, `report_software_gpu`, `report_vram_capped_only`, `report_vram_nvidia_over_cap`, `report_old_ffmpeg6`, `report_ffmpeg9`, `report_craft_pins_mixed`, `report_identifying` (planted fake user name, fake computer name, documentation IPv4, `.invalid` e-mail, profile path), `report_bom`, a UTF-16 file generated at test time with `iconv`, and the new ones: **`report_short_username_collision`** (an invented 4-character user name that also appears in the GPU name field: reported, not refused), **`report_short_username_leak`** (the same name in `tools.git.notes`: refused), `report_version_strings_not_ip` (driver, OS and tool version strings shaped like IPv4: accepted), `report_sha256_ok` (a 64-hex ffmpeg hash: accepted) and `report_hex65_leak` (a 65-hex run in a note: refused).

**Acceptance tests (run in the container)**
```bash
source scripts/lj_guard.sh
lj_with_disk 275 wp01a-pwsh -- bash win/tools/fetch_pwsh.sh /home/user/build-scratch/pwsh   # exit 0; prints SHA-256 and df before/after
bash tests/win/run_tests.sh --all     # runs every line below; exit 0 only if all pass (--quick: parse, lint and fixture lines)
python3 -I win/tools/ps_lint.py win/step0_pc_tests.ps1                                         # exit 0
bash win/tools/ps_parse.sh                                                                     # 0 parse errors in the script and every README fence
/home/user/build-scratch/pwsh/pwsh -NoProfile -File win/step0_pc_tests.ps1 -Out renders/wp01a/linux_report.json   # on Linux: exit 0, os.platform non-windows
python3 -I scripts/windows_check.py renders/wp01a/linux_report.json  # exit 1, "NOT A WINDOWS REPORT"
python3 -I scripts/windows_check.py tests/win/fixtures/report_gpu12_pro_16gb.json   # exit 0, gpu-8-12, ram 16+, Pro, WSL2 ok
python3 -I scripts/windows_check.py tests/win/fixtures/report_nogpu_home_8gb.json   # exit 0; gpu none, ram 8-15, Home, BitLocker not offered (information, not failure)
python3 -I scripts/windows_check.py tests/win/fixtures/report_software_gpu.json     # exit 0; gpu none ("Basic Render" counts as no GPU)
python3 -I scripts/windows_check.py tests/win/fixtures/report_vram_nvidia_over_cap.json # exit 0; VRAM taken from nvidia-smi, not the capped field
python3 -I scripts/windows_check.py tests/win/fixtures/report_vram_capped_only.json # exit 1, "VRAM unreadable"
python3 -I scripts/windows_check.py tests/win/fixtures/report_ffmpeg9.json          # exit 0; prints "run the colour-patch test on this build"
python3 -I scripts/windows_check.py tests/win/fixtures/report_craft_pins_mixed.json # exit 1; one match, one fallback pin, one mismatch, one absent
python3 -I scripts/windows_check.py tests/win/fixtures/report_identifying.json      # exit 2, one line per category as category= field= hit=xx**, no value echoed in full
python3 -I scripts/windows_check.py tests/win/fixtures/report_bom.json              # same result as the plain file
python3 -I scripts/windows_check.py --forbid exampleperson tests/win/fixtures/report_gpu12_pro_16gb.json  # exit 0 (not present)
python3 -I scripts/windows_check.py --forbid zeta tests/win/fixtures/report_short_username_collision.json  # exit 0 with a NOTE (hit is in gpus[0].name only)
python3 -I scripts/windows_check.py --forbid zeta tests/win/fixtures/report_short_username_leak.json       # exit 2: category=user_name field=tools.git.notes hit=ze**
python3 -I scripts/windows_check.py tests/win/fixtures/report_version_strings_not_ip.json  # exit 0 (driver versions are not IP addresses)
python3 -I scripts/windows_check.py tests/win/fixtures/report_sha256_ok.json               # exit 0 (64-hex exempt)
python3 -I scripts/windows_check.py tests/win/fixtures/report_hex65_leak.json              # exit 2, category=guid_serial
python3 -I scripts/windows_check.py --tier-json-out renders/wp01a/pc_tier.json tests/win/fixtures/report_gpu12_pro_16gb.json   # exit 0; validates against pc_tier.schema.json
```
- **Tier file leaks nothing:** a test greps `renders/wp01a/pc_tier.json` for every GPU, CPU and driver string and every exact size in the fixture and finds none; the schema has `additionalProperties: false`.
- **Self-scan (script side):** `pwsh -File win/step0_pc_tests.ps1 -TestFixture tests/win/fixtures/report_identifying.json -FakeUser <invented> -FakeComputer <invented> -FakeDomain <invented> -Out renders/wp01a/none.json` exits 2, stdout contains `category=` and a masked hit, stdout never contains a fake name in full, and `renders/wp01a/none.json` does not exist. The same with `report_short_username_collision.json -FakeUser zeta` exits 0, prints a `NOTE` and writes the file; with `report_short_username_leak.json` it exits 2 and names `tools.git.notes`.
- **Fail closed:** a copy of `win/step0_pc_tests.ps1` placed in a temp tree without `scripts/redaction_patterns.json` exits 2 and writes nothing; the same for `windows_check.py`.
- **One source:** `python3 -I scripts/public_lint.py --self-test` (WP-03) includes both consumers of this package and reports no disagreement; this package contains no copy of an identifying-data regex (`grep` test over `win/` and `scripts/windows_check.py` for the e-mail, IPv4 and MAC shapes finds nothing outside the pattern file).
- README test: every fenced `powershell` block parses; every referenced file exists (the "what comes next" titles are not paths); every heading named above is present; a pass with the 4.13 patterns finds no handle, e-mail, IP or absolute user path. A planted README block with a machine-scope `Set-ExecutionPolicy` makes `ps_lint.py` exit 1.
- Directory hash before and after any test-mode run shows the only new file is the `-Out` file (or none on a refusal).

**UNVERIFIED until the maker's first run (listed in the evidence JSON):** every CIM/WMI query, registry reads, `Get-LocalUser`, `System.Windows.Forms` screen bounds, `winget`, `wsl --status`, `nvidia-smi` output format, Vulkan detection (a DLL on disk is only a hint; the Real-ESRGAN test remains the proof), the `%TEMP%` default on a managed PC, Windows PowerShell 5.1 behaviour of every cmdlet, Group Policy handling, and whether version strings on the maker's PC trip any pattern.
**Fallback:** if the script fails on the PC or is not approved in time, the README's last section lists six one-line read-only commands the maker can paste (OS build, RAM, GPU name, free disk, `ffmpeg -version`, `py -0p`); the orchestrator reads those lines by eye (no free-text parser is built).

---

### WP-01b `lj.ps1` `doctor` and `close` v0, dry-run only

**Wave 2** (after the Sat 24 Oct five-minute tests, which show where each Craft app writes). **Runs: both.** **Refs:** W-26, W-06, W-29, D-12, D-15, D-25; assumption A-04.

**Owner paths:** `win/lj.ps1`, `win/lj.config.example.json`, `win/README-LJ.md`, `tests/win_lj/**`, `build/evidence/wp01b/**`.

**Goal.** A first version of the single session-close command (W-26) that shows the maker exactly what a close *would* remove, and a `doctor` that prints the hardware tier, **without being able to delete, commit, push or write anything**. Round 1 put `-Apply` (which deletes) and `-Commit` (which runs git) in the same Tuesday drop as the inventory, with every target list empty and UNVERIFIED; nudge 1 moved all of that after Sat 24 Oct and to week 4. In v0 those switches **do not exist**.

**Input from the maker (not a package dependency):** the output of the "where did it write" step in WP-07's `MAKER-CRAFT-ZIPS.md` (a listing of folders touched in the last hour under `%APPDATA%` and `%LOCALAPPDATA%`, printed with the profile path replaced by `%USERPROFILE%`). If it has not arrived by Mon 26 Oct, WP-01b ships with the per-app lists empty and says so (UNVERIFIED).

**Deliverables**
1. `win/lj.ps1` with `doctor`, `close`, `help`.
   - **`doctor`** runs the sibling `step0_pc_tests.ps1` (or reads an existing report with `-FromReport PATH`, used by tests and re-checks), then `windows_check.py` through `py -3 -I` or `python -I` if either exists, and prints the tier table. It writes nothing unless `-SaveTier PATH` is given, and then writes only the derived tier file of 4.16, never the raw report.
   - **`close` is a dry run, always.** It prints a numbered list of every file and folder it *would* remove, with counts and sizes, then a list of what it will never touch (anything under `media`, `archive`, `masters`, `originals`, the repo, any mounted container, any drive root, any path outside the configured root), then runs the read-only `stale_check.py --new-only` and `public_lint.py` if Python exists, prints `BACKUP: not implemented in v0 (week 4)` and the reminders (dismount the encrypted container, close the Craft apps). **It writes nothing, not even a log.** The configured root is validated first and refused (exit 2) if it is a drive root, the repo root or the profile root; reparse points (symlinks, junctions) are listed as `SKIPPED (link)` and never followed.
   - Targets in v0: `*.xmp` sidecars under `work` folders; folders named `Recovery`, `Auto-Save` or `cache` under the tools root; and, for each Craft app, a documented list for its recent-file list and (LightCraft) cache, filled from the maker's paste or left empty and marked UNVERIFIED.
   - Passing `-Apply`, `-Commit` or `-IncludeWindowsRecent` prints `not in v0: planned for v1 in week 4; nothing was done`, and exits 2.
2. `win/lj.config.example.json` (root, tools root, per-app lists) and `win/README-LJ.md` (plain language, parse-tested fences: what `doctor` and `close` show you; that `close` does nothing yet; how to read the list). Both are owned here so WP-01a's README never has to change.
3. `tests/win_lj/`: synthetic trees on Linux paths.

**Acceptance tests** (`bash tests/win_lj/run_tests.sh --all`, pwsh from WP-01a)
```bash
python3 -I win/tools/ps_lint.py win/lj.ps1 && bash win/tools/ps_parse.sh      # 0 errors, README fences included
pwsh -NoProfile -File win/lj.ps1 doctor -FromReport tests/win/fixtures/report_gpu12_pro_16gb.json   # prints the tier table; directory hash before/after identical
pwsh -NoProfile -File win/lj.ps1 doctor -FromReport tests/win/fixtures/report_gpu12_pro_16gb.json -SaveTier renders/wp01b/tier.json   # only the derived file appears; no fixture GPU or CPU string in it
pwsh -NoProfile -File win/lj.ps1 close -Config tests/win_lj/planted.config.json   # lists the planted *.xmp, Recovery and cache items; tree hash identical; exit 0
pwsh -NoProfile -File win/lj.ps1 close -Apply        # exit 2: "not in v0 ... nothing was done"; same for -Commit and -IncludeWindowsRecent
pwsh -NoProfile -File win/lj.ps1 close -Config tests/win_lj/root_is_slash.config.json   # exit 2; also the repo root and $HOME
```
- Canary files under `media/`, `archive/` and a symlink pointing outside the root appear under "will never touch" or "SKIPPED (link)" and are never listed as removable.
- No network call is made by `doctor` or `close` (verified under `unshare -rn`).
- The evidence JSON lists as `UNVERIFIED`: every Windows path behaviour, reparse-point handling on NTFS, `py -3 -I` availability, and every per-app list not filled from a real paste.

**What this does and does not satisfy.** W-26 and W-06 want `lj.ps1 close` "written and run once" by P-LOCK. v0 is a dry run the maker can run once in week 3; the real `close` (v1: `-Apply`, `-Commit` without push, backup, log) is built in week 4 (ROADMAP row 4) and its end-to-end run is the P-LOCK pass condition. The readiness map (WP-11b) will say `v0 done, v1 not started` rather than mark the item passed.

---

### WP-02 Ops files and hours report

**Wave 1. Runs: container.** The hours part may go out today on lint and test evidence alone (a CSV and one page). **Refs:** W-02, W-06, W-12, W-13, W-14 to W-19, W-57, O-01, O-10, O-12, O-14, O-15, D-02, D-13, D-15, D-17, D-26, D-27, D-28, W-10, W-49.

**Owner paths:** `ops/**`, `scripts/ops_lint.py`, `scripts/decisions_to_csv.py`, `scripts/hours_report.py`, `tests/ops/**`, `build/evidence/wp02/**`.

**Deliver in this order** (the first item is needed today):
1. `ops/hours.csv` (header only, exactly the schema of `research/production-scale-fixtures/hours.csv`: `date,shot_or_chapter,activity,minutes,who,note`; activity enum `gather|scan|story|brief_G0|style_G1|review_G2|craft_refine_G3|chapter_G4|dignity_G5|tech_G6|sound|grade|mix|captions|master|qc|admin|learn|rework|event`), `ops/HOURS-HOWTO.md` (one page, plain words: what counts, round to 5 minutes, use `-` in `shot_or_chapter` until shots exist, three examples, "this is the one file you type into; log honestly, the plan is built on what you actually did", and **"no names in `note`: IDs and relation tokens only" because the file lives in a public repository**), and `scripts/hours_report.py` (weekly totals by activity; the **indicative** W-02 reading: under about 8 h means the 6-minute F-0 would become the plan on Sun 1 Nov, 8 to under 14 means 9 minutes, 14 to under 16 means 12 only with added hours, 16 or more means 12; always printed as "indicative, the maker's reliable-hours number in writing decides").
2. `ops/decisions.csv` generated by `scripts/decisions_to_csv.py` from `DECISIONS.md` (never hand-typed): columns `id,table,short_title,value_or_default,status,decide_by,owner,source,last_changed,maker_answer,note`; 166 rows (D-01..D-30, W-01..W-60, O-01..O-35, S-01..S-41); `status` vocabulary `decided`, `default`, `open`, `pending`, `answered`, `superseded`, `applied`, `outstanding`; long values cut at 300 characters with `... see DECISIONS.md`; `maker_answer` and `last_changed` empty (orchestrator-owned; O-05 and O-13 pre-marked `answered`); D-14 and D-23 carry the note "superseded by D-26" and "superseded by D-29" (conflict C-07); S rows carry the Table 4 Status. Also a header-only `ops/gate_log.csv` with the existing production-scale gate-decision schema (`date,gate_id,runtime_before_min,runtime_after_min,trigger,measured_value,hours_per_week_H,decision_text,who`) so the planning skill still finds its log (conflict C-05).
3. `ops/GATHER.md`: IDs only. Part A "Before P-LOCK (own material and stand-ins only)": the week-1 own-material list as checklist lines with blanks for IDs (O-06 hands per era, O-07 the hum, O-08 object-clock candidates `OBJ-01..05`, O-09 existing voice recordings `REC-xx` with where they live as a relation token, O-10 ten-line family profile, O-11 answers from own knowledge, Mum-test per shared device `DEV-xx`, code name, project email), and the five stand-in scans (`LJ-ST-0001-F` to `-0005-F`, box code `ST` so a stand-in can never be mistaken for a real item). Part B "From Sun 15 Nov, only after P-LOCK passes": item classes (photo, print back, album page, object, letter, recording, place) each with the fields `id, class, holder (relation token only), cloud (default none), consent state, allowed_use, as-found photographed y/n, scanned y/n, returned y/n`, and the rules in one line each (D-02 covert, D-13 gate, D-15 privacy, D-17 never record her, W-49 album-and-hands under a true sentence, one-key-three-guards for hard items, borrow log, return same day). No names, addresses or relationships beyond tokens like `[relation]`.
4. `ops/SETTINGS-CARD.md`: proposal for the maker to sign Sun 1 Nov, written for a non-technical reader: one table, one row each for **TD-1 size (W-15)**, **TD-2 frame rate (W-14)**, **TD-3 captions (W-18)**, **TD-4 DCP standard (W-17)**, plus the sound/loudness and colour rows the register's W-16 puts on the card, plus a **Phone row (D-27)**. Columns: what it means in plain words, proposed value, register ID, the command that proves it, what changes if you change it. The phone row uses the planner's proposal (1920x1080 or 1280x720, 24 fps, H.264 High, BT.709, -16 LUFS / -1 dBTP, burned-in captions at a larger phone size to be set by the WP-08 test, transfer by cable or a private link only) and says **"proposed; WP-08 may refine the numbers before Sun 1 Nov; the orchestrator pastes `pipeline/phone/PHONE-ROW.md` over this row"**. Also a **Language and script** line: a non-Latin or code-switched film language adds font and caption tests (W-57; likely for this family, but the language is the maker's answer, O-02, O-10, O-15), and the line reads `Caption and font test ran in: devanagari (neutral test strings) on <date>; other scripts NOT TESTED until the maker's script is named`, with the script list and date pasted by the orchestrator from the `Scripts tested:` line of `pipeline/phone/PHONE-ROW.md` (WP-08), so the card records which script was tested and when. Signature block: `signed: no` and a date line, typed by the orchestrator when the maker says so.
5. `scripts/ops_lint.py`: checks that `ops/decisions.csv` matches `DECISIONS.md` (ID set equal, no duplicates, valid statuses), `hours.csv` header and enum, the card's rows and cited IDs, GATHER.md ID patterns and the gate sentence, and that none of the four files contains an e-mail, IP, handle or `TODO`, **all taken from `scripts/redaction_patterns.json` (4.13), never from a local copy of a regex**; it also checks the **`note` column of `hours.csv`** against the same categories and against the local deny list when present (nudge 3), and warns on a note over 80 characters (probably prose about a person) (J).

**Acceptance tests**
```bash
python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv
python3 -I scripts/decisions_to_csv.py --check ops/decisions.csv     # exit 0; 166 rows: D 30, W 60, O 35, S 41; --write twice is byte-identical
bash tests/ops/run_tests.sh                                           # runs the rest
python3 -I scripts/ops_lint.py                                        # exit 0
python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19    # header only: "no rows yet", exit 0
python3 -I scripts/hours_report.py tests/ops/fixtures/hours_9h30.csv --week-start 2026-10-19   # total 9.5 h, "9 minutes" reading
python3 -I scripts/hours_report.py tests/ops/fixtures/hours_7h30.csv --week-start 2026-10-19   # "under about 8 hours ... F-0 would become the plan"
python3 -I scripts/hours_report.py tests/ops/fixtures/hours_bad_activity.csv   # exit 1, names the line number
python3 -I scripts/ops_lint.py --hours tests/ops/fixtures/hours_bad_note.csv    # exit 1, names the line and the category (a planted e-mail-shaped string, a profile path, a name from a test deny list), masked
```
- Negative tests on a temp copy: delete one ID row, add one invented ID, change a header name: each makes `--check` or `ops_lint.py` exit 1 and name the problem.
- The card contains the strings TD-1, TD-2, TD-3, TD-4, "Phone", D-27, the `Language and script` line, and every cited ID exists in `DECISIONS.md` (string presence is an acceptable test for a document).
- `HOURS-HOWTO.md` contains the "no names in note" sentence; `hours_9h30.csv` and `hours_7h30.csv` pass the note check.

**Notes.** Phone numbers in the card are labelled "proposed (J)"; nothing in the card is signed by an agent. The card must not claim any Windows number as verified (W-28).

---

### WP-03 Shared checks: redaction patterns (4.13), disk and bench guard (4.9), `stale_check.py`, `public_lint.py`, theme guard

**Wave 1. Runs: container.** **Refs:** W-29, S-01 to S-41 (Table 4), D-26, D-28, D-15, risk 14 in ROADMAP section 12.

**Owner paths:** `scripts/redaction_patterns.json`, `scripts/lj_guard.sh`, `scripts/stale_check.py`, `scripts/stale_patterns.json`, `scripts/stale_allowlist.json`, `scripts/stale_baseline.json`, `scripts/public_lint.py`, `scripts/public_lint.config.json`, `tests/hygiene/**`, `build/evidence/wp03/**`.

**Deliverables.** Items 1 and 2 are small and everything else in the fortnight leans on them: deliver them in the first hours of wave 1, ahead of items 3 to 9.

1. **`scripts/redaction_patterns.json` (4.13).** All required categories, the `sha256_64hex` exemption, `field_exemptions` for version fields, `name_checks` with the hardware-name-field rule, `mask`, `placeholders`, `path_denylist`, `local_deny`, and every required positive and negative sample, built from fragments. An internal test (`tests/hygiene/test_patterns.py`) checks: every regex compiles in Python; no regex uses a construct outside the stated dialect (named groups, possessive quantifiers, variable-width lookbehind, `\d`); every category has at least one positive and one negative sample; every required sample is present; the file contains none of the strings it forbids. When it passes, WP-03 writes `build/evidence/wp03/LANDED-4.13.txt` (a one-line marker the orchestrator and WP-01a look for). Only WP-03 changes this file, and every change reruns `public_lint.py --self-test`.
2. **`scripts/lj_guard.sh` (4.9).** `lj_df_avail_mb`, `lj_with_disk`, `lj_bench`, `LJ_DF_CMD`, and the environment knobs for tests (`LJ_LOCK_WAIT_S`, `LJ_FLOOR_MB`, `LJ_HARD_FLOOR_MB`, `LJ_POLL_S`). README header in the file: how to call it, what it prints, what it never touches.
3. `scripts/stale_check.py` (standard library; read-only). Scans `playbooks/`, `.claude/skills/`, `skills-staging/`, `research/*-fixtures/`, `research/sources/` and `win/`, `pipeline/`, `scripts/`, `ops/`, `spikes/`. **Excludes** (historical or authoritative): `research/*.md`, `reviews/`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CHARTER.md`, `CLAUDE.md`, `build/`, and its own pattern, allowlist and baseline files and test fixtures (which quote the stale strings on purpose).
4. `scripts/stale_patterns.json`: one entry per detectable Table 4 row with `row_id`, `regex`, `severity` (`FAIL` unambiguous, `WARN` needs a human, e.g. "at L1"/"for L1" which can be a legitimate honesty level), `canonical`, `positive_samples[]`, `negative_samples[]`. Minimum content: the W-29 list (retired spellings of the process lock: "L1 process lock", "L1 lock"; of the spikes: "spikes S1-S5", "spike S1", "S1-S5", "S1 to S5"; and the phrases "not applied here", "for the scribe", "pending scribe", "Deltas to existing", "so that a scribe can patch"); S-01 (`fps=25`, `-r 25`, `-framerate 25`, `d=125`, `Timebase 25`, `indeterminateTimebase` with `"25"`, `atsc_1080p_25`, "at 25 fps", "9,000 frames", "25 frames a second"); S-28 (`-1.5 dBTP`, `TP=-1.5`); S-03, S-05 (co-keeper, Key 1/Key 2, two keys, both keys), S-06, S-13, S-16 to S-19 (25-minute private cut, 12-minute floor, four chapters of 2:15, "8 to 12 minute", private cut 20 to 30 minutes), S-21, S-22, S-24, S-26, S-27, S-29, S-35, S-37. Every Table 4 row either has a pattern or is listed in the report under "not machine-checkable (prose), with reason".
5. `scripts/stale_allowlist.json`: exactly the W-29 allowlist, each entry with `file`, `context regex`, `reason` and the register row: `playbooks/music-sound.md` "not applied here" (DX-gated check, broadcast anchor); negations ("no co-keeper", "Rings 1 and 2 are empty", "there is no insider"); a 25 next to "tested at 25, UNVERIFIED at 24" or "access copy only if a 50 Hz venue judders"; "Ring 1" inside "gathering 14". `--audit-allowlist` lists entries that match nothing (dead entries fail the audit).
6. Modes: default report mode (writes `--json` and `--md`), `--strict` (exit 1 on any non-allowlisted FAIL hit; the pre-gate mode), `--baseline` (writes `scripts/stale_baseline.json`: counts and locations of today's hits), `--new-only` (exit 1 only for hits not in the baseline; used by `lj.ps1 close` until the Haiku passes land, so the maker is not trained to ignore a permanently failing check), `--self-test`.
7. **Run once now** and write `build/evidence/wp03/stale_check_report.{json,md}`: counts per Table 4 row; for rows marked *applied* in Table 4 any hit is listed under **REGRESSIONS** (this is the most useful output: it shows what the scribes thought they fixed but did not); for rows marked *outstanding* (S-01, S-38, S-39, S-40) the hit list is the Haiku work order; then an **INFO: candidate new Table 4 rows** section counting consequences of D-27/D-28/D-29 that Table 4 does not yet cover ("Minecraft", "voxel", "Mojang" in playbooks and skills now contradict D-29; generic-holiday placeholders such as Hanukkah, Christmas, Ramadan, Ash Wednesday and Lunar New Year in the calendar sit beside a Hindu household's actual observances, conflict C-08). **Do not fix any hit; owner files are not in this package.** The first run is expected to exit 1.
8. `scripts/public_lint.py`: scans the git diff and untracked files (or `--paths`) with the **4.13 categories** (it reads the file; it carries no regex of its own for e-mail, IP, MAC, paths, tokens, GUIDs or handles); plus NUL bytes (binary); files over 1 MB; media and image extensions that `.gitignore` already blocks (it reports ignored-but-staged files); the **`path_denylist`** (a file named like a raw PC report is refused wherever it sits, except under `tests/win/fixtures/`); optionally the **local deny list** `scripts/public_lint.deny.local.txt` (git-ignored by the orchestrator's `*.local.*` rule) holding the maker's real names and PC name, loaded only on the maker's machine. `/home/user` is the generic placeholder and `/home/user/build-scratch` reads as the literal `<scratch>`; neither is flagged, while `/home/<any other name>` is. Prints findings masked (`category`, `file:line`, first two characters plus asterisks). Used by WP-01b's `lj.ps1 close` (read-only in v0), WP-02, WP-11a, WP-11b and the orchestrator before every commit. **`--self-test`** is the 4.13 disagreement test: it runs every sample through every consumer that exists (its own regex set, `windows_check.py`, `step0_pc_tests.ps1`, `run_checks_pc.ps1`) and exits 1 on any disagreement; a consumer that has not landed is `SKIPPED: not landed`.
9. **Theme guard** (`public_lint.py --theme`): keyword scan of *new theme-bearing files only* (`pipeline/scenes/`, `pipeline/phone/test_strings.json`, `ops/GATHER.md`, `skills-staging/`) for D-28 exclusions (Mughal, Islamic, mosque, minaret, Taj Mahal, Red Fort, church, cathedral, crucifix, nativity, Christmas, with word boundaries so "crossfade" and "across" never match). It cannot judge iconography; it says so in its output and in the README. Existing playbooks and research are reported INFO-only.

**Acceptance tests**
```bash
python3 -I tests/hygiene/test_patterns.py                # the pattern file is internally consistent (item 1); exit 0
bash tests/hygiene/run_tests.sh --all                    # guard tests, stale tests, lint tests (--quick: pattern test, guard tests and self-tests only)
python3 -I scripts/stale_check.py --self-test            # every pattern has >=1 positive and >=1 negative sample and they behave
python3 -I scripts/stale_check.py --audit-allowlist      # no dead allowlist entries
python3 -I scripts/stale_check.py --json build/evidence/wp03/stale_check_report.json --md build/evidence/wp03/stale_check_report.md ; echo $?   # 1 expected; report lists every Table 4 row
python3 -I scripts/stale_check.py --baseline && python3 -I scripts/stale_check.py --new-only   # exit 0 straight after the baseline
python3 -I scripts/public_lint.py --self-test            # no disagreement between consumers (skips only for consumers that have not landed)
```
- **Guard tests (nudge 2):** two `lj_with_disk` jobs started together: the second waits and then runs, and the ledger shows them one after the other; with `LJ_LOCK_WAIT_S=2` the waiter exits 3 `BUSY: held by <label>`; with a fake `df` reporting 700 MB, `lj_with_disk 350` runs and `lj_with_disk 320` exits 3 with the exact figures (`Avail - planned` below 400); with a fake `df` that falls below 250 MB mid-run, a sleeping child is terminated, its cleanup trap runs, and the exit is 3 `DISK-FLOOR`; `lj_bench` inside `lj_with_disk` works and the reverse order is refused with a message; the ledger line carries no path or host.
- **Pattern file:** every required sample behaves (the version strings, the 64-hex hash, the documentation addresses and a splatting variable are not flagged; the 65-hex run, the profile paths, the outside-range IP and the handle in prose are).
- Planted-tree test (temp directory shaped like the repo): each stale string in a playbook-like file is found; the same strings in the allowlisted contexts are not; the same strings in `research/*.md` and `reviews/` are ignored; adding one new stale line makes `--new-only` exit 1 while old hits are ignored.
- Read-only proof: `git status --porcelain` and a hash of the scanned tree are identical before and after.
- `public_lint.py` flags each planted category (e-mail, outside-range IP, MAC, user path, token shape, GUID, handle, NUL, 2 MB blob, staged `.mov`, a file named `pc_report.json` outside the fixtures) and passes a clean tree and the synthetic fixtures; its own source and test fixtures build the bad strings from fragments so the file itself stays clean; a path under `/home/user/build-scratch/` is not flagged and a path under `/home/` with any other name is.
- Theme guard flags "Mughal garden" and "Christmas card" in a planted scene file and does not flag "crossfade".

---

### WP-04 Route A harness `render.mjs` and the test scene (SP2)

**Wave 1. Runs: container.** **Refs:** W-23, W-14, W-15, W-16, W-21, W-41, W-57, D-25, D-26, D-28, D-29; spike SP2.

**Owner paths:** `pipeline/bin/render.mjs`, `pipeline/bin/README-render.md`, `pipeline/scenes/testcard/**`, `pipeline/lib/libs.lock.json`, `pipeline/lib/fetch_libs.sh`, `pipeline/lib/licences/**`, `pipeline/phone/test_strings.json`, `spikes/sp2_route_a/**`, `tests/render/**`, `build/evidence/wp04/**`.

**Goal.** A deterministic, resumable, shardable harness: scenes expose `window.seekTo(t)`; frames are captured by stepping; PNG or a piped ffmpeg chain; 1920x1080 at 24 fps; BT.709 tagged. SP2 is judged by this package's tests.

**Deliverables**
1. `render.mjs`: starts from the R7 code in `research/agent-pipeline.md` and keeps its contract (`seekTo(t)` pure, `window.ready`, `document.fonts.ready`, shards `i/n`, resume by skipping existing frames written through `.tmp` plus rename, `--alpha`) and adds: `--fps` default 24; `--w/--h` default 1920/1080; `--seconds` or `--frames a:b`; `--dir` plus repeatable `--mount /urlpath=dir` (so scenes can load `vendor/` fonts and libraries); `--chain NAME` selecting a chain from `pipeline/lib/chains.json` (built-in H.264 default until then); `--concurrency N` pages; `--json report.json` (frames, seconds, fps, peak RSS, Chromium version, chain, hashes); `--max-seconds` soft cap (container foreground commands stop at 10 minutes: finish the current frame, write a resume hint, exit 0); `--fail-on-pageerror` (exit 2, no partial output file); `executablePath` from `PW_CHROMIUM` or `/opt/pw-browsers/chromium`; Chromium flags `--force-device-scale-factor=1 --hide-scrollbars --disable-lcd-text --font-render-hinting=none` plus the SwiftShader flags of R7; waits two `requestAnimationFrame`s before each screenshot. **Fixes F-09**: the static server resolves the requested path, rejects anything outside the allowed roots (404), binds `127.0.0.1` only. **Network off**: `page.route` aborts every request not to the local server and the run exits 2 naming the URL (scenes must be self-contained).
2. `pipeline/scenes/testcard/` (style-neutral, nothing from section 4.10 excluded): a title area; a grid with a frame counter drawn from `seekTo`; a moving bar (judder check); a 16-bit-looking fine-detail texture panel generated from a seeded LCG that **pushes in** by writing `style.transform = scale(...)` at full float precision from a cosine in-out ease (the GSAP-for-the-ease-only pattern of W-41); a three-patch colour strip (255,0,0 / 128,128,128 / 224,172,140); a caption area with a Latin line, one line for every other script that has strings in `pipeline/phone/test_strings.json` (day 1: Devanagari; the text is read from that file through `--mount /phone=pipeline/phone`, never typed into the scene) and a hairline pair. Query variants: `?push=transform` (default), `?push=layout` (animates width/height/left/top, the **negative control** that MO8 must fail), `?random=1` (uses `Math.random`, the determinism negative control), `?filter=1` (an SVG filter so the 100-pixel tolerance path is exercised), `?gsap=1` (the same ease through GSAP's paused timeline, `tl.time(t,false)`), `?throw=1` (page error), `?net=1` (requests an external URL).
3. `pipeline/lib/fetch_libs.sh` + `libs.lock.json`: pinned versions and SHA-256 of `gsap` (dist file only; `3.15.0` is the planner's expectation and the version is **confirmed at fetch time** with `npm view`, the lock file recording what was actually fetched) and the test fonts from the `fontsource` npm font packages (OFL): Noto Sans, Kalam and the **Noto family for each script listed in `test_strings.json`** (nudge 4; day 1 Noto Sans Devanagari; Tamil, Telugu, Kannada, Malayalam, Bengali and Gujarati as `pending_O-10` entries whose package names are confirmed at fetch time, UNVERIFIED; adding one later is one more `npm pack`), fetched with `npm pack` into new empty folders, extracted with `tar`, single files copied into `vendor/js/` and `vendor/fonts/` (git-ignored); licence texts copied to `pipeline/lib/licences/`. GSAP is **not** committed (its licence is not OSI-approved; fetch on demand). If the npm registry is unreachable the script exits 3 with the exact error, and the scene runs without GSAP (`?gsap=1` marked SKIPPED).
4. `spikes/sp2_route_a/`: the SP2 driver, results and `VERDICT-SP2.md`.
5. `pipeline/phone/test_strings.json` (4.15), **delivered by Wed 21 Oct** so WP-08 and WP-02 can rely on it: the Latin entry, the Devanagari day-1 entries (digits and five plain Sanskrit-derived nouns, `checked_by_reader: false` until the maker confirms) with their `marks[]`, and empty `pending_O-10` blocks for the other six scripts. Any later script entry is a one-file follow-up for the same owner, not a new package.

**Acceptance tests** (`bash tests/render/run_tests.sh --all`; timed ones under `lj_bench`, anything writing over 100 MB under `lj_with_disk`, 4.9)
```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
bash pipeline/lib/fetch_libs.sh                                   # exit 0 (or 3 with the exact npm error)
node pipeline/bin/render.mjs --dir pipeline --page scenes/testcard/scene.html --mount /vendor=vendor --out renders/wp04/a --seconds 2 --json renders/wp04/a.json
```
- **A1 determinism:** two separate processes, frames 0-47, `?filter` off: identical SHA-256 per frame; with `?filter=1`: at most 100 differing pixels per frame (`compare -metric AE -fuzz 1%`).
- **A2 negative control:** `?random=1` frames differ by more than 100 pixels, so the harness's own determinism test provably catches a nondeterministic scene.
- **A3 sharding and resume:** shards `0/2` + `1/2` equal a single run frame for frame (hash-identical); a second invocation renders 0 frames.
- **A4 kill and resume (SP2 g):** SIGKILL a 240-frame run at about 50%; rerun completes; no `.tmp` files; final 240 frames; hashes equal an uninterrupted run.
- **A5 chain output:** `--chain h264` writes 48 frames; `ffprobe`: 1920x1080, `r_frame_rate` 24/1, `nb_frames` 48, `yuv420p`, `tv`, and `bt709` for matrix, primaries and transfer. (WP-11b repeats this with `spec_check.py`.)
- **A6 speed marks (SP2 a, e, f):** flat scene at least 8 fps (R11 pass mark; actual recorded); 1, 2 and 4 concurrent pages timed; a 2,400-frame (100 s) run piped straight into ffmpeg completes without accumulating PNGs (disk delta equals the output size, not the frame count); peak RSS recorded. That run is one `lj_with_disk 250` stage.
- **A7 fonts, per script (SP2 d; nudge 4):** for **every script in `test_strings.json` that has strings** (day 1: Latin and Devanagari), `document.fonts.check` is true for that script's Noto family (named in `libs.lock.json`), and each string is rendered twice, with the font loaded and with it blocked. The test requires (a) the IoU of the two ink masks at most 0.8, so a font that silently failed to apply is caught, and (b) a loaded-render ink-pixel count of at least 0.5 times that of a Pillow-raqm reference rendering of the same string at the same size, so a missing-glyph box is caught. **N is not a fixed number: it comes from the blocked-font baseline measured in the same run** (the blocked render's ink count and mask are recorded in the evidence with both thresholds, marked (J)). A script with no strings is listed `NOT TESTED`, never passed. Negative control: a Devanagari string set in the Latin-only family must fail (a).
- **A8 errors:** `?throw=1` exits 2 and leaves no partial output; `?net=1` exits 2 naming the blocked URL.
- **A9 path safety:** requests for `/../package.json` and `/%2e%2e/...` return 404.
- **A10 alpha:** `--alpha` frames report an alpha channel (`identify -format '%[channels]'`).
- **A11 MO8 pair (needs WP-05; skipped until it lands, run by WP-11b):** `?push=transform` passes the MO8 gate, `?push=layout` fails it.

**SP2 subset, justified.** (a), (d), (e), (f), (g) as specified; (b) rough.js is replaced by the seeded-LCG texture panel (rough.js is a style choice for G1 and adds nothing to a harness test); **(c) the three.js voxel diorama is dropped**: it existed to compare a voxel kitchen across renderers, and D-29 removed voxel work; the kitchen is a Blender set. A WebGL/SwiftShader smoke (one CSS 3D-transformed plane) replaces it and is recorded with its fps. If hero shots later need three.js, SP2 (c) is re-opened then.

---

### WP-05 Validators: spec check, colour-patch, MO8 gate (SP5, media half)

**Wave 1. Runs: container** (the PC run of the same tools is WP-09). **Refs:** W-14, W-15, W-16, W-17, W-19, W-20, W-41, D-27, S-01, S-28; spike SP5.

**Owner paths:** `pipeline/validators/**`, `pipeline/lib/chains.json`, `pipeline/settings.json`, `tests/validators/**`, `build/evidence/wp05/**`.

**Deliverables**
1. `pipeline/lib/chains.json` and `pipeline/settings.json` (4.5, 4.6).
2. `pipeline/validators/spec_check.py` (standard library): `ffprobe -show_entries` JSON; checks per profile: codec and profile; `pix_fmt`; 1920x1080; `r_frame_rate` equals `avg_frame_rate` equals 24/1; `nb_frames` equals `round(duration x 24)`; colour tags (H.264: all four of `color_range=tv`, `color_space`, `color_primaries`, `color_transfer` bt709; ProRes: range `unknown` is accepted with a note, as measured on 6.1.1); audio (48000 Hz; master PCM s24le with 24 bits; delivery AAC-LC stereo); **loudness** via `ffmpeg -nostats -i F -af ebur128=peak=true -f null -` (true peak at or below -1 dBTP everywhere, W-19; integrated within +-1 LU of the profile target, online -16); integrity (`ffmpeg -v error -i F -f null -` prints nothing; MP4 has `moov` before `mdat` for faststart); neutral metadata (no tags except an `encoder` tag). Profiles loaded from `pipeline/settings.json` plus `--profiles-file` (WP-08 supplies the phone profile). Output: one JSON document with a check list and a verdict; text summary on stdout.
3. `pipeline/validators/colour_patch.py` (standard library): builds the three-patch frame (255,0,0 / 128,128,128 / 224,172,140) as raw `rgb24`, encodes 2 frames through a named chain (`--chain NAME --chain-file F`, or `--all`, or the bare `-pix_fmt` and format-first chains as built-in **negative controls**), decodes back with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`, reports the worst per-channel error out of 255 per patch, passes at 3 or less (W-16). Runs identically on the PC with `--ffmpeg C:\...\ffmpeg.exe`. Records ffmpeg version line, configure flags and `sha256` of the binary (public file, not identifying), but no path. This **raw** JSON is what the maker reads and pastes in chat; it is never filed (4.4).
4. `pipeline/validators/mo8_gate.py`: wrapper around the reused `research/cinematic-quality-fixtures/mo8_audit.py` (called in place with `python3 -I`, never copied): runs it on a frame folder or a clip of at most about 96 frames (RAM), reads `mo8a_d4_px` and `mo8b_d4_px` (the fourth-difference estimators W-41 names), gates at 0.05 px and 0.04 px, reports roughness as informational only, and states that the gate applies to the **master before the delivery encode** (so it prefers `ffv1_lossless` or `prores422hq_master` clips or PNG folders).
5. Planted-defect generator in `tests/validators/` (SP5 media half) and good fixtures, all generated at test time under `renders/wp05/`.
6. `colour_patch.py --derive-from RAW --out DERIVED`: reads a raw `colour_patch_pc.json` (container-side, from a scratch file) and writes the filed form of 4.16 (`lj-pc-chains/1`: ffmpeg version, binary SHA-256, chain names, worst errors, pass flags; **no configure flags, no paths**).

**Acceptance tests** (`bash tests/validators/run_tests.sh --all`; the test renders run as one `lj_with_disk 150` stage, 4.9)
```bash
python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json build/evidence/wp05/colour_patch_ffmpeg-6.1.1.json
```
- **Regression oracle (container ffmpeg 6.1.1; numbers from Q-F1, tolerance +-1):** H.264 chain B (scale first) error about 1 and PASS; format-first chain A about 5 and FAIL; bare `-pix_fmt yuv420p` about 23 and FAIL (BT.601 under BT.709 tags, which `spec_check.py` must **not** catch, proving both tools are needed); ProRes 4444 bare about 25 and FAIL; ProRes 4444 chain about 0 and PASS. Any difference larger than 1 is recorded as a finding, not a failure of the package.
- **New measurement (F-12):** the `prores422hq_master` chain and the `h264_venue`, `h264_backup_main40` and `h264_online` chains each get a worst-error number; a chain above 3 is not accepted into `chains.json` as `approved: true`.
- **Planted defects for `spec_check.py`** (each must exit 1 naming the failed check): `yuvj420p`; 25 fps; 1280x720; BT.601-matrix pixels under BT.709 tags (tags pass, colour-patch fails); ProRes 4444 profile without alpha; true peak above -1 dBTP (clipped tone); 44.1 kHz audio; 16-bit PCM under the master profile; a `title` metadata tag; a truncated MP4 (no `moov`); a frame count that disagrees with duration times 24.
- **No false positives:** at least six good files across the four profiles all exit 0.
- **MO8 gate:** a Pillow sub-pixel push passes (about 0.003 px per the round-2 report); an ffmpeg `zoompan` push fails (about 0.6 px); the gate refuses a clip over 120 frames with a clear message.
- **Derived form:** a raw JSON with a planted configure flag containing a profile path and a user name yields a derived file with neither, which validates against its schema and passes `public_lint.py`.
- `colour_patch.py` and `spec_check.py` pass a `--selftest` that needs only ffmpeg; both run under `python3 -I` with no third-party module.

**UNVERIFIED:** results on ffmpeg 9.0.2 (the winget build) until the maker runs WP-09's runner; ProRes tag behaviour on Windows builds.

---

### WP-06 Round-trip emitters and validators: ORA, SVG ids, OTIO (SP5, hand-off half)

**Wave 1. Runs: container.** **Refs:** W-06, D-11, D-12, W-22, S-01 (24 fps), spike SP5.

**Owner paths:** `pipeline/roundtrip/**`, `tests/roundtrip/**`, `build/evidence/wp06/**` (venv lives at `/home/user/build-scratch/venv-otio`, outside the repo).

**Deliverables**
1. **ORA.** `emit_ora_layers.py` (Pillow) builds a synthetic layered still whose layers are named by id with `L00_asfound` as the bottom layer (the layer is a generated test card, **not a photo**), 8-bit sRGB straight-alpha PNG layers, `mimetype` stored first, `stack.xml`, `mergedimage.png`. `validate_ora.py` implements the R8 rules (zip opens; `mimetype` first and stored; `stack.xml` parses; every `src` exists; layers inside the canvas; names unique and matching `^[A-Za-z][A-Za-z0-9._-]*$`; only supported attributes). The **reused** `research/craft-visual-fixtures/make_ora.py` is run unchanged (cwd in scratch, output to `renders/wp06/`) as the known-good reference, and `research/craft-visual-fixtures/at-layers.ora` is validated too.
2. **SVG.** `svg_rig.py` generates a synthetic rig (unique ids, `data-pivot`, `data-z`, `viewBox`, no class/style reliance). `svg_roundtrip.sh` pushes it through **Inkscape plain-SVG export** as the stand-in "touching tool" (the documented fallback in `playbooks/craft-visual.md`) and then runs the reused `research/craft-visual-fixtures/check_ids.py` unchanged. Planted defects: ids stripped (what default svgo does), an element changed kind, `data-pivot` dropped.
3. **OTIO.** `emit_otio.py` (standard library, writes JSON) turns the neutral spec `pipeline/roundtrip/spec/neutral_timeline.example.json` (24 fps, four conformed stills, 24-frame dissolves, markers, one audio cue, relative `target_url`, `metadata.filmcraft` with scale and position keyframes from the Ken Burns maths below) into `.otio`, rebased from the 25 fps R3 E2 template of `research/craft-motion.md`. `kb_scale.py` implements the fit/cover formulas (3600x2400 into 1080p: fit 45.0, cover 53.3; 2880x1620: 66.67 for both) with unit tests. `validate_otio.py` implements the R8 OTIO rules at JSON level (target exists, relative path, `source_range` inside `available_range`, rate 24, dissolve offsets fit inside neighbours, markers present, `metadata.filmcraft` keys known) and, if the venv exists, also loads the file with `opentimelineio==0.18.1`. `adapter_probe.sh` runs the reused `research/sources/format-round1/make_otio.py` **unchanged** in a scratch directory against a synthetic `timeline169.json` at 24 fps (the script reads that exact file name and writes absolute paths, which is why `emit_otio.py` exists) and records which of EDL, FCPXML, Kdenlive and MLT adapters work.
4. Fixtures are generated at test time (stills as JPEG or PNG under `renders/wp06/`, git-ignored).

**Acceptance tests** (`bash tests/roundtrip/run_tests.sh --all`)
```bash
lj_with_disk 60 wp06-venv -- bash -c 'python3 -m venv /home/user/build-scratch/venv-otio && /home/user/build-scratch/venv-otio/bin/pip install opentimelineio==0.18.1'   # 0.8 MB wheel, about 50 MB venv, persistent until cleanup_scratch.sh
python3 -I pipeline/roundtrip/emit_ora_layers.py renders/wp06/layers.ora && python3 -I pipeline/roundtrip/validate_ora.py renders/wp06/layers.ora     # exit 0
python3 -I pipeline/roundtrip/validate_ora.py research/craft-visual-fixtures/at-layers.ora                                                             # exit 0
bash pipeline/roundtrip/svg_roundtrip.sh                            # clean pass-through: check_ids exit 0; 3 planted defects: exit 1 each
python3 -I pipeline/roundtrip/emit_otio.py pipeline/roundtrip/spec/neutral_timeline.example.json renders/wp06/ch.otio
python3 -I pipeline/roundtrip/validate_otio.py renders/wp06/ch.otio --with-otio /home/user/build-scratch/venv-otio/bin/python     # exit 0
bash pipeline/roundtrip/adapter_probe.sh                            # exit 0; JSON lists which adapters worked
```
- Planted defects, each detected with a named reason: ORA with a missing layer PNG, a duplicate layer name, a layer outside the canvas, `mimetype` not first; SVG ids stripped; OTIO clip outside `available_range`, rate 25 instead of 24, missing media, dissolve longer than its neighbour, absolute `target_url`.
- Inkscape's actual treatment of `data-*` attributes is **recorded as a finding** (we do not know it); the acceptance criterion is that ids survive and the finding is written.
- `kb_scale.py` unit tests give 45.0, 53.3 and 66.67 to one decimal.

**UNVERIFIED:** whether PhotoCraft, VectorCraft or FilmCraft accept and preserve these files (WP-10 on Linux CLIs; the maker's Windows five-minute tests are the real evidence).

---

### WP-07 SP1a: release sums for every pin; FilmCraft and EffectCraft headless tests; the maker's Craft-zip guide

**Wave 1. Runs: container.** **Refs:** W-22, D-11, D-12, W-23, D-15; spike SP1 (T1, T2 and T4 here; T3 and the other three apps in WP-10; T5 and T6 not run).

**Owner paths:** `spikes/sp1_craft_cli/**`, `vendor/craft/**` (git-ignored), `tests/sp1/**`, `build/evidence/wp07/**`.

**Goal.** Decide, with measurements, whether the Craft CLIs are a container render engine or only a maker-side refinement tool (ROADMAP 5.2: "Craft CLIs: only if SP1 T2/T4 pass"); and give the maker a Craft-zip guide for Sat 24 Oct. **Each tarball is downloaded once in the whole fortnight** (ledger below); round 1 fetched PhotoCraft, VectorCraft and LightCraft here for T1 and again in WP-10 for the read-backs (about 317 MB twice), and that is gone (nudge 6).

**Deliverables**
1. `release_assets.json`: on **Tuesday 20 Oct** fetch **every pin's `SHA256SUMS.txt`** (a few KB each, by direct URL because the release page and API are 403, F-04): PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 and its fallback 0.8.0, EffectCraft 0.11.1. From them record, per pin, the Linux tarball name, size and SHA-256 and the **Windows portable zip name and SHA-256**; the tarballs of the apps other than FilmCraft and EffectCraft are *not* downloaded here. Where `research/craft-motion.md` R8 recorded an independent hash (FilmCraft 0.8.0 `b166877905ae...`, EffectCraft 0.11.1 `b9cb2ce68dd6...`) the listing's value is compared with it; a mismatch is a stop-and-report finding. For every other asset the hash comes from the same host as the file, so it proves integrity only, not origin; the file says so. SoundCraft is listed as "not pinned (D-12), not fetched".
2. `MAKER-CRAFT-ZIPS.md` (plain language, exact PowerShell lines, 5.1-safe): for Sat 24 Oct. Create `C:\lj\tools\`; download each portable zip from the release page; `Get-FileHash -Algorithm SHA256` against the table; unzip to `C:\lj\tools\<app>-<tag>\`; create `portable.txt` where R7 says; **never install the Launcher**; copy the fixtures (`at-layers.ora`, `at-rig.svg`, `faded-print-a.lcpreset`, `at-lightcraft-steps.jsonl`, `check_ids.py`) into `C:\lj\at\`; pointers to the exact five-minute steps already in `playbooks/craft-visual.md` and `playbooks/craft-motion.md` (not copied); what to write down (version, signed or not, pass or fail, RAM seen); a line saying pins are the W-22 versions unless the orchestrator names a newer tag; "if a window flashes and closes, the three graphics fallbacks in R7"; and **a read-only "where did it write" step after each app's test** (new, for WP-01b): one pasted line that lists, with the profile path replaced by `%USERPROFILE%`, the folders under `%APPDATA%` and `%LOCALAPPDATA%` changed in the last hour, and a second that lists files under the app's own folder changed in the last hour. Both are read-only, 5.1-safe (parse-tested) and print only generalised paths, so the output is safe to paste.
3. `run_sp1.sh` and `drivers/*.py`: staged and idempotent, **one app at a time and only FilmCraft then EffectCraft**: each stage is `lj_with_disk <planned> <label> -- ...` (4.9) containing `curl` into a new empty folder, SHA-256 check, `tar` extraction into the same folder, the tests, and cleanup. **Profile chosen from live Avail:** `--profile full` (about 600 MB peak) only if Avail minus planned stays above 400 MB, else `--profile lean` (about 350 MB: low-entropy JPEG stills, a tree extracted from only the members the CLI needs, ProRes limited to 1 second), else exit 3 naming the shortfall and Q-1. The lean profile changes sizes and durations, never a pass criterion. FilmCraft 0.8.0 (fallback) is fetched only if 0.9.0 fails T1 or T2. **FilmCraft's verified tarball is kept** in `vendor/craft/_keep/` for WP-10's T3 when the keep-tarball rule of 4.9 allows (Avail after cleanup at least 700 MB); EffectCraft's is deleted with its tree.
4. **Blocked-download proof path:** any `curl` failure writes `blocked_proof.json` (URL, HTTP status, curl exit code, curl's stderr verbatim, proxy status line without credentials, time) and the run stops with exit 3. The fallback it proposes is written in advance in `spikes/sp1_craft_cli/FALLBACK.md`: SP1 becomes maker-PC evidence only (the Sat 24 Oct five-minute tests); the container renders with ffmpeg, Pillow and Chromium; Craft CLIs are not used in the container; ROADMAP 5.2 stays as the table says.
5. `VERDICT-SP1A.md`: T1, T2 and T4 table and the R8 decision rule applied; T3 "done in WP-10"; **T5 "not run: SoundCraft is unpinned and learning-only (D-12); no decision depends on it"** (nudge 7); T6 "not run: the web zips are not pins".

**Download ledger (each tarball once; total for the fortnight near 540 MB against the 2 GB allowance; the allowance became 2,560 MB on Tue 20 Oct 2026, see 4.9).**

| Asset | Size (bytes) | Fetched by | Times |
|---|---|---|---|
| FilmCraft 0.9.0 Linux tarball | 69,756,500 | WP-07 (kept for WP-10 T3 if disk allows, else WP-10 re-fetches once: recorded exception) | 1 (2 only on the exception) |
| EffectCraft 0.11.1 | 64,039,300 | WP-07 | 1 |
| PhotoCraft 0.10.0 | 83,037,328 | WP-10 | 1 |
| VectorCraft 0.13.1 | 124,613,940 | WP-10 | 1 |
| LightCraft 0.9.1 | 108,938,717 | WP-10 | 1 |
| FilmCraft 0.8.0 (fallback) | 69,692,976 | only if 0.9.0 fails T1 or T2 | 0 or 1 |
| SoundCraft 0.8.0 | 16,384,149 | nobody (T5 cut) | 0 |
| Six `SHA256SUMS.txt` | a few KB each | WP-07, Tue 20 Oct | 1 |
| PowerShell 7.5.4 | 75,396,784 | WP-01a | 1 |

**Test design (adaptations forced by disk, time and the project rate)**
- **T1 smoke:** per CLI `--version`, `commands | head`, `info --json` as in R8; exit code, stderr, time, `ldd` list; `VK_ICD_FILENAMES` unset.
- **T2 FilmCraft stills:** a Python driver **outside the vendor tree** calling `filmcraft-cli --project t2.fcproj --save exec ...` (parameter names confirmed with `filmcraft-cli describe <id>`, read from the local clone in F-06 for the command surface). Stills are generated as **low-entropy JPEG** (ImageMagick flat colour plus a numbered grid, so a 2880x1620 file is tens of KB; decode cost depends on pixels, not file size), N = 5, 20, 100 at 3600x2400 and 300 conformed at 2880x1620; PNG would not fit the disk. The H.264 export is **20 stills x 5 s at 24 fps = 2,400 frames** (R8 wrote 3,000 at 25 fps; pass mark scales to at least 5 fps, under 8 minutes); the ProRes 422 HQ export is limited to **3 seconds** (72 frames; 1 second in the lean profile) because a 3,000-frame ProRes file would be several GB. Checks as R8: no crash at N=100 and N=300, RSS slope per still under 40 MB, RSS at N=300 under 12 GB (a driver-side **watchdog polling `/proc/<pid>/status` kills the process at 10 GB**, `ulimit -v` is not used because wgpu maps large address ranges), `ffprobe` frame count equals expected, `ffmpeg -v error -i out.mov -f null -` is silent, first/last Ken Burns positions on a gridded still within 1 px, mid-dissolve pixel within 2 levels, `offlineMedia: []`. Under `lj_bench`.
- **T4 EffectCraft:** title comp, SVG line-draw and a 5-layer parallax comp at 1080p24, `RAYON_NUM_THREADS=1`, PNG RGBA, ProRes 4444 (3 seconds) and H.264; `ffprobe` pix_fmt and colour tags (issue #340); determinism on two runs; the OOM-killed H.264 `moov` observation only if it can be done without risking the session. Under `lj_bench`.
- All Craft binaries run via `env -i HOME=<throwaway> PATH=/usr/bin:/bin`, `cwd` in scratch, `timeout`, and `unshare -rn` when available (recorded). No Craft binary ever reads anything but synthetic files.

**Acceptance tests** (`bash tests/sp1/run_tests.sh --all` runs the lines below; `--quick` runs only `--list`, the fake-`df` line and `check_guide.py`, with no downloads)
```bash
bash spikes/sp1_craft_cli/run_sp1.sh --list                         # prints planned downloads, sizes, current df, the profile it would choose, and refuses (exit 3) if Avail minus planned is below 400 MB
bash spikes/sp1_craft_cli/run_sp1.sh --sums-only                    # Tue 20 Oct: all six SHA256SUMS.txt fetched; release_assets.json written; the R8 independent hashes compared
bash spikes/sp1_craft_cli/run_sp1.sh --only effectcraft v0.11.1 --t1-only    # sha256 equals the R8 table; T1 JSON written; tarball and tree deleted; df back within 10 MB of start
bash spikes/sp1_craft_cli/run_sp1.sh --all                          # full staged run (hours; background; disk and bench locks)
FORCE_BAD_ASSET=1 bash spikes/sp1_craft_cli/run_sp1.sh --only filmcraft v0.9.0   # 404 on a deliberately wrong asset name -> blocked_proof.json with the exact status and curl stderr; exit 3
LJ_DF_CMD=spikes/sp1_craft_cli/tests/fake_df_900.sh bash spikes/sp1_craft_cli/run_sp1.sh --list    # a fake 900 MB Avail: the full profile is refused and the lean one chosen; at 600 MB both are refused with the exact message
python3 -I spikes/sp1_craft_cli/check_guide.py                      # MAKER-CRAFT-ZIPS.md: every PowerShell fence parses (pwsh from WP-01a if present), every asset name and hash matches release_assets.json, the where-did-it-write lines print only %USERPROFILE%-form paths
```
- A deliberately corrupted tarball (one byte flipped in a copy) is rejected before extraction.
- After `--all`, `vendor/craft/` holds only `_keep/` (or nothing), `df` is within 10 MB of its start plus the kept 70 MB, and no envelope shows `avail_mb_min` under 250.
- `VERDICT-SP1A.md` states pass/fail per test and the decision rule outcome ("agents may render drafts with the Craft CLIs in the container" only if T2 and T4 pass; otherwise FilmCraft stays maker-side and the container renders with ffmpeg and code). A Linux CLI pass **proves nothing about Windows** and the verdict says so.

---

### WP-08 Phone deliverable: encode profile, legibility and fill-crop check, maker phone test (D-27)

**Wave 2. Runs: both** (checks in the container; the maker looks at the file on a real phone). **Refs:** D-27, D-28, D-15, W-17, W-18, W-19, W-21, W-57; `reviews/04-hindu-mobile-briefs-review.md` Part 0.2.

**Owner paths:** `pipeline/phone/profile.json`, `pipeline/phone/thresholds.json`, `pipeline/phone/phone_check.py`, `pipeline/phone/encode_phone.sh`, `pipeline/phone/encode_phone.py`, `pipeline/phone/sim_share.sh`, `pipeline/phone/PHONE-TEST.md`, `pipeline/phone/PHONE-ROW.md`, `skills-staging/phone-delivery/**`, `tests/phone/**`, `build/evidence/wp08/**`. (`pipeline/phone/test_strings.json` is WP-04's frozen file, 4.15; this package reads it and never edits it.)

**Goal.** A phone file made *from the same master* that plays beautifully on a phone and still reads when shared **and when the phone crops it to fill the screen**, with a measurable legibility check of text and captions at phone size in every script the film may use. Nothing in the playbooks covers the phone yet (searched), so this package also proposes the one skill that does.

**Deliverables**
1. `profile.json` (the 4.5/4.6 shape), proposals marked (J): `phone_1080` (1920x1080, 24 fps, H.264 High 4.0, `yuv420p`, BT.709 tv, CRF 20, `-maxrate 8M -bufsize 16M`, AAC-LC 48 kHz stereo 192 kbps, `-movflags +faststart`, metadata stripped, -16 LUFS / -1 dBTP as the online copy of W-19) and `phone_720_share` (1280x720, about 3.5 Mbps) for slow links. Captions are burned in at a **phone caption style** bigger than the venue's `FontSize=23` (candidate sizes measured, not guessed), at most about 32 characters a line, two lines, **and placed so the caption box ends at or above 88% of picture height** (the `fill_20x9` limit below), which is higher than the venue file's 5% margin. The file stays 16:9 (no reframing or cropping of the film for portrait).
2. `encode_phone.sh` / `encode_phone.py` (standard library plus ffmpeg): master (or any clip) + SRT/ASS -> phone MP4 through the chain, with `fontsdir=` and **relative file names with `cwd` set** so a Windows drive-letter colon never reaches the `subtitles=` filter (the caption_xheight round-2 lesson). Encodes run inside `lj_with_disk 100`.
3. `phone_check.py`: legibility check on a decoded frame set or file. **Scenarios:** `portrait` (held upright, 390 CSS px wide, device pixel ratio 3), `landscape` (844 CSS px wide), `small_portrait` (360 CSS px), `shared` (re-encoded to 480p at about 1 Mbps with `veryfast` to imitate a messenger) and, new (nudge 5), **`fill_20x9`**: the 16:9 picture shown on a 20:9 phone in landscape with the player set to fill or zoom, which scales the picture to the screen width, so it is 11.25 units tall on a 9-unit screen and **about 10% of the picture height is cropped at the top and again at the bottom** (`reviews/04` Part 0.2; `--aspect 19.5:9` gives about 9%). A caption at the venue file's 5% margin therefore loses its lower half. **Metrics per scenario:** caption x-height and cap height in physical pixels, millimetres and arcminutes at an assumed 35 cm distance; minimum stroke width in pixels (hairlines and the Devanagari headline); contrast ratio of fill against outline/backing (WCAG formula); caption box inside the 90% box; title text at least 5% of picture height (ROADMAP 6); and **caption position**: the bottom (and top) of the caption box as a percentage of picture height, compared with the scenario's crop line (`fill_20x9`: bottom must be at or above 88%, a 2-point margin inside the 90% crop line, (J) in `thresholds.json`). **Per script, for every script in `test_strings.json` that has strings** (day 1: Latin and Devanagari; the others are `NOT TESTED` until the maker's script is named, never a pass): the burned line is rendered, the **mark-survival check reads that script's mark positions from the same file** (`marks[]`, each with its `kind` and codepoints, 4.15) and derives each mark's zone by differential rendering with and without the mark's codepoints at 8x scale (no zone coordinate is stored or assumed, because Tamil, Telugu, Kannada, Malayalam, Bengali and Gujarati differ in where marks sit and how they stack), then requires at least 2 px of ink in that zone after the downscale to each scenario; and the **libass versus Pillow-raqm IoU test** (below) runs for each such script. Thresholds live in `thresholds.json` with a `source` and an explicit `(J)` where it is the planner's proposal; the arcminute minimum is **UNVERIFIED** (the planner recalls the ISO 9241-3 range of roughly 16 to 22 arcminutes for character height but did not re-read it) and the viewport table is an assumption about typical phones.
   **Findings, not predictions (nudge 5).** The expected outcome ("the venue caption size reads in landscape and fails in portrait") is a *finding the tool writes*, not something its self-test asserts: `phone_check.py --finding-fs23` writes `build/evidence/wp08/finding_fontsize23.json` with the `FontSize=23` verdict per scenario (including `fill_20x9` position) and the measured values, **whichever way it comes out**, and exits 0 either way.
4. `sim_share.sh`: the recompression simulation; never overwrites its input (hash checked).
5. `PHONE-TEST.md` (plain language): copy the test file to the phone by cable, AirDrop-style local transfer or any route (the test file has no personal content); watch in portrait and landscape at arm's length, **and once with the player set to fill/zoom**; seven questions (the six round-1 questions plus "when you zoom to fill, is the bottom line still whole?") with a yes/no/notes table; the maker answers in chat and the orchestrator records it in `ops/decisions.csv`. For the real film: cable or a private link only, never a service that keeps a copy without the maker's say (D-15).
6. `PHONE-ROW.md`: the final text of the settings card's phone row (WP-02 item 4) with the measured caption **size and position** (percent of picture height, and the `fill_20x9` verdict), and a **language/script note** that the orchestrator pastes into the card: `Scripts tested: <script> (neutral strings) on <date>; NOT TESTED: <the rest> (name the maker's script, O-10)`, so the card records which script was tested and when (nudge 4, W-57).
7. `skills-staging/phone-delivery/SKILL.md` + `CHANGES.md`: when to run the phone encode and check, exact commands, thresholds and their status, the rule that the phone file derives from the master and never replaces the venue file, the fill-crop rule, the per-script rule, the neutral-file-name and metadata rules, what to say when a check fails.

**Acceptance tests** (`bash tests/phone/run_tests.sh --all`; test frames rendered with WP-04, files validated with WP-05)
```bash
python3 -I pipeline/phone/phone_check.py --selftest                 # mechanisms only, see below; exit 0
python3 -I pipeline/phone/phone_check.py --finding-fs23 --out build/evidence/wp08/finding_fontsize23.json   # exit 0 whichever way each scenario comes out
bash pipeline/phone/encode_phone.sh renders/wp08/master10s.mov renders/wp08/caps.srt renders/wp08/phone.mp4
python3 -I pipeline/validators/spec_check.py renders/wp08/phone.mp4 --profiles-file pipeline/phone/profile.json --profile phone_1080   # exit 0
python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080   # worst error 3 or less
bash pipeline/phone/sim_share.sh renders/wp08/phone.mp4 renders/wp08/shared.mp4 && python3 -I pipeline/phone/phone_check.py renders/wp08/shared.mp4   # verdict recorded either way; input hash unchanged
python3 -I pipeline/phone/phone_check.py renders/wp08/phone.mp4 --scenario fill_20x9    # caption bottom reported as a percentage; the phone caption style passes, a clip burned with the venue margin fails
```
- **`--selftest` asserts mechanisms only (nudge 5):** a synthetic caption with a known-tiny x-height fails `portrait`; a synthetic caption at least twice the threshold passes `portrait`; a 1-px hairline frame fails `shared`; a caption box ending at 95% of picture height (the 5% margin) **fails `fill_20x9`** and one ending at 85% passes; a string whose mark codepoints are deleted fails the mark-survival check (negative control); a script whose `strings` is empty is reported `NOT TESTED`, never `PASS`. It makes no assertion about `FontSize=23`.
- **Per-script IoU (nudge 4):** for every script with strings, the burned line's ink matches a Pillow-raqm reference rendering (IoU of ink pixels at least 0.9), or the mismatch is reported as a shaping finding for that script; the evidence lists the scripts tested and the date in `scripts_tested.json`, which `PHONE-ROW.md` quotes.
- Bitrate cap: the produced file's average bitrate is at most the profile cap plus 10%.
- `pipeline/phone/test_strings.json` is a fixed allowlist: a lint test fails if any other Latin-or-Indic test string appears in `tests/phone/` or `pipeline/phone/` (section 4.10), and fails if a script block has strings but no `marks[]` key.
- `faststart`: `moov` precedes `mdat`.

**UNVERIFIED:** real phones' behaviour, messenger transcode rules (no service limits are asserted anywhere in this plan), how a given player implements fill or zoom (the 10% crop is arithmetic for a 20:9 screen, not a measurement of any app), the thresholds above, every viewport figure, and every non-Devanagari script (not tested until named).

---

### WP-09 Windows kit B: Ken Burns at 24, archive init, PC colour-patch runner

**Wave 2.** Parts 1 and 2 need only WP-01a's tools, so **the orchestrator may start WP-09 on Wed 21 Oct and put parts 1-2 into the Fri 23 Oct review bundle** (a named exception to the wave rule: the maker's Mon 26 and Tue 27 Oct exercises need them); parts 3 and 4 follow in the Wed 28 Oct bundle. **Runs: both.** **Refs:** W-06, W-14, W-16, W-27, W-41, W-22, W-25, D-13, D-15, D-26.

**Owner paths:** `win/kit2/**`, `tests/win_kit2/**`, `build/evidence/wp09/**`.

**Deliverables**
1. `kenburns_24.py` + `kenburns_24.ps1` (Ex 2 of `playbooks/toolchain.md`, P-LOCK must-pass): three moves (push-in, pan, a third) of about six seconds on three of the maker's own non-family stills, joined by one-second `xfade` dissolves, **1920x1080, 24 fps**, H.264 High yuv420p with BT.709 tags through the `h264_online` chain. The moves use the **Pillow sub-pixel box resize** method of `zoompan_vs_subpixel_prints.py` (`pil_resize_box`; imported if it has no import-time side effects, else ported with a citation) because `zoompan` is proof-only under W-41; an optional `--proof-zoompan` flag produces the ffmpeg `zoompan` version (`d=120` for 5 s, never 125) so the maker can see the difference. The reused `research/creator-threads-fixtures/kenburns_xfade.py` is square-only, which is why it is not the base. Round objects are not squashed (aspect-preserving crop to 16:9 first).
2. `archive_init.ps1` + `archive_verify.ps1` (Exercise 1 of `playbooks/ai-imagery.md`): creates the four-folder skeleton (names read from that playbook's Step 0, not invented) under a root the maker chooses (default `C:\lj\standin`, later the encrypted container), header-only `manifest.csv` and `steps.csv` with the columns the playbook defines, and `checksums.txt` via the **reused** `research/sources/format-round1/mk_manifest.ps1` / `verify_manifest.ps1` logic (called in place from the repo, LF endings, BOM-less). Stand-in ids use box code `ST`.
3. `run_checks_pc.ps1`: on the PC, runs `colour_patch.py --all` and `spec_check.py` against a clip it generates itself with the PC's ffmpeg. It **loads `scripts/redaction_patterns.json` (4.13) and fails closed**, self-scans its own output before writing, prints refusals as `category=`, `field=` and a masked hit, and offers `-PatternSelfTest SAMPLES.json`. It writes the **raw** `colour_patch_pc.json` (ffmpeg version line, configure flags, binary SHA-256, chain results) to `%TEMP%`, prints the path unexpanded, and prints a short paste block. **The maker reads the raw file and pastes it in chat only; it is never filed** (nudge 3). The orchestrator derives the filed form container-side with `colour_patch.py --derive-from RAW --out DERIVED` (WP-05, 4.16: version, sha256 and chain results, no configure flags, no paths) and files only that under `build/evidence/pc/`.
4. `README-KIT2.md`: plain-language, exact lines: install Python and ffmpeg with the winget ids from `playbooks/agent-pipeline.md` Step 2 (they are **UNVERIFIED**, never run on Windows), `py -3 -m pip install --user pillow numpy`, how to run for one session only (same three options as WP-01a's README), what each script prints and writes, and that the colour-patch file is pasted in chat and not saved into the project folder.

**Acceptance tests** (`bash tests/win_kit2/run_tests.sh --all`)
```bash
python3 -I win/tools/ps_lint.py win/kit2/*.ps1 && bash win/tools/ps_parse.sh      # tools from WP-01a
python3 -I win/kit2/kenburns_24.py --selftest --out renders/wp09/ex02.mp4
python3 -I pipeline/validators/spec_check.py renders/wp09/ex02.mp4 --profile online_h264     # 1920x1080, 24/1, yuv420p, tv, bt709 -> exit 0
python3 -I pipeline/validators/mo8_gate.py renders/wp09/ex02_push_only.mkv                  # sub-pixel push passes; the --proof-zoompan variant fails (documented)
/home/user/build-scratch/pwsh/pwsh -NoProfile -File win/kit2/archive_init.ps1 -Root renders/wp09/standin -Count 5   # skeleton + 5 synthetic stand-in files + checksums.txt
/home/user/build-scratch/pwsh/pwsh -NoProfile -File win/kit2/archive_verify.ps1 -Root renders/wp09/standin          # "checked 5 files, 0 problems"; after flipping one byte: MISMATCH names the file
/home/user/build-scratch/pwsh/pwsh -NoProfile -File win/kit2/run_checks_pc.ps1 -PatternSelfTest renders/wp09/samples.json   # agrees with the other consumers (public_lint --self-test)
```
- A circle drawn in a synthetic still measures an aspect ratio of 1.00 +- 0.01 in the output (Ex 2 "round object not squashed").
- `run_checks_pc.ps1` in test mode with a planted fake configure flag containing a profile path and a fake user name: it refuses with `category=` and a masked hit and writes nothing; with a clean fixture it writes the raw file to the given `-Out`, and `colour_patch.py --derive-from` produces a derived file with no configure flags that passes `public_lint.py`.
- Every `powershell` fence in `README-KIT2.md` parses; no stale 25 fps value in any new file; outputs pass `public_lint.py`. The kit tests write about 80 MB, under the 100 MB threshold, so they take no disk lock but still record `df` in their envelopes.

**UNVERIFIED:** all Windows behaviour, `py -3` launcher availability, Pillow wheels for the maker's Python, winget ids, the `%TEMP%` default on a managed PC.

---

### WP-10 SP1b: T1 and read-backs on PhotoCraft, VectorCraft and LightCraft; T3 on FilmCraft; SP3 prepared; SP4 armed; spike verdicts

**Wave 2. Runs: container.** **Refs:** W-22, W-23, D-12, D-15; spikes SP1 (T1 for three apps, T3), SP3, SP4.

**Owner paths:** `spikes/sp1b_readback/**`, `spikes/sp3_blender/**`, `spikes/sp4_idle/**`, `spikes/VERDICTS-W2.md`, `vendor/craft-sp1b/**` (git-ignored), `tests/spikes/**`, `build/evidence/wp10/**`.

**Deliverables**
1. **SP1b (T1 and the read-backs for the three visual apps; T3 for FilmCraft), Linux CLIs, one app at a time, each tarball downloaded here exactly once (nudge 6).** Each app is one `lj_with_disk` stage that does: `curl` into a new empty folder, SHA-256 against WP-07's `release_assets.json`, list the tarball (`tar -tvzf`) and compute the planned write, extract **only the members it needs**, run **T1 and the read-backs while the tree is on disk**, delete the tarball and the tree. If the guard refuses a stage (4.9: this package is the most exposed to the disk squeeze), the stage ends `BLOCKED` with the exact message and the remedy (answer Q-1, or move the read-back to the maker's PC); nothing is forced.
   - **PhotoCraft 0.10.0 (83 MB):** T1; `info <ora> --compact` and `convert` on the WP-06 ORA and on `at-layers.ora`, comparing layer names.
   - **VectorCraft 0.13.1 (125 MB):** T1; `convert` of the WP-06 rig and `at-rig.svg`, then the reused `check_ids.py`.
   - **LightCraft 0.9.1 (109 MB):** T1; `render` of a synthetic JPEG with `LIGHTCRAFT_GPU=0` and the `faded-print-a.lcpreset` import.
   - **FilmCraft 0.9.0, T3 interchange,** from the verified tarball WP-07 kept in `vendor/craft/_keep/` (SHA-256 re-checked; if WP-07 could not keep it, one re-fetch, recorded as a ledger exception): imports the WP-06 OTIO (plain and with `metadata.filmcraft`), `inspect sequence`, exports OTIO, FCP7 XML, FCPXML and EDL through `file.exportInterchange`, diffs the re-import, checks the motion keyframes survive only with the metadata (R8 T3 expectations), confirms relative media resolution, and checks the exported XML is well formed with `xmllint` (exporting FCP7 XML from FilmCraft is preferred over hand-writing it, `research/craft-motion.md` E3). The kept tarball is deleted afterwards (the one deliberate cross-package deletion: `_keep/` is a git-ignored hand-off folder, 4.9).
   - Every result is labelled **"Linux CLI result; not evidence for Windows"**.
2. **SP3 prepared, not run.** `spikes/sp3_blender/` holds `run_sp3.sh`, the entry conditions and the numbers: Blender is not installed, `pip install bpy==5.2.2` is a 402 MB wheel plus about 1 GB venv (R9/M14), the Blender tarball size is read by HEAD request, and the container has about 1.1 GB free. The reused research scripts (`followup2-s3-kitchen-standin.py`, `followup2-s3-run-sweep.sh` under `research/production-scale-fixtures/`) are syntax-checked (`py_compile`) and referenced, not copied. **Justified deferral:** SP3 runs in week 3 either on the maker's PC (`toolchain` Ex 5, Blender parallax timed with the Claude app closed) or in the container after at least 3.5 GB is free, and only on a **neutral** stand-in scene with no photograph (S3's own rule). The pass mark (one real hero frame within 2x the table) cannot be judged before the kitchen exists (G1).
3. **SP4 armed.** `spikes/sp4_idle/job.sh` (appends an epoch line every 10 s for 25 minutes to a file under the scratch folder), `gaps.py` (maximum gap, list of gaps over 30 s, verdict "kept awake / paused / killed"), `PROTOCOL.md` for the orchestrator (start the job, record `df`, leave the session idle at least 10 minutes with the tab closed, return, run `gaps.py`; the maker is asked only to close the tab for an evening). SP4 parts (d) cold versus cached setup timing, (e) the Gemini API key test and (f) a 50 MB git push are **not done**: (d) needs the disk, (e) is a third-party service call that needs the maker's recorded OK (D-15), (f) would bloat a public repo.
4. `spikes/VERDICTS-W2.md`: one row per SP1 to SP5 with status (Done / Partial / Deferred / Not run), evidence links, justification, next step and date. **The SP1 row lists T1 to T6 separately: T1 done for five apps; T2 and T4 from WP-07; T3 here; T5 "not run: learning-only app, no decision depends on it; re-open only if the maker asks to learn the app" (nudge 7); T6 "not run: the web builds are not pins".** SP2 and SP5 rows summarise WP-04, WP-05 and WP-06 evidence; the roadmap's decision rules are quoted, not reworded.

**Acceptance tests** (`bash tests/spikes/run_tests.sh --all`; `--quick` runs only the non-download lines)
```bash
bash spikes/sp1b_readback/run_sp1b.sh --list          # sizes from release_assets.json, df, the stage plan per app, and a refusal (exit 3) for any stage whose Avail minus planned is below 400 MB
bash spikes/sp1b_readback/run_sp1b.sh --all           # staged; each result JSON is labelled linux-cli; a refused stage is BLOCKED, not failed
python3 -I spikes/sp1b_readback/check_ledger.py       # each of the five tarballs was fetched once (from the disk ledger and the run logs); any exception is listed with its reason
bash spikes/sp3_blender/run_sp3.sh --check            # prints df, wheel size, tarball size by HEAD, "NOT RUN: needs >= 3.5 GB free", exit 3 on this container   [2026-10-20: the entry is now 1,900 MB after the measured peak of 1,408 MB, so the message reads "needs >= 1.9 GB free"]
python3 -m py_compile research/production-scale-fixtures/followup2-s3-kitchen-standin.py
bash spikes/sp4_idle/job.sh --seconds 60 --interval 2 && python3 -I spikes/sp4_idle/gaps.py <log>      # no gap > 5 s -> exit 0
python3 -I spikes/sp4_idle/gaps.py tests/spikes/fixtures/log_with_5min_gap.txt                        # planted gap detected -> exit 1
```
- After SP1b the `df` figure is within 10 MB of its start, `vendor/craft-sp1b/` is empty and `vendor/craft/_keep/` is gone; no envelope shows `avail_mb_min` under 250.
- `VERDICTS-W2.md` has five SP rows, the SP1 row has six T lines, and no row is without an evidence path.

---

### WP-11a Check-runner skeleton, `INDEX.md` writer and scratch cleanup

**Wave 1. Runs: container.** Small, light, and independent of every other package; it exists so that Fable's Fri 23 Oct review of wave 1 has `run_week2_checks.sh --quick` output attached (nudge 8: "WP-11 delivers the runner's skeleton in wave 1, even if it only runs the packages that exist"). **Refs:** W-06, W-26, W-29, D-26, D-30.

**Owner paths:** `scripts/run_week2_checks.sh`, `scripts/cleanup_scratch.sh`, `build/evidence/INDEX.md`, `build/evidence/week2_summary.json`, `build/evidence/wave1_quick.txt`, `tests/runner/**`, `build/evidence/wp11a/**`.

**Deliverables**
1. `scripts/run_week2_checks.sh` with `--list`, `--quick` (planned as under 5 minutes in total; measured 270 s on a fast container host and 374 s on a slower one, so the runner's quick budget is now 450 s, raised Tue 20 Oct 2026, a flag and not a failure; each area's `run_tests.sh --quick`, 60 s per-area timeout) and `--all`. It runs the test areas **sequentially, in a fixed dependency order listed in its header**: `hygiene` (WP-03), `win` (WP-01a), `ops` (WP-02), `validators` (WP-05), `render` (WP-04), `roundtrip` (WP-06), `sp1` (WP-07), `win_lj` (WP-01b), `win_kit2` (WP-09), `phone` (WP-08), `spikes` (WP-10), `runner` (WP-11a), `integration` (WP-11b). An area whose `tests/<area>/run_tests.sh` does not exist yet is `NOT LANDED` (listed, does not fail the run); a non-zero exit is `FAIL` (the runner exits 1); a hang past the timeout is `TIMEOUT` (also a FAIL). It collects exit codes and the evidence envelopes under `build/evidence/wpNN/` and writes `build/evidence/INDEX.md` (one row per package entry: counts of PASS, FAIL, UNVERIFIED, SKIPPED and BLOCKED, evidence paths, owner, and the **lowest `avail_mb_min`** seen in its envelopes, so the disk budget is visible), `build/evidence/week2_summary.json`, and, for `--quick`, `build/evidence/wave1_quick.txt` (the exact console output, the file attached to the Fri 23 Oct bundle). Its own output goes through `public_lint.py --text` once that exists.
2. `scripts/cleanup_scratch.sh`: `--dry-run` by default (lists what it would delete and the sizes); `--yes` deletes `<scratch>/pwsh`, the venvs, `vendor/craft*` and `renders/wp*`, then prints `df` before and after; it refuses to touch anything outside `<scratch>`, `vendor/` and `renders/`.
3. `tests/runner/`: fake areas (one passing, one failing, one missing, one that hangs, one whose output contains a planted e-mail-shaped string).

**Acceptance tests** (`bash tests/runner/run_tests.sh --all`)
```bash
bash scripts/run_week2_checks.sh --list              # prints the 13 areas in order and which have landed
bash scripts/run_week2_checks.sh --quick             # exit 0 when every landed area passes its --quick; wave1_quick.txt, INDEX.md and week2_summary.json written
bash scripts/cleanup_scratch.sh                      # dry run; deletes nothing (directory hash before/after)
```
- Against the fake areas: a failing area makes the runner exit 1 and `INDEX.md` shows FAIL; a missing area is `NOT LANDED` and exit stays 0; the hung area is killed and shown `TIMEOUT`; the planted e-mail-shaped string never reaches `wave1_quick.txt` unmasked; `INDEX.md` rows link evidence paths that exist.
- `cleanup_scratch.sh --yes` on a fake scratch tree removes only the listed items and refuses a root of `/` or `$HOME`.

---

### WP-11b Integration, evidence and P-LOCK readiness

**Wave 3. Runs: container.** **Refs:** W-06, W-26, W-29, D-26, D-27, D-30.

**Owner paths:** `tests/integration/**`, `build/evidence/P-LOCK-readiness-W2.md`, `build/evidence/pc/**` (derived PC evidence only, 4.16; the orchestrator files into it), `build/evidence/wp11b/**`, `pipeline/README.md`, `skills-staging/agent-first-production-pipeline/**`.

**Deliverables**
1. **Cross-package parity tests** in `tests/integration/`: `SETTINGS-CARD.md` values equal `pipeline/settings.json`, and the phone row equals `pipeline/phone/PHONE-ROW.md` and `profile.json`; `render.mjs`'s built-in chain equals `chains.json` `h264_venue` (or the documented chain it uses); `win/pins.json` equals `spikes/sp1_craft_cli/release_assets.json` versions equals the W-22 text; `ops/decisions.csv` equals `DECISIONS.md`; the `pc_report` fields `windows_check.py` reads exist in the schema; `lj.ps1 close` v0 calls the current script names (`stale_check.py --new-only`, `public_lint.py`) and defines no switch that deletes or commits; every script with strings in `test_strings.json` has a Noto family in `libs.lock.json`; the `Scripts tested:` line in `PHONE-ROW.md` equals `scripts_tested.json`.
2. **Redaction checks:** `python3 -I scripts/public_lint.py --self-test` with **zero skipped consumers** (all four present); no file in the repo outside `tests/win/fixtures/` matches the `path_denylist`; every file under `build/evidence/pc/` validates against its schema and contains none of the GPU, CPU or driver strings of the synthetic fixtures.
3. **Disk checks (nudge 2):** from the evidence envelopes, every stage with `planned_write_mb` above 100 satisfied `avail_mb_start - planned_write_mb >= 400` and `avail_mb_min >= 250`; WP-10's ledger check shows each tarball fetched once, with any exception listed; `df` after `cleanup_scratch.sh --yes` is reported.
4. **End-to-end:** WP-04's test scene rendered through `--chain` and checked by `spec_check.py`; WP-04 A11 (MO8 pair) run; the phone encode checked from a harness-rendered master, including `fill_20x9`.
5. **Hygiene on the whole build:** `stale_check.py --new-only` exit 0 (the build introduced no new stale value); `public_lint.py` clean over the full diff including the theme guard; no file over 1 MB; no binary; total new text under 9 MB (raised from 5 MB to 8 at gate review r1, Mon 19 Oct 2026: 13 packages of tests and evidence measured about 7 MB; raised to 9 on Tue 20 Oct 2026 at the week-2 close-out gate: measured 7.59 MB in 627 files, and the review rounds of weeks 3 and 4 will add more; if it reaches 8.5 MB, prune duplicate evidence first; raise it again only with a dated note); `git status` shows no ignored file staged.
6. `P-LOCK-readiness-W2.md`: the eight must-pass items and the other P-LOCK conditions, each with status `PASS (container)`, `UNVERIFIED (Windows)`, `maker-owed (with date)` or `not started (week 3-4)`; `lj.ps1 close` reads **"v0 dry-run done; v1 (apply, commit, backup, log) and its end-to-end run not started (week 4)"**, never PASS; the input for Fable's Sun 8 Nov mid-point check.
7. `pipeline/README.md` (one page: layout, how to run each tool, where evidence goes) and the staged update `skills-staging/agent-first-production-pipeline/SKILL.md` + `CHANGES.md` (points step 5-8 and the validators checklist at the real scripts; records the F-12 finding; the Windows `lj.ps1` commands that exist and what they do not do yet; the redaction rule in 4.13 and the raw-versus-derived rule in 4.4 and 4.16).

**Acceptance tests**
```bash
bash scripts/run_week2_checks.sh --quick               # exit 0, INDEX.md written
bash scripts/run_week2_checks.sh --all                 # exit 0 (or exact failing tests listed)
python3 -I scripts/stale_check.py --new-only           # exit 0
python3 -I scripts/public_lint.py                      # exit 0 (no flag: its default mode IS the diff against HEAD plus untracked files; there is no --diff option)
python3 -I scripts/public_lint.py --self-test          # exit 0 with no SKIPPED consumer
bash tests/integration/run_tests.sh --all              # the parity, redaction, disk and end-to-end tests above
```
- `INDEX.md` has one row for each of the thirteen entries (WP-01a to WP-11b) and every row links evidence that exists.
- `P-LOCK-readiness-W2.md` has no row without a status and no `PASS` for anything that needs Windows.

---

## 6. Waves, review dates and the critical path

| Day | Agents | The maker | Fable (4.14) |
|---|---|---|---|
| **Mon 19 Oct** | WP-03 delivers the pattern file and the guard first; WP-02 hours part, then `decisions.csv`; WP-01a (script, checker, tools); WP-11a; then WP-05, WP-06, WP-04 | Starts logging hours (WP-02's page) | - |
| **Tue 20 Oct** | WP-01a ready by 08:00; WP-07 fetches all `SHA256SUMS.txt`; WP-03 continues | Waits for the go, then runs the inventory and pastes the report in chat | **Reads WP-01a alone, morning** |
| Wed 21 Oct | WP-07 FilmCraft stage (disk is most open now); WP-03 first `stale_check.py` run; WP-09 early start (parts 1-2) | The week-1 own-material checklist (WP-02's `GATHER.md`) | - |
| Thu 22 Oct | WP-02 card and checklist; WP-11a done; WP-07 guide drafted; WP-04/05/06 finishing | - | - |
| **Fri 23 Oct** | Wave-1 bundle assembled with `run_week2_checks.sh --quick` output | Lab emails (not this plan) | **Reads wave 1 as one bundle** (plus WP-09 parts 1-2) |
| Sat 24 Oct | - | Craft zips, checksums, five-minute tests; pastes the "where did it write" lines | - |
| Sun 25 Oct | - | Pins frozen; week-1 facts answered (O-01 to O-13) | - |
| Mon 26 Oct | Wave 2 starts: WP-01b (with the Saturday paste), WP-08, WP-10; WP-07 T2/T4 results land | Ken Burns by script | - |
| Tue 27 Oct | WP-01b done | Archive and five stand-in scans | - |
| **Wed 28 Oct** | Wave-2 bundle assembled | Encrypted container (administrator account), separate Windows account | **Reads wave 2 as one bundle** (plus WP-07 results) |
| Thu 29 Oct | WP-09 parts 3-4 and the phone test file go to the maker; WP-11b starts | Colour-patch run on the PC; phone test | - |
| **Fri 30 Oct** | WP-11b done | Pilot tape ships (not this plan) | **Reads the readiness map and the final settings card** |
| Sat 31 Oct - Sun 1 Nov | - | Phone answers in chat; **signs the card Sun 1 Nov** | - |

Critical path for the maker: WP-02 (hours) -> WP-01a -> WP-07 guide -> WP-09 parts 1-2 -> WP-08 and WP-09 parts 3-4 -> the card. Critical path for P-LOCK evidence: WP-05 + WP-06 -> WP-10 -> WP-11b. Critical path for everything that writes: WP-03's guard (Mon 19). Buffer: the P-LOCK mid-point check is Sun 8 Nov, so slipping WP-08, WP-10 or WP-11b by three days costs nothing; slipping WP-01a, WP-02, WP-03's first two deliverables or WP-07's guide does.

---

## 7. Assumptions I made (orchestrator may veto)

- A-01 Layout in 4.1 (`win/`, `pipeline/`, `ops/`, `spikes/`, `scripts/`, `tests/`).
- A-02 The Windows tools folder is `C:\lj\tools\<app>-<tag>\` (see C-04).
- A-03 Thresholds in `win/tiers.json` and `pipeline/phone/thresholds.json` are proposals (J) with a `source` column; they can change without code edits.
- A-04 `lj.ps1 close` v0 is a dry run that cannot delete, commit or write; the real session close (apply, commit without push, backup, log) is v1 in week 4, and the real run is what satisfies W-26.
- A-05 GSAP is fetched, not committed; OFL fonts are fetched and hashed, not committed. The `gsap` pin (3.15.0 expected) is to be confirmed at fetch time (`libs.lock.json` records what was actually fetched and its hash); it is not a fact.
- A-06 `ops/decisions.csv` is generated from `DECISIONS.md`; the register stays the source of truth.
- A-07 No step in this plan needs a Windows run before Tue 20 Oct except the maker's own first inventory.
- A-08 Eleven packages are listed as thirteen schedulable entries because WP-01 and WP-11 each have two stages in different waves (the brief's "7-11 packages" is met by package count).
- A-09 Raw PC reports (`pc_report.json`, `colour_patch_pc.json`) are read by the maker and pasted in chat only; the repo holds derived tier files only (4.4, 4.16).
- A-10 Disk figures in this plan are a snapshot of a volume other jobs write to; `lj_guard.sh` reading `df` live is the authority, and the lean profiles exist so the plan survives a smaller number.
- A-11 Devanagari is the day-1 script **for tooling only**, because the plan can supply words for it today. It says nothing about her language (D-28, O-02, O-10); the settings card records which script was tested and when.

---

## 8. Conflicts and questions for the orchestrator (found while reading; none resolved here)

- **C-01 Two scripts named `windows_check.py`.** `research/cinematic-quality-fixtures/windows_check.py` is the measurement runner (caption x-height, zoom roughness, MO8, pan estimator) that writes `windows_check_report.json`, the file W-28 and ROADMAP risk 9 say must be in the repo before any Windows number is trusted. The script this brief asks for validates a PC *inventory* report and prints the hardware tier. Proposal: new file `scripts/windows_check.py` (inventory) and its report named `pc_report.json`; the old file keeps its name under `research/` and its report name; W-28 and the cinematic-quality skill keep meaning the old one. Decide whether to rename one.
- **C-02 Two `step0_pc_tests.ps1`.** The research version (`research/toolchain-fixtures/step0_pc_tests.ps1`) runs timed Blender/ffmpeg tests and writes a text report; the new one is read-only and writes JSON. `playbooks/toolchain.md` Step 0 still points at the old one. The timed tests move to a later optional kit (week 3: `toolchain` Ex 5).
- **C-03 Two things called `decisions.csv`.** `research/production-scale-fixtures/decisions.csv` is a gate-decision log; the brief wants an ID mirror. WP-02 creates `ops/decisions.csv` (mirror) and `ops/gate_log.csv` (the old schema). The animation-production-planning skill and ROADMAP risk 1 should say which.
- **C-04 Windows tools folder.** `playbooks/craft-motion.md` says `C:\LifeJourney\tools\`; `playbooks/craft-visual.md` says `C:\lj\...` and in places `C:\Program Files\PhotoCraft\...` (MSI), which D-12/W-22 forbid in favour of portable zips. This plan uses `C:\lj\tools\`. **Recommendation (Fable's note):** the orchestrator patches craft-motion's `C:\LifeJourney\tools\` through a Table 4 row so the inventory does not have to scan two roots forever. Until it does, `step0_pc_tests.ps1` scans both (WP-01a's fixtures include a Craft app found only under the second root), and removing the second root is a one-line follow-up.
- **C-05 Hours file has two audiences.** The planning skill reads the production-scale schema; the maker types into it. WP-02 keeps the schema and adds a plain how-to.
- **C-06 `ROADMAP.md` calls its own sections 7 and 8 the calendar and curriculum; the brief says "section 4-8".** I used the calendar (section 7) and curriculum (section 8).
- **C-07 Register inconsistencies.** D-14 still says the repository is private while D-26 (later) says public; D-23 is superseded by D-29. `ops/decisions.csv` will mark both. Not edited.
- **C-08 Calendar placeholders do not match D-28.** `ROADMAP.md`, `DECISIONS.md` (W-10) and some playbooks carry Hanukkah, Christmas, Ramadan, Ash Wednesday and Lunar New Year as generic holiday slots; the household is Hindu (the week 3 calendar row already says "Diwali this week if kept (unverified)"). `stale_check.py` reports them as INFO; replacing them waits for the family profile (O-10). Not edited.
- **C-09 `research/craft-motion.md` R3 template and `timeline.example.json` are 25 fps.** New code uses 24; WP-06 rebases the template.
- **C-10 Disk.** About 1.1 GB free (and falling while another job writes) is below the stated 2 GB download allowance (2,560 MB since Tue 20 Oct 2026) and well below what the first draft assumed. SP3 cannot run until disk is freed or SP3 moves to the PC. Levers (not touched): the pip cache 418 MB (Q-1), the huggingface cache 605 MB (keep, week 3).
- **C-11 Hardware facts versus a public repository.** The ai-photo skill reads `decisions/hardware.md` with the fields GPU, VRAM, RAM, free disk and Vulkan device, and `playbooks/agent-pipeline.md` Exercise 1 expects `maker-pc.json` in the repo. Under D-26 a raw inventory is a hardware fingerprint of one machine. This plan files **tier-level data only** (4.16); `windows_check.py --hardware-md` writes the bucketed draft. Decide whether the skill's field list is relaxed to buckets (the playbooks key on tiers, not models) or whether the exact figures stay on the maker's PC.
- **C-12 Provisional questions.** `reviews/04-hindu-mobile-briefs-review.md` Part 0.5 proposes O-36 to O-45 (script, lineage, deities, phone model, and so on). They are not in `DECISIONS.md` yet. This plan cites O-02 and O-10 as the sources of "her script" and treats the review's O-36 as provisional; when the orchestrator adds them, WP-02's `decisions_to_csv.py` picks them up from the register with no change.
- **C-13 `lj.ps1 close` "written and run once" (W-06, W-26).** ROADMAP week 1 lists `lj.ps1 close` v0 and P-LOCK requires it written and run once. This plan delivers v0 as a dry run (nudge 1) and the real thing in week 4; the readiness map says so instead of marking it passed.

---

## 9. Out of scope for weeks 1-2, and when it happens

| Item | Why not now | When / who |
|---|---|---|
| Source-type matrix (W-58) | researcher task | briefed week 2, due Sun 1 Nov (orchestrator) |
| Table 4 patches S-01, S-38, S-39, S-40; MO8 scribe pass | owner files are not Sonnet's; WP-03's report is the work order | Haiku before Fri 30 Oct / Sun 15 Nov |
| `r10_conform_footage` (W-59) | needs the footage test matrix | Fri 6 Nov (week 3) |
| `derive_album_look.py`, Whisper route, coverage strip, `venue.json`/`venue_calc.py` | week 3 rows | week 3 |
| `lint_template.py`, `edit_audit.py`, Lottie validator, manifest schema, `timeline-json-and-emitters` and the other two W-31 skills | weeks 3-4 | Sonnet/Haiku, before Sat 14 Nov |
| **`lj.ps1 close` v1** (`-Apply`, `-Commit`, `-IncludeWindowsRecent`, backup, push decision, log) and its real end-to-end run | needs the five-minute-test data, the encrypted drive and a backup target; destructive tooling only after the maker has seen the dry-run list | week 4 (ROADMAP row 4) |
| **SP1 T5 (SoundCraft) and T6 (web builds)** | D-12: SoundCraft is unpinned and learning-only; the web zips are not pins; no decision depends on either | re-open only if the maker asks to learn SoundCraft; recorded in `VERDICTS-W2.md` |
| Test strings and fonts for scripts other than Devanagari | the maker's script is not known until O-10 (Sun 25 Oct) | one follow-up task after O-10: a `libs.lock.json` entry (one `npm pack`), a `test_strings.json` block and a reader's check; the Sun 1 Nov card note shows what was tested |
| VeraCrypt container, separate Windows account, OneDrive off | admin rights, maker only | maker, Wed 28 Oct (README only mentions) |
| Ten-print scan pilot, album look, bake-off | weeks 3-4 | maker + Sonnet |
| SP3 run (Blender), SP4 execution, SP2 (c) three.js | disk / idle session / voxel dropped | section WP-10, WP-04 |
| Any style or look decision, any deity or temple imagery | style research is running in parallel; G1 is Sun 15 Nov | style track |

---

## 10. Risks and fallbacks

| # | Risk | Mitigation |
|---|---|---|
| R-1 | The Windows scripts fail on the maker's PC (5.1 quirks, Group Policy, CIM differences) | Conservative syntax lint, per-section try/catch, README lists six paste-in read-only commands as a fallback, first run is read-only so a failure costs nothing; Fable reads WP-01a before the maker does |
| R-2 | An identifying value reaches a committed file or a pasted report | One pattern source read by every scanner and a self-test that fails on disagreement (4.13); redaction by omission (4.4); a self-scan that refuses to write; the raw report stays on the PC and in chat (4.4); only derived tier files are filed; `public_lint.py` before every commit and a path denylist; local deny list on the PC |
| R-3 | Disk fills during SP1 and takes the session down | `lj_with_disk`: live `df`, "Avail minus planned stays above 400 MB", a 250 MB floor that aborts and cleans up, one writer at a time over 100 MB (4.9); lean profiles; each tarball downloaded once; delete after use; `df` in every envelope |
| R-4 | Timing results are contaminated by parallel work | One bench lock, load average recorded; results taken under load are marked `contaminated` |
| R-5 | Chromium frames differ between container and PC | Determinism claims are per environment; tolerance 100 px across environments |
| R-6 | Phone thresholds are my guesses | Marked (J) and UNVERIFIED; the maker's phone test and Fable's read decide; thresholds are data, not code; the FontSize-23 verdict is a finding, not a pass condition |
| R-7 | A Craft download is blocked or a hash mismatches | `blocked_proof.json`, stop-and-report on mismatch, written fallback (WP-07 item 4) |
| R-8 | Test content accidentally violates D-28/D-29 | Fixed string allowlist keyed by script, Sanskrit-derived neutral words, theme guard, nothing religious in tooling, Fable reads the first scene |
| R-9 | Many parallel packages tempt cross-edits | One owner per file, frozen interfaces (4.4 to 4.6, 4.13, 4.15, 4.16), parity tests in WP-11b |
| R-10 | The maker's attention is the bottleneck | Maker-facing drops are small, dated, and each has one page of plain instructions; destructive tooling is held back until week 4 |
| R-11 | **Another job keeps writing to the shared volume** (observed Mon 19 Oct) | Q-2; the guard's hard floor stops this plan's own stage; WP-07 and WP-10 degrade to lean profiles or end `BLOCKED` with the remedy rather than forcing; the pip-cache answer (Q-1) buys about 418 MB of headroom |
| R-12 | The inventory refuses to write on the maker's first day because of a harmless collision (short user name equal to a vendor name; a driver version shaped like an IP) | Hardware-name-field rule and version-field exemptions (4.13); the refusal names the category and prints a masked hit; the README says what to do; two fixtures for each case; the six paste-in commands as the last fallback |
| R-13 | The disk lock stalls other packages while a long stage runs | Stages are at most 60 minutes and never idle; waiters give up after 90 minutes with `BUSY: held by <label>`; fixed lock order disk then bench |

---

## 11. Revision log: how the Fable round-1 review was applied (Mon 19 Oct, same day)

Review: `reviews/build/plan-review-r1.md` (verdict REVISE, eight nudges, smaller notes). Nothing below changes the eleven packages; it splits two of them into stages, changes wave membership, adds the guard (4.9) and three frozen interfaces (4.13, 4.15, 4.16), and adds one rule about what PC data may be filed.

| Nudge | Where it landed | What changed |
|---|---|---|
| 1 Split WP-01; re-wave the destructive half | Section 1; WP-01a; WP-01b; 4.7; 4.13; section 9 | WP-01a (wave 1, read by Fable alone Tue morning) holds the inventory script, `windows_check.py`, tools, pins, schema, fixtures and the README. WP-01b (wave 2, after Sat 24 Oct) holds `lj.ps1` `doctor` and a **dry-run-only** `close`; `-Apply`, `-Commit`, `-IncludeWindowsRecent` do not exist until v1 in week 4 (A-04). The self-scan refusal names the category and prints the masked hit; the README has a "if the script refuses to write" section; fixture `report_short_username_collision` (and its leak twin) added; **a name hit inside a hardware-name field is reported, not refused** |
| 2 Disk as a mechanism | Section 0 (Q-1, Q-2), F-01, F-13, 4.2, 4.9, WP-03, WP-07, WP-10, WP-11b | `disk.lock` beside `bench.lock` in `scripts/lj_guard.sh` (WP-03); every write over 100 MB goes through `lj_with_disk`; the 2x rule is replaced by "Avail minus planned stays above 400 MB" plus a 250 MB abort floor; `df` figures are required in every evidence envelope and checked by WP-11b; **the pip-cache question is asked of the orchestrator in Q-1, with the answer marked PENDING and a default that still works** |
| 3 One redaction source | 4.13 (new), 4.4, 4.16 (new), WP-01a, WP-02, WP-03, WP-05, WP-09 | `scripts/redaction_patterns.json` (owner WP-03, first deliverable) with categories, the explicit 64-hex SHA-256 exemption and fragment-built positive and negative samples; `step0_pc_tests.ps1`, `run_checks_pc.ps1`, `windows_check.py` and `public_lint.py` read it, and `public_lint.py --self-test` fails on any disagreement; the raw `pc_report.json` and `colour_patch_pc.json` are read by the maker and pasted in chat only; only derived tier files are filed under `build/evidence/pc/`; `HOURS-HOWTO` says "no names in note" and `ops_lint.py` checks the `note` column |
| 4 Parameterise the script | 4.10, 4.15 (new), WP-04 (A7), WP-08, WP-02 (card), A-11 | `test_strings.json` is keyed by script with Devanagari as the day-1 entry (Sanskrit-derived neutral words); `libs.lock.json` names the Noto family per script; WP-08's mark-survival check reads per-script `marks[]` (zones derived by differential rendering, none assumed); WP-04 A7 and WP-08's IoU test loop over every listed script; A7's ink threshold comes from the blocked-font baseline; the card's language note records the script tested and the date |
| 5 WP-08: fill-crop scenario; findings not predictions | WP-08 | Scenario `fill_20x9` (about 10% of picture height cropped top and bottom), a caption-position metric with a (J) threshold at 88%, `PHONE-ROW.md` carries size **and** position; `--selftest` asserts mechanisms only (tiny fails, large passes, hairline fails `shared`, a 5%-margin caption fails `fill_20x9`); the FontSize-23 verdict is written to evidence as a finding |
| 6 Re-wave the Craft fetches | WP-07, WP-10, 4.9 | WP-07 runs FilmCraft and EffectCraft only (T1, T2, T4) and fetches every `SHA256SUMS.txt` on Tuesday; PhotoCraft, VectorCraft and LightCraft move wholly to WP-10 (T1 and read-backs while the tree is on disk); FilmCraft's tarball is kept for WP-10's T3 so no tarball is downloaded twice; a download ledger and a ledger check enforce it (about 317 MB saved) |
| 7 Cut SP1 T5 | Section 2, WP-07, WP-10, section 9 | SoundCraft is not fetched or run; `VERDICTS-W2.md` records "not run: learning-only app, no decision depends on it" |
| 8 Review at wave boundaries | 4.14 (new), section 6, WP-11a | Fable reads WP-01a alone Tue 20 Oct, wave 1 as one bundle Fri 23 Oct with `run_week2_checks.sh --quick` output attached (WP-11a delivers the runner skeleton in wave 1), wave 2 Wed 28 Oct, and the readiness map Fri 30 Oct; one named exception (WP-09 parts 1-2 join the Fri 23 Oct bundle) |

**Smaller notes.** C-04 now carries the recommendation to patch craft-motion's tools folder through Table 4 (section 8). `/home/user` is the generic placeholder and `/home/user/build-scratch` is the literal `<scratch>` (4.1, 4.13). The `gsap` version pin is confirmed at fetch time (A-05). The README tells the maker the VeraCrypt container is created from an administrator account and mounted from the project account (WP-01a). Section 4.10 is kept and extended. WP-02's card test stays a string-presence test (acceptable for a document). WP-04 A7's unset N is set from the blocked-font baseline.

*Round 2 of the review should take one short pass: the nudges change wave membership, the disk guard (4.9) and three interfaces (4.13, 4.15, 4.16), not the package list.*
