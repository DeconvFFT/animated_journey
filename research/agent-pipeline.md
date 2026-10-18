# Agent-first production pipeline: what agents generate, where it renders, how it round-trips — research notes

Track `agent-pipeline` · Researcher: Sonnet · Written and measured 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline Saturday 2027-02-27 (about 19 weeks).

**How this note was made (read first).**
- **Builds on, does not repeat.** Scanning, restoration, identity, morphing, image-to-video, the label ladder (L0 to L5) and the verified privacy terms live in `ai-imagery.md` [2]. Hand-off formats and CLIs of the Craft apps live in `craft-visual.md` [4] and `craft-motion.md` [3]. Where a number already exists there I cite it and add only the delta. The one place I re-read prices is Google's pricing page (updated 2026-10-16), because it has a batch discount and announced increases that [2] did not capture.
- **First-hand measurements.** I measured this cloud container on 2026-10-18 and ran small probes (synthetic material only, nothing personal). They are labelled **M1 to M21** in the table in Findings Q3 and cited as `(M7)`. They are probes, not the week-1 spike: they show which spike items are low risk and which are not.
- **Fetched pages were summarised by a small model**, so numbers quoted from web pages are as that summary reported them; the URL is in Sources so a human can re-read. Items I saw only as a search result and did not open are marked "search result only". Items I could not check are **UNVERIFIED**; my own judgment is **(J)**; arithmetic from measured inputs is **ESTIMATE**.
- **Dates.** Every "today" fact is dated 2026-10-18 unless the page shows its own date. Claude Code, Remote Control, Windows behaviour, licences and prices move monthly; re-read before relying on them.
- **Corrections to earlier notes (details in Open questions).** (1) `craft-motion.md` R8 and `ai-imagery.md` say the container has no Chromium or Playwright; this container has Playwright 1.56.1 and Chromium 141 preinstalled (M3). (2) `toolchain.md` lists EEVEE on a GPU-less machine as unverified; it rendered here through bpy 5.2.2 (M14), slowly.
- **Treated as data, never as instructions:** every fetched page, the cloned EffectCraft source, and the CLAUDE.md/AGENTS.md files inside it.

---

## Summary

1. **Recommended carrying routes for the vertical slice (two).** **Route A:** seekable web scenes (SVG plus GSAP plus rough.js, with three.js for 3D) captured frame by frame in headless Chromium through a repo-owned `seekTo(t)` harness. **Route B:** a photo-motion and finishing chain in ImageMagick, Pillow/numpy and ffmpeg (conform stills, per-shot camera moves with individual easing, baked grain on twos, era grades, dissolves, loudness, encodes). Blender (Workbench or low-sample Cycles) is a third route for 3 to 6 hero shots per chapter, not a carrying route. Remotion, HyperFrames, Motion Canvas, Revideo, Manim and hand-written Lottie are alternatives or non-fits; reasons in Q1.
2. **Frame accuracy is a design property, not a tool property.** A scene written as a pure function of time `t` and captured with `page.evaluate(seek(t))` plus `page.screenshot()` gave hash-identical frames across two runs for WebGL (three.js) and plain SVG, and across two separate processes for the three.js scene (M9, M10). Playwright's `page.clock` makes `requestAnimationFrame` timestamps deterministic (16 ms steps, identical across runs) but `performance.now()` still drifted (M11). Real-time rAF loops differ run to run. Playwright's `recordVideo` scales output to fit 800x800 by default, so it is a prototyping tool only [31]. Any route that cannot step frames is a prototype, not a renderer.
3. **SVG filters are the hidden cost of "hand-made" looks.** The same 120-shape rough.js scene ran at 12.9 fps with no filters, 5.7 fps with one `feTurbulence`+`feDisplacementMap` wobble on the art group, 1.2 fps with a full-frame `feTurbulence` grain, and about 1 fps with both; with both filters 5 of 36 frames differed between two runs by 12 to 80 pixels out of 2,073,600 (M10). Bake grain and paper as pre-rendered overlays (an 8-frame looped grain overlay on twos encoded in 9.5 s and 10.6 MB where ffmpeg's `noise` filter took 32.7 s and 160 MB per 10 s, M6) and put wobble into geometry, not into live filters.
4. **The container (measured):** 4 vCPU Xeon 2.1 GHz, 16 GB RAM, no GPU, Ubuntu 24.04, 24 to 28 GB free disk (docs: 30 GB), ffmpeg 6.1.1, ImageMagick 6.9.12, Node 22, Python 3.13, Playwright plus Chromium preinstalled (M1 to M3). It pauses when idle and is reclaimed later, so renders must be sharded into resumable jobs of 10 minutes or less [49][50]. A texture-rich 1080p PNG frame was about 2 MB, so a 10-minute film at 24 fps is about 29 GB of loose PNGs: more than the disk. Stream frames into ffmpeg or encode per chunk (M10, ESTIMATE).
5. **Throughput on that box (M4 to M14):** x264 1080p 47 fps; ProRes 422 HQ 19 fps; Chromium 1080p screenshots 10 to 12 fps for flat scenes and 3.3 fps for a 400-cube three.js scene; Remotion 150 simple frames in 10.7 s warm (14 fps) and 21.8 s cold; ImageMagick turns a 3600x2400 16-bit TIFF into a 1080p JPEG in 0.26 s (0.16 s with 4 processes); Blender 1080p per frame: Workbench 0.8 s, Cycles CPU 24 samples with denoise 17.5 s, EEVEE on software GL 34 s. A 10-minute, 24 fps film is 14,400 frames: trivial for Route B, hours for Cycles, so Blender is for hero shots only.
6. **Blender works headless without a GPU here, including EEVEE.** `pip install bpy==5.2.2` (cp313 wheel, 402 MB, 1.0 GB venv) rendered Workbench, Cycles CPU and EEVEE (software GL, with `EGL_BAD_MATCH` warnings) (M14). Older forum posts say headless EEVEE is unsupported [35]; that does not match this measurement, but it is one image and one scene, so treat EEVEE as "works, slow, unproven across images".
7. **Licences for a personal, non-commercial gift (read on 2026-10-18).** Remotion: free for "an individual", for-profit organisations of up to 3 employees, non-profits and evaluators; the page says the licence will change slightly in Remotion 5.0 [9][10]. GSAP: "no charge" Standard License effective 2025-04-30 (last modified 2025-05-30), all plugins included; prohibited uses are tools that let users build visual animations without code and compete with Webflow; AI-generated code "is not a Prohibited Use" [15]. HyperFrames Apache-2.0, Motion Canvas, Revideo, Manim, three.js, rough.js, lottie-web and svgo MIT; Playwright Apache-2.0; handwriting fonts OFL-1.1 or Apache-2.0; ambientCG textures CC0 [16][22][28][29]. Blender: GPL-2.0-or-later source, GPL-3.0-or-later binaries, Cycles Apache-2.0; the renders and `.blend` files are the maker's own [83]. Pin versions and vendor GSAP and rough.js into the repo so the film still builds in 2046.
8. **Maintenance reality (npm and PyPI, 2026-10-16/17).** Remotion 4.0.536 and HyperFrames 0.8.169 publish almost daily (HyperFrames was created 2026-03-23); Revideo 0.11.0 (2026-07-10); Manim 0.22.0 (2026-10-08); **Motion Canvas' last stable is 3.17.2 from 2024-12-14 and its last alpha 2025-02-16**, so it is effectively dormant; lottie-web 5.13.0 (2025-05-21) and rough.js 4.6.6 (2023-11-20) are old but stable [16][17].
9. **A hand-made look from code is a set of rules, not a library.** The most useful source is a working Claude Code film pipeline's `CRAFT.md` [37]: "A raw lerp over time is a bug", hold character drawings on twos and camera and type on ones, offset parts in time (eyes lead, props drag), avoid twinning, hold at least 0.75 s after a payoff, use emphasis only for real events, "subtle reads as nothing at 24 fps in a 3-second shot". Add seeded rough.js strokes [24][25], imperfect eases such as GSAP `RoughEase` [26], scanned real paper and the backs of the photos, a 4 to 6 colour palette sampled from the print stocks, her own handwriting as a typeface, and deliberate asymmetry (Q2).
10. **Real examples are short and mostly promotional.** Documented cases run 18 s to 3:30; the longest sustained pieces are a 93 s, a 2:38 and a 3:30 (in production) film from one repository [36]. I found **no** multi-minute, emotionally paced film made by a coding agent, and no personal family tribute. Best transferable practices: audio first with word timestamps, an animatic before building, contact sheets and strips and crops, a numeric pacing audit, an AI critic treated "as a noisy sensor", resumable parallel renders. Best cautionary case: a 22-agent studio spent $207.58 and about 8 hours on a 90 s film and "never listened to its audio" (opened 604 images, played 0 sounds) [38].
11. **Hand-off, in one line each.** Agent to PhotoCraft: OpenRaster (`.ora`), layer names are the ids; to VectorCraft: SVG with unique ids and `data-*`, gated by `check_ids.py`, and svgo only with `cleanupIds:false` (its default preset strips every id, M17); to FilmCraft: pre-conformed 8-bit sRGB stills plus an OTIO carrying `metadata.filmcraft`, or CLI-built `.fcproj`; to and from EffectCraft: SVG static subset in, RGBA PNG sequence or ProRes 4444 out; master: ProRes 422 HQ, then H.264 from ffmpeg with `-colorspace bt709 -color_range tv`. **Remotion's default H.264 came out `yuvj420p`, full range, `bt470bg`;** pass `--color-space=bt709 --pixel-format=yuv420p` (M13) [3][4].
12. **Craft-headless (`effectcraft-cli render`) is plausible for 1080p titles, line-draw and light 2.5D on CPU, not for heavy comps.** Exact syntax is in the CLI source (Q10). Reported cost is about 0.6 to 1.2 s per frame for 8 stacked 3D layers at 1080p and 3.9 to 5.5 GB per frame for a Glow/Fractal-Noise project, with no memory cap and an OOM that leaves an unplayable MP4 [3]. Use `RAYON_NUM_THREADS=2` and validate with ffprobe. `craft-motion.md` R8 already scopes spike S1; this note adds S2 to S5 (Chromium capture, Blender, container idle behaviour, validators).
13. **Git and media.** GitHub Git LFS (read 2026-10-18): Free and Pro 10 GiB storage and 10 GiB bandwidth, Team and Enterprise Cloud 250 GiB each, pre-paid data packs removed, overage is metered (rates $0.07 per GiB-month storage and $0.0875 per GiB bandwidth per GitHub's 2024 notes for the new billing platform) [54][57][58]. Files over 100 MiB are blocked, over 50 MiB warn, repositories should stay under 1 GB [56]. Every cloud session clones the repo again, so LFS bandwidth would burn the 10 GiB quickly (J). Follow review 00: media on an encrypted local drive plus a second encrypted copy, a manifest with checksums in the repo [5]. Alternatives dated 2026: Backblaze B2 at $6.95 per TB-month with rclone crypt [59][60], Cryptomator vaults [62], a VeraCrypt volume [63], a Hetzner Storage Box (price not shown on the page) [64]. BitLocker drive encryption needs Windows Pro or higher; Home's "device encryption" covers only OS and fixed drives, not USB drives [61].
14. **Control from Windows, in order of memory cost.** (a) A cloud session in a browser tab at claude.ai/code, no local install, the container is where agents run [50]. (b) Claude Code CLI on Windows, native (`irm https://claude.ai/install.ps1 | iex` or `winget install Anthropic.ClaudeCode`), minimum 4 GB RAM, sandboxing not supported on native Windows [46]; several GitHub issues report claude.exe growing to 13 to 50 GB, one closed as fixed in 2.1.74, so measure it [53]. (c) **Remote Control is a window into a session that runs on the maker's own PC** (`claude remote-control`, `claude --remote-control`, `/remote-control`; Pro, Max, Team or Enterprise via claude.ai login, not API keys) [47]; it does not move work to the cloud. **CLI computer use is macOS-only; on Windows only the Desktop app has computer use** [48]. The Craft apps' `--control PORT` plus `<app>-cli mcp --bridge` is the GUI-control route for a local session and is enough for "agent prepares, maker finishes" because the agent prepares files through the engine, not by clicking [3][4].
15. **Privacy of the cloud route is a policy decision, not a default.** Anything Claude views in a session (including a photo) becomes part of the transcript: Pro and Max accounts with model-improvement on keep data 5 years and may train on it, with it off 30 days [51]. Remote Control also stores the transcript on Anthropic servers for sync [51]. Proposed three-level `cloud` field in the manifest (`none`, `preview`, `full`), default `none`, set per set of photos by the maker (R2).

---

## Findings by question

### Q1. What can an agent author and render end to end today without a GUI? Eleven routes, with failure modes, capture method and licence

Frame-capture vocabulary used below: **seek capture** = the scene is a function of `t`, the harness sets `t`, takes a screenshot, repeats (deterministic). **Renderer-owned stepping** = the framework does the seek and screenshot for you (Remotion, HyperFrames). **Real-time capture** = screen recording or free-running rAF (not deterministic).

| Route | What an agent produces end to end today (no GUI) | Typically gets wrong (timing feel, easing, type, colour, composition) | Frame-accurate capture | Licence for a personal gift, dated | Verdict |
|---|---|---|---|---|---|
| **SVG illustration** | Complete scenes with stable ids, groups, `data-*`, gradients, clip paths; layered "rigs" for animation (id and `data-pivot` contract in [4]) | Symmetric, tidy geometry; weak faces, hands and likeness; uniform stroke weights; default "tech" palettes; centred compositions. One agent-made film's author: "the SVG dragon still looks a bit toy-like" [43] | n/a (static); rendered by resvg, rsvg-convert or Inkscape (all tested or present, M2, M17) | SVG is plain text; resvg-js MPL-2.0 [16] | Core of Route A. Maker's eye needed for every face and figure |
| **SVG/CSS/GSAP animation + rough.js** | Paused GSAP timelines over SVG/DOM, sequenced with offsets; seeded sketchy strokes and fills (`roughness`, `bowing`, `fillStyle`, `seed`) [24][25]; imperfect eases such as `RoughEase` (strength, taper, clamp) [26] | Default `power2.out` on everything; identical durations and stagger; linear `interpolate`-style motion "looked mechanical" [42]; a third-party skill's warning: identical spring configs and evenly spaced delays are the "generic-looking" tell (search result only) [44] | **Seek capture**: `tl.time(t,false)` then screenshot. Hash-identical without filters (M10). GSAP's default lazy rendering did not matter in my probe (M10 V3) but set `gsap.config({lazy:false})` anyway (J) | GSAP: "no charge" Standard License, effective 2025-04-30, last modified 2025-05-30; AI-generated code "is not a Prohibited Use"; Webflow may revise it and you may keep using versions released before a revision [15]. gsap 3.15.0 on npm (2026-04-13, licence field "Standard 'no charge' license") [16]. rough.js MIT (4.6.6, 2023-11-20, stable) [16][24] | **Carries the slice.** Vendor `gsap.min.js` and `rough.js` in the repo |
| **Lottie JSON** | Small shape animations when written by a model and previewed; round-trips through EffectCraft (self tests only) [3] | Renderability, not syntax: in the OmniLottie CVPR 2026 supplement about 35% of failures were empty `layers`, the rest blank output from missing fills/strokes, timing outside the duration, and unit mismatches (opacity 0 to 100, so `o:1` is 1%); LLM baselines including Claude Sonnet 4.5 had cases with no renderable Lottie after five attempts (search result only) [32][33] | lottie-web `goToAndStop(frame,true)` in Playwright is frame-addressable and eased correctly (M15); lottie-web 5.13.0 (2025-05-21) | lottie-web MIT [16]; the PyPI `lottie` package is **AGPL-3.0+** (M, pypi licence field), so do not bundle it in anything you distribute [17] | **Not a carrying route.** Author in SVG/GSAP; use Lottie only as an interchange for small EffectCraft pieces, always validated in lottie-web |
| **Remotion** (React, TSX) | Full compositions where "a video is a function of images over time" [13]; official agent skills (`npx remotion skills add`), setup `npx create-video --yes --blank` [14] | Missing `from` offsets on `<Sequence>` (everything animates at frame 0), `durationInFrames` mismatches, linear `interpolate` with no easing [42]; "the bottleneck shifts from technical skill to taste" [41] | **Renderer-owned stepping**: headless Chrome, one screenshot per frame [42]. Measured: 150 simple 1080p frames in 21.8 s cold and 10.7 s warm (M13). `--gl` default `null` in 4.0, `angle` in 5.0, `swangle` recommended with no GPU "Rendering might be slow" [11]. PNG slower than JPEG; high resolution slower [12] | Free for "an individual" and up to 3-employee for-profits, non-profits, evaluators; Company License otherwise ($25 per seat per month "Creators", $100 per month minimum "Automators", Enterprise from $500 per month); "In Remotion 5.0, the license will slightly change" [9][10] | Solid, but equals Route A with a React build step and a licence that will change; **pin 4.0.x and set `--color-space=bt709 --pixel-format=yuv420p`** (default was `yuvj420p`, full range, `bt470bg`, M13) |
| **HyperFrames** (HeyGen; HTML) | Plain HTML with `data-start`, `data-duration`, `data-track-index`; GSAP/CSS/Lottie/three.js/Anime.js/WAAPI "adapters"; `npx hyperframes init/preview/render`; Claude Code plugin and skills install [22] | Not evidenced yet; the only blog I found is a feature tour with no production verdict [23] | **Renderer-owned stepping**: "seeks each frame in headless Chrome and encodes the result with FFmpeg"; same input gives same frames, golden baselines kept in Git LFS (about 240 MB) [22] | Apache-2.0, "no per-render fees or commercial-use thresholds" [22]; requires Node 22+ and FFmpeg | Closest off-the-shelf version of Route A. Pre-1.0 (0.8.169, 2026-10-17), 7 months old, page shows 66.1k stars (not independently verified). Evaluate in experiment E1; the repo-owned harness is the default |
| **Motion Canvas** | TypeScript generator scenes with an editor; PNG/JPEG/WebP image-sequence export; `@motion-canvas/ffmpeg` plugin exists [18][16] | Export is driven from the editor in a browser: "depends on the capabilities of your browser"; no headless route in its docs; animations "will not scale with changes in resolution" [18] | Image-sequence export from the editor UI (frame accuracy not guaranteed in docs) [18] | MIT; 19.4k stars; **last stable 2024-12-14, last alpha 2025-02-16** [16][19] | Skip: dormant and UI-driven |
| **Revideo** (Motion Canvas fork) | Headless `renderVideo()` "runs anywhere Node and a headless browser run"; React `<Player/>` [20] | Not evidenced; same generator style as Motion Canvas | Headless render of the project (frame-stepping method not stated on the page) [20] | MIT; 0.11.0 on 2026-07-10; counts renders anonymously via PostHog (disable with `DISABLE_TELEMETRY=true`); 4.1k stars [16][20] | Fallback if generator-style scenes are wanted; not tested |
| **Manim** | Maths explainers, Cairo-rendered | Wrong tool for photographs and warmth; install is heavy | Frame files via its own renderer | MIT, double-licensed with 3b1b LLC copyright; 0.22.0 on 2026-10-08, Python 3.11+ [17][21] | Skip. `pip install manim==0.22.0` failed here on Python 3.13: `manimpango` needs the `pangocairo` dev library (M18); apt route untested |
| **three.js / voxel scenes** | Lit meshes, instanced voxels, textured planes with depth displacement, camera rigs | Flat lighting, same camera drift on every shot, default materials | **Seek capture** with a `renderAt(t)` function: 400 lit cubes at 1080p with SwiftShader WebGL2 ran 3.2 to 3.5 fps and produced **hash-identical** frames in two runs (M9). `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist` | three r186.1 (2026-09-24), MIT [16] | Part of Route A (same harness). Good for voxel dioramas and photo planes; keep scenes light |
| **Blender via bpy** | Scene building, import of SVG curves and Grease Pencil, 2.5D parallax planes, voxel dioramas, warm path-traced stills (recipes in [6]) | Over-bright default lighting, AgX desaturation unless `view_transform='Standard'` [6], over-tidy camera moves; API drift between versions [6] | Deterministic per frame; 1080p per frame on 4 vCPU: **Workbench 0.8 s, Cycles CPU (24 spp, denoise) 17.5 s, EEVEE on software GL 34 s** for Suzanne plus a sun (M14) | bpy 5.2.2 (PyPI, 2026-09-15, cp313 only, 402 MB wheel) [17]; Blender: GPL-2.0-or-later source, GPL-3.0-or-later binaries, renders are the maker's own [83] | Third route for hero shots; shard into 10-minute jobs or use a rented GPU hour |
| **ffmpeg + ImageMagick (+ Pillow/numpy)** | Conform, per-frame transforms, Ken Burns, grain, grades, dissolves (`xfade`), loudness (`loudnorm`, `ebur128`), all encodes; ImageMagick `-morph` | Stock moves: identical `zoompan` on every photo; ffmpeg's `noise` filter bloats files (M6) | Deterministic by construction | ffmpeg 6.1.1 (libx264, libx265, svtav1, prores_ks, ffv1, libvpx), ImageMagick 6.9.12 with `convert` only (M2) | **Route B.** The substrate every shot passes through |
| **Craft CLIs** (`effectcraft-cli render`, `filmcraft-cli`, `photocraft-cli batch/serve`) | See Q10 and [3][4] | Alpha software; see risks | CPU by default; frame stepping inside the app engine | EffectCraft's repo carries `LICENSE-APACHE` and `LICENSE-MIT` [68]; the other repos were not re-read here | Optional render engine pending the spike; always with an ffmpeg/code fallback |

**Which two routes carry the vertical slice, and why.**

| Criterion | A: seekable web scene | B: photo-motion + finishing chain | Remotion | Blender | Craft CLIs |
|---|---|---|---|---|---|
| Deterministic frames, measured | Yes, hash-identical (M9, M10) except heavy SVG filters (tiny diffs) | Yes (ffmpeg, ImageMagick) | Yes by design; not re-tested for identity | Yes | Test T4 |
| Speed on 4 vCPU, measured | 12.9 fps flat SVG, 3.3 fps heavy 3D | 47 fps encode; 7.8 fps per-frame photo move in Pillow (M21), about 20 fps with 3 to 4 processes (ESTIMATE) | 14 fps simple | 0.04 to 1.25 fps | Unmeasured |
| Hand-made look controllable | High: seeded strokes, custom eases, textures, own type | High for photographs: per-shot parameters, grain on twos, paper wobble | Same as A | High (lighting), slow to iterate | Medium |
| Maker can refine it | SVG in VectorCraft, ORA in PhotoCraft, OTIO in FilmCraft | OTIO and stills in FilmCraft | Hard (React code) | Hard (Blender is not one of the Craft apps) | Native |
| Licence and lock-in | Vendored MIT/"no charge" files | Open tools | Changes at 5.0 | GPL tool | Alpha |

So **A and B**. A produces everything drawn, lettered or constructed; B carries every real photograph and the final grade, so the real photos are never pulled through a framework that did not need them. Blender covers shots where real 3D light matters; three.js is the cheap 3D inside A.

**What the agent gets right versus what needs the maker's eye (J, backed by [37][41][43]).** Right: plumbing and consistency (ids, sizes, frame counts, colour tags, loudness), timing arithmetic and sync to word timestamps, repetition across 100 shots, variation of parameters from a seed, self-checks by numeric audit. Maker's eye: whether a face is her, whether a hold is long enough to feel, whether a colour is the colour of that kitchen, whether a joke lands, and anything about sound ("a human must check smoothness and sound" [43]).

**The motion-graphics template risk and how each route avoids it.** The tells are uniform easing, stock transitions, lower-thirds grammar, beat-synced zooms, glow gradients on dark backgrounds, centred type with typewriter reveals, and the same Ken Burns on every photo. Avoidance is procedural: (1) a per-shot parameter generator (seeded) that varies direction, duration, ease family, hold length and drift, so no two photos move alike; (2) a look-lock on three style frames before any motion is built; (3) a template-risk lint in the validators (R8): flag identical ease strings above a threshold, evenly spaced delays, uniform stagger, transitions of one type, zoom-in on every photo; (4) the maker's blind A/B between the generated draft and a hand-adjusted one at gate G2.

**Frame-accuracy ladder (what counts as production).**
1. Pure `seekTo(t)` or `renderAt(t)` plus screenshot: production (M9, M10).
2. Renderer-owned stepping (Remotion, HyperFrames): production.
3. Playwright `page.clock.install()` then `runFor(1000/fps)`: `Date`, timers and rAF are faked [30] and rAF timestamps were identical across runs, but `performance.now()` drifted (26, 34, 50, 65 ms for what should be 16 ms steps) (M11): use only for code that never reads `performance.now()`.
4. Free-running rAF plus screenshot: not deterministic (M11).
5. `recordVideo` or screen capture: size defaults to the viewport scaled to fit 800x800 and the page states no frame rate or quality guarantee [31]; prototyping only.

### Q2. How do we get a hand-crafted look out of code? Techniques, with sources and licences, and the anti-patterns

| Technique | How, concretely | Source and licence | Cost (measured) |
|---|---|---|---|
| **Seeded sketchy strokes and fills** | rough.js `roughness` (default 1), `bowing` (default 1), `fillStyle` (hachure, solid, zigzag, cross-hatch, dots, dashed, zigzag-line), `strokeWidth`, `disableMultiStroke`, `preserveVertices`; **set `seed` to a nonzero number per shape id** so the wobble is the same every render ("If seed is not defined, or set to 0, no seed is used") | rough.js MIT, SVG and canvas modes [24][25] | 120 hachure rects: 12.9 fps (M10) |
| **Imperfect easing** | GSAP `RoughEase` (`strength` 0.1 stays near the template ease, `taper`, `clamp`, `randomize:false` for even zig-zag), custom per-element ease curves, durations drawn from a seeded distribution; asymmetric curves (slow settle, quick start) | GSAP "no charge" licence includes all plugins [15][26] | negligible |
| **Anticipation, overshoot, settle; offset parts in time** | Eyes lead, body follows, props drag and settle last; "a raw lerp over time is a bug"; exaggerate ("subtle reads as nothing at 24 fps in a 3-second shot"); avoid twinning (give crowds different phases, seeds, variants) | `CRAFT.md` in a working Claude Code film pipeline [37] | none |
| **Hold on twos; camera and type on ones** | Hold character drawings on twos (12 drawings per second at 24 fps), keep camera and type on ones; line boil by swapping 2 to 5 slightly different drawings (squigglevision, Tom Snyder, a loop of five similar drawings) | [37]; line boil background from tutorials, search result only [34]; in-project recipe T4 in [8] | none |
| **Baked grain and paper on twos** | Pre-render 8 grain frames (`convert -size 1920x1080 xc:gray50 -seed N +noise Gaussian -attenuate 0.6 -colorspace Gray`), loop at 12 fps, `blend=all_mode=overlay:all_opacity=0.35` in ffmpeg | ImageMagick, ffmpeg | 10 s at 24 fps: 9.5 s and 10.6 MB, against 32.7 s and 160 MB for the `noise` filter (M6) |
| **Real scanned textures** | Paper, card, album pages, tape, torn edges from ambientCG (CC0: "You don't need to give credit", commercial and personal use allowed) [28]; far better, **scan the backs and borders of her own photos** (stamps, pencil notes, deckle edges: see the "always scan the backs" rule in [2]) | ambientCG CC0 [28] | image decode only |
| **Wobble that does not cost a filter** | Displace path points in JS with seeded noise at build time; if an SVG filter is unavoidable, apply `feTurbulence`+`feDisplacementMap` to a small region (MDN: `seed`, `baseFrequency`, `numOctaves`, `type`) [27] | MDN | wobble filter on the whole art group: 5.7 fps against 12.9 fps (M10) |
| **Hand-lettering fonts** | Self-hosted Google families via `@fontsource/*`: Caveat, Kalam, Reenie Beanie, Gaegu, Patrick Hand, Shadows Into Light (all OFL-1.1), Homemade Apple, Rock Salt, Special Elite (Apache-2.0) [16]. OFL FAQ: video titling is explicitly welcome; the artwork you make is not restricted; attribution is not required for artwork; you may not sell the font by itself; redistributing the font needs its notice and licence [29]. Self-host so the render never depends on a CDN | npm registry licence fields; OFL FAQ 1.1-update7 [16][29] | none |
| **Her handwriting as the typeface** | Scan letters, recipe cards and shopping lists; trace glyphs to SVG paths (Inkscape trace or potrace); keep three variants per letter and pick by seed so repeated letters differ; fonttools (MIT, 4.67.0) can build a font file if wanted [17]. The most personal "font" the project can have, and licence-clean because it is hers (J). **Ethics (Principle 4): use it only for words she actually wrote, or label new text as set in a typeface made from her handwriting; typing new sentences in her hand would put words in her mouth** | (J) | build once |
| **Limited palette** | 4 to 6 colours sampled from the fade of her print stocks (Kodak orange, Agfa green), recorded as palette ids in the style frame and enforced by the lint; era grades as ffmpeg chains (R7 in [6]) | [6] | negligible |
| **Deliberate asymmetry** | Off-centre composition, uneven margins, one element late, one slightly crooked, from the seed; never mirrored crowds | [37] | none |
| **Real photo as the material** | Photos as paper prints placed on a table (slight rotation, drop shadow, tape), edges torn or scalloped; "paper-print wobble on twos" for reconstructions (recipe C3 in [8]) | [8] | Route A |

**Anti-patterns that read as a template (flag in the lint and at gate G2).** Uniform easing or one spring config everywhere; evenly spaced stagger; one stock transition type (whip, glitch, zoom blur); lower-thirds grammar for people (name on a bar) outside the credits; zoom punch-ins synced to a beat or used "where nothing happens" [37]; the same slow zoom-in on every photo; centred type with constant-speed typewriter reveals; neon-on-dark gradients; looping or stretching an action to fill a slot ("Never loop, repeat or stretch an action, or its sounds, to fill a slot" [37]); perfect symmetry and pixel-perfect alignment everywhere (J).

**Process controls that matter more than any technique.**
- **Look-lock before motion.** The same pipeline sequence that produced the best examples was storyboard, then a full-length slate animatic, then section builds, then review passes [36]. For us: three style frames approved by the maker, then a 10-second look test, then the shot.
- **A shared craft guide.** Five parallel Claude subagents built sections "against one craft guide" [36]. Ours: `playbooks/craft.md` distilled from [37] plus the rules above, loaded by every implementer.
- **Numeric pacing audit and pop scan** before any draft goes to review (`tools/edit_audit.py` in [37]); "Treat any AI critic as a noisy sensor: shuffle, anonymise, repeat, and aggregate. Verify each claim at full resolution" [37]. A critic that "never saw the build" found 10 issues in round 1 and still 2 major ones in round 3; it "reviews stills only", so "a human must check smoothness and sound" [43].

### Q3. What does the container offer, what breaks at scale, and where does each stage run?

**Measurements (first-hand, this session, 2026-10-18; synthetic inputs only) [67].** Official ceilings for comparison: "approximate resource ceilings that may change: 4 vCPUs, 16 GB of RAM, 30 GB of disk"; each session gets a fresh Ubuntu 24.04 x86_64 VM; idle sessions pause after a few minutes with files saved and the VM can later be reclaimed; Bash foreground default 2 minutes, up to 10, then moved to the background; setup scripts that finish in about five minutes are cached for about seven days [49][50].

| ID | What | Result |
|---|---|---|
| M1 | Hardware and OS | 4 vCPU Intel Xeon 2.10 GHz; 16.1 GB RAM, no swap; Ubuntu 24.04.5, kernel 6.18.44; `df`: 252 GB device, 12 GB used and 28 GB free at start, 16 GB used and 24 GB free after installing bpy, Remotion and the probes; no `nvidia-smi`; Claude Code 2.1.302; Python 3.13.16; Node 22.22.0; git 2.43 and git-lfs 3.4.1; `gh` |
| M2 | Media tools | ffmpeg 6.1.1-3ubuntu5 with libx264, libx265, libsvtav1, libaom, `prores_ks`, ffv1, libvpx (NVENC, QSV, VAAPI encoders are compiled in but there is no hardware); filters `sidechaincompress`, `loudnorm`, `ebur128`, `arnndn`, `afftdn`, `xfade`, `zoompan`, `minterpolate`. ImageMagick 6.9.12-98 Q16 (`convert` only, no `magick`); policy limits memory 1 GiB, map 2 GiB, disk 2 GiB, area 256 MP, width and height 32 KP. Also present: `rsvg-convert`, Inkscape, `melt`, Pillow 12.3.0, numpy 2.5.3, 103 system font entries (DejaVu, FreeSans, Inter; no handwriting faces). Absent: ExifTool, OpenCV, Blender, OTIO, svgo until installed |
| M3 | Browser | Playwright 1.56.1 (global, `/opt/node-tools`) with Chromium 141.0.7390.37 and a headless shell prebuilt in `/opt/pw-browsers` (`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`); launch 0.49 s; WebGL2 works through ANGLE on SwiftShader (Vulkan 1.3.0 SwiftShader Device); `cdn.playwright.dev` answered HTTP 400 from here, so pin Playwright 1.56.x to match the preinstalled browser build (UNVERIFIED whether the CDN is blocked) |
| M4 | x264, 1080p30, 10 s, `-crf 18 -preset medium` | 6.4 s (47 fps); 12.1 MB |
| M5 | ProRes 422 HQ (`prores_ks -profile:v 3`, 1080p30, 10 s) | 15.6 s (19 fps); 97.8 MB (about 78 Mbit/s on this test pattern, so about 5.9 GB per 10 minutes; content-dependent) |
| M6 | Grain | x264 with `gblur=sigma=2,noise=alls=12:allf=t,vignette`: 42.2 s per 10 s (7 fps), 165 MB. ffmpeg `noise=alls=10:allf=t` alone at 24 fps: 32.7 s, 160 MB. Looped 8-frame pre-rendered grain overlay at 12 fps, `blend=overlay` 0.35: 9.5 s, 10.6 MB. Plain 24 fps reference: 4.1 s, 10.4 MB. (Visual strength of the overlay was not judged.) |
| M7 | ImageMagick on 3600x2400 16-bit TIFF (51.8 MB each) | to 1080p cover JPEG q92: 0.26 s each serially (20 files in 5.2 s), 0.16 s each with `xargs -P4` (3.1 s); `-morph 23` between two 1080p PNGs: 17.7 s for 25 frames |
| M8 | Chromium screenshots of a 1080p canvas | PNG 9.9 fps; JPEG q95 12.4 fps |
| M9 | three.js r186.1, 400 lit cubes, MSAA, 1080p, SwiftShader, `renderAt(t)` seek | 3.2 and 3.5 fps (two runs of 30 frames); the two runs' 30 frame hashes were identical and all 30 distinct |
| M10 | SVG: 120 rough.js hachure rectangles with ids, GSAP 3.15.0 paused timeline, `tl.time(t,false)` seek, 1080p | no filters 12.9 fps; `feTurbulence`+`feDisplacementMap` wobble on the art group 5.7 fps; full-frame `feTurbulence` grain 1.2 fps; both about 1.0 fps. Re-runs hash-identical in the three single-filter variants; with both filters, 5 of 36 frames differed between two passes by 12 to 80 pixels out of 2,073,600. PNG frames of this textured scene were 2.0 to 2.3 MB each (flat scenes: 14 to 165 KB) |
| M11 | `page.clock.install()` plus `runFor(1000/30)`, rAF logging | rAF timestamps 16, 32, 48, 64 ... identical across runs; `performance.now()` read 26, 34, 50, 65, 83, 96, 114, 128 (not faked); free-running rAF differs between runs |
| M12 | Transparent capture and encodes | `page.screenshot({omitBackground:true})` gave RGBA PNG (`srgba`, not opaque); 48 frames at 1080p in 3.9 s (12 fps); `prores_ks -profile:v 4444 -pix_fmt yuva444p10le` reported by ffprobe as `yuva444p12le`, 10.7 MB for 48 mostly transparent frames; H.264 with `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` verified by ffprobe. **Status: tags verified; matrix not verified; corrected 2026-10-18.** The bare `-pix_fmt yuva444p10le` encode gave BT.601 pixels under BT.709 tags on ffmpeg 6.1.1 (10-bit Y 326 for pure red, against 250; review round 1, section 1.1, reproduced in Q-F1). The matrix is now measured in M23 (Q-F1) |
| M13 | Remotion 4.0.536 (install 14 s, 464 MB of `node_modules`), 150-frame 1080p30 composition, container's headless shell via `Config.setBrowserExecutable` | 21.8 s cold (7 fps), 10.7 s warm (14 fps). Default output `yuvj420p`, `color_range=pc`, `color_space=bt470bg`; with `--color-space=bt709 --pixel-format=yuv420p`: `yuv420p`, `tv`, `bt709` |
| M14 | bpy 5.2.2 (cp313 wheel 402 MB, venv 1.0 GB), Suzanne plus a sun, 1080p, per frame (4 frames each) | Workbench 0.72 to 1.16 s; Cycles CPU 24 spp with denoise 17.4 to 19.0 s; EEVEE (software GL, `EGL_BAD_MATCH` warnings printed, output non-blank) 34.1 to 35.8 s. At 960x540: Workbench 0.4 s, Cycles 4.7 s, EEVEE 24.8 s for the first frame |
| M15 | lottie-web 5.13.0 in Playwright | `goToAndStop(frame,true)` at frames 0, 15, 30, 45, 59 gave x = 60, 79.2, 245.1, 328.7, 340 for a Bezier-eased test layer |
| M16 | OpenTimelineIO 0.18.1 (pip, Python 3.13) | write, read back, two clips plus a dissolve = 10:00 at 24 fps; `otiocat`, `otioconvert`, `otiostat`, `otiotool` installed |
| M17 | svgo 4.1.0 and @resvg/resvg-js 2.6.2 | svgo's default preset removed **every** `id` (kept `data-pivot`); with `cleanupIds:false` and `removeUnknownsAndDefaults:{keepDataAttrs:true}` all ids survived; resvg-js rendered a PNG |
| M18 | `pip install manim==0.22.0` on Python 3.13 | failed building `manimpango` 0.7.0: `pangocairo >= 1.30.0` not found; an apt install of the Pango/Cairo dev packages would be needed (untested) |
| M19 | Egress from this session (HTTP status only, no keys sent) | npm 200, PyPI 200, download.blender.org 200, `generativelanguage.googleapis.com` 404 (reachable), `api.replicate.com` 200, `fal.run` 404 (reachable), huggingface.co 200, `api.bfl.ai` 302, `api.lumalabs.ai` 200, `api.openai.com` 421, ambientcg.com 200, polyhaven.com 200, unpkg.com 200. This describes this session's network level only; each environment is set to None, Trusted, Full or Custom by the maker [49] |
| M20 | Claude Code process | about 759 MB resident after about 2 hours in this long session (Linux container) |
| M21 | Route B per-frame photo move: Pillow `Image.transform` (affine, bicubic) from a pre-conformed 2880x1620 still to 1920x1080, with an eased scale, drift and 0.6 degree wobble | 7.8 fps single process; 6.6 fps when piping raw frames to x264. ESTIMATE: about 20 fps with 3 to 4 processes, one shot each |

**What breaks at scale.**
- **Hundreds of 3600x2400 TIFFs.** Compute is not the problem (about 80 s to conform 300 serially, M7). Space and privacy are: 300 x 51.8 MB = 15.5 GB of 16-bit TIFF would fill most of the 24 to 28 GB disk and each cloud session starts from a fresh VM. Rule from [4]: scripts travel to the PC, scans never go to the cloud. Conform on the PC (R1 in [3]), keep masters on the encrypted drive, and only if the maker sets `cloud: preview` send 768 px JPEG proxies (about 100 KB each, ESTIMATE) so the agent can art-direct. ImageMagick 6's policy file caps pixel memory at 1 GiB and disk at 2 GiB: set `-limit` explicitly for montages.
- **A 10-minute 1080p render.** 14,400 frames at 24 fps. Texture-rich PNG frames of about 2 MB are about 29 GB (M10): more than the disk. Stream frames to ffmpeg (`image2pipe` for browser captures, `rawvideo` for Pillow, as in M21) or encode per 10-second chunk and delete frames; keep only the chunk encodes. A ProRes 422 HQ master of 10 minutes is about 5.9 GB on this test pattern (M5); an H.264 CRF 18 access copy about 0.7 GB (M4).
- **Idle pause and reclaim.** "After a few minutes without activity, a session's VM pauses with its files saved"; a reclaimed VM is rebuilt and "background work that was still running" is not restored [49][50]. Whether a running background job keeps the VM awake is UNVERIFIED (spike S4). Design for it: every render is sharded into jobs of 10 minutes or less, writes frames or chunks to disk, is resumable (skip frames that exist), and the agent polls with a monitor instead of sleeping.
- **Browser memory.** Loading 300 photos at 2880x1620 as WebGL textures is 5.6 GB (300 x 18.7 MB, ESTIMATE): load per shot, dispose after.
- **Chromium and the GPU.** No GPU; WebGL is SwiftShader (M3). Complex shaders and full-frame filters are the slow path (M10).
- **Process count.** 4 vCPUs: one Chromium with SwiftShader already uses several threads; run Route B shots in parallel processes, run Route A captures one or two at a time (J; measure in S2).

**Recommended split (where each stage runs).**

| Stage | Runs where | Why |
|---|---|---|
| Scan, LightCraft batch, conform, manifest checksums | Maker's PC | 16-bit masters stay local; 15.5 GB; privacy [4] |
| Restoration and upscale | PC GPU if present, else cleared photos via paid-tier API, else manual | Terms and tiers in [2] |
| Look-dev style frames, SVG art, shot scenes (Route A), shot scripts | Cloud container | CPU-only, deterministic, text-driven |
| Photo motion, grain, grade, dissolves, encodes (Route B) | Container for cleared proxies and synthetic stand-ins; **PC for real full-resolution photos** (the same scripts, run by the maker or a local agent) | The scripts are text, the photos are not |
| Hero 3D shots (Blender) | Container in 10-minute shards, or a rented GPU hour (RTX 4090 $0.34 to $0.89 per hour on RunPod per [2]) | Cycles 17.5 s per 1080p frame on 4 vCPU (M14) |
| Raster paint-over, SVG touch-up, title templates, timeline polishing | Maker's PC in the Craft apps | The refinement layer [3][4] |
| `effectcraft-cli render` of titles | Container if spike S1 passes, else the PC | CPU, memory-capped with `RAYON_NUM_THREADS=2` [3] |
| Assembly, master, access copies | OTIO opened in FilmCraft on the PC; `filmcraft-cli` in the container only after S1; ffmpeg produces every H.264 | ProRes then x264 [3] |
| Validation | Both: the same validators in the container and a Windows script on the PC | Q5 |
| Backup | PC (rclone crypt, second drive) | Media never lives in the repo [5] |

**Rough time and cost per 100-second chapter (2,400 frames at 24 fps; ESTIMATE from M4 to M21).**

| Item | Container compute | Maker time | Cash |
|---|---|---|---|
| Route A frames, flat SVG/DOM (about 40% of the chapter, 960 frames) | 960 / 12.9 fps = 1.2 min | review 10 min | $0 |
| Route A frames with a wobble filter | 960 / 5.7 fps = 2.8 min | | $0 |
| Route A frames with full-frame grain filter (avoid) | 960 / 1.2 fps = 13 min | | $0 |
| Three.js 3D, 480 frames (20 s) at 3.3 fps | 2.4 min | | $0 |
| Route B photo moves, 1,200 frames at 7.8 fps | 2.6 min single process, about 1 min with 3 to 4 | contact-sheet review 10 min | $0 |
| Baked grain plus x264 for 2,400 frames | about 1.6 min (9.5 s per 240 frames) | | $0 |
| ProRes 422 HQ intermediate for 2,400 frames | 2.1 min | | $0 |
| Blender hero shots, 2 x 10 s = 480 frames: Workbench / Cycles 24 spp / EEVEE software | 6 min / 2.3 h / 4.5 h in shards | look-dev 30 to 60 min | $0 in the container; about $0.05 to $0.40 on a rented GPU if Cycles on GPU takes 1 to 3 s per frame (ESTIMATE, UNVERIFIED) |
| Gemini image and Veo calls (Q4) for the chapter (about 50 images, 5 clips) | | | about $3 to $40 |
| FilmCraft assembly and export on the PC (4 cores, no NVIDIA) | H.264 at 4 to 16 fps (ESTIMATE from vendor numbers in [3]) = 2.5 to 10 min; ProRes at about 5 to 6 fps = 7 to 8 min | 30 to 60 min for the chapter pass | $0 |
| Total without Blender | about 10 to 15 min of container compute (the full-frame grain filter alone would add 13 min) | about 4.5 to 5.5 h of maker time per chapter including the chapter pass (Q7) | $3 to $40 |

The container itself has "no separate charge for the cloud VM" but counts toward plan usage limits [50]; how much of a Pro or Max allowance a day of iteration consumes is UNVERIFIED. The evidence from an unattended 22-agent run is a warning: $207.58 at API prices for about 8 hours and a 90 s film [38]. Do not run unattended multi-agent studios on this project.

### Q4. Generation services an agent can call from the container (delta to `ai-imagery.md`)

Reused unchanged from [2]: the verified privacy table (Gemini API paid tier acceptable for selected photos; unpaid tier and consumer app not; Luma never; Replicate API predictions deleted after an hour; OpenAI, Runway, Kling, Midjourney UNVERIFIED so "no"), the label ladder, the rule "if it looks like a photograph, it is a photograph", and the hardware-tier table for local models. What follows is only new.

| Item | Delta (dated) |
|---|---|
| **Google pricing page, updated 2026-10-16** [65] | Image prices per image (Standard / Batch): Nano Banana 2.1 `gemini-nano-banana-2.1` $0.0336 / $0.0168 at 1K, $0.0504 / $0.0252 at 2K, $0.113 / $0.0567 at 4K; Gemini 3.1 Flash Image (Nano Banana 2) $0.067 / $0.034 at 1K; Gemini 3 Pro Image (Nano Banana Pro) $0.134 / $0.067 at 1K and 2K, $0.24 / $0.12 at 4K. "Gemini 2.5 Flash Image is deprecated and will be shut down on October 2, 2026" (already past; matches [2]). Paid tier lists the Batch API as "a 50% cost reduction". Veo 3.1 per second with audio: Standard $0.40 (720p and 1080p), Fast $0.10 (720p) and $0.12 (1080p), Lite $0.05 (720p) and $0.08 (1080p); charged only on success. Free tier content "is used to improve Google's products"; paid tier content is not. **The page announces changes on 2026-12-01 and 2027-01-01**: Gemini 4 Argon (2026-12-01), and Gemini 3.8 and 3.6 Flash, the 3.8 TTS models and Robotics ER 2 (2027-01-01). It names **no image or video model** among them (checked in the round-1 review; this corrects the earlier "many paid prices increase" wording). No date is forced: re-read the page in the week the batch runs |
| **Batch cost, about 300 images** | Nano Banana 2.1 at 1K: 300 x $0.0336 = $10.08 standard or $5.04 batch; with 3 takes per kept image: $30.24 or $15.12. Nano Banana Pro at 1K: $40.20 or $20.10; with 3 takes: $120.60 or $60.30 (ESTIMATE, plus margin). Batch jobs return asynchronously, which suits the pause-and-reclaim container: submit, record job ids in the repo, collect later (J) |
| **Batch cost, about 30 short clips (5 s each, 150 s)** | Lite 720p $7.50; Fast 720p $15.00; Fast 1080p $18.00; Standard $60.00. With 3 takes: $22.50, $45, $54, $180. Veo batch pricing was not stated on the page (UNVERIFIED). These agree with the $0.25 to $2.00 per 5-second clip in [2] |
| **Replicate** [66] | Per-second GPU rates: A100 80GB $0.0014 per s ($5.04 per h), H100 $5.49 per h, L40S $3.51 per h, T4 $0.81 per h; per output: flux-1.1-pro $0.04 per image, flux-dev $0.025, flux-schnell $3.00 per 1,000; wan-2.1-i2v 480p $0.09 per s and 720p $0.25 per s. The page has no retention or privacy statement (see [2] for the one-hour API deletion). 300 images at flux-dev = $7.50; text-to-image models do not preserve likeness, so editing models (Kontext, Qwen-Image-Edit) are the ones that matter and their Replicate prices were not on this page (UNVERIFIED) |
| **Reachability and keys from the container** | Under the default **Trusted** level, `*.googleapis.com` is on the allowlist, so the Gemini API is reachable without changing anything [49]; other hosts need **Custom** or **Full**. This session could also reach Replicate, fal, Hugging Face, BFL and Luma (M19). Put the API key in the environment's **Network secrets** (Bearer header, bound to a host): the agent proxy attaches it to matching requests and the key "doesn't appear in the session's environment variables or in any file" [49]. Never paste a key into chat. Anyone who can use the environment can read its plain environment variables and setup script, so keys do not go there [49] |
| **Reference-image conditioning** | No change to [2]: use per-photo edit models (each photo supplies its own face) rather than one identity embedding across ages. New operational rule: a reference image that the agent can see in the session is subject to the `cloud` level in the manifest (R2) and to the Anthropic retention rules in Q8 |
| **What could run locally on the maker's GPU** | Unknown until the maker runs `nvidia-smi` or `dxdiag` and pastes the output into `maker-pc.json` (Open question 1). Then use the tier table in [2]. A local Claude Code session (Q8) or the maker's own scripts can call a local ComfyUI at `127.0.0.1` so real photos never reach the cloud (J) |
| **Not an agent route** | HyperFrames' hosted "upload your project ZIP" page and any "memorial video maker" service (HeyGen, Pollo and others appear in search results) take family photos to a third party; treat as "no" like the UNVERIFIED rows in [2] |

### Q5. Hand-off formats both ways, and the validators the agent runs before hand-off

Fixed project settings first (decide once in week 1, then never per shot): sequence 1920x1080 (the format track assumes a 1080p film [7]), one frame rate for the whole film (24, 25 or 30; default 24 so that "hold on twos" is 12 drawings per second), colour Rec. 709 / sRGB, audio 48 kHz 24-bit. The timeline spec stores seconds and ticks, so changing the rate later is a re-emit, not a rewrite.

| From to | Exact format | Colour, alpha, rate, naming | Validator the agent runs (container) and the PC-side check |
|---|---|---|---|
| **Agent to PhotoCraft** | OpenRaster `.ora`: zip of PNG layers plus `stack.xml`; layer names are the pipeline ids (`L10_sky`); opacity and `composite-op` set; offsets allowed; no adjustment layers, layer styles, live text or non-sRGB profile [4] | 8-bit sRGB RGBA PNG layers, straight alpha; canvas = shot size; name `LJ-C01-S014_<scene>.ora` | `validate_ora.py` (R8): opens as zip, `stack.xml` parses, every `src` exists, sizes within canvas, names unique and match the id regex. PC: `photocraft-cli info file.ora --compact`; the vendor-recorded third-party check is Krita 5.2.9 (32 of 35 files within 3/255) [4]. PSD is a fallback input only; PhotoCraft's PSD output "not always accepted by Photoshop" [4] |
| **PhotoCraft to pipeline** | The maker's `.ora` (or `.psd` when adjustment layers force it) stays private; exports are a flattened PNG and per-layer PNGs via `doc.exportLayers` plus the layer-tree JSON [4] | 8 or 16-bit sRGB; straight alpha PNG; `LJ-C01-S014_<scene>_v003.png` | `identify -format '%[channels] %[depth] %wx%h'` equals expectation; `photocraft-cli info --compact` JSON stored in the manifest; id regex on layer names |
| **Agent to VectorCraft** | SVG with unique ids `[A-Za-z][A-Za-z0-9._-]*`, `data-pivot` and `data-z` on groups and shapes, `viewBox="0 0 W H"`, no reliance on `class`, `<style>`, group `transform` or SMIL/CSS animation [4] | SVG user units = pixels of the shot canvas; fonts as outlines for final art | svgo only as a lint with `cleanupIds:false` (default preset strips all ids, M17); resvg render is non-blank; `vectorcraft-cli convert a.svg a.rt.svg` then `check_ids.py a.svg a.rt.svg` exits 0 [4] |
| **VectorCraft to pipeline** | SVG saved with Styling = Presentation Attributes, Object IDs = Layer Names, Fonts = SVG or outlines, Images = Embed, Decimals 3, Responsive off [4] | Same ids; classes and `<style>` are re-injected after the touch-up by id | `check_ids.py original touched` gates the hand-back; diff against the agent source; then GSAP is re-attached by id and `data-*` |
| **Agent to EffectCraft** | Static SVG subset (paths, basic shapes, groups, `use`, CSS `<style>`, gradients, strokes and dashes; text, images, filters, clipPaths, masks, patterns, markers and animation are ignored; ids become shape-group names) [3]; PNG stills; PNG/TIFF/EXR sequences (imported as one item) [3]; `.ectemplate` plus `values.json` for titles [68]; Lottie only as a self round trip | 8-bit sRGB; sequence names `name_[#####].png` | `effectcraft-cli info --json`; `render-frame --transparent` of frame 0 compared with a resvg render within tolerance; for templates, `render --template T.ectemplate --values V.json --out 'title_[#####].png'` fails fast on unknown controls [68] |
| **EffectCraft to pipeline** | RGBA PNG sequence (`--format png --channels rgba`), or ProRes 4444 (`--format prores --prores 4444 --channels rgba`), or WebM VP9 alpha; "both read back as straight alpha" [68] | Frame rate = project rate; zero-padded names | ffprobe `pix_fmt` (`yuva444p12le` expected for ProRes 4444, M12). Colour tags are not evidence: EffectCraft's open issue #340 says ProRes 4444 is "tagged bt709 but sRGB-encoded" (`research/craft-motion.md`, exports section). Consequence: prefer the RGBA PNG sequence; use ProRes 4444 only after the colour-patch test (R8) passes on that file. Frame count = duration x fps; ImageMagick reports alpha; the MP4 has a `moov` atom (an OOM-killed render leaves an unplayable MP4, issue #1615 [3]); two renders of an expression comp are identical |
| **Route A capture to editing** | PNG frames with `omitBackground:true` encoded to ProRes 4444 for overlays; opaque scenes to ProRes 422 HQ or H.264 | ProRes 4444 for overlays: `-vf "scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v prores_ks -profile:v 4444` (Q-F1; the bare `-pix_fmt` encode of M12 gave BT.601 pixels on ffmpeg 6.1.1). H.264: `-vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v libx264 -crf 18 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` (Q-F1: scale first; format first measured 5/255 RGB error, scale first 1/255); name `LJ-C01-S014_v007_draft.mov` | `ffprobe -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,color_space,color_range,color_transfer,color_primaries`; colour-patch test (R8, "Colour matrix") on the pixels, not the tags; render hashes or an AE count with a small fuzz (never bit-exact when SVG filters are used, M10) |
| **Agent to FilmCraft** | Pre-conformed stills (orientation applied, 8-bit sRGB, sized to the sequence plus Ken Burns headroom: FilmCraft decodes whole files to 8-bit RGBA and reads neither EXIF orientation nor ICC [3]); an `.otio` with `metadata.filmcraft` for motion, opacity and gain, or a session built through `filmcraft-cli`; never a hand-written `.fcproj` [3]; video as H.264 8-bit 4:2:0 progressive or ProRes, constant frame rate [3]; image sequences only as encoded clips (OTIO `ImageSequenceReference` is read as one file path) [3] | Motion `scale` 100 = native pixels, so a 3600x2400 still in a 1080p sequence needs cover scale = max(W/w, H/h) x 100 = 53.3 or a pre-conform [3]; absolute `file:///C:/LifeJourney/...` paths on one fixed project root [3] | `opentimelineio` parse (M16) plus rules: every `target_url` exists, `source_range` inside `available_range`, rate equals project rate, dissolve offsets fit, markers present; ffprobe of every video input (`r_frame_rate` equals `avg_frame_rate`). PC: FilmCraft import report has no "not supported" for motion; that is test T3 in [3] |
| **FilmCraft to assembly** | Master: ProRes 422 HQ at sequence size and rate; interchange exports: OTIO, FCP7 XML for Resolve, FCPXML, EDL; the `.fcproj` is a private working file [3] | 48 kHz 24-bit PCM audio | `ffprobe` (codec, `yuv422p10le`, frame count equals sequence duration, `r_frame_rate`), `ffmpeg -v error -i master.mov -f null -` prints nothing, `ebur128` on audio, three frames compared with `filmcraft-cli render` frames [3] |
| **Premiere copy** | H.264 High, CRF 16 to 18, `yuv420p`, BT.709 tagged, `+faststart`; 1080p safety copy at CRF 20, `-profile:v high -level 4.1` [3] | | ffprobe; played on a TV at 3 m (format track plan) [7] |
| **Audio** | WAV 48 kHz 24-bit PCM, `-c:a pcm_s24le -ar 48000`; loudness by `ebur128` and two-pass `loudnorm`; do not import MP3 or AAC into SoundCraft [3] | | `ffprobe`, `ebur128`; the maker (or a relative) listens, because no agent has: the film-studio run "never listened to its audio" [38] |
| **Lottie** | JSON from EffectCraft or hand-built | opacity 0 to 100, scale percent | lottie-web in Playwright: load, `goToAndStop` at three frames, check non-blank and eased positions (M15); reject empty `layers` |

**Which layered and edit formats the craft tracks recommend, and what that changes here.**
- **Layered:** OpenRaster for agent to PhotoCraft (only layered format with a third-party check; stdlib-writable); PSD as a fallback input and a private save; `.pcraft` is PhotoCraft's own [4]. Change to the pipeline: the agent emits layers as separate transparent PNGs with a generator (`make_ora.py` in the craft-visual fixtures) and never relies on adjustment layers surviving a round trip.
- **Edit:** OTIO as the portable contract (the only format Kdenlive and Resolve both read), with `metadata.filmcraft` for motion; FCP7 XML as a second file for Resolve; the `.fcproj` regenerated through the CLI, never authored [3]. Change to the pipeline: the chapter's neutral timeline spec JSON and the OTIO emitter become first-class code in `pipeline/bin`; stills must be conformed first (the 53.3 percent trap); Route A and EffectCraft outputs reach the timeline as encoded clips; if the fallbacks must keep Ken Burns, bake the motion in Route B instead of relying on keyframes surviving.

### Q6. Git and media: quotas, alternatives, manifest, naming, versions, gates

**GitHub facts, read 2026-10-18.**
- Git LFS included quota: GitHub Free 10 GiB bandwidth and 10 GiB storage; Pro the same; Free for organizations the same; Team 250 GiB each; Enterprise Cloud 250 GiB each. Pre-paid data packs "have been removed"; overage is metered: bandwidth billed per GiB downloaded, storage on an hourly usage rate; with a $0 budget, Git LFS is blocked until the first of the next month; with no payment method, exceeding storage blocks new pushes (clone still works) and exceeding bandwidth disables LFS until next month [54].
- Rates: $0.07 per GiB-month storage and $0.0875 per GiB bandwidth, from GitHub's 2024-06-03 changelog for new Enterprise accounts and the 2023 community FAQ ("GitHub will discontinue selling data packs") [57][58]; the billing page itself gave no dollar figures and pointed to the pricing calculator [54]. Treat the rates as the likely rates for personal accounts (UNVERIFIED for a Free or Pro account). Some third-party pages still advertise the old "$5 per 50 GB" packs (search result only).
- Maximum LFS file size: Free 2 GB, Pro 2 GB, Team 4 GB, Enterprise Cloud 5 GB [55].
- Plain Git: warning above 50 MiB, block above 100 MiB, browser uploads at most 25 MiB, repositories ideally under 1 GB and "less than 5 GB is strongly recommended"; no hard repository cap stated; release assets have no total size limit but each file must stay under the LFS maximum [56].
- Our situation: each cloud session starts from a fresh clone [49][50], so any LFS object in the checkout is downloaded again per session and counts against the 10 GiB monthly bandwidth: 20 sessions pulling 500 MB of LFS content is 10 GiB (J). `claude --cloud` bundle uploads also leave out files managed by Git LFS [50]. The HyperFrames repo itself notes full clones need LFS or `GIT_LFS_SKIP_SMUDGE=1` for about 240 MB of golden videos [22]. Whether the container's GitHub proxy supports LFS transfers is UNVERIFIED.
- Decision: no LFS for family media (it is not in the repo at all, per [5]). Keep the repo plain Git, under about 200 MB (J), with fonts, textures and vendored libraries as small normal files (each well under 50 MiB).

**Alternatives for 20 to 200 GB of family media with encryption at rest and a second copy (all read 2026-10-18).**

| Option | What it is | Price / limits | Encryption | Notes for this project |
|---|---|---|---|---|
| **Encrypted external SSD** (primary) | A local drive holding masters, scans, audio, video and renders | One-off purchase; price not checked here (UNVERIFIED) | **VeraCrypt** 1.26.29 (2026-06-09): free open source, encrypts a whole drive or a container file, Windows, macOS, Linux [63]. **BitLocker** drive encryption needs Windows Pro, Enterprise or Education; Home's "device encryption" covers the OS and fixed drives only, "it doesn't encrypt external/USB drives" [61] | Check the maker's Windows edition first (Open question 1). Losing the recovery key or password loses everything: store it on paper at a place the family trusts |
| **rclone crypt to Backblaze B2** (second copy, off-site) | rclone wraps a bucket and encrypts contents (XSalsa20 with Poly1305) and, by default, file and directory names (AES-256 EME) | B2 "starts at $6.95 / TB / mo", free egress up to 3x stored data, $0.01 per GB beyond, first 10 GB free, no minimum duration; the page is undated and shows a 2024 footer. 200 GB is about $1.39 per month, about $6 over 19 weeks (ESTIMATE) [59][60] | Scrypt key derivation; a salt ("password2") is advised; file length and modification time are not encrypted; the crypt password in `rclone.conf` is only lightly obscured; no independent audit is mentioned on the page; "Changing the password makes previously encrypted data unreadable" [60] | Account in the maker's name; keep `rclone.conf` off shared devices. There is no `rclone` binary on PATH in this container (`/opt/rclone` holds only a `rclone-filestore` entry); the sync runs from the PC |
| **Cryptomator vault on any cloud or drive** | Client-side vault, contents and file names encrypted with AES-256 | Desktop "pay what you want"; mobile has a small fee (review text, not the vendor page) [62] | Site cites independent audits, no dates [62] | Friendlier for a non-technical maker than rclone; file-level, so incremental sync works |
| **Hetzner Storage Box** | SFTP, SCP, Samba, WebDAV, BorgBackup, Restic, rclone, rsync over SSH; locations Germany or Finland; unlimited traffic; 1, 5, 10, 20 TB plans | Monthly prices were blank on the fetched page (UNVERIFIED) [64] | Encrypt client-side with rclone crypt, Borg or Restic | European data location may matter to the family (J) |
| **A NAS** | A home server with disks | Not researched (UNVERIFIED) | | Overkill for 200 GB; a second encrypted SSD kept elsewhere is simpler |

Recommended default (J): primary = VeraCrypt volume (or BitLocker if Pro) on an external SSD; second copy = rclone crypt to B2 nightly via a PowerShell script the agent writes; third = a second SSD stored away from the PC. The 3-2-1 rule and the checksum habit come from [2][5]. For a surprise, create the cloud account and the bucket under the maker's own login and keep the sync off any shared family device.

**What goes where (media rule from review 00, made operational) [5].**

| Tier | Contents | Where | Agent sees it? |
|---|---|---|---|
| **M0 repo** | Text, code, playbooks, JSON/YAML manifests, briefs, reviews, fonts and textures with licence files, synthetic fixtures, vendored libraries | Private GitHub repo (plain Git) | Yes |
| **M1 private** | Originals, 16-bit scans, audio, video, renders, `.fcproj`, `.ora`, `.psd` | Encrypted drive plus encrypted second copy | No |
| **M2 preview** | Downscaled derivatives (768 px JPEG proxies, 480p previews), only for sets with `cloud: preview` | Maker uploads to the session or a private artifact when the shot needs it | Yes, for that session |
| **M3 process** | Full-resolution derivatives needed for a cloud job | Uploaded for the job, deleted after, only `cloud: full` | Yes, for that job |

**Manifest schema, naming, versions and pruning** are in Recipes R1 and R2. **Review gates live in the repo** as one Markdown file per gate under `reviews/<chapter>/` plus a `status` field in `chapter.json`, so the orchestrator can see what is blocked.

### Q7. The everyday loop: roles, brief, checklist, feedback, cadence

The procedure is in Recipes R4, the shot-brief template in R3, the Fable checklist in R5 and the comment-file format in R6. Findings that shaped them:

- **Roles.** Orchestrator plans and integrates; Sonnet implementers each own one shot or one asset class and write only inside their shot folder; Fable reviews at gates with the charter rubric (six scores, approve only when all are 4 or higher and nothing critical is open) [1]; Haiku scribes distil playbooks; the maker directs, refines and approves. A trusted close relative is the proxy for hard chapters (Principle 5) and reads every chapter at gate G5.
- **Parallel agents against one guide.** The best-documented pattern is five parallel subagents each building a section against a single craft guide, after an animatic exists [36]. Use that, not a free-form "studio" [38].
- **The critic.** A fresh-context reviewer that sees only stills, timestamped contact sheets of 8 frames, plus the brief, found timing defects early (empty frames for 1.5 s, text frozen too long) and missed smoothness and sound [43]. In the unsandboxed 22-agent run, none of 994 critic actions opened the director's records (the separation was one sentence in the prompt), and the Opus critics cost $22.88 of the session's $158.37 [38]. So: critic = Fable or a fresh Sonnet with the brief and rubric, repeated and aggregated, then a human check of motion and audio.
- **Feedback channel from Windows.** (1) A Markdown comment file per shot (R6) with timecoded notes. (2) An annotated screenshot (Win+Shift+S) saved next to it. (3) For Craft-app questions, the app's own `ui.screenshot` via the control channel or MCP bridge (PhotoCraft's `ui_screenshot`, VectorCraft's `ui_screenshot`, `window.<app>.screenshot()` in the web builds) [3][4]. (4) Moving files: the browser upload on GitHub accepts at most 25 MiB per file [56]; the Remote Control docs confirm image and file attachments from phone or browser into a local session [47]; whether claude.ai/code cloud sessions accept image attachments was not stated in the pages I read (UNVERIFIED, test in week 1). Only synthetic or cleared images go through any of these.
- **Realistic cadence for one maker with a job (ESTIMATE, J).** The format track budgets about 10 h per week and about 190 h to the deadline [7]. Weekdays: 3 sessions of 30 to 45 minutes (watch one contact sheet and one 20 to 40 s preview, write comments). Saturday or Sunday: one 3 to 4 hour block in the Craft apps on two or three hero shots. A 10-minute film has roughly 120 shots, about 20 per 100-second chapter: 60% parameterised photo moves (2 minutes of maker time each), 25% designed graphics (12 minutes), 10% hero shots (60 minutes), 5% titles (5 minutes). That is about 3.5 hours of per-shot maker time per chapter, plus 1 to 2 hours for the chapter pass: 4.5 to 5.5 hours per chapter and about 30 hours for six chapters, well inside the 190 hours of the format track (ESTIMATE).

### Q8. Control from Windows without the desktop app

**Three places the agent can run (docs read 2026-10-18).**

| | Cloud session in a browser | Claude Code CLI on the PC | Remote Control |
|---|---|---|---|
| What it is | A session on Anthropic's infrastructure, started at claude.ai/code, the mobile app, the Desktop app, or `claude --cloud`; "keeps running after you close your laptop" [50] | `claude` in PowerShell, CMD or WSL | claude.ai/code or the Claude app as a window into a **local** session: "Claude keeps running locally the entire time, so your code execution and filesystem access stay on your machine" [47] |
| Windows install | Nothing but a browser and a GitHub link | Native: `irm https://claude.ai/install.ps1 \| iex` (PowerShell), `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` (CMD), or `winget install Anthropic.ClaudeCode` (no auto-update); WSL: the Linux installer inside WSL. Requirements: Windows 10 1809+, 4 GB+ RAM. Git for Windows is optional (Bash tool); without it Claude Code uses PowerShell. **Sandboxing is not supported on native Windows** (WSL 2 supports it) [46] | Same CLI |
| Start command | | `claude` | `claude remote-control` (server mode: prints a session URL, spacebar toggles a QR code; flags `--name`, `--spawn same-dir/worktree/session`, `--capacity N` default 32, `-c/--continue`, `--session-id`); `claude --remote-control` or `--rc` (interactive session also reachable remotely); `/remote-control` or `/rc` inside a session [47] |
| Needs | Pro, Max, Team or Enterprise plan [50] | A login or API key | Pro, Max, Team or Enterprise via claude.ai login, **API keys not supported**, direct `api.anthropic.com` (no Bedrock, Vertex, Foundry, gateway); unavailable if `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` or `DISABLE_GROWTHBOOK` is set; outbound HTTPS only, no inbound ports [47] |
| Can do | Everything in the container: generation, rendering, repo work; results leave by Git push | Everything on the PC: read the maker's drive, run Craft CLIs, MCP bridges to running Craft apps | Same as the CLI, steered from a browser or phone: attach photos and files, approve permissions, `/compact`, `/model`, `/mcp reconnect` |
| Cannot do | Reach the maker's PC, loopback ports or local drives; keep a VM awake while idle (pauses after minutes, reclaimed later) [49][50] | Computer use (macOS only) | Run if the PC sleeps or the terminal closes; "one remote session per interactive process"; `/plugin` and `/resume` are local-only; **the Fable usage-credits consent prompt is not forwarded** and the turn can end if nobody answers at the terminal; server mode gives up after about 10 minutes offline and sessions can be brought back for about 4 hours [47] |
| Windows status | Works from any browser | Documented platform | No OS restriction in the page; Windows Hello is named for Trusted Devices; **not tested on Windows by us** (UNVERIFIED) [47] |
| Privacy | Transcript stored by Anthropic; retention below | Local transcripts in `~/.claude/projects/` for 30 days by default | While connected, the transcript is also stored on Anthropic servers to sync devices [51] |

**Memory footprint (the maker's constraint).** No official number for the CLI. Evidence: this Linux session's `claude` process was about 759 MB resident after about 2 hours (M20). GitHub issues report native `claude.exe` on Windows reaching 13.2 GB RSS (#24840, Feb 2026), growing from about 5 to 13.3 GB committed over four hours (#42169, Apr 2026), 21.7 GB with sub-agents and MCP servers (#32304), more than 22 GB idle on a 32 GB machine (#25545), and 50.4 GB (#33356, closed as fixed in 2.1.74 per the reporter) (search results only, not opened) [53]. The "uses too much memory" complaint about the **desktop app** has a different cause in a mid-2026 report: a Hyper-V VM (Vmmem, about 1.8 GB) started after Cowork or agent mode (search result only) [53]. So: the CLI is not guaranteed lighter than the desktop app; the cloud session in a browser tab is the lightest agent location (a tab's memory was not measured, UNVERIFIED). Mitigations: restart the local session at chapter boundaries, `/compact`, watch Task Manager during the first week, keep subagents in the cloud, never leave a local session running overnight without checking.

**CLI computer use is macOS-only.** "Computer use in the CLI is not available on Linux or Windows. On Windows, use computer use in Desktop instead", and it needs a Pro or Max plan, claude.ai login and an interactive session [48]. Implication: without the Desktop app, an agent on the maker's Windows PC **cannot click arbitrary GUIs**. Everything GUI-shaped must go through (a) the Craft apps' own control channels, (b) files, or (c) the maker's hands.

**Do the Craft apps' `--control` and MCP bridge give enough GUI control for "agent prepares, maker finishes"?** Yes for state and screenshots, and the loop does not need more.
- PhotoCraft: `photocraft --control PORT`, loopback only, first frame must be a 64-hex bearer token; `photocraft-cli mcp --bridge 127.0.0.1:PORT --control-token-file PATH --automation-read-root DIR --automation-write-root DIR`; tools include `command_run`, `doc_inspect`, `render_preview`, `doc_open`, `doc_save`, `ui_screenshot` [4].
- VectorCraft and LightCraft: `--control PORT`, loopback, **no authentication** ("enable it only while you use it"); `vectorcraft-cli mcp --connect 127.0.0.1:7979` forwards every call so the maker watches the artwork change; tools include `ui_inspect`, `ui_screenshot`, `pointer_gesture`, `press_key`, `open_panel` [4].
- FilmCraft and EffectCraft: `--control PORT` and `<app>-cli mcp --bridge PORT` / `--bridge PORT` on CLI commands; FilmCraft's MCP server has no folder confinement flags, EffectCraft's and SoundCraft's do; web builds expose `window.filmcraft` / `window.effectcraft` with `screenshot`, `execute`, `request` [3]. `lightcraft-cli snapshot` writes PNGs of the whole UI headlessly [4].
- Who can use it: a **local** Claude Code session on the PC (`claude mcp add --transport stdio photocraft -- "C:\Program Files\PhotoCraft\photocraft-cli.exe" mcp --bridge ...`; syntax `claude mcp add [options] <name> -- <command> [args...]` [52]), steered from a browser by Remote Control if wanted. A **cloud** session cannot reach it (loopback on another machine).
- What it does for the loop: open the file the agent prepared in the running app, read the layer tree, take screenshots for feedback, run engine commands the maker asks for. What the maker still does: paint, nudge, judge, save.
- Risk: any local process can drive a `--control` port without a token (all but PhotoCraft); start it per session and close it [3][4].

**Recommended default (J).** Agents live in cloud sessions; the maker uses a browser tab. The Windows PC carries **a script-drop**, not an agent: `lj.ps1` (R10) with `pull`, `check-tools`, `run-steps <file>`, `snapshot`, `validate`, `push-feedback`. Add a local Claude Code session with Remote Control only for chapters where live driving of a Craft app saves time, and watch its memory.

### Q9. Real examples of films or animations made with coding agents (all links were opened unless marked)

Weighting: these are short (18 s to 3:30), mostly self-reported, and promotional in several cases. None is a multi-minute, emotionally paced documentary, and none is a family tribute. Treat them as evidence about plumbing and review loops, not about whether the result moves a viewer.

| # | Case (link in Sources) | Tools | Length and time | Author's own verdict | Template feel |
|---|---|---|---|---|---|
| 1 | **bishpls/animation-pipeline**: OPEN ALL NIGHT (93 s, 1080p24, cut-paper riso), WORDS ARE FOSSILS (86 s vertical), HELLO, WORLD! (2:38), TO BE CONTINUED (3:30, in production), FRAME PERFECT (34 s) [36][37] | Claude Code with a `make-film` skill; frames drawn by JavaScript as pure functions of time; WebGL riso shader (overprint, halftone, misregistration, mottling, paper grain); headless Chrome, parallel and resumable; ffmpeg; ElevenLabs Music and TTS with word timestamps; Gemini as media critic; Seedance only for two cut-ins in the third film | Render about 25 s on an M2 Pro with 6 workers for OPEN ALL NIGHT; five parallel subagents against one craft guide; seven song takes; total time and cost not stated on the page | No explicit quality rating; the first two films use "no generative video at all"; every sound lands "frame-exactly"; "Light is paper" | Actively fights it: physical-medium rules, named references (Saul Bass, Swiss posters), per-glyph kinetic type, blind ranked critiques |
| 2 | **claude-code-film-studio** (MorShahrezaye): The Multiplane Camera (90 s science film; cuts of 45 s portrait, 45 s square, 90 s landscape, two 8 s loops) [38] | Claude Code headless (`claude -p`, `bypassPermissions`); Sonnet 5.5 production then Opus 5.5 finishing; one WebGL2 page of raw GLSL, no image assets | Production 4 h 52 min, 1,547 tool calls, 17 agents, $158.37; finishing 3 h 05 min, 586 calls, 5 agents, $49.21; total about 8 h, 22 agents, $207.58 | Logs: "Nothing was auditioned by ear"; 604 images opened, 0 videos, 0 sounds played; 47% of soundtrack energy under 150 Hz; read 8% of its own craft library | Not stated; "seven flat panes of painted glass in the dark" |
| 3 | **scuti.asia** 18 s intro (HTML + GSAP 3, `window.seekTo(t)`, Chrome + ffmpeg, 540 frames) [43] | Claude Code (Opus 5.5) writes storyboard and code and calls a fresh critic | Re-render about 2 min; round 3 about 10 min; three critic rounds; total not stated | Critic is "the most valuable part"; "the SVG dragon still looks a bit toy-like"; "a human must check smoothness and sound" | Not claimed generic; early defects were timing (empty frames, text too long) |
| 4 | **Three Little Pigs** (ruidiao): 52 s, 15 scenes [40] | Claude Code with four custom skills; Azure TTS with character timestamps; local Qwen image models and Wan2.2-Lightning; ffmpeg | One terminal session "yesterday"; cost "essentially free" | Positive on "precise audio-visual timing" and consistent characters; no detailed critique | Not discussed |
| 5 | **Louise de Sadeleer**: custom motion graphics (bar charts, Venn diagrams, title cards) [41] | Claude Code, Remotion (Blank template, Tailwind), Remotion skill; ProRes `.mov` out | "A couple of prompts" per graphic | "Nailed the colors, the typography, and the entrance animations"; "the bottleneck shifts from technical skill to taste"; complex hand-drawn elements are harder | Mitigation: personalise to your own data and design system |
| 6 | **OpenReplay** Remotion tutorial: 15 s product-feature reveal [42] | Claude Code, Remotion | Not stated | "The friction is never the prompt: it's understanding the code Claude hands back"; "The payoff of this stack is the second render, not the first" | Linear `interpolate` "looked mechanical" until `spring()` or an easing was used |
| 7 | **claude-animation-studio** (i-afaqrashid): 20 to 58 s films incl. a 22 s "Happy Birthday" card [39] | Plugin; headless Chrome + ffmpeg; synthesised audio; offline TTS | `--draft` half-resolution is "2 to 4x faster"; no time given | Promotional; admits caption word times "can be a little off"; GIF previews silent | Not discussed |
| 8 | **BlenderMCP** reviews [45] | Claude plus a Blender add-on over a socket | No film found | "impressive but limited" (search result only) | n/a |
| 9 | **HyperFrames** feature post (Menon Lab) [23] | HyperFrames, Claude Code skill | Example prompts only | No verdict on quality; praise is for determinism | None |

**Practices that transfer to a personal, emotional piece.**
- **Audio first.** Pictures lock to word timestamps from the narration or music (cases 1, 4, 7). For us the audio is the mother's relatives' recorded voices; their pauses set the pace.
- **Animatic before building**, then parallel section builds against one craft guide (case 1).
- **Evidence-based review**: contact sheets for shape, frame strips for key moments, full-resolution crops for faces and type, seam checks at the first and last 0.3 s, a numeric pacing audit (case 1); a fresh-context critic repeated across rounds (case 3).
- **Resumable, parallel, scripted renders** and a `--draft` half-resolution mode (cases 1, 7).
- **Skills encode trial and error** (case 4): the orchestrator turns R4 into a skill.
- **Add a listening step**: the cautionary case 2 and "a human must check sound" (case 3) mean the maker or a relative listens to every chapter.
- **The second render is the payoff** (case 6): do not spend hours on a first draft; make the harness cheap to re-run.
- **Do not transfer:** unattended `bypassPermissions` studios (case 2's own warning says to use a disposable VM), AI-sung songs or cloned voices (Principle 4; the music question is in `creator-threads.md` [8]), hosted upload-your-ZIP renderers (case 9), and anything that sends family photos to a third-party video model.

### Q10. Where does the Craft-headless idea stand? Is `effectcraft-cli render` on CPU plausible?

- **Syntax (from the v0.11.1 CLI source, read not run) [68].** `effectcraft-cli render [--comp C] --out FILE [--format h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|gif|wav|aiff] [--start S] [--end S] [--work-area] [--fps N] [--resolution full|half|third|quarter|K] [--quality best|draft] [--channels rgb|rgba] [--jpeg-quality N] [--bitrate KBPS] [--prores proxy|lt|standard|hq|4444|4444xq] [--audio auto|on|off] ...`; `render --template T.ectemplate [--values V.json] --out 'title_[#####].png'`; `render F.ecproj --queue`; `render-frame ... --transparent`; `bench [--comp C] [--time S] [--scale K] [--n N] [--play N]` prints per-layer and per-effect ms/frame; `mcp [--autosave] [--automation-read-root DIR] [--automation-write-root DIR]`; headless CPU by default ("headless: renders on the CPU unless started with --gpu"). `.ectemplate` values override Essential Graphics controls by name, which is the strongest "agent prepares, maker finishes" pattern here: the maker designs a title or caption look once in the GUI, the agent renders every instance with different words (Q2 warns this is lower-thirds grammar if overused).
- **Speed and memory evidence [3].** Issue #1615: 8 stacked 1080p 3D video layers, 30 frames: 36 s on 1 thread (1.2 s/frame, 2.1 GB), 17 s on 4 threads (4.2 GB), over 9 GB and OOM at 16 threads; a single `render-frame` peaks at 1.8 GB; a real project with Glow, masks and Fractal Noise used 3.9 to 5.5 GB per frame. There is no CPU in-flight cap in v0.11.1 (`EFFECTCRAFT_CPU_INFLIGHT` is in a pull request only).
- **Plausible for:** 1080p titles, line-draw (Trim Paths), shape and text layers, and light 2.5D with 3 to 5 layers. ESTIMATE: 0.3 to 1.2 s per frame at 1 to 2 threads, so a 10-second shot at 24 fps (240 frames) takes 1.2 to 5 minutes and 2 to 4 GB. **Not plausible for:** Glow, Fractal Noise, heavy masks or rotoscope stacks, or anything that needs a cap you cannot set.
- **Guards the pipeline needs regardless:** `RAYON_NUM_THREADS=2`, one render per process, render to a new filename every time (a failed overwrite destroys the previous file, #1230), ffprobe the output (an OOM leaves no `moov`), checkpoint with `--autosave` [3].
- **Verdict.** Treat `effectcraft-cli render` as an optional container renderer for titles and light 2.5D. Route A reproduces titles and line-draw without it. Decide after spike S1 (T4 in `craft-motion.md` R8 [3]).
- **What the week-1 spike should install, run and measure.** S1 is already scoped in `craft-motion.md` R8 with exact tarballs, SHA-256 values, six tests and pass/fail rules [3]; do not duplicate it. Additions from this note: (a) in T4 also render a `.ectemplate` with `--values` and a 5-layer parallax comp, compare CPU ms/frame against Route A's three.js parallax plane scene at the same size (M9), and record whether `RAYON_NUM_THREADS=2` keeps RSS under 4 GB; (b) T3 should also run the OTIO through `opentimelineio` (M16) so the validator is tested on a real emitter output; (c) run S2 to S5 in R11 below.

---

## Recipes / templates

### R0. Pipeline diagram and decision table (deliverable a)

```
 MAKER (Windows PC, 8-10 h/week)              CLOUD CONTAINER (agents; 4 vCPU, 16 GB, ~24-28 GB free, pauses when idle)
 -------------------------------              -----------------------------------------------------------------------
 scan, interview, choose ---originals-------> (never; masters stay local)               ENCRYPTED DRIVE + 2nd COPY (M1)
 LightCraft batch, conform  <---scripts-----+                                           originals, masters, renders
 consent + cloud level (manifest)  ---------+--> PRIVATE GITHUB REPO (M0: text, code, manifests, briefs, reviews)
 brief approval (G0), style frames (G1)                      |
                                                             v
                                         ORCHESTRATOR -> Sonnet implementers (1 per shot, parallel, one craft guide)
                                           Route A: seekTo(t) scene (SVG+GSAP+rough.js, three.js) -> Chromium capture
                                           Route B: conform + photo moves + baked grain + grade (ImageMagick/Pillow/ffmpeg)
                                           Hero:    Blender CPU shards / rented GPU hour (3-6 shots per chapter)
                                           Craft headless (titles, light 2.5D) only if spike S1 passes
                                                             |
                                                             v
                                         VALIDATE (ffprobe, resvg, check_ids, ORA, OTIO rules, lottie-web, template lint)
                                         -> contact sheet + strips + crops + <=20 MB preview + render.json
                                                             |
                                                             v
                                         FABLE GATE G2 -> reviews/<chapter>/G2-<shot>.md
 pull previews / hand-off files <------------------------------+
 watch, comment (feedback/<shot>.md, screenshots)  -------------> revision (<= 2 rounds)
 REFINE in Craft app (PhotoCraft ORA, VectorCraft SVG, EffectCraft, FilmCraft)  [G3]
 export + lj.ps1 validate  -------------------------------------> hand-back validation, re-inject classes/GSAP, full-res final render
                                                             |
                                                             v
        assemble: timeline spec -> OTIO -> FilmCraft on the PC -> ProRes 422 HQ master -> ffmpeg H.264 -> loudness
        Fable chapter gate G4 -> proxy relative reads chapter G5 -> technical QC G6 -> backups (VeraCrypt + rclone crypt)
```

| Stage | Tool | Runs where | Hand-off format | Fallback |
|---|---|---|---|---|
| Scan and clean | LightCraft + PhotoCraft (per [4]) | PC | 16-bit TIFF, then 8-bit sRGB PNG 2880x1620 | darktable or VueScan, manual levels [2] |
| Restore and upscale | per [2] | PC GPU, or cleared photos via paid-tier API | PNG | manual cleanup, skip |
| Conform stills | ImageMagick, `-auto-orient -resize ... -depth 8 -strip` (R1 in [3]) | PC (real photos), container (stand-ins) | PNG, orientation applied, no ICC reliance | Pillow |
| Style frames | Agent SVG/HTML | Container | PNG at shot size | hand sketch by the maker |
| Illustrations and rigs | Agent SVG, then VectorCraft | Container, PC | SVG with ids, `check_ids.py` | Inkscape (present in the container) |
| Raster paint-over | PhotoCraft | PC | `.ora` | Krita (reads ORA, checked by the vendor [4]) |
| Drawn and 3D shots (Route A) | Chromium + `render.mjs` (R7) | Container | PNG frames or ProRes 4444 / H.264 | HyperFrames or Remotion (pinned, `--color-space=bt709`) |
| Photo shots (Route B) | Pillow/ImageMagick + ffmpeg | Container (cleared) or PC (real) | H.264 or ProRes clips | FilmCraft keyframes on the PC |
| Hero shots | Blender (bpy 5.2.2) | Container shards or rented GPU hour | PNG frames, then ProRes | three.js scene in Route A |
| Titles, captions | EffectCraft template CLI | Container if S1 passes, else PC | RGBA PNG sequence or ProRes 4444 | Route A SVG text with OFL fonts |
| Audio | Audacity + ffmpeg (`loudnorm`, `ebur128`), FilmCraft Essential Sound | PC (record, clean), container (mix, measure) | WAV 48 kHz 24-bit | none better; avoid SoundCraft [3] |
| Assembly | FilmCraft from OTIO | PC | `.fcproj` (private), OTIO/FCP7 XML | Kdenlive or Resolve free from OTIO [3]; `melt` or ffmpeg concat |
| Master and access copies | ffmpeg | Container or PC | ProRes 422 HQ, H.264 yuv420p BT.709 tv | FFV1/MKV dual master [7] |
| Validation | ffprobe, resvg, `check_ids.py`, `opentimelineio`, lottie-web | Both | JSON reports | manual checklist |
| Backup | VeraCrypt or BitLocker; rclone crypt to B2 | PC | encrypted copies, manifest checksums | second SSD |

### R1. Repo layout and media policy (deliverable b)

```
life-journey/                      private GitHub repo, plain Git, no LFS, target < 200 MB, innocuous name
  CHARTER.md  README.md  CLAUDE.md     CLAUDE.md = agent rules incl. media tiers and "no personal files in the repo"
  agents/  skills/  playbooks/  research/  reviews/        existing
  pipeline/
    bin/        render.mjs  conform.py  grain.sh  motion.py  otio_emit.py  contact_sheet.py  edit_audit.py
                validate_ora.py  check_ids.py  validate_svg.mjs  validate_media.py  validate_otio.py  lint_template.py
    lib/        gsap-3.15.0/ (vendored min.js + licence)  roughjs-4.6.6/  fonts/ (OFL/Apache files + LICENSE per family)
                textures/ (CC0, with source URL and date in textures.json)
    schema/     media.schema.json  shot.schema.json  render.schema.json
    win/        lj.ps1  README (what to install on the PC)
  chapters/
    ch01-<slug>/
      outline.md  script.md  shotlist.yaml  timeline.json (neutral spec, R3 in [3])  timeline.otio  chapter.json (status, gates)
      shots/LJ-C01-S014/
        brief.yaml  scene/ (index.html, art.svg, motion.py ...)  render.json (inputs, params, tool versions, seed, command, hashes)
        review/ (contact sheet, strips; synthetic or cleared images only)   handoff/ (small files for the Craft apps, if cleared)
  manifests/
    media.jsonl      one line per asset (R2); personal names replaced by person ids; the key P-id -> name is kept OFFLINE
    renders.jsonl    one line per render version (id, shot, version, status, sha256, bytes, where stored)
    people.consent.yaml   consent per person id and scope (no names)
  feedback/   LJ-C01-S014.md and screenshots of synthetic or cleared material
  reviews/<chapter>/   G0-... G6-... one file per gate
  .github/    optional: schema validation of manifests and briefs only; no rendering
```

Rules:
1. **M0 repo**: text, code, JSON/YAML, licensed fonts and textures, synthetic fixtures, vendored libraries; each file well under 50 MiB.
2. **M1 private**: scans, originals, audio, video, renders, `.fcproj`, `.ora`, `.psd` live only on the encrypted drive and its encrypted second copy; the repo has their checksums [5].
3. **`cloud` field gates what the agent may see** (R2). Default `none`. A set moves to `preview` or `full` only when the maker says so; before the first `preview`, the maker confirms the account's model-improvement setting is off (30-day instead of 5-year retention) [51].
4. **Naming.** Assets `LJ-<set>-<seq>-<side>` (for example `LJ-B03-0042-F`, as in [2]) with a derivative suffix `__L2` for the label level; people `P-001`; chapters `C01`; shots `LJ-C01-S014`; generated pieces `LJ-C01-S014-A03`. Renders `LJ-C01-S014_v007_draft.mov`; approved `..._v007_appr.mov`; chapters `LJ-C01_v003_master.mov`.
5. **Render versions** only increase and are never overwritten (EffectCraft overwrite loses data, #1230 [3]). `render.json` records the git commit of the scene, manifest ids, parameters, seed, tool versions and command line, and the output hashes.
6. **Pruning.** Keep the approved render, the last two drafts per shot, and any draft cited in a review; delete other drafts after 14 days; keep every `renders.jsonl` line forever. Frames are deleted as soon as the chunk is encoded.
7. **Gates in the repo.** One file per gate, `status` in `chapter.json` (`G0 approved`, ...), nothing moves to the next state without the previous gate file saying `approve` with all six scores 4 or higher [1].

### R2. Manifest schema (media.jsonl, one JSON object per line)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "sha256", "bytes", "media_type", "source", "date", "label", "consent", "cloud", "storage"],
  "properties": {
    "id":          {"type": "string", "pattern": "^LJ-[A-Z]\\d{2}-\\d{4}-[FB](__L[0-5])?$"},
    "sha256":      {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "bytes":       {"type": "integer"},
    "media_type":  {"enum": ["image/tiff", "image/png", "image/jpeg", "video/quicktime", "video/mp4", "audio/wav", "application/pdf", "image/svg+xml", "application/x-ora"]},
    "source":      {"type": "object", "required": ["kind", "holder"],
                    "properties": {"kind": {"enum": ["print-scan", "negative-scan", "slide-scan", "phone", "home-video", "letter", "document", "audio", "generated", "found"]},
                                   "holder": {"type": "string", "description": "person id who owns the original"},
                                   "origin": {"type": "string", "description": "album, box, folder; no names"},
                                   "scan": {"type": "object", "properties": {"date": {"type": "string"}, "ppi": {"type": "integer"}, "device": {"type": "string"}, "settings_ref": {"type": "string"}}}}},
    "people":      {"type": "array", "items": {"type": "string", "pattern": "^P-\\d{3}$"}},
    "date":        {"type": "object", "required": ["value", "precision", "basis"],
                    "properties": {"value": {"type": "string", "description": "ISO 8601 or a range"},
                                   "precision": {"enum": ["day", "month", "year", "decade", "unknown"]},
                                   "basis": {"enum": ["print-stamp", "exif", "told-by", "inferred", "unknown"]}, "told_by": {"type": "string"}}},
    "place":       {"type": "string"},
    "label":       {"type": "object", "required": ["level", "iptc_digital_source_type"],
                    "properties": {"level": {"enum": ["L0", "L1", "L2", "L3", "L4a", "L4b", "L4c", "L5"], "description": "Reality Ladder from ai-imagery"},
                                   "iptc_digital_source_type": {"type": "string", "description": "URI from the IPTC digitalsourcetype vocabulary (cv.iptc.org), see ai-imagery Q8"}}},
    "derived_from": {"type": "array", "items": {"type": "string"}},
    "chain":       {"type": "array", "items": {"type": "object", "required": ["tool", "version"], "properties": {"tool": {"type": "string"}, "version": {"type": "string"}, "params_sha256": {"type": "string"}}}},
    "consent":     {"type": "object", "required": ["status"],
                    "properties": {"status": {"enum": ["pending", "cleared", "restricted", "withheld"]},
                                   "by": {"type": "string", "description": "person id"}, "scope": {"type": "array", "items": {"enum": ["private-viewing", "family-screening", "wider"]}}, "note_ref": {"type": "string"}}},
    "sensitivity": {"type": "object", "properties": {"proxy_review": {"type": "boolean"}, "topics": {"type": "array", "items": {"type": "string"}}}},
    "cloud":       {"enum": ["none", "preview", "full"], "default": "none"},
    "storage":     {"type": "object", "required": ["primary"], "properties": {"primary": {"type": "string"}, "copy2": {"type": "string"}, "verified_at": {"type": "string"}}}
  }
}
```

Example line (synthetic): `{"id":"LJ-B03-0042-F__L1","sha256":"<64 hex>","bytes":51840664,"media_type":"image/tiff","source":{"kind":"print-scan","holder":"P-004","origin":"album 3, page 7","scan":{"date":"2026-11-02","ppi":600,"device":"flatbed","settings_ref":"scan-profiles/flatbed-600.json"}},"people":["P-001","P-007"],"date":{"value":"1984-08","precision":"month","basis":"print-stamp"},"place":"kitchen","label":{"level":"L1","iptc_digital_source_type":"http://cv.iptc.org/newscodes/digitalsourcetype/humanEdits"},"derived_from":["LJ-B03-0042-F"],"consent":{"status":"pending"},"cloud":"none","storage":{"primary":"vault:/scans/B03/0042-F__L1.tif","copy2":"b2crypt:/scans/B03/0042-F__L1.tif"}}`. The IPTC URIs and the level meanings are from [2]. Checksums are produced on the PC by a script; the repo validates only the shape.

### R3. Shot brief template (fields an agent needs to produce a first draft without asking)

```yaml
id: LJ-C01-S014
chapter: C01
class: A            # A parameterised photo move | B designed graphic | C hero shot | D title or caption
beat: "One sentence: what the viewer should feel or learn."
source_ref: "interview excerpt id or document id that this beat comes from"
duration_s: 6.0
fps: 24             # project rate; do not change per shot
route: B            # A | B | blender | craft
inputs:             # media ids with label level and cloud level; the agent must refuse ids whose cloud is none
  - {id: LJ-B03-0042-F__L1, role: main, cloud: preview, crop: "keep both faces; no silent crop"}
look:
  style_frame: styles/ch01/kitchen-warm-01.png
  palette: [paper-cream, tomato-red, ink-brown, faded-green]     # ids from the palette file, max 6
  type: {family: Caveat, source: fontsource, license: OFL-1.1, use: "captions only"}
  texture: {paper: "ambientcg:<asset id as recorded in textures.json>", grain: grain-8f-on-twos}
motion:
  camera: "slow push, drift left, settle at 4.8 s"      # a family, not a recipe; the generator picks parameters from the seed
  ease_family: asymmetric-settle
  hold_on_twos: true
  imperfections: [paper-wobble 0.6deg, late-by-3-frames: caption]
  seed: 20261024
audio: {vo: LJ-A02-0007, music_cue: m03, ambience: kitchen-tap, sync_points: ["3.2s: she laughs"]}
text: {captions: ["..."], language: en, burned_in: true}
transitions: {in: "dissolve 14 frames, uneven", out: "cut on laugh"}
constraints: [no invented faces, no lower thirds, no beat-synced zoom, reconstruction must be visibly stylised (L5)]
refine_in: {app: FilmCraft, touch: "caption timing; push amount"}
acceptance: ["first and last 0.3 s clean", "face never cropped", "hold >= 0.75 s after the laugh"]
output_level: L4a    # label ladder level of the result
privacy: {proxy_review: false}
```

### R4. The everyday loop as a written procedure (deliverable c; the orchestrator can turn this into a skill)

Roles: **O** orchestrator, **I** Sonnet implementer, **F** Fable advisor, **M** maker, **P** proxy relative, **S** scribe (Haiku). State lives in `chapter.json`. Time budgets are ESTIMATES for one shot; class A shots are batched.

0. **Plan the day (O, 5 min).** Read `chapter.json`; pick at most 5 shots in `ready`; check each brief's `inputs[].cloud`. If an input is `cloud: none`, the agent still writes the brief, the script and the expected `render.json`, commits them and marks the shot `pc-render`; M runs `lj.ps1 run <shot>` on the PC and pushes the validator JSON and the preview; only the cloud render is skipped. Raising the level is never the agent's move.
1. **Brief (O drafts, M approves) [G0, M 2 to 10 min].** M writes `approve: yes` or comments in `feedback/<shot>.md`. F checks Meaning, Ethics, testable acceptance (R5).
2. **Style frames, only for a new look [G1, M 15 min, F 10 min].** I produces 3 stills; F and M approve; palette, type, textures and seed recorded. No motion before G1.
3. **Generate (I, 10 to 40 min wall, async).** Read the brief, `playbooks/craft.md`, the rows of `media.jsonl`. Build the scene; render a `--draft` (half resolution) to a pipe; write `render.json`; make a contact sheet (shape), frame strips (key moments), full-resolution crops (faces, type) and a preview of 20 MB or less.
4. **Self-check (I, 5 min).** Run validators and `lint_template.py` and `edit_audit.py` (R8). Up to 3 fix loops; failures go to the review file, not around it.
5. **Fable review [G2, F 5 to 15 min].** Fresh context with the brief, contact sheet, strips, crops and validator JSON; scores and at most 8 nudges in `reviews/.../G2-<shot>.md`; verdict `approve` or `revise` (R5). Run the critic twice in different frame orders and aggregate; "treat any AI critic as a noisy sensor" [37].
6. **Maker review (M 5 to 10 min).** Watch the preview, with sound on. Write the comment file (R6). Blind A/B of the draft against a variant for any shot flagged template-risk. Approve, revise, or take it to the Craft app.
7. **Revise (I, 10 to 30 min).** At most 2 rounds, then freeze the scene.
8. **Refine in a Craft app [G3, M 20 to 90 min for class B and C only].** Pull the `handoff/` files; open them in PhotoCraft (ORA), VectorCraft (SVG, Save As settings from [4]) or EffectCraft or FilmCraft; export; run `lj.ps1 validate <file>`.
9. **Hand-back (I, 10 min).** Validate (`check_ids.py`, ORA stack, ffprobe), re-inject classes and GSAP by id, render the full-resolution final, version `v00N_appr`; update `renders.jsonl`.
10. **Assemble the chapter (O + M, 1 to 2 h per chapter pass).** Regenerate `timeline.otio` from the timeline spec; M opens it in FilmCraft, adjusts, exports ProRes 422 HQ; ffmpeg makes the H.264 access copy; audio loudness measured. **G4:** F reviews the whole chapter (pacing, variety of moves, continuity, captions). **G5:** P reads the chapter for dignity and facts (hard chapters especially). **G6:** technical QC (ffprobe, `ebur128`, captions, TV test at 3 m, safety copy) [7].
11. **Close (S, 10 min).** Update manifests and ledgers, commit, run the backup script, prune drafts, write the day's note.

Failure paths: a validator fails twice, F says `revise` three times, or a Craft app crashes: stop, write the finding in the shot's review file, switch the shot to its fallback route (R0 table). Never skip a gate to hit a date; shorten the shot list instead (Principle 6).

### R5. Fable review checklist at each gate (scores 1 to 5 on the six charter criteria [1]; approve only if all 4 or higher and nothing critical open)

- **G0 brief.** Meaning: does the beat come from a named source (interview or document), not from the template? Specificity: is a camera family, ease family, palette, type and seed named? Accuracy: dates, names (as ids), places match the manifest; every claim has `source_ref`. Feasibility: route chosen fits the clip class and time budget. Ethics: every input has `consent.status`, `cloud` allowed for this use, label level L0 to L5 shown on screen as the ladder requires [2]; no invented faces or voices. Craft: acceptance checks are testable.
- **G1 style frame.** Meaning: could this be any family's video? Palette 6 colours or fewer, sampled from her prints; type licence file present; textures have source and licence; asymmetry present; nothing from the anti-pattern list (Q2). Ethics: reconstruction frames are visibly stylised.
- **G2 shot draft.** Validators green (Q5) with JSON attached. Timing: hold after payoff at least 0.75 s, no looping to fill a slot, shots of 1.5 s or longer except impact frames, first and last 0.3 s clean. Motion: anticipation and settle present, no raw lerp, no twinning, hold on twos where drawn; ease strings not uniform. Faces and type checked on full-resolution crops. No lower-third grammar outside credits. Likeness: faces come from the photo, never regenerated. Template-risk lint output reviewed. Open items listed, not hidden.
- **G3 refine.** The maker's changes pass `check_ids`/ORA/ffprobe; nothing the maker did was lost; labelled.
- **G4 chapter.** Rhythm across shots (varied move families, holds, silence), continuity of palette and type, audio mix and loudness plan, captions (line length, rate, 42 characters per line limit from [7]), credit cue sheet per the ladder. **G4 rule:** no more than three class-A shots in a row without a held still, a class B, C or D shot, or a voice-only beat; at least one shot per chapter where the photo does not move at all. Sixty percent moving photographs is the slideshow the charter rejects, however varied the wobble.
- **G5 dignity (proxy relative).** Each hard topic (loss, illness, separation, money, conflict) cleared or removed; anything she might not want shown in front of others is out of the shared version (Principle 5).
- **G6 technical QC.** Master ProRes 422 HQ; H.264 yuv420p BT.709 tv; frame count, duration, 48 kHz audio; loudness within target; open and sidecar captions; a USB-playable file tested on the venue-class TV; checksums in the ledger; two backups verified.

### R6. Feedback comment file (`feedback/LJ-C01-S014.md`, written by the maker, read by the agents)

```markdown
---
shot: LJ-C01-S014
version: v007_draft
reviewer: maker
approve: no            # yes | no | with-changes
---
- 00:01.2  hold longer on her face; the push starts too soon  [should]
- 00:03.2  laugh lands, music is already loud  [blocker]
- 00:05.0  caption font too thin on the TV  [should]
- whole    camera drifts the same way as S013  [nice]
screenshots: [LJ-C01-S014_00-03.png]   # annotated with Win+Shift+S; synthetic or cleared images only
craft-app-needed: no
```

Severity words are `blocker`, `should`, `nice`. The agent answers each line in `render.json` notes with `done`, `declined (why)` or `question`.

### R7. Seek-capture harness (Route A renderer)

Tested status: the pattern was measured in M9, M10 and M12. The exact code block below was extracted from this file and run on the three.js probe scene: shards 0/2 and 1/2 wrote 24 distinct frames that were pixel-identical (0 differing pixels) to those from an earlier run of the same harness in a separate process; a re-run did 0 frames; `--ffmpeg` produced a 24-frame `yuv420p`, `tv`, `bt709` MP4. The `--ffmpeg` filter chain was changed in the round-1 follow-up (Q-F1); S2 must re-test it.

```js
// pipeline/bin/render.mjs   usage: node render.mjs --page scene.html --out frames --fps 24 --seconds 2 [--shard 0/2] [--alpha] [--ffmpeg out.mp4]
// The page must define window.seekTo(t_seconds) as a PURE function of t and set window.ready = true when fonts/images are loaded.
import { createRequire } from 'node:module'; import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process';
const { chromium } = createRequire(import.meta.url)(process.env.PW_PATH || 'playwright');     // container: /opt/node-tools/node_modules/playwright (1.56.1)
const a = Object.fromEntries(process.argv.slice(2).reduce((r, x, i, v) => (x.startsWith('--') ? [...r, [x.slice(2), v[i + 1]?.startsWith('--') || v[i + 1] === undefined ? true : v[i + 1]]] : r), []));
const fps = +a.fps || 24, N = Math.round((+a.seconds || 1) * fps), W = +a.w || 1920, H = +a.h || 1080, [si, sn] = (a.shard || '0/1').split('/').map(Number);
const root = path.resolve(a.dir || '.'); fs.mkdirSync(a.out || 'frames', { recursive: true });
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => fs.readFile(path.join(root, decodeURIComponent(q.url.split('?')[0])), (e, b) => e ? (r.writeHead(404), r.end()) : (r.writeHead(200, { 'content-type': mime[path.extname(q.url.split('?')[0])] || 'application/octet-stream' }), r.end(b)))).listen(0, '127.0.0.1');
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('pageerror', e => { console.error('[page error]', e.message); process.exitCode = 2; });
await page.goto(`http://127.0.0.1:${srv.address().port}/${a.page}`); await page.waitForFunction(() => window.ready === true); await page.evaluate(() => document.fonts.ready);
const ff = a.ffmpeg && spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv', '-c:v', 'libx264', '-crf', '18', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', a.ffmpeg], { stdio: ['pipe', 'inherit', 'inherit'] });
let done = 0; const t0 = Date.now();
for (let f = si; f < N; f += sn) {                                   // shard i of n takes every n-th frame
  const file = path.join(a.out || 'frames', `f_${String(f).padStart(6, '0')}.png`);
  if (!ff && fs.existsSync(file)) continue;                          // resume: skip frames that exist (written via .tmp + rename)
  await page.evaluate(t => window.seekTo(t), f / fps);
  const buf = await page.screenshot({ type: 'png', omitBackground: !!a.alpha });
  if (ff) ff.stdin.write(buf); else { fs.writeFileSync(file + '.tmp', buf); fs.renameSync(file + '.tmp', file); }
  done++;
}
if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
console.log(JSON.stringify({ shard: a.shard || '0/1', frames: done, seconds: (Date.now() - t0) / 1000 }));
await browser.close(); srv.close();
```

Notes: (1) `--ffmpeg` mode needs the whole shot in one process (no sharding) and used about 2.4 fps on the 3D probe because Chromium and x264 compete for 4 vCPUs. (2) A shot of 10 seconds is 240 frames: about 20 s for flat SVG, about 75 s for the heavy 3D probe. (3) Sharded runs write PNGs, so encode afterwards with `ffmpeg -framerate 24 -i frames/f_%06d.png ...` and delete the PNGs. (4) For alpha overlays use `--alpha` and the ProRes 4444 chain in Q5 (Q-F1). The bare `-pix_fmt yuva444p10le` encode of M12 gave BT.601 pixels under BT.709 tags on ffmpeg 6.1.1 and BT.709 pixels on 9.0.2, so the same line is not safe across builds. Run the colour-patch test (R8) on every command-line template and every ffmpeg version. The review's reading that `format=` must precede `scale=` for H.264 was not reproduced (Q-F1 measured format first at 5/255 and scale first at 1/255), so the H.264 chain is scale first. (5) Inside the scene, build GSAP as `gsap.timeline({paused:true})` and expose `window.seekTo = t => { tl.time(t, false); return true; }`; draw random-looking details from a seeded generator (`rough.js` `seed`, an LCG for positions), never `Math.random()` or `Date.now()` (M10).

### R8. Validators the agent runs before every hand-off (build in spike S5)

| Check | Command or rule | Catches |
|---|---|---|
| Media | `ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,color_space,color_range,color_primaries,color_transfer -of json file`; rules: `r_frame_rate == avg_frame_rate == project fps`; `pix_fmt` in the allowed list; `color_range=tv` and `color_space=bt709` for H.264; frame count equals `duration x fps`; `ffmpeg -v error -i file -f null -` prints nothing; `moov` present | wrong rate, `yuvj420p` full-range output (Remotion default, M13), truncated or OOM files |
| Alpha | `identify -format '%[channels] %[opaque]' frame.png` reports alpha and not opaque; ffprobe `pix_fmt` contains `a` for 4444 | opaque overlays |
| Colour matrix (pixels, not tags) | Encode a 3-patch frame (pure red 255,0,0; 50% grey 128,128,128; skin tone 224,172,140) through the shot's exact command line. Decode the frame to `rgb24` with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`; every channel must be within ±3/255 of the source. Run once per command-line template, and again whenever the ffmpeg version differs (the PC build is 9.0.2 from winget, not 6.1.1). Method: Q-F1 (M23) | BT.601 matrix under BT.709 tags, which tag checks cannot see: bare ProRes 4444 on 6.1.1 (error 25), bare H.264 `yuv420p` on 6.1.1 (error 23), format-first H.264 (error 5) |
| SVG | resvg-js or `rsvg-convert` render is non-blank; `check_ids.py a.svg a.rt.svg` exits 0; svgo is lint only, run with `plugins:[{name:'preset-default',params:{overrides:{cleanupIds:false,removeUnknownsAndDefaults:{keepDataAttrs:true}}}}]` (M17); ids match `^[A-Za-z][A-Za-z0-9._-]*$` | stripped ids, class/style reliance |
| ORA | `validate_ora.py`: zip opens; `stack.xml` parses; every `src` exists; layer sizes and offsets inside the canvas; names unique and match the id pattern; only supported attributes | broken hand-off to PhotoCraft |
| OTIO | `opentimelineio` parse (M16) plus rules: every `ExternalReference.target_url` exists, `source_range` inside `available_range`, rate equals project rate, dissolve in and out offsets fit inside neighbours, markers present, `metadata.filmcraft` keys known | out-of-range clips, wrong rate, missing media |
| Lottie | lottie-web in Playwright: `loadAnimation` then `goToAndStop` at 0, middle, end; non-blank frames; positions change; reject `layers: []` and opacity values at 0 to 1 scale (M15, [32]) | blank or invisible output |
| Fonts and textures | each `lib/fonts/<family>/` has the licence file; `textures.json` has a source URL and a date | licence drift |
| Audio | `ffprobe` 48000 Hz, 24-bit; `ffmpeg -i f -af ebur128=peak=true -f null -` loudness and true peak recorded | silent or clipped audio |
| Template-risk lint (`lint_template.py`) | parse scene and `render.json`: flag if more than 60% of tweens share one ease string, stagger spacing is uniform, one transition type exceeds 70% of cuts, every photo move has the same direction or duration, any zoom-in is on every photo | the template feel (Q2) |
| Pacing audit (`edit_audit.py`, after [37]) | hold after payoff at least 0.75 s; shots shorter than 1.5 s only as impact frames or at most three in a row; scan frame differences for pops against a local median | rushed cuts, glitches |
| Determinism | re-render two frames and compare with `compare -metric AE -fuzz 1%`; exact hash when no SVG filters are used; with filters accept up to 100 differing pixels (M10) | non-deterministic scenes |

### R9. Container setup script (cached if it finishes in about five minutes [49]; not timed here)

```bash
#!/bin/bash
# environment Setup script (runs once per cache build; the cache expires after about 7 days)
set -e
python3 -m venv /opt/lj-venv
/opt/lj-venv/bin/pip install --quiet bpy==5.2.2 opentimelineio==0.18.1 pillow numpy      # bpy wheel 402 MB, venv about 1 GB (M14)
mkdir -p /opt/lj-node && cd /opt/lj-node && npm init -y >/dev/null
npm i --silent svgo@4.1.0 @resvg/resvg-js@2.6.2 lottie-web@5.13.0 gsap@3.15.0 roughjs@4.6.6 three@0.186.1 \
      @fontsource/caveat @fontsource/kalam @fontsource/reenie-beanie @fontsource/gaegu @fontsource/patrick-hand
# Playwright 1.56.1 and Chromium 141 are preinstalled (M3); do not run `playwright install` (the CDN answered 400)
# Optional, only if Manim or Pango-based tools are wanted: apt-get install -y libpango1.0-dev libcairo2-dev pkg-config   (untested)
```

Keep the vendored copies in the repo (`pipeline/lib`) as the source of truth; this script is a convenience. Keep the total of installed tools under about 3 GB of the 24 to 28 GB free.

### R10. Windows companion script `lj.ps1` (design; agents write it, the maker double-clicks or runs it)

Commands: `doctor` (Windows edition from `Get-ComputerInfo`, RAM, free disk, GPU from `Get-CimInstance Win32_VideoController`, versions of `ffprobe`, `git` and each Craft CLI; writes `maker-pc.json`, and its output must not contain the PC's Windows user name or machine name, because the file lives in the repo: Pitfall 10 in the playbook); `pull` (git pull, show new briefs); `run <shot>` (renders a `pc-render` shot on the PC from its brief, playbook Step 4); `run-steps <steps.jsonl>` (feeds JSON lines to a Craft CLI as in R2 of [4]); `validate <file>` (ffprobe, `photocraft-cli info`, `vectorcraft-cli convert` plus `check_ids.py`, OTIO parse; prints JSON); `snapshot` (Craft app `ui.screenshot` or `lightcraft-cli snapshot`); `push-feedback` (commits `feedback/` and pushes); `backup` (checksums to `manifests/`, then rclone crypt to the second copy). Needed on the PC: Git, ffmpeg with ffprobe, Python 3.13 or `uv`, the Craft portable zips pinned per [3][4] (winget ids read from the manifests, not run on Windows: `Git.Git`, `Gyan.FFmpeg` (9.0.2), `Python.Python.3.13`; Q-F1). Use PowerShell with JSON through stdin to avoid quoting traps [4].

### R11. Week-1 spike scope (deliverable d; written, not run)

S1 is **already scoped** in `craft-motion.md` R8 (tarballs, SHA-256 values, tests T1 to T6, pass/fail and decision rule) [3]; run it as written. This note adds S2 to S5.

| Spike | Install | Run | Measure | Pass / fail and decision |
|---|---|---|---|---|
| **S2 Chromium capture** | Nothing new (Playwright 1.56.1 and Chromium 141 are preinstalled, M3); copy R7 to `pipeline/bin/render.mjs`; vendor GSAP, rough.js, three.js | (a) flat SVG scene, (b) rough.js plus GSAP with baked grain overlay in ffmpeg, (c) three.js voxel diorama with instanced cubes and a camera push, (d) a title with a self-hosted OFL font, (e) the same scenes with 1, 2 and 4 concurrent pages, (f) a 2,400-frame chapter piped to ffmpeg, (g) kill the process at 50% and resume | fps, peak RSS, disk, frames/s per concurrency level; `compare -fuzz 1%` between two runs; font loaded (`document.fonts.ready`); output tags with ffprobe | Pass: (a) at least 8 fps, (c) at least 2 fps, at most 100 differing pixels per frame, no OOM, resume works, tags correct. Fail: Route A moves to HyperFrames or Remotion (pinned) or to the maker's PC |
| **S3 Blender CPU** | `pip install bpy==5.2.2` (402 MB); optionally the `blender` tarball from download.blender.org (reachable, M19) | (a) 2.5D parallax from 5 RGBA PNG layers at 1080p with an emission-alpha shader: Workbench, Cycles at 4, 8 and 24 spp with denoise, EEVEE; (b) voxel diorama from instanced cubes with a warm sun (recipe R4 in [6]); (c) a 240-frame shard job with skip-existing; (d) optional: the same scene on a rented GPU hour (RunPod RTX 4090 $0.34 to $0.89 per hour per [2]) | s/frame, peak RSS, determinism of Cycles with a fixed seed, EEVEE stability across 2 container restarts | Pass: parallax or voxel hero shot of 240 frames in at most 60 minutes of container time at an acceptable look. Else parallax moves to three.js (Route A) or Pillow (Route B) and Blender is limited to stills. M14 gives the baseline: Suzanne 1080p Cycles 24 spp 17.5 s/frame |
| **S4 Container behaviour** | Nothing | (a) start a 25-minute background job that appends a timestamp every 10 s; stay idle for 10 minutes; read the log for gaps (does a running job keep the VM awake?); (b) repeat while the agent polls with a monitor every 2 minutes; (c) record `df` at start; (d) time the setup script cold and cached; (e) call the Gemini API with a synthetic image using a network secret and confirm the key is not in `env`; (f) push a 50 MB plain-Git file and re-clone to measure session start | gaps in the log, wall times, free disk, clone time | Decides the shard size (10 minutes or longer), whether polling is required, and whether the repo-size target of 200 MB is realistic |
| **S5 Validators** | `opentimelineio`, svgo, resvg-js, lottie-web (R9) | Build R8 checks; run on good fixtures and on planted defects: ORA with a missing PNG, SVG after default-svgo, OTIO clip outside `available_range`, H.264 `yuvj420p`, Lottie with `o:1`, ProRes without alpha, a scene with one ease string everywhere, and a new planted defect "BT.601 under BT.709 tags" (the bare `-pix_fmt` encodes on ffmpeg 6.1.1: ProRes 4444 and H.264 `yuv420p`, Q-F1), which tag checks pass and only the colour-patch test catches. The M23 script lives in the session scratchpad, not the repo: copy it into `pipeline/bin` for S5 | detection rate, false positives | Pass: all planted defects caught, no false positives on the good fixtures. Also run a Fable critic on a contact sheet with 3 planted defects to see whether the review gate catches them |

**Windows acceptance (maker, about 20 minutes, once):** the five-minute tests for each Craft app in `craft-visual.md` and `craft-motion.md` R7 [3][4], plus `lj.ps1 doctor` pasted back into `maker-pc.json`.

### R12. First three agent experiments for the vertical slice (deliverable e)

| # | Experiment | Route | Inputs | Done when | Decides |
|---|---|---|---|---|---|
| **E1** | **A hand-lettered title card and paper-cut transition (12 seconds).** Seeded rough.js shapes in a limited palette, one OFL handwriting face (and, if the maker supplies a letter scan, traced glyph variants), CC0 paper texture, baked grain on twos, GSAP timeline with RoughEase and per-element asymmetric eases, ProRes 4444 alpha overlay plus an opaque version. Make a second version with default GSAP eases and uniform stagger | A | Synthetic only; palette sampled from a cleared stand-in print | Re-render is identical within 100 pixels per frame; at least 8 fps on flat frames; validators green; the maker (and one relative, blind) picks the crafted version over the default one; planted-defect critic test run once | Whether Route A with `render.mjs` is the default; HyperFrames bake-off (one hour) if the harness feels heavy |
| **E2** | **Ten photos, ten different moves (40 seconds).** Pre-conform ten stand-in stills (R1 in [3]); a seeded generator picks direction, duration, ease family, hold, drift, paper wobble per photo; Pillow transform (M21), grain on twos, era grade, uneven dissolves; emit `timeline.otio` with `metadata.filmcraft`; the maker opens it in FilmCraft (test T3), moves a keyframe, exports ProRes | B | Ten synthetic or maker-cleared photos | No two moves alike by the lint; OTIO imports with motion intact; the stills scale trap handled; a baked variant exists for Resolve/Kdenlive; render under 10 minutes on the container | Whether OTIO-with-metadata is the edit contract, or bake motion in Route B and use OTIO only for cuts |
| **E3** | **One hero shot three ways (6 seconds): the kitchen table as a voxel diorama.** (a) three.js in the harness, (b) Blender Workbench and low-sample Cycles, (c) EffectCraft 2.5D via CLI if S1 passed. Compare look, seconds per frame, how easily the maker can change it, and the file the maker would touch. Also record a listening check: the maker plays the chapter audio on the target TV and writes what the agent could not hear | A, Blender, Craft | A synthetic scene; a cleared photo for the table texture | One route chosen for hero shots with a written reason; the audio listening step exists in the loop | The hero-shot route for the slice and the Blender budget per chapter |

Timeline fit (J): spikes S1 to S5 in week 1; E1 in week 2; E2 in week 3; E3 in week 4; the one-chapter slice in weeks 5 to 8 and reviewed in week 9 (2026-12-20), matching the format track's slice date [7].

---

## Tools and formats (cost, platform, maturity, scriptability as of 2026-10-18)

| Tool | Cost / licence | Platform | Maturity (latest, date) | Scriptable by an agent | Notes |
|---|---|---|---|---|---|
| Playwright + Chromium | Apache-2.0; free | Container (1.56.1, Chromium 141 preinstalled), Windows | npm latest 1.64.1 (2026-10-14) [16]; container build older | Yes | Pin 1.56.x in the container; `cdn.playwright.dev` answered 400 (M3). `page.clock` fakes rAF, not `performance.now` (M11) |
| GSAP | "No charge" Standard License incl. all plugins [15] | Browser, Node | 3.15.0 (2026-04-13) [16] | Yes | Vendor the file; licence may be revised, old versions stay usable [15] |
| rough.js | MIT [24] | Browser, Node (SVG mode needs a DOM) | 4.6.6 (2023-11-20): stable, old [16] | Yes | Use `seed` per shape [25] |
| three.js | MIT | Browser | r186.1 (2026-09-24) [16] | Yes | SwiftShader WebGL2 3.3 fps for 400 lit cubes at 1080p (M9) |
| HyperFrames (HeyGen) | Apache-2.0 [22] | Node 22+, FFmpeg; local, Docker, Lambda | 0.8.169 (2026-10-17), created 2026-03-23 [16][22] | Yes (Claude Code plugin and skills) | Pre-1.0 churn; Studio "available, evolving" [22] |
| Remotion | Free for individuals, up to 3-employee for-profits, non-profits, evaluators; Company License from $25 per seat per month; changes in 5.0 [9][10] | Node, headless Chrome | 4.0.536 (2026-10-16) [16] | Yes (official skills [14]) | `--color-space=bt709 --pixel-format=yuv420p` (M13); `--gl` `swangle` without GPU [11] |
| Motion Canvas | MIT [19] | Browser editor | 3.17.2 (2024-12-14), alpha 3.18.0-alpha.0 (2025-02-16) [16] | Weak (editor-driven) | Dormant |
| Revideo | MIT; anonymous render counting via PostHog [20] | Node + headless browser | 0.11.0 (2026-07-10) [16] | Yes | Not tested |
| Manim | MIT [21] | Python 3.11+ | 0.22.0 (2026-10-08) [17] | Yes | Install failed on 3.13 without Pango/Cairo dev packages (M18) |
| lottie-web / dotLottie web | MIT | Browser | 5.13.0 (2025-05-21); dotLottie web 0.81.0 (2026-10-06) [16] | Yes | Validator only; python `lottie` is AGPL-3.0+ [17] |
| svgo / resvg-js | MIT / MPL-2.0 | Node | 4.1.0 (2026-08-24) / 2.6.2 (2024-03-26, metadata modified 2026-01-28) [16] | Yes | svgo default strips ids: `cleanupIds:false` (M17) |
| OpenTimelineIO | Apache-2.0 | Python 3.10+ | 0.18.1 (2025-11-09) [17] | Yes | No schema validator beyond parse: write rules (R8) |
| Blender bpy | GPL-2.0-or-later source, GPL-3.0-or-later binaries; Cycles Apache-2.0; output is the maker's [83] | Linux/Windows/macOS wheels, Python 3.13 only for 5.1+ | 5.2.2 (2026-09-15) [17] | Yes | Workbench 0.8 s, Cycles 17.5 s, EEVEE 34 s per 1080p frame on 4 vCPU (M14) |
| ffmpeg / ImageMagick / Pillow / numpy | LGPL/GPL build, ImageMagick licence, HPND-style, BSD | Container (6.1.1 / 6.9.12 / 12.3.0 / 2.5.3); Windows needs installs | | Yes | `convert` only; policy limits 1 GiB / 2 GiB (M2) |
| Craft CLIs | Free, open source, alpha | Windows MSI/zip, Linux tar.gz | per [3][4] | Yes (CLI, MCP) | Spike S1 decides container use |
| Claude Code CLI | Pro, Max, Team, Enterprise or API | Windows 10 1809+, macOS 13+, Linux; 4 GB+ RAM [46] | 2.1.302 in the container | n/a | Native install is auto-updating, winget/Homebrew/apt are not [46] |
| Remote Control | Pro, Max, Team, Enterprise; no API keys [47] | Terminal, Desktop app, VS Code | docs read 2026-10-18 | n/a | Window into a local session [47] |
| Gemini API | Per-image and per-second prices in Q4 [65] | Cloud | pricing updated 2026-10-16 | Yes | Paid tier only for family photos [2][65] |
| Replicate | Per second of GPU or per output [66] | Cloud | undated | Yes | API predictions deleted after one hour [2] |
| Git LFS on GitHub | Free 10 GiB + 10 GiB; metered beyond [54] | Cloud | billing page read 2026-10-18 | Yes | Avoid for this project (Q6) |
| Backblaze B2 + rclone crypt | $6.95 per TB-month [59]; rclone MIT | Windows PC | page undated (footer 2024) | Yes | Names and contents encrypted by default [60] |
| Cryptomator / VeraCrypt | Open source; desktop pay-what-you-want / free [62][63] | Windows, macOS, Linux | VeraCrypt 1.26.29 (2026-06-09) [63] | Partly (GUI) | Needed for external SSDs on Windows Home [61] |
| Fonts (`@fontsource/*`) | OFL-1.1 or Apache-2.0 per family [16][29] | npm | 5.3.0 [16] | Yes | Self-hosted, with licence files |
| ambientCG textures | CC0 [28] | Web | undated page | Yes | Record URL and date in `textures.json` |

**Format cheat sheet.** Stills into FilmCraft: 8-bit sRGB PNG, orientation applied, 2880x1620 for a 1080p sequence. Alpha overlays: ProRes 4444 (`yuva444p10le` requested, reported as `yuva444p12le`) or RGBA PNG sequence. Layered raster: OpenRaster. Vector: SVG with ids. Edit: OTIO with `metadata.filmcraft`, FCP7 XML for Resolve. Master: ProRes 422 HQ (about 590 MB per minute on a test pattern, M5). Access copy: H.264 High, `yuv420p`, BT.709, `tv`, `+faststart`. Audio: WAV 48 kHz 24-bit. Dual master for archive: FFV1 v3 in Matroska or ProRes in QuickTime [7].

---

## Risks, pitfalls and ethics (with mitigations and fallbacks)

1. **The template feel.** Agents default to uniform eases, stock transitions and tidy symmetry. Mitigation: per-shot seeded parameter generation, look-lock before motion, `lint_template.py`, a blind A/B at G2, and the maker's eye at every Craft-app pass. Fallback: cut the effect, hold the shot longer.
2. **Agents do not hear.** A 22-agent run opened 604 images and played 0 sounds [38]; a stills-only critic cannot judge smoothness or sound [43]. Mitigation: measure loudness (`ebur128`), but require a human listening pass at G2 and G4, on the target TV.
3. **Non-determinism where filters are used.** Live SVG filters cost frame rate and produced tiny differences between runs (M10). Mitigation: bake grain and paper into overlays; compare with a fuzz; keep filters off the full frame.
4. **Idle pause and reclaim of the container.** Background work is not restored after a reclaim [50]. Mitigation: shards of 10 minutes or less, resumable frames, state in Git, spike S4. Fallback: run long jobs on the PC or a rented machine.
5. **Disk.** Textured PNG frames fill the disk (about 29 GB for a 10-minute film, M10). Mitigation: pipe to ffmpeg, encode per chunk, delete frames, budget 3 GB of tools (R9).
6. **Licence drift.** Remotion's licence changes in 5.0 [9]; GSAP's Webflow licence "may be updated at any time" [15]. Mitigation: pin versions, vendor GSAP and rough.js, store a dated copy of each licence page in `pipeline/lib/LICENSES/`, re-check before any upgrade. A personal gift is inside the free terms today.
7. **Alpha-software dependence.** The Craft apps are about 2.5 weeks old and cut a tag every 1 to 3 days [3][4]. Mitigation: every step has a non-Craft fallback (R0 table); the `.fcproj` is regenerable from the neutral timeline spec and OTIO; render to a new filename every time; never save over the only copy.
8. **Colour and range errors.** Remotion's default output was full-range `bt470bg` (M13); FilmCraft ignores EXIF orientation and ICC [3]. Mitigation: R8 media checks; conform stills first; test on the target TV.
9. **Privacy of the cloud route.** Photos that Claude views join the transcript; Pro and Max with model-improvement on keep 5 years and may train, with it off 30 days; cloud sessions store the transcript; Remote Control also syncs it to Anthropic [51]. Hosted renderers and "memorial video" services take photos to third parties. Mitigation: `cloud: none` by default, per-set maker decision, preview-size proxies, the account's model-improvement setting off before any `preview`, no hosted renderers, no photo on the Craft Discord/ticket flow (bug reports are relayed to public GitHub issues [3]).
10. **Surprise leaks.** Cloud sessions, the repo, Remote Control and mobile push notifications from the Claude app can show on shared devices; the repo name, commit messages, backup folders, B2 bucket name and desktop folders must be innocuous. Cloud photo libraries and family group chats are the usual leaks (charter [1]). Mitigation: a separate browser profile for the project; notifications off on shared phones; names as person ids in the manifest.
11. **Permissions.** Do not copy `bypassPermissions` studios [38]. Craft control ports are unauthenticated except PhotoCraft's (token) and FilmCraft's MCP has no folder confinement [3][4]: start them per session only. API keys go in Network secrets [49], never in chat, environment variables or the repo.
12. **Windows memory.** The CLI has reports of runaway memory on Windows (13 to 50 GB) [53]. Mitigation: cloud sessions by default; short local sessions; watch Task Manager in week 1.
13. **Principle 4 and the ladder.** No photoreal generation of people; reconstructions in the house style and labelled; her handwriting font used only for words she wrote (Q2); no voice cloning. Each output carries its label level in the manifest, the filename suffix and the credits [2].
14. **Over-scope and cost.** An unattended multi-agent run cost $207.58 for 90 s [38]; plan usage limits are shared with all other Claude use [50]. Mitigation: one shot per implementer, at most 3 parallel, 2 revision rounds, a weekly budget line, and Principle 6 (shorten the film before skipping a gate).
15. **Price and policy changes.** Google's pricing page announces changes on 2026-12-01 and 2027-01-01 (Gemini 4 Argon; Gemini 3.8 and 3.6 Flash, the 3.8 TTS models, Robotics ER 2) and names no image or video model among them [65]; GitHub's LFS rates for personal accounts are unverified [54][57]. Mitigation: no image or video model is named in the announced changes, so run the image batch when cleared photos exist and re-read the page in the week it runs; avoid LFS.
16. **EEVEE and GL stability.** EEVEE rendered here with `EGL_BAD_MATCH` warnings (M14) and forum posts say headless EEVEE was unsupported [35]. Mitigation: Workbench or Cycles by default; EEVEE only after S3.
17. **Evidence quality.** The examples are short and self-reported (Q9). Treat all quality claims as unproven for a 10-minute emotional piece.

---

## Open questions / gaps

1. **The maker's PC.** RAM, CPU cores, GPU and VRAM, free disk, Windows edition (BitLocker needs Pro or higher), whether a shared family device is involved. `lj.ps1 doctor` (R10) answers it. It sets local-model options, FilmCraft export speed, the encryption route, and whether a local agent is viable.
2. **Does a running background job keep a cloud VM awake?** Not documented in the pages read; spike S4.
3. **Does claude.ai/code accept image attachments in cloud sessions?** Remote Control docs confirm attachments into a local session [47]; cloud-session attachments were not stated. Test in week 1.
4. **Remote Control on native Windows** is not restricted in the docs but is untested by us [47].
5. **Plan usage limits.** Whether 19 weeks of daily agent work fits a Pro or Max allowance is unknown; cloud sessions "share rate limits" with all other use [50].
6. **GitHub LFS rates for personal accounts** are inferred from the 2024 changelog and 2023 FAQ [57][58]; the billing page itself had no dollar figures [54].
7. **Gemini price changes.** The announced changes name no image or video model [65]; re-read the page in the week the batch runs. Veo has no published batch price (Q-F5).
8. **SVG-filter non-determinism** (up to 80 pixels of 2.07 million in 5 of 36 frames, M10): cause not isolated (tiling, threading or timing); try `--disable-gpu-rasterization`, a single raster thread, or `--disable-features=...` in S2.
9. **HyperFrames** versus the repo-owned harness: determinism rules, lint syntax and render options were not documented on the pages I read [22]; bake-off in E1.
10. **Cycles on a rented GPU** was not measured; the estimate of 1 to 3 s per frame is a guess (UNVERIFIED).
11. **A browser tab's memory** for claude.ai/code and the local CLI's memory on the maker's PC: unmeasured.
12. **Can any model listen?** I did not evaluate audio-capable critics (for example Gemini with audio input), which would also send family audio to a third party. Default remains: a human listens.
13. **Frame rate.** 24, 25 or 30 depends on the venue's playback chain and region; the pipeline is rate-agnostic but must pick one in week 1.
14. **No multi-minute emotional agent-made film and no family tribute made with a coding agent were found.** X/Twitter, Reddit and YouTube were not reachable. A search of those communities by the maker may find better evidence.
15. **Corrections for earlier notes (for the scribes).** (a) `craft-motion.md` R8 and `ai-imagery.md` say the container lacks Chromium and Playwright; this container has Playwright 1.56.1 and Chromium 141 preinstalled (M3), so the Playwright web-build route in `craft-visual.md` Q8 is cheaper than stated. (b) `toolchain.md` lists headless EEVEE as unverified: it rendered here (M14). (c) `craft-motion.md` says the Craft CLIs have no spike data; S1 remains the gate. (d) `ai-imagery.md`'s Gemini 2.5 Flash Image shutdown date (2026-10-02) is now past [65].
16. **`rclone`** is not on PATH in the container; backup runs from the PC.
17. **Windows package ids** for ffmpeg and Python via winget: closed in the round-1 follow-up (Q-F1). The ids were read from the winget manifests and have not been run on Windows.

---

## Sources

Project files (read 2026-10-18)
- [1] Life Journey Project Charter — `CHARTER.md` — 2026-10-18 — roles, rubric, principles, constraints.
- [2] AI imagery and motion from real photos — `research/ai-imagery.md` — 2026-10-18 — verified privacy terms, label ladder, cost tiers, scanning rules, GPU tiers (its own numbered sources, including [83] RunPod prices, not re-opened).
- [3] ArtCraft motion and sound apps as refinement layers — `research/craft-motion.md` — 2026-10-18 — FilmCraft, EffectCraft, SoundCraft facts, R1 conform, R3 interchange, R4 EffectCraft recipes, R7 acceptance tests, R8 spike S1.
- [4] ArtCraft visual apps as refinement layers — `research/craft-visual.md` — 2026-10-18 — PhotoCraft ORA contract, VectorCraft id contract, control channels and MCP, recipes.
- [5] Charter review 00 — `reviews/00-charter-review.md` — 2026-10-18 — raw-material storage rule, section 5.
- [6] Free desktop toolchain and core techniques — `research/toolchain.md` — 2026-10-18 — Blender parallax and voxel recipes, era grades, GSAP free since 3.13.
- [7] Delivery format and experience architecture — `research/format.md` — 2026-10-18 — 8 to 12 minute film, dual master, captions, week-9 slice, hours budget.
- [8] Creator recipes — `research/creator-threads.md` — 2026-10-18 — hold-on-twos, paper-print wobble, AI music questions.

Frameworks, licences, techniques
- [9] Remotion LICENSE.md — https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md — read 2026-10-18 (copyright 2026) — free categories; "In Remotion 5.0, the license will slightly change".
- [10] Remotion Company License and pricing — https://www.remotion.pro/license — 2026-10-18 (undated, © 2026) — $25 per seat per month Creators, $100 per month Automators, Enterprise from $500.
- [11] Remotion `gl` options — https://www.remotion.dev/docs/gl-options — 2026-10-18 — swangle without GPU; defaults.
- [12] Remotion performance — https://www.remotion.dev/docs/performance — 2026-10-18 — PNG vs JPEG, GPU effects, concurrency.
- [13] Remotion fundamentals — https://www.remotion.dev/docs/the-fundamentals — 2026-10-18 — "A video is a function of images over time".
- [14] Remotion with Claude Code — https://www.remotion.dev/docs/ai/claude-code — 2026-10-18 — `npx remotion skills add`, blank template.
- [15] GSAP Standard "no charge" License — https://gsap.com/standard-license/ — effective 2025-04-30, last modified 2025-05-30 — free incl. plugins; prohibited uses; AI-generated code not prohibited.
- [16] npm registry metadata — https://registry.npmjs.org/remotion , /@remotion%2Frenderer , /@motion-canvas%2Fcore , /@motion-canvas%2Fffmpeg , /@revideo%2Fcore , /gsap , /lottie-web , /@lottiefiles%2Fdotlottie-web , /roughjs , /three , /playwright , /svgo , /@resvg%2Fresvg-js , /@hyperframes%2Fcore , /@fontsource%2Fcaveat (and kalam, reenie-beanie, gaegu, homemade-apple, patrick-hand, shadows-into-light, rock-salt, special-elite, courier-prime) — queried 2026-10-18 — versions, publish dates, licence fields.
- [17] PyPI JSON — https://pypi.org/pypi/bpy/json , /manim/json , /opentimelineio/json , /fonttools/json , /lottie/json — queried 2026-10-18 — versions, dates, `requires_python`, licences.
- [18] Motion Canvas rendering — https://motioncanvas.io/docs/rendering — 2026-10-18 — editor-driven image-sequence export.
- [19] Motion Canvas repository — https://github.com/motion-canvas/motion-canvas — 2026-10-18 — MIT, 19.4k stars.
- [20] Revideo repository — https://github.com/redotvideo/revideo — 2026-10-18 — MIT, `renderVideo()`, PostHog counting, 4.1k stars.
- [21] Manim Community repository — https://github.com/ManimCommunity/manim — 2026-10-18 — double MIT licence, 41.6k stars.
- [22] HyperFrames — https://github.com/heygen-com/hyperframes and https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md — 2026-10-18 — Apache-2.0, seek-based capture, adapters, commands.
- [23] "HyperFrames: Claude Code Can Now Write and Render Videos" — https://themenonlab.blog/blog/hyperframes-claude-code-writes-renders-videos — 2026-04-19 — feature tour, no production verdict.
- [24] rough.js — https://github.com/rough-stuff/rough — 2026-10-18 — MIT, SVG and canvas.
- [25] rough.js options — https://github.com/rough-stuff/rough/wiki — 2026-10-18 — `seed`, `roughness`, `bowing`, `preserveVertices`.
- [26] GSAP RoughEase — https://gsap.com/docs/v3/Eases/RoughEase/ — 2026-10-18 — `strength`, `taper`, `clamp`, `randomize`.
- [27] MDN `feTurbulence` — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence — 2026-10-18 — attributes and displacement example.
- [28] ambientCG licence — https://docs.ambientcg.com/license/ — 2026-10-18 — CC0.
- [29] SIL Open Font License FAQ — https://openfontlicense.org/ofl-faq/ — FAQ 1.1-update7 (Nov 2023), page updated 2026-01-12 — video titling welcome; do not sell the font alone.
- [30] Playwright clock — https://playwright.dev/docs/clock — 2026-10-18 — fakes Date, timers, rAF.
- [31] Playwright videos — https://playwright.dev/docs/videos — 2026-10-18 — default size scaled to fit 800x800.
- [32] OmniLottie (CVPR 2026) — https://arxiv.org/abs/2603.02138 and the CVPR 2026 supplemental PDFs for OmniLottie and LottieGPT (openaccess.thecvf.com) — search result only, not opened — failure modes of generated Lottie.
- [33] diffusionstudio/lottie ("text-to-lottie" skill with Skottie preview) — https://www.sourcepulse.org/projects/31067832 — search result only.
- [34] Line boil / squigglevision — https://www.premiumbeat.com/blog/how-to-create-line-boil-animations/ and https://www.foxrenderfarm.com/share/what-is-squigglevision/ — search results only, not opened.
- [35] Headless EEVEE history — https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-eevee/1436 and a vendor post https://irendering.net/eevee-next-headless-dilemma-cloud-render-farm-guide/ (October 2026) — search results only, not opened; the vendor claim is unverified.

Real examples
- [36] bishpls/animation-pipeline — https://github.com/bishpls/animation-pipeline — 2026-10-18 — films, stack, five parallel subagents.
- [37] bishpls `docs/CRAFT.md` — https://raw.githubusercontent.com/bishpls/animation-pipeline/main/docs/CRAFT.md — 2026-10-18 — timing, look, review loop, rendering rules.
- [38] claude-code-film-studio (MorShahrezaye) — https://github.com/MorShahrezaye/claude-code-film-studio and https://github.com/MorShahrezaye/claude-code-film-studio/tree/main/films/the-multiplane-camera — 2026-10-18 — 8 h, $207.58, "nothing was auditioned by ear".
- [39] claude-animation-studio — https://github.com/i-afaqrashid/claude-animation-studio — 2026-10-18 — plugin, 20 to 58 s films, MIT.
- [40] "I Generated a Cartoon Video Entirely from the Command Line" — https://ruidiao.substack.com/p/i-generated-a-cartoon-video-entirely — 2026-10-18 — 52 s, local Qwen and Wan2.2.
- [41] "How I make custom motion graphics using Claude Code + Remotion" (Louise de Sadeleer) — https://louisedesadeleer.substack.com/p/how-i-make-custom-motion-graphics — 2026-10-18 — "the bottleneck shifts from technical skill to taste".
- [42] "Making Videos with Claude Code and Remotion" — https://blog.openreplay.com/making-videos-claude-code-remotion/ — 2026-10-18 — Sequence offsets, linear interpolate, "the second render".
- [43] scuti.asia 18-second intro write-up — https://scuti.asia/?p=23313 — 2026-10-18 — storyboard, build, critic; `window.seekTo(t)`.
- [44] Third-party Remotion skill listing warning about generic motion — https://claudemarketplaces.com/skills/kimny1143/claude-code-template/remotion — search result only.
- [45] Claude and Blender MCP review — https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance — search result only.

Claude Code and environment (docs read 2026-10-18)
- [46] Advanced setup — https://code.claude.com/docs/en/setup — Windows install routes, requirements, sandboxing support.
- [47] Remote Control — https://code.claude.com/docs/en/remote-control — commands, requirements, limitations.
- [48] Computer use in the CLI — https://code.claude.com/docs/en/computer-use — macOS only.
- [49] Cloud environments — https://code.claude.com/docs/en/cloud-environments — resources, network levels, allowed domains, network secrets, caching.
- [50] Claude Code on the web — https://code.claude.com/docs/en/claude-code-on-the-web — cloud sessions, expiry, limits.
- [51] Data usage — https://code.claude.com/docs/en/data-usage — retention 5 years vs 30 days, training, Remote Control sync.
- [52] MCP — https://code.claude.com/docs/en/mcp — `claude mcp add` syntax, output limits.
- [53] Windows memory reports — https://github.com/anthropics/claude-code/issues/24840 , /issues/42169 , /issues/32304 , /issues/25545 , /issues/33356 ; https://dev.ua/en/news/claude-na-windows-masovo-pohlynaie-operatyvnu-pamiat-bez-mozhlyvosti-tse-zupynyty-1781185611 — search results only, not opened.

Git and storage
- [54] GitHub Docs, Git LFS billing — https://docs.github.com/en/billing/concepts/product-billing/git-lfs — 2026-10-18 — quotas, packs removed, metered.
- [55] GitHub Docs, About Git LFS — https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage — 2026-10-18 — 2/2/4/5 GB file limits.
- [56] GitHub Docs, About large files — https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github — 2026-10-18 — 50/100 MiB, 1 GB guidance.
- [57] GitHub changelog — https://github.blog/changelog/2024-06-03-new-enterprise-accounts-have-metered-billing-for-git-lfs/ — 2024-06-03 — $0.07 and $0.0875.
- [58] LFS to metered billing FAQ — https://github.com/orgs/community/discussions/61362 — read 2026-10-18 — data packs discontinued, free quotas.
- [59] Backblaze B2 pricing — https://www.backblaze.com/cloud-storage/pricing — 2026-10-18 (footer 2024) — $6.95 per TB-month.
- [60] rclone crypt — https://rclone.org/crypt/ — 2026-10-18 — cipher, name encryption, warnings.
- [61] BitLocker overview — https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/ — page date 2026-08-24, updated 2026-10-08 — editions; device encryption excludes USB drives.
- [62] Cryptomator — https://cryptomator.org/ — 2026-10-18 — client-side vaults.
- [63] VeraCrypt — https://veracrypt.io/en/Home.html — 2026-10-18 — 1.26.29, 2026-06-09.
- [64] Hetzner Storage Box — https://www.hetzner.com/storage/storage-box/ — 2026-10-18 — protocols and locations; prices not shown.

Generation prices
- [65] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing — page updated 2026-10-16 — image, Veo, batch, announced increases.
- [66] Replicate pricing — https://replicate.com/pricing — 2026-10-18 (undated) — GPU and per-output rates.

First-hand
- [67] Container measurements M1 to M21 — this session, 2026-10-18; scratch files under the session scratchpad (not kept in the repo); method and numbers in Findings Q3.
- [68] EffectCraft v0.11.1 source (shallow clone, read only) — https://github.com/storytold/effectcraft tag `v0.11.1` — `apps/effectcraft-cli/src/main.rs`, `docs/agents.md` — 2026-10-18 — exact `render`, `render --template`, `bench`, `mcp` syntax; alpha read-back note.

---

## Follow-up research (round 1)

Researcher: Sonnet, 2026-10-18. Scope: the eight follow-ups from `reviews/agent-pipeline-round1.md` section 4. Everything below was read or run on 2026-10-18. New sources continue the numbering at [69]; new first-hand measurements continue at M22. Anything I could not confirm is marked UNVERIFIED.

### Answers in brief

1. **winget ids are verified from the manifests.** `Gyan.FFmpeg` (full build, **FFmpeg 9.0.2**), `Python.Python.3.13` (3.13.15) and `Git.Git` (2.55.0.5). The PC will run **ffmpeg 9.x**, the container runs 6.1.1: three majors apart.
2. **The colour-patch test, re-run on the exact winget build, changes the recommended command line.** (a) The "format first" chain `format=yuv420p,scale=out_color_matrix=bt709:out_range=tv` is *not* the safe one: it fails the review's own tolerance (up to 5/255 RGB error, probably from converting twice) on 6.1.1 *and* on 9.0.2. (b) The "reordered" chain `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p` was correct on every build I ran (error 1/255 for 8-bit input, 3/255 for 16-bit input), including 6.1.1, where the review recorded Y = 81. I could not reproduce that. (c) Since ffmpeg 7.1 the bare `-pix_fmt yuv420p` plus tags now converts with BT.709 (it did not on 6.1.1), but **`-color_primaries` and `-color_trc` are no longer written into the stream**; they come out `unknown`. A trailing `setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv` fixes the tags on all builds tested. Details and the new standard chain are in Q-F1.
3. **S4 (does a background job keep a VM awake) is still not answered by any document I could read.** New documented facts: a background command in a cloud session has a 30-minute default time limit (up to 2 hours via `timeout`), and a pause or reclaim still ends it. Keep spike S4 as scoped.
4. **Image attachments in cloud sessions are still not stated.** They are documented for the Desktop app and for Remote Control sessions only. UNVERIFIED for claude.ai/code cloud sessions; one-minute test given below.
5. **Blender's licence is read from blender.org.** Source is "GNU GPL Version 2 or later"; binaries are distributed under GPL v3 or later; "What you create with Blender is your sole property."
6. **Veo has no published batch price**, and the Batch API pages do not list Veo. Budget Veo at list price. Replicate's own pages show **no price** for Kontext or Qwen-Image-Edit; third-party aggregators say about $0.04 to $0.05 per edit (UNVERIFIED).
7. **`cdn.playwright.dev` is not blocked from this container.** Playwright 1.64.1 plus Chromium 156 installed and launched here. The HTTP 400 came from the bare host root and from two URL forms the installer does not use for the new Chrome for Testing builds; the form it does use answers 200. Under the default **Trusted** network level the hosts are not on the documented allowlist (inference, UNVERIFIED).
8. **Hetzner Storage Box prices cannot be read from a static fetch** (the page fills them in with a script). Third-party aggregators list BX11 1 TB at EUR 3.20, BX21 5 TB at EUR 10.90, BX31 10 TB at EUR 20.80 per month, net of VAT (UNVERIFIED, dated unknown). BX41 (20 TB) unknown.
9. **Memory: not measurable from here.** No tab measurement and no Windows measurement exist; I give published anecdotes, one Linux proxy (a one-shot `claude -p` peaked at 256 MB), and a 15-minute measurement recipe for the PC.

### Q-F1. Windows install ids, the ffmpeg major they install, and the colour-patch test on that build

**Verified ids (read from the winget-pkgs manifests, not from memory) [69][70][71][72].**

| Tool | Command | Installs | Notes from the manifest |
|---|---|---|---|
| ffmpeg, full build | `winget install --id Gyan.FFmpeg -e` | **9.0.2** (release date 2026-09-20), zip with nested portable install, x64; exposes `ffmpeg`, `ffplay`, `ffprobe` as command aliases | Licence GPL-3.0; moniker `ffmpeg`, so plain `winget install ffmpeg` should resolve to it; the explicit `--id` form is safer. `ffmpeg -version` printed `9.0.2-full_build-www.gyan.dev`, built with gcc 16.2.0, libavutil 61.1.102 [73] |
| ffmpeg, smaller build | `winget install --id Gyan.FFmpeg.Essentials -e` | newest manifest I found is **9.0.1** (2026-08-12); a 9.0.2 manifest URL answered 404 | The directory listing page said "View all files", so it may be truncated. Also `Gyan.FFmpeg.Shared` (9.0.2, needs the DLLs on PATH) |
| Python 3.13 | `winget install --id Python.Python.3.13 -e` | **3.13.15** (2026-08-05), `burn` installer, x64 / x86 / arm64, user or machine scope | Manifest switches include `InstallAllUsers=0 PrependPath=1`; commands `py`, `python`, `pythonw`, `pyw`. The container has 3.13.16 (M1): same minor |
| Git for Windows | `winget install --id Git.Git -e` | **2.55.0.5** (2026-08-20), Inno installer, x64 and arm64, user or machine scope | Licence listed GPL-2.0. Release notes in the manifest: "Windows 8.1 support will be dropped after Git for Windows v2.55" |

I did not run `winget` itself (Linux container). Whether the maker's winget client is recent enough for zip-with-portable packages is UNVERIFIED; Windows 11 and current Windows 10 ship it, but check with `winget --version` in the week-1 doctor step.

**Which ffmpeg runs the test (M22).** I downloaded `ffmpeg-9.0.2-full_build.zip` from the URL in the winget manifest; its SHA-256 `759d0a9831c436a0eb331ad36f236c06cb04aaa0005da46571f0e9d3d9206f6b` equals the manifest's `InstallerSha256` (case aside). The Windows `ffmpeg.exe` ran under Wine 9.0 (`wine64`, installed from apt in this container) and was used for every 9.0.2 result below. swscale, zimg and x264 are CPU code, so I expect identical numbers on real Windows; that has not been run on a Windows machine (UNVERIFIED until the maker runs the test on the PC). For bracketing I also ran Gyan's 7.1.1 and 8.1.2 full builds the same way, and the container's native Ubuntu 6.1.1.

**Method (M23).** One 1920x1080 frame of three flat vertical patches: pure red (255,0,0), 50 percent grey (128,128,128), a skin tone (224,172,140). Encode 2 frames with `libx264 -crf 12 -preset veryfast` plus the four tags `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`, through each candidate chain. Read the raw Y of each patch centre from the decoded `yuv420p`; decode back to RGB with `scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24` and report the largest per-channel difference to the source (the review's rule: at most 3/255). Expected 8-bit limited-range Y for BT.709: 62.6 / 125.9 / 171.2; for BT.601: 81.5 / 125.9 / 173.9. The script is about 80 lines of Python 3 plus Pillow; it lived in the session scratchpad and is not kept in the repo (the orchestrator can ask for it to be copied into `pipeline/` for spike S5).

**H.264, 8-bit RGB PNG in (Y of red / grey / skin; worst RGB error out of 255).**

| Chain | Ubuntu 6.1.1 | Gyan 7.1.1, 8.1.2 | Gyan 9.0.2 (winget) |
|---|---|---|---|
| A. `format=yuv420p,scale=out_color_matrix=bt709:out_range=tv` (skill step 8, R7) | 62 / 125 / 169; **5** | same; **5** | 62 / 125 / 169; **5** |
| B. `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p` | 63 / 126 / 171; **1** | same; **1** | 63 / 126 / 171; **1** |
| C. bare `-pix_fmt yuv420p` plus tags | 81 / 126 / 174; **23** (BT.601 under BT.709 tags) | 63 / 126 / 171; **1** | 63 / 126 / 171; **1** |
| D. `zscale=matrix=709:range=limited,format=yuv420p` | 63 / 126 / 171; **1** | (not run) | 63 / 126 / 171; **1** |
| B plus trailing `setparams=...` (below; zscale variant not run with it) | same as B; all four tags written | same as B; all four tags written | same as B; all four tags written |

For 9.0.2 I repeated A to D on six input forms: 8-bit RGB PNG, opaque RGBA PNG, a numbered PNG sequence, 16-bit RGB PNG, raw `rgb24` video, and PNGs piped to `image2pipe`. On 9.0.2 the results were identical in all forms except 16-bit input, where B and C were off by 3, D by 2 and A by 5. The 6.1.1 run on the same six forms gave the same A, B and D numbers (and C stayed at 23 in every form).

**ProRes 4444 with alpha, RGBA PNG in (Y as 10-bit, red / grey / skin; BT.709 expects 250 / 504 / 685, BT.601 expects 326 / 504 / 696).**

| Chain | Ubuntu 6.1.1 | Gyan 9.0.2 |
|---|---|---|
| Bare `-pix_fmt yuva444p10le` plus tags (skill step 8, M12) | 326 / 504 / 696 (BT.601); worst error **25** | 250 / 504 / 685 (BT.709); worst error **0** |
| `format=yuva444p10le,scale=out_color_matrix=bt709:out_range=tv` | 250 / 504 / 685; **0** | 250 / 504 / 685; **0** |
| `zscale=matrix=709:range=limited,format=yuva444p10le` | 250 / 504 / 685; **0** | 250 / 504 / 685; **0** |

Alpha survived (opaque test image gave alpha 255). This confirms the review's finding for 6.1.1 (bare encode is BT.601 under BT.709 tags) and shows the same line is correct on 9.0.2.

**Tags (M24).** `ffprobe -show_entries stream=color_range,color_space,color_transfer,color_primaries`:
- Ubuntu 6.1.1 H.264: `tv, bt709, bt709, bt709` (all four written). ProRes 4444: range `unknown`, the other three `bt709`.
- Gyan 7.1.1, 8.1.2 and 9.0.2 H.264 with the skill's flags: `tv, bt709, unknown, unknown` (7.1.1 and 8.1.2 were read from the `ffmpeg -i` stream line, which shows `bt709/unknown/unknown`). ProRes 4444 on 9.0.2: `tv, bt709, unknown, unknown` (not run on 7.1.1 or 8.1.2). **`-color_primaries bt709 -color_trc bt709` stopped taking effect** (I ran at `-v error`, so I did not check whether a warning is printed). The matrix and range tags still arrive, presumably because the scaler sets them.
- Fixes that restore all four tags on 9.0.2 (each tested): append `setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv` to the filter chain (H.264 and ProRes 4444); or `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0` (H.264 only); or `-x264-params colorprim=bt709:transfer=bt709:colormatrix=bt709:range=tv`. `-movflags +write_colr` did not help. `setparams` also worked on 6.1.1 (H.264: four tags; ProRes: range stays `unknown`, which is that build's ProRes behaviour).

**Why (cited).** The FFmpeg Changelog for the 7.1 release lists "YUV colorspace negotiation for codecs and filters, obsoleting the YUVJ pixel format" [74]; my inference, not stated by the source, is that this is the change that makes the output tags drive the automatic RGB to YUV conversion (row C) and that lets the frame's own unset primaries and transfer override the encoder options. A trac ticket (#11309) that I saw only as a search result (the page itself is behind bot protection) reports `-color_primaries` and `-color_trc` not written in 7.1 while the same command worked in 7.0.2 [75]. The Changelog has no entry about the `scale` filter's matrix options, so "ffmpeg 7.x changed scale-filter colour negotiation" is better stated as "7.1 changed colourspace negotiation for codecs and filters". I did not test 7.0.x.

**Recommended command lines (supersede skill step 8, R7 and Q5 row "Route A capture to editing"; they pass on 6.1.1, 7.1.1, 8.1.2 and 9.0.2).**
- H.264: `-vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v libx264 -crf 18 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`
- ProRes 4444 alpha: `-vf "scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v prores_ks -profile:v 4444` (tested: 9.0.2 and 6.1.1 both give Y 250 / 504 / 685; alpha kept on 9.0.2, not checked on 6.1.1; tags as above).
- These use only built-in filters, so they also work in builds without libzimg; `zscale` stays an alternative where present (Gyan full builds list libzimg).
- Do not describe chain A as "correct"; it lands within 1 to 2 LSB in YUV but fails the review's ±3/255 RGB tolerance on both versions. The review's statement that B gives Y = 81 on 6.1 was **not reproduced** by me on 6.1.1 with any of six input forms; I do not know which input or option the review used. The patch test is the arbiter, so run it again on the PC.
- The validator must read all four tags (range, matrix, transfer, primaries) and also measure the patches, because after 7.1 a command can have correct pixels and missing tags, and before 7.1 the reverse.
- `lj.ps1 doctor` should record `ffmpeg -version` and the patch-test result next to the PC's ffmpeg version; re-run on every ffmpeg upgrade (winget upgrades `Gyan.FFmpeg` by installing the new zip).

### Q-F2. Does a running background job keep a cloud VM awake (spike S4)?

**Not stated.** Re-read pages: Use Claude Code in the cloud, Configure cloud environments, Get started with cloud, Tools reference, Mobile [49][50][76][77][78]. What the docs do say:
- "After a few minutes without activity, a session's VM pauses with its files saved"; the next message restores the same VM; a paused VM can be reclaimed later [49]. "Activity" is not defined. A session "counts as inactive while it waits for you to approve an MCP connector tool call or to sign in to an MCP server" [50].
- On reopening after reclaim, "Not restored: background work that was still running when the VM was reclaimed, such as subagents and shell commands" [50]. The environment cache "keeps what the setup script writes to disk and loses anything that was only running" [49].
- **New:** in "a session that runs unattended, such as ... a cloud session, background Bash and PowerShell commands have a time limit": "A command that Claude starts in the background gets 30 minutes, or the `timeout` Claude passes with `run_in_background`, up to a maximum of 2 hours"; a foreground command that times out and moves to the background gets 30 minutes from the move; the time limit needs Claude Code v2.1.285 or later (the container has 2.1.302) [76]. A background command started by the main conversation "keeps running after a final response, until it exits, is stopped, or reaches its time limit" [76]. That sentence is about the Claude Code process, and says nothing about the VM pause.
- "Closing the tab or navigating away doesn't stop the session. It continues running in the background until Claude finishes the current task, then idles" [80]. That is about an agent turn, not a shell job.
- Third-party (not Anthropic, search results only): a guide states the pause and reclaim facts above and explicitly does not address whether background processes keep a VM awake [81]; an issue-tracker mirror lists a bug "Background tasks killed without TaskStop when session goes idle" that the search summary attributed to the Desktop app's 15-minute idle timeout (page returned 503, not read; UNVERIFIED and not about cloud VMs).

**Design consequence (unchanged but now sharper).** Assume the VM can pause a few minutes after the last agent activity and that a background job is not an activity. Every job must be (1) at most 30 minutes (docs limit) and preferably 10 minutes or less, (2) resumable from files, (3) launched by an agent turn that then polls (with `Monitor` or a bounded wait) so that the session is visibly active. Whether a `Monitor` stream, whose "each output line" is fed back to Claude [76], counts as activity is also UNVERIFIED and goes into S4 as variant (c). I did not run S4 here: it needs the session to sit idle with no agent turn running, which a research subagent cannot do.

### Q-F3. Do claude.ai/code cloud sessions accept image attachments?

**Not stated for cloud sessions. UNVERIFIED.** Evidence, strongest first:
- Remote Control (a local session driven from claude.ai/code or the Claude app): "attach a photo or file in the Claude app or at claude.ai/code ... Claude sees attached photos directly as part of your message"; Claude Code saves photos under `~/.claude/uploads/` and passes other files as `@` references [47][78]. The mobile page puts this under the Remote Control heading, not the cloud heading [78].
- Desktop app feature table: file attachments "Images, PDFs" for Desktop and "Not available" for the CLI; the sentence "attach images, PDFs, and other files to your prompt using the attachment button, or drag and drop" is not scoped to a session type, but the same page says the "+" button (connectors) "is not available in cloud or WSL sessions" and "@mention is not available in cloud or WSL sessions" [77]. That is about connectors and @mentions; it does not say attachments are unavailable.
- The cloud pages I read (web, quickstart, environments) never mention attaching a file or image; the only upload they describe is the repository bundle [50][80]. A third-party guide on cloud sessions says the same [81]. A third-party skill listing claims "Claude Code on the Web has no file-upload widget" (search result only, not opened, not Anthropic) [82].
- This cloud VM has no `~/.claude/uploads/` directory at the moment (the directory may be created on first attachment, so this proves nothing).

**One-minute test for week 1 (maker).** Open a cloud session at claude.ai/code, drag any harmless image (not a family photo) into the prompt, ask the agent to run `ls -la ~/.claude/uploads/` and `file` on whatever path it was told. If it works, note the path; if not, the route is the private repo or the PC. **Either way the project rule stands: real photos are not sent to the cloud unless the manifest says so** (Q8, R2), so attachments matter only for style frames, scans of non-personal material and 768 px proxies the maker has cleared.

### Q-F4. Blender licence text

From the blender.org licence page, as returned by the fetch (re-check the wording on the page before quoting it in a credits slide) [83]:
- "The source code we develop at blender.org is default being licensed as GNU GPL Version 2 or later."
- Some modules use more permissive licences; the page gives Cycles as Apache 2.0.
- Blender's components are compatible with GPL version 3 or later, and binary distributions use that licence: "That is also the license to use for any distribution of Blender binaries."
- "What you create with Blender is your sole property." Output files, including `.blend` files, are "free for you to use as you like", commercially included.
- Python scripts that are published (add-ons) must be shared under a GPL-compatible licence.
The about page says: "You are free to use Blender for any purpose, including commercially or for education" and says nothing about who owns output [83]. For the Tools table: **Blender: GPL-2.0-or-later source, GPL-3.0-or-later binaries, Cycles Apache-2.0; renders and `.blend` files are the maker's own.** The licence of the `bpy` wheel on PyPI was not read (UNVERIFIED; the renders are the same).

### Q-F5. Veo batch pricing, and Replicate prices for likeness-preserving editing models

**Veo.** Gemini pricing page, updated 2026-10-16 UTC [65]: Veo 3.1 Standard (`veo-3.1-generate-preview`) $0.40 per second at 720p and 1080p and $0.60 at 4K; Fast (`veo-3.1-fast-generate-preview`) $0.10 (720p), $0.12 (1080p), $0.30 (4K); Lite (`veo-3.1-lite-generate-preview`) $0.05 (720p), $0.08 (1080p), no 4K. Prices are with audio; free tier "Not available". **The Veo section has no Batch table or column**, and the only batch statement is "Batch API (50% cost reduction)" in the paid-tier feature list, with no model scope. The Batch API page says batch "is priced at 50% of the standard interactive API cost for the equivalent model", lists text, Nano Banana image generation and embeddings, and **does not mention Veo** [84]. The video-generation page I fetched had no batch statement either [84]. Conclusion: no Veo batch price exists in the documents I read; plan at list price and treat any discount as a bonus. Updated cost for 30 clips of 5 s (150 s): Lite 1080p $12.00; Fast 1080p $18.00; Fast 4K $45.00; Standard 1080p $60.00; Standard 4K $90.00 (arithmetic from the table; multiply by takes).

**Replicate editing models. UNVERIFIED.** Replicate's own pages show no price: the model pages for `black-forest-labs/flux-kontext-pro` and `qwen/qwen-image-edit-plus` have none; the image-editing collection shows one price (`prunaai/p-image-edit`, "0.01$"); the pricing page lists only text-to-image per-output prices (flux-1.1-pro and others), nothing for Kontext or Qwen [66][85]. Black Forest Labs' pricing page says "1 credit = $0.01 USD" but its per-model prices are filled in by script; its calculator showed a bare "Rate: $0.048 / image" without naming a model [86]. Third-party aggregators (search-result snippets only) say **FLUX Kontext Pro $0.04 per image on Replicate** (four sites agree) and **Qwen-Image-Edit-Plus about $0.05, Qwen-Image-Edit-2511 about $0.04 on Replicate** (one site); that same site's own page, when I fetched it, said "No provider pricing available", so treat the Qwen figures as weak [87]. Planning numbers, clearly estimates: 300 edits at $0.04 to $0.05 = $12 to $15; with three takes $36 to $45. The first-party figure to prefer is Gemini's: Nano Banana 2.1 at $0.0336 per 1K image ($0.0168 batch) [65]. Both Kontext and Qwen-Image-Edit-Plus pages describe identity preservation ("Maintain identity across multiple edits"; "preserves facial identity across different portrait styles and pose transformations") [85]; whether that holds for a 1970s scan is a test for the vertical slice, not a claim. Re-read the price on the model page's API tab or the maker's Replicate billing screen before any batch.

### Q-F6. Is `cdn.playwright.dev` blocked from the container?

**No (M25, M26).** Probed with HTTP HEAD from this session:
- `https://cdn.playwright.dev/` (bare root): HTTP 400 with Azure headers (`x-ms-request-id`, `x-azure-ref`). That is what the CDN returns for a path-less request, which is probably what the earlier 400 (M3) was; I did not see the original command.
- Old build used by the preinstalled Playwright 1.56.1 (`builds/chromium/1194/chromium-linux.zip`): 307 to `playwright.download.prss.microsoft.com`, then 200, 182,333,649 bytes.
- Playwright 1.64.1 (npm latest, 2026-10-14 [16]) uses Chrome for Testing builds. Its installer code (read from the npm tarball) lists three mirrors (`cdn.playwright.dev/dbazure/download/playwright`, `playwright.download.prss.microsoft.com/dbazure/download/playwright`, `cdn.playwright.dev`) and uses the path `builds/cft/<browserVersion>/linux64/chrome-linux64.zip` for Chrome for Testing builds [88]. Probing by hand for Chromium 156.0.8078.4: the two `dbazure` forms answered 400 (via a 307 for the first), while `https://cdn.playwright.dev/builds/cft/156.0.8078.4/linux64/...` answered 200 (200,345,244 bytes for the browser, 125,797,539 for the headless shell). The installer log (`DEBUG=pw:install`) shows it fetching exactly that last form on attempt #1, and the Playwright ffmpeg helper from `https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1013/ffmpeg-linux.zip`. So the 400s I saw belong to URL forms the installer does not use for these builds.
- End to end: in a scratch directory, `npm i playwright@1.64.1`, then `npx playwright install chromium-headless-shell` (with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD` unset and `PLAYWRIGHT_BROWSERS_PATH` pointed at the scratch directory) succeeded (278 MB including Playwright's ffmpeg build); `chromium.launch` reported browser version 156.0.8078.4, `webgl2` available ("WebGL 2.0 (OpenGL ES 3.0 Chromium)") with SwiftShader flags, a page screenshot was written, launch plus screenshot took 0.51 s.
- Caveat: this session reaches many hosts that the default **Trusted** list does not name (M19). The documented Trusted list [49] includes `microsoft.com`, `packages.microsoft.com` and `*.data.mcr.microsoft.com` but neither `cdn.playwright.dev` nor `playwright.download.prss.microsoft.com`, so in an environment left at **Trusted** the browser download would likely be refused (inference, UNVERIFIED; I cannot change this session's level). Options: set **Custom** and add both hosts, or keep the preinstalled 1.56.1 plus Chromium 141 (works, M3). Upgrading is not needed for the pipeline today; the only reason would be a Chromium feature, so default is **keep 1.56.1**.

### Q-F7. Hetzner Storage Box monthly prices

- The fetched page lists BX11, BX21, BX31, BX41 with "Available storage 1 TB, 5 TB, 10 TB, 20 TB" and each price block is an empty `ho-price-container` element (product keys `ROBOT_1333` to `ROBOT_1336`) that a script fills in, so a static fetch cannot show prices; the docs page on Storage Boxes has no prices and points to the product page [64][89]. (The first-round note said "1, 5, 10, 20 TB plans"; the page I fetched today shows four plans, no BX51.)
- Third-party price comparison pages (search-result snippets only, undated): BX11 EUR 3.20 per month for 1 TB, BX21 EUR 10.90 for 5 TB, BX31 EUR 20.80 for 10 TB, all excluding 19 percent German VAT; nothing found for BX41 [89]. **UNVERIFIED**; a family in a non-EU country pays whatever the order page shows. For a 1 TB to 5 TB archive of scans and masters the cost is a few euros a month; verify at the order page before committing.
- Fit with the decision in Q8: a Storage Box gives a German or Finnish location, SFTP/rsync/Borg/rclone, and nothing is readable by Hetzner if encrypted client-side first (rclone crypt, Borg, Restic) [60][64]. Backblaze B2 at $6.95 per TB-month [59] is the comparison.

### Q-F8. Memory of the claude.ai/code tab and of a short native CLI session on Windows

**Neither could be measured from here** (no Windows machine; a tab needs the maker's login and browser). What exists:

| Item | Evidence | Status |
|---|---|---|
| claude.ai/code tab, Chrome or Edge | No measurement found. One Chrome Web Store listing for a "lite" extension claims long Claude chats use "2-4GB+" of browser memory (search snippet, marketing claim, no test) [91] | **UNVERIFIED**; measure |
| Native `claude` on Windows, baseline | One bug report calls its normal state "~300MB" per Task Manager (#32304, March 2026) [90] | Anecdote, not a measurement protocol |
| Native `claude` on Windows, long and heavy sessions | Reports of 13 GB RSS (#24840, 2.1.39 to 2.1.69), 21.7 GB (#32304, with sub-agents and three COM-based MCP servers), 13 to 14 GB and kernel non-paged pool at 31.5 GB with 3 to 4 concurrent sessions (#42169, up to 2.1.126). All three issues were closed by a bot ("not planned", duplicate) with no maintainer reply or fix version [90] | Real risk for long agent-heavy sessions; **cannot say whether current versions still do it** |
| Linux proxy, this container (M27, M20) | Claude Code 2.1.302 installed through Node (`/opt/node22/bin/claude`): a one-shot `claude -p "Reply with the single word ok."` peaked at **256 MB** resident (process tree, 4.4 s wall); the long-running session I am inside holds about 740 MB after 3 h 46 min | A proxy for a Node-hosted CLI, not for the Windows native build |

**What it means for the choice in Summary 14.** The Windows reports are about long sessions with many sub-agents or MCP servers, which is the pattern this project would use if run on the PC; the cloud session in a tab keeps that process off the PC, so it moves the memory cost to the tab, which is unmeasured. The maker's own constraint (the Desktop app is too heavy) is a different product from both. Until measured, keep the order in Summary 14 and add the measurement below to week 1.

**15-minute measurement for the maker (T-mem).**
1. Close everything else. Note free RAM in Task Manager, Performance tab.
2. Tab: in Edge or Chrome open claude.ai/code on a session with a long transcript (any session, no family material); press Shift+Esc (the browser's own Task Manager), note "Memory footprint" for that tab and the GPU process after 2 minutes and after 15 minutes of scrolling.
3. CLI: in PowerShell run `claude`, give it a 10-minute task (read a repo, run a sub-agent); in a second PowerShell window run `Get-Process claude* | Select-Object Id, @{n='WorkingSetMB';e={[int]($_.WorkingSet64/1MB)}}, @{n='PrivateMB';e={[int]($_.PrivateMemorySize64/1MB)}}` at 1, 5 and 10 minutes, and `Get-Counter '\Memory\Pool Nonpaged Bytes'` once at start and once at the end.
4. Write the four numbers and the Windows build into `maker-pc.json` (R10) so the route is chosen from data. Kill orphaned `claude.exe` processes between runs (#42169 reports orphans).

### Changes the scribes should make elsewhere (from this round)

1. **Replace the H.264 and ProRes 4444 command lines** in `research/agent-pipeline.md` (R7 note 4, Q5 row "Route A capture to editing", M12, M13 note, Risks 8, R8 "Colour matrix" row), `playbooks/agent-pipeline.md` (Templates, Validator "Alpha") and `skills/agent-first-production-pipeline/SKILL.md` (Procedure step 8 and the validators) with the two recommended lines in Q-F1. Remove the sentence "`format=` must come before `scale=`"; it is not supported by my measurements.
2. **Add "tags need `setparams` on ffmpeg 7.1 and later"** to Pitfalls, and make the validator read `color_primaries` and `color_transfer` as well as `color_space` and `color_range`.
3. **Step 2 of the playbook** can now name the packages: `winget install --id Gyan.FFmpeg -e`, `winget install --id Python.Python.3.13 -e`, `winget install --id Git.Git -e` (open a new terminal afterwards so PATH refreshes; not verified here). Close Open questions 17 (ids) and 6 (Playwright CDN) with this section.
4. **Summary 7 / Tools table:** Blender "GPL-2.0-or-later (source), GPL-3.0-or-later (binaries)" with the quote above; remove "(J, not re-read)".
5. **Q4 table:** add the Veo 4K prices and "no batch price published"; add the Replicate editing line as UNVERIFIED with the planning range.
6. **Open questions** that stay open: 2 (S4), 3 (attachments, test given), 11 (memory, recipe given), Hetzner price (order page).

### Sources added in this round

Winget and ffmpeg
- [69] winget-pkgs manifests for Gyan.FFmpeg 9.0.2 — https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Gyan/FFmpeg/9.0.2/Gyan.FFmpeg.installer.yaml , `.../Gyan.FFmpeg.locale.en-US.yaml` , `.../Shared/9.0.2/Gyan.FFmpeg.Shared.installer.yaml` , `.../Essentials/9.0.1/Gyan.FFmpeg.Essentials.installer.yaml` — read 2026-10-18.
- [70] winget-pkgs manifest, Python.Python.3.13 3.13.15 — https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/Python/Python/3/13/3.13.15/Python.Python.3.13.installer.yaml — read 2026-10-18.
- [71] winget-pkgs manifests, Git.Git 2.55.0.5 — https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Git/Git/2.55.0.5/Git.Git.installer.yaml and `.../Git.Git.locale.en-US.yaml` — read 2026-10-18.
- [72] winget-pkgs directory listings (versions) — https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/Gyan/FFmpeg , https://github.com/microsoft/winget-pkgs/tree/master/manifests/p/Python/Python/3/13 , https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/Git/Git , https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/Gyan/FFmpeg/Essentials — read 2026-10-18 (the pages say "View all files": lists may be incomplete).
- [73] Gyan build assets (downloaded, hash-checked for 9.0.2) — https://github.com/GyanD/codexffmpeg/releases/download/9.0.2/ffmpeg-9.0.2-full_build.zip , `.../7.1.1/ffmpeg-7.1.1-full_build.zip` , `.../8.1.2/ffmpeg-8.1.2-full_build.zip`.
- [74] FFmpeg Changelog at tag n9.0.2 — https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/Changelog — 7.1 entry "YUV colorspace negotiation for codecs and filters, obsoleting the YUVJ pixel format" (read through the fetch tool's summary).
- [75] FFmpeg trac ticket #11309 — https://trac.ffmpeg.org/ticket/11309 — search result only (page blocked by bot protection); reported `-color_primaries`/`-color_trc` not written in 7.1, working in 7.0.2.

Claude Code docs re-read 2026-10-18 (in addition to [46] to [51])
- [76] Tools reference — https://code.claude.com/docs/en/tools-reference — Background commands; Time limit for background commands; Monitor.
- [77] Claude Code Desktop — https://code.claude.com/docs/en/desktop — Feature comparison (File attachments); connector and @mention limits in cloud sessions.
- [78] Claude Code on mobile — https://code.claude.com/docs/en/mobile — attachments under Remote Control.
- [79] Claude Code documentation index — https://code.claude.com/docs/llms.txt — searched for idle, pause, lifecycle and keep-alive pages; none exists for Anthropic-hosted cloud VMs. (The Remote Control attach sentence is cited as [47].)
- [80] Get started with Claude Code in the cloud — https://code.claude.com/docs/en/web-quickstart — "Session keeps running after closing the tab".
- [81] "Claude Code Cloud Sessions: What Crosses the VM Boundary" — https://agentpatterns.ai/tools/claude/cloud-sessions/ — third-party secondary source; restates the docs, silent on background jobs and attachments.
- [82] Third-party "uploading-files" skill listing — https://claudeskills.info/skills/oaustegard/claude-skills/uploading-files/ — search result only; not Anthropic.

Licences and prices
- [83] Blender licence and about pages — https://www.blender.org/about/license/ , https://www.blender.org/about/ — read 2026-10-18.
- [84] Gemini API Batch API page and video page — https://ai.google.dev/gemini-api/docs/batch-api , https://ai.google.dev/gemini-api/docs/video — read 2026-10-18; pricing page [65] re-read (updated 2026-10-16).
- [85] Replicate pages — https://replicate.com/qwen/qwen-image-edit-plus , https://replicate.com/black-forest-labs/flux-kontext-pro , https://replicate.com/collections/image-editing , https://replicate.com/pricing [66] — read 2026-10-18; no editing-model prices.
- [86] Black Forest Labs pricing — https://docs.bfl.ai/quick_start/pricing , https://bfl.ai/pricing — read 2026-10-18; "1 credit = $0.01 USD"; per-model prices script-filled.
- [87] Aggregator pages — https://www.getmaxim.ai/bifrost/model-library/compare/replicate/flux-kontext-pro , https://pricepertoken.com/image/model/black-forest-labs-flux-kontext-pro , https://pricepertoken.com/image/model/qwen-qwen-image-edit-plus — search-result snippets; the two pricepertoken pages themselves said "No provider pricing available" when fetched.
- [88] Playwright installer code and browser list — https://registry.npmjs.org/playwright-core/-/playwright-core-1.64.1.tgz (via `npm pack playwright-core@1.64.1`) and https://unpkg.com/playwright-core@1.64.1/browsers.json — read 2026-10-18; plus HEAD probes of `cdn.playwright.dev` and `playwright.download.prss.microsoft.com`.
- [89] Hetzner Storage Box — https://www.hetzner.com/storage/storage-box/ (raw HTML read), https://docs.hetzner.com/storage/storage-box/general/ ; price snippets from https://www.whtop.com/compare/hetzner,servdiscount and similar comparison pages — search result only.

Memory
- [90] Claude Code GitHub issues — https://github.com/anthropics/claude-code/issues/24840 , /issues/42169 , /issues/32304 — opened 2026-10-18; all closed without a maintainer fix. #25545 and #33356 from [53] were not opened.
- [91] Chrome Web Store listing "Claude Lite" — https://chromewebstore.google.com/detail/jjnpgbknaolhhallboicaeeimhdnkdhd — search result only; marketing claim.

First-hand, this round (scratch files under the session scratchpad, not kept in the repo)
- [92] M22 to M28:
  - M22 Gyan 9.0.2 zip downloaded, SHA-256 equals the winget manifest, `ffmpeg.exe -version` run under Wine 9.0.
  - M23 colour-patch matrix: 6.1.1 native; 7.1.1, 8.1.2, 9.0.2 under Wine; H.264 chains A to D on six input forms (9.0.2 and 6.1.1), ProRes 4444 chains on RGBA PNG.
  - M24 tag probes with `ffprobe` for the same files and for `setparams`, `h264_metadata` and `-x264-params` fixes.
  - M25 HTTP HEAD probes of Playwright download hosts and mirrors.
  - M26 `playwright@1.64.1` plus `chromium-headless-shell` install and launch test (Chromium 156.0.8078.4).
  - M27 `claude -p` one-shot peak resident memory (process tree sampled every 0.25 s), Claude Code 2.1.302.
  - M28 Hetzner page raw HTML parse (price elements empty).

---

## Changelog

- **2026-10-18, round-1 review nudges applied (scribe).** M12 marked "tags verified; matrix not verified; corrected 2026-10-18" (the matrix is measured in M23, Q-F1). ProRes 4444 and H.264 command lines replaced with the Q-F1 measured chains (Q5 row, R7 note 4, R7 harness). The review's "`format=` before `scale=`" sentence was not applied: the round-1 follow-up (Q-F1) could not reproduce it and measured format-first H.264 outside tolerance. Colour-patch test added as R8 "Colour matrix" and planted defect in R11 S5. Gemini wording corrected: no image or video model is named in the announced changes, and no batch date is forced (Q4, Risks 15, OQ7). Class A renamed "parameterised photo move"; G4 class-A rule added in R5. `cloud: none` routes to the PC as `pc-render` (R4 step 0), not a stop. R10 gains `run <shot>`, `run-steps`, and a doctor privacy rule. Blender licence read from blender.org [83] (Summary 7, Q1, Tools). EffectCraft issue #340 cited in Q5 with its consequence.
