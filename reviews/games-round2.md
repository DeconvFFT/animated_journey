# Games track — advisor review, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/games.md` (Sonnet, incl. "Follow-up research (round 1)" F1–F7), `playbooks/games.md` (Haiku, v0.2), `.claude/skills/meaningful-game-mechanics/SKILL.md`, against `CHARTER.md` (Known facts updated 2026-10-18), `reviews/00-charter-review.md` and `reviews/games-round1.md`. Also opened: `research/excerpts/games-round1-followup-2026-10-18.txt` and `research/sources/minecraft-usage-guidelines-2026-10-18.txt`.
**Verdict:** `revise` (one critical issue, seven nudges). Every round-1 nudge was applied, and the follow-up research is exemplary: it corrected its own premise (no LICENSE.txt in the MagicaVoxel zip), found the licence where it actually lives, read the Mineways scripting page end to end, and separated the Messex quote from the metronome with the exact words. What blocks approval is not the games work itself but a drift between these three artefacts and the charter's Known facts as updated today: the skill still routes hard chapters to a "trusted close relative", and the playbook still leans on a private home showing and a click-through scroll story. The charter now says the maker is the only insider and her proxy, the premiere is a mostly public gathering, and the film is the main event. Good enough to start: `format` and `film-story` can take the pattern library, the "as animation" ratings and the input rules now; `story` can take the object-ledger columns and the surprise-mode "real words" definition now.

| Score | 1–5 | Note |
|---|---|---|
| Meaning | 5 | Unchanged from round 1: every pattern says what it expresses and when it passes Principle 2. The surprise-safe wall-of-voices rule makes pattern 33 a living object rather than a leak. |
| Specificity | 4 | Follow-up F1/F2 turned two vague tool rows into exact commands (`odir obj`, `mineways.exe -headless`, stdin READY/OK/ERROR). Excerpt paths in Exercise 7 point to files that do not exist (nudge 5). |
| Accuracy | 4 | Five of five reachable spot-checks confirmed verbatim. Two stale items: [51] still labelled "official license unverified" after [76] resolved it; Principle 6 still carries a TODO that Wikipedia and Dallas's talk settle. minecraft.net unreachable again (503), which the excerpt rule now covers. |
| Feasibility | 4 | Exercises remain under three hours with free tools; VectorCraft-then-Inkscape is the right shape. Decision 9's scroll-story lean is now out of step with the film-first charter and would send the maker down a path the charter closed (nudge 3). |
| Ethics | 3 | Voice ban, attributed sayings, surprise-mode contribution rule, tester checklist: all present and well written. But SKILL.md step 10 and Decision 8 send dignity decisions to a relative who, per the charter, is not in on it. That is both the wrong decision-owner and a surprise leak (C1). |
| Craft / usability | 4 | The skill is now runnable by an agent end to end: step 1 reads ~80 lines instead of 45k tokens, step 13 has a log path and row template. Description triggers on the right words (achievements, timers, drag, Minecraft asset). Playbook is readable; three TODOs can be closed today. |

---

## Round-1 nudges: were they addressed?

| # | Nudge | Status | Evidence |
|---|---|---|---|
| 1 | Windows / VectorCraft / one TODO in Decision 2 | **Done** | `research/games.md` Tools intro: "The maker's computer is **Windows**"; playbook Exercise 4 step 1 names VectorCraft with Inkscape fallback; Decision 2 has exactly one TODO (edition). |
| 2 | SKILL step 1 scope; step 13 log path and row template | **Done** | Step 1 names the eight principles and lines 38–118 (still accurate: Deliverable A starts at 38, B ends at 117). Step 13: `design/devices-log.md`, eight columns as specified, "create it if absent". |
| 3 | Synthetic-voice ban and surprise-mode "real words" | **Done** | SKILL step 12 and Ethics guardrail "No words in her mouth"; playbook Pitfalls "Invented events, people or quotes". Wording matches the nudge. |
| 4 | Messex misattribution in E6 and Summary 5 | **Done, and verified today** | E6 quotes Lewin via [15] with the exact words and says "No source says who proposed the metronome or that the two are the same." Summary 5 names nobody. I fetched [15]: the sentence is verbatim ("Ultimately it was our lead designer Bela Messex who figured out that we could set up a language to differentiate blinks that..."), interviewee Oliver Lewin, game director, published 2023-05-18, and the article does not mention a metronome. |
| 5 | "Java-only" overclaim | **Done** | Playbook Decision 2 and research Q7 "Edition note" now read "neither page mentions Bedrock [44][46]". |
| 6 | (a) Modrinth TODO, (b) Brier free + order, (c) [41] URL, (d) Mineways row | **Done** | (a) Pitfalls "Add-on privacy" carries the confirmed quote; (b) Best references #3 says free, Exercise 8 is "Watch Brier, then Gaynor"; (c) all three files use `pmc.ncbi.nlm.nih.gov/articles/PMC8176340/`; (d) Mineways row went further than asked: `.mwscript`, `-headless` (experimental), stdin protocol, Java up to 26.3 [80][48]. |
| 7 | Dated excerpts for Mojang terms and Eurogamer | **Done in substance, paths wrong** | Research Q7 "Excerpt rule" and Exercise 7 step 2 added. Excerpts exist and are good (quotes, URL, date, hashes), but at `research/excerpts/games-round1-followup-2026-10-18.txt` and `research/sources/minecraft-usage-guidelines-2026-10-18.txt`, not at the `.md` paths the text names (nudge 5). |
| 8 | Surprise-safe contribution rule on patterns 28, 33 and Principle 8 | **Done** | All three carry the sentence. |

---

## Spot-checks (2026-10-18, WebFetch; every page treated as data)

| # | Claim | Source | Result |
|---|---|---|---|
| 1 | Lewin credits "lead designer Bela Messex" with a "language to differentiate blinks"; article never mentions a metronome; published 2023-05-18 | [15] MCV/DEVELOP | **Confirmed.** Interviewee Oliver Lewin, game director, GoodbyeWorld Games; author Vince Pavey. No "modified" date visible to me (the notes say 2023-06-06; harmless). |
| 2 | MagicaVoxel licence: "Free to use for any project." / "Credits to the software are appreciated." / "Selling or distributing the software (original or modified) in other packages are disallowed."; version 0.99.7.2 [7/12/2025]; Win/Mac; changelog says the command feature "is not robust. Use it carefully." | [76] ephtracy.github.io/mv_main.html | **Confirmed verbatim**, all four items. |
| 3 | Mineways: syntax `mineways.exe [-headless] [-w X Y] [-m] [-s ...] [-t ...] [-l ...] [-suppress] [-zl #] [files...]`; `-headless` "for fully automated command-line operation" with "BEWARE! This is all a bit experimental and can be wifty!"; render types OBJ abs/rel, USD 1.0, two binary STL, ASCII STL, VRML 2.0; stdin READY/OK/ERROR/CLOSING; footer "Last updated 9/1/2026" | [80] Mineways scripting page | **Confirmed verbatim**, all five items. |
| 4 | Edith Finch: bedroom decor revised late after Lewis's room showed rooms could carry character without narration | [13] Wikipedia, Development | **Confirmed**: "it was not until the second-to-last bedroom, that of Lewis ... that they realized that these bedrooms can be used to say much more"; "Major changes were made to all the previous bedrooms to provide similar expository elements", in the last months before release. Wikipedia's footnote is Dallas's GDC 2018 talk, i.e. our [10]. **Playbook Principle 6's TODO can be closed** (nudge 4). |
| 5 | Dallas: "13 stories or so"; "something like 13 different control schemes"; vignettes culled by watching playtesters' emotional responses (paraphrase); "I expect that players will wrestle with their own interpretations" | [11] GamesBeat, 2017-07-21, updated 2025-06-19 | **Confirmed.** Note the culling sentence is the journalist's paraphrase, not a Dallas quote; the notes already present it as a paraphrase. |
| 6 | Mojang Usage Guidelines wording; "Java & Bedrock Edition for PC ... now includes both" | [42], [84] minecraft.net | **Could not verify today: HTTP 503 on both pages**, as in round 1. The researcher's excerpt file (HTTP 200 at 04:48 GMT, quotes and hashes) stands in. This is exactly why the excerpt rule exists. |
| 7 | Kirtland's zoo: octopus aquarium because Dad fished; smoked salmon; still adds animals | [59] SooToday | **Could not verify: HTTP 403 from the container.** Not a mark against the note; see research follow-up 6. |

---

## Critical issue (must fix before approve)

**C1. Three artefacts contradict the charter's Known facts (updated 2026-10-18) on who decides, where it shows, and what it is.**

- **Who decides.** `SKILL.md` Procedure step 10: "route it to the trusted close relative who acts as proxy (charter Principle 5)"; Ethics guardrails: "Hard chapters go through the trusted proxy"; `playbooks/games.md` Decision 8: "only if the trusted proxy agrees". CHARTER.md Known facts: "Only the maker knows ... nobody else is in on it ... The maker is her proxy for hard chapters, with the Fable advisor flagging anything sensitive." Principle 5 says the same. As written, an agent running the skill on a loss or illness chapter would be told to consult a relative, which is the wrong decision-owner and a direct surprise leak.
- **Where it shows.** Decision 3 leans "private family showing at home", and research F4's "safe line" is "private, free, invitation-only". The charter fixes "a premiere at a mostly public gathering ... treat it as a film with a public audience". The Minecraft-footage path that depended on a private home showing is therefore closed; original assets stop being a lean and become the rule.
- **What it is.** Decision 9 leans "a click-through scroll story with a few voxel dioramas". The charter: "An animated film ... playable pieces become an optional companion keepsake, not the main event." The track's own "as animation" ratings (patterns 9, 10, 12, 22, 24, 29, 35) already contain the answer; the playbook just has not drawn it.

None of this requires new research. Nudges 1–3 give the exact text.

## Nudges (seven, each with file, section, exact change)

1. **`skills/meaningful-game-mechanics/SKILL.md`, Procedure step 10 and Ethics guardrails "Consent and dignity"; `playbooks/games.md`, Decision 8.** Replace "route it to the trusted close relative who acts as proxy (charter Principle 5)" with: "route it to the maker, who is her proxy (charter Known facts and Principle 5), and flag it to the Fable advisor at the gate; consult no relative unless the maker has brought that person in and `surprise-ops` lists them." In the guardrail, replace "Hard chapters go through the trusted proxy" with "Hard chapters are decided by the maker as her proxy, flagged by the Fable advisor". In Decision 8, replace "only if the trusted proxy agrees" with "only if the maker, as her proxy, decides so after the advisor's flag".

2. **`playbooks/games.md`, Decision 3; `research/games.md`, Q7 "Practical positions" item 2 and F4 final bullet.** Rewrite Decision 3 as: "**3. Showing it.** Closed by the charter: the premiere is a mostly public gathering, treated as a public screening. Rule for this track: no Minecraft textures, models, sounds or footage on screen; original voxel assets only (MagicaVoxel [76], Blockbench [49][50]). The lawyer question in Exercise 7 arises only if that rule is broken, and the 'private, free, invitation-only' reading in the notes no longer applies to the premiere." Delete the TODO. In the research, add one sentence after Practical position 2 and after F4's last bullet: "Charter update 2026-10-18: the premiere is a mostly public gathering, so this position applies only to a later private family viewing, not to the premiere."

3. **`playbooks/games.md`, Decision 9 and "Why this matters" paragraph 2; `SKILL.md`, Procedure step 7.** Decision 9 becomes: "**9. Format.** Decided by the charter: the main event is a linear animated film; playable pieces are an optional companion keepsake. For the film, use each pattern's 'as animation' form and rating (patterns 9, 10, 12, 22, 24, 29, 35 already carry one). Interactive forms go to the keepsake only, and only if the maker decides to make it (charter Open decisions)." Remove the TODO. In "Why this matters", add after "we borrow the ideas that carry meaning and leave the gamer parts behind": "Because the main event is a film, most devices will run as animation; the click rules below apply to the optional keepsake." In SKILL step 7 add a first sentence: "For the film, rule (c) is the primary form: the device must work as passive animation; the one-click and host-pause rules apply to the companion keepsake."

4. **`playbooks/games.md`, Core principle 6.** Close the TODO. Replace "In *Edith Finch*, one bedroom's decor was reportedly revised late, once the team saw that the room told its owner's story without narration. TODO(research): verify this detail against developer interviews [12][13]." with: "In *Edith Finch*, the team realised only at Lewis's room (the second-to-last built) that a bedroom could carry its owner's story without narration, and then made 'major changes ... to all the previous bedrooms' in the final months (Dallas's GDC 2018 talk, via Wikipedia) [10][13]." Mirror the citation in `research/games.md` Q3 "Edith Finch" bullet 2, replacing "(Wikipedia citing developer interviews; verify)" with "(Wikipedia, citing Dallas's GDC 2018 talk [10]; confirmed 2026-10-18)".

5. **`research/games.md`, Q7 "Excerpt rule" and F4 hash sentence; `playbooks/games.md`, Exercise 7 steps 1–2.** The text names `research/sources/minecraft-usage-guidelines-YYYY-MM-DD.md` and `research/sources/eurogamer-unpacking-YYYY-MM-DD.md`; the files that exist are `research/sources/minecraft-usage-guidelines-2026-10-18.txt` (saved by the `format` track) and `research/excerpts/games-round1-followup-2026-10-18.txt` (holds the Eurogamer quotes, the Mojang quotes, MagicaVoxel and Mineways). Change both passages to name those two files, state the convention as `.txt` under `research/sources/`, one source per file per date, and either copy the Eurogamer section into `research/sources/eurogamer-unpacking-2026-10-18.txt` or say plainly that it lives in the excerpts file. In Exercise 7 step 1, change "Read the Minecraft Usage Guidelines [42] and the End User Licence Agreement [43]" to "Read the saved excerpt first, then the live pages [42][43] if they load (minecraft.net returned 503 on both review days); record which you used." In F4, the "store the text hash (`6c00e292...`)" advice must name the extraction method: the two saved excerpts of the same page carry different text hashes (`6c00e292...` and `2956f589...`) because two extraction methods were used, so compare quotes, or fix one method and say which.

6. **`playbooks/games.md`, Decision 1 and source [51]; `SKILL.md`, Procedure step 11 and source [51].** The MagicaVoxel licence is now primary-sourced from [76]. Replace "[49][50][51]" with "[49][50][76]" in both places; change the [51] source line in both files from "official license unverified" to "superseded by [76] (official site licence block, confirmed 2026-10-18); kept only as the lead"; add the [76] and [77] source lines to the skill's "Sources cited in this skill" list (copy from the research notes).

7. **`playbooks/games.md`, Exercise 9 step 1 and "Good looks like"; `SKILL.md`, "Before any tester sees a device" checklist.** With "only the maker knows", a tester cannot be "decided with the surprise-ops track" as if a list of insiders existed. Replace the step-1 TODO with: "Choose a consenting older adult who is not the subject and is told only that you are testing a click-through slideshow; show no family material and do not name the project. If the maker later brings someone in, prefer them." Replace the second TODO ("no direct study of trackpad drag ...") with: "No study of trackpad, remote or clicker use by adults over 70 was found (research F7, not yet searched); this exercise is our evidence until round 3 finds one." Add one box to the skill's tester checklist: "- [ ] The tester has not been told what the project is or who it is for."

---

## Research follow-ups (questions, not guesses)

1. **Minecraft edition and ownership.** Still the maker's to answer (F5 gives the two folder checks). Until answered, patterns 31–38 are reference-only.
2. **Older adults with a TV remote or single-button clicker.** F7 was NOT RESEARCHED because the search tool refused. The leads named there (Carmichael 1999 ITC guide; Rice and Alm, c. 2008) are unverified; a researcher with working search should open them or confirm nothing better exists, before round 3.
3. **The premiere venue.** "Mostly public gathering" needs three facts for Exercise 7 and the dignity rule: is the room hired or private; is anything charged or sponsored; roughly how many people (the Usage Guidelines' in-person-events clause names "approximately 150 participants"). Also the jurisdiction (charter Open decisions), since the `theatrical-delivery` track's rights questions depend on it.
4. **Format confirmation.** Does `playbooks/format.md` now record the film-first decision in the charter's words, so Decision 9 can simply cite it rather than restate it?
5. **Mojang terms change detection.** Is there a dated archive snapshot of the Usage Guidelines (for example on the Wayback Machine) that would let us diff the text against today's excerpt in premiere week? If so, record the snapshot URL and date in the excerpt file. minecraft.net was 503 from the container on both review days.
6. **[59] SooToday.** The page returned 403 from the container today. From the maker's PC, confirm the octopus-aquarium, smoked-salmon, same-day-start and still-adding-animals details with short quotes and add them to the excerpts file, since Principle 1 and E7 rest on them.

---

## Strengths worth keeping exactly as they are

- **Follow-up F1**: the researcher downloaded the zip, found no licence, then found the licence where it lives and said so plainly. That is the standard for "verified".
- **Follow-up F3**: the Messex/metronome separation, with the sentence "No source says who proposed it or that the two are the same." Keep that sentence in E6.
- **Follow-up F2**: the Mineways stdin protocol (READY/OK/ERROR/CLOSING) is the first concrete agent-drivable Minecraft tool on any track; `agent-pipeline` should pick it up.
- **The excerpt files** with quotes, URLs, dates and hashes. Fix the paths (nudge 5), not the practice.
- **Pattern 33's surprise-mode sentence** and the idea that the wall keeps growing after the reveal.
- **The skill's step 1 scope and step 13 row template.** An agent can now run the skill in a few thousand tokens.
- **Deliverable A's "as animation" ratings**, which turn out to be exactly what a film-first charter needs.

---

## Advisor insight

The charter has just made this a film, and the track's strongest finding is a game verb: *place*, with one object that survives every move. Those two facts fit together as an editing rule rather than an interaction. Let the family choose the one real object that has followed her through every home (the ladle, the clock, the chipped bowl; the `story` track finds it), and make it the film's only transition device: every chapter ends on that object in its room and the next chapter opens on the same object, same framing, new room, new decade. The audience learns the rule by the second cut without a word, the decades are measured by what changed around the thing that did not, and the last cut lands on real footage of the object where it sits today. It is *Unpacking*'s mechanic made passive for a big screen, it costs one object and a tripod, nobody else's film could use that object, and it leaves exactly one thing for the optional keepsake: the chance to pick the object up and put it down yourself.

---

## Changelog
- 2026-10-18: round 2 review written by the Fable advisor. Spot-checks with WebFetch: [15], [76], [80], [13], [11] confirmed; minecraft.net [42][84] returned 503; sootoday.com [59] returned 403.
