---
name: mobile-phone-delivery
description: Makes, encodes and checks the phone deliverables for the Life Journey film (the two phone files PH1 and PH2, phone captions, the phone-safe frame and the project-phone protocol), runs the phone tools (encode_phone, phone_check, sim_share) with their exact commands and thresholds, and sets the keepsake and sharing rules for her phone and relatives' phones. Use when a phone file, phone caption, phone-safe shot, keepsake route, relatives' copy or any on-phone image is planned, encoded, tested or signed off, when a caption size, margin or script is changed, or when the Phone row of the settings card is refreshed.
---

# Mobile phone delivery

## Purpose

Make every Life Journey deliverable play beautifully on a phone (D-27) without weakening the venue master. There is one picture and two phone files, PH1 and PH2, cut from the ProRes master, with measured phone floors and a repeatable device test (W-63). The reasoning, the decision tables and the open questions live in `playbooks/mobile-delivery.md`. This skill is the agent form of that playbook. It also holds the operational side: how the three phone tools in `pipeline/phone/` (WP-08) are run, what their thresholds mean and what to say when a check fails. The numbers are a model; the phone is the measurement.

## When to use

- Encoding or checking PH1 or PH2, and running or reading `encode_phone`, `phone_check` or `sim_share`.
- Setting phone caption burn-in, the phone-safe frame, the fill-crop card or the dark-step tests; changing a caption size, margin or script.
- Choosing or testing her keepsake route, or a relative's copy.
- Reviewing any image that appears on a phone surface: lock screen, thumbnail, icon, page frame or forwarded frame.
- Refreshing the Phone row of the settings card (`pipeline/phone/PHONE-ROW.md`).

## When not to use

- The venue master, DCP, venue captions or hall loudness: use `theatrical-delivery-and-rights`.
- Story choices, or which deity or motif to show: those are the maker's decisions (O-64, which absorbs O-42; O-44). This skill applies only the phone constraints.
- ArtCraft app steps: use `craft-apps-visual-refinement` or `craft-apps-motion-refinement`.
- Consent or labels for AI-altered photos: use `ai-photo-to-animation-pipeline`.
- Any send or upload of the film before the reveal. That is never allowed.

## Procedure

1. Confirm the phone unknowns (O-54, which absorbs O-43, and the backup state) from the maker's written answers (the intake table is `research/mobile-delivery.md`, Follow-up research, Q-F7). The backup questions are: does Google Photos back up, **is "Back up all device folders" on (K1's first question)**, does the phone manufacturer's gallery sync run (Samsung Gallery to OneDrive; others UNVERIFIED), is the account shared. Never check her phone (D-02). Anything unknown defaults to "treat it as on" (K1).
2. Start from the ProRes 422 HQ master (W-15). Never start from the venue file or from RGB frames, and the phone file never replaces the venue file (W-63). One picture, 16:9: no crop, no reframing, no vertical cut.
3. Set the phone captions: Latin text at FontSize 28, MarginV 40, Outline 2, white, at most 32 characters a line (it fits the 90% by 90% box in both scripts; the venue file keeps its own guide of 42), two lines, 20 characters a second. Size Gujarati by the height of KA (K2), not by FontSize 28: **Noto Sans Gujarati is the caption face (FontSize 26.2 for the 3.8% target; W-18, W-21)**. Hind Vadodara is not used for any date or Samvat (no Gujarati digits, U+0AE6 to U+0AEF, so a date falls back to FreeSerif), and Mukta Vaani is not used for Gujarati text (unfused conjuncts when tagged Gujarati); Noto Sans Gujarati carries the digits, the Om sign and every conjunct. Her script on cards and verse is shaped outlines, never live text (W-21).
4. Fix the burn-in path (the tool does it; do not hand-roll it). Captions are drawn with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in its header; the master carries a BT.709 tag), on the 1080 frame, before the downscale and the chain, on every build and for every script. Before ffmpeg n9.0 the `subtitles` filter shapes in simple mode and breaks Indic text without a warning, so never use `subtitles` or `drawtext` for an Indic line (W-75; measured again in `build/evidence/wp08/shaping_paths.json`). Run the shaping check first, once, at P-LOCK (it also checks the build; protocol row 11). Its container form, `phone_check.py --shaping-paths`, covers only scripts that have test strings, so the Gujarati burn on the PC stays a P-LOCK condition (W-06, W-75). The tool runs ffmpeg in its own work folder, so only the relative names `caps.ass` and `fonts` appear in the filter string and a Windows drive-letter colon never reaches it. **Fill-crop rule.** A 20:9 phone set to fill crops about 10% (19.5:9: about 9%) off the top and the bottom, so the caption box must end at or above the `fill_20x9` limit in the thresholds table (a smaller percentage of the height) and the whole bottom line stays. The venue margin (5%) does not do that; never move the venue file's margin to fix the phone file.
5. Encode. Check the disk first (`df -h`); the script runs inside the guard (`lj_with_disk 100`), and a 12-minute PH1 can reach 737 MB, so set `LJ_PLANNED_MB=800` for the film.
   ```bash
   bash pipeline/phone/encode_phone.sh MASTER.mov CAPTIONS.srt OUT.mp4 [--layout scene_report.json] [--profile phone_720_share] [--overwrite]
   ```
   PH1 is the default profile `phone_1080` (the T-M1 template: `-crf 20`, `-maxrate 8M -bufsize 16M`, High 4.1, AAC-LC 192k, `+faststart`, metadata stripped). PH2 is `--profile phone_720_share` (720p, `-crf 22`, `-maxrate 3500k -bufsize 7M`, High 3.1, AAC-LC 160k) for low-storage phones and for relatives. Keep the bracketed `lut3d` step out until Trim P is signed. The caller names the output (File checks: a neutral code before the reveal); the chain uses `-map_metadata -1` and `-fflags +bitexact`, and the tools print base names only and never caption text. The encode prints each step and checks size, fps, frame count, tags, level, bitrate (cap + 10%), `moov` before `mdat`, loudness and metadata (File checks), and writes `OUT.mp4.ass` and `OUT.mp4.phone.json` beside the file. Exit 1 means the file was made but one of its own checks failed.
6. Validate with the WP-05 tools (use `phone_720_share` in both for PH2):
   ```bash
   python3 -I pipeline/validators/spec_check.py OUT.mp4 --profiles-file pipeline/phone/profile.json --profile phone_1080
   python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080
   ```
   Run the colour-patch test (within ±3/255, twelve patches) on the PC build of each template (W-16), and the twelve-patch caption colour test (Exercise 3 step 5 of the playbook); tinted caption colours are allowed only on a build that passes it. The encode repeats its audio with a lower true-peak target when the AAC file reads above -1.0 dBTP; for a file made without the tool, measure the final MP4 by hand (ffprobe fields, atom order, loudness) and re-encode with `volume=-0.5dB` if the peak is too high.
7. Check legibility in the five views, and the fill crop on its own:
   ```bash
   python3 -I pipeline/phone/phone_check.py OUT.mp4                       # portrait, landscape, small_portrait, shared, fill_20x9
   python3 -I pipeline/phone/phone_check.py OUT.mp4 --scenario fill_20x9  # prints the caption bottom as a percentage of picture height
   python3 -I pipeline/phone/phone_check.py OUT.mp4 --scenario fill_20x9 --aspect 19.5:9
   python3 -I pipeline/phone/phone_check.py --style phone --json phone_style.json --scripts-json scripts_tested.json
   ```
   A file check needs its `.ass` and `.phone.json` beside it and a caption-free frame in the file; it reads the lines that are allowlisted test strings (a real film's free text is measured for position, size and contrast only). The shaping, mark-survival and size checks loop over every script in `pipeline/phone/test_strings.json` that has strings. A script without strings is NOT TESTED, never a pass. As of 2026-10-20 that leaves Latin and Devanagari (neutral strings, `checked_by_reader: false`); her language, Gujarati (D-31), is NOT TESTED until reader-confirmed strings with `marks[]` are added (three small steps, build plan 4.10). Then check each shot's frame against Frame checks, with the safe-area overlay on three frames.
8. Simulate sharing, then check the copy:
   ```bash
   bash pipeline/phone/sim_share.sh OUT.mp4 SHARED.mp4 && python3 -I pipeline/phone/phone_check.py SHARED.mp4
   ```
   `sim_share.sh` never overwrites its input (hash compared before and after) and copies the caption file and sidecar next to the copy.
9. After any change to the caption style, the strings or the size, run `phone_check.py --candidates`, `--finding-fs23 --out ...` (what FontSize 23, the venue size, does on a phone as measured; a finding, never asserted by the self-test) and `--shaping-paths`, then `--write-row pipeline/phone/PHONE-ROW.md` (the orchestrator pastes it over the card's Phone row and the `Scripts tested:` line over the language note), then `bash tests/phone/run_tests.sh --all`.
10. Set a thumbnail with light in it: the first frame of her object or her hands in the opening (W-32, W-33), never a title card and never a deity (O-64); the same frame marks the folder on the venue sticks.
11. Run the project-phone protocol (T-M6, thirteen rows) on an Android in the 2019 to 2021 class and an iPhone, with no accounts on either. A failed row gets fixed and re-run. Then put the synthetic test file on a real phone and have the maker answer `pipeline/phone/PHONE-TEST.md` (seven questions, including "when you zoom to fill, is the bottom line still whole?").
12. Choose the route with K1 (her phone: cable, with her yes, after the reveal; ask first whether "Back up all device folders" is on, since the app-folder route is safe only if it is off; otherwise the tablet or the stick; ask the same question again in the her-turn conversation, Sun 7 Mar after about 14:00, W-48; after the copy rename the file to the film's title in her script and offer the lock-screen still, W-73, W-74) and K4 (relatives: PH2 as a WhatsApp document, after the ledger closes). Free space first (keyed on O-54): PH1's 737 MB ceiling plus a 200 MB margin means at least 1 GB free on her phone; if O-54 reports less, PH2 goes on by cable and PH1 waits for the tablet or the stick.
13. Log every send in the rights log (T8 `phone_share`) and the sharing table (T-M4). Nothing is sent before the reveal or before the ledger closes.

## Checklists

**File checks (every output; `encode_phone` and `spec_check` check most of these, grain survival is a template measurement)**
- ffprobe: H.264 High; level 4.1 for PH1 and 3.1 for PH2; yuv420p; color range tv; bt709 primaries, transfer and matrix; 24/1 fps; frame count equal to the timeline.
- The master carries `color_space=bt709` before any burn-in; atom order `ftyp, moov, ..., mdat`; `+faststart` present.
- Metadata: no title, comment or location. The hash is recorded in the manifest.
- Colour patches within ±3/255 (research fixtures: PH1 3/255, PH2 2/255; the WP-08 chains measured worst 1/255 on ffmpeg 6.1.1, 2026-10-19).
- Final MP4 true peak at or below -1.0 dBTP; loudness -16 LUFS (measured on the AAC file).
- PH1 grain survival at least 70% of the master (CRF 20 gives 73%; CRF 22 gives 43%, which fails).
- File name is a neutral code before the reveal.

**Frame checks (every shot with `phone_safe`)**
- Action and hands inside 10% to 90% of the height; text inside 5% to 95% across and 12% to 88% down.
- Caption zone: venue 78% to 93% of height; phone 68% to 86%.
- Strokes: 4 px for meaning-bearing lines, 3 px for decoration, dots 6 px, holes 4 px, hatch 3 px on 9 px pitch. No 1 px lines and no hairlines.
- Must-read type and text contrast as in the thresholds table. Captions white or neutral by default.
- No deity image on any phone surface without the maker's written decision (O-64, which absorbs O-42).

**Protocol rows (T-M6)**
1 hygiene; 2 copy by cable; 3 one-tap play; 4 fill-crop card per player; 5 caption burn-in read at 35 cm and 50 cm; 6 dark steps at 100 and 500 lux; 7 strokes and colour; 8 thumbnail and sort position; 9 chat round trip (fixture only, optional); 10 sound tone ladder, then each cue and both hum takes (W-19, W-65); 11 Gujarati shaping on the PC (P-LOCK; the single shaping gate); 12 slice fixture played from the project phone's gallery (P-LOCK); 13 scrubber page opened from the project Android's file manager and from Files on the iPhone, recording whether the video plays (measures the page's demotion).

**Sharing checks**
- Before the reveal: nothing reaches any phone.
- After the reveal: cable to her phone, with her yes.
- Relatives: only after the ledger closes (W-48), with the maker's yes, as a WhatsApp document. Log `phone_share = relatives_after_ledger`. Release lines 4d to 4g apply.
- Guests: no QR code and no live link on the night.

## Thresholds and quality bar

`phone_check` reads these from `pipeline/phone/thresholds.json`. Every number is labelled (M), (C), (J) or UNVERIFIED; gallery, messenger and fill behaviour are measured, not assumed.

| What | Value | Status |
|---|---|---|
| Must-read letter height (Latin x-height, or the base-letter band for other scripts) | at least 3.2% of picture height (hard floor); target 3.8%, which is 41 px at 1080p | W-63 (settled) |
| Visual angle of that height | at least 18 arcmin at 35 cm (target 21) | (J); the arcminute minimum is UNVERIFIED (ISO 9241-3 recalled, not re-read) |
| Viewing distance | 35 cm design, 40 cm margin | (J) |
| Contrast, fill against outline | at least 4.5:1 (target 7:1), WCAG | (J) |
| Stroke width after the scenario's smallest grid | 10th percentile at least 1 px; a gated line (3 px or more) keeps at least half its contrast | (J); the drawn floors are under Frame checks (W-38) |
| Caption inside the 90% box | 5% to 95% both ways | settled (W-18) |
| Caption bottom in `fill_20x9` | at most 88% of picture height, measured from the top, so the box ends at 88% or higher up (the 90% crop line minus 2 points); top at least 12% | (J) |
| Title height | at least 5% of picture height | ROADMAP section 6 |
| Mark survival | at least 2 px of ink in the zone after the downscale, and closer to the reference with the mark than without | (J) |
| Shaping IoU, libass against Pillow-raqm | at least 0.9 | (J) |
| Viewports, the 480p / 1 Mbps / veryfast "messenger" | the table in the file | UNVERIFIED: typical phones, not a measured handset and not any service's encoder |

- A phone copy is a faithful reduction: master to PH1 to a chat proxy equals master straight to the proxy, within 0.01 (M).
- Black is pinned at code 16. The Trim P starting value is 4 to 7 IRE at codes 24 to 40 (J), tuned on the phone.
- Measured on synthetic material (`pipeline/phone/PHONE-ROW.md`, 2026-10-19): FontSize 28 in Noto Sans gives a Latin x-height of 3.44% of the picture height, above the 3.2% floor and under the 3.8% target, and the maker's phone test decides whether a step up is wanted. The venue size, FontSize 23, measures 2.82%, under the floor, which is why the phone file has its own caption setting.

## What to say when a check fails

- **A size check fails in `portrait` or `small_portrait` (advisory):** expected. Upright viewing is degraded by design; the answer is the hand-over line "turn it sideways", not a bigger caption.
- **`landscape` or `shared` fails on size:** raise the FontSize one step (the table in `caption_candidates.json` shows the cost in block height), re-run `--candidates`, and say that the maker's phone test is what confirms it.
- **`caption_bottom_pct` fails in `fill_20x9`:** the block sits too low. Raise `MarginV` (one unit is 3.75 px at 1080p) or shorten to one line.
- **A mark is lost, or the shaping IoU is under 0.9:** a shaping finding for that script. First check the build (`--shaping-paths`: is the `ass` filter used, is the font the lock file's?); then the font; then the size. Never fix it by editing the test strings.
- **A hairline fails `shared`:** the line is thinner than the floor for what a messenger keeps. Redraw it at 4 px or drop it (W-38); do not widen the share profile.
- **A script says NOT TESTED:** say so in the settings card (the `Scripts tested:` line does).
- **Anything about a real phone, a real messenger, or Windows:** say UNVERIFIED and what would verify it.

## Windows and the PC (UNVERIFIED)

`encode_phone.py` and `phone_check.py` are Python (standard library, plus numpy and Pillow with raqm for the checker) and call ffmpeg; `sim_share.sh`, `encode_phone.sh` and the tests are bash and run in the container. On the maker's PC run `py -3 -I pipeline\phone\encode_phone.py MASTER CAPTIONS.srt OUT.mp4` from the project folder. Nothing here has been run on Windows; the PC's ffmpeg (9.0.2 expected) and Pillow's raqm support are untested there.

## Guardrails

- **Respect and the Hindu-only rule (D-28).** "Indian" always means Hindu: Sanatan Dharma and its sanskriti. No Mughal or other Islamic motifs and no Christian motifs, ever. Leave out shared or ambiguous decoration by default: jaali, paisley, mehndi borders, arches, tile patterns. Church-shaped bells, candles where a diya belongs, a flat gold-disc halo drawn as in a church icon, crosses, winged figures: Christian or colonial layer, none. The ghanta (temple bell), the diya and the prabhavali or prabhamandala are Hindu and are not excluded by this rule. The swastika in a thumbnail or lock-screen still is out by default (SW0, W-72); a sathiyo on a phone surface is the maker's call alone, with the room's reading (O-44, O-66).
- **Deities** are shown with correct iconography and respect. The deity policy is class P1 for all eight deities: symbols and seva objects that are not a svarupa, and no deity drawn, generated or photographed (W-61); PR4, as the register states it: her Thakorji, chitraji, any picture of hers and anything inside the mandir are never photographed without her knowing; a seva article outside the mandir (the jhari in its cloth, the lamp, the closed doors) may be photographed by sight, untouched, on an unsynced phone (O-58), each logged as a G5 flag (O-48). No deity image on a phone surface until the maker decides in writing, as her proxy (O-64, which absorbs O-42). The default is her script's end-card line, a lamp or the object.
- **Rights.** Every forwarded copy is a public distribution, so no copy goes out before the ledger closes (W-48). Fonts must be OFL with a rights-log row (W-21). Nothing uncleared goes into a phone copy.
- **Privacy.** No personal media in git. The repo is public, so use person IDs only. Project phones carry no accounts unless the maker decides otherwise (Decision 12). Nobody checks her phone before the reveal (D-02). No phone test or copy leaves the project phones before the reveal. Test material for the tools is synthetic: no real photo, voice or caption of the family goes through them in the container (D-15).
- **Authority.** The register wins. This skill does not edit `DECISIONS.md`, `CHARTER.md`, `ROADMAP.md`, `CLAUDE.md` or anything under `.claude/`.

## References

- `pipeline/phone/`: `profile.json` (chains, profiles and caption styles), `thresholds.json`, `encode_phone.py` and `.sh`, `phone_check.py`, `sim_share.sh`, `test_strings.json` (WP-04's allowlist, read-only), `PHONE-TEST.md`, `PHONE-ROW.md`. `tests/phone/`: `run_tests.sh --quick|--all`. Evidence in `build/evidence/wp08/`.
- `playbooks/mobile-delivery.md`: the maker's playbook. It holds the full reasoning, the decision tables (K1 to K5, Decisions 1 to 14) and the proposed edits to other playbooks.
- `research/mobile-delivery.md`: the research notes. Summary, Q1 to Q10, templates T-M1 to T-M9 and the changes table.
- `research/mobile-delivery-fixtures/`: `safe_area_template.svg`, `phone_test_p1_fillcrop.svg`, the CSVs and the README.
- `research/devotional-sound-script.md`: the sibling track's Gujarati font, shaping and phone-speaker notes.
- Key URLs, read 2026-10-19 (full entries in Sources): [1] WhatsApp media limits (script-rendered; dated excerpt saved); [3] WhatsApp long videos and the document route (same); [18] Android supported formats; [20] YouTube recommended encoding settings; [10] Apple Shared Albums limits (page dated 2026-09-14); [37] Android USB File Transfer; [49] Android app pinning; [53] WCAG contrast.

## Sources

*Copied from `research/mobile-delivery.md` (items 1 to 73). The researcher read each page on the date shown; items 63 to 73 were added by the round-1 implementor. "Digest only" means read as a search-result summary. UNVERIFIED entries were not confirmed.*

1. WhatsApp Help Center, "How to send media, contacts, or location" — https://faq.whatsapp.com/453914586839706/?cms_platform=web — read 2026-10-19 — video default limit 100 MB and 720p (fast) or 64 MB and 480p (slow); documents 2 GB. **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium; one reading, not the maker's browser.**
2. WhatsApp Help Center, "About HD photos and videos" (Android) — https://faq.whatsapp.com/759301289012856/?cms_platform=android — read 2026-10-19 — HD per message or default under Media upload quality; no pixel numbers.
3. WhatsApp Help Center, "I can't send long videos" (today's title: "Can't send longer videos") — https://faq.whatsapp.com/823886715479103/ — read 2026-10-19 — "64MB on all platforms"; Document route up to 2 GB; the same page repeats [1]'s 100 MB and 720p default for a fast connection. **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
4. WhatsApp Help Center, "About forwarding limits" — https://faq.whatsapp.com/1053543185312573 — read 2026-10-19 — up to five chats at a time; a message forwarded to you "can only be shared with one additional group chat" (new on the re-read). **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
5. WhatsApp Blog, "Reactions, 2GB File Sharing, 512 Groups" — https://blog.whatsapp.com/reactions-2gb-file-sharing-512-groups — 2022-05-05, updated 2022-07-11 — 2 GB files; end-to-end encrypted.
6. WhatsApp Privacy Policy — https://www.whatsapp.com/legal/privacy-policy — "Effective January 4, 2021" as displayed — delivered messages deleted from servers; undelivered kept up to 30 days.
7. WhatsApp Help Center, "How to back up your chat history" (Android) — https://faq.whatsapp.com/481135090640375/?cms_platform=android — read 2026-10-19 — backup to WhatsApp cloud or Google; "Include videos in chats".
8. Telegram FAQ — https://telegram.org/faq — read 2026-10-19 — files up to 2 GB; chats stored in the Telegram cloud; silent on compression.
9. Telegram blog, "700 Million Users and Telegram Premium" — https://telegram.org/blog/700-million-and-premium — 2022-06-19 — 2 GB free, 4 GB Premium.
10. Apple Support, "Shared Albums limits" — https://support.apple.com/en-us/148868 — published 2026-09-14 — iOS 26 and earlier: 15 minutes at 720p; iOS 27 and later: original resolution, counts against storage.
11. Google Photos Help, "Choose the upload size of your photos and videos" — https://support.google.com/photos/answer/6220791 — read 2026-10-19 — Storage saver resizes video above 1080p to 1080p; 15 GB per account.
12. Google Photos Help, "Turn backup on or off" (now titled "Back up photos & videos") — https://support.google.com/photos/answer/6193313 — read 2026-10-19 and re-read in a headless Chromium (Android tab) — Photos settings, Backup; "your chosen device folders are automatically backed up too, not only your camera"; a "Back up all device folders" switch; no default folders listed; removal means deleting the items on photos.google.com (that turning backup off leaves them is an inference).
13. Apple Support, "How to use AirDrop on your iPhone or iPad" — https://support.apple.com/en-us/119857 — read 2026-10-19 — "Everyone for 10 Minutes"; AirDrop code with iOS 26.2 or later.
14. Google, "Android Quick Share support for AirDrop" — https://blog.google/security/android-quick-share-support-for-airdrop-security/ — 2025-11-20 — Pixel 10 first; AirDrop "Everyone for 10 minutes" only.
15. Google Drive Help, "Google Drive file size limits" — https://support.google.com/drive/answer/37603 — read 2026-10-19 — up to 5 TB a file.
16. Google Drive Help, "Share files from Google Drive" — https://support.google.com/drive/answer/2494822 — read 2026-10-19 — "Anyone with the link"; viewers can download unless turned off.
17. Gmail Help, "Attachment size limit" — https://support.google.com/mail/answer/6584 — read 2026-10-19 — 25 MB; larger replaced by a Drive link.
18. Android Developers, "Supported media formats" — https://developer.android.com/media/platform/supported-formats — read 2026-10-19 — H.264 Baseline and Main decoders; HEVC Main Level 3 for mobile; `moov` before `mdat`.
19. Apple Support, "iPhone 15 Tech Specs" — https://support.apple.com/en-us/111831 — read 2026-10-19 — 6.1 in, 2556x1179, 460 ppi; HEVC, H.264, ProRes.
20. YouTube Help, "Recommended upload encoding settings" — https://support.google.com/youtube/answer/1722171 — read 2026-10-19 — H.264 High, BT.709, 8 Mb/s 1080p SDR, AAC-LC, `moov` at front.
21. FFmpeg, "Formats Documentation" — https://www.ffmpeg.org/ffmpeg-formats.html — read 2026-10-19 (first 100,000 characters) — faststart; MP4 muxer writes Nero and QuickTime chapters by default.
22. Robitza, "CRF Guide" — https://slhck.info/video/2017/02/24/crf-guide.html — read 2026-10-19 — sane x264 range 18 to 28; plus or minus 6 is about half or double.
23. x265 documentation, command line options — https://x265.readthedocs.io/en/master/cli.html — read 2026-10-19 (first 100,000 characters) — CRF default 28; VBV needs both options in CRF mode; `--tune grain`.
24. caniuse, "HEVC/H.265 video format" — https://caniuse.com/hevc — read 2026-10-19 — "partial" in Chrome from 107 and Firefox from 137.
25. StatCounter, "Mobile Operating System Market Share India" — https://gs.statcounter.com/os-market-share/mobile/india — September 2026 — Android 93.89%, iOS 6.05%. Web traffic, not an installed base.
26. StatCounter, "Mobile Screen Resolution Stats India" — https://gs.statcounter.com/screen-resolution-stats/mobile/india — September 2026 — top six viewports (together 37%).
27. GSMArena, "Xiaomi Redmi 9A" — https://www.gsmarena.com/xiaomi_redmi_9a-10279.php — read 2026-10-19 — 6.53 in, 720x1600, 20:9, 400 nits typical; announced 2020-06-30; Helio G25; microUSB 2.0 with OTG.
28. GSMArena, "Xiaomi Redmi Note 10" — https://www.gsmarena.com/xiaomi_redmi_note_10-10247.php — read 2026-10-19 — 6.43 in, 1080x2400, 20:9; announced 2021-03-04.
29. GSMArena, "Xiaomi Redmi Note 10 review: lab tests" — https://www.gsmarena.com/xiaomi_redmi_note_10-review-2244p3.php — read 2026-10-19 — measured 475 nits manual, 682 auto.
30. Bababekova et al., "Font size and viewing distance of handheld smart phones", Optometry and Vision Science 88(7):795-7, 2011 — https://pubmed.ncbi.nlm.nih.gov/21499163/ — abstract via search digest only — mean 36.2 cm texting (n = 129), 32.2 cm web (n = 100).
31. GSMArena, "YouTube updated with pinch-to-zoom for screens wider than 16:9" — https://m.gsmarena.com/youtube_updated_with_pinchtozoom_for_screens_wider_than_169-news-28290.php — 2017-11-16 — crop-zoom fills and may crop; Samsung page (403) via digest only.
32. Apple Developer, "AVLayerVideoGravity.resizeAspectFill" — https://developer.apple.com/documentation/AVFoundation/AVLayerVideoGravity/resizeAspectFill — digest only — resizeAspect fits; resizeAspectFill fills.
33. Apple Support, "Transfer files between your Windows device and iPhone, iPad, or iPod touch" — https://support.apple.com/guide/devices-windows/transfer-files-between-your-devices-mchl4bd77d3a/windows — read 2026-10-19 — drag onto apps that support file sharing.
34. Apple Support, "Sync photos between your Windows device and iPhone, iPad, or iPod" — https://support.apple.com/guide/devices-windows/sync-photos-to-your-device-mchl4af095d3/windows — read 2026-10-19 — "Include videos"; unavailable while iCloud Photos is on.
35. Apple Support, "Sync movies between your Windows device and iPhone, iPad, or iPod" — https://support.apple.com/guide/devices-windows/sync-movies-to-your-device-mchl36119991/windows — read 2026-10-19 — needs the Apple TV app; home videos not mentioned.
36. Apple Support, "Connect external storage devices to iPhone" — https://support.apple.com/guide/iphone/external-storage-devices-iph95baac91f/ios — digest only (body truncated) — one partition in APFS, HFS+, exFAT, FAT32 or FAT.
37. Android Help, "Transfer files between your Android device and computer" — https://support.google.com/android/answer/9064445 — read 2026-10-19 — USB File Transfer mode.
38. Apple Developer Forums, "Publish or test mini sites locally in Safari with relative source references" — https://developer.apple.com/forums/thread/710001 — July 2022 — Files preview does not load relative references.
39. Apple Community, "How to open local html files in safari" — https://discussions.apple.com/thread/256102223 — 2025-07-21 and 22 — Quick Look "will not run JavaScript"; iOS 18.5.
40. GitHub, THU-MAIC/OpenMAIC issue 1847 — https://github.com/THU-MAIC/OpenMAIC/issues/1847 — opened 2026-10-08, open — standalone HTML export blank in the iOS Files preview.
41. MIT App Inventor Community, "Off topic html and Android 10" — https://community.appinventor.mit.edu/t/off-topic-html-and-android-10/35979 — June to August 2021 — `content://` addresses; relative links fail.
42. TiddlyWiki Talk, "Cannot play local video (Android)" — https://talk.tiddlywiki.org/t/cannot-play-local-video-android/3516 — 2022-06-01 — local video fails via relative paths.
43. Mozilla Bugzilla 1809954 — https://bugzilla.mozilla.org/show_bug.cgi?id=1809954 — closed as a duplicate — Firefox for Android cannot load subresources through `content://`.
44. WebKit blog, "Full Third-Party Cookie Blocking and More" — https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ — 2020-03-24 — seven-day cap on script-writable storage.
45. MDN, "Making PWAs installable" — https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable — read 2026-10-19 — HTTPS or localhost required.
46. Tranquillity Base, "mChapters" — https://www.tranquillitybase.jp/mChapters/mChapters_en.html — read 2026-10-19 — the Music and TV apps on iOS do not appear to support chapters.
47. Larry Jordan, "QuickTime: Display Chapter Markers" — https://larryjordan.com/articles/chapter-markers/ — read 2026-10-19 — QuickTime Player shows chapters.
48. Apple Support, "Use Guided Access on iPhone or iPad" — https://support.apple.com/en-us/111795 — read 2026-10-19 — triple-click the side button; disable screen areas or all touch.
49. Android Help, "Pin and unpin screens" — https://support.google.com/android/answer/9455138?hl=en — read 2026-10-19 — app pinning.
50. Xiaomi, "Notice of termination of Xiaomi Cloud sync for Gallery items" — https://i.mi.com/announcement/stop_service — read 2026-10-19 — ends 2022-10-25; data deleted 2023-08-01.
51. Samsung Support, "OneDrive on your Samsung phone or tablet" — https://www.samsung.com/us/support/answer/ANS10003437/ — digest only (403) — Gallery sync needs Samsung and Microsoft accounts.
52. W3C, "Understanding SC 2.5.5: Target Size (Enhanced)" — https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — read 2026-10-19 — 44 by 44 CSS pixels.
53. W3C, "Understanding SC 1.4.3: Contrast (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — read 2026-10-19 — 4.5:1; 3:1 for large text.
54. Lee et al., "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ — read 2026-10-19 — qualitative; swipes and double-taps failed.
55. Wikipedia, "Lux" — https://en.wikipedia.org/wiki/Lux — read 2026-10-19 — office 320 to 500 lux; overcast 1,000; full daylight 10,000 to 25,000.
56. Wikipedia, "Fresnel equations" — https://en.wikipedia.org/wiki/Fresnel_equations — read 2026-10-19 (first 100,000 characters) — about 4% reflectance per glass surface.
57. Netflix Partner Help Center, "Timed Text Style Guide: General Requirements" — https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements — read 2026-10-19 — two lines maximum; events 5/6 s to 7 s.
58. Local: `CHARTER.md`; `DECISIONS.md` (D-02, D-05, D-15, D-24, D-27, D-28, D-31, W-04, W-15 to W-20, W-25, W-26, W-30, W-33, W-35, W-46 to W-48, O-30, O-43); commit `ac6711e`. O-42 and O-43 were defined in `reviews/04-hindu-mobile-briefs-review.md`; the register (2026-10-19) absorbs them as O-64 and O-54, and O-44 is its own row.
59. Local: `playbooks/theatrical-delivery.md` (Steps 4 to 8, T1, T2, T8, T9, T11); `playbooks/format.md` (Step 8, Decisions 8 and 11, Step 15); `playbooks/cinematic-quality.md` (T1 PR2 and PR3, T6, Exercise 2, TY1); `playbooks/surprise-ops.md` (Step 11, Decision 15); `playbooks/toolchain.md` (captions).
60. Local: `research/hindu-visual.md` F3 (M-H1) and `research/hindu-visual-fixtures/phone_chart.svg`; `research/cinematic-quality.md` FQ1 (Legge and Bigelow 2011 and the BBC guidelines are cited there; neither was re-opened); `research/agent-pipeline.md` Q-F1; `reviews/04-hindu-mobile-briefs-review.md` Part 4.
61. Local: this track's fixtures and measurements, 2026-10-19: `research/mobile-delivery-fixtures/` (README, SVG templates, CSVs, Gujarati and Devanagari shaping evidence).
62. Local, sibling track: `research/devotional-sound-script.md` (Q9 fonts, Q10 shaping, Template L caption sizes, Summary 14 phone-speaker model) and `research/devotional-sound-script-fixtures/` (caption size and width CSVs, `shaping_fixture.tsv` and `.srt`, `phone_speaker_model_2026-10-19.csv`, README).
63. FFmpeg source at tags n6.1.1, n7.0, n8.0, n9.0.2 (`libavfilter/vf_subtitles.c`, `drawutils.c`, `libavcodec/ass.c`) — https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/libavfilter/vf_subtitles.c — read 2026-10-19 — n6.1.1 draws subtitle colours as BT.601; n7.0 uses the link's colourspace; n8.0 adds the `.ass` `YCbCr Matrix` header; `shaping` reaches `subtitles` in n9.0.
64. Google Fonts, `ofl/hindvadodara/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/hindvadodara/OFL.txt — read 2026-10-19 — SIL OFL 1.1, "Copyright (c) 2015 Indian Type Foundry", no Reserved Font Name.
65. Google Fonts, `ofl/notosansgujarati/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/notosansgujarati/OFL.txt — read 2026-10-19 — SIL OFL 1.1, "Copyright 2022 The Noto Project Authors", no Reserved Font Name.
66. MediaTek, "Helio G25" — https://www.mediatek.com/products/smartphones/mediatek-helio-g25 — read 2026-10-19 — H.264 and HEVC playback at 1080P 30 fps; no profile or bitrate given.
67. Android Developers, Media3 `PlayerView` — https://developer.android.com/reference/androidx/media3/ui/PlayerView — read 2026-10-19 — `resize_mode` default fit.
68. Apple Developer Documentation, `AVPlayerLayer.videoGravity` — https://developer.apple.com/documentation/avfoundation/avplayerlayer/videogravity — read 2026-10-19 — default `resizeAspect` (fit).
69. pushtimarg.net, "Seva" — https://pushtimarg.net/seva/ — read 2026-10-19 — Mangla: bells rung thrice and the Sankh blown; Shayan: a small lamp kept on.
70. pushtimarg.net, "FAQs" — https://pushtimarg.net/faqs/ — read 2026-10-19 — a picture "pusht" by a Goswami is served "from Mangala to Shayan"; nothing on phones or screens.
71. Local: `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt` — dated excerpts of [1] to [5].
72. Local: `research/pushtimarg-world.md` (F6, PR2, PR4, PR10, PR14, open Q3).
73. Local: round-1 fixtures in `research/mobile-delivery-fixtures/` (caption colour CSVs, `caption_ycbcr_matrix_example_2026-10-19.ass`, `scaler_bracket_720p_panel_2026-10-19.csv`, the re-cut Gujarati `.srt` and `.png`).

## Changelog

- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): PH1 and PH2 replace the retired phone-file names throughout (S-57); the caption face is Noto Sans Gujarati only, with Hind Vadodara and Mukta Vaani not used, and the `ass` path before ffmpeg n9.0 (W-21, W-75); the shaping check is the single P-LOCK gate (W-06); the sound row and cold-open work follow W-19, W-65 and W-76; the her-turn conversation is Sun 7 Mar after about 14:00 (S-64, W-48); O-42 resolves to O-64 and O-43 to O-54; the deity and sathiyo rows follow W-61, PR4 and W-72.
- 2026-10-20: Stale-wording sweep (2026-10-20): the register's phone figures, at most 32 characters a phone caption line (W-18) in procedure step 5 and the quality bar, and a PH2 cap of 3.5 Mb/s (W-63), written as `-maxrate 3500k -bufsize 7M` in procedure step 4 as in `pipeline/phone/profile.json`. No floor, check or decision changed.
- 2026-10-20: Folded in the build sprint's operational phone skill (WP-08), so there is one phone skill and `phone-delivery` is not installed: the `encode_phone`, `phone_check` and `sim_share` commands, the thresholds table and the failure answers now live here (procedure steps 3 to 9 and the two sections after the checklists). Procedure steps were renumbered, and the quality-bar bullets that restated the caption line (now step 3) and the type height (now the thresholds table) were merged into those places. No floor, check or decision changed.
- 2026-10-20: The photograph rule in Guardrails, Deities is PR4 as the register states it, word for word (Codes, W-61, W-70; `playbooks/mobile-delivery.md` surfaces table). The old clause barred a photograph of anything in her seva space; the register bars photographing her Thakorji, her chitraji, her pictures and anything inside the mandir without her knowing, and allows a seva article outside the mandir by sight, untouched, on an unsynced phone, each logged as a G5 flag. No floor, check or decision changed.
