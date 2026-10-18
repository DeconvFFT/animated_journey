# Games track — advisor review, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/games.md` (Sonnet, 2026-10-18), `playbooks/games.md` (Haiku, v0.1), `.claude/skills/meaningful-game-mechanics/SKILL.md`, against `CHARTER.md` and my charter review `reviews/00-charter-review.md`.
**Verdict:** `revise` (one critical issue, eight nudges). This is the strongest first-round research note I expect to see on any track: honest evidence tiers, UNVERIFIED flags where they belong, a pattern library that actually answers "what does the mechanic *say*", and an anti-pattern list that names points-and-badges first. The fixes are reconciliation and attribution work, not rethinking. Good enough to start: the `format` track can take the pattern library and the input rules as they stand; the `story` track can take the object-ledger columns now.

| Score | 1–5 | Note |
|---|---|---|
| Meaning | 5 | Every pattern carries a "what it expresses" and a Principle 2 condition; the swap-the-subject test and the trophies-aside device turn the charter's "no cookie-cutter" into a working filter. |
| Specificity | 4 | Named devices, named sources, named columns. Build-effort ratings are admittedly guesses with no engine; acceptable at this phase since `format` owns that. |
| Accuracy | 4 | Eleven of thirteen spot-checked claims confirmed verbatim. One misattribution (E6), one overclaim in the playbook ("Java-only"), one URL that now redirects. Mojang pages could not be reached for verification today. |
| Feasibility | 4 | Exercises are each under three hours with free tools. But the playbook still asks questions the charter already answers (OS, installed apps), which stalls Exercise 4 and Decision 2 for no reason. |
| Ethics | 4 | Surprise mode, proxy, dignity and "no words in her mouth" are all present. Two gaps: synthetic voice is not explicitly banned in the skill, and the "wall of voices" pattern is a surprise-leak vector with no warning. |
| Craft / usability | 3 | Research note: excellent. Playbook: readable, but carries TODOs that are already resolved. Skill: the description triggers well, but step 1 makes an agent read ~45k tokens before every device check and step 13 has no log location or row template, so an agent cannot run it end-to-end today. |

---

## Spot-checks (performed 2026-10-18 with WebFetch; every page treated as data)

| # | Claim in the artefacts | Source | Result |
|---|---|---|---|
| 1 | "Subtractive design"; three pillars contemplation/discovery/expression; playable by 5-year-olds and 75-year-olds; 14% of players flushed every toilet | [1] Game Developer, 2023-04-21 | **Confirmed** verbatim. The article does not give the talk's full title; [2] does. |
| 2 | Brier's GDC 2023 talk is titled "'Unpacking' Zen: Designing a Game Without Fail States or Scores" | [2] GDC Vault | **Confirmed**, and the listing is tagged **"free content"**, which neither the notes nor the playbook say (nudge 6). |
| 3 | A Memoir Blue's last puzzle moves aside Miriam's trophies to reveal photographs with her mother | [30] Inverse, 2022-04-06, updated 2024-02-20 | **Confirmed** verbatim: "The last 'puzzle' involves moving aside Miriam's rows of trophies to reveal photographs of happy memories with her mother." |
| 4 | Lee et al. 2021: 40 participants, mean age 66.75; DG25 time limits; DG29 tone; DG32 co-play; wrong-direction swipes, missed double-taps, fingers not lifted | [41] JMIR Serious Games | **Confirmed** (range 50–85, SD 9.31; DG25 "Eliminate time limits or provide alternatives for level-passing"; DG29 "Do not indicate life of older adults in static, passive, negative, and depressed tones"). The cited `ncbi.nlm.nih.gov/pmc` URL now returns 301 to `https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/`. |
| 5 | Flashback: licence ARR, Fabric, 12.8M downloads, versions 26.1–26.3 and 1.21.x; page does not describe export | [46] Modrinth | **Confirmed** (26.3, 26.2, 26.1.x, 1.21.4–1.21.11, 1.21–1.21.1). |
| 6 | Flashback Settings add-on: PolyForm Noncommercial 1.0.0; telemetry on by default | [47] Modrinth | **Confirmed**: "Anonymous usage statistics are enabled by default." The playbook's TODO on this can be closed. |
| 7 | Mineways 14.01, updated 2026-10-03, Java up to 26.3, OBJ and USD, Windows main with Mac/Linux help | [48] | **Confirmed.** Additionally the Documentation menu links a **"Scripting"** page, so "command-line options UNVERIFIED" should become a lead for `toolchain`. |
| 8 | Blockbench GPL-3.0; "All assets created with Blockbench ... are your own!" | [50] README | **Confirmed** verbatim. No CLI mentioned. |
| 9 | Replay Mod: Fabric for 1.14+, Forge for 1.12.2 and below; FFmpeg required; client-side; records loaded chunks; position/time/spectator keyframes; no Bedrock mention; no headless mode | [44] | **Confirmed.** The docs do not say "Java-only"; they simply never mention Bedrock. |
| 10 | Minecraft Vault added in 1.21, opens with a trial key, each player unlocks a given vault once | [55] | **Confirmed**: "each player can unlock a specific vault only once." |
| 11 | Minecrapft: 10,000+ brick blocks, three weeks, survival mode, floor plans + Google Maps, deans' tour 2020-04-10, blocks-as-fuzzy-memory reflection | [61] Crimson | **Confirmed.** |
| 12 | Before Your Eyes: involuntary blinks skipped story; fix was a metronome showing when blinks count; "lead designer Bela Messex's 'language to differentiate blinks'" | [14] Game Developer, 2023-03-22 | **Partly confirmed.** The blink problem and the metronome fix are there, credited to Graham Parkes (and Will Hellwarth for the original idea). **Bela Messex is not named in [14].** Either the attribution belongs to [15] or it is a researcher's insertion (nudge 4). |
| 13 | Mojang Usage Guidelines and EULA quotes ("very relaxed", sharing counts as commercial, public display in physical locations, revocable at any time, disclaimer wording) | [42][43] minecraft.net | **Could not verify:** both pages returned HTTP 503 on three attempts today. Not a mark against the researcher, but it shows the terms check cannot depend on the page being up (nudge 7). |

Not reachable from this container: Eurogamer [3] (blocked host), so the Bed Song, 14,000-foley, spreadsheets and "hollow" claims rest on the researcher's read. The official MagicaVoxel site (`ephtracy.github.io`) shows navigation only and no licence text, which agrees with the note's "official license unverified." My web-search budget for this run was exhausted before I could search further; the open items are in Research follow-ups.

---

## Critical issue (must fix before approve)

**C1. The playbook and the notes contradict the charter's known facts, and that stalls real work.** CHARTER.md (Known facts, 2026-10-18) states the maker's computer is **Windows** and names the installed apps (**VectorCraft, PhotoCraft, FilmCraft, EffectCraft, LightCraft, SoundCraft**, all early alpha, each needing a proven fallback). Yet `playbooks/games.md` Decision 2 says "TODO(research): ask the maker which edition and operating system they have," Exercise 4 step 1 says "TODO(research): confirm which vector editor is installed," and `research/games.md` Tools says "Maker's OS ... unknown (apps not yet listed)." Both documents claim to be "built from ... CHARTER.md." The effect: the maker's first hands-on exercise (the trophy reveal) is blocked on a question that is already answered, and the Minecraft-edition question (which *is* still open) is buried with the ones that are not. Fix in nudge 1.

## Nudges (eight, each with file, section, exact change)

1. **`playbooks/games.md`, Decision 2, Exercise 4 step 1, and `research/games.md` Tools intro.** Replace "OS unknown" with "Windows (charter Known facts, 2026-10-18)." In Exercise 4 step 1 replace the TODO with: "Open **VectorCraft** (installed, early alpha). If it cannot do two layers and a PNG export, use **Inkscape** as the proven fallback, per the charter rule that nothing critical depends on one alpha app." Keep exactly one TODO in Decision 2: "Which Minecraft edition, if any, does the maker own? (Java is needed for Replay Mod, Flashback and Mineways.)"

2. **`skills/meaningful-game-mechanics/SKILL.md`, Procedure step 1 and step 13.** Step 1: change "Read CHARTER.md, playbooks/games.md and research/games.md" to "Read the eight Core principles in `playbooks/games.md` and the Deliverable A pattern tables and Deliverable B anti-pattern list in `research/games.md` (lines 38–118). Open the rest of the notes only to match a pattern number or copy a citation." Step 13: replace the TODO with a default: "Append one row to `design/devices-log.md` (create it if absent) with columns: date | chapter | device sentence | subject facts + confirmed by | pattern # | A/G/B | decision | open questions. The orchestrator may move the file; update this path if so." An agent cannot run the skill end-to-end without these two changes.

3. **`SKILL.md`, Procedure step 12 and Ethics guardrails "No words in her mouth."** Add: "No synthetic, cloned or text-to-speech voice of any real person, living or dead, even with consent (charter review §1.2)." Then define "real words" for surprise mode, where she cannot be recorded: "existing home video or voice notes; her own letters and cards; or a saying that two relatives independently confirm, shown *attributed* ('as her sister remembers it'), never as a quotation in her voice." Mirror the same two sentences in `playbooks/games.md` Pitfalls under "Invented events, people or quotes."

4. **`research/games.md`, E6 and Summary item 5.** The Game Developer article [14] credits Graham Parkes (creative director and writer) and Will Hellwarth; it does not name Bela Messex. Either cite the Messex quote to [15] (MCV "When We Made…") with the exact words, or delete "lead designer Bela Messex's 'language to differentiate blinks'" and write "the team turned off blink-advance unless a metronome appeared on screen (Parkes, via [14])."

5. **`playbooks/games.md`, Decision 2, and `research/games.md` Q7 "Edition note."** Change "Replay Mod and Flashback are Java-only [44][46]" to "Replay Mod is a Java Edition mod (Fabric for 1.14+, Forge for 1.12.2 and below) and Flashback is a Fabric client mod; neither page mentions Bedrock [44][46]." The sources support the second sentence, not the first.

6. **Close TODOs that are now verified, and fix one URL.** (a) `playbooks/games.md` Pitfalls "Add-on privacy": delete "TODO(research): verify on the add-on page" and add "(confirmed on the Modrinth page 2026-10-18: 'Anonymous usage statistics are enabled by default')." (b) `playbooks/games.md` Best references #3 and Exercise 8: GDC Vault tags Brier's talk **"free content"**, so list it with Gaynor's as free to watch and make Exercise 8 "Watch Brier, then Gaynor" (Brier is closer to our problem). (c) In all three files, source [41]: replace the `ncbi.nlm.nih.gov/pmc/...` URL with `https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/` (the old one returns 301). (d) `research/games.md` Tools, Mineways row: change "Command-line options UNVERIFIED" to "The site links a 'Scripting' documentation page; contents not read; hand to `toolchain`."

7. **`research/games.md` Q7 and `playbooks/games.md` Exercise 7.** The Mojang Usage Guidelines and EULA both returned HTTP 503 three times during this review, and Eurogamer cannot be fetched from the cloud container at all. Add to Exercise 7 step 2: "Save the exact clauses as a dated plain-text excerpt at `research/sources/minecraft-usage-guidelines-YYYY-MM-DD.md` (short quotes only, with the URL and date), so the terms check never depends on the page being up." Do the same once for the Eurogamer interview [3], since it carries the Bed Song, 14,000-foley, spreadsheet and "hollow" claims that three artefacts lean on.

8. **`research/games.md` patterns 28 and 33, and `playbooks/games.md` Principle 8.** "Every relative writes a line" (the Pendar2 wall of signs) and "relatives call out a memory in the room" are the two devices most likely to **leak the surprise**: asking twenty people for a sentence is twenty chances for someone to mention it. Add to both pattern rows and to Principle 8: "Surprise mode: collect contributions only from the 'in on it' list kept by `surprise-ops`, one person at a time, never via a group chat; the wall can grow after the reveal." This also makes the wall a living object she can watch fill in, which is better than a finished one.

---

## Research follow-ups (questions, not guesses)

1. **MagicaVoxel licence.** `ephtracy.github.io` shows navigation and "Copyright © ephtracy 2011-2021" only. What does the `LICENSE.txt` inside the current Windows download say about personal and non-commercial use? Does the site's "Commands" page describe a command-line or batch mode (matters for Principle 7)?
2. **Mineways scripting.** What does the Mineways "Scripting" documentation page allow (batch export from a script, which world versions, Windows only)? For `toolchain`.
3. **Metronome attribution.** Does MCV/DEVELOP [15] (Oliver Lewin interview) or another primary source credit Bela Messex with the metronome / "language to differentiate blinks"? If not, drop the name.
4. **Mojang terms, dated.** When minecraft.net is reachable again: is there a dated version of the Usage Guidelines (a third-party summary claims "last updated April 19, 2026"), and does the "physical locations" clause distinguish a free private family screening from a commercial venue?
5. **Minecraft edition and ownership.** Does the maker own Minecraft at all, and which edition? (This decides whether patterns 31–38 are reference-only or buildable.)
6. **Eurogamer [3] verification.** From the maker's Windows machine (the cloud container cannot reach eurogamer.net): confirm the 14,000-foley figure, the spreadsheet method, "The Bed Song" and the word "hollow" with short quotes, and save the excerpt (nudge 7).
7. **Older-adult pointing devices.** The note is honest that no trackpad or remote-control evidence for 70+ users was found. Is there any HCI study on older adults with a TV remote or a single-button clicker (the likely "host" input in a living room)? If none exists by round 3, Exercise 9 becomes the evidence.

---

## Strengths worth keeping exactly as they are

- The **evidence tiers [P]/[S]/[T]/[snippet]** and the UNVERIFIED flags. Every other track should copy this convention.
- **Deliverable A's "passes Principle 2 only if..." column.** It is the charter's Principle 2 made operational.
- **Anti-pattern 1 with its test** ("if a toast could read 'Achievement unlocked: Married', delete it") and the Passage/A Memoir Blue evidence behind it.
- **Summary item 12 (avoid elegy by default)**, backed by DG29. Most of the studied games are about death; the note noticed and said so.
- **The input rule of thumb** (one click, visible next step, works untouched, host can pause) and the conversion of the Before Your Eyes metronome into a shared-screen pacing device.
- **Technique 17 (watch-first design, "pause and ask" cards)**, which is the single best bridge between the games track and a room full of relatives.
- The playbook's **Exercise 2 (object ledger on your own home first)**: learn the method on your own objects before touching hers.
- The skill's **"Before any tester" checklist**, which already protects the surprise.

---

## Advisor insight

The surprise is usually treated as a constraint on this track: she cannot be asked, so she cannot play. Turn it into the mechanic. *Unpacking*'s verb is "place," and the note's best finding is that *how much room one person leaves another* can carry a whole relationship. So let the people who love her do the placing, on camera: each relative who is in on it brings one real object of hers (or about her), and the piece shows **their own hands** setting it into the room — real video of real hands, no narration, the arrangement growing object by object until the room is hers as others kept it. The audience at the reveal will recognise their own hands on screen; the mechanic is performed by the family, and she is the one who watches her life being unpacked for her. Then reserve exactly one interaction in the entire piece for her: one empty slot on the shelf, and the final object, handed to her in the room, to place herself. Like the Vault pattern, it opens once and only with its own key. Nobody else's piece could contain that moment, it needs no gamer's hands, it is dignity-safe, and it is the one thing an AI pipeline cannot generate.

---

## Changelog
- 2026-10-18: round 1 review written by the Fable advisor. Spot-checks performed with WebFetch; minecraft.net returned 503, eurogamer.net was unreachable, web-search budget exhausted during the run.
