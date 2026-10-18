# Theatre-grade masters, venue playback and rights clearance

> A plain-language guide for the maker, who works on a Windows PC and is learning by doing. Track: `theatrical-delivery`. Built from `research/theatrical-delivery.md` (research date 2026-10-18). Nothing here is legal advice. Items marked **TODO(research)** are open and must not be treated as facts.

## Why this matters for our film

On Saturday 27 February 2027, the film will play on a screen and a sound system we do not control. It may be a venue TV, a projector, an LED wall, a laptop or a USB stick. Each one has its own quirks, and the audience will judge the film by what it sees and hears.

The charter asks for a film that could be shown in a theatre. That means one master built to a cinema standard, a few simple files made from it, each one tested on the real screen, and a written record of every right we rely on.

"Mostly public" changes the rights picture. A gathering open to guests beyond the family is a public showing in many places. Music, photos taken by other people and people's voices may then need permission, even if nobody pays. The jurisdiction is not yet known (TD-7), so treat every legal point here as "confirm first".

The surprise also lives in the files. File names, titles, metadata, thumbnails, test clips and the Windows "Recent" list can all give it away.

## Core principles

1. **One master, many derived files.** Everything comes from one 1920x1080, 24 fps ProRes master. Never re-author a shot for one deliverable.
2. **Judge on the real screen.** Your monitor is not the reference. Colour, brightness and captions are judged on the screen the audience will see, from the back row.
3. **Plan the failure before it happens.** Assume a cable, a laptop or the TV's file support will fail. Keep a ladder of fallbacks and walk it in rehearsal.
4. **Keep 24 fps.** It is the one frame rate DCP-o-matic calls safe for unknown places [16]. Do not speed up or slow down footage to suit a player.
5. **Cinema sound is not loudness-normalised.** Make three outputs from one mix: cinema, venue and online. A broadcast loudness target is not a cinema target [30][36].
6. **Burn the captions in.** Burned-in captions show on every screen. Soft subtitles depend on the device [20].
7. **Decide who sees it before you clear rights.** Set the door policy first (TD-5). Every asset gets a row in the rights log: cleared, substituted, or a documented risk with reasons and a way to undo it.
8. **Keep the surprise inside the files.** Neutral names, no title metadata, a neutral test clip for staff, and the film played only when the room is empty.

## How to do it, step by step

Work through these in order. Each step ends with a check you can run.

### Step 1. Lock the settings by Sunday 1 November 2026

Make decisions TD-1 to TD-4 (see Decisions) and write them on the settings card (Templates, T1). Save the card in the private repo.

Check: the card exists, is dated and is saved.

### Step 2. Install the tools on the Windows PC

- **DCP-o-matic 2.18.51**, released 16 October 2026. It is free and GPL-licensed, with Windows 64-bit and 32-bit builds [8][10].
- **ffmpeg and ffprobe.** The agent pipeline names the PC build Gyan 9.0.2 [3].
- **mpv or VLC** for playback. mpv does not turn on hardware decoding by default [41].
- **PowerShell's built-in `Get-FileHash`** for SHA-256 hashes [4].

Check: each tool opens and reports its version. How much memory DCP-o-matic uses on Windows is **TODO(research)**. Watch it in Task Manager during Exercise 3.

### Step 3. Prepare the master

- Format: ProRes 422 HQ `.mov`, 1920x1080, 24p, Rec.709, limited range, 10-bit 4:2:2, PCM 24-bit 48 kHz [3].
- Scans and stills: prepare them at 3840 px on the long edge or larger, so camera moves crop into real detail [3].
- Frame: 16:9 sits inside a 1.85 Flat container. A Scope crop would cut about 26% of the picture height and damage titles and photo moves [31].
- Check: ffprobe reports the size, frame rate, pixel format and colour tags you set. The frame count and duration match the timeline.

### Step 4. Grade once, then check on the screen

- Grade to Rec.709 / BT.1886 at a mid-key look. Rec.709 uses limited-range code values, 64 to 940 for luma on 10-bit [34].
- Working limits (a proposal, not a sourced rule): keep shadows above about code 20 to 24 on 8-bit limited range, keep whites at or below 235 (940 on 10-bit), and check skin tones against a known family photo.
- Make two small trims. They are lookup files applied only when exporting. The master is never touched.
  - **Trim V, for a lit venue:** a starting lift of about 2 to 4 IRE in the shadows and a mid-gamma rise of about 0.05 to 0.10. These are starting values only.
  - **Trim C, for a dark cinema:** identity (no change) until a real cinema test.
- Hash and log every trim file. The method is ffmpeg's `lut3d` filter, which is untested here (**TODO(research)**).

Check: the venue test clip (Exercise 4) looks right on the real screen.

### Step 5. Mix the sound in three outputs

Keep dialogue, music and effects as separate stems, and mix once.

- **Cinema:** do not normalise. Keep headroom and real dynamics. Report the loudness for information only and let a cinema technician align the room. A correctly aligned cinema sets the level, not a number [30].
- **Venue:** start at about -16 LUFS integrated and -1 dBTP. Check intelligibility in the back row with the oldest listener. Never trust the number over the room [2][5].
- **Online:** about -16 LUFS and -1 dBTP. Streaming services normalise, so a quiet cinema mix posted online would play quietly [38].
- **Conflict to settle on the card:** the research starts the venue at -1 dBTP, while the toolchain's loudness example uses -1.5 dBTP [2]. Pick one value and record why.
- Delivery is stereo (L/R) for now. A later cinema version may use a 5.1 fold-up with voices in the centre channel, which is the better cinema option (inference) [28].
- **Mono check:** if loudness drops by more than about 3 LU between the stereo and mono-folded readings, the mix has phase trouble that will show on a mono venue PA. This threshold is a rule of thumb (inference). See Exercise 5.

### Step 6. Burn in the captions

- Open captions, burned into the picture, for the venue file and for the first DCP.
- Keep all text inside the central 90% by 90% box. EBU R95 treats the outer 5% as the graphics-safe margin [37].
- At most two lines, 42 characters or fewer per line, and under 20 characters per second [4].
- **Venue file:** a line height of 7 to 8% of the picture height. The earlier format note reports that `FontSize=23` in ffmpeg gives about 8.0% at 1080p, tested on a TV from three metres [4]. **TODO(research):** confirm this on the real screen with the test clip.
- **Cinema:** start at 5.5 to 6% line height. The same percentage looks about twice as large to a cinema audience as on a 55-inch TV at three metres (computed). Keep captions out of the bottom 8 to 10%, where heads may block them (inference).
- Keep captions out of the black side bars of a Flat container. Do not bury them there.
- **Fonts:** Windows fonts may be used in a video if the text is rendered as a bitmap in the picture and the font file is not embedded [76]. For any DCP subtitle track, use a SIL OFL font, which is unrestricted for video titling [75].

Check: Exercise 4 shows the three caption sizes from the back of the room.

### Step 7. Build the venue file set

These are the rows of the spec sheet in Templates (T2).

- **Venue primary:** MP4, H.264 High level 4.1, yuv420p, BT.709 tags, AAC-LC 48 kHz stereo at 256 kbps, `+faststart`, `-crf 18 -maxrate 20M -bufsize 40M` [2]. Burned-in captions, a neutral file name, no title metadata.
- **Venue backup:** H.264 Main, level 4.0, 1080p24, about 8 Mbps. This is for old TVs and USB players (inference; test it).
- **Venue test clip:** 60 to 90 seconds with no personal content (T7).
- **Audio-only or still fallback:** a 3-minute version [5].
- **Online:** H.264 1080p, a cap of about 12 Mbps. Only after the T3 rights gate (Step 11).

Check: the test clip and the film share pixel format and tags, so one test covers both. Both play on the TV and on the spare laptop from the same path.

### Step 8. Check every file

- Run ffprobe on each file. Read `pix_fmt`, `color_range`, `color_space`, `color_transfer`, frame count and duration [3]. The exact command is **TODO(research)**.
- Run the colour-patch test after every re-encode [3].
- Loudness: `ffmpeg -nostats -i in.wav -af ebur128=peak=true -f null -` prints integrated loudness and peak. The command syntax was run in the cloud container, not yet on the PC.
- Metadata: strip it with `-map_metadata -1` (inference; test it) so no title or comment travels with the file.
- Hash: make a SHA-256 manifest of each delivery folder using the `mk_manifest.ps1` pattern that the research notes cite [4]. Copy the folder to the drive, then re-check the hashes from the drive.

Check: the manifest lists every file, and every hash matches after the copy.

### Step 9. Make the DCP, after the tests

Do this on the Windows PC, not in the cloud container. The container's root disk was full during testing and cannot hold a DCP [47]. Do it only after Exercise 3 passes. If the PC work is not ready, make the DCP after the premiere.

Settings in DCP-o-matic (names as in the manual; check each one on screen):

1. **New film,** named with the neutral code name. The title appears on cinema servers and in key files, so it must not carry her name before the reveal [5][15].
2. **Add the ProRes master.** DCP-o-matic reads it through FFmpeg. Reading ProRes is expected to work but is unverified (**TODO(research)**; test it in Exercise 3) [15].
3. **DCP tab:** Container Flat (1.85). Resolution 2K. Frame rate 24. Standard SMPTE. Encryption off. JPEG2000 bandwidth 100 to 125 Mbit/s (the cap is 250). Reels: single. "Use ISDCF name" ticked. Content type: feature [15].
4. **Audio:** six channels is the default. Map L to L and R to R at unity gain. Check what the ISDCF name shows; whether it reads "20" with only L and R mapped is **TODO(research)** [13].
5. **Video tab:** colour preset Rec. 1886 if the grade was made on a gamma-2.4 display, otherwise Rec. 709. Which gamma each preset applies is **TODO(research)**, so compare the two on a known frame. Range: Video (16-235). Scale to fit [12][35].
6. **Timed text:** leave it empty if the captions are already burned in [14].
7. **Make DCP.** Encoding can take many hours [11].
8. **Verify:** in the Player, open Tools, then Verify DCP. Fix every error and read every warning [18].
9. **Play in the Player.** This proves the package is well-formed, not that a cinema will accept it. The manual warns against depending on the Player without a lot of testing [17].
10. **Write the drive.** Use an MBR partition table with one primary partition of type 0x83, and ext3 or ext2 with a 128-byte inode [26]. DCP-o-matic's Disk Writer does this [19]. Label the drive "Do not read with a consumer computer" [26]. Never plug it into the Windows PC after it is written [26].
11. **Hash the DCP folder,** copy it to a second place, and re-check the hashes.

Size check: at 125 Mbit/s a finished minute is about 0.94 GB, so a 10-minute film is about 9.4 GB (computed) [15]. Encode speed measured on a cloud container was 3 to 4 wall minutes per finished minute for clean frames and about 12 for grainy frames [47]. Your PC's speed is **TODO(research)**. Record yours in Exercise 3.

### Step 10. Test where it will play

- **Venue survey:** ask the questions in Templates (T5) in your own words, without naming the film's subject. Due by Friday 6 November 2026.
- **Test clip first,** with the venue's AV person present. The film itself plays only when the room is empty or only you are present.
- **Full run** on Monday 22 February 2027. Cold starts on Thursday 25 and Friday 26 February. Walk the failure ladder once each with a stopwatch.
- **A later cinema:** ask two or three cinemas for written quotes using the enquiry questions (T6). The pages reviewed for this guide (Picturehouse, Everyman, Cinemark) list no prices, formats or insurance rules, so treat them as questions, not facts [89][90][91].

### Step 11. Clear the rights (start now, in parallel)

- Give every asset its own row in the rights log (T8). One row per asset, cue or person.
- **Sort every person and item into a tier:**
  - **A, in:** a recorded yes on the updated consent card, your own material, or her appearances as you decide.
  - **B, in with documented risk:** adults in ordinary family, event or holiday photos, shown briefly, with no voice and no sensitive context. The owner is known and was asked, or there is an accepted-risk entry. Ratify after the premiere.
  - **C, out unless a yes is on file:** identifiable minors, any voice or video of a living person, named living third parties in hard episodes, ex-partners, estranged people, and any illness, money or conflict scene.
  - **D, out:** the dead, animated or voiced without the closest family's yes; any synthetic voice; invented events shown as fact; identifiable strangers (crop, stylise or leave them out).
- **Music:** a commercial recording needs a sync licence from the publisher and a master licence from the label. A public-performance licence is a third, separate right [82]. A venue's blanket licence, where there is one, normally covers performance, not copying a recording into your film (background; unverified) [82]. For a public gathering, prefer CC0 or CC BY music with credit (not NC), production music licensed for events, original music, or a licensed substitute.
- **Photos taken by others:** find the photographer. Look for a studio stamp on the back of the print, and ask the family. Record every search step. Orphan works have no US safe harbour [54]. The UK has a licence scheme from £20 per work, for UK use only [62].
- **Games and brands:** no Mojang textures, sounds, UI or footage, and no third-party game footage by default [48][51]. Use "Minecraft" only as a secondary description, with the disclaimer, and only if you name it at all [48].
- **AI-assisted material:** every L2-or-higher item needs its tool name, version, date and tool terms. Keep a human-contribution note for each one, and put a pre-roll line before the title [53][65].
- **Accepted risk:** write down why, how you would undo it, who is exposed, and the date. Leave at least 48 hours between drafting and deciding (inference). Get the Fable advisor's written flag on every Tier C item and every accepted risk.
- **The consult:** book one hour with a local rights professional by Friday 4 December 2026. Ask it as a hypothetical, using the question list (T10). Whether to tell a lawyer about the surprise is your call.

### Step 12. After the premiere

- **Written releases** from contributors, lenders, parents of minors, the closest family of anyone who has died, and her. Send them between Sunday 28 February and Saturday 6 March 2027 (TD-L15). Ask for a written yes before any wider showing [79].
- **Her release** is offered after your turn conversation on Saturday 6 March 2027. It has no deadline (T9, 4e).
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
- **Steps:** run `ffmpeg -nostats -i in.wav -af ebur128=peak=true -f null -` on a stereo file. Then run the mono-fold version, `-af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true"`, on the same file. Compare the two integrated readings and note the peak.
- **Time:** about 30 minutes.
- **Good looks like:** both numbers are written down. A drop of more than about 3 LU is a warning sign (rule of thumb, inference). The command syntax has been run in the cloud container and still needs a run on the PC.

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
- **Steps:** fill every bracket in the consent card (T9, 4a). For each sentence, write down whether it is true today. If a sentence is not true, change it or cut it. Read the card aloud once, alone, on a timer. Do not use it with anyone until its bracketed lines are true.
- **Time:** about 45 minutes.
- **Good looks like:** every bracket is filled, every sentence is true, and the card commits you to a written release before any wider showing.

## Templates and checklists

### T1. Settings card (fill in by Sunday 1 November 2026)

```
TD-1 working size:      1920x1080, 16:9; stills 3840 px on the long edge or more   [ ] confirmed
TD-2 frame rate:        24 fps everywhere                                           [ ] confirmed
TD-3 captions:          burned-in open; venue line height 7-8%; cinema start 5.5-6% [ ] confirmed
TD-4 DCP:               Flat 1998x1080, SMPTE, unencrypted, 24 fps                  [ ] confirmed
Venue loudness start:   ____ LUFS integrated, ____ dBTP
                        (research: -16 LUFS, -1 dBTP; toolchain example: -16 LUFS, -1.5 dBTP)
Venue colour trim V:    ______ (starting values: lift 2-4 IRE; mid-gamma +0.05 to +0.10)
Cinema colour trim C:   identity until a real cinema test                           [ ]
Decided by / date:      ______
```

### T2. Delivery spec sheet

| Parameter | Venue, Sat 27 Feb 2027 | Cinema (later, DCP) | Online (private link, later) | Archive |
|---|---|---|---|---|
| Purpose | Plays on whatever the venue has | A hired or festival cinema screen | Family and invited viewers | Preservation and re-making |
| Picture | 1920x1080, 16:9, 24p constant, BT.709, limited range, burned-in open captions | DCP 2K Flat container 1998x1080; picture centred with 39 px black bars each side; XYZ 12-bit via DCP-o-matic [15][22][31] | Same as venue, 1080p24 | ProRes 422 HQ 1920x1080 24p (FFV1 optional) [2][3] |
| Container and codec | MP4, H.264 High 4.1, yuv420p, `+faststart` [2] | SMPTE DCP (picture and sound MXF, CPL, PKL, ASSETMAP), unencrypted [15][21] | MP4, H.264 High, CRF 20, 12 Mbps cap [2] | MOV (ProRes) and/or MKV (FFV1), PCM audio [2] |
| Bit rate | Up to 20 Mbps | JPEG2000 100 to 125 Mbit/s (cap 250) [15][18] | 8 to 12 Mbps | Master data rate |
| Audio | AAC-LC 48 kHz stereo 256 kbps; venue mix about -16 LUFS, -1 dBTP to start (confirm on site) [2][36] | PCM 24-bit 48 kHz; L and R in channels 1 and 2; cinema mix with headroom, not normalised [28][30][31] | AAC 256 kbps stereo; -16 LUFS, -1 dBTP [38] | PCM 24-bit 48 kHz, plus stems |
| Captions | Burned in; two lines; inside the 90% by 90% box [37][4] | Burned in by default, or a SMPTE subtitle track with an OFL font [14][27] | Burned in, plus SRT or VTT sidecar | SRT, VTT, plain-text transcript |
| Rights gate | T2 (public gathering): every row green or a documented risk; no unlicensed commercial music; no Mojang assets | T4: all T3 items green; releases signed; E&O decision; music cue sheet; AI disclosure | T3: releases signed; your explicit yes for the host [4] | Log, ledger and releases kept with the masters, in encrypted storage |
| File name | Neutral code name; no personal data; no title metadata; version and date | ISDCF-generated name; neutral title [15][25] | Neutral | Descriptive, in a folder with a README |
| Media | Two USB sticks (FAT32 if the file is under 4 GiB, which at 20 Mbps is about 28 minutes, computed; exFAT if the TV takes it) [43][44], plus two laptops | Drive written as MBR, one primary partition of type 0x83, ext2 or ext3, inode 128; label "Do not read with a consumer computer" [19][26] | Upload | Two physical copies plus one off-site [2] |
| Checks | ffprobe tags and pixel format; colour-patch test; loudness and mono-fold; caption legibility at 3 m; hashes; gates G6 and G6b [3] | Verify DCP with no errors; play in the Player; SHA-256 manifest; real-cinema test slot [18][17] | ffprobe; watch on a phone and a TV | Hash check yearly [2] |
| Fallback | Backup ladder (T3) | A second DCP with burned-in captions if subtitle rendering fails [20] | n/a | n/a |

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
- [ ] Ask who controls the venue fader. Know where the microphone is for a 30 to 60 second welcome [5].

**Kit**
- [ ] Two USB sticks in different pockets. Two laptops with the same file at the same path.
- [ ] Spare HDMI cable. Adapter kit (USB-C, DisplayPort, mini-HDMI). USB-C hub. Chargers.
- [ ] Printed running order. The test clip on a stick.
- [ ] A cloud copy only with your explicit yes [1][4].

**Backup ladder**
1. Laptop playing the screening file.
2. Second laptop with the same file.
3. USB stick straight into the TV or projector media player (needs the exFAT and MP4 test).
4. Phone by cable or cast.
5. The 3-minute audio or still version.
6. A postponed private evening, said plainly.

### T4. Run-sheet lines (technical)

Numbered to merge into the surprise-ops key dates and the reveal-day run sheet [5].

| ID | When | Who | Action | Pass criterion | If it fails |
|---|---|---|---|---|---|
| TD-L1 | Sun 1 Nov 2026 | Maker | Write TD-1 to TD-4 into the settings card | Card saved in repo | n/a |
| TD-L2 | By Fri 6 Nov 2026 | Maker | Venue survey (T5) | Answers logged | Assume the worst case: laptop, HDMI, TV |
| TD-L3 | By Sun 20 Dec 2026 (G9) | Maker, agents | Build and view the venue test clip on the home TV; caption sizes 20, 23, 26 at 3 m; mono-fold; ffprobe | All clip checks pass | Fix and rerun |
| TD-L4 | By Sun 20 Dec 2026 | Maker | Make a 60-second test DCP on the PC; Verify; play in the Player | Zero errors; plays | Move DCP work to after the premiere |
| TD-L5 | By Fri 4 Dec 2026 (follow-up Jan 2027) | Maker | Hold the consult; update the rights log and the releases | Notes saved | See Decisions |
| TD-L6 | Mon 15 Feb 2027 | Maker | Minecraft terms check (only if any Mojang name or asset is used); contributors confirm their clip; rights-log review | Hash matches, or the diff is read | Remove the asset or seek permission |
| TD-L7 | Fri 19 Feb 2027 (picture lock) | Maker | Freeze the rights log, AI cue sheet, music cue sheet and credits | Every row has a status | Take out or substitute |
| TD-L8 | Sat 20 and Sun 21 Feb 2027 | Maker, agents | Final exports: master, venue file, backup file, audio-only fallback; apply trims; ffprobe, loudness, mono-fold; hashes; two sticks; gate G6 [3] | G6 passes | Re-export |
| TD-L9 | Mon 22 Feb 2027 (full run) | Maker with venue AV operator | (1) Power the chain from cold; time to first frame. (2) Play the test clip: picture mode, overscan, HDR off, bars, PLUGE, ramp, tone level, left and right, caption size from the back row. (3) Room empty: play the first 5 and last 5 minutes and three spot sections. (4) Walk failure rungs 1 to 4. (5) Photograph settings and cabling. Gate G6b | Plays at the right levels; captions readable; no overscan crop; sound intelligible; mono-fold OK; cold start under 2 minutes | Adjust and repeat on Thursday or Friday |
| TD-L10 | Wed 24 Feb 2027 (room brief) | Maker | Confirm AV access times with the venue (send no content) | Times confirmed | n/a |
| TD-L11 | Thu 25 Feb 2027 (cold start 1) | Maker, with operator | Cold start on the real device and cable from power-off | First frame within 2 minutes | Rehearse again Friday |
| TD-L12 | Fri 26 Feb 2027 (cold start 2, pack list) | Maker | Cold start 2; Minecraft terms check 2 (if applicable); pack list (T3, Kit) | Pack list ticked | n/a |
| TD-L13 | Sat 27 Feb 2027, S minus 4 h and S minus 2 h | Tech | Set up; run the test clip; confirm Do Not Disturb, notifications hidden, mail and chat closed [5]; play the first and last 30 seconds; spoken-line sound check; snapshot settings | As rehearsal | Use the ladder |
| TD-L14 | End of night | Tech | Back up any agreed room recording; delete extras; collect USB sticks [5] | Sticks accounted for | n/a |
| TD-L15 | Sun 28 Feb to Sat 6 Mar 2027 | Maker | Send post-premiere releases (T9, 4d to 4g); her turn conversation on Sat 6 Mar [5] | Requests sent | n/a |
| TD-L16 | Mon 29 Mar 2027 (ledger closes) | Maker | Close the consent ledger; set T3 and T4 gates in the rights log | Every row kept, changed, removed or closed until a date | No wider showing |

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
6. Caption test: three sizes (FontSize 20, 23, 26) inside the 90% box, with frame outlines at 100%, 96.5% and 95% to show overscan and masking.
7. A slow 24p pan across a detailed image (judder and motion smoothing).
8. A one-minute speech sample at the film's mix level (intelligibility).

### T8. Rights-clearance log

One row per asset, cue or person. The log is a CSV in the private repo, with sheets for `assets`, `music_cues`, `ai_items`, `persons_releases` (the consent ledger), `fonts` and `games_brands`.

Header:

```
asset_id,type,title_or_description,where_used,how_obtained_and_by_whom,rights_holder_and_contact,persons_depicted,minor_flag,deceased_flag,needed_T1,needed_T2,needed_T3,needed_T4,permission_type,scope_media_territory_term_event,fee,status,evidence_ref_and_sha256,status_date,decided_by,advisor_flag,risk_tier,jurisdiction_note,substitute_asset_id,ai_label_L0_L5,ai_tool_version_date,music_cue_ref,release_id,notes
```

Column guide:
- `type`: photo, video, audio, music, voice, font, game, brand, ai, text or other.
- `needed_T1` to `needed_T4`: Y (needed), N, ? (unknown, ask) or V (venue-dependent). T1, the private cut for her alone, carries less exposure but is not zero, so third-party commercial assets stay "?" there.
- `status`: NS (not started), ASKED, GRANTED, REFUSED, SUBST (substituted), RISK (accepted documented risk), OUT, VERIFY (for the consult).
- `risk_tier`: A, B, C or D (see Step 11).
- `jurisdiction_note`: begins "Jurisdiction not yet known; confirm; not legal advice:" until TD-7 is answered.
- A RISK row must also say why, how it would be undone, who is exposed, and the date.

Sample rows (from the research notes):

| asset_id | type | where | rights holder | needed T1/T2/T3/T4 | permission | status | evidence | tier | note |
|---|---|---|---|---|---|---|---|---|---|
| PH-0042 | photo | Ch.1 | Aunt (took it, 1978) | ?/Y/Y/Y | Recorded yes on consent card | GRANTED | rec-0007.wav, sha256 ... | A | Ratify in writing after the premiere |
| PH-0107 | photo | Ch.2 | Studio stamp (defunct?) | ?/Y/Y/Y | None | VERIFY, SUBST candidate | scan of back, note | B | Search done 2026-xx-xx; UK scheme from £20 per work, UK only; US has no safe harbour |
| MU-003 | music | Ch.3 bed | CC BY composer | Y/Y/Y/Y | CC BY 4.0, credit | GRANTED | licence PDF | n/a | Credit in end titles |
| MU-011 | music | Ch.4 | Label and publisher | ?/Y/Y/Y | Sync and master needed | NS | none | n/a | Substitute with MU-003 |
| FN-001 | font | Titles | SIL OFL font | N/N/N/N | OFL | GRANTED | font file and OFL.txt | n/a | Rasterised in video; embedded in DCP track |
| GM-002 | game | Ch.5 | Mojang | ?/Y/Y/Y | Not used (original voxel assets) | OUT | check_mojang_quotes output | n/a | Disclaimer if the name appears |
| AI-014 | ai | Ch.2 | Tool terms; human selection | ?/Y/Y/Y | Tool terms read 2026-xx | GRANTED | steps.csv row | n/a | Label L4b; pre-roll line |

Before T4, every row needs `permission_type`, `scope`, `evidence_ref`, and a signed release or documented exception for every person in Tiers A to C.

### T9. Releases pack

Principles: say what the film is; state nothing untrue; you may omit the fact of the surprise, but not anything false; offer a way out; keep each text to one page; write in the person's language. Jurisdiction and legal wording are placeholders.

**4a. Contributor consent card, version 2.** Read it aloud on the recording. It replaces the old card in surprise-ops [5]. Read it only when the bracketed lines are true.

> "[MAKER] is making a film about [NAME]'s life as a surprise gift. It will be shown once, at a gathering on [date], to about [N] people: [family and invited friends] / [family, friends and community guests, which means it is a public-facing event, not only a family evening]. A longer private version will be given to [NAME]. May I use what you say, your recorded voice, your name, and any photographs or video you lend, in those showings? You can skip any question, stop, and ask me up to [Fri 19 Feb 2027] to take anything out. I will keep the recording private on storage I control [edit to match]. I may use software, including AI tools [that run on my own computer / in a private online workspace: edit to match], to type it up and tidy the sound, but I will not change what you said or make a synthetic copy of your voice. After the gathering I will ask you to sign a short written release if I want to show the film any further, for example online or in a cinema, and I will not do that without your signed yes. Is that all right with you?"

**4b. One-line version for a text or voice message:** "May I use your recorded voice and photos in a film for [NAME]'s gathering on [date], shown to about [N] guests, with you able to skip questions, stop, or have anything taken out until [date], and nothing wider without your written yes?"

**4c. Lender note** (for photos, video or letters lent by someone who is in on it): "You lend these items, which you took or own, for use in the film described above. You allow them to be shown at the gathering and in [NAME]'s private version. You may ask me to remove any item until [date]. I will return the originals on [date]. For any further showing I will ask you again in writing." For lenders who are **not** in on it, use a truthful pretext card from surprise-ops [5], and keep their copyright items out of the shared cut unless Tier B applies. Ratify afterwards.

**4d. Post-premiere written release** (contributor or lender; one page). Fields: name; the film (working title and occasion); what you contributed (voice recording dated, photographs listed, video). Then:
- I agree that the film may be shown: [ ] at further private gatherings; [ ] in a private online link; [ ] at public screenings, including a cinema or festival; [ ] kept in the family archive.
- I understand: no fee is payable. The maker may edit, crop, restyle and restore my contribution, including with AI-assisted restoration, but will not change the meaning of what I said or create a synthetic voice. My name will appear as [full name / first name / no name]. I may withdraw consent for future showings by writing to [contact]; copies already shared privately may remain. The maker will store my material at [place] for [period] and use it only for this film. I own, or have the right to license, what I contributed [or: someone else took it, named here].
- Territory: worldwide. Term: until I withdraw in writing [or: a fixed term of N years]. Governing law: [jurisdiction not yet known].
- Signature and date.

The usual documentary grant is all media, worldwide, in perpetuity [79]. This version trades that for a withdrawal right, so choose before any E&O application (your decision).

**4e. Her release** (offered after the reveal and her turn conversation, Saturday 6 March 2027; no deadline). In plain language: "This film is about you. Nothing is shown anywhere new without your yes. For each use, tick yes, no, or ask me again: [ ] family gatherings; [ ] a private online link for family; [ ] a public or invited screening you choose; [ ] a cinema or festival; [ ] kept in the family archive. You can ask me to remove or redo any scene (the list from our conversation is attached). You do not have to decide now; you can change your mind later by telling me. No payment passes either way. You keep the right to be named or not."
Fields: her name; the scene list with her choice (kept, changed, removed, or closed until a date); the uses table; signature; date; optional witness. This maps to the consent ledger and her version (about 24 April 2027) [5].

**4f. Parent or guardian addendum (minors).** "I am the parent or guardian of [child's name, age]. I allow [child]'s [photograph / voice / name] to be used as in the release above." Signature, relationship, date [86]. Under 14: guardian present, and one question. 14 to 17: guardian consent and the child's own yes in plain words [5].

**4g. Family-of-the-deceased note** (a short message; keep the reply in the log): "I am making a film about [NAME]. I would like to include a [photograph / recording] of [deceased person]. It would be shown [as a still, no movement, no new voice]. May I? You can say no, or ask me to remove it later." Record the sender, relationship and date.

**4h. Verbal-release script** (if a person will not sign). On the recording, state the purpose, where the film will first be shown (the gathering on [date]), and what further uses are possible. Ask them to say yes in their own words [79]. Do not ask for a signature long after they declined at the time [79].

### T10. Consult question list (one hour, asked as a hypothetical)

Send it before the hour. Do not name her.

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
13. Fonts and game content: is there any local rule about embedding fonts in video, or showing game footage?
14. Brand-name games: is a stylised voxel world "in the style of" a game safe, and what should I avoid?
15. If I later hire a cinema, what insurance and paperwork will they or the law require? Is E&O needed for a single screening?
16. Before a cinema, festival or online release, what is the minimum clearance file (log, releases, licences) a lawyer would want?
17. Who is liable if a contributor withdraws after the screening?
18. How should I word the releases here (term, territory, right to edit, withdrawal)?
19. Are there trademark or personality issues in using her name in the title?
20. Is it better to wait for her release before any screening beyond 27 February?

### T11. Pack list for 26 February 2027

- [ ] Two USB sticks with the film files (venue file, backup file, audio-only fallback).
- [ ] Two laptops, the same file at the same path.
- [ ] HDMI cable and a spare. Adapter kit. Chargers. USB-C hub.
- [ ] Printed running order and the failure ladder.
- [ ] The test clip on a stick.

## Decisions you'll need to make

Each decision lists the options and our current lean. Leans are not final until you write them on the settings card.

| ID | Decision | Options | Our current lean | What would change it |
|---|---|---|---|---|
| TD-1 | Working size | 1920x1080 (16:9); 2K DCI; UHD | Stay at 1920x1080. Derive the 2K Flat DCP from it. Prepare stills at 3840 px or more. UHD only for single hero shots, and only if a booked 4K cinema justifies it, decided before Sunday 3 January 2027 [3][15] | A booked 4K cinema and a chapter that needs more detail |
| TD-2 | Frame rate | 24 fps; 25 fps | 24 fps everywhere [16] | A 50 Hz-only venue whose test clip judders. Then make a 25 fps access copy with `fps=25`, not a speed change (untested) |
| TD-3 | Captions | Burned-in open captions; soft subtitles | Burned-in open captions (7 to 8% line height for the venue file). Sidecar SRT and VTT. A DCP subtitle track only for a later cinema, with an OFL font [20] | A venue that asks for soft subtitles |
| TD-4 | DCP container and standard | Flat 1998x1080; Scope. SMPTE; Interop | Flat, SMPTE, unencrypted, 24 fps [15][27] | A cinema that demands Interop or Scope |
| TD-5 | Door policy for 27 February | Invite-only; open to all | Your decision. Invite-only keeps festival premiere status, under Sundance's rule [88]. Open to all raises the music, photo, likeness and Minecraft exposure [48][56] | Your wishes for the room |
| TD-6 | Who runs playback on the day | Venue AV operator told a truthful minimum; a hired tech; you | A person told a truthful minimum (the venue operator or a hired tech). You host [5] | You bring someone in, which changes "only me" |
| TD-7 | Country and state of the premiere | Any | Needed before the consult. It also decides the music, photo and likeness answers [56] | None. It must be answered |
| TD-8 | Rights consult | Pay for one hour; skip | One paid hour by Friday 4 December 2026, asked as a hypothetical (T10) | Budget or privacy preferences |

### Other decisions

- **Who is in on it, and who approves the hard chapters.** You told us: only you, for now. You are her proxy for hard chapters. The compensating controls are the Fable advisor's written flag on every Tier C item and every accepted risk, a written reason and an undo note for every accepted risk, at least 48 hours between drafting and deciding (inference), and the paid consult. You asked that a second approver or a day-of tech be decided later, once the plan is ready. Bringing anyone in changes "only me", so note the decision when it is made.
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
- Trim values, the cinema caption size (5.5 to 6%) and the venue caption size need a real-screen test.

## Pitfalls

1. **Treating the rules as universal.** Fair use is US law. Fair dealing is UK and Indian law. Personality and post-mortem rights vary by country and US state. Every legal statement here needs its jurisdiction and "not legal advice" until TD-7 is answered [56][61][70][71].
2. **Using the old consent card.** It says "a film that family will watch together" and "private" [5]. Use version 2 (T9, 4a) before the first recording.
3. **Calling a free public premiere a family showing.** US law reaches beyond a family circle [56]. Sundance treats free public screenings as public exhibition [88]. Minecraft counts sharing as commercial use, even if it is free [48]. Use the door policy (TD-5) and the tiers.
4. **Loudness confusion.** A broadcast -23 LUFS target applied to a cinema mix is wrong [36]. A quiet cinema mix posted online will play quietly [38]. The venue PA is unknown until tested [5].
5. **Colour drift** between a consumer monitor, the venue and a cinema. Use one grade and two trims, test on the real screen, and turn HDR off [42].
6. **DCP ingest failures.** The common ones are the wrong drive format, a corrupt copy, subtitle or standard faults, KDM trouble, and a capability mismatch. The ranking is a judgement, not statistics (**TODO(research)**) [18][19][26].
7. **Writing a DCP drive and then using it on a consumer computer.** The consumer system may reformat or damage it [26]. Label it, never plug it into the Windows PC after writing, and keep a copy of the folder elsewhere.
8. **The surprise leaks through technical channels.** Look at DCP and file titles, metadata, thumbnails, "Recent" lists, staff who watch the film, and cloud copies. Use a neutral code name, strip metadata, use the neutral test clip for staff, and play the film only in an empty room [5].
9. **Minecraft terms are undated and can change.** The guidelines say the company may revoke the permissions at any time [48][49]. Use original voxel assets, and run the hash check in premiere week.
10. **Over-trusting fair use for family photographs.** "Still photographs in particular do not lend themselves to fair use treatment" [80]. Ask, substitute, or document a Tier B decision, and use the consult.
11. **Accepted risks decided by one person.** With no second key, mistakes go unchallenged. Use the advisor flag, written reasons, the 48-hour gap, and reversible choices first.
12. **AI disclosure and ownership gaps.** Free tool tiers may exclude commercial or public use. Re-encoding and platforms can strip metadata, and photoreal motion of a real person can read as a deepfake [6][65]. Keep the tool terms in the ledger and add the pre-roll line.
13. **Personal data in the rights log.** Names, consents and addresses stay in the private repo. Encrypt the archive copy. Upload nothing to a third party without your explicit yes [1].
14. **Misleading edits.** A film can mislead even when each clip is true [85]. Show no invented events as fact. Label reconstructions (L5) [6].
15. **Caption and sound accessibility.** Older audiences need readable captions and clear dialogue [4][5]. Test them from the back row with the oldest listener.
16. **Disk and compute limits in the cloud container.** The root disk was full during testing [47]. Encode the DCP on the PC, and use the container for measurement and checks.
17. **Relying on the DCP Player at the venue.** The manual warns against depending on it [17]. The venue gets the MP4. The DCP is for a cinema.
18. **Dignity for people who cannot be asked.** Apply the Tier C and D rules. Ask the closest family about the dead. The estranged default to out [5].

## Best references

These eight are the best use of your reading time. Each link is one that the research notes cite. The Sources section gives the dates and what was read.

1. **DCP-o-matic manual, DCP settings chapter** [15]. https://dcpomatic.com/manual/html/ch07.html. Why: the settings you will click, with the 2K advice, bit rate, container and standard explained.
2. **DCP-o-matic colour paper, "Colour conversions for DCP creation"** [22]. https://dcpomatic.com/manual/colour.pdf. Why: the colour maths in plain steps (Exercise 1).
3. **ISDCF Doc 3, DCP Delivery Recommendations** [26]. https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf. Why: the drive format rules and the warning about consumer computers.
4. **ISDCF Doc 11, "How Loud is a Movie?"** [30]. https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf. Why: why a cinema mix is set by the room and not by a loudness number.
5. **DCP-o-matic manual, verifying DCPs** [18]. https://dcpomatic.com/manual/html/ch19.html. Why: what each Verify error and warning means before you ship.
6. **IDA, "A Practical Discussion of Appearance Releases"** [79]. https://www.documentary.org/column/practical-discussion-appearance-releases. Why: what a release must say, and the verbal fallback.
7. **Sundance Film Festival 2027 submissions FAQ** [88]. https://www.sundance.org/submissions-faq. Why: a real festival's delivery and premiere rules, including the free-screening trap.
8. **Minecraft Usage Guidelines** [48]. https://www.minecraft.net/en-us/usage-guidelines. Why: the plain-language rules for any Mojang name, asset or footage.

## Sources

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

[48] Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 about 07:00 GMT; no visible date — physical locations, 150 participants, sharing equals commercial, name as title, disclaimer; extract hash c5a8...94222 matches earlier captures.

[49] Minecraft EULA — https://www.minecraft.net/en-us/eula — fetched 2026-10-18 about 07:00 GMT; no visible date — distribution, content ownership, guidelines revocable; excerpt in research/sources/.

[51] Microsoft, Game Content Usage Rules — https://www.xbox.com/en-US/developers/rules — "Last Updated: January 2015" — covers Microsoft games except Minecraft.

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
