# Theatre-grade masters, venue playback, and rights clearance for public screening — research notes

Researcher: Sonnet (Sonnet 5.5), track `theatrical-delivery`. Date of research: Sunday 2026-10-18. Premiere: Saturday 2027-02-27 (about 19 weeks). Maker: the only human on the project (confirmed again in the relayed request: "only me ... i will be the only one on this project"). Nothing here is legal advice. Every legal statement is flagged "jurisdiction not yet known; confirm; not legal advice" and carries the jurisdiction it comes from.

How to read the tags: **[n]** is a source in the numbered list at the end. Quoted phrases from web pages came back through the fetch tool; I re-checked word for word only the ones read directly from files I downloaded (Minecraft pages, ISDCF papers, EBU, ITU, Copyright Office, Sundance PDFs, the German KUG and the Indian Act). **UNVERIFIED** means I could not read a primary source on this date. **(inference)** is my own reasoning from sources. **(measured)** is a test I ran in the cloud container on 2026-10-18 (source [47]).

**A limit on this round.** The shared web-search budget ran out after my first four search calls returned "budget used up", so I could not search. I worked by fetching known primary pages directly (DCP-o-matic's manual, ISDCF papers, statutes, Sundance's 2027 rules, IDA articles, Minecraft's pages). Anything I could not reach is listed in "Open questions / gaps" and tagged UNVERIFIED in the text. I did not use search engines, readers or archive services as a workaround.

## Summary

1. **Keep the working master at 1920x1080, 24 fps, Rec.709, ProRes 422 HQ, 48 kHz 24-bit. Do not move to UHD or to 2K DCI as the working size.** A 2K Flat DCP (1998x1080) is derived from the 1080p master with the 16:9 picture centred and 39 px black bars each side. DCP-o-matic's own advice is "Use 2K unless you have content that is of high enough resolution to be worth presenting in 4K." [15]. UHD is four times the pixels and cost me 3.0x CPU and 3.7x wall time in a JPEG2000 test (measured) [47]. The week-2 decision (due Sun 1 Nov 2026) is in Finding 1.
2. **24 fps is the only frame rate DCP-o-matic calls safe for unknown places** (the manual's words: "24 frames per second (fps) for video and 48kHz for audio") [16]. A 25 fps source in a 24 fps DCP plays about 4% slow (a 4.17% change, about 0.71 semitone of pitch, computed) [16]. Keep 24; hold a 25 fps conform only as a contingency if the venue is 50 Hz-only and the test shows judder.
3. **DCP-o-matic 2.18.51 was released 16 October 2026 and is GPL-licensed** [8][10]. It has command-line tools (`dcpomatic2_create`, `dcpomatic2_cli`) so agents can drive it [21]. For an unknown cinema: SMPTE standard ("if in doubt"), unencrypted (no KDM), 2K Flat, 24 fps, JPEG2000 about 100 to 125 Mbit/s (cap 250), single reel [15]. Verify with the Player's Verify tool, hash the folder yourself, and write the drive as ext2/ext3 on an MBR table with a 128-byte inode [18][19][26].
4. **Encode time (measured, not DCP-o-matic itself):** ffmpeg's OpenJPEG wrapper on the 4-vCPU container took about 3 to 4 wall minutes per finished minute on clean synthetic frames and about 12 on grainy ones [47]. A 10-minute film is 0.5 to 2 hours, a 20-minute film 1 to 4 hours. The job limit is not the problem (background jobs run up to 2 hours). Disk is: a 10-minute DCP at 125 Mbit/s is about 9.4 GB, and the container's root disk had only about 140 to 290 MB free during my tests [47]. Encode the DCP on the Windows PC, or after the premiere.
5. **Colour: DCP-o-matic linearises the picture, converts with a 3x3 matrix to XYZ (Rec.709 primaries, D65), adapts the white point (Bradford), scales by 48/52.37, and applies a 1/2.6 gamma** [22]. Pick its "Rec. 1886" source preset for a gamma-2.4 grade, set Range to Video (16-235), and check the preview [12][35]. Which preset uses which gamma value is UNVERIFIED. Manage venue-TV versus cinema looks with one grade and two small trims (lookup tables applied at export), tested with a venue test clip on the real screen.
6. **Loudness: a cinema mix is not LUFS-normalised and a -23 LUFS broadcast target is wrong for it.** EBU R128's -23.0 LUFS, -1 dBTP is a broadcast-programme rule [36]. Cinemas are calibrated rooms where "a correctly aligned theatre playing a movie at fader 7 will reproduce the level heard by the director and mixer" [30]. Plan three audio outputs from one mix: a cinema mix (no normalisation, headroom kept), a venue/PA mix and an online mix (both start at about -16 LUFS, -1 dBTP; the venue PA is unknown until tested).
7. **Captions: burned-in open captions remain the safe default.** DCP-o-matic's own manual says burnt-in subtitles are slower to make but less likely to fail with unusual positioning or character sets, and projector-rendered ones "mostly work well but are not 100% reliable" [20]. Burned-in text rendered as a bitmap is allowed for Windows fonts (Microsoft treats it like a graphic file if the font is not embedded in the video) [76]. A DCP subtitle track embeds a font, so use an OFL font there [75]. Keep text inside EBU R95's 5% graphics-safe area [37].
8. **"Mostly public" matters for rights.** In US law a performance is "public" at "a place open to the public" or where "a substantial number of persons outside of a normal circle of a family and its social acquaintances is gathered" [56]. So the family-showing assumptions in earlier notes do not hold for the 27 February event: music needs sync and master permission, photos by others need the owner's permission or a documented risk decision, and contributors must be told the true audience. (US text; UK, EU and India differ. Jurisdiction not yet known; confirm; not legal advice.)
9. **Releases paradox, resolved in three stages.** (1) Ask only what can be asked truthfully now; update the consent card because it currently says "a film that family will watch together" and "private" [5]. (2) Build the public cut from cleared or low-risk appearances only. (3) Gather written releases after the premiere, before any cinema, online or further showing, including hers. Sections: Finding 8 and the Releases pack.
10. **Minecraft, re-read on 2026-10-18 at about 07:00 GMT:** the extracted text hash equals the earlier same-day captures and all 12 tracked quotes are PRESENT [48]. Today's read adds clauses the excerpt did not capture (see Finding 7). The default is unchanged: original voxel assets, "Minecraft" by reference only. Charging admission for projected gameplay in a theatre is an explicit "not allowed"; a free hall showing is not named but is not defined either.
11. **A free public premiere can cost a later festival run.** Sundance's 2027 FAQ counts any screening "for which tickets were made available for purchase or given freely to members of the general public" as "public theatrical exhibition"; "private, invite-only" screenings do not count [88]. If festivals ever matter, make 27 February invite-only. Other festivals' rules are UNVERIFIED. (Decision for the maker.)
12. **AI material: US copyright needs human authorship** (Copyright Office Part 2, Jan 2025: prompts alone are not enough; human selection, arrangement and modification can be protected; disclose more-than-minimal AI material when registering) [53]. Sundance requires disclosure of any AI use or risks disqualification [87][88]. The EU AI Act's Article 50 deepfake disclosure is "limited" for evidently artistic works [65]. The ai-imagery L0 to L5 ladder and cue sheet cover most of this but need six extensions (Finding 10).
13. **Photos by others are owned differently by country.** US and UK: generally the photographer. India: s.17(b) of the Copyright Act (the copy I read) makes the person who commissioned a photograph "for valuable consideration" the first owner "in the absence of any agreement to the contrary" [70]. Orphan works have no US safe harbour ("anyone using an orphan work does so under a legal cloud") [54]; the UK has a licence scheme with a £20 application fee for one work (sliding scale) plus a licence fee, UK use only [62]; the EU directive covers institutions only [63].
14. **E&O insurance:** distributors, broadcasters and exhibitors generally require it; usual limits are $1M per claim and $3M aggregate [77][78]. The only premium figure I found is "$2,500 or more" (IDA, 2017, USD) [78]. 2026 cost is UNVERIFIED. None of the cinema hire pages I read (Picturehouse, Everyman, Cinemark) lists a price, a format list or an insurance rule [89][90][91]. Treat all as quotes to request.
15. **Only the maker is on this project.** No second key exists for rights or hard-chapter decisions. Compensating controls are in Finding 11: the Fable advisor's flag, a written entry with reasoning for every accepted risk, a cooling-off gap, and a one-hour paid consult asked as a hypothetical. The day-of TECH role needs a decision (venue AV operator told a truthful minimum, or a hired tech); the maker cannot both host and run playback.

## Findings by question

### Finding 1. Safest master and deliverable set; resolution and frame rate; the week-2 decision

**Answer.** Keep agent-pipeline's settings card (1920x1080, 24 fps, Rec.709, 48 kHz 24-bit, ProRes 422 HQ master) [3]. Lock it by Sunday 1 November 2026 (the week-2 deadline) as decision TD-1, with three amendments: (a) all scans and stills are prepared at 3840 px on the long edge or larger ("4K-equivalent headroom") so camera moves crop into real detail; (b) a 2K Flat DCP and everything else are derived from the 1080p master, never re-authored; (c) a UHD "escape hatch" exists only for individual hero shots, and only if a booked 4K cinema justifies it (revisit date: before Chapter 2 rough cut, Sunday 3 January 2027, when resolution locks for good).

**Evidence for 1080p over 2K DCI or UHD as the working size.**

| Question | Evidence | Reading |
|---|---|---|
| What sizes does a DCP allow? | DCI 2K and 4K maximum frame sizes are 2048x1080 and 4096x2160. Flat is 1998x1080 (3996x2160 at 4K), Scope 2048x858, a 16:9 "HDTV" container 1920x1080 also exists, Full is 2048x1080 [31] (Wikipedia, secondary). DCP-o-matic gives Flat as 1998x1080 for 2K and offers a Container setting that pads content with black [12][15] | A 1920x1080 picture fits a Flat container with no scaling beyond centring: 39 px of black each side (inference from [12][31]) |
| What does DCP-o-matic advise? | "Use 2K unless you have content that is of high enough resolution to be worth presenting in 4K." Most commercial DCPs use 75 to 125 Mbit/s; the range is 50 to 250 [15] | 2K is the default even for people with 4K content |
| What does the cinema install base look like? | Wikipedia reports 98% of the world's screens digital by end-2017 [32] and 10,033 screens in India in 2025 [74]. I found no source giving the 2K versus 4K share, in India or elsewhere (UNVERIFIED). A 4K projector playing a 2K DCP by upscaling is standard DCI behaviour (background knowledge; the DCI specification itself was not readable on 2026-10-18, UNVERIFIED) | Any digital cinema takes a 2K DCP. Only a 4K-native look would need more, and our sources are not 4K |
| What does 4K cost? | UHD and DCI 4K have 4.0 times the pixels of 1080p. Measured JPEG2000 encode: 3996x2160 cost 3.0x the CPU-seconds and 3.7x the wall time of 1998x1080 on the same frames [47]. ProRes 422 HQ at 1080p is about 590 MB per minute on a test pattern [3] (so UHD about 4x, inference). Code-rendered shots (Blender, Remotion) scale with pixel count; the agent-pipeline notes already budget render time at 1080p [3] | Three to four times the render, encode and storage burden across about 120 shots for no visible gain on a TV or hall projector (inference) |
| What do the sources contain? | Photo prints and home video are the inputs [1]. AI image and video tools are the other input; their native sizes are not part of this track (ai-imagery owns that) | A UHD frame built from a 1080p-native clip or a small scan is upscaled, not sharper (inference) |
| Does a 2K DCI working size help? | It changes the frame to 1.90 (2048x1080) or 1.85 (1998x1080), while every TV and projector the venue may use is 16:9 | It trades a clean 16:9 frame for nothing the venue can show (inference) |

**Aspect ratio.** Use 16:9 inside the 1.85 Flat container. Scope (2.39) would crop a 16:9 frame to about 1920x803, cutting 26% of the height, which would hurt photo moves, titles and captions (inference from [31]). Choose Flat as the DCP container; the CLI option is `--container-ratio 185` [21].

**Frame rate: 24 versus 25, region unknown.**
- DCP-o-matic: the only universally safe rates are "24 frames per second (fps) for video and 48kHz for audio"; 25, 30, 48, 50 and 60 fps are supported by many newer projectors, "but not all". Its advice: use 24 fps and 48 kHz where possible, "especially if you are sending DCPs to unknown places" [16].
- Conforming 25 fps to a 24 fps DCP slows the picture by about 4% and resamples audio so it stays in sync but changes its pitch slightly [16]. The reverse (24 to 25) speeds everything up by 4.17%: a 10:00 film becomes 9:36 and pitch rises about 0.71 semitones (computed). That damages music and voices.
- 24 fps content on 60 Hz displays is shown by repeating frames unevenly (3:2 pulldown), which "creates uneven motion, appearing stroboscopic", called judder [39]. A 120 Hz display can show each 24 fps frame five times and avoid it [40]. Slow pans over stills expose judder most (inference).
- mpv's `--video-sync=display-resample` tries "to not skip or repeat frames when for example playing 24fps video on a 24Hz screen", at the price of a slight speed change; it requires constant frame rate [41].
- **Decision:** 24 fps master and 24 fps DCP everywhere. If the venue turns out to be 50 Hz-only and the test clip judders, make a contingency 25 fps access copy with the ffmpeg `fps=25` filter (duplicates about one frame in 24, audio untouched), not a speed change (inference; untested). That choice waits on the venue test.

**Recommended deliverable set for a one-off public gathering with unknown AV.**

| # | Deliverable | Spec | Why |
|---|---|---|---|
| 1 | Master | ProRes 422 HQ `.mov`, 1920x1080, 24p, Rec.709, limited range, 10-bit 4:2:2, PCM 24-bit 48 kHz | Existing settings card [3]; every other file derives from it |
| 2 | Venue screening file (primary) | H.264 High, level 4.1, yuv420p, 1080p24, BT.709 tags, AAC-LC 48 kHz stereo 256 kbps, `+faststart`, burned-in open captions, neutral file name, no metadata title | toolchain Step 12 [2]; burned-in captions are the one thing every screen shows [2][20] |
| 3 | Venue backup file | H.264 Main, level 4.0, 1080p24, about 8 Mbps, same captions | A weaker-decoder fallback for old TVs and USB players (inference; test) |
| 4 | Venue test clip (new) | 60 to 90 s, no personal content: bars, PLUGE, grey ramp (banding), 1 kHz line-up tone, pink noise, left/right ID, caption-size test, 24p pan, countdown | Lets venue staff see a test without seeing the film (surprise); see Templates |
| 5 | Audio-only/still fallback | 3-minute version per surprise-ops' ladder [5] | Last rung before a postponed private evening |
| 6 | Online | H.264 1080p, about 12 Mbps cap, -16 LUFS mix | toolchain Step 12 [2]; only after release step (Finding 8) |
| 7 | Cinema | SMPTE DCP, 2K Flat, 24 fps, unencrypted, stereo L/R in channels 1 and 2 of a 6-channel container (check the ISDCF name), JPEG2000 about 125 Mbit/s | Finding 4 |
| 8 | Archive | ProRes master, FFV1 if wanted, SRT/VTT sidecars, DCP folder, hash manifest, README | toolchain Step 15 [2] owns formats |

**Container, codec and capture checks (new on top of toolchain Step 13).** Check `pix_fmt`, `color_range`, `color_space`, `color_transfer`, frame count and duration with ffprobe; run the agent-pipeline colour-patch test on every re-encode; pass a mono-fold loudness check (Finding 3). H.265 is optional only: Windows and many USB players treat HEVC less uniformly than H.264 (UNVERIFIED; test before relying on it).

### Finding 2. Colour pipeline: consumer monitor to Rec.709 to projector to DCP

**What the standards say.**
- Rec.709 defines the camera-side transfer function and a limited range; the 10-bit limited-range code values run 64 to 940 for luma and 64 to 960 for chroma, and 0 to 3 and 1020 to 1023 are reserved [34].
- The display side is ITU-R BT.1886: a power function with exponent gamma 2.404 and a black-level lift, written for flat panels as a match to the legacy CRT; it also states that checking a display against it should be done in a dark room [35]. Rec.709 itself "does not specify a corresponding reference electro-optical transfer characteristic function" [34].
- Theatrical DCI-P3 uses a "simple 2.6 gamma curve"; its white point (x 0.314, y 0.351) is chosen to maximise xenon light output, and its blue primary matches Rec.709 [33]. A DCP stores X'Y'Z' (gamma 2.6) at 12 bits, with a 250 Mbit/s cap [31].

**What DCP-o-matic does with Rec.709 content** (from the authors' own paper) [22]:
1. Convert to linear RGB with a gamma curve (a pure power function or a modified one with a linear toe).
2. Multiply by a 3x3 matrix to XYZ. "These are the same for BT709 and sRGB, so the corresponding matrices are the same" (primaries R 0.64/0.33, G 0.30/0.60, B 0.15/0.06; white D65 x 0.3127, y 0.329).
3. Adjust the white point with a Bradford matrix.
4. Normalise: multiply by 48/52.37. (My reading: this places white at the DCI reference luminance of 48 cd/m2, which is 14 foot-lamberts. Inference.)
5. Apply gamma 1/2.6 to get non-linear XYZ.
The source preset list is: sRGB, Rec. 601, Rec. 709, Rec. 1886, Rec. 2020, S-Gamut3 and P3, plus Custom. The manual says the setting should be the colour space the content was "created or graded for" [12]. **Choose "Rec. 1886" if the grade was made on a gamma-2.4 display, "Rec. 709" otherwise; which gamma each preset applies is UNVERIFIED.** Compare the two on the preview against a known frame before committing. Range: choose Video (MPEG, 16-235) for the ProRes master; DCP-o-matic "usually guesses this correctly", so confirm [12]. Agent-pipeline pitfall 6 (Remotion output full-range and tagged bt470bg) is the case where the guess can be wrong [3].

**What this means in practice.**
- Because the conversion works in linear light, 100% Rec.709 content ends up inside the P3 gamut and the DCP carries no extra "look". The projector's own colour processing maps XYZ to its primaries [31][33]. You do not grade in P3 (inference).
- The surround matters more than the maths. A TV in a lit room, a projector in a hall with house lights low, and a dark cinema give three different effective contrasts. BT.1886's own note that the reference measurement belongs in a dark room [35] is the reason a one-grade-for-all result will shift.
- A consumer monitor is almost never calibrated to gamma 2.4, D65 and a dim surround. Without a probe, the maker cannot make a trustworthy absolute grade (inference). The agents generate colour by number (palettes sampled from prints, deterministic renders), so the safe approach is to keep values inside a conservative range and verify on the real screen.

**One grade, two trims (proposal, inference).**
- Master grade: Rec.709 / BT.1886, mid-key, no crushed blacks (keep shadows above code 20 to 24 on 8-bit limited range), no clipped whites (stay at or below 235 on 8-bit limited, 940 on 10-bit), skin tones checked against a known family photo.
- Trim V ("venue, lit room"): a small lookup table that lifts shadows by about 2 to 4 IRE and raises mid-gamma by about 0.05 to 0.10, applied only when exporting the venue screening file. Starting values; adjust only from the real screen.
- Trim C ("cinema, dark room"): identity at first. Adjust only after a real cinema test. DCP-o-matic does the colour conversion itself.
- Mechanism: a `.cube` lookup file applied at export with ffmpeg's `lut3d` filter (untested here); the master is never touched. Each trim file is hashed and logged.

**What to check on the real screen** (done with the venue test clip and the film's own first and last minutes):
- **Blacks:** the PLUGE bars; can you tell code 16, 20 and 24 apart? Do dark scenes show noise or crushing?
- **Whites and clipping:** a ramp up to 235; any flat patch at the top is clipping.
- **Skin:** a still of a real face in neutral light against the printed original.
- **Banding:** gradients in sky, vignettes and fades. Banding appears most when 10-bit sources go to 8-bit H.264. FFmpeg's scaler has dither options `auto`, `bayer`, `ed`, `a_dither`, `x_dither` [46]. The code-rendered gradients need dithering or fine grain at render time (inference). The DCP is 12-bit and shows less of it, but only if the intermediates were 10-bit or better [31].
- **HDR:** off on the TV and in Windows. Microsoft states that "All standard dynamic range (SDR) content and apps appear too bright or too dark" on some HDR-capable displays, and that HDR may turn itself off when a laptop is unplugged [42].
- **Picture mode:** a film/cinema/movie mode with motion smoothing, noise reduction and overscan off [40][45]. Names vary by maker (UNVERIFIED).

### Finding 3. Audio and captions

**Formats and layouts.**
- DCP audio is linear PCM, 24-bit, 48,000 or 96,000 samples per second, up to 16 channels [31]. The verifier raises an error if "the audio bit depth" is not 24 [18]. DCP-o-matic requires an even channel count; unused channels are filled with silence [15].
- ISDCF's channel order: 1 L, 2 R, 3 C, 4 LFE, 5 Ls, 6 Rs, 7 HI, 8 VI-N. "Not all channels need to be present in a given DCP" and "In all cases, an even number of channels shall be used" [28]. DCP-o-matic's audio map copies stereo to L and R [13].
- **Recommendation:** deliver stereo (L/R) now. For a later cinema screening, voices in a stereo mix sit as a phantom centre between widely spaced screen speakers, which is weaker for intelligibility; a 5.1 fold-up with voices in the centre channel is the better cinema version (inference). So the music-sound track should keep dialogue, music and effects stems.
- Gain in DCP-o-matic is per channel in dB, delay in either direction [13]. Mixing channels needs about -6 dB on each to prevent clipping [13].

**Loudness practice, by setting.**

| Setting | What the sources say | Practice for this film |
|---|---|---|
| Cinema (DCP) | No LUFS target for features. The aim is a calibrated room where the level is set by the mixer: "a correctly aligned theatre playing a movie at fader 7 will reproduce the level heard by the director and mixer"; lowering faders "from reference 7 to 6, 5 or even 4 1/2" gives "severe dialog intelligibility problems". Trailers are held to 85 dB Leq(m) (TASA), features are deliberately unregulated; no metric has "absolute value" [30]. The standard reference calibration (85 dB SPL per channel, pink noise at -20 dBFS, SMPTE RP 200) is background knowledge only, UNVERIFIED this round. Typical dialogue levels in finished DCPs: no source found this round (my recollection that theatrical mixes often sit near -27 LKFS dialogue-gated is background knowledge, UNVERIFIED) | Do not normalise. Keep a cinema mix with headroom and real dynamics, report its LUFS for information only, and let a cinema technician align the room |
| Broadcast | EBU R128: programme loudness target -23.0 LUFS (tolerance +/-0.5, +/-1.0 for live), true peak not above -1 dBTP, measured to ITU-R BS.1770 [36]. R128 is for broadcast programme normalisation (inference from its scope) | Not a target for cinema or the venue |
| Venue PA | Unknown until tested. toolchain Step 10 uses `loudnorm I=-16:TP=-1.5:LRA=11` and notes that small projector-room speakers may need more level [2] | Start the venue mix at about -16 LUFS integrated, -1 dBTP; check intelligibility in the back row with the oldest listener (surprise-ops already asks for a hard-of-hearing listener [5]); never trust the number over the room |
| Online | Streaming services normalise: Wikipedia lists YouTube at -14 LUFS, Spotify -14, Apple Music -16, and notes that Amazon, Tidal and YouTube "do not increase the volume of tracks" [38] (secondary). AES TD1004.1.15-10 (a -16 LKFS recommendation) was not readable on 2026-10-18 (403), UNVERIFIED | A -16 LUFS online mix. A quiet cinema mix posted online would play quietly, so do not reuse it |

**Checks (syntax run in the container; values from test tones only).**
`ffmpeg -nostats -i in.wav -af ebur128=peak=true -f null -` prints integrated loudness and peak. A mono-fold test measures the same file after `-af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true"`; a drop of more than about 3 LU against the stereo reading flags phase trouble that would bite on a mono venue PA (the threshold is my rule of thumb, inference).

**Captions.**
- **Burned-in open captions are the default** for the venue file and for a first DCP to an unknown cinema. DCP-o-matic lists three ways to add subtitles to a DCP: a small version-file (VF) DCP ("usually the best option"), projector-rendered subtitles ("mostly works well but is not 100% reliable"), and burnt-in subtitles (slower, but less likely to fail with unusual positioning or character sets) [20].
- **DCP subtitle tracks.** DCP-o-matic reads SubRip (`.srt`) and SubStation Alpha and can burn in with a checkbox, or leave the projector to render; it adds that open subtitles are visible to everyone and closed captions go to personal devices and cannot be burnt in [14]. ISDCF: most, if not all, projectors and servers support open subtitles and open captions [29]. Interop subtitles are an XML file that "cannot be encrypted" and need a special directory structure; SMPTE subtitles are an MXF file with no special structure and support encryption [27]. DCP-o-matic says to choose SMPTE "if in doubt", and the command-line default is SMPTE [15][21]. For a later festival: Sundance requires a DCP with both a Closed Caption and an Open Caption version, plus English SDH subtitles for non-English films [88].
- **Sidecars.** Keep `.srt` and `.vtt` for archive and online [2][4].
- **Fonts.** Microsoft states Windows fonts may be used to produce "captions and text included in videos" provided the text "is rendered as a bitmap image, and the font files themselves are not embedded within the video file" [76]. An SMPTE subtitle track carries a font (the verifier checks `LoadFont`) [18], so for any DCP subtitle track use an SIL OFL font: output is unrestricted ("video titling" is listed) and an embedded font may be subset [75].
- **Size and safe area (TV at three metres).** format.md's rule is line height 7 to 8% of picture height, with `FontSize=23` in ffmpeg's subtitles filter giving about 8.0% at 1080p, tested on the venue screen from three metres [4]. EBU R95 gives a graphics-safe area of 5% and an action-safe area of 3.5% at each edge; on 1920x1080 that is 96 px and 54 px for text, 67 px for action horizontally [37]. Keep burned-in text inside the 90% by 90% central box, at most two lines, 42 characters or fewer a line, and under 20 characters per second (format.md, from Netflix's timed-text guide [4]). The DCP verifier warns above 3 lines or 52 characters per line [18].
- **Size on a cinema screen (computed, inference).** A 10 m wide Flat screen is about 5.4 m tall. An 8% line is 43 cm high, seen from 12 m as about 2.0 degrees; a 55-inch TV (68 cm tall) at 3 m shows an 8% line as about 1.0 degree. So the same percentage is twice as large to a cinema audience. For a later cinema burn, 5.5 to 6% (1.4 degrees) is a reasonable start; keep captions out of the bottom 8 to 10% where heads may block the view (inference). Do not bury captions in the black side bars of a Flat container.
- **Cinema title sizes.** Keep titles inside the same 5% graphics-safe box and test on the real screen; venue masking can crop edges.

### Finding 4. DCP-o-matic: version, workflow, encode time, verification, testing, failures

**Version and licence on the date.** Stable **2.18.51, released 16 October 2026**; builds for Windows 64-bit and 32-bit, macOS, Linux (AppImage and distribution packages) [8]. Licence: "free and open-source and is licensed under the GNU GPL" (the linked text is version 2.0) [10]. GPL covers the software; it does not govern the DCPs it outputs (inference).

**Tools in the suite:** create DCPs from video, audio, subtitle and closed-caption files; play and verify DCPs; create KDMs; write cinema-format drives; combine and edit DCPs [23]. Command-line: `dcpomatic2_create` (builds a film from files; options include `--container-ratio`, `-f/--dcp-frame-rate`, `--twok`/`--fourk`, `--standard` SMPTE or interop (default SMPTE), `-a/--audio-channels`, `--encrypt/--no-encrypt`, `--no-use-isdcf-name`, `--video-bit-rate` in Mbit/s, `-o`) and `dcpomatic2_cli` (runs the transcode) [21]. Option names are from the manual; I did not run them (UNTESTED).

**Workflow from the ProRes master (GUI steps, with the CLI equivalents in brackets).**
1. New film; name it with the neutral code name (the DCP title shows on cinema servers and in KDMs/CPLs, so it must not carry her name before the reveal) [5].
2. Add the ProRes `.mov` as content (DCP-o-matic decodes through FFmpeg; ProRes reading is expected to work but is UNVERIFIED, test in December).
3. DCP tab: Container Flat (1.85); Resolution 2K; Frame rate 24; Audio channels 6 (the default) with L and R only mapped, or 2 if the target allows (check what the generated ISDCF name says, e.g. "20" versus "51": UNVERIFIED); Standard SMPTE; Encryption off; JPEG2000 bandwidth 100 to 125 Mbit/s ("Most commercial DCPs use bit rates between 75 and 125"); Reels: single reel; "Use ISDCF name" ticked; Content type "feature" for a feature (a "short" type is an ISDCF label, verify in the dialog) [15].
4. Video tab: colour preset (Rec. 1886 or Rec. 709), Range Video, scale to fit [12]. Audio tab: map L to L and R to R at unity gain [13]. Timed text: leave empty if captions are burned into the master; otherwise add the SRT and tick "Burn subtitles into image" [14].
5. Make DCP. DCP-o-matic checks the film first and shows hints; encoding can take many hours [11].
6. Verify (below), play in the Player, hash the folder, copy to the delivery drive.

**Encrypted or not.** Unencrypted means no KDM. The manual says whether encryption suits a project "is a tricky one": unencrypted lets anyone "take it and do whatever they want", encrypted means the cinema cannot show it without the right KDM, and KDM problems often surface close to showtime [19]. For one family film, unencrypted is the low-risk choice. (Sundance accepts encrypted DCPs only with "open keys" valid through the festival [88].)

**JPEG2000 bandwidth and size.** 50 to 250 Mbit/s adjustable [15]. The verifier errors above the equivalent of 250 Mbit/s in a frame and warns above 230 [18]. Computed picture size: 75 Mbit/s is 0.56 GB per finished minute, 125 Mbit/s is 0.94 GB, 250 Mbit/s is 1.88 GB. A 10-minute film is 5.6, 9.4 or 18.8 GB; a 20-minute film is 11.2, 18.8 or 37.5 GB. Film grain and noise push frames toward the cap, so grain costs bits (measured effect on speed below).

**Encode time per finished minute (measured, proxy).** ffmpeg 6.1.1 with the OpenJPEG wrapper (`-c:v libopenjpeg -cinema_mode 2k_24`), RGB converted to XYZ 12-bit, written to null, on the container's 4 vCPU Intel Xeon at 2.1 GHz [47]:

| Test | Frames | Wall | Frames per second | CPU-seconds per frame |
|---|---|---|---|---|
| 1998x1080, clean synthetic | 36 | 4.5 s | 8.0 | 0.44 |
| 1998x1080, clean synthetic | 72 | 12.0 s | 6.0 | 0.46 |
| 1998x1080 with heavy temporal noise | 72 | 35.7 s | 2.0 | 1.61 |
| 3996x2160, clean synthetic | 36 | 16.5 s | 2.2 | 1.33 |

At 1440 frames per finished minute this is about 3.0 to 4.0 wall minutes per minute (clean) and about 12 (noisy). A 10-minute film: about 30 to 40 minutes clean, about 2 hours noisy. A 20-minute film: about 1 to 1.3 hours clean, about 4 hours noisy. A newer 8-core PC could be 2 to 4 times faster (UNVERIFIED). Caveats: this is the ffmpeg wrapper, not DCP-o-matic's own encoder; the content is synthetic; another agent shared the CPU. DCP-o-matic can resume interrupted encodes (it keeps an `info` file of frames written) [21], spread work over several machines [21], and sets threads to the number of cores [21].

**Can the cloud container do it?** Compute: yes in principle, within the 2-hour background-job cap for a 10-minute clean film; a grainy 20-minute film would not fit in one job. Disk: no. The container's root disk was at 100% with about 140 to 290 MB free during my tests, and it is temporary [1][47]. **Plan:** encode the real DCP on the Windows PC (overnight), with a small test DCP in the cloud only if disk allows. The charter's reason for avoiding the Claude desktop app is memory; JPEG2000 encoding is CPU-bound, but DCP-o-matic's memory use on Windows is UNVERIFIED.

**Verification.**
- DCP-o-matic Player: Tools > Verify DCP reports Errors, Bv2.1 errors and Warnings, plus things that passed [18]. Errors include hash mismatches (CPL/PKL vs files), missing files, SMPTE and Interop mixed, invalid XML, missing asset map, audio bit depth not 24, picture frames over the 250 Mbit/s equivalent, sound assets with different channel counts, subtitle font problems [18]. Warnings include a first subtitle before 4 s into reel 1, subtitle lines over 52 characters, more than 3 lines, missing FFOC/LFOC markers, and JPEG2000 frames over 230 Mbit/s [18].
- The Player decodes at reduced resolution on slow computers, and the manual warns that full-resolution playback needs a very fast CPU, its advanced presentation mode "is not widely tested", and "I would not advise depending on it without plenty of testing" [17]. So the Player proves the DCP is well-formed; it does not prove a cinema will accept it.
- Own checks: SHA-256 manifest of the DCP folder, copied to the delivery drive and re-checked from the drive (toolchain's `mk_manifest.ps1` pattern [4]); `ffprobe` on the source. The verifier does a hash check against the PKL, but a copy made later still needs your own hash.

**Delivery media.** The only file system the manual guarantees in all cinemas is ext2; Windows and macOS need extra software, so use DCP-o-matic's Disk Writer to format and copy; network transfer is the manual's first suggestion [19]. ISDCF Doc 3: assume a USB 2.0 type A socket on the ingest device; MBR partition table with one primary partition (type 0x83); ext3 or ext2 with a 128-byte inode (`mkfs -t ext3 -I 128 -m 0`); read permission for "other"; and "it is not safe to connect a device containing a DCP to general purpose computer running many common consumer operating systems" because they may reformat or damage an unrecognised disk [26]. Label the drive "Do not read with a consumer computer". DCP-o-matic also notes the FAT32 4 GB file limit as a reason to split reels [15]; FAT32's maximum file is 4 GiB minus 1 byte [44].

**How to test without a cinema.**
1. Verify and play in the Player on your PC (above).
2. A real projectionist test. Cinemas that rent screens: Picturehouse (UK) lists screen hire packages that include a one-hour tech rehearsal, handheld microphones and technical support, most screens in Flat and Scope, some with Dolby Atmos; no prices on the page [89]. Everyman (UK): private hire where you can show "your own content"; prices and formats not stated [90]. Cinemark (US): a Private Events page that mentions "a private screening of your film" for "Filmmakers and independent studios"; prices and formats not stated [91]. **Typical hire cost: not found; request quotes (UNVERIFIED).** Ask: do you accept a DCP on ext2/ext3 or by download; do you accept HDMI, ProRes or MP4; is a test slot included; what insurance do you need (enquiry questions in Templates 2b).
3. Other test routes (not sourced, ask locally): a film club, university screening room, community cinema, or a post-production house with a DCP server.

**Five most common DCP failures at ingest** (ranked by my judgment from these sources; no ingest-failure statistics were found, so the ranking is UNVERIFIED).
1. **Wrong drive format or partitioning** (NTFS/exFAT/GPT instead of MBR plus ext2/ext3 with a 128-byte inode) [19][26].
2. **Corrupt or incomplete copy** (hash mismatch, missing file, consumer OS rewriting the disk) [18][26].
3. **Standard and subtitle problems** (Interop versus SMPTE mixed; subtitle fonts or positions the projector renders differently; early first subtitle) [18][20][27].
4. **Encryption and KDM** (wrong certificate or date window; problems tend to appear close to showtime) [19]. Avoided by shipping unencrypted.
5. **Capability mismatch** (frame rate other than 24 on an older projector; odd audio channel count; bit rate above 250 Mbit/s) [15][16][18].

### Finding 5. Venue playback: checklist, Windows laptop, USB, audio routing, backups, rehearsal

The checklist items below are my synthesis. Facts that have a source carry a citation; everything else is practice to confirm at the venue.

**TV**
- Picture mode: cinema/film/movie; motion smoothing off [40]; noise reduction off; overscan off ("just scan", "screen fit" or "full pixel", names vary) because "it is undesirable for digital flat panels" and "many LCD TVs still come with overscan enabled by default" [45]; HDR off (Finding 2); energy saver and auto-dimming off.
- Input: set the HDMI input to "PC" or "game" mode to keep 4:4:4 and low latency if available (UNVERIFIED); 1920x1080 at 24 or 60 Hz.
- USB playback: FAT32 caps a file at 4 GiB minus 1 byte [44]; exFAT is "supported in a number of media devices such as modern flat-panel TVs" but is not universal, because licensing "inhibited exFAT's adoption as a universal exchange format" [43]. Whether this TV takes exFAT, MKV or soft subtitles is still unknown (toolchain's open item [2]); keep captions burned in and the container MP4/H.264, and test.
- Sound: HDMI to the TV speakers is rarely enough for a room; see audio routing.

**Projector**
- Native resolution and aspect (1080p or WUXGA 16:10, which letterboxes 16:9), keystone and lens shift set once, warm-up time, lamp or laser hours, eco mode off, screen gain and ambient light (lights low, not dark, per surprise-ops [5]).
- Cable: short, good HDMI, tested; keep an adapter kit (USB-C, DisplayPort, mini-HDMI).
- EDID handshake: connect and power on in the order that worked in rehearsal; write it on the run sheet.

**LED wall** (questions for the operator; nothing sourced)
- Native pixel resolution and aspect ratio of the wall and of the processor's input; whether the processor scales 16:9 into the wall or crops; accepted frame rates; brightness setting (indoor walls are often far brighter than a TV, so reduce it); colour temperature and gamma; whether the operator controls a "play" source; where the audio comes from (the wall has none). Ask for a test pattern at the wall's native size.

**Windows laptop** (maker's PC)
- Plug in the charger; power mode best performance; screen and sleep timers never; Night light off; HDR off [42]; Notifications off with Do Not Disturb on [5]; Windows updates paused for the week; close mail, chat, cloud sync (surprise-ops G [5]); neutral desktop; Explorer preview and "Recent" lists cleaned.
- Display: Win+P (duplicate or second-screen-only) with the output at 1920x1080; refresh rate chosen to suit 24 fps (24, 48, 72 or 120 Hz if offered; otherwise 60 Hz judders [39]); scaling 100%. The exact Settings path is UNVERIFIED (the Microsoft page I tried returned 404).
- Player: a full-screen player (VLC or mpv) with the file loaded and paused on the first frame. With mpv, hardware decoding is not enabled by default ("to keep the out-of-the-box configuration as reliable as possible"); use `hwdec=auto` after proving it on this laptop, and consider `video-sync=display-resample`, which needs constant frame rate and can skip frames if you toggle fullscreen or resize mid-playback [41]. So go fullscreen first, then play.
- Audio: pick the HDMI or headphone output; set the default format to 48 kHz 24-bit so Windows does not resample (inference); turn off audio "enhancements".
- Two laptops, one file each, identical paths.

**Audio routing**
- HDMI to TV, projector or AV receiver (the receiver or soundbar may add its own processing; set it to stereo, dialogue-enhancement off).
- 3.5 mm to a venue mixer: use a stereo-to-two-channel DI box or lead; set the channel gain with the test clip's 1 kHz tone; watch for ground-loop hum; **many venue systems sum to mono, so do the mono-fold check (Finding 3)**.
- Ask who controls the venue fader; the venue PA stays an unknown until it is tested.
- Know where to put a microphone for the brief welcome (surprise-ops: MAKER speaks 30 to 60 seconds [5]).

**Backup ladder** (extends surprise-ops' ladder [5])
1. Laptop playing the screening file.
2. Second laptop with the same file.
3. USB stick straight into the TV or projector media player (needs the exFAT/MP4 test).
4. Phone by cable or cast.
5. The 3-minute audio or still version.
6. A postponed private evening, said plainly.
Keep two USB sticks in different pockets, a spare HDMI cable, the charger, a USB-C hub, and a printed running order [4][5]. A cloud copy only with the maker's explicit yes [1][4].

**Tech rehearsal protocol** (slots into surprise-ops' dates [5]; run-sheet lines are in Templates)
1. Neutral test clip first, with the venue's AV person present (no personal content).
2. Then the film itself only when the room is empty or only the maker is present (surprise).
3. Play the first 5 and last 5 minutes and three spot sections; the full run Monday 22 February; cold start #1 Thursday 25 February; cold start #2 Friday 26 February.
4. Walk the failure ladder rungs 1 to 4 once each, with a stopwatch.
5. Record settings (screenshots of TV menus and Windows display/sound) and photograph the cable layout.
6. Pass or fail gate G6b: the film plays start to finish at the right levels; captions legible from the back row; no overscan crop; black and white checks pass; sound intelligible; mono-fold OK; cold start under 2 minutes; backups verified.

### Finding 6. Rights by category (who owns what; gathering versus cinema versus online)

**Frame.** *Jurisdiction not yet known; confirm; not legal advice.* The tiers used below follow surprise-ops' shared and private cuts [5]:

- **T1, private cut:** the longer version handed to her alone.
- **T2, the 27 February public gathering:** free, no sponsor, size and door policy not yet known ("mostly public") [1].
- **T3, online link:** a private or unlisted link, later.
- **T4, cinema, festival or any commercial or ticketed showing.**

Two framing facts. First, "free" and "family" do not clear anything at T2. US law treats a showing as public at "a place open to the public or at any place where a substantial number of persons outside of a normal circle of a family and its social acquaintances is gathered" [56]. (UK, EU and India have their own tests; not fetched. India's s.52 has a narrow carve-out for performances in "bona fide religious ceremony" including marriage festivities, which does not obviously cover a tribute screening [70].) Second, platform and licensor terms can treat free sharing as commercial: Minecraft's own text does (Finding 7) [48].

**What family-film and personal-documentary makers actually do.** I found no survey or published practice for family films. What the documentary-practice sources show is a risk ladder, which I adopt (this is my synthesis, not survey data): **Ask** the owner or person; **Document** (written or recorded yes, or a dated decision); **Substitute** (licensed or original asset, a cropped or stylised version, an object instead of a face); or **Accept a documented risk** with reasons, reversibility and who is exposed. Sources behind it: written releases are best practice but "a well-considered verbal release is better than nothing" [79]; insurers expect written releases for recognisable living people, permissions from copyright owners, and for fair-use claims "a fair use opinion letter from an experienced clearance attorney" [77]; best-practice statements accept fair use in narrow documentary situations and say a failed attempt to clear does not defeat a fair-use claim [58].

#### 6.1 Music: the exhibition layer (music-sound owns the detail)

- **Two rights in one recording.** The publisher controls the composition (sync licence); the label controls the recording (master use licence); they are different owners [82]. Both are needed to put a commercial recording in a film. **A "public performance" licence is a third right** (US: ASCAP, BMI, SESAC [82]; UK: PRS and PPL; India: IPRS; names beyond the US are background knowledge, UNVERIFIED). A venue's blanket licence, where one exists, normally covers performance of the societies' repertoire at that venue, **not** copying a recording into your film (sync/master) (background; ASCAP and BMI pages returned 403, UNVERIFIED).
- **US exemption not to lean on.** 17 U.S.C. 110(4) exempts performing a nondramatic musical work "without any purpose of direct or indirect commercial advantage" and with no fee to performers, promoters or organisers; with an admission charge the proceeds must go "exclusively" to educational, religious or charitable purposes, and the owner can object in writing at least 7 days before. It deals with performance, not reproduction, and the text I read does not say whether it covers a soundtrack inside a film [57]. Do not rely on it (inference).
- **T2 (public gathering):** any commercial recording copied into the film needs sync plus master permission even if nothing is charged. Safe options in order (toolchain Decision 6 [2], IDA [82]): CC0 or CC BY music with credit (not NC); production music licensed for events or public performance; original or own-performed music; a licensed substitute with a similar mood. For her favourite songs: ask the rights holders for a one-event licence (fee UNVERIFIED), substitute, or keep the song out of the film and play it on the venue's system at the party (ask the venue whether its licence covers that; UNVERIFIED).
- **T3 (online):** sync and master with online scope; platform detection (YouTube) can block or mute commercial songs (toolchain Decision 6, format Decision 12 [2][4]).
- **T4 (cinema, festival):** a festival licence is the cheapest (one to two years, territory-limited) but other rights must be cleared later; all-media, worldwide, perpetual is the most expensive and usually needed for theatrical release; "There are no gray areas" (you hold written permission or you do not) [82]. E&O needs music cleared [77]. Sundance accepts temp music at submission if it is listed on screen before the film, and requires accepted films to sign a waiver that nothing infringes [88].
- **Cue sheet fields** (industry-standard fields from background knowledge; confirm with the relevant society's form): cue number, title, composer(s), publisher(s), society affiliation, recording artist and label if a recording, usage type (background instrumental, visual vocal, theme), time in and out, duration. The log in Templates carries these as columns music-sound fills.

#### 6.2 Photographs taken by others (studio, wedding, school, relatives, friends)

- **Who owns.** The person who took it, unless assigned or made as an employee. UK CDPA s.9(1): the author is "the person who creates it" [59]. India: the author of a photograph is "the person taking the photograph" (s.2(d)(iv)), but s.17(b) as printed in the Act copy I read says that for a photograph "taken ... for valuable consideration at the instance of any person, such person shall, in the absence of any agreement to the contrary, be the first owner" [70]. So in India a family that paid for a wedding photographer may own the picture, unlike the US or UK; confirm against the current text because I read a government-hosted consolidated copy of unknown date (UNVERIFIED). US ownership by the photographer is background knowledge (UNVERIFIED). Being in a photograph does not make the sitter its owner.
- **Practical sort.** (a) Taken by relatives or friends: they are contributors; ask them; low exposure. (b) Studio, wedding or school photographer: look for stamps on the print back; check any print-release wording; ask the studio if it exists. (c) Unknown photographer: treat as an orphan work (below). (d) Photos the maker took: fine.
- **Orphan works.** US: no safe harbour. The Copyright Office's 2015 report says "anyone using an orphan work does so under a legal cloud" and recommended limiting remedies for a good-faith diligent search; I found no sign it was enacted (UNVERIFIED for 2026) [54]. UK: the IPO licensing scheme. UK IPO application fee £20 for one work, £24 for two, £30 for five, £40 for ten, £60 for twenty, £80 for thirty; non-refundable; a separate licence fee is payable only if the licence is granted; licence up to 7 years; UK use only; film and photographs are covered; page updated 1 Dec 2025, read 2026-10-18 [62]. A diligent-search checklist is required [62]. EU: the 2012 directive allows only libraries, schools, museums, archives, film or audio heritage institutions and public broadcasters, for public-interest missions [63]. India: s.31A is a compulsory licence from the Appellate Board where the author is "dead or unknown or cannot be traced", after a newspaper notice [70].
- **Fair use and stills.** US fair use has four factors and "no formula" or safe percentage [55]. IDA: "Still photographs in particular do not lend themselves to fair use treatment" and the creator-as-owner point holds for amateur material [80]. The documentary "historical sequences" principle (no suitable substitute, cannot be licensed or only on excessive terms) is narrow [58]. Do not build a plan on fair use for other people's photographs (inference).
- **Act:** record photographer, provenance and permission for every photo in the manifest (ai-imagery's `manifest.csv` has a `consent_note` column [6]); for unknown photographers record the search done (stamps, family asking, dates) before choosing substitute or accept-risk.

#### 6.3 Archival and news footage

- **Costs and structure.** Archives price by media, territory and term; "worldwide rights usually cost more than domestic rights", exclusive and one-of-a-kind material costs more, and short licences cost more to replace later [81]. Festival-only licences are cheaper [82]. No per-second price was readable (British Pathe returned 403; UNVERIFIED).
- **US fair use versus UK and India fair dealing.** US: case-by-case four factors [55]. UK: fair dealing for criticism, review or quotation "for any type of copyright work" with "sufficient acknowledgement", and a test of "how would a fair-minded and honest person have dealt with the work?" [61]. EU: Member States may allow quotation, incidental inclusion and parody, subject to a three-step test [64]. India s.52(1)(a): fair dealing for private or personal use, criticism or review, and reporting current events; s.52(1)(u)(ii): inclusion of an artistic work in a film "only by way of background or ... incidental" [70]. Public-domain status turns on country and date; the IDA primer is a US guide [83]. (UK and India are not "fair use"; do not import a US argument.)
- **Practice for a life film:** use period footage sparingly; prefer public-domain or federal-government material, a licensed few seconds, a stylised reconstruction labelled L5 [6], or a still or object (substitute). Any accepted fair-use reliance gets a written note with the four factors.

#### 6.4 Fonts

- Fonts in Windows may be used in videos if the text is bitmap-rendered and the font file is not embedded in the video [76]. Do not embed Windows fonts in a DCP subtitle track or in an app; do not convert them [76].
- SIL OFL: output is unrestricted; "video titling" is listed; keep the licence and notices if redistributing the font; embedding in a document is allowed in full or as a subset [75]. Prefer OFL fonts for titles, captions and any DCP subtitle track.
- Other fonts (bundled with apps, free-for-personal-use fonts, Adobe or Monotype): read the video, broadcast and event terms; some free fonts are more restrictive than Windows fonts [76]. Log font, source, licence file and how it appears (rasterised or embedded).

#### 6.5 Likeness, voice and name; minors; the dead; the estranged

- **US (state law, varies).** Right of publicity is "primarily governed by state (as opposed to federal) law"; California extends post-mortem rights to 70 years, Indiana 100, Tennessee without expiry while use continues [71]. Newsworthy, expressive and documentary uses are often protected by the First Amendment, but not always for performances (Zacchini) [71][79]. Digital replicas: the Copyright Office's Part 1 report (31 July 2024) recommends a federal law [52]. A life-story film about a private person made with family cooperation is lower risk than commercial use, but jurisdiction decides; confirm which state.
- **UK.** I found no UK image-right source (UNVERIFIED); background: no general image right, but privacy and data-protection law apply to photographs and voices. **EU.** GDPR's household exemption is for "a purely personal or household activity" [67]; a public screening is outside it (inference, recital text not read). Germany (my translation of the German text): images may be distributed or publicly displayed only with the consent of the person depicted (consent presumed if paid), and for 10 years after death the consent of close relatives is needed (§22); exceptions for contemporary history, persons incidental to a place, assemblies and art not made to order, but not where the depicted person's (or relatives') legitimate interest is violated (§23) [68][69]. France: Civil Code art. 9 (privacy) [71]. **India.** Personality-rights protection is developing through the Delhi High Court (2025 to 2026 cases about AI misuse, from a secondary source) [71]; data-protection law (DPDP Act 2023) was not read (UNVERIFIED).
- **Minors.** A release for a minor needs a parent or guardian's signature; without it the release "may afford no legal protection to the publisher" [86]. surprise-ops: under 14, guardian present and one question; 14 to 17, guardian consent and a written release [5]. Public cut: no identifiable minor without guardian consent; adults who appeared as children in old photos can be asked now as adults.
- **The dead.** Germany: relatives' consent for 10 years [68]; California: 70 years [71]; UK, India: UNVERIFIED. Charter and ai-imagery: no motion on faces of the dead without the family's say, no synthetic voices [1][6]. surprise-ops: culture may bar images, voices or names of the dead [5]. Practice: ask the closest family and record the answer; substitute an object, place or still.
- **The estranged.** No legal test; the ethical default (surprise-ops) is out or a neutral past image if she would tell that story herself; never staged reconciliation [5]. With no proxy available, default to OUT.
- **Voice and name.** A voice is both likeness and personal data; use only recorded consent; no cloned voices [1]. A first name or "Grandma" is usually lower risk than a full name with a dated allegation.

#### 6.6 Brands, games and logos

See Finding 7. In stylised redraws of real photos, remove or change legible logos and brand packaging unless incidental; in code-built scenes use original shapes (inference).

### Finding 7. Minecraft (and other games): re-read on 2026-10-18 and diff

**Method.** I fetched the Usage Guidelines page and the EULA by curl over HTTP/1.1 at about 07:00 GMT on 2026-10-18 (both HTTP 200). I ran `research/sources/check_mojang_quotes.py` (the comparable-hash method from games.md G5 [7]) on my copy and on two earlier same-day captures held in the shared scratchpad (about 02:38 and 04:48 GMT) [48].

**Diff result.**
- All 12 tracked quotes: **PRESENT** (personal use; sharing equals commercial; physical-locations bullet and both examples; free to view; no selling copies; credits outside game content; 150 participants; no profit sponsors; name not the title; change clause).
- Extracted-text hash, identical in all three captures: `c5a8253c842dfe436b058295a5b09a7e26ecb1c85b53e1b17c84300253b94222` (37,148 characters). **So the guidelines text did not change between those captures.** Raw-HTML hashes differ between fetches because the page has dynamic parts, as the earlier excerpt warned [7]. The two hashes in the 2026-10-18 excerpt file came from different extraction methods and are not comparable.
- The page still shows no visible revision date. The EULA (first read for this track; no baseline): extracted text 16,687 characters, hash `2ff38e065ac43f9e5ea26c778d9ba8667228e53c7d6e52961f14e5273f5c42e1` [49]. I saved a short dated excerpt of both as `research/sources/minecraft-eula-and-extra-clauses-2026-10-18.txt`.

**Clauses in today's text that the earlier excerpt did not record** (short verbatim quotes) [48][49]:
- "All permissions and consents are given by us at our discretion and may be revoked at any time".
- Live in-game events must "Obtain permissions and clearances from the owners of any intellectual property (for example: music, brands, products, celebrities, performers)".
- "Clips of gameplay could be used as reference material if the subject is not the gameplay itself".
- In-person events: "You make it clear that you (not us) are responsible for anything that happens"; "Do not use official Minecraft brand or assets on your marketing materials"; the Minecraft name only "in a secondary name, secondary title, or description".
- Disclaimer text: "NOT AN OFFICIAL MINECRAFT [PRODUCT/SERVICE/EVENT/etc.]. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT" to be included "prominently".
- "In general You may do things that are specifically covered by the fair dealing or fair use exceptions to copyright and trademark laws."
- The allowances "do not authorize commercial companies, corporate brands, advertising agencies, non-profits, politicians ... to use or exploit Minecraft for promoting products, services, or agendas unrelated to Minecraft".
- "Assets" means "the code, software, graphics, textures, images, models, sounds and other audio from any of our games and any videos or screenshots taken from our games".
- EULA: "Do not distribute or make commercial use of anything we've made without our permission"; "distribute" includes "give copies of our game software or content to anyone else"; the Usage Guidelines are "extra permissions" they "reserve the right to change ... or withdraw"; "a single Minecraft block (including its textures and its 'look and feel') - we own that; your creation of a Gothic Cathedral with a rollercoaster running through it - we don't own that".

**What this allows, by setting** (reading of the text, not legal advice; Mojang says it cannot advise on a specific project [7]; the guidelines "do not form part of the policies" [48]):

| Use | Free, non-sponsored gathering of about 150 or fewer | Cinema (hired) | Online link |
|---|---|---|---|
| No Mojang name, textures, models, sounds or footage (original voxel assets) | Nothing to clear from Mojang; "Minecraft" may appear only as a secondary description, with the disclaimer if used | Same | Same |
| Minecraft footage or screenshots in the film | Not cleared. Shared "with others" counts as commercial use even free [48]. The physical-locations bullet gives two examples (promoting big-screen gameplay in a commercial venue; charging money in theatres) and a free hall is neither, but "publicly" and "physical locations" are undefined | Free hire: same ambiguity, same venue type as the explicit "not allowed" example. Ticketed: explicitly the "not allowed" case; also "All videos ... free to view" and "You don't sell copies" | The guidelines allow gameplay videos online if free to view and with unique content; our film is not a gameplay video, and sharing still counts as commercial |
| "Minecraft" in the title | Not as primary or dominant name [48] | Same | Same |
| Textures, mobs, UI (hotbar, hearts, achievements) | Avoid: brand and assets [48][7] | Avoid | Avoid |
| The 150-person line | A yardstick, not our trigger: written for community meet-ups; "events with more than 150 participants tend to be commercialized and sponsored" [48] | n/a | n/a |

**Recommended default (unchanged).** Original voxel assets built in MagicaVoxel or Blockbench, "Minecraft" by reference only (never the title), no Mojang textures, sounds or UI, and the disclaimer line in the credits if the name appears [7]. **What would unlock real footage:** written permission through Mojang's partnership-proposal route named on the page [48], or a decision to keep Minecraft footage out of the shared cut and in the private cut for her alone (still "sharing"; a documented risk, not a clearance). The EULA's "Your Content remains Your Content" supports original builds, not Mojang's textures or block look [49].

**Premiere-week routine.** Save the page (curl over HTTP/1.1), run `python -I check_mojang_quotes.py PAGE.html`, and compare the extract hash with `c5a8253c...94222`. Run on **Mon 15 Feb 2027** (after the Sat 6 Feb picture lock, before the Fri 19 Feb withdrawals close) and again **Fri 26 Feb** (cold start #2). Any MISSING quote or new hash means read the diff before the show. Re-save the dated excerpt.

**Other games (strict lead: Nintendo).** Nintendo's "Game Content Guidelines for Online Video & Image Sharing Platforms" (published 29 Nov 2018, updated 2 Sep 2024) cover online sharing by "individual consumers"; "Videos and images that contain mere copies of Nintendo Game Content without creative input or commentary are not permitted"; "other forms of monetization ... for commercial purposes are not permitted"; the guidelines "only cover the sharing of Nintendo Game Content on appropriate video and image sharing sites"; other uses "are subject to the relevant laws" and Nintendo cannot provide legal advice [50]. A public screening is not addressed, so treat it as not permitted without Nintendo's agreement. Microsoft's Game Content Usage Rules (last updated January 2015) cover Microsoft-published games and say "The only exception is Minecraft, which has its own guidelines"; use is limited to personal, non-commercial purposes, with videos and streams allowed on YouTube or Twitch [51]. **Default: no third-party game footage, characters, music or sounds in the film.** If a game was part of the family's texture, show it as an object, a drawing or her own words (inference).

### Finding 8. Releases versus the surprise

**The paradox.** A public screening wants releases from everyone who appears; asking for them reveals the film. The earlier consent card in surprise-ops says "a film that family will watch together, and a longer private version given to [NAME]" and promises not to share "more widely without asking you again" [5]. With a mostly public premiere [1] the first phrase is no longer true, and the surprise-ops rule is that you may omit but may not state anything untrue, and "Do not read this card until the bracketed line is true" [5]. **Delta for surprise-ops: update the card (Templates, 4a).**

**Resolution in three stages.**
1. **Now to picture lock: ask only what can be asked truthfully, tell contributors the true audience and use, and keep the surprise by omission.** Contributors are in on the secret (surprise-ops brief [5]); they hear: a film about her life for a gathering of N family, friends and community guests; her longer private version; possible later wider showing only with their written yes. Photo or video lenders who are not in the ring are asked through a truthful pretext card (A to E [5]); because a pretext such as "labelling photos" does not cover public use, their material stays out of the shared cut unless one of three things happens: they are brought in (the maker's decision), the item is low-risk Tier B below with a documented decision, or it is ratified afterwards.
2. **Public cut limited to cleared or low-risk appearances** (tiers below). The maker is the only person deciding. Every OUT stays out (surprise-ops rule: "any OUT on the shared cut means out" [5]).
3. **After the premiere, before any further showing: written releases.** Contributors, lenders, parents of minors, the family for the dead, and hers. No cinema, festival or online link until the consent ledger closes (Mon 29 Mar 2027 [5]) and the log shows green for T3 or T4.

**Appearance tiers for the public cut.**

| Tier | Who or what | Rule |
|---|---|---|
| A: in | Contributors who gave recorded consent on the updated card, and confirmed their clip by Mon 15 Feb [5]; the maker's own material; her appearances (see below) | In. Evidence: consent recording plus ledger row |
| B: in, documented risk | Adults in ordinary family, event or holiday photos shown briefly in the course of her story; no voice; no sensitive context; owner or photographer known and asked, or an accepted-risk entry | In, with a Tier B entry in the log and ratification after the premiere |
| C: only with explicit consent | Identifiable minors (guardian consent), any voice or video of a living person, named living third parties in hard episodes, ex-partners, estranged people, anyone in illness, money or conflict scenes | Out unless a yes is on file |
| D: out of the public cut | The dead animated or voiced without the closest family's yes; any synthetic voice; invented events shown as fact; identifiable strangers (crop, stylise or leave out) | Out |

Her appearance in a surprise film cannot be consented to beforehand. The proxy is the maker (charter), so for T2 the maker decides what of her life is shown (hard-chapter sheet [5]) and records the reason. **Her written release is gathered after the reveal** (below). IDA advises against asking for a signature long after the interview, because that suggests the producer needs it and invites refusal [79]. Ours is asked within days of the reveal, when the contributors and she have finally seen the film (inference), but before any further use.

**People who cannot be asked.**
- *Faces in old photos, unknown people:* crop to her and the people who can be named, stylise (L3) so a face is not a portrait, or choose another photo. Stylising does not remove the photographer's copyright (inference).
- *Estranged:* out, or a neutral past image only if she would tell it; never contacted cold [5].
- *Deceased:* the closest family says yes or no; record the answer; stills only unless they say more [1][5][6].
- *Minors:* guardian's yes; or out; or an adult-now yes.
- *Strangers in public-place photos:* IDA's "area release" is for fleeting or incidental appearances and "does not confer upon producers the same benefits of an appearance release" [79]; apply it by cropping and stylising, not by notice.

**Low-risk uses the public cut can include without a signed release** (decision aid, not a legal conclusion; confirm with the consult): the maker's own images; photos taken by contributors who gave recorded consent; fleeting background faces in a larger scene; adults in ordinary group photos (Tier B); original/CC0/licensed music and fonts; AI-labelled restorations of cleared photos. **Not low-risk:** a commercial recording, a studio photographer's portrait without checking, any identifiable minor, any voice not consented, any sensitive scene about a living third party, and any Minecraft or other-game asset.

**What a release must say** (for public screening and online use; plain language, one page; the full texts are in Templates): who is appearing and what (likeness, voice, name, photographs and recordings they lent); the film, its occasion and its audience; the uses allowed (public screening at named events; archive; private online link; cinema or festival), with check boxes so a person can say yes to some; no fee; term (until they withdraw, with a stated way to withdraw, or a fixed period; the usual documentary grant is all media, in perpetuity [79]); territory; the right to edit, crop, restyle and restore (including AI-assisted restoration, never changing what they said and never a synthetic voice); credit choice; a promise they own or may license what they lent; the data-protection notice (purpose, storage, retention, contact, withdrawal); the governing law (jurisdiction not yet known). Verbal releases recorded on camera are a fallback: cover the purpose, where it will first be used and how far it may travel [79].

### Finding 9. Extra for a real cinema or festival

- **E&O insurance (errors and omissions).** IDA 2012: required "for distribution deals with studios, television, cable networks, DVD and Internet sites"; standard limits $1,000,000 per claim and $3,000,000 aggregate with a $10,000 deductible; coverage takes at least three to five days; insurers expect a copyright report on underlying works, written agreements with creators, written releases for recognisable living persons giving rights to edit, music rights, permissions from copyright owners, and an opinion letter if relying on fair use [77]. IDA 2017: distributors, broadcasters and exhibitors generally require proof of coverage; typical distribution requirement is a deductible no higher than $25,000 and $1M/$3M limits; premium "$2,500 or more" for a typical distribution-required policy; three-year term typical; applications need an attorney's opinion letter and a commitment to the carrier's clearance procedures [78]. Neither article says whether festivals or private screenings require it. IDA members can ask HUB International for quotes [84]. **2026 cost: UNVERIFIED** (figures are 2012 and 2017, USD). A one-off hire at a cinema is not shown to require E&O by the pages I read; the venue may ask for public-liability insurance (ask; UNVERIFIED).
- **Clearance log and chain of title.** For a family film the chain of title is: the maker's original assets, plus a licence or permission for every third-party asset, plus the AI tools' terms. The log in Templates is that chain. Insurers' list above is the model [77].
- **Festival delivery (Sundance 2027 as exemplar).** Rules & Regulations item 24: the applicant must disclose any use of AI or risk disqualification [87]; FAQ 12: no restrictions on AI, disclosure required [88]. FAQ 14: you must license "any and all trademarked and/or copyrighted materials" before exhibiting publicly; accepted projects sign a waiver [88]. FAQ 18: screeners are online (maximum video bitrate 4,500 kbps H.264 mp4, AAC 256 kbps 2-channel stereo, maximum height 1080 px; no physical media) [88]. FAQ 31: in-person exhibition needs a DCP that includes both a Closed Caption and an Open Caption version, plus ProRes for online screenings, with English subtitles and SDH for non-English films; encrypted DCPs must supply open keys [88]. Frame rate and channel layout are not stated there; 24 fps and stereo or 5.1 are the usual (UNVERIFIED for other festivals).
- **Premiere status (important).** FAQ 8 defines "public theatrical exhibition" as "any screening of your completed project for which tickets were made available for purchase or given freely to members of the general public, whether at a film festival or any other public screening or event"; "private, invite-only or 'cast and crew' screenings" do not count, even with paid tickets, and work-in-progress or test screenings do not [88]. **A free public gathering can therefore cost eligibility in categories that require premiere status. If any festival life matters, make 27 February invite-only.** Other festivals differ (UNVERIFIED). This is the maker's call and the charter's "mostly public gathering" should say which.
- **Four-wall hire.** Picturehouse (UK): screen hire packages include a one-hour tech rehearsal, handheld microphones and technical support; most screens Flat and Scope; select cinemas have Dolby Atmos; no prices; the footer says 2026 [89]. Everyman (UK): private hire with "your own content" on the big screen; a host organises the event; no prices, formats or licensing stated [90]. Cinemark (US): private events including "a private screening of your film" for "Filmmakers and independent studios"; no prices or formats [91]. **Typical cost and terms: not available on these pages; UNVERIFIED.** Request quotes from two or three cinemas (enquiry questions in Templates 2b); expect to be asked for format (DCP or file), a tech test, insurance and music-licence statements.
- **Cue sheets.** Music cue sheet fields in 6.1; the AI cue sheet follows ai-imagery's end-credit cue sheet [6] (Finding 10).

### Finding 10. AI-generated material: ownership, registration, disclosure

| Topic | US | UK | EU | India |
|---|---|---|---|---|
| Ownership of purely AI output | Copyright Office Part 2 (29 Jan 2025): copyright "does not extend to purely AI-generated material, or material where there is insufficient human control over the expressive elements"; "prompts do not alone provide sufficient control" [53]. Thaler: the Supreme Court denied review on 2 Mar 2026 (Reuters via Wikipedia, secondary) [72] | CDPA s.9(3): for a computer-generated work "the author shall be taken to be the person by whom the arrangements necessary for the creation of the work are undertaken" [59]. A consultation (17 Dec 2024 to 25 Feb 2025) addressed computer-generated works; on 19 Mar 2026 DSIT published a report and impact assessment (content not read); no outcome on s.9(3) found [60] | No EU-wide AI-authorship rule found; the AI Act is about transparency, not ownership [65][66]. Originality needs a human author's own intellectual creation (background, UNVERIFIED) | Copyright Act s.2(d)(vi): for computer-generated works the author is "the person who causes the work to be created" [70]. No court test found |
| What human work is protected | Human-authored expression perceptible in outputs; creative selection, coordination, arrangement; creative modifications [53] | Per s.9(3) and ordinary originality | UNVERIFIED | UNVERIFIED |
| Registration and disclosure | Disclose more-than-de-minimis AI material and give a short statement of human contribution; hundreds of works with AI material have been registered, covering the human part [53] | UK has no registration | n/a | Registration exists; AI rules UNVERIFIED |
| Public disclosure duty | No general duty found for a private gathering (UNVERIFIED) | UNVERIFIED | AI Act Art. 50: providers must mark synthetic outputs; deployers of deepfakes "shall disclose"; for "evidently artistic, creative, satirical, fictional" work, disclosure is limited to the existence of such content "in an appropriate manner that does not hamper the display or enjoyment of the work" [65]. Application: the Commission says the Act became applicable on 2 Aug 2026 "with some exceptions", the AI Omnibus entered into force 27 Jul 2026 and moved high-risk dates; the page does not say whether it changed the Art. 50 timeline (UNVERIFIED) [66]. Whether a private individual is a "deployer" is not settled in my sources (background says personal non-professional activity is excluded; UNVERIFIED) | IT Rules amended (notified 10 Feb 2026, in force 20 Feb 2026) on synthetically generated content labelling, aimed at intermediaries (secondary source) [73] |
| Festivals | Sundance 2027 (a US festival): disclosure required, no ban [87][88]; others UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED |

**How ai-imagery's cue sheet and label ladder meet this.** The ladder (L0 scan; L1 cleaned; L2 enhanced; L3 restyled; L4 animated; L5 reconstruction) with labels in file names, `steps.csv`, XMP and the end-credit cue sheet [6] already gives indirect and direct disclosure. It satisfies Sundance's rule if the credits and metadata are accurate, and it meets Art. 50's "limited" disclosure for an artistic work if there is an on-screen cue. **Extensions needed (Templates, AI cue sheet):**
1. A short **pre-roll line before the title** ("Contains AI-assisted restoration and reconstruction; see credits") because Sundance asks for on-screen text for missing clearances and AI disclosure is a separate duty [88] (inference).
2. **Tool name, version and date** for every L2+ item, and the tool's terms about ownership and commercial use (free tiers may exclude commercial or public use; ai-imagery already flags "public or ticketed" [6]).
3. A **human-contribution statement** per item for a US registration (selection, arrangement, modification) [53].
4. Mark which L4b and L4c items could read as a **deepfake** (photoreal motion of a real person) so Art. 50(4)-style disclosure is explicit; stylised L3 and L5 are visibly drawn.
5. A line that **no synthetic voice** is used [1].
6. A note that **metadata may be stripped** by ffmpeg stream copy or re-encode and by platforms, so the credits and manifest are the real record [6].

### Finding 11. Who is in on it, and who approves: implications of "only me"

The relayed request settles this for the plan: **only the maker knows and only the maker is on the project.** For this track that means:
- **No second key.** surprise-ops' "two keys" and "proxy" structure (Decision 6, hard-chapter sheet [5]) assumes another person. For rights decisions, substitute: (a) the Fable advisor's written flag on each Tier C or accept-risk item, (b) a written entry with reasoning, jurisdiction note and "how would I undo it", (c) a gap of at least 48 hours between drafting and deciding on any accept-risk entry (inference), and (d) the consult below.
- **The paid consult.** Ask a local rights professional for one hour as a hypothetical ("a private person making a tribute film for a surprise public birthday gathering"), without naming her; whether to disclose the surprise to a lawyer under professional confidentiality is the maker's call. Question list in Templates.
- **Day-of TECH role.** The maker cannot both host the reveal and run playback. Options: the venue's AV operator, told a truthful minimum ("a short family video for a surprise on Saturday; please keep it quiet"); a hired AV tech with the same brief; or the maker's decision to bring one person in (this changes "only me"). Mark as an open decision (surprise-ops Decisions 6 and 12 [5]).
- **Rehearsals with staff** use the neutral test clip; the film itself plays only when the room is empty.
- **After the reveal,** the post-premiere releases are gathered by the maker alone; the consent ledger closes on day 30 [5].

## Exemplars and what they teach us

No published family-film clearance exemplar turned up (the search budget ended before I could look). The exemplars below are the closest working practice I could read.

| Exemplar | What it shows | What we take |
|---|---|---|
| **Sundance 2027 Rules & Regulations and FAQ** [87][88] | A real festival's delivery bar: DCP for in-person with Closed Caption and Open Caption versions; ProRes for online; screeners as H.264 stereo; AI use must be disclosed; accepted films sign a clearance waiver; free public screenings can void premiere status | Our deliverables column "Cinema" and the AI disclosure line; the decision to make 27 Feb invite-only if festivals matter |
| **DCP-o-matic itself** [8][15][18][24] | Free, GPL, used by "film-makers, projectionists, film festivals, subtitlists and cinema technicians"; has a Verify tool, a Player and command-line tools; its manual is blunt about what is untested | The cinema layer is buildable with free tools and scriptable; do not rely on the Player in the venue |
| **ISDCF papers** [26][27][28][29][30] | Practitioner documents on drive format, Interop versus SMPTE, channel order, subtitles, and cinema loudness | Our drive-format rule, SMPTE choice, channel mapping and the "no LUFS for cinema" rule |
| **Picturehouse and Everyman private hire** [89][90] | Cinemas accept private screenings of "your own content" and include a one-hour tech rehearsal in packages | The tech-rehearsal protocol and the question list for any later cinema |
| **IDA clearance articles** [77][78][79][81][82] | How documentary makers handle E&O, releases, archives and music: written releases, verbal fallback, fair-use opinion letters, festival-versus-all-media music licences | The rights log, the release wording, and the risk ladder |
| **Documentary Filmmakers' Statement of Best Practices in Fair Use (2005)** [58] | Four narrow situations where documentary makers can rely on fair use, and the limits | A reason not to treat fair use as a general answer for family photographs |
| **Minecraft Usage Guidelines** [48] | An unusually plain-language rights-holder policy that also says "we reserve the right to change our mind at any time" | Re-read and hash-check the page near the premiere; original voxel assets as the default |
| **Earlier project exemplars** [5][6] | surprise-ops' consent card and truthful pretext cards; ai-imagery's L0 to L5 ladder and end-credit cue sheet | We extend both, not replace them |

## Templates and deliverables

### Deliverable 0. Week-2 decisions (due Sunday 1 November 2026 unless noted)

| ID | Decision | Lean (this track) | What would change it |
|---|---|---|---|
| TD-1 | Working size | Stay 1920x1080 (16:9); 2K Flat DCP derived; stills at 3840 px or more on the long edge | A booked 4K cinema and a chapter that needs more detail: UHD for hero shots only, before Sun 3 Jan 2027 |
| TD-2 | Frame rate | 24 fps everywhere | A 50 Hz-only venue whose test shows judder: a 25 fps `fps=25` access copy |
| TD-3 | Captions | Burned-in open captions (7 to 8% line height for the venue file); sidecar SRT/VTT; DCP subtitle track only for a later cinema, with an OFL font | A venue that wants soft subtitles |
| TD-4 | DCP container and standard | Flat (1998x1080), SMPTE, unencrypted, 24 fps | A cinema that demands Interop or Scope |
| TD-5 | Door policy for 27 Feb | Maker decides: invite-only keeps festival premiere status (Sundance rule) [88]; open-to-all raises music, photo, likeness and Minecraft exposure | The maker's wishes for the room |
| TD-6 | Who runs playback on the day | A person told a truthful minimum (venue AV operator or hired tech); the maker hosts | The maker brings someone in (changes "only me") |
| TD-7 | Country and state of the premiere | Needed before the consult; also decides music, photo and likeness answers | None |
| TD-8 | Rights consult | One paid hour by Fri 4 Dec 2026 (asked as a hypothetical), before the contributor wave closes; a short follow-up in January if needed; question list below | Budget or privacy preferences |

### Deliverable 1. Delivery spec sheet

| Parameter | Venue, Sat 27 Feb 2027 | Cinema (later, via DCP) | Online (private link, later) | Archive |
|---|---|---|---|---|
| Purpose | Play on whatever the venue has (TV, projector, LED wall; laptop or USB) | A hired or festival cinema screen | Family and invited viewers | Preservation and re-making |
| Picture | 1920x1080, 16:9, 24p constant frame rate, BT.709, limited range, burned-in open captions | DCP 2K Flat container 1998x1080; the 16:9 picture centred, 39 px black bars each side; XYZ 12-bit via DCP-o-matic [15][22][31] | Same picture as venue, 1080p24 | ProRes 422 HQ 1920x1080 24p (optional FFV1 v3) [2][3] |
| Container and codec | MP4, H.264 High level 4.1, yuv420p, `+faststart`; `-crf 18 -maxrate 20M -bufsize 40M` [2] | SMPTE DCP (picture and sound MXF, CPL/PKL/ASSETMAP), unencrypted [15][21] | MP4 H.264 High, CRF 20, 12 Mbps cap [2] | MOV (ProRes) and/or MKV (FFV1), PCM audio [2] |
| Bit rate | up to 20 Mbps | JPEG2000 100 to 125 Mbit/s (hard cap 250) [15][18] | 8 to 12 Mbps | master data rate |
| Audio | AAC-LC 48 kHz stereo 256 kbps; venue mix about -16 LUFS integrated, -1 dBTP to start (confirm on site) [2][36] | PCM 24-bit 48 kHz; L/R in channels 1 and 2 of the container; cinema mix with headroom, not normalised; 5.1 fold-up only if voices need a centre channel [28][30][31] | AAC 256 kbps stereo; -16 LUFS, -1 dBTP [38] | PCM 24-bit 48 kHz, plus stems |
| Captions | Burned in; 2 lines; text inside the 90% by 90% safe box [37][4] | Burned in by default; or SMPTE subtitle track with an OFL font; a Sundance-style delivery adds Closed and Open Caption versions [14][27][88] | Burned in plus SRT/VTT sidecar | SRT, VTT, plain text transcript |
| Rights gate | T2 (public gathering): log green or documented risk for every asset; no unlicensed commercial music; no Mojang assets | T4: all T3 items green; releases signed; E&O decision; music cue sheet; AI disclosure | T3: releases signed; maker's explicit yes for the host [4] | Keep log, ledger and releases with the masters (encrypted storage) |
| File name | Neutral code name, no personal data, no metadata title; version and date | ISDCF-generated name, neutral title; first 40 characters carry the key facts [25][15] | Neutral | Descriptive, in a folder with README |
| Media | Two USB sticks (exFAT if the TV takes it; FAT32 if the file is under 4 GiB, which holds to about 28 minutes at 20 Mbps) [43][44] plus laptops | Drive written as MBR, one primary partition type 0x83, ext2 or ext3, inode 128; or network transfer; label "Do not read with a consumer computer" [19][26] | Upload | Two physical copies plus one off-site [2] |
| Checks | ffprobe tags and pixel format; colour-patch test; loudness and mono-fold; caption legibility at 3 m on the venue screen; hashes; G6 and G6b [3] | Verify DCP (no errors); play in Player; SHA-256 manifest; real-cinema test slot [18][17] | ffprobe; watch on a phone and a TV | Hash check yearly [2] |
| Fallback | Backup ladder above | A second DCP with burned-in captions if subtitle rendering fails [20] | n/a | n/a |
| Owner files | toolchain Step 12, agent-pipeline card and G6 | this track | format Decision 8 | toolchain Step 15 |

### Deliverable 2. Venue tech checklist and run-sheet lines

**2a. Venue survey questions** (ask by Fri 6 Nov 2026; log answers in a venue note; ask in the maker's own words, no mention of the film's subject):
1. Screen type and size: TV, projector, LED wall; native resolution; aspect ratio; distance to the back row.
2. Inputs: HDMI count and version, USB media playback, VGA or other; can we bring our own laptop; who operates it.
3. Projector: lumens or laser, lens shift, mounting, warm-up time; can the lights be dimmed to "low, not dark".
4. LED wall: processor input resolution and frame rates; whether it scales 16:9 or crops; brightness setting; colour temperature; test pattern at native size.
5. Sound: PA make, mixer inputs (3.5 mm, RCA, XLR), mono or stereo, subwoofer, house microphone for a 30 to 60 second welcome; who controls the fader.
6. Access: dates and hours for tests; time to rig; power; Wi-Fi.
7. Licences: does the venue hold a music licence and what does it cover; does it require our own insurance; any filming rules.
8. Staff: names, and what they will be told (truthful minimum).
9. Backup kit on site: spare HDMI, adapters, a second player.
10. Capacity and door policy.

**2b. Cinema enquiry questions (for any later hire or test slot; ask 2 to 3 cinemas for a written quote):**
1. Which screen sizes and formats (Flat, Scope), and is it a 2K or 4K projector?
2. Do you accept a DCP (and on what drive format, or by download), or only HDMI, Blu-ray, ProRes or MP4?
3. Is a tech rehearsal included, how long, and when?
4. What is the hire price by day and time, and what does it include (projectionist, microphone, house lights, captions)?
5. What insurance, licences or clearance statements do you require from me (public liability, E&O, music)?
6. Can I sell tickets or take donations, or must entry be free or invitation-only?
7. Does your own music licence cover anything I play, or only what is in my film?
8. Can I film or stream the event, and can I bring my own sound mix?
9. What is your cancellation policy and notice period?
10. Who will be in the room (staff names), and what do they need to know? (Truthful minimum only.)

**2c. Run-sheet lines (technical), numbered for merging into surprise-ops' key dates and Reveal-day run sheet** [5]:

| ID | When (surprise-ops date) | Who | Action | Pass criterion | If it fails |
|---|---|---|---|---|---|
| TD-L1 | Sun 1 Nov 2026 | Maker | Write TD-1 to TD-4 into the settings card | Card saved in repo | n/a |
| TD-L2 | By Fri 6 Nov 2026 | Maker | Venue survey (2a) | Answers logged | Assume worst case: laptop + HDMI + TV |
| TD-L3 | By Sun 20 Dec 2026 (G9) | Maker, agents | Build and view the venue test clip on the home TV; caption sizes 20, 23, 26 at 3 m; mono-fold; ffprobe | All clip checks pass | Fix and rerun |
| TD-L4 | By Sun 20 Dec 2026 | Maker | Make a 60-second test DCP in DCP-o-matic on the PC; Verify DCP; play in the Player | Zero errors; plays | Move DCP work to after the premiere |
| TD-L5 | By Fri 4 Dec 2026 (follow-up in Jan 2027) | Maker | Hold the consult; update the rights log and the releases | Notes saved | See Open questions |
| TD-L6 | Mon 15 Feb 2027 | Maker | Minecraft terms check #1 (only if any Mojang name or asset is used); contributors confirm their clip (surprise-ops); rights-log review | Hash matches or diff read | Remove asset or seek permission |
| TD-L7 | Fri 19 Feb 2027 (withdrawals close, surprise-ops; picture lock is Sat 6 Feb 2027, production-scale G-LOCK) | Maker | Freeze the rights log, AI cue sheet, music cue sheet and credits | Every row has a status | Out or substitute |
| TD-L8 | Sat 20 and Sun 21 Feb 2027 | Maker, agents | Final exports: master, venue file, backup file, audio-only fallback; apply trims; ffprobe, loudness and mono-fold; hashes; two sticks; **gate G6** [3] | G6 passes | Re-export |
| TD-L9 | **Mon 22 Feb 2027 (full run)** | Maker with venue AV operator | (1) Power the chain from cold and time to first frame. (2) Play the test clip: picture mode, overscan, HDR off, bars, PLUGE, ramp, tone level, left/right, caption size from the back row. (3) With the room empty, play the film's first 5 and last 5 minutes and three spot sections. (4) Walk the failure ladder rungs 1 to 4. (5) Photograph settings and cabling. **Gate G6b** | Plays at right levels; captions readable; no overscan crop; sound intelligible; mono-fold OK; cold start under 2 minutes | Adjust and repeat on Thu or Fri |
| TD-L10 | Wed 24 Feb 2027 (room brief) | Maker | Confirm AV access times with the venue (no content sent) | Times confirmed | n/a |
| TD-L11 | Thu 25 Feb 2027 (cold start #1) | Maker (+ operator) | Cold start on the real device and cable from power-off | First frame within 2 minutes | Rehearse again Fri |
| TD-L12 | Fri 26 Feb 2027 (cold start #2, pack list) | Maker | Cold start #2; Minecraft terms check #2 (if applicable); pack list: two sticks, two laptops, HDMI cable and spare, adapter kit, chargers, printed run sheet, test clip on a stick | Pack list ticked | n/a |
| TD-L13 | Sat 27 Feb S minus 4 h and S minus 2 h | TECH | Set up; run the test clip; confirm Do Not Disturb, notifications hidden, mail and chat closed [5]; play the film's first and last 30 seconds; spoken-line sound check; snapshot settings | As rehearsal | Use the ladder |
| TD-L14 | End of night | TECH | Back up any room recording agreed; delete extras; collect USB sticks [5] | Sticks accounted for | n/a |
| TD-L15 | Sun 28 Feb to Sat 6 Mar 2027 | Maker | Send post-premiere releases (4d to 4g); her turn conversation on Sat 6 Mar [5] | Requests sent | n/a |
| TD-L16 | Mon 29 Mar 2027 (ledger closes) | Maker | Close the consent ledger; set T3 and T4 gates in the rights log | Every row kept, changed, removed or closed until a date | No wider showing |

**2d. Venue test clip contents** (60 to 90 seconds, no personal content, built by the agents; one file, also kept as a DCP for the later test):
1. Countdown and slate (code name, version, date).
2. Colour bars and PLUGE (black level).
3. Grey ramp 0 to 100% in 10-bit steps (clipping, banding), then a smooth gradient (banding).
4. A real-face still of the maker or a stock public-domain face with known skin tone (skin check).
5. 1 kHz line-up tone at -20 dBFS, then left-only, right-only and pink noise (left/right ID, level, mono-fold).
6. Caption test: three sizes (FontSize 20, 23, 26) inside the 90% safe box, with a frame outline at 100%, 96.5% and 95% to see overscan and masking.
7. A slow 24p pan across a detailed image (judder, motion smoothing).
8. A one-minute speech sample at the film's mix level (intelligibility).
The tags and pixel format of this clip must match the venue file so one test covers both.

### Deliverable 3. Rights-clearance log template

One row per asset (or per cue or per person). The log is a CSV in the repo (private); sheets: `assets`, `music_cues` (fed by music-sound), `ai_items` (fed by ai-imagery `steps.csv`), `persons_releases` (the consent ledger), `fonts`, `games_brands`.

CSV header:

```
asset_id,type,title_or_description,where_used,how_obtained_and_by_whom,rights_holder_and_contact,persons_depicted,minor_flag,deceased_flag,needed_T1,needed_T2,needed_T3,needed_T4,permission_type,scope_media_territory_term_event,fee,status,evidence_ref_and_sha256,status_date,decided_by,advisor_flag,risk_tier,jurisdiction_note,substitute_asset_id,ai_label_L0_L5,ai_tool_version_date,music_cue_ref,release_id,notes
```

Column guide: `type` is photo, video, audio, music, voice, font, game, brand, ai, text or other. `needed_T1` to `needed_T4` take Y (needed), N, ? (unknown, ask) or V (venue-dependent). T1, the private cut for her alone, carries lower exposure but is not zero, so third-party commercial assets stay "?" there. `status` takes NS (not started), ASKED, GRANTED, REFUSED, SUBST (substituted), RISK (accepted documented risk), OUT, VERIFY (for the consult). `risk_tier` is A, B, C or D from Finding 8. `jurisdiction_note` always starts "Jurisdiction not yet known; confirm; not legal advice:" until TD-7 is answered. A RISK row must also say why, how it would be undone, who is exposed, and the date.

Sample rows:

| asset_id | type | where | rights holder | needed T1/T2/T3/T4 | permission | status | evidence | tier | note |
|---|---|---|---|---|---|---|---|---|---|
| PH-0042 | photo | Ch.1 | Aunt (took it, 1978) | ?/Y/Y/Y | Recorded yes on consent card | GRANTED | rec-0007.wav, sha256 ... | A | Ratify in writing after premiere |
| PH-0107 | photo | Ch.2 | Studio stamp "..." (defunct?) | ?/Y/Y/Y | None | VERIFY, SUBST candidate | scan back, note | B | Orphan-style search done 2026-xx-xx; UK IPO application fee £20 for one work (sliding scale) plus a licence fee; UK use only; US no safe harbour |
| MU-003 | music | Ch.3 bed | CC BY composer | Y/Y/Y/Y | CC BY 4.0, credit | GRANTED | licence PDF | n/a | Credit in end titles |
| MU-011 | music | Ch.4 | Label + publisher | ?/Y/Y/Y | Sync + master needed | NS | none | n/a | Substitute with MU-003 |
| FN-001 | font | titles | SIL OFL font | N/N/N/N | OFL | GRANTED | font + OFL.txt | n/a | Rasterised in video; embedded in DCP track |
| GM-002 | game | Ch.5 | Mojang | ?/Y/Y/Y | Not used (original voxel) | OUT | check_mojang_quotes output | n/a | Disclaimer if the name appears |
| AI-014 | ai | Ch.2 | Tool terms, human selection | ?/Y/Y/Y | Tool terms read 2026-xx | GRANTED | steps.csv row | n/a | Label L4b; pre-roll line |

Fields that must be filled before T4: `permission_type`, `scope`, `evidence_ref`, and a signed release or documented exception for every person in Tier A to C.

### Deliverable 4. Releases pack

Principles: say what the film is; do not state anything untrue; omit only the fact of the surprise; offer a way out; keep each text to one page; write in the person's language; jurisdiction and law text are placeholders.

**4a. Contributor consent card, version 2 (read aloud on the recording; replaces the card in surprise-ops [5]).** Read it only when the bracketed lines are true.

> "[MAKER] is making a film about [NAME]'s life as a surprise gift. It will be shown once, at a gathering on [date], to about [N] people: [family and invited friends] / [family, friends and community guests, which means it is a public-facing event, not only a family evening]. A longer private version will be given to [NAME]. May I use what you say, your recorded voice, your name, and any photographs or video you lend, in those showings? You can skip any question, stop, and ask me up to [Fri 19 Feb 2027] to take anything out. I will keep the recording private on storage I control [edit to match]. I may use software, including AI tools [that run on my own computer / in a private online workspace: edit to match], to type it up and tidy the sound, but I will not change what you said or make a synthetic copy of your voice. After the gathering I will ask you to sign a short written release if I want to show the film any further, for example online or in a cinema, and I will not do that without your signed yes. Is that all right with you?"

**4b. One-line version for a text or voice message:** "May I use your recorded voice and photos in a film for [NAME]'s gathering on [date], shown to about [N] guests, with you able to skip questions, stop, or have anything taken out until [date], and nothing wider without your written yes?"

**4c. Lender note (photos, video or letters lent by someone who is in on it):** "You lend these items, which you took or own, for use in the film described above. You allow them to be shown at the gathering and in [NAME]'s private version. You may ask me to remove any item until [date]. I will return the originals on [date]. For any further showing I will ask you again in writing." For lenders who are **not** in on it, use a truthful pretext card (A to E [5]) and do not use their copyright items in the shared cut unless Tier B applies; ratify afterwards.

**4d. Post-premiere written release (contributor or lender), one page.** Fields: your name; the film (working title and occasion); what you contributed (voice recording dated ..., photographs listed ..., video ...). *I agree that the film may be shown:* [ ] at further private gatherings, [ ] in a private online link, [ ] at public screenings, including a cinema or festival, [ ] kept in the family archive. *I understand:* no fee is payable; the maker may edit, crop, restyle and restore my contribution, including with AI-assisted restoration, but will not change the meaning of what I said or create a synthetic voice; my name will appear as [full name / first name / no name]; I may withdraw consent for future showings by writing to [contact], and copies already shared privately may remain; the maker will store my material at [place] for [period] and use it only for this film; I own, or have the right to license, what I contributed [or: someone else took it, named here]. Territory: worldwide. Term: until I withdraw in writing [or: a fixed term of N years]. Governing law: [jurisdiction not yet known]. Signature, date. The usual documentary grant is all media, worldwide, in perpetuity [79]; this version trades that for a withdrawal right, so choose before any E&O application (maker's decision).

**4e. Her release (offered after the reveal and her turn conversation, Sat 6 Mar 2027; no deadline).** In plain language: "This film is about you. Nothing is shown anywhere new without your yes. For each use, tick yes, no, or ask me again: [ ] family gatherings, [ ] a private online link for family, [ ] a public or invited screening you choose, [ ] a cinema or festival, [ ] kept in the family archive. You can ask me to remove or redo any scene (the list from our conversation is attached). You do not have to decide now; you can change your mind later by telling me. No payment passes either way. You keep the right to be named or not." Fields: her name, the scene list with her choice (kept, changed, removed, closed until a date), the uses table, signature, date, optional witness. This maps to surprise-ops' consent ledger and "her version" (about 24 Apr 2027) [5].

**4f. Parent or guardian addendum (minors).** "I am the parent or guardian of [child's name, age]. I allow [child]'s [photograph / voice / name] to be used as in the release above." Signature, relationship, date [86]. Under 14: guardian present, one question; 14 to 17: guardian consent and the child's own yes in plain words [5].

**4g. Family-of-the-deceased note** (short email; keep the reply in the log): "I am making a film about [NAME]. I would like to include a [photograph / recording] of [deceased person]. It would be shown [as a still, no movement, no new voice]. May I? You can say no, or ask me to remove it later." Record the sender, relationship and date.

**4h. Verbal-release script (if a person will not sign):** state on the recording the purpose, where it will first be shown (the gathering on [date]), what further uses are possible, and ask them to say yes in their own words [79]. Do not ask for a signature long after if they declined at the time [79].

### Deliverable 5. Jurisdiction-difference table and consult question list

*Jurisdiction not yet known; confirm; not legal advice.* Cells carry only what a source I read supports; "UNVERIFIED" means I did not read a primary source on this date.

| Topic | US | UK | EU | India |
|---|---|---|---|---|
| "Public" showing | Place open to the public, or a substantial number outside "a normal circle of a family and its social acquaintances" [56] | UNVERIFIED | UNVERIFIED | Narrow carve-out for performances in bona fide religious or official ceremonies, including marriage festivities, s.52(1)(za) [70] |
| Music at a free public event | Sync and master permission for any recording in the film; performance licence is separate; 110(4) is a narrow exemption for performances, not reproduction [57][82] | UNVERIFIED (PRS and PPL) | UNVERIFIED (national societies) | UNVERIFIED (IPRS); s.52(1)(za) is narrow [70] |
| Photograph ownership | Photographer by default (background, UNVERIFIED) | Author is "the person who creates it" [59] | UNVERIFIED | Author is "the person taking the photograph"; s.17(b): commissioned for valuable consideration, the commissioner is first owner absent agreement (copy read, date unknown) [70] |
| Orphan works | No safe harbour; 2015 Copyright Office recommended limiting remedies after a diligent search [54] | IPO licence: £20 application fee for one work (sliding scale) plus a licence fee; licence up to 7 years; UK use only [62] | Directive covers libraries, museums, archives, heritage institutions, public broadcasters only [63] | s.31A compulsory licence via the Appellate Board, after a newspaper notice [70] |
| Using others' work without permission | Fair use, four factors, no formula [55]; documentary best practices are narrow [58] | Fair dealing: criticism, review, quotation with acknowledgement [61] | Optional exceptions: quotation, incidental inclusion, parody; three-step test [64] | Fair dealing: private use, criticism or review, current events; incidental inclusion of artistic works in a film, s.52 [70] |
| Likeness, name, voice | State right of publicity; expressive uses often protected; post-mortem varies (California 70 years, Indiana 100, Tennessee unlimited if used) [71] | UNVERIFIED | Germany: consent to distribute or display images, 10-year post-mortem consent of relatives, exceptions limited by legitimate interest [68][69]; France: Civil Code art. 9 [71]; GDPR household exemption does not cover public showings (inference) [67] | Personality rights developing in the Delhi High Court [71]; DPDP Act UNVERIFIED |
| Minors | Parent or guardian signs a release [86] | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| AI-generated output ownership | Human authorship required; prompts alone insufficient [53] | s.9(3) names the arranger; reform under review [59][60] | UNVERIFIED | s.2(d)(vi) "the person who causes the work to be created" [70] |
| AI disclosure | No general duty found; festival rules (Sundance) apply [87][88] | UNVERIFIED | AI Act Art. 50 (deepfake disclosure, limited for artistic works); timing of application partly unclear [65][66] | IT Rules labelling of synthetic content from 20 Feb 2026, for intermediaries (secondary source) [73] |
| E&O insurance | Common requirement from distributors and exhibitors; $1M/$3M limits [77][78] | UNVERIFIED | UNVERIFIED | UNVERIFIED |

**Question list for the one-hour consult** (send before the hour; ask as a hypothetical):
1. In [country/state], is a free, non-sponsored tribute-film screening at a hired hall for about [N] guests a "public" performance? Does it matter if guests are invited rather than open to all?
2. Music: for a commercial recording copied into the film, do I need both sync and master permission for this event? Does the venue's performance licence cover any of it? Is there any exemption for non-profit or family events here?
3. Can I rely on a short, live-performed or cover version of a song? Who owns the rights?
4. Photographs: do the commissioned wedding and studio photographs belong to the photographer or the client here? What do I do about photographs whose photographer I cannot find?
5. Is there a safe way to use old family photographs in a film for a public event without permission from every photographer? What risk am I taking, and what does a documented decision look like?
6. Likeness and voice: what consent do I need from living people who appear in photographs or recordings, for this event, and for later online or cinema showings? Does a recorded verbal yes count?
7. Minors: what do I need for children who appear in photographs? When must a parent sign?
8. The dead: are there post-mortem rights here? Whose consent counts?
9. People who are estranged: do I have any obligation to tell them, or can I leave them out?
10. Data protection: do photographs and voice recordings count as personal data here, and what notice must I give contributors?
11. Surprise: is it lawful to gather contributions under a truthful but incomplete explanation, and what must I tell people before the screening?
12. AI: who owns AI-assisted restorations and reconstructions? What must I disclose, to whom, and when?
13. Fonts and game content: any local rule about embedding fonts in video, or showing game footage?
14. Brand-name games: is a stylised voxel world "in the style of" a game safe, and what should I avoid?
15. If I later hire a cinema, what insurance and paperwork will they or the law require? Is E&O needed for a single screening?
16. Before a cinema, festival or online release, what is the minimum clearance file (log, releases, licences) a lawyer would want?
17. Who is liable if a contributor withdraws after the screening?
18. How should I word the releases here (term, territory, right to edit, withdrawal)?
19. Any trademark or personality issues in using her name in the title?
20. Is it better to wait for her release before any screening beyond 27 February?

### Deliverable 6. Deltas to existing playbooks, by file and decision

| File | Where | Change |
|---|---|---|
| `toolchain.md` | Step 10 (sound) | Add that -16 LUFS is a venue/online start point and cinema mixes are not normalised; broadcast -23 LUFS is not a cinema target [30][36] |
| `toolchain.md` | Step 11 (captions) | Windows fonts are fine rasterised in video, not embedded in a DCP track; prefer OFL fonts [75][76] |
| `toolchain.md` | Step 12 (export set) | Add the venue test clip, the two trims, a mono-fold check, a DCP column |
| `toolchain.md` | Step 13 | Add `color_range`/`color_space` checks, loudness plus mono-fold |
| `toolchain.md` | Step 14 | Rehearse with the neutral test clip first; walk the ladder rungs; take settings screenshots |
| `toolchain.md` | Decision 7 | Change "Use 4K only after the venue screen is confirmed" to: 2K Flat DCP derived from 1080p; 4K not needed |
| `toolchain.md` | Decision 8 | Burned-in captions confirmed as default; DCP subtitle tracks later with OFL fonts |
| `toolchain.md` | Decision 9 | Add venue-survey questions (2a) |
| `agent-pipeline.md` | Step 1 and settings card | Lock 24 fps (TD-2); "Colour: Rec. 709, sRGB" should read Rec.709 / BT.1886 display target (gamma about 2.4) for video, sRGB for stills; add "stills 3840 px or more on the long edge" |
| `agent-pipeline.md` | Gate G6 | Add mono-fold check, trims applied, caption safe area, test clip played on the venue screen, DCP Verify if a DCP is made; add G6b (venue rehearsal) |
| `format.md` | Step 8 and Exercise 1 | Keep 7 to 8% line height for the venue file; add the cinema 5.5 to 6% note |
| `format.md` | Step 15 | "Send the file to the venue a day before" conflicts with the surprise: send only the test clip; bring the film on the day |
| `format.md` | Decision 3 (venue) | Add the survey questions |
| `format.md` | Decision 9 (Minecraft) | Replace "grey area" with the 2026-10-18 re-read and table (Finding 7) |
| `format.md` | Decision 12 (music) | Add the exhibition layer: sync + master + performance; public gathering is not a family circle |
| `format.md` | Decision 13 (languages) | Open: captions in other languages (VF or burned-in) |
| `surprise-ops.md` | Consent card | Replace with version 2 (4a): true audience and use, later written release |
| `surprise-ops.md` | Decision 6 (rings and keys) | Update for "only me": no co-keeper or proxy; compensating controls (Finding 11) |
| `surprise-ops.md` | Decision 12 (reveal format and room) | The charter now says "mostly public"; the run sheet and tiers must follow TD-5 |
| `surprise-ops.md` | Key dates | Add TD-L6, TD-L7, TD-L9 to TD-L16 |
| `surprise-ops.md` | Reveal-day run sheet S minus 2 h | Add test clip first, settings snapshot, backup stick and second laptop check |
| `surprise-ops.md` | After the reveal | Add the post-premiere release step (TD-L15) and the T3/T4 gate (TD-L16) |
| `ai-imagery.md` | Decisions 3 and 5 | "Public or ticketed" now applies to 27 Feb; add the six cue-sheet extensions (Finding 10) |
| `games.md` | Q7 and F4 | Add the 2026-10-18 diff result and new clauses |
| `CHARTER.md` | Open decisions | Add: door policy (TD-5), jurisdiction (TD-7), who runs playback (TD-6) |

## Tools, services and costs (as of 2026-10-18)

| Item | Cost and terms | Notes |
|---|---|---|
| DCP-o-matic 2.18.51 (released 16 Oct 2026) | Free; GNU GPL (version 2 linked) [8][10] | Windows 64/32-bit, macOS, Linux. Includes Player, Verify, Disk Writer, KDM tools and CLI [23][21]. Manual index [9] |
| ffmpeg and ffprobe | Free | Container build 6.1.1 (has `libopenjpeg`); the PC build per agent-pipeline is Gyan 9.0.2 [3][47] |
| mpv or VLC | Free | mpv: hardware decoding off by default; `display-resample` needs constant frame rate [41] |
| PowerShell `Get-FileHash` | Built in | SHA-256 manifests [4] |
| MagicaVoxel, Blockbench | Free (per games.md [7]) | For original voxel assets (Minecraft by reference) |
| SIL OFL fonts | Free; keep licence and notices [75] | Prefer for titles, captions and DCP subtitle tracks |
| Windows system fonts | Included; bitmap-rendered use in video allowed; no embedding or conversion [76] | Not for DCP subtitle tracks or apps |
| USB sticks, spare HDMI, adapters, a second laptop | UNVERIFIED (not priced) | Two sticks minimum; a drive for a DCP if needed |
| Test cinema slot, four-wall hire | UNVERIFIED. Picturehouse, Everyman and Cinemark list no prices [89][90][91] | Get 2 to 3 quotes; ask what tech rehearsal is included |
| E&O insurance | "$2,500 or more" (IDA, 2017, USD); limits $1M/$3M; deductible up to $25,000; three-year term typical [78]. 2012 figures: $10,000 deductible [77]. 2026 cost UNVERIFIED | Required by distributors, broadcasters and exhibitors; IDA members can ask HUB International [84] |
| UK IPO orphan works licence | Application fee £20 (1 work), £24 (2), £30 (5), £40 (10), £60 (20), £80 (30), non-refundable; a separate licence fee is payable only if the licence is granted; up to 7 years; UK use only [62] | Photograph applications need an uploaded image |
| One-hour rights consult | UNVERIFIED | Ask a local solicitor or attorney who works with media and IP; community arts-law clinics may exist (UNVERIFIED) |
| Music licences (sync, master, event) | UNVERIFIED | CC0 and CC BY music cost nothing; commercial songs need quotes |
| Minecraft permission | No fee schedule; partnership by proposal [48] | Original voxel assets avoid the question |
| Cloud container | Free within the session; 4 vCPU, 16 GB RAM, root disk was 100% full at about 140 to 290 MB free; background jobs up to 2 hours (tool limit) | Not suitable for the DCP encode (disk) [47] |

## Risks, pitfalls and ethics (with mitigations)

1. **Jurisdiction-specific facts presented as universal.** Fair use is US, fair dealing is UK and India, personality and post-mortem rights vary by country and US state, public-domain dates differ. *Mitigation:* every legal statement here carries its jurisdiction and "not legal advice"; TD-7 asks for the country; the consult list is written to be sent in advance.
2. **The consent card is no longer true.** It says "family will watch together" and "private" [5]. *Mitigation:* use version 2 (4a) before the first recording; do not use the old text.
3. **A free public premiere is not a family showing.** "Publicly" in US law reaches beyond a family circle [56]; music, photo and likeness exposure rise; Minecraft treats sharing as commercial [48]; Sundance treats free public screenings as public exhibition [88]. *Mitigation:* TD-5 door policy; tiers A to D; cleared or substituted assets in the shared cut.
4. **Loudness confusion.** A broadcast -23 LUFS target on a cinema mix is wrong; a quiet cinema mix posted online plays quietly; the venue PA is unknown [30][36][38]. *Mitigation:* three outputs from one mix; test clip and the oldest listener.
5. **Colour drift between a consumer monitor, the venue and a cinema.** *Mitigation:* one grade, two trims, tested on the real screen; no HDR; colour-patch test after every re-encode [3][42].
6. **DCP-ingest failures.** Wrong drive format, corrupt copy, standard and subtitle faults, KDM trouble, capability mismatch (Finding 4) [18][19][26]. *Mitigation:* ext2/ext3 MBR drive, Verify DCP, hash, unencrypted SMPTE, 24 fps, burned-in captions, a real-cinema test.
7. **A consumer computer can destroy a DCP drive** [26]. *Mitigation:* label it; never plug it into the Windows PC after writing; keep a copy of the folder elsewhere.
8. **Surprise leaks through technical channels.** DCP and file titles, metadata, thumbnails, Windows "Recent" lists, venue staff watching the film, cloud copies. *Mitigation:* neutral code name, metadata stripped (`-map_metadata -1`, inference), test clip for staff, film played only in an empty room, a truthful minimum brief for the operator [5].
9. **Minecraft terms are undated and revocable** [48][49]. *Mitigation:* original assets; the premiere-week hash check; dated excerpts in `research/sources/`.
10. **Fair use is over-trusted for stills.** "Still photographs in particular do not lend themselves to fair use treatment" [80]. *Mitigation:* ask, substitute, or document a Tier B decision; use the consult.
11. **Accepted risks decided by one person.** With no second key, errors can go unchallenged. *Mitigation:* advisor flag, written reasons, 48-hour gap, reversible choices first (Finding 11).
12. **AI disclosure and ownership gaps.** Free-tier tool terms, metadata stripped by re-encoding, deepfake-like L4b clips [6][65]. *Mitigation:* the six cue-sheet extensions; ledger of tool terms; pre-roll line.
13. **Personal data in the rights log and ledger.** Names, consents, addresses. *Mitigation:* keep in the private repo only; encrypted storage for the archive copy; nothing uploaded to third parties without the maker's explicit say [1].
14. **Misleading edits and false impressions.** A film can create liability or hurt even if each clip is true [85]. *Mitigation:* the hard-chapter sheet [5]; no invented events; reconstructions labelled L5 [6].
15. **Accessibility.** An older audience needs readable captions and clear sound [4][5]. *Mitigation:* burned-in captions at 7 to 8% line height; intelligibility check at the back row.
16. **Disk and compute limits in the container.** *Mitigation:* encode the DCP on the PC; keep the container for measurement and verification.
17. **Reliance on the DCP-o-matic Player at the venue.** The manual warns against depending on it without plenty of testing [17]. *Mitigation:* use MP4 in the venue; the DCP is for a cinema.
18. **Dignity and consent of people who cannot be asked.** *Mitigation:* Tier C and D rules; ask the closest family for the dead; the estranged default to out [5].

## Open questions / gaps

**Decisions only the maker can make:** TD-5 door policy (invite-only or open); TD-6 who runs playback; TD-7 country and state; TD-8 the consult; whether a cinema screening is wanted at all (the DCP is a post-premiere job unless the venue is a cinema); release term (perpetual versus withdrawable).

**UNVERIFIED or not found this round** (the search budget ran out; a follow-up search round could close most of these):
- 2K versus 4K installed-base shares; the DCI specification text itself (the site is script-rendered); SMPTE RP 200 cinema reference calibration (85 dB SPL, -20 dBFS pink noise) and typical DCP dialogue levels, as background knowledge only.
- Which gamma each DCP-o-matic colour preset applies; whether ProRes `.mov` imports cleanly; DCP-o-matic's own encode speed and its Windows memory use; the Windows Settings path for a 24 Hz refresh rate; whether the ISDCF name shows "20" with only L/R mapped.
- TV and projector USB format support (exFAT, MKV, soft subtitles) for the actual venue; LED-wall processor details; HEVC support on Windows and TV USB players.
- Cinema four-wall prices and terms (Picturehouse, Everyman, Cinemark list none); 2026 E&O premiums; whether a one-off hire needs E&O or public-liability insurance; festival specs other than Sundance (frame rate, channels, other festivals' AI and premiere rules).
- ASCAP, BMI, PRS, PPL and IPRS statements on what a venue licence covers; the US sound-recording performance right; UK and EU music rules; UK image-right position; India's DPDP Act and personality-rights details; minors' rules outside the US model-release note; post-mortem rights in the UK and India; the US orphan-works position in 2026.
- EU AI Act Article 50: whether the AI Omnibus (in force 27 Jul 2026) changed its timeline; whether a private individual is a "deployer"; EU and India copyright treatment of AI output.
- India Copyright Act s.17(b): I read a government-hosted consolidated copy of unknown date; confirm the current text.
- AES TD1004.1.15-10 and Netflix loudness numbers (pages blocked or script-rendered); British Pathe or Getty archive pricing; the Library of Congress and E&O vendor details.
- What family-film makers actually do about clearances: no survey found; the risk ladder in Finding 6 is a synthesis from documentary practice.
- Trim values (shadow lift, gamma) and the caption sizes for a cinema are starting hypotheses that need a real-screen test.

**Environment note for the orchestrator:** the container's root disk was at 100% during this round (about 140 to 290 MB free). Other agents may be affected.

## Sources

Local project files (read 2026-10-18):
[1] Project Charter — CHARTER.md — 2026-10-18 — facts, principles, open decisions.
[2] toolchain playbook — playbooks/toolchain.md — 2026-10-18 — Steps 10 to 15, Decisions 6 to 9.
[3] agent-pipeline playbook — playbooks/agent-pipeline.md — 2026-10-18 — settings card, gate G6, pitfall 6.
[4] format playbook — playbooks/format.md — 2026-10-18 — caption rules, hosting table, Decisions 3, 8, 9, 12, 13.
[5] surprise-ops playbook — playbooks/surprise-ops.md — 2026-10-18 — key dates, consent card, pretext cards, run sheet, Decisions 6 and 12.
[6] ai-imagery playbook — playbooks/ai-imagery.md — 2026-10-18 — L0 to L5 ladder, cue sheet, decisions.
[7] games research and Minecraft excerpt — research/games.md; research/sources/minecraft-usage-guidelines-2026-10-18.txt; research/sources/check_mojang_quotes.py — 2026-10-18 — earlier clause reading and the comparable-hash checker.

DCP-o-matic (all fetched 2026-10-18):
[8] DCP-o-matic download — https://dcpomatic.com/download — 2026-10-18 — stable 2.18.51, 16 October 2026; Windows, macOS, Linux.
[9] DCP-o-matic manual index — https://dcpomatic.com/manual/html/ — 2026-10-18 — chapter list (https://dcpomatic.com/manual redirects here).
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
[23] Manual, introduction — https://dcpomatic.com/manual/html/ch01.html — 2026-10-18 — tools in the suite.
[24] DCP-o-matic home page — https://dcpomatic.com/ — 2026-10-18 — purpose; used by film-makers, projectionists, festivals.
[25] ISDCF naming convention intro and document index — https://www.isdcf.com/registry/dcncintro/ and https://www.isdcf.com/resources/documents/ — 2026-10-18 — underscores, 40-character display note, document list.
[26] ISDCF Doc 3, DCP Delivery Recommendations — https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf — 2017-06-29 — MBR, 0x83, ext2/ext3, 128-byte inode, USB 2.0, consumer-OS warning.
[27] ISDCF Doc 2, DCP Transition Review — https://files.isdcf.com/papers/ISDCF-Doc2-DCP-TransitionReview.pdf — 2011-11-02 — Interop versus SMPTE tables.
[28] ISDCF Doc 4, audio channel packaging — https://files.isdcf.com/papers/ISDCF-Doc4-Audio-channel-recommendations.pdf — 2017-06-29 — channel order, even channel count.
[29] ISDCF Doc 10, Subtitles and Captions in Digital Cinema — https://files.isdcf.com/papers/ISDCF-Doc10-Subtitles-and-Captions-in%20Digital-Cinema-20160211.pdf — 2016-02-11 — open versus closed, support in projectors.
[30] ISDCF Doc 11, "How Loud is a Movie?" (Ioan Allen, SMPTE) — https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf — 2016-03-15 — calibrated rooms, fader 7, TASA 85 dB Leq(m), no feature limits.
[31] Wikipedia, Digital Cinema Package — https://en.wikipedia.org/wiki/Digital_Cinema_Package — 2026-10-18 — secondary: containers, bit rate, audio, Interop versus SMPTE, ext2/ext3.
[32] Wikipedia, Digital cinema — https://en.wikipedia.org/wiki/Digital_cinema — 2026-10-18 — secondary: 98% digital by end-2017; DCI sizes.
[33] Wikipedia, DCI-P3 — https://en.wikipedia.org/wiki/DCI-P3 — 2026-10-18 — secondary: primaries, white point, gamma 2.6.

Colour, audio, display:
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
[46] FFmpeg scaler documentation — https://ffmpeg.org/ffmpeg-scaler.html — 2026-10-18 — `sws_dither` options.
[47] Own measurements in the cloud container — 2026-10-18 — ffmpeg 6.1.1, `libopenjpeg`, 4-vCPU Intel Xeon at 2.1 GHz, 16 GB RAM; disk 100% full; `ebur128` and `pan` syntax run; JPEG2000 timings in Finding 4.

Rights, law and practice:
[48] Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 about 07:00 GMT; no visible date — physical locations, 150 participants, sharing equals commercial, name as title, disclaimer; extract hash c5a8...94222 matches earlier captures.
[49] Minecraft EULA — https://www.minecraft.net/en-us/eula — fetched 2026-10-18 about 07:00 GMT; no visible date — distribution, content ownership, guidelines revocable; excerpt in research/sources/.
[50] Nintendo, Game Content Guidelines for Online Video & Image Sharing Platforms — https://www.nintendo.co.jp/networkservice_guideline/en/index.html — 2018-11-29, updated 2024-09-02 — online platforms only, individuals, no commercial use.
[51] Microsoft, Game Content Usage Rules — https://www.xbox.com/en-US/developers/rules — "Last Updated: January 2015" — covers Microsoft games except Minecraft.
[52] US Copyright Office, Copyright and AI — https://www.copyright.gov/ai/ — 2026-10-18 — Part 1 (31 Jul 2024), Part 2 (29 Jan 2025), Part 3 pre-publication (9 May 2025).
[53] US Copyright Office, AI Part 2: Copyrightability — https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — January 2025 — conclusions, prompts, disclosure on registration.
[54] US Copyright Office, Orphan Works and Mass Digitization — https://www.copyright.gov/orphan/reports/orphan-works2015.pdf — June 2015 — "legal cloud"; limitation-on-remedies proposal.
[55] US Copyright Office, Fair Use — https://www.copyright.gov/fair-use/ — 2026-10-18 — four factors; no safe percentage.
[56] 17 U.S.C. 101 — https://www.law.cornell.edu/uscode/text/17/101 — 2026-10-18 — definition of "publicly" (family and social acquaintances).
[57] 17 U.S.C. 110 — https://www.law.cornell.edu/uscode/text/17/110 — 2026-10-18 — 110(4) non-commercial performance exemption.
[58] Documentary Filmmakers' Statement of Best Practices in Fair Use — https://cmsimpact.org/code/documentary-filmmakers-statement-of-best-practices-in-fair-use/ — November 2005 — four situations and limits.
[59] Copyright, Designs and Patents Act 1988, s.9 — https://www.legislation.gov.uk/ukpga/1988/48/section/9 — 2026-10-18 — authorship, computer-generated works.
[60] UK Government, Copyright and artificial intelligence consultation — https://www.gov.uk/government/consultations/copyright-and-artificial-intelligence — consultation 17 Dec 2024 to 25 Feb 2025; update 19 Mar 2026 — report and impact assessment published (not read).
[61] UK Government, Exceptions to copyright — https://www.gov.uk/guidance/exceptions-to-copyright — 2026-10-18 — criticism, review, quotation; fair dealing test.
[62] UK IPO, Orphan works licensing — https://www.gov.uk/guidance/copyright-orphan-works — 2026-10-18 — fees, 7-year licence, UK only.
[63] Directive 2012/28/EU, orphan works — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32012L0028 — 2026-10-18 — beneficiaries are institutions.
[64] Directive 2001/29/EC, Article 5 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32001L0029 — 2026-10-18 — quotation, incidental inclusion, parody, three-step test.
[65] EU AI Act, Article 50 — https://artificialintelligenceact.eu/article/50/ — 2026-10-18 — marking, deepfake disclosure, artistic works.
[66] European Commission, AI Act regulatory framework — https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai — last update 3 Aug 2026 — applicability and AI Omnibus.
[67] GDPR Article 2 — https://gdpr-info.eu/art-2-gdpr/ — 2026-10-18 — personal or household activity exemption.
[68] Kunsturhebergesetz (KUG) section 22 — https://www.gesetze-im-internet.de/kunsturhg/__22.html — 2026-10-18 — consent, 10 years post mortem (German text).
[69] KUG section 23 — https://www.gesetze-im-internet.de/kunsturhg/__23.html — 2026-10-18 — exceptions and limit (German text).
[70] Copyright Act, 1957 (India), consolidated copy — https://copyright.gov.in/Documents/Copyright_Act_1957.pdf — 2026-10-18; date of consolidation not shown — ss.2(d), 17, 31A, 52.
[71] Wikipedia, Personality rights — https://en.wikipedia.org/wiki/Personality_rights — 2026-10-18 — secondary: US state law, post-mortem terms, Germany, France, India cases.
[72] Wikipedia, Artificial intelligence and copyright — https://en.wikipedia.org/wiki/Artificial_intelligence_and_copyright — 2026-10-18 — secondary: D.C. courts, Supreme Court denial (Reuters, 2 Mar 2026), UK s.9(3).
[73] Wikipedia, Regulation of artificial intelligence — https://en.wikipedia.org/wiki/Regulation_of_artificial_intelligence — 2026-10-18 — secondary: India IT Rules amendment (notified 10 Feb 2026, in force 20 Feb 2026).
[74] Wikipedia, Cinema of India — https://en.wikipedia.org/wiki/Cinema_of_India — 2026-10-18 — secondary: 10,033 screens (2025).
[75] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — 2026-10-18 — output not restricted; video titling; embedding.
[76] Microsoft, Font redistribution FAQ — https://learn.microsoft.com/en-us/typography/fonts/font-faq — page dated 2024-11-19 — video captions as bitmaps allowed; no embedding or conversion.
[77] IDA, "Errors & Omissions: ... Guide to Protecting Your Film" (Winnie Wong) — https://www.documentary.org/feature/errors-omissions-rights-oh-my-guide-protecting-your-film — 2012-04-06 — E&O requirements, $1M/$3M, $10,000 deductible.
[78] IDA, "To Err (or Omit) Is Human - Thankfully, There's E&O" (Beer, Levy, Rosini) — https://www.documentary.org/column/err-or-omit-human-thankfully-theres-eo — 2017-09-28 — "$2,500 or more"; requirements; three-year term.
[79] IDA, "A Practical Discussion of Appearance Releases" — https://www.documentary.org/column/practical-discussion-appearance-releases — undated — release contents, verbal fallback, area releases.
[80] IDA, "Caveats for Using Amateur Footage" — https://www.documentary.org/column/caveats-using-amateur-footage-plus-considering-incentives-overseas-productions — undated — creator owns; stills and fair use.
[81] IDA, "Dusting Off Archive Agreements" (Beer, Levy, Rosini) — https://www.documentary.org/column/dusting-archive-agreements-fresh-review — 2018-01-09 — pricing factors, negotiation.
[82] IDA, "All Clear? A Basic Primer on Music Clearance" (David G. Powell) — https://www.documentary.org/feature/all-clear-basic-primer-music-clearance — 2003 — sync, master, festival versus all-media licences.
[83] IDA, "Copyright and Public Domain: An Updated Primer" — https://www.documentary.org/feature/copyright-and-public-domain-updated-primer — 2020-06-13 — US public-domain checking.
[84] IDA, Insurance program — https://www.documentary.org/membership/insurance — 2026-10-18 — production insurance and E&O via HUB International; no prices.
[85] IDA, "Beyond Vetting: Common Legal Issues for Documentary Filmmakers" (Katie Townsend) — https://www.documentary.org/column/beyond-vetting-common-legal-issues-documentary-filmmakers — 2020-06-11 — misleading edits; consent laws.
[86] Wikipedia, Model release — https://en.wikipedia.org/wiki/Model_release — 2026-10-18 — secondary: minors need parent or guardian signature.
[87] Sundance Film Festival 2027 Rules & Regulations — https://www.sundance.org/submissions-rules — 2026-10-18 (2027 festival) — item 24 AI disclosure.
[88] Sundance Film Festival 2027 submissions FAQ — https://www.sundance.org/submissions-faq — document created 2026-09-08 — premiere definition (FAQ 8), AI (12), temp music (13), clearance (14), screener format (18), DCP delivery (31).
[89] Picturehouse Cinemas, Venue hire — https://www.picturehouses.com/venue-hire — footer 2026; fetched 2026-10-18 — screen hire packages, one-hour tech rehearsal; no prices.
[90] Everyman Cinema, Private hire — https://ww2.everymancinema.com/private-hire — fetched 2026-10-18 — your own content; no prices.
[91] Cinemark, Private events — https://www.cinemark.com/private-events — footer 2026; fetched 2026-10-18 — private screening for filmmakers; no prices.

## Follow-up research (round 1)

Researcher: Sonnet (Sonnet 5.5), track `theatrical-delivery`. Date: Sunday 2026-10-18. Maker: the only human on the project (the relayed request says "for now only me" and that the maker will be the only one on the project). Nothing here is legal advice. The country of the premiere (TD-7) is still not given, so every legal item carries its jurisdiction.

**Method and limits of this round.**
- The shared web-search budget was already used up when I started (WebSearch returned "budget used up" on both attempts). I did not use search engines, archive services or readers as a workaround. I worked from primary pages fetched directly and from the DCP-o-matic source code.
- **Source code read directly.** I made a shallow git clone of the DCP-o-matic repository. Its HEAD is the tag `v2.18.51` (commit 920fb9b, dated 2026-10-16) [92]. I also cloned libdcp, the library that holds the colour presets (commit 891facc, 2026-10-01) [93]. Source facts below were read from those files and are tagged **(source)**. Test names and file lines are given so they can be re-checked.
- **What I did not do.** I downloaded the official 2.18.51 command-line package for Ubuntu 24.04 [95] and tried to launch two of its programs (`dcpomatic2_create`, `dcpomatic2_cli`). Both stopped at once on missing libraries and then on a missing resources folder. The next step (linking a resources folder into `/usr/share`) was declined by the session's permission system, so I stopped. **No DCP was built and no DCP-o-matic binary ran successfully.** I deleted the downloaded and extracted binaries. Everything below about DCP-o-matic's behaviour is therefore from source and tests, not from running it. The package URL is in [95] if the maker later wants a real test build.
- Quotes marked "(read from file)" were read from files I downloaded or cloned. All other quoted phrases came back through the fetch tool and were not re-checked word for word.
- Tags: **(source)** = read in the 2.18.51 code; **(measured)** = my test in the cloud container; **(computed)** = arithmetic; **(inference)** = my reasoning; **UNVERIFIED** = no primary source reached.

### FU-1. DCP-o-matic 2.18.51: colour presets, ProRes import, memory and speed

**Which gamma each preset applies (source) [92][93].** The presets are defined in `src/lib/colour_conversion.cc` (`PresetColourConversion::setup_colour_conversion_presets`) and implemented in libdcp's `src/colour_conversion.cc`. Each is "decode with an input gamma, convert primaries to XYZ, re-encode with a 2.6 gamma".

| Preset (dialog name, `--colourspace` id) | Input gamma | YUV to RGB matrix | Primaries and white | Output gamma |
|---|---|---|---|---|
| Rec. 709 (`rec709`) | **2.2**, plain power law | Rec. 709 | Rec. 709, D65 | 2.6 |
| Rec. 1886 (`rec1886`) | **2.4**, plain power law | Rec. 709 | Rec. 709, D65 | 2.6 |
| Rec. 601 (`rec601`) | 2.2 | Rec. 601 | Rec. 709 primaries, D65 | 2.6 |
| sRGB (`srgb`) | sRGB piecewise curve (2.4 with a linear toe: 0.04045, 0.055, 12.92) | Rec. 601 | Rec. 709 primaries, D65 | 2.6 |
| P3 DCI (`p3`) | 2.6 | Rec. 709 | DCI-P3, white (0.314, 0.351) | 2.6 |

- The source comment on the Rec. 1886 preset reads (read from file): "According to Olivier on DCP-o-matic bug #832, Rec. 1886 is Rec. 709 with 2.4 gamma". So "Rec. 709" in DCP-o-matic means **gamma 2.2**, not the broadcast OETF and not 2.4. This corrects the sentence in Summary item 5 that said the mapping was unverified.
- **Default trap (source).** When a file is added, `FFmpegContent::set_default_colour_conversion()` picks the preset from the file's colourspace tag: BT.709 gives **Rec. 709 (gamma 2.2)**; BT.601-type tags give Rec. 601; BT.2020 gives Rec. 2020; untagged files give Rec. 601 if the width is under 1080, otherwise Rec. 709. So a correctly tagged BT.709 ProRes master opens on the 2.2 preset. **A film graded on a 2.4 (BT.1886-style) monitor needs the preset changed to Rec. 1886 by hand** (or `--colourspace rec1886` on the command line, which applies to the next file given) [21].
- **How much it matters (computed).** Everything after the input gamma is identical in the two presets, so the linear-light ratio of the Rec. 709 preset to the Rec. 1886 preset for the same signal v is exactly v^(2.2-2.4):

| Signal level (0 to 1) | Linear light, 2.2 preset / 2.4 preset |
|---|---|
| 0.10 | 1.585 (59% brighter) |
| 0.25 | 1.320 |
| 0.50 | 1.149 |
| 0.75 | 1.059 |
| 0.90 | 1.021 |

 So choosing the wrong preset lifts shadows and midtones, not highlights. This matches the 58% figure for a dark value on a 2.2 display in `research/cinematic-quality.md`. Recommendation unchanged and now sourced: grade on a 2.4 reference, tag the master BT.709, set **Rec. 1886** and Range Video, and check a colour-patch frame in the DCP-o-matic preview before the long encode.
- The default selection also confirms the manual's table: Rec. 709 is suggested for "High-definition content including Blu-Ray rips" and the presets list in the manual names Rec. 1886 without a suggestion (read from `doc/manual/dcpomatic.xml`) [92].

**ProRes 422 HQ `.mov` import.**
- The manual says content can be "Movie files in almost any common format (e.g. MP4, MOV, MKV, etc.)" (read from file) [92].
- The code treats 10-bit 4:2:2 (`yuv422p10le`, what ProRes 422 HQ decodes to) as a YUV format in `FFmpegExaminer::yuv()` and in the image conversion paths in `src/lib/image.cc` (source).
- The project's own regression test `encode_xyz_from_prores_test` (`test/3042_regression_test.cc`) loads a `.mov` as content, builds a feature DCP and runs `make_and_verify_dcp`, then compares one frame against a DCP made from TIFFs (source). The test data file is private, so I could not confirm it is ProRes 422 HQ exactly.
- DCP-o-matic also exports ProRes HQ itself (`ExportFormat::PRORES_HQ`, used in `test/video_level_test.cc`) (source).
- **Verdict: supported by the code and covered by a regression test; not run by me. Still do the December test with a 5-second clip** (cheap, and it will also show the ISDCF name and verify result). A Windows-specific failure would not show in these tests (UNVERIFIED).

**Memory and encode speed on Windows.**
- No figure for either appears in the manual or the 2.18.51 release notes [94] (the notes list Disk Writer, VF and ISDCF-name changes only).
- **Threads (source):** the default number of encoding threads is `max(2, hardware_concurrency)` (`src/lib/config.cc`). The decoder waits when the queue holds `2 x threads + 1` frames (`j2k_encoder.cc`). The writer holds up to `threads x 3` finished frames in memory, adjustable as "Maximum number of frames to store per thread" (manual, `writer.cc`). Finished J2K frames are small (about 0.65 MB each at 125 Mbit/s and 24 fps, computed).
- **Per-encoder memory (measured proxy).** In the container, one frame-at-a-time 1998x1080 XYZ 12-bit JPEG2000 encode through ffmpeg's OpenJPEG wrapper peaked at about 514 MB, against 173 MB for the same filter chain written as raw video. So the J2K encoder added about 340 MB [96]. If DCP-o-matic's own encoder threads cost something similar, 8 threads would need roughly 3 GB, plus the frame queue and the GUI (inference). **Planning figure: 2 to 4 GB of RAM for the encode on a 4 to 8 core PC, less with fewer threads. UNVERIFIED on Windows; read Task Manager during the December test clip.**
- **Speed (measured proxy, unchanged).** Round-1 timings stand: about 3 to 4 wall minutes per finished minute on 4 vCPUs for clean frames, about 12 for grainy ones [47][96]. A clean 24-frame run took 3.3 s and a noisy one 11.4 s in this round's memory test, consistent with that. DCP-o-matic's own speed on Windows is **UNVERIFIED**.
- **GPU option (source).** The source supports the Grok GPU encoder only when built with `--enable-grok`, and it contacts a licence server. The standard Windows installer is not known to include it (UNVERIFIED). Do not plan on a GPU.
- **Use the 64-bit Windows installer.** The manual says the 32-bit build "may crash ... on a CPU with more than 4 cores" (read from file) [92].
- **Disk Writer on Windows.** 2.18.51 fixes "corrupted writes on the second and subsequent DCPs copied between re-starts", "potential fixes for corrupted writes in some rare situations", ejects the drive on completion and makes it "harder to accidentally overwrite the C: drive" [94]. This supports using the Disk Writer, but the earlier rule stands: **verify the written drive from the drive, not from the source folder**, and (inference from the fix wording) restart the Disk Writer between drives.

**Other small closures from the source.**
- A "short" content type exists: `SHR` (and `FTR`, `TLR`, `TST`, `XSN` and others) in `dcp_content_type.cc`; the create command's `-c SHR` accepts it (source). The earlier note "verify in the dialog" is closed.
- The create command (`dcpomatic2_create`) options listed in Finding 4 all exist in 2.18.51: `--colourspace`, `--container-ratio`, `-f`, `--twok`, `--fourk`, `-a`, `--no-encrypt`, `--no-use-isdcf-name`, `--video-bit-rate` (accepted range 10 up to the configured maximum), `--standard`, `-o` (source, `src/lib/create_cli.cc`). They are still UNTESTED by running.

### FU-2. Windows 11: 24 Hz refresh rate, and what the maker's laptop offers

- **Path.** Microsoft's HDR page says display settings are at "Settings > System > Display" (Windows 11) [42]. From there, the refresh-rate list is, from general Windows 11 knowledge, under **Advanced display** (in "Related settings") with the external display selected, in the **"Choose a refresh rate"** menu. **I could not confirm the last two steps on a Microsoft page:** the Microsoft Support navigation lists a "Display refresh rate" article [42], but its URL returned 404 to both fetch methods I tried (UNVERIFIED). The maker should photograph the real menu on the PC; the Win+P step in Finding 5 stays.
- **What can appear.** The list holds only modes the connected display reports. CTA-861 defines, at 1920x1080: 23.98/24 Hz (VIC 32), 25, 29.97/30, 50, 59.94/60, 100, 119.88/120 (VIC 63) and **47.96/48 Hz (VIC 111)**. It defines **no 72 Hz** mode [97]. So over HDMI to a TV or projector, 24, 48 and 120 Hz are plausible and 72 Hz is unlikely unless the display or driver adds a custom mode (inference). An external monitor or a laptop's own panel can offer other rates.
- **The maker's laptop.** Its model and the venue's display are unknown, so which of 24, 48, 72 and 120 Hz it offers over HDMI **cannot be answered from the web. It needs one input from the maker: the laptop model (and port type: HDMI version, or USB-C/DisplayPort with an adapter).** A five-minute check: plug into any HDMI TV, open the menu above, photograph the list. The venue's own display decides the final answer, so repeat at the rehearsal (Finding 5).
- **23.976 versus 24.** CTA-861 lists "23.98/24" together, and the mode a display really runs may be 23.976. Against a true 24.000 fps file that is a mismatch of 0.024 fps: one repeated or dropped frame about every 42 seconds (computed). mpv's `--video-sync=display-resample` removes it at the cost of a tiny speed change [41].

### FU-3. ISDCF name when only L and R are mapped in a 6-channel container

- **Answer: `_20`, not `_51`** (source). `Film::isdcf_name()` calls `mapped_audio_channels()`, which lists only output channels that some content actually maps to, then `audio_channel_types()` counts mapped front/surround channels (L, R, C, Ls, Rs, back-surrounds) as the first digit and mapped LFE as the second. LFE and others unmapped add nothing. The container size (6) only decides which mapped channels count.
- **Test evidence (source):** `isdcf_name_test` builds a film with `set_audio_channels(6)` and a mono file mapped to centre: the name carries `_10`; adding Left gives `_20`; Right `_30`; LFE `_31`; Ls `_41`; Rs `_51` (the field sits after the territory-rating part: `...US-R_20_4K_DI_...`).
- **For a stereo ProRes** the default mapping is 1:1 (input 0 to L, input 1 to R), so the name is `_20` with no changes. A mono file would map to **centre** and give `_10` unless remapped (`AudioMapping::make_default`, source).
- No mapped channels gives `_MOS`. `-HI` and `-VI` are added only if those channels are mapped.
- Remaining detail: the 6-channel MXF still carries the four silent channels (inference from `audio_channels()` = 6); a 2-channel setting also exists in the dialog and CLI (`-a 2`). Whether a particular cinema server prefers one of them is a question for the cinema (Template 2b).

### FU-4. Music inside a film shown at a hired hall: collecting-society statements

**Not retrievable this round:** ASCAP (403), BMI (403), IPRS (403), PRS for Music's main site (returns only a page title, no content). I did not route around the blocks. For the US, a weak secondary page says venue types "such as theaters and radio, are usually negotiated directly with the rights holder" [116]; treat it as UNVERIFIED, not as an ASCAP/BMI statement.

**UK, from PPL PRS's own site (pplprs.co.uk) and PPL:**
- TheMusicLicence "allows you to legally play music for employees or customers in your business through the radio, TV, other digital devices and live performances" [99]. **Film, cinema, synchronisation and hired halls are not mentioned** [99][100]. The Help page says no FAQ covers cinemas or DVDs [98].
- The Help page lists **MPLC** as the separate licence that "Covers your business premises for the public performance of copyright material contained within films" [98]. That is a film-showing licence for other people's films; it is not a music-clearance for a new film.
- **Temporary permits.** New customers can get "a temporary permit to cover the music usage at the event" (phone 0116 290 0525; no price stated) [98]. Existing licence holders ask to amend the licence. Charity and community events "may be able to get a discount" [98]. A hall that already holds TheMusicLicence should be asked in writing whether a film's soundtrack is within it.
- **A third-party statement (not PRS itself):** the UK charity Cinema For All's 2024 starter pack says the PRS/PPL licence "covers the copyright of any music used in your chosen film, plus any additional music you want to play" and that "Venues obtain this licence from PRS Music or PPL" [101]. This is about screening an existing licensed feature. **It does not clear the music inside a new film: the maker still needs sync (composition) and master (recording) permission from the rights holders, in writing, before the premiere** (Finding 6.1, music-sound).
- **Net for the maker (inference):** no collecting-society page I could read says that a venue licence covers music inside a privately made film. The safe line is unchanged: use music that is licensed for this public use (or original or public-domain-with-a-cleared-recording), keep a log of each permission, and ask the venue and PPL PRS (or the local society) the exact question in writing.

### FU-5. Public liability and E&O for a one-off four-wall cinema hire

**TD-7 (country) is still open, so this is a map, not an answer.**
- **What the cinema chains' own pages say.** The hire pages I read earlier (Picturehouse, Everyman, Cinemark) list no insurance rule or price [89][90][91]. This round Odeon, Curzon, Vue and AMC returned 403 and could not be read.
- **Public liability (UK).** A UK community-cinema starter pack states a group "need[s] to have" public liability insurance and "it is best to not rely on the Public Liability Insurance of your venue, as their policies might not cover all of your activity"; cost "depends on ... size of venue and who you are working with" [101]. It gives no limit. So the practical expectation is "have your own public-liability cover, or ask the venue in writing whether theirs covers a hirer's event". For a one-off, a short-event policy from a broker is the usual route (no price found; UNVERIFIED).
- **UK licensing points from the same pack [101]:** in Scotland "any venue showing films will need to apply for an annual Cinema Licence" under the Cinemas Act 1985 (not-for-profit groups can seek an exemption); Northern Ireland needs a Cinema Licence in some cases; the venue needs a council premises licence; films shown must respect the BBFC age certificate ("It is against the law to screen films to anyone under the age of the BBFC age certificate"). **For a self-made film with no BBFC certificate, ask the venue and the council how an unclassified film is handled** (UNVERIFIED for England and Wales). The pack also shows a film licence for third-party films costs "between £97 and £140" [101]; that does not apply to the maker's own film.
- **India (secondary only).** A public exhibition of a film in India needs certification by the CBFC under the Cinematograph Act 1952; the page I could read does not say whether a private invitation-only screening is exempt [110]. If the premiere is in India, ask the venue about certification before booking (UNVERIFIED).
- **US.** Nothing sourced for cinema private-rental insurance or a venue's certificate-of-insurance request. UNVERIFIED.
- **E&O is a distribution requirement, not a hire requirement.** Distributors, sales agents and streaming platforms require it [77][78][102]; none of the hire pages I read mentions it (inference: a one-off, non-sold premiere is unlikely to need it, but a venue that charges admission or a later festival or online release may ask).
- **2026 premium range (vendor page, not a broker quote).** Wrapbook's guide (page "last updated October 1, 2025") says "E&O policies often range from **$2,500 to $10,000** for a standard **three-year term with a $1 million limit**", typical limits "start around $1 million per claim and $3 million in aggregate", and it does not give separate prices for short films [102]. This agrees with the only earlier figure, IDA 2017's "$2,500 or more" [78]. HUB International's entertainment page (the IDA's insurer) names E&O as covering "copyright, defamation and privacy claims" and lists no price [103]; the IDA insurance page lists production general liability of "$1 million per occurrence / $2 million aggregate" and no E&O price [84]. USD, US-market figures; a UK or Indian quote will differ. **No short-film-specific 2026 premium found: UNVERIFIED.**
- **Questions to put to a cinema (add to Templates 2b):** do you require the hirer's public-liability certificate and at what limit; does your policy cover a hirer's own content and invited public; is an unclassified or uncertified film allowed (BBFC/CBFC or local rule); does the film need any rights declaration; who is liable for music and photographs in the film; what is the cancellation and technical-rehearsal policy.

### FU-6. EU AI Act, the AI Omnibus and Article 50

- **The Omnibus is Regulation (EU) 2026/1744**, done at Strasbourg 8 July 2026; it enters into force "on the third day following that of its publication" (read through the fetch tool) [104]. The Commission page says it "entered into force on 27 July 2026" [66].
- **What it changed for Article 50.** (1) A new transitional rule, Article 111(4): providers of generative systems "placed on the market before 2 August 2026" must "take the necessary steps in order to comply with Article 50(2) by **2 December 2026**" [104]. Article 50(2) is the duty to mark synthetic output in a machine-readable way, and it falls on the **providers** of the generator, not the film-maker. (2) Article 50(7) is replaced (the Commission encourages codes of practice on marking and labelling) [104]. **I found no change to Article 50(4)**, the deployer duty to disclose deep fakes, in the answers I got; both halves of the instrument went through the fetch tool, which answers only the questions I put to it, so this is **not a line-by-line read** and "no change found" is not conclusive (UNVERIFIED) [104]. The Commission page says "the transparency rules of the AI Act will come into effect in August 2026" and does not mention any Article 50 change [66].
- **High-risk dates moved** (not our track): Annex III systems from 2 December 2027, Annex I from 2 August 2028 [66][104]. Article 5 additions apply from 2 December 2026 [104].
- **Is a private individual a "deployer"?** Article 3(4): a deployer is anyone "using an AI system under its authority except where the AI system is used in the course of a personal non-professional activity" (read through the fetch tool) [105]. Article 2(10): the Regulation "does not apply to obligations of deployers ... who are natural persons using AI systems in the course of a purely personal non-professional activity" [106]. So a private person making a free tribute to their mother is outside the deployer duties **if** it is a personal, non-professional activity. The Act does not define that phrase. Whether a free event at a "mostly public" gathering still counts is **not settled in anything I read (UNVERIFIED; inference: likely yes if non-commercial and unpaid, less clear if tickets, sponsors or a later release)**.
- **Territory.** The Regulation reaches providers and deployers "located in a third country" only where the output "is used in the Union" [106]. If the premiere is outside the EU, it applies only if the film is shown in the EU. TD-7 decides.
- **If it did apply.** Article 50(4) duty for deep fakes: "disclose that the content has been artificially generated or manipulated", and for an evidently artistic, creative or fictional work the duty "is limited to disclosure of the existence of such generated or manipulated content" in a way that does not hamper enjoyment; information must be given "at the latest at the time of the first interaction or exposure" [65][105]. The existing plan (a single honest line in the pre-roll and end credits, cue sheet per ai-imagery) already meets that spirit; no new work needed. A deep fake is defined as content that "would falsely appear to a person to be authentic or truthful" [105]; visibly reconstructed, stylised scenes labelled L5 are the opposite of that (inference).

### FU-7. Commissioned photographs (India s.17(b)) and post-mortem image and privacy rules

**India Copyright Act 1957, s.17 proviso (b), read word for word from the government-hosted PDF [70] (text extracted with pdftotext):**
> "(b) subject to the provisions of clause (a), in the case of a photograph taken, or a painting or portrait drawn, or an engraving or a cinematograph film made, for valuable consideration at the instance of any person, such person shall, in the absence of any agreement to the contrary, be the first owner of the copyright therein;"

- Matches what Summary item 13 said. Two additions: it covers **paintings, portraits, engravings and cinematograph films** as well as photographs, and so also applies to anyone the maker pays to make a film or artwork (the maker is first owner absent contrary agreement; put the agreement in writing anyway). In s.2(d) the "author" of a photograph is "the person taking the photograph" and of a computer-generated work "the person who causes the work to be created" [70].
- **Currency caveat.** This copy includes the 2012 amendment (it notes the repeal of s.25 "w.e.f. 21-6-2012") but still refers to the "Appellate Board", so it predates the later tribunal changes. India Code (the official consolidated site) timed out or returned 403 in this round, and another government host returned 404. I found no statement that s.17(b) was amended after 1957 but cannot confirm the in-force text on today's date: **UNVERIFIED as "current"**. Wikipedia says the most recent amendment was 2012 [115] (secondary, undated).
- **The family case.** A studio portrait or a wedding photograph that a relative paid for "at the instance of" that relative belongs, absent agreement, to the commissioner (the relative or their heirs), not the photographer. So in India the right person to ask is the one who paid, not the photographer. Elsewhere (US, UK) the photographer is generally the first owner (Finding 6.2).

**UK.**
- **No data-protection claim for the dead:** the ICO says "Information about a deceased person does not constitute personal data and therefore is not subject to the UK GDPR" [108]. (Living relatives who appear are still covered by data protection and the privacy tort; Finding 6.5.)
- **A commissioner's privacy right in a photograph or film (CDPA 1988 s.85), still in force:** a person who "for private and domestic purposes commissions the taking of a photograph or the making of a film" has the right not to have copies issued to the public, the work exhibited or shown in public, or communicated to the public, where copyright subsists [109]. **This matters here:** a family portrait or a wedding film commissioned privately by a relative cannot be shown at a public gathering without that commissioner's consent, even if the maker has the photographer's licence. The page does not say what happens to this right when the commissioner dies, and I did not read s.95; UNVERIFIED [109].
- **No general UK image right.** I found no source for a post-mortem image right in the UK; the only general statement I could read is that "in common law jurisdictions, publicity rights fall into the realm of the tort of passing off" [71]. So for a dead relative, the live constraints are family dignity, the copyright points above, and defamation or confidence claims by living people. (Defamation of the dead was not checked: UNVERIFIED.)

**India.**
- **Delhi High Court, *Krishna Kishore Singh v. Sarla A. Saraogi*, 11 July 2023 (C. Hari Shankar J.), an interim ruling about a film on the late actor Sushant Singh Rajput [107].** The court held the rights asserted "are not heritable. They died with the death of SSR" (para 21.2) and that "Reputation, personality, and privacy and personality rights that emanate therefrom, are not heritable" (para 20(xiv)); refused an injunction against the film ("The IA is, therefore, dismissed", para 24); and kept the suit alive only for damages (para 25) [107]. It also records the principle that "once a matter becomes a matter of public record, the right to privacy no longer subsists" (para 19.4.8, quoting *R. Rajagopal*) [107].
- **Limits.** It is one judge's interim ruling, about a public figure and a film built from public material; it is not a statement about private family photographs or about a living person; other courts and later cases may differ; and a disclaimer "plainly untrue" was "worth tinsel" (para 18.7) [107], so a film that presents real events must not rely on a disclaimer. Delhi High Court cases protecting living celebrities' personality rights in 2026 are reported in a secondary source [71]. **Practical reading (inference): in India the dead have weaker personality claims than in Germany (KUG, 10 years [68]); the constraints that remain are copyright (who paid for the photograph), living relatives, and defamation.** The Digital Personal Data Protection Act 2023 was not read this round (UNVERIFIED).
- **Dignity still governs.** Charter principle 5 stays: nothing a mother or the closest family would not want shown to a public audience goes in, whatever the law allows.

### FU-8. How personal-documentary makers handle relatives' photographs and voices at public screenings (testing the Tier B synthesis)

**What I found is partial; no source documents a family-film maker's own clearance routine for relatives' photographs at a public screening.** What exists:

1. ***Tarnation* (Jonathan Caouette, 2003).** Made from "over 20 years of hundreds of hours of old Super 8 footage, VHS videotape, photographs", initially for "a total budget of $218.32, using free iMovie software"; Roger Ebert is quoted that "$400,000 more was eventually spent by the distributor on sound, print, score and music/clip clearances" to reach theatres [111]. **Lesson: a home-made family film is cheap until it goes public; the bill is music and clip clearance, not family material.** This supports Tier B's rule "build the public cut from cleared or low-risk assets" and the plan to avoid commercial songs in the shared cut. The page does not say how the mother's consent was handled.
2. ***Stories We Tell* (Sarah Polley, 2012).** Polley wanted "the story told in the words of everyone I could find who could speak about it", declined a "voice of God" narration, asked journalists to keep the story private until she was "ready to tell it in my own words" [113]; the film uses interviews with relatives, her father reading his own memoir, and **new Super 8 footage "shot to look like home movies"** with an actor as her late mother [112]. **Lessons for this project:** (a) the maker controlled when and how the story went public; (b) re-created home movies are a recognised device, but the project's rule (Charter principle 4) is that reconstructions are visibly reconstructions; (c) every voice in the film was a living person speaking for themselves. The sources I read do not say how consent from relatives was recorded (UNVERIFIED).
3. **Oral history practice for relatives' voices (documented professional norm) [114].** The Oral History Association's best practices: "obtaining and documenting the informed consent of the narrator"; narrators learn "the potential uses of the oral history"; "The interviewer should secure a signed legal release form, ideally when the interview is completed"; interviewers must "respect the rights of interviewees to refuse to discuss certain subjects, to restrict access to the interview"; where possible give the narrator "an opportunity to approve the oral history prior to public release." It does not address dead or withdrawing narrators. **This tests the Tier B voice rule well:** the surprise means the "uses" cannot be fully told up front, so the safe route is the one already planned: record only what can be said truthfully now; then after the premiere obtain a signed release before any further showing (Finding 8), and let the person view and approve their segment where they can.
4. IDA's amateur-footage note (earlier [80]) remains the only source for "creator owns; stills rarely get fair use".

**Verdict on the Tier B synthesis.** The two film accounts and the oral-history norm are consistent with it (early, honest, narrow asks; cleared assets in the public cut; post-event releases). They do not prove it. The risk ladder in Finding 6 therefore keeps its "synthesis" label. **No source tests the surprise element itself, a premiere that the main subject does not know about.**

### Changes to the earlier text in this file

| Earlier statement | Now |
|---|---|
| Summary 5 / Finding 2: preset gamma "UNVERIFIED" | Rec. 709 preset = gamma 2.2; Rec. 1886 preset = gamma 2.4; output 2.6; default for BT.709-tagged files is the 2.2 preset, so switch to Rec. 1886 by hand (FU-1). |
| Finding 4 step 2: ProRes import "UNVERIFIED" | Supported in code and regression tests; run the December clip test (FU-1). |
| Finding 4 step 3: ISDCF "20 versus 51" "UNVERIFIED" | `_20` with only L and R mapped (FU-3). |
| Finding 4: "short" content type "verify in the dialog" | `SHR` exists (FU-1). |
| Finding 4: DCP-o-matic Windows memory unverified | Planning figure 2 to 4 GB RAM; measure in December (FU-1). |
| Finding 5: Windows 24 Hz Settings path UNVERIFIED | Settings > System > Display confirmed; Advanced display > Choose a refresh rate is from general knowledge; 72 Hz is not an HDMI standard mode (FU-2). |
| Summary 13: India s.17(b) | Text confirmed word for word; also covers paintings, portraits, engravings and films; "current" still unverified (FU-7). |
| Summary 14: 2026 E&O premium UNVERIFIED | Vendor range $2,500 to $10,000, 3 years, $1M limit; no short-film price (FU-5). |
| Finding 6.5: UK and India post-mortem | UK: no data-protection claim for the dead, CDPA s.85 commissioner's privacy right applies to commissioned photos and films; India: Delhi HC 2023 says personality and privacy rights are not heritable (interim) (FU-7). |
| Open question: EU AI Omnibus and "deployer" | Omnibus adds a 2 Dec 2026 transition for Article 50(2) marking by providers; a person in a personal non-professional activity is outside the deployer duties (FU-6). |

### Still open after round 1

- **Inputs only the maker can give:** TD-7 country (decides insurance, licences, certification, AI Act territory); the laptop model and the venue's display and inputs; whether the premiere stays public-and-free or becomes invite-only.
- **UNVERIFIED:** ASCAP, BMI, IPRS and PRS for Music statements on films (403 or script-rendered pages); the Microsoft refresh-rate article; DCP-o-matic's own speed and memory on Windows; India Act currency after 2012; UK s.95 transmission of the s.85 right; unclassified-film rules for UK halls; US and India cinema hire insurance; a short-film E&O quote; Article 50(4) in Regulation 2026/1744 (no line-by-line read); India DPDP Act; a family-film maker's explicit clearance routine.
- **Suggested next steps (all cheap):** (1) a December 5-second ProRes test on the PC with Task Manager open (colour preset, ISDCF name, Verify DCP, memory, time); (2) ask a venue or a UK/EU/US/Indian PRO the written music question in FU-4 once TD-7 is set; (3) one broker quote for short-event public liability and, only if a later release is planned, short-film E&O.

### New sources (continuing the numbering)

[92] DCP-o-matic source, tag v2.18.51 — https://github.com/cth103/dcpomatic — shallow clone read 2026-10-18; HEAD = tag `v2.18.51`, commit 920fb9b, 2026-10-16 — files read: `src/lib/colour_conversion.cc`, `ffmpeg_content.cc`, `ffmpeg_examiner.cc`, `film.cc`, `util.cc`, `audio_mapping.cc`, `dcp_content_type.cc`, `config.cc`, `j2k_encoder.cc`, `writer.cc`, `create_cli.cc`, `test/3042_regression_test.cc`, `test/isdcf_name_test.cc`, `test/video_level_test.cc`, `doc/manual/dcpomatic.xml`.
[93] libdcp source — https://github.com/cth103/libdcp — shallow clone of the main branch, commit 891facc, 2026-10-01 — `src/colour_conversion.cc`, `src/gamma_transfer_function.cc`. DCP-o-matic 2.18.51 requires libdcp 1.9.22 or newer (`wscript`); I did not read the exact 1.9.22 tag.
[94] DCP-o-matic release notes for 2.18.51 — https://dcpomatic.com/release-notes?v=2.18.51 — 2026-10-18 — Disk Writer fixes on Windows, VF fixes, multi-language ISDCF name, audio-only export; no mention of ProRes, memory or speed.
[95] DCP-o-matic download page and the Ubuntu 24.04 command-line package (`dcpomatic-cli_1+2.18.51-1_amd64.deb`, 79,411,378 bytes) — https://dcpomatic.com/download and https://dcpomatic.com/dl?id=ubuntu-24.04-x86-cli&version=2.18.51 — 2026-10-18 — downloaded, not installed, launch attempts failed and the session's permission system declined a further step; files deleted.
[96] Own measurements in the cloud container, 2026-10-18 — ffmpeg 6.1.1 with `libopenjpeg -cinema_mode 2k_24`, 1998x1080 `xyz12le`, 24 frames; peak resident memory 514 MB (J2K) against 173 MB (raw video, same filters); wall 3.3 s clean and 11.4 s noisy; scripts in the session scratchpad (`measure_rss2.py`). Proxy only; not DCP-o-matic.
[97] Wikipedia, CTA-861 — https://en.wikipedia.org/wiki/CTA-861 — 2026-10-18 — secondary: 1080p24 (VIC 32), 1080p48 (VIC 111), 1080p120 (VIC 63); no 72 Hz.
[98] PPL PRS, Help — https://pplprs.co.uk/help/ — 2026-10-18 — MPLC listed as separate licence for films; temporary event permit; phone numbers; no cinema or DVD FAQ.
[99] PPL PRS, TheMusicLicence — https://pplprs.co.uk/themusiclicence/ — 2026-10-18 — coverage statement; film and cinema not mentioned.
[100] PPL, Playing music in a workplace or venue — https://www.ppluk.com/licensing/playing-music-in-a-workplace-or-venue/ — 2026-10-18 — silent on films and hired halls.
[101] Cinema For All, "How To Start a Community Cinema" starter pack — https://cinemaforall.org.uk/app/uploads/2024/05/How-to-Start-a-Community-Cinema-2024.pdf — upload path dated May 2024; downloaded and read 2026-10-18 — public liability, Cinemas Act 1985 (Scotland), premises licence, PRS statement, BBFC, film licence £97 to £140.
[102] Wrapbook, errors and omissions insurance guide — https://www.wrapbook.com/blog/errors-and-omissions-insurance — "last updated October 1, 2025" per the fetch — $2,500 to $10,000, three-year term, $1M limit; $1M/$3M typical. A production-services vendor page, not a broker quote.
[103] HUB International, Entertainment — https://www.hubinternational.com/en-us/industries/entertainment-insurance/ — 2026-10-18 — E&O described; no price or limit.
[104] Regulation (EU) 2026/1744 (AI Omnibus), EUR-Lex — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744 — done at Strasbourg 8 July 2026 — Article 111(4), Article 50(7), Article 113; both halves of the text went through the fetch tool with targeted questions, not read line by line.
[105] AI Act, Article 3 (definitions) — https://artificialintelligenceact.eu/article/3/ — 2026-10-18 — deployer, provider, deep fake; consolidated text of Regulation 2024/1689 before the Omnibus.
[106] AI Act, Article 2 (scope) — https://artificialintelligenceact.eu/article/2/ — 2026-10-18 — 2(1)(c) third-country outputs; 2(10) personal non-professional use.
[107] Krishna Kishore Singh v. Sarla A. Saraogi & Ors., Delhi High Court, 11 July 2023 — https://indiankanoon.org/doc/71066966/ — 2026-10-18 — paras 18.7, 19.4.8, 20(xiv), 21.2, 21.5, 24, 25 (read through the fetch tool; an interim order).
[108] ICO, "What is personal information? A guide" — https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-information-a-guide/ — 2026-10-18 — deceased persons.
[109] Copyright, Designs and Patents Act 1988, s.85 — https://www.legislation.gov.uk/ukpga/1988/48/section/85 — 2026-10-18 — "no known outstanding effects"; commissioner's privacy right.
[110] Wikipedia, Central Board of Film Certification — https://en.wikipedia.org/wiki/Central_Board_of_Film_Certification — 2026-10-18 — secondary: films "may only be publicly exhibited in India after certification by the board".
[111] Wikipedia, Tarnation (2003 film) — https://en.wikipedia.org/wiki/Tarnation_(2003_film) — 2026-10-18 — secondary: $218.32 budget, later clearances.
[112] Wikipedia, Stories We Tell — https://en.wikipedia.org/wiki/Stories_We_Tell — 2026-10-18 — secondary: re-created Super 8, actor as mother, narration.
[113] Sarah Polley, "Stories We Tell: A post by Sarah Polley" (NFB blog) — http://blog.nfb.ca/2012/08/29/stories-we-tell-a-post-by-sarah-polley/ — 2012-08-29 — her own words on voices and privacy.
[114] Oral History Association, Oral History Best Practices — https://oralhistory.org/best-practices/ — 2026-10-18 — consent, releases, uses, restrictions, approval before release.
[115] Wikipedia, Copyright law of India — https://en.wikipedia.org/wiki/Copyright_law_of_India — 2026-10-18 — secondary: most recent amendment 2012.
[116] Wikipedia, Performance rights organisation — https://en.wikipedia.org/wiki/Performance_rights_organisation — 2026-10-18 — secondary and weak: venues such as theatres "usually negotiated directly with the rights holder".


## Follow-up research (round 2)

Researcher: Sonnet (Sonnet 5.5), track `theatrical-delivery`. Date: Sunday 2026-10-18. Maker: the only human on the project (relayed again, as written: "for now only me and i will only bne the one on this project"; who is in on the secret and who approves the hard chapters "can wait until the plan is ready"). Nothing here is legal advice. The country of the premiere (TD-7) is still not given anywhere in the repo (I searched the charter, playbooks, roadmap and reviews), so every legal item carries its jurisdiction.

**Method and limits of this round.**
- **WebSearch was unavailable** (the shared budget of 200 searches per turn was used up when I started; the call returned "budget used up"). I did not use search engines, archive services or readers as a workaround. I worked from pages and files fetched directly at known addresses. Where an address could not be guessed, the item stays UNVERIFIED.
- **A real DCP-o-matic run.** Round 1 could not run the program. This round I downloaded the official 2.18.51 Ubuntu 24.04 command-line package, unpacked it into the session scratchpad (not installed), supplied three missing libraries from the Ubuntu archive into the same scratchpad, and pointed the program at its own folders with environment variables (`APPDIR`, `LD_LIBRARY_PATH`). It runs: `dcpomatic2_create --version` prints "dcpomatic version 2.18.51 920fb9b044". I built and encoded real DCPs from a ProRes 422 HQ file, verified them, decoded a frame, and measured CPU and memory [117]. Scripts, commands and raw numbers are in `research/theatrical-delivery-fixtures/followup2-*`. Verbatim excerpts of the legal texts are in `research/sources/theatrical-delivery-round2-excerpts-2026-10-18.txt`.
- **What this is not.** It is the Linux command-line build in a cloud container (4 vCPU Intel Xeon 2.1 GHz, shared with other jobs: load average 8.8 to 10.6 during my timing runs, so **wall-clock times are inflated and I do not rely on them; CPU seconds are the stable figure**). It is not the maker's Windows PC and not the graphical program. Windows behaviour stays UNVERIFIED.
- Tags: **(run)** = observed in my test of the real 2.18.51 binary; **(source)** = read in the 2.18.51 code; **(file)** = read in a document I downloaded; **(page)** = read through the fetch tool, not re-checked word for word; **(computed)**; **(inference)**; **UNVERIFIED** = no primary source reached.

### FU2-1. DCP-o-matic 2.18.51: colour presets, ProRes import, memory and speed

**Which gamma each colour preset applies (run, source) [117][118].**

| Preset (`--colourspace` id) | Input gamma | Output gamma | Where in the code |
|---|---|---|---|
| Rec. 709 (`rec709`) | **2.2** (plain power law) | 2.6 | libdcp `src/colour_conversion.cc`, `rec709_to_xyz()` (starts line 90) |
| Rec. 1886 (`rec1886`) | **2.4** (plain power law) | 2.6 | same file, `rec1886_to_xyz()` (starts line 157); its own comment says "According to Olivier on DCP-o-matic bug #832, Rec. 1886 is Rec. 709 with 2.4 gamma" |
| Rec. 601 (`rec601`) | 2.2 | 2.6 | `rec601_to_xyz()` (line 74) |
| sRGB (`srgb`) | 2.4 piecewise (0.04045, 0.055, 12.92) | 2.6 | `srgb_to_xyz()` (line 58) |
| P3 DCI (`p3`) | 2.6 | 2.6 | `p3_dci_to_xyz()` |

This agrees with round 1 and now has three independent confirmations.
1. **The source** (libdcp commit 891facc, DCP-o-matic tag v2.18.51 commit 920fb9b) as above.
2. **The project files the real program wrote** (run): the `ColourConversion` block of `metadata.xml` says `Gamma 2.2` for a default film and for `--colourspace rec709`, and `Gamma 2.4` for `--colourspace rec1886`; primaries 0.64/0.33, 0.30/0.60, 0.15/0.06, white 0.3127/0.3290 and `OutputGamma 2.6` in all three.
3. **A test frame** (run). I made a ProRes 422 HQ clip of grey bars (signal 10, 25, 50, 75, 90 and 100 percent) tagged BT.709, built a DCP with each preset, decoded one J2K frame with ffmpeg and read the Y code (0 to 4095) at each bar. The ratio of linear light between the two presets matches the exact prediction v^(2.2 minus 2.4):

| Bar (signal) | Y code, Rec. 709 preset | Y code, Rec. 1886 preset | Linear-light ratio measured | Predicted |
|---|---|---|---|---|
| 0.102 | 570 | 478 | 1.580 | 1.580 |
| 0.251 | 1226 | 1102 | 1.319 | 1.318 |
| 0.502 | 2205 | 2090 | 1.149 | 1.148 |
| 0.749 | 3091 | 3022 | 1.060 | 1.060 |
| 0.902 | 3617 | 3587 | 1.022 | 1.021 |
| 1.000 | 3948 | 3947 | 1.001 | 1.000 |

 Measured codes sit about 0.3 percent under the model's absolute values (for example 3948 against 3960 for white), which is not a gamma difference. **Verdict: the wrong preset lifts shadows and midtones (about 58 percent at 10 percent signal), not highlights.**
- **Default trap confirmed (run).** A ProRes file tagged BT.709 opens on the **Rec. 709 preset (gamma 2.2)**: `dcpomatic2_cli dump` prints "colour conversion Rec. 709" for a default film, and `FFmpegContent::set_default_colour_conversion()` (`ffmpeg_content.cc` lines 493 to 525) does that for BT.709 tags. **A film graded on a 2.4 (BT.1886-style) monitor needs Rec. 1886 chosen by hand** (dialog, or `--colourspace rec1886` before the file on the command line). Recommendation unchanged and now tested: grade on a 2.4 reference, tag the master BT.709, set Rec. 1886, check a grey-bar frame in the preview before the long encode.

**Does a ProRes 422 HQ `.mov` import cleanly? Yes on the Linux build (run).** The clip was `codec_name=prores`, `profile=HQ`, `yuv422p10le`, 1920x1080, 24 fps, BT.709 tags, 24-bit stereo audio. `dcpomatic2_create` accepted it, `dump` showed "1920x1080, 24fps ... DCI Flat at 2K, 150Mbit/s, SMPTE unencrypted", the encode finished with exit 0, and **`dcpomatic2_verify_cli` printed "DCP verified OK." with no warnings** (checked two DCPs). Output picture: JPEG2000, 1998x1080, XYZ 12-bit, 24 fps; sound: PCM 24-bit, 48 kHz, 6 channels. The Windows build uses the same decoder code (inference), but a Windows-only failure would not show here: **UNVERIFIED on Windows. The December 5-second test on the PC stays on the plan.**
- **Defaults worth knowing (source, run).** The J2K bit-rate cap defaults to 150 Mbit/s (`film.cc` line 215), so a 15-minute film at the cap is about 16.9 GB for picture plus 0.8 GB for 6-channel sound, 17.7 GB in all (computed: 150 Mbit/s is 1.125 GB a minute; six 24-bit 48 kHz channels are 52 MB a minute). A 32 GB stick holds roughly 25 minutes at the cap before the file system overhead (computed). My grainy test sat exactly at the cap (picture file 93.8 MB for 5 s is 150.0 Mbit/s); the clean test came in at 119.7 Mbit/s; the flat colour bars at about 11 Mbit/s. The create command uses a 6-channel container by default (`AudioChannels 6`).

**Encode cost and memory (run).** Source: 1920x1080 ProRes 422 HQ, Flat 2K, 120 frames (5 seconds) per clip, command-line `make-dcp` with `-t` threads.

| Clip | Threads | Wall s (inflated by a loaded box) | CPU s (user + system) | CPU s per frame | Peak RAM |
|---|---|---|---|---|---|
| Flat colour bars (48 frames) | 4 | 5.2 | 0.8 | 0.017 | 269 MB |
| Clean synthetic picture, ProRes 66 Mbit/s | 1 / 2 / 4 | 50 / 40 / 71 | 48 / 51 / 51 | 0.40 / 0.43 / 0.43 | 314 / 438 / 690 MB |
| Same picture with strong grain, ProRes 186 Mbit/s | 1 / 2 / 4 | 145 / 110 / 145 | 142 / 145 / 152 | 1.19 / 1.21 / 1.27 | 322 / 442 / 695 MB |

- **Memory fit: about 190 MB plus about 125 MB per encoding thread** (command-line program; the graphical program adds its own, which I did not measure). The default thread count is `max(2, hardware threads)` (`config.cc` line 86), so a 16-thread PC would land near 2.2 GB (extrapolation, inference). **This replaces round 1's "2 to 4 GB" planning figure with a measured one: well under 1 GB at 4 threads, 2 to 3 GB at 16. Read Task Manager during the December test anyway.**
- **Speed: plan by CPU seconds per frame, not by minutes.** On this 2.1 GHz core the cost was 0.4 to 0.43 s per frame for clean detail and about 1.2 to 1.3 s per frame for heavy grain, and only 0.017 s for flat colour bars (so content complexity swings it by a factor of 70, and **grain baked into the master roughly triples the encode**). Wall minutes = frames x CPU-s per frame / (cores x speed relative to this core) / 60 (computed). For a 15-minute film (21,600 frames): clean 2.6 CPU-hours (39 minutes on 4 of these cores, 19 minutes on 8), grainy 7.6 CPU-hours (1.9 hours on 4, 57 minutes on 8). A modern laptop core is probably faster than this Xeon core, but I have no figure for the maker's PC: **UNVERIFIED**. Flat-colour animation will sit between the two measured clean and bar figures (inference).
- The DCP-o-matic forum front page [120] shows only the latest post per forum; no performance thread was reachable. The 2.18.51 release notes [94] mention none of this. So no forum figure.

### FU2-2. ISDCF name when only L and R are mapped in a 6-channel container

- **Answer: `_20`, tested on the real program (run).** A stereo ProRes with the default mapping (input 0 to L, input 1 to R) in the default 6-channel container produced `LJTest_SHR-1_F-178_XX-XX_20_2K_20261018_SMPTE_OV`. A mono WAV (maps to Centre) gave `..._F_XX-XX_10_...`; a 6-channel 5.1 WAV (1:1 mapping) gave `..._F_XX-XX_51_...`. This matches round 1's source reading and the test file `isdcf_name_test`; the code is `film.cc` lines 1127 to 1132 (`audio_channel_types(mapped_audio_channels(), audio_channels())`; no mapped channels gives `_MOS`) [118].
- **The name and the machine-readable metadata differ, on purpose (run).** The CPL inside the same DCP says `<meta:MainSoundConfiguration>51/L,R,-,-,-,-</meta:MainSoundConfiguration>`, and the sound file has 6 channels (ffprobe: `pcm_s24le`, 48000 Hz, 6 channels). The ISDCF registry page lists SOUNDFIELD values `51`, `71`, `SDS` and `M` for that CPL field, and lists the file-name codes `20` ("2.0 (Stereo)"), `51`, `71`, `10` ("1.0 (Center Channel Mono)"), `21`; for `20` it adds "Only discrete audio should be used in a DCP; matrixed audio, such as Lt/Rt, should not be used." (page) [119]. So a projectionist's server may show "5.1" while the file name says 20; both are correct.
- **Practical rule (inference).** A stereo film as L/R only gives a phantom centre. Dialogue-heavy cinema mixes usually rely on the centre speaker; ask the venue whether they want L/R only or dialogue also sent to Centre (Template 2b), and decide before the mix, not after.

### FU2-3. Windows 11: 24 Hz refresh rate on an external display; what the maker's laptop offers

- **Path (page) [42].** Microsoft's own HDR settings page, read again today, says for Windows 11: select "System > Display > Advanced display," and then, under "Choose a refresh rate," pick the rate (in that page it is describing a 30 Hz fallback, but the menu names and path are the ones to use). The same page links a "Display refresh rate" article by a relative address without its identifier; the address I could construct returned 404 (round 1 saw the same), so the dedicated article stays unread. The path is now sourced to a Microsoft page, not general knowledge. The external display must be selected first in Settings > System > Display (inference).
- **Which rates can appear.** Only modes that the display reports and the driver accepts (round 1, CTA-861 [97]: 23.98/24, 25, 29.97/30, 50, 59.94/60, 100, 119.88/120 and 47.96/48 Hz at 1080p; no 72 Hz mode). Nothing new this round.
- **The maker's laptop: cannot be answered from the web.** The repo names no laptop model, GPU or port (my search found only the Craft apps' GPU bug notes). I did not find a vendor page I could read that lists HDMI modes for a given laptop GPU (the Microsoft article address I could construct returned 404; one Intel support address I tried redirected to a "not found" redirector, which I did not follow). **Needed from the maker: the laptop model and which port goes to the screen.** A five-minute check on any HDMI TV: open the menu above, photograph the "Choose a refresh rate" list; repeat at the venue (TD-L2b).

### FU2-4. Venue-licence coverage of music inside a film shown at a hired hall

**Access.** ASCAP (`ascap.com` and `ascap.com/help/ascap-licensing`), BMI (`bmi.com` and `bmi.com/licensing`) and IPRS (`iprs.org`) returned 403 again; PRS for Music's home page returned only its title. I did not route around the blocks.

**UK: what the PPL PRS site and tariffs say (file, page) [121][122][123].**
- **PRS Tariff 'C' (Cinemas)** is the one PRS tariff written for film soundtracks. It covers "public performances of PRS for Music's repertoire given in the course of, or in connection with, the exhibition of films ... at cinemas or other premises at which the commercial exhibition of films regularly takes place on not fewer than three days weekly for a period of not less than four months during the year", including music in "the soundtrack of a film". It "does not apply to performances ... in connection with entertainments to which there is no charge for admission". The copy the site links is marked "Effective 1st January 2024" and "will expire on 30th June 2024", so I have not seen the current edition [121]. **A one-off hired hall is not a "cinema" under this tariff, and a free showing is excluded from it** (file).
- **PPL tariffs for one-off events (file).** PPLPP002 "Single and Casual Events", effective 1 October 2026 to 30 September 2027, is for sound recordings used "as background music" at one-off events (conferences, fetes and the like): £20.44 a day for an average attendance of 1 to 500, £40.88 for 501 to 2,000, plus VAT, with a minimum fee. PPL's cinema tariff PPLPP036 covers background music in intervals only [122].
- **TheMusicLicence "live events" page (page) [123].** It lists "film screening" among performance types and says the licence covers "any additional recorded music used at the event". It does not say whether a film's own soundtrack is within the licence, and it does not address hired halls or whether a venue's licence covers a hirer. The Help page still sends such questions to 0116 290 0525 [98].
- **Net for the UK (inference).** No PPL PRS page I could read says that a hall's music licence clears the soundtrack of a privately made film. And it would not be enough anyway: the composition (sync) and recording (master) permissions for each track are separate and in writing (Finding 6.1). Ask in writing: "Is the soundtrack of a film we bring and show once, free, to about [N] people covered by your licence, or by a temporary permit, or not?"

**US: a government statement exists, from the other direction (file) [124].** The US Copyright Office's 2015 report says "Source licenses are commonly used in the motion picture industry, because the PROs are prohibited from licensing public performance rights directly to movie theater owners. Instead, film producers license public performance rights for the music used in films at the same time as the synchronization rights, and pass the performance rights along to the theaters that will be showing their films", and that such source licences "do not typically encompass non-theatrical performances". **Reading (inference): in the US the performance right for music in a film is cleared at the sync stage, so the maker's sync licence should say it covers public performance at the premiere; a hired hall's ASCAP/BMI licence is not the place to rely on.** Nothing from ASCAP or BMI themselves: UNVERIFIED. The report is from February 2015 and may not reflect later changes.

**India: the Act, not IPRS (file) [70].** I could not read IPRS. The consolidated Act (a government-hosted copy whose PDF metadata is dated January 2018) has: (1) s.18(1), third proviso: authors of lyrics and music in a film cannot waive a share of royalties "for the utilization of such work in any form other than for the communication to the public of the work along with the cinematograph film in a cinema hall" (so use outside a cinema hall is where the authors' own royalty right bites); (2) s.52(1)(k): hearing a recording in public is not infringement when it is "as part of the activities of a club or similar organisation which is not established or conducted for profit", or in a residents' common hall; (3) s.52(1)(za): performances in "any bona fide religious ceremony or an official ceremony", with an explanation that includes "a marriage procession and other social festivities associated with a marriage". **A private birthday-style premiere at a hired hall is not named in any of these (inference); whether a non-cinema showing needs an IPRS permission is UNVERIFIED.** Ask the venue and IPRS in writing once TD-7 is India.

### FU2-5. Public liability and E&O for a one-off four-wall hire

**TD-7 is still open, so this is a map.**
- **Public liability.** No new numbers. The UK community-cinema starter pack [101] (round 1) remains the only source that states an expectation: have your own public liability cover and do not rely on the venue's. This round's broker pages add only that short-term event cover exists: Film Emporium (US broker) says "Options may include one-day or short-term event insurance, annual coverage for multiple events", "subject to eligibility, policy terms, and underwriting", "Events outside the United States require advance review", and gives no limits or prices (page) [130]. Front Row Insurance Brokers (Canada) lists a separate "Festival & Special Event Insurance" product with no details (page) [131]. **No venue-required limit and no one-day premium found: UNVERIFIED.** The question list in FU-5 (round 1) is still the right set to put to the venue.
- **E&O: the expectation is a distribution one.** Film Emporium: "Most distribution, broadcast, or licensing agreements require E&O insurance before delivery"; "Certain film festivals may also require an E&O policy to screen your production"; a footnote in the applications section of its home page says "E&O Coverage is for completed films entering a distribution deal"; its E&O page does not mention one-off screenings (page) [130]. Front Row (Canada): E&O "is commonly required by broadcasters, distributors, streaming platforms, and sales agents before release"; a policy term is "commonly one to three years"; its 30 June 2026 article says "In many cases, it's a requirement" and does not say festivals require it (page) [131]. **Reading (inference): a free, one-off premiere with no sale and no festival entry is not expected to need E&O; a later festival, cinema release or online release may.**
- **2026 premium range for a short from a broker page: not found.** Film Emporium's and Front Row's pages carry no premium, limit, minimum or deductible; they direct you to a quote. The only range is still the vendor page [102] (Wrapbook, last updated 1 October 2025: $2,500 to $10,000, three-year term, $1 million limit) and IDA 2017 [78] ("$2,500 or more"). **UNVERIFIED as a 2026 broker figure; one quote request is the only way to close it.**

### FU2-6. EU AI Omnibus and Article 50; is a private person a "deployer"?

**Omnibus: read line by line this time (file) [104].** Regulation (EU) 2026/1744, OJ L of 24.7.2026, "shall enter into force on the third day following that of its publication", that is 27 July 2026. In Regulation 2024/1689 it amends Article 50 **only in paragraph 7** (point 20: the Commission "shall encourage and facilitate" codes of practice on "detection, marking and labelling" and assess whether they are "adequate to ensure compliance with the obligations laid down in paragraphs 2 and 4"), and it adds **Article 111(4)**: providers of generative systems placed on the market before 2 August 2026 "shall take the necessary steps in order to comply with Article 50(2) by 2 December 2026". The string "Article 50" occurs nowhere else in the instrument. **So Article 50(4) (deployers disclose deep fakes), 50(5) (timing) and the artistic-work limit were not changed, and the timeline for deployers did not move: Article 50 applies from 2 August 2026** (Commission pages, "These transparency obligations apply from 2 August 2026") [127]. This closes round 1's "no line-by-line read" caveat. Article 50(2), the machine-readable marking duty, falls on the **providers** of the generator, with a four-month grace period for legacy tools.

**Is a private person showing a film at a public gathering a "deployer"? Probably not for Article 50(4), now with the Commission's own text (file) [126][127].**
- The law: Article 3(4) defines a deployer as using an AI system under its authority "except where the AI system is used in the course of a personal non-professional activity"; Article 2(10): the Regulation "does not apply to obligations of deployers who are natural persons using AI systems in the course of a purely personal non-professional activity"; recital 13 repeats it [126].
- **The Commission's Article 50 guidelines, C(2026) 5054 final, 20.7.2026, section 2.4.1 paragraph 19:** "Any activity through which natural persons gain an economic benefit on a regular basis or are otherwise involved in a professional, business, trade, occupational or freelance activity should be considered as a 'professional' activity", and "the person should act in both a personal and a non-professional capacity to fall within the scope of the exception". Its excluded examples are "individuals using an AI system to generate deep fakes of the members of their household" and "individuals using an AI system in their personal capacity to generate deep fakes disseminated on social media" [127]. The test is the person's capacity (money, trade, freelance), not the size of the audience; **dissemination to the public on social media is an example inside the exclusion** (file). Paragraph 20 adds that the **provider** of the tool still owes marking (its example is a deep fake on a personal Christmas card).
- **Reading (inference): a free, unpaid tribute by the maker, shown once at a gathering, is within "purely personal non-professional"; the guidelines give no example of a screening at a public event, so this is not settled in so many words (UNVERIFIED on that exact fact).** The exclusion would not hold for a paid or sponsored showing, a business or freelance involvement of the maker, or a hired studio acting as its own deployer (paragraph 19 on professionals; round 1's production-scale vendor route). Territory is unchanged from round 1: the Regulation reaches the film only if it is used in the Union [106].
- **If it applied, the film is already in good shape (file).** The deep-fake definition (Article 3(60)) is content that "would falsely appear to a person to be authentic or truthful"; guidelines paragraph 114 says the test is objective, needs no intent to deceive, and looks at the "intended and reasonably foreseeable audience": where that audience "does not expect content to be authentic or truthful", the deep-fake criterion "will not be fulfilled"; paragraph 122 lists "a movie, gaming environment, or virtual reality scene" among audience expectations. Stylised, visibly animated chapters labelled as reconstructions are the opposite of that (inference). If something is photoreal, the attenuated duty for "evidently artistic ... work" is "limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work"; the guidelines (paragraph 143) say disclosure "at the start of a video" is a first-exposure example and should be repeated later where people may miss the start (a public gathering with people arriving late is that case; inference). Paragraph 124: relying on the lighter duty "cannot be a justification for failing to respect" intellectual property or data protection rights. The existing pre-roll line and end credit already do this; no new work.
- **Code of practice (page) [128].** The Commission's code of practice on marking and labelling AI-generated content was finalised after the 10 June 2026 plenary; section 1 is for providers, section 2 for deployers. Voluntary; the page does not mention artistic works.

### FU2-7. India s.17(b) text; UK and India post-mortem image and privacy rules

- **India Copyright Act 1957, s.17 proviso (b), confirmed word for word (file) [70].** "(b) subject to the provisions of clause (a), in the case of a photograph taken, or a painting or portrait drawn, or an engraving or a cinematograph film made, for valuable consideration at the instance of any person, such person shall, in the absence of any agreement to the contrary, be the first owner of the copyright therein;" Same text as round 1.
- **Official and dated? Official, yes; dated only by its metadata.** The PDF is on the Copyright Office (DPIIT) site and its cover says "Copyright Office, Department Of Industrial Policy & Promotion"; the file's creation date is 24 January 2018 and last modification 22 February 2018 (PDF metadata). It shows the 2012 amendment (s.25 "Omitted ... w.e.f. 21-6-2012") but still says "Appellate Board". The official India Code (`indiacode.nic.in`) returned 403 for both the Act page and the section page, so I could not read an "as on" date. **Current as of today: UNVERIFIED** (no amendment to s.17(b) seen; the later tribunal reforms concern the Appellate Board, inference). Wikipedia's "most recent amendment 2012" [115] is the only other statement.
- **UK, new (page) [129].** The Law Reform (Miscellaneous Provisions) Act 1934 s.1(1) has the proviso "that this subsection shall not apply to causes of action for defamation": a defamation claim does not pass to an estate. That is about the dead person's own claim; **whether anyone can sue for defaming someone already dead was not sourced: UNVERIFIED.** Earlier points stand: no UK GDPR rights for the dead [108]; a commissioner's privacy right in a privately commissioned photograph or film under CDPA s.85 [109].
- **India, new (file) [125].** The Digital Personal Data Protection Act 2023 (gazette text, 11 August 2023): "Data Principal" is "the individual to whom the personal data relates" (s.2(j)), so it speaks of a living individual with a child and disability extension; the Act does "not apply to personal data processed by an individual for any personal or domestic purpose" (s.3(c)(i)); and s.14 lets a person nominate someone to exercise the rights "in the event of death or incapacity". Commencement is by notification (s.1(2)) and **I did not check whether or when it has begun: UNVERIFIED**. **Whether a showing at a mostly public gathering still counts as "personal or domestic" is not settled in anything I read: UNVERIFIED.** Round 1's Delhi High Court reading (personality and privacy rights not heritable, 2023, interim) [107] is unchanged. Dignity (Charter principle 5) governs beyond the law.

### FU2-8. Family-film clearance practice: documented accounts (testing the Tier B synthesis)

**Result: still partial. I found no first-person account of a maker's clearance routine for relatives' old photographs and voices.** What I could read:
1. **Sarah Polley, NFB blog, 29 August 2012, re-read today [113].** She controlled when the story went public (journalists kept it private until she was "ready to tell it in my own words"; no interviews until the theatrical release) and wanted it "told in the words of everyone I could find who could speak about it", declining "voice of God" narration. **The post does not say whether she asked relatives' permission, showed them the film or used home movies or photographs** (page). Round 1's statement stands.
2. **Kirsten Johnson, *Dick Johnson Is Dead* (2020), Wikipedia summary [133].** The film "incorporates Johnson family photographs and home movies", including footage of her late mother; the article says nothing about permission or clearance. Its only interview source, Vulture (29 January 2020), could not be fetched ("unable to fetch from www.vulture.com"), so this lead is open (secondary, UNVERIFIED).
3. **Oral History Society (UK), 2019 guidance [132] (page).** For voices: an "Interview Recording Agreement" that "needs to be signed by each interviewee", with a file holding "the pre-interview participation agreement and the post-interview recording agreement". The page I could read does not address relatives or the dead. Together with the US Oral History Association norm [114] this is a documented **two-stage paper trail: agree before, sign after**.
4. Round 1's *Tarnation* ($218.32 to make, about $400,000 of clearances later) [111] and the IDA note that the creator owns amateur footage and stills rarely get fair use [80] stand.

**Verdict on the Tier B synthesis: unchanged.** The documented practice (the maker controls timing; written agreements before and after; the cost arrives at public release) is consistent with it and does not contradict it, but it does not test the surprise element or the old-photograph case. Open leads for a later round if the maker wants more: the Vulture interview with Johnson, and the Center for Media & Social Impact report "Honest Truths: Documentary Filmmakers on Ethical Challenges in Their Work" (its address redirected to an archive service, which I did not use).

### FU2-9. Repo-wide check: where "Fri 19 Feb 2027 picture lock" is still written (for the orchestrator)

Picture lock (G-LOCK) is **Sat 6 Feb 2027** in `playbooks/production-scale.md` (Step 14, gate table, T9), `playbooks/music-sound.md`, `playbooks/cinematic-quality.md`, `skills/animation-production-planning/SKILL.md`, `ROADMAP.md` (lines 230 and 293 record the decision) and `reviews/02-film-briefs-review.md`. **Fri 19 Feb 2027 is the withdrawals-close date** (consent card 4a, music-sound removal deadline). My scan covered every `.md`, `.txt`, `.csv`, `.json`, `.py` and `.sh` file under `.` [134].

**A. Text that still calls 19 Feb the picture lock (patch these).**

| File and line | Text now | Patch to |
|---|---|---|
| `playbooks/surprise-ops.md` line 275 (key-dates table; the origin) | `Fri 19 Feb 2027 \| Withdrawals close; picture lock` | split into `Sat 6 Feb 2027 \| Picture lock (G-LOCK, production-scale)` and `Fri 19 Feb 2027 \| Withdrawals close (removals only after lock)` |
| `playbooks/theatrical-delivery.md` line 330 (T4 row TD-L7) | `Fri 19 Feb 2027 (picture lock)` | `Fri 19 Feb 2027 (withdrawals close; picture lock was Sat 6 Feb, G-LOCK)` |
| `research/theatrical-delivery.md` line 316 (Finding 7) | `before the Fri 19 Feb picture lock` | `after the Sat 6 Feb picture lock, before the Fri 19 Feb withdrawals close` |
| `research/theatrical-delivery.md` line 470 (Deliverable 3 row TD-L7) | `Fri 19 Feb 2027 (picture lock)` | same as the playbook row |
| `research/surprise-ops.md` line 644 (week 18 row) | `Fri Feb 19: withdrawals close; picture lock` | `Fri Feb 19: withdrawals close` (lock is Sat Feb 6 in week 16) |
| `research/surprise-ops.md` line 707 (T-7 row) | `Picture lock held since Feb 19` | `Picture lock held since Sat Feb 6` |
| `research/surprise-ops.md` line 927 (risk table) | `the build deadline (picture lock Feb 19) can stay` | `(picture lock Feb 6)` |

**B. Different late lock dates that conflict with G-LOCK (patch these too; the earlier guess of `story.md` and `format.md` was right, but their wording is not "19 Feb").**
- `playbooks/story.md` line 152 (timeline table): row `Feb 7 – Feb 20 | Review with the proxy. Veto window. | Lock.` puts the lock at the end of 20 Feb. Move "Lock" to the `Jan 3 – Feb 6` row (lock Sat 6 Feb) and keep Feb 7 to 20 as "removals only, then final consent confirmations", consistent with the roadmap addendum ("withdrawals after lock are removals only", `ROADMAP-ADDENDUM.md` line 215).
- `playbooks/format.md` line 89 (Step 13): heading `Picture lock, captions, music and mastering (weeks 16 and 17, 2027-01-31 to 2027-02-13)` lets the lock float to 13 Feb. Split: picture lock Sat 2027-02-06 (G-LOCK); then captions, music and mastering to 2027-02-13 (G-MIX Sat 13 Feb in `skills/animation-production-planning/SKILL.md` line 73).

**C. Leave alone (checked, not errors).**
- `playbooks/surprise-ops.md` line 352 (consent card: "Before Friday 19 February 2027 you can ask me to take anything out or change it") and `playbooks/music-sound.md` lines 144, 411, 452, 488 and the skill `skills/life-film-music-and-sound/SKILL.md` line 104: 19 Feb is the withdrawal date. Consistent, with one note: after a 6 Feb lock a withdrawal can only remove something, not re-cut it.
- `ROADMAP.md` lines 159, 230, 293 and `ROADMAP-ADDENDUM.md` lines 173, 215, 242: they record the decision and the conflict.
- `playbooks/cinematic-quality.md` lines 484 to 489, 601, 772: offers "move picture lock to 13 Feb" only as an option if the maker prefers one strangers' session; the roadmap chose two sessions and 6 Feb.
- `research/production-scale.md` line 902: "final by Fri 19 Feb 2027 at the latest" is a vendor delivery date in a request for quote; check it against G-MASTER (Sat 20 Feb) when the quote is sent, not a picture-lock claim.
- `reviews/*`: they quote the error as the finding.

### Changes to the earlier text in this file

| Earlier statement | Now |
|---|---|
| FU-1: "No DCP was built and no DCP-o-matic binary ran successfully" | Superseded: the real 2.18.51 command-line tools ran in a container; DCPs built, verified OK and decoded (FU2-1) |
| FU-1: preset gamma from source only | Source, project files and decoded grey bars all agree: Rec. 709 preset 2.2, Rec. 1886 preset 2.4, output 2.6 |
| FU-1: ProRes import "supported by the code ... not run by me" | Run: a ProRes 422 HQ `.mov` imports, encodes and verifies OK on Linux; Windows still to test |
| FU-1: planning figure 2 to 4 GB RAM, speed "UNVERIFIED" | Measured: about 190 MB + 125 MB per thread; CPU cost 0.4 to 1.3 s per frame for detailed content, about 0.02 for flat bars (FU2-1) |
| FU-1: J2K bandwidth "125 Mbit/s" used for file size | Default cap is 150 Mbit/s (`film.cc` line 215); 15 minutes is about 17.7 GB at the cap |
| FU-3: `_20`, from source | Also run on the real program; CPL says `51/L,R,-,-,-,-`; mono gives `_10`; 5.1 gives `_51` |
| FU-2: "Advanced display > Choose a refresh rate is from general knowledge" | Sourced to Microsoft's HDR page [42] |
| FU-4: PRS/ASCAP/BMI/IPRS statements not retrievable | UK tariffs read (PRS Tariff C is cinema-only and excludes free entertainments; PPL one-off tariffs cover background music); US Copyright Office 2015 statement on source licences; India Act ss.18, 52 (FU2-4) |
| FU-6: Article 50(4) "no change found" (not line by line) | Confirmed line by line: Omnibus changes only Art 50(7) and adds Art 111(4); the Commission's guidelines of 20 July 2026 put a non-professional individual outside the deployer duties (FU2-6) |
| FU-5: E&O premium "vendor range only" | Same: two broker pages give no premium; E&O described as a distribution requirement (FU2-5) |
| Summary and Finding 7/Deliverable 3: "Fri 19 Feb picture lock" | Wrong label; see FU2-9 |

### Still open after round 2

- **Inputs only the maker can give:** TD-7 country; the laptop model and port; whether the premiere stays free and public-and-unpaid (the AI Act "personal non-professional" reading and the music-licence questions both depend on that).
- **Next cheap tests:** (1) the same grey-bar test on the maker's Windows PC, with Task Manager open, to replace the Linux proxy numbers (commands in `research/theatrical-delivery-fixtures/followup2-make-test-dcp.sh`; Windows program names and paths UNVERIFIED); (2) photograph the refresh-rate list; (3) one written question to the venue and PPL PRS (UK) / IPRS (India) about the film soundtrack; (4) one broker quote for short-event public liability.
- **UNVERIFIED:** ASCAP, BMI and IPRS statements; the current PRS cinema tariff; Windows memory and speed; whether India's s.17(b) text is current today; DPDP Act commencement and "personal or domestic" for a public showing; defamation of the dead (UK); a venue's required public-liability limit and a one-day premium; a 2026 short-film E&O premium from a broker; whether the AI Act exclusion covers a public-gathering screening in so many words; a first-person clearance routine for relatives' photographs and voices.

### New sources (continuing the numbering)

[117] Own tests with the official DCP-o-matic 2.18.51 command-line package for Ubuntu 24.04 (`dcpomatic2_create`, `dcpomatic2_cli`, `dcpomatic2_verify_cli`; "dcpomatic version 2.18.51 920fb9b044"), unpacked in a scratchpad, 2026-10-18; fixtures: `research/theatrical-delivery-fixtures/followup2-*` (colour table, ISDCF names, CPL sound configuration, timing, memory). Proxy for the Windows PC: Linux container, 4 vCPU Xeon 2.1 GHz, shared and loaded.
[118] DCP-o-matic tag v2.18.51 (commit 920fb9b, 2026-10-16) and libdcp (commit 891facc, 2026-10-01), re-cloned 2026-10-18 and read with line numbers — libdcp `src/colour_conversion.cc` (lines 58, 74, 90, 157, 176); `src/lib/ffmpeg_content.cc` lines 493 to 525; `src/lib/film.cc` lines 215 and 1127 to 1132; `src/lib/config.cc` line 86; `src/lib/cross_linux.cc` (resources found relative to the executable; libdcp resources via `APPDIR`). Same commits as [92][93].
[119] ISDCF, Digital Cinema Naming Convention registry — https://www.isdcf.com/registry/audioconfigs/ and https://www.isdcf.com/registry/dcncintro/ — 2026-10-18 (footer "(c) 2026"; no revision date) — audio codes 20, 51, 71, 10, 21; MainSoundConfiguration SOUNDFIELD values; "Only discrete audio should be used in a DCP".
[120] DCP-o-matic forum front page — https://dcpomatic.com/forum/ — 2026-10-18 — categories General, DCP-o-matic, Grok; latest posts only; no performance topic reachable (negative result).
[121] PRS for Music, Tariff 'C' Cinemas — https://pplprs.co.uk/wp-content/uploads/C-2024-Tariff.pdf — PDF created 2023-11-24; text "Effective 1st January 2024 ... will expire on 30th June 2024" (the edition the site links; current edition not seen) — scope, free-entertainment exclusion.
[122] PPL PRS tariffs page — https://pplprs.co.uk/business/other/ — 2026-10-18; PPL Single and Casual Events Tariff PPLPP002 — https://pplprs.co.uk/wp-content/uploads/PPLPP002-Single-Casual-Events-Oct-26.pdf — effective 1 Oct 2026 to 30 Sep 2027; PPL cinema background-music tariff PPLPP036 — https://pplprs.co.uk/wp-content/uploads/PPLPP036-BGM-Cinemas-September-26.pdf — effective 1 Sep 2026 to 31 Aug 2027.
[123] PPL PRS, TheMusicLicence for live events and festivals — https://pplprs.co.uk/themusiclicence/sectors/live-events-festivals/ — 2026-10-18 (page; no date shown) — "film screening", "additional recorded music used at the event"; no hired-hall or hirer statement.
[124] US Copyright Office, "Copyright and the Music Marketplace" (Register of Copyrights, February 2015; second printing May 2016) — https://www.copyright.gov/policy/musiclicensingstudy/copyright-and-the-music-marketplace.pdf — 2026-10-18 — page 33 and footnote 117 on source licences and movie theatres.
[125] Digital Personal Data Protection Act, 2023 (India), Gazette of India Extraordinary, No. 22 of 2023, 11 August 2023 — https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf — 2026-10-18 — ss.1(2), 2(j), 3(c)(i), 14. Commencement not checked.
[126] Regulation (EU) 2024/1689 (AI Act), original Official Journal text from EUR-Lex — https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689 — 2026-10-18 — recital 13, Articles 2(10), 3(4), 3(60), 50(4), 50(5), 50(7).
[127] European Commission, Guidelines on the implementation of the transparency obligations for certain AI systems under Article 50 of the AI Act, C(2026) 5054 final, 20.7.2026 (51 pages) — https://ec.europa.eu/newsroom/dae/redirection/document/131215, linked from https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems (library page: published 20 July 2026, "These transparency obligations apply from 2 August 2026") — 2026-10-18 — paragraphs 19 and 20 (personal non-professional), 114 (deep-fake test), 122 to 124 (artistic works), 143 (first exposure).
[128] European Commission, Code of Practice on Marking and Labelling of AI-generated Content — https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content — 2026-10-18 (page) — drafts 17 Dec 2025 and 3 Mar 2026; final after the 10 June 2026 plenary; applicable from 2 August 2026; providers (section 1) and deployers (section 2). The AI Act framework page [66], last update 3 August 2026, gives the Omnibus entry into force as 27 July 2026.
[129] Law Reform (Miscellaneous Provisions) Act 1934, s.1 — https://www.legislation.gov.uk/ukpga/Geo5/24-25/41/section/1 — 2026-10-18 (page; "Latest available (Revised)") — defamation proviso to survival of causes of action.
[130] Film Emporium (US broker), home page — https://www.filmemporium.com/ — errors and omissions page — https://www.filmemporium.com/errors-omissions — and special events page — https://www.filmemporium.com/special-events — 2026-10-18 (pages) — E&O described as a distribution and some-festival requirement; "one-day or short-term event insurance"; no prices or limits.
[131] Front Row Insurance Brokers (Canada), producer's E&O page — https://www.frontrowinsurance.com/producers-e-o-insurance/ — and article "Lights, Camera… Protection: Why producer's E&O insurance is essential for every production" — https://www.frontrowinsurance.com/news/why-producers-eo-insurance-matters/ (30 June 2026) — 2026-10-18 (pages) — term "one to three years"; no prices.
[132] Oral History Society (UK), "Oral History: Being legal and ethical" — https://www.ohs.org.uk/advice/ethical-and-legal/ and https://www.ohs.org.uk/advice/ethical-and-legal/after-the-interview/ — (c) 2019 — 2026-10-18 (pages) — Interview Recording Agreement; pre- and post-interview agreements.
[133] Wikipedia, Dick Johnson Is Dead — https://en.wikipedia.org/wiki/Dick_Johnson_Is_Dead — 2026-10-18 — secondary: family photographs and home movies; no clearance statement; cites a Vulture interview (29 Jan 2020) that I could not fetch.
[134] Own scan of the repository for picture-lock and 19 February wording, `python3 -I`, 2026-10-18 (all `.md`, `.txt`, `.csv`, `.json`, `.py`, `.sh` under `.`); the results are the tables in FU2-9.
