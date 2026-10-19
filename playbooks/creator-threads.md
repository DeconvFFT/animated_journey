# Creator Recipes for the Life Journey

*Playbook for the maker. Track `creator-threads`. Written 2026-10-18 (Sunday) and reconciled 2026-10-19; the LEARN phase has ended (D-30). Deadline 2027-02-27.*

Reconciled with [DECISIONS.md](../DECISIONS.md) (2026-10-18, and again on 2026-10-19 after the her-world merge), the single source of truth. Where a lean below disagrees with a register row, the register wins. D-nn rows are decided by the maker; W-nn rows are working defaults. The game-world tour is archived (D-29), and the film's look comes from her Hindu world (D-28, D-31).

**Read this first.** This playbook is **tool-verified recipe cores plus a capture protocol**. It is not a sweep of creator threads. That sweep did not happen: web search ran out of budget (refused four times on 2026-10-18), and Reddit, X, Medium and YouTube watch pages were blocked. So no creator's thread, Reddit post or watched tutorial shaped it. The recipes come from tool documentation, terms pages and small tests we ran in the sandbox, and each recipe says which kind of evidence it has. The orchestrator chose this scope (roadmap Decision 24, "Exit B"). The register keeps it as W-28: Exit B stands until the orchestrator's own seat proves a read-only call to the maker's PC works. The creator questions that need real threads (Q1 "life in N seconds" edits, Q3 tributes made for a parent and Q8 what editors say about tribute-video mistakes; Q4, the game-world memorial builds, is dropped with D-29) are one build-phase task: the nine searches and ten captures in the research note, less the ones that served Q4. It fires the first week the maker has thread captures saved in `research/creator-threads-captures/`, whose README is the capture protocol. Questions we could not answer are marked TODO(research).

**How to read the tags.** [T] means we read a tool or terms page on 2026-10-18. Its figures are as the page summary reported them, so check before you rely on one. [L] means we tested it ourselves in the sandbox. (M) means it is judgment, not sourced. UNVERIFIED means we could not confirm it. Numbers in brackets, such as [27], point to the Sources section.

## Why this matters for our life journey

Your mother's life is long, and the material is real: printed photos, digital photos, home videos, letters and people who remember. The charter asks us to restore, animate and connect those real things. It does not let us invent them.

Creators have worked out many ways to make still photos feel alive. Several are free and can be scripted. This playbook keeps the ones we could verify, and it says which are only documented.

The biggest lesson is about rhythm, not software. Noah Kalina's *Everyday* works because it shows one face, at a fixed speed of six photos per second, with an original piano score [31]. Our archive will have far fewer usable photos. We estimate 30 to 80 (M), so count your real archive first. The speed and the music have to be chosen on purpose. Copying a popular reel format would make the piece look generic, and the charter rules that out.

The ArtCraft apps have their own research tracks (craft-visual and craft-motion). This playbook does not cover them.

## Core principles

1. **Real memories stay real.** Move, align, crop and restore. Do not repaint faces or add things that were not there. Keep the untouched original. The recipes we verified only move and rotate pixels [L][64][66].
2. **Every device needs a reason.** Before a zoom, a wobble or a morph goes in, write one sentence: why this move, for this person, in this scene. If you cannot write it, cut the move.
3. **Choose one rhythm, then break it on purpose.** Hold each photo for a consistent time, and change the pace only at a turning point. We found no source for how long to hold a photo of an older person. TODO(research): test hold times with three viewers, once the gate in step 38 is passed.
4. **Same pose, years apart, is the strongest device.** Aligning two photos by the eyes keeps the face still while the years change [27][64].
5. **Use the most honest blend that works.** A plain dissolve keeps every pixel real. A mesh morph warps the photo. An AI in-between invents frames that never existed [19]. Start with the dissolve. Use the others only with a visible label and the maker's decision as proxy (D-04). The ranking itself is our researcher's judgment (M).
6. **Use her sound before library sound.** For the premiere cut that is the maker's captures in her empty house (objects, rooms, the sea's surf), then the tune she sang to you, hummed by you in week 1 in two takes and left uncleaned (W-44, W-65); room tone is never a first sound (W-36). No recorded voice of a living person goes in the premiere cut except her own HER-PUBLIC clip (D-05). A relative playing or singing something she loves is the best option we found (M), and it belongs to the April version, recorded in response to the film (D-06). A credited library track comes next, only as a labelled stand-in and only if the sound is hers (O-72). AI music is closed for the premiere (W-79).
7. **Every step needs a free fallback.** Nothing critical may depend on an archived, paid or blocked tool. Microsoft Old Photos and FILM are both archived [23][26].
8. **Dignity and consent come first.** The maker is her proxy and nobody else is (D-03). Hard chapters go through one-key-three-guards (D-04); face work and any use of a voice or likeness follow D-16 and D-05 (charter principle 5). Gather covertly. Keep family material off cloud libraries and off tools that upload it.

## How to do it, step by step

Parts A to E are the main path. It builds one chapter for the vertical slice: one same-pose pair, one simple move, one reconstruction and one music bed. Parts F and G are archived (D-29). Parts H to J are branches. Use a branch only if the format needs it, and only after its gate is passed.

The scripts in Parts B, C and D live in `research/creator-threads-fixtures/`. Either an agent runs them in the cloud session and sends you the output, or you run them on Windows after you install Python 3.14 with the Python install manager, add Pillow and numpy with pip, and run `winget install Gyan.FFmpeg` (confirmed identifier, ffmpeg 9.0.2, gives `ffmpeg`, `ffplay` and `ffprobe` [116]). The route is in research note F2 and has not been run on Windows. The three self-tests also pass on Python 3.14.6, Pillow 13.0.0 and numpy 2.5.4 on Linux [120]. Family photos never go to the cloud session; cloud runs use the synthetic test face only (charter, D-15, W-24).

### Part A: Get ready before you touch a photo

1. **Check the gate.** Ask whether she would want this shown in front of others. If you are unsure, you decide as her proxy, and nobody else does (D-03, O-11). Hard chapters (loss, illness, separation, money, conflict) stay out of the public cut unless they pass one-key-three-guards: a decision sheet, the Fable advisor's written flag, and your two decisions 72 hours apart, with default OUT on any doubt (D-04, charter principle 5). Real photos and stories are gathered only after the pipeline and process are locked: the P-LOCK process lock is Sat 14 Nov 2026 and covert collection starts Sun 15 Nov (D-13).
2. **Keep the master, work on a copy.** Store each original scan or print untouched. Align from a copy. The research note's tip is to keep a 16-bit TIFF master untouched (M).
3. **Start a manifest.** Keep one row per photo: the date and how sure you are, the place, who holds the original, the eye coordinates once measured, the consent status, and the licence for anything not made by the family. Log eye coordinates so every alignment can be repeated (M). The label system for AI-made or restored images is the L0 to L5 ladder in ai-imagery.md (settled, W-40).
4. **Keep it private.** Do not sync family photos to a cloud library, a shared device or a family group chat (charter). Do not run a tool that uploads them. pasteup sends prompts and images to the Gemini image API [60]. Eagle Animation sends error and usage events to PostHog by default, which you can switch off [61].
5. **Restore only if needed.** Restore a copy when a print is badly damaged. Do not build on Microsoft Old Photos. It is archived and marked for academic research use only [23]. TODO(research): pick a current restorer. The research did not verify one.

### Part B: The same-pose dissolve

6. **Pick a same-pose pair.** Look for the same doorway, chair, hat, angle and light. Both eyes should be visible, and the face should be fairly straight to the camera (M). Frontal faces are what face_morpher needs [28].

6a. **If the archive has no same-pose pair for a chapter, build the recent half without recording her.** The charter's gather-after-lock rule protects the archive and the interviews from a pipeline that is not yet safe, and D-17 bars recording her without her knowledge (W-33: the camera never searches for a face). So the recent half comes from the present, by sight, on the maker's own unsynced phone that is never synced to a shared or cloud library: the object or the place where she sits, or her hands in an album-and-hands session after P-LOCK (W-32, W-49; P-LOCK is the Sat 14 Nov 2026 process lock, and covert collection starts Sun 15 Nov, D-13, W-10). A same-pose pair that needs her face waits for the April version, or for her yes after the her-turn conversation (Sun 7 Mar after about 14:00, else Mon 8 Mar; D-06, W-48). Keep these shots out of any cloud library (step 4). Log each recent shot as a bookend in the manifest with the old photo it answers. Check the pairing yourself, as her proxy, before use (D-03).
7. **Mark both eye centres in each photo.** Click them in any image viewer. Or detect them with MediaPipe, which returns 478 landmarks [29]. MediaPipe landmarks 468 (subject's right eye) and 473 (subject's left eye) are the iris centres; tested on CPU on Linux, Windows run UNVERIFIED (note F7 [89][92][93][102]).
8. **Align the pair to one frame.** The method turns each photo so the eyes sit level, scales it so the eyes are the same distance apart, and moves it so the eye midpoint lands on a fixed target [27]. The tested script puts the eyes at 35% and 65% across and 40% down [64]. PyImageSearch's default uses 35% down [27]. Choose one value and use it for the whole set.
9. **Check by flipping.** Flip between the aligned photos. The eyes should not jump. The tested script was about 1.4 px off on synthetic test images. It has not been tried on real faces [L][64].
10. **Dissolve with a crossfade.** Use ffmpeg's xfade filter [65] or a transition in your editor. Hold each portrait long enough to read the face. The right length is a judgment call (M).

### Part C: One simple move (use it sparingly)

11. **Use the scripted move.** The tested recipe scales each still up to 3840 px, pushes in about 8% over the clip, adds a 1-second fade, runs at 24 frames per second and encodes H.264 at quality setting CRF 18 [65]. It uses ffmpeg `zoompan`, so treat it as a proof recipe only: `zoompan` snaps to whole pixels and fails MO8 on a final push, and finals use sub-pixel rendering (W-41). The script is `research/creator-threads-fixtures/kenburns_xfade.py`; the research note's Techniques T3 keeps the original bash [65].
12. **Feed each still once.** Do not loop a single image as the input. In our test, a looped input turned a 5-second setting into a 633-second file, until we fixed it [65].
13. **Push in on a detail.** Move toward the hands or the doorway, not on every photo. Write the "why this move" sentence (principle 2). Pan and zoom is built into most editors [46], so the default version looks generic. A Kdenlive pan-and-zoom tutorial exists. We saw only its title and channel [45].

### Part D: Reconstructions that look made by hand

14. **Make the reconstructed element a transparent PNG.** Draw it or cut it from paper. Keep a white border, like a printed photo.
15. **Add the paper wobble.** Hold each pose for two frames. Shift by up to about 3 px and tilt by up to about 0.6 degrees, using a fixed seed [60][66]. In our test, all 24 held pairs matched, all 23 pose changes differed, and the same seed gave the same result [L][66]. Keep the wobble small. A strong one looks like a cheap effect (M).
16. **Encode at 24 fps and place it on a plain backdrop.** Paper or wood works. Paper cutout is a long tradition, so the look reads as handmade [47][48].
17. **Label it on screen.** Reconstructions must look like reconstructions (principle 4). TODO(research): choose the wording and placement yourself, as proxy. The paper wobble is the exercise look: the film's own reconstruction material is whatever her hands made, set at G1 (W-38), and nothing is ever painted onto Thakorji's clothes or any seva article.

### Part E: Music

18. **Start with your own recording.** Hum the tune she sang to you in week 1, in two takes (closed-mouth and open vowel), uncleaned, into `originals` (W-44, W-65, O-07). Nobody is asked for a recording before the premiere (D-03). A relative playing or singing something she loves is an April-version recording, made in response to the film (D-06); the family owns it, so there is no licence question (M).
19. **If you use a library track, use a credited one, and only as a labelled stand-in (W-44, O-72).** Incompetech's free tier requires credit [10]. Its FAQ gives the credit wording "Licensed under Creative Commons: By Attribution 4.0" [11]. Under CC BY 4.0 you may adapt the track and use it commercially if you give credit, link the licence and say what you changed [12]. A paid licence without credit exists, but its price is not on the page [10]. The FAQ says there is no need to mention cutting and splicing; other changes must be made clear in the credits, saying which parts are yours [11] (checked 2026-10-18).
20. **Keep a licence record.** Save the licence page address and the date you checked it in the manifest.

### Part F: Archived (D-29)

21 to 25. **Archived.** Part F was a game-world camera tour: a recorded walk through a built world, keyframed and rendered. D-29 dropped the game-world look, so the tour, its recorder mods, its shader test and the game-licence reading that went with them are no longer part of the plan, and nothing in this playbook is cited from them. What replaces them in the agent pipeline is the Route A floor-art line (a `stroke-dashoffset` line-draw against `pathLength`, W-72) and the shadow-puppet hinge (`data-pivot` per joint), both in `playbooks/hindu-visual.md` Step 9, with the timed floor-art card of `playbooks/animated.md` Exercise 7. The steps keep the numbers 21 to 25 so that every later step number stays where other files cite it.

### Part G: A real-place start (archived)

26 to 27. **Archived.** Part G generated a game world from map data for a real street, so it went with Part F (D-29). A real place now enters the film as a place drawn in her house's line or as a photograph, and only a place that is hers (`hers_if` and `place_id`, `playbooks/saurashtra-world.md`); places are settings and transitions, never chapters (W-72), and no temple or haveli office is ever asked anything (D-02, D-03).

### Part H: Stop-motion of printed photos (prototype one scene)

28. **Turn telemetry off first.** Eagle Animation is free and open source, but it sends events to PostHog by default. Switch that off in its Settings [61].
29. **Lock the set.** Fix the camera on a stand, and lock focus and light. Use onion skin for small moves. Shoot about 12 frames per second of motion (M) [61].
30. **Keep the prints whole.** Do not crop into faces. Let the hand and the table show. A visible hand is part of the honest look (M).

### Part I: Polish in an editor

31. **Check which editor you have.** Your free editors are not yet confirmed. Kdenlive 26.08.2 is free, runs on Windows 10 and later, and is the editor our notes cover best [43]. DaVinci Resolve 21 is free but limited to 8-bit and up to 60 fps [35].
32. **Use Transform keyframes for hand adjustments.** Kdenlive's Transform effect has position, size, rotation, rotation point and blend modes, and it supports keyframes [38][39]. The docs do not say whether it works on still images. Transform is MLT `qtblend`; it moved a still in a headless render (F8 [96][101]); whether the Kdenlive window accepts it on an image clip is UNVERIFIED, keep Exercise 5.
33. **Watch the paper-cutout video before you copy its method.** Mint Visual's "Kdenlive | Paper Cutout Transition Tutorial" is listed on Kdenlive's own tutorials page [40][44]. We saw only its title and channel. Check it for paid assets. TODO(research): the steps.
34. **Render.** The Kdenlive render dialog is verified [50]. Render dialog > Generate Script, then `melt your_script.mlt` (manual 26.08 [97]). `melt.exe` is in `bin\` of both Kdenlive 26.08.2 Windows packages, next to `kdenlive.exe` and a bundled `ffmpeg.exe` (package contents listed, install not run [119]); confirm it is there after you install.

### Part J: AI photo motion (hold until two decisions are made)

35. **Decide the hardware first.** Wan 2.2's 5B model needs 24 GB of VRAM, according to its README [18]. ComfyUI says the 5B model should fit in 8 GB with offloading [19]. WanGP claims as little as 6 GB for select models [20]. The 14B models need at least 80 GB [18]. Your GPU is unknown. A rented RTX 4090 (24 GB) costs $0.89 per hour on RunPod's pricing page, updated 2026-10-08 [84]. Storage on the same page: Container Disk $0.10/GB/month; Volume Disk $0.10/GB/month running, $0.20 idle; Network Storage $0.07/GB/month under 1 TB; no separate egress charge listed (RunPod pricing, updated 2026-10-08 [84]). A four-hour test afternoon on a 4090 is about $3.56 plus well under $1 of storage (arithmetic, M). Verified on the page 2026-10-18. Billing is per second for Pod compute and for container and volume disk, with no data-transfer fee; network-volume storage is billed hourly. The account needs one hour's credit (about $0.89) to start a Pod, and the default spend limit is $80 per hour [110][111][112]. There are two tiers: Secure Cloud runs in T3/T4 data centres; Community Cloud is peer-to-peer hosts, and RunPod's terms do not rule out their seeing your files. Secure is a facility and reliability tier, and the terms make no confidentiality promise for it either [113][114]. Rule (D-15, W-23): no family photo goes to any rented GPU, in the learn phase or later, and Community Cloud is never used. A rented GPU is for non-family imagery only, on Secure Cloud, on an encrypted volume (volume disk only; container disk and network volumes cannot be encrypted), with the maker's recorded OK and the Pod and the volume terminated afterwards [115].
36. **Try one photo, gently.** Use restrained motion such as light, dust or a curtain, never a face (D-16). Compare it with the still, and label it as animation (principle 4). Do not use a first-and-last-frame method to fill the gap between two real photos. It invents the in-between [19].
37. **Face animation is out.** LivePortrait animates a still from a driving video, and its authors warn about deepfake misuse [21]. D-16 is decided: no AI animation of a real face, so it is not used in the film. Its LICENSE is MIT with a carve-out: InsightFace's models, which it uses for human faces, are non-commercial research only [85][86]; a public screening is not research, so it is out on licence grounds too.

### Part K: Check before you show anyone

38. **Test with strangers to her only.** The two stranger sessions are decided (W-43): S1 with one or two strangers on the slice about Sun 20 Dec (or the cold self-read), and S2 with three to five on the locked cut in week 17, each on a redacted copy under the truthful partial pretext. Test copies must not reveal the surprise. The research note's list of likely problems is a hypothesis, not a finding (M): a cut that runs past the room's attention, music that fights the narration, the same transition on every cut, captions that repeat the picture, and photos held too short to read faces. Editor advice from r/editors and r/VideoEditing was not read; it belongs to the build-phase capture task (Q8). TODO(research).
39. **Write the credits card.** List each source, its licence and the checked date, from the manifest.

## Learn-by-doing exercises

Practise on your own photos, or on a friend's who has agreed. Do not practise on your mother's material. The charter says real photos are gathered only after the pipeline is locked (P-LOCK, Sat 14 Nov; D-13).

If you do only one thing this week, do Exercise 1.

**Exercise 1: Align three pairs of your own photos.**
- **Goal:** learn eye alignment, by eye and by measurement.
- **Steps:** Pick three pairs of same-pose photos of yourself, taken years apart. Mark both eye centres in each photo. Run `python research/creator-threads-fixtures/align_eyes.py --image photo.jpg --left-eye 812,640 --right-eye 1180,652 --out aligned.png` for each photo, with your own eye coordinates. The left eye is the one on the picture's left. Flip between each pair.
- **Time:** about 1 hour (M). The research note estimates about 1 hour for six pairs.
- **Good looks like:** the eyes stay within a few pixels between flips. No hair or chin is cut off. You can say why each pair was chosen.

**Exercise 2: One scripted move with three stills.**
- **Goal:** run the scripted move and check its output.
- **Steps:** Put three photos in one folder. Run `python research/creator-threads-fixtures/kenburns_xfade.py still1.png still2.png still3.png --out move.mp4` with its default settings (4-second stills, 1-second fades, 24 fps). Check the total length and frame count.
- **Time:** 30 to 45 minutes.
- **Good looks like:** three clips with the 4-second setting and 1-second fades give about 13 seconds and 312 frames at 24 fps. That is what our sandbox test gave [65]. The move is slow, and no clip is looped.

**Exercise 3: Make a paper wobble.**
- **Goal:** make a hand-made feel without repainting a photo.
- **Steps:** Make a transparent PNG of a printed photo with a white border. Run `python research/creator-threads-fixtures/jitter_twos.py --card card.png --out-dir frames --hold 2 --jitter-px 3 --jitter-deg 0.6 --seed 7`, which gives a new pose every 2 frames, a shake of about 3 px, a tilt of about 0.6 degrees and seed 7. Then encode at 24 fps with `ffmpeg -framerate 24 -i frames/f%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p wobble.mp4`. Place the clip on paper or wood.
- **Time:** about 30 minutes.
- **Good looks like:** the card moves in small, steady jumps. Running it twice with the same seed gives the same clip. It looks like a hand moved it, not like a glitch (M).

**Exercise 4: A credited music end card.**
- **Goal:** learn the credit rule.
- **Steps:** Pick one Incompetech track. Read the FAQ and the licence page [10][11]. Write an end card with the title, the author, the CC BY 4.0 credit wording and a licence link [12]. If you edit the track, write which parts are yours [11].
- **Time:** about 30 minutes.
- **Good looks like:** the credit can be read on screen without pausing. The licence page address and the date are in the manifest.

**Exercise 5: Move one photo with keyframes.**
- **Goal:** learn position, size and rotation keyframes.
- **Steps:** Install Kdenlive 26.08.2 [43]. Put one photo on the timeline. Set position and size keyframes. Add a small rotation. Export.
- **Time:** 1 to 2 hours (M).
- **Good looks like:** the move is smooth, the edges stay clean, and you can explain the move in one sentence. If the Windows install fails, read the Windows troubleshooting page, which mostly covers versions 18.x to 21.x [42].

**Exercise 6: Archived (D-29).**
- **Replacement:** `playbooks/animated.md` Exercise 7, a timed floor-art line-draw card. The number stays so that Exercises 7 and 8 keep theirs.

**Exercise 7: Three printed photos on stop-motion.**
- **Goal:** learn steady framing and onion skin.
- **Steps:** Turn telemetry off in Eagle Animation [61]. Fix the camera and the lights. Shoot small moves with onion skin, at about 12 frames per second of motion. Export to video.
- **Time:** about a day, including setup (M).
- **Good looks like:** no print is cropped into a face. The hand and the table show. The motion is even.

**Exercise 8: A dry run of the gate.**
- **Goal:** practise the ethics check on one photo from your own archive.
- **Steps:** Write the "why this move" sentence for one move. Write a short decision sheet (D-04): is this a hard chapter, what must not be shown, the advisor's written flag, and your two decisions 72 hours apart.
- **Time:** about 30 minutes.
- **Good looks like:** a reader outside the project can follow the decision on one page.

## Decisions you'll need to make

Each decision gives the options and our current lean. A lean is not a decision. The maker decides, and the maker is also the proxy (D-03). Where the register has decided or defaulted a point, the entry says so and links [DECISIONS.md](../DECISIONS.md).

**1. Format: film, scroll story or a mix.**
- **Options:** a film built from dissolves, moves and music; a scroll story; a mix of both. The explorable game-world tour is dropped (D-29).
- **Our lean:** start with a film. Defaulted in the register (W-30, W-73, [DECISIONS.md](../DECISIONS.md)): Option A, a linear captioned film in chapters plus PH1 on her phone by cable as the companion; the offline scrubber page is a laptop and archive companion. No game-world chapter of any kind (D-29).

**2. Where AI photo motion runs.**
- **Options:** your own GPU (its model is unknown); a rented GPU (an RTX 4090 with 24 GB is $0.89 per hour on RunPod's pricing page, updated 2026-10-08 [84]); skip it. Storage on the same page: Container Disk $0.10/GB/month; Volume Disk $0.10/GB/month running, $0.20 idle; Network Storage $0.07/GB/month under 1 TB; no separate egress charge listed (RunPod pricing, updated 2026-10-08 [84]). A four-hour test afternoon on a 4090 is about $3.56 plus well under $1 of storage (arithmetic, M). Verified on the page 2026-10-18. Billing is per second for Pod compute and for container and volume disk, with no data-transfer fee; network-volume storage is billed hourly. The account needs one hour's credit (about $0.89) to start a Pod, and the default spend limit is $80 per hour [110][111][112]. Secure Cloud runs in T3/T4 data centres; Community Cloud is peer-to-peer hosts, and RunPod's terms do not rule out their seeing your files [113][114].
- **Our lean:** skip it for the vertical slice. Renting a GPU uploads what you send to a third party, so it is decided (D-15, W-23; see [DECISIONS.md](../DECISIONS.md)): non-family imagery only, on Secure Cloud, on an encrypted volume (volume disk only), with the maker's recorded OK and the Pod and the volume terminated afterwards [115]. Community Cloud is never used. No family photo goes to any rented GPU, now or later. Face animation is out (D-16).

**3. Music source.**
- **Options:** a family recording; a credited library track; AI-generated music.
- **Our lean (defaulted, W-44, W-65, W-79, [DECISIONS.md](../DECISIONS.md)):** for the premiere cut, the W-44 spine: your captures in her empty house (objects, rooms, the sea's surf) and the hum you record in week 1 in two takes; silence and room tone, never as a first sound; CC0 or CC BY tracks only as a labelled stand-in and only if the sound is hers (O-72); no licensed song (lean none, O-29); no sung recording of any kind before April (a relative's performance, a sung aarti, kirtan, a garba crowd, a temple loudspeaker or a 6 a.m. radio are April-column items, D-05); no AI music, and never an AI voice for a devotional text in Gujarati, Braj or Sanskrit. A family recording made for the film arrives in the April version (D-06).
- **Why not AI as the final track (M):** Suno's free-plan output is for personal, non-commercial use, and its songs cannot be monetized [5]. The free plan has no monthly downloads [2]. Pro, at $8 a month, allows 20 downloads [2]. Subscribing does not give retroactive commercial rights to earlier free songs [4]. Suno makes no promise that copyright will arise in an output [1]. The terms do not use the phrase public performance. They bar commercial performing of Output for every tier and require a Download before any commercial use. A non-commercial family screening is therefore not restricted by the terms; a ticketed, sponsored or venue-promoted screening would be [1]. The premiere is a mostly public gathering (D-08), not a family screening, and the register says Suno free-plan output may not be shown (W-44), so Suno output is not used in the premiere cut (W-44, W-79). This is a reading of the terms, not legal advice; the jurisdiction is unknown (checked 2026-10-18). A voice model may resemble only your own voice [1].
- **Other AI options:** Udio is not a music source for this film: its terms (Last Revised 2025-11-12) forbid downloading any Output, limit use to personal and non-commercial purposes, and give the company ownership of Output; downloads of audio, video and stems were switched off on 2025-10-29 [104][105][106]. No lawful file can be obtained, so no scratch track either; treat Udio as closed (W-44). Suno's paid-download route is the only hosted AI path, and its terms could change the same way; re-read them before the build phase. ACE-Step is open and runs locally with about 8 GB of VRAM. It states no commercial terms and warns of infringement risk, so treat it as experimental [17].
- **Library options:** Pixabay's summary allows free commercial use without attribution, but says nothing specific about music [13]. YouTube's Audio Library is not a safe default for a screening outside YouTube [14].

**4. Face blend: aligned dissolve, mesh morph or AI in-between.**
- **Our lean:** aligned dissolve for most pairs. Use face_morpher for two or three straight-on pairs at most [28]. Do not build the film on AI in-betweens [19]. FILM is archived [26].

**5. How reconstructions are labelled.**
- **Our lean:** a paper-wobble look plus a visible on-screen label. TODO(research): the wording and placement (your call, as proxy). The label ladder is settled (W-40; L0 to L5 in ai-imagery.md).

**6. Private gathering or public screening. Decided (D-08, [DECISIONS.md](../DECISIONS.md)).**
- **Options:** family only; a venue open to others; an online stream.
- **Decided:** a mostly public gathering, treated as a public screening (D-08). The US definition of "publicly" excludes a "normal circle of a family and its social acquaintances" [16], so a mostly public gathering falls outside that exclusion: clear everything for public screening. This is a reading of a statute, not legal advice. The event's jurisdiction stays unknown until the maker answers TD-7 (O-02).

**7. The timeline device.**
- **Options:** a grid with one cell per year, adapted from the "Your Life in Weeks" idea [33]; or no grid.
- **Our lean:** use a grid of years as an index. Fill each cell with a real object or room. Leave out the finiteness message ("those are your weeks"), which may sit badly at a celebration (M).

**8. Who is the proxy. Decided (D-03, D-04, [DECISIONS.md](../DECISIONS.md)).**
- **Options (closed):** one trusted close relative, or different people for different chapters.
- **Decided:** the maker is the proxy; nobody else. Hard chapters go through one-key-three-guards. The only re-open point is TD-L2c, Sun 3 Jan 2027.

## Pitfalls

- **Promotions and incentives.** PyImageSearch puts its code behind an email sign-up and promotes paid courses [27]. Incompetech sells a licence with no credit requirement [10]. Wait But Why sells a poster [33].
- **Old tutorials.** The PyImageSearch alignment post is from 2017 [27]. Kdenlive's written tutorials are from 2011 and 2015, and may be out of date [41]. Blackmagic's free PDFs are for Resolve 20 [36].
- **Archived or frozen tools.** Microsoft Old Photos was archived on 2026-10-03 [23]. FILM was archived on 2025-10-14 [26]. Boats Animator's main branch is being rewritten, so use a tagged release [62].
- **Privacy surprises.** pasteup uses the Gemini image API [60]. Eagle Animation's telemetry is on by default [61].
- **Face swap and voice.** InsightFace's pretrained models are for non-commercial research only, and its swap models need a licence [22]. Do not make a voice of anyone who has not agreed. Suno forbids voice models of other people [1].
- **Paid phone apps and services.** We found no verified desktop version of the paid "life in 60 seconds" apps, so skip them. MyHeritage's Deep Nostalgia reports about 100 million animations. It is a service, and its pricing is not on the page [25].
- **Fabricated frames.** AI in-betweens create frames that never existed [19].
- **Beat-synced reel grammar.** One listed repo describes "beat-synced stop-motion boomerang clips" [63]. We saw only its description, and it has one star. Skip beat-synced zooms, whip pans and trending sounds.
- **The looping trap.** A looped still turned a 5-second setting into a 633-second file in our test [65].
- **Dates vary.** Sources give *Everyday*'s start date as 2000-01-10 or 2000-01-11 [31]. Treat dates as checked, not certain.
- **Judgment is not evidence.** The list of common tribute-video mistakes is a hypothesis (M). Do not quote them as findings.

## Best references

1. **Noah Kalina, "Noah takes a photo of himself every day for 6 years" (YouTube).** https://www.youtube.com/watch?v=6B26asyGKDo. Watch it for the rhythm and the use of music. The research saw only the title and channel, not the content [32].
2. **PyImageSearch, "Face Alignment with OpenCV and Python" (2017-05-22).** https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/. The two-eye alignment method behind the same-pose dissolve. Expect an email sign-up and course promotions [27].
3. **Kdenlive manual, Rendering.** https://docs.kdenlive.org/en/exporting/render.html. The render dialog, Generate Script and `melt your_script.mlt`, for the cloud or the PC (Part I). The manual has no Windows steps [97].
4. **Kdenlive, Transform effect.** https://docs.kdenlive.org/en/effects_and_filters/video_effects/transform_distort_perspective/transform.html. Position, size, rotation and rotation point, with keyframes [39].
5. **Kdenlive, Effects and Filters.** https://docs.kdenlive.org/en/effects_and_filters.html. Keyframes and masking in one place [38].
6. **Incompetech, Music FAQ.** https://incompetech.com/music/royalty-free/faq.html. The exact credit wording, and the rule for disclosing edits [11].
7. **Creative Commons, Attribution 4.0 deed.** https://creativecommons.org/licenses/by/4.0/. What CC BY means in plain terms. Read it before you use any credited track [12].
8. **Eagle Animation (GitHub).** https://github.com/brick-a-brack/eagle-animation. Free stop-motion for printed photos. Switch telemetry off before you open it with any family material [61].

## Sources

Cited in this playbook. Numbers are kept from the research note. Every URL below is in the research note's source list. Sources [51] to [56], [58], [69], [71] and [121] belonged to the archived Parts F and G (D-29); they are no longer cited here and stay in the research note. Each was fetched or checked on 2026-10-18 unless the entry says otherwise. "Page-dated" means the page itself showed the date. "oEmbed" means YouTube's endpoint gave only the title and channel.

**Music and licensing**
- [1] Suno Terms of Service. https://suno.com/terms. Page-dated: revised 2026-08-10, effective 2026-09-03. Free output is personal and non-commercial. Pro and Premier output assignment, no copyright warranty, voice-model limits.
- [2] Suno Pricing. https://suno.com/pricing. Undated. Free $0 with no downloads; Pro $8 a month with 20 downloads; Premier $24 a month with 60 downloads.
- [4] Suno Help: subscribing and rights for earlier songs. https://help.suno.com/en/articles/2425729. Undated. No retroactive commercial licence by default.
- [5] Suno Help: free plan rights. https://help.suno.com/en/articles/9601601. Undated. Personal and non-commercial; cannot be monetized.
- [104] Udio Terms of Service. https://www.udio.com/terms-of-service. Page header "Last Revised on November 12, 2025". The fetch tool sees only the title; the text was read from the page's embedded script data by a plain GET. Section 1.2 and 6.3: no downloads, personal and non-commercial use only; section 6.1: the company owns Output; section 5.2: no commercial exploitation.
- [105] Udio Help: Changes associated with the Universal Music Group ("UMG") partnership. https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership. Undated. "On October 29, 2025, Udio entered into a partnership with Universal Music Group"; downloading of audio, video and stems has been disabled.
- [106] Udio Help: Udio - Warner Music Group (WMG) partnership. https://help.udio.com/en/articles/12874375-udio-warner-music-group-wmg-partnership. Undated. Udio is still governed by the "transition ToS" of 29 October; sharing only through udio.com links.
- [10] Incompetech Music Licenses. https://incompetech.com/music/royalty-free/licenses/. Undated. Free with credit; a paid no-credit licence, price not shown.
- [11] Incompetech Music FAQ. https://incompetech.com/music/royalty-free/faq.html. Footer dated 2026. Credit wording "Licensed under Creative Commons: By Attribution 4.0"; edits must be disclosed.
- [12] Creative Commons Attribution 4.0 deed. https://creativecommons.org/licenses/by/4.0/. Undated. Adaptation and commercial use allowed, with attribution, a licence link and an indication of changes.
- [13] Pixabay Content License summary. https://pixabay.com/service/license-summary/. Undated. Commercial use without attribution; no music-specific terms in the summary.
- [14] YouTube Audio Library help. https://support.google.com/youtube/answer/3376882. Undated. Creative Commons tracks need credit; use off YouTube not addressed.
- [16] 17 U.S.C. section 101 (Cornell LII). https://www.law.cornell.edu/uscode/text/17/101. Undated. Definition of "publicly".
- [17] ACE-Step. https://github.com/ace-step/ACE-Step. Page-dated 2025-05-06, 2025-06-02, and v1.5 on 2026-01-28. Apache-2.0 code; about 8 GB VRAM; no commercial terms stated; warns of infringement risk.

**AI motion, restoration and morph**
- [18] Wan2.2. https://github.com/Wan-Video/Wan2.2. Page-dated 2025-07-28 to 2025-11-13. Apache-2.0; README gives 24 GB for the 5B model and 80 GB for the 14B models.
- [19] ComfyUI Wan 2.2 tutorial. https://docs.comfy.org/tutorials/video/wan/wan2_2. Undated. The 5B model should fit in 8 GB with offloading; a first-and-last-frame workflow is described.
- [20] WanGP (DeepBeepMeep). https://github.com/deepbeepmeep/Wan2GP. Page-dated v18.17, 15 October 2026. Low-VRAM interface; 6 GB for select models.
- [21] LivePortrait (KwaiVGI). https://github.com/KwaiVGI/LivePortrait. Updates to 2025-06-01. Animates a still from a driving video; Windows installer; authors warn of deepfake misuse.
- [22] InsightFace. https://github.com/deepinsight/insightface. Update 2025-11-24. Code MIT; pretrained models for non-commercial research only.
- [23] Bringing Old Photos Back to Life (Microsoft). https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life. Archived 2026-10-03. MIT; academic research use only.
- [25] MyHeritage (Wikipedia). https://en.wikipedia.org/wiki/MyHeritage. Deep Nostalgia launched February 2021; about 100 million animations.
- [26] FILM: Frame Interpolation for Large Motion. https://github.com/google-research/frame-interpolation. Archived 2025-10-14. Apache-2.0; needs an NVIDIA GPU setup.
- [85] LivePortrait LICENSE (raw file). https://raw.githubusercontent.com/KwaiVGI/LivePortrait/main/LICENSE. MIT, "Copyright (c) 2024 Kuaishou Visual Generation and Interaction Center", plus an InsightFace carve-out: its models are for non-commercial research purposes only.
- [86] LivePortrait src/utils/cropper.py (raw file). https://raw.githubusercontent.com/KwaiVGI/LivePortrait/main/src/utils/cropper.py. The human-face path builds FaceAnalysisDIY(name="buffalo_l") and takes landmark_2d_106, that is, InsightFace models.
- [84] RunPod pricing. https://www.runpod.io/pricing. Page says "Updated October 8, 2026". RTX 4090 24 GB at $0.89 per hour (Secure Cloud, from the page's structured data). Storage prices on the same page (see step 35); no separate egress charge listed.
- [110] RunPod docs, Billing information. https://docs.runpod.io/references/billing-information. Undated. "All compute and storage charges are billed per second, with no fees for data transfer"; at least one hour's credit to start a Pod; $100 minimum prepaid-card deposit; $80 per hour default spend limit.
- [111] RunPod docs, Pod pricing. https://docs.runpod.io/pods/pricing. Undated. Pods billed by the second for compute and storage; network-volume storage billed hourly; container disk $0.10/GB/month running; volume disk $0.10 running and $0.20 stopped; network volume $0.07 under 1 TB; one hour's credit to start; $80 per hour default spend limit.
- [112] RunPod docs, Pods overview. https://docs.runpod.io/pods/overview. Undated. Pods billed by the second with no ingress or egress fees; Secure Cloud in "T3/T4 data centers"; Community Cloud "peer-to-peer".
- [113] RunPod docs, Choose a Pod. https://docs.runpod.io/pods/choose-a-pod. Undated. Secure Cloud "Best for: Production, sensitive data"; Community Cloud "Peer-to-peer providers", reliability "Variable"; "no longer accepting new hosts for Community Cloud".
- [114] RunPod Terms of Service. https://www.runpod.io/legal/terms-of-service. "Last Updated March 24, 2026". RunPod is "only the venue to connect Hosts with consumers"; customers protect their own data; the terms do not say whether a Community Cloud host can see customer content.
- [115] RunPod docs, Storage types. https://docs.runpod.io/pods/storage/types. Undated. Container disk cleared when the Pod stops; volume disk deleted when the Pod is terminated; "Encrypt volume" applies to volume disk only, and container disk and network volumes cannot be encrypted.

**Morph, alignment and timeline**
- [27] Face Alignment with OpenCV and Python (PyImageSearch). https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/. Dated 2017-05-22. Eye-point alignment steps.
- [28] face_morpher (alyssaq). https://github.com/alyssaq/face_morpher. Undated. MIT; frontal faces only; skips images with no face found.
- [29] MediaPipe Face Landmarker. https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker. Page-dated: updated 2026-10-09. 478 landmarks; Python.
- [31] Noah Kalina (Wikipedia). https://en.wikipedia.org/wiki/Noah_Kalina. Undated. Everyday: six photos per second; original piano score.
- [32] "Noah takes a photo of himself every day for 6 years" (YouTube, oEmbed). https://www.youtube.com/watch?v=6B26asyGKDo. Title and channel only.
- [33] Your Life in Weeks (Wait But Why). https://waitbutwhy.com/2014/05/life-weeks.html. Dated 2014-05-07.
- [89] MediaPipe Face Landmarker guide for Python. https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python. Updated 2026-10-09. 478 landmarks; install with python -m pip install mediapipe.
- [92] MediaPipe face_mesh_connections.py (raw file). https://raw.githubusercontent.com/google-ai-edge/mediapipe/master/mediapipe/python/solutions/face_mesh_connections.py. Iris rings 469 to 472 and 474 to 477.
- [93] MediaPipe tasks face_landmarker.py (raw file). https://raw.githubusercontent.com/google-ai-edge/mediapipe/master/mediapipe/tasks/python/vision/face_landmarker.py. The same iris connections in the Tasks API.

**Editing, collage and cutout**
- [35] DaVinci Resolve (Blackmagic Design). https://www.blackmagicdesign.com/products/davinciresolve. Footer dated 2026. Free: 8-bit, up to 60 fps, UHD; Studio $295.
- [36] Resolve training (Blackmagic Design). https://www.blackmagicdesign.com/products/davinciresolve/training. Undated. Free PDFs for Resolve 20.
- [38] Kdenlive, Effects and Filters. https://docs.kdenlive.org/en/effects_and_filters.html. Manual 26.08. Keyframes and masking.
- [39] Kdenlive, Transform effect. https://docs.kdenlive.org/en/effects_and_filters/video_effects/transform_distort_perspective/transform.html. Manual 26.08. Position, size, rotation, rotation point, blend modes.
- [40] Kdenlive video tutorials. https://docs.kdenlive.org/en/getting_started/tutorials/video_tutorials.html. Undated. 23 community videos listed.
- [41] Kdenlive written tutorials. https://docs.kdenlive.org/en/getting_started/tutorials/written_tutorials.html. Undated. Three articles from 2011 and 2015; the page warns they may be out of date.
- [42] Kdenlive Windows issues. https://docs.kdenlive.org/en/troubleshooting/windows_issues.html. Manual 26.08. Mostly fixes for 18.x to 21.x.
- [43] Kdenlive download. https://kdenlive.org/download/. Undated. Version 26.08.2; Windows installer and standalone version.
- [44] "Kdenlive | Paper Cutout Transition Tutorial" (Mint Visual, YouTube, oEmbed). https://www.youtube.com/watch?v=Fh1xhOzfjBE. Title and channel only.
- [45] "Tutorial: How to do pan and zoom with Kdenlive video editor" (Peter Thomson, YouTube, oEmbed). https://www.youtube.com/watch?v=B8ZPoWaxQrA. Title and channel only.
- [46] Ken Burns effect (Wikipedia). https://en.wikipedia.org/wiki/Ken_Burns_effect. Undated. Pan and zoom, history and software.
- [47] Cutout animation (Wikipedia). https://en.wikipedia.org/wiki/Cutout_animation. Undated. Flat materials, including photographs, moved by stop-motion.
- [48] Stop motion (Wikipedia). https://en.wikipedia.org/wiki/Stop_motion. Undated. Pixilation, cutout and object animation.
- [50] Kdenlive, Exporting. https://docs.kdenlive.org/en/exporting.html. Manual 26.08. Basic render workflow.
- [96] Kdenlive effect definition qtblend.xml (raw file). https://raw.githubusercontent.com/KDE/kdenlive/master/data/effects/qtblend.xml. Tag qtblend, display name "Transform", "Position, scale and opacity".
- [97] Kdenlive manual, Rendering. https://docs.kdenlive.org/en/exporting/render.html. Manual 26.08. Generate Script, then melt your_script.mlt; Job Queue; no Windows steps.
- [116] winget-pkgs manifest, Gyan.FFmpeg 9.0.2 (raw file). https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Gyan/FFmpeg/9.0.2/Gyan.FFmpeg.installer.yaml. `PackageIdentifier: Gyan.FFmpeg`; a zip with portable nested files; command aliases `ffmpeg`, `ffplay`, `ffprobe`; ReleaseDate 2026-09-20.

**Stop-motion and paper**
- [63] GitHub topic: stop-motion. https://github.com/topics/stop-motion. Listing, fetched 2026-10-18. Descriptions only.
- [60] pasteup. https://github.com/tmoody1973/pasteup. Copyright 2026; version 1.1.0. MIT; needs a Gemini API key; sends prompts and images to the Gemini image API.
- [61] Eagle Animation. https://github.com/brick-a-brack/eagle-animation. Undated. GPL-3.0; error and usage events to PostHog by default, switchable off in Settings.
- [62] Boats Animator. https://github.com/charlielee/boats-animator. Undated. GPLv3; main branch being rewritten.

**Local tests (sandbox, 2026-10-18; kept in research/creator-threads-fixtures/)**
- [64] research/creator-threads-fixtures/align_eyes.py, committed 2026-10-18. Original run: worst error 1.36 px on three synthetic cases. Same function as research note T1.
- [65] research/creator-threads-fixtures/kenburns_xfade.py, committed 2026-10-18 (Python port of the tested bash). Original run: 13.0 s, 312 frames, 5.7 s render; the looped-input trap. Research note T3.
- [66] research/creator-threads-fixtures/jitter_twos.py, committed 2026-10-18. Original run: 24 of 24 held pairs identical, 23 of 23 pose changes, deterministic for a seed. Research note T4.
- [101] qtblend Transform on a still, rendered with melt 7.22.0 under xvfb-run (sandbox, 2026-10-18; not kept in the repo). 50 frames, 1920 by 1080, H.264; first and last frames differ (mean absolute difference 40.3).
- [102] MediaPipe 1.1.1 Face Landmarker on CPU (sandbox, Python 3.13, Linux, no GPU, 2026-10-18; not kept in the repo). 478 landmarks, 0.027 s per detection; iris ring centres within 0.05 px and 0.17 px of landmarks 468 and 473.
- [119] Kdenlive 26.08.2 Windows packages, contents listed with 7-Zip 23.01, nothing run (sandbox, 2026-10-18; downloaded files deleted afterwards; not kept in the repo). https://download.kde.org/stable/kdenlive/26.08/windows/. `kdenlive-26.08.2.exe` (NSIS installer) and `kdenlive-26.08.2_standalone.exe` both list `bin/melt.exe` (73,219 bytes), `bin/kdenlive.exe`, `bin/kdenlive_render.exe`, `bin/ffmpeg.exe` and `lib/mlt/libmltqt6.dll`.
- [120] research/creator-threads-fixtures/ self-tests on Python 3.14.6 (uv), Pillow 13.0.0, numpy 2.5.4, ffmpeg 6.1.1, Linux, CPU (sandbox, 2026-10-18). Alignment worst error 0.51 px; Ken Burns 312 frames, 13.000 s, PASS; wobble 24 of 24 held pairs, 23 of 23 pose changes, same seed repeats, PASS.

## Changelog

- **2026-10-18, v1.** Written by the Haiku scribe from the creator-threads research note (Sonnet, same date) and the charter. No creator threads, Reddit posts or watched tutorials were read. Gaps are marked TODO(research).
- **Conflicts in the research note, kept visible:** (a) the tested alignment script puts the eyes at 40% down [64], while PyImageSearch's default is 35% [27]; (b) and (c) concerned the game-world tools of the archived Parts F and G and are dropped (D-29).
- **2026-10-18, v2.** Applied the Fable round 1 review: runnable fixtures committed under research/creator-threads-fixtures/, step 6a added with a charter gate, Suno and Incompetech wording checked, RunPod price added, Exercises 1-3 given commands, Sources [64]-[66] repointed.
- **2026-10-18, v3.** Applied the Fable round 2 review and the research note's follow-ups F1 to F8: Minecraft price $29.99 [69] (usage rules not yet read; see v4); MediaPipe eye centres 468/473, CPU tested on Linux only [89][92][93][102]; LivePortrait MIT with InsightFace carve-out [85][86]; Transform and Generate Script/melt [96][97][101]; RunPod storage [84]; step 6a rewritten, with the gather-after-lock reading flagged to the orchestrator as a decision for the maker. Sources [69][85][86][89][92][93][96][97][101][102] added.
- **2026-10-18, v4.** Applied the Fable round 3 review and the research note's round 2 follow-ups G1 to G6: Udio closed [104]-[106]; `melt.exe` in the Windows packages [119]; RunPod billing and the Community-tier rule [110]-[115]; `winget install Gyan.FFmpeg` [116]; Python 3.14.6 fixture run [120]; usage-guideline address [71], with the format track's dated excerpt [121] replacing the old "unread" status; scope set to tool-verified recipe cores plus a capture protocol (Exit B); step 6a now carries the orchestrator's recorded reading.
- **2026-10-18, v4.1.** Research note main body and fixtures README brought level with G1-G6 and Exit B (advisor round 4 nudges 1-3); skill step 4 now names the captures folder as data.
- **2026-10-18, v5.** Reconciled with DECISIONS.md (2026-10-18): proxy is the maker and Decision 8 closed (D-03, D-04); gathering dated from the L1 lock and Sun 15 Nov (D-13); mostly public gathering decided (Decision 6, D-08); music default is the hum and room sound with no relative's recording before the April version (W-44, D-05, D-06); Suno and Udio restated (W-44); rented GPU and cloud rules per D-15, W-23, W-24; LivePortrait and all face animation out (D-16); Minecraft footage closed for the public cut (D-23, W-30); strangers sessions S1 and S2 (W-43); `zoompan` recipe marked proof-grade (W-41); Exit B kept as W-28.
- **2026-10-19, v6.** Reconciled with DECISIONS.md after the her-world merge (2026-10-19): Parts F and G and Exercise 6 archived with their sources, and Decision 1 restated (D-29); the companion is PH1 by cable with the scrubber page a laptop and archive companion (W-30, W-73); the music spine follows W-44, W-65 and W-79 (two hum takes, no sung recording before April, no AI music, no AI devotional voice); step 6a no longer suggests casual photographs of her (D-17, W-33) and builds the recent half by sight or in an album-and-hands session; S1 is one or two strangers (W-43); P-LOCK replaces the old process-lock spelling; a note that the film's reconstruction material is her own hands' (W-38).
