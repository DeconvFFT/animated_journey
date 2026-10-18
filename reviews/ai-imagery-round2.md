# Review — track `ai-imagery`, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:** `research/ai-imagery.md` (Sonnet note plus its round-1 follow-up, sources 1 to 144), `playbooks/ai-imagery.md` (Haiku scribe, round-1 revision), `skills/ai-photo-to-animation-pipeline/SKILL.md`, read against `CHARTER.md` (Known facts updated 2026-10-18), `reviews/00-charter-review.md` and my round-1 review `reviews/ai-imagery-round1.md`.
**Verdict:** `revise`, narrowly. All eight round-1 nudges were applied, and applied well: the follow-up research ran the commands instead of quoting them, found a silent failure (`realesr-general-x4v3` writes an all-black image and exits 0) that no README would have revealed, and the scribe carried every correction into the playbook and the skill. One new issue blocks the gate, and it is the charter's fault as much as the track's: the charter now states a public premiere, and the track still plans for a private gift. That changes the licence defaults in all three files. It is a thirty-minute fix.

Good enough to start on now: everything in Stage 1 (scanning), Stage 3 (cutout and parallax), Stage 5 (classic morph), Q7 (privacy), Q8 (labels), Exercises 1, 2, 5, 6 and 7, and the skill's procedure apart from the licence guardrail.

---

## 1. Were the round-1 nudges addressed?

| # | Nudge | Status | Evidence |
|---|---|---|---|
| 1 | Windows forms under each command; "untested on Windows"; install route in Step 0 | **Done** | Playbook Step 0 has winget ids, the Real-ESRGAN zip, `py -3.12 -m venv`, ExifTool unzip steps, `wsl --install` and the cloud-container caveat; Steps 3, 7, 8 and Exercises 1, 5, 6 each carry a Windows line marked untested. Research Q1 table gives the vendor source per tool. |
| 2 | Bake-off on stand-ins; name the judges; insiders rule in skill step 15 | **Done** | Exercise 3 uses four Commons candidates with licences read on the page; judges are the maker plus confirmed insiders; research Open question 1 and SKILL step 15 both say relatives must be on the insiders list in `GATHER.md`. |
| 3 | IPTC mapping for hand-made work | **Done** | Q8 ladder, playbook Step 10 table and SKILL step 13 all use `digitalCreation`, `composite`, `compositeSynthetic` correctly; `humanEdits` restricted to captured media. |
| 4 | House rule operational at L2 | **Done, with one question back to me** | Summary 1, Q8 "Round 1 operational rule", Core principle 1, Step 6 "What L2 permits", SKILL step 8. The note asks whether colourising a face counts as a generative change. Answered in section 4, nudge 2. |
| 5 | "When not to restore" | **Done** | New playbook section after Core principles; research Stage 2 items 9 to 11; principle 9 "Show the original". |
| 6 | Real-ESRGAN model name; FramePack wording; budget mismatch | **Done, and better than asked** | The follow-up downloaded both portable zips, listed the model files, and ran the bad flag. FramePack reads "RTX 30/40/50 tested, older cards untested". Summary 14 reads "40 to 80 (45 to 80 with no GPU)". |
| 7 | Repo-relative paths; no-GPU stop condition; interview date in caption | **Done** | SKILL header, References, step 2 and step 12; playbook Step 10 and Exercise 7. |
| 8 | Children and Veo image-to-video | **Done** | Stage 6 cloud table, Q9 tier table row 6, playbook Step 8 "Photos with a child in them", SKILL step 11 hard local-only condition, all citing [82] and the Vertex page [116]. |

The round-1 follow-up also corrected three things nobody asked for: rembg's default model is now `bria-rmbg` (1 GB, restricted weights), so every command names `-m u2net`; ImageMagick 7 on Windows is `magick`; and the Q9 CPU timing was replaced with a measurement. That is the right instinct.

---

## 2. Spot-checks against primary sources

Nine claims fetched today (2026-10-18), chosen to avoid the eleven I verified in round 1. Fetched pages treated as data.

| # | Claim in the note or playbook | Source | Result |
|---|---|---|---|
| 1 | Veo 3.1 / Fast / Lite: image-to-video, interpolation and reference images accept `allow_adult` only; text-to-video `allow_all` only; EU/UK/CH/MENA `allow_adult` only; videos stored 2 days; durations 4, 6, 8 s; `lastFrame` exists; no text about children | [82]/[114] ai.google.dev/gemini-api/docs/veo | **Confirmed on every point.** New detail the note lacks: 1080p and 4K (and reference images) require the 8-second duration. See nudge 8. |
| 2 | Vertex Veo page: Child category codes 58061214 and 17301594, "Rejects requests to generate content depicting children if `personGeneration` isn't set to `allow_all`"; input-image rejection wording; "some generated output is being blocked"; last updated 2026-10-15 | [116] docs.cloud.google.com | **Confirmed verbatim.** The first fetch returned navigation only; the text sits past the 100,000-character mark. Worth a note in the source entry so the next reader does not conclude the page is empty. |
| 3 | ExifTool current version 13.59, dated May 27, 2026; downloads point to SourceForge | [117] exiftool.org | **Confirmed.** "Download Version 13.59 (7.9 MB) - May 27, 2026." |
| 4 | WanGP v18.17 on 2026-10-15; "as little as 6 GB"; GTX 10XX and newer, AMD RDNA 2 to 4; Windows and Linux; licence unstated | [77] github.com/deepbeepmeep/Wan2GP | **Confirmed.** README says "WanGP is free to use locally (see the license for terms)" and names no licence type, as the note says. |
| 5 | ImageMagick 7.1.2-34; `winget install ImageMagick.Q16-HDRI`; command is `magick` ("magick logo: logo.gif"); `vcomp140.dll` note | [120] imagemagick.org/download | **Confirmed.** |
| 6 | Luma Plus $30 per 10,000 credits; Ray3.2 100 credits per 5 s at 720p, 400 at 1080p; keyframes not on the pricing page | [81] lumalabs.ai/pricing | **Confirmed.** Page also shows $25 per month billed yearly. |
| 7 | GFPGAN: v1.3 "may slightly change identity"; Apache-2.0; example command `-v 1.3 -s 2`; "the sources give GFPGAN no `w` dial" | [17] GFPGAN README and `inference_gfpgan.py` (raw file, master) | **Partly wrong, and the TODO is closable.** The README's wording is "have a slight change on identity" (the note's quotation marks are slightly off). The README's option list has no weight flag, which is why the note says none exists, but the script defines `-w`/`--weight`, type float, default 0.5, help "Adjustable weights.", passed as `weight=args.weight` to `restorer.enhance`. The script also accepts `-v 1.4` and `RestoreFormer` even though the help text lists only `1 | 1.2 | 1.3`, and the README says V1.4 "produces slightly more details and better identity than V1.3". See nudge 3 and research follow-up 1. |
| 8 | DDColor: Apache-2.0; last news 2024-01-28; `scripts/infer.py --model_name ddcolor_modelscope --input ...` | [28] github.com/piddnad/DDColor | **Confirmed.** The README does not say whether DDColor preserves the input luminance channel, so the colourisation ruling below is written as a test to run, not a property to assume. |
| 9 | This session is a cloud VM, not the maker's PC | Local check today | **Confirmed again.** Kernel 6.18.44-fc, 4 vCPU, 15 GiB, no `nvidia-smi`, no `/mnt/c`, no WSL markers, no USB bus. The relayed request says the session is "open on my local system"; whatever is open, the shell this team runs in cannot see the Windows machine, its GPU or its scanner. The Q2 PowerShell block in the research note remains the only route to the hardware tier. |

Eight of nine hold; the ninth (GFPGAN) is an understatement caused by trusting the README over the code, and it resolves a TODO rather than opening one. Accuracy remains high.

---

## 3. Scores (1 to 5)

| Criterion | Score | Why |
|---|---|---|
| Meaning | 4 | "When not to restore" and principle 9 put the story side in. Era signals are now content, not defects. Still 4 rather than 5 because the track has not yet been asked which chapters get which restoration level; that is correctly left to the story and film-story tracks, but the playbook could say so in one line. |
| Specificity | 5 | Commands run, not quoted; zip contents listed; timings measured; stand-in photos named with licences; Windows forms given per command. |
| Accuracy | 4 | Eight of nine fresh spot-checks hold and the method notes are honest. Deductions: the private-gift framing contradicts the charter's Known facts; the GFPGAN quotation and dial claim; the Vertex source entry does not warn that the text is past the fetch cut-off. |
| Feasibility | 4 | The first exercise can now be done within an hour of reading on a Windows PC (install route, `Get-FileHash`, `magick`). The hardware tier is still unknown, which keeps every GPU recipe hypothetical, but the stop condition in the skill and the no-GPU column make that safe rather than blocking. |
| Ethics | 4 | Insiders rule, stand-ins, child rule, the dead, the voice ban, the honest Deep Nostalgia reading: all strong. Two deductions: the licence default is wrong for a public premiere, and the proposed paid test that submits a child's photo to Veo to see what happens is unnecessary (nudge 6). |
| Craft / usability | 4 | Skill description triggers on the right verbs and cases; procedure is followable by an agent; repo-relative paths; stop conditions. Deductions: one double-negative checklist line an agent will misread; the pixel-count rule is keyed to 1080p while the charter's bar is a big screen; the "decisions log" TODO names no file. |

---

## 4. Critical issues (block approval)

**C1. The track plans for a private gift; the charter now states a public premiere.** `CHARTER.md` Known facts (updated 2026-10-18) says "a premiere at a mostly public gathering on Feb 27... treat it as a film with a public audience", and Principle 7 is "Cleared for public screening". `playbooks/ai-imagery.md` Decision 3 leans "plan for a private gift" and says "The occasion and venue are still open in the charter", which is no longer true; Pitfall 6 and the Known gaps repeat it; `research/ai-imagery.md` Open question 7 asks "Premiere or private gift?"; `SKILL.md` Ethics guardrails say "Non-commercial weights... are acceptable for a private gift only", and the Before-any-release checklist asks the same question. Followed as written, an agent or the maker would pick FLUX.1 Kontext dev (non-commercial), SUPIR, InfiniteYou or the `bria-rmbg` weights on the assumption that nobody outside the family will see the result. Fix: nudge 1. The real open question is narrower: is the screening free (non-commercial licences may still be fine, but each must be read for "public performance") or ticketed (non-commercial weights out).

---

## 5. Nudges (at most 8, each with file, section and change)

1. **`playbooks/ai-imagery.md` Decision 3, Pitfall 6, Known gaps last bullet; `research/ai-imagery.md` Open question 7 and Pitfalls item 6; `SKILL.md` Ethics guardrails "Licences" bullet and Before-any-release checklist.** Replace "private gift versus public or ticketed" with the charter's fact: the premiere is public (Known facts; Principle 7). Delete "The occasion and venue are still open in the charter." Reframe the decision as *free public screening versus ticketed*, with the lean: assume a free public screening; where two tools do the same job choose Apache, MIT or BSD; before using any non-commercial weight (FLUX.1 Kontext dev [33], SUPIR [21], InfiniteYou [42], Depth Anything V2 Base/Large [58], `bria-rmbg` [55]) read its licence text for public exhibition and record the reading in `steps.csv`. In the skill, change the guardrail to "Non-commercial weights need a licence read for public exhibition before use; ticketed showing excludes them." (Resolves C1.)

2. **`research/ai-imagery.md` Q8 "Round 1 operational rule" last sentence; `playbooks/ai-imagery.md` Step 6 "Colour, for black-and-white prints" TODO(review); `SKILL.md` step 8 last sentence.** Answer to the open question: colourising a face is *not* a generative change to the face if the tool changes chroma only and leaves the original luminance intact, because the form of the face is still the record and only the colour is estimated; it stays L2 with the "colours estimated" caption. It *is* a generative change if luminance or texture on the face moves. Make it testable: convert original and result to Lab and diff the L channel over the face box; the AI team writes the script; set the threshold in the bake-off. DDColor's README does not state whether it preserves L [28], so run the test rather than assume. Remove the TODO(review) in all three places.

3. **`playbooks/ai-imagery.md` Step 6 "What L2 permits" second bullet and Exercise 4; `research/ai-imagery.md` Q8 operational rule ("GFPGAN has no `w` dial... TODO(research)"), R2 step 3, Tools table GFPGAN row, Pitfalls item 3.** Replace the TODO with: "`inference_gfpgan.py` has `-w`/`--weight`, default 0.5; `-v` also accepts `1.4` (README: 'slightly more details and better identity than V1.3') and `RestoreFormer` although the help text lists only 1, 1.2, 1.3 (verified from the script on 2026-10-18)." Correct the quotation to "have a slight change on identity". Do not state which end of `-w` is more faithful until research follow-up 1 confirms it; until then the playbook's fidelity dial is CodeFormer's `w` [15].

4. **`playbooks/ai-imagery.md` Step 5; `SKILL.md` step 7; `research/ai-imagery.md` Q1 "Output size check".** Key the upscale decision to the delivery master, not to 1080p. Charter Principle 6 is a big screen; until the `theatrical-delivery` track fixes the master (2K DCP is 2048x1080; UHD is 3840x2160), assume UHD and state the rule as arithmetic: pixels needed across = timeline width × (1 + push-in) × crop factor. A 3600x2400 scan with an 8 percent push-in on a UHD timeline needs about 4,150 px across, so "do not upscale a 4x6 at 600 ppi" is only true for 1080p. Options to list: scan hero prints at 800 to 1200 ppi, or allow a 2x Real-ESRGAN on hero prints as an L2 step, or keep push-ins under 5 percent. Mark "TODO(theatrical-delivery): master resolution".

5. **`playbooks/ai-imagery.md` Decision 6 and Step 0 "Cloud container" bullet; `SKILL.md` step 3; `research/ai-imagery.md` Q7 "Beyond terms".** Reconcile the charter's two lines ("heavy work... happens in the cloud wherever possible" and "nothing personal is... uploaded to a third-party service without the maker's explicit say") with an explicit split: the cloud is the default for everything that contains no family photo (tool installs and tests, the stand-in bake-off, style-LoRA training on the maker's own frames, scripts, renders of hand-built L5 scenes, morph and parallax tests on stand-ins); the maker's PC or a maker-approved rented GPU is the only place for anything with her face or a relative's. Add one sentence: "The team's cloud session is a Linux VM with no GPU and no view of the maker's PC (checked 2026-10-18); the hardware tier comes only from the Q2 PowerShell block."

6. **`research/ai-imagery.md` Q4 "Reading across" paragraph and "Open items after round 1" item 4; `playbooks/ai-imagery.md` Step 8 "Photos with a child in them" last sentence; Pitfall 8 if repeated.** Drop the planned paid Veo test with a child's photo. The rule ("no cloud image-to-video for any photo with a child") already stands on the documented behaviour: image-to-video accepts only `allow_adult` [114] and Vertex documents a Child rejection category [116]. Deliberately submitting a child's image to probe a safety filter teaches us only the shape of the error, costs account risk, and is the kind of act Principle 5 should make us uncomfortable with even on a public-domain photo. Replace with: "No test planned; the rule rests on [114] and [116], both read 2026-10-18."

7. **`SKILL.md` Per-clip checklist third line; Procedure step 2.** Reword "Middle frames inspected. No face matches neither endpoint." to "Middle frames inspected: every face in them matches one of the two end photos." In step 2, replace "(no decisions log file exists yet; TODO)" with the file the orchestrator should create and the agent should read, for example `decisions/hardware.md` with fields GPU, VRAM, RAM, free disk, Vulkan device listed (yes/no), scanner; the skill then has a path to check instead of a TODO.

8. **`research/ai-imagery.md` Summary 10, Stage 6 cloud table Veo row, Q6 restraint rule 6; `playbooks/ai-imagery.md` Step 8 "Generated image-to-video" clip-length bullet and "Cloud options"; `SKILL.md` step 11 image-to-video bullet.** Align the "3 to 5 seconds" rule with what Veo sells: durations are 4, 6 or 8 s, and 1080p and 4K (and reference images) require 8 s [114]. Write: "local models: 3 to 5 s; Veo: 4 s at 720p (the shortest), 8 s and a higher per-second price for 1080p or 4K". The per-clip cost column then needs a 4 s and an 8 s figure rather than a 5 s one.

---

## 6. Research follow-ups (facts not in the notes; do not guess)

1. GFPGAN `-w`/`--weight`: which end of the 0 to 1 range is more faithful to the input, from the GFPGAN architecture code or paper, not from a blog; and whether v1.4 or RestoreFormer changes identity drift on low-resolution inputs.
2. Maker's hardware inventory (still open from round 1): run the Q2 PowerShell block on the Windows PC and the Real-ESRGAN `.exe` once for the Vulkan device line; record the result in the decisions file named in nudge 7.
3. From the `theatrical-delivery` track: the master resolution and frame rate for the premiere (2K DCP, UHD, or both), so Step 5's pixel rule has a number.
4. Licence text, read on the page, for a free public screening: FLUX.1 dev non-commercial licence, SUPIR, InfiniteYou (CC-BY-NC), `bria-rmbg`, Depth Anything V2 Base/Large; and the AGPL question for Upscayl, DepthFlow and Video2X used as tools (distribution versus use).
5. Home-video capture (VHS, Hi8, MiniDV, 8 mm): the charter lists home videos as existing material and the track has not touched them. Capture device, deinterlacing, intermediate codec, and lab options with prices and dates.
6. Whether DDColor (or any chosen colouriser) preserves the input L channel by construction, from the DDColor paper (arXiv 2212.11613) or the code, so the nudge-2 test can be a confirmation rather than a discovery.
7. Still open from round 1: three creator posts (2025 to 2026) showing Kontext, Qwen-Image-Edit or SeedVR2 on real low-resolution family photos with before and after; and the Kopelman and Frosh 2025 paper on Deep Nostalgia for an independent account.
8. Re-run the morph, `xfade`, `zoompan` and `minterpolate` recipes on ffmpeg 9.x, since the sandbox tested 6.1.1 and the Windows builds are 9.0.2 [121][122].

---

## 7. Strengths (keep these)

- The follow-up's method: download the release asset, list it, run the bad flag, measure the failure (all-black PNG, exit 0). This is how every tool claim in the project should be settled.
- The Reality Ladder is now complete and correct against the IPTC vocabulary, with the write-the-URI rule, the ffmpeg-strips-the-tag finding and the sidecar fallback, all from runs.
- The stand-in bake-off: four Commons photos with the licence read on each page, a private-use rule for the two that name real people, and an explicit statement of which defects are still uncovered.
- "When not to restore" and principle 9 turn the era signals into content. That is the charter's Principle 3 applied to photographs, and it will matter more than any model choice.
- The child rule for cloud image-to-video, drawn from two Google pages and dated.
- The Deep Nostalgia reading in Q8 of the follow-up: it names the curation bias, extracts the one genuinely useful warning (an elderly relative seeing a late parent move, in company, without warning), and keeps the default.
- The skill's stop conditions (no GPU and no cloud approval; unknown terms mean no; photo contains a child) make it safe for an agent to run unattended.

---

## 8. Advisor insight

The backs of the prints are a second archive, and the pipeline already scans them. Family photos were labelled by hand for decades: a name, a year, "me and Rita, the summer the car died", in her mother's hand for her childhood and in her own hand for her children's. Use those backs as the film's whole caption and title system. Every on-screen caption that can be sourced from a back is shown *as that back*, flipped over like a print on a table; chapter titles are set in the handwriting of whoever labelled that era's photos; a reconstruction's caption ("Reconstructed from [name]'s memory") is written in the narrator's own hand, taken from a letter already in the archive. Nothing is generated: the words are L0, the hand is real, and the transition (turn the print over) is the oldest gesture anyone has with a photograph. It passes the Principle 2 test because a family that labels its prints, and how, is specific to this family; it solves the era-typography question the `animated` track is chasing without a single font licence; it gives the maker a reason to scan every back at 600 ppi now, when it costs nothing; and when the handwriting changes from her mother's to hers, the audience will know what happened before anyone says it.

---

## Changelog
- 2026-10-18: round 2 review by the Fable advisor; all 8 round-1 nudges verified as applied; 9 fresh spot-checks (8 hold, 1 TODO resolved from source code); verdict revise with 1 critical issue (public premiere versus private-gift framing) and 8 nudges.
