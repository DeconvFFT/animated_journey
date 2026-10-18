---
name: theatrical-delivery-and-rights
description: Builds and checks the Life Journey film's theatre-grade deliverables (1920x1080 ProRes master, venue MP4 with burned-in captions, loudness and mono-fold checks, DCP-o-matic 2K DCP with Verify and hashes) and the rights and releases for a public screening. Use when making, testing or troubleshooting masters, venue or TV playback, captions, loudness, DCP output, rights-log rows, releases, or any decision about showing the film publicly, in a cinema, at a festival or online.
---

# Theatrical Delivery and Rights

## Purpose

Turn the finished film into deliverables that play on screens and sound systems we do not control. Make sure every asset and person shown is cleared, substituted, or a documented risk before any public showing.

Facts come from `research/theatrical-delivery.md` (research date 2026-10-18). The human guide is `playbooks/theatrical-delivery.md`. Every legal statement is "jurisdiction not yet known; confirm; not legal advice" until TD-7 (country and state) is answered.

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
- Anything that would reveal the surprise to her or to people outside the ring.

## Procedure

1. Read the playbook's Decisions and T1 (settings card). Confirm the status of TD-1 to TD-8. If TD-7 is unknown, mark every legal output "jurisdiction not yet known".
2. Master: ProRes 422 HQ, 1920x1080, 24p, Rec.709, limited range, 10-bit 4:2:2, PCM 24-bit 48 kHz [3]. Prepare scans and stills at 3840 px on the long edge or larger [3]. Do not create a UHD or 2K DCI working copy (TD-1).
3. Probe every file with ffprobe. Record `pix_fmt`, `color_range`, `color_space`, `color_transfer`, frame count and duration [3]. The exact command is TODO(research); do not invent one.
4. Colour: one grade to Rec.709 / BT.1886. Trim V (lit venue) and Trim C (dark cinema) are `.cube` lookup files applied only at export, via ffmpeg `lut3d` (untested). Trim C stays identity until a real cinema test. Hash and log each trim [2][34].
5. Audio: one mix, with stems kept. Three outputs. Cinema: no normalisation, headroom kept [30]. Venue: start at about -16 LUFS integrated and -1 dBTP, then confirm on site. The toolchain example uses -1.5 dBTP, so record which value was used [2][36]. Online: -16 LUFS, -1 dBTP [38].
6. Loudness and mono check: `ffmpeg -nostats -i FILE -af ebur128=peak=true -f null -`, then the same with `-af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=peak=true"`. A drop of more than about 3 LU against stereo flags phase trouble (rule of thumb, inference).
7. Captions: open and burned in, inside the 90% by 90% box [37]. At most two lines, 42 characters or fewer per line, under 20 characters per second [4]. Venue line height 7 to 8% of picture height [4], confirmed on the real screen. Cinema start at 5.5 to 6% (inference). Windows fonts only as rasterised picture text [76]. Any DCP subtitle track uses an OFL font [75].
8. Venue file set: MP4, H.264 High 4.1, yuv420p, BT.709 tags, AAC-LC 48 kHz stereo 256 kbps, `-crf 18 -maxrate 20M -bufsize 40M` [2]. Backup: H.264 Main 4.0, about 8 Mbps. Also the test clip and an audio-only fallback [5]. Online H.264 at about 12 Mbps only after the T3 gate.
9. Neutral names everywhere. No personal name and no title metadata. Strip metadata with `-map_metadata -1` (inference; test it). The DCP title shows on cinema servers, so use the code name [5].
10. Test on the real screen before anything else. Play the venue test clip (bars, PLUGE, ramp, tone, left and right, slow pan, captions at 20, 23 and 26) with overscan and HDR off [40][42][45]. Record the TV settings. Play the film's first and last five minutes only in an empty room.
11. DCP, only after the test DCP passes, and encoded on the Windows PC, never in the cloud container [47]. DCP-o-matic 2.18.51 [8]. Container Flat 1.85, 2K, 24 fps, SMPTE, encryption off, JPEG2000 100 to 125 Mbit/s, single reel, ISDCF name on, content type feature [15]. Range Video [12]. Audio L and R at unity gain [13]. Timed text empty when captions are burned in [14].
12. Verify DCP in the Player (Tools, then Verify DCP). Fix every error and read every warning [18]. Play the DCP in the Player start to finish. This proves the package is well-formed, not that a cinema will accept it [17].
13. Write the drive with DCP-o-matic's Disk Writer: MBR, one primary partition of type 0x83, ext3 or ext2 with a 128-byte inode [19][26]. Label it "Do not read with a consumer computer". Never plug it into the Windows PC after writing [26].
14. Make a SHA-256 manifest of each delivery folder, copy the folder, and re-check the hashes from the drive [4].
15. Venue run: confirm the survey answers (T5). Run the test clip with the AV person present, then the full run, with a cold start under two minutes. Walk failure rungs 1 to 4 once each [5]. Gate G6 before final export; gate G6b at the venue full run.
16. Rights: one log row per asset, cue or person, using the T8 header. Assign tiers A to D (playbook Step 11). A RISK row needs why, how to undo it, who is exposed, and the date. Tier C items and every RISK row need the Fable advisor's written flag and at least 48 hours between drafting and deciding (inference).
17. Music: a commercial recording needs a sync licence and a master licence, and a performance licence is a third right [82]. Prefer CC0 or CC BY with credit (not NC), production music licensed for events, original music, or a licensed substitute.
18. Photos taken by others: find the photographer and record every search step. Orphan works have no US safe harbour [54]. The UK licence scheme starts at £20 per work and covers UK use only [62]. In India, s.17(b) may make the commissioner the first owner (copy read; date unknown; confirm) [70].
19. AI items: record the L-level, tool name and version, tool terms and a human-contribution note. Add a pre-roll line before the title. Mark photoreal motion of a real person as a possible deepfake [53][65].
20. Gates. T2 (27 February): every row green or a written RISK entry; no unlicensed commercial music; no Mojang assets. T3 (online): releases signed and the maker's explicit yes. T4 (cinema or festival): all T3 rows green, releases signed, E&O decision made, music cue sheet, AI disclosure [77][88].
21. Before any showing beyond 27 February, confirm the consent ledger has closed (Monday 29 March 2027) and the T3 or T4 gate is green [5].
22. Report back: what was checked, what is still TODO(research), and any conflict with the playbook (for example the venue loudness ceiling).

## Checklists

**Master and venue file (G6)**
- [ ] ffprobe fields recorded: 1920x1080, 24p, BT.709 tags, limited range.
- [ ] Colour-patch test passed after the last re-encode [3].
- [ ] Venue loudness and peak recorded. Mono-fold drop within about 3 LU.
- [ ] Captions inside the safe box, two lines at most, not in side bars.
- [ ] Metadata stripped; neutral file name; no title tag.
- [ ] Trims applied at export; each trim file hashed and logged.
- [ ] Manifest written; hashes re-checked from the drive.

**Venue playback day (G6b, TD-L9)**
- [ ] Test clip first, with the AV person present.
- [ ] Overscan off; HDR off; cinema or film mode; motion smoothing off.
- [ ] Captions readable from the back row; dialogue intelligible.
- [ ] Cold start under two minutes; failure rungs 1 to 4 walked.
- [ ] Two sticks, two laptops, settings photographed.

**DCP (before any cinema)**
- [ ] DCP-o-matic settings match Procedure step 11.
- [ ] Verify DCP: zero errors; every warning explained.
- [ ] Played in the Player start to finish.
- [ ] Drive: MBR, type 0x83, ext2 or ext3, inode 128, label set.
- [ ] Hash manifest matches the drive copy.

**Rights gate**
- [ ] Every row has a status: NS, ASKED, GRANTED, REFUSED, SUBST, RISK, OUT or VERIFY.
- [ ] Tier assigned; jurisdiction note present.
- [ ] Every RISK row has why, undo, exposed people and date.
- [ ] No Mojang name, asset or footage; no third-party game footage.
- [ ] No synthetic voice; every reconstruction labelled.

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
- Gather truthfully. The surprise may be omitted, but nothing untrue may be said. Read the consent card (T9, 4a) only when its bracketed lines are true [5].
- "Mostly public" triggers the public-rights answer. Family-circle assumptions do not hold for 27 February [56].
- Minors: a guardian's written yes, or the child is left out, or an adult-now yes (4f) [86][5].
- The dead: the closest family decides. Stills only unless they say more. Otherwise out [5]. Germany requires close relatives' consent for 10 years after death [68].
- The estranged: out by default, never contacted cold [5].
- Private data (names, consents, addresses) stays in the private repo. Nothing goes to a third-party service without the maker's explicit yes [1].
- Games and brands: no Mojang textures, sounds, UI or footage. "Minecraft" appears only as a secondary description, with the disclaimer [48].
- Misleading edits: a sequence must not present something as fact that it is not [85].
- Accepted risks are written down, reversible first, and decided by the maker with the advisor's flag.

## References

- `playbooks/theatrical-delivery.md`: the human guide (Decisions, templates T1 to T11, exercises, changelog).
- `research/theatrical-delivery.md`: the research notes, with the full citation list and the open gaps.
- `CHARTER.md`: principles 4 to 7 (real memories, dignity, theatrical bar, cleared for public screening).
- Key URLs: DCP settings https://dcpomatic.com/manual/html/ch07.html [15]; ISDCF Doc 3 https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf [26]; Minecraft Usage Guidelines https://www.minecraft.net/en-us/usage-guidelines [48]; Sundance FAQ https://www.sundance.org/submissions-faq [88].

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
- [48] Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 about 07:00 GMT; no visible date — physical locations, 150 participants, sharing equals commercial, name as title, disclaimer; extract hash c5a8...94222 matches earlier captures.
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
