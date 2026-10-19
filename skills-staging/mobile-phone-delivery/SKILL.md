---
name: mobile-phone-delivery
description: Makes, encodes and checks the phone deliverables for the Life Journey film (the phone master P1, the small P2 copy, phone captions, the phone-safe frame and the project-phone protocol), and sets the keepsake and sharing rules for her phone and relatives' phones. Use when a phone file, phone caption, phone-safe shot, keepsake route, relatives' copy or any on-phone image is planned, encoded, tested or signed off.
---

# Mobile phone delivery

## Purpose

Make every Life Journey deliverable play beautifully on a phone (D-27) without weakening the venue master. There is one phone master, cut from the ProRes master, with measured phone floors and a repeatable device test. The reasoning, the decision tables and the open questions live in `playbooks/mobile-delivery.md`. This skill is the agent form of that playbook.

## When to use

- Encoding or checking P1 (the phone master) or P2 (the small copy).
- Setting phone caption burn-in, the phone-safe frame, the fill-crop card or the dark-step tests.
- Choosing or testing her keepsake route, or a relative's copy.
- Reviewing any image that appears on a phone surface: lock screen, thumbnail, icon, page frame or forwarded frame.

## When not to use

- The venue master, DCP, venue captions or hall loudness: use `theatrical-delivery-and-rights`.
- Story choices, or which deity or motif to show: those are the maker's decisions (O-42, O-44). This skill applies only the phone constraints.
- ArtCraft app steps: use `craft-apps-visual-refinement` or `craft-apps-motion-refinement`.
- Consent or labels for AI-altered photos: use `ai-photo-to-animation-pipeline`.
- Any send or upload of the film before the reveal. That is never allowed.

## Procedure

1. Confirm the phone unknowns (O-43 and the backup state) from the maker's written answers (the intake table is `research/mobile-delivery.md`, Follow-up research, Q-F7). The backup questions are: does Google Photos back up, **is "Back up all device folders" on (K1's first question)**, does the phone manufacturer's gallery sync run (Samsung Gallery to OneDrive; others UNVERIFIED), is the account shared. Never check her phone (D-02). Anything unknown defaults to "treat it as on" (K1).
2. Start from the ProRes 422 HQ master (W-15). Never start from the venue file or from RGB frames.
3. Encode P1 with the T-M1 template: `-crf 20`, `-maxrate 8M -bufsize 16M`, High 4.1, AAC-LC 192k, `+faststart`, metadata stripped. Keep the bracketed `lut3d` step out until Trim P is signed.
4. Encode P2 (720p, `-crf 22`, `-maxrate 4M`, AAC-LC 160k) for low-storage phones and for relatives.
5. Burn the phone captions: Latin text at FontSize 28, MarginV 40, Outline 2, white, at most 36 characters a line, two lines. Size Gujarati by the height of KA (K2), not by FontSize 28: **Noto Sans Gujarati is the default caption face (FontSize 26.2 for the 3.8% target)**, citing the sibling's Q9 Gujarati paragraph: Hind Vadodara has no Gujarati digits (U+0AE6 to U+0AEF), so any date falls back to FreeSerif, while Noto Sans Gujarati carries the digits, the Om sign and every conjunct; use Hind Vadodara (24.8) only for lines without digits. Run the shaping check first (it also checks the build: `subtitles` before ffmpeg n9.0 shapes in simple mode). The master carries a BT.709 tag; an `.ass` carries `YCbCr Matrix: TV.709`.
6. Run the colour-patch test (within ±3/255, twelve patches) on the PC build of each template (W-16), and the twelve-patch caption colour test (Exercise 3 step 5 of the playbook). Tinted caption colours are allowed only on a build that passes it.
7. Measure the final MP4: the ffprobe fields, atom order (`moov` before `mdat`), true peak at or below -1.0 dBTP and loudness at -16 LUFS. Re-encode with `volume=-0.5dB` if the peak is too high.
8. Check each shot's frame: must-read type at x-height 3.2% or more (3.8% target), strokes 4 px or more, action and hands inside the central 80%, caption zone clear, safe-area overlay on three frames.
9. Set a thumbnail with light in it: the first frame of her object or her hands in the opening (W-32, W-33), never a title card and never a deity (O-42); the same frame marks the folder on the venue sticks. Name the file with a neutral code until the reveal.
10. Run the project-phone protocol (T-M6, thirteen rows) on an Android in the 2019 to 2021 class and an iPhone, with no accounts on either. A failed row gets fixed and re-run.
11. Choose the route with K1 (her phone: cable, with her yes, after the reveal; ask first whether "Back up all device folders" is on, since the app-folder route is safe only if it is off; otherwise the tablet or the stick) and K4 (relatives: P2 as a WhatsApp document, after the ledger closes). Free space first (keyed on O-43): P1's 737 MB ceiling plus a 200 MB margin means at least 1 GB free on her phone; if O-43 reports less, P2 goes on by cable and P1 waits for the tablet or the stick.
12. Log every send in the rights log (T8 `phone_share`) and the sharing table (T-M4). Nothing is sent before the reveal or before the ledger closes.

## Checklists

**File checks (every output)**
- ffprobe: H.264 High; level 4.1 for P1 and 3.1 for P2; yuv420p; color range tv; bt709 primaries, transfer and matrix; 24/1 fps; frame count equal to the timeline.
- The master carries `color_space=bt709` before any burn-in; atom order `ftyp, moov, ..., mdat`; `+faststart` present.
- Metadata: no title, comment or location. The hash is recorded in the manifest.
- Colour patches within ±3/255 (P1 and P2 measured at 3/255 and 2/255 in the container).
- Final MP4 true peak at or below -1.0 dBTP; loudness -16 LUFS.
- P1 grain survival at least 70% of the master (CRF 20 gives 73%; CRF 22 gives 43%, which fails).
- File name is a neutral code before the reveal.

**Frame checks (every shot with `phone_safe`)**
- Action and hands inside 10% to 90% of the height; text inside 5% to 95% across and 12% to 88% down.
- Caption zone: venue 78% to 93% of height; phone 68% to 86%.
- Strokes: 4 px for meaning-bearing lines, 3 px for decoration, dots 6 px, holes 4 px, hatch 3 px on 9 px pitch. No 1 px lines and no hairlines.
- Text contrast at least 4.5:1 (target 7:1). Captions white or neutral by default; a tinted caption colour only after the twelve-patch caption test passes on the PC build.
- No deity image on any phone surface without the maker's written decision (O-42).

**Protocol rows (T-M6)**
1 hygiene; 2 copy by cable; 3 one-tap play; 4 fill-crop card per player; 5 caption burn-in read at 35 cm and 50 cm; 6 dark steps at 100 and 500 lux; 7 strokes and colour; 8 thumbnail and sort position; 9 chat round trip (fixture only, optional); 10 sound tone ladder; 11 Gujarati shaping on the PC (P-LOCK); 12 slice fixture played from the project phone's gallery (P-LOCK); 13 scrubber page opened from the project Android's file manager and from Files on the iPhone, recording whether the video plays (measures the page's demotion).

**Sharing checks**
- Before the reveal: nothing reaches any phone.
- After the reveal: cable to her phone, with her yes.
- Relatives: only after the ledger closes (W-48), with the maker's yes, as a WhatsApp document. Log `phone_share = relatives_after_ledger`. Release lines 4d to 4g apply.
- Guests: no QR code and no live link on the night.

## Quality bar

- Must-read type: x-height 3.2% (hard floor) and 3.8% (target), which is 41 px at 1080p.
- Phone captions: FontSize 28, white, at most 36 characters a line, two lines, 20 characters a second.
- A phone copy is a faithful reduction: master to P1 to a chat proxy equals master straight to the proxy, within 0.01 (M).
- Every number is labelled (M), (C), (J) or UNVERIFIED. Gallery, messenger and fill behaviour are measured, not assumed.
- Black is pinned at code 16. The Trim P starting value is 4 to 7 IRE at codes 24 to 40 (J), tuned on the phone.

## Guardrails

- **Respect and the Hindu-only rule (D-28).** "Indian" always means Hindu: Sanatan Dharma and its sanskriti. No Mughal or other Islamic motifs and no Christian motifs, ever. Leave out shared or ambiguous decoration by default: jaali, paisley, mehndi borders, arches, tile patterns. Church-shaped bells, candles where a diya belongs, a flat gold-disc halo drawn as in a church icon, crosses, winged figures: Christian or colonial layer, none. The ghanta (temple bell), the diya and the prabhavali or prabhamandala are Hindu and are not excluded by this rule. The swastika in a thumbnail or lock-screen still is out by default (O-44).
- **Deities** are shown with correct iconography and respect. No deity image on a phone surface until the maker decides in writing, as her proxy (O-42). The default is her script's end-card line, a lamp or the object.
- **Rights.** Every forwarded copy is a public distribution, so no copy goes out before the ledger closes (W-48). Fonts must be OFL with a rights-log row (W-21). Nothing uncleared goes into a phone copy.
- **Privacy.** No personal media in git. The repo is public, so use person IDs only. Project phones carry no accounts unless the maker decides otherwise (Decision 12). Nobody checks her phone before the reveal (D-02). No phone test or copy leaves the project phones before the reveal.
- **Authority.** The register wins. This skill does not edit `DECISIONS.md`, `CHARTER.md`, `ROADMAP.md`, `CLAUDE.md` or anything under `.claude/`.

## References

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
58. Local: `CHARTER.md`; `DECISIONS.md` (D-02, D-05, D-15, D-24, D-27, D-28, D-31, W-04, W-15 to W-20, W-25, W-26, W-30, W-33, W-35, W-46 to W-48, O-30, O-43); commit `ac6711e`. O-42 to O-44 are defined in `reviews/04-hindu-mobile-briefs-review.md`.
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
