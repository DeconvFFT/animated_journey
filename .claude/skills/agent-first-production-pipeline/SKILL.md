---
name: agent-first-production-pipeline
description: "Use when building, rendering, validating or handing off Life Journey shots and chapters that agents generate from code (seekable SVG and GSAP scenes, photo-motion chains with ffmpeg and Pillow, Blender hero shots), or when setting up the render harness, media manifest, review gates, or the cloud-versus-PC split. Triggers include seekTo(t) scenes, render.mjs, shot briefs, gates G0 to G6, a photo set's cloud level, ProRes 4444 alpha overlay, BT.709 colour tags, lj.ps1, and any hand-off to or from the ArtCraft apps on the maker's Windows PC. Do not use it for interviews or story gathering (use life-story-interviewing), for consent and label decisions on AI-altered photos (use ai-photo-to-animation-pipeline), or for FilmCraft or EffectCraft motion details alone (use craft-apps-motion-refinement)."
---

# Agent-First Production Pipeline

## Purpose

Let agents make Life Journey shots from code and text, rendered in the cloud container where possible. The maker refines a few shots by hand in the Craft apps on Windows. Output must be repeatable, licence-clean and private. The Craft apps are free, early-alpha refinement layers, so nothing critical may depend on them.

Human guide: `playbooks/agent-pipeline.md`. Evidence, measurements (M1 to M21) and open gaps: `research/agent-pipeline.md`. Charter: `CHARTER.md`.

## When to use / when not to

Use it for:
- writing or changing a Route A scene, a Route B photo-motion script, a class C hero shot, or a `brief.yaml`;
- building the render harness, validators, manifests, review packs or gate files;
- preparing a hand-off for PhotoCraft, VectorCraft, FilmCraft or EffectCraft, or validating one that comes back.

Do not use it for:
- story gathering, interviews or dignity decisions (use `life-story-interviewing`);
- consent or label decisions on AI-altered photos (use `ai-photo-to-animation-pipeline`);
- FilmCraft or EffectCraft work on its own (use `craft-apps-motion-refinement`), or PhotoCraft and VectorCraft visual work alone (use `craft-apps-visual-refinement`).

## Procedure

1. **Confirm the phase.** Read the charter. Real family material may enter the pipeline only after the maker confirms it is locked. Until then, use synthetic or stand-in material only.
2. **Check the project settings** in the repo: 1920 x 1080; one frame rate for the whole film (24 unless the maker has decided otherwise); Rec. 709 and sRGB; audio 48 kHz, 24-bit. Never change them per shot.
3. **Classify the shot.** Class A is a parameterised photo move (seeded per photo, and capped by gate G4 in step 16), B a designed graphic, C a hero 3D shot, D a title or caption. Route A is a seekable web scene. Route B is a photo-motion chain. `blender` is for class C only. `craft` (EffectCraft titles) runs in the container only after spike S1 passes; on the maker's PC the EffectCraft template route is available once the five-minute test in `research/craft-motion.md` R7 passes.
4. **Check every input** in `manifests/media.jsonl`. If an input's `cloud` is `none`, the agent still writes the brief, the script and the expected `render.json`, commits them and marks the shot `pc-render`; the maker runs `lj.ps1 run <shot>` on the PC and pushes the validator JSON and the preview. Only the cloud render is skipped. Raising the level is never the agent's move. A `preview` set may use only proxies (about 768 px JPEG or 480p). Never upload full-size originals or masters, and never send family photos to a hosted renderer.
5. **Write `brief.yaml`** with: beat, `source_ref`, duration, route, every input with its `cloud` level, palette (six colours or fewer), motion family, seed, audio cues and acceptance checks. Ask the maker for gate G0. Do not start motion until G0 is approved.
6. **For a new look, build three style frames first** and ask for gate G1. Record the palette, each font with its licence file, and each texture in `textures.json` with its source URL and date.
7. **Build a Route A scene.** The page defines `window.seekTo(t)` as a pure function of `t`, which sets the picture and does nothing else. Build the timeline paused (`gsap.timeline({paused:true})`) and set `seekTo = t => { tl.time(t,false); return true; }`. Set `gsap.config({lazy:false})` anyway; lazy rendering did not change the probe frames (M10). Give every rough.js shape a nonzero `seed` derived from its id. Never use `Math.random()`, `Date.now()` or real-time timers. Set `window.ready = true` after fonts and images load. Vendor GSAP, rough.js and three.js into `pipeline/lib`, with their licence files.
8. **Render Route A in shards.** Run `node pipeline/bin/render.mjs --page scene.html --out frames --fps 24 --seconds N --shard i/n`. Each shard writes PNG frames through a temp file and rename, and skips frames that already exist. Keep each job at 10 minutes or less. Use `--ffmpeg` only for a whole shot in one process. Encode the frames afterwards with `ffmpeg -framerate 24 -i frames/f_%06d.png -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v libx264 -crf 18 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`, run the colour-patch check (Validators), then delete the PNGs. For alpha overlays, use `--alpha` and ProRes 4444 with `-vf "scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v prores_ks -profile:v 4444`. Use these chains as written. The bare `-pix_fmt yuva444p10le` encode gave BT.601 pixels on ffmpeg 6.1.1, and the format-first H.264 order measured 5/255 RGB error against the ±3/255 tolerance (research Q-F1), so the order is part of the chain. Resume rule: a shard job re-run after a reclaim skips frames that exist; never pass `--ffmpeg` to a sharded run.
9. **Build a Route B shot.** Use a seeded generator (seed from the brief) to pick direction, duration, ease family, hold, drift and wobble for each photo, so no two photos move alike. Conform each still with ImageMagick (auto-orient, fit to the sequence plus headroom, 8-bit, strip the profile; see R1 in `research/craft-motion.md`). A 1080p sequence needs stills of about 2880 x 1620. Make grain as an 8-frame pre-rendered overlay, loop it on twos and blend it with `blend=all_mode=overlay:all_opacity=0.35`. Do not use ffmpeg's `noise` filter for long renders (M6).
10. **Run the template and pacing checks.** `lint_template.py` should flag more than 60% of tweens sharing one ease string, uniform stagger, one transition type above 70% of cuts, the same move on every photo, or a zoom-in on every photo. `edit_audit.py` should check that holds after a payoff are at least 0.75 s and that shots under 1.5 s are impact frames only. Both are built in spike S5. Until they exist, do these checks by hand and say so in the review.
11. **Self-check.** Run the validators in the checklist below. Allow at most three fix loops. Write any failure into the review file. Stop and report, and switch to the fallback route, if a validator fails twice, if the critic says `revise` three times, or if a Craft app crashes.
12. **Make the G2 review pack.** Include a contact sheet of 8 timed frames, frame strips for key moments, full-resolution crops of faces and type, a preview of 20 MB or less, and `render.json` (inputs, seed, tool versions, command line, hashes). Run a fresh-context critic twice with different frame orders and compare the answers. The critic sees stills only, so never record a smoothness or sound judgment from it. Ask the maker to listen.
13. **Revise at most twice, then freeze the scene.** Answer each line of the maker's `feedback/<shot>.md` with `done`, `declined (reason)` or `question` in `render.json`.
14. **Hand off to a Craft app** only in these formats:
    - PhotoCraft: OpenRaster `.ora` (a zip of PNG layers plus `stack.xml`). Layer names are the IDs. Use no adjustment layers, layer styles or live text. Layers are 8-bit sRGB straight-alpha PNGs.
    - VectorCraft: SVG with unique IDs matching `^[A-Za-z][A-Za-z0-9._-]*$`, `data-pivot` and `data-z` on groups and shapes, and `viewBox="0 0 W H"`. Do not rely on `class`, `<style>`, group transforms or SMIL or CSS animation. Run svgo only as a lint, with `cleanupIds:false`, because its default preset strips every ID (M17).
    - EffectCraft: a static SVG subset in, and an RGBA PNG sequence or ProRes 4444 out. RGBA PNG sequence preferred; ProRes 4444 only after the colour-patch test passes, because EffectCraft issue #340 reports ProRes 4444 as "tagged bt709 but sRGB-encoded" (`research/craft-motion.md`). Use `effectcraft-cli render` in the container only after spike S1 passes; on the maker's PC the template route is available once the five-minute test in `research/craft-motion.md` R7 passes. Source is at `https://github.com/storytold/effectcraft` (tag v0.11.1) [68].
    - FilmCraft: pre-conformed 8-bit sRGB stills; an OTIO timeline with `metadata.filmcraft` for motion; H.264 8-bit 4:2:0 or ProRes at a constant frame rate; absolute `file:///` paths on one project root. Never hand-write an `.fcproj`.
    - Every export gets a new file name. Never overwrite. Validate it on return.
15. **Hand back and render the final.** Validate the export. Re-attach the GSAP timeline and classes by ID. Render at full resolution and save as `..._v00N_appr`. Add a line to `manifests/renders.jsonl`.
16. **Assemble the chapter.** Emit the neutral timeline spec and generate the OTIO file. Validate it. The maker opens it in FilmCraft on the PC and exports ProRes 422 HQ. Make the H.264 access copy with ffmpeg, then measure loudness with `ebur128`. Run gate G4 (pacing, variety, continuity, captions). Its class-A rule: no more than three class-A shots in a row without a held still, a class B, C or D shot, or a voice-only beat; at least one shot per chapter where the photo does not move at all. Gate G5 is for the proxy relative, and an agent never passes it. Run gate G6 (technical QC, including a TV test at about 3 metres).
17. **Commit text only** to the private repo: code, briefs, manifests (person IDs, never names), reviews, licensed fonts and textures, and vendored libraries. Never commit media. Keep the repo plain Git, with each file under 50 MiB and the repo target under about 200 MB (J). Commit messages and file names must look harmless.
18. **Close the session.** Update manifests and the ledger. Prune drafts: keep the approved render, the last two drafts per shot, and any draft a review cites. Delete the other drafts after 14 days. Keep every `renders.jsonl` line.

## Checklists

**Before rendering:** settings match step 2; brief approved at G0; every input's `cloud` level is set by the maker and allows this use; seed is set; no `Math.random`, `Date.now` or real-time timers in the scene; fonts and textures have licence files; spike results for this route are recorded.

**Validators (before any hand-off):**
- Video: `ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,color_space,color_range,color_primaries,color_transfer -of json <file>`. The frame rate must equal the project rate. H.264 must show yuv420p, BT.709 and `tv` range. The frame count must equal duration times frame rate. `ffmpeg -v error -i <file> -f null -` must print nothing, and the `moov` atom must be present.
- Alpha: the pixel format includes `a` for ProRes 4444 (`yuva444p12le` was reported in testing, M12).
- Colour matrix (pixels, not tags): encode a 3-patch frame (pure red 255,0,0; 50% grey 128,128,128; skin tone 224,172,140) through the shot's exact command line, decode it to `rgb24` with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`, and require every channel within ±3/255. Run it once per command-line template, and again whenever the ffmpeg version differs (the PC build is ffmpeg 9.0.2 from winget, not the container's 6.1.1). Tags alone are not evidence (research note, Q-F1).
- SVG: renders non-blank; every ID is present and matches the pattern; `check_ids.py` exits 0 on original and touched files.
- ORA: zip opens; `stack.xml` parses; every `src` exists; layers sit inside the canvas; names are unique and match the ID pattern.
- OTIO: parses with `opentimelineio` (M16); every media target exists; clips sit inside their available range; the rate matches the project.
- Audio: 48000 Hz, 24-bit; record loudness and true peak with `ffmpeg -i <file> -af ebur128=peak=true -f null -`.
- Lottie (interchange only): reject `layers: []`, and check opacity on a 0 to 100 scale.
- Determinism: render two frames again and compare with `compare -metric AE -fuzz 1%`. Exact hashes are expected without SVG filters. With filters, accept up to 100 differing pixels per frame (M10).

**Before anything goes to the cloud:** the maker set the `cloud` level; the account's model-improvement setting is off before the first `preview` (otherwise transcripts are kept 5 years and may be used for training, versus 30 days when it is off) [51]; only proxies or cleared images are used; no hosted renderer or memorial-video service; API keys are in the environment's network secrets [49].

**Repo hygiene:** no names, only IDs (`P-001`); the key that maps IDs to names stays offline; no media; innocuous repo and commit names.

## Quality bar

**Good:**
- Each shot names its source, and its beat comes from her life, not from a template.
- Motion uses several families, with varied easing and holds of 0.75 s or more after each payoff. Nothing loops or stretches to fill a slot.
- Two renders match (or fall within the stated tolerance). Faces come from the photo and are never regenerated.
- The palette has six colours or fewer, sampled from her prints. Every font has its licence file.
- Validators are green, with JSON attached, and `render.json` is complete.
- The maker has watched the shot with sound on.

**Mediocre (fix before review):**
- Default easing, an evenly spaced stagger, one stock transition, centred typewriter titles, the same zoom on every photo, or neon-on-dark gradients.
- Validators pass but nobody has listened.
- Full-frame live SVG filters, which are slow and not exactly repeatable (1.2 fps and 5 of 36 frames differing in M10).
- The critic approves a shot that the maker has not watched.

## Ethics and privacy guardrails

- **Real memories stay real.** Do not invent events, people, faces or words. Reconstructions are visibly stylised and labelled with their level on the ladder in `research/ai-imagery.md` [2]. The label appears in the manifest, the file name and the credits.
- **No photoreal generation of people, no voice cloning, no AI-sung songs.** Use her handwriting as a font only for words she actually wrote [1].
- **Consent level is the maker's decision.** The default is `none`. An agent may not raise a `cloud` level, and may not treat "pending" consent as cleared.
- **Surprise.** Keep media and names out of the repo. Keep repo names, commit messages and folder names harmless. Assume phone notifications can show on shared screens. Keep the project in its own browser profile.
- **Dignity.** Loss, illness, separation, money and conflict go to the proxy at G5. Anything she might not want seen in front of others stays out of the shared version (charter principle 5) [1].
- **Permissions and money.** No unattended multi-agent runs and no bypass-permission studios. One agent, one shot, at most three in parallel, two revision rounds. One unattended run cost $207.58 for 90 seconds [38].
- **Control ports.** Start a Craft app's control port only for the session that needs it, then close it. PhotoCraft requires a token. VectorCraft and LightCraft do not authenticate [4]. A cloud session cannot reach the maker's PC loopback ports [47][50].
- **Computer use.** The CLI cannot click apps on Windows; only the Desktop app can [48]. Use the Craft apps' own channels, files, or the maker's hands.

## References

- Human playbook: `playbooks/agent-pipeline.md`. Its Sources list uses the same [n] numbers as below.
- Research notes: `research/agent-pipeline.md`. Recipes R0 to R12, measurements M1 to M21, open questions.
- Charter: `CHARTER.md`.
- Open gaps (TODO(research)): whether a running background job keeps the cloud container awake (spike S4); whether cloud sessions accept image attachments; the maker's PC specifications (`lj.ps1 doctor` is designed, not built); plan usage limits for about 19 weeks; GitHub LFS rates for personal accounts; Remotion 5.0 licence text; the cause of SVG-filter differences; Cycles on a rented GPU; HyperFrames determinism rules; the Manim apt route. The `lint_template.py`, `edit_audit.py` and `render.mjs` scripts are designed and not yet written.
- Corrections in force: the container has Playwright 1.56.1 and Chromium 141 preinstalled (M3), so older notes that say otherwise are wrong. EEVEE rendered headless in the container (M14), but this is proven only for one image and scene. Spike S1 is still the gate for any Craft command-line use in the container. The Gemini 2.5 Flash Image shutdown date (2026-10-02) has passed.
- Key URLs (each read on 2026-10-18):
  - [36] `https://github.com/bishpls/animation-pipeline`
  - [37] `https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md`
  - [38] `https://github.com/MorShahrezaye/claude-code-film-studio`
  - [43] `https://scuti.asia/?p=23313`
  - [22] `https://github.com/heygen-com/hyperframes`
  - [25] `https://github.com/rough-stuff/rough/wiki`
  - [26] `https://gsap.com/docs/v3/Eases/RoughEase/`
  - [29] `https://openfontlicense.org/ofl-faq/`
  - [28] `https://docs.ambientcg.com/license/`
  - [47] `https://code.claude.com/docs/en/remote-control`
  - [48] `https://code.claude.com/docs/en/computer-use`
  - [49] `https://code.claude.com/docs/en/cloud-environments`
  - [50] `https://code.claude.com/docs/en/claude-code-on-the-web`
  - [51] `https://code.claude.com/docs/en/data-usage`
  - [65] `https://ai.google.dev/gemini-api/docs/pricing` (page updated 2026-10-16; its announced changes on 2026-12-01 and 2027-01-01 name no image or video model; re-read it in the week the batch runs)
  - [68] `https://github.com/storytold/effectcraft` (tag v0.11.1)
