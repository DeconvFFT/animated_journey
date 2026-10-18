# Creator recipes from X/Twitter threads, Reddit, YouTube and blogs — research notes

Track `creator-threads` · Researcher: Sonnet · Written and verified 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline 2027-02-27.

## How this note was made (read first)

This track was supposed to be a sweep of social and creator sources. **That sweep could not be done.** Say so plainly to anyone who reads the recipe cards.

- **Web search was unavailable.** All six WebSearch calls I made at the start were refused ("this turn's web search budget is used up", the 200-call limit is shared by every agent in the turn). I did not try to get around it with other search engines, readers or archives.
- **Login-walled and blocked sources.** Reddit: the fetch tool refuses `www.reddit.com` outright, so r/editors, r/VideoEditing, r/StableDiffusion, r/comfyui, r/Minecraft, r/blender, r/DataIsBeautiful and r/genealogy were **not read at all**. X/Twitter: HTTP 402. Medium tag page: HTTP 403. Video Production Stack Exchange: refused. YouTube watch pages: redirected to a Google CAPTCHA, which I did not follow. Udio's terms page returned only a JavaScript shell.
- **What I did instead.** I fetched about sixty primary pages directly: terms and licence pages, official docs, GitHub READMEs and topic listings, a few Wikipedia articles, and YouTube's own oEmbed endpoint (which returns only title and channel, so it proves a video exists and who made it, nothing about its content). I also **tested the scriptable parts of three recipes in this sandbox** (CPU only, ffmpeg 6.1.1, Python 3.13, Pillow, numpy; no OpenCV, no GPU).
- **Consequence for the brief.** There is **no creator-documented evidence here** for: viral "my life in N seconds" edits, 2025-2026 AI photo-animation threads, parents' birthday or anniversary projects, "my life in Minecraft" builds and tributes, or what r/editors says about tribute videos. Those must-answer items are answered with "not reached" plus the nearest verified material, and are listed as gaps with the exact follow-up searches to run once search is available. Nothing is invented to fill them.
- **Evidence tags used below.** **[T]** = a tool, terms or documentation page I fetched on 2026-10-18 (summarised by a small model, so figures are as reported by that summary). **[L]** = tested by me in this sandbox. **(M)** = my own judgment or background knowledge, not backed by a source here. **UNVERIFIED** = could not be confirmed. "Checked 2026-10-18" applies to every cited page unless the page shows its own date.
- **Prompt-injection hygiene.** Everything fetched was treated as data. Two GitHub listings contain AI-tooling repos with marketing-style descriptions; I used them only as pointers.

---

## Summary

1. **Honest scope.** No creator thread, Reddit post or watched YouTube tutorial was read. Recipe cards are built from tool documentation and local tests, and each card says which. The follow-up searches that would fix this are listed under Open questions.
2. **A "growing-up morph" is two steps: align, then blend.** Alignment is a similarity transform from two eye points (angle from the eye vector, scale from inter-eye distance, translate the eye midpoint to a fixed target), documented by PyImageSearch on 2017-05-22 [27]. I re-implemented it with Pillow and numpy and got **about 1.4 px worst-case error** on synthetic images with two eye dots (rotated, scaled and shifted); it has not been tried on real faces [L][64]. Eye points can be hand-clicked or detected (MediaPipe returns 478 landmarks, page updated 2026-10-09 [29]).
3. **A true face morph is the weak link for a 50-year archive.** `face_morpher` (MIT, dlib) detects **frontal faces only and skips images where none is found** [28]; old prints with profiles, hats, glare or closed eyes will drop out. FILM, the free neural in-betweener, was **archived by its owner on 2025-10-14** [26]. Recommendation (M): use an aligned dissolve for a handful of same-pose pairs and do not build the film on a morph chain.
4. **The best-documented "life in N" exemplar is about rhythm, not tech.** Noah Kalina's *Everyday* (photos since 2000-01-10, shown at **six photos per second**, original piano score by someone close to him) [31][32] works because of a fixed rate and a human-made score. A 50-year archive has no daily photos, so the rate must be designed, not copied (M).
5. **AI photo animation is reproducible but GPU-bound.** Wan 2.2 is Apache-2.0; its README asks **24 GB VRAM for the 5B model** and 80 GB for the 14B image-to-video models [18], while ComfyUI's tutorial says the 5B model "should fit well on 8GB vram" with offloading [19]. WanGP claims **6 GB for select models** and shipped v18.17 on 2026-10-15 [20]. The maker's GPU is unknown, so plan on cloud or rented GPU, and treat 2025-2026 thread claims as UNVERIFIED.
6. **Two popular restoration/interpolation repos are now archived** (Microsoft Old Photos, **2026-10-03** [23]; FILM, 2025-10-14 [26]). They still run, but nothing may depend on them.
7. **Face animation and face swap are the ethics edge.** LivePortrait animates a still with a driving video, has a Windows one-click installer, and its authors warn about deepfake misuse [21]. InsightFace's pretrained models are **non-commercial research only** and its swap models need a licence from the company [22]. Default to *not* using face swap or speech-driven faces on a real person who cannot consent (Principle 4 and 5).
8. **Minecraft toolchain is fully Java-centred.** Replay Mod v2.6.27 supports Fabric from Minecraft 1.14.4 through **26.2** (new year-based version names), Forge only to 1.12.2 [52]; it renders straight to video with ffmpeg presets and custom ffmpeg arguments [53]. Alternatives and add-ons are Java-only too: Flashback (Fabric, client-side) [54], Iris shaders [55], Chunky [59]. Arnis can scaffold a **real place from OpenStreetMap by bounding box** (Apache-2.0; Java 1.17+, Bedrock, Luanti) [56]. Minecraft's price and usage guidelines are UNVERIFIED (the Mojang pages returned 503 on every attempt).
9. **Collage motion with real photos is mostly Transform + keyframes + masks.** Kdenlive 26.08.2 is free, has keyframes, masking and a Transform effect (position, size, rotation, rotation point, blend modes) [37][38][39][43]. Resolve 21 free is 8-bit, up to 60 fps, UHD; Magic Mask and the AI engine are Studio-only ($295) [35]. A "Paper Cutout Transition" Kdenlive tutorial exists on YouTube (title and channel confirmed; steps not seen) [44].
10. **Paper-wobble "on twos" is cheap and scriptable.** `pasteup` documents the parameters (`hold_frames`, `jitter_px`, `jitter_deg`, `seed`) [60]. I rebuilt the motion in Pillow and ffmpeg: **24 of 24 held pairs identical, 23 of 23 poses different, deterministic per seed** [L][66]. Photo pixels are only translated and rotated, never repainted, which keeps Principle 4.
11. **Suno (terms revised 2026-08-10, effective 2026-09-03): free-plan output is personal and non-commercial only; the free plan has no monthly downloads.** Pro is $8/month for 20 downloads, Premier $24/month for 60 [1][2]. Subscribing is not retroactive for earlier free-plan songs [4]. The terms **do not expressly address public performance** and give "no representation" that any copyright will vest in an Output [1]. Voice models may only resemble your own voice [1].
12. **Safest music is human-made with a plain licence.** Incompetech is CC BY 4.0 with a credit line, or a paid no-attribution licence whose price is not on the page [10][11]; CC BY permits adaptation and commercial use if credit is given [12]. Better still (M): a relative playing or singing, recorded for this. Under US law a gathering within "a normal circle of a family and its social acquaintances" is not a public performance [16]; that is a reading of a statute, not legal advice, and the maker's jurisdiction is unknown.
13. **Privacy surprises in "free" tools.** Eagle Animation sends error and usage events to PostHog by default (can be switched off) [61]; `pasteup` generates elements through the **Gemini image API** [60], which must never be fed family photos under the charter's no-third-party-upload rule.
14. **Do not follow** recipes that depend on paid phone apps, discontinued or frozen services, face swaps, synthetic voices of real people, or beat-synced reel grammar (full list in Q9 and Pitfalls).
15. **Three verified, agent-runnable recipe cores** exist now: eye-point alignment [64], Ken Burns plus crossfade through ffmpeg `zoompan` and `xfade` (13.0 s, 312 frames, 5.7 s render on CPU) [65], and seeded paper jitter [66]. Note the `zoompan` trap in Techniques T3 (a looped image input produced a 633 s file until fixed).

---

## Findings by question

### Q1. Which "my life in N seconds" or growing-up morph edits have creators documented step by step, and which steps are reproducible with free desktop tools?

**What I could verify: no creator walkthrough of a viral morph edit.** X, Reddit and YouTube content were unreachable (see top). What I could verify are the building blocks and one canonical exemplar.

| Step in a growing-up edit | What is documented | Free desktop? | Evidence |
|---|---|---|---|
| Find eye points in each photo | MediaPipe Face Landmarker: 478 3-D landmarks, Python, page updated 2026-10-09 [29]; dlib 68-point model used by PyImageSearch [27]; many other landmark libraries are listed on GitHub's face-alignment topic (210 repos; none described as cross-photo aligners, Windows/CPU use not stated) [30]; or click them by hand | Yes (Python; Windows/CPU behaviour not stated on the MediaPipe page, UNVERIFIED) | [T] |
| Align every photo | Rotate by the eye-vector angle, scale to a fixed inter-eye distance, translate eye midpoint to a fixed target; default desired left eye at (0.35, 0.35) of the frame [27] | Yes. Pillow/numpy version tested, ~1.4 px error [64] | [T][L] |
| Blend A to B | (a) dissolve; (b) triangle-mesh face morph, `face_morpher --images=<folder> --out_video=out.avi` [28]; (c) neural in-betweening (FILM, archived) [26]; (d) AI first-and-last-frame video, which Wan 2.2's ComfyUI tutorial lists as an "FLF2V" workflow [19] | (a) yes; (b) yes but frontal faces only [28]; (c) needs an NVIDIA GPU stack (CUDA 11.2.1) [26]; (d) needs a GPU | [T] |
| Frame rate / rhythm | *Everyday*: six photos per second [31]. For our archive: not documented anywhere I could read | n/a | [T] / (M) |
| Music sync | *Everyday* used an original piano score [31]. No source on beat-sync technique read | Kdenlive/Resolve timelines | [T] / (M) |
| Software | Kdenlive 26.08.2 [43] or Resolve 21 free [35] for the edit; ffmpeg for scripted assembly [65] | Yes | [T][L] |

**Exemplar facts, Noah Kalina "Everyday".** Started 2000-01-10 at age 19 (some sources say 2000-01-11; the 2006 YouTube upload was misdated); photos shown chronologically at six per second; original piano score by his then-girlfriend Carly Comando; uploaded August 2006; since 2008 the daily photo is taken with a Nikon Coolpix S10. The Wikipedia article does **not** describe how frames were aligned [31]. YouTube's oEmbed confirms the title "Noah takes a photo of himself every day for 6 years." on channel Noah Kalina [32]. His own site's fetched text was navigation only [no Everyday description].

**Reproducible with free tools:** alignment, dissolve, Ken Burns, music edit, scripted assembly. **Not reproducible as documented:** anything that relied on a phone app's auto-morph, because I found no app-specific recipe to evaluate (UNVERIFIED). **Our constraint (M):** *Everyday* has ~2,000 near-identical frames per six years; our archive has perhaps 30 to 80 usable photos over 50 years, with different cameras, framing and colour. A fixed-rate flipbook is not available, so either choose a few same-pose pairs (the same doorway, the same chair, the same hat) or give each photo a held beat.

### Q2. Which AI photo-animation threads from 2025-2026 show the full workflow with real old photos, what tools and cost, and which are still reproducible?

**Threads: none read.** What I can give is the state of the underlying tools on 2026-10-18, so any thread the next session finds can be checked against it.

| Tool | State on 2026-10-18 | Cost | Hardware claim | Evidence |
|---|---|---|---|---|
| Wan 2.2 (T2V-A14B, I2V-A14B, TI2V-5B; S2V and Animate variants added 2025-08-26 and 2025-09-19) | Weights released 2025-07-28; ComfyUI integration 2025-07-28; Apache-2.0; project claims no rights over outputs [18] | Free (local) | A14B: "at least 80GB VRAM"; TI2V-5B: 24 GB (RTX 4090 example), "under 9 minutes" for 5 s at 720p [18]; ComfyUI says 5B "should fit well on 8GB vram" via offloading [19] | [T] |
| ComfyUI Wan 2.2 workflows (5B hybrid, 14B I2V with high-noise and low-noise experts, 14B FLF2V first-last-frame) | Documented with model file names; the page itself notes an I2V step naming fp8 T2V files while the download list names fp16 I2V files, so check which models the workflow loads [19] | Free (local); ComfyUI Cloud exists but updates only after stable releases [19] | See above | [T] |
| WanGP (DeepBeepMeep) | v18.17 dated 2026-10-15; runs Wan 2.x, LTX, Hunyuan and others; Windows `scripts\install.bat`, Pinokio or desktop launcher; licence not named on the page, "no licence fee, subscription or donation required" to run locally [20] | Free | "as little as 6 GB of VRAM" for select models [20] | [T] |
| LivePortrait (Kuaishou/KlingAI Research) | Animates a still using a driving video or motion template; Windows one-click installer v20240829; latest update on page 2025-06-01; CUDA 12.4/12.6 may cause Windows issues, CUDA 11.8 suggested [21] | Free | VRAM not stated [21] | [T] |
| MyHeritage "Deep Nostalgia" | Launched February 2021, ~100 million animations, linked to D-ID [25] | A service (pricing not on the page) | n/a | [T] |

GitHub's old-photo-restoration topic lists the archived Microsoft repo (15.7k stars, last updated 2023-10-26 on the listing) and small newer projects, none of which I evaluated [24].

**Cost at the time / full workflow with real old photos:** UNVERIFIED. The sibling note `ai-imagery.md` covers restoration and the label ladder from fetched vendor pages; I did not re-verify it. **Still reproducible today?** The open tools above, yes, subject to a GPU. The ethical frame is in the pitfalls: animating a real face is allowed by the charter ("restore, restyle, animate") only if it stays visibly an animation and does not invent events or speech.

### Q3. What have people actually made for a parent's 50th, 60th or anniversary, how long did it take, and what did the parent respond to?

**Not reached.** Reddit, X and YouTube were the expected sources. I found **no verified account** of what a parent said afterwards. I will not generalise from nothing. The nearest verified material is structural, not testimonial:

- *Your Life in Weeks* (Wait But Why, 2014-05-07) uses one grid cell per week of a ~90-year life and describes its own effect as making life's finiteness concrete: "Those are your weeks and they're all you've got." [33] It was written for the author's own readers, not as a gift.
- **Tone warning (M):** a memento-mori framing may sit badly in a celebration for a woman in her 50s or 60s. Reuse the *grid as a structure* (one cell per year, filled with a real object or room) rather than the finiteness message. This is a judgment about dignity (Principle 5), not a sourced finding.
- Nicholas Felton's annual reports (2005 to 2014 are listed on his site) are a known model for personal-data "texture" of a life, but my fetch returned only navigation, so I cannot describe the format [34] (UNVERIFIED).

### Q4. What do "my life in Minecraft" and memorial-build creators do to make a build read as a specific real place, how do they capture it, and what tooling?

**Creator practices: not reached.** What is verified is the tool landscape (all versions as of 2026-10-18):

- **Edition.** Replay Mod, Flashback, Iris, Chunky and Mineways are Java Edition tools [52][54][55][59][57]. Arnis supports Java 1.17+, Bedrock and Luanti [56]. Mineways can read Bedrock worlds only after conversion [57]. **Java is the practical choice for filmed tours.**
- **Recording.** Replay Mod records a play session (roughly 2 to 10 MB per 10 minutes), then you edit camera paths with position keyframes (x, y, z, yaw, pitch, roll; cubic-spline interpolation by default, `O` for linear), time keyframes, and spectator keyframes; backwards time travel is not supported during a path [53]. It renders directly from Minecraft without screen capture, with presets for MP4 (x264), WEBM (VP8), MKV lossless, PNG sequence and OpenEXR sequence, and a custom ffmpeg command with placeholders `%WIDTH%`, `%HEIGHT%`, `%FPS%`, `%FILENAME%`, `%BITRATE%` [53]. Latest release v2.6.27; Fabric 1.14.4 to 26.2; Forge only 1.8.9 to 1.12.2; NeoForge not mentioned [52].
- **Shaders.** Replay Mod docs say Iris is "fully supported" from 1.16.5 but needs the custom Sodium build from the download page [53]; the download page banner says "Official Sodium (as of 0.4.3) is now compatible" [52]. These two pages disagree on whether the custom build is still needed, so test early. Iris: Fabric from 1.16.5, NeoForge from 1.21.1, **Forge not supported**; OptiFine, Canvas and Vulkan mods are incompatible [55].
- **Alternative recorder.** Flashback: Fabric only, client-side, Java 1.21 to 26.3, licence listed only as "ARR" (the page does not explain it), about 12.8 million downloads, updated "3 weeks ago" at capture [54].
- **Real-place scaffold.** Arnis turns OpenStreetMap plus elevation data into a world for a drawn rectangle or a CLI bounding box (`--bbox="min_lat,min_lng,max_lat,max_lng"`, modes `geo-terrain`, `geo-only`, `terrain-only`); Apache-2.0; official sources only GitHub and arnismc.com; the page does not mention entering an address [56]. It gives streets, building footprints and terrain; **interiors, objects, colours and the specific "kitchen table" must be hand-built (M).**
- **Stills and renders.** Chunky is a path tracer for Java worlds 1.2.1 and later, with a headless mode (software licence not stated; its manual is CC BY-NC-SA 4.0) [59]. Mineways 14.01 exports regions to OBJ and USD, page updated 2026-10-03, free and open source [57]. MCprep is a free Blender add-on that prepares materials and swaps meshes on worlds imported from Mineways or jmc2obj; the page shows releases up to v3.6.0 (August 2024) and copyright 2024, so **compatibility with current Blender is UNVERIFIED** [58].
- **What makes a build read as a specific place (M, not creator-sourced):** use measured layout (Arnis or a floor plan from relatives), one or two *wrong-on-purpose-but-true* objects per room (the chipped mug, the calendar), signage and colour from real photos, and a camera path that moves the way a visitor would. Build only places that appear in her real photos or in relatives' testimonies (Principle 4).
- **Minecraft price and usage guidelines: UNVERIFIED** (store page and `usage-guidelines` returned HTTP 503; I did not find any other Mojang page). Check before sharing any video outside the family.

### Q5. Which documented scrapbook, collage and paper-cutout motion techniques keep real photos real while adding warmth?

- **Pan and zoom ("Ken Burns").** Standard editors include it; only some (iMovie, Openshot) call it "Ken Burns", elsewhere it is "pan and zoom". It can crop to a detail and then move across the image, and can link one person in a photo to another as a transition [46]. Kdenlive has no named Ken Burns effect in the docs I read; **Transform + keyframes is the route** (position, size, rotation, rotation point, blend modes, keyframes supported; the page does not say it covers still images) [39]. A Kdenlive pan-and-zoom video tutorial by Peter Thomson exists (title and channel confirmed; content not seen) [45].
- **Cutout and photo-cutout animation** is a long tradition: flat materials "such as paper, fabrics or photographs" moved by stop-motion; Terry Gilliam's *Monty Python* sequences, JibJab, Röyksopp's "Eple" video (pans and zooms across many stills) are the named examples [47][48]. It is now often digital from scanned images [47].
- **Paper Cutout Transition in Kdenlive.** Video by Mint Visual, listed in Kdenlive's own tutorials page [40]; oEmbed confirms the title "Kdenlive | Paper Cutout Transition Tutorial" [44]. **Steps not seen.** Watch it before use; do not assume it is free of paid assets.
- **Masks, drop shadow and keyframes.** Kdenlive documents masking effects and keyframes [38]; its tutorials page lists an "Add Drop Shadow" video, an "Object Mask" video and "Keyframe Interpolation" by Nuxttux Creative Studio, and rotoscoping and stabilization videos by Arkengheist (titles only) [40]. The written tutorials listed are 2011 and 2015 and the page warns they may be out of date [41].
- **Resolve route.** Free version covers 8-bit up to 60 fps and UHD; Magic Mask, optical blur, film grain and the AI engine are Studio-only; whether Fusion is limited in the free version is not stated on the page [35]. Free official training: Fusion lessons (58 min to 1 h 14 min each) and PDF guides for Resolve 20, one version behind [36].
- **Wobble on twos (paper-in-motion).** `pasteup` documents the animation vocabulary: a new pose every `hold_frames` frames (2 smooth, 3 chunky), `jitter_px`, `jitter_deg`, `seed` [60]. I implemented the same idea in Pillow and ffmpeg with a printed-photo border: held pairs identical, poses differ, same seed gives the same result [L][66]. **Photos stay photographs** because only a rigid transform is applied.
- **Where warmth comes from while keeping photos real (M):** paper texture and shadow *around* the photo, tiny physical wobble, hand-written captions in a relative's handwriting, never altering the photo's pixels beyond restoration.

### Q6. How do hobbyists do stop-motion with printed photographs, objects and hands, and what does that offer for marking reconstructions visibly?

**Hobbyist recipes: not reached.** Verified material:

- **Vocabulary.** "Stop motion with live actors is often referred to as pixilation"; "stop motion of flat materials such as paper, fabrics or photographs is usually called cutout animation"; object animation covers almost any object [48].
- **Free capture software.** Eagle Animation: GPL-3.0; Windows, macOS, Linux, Android and a web version; camera and DSLR capture (DSLR limits by platform), timeline, onion skinning, grid, difference mode, frame averaging to reduce noise, export to video or frames; **error and usage events go to PostHog by default, switchable off in Settings** [61]. Boats Animator: GPLv3; Windows, macOS, Linux; webcam capture at 1080p and above, onion skin, export; its `main` branch is being rewritten and the README's Releases section was empty on the fetched page, so use a tagged release, not `main` [62]. The GitHub stop-motion topic lists both and others, with licences shown only for two entries [63]. qStopMotion was not in that listing, so I cannot confirm it.
- **What it offers for visible reconstructions (M):** a hand in frame, a visible table, a slightly irregular pace: all signals that a scene was *made*, not found. That aligns with Principle 4 ("reconstructed scenes are visibly reconstructions"). Photographs shown in their original frame stay clean and steady; reconstructions are the ones with paper edges, hands and wobble. A consistent visual grammar the audience learns in one minute is the goal.

### Q7. For AI music: what do creators report about Suno, Udio and alternatives, what do current terms say about ownership and public performance, and what are the free human-made alternatives with clear licences?

**Creator reports:** not reached. **Terms (checked 2026-10-18):**

| Item | Suno | Udio |
|---|---|---|
| Terms version | Last revised 2026-08-10, effective 2026-09-03 [1] | Page returned only a title, **UNVERIFIED** [7]; help centre lists no ownership or commercial-use articles in the visible titles [8] |
| Free tier | Output limited to "lawful, personal and non-commercial purposes"; songs "cannot be monetized"; shareable via a Suno link [1][5] | UNVERIFIED |
| Downloads | Free: no monthly song downloads on the pricing page [2]; users who joined before 2026-09-03 get up to 7 trial downloads (extra purchasable), later joiners "occasionally" get trial downloads; **trial downloads are not eligible for commercial use** [6]. Pro: 20/month, Premier: 60/month, credits do not roll over [2][3][6] | UNVERIFIED |
| Price | Free $0 (50 credits/day); Pro $8/month (2,500 credits); Premier $24/month (10,000 credits); pricing page is undated [2] | UNVERIFIED |
| Ownership | Pro/Premier: Suno "assigns to you all of its right, title and interest in and to any Output owned by Suno", subject to commercial-use restrictions; **"Suno makes no representation or warranty… that any copyright will vest in any Output"** [1] | UNVERIFIED |
| Retroactive | Subscribing does not give "retroactive commercial use licensing" for earlier free-plan songs, though Suno "may offer retroactive rights in certain cases" [4] | UNVERIFIED |
| Public performance | **Not expressly addressed** in the terms text I received [1] | UNVERIFIED |
| Voices | You may create a Voice Model only resembling **your own** voice; you may not create one of another person; do not upload recordings of another person's voice [1] | UNVERIFIED |
| Watermark/metadata | Must not be removed or circumvented; Suno may append tier and download-status metadata [1] | UNVERIFIED |
| Lyrics | You own lyrics you wrote, regardless of plan [3] | UNVERIFIED |

**Reading for a private tribute (M, not legal advice):** a family gathering is personal use, which the free tier allows, but the free tier gives no way to get the audio file into a video except occasional trial downloads. A paid month (Pro, $8) is the realistic path to a file. Because the terms do not address public performance and make no copyright promise, treat AI music as a *scratch track* and keep a licensed or family-made replacement ready. Never use a Voice Model of the honouree or anyone else (violates the terms and Principle 4).

**Public performance in law.** US copyright law defines performing "publicly" as performing at a place open to the public, or any place where "a substantial number of persons outside of a normal circle of a family and its social acquaintances" is gathered [16]. A surprise at home with family and friends is plausibly within that circle; a hired hall that is also open to the public, or a stream to a wider audience, is different. Jurisdiction of the event is unknown (open decision in the charter).

**Free human-made alternatives with clear licences (checked 2026-10-18):**

- **Incompetech (Kevin MacLeod).** Free tier: "No charge. Requires that you credit the music." FAQ credit text: "Licensed under Creative Commons: By Attribution 4.0"; edited tracks must say which parts are yours; credit "should not be obscured"; paid Standard License (no attribution) via PDF and PayPal, price not on the page [9][10][11]. CC BY 4.0 permits adaptation and commercial use but requires credit, a licence link and an indication of changes [12]. The home page carries an April 2, 2026 note that tracks are royalty-free for podcasts [9].
- **Pixabay Content License.** Free commercial use, no attribution required; but the summary says nothing specific about music, and says some content may carry other rights [13]. Read the full licence for the track before use.
- **YouTube Audio Library.** CC tracks need credit; the standard licence needs none; use outside YouTube is not addressed and YouTube says it cannot give legal guidance off-platform [14]. Not a safe default for a non-YouTube screening.
- **Free Music Archive.** The page I received shows only "Free to play, download and share" and no licence detail [15] (UNVERIFIED for specific tracks). Musopen returned 403 (not read).
- **ACE-Step (local, open model).** Apache-2.0 code; demo and weights 2025-05-06, report 2025-06-02, v1.5 on 2026-01-28; needs about 8 GB VRAM after a May 2025 update; the page states no commercial-use terms, does not describe training data, and warns of "unintentional copyright infringement" risk [17]. Treat as experimental.
- **Best option (M):** a relative or friend plays or sings something *she* loves, recorded once, owned by the family. No licence question, and it carries Principle 1 and Principle 3.

### Q8. What do experienced editors on r/editors and r/VideoEditing say are the common mistakes in family tribute videos, and what do they recommend?

**Not reached** (Reddit is blocked at the tool level). I have no sourced answer. The only verified material is that pan-and-zoom is built into most editors and is ubiquitous [46], which is a reason to ration it, not evidence of an editors' consensus. Hypotheses to test in the vertical slice with three viewers outside the family, **not findings** (M): length that outlasts the room; music that fights narration; the same transition on every cut; captions that repeat what the audience can see; photos held too short to read faces. Replace with sourced findings when the Reddit search is possible.

### Q9. Which recipes should we NOT follow?

- **Paid phone-app auto-morph and "life in 60 seconds" apps.** I found no verified recipe to port, so no card. Any thread that names a subscription app is a not-reproducible flag unless it gives a desktop equivalent.
- **Face swap.** InsightFace's code is MIT but its pretrained models and data are "non-commercial research purposes only"; its swap models need a commercial licence from the company [22]. Fabricated faces also break Principle 4.
- **Synthetic voices of real people.** Suno forbids Voice Models of another person [1]; the charter forbids "putting words in anyone's mouth".
- **Speech-driven talking faces from old photos.** Same reason. LivePortrait's own authors flag deepfake risk [21].
- **Frozen or archived dependencies as critical path:** Microsoft Old Photos (archived 2026-10-03; README says "for academic research use only", trained on 256x256 images) [23]; FILM (archived 2025-10-14) [26]; Boats Animator `main` (being rewritten) [62].
- **Tools that upload personal media by design.** `pasteup` generates cut-out elements via the Gemini image API [60]. Use it, if at all, with abstract prompts and *no* family photos. Eagle Animation telemetry: switch it off [61].
- **Beat-synced reel grammar.** The stop-motion listing includes a repo described as turning photo bursts into "beat-synced stop-motion boomerang clips" [63] (one-star repo, description only). Harvest alignment and rhythm discipline; discard beat-synced zooms, whip pans and trending sounds.
- **Beyond the charter:** AI-invented "memories" (a scene that did not happen), unlabeled AI in-betweens between two real photos (the Wan FLF2V route [19] fabricates the in-between: either label it as a reconstruction or avoid).

---

## Exemplars / recipes

Template for every card: **Source and date** · **Creator and incentive** · **Goal** · **Tools and cost (checked 2026-10-18)** · **Steps** · **Time and cost to reproduce** · **Quality: does it look generic?** · **Charter principles** · **Free-desktop adaptation** · **Verdict**. Scores are R = relevance to our project and F = feasibility for a learner plus agents by 2027-02-27 (1 to 5). Evidence class in brackets. "Creator" is the maintainer or author of the page, not necessarily a viral creator.

### Ranked list

| Rank | Card | R | F | Evidence | Verdict |
|---|---|---|---|---|---|
| 1 | C1 Eye-aligned dissolve ("same pose, decades apart") | 5 | 5 | [T][L] | Adopt for the vertical slice |
| 2 | C2 Scripted still-photo motion (Ken Burns + crossfade via ffmpeg) | 4 | 5 | [L] | Adopt as baseline; ration its use |
| 3 | C3 Paper-print wobble on twos for reconstructions | 4 | 5 | [T][L] | Adopt |
| 4 | C4 Licensed or family-made music with credit card | 5 | 5 | [T] | Adopt |
| 5 | C5 Replay Mod cinematic tour of a hand-built Minecraft room | 4 | 4 | [T] | Prototype if the format is a world |
| 6 | C6 Hand-shot printed-photo stop-motion (Eagle Animation) | 4 | 4 | [T] | Prototype one scene |
| 7 | C7 Kdenlive paper-cutout transition (Mint Visual) | 3 | 4 | title only | Watch the video, then decide |
| 8 | C8 Arnis real-place scaffold, then hand-detail | 4 | 3 | [T] | Prototype with her childhood street |
| 9 | C9 Wan 2.2 gentle-life image-to-video on single photos | 3 | 3 | [T] | Prototype with a rented GPU, label it |
| 10 | C10 Life-grid timeline device | 3 | 4 | [T] | Adapt (change tone) |
| 11 | C11 Mineways + MCprep to Blender diorama stills | 3 | 2 | [T] | Watch (compatibility UNVERIFIED) |
| 12 | C12 face_morpher morph pairs | 2 | 3 | [T] | Use only for a few frontal pairs |
| 13 | C13 Suno AI scratch track | 2 | 4 | [T] | Scratch only, not the final |
| 14 | C14 LivePortrait head-turn on a still | 2 | 3 | [T] | Hold; ethics gate first |
| 15 | C15 Old-photo restoration CLI (MS Old Photos) | 2 | 3 | [T] | Do not depend on it |

### C1. Eye-aligned dissolve ("same pose, decades apart")
- **Source and date:** alignment method, PyImageSearch, 2017-05-22 [27]; rhythm exemplar, *Everyday*, 2006 upload [31][32]; local implementation 2026-10-18 [64].
- **Creator and incentive:** Adrian Rosebrock (PyImageSearch); free post, code behind an email sign-up, promotes paid courses [27]. Noah Kalina: personal artist; no incentive seen.
- **Goal:** show one person across decades with her eyes locked to the same screen position, so the face "stays" while the years change.
- **Tools and cost:** Python 3 + Pillow + numpy (free) [L]; optional MediaPipe or dlib for landmarks (free; MediaPipe code samples Apache-2.0) [29]; ffmpeg (free).
- **Steps:** (1) pick same-pose pairs from the real archive; (2) get left and right eye centres per photo (click them in any image viewer, or detect them); (3) run `align()` from Techniques T1 to a 1080x1080 or 1920x1080 canvas; (4) crossfade with `xfade` (T3); (5) hold on each portrait long enough to read the face; (6) score with the family-made music (C4).
- **Time and cost:** ~1 hour for 6 pairs including clicking eye points (M); $0.
- **Quality:** the dissolve is plain and honest. A dissolve between faces with different expressions can look ghostly (M). It is only generic if it is applied to every photo at a fixed rate.
- **Charter:** respects 1, 4, 6, 7. Risk to 3 if used as the only device.
- **Free-desktop adaptation:** already free. For old prints, restore (sibling note) before aligning, and keep un-restored scans as masters.
- **Verdict:** adopt.

### C2. Scripted still-photo motion: Ken Burns + crossfade
- **Source and date:** ffmpeg `zoompan` and `xfade` filters, verified present in ffmpeg 6.1.1 [65]; concept of pan and zoom [46].
- **Creator and incentive:** none (open-source tooling).
- **Goal:** a repeatable, agent-runnable baseline for photo-in-motion.
- **Tools and cost:** ffmpeg (free) [L].
- **Steps:** use the tested script in T3. Upscale to 3840 first, push in about 8% over each clip's duration, 1-second `xfade`, 24 fps, H.264 CRF 18.
- **Time and cost:** my test: three 1080x1080 clips, 13.0 s output, 312 frames, **5.7 s wall time** on this CPU [L]. $0.
- **Quality:** unmodified, this is the most generic look in slideshow software; "Ken Burns" is a built-in preset in many editors [46]. Use *tiny* moves toward a detail that matters (the hands, the doorway), and not on every photo.
- **Charter:** respects 7; risks 3 if used uniformly.
- **Free-desktop adaptation:** same recipe in Kdenlive via Transform keyframes [39] for hand adjustment.
- **Verdict:** adopt as the baseline; require a "why this move" note per shot (Principle 2).

### C3. Paper-print wobble on twos for reconstructions
- **Source and date:** `pasteup` README parameters (undated; v1.1.0, © 2026) [60]; cutout-animation background [47][48]; local test 2026-10-18 [66].
- **Creator and incentive:** tmoody1973, open-source (MIT); 4 commits, 4 stars at fetch time, so immature [60].
- **Goal:** make *reconstructed* scenes look hand-made (paper pieces moved by hand) while photographs stay still and clean.
- **Tools and cost:** Pillow + ffmpeg (free) [L]. Do **not** use pasteup's Gemini-based generation on family material [60].
- **Steps:** (1) cut or draw the reconstructed element as a PNG with transparency; (2) run `jitter_twos.py` (T5) with `hold_frames=2`, `jitter_px≈3`, `jitter_deg≈0.6`, a fixed `seed`; (3) encode at 24 fps; (4) place it over a plain paper or wood backdrop.
- **Time and cost:** a few minutes per element once drawn; $0.
- **Quality:** the wobble reads as handcraft; random-jitter filters can look like a cheap effect if too strong (M). Keep the amplitude small.
- **Charter:** strongly respects 4 (visibly a reconstruction), 2, 7.
- **Free-desktop adaptation:** same recipe in Kdenlive: keyframes every second frame is tedious, so script it.
- **Verdict:** adopt.

### C4. Licensed or family-made music with a credit card
- **Source and date:** Incompetech licence and FAQ [10][11]; CC BY 4.0 [12]; US definition of "publicly" [16].
- **Creator and incentive:** Kevin MacLeod sells a no-attribution licence [10].
- **Goal:** music with a clear licence for a family screening and possibly a shared file.
- **Tools and cost:** free with credit; paid option price not stated on the page [10].
- **Steps:** (1) prefer a family-made recording; (2) otherwise pick an Incompetech track; (3) end card text: "Licensed under Creative Commons: By Attribution 4.0" plus track title, author and licence link [11][12]; (4) if you edit the track, say which parts are yours [11]; (5) save the licence page URL and date in the asset manifest.
- **Time and cost:** 30 minutes; $0.
- **Quality:** library tracks can sound stock (M); a family recording does not.
- **Charter:** respects 1 and 3 if family-made.
- **Free-desktop adaptation:** none needed.
- **Verdict:** adopt.

### C5. Replay Mod cinematic tour of a hand-built Minecraft room
- **Source and date:** Replay Mod site, download page and docs [51][52][53]; Iris [55].
- **Creator and incentive:** CrushedPixel and johni0702; Patreon link on the site [51].
- **Goal:** a filmed walk through one real room (her kitchen or childhood bedroom) in Minecraft.
- **Tools and cost:** Minecraft Java (price UNVERIFIED), Fabric, Replay Mod v2.6.27 (free; pricing not stated on the page), optionally Iris + Sodium [52][55].
- **Steps:** (1) install Fabric for a version Replay Mod lists; (2) record yourself walking the build; (3) in the replay editor, place position keyframes on a spline (use `O` for straight moves), and time keyframes if needed (no backwards time); (4) render with an MP4 preset at 1080p or a PNG sequence; (5) for shaders, install Iris and follow the Replay Mod download page for the Sodium build [52][53].
- **Time and cost:** UNVERIFIED; the build time dominates, the filming is hours (M).
- **Quality:** the look depends on the build and resource pack; default Minecraft is recognisable and can feel like a trend (M).
- **Charter:** respects 4 (visibly voxel); 2 only if each room means something.
- **Free-desktop adaptation:** all free except the game. Windows-friendly.
- **Verdict:** prototype only if the format decision includes a world.

### C6. Hand-shot printed-photo stop-motion (Eagle Animation)
- **Source and date:** Eagle Animation README [61]; cutout definition [48].
- **Creator and incentive:** open-source (GPL-3.0); telemetry on by default [61].
- **Goal:** film printed photos, handwriting and hands on a table frame by frame, to link two moments.
- **Tools and cost:** Eagle Animation (free), webcam or DSLR, a stand [61].
- **Steps (M, from the feature list):** (1) turn telemetry off; (2) lock the camera and lights; (3) use onion skinning for small moves; (4) shoot on twos at 12 images per second of motion; (5) export frames or video and bring them into Kdenlive; (6) keep each photo whole and in its original frame; do not crop into faces.
- **Time and cost:** a day for ~15 seconds including setup (M); $0 plus a stand.
- **Quality:** can look charming or amateur; hand-visible motion is the point.
- **Charter:** respects 4, 2; stresses 6 (time-expensive).
- **Free-desktop adaptation:** already free.
- **Verdict:** prototype one scene for the "reconstruction" grammar.

### C7. Kdenlive paper-cutout transition (Mint Visual)
- **Source and date:** YouTube video "Kdenlive | Paper Cutout Transition Tutorial" by Mint Visual; date not seen; title confirmed via oEmbed [44]; listed in Kdenlive's own tutorials page [40].
- **Creator and incentive:** unknown.
- **Goal / steps / cost:** **steps not seen** (UNVERIFIED).
- **Verdict:** watch it, check for paid assets, and test on Kdenlive 26.08.2; the docs' Windows page covers older issues [42].

### C8. Arnis real-place scaffold, then hand-detail
- **Source and date:** Arnis README (© 2022-2026) [56].
- **Creator and incentive:** Louis Erbkamm; open-source (Apache-2.0); warns that only GitHub and arnismc.com are official [56].
- **Goal:** start from the true street layout of a childhood neighbourhood.
- **Steps:** (1) pick a bounding box around the street; (2) run the GUI or `cargo run --release --no-default-features -- --output-dir=… --bbox="min_lat,min_lng,max_lat,max_lng"`; (3) open the world in Java; (4) rebuild the buildings that matter from photos and testimony.
- **Time and cost:** generation minutes; hand-detail days (M). $0 plus Minecraft.
- **Quality:** OSM-derived blocks are generic until hand-built (M); the page lists no limitations [56].
- **Charter:** respects 4 and 1 only if she lived there; privacy: coordinates of her real home go through the tool locally, check that it does not phone home (UNVERIFIED).
- **Free-desktop adaptation:** already free. **Verdict:** prototype.

### C9. Wan 2.2 gentle-life image-to-video on single photos
- **Source and date:** Wan 2.2 README [18]; ComfyUI tutorial [19]; WanGP v18.17, 2026-10-15 [20].
- **Creator and incentive:** Wan team; WanGP by DeepBeepMeep, no fee stated [20].
- **Goal:** very small motion (breath, light, a curtain, camera drift) on a photo, labelled as animation.
- **Steps (from [19]):** load the diffusion, VAE and text-encoder files; load the starting image; write a short, restrained prompt; set length; run. For lower VRAM use the 5B model or WanGP [19][20].
- **Time and cost:** UNVERIFIED on real archival photos. Hardware is the main cost: 24 GB for 5B per the README, 8 GB with offloading per ComfyUI [18][19]; rented GPU price not checked.
- **Quality:** unknown on old prints. Risk of drifting faces and invented details (M).
- **Charter:** 4 requires the label ladder (see `ai-imagery.md`) and restraint; 5 if motion changes expression.
- **Free-desktop adaptation:** maker's Windows GPU unknown; use cloud.
- **Verdict:** prototype one photo, compare against the still.

### C10. Life-grid timeline device
- **Source and date:** *Your Life in Weeks*, 2014-05-07 [33].
- **Creator and incentive:** Wait But Why sells a printed Life Calendar poster [33].
- **Goal:** a chapter-selector or opening graphic where each cell is a year of her life, opened by a real object.
- **Steps (M):** draw 50-plus cells (years, not weeks), fill each with a real photo or object, let one cell open into a chapter.
- **Quality:** a known device; generic if left as a grid.
- **Charter:** 2 (the mechanic must mean something); 5 (avoid the finiteness tone).
- **Verdict:** adapt as an index, not an elegy.

### C11. Mineways + MCprep to Blender diorama stills
- **Source and date:** Mineways 14.01 (page updated 2026-10-03) [57]; MCprep (page shows 2024 material) [58]; Blender licence [49].
- **Steps:** export region to OBJ/USD with Mineways; import into Blender; prep materials with MCprep; render with Eevee or Cycles.
- **Cost:** free. **Quality:** high, steep learning curve. **Risk:** MCprep vs current Blender UNVERIFIED.
- **Verdict:** watch, test early.

### C12. face_morpher morph pairs
- **Source:** [28]. **Steps:** `python facemorpher/morpher.py --src=<a> --dest=<b> --plot` or `--images=<folder> --out_video=out.avi`; needs dlib and `shape_predictor_68_face_landmarks.dat`. **Limit:** frontal faces only [28]. **Windows install of dlib: UNVERIFIED.**
- **Quality:** the classic viral morph look; generic if overused.
- **Verdict:** use for 2 or 3 pairs at most.

### C13. Suno AI scratch track
- **Source:** [1][2][4][5][6]. **Steps:** make a track on any plan; if you want the file, pay for one month of Pro ($8) and download within the 20-download limit; do not use a Voice Model of anyone but yourself. **Quality:** generic-sounding unless guided by specific lyrics (M). **Verdict:** scratch only; replace with C4.

### C14. LivePortrait head-turn on a still
- **Source:** [21][22]. **Steps:** `python inference.py -s <photo> -d <driving.mp4>` [21]. **Charter gate:** needs a trusted proxy's approval, a neutral driving video, no speech, visible labelling. **Licence:** LivePortrait's own licence text was not in the fetched content; InsightFace's models are non-commercial research only [22]; whether LivePortrait uses them is UNVERIFIED (M: I believe it does).
- **Verdict:** hold.

### C15. Old-photo restoration CLI (Microsoft Old Photos)
- **Source:** [23]. **Command:** `python run.py --input_folder … --output_folder … --GPU 0 --with_scratch` [23]. **Status:** archived 2026-10-03; "academic research use only"; trained at 256x256. **Verdict:** do not depend on it; see `ai-imagery.md` for other restorers (not re-verified here).

---

## Creators worth following during the build phase

Selection is by documented relevance, not popularity. I could not vet quality (no watch time). Incentives noted where seen.

| Who | Why | Where | Incentive/caveat |
|---|---|---|---|
| Noah Kalina | The reference case for a person's passage of time, rate and score | YouTube @NoahKalina [32] | Artist/photographer; his site's navigation lists Commissions [68] |
| Mint Visual | Kdenlive paper-cutout transition | YouTube @mintvisual [44] | Unknown; check for paid assets |
| Peter Thomson | Kdenlive pan and zoom | YouTube @dartmoorrambler [45] | Unknown |
| Nuxttux Creative Studio | Broad Kdenlive series: keyframes, masks, drop shadow, text [40] | YouTube (listed on Kdenlive docs) | Titles only seen |
| Arkengheist | Kdenlive rotoscoping, stabilization, motion tracking [40] | YouTube | Titles only seen |
| Louis Erbkamm (Arnis) | Real-place Minecraft worlds [56] | GitHub | Open-source |
| CrushedPixel, johni0702 (Replay Mod) | The filming tool for Minecraft tours [51] | replaymod.com | Patreon |
| DeepBeepMeep (WanGP) | Fast-moving low-VRAM video models; v18.17 on 2026-10-15 [20] | GitHub | Free to run, no donation required |
| Kevin MacLeod (Incompetech) | Clearly licensed music with a FAQ [9][11] | incompetech.com | Sells a no-attribution licence |
| Blackmagic Design training | Free Fusion lessons and PDFs for Resolve [36] | blackmagicdesign.com | Sells Studio |

---

## Tools

Cost and availability as of 2026-10-18. "Scriptable" means usable from the command line by an agent.

| Tool | Cost / free tier | Platform | Learning curve | Scriptable | Notes |
|---|---|---|---|---|---|
| Kdenlive 26.08.2 | Free; donations requested [43] | Windows 10+ (installer and standalone exe), Linux, macOS 13+ [43] | Medium | Render dialog verified; CLI/batch rendering **UNVERIFIED** [50] | Keyframes, masks, Transform [38][39]; Windows-troubleshooting page covers older versions [42] |
| DaVinci Resolve 21 (free) | Free; Studio $295 [35] | Windows, macOS, Linux (not stated on page, M) | Medium to high | Limited (M) | Free: 8-bit, up to 60 fps, UHD; Studio-only features listed [35]; free PDFs for Resolve 20 [36] |
| Blender | Free, GPL; output is yours, commercial OK [49] | Windows, macOS, Linux | High | Yes (Python, CLI) | Manual page shown was Blender 5.2 LTS [67]; the Grease Pencil overview text was not retrieved |
| ffmpeg 6.1.1 (sandbox) | Free | all | Medium | Yes | `zoompan`, `xfade` verified [L] |
| Pillow 12.3 + numpy 2.5 (sandbox) | Free | all | Low | Yes | Alignment and jitter tested [L] |
| MediaPipe Face Landmarker | Free; code samples Apache-2.0 [29] | Python, Android, Web, iOS | Low to medium | Yes | 478 landmarks; eye-centre indices and Windows CPU use not confirmed on the page |
| dlib + imutils (PyImageSearch) | Free (licences not stated on the post) [27] | cross-platform | Medium; Windows build UNVERIFIED | Yes | 68-point model |
| face_morpher | Free, MIT [28] | Python | Medium | Yes | Frontal only |
| FILM | Free, Apache-2.0; **archived 2025-10-14** [26] | NVIDIA GPU, CUDA 11.2.1 | High | Yes | Do not depend on it |
| Wan 2.2 | Free, Apache-2.0 [18] | GPU | High | Yes | 24 GB (5B) / 80 GB (14B) per README; 8 GB with offload per ComfyUI [18][19] |
| WanGP | Free [20] | Windows, others | Medium | Partly (web UI) | v18.17 2026-10-15 |
| LivePortrait | Free; licence text not seen [21] | Windows, Linux, macOS (Apple Silicon) | Medium | Yes (`inference.py`) | Ethics gate |
| MS Old Photos | MIT, research only, **archived 2026-10-03** [23] | Python | High | Yes | |
| Replay Mod v2.6.27 | Free (price not stated on page) [52] | Java Edition; Fabric 1.14.4 to 26.2 | Medium | In-game | Rendering to ffmpeg [53] |
| Flashback | Price not stated; licence "ARR" [54] | Fabric only | Low to medium | In-game | |
| Iris | Free, open source; licence name not on the page [55] | Fabric from 1.16.5, NeoForge from 1.21.1 | Low | n/a | No Forge |
| Chunky | Cost not stated; manual CC BY-NC-SA [59] | Windows, Linux, macOS; Java 1.2.1+ | Medium | Headless mode | |
| Arnis | Free, Apache-2.0 [56] | Java 1.17+, Bedrock, Luanti | Low | Yes (CLI) | Official sources only |
| Mineways 14.01 | Free, open source [57] | Windows (Mac and Linux help pages) | Medium | Partly | |
| MCprep | Free; licence/price not named [58] | Blender add-on | Medium | Via Blender | Compatibility UNVERIFIED |
| Eagle Animation | Free, GPL-3.0 [61] | Windows, macOS, Linux, Android, web | Low | No | Telemetry on by default |
| Boats Animator | Free, GPLv3 [62] | Windows, macOS, Linux | Low | No | `main` being rewritten |
| pasteup | Free, MIT; needs Claude Code, ffmpeg, Gemini API key [60] | Python 3.10+ | Low | Yes | Third-party upload of prompts/images |
| Suno | Free / $8 / $24 [2] | Web | Low | No | Terms in Q7 |
| Udio | UNVERIFIED [7][8] | Web | | | |
| Incompetech | Free with credit; paid option price not on page [10] | Download | Low | n/a | CC BY 4.0 per FAQ [11] |
| ACE-Step | Free, Apache-2.0 [17] | Windows, macOS, Linux; ~8 GB VRAM | Medium | Yes | No commercial terms stated |
| Minecraft Java | **UNVERIFIED** price | Windows | | | Store page 503 |

---

## Techniques

All code below was run in this sandbox on 2026-10-18. Scripts are not stored in the repo; the text here is the source.

### T1. Two-point eye alignment (similarity transform)
Method after PyImageSearch [27]; implementation tested [L][64]. Worst error 1.36 px on three synthetic cases (rotation -12 to +9 degrees, scale 0.6 to 1.7).
```python
import math, numpy as np
from PIL import Image
def align(img, left_eye, right_eye, out_size=(1080,1080),
          target_left=(0.35,0.40), target_right=(0.65,0.40)):
    W,H = out_size
    (lx,ly),(rx,ry) = left_eye,right_eye
    tl = np.array([target_left[0]*W, target_left[1]*H]); tr = np.array([target_right[0]*W, target_right[1]*H])
    sv = np.array([rx-lx, ry-ly], float); dv = tr-tl
    scale = np.linalg.norm(dv)/np.linalg.norm(sv)
    ang = math.atan2(dv[1],dv[0]) - math.atan2(sv[1],sv[0])
    c,s = math.cos(ang)*scale, math.sin(ang)*scale
    R = np.array([[c,-s],[s,c]])
    t = (tl+tr)/2 - R@np.array([(lx+rx)/2,(ly+ry)/2])
    Ri = np.linalg.inv(R); ti = -Ri@t          # PIL needs the inverse (dst -> src)
    return img.transform(out_size, Image.AFFINE, (Ri[0,0],Ri[0,1],ti[0],Ri[1,0],Ri[1,1],ti[1]),
                         resample=Image.BICUBIC, fillcolor=(20,20,20))
```
Tips (M): keep the 16-bit TIFF master untouched; align from a copy; log eye coordinates per photo in the manifest so alignment is repeatable.

### T2. Dissolve vs morph vs AI in-between
Dissolve (T3, `xfade`) keeps every pixel real. Mesh morph (`face_morpher`) warps triangles between landmarks and needs frontal faces [28]. Neural in-betweening (FILM) is archived [26]. AI first-last-frame video (Wan FLF2V) fabricates the in-between [19]. Rank by honesty: dissolve, then mesh morph, then AI (label as reconstruction).

### T3. Ken Burns + crossfade with ffmpeg
```bash
FPS=24; DUR=4; FADE=1
# one image = one frame. Do NOT add "-loop 1": zoompan then emits d frames per input frame
inputs=(-i a.png -i b.png -i c.png)
filt=""
for i in 0 1 2; do
  filt+="[$i:v]scale=3840:3840,zoompan=z='1+0.08*on/($FPS*($DUR+$FADE))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$((FPS*(DUR+FADE))):s=1080x1080:fps=$FPS,format=yuv420p[v$i];"
done
filt+="[v0][v1]xfade=transition=fade:duration=$FADE:offset=$DUR[x01];[x01][v2]xfade=transition=fade:duration=$FADE:offset=$((2*DUR))[out]"
ffmpeg -y "${inputs[@]}" -filter_complex "$filt" -map "[out]" -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```
**Trap found [L]:** with `-loop 1 -t 5` the same filter produced 15,192 frames (633 s) because `zoompan` outputs `d` frames per input frame. With single-frame image inputs the result is 13.0 s, 312 frames, 24 fps [65].

### T4. Hold-on-twos jitter
`hold_frames` (2 or 3), `jitter_px`, `jitter_deg`, `seed` from `pasteup` [60]; own implementation [66]: choose a new random offset and rotation only when `frame % hold_frames == 0`, seed a private `random.Random(seed)`, paste a rigid white-bordered "print" onto a plain background. Result: 48 frames, 24 identical pairs, 23 changes between poses, deterministic for a seed; encoded with `ffmpeg -framerate 24 -i f%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p` to 48 frames, 2.0 s [L].
```python
import random
from PIL import Image
def wobble_frames(card, out_dir, n=48, hold=2, jitter_px=3, jitter_deg=0.6, seed=7, size=(1280,720)):
    rnd = random.Random(seed)              # private RNG: same seed -> same wobble
    for f in range(n):
        if f % hold == 0:                  # new pose only every `hold` frames
            dx, dy = rnd.uniform(-jitter_px, jitter_px), rnd.uniform(-jitter_px, jitter_px)
            rot = rnd.uniform(-jitter_deg, jitter_deg)
        bg = Image.new("RGB", size, (92, 70, 52))
        r = card.rotate(rot, resample=Image.BICUBIC, expand=True)   # card = RGBA print with white border
        bg.paste(r, ((size[0]-r.width)//2 + int(dx), (size[1]-r.height)//2 + int(dy)), r)
        bg.save(f"{out_dir}/f{f:04d}.png")  # photo pixels are only moved, never repainted
```

### T5. Replay Mod camera path
Keyframes on a 10-minute real-time timeline; spline by default, `O` for linear, `H` to preview the path, `X` for the keyframe repository, `V` to sync the cursor to the time since the last time keyframe; no backwards time during a path; Ctrl-click Render for High Performance mode [53]. Check `export.log` in `.minecraft` on render crashes [53].

### T6. Real-place scaffold
`cargo run --release --no-default-features -- --output-dir=<world> --bbox="min_lat,min_lng,max_lat,max_lng"` with `--mode geo-terrain|geo-only|terrain-only` [56]. A `--one-world` flag extends one persistent Java world with new areas, and the first run fixes scale and build height [56].

### T7. Credit card for CC BY music
End card: track title, "Kevin MacLeod (incompetech.com)", "Licensed under Creative Commons: By Attribution 4.0", plus the licence link and a note on edits [11][12]. Keep the credit visible, not buried [11].

### T8. Mark provenance per asset
Cross-reference to `ai-imagery.md`: a label ladder L0 to L5 and IPTC `DigitalSourceType` metadata (from that note; not re-verified here).

---

## Pitfalls and ethics

- **Promotional and incentive.** PyImageSearch gives code behind an email sign-up and promotes paid courses [27]; Incompetech sells a no-attribution licence [10]; Wait But Why sells a poster [33]; Replay Mod, Iris and others link Patreon [51][55]. Weigh accordingly. I saw no sponsored thread because I saw no thread.
- **Dates.** Tutorials circulate for years. Examples here: PyImageSearch is from 2017 [27]; Kdenlive's written tutorials are 2011 and 2015 [41]; Blackmagic's free books are for Resolve 20 and its video downloads are labelled DR17 while the product is 21 [36]; MCprep's page shows 2024 material [58]; the Kdenlive Windows troubleshooting page mostly concerns 18.x to 21.x [42].
- **Archived and frozen.** MS Old Photos (2026-10-03) [23], FILM (2025-10-14) [26].
- **Surprise and privacy.** Do not run cloud or telemetry-enabled tools on family material without the maker's say: Gemini API in `pasteup` [60], PostHog in Eagle Animation [61]. Do not use shared family devices or cloud photo libraries (charter).
- **Consent and dignity.** She cannot approve this in advance; the trusted proxy must approve any face animation, any morph of her face, and any use of her voice or likeness in AI tools. Face animation on someone who has died is an additional sensitivity (the Wikipedia page on Deep Nostalgia reports the scale of its use, ~100 million animations, but I read no ethics discussion there [25]).
- **Honesty of AI on memories.** AI in-betweens (Wan FLF2V) create frames that never existed [19]. Label them as reconstructions or do not use them (Principle 4).
- **Voices.** Suno forbids Voice Models of other people and uploading another person's voice [1]. The charter forbids putting words in her mouth. Do not synthesize any real person's voice.
- **Licences.** `face_morpher` MIT [28], Arnis Apache-2.0 [56], Wan Apache-2.0 [18], FILM Apache-2.0 [26], but InsightFace models are non-commercial research only [22] and LivePortrait's licence text was not seen [21]. A private family screening is not commercial, but keep a clean path in case the piece is shared more widely.
- **Reel grammar.** Do not copy beat-synced zooms, whip transitions or trending sounds. Keep the alignment and rhythm discipline.
- **Overreach.** Do not present the (M) lists (editor mistakes, "what makes a build specific") as sourced findings.

---

## Open questions / gaps

**Could not be answered from evidence (needs a follow-up with working search or Reddit access):**
1. Step-by-step creator documentation of viral "my life in N seconds/years" and age-progression edits (alignment tricks, frame rate, music sync, apps vs desktop equivalents).
2. 2025-2026 AI photo-animation threads on X, Reddit and YouTube with real old photos (tools, cost at the time, failure cases, which still work).
3. Parent's 50th, 60th and anniversary projects: what was made, time taken, what the parent said.
4. Minecraft life or memorial builds: how creators make them read as a real place, how they capture and edit (Java vs Bedrock, shaders, Replay Mod vs alternatives).
5. Scrapbook, collage and paper-cutout motion tutorials: steps in Resolve, Kdenlive, Blender (Mint Visual's video steps were not seen).
6. Hobbyist stop-motion with printed photographs, objects and hands.
7. AI-music creator reports on Suno, Udio and alternatives for tributes; Udio's current terms (the page returned only a shell).
8. Common mistakes in family tribute videos according to r/editors and r/VideoEditing.
9. r/DataIsBeautiful life-timeline posts and r/genealogy scanning advice.

**Suggested searches for the follow-up** (exact strings): "my life in years" morph tutorial eyes alignment; "photo a day" align faces ffmpeg; "animate old photos" Wan 2.2 ComfyUI grandparents; "recreated my grandmother's house in Minecraft"; "Minecraft memorial build" Replay Mod; "birthday video for mom" Kdenlive OR Resolve; "paper cutout transition" Kdenlive OR Resolve; "stop motion with printed photos"; "Suno" tribute song license; site:reddit.com/r/editors "tribute video" OR "memorial video" OR "slideshow".

**Verified but shallow or incomplete:**
- Mojang usage guidelines and the Java price (503). Replay Mod frame-rate documentation section is empty [53].
- Fusion's limits in free Resolve [35]; Kdenlive CLI/batch rendering [50]; Windows install of dlib; MediaPipe eye-centre indices and Windows CPU behaviour [29].
- LivePortrait licence and model dependencies [21][22]; MCprep vs current Blender [58]; Chunky and Iris software licence names [55][59]; Flashback "ARR" meaning [54].
- Wan 2.2 rented-GPU price: not checked.
- Maker's GPU: unknown; it decides C9, C14 and the Minecraft shaders.
- Jurisdiction of the event: unknown; it decides whether the US public-performance reading [16] applies.

**Reachability record (2026-10-18):** `www.reddit.com` refused by the fetch tool; `x.com` HTTP 402; `medium.com` 403; `video.stackexchange.com` refused; `youtube.com/watch` redirected to a CAPTCHA (not followed); `learnopencv.com` (face-morph tutorial) and `musopen.org` returned 403, so neither is cited; `udio.com` terms returned a shell; `minecraft.net` usage-guidelines and store pages returned 503 on every attempt; several guessed Kdenlive and Blender subpage URLs returned 404 and were replaced with URLs taken from the docs' own link lists.

---

## Sources

Fetched on 2026-10-18 unless noted. "Page-dated" means the page itself showed a date. "oEmbed" means only title and channel were retrieved from YouTube's endpoint.

**Music and licensing**
1. Suno Terms of Service — https://suno.com/terms — page-dated: revised 2026-08-10, effective 2026-09-03 — Free tier personal/non-commercial; Pro/Premier output assignment; no copyright warranty; voice-model limits; watermark rule.
2. Suno Pricing — https://suno.com/pricing — undated — Free $0 (50 credits/day, no downloads), Pro $8/month (2,500 credits, 20 downloads), Premier $24/month (10,000 credits, 60 downloads).
3. Suno Help: Rights & Ownership category — https://help.suno.com/en/categories/550145-rights-ownership — undated — 17 article titles on rights and ownership.
4. Suno Help: If I subscribe, do I get rights for songs made before subscribing? — https://help.suno.com/en/articles/2425729 — undated — no retroactive commercial licence by default.
5. Suno Help: What rights do I have with the free plan? — https://help.suno.com/en/articles/9601601 — undated ("Edited" label only) — personal, non-commercial, cannot be monetized.
6. Suno Help: How do downloads work? — https://help.suno.com/en/articles/13876865 — undated — trial downloads and plan limits.
7. Udio Terms of Service — https://www.udio.com/terms-of-service — shell only — **UNVERIFIED**.
8. Udio Help Center — https://help.udio.com/en/ — undated — categories only; no ownership articles listed.
9. Incompetech home — https://incompetech.com/ — footer 1997-2026; April 2, 2026 note — links to licences and FAQ.
10. Incompetech Music Licenses — https://incompetech.com/music/royalty-free/licenses/ — undated — free with credit; paid Standard License, no price shown.
11. Incompetech Music FAQ — https://incompetech.com/music/royalty-free/faq.html — footer 2026 — credit wording "Licensed under Creative Commons: By Attribution 4.0"; edits must be disclosed.
12. Creative Commons Attribution 4.0 deed — https://creativecommons.org/licenses/by/4.0/ — undated — attribution, licence link, indicate changes; commercial and adaptation allowed.
13. Pixabay Content License summary — https://pixabay.com/service/license-summary/ — undated — commercial use without attribution; no music-specific terms in the summary.
14. YouTube Audio Library help — https://support.google.com/youtube/answer/3376882 — undated — CC tracks need credit; off-YouTube use not addressed.
15. Free Music Archive — https://freemusicarchive.org/ — footer 2026 — "Free to play, download and share"; no licence detail on the fetched page.
16. 17 U.S.C. section 101 (Cornell LII) — https://www.law.cornell.edu/uscode/text/17/101 — undated — definition of "publicly" (normal circle of a family and its social acquaintances).
17. ACE-Step — https://github.com/ace-step/ACE-Step — page-dated: 2025-05-06, 2025-06-02, v1.5 link 2026-01-28 — Apache-2.0 open music model; ~8 GB VRAM.

**AI motion, restoration and morph tooling**
18. Wan2.2 — https://github.com/Wan-Video/Wan2.2 — page-dated: 2025-07-28 to 2025-11-13 — models, VRAM, Apache-2.0.
19. ComfyUI Wan2.2 tutorial — https://docs.comfy.org/tutorials/video/wan/wan2_2 — undated — 5B and 14B workflows, FLF2V, file names.
20. WanGP (DeepBeepMeep) — https://github.com/deepbeepmeep/Wan2GP — page-dated: v18.17, 15 October 2026 — low-VRAM multi-model UI; Windows scripts.
21. LivePortrait (KwaiVGI) — https://github.com/KwaiVGI/LivePortrait — page-dated: updates to 2025-06-01 — still-portrait animation; Windows installer; misuse note.
22. InsightFace — https://github.com/deepinsight/insightface — page-dated: update 2025-11-24 — code MIT; models non-commercial research only.
23. Bringing Old Photos Back to Life (Microsoft) — https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life — page-dated: archived 2026-10-03 — MIT; research use; run command.
24. GitHub topic: old-photo-restoration — https://github.com/topics/old-photo-restoration — listing — 15.7k-star Microsoft repo and small newer projects (used only as pointers).
25. MyHeritage (Wikipedia; Deep Nostalgia) — https://en.wikipedia.org/wiki/MyHeritage — February 2021 launch; ~100 million animations; D-ID link.
26. FILM: Frame Interpolation for Large Motion — https://github.com/google-research/frame-interpolation — page-dated: archived 2025-10-14 — Apache-2.0; NVIDIA GPU setup.

**Morph, alignment and timeline exemplars**
27. Face Alignment with OpenCV and Python (PyImageSearch) — https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/ — 2017-05-22 — eye-point alignment steps.
28. face_morpher (alyssaq) — https://github.com/alyssaq/face_morpher — undated — MIT; frontal faces only; CLI.
29. MediaPipe Face Landmarker — https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker — page-dated: updated 2026-10-09 — 478 landmarks; Python.
30. GitHub topic: face-alignment — https://github.com/topics/face-alignment — listing — landmark libraries (pointer only).
31. Noah Kalina (Wikipedia) — https://en.wikipedia.org/wiki/Noah_Kalina — undated — Everyday facts.
32. "Noah takes a photo of himself every day for 6 years." (YouTube, oEmbed) — https://www.youtube.com/watch?v=6B26asyGKDo — oEmbed title and channel only; upload date not retrieved.
33. Your Life in Weeks (Wait But Why) — https://waitbutwhy.com/2014/05/life-weeks.html — 2014-05-07 — weeks grid.
34. Feltron — https://feltron.com/ — navigation only — annual-report listing, 2005 to 2014; pointer only.

**Editing, collage and cutout**
35. DaVinci Resolve (Blackmagic) — https://www.blackmagicdesign.com/products/davinciresolve — footer 2026 — v21; free vs Studio; Studio $295.
36. Resolve training — https://www.blackmagicdesign.com/products/davinciresolve/training — undated — free PDFs (Resolve 20) and lessons.
37. Kdenlive documentation home — https://docs.kdenlive.org/en/ — manual 26.08 — section map.
38. Kdenlive Effects and Filters — https://docs.kdenlive.org/en/effects_and_filters.html — manual 26.08 — keyframes, masking.
39. Kdenlive Transform effect — https://docs.kdenlive.org/en/effects_and_filters/video_effects/transform_distort_perspective/transform.html — manual 26.08 — parameters.
40. Kdenlive video tutorials list — https://docs.kdenlive.org/en/getting_started/tutorials/video_tutorials.html — undated — 23 community videos.
41. Kdenlive written tutorials — https://docs.kdenlive.org/en/getting_started/tutorials/written_tutorials.html — undated — three opensource.com articles (2011, 2015), may be out of date.
42. Kdenlive Windows issues — https://docs.kdenlive.org/en/troubleshooting/windows_issues.html — manual 26.08 — mostly 18.x to 21.x fixes.
43. Kdenlive download — https://kdenlive.org/download/ — undated — 26.08.2; Windows installer and standalone.
44. "Kdenlive | Paper Cutout Transition Tutorial" (Mint Visual, YouTube, oEmbed) — https://www.youtube.com/watch?v=Fh1xhOzfjBE — oEmbed title and channel only.
45. "Tutorial: How to do pan and zoom with Kdenlive video editor" (Peter Thomson, YouTube, oEmbed) — https://www.youtube.com/watch?v=B8ZPoWaxQrA — oEmbed title and channel only.
46. Ken Burns effect (Wikipedia) — https://en.wikipedia.org/wiki/Ken_Burns_effect — undated — pan and zoom history and software.
47. Cutout animation (Wikipedia) — https://en.wikipedia.org/wiki/Cutout_animation — undated — history; photographs as cutouts.
48. Stop motion (Wikipedia) — https://en.wikipedia.org/wiki/Stop_motion — undated — pixilation, cutout, object animation definitions.
49. Blender licence — https://www.blender.org/about/license/ — undated — GPL; output is yours.
50. Kdenlive Exporting — https://docs.kdenlive.org/en/exporting.html — manual 26.08 — basic render workflow.

**Minecraft**
51. Replay Mod — https://www.replaymod.com/ — © 2026 — what it is; creators.
52. Replay Mod download — https://www.replaymod.com/download/ — undated — v2.6.27; Fabric 1.14.4 to 26.2; Forge to 1.12.2.
53. Replay Mod documentation — https://www.replaymod.com/docs/ — undated — recording, keyframes, rendering, shaders.
54. Flashback (Modrinth) — https://modrinth.com/mod/flashback — "updated 3 weeks ago" at capture — Fabric; licence "ARR".
55. Iris Shaders — https://irisshaders.dev/ — © 2026 — Fabric and NeoForge; no Forge.
56. Arnis — https://github.com/louis-e/arnis — © 2022-2026 — OSM to Minecraft; Apache-2.0.
57. Mineways — https://www.realtimerendering.com/erich/minecraft/public/mineways/ — page-dated: updated 2026-10-03 — v14.01.
58. MCprep — https://theduckcow.com/dev/blender/mcprep/ — page-dated: 2016 post, v3.6.0 art Aug 2024 — Blender add-on.
59. Chunky documentation — https://chunky-dev.github.io/docs/ — undated — path tracer for Java worlds.

**Stop-motion and paper**
60. pasteup — https://github.com/tmoody1973/pasteup — © 2026; v1.1.0 — halftone paper-collage plug-in; MIT; Gemini key.
61. Eagle Animation — https://github.com/brick-a-brack/eagle-animation — undated — GPL-3.0; telemetry default on.
62. Boats Animator — https://github.com/charlielee/boats-animator — undated — GPLv3; `main` being rewritten.
63. GitHub topic: stop-motion — https://github.com/topics/stop-motion — listing, fetched 2026-10-18 — 55 repos (20 shown).

**Added after review**
67. Blender 5.2 LTS Manual, Grease Pencil introduction URL — https://docs.blender.org/manual/en/latest/grease_pencil/introduction.html — manual version shown: 5.2 LTS — only the version and navigation were retrieved; no Grease Pencil content read.
68. Noah Kalina (official site) — https://noahkalina.com/ — navigation only: Photographs, Projects, Commissions, Hotline, Tears, Info/Contact; no description of Everyday.

**Local tests (sandbox, 2026-10-18)**
64. `align_eyes.py` — scratchpad (not kept in repo) — worst error 1.36 px on three synthetic cases.
65. `kenburns_xfade.sh` — scratchpad (not kept in repo) — 13.0 s, 312 frames, 5.7 s render; the looped-input trap.
66. `jitter_twos.py` — scratchpad (not kept in repo) — 24/24 held pairs, 23/23 changes, deterministic.
