# Devotional music, the sound of a Hindu home, and Indic scripts on screen

*Track: devotional-sound-script · Version 0.2 (round 1 revision) · Written 2026-10-19 (Monday), 19 weeks before the premiere on Saturday 2027-02-27 · Built from `research/devotional-sound-script.md` (researcher notes, 2026-10-19), `CHARTER.md` and `DECISIONS.md`. Where this playbook and the register disagree, the register wins. Scribe: Haiku; the Fable round 1 review (`reviews/devotional-sound-script-round1.md`) applied by the Sonnet implementor.*

*Reading key: [n] points to a source in the Sources list at the end, using the researcher's numbers. "(inference)" marks our suggestion, not something a source says. "UNVERIFIED" means the fact was not confirmed from a page that was opened. "TODO(research)" marks a gap. "SR" means a search-result summary only. Rights statements are as read on 2026-10-19 and wait on the premiere country (O-02, TD-7). This is not legal advice.*

*Her tradition is named here at the level the register uses (D-31). Her city, family, temple and other identifying details are left out, because the repo is public. Those details belong offline on the maker's machine.*

---

## Why this matters for our film

The most personal sounds in the film come from her home: a brass bell, a conch, the cooker's whistle, the grinder, a bhajan she knows by heart. The most personal words are the ones on screen: a deity's name, a verse, a title in her script. Both are where a mistake shows most. A bell that is someone else's recording, a verse with a broken conjunct, or a caption that falls back to another typeface will be noticed by her first and by the room second.

Four rules from the register set the limits before any choice is made.

- **D-05.** The premiere cut carries no recorded voice of any living person except her own HER-PUBLIC clip, if one passes. A temple's chanting crowd, a radio announcer and a vendor's cry are out as content.
- **D-16.** No synthetic or cloned voice of any real person, living or dead, even with consent. No AI-sung devotional text.
- **D-17 and D-02.** Nothing records her without her knowledge and a spoken yes. The maker records objects and rooms when the house is empty, on a device that does not sync to a shared cloud.
- **D-28 and D-31.** "Indian themes" always means Hindu themes: Sanatan Dharma and its sanskriti. Her tradition comes first and pan-Hindu material second. No Mughal or other Islamic motifs, and no Christian motifs.

Phones matter here too. D-27 says the film must play beautifully on a phone, and D-31 says her phone is Android. A phone speaker loses the low body of a drone and most of the room rumble. A caption that is correct in your own PC preview can break in a phone player, because a live-text file is shaped by that player's own fonts and rules. `playbooks/mobile-delivery.md` owns the phone caption pass and the phone-speaker protocol. This playbook supplies its sound and text inputs.

The first question is not "which raga?" It is "which of her things is this?" A sound or a word earns its place by being hers (charter Principle 2). The raga, the instrument and the script all follow from that answer.

---

## Core principles

1. **Hers first, pan-Hindu second.** (D-28, D-31; charter Principle 2.) A sound, a deity, a festival or a script enters the film because it is hers. A generic "Indian" sound, such as a stock temple bell or a dhak drum, is a labelled fallback only where she cannot be recorded, and it is never a motif by default. [Template I; note Summary 15]
2. **The words can be free while the tune is owned.** "Devotional means free" is wrong in five ways. The words may be public domain (Tulsidas, died 1623 [14, SR]; Annamacharya, died 1503 [56]; Phillauri, died 1881 [12]) while the tune, the arrangement, the recording and the performance belong to someone. Check each of the four separately. [note Summary 6; Q3]
3. **Origin is a question for the maker, not a ruling for the team.** Where a sound, a form or a name has a shared or court history (sitar, sarod, tabla, shehnai, santoor, khayal, harmonium, tanpura, ektara), flag it and default to leaving it out until the maker rules. The default cell value is `ASK`, which means silence or room tone in the render. [Template C; note Summary 13]
4. **No raga is assigned to her tradition until a named source or a teacher names it.** Raga-to-rasa is our inference, not the tradition's. Time-of-day windows differ between sources. No raga name goes on screen or in credits unless the recording's own metadata carries it. Where a name is needed, use Carnatic Kalyani or no name. [Q1; Template B]
5. **Licence by item and by country.** An uploader's licence field is a claim. The Great 78 Project says its audio is for "research, teaching, and private study only" [25]. ND cannot go under picture. NC and SA need a decision. A free, unticketed premiere is still a public showing. [Q4, Q5; Template F]
6. **Test Indic text on the real burn-in path, on the real machine.** Complex shaping is what we want. Before ffmpeg n9.0 the `subtitles` filter runs libass in simple shaping, which breaks conjuncts without any warning [96]. Fonts must be the ones the renderer will actually find. Size and wrap by measured width and base-letter height, not by a character count. [Q10; Template K; Template L1]
7. **Plan the sound and the text for a phone as well.** A phone speaker keeps a drone's jawari buzz but loses its body. Room rumble vanishes. Her Android phone is the device that counts for the live-text captions. [note Summary 14; Template L2; D-31]
8. **No AI voice of devotional text, and AI music is a poor fit.** The current AI music terms bar film use or allow only personal or non-commercial use, and no tool is shown to handle raga grammar, gamaka, tala or Sanskrit pronunciation. A locally run instrumental drone, labelled, is the only AI-adjacent option, and it almost never belongs in the premiere cut. [Template G]

*Terms used here, in plain words:* **raga** is a melodic framework; **tala** is a rhythmic cycle; **gamaka** is an ornament on a note; **sync** is permission to put music against picture; **master** is permission to use one particular recording; **ND, NC and SA** are Creative Commons terms (no derivatives, non-commercial, share-alike); **shaping** is how a script's letters combine into the glyphs drawn on screen; a **conjunct** joins two consonants into one form; the **reph** is a ra mark drawn above a letter; the **short-i** is a vowel sign drawn to the left of its consonant but spoken after it (general knowledge).

---

## How to do it, step by step

**Step 1. Settle the premiere country (O-02, TD-7). By Sunday 25 October.** Every term, every reading of the Indian section 52 exemption, and every performing-rights question depends on it. Until it is answered, every rights line reads "not yet known; confirm" (W-46). *Done when:* the country is written in the register.

**Step 2. Read the rows that bind this track.** Read D-05, D-16, D-17, D-28 and D-31 in `DECISIONS.md`, and the open rows O-36 and O-41. The proposed rows O-36 to O-45 are in `reviews/04-hindu-mobile-briefs-review.md` but are not yet rows in `DECISIONS.md`; the orchestrator must enter them before this track's decisions count. Note that `reviews/05-her-world-briefs-review.md` records the state, district, language and script (O-36) as answered; the script for Sanskrit verse is still open.

**Step 3. Build the tradition and text sheet (Template N, T-2 below).** One row per deity, festival or text in D-31. Fill "Source says" only from a page you have read, and quote it exactly. Mark a row `hers` only when the maker says so (O-38, O-39, O-41). *By:* rows for the script and settings card, Sunday 1 November; the cue map, Saturday 14 November.

**Step 4. Decide the script stack (O-36).** Use the decision table in T-7. The Gujarati caption set, the Devanagari verse strings and the title art all go on the settings card on Sunday 1 November.

**Step 5. Run the shaping gate on the PC (Template K, T-8).** Start with the ten-minute A/B in T-8 item 6 (Template K item 8 in the note). It decides whether the project's SRT template can burn Indic text at all. The full gate takes about an hour (item 2 of Template K, per the note). Sign the settings card only when all four gate conditions pass.

**Step 6. Size and wrap captions by measured width (T-9 and T-10).** Keep Tamil and Malayalam faces within the 90% box. Break only at word boundaries.

**Step 7. Make the sound list (T-3).** The maker records the house alone, when it is empty, on a device that does not sync to a shared cloud. The register's holiday window (Monday 21 December to Sunday 3 January, W-10) is the planned slot. Nothing records her. Each capture is a T8 `audio` row marked `maker`. Asking a temple's permission means telling someone a recording is being made (D-03, D-02). Default: record bells from the public hall only where recording is openly allowed without asking anyone; otherwise skip S-13 and use S-02, the household's own bell.

**Step 8. Flag every instrument (T-4).** Any flagged item defaults to `maker_rule = ASK`.

**Step 9. Build the cue map (T-1).** Every MOTIF and CLOCK row needs a `source_in_her_life`. A `raga_id` needs a named source. A MOTIF with `composition_status=unknown` blocks lock. A cue still `ASK` on Monday 14 December is replaced by silence or room tone.

**Step 10. Clear each source (T-5).** Run the ten-step checklist and the country table. Log each one as a T8 row: `music` for cues, `font` for typefaces, `audio` for captures. A platform's default contract is not the signed letter in T-6.

**Step 11. Phone and mono pass.** Run the 50% volume check and the phone-speaker sweep on a sample of each cue using the sibling's protocol in `playbooks/mobile-delivery.md`. Then run the mono fold. Record PASS or FAIL in `phone_check` and `mono_check`. The venue test is `playbooks/music-sound.md` Step 16.

**Step 12. Lock.** Every cue has a decision by Monday 14 December (W-44). Substitutes are locked by Friday 8 January.

---

## Learn-by-doing exercises

Times marked "estimate" are ours. The note gives the times for Template K item 2 (about an hour) and item 8 (about ten minutes).

### Exercise 1. Key your sheet to your unknowns

- **Goal.** See which decisions wait on which answers.
- **Steps.** (1) List the open items in the register and the proposed O-36 to O-45. (2) For each, write which table it unlocks (T-11). (3) Mark each row answered or `ASK`.
- **Time.** About 45 minutes (estimate).
- **What good looks like.** Every row in T-11 has an answer or `ASK`. No row is filled by a guess from a surname, a place or a photo.

### Exercise 2. Run the ten-minute subtitles test

- **Goal.** Learn whether the project's own SRT template shapes Indic text on your ffmpeg build.
- **Steps.** Render one frame of the A/B cue `ab.srt` three ways: with the project's `subtitles=` burn; with `shaping=simple`; and with an `ass=` file made from the same SRT. `ab.srt` is one cue of non-sacred test syllables only: Gujarati `શ્રી ક્ષ જ્ઞ ધર્મ કિ ક્ષિ`, Devanagari `क्ष त्र ज्ञ धर्म कि क्षि`. Never run the FAIL or `shaping=simple` render on a mantra, a deity's name, an aarti line or a Vedic verse; the broken frame is a deliberately wrong rendering and is kept only for the test syllables. The fixture folder's README (command 3b) has the commands. Do not copy them from this playbook.
- **Pass.** The default frame differs from the `simple` frame and matches the `ass` frame. **Fail.** The default frame matches `simple`, which is what ffmpeg 5.1 to 8.1.1 does [96].
- **Time.** About 10 minutes at the PC (note, Template K item 8).
- **What good looks like.** A T8 note with the PASS or FAIL, the output of `ffmpeg -version`, and the date. Do not treat the `Shaper:` log line as proof; it prints the same in both cases (note Summary 1).

### Exercise 3. Read the font log

- **Goal.** Prove which font drew each line.
- **Steps.** Run the libass burn with its debug output. Find each `fontselect:` line and check that it names the file you meant. Search for `Glyph 0x... not found`.
- **Time.** About 30 minutes (estimate).
- **What good looks like.** Every family resolves to its own file. The Anek and Catamaran variable files are not used by their plain family names (use a static instance, or the name libass prints). A Gujarati year set in a face without Gujarati digits shows the fallback line, and that face is then not used for dates.

### Exercise 4. Sort ten sounds with the hers-if key

- **Goal.** See what is hers and what needs a yes.
- **Steps.** Take ten rows from T-3. For each, answer the hers-if question, the voice risk and the capture method. Mark the row `ASK` where the answer is unknown.
- **Time.** About 40 minutes (estimate).
- **What good looks like.** No row records her or asks a relative to record. Every "hers" cell is answered or `ASK`.

### Exercise 5. Vet one archive item

- **Goal.** Learn why a licence field is a claim.
- **Steps.** Pick one item from T-5. Read its licence on the host's page and, where you can, on the rights holder's own page. Answer the ten checklist questions. Write a verdict and its reason. Do not download commercial audio to do this.
- **Time.** About 60 minutes (estimate).
- **What good looks like.** A verdict that names the page, the date you read it and the premiere country. A licence field is never the whole answer.

### Exercise 6. Write a name-free brief for one cue

- **Goal.** Practise the one-cue commission brief and its clauses. D-03 and D-07 mean nothing is sent before the premiere, so write it only.
- **Steps.** Copy the brief in T-6 and fill the instrument, the mood word and the time of day. Check that it names no deity, family, place or the film's subject. Check the seven s.19 clauses listed under it.
- **Time.** About 30 minutes (estimate).
- **What good looks like.** The brief tells a musician what it needs and reveals nothing else.

### Exercise 7. Check a caption line for width

- **Goal.** Find where a line passes the 90% box.
- **Steps.** Take one sample of 40 to 50 code points per script. Measure the rendered width at FontSize 23 with the fixture's procedure (the README, not this playbook). Compare the width to the box.
- **Time.** About 45 minutes (estimate).
- **What good looks like.** No line sits over 90% of the box. Any overflow is fixed by a shorter line or a smaller face, not by counting characters. The note found Noto Sans Tamil at 101.0% for a 41-code-point line, so the count of 42 is not the rule [note L1(d)].

### Exercise 8. Hear what the phone loses

- **Goal.** Hear the phone's bass cut-off on your own sounds.
- **Steps.** Record one bell and one room tone with the house empty. Play each at 50% volume on a phone speaker, then through headphones. Write down what has gone.
- **Time.** About 30 minutes (estimate).
- **What good looks like.** A note of what survived. The note's own model found that a drone keeps its buzz, and that room rumble and low "temple ambience" lose about 20 dB [note Summary 14]. Your result is a measurement of your device, not the note's model.

---

## Templates and checklists

### T-1. The cue map (extends `playbooks/music-sound.md` Step 5; Template A)

The first six columns are the existing Step 5 columns, unchanged. The other nineteen are new.

```
beat_id,cue_type,source_in_her_life,hard_flag,advisor_flag_ref,notes,tradition,raga_or_mode,raga_id,time_of_day_or_season,rasa,rasa_basis,instruments,origin_flag,maker_rule,source_route,licence_log_ref,composition_status,recording_status,performer_status,voice_present,phone_check,mono_check,not_before,date_read
```

- `tradition`: `hindustani`, `carnatic`, `temple_ritual`, `folk_regional:<name>`, `domestic_sound`, `none`.
- `raga_or_mode`: a raga name only if a named source or a teacher identifies it, or the cue is a vetted public-domain recording whose metadata says so. Otherwise use `none (drone only)`, `her tune (raga unknown)` or `pentatonic mode (not named)`.
- `raga_id`: R-01 to R-24 from the note's Template B, or blank. The full table is in `research/devotional-sound-script.md`.
- `time_of_day_or_season`: `dawn`, `morning`, `afternoon`, `dusk`, `evening`, `night`, `late_night`, `monsoon`, `any`, `n/a`. This is the same field as `season_or_time_of_day` in `research/hindu-frameworks.md`, so the two sheets join.
- `rasa`: `shanta`, `karuna`, `shringara_decorous`, `vira_quiet`, `hasya`, `adbhuta`, `vatsalya`. `rasa_basis`: `module_turn`, `tradition_word:<quote>` (a source's mood word) or `inference`.
- `instruments`: I-ids from T-4, separated by `;`.
- `origin_flag`: `NONE`, `SHARED`, `COURT`, `SUFI`, `CHURCH`, `COLONIAL_EUROPEAN`, `DHARMIC_NOT_HINDU`, `UNVERIFIED` (several allowed). `CHURCH` = a documented church or missionary channel. `COLONIAL_EUROPEAN` = a European instrument adopted in the colonial era, with no church channel shown. A flag says what the source says and no more.
- `maker_rule`: blank, `IN`, `OUT` or `ASK`. Default for any flagged instrument or form is `ASK`.
- `source_route`: in this order, `SILENCE`, `HER_TUNE_HUMMED`, `PD_PERFORMANCE_EXISTING`, `MAKER_OWN_SOUND`, `CC0`, `CC_BY`, `LOCAL_AI_BED`, `LICENSED_SONG`. Lean: none of the last two.
- `licence_log_ref`: the T8 `asset_id` (`MU-` for music, `FN-` for fonts).
- `composition_status`: `PD_text_and_tune`, `PD_text_owned_tune`, `owned`, `unknown`. `recording_status`: `n/a`, `PD:<countries>`, `owned:<label>`, `CC:<type>`, `maker`. `performer_status`: `maker`, `relative:release_pending`, `hired:written_consent_s38A2`, `n/a`.
- `voice_present`: `yes` or `no`. A `yes` row cannot enter the premiere cut unless it is her HER-PUBLIC clip (D-05).
- `not_before`: `PREMIERE`, `TD-L2c` or `APRIL` (D-07 and D-06).

**Rules.** (1) No MOTIF or CLOCK row without `source_in_her_life`. (2) A row with a `raga_id` but no named source is invalid. (3) Every `LOCAL_AI_BED` row has `voice_present=yes`, is labelled, never sits on the emotional peak, and is marked `APRIL`. (4) Any `origin_flag` other than `NONE` needs a `maker_rule` by Monday 14 December. (5) `composition_status=unknown` on a MOTIF blocks lock.

### T-2. Tradition and text sheet (Template N, condensed)

Columns: **Row · Item · What the source says · Text · Tune and recording · Use before April · Flag.** Under D-05, any recording of a living voice is a note for the April version unless it says otherwise.

| Row | Item | What the source says | Text | Tune and recording | Use before April | Flag |
|---|---|---|---|---|---|---|
| N1 | Haveli sangeet (temple kirtan) | Braj Bhasha padas by the Ashtachhap; verse divided into sthayi, antara, sanchari, abhog; instruments named: pakhavaj, bin, sarangi, tanpura, harmonium [88]; a 2026 peer-reviewed paper names pakhawaj, tanpura, harmonium, manjira and jhanjh [97] and a 2021 field study names jhanj, harmonium, been, sarangi and pakhawaj [98]; the bansuri is excluded because "sectarian custom treats the instrument as a sacred emblem reserved exclusively for Krishna" [88], a claim no other source repeats, while [97]'s list of 36 instruments of divine service includes Murali: contested, UNVERIFIED. The liturgy draws on nearly ten thousand padas by 30 to 40 poets [89]. The printed book to read is Gaston, *Krishna's Musicians* [102] (not read) | Public domain (16th-century poets; the page gives no dates) | Oral repertoire; a family's tune is unknown, so `composition_status=unknown` | Card text only, two lines, and only if hers | Recording and photography rules inside a haveli: none found that allow recording without asking; Nathdwara bars phones and cameras per an independent portal [100]. Ask the family, never a haveli |
| N2 | The eight daily darshans | Mangala, Shringara, Gvala, Rajabhoga, Utthapana, Bhoga, Sandhyarati, Shayana [89] (that list carries no inline citation on the page); the same eight names appear in the temple's own blog [99], an independent portal with hours [100] and a peer-reviewed paper [97]; the hours differ between sources | n/a | n/a | A structure for the day clock (inference) | Does her home keep any, and which? |
| N3 | Ashtakshar mantra `śrī kṛṣṇaḥ śaraṇaṃ mama` | Repeated three times in the first ceremony [89] | Traditional | Spoken or sung by family | Card, never audio | Which script she knows it in |
| N4 | Yamunashtakam | "an esoteric hymn to the river goddess Yamuna which is recited daily by followers"; Sanskrit; Vallabha died 1530 per sectarian accounts [90] | Public domain | Recitation is a living voice | Card only | Gujarati or Devanagari script |
| N5 | Narsinh Mehta's bhajans; the prabhatiya (morning) genre | 15th-century Gujarati poet-saint; "there is no consensus among scholars on exact dates"; "the prabhatiya genre is sung in the morning to evoke peacefulness and contentment" [91] | Public domain as a poet's work. A modernised printed edition may be a newer work (UNVERIFIED; T10) | Oral; recordings owned | A prabhatiya line as the morning card, only if hers | Which edition her family reads |
| N6 | "Vaishnava Jana To" | Narsinh Mehta's best-known composition; the best-known melody is a semi-classical arrangement set in the 1920s by Narayan Khare at Sabarmati Ashram, in Mishra Khamaj [92] | Public domain. The tool did not reproduce the first Gujarati line, so do not caption from this note | The arranger's death year is UNVERIFIED (not found in round 1 either [113]; the note's Follow-up 3 has the term table keyed on the year); recordings are owned | Text only | Whether her family sings this tune |
| N7 | Aarti: "Om Jai Jagdish Hare"; the Ambe Maa and Shiva, Lakshmi and Ganesh aartis | Phillauri wrote "Om Jai Jagdish Hare" c. 1870, and died 1881 [12]. Wikipedia credits the Marathi Ganesh aarti "Sukhakarta Dukhaharta" to Samarth Ramdas (1608 to 1682) [103]. No page opened names an author or a date for "Jai Adhya Shakti" or for the Shiva, Lakshmi or "Jai Ganesh Deva" aartis [112]; a sibling note reports a "Shivanand Swami" signature in the Shiva and Amba aartis, no date [R8]; the lead from memory (Shivanand Swami, 18th century) stays UNVERIFIED | Free to caption as text: "Om Jai Jagdish Hare"; "Sukhakarta Dukhaharta" only if it is hers. Every other aarti: unknown | Arrangements, printed editions and recordings owned | No other aarti text captioned until its author is read from a page opened | Do not caption any other aarti text before then |
| N8 | Garba and raas at Navaratri | A circle dance round an image of Amba or a clay pot with a flame; "the dhol and dholak (Indian drums), cymbals and shehnai" [93] | Traditional lines unknown | Film and album garbas are label property; a crowd recorded at an event is living voices | None (D-05) | The dhol is the only sound a source names; the shehnai carries an origin flag |
| N9 | Harsiddhi | "a regional Hindu goddess, popular in Gujarat, Madhya Pradesh, adjoining Maharashtra"; one aspect of Durga; kuldevi of many families [94]. No aarti named | n/a | n/a | None | Which song her home sings for her (O-38) |
| N10 | Shiva: "Om Namah Shivaya"; the Mahamrityunjaya mantra | Not re-read by the researcher (mantra text; traditional) | Traditional | Recordings owned (the note's row) | Card only, never audio | Fixture strings test its marks |
| N11 | Women's songs at festivals ("dhol songs") | "in Gujarat lay devotees, mainly women, sing dhol songs" [89]; [89] cites Mallison (1986), whose first page says the dhola are sung "essentiellement, sinon exclusivement, par des femmes" [101] | Traditional | A recording of living people | None (D-05, D-17) | That they sit outside the temple liturgy is [89]'s claim; only p. 79 of the primary was read |
| N12 | Ganesh and Lakshmi songs | Not researched | n/a | n/a | n/a | Add after the maker names which songs her home sings |

### T-3. The sound list for a Hindu home (Template I, condensed)

Rules that decide every row: D-17 (never record her), D-05 (no living voice in the premiere cut), Principle 2 (a sound earns its place by being hers), D-02 (record on a device that does not sync), and W-10 (the holiday window). "Hers if" keys to T-11. A row whose key is unanswered waits.

| id | Sound | Hers if | How to capture without recording her | Voice risk (D-05) | Phone (note's model) | Stand-in (only if hers; label it) |
|---|---|---|---|---|---|---|
| S-01 | Morning conch | She blows one at puja (O-38, O-39) | The maker blows or strikes the household's shell in the empty prayer corner | None | Survives | CC0 conch, 10.9 s [37] |
| S-02 | Brass hand-bell | A bell is on her shelf | The maker rings it at arm's length | None | Survives | CC0 temple bell, 30.5 s [37] |
| S-03 | Lamp, match, incense | She lights them daily | The maker strikes a match in the empty room | None | The hiss survives | None needed |
| S-04 | Pressure-cooker whistle | The cooker is hers | The maker runs it, house empty (fire safety first) | None | Survives | CC0 cooker, location unknown [37] |
| S-05 | Tadka sizzle | She tempers (ask only by looking at the pans) | The maker tempers in her pan | None | Survives | None |
| S-06 | Mixer-grinder | She owns one | Run it empty or with water | None | Mid band survives; low motor rumble weak | None |
| S-07 | Grinding stone | The stone is kept | The maker turns it | None | Partly survives | None |
| S-08 | Rice washing, steel tumbler and ladle | Daily kitchen objects | The maker, hands only | None | Survives | None |
| S-09 | Kolam or rangoli, powder swish | She draws (O-40) | The maker draws a test pattern in rice flour; no sand product | None | Very quiet; weak | None |
| S-10 | Bangles, anklets, a brass box | They are hers | The maker handles the objects in the box; never worn | None | Survives | None |
| S-11 | Room tone (kitchen, prayer corner, hall; W-10) | Always | 60 seconds per room, door shut, phone in airplane mode | None | Low rumble vanishes (-19.6 dB in one sample) | None |
| S-12 | Koel at dawn, crows | The garden or balcony had them | From the maker's own spot at dawn | None | Survives | CC0 koel, Singapore park, 7.8 s [37]; season UNVERIFIED |
| S-13 | Temple aarti at dusk | Her temple (O-38) | Bells, ghanta and drums only, from the public hall at off-peak times; the temple's own recording rule governs; no sung words. Asking a temple's permission means telling someone a recording is being made (D-03, D-02). Default: record bells from the public hall only where recording is openly allowed without asking anyone; otherwise skip S-13 and use S-02, the household's own bell. No rule allowing it was found at a haveli or temple of her tradition [100][110][111] | **High**: the congregation and priests are living voices | Survives | CC0 "Temple Ambience" has some people in it; check for speech [37] |
| S-14 | Temple loudspeaker from the street | The family hears one | An unintelligible distant wash only, if D-05 allows (open question 4) | High | n/a | None |
| S-15 | The 6 a.m. devotional radio | She keeps one | The radio's click and hiss with no station; never the programme | High | Survives | None |
| S-16 | Diwali crackers | She keeps Diwali (O-39) | From the maker's own street on the night | Street voices | Survives | Licence not verified (SR) |
| S-17 | Dhak, Durga Puja drums | **Not hers on D-31's region** (not Bengal) | No capture without a visit | Festival crowds | Survives | Kolkata dhaak, CC BY 4.0, credit needed [37]; out unless she says it is hers |
| S-18 | Ganesh visarjan drums | She keeps Ganesh Chaturthi | Not capturable in the window | Crowds | Survives | "Immersion Procession" pack: licence not shown on the pack page; read the file page |
| S-19 | Street: scooters, school bell, vendors | Only if the street is hers | Vendor cries are voices; skip | High | Survives | None: generic is out |
| S-20 | Train or station | Only if a journey is hers | By the maker on a visit; no announcements | High | Survives | None |

### T-4. Instrument and form flags (Template C, condensed)

Every flag other than NONE defaults to `maker_rule = ASK`. The flags come from the sources named; general-knowledge flags are marked UNVERIFIED. Flag vocabulary: NONE, SHARED, COURT, SUFI, CHURCH (a documented church or missionary channel), COLONIAL_EUROPEAN (a European instrument adopted in the colonial era, no church channel shown), DHARMIC_NOT_HINDU, UNVERIFIED. The skill's two lists equal the Default column: out = sitar, sarod, santoor, khayal; `ASK` = bansuri, tanpura, ektara, tabla, shehnai, harmonium and the Carnatic violin.

| id | Instrument or form | Flag | Note and source | Default |
|---|---|---|---|---|
| I-01 | Shankha (conch) | NONE (UNVERIFIED) | No page opened | IN if hers |
| I-02 | Ghanta (bell) | NONE (UNVERIFIED) | No page opened | IN if hers |
| I-03 | Damaru | NONE (UNVERIFIED) | Hourglass drum; shared with Tibetan Buddhist ritual (general knowledge) | IN if hers |
| I-04 | Manjira, kartal | NONE (UNVERIFIED) | Bhakti and kirtan | IN if hers |
| I-05 | Mridangam | NONE (UNVERIFIED) | Carnatic and temple; the tabla page carries a legend of Krishna halving a barrel drum [47] | IN if hers |
| I-06 | Pakhawaj | NONE; court use UNVERIFIED | Prakrit name (Sanskrit *pakṣavādya*); wooden body from the 14th century [51] | IN if hers |
| I-07 | Nadaswaram and thavil | NONE | "mangala vadyam", "very auspicious" [53] | IN if hers |
| I-08 | Chenda, edakka | NONE or SHARED (UNVERIFIED) | Also played at church festivals in Kerala (general knowledge) | Ask only if her region is Kerala |
| I-09 | Dhak | NONE | Bengal Durga Puja | Not hers on D-31's region |
| I-10 | Veena | NONE (UNVERIFIED) | No page opened | IN if hers |
| I-11 | Bansuri | NONE (UNVERIFIED; exclusion contested) | One tagged page says her sampradaya's temple custom keeps it out of the sanctum [88]; a 2026 paper lists Murali among 36 instruments of divine service and states no exclusion [97]; the temple's blog shows the deity's flute placed, withheld or offered darshan by darshan [99] | **ASK**. No stock "Krishna flute" bed |
| I-12 | Tanpura | SHARED-LIGHT | "Tumburu Vina" in Sanskrit; the modern form first pictured in Mughal-era paintings [52] | **ASK** |
| I-13 | Ektara | SHARED | Baul and kirtan use; "used by Hindu Sadhus and Islamic Sufi saints" [50] | **ASK** |
| I-14 | Sitar | COURT | First use of the word dated 1739; not in iconography before 1790 [46] | Out unless hers |
| I-15 | Sarod | COURT (AFGHAN) | From the instrument still played in Afghanistan, Pakistan and Kashmir; first mention about 1830 [46] | Out unless hers |
| I-16 | Tabla | SHARED (disputed) | "Clear pictorial evidence of the drum emerges only from about 1745" [47] | **ASK** (O-41) |
| I-17 | Shehnai | SHARED | Persian name or folk pungi; part of the royal naubat and of temple use [54, SR] | **ASK**; not chosen because it "sounds Indian" |
| I-18 | Santoor | SUFI or PERSIAN | "directly borrowed from the Persian santoor" [48] | Out |
| I-19 | Harmonium | COLONIAL_EUROPEAN (missionary channel: 'possibly' per [44]; unproven) | Arrived "possibly with missionaries or traders" in the mid-19th century; banned from All India Radio 1940 to 1971; widely used in bhajan and kirtan [44]. Used in her sampradaya's temple music, per [88], a 2026 peer-reviewed paper [97] and a 2021 field study [98] | **ASK** (O-41) |
| I-20 | Khayal (form) | COURT | A Persian or Arabic word that "entered India through the medium of the Persian language"; shaped in the Delhi Sultanate and at Mughal courts [49] | Out as a form unless hers |
| I-21 | Violin in Carnatic music | COLONIAL_EUROPEAN (UNVERIFIED) | General knowledge | Ask if her tradition is Carnatic |
| I-22 | Khol or mridanga with karatals (Gaudiya kirtan) | NONE (UNVERIFIED) | No page opened | IN if hers |
| I-23 | Ghazal and qawwali | OUT (D-28) | The harmonium is "almost all Qawwals'" instrument [44] | Out |

### T-5. Source vetting checklist and verdicts

**The ten-step checklist** (log the answers in T8): (1) read the licence on the rights holder's own page, not the host's field; (2) is the uploader the performer or the label; (3) the work date and the country of first publication, then the country table below; (4) is it a digitisation of a commercial recording (then the label owns the master, whatever the uploader says); (5) ND means no sync, SA means avoid, and NC needs a decision on whether a free, unticketed premiere is non-commercial; (6) the exact CC BY credit line; (7) save the page, the licence page, the URL, the date and a SHA-256 of the file; (8) a second source for the date; (9) living voices are out of the premiere cut (D-05); (10) generic stand-ins only if hers (Principle 2).

**Verdicts read on 2026-10-19:**

| Source (host and item) | Licence field | What we could establish | Verdict |
|---|---|---|---|
| Asuchanti Brajabasi, 1906 (archive.org) | Public Domain Mark | An Odia song recorded in Calcutta in March 1906 for G&T; published before 1925 [26][16] | Best candidate for a public-domain vocal. A 1906 singer is not living, but W-46's "the dead ... voiced" may apply (open question 4). Needs a second date source |
| Mridangam sample, V. Raghuraman, 2004 (archive.org) | CC public-domain dedication | A performer's sample; the identity of the uploader and performer is UNVERIFIED [26] | Candidate for stroke sounds if provenance is shown |
| Veena items, L. Ramakrishnan (2004) and K. G. Vijayakrishnan (2003) | CC public-domain dedication | Living performers; a gmail-hosted uploader | Candidates only if the uploader is the performer; instrumental, not voice |
| Veena Raja Rao 1930s album | CC public-domain dedication | Out of Indian and UK term; US 100-year rule | India only |
| VintageSense Vintage Indian Music | CC BY 3.0 | Digitised commercial film songs, including 1968; a private uploader [26] | **Reject** |
| M. S. Subbulakshmi concert (1999); N. Ramani and R. Pitchumani Iyer (2000) | Public Domain Mark | Recordings of 1999 and 2000; performers' and label rights run [26] | **Reject** (wrong licence) |
| Hindi Bhajans and Gujarati Bhajan items | CC0 or Public Domain Mark | Uploader-asserted; performers unverified | Reject unless provenance is shown |
| Hindustani Alaps (CompMusic, archive.org) | CC BY-NC (the rights line says CC BY-NC 2.5) | Research recordings; vocal [26] | NC; D-05 |
| Saraga 1.5 (Zenodo) | CC BY-NC-SA 4.0 [29] | Open; vocal concerts | **Reject** (SA; voices) |
| Sanidha (Georgia Tech) | CC BY 4.0 [30] | Access by email and VPN; concerts include voices | Needs contact, which breaks secrecy; out |
| RaagaDhvani (SR) | CC BY-ND 4.0 | Flute | **Reject** (ND) |
| Great 78 Project | None | "research, teaching, and private study only" [25] | **Reject** as a licence |
| Raga Junglism tanpura drones [36] | None stated | "100% open-access and ad-free" is not a licence | **Reject** until a licence is stated |
| Freesound CC0 bell, temple ambience, conch, koel, cooker [37] | CC0 | Pages opened; licence confirmed | Allowed as labelled stand-ins |
| Freesound dhaak, Kolkata 2021 [37] | CC BY 4.0 | Credit required | Not hers on D-31's region; out |
| Freesound conch labelled for Hindu use; Kerala temple percussion (SR) | CC BY-NC | NC | Decide |
| BBC Sound Effects (SR) | RemArc: personal, educational or research | Commercial use needs a licence | **Reject** |
| Musopen | Unread (403) | n/a | Unknown |

**Country table (read 2026-10-19, not legal advice; for T10):**

| Item | India | US | UK | Canada |
|---|---|---|---|---|
| Works | Life plus 60 from the next year (s.22) [1] | Works published before 1931 are public domain in 2026 [R1] | Life plus 70 [R1] | Not read |
| Sound recordings | 60 years from the next year after publication (s.27) [1] | Foreign-published: before 1925 public domain; 1925 to 1946, 100 years; 1947 to 1956, 110 years; 1957 to 14 February 1972, to 15 February 2067 [16] | 70 years from publication [R1] | A film soundtrack is excluded from "sound recording" [20] |
| Performers | 50 years from the next year after the performance (s.38(2)) [1] | n/a | Not read | Not read |
| Public performance | IPRS for works; PPL (registered 2026-06-11), Novex, RMPL and ISRA for recordings and performers [4][5][6][7] | No general public-performance right for sound recordings: §106(6) and §114(a) [15] | PRS TheMusicLicence names film screenings; "the sound track accompanying a film shall be treated as part of the film" (s.5B(2)) [18][19] | Re:Sound tariffs (events, dated to 2015) [21]; SOCAN and Re:Sound through Entandem [22, SR] |
| Non-profit exemption | s.52(1)(j), (k), (l), (za) [1] | §110(4) for non-profit performance of nondramatic musical works, with no admission charge and no payment to performers, promoters or organisers [15] | Not read | Not read |

**Section 52 in India, in plain words.** The religious-ceremony clause (za) covers a bona fide religious ceremony; its Explanation adds a marriage procession and social festivities of a marriage. Clause (l) covers an amateur club's performance of a work to a non-paying audience, or for a religious institution. Clauses (j) and (k) cover educational institutions, residents' halls and non-profit clubs. A film premiere is none of these. A live aarti performed at the gathering might sit inside (za); the film's soundtrack does not. A government notice read (za) broadly, and the Delhi High Court-appointed expert found its scope "largely untested" [1][2][3]. This applies only if the premiere is in India (O-02). **UNVERIFIED; for the T10 consult.**

**The IPRS tariffs** (2025 scheme, in force from 1 April 2025 per its text) name live, DJ and background music. The index lists 25 tariffs and none names a film screening [4]. Whether any applies is a T10 question (W-55). Sangeet Dwar, a one-window portal for on-ground public performance, soft-launched on 2026-02-06 [8]. The Supreme Court stayed only the direction to pay at RMPL's tariff on 2025-04-21, not the holding [9, SR]. For Australia, OneMusic's film-screenings licence is needed "regardless of whether there's an entry fee", with a minimum of AUD 86.52 for APRA works in July 2026, as the sibling note records [R1, its source 51]; OneMusic itself returned 403 on 2026-10-19 [23].

### T-6. The name-free commission brief and the signed letter

Use this only after TD-L2c (Sunday 3 January 2027, D-03) and only for the April version, unless the maker rules otherwise. Never send it before the premiere. The brief reveals nothing about her or the film.

```
I am making a short tribute film. I need [1-3] original instrumental cue(s) of [60-120] seconds for [bansuri / veena / nadaswaram / ...], played by you.
Mood word: [shanta / karuna / vatsalya]; time of day: [dawn / dusk]; free tempo with a gentle pulse only if the cue needs one.
No voice. No AI-generated material. No samples of commercial recordings. If you play a traditional melody, name it and where you learned it; I need it to be public domain.
Deliver a dry stereo WAV, 48 kHz, 24 bit, plus the unedited take. Delivery within [10] days. Fee [  ] for [n] revisions.
I will send a one-page signed letter before payment: worldwide, perpetual, all media including public exhibition, online private links, archive and any later cinema or festival; your written consent to the performance being used in a film; credit as you prefer or anonymous; confidentiality until [date after the premiere]; no reuse of the cue.
I cannot say who the film is about or where it will be shown. It will be shown to an audience; the signed letter covers public exhibition.
```

**The seven s.19 clauses the letter must carry** (India; not legal advice; from the note's Template H and Q6): (i) identify each cue; (ii) list the rights (reproduce in the film, exhibit and communicate to the public in a hall, private online link, archive, a later cinema or festival); (iii) say "worldwide, perpetual", because silence means five years and India only (s.19(5), (6)); (iv) state the consideration (s.19(3)); (v) record the performer's written consent to incorporation in a cinematograph film and the royalty position on commercial use (s.38A(2)); (vi) state the credit (s.38B); (vii) note that an author's equal share of royalties for uses other than cinema-hall exhibition cannot be assigned away (s.19(9), (10)) [1]. Also: confidentiality past 27 February (D-07). A platform's default text, such as Fiverr's or Upwork's, is not this letter [70][71].

### T-7. Font decision table keyed on O-36 (Template J, condensed)

All families below are SIL OFL 1.1 in their own `OFL.txt` (read 2026-10-19 from github.com/google/fonts [73]). The full measured table is `research/devotional-sound-script-fixtures/font_table_2026-10-19.csv`, with the copyright line, the Reserved Font Name flag and the SHA-256 of each file.

| If O-36 (script) is | Test these first | Caption face to try first | Watch for |
|---|---|---|---|
| Hindi, Marathi, Sanskrit (Devanagari) | Devanagari (16 strings) | Mukta, or Tiro Devanagari Hindi or Marathi | Vedic marks if verses are shown; IAST fallback |
| **Gujarati (D-31)** | Gujarati (18 strings) plus the Devanagari verse strings for Sanskrit text | **Noto Sans Gujarati** for captions; Rasa or Baloo Bhai 2 for cards; Noto Serif or Tiro Sanskrit for verse | Digits (Hind Vadodara fails); Om sign (Farsan fails); boxes on IAST letters in some faces; Kumar One collapse; whether she reads Sanskrit in Gujarati or Devanagari script |
| Tamil | Tamil (6), plus Devanagari strings if prayers are in Sanskrit | Hind Madurai | Line width; Sri ligature differences |
| Malayalam | Malayalam (6) | Hind Kochi | Chillus; width |
| Telugu or Kannada | Telugu or Kannada (6) | Hind Guntur, or Noto Sans Kannada | Vowel signs |
| Bengali or Odia | Bengali or Odia (6 or 5) | Hind Siliguri, or Noto Sans Oriya | Reph and ra-zophola |
| Gurmukhi (Punjabi) | Gurmukhi (3) | Mukta Mahee | Gurmukhi is used by Hindus and Sikhs alike; Gurbani is out of scope |
| She prays in Sanskrit and speaks another language | Both scripts and a mixed line | The regional face plus Tiro Sanskrit | Use `<font face>` in the SRT |
| Not yet answered | Devanagari and the room's language | Mukta | Do not guess a region from a surname |

**Gujarati family notes (read 2026-10-19 [73][95]).** Noto Sans Gujarati is the default caption face: it carries digits, the Om sign and every conjunct string, and clears the 3.1% working floor at FontSize 23 (KA at 3.33%). Android's own Gujarati sans is the same family (AOSP `fonts.xml`, read 2026-10-19 [105]; her model's skin may differ: UNVERIFIED). **Hind Vadodara has no Gujarati digits**: a year such as સંવત ૨૦૮૩ falls back silently to FreeSerif, with the log line `Glyph 0xAE8 not found`; the foundry's own source has no digit glyphs either, so it is not a Google Fonts packaging difference [109]. **Farsan has no Om sign** (U+0AD0). **Kumar One collapses under libass** (53 px of ink for a 44-code-point line where HarfBuzz predicts about 1,900). Cause found in round 1: its TrueType `prep` program fails in FreeType ("execution context too long") because its `maxp` declares no storage or stack, in the Google Fonts build and the foundry's own build alike [108]. It is outlined title art only (T-10 item 2) and never a libass caption face. **Mogra's two caption lines touch** at FontSize 23. **Mukta Vaani draws conjuncts as a half form plus a base** (3 or 4 glyphs where the others give 1 or 2); a Gujarati reader must approve its look before it captions anything. **Rasa** and **Baloo Bhai 2** hold the IAST letters the cards need (ṇ ṛ ṣ included).

**Latin with IAST, for mixed lines:** Noto Sans, Noto Serif, Gentium Plus, Charis SIL and Cardo carry the full core set. Mukta, Tiro, Baloo 2 and Gotu carry Latin with IAST for mixed Indic lines. Poppins, Hind and Yatra One lack the Vedic svara marks U+0951 and U+0952 [note Summary 4].

**Anek and Catamaran.** Anek variable fonts have default instance Medium (500), and Catamaran's default is Thin (100). libass does not resolve them by plain family name and silently falls back (Inter, FreeSans, FreeSerif or Unifont) [note Summary 2]. Use a static instance (fontTools' instancer, with `--update-name-table`), or the name libass prints (for example "Anek Telugu Medium"). For a Reserved Font Name family (Arya, Charis SIL, Gentium Plus, Gentium Book Plus, Martel, Libre Baskerville, Lora, Merriweather, Playfair Display, PT Serif), do not rename or modify [74].

**T8 font row.** `asset_id=FN-nnn`, `type=font`, `title_or_description=<family> <style>`, `where_used=captions | cards | title art`, `how_obtained_and_by_whom=downloaded by the maker from github.com/google/fonts ofl/<dir> on <date>`, `rights_holder_and_contact=<designer>; the copyright line from OFL.txt`, `permission_type=SIL OFL 1.1`, `scope=rasterised in video; embedded in a DCP subtitle track only if OFL (FAQ 1.12)`, `fee=0`, `status=GRANTED`, `evidence_ref_and_sha256=the font file and OFL.txt, both hashes`, `notes=RFN y/n; static or variable default; scripts covered; the libass "fontselect:" line pasted`.

### T-8. The shaping gate (Template K, condensed)

1. **Gate order.** The font table and the fixture come first. The maker signs the settings card on Sunday 1 November only if: (a) every font has a T8 row with an `OFL.txt` hash; (b) the PC's `ffmpeg -buildconf` shows libass and libharfbuzz, and `ffmpeg -version` is n9.0 or later (or the burn-in uses the `ass` filter); (c) the A/B in item 6 shows the real caption path matches the complex frame; (d) the fixture for her script passes on the PC's burn-in, and Chromium on the PC and a phone browser pass for any live text.
2. **Pass criteria.** No dotted circle, no tofu, no visible halant where a conjunct belongs, no standalone reph, no unmoved short-i, no detached matra, no fallback face. Every `fontselect:` line maps to the intended file, and no `Glyph 0x... not found` line appears. A caption line's ink width is within about 10% of the HarfBuzz advance sum for that font.
3. **Three renderings, one row per script.** The libass burn-in on the PC, Chromium on the PC, and a phone browser: pass or the tell, and the string id. For a browser page, load the faces with `@font-face` from local files and set `font-synthesis: none`, so the browser cannot fake a weight or style [86]; which font was used must be read in developer tools (UNVERIFIED here).
4. **`drawtext`.** Use it for a card only after running with `-loglevel verbose` and seeing `shape: script=<tag>`. On any ffmpeg older than n9.0, do not use `drawtext` for Indic text. From n6.1.1 to n8.1.1 its HarfBuzz code sets the Latin script before shaping [77].
5. **Sidecar files.** SRT and VTT must be UTF-8: a UTF-16 SRT is an error in the subtitles filter, and a UTF-8 BOM is fine (the researcher's own run; note Q10). Every player shapes live text its own way; test the sidecar in the player she or a relative would use, or ship a PDF of the captions beside it (inference). Media3 ExoPlayer plays side-loaded SubRip [106]; YouTube takes .srt as plain UTF-8 and says "No style info (markup) is recognized" [107], so a `<font face>` run is for the burn-in only and a sidecar line should be single-script. Whether her gallery or WhatsApp applies a sidecar at all is undocumented in the pages read (UNVERIFIED).
6. **The A/B that replaces the log-line gate (about ten minutes).** Run Exercise 2 on `ab.srt` (non-sacred test syllables only). PASS: the default `subtitles` frame differs from the `simple` frame, and equals the `ass` frame. FAIL: the default equals `simple`. Never run the FAIL or `shaping=simple` render on a mantra, a deity's name, an aarti line or a Vedic verse; the broken frame is a deliberately wrong rendering and is kept only for the test syllables.
7. **Numerals.** Put one numeral string in the fixture for her script. Gujarati: સંવત ૨૦૮૩. A face without the digits falls back silently.

*Why the ffmpeg version matters (note Summary 1, Q10).* The `subtitles` filter has no `shaping` option before n9.0. On n5.1 to n8.1.1 it passes simple shaping to libass: measured pixel for pixel on 6.1.1, and read in the source for the other tags [96]. From n9.0 `shaping` sits in a `SHAPING_OPTIONS` macro expanded into both `ass_options` and `subtitles_options` at n9.0 and n9.0.2 (default -1, `auto`), so `subtitles` is complex by default. libass has required HarfBuzz since 0.15.0 [76], and HarfBuzz is used by Android, Chrome, ChromeOS, Firefox, Flutter and Microsoft Edge [80]; Apple platforms are not on that list, and iOS Safari's engine is UNVERIFIED. The maker's PC has the winget `ffmpeg` (Gyan's full build, latest release 9.0.2, dated 2026-09-19 [75]). Whether that Windows build shapes correctly is UNVERIFIED until the PC test. Kdenlive's bundled ffmpeg 8.1.1 has no `drawtext` at all (`research/toolchain.md`). Anything run on an ffmpeg older than n9.0 must use `ass` with an ASS file made from the SRT (`ffmpeg -i in.srt out.ass`, then set the style in the ASS file) [96].

### T-9. Caption size and width (Template L1, condensed)

At FontSize 23, libass sets the line pitch near 86 px (7.96 to 8.06% of 1080) for every face. What varies is the letter size. The project's existing caption floor is an x-height of 3.1% (`playbooks/cinematic-quality.md`, TY1). There is no defined floor for Indic letters. This playbook uses the height of the base letter KA of at least 3.1% of picture height as the working analogue (inference).

| Face | KA at FontSize 23 | FontSize for 3.1% | Width at 23, one 40 to 51 code-point sample (share of the 90% box) |
|---|---|---|---|
| Noto Sans Devanagari | 2.59% | about 27.5 | 47.5% |
| Noto Serif Devanagari | 2.22% | 32 | not measured |
| Mukta | 3.06% | 23.3 | 50.6% (Devanagari) |
| Tiro Sanskrit | 3.06% | 23.3 | 56.4% |
| Hind | 3.24% | 22 | not measured |
| Noto Sans Gujarati | 3.33% | 21.4 (23 is enough) | 60.5% (44 code points) |
| Noto Serif and Anek Gujarati | 2.78% | 25.6 | not measured |
| Rasa | 3.06% | 23.3 | not measured |
| Mukta Vaani | 2.96% | 24.1 | not measured |
| Noto Sans Telugu | 3.98% | not needed | 55.3% |
| Bengali faces | not mapped to one face (3.24 to 3.52 across three) | check on the PC | 63.0% |
| Kannada faces | not mapped (3.33 and 3.89) | check on the PC | 58.2% |
| Noto Sans Oriya | not mapped | check on the PC | 71.6% |
| Gurmukhi faces | not mapped (2.69 to 3.80) | check on the PC | 70.0% |
| Hind Madurai | not mapped | check on the PC | 88.9% |
| Noto Sans Tamil (Tamil faces 2.41 to 3.61 across six; mapping not explicit) | not mapped | check on the PC | **101.0% at 41 code points: over the box** |
| Noto Sans Malayalam | not mapped (2.50 to 3.80 across five) | check on the PC | **100.9% at 50 code points: over the box** |

The Tamil and Malayalam figures were measured with complex shaping on the n9.0.2 `subtitles` filter. A first run on 6.1.1, which shapes in simple mode, overstated the other figures and gave 104.9% for Tamil and 111.0% for Malayalam [note L1(d)]. Maximum code points in the box: Tamil 40 (Noto) or 46 (Hind Madurai); Malayalam 49; Gujarati 72 (Noto Sans) to 90 (Anek). **The rule:** a caption line must fit the 90% box at the chosen face and size. The count of 42 is a guide, not the rule. Break at word boundaries only (a hyphenated break is allowed only at orthographic syllable boundaries [79]).

**Phone geometry (inputs for the mobile track).** Assume a 6.1-inch 19.5:9 phone, about 64.9 by 140.7 mm (computed). Landscape, a 16:9 picture fitted to the height is about 64.9 mm tall; KA at 3.06% is about 2.0 mm, or about 19 arc minutes at 35 cm. Portrait, the letterbox is about 36.5 mm wide and KA is about 1.1 mm, or about 11 arc minutes. A 20:9 phone showing a 16:9 picture full-bleed crops about 10% of the picture height at the top and bottom (computed), so a caption in the 5% margin is half cut. The arc-minute threshold for comfortable reading is UNVERIFIED. The maker's reader, on her own phone, decides it.

### T-10. Bilingual caption and card lines (Template L3, condensed)

1. The caption track carries the room's language only, two lines, each within the box width, at 20 characters a second or slower (Netflix's Hindi and Tamil guides give 22 for adults and 18 for children [81][82]; W-18 says 20).
2. Her script appears as **title art**, shaped once with HarfBuzz and converted to outlines (SVG or PNG), so no player can fall back to another face.
3. A **verse or blessing card** is two lines: line 1 her script (or Sanskrit in Devanagari); line 2 the maker's plain line in the room's language. IAST is not a third line. It goes in the printed programme or the archive text. Hindu-frameworks caps the cards at two by default and never more than five.
4. A sung or spoken line in her language: no recorded voice before April (D-05).
5. A mixed Latin and Indic caption line: one family that holds both (Mukta, Tiro, Baloo 2 or Gotu), or `<font face="...">` around the other run in the SRT (verified in the note), or `{\fn...}` in ASS. Never one `FontName` for a whole file. The `<font face>` run works in the burn-in only: YouTube says "No style info (markup) is recognized" for a sidecar SRT [107].
6. Names: popular spelling on screen (Krishna, Lakshmi, Ganesha). A deity is named in a caption only if she is hers (O-38).
7. Phone render: lift the caption block, enlarge it, and check it at 200%. Do not restyle the venue file (W-18).
8. Sidecar SRT and VTT are UTF-8, with a `lang` tag per cue where the player supports it.

**Romanisation.** IAST (formalised 10 September 1894 at the Geneva Oriental Congress [84]) marks ā ī ū ṛ ṝ ḷ ḹ ṃ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ. ISO 15919 (2001) writes vocalic r as r with a ring below, anusvara as ṁ, and long ē and ō [83]. Popular spelling carries no marks. **Use popular spelling on screen. Use IAST only on a verse card if asked, and never ISO 15919.** Netflix's Hindi guide transliterates names where no approved translation exists and has "no specific rules for Sanskrit words" [81].

### T-11. Decision tables keyed on the unknowns (Template M, extended)

| Key | If the answer is | Then |
|---|---|---|
| O-36 home region and language (answered for D-31) | Gujarati; Pushtimarg Vaishnav family; deities as named in D-31; Android | Template N rows; Gujarati font set (T-7); `maker_rule=ASK` on I-19 and I-11; no raga for her tradition until a source names one; an Android check on the phone pass |
| O-36 script for Sanskrit verse (open) | Devanagari | Verse cards in Devanagari with Tiro or Noto Serif verse faces |
| O-36 script for Sanskrit verse (open) | Gujarati | Verse cards in Gujarati script; test the Gujarati verse strings; the Devanagari strings stay in the fixture only |
| O-37 sampradaya (answered as Pushtimarg in D-31) | Vaishnava | Invocations and forms as in hindu-frameworks F2 |
| O-38 shelf and kuldevi | A named deity | A raga named for that deity is a label only if the deity is hers (Bhairav and Bhairavi: Shiva and Devi; Durga: the Goddess; Brindavani Sarang: Krishna) |
| O-39 festivals she keeps | Holi, Janmashtami, Nagapanchami, Annakuta [89]; Navaratri and garba [93]; whether she keeps them: O-39 | Capture slots and stand-ins only for what she keeps; the hindu-frameworks note owns the dates |
| O-41 songs: a lullaby | Yes | MOTIF = the hum; place the tune (traditional or owned) before lock |
| O-41: a bhajan with a harmonium | Yes | `maker_rule = ASK` on I-19 |
| O-41: film devotionals | Yes | Label property; lean none (W-44) |
| O-41: lines said by heart | Yes | Best card candidate; no music needed |
| O-41: no songs | Yes | Silence and room tone |
| O-43 her phone model and player (open) | Not yet answered | Phone pass waits; once the model is known, the Android check runs on her phone by cable |
| O-42 deity images on a public screen (proposed; not decided here) | Belongs to the hindu-visual track | This playbook does not decide it |

### T-12. Patch list for existing playbooks

Each row names a section that was checked by heading on 2026-10-19. The changes are proposals for the maker and the orchestrator. None is applied in this sprint.

| File | Section (checked) | What changes |
|---|---|---|
| `playbooks/music-sound.md` | Step 5 "Build the cue map" (line 66) and its columns | Add the nineteen new columns of T-1 and the five rules. `maker_rule=ASK` blocks lock on 14 December. `origin_flag` takes the split flags `CHURCH` and `COLONIAL_EUROPEAN` (round 1) |
| `playbooks/music-sound.md` | Step 3 "Choose your music route" (line 51) | After the relative's public-domain performance: a sung recording is a living voice (D-05), so only instrumentals qualify before April. Add that ND audio is excluded because sync is an adaptation (CC 4.0 and CC 3.0 [31][33]); SA and NC rules |
| `playbooks/music-sound.md` | Step 2 "Decide the premiere country" (line 47) and the rights table | Add the country table (T-5), the s.52 reading, and the 2025 IPRS scheme and 2026 PPL, Novex and RMPL changes |
| `playbooks/music-sound.md` | Template A "Licence log header" (line 217) and Template E "Composer checklist" (line 288) | Add `tradition_origin` and `composition_status`; Template E gains the s.19, s.38A(2) and s.38B clauses of T-6 |
| `playbooks/music-sound.md` | Template I "Sound-recording notes for the room" (line 389) and Step 16 "Venue test" (line 140) | Add the capture list S-01 to S-20 (T-3). Add the phone-speaker model (300 Hz and 500 Hz high-pass) to the mono and 50% checks; room rumble, not the drone, is what vanishes. The placement of the phone check in Step 16 is a proposal, not verified. S-13 defaults to skip (use S-02) unless recording is openly allowed without asking anyone (round 1) |
| `playbooks/music-sound.md` | "Decisions you'll need to make" (line 426) and "Pitfalls" (line 472) | Replace "Suno's free tier is non-commercial" with the terms of 2026-08-10. Add ElevenLabs (film excluded below Enterprise), MusicGen (CC-BY-NC weights [63]) and ACE-Step [64] rows. Add "no AI voice of any devotional text" as a named rule. Pitfalls: "devotional means free" and "an uploader's licence is not a licence" |
| `playbooks/theatrical-delivery.md` | T8 "Rights-clearance log" (line 387) | Add the `type=font` guide (T-7), the Anek and Catamaran note, a `tradition_origin` column and a `phone_share` scope |
| `playbooks/theatrical-delivery.md` | T10 "Consult question list" (line 449) | Append questions 21 to 28 from the note's Template E4 |
| `playbooks/theatrical-delivery.md` | Step 6 "Burn in the captions" (line 74) and TD-3 (line 490) | W-18's "42 characters" gains a width rule: the line must fit the 90% box in the chosen face. UTF-8 only |
| `playbooks/format.md` | Step 8 "Harden the slice", captions bullets (lines 79 to 81) | `FontSize=23` is not font-independent for Indic faces: size by base-letter height (T-9). The `subtitles` filter shapes Indic text in simple mode before n9.0: use `ass`. Use `<font face>` for mixed lines. Add the portrait-phone caption lift for the mobile track. A sidecar SRT loses `<font face>` markup on YouTube [107]: per-run faces are for the burn-in only (round 1) |
| `playbooks/toolchain.md` | "Step 11: Captions" (line 156) | The `subtitles` filter shapes Indic text in simple mode on n5.1 to n8.1.1; burn Indic captions with `ass` on those versions; `drawtext` only on n9.0 or later after the fixture. The gate is the A/B of T-8 item 6 and the `fontselect:` lines. `fontsdir`, variable fonts and static instances |
| `playbooks/agent-pipeline.md` | "Project settings card" (line 169) and W-16 | Add the font rows and the libass and HarfBuzz check. Record that the PC's ffmpeg (Gyan full, 9.0.2) and Kdenlive's 8.1.1 differ, with the date the A/B passed |
| `playbooks/cinematic-quality.md` | TY1 (line 290), TY3 and "T2. Style bible" (line 299) | TY1's caption floor is stated for Latin x-height; add the Indic analogue (KA height 3.1%) and the per-face FontSize. TY3: every font has an `OFL.txt` and a hash. T2 gains the Indic families and the title-art-as-outlines rule. Kumar One is outlined title art only and Hind Vadodara is not used for dates (round 1) |
| `playbooks/film-story.md` | "Template 5. The 'who is she' brief" (line 281) and the cards (W-35) | A verse card is two lines: her script, then the maker's plain line. IAST is not a third line. Names in popular spelling |
| `playbooks/animated.md` | None | **No change from this note.** The deity iconography and the look of Hindu devotional imagery belong to the hindu-visual track |
| `playbooks/ai-imagery.md` | None | **No change from this note.** Gap: AI image models' rendering of Devanagari and Gujarati text was not researched (TODO(research)) |
| `research/hindu-frameworks.md` | Template B, F6, O-36 and Template C | `season_or_time_of_day` is the join field. F6's harmonium flag is answered by I-19 (now `COLONIAL_EUROPEAN`) and the open question. The raga set per darshan is given by two sources that disagree [97][100]; no source maps a season to a raga set or names a tala per darshan |

**Proposed `DECISIONS.md` rows (for the orchestrator; not entered here).**
- **W-16 and W-21:** burn Indic captions with `ass` on ffmpeg older than n9.0 (the `subtitles` filter shapes in simple mode there). Static instances only for variable fonts. The libass `fontselect:` line goes in the T8 notes. No Gujarati caption face without digits for dates.
- **W-18:** a width rule for Indic scripts (the line must fit the 90% box in the chosen face). The "42 characters" count is a guide.
- **W-44:** ND-licensed audio excluded. A sung recording is a living voice under D-05. An AI bed has almost no home in the premiere cut. **Conflict to resolve:** W-44 lists "a relative's public-domain performance" as a source, which D-05 bars for a sung recording before the premiere.
- **A new O-row** for the harmonium and tabla ruling (O-41).
- **O-36 to O-45:** enter the proposed rows from `reviews/04-hindu-mobile-briefs-review.md` in `DECISIONS.md`. O-43 (her phone model) and O-42 (deity images) are not yet rows.

---

## What we leave out (the Hindu-only rule in practice)

The rule is D-28: "Indian themes" always means Hindu themes, and no Mughal, other Islamic or Christian motifs ever appear. Where a motif's origin is shared or ambiguous, we flag it and default to leaving it out. The table below turns that into things the film does not use.

| What | Why | Rule |
|---|---|---|
| Ghazal and qawwali | Sufi and Persianate forms (D-28). The harmonium is their usual instrument too [44] | Out |
| Khayal as a named form | A Persian or Arabic word; shaped in the Delhi Sultanate and at Mughal courts [49] | Out unless hers |
| Sitar and sarod as showpieces | Court histories [46] | Out unless a family source says they were hers |
| Shehnai, santoor | Persian origin or name [48][54] | Shehnai: ASK. Santoor: out |
| Mughal-era pictures as images | The ragamala idea of a raga-by-hour is old and Hindu in subject, but the images are Mughal and Deccani in lineage (note, hindu-frameworks flag 14) | The raga idea may be a label. The images are out |
| Raga names on screen (Yaman, Malhar, Todi, Bilaval) | Several names carry Persian-court or Akbar-court attributions on the pages read [39][41] | No raga name on screen. Use Carnatic Kalyani or no name |
| Desh as a motif | Political and Tagore-era associations; "Vande Mataram" uses it [39] | Avoid |
| Gurbani, Sikh kirtan, Jain and Buddhist chants (including a Mahabodhi recording) | Dharmic but not Hindu | Out unless the maker rules |
| Shyama Sangeet by Tagore or Nazrul | The composers are outside the Shakta line | Restrict to Ramprasad and the Shakta line |
| "Raghupati Raghava Raja Ram" with the "Ishwar Allah tere naam" line | The line's presence in the version is UNVERIFIED | Leave out until the maker picks a version |
| Film devotionals and modern album settings (T-Series, Saregama, Times Music) | Owned lyrics, tunes and recordings (W-44) | Lean none |
| AI-made devotional songs; any AI voice of a real singer | D-16; W-44; devotional communities' unease [66][67] | Out |
| Generic "Indian" stand-ins (a temple bell, a dhak, a koel, a sitar pad) | Principle 2: a generic Indian sound is out unless it is hers | Only as a labelled fallback where she cannot be recorded |
| A stock "Krishna flute" bed | The flute is the deity's emblem, placed or withheld darshan by darshan [99]; one tagged page says her sampradaya's temple custom also keeps the bansuri out of the sanctum [88], which a 2026 paper's instrument list contradicts [97] (UNVERIFIED, contested) | Do not buy. Ask (O-41) |
| Sung aarti, kirtan or garba recordings | Living voices (D-05) | April version only |
| Any aarti text whose author is not read | Rights and attribution unknown (N7) | Do not caption |
| A deity's name in a caption | Names are only hers (O-38) | Only if she is hers |
| The S-17 dhak drum | D-31 places her region outside Bengal | Out unless she says otherwise |
| Reference images and stock "Indian" pictures | Stock results can show Mughal or Islamic architecture (general knowledge; not checked in the note) | Check each image's subject and origin before use. A check, not a sourced claim |

---

## Decisions you'll need to make

Each decision lists the options and our lean. The lean is a suggestion for you to confirm, not a decision.

**D1. Does D-28 cover motifs only, or also the faith of performers and composers?** (Open question 5.)
- *Options:* (a) motifs and the world of the film only; (b) also the faith of the performers and composers of any recording or tune we use.
- *Our lean:* (a). Many film bhajans are by Muslim composers, lyricists or singers (general knowledge, UNVERIFIED here). Under (b) the rule would bar most of the Indian film-music catalogue. Decide before the cue map (Saturday 14 November).

**D2. Which script for Sanskrit verse? (O-36, open.)**
- *Options:* Devanagari for verse cards and Gujarati for her spoken lines; Gujarati for everything; Devanagari for everything.
- *Our lean (inference):* Devanagari for Sanskrit verse (the note's Template J names Noto Serif or Tiro Sanskrit for verse), and Gujarati for her spoken lines, until she says her family reads Sanskrit in Gujarati script. Test both on the settings card (Sunday 1 November).

**D3. Harmonium, tabla and bansuri (O-41).** (Open question 2 and question 12.)
- *Options:* (a) keep them because they are hers; (b) take them out of the film's sound; (c) ask her proxy case by case.
- *Our lean:* (c), with the default `ASK`, which means silence or room tone in the render until ruled. The harmonium arrived in the colonial period by a route the sources call "possibly" missionary, the tabla's origin is disputed, and three sources put the harmonium in her sampradaya's temple music [88][97][98], while the bansuri's exclusion rests on one tagged page and is contested [88][97]. Ruling due Monday 14 December.

**D4. Sitar, sarod, santoor and khayal (out by default); shehnai, tanpura, ektara and the Carnatic violin (`ASK`).** (Open question 3.)
- *Options:* out by default; `ASK` (silence in the render until ruled); in only if a family source says they were hers.
- *Our lean:* out by default for sitar, sarod, santoor and khayal, as the note recommends; `ASK` for the shehnai, tanpura, ektara and Carnatic violin, exactly as T-4 and the skill say. Ruling due Monday 14 December.

**D5. Does a historic recording of a deceased singer count as a voice under D-05 and W-46?** (Open question 4; for example the 1963 Suprabhatam recording.)
- *Options:* (a) allow it as music where the country's term has run out; (b) allow it with a cited archive and a country-by-country check; (c) keep it out.
- *Our lean:* (c) for the premiere cut. W-46 bars "the dead ... voiced" and the recording is a famous singer's voice, which the room would hear. Put the question to T10 in any case. The 1963 recording is out of India's term on our computation (published 1963; term ends 2023 [1][13]) but protected in the US until 2067-02-15 and in the UK to 2033 [16][R1]. The premiere country decides.

**D6. Does D-05 cover a temple's chanting crowd at a distance, or a radio?** (Open question 4.)
- *Options:* out entirely; or an unintelligible distant wash only.
- *Our lean:* out entirely for the premiere. Ask T10 whether any wash is allowed.

**D7. The premiere country (O-02, TD-7).**
- *Options:* India; the US; the UK; Canada; Australia; another country.
- *Our lean:* answer it by Sunday 25 October. Every term in T-5 changes with it, and a 1930s Indian record can be free in one country and owned in another [note Q5].

**D8. The Gujarati caption face and the card faces.**
- *Options:* Noto Sans Gujarati (captions); Rasa or Baloo Bhai 2 (cards); Mukta Vaani only after a Gujarati reader approves its half forms; Kumar One as outlined title art only (its libass collapse traces to a font defect; the PC's FreeType is untested).
- *Our lean:* Noto Sans Gujarati for captions, Rasa for a card with both a Gujarati line and an IAST line. Hind Vadodara is not used for dates. Decide on Sunday 1 November.

**D9. Live-text captions for her phone.**
- *Options:* sidecar SRT and VTT only; or sidecar files with a PDF of the captions beside them.
- *Our lean:* both (inference). The live text is shaped by her player's own fonts, and her Android model is not yet known (open question 8); Android's system Gujarati sans is Noto Sans Gujarati [105], and her model's skin may differ.

**D10. Raga names.**
- *Options:* never print one; print Carnatic Kalyani where a name is needed; print a raga name whose recording metadata carries it.
- *Our lean:* never print one.

**D11. Contacting the Sanidha project.** (Open question 9.)
- *Options:* contact now; wait until after the premiere.
- *Our lean:* wait. Access needs an email and a VPN account, which breaks secrecy, and its vocal content fails D-05 anyway.

**D12. The consult budget and the T10 list (O-04, W-55).** The list now has eight music questions (T10 items 21 to 28).
- *Options:* one paid hour by Friday 4 December with the full list; or a shorter list.
- *Our lean:* one hour with the full list, asked as a hypothetical once the country is known.

**D13. Her phone (O-43 and open question 8).**
- *Options:* ask for the model and the player now; or run the phone pass on a stand-in Android device.
- *Our lean:* ask by Sunday 1 November, so the phone caption pass and the speaker sweep run on her class of device, by cable.

**D14. AI music.**
- *Options:* closed; a locally run, labelled instrumental drone under voice only, April at the earliest; a paid Enterprise contract.
- *Our lean:* closed for the premiere. Stable Audio 3.0, run locally, has community-licence terms that allow commercial use under USD 1M of annual revenue [61]; the note treats it as the only local route. It still has almost no home in the premiere cut.

**D15. The burn-in path on the PC.**
- *Options:* the project's own `subtitles=` burn, only if the PC A/B (T-8 item 6) passes; or the `ass` filter on an ASS file made from the SRT.
- *Our lean:* `ass`, unless the PC A/B passes for `subtitles`. Decide on Sunday 1 November.

**D16. Deity images on a public screen (O-42).** Not decided here; the hindu-visual track owns it.

---

## Pitfalls

- **Silent font substitution.** A variable font with a non-Regular default (Anek, Catamaran) resolves to Inter, FreeSans, FreeSerif or Unifont without any warning on the picture. The proof is the `fontselect:` line, not the look [note Summary 2].
- **The `Shaper:` line is not a gate.** It prints `(COMPLEX)` on every build, including the ones that run simple shaping. Only the pixel test (Exercise 2) tells you [note Summary 1].
- **Before n9.0, `subtitles` breaks conjuncts silently.** Devanagari ksha, tra, jna and shri, and the reph in dharma, come out as separate glyphs. The tell is a visible halant in क्ष and ज्ञ, a standalone reph in धर्म, and an unmoved short-i in कि क्षि [note Q10].
- **`drawtext` in n6.1.1 to n8.1.1 is also broken for Indic text**: it sets Latin before shaping [77].
- **Hind Vadodara has no Gujarati digits.** Dates fall back silently to FreeSerif. The foundry's own source has none either [109].
- **Farsan has no Om sign; Kumar One collapses under libass (a defective `prep` and `maxp` pair [108]; outlined title art only); Mogra's lines touch; Mukta Vaani draws half forms.** Test each face on the PC before use.
- **The 42-character rule breaks in Tamil and Malayalam.** Measure the width, not the count.
- **FontSize 23 is not one size.** The base letter is 2.22% of the picture in Noto Serif Devanagari and 3.98% in Noto Sans Telugu. Size each face by its own KA height.
- **"Devotional means free" is wrong.** Check the words, the tune, the arrangement, the recording and the performance separately.
- **An uploader's licence field is not a licence.** VintageSense's CC BY 3.0 label sits on 1968 film songs; the Great 78 Project says "research, teaching, and private study only" [25][26].
- **An ND licence cannot go under picture.** CC 4.0 says a recording "synched in timed relation with a moving image" is always Adapted Material [31]. CC 3.0 calls the same act an Adaptation [33]. BY-ND and BY-NC-ND audio is out.
- **AI music terms.** Suno's free output is for "lawful, personal and non-commercial purposes" (terms revised 2026-08-10, effective 2026-09-03) [58]. Udio's output is personal and non-commercial only, and downloads have been off since the 2025-10-29 settlement [60, SR]. ElevenLabs Music excludes film, TV and radio below the Enterprise tier (updated 2026-10-09) [59]. MusicGen's weights are CC-BY-NC [63]. Lyria 3 has Hindi lyric support, and every track carries SynthID [62, SR]. None is shown to handle raga grammar [68].
- **A phone loses the body of a drone.** A crude phone model with a 300 Hz or 500 Hz high-pass keeps about 96% of a real tanpura's energy above 300 Hz, but loses room rumble and low "temple ambience" by about 20 dB [note Summary 14]. This model is a rule of thumb (about 250 to 500 Hz [87]); the maker's own sweep decides.
- **Live-text (sidecar) captions are shaped by the player.** Test the sidecar in her player. YouTube drops SRT markup [107].
- **Naming a raga on screen** is a claim a teacher or a metadata field must back. Never print one unless it does.
- **A hum is not free.** The maker's hum of a tune that is a film or album song is a performance of an owned composition (S2 in the note's Template E1). "A hum is free" is not a rule.
- **The sung voice in W-44.** "A relative's public-domain performance" as a source conflicts with D-05 for sung recordings. Use instrumentals only before April.
- **Sanskrit and Gujarati strings copied from memory.** Copy every string from its source and mark any transliteration the source does not give as TODO(research).

### Gaps the research did not close (TODO(research))

- **The maker's three renderings** (Windows ffmpeg burn-in, Chromium on the PC, a phone browser including her Android) have not been run. Every shaping result comes from Linux builds (ffmpeg 6.1.1 and a source-built n9.0.2, libass 0.17.1, HarfBuzz 8.3.0). Whether the Windows build's `subtitles` shapes correctly is UNVERIFIED. The A/B in T-8 item 6 (on `ab.srt`) settles it; record the `Raster: FreeType` and `Shaper:` debug lines with the result.
- **Kumar One's libass collapse** is explained (round 1): a hinting program that fails in FreeType; a newer libass, other FreeType releases and the Windows build are untested [108].
- **Mukta Vaani's half-form conjuncts** need a Gujarati reader's judgement.
- **Which Gujarati font Android ships:** AOSP maps Gujarati to Noto Sans Gujarati [105]; her model's skin and her player are UNVERIFIED (O-43).
- **Raga sets per darshan or season** for her tradition: two sources give sets per darshan and they disagree [97][100]; none maps a season to a raga set or names a tala per darshan. `raga_id` stays blank.
- **Aarti authorship** for "Jai Adhya Shakti" and the Shiva, Lakshmi and "Jai Ganesh Deva" aartis was not found in round 1 either; only the Ganesh aarti "Sukhakarta Dukhaharta" (Samarth Ramdas) was added [103].
- **The Khare arrangement's composer dates** were not found in round 1 either [113].
- **The harmonium statement** is now confirmed by [97][98]; **the bansuri statement** rests on one tagged Wikipedia page [88] and is contested [97]. No printed source was read (Gaston [102]).
- **The Pushtimarg home practice** of daily sevā and its sound was not read.
- **Recording rules in havelis and temples:** none found that allow recording without asking; the only rule found bars phones and cameras at Nathdwara [100][110]. Each temple's own rule governs.
- **Legal readings:** the reach of s.52 (za); the 60-year terms; performer rights and the waiver of s.38B moral rights; ND and sync; editions of old poets; the US and UK pre-1972 terms; the PRO questions. All of these are leads for the T10 consult and depend on the premiere country (O-02, TD-7).
- **Film exemplars** of raga, bhajan or Indic-script practice were not researched. The search budget ran out.
- **Sync desks and Gujarati film or garba labels** were not reached (404 or blocked).
- **Musopen, OneMusic (403 today), Wikimedia Commons and the Fiverr and Upwork terms** were not read.
- **AI image tools and Indic lettering** (how image models render Devanagari and Gujarati text on a plate) were not researched.
- **Her Android model and her player** (open question 8; O-43).
- **Deity iconography**, the look of Hindu devotional imagery, and O-42 belong to the hindu-visual track.
- **The sibling track's Exercise 7** in `playbooks/mobile-delivery.md` ("The Gujarati shaping check on the PC") overlaps Template K here. Reconcile the two before either is run.

---

## Best references (8)

1. **The Copyright Act, 1957** (the Copyright Office's PDF) [1]. Sections 2(f), 13(4), 17, 19, 22, 27, 38, 38A, 38B and 52(1)(j), (k), (l), (za). Opened. The primary text for every India term in this playbook.
2. **SIL Open Font License FAQ** [74]. FAQ 1.1 (video titling is a listed use), 1.11 and 1.12 (embedding), and 3.1 and 5.3 (Reserved Font Names). Opened.
3. **FFmpeg, `libavfilter/vf_subtitles.c` at the tags listed** [96]. Where the `shaping` option appears and when. Opened, with the controlled A/B in the fixture.
4. **FFmpeg, `libavfilter/vf_drawtext.c` and `doc/filters.texi`** [77]. The HarfBuzz script setting, tag by tag. Opened.
5. **W3C, Indic Layout Requirements (Working Draft)** [79], dated 2020-05-29. Line breaking and the danda rules. Opened.
6. **Microsoft, "Developing OpenType Fonts for Devanagari Script"** [78], dated 2022-06-24. The reph and the dotted circle. Opened.
7. **Netflix, Hindi Timed Text Style Guide** [81], change log dated 2025-10-17. The character and reading-speed limits, and the transliteration rule. Opened. Its counts are characters, not widths.
8. **Wikipedia, "Pushtimarga"** [89]. A starting map of her tradition's calendar, darshans and festivals. Opened in full (the last 2,828 characters hold only footer text). Treat it as a pointer, not a primary source; cross-check against [97][99] and [88], which carries a maintenance tag.

---

## Sources

Format: `[n] title — URL — date — status`. The numbers are the researcher's. *opened* means the page was fetched and read on 2026-10-19 (or the tool run by the researcher). *SR* means a search-result summary only. Fetch-tool summaries are noted where they apply. Only the sources this playbook cites are copied here.

[1] The Copyright Act, 1957 (the Copyright Office's PDF file named copyrightrules1957.pdf; the text ends with a note to Act 7 of 2017) — https://www.copyright.gov.in/documents/copyrightrules1957.pdf — read 2026-10-19 — opened.
[2] Arul George Scaria, "Reading Sec. 52(1)(za) of the Copyright Act 1957" (abstract; InfoJustice posting) — https://infojustice.org/archives/44930 — 2022-11-14 — opened (abstract only).
[3] "No Music License Required for Marriage Ceremonies: DPIIT Clarifies" (Lexology) and the Copyright Office notice — https://www.lexology.com/library/detail.aspx?g=eb72f71d-be44-4e6c-87d8-aca822654367 ; https://www.copyright.gov.in/Latest_Notice37.aspx ; https://www.theippress.com/2022/12/10/analyzing-the-contentious-section-521za-of-the-copyright-act-1957/ — SR (fetch 403 and 503).
[4] IPRS, "Tariff Schemes", Annexure A to the Notice of the 55th AGM — https://iprs.org/wp-content/uploads/2025/08/Annexure-A-to-55th-AGM-Notice-Tariff-Scheme.pdf — 2025 (in force from 1 April 2025 per its text) — opened (PDF text extracted locally).
[5] Amit Gurbaxani, "PPL licensing ruling shakes up India's performance rights sector", Music Ally — https://musically.com/2025/04/17/ppl-licensing-ruling-shakes-up-indias-performance-rights-sector/ — 2025-04-17 — opened.
[6] "Indian performance rights organisation PPL reinstated as a copyright society", Music Ally — https://musically.com/2026/06/22/indian-performance-rights-organisation-ppl-reinstated-as-a-copyright-society/ — 2026-06-22 — opened.
[7] "PPL India reinstated as a copyright society after a 12-year absence", Music Business Worldwide — https://www.musicbusinessworldwide.com/ppl-india-reinstated-as-a-copyright-society-after-a-12-year-absence/ — 2026-06-24 — opened.
[8] "Single-window music licensing platform Sangeet Dwar has launched", Music Ally — https://musically.com/2026/02/06/single-window-music-licensing-platform-sangeet-dwar-has-launched/ — 2026-02-06 — opened.
[9] LiveLaw, "Supreme Court Stays Delhi HC Direction in PPL's Plea" — https://www.livelaw.in/top-stories/copyright-claim-over-songs-in-restaurants-supreme-court-stays-delhi-hc-direction-in-phonographic-performance-ltds-plea-289923 — 2025-04 — SR.
[12] Wikipedia, "Om Jai Jagdish Hare" (opened) and "Shardha Ram Phillauri" (dates from a search summary) — https://en.wikipedia.org/wiki/Om_Jai_Jagdish_Hare ; https://en.wikipedia.org/wiki/Shardha_Ram_Phillauri — read 2026-10-19.
[13] K. Balakumar, "A recitation that many Hindu households wake up to", Swarajya — https://swarajyamag.com/amp/story/culture/a-recitation-that-many-hindu-households-wake-up-to — 2023-07-21 — opened.
[14] Wikipedia, "Hanuman Chalisa"; Swarajya on T-Series' Hanuman Chalisa — https://en.wikipedia.org/wiki/Hanuman_Chalisa ; https://swarajyamag.com/amp/story/culture/three-billion-views-for-hanuman-chalisa-on-t-series-youtube-channel-how-hindu-devotional-songs-conquered-the-internet — SR.
[15] 17 U.S.C. §§106, 110 (copyright.gov) and §114 (Cornell LII) — https://www.copyright.gov/title17/92chap1.html ; https://www.law.cornell.edu/uscode/text/17/114 — opened.
[16] Cornell University Library, "Copyright Term and the Public Domain in the United States" — https://guides.library.cornell.edu/copyright/publicdomain — "Last Updated: Jun 11, 2026" — opened.
[18] PPL PRS, "Pubs & Bars Music Licence" — https://pplprs.co.uk/themusiclicence/sectors/pubs-bars/ — cost examples "correct as of September 2026" — opened.
[19] Copyright, Designs and Patents Act 1988, s.5B — https://www.legislation.gov.uk/ukpga/1988/48/section/5B — opened.
[20] Copyright Act (Canada), s.2 — https://laws-lois.justice.gc.ca/eng/acts/c-42/section-2.html — opened.
[21] Re:Sound, Tariffs — https://www.resound.ca/tariffs — opened.
[22] Entandem, SOCAN and Re:Sound joint licensing (CAPACOA guide) — https://capacoa.ca/en/healthy-sector/copyright/what-you-should-know/ — SR.
[23] OneMusic Australia, Film Screenings licence — quoted in `research/music-sound.md` (its source 51, July 2026); not opened by the researcher (onemusic.com.au returned 403 on 2026-10-19) — the AUD 86.52 minimum comes from that note.
[25] Internet Archive, "78rpm Records Digitized by George Blood, L.P." (the Great 78 Project), collection metadata — https://archive.org/metadata/georgeblood — read 2026-10-19 — opened.
[26] Internet Archive item metadata read 2026-10-19 for `www.VintageSense.com-Vintage-Indian-Music-65n`, `Mridangam_sample1`, `LR_kIravANI`, `DrKGVijayakrishnan_bhairavidemo`, `HindustaniAlaps`, `asuchantibrajabasisei`, `VeenaRajaRao1930sAlbum`, `m.s.-subbulakshmi-carnatic-concert`, `classical-music-flute` — https://archive.org/metadata/<identifier> — opened. (Uploader details are deliberately not copied here.)
[29] Saraga: research datasets of Indian Art Music, v1.5, Zenodo — https://zenodo.org/records/4301737 — modified 2021-04-18 — opened.
[30] Sanidha, Georgia Tech — https://ccml.gtcmt.gatech.edu/data/Sanidha/ — opened.
[31] Creative Commons Attribution 4.0 legal code — https://creativecommons.org/licenses/by/4.0/legalcode — opened.
[33] Creative Commons Attribution 3.0 Unported legal code — https://creativecommons.org/licenses/by/3.0/legalcode — opened (the summariser returned the "Adaptation" definition and the synching sentence).
[36] Raga Junglism, "Tanpura samples: divine Indian drones in all 12 keys" — https://ragajunglism.org/tanpuras — opened.
[37] Freesound pages opened 2026-10-19: https://freesound.org/people/ganiket/sounds/466652/ (CC0); https://freesound.org/people/kylecutsfilms/sounds/443383/ (CC0); https://freesound.org/people/RoofDog/sounds/78974/ (CC0); https://freesound.org/people/AnneshaGhosh/sounds/592301/ (CC BY 4.0); https://freesound.org/people/SamuelGremaud/sounds/462922/ (CC0); https://freesound.org/people/ramblinglibrarian/sounds/460466/ (CC0); https://freesound.org/people/Calcuttan/packs/11448/ (pack page, no licences shown). SR: an Odiasites.com conch (CC BY-NC) and a temple percussion clip (CC BY-NC 4.0).
[39] Wikipedia pages read 2026-10-19: Raga https://en.wikipedia.org/wiki/Raga ; Bhairav, Todi, Bhoopali, Bhimpalasi, Yaman, Malkauns, Bageshri, Bhairavi (Hindustani), Desh, Malhar, Puriya Dhanashree, Alhaiya Bilawal, Brindavani Sarang, Durga, Hamsadhvani, Madhyamavati, Kalyani, Mohanam, Sankarabharanam, Kharaharapriya, Ananda Bhairavi, Reetigowla, Sindhu Bhairavi — all at https://en.wikipedia.org/wiki/<title> — opened. (Some claims are marked as needing citations; used here for the tradition's stated associations.)
[41] raag-hindustani.com, Yaman — https://raag-hindustani.com/Yaman.html — opened.
[44] Wikipedia, "Indian harmonium" — https://en.wikipedia.org/wiki/Indian_harmonium — opened (flagged as needing citations).
[46] Review of Allyn Miner, *Sitar and Sarod in the 18th and 19th Centuries* (Cahiers d'ethnomusicologie, OpenEdition) — https://journals.openedition.org/ethnomusicologie/1463?lang=en — opened (French).
[47] Wikipedia, "Tabla" — https://en.wikipedia.org/wiki/Tabla — opened.
[48] Wikipedia, "Santur" — https://en.wikipedia.org/wiki/Santur — opened.
[49] Wikipedia, "Khyal" — https://en.wikipedia.org/wiki/Khyal — opened.
[50] Wikipedia, "Ektara" — https://en.wikipedia.org/wiki/Ektara — opened.
[51] Wikipedia, "Pakhavaj" — https://en.wikipedia.org/wiki/Pakhavaj — opened.
[52] Wikipedia, "Tanpura" — https://en.wikipedia.org/wiki/Tanpura — opened.
[53] Wikipedia, "Nadaswaram" — https://en.wikipedia.org/wiki/Nadaswaram — opened.
[54] Wikipedia, "Shehnai" — https://en.wikipedia.org/wiki/Shehnai ; Darbar, "The Shehnai: a Folk Instrument Elevated to Classical Music" — https://darbar.org/the-shehnai-a-folk-instrument-elevated-to-classical-music/ — SR.
[56] Wikipedia, "Annamacharya" — https://en.wikipedia.org/wiki/Annamacharya — opened.
[58] Suno, Terms of Service — https://suno.com/terms — "Date of Last Revision: August 10, 2026"; "Effective Date: September 3, 2026" — opened 2026-10-19.
[59] ElevenLabs, Music Terms — https://elevenlabs.io/music-terms — "Last updated: 09 October 2026" — opened 2026-10-19.
[60] Udio, Terms of Service — https://www.udio.com/terms-of-service — "Last Revised on November 12, 2025" per a repository capture; the page's visible text did not load on 2026-10-19; downloads and launch status from press summaries (SR) — https://undetectr.com/blog/udio-review-2026 and similar.
[61] Stability AI, Community License — https://stability.ai/license — footer "© Stability AI Ltd, 2026" — opened 2026-10-19.
[62] Google, Generative AI Additional Terms of Service — https://policies.google.com/terms/generative-ai — "Last Modified: August 9, 2023" — opened; Lyria 3 in the Gemini app — https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/ ; https://9to5google.com/2026/02/18/gemini-app-music-lyria-3/ — 2026-02-18 — SR.
[63] Meta AudioCraft, MusicGen model card — https://raw.githubusercontent.com/facebookresearch/audiocraft/main/model_cards/MUSICGEN_MODEL_CARD.md — opened.
[64] ACE-Step README — https://raw.githubusercontent.com/ace-step/ACE-Step/main/README.md — opened.
[66] ISKCON News, "Bhakti Song Contest: Using AI and Music for Krishna Conscious Outreach" — https://iskconnews.org/bhakti-song-contest-using-ai-and-music-for-krishna-conscious-outreach/ — 2025-09-05 — opened.
[67] News On AIR, "Prasar Bharati Denies Collaboration with AI Band Trilok" — https://www.newsonair.gov.in/prasar-bharati-denies-collaboration-with-ai-band-trilok — 2025-12-12 — opened.
[68] AI and raga evidence: AIMC 2023, "Introductory Studies on Raga Multi-track Music Generation of Indian classical music using AI" — https://aimc2023.pubpub.org/pub/4pcwrxuo ; IJRASET review — https://www.ijraset.com/research-paper/ai-in-indian-classical-music ; MusicSeed and RaagEngine vendor pages — https://www.musicseed.ai/blog/indian-classical-music-generator ; https://raagengine.com/indian-classical-music-ai/ — SR.
[70] Fiverr Help Center, FAQs for clients — https://help.fiverr.com/hc/en-us/articles/360011454477-FAQs-for-clients — SR (403 on fetch).
[71] Upwork's default work-product terms (terms.law summary) — https://terms.law/2023/07/23/upworks-terms-ownership-of-freelancers-work-product/ — SR.
[73] github.com/google/fonts, `ofl/<family>/OFL.txt` and `METADATA.pb` for each family, e.g. https://raw.githubusercontent.com/google/fonts/main/ofl/mukta/OFL.txt — main branch read 2026-10-19 — opened.
[74] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — opened.
[75] Gyan Doshi, FFmpeg Windows builds — https://www.gyan.dev/ffmpeg/builds/ — release 9.0.2, 2026-09-19; winget names; essentials library list — opened; re-read 2026-10-19: 9.0.2 still the latest release.
[76] libass Changelog — https://raw.githubusercontent.com/libass/libass/master/Changelog — opened.
[77] FFmpeg `doc/filters.texi` at release/6.1, 7.1, 8.0 and master, and `libavfilter/vf_drawtext.c` at the tags n5.1 to n9.0.2, release/8.1, release/9.0 and master — https://raw.githubusercontent.com/FFmpeg/FFmpeg/<ref>/... — opened 2026-10-19.
[78] Microsoft, "Developing OpenType Fonts for Devanagari Script" — https://learn.microsoft.com/en-us/typography/script-development/devanagari — 2022-06-24 — opened.
[79] W3C, Indic Layout Requirements (Working Draft) — https://www.w3.org/TR/ilreq/ — 2020-05-29 — opened.
[80] HarfBuzz README — https://raw.githubusercontent.com/harfbuzz/harfbuzz/main/README.md — opened.
[81] Netflix, Hindi Timed Text Style Guide — https://partnerhelp.netflixstudios.com/hc/en-us/articles/115003196707 — change log 2025-10-17 — opened.
[82] Netflix, Tamil Timed Text Style Guide — https://partnerhelp.netflixstudios.com/hc/en-us/articles/4481912003987-Tamil-Timed-Text-Style-Guide — change log 2025-07-07 — opened.
[83] Wikipedia, "ISO 15919" — https://en.wikipedia.org/wiki/ISO_15919 — opened.
[84] Wikipedia, "International Alphabet of Sanskrit Transliteration" — https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration — opened.
[86] MDN, `font-synthesis` — https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis — opened.
[87] Phone-speaker bass cut-off: a speech-processing figure and a patent background (about 500 Hz and "below approximately 250 Hz") — https://www.researchgate.net/figure/Typical-frequency-response-of-smartphone-loudspeaker_fig1_221536353 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9596530 — SR (a rule of thumb, not a measured phone).
[88] Wikipedia, "Haveli Sangeet" — https://en.wikipedia.org/wiki/Haveli_Sangeet — read 2026-10-19 — opened (fetch-tool summary). Tagged as lacking reliable references; several claims "better source needed" (round 1: the two inline tags sit on other sentences, not on the instrument or bansuri sentences). The pages "Ashtachhap" and "Ashtachap" returned 404.
[89] Wikipedia, "Pushtimarga" — https://en.wikipedia.org/wiki/Pushtimarg — read 2026-10-19 — opened in full (the last 2,828 characters, read in round 1, hold only categories, a last-edited line of 4 October 2026 and footer links).
[90] Wikipedia, "Vallabhacharya" — https://en.wikipedia.org/wiki/Vallabhacharya — read 2026-10-19 — opened (dates: born 1478 or 1479; died 1530 per sectarian accounts).
[91] Wikipedia, "Narsinh Mehta" — https://en.wikipedia.org/wiki/Narsinh_Mehta — read 2026-10-19 — opened (dates inconsistent inside the page).
[92] Wikipedia, "Vaishnava Jana To" — https://en.wikipedia.org/wiki/Vaishnava_Jana_To — read 2026-10-19 — opened (the first Gujarati line was not reproduced by the tool).
[93] Wikipedia, "Garba (dance)" — https://en.wikipedia.org/wiki/Garba_(dance) — read 2026-10-19 — opened.
[94] Wikipedia, "Harsidhhi" (the page is "Harsiddhi") — https://en.wikipedia.org/wiki/Harsiddhi — read 2026-10-19 — opened.
[95] Wikipedia, "Gujarati script" — https://en.wikipedia.org/wiki/Gujarati_script — read 2026-10-19 — opened (the first 100,000 of 137,542 characters).
[96] FFmpeg `libavfilter/vf_subtitles.c` at the tags n5.1, n6.0, n6.1.1, n7.0, n7.1.1, n8.0, n8.0.1, n8.1, n8.1.1, n9.0 and n9.0.2 — https://raw.githubusercontent.com/FFmpeg/FFmpeg/<tag>/libavfilter/vf_subtitles.c — read 2026-10-19 — opened; with the researcher's own runs of `-h filter=subtitles` and `-h filter=ass` on 6.1.1 and on the n9.0.2 build, and the controlled A/B in `research/devotional-sound-script-fixtures/subtitles_vs_ass_shaping_2026-10-19.csv`.
[97] Rohit Kumar, "Haveli Sangeet as a medium of Vaishnava Bhakti within the Pushtimarg Sect", Sangeet Galaxy 15(2), July 2026, pp. 191 to 199 (ISSN 2319-9695; a self-described "Peer Reviewed e-Journal"; the author is a research scholar at the Central University of Punjab; the method is recorded YouTube videos and secondary sources, by its own statement; works cited include Gaston, Beck (2011) and Sharma (2010, Hindi)) — https://sangeetgalaxy.co.in/wp-content/uploads/2026/07/29.-Rohit-Kumar.pdf — read 2026-10-19 — opened (the fetch tool met a verification wall, so the 9-page PDF was downloaded with curl and its text extracted locally).
[98] Centre for Cultural Studies & Development, "Excerpt from the Study on Practice of KIRTAN – Haveli Sangeet" (PDF, 19 pages, undated; field visits 27 to 30 September 2021 and 9 November 2021) — https://ccsdindia.org/reports/Report-KIRTAN-Haveli-Sangeet.pdf — read 2026-10-19 — opened (PDF text extracted locally). Quotes a Nathdwara temple pakhawaj player; no names are copied here.
[99] Shrinathji Temple, Nathdwara (temple-linked blog; footer "Shrinathji Temple, Nathdwara"), "Shrinathji darshan" posts of 22 to 29 March 2013 — https://blog.nathdwaratemple.org/2013/03/shrinathji-darshan-mangla.html and the same folder's -shringar, -gwal, -rajbhog, -uthapan, -aarti, -bhog and -shayan .html pages — read 2026-10-19 — opened (fetch-tool summaries; the sidebar of the Mangla post lists the eight darshans as Shayan, Aarti, Bhog, Uthapan, Rajbhog, Gwal, Shringar, Mangla).
[100] shrinathdwara.in, "Daily Darshan Timings" — https://shrinathdwara.in/darshan/ — read 2026-10-19 — opened (fetch-tool summary). Describes itself as an "independent devotee fan portal", not operated by or affiliated with the Nathdwara Temple Board. Eight darshans with hours and ragas; the phones-and-cameras rule.
[101] Françoise Mallison, "Les chants dhola au Gujarāt et leur usage pour la dévotion vallabhite", Bulletin de l'École française d'Extrême-Orient 75 (1986), pp. 79 to 103 — https://www.persee.fr/doc/befeo_0336-1519_1986_num_75_1_1701 (DOI 10.3406/befeo.1986.1701) — read 2026-10-19 — opened (first page, p. 79, as text; the later pages are page images; the issue contents page https://www.persee.fr/issue/befeo_0336-1519_1986_num_75_1 was opened to find it).
[102] Anne-Marie Gaston, *Krishna's Musicians: Musicians and Music Making in the Temples of Nathdvara, Rajasthan* (New Delhi: Manohar, 1997; ISBN 817304161X; 358 pages) — Internet Archive record https://archive.org/metadata/krishnasmusician0000gast — record opened 2026-10-19; the full text is access-restricted: NOT READ. It is the only printed book in [88]'s reference list and is in the "Further reading" of Wikipedia's "Shrinathji" page; [97] lists a 2023 Manohar edition.
[103] Wikipedia, "Sukhakarta Dukhaharta" — https://en.wikipedia.org/wiki/Sukhakarta_Dukhaharta ; and "Ganesh Chaturthi" — https://en.wikipedia.org/wiki/Ganesh_Chaturthi (first 100,000 of 134,389 characters) — read 2026-10-19 — opened (fetch-tool summaries): "composed by the saint Samarth Ramdas (1608 - 1682 CE)"; no composition year; cites Vijay Golesar (Lokprabha, 2012) and Arun Shanbag, *Prarthana: A Book of Hindu Psalms* (2007), p. 163.
[104] Wikipedia, "Taittiriya Upanishad" — https://en.wikipedia.org/wiki/Taittiriya_Upanishad — first 100,000 of 162,070 characters read 2026-10-19 — opened (fetch-tool summary): the Devanagari line "मातृदेवो भव" in the eleventh anuvaka of Shiksha Valli, rendered "Be one to whom a mother is as god".
[105] Android Open Source Project, `frameworks/base/data/fonts/fonts.xml` (GitHub mirror, master) — https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/master/data/fonts/fonts.xml — read 2026-10-19 — opened. The file's header marks it DEPRECATED as a source of installed fonts; `und-Gujr` maps to NotoSansGujarati-Regular.ttf and -Bold.ttf, NotoSerifGujarati-VF.ttf as the serif fallback, and a compact NotoSansGujaratiUI.
[106] Android Developers, "Supported formats", Media3 ExoPlayer, section "Standalone subtitle formats" — https://developer.android.com/media/media3/exoplayer/supported-formats — read 2026-10-19 — opened (fetch-tool summary): WebVTT, TTML, SubRip and SSA/ASS supported as side-loaded files; nothing on fonts. The SubtitleView reference page (https://developer.android.com/reference/androidx/media3/ui/SubtitleView) loaded without its class text.
[107] YouTube Help, "Supported subtitle and closed caption file types" — https://support.google.com/youtube/answer/2734698 — read 2026-10-19 — opened (fetch-tool summary; no page date, footer "©2026 Google"): SubRip (.srt) under basic file formats; "No style info (markup) is recognized"; plain UTF-8.
[108] Kumar One font files: Google Fonts `ofl/kumarone/KumarOne-Regular.ttf` (SHA-256 04d6479721639f0d00aa34cfaa18d940eacf84060b427433edb70100b6d01100) and the foundry's `products/KumarOne-Regular.ttf` (SHA-256 2f0026416044ced58d8a1be796d57394a059f8ab84c3d1a33b0817919f2d80ea) — https://raw.githubusercontent.com/google/fonts/main/ofl/kumarone/KumarOne-Regular.ttf ; https://raw.githubusercontent.com/itfoundry/kumar/master/products/KumarOne-Regular.ttf ; repository page https://github.com/itfoundry/kumar (folders features, masters, products; no releases) — downloaded and tested 2026-10-19 (fontTools 4.67.0, freetype-py 2.13.2, libass 0.17.1 through ffmpeg 6.1.1); results in `research/devotional-sound-script-fixtures/kumar_one_and_hind_vadodara_followup_2026-10-19.csv`.
[109] Indian Type Foundry, Hind Vadodara source — https://raw.githubusercontent.com/itfoundry/hind-vadodara/master/GlyphOrderAndAliasDB ; https://raw.githubusercontent.com/itfoundry/hind-vadodara/master/masters/HindVadodara.glyphs (1.28 MB) ; repository page https://github.com/itfoundry/hind-vadodara (folders build, features, masters; no releases) — read 2026-10-19 — opened. The Google Fonts side: https://raw.githubusercontent.com/google/fonts/main/ofl/hindvadodara/HindVadodara-Regular.ttf and METADATA.pb.
[110] Wikipedia, "Nathdwara" — https://en.wikipedia.org/wiki/Nathdwara — read 2026-10-19 — opened (fetch-tool summary; maintenance-tagged): an uncited sentence, "Mobile phones, socks, and shoes are not allowed", with lockers near the gate.
[111] Temple sites that loaded in round 1 and state no recording or photography rule: https://www.nathdwara.in/ (operated by the Nathdwara Temple Board, per its footer), https://blog.nathdwaratemple.org/, https://www.dwarkadhish.org/ and https://somnath.org/ (Shree Somnath Trust). https://www.nathdwaratempleboard.org/ returned 503; https://nathdwaratemple.org/ returned only its title; https://www.nathdwara.in/ashtasakha.php covers the Ashtachhap poets only — all read 2026-10-19 (fetch-tool summaries).
[112] Wikipedia, "Aarti" — https://en.wikipedia.org/wiki/Aarti — read 2026-10-19 — opened (fetch-tool summary): names Om Jai Jagdish Hare, Om Jai Shiv Omkara, Om Jai Lakshmi Mata, Om Jai Adya Shakti, Sukhakarta Dukhaharta and others without authors or dates.
[113] Wikipedia pages searched in round 1 for the death year of the arranger of the "Vaishnava Jana To" tune, none of which gives one: "Vaishnava Jana To" (re-read; two mentions: "Narayan Khare, who served as musician at Gandhi's Ahmedabad Sabarmati ashram, set it in the 1920s" and his daughter on Mumbai radio in the 1940s; no link, no dates), "Vishnu Digambar Paluskar", "Sabarmati Ashram", "Gandharva Mahavidyalaya", "Narsinh Mehta", "Raghupati Raghav Raja Ram", the Gujarati page for the bhajan, and the surname page "Khare" (which lists only Narayan Bhaskar Khare, 1884 to 1970, a politician: a different person) — https://en.wikipedia.org/wiki/<title> — read 2026-10-19 (fetch-tool summaries). Pages at "Narayan Moreshwar Khare", "Narayan Khare" and "Narayanrao Khare", and the Hindi and Marathi equivalents tried, returned 404.

**Repository sources.**
[R1] `research/music-sound.md` (Q5 term table; cost ranges; OneMusic, cited as its source 51). Read for this playbook; not re-opened.
[R2] `research/hindu-frameworks.md` (Templates B, C, F; flags; the season and time field).
[R8] `research/gujarati-devotional-sound.md` (sibling track, in progress 2026-10-19). [R9] `research/saurashtra-world.md` (sibling track). Also: `research/devotional-sound-script.md` (the researcher's full note, 2026-10-19, with its "Follow-up research (round 1)" section), `research/devotional-sound-script-fixtures/` (the strings, CSVs and README; not reproduced here), `reviews/04-hindu-mobile-briefs-review.md` (the proposed O-36 to O-45), and `reviews/05-her-world-briefs-review.md` (the answers to O-36 to O-40 as recorded there).

**Sanskrit and regional-language strings (exact, with transliteration and source).** The strings are copied from the committed fixture (`research/devotional-sound-script-fixtures/shaping_fixture.srt`, read in round 1) and checked on 2026-10-19: the mantra's IAST against [89], and each Devanagari and Gujarati form by transliteration from its IAST (all five forms match letter for letter). The note gives a transliteration for some of the other strings and not for others; where it does not, the cell says so. The maker confirms the script she reads them in (open question 1).

| String (as in the source) | Transliteration as the source gives it | Use | Source |
|---|---|---|---|
| `śrī kṛṣṇaḥ śaraṇaṃ mama`; Devanagari `श्री कृष्णः शरणं मम` (fixture cue 1); Gujarati `શ્રી કૃષ્ણઃ શરણં મમ` (cue 7) | As [89] gives it: `śrī kṛṣṇaḥ śaraṇaṃ mama` (the page prints the K capitalised) | Ashtakshar mantra; card only, never audio | [89]; repeated three times in the first ceremony (the page cites Bennett 1993, p. 67). The two scripts are the fixture's |
| `શ્રી કૃષ્ણ` with IAST `śrī kṛṣṇa` | Given as "શ્રી કૃષ્ણ śrī kṛṣṇa" | A Gujarati-script test line with IAST letters (boxes on ṇ ṛ ṣ in some faces) | Note Q9 item 6; fixture `harfbuzz_shaping_results_*` and `iast_coverage_*` |
| `સંવત ૨૦૮૩` (fixture cue 7) | `saṃvat 2083`, read letter by letter from the script (inference); a numeral test, not a quotation | Gujarati numeral test (a face without Gujarati digits falls back) | Note Template K item 9; fixture |
| `क्ष` | ksha | Devanagari conjunct test | Note Q10 |
| `त्र` | tra | Devanagari conjunct test | Note Q10 |
| `ज्ञ` | jna | Devanagari conjunct test | Note Q10 |
| `श्री` | shri | Devanagari conjunct test | Note Q10 |
| `धर्म` | dharma | Devanagari reph test | Note Q10 |
| `कि` and `क्षि` | Not given in the note; "ki" and "kshi" are our reading (inference) | Short-i reorder test | Note Q10 |
| `मातृदेवो भव` (fixture cue 1) | `mātṛdevo bhava` | A fixture string for complex shaping; from the Taittiriya Upanishad, Shiksha Valli, eleventh anuvaka, where the page renders it "Be one to whom a mother is as god" | [104] (the page prints the Devanagari line; no romanisation); note Q10 |
| `यमुनाष्टकम्` (fixture cue 1) and `યમુનાષ્ટકમ્` (cue 7) | `Yamunāṣṭakam`, as [90] spells it | A Sanskrit hymn to the river goddess; card only | [90]; the two scripts are the fixture's |
| `Om Jai Jagdish Hare` | Title as given | Aarti; text free (Phillauri, d. 1881) | [12] |
| `Vaishnava Jana To` | Title as given | Narsinh Mehta; first line not reproduced by the tool | [92] |
| `Om Namah Shivaya` | As given | Card only; not re-read | Note N10 (no source text read) |
| `Shaant aur Gambhir` | As given (Hindi words) | A rasa word for Bhairav in the source | [39] |
| `Tumburu Vina` | As given (Sanskrit) | The tanpura's Sanskrit name | [52] |
| `pakṣavādya` (Prakrit origin of "pakhavaj") | As given | Instrument name | [51] |
| `mangala vadyam` | As given | Nadaswaram's name in its source | [53] |
| `sthayi`, `antara`, `sanchari`, `abhog` | As given | The four divisions of a verse in haveli sangeet | [88] |
| `Raghupati Raghava Raja Ram`; "Ishwar Allah tere naam" | English transliteration as the note gives it | Flagged; a version with the second line is UNVERIFIED | Note, Exclusions (UNVERIFIED) |

---

## Changelog

- **2026-10-19, v0.1 (first draft).** Written by the Haiku scribe from `research/devotional-sound-script.md` (Sonnet researcher, 2026-10-19) and `CHARTER.md`, with `DECISIONS.md` as the register. Conflicts and gaps are flagged, not resolved:
  - **Register.** O-36 to O-45 are proposed in `reviews/04-hindu-mobile-briefs-review.md` but are not rows in `DECISIONS.md`. O-42 and O-43 are not yet rows. The orchestrator must enter them.
  - **W-44 and D-05.** W-44 lists "a relative's public-domain performance" as a source. D-05 bars a sung recording before the premiere. This playbook treats sung recordings as living voices and allows only instrumentals before April.
  - **W-18.** "42 characters" needs a width rule, measured on Tamil and Malayalam faces (T-9). Proposed, not entered.
  - **W-16 and W-21.** The `ass` burn-in rule for ffmpeg before n9.0, and the static-instance rule for variable fonts, are proposed, not entered.
  - **Pointers checked.** The note's pointer to `format.md` Step 8 for captions is correct: the caption bullets sit under Step 8 "Harden the slice" (lines 79 to 81), although the step title does not say so. The note's "Template A (licence log)" and "Template E (composer checklist)" are correct for `music-sound.md`. The note's "Step 16" for the phone-speaker check is a proposal: Step 16 of `music-sound.md` is the venue test, and the placement is not verified.
  - **Privacy.** The register's D-31 names a city. This playbook does not repeat it, because the repo is public. Nor does it repeat her family's or temple's names, which the note also leaves out.
  - **Fixtures.** The scribe did not read the fixture README for v0.1. The Sonnet implementor read the README and `shaping_fixture.srt` on 2026-10-19 (v0.2, below). The commands are still not reproduced here, and the measurements are taken from the note.
  - **Sibling overlap.** `playbooks/mobile-delivery.md` has an Exercise 7 ("The Gujarati shaping check on the PC") that overlaps Template K here. Reconcile the two before either is run.
  - **Stand-in not hers.** S-17 (the dhak drum) is out on D-31's region (not Bengal), although the note's Template I listed it as a stand-in.
  - **Not done.** No playbook or register edits were made beyond this file. The skill is staged in `skills-staging/devotional-music-and-indic-scripts/`. Nothing is committed. The draft awaits `fable-advisor` review against the rubric in `CHARTER.md`.
- **2026-10-19, v0.2 (round 1).** Applied `reviews/devotional-sound-script-round1.md` in place (Sonnet implementor): the brief no longer says "private" and states public exhibition (T-6); the A/B runs on `ab.srt`, test syllables only, with the never-run-FAIL-on-sacred-text rule (T-8 item 6, Exercise 2); the shehnai and Carnatic violin are `ASK` in the skill, matching T-4, and D4 now says the same; Navaratri and garba re-cited to [93] (T-11); the TODO(research) string cells filled from the fixture and the fixture-README line above corrected; `SHAPING_OPTIONS` named in T-8; `CHURCH_COLONIAL` split into `CHURCH` and `COLONIAL_EUROPEAN` (T-1, T-4); the S-13 caveat restored with a skip default (T-3, Step 7). The eight follow-ups are answered in the note's "Follow-up research (round 1)": harmonium confirmed and bansuri contested (N1, I-11, I-19), N7 partly closed, the Khare death year and the Jai Adhya Shakti author still not found, Android's Gujarati font, Kumar One's cause, Hind Vadodara's digits, no recording rule found, the PC A/B still the maker's. Also fixed: Step 5 and T-8 item 1(c) pointed to "item 8" for the A/B, which is T-8 item 6; the header said Sunday for Monday 2026-10-19; Step 7 repeated itself. Not applied (not in the nudge list): the advisor insight on the darshan clock and the pakhawaj-first brief, and the tanpura one-liner for the Sun 25 Oct sitting.
