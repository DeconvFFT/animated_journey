# Theatre-grade masters, venue playback and rights clearance

> A plain-language guide for the maker, who works on a Windows PC and is learning by doing. Track: `theatrical-delivery`. Built from `research/theatrical-delivery.md` (research date 2026-10-18). Reconciled with `DECISIONS.md` (the decisions register; where this playbook and the register disagree, the register wins). Nothing here is legal advice. Items marked **TODO(research)** are open and must not be treated as facts.

## Why this matters for our film

On Saturday 27 February 2027, the film will play on a screen and a sound system we do not control. It may be a venue TV, a projector, an LED wall, a laptop or a USB stick. Each one has its own quirks, and the audience will judge the film by what it sees and hears.

The charter asks for a film that could be shown in a theatre. That means one master built to a cinema standard, a few simple files made from it, each one tested on the real screen, and a written record of every right we rely on.

"Mostly public" changes the rights picture. A gathering open to guests beyond the family is a public showing in many places. Music, photos taken by other people and people's voices may then need permission, even if nobody pays. The jurisdiction is not yet known (TD-7), so treat every legal point here as "confirm first".

The surprise also lives in the files. File names, titles, metadata, thumbnails, test clips and the Windows "Recent" list can all give it away.

## Core principles

1. **One master, many derived files.** Everything comes from one 1920x1080, 24 fps ProRes master. Never re-author a shot for one deliverable. The phone files PH1 and PH2 differ from the venue file only in Trim P, their caption burn-in and their encode (`DECISIONS.md` W-63).
2. **Judge on the real screen.** Your monitor is not the reference. Colour, brightness and captions are judged on the screen the audience will see, from the back row.
3. **Plan the failure before it happens.** Assume a cable, a laptop or the TV's file support will fail. Keep a ladder of fallbacks and walk it in rehearsal.
4. **Keep 24 fps.** It is the one frame rate DCP-o-matic calls safe for unknown places [16]. Do not speed up or slow down footage to suit a player.
5. **Cinema sound is not loudness-normalised.** Make three outputs from one mix: cinema, venue and the phone files (PH1 and PH2). A broadcast loudness target is not a cinema target [30][36].
6. **Burn the captions in.** Burned-in captions show on every screen. Soft subtitles depend on the device [20].
7. **Decide who sees it before you clear rights.** Set the door policy first (TD-5). Every asset gets a row in the rights log: cleared, substituted, or a documented risk with reasons and a way to undo it.
8. **Keep the surprise inside the files.** Neutral names, no title metadata, a neutral test clip for staff, and the film played only when the room is empty.

## How to do it, step by step

Work through these in order. Each step ends with a check you can run.

### Step 1. Lock the settings by Sunday 1 November 2026

Make decisions TD-1 to TD-4 (see Decisions) and write them on the settings card (Templates, T1), with the phone, font, script and burn-in rows the register added on 2026-10-19 (`DECISIONS.md` W-16). Save the card in the private repo.

Check: the card exists, is dated and is saved.

### Step 2. Install the tools on the Windows PC

- **DCP-o-matic 2.18.51**, released 16 October 2026. It is free and GPL-licensed, with Windows 64-bit and 32-bit builds [8][10].
- **ffmpeg and ffprobe.** The agent pipeline names the PC build Gyan 9.0.2 [3].
- **mpv or VLC** for playback. mpv does not turn on hardware decoding by default [41].
- **PowerShell's built-in `Get-FileHash`** for SHA-256 hashes [4].

Check: each tool opens and reports its version. How much memory DCP-o-matic uses on Windows is **TODO(research)**. Watch it in Task Manager during Exercise 3.

### Step 3. Prepare the master

- Format: ProRes 422 HQ `.mov`, 1920x1080, 24p, Rec.709, limited range, 10-bit 4:2:2, PCM 24-bit 48 kHz [3]. The master carries BT.709 tags before any caption burn-in, so the burn-in draws in BT.709 (W-16).
- Scans and stills: prepare them at 3840 px on the long edge or larger, so camera moves crop into real detail [3].
- Frame: 16:9 sits inside a 1.85 Flat container. A Scope crop would cut about 26% of the picture height and damage titles and photo moves [31].
- Check: ffprobe reports the size, frame rate, pixel format and colour tags you set. The frame count and duration match the timeline.

### Step 4. Grade once, then check on the screen

- Grade to Rec.709 / BT.1886 at a mid-key look. Rec.709 uses limited-range code values, 64 to 940 for luma on 10-bit [34].
- Working limits (a proposal, not a sourced rule): keep shadows above about code 20 to 24 on 8-bit limited range, keep whites at or below 235 (940 on 10-bit), and check skin tones against a known family photo.
- Make three small trims. They are lookup files applied only when exporting. The master is never touched.
  - **Trim V, for a lit venue:** a starting lift of about 2 to 4 IRE in the shadows and a mid-gamma rise of about 0.05 to 0.10. These are starting values only. They are set on site at the TD-L2b visit (by Sunday 17 January 2027).
  - **Trim C, for a dark cinema:** identity (no change) until a real cinema test.
  - **Trim P, for the phone files:** a mild shadow lift (4 to 7 IRE at codes 24 to 40, black pinned at 16) on top of the one grade, tuned on the project phone at 100 and 500 lux and set at G-SLICE (`DECISIONS.md` W-64; `playbooks/mobile-delivery.md` Exercise 5).
- Hash and log every trim file. The method is ffmpeg's `lut3d` filter. It was run in the cloud container on 2026-10-18 (ffmpeg 6.1.1) with a `.cube` file and gave no error; confirm once on the Windows PC.

Check: the venue test clip (Exercise 4) looks right on the real screen.

### Step 5. Mix the sound in three outputs

Keep dialogue, music and effects as separate stems, and mix once.

- **Cinema:** do not normalise. Keep headroom and real dynamics. Report the loudness for information only and let a cinema technician align the room. A correctly aligned cinema sets the level, not a number [30].
- **Venue:** render three masters at -23, -18 and -16 LUFS integrated, all at -1 dBTP, and choose one at the Mon 22 Feb 2027 venue run against sixty seconds of the hall's own room tone recorded from the back row; if no reading can be taken, load -18 first (`DECISIONS.md` W-19). Check intelligibility in the back row with the oldest listener. Never trust the number over the room [2][5].
- **Phone files (the online row):** PH1 and PH2 carry -16 LUFS integrated and -1 dBTP measured on the final MP4 after the AAC encode (W-19, W-63), plus a phone-speaker pass per cue on the project Android. Streaming services normalise, so a quiet cinema mix posted online would play quietly [38].
- **Settled (`DECISIONS.md` W-19): -1 dBTP everywhere, per R128 and the research; the toolchain's -1.5 was a loudnorm example, not a target [36][2].**
- Delivery is stereo (L/R) for now. A later cinema version may use a 5.1 fold-up with voices in the centre channel, which is the better cinema option (inference) [28].
- **Mono check:** if loudness drops by more than about 3 LU between the stereo and mono-folded readings, the mix has phase trouble that will show on a mono venue PA. This threshold is a rule of thumb (inference). See Exercise 5.

### Step 6. Burn in the captions

- Open captions, burned into the picture, for the venue file and for the first DCP.
- Keep all text inside the central 90% by 90% box. EBU R95 treats the outer 5% as the graphics-safe margin [37].
- At most two lines, 42 characters or fewer per Latin line, and under 20 characters per second [4]. The 42 is a guide: the rule is that a line fits the box in its face and breaks at word boundaries, and Indic faces overflow earlier (`DECISIONS.md` W-18).
- **Venue file:** a line height of 7 to 8% of the picture height. The earlier format note reports that `FontSize=23` in ffmpeg gives about 8.0% at 1080p, tested on a TV from three metres [4]. Confirmed at TD-L2b (by Sun 17 Jan 2027) from caption sizes 20, 23 and 26 on the venue screen; until then 23 is the working value. That is for Latin text. **Gujarati is sized by the height of its base letter KA, not by `FontSize`:** Noto Sans Gujarati gives KA 3.33% of picture height at 23, enough for the venue, and needs 26.2 for the phone's 3.8% target, so the phone files carry their own caption setting (`FontSize=28`, `MarginV` 40, two lines, at most 32 characters, measured to fit the 90% by 90% box in both scripts, block at 68 to 86% of height, white or neutral grey; W-18).
- **Cinema:** start at 5.5 to 6% line height. The same percentage looks about twice as large to a cinema audience as on a 55-inch TV at three metres (computed). Keep captions out of the bottom 8 to 10%, where heads may block them (inference).
- **Festival-style delivery:** a Sundance-style delivery needs a DCP with both a Closed Caption and an Open Caption version. Burned-in captions alone cannot satisfy that (Sundance FAQ 31, document dated 2026-09-08; "subject to change") [88].
- Keep captions out of the black side bars of a Flat container. Do not bury them there.
- **Fonts (W-21, W-75):** OFL fonts only for titles, cards and captions; video titling is a listed permitted use [75]. Every family has a `font` row in the rights log (T8) with its `OFL.txt` hash and the libass `fontselect:` line pasted in the notes. Indic families: Noto Sans Gujarati for captions; Rasa or Baloo Bhai 2 for cards with a Gujarati line and an IAST line in one face; Noto Serif Gujarati for verse; Noto Serif or Tiro Sanskrit for Devanagari verse; Shrikhand and Farsan as outlined title art only; Kumar One outlined title art only. Not used: Hind Vadodara for any date or Samvat (no Gujarati digits); Mukta Vaani for Gujarati text; the plain name "Anek Gujarati"; variable fonts except as static instances. Her script on titles and verse cards travels as shaped outlines, never live text. Windows system fonts are fine rasterised in video, never embedded in a DCP subtitle track [76]; commercial fonts under an Adobe or Monotype subscription are out.
- **Burn-in path for Indic text (W-18, W-75):** on any ffmpeg older than n9.0 the `subtitles` filter shapes Indic text in simple mode and breaks conjuncts, the reph and the short-i without a warning, and `drawtext` hard-codes Latin. Burn Indic text with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709` in the header). The ten-minute `ab.srt` A/B on the PC decides between `subtitles` and `ass`; the PC's Gyan 9.0.2 build is UNVERIFIED until it runs. The shaping burn is a P-LOCK condition. Never run a FAIL render on a mantra, a deity's name or a verse: test syllables only. Tinted captions only after the twelve-patch caption test passes on the PC build.

Check: Exercise 4 shows the three caption sizes from the back of the room.

### Step 7. Build the venue file set

These are the rows of the spec sheet in Templates (T2).

- **Venue primary:** MP4, H.264 High level 4.1, yuv420p, BT.709 tags, AAC-LC 48 kHz stereo at 256 kbps, `+faststart`, `-crf 18 -maxrate 20M -bufsize 40M` [2]. Burned-in captions, a neutral file name, no title metadata.
- **Venue backup:** H.264 Main, level 4.0, 1080p24, about 8 Mbps. This is for old TVs and USB players (inference; test it).
- **Venue test clip:** 60 to 90 seconds with no personal content, carrying a tone ladder from 100 Hz to 3.2 kHz (T7; W-17).
- **Phone files (T2b):** PH1, the phone master, from the ProRes master (never the venue file, never RGB frames): 1920x1080p24 H.264 High 4.1, CRF 20 with an 8 Mb/s cap, AAC-LC 192 kbps, phone captions burned, SDR only, no HEVC (its saving is the grain). PH2, the small copy: 1280x720, CRF 22, 3.5 Mb/s cap, level 3.1, captions burned on the 1080 frame before the downscale; the only file inside WhatsApp's 64 MB document limit. One 9:16 lock-screen still, no vertical cut (W-63).
- **Audio-only or still fallback:** a 3-minute version [5].
- **Projection leader:** the venue file's first thirty seconds are a countdown in her grammar (the years of her life ticking down in each decade's photo texture, one real sound from her world at reference level), decided at G-MASTER, Sat 20 Feb; the rehearsal copy, the test clip and everything the AV person sees keep the neutral slate (`DECISIONS.md` W-53).
- **Online (a hosted link):** H.264 1080p, a cap of about 12 Mbps. Only after the T3 rights gate (Step 11) and the ledger (W-48); there is no live link before the reveal (W-74).

Check: the test clip and the film share pixel format and tags, so one test covers both. Both play on the TV and on the spare laptop from the same path.

### Step 8. Check every file

- Run ffprobe on each file. Read `pix_fmt`, `color_range`, `color_space`, `color_transfer`, frame count and duration [3]. Use the command below. It was run in the cloud container on 2026-10-18 (ffmpeg 6.1.1); confirm it once on the Windows PC:

  ```
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,color_range,color_space,color_transfer,color_primaries,r_frame_rate,nb_frames:format=duration -of default=nw=1 FILE
  ```

  On the container's 1-second 1080p24 test file it printed `pix_fmt=yuv420p color_range=tv color_space=bt709 color_transfer=bt709 color_primaries=bt709 r_frame_rate=24/1 nb_frames=24 duration=1.000000`.
- Run the colour-patch test (within plus or minus 3 out of 255) after every re-encode and on each ffmpeg build: the container's 6.1.1 and the PC's 9.0.2 gave different pixels under identical tags (`DECISIONS.md` W-16) [3].
- Loudness: `ffmpeg -nostats -i in.wav -af ebur128=peak=true -f null -` prints integrated loudness and peak. The command syntax was run in the cloud container, not yet on the PC.
- Metadata: strip it with `-map_metadata -1`, so no title or comment travels with the file. Run in the cloud container on 2026-10-18, `ffmpeg -i in.mp4 -map_metadata -1 -c copy out.mp4` removed the title tag. ffmpeg re-adds a harmless `encoder` tag, which carries no personal data. Confirm on the Windows PC.
- Phone files: add `moov` before `mdat`, true peak after the AAC encode, grain survival of at least 70% on PH1, type floors and strokes, the safe-area overlay on three frames, no metadata, and a neutral code as the file name before the reveal (W-63; `playbooks/mobile-delivery.md` T-M1).
- Hash: make a SHA-256 manifest of each delivery folder using the `mk_manifest.ps1` pattern that the research notes cite [4]. Copy the folder to the drive, then re-check the hashes from the drive.

Check: the manifest lists every file, and every hash matches after the copy.

### Step 9. Make the DCP, after the tests

Do this on the Windows PC, not in the cloud container. The container's root disk was full during testing and cannot hold a DCP [47]. Do it only after Exercise 3 passes. If the PC work is not ready, make the DCP after the premiere.

**Branch: the venue is a cinema with a DCP server.** If the venue survey (T5) says the room is a cinema with a DCP server, the DCP becomes the primary deliverable. Exercise 3 moves to Sunday 29 November 2026, you book a January test slot, and the venue MP4 over HDMI becomes rung 1 of the backup ladder (T3). Otherwise the DCP is a contingency made after the premiere. The venue's written answer, due Sunday 15 November 2026, decides which (`DECISIONS.md` W-17).

Settings in DCP-o-matic (names as in the manual; check each one on screen):

1. **New film,** named with the neutral code name. The title appears on cinema servers and in key files, so it must not carry her name before the reveal [5][15].
2. **Add the ProRes master.** DCP-o-matic reads it through FFmpeg. Reading ProRes is expected to work but is unverified (**TODO(research)**; test it in Exercise 3) [15].
3. **DCP tab:** Container Flat (1.85). Resolution 2K. Frame rate 24. Standard SMPTE. Encryption off. JPEG2000 bandwidth 100 to 125 Mbit/s (the cap is 250). Reels: single. "Use ISDCF name" ticked. Content type: feature or short, to match the final runtime. The content type places the film in the projectionist's interface, so pick the one that matches the runtime [15].
4. **Audio:** six channels is the default. Map L to L and R to R at unity gain. Check what the ISDCF name shows; whether it reads "20" with only L and R mapped is **TODO(research)** [13].
5. **Video tab:** colour preset Rec. 1886 if the grade was made on a gamma-2.4 display, otherwise Rec. 709. Which gamma each preset applies is **TODO(research)**, so compare the two on a known frame. Range: Video (16-235). Scale to fit [12][35].
6. **Timed text:** leave it empty if the captions are already burned in [14].
7. **Make DCP.** Encoding can take many hours [11].
8. **Verify:** in the Player, open Tools, then Verify DCP. Fix every error and read every warning [18].
9. **Play in the Player.** This proves the package is well-formed, not that a cinema will accept it. The manual warns against depending on the Player without a lot of testing [17].
10. **Write the drive.** Use ext2 (DCP-o-matic: the only format guaranteed in all cinemas; ISDCF also allows ext3) with a 128-byte inode, on an MBR partition table with one primary partition of type 0x83. Re-partition any retail USB stick first (ISDCF: retail partition tables are "almost certainly incorrect"). MBR drives must be 2 TB or smaller [19][26]. DCP-o-matic's Disk Writer formats the drive this way [19]. Label the drive "Do not read with a consumer computer" [26]. Never plug it into the Windows PC after it is written [26].
11. **Hash the DCP folder,** copy it to a second place, and re-check the hashes.

Size check: at 125 Mbit/s a finished minute is about 0.94 GB, so a 10-minute film is about 9.4 GB (computed) [15]. Encode speed measured on a cloud container was 3 to 4 wall minutes per finished minute for clean frames and about 12 for grainy frames [47]. Your PC's speed is **TODO(research)**. Record yours in Exercise 3.

### Step 10. Test where it will play

- **Venue survey:** ask the questions in Templates (T5) in your own words, without naming the film's subject. Due by Friday 6 November 2026; the venue's written answer is due Sunday 15 November and decides file or DCP (`DECISIONS.md` W-17, O-21).
- **Test clip first,** with the venue's AV person present. The film itself plays only when the room is empty or only you are present.
- **Visit with the test clip only, by Sunday 17 January 2027 (TD-L2b).** Go with the venue's AV person and play the test clip, never the film. Record the TV or projector settings, check caption sizes 20, 23 and 26 from the back row (with the Gujarati KA check), check the PLUGE and tone level, and write down the lowest tone of the 100 Hz to 3.2 kHz ladder that the room carries from the back row: it decides the venue hum take (W-65). Then set Trim V and the TD-3 caption size from this visit. Without this visit, the first look at the real screen is Monday 22 February, five days before the premiere, and any caption or black-level surprise would force re-exports in premiere week.
- **Full run** on Monday 22 February 2027. Cold starts on Thursday 25 and Friday 26 February. Walk the failure ladder once each with a stopwatch.
- **A later cinema:** ask two or three cinemas for written quotes using the enquiry questions (T6). The pages reviewed for this guide (Picturehouse, Everyman, Cinemark) list no prices, formats or insurance rules, so treat them as questions, not facts [89][90][91].

### Step 11. Clear the rights (start now, in parallel)

- Give every asset its own row in the rights log (T8). One row per asset, cue or person.
- **Sort every person and item into a tier:**
  - **A, in:** a recorded yes on the updated consent card, your own material, or her appearances as you decide. Before the premiere, under only-me mode, see the box below.
  - **B, in with documented risk:** adults in ordinary family, event or holiday photos, shown briefly, with no voice and no sensitive context. The owner is known; under only-me nobody is asked before the premiere, so it carries an accepted-risk entry, ratified in writing after the premiere (`DECISIONS.md` W-46).
  - **C, out unless a yes is on file:** identifiable minors, any voice or video of a living person, named living third parties in hard episodes, ex-partners, estranged people, and any illness, money or conflict scene.
  - **D, out:** the dead, animated or voiced without the closest family's yes; any synthetic voice; invented events shown as fact; identifiable strangers (crop, stylise or leave them out).

> **Only-me mode (decided, `DECISIONS.md` D-03).** The maker is the only person in on the project. Until the maker decides to bring someone in, card 4a (T9) is not read to anyone. Reading it to a relative, lender or contributor is that decision, and it is parked. Before the premiere, Tier A means: the maker's own material, her appearances by proxy, and original, CC0 or licensed assets. Relatives' voices wait for the April version (Sat 24 Apr 2027), recorded after they sign release 4d (T9; `DECISIONS.md` D-05, D-06). So the public cut can contain: the maker's own material and cards (the maker's voice only as W-35 allows); her appearances by proxy; Tier B stills of adults, with no voice; attributed text with no voice; and original, CC0 or licensed music. It cannot contain a recorded voice of a living person before the premiere. Any step that asks a contributor to confirm, sign or approve (for example TD-L6) waits for the same decision. **Decision point: Sunday 3 January 2027** (T4, TD-L2c), when the narration plan is fixed.

- **Music:** a commercial recording needs a sync licence from the publisher and a master licence from the label. A public-performance licence is a third, separate right [82]. A venue's blanket licence, where there is one, normally covers performance, not copying a recording into your film (background; unverified) [82]. For a public gathering the premiere's sound is the maker's own captures and hum (`DECISIONS.md` W-44); CC0 or CC BY only as a labelled stand-in and only if the sound is hers (O-72); no sung recording of any kind before April (D-05). "Devotional" does not mean free: the words, the tune, the arrangement, the recording and the performance are five separate questions on every cue, and `composition_status` and `recording_status` are filled separately (W-79).
- **Photos taken by others:** find the photographer. Look for a studio stamp on the back of the print, and ask the family. Record every search step. Orphan works have no US safe harbour [54]. UK IPO application fee £20 for one work, £24 for two, £30 for five, £40 for ten, £60 for twenty, £80 for thirty; non-refundable; a separate licence fee is payable only if the licence is granted; licence up to 7 years; UK use only; film and photographs are covered; page updated 1 Dec 2025, read 2026-10-18 [62].
- **Games and brands:** none used (D-29); no third-party game footage by default. The T8 game row stays as a closed question.
- **Art, deity images and fonts (W-46, W-61):** no deity is drawn, generated or photographed, and AI never touches one; a hand-traced plate comes only from a logged public-domain source; a commissioned painting is April-only and name-free through a gallery under a signed s.17(b) letter; a museum photograph of a public-domain painting is a consult question (T10, 22). Each such item has an `artwork`, `deity_image` or `commissioned_art` row with a `tradition_origin` note, and each font a `font` row (T8).
- **AI-assisted material:** every L2-or-higher item needs its tool name, version, date and tool terms. Keep a human-contribution note for each one, and put a pre-roll line before the title [53][65].
- **Accepted risk:** write down why, how you would undo it, who is exposed, and the date. Leave at least 48 hours between drafting and deciding (inference). Get the Fable advisor's written flag on every Tier C item and every accepted risk. The mechanism: write the item as `rights/flags/<asset_id>.md` (why, undo, exposed, draft date) and request a Fable review of that file. Do not set status RISK or admit a Tier C item until the file carries a dated advisor line and 48 hours have passed since the draft date.
- **The consult:** book one hour with a local rights professional by Friday 4 December 2026. Ask it as a hypothetical, using the question list (T10). Whether to tell a lawyer about the surprise is your call.

### Step 12. After the premiere

- **Written releases** from contributors, lenders, parents of minors, the closest family of anyone who has died, and her. Send them between Sunday 28 February and Saturday 6 March 2027 (TD-L15). Ask for a written yes before any wider showing [79].
- **Her release** is offered after your turn conversation on Sunday 7 March 2027 after about 14:00, else Monday 8 March (moved off Maha Shivaratri; `DECISIONS.md` W-48). It has no deadline (T9, 4e).
- **Phone copies (TD-9, W-74):** nothing on her phone or any relative's before the reveal. On reveal weekend, with her yes and the backup question (K1) answered, PH1 goes onto her phone by cable (PH2 if under 1 GB is free) and the file is renamed to the title in her script. Relatives get PH2, or PH1 where storage allows, as a WhatsApp document only after the ledger closes and the maker says yes, each send logged with `phone_share = relatives_after_ledger`.
- **The April version:** relatives' response recordings run Sun 7 Mar to Sat 10 Apr 2027, the consent ledger closes Mon 29 Mar, and the April version is mixed Sun 11 to Fri 23 Apr and delivered Sat 24 Apr (`DECISIONS.md` W-48, D-06).
- **No cinema, festival or online link** until the consent ledger closes on Monday 29 March 2027 and the rights log shows green for T3 or T4 [5].

## Learn-by-doing exercises

### Exercise 1. Read the colour path in your own words

- **Goal:** explain what DCP-o-matic does to a Rec.709 frame, in five sentences.
- **Steps:** read the video-content chapter [12] and the colour paper [22]. Write one sentence for each step: linearise, convert to XYZ with a matrix, adjust the white point, scale by 48/52.37, apply the 1/2.6 gamma.
- **Time:** about 90 minutes.
- **Good looks like:** you can name the five steps. You can say which source preset you would choose for a gamma-2.4 grade, and why. You know that the gamma each preset uses is still unverified.

### Exercise 2. See judder with your own eyes

- **Goal:** find the TV and frame-rate settings that keep a slow pan smooth.
- **Steps:** get a 24p slow pan (test clip item 7). Play it on your home TV in each picture mode you can select. Turn motion smoothing off [40]. Find the refresh-rate setting on the PC (the Windows Settings path is **TODO(research)**). Note what you see at each setting.
- **Time:** about 45 minutes.
- **Good looks like:** you can say which picture mode and refresh rate give smooth motion. You can explain why 24 fps on a 60 Hz screen judders [39] and why a 120 Hz screen can avoid it [40].

### Exercise 3. Make and verify a 60-second test DCP

- **Goal:** prove the DCP path works on your PC from start to finish. Deadline: Sunday 20 December 2026 (TD-L4).
- **Steps:** use a 60-second test clip with no personal content. Follow Step 9. Note the encode time and the memory use you see. Run Verify and fix every error. Play the DCP in the Player. Write it to a spare USB drive, not one you will ship, because formatting erases the drive. Hash the folder and compare after copying.
- **Time:** about 2 to 4 hours, mostly waiting (an estimate; not measured on the PC).
- **Good looks like:** zero errors in Verify, every warning read and explained, the Player plays it start to finish, and the hashes match. You have written down the encode time per minute and the memory use.

### Exercise 4. Watch the venue test clip on your home TV

- **Goal:** find picture and caption problems before the venue does.
- **Steps:** dim the room to "low, not dark" [5]. Set the TV to cinema or film mode, with overscan off, HDR off and motion smoothing off [40][42][45]. Play the test clip. Check the PLUGE bars: can you tell levels 16, 20 and 24 apart? Check the ramp for clipping and the gradient for banding. Check the three caption sizes (20, 23 and 26) from three metres. Play the 1 kHz tone, then the left-only and right-only channels.
- **Time:** about 60 minutes.
- **Good looks like:** you can name the TV settings you used. The captions read from the back of the room. Nothing is cut at the edges. The top of the ramp shows no flat clipping.

### Exercise 5. Run the loudness and mono-fold checks

- **Goal:** know whether a file will survive a mono venue PA.
- **Steps:** run `ffmpeg -nostats -i in.wav -af ebur128=peak=true -f null -` on a stereo file. Then run the mono-fold version, `-af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true"`, on the same file. Compare the two integrated readings and note the peak. Then run the ffprobe command from Step 8 on the same file and note `pix_fmt`, `color_range` and the frame count.
- **Time:** about 30 minutes.
- **Good looks like:** both numbers are written down. A drop of more than about 3 LU is a warning sign (rule of thumb, inference). The loudness and mono-fold syntax has been run in the cloud container and still needs a run on the PC. The ffprobe check was run there on 2026-10-18 too.

### Exercise 6. Hash a folder and check the copy

- **Goal:** prove a copy is identical to the original.
- **Steps:** build a SHA-256 manifest of a test folder using the `mk_manifest.ps1` pattern that the research notes cite [4]. Copy the folder to a USB stick. Re-hash from the stick and compare line by line. Keep the manifest outside the stick.
- **Time:** about 30 minutes.
- **Good looks like:** every line matches. Any mismatch means copy the folder again before anything else.

### Exercise 7. Fill in the rights log for five rows

- **Goal:** learn the log before you need it.
- **Steps:** copy the CSV header from T8. Enter the sample rows from T8. Add one row for a photo you already have, with status NS (not started). Fill in the tier, the jurisdiction note and the evidence fields. Do not contact anyone. Keep the file in the private repo.
- **Time:** about 60 minutes.
- **Good looks like:** every row has a status from the allowed list, a tier, a jurisdiction note that begins "Jurisdiction not yet known; confirm; not legal advice", and an evidence reference.

### Exercise 8. Write your own venue and cinema questions

- **Goal:** ask neutral questions that reveal nothing about the film's subject.
- **Steps:** read the venue survey (T5) and the cinema enquiry (T6). Rewrite five questions in your own words. Keep each one short and neutral. Do not mention the film's subject or her.
- **Time:** about 45 minutes.
- **Good looks like:** each question is short, covers one thing, and could be asked by any event host.

### Exercise 9. Check the consent card against the truth

- **Goal:** make sure the card you will read to contributors is true.
- **Steps:** fill every bracket in the consent card (T9, 4a). For each sentence, write down whether it is true today. If a sentence is not true, change it or cut it. Read the card aloud once, alone, on a timer. Do not use it with anyone until its bracketed lines are true. While only-me mode holds (Step 11), do not read it to anyone at all.
- **Time:** about 45 minutes.
- **Good looks like:** every bracket is filled, every sentence is true, and the card commits you to a written release before any wider showing.

## Templates and checklists

### T1. Settings card (fill in by Sunday 1 November 2026)

```
TD-1 working size:      1920x1080, 16:9; stills 3840 px on the long edge or more   [ ] confirmed
TD-2 frame rate:        24 fps everywhere                                           [ ] confirmed
TD-3 captions:          burned-in open; venue line height 7-8% (set at TD-L2b); cinema start 5.5-6%; Gujarati sized by KA height, phone file its own setting (W-18) [ ] confirmed
TD-4 DCP:               Flat 1998x1080, SMPTE, unencrypted, 24 fps                  [ ] confirmed
Venue loudness:         three masters (-23, -18, -16 LUFS integrated), all -1 dBTP, chosen at the Mon 22 Feb run;
                        -18 first if no reading can be taken (DECISIONS.md W-19; -1 dBTP per R128, the toolchain's -1.5 was a loudnorm example)
Venue colour trim V:    ______ (starting values: lift 2-4 IRE; mid-gamma +0.05 to +0.10; final at TD-L2b, by 17 Jan 2027)
Cinema colour trim C:   identity until a real cinema test                           [ ]
Phone colour trim P:    ______ (4-7 IRE lift at codes 24-40, black pinned at 16; set at G-SLICE, W-64)
Phone rows (W-63):      PH1 1920x1080p24 H.264, CRF 20, 8 Mb/s cap; PH2 1280x720, CRF 22, 3.5 Mb/s cap; SDR only;
                        BT.709 tags on the master before the burn-in; -16 LUFS integrated, -1 dBTP on the final MP4 [ ]
Font rows (W-21):       every family with its OFL.txt hash in a T8 font row, libass fontselect: line pasted       [ ]
Script decision (O-15): cards in Gujarati; captions in the room's language; Sanskrit verse in Devanagari unless
                        the family reads it in Gujarati script                                              [ ]
Burn-in path:           subtitles | ass, from the ten-minute ab.srt A/B on the PC with the libass+HarfBuzz check [ ]
Gujarati fixture:       32 strings run on the PC, in Chromium and on the project Android, read by the native reader (O-62) [ ]
Colour-patch test:      within +/-3/255 on every command-line template on each ffmpeg build, incl. the twelve caption colours [ ]
Decided by / date:      ______
```

### T2. Delivery spec sheet

| Parameter | Venue, Sat 27 Feb 2027 | Cinema (later, DCP) | Online (private link, later) | Archive |
|---|---|---|---|---|
| Purpose | Plays on whatever the venue has | A hired or festival cinema screen | Family and invited viewers | Preservation and re-making |
| Picture | 1920x1080, 16:9, 24p constant, BT.709, limited range, burned-in open captions | DCP 2K Flat container 1998x1080; picture centred with 39 px black bars each side; XYZ 12-bit via DCP-o-matic [12][22][31] | Same as venue, 1080p24 | ProRes 422 HQ 1920x1080 24p (FFV1 optional) [2][3] |
| Container and codec | MP4, H.264 High 4.1, yuv420p, `+faststart` [2] | SMPTE DCP (picture and sound MXF, CPL, PKL, ASSETMAP), unencrypted [15][21] | MP4, H.264 High, CRF 20, 12 Mbps cap [2] | MOV (ProRes) and/or MKV (FFV1), PCM audio [2] |
| Bit rate | Up to 20 Mbps | JPEG2000 100 to 125 Mbit/s (cap 250) [15][18] | 8 to 12 Mbps | Master data rate |
| Audio | AAC-LC 48 kHz stereo 256 kbps; three venue masters (-23, -18, -16 LUFS), all -1 dBTP, one chosen at the 22 Feb run (`DECISIONS.md` W-19) [2][36] | PCM 24-bit 48 kHz; L and R in channels 1 and 2; cinema mix with headroom, not normalised [28][30][31] | AAC 256 kbps stereo; -16 LUFS, -1 dBTP [38] | PCM 24-bit 48 kHz, plus stems |
| Captions | Burned in; two lines; inside the 90% by 90% box [37][4] | Burned in by default, or a SMPTE subtitle track with an OFL font [14][27]. A Sundance-style delivery also needs a Closed Caption and an Open Caption DCP version, which burned-in captions alone cannot satisfy (Sundance FAQ 31, document dated 2026-09-08; "subject to change") [88] | Burned in, plus SRT or VTT sidecar | SRT, VTT, plain-text transcript |
| Rights gate | T2 (public gathering): every row green or a documented risk; no unlicensed commercial music; no deity drawn, generated or photographed (W-61); every font OFL with a `font` row (W-21) | T4: all T3 items green; releases signed; E&O decision; music cue sheet; AI disclosure | T3: releases signed; your explicit yes for the host [4] | Log, ledger and releases kept with the masters, in encrypted storage |
| File name | Neutral code name; no personal data; no title metadata; version and date | ISDCF-generated name; neutral title [15][25] | Neutral | Descriptive, in a folder with a README |
| Media | Two USB sticks (FAT32 if the file is under 4 GiB, which at 20 Mbps is about 28 minutes, computed; exFAT if the TV takes it) [43][44], plus two laptops | Drive: ext2 (the only format DCP-o-matic guarantees in all cinemas; ISDCF also allows ext3), 128-byte inode, MBR with one primary partition of type 0x83; re-partition retail sticks first; MBR drives must be 2 TB or smaller; label "Do not read with a consumer computer" [19][26] | Upload | Two physical copies plus a second encrypted SSD kept elsewhere; no cloud copy of family media (`DECISIONS.md` W-25) [2] |
| Checks | ffprobe tags and pixel format; colour-patch test; loudness and mono-fold; caption legibility at 3 m; hashes; gates G6 and G6b [3] | Verify DCP with no errors; play in the Player; SHA-256 manifest; real-cinema test slot [18][17] | ffprobe; watch on a phone and a TV | Hash check yearly [2] |
| Fallback | Backup ladder (T3) | A second DCP with burned-in captions if subtitle rendering fails [20] | n/a | n/a |

### T2b. Phone files (PH1 and PH2; `DECISIONS.md` W-63, W-73, W-74)

One picture, two files, never a second edit: both are emitted from the one locked 16:9 timeline and differ from the venue file only in Trim P, their caption burn-in and their encode. Windows numbers are UNVERIFIED until `windows_check_report.json` is in the repo. Templates and checks: `playbooks/mobile-delivery.md` T-M1.

| Parameter | PH1, the phone master | PH2, the small copy |
|---|---|---|
| Source | The ProRes 422 HQ master, never the venue file or RGB frames | The same master |
| Picture | 1920x1080p24, H.264 High 4.1, yuv420p, BT.709 tags on the master before the burn-in, CRF 20 with an 8 Mb/s cap, SDR only, no HEVC | 1280x720, CRF 22, 3.5 Mb/s cap, level 3.1, captions burned on the 1080 frame before the downscale |
| Audio | AAC-LC 192 kbps 48 kHz stereo; -16 LUFS integrated and -1 dBTP measured on the final MP4 | The same audio |
| Container | `+faststart`, `-map_metadata -1`, neutral code as the file name before the reveal | The same |
| Captions | Phone setting: `FontSize=28`, `MarginV` 40, two lines, at most 32 characters, block at 68 to 86% of height, white or neutral grey; Gujarati by KA height (26.2 with Noto Sans Gujarati) | The same, burned before the downscale |
| Size | 149 to 262 MB typical at 9 to 12 minutes, 737 MB ceiling | 39 to 92 MB; the only file inside WhatsApp's 64 MB document limit |
| Goes to | Her phone by cable on reveal weekend with her yes; relatives after the ledger where storage allows | Low-storage phones; relatives after the ledger |
| Checks | ffprobe fields and frame count equal to the timeline; `moov` before `mdat`; twelve colour patches within +/-3/255 on the PC build; true peak after AAC; grain survival of at least 70% on PH1; type floors and strokes; safe-area overlay on three frames; no metadata | The same |

### T3. Venue tech checklist

**TV**
- [ ] Picture mode: cinema, film or movie. Motion smoothing off [40]. Noise reduction off.
- [ ] Overscan off. The name varies ("just scan", "screen fit", "full pixel"). Many LCD TVs ship with it on [45].
- [ ] HDR off [42]. Energy saving and auto-dimming off.
- [ ] HDMI input set to PC or game mode if the TV offers it (UNVERIFIED; test).
- [ ] 1920x1080 at 24 or 60 Hz.
- [ ] USB: FAT32 cannot hold a file of 4 GiB or more (4 GiB minus one byte) [44]. exFAT is supported by many flat-panel TVs, but not all [43]. Whether this venue's TV takes exFAT, MKV or soft subtitles is **TODO(research)**. Keep captions burned in, use MP4 with H.264, and test.

**Projector**
- [ ] Native resolution and aspect (1080p, or WUXGA 16:10, which letterboxes 16:9). Keystone and lens shift set once.
- [ ] Warm-up time, lamp or laser hours, eco mode off, screen gain.
- [ ] Lights low, not dark [5].

**LED wall (questions for the operator; the specifics are TODO(research))**
- [ ] Native pixel resolution and aspect; whether the processor scales 16:9 into the wall or crops it.
- [ ] Accepted frame rates. Brightness setting (indoor walls are often far brighter than a TV, so reduce it).
- [ ] Colour temperature and gamma. Whether the operator controls a play source.
- [ ] Ask for a test pattern at the wall's native size. The wall has no audio; plan the sound separately.

**Windows laptop**
- [ ] Charger plugged in. Power mode: best performance. Screen and sleep timers set to never.
- [ ] Night light off. HDR off [42]. Do Not Disturb on, notifications hidden [5].
- [ ] Windows updates paused for the week. Mail, chat and cloud sync closed [5].
- [ ] Neutral desktop. Explorer previews and "Recent" lists cleaned.
- [ ] Output 1920x1080, scaling 100%. Refresh rate suits 24 fps where offered (the Settings path is TODO(research)).
- [ ] Audio output set to 48 kHz, 24-bit (inference). Audio enhancements off.
- [ ] Full-screen player (VLC or mpv) with the file loaded and paused on frame one. Go full screen first, then play [41].

**Audio routing**
- [ ] HDMI to TV, projector or AV receiver. Stereo mode, dialogue enhancement off.
- [ ] 3.5 mm to a venue mixer through a stereo DI box or lead. Set the level with the 1 kHz tone.
- [ ] Watch for ground-loop hum. Many venue systems sum to mono, so run the mono-fold check.
- [ ] The maker holds the master fader (`DECISIONS.md` W-54); ask what else the venue controls. Know where the microphone is for a 30 to 60 second welcome [5].

**Kit**
- [ ] Two USB sticks in different pockets, PH1 on both beside the venue file. Two laptops with the same file at the same path.
- [ ] Spare HDMI cable. Adapter kit (USB-C, DisplayPort, mini-HDMI). USB-C hub. Chargers.
- [ ] Printed running order. The test clip on a stick.
- [ ] No cloud copy of family media (`DECISIONS.md` W-25, D-15) [1][4].

**Backup ladder** (if the Step 9 DCP-server branch applies, rung 1 is the venue MP4 over HDMI)
1. Laptop playing the screening file.
2. Second laptop with the same file.
3. USB stick straight into the TV or projector media player (needs the exFAT and MP4 test).
4. PH1 on a phone by cable (the cable and adapter for her phone class, tested on a project phone), or cast.
5. The 3-minute audio or still version.
6. A postponed private evening, said plainly.

### T4. Run-sheet lines (technical)

Numbered to merge into the surprise-ops key dates and the reveal-day run sheet [5].

| ID | When | Who | Action | Pass criterion | If it fails |
|---|---|---|---|---|---|
| TD-L1 | Sun 1 Nov 2026 | Maker | Write TD-1 to TD-4 into the settings card | Card saved in repo | n/a |
| TD-L2 | By Fri 6 Nov 2026 | Maker | Venue survey (T5); the written answer is due Sun 15 Nov and decides file or DCP (`DECISIONS.md` W-17) | Answers logged in `venue.json` | Assume the worst case: laptop, HDMI, TV |
| TD-L5 | By Fri 4 Dec 2026 (follow-up Jan 2027) | Maker | Hold the consult; update the rights log and the releases | Notes saved | See Decisions |
| TD-L3 | By Sun 20 Dec 2026 (G9) | Maker, agents | Build and view the venue test clip on the home TV; caption sizes 20, 23, 26 at 3 m; mono-fold; ffprobe; the slice's PH1 played on both project phones | All clip checks pass | Fix and rerun |
| TD-L4 | By Sun 20 Dec 2026 | Maker | Make a 60-second test DCP on the PC; Verify; play in the Player | Zero errors; plays | Move DCP work to after the premiere |
| TD-L2c | Sun 3 Jan 2027 | Maker | Decide whether anyone is brought in (the only-me question, Step 11). Until then, card 4a is not read to anyone | Decision written down, with its date | Stay in only-me mode; the public cut keeps no recorded voice of a living person |
| TD-L2b | By Sun 17 Jan 2027 | Maker, with the venue AV person | Visit with the test clip only (no film). Record TV or projector settings, caption sizes 20, 23 and 26 from the back row with the Gujarati KA check, PLUGE and tone level, and the lowest tone of the 100 Hz to 3.2 kHz ladder the room carries from the back row (the venue hum take, W-65). Set Trim V and the TD-3 caption size from this visit | Settings recorded; Trim V and caption size set | If the venue is not booked by 17 Jan, say so and move this line; keep it before TD-L8 |
| TD-L6 | Mon 15 Feb 2027 (contributor placeholder: Mon 8 Feb) | Maker | Contributor clip confirmation (void under only-me; a dated placeholder that fires only if TD-L2c brought someone in, and then on Mon 8 Feb 2027; `DECISIONS.md` D-03, W-08); rights-log review | Hash matches, or the diff is read | Remove the asset or seek permission |
| TD-L7 | Fri 19 Feb 2027 (withdrawals close, surprise-ops; picture lock is Sat 6 Feb 2027, production-scale G-LOCK) | Maker | Freeze the rights log, AI cue sheet, music cue sheet and credits; withdrawals are executed as removals (understudy swaps), never a re-edit (`DECISIONS.md` W-08, W-47) | Every row has a status | Take out or substitute |
| TD-L8 | Sat 20 and Sun 21 Feb 2027 | Maker, agents | Final exports (G-MASTER): master, venue file as three loudness masters (-23, -18, -16 LUFS, all -1 dBTP; `DECISIONS.md` W-19), backup file, audio-only fallback, PH1, PH2 and the 9:16 still (W-63); apply trims (V, C, P); ffprobe, loudness, mono-fold; hashes; two sticks; gate G6 [3] | G6 passes | Re-export |
| TD-L9 | Mon 22 Feb 2027 (full run) | Maker with venue AV operator | (1) Power the chain from cold; time to first frame. (2) Play the test clip: picture mode, overscan, HDR off, bars, PLUGE, ramp, tone level, left and right, caption size from the back row; record sixty seconds of the hall's room tone from the back row, play the three loudness masters against it and choose one (`DECISIONS.md` W-19). (3) Room empty: play the first 5 and last 5 minutes and three spot sections. (4) Walk failure rungs 1 to 4. (5) Photograph settings and cabling. Gate G6b | Plays at the right levels; captions readable; no overscan crop; sound intelligible; mono-fold OK; cold start under 2 minutes | Adjust and repeat on Thursday or Friday |
| TD-L9b | Tue 23 Feb 2027 | Maker | Optional: re-render the AMB stem's last 20 seconds with the hall's room tone from the 22 Feb run; the only permitted sound change of premiere week (`DECISIONS.md` W-20) | Change logged; hashes updated | Keep the existing stem |
| TD-L10 | Wed 24 Feb 2027 (room brief) | Maker | Confirm AV access times with the venue (send no content) | Times confirmed | n/a |
| TD-L11 | Thu 25 Feb 2027 (cold start 1) | Maker, with operator | Cold start on the real device and cable from power-off | First frame within 2 minutes | Rehearse again Friday |
| TD-L12 | Fri 26 Feb 2027 (cold start 2, pack list) | Maker | Cold start 2; pack list (T3, Kit), with PH1 on both sticks and the phone cable and adapter | Pack list ticked | n/a |
| TD-L13 | Sat 27 Feb 2027, S minus 4 h and S minus 2 h | Tech | Set up; run the test clip; confirm Do Not Disturb, notifications hidden, mail and chat closed [5]; play the first and last 30 seconds; spoken-line sound check; snapshot settings | As rehearsal | Use the ladder |
| TD-L14 | End of night | Tech | Back up any agreed room recording; delete extras; collect USB sticks [5] | Sticks accounted for | n/a |
| TD-L17 | Sat 27 and Sun 28 Feb 2027 (reveal weekend) | Maker, with her yes | K1 first (is "Back up all device folders" on?); then PH1 by cable (PH2 if under 1 GB is free); rename the file to the title in her script; offer the lock-screen still; nothing to relatives yet (TD-9; `DECISIONS.md` W-73, W-74) | PH1 plays at one tap from her gallery or app folder | Tablet or stick route (W-73); nothing is copied without her yes |
| TD-L15 | Sun 28 Feb to Sat 6 Mar 2027 | Maker | Send post-premiere releases (T9, 4d to 4g); her turn conversation on Sun 7 Mar after about 14:00, else Mon 8 Mar [5] (W-48) | Requests sent | n/a |
| TD-L16 | Mon 29 Mar 2027 (ledger closes) | Maker | Close the consent ledger; set T3 and T4 gates in the rights log | Every row kept, changed, removed or closed until a date | No wider showing |
| TD-L18 | After Mon 29 Mar 2027 and a green rights log | Maker, with a yes per relative | PH2 (or PH1 where storage allows) as a WhatsApp document, once, never as media; log each send with `phone_share = relatives_after_ledger`; every Tier B still has its understudy first (TD-9; W-74) | Each send logged | No send |

### T5. Venue survey questions

Ask in your own words. Do not mention the film's subject.

1. Screen type and size: TV, projector or LED wall. Native resolution, aspect ratio, distance to the back row.
2. Inputs: HDMI count and version, USB media playback, VGA or other. Can we bring our own laptop? Who operates it?
3. Projector: lumens or laser, lens shift, mounting, warm-up time. Can the lights be dimmed to "low, not dark"?
4. LED wall: processor input resolution and frame rates. Does it scale 16:9 or crop? Brightness setting. Colour temperature. A test pattern at native size.
5. Sound: PA make, mixer inputs (3.5 mm, RCA, XLR), mono or stereo, subwoofer. Is there a microphone for a welcome? Who controls the fader?
6. Access: dates and hours for tests, time to rig, power, Wi-Fi.
7. Licences: does the venue hold a music licence, and what does it cover? Does it require our own insurance? Any filming rules?
8. Staff: names, and what they will be told (a truthful minimum only).
9. Backup kit on site: spare HDMI, adapters, a second player.
10. Capacity and door policy.

### T6. Cinema enquiry questions

Ask two or three cinemas for a written quote.

1. Which screen sizes and formats (Flat, Scope)? Is the projector 2K or 4K?
2. Do you accept a DCP (on what drive format, or by download), or only HDMI, Blu-ray, ProRes or MP4?
3. Is a tech rehearsal included? How long, and when?
4. What is the hire price by day and time, and what does it include (projectionist, microphone, house lights, captions)?
5. What insurance, licences or clearance statements do you require from me (public liability, E&O, music)?
6. Can I sell tickets or take donations, or must entry be free or by invitation?
7. Does your own music licence cover anything I play, or only what is in my film?
8. Can I film or stream the event, and can I bring my own sound mix?
9. What is your cancellation policy and notice period?
10. Who will be in the room (staff names), and what do they need to know? Truthful minimum only.

### T7. Venue test clip contents

60 to 90 seconds, no personal content, built by the agents. Its tags and pixel format must match the venue file.

1. Countdown and slate (code name, version, date).
2. Colour bars and PLUGE (black level).
3. Grey ramp from 0 to 100% in 10-bit steps (clipping and banding), then a smooth gradient (banding).
4. A still of a face with a known skin tone (a stock public-domain face, or a non-identifiable test image) for the skin check.
5. A 1 kHz line-up tone at -20 dBFS, then left-only, right-only and pink noise (left and right ID, level, mono-fold).
6. Caption test: three sizes (FontSize 20, 23, 26) inside the 90% box, with frame outlines at 100%, 96.5% and 95% to show overscan and masking, and one line of Gujarati test syllables (never a mantra, a deity's name or a verse) for the KA-height check from the back row (W-18).
7. A slow 24p pan across a detailed image (judder and motion smoothing).
8. A one-minute speech sample at the film's mix level (intelligibility).
9. A tone ladder from 100 Hz to 3.2 kHz: the lowest tone the room carries from the back row is written down at TD-L2b and decides the venue hum take (W-17, W-65).

### T8. Rights-clearance log

One row per asset, cue or person. The log is a CSV in the private repo, with sheets for `assets`, `music_cues`, `ai_items`, `persons_releases` (the consent ledger), `fonts` and `games_brands` (a closed question under D-29).

Header:

```
asset_id,type,title_or_description,where_used,how_obtained_and_by_whom,rights_holder_and_contact,persons_depicted,minor_flag,deceased_flag,needed_T1,needed_T2,needed_T3,needed_T4,permission_type,scope_media_territory_term_event,fee,status,evidence_ref_and_sha256,status_date,decided_by,advisor_flag,risk_tier,jurisdiction_note,substitute_asset_id,ai_label_L0_L5,ai_tool_version_date,music_cue_ref,release_id,tradition_origin,phone_share,composition_status,recording_status,notes
```

Column guide:
- `type`: photo, video, audio, music, voice, font, game, brand, ai, text, artwork, deity_image, commissioned_art or other. `deity_image` is expected to stay empty: no deity is drawn, generated or photographed (W-61).
- `tradition_origin`: a short note on where the item comes from in her tradition, with its source. `phone_share`: `none`, `her_device_only`, `relatives_after_ledger` or `public` (W-46, W-74). `composition_status` and `recording_status` are mandatory, as separate columns, on every `music` row (a label's "Traditional" is `unknown`).
- `needed_T1` to `needed_T4`: Y (needed), N, ? (unknown, ask) or V (venue-dependent). T1, her own version (the April version, `DECISIONS.md` D-06), carries less exposure but is not zero, so third-party commercial assets stay "?" there.
- `status`: NS (not started), ASKED, GRANTED, REFUSED, SUBST (substituted), RISK (accepted documented risk), OUT, VERIFY (for the consult).
- `risk_tier`: A, B, C or D (see Step 11).
- `advisor_flag`: the path `rights/flags/<asset_id>.md` and the date of the Fable advisor line (Step 11).
- `jurisdiction_note`: begins "Jurisdiction not yet known; confirm; not legal advice:" until TD-7 is answered.
- A RISK row must also say why, how it would be undone, who is exposed, and the date.

Sample rows (from the research notes):

| asset_id | type | where | rights holder | needed T1/T2/T3/T4 | permission | status | evidence | tier | note |
|---|---|---|---|---|---|---|---|---|---|
| PH-0042 | photo | Ch.1 | Aunt (took it, 1978) | ?/Y/Y/Y | None before the premiere under only-me (nobody is asked, `DECISIONS.md` W-46); written release 4d to 4g after it | RISK | rights/flags/PH-0042.md | B | Documented risk (an adult, no voice), ratified in writing after the premiere |
| PH-0107 | photo | Ch.2 | Studio stamp (defunct?) | ?/Y/Y/Y | None | VERIFY, SUBST candidate | scan of back, note | B | Search done 2026-xx-xx; UK IPO application fee £20 for one work (sliding scale) plus a licence fee; UK use only; US has no safe harbour |
| MU-003 | music | Ch.3 bed | CC BY composer | Y/Y/Y/Y | CC BY 4.0, credit | GRANTED | licence PDF | n/a | Credit in end titles |
| MU-011 | music | Ch.4 | Label and publisher | ?/Y/Y/Y | Sync and master needed | NS | none | n/a | Substitute with MU-003 |
| FN-001 | font | Titles | SIL OFL font | N/N/N/N | OFL | GRANTED | font file, OFL.txt and its hash, libass `fontselect:` line | n/a | Rasterised in video (her script as shaped outlines); in a DCP track only an OFL font |
| GM-002 | game | n/a | n/a | N/N/N/N | n/a, none used (D-29) | OUT | none | n/a | Kept so the log shows the question closed |
| AI-014 | ai | Ch.2 | Tool terms; human selection | ?/Y/Y/Y | Tool terms read 2026-xx | GRANTED | steps.csv row | n/a | Label L4b; pre-roll line |

Before T4, every row needs `permission_type`, `scope`, `evidence_ref`, and a signed release or documented exception for every person in Tiers A to C.

### T9. Releases pack

Principles: say what the film is; state nothing untrue; you may omit the fact of the surprise, but not anything false; offer a way out; keep each text to one page; write in the person's language. Jurisdiction and legal wording are placeholders. **Under only-me (`DECISIONS.md` D-03), 4a to 4c and 4h are not used before the premiere; 4d to 4g are sent Sun 28 Feb to Sat 6 Mar 2027 (W-48), and 4d to 4g gain the line "[ ] a copy of the film on my relatives' phones, sent by WhatsApp or similar; I understand a forwarded copy cannot be recalled" (W-48).**

**4a. Contributor consent card, version 2.** Read it aloud on the recording. It replaces the old card in surprise-ops [5]. Read it only when the bracketed lines are true. **Only-me mode:** nobody is read card 4a before the premiere (`DECISIONS.md` D-03); it is the April version's card (D-06), and comes into use earlier only if TD-L2c brought someone in (Step 11). Reading it to anyone is that decision.

> "[MAKER] is making a film about [NAME]'s life as a surprise gift. It will be shown once, at a gathering on [date], to about [N] people: [family and invited friends] / [family, friends and community guests, which means it is a public-facing event, not only a family evening]. A second version, the April version, with the voices of those who choose to join after the premiere, will be given to [NAME]. May I use what you say, your recorded voice, your name, and any photographs or video you lend, in those showings? You can skip any question, stop, and ask me up to [Fri 19 Feb 2027] to take anything out. I will keep the recording private on storage I control [edit to match]. I may use software, including AI tools [that run on my own computer / in a private online workspace: edit to match], to type it up and tidy the sound, but I will not change what you said or make a synthetic copy of your voice. After the gathering I will ask you to sign a short written release if I want to show the film any further, for example online or in a cinema, and I will not do that without your signed yes. Is that all right with you?"

**4b. One-line version for a text or voice message:** "May I use your recorded voice and your photographs in a film for [NAME]'s gathering on [date], shown to about [N] guests, with you able to skip questions, stop, or have anything taken out until [date], and nothing wider without your written yes?"

**4c. Lender note** (for photos, video or letters lent by someone after the premiere, or by someone brought in at TD-L2c): "You lend these items, which you took or own, for use in the film described above. You allow them to be shown at the gathering and in [NAME]'s April version. You may ask me to remove any item until [date]. I will return the originals on [date]. For any further showing I will ask you again in writing." Under only-me nobody is asked before the premiere (`DECISIONS.md` W-46, W-48): keep a lender's copyright items out of the public cut unless Tier B applies, and send the lender note after the premiere.

**4d. Post-premiere written release** (contributor or lender; one page). Fields: name; the film (working title and occasion); what you contributed (voice recording dated, photographs listed, video). Then:
- I agree that the film may be shown: [ ] at further private gatherings; [ ] in a private online link; [ ] at public screenings, including a cinema or festival; [ ] kept in the family archive.
- I understand: no fee is payable. The maker may edit, crop, restyle and restore my contribution, including with AI-assisted restoration, but will not change the meaning of what I said or create a synthetic voice. My name will appear as [full name / first name / no name]. I may withdraw consent for future showings by writing to [contact]; copies already shared privately may remain. The maker will store my material at [place] for [period] and use it only for this film. I own, or have the right to license, what I contributed [or: someone else took it, named here].
- Territory: worldwide. Term: until I withdraw in writing [or: a fixed term of N years]. Governing law: [jurisdiction not yet known].
- Signature and date.

The usual documentary grant is all media, worldwide, in perpetuity [79]. This version trades that for a withdrawal right, so choose before any E&O application (your decision).

**4e. Her release** (offered after the reveal and her turn conversation, Sunday 7 March 2027 after about 14:00, else Monday 8 March; no deadline). In plain language: "This film is about you. Nothing is shown anywhere new without your yes. For each use, tick yes, no, or ask me again: [ ] family gatherings; [ ] a private online link for family; [ ] a public or invited screening you choose; [ ] a cinema or festival; [ ] kept in the family archive. You can ask me to remove or redo any scene (the list from our conversation is attached). You do not have to decide now; you can change your mind later by telling me. No payment passes either way. You keep the right to be named or not."
Fields: her name; the scene list with her choice (kept, changed, removed, or closed until a date); the uses table; signature; date; optional witness. This maps to the consent ledger and her version (about 24 April 2027) [5].

**4f. Parent or guardian addendum (minors).** "I am the parent or guardian of [child's name, age]. I allow [child]'s [photograph / voice / name] to be used as in the release above." Signature, relationship, date [86]. Under 14: guardian present, and one question. 14 to 17: guardian consent and the child's own yes in plain words [5].

**4g. Family-of-the-deceased note** (a short message; keep the reply in the log): "I am making a film about [NAME]. I would like to include a [photograph / recording] of [deceased person]. It would be shown [as a still, no movement, no new voice]. May I? You can say no, or ask me to remove it later." Record the sender, relationship and date.

**4h. Verbal-release script** (if a person will not sign). On the recording, state the purpose, where the film will first be shown (the gathering on [date]), and what further uses are possible. Ask them to say yes in their own words [79]. Do not ask for a signature long after they declined at the time [79].

### T10. Consult question list (one hour, asked as a hypothetical)

Send it before the hour. Do not name her. The list was renumbered once on 2026-10-19 so that no two tracks claim the same numbers (`DECISIONS.md` W-55): 1 to 20 are this playbook's own; 21 to 25 come from the Hindu visual track; 26 to 28 are the devotional-sound track's music questions that no other block covers (its items on the IPRS tariff, s.52 and the 1963 recording term are folded into 28, 30 and 36 to 38); 29 to 40 are the Gujarati sound track's as written; 41 to 43 are the Saurashtra track's. Not legal advice; all of it waits on the premiere country (O-02, TD-7).

1. In [country or state], is a free, non-sponsored tribute-film screening at a hired hall for about [N] guests a "public" performance? Does it matter if guests are invited rather than open to all?
2. Music: for a commercial recording copied into the film, do I need both sync and master permission for this event? Does the venue's performance licence cover any of it? Is there any exemption for non-profit or family events here?
3. Can I rely on a short, live-performed or cover version of a song? Who owns the rights?
4. Photographs: do commissioned wedding and studio photographs belong to the photographer or the client here? What do I do about photographs whose photographer I cannot find?
5. Is there a safe way to use old family photographs in a film for a public event without permission from every photographer? What risk am I taking, and what does a documented decision look like?
6. Likeness and voice: what consent do I need from living people who appear in photographs or recordings, for this event and for later online or cinema showings? Does a recorded verbal yes count?
7. Minors: what do I need for children who appear in photographs? When must a parent sign?
8. The dead: are there post-mortem rights here? Whose consent counts?
9. People who are estranged: do I have any obligation to tell them, or can I leave them out?
10. Data protection: do photographs and voice recordings count as personal data here, and what notice must I give contributors?
11. Surprise: is it lawful to gather contributions under a truthful but incomplete explanation, and what must I tell people before the screening?
12. AI: who owns AI-assisted restorations and reconstructions? What must I disclose, to whom, and when?
13. Fonts: is there any local rule about embedding fonts in video, or about an OFL font in a DCP subtitle track?
14. Withdrawn (D-29). The number is kept so that questions 15 to 43 do not move.
15. If I later hire a cinema, what insurance and paperwork will they or the law require? Is E&O needed for a single screening?
16. Before a cinema, festival or online release, what is the minimum clearance file (log, releases, licences) a lawyer would want?
17. Who is liable if a contributor withdraws after the screening?
18. How should I word the releases here (term, territory, right to edit, withdrawal)?
19. Are there trademark or personality issues in using her name in the title?
20. Is it better to wait for her release before any screening beyond 27 February?
21. India: for a painting commissioned for payment and used in a film, who owns the copyright under s.17(b) and its proviso, and what must a written licence state (territory, term, all media including a phone file and an archive)?
22. In the premiere country, is a faithful museum photograph of a public-domain painting protected, and does a CC0 or PD-Art label clear it?
23. May the credits say "in the manner of" a named regional painting tradition without breaching the Geographical Indications Act or passing off?
24. Does depicting deities in a devotional animated film carry exposure under religious-feelings offences in India (a lead: BNS s.299, formerly IPC 295A, UNVERIFIED) or in the premiere country, and does a symbols-only policy change it?
25. Does an Indian author's moral right (s.57, UNVERIFIED) require credit or restrict cropping, recolouring or redrawing of a licensed painting?
26. Under s.19(9) can a commissioned composer's royalty share for non-cinema-hall uses be bought out?
27. A tune hummed by me that turns out to be a film song: is a short hum in a public film a performance of the work needing a licence?
28. Does the venue's PRO blanket licence (ASCAP, BMI, PRS, SOCAN, APRA, or IPRS in India) cover music inside a film screened there, and does any tariff in the IPRS 2025 index name a film screening?
29. India: a Gujarati garba or bhajan is credited "Traditional" on a label's release, but its film or compilation credits name a composer (for example a 1960 film with a named music director and a track list that says "Traditional (Folk)"). How do I establish who owns the tune and the arrangement, and does an unnamed arrangement carry its own copyright? Which extract (IPRS repertoire, film credits, the original record label) would a lawyer accept?
30. India and abroad: a composer died in 1984; his works run to the end of 2044 (s.22). A 1960 film or gramophone record of one of his songs may be out of term as a recording (ss.26 and 27) while the composition is not. If the premiere is in the US or UK, how do the terms differ for sound recordings and films? Does a re-issue or remaster by a label restart anything?
31. India: a medieval poet's text (Narsinh Mehta, Dayaram, Vallabhacharya) printed in a modern edition with an editor's choices or a transliteration: is the edition a separate work? May a two-line verse card be shown with the maker's own gloss, naming the edition?
32. India, US, UK: Meghani's *Halarda* (published 1928 or 1929; he died 9 Mar 1947) is treated as public domain in India by a volunteer's template. Confirm that, say how to treat the lullabies he collected versus those he wrote, and say how later volumes (1942 and 1947) are treated.
33. India: an orally transmitted folk song with no known author, never "published" in the Act's sense: what term applies (s.23), and does its first fixation in a collection or on a record start a clock? Does a new arrangement create a new work?
34. India: for a cassette-era Gujarati label that is defunct, merged or unreachable, how is the chain of title established? Is there any route (compulsory licence, orphan-work provision) that could apply to a film's use of a recording whose owner cannot be found?
35. India: is a hum of a few seconds of a copyrighted tune (the maker's own voice, as the film's motif) a "performance", a "reproduction" or an "adaptation" needing a licence (see 27)? Is there a de minimis rule, and does a two-line lyric card need its own permission?
36. India: if an intermediary signs a commission letter for me, does s.19(1) ("signed by the assignor") still work, and does s.38A(2) (the performer's written consent) still work? Does a confidentiality clause bind the performer past the premiere?
37. India: a devotional performer sings a Pushtimarg pada as seva. May they assign the performance for a film under s.38A(2) and s.19 while keeping moral rights under s.38B? May the maker credit them as anonymous at their request?
38. India: s.52(1)(za) and a family's own singing at the gathering (a live aarti or bhajan sung by a relative before the film). Does the exception cover the live singing and not the film's soundtrack?
39. India and abroad: an archive item labelled CC BY-NC 4.0 by an uploader (not the rights holder named in the item), in a library that says it was "posted for non-commercial purposes ... for private use". Can I rely on the label? If the rights holder never granted it, who is liable for the screening?
40. Abroad: is a free, invitation-only premiere "non-commercial" under CC BY-NC 4.0 when the room is hired and food is served? Does a later ticketed or festival screening change the answer?
41. Does tracing or redrawing a CC BY-SA 3.0 or GFDL photograph carry a share-alike duty into the film?
42. Does a swastika form in a floor drawing carry any exposure in the premiere country (TD-7)?
43. Does restating dated panchang facts from a site that claims copyright in "All Images and data" need any permission?

### T11. Pack list for 26 February 2027

- [ ] Two USB sticks with the film files (venue file, backup file, audio-only fallback, PH1).
- [ ] Two laptops, the same file at the same path.
- [ ] HDMI cable and a spare. Adapter kit. Chargers. USB-C hub.
- [ ] Printed running order and the failure ladder.
- [ ] The test clip on a stick.
- [ ] The cable and adapter for her phone class, tested on a project phone and the spare laptop (W-52).

## Decisions you'll need to make

Each decision lists the options and our current lean. Leans are not final until you write them on the settings card.

| ID | Decision | Options | Our current lean | What would change it |
|---|---|---|---|---|
| TD-1 | Working size | 1920x1080 (16:9); 2K DCI; UHD | Stay at 1920x1080. Derive the 2K Flat DCP from it. Prepare stills at 3840 px or more. UHD only for single hero shots, and only if a booked 4K cinema justifies it, decided before Sunday 3 January 2027 [3][15] | A booked 4K cinema and a chapter that needs more detail |
| TD-2 | Frame rate | 24 fps; 25 fps | 24 fps everywhere [16] | A 50 Hz-only venue whose test clip judders. Then make a 25 fps access copy with `fps=25`, not a speed change (untested) |
| TD-3 | Captions | Burned-in open captions; soft subtitles | Burned-in open captions (7 to 8% line height for the venue file). Sidecar SRT and VTT. A DCP subtitle track only for a later cinema, with an OFL font [20] | A venue that asks for soft subtitles |
| TD-4 | DCP container and standard | Flat 1998x1080; Scope. SMPTE; Interop | Flat, SMPTE, unencrypted, 24 fps [15][27] | A cinema that demands Interop or Scope; a venue that is a cinema with a DCP server (Step 9 branch) |
| TD-5 | Door policy for 27 February | Invite-only; open to all | Lean invite-only (`DECISIONS.md` W-54), decided by Sun 15 Nov because headcount and the share of strangers drive the cold open and the HOLD/PRIVATE rule. Invite-only keeps festival premiere status, under Sundance's rule [88]. Open to all raises the music, photo and likeness exposure [56] | Your wishes for the room |
| TD-6 | Who runs playback on the day | Venue AV operator told a truthful minimum; a hired tech; you | The venue operator runs playback, told a truthful minimum (a test clip, an empty room); you hold the master fader (`DECISIONS.md` W-54, D-07). A hired tech would be a person brought in [5] | You bring someone in, which changes "only me"; or the venue is a cinema with a DCP server (Step 9 branch) |
| TD-7 | Country and state of the premiere | Any | Needed before the consult. It also decides the music, photo and likeness answers [56] | None. It must be answered |
| TD-8 | Rights consult | Pay for one hour; skip | One paid hour by Friday 4 December 2026, asked as a hypothetical (T10, questions 1 to 43) | Budget or privacy preferences |
| TD-9 | Phone deliverable and sharing | PH1 by cable on reveal weekend; the tablet or stick route; nothing | PH1 by cable to her on reveal weekend with her yes and the K1 backup question answered first; PH2 to relatives as a WhatsApp document only after the ledger closes and the maker says yes (`DECISIONS.md` W-73, W-74) | Her backup state, her free storage (O-54), her yes |

### Other decisions

- **Register status of TD-1 to TD-9.** TD-9 phone deliverable and sharing W-74 (the keepsake route W-73, decided at G-SLICE, O-30). TD-1 size W-15 and TD-2 frame rate W-14 (24 fps settled); TD-3 captions W-18; TD-4 DCP W-17 (the venue's written answer, due Sun 15 Nov, decides file or DCP); TD-5 and TD-6 W-54 (decide by Sun 15 Nov); TD-7 country is pending from the maker (O-02, by Sun 25 Oct); TD-8 consult W-55 (by Fri 4 Dec, once the country is known). Loudness is W-19, and the settings card is signed Sun 1 Nov (W-16). All in `DECISIONS.md`.
- **Who is in on it, and who approves the hard chapters (decided).** Only the maker (`DECISIONS.md` D-03), who is her proxy for hard chapters under one-key-three-guards (D-04). The compensating controls are the Fable advisor's written flag on every Tier C item and every accepted risk, a written reason and an undo note for every accepted risk, at least 48 hours between drafting and deciding (W-46), and the paid consult (W-55). A second approver or a day-of tech would change "only me", so note that decision when it is made. The one re-open point is Sunday 3 January 2027 (TD-L2c); until then, and by default after it, only-me mode holds (Step 11).
- **Whether a cinema screening is wanted at all.** The research gives no lean. Our reading is this: the DCP is worth making before the premiere only if Exercise 3 passes. If it does not, make the DCP after the premiere. Encode on the PC, not the cloud [47].
- **Release term.** The usual documentary grant is all media, worldwide, in perpetuity [79]. Form 4d allows withdrawal for future showings. The research gives no lean. Decide before any E&O application.
- **Insurance.** Distributors and exhibitors generally require E&O [77][78]. Whether a one-off hire needs E&O or public-liability cover is **TODO(research)**. Ask the cinema (T6, question 5).

### Still unknown (TODO(research) items to close)

- The 2K versus 4K share of cinema screens (the search budget ran out).
- DCI specification text; SMPTE RP 200 reference calibration (85 dB SPL, -20 dBFS pink noise) and typical DCP dialogue levels. These are background knowledge only, not checked.
- Which gamma each DCP-o-matic colour preset applies; whether ProRes reads cleanly; DCP-o-matic's encode speed and memory use on Windows; the Windows path for a 24 Hz refresh rate; the ISDCF name when only L and R are mapped.
- TV, projector and LED-wall USB and format support at the real venue (exFAT, MKV, soft subtitles; HEVC on Windows and TV players).
- Cinema hire prices and terms (none listed on the pages reviewed); 2026 E&O premiums (only the 2012 and 2017 US figures were found); public-liability rules for a one-off hire; festival specifications other than Sundance.
- Venue-licence coverage from ASCAP, BMI, PRS, PPL and IPRS; the US sound-recording performance right; UK image rights; India's DPDP Act and personality-rights detail; minors and post-mortem rules outside the US and Germany; US orphan-works status in 2026.
- Whether the EU AI Omnibus changed the Article 50 timeline; whether a private person is an AI Act "deployer"; EU and India treatment of AI output.
- Whether the India Copyright Act s.17(b) text read in the research is current (a government-hosted consolidated copy of unknown date).
- Archive pricing (British Pathe and Getty; not found); consult and music-licence fees.
- What family-film makers actually do about clearances. No survey was found. The risk ladder in this guide is a synthesis.
### Scheduled tests

- **Venue, TD-L2b (by Sun 17 Jan 2027):** Trim V and the venue caption size, judged on the venue screen with the test clip.
- **Cinema, first real-cinema slot:** Trim C and the cinema caption size (5.5 to 6%).

## Record of deltas to other playbooks

The changes the other playbooks needed, by file and decision (research Deliverable 6 with the round-2 corrections), kept as a record of what changed and why. Status as of 2026-10-18 (Fable advisor): *applied* rows are done in the target file; the four *outstanding* rows are tracked in `DECISIONS.md` S-40 and `ROADMAP.md` Section 14 item 1 and are patched by Haiku before Fri 30 Oct. Quoted old values below were rewritten so this table itself carries no superseded value. The 2026-10-19 merge retired the games row and updated the two `format.md` rows.

| File | Where (section or decision) | Change | Status |
|---|---|---|---|
| `surprise-ops.md` | Consent card | Replace with version 2 (T9, 4a): the true audience and use, and a later written release. Add the only-me box: until the maker decides to bring someone in, the card is not read to anyone (Step 11; TD-L2c) | applied |
| `surprise-ops.md` | Decision 6 (rings and keys) | Rewritten for only-me (D-03, D-04): the maker is the sole proxy for hard chapters; one-key-three-guards; compensating controls (research Finding 11; "Other decisions" above) | applied |
| `surprise-ops.md` | Key dates, the 19 Feb row | Split the 19 Feb row into "Sat 6 Feb 2027, Picture lock (G-LOCK, production-scale)" and "Fri 19 Feb 2027, Withdrawals close (removals only after lock)" (W-08, S-03) | applied |
| `surprise-ops.md` | Key dates, new lines | Add "Sun 3 Jan 2027, TD-L2c: decide whether anyone is brought in" and "Sun 17 Jan 2027, TD-L2b: venue visit with the test clip only"; add TD-L6, TD-L7 and TD-L9 to TD-L16 from the T4 table | applied |
| `surprise-ops.md` | Decision 12 (reveal format and room) | The charter now says "mostly public"; the run sheet and tiers follow TD-5 | applied |
| `surprise-ops.md` | Reveal-day run sheet, S minus 2 h | Add the test clip first, a settings snapshot, and a backup-stick and second-laptop check (T4, TD-L13) | applied |
| `surprise-ops.md` | After the reveal | Add the post-premiere release step (TD-L15) and the T3 and T4 gate (TD-L16) | applied |
| `toolchain.md` | Step 10 (sound), the `loudnorm` example | True peak -1 dBTP everywhere in the `loudnorm` example and the text (`DECISIONS.md` W-19, S-28; the older example value was illustrative). Venue: three masters (-23, -18, -16 LUFS) chosen at the 22 Feb run; online -16 LUFS; cinema mixes are not normalised; a broadcast -23 LUFS target is not a cinema target [30][36] | applied |
| `toolchain.md` | Step 11 (captions) | Windows fonts are fine rasterised in video, not embedded in a DCP track; prefer OFL fonts [75][76] | applied |
| `toolchain.md` | Step 12 (export set) | Add the venue test clip, the two trims, a mono-fold check and a DCP column | applied |
| `toolchain.md` | Step 13 (checks) | Add `color_range` and `color_space` checks, and loudness plus mono-fold | **outstanding** (Haiku, before Fri 30 Oct) |
| `toolchain.md` | Step 14 (rehearsal) | Rehearse with the neutral test clip first; walk the ladder rungs; take settings screenshots | applied |
| `toolchain.md` | Decision 7 | Decision 7 now reads: 2K Flat DCP derived from the 1080p master; 4K not needed, UHD only for single hero shots if a 4K cinema is booked (W-15, S-32) | applied |
| `toolchain.md` | Decision 8 | Burned-in captions confirmed as the default; DCP subtitle tracks later, with OFL fonts | applied |
| `toolchain.md` | Decision 9 | Add the venue-survey questions (T5) | applied |
| `agent-pipeline.md` | Step 1 and the project settings card | Lock 24 fps (TD-2). Colour reads "Rec.709 / BT.1886 display target (gamma about 2.4) for video, sRGB for stills". Add "stills prepared at 3840 px or more on the long edge; 2K Flat DCP derived, never re-authored" | applied |
| `agent-pipeline.md` | Gate G6 | Add the mono-fold check, trims applied, caption safe area, the test clip played on the venue screen, and DCP Verify if a DCP is made; add G6b (venue rehearsal) | **outstanding** (Haiku, before Fri 30 Oct) |
| `format.md` | Step 8 and Exercise 1 | Keep 7 to 8% line height for the venue file; add the cinema 5.5 to 6% note | applied |
| `format.md` | Step 15 | "Send the file to the venue a day before" conflicts with the surprise: send only the test clip; bring the film on the day | applied |
| `format.md` | Decision 3 (venue) | Add the survey questions (T5) | applied |
| `format.md` | Decision 8 (hosting table) and Decision 12 (music) | Before any online link: the T3 gate (releases signed, explicit yes) [4]. Decision 12: add the exhibition layer (sync, master and performance); a public gathering is not a family circle | applied |
| `format.md` | Decision 9 (game content) | Closed as "none" under D-29 (O-05 answered); the 2026-10-18 re-read stays in `research/theatrical-delivery.md` as a historical record | applied 2026-10-19 |
| `format.md` | Decision 13 (languages) | Defaulted in `DECISIONS.md` W-57 and W-75 (cards in Gujarati; captions in the room's language; decide by Sun 1 Nov) | applied 2026-10-19 |
| `ai-imagery.md` | Decisions 3 and 5; end-credit cue sheet | "Public or ticketed" now applies to 27 Feb. Add the six cue-sheet extensions (research Finding 10): (1) a pre-roll line before the title; (2) tool name, version and date for each L2-or-higher item, with the tool's terms; (3) a human-contribution note per item; (4) a deepfake marker on photoreal motion of a real person (L4b and L4c); (5) a no-synthetic-voice line; (6) a metadata-stripping note: stream copy, re-encodes and platforms can strip metadata, so the credits and manifest are the record | **outstanding** (Haiku, before Fri 30 Oct) |
| `games.md` | Q7 and F4 | Retired with the game-terms material (D-29; S-45): nothing to add | retired 2026-10-19 |
| `CHARTER.md` | Open decisions | Add: door policy (TD-5), jurisdiction (TD-7), who runs playback (TD-6) | applied |

## Pitfalls

1. **Treating the rules as universal.** Fair use is US law. Fair dealing is UK and Indian law. Personality and post-mortem rights vary by country and US state. Every legal statement here needs its jurisdiction and "not legal advice" until TD-7 is answered [56][61][70][71].
2. **Using the old consent card.** It says "a film that family will watch together" and "private" [5]. Use version 2 (T9, 4a) before any recording; under only-me none is planned before the premiere (`DECISIONS.md` D-05).
3. **Calling a free public premiere a family showing.** US law reaches beyond a family circle [56]. Sundance treats free public screenings as public exhibition [88]. Use the door policy (TD-5) and the tiers.
4. **Loudness confusion.** A broadcast -23 LUFS target applied to a cinema mix is wrong [36]. A quiet cinema mix posted online will play quietly [38]. The venue PA is unknown until tested [5].
5. **Colour drift** between a consumer monitor, the venue and a cinema. Use one grade and two trims, test on the real screen, and turn HDR off [42].
6. **DCP ingest failures.** The common ones are the wrong drive format, a corrupt copy, subtitle or standard faults, KDM trouble, and a capability mismatch. The ranking is a judgement, not statistics (**TODO(research)**) [18][19][26].
7. **Writing a DCP drive and then using it on a consumer computer.** The consumer system may reformat or damage it [26]. Label it, never plug it into the Windows PC after writing, and keep a copy of the folder elsewhere.
8. **The surprise leaks through technical channels.** Look at DCP and file titles, metadata, thumbnails, "Recent" lists, staff who watch the film, and cloud copies. Use a neutral code name, strip metadata, use the neutral test clip for staff, and play the film only in an empty room [5].
9. **Calling art or a font "devotional" or "traditional" and treating it as free.** A museum photograph of a public-domain painting may be protected where you show it; an uploader's licence field is a claim; every font needs its `OFL.txt` hash. Keep a `tradition_origin` note and a rights row for every `artwork`, `deity_image`, `commissioned_art` and `font` (`DECISIONS.md` W-21, W-46, W-79).
10. **Over-trusting fair use for family photographs.** "Still photographs in particular do not lend themselves to fair use treatment" [80]. Ask, substitute, or document a Tier B decision, and use the consult.
11. **Accepted risks decided by one person.** With no second key, mistakes go unchallenged. Use the advisor flag, written reasons, the 48-hour gap, and reversible choices first.
12. **AI disclosure and ownership gaps.** Free tool tiers may exclude commercial or public use. Re-encoding and platforms can strip metadata, and photoreal motion of a real person can read as a deepfake [6][65]. Keep the tool terms in the ledger and add the pre-roll line.
13. **Personal data in the rights log.** Names, consents and addresses stay in the private repo. Encrypt the archive copy. Upload nothing to a third party without your explicit yes [1].
14. **Misleading edits.** A film can mislead even when each clip is true [85]. Show no invented events as fact. Label reconstructions (L5) [6].
15. **Caption and sound accessibility.** Older audiences need readable captions and clear dialogue [4][5]. Test them from the back row with the oldest listener.
16. **Disk and compute limits in the cloud container.** The root disk was full during testing [47]. Encode the DCP on the PC, and use the container for measurement and checks.
17. **Relying on the DCP Player at the venue.** The manual warns against depending on it [17]. The venue gets the MP4. The DCP is for a cinema.
18. **Dignity for people who cannot be asked.** Apply the Tier C and D rules. Ask the closest family about the dead. The estranged default to out [5].
19. **Burned-in captions do not satisfy a festival-style delivery.** A Sundance-style DCP needs both a Closed Caption and an Open Caption version (FAQ 31, document dated 2026-09-08; "subject to change") [88]. Check the festival's current rules before any submission.

## Best references

These eight are the best use of your reading time. Each link is one that the research notes cite. The Sources section gives the dates and what was read.

1. **DCP-o-matic manual, DCP settings chapter** [15]. https://dcpomatic.com/manual/html/ch07.html. Why: the settings you will click, with the 2K advice, bit rate, container and standard explained.
2. **DCP-o-matic colour paper, "Colour conversions for DCP creation"** [22]. https://dcpomatic.com/manual/colour.pdf. Why: the colour maths in plain steps (Exercise 1).
3. **ISDCF Doc 3, DCP Delivery Recommendations** [26]. https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf. Why: the drive format rules and the warning about consumer computers.
4. **ISDCF Doc 11, "How Loud is a Movie?"** [30]. https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf. Why: why a cinema mix is set by the room and not by a loudness number.
5. **DCP-o-matic manual, verifying DCPs** [18]. https://dcpomatic.com/manual/html/ch19.html. Why: what each Verify error and warning means before you ship.
6. **IDA, "A Practical Discussion of Appearance Releases"** [79]. https://www.documentary.org/column/practical-discussion-appearance-releases. Why: what a release must say, and the verbal fallback.
7. **Sundance Film Festival 2027 submissions FAQ** [88]. https://www.sundance.org/submissions-faq. Why: a real festival's delivery and premiere rules, including the free-screening trap.
8. **SIL Open Font License FAQ** [75]. https://openfontlicense.org/ofl-faq/. Why: video titling is a listed permitted use, and what an OFL family needs in the rights log (T8).

## Sources

Entries [48], [49] and [51] (a game publisher's usage guidelines, its EULA and a platform's content rules) are retired with the game-content material (`DECISIONS.md` D-29, S-48); they stay in `research/theatrical-delivery.md`, where those numbers still resolve.

[1] Project Charter — CHARTER.md — 2026-10-18 — facts, principles, open decisions.

[2] toolchain playbook — playbooks/toolchain.md — 2026-10-18 — Steps 10 to 15, Decisions 6 to 9.

[3] agent-pipeline playbook — playbooks/agent-pipeline.md — 2026-10-18 — settings card, gate G6, pitfall 6.

[4] format playbook — playbooks/format.md — 2026-10-18 — caption rules, hosting table, Decisions 3, 8, 9, 12, 13.

[5] surprise-ops playbook — playbooks/surprise-ops.md — 2026-10-18 — key dates, consent card, pretext cards, run sheet, Decisions 6 and 12.

[6] ai-imagery playbook — playbooks/ai-imagery.md — 2026-10-18 — L0 to L5 ladder, cue sheet, decisions.

[8] DCP-o-matic download — https://dcpomatic.com/download — 2026-10-18 — stable 2.18.51, 16 October 2026; Windows, macOS, Linux.

[10] Manual, Licence — https://dcpomatic.com/manual/html/ch01s03.html — 2026-10-18 — "free and open-source and is licensed under the GNU GPL".

[11] Manual, creating a DCP — https://dcpomatic.com/manual/html/ch03.html and https://dcpomatic.com/manual/html/ch03s03.html — 2026-10-18 — new film, disk space (100 GB for features), make DCP; encoding can take many hours.

[12] Manual, video content — https://dcpomatic.com/manual/html/ch06s04.html — 2026-10-18 — colour presets, range, scale and container.

[13] Manual, audio content — https://dcpomatic.com/manual/html/ch06s05.html — 2026-10-18 — audio map, gain, delay.

[14] Manual, timed text — https://dcpomatic.com/manual/html/ch06s06.html — 2026-10-18 — SRT/SSA/DCP XML, burn-in, open versus closed.

[15] Manual, DCP settings — https://dcpomatic.com/manual/html/ch07.html — 2026-10-18 — container, 2K advice, bandwidth 50 to 250 Mbit/s, standard, reels, FAT32 note.

[16] Manual, frame rates — https://dcpomatic.com/manual/html/ch12.html — 2026-10-18 — 24 fps and 48 kHz safe; 25 fps slowdown.

[17] Manual, playing DCPs — https://dcpomatic.com/manual/html/ch18.html — 2026-10-18 — Player limits and warnings.

[18] Manual, verifying DCPs — https://dcpomatic.com/manual/html/ch19.html, https://dcpomatic.com/manual/html/ch19s03.html, https://dcpomatic.com/manual/html/ch19s04.html — 2026-10-18 — errors, warnings, passes.

[19] Manual, writing DCPs to disks and encryption — https://dcpomatic.com/manual/html/ch20.html and https://dcpomatic.com/manual/html/ch10s04.html — 2026-10-18 — ext2, Disk Writer; "Should I encrypt?".

[20] Manual, common tasks — https://dcpomatic.com/manual/html/ch17.html — 2026-10-18 — VF DCP, subtitle options.

[21] Manual, encoding servers, threads, generated files, command line — https://dcpomatic.com/manual/html/ch13.html, ch11s03.html, ch14.html, ch15.html — 2026-10-18 — parallel encoding, resume, `dcpomatic2_create` options.

[22] Hetherington and Couzin, "Colour conversions for DCP creation" — https://dcpomatic.com/manual/colour.pdf — 2026-10-18 — linearise, matrix to XYZ, Bradford, 48/52.37, gamma 1/2.6 (text extracted from PDF).

[25] ISDCF naming convention intro and document index — https://www.isdcf.com/registry/dcncintro/ and https://www.isdcf.com/resources/documents/ — 2026-10-18 — underscores, 40-character display note, document list.

[26] ISDCF Doc 3, DCP Delivery Recommendations — https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf — 2017-06-29 — MBR, 0x83, ext2/ext3, 128-byte inode, USB 2.0, consumer-OS warning.

[27] ISDCF Doc 2, DCP Transition Review — https://files.isdcf.com/papers/ISDCF-Doc2-DCP-TransitionReview.pdf — 2011-11-02 — Interop versus SMPTE tables.

[28] ISDCF Doc 4, audio channel packaging — https://files.isdcf.com/papers/ISDCF-Doc4-Audio-channel-recommendations.pdf — 2017-06-29 — channel order, even channel count.

[30] ISDCF Doc 11, "How Loud is a Movie?" (Ioan Allen, SMPTE) — https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf — 2016-03-15 — calibrated rooms, fader 7, TASA 85 dB Leq(m), no feature limits.

[31] Wikipedia, Digital Cinema Package — https://en.wikipedia.org/wiki/Digital_Cinema_Package — 2026-10-18 — secondary: containers, bit rate, audio, Interop versus SMPTE, ext2/ext3.

[34] Wikipedia, Rec. 709 — https://en.wikipedia.org/wiki/Rec._709 — 2026-10-18 — secondary: OETF, limited range codes, no display EOTF.

[35] ITU-R BT.1886 (2011) — https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1886-0-201103-I!!PDF-E.pdf — March 2011 — reference EOTF, gamma 2.404.

[36] EBU R 128 (v5, November 2023) — https://tech.ebu.ch/docs/r/r128.pdf — 2023-11 — -23.0 LUFS, tolerances, -1 dBTP.

[37] EBU R 95 v1.1 (June 2017) — https://tech.ebu.ch/docs/r/r095.pdf — 2017-06 — action safe 3.5%, graphics safe 5%.

[38] Wikipedia, Loudness war — https://en.wikipedia.org/wiki/Loudness_war — 2026-10-18 — secondary: streaming targets (YouTube -14 LUFS, Apple Music -16).

[39] Wikipedia, Frame rate — https://en.wikipedia.org/wiki/Frame_rate — 2026-10-18 — secondary: 24 fps cinema, judder.

[40] Wikipedia, Motion interpolation — https://en.wikipedia.org/wiki/Motion_interpolation — 2026-10-18 — secondary: soap opera effect, 120 Hz.

[41] mpv manual — https://mpv.io/manual/stable/ — 2026-10-18 — `--video-sync`, `--hwdec`, constant frame rate.

[42] Microsoft Support, HDR settings in Windows — https://support.microsoft.com/en-us/windows/hdr-settings-in-windows-2d767185-38ec-7fdc-6f97-bbc6c5ef24e6 — 2026-10-18 — SDR looks off with HDR on; HDR off on battery.

[43] Wikipedia, exFAT — https://en.wikipedia.org/wiki/ExFAT — 2026-10-18 — secondary: TV support not universal.

[44] Wikipedia, File Allocation Table — https://en.wikipedia.org/wiki/File_Allocation_Table — 2026-10-18 — secondary: FAT32 4 GiB minus 1 byte.

[45] Wikipedia, Overscan — https://en.wikipedia.org/wiki/Overscan — 2026-10-18 — secondary: LCD TVs often ship with overscan on.

[47] Own measurements in the cloud container — 2026-10-18 — ffmpeg 6.1.1, `libopenjpeg`, 4-vCPU Intel Xeon at 2.1 GHz, 16 GB RAM; disk 100% full; `ebur128` and `pan` syntax run; JPEG2000 timings in Finding 4.




[53] US Copyright Office, AI Part 2: Copyrightability — https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — January 2025 — conclusions, prompts, disclosure on registration.

[54] US Copyright Office, Orphan Works and Mass Digitization — https://www.copyright.gov/orphan/reports/orphan-works2015.pdf — June 2015 — "legal cloud"; limitation-on-remedies proposal.

[56] 17 U.S.C. 101 — https://www.law.cornell.edu/uscode/text/17/101 — 2026-10-18 — definition of "publicly" (family and social acquaintances).

[61] UK Government, Exceptions to copyright — https://www.gov.uk/guidance/exceptions-to-copyright — 2026-10-18 — criticism, review, quotation; fair dealing test.

[62] UK IPO, Orphan works licensing — https://www.gov.uk/guidance/copyright-orphan-works — 2026-10-18 — fees, 7-year licence, UK only.

[65] EU AI Act, Article 50 — https://artificialintelligenceact.eu/article/50/ — 2026-10-18 — marking, deepfake disclosure, artistic works.

[70] Copyright Act, 1957 (India), consolidated copy — https://copyright.gov.in/Documents/Copyright_Act_1957.pdf — 2026-10-18; date of consolidation not shown — ss.2(d), 17, 31A, 52.

[71] Wikipedia, Personality rights — https://en.wikipedia.org/wiki/Personality_rights — 2026-10-18 — secondary: US state law, post-mortem terms, Germany, France, India cases.

[75] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — 2026-10-18 — output not restricted; video titling; embedding.

[76] Microsoft, Font redistribution FAQ — https://learn.microsoft.com/en-us/typography/fonts/font-faq — page dated 2024-11-19 — video captions as bitmaps allowed; no embedding or conversion.

[77] IDA, "Errors & Omissions: ... Guide to Protecting Your Film" (Winnie Wong) — https://www.documentary.org/feature/errors-omissions-rights-oh-my-guide-protecting-your-film — 2012-04-06 — E&O requirements, $1M/$3M, $10,000 deductible.

[78] IDA, "To Err (or Omit) Is Human - Thankfully, There's E&O" (Beer, Levy, Rosini) — https://www.documentary.org/column/err-or-omit-human-thankfully-theres-eo — 2017-09-28 — "$2,500 or more"; requirements; three-year term.

[79] IDA, "A Practical Discussion of Appearance Releases" — https://www.documentary.org/column/practical-discussion-appearance-releases — undated — release contents, verbal fallback, area releases.

[80] IDA, "Caveats for Using Amateur Footage" — https://www.documentary.org/column/caveats-using-amateur-footage-plus-considering-incentives-overseas-productions — undated — creator owns; stills and fair use.

[82] IDA, "All Clear? A Basic Primer on Music Clearance" (David G. Powell) — https://www.documentary.org/feature/all-clear-basic-primer-music-clearance — 2003 — sync, master, festival versus all-media licences.

[85] IDA, "Beyond Vetting: Common Legal Issues for Documentary Filmmakers" (Katie Townsend) — https://www.documentary.org/column/beyond-vetting-common-legal-issues-documentary-filmmakers — 2020-06-11 — misleading edits; consent laws.

[86] Wikipedia, Model release — https://en.wikipedia.org/wiki/Model_release — 2026-10-18 — secondary: minors need parent or guardian signature.

[88] Sundance Film Festival 2027 submissions FAQ — https://www.sundance.org/submissions-faq — document created 2026-09-08 — premiere definition (FAQ 8), AI (12), temp music (13), clearance (14), screener format (18), DCP delivery (31).

[89] Picturehouse Cinemas, Venue hire — https://www.picturehouses.com/venue-hire — footer 2026; fetched 2026-10-18 — screen hire packages, one-hour tech rehearsal; no prices.

[90] Everyman Cinema, Private hire — https://ww2.everymancinema.com/private-hire — fetched 2026-10-18 — your own content; no prices.

[91] Cinemark, Private events — https://www.cinemark.com/private-events — footer 2026; fetched 2026-10-18 — private screening for filmmakers; no prices.

## Changelog

- **v1, 2026-10-18.** First draft from `research/theatrical-delivery.md` (researcher's notes, 2026-10-18), by a Haiku scribe. Sources are copied from the notes with their original numbers. Open items are tagged TODO(research). Conflicts are flagged in Step 5 and T1 (venue loudness ceiling). Nothing here is legal advice.
- **v2, 2026-10-18 (Fable round 1 applied).** Added the only-me box (Step 11, T9 4a, TD-L2c); the verified ffprobe command, with lut3d and metadata stripping marked as run in the container; TD-L2b venue visit by 17 Jan 2027; the DCP-server branch (Step 9); the UK IPO fee wording (£24 step flagged TODO); the ext2 and partition rules; the Sundance Closed and Open Caption note; -1 dBTP settled; the advisor-flag mechanism (rights/flags); Flat citation in T2 now [12][22][31].
- **v3, 2026-10-18 (Fable round 2 applied).** Picture lock corrected: TD-L7 is now labelled as the withdrawals-close date (Fri 19 Feb 2027), and picture lock is Sat 6 Feb 2027 (G-LOCK, production-scale); UK IPO fee scale written once in full (the £24 TODO closed against gov.uk, read 2026-10-18); venue caption size confirmed at TD-L2b, with trims and the cinema caption size moved to Scheduled tests; T4 run sheet ordered by date; "Record of deltas to other playbooks" section added; SKILL step 22 example updated.
- **2026-10-18, Reconciled with DECISIONS.md (2026-10-18).** Sonnet implementor pass against the decisions register: venue loudness start replaced by the three-master choice (-23, -18, -16 LUFS, all -1 dBTP) at the 22 Feb run (W-19; S-28); venue asked by Fri 6 Nov, written answer due Sun 15 Nov decides file or DCP (W-17); only-me and the April version replace private-cut and contributor-confirmation wording (D-03 to D-06, W-48; S-09, S-10); Tier B is documented risk ratified after, nobody asked before the premiere (W-46); no cloud copy, second encrypted SSD (W-25); venue operator runs playback and the maker holds the fader (W-54); AMB re-render on 23 Feb (W-20); register status of TD-1 to TD-8 added; languages defaulted (W-57).
- **2026-10-19, Reconciled with DECISIONS.md after the her-world merge (2026-10-19).** Sonnet implementor pass against the merged register (S-48, S-64 and the phone, font and caption rows of W-16, W-18, W-21): game-content material retired under D-29 (T2 rights gate, T8 GM-002 kept as "n/a, none used", TD-L6 and TD-L12 terms checks, T10 question 14 withdrawn, sources [48], [49], [51], pitfalls 3 and 9, best reference 8); T10 renumbered once, 1 to 43 (W-55); T8 gains the `artwork`, `deity_image` and `commissioned_art` types and the `tradition_origin`, `phone_share`, `composition_status` and `recording_status` columns (W-46); the phone files PH1 and PH2, Trim P and TD-9 added (T1, T2b, T4 TD-L17 and TD-L18, W-63, W-64, W-74); Step 6 carries the Gujarati caption sizing, the OFL font families and the `ass` burn-in path before ffmpeg n9.0 (W-18, W-21, W-75); the venue test clip carries a tone ladder and the TD-L2b visit writes down the lowest tone the room carries (W-17, W-65); the her-turn conversation is Sun 7 Mar after about 14:00, else Mon 8 Mar (W-48); the backup ladder and pack list carry PH1 by cable (W-52). Citations kept; no research note or review touched.
- **2026-10-20, Stale-wording sweep (2026-10-20).** Sonnet implementor pass against the register and `scripts/stale_check.py`: the phone figures follow W-63 and W-18, a 3.5 Mb/s cap on PH2 (Step 7, the T1 settings card and the T2b table) and at most 32 characters a phone caption line (Step 6 and the T2b table); the TD-L6 row names the contributor clip confirmation without quoting the retired line (S-09); the 4b one-line message reads "your recorded voice and your photographs" so it cannot be mistaken for the retired fallback name (S-13). That 4b rewrite answered a WARN-only pattern (S-13.voice-and-photos-warn, "only meaningful as the old F-0 name") and was a clarity choice: the register retires that three-word phrase (written hyphenated here so the checker does not read it as the old name) only as the name of the F-0 fallback, not in every context. Citations kept.
