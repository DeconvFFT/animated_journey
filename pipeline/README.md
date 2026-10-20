# pipeline/: the production tools, weeks 1 and 2

This folder holds the tools that turn a scene made from code into a checked file: a seekable web scene is rendered frame by frame (Route A), encoded through a named
colour chain, checked against a delivery profile, and cut into the phone files. Everything here is built and tested on **synthetic, style-neutral test material**
(a test card, a tone, a geometric rig). No family media exists in the repo and none may be created or simulated. No style decision lives here: the look is the style
track's (G1). Nothing here has been run on Windows; where a tool also runs on the maker's PC it is marked UNVERIFIED until the maker's first run.
The map of what is proven and what is not, item by item, is `build/evidence/P-LOCK-readiness-W2.md`.

## Layout

| Path | What it is | Package |
|---|---|---|
| `pipeline/bin/render.mjs` | the Route A harness: headless Chromium steps `window.seekTo(t)`, PNG frames or a piped encode through `--chain`; sharded, resumable, network off. `pipeline/bin/README-render.md` | WP-04 |
| `pipeline/scenes/testcard/` | the style-neutral test card (grid, frame counter, moving bar, texture push, colour strip, caption area). Query variants are the negative controls | WP-04 |
| `pipeline/lib/chains.json` | the encode chains: `h264_venue`, `h264_backup_main40`, `h264_online`, `prores422hq_master`, `prores4444_alpha`, `ffv1_lossless`. The colour test, not the text, decides `approved` | WP-05 |
| `pipeline/lib/libs.lock.json`, `fetch_libs.sh`, `licences/` | pinned GSAP and OFL test fonts (one Noto family per script) fetched into the git-ignored `vendor/`; only the lock file and licence texts are committed | WP-04 |
| `pipeline/settings.json` | machine-readable mirror of `ops/SETTINGS-CARD.md`: picture, rate, colour, audio, captions, loudness and the delivery profiles | WP-05 |
| `pipeline/validators/` | `spec_check.py` (does the finished file meet its profile), `colour_patch.py` (do the pixels survive the chain, W-16), `mo8_gate.py` (is a slow push smooth, W-41). `README.md` | WP-05 |
| `pipeline/roundtrip/` | ORA, SVG-id and OTIO emitters and validators for the Craft hand-offs. `README.md` | WP-06 |
| `pipeline/phone/` | the phone files (D-27): `profile.json`, `encode_phone.sh`, `phone_check.py`, `sim_share.sh`, `PHONE-TEST.md`, `PHONE-ROW.md`; `test_strings.json` is the only test text allowed | WP-08 (strings WP-04) |

Related, outside this folder: `win/` (the PowerShell kit for the maker's PC), `scripts/` (repo checks and the redaction pattern file), `ops/` (hours, decisions mirror,
gather list, settings card), `spikes/` (SP1 to SP5), `tests/<area>/run_tests.sh` (one per package, each with `--quick` and `--all`).

## How to run each tool (repository root; Linux; `python3 -I`)

```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers          # never run "playwright install"
bash pipeline/lib/fetch_libs.sh                           # once: libraries and fonts into vendor/ (needs the npm registry)
node pipeline/bin/render.mjs --dir pipeline --mount /vendor=vendor --page scenes/testcard/scene.html --seconds 2 --chain h264_venue --ffmpeg renders/out.mp4
python3 -I pipeline/validators/spec_check.py renders/out.mp4 --profile venue_h264        # audio is part of the profile; see --list-profiles
python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json renders/colour.json
python3 -I pipeline/validators/mo8_gate.py renders/push_frames/                          # at most 96 frames, on the master before the delivery encode
bash pipeline/phone/encode_phone.sh MASTER.mov CAPTIONS.srt renders/phone.mp4            # PH1 from the ProRes master; runs inside the disk guard
python3 -I pipeline/phone/phone_check.py renders/phone.mp4 --scenario fill_20x9          # caption bottom as a percentage of picture height (limit 88)
python3 -I scripts/public_lint.py                         # is it safe to publish: the diff against HEAD plus untracked files (there is no --diff flag)
python3 -I scripts/stale_check.py --new-only              # retired values (25 fps, retired names) that the baseline does not already know
bash scripts/run_week2_checks.sh --quick                  # every test area, 60 s each; writes build/evidence/INDEX.md
bash tests/integration/run_tests.sh --all                 # the cross-package checks and the three end-to-end runs (about 3 minutes)
```

Exit codes everywhere: `0` pass, `1` a check failed, `2` bad usage, invalid input or identifying data found, `3` environment problem (tool missing, disk guard refused).
A write over 100 MB runs inside `lj_with_disk` (`scripts/lj_guard.sh`): it refuses unless free space minus the planned write stays above 400 MB and stops a stage below 250 MB.
`bash scripts/cleanup_scratch.sh` lists what the fortnight left behind (dry run); `--yes` deletes it.

## Rules every tool follows

- **Synthetic material only; 24 fps; BT.709 tags in the chain order of `chains.json`** (scale first, then `format=`, then `setparams=`). Tags alone are not evidence: `colour_patch.py` checks the pixels.
- **One redaction source.** What counts as identifying data (e-mail, address, path, token, serial, a name from the machine) is defined once, in `scripts/redaction_patterns.json`, and read by `public_lint.py`, `windows_check.py` and the two PowerShell scripts that write reports. `python3 -I scripts/public_lint.py --self-test --fail-on-skip` fails if any consumer disagrees or is missing.
- **Raw versus derived.** A raw PC inventory or raw colour-patch file from the maker's PC is a hardware fingerprint: it is read by the maker and pasted in chat only, never saved in the repo. Only the derived forms (`pc_tier.json`, `pc_chains.json`: buckets, versions, hashes, pass flags) may be filed, under `build/evidence/pc/`.
- **Windows behaviour is UNVERIFIED until the maker's PC has shown it.** A Linux CLI result for a Craft app is not evidence for Windows.

## Where evidence goes

| What | Where |
|---|---|
| one `lj-evidence/1` envelope per test (status, expected, actual, and a `disk` object with the free-space figures) | `build/evidence/wpNN/` (`tests_quick.jsonl`, `tests_all.jsonl`) |
| the table of the thirteen entries, with counts and the lowest free space seen | `build/evidence/INDEX.md`, `week2_summary.json` (written by `scripts/run_week2_checks.sh`) |
| the P-LOCK readiness map: every must-pass item and condition with one status | `build/evidence/P-LOCK-readiness-W2.md` |
| derived PC evidence (tier file, chain results) | `build/evidence/pc/` (filed by the orchestrator, never raw) |
| what each package built, how to run it, what is UNVERIFIED | `build/reports/WP-NN.md` |
| Fable's reviews | `reviews/build/` |
| renders, downloads, scratch (git-ignored, deleted when a test is done) | `renders/`, `vendor/`, `exports/`, the scratch folder beside the repo |
