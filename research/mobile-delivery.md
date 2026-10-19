# Phone delivery: the film and the keepsake on a mobile phone — research notes

*Track key `mobile-delivery`. Sonnet researcher, Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27). Builds on `CHARTER.md`, `DECISIONS.md` (D-02, D-15, D-24, D-27, D-28, **D-31**, W-15 to W-20, W-25, W-30, W-46 to W-48, O-30, O-43), `reviews/04-hindu-mobile-briefs-review.md` Part 4, the sibling note `research/devotional-sound-script.md` (Indic fonts, shaping, phone-speaker model), and the playbooks named in "Changes to existing playbooks".*

**Update made late on 2026-10-19 (D-31, commit `ac6711e`).** While this note was being written the maker recorded her world: **her region, her mother tongue (Gujarati), her tradition (a Pushtimarg Vaishnav family), her deities, all Hindu festivals, and an Android phone.** The brief (and the first draft of this note) treated her phone and script as unknown. I re-keyed what changes for this track: **her phone is Android** (hand-over, hygiene, keepsake and the device class she is probably in), **her script is Gujarati** (caption sizes, the shaping check, and a measured Gujarati shaping failure). Everything else in the decision tables stays keyed on what is still unknown (her Android's make, model, version, screen, storage, USB port and backup state: O-43). Pushtimarg and regional material is the other sprint's to research; this note only uses it where phone delivery touches it.

**Round-1 corrections (2026-10-19, later the same day).** `reviews/mobile-delivery-round1.md` asked for eight exact edits and seven follow-ups; they are applied in place below and answered in "Follow-up research (round 1)" at the end. Three readings of this note changed: (1) the Gujarati and Devanagari shaping failures were the **ffmpeg build** (`subtitles` before n9.0 shapes in simple mode), not the font (Q8, Summary 14); (2) tinted captions are fine on ffmpeg n7.0 and later when the master is BT.709-tagged, and the first pass's "cream shifts blue +9" did not reproduce (Q2, Q-F2); (3) the exhibit PNG and SRT were re-cut with the non-sacred test line only.

**How these notes were made, and what they cannot claim.**
- Every platform fact below was read on 2026-10-19 from the page named in Sources; if a page could not be opened it is marked **digest only** (read as a search-result summary) or **UNVERIFIED**.
- Measurements marked **(M)** were run today in the cloud container (ffmpeg 6.1.1 with libx264, libx265, libass and HarfBuzz; ImageMagick; rsvg-convert; Python 3.13 with numpy and Pillow) on **synthetic material only**. Nothing personal was used, and nothing was sent through any messaging app. Fixtures, result CSVs and the method are in `research/mobile-delivery-fixtures/` (README there). The harness scripts were throwaway and stayed in the scratchpad (sprint rule: no code is written).
- **Every Windows-side step is UNVERIFIED** until `windows_check_report.json` for the maker's PC is in the repo (W-28). The PC's ffmpeg is expected to be 9.0.2 (agent-pipeline Q-F1); the container's is 6.1.1; the colour-patch test must be re-run on the PC build (W-16).
- **Search budget.** The shared web-search allowance for this run ran out partway through, so a few items were fetched directly or left UNVERIFIED: Signal's limits (support.signal.org returned 403), Telegram's "send without compression" (official FAQ silent), the default fill/fit behaviour of the Android gallery, Google Photos, Apple Photos, WhatsApp and Telegram players, how filmmakers deliver vertical versions (Adobe's Auto Reframe page returned 403), and Apple's TV-app "Home Videos" route. The test protocol measures each of them on the project phones instead.
- Market shares and screen lists are web-traffic statistics (StatCounter, September 2026), not an installed-base count of this family's phones: UNVERIFIED for her.

---

## Summary

1. **One phone master, from the ProRes master: P1 = 1920x1080 24p H.264 High L4.1, 8-bit 4:2:0, BT.709, `-preset slow -crf 20 -maxrate 8M -bufsize 16M`, AAC-LC 192 kbps, `+faststart`, metadata stripped.** Measured on three synthetic masters: 2.0 to 2.7 Mb/s typical, 8 Mb/s at the cap. That is **199 to 262 MB for 12 minutes (149 to 196 MB for 9) typical, 737 MB (553 MB) as the hard ceiling** (M). The brief's "about 500 to 700 MB" is the ceiling, not the expectation.
2. **CRF 20 is a maximum, not a midpoint.** Grain survival in a flat patch (cinematic-quality PR3, pass at 70%) was 73% at CRF 20, 43% at CRF 22 and 17% at CRF 24 (M). If the film is finished with baked grain, a looser P1 fails the gate the plan already has.
3. **P2 (the small copy) is 1280x720 24p H.264, CRF 22, cap 4 Mb/s, AAC 160 kbps.** On this content CRF 22 lands at 0.4 to 0.9 Mb/s, so the cap never binds: **52 to 92 MB for 12 minutes** (M). P2 cannot carry grain (27% at CRF 20, 0% from CRF 23); PR3 does not apply to it. Its job is low-storage relatives' phones after the ledger, sent as a WhatsApp document.
4. **Skip the HEVC variant and any HDR variant.** HEVC at CRF 18 to 26 kept 1 to 27% of the grain; `--tune grain` at CRF 20 kept 49% but cost 3.5 MB against P1's 3.0 MB (M). The saving comes from deleting the grain. Android only guarantees HEVC Main Level 3 on mobile [18], browsers are "partial" [24], and iPhones play H.264 as well as HEVC [19]. The master is SDR BT.709 (W-15): there is no HDR picture to deliver.
5. **The "two lossy encodes turn line art to mush" watch-out is real but smaller than briefed; the damage is the messaging recompression.** Line-contrast retention through master to P1 to a WhatsApp-class 720p proxy equals master straight to the proxy within 0.01 (M). Deriving from the venue file costs 0.15 to 0.5 dB at the same CRF and 19% and 43% more bytes for P1 on the two uncapped clips (9 to 14% more for P2) (M). The decisive reason to encode from the master is that the venue file has the W-18 captions burned in at the venue position, so it cannot be the source at all.
6. **The 4 px line floor holds and is now reproduced.** Through a 720p, 2.5 Mb/s proxy a half-pixel 2 px line keeps 0.85 and 3 px keeps 0.93; through a 360p, 0.5 Mb/s proxy 3 px keeps 0.61 and 4 px 0.84 (M, reproduces `research/hindu-visual.md` M-H1 within 0.02). Meaning-bearing strokes 4 px, decoration 3 px, dots 6 px, holes 4 px, hatch 3 px at 9 px pitch.
7. **A 16:9 picture filled onto a 19.5:9 to 20:9 screen loses 9.0% to 10.0% of its height top and bottom (11.9% at 21:9).** The six most common Indian phone viewports in September 2026 are all between 19.5:9 and 20:9 (37% of Indian mobile web traffic) [26]. **Fill is a user action, not the default, in the one player documented** (YouTube's crop-zoom [31]); the other players' defaults are UNVERIFIED and the fill-crop card measures them.
8. **The W-18 caption has a bigger problem than the crop: ffmpeg's default `MarginV` puts caption descenders at 3.5% from the bottom, outside the 5% graphics-safe box** (M). The venue file needs `MarginV` 20 or more (6.9%); the phone file needs its own burn-in: `FontSize=28`, `MarginV=40` (block at 68% to 86% of height), at most 36 characters a line, two lines, white (M).
9. **Size passes, position and orientation fail.** FontSize 23 gives x-height 0.40° at 35 cm on a 6.1-inch screen in landscape fit (0.35° at 40 cm), above the 0.35° target I set; upright inline in a chat it drops to 0.23°, below any reasonable floor for a 50+ viewer. Design for landscape; treat the upright chat view as degraded.
10. **The cold open is a lighting problem before it is a grade problem.** In a 500 lux kitchen at about 150 nits of white, the first code distinguishable from black is 34 to 46 (8-bit limited range), not the 20 to 24 the working limit assumes (computed). The phone file needs a **Trim P** (shadow lift with black pinned) and the cold open needs either a visible first light within about 4 s or a first sound with energy above 400 Hz (phone speakers are small; test with the tone ladder). Decision flagged for the maker.
11. **The self-contained HTML keepsake does not work on a phone.** Quick Look in Files "will not run JavaScript" and does not load relative references on iPhone [38][39][40]; on Android a file manager hands Chrome a `content://` address whose relative video path fails [41][42][43]; embedding a 200 to 740 MB video in the page is not a real option. **W-30's "offline scrubber page on the USB" is demoted** to a laptop and TV companion; for her phone it is replaced by the film file itself, put on by cable.
12. **Recommended keepsake: P1 on her Android phone by USB cable (File Transfer mode, no cloud), plus a lock-screen still, with the chapter cards in the picture finding the chapters; the stick and an Android tablet in app-pinning mode are optional extras.** Scores out of 40: MP4 by cable 34; MP4 with chapter atoms 33 (but chapters are not honoured by phone players and ffmpeg's stream copy wrote an unmatched QuickTime chapter reference); dedicated device 32; USB-C drive 27; private page 22; PWA 21; HTML 20.
13. **Sharing: no route is allowed before the reveal.** After it: cable to her; AirDrop or Quick Share only from a device that already holds the file; relatives only after the ledger closes (W-48), as a WhatsApp **document** (2 GB limit; media is capped at 64 or 100 MB and recompressed, and only P2 fits that: 39 to 92 MB) [1][3]. A forward reaches five chats at a time [4], so every relative copy is a public distribution the rights log did not model: add a `phone_share` scope to T8 and a phone-sharing line to releases 4d to 4g. **Guests' phones: no QR code and no live media link on the night**; a spoken promise of a family copy after a named date, and at most a static page with no media, replaces it.
14. **Her phone is Android (D-31); on the Indian traffic evidence she is plausibly in the class the plan fears most, a 2019 to 2021 mid-range phone, 720p or 1080p, 20:9 (her model is unknown, O-43).** On a 720x1600 panel in landscape fit, the 1080p file is shown at 0.667 scale and a 4 px line is 2.7 device pixels; measured with an ideal scaler, P1 and the native-720p P2 are equally sharp (2 px lines 0.71 and 0.74, 3 px 1.08 and 1.10), so P2 earns its place on bytes, not sharpness (M); the phone's real scaler is UNVERIFIED. Her script is Gujarati: ffmpeg's `subtitles` filter before n9.0 shapes Indic text in simple mode and fails silently (measured: FreeSerif through 6.1.1 gives conjuncts unformed and viramas visible; the same font through n9.0.2 is correct, Q-F2b), so the shaping check in her script is a P-LOCK item that also checks the build.
15. **Hygiene is check 1, and it is wider than "turn off Google Photos".** Backup paths found today: Google Photos backup [12], Samsung Gallery sync to OneDrive (opt-in, digest only [51]), WhatsApp chat backup with "Include videos in chats" [7], and, for relatives' iPhones, iCloud Photos (which also blocks the Apple Devices photo sync [34]). Xiaomi's gallery cloud sync ended on 2022-10-25 for India [50], so it is no longer a risk but shows how these paths move. Project phones carry no accounts at all.

---

## Findings by question

### Q1. Phone realities by device class, and what that means for one phone master

**Device classes (all specifications read 2026-10-19 unless marked).**

| Class | Example | Screen | Peak brightness | Plays natively | Notes |
|---|---|---|---|---|---|
| A. 2019 to 2021 mid-range Android, low end | Redmi 9A (announced 2020-06-30, Android 10) [27] | 6.53 in IPS LCD, 720x1600, 20:9, about 269 ppi | 400 nits typical [27] | H.264 Baseline and Main decoders required from Android 3.0 and 6.0 [18]; High is universal in practice and is YouTube's own spec [20] (the High row was not in the page text I extracted: tested by the protocol) | LCD blacks are lifted; no HDR |
| A. mid-range Android, upper | Redmi Note 10 (announced 2021-03-04) [28] | 6.43 in Super AMOLED, 1080x2400, 20:9, about 409 ppi | 450 nits typical, 1100 claimed; **measured 475 manual, 682 auto** [29] | as above; YouTube sees HDR, Netflix reports SDR only on this phone [29] | HDR support differs per app on one phone |
| B. current Android | UNVERIFIED (specs not opened; the project phone decides) | usually 19.5:9 to 20:9, 1080 px tall | UNVERIFIED | H.264 High, HEVC | |
| C. iPhone of the last five years | iPhone 15 [19] | 6.1 in OLED, 2556x1179, 460 ppi, 19.5:9 | 1000 nits typical, 1600 HDR, 2000 outdoor [19] | HEVC, H.264, ProRes; HDR via Dolby Vision, HDR10+, HLG [19] | the 6.7 in sizes (2796x1290) are from memory: UNVERIFIED |
| D. her phone (D-31, O-43) | **Android** (make, model, version, storage, USB port: unknown) | unknown; on current evidence a class-A phone is the likeliest | unknown | H.264 High at least; the rest tested by the protocol | decision table K1 below |

**Market snapshot (StatCounter, September 2026, web traffic).** India mobile OS: Android 93.89%, iOS 6.05% [25]. Top six India mobile viewports (CSS pixels): 360x800 (15.28%), 393x873 (6.56%), 384x832 (4.16%), 385x854 (4.04%), 393x876 (3.67%), 360x804 (3.47%) [26]. Their aspect ratios are 2.167 to 2.233, that is 19.5:9 to 20:9, and none is 21:9. Date-stamp: 2026-09. Her phone is Android (D-31); iPhones matter only for relatives, and the 6% is the upper guess for them.

**Her likely screen, measured at its own scale (M).** A 720x1600 panel (the Redmi 9A class [27]) in landscape fit shows the picture at 1280x720 device pixels, so a 1080p file is scaled by 0.667 and a 720p file is shown 1:1. With an ideal bicubic scaler (the phone's real scaler is UNVERIFIED), contrast retained on the M-H1 chart: aligned 2 px line 0.71 for the master and P1, 0.74 for P2 shown natively; half-pixel 3 px 0.88 and 0.90; 4 px 1.05 and 1.08; hatch 3 px at 9 px pitch 0.97 and 0.99; through the 360p WA-STD proxy 3 px keeps 0.60 and 4 px 0.84 (CSV `roundtrip_contrast_720p_panel_2026-10-19.csv`). So **P1 and P2 look equally sharp on a 720p panel; P2's value is bytes**, and the 3 px and 4 px floors still hold (4 px at 1080 is 2.7 device pixels).

**Container and codec facts that matter.**
- Android: HEVC Main Profile **Level 3** is the mobile requirement (Level 4.1 only for Android TV) from Android 5.0 [18]. Level 3 is not a 1080p guarantee. Hardware on a 2019 to 2021 mid-range phone usually does more, but "usually" is not "guaranteed", and the project phone is where it is tested.
- Android streaming rule: for MP4, `moov` must precede `mdat` [18]: this is why `+faststart` is in the template. (A file copied by cable is not streamed, but a file opened from a chat or a link is.)
- HLG10 is required for user-generated HDR capture and playback, HDR10 for professional content [18]: HDR is a per-device, per-app matter.
- Browsers: HEVC is "partial" in Chrome from 107, Firefox from 137, supported in Safari and iOS Safari from 11 (caniuse, read 2026-10-19) [24]. Any web keepsake would have to use H.264.
- WhatsApp accepts 3GP, AVI, FLV, MKV, MOV and MP4 and warns that "high audio sample rate or professional cameras may be unsupported" [1]: 48 kHz AAC-LC is ordinary.

**What it means for one phone master.** H.264 High at level 4.1, 8-bit 4:2:0, SDR, BT.709, AAC-LC, `+faststart` is the only combination that every class plays from the gallery and every chat app accepts. It is also what YouTube asks for at 1080p24 SDR (H.264 High, BT.709, moov at the front, AAC-LC, **8 Mb/s**, stereo 48 kHz) [20], so P1's cap is not an invention. **UNVERIFIED and tested by the protocol (the chip is stated to play H.264 at 1080p 30 fps [66], with no profile or bitrate given):** whether H.264 High 4.1 plays from the gallery of a Redmi 9A; what WhatsApp's player does with a document-type MP4 on each OS.

### Q2. The encode ladder from the ProRes master

**Method and fixtures (M).** Three 12 s ProRes 422 HQ masters (10-bit 4:2:2, BT.709 tags, baked temporal grain): C1 a photo push (4% cosine push on a 4K texture, grain 3), C2 drawn flat-colour animation on twos with 4 px ink outlines, hatch, dots and a card line (grain 3), C3 the M-H1 chart panning at 0.5 px a frame (grain 7, worst case). Every encode is from the master. WhatsApp-class proxies are the two M-H1 stress levels (1280x720 at 2.5 Mb/s; 640x360 at 0.5 Mb/s): **they are not WhatsApp's encoder.** Details in `research/mobile-delivery-fixtures/README.txt`.

**Measured sizes (video bitrate includes container; audio added at 192 or 160 kb/s).**

| Clip | P1 Mb/s | P1 9 min / 12 min total | P2 Mb/s | P2 9 min / 12 min total | HEVC CRF 24 Mb/s |
|---|---|---|---|---|---|
| C2 drawn, grain 3 | 2.02 | 149 / 199 MB | 0.42 | 39 / 52 MB | 0.37 |
| C1 photo push, grain 3 | 2.71 | 196 / 262 MB | 0.86 | 69 / 92 MB | 0.59 |
| C3 dense lines, grain 7 | 8.48 (cap-bound; the 12 s sample includes the VBV start-up burst) | cap bound 553 / 737 MB | 0.70 | 58 / 78 MB | 0.36 |
| Cap bound | 8 Mb/s + AAC 192k | 553 / 737 MB | 4 Mb/s + AAC 160k | 281 / 374 MB | n/a |

CSV: `encode_ladder_sizes_2026-10-19.csv`. A real chapter will land between C2 and C3; **plan storage on the ceiling, expect a third of it.** One 12 s encode took 56 to 94 s with three jobs running on four cores (about 5 to 8 times real time under load): plan an hour per 12-minute P1 in the container; PC speed UNVERIFIED.

**CRF sweep (C2, 12 s; CSV `encode_ladder_sweep_2026-10-19.csv`).**

| Encode | Bytes | Mb/s | Grain survival in a flat paper patch (PR3 pass is 70%) |
|---|---|---|---|
| P1 CRF 16 | 12.7 MB | 8.4 (cap) | 89% |
| P1 CRF 18 | 6.3 MB | 4.2 | 89% |
| **P1 CRF 20** | **3.0 MB** | **2.0** | **73%** |
| P1 CRF 22 | 1.35 MB | 0.9 | 43% (fails) |
| P1 CRF 24 | 0.76 MB | 0.5 | 17% (fails) |
| P2 CRF 20, 720p | 0.88 MB | 0.6 | 27% |
| P2 CRF 23, 720p | 0.56 MB | 0.4 | 0% |
| HEVC CRF 18 | 1.19 MB | 0.8 | 27% |
| HEVC CRF 22 | 0.64 MB | 0.4 | 1% |
| HEVC `--tune grain` CRF 20 | 3.55 MB | 2.4 | 49% |

The CRF guide says plus or minus 6 halves or doubles the size and calls 18 to 28 the sane x264 range [22]; with baked grain the steps here are steeper, each +2 CRF cutting the bytes by 44% to 55% (3.03, 1.35, 0.76 MB) because the grain stops being coded. PSNR against the master barely moves across these rows (about 45 to 46 dB, dominated by the temporal grain), so **PSNR and SSIM do not rank these encodes; grain survival and line contrast do.** On the C3 worst case P1 kept 72% at the cap. Consequence for `cinematic-quality.md` PR3 ("flat-patch grain std after encode at least 70% of the master's", gate G6): P1 passes at CRF 20 and fails at 22; P2 and HEVC fail by construction and need either a per-file rule or an explicit "grain is not carried" note.

**Deriving from the venue file, measured (M).** Master to venue file (CRF 18, cap 20 Mb/s) to P1, against master to P1, both at CRF 20: PSNR 0.19, 0.53 and 0.14 dB lower (C1, C2, C3); bytes +19% (C1), +43% (C2), +0.2% (C3, cap-bound). P2 from the venue file: 0.20, 0.15 and 0.19 dB lower, bytes +14%, +9%, +9%. Grain survival in the flat patch was *higher* from the venue file (81% to 87% against 72% to 73%) because the second pass spends bits keeping the first pass's noise: more bytes, not a better picture. Line contrast was unchanged (previous table). The honest reasons to encode from the master are therefore bytes, a clean colour path, and that **the venue file has the venue captions in it**, so the phone captions could not be re-placed.

**Colour-patch test, the W-16 method on the new templates (M; twelve patches including near-blacks; ±3/255 rule).**

| Template | Worst channel error | Notes |
|---|---|---|
| P1 | 3/255 (cream, red -3) | at the limit; the rule is coarse |
| P2 | 2/255 | |
| HEVC | 2/255 | |
| bare `-pix_fmt yuv420p` from an RGB PNG, tags set to 709 | **23/255** (pure red, green +23) | the known BT.601 trap (agent-pipeline Q-F1) reproduced: the ladder starts from the YUV ProRes master, never from RGB frames, and any RGB step names `scale=out_color_matrix=bt709` |

ProRes in MOV reports `color_range=unknown` to ffprobe (M); the templates name `in_range=tv` explicitly. An identity `.cube` through `lut3d` placed ahead of the P1 filters kept every patch within 1.9/255 (plain `lut3d` on the 10-bit 4:2:2 master) and 2.0/255 (with explicit BT.709 conversions to and from RGB around it), so Trim P can be a `lut3d` step on ffmpeg 6.1.1; the PC build must repeat the test (W-16). CSV: `colour_patch_2026-10-19.csv`.

**Caption colour through the burn-in (M; first reading, then the round-1 re-run).** First reading, ffmpeg 6.1.1: white stayed 255,255,255; light grey E6E6E6 became 231; cream F3E9D2 became 242,232,219 (blue +9); red FF0000 became 255,21,0; ochre F0B323 became 249,174,24; the conclusion drawn was that libass converts ASS colours with the wrong matrix. **Round-1 re-run (twelve colours, four ffmpeg builds, `Follow-up research (round 1)` Q-F2):** the saturated colours reproduce on 6.1.1 (pure red 255,23,0; ochre 246,175,27; film red and green off by 12 and 14; worst 23/255) but **cream does not (242,230,208, within 3/255)**, so the "blue +9" reading is withdrawn. The cause is the source: n6.1.1's `subtitles` filter calls `ff_draw_init()` and the drawing code treats a YUV frame as BT.601; **from n7.0 it draws in the link's colourspace, and every colour is within 3/255 when the master is BT.709-tagged**; from n8.0 an `.ass` track's `YCbCr Matrix` header decides (missing or `TV.601` means BT.601 again, `None` or `TV.709` is correct). Rule: **caption text is white or neutral light grey by default; a tinted caption colour is allowed on a build that passes the twelve-patch caption test on the real master** (the PC build's run is UNVERIFIED); anything the test does not clear is a graphic (PNG or SVG overlay) with its own colour-patch row. The master's BT.709 tag is checked first (`ffprobe` `color_space=bt709`).

**Audio (M).** AAC adds true peak: a -1.0 dBFS sine measured -1.0 dBTP before and -0.7 dBTP after AAC-LC 192 kb/s; a hot square wave measured +1.1 dBTP before and +1.8 dBTP after. W-19's -1 dBTP is measured on the WAV. **Measure the final MP4** (`ebur128=peak=true`) and, if it reads above -1.0, re-encode with `volume=-0.5dB`. P1 and P2 audio: online row of W-19 (-16 LUFS integrated, -1 dBTP).

**Container hygiene (M).** All three encodes had atom order `ftyp, moov, free, mdat`, so `+faststart` worked. `-map_metadata -1` leaves only an `encoder` tag, `handler_name=VideoHandler` and the x264 or x265 SEI string; no title, no location, no creation time. With `-fflags +bitexact` the version numbers go too. Consequence: **a gallery that sorts by creation time may put the file at an odd position** (UNVERIFIED which gallery does what; the protocol records it). The thumbnail is a second hazard: a cold open that starts in black gives a black thumbnail (check 8).

**Is any HDR variant ever worth it? No.** (1) The master is SDR Rec.709 graded once (W-15, W-16); an HDR file would invent highlights and break "one grade". (2) HDR playback is per device and per app even on one phone (Redmi Note 10: YouTube HDR, Netflix SDR [29]); the Redmi 9A has no HDR panel [27]. (3) iPhones play HDR [19] but nothing in the plan needs it. (4) A phone's own enhancement modes are outside our control; the answer to them is the project-phone test, not a second grade.

**Is the HEVC P1 for her iPhone worth it? No.** The x265 default CRF is 28, VBV needs both `--vbv-maxrate` and `--vbv-bufsize` in CRF mode, and `--tune grain` switches on its grain-preserving rate control [23]; even so, the "saving" is the grain (table above); Android's mobile guarantee is Level 3 [18]; web support is partial [24]; her iPhone plays H.264 equally [19]. If the finished film has little or no grain (clean vector scenes), re-test; the template is in T-M1 for that case.

**Is the visual quality after one WhatsApp round-trip acceptable?** That cannot be measured here (nothing may be sent). On the proxies (M, static M-H1 chart, frame 36, contrast retained, 1.00 is full; L = landscape full screen, P = upright inline at 0.5625):

| Feature (at 1080p) | P1 L | master to WA-HD L | P1 to WA-HD L | P2 L | master to WA-STD L | P1 to WA-STD L | P1 P (upright) | P1 to WA-STD P |
|---|---|---|---|---|---|---|---|---|
| black line 1 px | 0.99 | 0.60 | 0.60 | 0.61 | 0.26 | 0.26 | 0.46 | 0.24 |
| line 2 px, half-pixel | 1.00 | 0.85 | 0.85 | 0.88 | 0.48 | 0.48 | 0.69 | 0.46 |
| line 3 px, half-pixel | 1.00 | 0.93 | 0.94 | 0.96 | 0.61 | 0.61 | 0.91 | 0.61 |
| line 4 px, half-pixel | 1.00 | 1.06 | 1.06 | 1.08 | 0.84 | 0.84 | 1.02 | 0.84 |
| hatch 1 px, pitch 3 | 1.02 | 0.49 | 0.49 | 0.52 | 0.00 | 0.02 | 0.37 | 0.02 |
| hatch 2 px, pitch 6 | 1.01 | 1.02 | 1.02 | 1.06 | 0.50 | 0.50 | 1.01 | 0.42 |
| hatch 3 px, pitch 9 | 1.01 | 1.12 | 1.11 | 1.13 | 0.87 | 0.87 | 1.12 | 0.84 |
| cream on indigo 2 px | 1.01 | 0.94 | 0.93 | 0.96 | 0.60 | 0.60 | 0.85 | 0.57 |
| cream on indigo 3 px | 1.01 | 1.09 | 1.08 | 1.09 | 0.86 | 0.86 | 1.02 | 0.79 |

Reading it: **a clean P1 is not where line art is lost; the 720p or 360p chat recompression is.** Going master to P1 to the proxy equals master to the proxy (columns 3 and 4, and 6 and 7). P2, already 720p, behaves like the WA-HD proxy. Upright inline view loses even the clean file's 2 px lines. Full CSV: `roundtrip_contrast_2026-10-19.csv`. **UNVERIFIED:** real WhatsApp, Telegram and Signal output (resolution, bitrate, frame rate, treatment of darks). The protocol measures it with `ffprobe` on two project phones, fixture content only.

### Q3. Legibility at arm's length

**Viewing distance.** Smartphone text is held at a mean of 36.2 cm for text messages (range 17.5 to 58.0) and 32.2 cm for web pages (19 to 60), n = 129 and n = 100 (Bababekova et al. 2011, abstract via search digest [30]). I use **35 cm as the design distance and 40 cm as the 50+ margin**; video distance is UNVERIFIED. Fluent reading needs an x-height of about 0.2° to 2° (Legge and Bigelow 2011, as cited in `research/cinematic-quality.md` Q10; the PDF returned 503 today and was not re-opened). The repo's TY1 applies a 1.5x margin to the 0.2° floor; for a 50+ viewer without reading glasses I use **0.30° as a hard floor and 0.35° as the target**.

**Measured caption geometry (M; ffmpeg `subtitles` on an `.srt`, Liberation Sans, 1080p; matches the earlier FQ1 x-height figures).**

| FontSize | x-height % of picture height | cap height % | line pitch % | 42-char line width | 36-char line width |
|---|---|---|---|---|---|
| 20 | 3.28 | 4.28 | 6.94 | about 66% | about 55% |
| **23 (W-18)** | **3.81** | **4.92** | **7.96** | **75% to 80%** | 67% |
| 26 | 4.26 | 5.56 | 9.07 | 85% to 90% | 76% |
| **28** | **4.64** | **6.03** | **9.72** | **91% to 97% (overflows the 90% box)** | **82%** |
| 30 | 4.92 | 6.42 | 10.46 | 98% to 100% | 88% |
| 32 | 5.28 | 6.87 | 11.11 | clips | 94% |

So **FontSize 28 holds at most about 36 to 38 characters a line**, FontSize 26 holds 42, FontSize 23 holds 42 comfortably.

**Cap heights and angles at 35 cm (computed from the published diagonal and pixel counts; CSV `caption_geometry_35cm_2026-10-19.csv`).**

| View | Picture height | FS 23 cap / x-height | FS 26 cap / x-height | FS 28 cap / x-height |
|---|---|---|---|---|
| 6.1 in, 19.5:9 (iPhone 15 geometry), landscape fit | 64.9 mm | 3.19 mm / 2.47 mm = **0.40°** | 3.61 / 2.76 = 0.45° | 3.91 / 3.01 = 0.49° |
| same, landscape fill | 79.1 mm | 3.89 / 3.02 = 0.49° | 4.40 / 3.37 = 0.55° | 4.77 / 3.67 = 0.60° |
| same, upright full width | 36.5 mm | 1.80 / 1.39 = **0.23°** | 2.03 / 1.56 = 0.25° | 2.20 / 1.69 = 0.28° |
| 6.7 in, 20:9 (2400x1080), landscape fit | 69.8 mm | 3.44 / 2.66 = 0.44° | 3.88 / 2.98 = 0.49° | 4.21 / 3.24 = 0.53° |
| same, landscape fill | 87.3 mm | 4.29 / 3.33 = 0.54° | 4.85 / 3.72 = 0.61° | 5.26 / 4.05 = 0.66° |
| same, upright full width | 39.3 mm | 1.93 / 1.50 = 0.25° | 2.18 / 1.67 = 0.27° | 2.37 / 1.82 = 0.30° |
| Redmi 9A 6.53 in, landscape fit | 68.1 mm | 3.35 / 2.59 = 0.42° | 3.78 / 2.90 = 0.47° | 4.10 / 3.16 = 0.52° |

At 30 and 40 cm the 6.1 in landscape-fit x-height reads 0.47° and 0.35° for FS 23, 0.58° and 0.43° for FS 28. **Does the venue caption pass at arm's length?** On size, yes in landscape (0.40° at 35 cm, 0.35° at 40 cm on the smallest screen). On position, no (next question). In the upright chat view, no at any size I can set without breaking the 16:9 design (0.35° at 35 cm needs an x-height of 5.4% to 5.9% of picture height, about FontSize 33 to 36, which does not fit 36 characters on a line). **The phone file therefore carries its own burn-in at FontSize 28 for margin, and the maker is told that sideways is the intended view.**

**Minimums for the phone file (the TY1 row of `cinematic-quality.md` gets a phone column).**

| Element | Venue floor (existing) | Phone floor (new) | Basis |
|---|---|---|---|
| Must-read type (chapter cards, titles, credits) | x-height 2.5%, font 5% | **x-height 3.2% hard floor, 3.8% target (41 px at 1080p; font about 7.3% of height in Liberation Sans)** | 0.30° and 0.35° at 40 cm on a 6.1 in landscape-fit screen (computed) |
| Captions | x-height 3.1% at 6 screen heights; FS 23 | **FS 28, white, outline 2, at most 36 characters a line, two lines; reading speed unchanged (20 cps, 2 lines, 5/6 s to 7 s per event [57])** | table above |
| Credits and the cue sheet | rolled or carded | **static cards, at least 4 s each, no roll; the full cue sheet goes in the archive and a printed or PDF page**, because rolling or sub-3.2% type cannot carry it | (J) |
| Meaning-bearing strokes | 2 px | **4 px; 3 px for decoration; dots 6 px; holes 4 px; hatch 3 px at 9 px pitch; no 1 px, no hairlines** | M-H1 and today's reproduction |
| Text contrast | none stated | **at least 4.5:1, large text 3:1 [53]; on a bright phone aim for 7:1 or better** | computed below |

**Contrast on the film's own palette (computed, sRGB relative luminance; "veil" is the reflection of the room, below).** Ink on cream 15.2:1; cream on indigo 11.3:1; ink on yellow 9.8:1; cream on red 5.3:1; cream on green 4.2:1 (fails 4.5, passes large text); **red on yellow 3.4:1 (large text only), ink on red 2.9:1 (fails even the 3:1 large-text rule), green on red 1.2:1 (fails; equal brightness).** The traditional red, yellow and green grounds therefore need cream or ink text chosen by luminance, not by hue. A 12.7-nit veil (500 lux, 8% reflectance) cuts ink on cream to 9.8:1 and cream on green to 3.8:1.

**Dark steps and the cold open (computed from [55][56]).** A phone screen reflects the room: veil = ambient illuminance x reflectance / pi. Uncoated glass reflects about 4% per surface [56]; an office is 320 to 500 lux, an overcast day 1,000, full daylight 10,000 to 25,000 [55]. Veil is **6.4 nits at 500 lux and 4%, 12.7 nits at 500 lux and 8% or 1,000 lux and 4%, 127 to 255 nits in daylight.** With white at 150 nits (about 50% on a phone that measures 475 nits at 100% [29]; the slider-to-nits curve is UNVERIFIED), the first 8-bit limited-range code that is at least 10% brighter than the veil-lifted black is:

| Room | Reflectance | Gamma 2.2 | Gamma 2.4 |
|---|---|---|---|
| 100 lux (evening) | 4% | 24.8 | 27.5 |
| 300 lux | 4% | 30.5 | 34.2 |
| 500 lux (bright kitchen) | 4% | 34.3 | 38.5 |
| 500 lux | 8% | 41.1 | 46.0 |
| 1,000 lux (by a window) | 4% | 41.1 | 46.0 |
| 1,000 lux | 8% | 50.3 | 56.1 |

(Full grid: `dark_steps_veil_2026-10-19.csv`; code 16 is black, 235 is white.) **Evening viewing needs no lift (W-15's working limit of 20 to 24 holds); a bright kitchen buries everything below code 34 to 46.** Venue Trim V is "lift 2 to 4 IRE, mid-gamma +0.05 to +0.10" (theatrical-delivery Step 4); **a Trim P starting value of about 4 to 7 IRE (9 to 15 codes) at codes 24 to 40, fading to identity by about code 100, black pinned at 16**, is the compromise between the two rooms. These are starting values (J); tune on the project phone with the dark-step page at 100 and 500 lux; do not let a lift show as banding in the dark gradient (M-C4 in `research/cinematic-quality.md`: an 8-bit dark ramp shows 26 levels against 100 at 10-bit).

**What decides the cold open (W-36).** Pinned black stays black on an OLED and shows as a dim grey mirror on a lit LCD; in both a viewer sees nothing and can think the file is dead. Two levers, both for the maker (the track proposes, `cinematic-quality` and `music-sound` decide): **(1)** a visible first light within about 4 s in both files (it costs the picture no re-edit if the cold open already has one; it is a design rule if not); **(2)** a first sound with energy above about 400 Hz (a spoon, a latch, a kettle, a pressure-cooker whistle rather than a low room rumble), at the level of the rest of the film; check with the tone ladder which tones this phone passes at 50% volume (small phone speakers roll off low frequencies; UNVERIFIED which tone). The sibling track's crude phone model (a 300 or 500 Hz high-pass) cost a CC0 temple bell 2.6 to 2.8 dB, a koel 0.0 to 0.1 dB and a conch 1.6 to 4.1 dB, but room ambience with people about 20 dB, on one sample each (`research/devotional-sound-script-fixtures/phone_speaker_model_2026-10-19.csv`); the bass cut-off of a phone speaker is "about 250 to 500 Hz" there (its source [87]): the cold open's room sound should lean on the bell, spoon and latch family, not the rumble.

### Q4. The fill-crop problem and the safe-area template

**Geometry (computed; CSV `fill_crop_2026-10-19.csv`).** A 16:9 picture scaled to cover a landscape screen of aspect A loses (1 - (16/9)/A)/2 of its height at the top and the same at the bottom.

| Screen | Crop top and bottom each | Visible height | Fit: bars each side |
|---|---|---|---|
| 18:9 | 5.6% | 88.9% | 5.6% |
| 19:9 | 7.9% | 84.2% | 7.9% |
| **19.5:9** (iPhone 15, Galaxy A series) | **9.0%** | 82.1% | 9.0% |
| **20:9** (Redmi 9A and Note 10, most India Android) | **10.0%** | 80.0% | 10.0% |
| 21:9 | 11.9% | 76.2% | 11.9% |

The central 80% is exact for 20:9 and loses 2 points a side at 21:9 (rare: none of the top six Indian viewports is 21:9 [26]). A 9:16 window cut from a 16:9 frame keeps 31.6% of the width; a 1:1 window keeps 56.3% (computed).

**What each player does (dated).**
- **YouTube:** fill is a user action. It added crop-zoom for screens wider than 16:9 in November 2017 (version 12.44) and the video "may crop some of the video"; Samsung's support page confirms the zoom needs a mismatched aspect ratio [31] (the Samsung page returned 403 on fetch; read from a search digest).
- **iOS and AVFoundation:** `resizeAspect` fits within the bounds, `resizeAspectFill` fills and crops (Apple Developer documentation, digest only) [32]. Which of the two Apple Photos, the TV app and WhatsApp use by default is UNVERIFIED; the round-1 read of Apple's documentation adds that `AVPlayerLayer.videoGravity` defaults to `resizeAspect` (fit) [68], a statement about the component, not about those apps.
- **VLC for Android:** has distinct fit and fill display modes (forum and code-review digests only; labels and default UNVERIFIED).
- **Android gallery, Google Photos, Apple Photos, WhatsApp and Telegram players:** UNVERIFIED (the AndroidX Media3 `PlayerView` defaults to fit [67], again a component default; no vendor page for the five apps was found, Q-F5). **The fill-crop card (`phone_test_p1_fillcrop.svg`) measures each:** read the first percentage visible at the top and bottom, in fit and in fill.

**The venue caption position, measured (M).** The W-18 box is 5% (54 px at 1080p). With ffmpeg's default `MarginV` (10 on the 288-line canvas), a two-line caption's descenders sit at y = 1041, **3.5% from the bottom: outside the box, and inside any fill crop.**

| MarginV | Bottom margin to descenders | Block top (FS 23, two lines) | Survives 20:9 fill (needs more than 10%) |
|---|---|---|---|
| 10 (default) | 3.5% | 81.9% | no |
| 15 (interpolated, not rendered) | about 5.2% | about 80% | no |
| 20 | 6.9% | 78.4% | no |
| 30 | 10.5% | 74.9% | barely |
| **35** | **12.2%** | 73.2% (FS 28: 70.0%) | yes |
| **40** | **13.9%** | 71.5% (FS 28: 68.2%) | yes, also at 21:9 (11.9%) |

**Template (fixture `research/mobile-delivery-fixtures/safe_area_template.svg`, 1920x1080 overlay).**
- *Venue file (W-18 unchanged except one number):* FontSize 23, **`MarginV` 20 or more** (bottom margin 6.9%, inside the 5% box); text inside the 90% by 90% box.
- *Phone file:* captions at FontSize 28, `MarginV` 40, two lines, at most 36 characters, block at 68% to 86% of height; **all must-read type and essential action inside the central 80% of height (10% to 90%), with a cushion: text box 5% to 95% across, 12% to 88% down** (the cushion is for rounded corners of about 5 mm, about 70 px at 1920 wide, and for player controls that appear on tap: assumption, UNVERIFIED).
- *Every file:* hands (W-33) and the object inside the central 80%; in a captioned shot, also out of the caption zone (venue 78% to 93%, phone 68% to 86%).
- *Shot brief fields for G2:* `phone_safe: {action_inside_central80, text_inside_phone_box, caption_zone_clear}` (booleans; the validator can compute the first two from the brief's boxes).

**Consequence under D-05.** The premiere cut has no recorded living voice except at most one HER-PUBLIC clip, so burned captions are few; the cards and credits are the text the phone has to carry. That is why the type floors above matter more than the caption position.

### Q5. Vertical and square companions

**Arithmetic (computed).** A full-height 9:16 window holds 31.6% of a 16:9 frame's width; a square holds 56.3%. The kitchen set, group photos and hands across a table (W-33, W-34) do not survive a 31.6% window without a recomposed shot.

**Cost model (J on the production-scale figures).** The Base model puts animation and compositing at **4.6 maker-hours per finished minute** and chapter passes at 1.2, finishing at 2.7 [`playbooks/production-scale.md`]. A vertical cut needs every shot recomposed (about 8 shots a minute, W-34: 72 to 96 shots), every card and credit reset for a 1080-wide frame, a second caption layout, a second review and master. At 25% to 50% of the animation time per shot (1.2 to 2.3 hours) plus a quarter of the passes and finishing (about 1 hour), that is **about 2 to 3.3 maker-hours per finished minute, 25 to 40 hours for 12 minutes, which is 9% to 14% of the 284-hour Base** (about two weeks at 16 hours a week). UNVERIFIED: how filmmakers actually deliver vertical versions (Adobe's Auto Reframe page returned 403; the usual practice of an automatic reframe pass with per-shot keyframes is general knowledge, not sourced here).

**Does it buy anything?** D-02 forbids a teaser before the reveal, so a vertical cut cannot be used for the reason vertical cuts usually exist (social promotion). After the reveal nobody has asked for one, D-24 says finish beats sprawl, and an art-directed 16:9 film reframed to 9:16 is a second film. **Confirmed: no vertical or square cut.** **One 9:16 (or 1:1) still keepsake** (a frame with the end-card line in her script, for her lock screen) costs about an hour. Rules: her handwriting only for words she wrote (W-35); no deity image on a lock screen (it sits under the clock and notifications and under thumbs; hindu-visual default P1 symbols only and R20); no swastika form unless the maker decides (hindu-visual 1.4); the script checked against a printed source (R19).

### Q6. Sharing routes (dated; all "before the reveal" cells are no)

Quality and limits come from the pages in Sources, read 2026-10-19. "Cloud copy under W-25" means a copy held by a service other than the maker's two encrypted drives.

| Route | Size limit | Recompression and effect on text and darks | Who holds a copy | Cloud copy under W-25? | Before the reveal | After: to her | After: to relatives before the ledger (W-48) | After the ledger |
|---|---|---|---|---|---|---|---|---|
| **WhatsApp as media** | default video limit **100 MB and 720p on a fast connection, 64 MB and 480p on a slow one** [1]; [3] itself says "64MB on all platforms" and, two lines later, the 100 MB and 720p default for a fast connection (all three pages re-read 2026-10-19 in a headless browser; excerpt saved): plan on 64 MB. HD is a per-message choice or a default under Settings, Storage and data, Media upload quality [2]; the pages give no pixel numbers for HD | always re-encoded; line art holds only at 4 px and above (proxies, above); darks UNVERIFIED | sender, recipient; WhatsApp servers while delivering: delivered messages are deleted, undelivered ones are kept encrypted up to 30 days, forwarded media stored temporarily [6]; **chat backup with "Include videos in chats" copies it to Google Drive, WhatsApp cloud storage or iCloud** [7] | transit: encrypted, temporary; **backup: yes** | **no** | not needed (cable first) | **no** | P2 only: 39 to 92 MB measured, under 100 MB in every case and under 64 MB only for the flat drawn content; P1 never |
| **WhatsApp as document** | **2 GB** [1][3][5], end-to-end encrypted [5] | WhatsApp points to Document for "longer or larger media" [3]; that it leaves the bytes unchanged is implied, not stated: **UNVERIFIED, test by comparing SHA-256 on two project phones**; how the recipient opens it (default player on Android, preview on iPhone) UNVERIFIED | as above; "Message yourself" is still a send | as above | **no, including to the maker's own second number (D-02, D-15)** | not needed | **no** | P1 or P2 as a document, once the ledger is closed and the maker says yes; forwarding to five chats at a time cannot be prevented [4]; a relative who re-forwards a forwarded item reaches one additional group chat by [4]'s text, and the copy still cannot be recalled |
| **Telegram** | **2 GB each, 4 GB with Premium** [8][9] (2022-06-19); "send without compression": UNVERIFIED (third-party only) | media compressed unless sent as a file (UNVERIFIED) | Telegram cloud: chats are stored encrypted on its servers [8] | **yes, persistent** | no | no | no | no unless the maker says yes to a persistent cloud copy |
| **Signal** | UNVERIFIED (site blocked); a third party gives 100 MB for files and Standard or High image quality | UNVERIFIED | UNVERIFIED | UNVERIFIED | no | no | no | UNVERIFIED; not a likely family route |
| **AirDrop** | none stated | original file (not stated on the page; UNVERIFIED); peer to peer | the two devices | no | n/a (no iPhone holds the film before the reveal) | yes, from a device that already holds it | no | yes; recipient must be Contacts Only or **Everyone for 10 Minutes**; from iOS 26.2 a non-contact needs an **AirDrop code** [13] |
| **Quick Share** (Android to Android, the natural nearby route for her phone; and Android to iPhone) | none stated | peer to peer, no server; the Android-to-Android case itself is UNVERIFIED (not on the page I read); works with AirDrop **only** when the iPhone is on "Everyone for 10 minutes"; launched on the Pixel 10 family 2025-11-20; availability on other makes UNVERIFIED [14] | the two devices | no | n/a | yes, same condition | no | yes |
| **Google Photos shared album or link** | 15 GB free per account [11] | **Storage saver resizes video above 1080p to 1080p**; Original quality unchanged [11] | Google | **yes** | no | no (her gallery backup is her call, Q7) | no | no unless the maker says yes |
| **iCloud Shared Albums** | albums created in iOS 26 or earlier: videos up to **15 minutes, delivered at up to 720p**, 5,000 items, items not counted against storage; albums created in iOS 27 or later: **original format and full resolution**, counted against the owner's storage, 100 subscribers (page published 2026-09-14) [10] | 720p on older albums | Apple; up to 100 subscribers | **yes, and a shared album is the charter's named "family cloud library" tip-off risk** | no | no | no | no unless the maker says yes |
| **Google Drive or OneDrive link** | Drive 5 TB a file [15] | none by the host; Drive previews are processed (UNVERIFIED) | Google or Microsoft; "Anyone with the link" works without signing in, and viewers can download unless the owner turns it off [16] | **yes** | no | no | no | no: hosting is allowed only after W-48 with the maker's explicit yes, and it adds forwarding of the link |
| **Email** | Gmail 25 MB; larger is replaced by a Drive link [17] | n/a | provider, recipient | yes | no | no | no | no |
| **Cable** (Android MTP; iPhone from the PC) | storage only | none | her phone, the PC | no (unless her gallery backup is on) | n/a | **yes, the primary route** | n/a | n/a |
| **USB-C drive into her phone** | exFAT or FAT32; a P1 of at most 737 MB is far under FAT32's 4 GiB | none | the drive | no | n/a | yes | n/a | n/a |

**What it means for Tier B stills (W-46, W-47).** After the reveal, one relative forwarding the file is a public distribution the rights log did not model: Tier B stills of relatives who have not yet signed travel with it. **Her copy is one copy on her phone; relatives' copies wait for the ledger (W-48).** Add to T8 a `phone_share` column (values `none`, `her_device_only`, `relatives_after_ledger`, `public`) and to releases 4d to 4g a line: "[ ] a copy of the film on my relatives' phones, sent by WhatsApp or similar; I understand a forwarded copy cannot be recalled" (4e adds: "a copy on my phone and in my phone's backup account").

### Q7. Keepsake options for a 50+ viewer with no precision gestures

**Evidence that decides the HTML options.**
- **iPhone:** Files' Quick Look is "the closest option and it will not run JavaScript"; since iOS 18.5 Safari and Firefox no longer open HTML files directly (Apple Community answer, July 2025) [39]. The Files preview of a local page shows the text and inline CSS but **does not load relative references** (Apple Developer Forums, July 2022) [38]. A standalone HTML player export shows a blank page in the iOS Files preview, the author suspects scripts are not run, still open on 2026-10-08 [40].
- **Android:** a page opened from a file manager gets a `content://` address; relative links then fail with ERR_FILE_NOT_FOUND on Android 10 and later; `file:///sdcard/Download/page1.html` worked on Android 10 and not on Android 11 (MIT App Inventor thread, 2021) [41]. Local video in an HTML page fails on Android through relative paths; the workarounds were a file picker or a local server (TiddlyWiki forum, 2022-06-01) [42]. Firefox for Android has an open feature request for this (Bugzilla 1809954) [43]. Chrome-specific current behaviour on Android 14 and later is UNVERIFIED.
- **Self-contained is not feasible:** inlining 199 to 737 MB of video as base64 makes the page 270 to 980 MB and needs the browser to hold it.

**Scores (1 to 5, five is best; effort 5 = least effort, risk 5 = lowest risk).**

| Option | Works offline | Works on her phone | No cloud | One tap | Large text | Revisitable | Effort | Risk | Total /40 |
|---|---|---|---|---|---|---|---|---|---|
| (a) **MP4 by cable into the gallery** | 5 | 5 | 4 | 5 | 3 | 4 | 4 | 4 | **34** |
| (b) MP4 with chapter atoms | 5 | 5 | 4 | 5 | 3 | 4 | 3 | 4 | 33 |
| (c) Self-contained HTML from `timeline.json` | 3 | 1 | 5 | 2 | 4 | 2 | 2 | 1 | 20 |
| (d) PWA | 2 | 3 | 1 | 4 | 4 | 3 | 2 | 2 | 21 |
| (e) Private page behind Cloudflare Access, after W-48 | 1 | 4 | 1 | 2 | 4 | 5 | 3 | 2 | 22 |
| (f) Dedicated preloaded device (a tablet or spare phone), airplane mode, one icon | 5 | 3 | 5 | 5 | 5 | 4 | 2 | 3 | 32 |
| (g) USB-C drive into her phone | 5 | 3 | 5 | 2 | 3 | 3 | 3 | 3 | 27 |

Why each score, in one line.
- **(a)** Plays everywhere (Q1); "no cloud" is 4, not 5, because if her gallery backs up to Google Photos or iCloud the file is uploaded the moment it lands (Q8). **Android (her phone, D-31):** USB File Transfer mode, drag to the phone [37] (UNVERIFIED on the PC); a Quick Share from the maker's own Android project phone is a second route (Android to Android specifics UNVERIFIED; [14] documents only the Pixel-to-AirDrop case). **iPhone from Windows (relatives only):** Apple Devices app, Files, drag onto an app that supports file sharing (for example VLC) [33], then tap it in that app; or Photos, "Sync Photos from folder", "Include videos", which is **unavailable while iCloud Photos is on** [34]. Movies sync needs the Apple TV app on the PC and does not mention home videos [35]; Home Videos in the TV app is UNVERIFIED.
- **(b)** ffmpeg's MP4 muxer writes both Nero chapter markers and a QuickTime chapter track by default [21]; a stream-copy remux here wrote three readable chapters but ffprobe warned "Referenced QT chapter track not found" (M). QuickTime Player shows chapters [47]; the Music and TV apps on iOS "do not appear to support" them [46]; VLC desktop reads them (search digest); Android gallery and Apple Photos behaviour UNVERIFIED. **Keep chapter atoms out of P1; put them in the archive and the VLC copy only.** The cards in the picture (W-04) are her chapter menu.
- **(c)** Fails on the iPhone and is unreliable on Android (evidence above). **Demote.**
- **(d)** A PWA is installable only over HTTPS or localhost [45], so it is a hosted link; Safari deletes script-writable storage, including Cache API and IndexedDB, after seven days without use unless the app is on the home screen [44]; a 200 MB offline video in a cache is not a keepsake. **Demote.**
- **(e)** A good relatives' route later, not hers: email-code login is a typing task, a hosted copy before the ledger closes is forbidden by W-48, and the Free plan's 50-seat limit is read from `playbooks/format.md` (read there on 2026-10-18; not re-read today).
- **(f)** The strongest accessibility option: Android **app pinning** (Settings, Security, App pinning; you need her PIN, pattern or password to unpin; Pixel steps need Android 11 or later) [49] makes one app with one visible control on her phone or on an Android tablet; iPhone **Guided Access** (triple-click the side button; circle areas to ignore touch; or turn Touch off) [48] is the equivalent for a relative's iPhone. Older adults in a 40-person study often preferred tablets because of eyesight decline [54]. It is a device, not her phone, so it does not meet D-27 alone. Cost UNVERIFIED (O-04).
- **(g)** iPhone 15 and later accept a drive with one partition in exFAT, FAT32, FAT, APFS or HFS+ and show it in Files (digest of the Apple page) [36]; Android needs OTG support, which varies by phone (GSMArena lists the Redmi 9A with microUSB 2.0 and OTG [27]; her phone's port is unknown, O-43). Four steps (adapter, plug, Files, tap) are not "one tap".

**Recommendation (confirms, replaces or demotes W-30's "offline scrubber page on the USB" at G-SLICE, Sun 20 Dec, O-30).**
1. **Replace** the phone-facing companion with **(a): P1 on her Android phone by USB cable**, with a lock-screen still and her chapter cards in the picture. The maker does the cable step on reveal weekend with her yes, on her phone.
2. **Demote** the scrubber page: keep it only as a desktop or laptop companion (OpenMAIC's note says its HTML works over `file://` in desktop browsers [40]) and the archive; do not promise it for her phone.
3. **Keep the USB stick** as the archive and TV carrier (P1 beside the venue file), and as rung 3 of the premiere failure ladder.
4. **Offer (f)** (an Android tablet with app pinning) as the premium keepsake if the budget and her devices say so (O-04, O-43).
5. **Her phone's own backup is hers to decide.** If her gallery backs up to a cloud account (on Android most likely Google Photos [12]), first ask whether "Back up all device folders" is on (the app-folder route is safe only if it is off; if on or unknown, use the tablet or the stick), then put P1 in an app's own folder (VLC's) at the reveal and raise the question again in the her-turn conversation (Sat 6 Mar), because a camera-roll copy becomes a cloud copy at once and, if her library is shared, visible to relatives before the ledger closes (W-48).

### Q8. Guests' phones at the premiere, and test-phone hygiene

**A QR code to a private replay: what it exposes.** (1) A hosted copy before the ledger closes, which W-48 forbids. (2) Uncontrolled copies: the link goes to every guest including strangers (W-54), and a download is one tap [16]. (3) Tier B stills of relatives who have not signed, and her likeness, in strangers' galleries. (4) A QR printed on anything that can be scanned before the reveal. (5) A forward reaches five chats at a time [4].

| Option | Exposes | Verdict |
|---|---|---|
| QR to a private replay | all of the above | **no** |
| QR to a static thank-you page, no media | the page address only | allowed at most, plain and quiet; no ornament (see Exclusions) |
| No QR; a spoken line in the welcome ("a copy for the family follows after [named date]"; a guest asks, you answer later) | nothing | **default** |
| Ask guests not to film the screen | nothing | add to the 30 to 60 s welcome; `playbooks/surprise-ops.md` Step 11 already says phones are silent and the room, not her, is filmed |

**Confirmed: no live media link or QR on the night.** The printed book in surprise-ops Decision 15 may carry static QR codes only; the lean "a book whose chapters can be found without any QR code" stands.

**Hygiene (check 1 of the protocol).** The failure paths found today:
- **Google Photos** backup (Photos settings, Backup) uploads new media, and it covers "your chosen device folders ... not only your camera", with a "Back up device folders" screen and a "Back up all device folders" switch (re-read 2026-10-19 [12]). The page advises deleting already backed-up items on photos.google.com; that turning backup off leaves them in place is an inference. The page lists no default folders (Q-F3).
- **iCloud Photos** (iPhones only, so relatives' phones and any iPhone project phone) keeps the camera roll in iCloud (general knowledge; the Apple page I read says only that, with it on, the Apple Devices app offers no photo sync at all [34]).
- **The phone manufacturer's gallery sync (Samsung Gallery to OneDrive; others UNVERIFIED)**: the Samsung one is opt-in and needs a Samsung and a Microsoft account (digest only [51]).
- **WhatsApp chat backup** copies media to Google Drive, WhatsApp cloud storage or iCloud; "Include videos in chats" decides whether videos are in it [7].
- **"Send as document to myself"** puts the file on WhatsApp's servers during delivery [6].
- **Xiaomi** ended Gallery sync to its cloud on 2022-10-25 (India in the first group; data deleted 2023-08-01) [50]: no longer a risk, and a reminder that these paths move. Other makers' clouds (Oppo, Vivo, Realme, OnePlus): UNVERIFIED; check Settings for any account or cloud toggle.

**Rule: project phones are devices with no accounts at all** (no Apple ID, no Google account, no Samsung or Microsoft account, no WhatsApp for any slice or family frame), airplane mode for tests, location off. The maker's own phone is not a project phone: it is probably inside the family's cloud and backup arrangements, which is the tip-off the charter names. Two P-LOCK additions: **an Indic caption burned in on the PC with correct shaping**, and **the project phone playing the slice fixture from its gallery.**

**Indic shaping, a measured warning in her script (M; corrected in round 1).** Rendering the Gujarati test line `ક્ષત્રિય જ્ઞાન ધર્મ કિ ક્ષિ` (kṣatriya "the warrior order", here only a conjunct test; jñāna "knowledge"; dharma; ki and kṣi, which test the short-i sign) through ffmpeg 6.1.1 (libass with HarfBuzz) with FreeSerif, the only Gujarati-capable face in this container, produced **no error and wrong text**: conjuncts not formed, viramas visible, the reph standing alone, the short-i matra after the consonant instead of before it (`gujarati_shaping_freeserif_2026-10-19.png`, top row). The same happened to the Devanagari line `श्री क्षत्रिय ज्ञान` (the honorific śrī and two test words) with FreeSans (`indic_shaping_freesans_2026-10-19.png`). **The first pass blamed the fonts; the round-1 re-run shows the build was the cause:** the same `.srt` and the same font through ffmpeg n9.0.2 are shaped correctly (the picture's bottom row; ink width 1172 px against 1597 px for the Gujarati line), because the `subtitles` filter of ffmpeg before n9.0 shapes in simple mode (the sibling's finding; Q-F2b). The sibling's named tells ("visible halant", "standalone reph", "unmoved i-matra") are exactly what the top row shows, and its fonts (Noto Sans Gujarati, Hind Vadodara, Mukta Vaani) were checked with HarfBuzz and libass. The check is visual, on the PC, with the chosen OFL font, and it joins P-LOCK; **it also checks the PC build** (a `subtitles` filter older than n9.0 shows the top row whatever font is chosen). The earlier exhibit carried a first line that was a deity's invocation rendered wrongly; it was removed so that no sacred text is kept as a broken exhibit (review round 1, section 2).

### Q9. Accessibility for a 50+ viewer

- **Text:** the floors in Q3 (x-height 3.2% hard, 3.8% target, captions FS 28); captions burned in so she never has to find a switch; a clean copy only for the archive. An HTML keepsake that survives would respect the phone's text-size setting; none survived, so this is moot.
- **One-tap play:** the file opens from the gallery thumbnail with one tap; **set the thumbnail deliberately** (a black cold open gives a black thumbnail; check 8), and name the file in her language or with a neutral code name before the reveal.
- **No pinch, no scrub precision, a visible pause:** the stock players give a tap-to-pause and a scrub bar; the film is designed to be watched without scrubbing (cards, not a menu). **WCAG 2.2 2.5.5** asks for targets of at least 44 by 44 CSS pixels to help people with tremor or limited dexterity [52]; a 40-person older-adult study found swipes, double-taps and drag gestures failed in practice and asked for simple, well-placed buttons and a text-size option [54] (qualitative, no numbers).
- **Kiosk mode:** Android app pinning for her phone or an Android tablet, Guided Access for a relative's iPhone (Q7).
- **Sound:** the tone ladder finds her phone speaker's low cut; speech and the first sound must sit above it; earbuds as a second pass.

### Q10. What changes, and where it changes (decision tables keyed on the unknowns)

The maker has not yet said her phone, her backup state, her language or how she holds the phone. These tables light up when O-36 to O-43 arrive.

**K1. Her phone and her backup, to the hand-over route (reveal weekend, with her yes).**

Her phone is Android (D-31): the first three rows are hers; the iPhone rows are for relatives after the ledger.

| Phone | Cloud photo backup | Route | Do not |
|---|---|---|---|
| **Android (hers)** | Google Photos backup on, or the phone manufacturer's gallery sync on (Samsung Gallery to OneDrive; others UNVERIFIED) | **First question, at the reveal-weekend check and in the her-turn conversation (Sat 6 Mar): is "Back up all device folders" on?** Google's page says backup covers "your chosen device folders ... not only your camera" and that with the switch on "photos in new device folders automatically back up" [12]. **The app-folder route is safe only if the switch is off.** Off: USB File Transfer [37] into a folder her backup is not set to read, or an app's own folder such as VLC's (whether another app's private `Android/data` folder counts as a device folder is UNVERIFIED). On or unknown: the Android tablet or the stick, or, with her yes, switch that folder off in "Back up device folders" before the copy. Which folders each skin turns on by default is not documented (Q-F3) | drop it in DCIM/Camera, the folder backup reads by default (UNVERIFIED default) |
| **Android (hers)** | off | USB File Transfer [37] into Movies; tap in the gallery | |
| **Android (hers)** | unknown at reveal | treat as on, and treat "Back up all device folders" as on; do not look at her phone beforehand (D-02); ask O-43 and the backup question first; at the reveal check, with her yes, look at the switch together before any cable copy | guess |
| iPhone (a relative) | iCloud Photos on | Apple Devices, Files, drag onto VLC [33] (needs the App Store); Photos sync is unavailable [34] | Save Video to Photos |
| iPhone (a relative) | iCloud Photos off | Apple Devices, Photos, Sync from folder, Include videos [34]; or the VLC route | |
| Android with OTG, or iPhone 15 or later | any | the USB stick as a second copy | rely on it as the only route |

**K2. Her language and script: Gujarati (D-31), to the caption and type sizes.** Latin (the room's language): FS 28, 36 characters a line. Gujarati has no headline and no true x-height, so I use the height of the base letter KA as the analogue (the sibling track's working analogue, inference). Through the same `subtitles` filter at FontSize 23 the sibling measured KA at **3.52% of picture height in Hind Vadodara, 3.33% in Noto Sans Gujarati, 2.96% in Mukta Vaani**, and a 44-code-point Noto Sans Gujarati line at 54% of the frame (`caption_size_FontSize23_*.csv`, `caption_width_FontSize23_*.csv`; one sample sentence each). To reach my phone target of 3.8% the FontSize is 23 x 3.8 / KA: **24.8 (Hind Vadodara), 26.2 (Noto Sans Gujarati), 29.5 (Mukta Vaani)**; for the 3.2% hard floor 20.9, 22.1 and 24.9. At those sizes a 36 to 44 code-point Gujarati line is not width-limited (Noto Sans Gujarati at FontSize 28 is about 66% of the frame). Her script belongs on the title and verse **cards** as shaped outlines, with the room-language captions underneath (sibling Template L3), so the phone burn-in is mostly the room's language. **Noto Sans Gujarati is the default caption face (FontSize 26.2 for the 3.8% target, 22.1 for the floor)**: the sibling's Q9 Gujarati paragraph found that Hind Vadodara has no Gujarati digits (U+0AE6 to U+0AEF), so any date or year (સંવત ૨૦૮૩) falls back to FreeSerif, while Noto Sans Gujarati carries digits, the Om sign and every conjunct string it shaped (`research/devotional-sound-script.md` Q9 and font table). Hind Vadodara (24.8) stays an alternative for lines without digits. Both are SIL OFL 1.1 with no Reserved Font Name (github.com/google/fonts `ofl/hindvadodara/OFL.txt` and `ofl/notosansgujarati/OFL.txt`, read 2026-10-19). Shaping test first (Q8). Other scripts (Devanagari for Sanskrit verses, others) per the sibling's CSVs: size by base-letter height, not FontSize.

**K3. How she holds the phone (V7 in hindu-visual), to the design rule.** Sideways: landscape-fit design, size floors in Q3. Upright in a chat: the picture is 36.5 mm tall; nothing in the film is legible at 0.35°; the hand-over must say "turn it sideways" (a 3 s rotate card is a creative call, not recommended).

**K4. Relatives' phones, to the file.** Storage under 3 GB free or slow data: P2 (39 to 92 MB). Otherwise P1 as a document (199 to 262 MB typical). Never media; never HEVC.

**K5. Where the premiere is (O-02, O-44), to the sharing rule.** Unchanged: no live link on the night; WhatsApp document after the ledger; the venue may have a policy on filming (ask in the room brief, W-52, access times only).

---

## Exemplars and what they teach us

| Exemplar | What it shows | What we take |
|---|---|---|
| **YouTube's recommended upload settings** [20] | the de-facto cross-device H.264 spec: High profile, BT.709, 8 Mb/s at 1080p 24 to 30 fps SDR, AAC-LC, moov at the front | P1's cap of 8 Mb/s and its tags are the industry's own safe numbers |
| **YouTube crop-zoom for tall phones (2017)** [31] | fill is a viewer's choice introduced for screens wider than 16:9 | design for the crop; do not assume it |
| **Apple's Shared Albums change (page published 2026-09-14)** [10] | limits are tied to the OS version of the album's creator: 720p and 15 minutes in iOS 26 and earlier, original resolution in iOS 27 and later | date-stamp every limit; test on the real versions; never plan around a platform's lowest-quality path |
| **OpenMAIC issue 1847 (opened 2026-10-08)** [40] | a standalone HTML export shows a blank page in the iOS Files preview; the fix under discussion is a static fallback and a documented, tested opening method | "self-contained HTML opens everywhere" is false on iPhone; a keepsake must be tested on the device or dropped |
| **Xiaomi's end of Gallery cloud sync (2022-10-25; data deleted 2023-08-01)** [50] | vendor clouds appear and vanish, and ship with default behaviours | no cloud is a keepsake; hygiene checks are re-run, not assumed |
| **WhatsApp's own advice: send longer or larger media as a Document** [3] | the platform's escape hatch is the route a 200 to 740 MB film must take | the only chat route is the document route, after the ledger |
| **Guided Access and Android app pinning** [48][49] | the platform's own "one app, ignore touches" modes | the "grandmother mode" for a dedicated device |
| **`research/hindu-visual.md` M-H1 and its chart** | a fixture and a harness description that this track rebuilt and extended | reproduced within 0.02; extended to double-encode, HEVC and P2 chains |

---

## Templates and deliverables

### T-M1. Phone deliverable spec: the encode ladder (templates ran in the container on 2026-10-19; Windows UNVERIFIED)

Source for every file: the ProRes 422 HQ master (W-15). Never the venue file, never RGB frames. Run the W-16 colour-patch test on each template on the PC build.

```
# P1 phone master (hers; relatives' phones as a document after the ledger)
ffmpeg -i MASTER.mov -map 0:v:0 -map 0:a:0 ^
 -vf "[lut3d=trim_p.cube,]subtitles=phone.srt:force_style='FontName=<OFL font>,FontSize=28,MarginV=40,Outline=2,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,WrapStyle=2',scale=in_range=tv:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int+bicubic,format=yuv420p" ^
 -c:v libx264 -preset slow -crf 20 -maxrate 8M -bufsize 16M -profile:v high -level:v 4.1 -pix_fmt yuv420p ^
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -g 48 ^
 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -map_metadata -1 -fflags +bitexact LJ_P1_<code>.mp4
```
(The bracketed `lut3d` step is used once Trim P is signed; it comes before the captions so the trim never touches the type. Without a `phone.srt` the subtitles filter is dropped. The combined line, with an identity cube and the phone captions, ran in the container on a 3 s clip on 2026-10-19 and probed as High, level 41, yuv420p, tv, bt709, 72 frames (M). On Windows run in the working folder with relative names.)

```
# P2 small copy (low-storage phones; document route)
 -vf "[lut3d=trim_p.cube,]subtitles=phone.srt:...,scale=1280:720:in_range=tv:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p"
 -c:v libx264 -preset slow -crf 22 -maxrate 4M -bufsize 8M -profile:v high -level:v 3.1 -pix_fmt yuv420p <same tags> -g 48 -c:a aac -b:a 160k ... LJ_P2_<code>.mp4
```
P2's captions are burned on the 1080 frame before the downscale; re-check the type floor at 720 (x-height 3.8% is 27 px).

```
# HEVC variant: NOT RECOMMENDED (grain loss); template only for a grain-free finish
 -c:v libx265 -preset medium -crf 18 -x265-params vbv-maxrate=6000:vbv-bufsize=12000:keyint=48 -pix_fmt yuv420p -tag:v hvc1 <same tags> ...
```

| Check (run on every output) | Pass | Source |
|---|---|---|
| `ffprobe`: `codec_name=h264 profile=High level=41 pix_fmt=yuv420p color_range=tv color_space=bt709 color_transfer=bt709 color_primaries=bt709 r_frame_rate=24/1`, frame count = timeline | equal | theatrical-delivery Step 8 |
| Atom order | `ftyp, moov, ..., mdat` | M |
| Master tag, before any burn-in | `ffprobe` shows `color_space=bt709` on the ProRes master (an untagged master makes every ffmpeg build draw captions in BT.601: 23/255 on saturated colours) | Q-F2, M |
| Colour patch (twelve patches) | ±3/255 | W-16, M |
| Final-MP4 true peak | ≤ -1.0 dBTP, loudness -16 LUFS | W-19, M |
| Grain survival, flat patch (P1 only) | ≥ 70% of the master | PR3, M |
| Type floor and strokes | Q3 table | M-H1 |
| Safe-area overlay composited on three frames | all pass | T-M3 |
| Metadata | no title, comment, location; hash in the manifest | Step 8 |
| File name | neutral code before the reveal | W-17 |

### T-M2. Text, stroke and contrast minimums (the Q3 table, as a checklist)

Must-read type x-height ≥ 3.2% (target 3.8%); captions FS 28, ≤ 36 characters, two lines, white; no scrolling credits; strokes 4 px (3 px decoration, dots 6, holes 4, hatch 3 at 9 px); contrast ≥ 4.5:1 (7:1 target); text on red or green grounds in cream or ink chosen by luminance; no hairlines; no tinted caption text.

### T-M3. Safe-area template and shot-brief fields

File: `research/mobile-delivery-fixtures/safe_area_template.svg`. Fill-crop card: `phone_test_p1_fillcrop.svg`. Brief fields: `phone_safe`, `hands_box`, `object_box` (pixels at 1080p), `caption_zone: none | venue | phone`. G2 composites the overlay on three frames per shot.

### T-M4. Sharing-routes table

In Q6 (columns: route; limit; recompression; holder; cloud copy; before; to her; relatives before the ledger; after the ledger; date read 2026-10-19). Tested-on-project-phone column to be filled by protocol check 9.

### T-M5. Keepsake options matrix with recommendation

In Q7 (scores and the five-point recommendation).

### T-M6. Phone test protocol (thirteen rows; one device, under 60 minutes; run on each class)

**Devices (her phone is Android, D-31, so the Androids come first).** (1) an old mid-range Android with a 720p screen (Redmi 9A class), (2) an Android with a 1080p screen (Redmi Note 10 class), (3) a current Android, (4) an iPhone of the last five years, for relatives only, (5) optionally a 6.7 in phone. **Her phone is tested only after the reveal, with her yes.** Project phones carry no accounts.

| # | Check | How | Pass | On fail |
|---|---|---|---|---|
| 1 | **Hygiene (first, 10 min)** | no Apple, Google, Samsung or Microsoft account signed in; Google Photos and iCloud Photos off or absent; WhatsApp absent (or installed with fixture content only); airplane mode; location off; brightness 50%, auto-brightness off; room 300 to 500 lux (a free lux app, accuracy UNVERIFIED); screen mode set to Natural or Standard and recorded | every box ticked in writing | stop; no media goes on the phone |
| 2 | **Copy by cable** (5 min) | Android: File Transfer [37]; iPhone: VLC file sharing [33] (UNVERIFIED on the PC) | file present, hash equal | fix cable or app |
| 3 | **One-tap play** | tap the thumbnail; sound on | plays at once; seek works (faststart) | re-encode with `+faststart`; check atom order |
| 4 | **Fill-crop card** (per player: gallery, Google or Apple Photos, VLC, and Telegram or WhatsApp if installed with fixtures) | landscape; fit, then fill by tap or pinch; read the first visible percentage top and bottom | recorded; crop 9% to 10% expected | none: record into the template; if more than 12%, move text higher |
| 5 | **Caption burn-in** (venue and phone variants of the 20 s card) | read both captions at 35 cm, then at **50 cm as a proxy for a 50+ viewer**, fit and fill | phone caption fully visible and readable at 50 cm in fit and fill; venue caption cut in fill (expected) | raise `MarginV`; or enlarge FontSize |
| 6 | **Dark steps** (page 2), on a clean file and on a Trim P file | find the first patch you can tell from code 16, at 100 lux and at 500 lux | both codes recorded; with Trim P, picture detail that must be seen sits at or above the 500 lux code and the 100 lux room does not look milky | adjust Trim P |
| 7 | **Strokes and colour** (page 3 chart) | 3 px lines visible, 4 px crisp, hatch 3 px/9 px visible, equal-brightness pair noted | pass | enlarge strokes in the art |
| 8 | **Gallery thumbnail and sort position** | look at the file in the gallery list | thumbnail not a dead black frame; sorted where expected (stripped metadata) | set a poster frame or first light; set `creation_time` |
| 9 | **Chat round trip, fixture only** (optional, two project devices): document and media | WhatsApp document: SHA-256 before and after; media: `ffprobe` the received file (resolution, bitrate, fps) | document hash identical; media numbers written to the routes table | if the document changes, it is not a lossless route |
| 10 | **Sound** | tone ladder 100 Hz to 3.2 kHz at 50% volume in a quiet room; then pink noise; then earbuds | speech band (400 Hz to 3 kHz) clearly audible; lowest audible tone written down | move the cold-open sound up in frequency; raise the first cue |
| 11 | **Gujarati caption shaping on the PC** (P-LOCK) | burn the Gujarati strings of the sibling's `shaping_fixture.srt` (ids guj-shri, guj-ksha, guj-jna, guj-dharma, guj-om) with the chosen OFL font (Noto Sans Gujarati is the default caption face; Hind Vadodara fails the digits string) through the subtitles filter; read the libass log lines the sibling's README names | conjuncts formed, reph and matra placement correct; no visible virama (compare the two-row `gujarati_shaping_freeserif_2026-10-19.png`: top row the failing 6.1.1 build, bottom row the correct n9.0.2 build; if the PC shows the top row, the build is older than n9.0) | change font or renderer; `drawtext` is out on any ffmpeg older than n9.0 (sibling Q10) |
| 12 | **Slice fixture from the project phone's gallery** (P-LOCK) | copy the slice fixture; play | plays with sound at one tap | per rows 2 and 3 |
| 13 | **Scrubber page from the file manager and from Files** (measures the demotion of W-30's page) | open the scrubber page (the slice fixture's page, or a stand-in page with a relative-path video) from the project Android's file manager and from Files on the iPhone; record whether the video plays | recorded for both platforms. If it plays on both, the laptop companion gains a phone fallback for free; if not, the demotion stands, now measured | none: keep the demotion; note the Android version, the browser and the iOS version |

**Evidence:** a photograph of the screen for each row (fixture content only). **Time:** rows 1 to 8 and 10 take about 45 minutes per device once practised; row 9 is the extra; row 13 is about two minutes. Each fail names the fix.

### T-M7. Guests' phones decision

In Q8: no QR, no live link; a spoken promise of a family copy after a named date; a plain static page at most.

### T-M8. Rights-log additions

T8 gains a `phone_share` column (`none | her_device_only | relatives_after_ledger | public`). Releases 4d to 4g gain the line quoted in Q6. TD-9 (new): "Phone deliverable: P1 by cable to her phone on reveal weekend with her yes; P2 to relatives as a WhatsApp document only after the ledger closes (W-48) and the maker says yes."

### T-M9. Vertical cost model (Q5), and the lock-screen still

About 2 to 3.3 maker-hours per finished minute for a vertical cut (25 to 40 hours for 12 minutes; not recommended); about 1 hour for one still.

---

## Exclusions and ambiguous cases (under the maker's Hindu-only rule, D-28)

| Item | Why it is flagged | Default |
|---|---|---|
| A deity image as lock-screen still, thumbnail or app icon | a phone is touched, carried and laid face-down, and its lock screen sits under the clock and notifications (my reasoning, J; not a sourced norm); the film's default deity policy is symbols only (`research/hindu-visual.md` P1, R17, R20); whether *she* would welcome it is O-42 | out; her script end-card line, a lamp or the object instead |
| Her own deities (the eight named in D-31) on a phone surface (lock screen, thumbnail, icon) | they are hers, which is the test the charter sets; but a deity image on a device raises the placement and handling questions above, and how a Pushtimarg household treats an image of Shrinathji or Bal Krishna on a phone is the Pushtimarg sprint's to say (UNVERIFIED here) | symbols and her script until O-42 is answered by the maker as her proxy; then the maker decides, in writing, per surface |
| Forwardable deity frames | once a relative forwards the film, a frame can be saved among unrelated photos (community norm, UNVERIFIED) | follow O-42; no deity in the gallery thumbnail or poster frame |
| Decorative frames on any phone page (thank-you page, PWA, HTML): paisley, jaali screens, cusped or multifoil arches, mehndi borders, geometric tile patterns | shared or Indo-Islamic origin (hindu-visual exclusion list); and no ornament without a reason (Principle 2) | none; a plain, quiet page |
| Bells, candles, haloes, crosses and winged figures as UI marks (the Christian or colonial forms only) | Christian or colonial layer in these forms | Church-shaped bells, candles where a diya belongs, a flat gold-disc halo drawn as in a church icon, crosses, winged figures: Christian or colonial layer, none. The ghanta (temple bell), the diya and the prabhavali or prabhamandala are Hindu and are not excluded by this row. |
| A decorative QR frame (rangoli or mandala border) | decoration for its own sake | plain QR, and only a static one |
| The swastika in a thumbnail or lock-screen still | sacred in ritual form, misread in a public room outside India (hindu-visual 1.4) | the maker's call alone (O-44); default out |
| Dharmic-not-Hindu or Adivasi text in a thank-you line | not covered by D-28 | none; ask |
| Ringtones, notification sounds, sound chips | none needed; no Om tone as a UI sound | the tone ladder uses plain sine tones |

No Mughal, other Islamic or Christian motif enters through this track; the only shared or ambiguous items are the decorative devices above, all defaulted to out.

---

## Tools, sources, services and costs (as of 2026-10-19)

| Item | Use | Cost | State |
|---|---|---|---|
| ffmpeg (winget `Gyan.FFmpeg`, expected 9.0.2) and the container's 6.1.1 | all encodes | free | PC UNVERIFIED (W-28) |
| VLC (desktop and phones) | playback, iPhone file sharing target | free | |
| Apple Devices app (Microsoft Store) | PC to iPhone file sharing and photo sync | free; needs Windows 10 or 11 | UNVERIFIED on the PC |
| Apple TV app for Windows | only for the movies sync route | free | home videos UNVERIFIED [35] |
| WhatsApp, Telegram, Signal | fixture-only tests | free; Telegram Premium price UNVERIFIED | |
| Two project phones (an Android of the 2019 to 2021 class and an iPhone) | the protocol | UNVERIFIED (used market); the maker may own old phones | O-04, O-43 |
| USB-C or OTG drive and adapters | keepsake (g), stick | UNVERIFIED | |
| Tablet for option (f) | optional keepsake | UNVERIFIED | O-04 |
| Lux meter app or meter | room lighting for tests | free app; accuracy UNVERIFIED | |
| Cloudflare Access Free (50 seats) | only after W-48, relatives | free; limit read in `playbooks/format.md` on 2026-10-18; the pricing pages I tried today did not show it | not used before the ledger |
| Google Drive | not used | 15 GB free per account [11] | |

---

## Changes to existing playbooks

| File | Section | What changes |
|---|---|---|
| `playbooks/theatrical-delivery.md` | **T2 Delivery spec sheet** | Add a column "Phone (hers by cable; relatives after the ledger)": P1, P2 as in T-M1, SDR only, burned phone captions, sizes (9 min 149 to 196 MB typical, 553 MB ceiling; 12 min 199 to 262 MB, 737 MB), checks of T-M1 |
| same | **Step 5 Mix** | Phone files are the online row (-16 LUFS, -1 dBTP) **measured on the final MP4**: AAC adds 0.3 to 0.7 dB of true peak on hot material (M) |
| same | **Step 6 Burn in the captions** and **T1 settings card** | The ffmpeg default `MarginV` puts caption descenders at 3.5%, outside the 5% box: write `MarginV` 20 or more into the card (venue). Add the phone burn-in (FontSize 28, MarginV 40, 36 characters, white) and the fill-crop rule. Tinted caption text shifts colour (cream blue +9): captions white or neutral |
| same | **Step 7 Build the venue file set** | Add P1 and P2 to the file set, encoded from the master (not from the venue file, which has the venue captions in it) |
| same | **Step 8 Check every file** | Add atom order, true peak after AAC, PR3 grain survival for P1, the 12-patch colour test, and the phone protocol T-M6 |
| same | **T8 rights log; T9 releases 4d to 4g** | `phone_share` column; a phone-sharing line (Q6) |
| same | **T11 Pack list for 26 February** | "Phone by cable" becomes a tested cable and adapter for **her** phone class and for the spare laptop, with P1 on both sticks; add two project phones' results |
| same | **Decisions (TD table)** | New **TD-9** phone deliverable (T-M8) |
| `playbooks/format.md` | **Step 8 Harden the slice** (caption bullets) and **Exercise 1** | `MarginV` and the phone burn-in; arm's-length caption test at 35 and 50 cm on the project phones; add the phone protocol; with the sibling's change ("FontSize=23 is not font-independent for Indic faces"): the phone size for Gujarati is set by KA height, K2 |
| same | **Decision 8 Where it lives** | New row "her phone, by cable"; shared-album rows marked as downscaling and as cloud copies (iCloud 720p on albums created before iOS 27, 2026-09-14 [10]; Google Photos Storage saver to 1080p [11]) |
| same | **Decision 11 A companion** and **Step 15** | The offline scrubber page is **demoted** to a laptop and archive companion; for her phone it is replaced by P1 by cable (Q7); the failure ladder's "phone by cable" is a tested route |
| `DECISIONS.md` (orchestrator) | **W-30** | Replace "offline scrubber page on the USB" by the Q7 recommendation at G-SLICE (O-30) |
| same | **W-18** | Add `MarginV` 20 or more for the venue file; add the phone burn-in as a second caption setting |
| same | **new rows (proposed)** | P1 and P2 specs; TD-9; check 1 hygiene as a W-26 extension (project phones carry no accounts); K1 to K5 keyed on O-43 |
| `playbooks/cinematic-quality.md` | **T1 PR3 Grain survival** | State that P1 passes at CRF 20 (73%) and fails at 22 (43%); P2 and HEVC are exempt or measured at equal viewing scale |
| same | **T6 Projection-truth checklist** and **Exercise 2 dark steps** | Phone-truth sub-list: fill-crop card, 35 and 50 cm caption read, dark steps at 100 and 500 lux, upright view as degraded |
| same | **T2 style bible, decisions 3 and 8** | `phone_min_xheight_pct: 3.2 (target 3.8)`; **Trim P** as a third trim beside V and C (starting 4 to 7 IRE at codes 24 to 40, black pinned); grain at CRF 20 or looser fails PR3 |
| same | **TY1** | Phone column: x-height 3.2% hard, 3.8% target; strokes 4 px |
| `playbooks/agent-pipeline.md` | **Shot brief YAML; G2 review pack; G6** | `phone_safe`, `hands_box`, `object_box`, `caption_zone`; G2 composites `safe_area_template.svg`; G6 adds the T-M1 checks |
| `playbooks/music-sound.md` | **Exercise 6 and Template G** | Phone-speaker pass with the tone ladder; first cold-open sound above 400 Hz; AAC true-peak check |
| `playbooks/surprise-ops.md` | **Step 11 (reveal), item 9; Decision 15 keepsake; Step 10 fallback ladder** | Cable copy to her phone as a reveal-weekend step with K1; no QR on the night and the spoken-promise line; scrubber demoted; the printed book's QR codes stay static, with chapters findable without them |
| `playbooks/toolchain.md` and `.claude/skills/free-creative-toolchain/recipes/r9_deliver.sh` (orchestrator edits; I do not touch `.claude/`) | **Step 11 captions; the r9 caption recipe** | The recipe line `FontSize=28 ... MarginV=40` coincides with the phone burn-in but is DejaVu and Outline 2 on the venue file; split into venue and phone recipes; add the libass colour warning |
| `skills-staging/` (proposed, scribe) | new skill `phone-delivery-and-keepsake` | agent form of T-M1, T-M3, T-M6 and the Q8 hygiene rule |

---

## Open questions for the maker

1. **O-43, narrowed by D-31 (her phone is Android).** Make, model, Android version, screen size and resolution (720p or 1080p), free storage, USB port type (micro-USB or USB-C, and whether it takes an OTG drive), which app she watches video in (WhatsApp, YouTube, the gallery), and whether she holds it sideways (hindu-visual V7). Does she use reading glasses for the phone, and what is its text-size setting? (Sets K1 to K3.)
2. **Her backup state.** Does her Android back up photos to Google Photos, does the phone manufacturer's gallery sync to a cloud (Samsung Gallery to OneDrive, others UNVERIFIED), **is "Back up all device folders" on in Google Photos**, and is her Google account shared with anyone? Answer from your own knowledge; do not look at her phone (D-02).
3. **Relatives' phones.** Which two or three phones do close relatives use, and how much free storage or data do they have? (Sets P2 and K4.)
4. **Project phones.** Do you have, or will you buy or borrow, two phones with no accounts (an Android of the 2019 to 2021 class and an iPhone)? Budget (O-04)?
5. **Cold open.** Do you accept either a visible first light within about 4 s or a first sound above 400 Hz on the phone file (Q3)? Do you accept a mild Trim P?
6. **Caption policy.** Given D-05, will captions exist beyond cards? If not, the phone burn-in applies only to the HER-PUBLIC line and the cards' type floor decides.
7. **Tablet.** Is a dedicated tablet in Guided Access worth the budget as her keepsake (option f)?
8. **Guests.** Do you accept "no QR, no link on the night; a spoken promise of a family copy after a named date", and what date?
9. **Her backup, her call.** The first question, at the reveal-weekend check and again in the her-turn conversation on Sat 6 Mar: is "Back up all device folders" on? If it is off, the film can go in a new or an app's folder; if it is on or unknown, do you want it on the tablet or the stick until she decides, or do you decide otherwise?
10. **Lock-screen still.** Her script end-card line only (no deity image, no swastika), checked against a printed source: confirm.
11. **Language of the captions and the cards** (O-15; her script is Gujarati, D-31): captions in the room's language and her script on cards, or Gujarati captions too? That decides K2 and the shaping font test, which should join the settings card on Sun 1 Nov. Which Gujarati face? Noto Sans Gujarati is the default caption face (the sibling's Q9: it carries digits, the Om sign and every conjunct); Hind Vadodara only for lines without digits.
12. **Pushtimarg and her phone.** Would a deity image on a phone surface (lock screen, thumbnail) be welcome to her or not (O-42, with the Pushtimarg sprint's norms)? Until you answer, the lock-screen still carries her script line only.

---

## Sources

Web sources were read on 2026-10-19 unless marked. "Digest only" means read as a search-result summary, page not opened by me.

1. WhatsApp Help Center, "How to send media, contacts, or location" (web) — https://faq.whatsapp.com/453914586839706/?cms_platform=web — read 2026-10-19 — video default limit 100 MB and 720p (fast) or 64 MB and 480p (slow); documents 2 GB; Standard or HD quality; formats; Status 90 s. **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium (HTTP 200 there; the fetch tool returns only the title; curl gets an HTTP 400 error page); one reading, not the maker's browser.**
2. WhatsApp Help Center, "About HD photos and videos" (Android) — https://faq.whatsapp.com/759301289012856/?cms_platform=android — read 2026-10-19 — HD per message or default under Media upload quality; no pixel numbers; connection affects quality.
3. WhatsApp Help Center, "I can't send long videos" — https://faq.whatsapp.com/823886715479103/ (reached from /545917406122452/) — read 2026-10-19 — "64MB on all platforms" and the Document route up to 2 GB; the page also repeats [1]'s 100 MB and 720p default for a fast connection, so the inconsistency is inside this page; the title today is "Can't send longer videos". **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
4. WhatsApp Help Center, "About forwarding limits" — https://faq.whatsapp.com/1053543185312573 — read 2026-10-19 — up to five chats at a time; "forwarded many times" after five-chat chains; a message forwarded to you "can only be shared with one additional group chat" (new on the 2026-10-19 re-read). **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
5. WhatsApp Blog, "Reactions, 2GB File Sharing, 512 Groups" — https://blog.whatsapp.com/reactions-2gb-file-sharing-512-groups — post 2022-05-05, updated 2022-07-11 — 2 GB files, end-to-end encrypted.
6. WhatsApp Privacy Policy — https://www.whatsapp.com/legal/privacy-policy — "Effective January 4, 2021" as displayed — delivered messages deleted from servers; undelivered kept encrypted up to 30 days; forwarded media stored temporarily.
7. WhatsApp Help Center, "How to back up your chat history" (Android) — https://faq.whatsapp.com/481135090640375/?cms_platform=android — read 2026-10-19 — backup to WhatsApp cloud or Google; "Include videos in chats".
8. Telegram FAQ — https://telegram.org/faq — read 2026-10-19 — files up to 2 GB each; chats stored in the Telegram cloud; silent on compression.
9. Telegram blog, "700 Million Users and Telegram Premium" — https://telegram.org/blog/700-million-and-premium — 2022-06-19 — 2 GB free, 4 GB Premium.
10. Apple Support, "Shared Albums limits" — https://support.apple.com/en-us/148868 — published 2026-09-14 — iOS 26 and earlier: video up to 15 minutes at up to 720p, 5,000 items; iOS 27 and later: original and full resolution, counts against storage.
11. Google Photos Help, "Choose the upload size of your photos and videos" — https://support.google.com/photos/answer/6220791 — read 2026-10-19 — Storage saver resizes video above 1080p to 1080p; 15 GB per account.
12. Google Photos Help, "Turn backup on or off" — https://support.google.com/photos/answer/6193313 — read 2026-10-19; re-read the same day in a headless Chromium on the Android tab with its sections expanded (the page's title is now "Back up photos & videos"; the first pass saw it as "Turn backup on or off") — Photos settings, Backup; "your chosen device folders are automatically backed up too, not only your camera"; "Back up device folders" screen and a "Back up all device folders" switch ("photos in new device folders automatically back up"); no default folders listed; removal means turning backup off and deleting the items on photos.google.com (that turning backup off leaves them is an inference).
13. Apple Support, "How to use AirDrop on your iPhone or iPad" — https://support.apple.com/en-us/119857 — read 2026-10-19 — Everyone for 10 Minutes; AirDrop code with iOS 26.2 or later.
14. Google, "Android Quick Share support for AirDrop" — https://blog.google/security/android-quick-share-support-for-airdrop-security/ — 2025-11-20 — Pixel 10 first; peer to peer; AirDrop "Everyone for 10 minutes" only.
15. Google Drive Help, "Google Drive file size limits" — https://support.google.com/drive/answer/37603 — read 2026-10-19 — up to 5 TB a file.
16. Google Drive Help, "Share files from Google Drive" — https://support.google.com/drive/answer/2494822 — read 2026-10-19 — "Anyone with the link"; viewers can download unless turned off.
17. Gmail Help, "Attachment size limit" — https://support.google.com/mail/answer/6584 — read 2026-10-19 — 25 MB; larger replaced by a Drive link.
18. Android Developers, "Supported media formats" — https://developer.android.com/media/platform/supported-formats — read 2026-10-19 — H.264 Baseline (3.0+) and Main (6.0+) decoders; HEVC Main Level 3 for mobile; HLG10 and HDR10; moov before mdat.
19. Apple Support, "iPhone 15 Tech Specs" — https://support.apple.com/en-us/111831 — read 2026-10-19 — 6.1 in, 2556x1179, 460 ppi, 1000/1600/2000 nits; HEVC, H.264, ProRes.
20. YouTube Help, "Recommended upload encoding settings" — https://support.google.com/youtube/answer/1722171 — read 2026-10-19 — H.264 High, BT.709, 8 Mb/s 1080p SDR, AAC-LC, moov at front.
21. FFmpeg, "Formats Documentation" — https://www.ffmpeg.org/ffmpeg-formats.html — read 2026-10-19 (first 100,000 characters; the FFMETADATA chapter syntax section was truncated) — faststart; MP4 muxer writes Nero chapters and a QuickTime chapter track by default.
22. Robitza, "CRF Guide (Constant Rate Factor in x264, x265 and libvpx)" — https://slhck.info/video/2017/02/24/crf-guide.html — read 2026-10-19 — sane x264 range 18 to 28, default 23; plus or minus 6 is about half or double.
23. x265 documentation, command line options — https://x265.readthedocs.io/en/master/cli.html — read 2026-10-19 (first 100,000 characters) — CRF default 28; VBV needs both options in CRF mode; `--tune grain` enables `--rc-grain`.
24. caniuse, "HEVC/H.265 video format" — https://caniuse.com/hevc — read 2026-10-19 — partial in Chrome from 107, Firefox from 137; Safari and iOS Safari supported.
25. StatCounter, "Mobile Operating System Market Share India" — https://gs.statcounter.com/os-market-share/mobile/india — September 2026 — Android 93.89%, iOS 6.05%.
26. StatCounter, "Mobile Screen Resolution Stats India" — https://gs.statcounter.com/screen-resolution-stats/mobile/india — September 2026 — top six viewports and shares.
27. GSMArena, "Xiaomi Redmi 9A" — https://www.gsmarena.com/xiaomi_redmi_9a-10279.php — read 2026-10-19 (and again in a headless Chromium) — 6.53 in IPS LCD, 720x1600, 20:9, 400 nits typical, announced 2020-06-30; chipset MediaTek MT6762G Helio G25; microUSB 2.0 with OTG; microSDXC slot.
28. GSMArena, "Xiaomi Redmi Note 10" — https://www.gsmarena.com/xiaomi_redmi_note_10-10247.php — read 2026-10-19 — 6.43 in Super AMOLED, 1080x2400, 20:9, 450 nits typical and 1100 peak, announced 2021-03-04.
29. GSMArena, "Xiaomi Redmi Note 10 review: lab tests" — https://www.gsmarena.com/xiaomi_redmi_note_10-review-2244p3.php — read 2026-10-19 — measured 475 nits manual and 682 auto; YouTube sees HDR, Netflix SDR only.
30. Bababekova et al., "Font size and viewing distance of handheld smart phones", Optometry and Vision Science 88(7):795-7, 2011 — https://pubmed.ncbi.nlm.nih.gov/21499163/ — abstract via search-result digest only (page needs cookies) — mean 36.2 cm texting (n=129), 32.2 cm web (n=100).
31. GSMArena, "YouTube updated with pinch-to-zoom for screens wider than 16:9" — https://m.gsmarena.com/youtube_updated_with_pinchtozoom_for_screens_wider_than_169-news-28290.php — 2017-11-16 — crop-zoom fills the screen and may crop video; Samsung's support page (https://www.samsung.com/us/support/troubleshoot/TSG10004866, 403) via digest only.
32. Apple Developer, "AVLayerVideoGravity.resizeAspectFill" — https://developer.apple.com/documentation/AVFoundation/AVLayerVideoGravity/resizeAspectFill — digest only (page is script-rendered) — resizeAspect fits; resizeAspectFill fills.
33. Apple Support, "Transfer files between your Windows device and iPhone, iPad, or iPod touch" (Apple Devices app) — https://support.apple.com/guide/devices-windows/transfer-files-between-your-devices-mchl4bd77d3a/windows — read 2026-10-19 — Files in the sidebar; drag onto apps that support file sharing.
34. Apple Support, "Sync photos between your Windows device and iPhone, iPad, or iPod" — https://support.apple.com/guide/devices-windows/sync-photos-to-your-device-mchl4af095d3/windows — read 2026-10-19 — Include videos; unavailable while iCloud Photos is on.
35. Apple Support, "Sync movies between your Windows device and iPhone, iPad, or iPod" — https://support.apple.com/guide/devices-windows/sync-movies-to-your-device-mchl36119991/windows — read 2026-10-19 — needs the Apple TV app on Windows; home videos not mentioned.
36. Apple Support, "Connect external storage devices to iPhone" — https://support.apple.com/guide/iphone/external-storage-devices-iph95baac91f/ios — digest only (page body truncated on fetch) — one partition in APFS, HFS+, exFAT, FAT32 or FAT; Files app.
37. Android Help, "Transfer files between your Android device and computer" — https://support.google.com/android/answer/9064445 — read 2026-10-19 — USB File Transfer mode.
38. Apple Developer Forums, "Publish or test mini sites locally in Safari with relative source references" — https://developer.apple.com/forums/thread/710001 — July 2022 — Files preview does not load relative references; Safari no longer opens local files on iPad.
39. Apple Community, "How to open local html files in safari" — https://discussions.apple.com/thread/256102223 — 2025-07-21 and 22 — Quick Look "will not run JavaScript"; iOS 18.5.
40. GitHub, THU-MAIC/OpenMAIC issue 1847 — https://github.com/THU-MAIC/OpenMAIC/issues/1847 — opened 2026-10-08, open — standalone HTML export blank in the iOS Files preview; works over `file://` on desktop.
41. MIT App Inventor Community, "Off topic html and Android 10" — https://community.appinventor.mit.edu/t/off-topic-html-and-android-10/35979 — June to August 2021 — `content://` addresses; relative links fail on Android 10 and 11.
42. TiddlyWiki Talk, "Cannot play local video (Android)" — https://talk.tiddlywiki.org/t/cannot-play-local-video-android/3516 — 2022-06-01 — local video fails via relative paths; local server workaround.
43. Mozilla Bugzilla 1809954 — https://bugzilla.mozilla.org/show_bug.cgi?id=1809954 — closed as a duplicate — Firefox for Android cannot load subresources of local HTML opened through `content://`.
44. WebKit blog, "Full Third-Party Cookie Blocking and More" — https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ — 2020-03-24 — seven-day cap on script-writable storage; home-screen web apps exempt.
45. MDN, "Making PWAs installable" — https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable — read 2026-10-19 — HTTPS or localhost required; iOS 16.4 and later install from the Share menu.
46. Tranquillity Base, "mChapters" — https://www.tranquillitybase.jp/mChapters/mChapters_en.html — read 2026-10-19 — the Music and TV apps on iOS (since iOS 12.3) do not appear to support chapters.
47. Larry Jordan, "QuickTime: Display Chapter Markers" — https://larryjordan.com/articles/chapter-markers/ — read 2026-10-19 — QuickTime Player shows chapters in QuickTime and MPEG-4 movies.
48. Apple Support, "Use Guided Access on iPhone or iPad" — https://support.apple.com/en-us/111795 — read 2026-10-19 — triple-click the side button; disable screen areas or all touch.
49. Android Help, "Pin and unpin screens" — https://support.google.com/android/answer/9455138?hl=en — read 2026-10-19 — App pinning; some steps need Android 11 or later on Pixel.
50. Xiaomi, "Notice of termination of Xiaomi Cloud sync for Gallery items" — https://i.mi.com/announcement/stop_service — read 2026-10-19 — ends 2022-10-25; India in the first group; data deleted 2023-08-01.
51. Samsung Support, "OneDrive on your Samsung phone or tablet" — https://www.samsung.com/us/support/answer/ANS10003437/ — digest only (403 on fetch; regional Samsung pages seen in search results) — Gallery sync with OneDrive needs Samsung and Microsoft accounts; may be off by default.
52. W3C, "Understanding SC 2.5.5: Target Size (Enhanced)" — https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — read 2026-10-19 — 44 by 44 CSS pixels.
53. W3C, "Understanding SC 1.4.3: Contrast (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — read 2026-10-19 — 4.5:1; 3:1 for large text.
54. Lee et al., "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ — read 2026-10-19 — qualitative: swipes and double-taps failed; larger fonts and objects; tablets preferred.
55. Wikipedia, "Lux" — https://en.wikipedia.org/wiki/Lux — read 2026-10-19 — overcast day 1,000; full daylight 10,000 to 25,000; office 320 to 500.
56. Wikipedia, "Fresnel equations" — https://en.wikipedia.org/wiki/Fresnel_equations — read 2026-10-19 (first 100,000 characters) — about 4% reflectance per glass surface at normal incidence.
57. Netflix Partner Help Center, "Timed Text Style Guide: General Requirements" — https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements — read 2026-10-19 — two lines maximum; events 5/6 s to 7 s; no character count on this page.
58. Local: `CHARTER.md` (Known facts, including "Her world", 2026-10-19); `DECISIONS.md` (D-02, D-05, D-15, D-24, D-27, D-28, **D-31**, W-04, W-15 to W-20, W-25, W-26, W-30, W-33, W-35, W-46 to W-48, O-30, O-43); commit `ac6711e` ("Record her world") — read 2026-10-19.
59. Local: `playbooks/theatrical-delivery.md` (Steps 4 to 8, T1, T2, T8, T9, T11), `playbooks/format.md` (Step 8, Decisions 8 and 11, Step 15), `playbooks/cinematic-quality.md` (T1 PR2 and PR3, T6, Exercise 2, TY1), `playbooks/production-scale.md` (stage hours), `playbooks/surprise-ops.md` (Step 11, Decision 15), `playbooks/toolchain.md` (captions) — read 2026-10-19.
60. Local: `research/hindu-visual.md` F3 (M-H1) and `research/hindu-visual-fixtures/phone_chart.svg`; `research/cinematic-quality.md` FQ1 (caption x-height; cites Legge and Bigelow 2011, J Vision 11(5):8, and the BBC subtitle guidelines via `playbooks/format.md` [105]; neither re-opened today: the Legge PDF returned 503, bbc.co.uk is not reachable by the fetch tool); `research/agent-pipeline.md` Q-F1 (colour-patch method); `reviews/04-hindu-mobile-briefs-review.md` Part 4.
61. This track's fixtures and measurements, 2026-10-19: `research/mobile-delivery-fixtures/` (README, SVG templates, CSVs, Devanagari and Gujarati shaping evidence).
62. Local, sibling track: `research/devotional-sound-script.md` (Q9 fonts, Q10 shaping, Template L caption sizes for phones, Summary 14 phone-speaker model) and `research/devotional-sound-script-fixtures/` (`caption_size_FontSize23_2026-10-19.csv`, `caption_width_FontSize23_2026-10-19.csv`, `shaping_fixture.tsv` and `.srt`, `phone_speaker_model_2026-10-19.csv`, README) — read 2026-10-19; its numbers are used as inputs and credited where used.
63. FFmpeg source files at four release tags: `libavfilter/vf_subtitles.c` (n6.1.1, n7.0, n8.0, n9.0.2), `libavfilter/drawutils.c` and `libavcodec/ass.c` (n6.1.1, n9.0.2) — https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/libavfilter/vf_subtitles.c (the same path under each tag) — read 2026-10-19 — n6.1.1 calls `ff_draw_init()` (YUV defaults to SMPTE170M); n7.0 calls `ff_draw_init2()` with the link's colourspace; n8.0 adds `ass_get_color_space()` for the track's `YCbCr Matrix`; the `shaping` option is on `ass` through n8.0 and on `subtitles` from n9.0; ffmpeg's SRT-to-ASS header says `YCbCr Matrix: None`. The n9.0.2 tag commit is 946fcce ("Update for 9.0.2", 2026-09-18, from `git ls-remote`).
64. Google Fonts, `ofl/hindvadodara/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/hindvadodara/OFL.txt (raw file read) — read 2026-10-19 — "Copyright (c) 2015 Indian Type Foundry", SIL Open Font License Version 1.1 (26 February 2007), no Reserved Font Name clause on the licence line.
65. Google Fonts, `ofl/notosansgujarati/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/notosansgujarati/OFL.txt (raw file read) — read 2026-10-19 — "Copyright 2022 The Noto Project Authors (https://github.com/notofonts/gujarati)", SIL Open Font License Version 1.1, no Reserved Font Name clause.
66. MediaTek, "Helio G25" — https://www.mediatek.com/products/smartphones/mediatek-helio-g25 — read 2026-10-19 in a headless Chromium — Video Playback "H.264, H.265 / HEVC", Video Playback FPS "1080P @ 30 fps", max display resolution 1600 x 720; no H.264 profile or bitrate given.
67. Android Developers, Media3 `PlayerView` and `AspectRatioFrameLayout` — https://developer.android.com/reference/androidx/media3/ui/PlayerView — read 2026-10-19 in a headless Chromium — `resize_mode` valid values fit, fixed_width, fixed_height, fill, zoom; "Default: fit".
68. Apple Developer Documentation, `AVPlayerLayer.videoGravity` and `AVLayerVideoGravity.resizeAspect` — https://developer.apple.com/documentation/avfoundation/avplayerlayer/videogravity (read through the page's data file, https://developer.apple.com/tutorials/data/documentation/avfoundation/avplayerlayer/videogravity.json) — read 2026-10-19 — "The default value is" `resizeAspect`, which "preserves its aspect ratio and fits it within the layer's bounds".
69. pushtimarg.net, "Seva" — https://pushtimarg.net/seva/ — read 2026-10-19 in a headless Chromium — the nitya seva vidhi: at Mangla "one should ring the bells thrice and blow the Sankh" (after thinking of the cow-bells of Vraj); at Shayan "keep a small/soft lamp on"; the routine "should not be viewed with rigidity" and varies among the seven houses.
70. pushtimarg.net, "FAQs" — https://pushtimarg.net/faqs/ — read 2026-10-19 in a headless Chromium — a devotee's question about a "Chitra Swaroop-Shrinathji" that "had been pusht" and is served "from Mangala to Shayan"; no text on phones, wallpapers or screens found in the page text.
71. Local: `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt` — dated text excerpts of [1] to [5], saved 2026-10-19.
72. Local: `research/pushtimarg-world.md` (F6 reverence norms, PR2, PR4, PR10, PR14, open Q3) — read 2026-10-19.
73. Local: this track's round-1 fixtures, 2026-10-19: `caption_colour_ffmpeg_builds_2026-10-19.csv`, `caption_colour_summary_2026-10-19.csv`, `caption_colour_real_text_2026-10-19.csv`, `caption_ycbcr_matrix_example_2026-10-19.ass`, `scaler_bracket_720p_panel_2026-10-19.csv` and the re-cut `gujarati_shaping_freeserif_2026-10-19.srt` and `.png` in `research/mobile-delivery-fixtures/`.

---

## Follow-up research (round 1)

*Sonnet implementor, Monday 2026-10-19 (the same day as the first pass), answering the seven research follow-ups in `reviews/mobile-delivery-round1.md` section 5 and applying its eight nudges to the playbook and the skill. Labels as above: **(M)** measured in the cloud container on synthetic material, **(C)** computed, **(J)** judgement, **UNVERIFIED** not checked. Windows steps stay UNVERIFIED until `windows_check_report.json` for the maker's PC is in the repo (W-28).*

**How this pass was made, and what it could not do.**
- **Search budget.** The shared web-search allowance (200 calls a turn, shared by every agent) was already used up, so no search engine was queried. Every page below was fetched by its own address: with the fetch tool, with raw files from GitHub, or, for script-rendered pages, with a headless Chromium (Playwright 1.56.1, HeadlessChrome 141) that ships in the container. Pages were treated as data. Anything that needed a search (per-skin Google Photos defaults, vendor player defaults, the Pushtimarg view of a phone wallpaper) is marked as not found rather than guessed.
- **Builds for the caption tests.** The container's ffmpeg is 6.1.1 (Ubuntu apt). I built ffmpeg **n7.0, n8.0 and n9.0.2 from their git tags** in a RAM disk (about a minute each, same libass 0.17.1 and HarfBuzz 8.3.0 as 6.1.1). n9.0.2 is the version the maker's PC reportedly has (sibling README: Gyan "release full" 9.0.2, dated 2026-09-19); **the PC's own build bundles its own libass and may differ, so the PC re-run stays required**. No code was kept in the repo; fixtures and CSVs are in `research/mobile-delivery-fixtures/` (README, section "Round-1 method").
- **No phone, no WhatsApp account and no maker answer exists yet**, so Q-F1 (device behaviour) and Q-F7 (O-43) could be prepared but not run or answered.

### Answers at a glance

| # | Question | Answer in one line |
|---|---|---|
| Q-F1 | WhatsApp on the project phones; the Help Center figures | Device test **not run** (no accounts, Decision 12 is the maker's, no phones); recording tables are ready. The Help Center numbers **were re-read** in a headless browser and are saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`: the 64 MB and 100 MB lines are on the same page, 2 GB for documents confirmed, and one new forwarding line. |
| Q-F2 | Does ffmpeg 9.0.2 still shift tinted captions? | **No, in the container's n9.0.2 build, when the master is BT.709-tagged** (worst 3/255 on twelve colours; 6.1.1 gives 23/255). Cause found in the source: n7.0 draws subtitles in the link's colourspace. **An `.ass` file without a `YCbCr Matrix` header falls back to BT.601 on n8.0 and later (23/255 again); `TV.709` or `None` fixes it.** An untagged master fails on every build. PC re-run still required. |
| Q-F2b | (found on the way) the Gujarati and Devanagari "failure" exhibits | **The cause was the build, not the font.** The same FreeSerif and FreeSans lines shape correctly through n9.0.2's `subtitles` filter; 6.1.1's `subtitles` filter shapes in simple mode. Three texts that blamed "a font without Indic shaping tables" are corrected. |
| Q-F3 | Google Photos "Back up device folders" defaults by skin | **Not documented.** Google's page lists no default folders; it documents the "Back up all device folders" switch. No OEM page could be read. K1 is rewritten to ask first. |
| Q-F4 | Redmi 9A class: H.264 High 4.1 at 8 Mb/s; its real scaler | MediaTek lists H.264 and HEVC playback at 1080p 30 fps for the Helio G25; the profile and bitrate are not stated, and Android requires only Baseline and Main. **UNVERIFIED on a handset; row 3 measures it.** Scaler: not knowable here; six scalers bracket it: **a 3 px line keeps at least 0.83 contrast under every scaler at every phase, a 4 px line at least 0.94** (M). |
| Q-F5 | Default fit or fill of the five players | Documented only for the platform components: Media3 `PlayerView` defaults to fit; Apple's `AVPlayerLayer` defaults to `resizeAspect` (fit). **The five apps' own defaults are not documented anywhere I could read**; the fill-crop card (row 4) is the measurement. |
| Q-F6 | Pushtimarg norm for an image on a phone surface; the morning bell and lamp | **No sampradaya page I read says anything about a phone surface.** What it does say (a picture can be a living svarupa in seva) supports the default "none unless she knows and says yes". **The morning bell is in the sampradaya's own Mangla text (bells rung three times, conch blown); a lit lamp is documented at Shayan, not at Mangla.** Whether her household does either is the maker's. |
| Q-F7 | O-43 | **Not answered: only the maker can.** An intake table with each field, the decision it drives and the default is below. |

### Q-F1. WhatsApp: the Help Center figures and the project-phone measurement

**Help Center figures, re-read 2026-10-19 in a headless browser (M; the excerpt is saved).** The pages are script-rendered: the fetch tool returns only a title and a plain `curl` gets an HTTP 400 "Error" page. Rendered in Chromium, all four returned HTTP 200 with their text. What they say, verbatim, is in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`.
- **[1] media limits (web variant).** "For users with a faster internet connection, the default video size limit is 100MB and 720p resolution. For users with a slower internet connection, the default video size limit is 64MB and 480p resolution." Documents: "The maximum allowed document size is 2 GB." Formats: "3GP, AVI, FLV, MKV, MOV, MP4." Also "High audio sample rate or professional cameras may be unsupported."
- **[3] long videos (the title today is "Can't send longer videos").** The "conflict" the first pass recorded between [1] and [3] is **inside [3] itself**: "The maximum file size for videos sent or forwarded through WhatsApp is 64MB on all platforms", then, two lines later, the 100 MB and 720p default for fast connections. WhatsApp's own page is inconsistent; **plan on 64 MB** stands. The page does not say a Document is left unchanged; it says Document is the way to send "longer or larger media".
- **[4] forwarding.** "You can forward messages to up to five people or groups at a time." **New:** "If you're forwarding a message or update that was forwarded to you, it can only be shared with one additional group chat." A chain of five or more chats gets the label "Forwarded many times." Neither line prevents forwarding; **a forwarded copy still cannot be recalled** (release line stays).
- **[2] HD (Android variant).** Still no pixel or bitrate numbers. **New:** "If you attach an existing photo or video, you don't have to select between Standard quality or HD quality." The page does not say what quality an existing gallery video then gets.
- **[5] blog.** 2 GB, end-to-end encrypted, posted 2022-05-05, updated 2022-07-11: unchanged.
- **Limits of this reading.** A US-hosted headless browser, not the maker's browser; WhatsApp may show other numbers by country or app version. The three numbers (64 MB, 100 MB, 2 GB) are therefore **re-read, one reading** and no longer "not re-readable by fetch". One reading in the maker's own browser is optional.

**Device behaviour (document byte-identity by SHA-256; media resolution, bitrate, frame rate, darks): not run.** It needs a WhatsApp account on each of two project phones, which the no-accounts rule forbids until the maker decides Decision 12 (playbook), and no project phone exists yet (O-04). It also cannot be done honestly with a third party's phone or the maker's own. What is ready for the day it runs (J, fixture only, two separate numbers, accounts removed afterwards, nothing of hers):
1. **Fixtures.** `phone_test_card_clean.mp4` (the 20 s card; build commands in the fixtures README) as the clean file, plus the 12-second C3 dense-lines clip as the stress file. Record each file's SHA-256 on the PC first: `Get-FileHash -Algorithm SHA256 file.mp4` (PowerShell).
2. **Document route.** Send the file as a Document; receive it on the second phone; copy the received file back to the PC over the cable (File Transfer mode) and hash it there, because most Android file managers cannot hash. **Pass: the hash equals.** Write the result in T-M4.
3. **Media route, Standard and HD (two sends each).** Copy the received video back to the PC and run `ffprobe -show_entries stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,bit_rate,pix_fmt,color_space,color_range -of json`. Record resolution, video bitrate, frame rate, and whether the audio sample rate changed.
4. **Darks.** Decode the received dark-step page frame with the Q-F1 method (`scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`; the colour-patch method of `research/agent-pipeline.md`) and read the twelve patches (codes 16 to 100) against the sent file; write the first code that still differs from 16.
5. **Sizes of the send.** Note whether a P1 of 199 to 262 MB (typical, 12 minutes) is accepted as a Document and how long the send takes on the maker's connection.

| Route | Sent (hash, size) | Received hash | Resolution | Video Mb/s | fps | First visible code vs 16 | Notes |
|---|---|---|---|---|---|---|---|
| Document | | | | | | | |
| Media, Standard | | n/a | | | | | |
| Media, HD | | n/a | | | | | |

Until it runs, the document route's byte identity, the media route's numbers and the treatment of darks are **UNVERIFIED**. The 720p and 360p proxies of Q2 remain stress levels, not WhatsApp's encoder.

### Q-F2. Caption colours through the `subtitles` filter on ffmpeg 6.1.1, n7.0, n8.0 and n9.0.2

**What the source says (read 2026-10-19; [63]).**

| ffmpeg | What `libavfilter/vf_subtitles.c` does when it draws the glyph colours | Consequence |
|---|---|---|
| n6.1.1 | `ff_draw_init()`, which passes an unspecified colourspace; `drawutils.c` then treats a YUV frame as `AVCOL_SPC_SMPTE170M` (BT.601) | glyph RGB is converted to YUV with BT.601 coefficients and shown under BT.709 tags: a colour shift |
| n7.0 | `ff_draw_init2()` with `inlink->colorspace` and `inlink->color_range`: **the link's own colourspace** | correct when the master carries a BT.709 tag; BT.601 again when the link is unspecified |
| n8.0 | adds `ass_get_color_space(track->YCbCrMatrix, inlink->colorspace)`: `None` means the link; `TV.709` or `PC.709` means BT.709; `TV.601`, `PC.601`, a missing header and an unknown value mean BT.601 | **the `.ass` header now decides** |
| n9.0.2 | same as n8.0, plus the `shaping` option on the `subtitles` filter | same colour behaviour; shaping fixed (Q-F2b) |

ffmpeg's own SRT-to-ASS header carries `YCbCr Matrix: None` (`libavcodec/ass.c`, both n6.1.1 and n9.0.2), so every `.srt` burn-in follows the link's colourspace from n7.0 on. The lead in the review (n7.0 draws subtitles in the link's colourspace) is **confirmed in the source**.

**Measured (M; twelve caption colours as a solid block glyph, BT.709-tagged ProRes master, the P1 chain, libx264 CRF 20, Q-F1 decode; worst channel error in 0 to 255 units; rule ±3).** Full rows: `caption_colour_ffmpeg_builds_2026-10-19.csv`, summary `caption_colour_summary_2026-10-19.csv`.

| Caption path | 6.1.1 | n7.0 | n8.0 | n9.0.2 |
|---|---|---|---|---|
| SRT, `force_style` PrimaryColour (the P1 template path) | **23** (4 of 12 fail) | 3 | 3 | **3** |
| SRT with `<font color>` tags | 23 | 3 | 3 | 3 |
| ASS, no `YCbCr Matrix` header | 23 | 3 | **23** | **23** |
| ASS, `YCbCr Matrix: None` | 23 | 3 | 3 | 3 |
| ASS, `YCbCr Matrix: TV.709` | 23 | 3 | 3 | 3 |
| ASS, `YCbCr Matrix: TV.601` | 23 | 3 | 23 | 23 |
| **Untagged** master, SRT `force_style` | 23 | 23 | 23 | **23** |
| Untagged master, `setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv` before `subtitles`, five colours | 23 | 2 | n/a | **2** |

On 6.1.1 the failing patches are pure red (error 23), film green 2E7D32 (14), film red B5282B (12) and ochre F0B323 (8); white, greys, ink, indigo, skin and cream are within 3. **The first pass's "cream F3E9D2 becomes 242,232,219 (blue +9)" is not reproduced:** cream came out 242,230,208 on 6.1.1 (a block glyph and real Liberation Sans FontSize 28 text with Outline 2, glyph interior only; `caption_colour_real_text_2026-10-19.csv`) and 241 to 242, 231, 210 on n9.0.2. The cause of the first reading is unknown (its harness was throwaway); the saturated-colour shifts did reproduce (pure red 255,23,0 against 255,21,0; ochre 246,175,27 against 249,174,24). Real text on n9.0.2 stayed within 3/255 for eight colours in both 4:2:0 and 4:4:4; on 6.1.1 the 4:4:4 control still shows red at 24, so **chroma subsampling is not the cause; the matrix is** (M).

**Answers.**
1. **Does the Windows 9.0.2 build still shift tinted captions? The same source version, built here, does not**, for SRT captions and for `.ass` files with `None` or `TV.709`, provided **the master carries a BT.709 tag**. The PC build was not run and bundles its own libass: **UNVERIFIED for the PC; re-run the twelve-patch caption test there** (recipe below).
2. **The libass `YCbCr Matrix` header is the portable fix for `.ass` files, with a limit.** `TV.709` (or `None`) gives 3/255 on n7.0, n8.0 and n9.0.2. It is **ignored on 6.1.1** (still 23), so it is harmless there but does not rescue the container's apt build. **An `.ass` file with the header missing, or written as `TV.601`, shifts colours on n8.0 and later** (23/255): a hand-written `.ass`, or one exported by a tool that writes `TV.601` (Aegisub's default header, J, not checked), would bring the old fault back on the PC. Example file: `caption_ycbcr_matrix_example_2026-10-19.ass`.
3. **The tag is now a requirement, not a nicety.** On an untagged master every build falls back to BT.601. Check `ffprobe -show_entries stream=color_space` on the master (bt709), or put the `setparams` line before `subtitles` (2/255 on n7.0 and n9.0.2).
4. **The rule.** Captions stay **white or neutral light grey by default**. A tinted caption colour is allowed on a build that passes the twelve-patch caption test (every patch within ±3/255 on the real master) and the result is recorded in `windows_check_report.json`. On the container's 6.1.1 the neutral-only rule stands. The previous "tinted type is a graphic" fallback (PNG or SVG overlay) stays for anything the test does not clear.
5. **PC recipe (relative file names; a drive letter's colon breaks the filter string).** (a) `ffmpeg -hide_banner -version` and `-buildconf | Select-String libass`; (b) `ffprobe` the master for `color_space=bt709`; (c) for each of the twelve colours: `ffmpeg -y -i master.mov -vf "subtitles=one.srt:force_style='FontName=DejaVu Sans,FontSize=40,Outline=0,Shadow=0,PrimaryColour=&H00BBGGRR&',<the P1 scale and format string>" -c:v libx264 -preset slow -crf 20 <the P1 tags> t.mp4`, with `one.srt` holding `{\an5}█` (U+2588); (d) decode `crop=40:40:940:520,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24` and read the median; (e) repeat once with an `.ass` that has `YCbCr Matrix: TV.709` and once with the header removed (the second is expected to fail on 9.0.2). Pass: every patch within ±3/255.

### Q-F2b. A correction found on the way: the shaping failure was the build, not the font

The first pass blamed FreeSerif (Gujarati) and FreeSans (Devanagari) for "no Indic shaping tables". The sibling track had already found that **ffmpeg before n9.0 draws `subtitles` in simple shaping** (`research/devotional-sound-script-fixtures/README.txt`). I re-ran both exhibits (M): the same `.srt`, the same font, one run through each build. **`subtitles` on 6.1.1, n7.0 and n8.0: ink width 1597 px for the Gujarati line, conjuncts unformed (Devanagari, 6.1.1 only: 940 px). `subtitles` on n9.0.2: 1172 px and 666 px, correctly shaped**; the `ass` filter on 6.1.1, n7.0 and n8.0 also gives 1172 px for the Gujarati line. FreeSerif and FreeSans shape correctly when the renderer does complex shaping. Source: `vf_subtitles.c` adds the `shaping` option to the `subtitles` filter only in n9.0 (n8.0 had it on `ass` only, so the `subtitles` filter's field stayed 0, which is simple shaping). **Consequences:** (a) "A font without Indic shaping tables fails silently" is wrong as written and is rewritten in the playbook (Pitfalls, Exercise 7) and above (Q8, Summary 14); (b) the exhibit is now a two-row picture, 6.1.1 on top (fails) and n9.0.2 below (correct), made from the same SRT, in `gujarati_shaping_freeserif_2026-10-19.png`; (c) on the PC the check in Exercise 7 is also a **build check**: if the PC's `subtitles` filter shows the top row, the build is older than n9.0, whatever font is chosen. The re-cut line carries the non-sacred test words only (Nudge 1 of the review).

### Q-F3. Google Photos "Back up device folders": what is on by default

**What Google documents (read 2026-10-19 in a headless browser, Android tab, sections expanded; [12]).** "Important: When you turn "Backup" on, your chosen device folders are automatically backed up too, not only your camera. You can choose to automatically backup all folders, or turn "Backup" on or off for individual device folders." Steps: Photos settings, Backup, "Back up device folders", a toggle per folder, and "Optional: Turn Back up all device folders on or off. If "Back up all device folders" is on, photos in new device folders automatically back up." **The page lists no default folders and says nothing about MIUI, One UI, ColorOS or Funtouch.** Removal: "turn off backup", then delete the backed-up items on photos.google.com, and "leave backup off" so the local copy is not deleted; the page does not state that turning backup off leaves already-backed-up items in place (that reading is an inference).

**What I could not establish.** Which folders are on by default on each skin: no Google or OEM page listing them was reachable (Samsung's support page timed out in the headless browser; the search allowance was spent). From recollection (J, not sourced) a fresh Google Photos set-up backs up the Camera folder (`DCIM/Camera`) and leaves other folders off with "Back up all device folders" off, but it varies by skin and app version, and an OEM gallery may have its own cloud sync (Samsung Gallery to OneDrive is documented; Xiaomi's ended 2022-10-25 [50]; Oppo, Vivo, Realme and OnePlus clouds UNVERIFIED).

**What changes (K1).** K1 cannot name a safe folder from a source. It now **asks first**: is "Back up all device folders" on? That is the first question in the her-turn conversation (Sat 6 Mar) and in the reveal-weekend check. The app-folder route (a new folder, or VLC's) is safe only if that switch is off; whether a folder inside another app's private `Android/data` directory counts as a device folder is UNVERIFIED. If the switch is on or unknown: the tablet or the stick, or, with her yes, switch that folder off before the copy.

### Q-F4. The Redmi 9A class: H.264 High 4.1 at 8 Mb/s, and the real scaler

**Decode (C, from specifications; no handset).** MediaTek's Helio G25 page (the Redmi 9A's chip, MT6762G, per GSMArena [27]; [66]): "Video Playback: H.264, H.265 / HEVC; Video Playback FPS: 1080P @ 30 fps". P1 is 1080p at 24 fps, inside that envelope, and H.264 level 4.1 allows 1080p at 30 fps with a peak of 50 Mb/s (62.5 for High) (J, from the H.264 level table, not re-opened), so 8 Mb/s is far inside the level. **Not stated anywhere I read: the H.264 profile and the bitrate the chip decodes.** The Android page lists only Baseline (Android 3.0+) and Main (6.0+) decoders as required [18], re-read today with the same result. So **High 4.1 at the 8 Mb/s cap on a Redmi 9A is UNVERIFIED on a handset**; T-M6 row 3 measures it (play the cap-bound C3 clip, not only the slice).
**Her phone is not necessarily this one.** Specs of the class, for O-43 planning: GSMArena lists the Redmi 9A with microUSB 2.0 with OTG and a microSDXC slot [27] (read 2026-10-19), which retires the "micro-USB class is UNVERIFIED" line for the stick route (g) for this model only.

**Scaler (M).** The note's 0.71 / 1.09 / 1.05 figures used an ideal bicubic. The phone's real scaler is not documented in anything I could read, so I bracketed it: a black line of width w on cream at 1080p, scaled to 1280x720 device pixels, at **twelve sub-pixel phases** (a 2/3 scale repeats every 3 source pixels), through six scalers. Contrast retained (1.00 = full); minimum over the phases, then mean (`scaler_bracket_720p_panel_2026-10-19.csv`).

| Scaler | 1 px | 2 px | **3 px** | **4 px** | 6 px |
|---|---|---|---|---|---|
| Catmull-Rom, support-scaled (the note's "ideal bicubic") | 0.36 / 0.50 | 0.67 / 0.85 | **0.88 / 1.01** | 1.00 / 1.04 | 1.01 / 1.03 |
| Lanczos 3 | 0.37 / 0.52 | 0.69 / 0.89 | 0.91 / 1.04 | 1.01 / 1.07 | 1.01 / 1.05 |
| Area (box) average | 0.38 / 0.56 | 0.75 / 0.90 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Bilinear, support-scaled (triangle prefilter) | 0.33 / 0.44 | 0.61 / 0.77 | **0.83 / 0.93** | 0.94 / 0.99 | 1.00 / 1.00 |
| Bilinear single-tap (GPU texture sampling, no prefilter) | 0.25 / 0.52 | 0.63 / 0.86 | 0.88 / 0.98 | 1.00 / 1.00 | 1.00 / 1.00 |
| Nearest | 0.00 / 0.58 | 0.50 / 0.92 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |

Reading: **under every scaler and phase a 3 px line keeps at least 0.83 and a 4 px line at least 0.94, so the 3 px decoration and 4 px meaning-bearing floors do not depend on the "ideal bicubic" assumption.** Lines of 2 px can drop to 0.5 to 0.67 and 1 px lines can vanish under nearest or a single tap, which is the reason for the floors. The harness reproduces the earlier CSV (A and B rows, Catmull-Rom) within 0.01. What it cannot say: which scaler her phone uses, and any sharpening the OEM adds; that stays a protocol observation (T-M6 row 7 on the 720p project phone).

### Q-F5. Default fit or fill of the players

| Player | Documented default | Source |
|---|---|---|
| AndroidX Media3 `PlayerView` (the component many Android video apps are built on) | `resize_mode` **fit** ("Default: fit"); other modes fixed_width, fixed_height, fill, zoom | [67], read 2026-10-19 |
| Apple `AVPlayerLayer` (the component of iOS players) | `videoGravity` default **`resizeAspect`**: "The video preserves its aspect ratio and fits it within the layer's bounds" | [68], read 2026-10-19 (the first pass had only a digest of the `resizeAspectFill` page [32]) |
| YouTube | fill is a user action (crop-zoom for tall screens) | [31] |
| Android gallery (OEM), Google Photos, Apple Photos, WhatsApp, Telegram | **no vendor documentation found** | not documented in anything I could read |

The two platform defaults are for the components, not for the five apps, which can override them. The vendor apps' behaviour, and the **fill-crop card measurement**, remain the maker's: T-M6 row 4 (read the first visible percentage at the top and bottom, in fit and in fill, per player). The design rule is unchanged: expect a 9% to 10% crop in fill, keep type in the central 80% of the height.

### Q-F6. Pushtimarg: an image on a phone surface, and the morning bell and lamp

**A deity image on a phone surface (lock screen, thumbnail, wallpaper).**
- **No sampradaya page I read says anything about phones or screens.** I read the sampradaya's seva page and its FAQ page in a headless browser today ([69], [70]), the Pushtimarg sprint's notes (`research/pushtimarg-world.md`, [72]) and keyword-searched both pages' text for phone, mobile, wallpaper, screen, photograph and picture. The one haveli FAQ that might have been relevant (PushtiDham) answered HTTP 405 and was not read.
- **What the tradition does say bears on the question.** (1) A picture can be a svarupa: the FAQ carries a devotee's account of a "Chitra Swaroop-Shrinathji" that "had been pusht" by a Goswami and is served "from Mangala to Shayan" [70]; the sprint's finding is that the same print can be décor in one house and a living child in another, and **a film cannot tell which by looking** [72, F6]. (2) No page forbids reproduction. (3) At Nathdwara phones are barred inside the temple [72, F6, independent portal]. (4) Seva scenes carry no phone and no street clothes (PR14 [72]).
- **So O-42 is answered with the tradition's own norm as follows (J):** there is no stated rule for a phone, and the stated reason for care (an image may be a svarupa in seva, and a phone lock screen is touched all day) stands. The sprint's rule PR2 and PR4 applies unchanged: **no svarupa image on any phone surface unless the maker knows it is hers to show and her own answer allows it**, never a photograph of her Thakorji taken without her knowing. The default in this playbook (none; her script line, a lamp or the object) is the tradition's own default carried to the phone. The one question left for her is a question, not a decision: "would you want an image of Thakorji as this film's picture on your phone?", asked at the her-turn conversation (Sat 6 Mar).

**The morning ghanta and diya: are they her household's practice?**
- **The bell.** The sampradaya's published daily routine for a household that serves Thakorji at home says, at Mangla: "Thinking of ringing noise from the small necklace around the neck of cows of Vraja, one should ring the bells thrice and blow the Sankh" [69]. So the bell, rung three times with the conch, **is in the tradition's own morning routine**, and it carries a meaning (the cows' bells of Vraj).
- **The lamp.** The same page puts a lamp at night: at Shayan, "keep a small/soft lamp on" [69]; Rajbhog offers "Dhoopdeep". **It does not put a lit diya at Mangla in the text I read.** (The sprint's Mangla light, "a single lamp or stove flame", is its own scene suggestion, [72].) The advisor's "first light is the flame she lights" therefore rests on the maker's knowledge of her morning, not on the sampradaya's text.
- **Her household.** The page itself says these rituals "should not be viewed with rigidity" because they are "also varying among the main seven houses" [69]; whether her household serves Thakorji at home, and which darshans it keeps, is the sprint's open Q3 [72]. **Neither the bell nor the lamp is confirmed as hers.** The advisor's cold-open idea is sound for a household that does Mangla; if hers starts another way, use that (the review says the same). Recording rule: the bell is an object; recording it when she is out is not recording her (D-17), but a seva article is shown by hands and never on the floor or in the wrong place (PR10 [72]).

### Q-F7. O-43, from the maker's own knowledge, never by looking at her phone

**Not answered.** Only the maker can; this pass cannot ask anyone (D-03) and must not look at her phone (D-02). Fill the table from memory; leave a field blank rather than check. Each blank falls to the default in the last column.

| Field (O-43 and backup state) | Maker's answer | Drives | Default if unknown |
|---|---|---|---|
| Make and model | | K1, screen class, USB port | treat as a Redmi 9A class phone (J) for the fill and caption tests |
| Android version | | Quick Share, app pinning (Android 11+ on Pixel steps [49]), whether MTP reaches app folders | assume Android 10 to 12 |
| Screen: size and resolution (720p or 1080p) | | scaler and sharpness (Q-F4), crop (K2, T-M3) | 720x1600, 20:9: crop 10% in fill |
| Free storage (Settings, Storage; ask her at the reveal check, with her yes) | | P1 or P2 (Size and storage check: **at least 1 GB free for P1**) | treat as under 1 GB: P2 by cable, P1 waits for the tablet or the stick |
| USB port and whether it takes an OTG drive | | stick (g) | micro-USB with OTG for the Redmi 9A class [27]; her port unknown |
| The app she watches video in (gallery, YouTube, WhatsApp, VLC) | | which player's fit or fill matters (Q-F5) | the gallery, in fit |
| How she holds it (sideways or upright) | | K3: sideways design, upright is degraded | sideways, and the hand-over says "turn it sideways" |
| Reading glasses for the phone | | caption size (FS 28 floor stays) | assume yes |
| Text-size setting | | nothing in the file (a burned caption ignores it); tells how much she needs large type | assume large |
| Google Photos backup on or off; **is "Back up all device folders" on** | | K1 first question | treat as on |
| The phone maker's own gallery sync (Samsung Gallery to OneDrive; others UNVERIFIED) | | K1 | treat as on |
| WhatsApp chat backup with "Include videos in chats" | | hygiene, Pitfalls [7] | treat as on |
| Is her Google account shared with anyone | | W-48 (a shared library shows a copy before the ledger closes) | treat as shared |

### What these findings change, by section

| File | Section (as it exists) | Change |
|---|---|---|
| `playbooks/mobile-delivery.md` | Step 4, K2, Exercise 7, T-M6 row 11, Pitfalls (shaping, tinted captions), What we leave out, K1, Step 7, Step 8, Size and storage check, Decision 14, T-M6 row 13, Sources | applied in place today (see its changelog line) |
| `skills-staging/mobile-phone-delivery/SKILL.md` | steps 1, 5, 9, 10, 11; Guardrails; Quality bar; protocol rows; Sources | applied in place today |
| `playbooks/theatrical-delivery.md` | **Step 6 (burn in the captions) and T1 (settings card)** | the tinted-caption rule becomes "white or neutral by default; tinted only after the twelve-patch caption test passes on the PC build and the master is tagged"; add "an `.ass` carries `YCbCr Matrix: TV.709`"; add the shaping build check (`subtitles` before n9.0 shapes in simple mode) |
| `playbooks/format.md` | **Step 8 (harden the slice), caption bullets** | the same two lines for the venue burn-in |
| `playbooks/toolchain.md` and `.claude/skills/free-creative-toolchain/recipes/r9_deliver.sh` (orchestrator edits; `.claude/` is not touched here) | **Step 11 captions; the r9 caption recipe** | the libass colour warning is now "ffmpeg before n7.0 assumes BT.601; from n8.0 an `.ass` without the header does too"; the recipe must name the header |
| `research/devotional-sound-script-fixtures/shaping_fixture_noto.ass` and the sibling's PC commands | the ASS pages | add `YCbCr Matrix: TV.709` to the header (its colours are near-neutral, so no visible effect today, but it would shift a tinted one on n8.0 and later) |
| `research/hindu-visual-fixtures/README.txt` and `research/hindu-visual.md` (M-H1) | the 720p-panel claim | none needed: the 3 px and 4 px floors hold under the six scalers (Q-F4) |
| `playbooks/music-sound.md` | **Exercise 6; the cold-open sound** | a candidate first sound, the shrine bell rung three times, backed by the sampradaya's Mangla text (Q-F6); the maker confirms it is hers before any cue is mapped |
| `research/pushtimarg-world.md` (the sprint's note, not edited here) | F6 | one line for the sprint: a phone surface is not covered by any page read; PR2 and PR4 carry over |
| `DECISIONS.md` (orchestrator) | O-42 to O-44 rows still missing; D-31 | O-42's answer (Q-F6) and O-43's intake table (Q-F7) can be added as the recommendation text |

*Not done, because it needs the maker or the hardware: the PC re-run of the caption test and of Exercise 7; the WhatsApp device test (Decision 12); the Redmi 9A decode and scaler (a project phone); the fill-crop card per player; the O-43 answers; one reading of the WhatsApp pages in the maker's browser (optional); the Pushtimarg Q3 answer on what her household keeps at home.*
