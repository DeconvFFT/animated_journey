# Review — track `ai-imagery`, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/ai-imagery.md` (Sonnet note, 102 sources), `playbooks/ai-imagery.md` (Haiku scribe, v1), `skills/ai-photo-to-animation-pipeline/SKILL.md`, read against `CHARTER.md` and my charter review `reviews/00-charter-review.md`.
**Verdict:** `revise`. This is the strongest research of the Learn phase so far: honest about its own limits, dated throughout, and built around Principle 4 rather than around tools. It fails the gate on two concrete points, both fixable in a day: the playbook's commands do not run on the maker's Windows machine that the charter now names, and the week-1 bake-off as written needs the mother's real photos before the charter's gathering gate opens and before the covert rules are in place.

Good enough to start on now (per my charter-review allowance for first drafts): Stage 1 scanning, Stage 3 cutout and parallax, Stage 5 classic morph, Q7 privacy table, Q8 label ladder apart from the IPTC mapping fix below.

---

## 1. Spot-checks against primary sources

Eleven claims fetched today (2026-10-18). Fetched pages treated as data.

| # | Claim in the note | Source | Result |
|---|---|---|---|
| 1 | Veo 3.1 Lite / Fast / Standard $0.05 / $0.10 / $0.40 per second at 720p; Nano Banana Pro $0.134 per 1K/2K image; `gemini-2.5-flash-image` deprecated, shutdown 2026-10-02 | [51] ai.google.dev pricing | **Confirmed.** Page adds 1080p and 4K rates ($0.08 Lite 1080p; $0.12 / $0.30 Fast; $0.60 Standard 4K) and says "migrate to Gemini 3.1 Flash Image". Shutdown date is already past. |
| 2 | Unpaid tier trains and forbids personal data; paid tier does not train; effective 2026-03-23, updated 2026-04-28 | [85] Gemini API terms | **Confirmed**, including the exact sentence "Do not submit sensitive, confidential, or personal information to the Unpaid Services." |
| 3 | Wan2.2 5B "should fit well on 8GB vram with the ComfyUI native offloading"; README says at least 24 GB | [70] docs.comfy.org; [69] Wan2.2 README | **Both confirmed.** The README's 24 GB figure is for its own `generate.py` with offload flags; the 8 GB figure is ComfyUI's. The note presents the conflict fairly. |
| 4 | CodeFormer `w` in [0,1], larger is more faithful; NTU S-Lab licence; unofficial-site warning; last news 2023-07-20 | [15] GitHub | **Confirmed** verbatim. |
| 5 | FramePack 6 GB minimum; RTX 30/40/50 only; 2.5 s per frame on a 4090, 1.5 with TeaCache; laptops 4 to 8x slower; prefers large motion; fake-site warning | [72] GitHub | **Mostly confirmed.** One overstatement: the README says GTX 10XX/20XX are "not tested", not unsupported. |
| 6 | IPTC Digital Source Type has `print`, `negativeFilm`, `positiveFilm`, `humanEdits`, `algorithmicallyEnhanced`, `compositeWithTrainedAlgorithmicMedia`, `trainedAlgorithmicMedia`, `composite`; `minorHumanEdits` retired 2024-09-17 | [89] cv.iptc.org | **Confirmed.** The vocabulary also has `digitalCreation` ("created by a human using non-generative tools") and `compositeSynthetic`, which the ladder should use (see nudge 3). |
| 7 | RunPod RTX 4090 $0.34 community / $0.89 secure per hour; updated 2026-10-08 | [83] runpod.io | **Confirmed.** The $0.34 figure is only in the page's structured data; the visible card shows $0.89. Worth a footnote. |
| 8 | rembg CLI `i`, `p`, `-om`, `-a`, `-m`; `rembg[cpu]`; MIT; `bria-rmbg` default needs a paid agreement for commercial use; cloud back-ends send images to servers | [55] GitHub | **Confirmed**, including "Images are sent to withoutBG's servers". |
| 9 | FILM repository archived 2025-10-14; built for "near-duplicate photos"; CUDA 11.2.1, Python 3.9 | [61] GitHub | **Confirmed.** |
| 10 | Real-ESRGAN ncnn portable: `-i -o -n -s -t`; Intel/AMD/Nvidia; BSD-3 | [18] GitHub | **Flags and platforms confirmed.** But the README's ncnn model list is `realesrgan-x4plus`, `realesrnet-x4plus`, `realesrgan-x4plus-anime`, `realesr-animevideov3`; `realesr-general-x4v3` appears only in the Updates section. The playbook's example command may fail on the portable build. |
| 11 | Epson V600 "Discontinued"; 6400 dpi; Dmax 3.4; OS list ends at Windows 8 / OS X 10.10 | [9] epson.com | **Confirmed.** |

Accuracy of what was checked is high. The researcher's method note (numbers checked against a small-model summary, not the raw page) is honest and, on this sample, did not introduce errors.

---

## 2. Scores (1 to 5)

Scores are for the set; where one artifact differs I say so.

| Criterion | Score | Why |
|---|---|---|
| Meaning | 4 | The whole track is organised around Principle 4 and the relatives' line-up test, which is exactly right. The paper-theatre parallax (E7) and attribute-based ageing character sheet (E8) are ideas with meaning, not just tricks. What is missing is the story side of restoration: *when not to restore*. Fade, grain, Polaroid borders, the handwriting on the back are era texture (Principle 3) and the note treats them only as defects. |
| Specificity | 5 | Commands, prices, VRAM tiers, label levels, CSV columns, flag names, dated statuses. A scribe wrote a playbook from it without re-reading sources, which is the test I set. |
| Accuracy | 4 | 11 of 11 spot-checks hold; everything fast-moving is dated; M / UNVERIFIED / ESTIMATE markers are used consistently. Deductions: FramePack GPU wording, the Real-ESRGAN ncnn model name, the IPTC mapping for hand-made work, and the summary's "40 to 75 hours" against the table's "40 to 80". |
| Feasibility | 3 | The charter (updated today) says the maker is on Windows with memory constraints. Every command in the playbook was tested on Linux only and two will fail outright on Windows (`convert`, `sha256sum`). Exercise 3 asks for CodeFormer (Python, PyTorch, CUDA) in week 1 on hardware nobody has inventoried. The no-GPU path is real and the tier table is the right shape, but the maker cannot do the first exercise within an hour of reading, which is my usability bar for playbooks. |
| Ethics | 4 | The house rule, the Reality Ladder, local-by-default, the children-and-third-parties point, the treatment of the dead, and the voice ban are all stronger than I asked for. Two gaps: the bake-off and line-up tests need the mother's photos and relatives before the gathering gate and the "who is in on it" decision; and the L2 rung lets a generative model repair a face while the result still "looks like a photograph", which the house rule says must not happen. |
| Craft / usability | 4 | Research note: long but navigable; stage tables and decision tables are where a scribe needs them. Playbook: clear voice, honest about judgment versus source, decisions marked "from the note" versus "scribe's reading". Skill: the description triggers on the right verbs and nouns and the 16-step procedure plus checklists is usable by an agent; it loses a point for absolute `/home/user/...` paths (the repo moves to GitHub and to a Windows PC), a hard-coded "2026" in the reconstruction caption, and no stop condition when there is no GPU and no cloud approval. |

---

## 3. Critical issues (block approval)

**C1. The playbook targets Linux while the maker is on Windows.** `CHARTER.md` (Known facts, Oct 18) states the maker's computer is Windows. `playbooks/ai-imagery.md` Step 3 uses `sha256sum`, Step 7 and Exercise 6 use `convert ... -morph`, and Step 8 uses a bash-quoted ffmpeg filter. On Windows, ImageMagick 7 is invoked as `magick` (plain `convert` collides with the system's disk utility), `sha256sum` does not exist (PowerShell `Get-FileHash -Algorithm SHA256` or `certutil -hashfile <file> SHA256`), and the quoting differs. The playbook's own Pitfalls admit "Windows set-up is not yet researched", but a playbook whose first exercise fails on the reader's machine is not usable. Fix: give Windows forms beside each command, and state once whether the recommended route is native Windows builds or WSL (research follow-up 1).

**C2. The week-1 bake-off breaks the charter's gathering gate and the covert rules.** Research note Open question 1, playbook Exercise 3 and Pitfall 1 all call for five of *her* real photos in week 1, judged by relatives. The charter says real photos are gathered only after the pipeline is locked, and that nothing may tip her off. Scanning five prints from her albums this week is gathering, and consulting relatives who are not yet "in on it" is a leak risk. Fix: run the bake-off on stand-in photos that have the same defects (the maker's own childhood prints, a consenting relative's, or public-domain archival prints from an institution's open collection), and judge likeness with the maker and one confirmed insider. Move the real-photo line-up to the vertical slice, after the "who is in on it" decision (charter, open decisions; my charter review 1.3.4).

---

## 4. Nudges (at most 8, each with file, section and change)

1. **`playbooks/ai-imagery.md`, "How to do it" Steps 3, 7, 8 and Exercises 1, 5, 6.** Add a Windows column or line under each command: `magick a.png b.png -morph 14 frames\m_%02d.png`; `Get-FileHash 01_masters\*.tif -Algorithm SHA256 | Export-Csv checksums.csv`; and PowerShell-safe quoting for the ffmpeg `zoompan` and `xfade` filters. Mark each as "untested on Windows" until the maker runs it, and put the install route (native, WSL, or the cloud container for CPU steps) in Step 0. (Resolves C1.)

2. **`playbooks/ai-imagery.md`, Exercise 3; `research/ai-imagery.md`, Open questions 1; `SKILL.md`, Procedure step 15.** Reword the bake-off to use stand-in photos with matching defects (faded colour print, small black-and-white print, soft group shot, torn print, 1990s digital file) that are *not* from the mother's archive; name who may judge (the maker plus confirmed insiders only); and add to the skill's step 15: "Relatives consulted for likeness must be on the insiders list in `GATHER.md`." (Resolves C2.)

3. **`research/ai-imagery.md`, Q8 "Reality Ladder" table; `playbooks/ai-imagery.md`, Step 10 table; `SKILL.md`, step 13.** Fix the IPTC mapping for hand-made work. `humanEdits` is for non-generative edits *to captured media*; a hand-built voxel or clay character or scene is `digitalCreation` ("created by a human using non-generative tools", added 2024-09-17). So: L3 hand route = `digitalCreation` when drawn from scratch, `composite` when layered over a real photo; L5 hand-built = `digitalCreation`; L5 AI-built = `trainedAlgorithmicMedia`; L5 mixed = `compositeSynthetic`. Verified against [89] today.

4. **`research/ai-imagery.md`, Summary item 1 and Q8; `playbooks/ai-imagery.md`, Core principle 1 and Step 6.** Make the house rule operational at L2. As written, a diffusion "restore this photo" pass (SeedVR2, Qwen-Image-Edit, Gemini) can redraw a face and the output still looks like a photograph, which is what the rule forbids. Add: *generative repair at L2 is permitted on non-face regions only (tears, stains, backgrounds); faces at L2 are limited to non-generative fixes or CodeFormer/GFPGAN at `w` 0.7 or higher with blend-back; any generative change to a face either moves the image to L3 (it must then look drawn) or is rejected.* This also tells the agent what "R" on screen means.

5. **`playbooks/ai-imagery.md`, new short section after Core principles, "When not to restore"; `research/ai-imagery.md`, Stage 2 "Keeping results honest".** Add the story-side rule: decide the restoration level per chapter from what the chapter needs, not from what the tool can do. Fade, grain, Polaroid borders, the scalloped edge, the date stamp and the handwriting on the back are era signals that the `animated` track will want; keep an untouched L0/L1 version of every hero photo in the timeline, and promote E1's "show the untouched original beside the restoration at least once" from a reuse note to a principle.

6. **`playbooks/ai-imagery.md`, Step 6 item 2 and Exercise 3 step 2(b); `research/ai-imagery.md`, R2 step 2 and Stage 6 FramePack rows; Summary item 14.** Three accuracy corrections: (a) the Real-ESRGAN README's ncnn model list does not include `realesr-general-x4v3`; use `-n realesrgan-x4plus -s 2` as the documented example, or verify the general model ships in the portable zip (research follow-up 3); (b) FramePack's README says GTX 10XX/20XX are "not tested", not excluded, so write "RTX 30/40/50 tested; older cards untested"; (c) change the Summary's "40 to 75 human hours" to match the Q9 table ("40 to 80; 45 to 80 with no GPU").

7. **`SKILL.md`, header "Read these before you start", References, Procedure steps 2, 3 and 12.** Replace absolute `...` paths with repo-relative paths (`playbooks/ai-imagery.md`, `research/ai-imagery.md`) so the skill survives the move to GitHub and to the maker's PC. In step 2 add the stop condition: "If there is no GPU and no cloud approval, stop after L1, log the row, and hand the photo to the maker with the candidate routes." In step 12 and the playbook's Step 10 caption, replace the fixed "2026" with the interview date from `manifest.csv` ("Reconstructed from [name]'s memory, [interview date]").

8. **`research/ai-imagery.md`, Stage 6 cloud table and Q9 hardware-tier table; `playbooks/ai-imagery.md`, Step 8 "Cloud options"; `SKILL.md`, step 11.** Draw the conclusion the note already contains: per the note's own reading of [82], Veo I2V `personGeneration` accepts only `allow_adult`, so childhood photos cannot go through Veo image-to-video at all. State this plainly in the no-GPU row ("6 Image-to-video: for photos with children, parallax or local only; cloud I2V not available") and add "photo contains a child" to the skill's step 11 as a hard local-only condition. This matters for a piece that starts in childhood.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. Windows install path for the no-GPU toolchain: do ffmpeg, ImageMagick 7, Real-ESRGAN ncnn, rembg and Depth Anything V2 Small run natively on Windows for a learner, or is WSL the sane default? Which needs Python? One tested command per tool on a Windows machine, dated.
2. Maker's hardware inventory (my charter review 1.3.2): GPU model and VRAM, RAM, free disk, scanner access. Until this exists the tier table stays hypothetical.
3. Does the Real-ESRGAN ncnn portable release include `realesr-general-x4v3` weights, and what is the exact flag to select it? Check the release assets, not the README.
4. Veo 3.1 `personGeneration` rules for image-to-video: confirm `allow_adult` is the only option, and whether an image containing a child is rejected or silently altered. Read [82] directly and date it.
5. ExifTool on Windows: exact command to write `XMP-iptcExt:DigitalSourceType` to a TIFF and read it back, and what survives in MP4/MOV (XMP sidecar versus embedded). Run it, do not quote it.
6. Public-domain stand-in photos for the bake-off: an institution's open collection with faded colour prints, small black-and-white prints and torn prints, with licence terms read on the page.
7. Creator evidence on archival inputs (the budget-starved gap): three creator posts or videos from 2025 to 2026 showing Kontext, Qwen-Image-Edit or SeedVR2 on real low-resolution family photos, with before/after shown.
8. Family reactions to animating the dead: at least two first-hand accounts (not vendor marketing) from Deep Nostalgia-style use, to inform Decision 4.

---

## 6. Strengths (keep these)

- The method note at the top of the research: budget, what was and was not fetched, how summaries were checked. Every track should copy it.
- The house rule "if it looks like a photograph, it is a photograph; anything invented is drawn", and the Reality Ladder with four carriers (filename, `steps.csv`, XMP, credits). This is the "visibly reconstructions" convention my charter review asked for, delivered.
- "Carry age in the character design, not in one embedding" (Summary 6, Stage 4b) is the single most useful technical finding for a 50-year likeness problem, and it is cheap.
- The honesty ranking of morph methods, with the finding that FILM is built for near-duplicates and first/last-frame models invent faces, and the default to chain morphs through real intermediate photos.
- Privacy table with verdicts and dates, and the default of "unreadable terms mean no".
- Stale-tool alarms with archive dates (FILM, Old Photos, DeOldify, IP-Adapter, Nano Banana 1).
- Playbook decisions marked "from the note" versus "scribe's reading, confirm", and the budget mismatch caught by the scribe.
- Skill description names the verbs an agent will see (scan, restore, upscale, cut out, stylise, morph, animate) and the decision cases (label, consent, privacy), so it will trigger.

---

## 7. Advisor insight

Make the restoration ladder itself the one mechanic of the piece. Every photo enters the way it was found: faded, small, a scan with its border and the writing on the back (L0). It is *attention* that restores it: a dwell, a hover, a relative's voice saying who is in it, and the print clears to L1 or L2 while you watch. Nothing is restored unless someone remembers it, and photos nobody could name stay faded on purpose. This passes the Principle 2 test (memories fade unless tended; that is true of this life and of every life, but *which* photos clear and whose voice clears them is unmistakably hers), it makes the honesty labelling intrinsic instead of a caption (the viewer has seen the original a second earlier), it costs almost nothing (two versions of each hero photo and a dissolve, both already in the pipeline), and it turns the `ai-imagery` track's "show the untouched original at least once" into the grammar of the whole film. It also gives the `story` track a concrete reason to collect voices naming photos, which is the highest emotion-per-hour asset we have.

---

## Changelog
- 2026-10-18: round 1 review by the Fable advisor; 11 spot-checks; verdict revise with 2 critical issues and 8 nudges.
