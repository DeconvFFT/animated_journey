# Phone delivery: her film and her keepsake on a phone

*Playbook for the maker. Track `mobile-delivery`. Scribe draft, Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27), revised the same day against `reviews/mobile-delivery-round1.md` (round 1, verdict revise). Built from `research/mobile-delivery.md` (including its "Follow-up research (round 1)"), `CHARTER.md` and `DECISIONS.md`. **Status: round 1 applied; awaiting the round-2 review. Reconciled with `DECISIONS.md` after the her-world merge (2026-10-19):** the phone files are PH1 and PH2 (W-63), the her-turn conversation is Sun 7 Mar after about 14:00 (W-48), O-42 is now O-64 and O-43 is now O-54, and the fonts, the cold open, the hum and the deity rows follow W-21, W-76, W-65 and W-61. Under `CLAUDE.md`, nothing here counts as done until `fable-advisor` scores every rubric line 4 or higher, and the review is saved in `reviews/`.*

**How to read the claims.** `[n]` points to the Sources section; each entry says when the page was read and whether it was only seen as a search digest. **(M)** was measured in the cloud container on synthetic fixtures. **(C)** is computed from published numbers. **(J)** is a team judgement. **UNVERIFIED** means not yet checked; the protocol in Templates measures it on the project phones or the PC. **TODO(research)** marks a gap the research did not close. `D-`, `W-` and `O-` IDs point to `DECISIONS.md`. Where an ID is defined only in a review, the text says so.

---

## Why this matters for our film

- **The phone is a delivery target (D-27).** The film and any keepsake must play beautifully on a phone as well as on the venue screen: phone-legible text and captions, a phone-safe frame, and a phone file that survives sharing.
- **Her phone is Android (D-31).** StatCounter's September 2026 India figures put Android at 93.89% of mobile OS traffic and iOS at 6.05% [25]. That is a web-traffic statistic, not her phone: **UNVERIFIED for her** until question O-54 (which absorbs O-43) is answered.
- **Her screen is probably the class the plan worries about most (J).** That means a 2019 to 2021 mid-range Android, 720p or 1080p, 20:9. The example used is the Redmi 9A class: 6.53 in, 720x1600, 400 nits typical [27]. The six most common Indian phone viewports in September 2026 are all between 19.5:9 and 20:9 and together make up 37% of Indian mobile web traffic [26]. Phones this tall crop a 16:9 picture by about 9% to 10% at the top and bottom (C).
- **Sideways is the only view that works for captions (M, C).** At 35 cm on a 6.1 in screen, a caption at FontSize 23 has an x-height of 0.40° when the phone is held sideways, and 0.23° upright in a chat. The target for a 50+ viewer is 0.35°. Upright viewing is degraded by design, so the hand-over must say "turn it sideways".
- **Her keepsake has to be a file she can tap, not a web page.** Self-contained HTML does not work on her phone. On iPhone, Quick Look "will not run JavaScript" and does not load relative references [38][39][40]. On Android, a file opened from a file manager gets a `content://` address whose relative video path fails [41][42][43]. Embedding 199 to 737 MB of video in a page is not realistic (C).
- **Every copy is a public distribution.** A forward reaches five chats at a time, and a relative who re-forwards a forwarded copy reaches one more group chat (the page's own words, re-read 2026-10-19) [4]. The rights log does not yet model that, so sharing is a rights decision, not a convenience.
- **The phone copy is her room.** Her script on the cards, her object, her room sound and her end-card line are what the phone shows. Personal before generic: the phone file should feel like her film, not a generic one.

---

## Core principles

1. **One phone file, PH1, cut from the ProRes master.** Encode from the 10-bit 4:2:2 master (W-15). Never encode from the venue file, which has the venue captions burned in, and never from RGB frames. A bare RGB-to-YUV step gave a 23/255 colour error on pure red in the container (M).
2. **Design for landscape fit.** The phone file is shown sideways at 16:9, with bars or a 9% to 10% crop. Keep the picture and every must-read word inside the central 80% of the height, with a cushion.
3. **Measure on the device, not on the spec sheet.** Phone numbers that are computed (C) or measured on a stand-in (M) are provisional until the protocol runs on the project phones.
4. **Her copy is a file on her phone, put there by cable.** Not a link, not a web page, not a cloud share. The offline scrubber page in W-30 is demoted to a laptop and archive companion (O-30 decides at G-SLICE).
5. **Nothing reaches a phone before the reveal, and nothing reaches a relative's phone before the ledger closes (W-48).** After the ledger, a WhatsApp document is the only relative route, and only with the maker's yes.
6. **No gesture is required.** One tap to play. No pinch, no scrubbing, no QR code, no menu. The film finds its chapters through cards in the picture. Any on-screen control respects the 44 by 44 CSS pixel target [52].
7. **Hygiene before quality.** Project phones carry no accounts. Her backup state is checked before any copy lands on her phone, because a camera-roll copy can become a cloud copy at once.
8. **The Hindu-only rule and the respect rule apply on the phone too.** That covers the lock screen, the gallery thumbnail, the app icon and any page frame (D-28). See What we leave out.

---

## How to do it, step by step

**Step 1. Get the unknowns in writing (weeks 1 to 2).** Answer the O-54 questions (which absorb O-43) from your own knowledge: make, model, Android version, screen (720p or 1080p), free storage, USB port type (and whether it accepts an OTG drive), the app she watches video in, whether she holds the phone sideways, whether she uses reading glasses for it, and her text-size setting. Answer the backup questions: does her Android back up photos to a cloud account, does the phone manufacturer's gallery sync run (Samsung Gallery to OneDrive; others UNVERIFIED), **is "Back up all device folders" on in Google Photos** (K1's first question), and is her account shared with anyone? The research note's O-43 intake table (Follow-up research, Q-F7) lists every field with its default. **Do not look at her phone (D-02).** Write the answers into a phone profile. Anything unknown falls to the decision tables K1 to K5 (Templates), and the default is "treat it as on".

**Step 2. Add the phone rows to the settings card (T1, signed by Sun 1 Nov).** Write in: PH1 and PH2 specifications; SDR only (no HDR file); BT.709 tags; 24 fps; online loudness -16 LUFS integrated and -1 dBTP, measured on the final MP4 (W-19); no HEVC file. The phone row sits beside the venue row (W-16, O-14). The font rows (W-21) and the burn-in path (`subtitles` or `ass`, decided by the PC A/B of Exercise 7; W-75) go on the same card.

**Step 3. Encode PH1 from the master, and PH2 for relatives' phones.** Use the T-M1 templates in Templates. PH1 is `-crf 20` with an 8 Mb/s cap. PH2 is 720p at `-crf 22`. Until the reveal, name the files with a neutral code, not her name and not her language. Run the encodes in the working folder with relative file names.

**Step 4. Burn the phone captions.** Latin captions: FontSize 28, MarginV 40, Outline 2, white, at most 32 characters a line (measured to fit the 90% by 90% box in both scripts at FontSize 28; the venue file keeps its own guide of 42, W-18), two lines, block at 68% to 86% of the height. Gujarati captions do **not** use FontSize 28. Size them by the height of the base letter KA (K2): for the 3.8% target, **FontSize 26.2 with Noto Sans Gujarati, the caption face** (W-18, W-21; it carries the digits, the Om sign and every conjunct string it shaped). Hind Vadodara is not used for any date or Samvat (it has no Gujarati digits, U+0AE6 to U+0AEF, so a date such as સંવત ૨૦૮૩ falls back to FreeSerif), and Mukta Vaani is not used for Gujarati text (unfused conjuncts when tagged Gujarati) (W-21). On any ffmpeg older than n9.0 an Indic line is burned with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in its header), never `subtitles` or `drawtext` (W-75). Run Exercise 7 before any Gujarati text is burned.

**Step 5. Check every file.** Run the T-M1 checks: the ffprobe values (and the master's BT.709 tag before any burn-in); atom order with `moov` before `mdat`; twelve colour patches within ±3/255; true peak after AAC (measure the final MP4; if it reads above -1.0 dBTP, re-encode with `volume=-0.5dB`); grain survival for PH1 (at least 70% of the master; CRF 20 passes at 73%, CRF 22 fails at 43%); type floors; the safe-area overlay on three frames; metadata; and the file name.

**Step 6. Run the project-phone protocol (T-M6).** Use two project phones with no accounts: an Android in the 2019 to 2021 class, and an iPhone for the relatives' route. Start with the hygiene row. The protocol has thirteen rows and takes about 45 minutes per device once practised (row 13 is two minutes). Photograph each screen. Use fixture content only. **Her phone is tested only after the reveal, with her yes.**

**Step 7. Set the thumbnail and check the sort position.** A cold open that starts in black gives a black thumbnail (check 8). Set a poster frame that has light in it. **The thumbnail is the first frame of her object or her hands in the opening (W-32, W-33): never a title card and never a deity (O-64, which absorbs O-42; see What we leave out), and the same frame marks the folder on the venue sticks so the maker recognises the file in a hurry.** Check where the file sorts in each gallery, because stripped metadata may move it.

**Step 8. Choose the route with her yes, on reveal weekend.** First ask K1's question, with her yes and her phone in her hand: **is "Back up all device folders" on?** The default route is a USB File Transfer copy by cable, into a folder her backup does not read or into an app's own folder such as VLC's, then a tap in her gallery; it is safe only if that switch is off (K1). An Android tablet in app pinning, or the stick, is the route if it is on or unknown (O-04 for the tablet). **Free space first (keyed on O-43):** PH1's ceiling is 737 MB; with a 200 MB margin she needs **at least 1 GB free** on her phone. If O-43 reports less, PH2 goes on by cable and PH1 waits for the tablet or the stick. Do not do the cable step before she has said yes, and never on her phone before the reveal. After the copy, rename the file to the film's title in her script (not a transliteration) and offer the lock-screen still (W-73, W-74); nothing goes to relatives yet, and the promise of a family copy is spoken, with a named date.

**Step 9. Share with relatives only after the ledger closes (W-48).** Send PH2 (or PH1 where storage allows) as a WhatsApp document, once, with the maker's yes. Record each send in the rights log with `phone_share = relatives_after_ledger`. Tell each relative that a forwarded copy cannot be recalled (release lines 4d to 4g). Guests get no QR code and no live link on the night.

**Step 10. Keep the fallback honest.** Phone-by-cable is part of the premiere failure ladder (W-52). Test it once before the 26 February pack list (T11 in `playbooks/theatrical-delivery.md`), with a cable and an adapter for her phone class, on a project phone and on the spare laptop, and with PH1 on both USB sticks beside the venue file (W-52). Record the result in the sharing table (T-M4). A failed check goes back to the encode or caption step, not into a note.

---

## Learn-by-doing exercises

Each exercise runs on synthetic material or on the project phones. None touches her phone, her photographs or a family account.

### Exercise 1. Write the phone profile and wipe the project phones (45 to 60 minutes)

- **Goal.** A written phone profile (Step 1) and two project phones with no accounts.
- **Steps.** (1) Write the O-43 and backup answers as a short table. (2) On each project phone, work through the hygiene row (T-M6 row 1): no Apple, Google, Samsung or Microsoft account; Google Photos and iCloud Photos off or absent; WhatsApp absent; airplane mode; location off; brightness 50% with auto-brightness off; screen mode recorded. (3) Photograph each check.
- **Time.** About an hour for the profile and two devices.
- **What good looks like.** Every box ticked in writing. Every unknown in K1 has a stated default. No media on either phone.

### Exercise 2. Encode the ladder from a synthetic master (about an hour per 12-minute PH1 in the container; PC speed UNVERIFIED)

- **Goal.** See the bytes and the grain for yourself.
- **Steps.** (1) Take a 12-second synthetic master. The research fixtures are the model: a photo push, drawn flat colour with 4 px outlines, and dense lines. (2) Run the PH1 template, then the PH2 template. (3) Run `ffprobe` on each output and check the atom order. (4) Record bytes and Mb/s in a table and compare with the ranges in Templates.
- **Time.** About one hour, mostly waiting.
- **What good looks like.** PH1 at CRF 20 lands near 2.0 to 2.7 Mb/s on drawn and photo content. PH2 lands near 0.4 to 0.9 Mb/s. The ffprobe fields match T-M1, and `moov` comes before `mdat`.

### Exercise 3. The colour-patch test on the PC build (W-16; about an hour, an hour and a half with step 5)

- **Goal.** Prove that the Windows ffmpeg makes the same colours as the container's, for the picture and for the burned captions.
- **Steps.** (1) Make twelve patches, including near-blacks, cream and saturated red. (2) Encode each template (PH1, PH2) and a control made with bare `-pix_fmt yuv420p` from an RGB PNG. (3) Compare decoded values with the originals. (4) Repeat with an identity `.cube` through `lut3d` placed before the PH1 filters. (5) **Caption colours (Follow-up research, Q-F2):** first `ffprobe` the master for `color_space=bt709`. Then burn each of twelve caption colours (white, grey E6, cream F3E9D2, ochre F0B323, pure red, film red B5282B, film green 2E7D32, indigo 1F2A5A, skin, grey 50%, grey EB, ink 181410) as a solid block (U+2588) through the PH1 chain and compare the decoded block with the source colour, once from an `.srt` with `force_style` PrimaryColour, once from an `.ass` that has `YCbCr Matrix: TV.709` (example: `research/mobile-delivery-fixtures/caption_ycbcr_matrix_example_2026-10-19.ass`), and once with that header removed.
- **Time.** About an hour; step 5 adds about half an hour.
- **What good looks like.** PH1 and PH2 within ±3/255 on every channel. The bare control shows the known fault (23/255 in the container). If the PC build fails, change the template or the build and re-run. Do not accept a close number. For step 5: in the container, ffmpeg n9.0.2 built from source passed (worst 3/255 for the `.srt` and for `TV.709` or `None`), ffmpeg 6.1.1 failed (23/255 on saturated colours), and an `.ass` with no header failed on n8.0 and later (23/255); the PC's own build is **UNVERIFIED** until this step runs on it. Only if all twelve pass on the PC may tinted caption colours be used there (T-M2).

### Exercise 4. Arm's-length captions and the fill-crop card (about 45 minutes per device)

- **Goal.** Read the phone caption and the crop as a 50+ viewer would.
- **Steps.** (1) Play the 20-second caption card in both versions (venue and phone) on each project phone. (2) Read both captions at 35 cm, then at 50 cm as a proxy for a 50+ viewer, in fit and in fill. (3) Use `research/mobile-delivery-fixtures/phone_test_p1_fillcrop.svg`. Read the first visible percentage at the top and bottom, in fit and in fill, for each player you have: the gallery, Google Photos, Apple Photos, VLC, and WhatsApp or Telegram if they are installed with fixtures.
- **Time.** About 45 minutes per device.
- **What good looks like.** The phone caption is fully readable at 50 cm in fit and fill. The venue caption may be cut in fill; that is expected. The crop reads 9% to 10%. If a player crops more than 12%, move the text higher.

### Exercise 5. Dark steps and strokes (about 40 minutes)

- **Goal.** Find the first code you can see from black at two room lights, and the thinnest lines you can see.
- **Steps.** (1) On the dark-step page, find the first patch you can tell apart from code 16, at 100 lux and at 500 lux, on a clean file and on a Trim P file. (2) On the strokes page, note whether 3 px lines show, whether 4 px lines are crisp, whether hatch at 3 px on 9 px pitch shows, and whether the equal-brightness pair (red on green) separates.
- **Time.** About 40 minutes.
- **What good looks like.** Both codes recorded. With Trim P, the detail that must be seen sits at or above the 500 lux code, and the 100 lux room does not look milky. Lines of 4 px and more are crisp. If not, enlarge the strokes in the art.

### Exercise 6. The cold-open sound ladder (about 30 minutes; a P-LOCK item with the first-sound listening test, W-06)

- **Goal.** Find which sounds this phone's speaker actually plays, and rank the candidate first sounds and the two hum takes on it. The phone decides, not taste (W-76).
- **Steps.** (1) In a quiet room at 50% volume on the project Android, play tones from 100 Hz to 3.2 kHz, one at a time. (2) Write down the lowest tone you hear clearly. (3) Play pink noise, then the same with earbuds. (4) Play each candidate first sound of Decision 7 and the two hum takes (closed-mouth and open vowel, W-65), and write pass or fail beside each. (5) Rank the candidates before beat sheet v1, Sun 6 Dec (W-76).
- **Time.** About 30 minutes.
- **What good looks like.** Speech (400 Hz to 3 kHz) is clearly audible. The cold open's first sound has energy above about 400 Hz (a spoon on steel, the cooker whistle, a hand-bell, water poured into brass), not a low room rumble. Room tone alone, a deep sea swell, a closed-mouth hum and pakhawaj bass fail on a phone speaker; a bell, a conch (thin), jhanj, manjira, tanpura, surf, the cooker and an open-vowel hum pass (W-19). If the first sound lives only below the lowest audible tone, move it up in frequency or give the cold open a visible first light within about 4 s (W-36). The phone files carry the open-vowel hum unless the closed-mouth take passes at 50% (W-65).

### Exercise 7. The Gujarati shaping check on the PC (the single shaping gate, a P-LOCK item; about an hour)

- **Goal.** Show that Gujarati captions shape correctly with the chosen OFL font **on the PC's own ffmpeg build**. This is the one shaping gate, shared with `playbooks/devotional-sound-script.md` Template K and run once at P-LOCK (W-06). Its result decides whether the PC burns with `subtitles` or with `ass` on an ASS file made from the SRT (W-75), and a native Gujarati reader reads the sheets (O-62).
- **Steps.** (1) Burn the sibling track's shaping fixture (ids `guj-shri`, `guj-ksha`, `guj-jna`, `guj-dharma`, `guj-om`, in `research/devotional-sound-script-fixtures/shaping_fixture.tsv`; add `guj-digits`) through the `subtitles` filter with Noto Sans Gujarati, the caption face, and once with Hind Vadodara as a negative control, to see its digit fallback on `guj-digits` (it is not a candidate, W-21). (2) Read the libass log lines the sibling's README names. (3) Burn this track's own test line, `research/mobile-delivery-fixtures/gujarati_shaping_freeserif_2026-10-19.srt`, and compare it with the two-row picture `gujarati_shaping_freeserif_2026-10-19.png`: the top row is ffmpeg 6.1.1's `subtitles` filter (it fails), the bottom row is ffmpeg n9.0.2 (correct), both from the same SRT and the same font. **If the PC's frame looks like the top row, the build is older than n9.0, whatever the font** (Follow-up research, Q-F2b).
- **Time.** About an hour.
- **What good looks like.** Conjuncts formed, the reph and the short-i matra in the right places, no visible virama, and the digits drawn as Gujarati digits with no `Glyph ... not found` log line. **Licences closed:** Noto Sans Gujarati and Hind Vadodara are both SIL OFL 1.1 with no Reserved Font Name (github.com/google/fonts `ofl/notosansgujarati/OFL.txt` and `ofl/hindvadodara/OFL.txt`, read 2026-10-19 [64][65]); still save each `OFL.txt` and its hash in the rights row (W-21). `drawtext` is out on any ffmpeg older than n9.0 (sibling Q10).
- **Script strings, copied exactly from the research note (Q8).** Gujarati test line: `ક્ષત્રિય જ્ઞાન ધર્મ કિ ક્ષિ`, which reads kṣatriya (the warrior order; here only a conjunct test), jñāna (knowledge), dharma, ki and kṣi (the last two syllables test the short-i sign). Devanagari test string: `श्री क्षत्रिय ज्ञान`, which reads śrī (an honorific), kṣatriya, jñāna. Both are shaping test strings, not verses. Source: `research/mobile-delivery.md` Q8, measured on the FreeSerif and FreeSans exhibits through 6.1.1 and n9.0.2.

### Exercise 8. The document route, fixture only (optional; two project devices)

- **Goal.** Learn whether a WhatsApp document arrives byte for byte.
- **Steps.** (1) Use a fixture file, never the film. (2) Take the SHA-256 on the sending side. (3) Send it as a document to the second project device. (4) Take the SHA-256 on the receiving side and compare. (5) Run `ffprobe` on the received media copy and write the resolution, bitrate and frame rate into the sharing table.
- **Time.** About an hour, plus set-up.
- **What good looks like.** The hashes match, which would make the document route lossless. Until this runs, that is **UNVERIFIED**. **This test needs WhatsApp accounts on the two project phones, which the no-accounts rule forbids. Decide Decision 12 first.**

---

## Templates and checklists

### T-M1. Phone encode templates (run in the container on 2026-10-19; Windows UNVERIFIED)

Source for every file: the ProRes 422 HQ master (W-15). Never the venue file, never RGB frames. Run the colour-patch test (Exercise 3) on each template on the PC build.

**PH1 (hers; relatives' phones as a document after the ledger).**

```
ffmpeg -i MASTER.mov -map 0:v:0 -map 0:a:0 ^
 -vf "[lut3d=trim_p.cube,]subtitles=phone.srt:force_style='FontName=<OFL font>,FontSize=28,MarginV=40,Outline=2,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,WrapStyle=2',scale=in_range=tv:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int+bicubic,format=yuv420p" ^
 -c:v libx264 -preset slow -crf 20 -maxrate 8M -bufsize 16M -profile:v high -level:v 4.1 -pix_fmt yuv420p ^
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -g 48 ^
 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -map_metadata -1 -fflags +bitexact LJ_PH1_<code>.mp4
```

- The bracketed `lut3d=trim_p.cube,` step is used only once Trim P is signed (Decision 6). Until then, delete it.
- Without a `phone.srt`, drop the `subtitles` filter.
- For a line in Gujarati or Devanagari on an ffmpeg older than n9.0, replace `subtitles=phone.srt:force_style=...` with `ass=phone.ass`, an ASS file made from the SRT with `YCbCr Matrix: TV.709` in its header and the Gujarati style at FontSize 26.2 (W-75, W-18). `subtitles` stays for Latin lines and for builds from n9.0.
- `<OFL font>` stays a placeholder until the font is chosen and its licence file is in the rights log (W-21); for Gujarati lines the default is Noto Sans Gujarati (K2).
- **The master must carry BT.709 tags before the burn-in** (`ffprobe` `color_space=bt709`). On an untagged master every ffmpeg build draws the captions in BT.601 (23/255 on saturated colours); `setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv` before `subtitles` fixes that on n7.0 and later (Follow-up research, Q-F2).
- The combined line, with an identity cube and phone captions, ran in the container on a 3-second clip and probed as High, level 41, yuv420p, tv, bt709, 72 frames (M). It is untested on Windows.

**PH2 (low-storage phones; document route).** The research note abbreviates the subtitles string with `...`. Use the PH1 subtitles string unchanged. The captions are burned on the 1080 frame before the downscale.

```
 -vf "[lut3d=trim_p.cube,]subtitles=phone.srt:force_style='<same as PH1>',scale=1280:720:in_range=tv:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p"
 -c:v libx264 -preset slow -crf 22 -maxrate 3500k -bufsize 7M -profile:v high -level:v 3.1 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -g 48 -c:a aac -b:a 160k ... LJ_PH2_<code>.mp4
```

- The PH2 `-bufsize` (7M) is twice the cap (3500k), by the same convention as PH1's `-maxrate 8M -bufsize 16M`; if a register row ever moves a cap, move its `-bufsize` with it (and `pipeline/phone/profile.json`).

**HEVC variant: not recommended (grain loss).** A template only for a grain-free finish. Re-test only if the finished film has little or no grain.

```
 -c:v libx265 -preset medium -crf 18 -x265-params vbv-maxrate=6000:vbv-bufsize=12000:keyint=48 -pix_fmt yuv420p -tag:v hvc1 <same tags> ...
```

**Checks on every output.**

| Check | Pass | Source |
|---|---|---|
| `ffprobe`: `codec_name=h264 profile=High level=41` (PH1; level 31 for PH2), `pix_fmt=yuv420p`, `color_range=tv`, `color_space=bt709`, `color_transfer=bt709`, `color_primaries=bt709`, `r_frame_rate=24/1`; frame count equals the timeline | equal | theatrical-delivery Step 8 |
| Atom order | `ftyp, moov, ..., mdat` | M |
| Master tag, before any burn-in | `ffprobe` shows `color_space=bt709` on the ProRes master | Q-F2, M |
| Colour patch (twelve patches) | within ±3/255 | W-16, M |
| Final MP4 true peak and loudness | at or below -1.0 dBTP; -16 LUFS | W-19, M |
| Grain survival, flat patch (PH1 only) | at least 70% of the master | cinematic-quality T1 PR3 (not the Pushtimarg rule PR3), M |
| Type floors and strokes | the Q3 table (T-M2) | M-H1 |
| Safe-area overlay on three frames | all pass | T-M3 |
| Metadata | no title, comment or location; hash in the manifest | Step 8 |
| File name | neutral code before the reveal | W-17 (as cited in the note) |

**Measured sizes (M; from 12-second clips; the 9- and 12-minute columns are projections of the same bitrates).**

| Clip | PH1 Mb/s | PH1 at 9 min / 12 min | PH2 Mb/s | PH2 at 9 min / 12 min |
|---|---|---|---|---|
| C2, drawn flat colour, grain 3 | 2.02 | 149 / 199 MB | 0.42 | 39 / 52 MB |
| C1, photo push, grain 3 | 2.71 | 196 / 262 MB | 0.86 | 69 / 92 MB |
| C3, dense lines, grain 7 (cap-bound) | 8.48 (cap) | 553 / 737 MB (ceiling) | 0.70 | 58 / 78 MB |

Plan storage on the ceiling and expect a third of it. The PH2 cap (3.5 Mb/s, W-63, with its 160 kbps AAC) would allow 247 / 329 MB at 9 / 12 minutes, but the content never reaches it.

**CRF sweep (C2; the grain test).**

| Encode | Bytes | Mb/s | Grain survival (PR3 pass is 70%) |
|---|---|---|---|
| PH1 CRF 16 | 12.7 MB | 8.4 (cap) | 89% |
| PH1 CRF 18 | 6.3 MB | 4.2 | 89% |
| **PH1 CRF 20** | **3.0 MB** | **2.0** | **73%** |
| PH1 CRF 22 | 1.35 MB | 0.9 | 43% (fails) |
| PH1 CRF 24 | 0.76 MB | 0.5 | 17% (fails) |
| PH2 CRF 20, 720p | 0.88 MB | 0.6 | 27% |
| PH2 CRF 23, 720p | 0.56 MB | 0.4 | 0% |
| HEVC CRF 18 | 1.19 MB | 0.8 | 27% |
| HEVC `--tune grain` CRF 20 | 3.55 MB | 2.4 | 49% |

PSNR against the master barely moves across these rows (about 45 to 46 dB), so PSNR and SSIM do not rank them. Grain survival and line contrast do.

### T-M2. Text, stroke and contrast minimums (phone column)

- **Must-read type:** x-height at least 3.2% of picture height (hard floor), 3.8% target (41 px at 1080p). These give 0.30° and 0.35° at 40 cm on a 6.1 in landscape-fit screen (C).
- **Captions:** FontSize 28, white, outline 2, at most 32 characters a line, two lines, reading speed unchanged (20 characters a second, 5/6 to 7 s per event) [57].
- **Credits and the cue sheet:** static cards, each at least 4 s, no rolling credits. The full cue sheet goes in the archive and on a printed or PDF page (J).
- **Strokes:** 4 px for meaning-bearing strokes; 3 px for decoration; dots 6 px; holes 4 px; hatch 3 px on 9 px pitch. No 1 px lines, no hairlines (M-H1 and today's reproduction).
- **Contrast:** at least 4.5:1 for text, 3:1 for large text [53]; aim for 7:1 on a bright phone (C). On the film's palette (computed, sRGB): ink on cream 15.2:1; cream on indigo 11.3:1; ink on yellow 9.8:1; cream on red 5.3:1; cream on green 4.2:1 (fails 4.5, passes large text); red on yellow 3.4:1 (large text only); ink on red 2.9:1 (fails even 3:1); green on red 1.2:1 (fails). Choose cream or ink by luminance, not by hue.
- **Caption colour:** white or neutral light grey by default. A tinted caption colour is allowed only on a build that passes the twelve-patch caption test with a tagged master (Exercise 3 step 5; ffmpeg n9.0.2 passed in the container, the PC build is UNVERIFIED), and an `.ass` carries `YCbCr Matrix: TV.709`. Tinted type the test does not clear is a graphic (PNG or SVG), not a subtitle, with its own colour-patch row (see Pitfalls).

### T-M3. Phone-safe frame and shot-brief fields

File: `research/mobile-delivery-fixtures/safe_area_template.svg` (1920x1080 overlay). Fill-crop card: `phone_test_p1_fillcrop.svg`.

- **Venue file (W-18, one number changed):** FontSize 23, `MarginV` 20 or more (bottom margin 6.9%, inside the 5% box), text inside the 90% by 90% box.
- **Phone file:** captions at FontSize 28, `MarginV` 40, two lines, block at 68% to 86% of height. All must-read type and essential action inside the central 80% of height (10% to 90%), with a cushion: text box 5% to 95% across, 12% to 88% down. The cushion covers rounded corners of about 5 mm (about 70 px at 1920 wide) and on-screen controls that appear on tap (assumption, UNVERIFIED).
- **Every file:** hands (W-33) and the object inside the central 80%. In a captioned shot, also outside the caption zone (venue 78% to 93%; phone 68% to 86%).
- **Shot-brief fields for G0 and G2:** `phone_safe: {action_inside_central80, text_inside_phone_box, caption_zone_clear}` (booleans; a validator can compute the first two from the boxes), `hands_box`, `object_box` (pixels at 1080p), and `caption_zone: none | venue | phone`. G2 composites the overlay on three frames per shot. The full G0 list, with the Hindu-world fields (`motif_check`, `deity_form`, `deity_source`, `respect_check`, `phone_stroke_ok`, `place_id`, `political_room`, `kitchen_hour`, `hands_making`, `seat_check`), is W-42 and sits in the shot brief of `playbooks/agent-pipeline.md`.

### T-M4. Sharing routes (condensed from the note's table; read 2026-10-19; "before the reveal" is no for every route)

| Route | Size limit | Recompression and effect | Cloud copy under W-25? | After: to her | After: relatives, before the ledger | After the ledger |
|---|---|---|---|---|---|---|
| WhatsApp as media | 100 MB and 720p on a fast connection, 64 MB and 480p on a slow one [1]; [3] itself says 64 MB on all platforms and, two lines later, the same 100 MB and 720p default (all re-read 2026-10-19). **Plan on 64 MB.** | Always re-encoded. Line art holds only at 4 px and above (M). Darks UNVERIFIED. | Backup: yes, if "Include videos in chats" is on, copied to Google Drive, WhatsApp cloud or iCloud [7] | No | No | PH2 only, and under 64 MB only for the flat drawn content (39 MB at 9 min, 52 MB at 12 min). PH1 never. |
| WhatsApp as document | 2 GB [1][3][5]; end-to-end encrypted [5] | WhatsApp points to Document for "longer or larger media" [3]. That the bytes are unchanged is implied, not stated: **UNVERIFIED** (Exercise 8). | As above | No | No, including to the maker's own second number (D-02, D-15) | PH1 or PH2, once, when the maker says yes. Forwarding to five chats at a time cannot be prevented, and a re-forward of a forwarded copy reaches one additional group chat [4]. |
| Telegram | 2 GB each, 4 GB with Premium [8][9] | "Send without compression": UNVERIFIED (third-party only) | Yes; chats stored on Telegram's servers [8] | No | No | Only if the maker says yes to a persistent cloud copy |
| Signal | UNVERIFIED (support page returned 403) | UNVERIFIED | UNVERIFIED | No | No | UNVERIFIED; not a likely family route |
| AirDrop | None stated | Peer to peer; original file UNVERIFIED | No | Yes, from a device that already holds the file | No | Recipient must be on "Contacts Only" or "Everyone for 10 Minutes"; from iOS 26.2 a non-contact needs an AirDrop code [13] |
| Quick Share (Android to Android; to iPhone) | None stated | Peer to peer, no server. The Android-to-Android case is UNVERIFIED; it works with AirDrop only when the iPhone is on "Everyone for 10 minutes". Launched on the Pixel 10 family 2025-11-20 [14]. | No | Yes, from a device that already holds the file | No | Yes |
| Google Photos shared album or link | 15 GB free per account [11] | Storage saver resizes video above 1080p to 1080p; Original quality is unchanged [11] | Yes | No | No | No, unless the maker says yes |
| iCloud Shared Albums | Albums created in iOS 26 or earlier: videos up to 15 minutes, at up to 720p. Albums created in iOS 27 or later: original and full resolution, counted against storage, 100 subscribers (page published 2026-09-14) [10] | 720p on older albums | Yes; the charter's named "family cloud library" tip-off risk | No | No | No, unless the maker says yes |
| Google Drive or OneDrive link | Drive: 5 TB a file [15] | None by the host; Drive preview processing UNVERIFIED | Yes; "Anyone with the link" works without sign-in, and viewers can download unless the owner turns that off [16] | No | No | Only after W-48, with an explicit yes; it adds link forwarding |
| Email | Gmail: 25 MB; larger is replaced by a Drive link [17] | n/a | Yes | No | No | No |
| Cable (Android File Transfer mode; iPhone from the PC) | Storage only | None | No, unless her gallery backup is on | **Yes, the primary route** | n/a | n/a |
| USB-C drive into her phone | exFAT or FAT32; a PH1 of at most 737 MB is far under FAT32's 4 GiB | None | No | Yes | n/a | n/a |

### T-M5. Keepsake options (scores 1 to 5; five is best; effort 5 is least effort; risk 5 is lowest risk)

| Option | Works offline | Works on her phone | No cloud | One tap | Large text | Revisitable | Effort | Risk | Total /40 |
|---|---|---|---|---|---|---|---|---|---|
| (a) **MP4 by cable into the gallery** | 5 | 5 | 4 | 5 | 3 | 4 | 4 | 4 | **34** |
| (b) MP4 with chapter atoms | 5 | 5 | 4 | 5 | 3 | 4 | 3 | 4 | 33 |
| (c) Self-contained HTML | 3 | 1 | 5 | 2 | 4 | 2 | 2 | 1 | 20 |
| (d) PWA | 2 | 3 | 1 | 4 | 4 | 3 | 2 | 2 | 21 |
| (e) Private page behind Cloudflare Access (after W-48 only) | 1 | 4 | 1 | 2 | 4 | 5 | 3 | 2 | 22 |
| (f) Dedicated preloaded device (tablet or spare phone), airplane mode, one icon | 5 | 3 | 5 | 5 | 5 | 4 | 2 | 3 | 32 |
| (g) USB-C drive into her phone | 5 | 3 | 5 | 2 | 3 | 3 | 3 | 3 | 27 |

Why, in short. **(a)** plays everywhere, and "no cloud" is 4 rather than 5 because a backed-up gallery uploads the file the moment it lands. **(b)** ffmpeg writes both Nero and QuickTime chapter markers; a stream copy gave a warning "Referenced QT chapter track not found" (M), and the iOS Music and TV apps do not appear to show chapters [46]. Keep chapter atoms out of PH1; use them in the archive and the VLC copy only. **(c)** fails on the iPhone and is unreliable on Android: demoted. **(d)** is installable only over HTTPS or localhost [45]; Safari deletes script-writable storage after seven days without use unless the app is on the home screen [44]: demoted. **(e)** is a later relatives' route, after W-48; the Free plan's 50-seat limit comes from `playbooks/format.md` and is not re-confirmed (TODO(research)). **(f)** is the strongest accessibility option: Android app pinning, or iPhone Guided Access for a relative [48][49]. It is a device, not her phone, so it does not meet D-27 alone. Cost UNVERIFIED (O-04). **(g)** works on iPhone 15 and later with an exFAT, FAT32, FAT, APFS or HFS+ drive [36]; Android needs OTG support, which varies (GSMArena lists the Redmi 9A with microUSB 2.0 and OTG [27]; her phone's port is unknown, O-43).

### T-M6. The project-phone protocol (thirteen rows; about 45 minutes per device once practised)

Devices: (1) an old mid-range Android with a 720p screen (Redmi 9A class); (2) an Android with a 1080p screen (Redmi Note 10 class); (3) a current Android; (4) an iPhone of the last five years, for relatives only; (5) optionally a 6.7 in phone. Her phone is tested only after the reveal, with her yes.

| # | Check | How | Pass | On fail |
|---|---|---|---|---|
| 1 | **Hygiene** (first; 10 min) | No Apple, Google, Samsung or Microsoft account; Google Photos and iCloud Photos off or absent; WhatsApp absent (or fixture content only); airplane mode; location off; brightness 50% with auto-brightness off; room 300 to 500 lux (a free lux app; accuracy UNVERIFIED); screen mode Natural or Standard, recorded | Every box ticked in writing | Stop. No media goes on the phone. |
| 2 | Copy by cable (5 min) | Android: File Transfer [37]. iPhone: VLC file sharing [33] (UNVERIFIED on the PC) | File present; hash equal | Fix the cable or the app |
| 3 | One-tap play | Tap the thumbnail; sound on. On the Redmi 9A class also play the cap-bound dense-lines clip (8 Mb/s) end to end: the chip is stated to play H.264 at 1080p 30 fps, with no profile or bitrate given, and Android lists only Baseline and Main as required [18][66] | Plays at once; seek works (faststart); no stutter on the cap-bound clip | Re-encode with `+faststart`; check atom order; if only the cap-bound clip stutters, lower the cap and record the handset |
| 4 | Fill-crop card, per player (gallery, Google Photos, Apple Photos, VLC; Telegram or WhatsApp if installed with fixtures) | Landscape; fit, then fill by tap or pinch; read the first visible percentage top and bottom | Recorded; crop 9% to 10% expected | Record in the template. If more than 12%, move the text higher. |
| 5 | Caption burn-in (venue and phone versions of the 20-second card) | Read both at 35 cm, then at **50 cm as a proxy for a 50+ viewer**, fit and fill | Phone caption fully readable at 50 cm in fit and fill; venue caption cut in fill (expected) | Raise `MarginV`, or enlarge FontSize |
| 6 | Dark steps (on a clean file and a Trim P file) | First patch you can tell from code 16, at 100 lux and at 500 lux | Both codes recorded; with Trim P, the detail that must be seen sits at or above the 500 lux code, and the 100 lux room does not look milky | Adjust Trim P |
| 7 | Strokes and colour (page 3 chart) | 3 px lines visible; 4 px crisp; hatch 3 px at 9 px pitch visible; equal-brightness pair noted | Pass | Enlarge the strokes in the art |
| 8 | Gallery thumbnail and sort position | Look at the file in the gallery list | Not a dead black frame; sorted where expected | Set a poster frame or first light; set `creation_time` |
| 9 | Chat round trip, fixture only (optional; two project devices) | WhatsApp document: SHA-256 before and after. Media: `ffprobe` the received file (resolution, bitrate, frame rate). | Document hash identical; media numbers written into T-M4 | If the document changes, it is not a lossless route |
| 10 | Sound | Tone ladder 100 Hz to 3.2 kHz at 50% volume in a quiet room; then pink noise; then earbuds; then each cue of the cue map and both hum takes (W-19, W-65) | Speech band (400 Hz to 3 kHz) clearly audible; lowest audible tone written down; a cue that fails (room tone, a deep sea swell, a closed-mouth hum, pakhawaj bass) is marked for its open-vowel or bell replacement | Move the cold-open sound up in frequency; raise the first cue; use the open-vowel hum on the phone files |
| 11 | **Gujarati caption shaping on the PC** (P-LOCK; the same gate as Exercise 7) | Burn the sibling's shaping fixture (ids in Exercise 7) with the chosen OFL font (Noto Sans Gujarati is the caption face, W-21; Hind Vadodara fails the digits string and is a negative control only) through the `subtitles` filter; read the libass log lines the sibling's README names | Conjuncts formed; reph and matra placement correct; no visible virama (compare the two-row picture: top row the failing 6.1.1 build, bottom row the correct n9.0.2 build) | Change the build first (older than n9.0 shows the top row), then the font or renderer. `drawtext` is out on any ffmpeg older than n9.0. |
| 12 | **Slice fixture played from the project phone's gallery** (P-LOCK) | Copy the slice fixture; play it | Plays with sound at one tap | As rows 2 and 3 |
| 13 | **Scrubber page from the file manager and from Files** (measures the demotion of W-30's page; two minutes) | Open the scrubber page (the slice fixture's page, or a stand-in page with a relative-path video) from the project Android's file manager and from Files on the iPhone; record whether the video plays | Recorded for both platforms. If it plays on both, the laptop companion gains a phone fallback for free; if not, the demotion stands, now measured | None: keep the demotion; note the Android version, the browser and the iOS version |

Evidence: a photograph of the screen for each row (fixture content only). Each fail names its fix.

### K1 to K5. Decision tables keyed on the unknowns

**K1. Her phone and her backup, to the reveal-weekend route (her yes first).** Her phone is Android (D-31); the iPhone rows are for relatives after the ledger.

| Phone | Cloud photo backup | Route | Do not |
|---|---|---|---|
| Android (hers) | Google Photos backup on, or the phone manufacturer's gallery sync on (Samsung Gallery to OneDrive; others UNVERIFIED) | **First question, at the reveal-weekend check and again in the her-turn conversation (Sun 7 Mar after about 14:00, else Mon 8 Mar; W-48): is "Back up all device folders" on?** Google's page says backup covers "your chosen device folders ... not only your camera", with a "Back up device folders" screen and a "Back up all device folders" switch; with the switch on, "photos in new device folders automatically back up" [12]. **The app-folder route is safe only if that switch is off.** Off: USB File Transfer into a folder her backup is not set to read, or into an app's own folder such as VLC's (whether another app's private `Android/data` folder counts as a device folder is UNVERIFIED). On or unknown: the Android tablet or the stick, or, with her yes, switch that folder off in "Back up device folders" before the copy. Which folders each skin (MIUI, One UI, ColorOS, Funtouch) turns on by default is not documented; Google's page lists none. | Drop it into DCIM/Camera, the folder backup reads by default (UNVERIFIED default) |
| Android (hers) | Off | USB File Transfer into Movies; tap it in the gallery | |
| Android (hers) | Unknown at reveal | Treat as on, and treat "Back up all device folders" as on. Do not look at her phone beforehand (D-02). Answer O-43 and the backup question first; at the reveal check, with her yes, look at the switch together before any cable copy. | Guess |
| iPhone (a relative) | iCloud Photos on | Apple Devices, Files, drag onto VLC (needs the App Store) [33]. Photo sync is unavailable while iCloud Photos is on [34]. | Save Video to Photos |
| iPhone (a relative) | iCloud Photos off | Apple Devices, Photos, Sync from folder, Include videos [34]; or the VLC route | |
| Android with OTG, or iPhone 15 or later | Any | The USB stick as a second copy | Rely on it as the only route |

**K2. Her language and script (Gujarati, D-31), to the caption and type sizes.** Latin: FontSize 28, 32 characters a line. Gujarati has no headline and no true x-height, so the height of the base letter KA is the analogue (the sibling track's working analogue; inference, J). At FontSize 23 the sibling measured KA at 3.52% of picture height in Hind Vadodara, 3.33% in Noto Sans Gujarati and 2.96% in Mukta Vaani (one sample sentence each). For the 3.8% target, FontSize is 24.8, 26.2 and 29.5 respectively; for the 3.2% hard floor, 20.9, 22.1 and 24.9 (C); the Hind Vadodara and Mukta Vaani figures are kept as measurements only, because neither is used (W-21). **Noto Sans Gujarati (26.2 for the target, 22.1 for the floor) is the caption face** (W-18, W-21). The sibling's Q9 Gujarati paragraph (`research/devotional-sound-script.md`) found that Hind Vadodara has no Gujarati digits (U+0AE6 to U+0AEF), so any date or year (સંવત ૨૦૮૩) falls back to FreeSerif, while Noto Sans Gujarati carries digits, the Om sign and every conjunct string it shaped; Mukta Vaani leaves conjuncts unfused when the text is tagged Gujarati (W-21). Cards and verse are shaped outlines, not captions: Rasa or Baloo Bhai 2 for cards, Noto Serif Gujarati for verse (about 25.6), Noto Serif or Tiro Sanskrit for Devanagari verse, and Shrikhand and Farsan only as outlined title art, never live text (W-21). Her script belongs on title and verse cards as shaped outlines, with the room-language captions underneath (sibling Template L3), so the phone burn-in is mostly the room's language. Shaping test first (Exercise 7). Other scripts: size by base-letter height, not by FontSize.

**K3. How she holds the phone (V7 in `research/hindu-visual.md`), to the design rule.** Sideways: landscape-fit design and the size floors above. Upright in a chat: the picture is 36.5 mm tall on a 6.1 in screen, and nothing is legible at 0.35°. The hand-over must say "turn it sideways". A three-second rotate card is a creative call, not recommended.

**K4. Relatives' phones, to the file.** Under 3 GB free storage or slow data: PH2 (39 to 92 MB). Otherwise PH1 as a document (199 to 262 MB typical at 12 minutes). Never send as media. Never HEVC.

**K5. Where the premiere is (O-02, O-44), to the sharing rule.** Unchanged: no live link on the night; WhatsApp document only after the ledger. The venue may have a filming policy, which goes in the room brief (W-52, access times only).

### Phone-surface checklist (any image on a phone, not only the film)

- Lock screen, gallery thumbnail, app icon, poster frame, forwarded frame, page frame and QR code are all checked against What we leave out.
- No deity image on any phone surface until the maker decides in writing, surface by surface (O-64, which absorbs O-42; W-73). Default: her script end-card line, a lamp, or the object.
- The thumbnail is not a dead black frame (check 8): it is the first frame of her object or her hands (W-32, W-33), never a title card and never a deity (O-64).
- Any decorative frame is out by default (jaali, paisley, mehndi borders, arches, tile patterns).
- Text on a phone surface is at least 4.5:1 contrast and at least 44 by 44 CSS pixels for any control [52][53].

### T-M8. Rights-log additions

- T8 gains a `phone_share` column: `none`, `her_device_only`, `relatives_after_ledger`, `public`. It also gains the types `artwork`, `deity_image`, `commissioned_art` and `font` and a `tradition_origin` note (W-46).
- Releases 4d to 4g gain this line: "[ ] a copy of the film on my relatives' phones, sent by WhatsApp or similar; I understand a forwarded copy cannot be recalled." Release 4e adds: "a copy on my phone and in my phone's backup account."
- Decision line TD-9 (now decided in the register as W-74): "Phone deliverable: PH1 by cable to her phone on reveal weekend with her yes; PH2 to relatives as a WhatsApp document only after the ledger closes (W-48) and the maker says yes."
- Each font, cue and person used in a phone copy has a row (W-21, W-46).

### Size and storage check

Use the sizes table in T-M1. Plan storage on the ceiling (737 MB for PH1 at 12 minutes) and expect about a third of it.

**Reveal-weekend arithmetic, keyed on O-43 (free storage on her phone).** PH1 at the 737 MB ceiling plus a 200 MB margin (J: her own photos, the gallery's cache, an update that fires at the wrong moment) means **at least 1 GB free on her phone**. If O-43 reports less, PH2 goes on by cable (typically 52 to 92 MB at 12 minutes, 374 MB at its cap) and PH1 waits for the tablet or the stick. If O-43 is unanswered, read Settings, Storage together with her at the reveal check, with her yes (never beforehand, D-02), and treat "unknown" as under 1 GB.

---

## What we leave out (the Hindu-only rule in practice)

**The rule (D-28).** "Indian themes" always means Hindu themes: Sanatan Dharma and its sanskriti. Hindu gods, epics, Hindu history, temple architecture and Hindu art traditions are welcome. **No Mughal or other Islamic motifs. No Christian motifs. Ever.** When a motif's origin is shared or ambiguous, flag it, and leave it out by default. Deities are depicted with correct iconography and respect. Nothing in this phone track introduces a Mughal, Islamic or Christian motif. The only shared or ambiguous items it meets are decorative devices, and they are defaulted out.

| Item | Why it is flagged | Default |
|---|---|---|
| A deity image as lock-screen still, thumbnail or app icon | A phone is touched, carried and laid face-down, and its lock screen sits under the clock and notifications (J; not a sourced norm). The film's deity policy is class P1 for all eight deities: symbols and seva objects that are not a svarupa, and no deity drawn, generated or photographed (W-61). Whether she would welcome more is O-64 (which absorbs O-42). | Out. Her script end-card line, a lamp or the object instead. |
| Her own deities (the eight named in D-31) on a phone surface | They are hers, which is the test the charter sets. But a deity image on a device raises placement and handling questions. The Pushtimarg track's answer is that a picture may be pusht (in seva) and the film cannot tell by looking, so nothing in seva is photographed without her knowing (PR4, W-61); how her tradition treats an image on a phone is otherwise UNVERIFIED. O-64 (which absorbs O-42) is the open question. | Symbols and her script until the maker, as her proxy, answers O-64 in writing for each surface (W-73). |
| Forwardable deity frames | Once a relative forwards the film, a frame can be saved among unrelated photos (community norm; UNVERIFIED). | Follow O-64 (which absorbs O-42). No deity image in the gallery thumbnail or poster frame. |
| Decorative frames on any phone page (thank-you page, PWA, HTML): paisley, jaali screens, cusped or multifoil arches, mehndi borders, geometric tile patterns | Shared or Indo-Islamic origin on the `hindu-visual` exclusion list, and no ornament without a reason (Principle 2). | None. A plain, quiet page. |
| Bells, candles, haloes, crosses and winged figures as UI marks (the Christian or colonial forms only) | Christian or colonial layer in these forms. | Church-shaped bells, candles where a diya belongs, a flat gold-disc halo drawn as in a church icon, crosses, winged figures: Christian or colonial layer, none. The ghanta (temple bell), the diya and the prabhavali or prabhamandala are Hindu and are not excluded by this row. |
| A decorative QR frame (rangoli or mandala border) | Decoration for its own sake. | A plain QR code, and only a static one. |
| The swastika in a thumbnail or lock-screen still | Sacred in ritual form, but misread in a public room outside India (`hindu-visual` 1.4). | Out by default (SW0, W-72); a sathiyo on a phone surface is the maker's call alone, with the room's reading (O-44, O-66). |
| Dharmic-but-not-Hindu or Adivasi text in a thank-you line | Not covered by D-28. | None. Ask the maker. |
| Ringtones, notification sounds, sound chips | None are needed. No Om tone as a UI sound. | The tone ladder uses plain sine tones. |

---

## Decisions you'll need to make (options and our lean)

| # | Decision | Options | Our lean | By when, who |
|---|---|---|---|---|
| 1 | Her keepsake route | (a) MP4 by cable; (f) tablet in app pinning; (g) USB-C drive; (b) chapter atoms; (c) HTML; (d) PWA; (e) private page | (a) by cable. (f) if the budget allows (O-04). Keep the stick (g) as the archive and as rung 3 of the failure ladder. Chapter atoms only in the archive and the VLC copy. | Maker, at G-SLICE (O-30); the cable step on reveal weekend with her yes |
| 2 | The offline scrubber page (W-30) | Keep it for her phone; demote it to a laptop and archive companion | Demote it for her phone. Keep it for a laptop or TV. | Maker, at G-SLICE, Sun 20 Dec (O-30) |
| 3 | Deity image on any phone surface (O-64, absorbs O-42) | None; symbols; her own deities, decided surface by surface in writing | None for now. Her end-card line, a lamp or the object instead. The tradition's own norm carries over: no sampradaya page read covers a phone, but a picture can be a living svarupa in seva, so no deity image unless she knows and says yes (`research/pushtimarg-world.md` PR2 and PR4; research note Q-F6). | Maker, as her proxy, before any phone surface is set |
| 4 | The lock-screen still | Her end-card line (the greeting or blessing she actually says; her handwriting only for words she wrote, W-35); a lamp; the object | Her end-card line (W-69, W-73): in Gujarati, in her hand only if a sample exists, shaped through the real pipeline and read by the native reader (O-62), checked against a printed source (R19 as cited in the note). **The end-card wording is not yet known: TODO(maker); it follows O-49.** | Maker, by G-SLICE |
| 5 | Caption language on the phone file (O-15; Q11 of the note) | Room-language captions; Gujarati captions too; her script on cards only | Room-language captions burned in, so no switch is needed; her script on title and verse cards as shaped outlines | Maker, Sun 1 Nov (O-15) |
| 6 | Trim P (mild shadow lift) | Off; a mild lift; a stronger lift | Mild: start at 4 to 7 IRE at codes 24 to 40, black pinned at 16, tuned in Exercise 5 (J) | Maker, at G-SLICE |
| 7 | Cold open on a phone | A visible first light within about 4 s; a first sound above 400 Hz; both | Both, if the cold open can take them; otherwise a first sound above 400 Hz, ranked on the project Android in Exercise 6 before beat sheet v1, Sun 6 Dec (W-36, W-76). Candidates, in the register's order: water poured into brass if the home keeps Yamunajal in a jhari (O-77; a stand-in kitchen vessel, never her jhari); a household hand-bell outside the mandir, or the maker's own, struck once, if the morning bell is hers (O-46, W-70); the conch (thin; the maker's own or none); a spoon on a steel vati or the cooker whistle (the fully domestic version, no gate). Room tone alone fails as a first sound on a phone. No bell and no conch are needed for the Mangla reading to land. The sampradaya's Mangla text has the bells rung three times and the conch blown (a lit lamp is documented at Shayan, not at Mangla, research note Q-F6); the maker confirms what is her household's practice before any cue is mapped, and if her morning starts another way, use that. | Maker, with the music-sound and cinematic-quality tracks |
| 8 | Vertical or square cut | None; one 9:16 still; a full vertical cut | None. One 9:16 still for her lock screen (about one hour). A full vertical cut costs about 25 to 40 hours (C, J), 9% to 14% of the 284-hour Base model, and D-24 says finish beats sprawl. | Maker, after the slice speaks (D-24) |
| 9 | Her backup and the copy | App-folder route (VLC); a folder her backup does not read; the tablet or the stick; ask again at the her-turn conversation (Sun 7 Mar after about 14:00, W-48) | First question: is "Back up all device folders" on? The app-folder route only if it is off; on or unknown means the tablet or the stick (K1) | Maker, reveal weekend (the note's question 9) |
| 10 | Guests' phones at the premiere | No QR code; a static thank-you page with no media; a spoken promise of a family copy after a named date | No QR and no live link. A spoken promise after a named date (the default). A static page with no media at most. The date is TODO(maker). | Maker, Sun 15 Nov (the note's question 8) |
| 11 | HEVC variant | None; re-test if the finished film has little grain | None, because the HEVC "saving" is the grain (M) | Maker, at picture lock (G-LOCK) |
| 12 | WhatsApp accounts on the two project phones for Exercise 8 | No test (the document route stays UNVERIFIED); or a test with two separate numbers, fixture content only, accounts removed afterwards | Lean: run the test with fixtures only, on two separate numbers, and remove the accounts afterwards. **This amends the no-accounts rule for those two devices, so it is the maker's call.** | Maker, before Exercise 8 |
| 13 | Relatives' copies | PH2 by document; PH1 by document where storage allows; none | PH2 for low-storage phones and PH1 where storage allows, after the ledger, one copy each, with the release line | Maker, after W-48 and releases 4d to 4g |
| 14 | File name and thumbnail | Her name; her language; a neutral code | A neutral code until the reveal. After the reveal, the title in her language. The thumbnail is the first frame of her object or her hands in the opening (W-32, W-33), never a title card and never a deity (O-64), and the same frame marks the folder on the venue sticks. | Maker, before the reveal (file name check, W-17 as cited) |

---

## Pitfalls

- **The ffmpeg default `MarginV` puts caption descenders at 3.5% from the bottom**, outside the 5% graphics-safe box (M). Use `MarginV` 20 or more on the venue file and 40 on the phone file. With the default, a two-line caption is cut in a 20:9 fill crop.
- **Tinted caption text shifts colour through the burn-in on ffmpeg 6.1.1, and again on n8.0 and later for an `.ass` with no `YCbCr Matrix` header.** On 6.1.1 pure red came out 255, 23, 0; ochre F0B323 246, 175, 27; film red B5282B 193, 52, 41; film green 2E7D32 40, 111, 47 (worst 23/255); white, greys, indigo, skin and cream stayed within 3 (M, re-run 2026-10-19 on twelve colours; the first pass's "cream blue +9" did not reproduce). From n7.0 the `subtitles` filter draws in the link's colourspace and every colour is within 3/255 on a BT.709-tagged master (ffmpeg n9.0.2 built from source: worst 3); from n8.0 an `.ass` file's header decides: `None` or `TV.709` is correct, a missing header or `TV.601` is BT.601 (23/255). An untagged master fails on every build. **Captions are white or neutral by default; tinted only after the twelve-patch caption test passes on the PC build** (Exercise 3 step 5, T-M2).
- **A bare RGB-to-YUV step gives a 23/255 error** on pure red (M). Start from the YUV ProRes master. Any RGB step must name `scale=out_color_matrix=bt709`.
- **HEVC looks like a saving only because it deletes the grain.** HEVC at CRF 18 kept 1 to 27% of the grain; `--tune grain` at CRF 20 kept 49% at 3.55 MB against PH1's 3.0 MB (M). Android guarantees HEVC only at Main Level 3 for mobile [18]; browsers are "partial" [24]; her iPhone plays H.264 as well [19].
- **The damage is the chat recompression, not the PH1 encode.** Master to PH1 to a WhatsApp-class 720p proxy equals master straight to the proxy, within 0.01 (M). A 3 px line keeps 0.61 through a 360p, 0.5 Mb/s proxy and a 4 px line keeps 0.84 (M).
- **Chapter atoms are not honoured on phones.** A stream copy wrote a QuickTime chapter reference that ffprobe could not match (M). Keep them out of PH1.
- **A gallery that sorts by creation time may place a stripped file oddly.** Which gallery does what is UNVERIFIED; check 8 records it.
- **ffmpeg's `subtitles` filter before n9.0 shapes Indic text in simple mode and fails silently.** FreeSerif (Gujarati) and FreeSans (Devanagari) through 6.1.1 produced no error and wrong text (M): conjuncts not formed, viramas visible, the reph standing alone. The same files through n9.0.2 are correct, so the cause is the build, not the font (the first pass blamed "a font without Indic shaping tables"; corrected in round 1, research note Q-F2b). Check the PC build and the chosen font by eye (Exercise 7).
- **Fill is a viewer's choice in YouTube**, which added crop-zoom in November 2017 [31]. Apple's `resizeAspectFill` fills and crops [32]. Documented defaults exist only for the components: the AndroidX Media3 `PlayerView` defaults to fit [67] and Apple's `AVPlayerLayer` to `resizeAspect`, also fit [68]. The defaults of the Android gallery, Google Photos, Apple Photos, WhatsApp and Telegram themselves are not documented in anything read (UNVERIFIED); row 4 measures them. Expect a 9% to 10% crop.
- **Upright in a chat, the captions are degraded** (0.23° at 35 cm). The film is designed for sideways.
- **Equal-brightness colours vanish together.** Red on green is 1.2:1; ink on red is 2.9:1 and fails the 3:1 large-text rule.
- **Google Photos backup covers "your chosen device folders ... not only your camera",** and with "Back up all device folders" on, "photos in new device folders automatically back up" [12]. The page advises deleting already backed-up items on photos.google.com; that turning backup off leaves them in place is an inference. iCloud Photos on an iPhone blocks the Apple Devices photo sync [34].
- **WhatsApp chat backup with "Include videos in chats"** copies videos to Google Drive, WhatsApp cloud storage or iCloud [7].
- **Vendor clouds appear and vanish.** Xiaomi ended Gallery cloud sync on 2022-10-25, with data deleted on 2023-08-01 [50]. Other makers' clouds (Oppo, Vivo, Realme, OnePlus) are UNVERIFIED: check the settings on each phone.
- **Self-contained HTML is not a keepsake.** A standalone HTML export showed a blank page in the iOS Files preview (OpenMAIC issue 1847, opened 2026-10-08, still open [40]). Android `content://` pages fail on relative links [41][42][43]. Both rest on forum evidence, read and not run, until T-M6 row 13 measures them on the project phones.
- **Apple Shared Albums limits depend on the creator's OS.** Albums made in iOS 26 or earlier deliver 720p and up to 15 minutes (page published 2026-09-14) [10]. Never plan around a platform's lowest-quality path.
- **Two project phones with WhatsApp is an account** (Decision 12).
- **A forwarded copy cannot be recalled.** The release line says so, and the rights log has a `phone_share` column.

### Gaps the research did not close (TODO(research))

- Signal's limits (support page returned 403) and Telegram's "send without compression" (the FAQ is silent): UNVERIFIED.
- The default fit or fill of the Android gallery, Google Photos, Apple Photos, WhatsApp and Telegram players: not documented in anything read; only the Media3 and AVFoundation component defaults are (fit) [67][68]. The fill-crop card measures the apps.
- How filmmakers deliver vertical versions: unsourced (Adobe's Auto Reframe page returned 403). The vertical cost (2 to 3.3 maker-hours per finished minute) is a judgement on production-scale figures.
- Real WhatsApp, Telegram and Signal output (resolution, bitrate, darks, whether a document is byte-identical) was not measured; the recording tables are ready and the test waits for Decision 12 and the project phones (research note Q-F1). Only the M-H1 WhatsApp-class proxies were used.
- Every Windows-side step is UNVERIFIED until `windows_check_report.json` for the maker's PC is in the repo (W-28). The colour-patch test and the caption colour and shaping tests must be re-run on the PC build (W-16, Exercise 3 step 5, Exercise 7); the container's n9.0.2 passes, but the PC's bundled libass is unknown.
- Whether the Redmi 9A class decodes H.264 High 4.1 at the 8 Mb/s cap: MediaTek states H.264 playback at 1080p 30 fps with no profile or bitrate [66]; UNVERIFIED on a handset (row 3). Its real scaler is unknown; six scalers bracket it and a 3 px line keeps at least 0.83 under all of them (research note Q-F4).
- Phone geometry and the veil and dark-step table are computed from published specs and assumed reflectance, white level and viewing distance. The 50% brightness-to-nits curve is UNVERIFIED.
- Her Android's make, model, version, screen, storage, USB port and backup state are unknown (O-54, which absorbs O-43; the intake table is research note Q-F7). Which folders each skin's Google Photos backs up by default is not documented (Google's page lists none), so K1 asks first.
- Legge and Bigelow (2011, the x-height basis) returned 503 and the BBC subtitle guidelines were unreachable; neither was re-opened.
- Samsung's OneDrive page is digest only (it timed out in a headless browser too), Apple external storage and PubMed are digest only. Apple's `AVLayerVideoGravity` is now read from Apple's own data file [68].
- Cloudflare Access's 50-seat limit was not re-confirmed.
- Whether her household keeps Thakorji's morning seva (the bell, a lamp) is O-46 (the Pushtimarg sprint's open Q3); the sampradaya's text has the bell at Mangla and a lamp at Shayan (research note Q-F6).

---

## Best references (8)

1. **WhatsApp Help Center, "How to send media, contacts, or location"** [1]. The media limits (100 MB and 720p fast, 64 MB and 480p slow) and the 2 GB document route. Read 2026-10-19 and re-read in a headless browser the same day (excerpt saved). [3] states the 64 MB and the 100 MB figures on its own page; plan on 64.
2. **WhatsApp Help Center, "Can't send longer videos"** (earlier read as "I can't send long videos") [3]. The "64MB on all platforms" line and the document route.
3. **Android Developers, "Supported media formats"** [18]. H.264 decoders, HEVC Main Level 3 for mobile, and `moov` before `mdat` for streaming.
4. **YouTube Help, "Recommended upload encoding settings"** [20]. H.264 High, BT.709, 8 Mb/s at 1080p SDR, AAC-LC, `moov` at the front. PH1's cap follows this.
5. **Apple Support, "Shared Albums limits"** [10]. Dated 2026-09-14. Limits depend on the album creator's iOS version.
6. **Android Help, "Transfer files between your Android device and computer"** [37]. USB File Transfer mode, the route to her phone.
7. **Android Help, "Pin and unpin screens"** [49]. App pinning, the one-app mode for option (f).
8. **W3C, "Understanding SC 1.4.3: Contrast (Minimum)"** [53]. The 4.5:1 and 3:1 floors used in T-M2.

---

## Sources

*Copied from `research/mobile-delivery.md` (Sources, items 1 to 73, plus the local items). Each page was read by the researcher on the date shown; items 63 to 73 were added and opened by the round-1 implementor on 2026-10-19. "Digest only" means read as a search-result summary. Entries marked UNVERIFIED were not confirmed.*

1. WhatsApp Help Center, "How to send media, contacts, or location" (web) — https://faq.whatsapp.com/453914586839706/?cms_platform=web — read 2026-10-19 — video default limit 100 MB and 720p (fast) or 64 MB and 480p (slow); documents 2 GB; Standard or HD quality; formats; Status 90 s. **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium (the fetch tool returns only the title); one reading, not the maker's browser.**
2. WhatsApp Help Center, "About HD photos and videos" (Android) — https://faq.whatsapp.com/759301289012856/?cms_platform=android — read 2026-10-19 — HD per message or default under Media upload quality; no pixel numbers; connection affects quality.
3. WhatsApp Help Center, "I can't send long videos" — https://faq.whatsapp.com/823886715479103/ (reached from /545917406122452/) — read 2026-10-19 — "64MB on all platforms" and the Document route up to 2 GB; the same page repeats [1]'s 100 MB and 720p default for a fast connection; the title today is "Can't send longer videos". **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
4. WhatsApp Help Center, "About forwarding limits" — https://faq.whatsapp.com/1053543185312573 — read 2026-10-19 — up to five chats at a time; "forwarded many times" after five-chat chains; a message forwarded to you "can only be shared with one additional group chat" (new on the re-read). **script-rendered; dated text excerpt saved in `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt`; re-read 2026-10-19 in a headless Chromium.**
5. WhatsApp Blog, "Reactions, 2GB File Sharing, 512 Groups" — https://blog.whatsapp.com/reactions-2gb-file-sharing-512-groups — post 2022-05-05, updated 2022-07-11 — 2 GB files, end-to-end encrypted.
6. WhatsApp Privacy Policy — https://www.whatsapp.com/legal/privacy-policy — "Effective January 4, 2021" as displayed — delivered messages deleted from servers; undelivered kept encrypted up to 30 days; forwarded media stored temporarily.
7. WhatsApp Help Center, "How to back up your chat history" (Android) — https://faq.whatsapp.com/481135090640375/?cms_platform=android — read 2026-10-19 — backup to WhatsApp cloud or Google; "Include videos in chats".
8. Telegram FAQ — https://telegram.org/faq — read 2026-10-19 — files up to 2 GB each; chats stored in the Telegram cloud; silent on compression.
9. Telegram blog, "700 Million Users and Telegram Premium" — https://telegram.org/blog/700-million-and-premium — 2022-06-19 — 2 GB free, 4 GB Premium.
10. Apple Support, "Shared Albums limits" — https://support.apple.com/en-us/148868 — published 2026-09-14 — iOS 26 and earlier: video up to 15 minutes at up to 720p, 5,000 items; iOS 27 and later: original and full resolution, counts against storage.
11. Google Photos Help, "Choose the upload size of your photos and videos" — https://support.google.com/photos/answer/6220791 — read 2026-10-19 — Storage saver resizes video above 1080p to 1080p; 15 GB per account.
12. Google Photos Help, "Turn backup on or off" — https://support.google.com/photos/answer/6193313 — read 2026-10-19 and re-read in a headless Chromium (Android tab, sections expanded; the page's title is now "Back up photos & videos") — Photos settings, Backup; "your chosen device folders are automatically backed up too, not only your camera"; a "Back up all device folders" switch ("photos in new device folders automatically back up"); no default folders listed; removal means turning backup off and deleting the items on photos.google.com (that turning backup off leaves them is an inference).
13. Apple Support, "How to use AirDrop on your iPhone or iPad" — https://support.apple.com/en-us/119857 — read 2026-10-19 — "Everyone for 10 Minutes"; AirDrop code with iOS 26.2 or later.
14. Google, "Android Quick Share support for AirDrop" — https://blog.google/security/android-quick-share-support-for-airdrop-security/ — 2025-11-20 — Pixel 10 first; peer to peer; AirDrop "Everyone for 10 minutes" only.
15. Google Drive Help, "Google Drive file size limits" — https://support.google.com/drive/answer/37603 — read 2026-10-19 — up to 5 TB a file.
16. Google Drive Help, "Share files from Google Drive" — https://support.google.com/drive/answer/2494822 — read 2026-10-19 — "Anyone with the link"; viewers can download unless turned off.
17. Gmail Help, "Attachment size limit" — https://support.google.com/mail/answer/6584 — read 2026-10-19 — 25 MB; larger replaced by a Drive link.
18. Android Developers, "Supported media formats" — https://developer.android.com/media/platform/supported-formats — read 2026-10-19 — H.264 Baseline (3.0+) and Main (6.0+) decoders; HEVC Main Level 3 for mobile; HLG10 and HDR10; `moov` before `mdat`.
19. Apple Support, "iPhone 15 Tech Specs" — https://support.apple.com/en-us/111831 — read 2026-10-19 — 6.1 in, 2556x1179, 460 ppi, 1000/1600/2000 nits; HEVC, H.264, ProRes.
20. YouTube Help, "Recommended upload encoding settings" — https://support.google.com/youtube/answer/1722171 — read 2026-10-19 — H.264 High, BT.709, 8 Mb/s 1080p SDR, AAC-LC, `moov` at front.
21. FFmpeg, "Formats Documentation" — https://www.ffmpeg.org/ffmpeg-formats.html — read 2026-10-19 (first 100,000 characters; the FFMETADATA chapter syntax section was truncated) — faststart; MP4 muxer writes Nero chapters and a QuickTime chapter track by default.
22. Robitza, "CRF Guide (Constant Rate Factor in x264, x265 and libvpx)" — https://slhck.info/video/2017/02/24/crf-guide.html — read 2026-10-19 — sane x264 range 18 to 28, default 23; plus or minus 6 is about half or double.
23. x265 documentation, command line options — https://x265.readthedocs.io/en/master/cli.html — read 2026-10-19 (first 100,000 characters) — CRF default 28; VBV needs both options in CRF mode; `--tune grain` enables `--rc-grain`.
24. caniuse, "HEVC/H.265 video format" — https://caniuse.com/hevc — read 2026-10-19 — "partial" in Chrome from 107 and Firefox from 137; Safari and iOS Safari supported.
25. StatCounter, "Mobile Operating System Market Share India" — https://gs.statcounter.com/os-market-share/mobile/india — September 2026 — Android 93.89%, iOS 6.05%. Web traffic, not an installed base.
26. StatCounter, "Mobile Screen Resolution Stats India" — https://gs.statcounter.com/screen-resolution-stats/mobile/india — September 2026 — top six viewports and shares (together 37%).
27. GSMArena, "Xiaomi Redmi 9A" — https://www.gsmarena.com/xiaomi_redmi_9a-10279.php — read 2026-10-19 (again in a headless Chromium) — 6.53 in IPS LCD, 720x1600, 20:9, 400 nits typical, announced 2020-06-30; chipset MediaTek MT6762G Helio G25; microUSB 2.0 with OTG; microSDXC slot.
28. GSMArena, "Xiaomi Redmi Note 10" — https://www.gsmarena.com/xiaomi_redmi_note_10-10247.php — read 2026-10-19 — 6.43 in Super AMOLED, 1080x2400, 20:9, 450 nits typical and 1100 peak, announced 2021-03-04.
29. GSMArena, "Xiaomi Redmi Note 10 review: lab tests" — https://www.gsmarena.com/xiaomi_redmi_note_10-review-2244p3.php — read 2026-10-19 — measured 475 nits manual and 682 auto; YouTube sees HDR, Netflix SDR only.
30. Bababekova et al., "Font size and viewing distance of handheld smart phones", Optometry and Vision Science 88(7):795-7, 2011 — https://pubmed.ncbi.nlm.nih.gov/21499163/ — abstract via search digest only (page needs cookies) — mean 36.2 cm texting (n = 129), 32.2 cm web (n = 100).
31. GSMArena, "YouTube updated with pinch-to-zoom for screens wider than 16:9" — https://m.gsmarena.com/youtube_updated_with_pinchtozoom_for_screens_wider_than_169-news-28290.php — 2017-11-16 — crop-zoom fills the screen and may crop video; Samsung's support page (https://www.samsung.com/us/support/troubleshoot/TSG10004866, 403) via digest only.
32. Apple Developer, "AVLayerVideoGravity.resizeAspectFill" — https://developer.apple.com/documentation/AVFoundation/AVLayerVideoGravity/resizeAspectFill — digest only (page is script-rendered) — resizeAspect fits; resizeAspectFill fills.
33. Apple Support, "Transfer files between your Windows device and iPhone, iPad, or iPod touch" (Apple Devices app) — https://support.apple.com/guide/devices-windows/transfer-files-between-your-devices-mchl4bd77d3a/windows — read 2026-10-19 — Files in the sidebar; drag onto apps that support file sharing.
34. Apple Support, "Sync photos between your Windows device and iPhone, iPad, or iPod" — https://support.apple.com/guide/devices-windows/sync-photos-to-your-device-mchl4af095d3/windows — read 2026-10-19 — "Include videos"; unavailable while iCloud Photos is on.
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
49. Android Help, "Pin and unpin screens" — https://support.google.com/android/answer/9455138?hl=en — read 2026-10-19 — app pinning; some steps need Android 11 or later on Pixel.
50. Xiaomi, "Notice of termination of Xiaomi Cloud sync for Gallery items" — https://i.mi.com/announcement/stop_service — read 2026-10-19 — ends 2022-10-25; India in the first group; data deleted 2023-08-01.
51. Samsung Support, "OneDrive on your Samsung phone or tablet" — https://www.samsung.com/us/support/answer/ANS10003437/ — digest only (403 on fetch) — Gallery sync with OneDrive needs Samsung and Microsoft accounts; may be off by default.
52. W3C, "Understanding SC 2.5.5: Target Size (Enhanced)" — https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — read 2026-10-19 — 44 by 44 CSS pixels.
53. W3C, "Understanding SC 1.4.3: Contrast (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — read 2026-10-19 — 4.5:1; 3:1 for large text.
54. Lee et al., "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ — read 2026-10-19 — qualitative: swipes and double-taps failed; larger fonts and objects; tablets preferred.
55. Wikipedia, "Lux" — https://en.wikipedia.org/wiki/Lux — read 2026-10-19 — overcast day 1,000; full daylight 10,000 to 25,000; office 320 to 500.
56. Wikipedia, "Fresnel equations" — https://en.wikipedia.org/wiki/Fresnel_equations — read 2026-10-19 (first 100,000 characters) — about 4% reflectance per glass surface at normal incidence.
57. Netflix Partner Help Center, "Timed Text Style Guide: General Requirements" — https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements — read 2026-10-19 — two lines maximum; events 5/6 s to 7 s; no character count on this page.
58. Local: `CHARTER.md` (Known facts, including "Her world", 2026-10-19); `DECISIONS.md` (D-02, D-05, D-15, D-24, D-27, D-28, D-31, W-04, W-15 to W-20, W-25, W-26, W-30, W-33, W-35, W-46 to W-48, O-30, O-43); commit `ac6711e` ("Record her world") — read 2026-10-19. Note: O-42 and O-43 were defined in `reviews/04-hindu-mobile-briefs-review.md`; the register (2026-10-19) absorbs them as O-64 and O-54, and O-44 is its own row.
59. Local: `playbooks/theatrical-delivery.md` (Steps 4 to 8, T1, T2, T8, T9, T11), `playbooks/format.md` (Step 8, Decisions 8 and 11, Step 15), `playbooks/cinematic-quality.md` (T1 PR2 and PR3, T6, Exercise 2, TY1), `playbooks/production-scale.md` (stage hours), `playbooks/surprise-ops.md` (Step 11, Decision 15), `playbooks/toolchain.md` (captions) — read 2026-10-19.
60. Local: `research/hindu-visual.md` F3 (M-H1) and `research/hindu-visual-fixtures/phone_chart.svg`; `research/cinematic-quality.md` FQ1 (caption x-height; cites Legge and Bigelow 2011, J Vision 11(5):8, and the BBC subtitle guidelines via `playbooks/format.md` [105]; neither re-opened today); `research/agent-pipeline.md` Q-F1 (colour-patch method); `reviews/04-hindu-mobile-briefs-review.md` Part 4.
61. Local: this track's fixtures and measurements, 2026-10-19: `research/mobile-delivery-fixtures/` (README, SVG templates, CSVs, Devanagari and Gujarati shaping evidence).
62. Local, sibling track: `research/devotional-sound-script.md` (Q9 fonts, Q10 shaping, Template L caption sizes for phones, Summary 14 phone-speaker model) and `research/devotional-sound-script-fixtures/` (`caption_size_FontSize23_2026-10-19.csv`, `caption_width_FontSize23_2026-10-19.csv`, `shaping_fixture.tsv` and `.srt`, `phone_speaker_model_2026-10-19.csv`, README) — read 2026-10-19; its numbers are used as inputs and credited where used.
63. FFmpeg source files at four release tags: `libavfilter/vf_subtitles.c` (n6.1.1, n7.0, n8.0, n9.0.2), `libavfilter/drawutils.c` and `libavcodec/ass.c` (n6.1.1, n9.0.2) — https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/libavfilter/vf_subtitles.c (the same path under each tag) — read 2026-10-19 — n6.1.1 draws subtitle colours as BT.601 on YUV; n7.0 uses the link's colourspace; n8.0 adds the `.ass` `YCbCr Matrix` header; the `shaping` option reaches the `subtitles` filter in n9.0; ffmpeg's own SRT-to-ASS header says `YCbCr Matrix: None`.
64. Google Fonts, `ofl/hindvadodara/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/hindvadodara/OFL.txt (raw file read) — read 2026-10-19 — "Copyright (c) 2015 Indian Type Foundry", SIL Open Font License Version 1.1, no Reserved Font Name clause.
65. Google Fonts, `ofl/notosansgujarati/OFL.txt` — https://github.com/google/fonts/blob/main/ofl/notosansgujarati/OFL.txt (raw file read) — read 2026-10-19 — "Copyright 2022 The Noto Project Authors (https://github.com/notofonts/gujarati)", SIL Open Font License Version 1.1, no Reserved Font Name clause.
66. MediaTek, "Helio G25" — https://www.mediatek.com/products/smartphones/mediatek-helio-g25 — read 2026-10-19 in a headless Chromium — video playback H.264 and H.265 / HEVC at 1080P 30 fps; no H.264 profile or bitrate given.
67. Android Developers, Media3 `PlayerView` — https://developer.android.com/reference/androidx/media3/ui/PlayerView — read 2026-10-19 in a headless Chromium — `resize_mode` "Default: fit".
68. Apple Developer Documentation, `AVPlayerLayer.videoGravity` and `AVLayerVideoGravity.resizeAspect` — https://developer.apple.com/documentation/avfoundation/avplayerlayer/videogravity (read through the page's data file) — read 2026-10-19 — default `resizeAspect`, which fits within the layer's bounds.
69. pushtimarg.net, "Seva" — https://pushtimarg.net/seva/ — read 2026-10-19 in a headless Chromium — Mangla: "one should ring the bells thrice and blow the Sankh"; Shayan: "keep a small/soft lamp on"; the routine "should not be viewed with rigidity".
70. pushtimarg.net, "FAQs" — https://pushtimarg.net/faqs/ — read 2026-10-19 in a headless Chromium — a "Chitra Swaroop-Shrinathji" that "had been pusht" is served "from Mangala to Shayan"; no text on phones or screens found.
71. Local: `research/sources/mobile-delivery-whatsapp-excerpts-2026-10-19.txt` — dated text excerpts of [1] to [5].
72. Local: `research/pushtimarg-world.md` (F6, PR2, PR4, PR10, PR14, open Q3) — read 2026-10-19.
73. Local: this track's round-1 fixtures, 2026-10-19: caption colour CSVs, `caption_ycbcr_matrix_example_2026-10-19.ass`, `scaler_bracket_720p_panel_2026-10-19.csv` and the re-cut `gujarati_shaping_freeserif_2026-10-19.srt` and `.png`, all in `research/mobile-delivery-fixtures/`.

---

## Changelog

- **2026-10-19, v1 (Haiku scribe pass).** Built from `research/mobile-delivery.md` (track `mobile-delivery`, including its D-31 update). Sections written as the brief asked. Not yet reviewed by `fable-advisor`. No file under `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited. Nothing was committed.
- **Scope note.** The brief said her region, language, deities and phone were "not yet told". The register (D-31, 2026-10-19) and the research note record them, so this playbook keys on D-31 where phone delivery touches them. The region is left out on purpose, because the repo is public.
- **Skill name.** The research note proposes `phone-delivery-and-keepsake`. The skill was written as `mobile-phone-delivery`, as the brief asked.
- **Register gap.** O-42, O-43 and O-44 are cited in the note but are defined only in `reviews/04-hindu-mobile-briefs-review.md`. `DECISIONS.md` (at this commit) has rows only up to O-35. TODO(orchestrator): add these rows to the register. **Resolved 2026-10-19:** Table 3 of the register absorbs O-42 into O-64 and O-43 into O-54, and O-44 is its own row; the older IDs still resolve to their rows.
- **2026-10-19, round 1 applied (Sonnet implementor, against `reviews/mobile-delivery-round1.md`).** Applied in place: the Gujarati exhibit re-cut with the non-sacred line only and its transliteration filled (Exercise 7, README, research Q8); Noto Sans Gujarati as the default caption face and both OFL licences closed (Step 4, K2, T-M6 row 11); the Christian-layer exclusion reworded so the ghanta, diya and prabhavali are not excluded; K1 and the Google Photos pitfall corrected (manufacturer's gallery sync, "Back up all device folders" asked first, the [12] inference marked); WhatsApp Sources [1], [3], [4] marked script-rendered with a saved dated excerpt; T-M6 row 13 (scrubber page) added; thumbnail rule in Step 7 and Decision 14; the 1 GB reveal-weekend arithmetic in Step 8 and Size and storage check; plus findings of the new "Follow-up research (round 1)": tinted captions pass on ffmpeg n7.0 and later with a tagged master (an `.ass` needs `YCbCr Matrix: TV.709`), the shaping failure was the pre-n9.0 `subtitles` build and not the font, and the Pushtimarg bell and lamp, scaler bracket and player-default answers. No file under `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited. Nothing was committed.
- **2026-10-19, v2 (Sonnet implementor).** Reconciled with DECISIONS.md after the her-world merge (2026-10-19): PH1 and PH2 replace the retired phone-file names throughout (S-57); the her-turn conversation date is Sun 7 Mar after about 14:00 (S-64, W-48); the caption face is Noto Sans Gujarati only, with Hind Vadodara and Mukta Vaani not used (W-21), and an Indic line on an ffmpeg older than n9.0 goes through the `ass` filter (W-75); Exercise 7 is named the single shaping gate (S-65, W-06); Exercise 6 and Decision 7 follow the register's cold-open ladder and the two hum takes (W-36, W-65, W-76, W-70); the deity and darshan rows follow W-61 and PR4 with O-42 resolved to O-64 and O-43 to O-54; the lock-screen still follows W-69 and W-73; the sathiyo row follows W-72 (SW0); the project-phone and sharing rules were already W-73 and W-74 and are unchanged.
- **2026-10-20, Stale-wording sweep (2026-10-20).** The playbook follows the register's phone figures: a PH2 cap of 3.5 Mb/s (W-63), so the PH2 command in T-M1 reads `-maxrate 3500k -bufsize 7M` as in `pipeline/phone/profile.json` and the cap-bound line under the measured sizes reads 247 and 329 MB at 9 and 12 minutes (3.5 Mb/s plus the 160 kbps AAC); and at most 32 characters a phone caption line (W-18) in Step 4, T-M2, K2 and the record of proposed changes. Round 2 adds one clause under the PH2 command in T-M1: its `-bufsize` is twice the cap, by the same convention as PH1's `8M` / `16M`, so the next cap change moves both. No measured size, floor or decision changed.

### Record of the changes this track proposed to other files

*A record, not a to-do list. Status 2026-10-19: the register absorbed the rows addressed to `DECISIONS.md` (W-16, W-18, W-19, W-30, W-63, W-64, W-73, W-74, TD-9, K1, O-54, O-64); the playbook rows below are applied by their owners and tracked in Table 4 of the register (the register wins on any difference). The table stays so a reader can see what this track proposed.*

| File | Section (as it exists) | Proposed change |
|---|---|---|
| `playbooks/theatrical-delivery.md` | T2. Delivery spec sheet | Add a phone column: PH1 and PH2, SDR only, burned phone captions, sizes, the T-M1 checks |
| same | Step 5. Mix the sound in three outputs | Phone files on the online row (-16 LUFS, -1 dBTP), measured on the final MP4 |
| same | Step 6. Burn in the captions; T1. Settings card | `MarginV` 20 or more for the venue file; phone burn-in (FontSize 28, MarginV 40, 32 characters, white); fill-crop rule; tinted captions out unless the twelve-patch caption test passes on the PC build and the master is BT.709-tagged; an `.ass` carries `YCbCr Matrix: TV.709`; the `subtitles` filter before n9.0 shapes Indic text in simple mode |
| same | Step 7. Build the venue file set | Add PH1 and PH2, encoded from the master, not from the venue file |
| same | Step 8. Check every file | Atom order; true peak after AAC; PR3 grain for PH1; twelve-patch colour test; the T-M6 protocol |
| same | T8. Rights-clearance log; T9. Releases pack | `phone_share` column; phone-sharing line in releases 4d to 4g |
| same | T11. Pack list for 26 February 2027 | "Phone by cable" tested for her phone class and the spare laptop, with PH1 on both sticks |
| same | Decisions you'll need to make (TD table) | New TD-9 (phone deliverable) |
| `playbooks/format.md` | Step 8. Harden the slice; Exercise 1: The caption test on a real screen | `MarginV` and phone burn-in; arm's-length test at 35 and 50 cm; phone protocol; Gujarati sizing by KA height (K2) |
| same | Decision 8: Where it lives | New row "her phone, by cable"; shared-album rows marked as downscaling and as cloud copies |
| same | Decision 11: A companion; Step 15. Event kit and delivery | Scrubber page demoted to laptop and archive; phone by cable is a tested route |
| `playbooks/cinematic-quality.md` | T1. Per-shot checklist (PR3 grain survival; TY1) | PH1 passes at CRF 20 (73%) and fails at 22 (43%); PH2 and HEVC exempt or measured at equal viewing scale; phone column for TY1 (x-height 3.2% hard, 3.8% target; strokes 4 px) |
| same | T6. Projection-truth checklist; Exercise 2: Find the dark steps on your screen | Phone-truth sub-list: fill-crop card, 35 and 50 cm caption read, dark steps at 100 and 500 lux, upright view as degraded |
| same | T2. Style bible (decisions 3 and 8) | `phone_min_xheight_pct` 3.2 (target 3.8); Trim P as a third trim beside V and C |
| `playbooks/agent-pipeline.md` | Shot brief (one file per shot, brief.yaml); Step 8. Review pack and critic (gate G2); G6 technical check | `phone_safe`, `hands_box`, `object_box`, `caption_zone`; G2 composites `safe_area_template.svg`; G6 adds the T-M1 checks |
| `playbooks/music-sound.md` | Exercise 6: Mono and small-speaker check; Template G. Mix targets, ducking and the loudness recipe | Phone-speaker pass with the tone ladder; first cold-open sound above 400 Hz; AAC true-peak check |
| `playbooks/surprise-ops.md` | Step 11. The reveal (item 9); Decision 15: Keepsake form; Step 10. Build the reveal (fallback ladder) | Cable copy to her phone as a reveal-weekend step (K1); no QR on the night and the spoken-promise line; scrubber demoted; the printed book's QR codes stay static |
| `playbooks/toolchain.md` | Step 11: Captions; Decision 8: Burned-in captions or soft subtitles? | Split the r9 caption recipe into venue and phone versions; add the libass colour warning (ffmpeg before n7.0 assumes BT.601; from n8.0 an `.ass` without the header does too). The recipe file under `.claude/` is an orchestrator edit, not this scribe's. |
| `DECISIONS.md` (orchestrator, not edited here) | W-18; W-30; new rows | W-18: add `MarginV` 20 or more and the phone burn-in as a second caption setting. W-30: replace the offline page for her phone at G-SLICE (O-30). New rows: PH1 and PH2 specs, TD-9, K1 to K5, and register rows for O-42 to O-44. |
| `skills-staging/mobile-phone-delivery/SKILL.md` | New | Agent form of T-M1, T-M3, T-M6 and the hygiene rule |

Not changed by this track: `playbooks/animated.md`, `playbooks/film-story.md` and `playbooks/ai-imagery.md`. The research note proposes no change to them, and this scribe pass did not re-read them. Any overlap is TODO(research).
