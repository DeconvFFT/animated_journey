---
name: phone-delivery
description: Runs and reads the Life Journey phone-file tools (encode_phone, phone_check, sim_share) that turn the 16:9 master into the phone file PH1 or PH2 with burned-in phone captions, then check that text, strokes and marks still read in portrait, landscape, a small phone, after sharing and when a 20:9 player fills the screen, for every script that has test strings. Use when a phone file or phone caption is encoded, checked or signed off, when a caption size, margin or script is changed, or when the Phone row of the settings card is refreshed. Companion to mobile-phone-delivery (the decisions); this skill is the commands and the thresholds.
---

# Phone delivery tools

## Purpose

Make the phone file and prove, with numbers, that it reads on a phone (D-27). The decisions and the reasoning are in `mobile-phone-delivery` and `playbooks/mobile-delivery.md`; this skill is how the three WP-08 tools are run, what they decide and what to say when a check fails. Everything in `pipeline/phone/`.

## Rules that never bend

- **The phone file derives from the master.** Start from the ProRes 422 HQ master (W-15); never from the venue file and never from RGB frames. The phone file never replaces the venue file (W-63). One picture, 16:9: no crop, no reframing, no vertical cut.
- **The burn-in goes on the 1080 frame, before the downscale and the chain.** Captions are drawn with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in its header) on every build, because ffmpeg before n9.0 draws the `subtitles` filter in simple shaping and breaks Indic text without a warning (W-75; measured again in `build/evidence/wp08/shaping_paths.json`).
- **Relative file names, cwd set.** `encode_phone.py` runs ffmpeg in its own work folder, so only `caps.ass` and `fonts` ever appear inside the filter string and a Windows drive-letter colon never reaches it.
- **Neutral names and no metadata.** Output names are chosen by the caller (a neutral code before the reveal); the chain uses `-map_metadata -1` and `-fflags +bitexact`; the tools print base names only and never caption text.
- **Fill-crop rule.** A 20:9 phone set to fill crops about 10% (19.5:9: about 9%) off the top and the bottom. The caption box must end at **88%** of the picture height or higher up (a smaller percentage), so the whole bottom line stays (the venue margin, 5%, does not).
- **Per-script rule.** The shaping IoU (at least 0.9 against Pillow-raqm), the mark-survival check and the size check loop over every script in `pipeline/phone/test_strings.json` that has strings. A script without strings is **NOT TESTED**, never a pass. Today: Latin and Devanagari (neutral, `checked_by_reader: false`). Her language, Gujarati (D-31), is NOT TESTED until reader-confirmed strings with `marks[]` are added (three small steps, build plan 4.10).
- **Findings, not predictions.** `--finding-fs23` writes what FontSize=23 does on a phone as measured; the self-test never asserts it.
- **Nothing personal.** Test material is synthetic. No real photo, voice or caption of the family goes through these tools in the container (D-15); the real film's captions are private and the tools never print them.

## Procedure

1. Check the decks are clear: `df -h`; encodes run inside the guard (`lj_with_disk 100`; a 12-minute PH1 can reach 737 MB, so plan 800 with `LJ_PLANNED_MB=800`).
2. Encode (container; Windows is UNVERIFIED, there run the Python file directly with `py -3 -I`):
   ```bash
   bash pipeline/phone/encode_phone.sh MASTER.mov CAPTIONS.srt OUT.mp4 [--layout scene_report.json] [--profile phone_720_share] [--overwrite]
   ```
   It prints each step, checks size, fps, frame count, tags, level, bitrate (cap + 10%), `moov` before `mdat`, loudness (-16 LUFS, -1 dBTP measured on the AAC file), metadata, and writes `OUT.mp4.ass` and `OUT.mp4.phone.json` beside the file.
3. Validate with the WP-05 tools:
   ```bash
   python3 -I pipeline/validators/spec_check.py OUT.mp4 --profiles-file pipeline/phone/profile.json --profile phone_1080
   python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080
   ```
4. Check legibility in the five views, and the fill crop on its own:
   ```bash
   python3 -I pipeline/phone/phone_check.py OUT.mp4                       # portrait, landscape, small_portrait, shared, fill_20x9
   python3 -I pipeline/phone/phone_check.py OUT.mp4 --scenario fill_20x9  # prints the caption bottom as a percentage of picture height
   python3 -I pipeline/phone/phone_check.py OUT.mp4 --scenario fill_20x9 --aspect 19.5:9
   python3 -I pipeline/phone/phone_check.py --style phone --json phone_style.json --scripts-json scripts_tested.json
   ```
   A file check needs its `.ass` and `.phone.json` beside it and a caption-free frame in the file; it reads the lines that are allowlisted test strings (a real film's free text is measured for position, size and contrast only).
5. Simulate sharing, then check the copy:
   ```bash
   bash pipeline/phone/sim_share.sh OUT.mp4 SHARED.mp4 && python3 -I pipeline/phone/phone_check.py SHARED.mp4
   ```
   `sim_share.sh` never overwrites its input (hash compared before and after) and copies the caption file and sidecar next to the copy.
6. After any change to the caption style, the strings or the size: `python3 -I pipeline/phone/phone_check.py --candidates`, `--finding-fs23 --out ...`, `--shaping-paths`, then `--write-row pipeline/phone/PHONE-ROW.md` (the orchestrator pastes it over the card's Phone row and the `Scripts tested:` line over the language note), and `bash tests/phone/run_tests.sh --all`.
7. Put the test file on a real phone and have the maker answer `pipeline/phone/PHONE-TEST.md` (seven questions, including "when you zoom to fill, is the bottom line still whole?"). The numbers are a model; the phone is the measurement.

## Thresholds and their status (`pipeline/phone/thresholds.json`)

| What | Value | Status |
|---|---|---|
| Letter height (Latin x-height, or the base-letter band for other scripts) | at least 3.2% of picture height (target 3.8%) | W-63 (settled) |
| Visual angle of that height | at least 18 arcmin at 35 cm (target 21) | (J); the arcminute minimum is UNVERIFIED (ISO 9241-3 recalled, not re-read) |
| Viewing distance | 35 cm design, 40 cm margin | (J) |
| Contrast, fill against outline | at least 4.5:1 (target 7:1), WCAG | (J) |
| Stroke width after the scenario's smallest grid | 10th percentile at least 1 px; a gated line (3 px or more) keeps at least half its contrast | (J); the 4 px meaning-line floor is W-38 |
| Caption inside the 90% box | 5% to 95% both ways | settled (W-18) |
| Caption bottom in `fill_20x9` | at or above 88% (the 90% crop line minus 2 points) | (J) |
| Title height | at least 5% of picture height | ROADMAP section 6 |
| Mark survival | at least 2 px of ink in the zone after the downscale, and closer to the reference with the mark than without | (J) |
| Shaping IoU, libass against Pillow-raqm | at least 0.9 | (J) |
| Viewports, the 480p / 1 Mbps / veryfast "messenger" | the table in the file | UNVERIFIED: typical phones, not a measured handset and not any service's encoder |

## What to say when a check fails

- **A size check fails in `portrait` or `small_portrait` (advisory):** expected. Upright viewing is degraded by design; the answer is the hand-over line "turn it sideways", not a bigger caption.
- **`landscape` or `shared` fails on size:** raise the FontSize one step (the table in `caption_candidates.json` shows the cost in block height), re-run `--candidates`, and say that the maker's phone test is what confirms it.
- **`caption_bottom_pct` fails in `fill_20x9`:** the block sits too low. Raise `MarginV` (one unit is 3.75 px at 1080p) or shorten to one line; never move the venue file's margin to fix the phone file.
- **A mark is lost, or the shaping IoU is under 0.9:** a shaping finding for that script. First check the build (`--shaping-paths`: is the `ass` filter used, is the font the lock file's?); then the font; then the size. Never fix it by editing the test strings.
- **A hairline fails `shared`:** the line is thinner than the floor for what a messenger keeps. Redraw it at 4 px or drop it (W-38); do not widen the share profile.
- **A script says NOT TESTED:** say so in the settings card (the `Scripts tested:` line does); do not call it a pass.
- **Anything about a real phone, a real messenger, or Windows:** say UNVERIFIED and what would verify it.

## Windows and the PC (UNVERIFIED)

`encode_phone.py` and `phone_check.py` are Python (standard library, plus numpy and Pillow with raqm for the checker) and call ffmpeg; `sim_share.sh`, `encode_phone.sh` and the tests are bash and run in the container. On the maker's PC run `py -3 -I pipeline\phone\encode_phone.py MASTER CAPTIONS.srt OUT.mp4` from the project folder. Nothing here has been run on Windows; the PC's ffmpeg (9.0.2 expected) and Pillow's raqm support are untested there. The Gujarati shaping burn on the PC remains a P-LOCK condition (W-06, W-75).

## Files

`pipeline/phone/`: `profile.json` (chains and profiles in the shape of `chains.json` and `settings.json`, plus caption styles), `thresholds.json`, `encode_phone.py`, `encode_phone.sh`, `phone_check.py`, `sim_share.sh`, `test_strings.json` (WP-04's allowlist, read-only), `PHONE-TEST.md`, `PHONE-ROW.md`. `tests/phone/`: `run_tests.sh --quick|--all`, `run_checks.py`, `make_master.py`, `lint_strings.py`, `scene/`. Evidence in `build/evidence/wp08/`.
