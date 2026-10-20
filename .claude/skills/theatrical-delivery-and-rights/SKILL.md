---
name: theatrical-delivery-and-rights
description: Builds and checks the Life Journey film's theatre-grade deliverables (1920x1080 ProRes master, venue MP4 with burned-in captions, the PH1 and PH2 phone files, loudness and mono-fold checks, DCP-o-matic 2K DCP with Verify and hashes) and the rights and releases for a public screening. Use when making, testing or troubleshooting masters, venue or TV playback, captions, loudness, DCP output, rights-log rows, releases, or any decision about showing the film publicly, in a cinema, at a festival or online.
---

# Theatrical Delivery and Rights

## Purpose

Turn the finished film into deliverables that play on screens and sound systems we do not control. Make sure every asset and person shown is cleared, substituted, or a documented risk before any public showing.

Facts come from `research/theatrical-delivery.md` (research date 2026-10-18). The human guide is `playbooks/theatrical-delivery.md`. The decisions register `DECISIONS.md` is the source of truth: where this skill and the register disagree, the register wins. Every legal statement is "jurisdiction not yet known; confirm; not legal advice" until TD-7 (country and state) is answered.

## When to use

- Setting or changing master, venue, DCP, archive or online settings.
- Making or checking the venue test clip, captions, loudness, mono-fold, colour trims or hashes.
- Building, verifying or troubleshooting a DCP.
- Writing run-sheet lines or a playback plan for a venue.
- Adding rows to the rights log, drafting releases, or preparing the consult questions.
- Deciding whether an item may appear at the 27 February gathering, a cinema, a festival or online.

## When not to use

- Story, edit, animation or AI-generation decisions. Use the other project skills.
- Gathering stories, photos or consent from people. This skill says what a release must contain, not how to ask for it.
- Giving legal advice or settling a legal question. Flag it for the consult.
- Anything that would reveal the surprise to her or to people outside the ring (under only-me mode, that is everyone else).

## Procedure

1. Read `DECISIONS.md`, then the playbook's Decisions and T1 (settings card). Confirm the status of TD-1 to TD-9 (register rows W-14 to W-19, W-54, W-55, W-74; TD-7, the country, is pending from the maker as O-02; TD-9 is the phone deliverable and sharing rule). If TD-7 is unknown, mark every legal output "jurisdiction not yet known".
2. Master: ProRes 422 HQ, 1920x1080, 24p, Rec.709, limited range, 10-bit 4:2:2, PCM 24-bit 48 kHz [3]. Prepare scans and stills at 3840 px on the long edge or larger [3]. Do not create a UHD or 2K DCI working copy (TD-1).
3. Probe every file with ffprobe. Record `pix_fmt`, `color_range`, `color_space`, `color_transfer`, frame count and duration [3]. Use this command, run in the container on 2026-10-18 (ffmpeg 6.1.1); confirm once on the Windows PC: `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,color_range,color_space,color_transfer,color_primaries,r_frame_rate,nb_frames:format=duration -of default=nw=1 FILE`.
4. Colour: one grade to Rec.709 / BT.1886. Trim V (lit venue), Trim C (dark cinema) and Trim P (the phone files; a mild shadow lift set at G-SLICE, W-64) are `.cube` lookup files applied only at export, via ffmpeg `lut3d` (run in the container on 2026-10-18 without error; confirm once on the PC). Trim C stays identity until a real cinema test. Trim V is set on site at the TD-L2b visit (by Sunday 17 January 2027). Hash and log each trim [2][34].
5. Audio: one mix, with stems kept. Three outputs. Cinema: no normalisation, headroom kept [30]. Venue: three masters at -23, -18 and -16 LUFS integrated, all at -1 dBTP, chosen at the Mon 2027-02-22 run against sixty seconds of the hall's own room tone recorded from the back row; if no reading can be taken, load -18 first (`DECISIONS.md` W-19). Settled: -1 dBTP everywhere, per R128 and the research; the toolchain's -1.5 was a loudnorm example, not a target [36][2]. Phone files (the online row): PH1 and PH2 at -16 LUFS integrated and -1 dBTP measured on the final MP4 after the AAC encode (W-19, W-63) [38].
6. Loudness and mono check: `ffmpeg -nostats -i FILE -af ebur128=peak=true -f null -`, then the same with `-af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true"`. A drop of more than about 3 LU against stereo flags phase trouble (rule of thumb, inference).
7. Captions: open and burned in, inside the 90% by 90% box [37]. At most two lines, 42 characters or fewer per Latin line (a guide: the rule is that a line fits the box in its face), under 20 characters per second [4]. Venue line height 7 to 8% of picture height [4], confirmed on the real screen. Cinema start at 5.5 to 6% (inference). **Gujarati is sized by the height of KA, not by `FontSize`** (Noto Sans Gujarati: KA 3.33% at 23; 26.2 for the phone's 3.8%), and the phone files carry their own caption setting (`FontSize=28`, `MarginV` 40, at most 32 characters, which fits the 90% by 90% box in both scripts, block at 68 to 86% of height; W-18). On any ffmpeg older than n9.0 burn Indic text with the `ass` filter on an ASS file made from the SRT (`YCbCr Matrix: TV.709`), never `subtitles` or `drawtext`; the ten-minute `ab.srt` A/B on the PC decides (W-75). Fonts are OFL only, each with a `font` row, its `OFL.txt` hash and the libass `fontselect:` line; her script on titles and verse cards travels as shaped outlines, never live text (W-21). Windows fonts only as rasterised picture text [76]. Any DCP subtitle track uses an OFL font [75].
8. Venue file set: MP4, H.264 High 4.1, yuv420p, BT.709 tags, AAC-LC 48 kHz stereo 256 kbps, `-crf 18 -maxrate 20M -bufsize 40M` [2]. Backup: H.264 Main 4.0, about 8 Mbps. Also the test clip (60 to 90 seconds, no personal content, with a tone ladder from 100 Hz to 3.2 kHz whose lowest back-row tone is written down at TD-L2b, W-17, W-65) and an audio-only fallback [5]. Phone files from the ProRes master, never the venue file: PH1 1920x1080p24 H.264 High 4.1, CRF 20, 8 Mb/s cap, AAC-LC 192 kbps, captions burned, SDR only, no HEVC; PH2 1280x720, CRF 22, 3.5 Mb/s cap, level 3.1 (W-63). The venue file opens with a thirty-second countdown in her grammar, decided at G-MASTER (Sat 2027-02-20); the rehearsal copy and the test clip keep the neutral slate (`DECISIONS.md` W-53). Online H.264 at about 12 Mbps only after the T3 gate.
9. Neutral names everywhere. No personal name and no title metadata. Strip metadata with `ffmpeg -i in.mp4 -map_metadata -1 -c copy out.mp4` (run in the container on 2026-10-18; it removed the title tag; ffmpeg re-adds a harmless `encoder` tag; confirm on the PC). The DCP title shows on cinema servers, so use the code name [5].
10. Test on the real screen before anything else. Play the venue test clip (bars, PLUGE, ramp, tone, tone ladder, left and right, slow pan, captions at 20, 23 and 26 with the Gujarati KA line) with overscan and HDR off [40][42][45]. Record the TV settings. Play the film's first and last five minutes only in an empty room.
11. DCP, only after the test DCP passes, and encoded on the Windows PC, never in the cloud container [47]. The venue's written answer (asked by Fri 2026-11-06, due Sun 2026-11-15) decides whether the 2K Flat DCP is the primary deliverable or a contingency made after the premiere (`DECISIONS.md` W-17). DCP-o-matic 2.18.51 [8]. Container Flat 1.85, 2K, 24 fps, SMPTE, encryption off, JPEG2000 100 to 125 Mbit/s, single reel, ISDCF name on, content type feature or short, to match the final runtime; the type places the film in the projectionist's interface [15]. Range Video [12]. Audio L and R at unity gain [13]. Timed text empty when captions are burned in [14].
12. Verify DCP in the Player (Tools, then Verify DCP). Fix every error and read every warning [18]. Play the DCP in the Player start to finish. This proves the package is well-formed, not that a cinema will accept it [17].
13. Write the drive with DCP-o-matic's Disk Writer: ext2 (the only format DCP-o-matic guarantees in all cinemas; ISDCF also allows ext3), with a 128-byte inode, on an MBR table with one primary partition of type 0x83. Re-partition any retail USB stick first (ISDCF: retail partition tables are "almost certainly incorrect"). MBR drives must be 2 TB or smaller [19][26]. Label it "Do not read with a consumer computer". Never plug it into the Windows PC after writing [26].
14. Make a SHA-256 manifest of each delivery folder, copy the folder, and re-check the hashes from the drive [4].
15. Venue run: confirm the survey answers (T5). Run the test clip with the AV person present, then the full run, with a cold start under two minutes, and choose one of the three loudness masters (W-19). The maker holds the master fader (W-54). Walk failure rungs 1 to 4 once each [5]. Gate G6 before final export; gate G6b at the venue full run.
16. Rights: one log row per asset, cue or person, using the T8 header. Assign tiers A to D (playbook Step 11). A RISK row needs why, how to undo it, who is exposed, and the date. Tier C items and every RISK row need the Fable advisor's written flag and at least 48 hours between drafting and deciding (inference). Advisor-flag mechanism: write the item as `rights/flags/<asset_id>.md` (why, undo, exposed, draft date) and request a Fable review of that file. Do not set status RISK or admit a Tier C item until the file carries a dated advisor line and 48 hours have passed since the draft date.

    **Only-me mode (decided, `DECISIONS.md` D-03).** The maker is the only person in on the project. Nobody is read card 4a (T9) before the premiere; reading it to anyone is a bringing-in decision, parked until TD-L2c. Before the premiere, Tier A means the maker's own material, her appearances by proxy, and original, CC0 or licensed assets; Tier B stills of adults carry a documented risk, ratified after, and nobody is asked (W-46). Relatives' voices wait for the April version (Sat 2027-04-24), recorded after they sign release 4d (D-05, D-06). The public cut can therefore contain the maker's own material and cards (the maker's voice only as W-35 allows), her appearances by proxy, Tier B stills of adults (no voice), attributed text with no voice, and original, CC0 or licensed music. It cannot contain a recorded voice of a living person before the premiere. Any step that asks a contributor to confirm, sign or approve (for example TD-L6) waits for the same decision. Decision point: Sunday 3 January 2027 (playbook T4, TD-L2c).
17. Music: a commercial recording needs a sync licence and a master licence, and a performance licence is a third right [82]. The premiere's sound is the maker's own captures and hum (W-44); CC0 or CC BY only as a labelled stand-in and only if the sound is hers (O-72); no sung recording before April (D-05). "Devotional" does not mean free: words, tune, arrangement, recording and performance are five separate questions, and `composition_status` and `recording_status` are separate mandatory columns (W-79).
18. Photos taken by others: find the photographer and record every search step. Orphan works have no US safe harbour [54]. UK IPO application fee £20 for one work, £24 for two, £30 for five, £40 for ten, £60 for twenty, £80 for thirty; non-refundable; a separate licence fee is payable only if the licence is granted; licence up to 7 years; UK use only; film and photographs are covered; page updated 1 Dec 2025, read 2026-10-18 [62]. In India, s.17(b) may make the commissioner the first owner (copy read; date unknown; confirm) [70].
19. AI items: record the L-level, tool name and version, tool terms and a human-contribution note. Add a pre-roll line before the title. Mark photoreal motion of a real person as a possible deepfake [53][65]. No deity is drawn, generated or photographed and AI never touches one (W-61); artwork, `deity_image`, `commissioned_art` and `font` rows carry a `tradition_origin` note, and every row a `phone_share` value (W-46).
20. Gates. T2 (27 February): every row green or a written RISK entry; no unlicensed commercial music; no deity drawn, generated or photographed; every font OFL with a `font` row. T3 (online): releases signed and the maker's explicit yes. T4 (cinema or festival): all T3 rows green, releases signed, E&O decision made, music cue sheet, AI disclosure [77][88].
21. Before any showing beyond 27 February, confirm the consent ledger has closed (Monday 29 March 2027) and the T3 or T4 gate is green [5]. Phone copies (TD-9, W-74): nothing on her phone or a relative's before the reveal; on reveal weekend, with her yes and K1 answered, PH1 by cable (PH2 if under 1 GB is free); relatives get PH2 or PH1 as a WhatsApp document only after the ledger closes and the maker says yes; the her-turn conversation is Sun 7 Mar after about 14:00, else Mon 8 Mar (W-48). Consult questions are T10 1 to 43, renumbered once (W-55).
22. Report back: what was checked, what is still TODO(research), and any conflict with the playbook (for example a date that disagrees with another playbook, such as picture lock, which is Sat 6 Feb 2027 per production-scale G-LOCK).

## Checklists

**Master and venue file (G6)**
- [ ] ffprobe fields recorded: 1920x1080, 24p, BT.709 tags, limited range.
- [ ] Colour-patch test passed after the last re-encode [3].
- [ ] All three venue masters (-23, -18, -16 LUFS) measured at -1 dBTP; the chosen one recorded at the 22 Feb run (W-19). Mono-fold drop within about 3 LU.
- [ ] Captions inside the safe box, two lines at most, not in side bars.
- [ ] Metadata stripped; neutral file name; no title tag.
- [ ] Trims applied at export; each trim file hashed and logged.
- [ ] Manifest written; hashes re-checked from the drive.

**Venue playback day (G6b, TD-L9)**
- [ ] Test clip first, with the AV person present.
- [ ] Overscan off; HDR off; cinema or film mode; motion smoothing off.
- [ ] Captions readable from the back row; dialogue intelligible.
- [ ] Cold start under two minutes; failure rungs 1 to 4 walked.
- [ ] Two sticks with PH1 beside the venue file, two laptops, the phone cable and adapter tested, settings photographed.

**DCP (before any cinema)**
- [ ] DCP-o-matic settings match Procedure step 11.
- [ ] Verify DCP: zero errors; every warning explained.
- [ ] Played in the Player start to finish.
- [ ] Drive: ext2 or ext3, 128-byte inode, MBR with one primary partition of type 0x83; retail stick re-partitioned; label set.
- [ ] Hash manifest matches the drive copy.

**Rights gate**
- [ ] Every row has a status: NS, ASKED, GRANTED, REFUSED, SUBST, RISK, OUT or VERIFY.
- [ ] Tier assigned; jurisdiction note present.
- [ ] Every RISK row has why, undo, exposed people and date.
- [ ] No game name, asset or footage (D-29); no deity drawn, generated or photographed (W-61); every font has its `OFL.txt` hash.
- [ ] No synthetic voice; every reconstruction labelled.
- [ ] Only-me mode: no recorded voice of a living person in the premiere cut except her own HER-PUBLIC clip after one-key-three-guards (D-04, D-05); relatives' voices are April-version items (D-06).
- [ ] Every Tier C item and RISK row has `rights/flags/<asset_id>.md` with a dated advisor line.

## Quality bar

Theatrical work holds up on a big screen. Mediocre work does not.

- **Picture:** one grade across the film; no crushed blacks or clipped whites; no banding in skies, vignettes or fades; no overscan crop; slow pans show no judder on the venue screen [39][40].
- **Captions:** readable from the back row, inside the safe box, timed to the speech, never hidden in black bars.
- **Sound:** dialogue intelligible at the back of the room; mono-fold check passes; the cinema mix is not normalised; no clipping.
- **Delivery:** every file passes probe and hash checks; a DCP has zero Verify errors; the cold start is under two minutes; backups are verified.
- **Honesty:** reconstructions are labelled; no invented events are shown as fact; no synthetic voices; AI use is disclosed.
- **Rights:** every asset has a status; nothing sits on the not-allowed list; the surprise survives in file names, titles and metadata.
- **Mediocre tells:** a grade approved only on a monitor; a test never played on the venue screen; loudness set by a broadcast number; a DCP never played; a rights row that says "fine" with no evidence.

## Ethics, rights and privacy guardrails

- Never invent facts, tools, prices or URLs. Mark every gap TODO(research).
- No cloned or synthetic voices. Reconstructed scenes are visibly reconstructions [1][6].
- Gather truthfully. The surprise may be omitted, but nothing untrue may be said. Read the consent card (T9, 4a) only when its bracketed lines are true [5], and under only-me mode not to anyone at all (Procedure step 16).
- "Mostly public" triggers the public-rights answer. Family-circle assumptions do not hold for 27 February [56].
- Minors: a guardian's written yes, or the child is left out, or an adult-now yes (4f) [86][5].
- The dead: the closest family decides. Stills only unless they say more. Otherwise out [5]. Germany requires close relatives' consent for 10 years after death [68].
- The estranged: out by default, never contacted cold [5].
- Private data (names, consents, addresses) stays in the private repo. Nothing goes to a third-party service without the maker's explicit yes [1].
- Games and brands: none used (D-29; Minecraft is dropped). Her Hindu world (D-28): no deity image on a phone surface until the maker decides in writing per surface (O-64); no decorative frame (jaali, paisley, mehndi border, arch, tile); no Om tone as a UI sound (W-73).
- Misleading edits: a sequence must not present something as fact that it is not [85].
- Accepted risks are written down, reversible first, and decided by the maker with the advisor's flag, filed at `rights/flags/<asset_id>.md` (Procedure step 16).

## References

- `playbooks/theatrical-delivery.md`: the human guide (Decisions, templates T1 to T11, exercises, changelog).
- `research/theatrical-delivery.md`: the research notes, with the full citation list and the open gaps.
- `CHARTER.md`: principles 4 to 7 (real memories, dignity, theatrical bar, cleared for public screening).
- `DECISIONS.md`: the decisions register (source of truth).
- Key URLs: DCP settings https://dcpomatic.com/manual/html/ch07.html [15]; ISDCF Doc 3 https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf [26]; Sundance FAQ https://www.sundance.org/submissions-faq [88].

### Sources

- [1] Project Charter — CHARTER.md — 2026-10-18 — facts, principles, open decisions.
- [2] toolchain playbook — playbooks/toolchain.md — 2026-10-18 — Steps 10 to 15, Decisions 6 to 9.
- [3] agent-pipeline playbook — playbooks/agent-pipeline.md — 2026-10-18 — settings card, gate G6, pitfall 6.
- [4] format playbook — playbooks/format.md — 2026-10-18 — caption rules, hosting table, Decisions 3, 8, 9, 12, 13.
- [5] surprise-ops playbook — playbooks/surprise-ops.md — 2026-10-18 — key dates, consent card, pretext cards, run sheet, Decisions 6 and 12.
- [6] ai-imagery playbook — playbooks/ai-imagery.md — 2026-10-18 — L0 to L5 ladder, cue sheet, decisions.
- [8] DCP-o-matic download — https://dcpomatic.com/download — 2026-10-18 — stable 2.18.51, 16 October 2026; Windows, macOS, Linux.
- [12] Manual, video content — https://dcpomatic.com/manual/html/ch06s04.html — 2026-10-18 — colour presets, range, scale and container.
- [13] Manual, audio content — https://dcpomatic.com/manual/html/ch06s05.html — 2026-10-18 — audio map, gain, delay.
- [14] Manual, timed text — https://dcpomatic.com/manual/html/ch06s06.html — 2026-10-18 — SRT/SSA/DCP XML, burn-in, open versus closed.
- [15] Manual, DCP settings — https://dcpomatic.com/manual/html/ch07.html — 2026-10-18 — container, 2K advice, bandwidth 50 to 250 Mbit/s, standard, reels, FAT32 note.
- [17] Manual, playing DCPs — https://dcpomatic.com/manual/html/ch18.html — 2026-10-18 — Player limits and warnings.
- [18] Manual, verifying DCPs — https://dcpomatic.com/manual/html/ch19.html, https://dcpomatic.com/manual/html/ch19s03.html, https://dcpomatic.com/manual/html/ch19s04.html — 2026-10-18 — errors, warnings, passes.
- [19] Manual, writing DCPs to disks and encryption — https://dcpomatic.com/manual/html/ch20.html and https://dcpomatic.com/manual/html/ch10s04.html — 2026-10-18 — ext2, Disk Writer; "Should I encrypt?".
- [26] ISDCF Doc 3, DCP Delivery Recommendations — https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf — 2017-06-29 — MBR, 0x83, ext2/ext3, 128-byte inode, USB 2.0, consumer-OS warning.
- [30] ISDCF Doc 11, "How Loud is a Movie?" (Ioan Allen, SMPTE) — https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf — 2016-03-15 — calibrated rooms, fader 7, TASA 85 dB Leq(m), no feature limits.
- [34] Wikipedia, Rec. 709 — https://en.wikipedia.org/wiki/Rec._709 — 2026-10-18 — secondary: OETF, limited range codes, no display EOTF.
- [36] EBU R 128 (v5, November 2023) — https://tech.ebu.ch/docs/r/r128.pdf — 2023-11 — -23.0 LUFS, tolerances, -1 dBTP.
- [37] EBU R 95 v1.1 (June 2017) — https://tech.ebu.ch/docs/r/r095.pdf — 2017-06 — action safe 3.5%, graphics safe 5%.
- [38] Wikipedia, Loudness war — https://en.wikipedia.org/wiki/Loudness_war — 2026-10-18 — secondary: streaming targets (YouTube -14 LUFS, Apple Music -16).
- [39] Wikipedia, Frame rate — https://en.wikipedia.org/wiki/Frame_rate — 2026-10-18 — secondary: 24 fps cinema, judder.
- [40] Wikipedia, Motion interpolation — https://en.wikipedia.org/wiki/Motion_interpolation — 2026-10-18 — secondary: soap opera effect, 120 Hz.
- [42] Microsoft Support, HDR settings in Windows — https://support.microsoft.com/en-us/windows/hdr-settings-in-windows-2d767185-38ec-7fdc-6f97-bbc6c5ef24e6 — 2026-10-18 — SDR looks off with HDR on; HDR off on battery.
- [45] Wikipedia, Overscan — https://en.wikipedia.org/wiki/Overscan — 2026-10-18 — secondary: LCD TVs often ship with overscan on.
- [47] Own measurements in the cloud container — 2026-10-18 — ffmpeg 6.1.1, `libopenjpeg`, 4-vCPU Intel Xeon at 2.1 GHz, 16 GB RAM; disk 100% full; `ebur128` and `pan` syntax run; JPEG2000 timings in Finding 4.
- [53] US Copyright Office, AI Part 2: Copyrightability — https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — January 2025 — conclusions, prompts, disclosure on registration.
- [54] US Copyright Office, Orphan Works and Mass Digitization — https://www.copyright.gov/orphan/reports/orphan-works2015.pdf — June 2015 — "legal cloud"; limitation-on-remedies proposal.
- [56] 17 U.S.C. 101 — https://www.law.cornell.edu/uscode/text/17/101 — 2026-10-18 — definition of "publicly" (family and social acquaintances).
- [62] UK IPO, Orphan works licensing — https://www.gov.uk/guidance/copyright-orphan-works — 2026-10-18 — fees, 7-year licence, UK only.
- [65] EU AI Act, Article 50 — https://artificialintelligenceact.eu/article/50/ — 2026-10-18 — marking, deepfake disclosure, artistic works.
- [68] Kunsturhebergesetz (KUG) section 22 — https://www.gesetze-im-internet.de/kunsturhg/__22.html — 2026-10-18 — consent, 10 years post mortem (German text).
- [70] Copyright Act, 1957 (India), consolidated copy — https://copyright.gov.in/Documents/Copyright_Act_1957.pdf — 2026-10-18; date of consolidation not shown — ss.2(d), 17, 31A, 52.
- [75] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — 2026-10-18 — output not restricted; video titling; embedding.
- [76] Microsoft, Font redistribution FAQ — https://learn.microsoft.com/en-us/typography/fonts/font-faq — page dated 2024-11-19 — video captions as bitmaps allowed; no embedding or conversion.
- [77] IDA, "Errors & Omissions: ... Guide to Protecting Your Film" (Winnie Wong) — https://www.documentary.org/feature/errors-omissions-rights-oh-my-guide-protecting-your-film — 2012-04-06 — E&O requirements, $1M/$3M, $10,000 deductible.
- [82] IDA, "All Clear? A Basic Primer on Music Clearance" (David G. Powell) — https://www.documentary.org/feature/all-clear-basic-primer-music-clearance — 2003 — sync, master, festival versus all-media licences.
- [85] IDA, "Beyond Vetting: Common Legal Issues for Documentary Filmmakers" (Katie Townsend) — https://www.documentary.org/column/beyond-vetting-common-legal-issues-documentary-filmmakers — 2020-06-11 — misleading edits; consent laws.
- [86] Wikipedia, Model release — https://en.wikipedia.org/wiki/Model_release — 2026-10-18 — secondary: minors need parent or guardian signature.
- [88] Sundance Film Festival 2027 submissions FAQ — https://www.sundance.org/submissions-faq — document created 2026-09-08 — premiere definition (FAQ 8), AI (12), temp music (13), clearance (14), screener format (18), DCP delivery (31).

## Changelog

- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18). Venue loudness start replaced by the three-master choice, all at -1 dBTP (W-19; S-28); venue answer decides file or DCP (W-17); only-me and the April version replace private-cut wording, Tier B is documented risk ratified after (D-03 to D-06, W-46); the maker holds the master fader (W-54).
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19). Game-terms material retired under D-29 (T2 gate, checklist, guardrail, source [48]; S-48, S-50); the phone files PH1 and PH2, Trim P and TD-9 added (W-63, W-64, W-74); Gujarati caption sizing, the OFL font rows and the `ass` burn-in path before ffmpeg n9.0 (W-18, W-21, W-75); the test clip's tone ladder (W-17, W-65); rights rows for artwork, deity images, commissioned art and fonts with `tradition_origin` and `phone_share` (W-46); "devotional means free" note (W-79); T10 renumbered 1 to 43 (W-55); the her-turn conversation is Sun 7 Mar after about 14:00, else Mon 8 Mar (W-48). Patched copy staged in `skills-staging/`; the orchestrator installs it.
- 2026-10-20: Stale-wording sweep (2026-10-20): steps 7 and 8 carry the register's phone figures, at most 32 characters a phone caption line (W-18) and a 3.5 Mb/s cap on PH2 (W-63). No gate, check or decision changed.
