---
name: ai-photo-to-animation-pipeline
description: Runs the Life Journey pipeline that turns real family photos into honestly labelled restored, stylised, morphed or animated shots, from scan through labelling to the maker's line-up review. Use when a task involves scanning, restoring, upscaling, cutting out, stylising, morphing or animating a real photo, when choosing an AI tool or route for one, or when deciding which label, consent or privacy step applies to it.
---

# AI Photo-to-Animation Pipeline

Reconciled with [DECISIONS.md](../../DECISIONS.md) (2026-10-18, and again on 2026-10-19 after the her-world merge), the single source of truth. Where this skill disagrees with a register row, the register wins. D-nn rows are decided by the maker; W-nn rows are working defaults. No generative route ever touches a deity (D-28, W-61), and the game-world rule is retired (D-29).

## Purpose

Turn the maker's mother's real photos into finished shots that obey charter principle 4: AI may restore, restyle, animate and connect real photos. It may not invent events, fake people or put words in anyone's mouth. Every output carries a label that says what was done and what was invented.

Read these before you start a new photo type:
- Playbook (for the maker, with decisions and exercises): `playbooks/ai-imagery.md`
- Research note (the evidence and the numbered sources): `research/ai-imagery.md`

Items marked TODO(research) are open. Do not treat them as settled.

## When to use / when not to

**Use** for:
- Scanning, cleaning, restoring, upscaling, colourising, stylising, cutting out, morphing or animating a real photo for the Life Journey.
- Choosing a tool or route for one photo or clip.
- Writing `manifest.csv`, `steps.csv`, labels or the credits cue sheet for this work.
- Reviewing a derivative before it enters the project.

**Do not use** for:
- Story gathering, interviews, or deciding what a chapter says. Those belong to other tracks and skills.
- Anything that would make a real person speak, sing or appear in a new event: voice cloning, lip-sync, talking photos, or a generated scene of a real person. Stop and tell the maker.
- Photoreal generation of people, scenes or voices. Under the proposed house rule, reconstructions use the stylised house look only.
- Any restoration, edit, stylisation, motion or generation of a deity image. No AI route is run on a deity in any class (W-61); use the `hindu-visual-language` skill for the sources a deity image may come from.
- Code or app work on the ArtCraft apps. Those are other tracks.
- Any cloud or third-party step the maker has not approved. Stop and ask.

## Procedure

1. **Intake.** Confirm the photo's ID (`LJ-<box>-<seq>-<side>`), its date confidence, and whether its chapter is sensitive (loss, illness, separation, money, conflict). Sensitive chapters go through one-key-three-guards before any work: the maker is the proxy (D-03, D-04). Do not animate the face or expression of a person who has died; the family cannot be asked under only-me, so the premiere cut has environment motion and parallax only (W-40).
2. **Read the hardware tier.** Read the maker's GPU tier from `decisions/hardware.md` (repo-relative), which the orchestrator creates. Its fields: GPU, VRAM, RAM, free disk, Vulkan device listed (yes or no) and its name (a software device such as `llvmpipe`, `SwiftShader` or "Basic Render" counts as no GPU), and scanner. If the file or a GPU field is missing, assume no GPU, and ask the maker. If there is no GPU and no cloud approval, stop after L1, log the row, and hand the photo to the maker with the candidate routes.
3. **Read the privacy route.** Split by content. Work with no family photo may run in the cloud: tool installs and tests, the stand-in bake-off, style-LoRA training on the maker's own hand-made frames, scripts, renders of hand-built L5 scenes, and morph and parallax tests on stand-ins. Anything with her face or a relative's runs only on the maker's PC (D-15, W-23): no full-size family photo goes to a cloud session, a hosted renderer or a rented GPU. Every photo set carries `cloud: none` by default and only the maker raises it (W-24). `preview` proxies of about 768 px may go to the cloud container only after the account's model-improvement setting is off. A rented GPU is for non-family imagery only, on Secure Cloud with an encrypted volume and the maker's recorded OK, never Community Cloud. The team's cloud session is a Linux VM with no GPU and no view of the maker's PC (checked 2026-10-18); the hardware tier comes only from the Q2 PowerShell block. Check the cloud verdict table under Ethics guardrails in this file before any service is used. Unknown terms mean no.
4. **Create the record first.** Add a `manifest.csv` row before processing. Store the scan in `01_masters` as read-only. Write its sha256 to `checksums.txt`.
5. **Scan.**
   - Flatbed: 600 ppi, colour, 16-bit TIFF. Turn off auto-enhance and restore-fading. Scan the back of any print with writing.
   - Phone: keep it parallel with a level app, use soft light, no flash, lock focus and exposure, and use PhotoScan's four-dot capture for glare.
   - Film: 1:1 macro on a copy stand, about f/8, lowest ISO, masked holder. Convert negatives with darktable's `negadoctor`, and keep the unexposed film border in the scan.
6. **Make the L1 copy.** Crop, straighten, and fix the colour cast one channel at a time with levels and curves. Remove dust with the healing brush. No AI. Save as `__L1`. Log it in `steps.csv` with `invents = colour` if the colour changed, otherwise `none`.
7. **Count pixels before any upscale, against the master.** Pixels needed across = timeline width × (1 + push-in) × crop factor (1.0 for a landscape print that fills the frame width). The master is 1920x1080 and stills are prepared at 3840 px on the long edge; a 2K Flat DCP is derived from the master and 4K is not needed (W-15, settled). A 4x6 print at 600 ppi (3,600 px across) with an 8 percent push-in is enough for 1080p and 2K, and a plain resize covers the 3840 px target. UHD applies only to single hero shots if a 4K cinema is booked: there a 4x6 print needs about 4,150 px, so scan at 800 to 1,200 ppi, or log a 2x Real-ESRGAN pass as L2, or keep push-ins under about 5 percent (which helps only if the picture fills less than about 89 percent of the frame width). Upscale only where the count is short: wallet prints, 1990s digital files, video frames and any hero print booked at UHD.
8. **Restore only if needed (L2).** Use Real-ESRGAN for a plain upscale: `realesrgan-ncnn-vulkan -i in.png -o out.png -n realesrgan-x4plus -s 2`. Do not use `-n realesr-general-x4v3`, which the portable build cannot load and which writes an all-black image [104]. Check `-h` for flags. Use face restoration only if the bake-off passed for this photo type. For CodeFormer, use `w` 0.7 to 1.0, then blend 40 to 60 percent back over the plain upscale with a layer mask. Reject any result with new teeth, eyelids or a changed jaw. Skip faces under about 64 px wide. At L2, generative repair is allowed on non-face regions only. Any generative change to a face moves the image to L3 or is rejected. Colourise only if the story needs it, and caption the shot "colours estimated." A face stays L2 if the tool changes chroma only and leaves the original luminance; it is a generative change (L3 or reject) if luminance or texture on the face moves. Test it by diffing the L channel of the original and the result in CIELAB over the face box, with the threshold set in the bake-off (playbook Step 6 has the ruling).
9. **Stylise (L3), using recipe R4's routes.**
   - Route A, hand-made (default): for each age band, pick 3 to 5 real photos, list identity attributes (hair, glasses, beard, scars, posture, signature clothes, height), and build a character sheet in the chosen look. The look is the maker's own hand-made material, set at G1 (W-38): where that is seva craft it is the *making*, never the finished seva article and never a reconstruction painted onto Thakorji's clothes. The game-style block look of the earlier plan is retired with its tools (D-29).
   - Route B, AI edit on the real photo: use an edit model that starts from the photo (FLUX.1 Kontext dev, Qwen-Image-Edit-2511, FLUX.2 klein). In the prompt, use "while maintaining the same facial features, hairstyle, and expression." Change one thing per step. Keep one seed, one LoRA strength and one prompt template per chapter.
   - Route C, identity adapters: do not use for real people. Their output is a new picture of the person, so it becomes an L5 reconstruction.
   - Route D, style LoRA: train only on the maker's own hand-made frames, never on a face (D-16: no model is trained on her face).
   - Deities: Routes B, C and D are never used on a deity, and a plate is never repaired by diffusion (W-61). The default policy is P1, symbols and seva objects that are not a svarupa, so no deity figure is drawn, generated or photographed; if the maker rules a higher class at O-64, an image comes only from a hand-drawn vector symbol, a logged hand-traced public-domain plate, her own photograph (a svarupa picture only in the April version, and only if she knows) or a commissioned painting. Never draw or open the eyes of a svarupa, and treat any picture of one on her shelf as a possible seva object that is not photographed without her knowing (PR3, PR4).
10. **Connect two real photos (L4a, or L4c if generated).** Use a classic landmark morph or an ImageMagick or ffmpeg dissolve between two real photos. Chain through real intermediate photos where they exist. Use a generated in-between (Wan FLF2V, Veo `lastFrame`) only as L4c, only inside a labelled reconstruction, and only after inspecting the middle frames.
11. **Add motion to a still (L4a, or L4b if generated).**
    - Parallax: `rembg` cutout (never the cloud back-ends), Depth Anything V2 Small depth, depth blurred or flattened across faces, rendered with DepthFlow, Blender or paper-theatre layers. Keep the orbit at 2 to 3 degrees and the push-in at 3 to 8 percent.
    - Image-to-video: first frame is the restored still, motion words only, no speech, 3 to 4 takes, environment motion preferred. Hosted image-to-video (Veo and the like) is for stand-ins and non-family imagery only; a family photo uses a local model (D-15, W-24). Clip length: local models 3 to 5 seconds; Veo 4 seconds at 720p (the shortest), or 8 seconds and a higher per-second price for 1080p or 4K, because those need 8 seconds [114]. Gate each take with a face-similarity script. This gate is unverified (TODO(research)).
    - Hard local-only condition: the photo contains a child. No cloud image-to-video for it. Veo accepts only `allow_adult` for image-to-video [82], and Google's Vertex page rejects child content when `personGeneration` is not `allow_all` [116]. Use parallax or a local model. See playbook Step 8.
12. **Reconstruct (L5), only from testimony.** Before the premiere that means the maker's own knowledge or an album-and-hands session (W-49), not a recorded interview (D-03); recorded relative testimony arrives with the April version (D-06). Write a brief that separates what is known from what is invented. Use the house look only. Caption it "Reconstructed from [name]'s memory, [interview date]", taking the date from the source's row in `manifest.csv` (the `interview_date` column, which holds the session date). Sensitive scenes go through one-key-three-guards (D-04); nobody is asked before the premiere.
13. **Label.** Set the level (L0 to L5). Write the IPTC DigitalSourceType URI to XMP, using the playbook's Step 10 mapping. An AI edit on a real photo is `compositeWithTrainedAlgorithmicMedia`. A hand-drawn scene from scratch, including a hand-built L5, is `digitalCreation`. Hand work layered over a real photo is `composite`. An AI-built L5 is `trainedAlgorithmicMedia`. Mixed work is `compositeSynthetic`. `humanEdits` is only for non-generative edits to captured media. Write the URI, not the label text. ExifTool was run on Linux only, so test it on a copy first. For video, write the tag after the final export, because ffmpeg strips it [105]. Put the label in the filename suffix, in `steps.csv`, and in the credits cue sheet. A `deity_image` row is L0 or L1 (her own photograph of seva objects that are not a svarupa; a svarupa picture only in the April version, when she knows), L2 only for non-generative scaling, or L3 for a traced plate; never L4 or L5.
14. **Log every change.** One `steps.csv` row per derivative, with tool, version, settings, seed, `invents` (none, texture, colour, frames or faces), label, reviewer and approval, plus `deity_form` and `deity_source` (both `none` unless the row is a deity image).
15. **Review.** Flick the original and the result at 100 percent. During the week-1 bake-off, judge only stand-in photos (not her archive); the maker is the only judge (D-03). Her real photos are judged in the vertical slice, after P-LOCK (Sat 14 Nov), by the maker alone from their own knowledge ("Does this look like her at that age?"); there is no insiders list and no relative is asked (W-40, O-11). The maker signs likeness at five of five correct in a shuffled line-up, passed twice, 48 hours apart (W-40). Include the answer in the manifest. Mark the row approved only after review.
16. **Back up.** Keep three copies on two kinds of media (3-2-1), with the second copy on a second encrypted SSD kept elsewhere; there is no cloud copy of family media (W-25). Re-check the checksums after each backup.

## Checklists

**Per photo (before it leaves `02_work`)**
- [ ] ID follows the pattern, and the manifest row is complete (id, medium, ppi, scan_date, date_est, date_confidence, consent_note).
- [ ] Master is read-only and its sha256 is recorded.
- [ ] Sensitive-chapter check done through one-key-three-guards (the maker is the proxy; D-04).
- [ ] Every step is in `steps.csv` with an `invents` value.
- [ ] A deity image has `deity_form` and `deity_source`, is L0 to L3 only, and no generative route touched it.
- [ ] Label in the filename, XMP, `steps.csv` and cue sheet all agree.
- [ ] Caption on screen where required: "colours estimated" for colourised shots, "Reconstructed from..." for L5.

**Per clip**
- [ ] First frame matches the restored still.
- [ ] No speech, no lip movement, no added sound.
- [ ] Middle frames inspected: every face in them matches one of the two end photos.
- [ ] Face-similarity gate run, or recorded as not run.
- [ ] No face or expression motion for a person who has died (none at all in the premiere cut, W-40).
- [ ] On-screen label: "moved", and "frames invented" where generated.

**Before any release**
- [ ] Every derivative is approved in `steps.csv`.
- [ ] Credits list each AI tool and its label.
- [ ] Originals are still in `01_masters`, and the checksums match.
- [ ] No file depends on a cloud service, and no full-size family photo has left the PC (D-15, W-24).
- [ ] Licences checked for the showing type: free public screening, or ticketed (the premiere is public; charter Principle 7).

## Quality bar

**Good work looks like this:**
- At 100% zoom, skin reads as skin. The background keeps the grain of the original. Nothing new appears in the face: no new teeth, eyelids or jaw.
- Original and result flick back and forth with the same framing.
- The maker recognises the person and the age, without being told which image is which.
- The label matches what was done, and every invention is recorded in `steps.csv`.
- Motion is small and honest. The camera moves, the gaps show, and the subject stays still unless the original shows motion.

**Mediocre work (fix it or reject it):**
- The "improved" face is cleaner than any real photo of the person, with a different nose, jaw or eye spacing. (Identity drift; see GFPGAN's note [17].)
- Hair or background smears at the face seam. This is a known whole-image CodeFormer problem [15].
- Colour is saturated or orange, or the skin looks plastic. These are known DeOldify failure modes [29] and a known SeedVR2 output problem [24].
- A label is missing, or says "unaltered" for something that was restored.
- A morph shows ghosting that reads as a second face.
- Motion invents an expression or speech.

## Ethics guardrails

- **Real memories stay real.** Restoration and restyle are allowed. Invented events, fake people and words in anyone's mouth are not (charter principle 4).
- **No photoreal generation** of people or scenes. Reconstructions use the house look and carry a visible caption.
- **No voice cloning, lip-sync or talking photos** of anyone.
- **No face or expression animation of people who have died** in the premiere cut: under only-me the family cannot be asked (D-03, W-40). Environment motion and parallax only.
- **Local by default.** Family photos stay on the maker's machine (`cloud: none` by default; only the maker raises it). No full-size family photo goes to a cloud session, a hosted renderer or a rented GPU, and Community Cloud never (D-15, W-23, W-24). Download results at once.
- **Children and third parties** in the photos have not agreed to vendor processing. Process them locally.
- **Covert work.** Nothing may sync to a cloud photo library or shared device that the mother can see (charter).
- **Licences.** Non-commercial weights need a licence read for public exhibition before use; a ticketed showing excludes them.
- **Unread licences.** FLUX.2 dev, FLUX.2 klein 9B and InstantID have no licence read in the research note (TODO(research)). Do not use them for a shown frame until read.
- **Deities (D-28, W-61).** The default policy is P1: no deity is drawn, generated or photographed, and no AI route touches one in any class. Nothing of the Thakorji, Lalan, chitraji or any picture of hers is photographed without her knowing (PR4). Any phone surface or on-screen tag that must be read follows the phone-safe frame (W-63).
- **Label everything.** Use L0 to L5, the IPTC URI in XMP, and the credits cue sheet.

**Cloud verdicts (from the research note's privacy table, Q7):**

| Service | Verdict |
|---|---|
| Gemini consumer app, Keep Activity on | Never for family photos. It trains on activity, and some chats are reviewed by people and kept up to three years [84]. |
| Gemini API, unpaid tier | Never for family photos. Content is used to improve products, and the terms say not to submit personal information [85]. |
| Gemini API, paid tier | Not for family photos at any size (D-15); stand-ins and non-family imagery only. Prompts and files are not used to improve products [85]. |
| Luma | Never. Its privacy policy lists training as a purpose [86]. |
| Adobe Firefly | Its claim is "never trained on customer content" [87]. The consumer terms were not read, so treat as no until read (TODO(research)). |
| Replicate | API only, and save results locally. API predictions are removed after an hour [88]. |
| OpenAI, Runway, Kling, Midjourney, MyHeritage, Remini and Bending Spoons, fal.ai retention, Hugging Face Spaces, Topaz cloud | Unverified. Do not upload. |
| Unofficial "free restore" sites, rembg cloud back-ends | Never [15][55]. |
| Topaz desktop apps | Local rendering, offline use. Its privacy policy does not say whether images train models [31][32]. |

## References

- Decision register (source of truth): `DECISIONS.md`
- Playbook: `playbooks/ai-imagery.md`
- Hindu visual language (deity sources and respect rules): `playbooks/hindu-visual.md`
- Research note: `research/ai-imagery.md`. Relevant sections: Q1 (scanning), Q2 (restoration), Q3 and Q4 (stylising and likeness), Q5 (morphs), Q6 (image-to-video), Q7 (privacy), Q8 (labelling), Q9 (hardware tiers), Pitfalls and Ethics.
- Key sources (numbers match the research note's Sources list):
  - [1] Library of Congress, Scanning Your Personal Collections: https://www.digitalpreservation.gov/personalarchiving/documents/scanning_collections.pdf
  - [2] U.S. National Archives, Digitizing Family Papers: https://www.archives.gov/preservation/family-archives/digitizing.html
  - [5] John Hultgren, Scanning Film: https://hultgren.org/articles/scan/index.php
  - [13] darktable negadoctor module: https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/negadoctor/
  - [15] CodeFormer: https://github.com/sczhou/CodeFormer
  - [17] GFPGAN: https://github.com/TencentARC/GFPGAN
  - [18] Real-ESRGAN: https://github.com/xinntao/Real-ESRGAN
  - [21] SUPIR: https://github.com/Fanghua-Yu/SUPIR
  - [23] SeedVR: https://github.com/ByteDance-Seed/SeedVR
  - [24] ComfyUI-SeedVR2_VideoUpscaler: https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler
  - [28] DDColor: https://github.com/piddnad/DDColor
  - [29] DeOldify: https://github.com/jantic/DeOldify
  - [33] FLUX.1 Kontext dev: https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
  - [34] FLUX.1 Kontext dev, ComfyUI tutorial: https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev
  - [46] ai-toolkit: https://github.com/ostris/ai-toolkit
  - [47] fluxgym: https://github.com/cocktailpeanut/fluxgym
  - [55] rembg: https://github.com/danielgatis/rembg
  - [58] Depth Anything V2: https://github.com/DepthAnything/Depth-Anything-V2
  - [60] DepthFlow: https://github.com/BrokenSource/DepthFlow
  - [65] LearnOpenCV FaceMorph: https://github.com/spmallick/learnopencv/tree/master/FaceMorph
  - [67] Wan2.1-FLF2V-14B-720P: https://huggingface.co/Wan-AI/Wan2.1-FLF2V-14B-720P
  - [70] Wan2.2 ComfyUI tutorial: https://docs.comfy.org/tutorials/video/wan/wan2_2
  - [72] FramePack: https://github.com/lllyasviel/FramePack
  - [77] WanGP: https://github.com/deepbeepmeep/Wan2GP
  - [82] Veo 3.1 in the Gemini API: https://ai.google.dev/gemini-api/docs/veo
  - [114] Veo 3.1 in the Gemini API (same page as [82]): https://ai.google.dev/gemini-api/docs/veo
  - [84] Gemini Apps Privacy Hub: https://support.google.com/gemini/answer/13594961
  - [85] Gemini API Additional Terms of Service: https://ai.google.dev/gemini-api/terms
  - [86] Luma Labs Privacy Policy: https://lumalabs.ai/legal/privacy-policy
  - [87] Adobe Firefly generative AI approach: https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html
  - [88] Replicate data retention: https://replicate.com/docs/topics/predictions/data-retention
  - [89] IPTC Digital Source Type vocabulary: https://cv.iptc.org/newscodes/digitalsourcetype/
  - [90] IPTC Photo Metadata User Guide: https://www.iptc.org/std/photometadata/documentation/userguide/
  - [94] Partnership on AI, Responsible Practices for Synthetic Media: https://syntheticmedia.partnershiponai.org/
  - [96] APA GenAI Best Practices Tool Kit: https://www.archivalproducersalliance.com/tool-kit-for-documentaries
  - [98] Roadrunner (Wikipedia): https://en.wikipedia.org/wiki/Roadrunner:_A_Film_About_Anthony_Bourdain
  - [99] What Jennifer Did (Wikipedia): https://en.wikipedia.org/wiki/What_Jennifer_Did
  - [100] They Shall Not Grow Old (Wikipedia): https://en.wikipedia.org/wiki/They_Shall_Not_Grow_Old
  - [104] and [105] Local test runs (Real-ESRGAN flags and missing-model behaviour; ExifTool and MP4 tag handling): see the research note's follow-up round, not web pages
  - [116] Veo responsible AI and usage guidelines (Vertex): https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines (page text sits past a 100,000-character navigation block; a first fetch looks empty)
  - [102] Local sandbox test of ImageMagick and ffmpeg commands (commands run; result quality not judged on real faces). Not a web page; see the research note.

## Changelog

- 2026-10-18: Reconciled with DECISIONS.md (2026-10-18): the maker judges likeness alone (no insiders, no GATHER.md; D-03, W-40); cloud policy restated as decided (`cloud: none`, no family photo to any hosted service or rented GPU; D-15, W-23, W-24); master settled at 1080p with stills at 3840 px (W-15); backup is a second encrypted SSD with no cloud copy (W-25); no face or expression motion for the dead in the premiere cut (W-40); no model trained on her face (D-16); L5 testimony under only-me (W-49, D-06).
- 2026-10-19: Reconciled with DECISIONS.md after the her-world merge (2026-10-19): no generative route for a deity and the deity-image label rule (W-61); `deity_form` and `deity_source` in `steps.csv`; Route A follows W-38 and the game-style block look is retired (D-29); P-LOCK replaces the old process-lock spelling; on-screen tags follow the phone-safe frame (W-63).
