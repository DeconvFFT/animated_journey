# Music, Songs, Voices and the Mix for a Life Film

*Track: music-sound · Version 0.3 (round 2 review applied) · Written 2026-10-18 (Sunday), 19 weeks before the premiere on Saturday 2027-02-27 · Built from `research/music-sound.md` (researcher notes, 2026-10-18) and `CHARTER.md`. Scribe: Haiku.*

*Reading key: [n] points to a source in the Sources list at the end. "(inference)" marks our own suggestion, not something a source says. "UNVERIFIED" means we could not confirm the fact from a page we actually opened. "TODO(research)" marks a gap that still needs filling. Every rights statement here is "as read on 2026-10-18". Re-check it for the real country, venue and date. This is not legal advice.*

---

## Why this matters for our film

Music and sound carry the feeling of a life between the big moments. A kettle in the morning, a radio in the car, a waltz she used to hum. The audience will forget the exact cues. They will remember whether the film felt true, and whether they could hear her.

Two things can sink a film like this even when the picture is beautiful. The first is a rights problem: a song that cannot be shown in public, found out a week before the premiere. The second is a sound problem: a voice nobody can hear at the back of the room, or music that buries her words. This playbook is about avoiding both.

You have said that for now only you know about the film, and that you are the only person on the project. This playbook assumes that. Any option that brings in another person (a composer, a mixer, a publisher, a venue engineer) is marked as a trade-off against the secret, not as a default.

Her voice carries the film, but which of her recordings may lead in the public cut is decided by the two-tier rule in Core principle 1. The charter (principle 4) [1] allows AI to restore a real recording, but not to invent words or copy a voice. Music sits under voices and never speaks for her.

---

## Core principles

1. **Voices lead, under a two-tier rule for her found voice.** Any recorded voice sits above the music, and the music steps back when someone speaks. Her found voice is used as recorded and never re-cut into new sentences [1][4]. Two tiers decide what may lead in the public cut:
   - **Tier 1 (HER-PUBLIC), eligible for the public cut.** Speech she gave knowing a camera was on (home video at a family event, a toast, singing at a birthday), addressed to the room, the camera or a family event, and used as recorded. It may lead in the public cut only after the one-key-three-guards decision: a decision sheet, a Fable advisor flag, a 72-hour double yes, and default OUT on doubt (review 02 §0.3).
   - **Tier 2 (HER-PRIVATE), private cut only.** Anything addressed to a third party: a voicemail, an answering-machine greeting, a phone call or a message. It stays out of the public cut and goes to the T9 ledger (`research/surprise-ops.md` T9: the corrections ledger and the post-reveal conversation) for her own post-reveal decision.
   This playbook adopts the stricter reading of `surprise-ops` Decision 18 and `film-story` Decision 3, and their labels HER-PUBLIC and HER-PRIVATE. `public_cut_eligible` takes the values `yes` or `no`. The rule is stated here once. Template D3 carries the `addressed_to` and `public_cut_eligible` columns that apply it.
2. **Silence is a sound.** Take the music out before the hardest moment, not after. *Up* does this: the music slows, nearly stops and strips down to a piano before the hardest beat [66][67]. Burns's sound team put it this way: "Nothing makes sound more effective than the absence of sound" [72].
3. **One motif, many weathers.** Pick one theme early and let it return with a different instrument, tempo or mood as her life changes [66][67].
4. **Royalty-free is not cleared for a public screen.** A licence can be fine for a private link and wrong for a gathering, a festival or a cinema. Read the tier, quote the sentence and date it before you use anything [32][35][33].
5. **AI is a labelled bed, a temp, or a sound effect. Never her songs, never a copied voice.** AI music is allowed in principle because it is not a memory. It cannot re-sing her song or imitate a real singer [1][11][19][26].
6. **Keep the originals. Clean only copies.** Keep every recording exactly as received. Work on a copy at 48 kHz, 24-bit. Listen to what you removed before you keep a cleaned version [80][86].
7. **Mix for the room you will play in.** A cinema, a venue PA and an online copy each need a different level. None of them is "-14 LUFS for everything" [94][95][93].
8. **Every asset has a row in the licence log.** No row, no use. The log is the clearance record for any later festival, cinema or theatrical check [1][32].

*Terms used here, in plain words:* **LUFS** is a loudness number for a whole programme. **dBTP** is the highest peak allowed. **Stems** are separate audio files for voices (DX), music (MX), effects (FX) and room sound (AMB). **Sync licence** is permission to put a composition against picture. **Master licence** is permission to use a particular recording. **PRO** is a performing-rights organisation (ASCAP, BMI, PRS and so on). **Cue sheet** is the list of music in a film that the PRO uses to pay writers.

---

## How to do it, step by step

Dates follow the sound schedule in Template J, which matches the project timeline. Each step says what "done" looks like.

**Step 1. Set up folders and the licence log (this week).**
Make one project folder on your PC with four subfolders: `originals` (never edited), `working` (copies you may change), `stems` and `exports`. Put the licence log file in the project folder, using the header in Template A. Folder names are our suggestion (inference).
*Done when:* the log file exists and has its header row.

**Step 2. Decide the premiere country and venue (by 2026-10-31).**
The rest of this plan depends on this decision. Public-domain dates, performing-rights rules and venue licences all change by country [44][45][47][48][51][52][53]. The research read US, UK, EU, Indian and Canadian rules as far as it could. It did not read the UK PRS, German GEMA, French SACEM or Indian IPRS practice (TODO(research)).
*Done when:* the country and venue are written at the top of the log.

**Step 3. Choose your music route (by 2026-11-30).**
The research's lean is a stack of sources, not one big purchase. The full rights table is Deliverable 1 in `research/music-sound.md`. In short:
- silence and room tone for the hardest chapters;
- a relative playing a public-domain tune, with a written release, or a public-domain recording from a source whose terms you have read (Musopen's terms could not be read [43]);
- sound you record yourself, or CC0 sound;
- CC BY music or sound with credit, if the licence allows your use;
- a labelled AI bed under her voice, only if you accept it (see Decisions);
- at most one or two licensed songs, if you can clear them.
*Done when:* every cue type in Step 5 has a named source.

**Step 4. Test your voice capture on yourself (by 2026-10-31).**
Use your own voice only, and do this before any relative is asked. Follow Exercise 1. The phone settings come from [78] and [79]. The relative's card is Template D.
*Done when:* you have a clean test file that you have checked on headphones.

**Step 5. Build the cue map (by 2026-11-14).**
Take each beat from the film's beat sheet and give it one cue type:
- **MOTIF**: her theme.
- **CLOCK**: a sound that dates the scene (an era song or an era sound).
- **BED**: low music or ambience under the picture.
- **PULL-OUT**: silence and room tone only.
- **VOICE-ZONE**: her voice or a relative's, with no music.
- **END**: a hard cut to black with no music tail [7].

Give each MOTIF and CLOCK a `source_in_her_life`: the beat-sheet evidence row, or the relative who named the sound. **No MOTIF or CLOCK without one.** This is the test that a sound comes from her life and is not decoration (charter principle 2: it must mean something; review round 1). Write `cue_map.csv` with the columns `beat_id, cue_type, source_in_her_life, hard_flag, advisor_flag_ref, notes`. Copy `hard_flag` from the film-story beat sheet's `hard_flag` column (values NONE, SHARED-LIGHT, PRIVATE, HOLD, OUT, per the `film-story` template), so the two files join on `beat_id`.

For any beat flagged hard-chapter, set the cue type to PULL-OUT by default. A cue that is not silence there needs a flag line for the Fable advisor (skill Procedure 4a). Write the flag line to `reviews/<chapter>/sound-flags.md` (the gate-file convention in `playbooks/agent-pipeline.md`), one line per beat: `beat_id | proposed cue | why not silence | date`, and set `advisor_flag_ref` on the cue_map row.

For each decade, also write down what was playing in the house. Ask only in low-key ways that do not reveal the project. Include object-sound questions, such as "what did the house sound like in the mornings?", so the ambience and effects palette (research Q7) comes from her objects, not from a generic 1970s list [1][7].
*Done when:* `cue_map.csv` lists every beat with a type, and each MOTIF and CLOCK has a source.

**Step 6. Ask for songs only after you accept the trade-off (by 2026-11-15).**
A song needs two permissions. The publisher gives the sync licence for the composition, and the label gives the master licence for the recording. Skipping either one is infringement [35][36]. A PRO or venue licence does not replace either one. ASCAP says it does not license the right to put music into a motion picture [49].

Asking the publisher and the label means outsiders learn that a film uses the song (inference). That is the trade-off. If you accept it, ask the publisher first, because it sets the composition price. Then ask the label, often under a "most favoured nations" clause that makes the two sides equal [36]. Ask for the exact media, territory and term in writing: non-theatrical public screening, festival, unlisted online link, worldwide, perpetual or five years, with an option to upgrade to theatrical [36].
*Done when:* each song has an ask in writing, or you have dropped it.

**Step 7. Build a temp track from things you can keep (November).**
Use CC0 or CC BY tracks you could keep, or rough sounds you make yourself. A temp that is not cleared goes in the log as `TEMP-UNCLEARED`. It stays on your PC and is never shown to anyone [1][64]. Do not upload temp music to a cloud service or send it to family.
*Done when:* the animatic has a temp for each cue type you need, and each temp has a log row.

**Step 8. Spot the animatic (when it is about 80% locked).**
Fill the spotting sheet (Template B). Give each cue a reel and cue number, such as 1m1, plus timecodes, function, hit points and mood words [62][63]. Then run the temp-love tests. Mute the temp on three cues and check that each scene still works. Use two different temps for the key cue [64]. "Temp love" is standard industry slang, but no page we read defines it (UNVERIFIED).
*Done when:* every cue has a spotting row and a decision placeholder.

**Step 9. Decide each cue by 2026-12-14.**
For each cue, choose one: commissioned score, AI bed, public-domain performance, a relative's recording, a library cue, a licensed song, or none. Commission only the cue that carries the motif or the emotional peak. Everything else can be public domain, relative, library or silence (inference from the cost ranges in [58] and [36]). Write the decision on the spotting row.
*Done when:* no cue says "TBD".

**Step 10. Make and clear, per chapter, from the slice (2026-12-06) to each chapter's `locked=1` (last at G-LOCK, 2027-02-06).**
Build or get each cue. Set a log row's status to `cleared` only when every venue you plan to use has a quoted sentence that covers it. Get a written release for any relative's performance (Template D). If you use a composer, the checklist in Template E applies.

**A composer working from picture lock is not feasible on this calendar.** The research's planning figure is 3 to 5 weeks from locked picture to final stems, plus one week of revisions (inference) [61][62]. Counted from G-LOCK on 2027-02-06, that lands between 2027-02-27 and 2027-03-13: on or after the premiere. A composer would need a near-lock animatic by mid-January, which is a different plan (review round 1). If a composer is wanted at all, the answer is yes or no by 2026-11-30 (Decision 2).
*Done when:* every cue is `cleared`, `final` or replaced.

**Step 11. Lock substitutes by 2027-01-08.**
A licensed song without a written answer by 2026-12-14 is replaced. Substitutes are silence, a relative's performance of a public-domain tune, or a public-domain tune. Lock the substitute by 2027-01-08 and log it.
*Done when:* no song in the film is waiting for an answer.

**Step 12. Clean her found voice, per chapter, on copies (after the decision for any public use).**
Work on copies only, using the chain in Template F. Allowed: level, high-pass, hum and noise reduction, a clean fade in and out, and trimming silence at the head and tail of a clip. Not allowed: re-cutting into new sentences, splicing across pauses, looping, stretching, pitch change, bandwidth extension or any generative "enhancer" on her voice. Resemble Enhance's enhancer "restor[es] audio distortions and extend[s] the audio bandwidth", which synthesises signal. Only its `--denoise_only` mode is acceptable [85][1][4]. Cut only at natural pauses between full sentences [4].

Order matters. Fill `addressed_to` and `public_cut_eligible` in the found-voice log (Template D3) before any clip is used in the public cut. Clean for the public cut only tier 1 items that have passed the one-key-three-guards decision. Tier 2 items are cleaned for the private cut only (`surprise-ops` Decision 18). The slice chapter's voice work starts in December, with G-SLICE on 2026-12-20.
*Done when:* the cleaned file sounds like her, the original is untouched, and the log row says which cut the clip may enter.

**Step 13. Replace temp with final music, chapter by chapter (2027-01-17 to G-LOCK, 2027-02-06).**
Sound work on a chapter begins on the day that chapter is marked `locked=1` in `status.csv` (rolling chapter lock, `production-scale` Step 14). The vertical slice is the one exception: its DX cleanup, ambience and effects start in December. Drop the stems in at the same timecode, one chapter at a time. Move the music, not the picture (inference). Ask for alternate lengths (full, 30 seconds, bumper) and one or two seconds of spare audio at each end of a cue, so you can trim without re-cutting (our practice). Never lock a sync point to a licensed song's hit point (research F7).
*Done when:* each locked chapter's conformed music stem plays against the locked picture.

**Step 14. Build the mix (per chapter as it locks; mix v1 at G-MIX, 2027-02-13).**
Between G-LOCK (2027-02-06) and G-MIX (2027-02-13) there is one week, not two. Work in this order for each locked chapter: dialogue first (DX, each voice on its own track), then music (MX) under it, then ambience (AMB) and effects (FX). Set the ducking by ear, starting from Template G [101][102]. Print the stems first, then the stereo mix, then the loudness versions in Step 15. Keep everything at 48 kHz, 24-bit [99]. The DCI audio spec itself was not read (TODO(research)).

**Tools.** The proven chain is Audacity for repair and listening [104], ffmpeg for measuring and conversion [86], and REAPER or your video editor's audio page for the mix [103]. DaVinci Resolve Free's Fairlight page documents a ducker, a de-hummer and loudness meters with no Studio tag in the Resolve 21 reference manual (research F9). Confirm this on the installed build before you rely on it. Ardour is another free option under GPL v2; its Windows price was not shown [107]. SoundCraft is pre-alpha, has no sidechain bus and has open correctness bugs [105][5]. Use it for experiments only.

*Done when:* each stem is the same length and starts at 00:00:00:00.

**Step 15. Make three loudness versions (2027-02-13 to G-MASTER, 2027-02-20).**
- **Venue (starting point):** -18 LUFS integrated, -1.5 dBTP. Make -23 and -16 alternates too, then choose at the 2027-02-22 run. The -23 figure borrows from the broadcast reference [93]. The -18 starting point is from AES TD1008 for speech [98] (inference, see Decisions). The loudness target is set by the theatrical-delivery track (`production-scale` Step 15); this starting point stands until that track decides.
- **Online:** -16 LUFS, -1.5 dBTP. This matches the setting in the project's toolchain playbook [2]. Spotify normalises playback to -14 LUFS [97].
- **Cinema:** no LUFS target. Keep the dynamics, keep peaks around -3 to -6 dBFS (inference), and have a professional make any cinema version. Cinema level is a calibrated playback level, not a loudness number [94][95].

Use the two-pass method in Template G. Do not use single-pass dynamic `loudnorm` for a master. It upsamples to 192 kHz unless you set the rate, and it only goes linear when you give it four measured values [86][108].

**Operational rule.** The maker, not the venue engineer, holds the master fader during the film. Set the level at the 2027-02-22 run, from the back row, on the neutral-voice reel, and write the fader position on the run sheet.

**DX-gated check (before any master is signed off).** Measure DX and full mix over the same speech spans only (the `voice_present=yes` rows of `spotting.csv`), either by trimming and concatenating those spans with `atrim` and `concat` before `ebur128`, or per chapter, applying the test to chapters with speech. A whole-film integrated figure would compare a DX stem that is silent through every wordless passage with a full mix that is not, so a montage would skew the result. Keep 6 LU as the starting threshold (inference; the broadcast anchor in research G3 is not applied here): if the integrated DX sits more than 6 LU under the full mix, the music is too loud for a room with many listeners aged 50 and over. Lower the music and measure again. Record the per-chapter offset in the log.

*Done when:* each master's measurement and its DX-gated check are written in the log.

**Step 16. Venue test (Mon 2027-02-22).**
The surprise-ops run sheet puts the full run on the real playback chain on Monday 22 February. Start with the calibration reel: pink noise, a sweep, a neutral voice reading a neutral text, and one music bed. Use a calibration reel, not the film itself, so the venue's engineer hears nothing of the story (inference from the research's advice). Then run the film on the real chain. The maker holds the master fader, sets the level from the back row on the neutral-voice reel, and writes the fader position on the run sheet. Use Template H.
*Done when:* the fader position is written on the run sheet, and the chosen master (-18, -23 or -16) is recorded in the log.

**Step 17. Final files, cue sheet and log freeze (2027-02-20 to 02-25).**
Export the final files by G-MASTER (2027-02-20). The relatives' removal deadline is Friday 2027-02-19 [6], so apply any removals before the masters are exported (inference). Make the cue sheet (Template C). Freeze the log by 2027-02-25. Record file hashes [8]. Put a backup on a second stick and the standalone WAV on a third device. Re-read every AI and subscription row and note the date [11][19].
*Done when:* the log and cue sheet are frozen and copied to two places.

**Step 18. Day before (2027-02-26).**
Check the playback path (USB, laptop or HDMI), lip sync, and that the audio is not forced to mono. Use the day-before checks in Template H.

---

## Learn-by-doing exercises

Each exercise has a goal, steps, a time estimate (our estimate) and a "good looks like" line. Use your own voice, your own sounds or CC0 material. Do not use anything of hers in these exercises.

### Exercise 1: Check your own voice capture

- **Goal.** Get a clean file from your own phone, and confirm what format it is saved in.
- **Steps.** (1) On an iPhone, go to Settings, Voice Memos, Audio Quality and choose Lossless. On Android, use the highest-quality setting, at least 128 kbps [78]. (2) Record in a quiet room with soft furnishings. Turn off fans and the fridge if you can. (3) Put the phone on a folded towel, about 6 inches from your mouth. The guides give 5 to 12 inches for one speaker [78][4]. (4) Say your name, today's date and "test". (5) Play it back on headphones. (6) Check the codec with `ffprobe` (our command, not tested here): `ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of default=nw=1 "in.m4a"`. Write down what it says. The research assumed Lossless is ALAC, but that is not confirmed (TODO(research)).
- **Time.** About 45 minutes.
- **Good looks like.** The slate is clear, the room tone is quiet, the original is in `originals` unchanged, and you have written down the codec.

### Exercise 2: Install and check the tools

- **Goal.** Know which versions run on your PC, and pin them.
- **Steps.** (1) Get FFmpeg from an official route. The project's download page lists releases, and Windows builds come from third parties such as gyan.dev and BtbN [87][2]. Check the page you download from before you trust it. (2) In a terminal, run `ffmpeg -version`. (3) Get Audacity from its download page. The page lists version 4.0.1 for Windows [104]. Stability on Windows is UNVERIFIED (TODO(research)). Pin the version you test. (4) Write both version numbers in the project README.
- **Time.** About 60 to 90 minutes.
- **Good looks like.** Both programs print a version. The notes say which build you used. The notes say the sandbox tests ran on FFmpeg 6.1.1 [108], so your Windows build is a new test.

### Exercise 3: Remove hum and rumble, and listen to what went

- **Goal.** Clean a noisy test clip without damaging the voice.
- **Steps.** (1) Record 30 seconds of your own voice with the fridge or a fan running. (2) Copy it to `working`. Keep the original in `originals`. (3) Run the chain in Template F, steps 0 to 2. (4) Run the "removed" version with `om=n`. (5) Play the removed track. If you hear consonants or breaths in it, back off. (6) Compare the cleaned version to the original at matched loudness.
- **Time.** About 90 minutes.
- **Good looks like.** The hum is quieter and the voice is intact. The removed track contains only hum and hiss, with no words. There is no warble or "underwater" smear.

### Exercise 4: Make a loudness version in two passes

- **Goal.** Measure a mix, then normalise it to -18 LUFS with a linear second pass.
- **Steps.** (1) Use any voice clip of about 2 minutes, or your Exercise 3 file. (2) Measure it with `ebur128` (Template G). (3) Run the first `loudnorm` pass with `print_format=json`. (4) Copy the four measured values and the offset into the second pass. (5) Check that the second pass prints "Normalization Type: Linear" [108]. Check the peak.
- **Time.** About 60 minutes.
- **Good looks like.** The output is close to -18 LUFS, the peak is at or below -1.5 dBTP, the quiet passages are still quiet, and the second pass reports linear.

### Exercise 5: Duck a music bed under a voice

- **Goal.** Music that drops under speech and comes back in the pauses, without pumping.
- **Steps.** (1) Use your Exercise 3 voice file as DX and any CC0 music bed as MX. (2) Run the sidechain command in Template G. (3) Listen for pumping. (4) Check that the music returns in the pauses and that it does not rise in short breaths. (5) Move the most important line by hand with volume automation, if needed [101][102].
- **Time.** About 60 minutes.
- **Good looks like.** The words are clear at every point, the music is felt more than heard under speech, and no note jumps.

### Exercise 6: Mono and small-speaker check

- **Goal.** Make sure the mix survives a laptop, a phone and a mono sum.
- **Steps.** (1) Play Exercise 5's output on laptop speakers, then on earbuds. (2) Sum it to mono with `-ac 1`, and play that. (3) Listen for phase problems, a missing voice or a thin sound.
- **Time.** About 30 minutes.
- **Good looks like.** The voice is clear in mono and on small speakers. Nothing vanishes in the sum.

### Exercise 7: Fill one licence-log row correctly

- **Goal.** Learn the difference between "free" and "cleared".
- **Steps.** (1) Find one CC0 sound on Freesound. Freesound's CC0 and CC BY licences are free to use, and CC BY needs credit [75]. (2) Read the licence tag on the page. Check for a GenAI tag, because AI-generated uploads are permitted if tagged [75]. (3) Save a screenshot of the licence text. (4) Fill one row of the log (Template A), quoting the sentence. (5) Set the status to `candidate`, not `cleared`, because one example is not a whole cue.
- **Time.** About 45 minutes.
- **Good looks like.** The row has a date, a quoted sentence, a file for the screenshot and a status. A reviewer can tell from the row alone whether it is safe to use.

### Exercise 8: Write a name-free composer brief for one cue (write only, do not send)

- **Goal.** Learn what a composer needs, without telling anyone about the film.
- **Steps.** (1) Pick one MOTIF or BED cue. (2) Write the motif meaning in plain words, the two or three moods it must reach, and the timecodes in and out with hit points [62][63]. (3) Write the dialogue zones and the "do not touch" list. (4) Add the delivery spec (48 kHz, 24-bit WAV, full and short lengths). (5) Check the brief for names, places and anything that identifies her.
- **Time.** About 2 hours.
- **Good looks like.** A stranger could write to the brief with no clue who the film is about, and the cue can be checked against the picture by timecode.

---

## Templates and checklists

### Template A. Licence log header

Copy this as the first line of `log/licence_log.csv`. One row per asset. Add a second row if the same asset has a different licence for a different use. Keep the file on your PC.

```
asset_id,type,title,creator,source_url,date_accessed,plan_or_tier,account_name,licence_name_and_version,licence_text_file,quoted_sentence,sync,master,public_performance_who,cleared_private,cleared_gathering,cleared_festival,cleared_cinema,cleared_online,attribution_text,restrictions,term_and_territory,subscription_dependent,cost_paid,receipt_file,pro_or_cue_sheet_status,ai_generated,ai_tool_and_version,ai_plan_at_download,download_date,ai_prompt_or_settings_file,principle4_check,status,used_in_cues,reviewer,last_reread_date
```

- **Legend for `cleared_*`:** Y (expressly covered as read), y (not stated, a fair reading says yes, get it in writing), C (covered only if the contract says so), ? (unstated or unverified), N (excluded or unavailable).
- **`status`:** temp, candidate, cleared, final, rejected.
- **`account_name`:** the account name, not a personal email address, if the file may be shared later. The research header used `account_email`; we changed it for privacy (inference).

### Template B. Spotting sheet header and one example row

```
cue_id,reel_cue,chapter,tc_in,tc_out,dur_s,picture_note,function,source_in_her_life,motif,mood_words,tempo_or_feel,hit_points_tc,pull_out_points_tc,voice_present,voice_id,dialogue_priority,temp_ref,source_plan,rights_state,ai_used,notes
C07,1m7,C3-kitchen,01:06:12:00,01:07:38:12,86.5,"photo of the kitchen table, slow push-in",BED,"[beat-sheet evidence ID] (illustrative: a relative named the waltz)",A (waltz),"warm, slightly worn","slow 3/4, music-box","01:06:40:00 (hand enters)","01:07:30:00 (music out, room tone only)",yes,V-uncle-02,voice leads,TEMP-incompetech-Floral,composer,pending,no,"no cymbals; leave 2 s of room tone before her voice"
```

The example row is illustrative. Its `temp_ref` names a CC BY temp, so the log row for that temp must say how it is credited.

**Rule.** No MOTIF or CLOCK without a `source_in_her_life`: the beat-sheet evidence row, or the relative who named the sound. The rule binds MOTIF and CLOCK cues; the example's column is filled anyway.

### Template C. Cue sheet fields

ASCAP lists what a cue sheet needs: programme title, music title, duration, how the music was used, the entitled parties with ownership shares, and the production company's details [50]. The project adds licence and AI fields.

```
program_title,program_year,cue_no,music_title,usage,duration_mmss,tc_in,composer_1,composer_1_pro,composer_1_share,publisher,publisher_pro,publisher_share,master_owner,source_type,licence_ref,ai_generated,ai_tool_version,notes
```

- **Usage terms** (check the template for exact wording): visual vocal, visual instrumental, background vocal, background instrumental, theme, logo, main title, end credit [50].
- **AI-generated cues:** set `ai_generated` to yes and leave the composer and writer shares blank. A wholly AI composition cannot be registered with ASCAP, BMI or SOCAN, and the US Copyright Office says prompts alone do not give sufficient control [28][29]. Say so in the notes.
- **Deadlines:** cue sheets are filed each quarter. ASCAP's quarterly dates (2027-01-01 for the March and April 2027 distributions; 2027-04-02 for June and July) come from the captured text of ASCAP's cue-sheet page, because the live page returned 403 on 2026-10-18 (research F1) [50]. They govern broadcast-type performances. A single gathering is not a surveyed broadcast, so the date is a project gate only if a cleared commercial song with an ASCAP writer is used and the film is later broadcast or streamed. The production company usually files [50].

### Template D. The relative's card and the extended consent card

**D1. Voice card (what a relative does).** Pair this with the voice-letter prompt in surprise-ops [6]. Edit it before you send it.

1. iPhone: Settings, Voice Memos, Audio Quality, Lossless. Android: the highest quality the recorder offers, at least 128 kbps [78].
2. A quiet room with soft things in it, such as a bedroom with the door shut or a closet. Turn off fans and TV if you can [78].
3. Put the phone on a folded towel or cushion, with the microphone uncovered, about a hand's length (6 inches) from your mouth. Turn on Do Not Disturb and plug the phone in [78][4].
4. Say your name, today's date and "test", then play it back on earphones. Fix anything you hear.
5. Record the prompt. Two to five minutes is plenty [6].
6. Send the recording as a file (Voice Memos, Share, Mail, AirDrop or USB), not as a chat "audio message". Keep your own original [79][6].
7. If you want something cut, say so before the date on the card.

**D2. Extended consent card (decided in round 1; the spoken card reads it after the surprise-ops card).** The existing surprise-ops card already tells a contributor that a film exists [6], so the addition carries only the public fact, in the fewest truthful words. Read this sentence after the surprise-ops card:

> "The film may also be shown to people outside the family at a gathering in late February. Tell me if your voice may be heard there."

The answer is one of two. **(A)** Family only: keep my voice to the private version. **(B)** The gathering: my voice may be heard there. You can change your answer or ask me to cut anything until Friday 19 February 2027 [6]. The sentence names no venue and no ticket status, so no bracketed claim needs checking.

**Tier C is not spoken.** Festival, cinema and later showings are a written ask after the premiere, and nothing about them is promised before the maker's own post-premiere release (review 02 §0.3).

**Routing.** The orchestrator patches `playbooks/surprise-ops.md` (Truthful pretext cards section, consent card) with the D2 sentence and the A/B answers by **Saturday 2026-11-07**, one week before the Track B voice-collection gate on 2026-11-14 (story.md Decision 11). Until that patch lands, D2 is not read and no relative is recorded for the public cut. Log the tier and the spoken yes with each file [6].

**D3. Found-voice log header.** Add one row per item to the inventory in `story.md` [4]. Set `addressed_to` and `public_cut_eligible` first, then `use_decision`.

```
item_id,holder,device_or_format,date_made,who_speaks,addressed_to,length,quality,original_in_hand,copied_once,hum_hz,noise_notes,other_voices_heard,consent_status_each,deceased_flag,closest_family_ok,public_cut_eligible,use_decision,cut_points_tc,credit_line
```

- `addressed_to`: the room, the camera, a family event, or a named third party (voicemail, greeting, phone call, message).
- `public_cut_eligible`: `yes` (HER-PUBLIC) only if she knew a camera was on, the speech is not addressed to a third party, and the clip is used as recorded. Otherwise `no` (HER-PRIVATE). A `yes` still needs the one-key-three-guards decision; doubt means `no`.
- `use_decision`: `as_recorded` (public cut only if `public_cut_eligible` is `yes` and the decision is recorded), `private_only` (tier 2, HER-PRIVATE, or undecided), or `none`.

Every person heard needs a consent status. That includes children, friends and relatives, and the dead, whose use needs the closest family's yes [6].

### Template E. Composer checklist (only if you decide to commission)

**Contract (confirm with an entertainment lawyer; not legal advice).**
- [ ] **Grant, not just ownership.** Sync, the composer's own master recording, and public performance through the PRO. Media: all, including festival, theatrical and online. Territory: worldwide. Term: perpetual. Exclusive or not [57].
- [ ] **Licence, not buyout (our lean).** A buyout costs more and adds nothing the film needs (inference). Standard clauses can mean "a complete assignment in copyright" if not negotiated [57].
- [ ] **Writer's share stays with the composer.** Work for hire does not give up performing royalties. BMI says the writer's share will not be paid to the employer [56].
- [ ] **Credit** on all copies, with prominence equal to other key creatives [57].
- [ ] **Cue sheet** with the composer's name and PRO, filed before quarterly deadlines [50][56].
- [ ] **No generative AI without disclosure, and no uncleared samples or songs** (our addition, supporting principle 5).
- [ ] **Confidentiality** until after 2027-02-27, including from her circle (our addition). It must cover the name-free brief.
- [ ] **Revisions and a kill fee.** Limit post-delivery changes and agree a kill fee (single source, UNVERIFIED).

**Brief.** A locked or near-locked animatic with burned-in timecode. A spotting list with in and out points, durations, hit points, tempo, structure and mood [62][63]. The temp track and what it does, not which notes it plays. The motif brief. The dialogue map. A do-not-touch list (found-voice and silence zones). The delivery spec. The cue-sheet fields [50]. Keep the brief name-free.

**Costs (2026, directional).** Indie composers quote $100 to $500 per finished minute. Boutique studios quote $500 to $2,000 or more per minute [58]. A forum snippet says ultra-low-budget films pay "$2000 for a short" [59]. For 8 to 12 minutes of score, the indie range gives about $800 to $6,000 (our arithmetic). Student and early-career fees were not found (TODO(research)).

**Finding a composer.** The research found programmes that pair composers with filmmakers, not an open job board: the Santa Barbara scoring lab, the San Francisco Conservatory with SFFILM, and a Jacobs School programme with Film Independent [61]. Working composers discuss rates in forums such as VI-Control [59]. SoundBetter, Fiverr and Upwork were not read (TODO(research)).

### Template F. Found-voice cleanup chain

Work on copies. The commands below ran in a Linux sandbox on FFmpeg 6.1.1, on synthetic test signals, and not on Windows [108]. Re-run them on your PC and listen. In PowerShell, keep each filtergraph in double quotes and run one line at a time.

```
# 0. keep the original; make a working copy at 48 kHz, 24-bit (tested for ALAC to WAV)
ffmpeg -i in.m4a -c:a pcm_s24le -ar 48000 work.wav

# 1. hum at 60 Hz (use 50 for 50 Hz mains), rumble, gentle denoise (parts tested)
ffmpeg -i work.wav -af "bandreject=f=60:width_type=q:w=30,bandreject=f=120:width_type=q:w=30,highpass=f=80,afftdn=nr=10:nf=-45:tn=1" -c:a pcm_s24le work_dn.wav

# 2. listen to what was removed (afftdn output_mode=noise)
ffmpeg -i work.wav -af "highpass=f=80,afftdn=nr=10:nf=-45:tn=1:om=n" -c:a pcm_s24le work_removed.wav

# optional neural denoise on a 48 kHz WAV (not tested here; the Windows binary is TODO(research)) [83]
deep-filter work.wav
# RNNoise is a library; its demo reads raw 16-bit 48 kHz PCM, not WAV [82]

# optional arnndn with a model file such as std.rnnn (not tested here) [84]
ffmpeg -i work.wav -af "arnndn=m=std.rnnn:mix=0.8" work_rn.wav
```

In Audacity, use Effect, Noise Removal and Repair, Noise Reduction. Learn the profile from noise only, using at least 2048 samples. Start at the defaults and use the lowest setting that works [80]. For hum, use Effect, EQ and Filters, Notch Filter at 60 or 50 Hz, then the harmonics with a Q between 2 and 10 [81]. Check on headphones and small speakers.

Hum usually shows as 60 Hz with a bigger 120 Hz part from the power supply. A notch filter usually removes it. Check for a ground loop before you filter [91].

**Rules.** Keep the original. Use the lowest reduction that works. Cut only at pauses. Keep room tone under cuts, because noise reduction leaves dead air. Do not use a cloud enhancer on family audio. Auphonic uses content to improve its algorithms, and Descript lists AI training among its uses. Adobe's terms for Enhance Speech could not be read [88][89][90].

### Template G. Mix targets, ducking and the loudness recipe

**Targets.**

| | Cinema | Venue PA | Online |
|---|---|---|---|
| File | Stems and a stereo mix at 48 kHz, 24-bit. A professional builds any DCP (inference) [99] | `venue_-18.wav` plus `-23` and `-16` alternates, with the same audio on the video master | `online_-16.mp4` (AAC) |
| Level | Calibrated playback, not LUFS. Peaks at or below about -3 dBFS (inference) [94][95] | -18 LUFS integrated, -1.5 dBTP, loudness range about 8 to 10 LU or less (inference from [98][93]) | -16 LUFS, -1.5 dBTP [2] |
| Check | Mono sum. Dialogue still clear with playback 6 dB lower (our test; theatre faders are often lowered [94]) | Listen from front, side and back; DX-gated check on speech spans only (full mix no more than 6 LU above the DX stem) | Re-measure after the AAC encode |

**Operational (venue).** The maker holds the master fader during the film, not the venue engineer. The level is set at the 2027-02-22 run from the back row, on the neutral-voice reel, and the fader position is written on the run sheet.

**Stereo fold-down.** Stereo DCPs are normally played back as plain left and right in cinemas. Do not count on matrix decoding to make a centre channel. A mix that folds safely to mono is the safe path [100].

**Stems.** Name them `film_v01_DX_48k24.wav`, with prefixes `DX_`, `MX_`, `FX_`, `AMB_`, `FULL_` and `ME_` (music and effects without dialogue, for any later translation). Keep the originals and the cleaned versions separate. Make a hash list [8].

**Ducking starting values (set by ear).** Ratio 2:1 to 6:1. Attack 15 to 20 ms. Release 600 to 700 ms, so the music does not rise during short pauses. Threshold by ear. Duck 6 to 12 dB in busy passages and 1 to 2 dB under tone (practice). Hand-ride the key lines [101][102].

**Commands (tested in the sandbox; re-run on Windows).**

```
# measure
ffmpeg -i mix.wav -af ebur128=peak=true -f null -

# DX-gated check, speech spans only: first cut the voice_present=yes spans into dx_speech.wav and mix_speech.wav (atrim and concat; this cut is not yet tested, TODO(research)), then read the Integrated line of each summary. Do not measure the whole film for this check.
ffmpeg -i dx_speech.wav -af ebur128=peak=true -f null -
ffmpeg -i mix_speech.wav -af ebur128=peak=true -f null -

# pass 1: measure for the venue master
ffmpeg -i mix.wav -af loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json -f null -

# pass 2: linear, with the measured values pasted in (the output must say "Normalization Type: Linear")
ffmpeg -i mix.wav -af "loudnorm=I=-18:TP=-1.5:LRA=11:measured_I=...:measured_TP=...:measured_LRA=...:measured_thresh=...:offset=...:linear=true:print_format=summary" -ar 48000 -c:a pcm_s24le venue_-18.wav

# sidechain ducking: music (mx.wav) under dialogue (dx.wav)
ffmpeg -i mx.wav -i dx.wav -filter_complex "[1:a]asplit=2[sc][dxo];[0:a][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=700[mxd];[mxd][dxo]amix=inputs=2:normalize=0[out]" -map "[out]" -c:a pcm_s24le mix.wav
```

FFmpeg 9.0.2 was released on 2026-09-18 [87]. The sandbox used 6.1.1 [108]. Check the filter names in your build with `ffmpeg -filters`.

### Template H. Venue test and day-before checks

**Venue test (Mon 2027-02-22).**
- [ ] Play the calibration reel (pink noise, a sweep, a neutral voice reading neutral text, one bed). The maker holds the master fader; write the fader position on the run sheet.
- [ ] Play each of the three masters. Pick one and write the setting in the log.
- [ ] Check the player path (USB, laptop, HDMI), lip sync, and that the audio is not forced to mono.
- [ ] Check speech intelligibility at the back and sides, with at least one listener who does not have perfect hearing and who is not told the content.
- [ ] Compare each chosen master's per-chapter DX-gated offset (Step 15) with what the back-row listener reports.
- [ ] Keep a backup file on a second stick and the standalone WAV on a third device.

**Day before (2027-02-26).**
- [ ] The final file plays from the stick, the laptop and the HDMI route, with the chosen master.
- [ ] The log is frozen, and the hash list matches.
- [ ] The AI and subscription rows were re-read this week, with the date.

### Template I. Sound-recording notes for the room (your own recordings)

Record room tone for each location, in mono, for 30 to 60 seconds, with the microphone placed as it was for the voice. Lay it under dialogue edits so that cuts do not sound like a dropout. Without it, the track "goes silent in a way the audience hears as a technical fault" [74]. The 30 to 60 seconds is our practice, not a source figure.

Record sound effects in your own kitchen or a similar room, when she is not there, with no people in frame or earshot. A tap, a kettle, a door, a bus stop. This avoids consent issues and a tip-off (inference from the charter).

### Template J. Sound schedule (T-minus)

Built on the production-scale gates (G-SLICE-0 2026-12-06, G-SLICE 2026-12-20, G-MID 2027-01-17, G-DRAFT 2027-01-31, G-LOCK 2027-02-06, G-MIX 2027-02-13, G-MASTER 2027-02-20) and the surprise-ops run sheet (Mon 22 Feb to Sat 27 Feb). The format.md week-18 dates are not used. A composer from lock is not feasible on this calendar (Step 10).

| Date | What |
|---|---|
| 2026-10-18 to 10-31 | Decide the premiere country and venue. Build the log. Test your own voice capture and the cleanup chain. Low-key asks: "what was playing" and object sounds ("what did the house sound like in the mornings?"). |
| 2026-11-14 | Voice-collection gate from story.md (Decision 11, as the research notes it) [4]. The extended consent card (Template D2) is read only after the surprise-ops truthful pretext check. |
| by 2026-11-15 | Sync asks, at most two songs (only if you accepted the trade-off in Step 6). |
| by 2026-11-30 | Music route chosen. Composer yes or no (Decision 2). Temp library built. |
| 2026-12-06 (G-SLICE-0) | Animatic with temp sound. Every MOTIF and CLOCK has a `source_in_her_life`. |
| 2026-12-14 | Hard decision gate: each song cleared or replaced; each cue decided. |
| 2026-12-20 (G-SLICE) | Chapter 1 at final quality, with its sound mix. Slice DX cleanup, ambience and effects run in December. |
| 2026-12-28 | REAPER: buy the $60 licence (personal use qualifies), or start the trial only to defer the spend to this date (60 days; a trial started on this date ends 2027-02-26 and covers the 13–20 Feb mix) (Decision 7). |
| 2027-01-08 | Substitutes locked. |
| 2027-01-17 (G-MID) | Rolling chapter locks begin. Sound work on a chapter starts when it is `locked=1`. |
| 2027-01-31 (G-DRAFT) | At least 60 percent rolling-locked; each locked chapter has its cues decided. |
| 2027-02-06 (G-LOCK) | Picture lock: every shot `locked=1`. The last chapters start their sound work. |
| 2027-02-13 (G-MIX) | Mix v1 for all locked chapters. One week after G-LOCK, not two. |
| 2027-02-19 | Relatives' removal deadline [6]. Apply removals before the masters (inference). |
| 2027-02-20 (G-MASTER) | Three loudness masters: venue -18 with -23 and -16 alternates; online -16. DX-gated check passed. Hashes and loudness reports. |
| 2027-02-21 to 02-25 | Copies, cue sheet, hashes checked. Log freeze by 2027-02-25. |
| 2027-02-22 (Mon) | Full run on the real playback chain (surprise-ops run sheet). Calibration reel first. The maker sets the fader from the back row; the position goes on the run sheet. |
| 2027-02-24 (Wed) | Room brief (surprise-ops). No new sound files unless the 22 Feb run fails (inference). |
| 2027-02-25 (Thu) | Cold start 1 from a powered-off laptop (surprise-ops). |
| 2027-02-26 (Fri) | Cold start 2 and the day-before check (Template H). |
| 2027-02-27 | Premiere. |

---

## Decisions you'll need to make

Each decision lists the options, then our current lean. A lean is a suggestion for you to confirm, not a decision.

**1. Premiere country and venue.**
- *Options:* name a country now, or keep it open until the venue is known.
- *Lean:* decide by 2026-10-31. Every public-domain, performing-rights and venue-licence rule depends on it. The notes do not give a lean on which country (TODO(research): UK, German, French and Indian practice was not read).

**2. Whether anyone else is brought in.** Composer, pro mixer, rights lawyer, venue engineer.
- *Options:* (a) no one, the default; (b) a composer, the cleanest rights route for a score, at about $800 to $6,000 (our arithmetic) [58]; (c) a mixer for the cinema or venue version; (d) a lawyer for the country check.
- *Trade-off:* each person who joins learns about the film. The composer is the cleanest rights route and the worst fit for the secret [1][56].
- *Lean:* no one, as you have said. A composer working from lock is out on this calendar (Step 10), so a composer is a yes or no by 2026-11-30 or not at all. If someone joins later, use a name-free brief and a confidentiality clause that runs past 2027-02-27.

**3. Which one or two songs are truly hers.**
- *Options:* ask for up to two songs (sync and master, with the trade-off in Step 6); use a relative's performance of her song (publisher only, no master) [36]; use a public-domain tune in a relative's voice; use no song.
- *Lean:* at most two songs. Send the asks only if you accept the trade-off. Set the 2026-12-14 gate. If a song is not in writing by then, substitute.

**4. Whether labelled AI music is acceptable.**
- *Options:* (a) no AI at all; (b) AI as temp only, marked `TEMP-UNCLEARED` and never shown; (c) AI as a labelled bed under voice, with a credit line; (d) AI sound effects, such as Stable Audio's small SFX model.
- *Facts that matter:* Suno's free tier is for personal, non-commercial use. Its paid plans assign any output Suno owns, but Suno gives no copyright warranty [11][12]. Udio downloads have been off since 2025-10-29 [18][13], so it cannot supply a film file. Its primary terms could not be read (UNVERIFIED). One June 2026 explainer says paid plans grant commercial use, which conflicts with the other sources [14]. Stable Audio 3.0 has open weights, the Community Licence lets small creators own and commercialise outputs (under $1M revenue), and it runs on your PC [21][22][23]. ElevenLabs' music terms exclude film, TV and radio on every plan except the Enterprise Music tier, and Enterprise Music Lite also excludes them [19]. Google's Lyria 3 commercial terms were not confirmed (UNVERIFIED) [24][25].
- *Other facts:* Stability faces separate image-training suits, per a 2025 trade report, and no music-specific suit was found [109]. The EU AI Act's Article 50 may require synthetic audio to be marked, and deepfakes to be disclosed, with a lighter duty for an "evidently artistic, creative" work [31]. Whether it applies to a small screening, or was delayed, is UNVERIFIED (TODO(research)). The Archival Producers Alliance advises logging and disclosing generated material in documentaries; we read only its landing page [92].
- *Lean:* (b), and (c) only if you accept it. Prefer the local Stable Audio route, because it uploads nothing. Never use AI for her songs, never imitate a real singer or voice, and never build the emotional peak on an AI cue [1][26]. Label it in the credits.

**5. Whether a cinema booking is a real goal.**
- *Options:* (a) plan for a venue PA only; (b) plan for a cinema, which means a professional 5.1, a DCP and a calibrated room.
- *Lean:* plan for (a) now, and build stems so a professional can make a 5.1 later (inference). A cinema booking would change the work, and that choice belongs to you.

**6. Consent for relatives: the spoken card and the written ask (decided in round 1).**
- *Decided:* the spoken card is the surprise-ops card plus one public sentence (Template D2). It takes two answers, A (family only) and B (the gathering). Tier C (festival, cinema, later showings) is a written ask after the premiere, not part of the spoken card.
- *Still open:* only the secrecy check. The orchestrator patches `playbooks/surprise-ops.md` by Saturday 2026-11-07 (Template D2, Routing). Until that patch lands, D2 is not read. This is the single place this check is tracked.
- *Lean:* honour removals until 2027-02-19, and promise nothing about festivals or cinemas before your own post-premiere release (review 02 §0.3).

**7. Small spends.**
- *REAPER:* a 60-day full-function trial, or a $60 discounted licence for an individual using REAPER only for personal use, or for an individual or business using it commercially with yearly gross revenue at or under $20,000 (purchase page, read 2026-10-18 and re-read by the scribe the same day). The standard commercial licence is $225 [103]. A trial started on 2026-12-28 ends 2027-02-26 and covers the 13–20 Feb mix (G-MIX to G-MASTER). That end date is after G-MASTER, so the trial is enough only if nothing has to be re-mixed after 2027-02-26. *Lean:* buy the $60 licence (personal use qualifies), so the mix is not on a timer; start the trial only to defer the spend to 2026-12-28.
- *Suno Pro:* $10 a month, 20 downloads [13]. *Lean:* skip it. Stable Audio runs locally and costs nothing (research figure) [21][23].
- *Audacity, FFmpeg:* free [87][104].
- *Composer:* see Decision 2.

**8. The music spine.**
- *Options:* the stack in Step 3, or a simpler route with silence and her voice only.
- *Lean:* the research's stack, which keeps the secret. Silence and room tone, then a relative's public-domain performance, then your own sound. Cleared music comes last, for one or two cues only.

**9. Runtime** (charter open decision). A shorter film needs fewer cues to clear and fewer mixes to check (inference). The research does not set a runtime. *Lean:* leave this to the runtime decision in the film track.

---

## Pitfalls

1. **"Royalty-free" mistaken for "cleared to screen".** Most free and subscription terms exclude film, festival or theatrical use. Epidemic Sound sends festival and theatrical films to an Enterprise licence [32]. ElevenLabs excludes film on every plan except the Enterprise Music tier, and Enterprise Music Lite also excludes it [19]. Mixkit excludes CDs, DVDs, games and TV and radio broadcast, and is silent on film [38]. The YouTube Audio Library says YouTube cannot advise on off-platform use [40]. Pixabay's terms do not warrant that any consents or licences have been obtained [39]. *Fix:* read the tier, quote the sentence, date it, and ask the library in writing for each use.
2. **A venue's PRO licence mistaken for sync.** It is not one. ASCAP does not license sync [49]. Ask the venue which PRO licences it holds, and whether they cover music in a film shown there. In Australia, OneMusic requires a film-screening licence for an event "regardless of whether there's an entry fee" [51]. In the US, cinema owners say producers clear performance at source [53]. The non-profit exemption in 17 U.S.C. 110(4) covers only "nondramatic" musical works, not a motion picture as a whole [54].
3. **Free does not mean fine for a festival.** Musicbed says "most festivals explicitly reject Creative Commons and 'copyright-free' claims" [35]. A festival can disqualify you or pull the film for a false clearance claim [35]. Keep CC-based music out of the master if you might enter a festival.
4. **CC BY-NC and CC BY-ND traps.** NC bars uses "primarily intended for or directed toward commercial advantage". A paid festival entry, a cinema booking or a monetised link can count [41]. ND (no derivatives) bars changes, and a video that uses a track is a derivative [41]. Keep both out of the master.
5. **AI terms and lawsuits move.** Suno and Stable Audio terms change. The label suits against Suno are live. Fact discovery closed on 2026-09-30 in the first case, and a second UMG and Sony suit was filed on 2026-09-18. No summary-judgment ruling or settlement was found as of 2026-10-18 (research F2) [16]. Re-read the status in the week of 2027-02-01. Re-read the terms the week before the premiere, keep downloads and receipts, and keep a swap-ready alternative for every AI cue.
6. **AI cues cannot be registered as wholly AI.** A wholly AI composition cannot be registered with ASCAP, BMI or SOCAN. Say so on the cue sheet, and do not claim a composer or writer share for it [28][29].
7. **Cloud "enhancers" and family audio.** Auphonic uses content to improve its algorithms (business customers can opt out on request), and staff or contractors may listen to it. It deletes audio after 21 days [88]. Descript lists training AI models among its uses [89]. Adobe's policy mentions machine-learning analysis, with an opt-out [90]. *Fix:* never upload family audio to any of them. Keep it on your PC.
8. **Anything that fakes a voice.** Out: narration in her voice, AI re-singing of her song, text-to-speech of a relative's letter in that relative's voice, a cloned relative. Principle 4 and the tools' own terms agree. Suno allows a voice model only of your own voice [11]. ElevenLabs bars mimicry and Google bars impersonation [19][26]. Midler v. Ford is a US advertising case where imitating a singer's distinctive voice was held unlawful [55]. Treat it as a reason to avoid sound-alikes.
9. **Temp love and temp leaks.** Temp music tends to become the music. Mute the temp on three cues and test. Brief the composer on what the temp does, not which notes it plays [64]. Keep temp on your PC.
10. **Wrong loudness.** Do not master a cinema version to -14 LUFS. Do not use single-pass dynamic `loudnorm` for a master [86][94]. The "-23 or -14 for everything" rule does not apply to a cinema or an unknown PA [94][95].
11. **Loss beats with the wrong sound.** Do not add sirens, monitors or heartbeats to a real loss. Those belong to war films, not to a mother's illness (inference, from the Vietnam War sound practice [73]). Default to silence and room tone for hard chapters, and let the maker decide. The Fable advisor flags sensitive cues (charter principle 5) [1].
12. **Re-cutting her voice.** Splicing, looping, stretching, pitch changes and bandwidth extension all break principle 4 [1][4]. A/B the cleaned file against the original, and keep the original.
13. **Sync price shock, or silence.** Festival-only sync and master fees for indie songs are roughly $500 per side, for about 12 months. Recognisable names are about $800 to $1,500 per side. Step-ups can be 3 to 10 times the first price [36]. For independent films with distribution, one unattributed range puts a song at $10,000 to $80,000 [37], so a later distribution plan would change the cost. Negotiate the step-up before you sign. Send asks by 2026-11-15, set the 2026-12-14 gate, and keep a substitute.
14. **A quiet recording that is not quiet enough.** Phone recordings in a room with a fridge or fan carry hum and room noise. Turn them off first, as the guides advise [78] (Exercise 1). Do not rely on software to fix a bad room.
15. **Chat-app voice notes.** Chat apps may recompress audio. That was not verified (UNVERIFIED). Ask relatives to send a file, not a chat voice note [79][6].
16. **Minecraft's audio.** The Minecraft Usage Guidelines count "sounds and other audio from any of our games" as brand assets, and sharing counts as commercial use under the guidelines. Permissions can be revoked [10]. Do not use game sounds or music. Build your own sound language for any Minecraft-styled sequence.
17. **Jurisdiction mistakes.** Public-domain dates, performing-rights rules and venue licences differ by country [44][45][46][47][48][51][53]. Decide the country first.
18. **Secrecy leaks through the people around the film.** A composer, a mixer, a lawyer, a venue engineer, a publisher, a label and a relative all learn something. Name-free briefs, a calibration reel, and a confidentiality clause limit the damage. The no-outsider path avoids it.
19. **Consent creep from private to public.** The current card promises "a film that family will watch together" [6]. A public gathering goes beyond that. Extend the card only after the surprise-ops truthful pretext check of the Template D2 wording, and honour removals until 2027-02-19 [6].
20. **Hum that you can't hear.** Cleaning removes hum but also softens voice. Listen to the removed track, and keep room tone under cuts.

---

## Best references

These are the eight sources most worth your time. Read them in this order. Each is cited in the Sources list.

1. **ASCAP licensing FAQ** [49]. Why a venue or PRO licence does not give you sync. Primary source. https://www.ascap.com/help/ascap-licensing
2. **ASCAP Cue Sheet Corner** [50]. What a cue sheet must contain, and the quarterly deadlines. Primary source. https://www.ascap.com/help/royalties-and-payment/cue-sheets
3. **Musicbed, music licensing for film festivals** [35]. Sync, master and public performance are separate. Festivals reject CC claims. Vendor guide, and the host name is unusual, so check it against the source. https://wpengine.fm.co/musicbed/resources/music-licensing-for-film-festivals/
4. **Fox Music, music licensing for short films** [36]. Realistic festival-only prices, step-ups and covers. Vendor, so treat prices as directional. https://www.foximusic.com/blog/?p=601
5. **Audacity Noise Reduction manual** [80]. How to learn a noise profile and why a high setting damages the audio that remains. Primary source. https://manual.audacityteam.org/man/noise_reduction.html
6. **FFmpeg filters documentation** [86]. `loudnorm`, `afftdn`, `arnndn` and `sidechaincompress`. Read the `loudnorm` section before any master. Primary source. https://ffmpeg.org/ffmpeg-filters.html
7. **EBU R 128** [93]. The broadcast loudness reference (-23 LUFS) and why it is not a cinema or venue target. Primary source. https://tech.ebu.ch/docs/r/r128.pdf
8. **Ioan Allen, "How Loud is a Movie?"** [94]. Why cinema level is a calibrated playback level, not a LUFS target. Primary source (SMPTE paper, via ISDCF). https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf

Also worth a look, but not in the top eight: the Freesound FAQ on CC tags [75] and Sonniss's bundle terms [76] for effects, and the Minecraft Usage Guidelines [10] before any game-styled sequence.

**Films to study for sound.** These are teaching examples, not templates.
- *Coco:* one song, four performances. The showy version comes first, and the sincere versions are shorter, plainer and later [7][69].
- *Boyhood:* no score. Songs from each year act as clocks, and two titles were cut for clearance reasons [68].
- *Robot Dreams:* a song that became the theme. The production could not afford it for the closing credits [70][7].
- *Stories We Tell:* one archive recording supplies the film's sound world. The only source is a search summary, so the depth is UNVERIFIED [71].

---

## Sources

Strength tags: P primary (the rules or the maker), S secondary or press, V vendor (sells something), F forum or snippet-grade, SR search-result excerpt only (page not read), LOCAL a file in this project. Dates are page dates where shown, otherwise the read date, 2026-10-18.

**Project files**
- [1] LOCAL `CHARTER.md`, CHARTER.md. Read 2026-10-18. Principles 4, 5 and 7; cloud and upload rule; open decisions.
- [2] LOCAL `toolchain.md`, playbooks/toolchain.md. Online loudness setting (-16 LUFS, -1.5 dBTP) and music notes.
- [4] LOCAL `story.md`, playbooks/story.md. Phone recording, found-voice paragraph (restored and used as itself; not extended or imitated; Decision 10), Track B gate (Decision 11).
- [5] LOCAL `craft-motion.md`, playbooks/craft-motion.md. SoundCraft findings, including issues #707 and #710 (MP3 and AAC import can silently shorten or shift audio).
- [6] LOCAL `surprise-ops.md`, playbooks/surprise-ops.md. Current consent card, voice letter, removal deadline 2027-02-19, Decision 10 (recording rule), Bourdain case.
- [7] LOCAL `film-story.md`, research/film-story.md. Cue lengths for *Up*, *Coco* and *Robot Dreams*; end-cut advice; Tarnation cost.
- [8] LOCAL `format.md`, playbooks/format.md. Hash list (Step 4). Its rehearsal dates are retired for this track (2026-10-18); the venue test is the Mon 2027-02-22 run.
- [10] Minecraft Usage Guidelines, https://www.minecraft.net/en-us/usage-guidelines. Read live 2026-10-18. P. Game sounds and audio count as brand assets; sharing counts as commercial use; permissions revocable.

**AI music and AI rules**
- [11] Suno Terms of Service, https://suno.com/terms. Revised 2026-08-10, effective 2026-09-03. P. Output assignment, no copyright warranty, downloads, voice-model limits, training licence.
- [12] Suno Help, commercial use, https://help.suno.com/en/articles/2410177. Undated. P. Pro and Premier commercial rights; free tier non-commercial.
- [13] Undetectr, "Suno vs Udio 2026", https://undetectr.com/blog/suno-vs-udio-2026-which-is-better. 2026-10-04. V (sells file-processing; no listening tests). Suno V6 launch, prices and download counts.
- [14] Dubspot, "AI Music Licensing Explained (2026)", https://blog.dubspot.com/ai-music-licensing-explained-2026. 2026-06-12. S. A rights summary that conflicts with other sources on Udio.
- [15] Dynamoi, AI music lawsuits timeline, https://dynamoi.com/learn/ai-music-distribution/ai-music-copyright-cases-timeline. Last updated 2026-05-11. S/V. Settlements; internally inconsistent on Warner v. Udio (TODO(research)).
- [16] Music Business Worldwide, stream-ripping order, https://www.musicbusinessworldwide.com/umg-and-sony-accuse-suno-of-pirating-youtube-via-stream-ripping-to-train-its-ai/. August 2026. S. Order of 2026-08-18; fact discovery closed 2026-09-30.
- [18] Reports on Udio downloads and terms, https://dynamoi.com/learn/ai-music-distribution/is-udio-music-still-downloadable ; https://newindustryfocus.com/articles/udio-allows-downloads-for-48-hours-following-umg-deal-outcry. SR. Downloads disabled 2025-10-29.
- [19] ElevenLabs, Music Terms, https://elevenlabs.io/music-terms. Last updated 2026-10-09. P. Film, TV and radio excluded on every plan except the Enterprise Music tier; Enterprise Music Lite also excludes them (advisor spot-check, 2026-10-18).
- [21] Stability AI, licence page, https://stability.ai/license. Undated. P. Community Licence under $1M revenue; Enterprise tier.
- [22] The Decoder, Stable Audio 3.0, https://the-decoder.com/stability-ai-launches-stable-audio-3-0-with-up-to-six-minute-tracks-and-open-weights/. 2026-05-20. S.
- [23] Music Business Worldwide, Stable Audio 3.0, https://musicbusinessworldwide.com/stability-ai-launches-new-audio-models-that-can-generate-6-minute-music-tracks. 2026-05-21. S. Licence quote and training-data claim (company claim).
- [24] Google, Lyria 3 in the Gemini app, https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/. 2026-02-18. P. Commercial terms not stated.
- [25] Google Cloud, Lyria 3 and 3 Pro on Vertex AI, https://cloud.google.com/blog/products/ai-machine-learning/lyria-3-and-lyria-3-pro-on-vertex-ai. 2026-04-07. P. SynthID; C2PA.
- [26] Google, Generative AI Prohibited Use Policy, https://policies.google.com/terms/generative-ai/use-policy. Last modified 2024-12-17. P.
- [28] US Copyright Office, Part 2 Copyrightability Report, https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf. January 2025. P. Prompts alone do not give sufficient control.
- [29] Music Week, ASCAP, BMI and SOCAN on AI, https://www.musicweek.com/publishing/read/ascap-bmi-and-socan-align-on-musical-compositions-using-ai-tools-alongside-human-authorship/092955. 2025-10-28. S.
- [31] EU AI Act, Article 50, https://artificialintelligenceact.eu/article/50/. The page says it applies from 2026-08-02. S (unofficial site). Any delay is UNVERIFIED (TODO(research)).

**Libraries, rights and licensing**
- [32] Epidemic Sound, for filmmakers, https://www.epidemicsound.com/filmmaking/. Read 2026-10-18. V. Pro for online commercial work; Enterprise for theatrical or festival films.
- [33] Epidemic Sound, pricing and licensing FAQ, https://www.epidemicsound.com/pricing/. Read 2026-10-18. V. Cancellation; Enterprise 12-month minimum. Prices not read.
- [35] Musicbed, music licensing for film festivals, https://wpengine.fm.co/musicbed/resources/music-licensing-for-film-festivals/. Read 2026-10-18. V. Host name is unusual; the content is Musicbed's. Sync, master, public performance and CC rejection.
- [36] Fox Music, music licensing for short films, https://www.foximusic.com/blog/?p=601. Updated 2026-10-02. V. Directional prices, step-ups, covers.
- [37] Dynamoi, sync licensing fee benchmarks, https://dynamoi.com/learn/statistics/sync-licensing-fee-benchmarks. Published 2026-01-04, modified 2026-05-04. S/V. Directional and partly unattributed.
- [38] Mixkit, free stock music licence summary, https://mixkit.co/free-stock-music/ ; https://mixkit.co/license/. Read 2026-10-18. V.
- [39] Pixabay Terms of Service, https://pixabay.com/service/terms/. Last updated 2024-11-18 per the page. P.
- [40] YouTube Help, Audio Library, https://support.google.com/youtube/answer/3376882. Undated. P.
- [41] Free Music Archive FAQ, https://freemusicarchive.org/faq. Undated. P. NC and ND rules; FMA-Limited bars video.
- [43] Musopen, https://musopen.org/about/. SR (the site blocked fetches). Public-domain recording claims. Its terms were not read, and one guide says they carry older personal, non-commercial wording (TODO(research)).
- [44] IMSLP, Copyright Made Simple, https://imslp.org/wiki/IMSLP:Copyright_Made_Simple. Undated. S/P (a volunteer library's rules).
- [45] Cornell Library, copyright term and the public domain chart, https://guides.library.cornell.edu/copyright/publicdomain. Chart read 2026-10-18. S.
- [46] Duke Center for the Study of the Public Domain, Public Domain Day 2026, https://cspd.law.duke.edu/publicdomainday/2026/. January 2026. S.
- [47] GOV.UK, how long copyright lasts, https://www.gov.uk/copyright/how-long-copyright-lasts. SR (search-result summary for the UK rule).
- [48] Indian Copyright Act 1957 and commentary, https://www.indiacode.nic.in/bitstream/123456789/1367/1/a195714.pdf. SR (term figures from a search summary; verify).
- [49] ASCAP, licensing FAQ, https://www.ascap.com/help/ascap-licensing. Read 2026-10-18 by the researcher; not re-read by the advisor on 2026-10-18 (HTTP 403). P. ASCAP does not license sync or mechanical rights.
- [50] ASCAP, Cue Sheet Corner, https://www.ascap.com/help/royalties-and-payment/cue-sheets. Read 2026-10-18 by the researcher; not re-read by the advisor on 2026-10-18 (HTTP 403). P. Cue sheet contents, usage terms and quarterly deadlines.
- [51] OneMusic Australia, Film Screenings, https://assets.onemusic.com.au/images/PDFs/guides/Film-Screenings.pdf. July 2026. P.
- [52] SUISA, screenings in cinemas and film festivals, https://www.suisa.ch/en/Kunden/Musik-in-Filmen/Filmvorfuehrungen/Vorfuehrung-in-Kinos-und-an-Filmfestivals.html. Undated. P. The screening party applies to SUISA.
- [53] US cinema operator comment to the Department of Justice, https://media.justice.gov/vod/atr/ascapbmi2019/pc-642.pdf. 2019-08-09. P as an exhibitor's statement, not law.
- [54] 17 U.S.C. 110, https://www.law.cornell.edu/uscode/text/17/110. Read 2026-10-18. P. The non-profit performance exemption (110(4)) covers only nondramatic musical works.
- [55] Midler v. Ford Motor Co., 849 F.2d 460 (9th Cir. 1988), https://en.wikipedia.org/wiki/Midler_v._Ford_Motor_Co. S. US advertising case.
- [56] Society of Composers and Lyricists, "Performing Rights and Wrongs", https://thescl.com/articles/performing-rights-and-wrongs/. Undated. P.
- [57] Australian Guild of Screen Composers, FAQ, https://www.agsc.org.au/faq. Undated. P (Australian practice).
- [58] Twine, composer prices, https://www.twine.net/blog/music-composer-prices-and-commissions/. 2025-12-02. V (marketplace).
- [59] VI-Control, "Rates for scoring an indie short film?", https://vi-control.net/community/threads/rates-for-scoring-an-indie-short-film.158475/. F.
- [61] Composer-pairing programmes: https://hfa.ucsb.edu/news/santa-barbara-international-film-festival-selects-student-composers-inaugural-scoring-lab ; https://theviolinchannel.com/san-francisco-conservatory-of-music-partners-with-sffilm/ ; https://www.richardmarvin.com/iu-jacobs-school-of-music-students-collaborate-with-film-independents-project-involve-for-sixth-consecutive-year/. SR.
- [62] Christopher Caliendo, "Spot the Film", https://christophercaliendo.com/spot-the-film-5-composer-tips-every-filmmaker-should-know-about-scoringfilmmakers-spot-the-film/. 2025-06-06. S.
- [63] Simpsons Wiki, "Spotting notes", https://simpsonswiki.com/wiki/Spotting_notes. Undated. F (a production description for one show).
- [64] Wikipedia, "Temp track", https://en.wikipedia.org/wiki/Temp_track. S.

**Exemplars**
- [66] Wikipedia, *Up* opening sequence, https://en.wikipedia.org/wiki/Up_opening_sequence. S.
- [67] M. Wozny, "Creating an emotional impact without dialogue: the case study of Pixar's Up", https://studentjournals.shu.ac.uk/index.php/enquiry/article/download/125/125/398. Undated. S.
- [68] Dazed, "How Richard Linklater soundtracked Boyhood", https://www.dazeddigital.com/music/article/22887/1/how-richard-linklater-soundtracked-boyhood. Undated. S.
- [69] Wikipedia, *Coco* (soundtrack), https://en.wikipedia.org/wiki/Coco_(soundtrack). S.
- [70] *Robot Dreams* reporting, https://www.wvxu.org/2024-06-05/a-new-animated-film-follows-a-lonely-dog-and-his-robot-friend-in-new-york-city ; https://fipresci.org/?p=30597. SR.
- [71] BFI, *Stories We Tell*, https://bfi.org.uk/sight-and-sound/reviews/film-week-stories-we-tell. SR.
- [72] Mix Online, sound for *The War*, https://www.mixonline.com/?p=78678. Undated. S.
- [73] Motion Picture Association, Vietnam War sound designer, https://www.motionpictures.org/2018/10/the-vietnam-war-sound-designer-on-enhancing-emotional-memories-of-the-war/. 2018. S.
- [74] Wikipedia, "Room tone", https://en.wikipedia.org/wiki/Room_tone. S.

**Sound libraries**
- [75] Freesound FAQ, https://freesound.org/help/faq/. Undated. P. CC0, CC BY, CC BY-NC; AI-generated uploads permitted if tagged.
- [76] Sonniss GDC Game Audio Bundles, https://sonniss.com/gameaudiogdc/. Copyright notice 2014 to 2026. P. Media production use; no AI or ML training.

**Voice capture and cleanup**
- [78] University of Dayton Libraries, phone recording tips, https://libguides.udayton.edu/oral-history-recording/phone-tips. Undated. P.
- [79] Oral History Association, remote interviewing resources, https://oralhistory.org/?p=10412. Undated. P.
- [80] Audacity manual, Noise Reduction, https://manual.audacityteam.org/man/noise_reduction.html. P.
- [81] Audacity manual, Notch Filter, https://manual.audacityteam.org/man/notch_filter.html. P.
- [82] RNNoise README, https://raw.githubusercontent.com/xiph/rnnoise/main/README. P.
- [83] DeepFilterNet, https://github.com/Rikorose/DeepFilterNet ; releases https://github.com/Rikorose/DeepFilterNet/releases (v0.5.6). P. Windows binary not confirmed (TODO(research)).
- [84] arnndn-models, https://github.com/richardpl/arnndn-models. Archived 2024-06-06. P.
- [85] Resemble Enhance README, https://raw.githubusercontent.com/resemble-ai/resemble-enhance/main/README.md. P. Enhancer is generative; `--denoise_only` mode only.
- [86] FFmpeg filters documentation, https://ffmpeg.org/ffmpeg-filters.html. P.
- [87] FFmpeg download page, https://ffmpeg.org/download.html. Read 2026-10-18. P. 9.0.2 released 2026-09-18.
- [88] Auphonic, privacy, https://auphonic.com/privacy. Footer 2026. P.
- [89] Descript, privacy policy, https://www.descript.com/privacy. Last updated 2025-04-14. P.
- [90] Adobe privacy policy, https://www.adobe.com/privacy/policy.html ; Generative AI User Guidelines, https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html. P. Enhance Speech terms were not readable (TODO(research)).
- [91] Home-video audio forum threads, https://www.digitalfaq.com/forum/video-restore/12328-hum-vhs-vhs-print.html ; https://forum.videohelp.com/showthread.php?p=2441349. F/SR.
- [92] Archival Producers Alliance, GenAI guidelines landing page, https://www.archivalproducersalliance.com/genai-guidelines. S. The full guidelines were not read.

**Loudness and mix**
- [93] EBU R 128 (November 2023), https://tech.ebu.ch/docs/r/r128.pdf. P.
- [94] Ioan Allen, "How Loud is a Movie?" (SMPTE paper, via ISDCF Doc 11), https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf. 2016-03-15. P.
- [95] Production Expert, "Loudness and dynamics in cinema sound", https://www.production-expert.com/home-page/2017/6/21/loudness-and-dynamics-in-cinema-sound. 2017-06-21. S. Includes a small sample of Dutch films.
- [97] Spotify for Artists, loudness normalisation, https://support.spotify.com/us/artists/article/loudness-normalization/. Undated. P.
- [98] Production Expert on AES TD1008 (2021), https://www.production-expert.com/production-expert-1/aes-update-loudness-recommendations-for-audio-only-streaming. 2021-09-23. S.
- [99] DCI audio parameters, https://www.soundandvision.com/content/bits-bijou ; https://files.isdcf.com/papers/IntroToDigitalCinema.pdf. SR. The DCI spec itself was not read (TODO(research)).
- [100] DCP-o-matic forum, "Stereo audio to 6 - 5.1 Audio", https://dcpomatic.com/forum/viewtopic.php?p=10951. 2023-09-06 to 09-09. F.
- [101] Sound on Sound, "Duck Tales", https://www.soundonsound.com/techniques/duck-tales. Undated. S.
- [102] CapCut, audio ducking guide, https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video. SR/V (weak).
- [103] REAPER, purchase page, https://www.reaper.fm/purchase.php. Version 7.82 dated 2026-10-04. P. Read 2026-10-18 (scribe re-read): the discounted licence covers "an individual, and REAPER is only for your personal use", and commercial users with yearly gross revenue up to USD $20,000; a 60-day evaluation "with full functionality".
- [104] Audacity, download page, https://www.audacityteam.org/download/. Read 2026-10-18. P.
- [105] SoundCraft README and docs/gaps.md, https://github.com/storytold/soundcraft ; https://raw.githubusercontent.com/storytold/soundcraft/main/docs/gaps.md. Read 2026-10-18. P. Pre-alpha; no sidechain bus; open correctness bugs.
- [106] Blackmagic Design, Fairlight and Resolve Studio pages, https://www.blackmagicdesign.com/products/davinciresolve/fairlight ; https://www.blackmagicdesign.com/products/davinciresolve/studio. Read 2026-10-18. V. Free-version limits not stated.
- [107] Ardour, https://ardour.org/. Read 2026-10-18. P. GPL v2; Windows price not shown.
- [108] Own measurement, sandbox runs on 2026-10-18 (not a web source). FFmpeg 6.1.1 on synthetic signals: two-pass `loudnorm` (linear confirmed on the speech-like test); `sidechaincompress` with `amix`; `afftdn` with `om=n`; `bandreject` on a 60 and 120 Hz test tone (mean level -34.1 dB to -55.2 dB); ALAC to 24-bit 48 kHz WAV. No family audio. Windows builds were not tested.
- [109] Music Business Worldwide, Stable Audio 2.5 launch, https://www.musicbusinessworldwide.com/stability-ai-launches-ai-model-for-brands-to-create-custom-sounds. 2025-09-11. S. Getty and artist suits against Stability (image suits, per the note).

---

## Changelog

- **2026-10-18, v0.1 (draft).** First draft by the Haiku scribe from `research/music-sound.md` (Sonnet researcher) and `CHARTER.md`. Gaps are marked TODO(research). Conflicts are flagged, not resolved:
  - The REAPER trial date (about 2026-12-28) does not match the February mix window in the schedule, and the research's "January mix" wording does not match either (Decision 7).
  - The Warner v. Udio status is reported inconsistently within one source [15] (TODO(research)).
  - The extended consent card (Template D2) may reveal the project to relatives, and was not checked against the secrecy rules (TODO(research)).
  - The research's "pre-1926" brief is for recordings. The composition cut-off in 2026 is 1930, so public-domain composition dates are published before 1931 (as the notes say).
  - The "story.md Decision 10" cross-reference was checked. story.md states the found-voice rule and refers to Decision 10, and the rule matches the research.
  - The Netflix and DCI spec figures come from secondary sources only (TODO(research)). The "Films to study" list cites the research's exemplar notes, which rely on search summaries for some films.
- **2026-10-18, v0.2 (round 1 review applied, Fable advisor).** Found voice now uses a two-tier rule (Core principle 1; Template D3 adds `addressed_to` and `public_cut_eligible`), citing surprise-ops Decision 18 and film-story Decision 3 at their stricter reading. Schedule rebuilt on G-LOCK 2027-02-06, G-MIX 2027-02-13, G-MASTER 2027-02-20 and the 2027-02-22 run; format.md week-18 dates dropped; rolling chapter locks added; composer from lock ruled out. `source_in_her_life` added to cue_map and the spotting sheet. D2 consent wording decided and routed to the surprise-ops truthful pretext cards. ElevenLabs Enterprise Music Lite exclusion, Suno Remix limit, REAPER dates (trial to 2027-02-26), DX-gated check and master-fader rule added; ASCAP sources tagged as not re-read by the advisor; Step 17 cue-sheet reference corrected to Template C.
- **2026-10-18, v0.3 (round 2 review applied, Fable advisor; Haiku scribe).** Research Deliverables 2, 3d, 3e, F6, F7, Summary 13, Q9, the REAPER row and source [8] now match this playbook (the superseded consent card is withdrawn, not kept); D2 routing is a dated surprise-ops patch by Saturday 2026-11-07, not a round; the DX-gated check measures speech spans only (6 LU kept as the starting threshold, labelled inference); cue_map gained `hard_flag` and `advisor_flag_ref`, with the flag written to `reviews/<chapter>/sound-flags.md`; HER-PUBLIC and HER-PRIVATE added beside tiers 1 and 2, with the T9 ledger path; REAPER's $60 personal-use condition added (purchase page re-read) and the schedule row rewritten.