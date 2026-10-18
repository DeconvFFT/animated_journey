# theatrical-delivery — round 1 of 3 (Fable advisor)

**Date:** Sunday 2026-10-18 (week 1 of 19; premiere Saturday 2027-02-27)
**Reviewed:** `research/theatrical-delivery.md` (767 lines), `playbooks/theatrical-delivery.md` (v1, 663 lines), `.claude/skills/theatrical-delivery-and-rights/SKILL.md` (161 lines), against `CHARTER.md` and my brief review `reviews/02-film-briefs-review.md` §1.5.
**Maker's standing instruction (relayed verbatim):** "for now only me and i will only bne the one on this project"; the question of who else is in on the secret and who approves the hard chapters "can wait until the plan is ready". I treat that as binding on this review: nothing below asks the maker to bring anyone in; several nudges ask the playbook to state plainly what "only me" costs the film so the deferred decision is an informed one.

**Verdict: revise.** Scores: meaning 3, specificity 5, accuracy 4, feasibility 4, ethics 4, craft 3.

This is a strong, honest research round done under a real handicap (the search budget died after four calls, and the researcher said so instead of working around it). The playbook is the most usable technical guide the project has produced so far. The revisions needed are mostly about making the plan true to the maker's "only me" and about closing a handful of self-inflicted TODOs that would stall an agent.

---

## 1. Spot-checks (12 claims, all fetched today)

| # | Claim in the artefacts | Source checked | Result |
|---|---|---|---|
| 1 | DCP-o-matic stable **2.18.51, released 16 October 2026**; Windows 64/32-bit, macOS, Linux [8] | https://dcpomatic.com/download | **Confirmed** verbatim ("2.18.51", "16th October 2026"). |
| 2 | "Use 2K unless you have content that is of high enough resolution to be worth presenting in 4K"; bandwidth 50–250 Mbit/s; "Most commercial DCPs use bit rates between 75 and 125 Mbit/s"; "If in doubt, use SMPTE"; FAT32 4 GB note [15] | https://dcpomatic.com/manual/html/ch07.html | **Confirmed** verbatim. Note: ch07 does **not** list Flat as 1998x1080; that figure in T2 rests on [31] (Wikipedia) and [12]. Fine, but cite it that way. |
| 3 | ISDCF Doc 3: MBR only (no GPT), one primary partition type 0x83, EXT3 or EXT2 with 128-byte inode, `mkfs -t ext3 -I 128 -m 0`, assume USB 2.0 type A, "not safe to connect ... to general purpose computer running many common consumer operating systems", suggested warning label [26] | https://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf (text extracted locally) | **Confirmed** verbatim. Two useful extras the notes missed: MBR limits the drive to 2 TB, and "Storage device purchased at retail, particularly USB sticks, may have existing partition tables ... almost certainly ... incorrect", so always re-partition. |
| 4 | DCP-o-matic: "the only format that is guaranteed to work in all cinemas is ext2"; Disk Writer formats and copies from Windows/macOS/Linux; network transfer preferred when small enough [19] | https://dcpomatic.com/manual/html/ch20.html | **Confirmed.** Playbook Step 9.10 says "ext3 or ext2 ... Disk Writer does this": Disk Writer writes **ext2**; say ext2. |
| 5 | Subtitle options: VF DCP "usually the best option"; projector-rendered "mostly works well but is not 100% reliable"; burnt-in "less likely to go wrong, especially ... unusual subtitle positioning or character sets" [20] | https://dcpomatic.com/manual/html/ch17.html | **Confirmed** verbatim. |
| 6 | Frame rates: 24 fps / 48 kHz the only rates safe "if you are sending DCPs to unknown places"; 25-in-24 plays slower with resampled audio [16] | https://dcpomatic.com/manual/html/ch12.html | **Confirmed** (paraphrase accurate). |
| 7 | Colour presets sRGB, Rec. 601, Rec. 709, Rec. 1886, Rec. 2020, S-Gamut3, P3; Range Video 16-235 / Full; "In most cases DCP-o-matic will guess the correct Range setting" [12] | https://dcpomatic.com/manual/html/ch06s04.html | **Confirmed.** The manual's own suggestion for HD content is **Rec. 709**; the "Rec. 1886 for a gamma-2.4 grade" lean is the researcher's inference and is correctly marked unverified. |
| 8 | EBU R 95: action safe 3.5%, graphics safe 5% [37] | https://tech.ebu.ch/docs/r/r095.pdf (text extracted locally) | **Confirmed** ("The action safe area is 3.5% and the graphics safe area is 5%, at the top, bottom and ..."). |
| 9 | Microsoft: Windows fonts for "captions and text included in videos" allowed "providing the captions or text is rendered as a bitmap image, and the font files themselves are not embedded within the video file"; no conversion; page dated 2024-11-19 [76] | https://learn.microsoft.com/en-us/typography/fonts/font-faq | **Confirmed** verbatim, including `ms.date: 2024-11-19`. |
| 10 | UK IPO orphan works: £20 application fee for one work; licence up to 7 years; UK use only [62]; playbook/skill say "from £20 per work" | https://www.gov.uk/guidance/copyright-orphan-works | **Mostly confirmed; wording slip.** The fee is a sliding scale: £20 for 1 work, £24 for 2, £30 for 5, £80 for 30 (not "£20 per work"), non-refundable, **plus a separate licence fee if granted**. Page last updated 1 December 2025. |
| 11 | Sundance 2027 FAQ 8: "public theatrical exhibition" = tickets "made available for purchase or given freely to members of the general public"; "private, invite-only or 'cast and crew' screenings ... are not considered"; FAQ 12 AI disclosure or disqualification; FAQ 18 screener 4500 kbps H.264 / 256 kbps AAC stereo / max 1080 px; FAQ 31 DCP with Closed Caption **and** Open Caption versions, ProRes for online, open keys [88] | https://www.sundance.org/submissions-faq (PDF, text extracted locally; created 2026-09-08) | **Confirmed** verbatim. FAQ 31 adds "these specifications are subject to change at any time". Rules PDF header confirms "2027 SUNDANCE FILM FESTIVAL". |
| 12 | 17 U.S.C. 101 "publicly": "a place open to the public or at any place where a substantial number of persons outside of a normal circle of a family and its social acquaintances is gathered" [56] | https://www.law.cornell.edu/uscode/text/17/101 | **Confirmed** verbatim. |
| 13 | Minecraft Usage Guidelines re-read: extract hash `c5a8253c...94222`, all 12 tracked quotes present; theatre example; 150 participants; "may be revoked at any time"; disclaimer text [48] | https://www.minecraft.net/en-us/usage-guidelines (curl at ~08:50 GMT; WebFetch returned 503) | **Confirmed.** Ran `research/sources/check_mojang_quotes.py` on today's capture: 37,148 chars, sha256 `c5a8253c842dfe436b058295a5b09a7e26ecb1c85b53e1b17c84300253b94222`, 12/12 PRESENT. Same hash as the researcher's three captures. |

**Computed figures re-checked:** 125 Mbit/s = 937.5 MB per finished minute (0.94 GB, correct); 4 GiB at 20 Mbit/s = 28.6 min (correct); 24→25 fps = 4.17%, 0.707 semitone (correct); 8% line on a 5.4 m screen at 12 m ≈ 2.06°, on a 55-inch TV at 3 m ≈ 1.05° (correct).

**Commands the playbook marks "untested" or "TODO(research)":** I ran them in the container (ffmpeg 6.1.1) on a 1-second synthetic 1080p24 file:

```
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,pix_fmt,color_range,color_space,color_transfer,color_primaries,r_frame_rate,nb_frames:format=duration \
  -of default=nw=1 FILE
```
prints `pix_fmt=yuv420p color_range=tv color_space=bt709 color_transfer=bt709 color_primaries=bt709 r_frame_rate=24/1 nb_frames=24 duration=1.000000`. `ffmpeg -i in.mp4 -map_metadata -1 -c copy out.mp4` removed the `title` tag (ffmpeg re-adds a harmless `encoder=Lavf...` tag; no personal data). `ffmpeg -i in.mp4 -vf lut3d=trim.cube ...` applied a `.cube` LUT without error. So three TODOs can be closed today; they still need one run on the Windows PC (Gyan build) to be marked done there.

No fetched claim failed. Accuracy is high; the slips are wording, not substance.

---

## 2. Scores and reasoning

**Meaning: 3.** The technical half is faithful to the charter (one master, real-screen judgement, surprise kept inside the files). The rights half has the right spine (tiers A–D, the three-stage releases resolution, her release with a per-scene veto, no synthetic voice). What is missing is the one sentence the maker most needs: under "only me", **no living relative's voice can be in the public cut before the premiere**, because asking for consent reveals the film, and Tier C already (rightly) puts any voice of a living person behind an explicit yes. The playbook's Tier A and the consent card 4a quietly assume a ring of contributors who are in on it; the charter and the maker's own words say there is none. That is not a legal footnote, it is the film's narrative voice. The playbook should state the consequence and the three paths (maker's own narration; attributed text and still photographs under Tier B; bring someone in later) so the deferred decision is informed, not forced.

**Specificity: 5.** Named settings, dialog names, commands, dates, line IDs that merge into the surprise-ops run sheet, a CSV header, a question list. Nothing is hand-wavy.

**Accuracy: 4.** Twelve of twelve fetched claims hold, most verbatim. Deductions: "£20 per work" (it is a sliding application fee plus a separate licence fee); "ext3 or ext2 ... Disk Writer does this" (Disk Writer writes ext2, which DCP-o-matic calls the only guaranteed format); Flat 1998x1080 attributed to ch07, which does not give the figure; and three "untested" items that were testable in the container in under a minute.

**Feasibility: 4.** The DCP is correctly made optional and PC-side; the venue MP4 is the real deliverable; the home-TV test clip is a good learner's exercise. Two gaps: the first look at the **real venue screen** is Monday 22 February, five days out, so any Trim V or caption-size surprise forces re-exports in premiere week; and there is no branch for "the venue turns out to be a cinema with a DCP server", which, for a maker who wants a theatre, is a live possibility and would make the DCP primary.

**Ethics (incl. rights): 4.** Tiers, the dead, minors, the estranged, no cloned voices, truthful omission not falsehood, personal data kept in the private repo: all present and consistent with Principles 4, 5 and 7. One structural flaw (the contributor-ring assumption above) and one small one: the skill tells an agent to obtain "the Fable advisor's written flag" without saying how (where the request goes, what the flag file is called, how long to wait).

**Craft / usability: 3.** Playbook: clear, ordered, checkable, well-pitched for a learner. Skill: the description triggers well (it names the deliverables and the decisions), and the 22-step procedure is agent-usable, except that it instructs the agent not to invent an ffprobe command and marks `lut3d` and `-map_metadata -1` untested when all three run today; an agent following the skill would stall on step 3 for no reason. The theatrical bar itself is held (one grade, two trims, test on the real screen, Verify DCP, hashes), but the schedule puts the only real-screen test in premiere week.

---

## 3. Critical issues (must be fixed before approval)

1. **The releases plan assumes contributors who are in on the secret; the maker has said there are none.** `playbooks/theatrical-delivery.md` Step 11 Tier A ("contributors who gave recorded consent on the updated card") and T9 4a ("[MAKER] is making a film about [NAME]'s life as a surprise gift") both bring the listener into the ring. `CHARTER.md` Known facts and the maker's relayed words say only the maker knows, with relatives used only through asks that do not reveal the project, "unless the maker later decides to bring someone in", a decision the maker has deferred. The playbook must (a) say that reading 4a to anyone **is** that decision and is parked; (b) say what the public cut can therefore contain before the premiere: the maker's own material and narration, her appearances by proxy, Tier B stills of adults, attributed text with no voice, cleared or original music; (c) say plainly that relatives' recorded voices wait for the post-premiere release (T9 4d) and so appear only in T1 (her private version) or later showings; and (d) put the decision point on the calendar (the research already picks Fri 4 Dec 2026 for the consult; the "bring someone in?" decision belongs at or before the Sunday 3 January 2027 resolution lock, when the narration plan is fixed). The same change belongs in `SKILL.md` Procedure step 16 and the Rights gate checklist.

---

## 4. Nudges (8, each file + section + exact change)

1. **`playbooks/theatrical-delivery.md`, Step 11 and T9 4a** — add a boxed paragraph headed "Only-me mode (current)" directly under the tier table: "Until you decide to bring someone in, card 4a is not read to anyone. Tier A before the premiere = your own material, her appearances by proxy, and original/CC0/licensed assets. Relatives' voices: private cut only, or after 4d. Decision point: by Sun 3 Jan 2027." Mirror it in `SKILL.md` step 16 and the Rights gate checklist ("No living person's voice in the public cut without a recorded yes; under only-me mode that means none before the premiere").

2. **`playbooks/theatrical-delivery.md`, Step 8 and Exercise 5; `SKILL.md` Procedure step 3 and step 9** — replace "The exact command is TODO(research); do not invent one" with the ffprobe command above (verified in the container 2026-10-18, ffmpeg 6.1.1; "run once on the Windows PC and tick"). Change `lut3d` and `-map_metadata -1` from "untested" to "run in the container 2026-10-18; note ffmpeg re-adds an `encoder` tag, which carries no personal data; confirm on the PC".

3. **`playbooks/theatrical-delivery.md`, T4 run-sheet and Step 10** — add **TD-L2b, by Sun 17 Jan 2027: visit the venue with the test clip only (no film), with the AV person; record TV/projector settings, caption sizes 20/23/26 from the back row, PLUGE, tone level; set Trim V and TD-3 caption size from this visit.** Rationale: today the first real-screen look is Mon 22 Feb; a caption or black-level surprise then costs re-exports in premiere week. If the venue is not yet booked by 17 Jan, say so and move the line, but keep it before TD-L8.

4. **`playbooks/theatrical-delivery.md`, Decisions table and Step 9** — add a branch to TD-6/TD-4: "If the venue survey (T5, 6 Nov) says the room is a cinema with a DCP server: the DCP becomes the primary deliverable, Exercise 3 moves to Sun 29 Nov 2026, book a real-cinema test slot in January, and the venue MP4 over HDMI becomes rung 1 of the backup ladder." Also note from the ch07 check that content type "feature" vs "short" places the film in the projectionist's interface; pick the one that matches the final runtime.

5. **`playbooks/theatrical-delivery.md`, Step 11 (photos) and `SKILL.md` step 18** — change "from £20 per work" to "UK IPO application fee £20 for one work (sliding scale: £24 for two, £30 for five, £80 for thirty), non-refundable, **plus a separate licence fee if granted**; licence up to 7 years, UK use only; page updated 1 Dec 2025 [62]".

6. **`playbooks/theatrical-delivery.md`, Step 9.10, T2 "Media" row and `SKILL.md` step 13** — say "ext2 (DCP-o-matic: the only format guaranteed in all cinemas; ISDCF also allows ext3), 128-byte inode, MBR with one primary 0x83 partition; re-partition any retail USB stick first (ISDCF: retail partition tables are 'almost certainly incorrect'); MBR drives must be 2 TB or smaller [19][26]". In T2 Picture row, cite Flat 1998x1080 to [12][31], not [15].

7. **`SKILL.md`, Procedure step 16 and the Ethics guardrails** — specify the mechanism for the advisor flag so an agent can act: "Write the item as `rights/flags/<asset_id>.md` (why, undo, exposed, draft date), request a Fable review of that file, and do not set status RISK or admit a Tier C item until the file carries a dated advisor line and 48 hours have passed." Add the same two sentences to the playbook's Step 11 "Accepted risk" bullet.

8. **`playbooks/theatrical-delivery.md`, T2 Cinema "Captions" row and Pitfalls** — restore the research's note that a festival-style delivery (Sundance FAQ 31) requires **both** a Closed Caption and an Open Caption DCP version, which burned-in captions alone cannot satisfy; add "specifications subject to change" and the date read (2026-09-08 document). Add to Step 5 the one-line settlement of the dBTP conflict: "-1 dBTP (R128 and the research); the toolchain's -1.5 was a loudnorm example, not a target", so the maker is not asked to adjudicate a non-decision on the settings card.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

- Which gamma value each DCP-o-matic colour preset applies (Rec. 709 vs Rec. 1886), from the source or a test frame; whether a ProRes 422 HQ `.mov` imports cleanly; DCP-o-matic 2.18.51 memory use and encode speed on the maker's Windows PC (Exercise 3 will measure it; a forum or release-note figure would set expectations earlier).
- Windows 11 Settings path for setting a 24 Hz refresh rate on an external display, and whether the maker's laptop GPU offers 24/48/72/120 Hz over HDMI.
- What the ISDCF name shows when only L and R are mapped in a 6-channel container ("20" vs "51"), from DCP-o-matic's naming code or a test build.
- Venue-licence coverage statements from PRS/PPL (UK), ASCAP/BMI (US) and IPRS (India) on whether a blanket licence covers music inside a film shown at a hired hall (the pages returned 403 this round).
- Public-liability and E&O expectations for a one-off four-wall hire in the maker's country (TD-7 first); 2026 E&O premium range for a short from at least one broker page.
- Whether the EU AI Omnibus (in force 27 Jul 2026) changed the Article 50 transparency timeline, and whether a private individual showing a film at a public gathering is a "deployer".
- Current text of India Copyright Act s.17(b) (commissioned photographs) from an official, dated source; UK and India post-mortem image/privacy rules.
- Family-film clearance practice: one or two documented accounts (festival Q&As, filmmaker blogs, archive-house guidance) of how personal-documentary makers handle relatives' old photographs and voices, to test the Tier B synthesis.

---

## 6. Strengths (keep these)

- Honest about the search outage and about every inference, computation and unverified item; the UNVERIFIED tagging is exemplary and the spot-checks bear it out.
- "One master, many derived files; judge on the real screen; plan the failure first; burn the captions in; keep 24 fps": five principles a learner can hold in their head, each sourced.
- The surprise is treated as a technical property of the files (titles, ISDCF names, metadata, Recent lists, who sees the test clip vs the film), not only a social one.
- The neutral venue test clip (T7) is a genuinely good device: it lets staff test everything without seeing anything, and it doubles as the learner's colour, caption and mono-fold classroom.
- The three-stage releases resolution and her own release (4e) with a per-scene kept/changed/removed/closed-until ledger is the most dignified answer yet to "she cannot approve it in advance".
- The Minecraft re-read is reproducible (hash, script, dated excerpt) and I reproduced it today.
- Run-sheet lines carry IDs that merge into surprise-ops without renumbering.

---

## 7. Advisor insight

Turn the premiere's playback into a one-shot "projection" of her life rather than a file that happens to be played. Concretely: the venue test clip already has a countdown and slate. Build the **real film's first thirty seconds as a projection leader in her own visual grammar**, a countdown made of the years of her life (1970s... 1980s...) ticking down in the texture of each decade's photographs, with the 1 kHz line-up tone replaced by a single real sound from her world (a kettle, a sewing machine, a bicycle bell) at the mix's reference level. It is technically the same leader the AV person needs (level, sync, framing, overscan check all still readable), so it costs nothing to rehearse and reveals nothing in rehearsal if the rehearsal copy uses the neutral slate. But on the night, the room's first image is not "bars and tone", it is the film teaching the audience how to watch it: time is the material, and this is the tempo. The stranger in row seven learns in thirty seconds that she is about to be shown a life, not a party video, and the maker gets a leader that silently proves the chain (levels, edges, sync) before the first real frame, which is what a projectionist's leader was always for.

---

## Changelog
- 2026-10-18: round 1 by the Fable advisor. 13 claims fetched and checked (12 web sources plus a reproduced Minecraft hash); three "untested" commands run in the container. Verdict revise; one critical issue (contributor-ring assumption vs "only me"); eight nudges.
