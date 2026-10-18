---
name: meaningful-game-mechanics
description: Designs, reviews or cuts game-like mechanics, maps, timelines, inventories, reveals and pacing devices for the Life Journey, so each one expresses something true about the subject's life with no points, fail states or precision gestures. Use it whenever a chapter needs an interactive or animated device, when someone proposes achievements, scores, timers, drag gestures or Minecraft assets, or when a device must pass the swap-the-subject test and the ethics checks.
---

# Meaningful Game Mechanics

## Purpose

Make sure every interactive or animated device in the Life Journey passes charter Principle 2: mechanics must mean something. This skill turns the research notes into a repeatable check. Write the device as one sentence, run the swap test, score it, apply the input and ethics rules, then log the decision. The human-readable version is `playbooks/games.md`.

## When to use

- Choosing or designing a device for a chapter: reveal, map, inventory, conversation, routine, pacing, voxel scene.
- Reviewing a device someone else proposed.
- Someone asks for achievements, points, badges, levels, progress bars, timers, a fail state, drag gestures or a Minecraft asset.
- Before any device is shown to a tester.

## When not to use

- Gathering or writing story facts. That belongs to the `story` track. Do not invent facts to fill a device.
- Choosing the engine, delivery format or screening plan. That belongs to the `format` track. Hand off.
- Restoring or animating real photos. That belongs to the `ai-imagery` track.
- Tool installs and licence reading beyond the checklists here. Mark TODO(research) and hand off to `toolchain`.
- Legal questions about Minecraft or venues. Flag them for the maker and a lawyer. Do not answer them as legal advice.
- Writing code. The project is in the LEARN phase, so this skill makes design decisions only. Later phases still run these checks before any build.

## Procedure

1. Read `CHARTER.md`, `playbooks/games.md` and `research/games.md`. Confirm that the chapter's story facts exist in the story track. If a fact is unconfirmed, write `TODO(story): <fact>` and do not design around it.
2. Write the device as one sentence: "In this chapter the viewer [does X], which means [Y] about her life." If you cannot finish the sentence, the device is decoration. Cut it, or return to step 1 for a new idea. Strong examples: a trophies-aside reveal [30] and a conversation puzzle that eases with comfort [5][6].
3. List the subject facts the device uses. Each needs a specific object, room, place, saying or event, plus its source and whether the family has confirmed it. Keep these in an object ledger, as the *Unpacking* team did [3].
4. Run the swap test. Replace her facts with another family's facts in your head. If the device still works unchanged, it fails Principle 2. Redesign it.
5. Match the device to a pattern in the notes' pattern library (patterns 1 to 39, in "Deliverable A" of `research/games.md`). Record the pattern number, or write "new" and describe it in one line.
6. Score the device (these are judgment calls, not research findings): access 1 to 5, gimmick risk L, M or H, build effort S, M or L. Use the scales in the checklist below. Anything in the vertical slice needs access 4 or 5.
7. Apply the input rules. Accept only: one click or tap; a visible next step; auto-advance or passive animation that still works if nobody touches it; a host pause. Reject drag, swipe, double-tap, long-press, rhythm taps, eye-blinks, webcam tracking, analog sticks and timed reactions. Convert each rejected input to one of the accepted ones. Basis: [39][40][41]. The pause chime comes from *Before Your Eyes* [14].
8. Apply the anti-game rules. Remove points, XP, badges, achievements, levels, leaderboards, progress bars, completion percentages, game-over states and any timer tied to a viewer's action. Basis: [23][37][38] for points, [26] for fail states. Remove stock vocabulary: circle-of-life day and night, generic biomes, treasure chests, hearts and hunger bars, enemies standing in for illness or money.
9. Apply the truth rules. Reconstructed scenes use a different medium from documents and carry a visible label. Nothing is invented: no events, people, quotes or objects without a source or the family's confirmation. Basis: [11][13].
10. Apply the dignity rule. If the chapter covers loss, illness, separation, money or conflict, mark it "needs proxy decision" and route it to the trusted close relative who acts as proxy (charter Principle 5). The default is to leave it out of the shared version. A locked chapter can follow the Minecraft Vault pattern: it opens once and only with its own key [55].
11. Apply the IP rule. If any Minecraft asset appears (textures, models, sounds, footage), mark it "terms check needed." The default is to swap it for original voxel or vector assets. Tools: [49][50][51].
12. Check the voice. A device must not put words in her mouth. Any speech comes from her real recorded words or from text with a real source.
13. Record the decision in the chapter's design log: device name, one-sentence device, subject facts, pattern number, scores, decision (keep, redesign or cut), open questions. TODO(research): choose the log's file location with the orchestrator.
14. Hand off. Delivery goes to the `format` track, tools to `toolchain`, photos to `ai-imagery`. Send the rubric scores to the Fable advisor gate.

## Checklists

**Device approval (every box must be ticked):**
- [ ] A one-sentence device exists and names a real fact.
- [ ] It passes the swap-the-subject test.
- [ ] No points, badges, levels, progress bars, timers or fail states.
- [ ] Works with one click, or with no input at all.
- [ ] Shows a next step; auto-advances or waits for a click; the host can pause.
- [ ] Reconstructions are labelled; nothing is invented.
- [ ] A hard chapter has a proxy decision, or is left out.
- [ ] No Minecraft asset, or the terms check is recorded.
- [ ] For the slice: access 4 or 5, gimmick risk L or M, build effort S or M.

**Scales (judgment):**
- Access: 5 fine as is; 4 fine with click-to-act or auto-advance; 3 redesign needed; 2 convert to passive animation; 1 drop.
- Gimmick risk: L, M or H, the chance the device reads as decoration or a borrowed trend.
- Build effort: S about a day with AI help; M 2 to 5 days; L 1 to 3 weeks. These are rough guesses, with no engine assumed.

**Before any tester sees a device:**
- [ ] The tester is someone the maker has agreed to involve.
- [ ] Nothing on screen reveals the subject's identity or the project's name.
- [ ] The test runs on a machine the subject does not use.
- [ ] Screenshots and recordings do not sync to a cloud photo library.
- [ ] Questions ask how it felt, not whether it was understood.
- [ ] No test is run with the subject herself.

**Before any public or large-screen showing:**
- [ ] Minecraft terms re-read on the day of the showing, with the date recorded.
- [ ] No Mojang logo, and no claim of official status. A disclaimer is used.
- [ ] Original assets are used unless the terms check passes for that use.
- [ ] A lawyer has answered the question for any hired venue.

## Quality bar

A good device:
- Turns one verb into a specific real object or place. A viewer can say what it means without a caption.
- Works on an untouched screen and for a host.
- Could not work unchanged for another family.
- Reads at thumbnail size, with few colours and a clear silhouette. See [64][65].

A mediocre device:
- Is "a nice animation" with no sentence behind it.
- Has a points bar or a badge, however small.
- Uses generic icons, default textures, or a famous game's look with new stickers.
- Is timed, so a slow reader fails.
- Holds a reveal that the viewer cannot discover without words.

Approval rule (charter): the advisor gate approves only when every rubric score is 4 or higher and nothing critical is open. The rubric is meaning, specificity, accuracy, feasibility, ethics and usability.

## Ethics guardrails

- **Consent and dignity.** Hard chapters go through the trusted proxy, and the default is to leave them out (charter Principle 5). Whether to release a story at all is a real question. The *That Dragon, Cancer* developer asked it of himself and faced critics over it [17][18].
- **No invented facts.** Reconstructions are visibly reconstructions. Unreliable or disputed accounts are shown as such [11][13].
- **No words in her mouth.** No invented quotes (charter Principle 4).
- **No elegy by default.** She is alive. Take devices from death-forward games such as *Passage* and *Spiritfarer* [23][27], not their register [41].
- **Surprise.** Devices, cloud sync and group chats must not give the surprise away.
- **Minecraft terms.** Permissions can be revoked at any time. Mojang's wording treats sharing with the community as commercial. Selling copies is not allowed, and endorsement must not be implied [42][43].
- **Add-on privacy.** Read the settings of add-ons before installing. The Flashback Settings add-on has telemetry on by default [47].
- **Second-hand stories.** Do not repeat unverified memorial stories as fact [57][58].

## References

- Playbook (human-readable version): `playbooks/games.md`
- Research notes (pattern library, anti-patterns, sources): `research/games.md`
- Charter (principles, rubric, constraints): `CHARTER.md`
- Start reading: [1], [3], [5], [30]. Watch next (not yet watched): Brier's 2023 talk [2], Dallas's 2018 talk [10], and Gaynor's 2014 talk [36].

**Sources cited in this skill** (copied from `research/games.md`; tier tags as in the notes):

[1] Danielle Riendeau — "'Unpacking' the design pillars of a chill puzzle game" — https://www.gamedeveloper.com/design/unpacking-the-design-pillars-of-a-chill-puzzle-game — 2023-04-21 — [S] summary of Wren Brier's GDC 2023 talk.
[2] GDC Vault — "'Unpacking' Zen: Designing a Game Without Fail States or Scores" (Wren Brier, GDC 2023) — https://www.gdcvault.com/play/1029400/-Unpacking-Zen-Designing-a — 2023 — [P] listing seen via search; video not viewed.
[3] Eurogamer — "The creators of Unpacking on developing a 'weird', queer, BAFTA-winning game" — https://www.eurogamer.net/the-creators-of-unpacking-on-developing-a-weird-queer-bafta-winning-game — April 2022 — [S] Brier and Dawson; read in full.
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
[41] Lee S, Oh H, Shi C-K, Doh YY — "Mobile Game Design Guide to Improve Gaming Experience for the Middle-Aged and Older Adult Population", JMIR Serious Games 2021;9(2):e24449 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8176340/ (text retrieved via NCBI E-utilities) — 2021 — [P] 40 participants, mean age 66.75.
[42] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18; no visible date — [P].
[43] Mojang/Microsoft — Minecraft End User License Agreement — https://www.minecraft.net/en-us/eula — fetched 2026-10-18 — [P].
[47] Modrinth — Flashback Settings — https://modrinth.com/project/mOIDKWOa — fetched 2026-10-18 — [P] note: add-on; PolyForm Noncommercial; telemetry on by default.
[49] Blockbench — https://blockbench.net/ — fetched 2026-10-18 — [P].
[50] Blockbench README — https://cdn.jsdelivr.net/gh/jannisx11/blockbench@master/README.md — fetched 2026-10-18 — [P] GPL-3.0; assets are yours.
[51] VoxelFans — MagicaVoxel page (third-party) — https://voxelfanscom.nuxt.dev/magicaVoxel — fetched 2026-10-18 — [T] "free for personal and commercial use"; official license unverified.
[55] Minecraft Wiki — Vault — https://minecraft.wiki/w/Vault — fetched 2026-10-18.
[57] Salon (from The Daily Dot) — "Gamer uses 'Minecraft' to pay tribute to his wife" — https://salon.com/2014/03/13/gamer_uses_minecraft_to_pay_tribute_to_his_wife_partner — 2014-03-13 — [S] second-hand; original not found.
[58] Everplans — Adam Seifer, "Minecraft video game memorial honors loved one" — https://everplans.com/articles/minecraft-video-game-memorial-honors-loved-one — undated — [S] cites a Reddit post (not found).
[64] Game Developer — Zach Soares, "Voxel Art: Reducing the Greebles" — https://www.gamedeveloper.com/design/voxel-art-reducing-the-greebles — 2017-06-05.
[65] 80.lv — Gabriel de Laubier, "Using Voxels for Simple Dioramas" — https://80.lv/articles/using-voxels-for-simple-dioramas — 2017-07-26.
