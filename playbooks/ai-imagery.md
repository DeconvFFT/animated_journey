# AI Imagery and Motion from Real Photos

*For the maker. Track `ai-imagery`. Built from the research note at `research/ai-imagery.md` (sources read 2026-10-18). Deadline: Saturday 2027-02-27.*

**How to read this.** Numbers in square brackets, such as [2], point to the Sources list at the end. They match the research note. **TODO(research)** marks a gap we have not closed. Time estimates are planning guesses unless a source gives them. Some sources were seen only as search snippets; the Sources list says so.

## Why this matters for our life journey

Your mother's real photos are the strongest material this project has. The charter's fourth principle says AI may restore, restyle, animate and connect real photos. It may not invent events, create fake people, or put words in anyone's mouth. This playbook shows how we keep that promise.

The main risk is that these tools make things look finished. Almost every tool that cleans, enlarges, colours or animates a photo also invents something: texture, a feature, a colour, or a frame. Some of those inventions will look like memory and are not.

Three facts shape the plan.

- **Nobody has tested these tools on the kind of photo we have.** The research found clean, modern demo portraits. It found no tests on faded, low-resolution or black-and-white family prints. So in week 1 we run a five-photo bake-off, judged by relatives who knew her.
- **Most of the work is hands-on.** The research note estimates about 40 to 80 human hours for 300 photos, mostly scanning and hand clean-up, not computer time. The note's summary and its table differ slightly, and this is an estimate, not a measurement.
- **We start small.** One chapter, a 30-photo vertical slice, comes before the rest of the archive (charter principle 6).

## Core principles

1. **If it looks like a photograph, it is a photograph, possibly restored. Anything invented is drawn.** The research note proposes this as a house rule. It needs your approval before we rely on it.
2. **Keep the original untouched.** Every change is a labelled copy. The master scan never changes [1][2].
3. **Fix the photo without AI first.** Levels, colour cast, dust and cropping come first. Escalate only if the photo is still unusable.
4. **Restoration is generation.** Upscalers, face restorers, colourisers and frame makers all invent something. Find out what each tool invents, and write it down.
5. **Judge likeness with people who knew her.** A sharpness score does not tell you whether the face is still her. Ask a relative: "Does this look like your mother at that age?" (charter principle 5).
6. **Morph only between real photos.** A classic morph or a dissolve adds no new faces. A tool that generates in-between frames is labelled, and it is never shown as a record.
7. **Leave the faces of people who have died alone**, unless the family has said yes first. Motion in the environment, such as light, leaves or parallax, is the safe default.
8. **Small first, then scale.** One photo, then the 30-photo slice, then the rest.

## How to do it, step by step

Each step names the research recipe it comes from (R1 to R6 in the note). Commands were tested on Linux only. Windows set-up is not yet researched (see Pitfalls). Check each command's own help text before you rely on its flags.

### Step 0: Set up the folders and the records (R1)

Create four folders: `01_masters`, `02_work`, `03_exports` and `04_reconstructions`. Put them on a drive or account that no one in the family will browse during the surprise. Keep one checksum file for the masters.

Give every scan an ID such as `LJ-B03-0042-F`. B03 is the box, 0042 the sequence number, and F the front (use B for the back). A rescan adds `-R2`. Put the date in the record, not in the file name, because many photos are undated. This departs on purpose from the Library of Congress's date-first names [1].

Keep two plain CSV files:

- `manifest.csv`, one row per scan. Columns: id, box, medium, scan_date, device, ppi, bit_depth, profile, date_est, date_confidence, people, place, caption_source, consent_note, sha256, notes.
- `steps.csv`, one row per change. Columns: derivative_id, parent_id, step_no, tool, version, settings, seed, invents (none, texture, colour, frames or faces), label_level, reviewer, approved.

The National Archives asks for who, what, where and when [2]. The manifest does that job.

### Step 1: Clean the print and the glass

Clean dust off the originals and the scanner glass first [1]. Do not peel photos out of sticky album pages. Photograph the page in place and split the pictures later. Keep the physical originals [2]. If relatives lend you prints, return each one exactly as it came.

### Step 2: Scan by medium

| What you have | How to capture it | Target | Save as |
|---|---|---|---|
| Loose prints up to 5x7 | Flatbed at 600 ppi [1]; 2 to 4 prints per pass, with a gap between them | 600 ppi | 16-bit TIFF |
| Wallet and 3x3 prints | Flatbed | 1200 ppi (judgment) | TIFF |
| Sticky or magnetic album pages, curled prints | Phone or camera on a stand, filling the frame | 12 MP or more (judgment) | RAW plus JPEG |
| 35 mm slides and negatives | Camera with a 1:1 macro lens on a copy stand [5], or a film flatbed with holders [9][10] | 3200 to 4000 ppi (judgment; not in any source read) | 16-bit TIFF or RAW |
| 120 medium format | Flatbed with a holder | 2400 ppi (judgment) | TIFF |
| Letters and documents | Flatbed | 300 ppi; 600 for handwriting (judgment) | TIFF or PDF/A |
| VHS, Hi8, MiniDV, 8 mm film | Not researched | n/a | TODO(research): home video capture and 8 mm lab options |

**Flatbed settings.** Use 600 ppi, colour, 16-bit. Turn off the scanner's auto-enhance and restore-fading options, so the master stays raw. Scan the back of any print that has writing on it.

**Phone settings.** Keep the phone parallel to the print, on a stand or a stack of books. Use a level app. Put two soft lights at about 45 degrees, or use window light, out of the glare. Lock focus, exposure and white balance. Do not use flash. Shoot RAW if the phone allows it. For glossy prints, use the four-dot capture in Google PhotoScan to cancel glare [6]. PhotoScan is free but "frozen in time," and its last Android update is listed as 2023-07-24 (search snippet only) [6][7]. For album pages, Photomyne scans several prints at once [14]. It costs $59.99 per year after a 3-day trial, and its AI restoration costs extra credits [14].

**Film settings.** Use a camera with a 1:1 macro lens, a copy stand rather than a tripod, a cable release, about f/8, the lowest ISO, and masked film holders [5]. For colour negatives, darktable's `negadoctor` module needs part of the unexposed film border in the scan. Sample the film base colour first, use a linear working profile, and leave out the filmic and base-curve modules [13]. Negative Lab Pro runs inside Lightroom Classic, and its page shows no price [12].

**Buying a scanner.** Decide this before you spend money. The Epson V600 is listed as discontinued [9]. The Epson V850 Pro is listed at $1,999, and its cart state was unclear on the page [10]. Both Epson pages list only old operating systems [9][10]. VueScan (version 9.8.59, dated 2026-09-26) supports more than 8,000 scanners and offers Infrared Clean and Restore Fading [11]. A reviewer says that scanning above the optical limit gives "fatter pixels" (search snippet; page not read) [8]. Infrared cleaning is generally ineffective on black-and-white silver film (judgment, not verified here).

### Step 3: Check each scan and make checksums

Check each scan at 100% zoom. Look for cut-off corners, blur and glare the scan cannot remove. Then write checksums, so you can later prove a master has not changed:

`sha256sum 01_masters/*.tif > checksums.txt` (from R1)

Back up 3-2-1: three copies, on two kinds of media, with one copy off-site [2].

### Step 4: Make the cleaned copy (L1)

Work on a copy, never on the master. Crop and straighten. Fix the colour cast one channel at a time, with levels and curves. Remove remaining dust with the healing brush in GIMP or Krita. Save it with the suffix `__L1`. There is no AI in this step.

Faded 1970s to 90s colour prints usually have a magenta or yellow cast and low contrast. That is a levels problem, so fix it per channel before any AI (judgment; no tested AI result exists for these prints). If you also use the scanner's own "restore fading" output, keep it as a separate file, because it changes colours [11].

### Step 5: Decide whether the photo needs help

Count the pixels before you upscale. A 4x6 print scanned at 600 ppi is 3600 by 2400 pixels. That is already enough for a 1080p timeline with a small push-in, and close to 4K. Do not upscale it. Upscale only wallet prints, 1990s digital camera files and video frames.

### Step 6: Restore only what needs it (L2)

Work through the tools in this order.

1. **Non-AI fixes** (Step 4).
2. **Plain upscale, if needed.** Real-ESRGAN is free, licensed BSD-3, and has portable builds for Intel, AMD and Nvidia graphics [18]. The note's example is `realesrgan-ncnn-vulkan -i in.png -o out.png -n realesr-general-x4v3 -s 2`. Check the flags with `-h` first.
3. **Face restoration, only if your bake-off says it helps.** CodeFormer has a fidelity dial, `w`, from 0 to 1. Higher is more faithful [15]. Try 0.7 to 1.0, then blend the result 40 to 60 percent back over the plain upscale, using a layer mask (practice from the note).
4. **Heavy damage only.** SeedVR2 [24] or SUPIR [21][22]. SUPIR is non-commercial [21]. SeedVR warns that it "can over-generate detail" on lightly degraded input [23].

**Warnings about face tools.**

- GFPGAN v1.3 "may slightly change identity" [17].
- Face super-resolution can make a different person. PULSE says it "makes imaginary faces of people who do not exist" [30].
- Sources disagree about which face tool keeps likeness best. The two comparisons we saw are search snippets only [19][20]. The only real test is your own photos at 100% zoom.
- Do not restore faces narrower than about 64 px. This is the note's rule of thumb (judgment).
- Reject any result with new teeth, new eyelids or a changed jaw.

**Colour, for black-and-white prints.** Treat colourising as costume design. DDColor [28] and DeOldify [29] guess every colour. DeOldify is known for "orange skin and overly red lips" [29]. Check clothes, rooms and cars against family memory or other colour photos. Keep skin tones muted. Caption the result "colours estimated."

**Label and log.** This step is L2. If a generative model repaired content, the IPTC value is `compositeWithTrainedAlgorithmicMedia` [89]. Log each tool, version, setting, seed and what it invents in `steps.csv`.

### Step 7: Connect two real photos (L4a or L4c)

**Classic morph (no invented frames, L4a).** Align the eyes first. Mark 10 to 20 landmarks on each photo: eyes, brows, nose, mouth, jaw, hairline and shoulders. Build Delaunay triangles. For each frame, warp both photos toward the in-between shape and cross-dissolve them, using 24 to 48 frames with ease in and out [65]. LearnOpenCV's FaceMorph is a reference example in Python and C++. Its folder shows code and landmark files only, so check its licence before reuse (not shown on the page) [65].

**Dissolve (no invented frames).** For a quick baseline, `convert a.png b.png -morph 14 frames/m_%02d.png` makes a morph sequence, and ffmpeg can assemble it. An `xfade` dissolve in ffmpeg also works. The research team confirmed these commands run in a Linux sandbox. They did not judge the results on real faces [102].

**Best design.** Chain morphs through real intermediate photos, such as ages 6, 12 and 18. Each segment then joins two real images. A paper-turn or block-build transition says "time passed" without implying that a face existed.

**Generated in-between (L4c, use sparingly).** Tools such as Wan2.1 FLF2V [67] or Veo 3.1 with `lastFrame` [82] generate the whole video between two images. They invent intermediate faces and motion. Inspect the middle frames. If a face matches neither photo, it was invented. Use this only inside a labelled reconstruction, and never present it as a record of how she looked.

### Step 8: Add motion to one still (L4a, L4b)

**Parallax (L4a).** A still becomes a slow camera move, as if the camera were drifting past layers.

1. **Cut out the subject.** `rembg i -m u2net in.png fg.png` [55]. Use `-a`, `-vm` and `-dc` for hair edges. Never use the cloud back-ends, which "send images to their servers" [55].
2. **Make a depth map.** Depth Anything V2 Small is Apache-2.0 and falls back to CPU [58]. Blur or flatten the depth across faces, because depth maps bulge faces (judgment).
3. **Render.** Choose one: DepthFlow [60] (AGPL-3.0, GPU implied, its CLI docs were not read), a displaced plane in Blender (judgment), or layered cut-outs in Kdenlive or DaVinci Resolve (judgment).
4. **Keep the move small.** Orbit 2 to 3 degrees and push in 3 to 8 percent. Fill any gaps with cloned background, which stays L1. If you use generative fill, the clip becomes L4b and needs an "invents" note.

**Paper theatre (no GPU).** Make the layers physical. Use 3 to 5 cut-out layers with soft shadows, and move them with small transforms. The gaps show as honest holes. This needs no GPU and suits a papercraft look (judgment; a test idea for the vertical slice).

**Pure 2D push-in (sandbox-tested).** This 4-second move comes from the note [102]:

`ffmpeg -loop 1 -i in.png -vf "zoompan=z='min(zoom+0.0007,1.08)':d=96:s=960x720:fps=24,format=yuv420p" -t 4 kb.mp4`

**Generated image-to-video (L4b).** Use only with these rules.

- The first frame is always the restored photo. Never generate from text alone.
- Describe motion only. Do not re-describe the face.
- Use restraint words such as "very subtle," "slow," "locked-off camera," "no scene change" and "no cut." These phrases are the research note's own synthesis from model documentation. No creator-tested prompts were reachable (untested).
- Prefer environment motion, such as leaves, curtains, dust in light, or water, over faces and hands.
- Keep clips to 3 to 5 seconds. Use a fixed seed and 3 to 4 takes. Keep the take with the least change.
- Compare the first and last frames with a face-similarity script, and reject a take that drifts. This approach is unverified (TODO(research): choose and test a tool).
- Never ask for speech, lip movement or sound.

**Local options (need a graphics card).** Wan2.2 TI2V-5B: ComfyUI says it fits 8 GB with offloading [70], while the README says 24 GB [69]. FramePack needs 6 GB, and runs only on RTX 30, 40 and 50 series cards [72]. WanGP runs select models on 6 GB and was updated 2026-10-15 [77]. LTX-2 needs 32 GB or more [75].

**Cloud options (privacy rules first; see Decision 6).** A 5-second Veo 3.1 clip costs $0.25 on Lite, $0.50 on Fast and $2.00 on Standard, at 720p with audio [51]. Kling 2.5 Turbo Pro via fal is about $0.35 for 5 seconds [52]. Luma Ray3.2 is about $0.30 at 720p on its Plus plan [81]. Whether Kling, Runway and Luma support first-and-last-frame generation is unconfirmed (TODO(research)). Runway's pricing page is internally inconsistent [80].

**Faces of people who have died.** No face or expression animation (principle 7 and Decision 4). Parallax or environment motion only, and ask the family first. MyHeritage's Deep Nostalgia made nearly 100 million animations [101]. The research did not read any reaction to animating the dead (TODO(research)).

### Step 9: Stylise in the house look (L3)

Pick one look for the whole chapter, and write a two-line style bible: palette, line weight, proportions. Then choose a route (labels follow recipe R4).

- **Route A, hand-made (default).** For each age band (child, teen, young adult, adult, older), pick three to five real photos. List identity attributes: hair shape and colour, glasses, beard, scars, posture, signature clothes, and height relative to others. Build a character sheet in your chosen look: voxel, pixel or clay. MagicaVoxel and Blockbench are believed to be free, but this is unverified [notes]. Take the palette from the photo. For block-palette backgrounds, MapartCraft is a free browser tool under GPL-3.0 [54].
- **Route B, AI edit on the real photo.** Use an edit model that starts from your photo, such as FLUX.1 Kontext dev [33][34] (non-commercial, gated), Qwen-Image-Edit-2511 (Apache-2.0) [36], or FLUX.2 klein 4B (about 8 GB) [38]. Keep the input near 1 megapixel [37]. In the prompt, name the subject specifically and add "while maintaining the same facial features, hairstyle, and expression" [34]. Change one thing per step. Keep one seed, one LoRA strength and one prompt template per chapter. Choose the result by line-up.
- **Route C, identity adapters: avoid for real people.** InstantID [40], PuLID-FLUX [41] and InfiniteYou [42] generate a new picture of the person from a prompt. The pose, clothes and scene are then invented. That makes it a reconstruction (L5), not a restyle. Use it only if a new angle is truly needed, and label it.
- **Route D, style LoRA on your own art.** Train a style LoRA on 10 to 30 of your own hand-made frames, using fluxgym (12 GB) [47] or ai-toolkit [46]. A person LoRA is not the default. It is only conditionally acceptable, with consent, local training, deletion afterwards and labels (research note, Q4c).

The Kontext style LoRAs, such as Clay Toy, Origami and Paper Cutting, have no stated licence [45]. Check it before use.

**Line-up test.** Show five stylised faces to relatives who knew her. Ask who is who, and at what age. Adjust the attributes, not the faces. The pass mark is set during the vertical slice (TODO(research)).

### Step 10: Label what you made

Every derivative gets a level. The ladder below is the research note's proposal (Q8).

| Level | Meaning | Example steps | IPTC value (in XMP) | On screen |
|---|---|---|---|---|
| L0 Scan | Unaltered digitisation | Flatbed or camera scan | `print`, `negativeFilm` or `positiveFilm` | Plain photo frame |
| L1 Cleaned | Human, non-generative fixes | Crop, deskew, levels, healing brush | `humanEdits` | Plain photo frame |
| L2 Enhanced | Algorithmic restoration that invents texture or colour | Upscale, face restore, colourise, diffusion repair | `algorithmicallyEnhanced`; use `compositeWithTrainedAlgorithmicMedia` if a generative model repaired content | Small "R" tag; colourised shots add "colours estimated" |
| L3 Restyled | Real photo redrawn in the house look | Edit model with style LoRA; hand-built character from the photo | `compositeWithTrainedAlgorithmicMedia` (AI) or `humanEdits` / `composite` (hand) | Obviously stylised |
| L4 Animated | Motion added to a real photo | 4a parallax or classic morph (no generated frames); 4b image-to-video; 4c generated in-between | 4a `humanEdits` or `algorithmicallyEnhanced`; 4b and 4c `compositeWithTrainedAlgorithmicMedia` | Tag on the clip: "moved", "frames invented" |
| L5 Reconstruction | Scene never photographed, built from testimony | Stylised scene in the house look | `trainedAlgorithmicMedia` (AI) | Always stylised; caption "Reconstructed from [name]'s memory, 2026" |

The IPTC values come from the Digital Source Type vocabulary [89]. The IPTC user guide says to write the URI, not the label, and to store it in XMP only [90].

Carry the label in four places: the file-name suffix (`__L2`), `steps.csv`, the embedded XMP, and the end-credit cue sheet [96]. The research note suggests the Archival Producers Alliance cue-sheet idea [95][96]. For how to disclose, Partnership on AI separates direct disclosure (labels on screen) from indirect disclosure (metadata, C2PA) [94].

**Metadata command (UNVERIFIED).** The research team did not run ExifTool, because it was not installed in the sandbox. The note's example is:

`exiftool -XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/print LJ-B03-0042-F.tif`

Test it on a copy first. TODO(research): confirm the tag syntax on Windows, and check what survives in MP4 files. Video containers may drop IPTC fields (judgment, unverified). So the manifest and the credits are the real record.

C2PA (Content Credentials) is an open standard [91][92]. Signing needs certificates, and the research did not cover signing for a private project (TODO(research)). Google's image and video outputs carry SynthID watermarks [50][82].

### Step 11: Review before anything is shown

- Flick between the original and the result at 100%, both ways.
- Ask one relative who knew her: "Does this look like her at that age?" Record the answer in the manifest.
- Check the label, the manifest row and the `steps.csv` entry.
- Check that the end credits name every AI tool used.
- Send anything sensitive, such as loss, illness, separation, money or conflict, to the trusted proxy first (charter principle 5).

## Decisions you'll need to make

Each decision lists the options and our current lean. A lean marked "(from the note)" is one the research note states. A lean marked "(scribe's reading, confirm)" is one we derived from the note and the charter, and it needs your confirmation.

**1. Scanner: borrow, buy, or use a phone.**

- *Borrow a flatbed* from a library, a relative or a makerspace. Best for a large batch of prints at 600 ppi (decision table in the note).
- *Buy.* The Epson V850 Pro is $1,999 [10]. The V600 is discontinued [9]. VueScan can drive some scanners whose Epson drivers no longer work [11].
- *Use a phone.* Fine for fewer than 400 prints, with PhotoScan [6] (decision table in the note). Photomyne is the choice for album pages [14].
- **Lean (from the note):** borrow a flatbed for the big batch, and use a phone on a stand for album pages and small batches. (Scribe's reading, confirm:) do not buy anything before the bake-off.

**2. Graphics card (GPU) tier.** The charter does not say which graphics card the Windows PC has.

- *No GPU.* CPU tools, hand work, parallax, morph and grading all work. Use a cloud step only where Decision 6 allows.
- *8 to 12 GB Nvidia.* Real-ESRGAN, CodeFormer, smaller SeedVR2 builds, FLUX.2 klein 4B, FramePack and WanGP.
- *16 GB or more.* Adds Qwen-Image-Edit-2511 and PuLID-FLUX. Some big-model VRAM figures are not stated in any source (see gaps).
- *Rent a GPU.* RunPod lists an RTX 4090 at $0.34 per hour (community) or $0.89 (secure), updated 2026-10-08 [83]. A rented machine is a third-party service, so it falls under Decision 6.
- **Lean (from the note):** start on the no-GPU path. Then check your graphics card and decide.

**3. Private gift, or a public or ticketed showing.**

- *Private gift.* Non-commercial weights are fine. Examples: SUPIR [21], FLUX.1 Kontext dev [33], InfiniteYou's model [42], and Depth Anything V2 Base or Large [58].
- *Public or ticketed.* Check every non-commercial weight and every copyleft tool (AGPL: Upscayl, DepthFlow, Video2X; GPL-3.0: ComfyUI, chaiNNer, Krita AI Diffusion) before you start. The note says these are fine for a private gift and need reassessing for a ticketed event.
- **Lean (scribe's reading, confirm):** plan for a private gift. Where two tools do the same job, choose the one with a commercial-friendly licence, so a later showing stays possible. The occasion and venue are still open in the charter.

**4. Animating people who have died.**

- *Option A: no motion of faces or expressions.* Environment motion and parallax only, and only after the family says yes.
- *Option B: face or expression motion, with the family's explicit yes.* The note advises against it. Its research did not cover this case (TODO(research)).
- *Option C: stills only.* No motion at all for them.
- **Lean (from the note and charter principle 5):** Option A by default. Ask the family before any motion of them. The note's two lines read differently, one saying "no expression animation" and the other "without the family's say." We read them together as: never by default, and only with the family's yes.

**5. How far to label.**

- *Option A: file names only.*
- *Option B: the full six-level ladder (L0 to L5)* in file names, the manifest, the XMP metadata and the credits.
- **Lean (from the note):** Option B. The ladder is the research team's proposal, so you may simplify it for the first chapter if you tell the orchestrator.

**6. Where processing happens (privacy).**

- *Option A: local only.* Nothing leaves your machine. This is the default.
- *Option B: a paid tier whose terms say no training, for cleared photos only.* The Gemini API paid tier does not use prompts and files to improve products [85]. Veo results are stored for 2 days [82], so download them at once.
- *Option C: consumer apps, or any service whose terms the research could not read.* Never.
- **Lean (from the charter and the note):** Option A. The charter says nothing personal goes to a third-party service without your explicit say. That includes a rented GPU. So any cloud step needs your yes first.

**7. Face restoration.**

- *None.*
- *CodeFormer at high fidelity, with blend-back* [15].
- *An edit model on the real photo* [33][36].
- **Lean (from the note):** none by default. Run the bake-off, then choose per photo type. Non-AI fixes come first.

**8. Stylisation route.**

- *Route A, hand-made* (no GPU, likeness built in by design).
- *Route B, AI edit on the photo.*
- **Lean (from the note):** Route A for the first chapter. Use Route B only if it passes the line-up test.

**9. Motion between two photos.**

- *Classic morph or dissolve* (no invented frames).
- *Generated in-between* (invents frames).
- **Lean (from the note):** classic morph and dissolve. Generated in-betweens only when labelled and never as a record.

## Learn-by-doing exercises

Each exercise gives a goal, steps, a time estimate, and what good looks like. The time estimates are planning guesses.

### Exercise 1: Set up the archive and scan five prints

**Goal.** A master, a cleaned copy and a manifest row for every scan.

**Steps.**
1. Create the four folders from Step 0.
2. Clean the scanner glass. Scan five prints at 600 ppi, colour, 16-bit.
3. Scan the back of any print with writing on it.
4. Name the files with the LJ pattern.
5. Fill in five rows of `manifest.csv`.
6. Run `sha256sum` and save `checksums.txt`.
7. Make an L1 copy of one print.

**Time.** About 2 hours (estimate).

**What good looks like.** Five TIFFs that open at 100% with no glass dust. Names that follow the pattern. Five manifest rows with no blanks in id, medium, ppi or scan_date. A checksum file. The L1 copy has the same content as the master, only cleaner.

### Exercise 2: Fix a faded print without AI

**Goal.** Remove a colour cast using levels and curves alone.

**Steps.** Open the 16-bit master in GIMP, Krita or darktable. Adjust each channel so the whites look neutral. Add contrast with a gentle curve. Flick between the original and the result. Save as L1.

**Time.** 1 to 2 hours (estimate).

**What good looks like.** Skin looks like skin, not orange or grey. Nothing new appears in the picture. A relative recognises the print as the same photo, only cleaner.

### Exercise 3: Five-photo bake-off (week 1)

**Goal.** Find out whether any tool helps on the kinds of photo we really have.

**Steps.**
1. Pick five photos: a faded colour print, a small black-and-white print, a soft group snapshot with small faces, a torn print, and a 1990s low-resolution digital file [research note, open question 1].
2. For each photo, make four versions: (a) the L1 fix only; (b) Real-ESRGAN at 2x [18]; (c) CodeFormer at `w` 0.7, 0.8 and 1.0, blended 50% back [15]; (d) one edit model run locally, if your graphics card allows. If not, skip it and say so.
3. Look at each version at 100%. Note what it invents: teeth, eyelids, jaw, hair, background.
4. Show the versions, unlabelled, to relatives who knew her. Record who they recognise, and at what age.

**Time.** 1 to 2 days, spread across the week (estimate).

**What good looks like.** A table with one row per photo and tool. Columns: "what it invents," "does it look like her," and a verdict. A chosen route for each photo type. Keep the photos on your machine. Show relatives only the people who are in on the surprise, because showing family photos is story gathering under the charter's covert rules.

### Exercise 4: The face dial

**Goal.** Learn what the fidelity setting and the blend-back actually do.

**Steps.** Pick one face at least 64 px wide. Run CodeFormer at `w` 0.5, 0.7 and 0.9. Check `--help` for the flag names. Blend each result over the plain upscale at 40%, 50% and 60%, using a layer mask. Compare at 100%.

**Time.** 1 to 2 hours (estimate). The note's Q2 table says a GPU is recommended for CodeFormer, and CPU use is unconfirmed.

**What good looks like.** You can find a setting where the skin improves but the teeth, eyelids and jaw stay the same. If you cannot find one, the answer for that photo is no face restoration.

### Exercise 5: Paper-theatre push-in

**Goal.** A 4-second move on one photo, with no GPU and no invented pixels.

**Steps.** Pick a photo with a clear subject and background. Cut the subject out by hand in GIMP or Krita, or with `rembg` if it is installed. Make three layers: background, subject, and a foreground object if one exists. Add soft shadows. Move the layers with small transforms in Kdenlive or DaVinci Resolve. Or run the `zoompan` command from Step 8. Keep the move to a 3 to 8% push-in.

**Time.** 2 to 3 hours (estimate).

**What good looks like.** The gaps are visible and plain. The move feels like depth. Nothing morphs or shimmers.

### Exercise 6: Morph between two real photos

**Goal.** A transition that says "time passed" with no generated frames.

**Steps.** Choose two real photos of the same person at different ages, cleared by a relative. Align the eyes by scaling and rotating. Run the ImageMagick morph (14 frames), and assemble it with ffmpeg. Make an `xfade` dissolve for comparison. If time allows, add landmarks using the LearnOpenCV example [65].

**Time.** About 2 hours (estimate).

**What good looks like.** The middle frames show ghosting on hair and background, not a new face. The clip is labelled L4a, and both end photos appear in the credits.

### Exercise 7: Label and credit one reconstruction

**Goal.** A labelled reconstruction with the right caption and metadata.

**Steps.** Write a one-page brief: what is known, what is invented, and which invented parts are generic. Choose the look (Route A). Write the caption "Reconstructed from [name]'s memory, 2026." Add a manifest row and a `steps.csv` entry with label L5. Add a line to the cue sheet. Optional, and unverified: test the ExifTool command on a copy of one TIFF, then read the tag back with ExifTool.

**Time.** 1 to 2 hours (estimate), not counting drawing.

**What good looks like.** The caption appears on screen and in the credits. The brief is saved. The record names the source and the date. If you ran the ExifTool check, the IPTC value reads back. If you did not, the step is marked TODO.

## Pitfalls

1. **Demos flatter.** Most public demos use clean, modern portraits. No source the research reached shows these tools on faded, low-resolution or black-and-white family prints. Treat any quality claim as untested until your bake-off.
2. **Restoration is generation.** Upscalers, face restorers and colourisers invent texture, features and colour. Frame makers invent frames. The tool tables in the research note say what each tool invents.
3. **Face drift and plastic skin.** GFPGAN may change identity [17]. SeedVR2 had a "plastic" output problem, which version 2.5.6 addressed [24]. Fake-face methods such as PULSE make people who do not exist [30]. Blend back, and check with a relative.
4. **Age gaps.** Face recognition accuracy falls by 10 to 17 percent for same-person pairs with age gaps, in a 2017 benchmark [53]. The note expects identity tools to pull a face toward the age of the reference photo. That is a reasoned expectation, not a tested result (judgment in the note). Do not expect one face to cover childhood to today. Use each photo's own face, one photo per output.
5. **Stale tutorials.** FILM was archived 2025-10-14 [61]. Microsoft's Old Photos repository was archived 2026-10-03 [25]. DeOldify was archived 2024-10-19 [29]. IP-Adapter-plus has been maintenance-only since 2025-04-14 [44]. The first Nano Banana model (`gemini-2.5-flash-image`) is marked deprecated with a 2026-10-02 shutdown on Google's pricing page [51]. The image docs call it only "legacy" [50]. That date has already passed, so assume it is gone and check before use. Check the dates and licence of any tutorial from 2023 to 2025.
6. **Licence traps.** See Decision 3.
7. **Fake sites and listicles.** The CodeFormer, FramePack and DepthFlow pages each warn that look-alike sites are unofficial or fraudulent [15][72][60]. Use the official repository or vendor page only.
8. **Cloud privacy.**
   - *Gemini consumer app, with Keep Activity on:* uploaded photos may be used to train models, and some chats are reviewed by people and kept for up to three years [84]. Never for family photos.
   - *Gemini API unpaid tier:* content is used to improve products, and the terms say not to submit personal information [85]. Never for family photos.
   - *Gemini API paid tier:* prompts and files are not used to improve products [85]. Acceptable only for cleared photos, with your yes (Decision 6).
   - *Luma:* its privacy policy lists training as a purpose, with no opt-out stated [86]. Never.
   - *Adobe Firefly:* Adobe says it has never trained Firefly on customer content [87]. The consumer terms were not read (TODO(research)).
   - *Replicate:* API predictions are removed after an hour [88]. Save results locally at once.
   - *Topaz:* desktop apps render locally and without limit [31]. The privacy policy does not say whether images are used for training [32]. The cloud terms were not read (TODO(research)). Use the desktop app offline.
   - *Unreadable terms:* OpenAI, Runway, Kling, Midjourney, MyHeritage, Remini and Bending Spoons, fal.ai's retention, Hugging Face Spaces. The research could not read these. Treat them as "do not upload."
   - *Unofficial "free restore" sites and rembg's cloud back-ends.* Never [15][55].
9. **Animating the dead.** See Step 8 and Decision 4. Deep Nostalgia's scale [101] shows demand, not consent. TODO(research): find out how families react to animating people who have died.
10. **Voice.** Voice cloning, lip-sync and talking-photo tools are out of scope. In *Roadrunner*, a synthetic voice of Anthony Bourdain read his written words. It was undisclosed until an interview, and the estate executor disputed having approved it [98].
11. **Reconstructions must look like reconstructions.** Never photoreal. Always the house look, with a caption. Never pair a generated face with a real name in a way that suggests a record. Viewers flagged images in *What Jennifer Did* as possibly AI-made, and the executive producer denied AI use [99].
12. **Provenance is partial.** SynthID marks Google outputs, not local restoration [50][82]. MP4 files may drop IPTC fields (unverified). The manifest and the credits are the real record.
13. **Outputs disappear.** Veo videos are stored for 2 days [82]. Replicate API outputs are removed after an hour [88]. Models get retired [51]. Download and log at once.
14. **Hardware and drivers.** The V600 is discontinued, and the Epson pages list old operating systems [9][10]. Test your scanner on your Windows version early, or use VueScan [11].
15. **Mixed looks.** Heavily restored photos next to untouched ones break a chapter's look. Set one restoration level per chapter.
16. **Covert handling (charter).** A phone scan may land in a photo library that syncs to a cloud account your mother can see, or on a shared device. Use a device and account she cannot see, and check the sync settings before the first scan. TODO(research): the note did not check how PhotoScan or Photomyne save and sync files on the maker's phone.
17. **Originals in other hands.** Relatives lend prints. Handle them gently, scan the backs too, and return them unchanged [2].
18. **Sprawl.** Model tinkering never ends. Time-box each tool trial, and finish one chapter first (principle 6).

### Known gaps (TODO(research))

- **No archival-photo evidence** for any generative edit tool. The week 1 bake-off closes this.
- **Restraint prompts** are the research note's synthesis, not tested by creators. The creator threads, YouTube and Reddit were not reached, because the search budget ran out.
- **Terms pages not read:** see Pitfall 8.
- **FADGI numbers.** The third-edition guidance on ppi, bit depth and colour sits in a PDF the research could not read [4]. The 600 ppi and 3200 to 4000 ppi figures are partly judgment.
- **Home video** (VHS, Hi8, MiniDV) and **8 mm film** were not researched.
- **VRAM** for FLUX.1 Kontext dev, Qwen-Image-Edit-2511, Wan FLF2V and Wan2.2 14B is not stated in any source read.
- **First-and-last-frame support and pricing** for Kling, Runway and Luma are unconfirmed.
- **Gemini 2.5 Flash Image.** The pricing page says deprecated with a 2026-10-02 shutdown; the image docs say only "legacy." The sources conflict.
- **ExifTool syntax, C2PA signing and MP4 handling** were not run. ExifTool was not installed in the sandbox.
- **MagicaVoxel and Blockbench** licence and price are unverified.
- **DepthFlow's CLI documentation** (depth.tremeschin.com) was not fetched.
- **Windows set-up** for ffmpeg, ImageMagick, Real-ESRGAN and CodeFormer was not researched. The commands were tested on Linux. SAM 2 notes WSL for Windows [56]. Check each tool's Windows build or use WSL.
- **Budget figures.** The note's summary says 40 to 75 human hours, and its table says 40 to 80 (45 to 80 with no GPU). Use the table.
- **ArtCraft apps** (PhotoCraft, LightCraft and the rest) are outside this track. TODO(research): see the craft-visual and craft-motion tracks.
- **Open family and maker decisions:** whether the family accepts any animation of relatives who have died, and whether the work is a private gift or a public or ticketed showing (Decisions 3 and 4).

## Best references

These eight are the most useful for the maker. Each one is a primary page the research read.

1. **NARA, Digitizing Family Papers** [2]. https://www.archives.gov/preservation/family-archives/digitizing.html. Plain rules for names, the 3-2-1 backup, and who, what, where and when. Read it before you name your first file.
2. **Library of Congress, Scanning Your Personal Collections** [1]. https://www.digitalpreservation.gov/personalarchiving/documents/scanning_collections.pdf. Resolution and greyscale basics. It is dated 2011, so keep its JPEG advice out and use a lossless master.
3. **John Hultgren, Scanning Film** [5]. https://hultgren.org/articles/scan/index.php. One practitioner's copy-stand setup for film and prints. It gives no DPI figures, so pair it with [13].
4. **darktable, negadoctor module** [13]. https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/negadoctor/. How to convert negatives, and why you need the film border.
5. **CodeFormer** [15]. https://github.com/sczhou/CodeFormer. The fidelity dial `w` and the warning about unofficial sites. Its last news item is dated 2023-07-20, so check for a newer release.
6. **FLUX.1 Kontext dev, ComfyUI tutorial** [34]. https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev. The prompt wording that keeps a face. Read the licence on the model card [33] first, because it is non-commercial.
7. **LearnOpenCV FaceMorph** [65]. https://github.com/spmallick/learnopencv/tree/master/FaceMorph. Example code for a classic landmark morph. Check its licence before reuse, because the page does not show one.
8. **Archival Producers Alliance, GenAI Best Practices Tool Kit** [96]. https://www.archivalproducersalliance.com/tool-kit-for-documentaries. Templates for transparency tips, crediting and a cue sheet, which fit our credits page.

## Sources

Numbers match the research note's Sources list at `research/ai-imagery.md`. The entries are copied from that list. Only the number format changed, from "1." to "[1]." Source [102] is a local test run in the research sandbox, not a web page. Fetched pages were read on 2026-10-18 unless the entry says otherwise. "Snippet" means the page was not fetched, only a search summary was seen.

[1] Scanning Your Personal Collections (Library of Congress Personal Digital Archiving series) — https://www.digitalpreservation.gov/personalarchiving/documents/scanning_collections.pdf — PDF created 2011-10-06 — 300 dpi for documents; 400 to 600 for enlargements; above 600 unnecessary; greyscale vs colour; `yyyymmdd` names; two copies.
[2] Digitizing Family Papers (U.S. National Archives) — https://www.archives.gov/preservation/family-archives/digitizing.html — undated — Latin-letter names, 3-2-1 backup, keep originals, who/what/where/when; defers ppi to FADGI and IPI.
[4] FADGI Technical Guidelines for Digitizing Cultural Heritage Materials page — https://www.digitizationguidelines.gov/guidelines/digitize-technical.html — 3rd edition 2023 — page lists the guidelines but no numbers.
[5] Scanning Film (John Hultgren) — https://hultgren.org/articles/scan/index.php — 2023-11-10 — camera-scanning setup with macro lens, stand, holders; no DPI.
[6] Is Google PhotoScan still available in 2026? (Lightroom Tools blog) — https://lightroom-tools.com/blog/google-photoscan-still-available-2026 — 2026-05-18 — PhotoScan free but frozen; four-dot glare removal; alternatives.
[7] PhotoScan by Google Photos (AppBrain listing) — https://www.appbrain.com/app/photoscan-by-google-photos/com.google.android.apps.photos.scanner — snippet only — last update 2023-07-24.
[8] Review: Epson Perfection V600 vs. V850 Photo Scanners (Larry Jordan) — https://dev.larryjordan.com/articles/product-review-epson-v600-vs-v850-photo-scanners/ — snippet only — Dmax 3.5 vs 4.0; V850 better dust removal; interpolation caveat.
[9] Epson Perfection V600 Photo Scanner (Epson America) — https://epson.com/For-Home/Scanners/Photo-Scanners/Epson-Perfection-V600-Photo-Scanner/p/B11B198011 — undated, © 2026 — specs; marked Discontinued.
[10] Epson Perfection V850 Pro (Epson America) — https://epson.com/For-Home/Scanners/Photo-Scanners/Epson-Perfection-V850-Pro-Photo-Scanner/p/B11B224201 — undated — $1,999; Dmax 4.0; cart error.
[11] VueScan — https://www.vuescan.com/ — 9.8.59 dated 2026-09-26 — 8,000+ scanners; Infrared Clean; Restore Fading; no price on page.
[12] Negative Lab Pro — https://www.negativelabpro.com/ — v3.1, © 2025 — Lightroom Classic plug-in; no price on page.
[13] darktable negadoctor module — https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/negadoctor/ — undated — negative conversion workflow.
[14] Photomyne — https://www.photomyne.com/ — app v6.6.2, © 2015-2026 — $59.99 per year after 3-day trial; AI restoration extra credits.
[15] CodeFormer (sczhou) — https://github.com/sczhou/CodeFormer — last news 2023-07-20 — `w` fidelity; CLI; NTU S-Lab licence; unofficial-site warning.
[17] GFPGAN (TencentARC) — https://github.com/TencentARC/GFPGAN — undated — v1.3 may slightly change identity; Apache-2.0.
[18] Real-ESRGAN (xinntao) — https://github.com/xinntao/Real-ESRGAN — undated — ncnn portable builds; BSD-3; model list.
[19] GFPGAN and CodeFormer guide (Replicate) — https://replicate.com/guides/upscaling-images/gfpgan-and-codeformer — snippet only — likeness advice.
[20] CodeFormer vs ESRGAN: Enhance faces (Segmind) — https://blog.segmind.com/codeformer-vs-esrgan/ — snippet only — example where result bore little resemblance.
[21] SUPIR (Fanghua-Yu) — https://github.com/Fanghua-Yu/SUPIR — undated — non-commercial; low-memory options.
[22] ComfyUI-SUPIR (kijai) — https://github.com/kijai/ComfyUI-SUPIR — undated — VRAM tests; SUPIR now in ComfyUI core.
[23] SeedVR / SeedVR2 (ByteDance-Seed) — https://github.com/ByteDance-Seed/SeedVR — ICLR 2026 acceptance noted 2026-01-27 — Apache-2.0; over-generation warning.
[24] ComfyUI-SeedVR2_VideoUpscaler (numz) — https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler — v2.5.24 dated 2025-12-24 — VRAM tiers; CLI; plastic-output fix.
[25] Bringing Old Photos Back to Life (Microsoft) — https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life — archived 2026-10-03 — research-only, MIT.
[28] DDColor — https://github.com/piddnad/DDColor — last news 2024-01-28 — Apache-2.0; CLI.
[29] DeOldify (jantic) — https://github.com/jantic/DeOldify — archived 2024-10-19 — MIT; accuracy caveats.
[30] PULSE (adamian98) — https://github.com/adamian98/pulse — CVPR 2020 — outputs are imaginary faces.
[31] Topaz Labs pricing — https://www.topazlabs.com/pricing — no date, 2026 offers — Photo, Gigapixel, Video, Studio prices; local unlimited.
[32] Topaz Labs privacy policy — https://www.topazlabs.com/privacy-policy — last updated 2024-10-03 — does not address local vs cloud or training.
[33] FLUX.1 Kontext [dev] — https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev — undated — 12B editing model; non-commercial, gated; API outputs carry C2PA.
[34] FLUX.1 Kontext dev ComfyUI tutorial — https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev — undated — identity-preserving prompt patterns.
[36] Qwen-Image-Edit-2511 — https://huggingface.co/Qwen/Qwen-Image-Edit-2511 — undated — identity consistency; 20B; Apache-2.0.
[37] Qwen-Image-Edit ComfyUI tutorial — https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit — undated — fp8 files; scale to about 1 MP.
[38] FLUX.2 (Black Forest Labs) — https://github.com/black-forest-labs/flux2 — dev 2025-11-25, klein 2026-01-15 — variants and licences.
[40] InstantID — https://github.com/instantX-research/InstantID — last log 2024-07-18 — one face; insightface non-commercial.
[41] PuLID — https://github.com/ToTheBeginning/PuLID — last entry 2024-10-31 — FLUX 16 GB; Apache-2.0.
[42] InfiniteYou — https://github.com/bytedance/InfiniteYou — March 2025 — VRAM figures; model CC-BY-NC.
[44] ComfyUI_IPAdapter_plus — https://github.com/cubiq/ComfyUI_IPAdapter_plus — maintenance mode 2025-04-14 — FaceID notes.
[45] Kontext-Style-Loras (Owen777) — https://huggingface.co/Owen777/Kontext-Style-Loras — undated — 22 style LoRAs; no licence stated.
[46] ai-toolkit (ostris) — https://github.com/ostris/ai-toolkit — © 2026 — training suite; MIT.
[47] fluxgym — https://github.com/cocktailpeanut/fluxgym — undated — 12/16/20 GB LoRA training; MIT.
[50] Gemini API image generation docs — https://ai.google.dev/gemini-api/docs/image-generation — undated — editing; reference limits; SynthID; model names.
[51] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing — undated — Veo 3.1 and image prices; free vs paid data use; 2.5 Flash Image deprecation note.
[52] fal.ai pricing — https://fal.ai/pricing — undated, 2026 — Kling and Nano Banana Edit prices.
[53] The Cross-Age LFW (CALFW) — https://arxiv.org/abs/1708.08197 — 2017 — 10 to 17 percent accuracy drop across ages.
[54] MapartCraft — https://github.com/rebane2001/mapartcraft — undated — browser mapart generator; GPL-3.0.
[55] rembg — https://github.com/danielgatis/rembg — undated — CLI, CPU, MIT, cloud back-end warning.
[56] SAM 2 — https://github.com/facebookresearch/sam2 — SAM 2.1 2024-09-30 — Apache-2.0.
[58] Depth Anything V2 — https://github.com/DepthAnything/Depth-Anything-V2 — undated — licences by size.
[60] DepthFlow (BrokenSource) — https://github.com/BrokenSource/DepthFlow — undated — AGPL-3.0; fake-site warning.
[61] FILM (google-research/frame-interpolation) — https://github.com/google-research/frame-interpolation — archived 2025-10-14 — Apache-2.0; TF2/CUDA 11.2.
[65] LearnOpenCV FaceMorph example — https://github.com/spmallick/learnopencv/tree/master/FaceMorph — undated — folder listing only (code files and landmark files).
[67] Wan2.1-FLF2V-14B-720P — https://huggingface.co/Wan-AI/Wan2.1-FLF2V-14B-720P — undated — first/last frame; 720p only; Apache-2.0.
[69] Wan2.2 — https://github.com/Wan-Video/Wan2.2 — released 2025-07-28 — variants, VRAM, Apache-2.0.
[70] Wan2.2 ComfyUI tutorial — https://docs.comfy.org/tutorials/video/wan/wan2_2 — undated — 5B fits 8 GB with offload; FLF2V workflow.
[72] FramePack (lllyasviel) — https://github.com/lllyasviel/FramePack — latest news 2025-07-14 — 6 GB; Apache-2.0; speed; fake-site warning.
[75] ComfyUI-LTXVideo — https://github.com/Lightricks/ComfyUI-LTXVideo — undated — 32 GB+ VRAM.
[77] WanGP (deepbeepmeep) — https://github.com/deepbeepmeep/Wan2GP — v18.17 on 2026-10-15 — 6 GB select models.
[80] Runway pricing — https://runway.com/pricing (redirected from runwayml.com/pricing) — undated — plans and credits.
[81] Luma pricing — https://lumalabs.ai/pricing — undated — plans, Ray3.x credits.
[82] Veo 3.1 in the Gemini API — https://ai.google.dev/gemini-api/docs/veo — Veo 3.1 Preview updated Jan 2026, Lite Mar 2026 — image-to-video, `lastFrame`, `allow_adult`, SynthID, 2-day storage.
[83] RunPod pricing — https://www.runpod.io/pricing — updated 2026-10-08 — GPU hourly prices.
[84] Gemini Apps Privacy Hub — https://support.google.com/gemini/answer/13594961 — last updated 2026-10-13 — training, human review, retention.
[85] Gemini API Additional Terms of Service — https://ai.google.dev/gemini-api/terms — effective 2026-03-23, updated 2026-04-28 — unpaid vs paid data use.
[86] Luma Labs Privacy Policy — https://lumalabs.ai/legal/privacy-policy — last updated 2026-04-20 — model training as a purpose.
[87] Adobe Firefly generative AI approach — https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html — undated, © 2026 — no training on customer content.
[88] Replicate data retention — https://replicate.com/docs/topics/predictions/data-retention — undated — API outputs removed after one hour.
[89] IPTC Digital Source Type vocabulary — https://cv.iptc.org/newscodes/digitalsourcetype/ — undated; retirements dated 2022-06-14 and 2024-09-17 — term list and definitions.
[90] IPTC Photo Metadata User Guide — https://www.iptc.org/std/photometadata/documentation/userguide/ — undated — Digital Source Type guidance.
[91] C2PA — https://c2pa.org/ — page updated 2026-01-08 — Content Credentials standard.
[92] Content Credentials — https://contentcredentials.org/ — page updated 2025-10-06 — provenance feature overview.
[94] Partnership on AI Responsible Practices for Synthetic Media — https://syntheticmedia.partnershiponai.org/ — launched Feb 2023, case studies added 2024 — consent, disclosure, direct vs indirect.
[95] Archival Producers Alliance GenAI guidelines — https://www.archivalproducersalliance.com/genai-guidelines — undated; guidelines PDF titled Sept 2024 (not readable) — landing page.
[96] APA GenAI Best Practices Tool Kit — https://www.archivalproducersalliance.com/tool-kit-for-documentaries — undated — transparency tips, credits, cue sheet.
[98] Roadrunner: A Film About Anthony Bourdain (Wikipedia) — https://en.wikipedia.org/wiki/Roadrunner:_A_Film_About_Anthony_Bourdain — undated — AI voice controversy.
[99] What Jennifer Did (Wikipedia) — https://en.wikipedia.org/wiki/What_Jennifer_Did — undated — suspected AI images.
[101] MyHeritage (Wikipedia) — https://en.wikipedia.org/wiki/MyHeritage — undated — Deep Nostalgia launch and scale.
[102] Local sandbox test (this session, 2026-10-18) — ffmpeg 6.1.1 and ImageMagick `convert`; commands `convert a.png b.png -morph 14`, `ffmpeg ... xfade`, `zoompan`, `minterpolate=fps=48:mi_mode=mci`, and frame-sequence assembly ran without error on synthetic images; confirms the commands run, not that results are good on real faces.

## Changelog

- 2026-10-18: Version 1, written by the haiku scribe from `research/ai-imagery.md` (sources read 2026-10-18) and `CHARTER.md`. Open gaps are listed under Pitfalls as TODO(research). Each decision lean is marked either "from the note" or "scribe's reading, confirm."
