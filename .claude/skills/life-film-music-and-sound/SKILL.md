---
name: life-film-music-and-sound
description: Plans, checks and logs the score, songs, temp track, found voice, sound design and mix for the Life Journey film, including cue mapping, licence logging for a public premiere, voice cleanup, loudness targets and stems. Use when a cue, song, AI-generated music, temp track, voice recording or mix decision is planned, reviewed or logged, or when a music or sound rights question comes up for the 2027-02-27 premiere.
---

# Life Film Music and Sound

## Purpose

Keep the music, voices and mix of the Life Journey film honest, cleared for a public screening, and good enough for a theatre-grade room. This skill turns the research notes into a procedure for Claude agents. The human version is `playbooks/music-sound.md`. The source notes are `research/music-sound.md`.

The maker is the only person on the project and the only one who knows about the film (answer given 2026-10-18). Assume no second keeper, no collaborator and no insider.

## When to use / when not to

**Use** when:
- a cue (motif, clock, bed, pull-out, voice-zone or end) is mapped, spotted, decided, cleared or replaced;
- a song, sound effect, library track, AI-generated track or temp track is proposed, logged or used;
- a found voice, relative recording or consent card is drafted or reviewed;
- a mix, stem set, loudness target or venue playback is planned or checked;
- a rights statement for music or sound is needed for the premiere country, venue or date.

**Do not use** for:
- picture, story structure, runtime or interview questions (use the story and format skills);
- final sign-off on rights or contracts. This is not legal advice. Flag for the maker and, if needed, a lawyer.
- any action that contacts a publisher, label, composer, mixer, venue or relative about the film without the maker's written go-ahead. This skill plans those asks. It does not send them.

## Procedure

1. **Read the state first.** Read `CHARTER.md`, the playbook and the licence log. Check that the premiere country and venue are written at the top of the log. If they are not, stop every rights-dependent step and ask the maker. Public-domain dates, PRO rules and venue licences depend on them.
2. **Check the secrecy status before any outreach.** List who would learn about the film from the step, and whether it can be done as a low-key ask. A publisher, a label, a composer or a venue engineer all learn about the film. Ask the maker before anything leaves the project.
3. **Open or update the licence log.** Use the header in playbook Template A. Every music, sound and AI asset gets one row, and a second row if the licence differs by use. Keep the file on the maker's PC.
4. **Map the cues.** Give each beat one type: MOTIF (her theme), CLOCK (a sound that dates a scene), BED (low music or ambience), PULL-OUT (silence and room tone), VOICE-ZONE (no music) or END (hard cut, no tail). Write `cue_map.csv` with a `source_in_her_life` column: the beat-sheet evidence row, or the relative who named the sound. No MOTIF or CLOCK without one. Ask the object-sound questions too (for example, what the house sounded like in the mornings), so the ambience and effects palette comes from her objects.
4a. **Flag hard chapters before any sound is placed.** For any beat flagged hard-chapter in the beat sheet, set the cue type to PULL-OUT by default, and write a flag line for the Fable advisor naming the beat, the proposed sound and why it is not silence. Write the flag line to `reviews/<chapter>/sound-flags.md` (the gate-file convention in `playbooks/agent-pipeline.md`), one line per beat: `beat_id | proposed cue | why not silence | date`, and set `advisor_flag_ref` on the cue_map row, with `hard_flag` copied from the beat sheet. No MOTIF or BED over a hard chapter without that flag.
5. **Pick a source from the stack, in this order of risk.** Silence and room tone; her own recording as recorded; the maker's own sound; a relative's performance of a public-domain tune with a written release; CC0 or Sonniss sound; CC BY music with credit; a labelled AI bed; a licensed song last, and only for one or two cues. Never default to a commercial or free track without reading its tier.
6. **Set the status honestly.** Mark `cleared` only when the log row quotes a sentence that covers each planned use (private, gathering, festival, cinema, online). Otherwise use `candidate`, `temp` or `rejected`. A temp that is not cleared is `TEMP-UNCLEARED`, stays on the maker's PC and is never shown.
7. **Check AI sources before use.** Read the AI rows of the licence log and the Q3 table in the research notes, and check `last_reread_date`. Re-read any term older than 30 days before use. Read the tool's terms as they stand, date the read, and log the plan and version. Do not rely on a remembered tier, price or download status; those change. Prefer a locally run model, since nothing is uploaded, once its licence has been read this way. Save the download and metadata. Check the commercial terms of any service you have not read. Keep the two durable rules, which never change: never use AI for her songs, and never imitate a real singer or voice. Never build the emotional peak on an AI cue.
8. **Log the found voice.** For each item, record the fields in playbook Template D3: holder, format, date, who speaks, `addressed_to`, length, quality, whether the original is in hand, consent status of everyone heard, deceased flag, closest family's yes, `public_cut_eligible` and `use_decision`. Set `public_cut_eligible` to `yes` (HER-PUBLIC, tier 1) only when she knew a camera was on, the speech is not addressed to a third party, and it is used as recorded; otherwise `no` (HER-PRIVATE, tier 2). Tier 2 items (addressed to a third party) are private only and go to the T9 ledger (`research/surprise-ops.md` T9: the corrections ledger and the post-reveal conversation). Copy originals once and never edit them. The two-tier rule is stated once, in playbook Core principle 1; it adopts the stricter reading of surprise-ops Decision 18 and film-story Decision 3.
9. **Clean on copies only.** Make a working copy with `ffmpeg -i in.m4a -c:a pcm_s24le -ar 48000 work.wav`. Run the chain in playbook Template F: hum notch at 60 or 50 Hz, high-pass at 80 Hz, gentle `afftdn`. Then write the removed track with `om=n` and listen to it. Allowed: level, high-pass, hum and noise reduction, fades, and trimming silence at the ends. Not allowed: re-cutting into new sentences, looping, stretching, pitch change, bandwidth extension, or any generative enhancer other than Resemble's `--denoise_only` mode.
10. **Cut only at pauses.** Cut found voice only between full utterances. Keep room tone under every cut. Add a credit line that says these are her own recorded words, with the year and source.
11. **Mix in order.** DX (voices) first, then MX (music) under it, then AMB and FX. Duck with a sidechain, starting at ratio 2:1 to 6:1, attack 15 to 20 ms, release 600 to 700 ms, and threshold set by ear. Hand-ride the key lines. Name stems `film_v01_DX_48k24.wav`, all 48 kHz, 24-bit, from 00:00:00:00.
12. **Make three loudness versions, and no more.** Venue: -18 LUFS integrated, -1.5 dBTP, with -23 and -16 alternates. Online: -16 LUFS, -1.5 dBTP. Cinema: no LUFS target. Keep dynamics and peaks around -3 to -6 dBFS, and have a professional do any cinema version. Use two passes. The second pass must print "Normalization Type: Linear". Never use single-pass dynamic `loudnorm` for a master.
13. **Test the mix.** Check a mono sum, laptop speakers and earbuds. Check the dialogue at 6 dB below the reference level. The DX-gated check is measured over speech spans only (the `voice_present=yes` rows of `spotting.csv`), per chapter or on the concatenated spans, never over the whole film; keep 6 LU as the starting threshold (inference; see playbook Step 15) and record the per-chapter offset in the log. For the venue, use a calibration reel that contains no story. Record the chosen fader or PA setting.
14. **Make the cue sheet.** Use the ASCAP fields in playbook Template C, with the AI and licence fields added. A wholly AI composition cannot be registered with ASCAP, BMI or SOCAN, so leave its composer and writer shares blank and say why.
15. **Freeze and copy.** Freeze the log on or before 2027-02-25, write a hash list, and keep copies on a second stick and a third device. Re-read every AI and subscription row in the week before the premiere, and note the date.
16. **Report.** List each `TODO(research)` item the work touched. Never invent a licence term, price, date or URL. Quote the source, or mark the fact UNVERIFIED.

## Checklists

**Before a cue is marked `cleared`:**
- [ ] The log row has a source URL or file, a date read, a quoted sentence and a licence name.
- [ ] The row says yes or no for each use: private, gathering, festival, cinema, online.
- [ ] No CC BY-NC or CC BY-ND track is in the master. FMA-Limited is excluded.
- [ ] If AI: tool, version, plan at download, download date and settings file are logged. The attribution line is drafted.
- [ ] If a song: sync and master are both in writing, with the media, territory and term written down.
- [ ] If a relative performed it: a written release covers the venues named.
- [ ] No Minecraft or other game sound or music is used.

**Before any found voice is used:**
- [ ] The original is in `originals`, unedited, with a hash.
- [ ] Consent status for each person heard is logged, including children, friends and the dead (with the closest family's yes).
- [ ] `addressed_to` and `public_cut_eligible` are set. A clip addressed to a third party is private only.
- [ ] For any public-cut use: the one-key-three-guards decision is recorded (decision sheet, advisor flag, a 72-hour double yes, default out on doubt).
- [ ] The consent tier is recorded with the spoken yes: A or B. Tier C is a written ask after the premiere.
- [ ] The clip is used as recorded, and cut only at pauses.
- [ ] No cloud enhancer has touched the file. No voice model or text-to-speech in a real person's voice has been used.

**Before a master is exported:**
- [ ] The two-pass loudness output says "Normalization Type: Linear".
- [ ] Peaks are at or below -1.5 dBTP for venue and online copies.
- [ ] The mono sum has been listened to.
- [ ] DX-gated check on speech spans only (the `voice_present=yes` rows of `spotting.csv`): the full mix is no more than 6 LU above the DX stem, both measured integrated over those spans; per-chapter offset recorded.
- [ ] The stems are the same length, start at 00:00:00:00, and are named by the convention above.
- [ ] A backup of the file and the log is on a second device.

## Quality bar: theatrical or mediocre

**Theatrical** looks like this:
- One motif returns with a different instrument, tempo or mood as her life changes.
- The music steps back before the hardest moment and leaves silence or room tone, not a swell.
- Her voice is clear at the back of the room at the chosen venue fader, with music under it.
- Ducking is invisible: no pumping, and the music returns in the pauses.
- Room tone sits under every cut, so no edit sounds like a dropout.
- Every sound has a log row that a reviewer can check without asking the maker.
- Her voice sounds like her, uncut, with no bandwidth extension or invented words.
- Loudness is chosen for the room, not for a streaming number.

**Mediocre** looks like this:
- Music at one level throughout, or music that never leaves.
- A temp track that survived into the final mix.
- "Royalty-free" assumed to mean cleared for a public screen.
- Every master set to -14 LUFS, or a cinema master squashed to a loudness target.
- A voice that was denoised so hard it sounds underwater, or extended to fill the bandwidth.
- An AI cue at the emotional peak, or AI that sounds like loop-based wallpaper.
- Dead air where room tone should be.

## Ethics, rights and privacy guardrails

- **No voice copies.** Never clone, imitate or synthesise her voice or a relative's. Never re-sing her song with AI or a sound-alike. Never generate a letter or narration in a relative's voice (charter principle 4; Suno, ElevenLabs and Google terms agree).
- **Found voice stays as recorded.** Restoration is allowed. Invention is not. Her words are never re-cut into new sentences.
- **Family audio stays on the maker's PC.** Do not upload it to Suno, Auphonic, Descript, Adobe or any other cloud service without the maker's written decision and a read of its current terms (research Q8 records what was read on 2026-10-18; re-read before use).
- **Hard chapters get silence.** No sirens, monitors or heartbeats under a real loss. The maker decides, and the Fable advisor flags sensitive cues (charter principle 5).
- **Secrecy.** No outreach to a publisher, label, composer, mixer, lawyer, venue or relative about the film without the maker's written go-ahead. Name-free briefs only. The spoken consent card is the surprise-ops card plus one public sentence (playbook Template D2). Its wording goes through the surprise-ops truthful pretext cards before anyone reads it. The orchestrator patches `playbooks/surprise-ops.md` (Truthful pretext cards section, consent card) with the D2 sentence and the A/B answers by Saturday 2026-11-07; until that patch lands, D2 is not read and no relative is recorded for the public cut.
- **Consent.** Spoken answers are A (family only) or B (the gathering). Tier C (festival, cinema, later showings) is a written ask after the premiere, and nothing about festivals or cinemas is promised before then. Removals are honoured until Friday 2027-02-19. Log the spoken yes with each file.
- **AI disclosure.** Label AI-generated audio in the credits. The EU AI Act's Article 50 may apply, and whether it applies to a small screening is unverified (TODO(research)). The Archival Producers Alliance advises logging and disclosing generated material (page read only).
- **Minecraft.** Game sounds and music are brand assets under the Usage Guidelines, and sharing counts as commercial use. Do not use them. Build a sound language of your own.
- **Not legal advice.** Public-domain dates, performing-rights rules, venue licences and personality rights differ by country. UK, German, French and Indian collecting-society rules were not read (TODO(research)).

## References

- Playbook (human version): `playbooks/music-sound.md`
- Research notes (source of every fact here): `research/music-sound.md`
- Charter: `CHARTER.md`
- Consent card and removal deadline: `playbooks/surprise-ops.md`
- Found-voice rules: `playbooks/story.md` (Decision 10); `playbooks/surprise-ops.md` (Decision 18, tier 2, private only); `research/film-story.md` (Decision 3, public cut)
- Key URLs, all read on 2026-10-18 unless noted:
  - ASCAP licensing FAQ, https://www.ascap.com/help/ascap-licensing
  - ASCAP Cue Sheet Corner, https://www.ascap.com/help/royalties-and-payment/cue-sheets
  - Musicbed, music licensing for film festivals (unusual host; vendor), https://wpengine.fm.co/musicbed/resources/music-licensing-for-film-festivals/
  - Fox Music, short films (vendor), https://www.foximusic.com/blog/?p=601
  - Audacity Noise Reduction, https://manual.audacityteam.org/man/noise_reduction.html
  - Audacity Notch Filter, https://manual.audacityteam.org/man/notch_filter.html
  - FFmpeg filters documentation, https://ffmpeg.org/ffmpeg-filters.html
  - FFmpeg download page, https://ffmpeg.org/download.html
  - EBU R 128, https://tech.ebu.ch/docs/r/r128.pdf
  - Ioan Allen, cinema loudness (ISDCF Doc 11), https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf
  - Freesound FAQ (CC tags and AI tag), https://freesound.org/help/faq/
  - Sonniss GDC bundles (media use only), https://sonniss.com/gameaudiogdc/
  - Suno Terms of Service (revised 2026-08-10), https://suno.com/terms
  - Stability AI licence (Community tier), https://stability.ai/license
  - ElevenLabs Music Terms (updated 2026-10-09), https://elevenlabs.io/music-terms
  - Epidemic Sound for filmmakers (vendor), https://www.epidemicsound.com/filmmaking/
  - Spotify loudness normalisation, https://support.spotify.com/us/artists/article/loudness-normalization/
  - Minecraft Usage Guidelines, https://www.minecraft.net/en-us/usage-guidelines
- Open gaps (see the research notes for the full list): premiere country and venue; UK PRS, GEMA, SACEM and IPRS practice; the DCI and Netflix specs read directly; Udio's and Google Lyria's primary terms; Audacity 4.0.1 on Windows; the DeepFilterNet Windows binary; Musopen's terms (403 on every path read); the Resolve Free build check (research F9).
