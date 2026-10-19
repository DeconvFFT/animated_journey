---
name: meaningful-game-mechanics
description: Designs, reviews or cuts game-like mechanics, maps, timelines, inventories, reveals and pacing devices for the Life Journey, so each one expresses something true about the subject's life with no points, fail states or precision gestures. Use it whenever a chapter needs an interactive or animated device, when someone proposes achievements, scores, timers, drag gestures or a game's look or assets, or when a device must pass the swap-the-subject test and the ethics checks.
---

# Meaningful Game Mechanics

**Reconciled with `DECISIONS.md` (2026-10-19, after the her-world merge); the register wins.** Decided there: the game-world look is dropped (D-29, which replaces D-23); the look comes from her own Hindu world (D-28, D-31, W-72), and nothing from any game's textures, sounds, UI, footage or name is used. This skill keeps only what games taught about meaning: the swap-the-subject test, one verb per device, the object ledger and the input and ethics rules. Playable pieces are an optional companion (W-30); the default companion is the film itself, PH1 on her phone by cable (W-73, TD-9). The maker is the only person on the project and the sole proxy for hard chapters, who decides under one-key-three-guards (D-03, D-04). O-05 is answered: the game was only an example.

## Purpose

Make sure every interactive or animated device in the Life Journey passes charter Principle 2: mechanics must mean something. This skill turns the research notes into a repeatable check. Write the device as one sentence, run the swap test, score it, apply the input and ethics rules, then log the decision. The human-readable version is `playbooks/games.md`.

## When to use

- Choosing or designing a device for a chapter: reveal, map, inventory, conversation, routine, pacing, built set (the kitchen, W-34).
- Reviewing a device someone else proposed.
- Someone asks for achievements, points, badges, levels, progress bars, timers, a fail state, drag gestures or a game's look or assets.
- Before any device is shown to a tester.

## When not to use

- Gathering or writing story facts. That belongs to the `story` track. Do not invent facts to fill a device.
- Choosing the engine, delivery format or screening plan. That belongs to the `format` track. Hand off.
- Restoring or animating real photos. That belongs to the `ai-imagery` track.
- Tool installs and licence reading beyond the checklists here. Mark TODO(research) and hand off to `toolchain`.
- Legal questions about rights, venues or showing. Flag them for the maker and the rights consult (W-55, TD-8). Do not answer them as legal advice.
- Writing code. The project is in the LEARN phase, so this skill makes design decisions only. Later phases still run these checks before any build.

## Procedure

1. Read the eight Core principles in `playbooks/games.md` and the Deliverable A pattern tables and Deliverable B anti-pattern list in `research/games.md` (lines 38–118). Open the rest of the notes only to match a pattern number or copy a citation. Confirm that the chapter's story facts exist in the story track. If a fact is unconfirmed, write `TODO(story): <fact>` and do not design around it.
2. Write the device as one sentence: "In this chapter the viewer [does X], which means [Y] about her life." If you cannot finish the sentence, the device is decoration. Cut it, or return to step 1 for a new idea. Strong examples: a trophies-aside reveal [30] and a conversation puzzle that eases with comfort [5][6].
3. List the subject facts the device uses. Each needs a specific object, room, place, saying or event, plus its source and whether the family has confirmed it. Keep these in an object ledger, as the *Unpacking* team did [3].
4. Run the swap test. Replace her facts with another family's facts in your head. If the device still works unchanged, it fails Principle 2. Redesign it.
5. Match the device to a pattern in the notes' pattern library (patterns 1 to 39, in "Deliverable A" of `research/games.md`). Record the pattern number, or write "new" and describe it in one line.
6. Score the device (these are judgment calls, not research findings): access 1 to 5, gimmick risk L, M or H, build effort S, M or L. Use the scales in the checklist below. Anything in the vertical slice needs access 4 or 5.
7. For the film, rule (c) is the primary form: the device must work as passive animation; the one-click and host-pause rules apply to a playable companion, which exists only under W-30's conditions (the default companion is PH1 by cable, W-73). Apply the input rules. Accept only: one click or tap; a visible next step; auto-advance or passive animation that still works if nobody touches it; a host pause. Reject drag, swipe, double-tap, long-press, rhythm taps, eye-blinks, webcam tracking, analog sticks and timed reactions. Convert each rejected input to one of the accepted ones. Basis: [39][40][41]. The pause chime comes from *Before Your Eyes* [14].
8. Apply the anti-game rules. Remove points, XP, badges, achievements, levels, leaderboards, progress bars, completion percentages, game-over states and any timer tied to a viewer's action. Basis: [23][37][38] for points, [26] for fail states. Remove stock vocabulary: circle-of-life day and night, generic biomes, treasure chests, hearts and hunger bars, enemies standing in for illness or money, and the Hindu-world tells of the style bible (generic India, generic Gujarat, colonial-Christian and deity-misuse tells: W-38 decision 10, W-66).
9. Apply the truth rules. Reconstructed scenes use a different medium from documents and carry a visible label. Nothing is invented: no events, people, quotes or objects without a source or the family's confirmation. Basis: [11][13].
10. Apply the dignity rule. If the chapter covers loss, illness, separation, money or conflict, mark it "needs proxy decision" and route it to the maker, who is her proxy (charter Known facts and Principle 5; D-03), under one-key-three-guards (D-04): a decision sheet, Fable's written flag (Fable flags and never passes G5), and the maker's two decisions 72 hours apart; consult no relative. The default is OUT of the public cut. A locked chapter follows W-37: three visibly unfinished places drawn as closed doors in her house's line with the held card, never the home mandir's doors (those are shown once, in the shrine moment, W-61; PR15), and an open chapter card.
11. Apply the rights and deity rule (D-29, W-46, W-61). No texture, model, sound, UI or footage from any game appears in the public cut; every asset is the maker's own, hand-drawn or hand-traced from a logged source, with a rights-log row and a `motif_check` value (W-66). A device never draws, generates, photographs, lifts aside, opens, dresses or reveals a deity or a seva article; anything that stands for a deity carries `deity_form` and `deity_source`, and no generative route touches it (W-61, W-70, PR10). If an outside asset appears anyway, mark it "rights check needed" and swap it for a hand-drawn or hand-traced one.
12. Check the voice. A device must not put words in her mouth. Any speech comes from her real recorded words or from text with a real source. No synthetic, cloned or text-to-speech voice of any real person, living or dead, even with consent (charter review §1.2). Where she cannot be recorded, real words for surprise mode are her HER-PUBLIC clip if it passes one-key-three-guards (HER-PRIVATE voice notes never enter the public cut; D-05, W-45); her own letters and cards; or a saying that two relatives independently confirm, shown as attributed text with no voice ("as her sister remembers it"), never as a quotation in her voice.
13. Record the decision. Append one row to `design/devices-log.md` (create it if absent) with columns: date | chapter | device sentence | subject facts + confirmed by | pattern # | A/G/B | decision | open questions. A/G/B are the access, gimmick risk and build effort scores from step 6. The orchestrator may move the file; update this path if so.
14. Hand off. Delivery goes to the `format` track, tools to `toolchain`, photos to `ai-imagery`. Send the rubric scores to the Fable advisor gate.

## Checklists

**Device approval (every box must be ticked):**
- [ ] A one-sentence device exists and names a real fact.
- [ ] It passes the swap-the-subject test.
- [ ] No points, badges, levels, progress bars, timers or fail states.
- [ ] Works with one click, or with no input at all.
- [ ] Shows a next step; auto-advances or waits for a click; the host can pause.
- [ ] Reconstructions are labelled; nothing is invented.
- [ ] A hard chapter has a one-key-three-guards decision (sheet, Fable's flag, two maker decisions 72 hours apart), or is left out.
- [ ] No outside game asset; every asset has a rights-log row and a `motif_check` value (W-46, W-66).
- [ ] No device lifts aside, opens, dresses or reveals a deity or a seva article; the home mandir's doors are shown closed, once (W-61).
- [ ] For the slice: access 4 or 5, gimmick risk L or M, build effort S or M.

**Scales (judgment):**
- Access: 5 fine as is; 4 fine with click-to-act or auto-advance; 3 redesign needed; 2 convert to passive animation; 1 drop.
- Gimmick risk: L, M or H, the chance the device reads as decoration or a borrowed trend.
- Build effort: S about a day with AI help; M 2 to 5 days; L 1 to 3 weeks. These are rough guesses, with no engine assumed.

**Before any tester sees a device:**
- [ ] The tester is a stranger to her who is told nothing about the project and sees no family material (only-me, D-03; W-43).
- [ ] Nothing on screen reveals the subject's identity or the project's name.
- [ ] The test runs on a machine the subject does not use.
- [ ] Screenshots and recordings do not sync to a cloud photo library.
- [ ] Questions ask how it felt, not whether it was understood.
- [ ] No test is run with the subject herself.
- [ ] The tester has not been told what the project is or who it is for.

**Before any public or large-screen showing:**
- [ ] Every asset on screen has a green rights-log row (W-46); no outside brand, logo or interface appears.
- [ ] Every line meets the phone floor (4 px meaning lines at 1080p, W-38 decision 3).
- [ ] Any rights question for the hired venue went to the consult (W-55, TD-8), not to this skill.

## Quality bar

A good device:
- Turns one verb into a specific real object or place. A viewer can say what it means without a caption.
- Works on an untouched screen and for a host.
- Could not work unchanged for another family.
- Reads at thumbnail size and at the phone floor, with few colours and a clear silhouette (4 px meaning lines, W-38 decision 3).

A mediocre device:
- Is "a nice animation" with no sentence behind it.
- Has a points bar or a badge, however small.
- Uses generic icons, default textures, or a famous game's look with new stickers.
- Is timed, so a slow reader fails.
- Holds a reveal that the viewer cannot discover without words.

Approval rule (charter): the advisor gate approves only when every rubric score is 4 or higher and nothing critical is open. The rubric is meaning, specificity, accuracy, feasibility, ethics and usability.

## Ethics guardrails

- **Consent and dignity.** Hard chapters are decided by the maker as her proxy under one-key-three-guards (D-04), flagged by the Fable advisor, and the default is to leave them out of the public cut (charter Principle 5). Whether to release a story at all is a real question. The *That Dragon, Cancer* developer asked it of himself and faced critics over it [17][18].
- **No invented facts.** Reconstructions are visibly reconstructions. Unreliable or disputed accounts are shown as such [11][13].
- **No words in her mouth.** No invented quotes (charter Principle 4). No synthetic, cloned or text-to-speech voice of any real person, living or dead, even with consent (charter review §1.2). Where she cannot be recorded, real words for surprise mode are her HER-PUBLIC clip if it passes one-key-three-guards (HER-PRIVATE voice notes never enter the public cut; D-05, W-45); her own letters and cards; or a saying that two relatives independently confirm, shown as attributed text with no voice ("as her sister remembers it"), never as a quotation in her voice.
- **No elegy by default.** She is alive. Take devices from death-forward games such as *Passage* and *Spiritfarer* [23][27], not their register [41].
- **Surprise.** Devices, cloud sync and group chats must not give the surprise away.
- **Rights.** Every asset is the maker's own or cleared (W-46); nothing from a game's owner is used or implied (D-29).
- **Add-on privacy.** Read the settings of any add-on before installing it on a computer that holds family material; telemetry can be on by default (D-15, W-26).
- **Second-hand stories.** Do not repeat unverified memorial stories as fact.
- **The seva space.** A device never handles, reveals or dresses anything of her seva or any deity (W-61, W-70, PR10); the "trophies aside" move is for trophies and photographs only.

## References

- Playbook (human-readable version): `playbooks/games.md`
- Research notes (pattern library, anti-patterns, sources): `research/games.md`
- Charter (principles, rubric, constraints): `CHARTER.md`
- Start reading: [1], [3], [5], [30]. Watch next (not yet watched): Brier's 2023 talk [2], Dallas's 2018 talk [10], and Gaynor's 2014 talk [36].

**Sources cited in this skill** (copied from `research/games.md`; tier tags as in the notes; numbers missing here belong to the game-world look dropped under D-29 and stay in the research note as a historical record):

[1] Danielle Riendeau — "'Unpacking' the design pillars of a chill puzzle game" — https://www.gamedeveloper.com/design/unpacking-the-design-pillars-of-a-chill-puzzle-game — 2023-04-21 — [S] summary of Wren Brier's GDC 2023 talk.
[2] GDC Vault — "'Unpacking' Zen: Designing a Game Without Fail States or Scores" (Wren Brier, GDC 2023) — https://www.gdcvault.com/play/1029400/-Unpacking-Zen-Designing-a — 2023 — [P] listing seen via search; tagged "free content" on the listing; video not viewed.
[3] Eurogamer — "The creators of Unpacking on developing a 'weird', queer, BAFTA-winning game" — https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game — 2022-04-12, Ed Nightingale — [S] Brier and Dawson; read in full.
[5] Player.One — Ken Wong interview, "Florence Tells A Love Story With Actions, Not Words" — https://www.player.one/florence-game-ken-wong-interview-123975 — 2018-02-12 — [S] puzzle easing, "interactions".
[6] Milanote / Ollie Campbell — "The Lead Designer of Monument Valley Deconstructs His Latest Game, Florence" — https://milanote.com/the-work/lead-designer-of-monument-valley-deconstructs-his-latest-game-florence — undated (post-2018) — [S] mechanics, cut chapters.
[10] GDC Vault — "Weaving 13 Prototypes into 1 Game: Lessons from 'Edith Finch'" (Ian Dallas, GDC 2018) — https://gdcvault.com/play/1025016/Weaving-13-Prototypes-into-1 — 2018 — [P] listing only.
[11] GamesBeat — "The story behind the haunting What Remains of Edith Finch" — https://gamesbeat.com/the-story-behind-the-haunting-what-remains-of-edith-finch/ — 2017-07-21 (updated 2025-06-19) — [S] Dallas quotes.
[13] Wikipedia — "What Remains of Edith Finch" — https://en.wikipedia.org/wiki/What_Remains_of_Edith_Finch — fetched 2026-10-18 — [T] development notes, decor revision, reception.
[14] Game Developer — Sam Machkovech, "A seven-year blink of an eye: Before Your Eyes' woes deconstructed at GDC" — https://www.gamedeveloper.com/marketing/a-seven-year-blink-of-an-eye-before-your-eyes-s-dev-woes-deconstructed — 2023-03-22 — [S] Graham Parkes's GDC 2023 talk.
[17] Game Developer — Christian Nutt, "Game as memorial: That Dragon, Cancer developer reflects" — https://gamedeveloper.com/design/game-as-memorial-i-that-dragon-cancer-i-developer-reflects — 2014-11-12 — [S].
[18] The Spinoff — Tof Eklund, "'Death is the thing we all share'" — https://thespinoff.co.nz/pop-culture/02-06-2017/death-is-the-thing-we-all-share-why-one-father-made-a-video-game-about-his-sons-cancer-battle — 2017-06-02 — [S] Ryan Green.
[23] Jason Rohrer — Passage statement — https://hcsoftware.sourceforge.net/passage/statement.html — undated (c. 2007) — [P].
[26] Wikipedia — "Gris" — https://en.wikipedia.org/wiki/Gris — fetched 2026-10-18 — [T] no fail state, grief, accessibility.
[27] Pocket Tactics — "Love, Death, and Margot Tenenbaum — the many inspirations of Spiritfarer" — https://www.pockettactics.com/spiritfarer/interview — updated 2021-08-13 — [S] Nicolas Guérin.
[30] Inverse — Jess Reyes, "What happened with Miriam and her mom at the end of A Memoir Blue?" — https://www.inverse.com/gaming/memoir-blue-ending-explained — 2022-04-06 (updated 2024-02-20) — [S] trophies-to-photographs ending.
[36] Game Developer — "Video: Why is Gone Home a game?" — https://www.gamedeveloper.com/design/video-why-is-i-gone-home-i-a-game- — 2014-05-26 — [P] Steve Gaynor GDC 2014; free video on GDC Vault.
[37] Kotaku (republished with permission) — Margaret Robertson, "Can't Play, Won't Play" — https://kotaku.com/cant-play-wont-play-5686393 — 2010-11-10 — [P] pointsification.
[38] Ian Bogost — "Gamification is Bullshit" — https://www.bogost.com/blog/gamification_is_bullshit/ — 2011 — [P].
[39] Game Accessibility Guidelines — full list — https://gameaccessibilityguidelines.com/full-list/ — fetched 2026-10-18 — community checklist.
[40] Game Accessibility Guidelines — "Allow players to progress through text prompts at their own pace" — https://gameaccessibilityguidelines.com/allow-players-to-progress-through-text-prompts-at-their-own-pace — fetched 2026-10-18.
[41] Lee S, Oh H, Shi C-K, Doh YY — "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8176340/ (text retrieved via NCBI E-utilities) — 2021 — [P] 40 participants, mean age 66.75.

## Changelog

- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18). Original voxel assets only and the IP rule per D-23; hard chapters per one-key-three-guards (D-04); testers are strangers to her with no family material (D-03, W-43); found-voice wording per D-05 and W-45; the Minecraft chapter waits on O-05 and W-30.
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19). The Minecraft and voxel clauses are retired under D-29 (S-45, S-50): the look comes from D-28 and W-72; the IP step became the rights and deity rule (W-46, W-61); the locked-chapter pattern follows W-37; the terms, tool and add-on sources removed; the companion is PH1 by cable (W-73).
