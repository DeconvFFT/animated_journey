---
name: ai-photo-to-animation-pipeline
description: Runs the Life Journey pipeline that turns real family photos into honestly labelled restored, stylised, morphed or animated shots, from scan through labelling to relative line-up review. Use when a task involves scanning, restoring, upscaling, cutting out, stylising, morphing or animating a real photo, when choosing an AI tool or route for one, or when deciding which label, consent or privacy step applies to it.
---

# AI Photo-to-Animation Pipeline

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
- Code or app work on the ArtCraft apps. Those are other tracks.
- Any cloud or third-party step the maker has not approved. Stop and ask.

## Procedure

1. **Intake.** Confirm the photo's ID (`LJ-<box>-<seq>-<side>`), its date confidence, and whether its chapter is sensitive (loss, illness, separation, money, conflict). Sensitive chapters go to the trusted proxy before any work. If the family has not decided on animating a person who has died, do not animate that person.
2. **Read the hardware tier.** Read the maker's GPU tier from `decisions/hardware.md` (repo-relative), which the orchestrator creates. Its fields: GPU, VRAM, RAM, free disk, Vulkan device listed (yes or no) and its name (a software device such as `llvmpipe`, `SwiftShader` or "Basic Render" counts as no GPU), and scanner. If the file or a GPU field is missing, assume no GPU, and ask the maker. If there is no GPU and no cloud approval, stop after L1, log the row, and hand the photo to the maker with the candidate routes.
3. **Read the privacy route.** Split by content. Work with no family photo may run in the cloud: tool installs and tests, the stand-in bake-off, style-LoRA training on the maker's own hand-made frames, scripts, renders of hand-built L5 scenes, and morph and parallax tests on stand-ins. Anything with her face or a relative's runs only on the maker's PC or a maker-approved rented GPU, and any upload of it needs the maker's explicit yes. The team's cloud session is a Linux VM with no GPU and no view of the maker's PC (checked 2026-10-18); the hardware tier comes only from the Q2 PowerShell block. Check the cloud verdict table under Ethics guardrails in this file before any service is used. Unknown terms mean no.
4. **Create the record first.** Add a `manifest.csv` row before processing. Store the scan in `01_masters` as read-only. Write its sha256 to `checksums.txt`.
5. **Scan.**
   - Flatbed: 600 ppi, colour, 16-bit TIFF. Turn off auto-enhance and restore-fading. Scan the back of any print with writing.
   - Phone: keep it parallel with a level app, use soft light, no flash, lock focus and exposure, and use PhotoScan's four-dot capture for glare.
   - Film: 1:1 macro on a copy stand, about f/8, lowest ISO, masked holder. Convert negatives with darktable's `negadoctor`, and keep the unexposed film border in the scan.
6. **Make the L1 copy.** Crop, straighten, and fix the colour cast one channel at a time with levels and curves. Remove dust with the healing brush. No AI. Save as `__L1`. Log it in `steps.csv` with `invents = colour` if the colour changed, otherwise `none`.
7. **Count pixels before any upscale, against the master.** Pixels needed across = timeline width × (1 + push-in) × crop factor (1.0 for a landscape print that fills the frame width). Assume a UHD master (3,840 px across) until the theatrical-delivery track fixes it (TODO(theatrical-delivery): master resolution). On UHD, a 4x6 print at 600 ppi (3,600 px across) with an 8 percent push-in needs about 4,150 px, so it is short; it is enough for 2K or 1080p. For UHD hero prints, scan at 800 to 1,200 ppi, or log a 2x Real-ESRGAN pass as L2, or keep push-ins under about 5 percent (which helps only if the picture fills less than about 89 percent of the frame width). Upscale only where the count is short: wallet prints, 1990s digital files, video frames and hero prints.
8. **Restore only if needed (L2).** Use Real-ESRGAN for a plain upscale: `realesrgan-ncnn-vulkan -i in.png -o out.png -n realesrgan-x4plus -s 2`. Do not use `-n realesr-general-x4v3`, which the portable build cannot load and which writes an all-black image [104]. Check `-h` for flags. Use face restoration only if the bake-off passed for this photo type. For CodeFormer, use `w` 0.7 to 1.0, then blend 40 to 60 percent back over the plain upscale with a layer mask. Reject any result with new teeth, eyelids or a changed jaw. Skip faces under about 64 px wide. At L2, generative repair is allowed on non-face regions only. Any generative change to a face moves the image to L3 or is rejected. Colourise only if the story needs it, and caption the shot "colours estimated." A face stays L2 if the tool changes chroma only and leaves the original luminance; it is a generative change (L3 or reject) if luminance or texture on the face moves. Test it by diffing the L channel of the original and the result in CIELAB over the face box, with the threshold set in the bake-off (playbook Step 6 has the ruling).
9. **Stylise (L3), using recipe R4's routes.**
   - Route A, hand-made (default): for each age band, pick 3 to 5 real photos, list identity attributes (hair, glasses, beard, scars, posture, signature clothes, height), and build a character sheet in the chosen look.
   - Route B, AI edit on the real photo: use an edit model that starts from the photo (FLUX.1 Kontext dev, Qwen-Image-Edit-2511, FLUX.2 klein). In the prompt, use "while maintaining the same facial features, hairstyle, and expression." Change one thing per step. Keep one seed, one LoRA strength and one prompt template per chapter.
   - Route C, identity adapters: do not use for real people. Their output is a new picture of the person, so it becomes an L5 reconstruction.
   - Route D, style LoRA: train only on the maker's own hand-made frames, never on a face, unless the consent conditions in playbook Step 9 are met.
10. **Connect two real photos (L4a, or L4c if generated).** Use a classic landmark morph or an ImageMagick or ffmpeg dissolve between two real photos. Chain through real intermediate photos where they exist. Use a generated in-between (Wan FLF2V, Veo `lastFrame`) only as L4c, only inside a labelled reconstruction, and only after inspecting the middle frames.
11. **Add motion to a still (L4a, or L4b if generated).**
    - Parallax: `rembg` cutout (never the cloud back-ends), Depth Anything V2 Small depth, depth blurred or flattened across faces, rendered with DepthFlow, Blender or paper-theatre layers. Keep the orbit at 2 to 3 degrees and the push-in at 3 to 8 percent.
    - Image-to-video: first frame is the restored still, motion words only, no speech, 3 to 4 takes, environment motion preferred. Clip length: local models 3 to 5 seconds; Veo 4 seconds at 720p (the shortest), or 8 seconds and a higher per-second price for 1080p or 4K, because those need 8 seconds [114]. Gate each take with a face-similarity script. This gate is unverified (TODO(research)).
    - Hard local-only condition: the photo contains a child. No cloud image-to-video for it. Veo accepts only `allow_adult` for image-to-video [82], and Google's Vertex page rejects child content when `personGeneration` is not `allow_all` [116]. Use parallax or a local model. See playbook Step 8.
12. **Reconstruct (L5), only from recorded testimony.** Write a brief that separates what is known from what is invented. Use the house look only. Caption it "Reconstructed from [name]'s memory, [interview date]", taking the date from the source's row in `manifest.csv` (the `interview_date` column). Get the narrator's and family's agreement for sensitive scenes.
13. **Label.** Set the level (L0 to L5). Write the IPTC DigitalSourceType URI to XMP, using the playbook's Step 10 mapping. An AI edit on a real photo is `compositeWithTrainedAlgorithmicMedia`. A hand-drawn scene from scratch, including a hand-built L5, is `digitalCreation`. Hand work layered over a real photo is `composite`. An AI-built L5 is `trainedAlgorithmicMedia`. Mixed work is `compositeSynthetic`. `humanEdits` is only for non-generative edits to captured media. Write the URI, not the label text. ExifTool was run on Linux only, so test it on a copy first. For video, write the tag after the final export, because ffmpeg strips it [105]. Put the label in the filename suffix, in `steps.csv`, and in the credits cue sheet.
14. **Log every change.** One `steps.csv` row per derivative, with tool, version, settings, seed, `invents` (none, texture, colour, frames or faces), label, reviewer and approval.
15. **Review.** Flick the original and the result at 100 percent. During the week-1 bake-off, judge only stand-in photos (not her archive), with the maker and confirmed insiders. Her real photos are judged in the vertical slice, after the "who is in on it" decision, by asking one relative who knew her: "Does this look like her at that age?" Relatives consulted for likeness must be on the insiders list in `GATHER.md` (not yet written; TODO). Include the answer in the manifest. The pass mark is set in the vertical slice (TODO(research)). Mark the row approved only after review.
16. **Back up.** Keep three copies on two kinds of media, with one off-site (3-2-1). Re-check the checksums after each backup.

## Checklists

**Per photo (before it leaves `02_work`)**
- [ ] ID follows the pattern, and the manifest row is complete (id, medium, ppi, scan_date, date_est, date_confidence, consent_note).
- [ ] Master is read-only and its sha256 is recorded.
- [ ] Sensitive-chapter check done, and the proxy informed.
- [ ] Every step is in `steps.csv` with an `invents` value.
- [ ] Label in the filename, XMP, `steps.csv` and cue sheet all agree.
- [ ] Caption on screen where required: "colours estimated" for colourised shots, "Reconstructed from..." for L5.

**Per clip**
- [ ] First frame matches the restored still.
- [ ] No speech, no lip movement, no added sound.
- [ ] Middle frames inspected: every face in them matches one of the two end photos.
- [ ] Face-similarity gate run, or recorded as not run.
- [ ] No face or expression motion for a person who has died, unless the family has said yes.
- [ ] On-screen label: "moved", and "frames invented" where generated.

**Before any release**
- [ ] Every derivative is approved in `steps.csv`.
- [ ] Credits list each AI tool and its label.
- [ ] Originals are still in `01_masters`, and the checksums match.
- [ ] No file depends on a cloud service the maker has not approved.
- [ ] Licences checked for the showing type: free public screening, or ticketed (the premiere is public; charter Principle 7).

## Quality bar

**Good work looks like this:**
- At 100% zoom, skin reads as skin. The background keeps the grain of the original. Nothing new appears in the face: no new teeth, eyelids or jaw.
- Original and result flick back and forth with the same framing.
- A relative who knew her recognises the person and the age, without being told which image is which.
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
- **No face or expression animation of people who have died** unless the family says yes. Environment motion and parallax are the default, and even those follow a family conversation.
- **Local by default.** Family photos stay on the maker's machine. Cloud use needs the maker's explicit yes, and then only for cleared photos, on paid tiers whose terms say no training. Download results at once.
- **Children and third parties** in the photos have not agreed to vendor processing. Process them locally.
- **Covert work.** Nothing may sync to a cloud photo library or shared device that the mother can see (charter).
- **Licences.** Non-commercial weights need a licence read for public exhibition before use; a ticketed showing excludes them.
- **Unread licences.** FLUX.2 dev, FLUX.2 klein 9B and InstantID have no licence read in the research note (TODO(research)). Do not use them for a shown frame until read.
- **Label everything.** Use L0 to L5, the IPTC URI in XMP, and the credits cue sheet.

**Cloud verdicts (from the research note's privacy table, Q7):**

| Service | Verdict |
|---|---|
| Gemini consumer app, Keep Activity on | Never for family photos. It trains on activity, and some chats are reviewed by people and kept up to three years [84]. |
| Gemini API, unpaid tier | Never for family photos. Content is used to improve products, and the terms say not to submit personal information [85]. |
| Gemini API, paid tier | Only for cleared photos, with the maker's yes. Prompts and files are not used to improve products [85]. |
| Luma | Never. Its privacy policy lists training as a purpose [86]. |
| Adobe Firefly | Its claim is "never trained on customer content" [87]. The consumer terms were not read, so treat as no until read (TODO(research)). |
| Replicate | API only, and save results locally. API predictions are removed after an hour [88]. |
| OpenAI, Runway, Kling, Midjourney, MyHeritage, Remini and Bending Spoons, fal.ai retention, Hugging Face Spaces, Topaz cloud | Unverified. Do not upload. |
| Unofficial "free restore" sites, rembg cloud back-ends | Never [15][55]. |
| Topaz desktop apps | Local rendering, offline use. Its privacy policy does not say whether images train models [31][32]. |

## References

- Playbook: `playbooks/ai-imagery.md`
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
