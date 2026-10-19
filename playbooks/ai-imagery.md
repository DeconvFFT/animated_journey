# AI Imagery and Motion from Real Photos

*For the maker. Track `ai-imagery`. Built from the research note at `research/ai-imagery.md` (sources read 2026-10-18). Deadline: Saturday 2027-02-27.*

Reconciled with [DECISIONS.md](../DECISIONS.md) (2026-10-18, and again on 2026-10-19 after the her-world merge), the single source of truth. Where a lean below disagrees with a register row, the register wins. D-nn rows are decided by the maker; W-nn rows are working defaults. No generative route ever touches a deity (D-28, W-61), and the game-world rule is retired (D-29).

**How to read this.** Numbers in square brackets, such as [2], point to the Sources list at the end. They match the research note. **TODO(research)** marks a gap we have not closed. Time estimates are planning guesses unless a source gives them. Some sources were seen only as search snippets; the Sources list says so.

## Why this matters for our life journey

Your mother's real photos are the strongest material this project has. The charter's fourth principle says AI may restore, restyle, animate and connect real photos. It may not invent events, create fake people, or put words in anyone's mouth. This playbook shows how we keep that promise.

The main risk is that these tools make things look finished. Almost every tool that cleans, enlarges, colours or animates a photo also invents something: texture, a feature, a colour, or a frame. Some of those inventions will look like memory and are not.

Three facts shape the plan.

- **Nobody has tested these tools on the kind of photo we have.** The research found clean, modern demo portraits. It found no tests on faded, low-resolution or black-and-white family prints. So in week 1 we run a five-photo bake-off on stand-in photos with the same defects, judged by the maker alone (under only-me there are no insiders, D-03; likeness is the maker's, W-40). Her own photos wait for P-LOCK (Sat 14 Nov) and the vertical slice (D-13, W-07).
- **Most of the work is hands-on.** The research note estimates about 40 to 80 human hours for 300 photos, mostly scanning and hand clean-up, not computer time. This is an estimate, not a measurement. The research note's summary and its table now agree.
- **We start small.** One chapter, a 30-photo vertical slice (C01, final Sun 20 Dec, W-07), comes before the rest of the archive (charter principle 6).

## Core principles

1. **If it looks like a photograph, it is a photograph, possibly restored. Anything invented is drawn.** The research note proposes this as a house rule. It needs your approval before we rely on it. At L2, generative repair is allowed on non-face regions only. Faces get non-generative fixes, or CodeFormer or GFPGAN with blend-back. A generative change to a face moves the image to L3, where it must look drawn, or the image is rejected (Step 6).
2. **Keep the original untouched.** Every change is a labelled copy. The master scan never changes [1][2].
3. **Fix the photo without AI first.** Levels, colour cast, dust and cropping come first. Escalate only if the photo is still unusable.
4. **Restoration is generation.** Upscalers, face restorers, colourisers and frame makers all invent something. Find out what each tool invents, and write it down.
5. **The maker judges likeness, alone.** A sharpness score does not tell you whether the face is still her. Under only-me there are no insiders (D-03), so the maker signs likeness from their own knowledge: five of five correct in a shuffled line-up, passed twice, 48 hours apart (W-40). The Fable advisor flags and never signs it (charter principle 5).
6. **Morph only between real photos.** A classic morph or a dissolve adds no new faces. A tool that generates in-between frames is labelled, and it is never shown as a record.
7. **Leave the faces of people who have died alone**, unless the family has said yes first. Motion in the environment, such as light, leaves or parallax, is the safe default. Under only-me nobody can be asked before the premiere (D-03), so the premiere cut has no face or expression motion for them at all (W-40).
8. **Small first, then scale.** One photo, then the 30-photo slice, then the rest.
9. **Show the original.** Keep an untouched L0 or L1 version of every hero photo, and show it beside the restoration at least once. See "When not to restore" below.

## When not to restore

Restoration is a story choice, not a default. What a tool can fix does not decide what should be fixed.

- **Decide the level per chapter from what the story needs,** not from what the tool can do. Use one restoration level for each chapter, so the look holds (Pitfall 15).
- **Treat the era signals as content.** Fade, grain, Polaroid borders, the scalloped edge, date stamps and handwriting on the back tell the viewer when a photo was taken. Keep them unless the chapter's story needs them gone. This is charter principle 3, texture over checklist, applied to the photos.
- **Keep an untouched L0 or L1 version of every hero photo** in the timeline.
- **Show the untouched original beside the restoration at least once,** and say plainly what was added: colour, sound, motion. The lesson of *They Shall Not Grow Old* is that critics said it erased the original filmmakers and implied the archive was in disrepair [100].

## How to do it, step by step

Each step names the research recipe it comes from (R1 to R6 in the note). Commands were tested on Linux only (research sandbox, 2026-10-18). Each command that differs on Windows has its Windows form beside it, and every Windows form is **untested on Windows** until the maker runs it. The install route is in Step 0. Check each command's own help text before you rely on its flags.

### Step 0: Set up the folders and the records (R1)

Create four folders: `01_masters`, `02_work`, `03_exports` and `04_reconstructions`. Put them inside the VeraCrypt container on the external drive, in a separate Windows account that no one in the family will browse during the surprise (W-25, W-26). Keep one checksum file for the masters.

Give every scan an ID such as `LJ-B03-0042-F`. B03 is the box, 0042 the sequence number, and F the front (use B for the back). A rescan adds `-R2`. Put the date in the record, not in the file name, because many photos are undated. This departs on purpose from the Library of Congress's date-first names [1].

Keep two plain CSV files:

- `manifest.csv`, one row per scan. Columns: id, box, medium, scan_date, device, ppi, bit_depth, profile, date_est, date_confidence, people, place, caption_source, interview_date, consent_note, sha256, notes. `interview_date` is filled when a caption cites an interview, as the L5 caption does; before the premiere it holds the date of the album-and-hands session or of the maker's own written recollection (W-49, D-03).
- `steps.csv`, one row per change. Columns: derivative_id, parent_id, step_no, tool, version, settings, seed, invents (none, texture, colour, frames or faces), label_level, reviewer, approved, deity_form, deity_source. `deity_form` and `deity_source` stay `none` on every row that is not a deity image (W-61, Step 9).

The National Archives asks for who, what, where and when [2]. The manifest does that job.

**Install route on the Windows PC (untested on Windows).** Native Windows is the default. WSL is a fallback, needed only if the PC has no working Vulkan driver, in which case the Real-ESRGAN `.exe` prints `invalid gpu device` [104]. Whether WSL fixes that is UNVERIFIED. The only tested commands are the Linux runs in the research sandbox [102][104][105].

- **ffmpeg:** `winget install ffmpeg`, or `winget install "FFmpeg (Essentials Build)"` [121][122].
- **ImageMagick 7:** `winget install ImageMagick.Q16-HDRI` [120]. It runs as `magick`, not `convert`, because Windows ships its own `convert.exe`, a disk utility [120].
- **Real-ESRGAN (ncnn):** download `realesrgan-ncnn-vulkan-20220424-windows.zip` from release v0.2.5.0 [110], unzip it, and run `.\realesrgan-ncnn-vulkan.exe`.
- **rembg:** needs Python 3.11 to 3.13 [123]. Make a virtual environment with `py -3.12 -m venv .venv` and install with `pip install "rembg[cpu,cli]"` [123] (the venv commands are judgment, untested).
- **Depth Anything V2 Small:** install CPU PyTorch from `https://download.pytorch.org/whl/cpu`, then `pip install transformers pillow` [124][125][106].
- **ExifTool:** unzip `exiftool-13.59_64.zip`, rename `exiftool(-k).exe` to `exiftool.exe`, keep the `exiftool_files` folder beside it, and put both on PATH [118].
- **WSL:** `wsl --install` from an administrator PowerShell, then restart. It needs Windows 10 build 19041 or later, or Windows 11 [126]. SAM 2 also notes WSL as the route for Windows [56].
- **Cloud container for CPU steps:** it runs Linux and is temporary. Use it by content, as Decision 6 sets out. Work with no family photo may run there. Anything with her face or a relative's stays on the maker's PC: no full-size family photo goes to a cloud session, a hosted renderer or a rented GPU. A rented GPU is for non-family imagery only, on Secure Cloud with an encrypted volume and the maker's recorded OK, never Community Cloud (D-15, W-23, W-24). The team's cloud session is a Linux VM with no GPU and no view of the maker's PC (checked 2026-10-18); the hardware tier comes only from the Q2 PowerShell block in the research note.

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

Windows (PowerShell, untested on Windows; `sha256sum` does not exist there): `Get-FileHash 01_masters\*.tif -Algorithm SHA256 | Export-Csv checksums.csv -NoTypeInformation`. This writes CSV rather than the `sha256sum` text format, with the same SHA-256 hashes.

Back up 3-2-1 [2]: three copies, on two kinds of media, with the second copy on a second encrypted SSD kept elsewhere. There is no cloud copy of family media (W-25).

### Step 4: Make the cleaned copy (L1)

Work on a copy, never on the master. Crop and straighten. Fix the colour cast one channel at a time, with levels and curves. Remove remaining dust with the healing brush in GIMP or Krita. Save it with the suffix `__L1`. There is no AI in this step.

Faded 1970s to 90s colour prints usually have a magenta or yellow cast and low contrast. That is a levels problem, so fix it per channel before any AI (judgment; no tested AI result exists for these prints). If you also use the scanner's own "restore fading" output, keep it as a separate file, because it changes colours [11].

### Step 5: Decide whether the photo needs help

Count pixels against the master the film will be made at (1080p, W-15). The arithmetic is: pixels needed across = timeline width × (1 + push-in) × crop factor. The crop factor is 1.0 for a landscape print that fills the frame width.

The master is settled (W-15, [DECISIONS.md](../DECISIONS.md)): 1920x1080, 16:9, with stills prepared at 3840 px on the long edge. A 2K Flat DCP is derived from the master and never re-authored, and 4K is not needed. A 4x6 print scanned at 600 ppi (3,600 by 2,400 px) is about 6 percent under the 3840 px target, which a plain resize covers, and it is enough for the 1080p master (about 2,075 px needed with an 8 percent push-in) and for a 2K DCP (2,048 px across [156]; about 2,160 to 2,210 px needed). UHD applies only to single hero shots if a 4K cinema is booked. On UHD, the same print with an 8 percent push-in needs about 4,150 px across, so it falls short.

For a hero print booked at UHD, choose one of these:
- Scan hero prints at 800 to 1,200 ppi. A 4x6 at 800 ppi is 4,800 by 3,200 px.
- Allow a 2x Real-ESRGAN pass on hero prints, logged as an L2 step (Step 6).
- Keep push-ins under about 5 percent. This helps only if the picture fills less than about 89 percent of the frame width (3,600 ÷ (3,840 × 1.05)). At full width, even a 0 percent push-in needs 3,840 px.

Upscale only where the count is short: wallet prints, 1990s digital camera files, video frames and any hero print booked at UHD.

### Step 6: Restore only what needs it (L2)

Work through the tools in this order.

1. **Non-AI fixes** (Step 4).
2. **Plain upscale, if needed.** Real-ESRGAN is free, licensed BSD-3, and has portable builds for Intel, AMD and Nvidia graphics [18]. Use `realesrgan-ncnn-vulkan -i in.png -o out.png -n realesrgan-x4plus -s 2` (`-s` takes 2, 3 or 4) [104][110][112]. Windows (untested on Windows): `.\realesrgan-ncnn-vulkan.exe -i in.png -o out.png -n realesrgan-x4plus -s 2`. The name `realesr-general-x4v3` does not work with the portable build. It exits 0 and writes an all-black image, so check each output's file size and look at it [104]. Check the flags with `-h` first.
3. **Face restoration, only if your bake-off says it helps.** CodeFormer has a fidelity dial, `w`, from 0 to 1. Higher is more faithful [15]. Try 0.7 to 1.0, then blend the result 40 to 60 percent back over the plain upscale, using a layer mask (practice from the note).
4. **Heavy damage only.** SeedVR2 [24] or SUPIR [21][22]. SUPIR is non-commercial [21]. SeedVR warns that it "can over-generate detail" on lightly degraded input [23].

**What L2 permits (house rule, made operational in round 1).**
- Generative repair on non-face regions only: tears, stains and backgrounds.
- Faces at L2: non-generative fixes, or CodeFormer at `w` 0.7 or higher, or GFPGAN, each with blend-back. `inference_gfpgan.py` has `-w/--weight` (default 0.5), but the value does nothing: outputs were bit-identical at 0, 0.5 and 1 for v1.3, v1.4 and RestoreFormer (run 2026-10-18) [146][149]. Do not tune it. Its `-v` also accepts 1.4 (README: "slightly more details and better identity than V1.3") and RestoreFormer, although the help text lists only 1, 1.2 and 1.3 (verified from the script, 2026-10-18) [146][147]. The fidelity dial is CodeFormer's `w` [15].
- Any generative change to a face moves the image to L3, where it must look drawn, or the image is rejected.

**Warnings about face tools.**

- GFPGAN v1.3's README says it can "have a slight change on identity" [17].
- Face super-resolution can make a different person. PULSE says it "makes imaginary faces of people who do not exist" [30].
- Sources disagree about which face tool keeps likeness best. The two comparisons we saw are search snippets only [19][20]. The only real test is your own photos at 100% zoom.
- Do not restore faces narrower than about 64 px. This is the note's rule of thumb (judgment).
- Reject any result with new teeth, new eyelids or a changed jaw.

**Colour, for black-and-white prints.** Treat colourising as costume design. DDColor [28] and DeOldify [29] guess every colour. DeOldify is known for "orange skin and overly red lips" [29]. Check clothes, rooms and cars against family memory or other colour photos. Keep skin tones muted. Caption the result "colours estimated." **Ruling on colourised faces (advisor review, round 2).** Colourising a face stays L2, captioned "colours estimated", if the tool changes chroma only and leaves the original luminance (L) on the face. It is a generative change, so L3 or reject, if luminance or texture on the face moves. Test it: convert the original and the result to CIELAB, and diff the L channel over the face box. The AI team writes the script, and the threshold is set in the bake-off. Starting values from the round-2 DDColor run, tiny model only: mean ΔL under 0.5 and 99th percentile under 2 over the face box, with a human look at any patch above 5 [153]. The L-channel diff catches luminance change; a 100 percent flick check catches texture change. DDColor's code keeps the input L by construction [151], but its README does not say so [28], so run the test rather than assume it.

**Label and log.** This step is L2. If a generative model repaired content, the IPTC value is `compositeWithTrainedAlgorithmicMedia` [89]. Log each tool, version, setting, seed and what it invents in `steps.csv`.

### Step 7: Connect two real photos (L4a or L4c)

**Classic morph (no invented frames, L4a).** Align the eyes first. Mark 10 to 20 landmarks on each photo: eyes, brows, nose, mouth, jaw, hairline and shoulders. Build Delaunay triangles. For each frame, warp both photos toward the in-between shape and cross-dissolve them, using 24 to 48 frames with ease in and out [65]. LearnOpenCV's FaceMorph is a reference example in Python and C++. Its folder shows code and landmark files only, so check its licence before reuse (not shown on the page) [65].

**Dissolve (no invented frames).** For a quick baseline, create a folder called `frames`, then run `convert a.png b.png -morph 14 frames/m_%02d.png` (ImageMagick 6 on Linux) [102]. Assemble the frames with `ffmpeg -framerate 24 -i frames/m_%02d.png -c:v libx264 -pix_fmt yuv420p morph.mp4` [102]. An `xfade` dissolve in ffmpeg also works: `ffmpeg -loop 1 -t 2 -framerate 24 -i a.png -loop 1 -t 2 -framerate 24 -i b.png -filter_complex "[0][1]xfade=transition=fade:duration=1:offset=1,format=yuv420p" xfade.mp4` [102]. The research team confirmed these commands run in a Linux sandbox. They did not judge the results on real faces.

Windows (untested on Windows): `magick a.png b.png -morph 14 frames\m_%02d.png`. ImageMagick 7 on Windows is `magick`, and the folder can be made with `New-Item -ItemType Directory frames`. The ffmpeg lines run unchanged in PowerShell with backslash paths. Keep the xfade filter in double quotes, as shown.

**Best design.** Chain morphs through real intermediate photos, such as ages 6, 12 and 18. Each segment then joins two real images. A paper-turn transition, or the object clock (W-32), says "time passed" without implying that a face existed.

**Generated in-between (L4c, use sparingly).** Tools such as Wan2.1 FLF2V [67] or Veo 3.1 with `lastFrame` [82] generate the whole video between two images. They invent intermediate faces and motion. Inspect the middle frames. If a face matches neither photo, it was invented. Use this only inside a labelled reconstruction, and never present it as a record of how she looked.

### Step 8: Add motion to one still (L4a, L4b)

**Parallax (L4a).** A still becomes a slow camera move, as if the camera were drifting past layers.

1. **Cut out the subject.** `rembg i -m u2net in.png fg.png` [55]. Name the model with `-m`: rembg 2.0.85 defaults to `bria-rmbg`, a 1 GB download whose weights need a paid agreement for commercial use [55][106][123]. Windows (untested on Windows): the same command inside the venv from Step 0. Use `-a`, `-vm` and `-dc` for hair edges. Never use the cloud back-ends, which "send images to their servers" [55].
2. **Make a depth map.** Depth Anything V2 Small is Apache-2.0 and falls back to CPU [58]. Blur or flatten the depth across faces, because depth maps bulge faces (judgment).
3. **Render.** Choose one: DepthFlow [60] (AGPL-3.0, GPU implied, its CLI docs were not read), a displaced plane in Blender (judgment), or layered cut-outs in Kdenlive or DaVinci Resolve (judgment).
4. **Keep the move small.** Orbit 2 to 3 degrees and push in 3 to 8 percent. Fill any gaps with cloned background, which stays L1. If you use generative fill, the clip becomes L4b and needs an "invents" note.

**Paper theatre (no GPU).** Make the layers physical. Use 3 to 5 cut-out layers with soft shadows, and move them with small transforms. The gaps show as honest holes. This needs no GPU and suits a papercraft look (judgment; a test idea for the vertical slice).

**Pure 2D push-in (sandbox-tested).** This 4-second move comes from the note [102]:

`ffmpeg -loop 1 -i in.png -vf "zoompan=z='min(zoom+0.0007,1.08)':d=96:s=960x720:fps=24,format=yuv420p" -t 4 kb.mp4`

Windows (PowerShell, untested on Windows): the same command. Keep the whole filter in double quotes, as shown. The single quotes inside it are literal. Do not wrap the whole filter in single quotes. This command is proof-grade only: `zoompan` snaps to whole pixels and fails MO8 on a final push, so finals use sub-pixel rendering (W-41; cinematic-quality MO8).

**Generated image-to-video (L4b).** Use only with these rules.

- The first frame is always the restored photo. Never generate from text alone.
- Describe motion only. Do not re-describe the face.
- Use restraint words such as "very subtle," "slow," "locked-off camera," "no scene change" and "no cut." These phrases are the research note's own synthesis from model documentation. No creator-tested prompts were reachable (untested).
- Prefer environment motion, such as leaves, curtains, dust in light, or water, over faces and hands.
- Keep clips short. Local models: 3 to 5 seconds. Veo: 4 seconds at 720p (the shortest), or 8 seconds with a higher per-second price for 1080p or 4K, because those need 8 seconds [114]. Use a fixed seed and 3 to 4 takes. Keep the take with the least change.
- Compare the first and last frames with a face-similarity script, and reject a take that drifts. This approach is unverified (TODO(research): choose and test a tool).
- Never ask for speech, lip movement or sound.

**Local options (need a graphics card).** Wan2.2 TI2V-5B: ComfyUI says it fits 8 GB with offloading [70], while the README says 24 GB [69]. FramePack needs 6 GB. Its README tests RTX 30, 40 and 50 series cards. Older cards are untested, not excluded [72]. WanGP runs select models on 6 GB and was updated 2026-10-15 [77]. LTX-2 needs 32 GB or more [75].

**Cloud options (privacy rules first; see Decision 6).** The prices below are for reference and for stand-in or non-family imagery only: no full-size family photo goes to a hosted service, ever (D-15, W-24). A Veo 3.1 clip at 720p with audio costs $0.20 on Lite, $0.40 on Fast and $1.60 on Standard for 4 seconds, or $0.40, $0.80 and $3.20 for 8 seconds [51]. Durations are 4, 6 or 8 seconds [82]; 1080p, 4K and reference images need 8 seconds [114]. The per-second prices for 1080p and 4K are not in our notes (TODO(research)). Kling 2.5 Turbo Pro via fal is about $0.35 for 5 seconds [52]. Luma Ray3.2 is about $0.30 at 720p on its Plus plan [81]. Whether Kling, Runway and Luma support first-and-last-frame generation is unconfirmed (TODO(research)). Runway's pricing page is internally inconsistent [80].

**Photos with a child in them: no cloud image-to-video.** Veo's image-to-video accepts only `allow_adult` [82]. Google's Vertex AI page says it rejects requests to generate content depicting children when `personGeneration` is not `allow_all` [116]. For these photos, use parallax or a local model only. Local image-to-video needs a graphics card. No test planned; the rule rests on [114] and [116], both read 2026-10-18.

**Faces of people who have died.** No face or expression animation (principle 7 and Decision 4). Parallax or environment motion only. Under only-me nobody can be asked before the premiere (D-03), so a family yes cannot be had in time and the premiere cut has no face or expression motion for them at all (W-40). MyHeritage's Deep Nostalgia made nearly 100 million animations [101]. The research did not read any reaction to animating the dead (TODO(research)).

### Step 9: Stylise in the house look (L3)

Pick one look for the whole chapter, and write a two-line style bible: palette, line weight, proportions. Then choose a route (labels follow recipe R4).

- **Route A, hand-made (default).** For each age band (child, teen, young adult, adult, older), pick three to five real photos. List identity attributes: hair shape and colour, glasses, beard, scars, posture, signature clothes, and height relative to others. Build a character sheet in the chosen look. The look is the maker's own hand-made material, filled at G1 (W-38); where that is seva craft it is the *making*, never the finished seva article and never a reconstruction painted onto Thakorji's clothes. The game-style block look of the earlier plan is retired with its tools (D-29). Take the palette from the photo.
- **Route B, AI edit on the real photo.** Use an edit model that starts from your photo, such as FLUX.1 Kontext dev [33][34] (non-commercial, gated), Qwen-Image-Edit-2511 (Apache-2.0) [36], or FLUX.2 klein 4B (about 8 GB) [38]. Keep the input near 1 megapixel [37]. In the prompt, name the subject specifically and add "while maintaining the same facial features, hairstyle, and expression" [34]. Change one thing per step. Keep one seed, one LoRA strength and one prompt template per chapter. Choose the result by line-up.
- **Route C, identity adapters: avoid for real people.** InstantID [40], PuLID-FLUX [41] and InfiniteYou [42] generate a new picture of the person from a prompt. The pose, clothes and scene are then invented. That makes it a reconstruction (L5), not a restyle. Use it only if a new angle is truly needed, and label it.
- **Route D, style LoRA on your own art.** Train a style LoRA on 10 to 30 of your own hand-made frames, using fluxgym (12 GB) [47] or ai-toolkit [46]. A person LoRA is out for her (D-16: no model is trained on her face). For anyone else it would need consent, local training, deletion afterwards and labels (research note, Q4c), and under only-me nobody can be asked, so none.

The Kontext style LoRAs, such as Clay Toy, Origami and Paper Cutting, have no stated licence [45]. Check it before use.

**Deities: no generative route (D-28, W-61).** The default policy is P1: symbols (lamp, kalash, lotus, conch, Om, linga, padukas, yantra, tulsi) and seva objects that are not a svarupa. Under it no deity figure is drawn, generated or photographed, and no generative route touches a deity in any class. If the maker rules a higher class at O-64, a deity image comes only from a hand-drawn vector symbol checked against the sheet, a hand-traced plate from a logged public-domain source, her own photograph (seva objects now; a svarupa picture only in the April version, and only if she knows), or a commissioned painting by a hereditary painter. Routes B (AI edits), C (identity adapters) and D (LoRAs) are never used on a deity, and a plate is never repaired by diffusion. Never draw or open the eyes of a svarupa, and remember that a picture of a svarupa may itself be a seva object (PR3, PR4 in `playbooks/pushtimarg-world.md`): nothing of the Thakorji, Lalan, chitraji or any picture of hers is photographed without her knowing. Deity line-art and vector symbols need no model at all. The rules live in `playbooks/hindu-visual.md`.

**Line-up test.** The maker signs likeness alone (D-03, W-40). Show five stylised faces in a shuffled line-up with decoys (the full protocol is in cinematic-quality T3). Ask who is who, and at what age. Adjust the attributes, not the faces. Run this on her real photos in the vertical slice, after P-LOCK (Sat 14 Nov). The pass mark is set (W-40): five of five correct, passed twice, 48 hours apart.

### Step 10: Label what you made

Every derivative gets a level. The ladder below is the research note's proposal (Q8).

| Level | Meaning | Example steps | IPTC value (in XMP) | On screen |
|---|---|---|---|---|
| L0 Scan | Unaltered digitisation | Flatbed or camera scan | `print`, `negativeFilm` or `positiveFilm` | Plain photo frame |
| L1 Cleaned | Human, non-generative fixes | Crop, deskew, levels, healing brush | `humanEdits` | Plain photo frame |
| L2 Enhanced | Algorithmic restoration that invents texture or colour | Upscale, face restore, colourise, diffusion repair | `algorithmicallyEnhanced`; use `compositeWithTrainedAlgorithmicMedia` if a generative model repaired content | Small "R" tag; colourised shots add "colours estimated" |
| L3 Restyled | Real photo redrawn in the house look | Edit model with style LoRA; hand-built character from the photo | `compositeWithTrainedAlgorithmicMedia` (AI edit on a real photo); `digitalCreation` (hand-drawn from scratch); `composite` (hand-drawn over a real photo) | Obviously stylised |
| L4 Animated | Motion added to a real photo | 4a parallax or classic morph (no generated frames); 4b image-to-video; 4c generated in-between | 4a `humanEdits` or `algorithmicallyEnhanced`; 4b and 4c `compositeWithTrainedAlgorithmicMedia` | Tag on the clip: "moved", "frames invented" |
| L5 Reconstruction | Scene never photographed, built from testimony | Stylised scene in the house look | `digitalCreation` (hand-built); `trainedAlgorithmicMedia` (AI-built); `compositeSynthetic` (mixed) | Always stylised; caption "Reconstructed from [name]'s memory, [interview date]" |

**Deity images (W-61).** A `deity_image` row carries L0 or L1 (her own photograph of seva objects that are not a svarupa; a svarupa picture only in the April version, when she knows), L2 only for non-generative scaling, or L3 for a hand-traced plate; never L4 or L5. `deity_form` and `deity_source` (the R17 route in `playbooks/hindu-visual.md`) are filled in `steps.csv` on every deity row. A diffusion repair of a deity plate is banned, because it can silently change an attribute: that is stricter than the face rule for people (W-40).

**L5 testimony under only-me.** Before the premiere the testimony behind an L5 scene comes from the maker's own knowledge or an album-and-hands session (W-49), not from a recorded interview (D-03). The caption names a relation rather than a person where it can, because person IDs only live in the repo and the ID-to-name key stays offline (D-14). Recorded relative testimony arrives with the April version (D-06).

The IPTC values come from the Digital Source Type vocabulary [89]. The IPTC user guide says to write the URI, not the label, and to store it in XMP only [90]. `humanEdits` is only for non-generative edits to captured media. A hand-built clay, paper, thread or floor-art scene made from scratch is `digitalCreation`, which means "created by a human using non-generative tools" and was added on 2024-09-17 [89]. `composite` is for hand work layered over a real photo, and `compositeSynthetic` is for mixed work. Checked against [89] on 2026-10-18.

Carry the label in four places: the file-name suffix (`__L2`), `steps.csv`, the embedded XMP, and the end-credit cue sheet [96]. The research note suggests the Archival Producers Alliance cue-sheet idea [95][96]. For how to disclose, Partnership on AI separates direct disclosure (labels on screen) from indirect disclosure (metadata, C2PA) [94]. On-screen tags and L5 captions that the audience must read follow the phone-safe frame (x-height 3.2% as the hard floor, W-63) and the caption rules (W-18); a caption's gloss is in the room's language, and any Gujarati card line is read by the native reader (W-35, O-62).

**Metadata command.** ExifTool 13.59 was run on Linux in the research sandbox, and writing the tag and reading it back worked [105]. Windows is untested. The tag needs the full URI. A label sentence written into the tag is stored as plain text, and readers will not recognise it [105]. The command is:

`exiftool -overwrite_original "-XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/print" LJ-B03-0042-F.tif`

Windows (untested on Windows): the same command in PowerShell, with the tag in double quotes as shown. Read it back with `exiftool -G1 -a -s -XMP-iptcExt:DigitalSourceType LJ-B03-0042-F.tif` [105].

`-overwrite_original` rewrites the file in place, so test on a copy first. For video, ffmpeg stream copy and re-encode both strip the tag from MP4. ExifTool writes it into MP4 and MOV and reads it back [105]. So write the tag as the last step, after the final export. Whether the maker's editor or a phone player keeps the tag is UNVERIFIED (TODO(research)). The manifest and the credits are the real record.

C2PA (Content Credentials) is an open standard [91][92]. Signing needs certificates, and the research did not cover signing for a private project (TODO(research)). Google's image and video outputs carry SynthID watermarks [50][82].

### Step 11: Review before anything is shown

- Flick between the original and the result at 100%, both ways.
- The maker answers "Does this look like her at that age?" from their own knowledge; there is no insider under only-me (D-03, O-11). Record the answer in the manifest.
- Check the label, the manifest row and the `steps.csv` entry.
- Check that the end credits name every AI tool used.
- Send anything sensitive, such as loss, illness, separation, money or conflict, through one-key-three-guards first: a decision sheet, the Fable advisor's written flag, and the maker's two decisions 72 hours apart (D-04, charter principle 5).

## Decisions you'll need to make

Each decision lists the options and our current lean. A lean marked "(from the note)" is one the research note states. A lean marked "(scribe's reading, confirm)" is one we derived from the note and the charter, and it needs your confirmation.

**1. Scanner: borrow, buy, or use a phone.**

- *Borrow a flatbed* from a library, a relative or a makerspace. Best for a large batch of prints at 600 ppi (decision table in the note).
- *Buy.* The Epson V850 Pro is $1,999 [10]. The V600 is discontinued [9]. VueScan can drive some scanners whose Epson drivers no longer work [11].
- *Use a phone.* Fine for fewer than 400 prints, with PhotoScan [6] (decision table in the note). Photomyne is the choice for album pages [14].
- **Lean (from the note):** borrow a flatbed for the big batch, and use a phone on a stand for album pages and small batches. (Scribe's reading, confirm:) do not buy anything before the bake-off. Defaulted in the register (W-27, O-23): the scan tool is whichever wins the ten-print pilot, decided Sun 15 Nov.

**2. Graphics card (GPU) tier.** The charter does not say which graphics card the Windows PC has.

- *No GPU.* CPU tools, hand work, parallax, morph and grading all work. Use a cloud step only where Decision 6 allows.
- *8 to 12 GB Nvidia.* Real-ESRGAN, CodeFormer, smaller SeedVR2 builds, FLUX.2 klein 4B, FramePack and WanGP.
- *16 GB or more.* Adds Qwen-Image-Edit-2511 and PuLID-FLUX. Some big-model VRAM figures are not stated in any source (see gaps).
- *Rent a GPU.* RunPod lists an RTX 4090 at $0.34 per hour (community) or $0.89 (secure), updated 2026-10-08 [83]. A rented machine is a third-party service, so it falls under Decision 6: non-family imagery only, Secure Cloud, never Community Cloud (W-23).
- **Lean (from the note):** start on the no-GPU path. Then check your graphics card and decide. Defaulted in the register (W-23, [DECISIONS.md](../DECISIONS.md)): the GPU tier is settled after the PC inventory (Exercise 1).

**3. Free public screening, or ticketed.** The charter now states a premiere at a mostly public gathering on Feb 27, to be treated as a film with a public audience (Known facts). Principle 7 (cleared for public screening) therefore applies. The open question is whether admission is free; the register's door-policy default is invite-only (W-54, decide by Sun 15 Nov).

- *Free public screening.* Non-commercial weights may be used only after each licence is read for public exhibition, and the reading is logged in `steps.csv`. Examples: SUPIR [21], FLUX.1 Kontext dev [33], Depth Anything V2 Base or Large [58], and rembg's `bria-rmbg` [55]. FLUX.1 dev's licence has two phrases, "production purposes" and "impact on end users", that only its publisher can settle [159].
- *Ticketed showing.* Exclude every non-commercial weight. Any payment, such as a ticket, donation or sponsor, flips them to no [159][161].
- *InfiniteYou is out either way.* Its licence says "for academic research purposes only" [42][162]. Do not use it for any frame that is shown.
- *Copyleft tools.* On the AGPL text, running Upscayl, DepthFlow and Video2X unmodified creates no source-code duty [166]. The models they bundle were not checked, and the GPL-3.0 tools (ComfyUI, chaiNNer, Krita AI Diffusion) were not re-read (TODO(research)).
- **Lean (scribe's reading, confirm):** assume a free public screening. Where two tools do the same job, choose the one with an Apache-2.0, MIT or BSD licence, for example U-2-Net [168] or Depth Anything V2 Small [58], so a ticketed showing later stays possible. Deity line-art and vector symbols need no model, so none of this licence reading applies to them (W-61).

**4. Animating people who have died.**

- *Option A: no motion of faces or expressions.* Environment motion and parallax only.
- *Option B: face or expression motion, with the family's explicit yes.* The note advises against it. Its research did not cover this case (TODO(research)).
- *Option C: stills only.* No motion at all for them.
- **Lean (from the note and charter principle 5):** Option A by default. Settled for the premiere cut (W-40, [DECISIONS.md](../DECISIONS.md)): no face or expression motion of anyone who has died, because under only-me the family cannot be asked before the premiere (D-03). Environment motion and parallax only; the family-yes route waits until after the premiere. The note's two lines read differently, one saying "no expression animation" and the other "without the family's say." We read them together as: never by default, and only with the family's yes.

**5. How far to label.**

- *Option A: file names only.*
- *Option B: the full six-level ladder (L0 to L5)* in file names, the manifest, the XMP metadata and the credits.
- **Settled (W-40, [DECISIONS.md](../DECISIONS.md)):** Option B, the full L0 to L5 ladder in the file name, `steps.csv`, the XMP and the end-credit cue sheet.

**6. Where processing happens (privacy). Decided: D-15, W-23, W-24 ([DECISIONS.md](../DECISIONS.md)).**

- *Option A: local only.* Nothing leaves your machine. This is the default for any photo with a family member in it, including anything with her face or a relative's.
- *Option B: a paid tier whose terms say no training.* Closed for family photos, because D-15 bars any full-size family photo from a hosted renderer; open for stand-ins and non-family imagery only. The Gemini API paid tier does not use prompts and files to improve products [85]. Veo results are stored for 2 days [82], so download them at once.
- *Option C: consumer apps, or any service whose terms the research could not read.* Never.
- *Option D: cloud, for work with no family photo in it.* Tool installs and tests, the stand-in bake-off, style-LoRA training on your own hand-made frames, scripts, renders of hand-built L5 scenes, and morph and parallax tests on stand-ins.
- **Decided: split by content, `cloud: none` by default.** Only the maker raises a photo set's `cloud` level; an agent never does (W-24). The charter says heavy work happens in the cloud wherever possible, and that nothing personal goes to a third-party service without your explicit say. We read both as one split. Option D is the default for everything with no family photo. Anything with her face or a relative's stays on your PC (Option A). `preview` proxies of about 768 px may go to the cloud container only after the account's model-improvement setting is off (W-23, W-24). A rented GPU is a third-party service: non-family imagery only, on Secure Cloud with an encrypted volume and your recorded OK, never Community Cloud. The team's cloud session is a Linux VM with no GPU and no view of your PC (checked 2026-10-18), so your hardware tier comes only from the Q2 PowerShell block in the research note.

**7. Face restoration.**

- *None.*
- *CodeFormer at high fidelity, with blend-back* [15].
- *An edit model on the real photo* [33][36].
- **Lean (from the note):** none by default. Run the bake-off, then choose per photo type. Non-AI fixes come first. Defaulted in the register (W-40, [DECISIONS.md](../DECISIONS.md)): faces at L2 are non-generative, or CodeFormer `w` of 0.7 or more blended back; any generative face change moves to L3 or is rejected; the five-photo bake-off on stand-ins comes before any tool decision.

**8. Stylisation route.**

- *Route A, hand-made* (no GPU, likeness built in by design).
- *Route B, AI edit on the photo.*
- **Lean (from the note):** Route A for the first chapter. Use Route B only if it passes the line-up test. Routes B to D are never used on a deity (W-61).

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
2. Clean the scanner glass. Scan five stand-in prints (from the Exercise 3 list, not her albums; scanning her albums this week would be gathering before the gate opens: the gate is P-LOCK on Sat 14 Nov, and collection starts Sun 15 Nov, D-13) at 600 ppi, colour, 16-bit.
3. Scan the back of any print with writing on it.
4. Name the files with the LJ pattern.
5. Fill in five rows of `manifest.csv`.
6. Run `sha256sum` and save `checksums.txt`. On Windows, use the `Get-FileHash` line in Step 3 (untested on Windows).
7. Make an L1 copy of one print.

**Time.** About 2 hours (estimate).

**What good looks like.** Five TIFFs that open at 100% with no glass dust. Names that follow the pattern. Five manifest rows with no blanks in id, medium, ppi or scan_date. A checksum file. The L1 copy has the same content as the master, only cleaner.

### Exercise 2: Fix a faded print without AI

**Goal.** Remove a colour cast using levels and curves alone.

**Steps.** Open the 16-bit master in GIMP, Krita or darktable. Adjust each channel so the whites look neutral. Add contrast with a gentle curve. Flick between the original and the result. Save as L1.

**Time.** 1 to 2 hours (estimate).

**What good looks like.** Skin looks like skin, not orange or grey. Nothing new appears in the picture. The maker recognises the print as the same photo, only cleaner.

### Exercise 3: Five-photo bake-off (week 1)

**Goal.** Find out whether any tool helps on the kinds of photo we really have, without using her archive for the test. The maker is the only judge (D-03, W-40): under only-me there is no insiders list.

**Steps.**
1. Pick five **stand-in** photos, none from her archive, with these defects: a faded colour print, a small black-and-white print, a soft group snapshot with small faces, a torn print, and a 1990s low-resolution digital file [research note, open question 1]. Sources: the maker's own prints, or public-domain archival prints. No relative's print: nobody is asked before the premiere (D-03). Candidates from the research follow-up (Q6; licences read on each Commons page, re-check before use): NARA 546220, a faded colour print [132]; US Navy 80-G-27208, a creased print [131]; the State Archives of North Carolina's 1952 black-and-white snapshot with cracks and a torn corner [134]; and "1971-12-John Call Cook", a faded colour snapshot under CC BY-SA 3.0 [133]. Files [133] and [134] show named people, and [134] names a child who may still be alive, so keep tests with them private and publish nothing from them. No candidate yet for the soft group snapshot or the 1990s digital file (TODO(research)).
2. For each photo, make four versions: (a) the L1 fix only; (b) Real-ESRGAN at 2x with `-n realesrgan-x4plus -s 2` [18][104]; (c) CodeFormer at `w` 0.7, 0.8 and 1.0, blended 50% back [15]; (d) one edit model run locally, if your graphics card allows. If not, skip it and say so.
3. Look at each version at 100%. Note what it invents: teeth, eyelids, jaw, hair, background.
4. Show the versions unlabelled to the judge (the maker alone; ask an agent to shuffle the labels). For each version, ask whether it still looks like the same person and the same photo as the original, and what it added. A result on a stand-in is evidence about the defect, not about her photos.

**Time.** 1 to 2 days, spread across the week (estimate).

**What good looks like.** A table with one row per stand-in and tool. Columns: "what it invents," "same person and same photo as the original," and a verdict. A chosen route for each defect type. Keep the stand-ins and their versions on your machine. Only the maker sees them. Her own photos are not used in this exercise, because gathering them waits for the charter's gathering gate.

### Exercise 4: The face dial

**Goal.** Learn what the fidelity setting and the blend-back actually do.

**Steps.** Pick one face at least 64 px wide. Run CodeFormer at `w` 0.5, 0.7 and 0.9. Check `--help` for the flag names. Blend each result over the plain upscale at 40%, 50% and 60%, using a layer mask. Compare at 100%.

**Do not use GFPGAN's `-w` as a dial.** The repo accepts it and ignores it: outputs were bit-identical at 0, 0.5 and 1 [146][149]. This exercise uses CodeFormer's `w` only.

**Time.** 1 to 2 hours (estimate). The note's Q2 table says a GPU is recommended for CodeFormer, and CPU use is unconfirmed.

**What good looks like.** You can find a setting where the skin improves but the teeth, eyelids and jaw stay the same. If you cannot find one, the answer for that photo is no face restoration.

### Exercise 5: Paper-theatre push-in

**Goal.** A 4-second move on one photo, with no GPU and no invented pixels.

**Steps.** Pick a photo with a clear subject and background. Cut the subject out by hand in GIMP or Krita, or with `rembg` if it is installed. Make three layers: background, subject, and a foreground object if one exists. Add soft shadows. Move the layers with small transforms in Kdenlive or DaVinci Resolve. Or run the `zoompan` command from Step 8 (on Windows, the same command, untested on Windows). Keep the move to a 3 to 8% push-in.

**Time.** 2 to 3 hours (estimate).

**What good looks like.** The gaps are visible and plain. The move feels like depth. Nothing morphs or shimmers.

### Exercise 6: Morph between two real photos

**Goal.** A transition that says "time passed" with no generated frames.

**Steps.** Choose two real photos of the same person at different ages that are yours or public-domain (nobody is asked before the premiere, D-03). Align the eyes by scaling and rotating. Run the ImageMagick morph (14 frames; `magick` on Windows, see Step 7), and assemble it with ffmpeg. Make an `xfade` dissolve for comparison. If time allows, add landmarks using the LearnOpenCV example [65].

**Time.** About 2 hours (estimate).

**What good looks like.** The middle frames show ghosting on hair and background, not a new face. The clip is labelled L4a, and both end photos appear in the credits.

### Exercise 7: Label and credit one reconstruction

**Goal.** A labelled reconstruction with the right caption and metadata.

**Steps.** Write a one-page brief: what is known, what is invented, and which invented parts are generic. Choose the look (Route A). Write the caption "Reconstructed from [name]'s memory, [interview date]." Add a manifest row and a `steps.csv` entry with label L5. Add a line to the cue sheet. Optional: test the ExifTool command from Step 10 on a copy of one TIFF, then read the tag back. This was run on Linux only [105].

**Time.** 1 to 2 hours (estimate), not counting drawing.

**What good looks like.** The caption appears on screen and in the credits. The brief is saved. The record names the source and the date. If you ran the ExifTool check, the IPTC value reads back. If you did not, the step is marked TODO.

## Pitfalls

1. **Demos flatter.** Most public demos use clean, modern portraits. No source the research reached shows these tools on faded, low-resolution or black-and-white family prints. Treat any quality claim as untested until your bake-off.
2. **Restoration is generation.** Upscalers, face restorers and colourisers invent texture, features and colour. Frame makers invent frames. The tool tables in the research note say what each tool invents.
3. **Face drift and plastic skin.** GFPGAN may change identity [17]. SeedVR2 had a "plastic" output problem, which version 2.5.6 addressed [24]. Fake-face methods such as PULSE make people who do not exist [30]. Blend back, and check at 100% against the original (the maker is the only judge, W-40).
4. **Age gaps.** Face recognition accuracy falls by 10 to 17 percent for same-person pairs with age gaps, in a 2017 benchmark [53]. The note expects identity tools to pull a face toward the age of the reference photo. That is a reasoned expectation, not a tested result (judgment in the note). Do not expect one face to cover childhood to today. Use each photo's own face, one photo per output.
5. **Stale tutorials.** FILM was archived 2025-10-14 [61]. Microsoft's Old Photos repository was archived 2026-10-03 [25]. DeOldify was archived 2024-10-19 [29]. IP-Adapter-plus has been maintenance-only since 2025-04-14 [44]. The first Nano Banana model (`gemini-2.5-flash-image`) is marked deprecated with a 2026-10-02 shutdown on Google's pricing page [51]. The image docs call it only "legacy" [50]. That date has already passed, so assume it is gone and check before use. Check the dates and licence of any tutorial from 2023 to 2025.
6. **Licence traps.** Non-commercial weights need a licence read for public exhibition before use, and a ticketed showing excludes them (Decision 3). InfiniteYou's licence says "for academic research purposes only" [162], so it is out for any shown frame. FLUX.2 dev, FLUX.2 klein 9B [38] and InstantID [40] have no licence read yet (TODO(research)). The charter fixes a public premiere (Known facts; Principle 7).
7. **Fake sites and listicles.** The CodeFormer, FramePack and DepthFlow pages each warn that look-alike sites are unofficial or fraudulent [15][72][60]. Use the official repository or vendor page only.
8. **Cloud privacy.**
   - *Gemini consumer app, with Keep Activity on:* uploaded photos may be used to train models, and some chats are reviewed by people and kept for up to three years [84]. Never for family photos.
   - *Gemini API unpaid tier:* content is used to improve products, and the terms say not to submit personal information [85]. Never for family photos.
   - *Gemini API paid tier:* prompts and files are not used to improve products [85]. Not for family photos at any size (D-15); acceptable for stand-ins and non-family imagery only (Decision 6).
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
19. **AI deity images, even as placeholders.** Anything generated can leak into the cut, and the community has objected: the Hindu American Foundation's guidance says AI images "are not inherently sacred", and the Jagannath temple administration filed a police complaint in January 2026 over AI-generated videos of its deity (`playbooks/hindu-visual.md`, its sources 79, 83 and 84). No generative route touches a deity, not even for a storyboard (W-61).

### Known gaps (TODO(research))

- **No archival-photo evidence** for any generative edit tool. The week 1 bake-off on stand-ins tests the defects, not her photos. The real-photo line-up in the vertical slice tests her photos.
- **Restraint prompts** are the research note's synthesis, not tested by creators. The creator threads, YouTube and Reddit were not reached, because the search budget ran out.
- **Terms pages not read:** see Pitfall 8.
- **FADGI numbers.** The third-edition guidance on ppi, bit depth and colour sits in a PDF the research could not read [4]. The 600 ppi and 3200 to 4000 ppi figures are partly judgment.
- **Home video** (VHS, Hi8, MiniDV) and **8 mm film** were not researched.
- **VRAM** for FLUX.1 Kontext dev, Qwen-Image-Edit-2511, Wan FLF2V and Wan2.2 14B is not stated in any source read.
- **First-and-last-frame support and pricing** for Kling, Runway and Luma are unconfirmed.
- **Gemini 2.5 Flash Image.** The pricing page says deprecated with a 2026-10-02 shutdown; the image docs say only "legacy." The sources conflict.
- **C2PA signing** was not researched. ExifTool syntax and MP4 handling were run on Linux [105]. Windows runs are not done.
- **AI image models' rendering of Devanagari and Gujarati text** was not researched. Until it is, typeset every Indic string from a font and never accept generated text (`playbooks/cinematic-quality.md` T9 row 7; W-75).
- **DepthFlow's CLI documentation** (depth.tremeschin.com) was not fetched.
- **Windows set-up** for ffmpeg, ImageMagick, Real-ESRGAN, rembg, Depth Anything V2 and ExifTool is researched from vendor pages (Step 0), not run on Windows. CodeFormer's Windows route is not researched (TODO(research)).
- **Budget figures.** Resolved in round 1: the research summary now matches its table, 40 to 80 human hours (45 to 80 with no GPU).
- **Insiders list (`GATHER.md`)** is not needed under only-me (D-03): the maker judges likeness alone (W-40). If TD-L2c (Sun 3 Jan) ever brings someone in, write `GATHER.md` before anyone judges a likeness.
- **ArtCraft apps** (PhotoCraft, LightCraft and the rest) are outside this track. TODO(research): see the craft-visual and craft-motion tracks.
- **Open maker decisions:** whether the public premiere on 27 February is free or ticketed (Decision 3; the register's door-policy default is invite-only, W-54). The charter fixes the premiere as public; the price is open. Animating relatives who have died is settled for the premiere cut: no face or expression motion (Decision 4, W-40).
- **Licence text not read:** FLUX.2 dev, FLUX.2 klein 9B [38] and InstantID [40] (TODO(research)). Do not use them for a shown frame until read.

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
[17] GFPGAN (TencentARC) — https://github.com/TencentARC/GFPGAN — undated — v1.3 "have a slight change on identity" (README table); Apache-2.0.
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
[54] Retired under D-29 (a game-map tool); no longer cited.
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
[104] Local tests of the Real-ESRGAN ncnn Ubuntu build (2026-10-18) — `-h` text, missing-model behaviour, timings under Mesa llvmpipe software Vulkan, "invalid gpu device" without Vulkan.
[105] Local tests of ExifTool 13.59, ffmpeg 6.1.1 and ImageMagick 6.9.12 metadata handling (2026-10-18) — TIFF, MP4, MOV, sidecars.
[106] Local tests of rembg 2.0.85 (onnxruntime 1.31.0) and Depth Anything V2 Small via transformers 5.20.1, torch 2.14.1+cpu, Python 3.13.16 (2026-10-18).
[110] realesrgan-ncnn-vulkan-20220424-windows.zip — https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip — 45,474,481 bytes; contents listed.
[112] Real-ESRGAN README — https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/README.md — four portable models; general-x4v3 in Updates only.
[114] Veo 3.1 in the Gemini API (same page as [82]) — https://ai.google.dev/gemini-api/docs/veo — "Last updated 2026-10-08 UTC" — personGeneration table, limitations, safety; 1080p, 4K and reference images need 8 seconds (round-2 review's read, 2026-10-18).
[116] Veo responsible AI and usage guidelines (Vertex) — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines — last updated 2026-10-15 UTC — Child category support codes; input-image rejection text. The page text sits past a 100,000-character navigation block, so a first fetch looks empty; read past it (checked 2026-10-18).
[118] ExifTool install — https://exiftool.org/install.html — Windows executable steps; no Perl needed.
[120] ImageMagick download — https://imagemagick.org/download/ — 7.1.2-34; winget ids; portable; `vcomp140.dll` note; `magick` command; no release date shown.
[121] FFmpeg download — https://ffmpeg.org/download.html — 9.0.2 (2026-09-18), 8.1.3 (2026-09-21); Windows builds by gyan.dev and BtbN.
[122] Gyan.dev FFmpeg builds — https://www.gyan.dev/ffmpeg/builds/ — release 9.0.2, 2026-09-19; choco, scoop and winget commands.
[123] rembg — https://github.com/danielgatis/rembg — Python `>=3.11,<3.14`; pip extras; models download to `~/.rembg/models`; no Windows notes.
[124] Depth-Anything-V2 — https://github.com/DepthAnything/Depth-Anything-V2 — `run.py --encoder vits`; Small is Apache-2.0; no Windows notes.
[125] Depth-Anything-V2-Small-hf — https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf — Apache-2.0; 24.8M parameters; pipeline snippet.
[126] Install WSL, Microsoft Learn — https://learn.microsoft.com/en-us/windows/wsl/install — updated_at 2026-06-02; `wsl --install`; Windows 10 build 19041 or later.
[131] Commons file 80-G-27208 — https://commons.wikimedia.org/wiki/File:80-G-27208_(31323126572).jpg — US Navy, Nov 1942; public domain (federal work).
[132] Commons file NARA 546220 — https://commons.wikimedia.org/wiki/File:CHEMICAL_PLANTS_ON_SHORE_ARE_CONSIDERED_PRIME_SOURCE_OF_POLLUTION_-_NARA_-_546220.jpg — EPA DOCUMERICA, June 1972; public domain.
[133] Commons file 1971-12-John Call Cook — https://commons.wikimedia.org/wiki/File:1971-12-John_Call_Cook.jpg — CC BY-SA 3.0; 3,007x3,971.
[134] Commons file Clara MEEKINS 1952 — https://commons.wikimedia.org/wiki/File:Clara_MEEKINS,_1_year_old,_1952,_in_front_of_the_house_on_South_Street,_Raleigh,_NC,_where_she_was_born._People_visible_sitting_on_the_porch_of_the_house_are_all_family._Clara_remembers_they_would_(26480797321).jpg — State Archives of North Carolina via Flickr Commons; "No known copyright restrictions".
[146] GFPGAN source, raw files on `master` (read 2026-10-18) — https://raw.githubusercontent.com/TencentARC/GFPGAN/master/inference_gfpgan.py ; …/gfpgan/utils.py ; …/gfpgan/archs/gfpganv1_clean_arch.py ; …/gfpgan/archs/gfpganv1_arch.py ; …/gfpgan/archs/restoreformer_arch.py — `-w` defined; `weight` goes to `**kwargs` and is never read.
[147] GFPGAN README (raw) — https://raw.githubusercontent.com/TencentARC/GFPGAN/master/README.md — v1.4 "slightly more details and better identity than V1.3"; V1.3 table "slight change on identity"; RestoreFormer inference added.
[149] Local runs, 2026-10-18: GFPGAN v1.3, v1.4 and RestoreFormer weights through the repo's own architecture files, on CPU; `weight` unset, 0.0, 0.5 and 1.0 gave identical outputs. Weight hashes are in the research note's [149].
[151] DDColor repository, `git clone --depth 1` at commit 2adb63f2656ac41cbdf7b894cddd94121a3faf13 (2026-01-18) — https://github.com/piddnad/DDColor — `ddcolor/pipeline.py` concatenates the input L with the predicted ab channels; Apache-2.0.
[153] Local run, 2026-10-18: DDColor `piddnad/ddcolor_paper_tiny` on CPU through `ColorizationPipeline`; four scikit-image test images; ΔL measurements (tiny model only).
[156] Digital Cinema System Specification v1.4.4, DCI, approved 2024-01-03 — https://documents.dcimovies.com/DCSS/42cfeb997ae72dd484f7b027547e6e0bfad43ecf/Digital%20Cinema%20System%20Specification.pdf — read as text: 2K 2048x1080 at 24 or 48 FPS; 4K 4096x2160 at 24 FPS.
[159] FLUX.1 [dev] Non-Commercial License v1.1.1 — https://raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev — read in full 2026-10-18; names FLUX.1 Kontext [dev].
[161] SUPIR licence and README — https://raw.githubusercontent.com/Fanghua-Yu/SUPIR/master/LICENSE ; …/README.md — read in full 2026-10-18; "Commercial Use" definition; Non-Commercial Use Only Declaration.
[162] InfiniteYou — https://raw.githubusercontent.com/bytedance/InfiniteYou/main/README.md ; https://huggingface.co/ByteDance/InfiniteYou/raw/main/README.md — read 2026-10-18; "for academic research purposes only".
[166] GNU Affero General Public License v3 — https://www.gnu.org/licenses/agpl-3.0.txt — read 2026-10-18; sections 0, 2 and 13.
[168] U-2-Net LICENSE (Apache-2.0) — https://raw.githubusercontent.com/xuebinqin/U-2-Net/master/LICENSE ; rembg `LICENSE.txt` (MIT) — https://raw.githubusercontent.com/danielgatis/rembg/main/LICENSE.txt.
[100] They Shall Not Grow Old (Wikipedia) — https://en.wikipedia.org/wiki/They_Shall_Not_Grow_Old — undated — restoration, colourisation, criticisms.
[102] Local sandbox test (this session, 2026-10-18) — ffmpeg 6.1.1 and ImageMagick `convert`; commands `convert a.png b.png -morph 14`, `ffmpeg ... xfade`, `zoompan`, `minterpolate=fps=48:mi_mode=mci`, and frame-sequence assembly ran without error on synthetic images; confirms the commands run, not that results are good on real faces.

## Changelog

- 2026-10-18: Version 1, written by the haiku scribe from `research/ai-imagery.md` (sources read 2026-10-18) and `CHARTER.md`. Open gaps are listed under Pitfalls as TODO(research). Each decision lean is marked either "from the note" or "scribe's reading, confirm."
- 2026-10-18, round 1 (Fable review applied by the Haiku scribe): added Windows forms and the install route (C1); moved the bake-off to stand-in photos judged by the maker and confirmed insiders, with real photos moved to the vertical slice (C2); fixed the IPTC mapping for hand-made work; made the L2 face rule operational and added "When not to restore"; corrected the Real-ESRGAN command, FramePack GPU wording, budget and metadata notes; added the child-photo cloud limit; replaced the fixed 2026 caption date with the interview date.
- 2026-10-18, round 2 (Fable review applied by the Haiku scribe): C1 fixed, with Decision 3 and the licence default reframed as free public screening versus ticketed, because the charter now fixes a public premiere. Colourised faces ruled L2 or L3 by a Lab L-channel test. GFPGAN `-w` recorded as having no effect, so CodeFormer's `w` stays the dial, and the v1.3 quotation corrected. Upscale rule keyed to the UHD master arithmetic (TODO(theatrical-delivery)). Cloud split by content. Veo costs and clip lengths restated for 4 s and 8 s, and the child-photo test dropped.
- 2026-10-18, round 3: Reconciled with DECISIONS.md (2026-10-18): likeness and review are the maker's alone (no insiders, no GATHER.md; D-03, W-40); master settled at 1080p with stills at 3840 px and a derived 2K DCP (W-15); cloud policy restated as decided (`cloud: none`, no family photo to any hosted service or rented GPU; D-15, W-23, W-24); backup is a second encrypted SSD with no cloud copy (W-25); no face or expression motion for the dead in the premiere cut (W-40); no model trained on her face (D-16); voxel only as original assets, never the marker (D-23, W-38); L5 testimony and `interview_date` under only-me (W-49); `zoompan` marked proof-grade (W-41); door policy and scanner defaults linked (W-54, W-27).
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): the game-style block look and its tools retired (D-29); Route A follows W-38 decisions 2 and 6; no generative route for a deity, with the deity-image label rule and the `deity_form` and `deity_source` columns (W-61; the Step 9 and Step 10 deltas of `playbooks/hindu-visual.md` and `playbooks/pushtimarg-world.md`); the AI-deity pitfall and the Indic-text gap; on-screen tags follow the phone-safe frame (W-63); P-LOCK replaces the old process-lock spelling.
