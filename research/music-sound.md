# Score, songs, voices and the mix for a life film — research notes

Track: `music-sound` (Sonnet researcher). Written 2026-10-18 (Sunday), 19 weeks before the premiere on Saturday 2027-02-27. Scope: research only; nothing here is code to ship or legal advice. Jurisdiction of the premiere is still an open charter decision, so every rights statement is flagged "per the terms as read on 2026-10-18" and must be re-checked for the real country, venue and date [1].

How to read the tags. Each source in the list carries a strength tag. P = primary (the rules or the maker themselves). S = secondary or press. V = vendor, who sells something. F = forum or snippet-grade. SR = seen only in a search-result excerpt, page not read. LOCAL = a file in this project. When the notes say UNVERIFIED, the fact could not be confirmed from a page I actually read. Legend for rights cells in the tables: **Y** = expressly covered by the terms as read; **y** = not expressly stated, a fair reading says yes, get it in writing; **?** = not stated or UNVERIFIED; **N** = excluded as read or not available.

A research-limit note up front: the web-search budget for this run (200 searches per turn, shared by every agent) ran out partway through. The later fact-finding used direct page fetches only, so a number of pages (Artlist, Zapsplat, Soundstripe, Musopen, BBC Sound Effects, IPRS, PRS, BMI, the Udio terms) could not be read. They are listed in the gaps section rather than guessed.

---

## Summary

1. **Nothing "free" or "royalty-free" is automatically cleared for a public screening, and the terms I read mostly say so.** Suno's free tier is personal and non-commercial [11][12]. ElevenLabs' Eleven Music terms (updated 2026-10-09) exclude "film, TV, radio" on every plan except the Enterprise Music tier; Enterprise Music Lite also excludes them (advisor spot-check, reviews/music-sound-round1.md) [19]. Epidemic Sound sends "films intended for theatrical/festival release" to a custom Enterprise licence [32]. Mixkit excludes "CDs, DVDs, Video Games or TV & Radio broadcasts" and is silent on film [38]. The YouTube Audio Library page does not address use off YouTube [40]. Musicbed says "most festivals explicitly reject Creative Commons and 'copyright-free' claims" [35].
2. **Recommended music spine (a lean for the maker to confirm):** one original or relative-performed motif, public-domain tunes in new performances, a small number of cleared songs (at most two), real voices and a lot of silence. AI music is allowed by Principle 4 because it is not a memory, but only as a labelled bed or as temp, never as her songs re-sung [1][4].
3. **Commissioning a composer is the cleanest rights route and the worst fit for "only the maker knows".** Indie composers quote about $100-$500 per finished minute (Twine, 2025-12-02) [58]; one forum snippet puts a short at "$2000" [59]. For 8-12 minutes of score that is roughly $800-$6,000 (our arithmetic). It also brings one stranger into the secret. The fallback path (PD, relative, CC0/CC BY, AI bed, silence) needs no one.
4. **AI music in October 2026.** Suno terms revised 2026-08-10, effective 2026-09-03: Pro and Premier get an assignment of "any Output owned by Suno", but no copyright warranty, and commercial use is tied to permitted downloads [11][12]. Udio has had downloads disabled since 2025-10-29, so it cannot supply a film file [13][18]. Stable Audio 3.0 (2026-05-20) has open weights and a Community Licence that lets small creators own and commercialise outputs, and it can run on the maker's own PC [21][22][23]. Google's Lyria 3 makes 30-second clips in Gemini and up to 3 minutes in Vertex AI preview, with commercial terms I could not confirm [24][25].
5. **Copyright and PRO consequences of AI music.** The US Copyright Office says copyright does not extend to purely AI-generated material and that "prompts do not alone provide sufficient control" [28] (hub and publication dates: [27]). ASCAP, BMI and SOCAN (announced 2025-10-28) register partly-AI works but not wholly AI ones [29][30]. So a purely generated cue has no registrable composer and no writer's share. The cue sheet should say so.
6. **Litigation is live.** Warner has settled with Suno (and, by most reports, Udio), and UMG has settled with Udio. UMG and Sony v. Suno continue; on 2026-08-18 the judge let the labels add a stream-ripping claim, with fair-use summary judgment expected after fact discovery closed on 2026-09-30 [15][16]. A second UMG and Sony suit (2026-09-18, 60,202 recordings) has been filed, and no summary-judgment ruling or settlement was found as of 2026-10-18 (F2) [112][113]. A ruling could land before the premiere, but none is scheduled in anything read.
7. **A venue's PRO licence never covers sync.** ASCAP says it does not license the right to put music in "a motion picture, video or TV program"; that is for publishers [49]. Whether a venue needs a PRO licence for the music inside a film shown there varies: Australia's OneMusic requires an event organiser to hold a Film Screenings licence "regardless of whether there's an entry fee" [51]; US cinema owners say producers clear performance at source [53]; the US non-profit exemption in 17 U.S.C. 110(4) covers only "nondramatic" musical works, not a motion picture [54].
8. **Public domain, 2026 edition.** US compositions published before 1931 and US recordings first published before 1926 are public domain as of 2026-01-01 [45][46]. A modern recording of a public-domain tune is still protected, so use a relative's performance, a Musopen-type recording whose terms you have read, or a pre-1926 US recording. UK and EU rules differ; India uses 60-year terms [44][47][48].
9. **Favourite songs.** A song needs two permissions: publisher (sync) and label (master) [35][36]. Festival-only indie rates are about $500 per side for about 12 months; recognisable names about $800-$1,500 per side; a later step-up can be 3-10 times [36]. There is no sourced timeline, so start the asks now and set a decision gate (below). A cover removes the master fee but not the sync fee [36].
10. **Voice capture.** Set the iPhone to Lossless and Android to 128 kbps or higher; phone on a soft surface about 5-12 inches from the mouth; keep the original file untouched; do not let remote platforms re-compress it [78][79][4]. Ask relatives to send the file as an attachment or shared file, not as a chat "audio message" (chat-app recompression is UNVERIFIED but likely).
11. **Cloud "enhancers" fail the charter test as read.** Auphonic uses content to improve its algorithms by default (business opt-out on request), lets staff listen, and deletes audio after 21 days [88]. Descript lists training AI models among its uses and has a "Share Data with Descript" toggle [89]. Adobe's policy mentions machine-learning analysis with an opt-out and does not mention Podcast; Enhance Speech's own terms were not readable [90]. Family audio stays on the maker's PC.
12. **Local chain:** Audacity Noise Reduction and Notch Filter, RNNoise or DeepFilterNet, ffmpeg `afftdn` and `highpass`, with the listen-to-what-was-removed check [80][81][82][83][86]. Generative "enhancers" that "restore" and "extend bandwidth" (Resemble Enhance's enhancer) invent signal and break the found-voice rule; its `--denoise_only` mode is the only acceptable use [85].
13. **Mix: keep three loudness practices apart.** Cinema is a calibrated playback level (85 dBC pink noise per channel, "fader 7"), not a LUFS target; the movie-loudness metric Ioan Allen proposes "has no absolute value" [94][95]. Broadcast is -23 LUFS, +/-1 LU in live, -1 dBTP [93]. Online is about -14 LUFS on Spotify and -18 for speech in AES TD1008 [97][98]. A venue PA is unknown until the Mon 2027-02-22 run on the real chain (surprise-ops run sheet).
14. **Stereo that folds down safely.** A stereo DCP is normally played as plain L+R in cinemas; do not count on matrix decoding [100]. If a cinema books the film, a professional should make a 5.1 with dialogue in the centre from our stems. Stems: DX, MX, FX, AMB at 48 kHz, 24-bit WAV, matching the DCI audio spec (24-bit, 48 or 96 kHz) [99].
15. **Tools verdict.** SoundCraft calls itself "pre-alpha", has no sidechain bus and has open mix-correctness bugs [105][5]. Use Audacity plus ffmpeg as the proven chain, mix inside the NLE's audio page or in Reaper (60-day full-function evaluation, then $60 discounted licence) [103], and keep SoundCraft for experiments only. I tested the ffmpeg two-pass loudness, ducking, denoise and ALAC-to-WAV commands in a sandbox [108].

---

## Findings by question

### Q1. Beat-level: where music enters, leaves and returns in life films

What each exemplar teaches at beat level. Durations are published cue lengths, not stopwatch timings (this environment cannot play video) [7].

| Film | Where music enters and leaves | How the motif returns | Era songs and diegesis | Where silence works | Rights lesson |
|---|---|---|---|---|---|
| *Up* (2009), "Married Life" montage | Music carries a wordless sequence of about 4:05 picture on a 4:10 cue [7]. Giacchino wrote it first because it "would inform the rest of the story"; Docter asked for something like "one's grandmother's music box", hence a waltz [66]; Giacchino began from the storyboards and wrote a restrained, "quiet and gentle" answer to Carl's loss [65]. | The theme "play[s] throughout the rest of the film, changing in timbre depending on the context" [66]. Tempo drops at upsetting incidents and is "sweetly upbeat" as they grow together [67]. | None; all score. | Music slows at the doctor's office, nearly stops at the unkept promise, and "as instruments drop out of the harmony, leaving only a piano" the hospital beat arrives; the screen fades to black as the music ends [66]. The sequence is "almost completely silent" apart from music, and film-story.md records that the team stripped dialogue and effects from it (its source P2; I did not re-verify that) [66][7]. | An original score owns the motif; no clearance risk. |
| *Coco* | One song, four performances: showy 1:49 (comic, a bell falls), lullaby 1:09, reunion 1:13, credits duet 2:46 [7][69]. | The sincere versions are shorter, plainer and later than the showy one; the long pop duet comes after the payoff as decompression [7]. | The song is diegetic: sung by characters. | The payoff is a very old woman singing along, not a spectacle [7]. | Songs and score had separate composers (songs by Anderson-Lopez and Lopez; score by Giacchino) [69]. A motif can be a song you can afford to own. |
| *Robot Dreams* | "September" was picked for a roller-dance scene, then became the theme because the film runs September to September [70]. | Returns as a piano version, in Robot's whistle, and in the final boombox dance [7]. Berger: "the music is the voice of the characters" [7]. | The song is diegetic (boombox) and score. | Robot chooses not to chase Dog; the reunion is a fantasy [7]. | The production "could not afford" the song for the closing credits [7]. A licensed motif has a whole-film price, not a scene price. |
| *Boyhood* | No score: "A score wasn't going to work, it had to be songs coming from that year or that time period" [68]. | No single motif; "Deep Blue" plays as the film fades to black [68]. | Songs from each year as clocks; they "had to feel like it was coming from your observations" (radio, car, stereo); Linklater tested year-lists on young listeners and used one-hit wonders because they "instantly evoke a period" [68]. | Not documented. | "Get Lucky" and "Hey Ya" were dropped "for copyright reasons" [68]. Era-song design is a rights project. |
| *Stories We Tell* (2012) | The soundtrack is "largely excerpts from Abraham Lass's 1971 Smithsonian recording *Play Me a Movie*" (a period instrument world for the home movies) [71]. | One recording supplies the film's sound world. | Home-movie texture, not hits. | The father's narration is recorded in a studio and shown on screen [71]. | One sonic world is cheaper and more coherent than many songs (search-result summary; UNVERIFIED depth). |
| *The War* (Burns) | Not a score study. | Music rises after the effects drop out. | Sound is matched to what is on screen: "When you see a German 88, you hear a German 88" [72]. | "Nothing makes sound more effective than the absence of sound"; after explosions effects pull back while music rises [72]. | For archival material, restraint and low mix levels [73]. |

**Five rules for a 12-25 minute life film with a public audience** (our synthesis from the table; inference where marked):

1. **One motif, many weathers.** Fix a single theme early and let it change timbre and tempo with her life (music-box waltz to a lone piano), as *Up* does [66][67]. Write or choose it before the other cues, and make sure you own or have cleared it for every venue you may use, because *Robot Dreams* could not afford its theme song for the credits [7].
2. **The sincere version is shorter, quieter and later than the showy one.** Put the comedy on the first, showier use and the feeling on the last, plain one (*Coco* 1:49 against 1:09 and 1:13) [7].
3. **Use era songs as clocks only when the world plays them** (a radio, a car, a kitchen), and limit them to the few you can clear. *Boyhood* needed songs "from that year", lost two to clearance, and still counts as a heavy rights project [68]. For this film, plan at most two licensed songs and carry the other decades by sound (a phone ring, a TV hum) instead of by hits (inference).
4. **Let silence take the hardest beat.** Pull the music out before the loss, not after it: *Up*'s music slows, nearly stops, and strips to a piano before the hospital beat and the fade to black [66]; Burns's mixers pull effects back so the quiet is audible [72]. For the final minute, hard cut to black with no music tail, as film-story suggests [7].
5. **Real voices lead; music steps back and never speaks for her.** Any recorded voice sits above the bed. Her found voice is used only as recorded, never re-cut into a new sentence (Principle 4, story.md Decision 10) [1][4]. Leave a second or two of her own room tone before and after a phrase so it lands (inference).

### Q2. Commissioning a composer in 2026

**Where to find one (only what I actually saw).** Student-composer and fellowship programmes pair composers with filmmakers, which shows the model rather than an open job board: the Santa Barbara International Film Festival's composer mentorship (a strict 15-day deadline for a student score), the San Francisco Conservatory of Music and SFFILM Sound and Cinema Fellowship, Indiana University Jacobs School's work with Film Independent's Project Involve, and an Italian conservatory's call for short films [61]. Working composers talk rates in forums such as VI-Control and r/composer (a "looking for composers" thread exists) [59]. Twine is a freelance marketplace that publishes price bands [58]. SoundBetter, Fiverr, Upwork and local composers' guilds were not read; which are active in the maker's country is UNVERIFIED. The composer-rights societies I did read are the Society of Composers and Lyricists [56], the Australian Guild of Screen Composers [57] and the Canadian guild's 2023 survey [60].

**Cost (2026).** Twine (2025-12-02) puts indie or freelance composers at $100-$500 per minute of finished music and boutique studios at $500-$2,000+ per minute, with projects from "a few hundred dollars for a short indie cue" up [58]. A forum snippet says most ultra-low-budget films pay no more than "$2000 for a short" and that established composers quote $750-$1,500 per minute [59]. Applying the Twine indie band to 8-12 minutes of score gives about $800-$6,000 (our arithmetic). Student or early-career flat fees and credit-only collaborations exist (the programmes above) but I found no price (UNVERIFIED).

**Timeline from picture lock.** I found no sourced turnaround. The Santa Barbara programme gave students 15 days for a short [61]. Our planning figure, an inference: 3-5 weeks from locked picture to final stems for about 10 minutes of music, plus one week for revisions. Composers need exact SMPTE in and out points before they sketch or produce stems, and vague spotting leads to "endless revisions, ballooning timelines, and increased post-production costs" [62].

**What the contract must cover** (checklist; confirm with an entertainment lawyer):
- **Grant, not just ownership.** Sync (music with picture), the recording (the composer's own master), and public performance (collected through the PRO). Media: all media, including festival, theatrical and online. Territory: worldwide. Term: perpetual. Exclusive or not. A sync licence "can be exclusive or non-exclusive and limited by territory and duration", and the client "does not need to own the music copyright" [57].
- **Work for hire versus licence.** Without negotiation, standard clauses often mean "a complete assignment in copyright" [57]. Work for hire does not give up the writer's performing royalties: "Your performing rights are never part of the negotiations", the writer's share is non-transferable, and BMI says "in no case will the writer's share of royalties be paid to the employer" [56]. Our lean for a tribute film: an exclusive, perpetual, worldwide, all-media licence with the composer keeping authorship credit and the writer's share, rather than a buyout, because a buyout costs more and adds nothing the film needs (inference). One survey shows buyout pressure on composers is common (26% of Canadian respondents had been asked for a full buyout) [60].
- **PRO and cue sheets.** The composer's name must be on the cue sheet; cue sheets must reach the PRO before quarterly deadlines [56][50]. ASCAP's 2027 dates govern broadcast-type performances only (F1). The production company is normally responsible for filing [50].
- **Credit and moral rights.** Credit on all copies with prominence equal to other key creatives; check consent to alteration [57].
- **Deliverables.** Stems and a full mix as 48 kHz 24-bit WAV, alternate lengths (full, short, bumper), a tempo or hit-point map, and the project file or MIDI (our additions).
- **No generative AI without disclosure, no uncleared samples, no quoting of uncleared songs** (our additions, supporting Principle 4 and the clearance log).
- **Confidentiality.** Silence about the project until after 2027-02-27, including from her circle (our addition; see the secrecy note below).
- **Revisions and kill fee.** Limit post-delivery changes and agree a kill fee (single-source overview; UNVERIFIED).

**What the composer needs from us.** A locked or near-locked animatic with burned-in timecode; a spotting list with in and out points, durations, hit points, tempo, structure, style and emotional tone [62]; the temp track and why it works; the motif brief (what the theme means, and the two or three moods it must reach); the dialogue map (where voices sit, so music steps back); a "do not touch" list (found-voice zones, silence zones); delivery spec; and the cue-sheet fields [50][63]. A spotting note lists start and stop timecodes, length and a description of each cue [63].

**Secrecy note.** A composer, a pro mixer, a rights lawyer and a venue engineer are all people who learn about the film. The maker is the only person in on it and decides whether to widen that. If one is brought in: brief from a name-free animatic and cue sheet, add a confidentiality clause that runs past 2027-02-27, and choose someone outside her circle (inference).

### Q3. AI music services, read on 2026-10-18

All of these are dated snapshots. AI terms change often, and none of these should be quoted later without a re-read.

| Service | Ownership and commercial terms (what I read) | Public performance, festival, cinema | PRO registrability and labelling | Litigation | Quality and tells | Principle 4 fit |
|---|---|---|---|---|---|---|
| **Suno** (ToS revised 2026-08-10, effective 2026-09-03) [11][12] | Free tier: Outputs only for "lawful, personal and non-commercial purposes". Pro/Premier: Suno "hereby assigns" to you "any Output owned by Suno", but Output "will remain subject to these Terms of Service including any applicable commercial use restrictions", and Suno "makes no representation or warranty... that any copyright will vest in any Output". Commercial use only for Output downloaded through an approved channel; subscribing later does not make earlier free songs commercial [11][12]. "Nothing in this paragraph permits commercial use of any Remix" [11]. Downloads are described as perpetual and unaffected by later cancellation [11] (per a page summary; re-read before relying). | No specific public-performance clause: "perform" appears only in the general bar on commercial use [11]. A paid-plan Output has commercial rights, so a public gathering, festival or cinema is y, but unstated. | A wholly AI composition cannot be registered with ASCAP, BMI or SOCAN; partly-AI works can [29][30]. You may not remove or obscure Suno's fingerprints, watermarks or metadata, and Suno "may publicly identify Output as generated through the Service" [11]. A voice model may only be of your own voice [11]. | UMG and Sony v. Suno active; Warner settled; 2026-08-18 order let the labels add a DMCA 1201 stream-ripping claim; fact discovery closed 2026-09-30 in the first case; a second UMG and Sony suit (2026-09-18, 60,202 recordings, v6 models) is filed; no summary-judgment ruling or settlement found as of 2026-10-18 (F2) [112][113]. Suno retired its earlier models on 2026-09-09, so keep any file made with them (F2) [118]. | V6 launched 2026-09-09; user reports are mixed, with "muddy", "muffled", "flat" mixes [13]. Prices: Pro $10 a month ($8 yearly), 20 downloads; Premier $30 ($24), 60 downloads; Pro has Auto Split to up to 12 stems [13]. | Allowed: it is not a memory. Never upload family audio (the ToS gives Suno a perpetual licence to use content to improve its models [11]). |
| **Udio** | Downloads of audio, video and stems have been disabled since 2025-10-29 under the UMG settlement; terms revised 2025-11-12 reportedly limit output to personal, non-commercial use [18]. A 48-hour download window reopened and closed in early November 2025 [17]. A 2026-10-04 comparison lists no downloads on any plan [13]. One June 2026 explainer says paid plans grant commercial use, which conflicts with the rest [14]. | Not usable: no file to put in a film. | n/a | Warner and UMG settled; Sony v. Udio active [15]. | Praised for cinematic and ambient material by some users [13]. | Udio's own pages confirm downloads are disabled (blog 2025-10-29; Help article restated 2026-02-17) [122][124]. Its terms page is script-rendered, so the commercial-use wording stays UNVERIFIED (F3) [126]. |
| **Stable Audio 3.0** (2026-05-20) [21][22][23] | Open weights for Small SFX, Small and Medium on Hugging Face; Large via API only. "Under the Stability AI Community License, you own your outputs and can distribute and commercialize them freely"; organisations over $1M annual revenue need an enterprise licence (which adds indemnity) [23][21]. Company says trained on "fully licensed data" (AudioSparx and Freesound CC recordings, per the cited paper); not independently verified [23]. | Community Licence is silent on venue types, so y for all. | PRO status as for Suno (wholly AI: not registrable) [29]. | Stability faces separate image-training suits (Getty, class actions) per a 2025 trade report [109]; no music-specific suit found. | Medium makes tracks up to 6:20; Small 2:00; Small SFX is a sound-effects model [22]. Quality claims are Stability's own [22]. Can run locally, so no upload. | Allowed. Local run keeps everything on the maker's PC. |
| **Google Lyria 3 / Lyria 3 Pro** | Gemini app: 30-second tracks, beta, ages 18+, 2026-02-18 [24]. Vertex AI: Lyria 3 Pro up to 3 minutes, public preview, 2026-04-07 [25]. Neither page states commercial rights or indemnity [24][25]: UNVERIFIED. | Unknown. | All outputs carry SynthID; Vertex supports C2PA [25]. Google's prohibited-use policy bars impersonation without disclosure and "claiming it was created solely by a human, in order to deceive" [26]. | n/a | "Designed for original expression, not for mimicking existing artists" [24]. | Allowed; terms to confirm before use. |
| **ElevenLabs Eleven Music** (terms updated 2026-10-09) [19] | "All online and offline commercial use permitted, except film, TV, radio, and Studio Games" on Free, Starter, Creator, Pro, Scale and Business; Enterprise Music has no listed exclusions; Enterprise Music Lite also excludes film, TV and radio (advisor spot-check, reviews/music-sound-round1.md). Free output needs attribution ("denote Eleven Music"). Ownership "in accordance with your Underlying ElevenLabs Agreement". | Film is excluded on every non-Enterprise plan, so festival and cinema are N. A free gathering is ? (not "commercial", but a film). | PRO not mentioned [19]. Streaming disclosure per platform rules [19]. Artist-name prompts are barred on all plans [19]. | Launch deals with Merlin and Kobalt (2025-08-05) [20]. | Claims "studio-grade" music [20]. | Allowed, but unusable for this film without Enterprise. |
| **Others** | Meta MusicGen weights are non-commercial (CC BY-NC) [2]. Mureka, AIVA, Soundraw, Beatoven and similar were not researched; UNVERIFIED. | | | | | |

**Labelling.** Plan a credit line such as "Additional music generated with [tool, version] and arranged by [name]; no real artist's voice or style was imitated." The EU AI Act's Article 50 (page says it applies from 2 August 2026) requires providers to mark synthetic audio machine-readably and deployers to disclose deepfakes, narrowing the duty for an "evidently artistic, creative... work" to disclosure "in an appropriate manner that does not hamper the display or enjoyment" [31]. A music bed is not a deepfake on its face. Applicability to a private-ish screening in a given country, and any delay under EU "digital omnibus" proposals, are UNVERIFIED.

**"AI sound" tells.** Sourced: muddy, flat or muffled mixes in Suno V6 reports [13], and file tags ("made with suno"; C2PA manifest on V6-era WAVs, per a vendor-run blog) [13]. Our listening heuristics, not sourced: loop-like structure with no development, harmonic wandering, mushy transients, smeared stereo, vocals with phoneme blur and cliche lyrics, endings that do not resolve. Test: solo the stems and listen at a cinema-like level before using any cue.

**Fit for this film.** AI is best as temp or as a plain bed under voice. Do not use it for her songs or for anything that imitates a real artist or a real voice. If a Suno cue is used in the film, generate it only while subscribed, download it (do not stream-record), keep the receipt and the download metadata, and log the model and date [11][12].

### Q4. Royalty-free libraries and free sources: what each tier covers

Cells follow the legend above. "Gathering" = a free, non-commercial public screening.

| Source and tier (read date) | Private link | Gathering | Festival | Cinema | Attribution and notes |
|---|---|---|---|---|---|
| **Epidemic Sound, Pro** [32][33] | Y for "online" use (ads, branded content, client social or web work) | ? not stated | N: festival and theatrical go to Enterprise | N | Enterprise gives "a tailored license" for "films intended for theatrical/festival release". "Once a video is cleared through our system, the license is global and perpetual" [32]. If you cancel "you have until your plan's end date to use Epidemic Sound" [33]; the two statements need a written answer. Prices were JS-rendered and not read. |
| **Epidemic Sound, Enterprise** [32] | Y | y | Y | Y | Custom; at least 12-month agreements [33]. Needs a sales conversation. |
| **Artlist** [34] | ? | ? | ? | ? | Not read (pages blocked). Search excerpts: Pro "covers... websites, TV, podcasts and films" for personal and client projects, Social is for personal creators; a sponsored Filmmaker Magazine post says festival screening needs no extra fee; theatrical is not mentioned. UNVERIFIED. |
| **Musicbed** [35] | per quote | per quote | Y with a festival licence | C: broader or custom licence | "Some licenses only cover festival screenings"; sync, master and public performance are separate; "Custom licenses are negotiated"; no prices published. Festivals can "disqualify you, pull the film from the program, or revoke an award" if clearance claims are false [35]. |
| **Mixkit (Free licence)** [38] | Y | y | ? | ? | "No attribution or sign-up required"; not for "CDs, DVDs, Video Games or TV & Radio broadcasts"; film and public screening not mentioned on the page read. Full text sits in a modal I could not extract. |
| **Pixabay (Content Licence, Terms updated 2024-11-18 per page)** [39] | y | y | ? | ? | No audio-specific prohibited uses; no standalone resale; "We do not warrant that any consents or licenses have been obtained"; stop using content if a claim is made. I found no Content ID clause in the Terms (the licence summary returned 403). |
| **YouTube Audio Library** [40] | Y inside YouTube | ? | ? | ? | "Copyright-safe", "won't be claimed... through the Content ID system"; CC BY tracks need a credit in the description; "YouTube can't give legal guidance, including guidance on issues with music that can occur off the platform". Not a default for a screening. |
| **Free Music Archive** [41] | per track | per track | per track | per track | Mostly CC. "Under Creative Commons licenses, incorporating a song into a video is a derivative work, too": No-Derivatives tracks are out; FMA-Limited tracks allow no video use at all ("No video, no redistribution, no broadcast/podcast, etc."). |
| **ccMixter** [42] | per track | per track | per track | per track | "Liberally licensed", free "if you give credit"; per-track licences not enumerated on the page; the site's own text is CC BY-NC 4.0. |
| **incompetech (Kevin MacLeod)** | Y | Y | y | y | CC BY 4.0, credit required; live productions allowed; edits must be disclosed [2][3]. Festival declarations may still be a problem [35]. |
| **Sonniss GDC game-audio bundles** [76] | Y | Y | Y | Y | Royalty-free, no attribution, "media production (games, film, TV, interactive projects) only", no AI/ML training, no resale as sound effects. Latest bundle on the page is GDC 2024. |
| **Freesound** [75] | CC0 and CC BY Y | Y | Y | Y | CC BY needs credit; CC BY-NC bars earning money. AI-generated uploads are permitted if tagged with a GenAI tag, so check the tag on a "CC0" sound. |
| **Musopen** [43] | y | y | ? | ? | Seen only in search excerpts (the site blocked fetches): recordings described as public domain, with requests rather than conditions to credit and not to sell them directly. A secondary guide says its Terms of Use carry older "personal, non-commercial" language. UNVERIFIED. |
| **Soundstripe, Uppbeat, Zapsplat, BBC Sound Effects** | ? | ? | ? | ? | Not read (404, 429, 403 and a blocked fetch). BBC's stated terms in toolchain.md: "personal/educational projects, or licence them for use" [77]. |

**The CC BY-NC trap.** NC bars uses "primarily intended for or directed toward commercial advantage"; FMA admits it is "no authority" on what counts [41]. A free family premiere is probably non-commercial, but the same file then cannot go to a festival with an entry fee, a cinema booking, a sponsored venue or a monetised link. It also fails the "most festivals reject CC claims" test [35]. Keep NC out of the master. Likewise ND: video use is a derivative [41].

**A subscription is not a licence for a screening.** Personal-plan "social" licences usually cover online posting. A cancelled plan can end your right to use the music [33]. Read the tier, quote the sentence, date it, and save a screenshot in the licence log (Deliverable 5).

### Q5. Public domain: composition versus recording, by jurisdiction

Two copyrights sit in every recorded song: the composition (words and music) and the recording (the performance as fixed). A recording can be public domain while the composition is not, and the reverse. The premiere country is undecided, so the table gives the rules as read and flags what to confirm. Not legal advice.

| Jurisdiction | Compositions | Sound recordings | Notes |
|---|---|---|---|
| **United States**, as of 2026-01-01 | Published before 1931: public domain [45][44]. (The brief's "pre-1926" is the recordings cut-off; the composition cut-off in 2026 is 1930.) Duke's list includes "I Got Rhythm", "Georgia on My Mind", "Body and Soul" [46]. | First published before 1926: public domain. 1926-1946: 100 years from publication; 1947-1956: 110 years; to 1972-02-14: protected until 2067-02-15 [45]. Foreign-published recordings: before 1925 public domain [45]. 1925 examples: Bessie Smith's "The St. Louis Blues" with Louis Armstrong, Gene Austin's "Yes Sir, That's My Baby" [46]. Recordings first published inside films follow the film's term [46]. | Terms run to year end, so works enter on 1 January [45]. Later recordings of 1930 songs "remain copyrighted" [46]. The Music Modernization Act and the Classics Protection and Access Act produce these terms [46]. |
| **United Kingdom** | Life of the author plus 70 years (IPO summary, via search result) [47]. | 70 years from first publication (GOV.UK; s.13A CDPA) [47]. | IMSLP lists EU recordings first published 1962 or earlier as public domain, which fits term extensions that did not revive expired rights (our reading; verify) [44]. |
| **European Union** | Life plus 70 [44]. | 70 years; IMSLP's recording cut-off for the EU is first publication in 1962 or earlier [44]. | France and Spain can run longer [44]. Editions can carry up to 30 years of protection in some countries [44]. |
| **India** | Musical work: 60 years counted from the year after the author's death (s.22) [48]. By that formula, authors who died in 1965 or earlier are out of term in 2026 (our computation; verify, and lyrics have a separate author). | 60 years from the start of the calendar year after publication (s.27) [48]. By that formula, recordings published up to 1965 are out of term in 2026 (our computation; verify). | Source is a search-result summary of the Act and commentary, not the statute text. A song free in India may still be protected in the US or EU. |
| **Canada** (IMSLP host rule) | Death before 1972 [44]. | Published 1964 or earlier [44]. | IMSLP serves scores on that basis; US-only public-domain scores sit on a separate US server [44]. |

**Usable sources.** IMSLP for scores (public domain in Canada, US or EU depending on the server; it warns that editions can add protectable material) [44]. Musopen recordings are described as public domain (search-result excerpts), but I could not read its terms and one guide says its Terms of Use are older [43]. Pre-1926 US commercial recordings are free in the US from 2026 [45][46]. A relative's own performance is the safest "recording". The Library of Congress National Jukebox and the Internet Archive's 78 rpm collections were not readable this session (403); UNVERIFIED.

**A relative's own performance.**
- *Public-domain tune:* no composition licence needed (confirm status in the premiere country). The performance is the relative's. Obtain a written release (extend the consent card; see Deliverable 3) for use of the recorded performance in the film, at the gathering, and (if they agree) at festivals, in a cinema and on a private link. Modern arrangements or editions of public-domain tunes may carry their own copyright [44].
- *Copyrighted tune:* the recording is new, so no master licence is needed, but the composition still needs a publisher sync licence: "A cover removes the master fee, but you still need the sync licence" [36]. A venue's PRO licence does not supply it [49].
- *Rights the performer holds:* UK and Indian law give performers separate rights; the consent card should name them (not researched; UNVERIFIED).

### Q6. Licensing her favourite songs

**Process.** Each pre-existing song needs a **sync licence** from the publisher (the composition) and a **master licence** from the label (the recording); "Skipping one is infringement, even if the other is paid" [36]; "You need both" [35]. ASCAP states it does not license the right to record music "as part of an audio-visual work such as a motion picture, video or TV program"; mechanical and synchronization rights "are licensed by writers or publishers", and it points to the music publishers and the Harry Fox Agency [49]. Typical order: identify the publisher(s) and label through ASCAP or BMI repertoire search; ask the publisher first (it fixes the composition price and often the split); then ask the label, usually under a "most favoured nations" (MFN) clause that makes the two sides equal [36]. Ask for the media, territory and term up front: "non-theatrical public screening plus festival plus unlisted online link, worldwide, perpetual or 5 years, with an option to upgrade to theatrical".

**Realistic costs (all third-party and directional, 2026).**
- *Festival-only, lesser-known artists:* about $500 per side with a 12-month window, so about $1,000 per song. *More recognisable names:* about $800-$1,500 per side ($1,600-$3,000 per song). Both figures are Reddit-reported and quoted by a licensing vendor on 2026-10-02 [36]. A Film Independent figure of about $500 per side is the sourced end of the range [37].
- *Beyond festivals:* "into the thousands per song"; one anecdote has $500 festival rights becoming a $4,000 quote when a streamer wanted the short; step-ups of "3 to 10 times" are cited [36]. Negotiate step-up pricing before signing [36].
- *Independent film with distribution:* $10,000-$80,000 per song (unattributed range); "millions" for the highest-profile placements [37].
- *Projects that ran into it:* *Tarnation*'s later spend of about $400,000 on sound, print, score and clearances; *Robot Dreams* could not afford its song for the credits [7].
- *Our reading:* a famous song in a non-commercial public showing might be quoted far below these film-distribution figures, or the rights holder may ignore a micro request. No source speaks to that case. UNVERIFIED.

**Timeline.** No sourced durations; the vendor guide describes slow, email-heavy negotiations without durations and advises making clearance decisions before picture lock [36]. Plan eight to twelve weeks from first ask to signature (inference). With the premiere on 2027-02-27, send the asks by 2026-11-15, set a hard decision gate on 2026-12-14, and lock a substitute by 2027-01-08.

**What a public gathering and a cinema change.**
- *Sync and master do not depend on the room.* The licence's media, territory and term do. A festival-only licence "doesn't carry over if the film is later distributed or streamed" [35].
- *Public performance depends on country.* United States: cinema owners say they take one licence from the distributor and that producers clear performance "at the source" [53]; for a non-profit, no-admission event, 17 U.S.C. 110(4) exempts performance of "nondramatic" musical works but not a motion picture as a whole, and says nothing about sync [54]. Australia: the event organiser needs OneMusic's Film Screenings licence for the music in the film "regardless of whether there's an entry fee", with a minimum fee ($86.52 minimum shown for APRA works, July 2026) [51]. Switzerland: the screening party applies to SUISA for a cinema or festival licence [52]. UK, EU and India venue practice (PRS, GEMA, SACEM, IPRS) was not readable; UNVERIFIED.
- *What a venue's PRO blanket licence covers.* It authorises the venue to play repertoire music to its audience. It never covers sync, mechanical or master rights [49]. Whether it also covers the soundtrack of a film brought in by a guest depends on the country and the licence wording (above). Ask the venue in writing: "Which PRO licences do you hold, and do they name music in films shown here?"

**Substitute patterns ranked from lowest risk to highest.**

| Rank | Pattern | Rights position | Notes |
|---|---|---|---|
| 1 | **No music** (silence, room tone, her voice) | None needed | Strongest Principle 4 and 7 fit; *Up* and Burns show silence working [66][72]. |
| 2 | **A relative performs a public-domain tune** | Release from the performer only | Best sound people can own; the family owns the recording. |
| 3 | **Commissioned or library "mood-alike"** | Composer licence, or a library tier whose text you quoted | Read the tier for the exact use [32][35]. |
| 4 | **A relative performs her actual song** | Publisher sync licence only; no master | "A cover removes the master fee" [36]. Still needs the publisher; PRO does not substitute [49]. |
| 5 | **The title on a card** (text, no sound) | Probably none (a title alone is not music; inference, not researched) | Cheap and honest: "the song she sang badly on purpose". |
| 6 | **The song quoted in narration** (lyrics spoken or shown) | Lyrics are a copyrighted text; quoting more than a few words needs care (inference, not researched) | Keep to a fragment that her relative said in conversation. |
| 7 | **A sound-alike recording** (a person imitating the record) | Still needs the publisher sync licence [36]. Imitating a famous singer's distinctive voice for a commercial purpose was held unlawful in *Midler v. Ford* (9th Cir., 1988, a US, advertising case) [55] | Risky; avoid. |
| 8 | **AI re-singing, voice clone, or a generated cover "in her voice"** | Out under Principle 4; also against the terms of Suno (no voice model of another person), ElevenLabs (no mimicry) and Google (no impersonation) [1][11][19][26] | Anti-pattern only. |

### Q7. Sound design: foley, ambience, room tone, and still photographs

**Free and clearly licensed sources (licence read).**
- *Freesound:* CC0 (use freely), CC BY (credit), CC BY-NC (no earning); read the tag because "AI generated audio... is permitted" if tagged [75].
- *Sonniss GDC bundles:* royalty-free, "media production (games, film, TV, interactive projects) only", no attribution, no AI/ML training, no resale as sound effects [76].
- *BBC Sound Effects:* terms in toolchain.md say "personal/educational projects, or licence them for use"; a public screening is not confirmed, and I could not re-read the page [77].
- *Pixabay and Mixkit sound effects:* Pixabay's Terms list no audio-specific prohibition [39]; Mixkit's SFX licence text was not extractable [38]. UNVERIFIED for festival or cinema.
- *Generated effects:* Stable Audio 3.0 Small SFX (open weights, 459M parameters, up to two minutes, runs locally) [22].
- *Minecraft's own audio:* the Usage Guidelines define the brand's "assets" to include "sounds and other audio from any of our games", and treat sharing as commercial use under the guidelines [10]. Do not rip game sounds or music (the local excerpt of the guidelines is [9]); build a block-and-world sound language of your own for any Minecraft-styled sequence (Principle 2: it must mean something).
- *Your own recordings:* the best and cheapest. Record the empty kitchen of a similar house, a tap, a kettle, a door, a bus stop, with the maker's phone and no people in frame or earshot, at a time she is away. That avoids both consent issues and a tip-off (inference from the charter).

**Room tone.** Each location has its own presence; record 30-60 seconds of "silence" in each room, in mono, with the microphone placed as it was for the voice, and lay it under dialogue edits so the cut does not sound like a dropout; without it the track "goes silent in a way the audience hears as a technical fault" [74] (the 30-60 seconds is our practice, not sourced). Cleaned voice recordings need room tone laid back in, because noise reduction leaves dead air.

**Era ambience.** A starter palette for the decades from the 1970s to now, to be replaced by what the interviews say (inference): a rotary or push-button phone, a pressure cooker, ceiling fans, a cassette player's mechanics, a CRT hum, a dial-up modem, school bells, a bus, a market, a pot on the stove. Source each as CC0, Sonniss or your own, and list it in the licence log.

**How documentary makers score photographs.** The sources I read are about archival film, not stills, so the following is our synthesis, tied to them:
- Build in layers: a continuous room-tone bed per scene, one or two low-level ambiences, and three to six "hero" sounds tied to objects in the picture, then remove them at the hard beat. Burns's sound team matches sound to what is visible ("When you see a German 88, you hear a German 88") and pulls effects away after impact [72].
- Treat weak archive with restraint, mixed "very quietly", so the viewer feels the gap without hearing a fake [73].
- Make the sound serve the story, not the technique: "what are we going to do with sound that is going to deepen the viewer's experience" [73].
- Principle 4 limits: generic, room-level sound under a real photograph is a reconstruction and must be visibly or audibly treated as one (a credit line is enough). No invented crowd speech, laughter, shouting or any person's voice. In animated scenes, sound is part of the animation world and needs no such label.
- Hard chapters: default to silence and room tone. Do not add sirens, monitors or heartbeats to a real loss (the heartbeat and helicopter blend in the Vietnam War sound design suits a war film, not a mother's illness) [73] (inference).

### Q8. Voice capture, cleanup, cloud terms, found voice, and restoring home-video audio

**Phone capture (settings and placement).**
- *iPhone:* Settings > Voice Memos > Audio Quality > Lossless. *Android:* choose a recorder with 128 kbps or higher, or a WAV option (app names UNVERIFIED) [78].
- Quiet room with soft things in it (rugs, curtains, cushions; a closet works); switch off fans and fridge; Do Not Disturb on; phone plugged in [78][4].
- Place the phone on a folded towel or stand, not in the hand, with the microphone uncovered. For one speaker, 5-6 inches [78] or 6-12 inches [4] from the mouth. For two speakers, the guides say only "as close to both speakers as possible" [78]; the two-speaker distance is settled by story.md's Exercise 2, with the one-phone-per-person option as the ideal [4].
- Run a second phone as a backup [4]. Say a slate (name, date, "test") first, then play it back with headphones.
- Keep the original. The Oral History Association: record uncompressed if possible; most platforms compress to MP3 or MP4; "re-saving a compressed file compresses it again"; archives want WAV or Broadcast WAV, with FLAC and AIFF acceptable [79].
- *Remote collection through a channel she never sees.* The relative records on their own phone (Voice Memos "can share a recording as one .m4a file" via AirDrop, Mail or Messages [6]) and sends it as an email attachment or a shared-file link into an inbox only the maker reads, or hands over a USB stick. Phone recordings are "likely the most secure way to conduct a remote interview" [79]. Chat apps' voice-note recompression was not read and is UNVERIFIED.
- *Format check on arrival.* `ffprobe` the codec (ALAC or AAC) and keep it as received. Make a working copy with `ffmpeg -i in.m4a -c:a pcm_s24le -ar 48000 work.wav`. Converting a lossy file to 24-bit WAV changes the container only, not the quality (tested for ALAC to WAV; [108]).

**The free local cleanup chain (all on the maker's PC).**
1. *Hum:* Audacity Notch Filter at the mains frequency (60 Hz in North America; 50 Hz in the UK and most other countries), then at the harmonics with a Q between 2 and 10 [81]; optional mild Noise Reduction after [81]. Or ffmpeg `bandreject` at 60 and 120 Hz (sandbox: mean level on a synthetic 60/120 Hz tone fell from -34 dB to -55 dB [108]).
2. *Rumble:* `highpass=f=80`.
3. *Broadband noise:* Audacity Noise Reduction. Learn a noise profile from at least 2048 samples of noise only; the manual says a longer sample is better and that "higher values than necessary... will result in damage to the audio that remains"; keep Sensitivity as low as works because low values show artifacts [80]. For batch work, ffmpeg `afftdn` (default 12 dB reduction, -50 dB noise floor) [86].
4. *Neural denoise (optional):* DeepFilterNet's `deep-filter` takes 48 kHz WAV only and has a Windows-supported framework (MIT/Apache dual licence); the latest release I saw was v0.5.6 (31 Aug), and whether a Windows .exe is among its assets was not shown [83]. RNNoise (Xiph) is a library; its demo works on raw 16-bit 48 kHz PCM, not WAV [82]; ffmpeg's `arnndn` needs a model file such as `std.rnnn` from the archived arnndn-models repo [84][86].
5. *Listen to what you removed.* `afftdn` has `output_mode=noise`; `arnndn` has `mix=-1` ("hear actual noise removed from input signal") [86]. If consonants and breaths are in the removed track, back off.
6. *Level, not squash.* Ride levels by hand; avoid heavy compression on found voice.
7. *Check artefacts.* Watch for musical-noise warble, dulled consonants, "underwater" smear, chopped reverb tails and a dead-air floor between words. Always A/B at matched loudness and keep the original on a separate track.
- *Do not use generative "enhancers" on her found voice.* Resemble Enhance's enhancer "restor[es] audio distortions and extend[s] the audio bandwidth"; that synthesises signal. Its `--denoise_only` mode is the only acceptable use (MIT licence, local) [85]. The same logic applies to cloud tools such as Adobe's Enhance Speech (its mechanism is UNVERIFIED).

**Privacy and training terms of cloud enhancers, read on 2026-10-18.**

| Service | What the page says | Charter verdict |
|---|---|---|
| **Auphonic** (privacy page, no effective date; footer 2026) [88] | Uses content to improve its algorithms; "your Content may be viewed and/or listened to by an Auphonic employee or any person contracted by Auphonic"; business customers can opt out of training by contacting Auphonic; audio files deleted after 21 days, video after 7; processed mainly on Hetzner servers in Germany with Cloudflare R2 storage. | No. Training and human access by default. |
| **Descript** (privacy policy last updated 2025-04-14) [89] | Lists "training our artificial intelligence models" among uses; "Share Data with Descript" can be turned off; voiceprints kept up to three years after last access; Studio Sound not mentioned. | No. |
| **Adobe Podcast Enhance Speech** (Privacy Policy updated 2025-10-24; Gen-AI guidelines updated 2026-05-15) [90] | The privacy policy says Adobe analyzes content "using techniques such as machine learning in order to improve our Services", subject to an opt-out, and does not mention Podcast. Enhance Speech's own terms were not readable (the product page returned a title only). Generative-AI inputs and results "may be reviewed". | No. UNVERIFIED terms; not read. |
| **StoryCorps Connect and similar** | Already ruled out in story.md Decision 9: its terms give StoryCorps a perpetual licence [4]. | No. |

The rule is simple: family audio stays on the maker's PC unless a named batch's terms were read on the date and the maker said yes in writing (charter) [1].

**Her found voice (home video, voicemail, tapes): rules.**
- *Use as recorded.* Allowed: level, high-pass, hum and noise reduction, clean fade in and out, trimming silence at head and tail. Not allowed: re-cutting into new sentences, splicing across pauses, looping, stretching, pitch change, bandwidth extension, dubbing under a different picture so it means something else, or any synthetic extension of the voice (Principle 4; story.md Decision 10) [1][4].
- *Cut only at natural pauses between full utterances,* never inside a sentence. Say in the credits that these are her own recorded words with the year and the source ("recorded 1998, from a family video").
- *Everyone heard needs a consent status.* The story.md found-voice inventory already records the consent status of everyone heard [4]; add a column for the other voices in the clip (children, friends, relatives), including the dead, whose use needs the closest family's yes [6].
- *Law and ethics (jurisdiction flagged; do not conclude):* who owns the recording (usually whoever made it); the speaker's privacy and publicity rights; data-protection rules if the premiere is in the UK or EU, where a voice can be personal data and the household exemption is narrow (see F6: the EDPB household-exemption guidance reads that exemption narrowly, so a public screening falls outside it) [6][133]; personality-rights case law in India and state publicity rights in the US (not researched). This is one question for a lawyer, or the maker's own judgement: "May I play a private recording of her voice, made by a family member, to a public audience that includes her, at an event she does not know about?" The answer should be written into the plan before the voice is used (Principle 5 and 7).
- *Credit what is generated.* The Archival Producers Alliance's guidance for generative material in documentaries is to log and disclose it; I read only its landing page, so treat the details as UNVERIFIED [92][7].
- *Dignity.* Any recording she might not want a public to hear stays out. The Bourdain case shows how synthetic voices of a real person went wrong [6].

**Restoring home-video audio (hum, hiss, azimuth, dropouts).** Sources here are forum-grade (VideoHelp and DigitalFAQ threads seen in search results) plus the Audacity manual [91][81]:
- *Capture first.* Clean the heads and play from the best-behaved deck; many decks default to the Hi-Fi track, and if Hi-Fi sounds fluttery or harsh from mistracking, adjust tracking, or use the lower-quality linear track instead [91]. Capture at 48 kHz, 24-bit [99] with the original tape kept.
- *Hum* shows as 60 Hz plus a larger 120 Hz component from power-supply ripple; a notch filter usually removes it [91][81]. Check for a ground loop in the capture chain before filtering.
- *Hiss* is harder than hum, and Audacity is "okay" but results vary; one user reported total silence from over-aggressive settings [91]. Use the lowest reduction that works and keep the original.
- *Azimuth* (cassette head alignment) and *dropouts* were not covered by a source I could read; do these on the playback side (best deck, adjust, re-capture) before software repair. UNVERIFIED.
- *Video audio is often 8-bit-equivalent in noise floor.* Do not over-clean; leave some room tone.

### Q9. The mix: dialogue forward, ducking, stereo versus 5.1, three loudness practices

**Dialogue-forward rules** (practitioner guidance; no film-mixer source found that gives a single universal depth):
- Voice is the lead. Music sits under any real voice; keep it clear in the 1-4 kHz speech band by EQ rather than only by level (our practice).
- *Ducking by sidechain:* Sound on Sound recommends a "low ratio (say, 2:1)", a "medium fast attack (maybe 15 or 20 ms)", a long release "sometimes as much as 600 or 700 ms" so the music does not rise during short pauses, a threshold set by ear, and "as unnoticeable as possible" [101]. A creator guide suggests 6-12 dB of duck with 30-80 ms attack and 250-700 ms release (snippet-grade) [102].
- *Ride by hand for the key lines.* The sidechain gives a starting curve; the film's most important lines are handled with fader automation (practice).
- *Small-room reality.* Cinema fader levels are often lowered from reference, which causes "severe dialog intelligibility problems" [94]. Make dialogue intelligibility robust: a clean DX stem, music under it, no loud music peaks immediately after a quiet line.
- *The ffmpeg sidechain (tested):* `[music][dx]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=700` with `asplit` on the dialogue and `amix=normalize=0` ran correctly in the sandbox [86][108].

**Three loudness practices, kept apart.**

| | **Cinema (DCP in a calibrated room)** | **Venue PA / projector speakers** | **Online (private link, YouTube, streaming)** |
|---|---|---|---|
| **What defines the level** | A calibrated acoustic level, not a LUFS number. SMPTE-style alignment sets 85 dBC per speaker on pink noise at -20 dBFS (the exact value is disputed: Katz argues 83 dB) with the processor at "fader 7"; the correctly aligned theatre "will reproduce the level heard by the director and mixer" [94][95]. | Unknown until you test it. The operator sets the master fader. | The platform normalises. |
| **Numbers** | Average dialogue sits roughly 7-9 dB below reference (about 76 dBA); measured dialogue in 24 mainly Dutch films ran from -41 to -25 LUFS; a proposed cinema Program Level limit is -27 LUFS [95]. Ioan Allen's Leq(m10) "has no absolute value" and is "in no way" a regulation of features [94]. Netflix's streaming spec asks about -27 LKFS dialogue-gated, +/-2 LU, -2 dBTP (search snippet; page unreadable) [96]. | Starting point for the file, our inference: **-18 LUFS integrated** (AES TD1008: -18 for speech content [98]), true peak -1.5 dBTP, loudness range under about 8-10 LU. Make alternates at **-23** (quiet hall, broadcast-like [93]) and **-16** (noisy room), then pick at the rehearsal. | Spotify normalises to -14 LUFS, true peak -1 dB max, and keeps -2 if louder than -14 [97]. AES TD1008 (2021): -14 for the loudest album track, -18 for speech [98]. toolchain.md uses -16 LUFS, -1.5 dBTP [2]. YouTube's -14 figure is secondary only (UNVERIFIED) [13]. |
| **Who sets the final fader** | The cinema chain. Trailers cap at 85 dB Leq(m) under TASA; features are not regulated [94]. | You, on the day. | The platform. |
| **What to deliver** | Stems and a stereo mix with ample headroom (peaks around -3 to -6 dBFS, not squashed), mixed at a calibrated level by a professional if a cinema books it (inference). **No LUFS normalisation.** | One master video with embedded audio plus a standalone 48 kHz 24-bit stereo WAV for the PA desk. | An AAC or H.264 file with the -16 LUFS master. |

For comparison, the broadcast reference is EBU R 128 (November 2023): programme loudness normalised to -23.0 LUFS, a tolerance of +/-1.0 LU where exact attainment is not practical, and a true peak no higher than -1 dBTP [93]. It is none of the three columns above, but it is the figure the -23 alternate borrows.

**Do not use single-pass dynamic `loudnorm` on the cinema or venue master.** ffmpeg's `loudnorm` has a dynamic and a linear mode, upsamples to 192 kHz in dynamic mode (so set `-ar 48000`), and only goes linear if all four measured values are supplied (`measured_I`, `measured_LRA`, `measured_TP`, `measured_thresh`) [86]. The tested recipe is a measure pass, then a linear pass; check that the second pass prints "Normalization Type: Linear" [108]. toolchain.md's `-af loudnorm=I=-16:TP=-1.5:LRA=11` is fine for the online copy but would squash a quiet life film's dynamics if used as the master [2].

**Stereo versus 5.1.** The DCI audio spec is 24-bit PCM at 48 or 96 kHz with up to 16 channels (a forum copy and secondary sources, not the spec itself) [99]. Stereo DCPs "are normally played back as plain L+R", and ISDCF discourages matrix audio, so do not count on a Pro Logic-style up-mix; DCP-o-matic's Mid-Side Decoder can build a centre but is a workaround [100]. For this film: **mix stereo that folds down safely** (check mono sum, dialogue dual-mono centred, no out-of-phase wide effects). If a cinema books the film, a professional makes a 5.1 from our stems with dialogue in the centre channel; do not attempt it alone (inference).

**Stem deliverables (48 kHz, 24-bit WAV, same length, start at 00:00:00:00):** DX (found voice and relatives, each on its own sub-track, originals archived), MX (score and songs), FX (spot effects and foley), AMB (room tone and ambience), plus a stereo full mix and an M&E (music and effects without dialogue) in case of a second-language version. The 48 kHz 24-bit spec follows the DCI audio parameters [99].

**Where to listen.** The venue test: at the Mon 2027-02-22 run on the real screen and speakers (surprise-ops run sheet; the format.md week-18 dates are not used), from the front row, the back row and a side seat. Also on laptop speakers, a phone, earbuds and in mono. Use a calibration reel with no story in it (pink noise, a sweep, your own voice reading a neutral text, and one music bed) so the venue's engineer does not see the film. A phone SPL app is a relative check only (accuracy UNVERIFIED).

**Tool verdict for this film's mix.**
- *SoundCraft:* README says "pre-alpha: it covers 94 % of the incumbent's menu items (measured)", about 40% of the way to replacing a professional DAW; it exports WAV at 16, 24 or 32-bit float and reports peak, true peak and LUFS on bounce [105]. The gaps list says "No sidechain (key input) buses for any host", no AAF/OMF, about 25 open correctness bugs, Windows only lightly exercised, and loudness metering is not mentioned [105]. Issues #710 and #707 (MP3 and AAC import can silently shorten or shift audio) are recorded in craft-motion.md [5]. Verdict: experiments only, WAV and FLAC only, never for delivery.
- *Audacity plus ffmpeg:* the proven chain. Audacity lists version 4.0.1 on its download page (release date not shown; Windows x86_64 and ARM64) [104]; pin the version you tested. FFmpeg 9.0.2 was released 2026-09-18, with Windows builds from gyan.dev and BtbN [87]. Use Audacity for repair and listening, ffmpeg for batch work, conversion and loudness measurement.
- *A free-to-evaluate DAW:* REAPER 7.82 (2026-10-04) has a 60-day evaluation with "full functionality"; $60 discounted licence for an individual using REAPER only for personal use, or for an individual or business using it commercially with yearly gross revenue up to $20,000; $225 commercial [103] (the purchase page re-read by the scribe on 2026-10-18 confirms the personal-use condition). The 60 days will not stretch to the premiere from today (132 days), so start the trial around 2026-12-28 to cover the 13–20 Feb mix (G-MIX to G-MASTER), or buy the $60 licence (personal use qualifies). Start the trial only to defer the spend to 2026-12-28. Ardour 9.8 is GPL v2; its Windows binary price was not shown [107].
- *DaVinci Resolve Fairlight:* the Fairlight page lists a ducker, a de-hummer, loudness meters and surround formats up to 22.2; the only items it marks Studio-only are immersive 3D audio, the foley sampler and the extra FX; which of the rest are in the Free version is not stated (UNVERIFIED) [106]. Studio's neural voice isolation is a generative-adjacent tool and not needed.
- *Lean:* mix inside the NLE's audio page or in REAPER; repair in Audacity; measure and convert in ffmpeg; keep SoundCraft for experiments. Apply the final-mix rule: decide once, pin versions in the log.

### Q10. Temp track to final

- **Spotting the animatic.** Lock the picture or use a near-lock cut, burn in timecode, and list each cue's start and stop, its function (motif, clock, silence pull-out, protected-voice zone), its hit points and its mood in plain words, using reel and cue numbers such as 1m1, 1m2 [62][63]. Fill the spotting template in Deliverable 2.
- **Temp music and "temp love".** A temp track is "a guideline for the tempo, mood or atmosphere" and is normally swapped for an original score; some argue it constrains the composer [64]. "Temp love" (attachment to the temp until nothing else sounds right) is a standard industry term; no page I read defines it (UNVERIFIED). Counter it by (a) using two different temps for a key cue, (b) muting the temp and testing silence on at least three cues, (c) briefing the composer on what the temp does, not what notes it plays, and (d) keeping the motif from the temp track's own melody.
- **Temp rules for this project.** Temp stays on the maker's PC and out of any copy shown to anyone; mark it `TEMP-UNCLEARED` in the licence log; never upload it to a cloud or share it with a family member; no temp with a real artist's voice re-created by AI. The charter's cloud rule applies [1].
- **When to commission or generate.** Decide per cue by 2026-12-14. Commission when the cue carries the motif or the emotional peak. Use PD, relative or library for everything else. Use AI only for beds under voice, as temp, or for SFX, with the rights steps in Q3. Do not generate a cue and then hope to clear it.
- **Replace temp without re-cutting.** Cut the picture to timecode, not to the temp's beats; give the composer a hit-point map; ask for a mock-up two weeks before final; allow only a few frames of picture change after lock; get alternate lengths (full, 30 s, bumper) and 1-2 second handles; drop the stems in at the same timecode and move the music, not the picture.
- **Cue sheet.** A cue sheet is "a schedule of the music contained in a film" listing the title, how it was performed (visual instrumental, vocal, background instrumental or vocal), the duration, and the composers and publishers with ownership shares; the production company usually files it, and PRO deadlines are quarterly (ASCAP: submission by 2027-01-01 for the March and April 2027 distributions, 2027-04-02 for June and July) [50]. Festivals and cinemas also ask for one; add the licence references and an AI-generated flag. If the film never leaves the family and a venue, a cue sheet is still the best clearance record for theatrical-delivery.

---

## Exemplars and what they teach us

- **Up.** The motif is written first and returns in changed timbre; the loss beat is carried by subtraction (slow, near-stop, a lone piano, fade to black) rather than addition [66][67]. Teaches: the sound of grief is the music taking things away.
- **Coco.** Song as shortest-last: showy 1:49, sincere 1:09 and 1:13, credits 2:46 [7][69]. Teaches: how a motif's cost and weight are distributed across the film.
- **Robot Dreams.** A single cleared song as theme and as "voice"; lack of budget for the credits [7][70]. Teaches: price the whole film's use, not a scene.
- **Boyhood.** Songs-as-calendar, no score; two titles cut for rights [68]. Teaches: era songs are the most expensive way to date a scene; sound can date it for free.
- **Stories We Tell.** One recording supplies the film's sonic world; the father's studio narration is shown [71]. Teaches: one coherent palette beats many songs (search-result level; UNVERIFIED depth).
- **The War and the Vietnam War series.** Sound designed to what is on screen, with restraint for weak archive, and silence as the strongest effect [72][73]. Teaches: how to design for still photographs without faking events.
- **Tarnation.** Made for $218.32; the distributor spent about $400,000 on sound, print, score and clearances afterwards [7]. Teaches: the largest hidden cost of a personal film is rights, not production.

---

## Templates and deliverables

### Deliverable 1. Music-strategy decision matrix

Legend: **Y** expressly covered as read; **y** not expressly stated, fair reading says yes (confirm in writing); **C** covered only if the contract or licence says so; **?** unstated or UNVERIFIED; **N** excluded or unavailable. "Gathering" = free, non-commercial public screening on 2027-02-27. Read on 2026-10-18; not legal advice; the premiere country is open.

**Table 1A. Rights coverage**

| # | Option | Private family viewing | Public gathering | Festival | Cinema (booked) | Online private link | Basis |
|---|---|---|---|---|---|---|---|
| 1 | Commissioned score, exclusive all-media licence | C | C | C | C | C | Draft per Q2 checklist [56][57] |
| 2 | Commissioned score, work for hire or assignment | C | C | C | C | C | Same; writer's share stays with the composer [56] |
| 3 | Relative plays a public-domain tune | C | C | C | C | C | Written release from the performer; confirm PD status in the venue's country [44][45] |
| 4 | Relative plays her actual (copyrighted) song | C | C | C | C | C | Publisher sync licence needed; no master [36][49] |
| 5 | Pre-1926 US recordings of a public-domain composition | Y | Y | y | y | Y | Per country; US rule [45][46] |
| 5b | Musopen recordings, until its terms are read | ? | ? | ? | ? | ? | Musopen terms not read: every path returned 403 (F4) [43][127] |
| 6 | CC0 or Sonniss/Freesound CC0 sounds | Y | Y | Y | Y | Y | Check the GenAI tag on Freesound [75][76] |
| 7 | CC BY (incompetech, Freesound CC BY, FMA CC BY) | Y | Y | y | y | Y | Credit; festivals can reject CC claims [35][2][41] |
| 8 | CC BY-NC | Y | ? | N | N | ? | NC trap [41][35] |
| 9 | CC BY-ND, FMA-Limited | N | N | N | N | N | Video is a derivative; FMA-Limited bars video [41] |
| 10 | Subscription library, standard/online tier (Epidemic Pro) | ? | ? | N | N | Y | Online only; festival/theatrical = Enterprise [32][33] |
| 11 | Library enterprise or per-project licence (Epidemic Enterprise, Musicbed) | C | C | C | C | C | Negotiate scope; Musicbed prices by quote [32][35] |
| 12 | Free sites: Pixabay, Mixkit, YouTube Audio Library | y | y | ? | ? | y | Pixabay Terms silent on audio and Content ID [39]; Mixkit excludes TV/radio/CD/DVD/games [38]; YouTube silent off-platform [40] |
| 13 | Suno free tier | Y | N | N | N | N | "personal and non-commercial" only [11][12] |
| 14 | Suno Pro/Premier, downloaded while subscribed | Y | y | y | y | Y | Assignment of Output, no copyright warranty, commercial via downloads; no public-performance clause; "Nothing in this paragraph permits commercial use of any Remix" [11][12] |
| 15 | Stable Audio 3.0 local, Community Licence | Y | y | y | y | Y | Under $1M revenue [21][23] |
| 16 | ElevenLabs Eleven Music (not Enterprise Music) | ? | ? | N | N | ? | Film/TV/radio excluded on every plan except the Enterprise Music tier; Enterprise Music Lite also excludes them [19] (advisor spot-check) |
| 17 | Udio | N | N | N | N | N | Downloads off [13][18] |
| 18 | Google Lyria 3 / 3 Pro | ? | ? | ? | ? | ? | Commercial terms not found [24][25] |
| 19 | Licensed song, sync + master | C | C | C | C | C | Media, territory, term as signed [35][36] |
| 20 | Human sound-alike of a famous recording | C | C | C | C | C | Publisher sync still needed; imitation risk [36][55] |
| 21 | AI cover, re-singing or cloned voice | N | N | N | N | N | Principle 4; also barred by tool terms [1][11][19][26] |
| 22 | No music, room tone and her voice | Y | Y | Y | Y | Y | Nothing to clear |

**Table 1B. Cost, timeline, quality, Principle 4 and secrecy** (costs 2026; ranges are directional)

| # | Cost | Timeline (plan) | Quality | Principle 4 fit | Secrecy fit (only the maker knows) |
|---|---|---|---|---|---|
| 1-2 | About $100-$500 per finished minute indie [58]; roughly $800-$6,000 for 8-12 min (our arithmetic) | 3-5 weeks after lock + 1 revision week (inference); a student score can run to 15 days [61] | Highest ceiling; depends on the person | Fully fits (a human wrote it) | Poor: one stranger learns of the film. Mitigate: name-free brief, confidentiality clause |
| 3 | $0 | Days | Heartfelt; technical quality varies | Best: a real family sound | Needs a relative in on a pretext (consent card) |
| 4 | Sync fee only, about half of a per-song price (festival indie about $500 per side) [36] | 8-12 weeks (inference) | As recorded | Fits | Same as 3, plus a publisher email |
| 5 | $0 | Days | Old recordings: variable; check noise | Fits | Good |
| 6 | $0 | Days | Generic to good | Fits | Good |
| 7 | $0, with credit | Days | Generic to good | Fits | Good |
| 8-9 | n/a | n/a | n/a | n/a | n/a |
| 10-11 | Subscription price not read; Enterprise 12-month minimum [33]; library lifetime example $500-$600 for 5 tracks (vendor case study) [36] | Days to weeks | Library music sounds like library music | Fits | Good |
| 12 | $0 | Days | Generic | Fits | Good |
| 13-14 | Pro $10 a month ($8 yearly), 20 downloads; Premier $30 ($24), 60 [13] | Hours | Good beds; vocals and mixes often "muddy" [13] | Allowed with a credit; no artist imitation | Excellent (no one else) |
| 15 | $0 (needs a capable PC; hardware unspecified) | Hours | Company claims only [22] | Allowed | Excellent, local |
| 16-18 | n/a | n/a | n/a | n/a | n/a |
| 19 | Festival-only $500-$3,000 per song; distribution and cinema far more [36][37] | 8-12 weeks (inference) | The real record | Fits (it is real) | Requires an outside request (publisher, label) |
| 20 | Sync fee plus session cost | Weeks | Hit or miss | Risky | Needs a singer |
| 21 | n/a | n/a | n/a | Out | n/a |
| 22 | $0 | n/a | Often the strongest choice | Strongest | Best |

**Reading the matrix for this film.** Rows 22, 5, 6, 7, 3 carry no rights risk; rows 1, 14 and 15 give the film a score; row 19 buys her one song. A workable stack that keeps the secret: 3 + 5 + 22 + 6/7, with 14 or 15 as beds, and 19 for one or two songs.

### Deliverable 2. Temp-track-to-final workflow, spotting-notes template and cue sheet

**Workflow (owner: the maker; "log" = the licence log in Deliverable 5).**

| Step | When | What | Output |
|---|---|---|---|
| 0. Cue map by type | now to 2026-11-14 | From film-story's beat sheet `music_cue` column, assign each beat a cue type: MOTIF, CLOCK (era song), BED, PULL-OUT (silence), VOICE-ZONE (no music), END (no tail) [7]. List "what was playing in the house" for each decade, from low-key asks | `cue_map.csv` |
| 1. Build the temp | 2026-11 | Temp from cleared or CC0/CC BY tracks you could keep, plus AI scratch beds; commercial temp only if flagged `TEMP-UNCLEARED` and kept on the PC | Animatic with temp, log rows |
| 2. Spot | when animatic v2 is about 80% locked | Fill the spotting sheet below; run the "temp love" tests (mute temp on three cues; two temps for the key cue) | `spotting.csv` |
| 3. Decide per cue | by 2026-12-14 | commission, generate, PD, relative, library, song or none; update the log | Decision list |
| 4. Make and clear | 2026-12-06 to each chapter's `locked=1` (last at G-LOCK 2027-02-06) | Composer or AI beds; PD and relative recordings with releases; sync asks sent by 2026-11-15; substitute locked by 2027-01-08. A composer from lock is not feasible on this calendar | Files plus log rows `cleared` |
| 5. Replace temp | Per chapter from 2027-01-17 (rolling locks); all by G-LOCK 2027-02-06 | Drop stems in at the same timecode; move music, not picture | Conformed music stem per chapter |
| 6. Mix and masters | Mix v1 at G-MIX 2027-02-13; three masters by G-MASTER 2027-02-20 | Deliverable 4 (DX-gated check added) | Three masters plus stems |
| 6b. Venue test | Mon 2027-02-22 (surprise-ops run sheet) | Calibration reel, then the film on the real chain; the maker holds the fader | Fader position on the run sheet |
| 7. Cue sheet and clearance pack | by 2027-02-25 | Final cue sheet, log freeze, receipts | Feeds theatrical-delivery's clearance log |

**Rolling chapter lock.** Sound work on a chapter begins when that chapter is marked `locked=1` in `status.csv`. The vertical slice (G-SLICE, 2026-12-20) is the exception: its DX cleanup, ambience and effects start in December. A composer working from G-LOCK is out on this calendar.

**Spotting-notes template** (one row per cue; reel-and-cue numbering as in [62][63]):

```
cue_id,reel_cue,chapter,tc_in,tc_out,dur_s,picture_note,function,source_in_her_life,motif,mood_words,tempo_or_feel,hit_points_tc,pull_out_points_tc,voice_present,voice_id,dialogue_priority,temp_ref,source_plan,rights_state,ai_used,notes
C07,1m7,C3-kitchen,01:06:12:00,01:07:38:12,86.5,"photo of the kitchen table, slow push-in",BED,"[beat-sheet evidence ID] (illustrative: a relative named the waltz)",A (waltz),"warm, slightly worn","slow 3/4, music-box","01:06:40:00 (hand enters)","01:07:30:00 (music out, room tone only)",yes,V-uncle-02,voice leads,TEMP-incompetech-Floral,composer,pending,no,"no cymbals; leave 2 s of room tone before her voice"
```

**Cue-sheet template.** ASCAP lists the information a cue sheet needs: programme identification, music title, duration, "how the music was used (e.g. visual instrumental, visual vocal)", entitled parties (songwriters, composers, publishers) with ownership shares, and the production company's contact details [50]. The project adds licence and AI fields.

```
program_title,program_year,cue_no,music_title,usage,duration_mmss,tc_in,composer_1,composer_1_pro,composer_1_share,publisher,publisher_pro,publisher_share,master_owner,source_type,licence_ref,ai_generated,ai_tool_version,notes
"Life Journey (working title)",2027,1m1,"Waltz for [Name]",background instrumental,01:26,00:03:12:00,"[Composer]",ASCAP/BMI/PRS/IPRS,50,"[Composer publishing]",...,50,"[Composer]",commissioned,L-0003,no,,
```

Usage terms: visual vocal, visual instrumental, background vocal, background instrumental, theme, logo, main title, end credit [50] (check the template for exact terms).

### Deliverable 3. Discreet voice-capture kit

**3a. What a relative does (plain-language card; edit before sending).** Pair it with the existing "voice letter" prompt in surprise-ops [6].
1. iPhone: Settings, Voice Memos, Audio Quality, **Lossless**. Android: use the recorder's highest quality, 128 kbps or more [78].
2. A quiet room with soft things (a bedroom with the door shut; a closet works). Turn off fans, TV, fridge sounds if you can [78].
3. Phone on a folded towel or cushion on a table, microphone at the bottom edge uncovered, about a hand's length (6 inches) from your mouth. Do Not Disturb on, plugged in [78][4].
4. Say your name, today's date, and "test", then play it back with earphones. Fix anything you hear.
5. Record the prompt in the card. Two to five minutes is plenty [6].
6. Share the recording **as a file** (Voice Memos > Share > Mail, or AirDrop/USB), not as a chat "audio message", into the inbox the maker gave you. Keep your original [79][6].
7. If you want anything taken out afterwards, say so before the date on the card.

**3b. Two speakers.** One phone each about 6 inches from each mouth is the ideal; if only one phone, place it between them at about equal distances and test at 6, 12 and 24 inches before the real thing (story.md Exercise 2 settles the distance) [4][78]. Clap once at the start of both phones if two are used, to align them (our practice).

**3c. The cleanup chain (all local; commands tested on ffmpeg 6.1.1 in the sandbox unless marked).**
```
# 0. keep the original; make a working copy at 48 kHz, 24-bit
ffmpeg -i in.m4a -c:a pcm_s24le -ar 48000 work.wav          # tested (ALAC to WAV)
# 1. hum (use 50 if mains is 50 Hz), then rumble and gentle denoise
ffmpeg -i work.wav -af "bandreject=f=60:width_type=q:w=30,bandreject=f=120:width_type=q:w=30,highpass=f=80,afftdn=nr=10:nf=-45:tn=1" -c:a pcm_s24le work_dn.wav   # parts tested
# 2. hear what was removed (afftdn output_mode=noise)
ffmpeg -i work.wav -af "highpass=f=80,afftdn=nr=10:nf=-45:tn=1:om=n" -c:a pcm_s24le work_removed.wav   # tested
# optional neural denoise, 48 kHz WAV only (not tested here)
deep-filter work.wav
# optional: ffmpeg arnndn, with a model file (std.rnnn); mix=-1 outputs the removed noise (not tested here)
ffmpeg -i work.wav -af "arnndn=m=std.rnnn:mix=0.8" work_rn.wav
```
In Audacity: Effect, Noise Removal and Repair, Noise Reduction (learn a profile from noise only, at least 2048 samples; start at the defaults and use the lowest values that work) [80]; Effect, EQ and Filters, Notch Filter at 60 or 50 Hz then harmonics with Q between 2 and 10 [81]. Check on headphones and on small speakers.

**3d. Consent wording for the gathering (replaces the long card, withdrawn 2026-10-18; use playbook Template D2).** The long card that stood here, with its spoken wider-use line, is withdrawn: it offered festival and cinema use that the maker has not yet decided. Use the playbook Template D2 card (`playbooks/music-sound.md`). Read the surprise-ops card [6] first, then this one sentence:

> "The film may also be shown to people outside the family at a gathering in late February. Tell me if your voice may be heard there."

The answer is one of two. **(A)** Family only: keep my voice to the private version. **(B)** The gathering: my voice may be heard there. You can change your answer or ask me to cut anything until Friday 19 February 2027 [6]. The sentence names no venue and no ticket status, so no bracketed claim needs checking.

Tier C (festival, cinema, later showings) is a written ask after the premiere; nothing about them is promised before the maker's own post-premiere release. Log the tier and the spoken yes with each file. Do not read the card until the surprise-ops truthful pretext check is done (Template D2, Routing).

**3e. Found-voice log (add to story.md's inventory):** Header identical to playbook Template D3 (its column definitions apply): `item_id,holder,device_or_format,date_made,who_speaks,addressed_to,length,quality,original_in_hand,copied_once,hum_hz,noise_notes,other_voices_heard,consent_status_each,deceased_flag,closest_family_ok,public_cut_eligible,use_decision,cut_points_tc,credit_line`. `public_cut_eligible` is `yes` (HER-PUBLIC) or `no` (HER-PRIVATE); `use_decision` is `as_recorded`, `private_only` or `none`.

### Deliverable 4. Mix spec: three targets and stem deliverables

**Targets**

| | Cinema | Venue PA | Online |
|---|---|---|---|
| File | Stems + stereo mix, 48 kHz, 24-bit WAV; a professional conforms to a DCP [99] | `venue_-18.wav` (and `-23`, `-16` alternates); video master with the same audio | `online_-16.mp4` (AAC) |
| Level rule | Calibrated mix level, no LUFS normalisation; keep peaks at or below about -3 dBFS and dynamics intact (inference) [94][95] | Integrated -18 LUFS, -1.5 dBTP, LRA below about 8-10 LU; choose the version at the rehearsal (inference from [98][93]) | Integrated -16 LUFS, -1.5 dBTP [2][97] |
| Check | Mono sum; dialogue still legible with the playback 6 dB lower (our test; [94] notes theatre faders are often lowered by up to 10 dB) | Listen at front, side and back | Re-measure after the AAC encode |

**Signal flow.** DX (found voice, relatives) first, then MX under it, then AMB and FX; print stems; then the stereo mix; then three loudness masters.

**Ducking starting values (set by ear).** Ratio 2:1 to 6:1, attack 15-20 ms, release 600-700 ms, threshold by ear, 6-12 dB of duck in busy passages and about 1-2 dB for tone; hand-ride key lines [101][102].

**Measure and normalise (tested).**
```
# measure
ffmpeg -i mix.wav -af ebur128=peak=true -f null -
# pass 1 for the venue master
ffmpeg -i mix.wav -af loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json -f null -
# pass 2 (linear): paste the four measured values and the offset; the output must say "Normalization Type: Linear"
ffmpeg -i mix.wav -af "loudnorm=I=-18:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true:print_format=summary" -ar 48000 -c:a pcm_s24le venue_-18.wav
# ducking with sidechain
ffmpeg -i mx.wav -i dx.wav -filter_complex "[1:a]asplit=2[sc][dxo];[0:a][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=700[mxd];[mxd][dxo]amix=inputs=2:normalize=0[out]" -map "[out]" -c:a pcm_s24le mix.wav
```
On PowerShell, keep each filtergraph in double quotes; the Windows null target `-f null -` works as written. FFmpeg Windows builds: gyan.dev, BtbN [87].

**Stems.** `DX_`, `MX_`, `FX_`, `AMB_`, `FULL_`, `ME_` prefixes; same length, starting at 00:00:00:00; name with `film_v01_DX_48k24.wav`; archive the untouched originals and the cleaned versions separately; hash list per format.md Step 4 [8].

**DX-gated check (speech spans only).** Measure DX and full mix over the same `voice_present=yes` spans from `spotting.csv`, per chapter or on the concatenated spans, never over the whole film. Keep 6 LU as the starting threshold (inference) and record the per-chapter offset. Playbook Step 15 and Template G are the controlling text.

**Venue-test checklist (Mon 2027-02-22).**
- [ ] Play the calibration reel (pink noise, sweep, neutral voice, one bed). The maker holds the master fader: set it from the back row on the neutral-voice reel and write the position on the run sheet.
- [ ] Play each of the three masters; pick one; record the setting.
- [ ] Check the player path (USB, laptop, HDMI), lip sync, and that the audio is not forced to mono.
- [ ] Check speech intelligibility at the back and sides, with at least one listener who does not have perfect hearing (not told the content).
- [ ] Compare each chosen master's per-chapter DX-gated offset (speech spans) with what the back-row listener reports.
- [ ] Put a backup file on a second stick and the standalone WAV on a third device.

### Deliverable 5. Music and SFX licence log (feeds theatrical-delivery's clearance log)

One row per asset; one row per use if the licence differs. Save the licence text or a screenshot with the date, and quote the sentence.

```
asset_id,type,title,creator,source_url,date_accessed,plan_or_tier,account_email,licence_name_and_version,licence_text_file,quoted_sentence,sync,master,public_performance_who,cleared_private,cleared_gathering,cleared_festival,cleared_cinema,cleared_online,attribution_text,restrictions,term_and_territory,subscription_dependent,cost_paid,receipt_file,pro_or_cue_sheet_status,ai_generated,ai_tool_and_version,ai_plan_at_download,download_date,ai_prompt_or_settings_file,principle4_check,status,used_in_cues,reviewer,last_reread_date
```
- `status`: temp, candidate, cleared, final, rejected.
- `cleared_*`: Y, y, C, ? or N, using the legend above, with the quoted sentence in `quoted_sentence`.
- Example row: `L-0004, music, "Cue title", Kevin MacLeod, https://incompetech.com/..., 2026-10-18, free, -, CC BY 4.0, licences/L-0004.png, "Licensed under Creative Commons: By Attribution 4.0", n/a (CC), n/a, venue/PRO, Y, Y, y, y, Y, "Title by Kevin MacLeod (incompetech.com)...", edits disclosed, perpetual worldwide, no, 0, -, n/a, no, -, -, -, -, ok, final, 1m3, maker, 2026-10-18`.
- Re-read every AI and subscription row in the week before 2027-02-27, and record the date.
- For `theatrical-delivery`: export the log as the music-and-SFX half of its clearance log (columns: asset, creator, source, licence, scope by venue type, evidence file, cost, attribution, restrictions, status).

### Sound schedule (T-minus, aligned with production-scale gates and the surprise-ops run sheet; format.md week 18 not used)

| Date | What |
|---|---|
| 2026-10-18 to 10-31 | Decide the premiere country and venue; build the log; test own-voice capture and the cleanup chain; low-key asks, including object sounds |
| 2026-11-14 | Track B voice-collection gate (story.md Decision 11 lean) [4]; the extended consent card is read only after the surprise-ops truthful pretext check |
| by 2026-11-15 | Sync asks (at most two songs) |
| by 2026-11-30 | Music path chosen; composer yes or no (a composer from lock is not feasible); temp library built |
| 2026-12-06 (G-SLICE-0) | Animatic with temp sound; source_in_her_life on every MOTIF and CLOCK |
| 2026-12-14 | Hard decision gate: song cleared or replaced; commission or generate per cue |
| 2026-12-20 (G-SLICE) | Chapter 1 with its sound mix; slice DX cleanup, AMB and FX run in December |
| 2026-12-28 | Start the REAPER trial (60 days; ends 2027-02-26; covers the 13–20 Feb mix), or buy the $60 licence |
| 2027-01-08 | Substitutes locked |
| 2027-01-17 (G-MID) | Rolling chapter locks begin; sound on a chapter starts at locked=1 |
| 2027-01-31 (G-DRAFT) | At least 60 percent rolling-locked |
| 2027-02-06 (G-LOCK) | Picture lock; every shot locked=1 |
| 2027-02-13 (G-MIX) | Mix v1 and grade v1 for all locked chapters |
| 2027-02-19 | Relatives' removal deadline [6]; apply removals before the masters |
| 2027-02-20 (G-MASTER) | Three masters (venue -18 with -23 and -16 alternates; online -16); DX-gated check |
| 2027-02-21 to 02-25 | Hashes, copies, cue sheet; log freeze by 02-25 |
| 2027-02-22 (Mon) | Full run on the real playback chain; maker sets the fader from the back row; position on the run sheet |
| 2027-02-24 (Wed) | Room brief (surprise-ops) |
| 2027-02-25 (Thu) | Cold start 1 |
| 2027-02-26 (Fri) | Cold start 2; day-before check |
| 2027-02-27 | Premiere |

---

## Tools, services and costs (as of 2026-10-18)

| Tool or service | Version and date | Cost | Rights or terms point | Source |
|---|---|---|---|---|
| Audacity | 4.0.1 on the download page (release date not shown); Windows x86_64 and ARM64 | Free; source offered | Licence not stated on the page; check the app's privacy settings; pin the version you test | [104] |
| FFmpeg | 9.0.2 released 2026-09-18 (8.1.3 on 2026-09-21); Windows builds from gyan.dev, BtbN | Free | Sandbox tests ran on 6.1.1; re-run on the Windows build | [87][108] |
| REAPER | 7.82, 2026-10-04 | 60-day full-function evaluation; $60 discounted (individuals using REAPER only for personal use, or commercial gross yearly revenue up to $20,000); $225 commercial | A trial started 2026-12-28 ends 2027-02-26 and covers the mix; buy the $60 licence to remove the timer | [103] |
| DaVinci Resolve (Fairlight) | Resolve 21 Free; Studio $295 | Free / $295 | Studio-only: immersive 3D audio, foley sampler, extra FX, neural voice isolation; the rest not stated | [106][2] |
| Ardour | 9.8 | Windows price not shown | GPL v2 | [107] |
| SoundCraft | pre-alpha README (tag not shown); MIT or Apache-2.0 | Free | No sidechain; about 25 open correctness bugs; delivery off the critical path | [105][5] |
| RNNoise / DeepFilterNet / arnndn / Resemble Enhance | DeepFilterNet v0.5.6; arnndn-models archived 2024-06-06; Resemble MIT | Free | Local, no upload; DeepFilterNet MIT or Apache; Resemble's enhancer is generative (do not use on found voice) | [82][83][84][85] |
| Whisper / whisper.cpp | local | Free | Local transcription per story.md Decision 9 | [4] |
| Suno Pro / Premier | ToS effective 2026-09-03 | $10 / $30 a month ($8 / $24 yearly), 20 / 60 downloads | Commercial via downloads while subscribed | [11][13] |
| Stable Audio 3.0 | 2026-05-20 | Free (<$1M revenue) | Own outputs; local run | [21][23] |
| ElevenLabs Eleven Music | terms 2026-10-09 | Plan prices not read | Film excluded unless Enterprise | [19] |
| Composer | 2025-12-02 price bands | $100-$500 per minute indie | Licence terms per Q2 | [58] |
| Song licences | 2026-10-02 vendor guide | About $500-$1,500 per side festival-only | Sync + master; step-ups | [36] |
| Epidemic Sound | 2026-10-18 pages | Prices not read | Enterprise for festival or theatrical | [32][33] |

---

## Risks, pitfalls and ethics (with mitigations)

1. **"Royalty-free" mistaken for "cleared to screen".** Mitigation: Q4 table; quote the sentence and date it; ask the library's licensing team in writing for the gathering, festival and cinema cases [32][35].
2. **A venue PRO licence mistaken for sync.** It is not [49]. Ask the venue which licences it holds, and who is responsible for music in a guest's film [51][53].
3. **AI terms and lawsuits move.** Re-read Suno and Stable Audio terms in the week before the premiere; keep downloads, receipts and metadata; keep a swap-ready alternative (PD, CC0 or silence) for every AI cue; never build the emotional peak on an AI cue [11][15][16].
4. **AI cue not registrable and not protected.** Say so in the cue sheet; do not claim a composer or writer share for it [28][29].
5. **Cloud enhancers.** Local only; never upload family audio to Suno, Auphonic, Descript, Adobe or any "voice" tool [88][89][90][11].
6. **Anything that fakes a voice.** Out: narration "in mum's voice", AI re-singing of her song, text-to-speech of a relative's letter in that relative's voice, a voice-cloned relative. Principle 4 and the tools' own terms agree [1][11][19][26].
7. **Over-processing or re-cutting her found voice.** Rules in Q8; A/B against the original; no bandwidth extension.
8. **Consent creep from private to public.** Extend the card; tiers A, B, C; log the spoken yes; honour removals until 2027-02-19 [6].
9. **Venue PA surprises.** Rehearse on Mon 2027-02-22 with a calibration reel, then the film on the real chain; carry the three masters, a standalone WAV, a backup stick; lip-sync check.
10. **Wrong loudness.** Do not mix a cinema master to -14 LUFS, and do not use single-pass dynamic loudnorm for the master [86][94].
11. **Temp love and temp leaks.** Temp stays on the maker's PC; mute tests; two temps; brief the composer on function.
12. **Secrecy leakage through a composer, mixer, lawyer or venue engineer.** Name-free briefs, confidentiality clause past 2027-02-27, calibration reel, or choose the no-outsider path.
13. **Sync price shock or silence.** At most two songs; send asks by 2026-11-15; hard gate 2026-12-14; substitute ladder.
14. **Hard-chapter audio drama.** Default to silence and room tone; no medical or siren sound; the maker decides, the Fable advisor flags (charter Principle 5) [1].
15. **Minecraft's own audio.** The guidelines count game sounds and audio as brand "assets"; sharing counts as commercial use under their rules and permissions may be revoked; do not use it [10].
16. **Jurisdiction mistakes.** Midler is a US advertising case [55]; PD dates differ by country [44][45][47][48]; PRO and venue rules differ [51][52][53][54]. Decide the premiere country first.
17. **Festival or cinema later.** If the film goes to a festival, CC-based music may be rejected [35]. Keep the log festival-ready from day one.
18. **Loudness myths.** The "-23 or -14 for everything" rule does not apply to a cinema or an unknown PA [94][95].

---

## Open questions / gaps

**For the maker to decide**
1. Premiere country and venue (affects PD dates, PRO and venue licences, cinema practice).
2. Whether to bring anyone in for music or mix (composer, pro mixer, lawyer). Default per the maker: no one.
3. Which one or two songs are truly "hers"; whether substitutes would be acceptable.
4. Whether AI music is acceptable as a labelled bed (Principle 4 allows it; the maker's taste decides).
5. Whether a cinema booking is a real goal (then plan a professional 5.1 and a calibrated mix room).
6. Consent tiers A, B, C (what you can honestly offer relatives).
7. Small spends: REAPER $60, Suno Pro for one month ($10), a composer.

**Research gaps (UNVERIFIED or not read)**
- The web-search budget ran out mid-run; no new searches were possible after it, so fetch-only coverage followed. Pages that could not be read: Artlist licence and help centre (403), Soundstripe (404), Uppbeat (429), Zapsplat licence (403), Musopen terms (403), BBC Sound Effects (fetch blocked), Pixabay licence summary (403), IPRS (403), PRS TheMusicLicence (title only), BMI (403), ASCAP venue pages other than the FAQ and cue-sheet pages, the Udio terms (script-rendered), Netflix's sound-mix spec (script-rendered), Library of Congress National Jukebox rights page (403), Adobe Enhance Speech terms.
- Zero primary data for composer turnaround from lock; fees for students and early-career composers; sync clearance timelines; famous-song fees for a non-commercial public showing.
- Festival-specific music declaration forms and AI-use policies.
- Whether EU AI Act Article 50 was delayed by an omnibus change; its application to a private-ish screening [31].
- India's IPRS tariffs, wedding or ceremony exemptions, and personality-rights case law; UK PRS rules for a film screening; GEMA and SACEM.
- Udio's primary terms; Lyria commercial terms and indemnity; ElevenLabs Enterprise terms; Mureka, AIVA, Soundraw.
- Chat-app voice-note recompression; Voice Memos Lossless codec (assumed ALAC; confirm with `ffprobe`).
- Azimuth and dropout repair for tape; VHS Hi-Fi capture chain specifics.
- Resolve Free's Fairlight limits; Audacity 4.0.1 stability on Windows; DeepFilterNet Windows binary availability; arnndn model choice.
- Dolby or SMPTE primary text for cinema calibration (only secondary summaries read); typical DCP dialogue levels beyond a small Dutch sample [95].
- Suno litigation after 2026-09-30 and any fair-use ruling.

---

## Sources

Numbered; tag = strength (P primary, S secondary or press, V vendor, F forum or snippet-grade, SR search-result excerpt only, LOCAL project file). Dates are page dates where shown, otherwise the read date (2026-10-18).

**Project files**
[1] LOCAL `CHARTER.md` — CHARTER.md — read 2026-10-18 — principles 4, 5, 7; cloud and upload rule; open decisions.
[2] LOCAL `playbooks/toolchain.md` — playbooks/toolchain.md — Step 10, Decision 6, TODO list (sources there: [76] incompetech FAQ, [77] YouTube Audio Library, [85] BBC, [86] Mixkit, [88] Suno, [89] USCO, [90] MusicGen).
[3] LOCAL `playbooks/creator-threads.md` — Part E (ask for a family recording first); music source decision.
[4] LOCAL `playbooks/story.md` — Step 2 (phone recording), Step 3 (local transcription), Decisions 8-11, found-voice paragraph, Exercise 2.
[5] LOCAL `playbooks/craft-motion.md` — Decision 8 and the SoundCraft findings (issues #707, #710).
[6] LOCAL `playbooks/surprise-ops.md` — consent card, voice letter, Decisions 9 and 10, removal deadline Friday 2027-02-19, Bourdain case [63 there], ICO note [87 there], Apple Voice Memos share note [17 there].
[7] LOCAL `research/film-story.md` — Q6 cue lengths for Coco, Up, Robot Dreams; Tarnation cost.
[8] LOCAL `playbooks/format.md` — Step 4 hash list. Its Step 14 rehearsal dates (2027-02-14 to 02-20) are retired for this track as of 2026-10-18; the venue test is the Mon 2027-02-22 run.
[9] LOCAL `research/sources/minecraft-usage-guidelines-2026-10-18.txt` — earlier excerpt of the Minecraft guidelines.
[10] Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — read live 2026-10-18 — P — "assets" include "sounds and other audio from any of our games"; sharing counts as commercial use; permissions revocable.

**AI music and AI-related rules**
[11] Suno Terms of Service — https://suno.com/terms — revised 2026-08-10, effective 2026-09-03 — P — Output assignment, no copyright warranty, downloads, watermarks, voice-model limits, training licence.
[12] Suno Help, commercial use — https://help.suno.com/en/articles/2410177 — undated "Edited" — P — Pro/Premier commercial rights; free non-commercial; no retroactive licence.
[13] Undetectr, "Suno vs Udio 2026" — https://undetectr.com/blog/suno-vs-udio-2026-which-is-better — 2026-10-04 — V (sells file-processing; no listening tests) — V6 launch 2026-09-09, prices, downloads, stems, artefacts.
[14] Dubspot, "AI Music Licensing Explained (2026)" — https://blog.dubspot.com/ai-music-licensing-explained-2026 — 2026-06-12 — S — rights summary; conflicts with others on Udio.
[15] Dynamoi, AI music lawsuits timeline — https://dynamoi.com/learn/ai-music-distribution/ai-music-copyright-cases-timeline — last updated 2026-05-11 — S/V — settlements and status (internally inconsistent on Warner v. Udio).
[16] Music Business Worldwide, Judge Saylor order on stream-ripping — https://www.musicbusinessworldwide.com/umg-and-sony-accuse-suno-of-pirating-youtube-via-stream-ripping-to-train-its-ai/ — August 2026 — S — 2026-08-18 order; fact discovery closes 2026-09-30.
[17] RouteNote, Udio downloads reopened — https://routenote.com/blog/?p=106330 — 2025-11-03 — S.
[18] Reports on Udio download shutdown and terms — https://dynamoi.com/learn/ai-music-distribution/is-udio-music-still-downloadable ; https://newindustryfocus.com/articles/udio-allows-downloads-for-48-hours-following-umg-deal-outcry — SR — downloads disabled 2025-10-29; terms from 2025-11-12.
[19] ElevenLabs, Music Terms — https://elevenlabs.io/music-terms — last updated 2026-10-09 — P — plan table; film, TV, radio excluded except Enterprise.
[20] Music Business Worldwide, Eleven Music launch — https://www.musicbusinessworldwide.com/eleven-music-new-ai-rival-to-suno-launches-with-merlin-kobalt-licensing-deals-in-the-bag/ — 2025-08-05 — S.
[21] Stability AI, license page — https://stability.ai/license — undated — P — Community (<$1M) and Enterprise tiers; Stable Audio 3.0 listed.
[22] The Decoder, Stable Audio 3.0 — https://the-decoder.com/stability-ai-launches-stable-audio-3-0-with-up-to-six-minute-tracks-and-open-weights/ — 2026-05-20 — S.
[23] Music Business Worldwide, Stable Audio 3.0 — https://musicbusinessworldwide.com/stability-ai-launches-new-audio-models-that-can-generate-6-minute-music-tracks — 2026-05-21 — S — licence quote; training-data claim.
[24] Google, Lyria 3 in the Gemini app — https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/ — 2026-02-18 — P.
[25] Google Cloud, Lyria 3 and 3 Pro on Vertex AI — https://cloud.google.com/blog/products/ai-machine-learning/lyria-3-and-lyria-3-pro-on-vertex-ai — 2026-04-07 — P.
[26] Google, Generative AI Prohibited Use Policy — https://policies.google.com/terms/generative-ai/use-policy — last modified 2024-12-17 — P.
[27] US Copyright Office, AI hub — https://www.copyright.gov/ai/ — Part 2 published 2025-01-29; Part 3 pre-publication 2025-05-09 — P.
[28] US Copyright Office, Part 2 Copyrightability Report — https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — January 2025 — P — conclusions on prompts and AI outputs.
[29] Music Week, ASCAP, BMI and SOCAN on AI — https://www.musicweek.com/publishing/read/ascap-bmi-and-socan-align-on-musical-compositions-using-ai-tools-alongside-human-authorship/092955 — 2025-10-28 — S.
[30] Hypebot, same announcement — https://www.hypebot.com/with-ascap-bmi-and-socan-unity-a-new-era-for-human-creators-and-ai-tools.md — 2025-10-30 — S.
[31] EU AI Act Article 50 — https://artificialintelligenceact.eu/article/50/ — page states application from 2 August 2026 — S (unofficial site).

**Libraries, rights and licensing**
[32] Epidemic Sound for filmmakers — https://www.epidemicsound.com/filmmaking/ — read 2026-10-18 — V — Pro for digital commercial work; Enterprise for theatrical or festival films.
[33] Epidemic Sound pricing and licensing FAQ — https://www.epidemicsound.com/pricing/ — read 2026-10-18 — V — cancellation, Enterprise 12-month minimum; prices not rendered.
[34] Artlist — https://help.artlist.io/hc/en-us/articles/29490991524253 ; https://filmmakermagazine.com/?p=110675 — SR (both 403 on fetch) — Pro/Social licence summary; sponsored festival claim.
[35] Musicbed, music licensing for film festivals — https://wpengine.fm.co/musicbed/resources/music-licensing-for-film-festivals/ — read 2026-10-18 (odd host; Musicbed content) — V — sync, master, public performance; festival licences; CC rejection.
[36] Fox Music, music licensing for short films — https://www.foximusic.com/blog/?p=601 — updated 2026-10-02 — V — directional costs, step-ups, covers, PD note.
[37] Dynamoi, sync licensing fee benchmarks — https://dynamoi.com/learn/statistics/sync-licensing-fee-benchmarks — published 2026-01-04, modified 2026-05-04 — S/V — directional, partly unattributed.
[38] Mixkit free stock music (licence summary) — https://mixkit.co/free-stock-music/ ; licence page https://mixkit.co/license/ — read 2026-10-18 — V.
[39] Pixabay Terms of Service — https://pixabay.com/service/terms/ — last updated 2024-11-18 per page — P.
[40] YouTube Help, Audio Library — https://support.google.com/youtube/answer/3376882 — undated — P.
[41] Free Music Archive FAQ — https://freemusicarchive.org/faq — undated — P.
[42] ccMixter — https://ccmixter.org/ — undated — P.
[43] Musopen — https://musopen.org/about/ — SR (403 on fetch) — claims about public-domain recordings.
[44] IMSLP, Copyright Made Simple — https://imslp.org/wiki/IMSLP:Copyright_Made_Simple — undated — S/P (a volunteer library's rules).
[45] Cornell Library, copyright term and the public domain chart — https://guides.library.cornell.edu/copyright/publicdomain — chart rows read 2026-10-18 — S.
[46] Duke Center for the Study of the Public Domain, Public Domain Day 2026 — https://cspd.law.duke.edu/publicdomainday/2026/ — January 2026 — S (first 100,000 characters read).
[47] GOV.UK, how long copyright lasts; Copyright, Designs and Patents Act 1988, duration — https://www.gov.uk/copyright/how-long-copyright-lasts ; https://www.legislation.gov.uk/ukpga/1988/48/part/I/chapter/I/crossheading/duration-of-copyright — SR.
[48] Indian Copyright Act 1957 (India Code) and commentary — https://www.indiacode.nic.in/bitstream/123456789/1367/1/a195714.pdf — SR (term figures from the search summary).
[49] ASCAP, licensing FAQ — https://www.ascap.com/help/ascap-licensing — read 2026-10-18 by the researcher; not re-read by the advisor on 2026-10-18 (HTTP 403) — P — ASCAP does not license sync or mechanical rights.
[50] ASCAP, Cue Sheet Corner — https://www.ascap.com/help/royalties-and-payment/cue-sheets — read 2026-10-18 by the researcher; not re-read by the advisor on 2026-10-18 (HTTP 403) — P — cue-sheet contents and quarterly deadlines.
[51] OneMusic Australia, Film Screenings — https://assets.onemusic.com.au/images/PDFs/guides/Film-Screenings.pdf — July 2026 — P.
[52] SUISA, screenings in cinemas and film festivals — https://www.suisa.ch/en/Kunden/Musik-in-Filmen/Filmvorfuehrungen/Vorfuehrung-in-Kinos-und-an-Filmfestivals.html — undated — P.
[53] US cinema operator comment to the Department of Justice on the ASCAP and BMI decrees (movie theater exemption) — https://media.justice.gov/vod/atr/ascapbmi2019/pc-642.pdf — 2019-08-09 — P as a statement of an exhibitor's position, not law.
[54] 17 U.S.C. 110 — https://www.law.cornell.edu/uscode/text/17/110 — read 2026-10-18 — P.
[55] Midler v. Ford Motor Co., 849 F.2d 460 (9th Cir. 1988) — https://en.wikipedia.org/wiki/Midler_v._Ford_Motor_Co. — S.

**Composers, spotting, temp tracks**
[56] Society of Composers and Lyricists, "Performing Rights and Wrongs" — https://thescl.com/articles/performing-rights-and-wrongs/ — undated — P.
[57] Australian Guild of Screen Composers, FAQ — https://www.agsc.org.au/faq — undated — P (Australian practice).
[58] Twine, composer prices — https://www.twine.net/blog/music-composer-prices-and-commissions/ — 2025-12-02 — V (marketplace).
[59] VI-Control, "Rates for scoring an indie short film?" — https://vi-control.net/community/threads/rates-for-scoring-an-indie-short-film.158475/ ; r/composer mirror https://reddit.birdcat.cafe/r/composer/comments/1gwbirc/looking_for_composers — F/SR.
[60] Screen Composers Guild of Canada, 2023 Member Survey — https://screencomposers.ca/wp-content/uploads/2023/08/SCGC-2023-Member-Survey-Report.pdf — 2023 — P (buyout and publishing data).
[61] Composer-pairing programmes — https://hfa.ucsb.edu/news/santa-barbara-international-film-festival-selects-student-composers-inaugural-scoring-lab ; https://theviolinchannel.com/san-francisco-conservatory-of-music-partners-with-sffilm/ ; https://www.richardmarvin.com/iu-jacobs-school-of-music-students-collaborate-with-film-independents-project-involve-for-sixth-consecutive-year/ — SR.
[62] Christopher Caliendo, "Spot the Film" — https://christophercaliendo.com/spot-the-film-5-composer-tips-every-filmmaker-should-know-about-scoringfilmmakers-spot-the-film/ — 2025-06-06 — S.
[63] Simpsons Wiki, "Spotting notes" — https://simpsonswiki.com/wiki/Spotting_notes — undated — F (a production description for one show).
[64] Wikipedia, Temp track — https://en.wikipedia.org/wiki/Temp_track — S.

**Exemplars**
[65] Far Out, "Keeping Score: Up and the sound of heartbreak" — https://faroutmagazine.co.uk/up-sound-of-heartbreak/ — undated — S.
[66] Wikipedia, Up opening sequence — https://en.wikipedia.org/wiki/Up_opening_sequence — S.
[67] M. Wozny, "Creating an emotional impact without dialogue: the case study of Pixar's Up" — https://studentjournals.shu.ac.uk/index.php/enquiry/article/download/125/125/398 — undated student journal — S.
[68] Dazed, "How Richard Linklater soundtracked Boyhood" — https://www.dazeddigital.com/music/article/22887/1/how-richard-linklater-soundtracked-boyhood — undated — S.
[69] Wikipedia, Coco (soundtrack) — https://en.wikipedia.org/wiki/Coco_(soundtrack) — S (via search result and film-story [38][39]).
[70] Robot Dreams reporting — https://www.wvxu.org/2024-06-05/a-new-animated-film-follows-a-lonely-dog-and-his-robot-friend-in-new-york-city ; https://fipresci.org/?p=30597 — SR (the "September" origin quotes come from the search summary; film-story cites Paste and TheWrap).
[71] BFI, Stories We Tell — https://bfi.org.uk/sight-and-sound/reviews/film-week-stories-we-tell — SR.
[72] Mix Online, sound for The War — https://www.mixonline.com/?p=78678 — undated — S.
[73] Motion Picture Association, Vietnam War sound designer — https://www.motionpictures.org/2018/10/the-vietnam-war-sound-designer-on-enhancing-emotional-memories-of-the-war/ — 2018 — S.
[74] Wikipedia, Room tone (Presence) — https://en.wikipedia.org/wiki/Room_tone — S.

**Sound libraries**
[75] Freesound FAQ — https://freesound.org/help/faq/ — undated — P.
[76] Sonniss GDC Game Audio Bundles — https://sonniss.com/gameaudiogdc/ — copyright notice 2014-2026 — P.
[77] BBC Sound Effects — https://sound-effects.bbcrewind.co.uk/licensing — not re-fetched (blocked); wording from toolchain.md [85 there].

**Voice capture and cleanup**
[78] University of Dayton Libraries, phone recording tips — https://libguides.udayton.edu/oral-history-recording/phone-tips — undated — P.
[79] Oral History Association, Remote Interviewing Resources — https://oralhistory.org/?p=10412 — undated — P.
[80] Audacity manual, Noise Reduction — https://manual.audacityteam.org/man/noise_reduction.html — P.
[81] Audacity manual, Notch Filter — https://manual.audacityteam.org/man/notch_filter.html — P.
[82] RNNoise README — https://raw.githubusercontent.com/xiph/rnnoise/main/README — P.
[83] DeepFilterNet — https://github.com/Rikorose/DeepFilterNet (README, LICENSE-MIT, LICENSE-APACHE) ; releases https://github.com/Rikorose/DeepFilterNet/releases (v0.5.6) — P.
[84] arnndn-models (RNNoise models for ffmpeg) — https://github.com/richardpl/arnndn-models — archived 2024-06-06 — P.
[85] Resemble Enhance README — https://raw.githubusercontent.com/resemble-ai/resemble-enhance/main/README.md ; LICENSE (MIT) — P.
[86] FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html — P — `loudnorm`, `afftdn`, `arnndn`, `sidechaincompress`.
[87] FFmpeg download page — https://ffmpeg.org/download.html — read 2026-10-18 — P — 9.0.2 (2026-09-18).
[88] Auphonic, privacy — https://auphonic.com/privacy — footer 2026 — P.
[89] Descript, privacy policy — https://www.descript.com/privacy — last updated 2025-04-14 — P.
[90] Adobe Privacy Policy (last updated 2025-10-24); Generative AI User Guidelines (last updated 2026-05-15); Enhance Speech page — https://www.adobe.com/privacy/policy.html ; https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html ; https://podcast.adobe.com/en/enhance — P (Enhance page title only).
[91] Home-video audio forums — https://www.digitalfaq.com/forum/video-restore/12328-hum-vhs-vhs-print.html ; https://forum.videohelp.com/showthread.php?p=2441349 — F/SR (403 on fetch; read as search summaries).
[92] Archival Producers Alliance, GenAI guidelines — https://www.archivalproducersalliance.com/genai-guidelines — page read; guidelines document not read — S.

**The mix**
[93] EBU R 128 (November 2023) — https://tech.ebu.ch/docs/r/r128.pdf — P.
[94] Ioan Allen, "How Loud is a Movie?" (SMPTE paper, via ISDCF Doc 11, 2016-03-15) — https://files.isdcf.com/papers/ISDCF-Doc11-MovieLoudnessMeasurement20160315.pdf — P.
[95] Production Expert, "Loudness and dynamics in cinema sound" — https://www.production-expert.com/home-page/2017/6/21/loudness-and-dynamics-in-cinema-sound — 2017-06-21 — S.
[96] Netflix Sound Mix Specifications — https://backlothelp.netflix.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-5 — SR (page unreadable; figures from the search summary).
[97] Spotify for Artists, loudness normalization — https://support.spotify.com/us/artists/article/loudness-normalization/ — undated — P.
[98] Production Expert on AES TD1008 (2021) — https://www.production-expert.com/production-expert-1/aes-update-loudness-recommendations-for-audio-only-streaming — 2021-09-23 — S.
[99] DCI audio parameters — https://www.soundandvision.com/content/bits-bijou ; https://files.isdcf.com/papers/IntroToDigitalCinema.pdf — SR (the DCI spec itself was not read).
[100] DCP-o-matic forum, "Stereo audio to 6 - 5.1 Audio" — https://dcpomatic.com/forum/viewtopic.php?p=10951 — 2023-09-06 to 09-09 — F.
[101] Sound on Sound, "Duck Tales" — https://www.soundonsound.com/techniques/duck-tales — undated — S.
[102] CapCut, audio ducking guide — https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video — SR/V (weak).
[103] REAPER, purchase page — https://www.reaper.fm/purchase.php — version 7.82 dated 2026-10-04 — P. Re-read by the scribe on 2026-10-18: the $60 discounted licence covers "an individual, and REAPER is only for your personal use" and commercial users with yearly gross revenue up to USD $20,000; the evaluation is "60 days … with full functionality".
[104] Audacity, download — https://www.audacityteam.org/download/ — read 2026-10-18 — P.
[105] SoundCraft README and docs/gaps.md — https://github.com/storytold/soundcraft ; https://raw.githubusercontent.com/storytold/soundcraft/main/docs/gaps.md — read 2026-10-18 — P.
[106] Blackmagic Design, Fairlight and Resolve Studio pages — https://www.blackmagicdesign.com/products/davinciresolve/fairlight ; https://www.blackmagicdesign.com/products/davinciresolve/studio — read 2026-10-18 — V.
[107] Ardour — https://ardour.org/ — read 2026-10-18 — P.
[108] Own measurement — sandbox runs, 2026-10-18 (not a web source): ffmpeg 6.1.1 on synthetic pink-noise "dialogue" and sine "music": `loudnorm` two-pass (linear confirmed on the speech-like test; the first test with a flat-level signal reported "Dynamic"), `sidechaincompress` plus `amix`, `afftdn` with `om=n`, `bandreject` hum cut (mean level -34.1 dB to -55.2 dB on a 60/120 Hz test tone), ALAC to 24-bit 48 kHz WAV. No family audio. Windows builds and DeepFilterNet/arnndn were not tested.
[109] Music Business Worldwide, Stable Audio 2.5 launch — https://www.musicbusinessworldwide.com/stability-ai-launches-ai-model-for-brands-to-create-custom-sounds — 2025-09-11 — S — Getty and artist suits against Stability.

---

## Follow-up research (round 1)

Written 2026-10-18 (Sunday), 19 weeks before the premiere on Saturday 2027-02-27. Sonnet researcher, targeted follow-up on nine questions. Tags as above (P primary, S secondary or press, V vendor, F forum, SR search excerpt only, LOCAL project file). New sources continue the numbering at [110]. Nothing here is legal advice. The premiere country is still undecided, so every rights statement is conditional.

**Research limits this round (read first).** (1) The web-search tool refused the four queries I tried because the shared 200-search budget was used up, so I ran no searches; everything below comes from direct page fetches, from files downloaded from the vendor's own server, and from code and PDFs I opened. I did not try to get around the limit. (2) These hosts blocked reading today: ASCAP (403, www and bare host), BMI (403), IPRS (403), Musopen (403 on every path I tried), APRA AMCOS (403), India Code (403), the California legislature (403), gesetze-im-internet.de (503); SACEM is blocked by the fetch tool itself; PRS and the Apple Messages page returned only a title or table of contents (script-rendered). I did not use archive, reader or proxy services to get around any of these. (3) Where a fact comes only from a Wikipedia article, an unofficial statute mirror or a trade press piece, the source line says so.

### Answers at a glance

| # | Question | Result |
|---|---|---|
| F1 | ASCAP 2027 cue-sheet deadlines and usage categories | Deadline table **confirmed from the text the first-round researcher captured on 2026-10-18 06:44 UTC** (the live page is 403 today, so this is not an independent re-read): March/April 2027 distributions need the cue sheet by **2027-01-01**; June/July by 2027-04-02. Full category code list and BMI's equivalent: **UNVERIFIED**. |
| F2 | UMG and Sony v. Suno after 2026-09-30 | **No summary-judgment ruling and no settlement found** as of reading on 2026-10-18. New since the notes: a second UMG/Sony suit filed 2026-09-18. Latest dated item I read: 2026-10-02. |
| F3 | Udio's primary terms | Udio's own pages confirm **downloads disabled** (2025-10-29, restated 2026-02-17). The terms page itself is script-rendered, so commercial-use wording is **UNVERIFIED**. Moot while there is no file to download. |
| F4 | Musopen Terms of Use | **Not read.** Every Musopen path returned 403. Date and wording UNVERIFIED. |
| F5 | Collecting society and venue licence for music inside a guest's film | Partial. **GEMA** (Germany) has a tariff for single film screenings (version valid from 2026-01-01). **UK**: only a community-cinema guide, no primary PRS text. **PRS primary, SACEM, IPRS: UNVERIFIED.** |
| F6 | Playing a living person's private voice recording to a public audience | Sourced the **household exemption** (narrow; a public screening is outside it) and the **voice-as-personal-data** point. Personality-rights law is not uniform; a ready consult sheet is below. |
| F7 | Rolling chapter lock for sound; re-conform cost | **No source found** that describes how documentary or animation shorts stage sound per reel, or any measured re-conform cost. A staging plan and a cost formula follow, both labelled inference. |
| F8 | Voice Memos Lossless codec; chat apps | **Could not confirm on a real iPhone file** (none available). Signal Android's code does not transcode audio files. WhatsApp and iMessage: UNVERIFIED. A 10-minute hash test settles it. |
| F9 | Resolve Free: ducker, de-hummer, loudness meters | **Yes, per the Resolve 21 manual**: all three are documented without a Studio tag. Studio tags sit on Voice Isolation, Dialogue Separator, Music Remixer, AI Audio Assistant, Atmos-type buses and B-chain. Confirm on the installed Free build. |

---

### F1. ASCAP cue-sheet deadlines (2027) and usage categories

**What I could and could not read.** The live ASCAP page and its payment-schedule page returned 403 today [110]. BMI returned 403 [111]. The text of the ASCAP "Cue Sheet Corner" page, however, is preserved in the first-round researcher's session log, captured at 2026-10-18 06:44 UTC [110]. Treat that as the same page, read earlier the same day, not as a fresh read.

**Deadlines as captured.** "Deadlines for submission of cue sheets" [110]:

| Distribution dates | Submission deadline |
|---|---|
| September 2026 / October 2026 | July 3, 2026 |
| December 2026 / January 2027 | October 2, 2026 |
| **March 2027 / April 2027** | **January 1, 2027** |
| June 2027 / July 2027 | April 2, 2027 |
| September 2027 / October 2027 | July 2, 2027 |
| December 2027 / January 2028 | October 1, 2027 |

The notes' figure (2027-01-01 for March/April, 2027-04-02 for June/July) matches. The page says the schedule "indicates when a cue sheet must be received by ASCAP in order for ASCAP to process it for the appropriate quarterly distribution", and that "ASCAP distributes royalties for performances approximately six (6) months after the broadcast performance" [110]. 2027-01-01 is a Friday and a public holiday (our calendar check), so treat 2026-12-18 as the working date.

**Who files.** "The production company is typically responsible for submitting cue sheets." ASCAP "accepts cue sheets directly from Networks and/or Production Companies and cannot accept cue sheets directly from members unless the source of the submission can be substantiated"; cue sheets go to TVCUESHEET@ascap.com [110].

**What a cue sheet must contain** [110]: identifying information for the programme; title of the music; duration; "How the music was used (e.g. Was it a series theme? Visual instrumental? Visual vocal?)"; entitled parties (songwriters, composers, publishers) with ownership shares; and the production company's name and contact details. The page also lists "ASCAP & BMI Announce New Standardized Cue Sheet Template Powered by RapidCue" (Summer 2016) as an article; I did not read it.

**Usage categories.** The captured text gives only examples: "visual instrumental, vocal, background instrumental or vocal", plus "series theme", "visual instrumental", "visual vocal" [110]. A complete code list is **UNVERIFIED**, and BMI's equivalent page is unread [111]. Background knowledge, not verified this round: the usual industry set is visual instrumental, visual vocal, background instrumental, background vocal, theme, main title, end title and logo. For this film the practical mapping is: a relative playing on screen is visual instrumental; underscore is background instrumental; a recording heard without a performer on screen is background vocal.

**What this means for the plan (inference).** The deadlines govern royalties for broadcast-type performances reported to ASCAP, paid about six months later [110]. A single public gathering is not a surveyed broadcast, and the film's planned cues (public-domain tunes, a relative's performance, library or AI beds with no ASCAP writer) may carry no ASCAP member share at all. So the 2027-01-01 date is not a project gate. It becomes one only if (a) a cleared commercial song with an ASCAP writer is in the film and (b) the film is later broadcast or streamed. The cue sheet stays worth making as the clearance record (Deliverable 2). No change to the schedule row for 2027-02-21 to 02-25.

---

### F2. UMG and Sony v. Suno after fact discovery (read 2026-10-18)

**Finding: no summary-judgment ruling and no UMG or Sony settlement turned up.** I cannot read the court docket from here, so this is a negative result from trade press, not a docket check.

What the press shows, newest first:
- **2026-10-02** (MBW, Shulman interview): neither UMG nor Sony has licensed Suno, per the article. Suno signed BMG on August 12 and Believe on September 8; Warner settled in November 2025. On 2026-09-09 Suno launched its v6 models, developed with WMG, BMG and Believe, and retired its previously used models the same day [118]; in August Suno had said "When the new models launch, all prior models will be retired" [117].
- **2026-09-22** (MBW): UMG and Sony filed a **second suit on Friday 2026-09-18** in federal court in Boston, assigned to the same judge (F. Dennis Saylor IV). It covers **60,202 recordings** and argues Suno's v6 models derive from earlier models trained on unlicensed music: "Training a 'new' model on the outputs of an infringing model does not eliminate the infringement; it launders it." It also alleges circumvention of YouTube's anti-downloading technology. The labels asked for a jury trial; damages sought run to up to $150,000 per work. Suno: "These claims remain fundamentally flawed on both the facts and the law." In the original case (560 recordings), fact discovery closed on September 30; the parties asked on 2026-09-18 to run discovery on the new stream-ripping claim through **2026-11-20** [112][113]. The articles do not mention summary judgment, a trial date or settlement talks [112][113].
- **2026-09-08** (MBW): Suno's 2026-09-01 answer admits it obtained YouTube audio for training using yt-dlp, argues the labels lack standing on the stream-ripping claim, and asserts fair use. The article says both sides are expected to file summary-judgment motions on fair use, and gives no date [114].
- **2026-08-27** (MBW): the same judge denied most of Suno's motion to dismiss a separate indie-artist proposed class action [116].
- **Other fronts:** GEMA won first-instance in Munich against Suno on 2026-07-31 (appealable; Suno "evaluating all available options, including an appeal") [119]; Sony filed a second suit against Udio on 2026-07-20 [121].
- **Negative check on the reading date:** the MBW Suno tag page and the MBW homepage, both read on 2026-10-18, showed no headline about a summary-judgment ruling or a UMG/Sony settlement. The homepage items mostly carried no dates (one shows "Wednesday (October 14)"), so the newest item I can date is 2026-10-02 [118][120].

**What it means (inference).** Summary judgment has not been briefed on any date I can find, and a second case with its own discovery window runs to at least 2026-11-20. A fair-use ruling before 2027-02-27 is possible but not scheduled in anything I read. It would not change the plan: the notes already treat every AI cue as swappable and never as the emotional peak. **Practical updates:** (1) re-read this item in the week of 2027-02-01; (2) Suno has retired its earlier models, so if the maker generated any temp or cue with an earlier model, download the file now and keep the receipt, because it can no longer be regenerated (per [118]); (3) from 2026-09-03 a paid subscriber must spend a download on a track before releasing, selling or licensing it [117], which matches the notes' download rule.

---

### F3. Udio's primary terms as they stand (read 2026-10-18)

**What Udio's own pages say.**
- Blog, 2025-10-29: "Starting today, downloads from the platform will be unavailable." "Over the next several months, Udio will be in a transition period." The post does not mention commercial use or ownership [122].
- Help centre article "Changes associated with the Universal Music Group partnership", dated **2026-02-17**: "Note that downloading of audio, video, and stems has been disabled." It also lists credit-limit changes (Standard 1,200 to 2,400; Pro 4,800 to 6,000) and does not address commercial use or ownership [124].
- Help centre WMG article, 2025-11-19: Udio is governed by its transition terms of service, which "was put into place on 29 October"; asked whether the labels own Udio, it answers "No, they did not."; shared songs stay available at udio.com URLs [123][125].
- Plans (help article, undated): Free (10 daily credits), Standard (2,400 a month), Pro (6,000 a month); no commercial-use statement [126].
- Changelog: "Updated TOS" on 2025-01-23 (an older revision); no later terms entry [126].

**What I could not read.** The terms page (udio.com/terms-of-service) is script-rendered and returned only its title, and /terms returned the login page. So **the commercial-use and ownership clauses of the current terms remain UNVERIFIED** [126]. I found no help-centre or blog statement of commercial rights.

**Reconciling the sources.** The notes' secondary reports said downloads were disabled and the terms were revised on 2025-11-12 to personal, non-commercial use [18]. Udio's own pages support the downloads part. The "terms revised 2025-11-12" and "personal, non-commercial" claims stay secondary. The Dubspot explainer saying paid plans grant commercial use [14] is neither confirmed nor refuted by any Udio page I could read. It does not matter in practice: with downloads disabled there is no audio file to put in a film, and recording a stream would be a workaround the terms probably forbid (inference; the terms are unread). Sony is the only major without a deal with Udio and has sued it twice [121]. **Verdict unchanged: Udio cannot supply a film file.** Re-check only if Udio's "reimagined platform" ships downloads; no page I read gives a date.

---

### F4. Musopen Terms of Use

**Not read.** `musopen.org/terms/`, `/terms-of-service/`, `/terms-of-use/`, `/faq/`, `/about/` and the home page all returned 403 [127]. I cannot quote or date the current wording, and I cannot confirm or refute the guide's older "personal, non-commercial" phrasing. The only other description I could read, the Wikipedia article, calls the music "public domain" with "creative commons licensing" but takes its freemium details from a 2013 sign-up page, so it is out of date [127].

**Do this instead (maker's own browser, 5 minutes).** Open the Musopen terms page on the Windows PC. Paste into `licence-log.csv`: the exact sentence about use of recordings, the page's "last updated" date if shown, today's date and the URL. If the sentence limits use to "personal" or "non-commercial", treat Musopen as not cleared for a public screening and use a recording that does not depend on that sentence: a relative's performance of a public-domain tune, or a pre-1926 US recording with a primary rights statement [45][46].

---

### F5. Collecting society and venue practice for music inside a guest's film

The premiere country is still open, so this is a table of what each society or source says, with a question to put to the venue.

| Country | What I could read | Status |
|---|---|---|
| **Germany (GEMA)** | The tariff overview has a film-screening tab with separate tariffs for single screenings (Tarif T), regular screenings outside cinemas (T-R), cinema operators (T-F) and, elsewhere, music performed when video carriers are played back (Tarif BT) [128]. Tarif T: "Die Vergütungssätze T gelten für Musikwiedergaben bei einzelnen Tonfilmvorführungen, unabhängig von der Art des Filmes"; examples are single screenings by municipalities, churches and youth institutions; **version 46, valid from 2026-01-01**; the page does not say who pays, whether it covers music already in the film, or how the fee is calculated [128]. General rule on the overview: "Eine geplante Musiknutzung muss vorher bei uns angemeldet werden" [128]. GEMA's page for film productions says that if you plan to perform your own production publicly (it names image films, corporate media and training videos), "Dann müssen Sie zusätzlich zur Klärung des Filmherstellungsrechts auch die Aufführungsrechte von uns erwerben", and describes its production-right tariffs as "lediglich Auffangtarife" (fallback tariffs) [129]. | Partial. Payer and calculation: UNVERIFIED (tariff PDF unread). Whether a family premiere falls under Tarif T or the production page: ask GEMA or the venue. |
| **United Kingdom (PRS)** | PRS pages returned only titles [131]. A community-cinema guide (Cinema For All, "How to Start a Community Cinema", 16 May 2024) tells organisers the venue's "PRS music licence" "covers the copyright of any music used in your chosen film, plus any additional music you want to play as the audience are entering or leaving. Venues obtain this licence from PRS Music or PPL." It also says a film licence from the distributor is always needed [130]. | Secondary and not PRS's own wording; it also blurs PRS and PPL. **PRS primary: UNVERIFIED.** It supports the notes' point that a venue's PRS licence covers performance of the film's music, never sync or master [49]. |
| **France (SACEM)** | The fetch tool blocks sacem.fr [131]. | **UNVERIFIED.** |
| **India (IPRS)** | IPRS returned 403; India Code returned 403 [131]. | **UNVERIFIED.** |
| **Australia, Switzerland, USA** | Already in the notes [51][52][53][54]. | As before. |

**Question to put to the venue, in writing (works in any country):** "Which collecting-society licences do you hold (PRS, GEMA, SACEM, IPRS, ASCAP/BMI, OneMusic)? Do they name music inside a film shown by a guest? If not, who is responsible: you or the organiser? Is there a form, fee or notice date for a one-off screening?" Log the answer next to the premiere date.

**What would change the plan.** If the answer is "the organiser reports and pays", the cue sheet becomes the document you hand over, which is a reason to keep Deliverable 5 current. A film built from public-domain tunes, relative performances and library tracks cleared in writing, with no collecting-society member repertoire, gives the society nothing to claim, but the venue may still ask for a declaration (inference).

---

### F6. Jurisdiction-flagged question for the one-hour consult: a private voice recording played to a public

**The question as it should be put (one paragraph the lawyer can read cold).** "I am making a surprise tribute film for my mother's 50th-plus year, to be shown once at a mostly public gathering in [country, city] on 2027-02-27. It includes private audio recordings of living people's voices (my mother; other relatives; friends), made by family members for private purposes, years ago or recently. The speakers have not agreed to a public showing; for my mother, she cannot be asked. Which laws govern playing those recordings to the public here? Specifically: personality, privacy or publicity rights; data-protection law (is a voice personal data, is the household exemption available, which lawful basis, is there an artistic-expression exemption); any recording-consent or confidentiality-of-speech offence; and who needs to give what consent, in what form, before I play the recording?"

**What the sources support (EU/UK data protection).**
- **Household exemption.** GDPR Article 2(2)(c) excludes processing "by a natural person in the course of a purely personal or household activity" [132]. In the video-surveillance context the EDPB says it "must be narrowly construed" and, quoting the Court of Justice in *Lindqvist*, it relates "only to activities which are carried out in the course of private or family life of individuals, which is clearly not the case with the processing of personal data consisting in publication on the internet so that those data are made accessible to an indefinite number of people". Its worked example of what stays inside the exemption: a tourist who "shows the footage to friends and family but does not make it accessible for an indefinite number of people" [133]. *Rynes* (C-212/13) held that a camera covering public space is "directed outwards from the private setting of the person processing the data" and so is not purely personal or household [134]. **Reading:** a family member's private recording is inside the household exemption; a mostly public premiere, run by the maker, is not. So if the premiere is in the EU or the UK, the maker should assume the data-protection rules apply to the screening itself (inference from the sources; the lawyer should confirm).
- **A voice is personal data.** The EDPB's voice-assistant guidelines say personal data in voice recordings may carry meaning in "its content" and "its meta-information (sex or age of the speaker etc.)", and "voice data is inherently biometric personal data", with a valid Article 6 basis and an Article 9 derogation needed when such data "is processed for the purpose of uniquely identifying a natural person" [135] (said in the voice-assistant context). Playing a recording to an audience is not identification processing, so Article 9 is probably not the issue (inference); ask.
- **Artistic-expression exemption.** Article 85(2) tells member states to provide exemptions "for processing carried out for journalistic purposes or the purpose of academic artistic or literary expression" where necessary to reconcile data protection with freedom of expression [132]; national laws differ and I did not read any country's. UK: Data Protection Act 2018 Schedule 2 Part 5 paragraph 26 disapplies many GDPR provisions for artistic purposes only if the processing is aimed at publication, the controller "reasonably believes that the publication of the material would be in the public interest", and compliance would be incompatible with the artistic purpose [136]. Whether a one-off biographical tribute to a private person meets "public interest" is exactly the kind of point to ask about.
- **Transparency and the surprise.** The notice duties in Articles 13 and 14 are among the provisions an artistic exemption can disapply [136]; without one, the surprise conflicts with them. Ask the lawyer how to handle this (for example a recorded consent from the speakers other than the mother, and a plain notice at the door).

**Personality, privacy and publicity law (what I could source; all weak).**
- **USA.** Publicity rights are state law. New York Civil Rights Law s.51 applies where a person's voice is used "for advertising purposes or for the purposes of trade" without written consent, with injunction and damages [138]. California Civil Code s.3344 covers use of a "name, voice, signature, photograph, or likeness"; I could only read this through Wikipedia, because the legislature page returned 403 [139]. Both read as commercial-use laws, so a free family tribute may fall outside them; privacy torts (private facts, false light) were not researched. UNVERIFIED for the state in question.
- **Germany.** The general right of personality (Basic Law and BGB s.823(1)) is described as protecting everyone and as not limited to commercial use [139]. Separately, s.201 of the Criminal Code (*Verletzung der Vertraulichkeit des Wortes*) punishes unauthorised recording of the privately spoken word and certain uses of such a recording, with up to three years or a fine; s.201(2) covers publicly communicating a recording or overheard words if it could harm another's legitimate interests [137]. My reading of the secondary summary is that the offence turns on whether the recording was authorised, so the lawyer should ask how and why each recording was made. The official statute text was not readable (503) [137].
- **France.** Article 9 of the Civil Code (private life) and Penal Code arts 226-1 ff. are named [139]; voice is not mentioned there. UNVERIFIED.
- **India.** I found only press-level mentions of 2025 Delhi High Court actions by celebrities over AI misuse [139]; nothing on private persons. The Digital Personal Data Protection Act 2023's remaining provisions commence on **2027-05-13** per Wikipedia [140], after the premiere; primary text unread (403), and the Act's personal or domestic purpose exemption could not be checked. UNVERIFIED.
- **United Kingdom.** No sourced statement on privacy or personality rights beyond data protection. UNVERIFIED.

**Facts to bring to the consult:** who made each recording, when, with what knowledge and for what stated purpose; whether the speaker is living and where; whether the recording captures anything private or health-related; where the premiere is and who is invited; whether it is filmed or shared afterwards (it should not be; see the removal deadline 2027-02-19 [6]); what the maker plans if a speaker objects.

**A decision the maker can take before the consult (inference).** For every voice other than the mother's, get a recorded or written yes to a public showing from the speaker (or the closest family if the speaker has died), using the D2 card, answer B; tier C is a written ask after the premiere [6]. The mother's own recordings are the proxy decision under Principle 5; the maker is the only person on the project, so that decision and the lawyer's answer are the maker's alone. Ask the other speakers without naming the film's subject or occasion (the consent card already works this way [6]); if a speaker's yes cannot be had without tipping her off, that voice stays out. The law above is a floor; the charter's dignity rule is stricter.

---

### F7. Rolling chapter lock for sound: staging and the cost of an unlock

**What I could source.**
- Picture lock "is the moment in post-production when the video edit is finalized"; after it, sound editors "receive a stable cut", and "any change after picture lock creates a domino effect, requiring rework across all these areas"; sound may need to re-sync dialogue and effects, sometimes from scratch. Changes to shot order, timing or duration should be treated as an unlock (ECG Productions, updated 2026-06-28; an agency blog, so V) [141].
- Handover: after the final cut "the sound editor can begin to finalize the soundtrack and the composer can time scenes to finish writing the film score"; on lower-budget films, temporary music and effects are inserted and later replaced (Wikipedia, Film editing) [142].
- A 35 mm sound reel (1,000 feet) runs "approximately 11 minutes"; a feature averages about five 2,000-foot reels (Wikipedia, Reel) [142]. So "reel" practice means units of about 10 to 20 minutes; our whole film is 12 to 15 minutes, which makes a chapter of 2 to 4 minutes our reel-equivalent (inference).
- Mixing is staged: a dialogue premix first (levels, crossfades, noise removal), music temporary or permanent added, then a final mix; after test screenings, a re-cut means the soundtrack "must be mixed again" (Wikipedia, Re-recording mixer) [142].
- Animation: animatics are shown "in sync with rough dialogue (i.e., scratch vocals) or rough soundtrack" (Wikipedia, Animatic) [142]. That is the temp-sound stage our plan already calls for (G-SLICE-0).
- Resolve has a Compare Timeline window that "shows the two timelines stacked together, highlighting their differences" against a backup [143]. That is the closest tool I found for finding what a late picture change touched.

**What I could not source.** How documentary or animation shorts stage sound per reel before full lock, and any measured hours to re-conform a locked reel. I found no primary description (Avid, Dolby, Netflix and festival pages were not reachable by direct link and I could not search). **UNVERIFIED; the plan below is our inference, built on the project's own hours table [149].**

**Proposed per-chapter sound stages (inference; dates from production-scale Step 14 [149]).**

| Stage | Trigger | What is allowed | What stays open |
|---|---|---|---|
| S0 temp | animatic (G-SLICE-0) | scratch voice, temp music, no mix | everything |
| S1 spot | chapter passes G4 (rolling lock begins 2027-01-17) | music spotting notes, cue list, found-voice cleanup on copies | cue lengths and sync hits |
| S2 build | chapter marked `locked=1` | final cues fitted, ambience and room tone laid, dialogue premix | levels only |
| S3 mix | all chapters locked, G-LOCK 2027-02-06 | full mix, ducking, three loudness versions | nothing |
| S4 print | after venue rehearsal | stems, masters, hashes | nothing |

Note an inconsistency to fix in the schedule: the notes assume picture lock for sound on **2027-01-15**; the roadmap's rolling locks start 2027-01-17 and full lock is **2027-02-06** [149]. The sound plan should follow the roadmap: S1 and S2 per chapter from 2027-01-17, S3 from G-LOCK 2027-02-06 to mix v1 at G-MIX 2027-02-13, masters by G-MASTER 2027-02-20.

**What an unlock costs (inference using the project's figures [149]).** Sound integration is planned at **0.6 maker-hours per finished minute**; grade, mix, captions and QC at **2.7** (0.8 if bought) [149]. For an unlocked chapter of N minutes, the sound cost is about 0.6 x N hours if cues are hit to picture and every cue after the change must be re-spotted, plus a re-listen on the venue-class speaker, plus 0.1 to 0.3 hours to re-run the loudness measurement and re-export stems (our guess, no source). A one-shot change inside a chapter that leaves later timing equal (an equal-frame-count swap) costs almost nothing; a duration change moves every later cue in that chapter. A 3-minute chapter is therefore roughly 2 to 3 hours of sound rework per unlock, and the project's two-unlock allowance after lock [149] is a roughly 5-hour reserve for sound. Treat these as planning numbers to replace with the first measured chapter.

**Design rules that keep unlocks cheap (inference).**
1. Do the mix inside the same Resolve project as the picture, so a ripple edit moves audio with picture and no conform round trip exists. Mixing in REAPER needs an export-and-conform step that I have not researched (UNVERIFIED).
2. Keep each chapter's music as its own cue ending in a tail or on silence at the chapter boundary, with one to two seconds of spare audio at each end (playbook Step 13), so a change in chapter 3 cannot move chapter 4.
3. Put a room-tone bed under every chapter and keep dialogue and voice-over as separate clips, never baked into a music track.
4. Never lock a sync point to a licensed song's hit point (the notes' rule: substitute by 2027-01-08).
5. Record the lock as a file (timeline hash, durations) as production-scale already says; the sound stages above read from that file.

---

### F8. Voice Memos "Lossless" codec; do chat apps re-encode an attached .m4a?

**Voice Memos Lossless codec: not confirmed.** Apple's Voice Memos settings page says only: "Choose either Compressed (for lower-quality, smaller files) or Lossless (for high-quality, larger files)", and names no codec, container or sample rate [147]. Wikipedia says saved voice memos "can be shared as a .m4a file" [146], and that ALAC "is frequently stored within an MP4 container with the filename extension .m4a", the same extension Apple uses for lossy AAC [146]. So the assumption (Lossless = ALAC in .m4a) is plausible but **UNVERIFIED**: the sandbox had no real iPhone recording. The three .m4a files on this machine were: our own earlier ALAC test file, an ExifTool test image (AAC, 32 kHz, encoder "iTunes v4.9"), and a Whisper benchmark clip (AAC); none is a Voice Memos file [148].

**The check, for the first real file the maker or a relative sends:**
```
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels,bits_per_raw_sample,bit_rate:format=format_name:format_tags=encoder,major_brand -of default=nw=1 "file.m4a"
```
What to expect, from synthetic files made with ffmpeg 6.1.1 in the sandbox [148]: an ALAC file prints `codec_name=alac`, a `bits_per_raw_sample` value (16 here) and a content-dependent bit rate (142 kbps for the test tone); an AAC file prints `codec_name=aac`, `bits_per_raw_sample=N/A` and a bit rate near the target (64 kbps here). The command ran cleanly on both. Both report container `mov,mp4,m4a,3gp,3g2,mj2`. Record codec, sample rate and any `encoder` tag in the licence log and keep the file byte-for-byte.

**Do chat apps re-encode an attached .m4a? Partial answers.**

| App | Voice note | Attached audio file | Evidence |
|---|---|---|---|
| **Signal (Android)** | Recorded in the app as AAC (`AudioRecorder.java` sets the attachment type to AAC). The fallback encoder `AudioCodec.java` uses **AAC-LC, 32 kbps, mono, 44.1 kHz**; the preferred `MediaRecorderWrapper` settings were not read [145]. Either way lossy at capture. | `PushMediaConstraints.java` applies transcoding settings to video and compression settings to images only; audio and documents share the general attachment size limit and no transcoding method [145]. **Not re-encoded by that code path**; I did not trace the whole upload path, and Signal iOS was not read. | Source code read 2026-10-18 (P, Android only). |
| **WhatsApp** | Opus at 8 to 16 kHz sampling rates per Wikipedia [146]: narrow-band, not usable for archival or final-mix voice. | Wikipedia: uploads of all file types are allowed (limit 2 GB since 2022) [146]. Whether a .m4a sent as a Document is left byte-identical: **UNVERIFIED** (the FAQ pages are script-rendered). | S. |
| **iMessage** | Not read (the Apple Messages audio-message article returned only its table of contents). **UNVERIFIED.** | **UNVERIFIED.** | none. |

**Ten-minute hash test (settles all three, needs only the maker).** Make a known .m4a and run `Get-FileHash file.m4a -Algorithm SHA256` on Windows (or `shasum -a 256` on a Mac). Send it once as a plain attachment or document and once as a voice note, between two of the maker's own devices or accounts, to keep the secret. Re-hash what arrives. Same hash means untouched; a different hash means re-encoded. Until the test is done, keep the notes' rule: relatives send the file by email attachment, AirDrop or USB, not as a chat voice note [78][79][6].

---

### F9. DaVinci Resolve Free: can its Fairlight page host the mix?

**Answer: very likely yes for the functions asked about; confirm on the installed Free build.** I downloaded the DaVinci Resolve 21 Reference Manual (PDF, 4,444 pages, created 2026-07-09) from Blackmagic's server and searched its text [143]. The manual does not have one Free-versus-Studio table, so the finding rests on where the manual does and does not write "Studio" next to a feature.

| Need | What the manual says | Studio tag? |
|---|---|---|
| **Ducker** | "Ducker (Track Mode Only): The Ducker Track FX plugin allows you to automatically lower the level" of a target from other tracks. "The Ducker uses changes in level only to do its work; the audio is not compressed or limited." Controls: Duck Amount (default 2.7 dB), Lookahead (15 ms), Rise Time (10 ms), Hold (150 ms), Recovery Time (750 ms). Track FX list: Voice Isolation, Dialogue Leveler, Dialogue Separator, Music Remixer, Ducker [143]. | **No tag.** |
| **Sidechain compression** | "DaVinci Resolve supports the sidechaining of compatible Fairlight FX, AU, and VST plugins", for example the Channel Dynamics compressor or the Fairlight FX Limiter [143]. | No tag. |
| **De-Hummer** | Listed under Fairlight FX; "Eliminates hum noise"; controls include a 50/60 Hz selector, Amount, Slope and a checkbox "Listen to Hum only", which lets you hear what is being removed [143]. | **No tag.** |
| **Noise Reduction (audio)** | Listed under Fairlight FX with its own custom UI [143]. | No tag. (The "temporal and AI spatial noise reduction" that Blackmagic's page lists for Studio reads as video noise reduction; our reading [144].) |
| **Loudness meters** | Loudness meters show integrated loudness in LUFS; standards selectable: BS.1770-1, BS.1770-4, ATSC A/85, EBU R128, OP-59, TR-B32, AGCOM 219, Netflix, YouTube, Disney 2.0 and Disney 5.1; default target -23 LUFS, adjustable (for example -14); true-peak per BS.1770-4. An **Offline Loudness Analyzer** (right-click a clip, Analyze Audio Level) measures files and bounces [143]. | **No tag.** |
| Statement on plugin availability | "Fairlight FX are pre-installed with all DaVinci Resolve installations", providing effects "to all DaVinci Resolve users" [143]. | n/a |

**What is Studio-only (explicitly tagged).** Dialogue Separator, Music Remixer, Voice Isolation ("a DaVinci Neural Engine AI effect that is only available in DaVinci Resolve Studio"), AI Audio Assistant, Surround Buses in Fairlight (the Atmos-type formats 9.1.6 and 22.2), object-based formats (Dolby Atmos 7.1.2/7.1.4, MPEG-H, SMPTE ST.2098), Auro-3D and B-Chain support [143]. Blackmagic's product pages add that Studio gives "more Fairlight FX audio plugins", and that the Foley Sampler and immersive 3D mixing are Studio features [144]. None of these is needed for a stereo mix, and the three neural effects are ones we would not use on her found voice anyway (they alter or separate the signal; Principle 4).

**Where this leaves the plan.** The notes' Step 14 said the Free version's ducker, de-hummer and loudness meters were UNVERIFIED [106]. They are documented without a Studio tag, so the maker's free NLE can host the dialogue-first mix, ducking, and loudness measurement without REAPER. That also supports F7's rule of mixing in the same project as the picture. Keep REAPER and ffmpeg as the proven fallback: ffmpeg `loudnorm` two-pass remains the way to make the three loudness versions reproducibly from the command line [86][108].

**Do before relying on it (about 15 minutes, on the Windows PC).** Install Resolve Free, open the Fairlight page, and check: Effects Library lists Ducker, De-Hummer, Noise Reduction and De-Esser; the Mixer shows the Loudness meter and the standard menu; right-click a clip shows Analyze Audio Level. If any is missing, note the build number and fall back to REAPER. Not checked this round: Resolve 21 Free's system requirements on the maker's PC (the charter flags memory use) and whether Free outputs 5.1 buses (the manual's Studio tag covers only the Atmos-type bus list above); both UNVERIFIED.

---

### Changes to earlier notes (for the scribes)

1. Summary item 6 and Q3 (Suno row): add the second UMG/Sony suit (2026-09-18, 60,202 recordings, v6 "launders" theory), the 2026-09-09 retirement of earlier Suno models, and the dated negative check in F2.
2. Q3 (Udio row): replace "primary terms could not be read" with F3: downloads disabled per Udio's own pages (2025-10-29; restated 2026-02-17); commercial-use wording still UNVERIFIED.
3. Cue-sheet paragraph and Template C: the 2027-01-01 and 2027-04-02 deadlines are confirmed from the captured page text, but they matter only for broadcast-type performances (F1).
4. Step 14 Tools line and the gaps list: Resolve Free's ducker, de-hummer and loudness meters are documented without Studio tags (F9).
5. Schedule: the assumed picture lock for sound on 2027-01-15 conflicts with the roadmap's rolling locks from 2027-01-17 and full lock on 2027-02-06 (F7).
6. Step 12 and the found-voice law paragraph: replace "the ICO page was not conclusive" with F6 (EDPB household-exemption guidance; the consult question).

### Remaining gaps after round 1

- Docket-level status of the Suno cases after 2026-10-02 (no docket access); re-read in the week of 2027-02-01.
- BMI and ASCAP complete usage-code lists; ASCAP/BMI behaviour for a non-broadcast screening.
- Udio's current terms text (commercial use, ownership); Musopen's terms (all 403): both need the maker's browser.
- PRS primary wording on films shown by guests; SACEM; IPRS and India's Copyright Act s.52 position for events.
- GEMA Tarif T payer and fee basis (tariff PDF unread).
- A real Voice Memos Lossless file for `ffprobe`; WhatsApp and iMessage handling of an attached .m4a; Signal iOS.
- Any primary source on per-reel sound staging for documentary or animation shorts and on re-conform costs; REAPER's conform tools.
- Personality, privacy and publicity law for the actual premiere country; UK; India; national artistic-expression exemptions under GDPR Article 85; the official text of s.201 StGB.
- Resolve 21 Free: confirm on the installed build; system requirements; 5.1 availability.

---

### Sources added in round 1 (continue the numbering; tags as above)

**F1 cue sheets**
[110] ASCAP, Cue Sheet Corner — https://www.ascap.com/help/royalties-and-payment/cue-sheets — text captured 2026-10-18 06:44 UTC by the first-round researcher (session log, agent aeb4a846721a183e0, workflow wf_4e84bd67-bdb); live fetch 403 on 2026-10-18 for this URL, the bare host `ascap.com`, and `/help/royalties-and-payment/payment/payment-schedule` — P (captured copy; not re-read live).
[111] BMI (https://www.bmi.com/ and /creators/detail/cue_sheet_submission) — 403; APRA AMCOS (https://www.apraamcos.com.au/) — 403; SESAC (https://www.sesac.com/) — read, no cue-sheet content on the page, Help Center link only; SOCAN (https://www.socan.com/) — read, no cue-sheet content — not read for cue sheets.

**F2 Suno litigation**
[112] Music Business Worldwide, "Suno confirms V6 model was trained on 'creations' from users, as it blasts latest Sony and Universal lawsuit" — https://www.musicbusinessworldwide.com/suno-confirms-v6-model-was-trained-on-creations-from-users-as-it-blasts-latest-sony-and-universal-lawsuit/ — 2026-09-22 — S (complaint PDF linked there: .../files/2026/09/26-cv-14275-Dkt.-1-Complaint.pdf; not opened).
[113] MBW, second UMG/Sony suit — https://www.musicbusinessworldwide.com/universal-and-sony-sue-suno-for-a-second-time-claiming-platforms-v6-models-are-the-fruit-of-the-same-poisoned-tree/ — 2026-09-18 — S.
[114] MBW, "Suno admits it obtained YouTube audio to train its AI, but challenges UMG and Sony's standing..." — https://www.musicbusinessworldwide.com/suno-admits-it-obtained-youtube-audio-to-train-its-ai-but-challenges-umg-and-sonys-standing-to-bring-stream-ripping-claim/ — 2026-09-08 — S.
[115] MBW, Suno–Believe licensing deal — https://www.musicbusinessworldwide.com/suno-inks-global-licensing-deal-with-believe/ — 2026-09-08 — S.
[116] MBW, judge refuses to dismiss indie class action — https://www.musicbusinessworldwide.com/judge-refuses-to-dismiss-indie-artists-proposed-class-action-against-suno-clearing-ai-output-and-stream-ripping-claims-for-discovery/ — 2026-08-27 — S.
[117] MBW, "5 things to know about Suno's BMG licensing deal, download caps, watermarks, and more" — https://www.musicbusinessworldwide.com/5-things-to-know-about-sunos-bmg-licensing-deal-download-caps-watermarks-and-more/ — 2026-08-17 — S.
[118] MBW, Shulman interview — https://www.musicbusinessworldwide.com/suno-is-far-beyond-2m-subscribers-and-300m-in-revenue-says-mikey-shulman-who-argues-its-good-that-ai-music-has-no-firm-rules-of-the-road-yet/ — 2026-10-02 — S (newest dated item read).
[119] MBW, GEMA v. Suno (Munich Regional Court) — https://www.musicbusinessworldwide.com/suno-infringed-copyright-in-gema-case-german-court-rules/ — 2026-07-31 — S.
[120] MBW, Suno tag page and homepage — https://www.musicbusinessworldwide.com/tag/suno/ ; https://www.musicbusinessworldwide.com/ — read 2026-10-18 — S (negative check; most items undated).
[121] MBW, Sony's second suit against Udio — https://www.musicbusinessworldwide.com/sony-music-files-new-lawsuit-against-ai-platform-udio-asserting-over-30000-sound-recordings-a-judge-barred-it-from-adding-to-its-original-case/ — 2026-07-20 — S.

**F3 Udio**
[122] Udio blog, "A New Era of Music - Udio with Universal Music Group" — https://www.udio.com/blog/a-new-era — 2025-10-29 — P.
[123] Udio blog, "Udio with Warner Music Group" — https://www.udio.com/blog/udio-warner — 2025-11-19 — P.
[124] Udio Help, "Changes associated with the Universal Music Group ("UMG") partnership" — https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership — dated 2026-02-17 — P.
[125] Udio Help, "Udio - Warner Music Group (WMG) partnership" — https://help.udio.com/en/articles/12874375-udio-warner-music-group-wmg-partnership — 2025-11-19 — P.
[126] Udio terms page (https://www.udio.com/terms-of-service, /terms) — script-rendered, title or login page only; Udio Help credits article https://help.udio.com/en/articles/10739134-credits-and-credit-limits ; changelog https://help.udio.com/en/articles/10748731-changelog-what-s-new-with-udio ; help collections and sitemap (no article on commercial use) — read 2026-10-18 — P.

**F4 Musopen**
[127] Musopen — https://musopen.org/ (and /terms/, /terms-of-service/, /terms-of-use/, /faq/, /about/) — 403 on all; Wikipedia, Musopen — https://en.wikipedia.org/wiki/Musopen — S, relies on a 2013 sign-up page.

**F5 collecting societies**
[128] GEMA, tariff overview and tariff pages — https://www.gema.de/de/musiknutzer/tarifuebersicht ; .../tarif-t (version 46, valid from 2026-01-01) ; .../tarif-t-r (version 44, valid from 2025-07-01) ; .../tarif-bt (version 49, valid from 2026-01-01) — read 2026-10-18 — P.
[129] GEMA, "Filme, Serien, Werbespots" — https://www.gema.de/de/musiknutzer/av-produktionen — read 2026-10-18 — P.
[130] Cinema For All, "How to Start a Community Cinema" (Starter Pack, PDF created 16 May 2024) — https://www.cinemaforall.org.uk/app/uploads/2024/05/How-to-Start-a-Community-Cinema-2024.pdf — S (UK community-cinema guidance, not PRS).
[131] PRS (https://www.prsformusic.com/ and /get-a-music-licence/live-music-and-event — titles only); IPRS (https://iprs.org/, https://www.iprs.org/ — 403); SACEM (www.sacem.fr, clients.sacem.fr — blocked by the fetch tool); India Code Copyright Act PDF — 403 — not read.

**F6 law**
[132] GDPR Article 2 and Recital 18; Article 85 — https://gdpr-info.eu/art-2-gdpr/ ; https://gdpr-info.eu/recitals/no-18/ ; https://gdpr-info.eu/art-85-gdpr/ — read 2026-10-18 — S (unofficial mirror; recital text only in short quotes).
[133] EDPB, Guidelines 3/2019 on processing of personal data through video devices, v2.0 adopted 2020-01-29 (v2.1 2020-02-26), section 2.3 "Household exemption" — https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf — P — PDF downloaded and read 2026-10-18.
[134] Court of Justice: *Rynes* C-212/13 (para 33) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62013CJ0212 ; *Lindqvist* C-101/01 (para 47) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62001CJ0101 — P (short quotes via the fetch tool).
[135] EDPB, Guidelines 02/2021 on virtual voice assistants, v2.0 adopted 2021-07-07, para 31 — https://www.edpb.europa.eu/system/files/2021-07/edpb_guidelines_202102_on_vva_v2.0_adopted_en.pdf — P — PDF downloaded and read 2026-10-18.
[136] Data Protection Act 2018, Schedule 2 Part 5 (para 26, journalistic, academic, artistic and literary purposes) — https://www.legislation.gov.uk/ukpga/2018/12/schedule/2/part/5 — P — read 2026-10-18 (summary via the fetch tool).
[137] Criminal Code (Germany) s.201 — https://dejure.org/gesetze/StGB/201.html — S (paraphrase via the fetch tool; gesetze-im-internet.de returned 503).
[138] New York Civil Rights Law s.51 — https://www.nysenate.gov/legislation/laws/CVR/51 — P — read 2026-10-18.
[139] Wikipedia, Personality rights — https://en.wikipedia.org/wiki/Personality_rights — S (first 100,000 characters read; California s.3344 voice, Germany, France, India press mentions).
[140] Wikipedia, Digital Personal Data Protection Act, 2023 — https://en.wikipedia.org/wiki/Digital_Personal_Data_Protection_Act,_2023 — S (commencement dates; primary text 403).

**F7 lock and staging**
[141] ECG Productions, "What Is Picture Lock and Why It's Crucial for Smooth Post-Production" — https://www.ecgprod.com/what-is-picture-lock-why-does-it-matter — updated 2026-06-28 — V.
[142] Wikipedia: Film editing (https://en.wikipedia.org/wiki/Film_editing, first 100,000 characters), Reel (https://en.wikipedia.org/wiki/Reel), Re-recording mixer (https://en.wikipedia.org/wiki/Re-recording_mixer), Animatic (https://en.wikipedia.org/wiki/Animatic) — S.

**F9 Resolve**
[143] Blackmagic Design, DaVinci Resolve 21 Reference Manual — https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf — PDF creation date 2026-07-09, 4,444 pages, downloaded and text-searched 2026-10-18 — P (Cut-page chapter 38 and Fairlight chapters 180 to 184: Ducker, Audio Effects, Fairlight FX, Audio Meters, Immersive Audio; Studio tags quoted above).
[144] Blackmagic Design, Fairlight page, Resolve Studio page, tech specs (Resolve 21 listed; Studio $295) — https://www.blackmagicdesign.com/products/davinciresolve/fairlight ; .../studio ; .../techspecs ; .../compare (no comparison table) — read 2026-10-18 — V.

**F8 voice notes**
[145] Signal-Android source at `main`: `app/src/main/java/org/thoughtcrime/securesms/audio/AudioCodec.java`, `AudioRecorder.java`, `mms/PushMediaConstraints.java` — https://raw.githubusercontent.com/signalapp/Signal-Android/main/app/src/main/java/org/thoughtcrime/securesms/audio/AudioCodec.java (and siblings) — read 2026-10-18 — P (code; Android only; `MediaConstraints.java` and the support page not readable).
[146] Wikipedia: WhatsApp (https://en.wikipedia.org/wiki/WhatsApp, first 100,000 characters), Apple Lossless Audio Codec (https://en.wikipedia.org/wiki/Apple_Lossless_Audio_Codec), Voice Memos (https://en.wikipedia.org/wiki/Voice_Memos) — S.
[147] Apple Support, Voice Memos for Mac, "Change Voice Memos settings" — https://support.apple.com/guide/voice-memos/change-voice-memos-settings-vm0ba246ff3e/mac — P — quote above. The iPhone guide and the "Send and receive audio messages" article returned only tables of contents.
[148] Own measurement, 2026-10-18 (not a web source): ffprobe 6.1.1 on synthetic ALAC and AAC .m4a files made with ffmpeg 6.1.1, and on the three .m4a files already on the machine (none a Voice Memos recording).
[149] LOCAL `playbooks/production-scale.md` — Step 14 (rolling locks from 2027-01-17; G-DRAFT 2027-01-31; G-LOCK 2027-02-06; unlock rule, two unlocks after lock), the stage-hours table (sound integration 0.6; grade, mix, captions and QC 2.7, or 0.8 if bought) — read 2026-10-18.

---

## Follow-up research (round 2)

Written 2026-10-18 (Sunday), 19 weeks before the premiere on Saturday 2027-02-27. Sonnet researcher, targeted follow-up on eight questions. Tags as above (P primary, S secondary or press, V vendor, F forum, SR search excerpt only, LOCAL project file, OWN own measurement in the sandbox, not a web source). New sources continue the numbering at [150]. Nothing here is legal advice. The premiere country is still undecided (the playbook's decision date is 2026-10-31), so every rights statement is conditional.

**Context update from the maker (2026-10-18).** In answer to "who is in on the secret, and who could approve the hard chapters for her?" the maker wrote: for now only the maker, and the maker will be the only one on this project. That matches the charter: the maker is the sole person in on it and acts as her proxy for hard chapters, with the Fable advisor flagging sensitive material but not deciding. Four consequences for this track: (a) there is no second approver, so sign-off on the D2 consent sentence (G4) is the maker's; (b) the one-hour rights consult (F6, G7) is the maker's alone; (c) a composer, pro mixer, lawyer, venue engineer or society contact widens the circle and stays a later choice for the maker, using the name-free brief and the confidentiality clause already in the notes; (d) the January re-conform timing (G8) is done by the maker's own hands.

**Research limits this round (read first).** (1) The web-search tool refused my one query because the shared search budget is used up (same as round 1), so I ran no searches. Everything below comes from direct page fetches and from files downloaded from the publisher's own server. (2) Hosts that still do not deliver their text: ASCAP (plain HTTP 403 again, on both the fetch tool and curl); BMI and Musopen (HTTP 403 whose body is a Cloudflare "Just a moment..." browser challenge, so a normal browser should load them); IPRS (HTTP 403, Cloudflare "Attention Required!" page); SACEM (blocked by the fetch tool itself, so I did not try another route); Netflix's Knowledge Hub (a script-rendered app whose HTML holds only the title "Knowledge Hub"; I did not call its private data API); PRS (pages return navigation only); two guessed hosts, backlothelp.netflixstudios.com and partners.bbc.co.uk, were refused by the egress proxy. I did not use archive, reader or proxy services, and I did not try to pass a browser challenge. (3) The Udio and RapidCue findings below came from reading the publisher's own page data and PDF, which the fetch tool's summary could not show.

### Answers at a glance

| # | Question | Result |
|---|---|---|
| G1 | ASCAP cue-sheet dates and usage categories | **Dates: still not independently re-read.** ASCAP is 403 again; BMI is behind a browser challenge. [50] stays tagged. **Categories: now confirmed from a primary source**, the RapidCue Batch Reference Guide (April 2025, © BMI, run by BMI and ASCAP): 29 valid `CueUsage` values and 10 `CueSubUsage` values, listed below, plus the fields that map onto our licence log. |
| G2 | Musopen Terms of Use | **Not read.** Cloudflare browser challenge, so the page exists and the maker's browser should show it. Paste-ready log row and decision rule below. Maker action, 5 minutes. |
| G3 | Dialogue-to-programme loudness offset | **Broadcaster anchor found: EBU R 128 s4 and Tech 3343 (both November 2023).** "Loudness-to-Dialogue Ratio" LDR = Programme Loudness minus Dialogue Loudness, recommended **at most 5 LU** for adapted cinematic content; ORF's 44-film study found a mean below 4 LU and unadapted films above 15 LU. Our playbook's 6 LU is 1 LU looser than the only broadcaster number found. Netflix's -27 LKFS spec **not read** (script-rendered). Dolby and BBC guidance **UNVERIFIED** (no readable primary). |
| G4 | Owner and date of the D2 patch to surprise-ops | **Not applied yet** (checked: the surprise-ops playbook has not changed since 06:49 UTC, and music-sound Template D2 still says "next round"). **Owner: the orchestrator session. Date: Saturday 2026-11-07.** The maker signs off the wording. |
| G5 | Free Fairlight on the maker's PC | **Cannot be run from here** (no access to the PC). Added: the manual's memory-cap setting, a tested sampling script, and a one-page result sheet. Resolve 21 Windows minimum RAM: **UNVERIFIED**. |
| G6 | Udio's primary terms | **Read from the page** (Last Revised November 12, 2025). Downloads barred; Output usable "solely for your personal and non-commercial purposes"; Udio and its licensors own Output. Both secondary reports are confirmed on these points. **Udio is out for the film.** New: its licence over anything uploaded as Input Content is perpetual and irrevocable, so never upload family audio or photos. |
| G7 | Society practice and the F6 consult question | **GEMA's Tarif T read in full (primary):** 1.3% of net ticket revenue, minimum EUR 30.40 per screening up to 150 people, and more. PRS, SACEM, IPRS: **UNVERIFIED.** The F6 consult paragraph stands; three add-on questions below. |
| G8 | Measured re-conform cost | **Machine part measured in the sandbox: 23 to 28 seconds for a 3-minute chapter.** The human part cannot be measured before a real chapter exists. A stopwatch protocol, a dry run on the slice chapter (2026-12-21 to 12-27) and the January timing are set out below. F7's figures remain inference. |

---

### G1. ASCAP cue-sheet dates and usage categories

**Dates (unchanged).** ASCAP's cue-sheet page returned plain "403 Forbidden" on the fetch tool and on curl this round [155], in addition to the earlier attempts [110]. BMI's cue-sheet URLs returned a Cloudflare challenge page, not content [155]. So the deadline table in F1 (March/April 2027 distributions need the cue sheet by 2027-01-01; June/July by 2027-04-02) still rests on the text captured at 06:44 UTC [110]. **[50] stays tagged.** The conclusion in F1 also stands: the date is not a project gate unless a cleared commercial song with an ASCAP or BMI writer is in the film and the film is later broadcast or streamed.

**Maker action, only if such a song is in the cut (5 minutes, own browser).** Open the ASCAP page named in [50]. Paste into the licence log the two table rows "March 2027 / April 2027" and "June 2027 / July 2027", the sentence beginning "How the music was used", the date you read it, and the page's own date if shown. If no ASCAP or BMI writer is involved, skip this and leave [50] tagged.

**Usage categories (confirmed from a primary source).** RapidCue is the electronic cue-sheet service for performing rights organisations. Its Batch Reference Guide is copyrighted "2019-2025 BMI", was created 2025-04-28 (PDF metadata), and tells readers to contact "RapidCue representatives at BMI and ASCAP" [154]. Its Appendix A.5 gives the valid `CueUsage` values and A.6 the valid `CueSubUsage` values [154]:

- **CueUsage (29):** Background; Background Instrumental; Background Vocal; Bumper; Closing Theme; End Title Theme; Film Theme Close; Film Theme Close Background Instrumental; Film Theme Close Background Vocal; Film Theme Close Visual Instrumental; Film Theme Close Visual Vocal; Film Theme Open; Film Theme Open Background Instrumental; Film Theme Open Background Vocal; Film Theme Open Visual Instrumental; Film Theme Open Visual Vocal; Indistinguishable; Logo; Main Title Theme; Opening Theme; Segment Theme; Theme Instrumental Close; Theme Instrumental Open; Theme Vocal Close; Theme Vocal Open; Visual Dance; Visual Instrumental; Visual Performance Accompaniment; Visual Vocal.
- **CueSubUsage (10):** None; A Cappella; Dance; Humming; Indistinguishable; Live Performance Symphonic; Lyricless Vocals; Noodling; Spoken; Whistling.

This is a superset of the examples on ASCAP's page ("visual instrumental, vocal, background instrumental or vocal", "series theme") [110], so the two sources agree. It is RapidCue's data-entry list, not ASCAP's own page, and I did not check it against BMI's cue-sheet page.

**Mapping for this film (inference; confirm with the society if a sheet is ever filed).**

| Cue in the film | `CueUsage` / `CueSubUsage` |
|---|---|
| A relative plays or sings on screen | Visual Instrumental or Visual Vocal |
| The maker's or her hummed tune, heard with no performer visible | Background Vocal, sub-usage Humming (Visual Vocal if the hummer is on screen) |
| Library or AI underscore | Background Instrumental |
| Song over the opening or end titles | Opening Theme or Main Title Theme; End Title Theme |
| A sting on a production logo, if any | Logo |

**Fields worth adding to Deliverable 5 and the cue-sheet template [154].** `PublicDomainIndicator` (Yes or No, required on every cue) and `PublicDomainTerritory` (World or US, required when Yes); `SyncUseIndicator` and `SyncUseLicensor`; `MasterUseIndicator` and `MasterUseLicensor`; `Performer`; `LibraryName`, `CDNumber`, `CutNumber` for library tracks; `Duration` as HHMMSS; interested-party `Role` from a fixed list (Composer, Author, Publisher and others), `Shares` as five digits (100% = 10000, 50% = 05000). The guide also describes a "no music" cue sheet [154]. Alphabetic entries are uppercase in the XML [154].

---

### G2. Musopen Terms of Use

**Not read.** `musopen.org/` and `musopen.org/terms/` returned HTTP 403 on curl and on the fetch tool; the body is Cloudflare's "Just a moment..." challenge [155]. That is a check meant for browsers, so the maker's own browser should pass it. I did not try to get around it.

**Maker action (5 minutes, own browser, by 2026-10-31 with the log build).** Open the Musopen terms page. Paste one row into `licence-log.csv` and, if it fits, the page's own date:

```
asset_id,type,title,creator,source_url,date_accessed,plan_or_tier,licence_name_and_version,quoted_sentence,page_last_updated,cleared_gathering,status
L-xxxx,policy,"Musopen terms of use","Musopen","https://musopen.org/terms/",2026-10-xx,free,"Terms of Use (as shown)","<exact sentence about how recordings may be used>","<date on the page, or 'none shown'>",<Y|y|C|?|N>,<candidate|rejected>
```

Decision rule, unchanged from F4: if the sentence limits use to "personal" or "non-commercial", Musopen is **not** cleared for a public screening, and the music uses a source that does not depend on it (a relative's performance of a public-domain tune, or a pre-1926 US recording with a primary rights statement [45][46]).

---

### G3. A dialogue-to-programme loudness offset to anchor the playbook's 6 LU check

**The check being anchored.** Playbook Step 15, "DX-gated check", and Template G: measure the dialogue stem (DX) alone and the full mix, both integrated; "if the integrated DX sits more than 6 LU under the full mix, the music is too loud for a room with many listeners aged 50 and over". In EBU terms that is the Loudness-to-Dialogue Ratio with the dialogue stem as the dialogue measurement.

**What the EBU documents say (primary, November 2023).**
- **Definitions.** "Programme Loudness (PL): The integrated loudness over the duration of a programme"; "Dialogue Loudness (DL): The average loudness of the speech component of a programme"; "Loudness-to-Dialogue Ratio (LDR): The difference between Programme and Dialogue Loudness (LDR = PL - DL)". A footnote adds: "Dialogue Loudness is also called 'Speech Loudness' or 'Speech-gated Loudness'" [151]. So "dialogue-gated" and "dialogue loudness" are the same measurement family as our DX-stem check.
- **Limit.** Recommendation j): "the Loudness-to-Dialogue Ratio of Cinematic Content should not exceed 5 LU." Recommendation k): "if the Loudness-to-Dialogue Ratio of Cinematic Content is within 5 LU, no dynamic adaptation needs to be performed", and "increasing Dialogue Loudness to match Programme Loudness (LDR = 0) should be avoided" [151].
- **Evidence behind 5 LU.** Tech 3343 §9.4 reports an analysis of 44 feature films from ORF's database, dubbed into German and already dynamically adapted by two experienced sound engineers: "The mean Loudness-to-Dialogue Ratio was for both methods below 4 LU"; for the stricter "narrow-range" dialogue (no whisper, shout or song, no competing music or effects) LDR was "higher, but still ≤ 5 LU"; the two measurement methods (a speech-edited centre channel versus Dolby's Dialogue Intelligence algorithm) differed by a mean of 0.4 LU [150]. Unadapted film mixes: LDR "can be excessive, sometimes more than 15 LU!" [150]; the s4 worked example is a film at PL -17 and DL -29 LUFS (LDR 12) [151].
- **What 5 LU does to levels.** With the -23.0 LUFS target and LDR at most 5 LU, dialogue "can effectively sit on one level in the range of −28.0 ≤ DL ≤ −23.0 LUFS"; if the dialogue is normalised to -23, the programme can "maximally reach -18.0 LUFS" [150][151]. That is the same number as the notes' venue master (-18 LUFS integrated), so a venue master at -18 with LDR at most 5 implies dialogue at about -23 LUFS or louder. This is arithmetic on the EBU figures, not an EBU statement about halls.
- **How to measure it cheaply.** Tech 3343 §9.4.1 spot-check: choose three on-screen dialogue sequences from the beginning, middle and end ("omit off-screen narration"); each about 30 seconds; no music or competing effects; measure each with ITU-R BS.1770; the average is the narrow-range DL. With a separate dialogue stem, measure the stem; for a stereo programme with no stem, "the complete mix is the basis" [150][151].

**Limits of this anchor (important).** R 128 s4 is guidance on adapting dynamic films for **broadcast and streaming**; it says it "is explicitly not intended as production advice for feature films", and "programmes for playback in cinemas are explicitly not considered" [151]. So 5 LU is an anchor from the only broadcaster document I could read, not a rule for a hall PA.

**Our 6 LU versus 5 LU (inference).** The playbook's 6 LU is one LU looser than the EBU figure, and the ORF mean (below 4 LU) shows 5 LU is routinely met by a careful dynamic adaptation. Recommended wording for the scribes: **target LDR of 5 LU or less (EBU R 128 s4); more than 5 LU means look at the music; more than 6 LU is a fail that must be fixed before a master is signed off**. That keeps 6 as the hard line the playbook already wrote and adds the EBU number as the aim. The room still has the last word: the 2027-02-22 run from the back row decides.

**Sandbox check of the measurement itself (OWN [160]).** I built a synthetic 3-minute chapter (a public speech clip repeated with gaps as "dialogue", a steady three-note pad as "music"), normalised the dialogue to -23.0 LUFS and measured with `ffmpeg -af ebur128`. LDR = integrated(mix) minus integrated(DX):

| Music gain | Mix integrated (LUFS) | LDR (LU) |
|---|---|---|
| -20 dB | -24.2 | -1.2 |
| -10 dB | -22.6 | 0.4 |
| -6 dB | -20.1 | 2.9 |
| -4 dB | -18.5 | 4.5 |
| -2 dB | -16.9 | 6.1 |
| 0 dB | -15.1 | 7.9 |

Two things to know. (1) Near the limit, about 0.8 LU of LDR moves per dB of music, so moving the limit from 6 to 5 LU lowers the music by roughly 1 to 1.5 dB in this synthetic case (not general). (2) With very quiet music the number can read **negative**: the mix measured lower than the dialogue alone. The likely cause (inference, not tested further) is that a quiet bed fills the gaps, lowers the relative gate's threshold and lets quieter speech blocks into the gated average. Read LDR only when the music is audible; a reading near zero or below does not mean "perfect". Recipe, per file: `ffmpeg -hide_banner -nostats -i FILE -af ebur128 -f null - 2>&1 | awk '/Summary/{s=1} s&&/I:/{print $2; exit}'`.

**Netflix's dialogue-gated spec: not read directly.** The old partner-help address 301-redirects to `studiopartner.netflix.net/studio/branded-sound-mix-spec-and-best-practices`, a script-rendered app whose HTML holds only the title "Knowledge Hub" [153]. I did not call its private data interface. The "-27 LKFS dialogue-gated, +/-2 LU, -2 dBTP" figure therefore stays a search-snippet item [96], tagged UNVERIFIED. **Maker action (3 minutes, own browser):** open that address, find the loudness section, and paste the sentences giving the dialogue-gated target, its tolerance, the true-peak limit and the loudness-range limit into the log with the date and any version label on the page. It is a streaming spec and is not needed for the hall; its value is as a second anchor for "dialogue-gated".

**Dolby and BBC: UNVERIFIED.** No Dolby or BBC page with a dialogue-versus-programme figure was readable (the Dolby professional TV page I read links no loudness documents; the BBC R&D pages are script-rendered; the BBC delivery host was refused by the egress proxy). Dolby is present indirectly: the ORF study used Dolby's Dialogue Intelligence, and a Dolby staff member is among the contributors named in R 128 s4 [150][151]. Tech 3343 also notes that in Dolby's metadata "dialnorm genuinely describes the loudness of an entire programme" unless anchor-based normalisation is used, in which case it describes the dialogue [150]. Tech 3343 gives -27 as the factory default of dialnorm in Dolby Digital and -31 as its lowest value [150], and Tech 3344 section 6.7 notes home-theatre equipment that applies a fixed offset to a -27 LUFS reference [152]; I claim no link between those and Netflix's figure. No practitioner (non-broadcaster) source for a hall or PA setting turned up; the nearest context is still the cinema measurements already in the notes [94][95].

---

### G4. Who patches the surprise-ops consent card with the D2 sentence, and by when

**Status (checked 2026-10-18).** Not applied. `playbooks/surprise-ops.md` was last modified at 06:49 UTC and contains no D2 text; its consent card still promises "a film that family will watch together, and a longer private version given to [NAME]" [161]. `playbooks/music-sound.md` Template D2 "Routing" still says the wording goes to surprise-ops "at that track's next round", although that track has finished round 3 [161]. The round-2 advisor review had already asked for a dated action instead [161].

**Owner and date.** The advisor review's note to the orchestrator reads: "Patch the surprise-ops consent card directly, by 2026-11-07, so the Track B gate on 2026-11-14 is not blocked" [161]. So: **the orchestrator session applies the patch to `playbooks/surprise-ops.md` (Consent card section, and the one-line text/voice version) by Saturday 2026-11-07, one week before the voice-collection gate on Saturday 2026-11-14. The maker approves the wording**, since the maker reads the card aloud and is the only human on the project. Until the patch lands, D2 is not read and no relative is recorded for the public cut [161]. I did not edit `surprise-ops.md`, which is outside this task.

**What the patch should contain (suggestions).** (1) The D2 sentence after the existing card: "The film may also be shown to people outside the family at a gathering in late February. Tell me if your voice may be heard there." (2) The two answers, A (family only) and B (the gathering), with changes allowed until Friday 2027-02-19 [6]. (3) Reconcile the card's "two places" sentence so the family-only version and the gathering version do not contradict each other. (4) Record the open point already in the playbook: a relative who hears D2 learns that a late-February gathering exists, and the secrecy check of that fact has not been done. The maker decides per relative; an answer of A, or no question asked, keeps that voice out of the public cut.

---

### G5. Free Fairlight on the maker's Windows PC (the F9 fifteen-minute check)

**Result: not done, because it needs the PC.** The charter says GUI control of the maker's machine is not connected, so I cannot read the installed build. Ducker, De-Hummer, Noise Reduction and the Loudness meter remain "documented without a Studio tag" per F9 [143], and **present on the installed build: UNVERIFIED.**

**What I could add.**
- **A way to stay inside the memory constraint.** The Resolve 21 manual (Chapter 4, System and User Preferences, Memory and GPU) describes a preference, "Limit Resolve Memory Usage to", that caps the system memory Resolve uses and so keeps memory free for other applications: "The maximum and default setting for this preference is 75 percent of your system's RAM." It also offers a separate limit for the Fusion cache [143]. So Resolve's use can be capped.
- **Windows minimum RAM: UNVERIFIED.** The Blackmagic tech-specs page lists only hardware products and no RAM or GPU minimum [159]. The manual points to a separate Configuration Guide on Blackmagic's support page [143]; the support page I read carried no link to it [159].
- **A tested memory log.** `memlog.ps1` (below) samples Resolve's memory every few seconds into a CSV. I ran it on PowerShell 7 on Linux against an ffmpeg process (6 samples, peak reported correctly) [160]; it has **not** been run on Windows, where the process name should be `Resolve` (check Task Manager, Details tab).

```
# memlog.ps1  -  .\memlog.ps1 -Minutes 5            (Resolve running, chapter playing on the Fairlight page)
param([double]$Minutes = 5, [string]$Name = 'Resolve', [int]$Every = 5)
$end  = (Get-Date).AddMinutes($Minutes)
$rows = @()
while ((Get-Date) -lt $end) {
  $p = Get-Process -Name $Name -ErrorAction SilentlyContinue
  if ($p) {
    $rows += [pscustomobject]@{
      time      = (Get-Date).ToString('HH:mm:ss')
      workingMB = [math]::Round(($p | Measure-Object WorkingSet64 -Sum).Sum / 1MB)
      privateMB = [math]::Round(($p | Measure-Object PrivateMemorySize64 -Sum).Sum / 1MB)
    }
  }
  Start-Sleep -Seconds $Every
}
$rows | Export-Csv "$Name-mem.csv" -NoTypeInformation
$peak = $rows | Sort-Object workingMB -Descending | Select-Object -First 1
"peak working set: $($peak.workingMB) MB at $($peak.time); samples: $($rows.Count)"
```

**Result sheet for the maker (15 minutes).** Fill in and paste into the log.

| Item | Result |
|---|---|
| Resolve build (Help > About) and Free or Studio | |
| Installed RAM (Task Manager > Performance > Memory) | |
| "Limit Resolve Memory Usage to" (Preferences > System > Memory and GPU) | default 75%, or the value you set |
| Fairlight page, Effects Library lists Ducker | Y / N |
| ... De-Hummer | Y / N |
| ... Noise Reduction | Y / N |
| ... De-Esser | Y / N |
| Mixer shows the Loudness meter and its standard menu (EBU R128, Netflix, and so on) | Y / N |
| Right-click a clip > Analyze Audio Level present | Y / N |
| Peak working set during 5 minutes of playback (from `memlog.ps1`) | MB |
| Audio dropouts or stutter during playback | Y / N |
| Verdict | accept / cap and retest / fall back to REAPER [103] |

**Acceptance rule (my proposal, inference; the maker may change it):** accept if the peak working set stays at or below half of the installed RAM, playback is clean, and the PC stays usable with a browser open. If not, set the cap to 50% and retest once; if still over, use REAPER (60-day trial per the schedule, or the $60 licence [103]) for the mix and keep Resolve for picture.

---

### G6. Udio's primary terms, read from the page

**How it was read.** `udio.com/terms-of-service` is a Next.js page: the fetch tool's extractor shows only its title, but the full text is in the page's server-rendered data. I downloaded the HTML (HTTP 200) and extracted the text from it. The header reads "TERMS OF SERVICE" and "**Last Revised on November 12, 2025**" [156]. The clauses quoted here are saved in `research/sources/udio-terms-2026-10-18.txt`.

**What the terms say (quotes under 125 characters; numbering is the page's).**

| Clause | Text | Meaning for the film |
|---|---|---|
| 1.2 | "You may not download copies of any Output or any other output generated by the Services." It also bars you from making Output available "on any personal device or on any streaming platform" [156]. | No legal route to a file on the maker's PC. |
| 6.3 | "you may use Output solely for your personal and non-commercial purposes", and may not download any copies of it from the App "for any purpose" [156]. | Use is personal and non-commercial only. A mostly public gathering strains "personal"; the download bar makes it moot. |
| 5.2 | Among the prohibited acts: "exploit the Services, any Output, or the outputs of other users for any commercial purpose" [156]. | Any commercial use is barred. |
| 6.1 | "the Company and/or its licensors own all right, title and interest in and to the Services and the Output"; ownership that "vests with you" is assigned to the Company [156]. | Udio and its licensors, not the user, own the Output. |
| 6.4 | A credit to Udio is required for public use of Output, except for Output generated during a paid subscription [156]. | Moot, given the rows above. |
| 1.1 and 6.3 (second paragraph) | "we may use your Input Content and any Output to train or otherwise improve our Services"; the licence over Your Content is "worldwide, perpetual and irrevocable" and "sub-licensable" [156]. | Anything uploaded as Input Content (a voice, a photo, a song) is licensed to Udio for good. |

**Reconciling the earlier reports.** The two secondary reports said downloads were disabled and that the terms were revised on 2025-11-12 to personal, non-commercial use [18]. Both are **confirmed by the primary text**: the revision date matches, and the page I read on 2026-10-18 still shows that revision, so there has been no later revision in 11 months. The Dubspot report that paid plans grant commercial use [14] is **contradicted** by clauses 5.2 and 6.3 as served. F3's verdict stands, now on primary evidence: **Udio cannot supply a file for a public screening.**

**New guardrail (inference).** Do not upload any family audio, voice recording, photo or humming to Udio, even as a style reference: clause 6.3 gives Udio a perpetual, irrevocable licence over it, which conflicts with the charter's rule that personal material stays private and with the consent given by the people heard.

---

### G7. Collecting-society practice for the premiere country, and the F6 consult question

The country is still open (playbook Step 2, decision date 2026-10-31). Below is what can be read in advance for the four societies named.

| Society | What I could read | Status |
|---|---|---|
| **GEMA (Germany)** | **Tarif T, version 46, valid from 2026-01-01** (PDF created 2025-12-01) is the tariff for music in single film screenings outside cinemas [157]. Fee: "1,3 % des Nettokartenumsatzes" per screening; **minimum per screening**: up to 150 people EUR 30.40, up to 300 people EUR 60.80, each further 150 people EUR 30.40; net amounts plus 7% VAT. A **15% discount** applies to events with a religious, cultural or social purpose that demonstrably pursue no economic aims (§39(3) VGG), on the per-screening rates only. The rates apply only if GEMA's consent is acquired "rechtzeitig vor Beginn der Nutzung" (in good time before use). The fee does not depend on how many works are played. It covers only GEMA's rights, not reproduction. **Consent is granted "unter der Voraussetzung", on condition that the right to use the music in the film has been properly acquired from the rightholders**, so sync is still your job. The tariff covers single screenings "außerhalb von Filmtheatern" (outside cinemas); regular screenings inside cinemas fall under Tarif T-F, not read. A clause on generative AI says that a licensee who claims AI output is not protected must prove it was made autonomously with no creative human contribution and reproduces no protected works or parts of works [157]. | **Primary, read.** Worked example with no ticket sales (our arithmetic): 120 guests EUR 32.53 gross; 200 guests EUR 65.06; 400 guests EUR 97.58, before any discount. The tariff does not name the payer; the organiser applying in advance is the natural reading (inference). Whether a family premiere qualifies for the 15% cultural/social discount: ask GEMA. |
| **PRS (UK)** | The home page and the licence pages (`/get-a-music-licence`, `live-music-and-event`, `business-and-commercial`, `tv-and-media-production`) return HTTP 200 but the delivered HTML holds navigation only, with no film-screening text [158]. | **UNVERIFIED.** The community-cinema guide in F5 [130] remains the only (secondary) source. |
| **SACEM (France)** | Blocked by the fetch tool; not tried by other means. | **UNVERIFIED.** |
| **IPRS (India)** | HTTP 403, Cloudflare "Attention Required!" page [155]. | **UNVERIFIED.** |

**The F6 consult paragraph stands unchanged.** Three add-on questions for whichever country is chosen, so the one hour is not spent on basics:
1. "Is a free, one-off showing at a private-hire venue to invited and uninvited guests a 'public' performance here, and which collecting-society licences does that trigger for the music inside the film?" (GEMA's tariff turns on the screening, not the film.)
2. "The tariff or licence says the society's consent assumes the music was properly licensed for the film. What evidence of sync and master clearance does the society or venue expect, and in what form?" (GEMA's Tarif T conditions its consent on exactly this [157].)
3. "If any music in the film is generative-AI output, who has to show whether it is protected by copyright: the licensee or the society?" (GEMA puts that burden on the licensee [157]; ask whether the chosen country does the same.)

Once the country is chosen, replace `[country, city]` in the F6 paragraph and add the venue question from F5. The maker alone takes the consult (see the context update above).

---

### G8. A measured re-conform cost for one late picture change inside a locked chapter

**What can be measured now, and what cannot.** F7's figures (about 0.6 maker-hours per finished minute of sound integration, 2 to 3 hours of sound rework for a 3-minute chapter per unlock, 0.1 to 0.3 hours for re-measure and re-export) are inference. No real chapter exists yet, so the human part (re-spotting, fixing crossfades, listening) cannot be timed honestly. The machine part can, and I timed it.

**Sandbox timing, one 3-minute stereo chapter (OWN [160]).** Input: a 48 kHz 24-bit stereo WAV (51.8 MB). Machine: 4 vCPU Linux sandbox, ffmpeg 6.1.1. Three runs each, wall-clock seconds:

| Step | Seconds (min to max) |
|---|---|
| Measure integrated loudness (`ebur128`) | 1.7 to 1.8 |
| `loudnorm` pass 1 (analyse) | 4.9 to 6.8 |
| `loudnorm` pass 2 (write 24-bit WAV; confirmed -18.0 LUFS on the output) | 1.3 to 1.8 |
| AAC 256 kbps encode for the online version | 12.3 to 13.2 |
| Re-export three 24-bit stems | 3.1 to 4.7 |
| **Total** | **23 to 28** |

So the scripted re-measure and re-export of a chapter is **under half a minute** here. The maker's PC and Resolve's own deliver page will differ, but the order of magnitude says F7's 0.1 to 0.3 hours (6 to 18 minutes) is almost entirely the human steps, above all the listen-through, not the rendering. Pass 2 followed the pass-1 numbers measured on the same file.

**Stopwatch protocol for the maker (so the numbers can be written back).** Time each step with a phone stopwatch; stop only for the step, not for breaks.

| Step | What is timed |
|---|---|
| T1 | From "picture change approved" to the new picture in the Resolve timeline; use Compare Timeline against the backup [142][143] to see what moved |
| T2 | Re-spot the cues after the change (the cues that moved or now miss a hit point) |
| T3 | Fix transitions: crossfades, room tone under the new length, ambience |
| T4 | Re-premix dialogue (levels only, per the S2 stage in F7) |
| T5 | Re-run loudness (LDR from G3, integrated, true peak) and re-export stems and masters (`ebur128` and `loudnorm` as above) |
| T6 | Listen-through of the whole chapter on the venue-class speakers or the closest thing |

Log one row per unlock:

```
unlock_id,date,chapter,minutes_of_chapter,change_type,delta_frames,cues_moved,t1_min,t2_min,t3_min,t4_min,t5_min,t6_min,total_min,hours_per_finished_minute,notes
```

`change_type` is one of: equal-length swap, shortening, lengthening. `delta_frames` is the signed change. `hours_per_finished_minute` is total hours divided by the chapter's minutes, directly comparable with the 0.6 in production-scale.

**When to measure (proposal, inference).**
1. **Dry run on the slice chapter, 2026-12-21 to 2026-12-27.** After G-SLICE (Sunday 2026-12-20) chapter 1 exists with its sound mix. Make one deliberate change: lengthen one shot by two seconds, then re-conform and time T1 to T6. This gives a first number three weeks earlier than January and tests the "keep each chapter's music as its own cue" rules from F7.
2. **First real unlock, from Sunday 2027-01-17** (G-MID, when rolling locks begin). Time the first chapter that is unlocked after its lock, using the same log.
3. **Write-back.** The orchestrator or a scribe replaces the inference in the F7 "What an unlock costs" paragraph with the measured rows, and sends the hours-per-finished-minute figure to the production-scale stage-hours table (sound integration 0.6; grade, mix, captions and QC 2.7) [149]. Until then the F7 numbers stay labelled inference.

---

### Changes to earlier notes (for the scribes)

1. **Playbook Step 15 ("DX-gated check"), Template G and research Deliverable 4:** add the EBU Loudness-to-Dialogue Ratio (G3): target 5 LU or less, fail above 6 LU; state that the source is broadcast guidance and "not production advice for feature films" [150][151]. Add the gating caveat (a quiet bed can read negative).
2. **Cue-sheet paragraph, playbook Template C, research Deliverables 2 and 5:** replace "check the template for exact terms" with the RapidCue `CueUsage` and `CueSubUsage` lists and the added fields (G1) [154]. [50] and [110] keep their tags for the deadline dates.
3. **Q3 (Udio row), F3 and Template (AI services):** replace "terms revised 2025-11-12, secondary" with the primary clauses (G6) [156]; add the guardrail never to upload family audio or photos to Udio.
4. **F5 table, GEMA row:** replace "payer and calculation UNVERIFIED" with the Tarif T figures (G7) [157]; add the sync-clearance condition and the generative-AI clause to the clearance pack.
5. **Template D2 "Routing" and Decision 6:** replace "at that track's next round" with the dated action in G4 (orchestrator patches `playbooks/surprise-ops.md` by Saturday 2026-11-07; maker approves).
6. **F9 / Step 14 (Resolve Free):** add the memory-cap setting and `memlog.ps1` (G5) [143]; the installed-build check is still open.
7. **F7 and the sound schedule:** add the machine-time measurement and a schedule row "2026-12-21 to 12-27, re-conform dry run on the slice chapter" (G8).
8. **Sources:** [96] Netflix loudness stays SR-only until the maker's browser read (G3).

### Remaining gaps after round 2

- Maker's browser reads (each 3 to 5 minutes): Musopen terms (G2, by 2026-10-31); Netflix dialogue-gated loudness section (G3); ASCAP deadline table, only if an ASCAP or BMI writer is in the cut (G1).
- Resolve Free on the installed build: effects present, peak memory, verdict (G5).
- Dolby and BBC primary guidance on dialogue level relative to programme level; any practitioner source for hall or PA playback (G3).
- PRS primary wording on films shown by guests; SACEM; IPRS (G7). These matter only for the chosen country.
- GEMA: whether a family premiere qualifies for the 15% cultural/social discount, and who the payer is (G7).
- The measured human-time re-conform figures (G8): dry run 2026-12-21 to 12-27; first real unlock from 2027-01-17.
- Carried forward from round 1 and not touched this round: Suno docket status after 2026-10-02; a real Voice Memos Lossless file for `ffprobe`; WhatsApp and iMessage handling of an attached .m4a; personality, privacy and publicity law for the actual premiere country.

### Sources added in round 2 (continue the numbering; tags as above)

**G3 loudness offset**
[150] EBU, Tech 3343, "Guidelines for Production of Programmes in accordance with EBU R 128", version 4, November 2023 (PDF created 2023-11-18, 46 pages) — https://tech.ebu.ch/docs/tech/tech3343.pdf — downloaded and text-searched 2026-10-18 — P (section 4.1 anchor signal; section 6 dialnorm; section 9.4 Cinematic Content, 9.4.1 to 9.4.3).
[151] EBU, R 128 s4, "Loudness Normalisation of Cinematic Content", supplement 4 to R 128, November 2023 (PDF created 2023-11-18, 6 pages) — https://tech.ebu.ch/docs/r/r128s4.pdf — downloaded and read in full 2026-10-18 — P (definitions, recommendations f) to q), Figure 1; scope note that it is not production advice for feature films and excludes cinema playback).
[152] EBU, Tech 3344, "Guidelines for distribution and reproduction in accordance with EBU R 128", v2.1, July 2016 — https://tech.ebu.ch/docs/tech/tech3344.pdf — downloaded and searched 2026-10-18 — P (section 6.7 and Annex A mention a -27 LUFS home-theatre offset; not otherwise used).
[153] Netflix, Sound Mix Specifications and Best Practices — https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001794307 (301 to) https://studiopartner.netflix.net/studio/branded-sound-mix-spec-and-best-practices — read 2026-10-18 — V — script-rendered; title "Knowledge Hub" only; content NOT read.

**G1, G2, G7 access results and cue sheets**
[154] RapidCue, Batch Reference Guide, April 2025 (PDF created 2025-04-28; copyright 2019-2025 BMI; support contact "RapidCue representatives at BMI and ASCAP"), with XML schema v1.4.5 — https://www.rapidcue.com/RapidCue%20Batch%20Reference%20Guide_April%202025.pdf ; https://www.rapidcue.com/Rapidcue_XML_Schema_v1.4.5.xsd ; home page https://www.rapidcue.com/ — downloaded and read 2026-10-18 — P (Appendix A.5 Cue Usage, A.6 Cue SubUsage, Cue field table, "no music" cue sheets).
[155] Access results, 2026-10-18 (not content): ASCAP https://www.ascap.com/help/royalties-and-payment/cue-sheets — plain HTTP 403 on the fetch tool and on curl; BMI https://www.bmi.com/creators/detail/cue_sheet_submission and https://www.bmi.com/creators/cue_sheets — HTTP 403, Cloudflare "Just a moment..." page; Musopen https://musopen.org/ and https://musopen.org/terms/ — same Cloudflare page; IPRS https://www.iprs.org/ — HTTP 403, Cloudflare "Attention Required!" page; backlothelp.netflixstudios.com and partners.bbc.co.uk — refused by the egress proxy. None circumvented.

**G6 Udio**
[156] Udio, Terms of Service, "Last Revised on November 12, 2025" — https://www.udio.com/terms-of-service — fetched 2026-10-18 (HTTP 200); text extracted from the page's server-rendered data — P — clauses 1.1, 1.2, 5.2, 6.1, 6.3, 6.4; capture of the quoted clauses in `research/sources/udio-terms-2026-10-18.txt`.

**G7 societies**
[157] GEMA, Tarif T, "Filmvorführungen", version 46, valid from 2026-01-01 (PDF created 2025-12-01, 4 pages) — https://www.gema.de/de/musiknutzer/tarifuebersicht/tarif-t ; PDF linked from that page as tarif_t_version46.pdf — downloaded and read in full 2026-10-18 — P.
[158] PRS for Music — https://www.prsformusic.com/ ; /get-a-music-licence ; /get-a-music-licence/live-music-and-event ; /business-and-commercial ; /tv-and-media-production — fetched 2026-10-18 (HTTP 200) — V — no film-screening text in the delivered HTML (navigation only).

**G5 Resolve**
[159] Blackmagic Design, DaVinci Resolve tech-specs page and Resolve and Fairlight product pages, and the support page https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion — read 2026-10-18 — V — no Windows RAM or GPU minimum for Resolve; no link to the Configuration Guide found. (The Resolve 21 manual's memory-cap text is under [143].)

**G3, G5, G8 own measurements and local files**
[160] Own measurements, 2026-10-18 (not a web source), 4 vCPU Linux sandbox, ffmpeg 6.1.1, PowerShell 7: (a) LDR sweep on a synthetic 3-minute chapter (speech clip as dialogue at -23.0 LUFS, steady pad as music); (b) timing of `ebur128`, `loudnorm` two-pass, AAC encode and stem re-export, three runs; (c) `memlog.ps1` run against an ffmpeg process (6 samples). Not run on Windows or on Resolve.
[161] LOCAL: `reviews/music-sound-round2.md` (nudge 6; section 9 "Notes for the orchestrator"); `playbooks/music-sound.md` Template D2 and Decision 6; `playbooks/surprise-ops.md` consent card (file times read 2026-10-18); `playbooks/production-scale.md` gates and stage-hours (via [149]); `CHARTER.md`.

## Changelog

- 2026-10-18, deltas applied from round 1 (C1 and the round-2 nudges, `reviews/music-sound-round2.md`; Haiku scribe): Deliverable 3d now carries the playbook D2 card (the long card with the festival and cinema line is withdrawn; tier C is a written ask after the premiere); F6 points to D2 answer B; the Deliverable 2 spotting header and worked row and the Deliverable 3e found-voice header are identical to playbook Templates B and D3; Summary 13, Q9, the REAPER tools row and F7's last sentence no longer carry the 2027-02-14 rehearsal, the January mix, the "unless started late" wording or the 02-12 schedule; source [8] rehearsal dates retired in both lists; the REAPER $60 personal-use condition (purchase page re-read 2026-10-18) added to Q9, the tools row and [103]; Deliverable 4 and the venue checklist point to the speech-span DX check; the D2 routing date is Saturday 2026-11-07. Still open, not applied here: the G3 loudness-to-dialogue text for playbook Step 15 and Template G, and the other round-2 "Changes to earlier notes" items.
