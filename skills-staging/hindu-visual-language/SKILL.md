---
name: hindu-visual-language
description: Briefs, sources and checks the Hindu visual idiom for the Life Journey film (floor art, temple architecture, deity iconography, shadow-puppet and scroll structure) under the Hindu-only rule, the deity respect rules, the 4 px phone line floor and the rights routes. Use when a card, title, set, frame device, motif, transition, symbol or deity image is drawn, briefed, sourced or reviewed, or when a motif's origin, a deity image's source or a phone line is in doubt. Do not use it for rites, festivals, shlokas, rasa or objects (use hindu-life-story-frameworks), for fonts, Indic script shaping, sound, grading or captions, or for AI photo restoration of real people.
---

# Hindu visual language

Staged for review at `skills-staging/hindu-visual-language/`. It is not yet in `.claude/skills/`. Moving it needs the orchestrator's decision and the Fable advisor's review (CLAUDE.md). Reconciled with [DECISIONS.md](../../DECISIONS.md) after the her-world merge (2026-10-19). Where this skill disagrees with a row in it, the register wins. D-rows are decided by the maker. W-rows and O-rows are working defaults or open questions. Style-bible decision 11 is `11_hindu_idiom` and decision 12 is moving footage (W-38, W-59).

## Purpose

Make every Hindu visual in the film hers, correct, respectful, legible on a phone and cleared for public screening. Turn the maker's household answers (held offline) into briefs, sheets, checklists and a `hindu_idiom` block. Refuse anything that cannot be sourced, dated or attributed. The film's world is Hindu: Sanatan Dharma and its sanskriti (D-28). "Indian" always means Hindu. No Mughal, Islamic or Christian motif. A shared or ambiguous origin defaults out. The playful, crafted feel comes from this Hindu design world, and D-29 retired the earlier game-world rule (D-23). For her the floor-art line (sathiyo and rangoli) is the primary idiom and the pichwai manner is the frame register, in season and never the niche; the default deity policy is P1, symbols and seva objects that are not a svarupa (W-61).

## When to use

- A card, title, set, frame device, transition, symbol or deity image is proposed.
- The `11_hindu_idiom` block (style-bible decision 11) is drafted, reviewed or changed.
- A motif's origin is shared, unclear or flagged, or a deity image's source is in question.
- A rights row is written for an artwork, a plate, a commissioned painting or a deity image.

## When not to use

- Rites, festivals, vrats, shlokas, invocations, rasa, objects or dates: use `hindu-life-story-frameworks`.
- Fonts, Indic script shaping, captions, sound, grading and loudness: the sibling tracks.
- Restoring or animating a real photograph of a person: `ai-photo-to-animation-pipeline`. Never run any AI route on a deity image.

## Inputs

- The household block, held offline with the ID key. Any key marked `TODO_maker` is the maker's answer. Ask for it in one line; never guess it.
- D-28 (the rule), D-31 (her world, as the register states it; do not repeat its details in repo text), D-27 (phone), D-16 (real memories), W-32 and W-33 (object clock, hands), W-34 (the one built room), W-38 (style bible), W-40 (faces), W-46 (rights tiers), W-61 (deity policy and the shrine moment), W-63 (the phone-safe frame), W-66 (Hindu-only audit values), W-70 (captures and seva articles), W-71 (the three places), W-72 (one idiom per register), W-75 (Gujarati on screen).
- `research/hindu-visual.md`: the tables K1 to K6, T1 to T11, the exclusion list E1 to E27 (the register counts E1 to E34 with the siblings' items, cited with their file) and the respect rules R1 to R20, with its "Follow-up research" answers (round 1: A1 to A8; round 2: B1 to B8).
- `research/pushtimarg-world.md` and `research/saurashtra-world.md` are in the repo (committed 2026-10-19); `research/gujarati-devotional-sound.md` is a sound note. They are her world, named in CHARTER.md, and own the tilak (pushtimarg-world T8), the haveli (F2, T3), Yamunaji (F8), Mahaprabhuji (F7), Takhteshwar and Harsiddhi (saurashtra-world T1 P01, P08) and the sathiyo (T12). Read them before any default. Where a sibling gives no answer, key the item to `TODO(research)` there and do not guess.

## Procedure

1. List the household keys the task needs. If one is `TODO_maker`, ask the maker in one line, or default to P1 (symbols and seva objects that are not a svarupa) and leave the item out. Where D-31 already answers a key, do not ask again; where a sibling sprint owns the answer (tilak, haveli, sathiyo, Yamunaji's form), cite it rather than guess.
2. Gate the motif. Its D-28 flag must be OK or OK-note. If it is FLAG or OUT, or on the exclusion list, leave it out and write the one-line question for the maker. The list gives each origin: a cusped arch, where the arch alone proves nothing [56]; Mughal-trained Kangra painting [35].
3. Check that it is hers: her region, her sampradaya, her hands or her shelf, or a floor art of her region. Her own tradition comes first; pan-Hindu comes second.
4. Name one form per deity shot, with its row on the iconography sheet (T3 in the research). Her own shelf image beats the default: the maker looks, counts and describes it, and photographs no svarupa and no picture of hers without her knowing (step 5). Disagreements go to the maker as one-line questions.
5. Choose the deity source route (R17) and fill `deity_source`. Under the default policy P1 no deity figure is drawn, generated or photographed, so only a symbol applies; the later routes open only if the maker rules a higher class at O-64. The routes are: an agent-drawn vector symbol checked against the sheet; a hand-traced public-domain plate with its plate ID and licence text logged, screened for satire (R18) and approved by the maker; her own photograph, by sight and untouched (W-70), on an unsynced phone, `cloud: none`, of seva objects that are not a svarupa (the lamp, the jhari in its red cloth, the thali, the folded cloth), never the Thakorji, Lalan, chitraji or any picture of hers without her knowing (`research/pushtimarg-world.md` PR4, F6: a picture may be pusht and in seva); a svarupa only if O-64 says yes and she knows, i.e. the April version at the earliest; or a commissioned painting under a signed licence. Never generative, never AI-altered, never a temple murti photograph, never a photograph of a framed print [79][83][84][86].
6. Draw as seekable SVG (Route A) where it fits. Use `pathLength` with `stroke-dashoffset` for line-draw [45]; `data-pivot` per joint for puppets, which have four to twelve joints [44]; `data-z` for order. Keep gold as a flat colour with a baked highlight; no filters.
7. Apply the phone floor: meaning-bearing lines 4 px or more; decoration 3 px or more and expendable; dots 6 px; puppet holes 4 px; hatching with a 3 px stroke at 9 px pitch; no 1 px and no hairlines. The phone-safe frame goes with it (W-63): must-read type at an x-height of 3.2% or more, hands and the object inside the central 80% of height. State every phone result as a measurement with its proxy (M, the synthetic chart [104]), not as a standard. The chat proxies are not WhatsApp's encoder [105].
8. Count arms, attributes and hand order against the sheet and her image, twice: once by an agent and once by the maker [61]. Never mirror a deity asset (a mirror reverses the hand order).
9. Walk R1 to R20 on every deity shot. Fix any fail in the frame itself; a note does not count as a fix. The sources behind the rules: [80] for feet and the ground; [85] for a human beside a deity; [91][93] for comic or casual treatment; [81] for complexion, sexualisation and aggression.
10. Write the rights row: type `artwork`, `deity_image` or `commissioned_art`; `tradition_origin`; `licence_text_saved` with the date; `plate_screening`; status GRANTED, VERIFY, ASK or NS. A CC BY-NC, non-commercial or share-alike term is ASK, never yes [14][15][1][25].
11. Label the honesty level (L0 to L5) in the file name and in `steps.csv`. A deity image is L0 or L1 (her own photograph of seva objects; a svarupa picture only in the April version, with O-64 yes and her knowing), L2 only for non-generative scaling, L3 for a traced plate, and never L4 or L5.
12. Write the brief with the W-42 fields: `motif_check` (hindu, Hindu-Gujarati, flagged, excluded, jain_flag, adivasi_flag or political-room, with a source), `deity_form`, `deity_source`, `respect_check` (R1 to R20, VR-1 to VR-3, PR1 to PR25), `phone_stroke_ok`, `phone_safe`, `political_room` and `seat_check`. Send every flagged brief and every deity shot to Fable. The maker approves each deity drawing as her proxy.
13. Return the pre-G2 checklist with each item's status (below).

## Checklists

**Gate (before drawing).**
- [ ] D-28 flag is OK or OK-note.
- [ ] Not on the exclusion list (E1 to E27 here, E1 to E34 with the siblings' items), or the maker's one-line overrule is logged.
- [ ] Hers: region, sampradaya, hands, shelf, or a floor art of her region.
- [ ] Can be drawn at the phone floor without losing its identity.

**Deity shot.**
- [ ] One named form; sheet row cited.
- [ ] `deity_source` route R17 chosen; plate ID and licence text logged.
- [ ] Two counts of arms, attributes and hand order; both match the row and her image.
- [ ] No mirror, no AI, no diffusion repair.
- [ ] R1 to R20 walked; every fail fixed in the frame.
- [ ] Symbol, seva object or figure, per the policy the maker set (default P1: symbols and seva objects that are not a svarupa).
- [ ] A prayer beat is her mandir's closed doors with the jhari in its red cloth and a lamp outside; no door, curtain, niche, seat or opening onto a person, and nothing in seva drawn (PR5 to PR7).

**Rights row.**
- [ ] Type, source, licence text saved with date, `tradition_origin`, `plate_screening`, status.
- [ ] Commission only under a signed written licence naming the film use, worldwide territory, the term (covering the April version and the archive), all media including the phone file, and the credit [25].

**Phone.**
- [ ] Every line at or above the floor: 4 px meaning, 3 px decoration, dots 6 px, holes 4 px, hatch 3 px at 9 px pitch.
- [ ] Checked on the synthetic chart (M) and, when measured, on real output on the project Android; her phone is never tested before the reveal (W-26, W-73).
- [ ] Phone-safe frame: must-read type 3.2% x-height or more; hands and the object inside the central 80% of height (W-63).

## Quality bar

Score the output on the register's six rubric items. Approve only at 4 or higher on each, with nothing critical open.

- **Meaning.** The motif is hers and its origin is named.
- **Specificity.** Form, sheet row, route, plate ID and px values are given.
- **Accuracy.** Each claim carries an [n] source, or is marked J, UNVERIFIED or TODO(research). No invented shloka, date, plate or licence.
- **Feasibility.** An agent and the maker can draw it by the gate date.
- **Ethics.** The respect rules hold; no generated deity; rights per record.
- **Craft and usability.** Legible at 4 px on a phone. Swap test: a different household produces a visibly different film.

## Guardrails

- **Respect.** No generated, altered or mirrored deity. No feet, shoes or soles near a deity [80]. No comic, casual or slangy treatment of a deity [91][93]. No dissolve, wipe or morph on a deity. No human at the same level and scale as a deity, and no hand in hand with one [85]. No fabricated ritual [83][84]. No sexualised or aggressive deity [81]. Padukaji (Mahaprabhuji's and Gusainji's footwear and footprints) are seva objects, not footwear: never below the knee, never worn; R3 does not apply to them (`research/pushtimarg-world.md` PR11).
- **Mahaprabhuji (Shri Vallabhacharya).** Revered in her sampradaya; apply the deity respect rules R1 to R20 and the real-person rules of D-16 (no AI, no animated face), whichever is stricter; form, mark and image convention come from `research/pushtimarg-world.md` F7, T8 and PR19 (leads, not rulings: rosary in the right hand and lotuses in the other; never on one seat or level with a svarupa); symbol only (P1) until the maker rules, static, framed high, never level with a svarupa and never captioned casually (W-61, PR19).
- **Her tradition (Pushtimarg).** Yamuna Maharani is the jhari in its red cloth, never a local sea or river, and Yamunajal is never poured away on screen (PR20, W-61, W-70). No darshan name on a card (PR16). Thakorji's seva articles never share a thali, lamp, cloth or frame with another deity's puja (PR18). Never draw or open the eyes of a svarupa (PR3). Run VR-1 to VR-3 and PR1 to PR25 (`playbooks/pushtimarg-world.md` T2) beside R1 to R20.
- **Hindu only (D-28).** No Mughal, Islamic or Christian motif. A shared or ambiguous motif is out by default. The maker overrules one line at a time, in the log. The rule governs motifs, not people. The pichwai is an OK-note, not a flag: the page read states a Deccan origin and names no Mughal or Rajput influence [38]; the Nathdwara school is a subset of the Mewar school ([114]; Wikipedia, Nathdwara painting [137]), the one Rajput idiom E10 does not flag [37]; and it is temple art of her own sampradaya. In the temple Shrinathji is never painted into the pichwai, so under P1 the register is the pichwai-manner border, bands and night sky with an object of hers or text at the centre, never the niche, never behind a face (`research/pushtimarg-world.md` PR5); painted only for Sharad and Gopashtami chapters, white-and-gold at Diwali and Annakut, none in winter, white at Vasant (PR23; the sanctum's rule from Talwar, `research/pushtimarg-world.md` [32]; a household's occasion cloth, painted or printed, is the maker's Q4/O-48, and `pushtimarg-world.md` records the open question); repeat unit 6 px or more. Its real cautions are that a painted svarupa is P4 by a hereditary painter who paints the day's shringar and that it is dense (the phone floor). Also out by default: mirror work (E27), mehndi unless asked (E17), paisley (E16), jaali (E1), chhatri (E4), the cusped arch (E2), the kulhe and jama-vagha silhouettes of a svarupa's shringar (`research/pushtimarg-world.md` E27, PR8; its E27 is a different item from this list's E27), "Saal Mubarak" on a card (`research/saurashtra-world.md` X11; Nutan Varshabhinandan instead), Ragamala as an image and the Rajput court idiom (E10). The swastika is the maker's call [88]: for her it is the sathiyo, her own hands' threshold drawing, shown or not (a lead to verify [123]).
- **The look and the shrine moment.** Primary idiom: the floor-art line (sathiyo and rangoli of her region; her own hand's form is the maker's answer), drawn as seekable SVG, meaning lines 4 px, decoration 3 px, dots 6 px. Frame register: the pichwai manner, in season, never the niche. Set language: her temple and her haveli drawn, never photographed. The shrine moment is her home mandir's closed doors at the hours the house closes them, with the jhari in its red cloth and a lamp outside (`research/pushtimarg-world.md` PR6; review 04 addendum 1.2); second, the shelf's small lamp with the backcloth changing by season, only if the maker's Q4/O-48 confirms a household occasion cloth; third, her threshold drawing as the seat of the Vasant kalash on the title card, only if the maker chooses the sathiyo (`playbooks/hindu-visual.md` Template H8, SW1 or SW2; under SW0 the kalash on a plain lotus).
- **Rights.** Clearance is per record. "Public domain" and "CC0" clear the record only [14][15][1]. Amar Chitra Katha panels, temple-trust calendar art, Pinterest reposts and Google Arts and Culture zooms are out [97][19]. Ask about a commercial reading before any public use. This is not legal advice; the legal points go to the TD-8 consult [25].
- **Privacy.** Nothing about her household in repo text. The household block stays offline with the ID key. Photograph her shelf only yourself, unseen, by sight and untouched, on an unsynced phone (W-32, W-70), and only seva objects that are not a svarupa (the lamp, the jhari in its red cloth, the thali, the folded cloth); never the Thakorji, Lalan, chitraji or any picture of hers without her knowing (`research/pushtimarg-world.md` PR4, F6); a svarupa only if O-64 says yes and she knows, i.e. the April version at the earliest. Never ask a relative to photograph her shelf or her temple. Temple photography rules are per temple; Tamil Nadu bans it [86]; her temples' rules: the Somnath Trust bans photography and phones [118] and the Ambaji trust bans phones, cameras and electronic gadgets in its premises [145]; no page states a rule for Takhteshwar, Nishkalank, Gopnath or Harsiddhi (`research/saurashtra-world.md` T1; UNVERIFIED).
- **Secrecy (D-02).** Nothing that tips her off. Nothing is asked of anyone that reveals the project.
- **Honesty (D-16).** Reconstructions are visibly reconstructions. No synthetic or cloned voice. No invented events, no invented words in a deity's mouth (R19).
- **Sanskrit and regional text.** Copy it only from a printed source, with its transliteration and the source named. Do not write new mantras or shlokas from memory.

## References

**Documents.**
- `playbooks/hindu-visual.md`: the maker's playbook, with the gaps (TODO(research)) and the record of changes asked of other playbooks.
- `research/hindu-visual.md`: the research, with every table this skill uses (K1 to K6, T1 to T11, E1 to E27, R1 to R20).
- `CHARTER.md`, `DECISIONS.md`: D-27, D-28, D-29, D-31; W-32, W-33, W-34, W-38, W-40, W-46, W-47, W-61, W-63, W-66, W-70 to W-72, W-75; O-06, O-47, O-54 and O-64 to O-67 (the register's IDs for review 04's O-40, O-38, O-43, O-42 and the look, the sathiyo and decision 11, and review 05's O-52).
- Playbooks changed by this track (applied 2026-10-19): cinematic-quality (T1 PR2b, B9, TY5 and HW1 to HW5; T2 decisions 3, 11 and 12; T5 items 28 to 39; T6; T9 rows 24 to 28; Exercise 9), animated (Decision 1, Exercise 7), ai-imagery (Steps 9 and 10). Still open in their own passes: theatrical-delivery (T8, T10), agent-pipeline (Route A, G2 pack), craft-visual (SVG hooks).

**Sources cited in this skill (copied from `research/hindu-visual.md`; "digest only" means seen in a search result and not opened).**

- [1] Cleveland Museum of Art, Open Access — https://www.clevelandart.org/open-access — 2026-10-19 — CC0 images and data; exclusions; launched January 2019 (read).
- [14] Wellcome Collection, "Lakshmi lustrated by two elephants" — https://wellcomecollection.org/works/phr7cv3d — 2026-10-19 — CC BY-NC 4.0, reference 26778i (read).
- [15] Wellcome Collection Catalogue API, query "Kalighat" — https://api.wellcomecollection.org/catalogue/v2/works?query=Kalighat&pageSize=100&include=items — 2026-10-19 — 184 results; licence tally 96 PDM, 4 CC BY, 3 CC BY-NC, 81 without images (queried).
- [19] Google Arts & Culture partner FAQ — https://support.google.com/culturalinstitute/partners/answer/6002688?hl=en — 2026-10-19 — digest only: partners keep rights.
- [25] Copyright Act, 1957, s.17 and the Act — https://indiankanoon.org/doc/1404402/ and https://indiankanoon.org/doc/1136195/ — 2026-10-19 — s.17(b) and proviso, s.19, s.22; the second page shows the 7 June 2012 text; currency UNVERIFIED (read).
- [35] Wikipedia, Kangra painting — https://en.wikipedia.org/wiki/Kangra_painting — 2026-10-19 — Mughal-trained origin, Vaishnava subject (read).
- [37] Wikipedia, Rajput painting — https://en.wikipedia.org/wiki/Rajput_painting — 2026-10-19 — schools, Mughal influence; Mewar "this most traditionalist of Rajput courts" (read; the Mewar sections re-read in full in round 2).
- [38] Wikipedia, Pichhwai (the page as served; "Pichwai" redirects to it) — https://en.wikipedia.org/wiki/Pichwai — 2026-10-19 — Pushtimarg, Shrinathji; a Deccan origin (Aurangabad named); names no Mughal or Rajput influence (read, re-read in rounds 1 and 2).
- [44] Sarmaya, Tholu Bommalata guide — https://sarmaya.in/guides/tholu-bommalata/ — 2026-10-19 — sizes, perforations, four to twelve joints, Lepakshi and Islamic influences (read).
- [45] Wikipedia, Kolam — https://en.wikipedia.org/wiki/Kolam — 2026-10-19 — pulli, sikku, Margazhi, mathematics (read; several claims tagged "citation needed").
- [56] Wikipedia, Torana — https://en.wikipedia.org/wiki/Torana — 2026-10-19 — Hindu, Buddhist, Jain; Chaulukya; mango-leaf torana (read).
- [61] T. A. Gopinatha Rao, Elements of Hindu Iconography, Vol. I Part I (Madras, 1914) — https://archive.org/details/india.history.resource.94142 (text at https://archive.org/download/india.history.resource.94142/94142_djvu.txt) — 2026-10-19 — Ganapati, Vishnu forms, the 24 images, Rama's group, Venkatesa, Vithoba, Jagannatha (read; a 1914 colonial-era scholar, some historical claims contested and not repeated).
- [79] Hindu American Foundation, "Can AI-generated images be used in worship?" (Devala Rees) — https://www.hinduamerican.org/?p=25156 — published 6 Oct 2025, updated 24 Oct 2025; read 2026-10-19.
- [80] Hindu American Foundation, guidelines on the commercial use of deity images — https://www.hinduamerican.org/?p=2408 — undated; read 2026-10-19 — "don't do it" and "caution" tiers.
- [81] Das, Kundu, Mim, Guha and Ahmed, "Generative AI Alignment with Hinduism's Theological Plurality and Sacred Representation", arXiv:2608.28228v1 — https://arxiv.org/html/2608.28228v1 — 28 Aug 2026; read 2026-10-19 — 15 interviews, June 2024 to April 2026; models not named.
- [83] Sambad English, SJTA files police complaint over AI-generated videos of Lord Jagannath — https://sambadenglish.com/latest-news/sjta-files-police-complaint-over-ai-generated-videos-of-lord-jagannath-11014550 — 20 Jan 2026; read 2026-10-19.
- [84] Organiser, AI-generated videos of Bhagwan Jagannath spark outrage — https://organiser.org/2026/01/21/336054/bharat/odisha-ai-generated-videos-of-bhagwan-jagannath-spark-outrage-puri-temple-administration-files-police-complaint/ — 21 Jan 2026; read 2026-10-19 — "nationalist" slant; temple's account only.
- [85] IOL, Phoenix artist under fire for AI images with Hindu deities — https://iol.co.za/thepost/news/2024-10-06-phoenix-artist-under-fire-for-ai-images-with-hindu-deities/ — about 2024 (the page says "2 years ago"); read 2026-10-19.
- [86] The Star, Tamil Nadu: temples ease phone restrictions, retain ban on photography — https://www.thestar.com.my/aseanplus/aseanplus-news/2026/10/11/tamil-nadu-temples-ease-phone-restrictions-retain-ban-on-photography — 11 Oct 2026; read 2026-10-19.
- [88] Hindu American Foundation, Reporters Guide to the Swastika — https://www.hinduamerican.org/swastika-reporters-guide/ — undated; read 2026-10-19 (the 45-degree description is from a WION explainer credited to HAF, digest only: https://embed.wionews.com/web-stories/india-news/business-economy/difference-between-swastika-and-hakenkreuz-1719917836714).
- [91] Wikipedia, Ramayana: The Legend of Prince Rama — https://en.wikipedia.org/wiki/Ramayana:_The_Legend_of_Prince_Rama — 2026-10-19 (read).
- [93] Wikipedia, Adipurush — https://en.wikipedia.org/wiki/Adipurush — 2026-10-19 (read; first 100,000 of 135,700 characters).
- [97] Wikipedia, Amar Chitra Katha — https://en.wikipedia.org/wiki/Amar_Chitra_Katha — 2026-10-19 (read).
- [104] Phone-legibility fixture, this sprint — `research/hindu-visual-fixtures/` (chart, results, README) — 2026-10-19 — M-H1.
- [105] Anecdotal WhatsApp reports — https://obsproject.com/forum/threads/what%C2%B4s-the-best-video-quality-small-files-for-whatsapp-settings.110051/ ; https://www.guidingtech.com/send-hd-photos-and-videos-in-whatsapp/ — 2026-10-19 — digest only: about 640 px wide at about 500 kb/s, some 15 fps; "HD" means 720p. Not a measurement of the real encoder.
- [114] Wikipedia, Nathdwara — https://en.wikipedia.org/wiki/Nathdwara — 2026-10-19 — Haveli of Shrinathji; Mewar-school Pichwai painting; the page carries promotional-tone and missing-citation tags (read).
- [118] Shree Somnath Trust, FAQ — https://somnath.org/faq/ — 2026-10-19 — "Photography is strictly prohibited"; electronic gadgets prohibited (read).
- [123] English Wiktionary, સાથિયો — https://en.wiktionary.org/wiki/સાથિયો — 2026-10-19 — "(Hinduism) swastika, a religious symbol"; entry last edited 1 March 2023 (read; the script is the headword, for lookup only).
- [137] Wikipedia, Nathdwara painting — https://en.wikipedia.org/wiki/Nathdwara_painting — 2026-10-19 — "subset of the Mewar school" (raw wikitext read).
- [145] Arasuri Ambaji Mata Devasthan Trust, official site — https://ambajitemple.in/ambaji-temple ; https://ambajitemple.in/ — 2026-10-19 — "no idol of the Goddess", the Yantra worshipped as the deity; the premises ban on phones, cameras and electronic gadgets (wording as returned by the fetch tool's quoted fragments).

## Changelog

- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): the register's IDs for the deity policy, hands, phone and household keys (O-64, O-06, O-54, O-47); W-42 brief fields; the shrine moment, the Pushtimarg and Yamunaji rules, photographs by sight and untouched, the phone-safe frame, and no testing on her phone before the reveal (W-61, W-63, W-70, W-26, W-73); the sibling notes are committed; style-bible decision 12 is moving footage and `11_hindu_idiom` keeps its number.
