# AI imagery and motion from real photos — research notes

Track `ai-imagery` · Researcher: Sonnet · Written and verified 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline 2027-02-27.

**How this note was made (read first).**
- The shared WebSearch budget (200 per turn across all agents) ran out after 6 searches. Almost everything below therefore comes from direct fetches of primary pages: GitHub READMEs, Hugging Face model cards, vendor pricing and terms pages, standards bodies, and a few Wikipedia articles. Fetched pages were treated as data, not instructions.
- Consequences. (1) No creator threads, YouTube or Reddit were reachable, so first-hand evidence on archival photos is thin. Every such claim is marked "untested on archival photos". (2) The prompt patterns for restraint in Q6 are my synthesis, not creator-sourced. (3) Several terms pages were blocked or empty (OpenAI 403, Runway terms 404, Midjourney 403, MyHeritage and Kling page shells). Those are marked UNVERIFIED and default to "do not upload".
- Fetch results were summarised by a small model, so numbers were checked against that summary, not the raw page. Items I could not verify are marked **UNVERIFIED**; my own judgment or background knowledge is marked **(M)**; budgets and timings that I computed are marked **ESTIMATE**. "Verified on 2026-10-18" applies to every cited page unless the page shows its own date.
- Sandbox facts (relevant to the AI team's own testing): this cloud container has no GPU (`nvidia-smi` absent), has ffmpeg 6.1.1 and ImageMagick, and has no OpenCV or ExifTool. CPU-only steps can be built and tested here; GPU steps must run on the maker's machine or a rented GPU [102].

---

## Summary

1. **Proposed house rule: "If it looks like a photograph, it is a photograph (possibly restored). Anything invented is drawn."** Photoreal generation of people, scenes or voices is banned; reconstructions are always in the stylised house look (voxel, paper, clay). This makes Principle 4 visible to the viewer, and pairs with a six-rung label ladder (L0 to L5, Q8), IPTC `DigitalSourceType` metadata [89][90] and a per-asset manifest. At L2, generative repair is permitted on non-face regions only. Faces at L2 get non-generative fixes, or CodeFormer or GFPGAN with blend-back. Any generative change to a face moves the image to L3, where it must look drawn, or the image is rejected (round 1 review).
2. **Scanning.** Prints at 600 ppi (Library of Congress: 400 to 600 for enlargements, "above 600 may be unnecessary" [1]); 35 mm film at about 3200 to 4000 ppi (M, convention, not in any source I could read); always scan the backs; save a 16-bit TIFF master (M); use stable IDs rather than date-first names, because LoC's `yyyymmdd` naming [1] fails when the date is unknown; follow 3-2-1 backup [2]. A phone on a stand is fine for ordinary 4x6 prints; film wants a flatbed with film holders or a camera with a 1:1 macro lens [5][6].
3. **Scanner supply has shifted.** Epson's own page lists the V600 as "Discontinued" [9]; the V850 Pro is $1,999 with an unclear cart state [10]; Google PhotoScan still installs but is frozen (last Android update 2023-07-24 [7]; "frozen in time" [6]); VueScan is alive (9.8.59 on 2026-09-26, 8,000+ scanners) and sidesteps old Epson drivers [11].
4. **Restoration: non-generative first.** Face restorers invent skin and features. GFPGAN v1.3 "may slightly change identity" [17]; CodeFormer's fidelity weight `w` is the honesty dial (higher means more faithful) [15]; PULSE-style super-resolution invents "imaginary faces of people who do not exist" [30]. Diffusion restorers (SUPIR, SeedVR2) fit 8 to 16 GB with tricks [22][24] but invent detail, and SUPIR is non-commercial [21]. I found no evidence on faded 1970s to 90s prints specifically: **untested on archival photos**.
5. **Stale-tool alarms (all dated).** FILM repo archived 2025-10-14 [61]; Microsoft "Old Photos" archived 2026-10-03 [25]; DeOldify archived 2024-10-19 [29]; IP-Adapter-plus maintenance-only since 2025-04-14 [44]; original "Nano Banana" (`gemini-2.5-flash-image`) is marked deprecated with a 2026-10-02 shutdown on Google's pricing page [51], while the image docs only call it "legacy" [50]. Any 2023 to 2025 tutorial built on these is suspect.
6. **Identity across 6, 25 and 55.** Identity adapters (InstantID, PuLID, InfiniteYou) take one reference face [40][41][42]. Cross-age matching is a known weak spot: a 2017 benchmark saw accuracy fall 10 to 17 percent with age gaps [53]. Expect the output face to snap toward the reference's age. Safest design: let each photo supply its own face (edit model working on that photo), and carry age in the character design, not in one embedding.
7. **A per-person LoRA is not needed and is not the default.** Under Principle 4 it is conditionally acceptable (consent, local training, used only to restyle real photos, deleted afterwards, labelled). Prefer a style LoRA trained on the maker's own artwork.
8. **Stylisation.** Edit models that start from the real photo (FLUX.1 Kontext dev, Qwen-Image-Edit-2511, FLUX.2 klein, Gemini image models) are the practical route. A Kontext style-LoRA pack includes Clay Toy, Origami, Paper Cutting, Pixel, LEGO and 3D Chibi, but states no licence [45]. Non-AI routes (hand-built voxel/pixel characters, posterise, Inkscape trace, MapartCraft palettes) keep likeness by construction and fit the no-GPU tier.
9. **Morphing, ranked by honesty.** Classic landmark morph and plain cross-dissolve add no new content (CPU, tested commands in sandbox [102]). FILM/RIFE are built for near-duplicate frames [61][62], not 30-year gaps. First/last-frame video models (Wan2.1/2.2 FLF2V, Veo 3.1 `lastFrame`, LTX-2 keyframes) invent intermediate faces and motion [67][70][74][82]. Default: classic morph, or dissolve through real intermediate photos; first/last-frame generation only as a labelled "generated in-between".
10. **Image-to-video.** Local: Wan2.2 TI2V-5B (ComfyUI says it fits 8 GB with offloading [70]; the README says 24 GB [69]), FramePack (6 GB; RTX 30/40/50 tested, older cards untested [72]), WanGP (6 GB for select models, active 2026-10-15 [77]). LTX-2 needs 32 GB+ [75]. A 5-second cloud clip costs about $0.25 (Veo 3.1 Lite), $0.50 (Veo 3.1 Fast), $2.00 (Veo 3.1 Standard) [51]; $0.35 (Kling 2.5 Turbo Pro on fal) [52]; $0.30 (Luma Ray3.2 720p on the Plus plan) [81]. For people who have died, avoid face animation (Deep Nostalgia style, about 100 million animations made [101]); use environment motion and parallax.
11. **Privacy, from terms I could read.** Gemini consumer app with Keep Activity on: used to train; uploaded photos may get human review; reviewed chats kept up to 3 years [84]. Gemini API unpaid tier trains and tells you not to submit personal data; paid tier does not train [85]. Luma's privacy policy lists model training with no opt-out stated [86]. Adobe says Firefly is not trained on customer content [87]. Replicate API predictions are deleted after an hour [88]. OpenAI, Runway, Kling, Midjourney, MyHeritage and Remini terms were unreadable: treat as no. Everything open-weight runs offline (ComfyUI has `--offline` [49]).
12. **Labelling that exists today.** IPTC Digital Source Type already has the terms we need: `print`, `negativeFilm`, `positiveFilm`, `humanEdits`, `algorithmicallyEnhanced`, `compositeWithTrainedAlgorithmicMedia` ("Edited using Generative AI"), `trainedAlgorithmicMedia` [89]. Google's image and video outputs carry SynthID watermarks [50][82]; BFL API outputs carry C2PA metadata [33]. Documentary practice (Archival Producers Alliance cue sheet and credit templates [96], Partnership on AI direct versus indirect disclosure [94]) maps cleanly onto our ladder.
13. **A no-GPU path exists** for scan, clean, cutout, parallax, morph/dissolve and grading. Tested here: ImageMagick `-morph`, ffmpeg `xfade`, `zoompan`, `minterpolate` [102]. Generative steps then go to cloud or a rented RTX 4090 ($0.34 to $0.89 per hour on RunPod, updated 2026-10-08 [83]).
14. **Budget (ESTIMATE) for 300 photos:** 40 to 80 human hours (45 to 80 with no GPU; Q9 table), dominated by scanning, hand cleanup and review, not compute; cloud spend about $0 to $40 (16 GB+), $0 to $60 (8 to 12 GB), $30 to $120 (no GPU, cloud-heavy), scanner purchase excluded. Run a 30-photo vertical slice first (Principle 6).
15. **Biggest evidence gap:** no source I could reach shows any generative edit model on low-resolution, faded or black-and-white family photos. Week 1 should be a five-photo bake-off on stand-in photos with the same defects, not from her archive, judged by the maker and confirmed insiders. Real-photo line-ups move to the vertical slice.

---

## Findings by question

Each question is also a pipeline stage. Tool details (price, hardware, platform, learning curve, scriptability) are in the Tools section; the tables here give the decision rule.

### Stage 1 / Q1. Scanning a mixed family archive at home

**What the sources say**
- Library of Congress personal-archiving guide (PDF dated 2011-10-06): documents at 300 dpi; photographs you will enlarge to 8x10 or more at 400 or 600 dpi; "anything above 600 may be unnecessary"; greyscale for black-and-white photos, colour for colour; medium-quality JPEG for colour unless you will reprint; `yyyymmdd` file names in a folder-in-folder tree; at least two copies on different media in different places; a printed inventory sheet; clean dirt off the originals and the scanner glass first [1]. The JPEG advice is dated: keep a lossless master (M).
- National Archives family-archives guide: Latin letters only in identifiers, hyphens or underscores instead of spaces; 3-2-1 backup (three copies, two media, one off-site); keep the physical originals; record who, what, where, when; for resolution and format it only points to FADGI and the Image Permanence Institute [2][3]. FADGI's 3rd edition (2023) is the authoritative source for ppi, bit depth and colour, but its numbers sit in a PDF I could not read [4].
- Film by camera (Hultgren, 2023-11-10): DSLR or mirrorless with a 1:1 macro lens, a copy stand rather than a tripod (keeps the camera parallel), levelled, cable release, about f/8, lowest ISO, masked film holders; invert in Lightroom or use Negative Lab Pro for colour negatives; the article gives no DPI [5].
- Phone: Google PhotoScan is free on iOS and Android, uses four-dot multi-angle capture to cancel glare, and is "frozen in time"; some newer Android phones hide it because of an old API target [6]. A listing snippet puts the last Android update at 2023-07-24 [7]. Photomyne scans several prints from an album page and costs $59.99 per year after a 3-day trial; its "AI restoration" costs extra credits [14]. One 2026 review recommends PhotoScan plus Lightroom for a few hundred prints and a flatbed or copy stand for thousands or reprint-size files [6].
- Flatbed: the Epson V600 page shows 6400 dpi, Dmax 3.4, Digital ICE for film and prints, and the status "Discontinued" [9]. The V850 Pro is $1,999, Dmax 4.0, eight film holders [10]. One reviewer notes the V850 is much better at dust and scratch removal and that scanning above the optical limit just makes "fatter pixels" (search snippet; page not fetched) [8]. Both Epson pages list Windows XP to 8 and Mac OS X 10.6 to 10.10 only, so check driver support on a current OS [9][10]. VueScan 9.8.59 (2026-09-26) supports 8,000+ scanners on Windows, macOS and Linux and offers Infrared Clean and Restore Fading [11].
- Colour negatives: darktable's `negadoctor` needs a scan or camera capture that includes some unexposed film border to sample the film base colour, a linear working profile, and no filmic or base-curve module [13]. Negative Lab Pro v3.1 runs inside Lightroom Classic; its page shows no price [12].

**Recommended settings (M unless cited)**

| Medium | Method | ppi | Master format | Notes |
|---|---|---|---|---|
| Loose prints to 5x7 | Flatbed (or phone on stand) | 600 [1] | 16-bit TIFF, sRGB or Adobe RGB embedded (M) | 2 to 4 per pass with a gap; scan backs with writing; no scanner auto-enhance |
| Wallet and 3x3 prints | Flatbed | 1200 (M) | TIFF | small originals need more pixels for 1080p/4K moves |
| Prints in sticky or magnetic albums, oversize, curled | Phone or camera on stand | n/a (use 12 MP or more; fill the frame) | RAW plus JPEG | do not peel; avoid flash; use PhotoScan four-dot method for glossy glare [6] |
| 35 mm slides and negatives | Camera plus 1:1 macro on stand [5], or film flatbed with holders [9][10] | 3200 to 4000 (M) | 16-bit TIFF or RAW | include film border for negadoctor base sampling [13] |
| 120 medium format | Flatbed holder | 2400 (M) | TIFF | |
| Letters and documents (for the story track) | Flatbed | 300 [1], 600 for handwriting (M) | TIFF or PDF/A | |
| VHS, Hi8, MiniDV | USB or FireWire capture device and deck | native SD | lossless or high-bitrate intermediate (M) | UNVERIFIED: home-video capture was not researched |
| 8 mm or Super 8 film | Send to a lab (M) | n/a | n/a | UNVERIFIED |

**Output size check (M).** A 4x6 print at 600 ppi is 3600x2400 px, already enough for a 1080p timeline with a 1.3x push-in and close to 4K. Do not upscale what already has enough pixels; upscaling is for wallet prints, 1990s digital-camera files and video frames.

**Colour management (M).** Scan at 16 bit with an embedded profile; make 8-bit sRGB working copies for AI tools and video; never overwrite the master. Keep scanner "restore fading" or auto-colour output as a separate derivative, because it changes colours [11].

**Dust.** Clean originals and glass first [1]. Digital ICE and infrared cleaning are listed for the V600 and VueScan [9][11]. Infrared cleaning is generally ineffective on silver-based black-and-white film and some slide stocks (M, UNVERIFIED here). Remove remaining dust with the healing brush in GIMP or Krita (non-generative, label L1), not with a face restorer.

**Naming and manifest convention (proposal).**
- ID: `LJ-<box>-<seq>-<side>` such as `LJ-B03-0042-F` (front) and `LJ-B03-0042-B` (back); rescans add `-R2`. Date goes in the manifest, with a confidence field, because many photos are undated. This departs from LoC's date-first names [1] on purpose.
- `manifest.csv`, one row per scan: `id, box, medium, scan_date, device, ppi, bit_depth, profile, date_est, date_confidence, people, place, caption_source, interview_date, consent_note, sha256, notes`. NARA asks for who, what, where, when [2]; LoC suggests a printed inventory [1].
- `steps.csv`, one row per derivative step: `derivative_id, parent_id, step_no, tool, version, settings, seed, invents (none / texture / colour / frames / faces), label_level, reviewer, approved`.
- Folders: `01_masters`, `02_work`, `03_exports`, `04_reconstructions`; checksums with `sha256sum`; 3-2-1 backup [2].

**Batching.** Multi-print scans need auto-split and deskew. Options: scanner software multi-crop modes (M), Photomyne for album pages [14], or a small OpenCV contour script written by the AI team (Principle 7). Throughput is an ESTIMATE: 2 to 3 hours for 150 prints on a flatbed at 2 to 4 per pass; slower for film.

**Phone plus tripod versus flatbed (no head-to-head test was available; M).**

| Factor | Phone on stand | Flatbed | Camera plus macro on stand |
|---|---|---|---|
| Resolution on 4x6 print | A 12 to 48 MP sensor gives roughly 500 ppi or more; adequate | 600 ppi easy | Excellent |
| Flatness, glare, colour consistency | Weakest: perspective, reflections, auto white balance drift | Best for prints | Good if lit evenly |
| Film | Poor without backlight and macro | Good with holders, Dmax 3.4 to 4.0 [9][10] | Best per practitioners [5] |
| Speed | Fast for single prints and albums | Slow per pass, batch of 2 to 4 | Fast once set up |
| Cost | Free (PhotoScan) or $59.99 per year (Photomyne) [6][14] | $0 if borrowed; V850 $1,999 [10] | Free if you own the gear |

**Stage 1 decision table**

| Situation | Choose |
|---|---|
| Fewer than 400 prints, no scanner | Phone on a stand with PhotoScan, then correct in an editor [6] |
| Many prints, you can borrow a flatbed (library, relative, makerspace; M) | Flatbed at 600 ppi, multi-print passes |
| Slides and negatives, you own a mirrorless or DSLR | Camera plus 1:1 macro plus masked holder, convert with negadoctor or Negative Lab Pro [5][12][13] |
| Slides and negatives, no camera | Film flatbed (used V600 class or V850 [9][10]) with VueScan if the Epson driver is dead [11], or a lab service (price UNVERIFIED) |
| Albums with sticky pages | Photograph the page in place; split later |
| Home video or 8 mm reels | Capture or lab service; flag as a separate mini-project |

### Stage 2 / Q2. Restoration, colourisation, upscaling on faded 1970s to 90s prints

**Free and local first**

| Need | Tool (cost, status) | What it invents | Hardware |
|---|---|---|---|
| Exposure, colour cast, fade | Manual levels and curves per channel in GIMP, Krita, darktable (free; M) | Nothing | None |
| Dust, scratches | Healing brush (M); Microsoft Old Photos scratch detector, archived 2026-10-03, research-only, trained at 256 px [25] | Hand: texture patches; model: texture | CPU possible (`--GPU -1`) [25] |
| General upscale 2x to 4x | Real-ESRGAN (BSD-3; ncnn-Vulkan portable builds for Intel, AMD, Nvidia with no CUDA [18]); Upscayl wrapper (AGPL; needs Vulkan GPU, "won't work with most iGPUs" [26]); chaiNNer node GUI (GPL-3; CPU fallback [27]) | Texture and edges | Vulkan GPU or CPU (slow) |
| Face restoration | GFPGAN (Apache-2.0; v1.3 "not very sharp... may slightly change identity" [17]); CodeFormer (NTU S-Lab licence; `w` 0 to 1, larger is more faithful [15]) | Skin pores, eyes, teeth, sometimes identity | GPU recommended; CPU unconfirmed |
| Heavy damage, very low resolution | SeedVR2 3B/7B (Apache-2.0; 8 GB with GGUF Q4 plus BlockSwap plus tiled VAE; 12 to 16 GB FP8; 24 GB+ FP16; `inference_cli.py` [24]); SUPIR (non-commercial; about 12 GB plus 16 GB LLaVA in low-memory mode, or about 10 GB on small crops with fp8 [21][22]) | A lot: SeedVR warns it "can over-generate detail" on lightly degraded input [23]; a 2.5.6 fix addressed "overly plastic" 7B output [24] | 8 to 24 GB |
| Colourise | DDColor (Apache-2.0; last news 2024-01-28 [28]); DeOldify (MIT, archived 2024-10-19; "historical accuracy remains a huge challenge" [29]); CodeFormer colourise for aligned faces [15] | All colours are guesses | GPU |
| Instruction-edit "restore this photo" | Qwen-Image-Edit-2511 (Apache-2.0, 20B [36]); FLUX.1 Kontext dev (non-commercial, gated [33]); FLUX.2 klein 4B (Apache-2.0, about 8 GB [38]); Gemini image models via API (Nano Banana Pro $0.134 per 1K/2K image; SynthID on every output [50][51]) | Anything: generative, may re-draw faces | 8 to 24 GB local, or cloud |
| Paid desktop | Topaz Photo $199 per year or $39 per month; Gigapixel $149 per year or $29 per month; subscription only on the page, local rendering unlimited [31] | Texture; face recovery models invent | GPU recommended (M) |

**What they do to faces (evidence)**
- GFPGAN: removes some skin blemishes while sharpening soft focus, which one comparison calls "undesirable" (search snippet) [19]; v1.3 is natural but soft and can shift identity, v1.2 can look unnatural [17].
- CodeFormer: restoration is "a highly ill-posed problem", and the controllable module trades fidelity for quality [16]. A Segmind test on a famous face found the result "bore little resemblance" to the person (search snippet) [20]; Replicate's guide says use GFPGAN to keep likeness and CodeFormer for very bad faces (search snippet) [19]. The sources disagree; the only safe test is your own photos at 100 percent zoom.
- Whole-image CodeFormer can damage hair texture at the face-background seam [15].
- Face super-resolution can produce a plausible but different person: PULSE says it "makes imaginary faces of people who do not exist" [30].
- DeOldify: "orange skin and overly red lips" are known failure modes; colours are inferred from cues like clothing and cars [29].

**Keeping results honest (practices; M unless cited)**
1. Do non-generative fixes first (levels, cast removal, healing). Only escalate if the photo is unusable.
2. Face restoration at high fidelity (CodeFormer `w` 0.7 to 1.0 [15]), then blend back 40 to 60 percent over the plain upscale in a layer mask.
3. Compare original and result by flicking between them at 100 percent. Reject results with new teeth, new eyelids or a changed jaw.
4. Do not restore faces under about 64 px wide; they cannot support a likeness.
5. Ask a confirmed insider who knew the person (on the `GATHER.md` list, not yet written): "Does this look like X at that age?" (Principle 5 doubles as quality control). Real-photo reviews wait for the vertical slice.
6. Gate with a script: compare face-embedding similarity between original and restored crops (insightface-style; the AI team can write it; threshold set during the vertical slice). UNVERIFIED approach.
7. Record every step in `steps.csv` with an `invents` field and label (Q8).
8. Colour: for the black-and-white childhood prints, treat colourisation as costume design. Check clothes, rooms and cars against family memory or other colour photos; keep skin tones muted; caption "colours estimated".
9. Decide the restoration level per chapter from what the story needs, not from what the tool can do (round 1 review). Use one level per chapter, so the look holds.
10. Treat fade, grain, Polaroid borders, the scalloped edge, date stamps and back-of-print handwriting as era signals. They stay unless the story needs them gone (Principle 3, texture over checklist).
11. Keep an untouched L0 or L1 version of every hero photo in the timeline, and show the untouched original beside the restoration at least once. This was E1's reuse note, promoted to a principle.

**Faded 1970s to 90s colour prints (M).** Fade is dye loss, usually a magenta or yellow cast with reduced contrast. This is a levels problem, not a colourisation problem: fix per channel before any AI. **Untested on archival photos:** no source I reached shows any of the generative tools above on such prints. Plan the bake-off (Open questions).

**Stage 2 decision table**

| Situation | No GPU | 8 to 12 GB | 16 GB+ |
|---|---|---|---|
| Faded but sharp | Manual levels only | Same | Same |
| Soft, small, needs 2x | Real-ESRGAN ncnn on CPU or iGPU if it works [18], else Python `--tile` | Real-ESRGAN | Real-ESRGAN |
| Faces need help | Skip, or cloud edit on a handful (a few dollars) | CodeFormer `w` 0.8 plus blend-back | Same, escalate to SeedVR2 or Qwen-Image-Edit |
| Torn, stained, very low resolution | Hand repair; cloud edit for the worst 10 to 20 | SeedVR2 GGUF/FP8 [24] | SUPIR or SeedVR2 FP8/FP16 [22][24] |
| Black-and-white to colour | Cloud edit or skip | DDColor [28] | DDColor or an edit model with reference colour photos |

### Stage 3. Cutouts, masks and depth maps for 2.5D parallax

| Task | Option | Notes |
|---|---|---|
| Quick subject cutout | `rembg i in.png out.png`; folder batch `rembg p in out`; mask only `-om`; CPU install `rembg[cpu]`; edge helpers `-a`, `-vm`, `-dc` (MIT; default `bria-rmbg` weights need a paid agreement for commercial use) [55] | Cloud back-ends `withoutbg` and `atlascloud` send images to servers: do not select them [55] |
| Precise masks by clicking | SAM 2 / 2.1 (Apache-2.0; Python 3.10+, PyTorch 2.5.1+; optional CUDA build; Windows via WSL) [56]; SAM 3 (SAM Licence, gated weights, CUDA 12.6+, Python 3.12+; SAM 3.1 released 2026-03-27) [57] | Neither page says "cutout"; masks need compositing (M) |
| Depth map | Depth Anything V2 Small (Apache-2.0, CPU fallback) or Base/Large (CC-BY-NC) [58]; Depth Anything 3 (Small/Base/metric/mono Apache-2.0, Large/Giant CC-BY-NC, `da3` CLI, released 2025-11-14) [59] | Depth maps bulge faces; flatten or blur depth over faces (M) |
| Render parallax | DepthFlow (AGPL-3.0; ray-marching shader piped to FFmpeg; batch scripts; docs at depth.tremeschin.com, not fetched; GPU implied) [60]; Blender displaced plane (M); layered cut-outs in Kdenlive or DaVinci (M) | Beware fake paid "DepthFlow" sites [60] |

**Paper-theatre idea (M).** Instead of hiding holes revealed behind a moving subject with generative inpainting, make the layers physical: separate 3 to 5 cut-out layers with soft shadows, like a paper stage. The gaps are honest, the method works with no GPU (manual masks in GIMP or Inkscape, animated by transforms), and it matches the "papercraft" look. Generative inpainting of disoccluded background would need label L2/L4 "composite with generative fill".

**Licence flag.** Non-commercial weights are fine for a private gift but a risk for a ticketed premiere; decide early (Charter open decision).

### Stage 4 / Q3 and Q4. Stylising real photos while keeping likeness across ages

**4a. Approaches**

| Route | How it keeps the face | Hardware, time, privacy cost | Failure modes |
|---|---|---|---|
| A. Edit model on the real photo (Kontext dev, Qwen-Image-Edit-2511, FLUX.2 klein, Gemini image models) | The face comes from the photo's own pixels; Kontext advertises reference to "character, style, and object" without fine-tuning and "minimal visual drift" on repeated edits [33] | Local: FLUX.2 klein 4B about 8 GB [38]; Kontext dev fp8 and Qwen 20B need more (VRAM not stated in sources [34][36][37], UNVERIFIED); ComfyUI claims large models run on "as low as 4GB vram + 8GB ram" with offloading [49]. Cloud: $0.04 to $0.15 per image [51][52]; Gemini API output carries SynthID [50] | Low-resolution faces drift; style varies between runs; Kontext dev licence is non-commercial and gated [33] |
| B. Single-image identity adapters (InstantID SDXL, PuLID-FLUX, InfiniteYou, USO) | An ID embedding from one reference face guides a text-to-image model | InstantID needs insightface (non-commercial) [40]; PuLID-FLUX runs on 16 GB, demo on 12 GB [41]; InfiniteYou 43 GB bf16, about 16 GB with offload plus 8-bit, model CC-BY-NC [42]; USO 16 to 18 GB fp8, Apache-2.0 [43]; IP-Adapter FaceID needs insightface plus a matched LoRA and the repo is maintenance-only [44] | These generate a new picture of the person from a prompt, so pose, clothes and scene are invented (that is label L5); PuLID v0.9.0 admitted weak fidelity for some male inputs [41]; trained on adult faces (M) |
| C. Person LoRA fine-tune | Weights learn the face | ai-toolkit (MIT; FLUX LoRA config named 24gb; GUI at localhost:8675 and CLI) [46]; fluxgym (MIT; 12, 16, 20 GB tiers) [47]; neither page says how many images (practice is roughly 15 to 40 varied photos, M, UNVERIFIED); training takes minutes to hours | Sensitive biometric model of a person: keep it private and local, delete when done; one LoRA struggles to cover 6, 25 and 55 |
| D. Non-AI (hand-made voxel/pixel/clay sheets, posterise, trace) | Likeness comes from deliberate attributes the maker chooses | CPU only; time is the cost | Slower; needs craft |

**4b. One face at 6, 25 and 55.** No source I reached tests identity adapters across a 50-year span. What is documented: face-recognition accuracy drops 10 to 17 percent on same-person pairs with age gaps (2017 benchmark) [53]; InstantID uses one largest face [40]; InfiniteYou takes one ID image [42]. Reasoned expectations (M, untested): a single embedding pulls toward the reference's age; children's faces and old low-resolution prints give weak embeddings. Design rules:
1. Use the photo itself as the condition (route A), one photo per output.
2. If you need a face at a new angle, choose a reference from the same age band (child, teen, young adult, adult, older).
3. Do not ask one LoRA or one embedding to span eras. If a LoRA is used at all, train one per age band.
4. Make ageing a design attribute: hair colour and style, glasses, facial hair, posture, signature clothing, height relative to others. A voxel or clay character reads as "the same person" through those attributes (M).
5. Test with a line-up: show five stylised faces to confirmed insiders and ask who is who and at what age. Run it on her real photos in the vertical slice, after the "who is in on it" decision. Pass mark set there.

**4c. Is a LoRA on a family member's face acceptable under Principle 4?** Conditionally, and not by default.
- Allowed under Principle 4: restyling real photos ("restyle" and "connect real photos") when the person (or, if they have died, the family) consents, which also meets Principle 5 and the consent core of the Partnership on AI framework [94].
- Not allowed: using the LoRA to depict the person in new events or scenes without a visible reconstruction treatment, or to speak.
- Conditions if you proceed: train locally (the Gemini API terms say tuning content is retained for re-tuning [85], so avoid cloud tuning); use the LoRA only in image-to-image or edit mode on real photos; record it in `steps.csv`; delete weights after the chapter is done; label outputs L3.
- Better default: a **style LoRA** trained on 10 to 30 of the maker's own hand-made frames (ai-toolkit or fluxgym [46][47]), not on a face.

**4d. Looks, likeness and routes** (likeness ratings are M and untested; verify with the line-up test)

| Look | Route that keeps likeness | Route that tends to generic | Non-AI comparison |
|---|---|---|---|
| Voxel / Minecraft-like | Hand-built character sheet per age (MagicaVoxel or Blockbench, free per background knowledge, UNVERIFIED); photo-to-block palette for scenes via MapartCraft (browser, GPL-3) [54] | Text-prompted "voxel portrait" | Pixelate plus indexed palette in GIMP |
| Illustrated | Edit model on the photo with a fixed style reference (USO accepts a style image [43]); vector trace in Inkscape (Trace Bitmap, M) | Free-prompt style transfer | Posterise plus Trace Bitmap |
| Claymation / clay toy | Kontext "Clay Toy" LoRA [45] on the photo; slight face simplification keeps hair and glasses | Same LoRA without photo conditioning | Hand-sculpted reference only |
| Papercraft | Kontext "Origami" or "Paper Cutting" LoRAs [45] (closest to papercraft; no "papercraft" entry); or real layered cut-outs (Stage 3) | | Layered cut-out in an editor |

### Stage 5 / Q5. Morphing between two real photos of the same person at different ages

| Method | What it does | Invents? | Cost and effort | Charter verdict |
|---|---|---|---|---|
| Classic landmark morph (Delaunay triangles, per-triangle warp, cross-dissolve) [65] | Warps both photos toward an intermediate geometry and blends | No new content: every pixel is a blend of the two inputs (ghosting on hair and background). The in-between face is a blend, not a record of a real face | CPU; free; 1 to 2 hours learning. Landmark code in LearnOpenCV FaceMorph (C++ and Python; folder lists code and landmark files only) [65] | Allowed ("connect real photos"); label L4 "morph" |
| Plain cross-dissolve / xfade | Fade | None | `ffmpeg xfade`, ImageMagick `-morph` (both run in sandbox [102]) | Allowed |
| FILM [61], RIFE / Practical-RIFE [62][63] | Optical-flow in-betweens from "near-duplicate photos" [61] | Warped pixels; at 30-year gaps expect ghosting or melted faces (M, untested) | FILM: TF2, CUDA 11.2, Python 3.9, archived 2025-10-14 [61]. RIFE: MIT, `inference_img.py` with `--exp=4` gives 16x frames [62]; Practical-RIFE 4.25 default, 4.26 on 2024-09-21 [63]; ComfyUI wrapper has FILM, RIFE and others [64] | Fine for short gaps or to smooth a classic morph; poor fit for decades |
| First/last-frame video generation: Wan2.1 FLF2V 14B 720p only, Apache-2.0 [67]; Wan2.2 FLF2V in ComfyUI [70]; Veo 3.1 `lastFrame` [82]; LTX-2 `KeyframeInterpolationPipeline` [74] | Generates a whole video between two images | Yes: invented intermediate faces, expressions and scene motion; may drift identity | Local VRAM for Wan FLF2V not stated [67][70] (UNVERIFIED); Veo 3.1 Fast $0.10 per second [51]; Luma keyframes not covered on its pricing page [81] | Only as a labelled "generated in-between" in the reconstruction treatment; never to claim "this is how she looked at 15" |
| Age-progression GANs (SAM, SIGGRAPH 2021) [66] | Re-synthesises a face at a target age from StyleGAN | Yes: fabricates faces | NVIDIA GPU required [66] | Out of scope for a real person's history |

**Honesty answer.** Classic morph and dissolve do not hallucinate. Frame interpolation hallucinates only at occlusions for small gaps and fails visibly for large ones. First/last-frame generation hallucinates intermediate faces and is acceptable under Principle 4 only if treated as a visibly generated device, labelled, and never presented as a record. **Labels:** L4a "morph (no generated frames)"; L4c "generated in-between (frames invented)".

**Best honest design (M).** Chain morphs through real intermediate photos (age 6, 12, 18...), so each segment connects two real images. A dissolve through a paper-turn or block-build transition says "time passed" without implying a face existed.

### Stage 6 / Q6. Image-to-video and video upscaling

**Local options (verified 2026-10-18)**

| Model | Key facts | Hardware | Notes |
|---|---|---|---|
| Wan2.2 TI2V-5B / I2V-A14B (Apache-2.0, released 2025-07-28) [69] | README: 14B single GPU needs 80 GB; TI2V-5B "at least 24GB" at 720p 24 fps; ComfyUI doc: 5B "should fit well on 8GB vram with the ComfyUI native offloading" [69][70] | 8 GB (5B with offload) to 24 GB+ | Wan2.2-Lightning 4-step LoRAs claim about 20x speed-up but artefacts at "extremely large motion" [71] |
| FramePack (Apache-2.0) [72] | 13B next-frame-section model; 6 GB minimum; RTX 30/40/50 tested, older cards untested (README: GTX 10XX/20XX "not tested", not excluded); 4090 about 2.5 s per frame (1.5 with TeaCache); laptops 4 to 8x slower; Windows one-click, over 30 GB downloads | 6 GB+ | README favours "large, dynamic motions" over subtle ones; fake sites exist [72] |
| WanGP (free to use locally; licence unstated) [77] | Wan 2.1/2.2, LTX family, Hunyuan 1.5 and more; "as little as 6 GB" for select models; Windows and Linux; NVIDIA GTX 10+ and AMD RDNA; v18.17 on 2026-10-15 | 6 GB+ | Good single front-end for low VRAM |
| LTX-Video 0.9.x and LTX-2.x [73][74][75] | LTX-2.5 recommended, 66 GiB download; ComfyUI-LTXVideo wants a CUDA GPU with 32 GB+ and 100 GB disk; community 8-bit LTX-Video run on 8 GB claimed | 8 GB (old) to 32 GB+ | LTX-2 generates synced audio: ignore, we do not generate sound from photos |
| HunyuanVideo-1.5 (8.3B, 2025-11-20) [76] | I2V 480p and 720p; minimum 14 GB with offload | 14 GB+ | Licence terms not read |
| LivePortrait [78] | Animates a portrait from someone else's driving video | NVIDIA, or Mac MPS (about 20x slower than a 4090) | Out of scope for expressions or speech; authors warn of deepfake misuse [78] |

**Cloud options and cost per 5-second clip** (prices as shown 2026-10-18; per-clip figures are my arithmetic)

| Service | Price basis | 5 s clip | Notes |
|---|---|---|---|
| Google Veo 3.1 Lite / Fast / Standard (Gemini API, paid) | $0.05 / $0.10 / $0.40 per second at 720p (with audio) [51] | $0.25 / $0.50 / $2.00 | Input image is the first frame; `lastFrame` for Veo 3.1; durations 4, 6 or 8 s; I2V `personGeneration` accepts only `allow_adult` [82]. So photos with children get no cloud image-to-video. The Gemini API page is silent on children, and Google's Vertex page rejects child content when `personGeneration` is not `allow_all` [116]. Expect a refusal, not an altered video (M, UNVERIFIED; a paid test with a public-domain child photo is TODO(research)). SynthID; stored 2 days [82] |
| Kling 2.5 Turbo Pro / Kling v3 via fal | $0.07 / $0.14 per second [52] | $0.35 / $0.70 | fal page has no retention statement [52] |
| Luma Ray3.2 | 100 credits for 720p 5 s; 400 for 1080p; Plus $30 per 10,000 credits [81] | $0.30 (720p), $1.20 (1080p) on Plus | Privacy policy: see Q7 |
| Runway | Standard $15 (625 credits), Pro $35 (2,250); Gen-4 Turbo about 5 to 6 credits per second, Gen-4.5 12 per second (page inconsistent) [80] | about $0.60 to $0.72 (Turbo), about $1.44 (Gen-4.5) on Standard | Free plan: 125 one-time credits; training statement not on the page [80] |

**Prompt patterns for restraint.** Sourced hints: Wan's README example describes the subject's look, posture, background and mood plus a close-up framing [68]; Veo's I2V examples pair scene description with camera and motion language [82]; FramePack prefers large motion [72]; Kontext advises specific descriptions and "while maintaining the same facial features, hairstyle, and expression" [34]. I found no creator-shared restraint prompts, so the rest is **my synthesis, untested**:
1. The first frame is always the restored photo. Never generate from text.
2. Describe motion only, not appearance. Do not re-describe the face.
3. Use restraint words: "very subtle", "slow", "locked-off camera", "subject remains still except gentle breathing and a slow blink", "no scene change", "no cut".
4. Prefer environmental motion (leaves, curtains, dust in light, water) over faces and hands.
5. Negative prompts on local models: "morphing, warping face, changing identity, extra people, text, fast motion, camera shake".
6. Short clips (3 to 5 s), fixed seed, 3 to 4 takes, pick the one with least change.
7. Gate with a script: face-embedding similarity between frame 1 and the last frame; reject below threshold (UNVERIFIED approach, scriptable).
8. Everything after frame 1 is invented, including blinks and hair movement. Label L4b "image-to-video (frames invented)".
9. For people who have died: no lip movement, no expression animation, no sound. Environmental motion or parallax only, and ask the family first (Principle 5 judgment, M. Context: MyHeritage's Deep Nostalgia produced nearly 100 million animations [101]; the article I read does not discuss reactions to animating the dead.)

**Video upscaling and interpolation**

| Tool | Facts | Notes |
|---|---|---|
| Video2X 6.4.0 (AGPL-3.0) [79] | Real-ESRGAN, Real-CUGAN, RIFE, Anime4K via ncnn and Vulkan; Windows and Linux; AVX2 CPU needed | CLI docs at docs.video2x.org (not fetched) |
| SeedVR2 (Apache-2.0) [23][24] | Video and image restoration; README example runs 100 frames of 720x1280 on one 80 GB H100; ComfyUI node and CLI run on 8 to 24 GB with GGUF/FP8 and BlockSwap | "Not always robust to heavy degradations or very large motion"; over-sharpens |
| Topaz Video $299 per year or $59 per month (local unlimited; cloud credits for the web version) [31] | Closed source | Subscription only on page |
| ffmpeg `minterpolate`, `framerate`, `scale` | Present in ffmpeg 6.1.1 and run in sandbox [102] | CPU; motion-interpolation artefacts expected (M) |

### Stage 7 / Q7. Privacy and terms for uploading family photos

**What I could read (dated)**

| Service | What the current text says | Verdict |
|---|---|---|
| Gemini app (consumer), page updated 2026-10-13 [84] | With Keep Activity on, activity (including uploaded photos or videos) is used to improve services and train generative AI, and "a subset of chats are reviewed by human reviewers... retained for up to three years"; auto-delete default 18 months; with Keep Activity off, chats still saved 72 hours and not used for training unless you send feedback; already-reviewed chats are not deleted | Only with Keep Activity off, and only for photos the family has cleared |
| Gemini API, unpaid tier and AI Studio free (terms effective 2026-03-23, updated 2026-04-28) [85][51] | Content is used to improve products; human reviewers may read input and output; "Do not submit sensitive, confidential, or personal information" | Never for family photos |
| Gemini API, paid tier [85][51] | Prompts and files not used to improve products; logged for a limited period for abuse detection; Veo videos stored 2 days [82] | Acceptable for selected photos; download results immediately |
| Luma (privacy policy, 2026-04-20) [86] | Lists "Train, develop, and improve the artificial intelligence, machine learning, and models" as a purpose; collects chat and upload content; says it may be reproduced in outputs; no opt-out stated | Never |
| Adobe Firefly [87] | "We do not and have never trained Adobe Firefly on customer content"; page undated | Acceptable on this point; consumer terms and Photoshop content analysis not read (UNVERIFIED) |
| Replicate [88] | API predictions removed after an hour; web UI predictions kept indefinitely; training use not stated | API only, save locally; terms for individual hosted models not read |
| fal.ai [52] | No retention statement on the pricing page | UNVERIFIED |
| Topaz [31][32] | Desktop apps render locally and unlimited; web apps and cloud video render in the cloud; the privacy policy (2024-10-03) does not state whether images are used for training | Use the desktop app offline; avoid web/cloud |
| OpenAI (ChatGPT, API), Runway, Kling, Midjourney, MyHeritage, Remini/Bending Spoons | Pages returned 403 or 404, were empty shells, or lacked terms text | UNVERIFIED: treat as no until read |
| Unofficial "free AI restore" sites and public Hugging Face Spaces | CodeFormer's README warns many third-party sites are unofficial and only its HF, Replicate and OpenXLab demos are maintained by the authors [15]; FramePack and DepthFlow warn about fake download and paid sites [72][60] | Never |
| `rembg` cloud back-ends | They "send images to their servers" [55] | Never select |

**Fully offline alternatives.** Real-ESRGAN ncnn [18], GFPGAN [17], CodeFormer [15], SeedVR2 [24], SUPIR [22], rembg [55], SAM 2 [56], Depth Anything V2 [58], DepthFlow [60], RIFE [62], OpenCV morph [65], ImageMagick and ffmpeg [102], Kontext, Qwen-Image-Edit, FLUX.2 klein [33][36][38], Wan2.2, FramePack, WanGP [69][72][77], Krita AI Diffusion with local ComfyUI [48]. Model weights download once; ComfyUI offers `--offline` [49]. After downloading, disconnect or firewall the machine for sensitive batches (M).

**Beyond terms (Principle 5).** The archive contains relatives, children and third parties who have not consented to their faces being sent to a vendor. Default to local processing.

### Q8. Labelling restored versus stylised versus generated

**What others do**
- IPTC `DigitalSourceType` vocabulary: `print` (scanned from an opaque medium), `negativeFilm`, `positiveFilm`, `humanEdits` (non-generative human edits; `minorHumanEdits` was retired 2024-09-17), `algorithmicallyEnhanced` (algorithmic change "without changing the main content", for example sharpening or denoise), `compositeWithTrainedAlgorithmicMedia` ("Edited using Generative AI", such as inpainting), `trainedAlgorithmicMedia` ("Created using Generative AI"), `composite` [89]. Round 1 check against [89] adds `digitalCreation` ("created by a human using non-generative tools", added 2024-09-17) and `compositeSynthetic`, which the ladder below uses. `humanEdits` is for non-generative edits to captured media only. The IPTC user guide says to write the URI (not the label) into the field, stored in XMP only, and that ExifTool can script bulk updates [90].
- C2PA / Content Credentials: open standard, "nutrition label" for content [91][92]; the Rust SDK is beta and supports spec 2.4 [93]. Signing needs certificates; optional for a private project (M).
- Machine marks: Gemini image and Veo outputs carry SynthID watermarks [50][82]; BFL API outputs carry C2PA metadata [33].
- Documentary practice: Archival Producers Alliance guidelines (Sept 2024 PDF; not readable here) plus a toolkit with Transparency Tips, Crediting Suggestions, a GenAI Tracker/Cue Sheet and "10 Questions Before You Start" [95][96]. Partnership on AI: disclose when synthetic elements would change how viewers perceive the content; direct disclosure (labels, notes) versus indirect (metadata, C2PA); disclose how consent was obtained [94]. Wikimedia Commons: document the prompt, name the engine, list both human and AI as authors [97].
- Cautionary cases: *Roadrunner* used an undisclosed AI voice of Anthony Bourdain; the estate executor disputed consent; disclosure came only in an interview [98]. *What Jennifer Did* images drew accusations of AI manipulation that the producer denied [99]. *They Shall Not Grow Old* restored, colourised and retimed 100 hours of footage (13 to 24 fps per a *Variety* review cited by Wikipedia); critics said it erased the original filmmakers and implied the archive was in disrepair [100].

**Proposed convention: the Reality Ladder**

| Level | Meaning | Example steps | IPTC value | On screen |
|---|---|---|---|---|
| L0 Scan | Unaltered digitisation | Flatbed or camera scan | `print`, `negativeFilm` or `positiveFilm` | Plain photo frame |
| L1 Cleaned | Human, non-generative fixes | Crop, deskew, levels, healing brush | `humanEdits` | Plain photo frame |
| L2 Enhanced | Algorithmic restoration that invents texture or colour | Upscale, face restore, colourise, diffusion repair | `algorithmicallyEnhanced`; use `compositeWithTrainedAlgorithmicMedia` if a generative model repaired content | Photo frame plus small "R" tag; colourised ones add "colours estimated" |
| L3 Restyled | Real photo redrawn in the house look | Edit model with style LoRA, hand-built voxel from photo | `compositeWithTrainedAlgorithmicMedia` (AI edit on a real photo); `digitalCreation` (hand-drawn from scratch); `composite` (hand-drawn over a real photo) | Obviously stylised |
| L4 Animated | Motion added to a real photo | 4a parallax or classic morph (no generated frames); 4b image-to-video; 4c generated in-between | 4a `humanEdits`/`algorithmicallyEnhanced`; 4b/4c `compositeWithTrainedAlgorithmicMedia` | Tag on the clip: "moved", "frames invented" |
| L5 Reconstruction | Scene never photographed, built from testimony | Stylised scene in house look | `digitalCreation` (hand-built); `trainedAlgorithmicMedia` (AI-built); `compositeSynthetic` (mixed) | Always stylised; caption "Reconstructed from [name]'s memory, [interview date]" |

**Round 1 operational rule at L2 (house rule).** Generative repair is permitted on non-face regions only (tears, stains, backgrounds). Faces at L2 are limited to non-generative fixes, or CodeFormer or GFPGAN with blend-back; CodeFormer's `w` should be 0.7 or higher, and GFPGAN has no `w` dial in the sources (TODO(research)). Any generative change to a face moves the image to L3, where it must look drawn, or the image is rejected. Open question for the Fable advisor: under this rule, does colourising a face count as a generative change?

Carry the label in four places: filename suffix (`__L2`), `steps.csv`, embedded XMP, and the end credits as an APA-style cue sheet [96]. Video containers do not reliably carry IPTC fields (M, UNVERIFIED), so the manifest and credits are the authoritative record.

**ExifTool pattern (UNVERIFIED: ExifTool is not installed in the sandbox).** `exiftool -XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/print LJ-B03-0042-F.tif` (URI from the vocabulary page [89]; tag syntax from ExifTool conventions, M).

### Q9. Cost and time for about 300 photos, by hardware tier, plus the tier decision table

**Assumptions (ESTIMATE, mostly unsourced).** 300 photos scanned; 150 restored or upscaled (only the 40 hardest go to a generative or cloud model on the no-GPU tier); 60 stylised; 100 parallax shots; 20 morphs; 25 hero image-to-video clips of 5 seconds. Generative stages assume 3 takes per kept result, so the no-GPU tier makes about 300 cloud image edits (40 restorations plus 60 stylisations, 3 takes each, plus margin) and 75 clip takes. Scanner purchase and Topaz excluded. Cloud prices from [51][52][80][81][83]; FramePack time derived from [72] (150 frames at 2.5 s per frame is about 6 minutes on a 4090; 4 to 8x slower on laptop-class cards).

| | No GPU | 8 to 12 GB NVIDIA | 16 GB+ |
|---|---|---|---|
| Human hours (scan 10 to 14, manifest 5, hand clean 10 to 25, labels 3 to 5; supervise AI and review 15 to 30 with no GPU, 12 to 25 with a GPU) | 45 to 80 | 40 to 70 | 40 to 65 |
| Machine time | Real-ESRGAN on CPU measured at roughly 1,250 to 1,500 s per megapixel of input on a 4 vCPU VM with software Vulkan [104]. A 600 ppi scan of a 4x6 print is 8.6 MP, so CPU suits small crops or a handful of photos; send the rest to a GPU or cloud (real GPU speed unmeasured). Cloud jobs minutes each | Restore 2 to 8 h; stylise 3 to 12 h; FramePack clips 25 to 50 min each on laptop-class, so use cloud for hero clips | Restore 1 to 5 h; stylise 2 to 8 h; 75 clip takes at 5 to 6 min each is 6 to 8 h overnight |
| Cloud spend | About $30 to $85: roughly 300 edits at $0.04 to $0.15 ($12 to $45) plus 75 clip takes at $0.25 to $0.50 ($19 to $38); up to about $120 with Pro-tier image models or Standard Veo. Renting a 4090 for 25 to 30 hours instead costs about $10 to $30 plus storage | $0 to $60 (cloud only for hero clips) | $0 to $40 |
| Privacy exposure | High unless cloud limited to cleared photos | Low | Lowest |

**Hardware-tier decision table**

| Stage | No GPU | 8 to 12 GB | 16 GB+ |
|---|---|---|---|
| 1 Scan | Same for all tiers (Stage 1 table) | Same | Same |
| 2 Restore and upscale | Manual levels; Real-ESRGAN ncnn (iGPU support uncertain [18][26]) or CPU; cloud edit for a few photos | Real-ESRGAN, CodeFormer, SeedVR2 GGUF/FP8 [24], SUPIR tiled [22] | Add SUPIR comfortably, SeedVR2 FP8/FP16, Qwen-Image-Edit |
| 3 Cutout and depth | `rembg[cpu]`, Depth Anything V2 Small on CPU [55][58], manual masks, paper-theatre layers | Add SAM 2, DepthFlow | Add SAM 3 (CUDA) [57] |
| 4 Stylise | Hand-built voxel/pixel/clay, posterise, Inkscape trace; or cloud edit | FLUX.2 klein 4B [38], Z-Image Turbo (fits 16 GB [39]; smaller GPUs via quantised builds, UNVERIFIED), Krita AI Diffusion (6 GB recommended [48]), fluxgym style LoRA (12 GB [47]) | Add Qwen-Image-Edit-2511, PuLID-FLUX 16 GB [41], InfiniteYou 16 GB with offload [42], USO 16 to 18 GB [43], ai-toolkit LoRA [46] |
| 5 Morph | OpenCV Delaunay morph, ImageMagick, ffmpeg xfade [65][102] | Add RIFE and ComfyUI FILM [62][64] | Add Wan FLF2V (VRAM UNVERIFIED [67][70]); LTX-2 keyframes need 32 GB+ [75] |
| 6 Image-to-video | Cloud only for photos without children (Veo Lite or Fast, Kling). Photos with children: parallax or local only (local image-to-video needs a GPU) | Wan2.2 5B [70], FramePack [72], WanGP [77] | Add Wan2.2 14B with FP8 or GGUF plus Lightning (VRAM UNVERIFIED [71]), HunyuanVideo-1.5 (14 GB minimum [76]) |
| 6b Video upscale | ffmpeg scale or skip; Video2X needs Vulkan [79] | Video2X; SeedVR2 GGUF (slow) | SeedVR2 FP8/FP16 |
| 7 Privacy | Cloud steps need the Q7 rules | Offline possible except big clips | Fully offline possible |

Apple Silicon: chaiNNer uses MPS [27]; Krita plugin supports MPS on macOS 14+ [48]; ComfyUI supports Apple Silicon [49]; LivePortrait about 20x slower than a 4090 [78]; BlockSwap unavailable on macOS [24]; SAM 3 and FILM need CUDA [57][61]. Unified memory versus the VRAM tiers is UNVERIFIED.

---

## Exemplars / recipes

### Exemplars and cautionary cases

Creator-made exemplars on family archives were not reachable (no search budget); the cases below are documentary and industry precedents plus two design ideas of our own.

**E1. *They Shall Not Grow Old* (Peter Jackson, 2018): restoration, colour, retime, sound.** [100]
- What: 100 hours of Imperial War Museum footage restored, much of it colourised, retimed (13 to 24 fps per a *Variety* review cited by Wikipedia), with dialogue built from lip reading and oral-history audio.
- Why it matters: the clearest precedent that restoration plus colour plus interpolation changes how people read old images. Critics said it erased the original filmmakers, implied the archive was in disrepair, and that lip reading cannot recover accents.
- Reuse: credit the original photographer or family member on screen; show an untouched original beside the restoration at least once; say plainly what was added (colour, sound, motion).
- Caveat: the Wikipedia article does not say how colours were checked.

**E2. *Roadrunner* (2021): the AI voice.** [98]
- What: a synthetic voice read Anthony Bourdain's written words; undisclosed in the film, revealed in an interview; the estate executor disputed having approved it.
- Lesson: this is exactly what Principle 4 forbids ("put words in anyone's mouth"). Any voice-clone or lip-sync tool that makes a real person speak is out of scope; mentioned here only as a warning.

**E3. *What Jennifer Did* (2024): suspected AI images in a documentary.** [99]
- What: viewers flagged images near the 28-minute mark with warped fingers and jumbled backgrounds; the executive producer denied AI use; Netflix and the director made no comment (per Wikipedia at fetch time).
- Lesson: when archival-looking images cannot be traced, trust collapses. Our manifest and the "if it looks like a photograph it is a photograph" rule are the antidote.

**E4. MyHeritage Deep Nostalgia (2021).** [101]
- What: face-animation of still photos; launched February 2021; nearly 100 million animations.
- Lesson: it shows demand and how easy "animate the ancestor" is. It also animates faces with expressions the person may never have made, so we restrict face animation (Q6, item 9).

**E5. Archival Producers Alliance GenAI guidelines and toolkit.** [95][96]
- What: documentary-industry guidelines (Sept 2024 PDF, not readable here) and a toolkit with Transparency Tips, Crediting Suggestions, a GenAI Tracker/Cue Sheet, "10 Questions Before You Start", Workflow Tips and Case Studies.
- Reuse: adopt the cue-sheet idea as our `steps.csv` and end-credits page.

**E6. Partnership on AI Synthetic Media Framework.** [94]
- What: responsible-practice framework built on consent, disclosure and transparency; distinguishes direct disclosure (labels, notes) from indirect (metadata, C2PA).
- Reuse: use both: on-screen tags (direct) plus XMP and manifest (indirect).

**E7. Paper-theatre parallax (our proposal, M).** Real cut-out layers with soft shadows instead of generative fill behind moving subjects. Honest, no-GPU, scriptable, fits a papercraft look. Test in the vertical slice.

**E8. Attribute-based ageing character sheet (our proposal, M).** A hand-made voxel/pixel/clay character per age band, with identity carried by hair, glasses, clothes and posture rather than a synthesised face. Test with an insiders' line-up in the vertical slice.

### Recipe R1. Scan and clean

Goal: a lossless master plus a clean working copy for every photo, with a manifest row. Labels L0 and L1.
1. Prepare: set up folders and `manifest.csv` (Q1). Clean the originals and scanner glass [1]. Keep originals; do not peel albums [2].
2. Flatbed prints: 600 ppi, colour, 16 bit, scanner "auto-enhance" and "restore fading" off; 2 to 4 prints per pass with gaps; save TIFF [1][11]. Scan the back of any print with writing.
3. Phone path: stand or a stack of books so the phone is parallel to the print (use a level app); two soft lights at 45 degrees or window light, out of the glass reflection; lock focus, exposure and white balance; no flash; shoot RAW if available; for glossy glare use PhotoScan's four-dot capture [6]; for album pages use Photomyne [14].
4. Film path: camera on a copy stand with a 1:1 macro lens, f/8, lowest ISO, cable release, masked holder [5]; convert negatives with darktable `negadoctor` (include unexposed film border; sample film base colour first) [13] or Negative Lab Pro (Lightroom Classic) [12]; or use a film flatbed with VueScan Infrared Clean [9][11].
5. Split and straighten multi-print scans (OpenCV contour script by the AI team; Principle 7). Name `LJ-B03-0042-F`.
6. Write checksums and fill `manifest.csv`: `sha256sum 01_masters/*.tif > checksums.txt`.
7. Make the L1 copy: crop, deskew, per-channel levels to remove the cast, healing brush on dust. Save `__L1`. No AI.
8. Back up 3-2-1 [2].
9. Embed provenance (UNVERIFIED command): `exiftool -XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/print LJ-B03-0042-F.tif` for the master; use `.../humanEdits` for the L1 copy [89][90].

Why it works: it separates the untouched record from every later choice.

### Recipe R2. Restore and upscale

Goal: usable 1080p/4K source images without inventing faces. Label L2.
1. Start from the `__L1` copy. Decide if upscaling is needed: a 4x6 print at 600 ppi is already 3600x2400 px (Q1), so skip.
2. Upscale only where needed (wallet prints, 1990s digital files). Real-ESRGAN portable: `realesrgan-ncnn-vulkan -i in.png -o out.png -n realesrgan-x4plus -s 2` (`realesr-general-x4v3` is not in the portable zip; with it the tool exits 0 and writes an all-black image, so check file size and look at the output; run `-h` to confirm; use `-t` for tiling) [18][104][110]. No GPU: use the Python script with `--tile`, slow (M).
3. Faces: `python inference_codeformer.py -w 0.8 --input_path in.png` (add `--bg_upsampler realesrgan --face_upsample` if wanted); higher `w` is more faithful [15]. Alternative: `python inference_gfpgan.py -i inputs -o results -v 1.3 -s 2` [17]. Blend the face result 40 to 60 percent over the plain upscale in a layer mask (M).
4. Heavy damage only: SeedVR2 via ComfyUI node or `inference_cli.py` (3B GGUF for 8 GB, FP8 for 12 to 16 GB; LAB colour correction recommended for fidelity) [24], or SUPIR (non-commercial) [21][22].
5. Colourise black-and-white only if the story needs it: `python scripts/infer.py --model_name ddcolor_modelscope --input ./bw_dir` [28]. Check colours against family memory; mute skin tones.
6. Review: flick original versus result at 100 percent; a confirmed insider who knew the person approves or rejects; optional embedding-similarity gate (UNVERIFIED approach).
7. Record tool, version, settings, seed and `invents` in `steps.csv`; save as `__L2`; write XMP `algorithmicallyEnhanced` (or `compositeWithTrainedAlgorithmicMedia` if a generative model repaired content) [89]; for colourised prints add the caption "colours estimated".

Fallback for no GPU: do steps 1 and 7 by hand; use a cloud edit model on at most 10 to 20 cleared photos (Q7).

### Recipe R3. Cutout and parallax

Goal: 4 to 8 second camera moves on a still, with honest disocclusion. Label L4a.
1. Pick a photo with clear layers (subject, mid-ground, background) and enough resolution.
2. Cut out the subject: `rembg i -m u2net in.png fg.png` (use `-a` or `-vm` and `-dc` for hair; `-om` for a mask only) [55]; or click masks with SAM 2 [56]; or by hand in GIMP/Krita/Inkscape.
3. Depth map: Depth Anything V2 `python run.py --encoder vits --img-path in.png --outdir depth --pred-only --grayscale` (flag names per repo convention; check `--help`; Small is Apache-2.0 and falls back to CPU) [58]. Blur or flatten depth across faces.
4. Option A (GPU): render with DepthFlow (AGPL; docs at depth.tremeschin.com) [60]. Option B: displace a subdivided plane in Blender (M). Option C (no GPU, paper-theatre): 3 to 5 layers moved with transforms in Kdenlive or DaVinci (M).
5. Disocclusion: keep orbit to 2 to 3 degrees and push-in to 3 to 8 percent; extend backgrounds by cloning (L1). If you use generative fill, the clip becomes L4b with an `invents` note.
6. Pure 2D alternative, tested in sandbox [102]: `ffmpeg -loop 1 -i in.png -vf "zoompan=z='min(zoom+0.0007,1.08)':d=96:s=960x720:fps=24,format=yuv420p" -t 4 kb.mp4`.
7. Label and log.

### Recipe R4. Stylise with likeness

Goal: one coherent look that still reads as the same person at 6, 25 and 55. Label L3.
1. Choose the look and write a two-line style bible (palette, line weight, proportions). Decide route per chapter (Q4).
2. Route A (default, hand-made): for each age band, pick 3 to 5 real photos; list identity attributes (hair shape and colour, glasses, beard, scars, posture, signature clothes, height versus others); build a character sheet in the chosen look (MagicaVoxel/Blockbench or pixel art; UNVERIFIED tools; or Inkscape trace and manual tidy); take the palette from the photo. Backgrounds can use MapartCraft for block palettes [54].
3. Route B (AI on the real photo): input the L2 photo at about 1 MP [37]; use FLUX.1 Kontext dev with a style LoRA from [45], Qwen-Image-Edit-2511 [36], or FLUX.2 klein [38]. Prompt pattern from the Kontext guide: name the subject specifically and add "while maintaining the same facial features, hairstyle, and expression"; change one thing per step; English prompts [34]. Keep one seed, one LoRA strength and one prompt template per chapter. Batch with ComfyUI workflow JSON or its local API [49]. Pull four seeds and choose by line-up.
4. Route C (only if a new angle is truly needed): InstantID/PuLID/InfiniteYou from a same-age reference, conditioned on the original composition [40][41][42]; otherwise it is an L5 reconstruction.
5. Route D (optional style LoRA): train on the maker's own 10 to 30 hand-made frames with fluxgym (12/16/20 GB) or ai-toolkit [46][47]. Use a person LoRA only per Q4c.
6. Line-up test: show five stylised faces to confirmed insiders; record who is recognised and at what age. Adjust attributes, not faces. Real-photo line-ups run in the vertical slice.
7. Log in `steps.csv`; XMP `compositeWithTrainedAlgorithmicMedia` for AI routes; credits mention the tools.

### Recipe R5. Morph between two photos

Goal: a "time passing" transition between two real photos of the same person. Label L4a (classic) or L4c (generated).
1. Align: scale and rotate photo B so the eye positions match photo A. Crop to the same aspect ratio.
2. Classic morph: mark 10 to 20 landmarks per photo (eyes, brows, nose, mouth, jaw, hairline, shoulders); build Delaunay triangles; for each frame warp both images toward the interpolated landmarks and cross-dissolve with weight t; ease in and out; 24 to 48 frames. Reference code: LearnOpenCV FaceMorph (Python/C++) [65].
3. No-landmark baseline, tested in sandbox [102]: `convert a.png b.png -morph 14 frames/m_%02d.png` then `ffmpeg -framerate 24 -i frames/m_%02d.png -c:v libx264 -pix_fmt yuv420p morph.mp4`; or `ffmpeg -loop 1 -t 2 -framerate 24 -i a.png -loop 1 -t 2 -framerate 24 -i b.png -filter_complex "[0][1]xfade=transition=fade:duration=1:offset=1,format=yuv420p" xfade.mp4`.
4. Optional smoothing: RIFE `python inference_img.py --img a.png b.png --exp=4` produces 16x frames [62]; or `ffmpeg -i in.mp4 -vf "minterpolate=fps=48:mi_mode=mci" out.mp4` (CPU, tested to run [102]). Expect ghosting if the gap is large (M).
5. Chain through real intermediate photos where they exist.
6. Optional generated version: Wan2.1 FLF2V `python generate.py --task flf2v-14B --size 1280*720 --ckpt_dir ./Wan2.1-FLF2V-14B-720P --first_frame a.png --last_frame b.png --prompt "..."` [67], or Wan2.2 FLF2V in ComfyUI [70], or Veo 3.1 with `lastFrame` [82]. Prompt for motion only. Inspect middle frames: if a face appears that matches neither photo, it is invented. Use only in the reconstruction treatment and label L4c.
7. Log, label, and show the two source photos at the ends of the transition.

### Recipe R6. Label a reconstruction

Use when a scene was never photographed but is remembered (the kitchen table in 1978).
1. Source it: whose testimony, which interview, which date; record in `manifest.csv`. Get the narrator's and the family's OK for sensitive scenes (Principle 5).
2. Brief: write what is known versus what is invented (furniture colour, light) and keep invented elements generic.
3. Make it only in the house stylised look (voxel, clay or paper); no photoreal people, no synthetic voices [98].
4. Add the visible cue: a consistent frame treatment and the caption "Reconstructed from [name]'s memory, [interview date]".
5. Embed metadata: `trainedAlgorithmicMedia` (AI-built), `digitalCreation` (hand-built) or `compositeSynthetic` (mixed) [89]. Write the full URI, not the label text. For video, tag after the last export, because ffmpeg strips the tag [105]; add prompt, model, seed and testimony ID in `steps.csv`; add a line to the credits cue sheet [96].
6. Review with the family; archive the brief.

---

## Tools

Prices and statuses as shown on the linked pages on 2026-10-18 ("verified on" is that date unless a snippet is noted). Learning curve and scriptability ratings are my judgment (M) unless stated.

### Digitise

| Tool | What | Cost | Platform and hardware | Learning | Scriptable | Verified |
|---|---|---|---|---|---|---|
| Epson Perfection V600 [9] | Flatbed with film unit, 6400 dpi, Dmax 3.4, Digital ICE | Price not on page; status "Discontinued" | Page lists Windows XP-8 and Mac OS X 10.6-10.10 | Low | Vendor software, GUI | 2026-10-18 |
| Epson V850 Pro [10] | Dual-lens flatbed, Dmax 4.0, eight holders | $1,999; add-to-cart error | Same OS list | Low | GUI | 2026-10-18 |
| VueScan 9.8.59 [11] | Scanner driver and software, IR dust cleaning, Restore Fading | Price not on page | Windows, macOS, Linux; 8,000+ scanners | Medium | CLI unverified | 2026-10-18 |
| Negative Lab Pro v3.1 [12] | Negative conversion in Lightroom Classic | Price not on page; free trial | Needs Lightroom Classic | Medium | No | 2026-10-18 |
| darktable negadoctor [13] | Negative conversion module | Free (darktable) | Desktop; CPU | Medium | darktable-cli unverified | 2026-10-18 |
| Google PhotoScan [6][7] | Phone app, four-dot glare removal | Free | iOS and Android; frozen since 2023 | Low | No | 2026-05-18 article |
| Photomyne [14] | Multi-print phone scanning, AI restoration extra credits | $59.99 per year after 3-day trial | iOS and Android | Low | No | 2026-10-18 |
| Camera plus 1:1 macro on stand [5] | Camera-scan film and prints | Existing gear | DSLR or mirrorless | Medium | Tethered capture possible (M) | 2023-11-10 article |
| ImageMagick, ffmpeg [102] | Batch image and video tools | Free | CPU; present in sandbox | Medium | Full CLI | 2026-10-18 (run) |

### Restore, upscale, colourise

| Tool | What | Cost and licence | Platform and hardware | Learning | Scriptable | What it invents | Verified |
|---|---|---|---|---|---|---|---|
| Real-ESRGAN [18] | General upscaler | Free, BSD-3 | Win/Linux/mac; ncnn builds on Intel, AMD, Nvidia; Python needs PyTorch | Low | CLI | Texture, edges | 2026-10-18 |
| Upscayl 2.15 [26] | GUI for upscaling models | Free, AGPL-3.0 | Win/mac/Linux; Vulkan GPU, most iGPUs unsupported | Low | Separate ncnn CLI | Texture | 2026-10-18 |
| chaiNNer [27] | Node-graph image processing | Free, GPL-3.0 | Win/mac/Linux; CPU fallback; MPS on Apple Silicon | Medium | CLI per wiki (not read) | Depends on model | 2026-10-18 |
| GFPGAN 1.3 [17] | Blind face restoration | Free, Apache-2.0 | Python, PyTorch, NVIDIA GPU | Medium | CLI | Skin, features; may change identity | 2026-10-18 |
| CodeFormer [15][16] | Face restoration, `w` fidelity knob; also colourise and inpaint aligned faces | Free; NTU S-Lab licence (terms not read) | Python, PyTorch 1.7+, CUDA 10.1+ | Medium | CLI | Face detail; hair seam damage | 2026-10-18 (last news 2023-07-20) |
| SeedVR2 [23][24] | One-step diffusion image and video restorer | Free, Apache-2.0 | 8 GB (GGUF Q4 + BlockSwap), 12 to 16 GB (FP8), 24 GB+ (FP16); ComfyUI and `inference_cli.py` | Medium-high | CLI | Plenty: over-generates, was plastic in 2.5.6 | 2026-10-18 |
| SUPIR [21][22] | Diffusion restorer (SDXL-based) | Free, non-commercial | About 12 GB + LLaVA 16 GB low-mem mode, or ~10 GB fp8 small crops; now in ComfyUI core per wrapper author | High | Batch script | A lot | 2026-10-18 |
| Microsoft Old Photos [25] | Scratch detection plus restoration | Free, MIT, research use, repo archived 2026-10-03 | NVIDIA, or CPU with `--GPU -1`; trained at 256 px | Medium | CLI | Texture, faces | 2026-10-18 |
| DDColor [28] | Colourise | Free, Apache-2.0 | PyTorch; CUDA 11.8 build suggested | Medium | CLI | All colours | 2026-10-18 (last news 2024-01-28) |
| DeOldify [29] | Colourise | Free, MIT, archived 2024-10-19 | Linux, about 4 GB+ | Medium | Python | All colours | 2026-10-18 |
| Topaz Photo, Gigapixel, Video [31] | Closed-source desktop upscalers | Photo $199 per yr or $39 per mo; Gigapixel $149 or $29; Video $299 or $59; Studio bundle $399 per yr; subscription only on page | Win and Mac; local rendering unlimited | Low | No CLI seen | Texture, faces | 2026-10-18 |
| PULSE [30] | Face upsampling by latent search | Research | GPU | n/a | n/a | Fictional faces: do not use | 2026-10-18 |

### Cutout and depth

| Tool | What | Cost and licence | Hardware | Learning | Scriptable | Verified |
|---|---|---|---|---|---|---|
| rembg [55] | Background removal CLI | Free, MIT; some weights restricted | CPU works (`rembg[cpu]`); cached models; avoid cloud back-ends | Low | `i`, `p`, `s`, `b`, `d` CLI | 2026-10-18 |
| SAM 2.1 [56] | Promptable segmentation | Apache-2.0 | Python 3.10+, PyTorch 2.5.1+; GPU build; WSL on Windows | Medium | Python | 2026-10-18 |
| SAM 3 / 3.1 [57] | Concept-prompted segmentation | SAM Licence; gated weights | CUDA 12.6+, Python 3.12+ | Medium | Python | 2026-10-18 |
| Depth Anything V2 [58] | Monocular depth | Small Apache-2.0; Base/Large CC-BY-NC | CPU fallback; GPU better | Low | `run.py` | 2026-10-18 |
| Depth Anything 3 [59] | Depth, pose, 3D Gaussians | Small, Base, metric, mono Apache-2.0; Large, Giant CC-BY-NC | CUDA in example | Medium | `da3` CLI | 2026-10-18 |
| DepthFlow [60] | 2.5D parallax renderer | Free, AGPL-3.0 | GPU (ray-marching shader); FFmpeg | Medium | Scripts; docs not fetched | 2026-10-18 |

### Edit, identity, stylise

| Tool | What | Cost and licence | Hardware | Learning | Scriptable | What it invents | Verified |
|---|---|---|---|---|---|---|---|
| FLUX.1 Kontext dev [33][34] | 12B instruction image editing | Free weights; non-commercial, gated | VRAM not stated; fp8 file recommended | Medium | ComfyUI API | Anything it redraws | 2026-10-18 |
| Qwen-Image-Edit-2511 [35][36][37] | 20B editing, better identity consistency | Apache-2.0 (2509 released 2025-09-22, 2511 on 2025-12-23) | VRAM not stated; fp8 file in ComfyUI | Medium | ComfyUI API | Anything it redraws | 2026-10-18 |
| FLUX.2 klein 4B / 9B, dev [38] | Multi-reference generation and editing | 4B Apache-2.0; 9B and dev non-commercial | klein 4B about 8 GB; dev needs H100 or quantised | Medium | Python | Anything | 2026-10-18 |
| Z-Image (Turbo, base) [39] | 6B image model | Apache-2.0; edit variant "to be released" on page | Turbo fits 16 GB; 4 GB via sd.cpp claimed | Medium | Python | Anything | 2026-10-18 |
| Gemini image models [50][51] | Cloud editing with up to 14 references; SynthID on all output | Nano Banana Pro $0.134 per 1K/2K image; legacy 2.5 Flash Image $0.039, deprecated, shutdown dated 2026-10-02 on pricing page | Cloud | Low | API | Anything | 2026-10-18 |
| InstantID [40] | SDXL single-face adapter | Apache-2.0 code; insightface and checkpoints research-only; last log 2024-07-18 | VRAM not stated | Medium | Python | New image of the person | 2026-10-18 |
| PuLID-FLUX [41] | ID customisation for FLUX | Apache-2.0; v0.9.1 on 2024-10-31 | 16 GB; demo 12 GB | Medium | Python; third-party ComfyUI | New image | 2026-10-18 |
| InfiniteYou [42] | FLUX identity-preserving generation | Code Apache-2.0; model CC-BY-NC research | 43 GB bf16, about 16 GB with offload plus 8-bit | Medium-high | Python | New image | 2026-10-18 |
| USO [43] | Style plus subject | Apache-2.0 | 16 to 18 GB fp8 | Medium-high | Python, ComfyUI | New image | 2026-10-18 |
| IP-Adapter plus [44] | Reference and FaceID nodes | GPL-3.0; maintenance-only since 2025-04-14 | SD1.5/SDXL | Medium | ComfyUI | New image | 2026-10-18 |
| Kontext style LoRAs [45] | 22 styles incl. Clay Toy, Origami, Paper Cutting, Pixel, LEGO | Licence not stated | With Kontext dev | Low-medium | Diffusers | Re-draws | 2026-10-18 |
| ai-toolkit [46] | LoRA and model training; GUI and CLI | Free, MIT | Config for 24 GB; supports Qwen, Kontext, Wan, Z-Image, LTX-2 | High | CLI | n/a | 2026-10-18 |
| fluxgym [47] | FLUX LoRA training UI | Free, MIT | 12, 16 or 20 GB | Medium | Gradio, scripts | n/a | 2026-10-18 |
| ComfyUI [49] | Node-graph runner for all of the above | Free, GPL-3.0; cloud version is paid | Win/mac/Linux; "as low as 4GB vram + 8GB ram" claimed; `--offline` | High | Workflow JSON, local API | n/a | 2026-10-18 |
| Krita AI Diffusion [48] | Krita plugin using ComfyUI | Free, GPL-3.0 | 6 GB+ recommended; CPU very slow; MPS on macOS 14+ | Medium | Not really | Depends | 2026-10-18 |
| MapartCraft [54] | Browser Minecraft map-art generator | Free, GPL-3.0 | Browser | Low | No | Nothing (palette mapping) | 2026-10-18 (README thin) |
| MagicaVoxel, Blockbench | Voxel and block modelling | Believed free (M) | Desktop | Medium | No | n/a | UNVERIFIED |

### Morph and interpolation

| Tool | What | Cost and licence | Hardware | Learning | Scriptable | What it invents | Verified |
|---|---|---|---|---|---|---|---|
| FILM [61] | Large-motion interpolation | Apache-2.0; archived 2025-10-14 | TF2, CUDA 11.2.1, cuDNN 8.1, Python 3.9 | High | CLI | In-betweens | 2026-10-18 |
| RIFE and Practical-RIFE [62][63] | Real-time flow interpolation | MIT | GPU; 2x 720p at 30+ fps on a 2080 Ti | Medium | `inference_img.py`, `inference_video.py` | In-betweens | 2026-10-18 |
| ComfyUI-Frame-Interpolation [64] | FILM, RIFE, GMFSS, AMT and more | MIT | Experimental Taichi back-end for non-NVIDIA | Medium | ComfyUI | In-betweens | 2026-10-18 |
| LearnOpenCV FaceMorph [65] | Landmark Delaunay morph example | Licence not shown | CPU | Medium | Python | Nothing new | 2026-10-18 |
| ImageMagick `-morph`, ffmpeg `xfade`, `minterpolate` [102] | Dissolve and motion interpolation | Free | CPU | Low | CLI | Nothing / minterpolate artefacts | Run in sandbox 2026-10-18 |
| SAM age manipulation [66] | StyleGAN age transform | MIT | NVIDIA | High | Python | A whole face: avoid | 2026-10-18 |

### Image-to-video, video upscaling, infrastructure

| Tool | What | Cost and licence | Hardware | Learning | Scriptable | Verified |
|---|---|---|---|---|---|---|
| Wan2.1 FLF2V 14B [67][68] | First/last-frame to video, 720p only | Free, Apache-2.0 | VRAM not stated | High | `generate.py` | 2026-10-18 |
| Wan2.2 (TI2V-5B, I2V-A14B) [69][70] | Open image-to-video | Free, Apache-2.0 | 8 GB (ComfyUI offload) to 80 GB | High | CLI, ComfyUI | 2026-10-18 |
| Wan2.2-Lightning [71] | 4-step LoRAs | Apache-2.0 | As Wan2.2 | High | ComfyUI | 2026-10-18 |
| FramePack [72] | Next-frame-section I2V | Free, Apache-2.0 | 6 GB; RTX 30/40/50 tested, older cards untested | Low | Gradio; Python | 2026-10-18 |
| LTX-Video / LTX-2.x [73][74][75] | I2V with keyframes and audio | Repo Apache-2.0; LTX-2 licence files not read | LTX-2 on ComfyUI: 32 GB+ VRAM | High | ComfyUI, Python | 2026-10-18 |
| HunyuanVideo-1.5 [76] | 8.3B I2V | Licence not read | 14 GB minimum with offload | High | Python | 2026-10-18 |
| WanGP [77] | One UI for many video and image models | Free locally; licence unstated | 6 GB+ select models | Low-medium | Browser UI | 2026-10-18 |
| LivePortrait [78] | Portrait animation from a driving video | Licence not seen | NVIDIA or Mac MPS | Medium | Python | Out of scope |
| Veo 3.1 Lite / Fast / Standard [51][82] | Cloud I2V and first/last frame | $0.05 / $0.10 / $0.40 per second | Cloud | Low | API | 2026-10-18 |
| Kling via fal [52] | Cloud I2V | 2.5 Turbo Pro $0.07 per s; v3 $0.14 per s | Cloud | Low | API | 2026-10-18 |
| Luma Ray3.x [81] | Cloud I2V | Plus $30 per 10,000 credits; privacy: avoid | Cloud | Low | App and API | 2026-10-18 |
| Runway Gen-4 family [80] | Cloud I2V | Free 125 credits; Standard $15; Pro $35; Max $95 | Cloud | Low | App and API | 2026-10-18 |
| Video2X 6.4.0 [79] | Video upscale and interpolation | Free, AGPL-3.0 | Vulkan GPU, AVX2 CPU | Medium | CLI | 2026-10-18 |
| RunPod [83] | Rented GPUs | RTX 4090 $0.34 (community) or $0.89 (secure) per hour; 5090 $0.69 or $1.19; volume disk $0.10 per GB-month running | Cloud | Medium | API | Page dated 2026-10-08 |
| Replicate, fal [52][88] | Hosted model APIs | Per-use | Cloud | Low | API | 2026-10-18 |

---

## Techniques

- **Copy-stand scanning** (camera or phone parallel to the item, even light, level, remote trigger): [5][6].
- **Film-base sampling for negatives** (include unexposed border, sample base colour first, linear working profile): [13].
- **Non-generative first**: per-channel levels, cast removal, healing brush before any model (Q2).
- **Fidelity-controlled face restoration with blend-back** (CodeFormer `w`, 40 to 60 percent mask blend): [15].
- **Tiled processing** (`-t` in Real-ESRGAN, `--tile`, tiled VAE in SUPIR and SeedVR2) to fit limited VRAM: [18][22][24].
- **Alpha matting and edge decontamination** (`rembg -a`, `-vm`, `-dc`): [55].
- **Monocular depth to 2.5D parallax**, with depth softening over faces (M): [58][60].
- **Paper-theatre layering** to avoid generative fill (M).
- **Delaunay-triangle landmark morph** with eye alignment and ease curves: [65].
- **Optical-flow interpolation** for short gaps (`--exp` in RIFE; `minterpolate`): [62][102].
- **First/last-frame conditioning** (labelled generated): [67][82].
- **Reference-conditioned editing** with explicit "keep the same facial features" clauses and single-change steps: [34].
- **Style LoRA from the maker's own artwork** instead of a person LoRA: [46][47].
- **Seed locking and multi-take selection**, picking the take with least change (M).
- **Identity gate**: face-embedding similarity between source and output crops; scriptable QA (M, UNVERIFIED).
- **Line-up test with confirmed insiders** for likeness, in the vertical slice (M).
- **Metadata labelling**: IPTC Digital Source Type URIs written to XMP; `steps.csv` cue sheet: [89][90][96].
- **Fully offline run**: pre-download weights, then disconnect or use `--offline`: [49][55].

---

## Pitfalls and ethics

1. **Likeness theatre.** Demos use clean modern portraits. Nothing I reached shows these tools on faded, low-resolution or black-and-white family photos. Treat every quality claim as untested on archival photos until the bake-off.
2. **Restoration is generation.** Upscalers, face restorers and colourisers invent texture, features and colours; morphs and image-to-video invent frames. Each tool row states what is invented so the maker can decide and label.
3. **Plastic skin and identity drift.** GFPGAN may shift identity [17]; SeedVR2 had a "plastic" bug [24]; PULSE-style methods make fictional faces [30]. Face restore only at high fidelity, blend back, and check with a confirmed insider.
4. **Stale tutorials.** FILM (archived 2025-10-14), Microsoft Old Photos (archived 2026-10-03) and DeOldify (archived 2024-10-19) are read-only [61][25][29]; IP-Adapter plus is maintenance-only [44]; InstantID, PuLID and CodeFormer show no dated activity after 2024, 2024 and 2023 respectively on the pages I read [40][41][15]; the first Nano Banana model is being retired [51]; Wan 2.1 posts are superseded by Wan 2.2 [69]. Check dates and licences before following a 2023 to 2025 guide.
5. **Fake sites and affiliate listicles.** FramePack, DepthFlow and CodeFormer READMEs all warn that look-alike sites and apps are unofficial or fraudulent [72][60][15]. Use the GitHub repo or the vendor's own page only.
6. **Licence traps.** Non-commercial: SUPIR [21], FLUX.1 Kontext dev [33], FLUX.2 dev and klein 9B [38], InfiniteYou model [42], Depth Anything V2 Base/Large [58], InstantID/insightface [40], rembg `bria-rmbg` weights [55]. Copyleft: Upscayl, DepthFlow, Video2X are AGPL; ComfyUI, chaiNNer and Krita plugin are GPL-3.0. Fine for a private gift; reassess if the work will be screened at a ticketed event.
7. **Cloud privacy.** See Q7. Family photos include children and third parties; default to local processing, or to paid tiers whose terms say no training, and only for cleared photos.
8. **Voice.** Voice cloning, lip-sync and "talking photo" tools are out of scope under Principle 4. *Roadrunner* is the warning [98]. Image-to-video prompts must not ask for speech.
9. **Animating the dead.** No face or expression animation of people who have died without the family's say (Principle 5). Environmental motion and parallax are the safe alternatives.
10. **Reconstructions must be visibly reconstructions.** Never photoreal; always the house stylisation plus caption (R6). Never use a generated face and a real name together in a way that implies a record.
11. **Provenance is partial.** SynthID marks Google outputs, not local restoration [50][82]; MP4 containers may drop IPTC fields (M). The manifest and credits are the real record.
12. **Ephemeral outputs.** Veo videos are deleted after 2 days [82]; Replicate API outputs after 1 hour [88]; models get retired [51]. Download and log immediately.
13. **Hardware and drivers.** The Epson V600 is discontinued and Epson's pages list XP-era operating systems [9][10]; test the scanner on the maker's machine early, or use VueScan [11].
14. **Consistency.** Mixing heavily restored and untouched photos in one chapter breaks the look; decide a level per chapter.
15. **Sprawl.** Exploring models is addictive; Principle 6 says one polished chapter first. Timebox tool trials.

---

## Open questions / gaps

1. **Archival-photo evidence is missing.** Plan a five-photo bake-off in week 1 on stand-in photos with the same defects, not from her archive: faded colour print, small black-and-white print, soft group snapshot with small faces, torn print, 1990s low-resolution digital file. Stand-in sources: the maker's own prints, a consenting relative's print (if that relative is a confirmed insider), or public-domain prints. The follow-up (Q6) found candidates for four of the five; none yet for the group snapshot or the 1990s digital file. Run through R2 (Real-ESRGAN + CodeFormer, SeedVR2, Qwen-Image-Edit-2511 or Kontext, one cloud edit model) and have the maker and confirmed insiders judge whether each version keeps the same person and photo. The insiders list (`GATHER.md`) does not exist yet, so the maker judges alone for now. The real-photo line-up moves to the vertical slice, after the "who is in on it" decision.
2. **Creator threads, Reddit and YouTube** (restraint prompts for old-photo animation, colourisation practice, Minecraft-style conversions) could not be searched because the budget ran out. A follow-up search pass is needed.
3. **Terms pages not read:** OpenAI (403), Runway terms (404), Midjourney (403), Kling, MyHeritage, Remini/Bending Spoons, fal.ai, Hugging Face Spaces, Adobe consumer terms, Topaz cloud processing. All UNVERIFIED and treated as "do not upload".
4. **FADGI numbers** (3rd edition, 2023) for ppi, bit depth and colour were not readable [4]; the 600 and 3200 to 4000 ppi guidance is partly my judgment.
5. **Local VRAM for several routes is not stated in any source I read:** FLUX.1 Kontext dev, Qwen-Image-Edit-2511, Wan FLF2V, Wan2.2 14B with FP8 or GGUF. Test on the maker's actual GPU.
6. **Which tier is the maker on?** The Charter lists no GPU. The sandbox has none either.
7. **Premiere or private gift?** It decides whether non-commercial and AGPL tools are acceptable.
8. **Gemini 2.5 Flash Image status:** pricing page says deprecated with shutdown 2026-10-02; image docs say only "legacy" [50][51]. Re-check before using.
9. **First/last-frame products:** Kling, Runway and Luma keyframe support and pricing not confirmed (Luma's pricing page does not cover keyframes [81]).
10. **ExifTool and C2PA signing** were not run here; the signing certificate story for a private project is unresearched [93].
11. **Home-video capture** (VHS, Hi8, MiniDV, 8 mm) and deinterlacing were not researched.
12. **Colourisation accuracy:** reference-based colourisation from the family's own colour photos is not evaluated.
13. **Whether Apple unified memory** maps to the VRAM tiers is unverified.
14. **Family decision (Principle 5):** are animated faces of the deceased acceptable to this family? Ask before any such work.
15. **Immersity AI and other cloud 2.5D services** were not checked; DepthFlow's own CLI documentation (depth.tremeschin.com) was not fetched.

---

## Sources

Fetched pages were read on 2026-10-18. "Snippet" means only a search-result summary was seen and the page was not fetched. Source 102 is a local test in the sandbox.

1. Scanning Your Personal Collections (Library of Congress Personal Digital Archiving series) — https://www.digitalpreservation.gov/personalarchiving/documents/scanning_collections.pdf — PDF created 2011-10-06 — 300 dpi for documents; 400 to 600 for enlargements; above 600 unnecessary; greyscale vs colour; `yyyymmdd` names; two copies.
2. Digitizing Family Papers (U.S. National Archives) — https://www.archives.gov/preservation/family-archives/digitizing.html — undated — Latin-letter names, 3-2-1 backup, keep originals, who/what/where/when; defers ppi to FADGI and IPI.
3. Family Archives (U.S. National Archives) — https://www.archives.gov/preservation/family-archives — undated — landing page linking digitizing, handling, storing.
4. FADGI Technical Guidelines for Digitizing Cultural Heritage Materials page — https://www.digitizationguidelines.gov/guidelines/digitize-technical.html — 3rd edition 2023 — page lists the guidelines but no numbers.
5. Scanning Film (John Hultgren) — https://hultgren.org/articles/scan/index.php — 2023-11-10 — camera-scanning setup with macro lens, stand, holders; no DPI.
6. Is Google PhotoScan still available in 2026? (Lightroom Tools blog) — https://lightroom-tools.com/blog/google-photoscan-still-available-2026 — 2026-05-18 — PhotoScan free but frozen; four-dot glare removal; alternatives.
7. PhotoScan by Google Photos (AppBrain listing) — https://www.appbrain.com/app/photoscan-by-google-photos/com.google.android.apps.photos.scanner — snippet only — last update 2023-07-24.
8. Review: Epson Perfection V600 vs. V850 Photo Scanners (Larry Jordan) — https://dev.larryjordan.com/articles/product-review-epson-v600-vs-v850-photo-scanners/ — snippet only — Dmax 3.5 vs 4.0; V850 better dust removal; interpolation caveat.
9. Epson Perfection V600 Photo Scanner (Epson America) — https://epson.com/For-Home/Scanners/Photo-Scanners/Epson-Perfection-V600-Photo-Scanner/p/B11B198011 — undated, © 2026 — specs; marked Discontinued.
10. Epson Perfection V850 Pro (Epson America) — https://epson.com/For-Home/Scanners/Photo-Scanners/Epson-Perfection-V850-Pro-Photo-Scanner/p/B11B224201 — undated — $1,999; Dmax 4.0; cart error.
11. VueScan — https://www.vuescan.com/ — 9.8.59 dated 2026-09-26 — 8,000+ scanners; Infrared Clean; Restore Fading; no price on page.
12. Negative Lab Pro — https://www.negativelabpro.com/ — v3.1, © 2025 — Lightroom Classic plug-in; no price on page.
13. darktable negadoctor module — https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/negadoctor/ — undated — negative conversion workflow.
14. Photomyne — https://www.photomyne.com/ — app v6.6.2, © 2015-2026 — $59.99 per year after 3-day trial; AI restoration extra credits.
15. CodeFormer (sczhou) — https://github.com/sczhou/CodeFormer — last news 2023-07-20 — `w` fidelity; CLI; NTU S-Lab licence; unofficial-site warning.
16. Towards Robust Blind Face Restoration with Codebook Lookup Transformer — https://arxiv.org/abs/2206.11253 — 2022 — ill-posed problem; fidelity-quality module.
17. GFPGAN (TencentARC) — https://github.com/TencentARC/GFPGAN — undated — v1.3 may slightly change identity; Apache-2.0.
18. Real-ESRGAN (xinntao) — https://github.com/xinntao/Real-ESRGAN — undated — ncnn portable builds; BSD-3; model list.
19. GFPGAN and CodeFormer guide (Replicate) — https://replicate.com/guides/upscaling-images/gfpgan-and-codeformer — snippet only — likeness advice.
20. CodeFormer vs ESRGAN: Enhance faces (Segmind) — https://blog.segmind.com/codeformer-vs-esrgan/ — snippet only — example where result bore little resemblance.
21. SUPIR (Fanghua-Yu) — https://github.com/Fanghua-Yu/SUPIR — undated — non-commercial; low-memory options.
22. ComfyUI-SUPIR (kijai) — https://github.com/kijai/ComfyUI-SUPIR — undated — VRAM tests; SUPIR now in ComfyUI core.
23. SeedVR / SeedVR2 (ByteDance-Seed) — https://github.com/ByteDance-Seed/SeedVR — ICLR 2026 acceptance noted 2026-01-27 — Apache-2.0; over-generation warning.
24. ComfyUI-SeedVR2_VideoUpscaler (numz) — https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler — v2.5.24 dated 2025-12-24 — VRAM tiers; CLI; plastic-output fix.
25. Bringing Old Photos Back to Life (Microsoft) — https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life — archived 2026-10-03 — research-only, MIT.
26. Upscayl — https://github.com/upscayl/upscayl — v2.15 — Vulkan required; AGPL-3.0.
27. chaiNNer — https://github.com/chaiNNer-org/chaiNNer — undated — node GUI; GPL-3.0; CPU fallback.
28. DDColor — https://github.com/piddnad/DDColor — last news 2024-01-28 — Apache-2.0; CLI.
29. DeOldify (jantic) — https://github.com/jantic/DeOldify — archived 2024-10-19 — MIT; accuracy caveats.
30. PULSE (adamian98) — https://github.com/adamian98/pulse — CVPR 2020 — outputs are imaginary faces.
31. Topaz Labs pricing — https://www.topazlabs.com/pricing — no date, 2026 offers — Photo, Gigapixel, Video, Studio prices; local unlimited.
32. Topaz Labs privacy policy — https://www.topazlabs.com/privacy-policy — last updated 2024-10-03 — does not address local vs cloud or training.
33. FLUX.1 Kontext [dev] — https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev — undated — 12B editing model; non-commercial, gated; API outputs carry C2PA.
34. FLUX.1 Kontext dev ComfyUI tutorial — https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev — undated — identity-preserving prompt patterns.
35. Qwen-Image (QwenLM) — https://github.com/QwenLM/Qwen-Image — Edit-2509 announced 2025-09-22, Edit-2511 2025-12-23, Qwen-Image-2.0 announced 2026-02-10 — Apache-2.0.
36. Qwen-Image-Edit-2511 — https://huggingface.co/Qwen/Qwen-Image-Edit-2511 — undated — identity consistency; 20B; Apache-2.0.
37. Qwen-Image-Edit ComfyUI tutorial — https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit — undated — fp8 files; scale to about 1 MP.
38. FLUX.2 (Black Forest Labs) — https://github.com/black-forest-labs/flux2 — dev 2025-11-25, klein 2026-01-15 — variants and licences.
39. Z-Image (Tongyi-MAI) — https://github.com/Tongyi-MAI/Z-Image — Turbo 2025-11-26, base 2026-01-27 — 6B, Apache-2.0.
40. InstantID — https://github.com/instantX-research/InstantID — last log 2024-07-18 — one face; insightface non-commercial.
41. PuLID — https://github.com/ToTheBeginning/PuLID — last entry 2024-10-31 — FLUX 16 GB; Apache-2.0.
42. InfiniteYou — https://github.com/bytedance/InfiniteYou — March 2025 — VRAM figures; model CC-BY-NC.
43. USO — https://github.com/bytedance/USO — 2025-08-27 — style plus subject; 16 to 18 GB fp8.
44. ComfyUI_IPAdapter_plus — https://github.com/cubiq/ComfyUI_IPAdapter_plus — maintenance mode 2025-04-14 — FaceID notes.
45. Kontext-Style-Loras (Owen777) — https://huggingface.co/Owen777/Kontext-Style-Loras — undated — 22 style LoRAs; no licence stated.
46. ai-toolkit (ostris) — https://github.com/ostris/ai-toolkit — © 2026 — training suite; MIT.
47. fluxgym — https://github.com/cocktailpeanut/fluxgym — undated — 12/16/20 GB LoRA training; MIT.
48. Krita AI Diffusion (Acly) — https://github.com/Acly/krita-ai-diffusion — undated — GPL-3.0; 6 GB recommended.
49. ComfyUI — https://github.com/comfyanonymous/ComfyUI — undated — GPL-3.0; `--offline`; workflow JSON.
50. Gemini API image generation docs — https://ai.google.dev/gemini-api/docs/image-generation — undated — editing; reference limits; SynthID; model names.
51. Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing — undated — Veo 3.1 and image prices; free vs paid data use; 2.5 Flash Image deprecation note.
52. fal.ai pricing — https://fal.ai/pricing — undated, 2026 — Kling and Nano Banana Edit prices.
53. The Cross-Age LFW (CALFW) — https://arxiv.org/abs/1708.08197 — 2017 — 10 to 17 percent accuracy drop across ages.
54. MapartCraft — https://github.com/rebane2001/mapartcraft — undated — browser mapart generator; GPL-3.0.
55. rembg — https://github.com/danielgatis/rembg — undated — CLI, CPU, MIT, cloud back-end warning.
56. SAM 2 — https://github.com/facebookresearch/sam2 — SAM 2.1 2024-09-30 — Apache-2.0.
57. SAM 3 — https://github.com/facebookresearch/sam3 — SAM 3.1 2026-03-27 — gated; CUDA 12.6+.
58. Depth Anything V2 — https://github.com/DepthAnything/Depth-Anything-V2 — undated — licences by size.
59. Depth Anything 3 — https://github.com/ByteDance-Seed/Depth-Anything-3 — 2025-11-14 — licences by size; `da3` CLI.
60. DepthFlow (BrokenSource) — https://github.com/BrokenSource/DepthFlow — undated — AGPL-3.0; fake-site warning.
61. FILM (google-research/frame-interpolation) — https://github.com/google-research/frame-interpolation — archived 2025-10-14 — Apache-2.0; TF2/CUDA 11.2.
62. RIFE (hzwer/ECCV2022-RIFE) — https://github.com/hzwer/ECCV2022-RIFE — README items to 2024-08 — MIT; `inference_img.py`.
63. Practical-RIFE — https://github.com/hzwer/Practical-RIFE — model 4.26 on 2024-09-21 — MIT.
64. ComfyUI-Frame-Interpolation — https://github.com/Fannovel16/ComfyUI-Frame-Interpolation — undated — VFI model list; MIT.
65. LearnOpenCV FaceMorph example — https://github.com/spmallick/learnopencv/tree/master/FaceMorph — undated — folder listing only (code files and landmark files).
66. SAM: Style-based Age Manipulation — https://github.com/yuval-alaluf/SAM — SIGGRAPH 2021 — StyleGAN age transform; NVIDIA GPU.
67. Wan2.1-FLF2V-14B-720P — https://huggingface.co/Wan-AI/Wan2.1-FLF2V-14B-720P — undated — first/last frame; 720p only; Apache-2.0.
68. Wan2.1 — https://github.com/Wan-Video/Wan2.1 — FLF2V release note 2025-04-17 — T2V-1.3B needs 8.19 GB; I2V prompt example.
69. Wan2.2 — https://github.com/Wan-Video/Wan2.2 — released 2025-07-28 — variants, VRAM, Apache-2.0.
70. Wan2.2 ComfyUI tutorial — https://docs.comfy.org/tutorials/video/wan/wan2_2 — undated — 5B fits 8 GB with offload; FLF2V workflow.
71. Wan2.2-Lightning — https://huggingface.co/lightx2v/Wan2.2-Lightning — I2V LoRA 2025-08-07 — 4-step; artefacts at large motion.
72. FramePack (lllyasviel) — https://github.com/lllyasviel/FramePack — latest news 2025-07-14 — 6 GB; Apache-2.0; speed; fake-site warning.
73. LTX-Video (Lightricks) — https://github.com/Lightricks/LTX-Video — LTX-2 announced 2025-10-23 — 0.9.8 variants; Apache-2.0.
74. LTX-2 (Lightricks) — https://github.com/Lightricks/LTX-2 — undated — LTX-2.5 recommended; keyframe interpolation; 66 GiB download.
75. ComfyUI-LTXVideo — https://github.com/Lightricks/ComfyUI-LTXVideo — undated — 32 GB+ VRAM.
76. HunyuanVideo-1.5 — https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 — 2025-11-20 — 8.3B; 14 GB minimum.
77. WanGP (deepbeepmeep) — https://github.com/deepbeepmeep/Wan2GP — v18.17 on 2026-10-15 — 6 GB select models.
78. LivePortrait — https://github.com/KwaiVGI/LivePortrait — changelog to 2025-06-01 — deepfake-risk disclaimer.
79. Video2X — https://github.com/k4yt3x/video2x — v6.4.0 — AGPL-3.0; Vulkan.
80. Runway pricing — https://runway.com/pricing (redirected from runwayml.com/pricing) — undated — plans and credits.
81. Luma pricing — https://lumalabs.ai/pricing — undated — plans, Ray3.x credits.
82. Veo 3.1 in the Gemini API — https://ai.google.dev/gemini-api/docs/veo — Veo 3.1 Preview updated Jan 2026, Lite Mar 2026 — image-to-video, `lastFrame`, `allow_adult`, SynthID, 2-day storage.
83. RunPod pricing — https://www.runpod.io/pricing — updated 2026-10-08 — GPU hourly prices.
84. Gemini Apps Privacy Hub — https://support.google.com/gemini/answer/13594961 — last updated 2026-10-13 — training, human review, retention.
85. Gemini API Additional Terms of Service — https://ai.google.dev/gemini-api/terms — effective 2026-03-23, updated 2026-04-28 — unpaid vs paid data use.
86. Luma Labs Privacy Policy — https://lumalabs.ai/legal/privacy-policy — last updated 2026-04-20 — model training as a purpose.
87. Adobe Firefly generative AI approach — https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html — undated, © 2026 — no training on customer content.
88. Replicate data retention — https://replicate.com/docs/topics/predictions/data-retention — undated — API outputs removed after one hour.
89. IPTC Digital Source Type vocabulary — https://cv.iptc.org/newscodes/digitalsourcetype/ — undated; retirements dated 2022-06-14 and 2024-09-17 — term list and definitions.
90. IPTC Photo Metadata User Guide — https://www.iptc.org/std/photometadata/documentation/userguide/ — undated — Digital Source Type guidance.
91. C2PA — https://c2pa.org/ — page updated 2026-01-08 — Content Credentials standard.
92. Content Credentials — https://contentcredentials.org/ — page updated 2025-10-06 — provenance feature overview.
93. c2pa-rs — https://github.com/contentauth/c2pa-rs — beta, supports spec 2.4 — Rust SDK; c2patool moved to its own repo.
94. Partnership on AI Responsible Practices for Synthetic Media — https://syntheticmedia.partnershiponai.org/ — launched Feb 2023, case studies added 2024 — consent, disclosure, direct vs indirect.
95. Archival Producers Alliance GenAI guidelines — https://www.archivalproducersalliance.com/genai-guidelines — undated; guidelines PDF titled Sept 2024 (not readable) — landing page.
96. APA GenAI Best Practices Tool Kit — https://www.archivalproducersalliance.com/tool-kit-for-documentaries — undated — transparency tips, credits, cue sheet.
97. Wikimedia Commons: AI-generated media — https://commons.wikimedia.org/wiki/Commons:AI-generated_media — undated — document prompt, name engine, list authors.
98. Roadrunner: A Film About Anthony Bourdain (Wikipedia) — https://en.wikipedia.org/wiki/Roadrunner:_A_Film_About_Anthony_Bourdain — undated — AI voice controversy.
99. What Jennifer Did (Wikipedia) — https://en.wikipedia.org/wiki/What_Jennifer_Did — undated — suspected AI images.
100. They Shall Not Grow Old (Wikipedia) — https://en.wikipedia.org/wiki/They_Shall_Not_Grow_Old — undated — restoration, colourisation, criticisms.
101. MyHeritage (Wikipedia) — https://en.wikipedia.org/wiki/MyHeritage — undated — Deep Nostalgia launch and scale.
102. Local sandbox test (this session, 2026-10-18) — ffmpeg 6.1.1 and ImageMagick `convert`; commands `convert a.png b.png -morph 14`, `ffmpeg ... xfade`, `zoompan`, `minterpolate=fps=48:mi_mode=mci`, and frame-sequence assembly ran without error on synthetic images; confirms the commands run, not that results are good on real faces.


---

## Follow-up research (round 1)

Researcher: Sonnet · Run 2026-10-18 (Sunday) · Answers eight follow-up questions from `reviews/ai-imagery-round1.md`. Sources continue the numbering above (103 onward, listed at the end of this section). Marks as before: **UNVERIFIED** (not confirmed), **(M)** (my judgment or background knowledge), **ESTIMATE** (computed).

**How this round was made, and its limits (read first).**
- **The session is not the maker's computer.** The relayed request said the session was "open on my local system". What this subagent can see is a cloud Linux VM: Ubuntu 24.04.5, kernel 6.18.44 "fc" build, 4 vCPU Xeon at 2.10 GHz, 15 GiB RAM, no GPU, no scanner, no `/mnt/c`, no WSL markers, working directory `/home/user` [103]. Nothing about the maker's Windows PC, GPU, disk or scanner is reachable from here. Every "run" below happened on that VM; Windows behaviour is cited from official pages or marked UNVERIFIED.
- **The shared WebSearch budget was exhausted.** Two search attempts at the start of Q6 returned "budget used up". I did not search by other means. Q3, Q4, Q5 and most of Q1 rest on direct fetches and local runs. Q6 rests on direct fetches of Wikimedia Commons category and file pages. Q7 and Q8 could not be answered properly; see their notes. Blocked or empty fetches: reddit.com, theverge.com, journals.sagepub.com (403), technewsworld.com (403), catalog.archives.gov (empty app shell), the GitHub API through `gh` (not enabled for this session).
- Fetched pages were treated as data. Fetch output was summarised by a small model, so quotes were checked against that summary, not the raw page. Downloads (Real-ESRGAN zips, ExifTool source, rembg models) went into their own empty directories. The only downloaded executable I ran was the Real-ESRGAN Linux binary. I also installed packages from PyPI and PyTorch's CPU index into a virtual environment, and Ubuntu's Vulkan drivers through apt on the VM.

### Status at a glance

| # | Question | Status | Short answer |
|---|---|---|---|
| 1 | Windows install path, no-GPU toolchain | Partly answered | Native Windows is the sane default for all five tools; WSL is the fallback, and the one real reason to need it is a PC with no Vulkan driver. No Windows run was possible (UNVERIFIED); every command was run on Linux instead and dated. |
| 2 | Maker's hardware | **Not answerable here** | The sandbox is not the maker's PC. Paste-ready PowerShell commands are below (not run). The tier table stays hypothetical. |
| 3 | `realesr-general-x4v3` in the ncnn portable release | Answered: **no** | Not in the Windows or Ubuntu portable zips, and the exact flag fails silently with a black image. |
| 4 | Veo 3.1 `personGeneration` for image-to-video | Answered, with one gap | `allow_adult` is the only I2V value. The Gemini API page says nothing about children; Google's Vertex page says child requests are rejected, with support codes. No page says "silently altered". Child-photo behaviour needs one cheap test. |
| 5 | ExifTool, XMP DigitalSourceType | Answered (Linux run of 13.59) | Commands and outputs below. Write the full IPTC URI, not the friendly name. ffmpeg strips the tag from MP4; tag after the last export. |
| 6 | Public-domain stand-in photos | Answered, partial | Four candidates read and viewed (faded colour, creased, cracked and torn, faded snapshot). Two are public domain, one is "no known copyright restrictions", one is CC BY-SA 3.0. |
| 7 | Creator evidence on archival inputs | **Not met (0 of 3)** | Needs a search pass. What I could reach (vendor and tool pages) shows no old-photo examples. |
| 8 | Family reactions to animating the dead | **Partly met** | First-hand words exist only inside one vendor-curated post (11 named users). No independent first-hand account reached. A 2025 academic paper is the lead to chase. |

### Corrections to earlier text in this note and the playbook (applied in the round 1 scribe pass)

1. **Recipe R2 step 2 (line 370 above) is wrong.** `realesrgan-ncnn-vulkan ... -n realesr-general-x4v3 -s 2` does not work with the portable release (Q3). It writes an all-black image and exits 0. Use `-n realesrgan-x4plus` for photos. `playbooks/ai-imagery.md` line 94 quotes the same command and needs the same fix.
2. **Q9 CPU time for Real-ESRGAN is too optimistic.** The table says "about 1 to 7.5 h for 150 photos (0.5 to 3 min each, ESTIMATE)". Measured on this VM through a software Vulkan driver (Q3 timings): 72 s for a 220x220 input and 241 s for a 440x440 input with the photo model, roughly 1,250 to 1,500 s per megapixel of input. A 600 ppi scan of a 4x6 print is 8.6 MP. Treat CPU-only Real-ESRGAN as "small crops or a handful of photos", and send the rest to a GPU or cloud. A real Vulkan GPU or iGPU will be far faster; that is unmeasured.
3. **rembg's default model changed.** In rembg 2.0.85 the default (`-m`) is `bria-rmbg`, a 1.02 GB download [106][123]. Earlier notes assumed u2net. Older tutorials that say "rembg downloads a 170 MB model" are out of date.
4. **ImageMagick 7 on Windows uses `magick`, not `convert`.** All tested ImageMagick commands in [102] used IM6 `convert`. On Windows write `magick ...` (the official page's own examples are `magick logo: logo.gif` [120]). Windows also ships its own `convert.exe` (a disk utility), which is why bare `convert` is a trap there (M).

### Q1. Windows install path for the no-GPU toolchain

**Answer.** Native Windows is the sane default. WSL is not required for any of the five tools. I could not run anything on Windows, so every "Windows install" cell below comes from the vendor's page and is UNVERIFIED on a real PC. I ran the equivalent command on the Linux VM and dated it.

| Tool | Native Windows route (source) | One command, run 2026-10-18 on Linux (Windows run UNVERIFIED) | Result |
|---|---|---|---|
| ffmpeg | `winget install ffmpeg` (full build) or `winget install "FFmpeg (Essentials Build)"`; gyan.dev lists release 9.0.2 dated 2026-09-19 [122]. ffmpeg.org links gyan.dev and BtbN for Windows builds; it shows 9.0.2 (2026-09-18) and 8.1.3 (2026-09-21) [121]. | `ffmpeg -v error -y -f lavfi -i testsrc=duration=2:size=320x240:rate=24 -f lavfi -i sine=frequency=440:duration=2 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest clip.mp4` | Made a 31,449-byte clip with ffmpeg 6.1.1 (Ubuntu build, older than the 9.x current) [105]. Re-check earlier xfade/zoompan/minterpolate recipes on 9.x. |
| ImageMagick 7 | `winget install ImageMagick.Q16-HDRI` (official package id) or the installer `ImageMagick-7.1.2-34-Q16-HDRI-x64-dll.exe`; a portable `.7z` also exists. The page says that if something fails "you likely need `vcomp140.dll`" [120]. | Windows form: `magick scan.tif -resize 50% out.tif` (not run: no IM7 here). Run instead: `convert scan_0001.tif -resize 50% im_out.tif` on IM 6.9.12. | Worked, and the TIFF's XMP DigitalSourceType survived the resize; `-strip` removed it [105]. |
| Real-ESRGAN ncnn | Download `realesrgan-ncnn-vulkan-20220424-windows.zip` from release v0.2.5.0 (45,474,481 bytes) [110], unzip, run `.\realesrgan-ncnn-vulkan.exe`. Needs a Vulkan driver (Q3). | `./realesrgan-ncnn-vulkan -i input.jpg -o o_x4plus.png -n realesrgan-x4plus` (Ubuntu zip, software Vulkan) | 880x880 output in 72 s on 4 vCPU [104]. With no Vulkan driver at all it prints `vkCreateInstance failed -9` and `invalid gpu device`, exit 255 [104]. |
| rembg | Python 3.11 to 3.13 only (`>=3.11,<3.14`); `pip install "rembg[cpu,cli]"` [123]. On Windows use a venv, for example `py -3.12 -m venv .venv` (M). | `rembg i -m u2netp in.jpg out.png` | rembg 2.0.85, onnxruntime 1.31.0, Python 3.13.16. `u2netp` (4.6 MB) took 2.6 s including download. Default `bria-rmbg` (1,024,331,469 bytes) took 82 s the first time and 33.5 s cached, for a 220x220 image [106]. `u2net` (176 MB) took 9.7 s including download. |
| Depth Anything V2 Small | Apache-2.0 licence; 24.8M parameters; `pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")`; the repo has no Windows notes and its sample code falls back to CPU [124][125]. Install CPU PyTorch from `https://download.pytorch.org/whl/cpu`, then `pip install transformers pillow`. | `pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")(image)` | torch 2.14.1+cpu, transformers 5.20.1. Load 12.7 s including a 95 MB model download; 0.31 to 0.40 s per image on a 220x220 input [106]. |
| ExifTool | See Q5. | See Q5. | See Q5. |

**When WSL is worth it (M, partly sourced).**
- Install is one command, `wsl --install`, from an administrator PowerShell, then a restart; it needs Windows 10 2004 (build 19041) or later, or Windows 11. Microsoft's page was updated 2026-06-02 [126].
- The reason to use it here: a PC with no working Vulkan driver cannot run the Windows `realesrgan-ncnn-vulkan.exe` at all. On the Linux VM, installing Ubuntu's `mesa-vulkan-drivers` (the llvmpipe software driver) made the same binary run on CPU [104]. Whether that works inside WSL is UNVERIFIED.
- Otherwise WSL adds file-sharing friction between Windows and Linux paths (M) and gains nothing for these five tools.
- Python tools: pin one version (3.12 or 3.13). Tested here on 3.13.16; rembg's own limit is below 3.14 [123].

### Q2. Maker's hardware inventory (charter review 1.3.2)

**Not obtained.** The session is a cloud VM, not the maker's PC (see "How this round was made"), so GPU model, VRAM, free disk and scanner are unknown. For the record, the VM itself: Intel Xeon 2.10 GHz, 4 vCPU, 15 GiB RAM, about 23 GB free of 252 GB, no GPU, no scanner [103]. Do not use these numbers for the tier table.

**Paste-ready PowerShell for the maker (not run: UNVERIFIED).** One block, one paste, and they send back the text:

```powershell
(Get-CimInstance Win32_OperatingSystem) | Select-Object Caption,BuildNumber
Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
"{0:N1} GiB RAM" -f ((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB)
Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
Get-PSDrive -PSProvider FileSystem | Select-Object Name,@{n='FreeGiB';e={[math]::Round($_.Free/1GB,1)}}
Get-PnpDevice -Class Image -PresentOnly | Select-Object FriendlyName,Status
```

- **Do not trust `AdapterRAM` for VRAM.** Microsoft documents it as a `uint32` of bytes [127], so by type it cannot report more than about 4 GiB (my inference from the type; the page does not say so). That is why the block asks `nvidia-smi` for VRAM. On a PC without an NVIDIA card, `nvidia-smi` will fail; then read Task Manager, Performance, GPU, "Dedicated GPU memory" (M).
- **Vulkan check, free:** run `realesrgan-ncnn-vulkan.exe -i input.jpg -o out.png` once. On Linux the first lines list each Vulkan device as `[0 <name>]`; `invalid gpu device` means none [104]. That one run answers "can this PC use the ncnn tools".
- Scanner: `Get-PnpDevice -Class Image` lists WIA scanners and cameras (M). Also ask: model number, whether it takes film holders, and whether it sits in a room the mother uses (review 1.7).

### Q3. Does the Real-ESRGAN ncnn portable release include `realesr-general-x4v3`, and what flag selects it?

**Answer: No. There is no flag, because the weights are not in the portable zips.** Checked in the release assets, not the README.

- **Assets.** Release v0.2.5.0 carries the three portable zips `realesrgan-ncnn-vulkan-20220424-{windows,ubuntu,macos}.zip` [108]. I downloaded the Windows and Ubuntu zips and listed them [110][111]. The model files in both are exactly: `realesr-animevideov3-x2`, `-x3`, `-x4`, `realesrgan-x4plus`, `realesrgan-x4plus-anime` (each a `.bin` and `.param`). Nothing named `general`. Nothing for `realesrnet-x4plus` either, although the binary's `-h` text lists it.
- **Where the general model lives.** Release v0.3.0 (page shows "20 Sep", no year) adds `realesr-general-x4v3.pth` and `realesr-general-wdn-x4v3.pth` [109]. These are PyTorch weights, not ncnn `.param`/`.bin`. They download from the v0.2.5.0 URL path (4,885,111 bytes each by HTTP header) and 404 under the v0.3.0 path. The `-dn` denoise option is described for the Python script, not the ncnn binary [109]; the ncnn `-h` has no `-dn` [104].
- **README.** The portable-executable section lists four models; `realesr-general-x4v3` appears only in the Updates section, with no ncnn download [112]. A separate repo, Real-ESRGAN-ncnn-vulkan, has releases v0.2.0 and v0.1.3.2 [113]; its v0.2.0 Windows zip (2,159,606 bytes) holds only the exe, two DLLs, a licence and a README, with no models folder.
- **What happens if you try anyway** (run 2026-10-18, Linux build with software Vulkan [104]): `-n realesr-general-x4v3` prints `fopen .../models/realesr-general-x4v3.param failed`, `find_blob_index_by_name data failed`, **exits 0**, and writes a valid 880x880 PNG that is **entirely black** (mean 0, standard deviation 0). A learner would see "success". Always check output visually or by file size.
- **Working command for photos:** `realesrgan-ncnn-vulkan.exe -i in.png -o out.png -n realesrgan-x4plus -s 2` (`-s` accepts 2, 3, 4; `-t` sets tile size; `-f` sets format) [104][110]. The shipped `realesr-animevideov3` models are tiny and fast (3.2 s for a 220x220 input at `-s 2`) but are built for anime video, not photos [112].
- **Timings on this VM** (4 vCPU Xeon, software Vulkan, `realesrgan-x4plus`): 220x220 input to 880x880 in 72 s; 440x440 input at `-s 2` to 880x880 in 241 s [104]. A real GPU will differ; unmeasured.
- **If the general model is wanted:** convert the `.pth` to ncnn yourself, or use the Python script (needs PyTorch). I did not fetch any conversion guide: UNVERIFIED.

### Q4. Veo 3.1 `personGeneration` for image-to-video

Read `ai.google.dev/gemini-api/docs/veo` directly on 2026-10-18. The page footer says "Last updated 2026-10-08 UTC" [114].

| Mode | Veo 3.1, 3.1 Fast, 3.1 Lite | Veo 3 and 3 Fast (deprecated) |
|---|---|---|
| Text-to-video and extension | `allow_all` only | `allow_all` only |
| Image-to-video, interpolation, reference images | **`allow_adult` only** | Image-to-video: `allow_adult` only (other modes not stated) |

- **Confirmed:** `allow_adult` is the only value for image-to-video on this API. `dont_allow` appears nowhere on the page, and no default is stated. In EU, UK, CH and MENA locations `allow_adult` is the only allowed value for `personGeneration` (text-to-video included) [114].
- **Children: the Gemini API page does not say.** Searching it for child, children, minor, under 18 and kids found nothing. What it does say: "Generated videos are passed through safety filters and memorization checking processes"; the prompt guide says safety filters apply to generated videos and uploaded photos; blocked videos are not charged; Veo 3.1 can block a video for audio-related safety reasons [114]. There are no documented error messages and no mention of `raiMediaFilteredReasons` or similar fields.
- **Google's Vertex AI page for Veo does say** (different product surface, "Last updated 2026-10-15 UTC") [116]: safety support codes `58061214` and `17301594` are the **Child** category, "Rejects requests to generate content depicting children if `personGeneration` isn't set to `allow_all`" or the project is not on an allowlist. An input-image rejection reads "Veo could not generate videos because the input image violates ... usage guidelines". When fewer videos than asked come back, "some generated output is being blocked". The page says nothing about blurring or silently altering a video.
- **Reading across (M, UNVERIFIED):** because image-to-video allows only `allow_adult`, a family photo that shows a child is most likely refused, not altered, and the refusal is probably a blocked or empty response with a support code. No page I read confirms this for the Gemini API. A one-off paid test would settle it: send one image of a child (see Q6, NARA 546220 has children in the water) to Veo 3.1 Lite (about $0.25 for 5 seconds per the pricing page in [51]) and record the exact response. Do not use a family photo for that test.
- Practical rule for the playbook: any photo with a child in it is probably unusable for Veo image-to-video. Her childhood photos are the likeliest to hit this. Plan parallax or local models for them.
- The video overview page [115] (last updated 2026-06-30) now lists a second video model, "Gemini Omni Flash"; I did not read its person rules.

### Q5. ExifTool: write and read `XMP-iptcExt:DigitalSourceType`; what survives in MP4 and MOV

**Run, not quoted.** ExifTool 13.59 (the current release, dated May 27, 2026 on its home page [117]) from the official source tarball [119], run with Perl 5.38.2 on the Ubuntu VM on 2026-10-18. I could not run the Windows `exiftool.exe` (same program, packaged for Windows; the install steps are on [118]); Windows run UNVERIFIED. The tarball and zip are on SourceForge; the direct `exiftool.org/Image-ExifTool-13.59.tar.gz` path returned 404.

**Windows install (from [118], not run):** unzip `exiftool-13.59_64.zip`; rename `exiftool(-k).exe` to `exiftool.exe`; keep the `exiftool_files` folder beside it; put both in a folder on PATH.

**TIFF, the tested commands** (on Windows use double quotes in `cmd` and PowerShell, never single quotes (M)):

```
exiftool -overwrite_original "-XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/algorithmicallyEnhanced" scan_0001.tif
exiftool -G1 -a -s -XMP-iptcExt:DigitalSourceType scan_0001.tif
```

Observed output, 16-bit 800x600 TIFF:

```
    1 image files updated
[XMP-iptcExt]   DigitalSourceType               : http://cv.iptc.org/newscodes/digitalsourcetype/algorithmicallyEnhanced
```

- **Write the full URI.** ExifTool 13.59 treats `DigitalSourceType` as free text with no value list (its source defines the tag with no value mapping). Writing `"-XMP-iptcExt:DigitalSourceType=Edited using Generative AI"` stored that literal sentence in the file; it did **not** convert it to the IPTC term. Readers that expect the vocabulary URI (see [89]) will not recognise the sentence. Use `http://cv.iptc.org/newscodes/digitalsourcetype/<term>` with the terms listed in summary item 12.
- Without `-overwrite_original` ExifTool keeps a `scan_0001.tif_original` backup (M: standard behaviour, not tested here).
- ExifTool edits metadata and rewrites the file in place. I did not hash the pixels before and after, so "pixel data unchanged" is UNVERIFIED (M: ExifTool is built to touch metadata only).

**MP4 and MOV, run on 2-second test clips made with ffmpeg 6.1.1:**

| Step | Result |
|---|---|
| `exiftool -overwrite_original "-XMP-iptcExt:DigitalSourceType=http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia" clip.mp4` then read it back | Works. In MP4 the XMP packet sits in a top-level `uuid` atom; in MOV it sits in an `XMP_` atom under the movie's user data. Both read back correctly. |
| `ffmpeg -i clip.mp4 -c copy remux_copy.mp4` (stream copy, default metadata) | **Tag lost.** |
| `ffmpeg -i clip.mp4 -map_metadata 0 -c copy remux_mm0.mp4` | **Tag lost.** |
| `ffmpeg -i clip.mp4 -c:v libx264 -c:a aac reenc.mp4` | **Tag lost.** |
| Sidecar: `exiftool -o untagged.xmp "-XMP-iptcExt:DigitalSourceType=<URI>" untagged.mp4` | Writes `untagged.xmp` (1,204 bytes). It also copies in file-derived tags (width, height, frame rate, audio rate). The video itself stays untagged. |
| Cleaner sidecar: make a blank XMP packet, then `exiftool -overwrite_original "-XMP-iptcExt:DigitalSourceType=<URI>" blank.xmp` | Works; 487-byte file holding only the tag. |
| Read the MP4 while a same-named `.xmp` sits beside it | ExifTool does **not** pick the sidecar up automatically for MP4. Read the `.xmp` file by name. |
| ImageMagick 6.9.12 `convert in.tif -resize 50% out.tif` | TIFF XMP **kept**. `-strip` **removed** it. |

**Rules that follow:** (1) For video, write the tag as the very last step, after the final ffmpeg or editor export, and write it into the delivered file. (2) Keep a sidecar `.xmp` or the manifest as the source of truth; the embedded tag is a courtesy copy. (3) For stills, tag the final TIFF/JPEG after all ImageMagick work, and re-read it. (4) Whether DaVinci Resolve, Premiere, YouTube or a phone player keep or show the tag is UNVERIFIED; the maker's own editor was not available to test.

### Q6. Public-domain stand-in photos for the bake-off

The five-photo bake-off needs a faded colour print, a small black-and-white print, a soft group snapshot, a torn print and a 1990s low-resolution digital file. Without search I browsed Wikimedia Commons damage categories, read each file page's licence block, and **viewed** a 960-pixel preview of four files (downloaded into their own folder). The licence on each Commons file page is what I report; Commons rights tags can be wrong, so re-check before any publication.

| Candidate | What I saw in the preview | Licence as read on the page | Notes |
|---|---|---|---|
| **NARA 546220**, EPA DOCUMERICA, photographer Marc St. Gil, June 1972, 3,000x2,025 [132] | Strong red-magenta cast, washed shadows, children wading by a tank. Category "Faded color photographs". | Commons template "Public domain", reason "work of an Environmental Protection Agency employee, taken or made as part of that person's official duties"; "all EPA images are in the public domain" | **Faded colour print stand-in.** Original medium (slide or print) is not stated on the page. Has small children in frame, which makes it the right test image for Q4. |
| **US Navy 80-G-27208**, Nov 1942, 2,179x2,296 [131] | Orange-brown toned print with a vertical crease or tear line down the middle and light scratches. Category "Ripped photographs". The page does not describe the damage. | "work of a sailor or employee of the U.S. Navy ... official duties"; public domain in the US; also tagged Public Domain Mark 1.0 | **Creased or torn print stand-in.** Adult in shorts doing a gym-wheel stunt. |
| **State Archives of North Carolina, "Clara MEEKINS, 1 year old, 1952"**, Commons file 986x1,000 [134] | Black-and-white snapshot of a toddler on a porch: crazed cracks across the emulsion, white spots, torn corner at top left, a car at left. Category "Damaged photographs". | Label "No known copyright restrictions" with a link to Flickr's usage page [136] | **Small, badly damaged b&w stand-in.** Physical print size is not stated, so "small" is UNVERIFIED. Flickr's page says the institution "can neither grant permission ... nor provide a guarantee that the photograph is in the public domain" and tells users to do their own analysis [136]. The title names the child, who may still be alive: use privately, do not publish outputs. |
| **"1971-12-John Call Cook"**, 3,007x3,971 [133] | Faded colour snapshot: blue-purple cast, red speckle dust all over, a smiling man at Christmas. Category "Faded color photographs". | **CC BY-SA 3.0**, "own work" of the uploader. Not public domain. | Best match for a 1970s home colour print. Private bake-off use is fine; any published output needs attribution and the same licence. Named real person. |

- **Not recommended:** "Damaged group photo of a school football team" [135] is CC BY 2.0 with a banner that its copyright information may be wrong.
- **Not covered:** a soft group snapshot with small faces, and a 1990s low-resolution digital file. Commons' damage categories are tiny (Faded color photographs: 7 files; Ripped photographs: 4 files [129][130]; Damaged photographs: 414 files, 200 shown [128]), so I looked at only a few of them.
- **Library of Congress** "Free to Use and Reuse" [137] lists sets (for example Families, 1800s to 1940s; John Margolies Roadside America, colour, 1969 to 2008; Work in America, 1977 to 1998). The page gives no rights definition, and I did not read any item page, so the licence terms for LoC items are UNVERIFIED. No set is labelled snapshots.
- **NARA's own catalog** page for 546220 returned an empty shell, so I could not read NARA's copyright wording; the Commons template is my only source for it.
- These are public images, so the Charter's rule against uploading personal material to third parties does not bind them. Even so, two show named real people, so keep the outputs private and treat all four as test material only (M).

### Q7. Creator evidence on archival inputs (Kontext, Qwen-Image-Edit, SeedVR2)

**Not met: 0 of 3 creator posts found.** This needed web search, which was exhausted; Reddit, X, YouTube and most blogs are also not fetchable here. What I could read:
- The FLUX.1 Kontext docs overview shows no old-photo, low-resolution or damaged-photo example and links no creator tutorials [143].
- The Qwen-Image-Edit-2511 model card has no restoration examples and no creator tutorials; it links a 35-thread discussion board and about 200 third-party Spaces [142].
- The SeedVR2 ComfyUI README links two YouTube deep-dives, "SeedVR2 v2.5 Deep Dive Tutorial" (`youtu.be/MBtWYXq_r60`) and "SeedVR2 Deep Dive Tutorial" (`youtu.be/I0sl45GMqNg`), plus the AInVFX channel. The README describes them as general upscaling workflows, not family photos, and I did not watch them [141]. They are leads, not evidence.

**Next step:** when search is available, look for creator posts from 2025 to 2026 that show a real scanned or low-resolution family photo, a before and after, and the settings. The open gap in the Summary (item 15) stands.

### Q8. Family reactions to animating the dead (for playbook Decision 4)

**Partly met.** I could not reach an independent first-hand account. The Verge (the main 2021 news piece) and Reddit are blocked here, the Sage paper returned 403, TechNewsWorld returned 403, and Wikipedia has no page for the feature. What I did read:

- **Vendor-curated first-hand quotes** [138]. MyHeritage's own blog (2021-03-04) embeds users' tweets from 2021-02-27 to 2021-03-04. The people are real and named, the words are theirs, but the company chose them and the post says so, so the mix is skewed to the positive. I saw the vendor's page, not the original tweets. Examples:
  - Jean McKenney, photo of her mother, who died in 1992: "It brought tears to my eyes. She was so beautiful."
  - Natasha (@ndelriego), great-grandfather's photo: "I just showed my grandmother and she broke down crying. This is amazing!" (a family elder's reaction).
  - Tracy Iglesias, father's photo on the anniversary of his death: "Seeing his face move after decades was mind-blowing as we didn't have video of him."
  - Diego R. Cáceres (in Spanish), whose father died when Diego was seven months old: all his life he dreamed of seeing his father alive for at least a moment.
  - "Vegan Diva", aunt who survived the Holocaust: "I sort of feel more like I'm meeting her thanks to this animation."
  - Mateja Kuhar: "I shed a few tears of joy last night. I saw my late grandpa once more, like in a dream."
  - Jason Glisson, grandfather's WWII photo: "seeing it move really shocked me."
  - Mixed or critical, same post: Ferris Jabr called it "an eerie yet captivating technology, raising many complex issues"; Robert Howard, after animating a bought antique portrait of a stranger, was "now... slightly afraid of it".
- **Secondhand press** [140]. SingularityHub (2021-04-08) repeats MyHeritage's line that users "were moved to tears" and says many posted animations on Twitter; it quotes no individual and links only a hashtag page.
- **No criticism on Wikipedia.** The MyHeritage article records the February 2021 launch and nearly 100 million animations but no reaction or ethics discussion [139]. It cites a 2025 paper, Kopelman and Frosh, "The 'algorithmic as if': Computational resurrection and the animation of the dead in Deep Nostalgia", *New Media & Society* 27(4): 2393 to 2413, DOI 10.1177/14614448231210268 [139]. That paper is the best lead for independent evidence; I could not read it.
- IEEE Spectrum's "digital afterlife" feature has no first-hand accounts and does not mention photo animation [144].

**What it means for Decision 4 (M).**
1. The reactions that exist are strong, emotional and mostly tearful, including from an elderly relative (Natasha's grandmother). That is exactly the risk in a surprise reveal: the mother may see her own late parent move, in company, with no warning.
2. The only first-hand worries I found are about the uncanny ("eerie", "slightly afraid"), not about dignity or consent; nobody quoted is a relative who objected. That is the curation bias, not proof there were no objections.
3. Keep the proposed default: no face or expression animation of people who have died. If the proxy relative wants it for a specific person, preview it with the proxy alone first, label it as animated, keep it short and silent, and never put it first in a group showing. The playbook's TODO(research) on this stays open until an independent account (or the Kopelman and Frosh paper) is read.

### Open items after round 1

1. **Maker:** run the Q2 PowerShell block and paste the output; run the Real-ESRGAN `.exe` once to see whether a Vulkan device is listed. This unlocks the tier table.
2. **Scribe (Haiku):** fix the `realesr-general-x4v3` command in R2 and `playbooks/ai-imagery.md` line 94; replace the CPU timing in Q9; add the IPTC "write the URI" rule and the "tag after the last ffmpeg step" rule to Recipe R6.
3. **Search pass needed** (budget or a follow-up message) for Q7 and for an independent Q8 account; also the Sage paper if reachable.
4. **One Veo test** with a public-domain child photo to see what Veo 3.1 Lite returns (about $0.25).
5. **Windows runs:** each tested command above should be run once on the maker's PC and dated; Windows behaviour is UNVERIFIED until then.
6. **ffmpeg 9.x re-test** of the morph and zoom recipes (tested on 6.1.1 only).

### New sources (round 1), numbering continues from 102

103. Local sandbox environment (this session, 2026-10-18) — Ubuntu 24.04.5, kernel 6.18.44, 4 vCPU Xeon 2.10 GHz, 15 GiB RAM, no GPU, no scanner, no `/mnt/c`, no WSL markers.
104. Local tests of the Real-ESRGAN ncnn Ubuntu build (2026-10-18) — `-h` text, missing-model behaviour, timings under Mesa llvmpipe software Vulkan, "invalid gpu device" without Vulkan.
105. Local tests of ExifTool 13.59, ffmpeg 6.1.1 and ImageMagick 6.9.12 metadata handling (2026-10-18) — TIFF, MP4, MOV, sidecars.
106. Local tests of rembg 2.0.85 (onnxruntime 1.31.0) and Depth Anything V2 Small via transformers 5.20.1, torch 2.14.1+cpu, Python 3.13.16 (2026-10-18).
107. Real-ESRGAN releases — https://github.com/xinntao/Real-ESRGAN/releases — v0.3.0 and v0.2.5.0 listed; dates show no year.
108. Real-ESRGAN v0.2.5.0 — https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.2.5.0 — portable zips dated 20220424; 8 assets, partly shown.
109. Real-ESRGAN v0.3.0 — https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.3.0 — general-x4v3 `.pth` assets; `-dn` for the Python script.
110. realesrgan-ncnn-vulkan-20220424-windows.zip — https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip — 45,474,481 bytes, SHA-256 abc02804e17982a3be33675e4d471e91ea374e65b70167abc09e31acb412802d; contents listed.
111. realesrgan-ncnn-vulkan-20220424-ubuntu.zip — https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip — 46,931,474 bytes; same models; executed in sandbox.
112. Real-ESRGAN README — https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/README.md — four portable models; general-x4v3 in Updates only.
113. Real-ESRGAN-ncnn-vulkan — https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases — v0.2.0 and v0.1.3.2; v0.2.0 Windows zip downloaded: no models.
114. Veo 3.1 in the Gemini API — https://ai.google.dev/gemini-api/docs/veo — "Last updated 2026-10-08 UTC" — `personGeneration` table, limitations, safety.
115. Video generation overview, Gemini API — https://ai.google.dev/gemini-api/docs/video — last updated 2026-06-30 UTC — lists Gemini Omni Flash and Veo 3.1; no person rules.
116. Veo responsible AI and usage guidelines (Vertex) — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines — last updated 2026-10-15 UTC — Child category support codes; input-image rejection text.
117. ExifTool home — https://exiftool.org/ — version 13.59, May 27, 2026; downloads linked to SourceForge.
118. ExifTool install — https://exiftool.org/install.html — Windows executable steps; no Perl needed.
119. Image-ExifTool-13.59.tar.gz — https://sourceforge.net/projects/exiftool/files/Image-ExifTool-13.59.tar.gz/download — SHA-256 668ea3acececb7235fbd0f4900e72d5f12c9b07e5c778fd36cb1e9b5828fd65a; run in sandbox.
120. ImageMagick download — https://imagemagick.org/download/ — 7.1.2-34; winget ids; portable; `vcomp140.dll` note; `magick` command; no release date shown.
121. FFmpeg download — https://ffmpeg.org/download.html — 9.0.2 (2026-09-18), 8.1.3 (2026-09-21); Windows builds by gyan.dev and BtbN.
122. Gyan.dev FFmpeg builds — https://www.gyan.dev/ffmpeg/builds/ — release 9.0.2, 2026-09-19; choco, scoop and winget commands.
123. rembg — https://github.com/danielgatis/rembg — Python `>=3.11,<3.14`; pip extras; models download to `~/.rembg/models`; no Windows notes.
124. Depth-Anything-V2 — https://github.com/DepthAnything/Depth-Anything-V2 — `run.py --encoder vits`; Small is Apache-2.0; no Windows notes.
125. Depth-Anything-V2-Small-hf — https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf — Apache-2.0; 24.8M parameters; pipeline snippet.
126. Install WSL, Microsoft Learn — https://learn.microsoft.com/en-us/windows/wsl/install — updated_at 2026-06-02; `wsl --install`; Windows 10 build 19041 or later.
127. Win32_VideoController, Microsoft Learn — https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-videocontroller — page date 2023-11-09; `AdapterRAM` is `uint32` bytes.
128. Commons, Category:Damaged photographs — https://commons.wikimedia.org/wiki/Category:Damaged_photographs — 414 files; subcategories for faded, ripped, scratched.
129. Commons, Category:Faded color photographs — https://commons.wikimedia.org/wiki/Category:Faded_color_photographs — 7 files.
130. Commons, Category:Ripped photographs — https://commons.wikimedia.org/wiki/Category:Ripped_photographs — 4 files.
131. Commons file 80-G-27208 — https://commons.wikimedia.org/wiki/File:80-G-27208_(31323126572).jpg — US Navy, Nov 1942; public domain (federal work).
132. Commons file NARA 546220 — https://commons.wikimedia.org/wiki/File:CHEMICAL_PLANTS_ON_SHORE_ARE_CONSIDERED_PRIME_SOURCE_OF_POLLUTION_-_NARA_-_546220.jpg — EPA DOCUMERICA, June 1972; public domain.
133. Commons file 1971-12-John Call Cook — https://commons.wikimedia.org/wiki/File:1971-12-John_Call_Cook.jpg — CC BY-SA 3.0; 3,007x3,971.
134. Commons file Clara MEEKINS 1952 — https://commons.wikimedia.org/wiki/File:Clara_MEEKINS,_1_year_old,_1952,_in_front_of_the_house_on_South_Street,_Raleigh,_NC,_where_she_was_born._People_visible_sitting_on_the_porch_of_the_house_are_all_family._Clara_remembers_they_would_(26480797321).jpg — State Archives of North Carolina via Flickr Commons; "No known copyright restrictions".
135. Commons file "Damaged group photo of a school football team" — https://commons.wikimedia.org/wiki/File:Damaged_group_photo_of_a_school_football_team_(16309215778).jpg — CC BY 2.0; disputed-copyright banner.
136. Flickr Commons usage — https://www.flickr.com/commons/usage/ — "no known copyright restrictions" meaning and disclaimer.
137. Library of Congress Free to Use and Reuse — https://www.loc.gov/free-to-use/ — set list; no rights definition on the page.
138. MyHeritage blog, "Deep Nostalgia is an Internet Sensation!" — https://blog.myheritage.com/2021/03/deep-nostalgia-is-an-internet-sensation/ — 2021-03-04 — vendor-curated user tweets.
139. MyHeritage (Wikipedia), re-read — https://en.wikipedia.org/wiki/MyHeritage — cites Kopelman and Frosh 2025, DOI 10.1177/14614448231210268; no reaction text.
140. SingularityHub on Deep Nostalgia — https://singularityhub.com/2021/04/08/deep-nostalgia-uses-ai-to-make-old-photos-of-your-relatives-wink-nod-dance-and-more/ — 2021-04-08 — secondhand "moved to tears".
141. ComfyUI-SeedVR2_VideoUpscaler README — https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler — links two YouTube deep-dives; no photo-restoration examples.
142. Qwen-Image-Edit-2511 model card — https://huggingface.co/Qwen/Qwen-Image-Edit-2511 — no restoration examples; discussions and Spaces only.
143. FLUX.1 Kontext overview (BFL docs) — https://docs.bfl.ai/kontext/kontext_overview — no old-photo examples; vendor links only.
144. IEEE Spectrum, "The Creepy New Digital Afterlife Industry" — https://spectrum.ieee.org/digital-afterlife — chatbots and companies; no photo animation, no family testimony.
