# Free desktop toolchain and core techniques — research notes

Track: `toolchain` · Researcher: Sonnet · Date checked: **2026-10-18** (all "as of" claims below) · Deadline for the project: 2027-02-27.

**How to read the evidence flags.** Every scriptability claim carries one of three flags.

- **[RUN]** — I ran the command on 2026-10-18 in the cloud sandbox (Ubuntu 24.04, 4 vCPU, no GPU) and inspected the output. Versions actually run: ffmpeg 6.1.1, ImageMagick 6.9.12 (IM6, `convert`), Blender as a Python module `bpy` 5.2.2 (pip, Python 3.13), Inkscape 1.2.2, MLT `melt` 7.22.0, Synfig 1.5.1, Goxel 0.11.0 (under Xvfb), librsvg `rsvg-convert` 2.58.0 [100]. These are older than the newest releases listed in the matrix, so flags/menus can differ slightly on the maker's machine; the commands are long-standing, but the maker should re-run them once on their own install.
- **[DOC]** — stated in the vendor's own documentation that I fetched; not run here.
- **[UNVERIFIED]** — I could not confirm it this session (page blocked, JS-only, or not found). Treat as a to-do for the maker's first session, not as a fact.

**Tool limits this session (matters for the gaps list).** The shared web-search budget was already used up, so every source below was reached by fetching a known official URL directly; I found no new sources by searching. YouTube began rate-limiting my requests (Google "sorry" page) after ~25 page fetches, so exact upload dates and software versions exist only for two videos; the rest carry the "N months ago" text from the channel listing seen on 2026-10-18. Several sites sit behind bot challenges (Pixabay licence page via curl, Freesound, Musopen, Zapsplat, Openverse, FFmpeg's Trac wiki); I did not try to bypass them. Pixabay, Freesound and Sonniss were readable through the WebFetch tool instead.

---

## Summary

1. **Recommended narrow stack (about three tools plus glue).** Blender 5.2 LTS (2.5D parallax, voxel scenes, line-draw reveals, camera moves, headless rendering) + Inkscape 1.4.x (maps, timelines, titles, stroke paths; SVG is plain XML an agent can write) + one video editor for the human finishing pass: Kdenlive 26.08 by default (MLT-based, agent-drivable through `melt`, built-in subtitles and Whisper), or DaVinci Resolve 21 Free if the maker already uses it. Glue that agents drive: ffmpeg and ImageMagick. Everything else in the matrix is "know it exists, use only if a specific need appears". [2][8][24][32]
2. **Scriptability, verified by running.** ffmpeg, ImageMagick, Blender (`bpy`), Inkscape CLI, MLT `melt`, Synfig CLI and Goxel CLI all produced correct output headless on 2026-10-18 (flagged [RUN] throughout). Not verified: GIMP 3 batch Python, Krita headless Python, Glaxnimate's pip module (its Linux wheel failed to import here: it needs Qt 6.10, KDE KF6 and libav 61 libraries), Resolve external scripting, Audacity 4 scripting pipe.
3. **Resolve Free vs Studio, today.** Free (Resolve 21 / "What's New in 21.1") works with "virtually all 8-bit video formats at up to 60fps" up to UHD 3840×2160 and includes collaboration and HDR grading; Studio ($295) adds 10-bit to 120 fps and beyond 4K, the AI Neural Engine (Magic Mask, text-based editing, etc.), extra Resolve FX, noise reduction, film grain, multi-GPU and hardware H.264/H.265 acceleration, and lists a "remote scripting API". [2][3]
4. **Resolve scripting in Free is internal only (best reading).** Blackmagic's README says the API is a "common superset for both the Free and Studio versions" and that Studio-only calls return False in Free; it documents the Console, `Workspace > Scripts`, and a `-nogui` headless launch. A third-party wrapper says external scripting needs Studio ("Free version does not allow API access"). The Studio page lists "remote scripting API" as a Studio feature. Check `Preferences > System > General > External scripting using` on the maker's install. [3][6][7]
5. **MLT is the agent-friendly editing engine.** Kdenlive and Shotcut both sit on MLT; Kdenlive renders by calling `melt`, can "Generate Script" (a `.mlt` file you run with `melt script.mlt`), and Shotcut saves projects as MLT XML. I hand-wrote an MLT XML file with an `affine` Ken Burns filter and rendered it headless with `melt` [RUN]. OpenShot uses its own engine (libopenshot), not MLT. [11][17][18][20][23]
6. **Simplest reliable Ken Burns / 2.5D pipeline.** (a) ImageMagick crop to 16:9 → (b) ffmpeg `zoompan` for single-image moves, or Blender planes at different depths for parallax → (c) PNG sequence → ffmpeg. All steps ran headless. **Verified trap:** `zoompan` stretches a 3:2 photo by ~18% unless you crop to the output aspect first (a circle became 641×541). [RUN][63]
7. **Version drift is real and I hit it repeatedly in one session.** In Blender 5.2: the sequencer API is `strips` not `sequences`, `new_effect()` takes `length` not `frame_end`, video output needs `image_settings.media_type='VIDEO'` before `file_format='FFMPEG'`, and the default view transform is AgX, which desaturates photos (set `Standard`). SVG import lands at 0.0254/90 m per px (a 520 px path became 0.147 m). [RUN]
8. **SVG-centred look without a web app.** Inkscape has no native animation (its own Learn page says so). Working paths: script N SVG frames with `stroke-dasharray`/`stroke-dashoffset` → `rsvg-convert` → ffmpeg (48 frames at 1280 px in 1.9 s) [RUN]; Blender curve bevel-factor reveal and the Grease Pencil **Build** modifier on an imported SVG both rendered headless [RUN]. **Trap:** librsvg ignored `pathLength="1"`, so compute the real path length. [35][65][66]
9. **Voxel look.** MagicaVoxel (Windows/Mac only, GUI only, v0.99.7.2 of 2025-07-12) is the fast hand-modelling tool and has no external CLI; Goxel is cross-platform with a CLI export and, in newer source, a `--script` option. The chain photo → `.vox` (script) → Goxel (`--export x.obj`) → Blender (vertex colours imported) → warm Sun + world light → PNG sequence worked end-to-end [RUN], but axis conventions bite (Blender's OBJ importer assumes Y-up while Goxel and MagicaVoxel are Z-up: my first render was sideways until I passed `forward_axis='Y', up_axis='Z'`) and automatic "luminance → depth" voxelising is a crude relief, not a recognisable room. [56][57][58]
10. **Export in three profiles.** TV/USB/projector: H.264 High, Level 4.1, `yuv420p`, 1080p, AAC-LC 48 kHz stereo, MP4 with `+faststart`, BT.709 tags, and keep each file under 4 GB for FAT32 sticks. Private link: same codec family, `crf 20`, `maxrate 12M` at 1080p (YouTube's own recommendation is 8 Mbps for 1080p25/30). Archive: ProRes 422 HQ in `.mov` and/or FFV1 v3 in Matroska — both appear in the Library of Congress 2025-2026 Recommended Formats Statement — plus PCM 24-bit audio, sidecar SRT, sources, project files and checksums. All commands ran [RUN]. [11][91][92][93][94]
11. **Captions.** Burn-in is the only option that works on every TV and projector; keep a sidecar `.srt`. Kdenlive 26.08 has multiple subtitle tracks, import/export and VOSK/Whisper speech-to-text; Whisper itself is MIT-licensed and prints SRT/VTT from the command line. [12][13][75]
12. **Music with clear terms for a public non-commercial screening plus a private link.** Strongest: Kevin MacLeod / incompetech (CC BY 4.0; his FAQ explicitly allows live productions, streaming and monetised YouTube with credit), Freesound CC0 and CC BY items, Sonniss GDC bundles (royalty-free, no attribution, no AI training), Kenney (CC0). Avoid CC BY-NC for anything that might leave the room. FreePD shut down (2008–2025). The person's own favourite commercial songs are **not** free to put in a film that is shown publicly or uploaded; plan substitutes. [76][79][80][82][83][84]
13. **AI music.** Suno's terms (revised 2026-08-10, effective 2026-09-03): free-tier outputs are for personal, non-commercial use only and Suno assigns no ownership to free users; paid tiers get assignment but no copyright guarantee. Meta's MusicGen weights are CC-BY-NC 4.0 (code MIT). The US Copyright Office published Part 2 on AI-output copyrightability on 2025-01-29 (I did not read its conclusions). [88][89][90]
14. **Photopea is a web app.** Its own page says it runs on your device and uploads nothing, and works offline after loading; that is a vendor claim, not an audit. For family photos prefer GIMP 3.2 or Krita installed locally. [55]
15. **Hardware floor.** Blender 5.x needs at least 4 cores, 8 GB RAM, a 2 GB VRAM GPU with OpenGL 4.3/Vulkan 1.3 (Apple Silicon only on macOS from 5.0). Shotcut asks for 4 cores/8 GB for HD. Resolve's floor was not verified. On a 4-vCPU no-GPU VM, Blender Cycles took ~1.3 s per 640×360 frame at 4 samples; plan draft renders, proxies and overnight batches. [20][30][RUN]

---

## Findings by question

### Q1. Video editors: what free includes/excludes today, MLT underpinnings, and what an agent can drive without a GUI

All statements dated 2026-10-18 unless noted.

| Editor (version, date) | What the free edition includes | What it excludes / fine print | Engine | Agent can drive without a GUI? |
|---|---|---|---|---|
| **DaVinci Resolve 21 Free** (page shows "What's New in 21.1") [2][4] | Edit, Cut, Color, Fusion (VFX/motion graphics), Fairlight (audio), and the new **Photo page** (introduced in 21; which Photo-page tools are Free is not itemised); "virtually all 8-bit video formats at up to 60fps in resolutions as high as Ultra HD 3840×2160"; multi-user collaboration; HDR grading. Official training videos: Edit Part 1 (1h09m), Edit Part 2 (44m), Visual Effects in the Edit Page (30m), Introduction to Color (1h33m), Delivering Content (19m), Introduction to Sound Design (58m), Fusion intro (58m). Training books are for **Resolve 20** (file stamps in their URLs suggest Sep 2025), so some menus differ in 21. [5] | **Studio ($295 "excluding sales tax and shipping")** adds: 10-bit up to 120 fps, resolutions beyond 4K (up to 32K), multi-GPU, hardware-accelerated H.264/H.265 decode/encode, DaVinci AI Neural Engine (Magic Mask, text-based editing, smart reframe, object removal, face recognition, speed warp, Super Scale), ~45 extra Resolve FX (AI UltraNR, etc.), temporal/AI spatial noise reduction, film grain, optical blur, lens correction, stereoscopic 3D, Dolby Vision/HDR10+, IMF/DCP, remote scripting API, Fairlight extras (voice isolation, dialogue separator). Free-edition GPU/RAM floor and Linux codec limits: **[UNVERIFIED]**. [2][3] | Blackmagic proprietary | **Partly.** Internal scripting (Console and `Workspace > Scripts`, Python 3 or Lua) is documented and works across Free/Studio; **external** scripts need Studio (third-party statement; Studio page lists "remote scripting API"). Headless launch `-nogui` is documented in the README (edition not stated). Timelines can be built from agent-written **AAF/EDL/XML/FCPXML/DRT/ADL/OTIO** files through `ImportTimelineFromFile`; render queue and presets are scriptable (`AddRenderJob`, `SetRenderSettings`, `StartRendering`). [3][6][7] |
| **Kdenlive 26.08.2** (released 2026-10-13; 26.12 in development) [8][9] | Everything: GPL, no editions. Windows 10+, macOS 13+ (Silicon/Intel), Linux AppImage/Flatpak. Multi-track timeline, nested sequences, title editor (rounded rectangles, snapping in 26.08), Glaxnimate integration for Lottie titles, keyframes with a curve editor and easing modes, mask effects, rotoscoping effect, **multiple subtitle tracks, import/export, VOSK or Whisper speech-to-text**, proxies, render presets (H.264/AAC MP4, H.265 4K, AV1, VP9, **ProRes 422/422 HQ/444, FFV1, DNxHR**, GIF). [8][10][11][12][13][14] | Hardware-accelerated render presets (NVENC, VAAPI, VideoToolbox) are labelled "experimental". Docs say Windows has "some drawbacks". Kdenlive 26.04.3 notes mention "preventing unwanted command execution on MLT versions below 7.40" — only open project files you or your agents made. [9][11][14] | **MLT** (`melt`) + ffmpeg | **Yes for rendering, partly for authoring.** "Generate Script" saves a `.mlt` render script; run with `melt your_script.mlt` [DOC]. Project files are XML on MLT, but hand-authoring a native `.kdenlive` is version-fragile **[UNVERIFIED]**; safer: agents write plain MLT XML and render with `melt` [RUN] while the human uses Kdenlive for finishing. |
| **Shotcut 26.9.27** (blog dated 2026-09-27: "Auto Duck and Adjustment Clip"; 26.8 "Elements", 26.6 "High Dynamic Range") [19][21] | Everything, free and open source, no editions. Windows 10/11 (Intel/AMD/ARM), macOS 12–27 universal, Linux (Flathub, Snap, AppImage, portable tar). New release roughly every two months; versions are date-based and can be kept side by side. Minimum: 4 cores/8 GB for HD, 8 cores/16 GB for 4K; OpenGL 2.0/Direct3D 11. Preview Scaling and Proxy features for weak machines. [19][20][21] | Licence is not named on the download page (it says free, open source) — **[UNVERIFIED]**. | **MLT**; projects save as **MLT XML** [20] | **Yes in principle:** MLT XML is the native project format (`melt` can render it) — the XML Shotcut writes carries Shotcut-specific properties; running Shotcut's own file through `melt` **[UNVERIFIED]**. Hand-written plain MLT XML ran fine under `melt` [RUN]. |
| **OpenShot 4.0.1** [22][23] | Free, GPL-3 or later; Windows (Store/EXE), Linux (AppImage/Snap/PPA), macOS (Intel listed), Chrome OS. libopenshot 0.7.0 is a C++ library with Timeline, Clip, Keyframe, FFmpegReader/Writer classes. | Simplest feature set; not MLT. Python bindings and the `.osp` project format being JSON are **[UNVERIFIED]** here. | **libopenshot** (own engine) | **Possibly** via libopenshot bindings **[UNVERIFIED]**. Not recommended: smaller ecosystem for our techniques. |

**MLT underpinnings (primary docs).** MLT XML is a list of *producers*, *playlists* (tracks) and *multitracks* (filters and transitions), consumed by *consumers* such as SDL playback, the `avformat` encoder, or the `xml` serialiser. `melt` maps files to producers, accepts filters (`-filter`), transitions/mixers (`-mix 25 -mixer luma`) and consumers (`-consumer avformat:out.mp4 vcodec=libx264`), and can serialise any command-line composition to XML with `-consumer xml:project.mlt`. **Pitfalls found [RUN]:** `melt` defaults to the DV PAL profile (720×576) unless you pass `-profile atsc_1080p_25`; image producers print "The MLT Qt module requires a X11 environment" and fall back (use `xvfb-run -a melt …` if titles or Qt producers are needed); a 3:2 photo letterboxes unless cropped to 16:9 first. [11][17][18]

**Decision rule for the editor slot.** Use whichever of Kdenlive / Resolve Free is already installed and familiar. If both: Kdenlive for agent-assisted assembly, captions and delivery (scriptable through MLT), Resolve only if the maker wants its colour page or Fairlight and accepts that agent help then stops at generated timeline files plus ffmpeg post-processing.

### Q2. Which tools render/export headless, exact entry points, and what cannot (MagicaVoxel)

| Tool | Exact entry point | Status | Notes |
|---|---|---|---|
| **Blender 5.2 LTS** | `blender -b scene.blend -E CYCLES -s 1 -e 250 -o //out/f_#### -a` (arguments run in order; `-f`/`-a` must be last); run scripts with `blender -b -P script.py` (`--python-exit-code 1` to fail loudly) [25][26]. Or `pip install bpy` then `import bpy` — "Blender as a Python module", behaves like `--background` with factory startup [27]. | **[RUN]** via `bpy` 5.2.2; CLI **[DOC]** (I did not execute the `blender` binary) | No threads or `--log` equivalents in `bpy`; one `.blend` per process. Start from `bpy.ops.wm.read_factory_settings(use_empty=True)`. On a GPU-less box Workbench and Cycles-CPU rendered fine (EGL warnings are harmless). |
| **Inkscape 1.4.4** | `inkscape --export-type=png --export-width=1920 --export-filename=out.png in.svg`; objects: `--export-id=ID --export-id-only`; actions: `inkscape --batch-process --actions="select-by-id:route;object-stroke-to-path;export-filename:out.svg;export-plain-svg;export-do" in.svg`; `--shell` for many files; `--actions-file`; `--query-all` [33][34] | **[RUN]** on 1.2.2 (export + actions worked; prints "No GUI available, some actions may fail"). 1.4.4 flags **[DOC]** | Actions only run with `--batch-process` or `--with-gui`. **macOS caveat:** in the official 1.4.3+ `.dmg`, extensions (and Python-based import/export) fail when Inkscape is started from the command line (CVE fix). [32] Inkscape 1.4 added "many new actions" for editing SVG and customising export, also available in the Command Palette. [37] |
| **ImageMagick 7.1.2-34** | `magick in.jpg -gravity center -crop 3840x2160+0+0 +repage out.jpg`; batch: `mogrify -path out/ -resize 3840x -gravity center -crop 3840x2160+0+0 +repage *.jpg` [64] | **[RUN]** on IM6 (`convert`/`mogrify`); IM7 uses `magick` | Linux gets an AppImage only; macOS via Homebrew (`imagemagick-full` for SVG/JPEG XL delegates). [64] |
| **ffmpeg 9.0.2 current (builds 6.1.1 run)** | See recipes R1, R9. Windows builds come from gyan.dev or BtbN; macOS static builds from evermeet.cx (the project ships source only). [62][63] | **[RUN]** | `zoompan`, `xfade` (fade, wipeleft, fadeblack, circleopen, dissolve, …), `subtitles`, `lut3d`, `colorbalance`, `curves`, `noise`, `vignette`, `loudnorm`, encoders `libx264`, `libx265`, `prores_ks`, `ffv1`, `aac`, `flac` all present. |
| **MLT `melt`** | `melt in.mlt -profile atsc_1080p_25 -consumer avformat:out.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p`; serialise: `melt a.jpg out=49 b.jpg out=49 -mix 25 -mixer luma -consumer xml:auto.mlt` [17] | **[RUN]** 7.22.0 | The engine under Kdenlive and Shotcut. |
| **Synfig 1.5.1** | `synfig scene.sif -t png -w 1920 -h 1080 --begin-time 0 --end-time 2s -o out.png` (also `--fps`, `--time`, `--append`) [43] | **[RUN]** — a hand-written `.sif` (XML) rendered 49 frames in 0.3 s. `-t ffmpeg --video-codec` printed usage when I tried it (syntax unconfirmed) → use a PNG sequence + ffmpeg | `.sif` is XML an agent can generate; 50+ layer types, bones, vector tweening. [42] |
| **Glaxnimate 0.6.0** (released 2026-03-03) | `pip install glaxnimate`, then `glaxnimate.model.Document()`, `glaxnimate.io.registry.from_slug("lottie").save(document)` — "without the need of a GUI" [39] | **[DOC]**; import **failed** in my Ubuntu 24.04 sandbox: the Linux wheel links Qt 6.10, KF6 (CoreAddons, Archive, I18n), potrace and libav 61, which were absent. Treat headless use as unproven outside a recent KDE/Qt runtime. | Exports Lottie/TGS, SVG+SMIL, GIF, WebP, raster frames, and (0.6.0) a sequence of SVG frames; **no direct MP4 documented** → frames + ffmpeg. [38][40][41] |
| **GIMP 3.2.6** | `gimp-console -i --batch-interpreter <procedure> -b '<command>' --quit` (reads stdin with `-b -`) [49]. API since 3.0: GObject-Introspection, **standard Python 3** (replaced Python-fu), plus Script-Fu (TinyScheme), JavaScript, Lua; **GIMP 2.10 plug-ins/scripts break**; API stable for all 3.x [47][48] | **[DOC]**; GIMP 3 not installable in the sandbox. The procedure name for Python batch (`python-fu-eval` in 2.10) is **[UNVERIFIED]** for 3.x | For repeatable photo ops prefer ImageMagick [RUN]; use GIMP for hand retouching and masks. |
| **Krita 5.3.4.1** | `krita in.kra --export --export-filename out.png`; animation: `krita --export-sequence --export-filename f.png scene.kra` [52] | **[DOC]** | Python API runs **inside** the GUI process (Scripter docker, plugins) [54]; no documented headless Python — an offscreen-Qt workaround is **[UNVERIFIED]**. Animation render goes PNG sequence → FFmpeg (bundled optionally since 5.2); no transparent video. [53] |
| **Audacity 4.0.1** | Macros (Tools > Apply Macro; "not more than 500 files at a time") and `mod-script-pipe` (named pipe, Python/Perl) [61] | **[DOC]** from the legacy 3.x development manual; whether the pipe module ships in Audacity 4 is **[UNVERIFIED]** | Scripting weakens security; never expose it. **Audio automation is better done in ffmpeg** (`loudnorm`, fades, mixes — [RUN]). |
| **MagicaVoxel 0.99.7.2** | **None.** GUI plus an in-app console (press TAB) with commands such as `size`, `flip`, `scale`. Final render can run "in the background" and Turntable Mode writes `name (frame index).png`. [56] | **GUI-only** | **Workaround:** generate `.vox` files from a script (public RIFF-style spec, v150) and open them in MagicaVoxel for the path-traced render; or export OBJ/PLY and render in Blender; or use Goxel for CLI conversion. [57][58] |
| **Goxel (apt 0.11.0 run; README says 0.15.1)** | `xvfb-run -a goxel in.vox --export out.obj` ; newer source adds `--script FILENAME` (QuickJS JavaScript) and always opens a GLFW window, hence Xvfb on servers [58] | **[RUN]** for `--export` (0.24 s); `--script` **[DOC]** (source only) | Exports obj, ply, png, glTF2, MagicaVoxel, Qubicle; OBJ carries per-vertex colours. |
| **Resolve Free** | Console / `Workspace > Scripts` (internal); `-nogui` launch; external `scriptapp("Resolve")` needs Studio per third-party note [6][7] | **[DOC]/[UNVERIFIED]** | See Q1. |
| **Blockbench, OpenToonz, Friction, OpenShot** | JS plugin API (Blockbench); GUI (others); no documented headless CLI found | **[UNVERIFIED]** | Not in the narrow stack. |

### Q3. Simplest reliable 2.5D parallax and Ken Burns pipeline with free tools; what can be batched

**Pipeline (every step except 2's judgement ran headless):**

1. **Prepare** (batch). Scan or copy at the highest resolution you have; aim for ≥ 1.5× the output width so moves can crop (≥ 2880 px wide for 1080p, ≥ 5760 for 4K). Crop to 16:9 in ImageMagick (R1a). *Verified:* 3000×2000 → `mogrify … -crop 3840x2160` gave 3840×2160 [RUN].
2. **Cut out layers** (semi-batch). *Manual:* GIMP 3.2 or Krita selection → layer mask → export PNG with alpha (best control, nothing leaves the machine). *Assisted:* `rembg i in.png out.png` (MIT, local CLI) for the main subject [73]; SAM 2 (Apache-2.0) for clicking out several objects [74]; Depth Anything V2 for a depth map — **Small is Apache-2.0, Base/Large are CC-BY-NC-4.0** [72]. Filling the background behind a cut-out person *invents pixels*: keep it minimal, keep the original, and obey the charter's "reconstructions are visibly reconstructions".
3. **Move the camera.**
   - *Single image, no layers:* ffmpeg `zoompan` (R1). Crop to the output aspect **first** (verified stretch bug) and pre-upscale (`scale=6000:-1`) because `zoompan` positions on whole pixels [RUN].
   - *Layered parallax in Blender (recommended):* planes at different distances with an emission + alpha shader (no relighting), a camera dolly with the default Bezier ease, `view_transform='Standard'` (R2). 50 frames at 640×360, 4 samples Cycles-CPU took 66 s on 4 vCPUs [RUN].
   - *Layered parallax in any editor:* put layers on separate tracks and keyframe position/scale with larger movement for nearer layers (Kdenlive's Transform effect [15]; the Shotcut and Resolve equivalents are named from memory). Scriptable as MLT XML (R5, `affine` filter keyframes [RUN]).
4. **Render** (batch, resumable). PNG sequence → ffmpeg H.264 or ProRes (R9). Draft at 480p/low samples, final overnight.
5. **Unify look** (batch). One ffmpeg grade chain (R7) over all moves so layers and eras match.

**Batchable:** crop, resize, cut-out generation (rembg/SAM/depth), layer assembly script, camera paths, renders, encodes, grade, loudness. **Human-only:** choosing the crop/face framing, mask QA (hair, glass), inpainting decisions and honesty labelling, timing to music, and approving each person's presence (charter: dignity and consent).

### Q4. SVG-centred look (line-draw reveals, maps, timelines, hand-drawn titles): Inkscape → video without a web app

Inkscape's own Learn page: "Inkscape does not support animation natively but SVG files do." It points to JessyInk, Sozi, Blender, Synfig Studio, Friction, Inka and Krita as ways to animate Inkscape artwork, plus hand-written SMIL/CSS/JavaScript. [35] Practical paths, in order of simplicity:

1. **Script the frames (verified, no 3D, no browser).** Author in Inkscape; each reveal element is a single stroked `<path>` with an `id`. A Python script (R3) reads `d`, computes length (`svgpathtools`), writes N SVGs with `stroke-dasharray="L L"` and `stroke-dashoffset` easing from L to 0, renders with `rsvg-convert -w 1280` (or `inkscape --export-type=png`) and encodes with ffmpeg. 48 frames at 1280×720 rendered in 1.9 s [RUN]. **Trap:** librsvg 2.58 did not honour `pathLength="1"` (browsers do — MDN) so every frame looked fully drawn; use real lengths. [65][66]
2. **Blender, curves.** `bpy.ops.import_curve.svg(filepath=…)`, set `bevel_depth`, keyframe `curve.bevel_factor_end` 0→1, render Workbench: 24 frames 640×360 in ~4 s [RUN]. Scale trap: 1 px ≈ 0.000282 m (consistent with a 90 dpi assumption; measured), so a bevel of 0.02 m swamps the drawing and the camera must be framed from the object's dimensions. The **Trim Curve** geometry node is the node-based alternative (Factor/Length mode; does not support cyclic splines) [29].
3. **Blender, Grease Pencil.** `bpy.ops.wm.grease_pencil_import_svg` + modifier type `GREASE_PENCIL_BUILD` (modes Sequential/Concurrent/Additive; transitions Grow/Shrink/Fade in the Python enum, whereas the 5.2 manual says Grow/Shrink/Vanish — more drift; time modes DrawSpeed/Frames/Percentage) drew an imported SVG progressively in a headless Workbench render [RUN][28]. Grease Pencil is also where **hand-drawn titles** belong if the maker has a pen tablet: "Natural Drawing Speed" replays the recorded stylus speed. Blender recommends a pen tablet for Grease Pencil drawing. [28][30]
4. **Glaxnimate (Lottie / SVG-SMIL / GIF / WebP / frame sequences).** Good for animated icons, lower-thirds and Lottie exports; Kdenlive integrates it for titles (since 22.08). No direct video export is documented, so go via frames. Its docs say it supports most of the extra attributes Inkscape writes, so round-tripping is easy. [14][38][40][41]
5. **Web libraries (concepts only).** CSS `stroke-dashoffset` (Chris Coyier, CSS-Tricks, 2014-02-18, still the clearest explanation) and GSAP **DrawSVGPlugin**; since GSAP 3.13 "100% FREE including all bonus plugins" (Webflow). Capturing browser animation to video needs a headless browser — not tested, and it is the "web app" route the brief wants to avoid. [65][66][67]

**Maps and timelines.** Draw static maps as layered SVG; reveal routes with approach 1; for a timeline, keep one wide SVG and either animate a `transform: translate()` via frames, or pan a Blender orthographic camera over imported curves (parallax between layers comes free). **Hand-drawn titles caveat:** outline-glyph fonts have fills, not centre-line strokes, so a dash-offset reveal will not "write" them. Use a single-line (centre-line) font, trace handwriting with Inkscape's Trace Bitmap / Calligraphy tool, or draw the title in Grease Pencil. [36]

### Q5. Voxel / Minecraft-like look from a photo reference

- **Fastest way to a recognisable object or room: hand-model hero objects with the photo as reference, then assemble a scripted layout.** MagicaVoxel (free for any project, no redistribution; Windows/Mac only; 0.99.7.2, 2025-07-12) is the quickest voxel editor and includes a GPU path-tracing renderer with denoiser, IBL (`.hdr`), Photo mode up to 12000×12000 and Turntable Mode (PNG sequence). On Linux: Goxel (GPL-3, Win/Mac/Linux, layers, ray tracing, exports obj/ply/glTF2/.vox/Qubicle) or Blockbench (free GPL; "use cuboids to get that Minecraft aesthetic"; animation editor; plugin store; Mojang Studios among its users). "Fastest" is my judgement from tool descriptions; **I did not time a human modeller.** [56][58][59]
- **Automatic photo → voxel exists but is crude.** My script (R4) turned a 64×36 downsample into a 21k-voxel brightness-depth relief (bright areas bulge forward); the Goxel→Blender chain rendered it upright with vertex colours [RUN], and the synthetic test scene was recognisable, but it is a blocky relief, not a modelled "room". The MagicaVoxel Viewer's older notes mention importing a greyscale PNG as a heightmap and voxelising `.obj`; a depth-map from Depth Anything V2 would beat luminance. [56][72]
- **Warm lighting and render in Blender (verified settings).** Sun light colour (1.0, 0.78, 0.55), strength 4, angle 8°; world colour (0.9, 0.62, 0.4) strength 0.6; Cycles CPU 24 samples + denoise; `view_transform='Standard'`; 960×540 still in 8 s on 4 vCPUs [RUN]. In-app alternative: MagicaVoxel's path tracer with IBL and denoiser.
- **Export for video.** PNG sequence (turntable or dolly) → ffmpeg; or OBJ/PLY/glTF into Blender for composite with 2.5D layers. `.vox` stores 256 palette colours and one byte per voxel coordinate (so at most 256 per axis per model chunk); the editor's own size limit is **[UNVERIFIED]**. [57]
- **Axis gotchas [RUN].** `.vox` and Goxel's OBJ are Z-up; Blender's OBJ importer assumes Y-up and silently rotates, so call `bpy.ops.wm.obj_import(filepath=…, forward_axis='Y', up_axis='Z')`. When writing `.vox` yourself put picture rows on z and depth on y, or the picture lies flat on the floor (my first two renders). The MagicaVoxel FAQ also warns that exported models are not centred unless `IO > Export > Local` is enabled. [56]

### Q6. Correct export settings: big-screen premiere (laptop or USB stick), private web link, twenty-year archive master, captions

Hard facts first. H.264 level 4.1 covers 1080p at about 30 fps (level 4.2 ≈ 64 fps; 3840×2160 needs level 5.1 at ≈ 31.7 fps), so **1080p H.264 High@4.1 is the safest common denominator**; 4K needs HEVC or level 5.1 and must be tested on the actual display. [95] FAT32 caps a single file at 4 GB − 1 byte [96]; at 12 Mbps video + 256 kbps audio that is ≈ 46 minutes, at 20 Mbps ≈ 28 minutes (my arithmetic) — format the stick exFAT or keep files below the limit and test the TV. Whether a given TV/projector accepts exFAT, MKV or soft subtitles is **[UNVERIFIED]**: no TV maker's spec was readable this session. Always rehearse on the real hardware.

| Deliverable | Container / codec | Command (tested [RUN] on ffmpeg 6.1.1) | Why |
|---|---|---|---|
| **Premiere from laptop (HDMI)** | Play the ProRes/FFV1 master or the MP4 below in VLC/mpv; set the laptop to 1920×1080, mirror displays, turn off notifications/sleep | — | Removes TV decoder risk. Rehearse with the venue's cable/adapter. |
| **USB stick / TV / projector** | MP4, H.264 High@4.1, `yuv420p`, AAC-LC 48 kHz stereo, `+faststart`, BT.709 tags | `ffmpeg -i master.mov -c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart deliver_usb.mp4` (the `-maxrate` pair is my safety margin; I tested the command without it, and `-maxrate 12M -bufsize 24M` in the web variant) | Matches YouTube's own "safe" spec (MP4, moov atom first, H.264 High, 4:2:0, progressive, AAC-LC 48 kHz) and the AVC level table. [91][95] |
| **Private web link** | Same as above, 1080p, lower bitrate | `ffmpeg -i master.mov -c:v libx264 -preset slow -crf 20 -maxrate 12M -bufsize 24M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart web_1080.mp4` | YouTube recommends 8 Mbps (1080p, 24/25/30 fps), 12 Mbps (48/50/60 fps), 35–45 Mbps (4K), stereo audio 384 kbps; "No Edit Lists", moov at front; closed GOP; encode at the recorded frame rate; deinterlace first. [91] |
| **Twenty-year archive master** | **A.** ProRes 422 HQ in `.mov` **and/or B.** FFV1 version 3 in Matroska; audio PCM 24-bit 48 kHz (ProRes file) or FLAC (FFV1 file) | A: `ffmpeg -i master_in.mov -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le -c:a pcm_s24le archive_prores422hq.mov` · B: `ffmpeg -i master_in.mov -c:v ffv1 -level 3 -coder 1 -context 1 -g 1 -slicecrc 1 -c:a flac archive_ffv1.mkv` | The Library of Congress Recommended Formats Statement 2025-2026 lists file-based video in this order of preference: IMF, **FFV1 v3 (RFC 9043) in Matroska**, **ProRes 4444 XQ/4444/422 HQ in QuickTime**, MPEG-2, XDCAM; an MP4 is a "viewing proxy". FFV1 is a lossless intra-frame format specified in an RFC; Matroska is RFC 9559. [92][93][94] |
| **Captions** | Burn-in for the screening file; sidecar `.srt` (and `.vtt` for web); soft-sub MKV for the archive | burn-in: `-vf "subtitles=subs.srt:force_style='FontName=DejaVu Sans,FontSize=28,Outline=2,MarginV=40'"` ; MP4 soft: `-i subs.srt -map 0 -map 1 -c copy -c:s mov_text` ; MKV soft: `-c:s srt` — all three muxed and probed OK | Burned-in text cannot be dropped by a TV; soft MP4 `mov_text` support on TVs is **[UNVERIFIED]**. Generate the first draft with Whisper or Kdenlive's speech-to-text, then proof-read every name and place. [13][75] |

**Also set:** keep the project's frame rate (24/25/30) all the way; never mix variable-frame-rate phone clips into the timeline without converting to constant frame rate (`-fps_mode cfr -r 25`, untested here); loudness `-af loudnorm=I=-16:TP=-1.5:LRA=11` (measured test file went −22.1 → −16.0 LUFS [RUN]); EBU R 128 broadcast target is −23 LUFS, but rooms with a projector and small speakers usually want the louder streaming-style level — test in the room. [97]

**Archive package checklist (20-year view).** Master file(s) + sidecar SRT/VTT + project files (`.blend`, `.kdenlive`/`.mlt`, SVG sources) + original photos/audio + a `README.txt` naming every tool *and version* + licence/credits file + SHA-256 checksums; two physical copies and one off-site; re-verify checksums yearly; migrate when a format dies. Keep the exact `ffmpeg` command lines in the repo.

### Q7. Free music and SFX: licences clearly allowing a public non-commercial screening and a private online link; attribution; AI generators

"Clearly" = I read the licence text myself. Anything else is flagged. **Not legal advice.**

| Source | Licence as read (2026-10-18) | OK for public non-commercial screening + private link? | Attribution |
|---|---|---|---|
| **Kevin MacLeod, incompetech.com** | CC BY 4.0. FAQ: yes for YouTube (monetisable), streaming sites, "live productions", "for something else? Probably". [76] CC BY 4.0 defines "Share" to include **public performance**. [79] | **Yes, clearly.** | Required. Format: `Title` / `Kevin MacLeod (incompetech.com)` / `Licensed under Creative Commons: By Attribution 4.0` / `https://creativecommons.org/licenses/by/4.0/`. In films, put it in the end credits. If a rights-holder asks, remove it where practicable (CC BY 4.0 §3(a)(3)). Beware YouTube Content ID claims on widely re-used tracks (his FAQ has a Content ID article). |
| **Freesound** | Per-sound: CC0, CC BY, CC BY-NC. CC BY-NC "can't earn any money". [80] | **Yes for CC0 and CC BY.** Avoid BY-NC: CC says NC means "primarily intended for or directed toward commercial advantage or monetary compensation", decided case by case — a family showing is almost certainly fine, but the film may travel. [78] | CC BY: title, uploader name, Freesound link and licence ("licensed under CC BY 4.0"); a credits page is fine. CC0: none. |
| **Sonniss GDC Game Audio Bundles** | "Royalty free and commercially usable", unlimited projects, **no attribution**, no resale as SFX, **no AI/ML training**; latest listed page: GDC 2024 (no 2025 bundle; 2026 bundle on gdc.sonniss.com). [82] | Yes (media production use). | None required (appreciated). |
| **Kenney** (game assets; audio packs not checked) | "all game assets on the asset pages are public domain licensed (CC0)". [83] | Yes. | Not required. |
| **Pixabay Content License** | Page covers "Content" generally ("royalty-free images, video, audio and other media"): no attribution needed; cannot sell/distribute content standalone; the summary page did **not** mention Content ID. [81] | Likely yes; read the specific track page. | Not required. |
| **YouTube Audio Library** | Content-ID-safe *on YouTube*; tracks under CC BY need credit in the video description; "YouTube can't give legal guidance … on issues … that can occur off the platform". [77] | Only guaranteed for YouTube. For a premiere file, use only CC BY tracks and copy their licence text. | CC BY: credit in description (generate via "Copy"). |
| **Free Music Archive** | Home page frames FMA as "Discovery / personal use"; per-track CC licences not shown on that page; the "royalty free" language belongs to the paid Tribe of Noise service. [87] | **Check each track page.** | Per licence. |
| **BBC Sound Effects (RemArc)** | "use them in your own personal/educational projects, or licence them for use". [85] Full terms not extracted (JS site). | Personal/private only is the safe reading; a public screening is **[UNVERIFIED]**. | Check terms. |
| **Mixkit** | Separate licences per item type (Stock Music Free, Sound Effects Free); the terms live in a pop-up I could not extract. [86] | **[UNVERIFIED]** | — |
| **FreePD** | **Closed** ("2008–2025", hosting ceased). [84] | Do not rely on mirrors. | — |
| **Musopen, Zapsplat, Openverse, ccMixter** | Pages blocked or not read. | **[UNVERIFIED]** | — |

**The person's own favourite songs.** Commercial recordings need both a *master* licence (the recording) and a *sync* licence (the composition) for a film that is shown publicly or uploaded; an unlisted YouTube link will trigger Content ID. Options, in order of safety: (1) CC0/CC BY substitutes in a similar mood; (2) the maker plays or records the tune themselves or with family (the composition is still protected, the recording is yours — ask a rights professional if it will be shown beyond the family); (3) use the original only in a strictly private, offline home viewing, as the maker's own informed risk; (4) no music, diegetic sound, or the person's own voice. Venue "blanket" music licences cover live/background performance in the venue, not synchronising a song into a film (general knowledge; **[UNVERIFIED]** here).

**AI music generators.** *Suno* (terms revised 2026-08-10, effective 2026-09-03): free/basic users "will only use such Outputs for your lawful, personal and non-commercial purposes", and Suno assigns no ownership to them; Pro/Premier get an assignment of Suno's rights but "makes no representation … that any copyright will vest", and commercial use needs a permitted download (limits by tier). [88] A private family screening sits inside "personal"; a public premiere or open link is murkier — buy a paid month first if you want it. *Meta MusicGen / AudioCraft:* code MIT, **weights CC-BY-NC 4.0** — fine for non-commercial local generation, not for anything commercial. [90] *US Copyright Office AI Part 2 (Copyrightability), 2025-01-29* exists; I did not read its conclusions, so I make no copyright claim. [89] Udio, Stable Audio, Google Lyria status in 2026: **[UNVERIFIED]**. Charter reminder: do not synthesise a voice or "performance" of a real person (living or dead) — principle 4.

### Q8. Reliable free tutorial creators, current versions, and which tutorials cover our techniques

**Method and limits.** I preferred official, dated, versioned text docs. For video I read each creator's channel listing page on 2026-10-18 (title, length, "N months ago") and treated a creator as reliable only if the listing showed recent, non-clickbait, tool-specific work. Exact upload dates and software versions were only retrievable for two videos before YouTube rate-limited me; every other video carries an approximate date ("≈" = relative age on 2026-10-18) and **"version unverified"**. [98][99]

| Creator / source | Tool | Why trust / evidence seen | Currency | Caveat |
|---|---|---|---|---|
| **Blender Studio** (Blender Foundation) | Blender | Official; courses (Customizing Material Assets, Story Tools, 3D Printing, Advanced Facial Rigging) and categories Animation, Geometry Nodes, Lighting, Rendering, Shading [31]; channel shows "Brand New Material Assets in Blender 5.2 LTS" 5:27, ≈3 months ago [98] | Current (5.2 LTS) | Which lessons are free vs subscriber-only: **[UNVERIFIED]** |
| **Blender Guru** (Andrew Price) | Blender | "Beginner Blender Tutorial (2026)" 4:19:10 (≈9 months ago); Donut series refreshed ("How to Scatter in Blender 5.0 (Donut Part 7)" 36:44; "The Basics of Lighting and Rendering in Blender (Donut Finale)" 32:57 ≈10 months ago); "Fundamentals of Lighting in Blender" 43:26 ≈5 months ago [98] | Blender 5.0-era; the same listing still shows "Beginner Blender 4.0 Tutorial" parts (≈2 years old) — **skip those** | Long-form; version of the 2026 beginner course unverified (likely 5.0 — released 2025-11-18 [24]) |
| **Default Cube** | Blender Geometry Nodes | Frequent, short, technique-specific; recent items refer to Blender 5.2 ("Blender 5.2? Okay, here is some free stuff") [98] | Current | Assumes beginner basics; useful for Trim Curve / instancing / voxel-style scatter |
| **Grant Abbitt (Gabbitt)** | Blender modelling | Step-by-step beginner series posted days before the check [98] | Current | Modelling-heavy, not our camera/render techniques |
| **Blackmagic Design training** | Resolve | Official; video series with durations: Edit 1h09m + 44m, Visual Effects in the Edit Page 30m (travelling mattes), Intro to Color 1h33m, Advanced Color 57m, Color Management 31m, Delivering Content 19m, Intro to Sound Design 58m, Intro to Mixing 1h16m, Fusion intro 58m, Motion Graphics in Fusion 1h08m; PDFs "Beginner's Guide to DaVinci Resolve 20", "Editor's Guide…", "Colorist Guide…" with lesson files [5] | Resolve 20 books; videos undated | Menus differ in 21; Studio-only tools appear in lessons |
| **Casey Faris** | Resolve | Weekly Resolve tutorials; colour-grading look series ("What is a Color Grading LOOK?" 4:19 ≈6 months ago; "Why Your Color Grades Don't MATCH" 34:43 ≈5 months ago) [98] | Current | YouTube-creator style (retention hooks); Resolve version unverified; some Studio-only features |
| **Kdenlive manual + Nuxttux Creative Studio** | Kdenlive | The Kdenlive 26.08 manual's own video-tutorial page lists Nuxttux (14 entries) [16]; channel lists "Masking & Transition Effects Editing" 16:44 (≈5 months), "Shape Morphing and Match Cut – Friction Graphics Tutorial" 15:57 (≈6 months), "Import Image Sequence into Kdenlive" 5:52, "Faster Edit with Video Proxy Clips" 4:06, "Render Video with Transparent Background" 2:10 [98]. **"Keyframe Interpolation – Kdenlive Tutorial" 5:34, uploaded 2025-05-29** [99] | Current | Kdenlive version unverified per video |
| **Arkengheist 2.0** | Kdenlive | Listed in the official docs for Rotoscoping, Motion Tracking, Locked-on Stabilization [16]. **"Kdenlive Tutorial – Rotoscoping, what it does, how to use it" 16:09, uploaded 2020-11-21** [99] | **Outdated** (pre-2024; Kdenlive 20.x era UI) | Use for the concept only; check against the 26.08 manual's mask/rotoscoping pages |
| **Logos By Nick** | Inkscape | Weekly Inkscape tutorials, e.g. "Trace A Pencil Sketch Into Vectors with Inkscape" 31:00 (≈1 month ago), "Feather Edges With This Live Masking Technique" 8:13 [98] | Current | Logo/design focus; no animation |
| **Davies Media Design** | GIMP 3 | "Learn GIMP 3.0 Photo Editing for Beginners in 25 Minutes" 25:37; "What's New In GIMP 3.0" 29:43; "GIMP 3.0 Non-Destructive Editing" 5:53 (all ≈1 year ago) [98] | One minor behind (3.2.6 current [46]) | 3.0 → 3.2 added link/vector layers etc. [48] |
| **Audacity (official channel)** | Audacity | "Introducing Audacity 4: New tools & a new look" 5:02 (≈1 month ago) [98] | Current (4.0.1) | Older 3.x videos on the same channel |
| **Text docs (best for version accuracy)** | all | Kdenlive 26.08 manual [11]–[16]; Blender 5.2 LTS manual [25][26][28][29]; Krita 5.3 manual [52]–[54]; Synfig manual 1.5.1 [42]; OpenToonz manual 1.7.1 [45]; Inkscape tutorials incl. **Interpolate**, Tracing, Calligraphy [36]; GIMP community tutorials (Layer Masks, Basic Color Curves, Luminosity Masks) [50] | Dated by manual version | Glaxnimate's manual on the web is **0.5.4** while the app is 0.6.0 [41] |
| **Do NOT use** | Shotcut | A YouTube channel named "ShotCut Video Editor" is **not** the official Shotcut: its listing is one-year-old AI-template ads (e.g. "AI Baby Generator Fun…") [98]. Use the Shotcut site's How-To list and forum. [21] | — | Lookalike channels exist for several tools |

**Coverage matrix (what I could actually point to).**

| Technique | Best verified resource | Gap |
|---|---|---|
| Ken Burns | Our tested R1 (ffmpeg) and R5 (MLT); Kdenlive Transform effect docs [15]; concept [71] | The docs-linked "How to do pan and zoom with Kdenlive" video returned no title on 2026-10-18 (dead or private) — no verified Ken Burns video tutorial |
| 2.5D parallax | Our tested R2 (Blender); concept [71] | **No verified tutorial** found for photo-layer parallax in Blender |
| Masking / rotoscoping | Kdenlive manual masking effects [12][15]; Nuxttux Masking (≈5 mo) and Object Mask [16][98]; Resolve "Visual Effects in the Edit Page" 30m [5] | Rotoscoping video is 2020 (outdated); Resolve Magic Mask is Studio-only |
| Morph transitions | Inkscape Interpolate tutorial [36]; Nuxttux Friction "Shape Morphing" (≈6 mo) [98]; Synfig tweening [42] | No photo-to-photo morph tutorial (that is the `ai-imagery` track's job) |
| Match cuts | Definition and examples [71]; Nuxttux Friction item | No editing-level tutorial verified |
| Keyframing and easing | Nuxttux Keyframe Interpolation (2025-05-29, 5:34) [99]; easings.net [70]; Kdenlive manual keyframes [15]; Blender F-curve docs; twelve principles (slow in/out) [71] | — |
| Line-draw SVG animation | CSS-Tricks (2014-02-18) [65]; MDN [66]; Blender Build modifier and Trim Curve manual pages [28][29]; our R3 | No verified video tutorial |
| Voxelising a photo or scene | MagicaVoxel and Goxel pages [56][58]; our R4 | **No verified tutorial** |
| Photo cut-outs | GIMP 3.0 beginner video (≈1 y) [98]; GIMP "Layer Masks" tutorial [50]; rembg/SAM 2 READMEs [73][74] | — |
| Colour grading by era | Resolve "Introduction to Color" 1h33m [5]; Casey Faris look series [98]; our R7 | No "era look" tutorial verified |
| Sound design and music pacing | Resolve "Introduction to Sound Design" 58m and "Introduction to Mixing" 1h16m [5]; Shotcut 26.9 "Auto Duck" release [21]; Audacity 4 intro [98] | Music-to-picture pacing is a technique, not a tool: see syllabus |
| Captions | Kdenlive Speech-to-Text manual [13]; Whisper README [75]; our R9 | Resolve Free captions: **[UNVERIFIED]** (text-based editing is Studio) |
| Export settings | Resolve "Delivering Content" 19m [5]; YouTube upload settings [91]; LoC [92]; our R9 | TV maker specs not read |

### Q9. Minimum hardware for the recommended stack; what degrades gracefully on a weak laptop

| Tool | Stated floor (source) | How it degrades gracefully |
|---|---|---|
| **Blender 5.2 LTS** | Windows/Linux: 4 cores (SSE4.2), 8 GB RAM, GPU with 2 GB VRAM and OpenGL 4.3 (Vulkan 1.3); recommended 8 cores, 32 GB, 8 GB VRAM. **macOS: Blender 5.0+ needs Apple Silicon**, macOS 13+ (4.5 LTS was the last Intel release). 1920×1080 screen recommended. [30] | Work in Workbench/EEVEE viewport; Cycles on CPU with a few samples + denoiser; render at 50 % resolution scale for drafts; render overnight from the command line. **Measured here [RUN] (4 vCPU, no GPU):** parallax planes 640×360 @ 4 spp Cycles = 1.3 s/frame (50 frames in 66 s); Workbench line-draw 24 frames 640×360 in 4 s; voxel still 960×540 @ 24 spp + denoise = 8 s. At 1080p expect ≈ 9× the pixels; a 30-second 25 fps shot (750 frames) at ≈ 12 s/frame is ≈ 2.5 h — *my extrapolation*. |
| **Kdenlive 26.08** | Windows 10+, macOS 13+, Linux AppImage/Flatpak [8]; CPU/RAM floor **[UNVERIFIED]** | Proxy clips (docs: "Proxy Clips can now be used in preview"), lower-resolution preview, "Generate Script" to render later in batch, encoder threads setting [11][12] |
| **Shotcut 26.9.27** | 64-bit; 2 GHz core for SD, **4 cores for HD, 8 cores for 4K**; 4/8/16 GB RAM for SD/HD/4K; OpenGL 2.0 or Direct3D 11 [20] | "Preview Scaling and Proxy features to help reduce preview lag" (FAQ) [20] |
| **DaVinci Resolve 21 Free** | **[UNVERIFIED]** (Blackmagic's configuration guide was not read). Studio lists multi-GPU and hardware H.264/H.265 acceleration as Studio features, which suggests Free leans on the CPU for long-GOP decode/encode (my inference). [3] | Proxy/optimised media and timeline resolution reduction (names from memory); if the laptop struggles, assemble in Kdenlive and use Resolve only for colour. |
| **Inkscape 1.4.4** | No official floor on the pages read — **[UNVERIFIED]**. Known issue: Wayland docked-tab crash. [32] | Keep documents light (avoid thousands of nodes / heavy blur); the CLI export is cheap (0.2 s per file on my VM) |
| **GIMP 3.2.6** | macOS 11+, AppImage on Debian 13+; no RAM floor stated [46] | Work on 16:9 crops at final size; ImageMagick for batch |
| **Krita 5.3.4.1** | 4 GB RAM minimum, 16 GB recommended; OpenGL 3.0 or Direct3D 11; Windows 8.1+/macOS 10.15+/Linux [51]. Animation keeps all frames in RAM [53] | Not used for long animation here |
| **Synfig 1.5.1** | Dual-core 2 GHz, 2 GB RAM, Win 7+/OS X 10.8+/2012+ Linux [42] | Renders as PNG sequence in seconds for simple scenes [RUN] |
| **MagicaVoxel** | Needs a GPU/driver meeting its path-tracer requirement; "Black screen in the renderer: GPU cards or the driver don't meet the requirement" [56] | Edit in the viewport; render stills at small size; or export to Blender |
| **ffmpeg / ImageMagick** | None stated | `-preset fast`, lower resolution drafts, `-threads` |

**Weak-laptop playbook.** (1) Keep a 960×540 "draft" version of every shot; (2) proxies or preview scaling in the editor; (3) render Blender frames as PNG sequences so a crash only loses one frame; (4) run the heavy renders overnight with the command line; (5) store originals on an external drive, never edit directly from a USB stick; (6) export the final in one pass from the master.

---

## Exemplars / recipes

Each recipe: what it is, why it works, how it was made, what we can reuse. Code is what I ran on 2026-10-18 unless noted. The container is temporary: **commit these to the private repo** (scratch copies in the sandbox are lost).

### R1 — Scripted Ken Burns + dissolve (ffmpeg + ImageMagick) [RUN]
*What:* a still photo becomes a slow push-in/pan with an eased dissolve to the next. *Why it works:* `zoompan` is a pure function of the output frame number, so it is deterministic and batchable; cropping to 16:9 first avoids the 18 % stretch I measured on 3:2 sources; the pre-upscale avoids pixel-snapping jitter (standard workaround; I did not test the un-upscaled case). *Reuse:* wrap in a Python loop over a shot list (photo, move, duration, era grade).
```bash
# a) batch: crop every photo to 16:9 at 3840 px (IM7: use `magick mogrify`)
mogrify -path out/ -resize 3840x -gravity center -crop 3840x2160+0+0 +repage -quality 92 in/*.jpg
# b) push-in 5 s @ 25 fps (crop to the output aspect FIRST; upscale; then zoompan)
ffmpeg -loop 1 -i photoA.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z='min(1+0.0008*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 kbA.mp4
# b2) left-to-right pan at constant zoom 1.15
ffmpeg -loop 1 -i photoB.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z=1.15:x='(iw-iw/zoom)*on/124':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 panB.mp4
# c) 1 s dissolve starting at 4 s (other transitions: wipeleft, fadeblack, circleopen, dissolve ...)
ffmpeg -i kbA.mp4 -i panB.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```
Source: ffmpeg filters docs ([63]; zoompan and xfade sections).

### R2 — Headless 2.5D parallax in Blender from layer PNGs [RUN]
*What:* bg/mid/fg PNGs (with alpha) on planes at different depths; a Bezier-eased camera dolly produces true parallax. *Why it works:* emission+alpha materials keep the photo's pixels untouched; plane size is computed from distance so each layer fills the frame; no GUI. *Tested:* 3 synthetic layers, 50 frames 640×360, Cycles CPU 4 spp = 66 s; first/last frame showed the foreground shifting relative to the midground. *Changes since the first test:* `view_transform='Standard'` added (the first test used the default AgX and colours came out visibly desaturated) and the code was tidied; I then re-ran the code below **verbatim**: 50 frames in 64 s, and a sky pixel read #FCCF97 against the source gradient's #FFD9A0 at the very top, i.e. colour preserved.
```python
# pip install bpy   (Blender 5.2 as a Python module; needs a matching Python, here 3.13)
import bpy, math, os
W = os.path.abspath(os.path.dirname(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 640, 360, 25
sc.frame_start, sc.frame_end = 1, 50
sc.view_settings.view_transform = 'Standard'          # default AgX desaturates photos
def plane_height(dist):                                # fills a 16:9 frame at 50 mm / 36 mm sensor
    return (dist * 36 / 50) / (16 / 9)
def add_layer(name, png, y, margin=1.1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 0))
    o = bpy.context.object; o.name = name
    h = plane_height(10 + y) * margin                  # camera sits at y = -10
    o.scale = (h * 16 / 9, h, 1); o.rotation_euler = (math.radians(90), 0, 0)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(W, 'layers', png))
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(tex.outputs['Color'], em.inputs['Color']); nt.links.new(tex.outputs['Alpha'], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface']); o.data.materials.append(m)
add_layer('bg', 'bg.png', 8, 1.25); add_layer('mid', 'mid.png', 0); add_layer('fg', 'fg.png', -5)
bpy.ops.object.camera_add(location=(-0.4, -10, 0), rotation=(math.radians(90), 0, 0))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 50; cam.data.sensor_width = 36
cam.keyframe_insert('location', frame=1)               # Bezier (eased) by default
cam.location.x = 0.4; cam.keyframe_insert('location', frame=50)
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = os.path.join(W, 'renders', 'p_')
bpy.ops.render.render(animation=True)
```
Then: `ffmpeg -framerate 25 -i renders/p_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p parallax.mp4` [RUN].

### R3 — SVG line-draw to video without a browser (Python + librsvg + ffmpeg) [RUN]
*What:* any single stroked path draws itself with ease-in/out. *Why it works:* dash-array = path length, dash-offset L→0. *Trap fixed:* `pathLength="1"` was ignored by librsvg 2.58 so every frame looked complete; compute real length. 48 frames at 1280 px rendered in 1.9 s; the code below was re-run verbatim (48 PNGs, 1280×720 H.264).
```python
# pip install svgpathtools ; needs `rsvg-convert` (librsvg2-bin) or Inkscape on PATH
import os
from svgpathtools import parse_path
os.makedirs('frames', exist_ok=True)
d = "M 60 300 C 140 80, 240 80, 300 200 S 460 330, 580 60"   # copy the path's d= from Inkscape (XML editor, Ctrl+Shift+X)
L = parse_path(d).length(); n = 48
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 640 360">
<rect width="640" height="360" fill="#f7f1e3"/>
<path d="%s" fill="none" stroke="#222" stroke-width="6" stroke-linecap="round"
 stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f"/></svg>'''
ease = lambda t: t*t*(3-2*t)                                   # smoothstep ease in-out
for i in range(n):
    open('frames/f_%04d.svg' % i, 'w').write(svg % (d, L, L, L*(1-ease(i/(n-1)))))
```
```bash
for f in frames/f_*.svg; do rsvg-convert -w 1280 "$f" -o "${f%.svg}.png"; done   # or: inkscape --export-type=png --export-width=1280 --export-filename=x.png f.svg
ffmpeg -framerate 24 -i frames/f_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p linedraw.mp4
```
*Reuse:* many paths → stagger offsets per path; maps → one path per route; for overlays keep the PNG sequence with alpha and bring it into the editor.

### R3b — Same reveal inside Blender [RUN]
Curves: `bpy.ops.import_curve.svg(filepath=…)`; then `curve.bevel_depth ≈ 0.0012` (SVG imports at ~0.000282 m/px), `curve.bevel_factor_mapping_end='SPLINE'`, keyframe `curve.bevel_factor_end` 0→1, orthographic camera framed from `object.dimensions`, Workbench flat render (24 frames 640×360 in ~4 s). Grease Pencil: `bpy.ops.wm.grease_pencil_import_svg(filepath=…)`; `m = obj.modifiers.new('Build','GREASE_PENCIL_BUILD'); m.mode='CONCURRENT'; m.transition='GROW'; m.time_mode='PERCENTAGE'`; keyframe `m.percentage_factor` 0→1. Raise `curve.resolution_u` for smoother bends (the default looked polygonal). See [28][29].

### R4 — Photo → voxel relief → Goxel → Blender warm render [RUN, with caveats]
*What (all three code blocks below were re-run verbatim):* an end-to-end automated chain that proves each hand-off works. *Why only a recipe, not a look:* depth comes from brightness (bright areas bulge toward the camera), so it is a relief, not a modelled room; use it as the plumbing for hand-modelled hero objects (export OBJ/PLY from MagicaVoxel/Goxel, then the same Blender step). A depth map from Depth Anything V2 would be a better depth source than brightness. *Orientation lessons:* `.vox` is Z-up; keep picture rows on z and depth on y; Blender's OBJ importer needs `forward_axis='Y', up_axis='Z'`.
```python
# photo2vox.py  — writes MagicaVoxel .vox (spec: RIFF-style chunks MAIN/SIZE/XYZI/RGBA, version 150) [57]
import struct, sys, numpy as np
from PIL import Image                                   # pip install pillow
src, out = sys.argv[1:3]; W, H, DEPTH = 64, 36, 16
im = Image.open(src).convert('RGB').resize((W, H), Image.LANCZOS)
q = im.quantize(colors=64, method=Image.MEDIANCUT); pal = q.getpalette()[:64*3]; idx = np.array(q)
lum = np.array(im.convert('L'), dtype=float) / 255.0
# x = image x, z = image row (flipped so the top of the photo is up), y = depth: relief grows toward -y
vox = [(x, DEPTH-1-d, H-1-row, int(idx[row, x]) + 1) for row in range(H) for x in range(W)
       for d in range(1 + int(lum[row, x] * (DEPTH-1)))]          # colour index is 1-based
chunk = lambda cid, c, ch=b'': cid + struct.pack('<ii', len(c), len(ch)) + c + ch
size = chunk(b'SIZE', struct.pack('<iii', W, DEPTH, H))          # x, y (depth), z (up)
xyzi = chunk(b'XYZI', struct.pack('<i', len(vox)) + b''.join(struct.pack('<4B', *v) for v in vox))
rgba = b''.join(bytes((*pal[i*3:i*3+3], 255)) if i < 64 else bytes((0, 0, 0, 255)) for i in range(256))
open(out, 'wb').write(b'VOX ' + struct.pack('<i', 150) + chunk(b'MAIN', b'', size + xyzi + chunk(b'RGBA', rgba)))
```
```bash
python photo2vox.py scene.jpg scene.vox
xvfb-run -a goxel scene.vox --export scene.obj          # 0.24 s; OBJ has per-vertex colours (v x y z r g b), Z-up
```
```python
# render_voxel.py — Blender side (bpy 5.2): import, vertex-colour material, warm light, still render (≈8 s at 960x540, 24 spp + denoise)
import bpy, math, os
W = os.path.abspath(os.path.dirname(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=os.path.join(W, 'scene.obj'), forward_axis='Y', up_axis='Z')   # default is Y-up
obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
mat = bpy.data.materials.new('vox'); mat.use_nodes = True; nt = mat.node_tree
ca = nt.nodes.new('ShaderNodeAttribute'); ca.attribute_name = obj.data.color_attributes[0].name   # 'Color'
nt.links.new(ca.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color']); obj.data.materials.append(mat)
sc = bpy.context.scene
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(60), 0, math.radians(-30)))
sun = bpy.context.object; sun.data.energy = 4; sun.data.color = (1.0, 0.78, 0.55); sun.data.angle = math.radians(8)   # warm key
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
bg = sc.world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.9, 0.62, 0.4, 1); bg.inputs['Strength'].default_value = 0.6
dims = obj.dimensions
bpy.ops.object.camera_add(location=(0, -dims.x * 1.5, 0), rotation=(math.radians(90), 0, 0))   # front view from -y
sc.camera = bpy.context.object; sc.camera.data.lens = 50
sc.view_settings.view_transform = 'Standard'; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.filepath = os.path.join(W, 'voxel_still.png'); bpy.ops.render.render(write_still=True)
```
For a turntable (untested): parent the camera to an Empty at the object's centre, keyframe the Empty's Z rotation 0→360°, and render the PNG sequence.

### R5 — A hand-written MLT project rendered by `melt` (agent-driven "editor") [RUN, melt 7.22.0]
*What:* two photos on a playlist; the first has an `affine` filter with keyframed rectangle (Ken Burns); rendered with `melt`. *Why it works:* MLT XML is the native format of Kdenlive/Shotcut's engine; an agent can generate hundreds of shots. *Traps:* pass `-profile atsc_1080p_25` (default is DV PAL 720×576); crop photos to 16:9 first (a 3:2 image letterboxed in my first frame); ignore the "MLT Qt module requires X11" notice or use `xvfb-run -a`.
```xml
<mlt LC_NUMERIC="C" version="7.0.0" profile="atsc_1080p_25">
  <producer id="a" in="0" out="99"><property name="resource">photoA.jpg</property><property name="length">100</property></producer>
  <producer id="b" in="0" out="99"><property name="resource">photoB.jpg</property><property name="length">100</property></producer>
  <tractor id="kb_a" in="0" out="99">
    <multitrack><track producer="a"/></multitrack>
    <filter mlt_service="affine"><property name="transition.rect">0=0 0 1920 1080 1;99=-160 -100 2240 1260 1</property><property name="transition.distort">0</property></filter>
  </tractor>
  <playlist id="main"><entry producer="kb_a" in="0" out="99"/><entry producer="b" in="0" out="99"/></playlist>
  <tractor id="final"><multitrack><track producer="main"/></multitrack></tractor>
</mlt>
```
`melt story.mlt -silent -consumer avformat:story.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p an=1` → 200 frames, 1920×1080. [17][18]

### R6 — Hand-written Synfig scene rendered headless [RUN, Synfig 1.5.1]
A `.sif` (XML, canvas version 1.4) with one `circle` layer and an animated `origin` (two waypoints) rendered with `synfig test.sif -t png -w 480 -h 270 --begin-time 0 --end-time 2s -o out/dot.png` → 49 PNGs in 0.3 s. *Use:* if the maker likes Synfig's vector tweening/bones, an agent can generate scenes and render sequences; we do not recommend adding Synfig to the stack unless a shot needs bone-rigged cut-out animation. [42][43]

### R7 — Era grades as ffmpeg chains [RUN]
```bash
# 1970s: lifted, warm, softly desaturated, grain, vignette
-vf "curves=preset=lighter,colorbalance=rs=.12:gs=.02:bs=-.15:rm=.08:bm=-.08,eq=saturation=0.85:contrast=0.92,noise=alls=14:allf=t+u,vignette=PI/5"
# 1950s black and white: lifted blacks, rolled-off whites, grain
-vf "format=gray,curves=all='0/0.04 0.5/0.5 1/0.94',noise=alls=18:allf=t+u,vignette=PI/4"
# any film-LUT you are licensed to use:  -vf "lut3d=file.cube"
```
Both produced the intended look on a test chart (the warm one visibly faded with a blue-grey shadow tint). Save each era's exact string in the repo so every photo from that decade gets the same treatment. Do not "colourise" black-and-white photos with AI without labelling it a reconstruction (charter principle 4).

### R8 — Blender sequencer as a scriptable editor (and an API-drift specimen) [RUN]
```python
sc.render.image_settings.media_type = 'VIDEO'; sc.render.image_settings.file_format = 'FFMPEG'   # 5.x: media_type first
sc.render.ffmpeg.format = 'MPEG4'; sc.render.ffmpeg.codec = 'H264'; sc.render.ffmpeg.audio_codec = 'NONE'
se = sc.sequence_editor_create(); coll = se.strips                                               # 5.x: `strips` (older: `sequences`)
a = coll.new_movie('A', 'kbA.mp4', channel=1, frame_start=1)
b = coll.new_movie('B', 'kbB.mp4', channel=2, frame_start=100)                                   # 25-frame overlap
coll.new_effect('xf', 'CROSS', channel=3, frame_start=100, length=25, input1=a, input2=b)       # 5.x: `length`, not `frame_end`
```
Rendered a 1920×1080, 224-frame H.264 crossfade in 11 s. Lesson for every scribe: the `new_effect(... frame_end=...)` call and the `FFMPEG` file-format line each threw an exception on my first attempt (the examples I remembered were from earlier versions), and I only avoided a third by checking `dir(sequence_editor)` first. Always run a one-line probe (`dir()`, enum listing) before trusting a remembered Blender snippet.

### R9 — The delivery trio plus verification [RUN]
See Q6 for the three commands. Verify with `ffprobe -v error -show_entries stream=codec_name,profile,level,pix_fmt,width,height,sample_rate,channels -of csv=p=0 file`. Results seen: MP4 `h264,High,level 41,yuv420p,1920x1080` + `aac,LC,48000,2`; ProRes `prores,HQ,yuv422p10le` + `pcm_s24le`; FFV1 `ffv1,…` + `flac`.

### Reference exemplars (third-party, for what to copy)
- **incompetech credit block** (what a compliant credit looks like) [76].
- **Kdenlive "Generate Script" batch rendering** (overnight queue) [11].
- **Blender Studio Overgrown/Cowboi production logs** show how a small team documents a pipeline (channel listing) [98] — read for habits, not for this project's look.

---

## Tools

**Grade legend (Scriptability column).** **A** = runs headless from a script and I ran it. **B** = documented as headless/CLI, not run here. **C** = scripting exists only inside the running GUI. **D** = GUI only. **W** = web service or runtime format. "Verified on" = the date I ran the command or read the doc. Cost is "as of 2026-10-18".

### Tool matrix

| Tool | Role in this project | Version (2026-10-18) | Cost / licence | Platforms | Learning curve (motivated beginner) | Scriptability grade and exact entry point | One-line example | Verified on |
|---|---|---|---|---|---|---|---|---|
| **ffmpeg** | Glue: Ken Burns, transitions, grade, captions, loudness, all encodes, frame-sequence to video | 9.0.2 (2026-09-18; page also lists 8.1.3 dated 2026-09-21) [62]; run: 6.1.1 | Free, open source; builds from gyan.dev / BtbN (Windows), evermeet.cx (macOS) | Win/macOS/Linux | Syntax is steep; agents write it, the maker only runs it | **A** — `ffmpeg …` | `ffmpeg -i in.mov -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -movflags +faststart out.mp4` | 2026-10-18 [RUN] |
| **ImageMagick** | Batch crops, resizes, contact sheets, grain, sepia | 7.1.2-34 AppImage [64]; run: 6.9.12 (`convert`) | Free | Linux AppImage; macOS Homebrew; Windows binaries | Moderate | **A** — `magick` (IM7) / `convert`, `mogrify` (IM6) | `magick in.jpg -gravity center -crop 3840x2160+0+0 +repage out.jpg` | 2026-10-18 [RUN, IM6] |
| **Blender** | 2.5D parallax, voxel scenes, line-draw reveals, camera moves, VSE assembly; the one deep tool | 5.2 LTS (2026-07-14; 5.1 2026-03-17; 5.0 2025-11-18) [24]; run: bpy 5.2.2 | Free, GPL | Win/macOS (Apple Silicon only from 5.0)/Linux | Steep; large payoff; official + creator tutorials are plentiful | **A** — `blender -b file.blend -a`; `blender -b -P script.py`; `pip install bpy` [25][27] | `python -c "import bpy; bpy.ops.wm.read_factory_settings(use_empty=True)"` | 2026-10-18 [RUN via bpy; CLI DOC] |
| **Inkscape** | Maps, timelines, titles, stroke paths, vector cut-outs | 1.4.4 (2026-05-06) [32] | Free, GPL | Win (incl. ARM)/macOS/Linux | Moderate; excellent official tutorials | **A (export/actions)** — `inkscape --export-type=… --export-filename=… in.svg`; `--batch-process --actions=…` [33][34] | `inkscape --export-type=png --export-width=1920 --export-filename=out.png in.svg` | 2026-10-18 [RUN on 1.2.2] |
| **Kdenlive** | Editor of record (default): assembly, subtitles, delivery; agent renders via `melt` | 26.08.2 (2026-10-13) [8][9] | Free, GPL | Win 10+/macOS 13+/Linux | Moderate | **B/A** — render scripts run with `melt`; Generate Script button [11] | `melt your_script.mlt` | 2026-10-18 [DOC; melt RUN] |
| **MLT / melt** | Headless renderer and XML project engine under Kdenlive/Shotcut | 7.22.0 run (MLT ≥ 7.40 recommended for security per Kdenlive notes [9]) | Free (LGPL/GPL) | Win/macOS/Linux | Moderate | **A** — `melt in.mlt -profile atsc_1080p_25 -consumer avformat:out.mp4 …` [17][18] | see R5 | 2026-10-18 [RUN] |
| **DaVinci Resolve (Free)** | Alternative editor/colour/audio; official training | 21 (21.1) [2][4] | Free; Studio $295 [2][3] | Win/macOS/Linux (Linux distro support not verified) | Moderate-steep; best structured training | **C** — Console, `Workspace > Scripts`; `-nogui`; external API needs Studio [6][7] | In-console: `resolve.GetProjectManager()` (README example) | 2026-10-18 [DOC, mirror dated 24 Jul 2026] |
| **Shotcut** | Alternative gentle editor; MLT XML project | 26.9.27 [19][21] | Free | Win/macOS/Linux | Gentle | **B** — MLT XML + `melt` [20] | `melt project.mlt -consumer avformat:out.mp4` | 2026-10-18 [DOC] |
| **OpenShot** | Gentlest editor; not recommended for this project | 4.0.1 [22]; libopenshot 0.7.0 [23] | Free, GPL-3+ | Win/macOS/Linux/ChromeOS | Gentle | **UNVERIFIED** (C++ library; bindings not confirmed) | — | 2026-10-18 |
| **GIMP** | Hand cut-outs, retouching, masks | 3.2.6 (2026-09-10) [46] | Free | Win/macOS 11+/Linux (AppImage, Flatpak, Snap) | Moderate | **B** — `gimp-console -i --batch-interpreter <proc> -b - --quit`; Python 3 API [47][49] | see Q2 | 2026-10-18 [DOC] |
| **Krita** | Painting, masks, frame-by-frame animation | 5.3.4.1 (2026-10-07) [51] | Free, GPL-3 | Win/macOS/Linux (+Android) | Moderate | **B/C** — `krita in.kra --export --export-filename out.png`; `--export-sequence`; Python inside GUI [52][54] | `krita --export-sequence --export-filename f.png scene.kra` | 2026-10-18 [DOC] |
| **Photopea** | Quick edits only; **web app** | Web (no version) | Free to use; pricing and ad terms not read | Browser | Gentle | **W** (embed API exists) | — | 2026-10-18 [55] |
| **Glaxnimate** | Lottie/animated-SVG/GIF/WebP; Kdenlive title animations | 0.6.0 (2026-03-03) [38][40] | Free (KDE) | Win (Store)/macOS Intel+Arm/Linux | Gentle-moderate | **B** — `pip install glaxnimate`; Linux wheel import failed here | see Q2 | 2026-10-18 [DOC; import FAILED] |
| **Synfig Studio** | Vector tweening, bone cut-outs (only if a shot needs it) | 1.5.1 [42] | Free, GPL-3 | Win/macOS/Linux | Steep | **A** — `synfig scene.sif -t png -w W -h H -o out.png` [43] | R6 | 2026-10-18 [RUN] |
| **OpenToonz** | Cel-style 2D animation (Ghibli lineage); skip | 1.7.1 manual [45] | Free (BSD source) | Win/macOS/Linux | Steep | **UNVERIFIED** | — | 2026-10-18 |
| **Friction** | New SVG-centred motion graphics (SMIL export, ECMAScript expressions, FFmpeg render) — watch, don't adopt yet | 1.0.0 (release-candidate links on site) [44] | Free, GPL-3.0 | Win/macOS/Linux | Moderate | **UNVERIFIED** (GUI; in-app expressions) | — | 2026-10-18 |
| **MagicaVoxel** | Fast hand-modelling of voxel objects + path-traced stills/turntables | 0.99.7.2 (2025-07-12) [56] | Free for any project; selling or redistributing the software is disallowed | **Win/Mac only** | Gentle | **D** — GUI + in-app console | generate `.vox` by script (R4) | 2026-10-18 [DOC] |
| **Goxel** | Cross-platform voxel editor/converter | README 0.15.1; apt 0.11.0 run [58] | Free, GPL-3 | Win/macOS/Linux/iOS/Android | Gentle | **A (export)** — `xvfb-run -a goxel in.vox --export out.obj`; `--script` in newer source | R4 | 2026-10-18 [RUN 0.11.0] |
| **Blockbench** | Cuboid "Minecraft-style" models, animation editor, glTF/OBJ | Not read [59] | Free, GPL; also web app | Win/macOS/Linux + web | Gentle | **C** — JavaScript plugins; CLI unverified | — | 2026-10-18 |
| **Audacity** | Voice clean-up, quick edits | 4.0.1 [60] | Free (licence not read) | Win (x64+ARM64)/macOS/Linux AppImage | Gentle | **B/UNVERIFIED** — macros; `mod-script-pipe` documented for 3.x [61] | prefer ffmpeg `loudnorm` | 2026-10-18 |
| **Whisper** | Draft captions and transcripts (also used inside Kdenlive) | CLI/model README [75] | MIT (code and weights) | Python | Moderate | **B** — `whisper audio.flac --model turbo` | `whisper narration.wav --model turbo --output_format srt` (format flag from memory; README shows the plain command) | 2026-10-18 [DOC] |
| **rembg / SAM 2 / Depth Anything V2** | Cut-outs, masks, depth for 2.5D | READMEs [72][73][74] | rembg MIT; SAM 2 Apache-2.0; Depth Anything V2 Small Apache-2.0, **Base/Large CC-BY-NC-4.0** | Python | Moderate | **B** — `rembg i in.png out.png` | — | 2026-10-18 [DOC] |
| **Lottie / Rive / GSAP-CSS-SVG** | Concepts only (no commitment to code): Lottie = open JSON animation spec [69]; Rive = editor + runtime, free plan puts a Rive splash on exports (Cadet $9/seat/mo removes it) [68]; GSAP = free since 3.13 incl. DrawSVG [67]; CSS `stroke-dashoffset` [65][66] | — | see left | Web | — | **W** | — | 2026-10-18 |

### Recommended narrow stack (learn deeply)

1. **Blender 5.2 LTS** — pin this version for the whole project; do not upgrade mid-build (API drift is real, see Summary 7). It covers parallax, voxel/Minecraft-like rendering, line-draw, camera work and headless batches.
2. **Inkscape 1.4.x** — maps, timelines, hand-made stroke titles; plain-text SVG that agents can generate and edit.
3. **One editor — Kdenlive 26.08 by default** (agent-drivable through MLT/`melt`, subtitles, proxies, batch render scripts). Swap in **Resolve 21 Free** only if the maker already works fluently in it and wants its colour and Fairlight tools.
4. **Glue the agents run:** ffmpeg + ImageMagick (+ Python). Raster editing is "use what's installed": GIMP 3.2 or Krita for hand cut-outs (light use). Voxel hero objects: MagicaVoxel (Win/Mac) or Goxel/Blockbench (Linux).
5. **Skip unless a specific shot demands it:** Synfig, OpenToonz, OpenShot, Friction, Glaxnimate, Rive, Audacity (ffmpeg and the editor cover audio).

### "Recognise your apps" checklist (the maker reports back)

The charter says GUI control of the maker's machine isn't connected, so the maker runs these and pastes the output. (Commands are standard but **not run here** on Windows/macOS.)

| App | Where to read the version | Files it makes (so we can recognise them) | Tell us |
|---|---|---|---|
| DaVinci Resolve | Menu `DaVinci Resolve > About` (mac) / `Help > About` (Win/Linux); check `Preferences > System > General > External scripting using` (if it is missing or cannot be set to Local you probably have Free — hypothesis, **[UNVERIFIED]**) | `.drp` project archive, `.drt` timeline (extensions other than `.kdenlive`, `.mlt`, `.kra`, `.blend`, `.vox`, `.svg` are from memory) | Free or Studio; version number |
| Kdenlive | `Help > About Kdenlive` | `.kdenlive` | Version; Flatpak/AppImage/installer |
| Shotcut | `Help > About Shotcut` | `.mlt` | Version (date-based, e.g. 26.9.27) |
| OpenShot | `Help > About` | `.osp` | Version |
| Inkscape | `Help > About Inkscape` | `.svg` | Version (must be 1.x; 1.4.4 current) |
| GIMP | `Help > About GIMP` | `.xcf` | 2.10 or 3.x (3.x scripts differ) |
| Krita | `Help > About Krita` | `.kra` | Version |
| Blender | Splash screen or `Help > About Blender` | `.blend` | Version (LTS 5.2 or other) |
| MagicaVoxel / Goxel / Blockbench | About box | `.vox` / `.gox` / `.bbmodel` | Whether installed |
| Audacity | `Help > About Audacity` | `.aup3` | 3.x or 4.x |
| ffmpeg / ImageMagick | terminal: `ffmpeg -version` and `magick -version` (IM6: `convert -version`) | — | First line of each, or "not found" |

Terminal one-liners to paste back: Windows PowerShell `Get-Command ffmpeg, magick, blender, inkscape, melt -ErrorAction SilentlyContinue | Select-Object Name, Version`; macOS/Linux `which ffmpeg magick convert blender inkscape melt kdenlive shotcut gimp krita; ffmpeg -version | head -1`; Linux packages `flatpak list --app` and `snap list`. Also tell us: OS and version, CPU model and cores, RAM, GPU model, free disk space, and whether a pen tablet exists.

---

## Techniques

Date checked for every resource: **2026-10-18**. "Exact date" only where I could read it. Tags are *tool · version · duration · date*. YouTube links use IDs I saw in channel listings or official docs; I could not open those video pages (rate limit) except where stated.

| # | Technique | How we do it (scripted where possible) | Best free resources found | Practice |
|---|---|---|---|---|
| 1 | **Ken Burns and 2.5D parallax** | R1 (ffmpeg), R2 (Blender planes), R5 (MLT affine) | Concept: Wikipedia "Ken Burns effect", "Parallax scrolling" [71]. Reference: ffmpeg `zoompan`/`xfade` docs, ffmpeg 9.0 era [63]. Kdenlive Transform effect docs · Kdenlive 26.08 manual [15]. **No verified video tutorial** (gap). | Ex 2, 3, 4, 5 |
| 2 | **Masking and rotoscoping** | Editor masks (Kdenlive mask effects, rotoscoping effect), Resolve travelling mattes; GIMP/Krita layer masks for stills; SAM 2 for AI-assisted masks | Kdenlive 26.08 manual masking effects [12][15] · Nuxttux "Masking & Transition Effects Editing – Kdenlive Tutorial" · Kdenlive (version unverified) · 16:44 · ≈May 2026 · `https://www.youtube.com/watch?v=tHzP9kJQJeg` · Nuxttux "Object Mask" (in Kdenlive docs list) · `https://youtu.be/4Pw9b6xhO_k` · Resolve official "Visual Effects in the Edit Page" · Resolve (21-era training page) · 30 min · date n/a [5] · Arkengheist "Rotoscoping" · Kdenlive ~20.x · 16:09 · 2020-11-21 · **outdated**, concept only `https://www.youtube.com/watch?v=gcIKU4KxfLk` [99] | Ex 4 |
| 3 | **Morph transitions** | Vector: Inkscape *Interpolate* extension, Synfig/Glaxnimate path tweening, Friction; raster dissolves: ffmpeg `xfade` (not a true morph) | Inkscape tutorial "Interpolate" · Inkscape 1.x docs · text · date n/a [36] · Nuxttux "Shape Morphing and Match Cut – Friction Graphics Tutorial" · Friction (version unverified) · 15:57 · ≈Apr 2026 · `https://www.youtube.com/watch?v=758rfoR_l1I` · Synfig manual 1.5.1 [42] | Ex 6 (optional) |
| 4 | **Match cuts** | Choose pairs by shape/position across eras; align with an overlay at 50 % opacity (idea, **untested**), hard cut or 0.5 s `xfade` | Definition: Wikipedia "Match cut" — a cut matching composition, action or subject; a **graphic match** matches shapes, colours or movement across a transition, which is the useful form for life-journey era jumps [71]; Nuxttux Friction item above | Ex 4/10 (as a cut) |
| 5 | **Keyframing and easing** | Editor keyframes (Kdenlive curve editor, easing modes); Blender F-curves (Bezier default); R3 uses smoothstep | Nuxttux "Keyframe Interpolation – Kdenlive Tutorial" · Kdenlive ≈25.04 (inferred from date) · 5:34 · **2025-05-29** [99] · easings.net cheat sheet [70] · Kdenlive 26.08 manual: keyframes/auto-keyframe [15], easing modes added in 25.x [12] · Blender 5.2 manual "F-Curve Properties" [101] · "Slow in and slow out" in the twelve principles [71] | Ex 3, 5, 6 |
| 6 | **Line-draw SVG animation** | R3 (Python + librsvg + ffmpeg), R3b (Blender curve bevel / Grease Pencil Build), Trim Curve node | CSS-Tricks "How SVG Line Animation Works" · Chris Coyier · CSS/SVG · text · **2014-02-18** (technique still valid) [65] · MDN `stroke-dashoffset` (`pathLength` normalisation) [66] · Blender 5.2 manual: Grease Pencil Build modifier [28], Trim Curve node [29] · GSAP DrawSVG (free since 3.13) [67] · Logos By Nick "Trace A Pencil Sketch Into Vectors with Inkscape" · Inkscape (version unverified) · 31:00 · ≈Sep 2026 · `https://www.youtube.com/watch?v=72Tb0IMuVps` | Ex 6 |
| 7 | **Voxelising a photo or scene** | Hand-model hero objects (MagicaVoxel/Goxel/Blockbench) from a reference photo; optional auto-relief script R4; assemble and light in Blender | MagicaVoxel page (feature demos linked there; not opened) [56] · Goxel README [58] · Blockbench [59] · `.vox` spec [57] · **No verified tutorial** (gap) | Ex 8 |
| 8 | **Photo cut-outs for 2.5D** | Manual (GIMP/Krita), assisted (rembg, SAM 2), depth (Depth Anything V2) — all local | Davies Media Design "Learn GIMP 3.0 Photo Editing for Beginners in 25 Minutes" · GIMP 3.0 · 25:37 · ≈2025 ("1 year ago") · `https://www.youtube.com/watch?v=pXsP6vNtjck` · GIMP "Layer Masks" community tutorial [50] · rembg, SAM 2, Depth Anything V2 READMEs [72][73][74] | Ex 4 |
| 9 | **Colour grading by era** | Editor colour tools (Resolve Color page is the strongest free option); ffmpeg chains R7; one saved recipe per decade | Resolve official "Introduction to Color" · Resolve (21-era page) · 1h33m · date n/a [5] · Casey Faris "What is a Color Grading LOOK?" · Resolve (version unverified) · 4:19 · ≈Apr 2026 · `https://www.youtube.com/watch?v=xGoBcesIHqk` · GIMP "Basic Color Curves" [50] · R7 | Ex 7 |
| 10 | **Sound design and music pacing** | Voice first, then music bed ducked under it, then room tone/SFX; cut or move title cards on music phrases; markers/guides for chapter beats; loudness at the end (`loudnorm`) | Resolve official "Introduction to Sound Design" 58 min and "Introduction to Mixing" 1h16m [5] · Shotcut 26.9 "Auto Duck" release (2026-09-27) [21] · Audacity "Introducing Audacity 4" · Audacity 4.0 · 5:02 · ≈Sep 2026 · `https://www.youtube.com/watch?v=BTQymidLYIM` · EBU R 128 background [97] · licences in Q7 | Ex 9 |
| 11 | **Captions** | Whisper or Kdenlive speech-to-text for the draft, human proofread, burn-in + sidecar SRT | Kdenlive 26.08 manual "Speech to Text" (VOSK/Whisper) [13] · Whisper README [75] · R9 | Ex 9 |
| 12 | **Export settings (big screen, private link, archive)** | R9 trio; rehearse on the real display | Resolve official "Delivering Content" · Resolve 21-era · 19 min [5] · YouTube recommended upload encoding settings [91] · Library of Congress Recommended Formats Statement 2025–2026 [92] · RFC 9043, RFC 9559 [93][94] · Kdenlive render presets [11] | Ex 10 |

Other free text resources worth a bookmark: Blender Studio training (some courses) [31]; Kdenlive "Import Image Sequence into Kdenlive" 5:52 and "Faster Edit with Video Proxy Clips" 4:06 (Nuxttux, ≈5 months old) for the Blender-frames and weak-laptop workflows [98].

### First 10 exercises (each under two hours; concrete output; self-check)

Practice on **synthetic or stock images and a few non-sensitive family photos**; keep the real hero material for the vertical slice. Put each exercise in `exercises/exNN/` in the private repo and keep every command line.

| # | Exercise (≤ 2 h) | Output file(s) | Self-check |
|---|---|---|---|
| 1 | **Inventory and dry run.** Fill the "recognise your apps" table; install or locate ffmpeg and ImageMagick; batch-crop 5 photos to 3840×2160 (R1a). | `inventory.md`, `photos_16x9/*.jpg` | `ffmpeg -version` prints; `identify -format '%f %wx%h\n' photos_16x9/*.jpg` shows 3840×2160 for all (ratio 1.778). |
| 2 | **Ken Burns by script.** Three photos → three 6 s clips (push-in, pull-out, pan) with R1, joined by 1 s `xfade` dissolves. | `ex02_kenburns.mp4` | `ffprobe` shows 1920×1080, 25 fps, H.264; a circle or round face is **not** squashed (the stretch bug); no visible pixel-shimmer on the slowest move. |
| 3 | **Same in the editor, with easing.** Rebuild ex 2 in Kdenlive (or Resolve): keyframed position/scale with ease-in-out, 1 s dissolves, one proxy-clip pass; export with the USB profile from Q6. | `ex03_editor.mp4`, project file | Speed curve starts and ends gently (scrub the keyframe curve); `ffprobe`: High profile, level 4.1, `yuv420p`, AAC 48 kHz; file opens from a USB stick. |
| 4 | **Cut-outs and fake parallax.** One photo → foreground/midground/background PNGs with alpha (GIMP/Krita, or rembg then hand-fix); animate in the editor with larger move on nearer layers; add one hard match cut to a second photo. | `layers/*.png`, `ex04_parallax_editor.mp4` | Foreground moves ≥ 2× the background; no light halo on cut edges at 100 % zoom; edge feather 1–2 px. |
| 5 | **Parallax in Blender by script.** Run R2 on the ex-4 layers: 480p draft, then 1080p final; `Standard` view transform; PNG sequence → ffmpeg. | `parallax.py`, `ex05_parallax_blender.mp4`, render-time note | A colour swatch in the render matches the source photo (not desaturated); the command runs from a terminal with no GUI; time per frame is written in the note. |
| 6 | **Line-draw route and title.** In Inkscape draw a route or a signature/title as **one stroked centre-line path**; run R3 (or R3b in Blender); add easing. | `route.svg`, `ex06_linedraw.mp4` (and `frames/` PNGs) | The line starts, finishes and eases as designed; the last frame equals the static SVG exported by `inkscape --export-type=png`; the script reads the path length from the file, not a typed number. |
| 7 | **Era looks.** Take 3 photos from three decades (or stock) plus one modern clip; build a look for each decade with R7 or the editor's colour page; save each as a text recipe/LUT. | `looks/70s.txt`, `looks/50s_bw.txt`, `ex07_eras.mp4` | Blacks are lifted and saturation reduced in the older looks (check waveform/scopes or compare histograms); the same recipe applied twice gives identical results (it is a saved string). |
| 8 | **One voxel hero object.** Model one household object from a reference photo in MagicaVoxel (Win/Mac) or Goxel/Blockbench; export OBJ/PLY; import into Blender; warm light (R4 settings); 5 s turntable. | `object.vox` (or `.gox`), `object.obj`, `ex08_turntable.mp4` | A friend who never saw the photo names the object; colours ≤ 32 palette entries; correct way up; renders under 30 s/frame at 960×540 on your machine. |
| 9 | **Sound and captions.** Record 40 s of narration (phone memo is fine), add a CC BY or CC0 music bed (credit text prepared from the licence page), duck the music under the voice, `loudnorm` to −16 LUFS, draft captions with Whisper/Kdenlive and proofread. | `ex09_sound.mp4`, `ex09.srt`, `credits.txt` | `loudnorm` report integrated within ±1 LU of target; captions in sync within ~0.2 s at three spot checks; every name spelled right; the credit block matches the licence's required wording. |
| 10 | **Mini-chapter and delivery rehearsal.** Cut ex 2–9 into a 60–90 s chapter; export the **USB**, **web** and **archive** versions from Q6; play the USB file on the actual TV/projector; write the archive README and SHA-256 checksums. | `chapter_usb.mp4`, `chapter_web_1080.mp4`, `chapter_archive.mov` (or `.mkv`), `README.txt`, `SHA256SUMS` | Plays from the stick with sound and captions; `ffprobe` table matches the profile; `sha256sum -c SHA256SUMS` passes; archive file opens in a second player (VLC/ffplay). |

**Pace suggestion.** Two exercises a week finishes the path by about 2026-11-22 (week 5), leaving roughly 14 of the 19 weeks for the vertical slice and chapters. Re-time after exercise 5, the first Blender render, because that is where weak hardware shows up.

---

## Pitfalls and ethics

**Version drift (the Fable watch-out, with evidence).**
- Blender 5.2: `sequence_editor.sequences` → `strips`; `new_effect(frame_end=…)` → `length=`; `file_format='FFMPEG'` needs `media_type='VIDEO'` first; Grease Pencil Build transition enum is `GROW/SHRINK/FADE` while the manual says Grow/Shrink/Vanish; default view transform AgX; SVG import scale. All hit or observed on 2026-10-18 [RUN][27][28].
- GIMP 3.0 replaced Python-fu with standard Python 3 and broke 2.10 plug-ins; the API is stable across 3.x. Any GIMP script or tutorial from before 2025 needs checking. [47][48]
- Kdenlive: the docs-listed rotoscoping video is from 2020 (Kdenlive 20.x UI); keyframes were reworked in 25.x–26.x (easing modes, curve editor, math expressions in effect values) and a September 2026 status report describes a further keyframe-system refactor ("Parametrized Keyframes") in progress. [9][10][12][99]
- Inkscape 1.4 added "many new command line options" and actions; pre-1.0 flags such as `--without-gui` were removed (the wiki says so), so old forum answers mislead; on macOS the 1.4.3+ dmg disables extensions from the command line. [32][34][37]
- Glaxnimate's web manual is 0.5.4 while the app is 0.6.0. [41]
- Resolve training books are for 20 while the app is 21.1. [5]
- **Rules:** pin the Blender LTS; record every tool version in each project README; before trusting a remembered API snippet run a probe (`dir()`, enum listing, `--help`); tag every tutorial with tool, version, duration, date; treat anything pre-2024 as concept-only.

**"Has a Python API" is not "runs headless".** Krita, Blockbench, Audacity, MagicaVoxel and Resolve Free script *inside* the running GUI. Glaxnimate's pip wheel exists but would not import on Ubuntu 24.04 without Qt 6.10/KF6/libav 61. Goxel opens a window even for `--export` (use Xvfb on servers). Only ffmpeg, ImageMagick, Blender (`bpy`), Inkscape CLI, `melt`, Synfig CLI and Goxel `--export` were proven headless.

**Free-edition fine print.** Resolve Free is 8-bit up to UHD 60 fps, without the Neural Engine tools (Magic Mask, text-based editing…), noise reduction, film grain or hardware H.264/H.265 acceleration; the lessons in Blackmagic's own training mix Free and Studio features. Kdenlive's hardware-encoding presets are experimental. MagicaVoxel is Windows/Mac only and its licence forbids redistributing the app. Rive's free plan stamps a splash screen on exports. Audacity's scripting pipe weakens security.

**Colour and geometry traps (all measured).** AgX default desaturates photos; `melt` defaults to the 601/PAL profile (720×576); 3:2 photos stretch in `zoompan` and letterbox in `melt`; `pathLength` is ignored outside browsers; Blender's OBJ importer assumes Y-up while voxel tools are Z-up; SVG imports at 0.000282 m/px; handwriting fonts are outlines so a dash-offset reveal cannot "write" them.

**Web tools presented as desktop.** Photopea is a web app. Its own page says it "runs completely in your device … does not upload any of your files to the internet" and works offline once loaded, but that is a vendor statement (I did not audit it or read the site's terms, ads or tracking); use GIMP 3.2 or Krita locally for family photos. The same caution applies to any "AI photo animator" website: uploading someone's photos to a third party needs that person's and the photographed people's consent (charter principle 5). Local tools (rembg, SAM 2, Depth Anything V2, Whisper) keep files on the machine after the models are downloaded once. [55][72][73][74][75]

**Security of project files.** Kdenlive 26.04.3 hardened against "unwanted command execution on MLT versions below 7.40", so open only project files you or your agents made, and keep Kdenlive/MLT current; Inkscape's macOS CVE fix (CVE-2025-15523) is why extensions are disabled from the CLI. Download tools only from the official sites (OpenToonz's README warns about look-alike download sites; a look-alike "ShotCut Video Editor" YouTube channel exists). [9][32][45][98]

**Music "royalty-free" claims.** "Royalty-free" does not mean "may be performed publicly" or "no credit". Read the licence page, not the search result: incompetech requires a credit, Freesound CC BY needs title/uploader/link/licence, CC BY-NC invites interpretation, YouTube's Audio Library comfort stops at YouTube, FreePD no longer exists, and several popular libraries blocked my fetch so their terms are unread. Keep a `credits.txt` and a `licences/` folder with a saved copy of each licence page and the download date. Commercial songs from the person's life need sync and master licences for any public or online use. [76]–[90]

**Ethics (charter principles 4 and 5).**
- *Real memories stay real.* Cut-out inpainting, colourising, upscaling and voxelising change or invent pixels. Keep originals untouched, record each AI step in a log, and let the finished film show reconstructed material visibly (for example a consistent vignette or caption style for "reconstructed").
- *No invented people, words or voices.* No synthetic voice or "performance" of a real person, living or dead; no AI music pretending to be a particular artist. AI music (Suno, MusicGen) is fine as an anonymous score if the licence tier fits and the maker discloses it. [88][90]
- *Consent for a room.* A public screening shows other people's faces and stories: ask each living person who is shown, and decide chapters about loss, illness, money or conflict with the family before editing them in.
- *Privacy of working files.* Keep photos and drafts in the private repo or on an encrypted drive; do not put them in cloud tools without a decision; do not publish test renders that contain real photos.
- *Tool-assisted does not mean less honest.* Credit the music and sound sources in the film's end credits as the licences require.

**Operational.** The cloud sandbox is temporary: commit scripts, recipes and text project files to the private repo; keep large masters on the maker's drives (GitHub has file-size limits, **[UNVERIFIED]** exact numbers). Rendering overnight needs a power plan and a sleep-disabled laptop.

---

## Open questions / gaps

1. **The maker's OS, apps and hardware are unknown.** Everything here is conditional until the "recognise your apps" table comes back. If the maker is on Linux, MagicaVoxel is out (Goxel/Blockbench/Blender instead) and Resolve Free may have codec limits; if on Apple Silicon, Blender 5 works but Intel Macs are limited to 4.5 LTS. [30]
2. **Resolve Free:** external scripting status on 21.x, hardware floor, Linux codec limits, whether captions/subtitle tracks are available, and exactly which Photo-page tools are Free — all **[UNVERIFIED]**. Blackmagic's configuration guide and a real Free install would settle this in minutes.
3. **Unverified headless claims:** GIMP 3 batch Python (the procedure name), Krita headless Python, Glaxnimate pip on the maker's OS, Audacity 4 scripting pipe, OpenShot Python/`.osp`, running a Shotcut-saved `.mlt` through `melt`, hand-generating a native `.kdenlive`, the `blender` binary itself (I used `bpy`), EEVEE on a GPU-less machine, the Goxel `--script` option (source only), Synfig's ffmpeg target syntax.
4. **Tutorials.** Exact upload dates and software versions are known for two videos only (YouTube rate-limited me); no verified tutorial exists in my notes for Ken Burns in an editor, 2.5D parallax in Blender, photo-to-voxel, SVG line-draw, photo morphing or "era" grading. A later scribe task should re-fetch channel listings (pace requests) and open each shortlisted video.
5. **Screening hardware.** No TV or projector maker's format specification was readable. Open: exFAT vs FAT32 on the target, MKV and soft-subtitle support, HEVC 4K support, 4:3 vs 16:9 projectors, audio output path, venue HDMI/USB. Plan a rehearsal at the venue.
6. **Licences not read:** Mixkit terms (pop-up), Musopen, Zapsplat, Openverse, ccMixter and FMA per-track terms, BBC SFX full terms, Pixabay's Content ID clause, YouTube Audio Library "standard licence" outside YouTube, whether Suno-style outputs can be shown publicly on a free tier, Udio/Stable Audio/Lyria 2026 terms, and the conclusions of the US Copyright Office AI Part 2 report. Venue music licences versus film synchronisation need a rights professional.
7. **Voxel look.** Human modelling time per object is unmeasured; Blender-native voxel routes (Geometry Nodes, remesh, instancing) and depth-map displacement/camera-projection parallax were not tested; MagicaVoxel under Wine on Linux is unknown.
8. **Hardware floors** for Kdenlive, Inkscape and Resolve Free were not found on the pages fetched.
9. **Search budget.** The shared web-search budget was exhausted before I started, so source discovery relied on known official URLs. Other, possibly better tutorials and tools may exist that I could not look for.

---

## Sources

Numbering is shared with the inline citations. "Fetched 2026-10-18" applies to every entry unless a different date is given. "(WebFetch)" means I read it through the WebFetch summariser; others were fetched directly and read in full or searched locally. Where a page states its own date or version I give it.

[1] Project charter — CHARTER.md — undated (local file) — principles incl. "prefer scriptable tools", real memories stay real, dignity and consent.
[2] DaVinci Resolve (product page) — https://www.blackmagicdesign.com/products/davinciresolve — Resolve 21 / "What's New in 21.1" — Free = 8-bit up to 60 fps, UHD; Studio adds 10-bit 120 fps and >4K. (also WebFetch)
[3] DaVinci Resolve Studio — https://www.blackmagicdesign.com/products/davinciresolve/studio — Studio $295 excl. tax/shipping; Studio feature list incl. remote scripting API, multi-GPU, H.264/H.265 hardware acceleration, Neural Engine.
[4] DaVinci Resolve — What's New — https://www.blackmagicdesign.com/products/davinciresolve/whatsnew — 21.1; Photo page, AI tools.
[5] DaVinci Resolve — Training — https://www.blackmagicdesign.com/products/davinciresolve/training — official video series with durations; Resolve 20 training books (PDF).
[6] DaVinci Resolve Scripting README (mirror of Blackmagic's README.txt by X-Raym) — https://gist.githubusercontent.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8/raw — "Last Updated: 24 Jul 2026" — Console/Scripts menu, `-nogui`, API superset for Free and Studio, `ImportTimelineFromFile` formats, render functions.
[7] pydavinci README — https://raw.githubusercontent.com/pedrolabonia/pydavinci/main/README.md — undated, Resolve 18 era, third party — "External scripting … requires Resolve Studio (Free version does not allow API access)".
[8] Kdenlive — Downloads — https://kdenlive.org/download/ — 26.08.2; Windows 10+, macOS 13+, AppImage/Flatpak.
[9] Kdenlive — News — https://kdenlive.org/news/ — 26.08.2 (2026-10-13); 26.12 in development; 26.04.3 (2026-07-06) MLT command-execution hardening.
[10] Kdenlive 26.08.0 released — https://kdenlive.org/news/releases/26.08.0/ — 2026-08-31.
[11] Kdenlive manual — Rendering — https://docs.kdenlive.org/en/exporting/render.html — manual 26.08 — presets (ProRes, FFV1, H.264, H.265, AV1), Generate Script, `melt script.mlt`, proxies, experimental hardware presets.
[12] Kdenlive manual — What's New — https://docs.kdenlive.org/en/more_information/whats_new.html — keyframe easing modes, curve editor, subtitles, mask effects, proxies in preview.
[13] Kdenlive manual — Speech to Text — https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html — VOSK and Whisper subtitles.
[14] Kdenlive manual — Introduction — https://docs.kdenlive.org/en/getting_started/introduction.html — MLT, Glaxnimate integration (22.08), nested timelines (23.04).
[15] Kdenlive manual — Effects and Filters — https://docs.kdenlive.org/en/effects_and_filters.html — Transform effect, keyframes, auto-keyframe, masking effects.
[16] Kdenlive manual — Video Tutorials — https://docs.kdenlive.org/en/getting_started/tutorials/video_tutorials.html — official list (Nuxttux, Arkengheist 2.0, others).
[17] MLT — melt documentation — https://www.mltframework.org/docs/melt/ — (WebFetch) producers, filters, consumers, `xml` consumer.
[18] MLT — XML documentation — https://www.mltframework.org/docs/mltxml/ — producers, playlists, multitracks, filters, consumers.
[19] Shotcut — Download — https://www.shotcut.org/download/ — (WebFetch) 26.9.27; platforms.
[20] Shotcut — FAQ — https://www.shotcut.org/FAQ/ — minimum requirements; projects saved as MLT XML; Preview Scaling and Proxy.
[21] Shotcut — home and news — https://www.shotcut.org/ ; https://www.shotcut.org/blog/ — 26.9 "Auto Duck and Adjustment Clip" (2026-09-27), 26.8, 26.6, 26.4; releases about every two months.
[22] OpenShot — Download and User Guide — https://www.openshot.org/download/ ; https://www.openshot.org/user-guide/ — v4.0.1; GPL v3 or later.
[23] libopenshot C++ API — https://www.openshot.org/files/libopenshot/ — version 0.7.0; Timeline, Clip, Keyframe, FFmpegReader/Writer.
[24] Blender — Releases — https://www.blender.org/download/releases/ — (WebFetch) 5.2 LTS 2026-07-14; 5.1 2026-03-17; 5.0 2025-11-18; 4.5 LTS 2025-07-15.
[25] Blender 5.2 LTS Manual — Command Line Arguments — https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html — `-b`, `-P/--python`, `--python-exit-code`, `-E`, `--factory-startup`.
[26] Blender 5.2 LTS Manual — Rendering From The Command Line — https://docs.blender.org/manual/en/latest/advanced/command_line/render.html — page "Last updated on 2026-10-17"; argument order; `-f`, `-a`, `-o`, `-F`.
[27] Blender Python API — Blender as a Python Module — https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html — `pip` module, limitations, default startup scene.
[28] Blender 5.2 LTS Manual — Grease Pencil Build Modifier — https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html
[29] Blender 5.2 LTS Manual — Trim Curve Node — https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/trim_curve.html
[30] Blender — System Requirements — https://www.blender.org/download/requirements/ — minimum/recommended; Apple Silicon only from 5.0; pen tablets recommended for Grease Pencil.
[31] Blender Studio — Training — https://studio.blender.org/training/ — courses and lesson types.
[32] Inkscape 1.4.4 release page — https://inkscape.org/release/ (redirects to /release/inkscape-1.4.4/) — released 2026-05-06; Windows on Arm; macOS extension-CLI known issue (CVE-2025-15523).
[33] Inkscape — man page — https://inkscape.org/doc/inkscape-man.html — export, query and action options.
[34] Inkscape Wiki — Using the Command Line — https://wiki.inkscape.org/wiki/Using_the_Command_Line — (WebFetch) `--actions` needs `--batch-process`; shell mode.
[35] Inkscape — Learn: Animation — https://inkscape.org/learn/animation/ — "Inkscape does not support animation natively".
[36] Inkscape — Tutorials index and Interpolate tutorial — https://inkscape.org/learn/tutorials/ ; https://inkscape.org/doc/tutorials/interpolate/tutorial-interpolate.html — official tutorials (Basic, Shapes, Advanced, Tracing, Calligraphy, Interpolate…).
[37] Inkscape Wiki — Release notes 1.4 — https://wiki.inkscape.org/wiki/Release_notes/1.4 — "Many new actions have been added", new command line options.
[38] Glaxnimate — https://glaxnimate.org/ — vector animation; Lottie, GIF, WebP, animated SVG; Python scripting.
[39] Glaxnimate — Scripting — https://glaxnimate.org/contributing/scripting/ — console, plugins, `pip install glaxnimate`, example.
[40] Glaxnimate 0.6.0 release notes — https://glaxnimate.org/news/releases/0.6.0/ — 2026-03-03; SVG frame-sequence export; Microsoft Store, macOS Intel/Arm.
[41] Glaxnimate Manual — Supported Formats — https://docs.glaxnimate.org/en/formats.html — manual 0.5.4; Lottie, TGS, SVG with SMIL, WebP/GIF, raster frames.
[42] Synfig — https://www.synfig.org/ ; https://synfig.readthedocs.io/en/latest/ — manual 1.5.1; requirements; vector tweening, bones.
[43] Synfig CLI source — https://raw.githubusercontent.com/synfig/synfig/master/synfig-core/src/tool/optionsprocessor.cpp — options `-t`, `-w`, `-h`, `--fps`, `--time`, `--begin-time`, `--end-time`, `--append`, `--video-codec`.
[44] Friction — https://friction.graphics/ ; https://raw.githubusercontent.com/friction2d/friction/main/README.md — GPL-3.0-only; SMIL export; ECMAScript expressions; FFmpeg; 1.0.0 release-candidate download links.
[45] OpenToonz — https://opentoonz.github.io/e/ ; https://raw.githubusercontent.com/opentoonz/opentoonz/master/README.md ; https://opentoonz.readthedocs.io/en/latest/ — free for commercial and non-commercial use; manual 1.7.1; "official source only" warning.
[46] GIMP — Downloads — https://www.gimp.org/downloads/ — 3.2.6 (2026-09-10); macOS 11+; AppImage needs Debian 13+.
[47] GIMP 3.0 Release Notes — https://www.gimp.org/release-notes/gimp-3.0.html — new API, Python 3, plug-in breakage.
[48] GIMP 3.2 Release Notes — https://www.gimp.org/release-notes/gimp-3.2.html — scripting API additions; API stable across 3.x.
[49] GIMP — man page — https://www.gimp.org/man/gimp.html — `--batch-interpreter`, `-b`, `--quit`, `gimp-console`.
[50] GIMP — Community Tutorials — https://www.gimp.org/tutorials/ — Layer Masks, Basic Color Curves, Luminosity Masks.
[51] Krita — Download — https://krita.org/en/download/ — 5.3.4.1 released 2026-10-07; system requirements.
[52] Krita Manual — Linux Command Line — https://docs.krita.org/en/reference_manual/linux_command_line.html — manual 5.3.0; `--export`, `--export-sequence`, `--template`.
[53] Krita Manual — Animation with Krita; Render Animation — https://docs.krita.org/en/user_manual/animation.html ; https://docs.krita.org/en/reference_manual/render_animation.html — PNG sequence then FFmpeg; frames held in RAM; no transparent video.
[54] Krita Manual — Introduction to Python Scripting — https://docs.krita.org/en/user_manual/python_scripting/introduction_to_python_scripting.html — Scripter inside Krita.
[55] Photopea — Learn: Introduction — https://www.photopea.com/learn/ — vendor statement on local processing.
[56] MagicaVoxel — https://ephtracy.github.io/mv_main.html ; https://ephtracy.github.io/mv_renderer.html ; https://ephtracy.github.io/mv_commands.html — 0.99.7.2 [7/12/2025]; licence; renderer; export; console; FAQ.
[57] MagicaVoxel .vox file format — https://raw.githubusercontent.com/ephtracy/voxel-model/master/MagicaVoxel-file-format-vox.txt — dated 10/18/2016; chunk spec.
[58] Goxel — https://goxel.xyz/ ; https://raw.githubusercontent.com/guillaumechereau/goxel/master/README.md ; https://raw.githubusercontent.com/guillaumechereau/goxel/master/src/main.c — README "Version 0.15.1", GPL-3, formats; CLI `--export`, `--script`.
[59] Blockbench — https://www.blockbench.net/ — low-poly/cuboid models, animation, plugins, web app, GPL.
[60] Audacity — Downloads and Audacity 4 — https://www.audacityteam.org/download/ ; https://www.audacityteam.org/audacity-4/ — 4.0.1.
[61] Audacity Manual — Scripting; Macros — https://manual.audacityteam.org/man/scripting.html ; https://manual.audacityteam.org/man/macros.html — legacy development manual.
[62] FFmpeg — Download — https://ffmpeg.org/download.html — (WebFetch) 9.0.2 (2026-09-18), 8.1.3 (2026-09-21); source only, Windows/macOS builds from third parties.
[63] FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html — zoompan, xfade, subtitles, lut3d, colorbalance, curves, loudnorm.
[64] ImageMagick — Download; Command-line Processing — https://imagemagick.org/download/ ; https://imagemagick.org/command-line-processing/ — 7.1.2-34 AppImage; `magick`.
[65] CSS-Tricks — How SVG Line Animation Works (Chris Coyier) — https://css-tricks.com/svg-line-animation-works/ — 2014-02-18.
[66] MDN — stroke-dashoffset — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/stroke-dashoffset — resolved against `pathLength`.
[67] GSAP — Pricing; 3.13 release; DrawSVG plugin — https://gsap.com/pricing/ ; https://gsap.com/blog/3-13/ ; https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/ — "GSAP is now free for everyone", all plugins free.
[68] Rive — Pricing — https://rive.app/pricing — Free $0 with splash screen on exports; Cadet $9/seat/month.
[69] Lottie Animation Format specification — https://lottie.github.io/lottie-spec/latest/ — Community Specification.
[70] Easing Functions Cheat Sheet — https://easings.net/
[71] Wikipedia — Match cut; Ken Burns effect; Parallax scrolling; Twelve basic principles of animation — https://en.wikipedia.org/wiki/Match_cut ; https://en.wikipedia.org/wiki/Ken_Burns_effect ; https://en.wikipedia.org/wiki/Parallax_scrolling ; https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation — concept definitions (match cut and "graphic match"; panning/zooming over stills; layer parallax; slow in/slow out).
[72] Depth Anything V2 README — https://raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md — Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0.
[73] rembg README — https://raw.githubusercontent.com/danielgatis/rembg/main/README.md — MIT; CLI `rembg i`.
[74] SAM 2 README — https://raw.githubusercontent.com/facebookresearch/sam2/main/README.md — Apache-2.0 model and code.
[75] Whisper README; whisper.cpp README — https://raw.githubusercontent.com/openai/whisper/main/README.md ; https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/README.md — MIT; `whisper audio.flac --model turbo`.
[76] incompetech — Music FAQ — https://incompetech.com/music/royalty-free/faq.html — CC BY 4.0; credit format; live productions allowed.
[77] YouTube Help — Use music and sound effects from the Audio Library — https://support.google.com/youtube/answer/3376882 — attribution; Content-ID-safe; no off-platform legal guidance.
[78] Creative Commons — FAQ — https://creativecommons.org/faq/ — meaning of NonCommercial.
[79] Creative Commons Attribution 4.0 legal code — https://creativecommons.org/licenses/by/4.0/legalcode.en — (WebFetch) "Share" includes public performance; attribution rules.
[80] Freesound — FAQ — https://freesound.org/help/faq/ — (WebFetch) CC0, CC BY, CC BY-NC; attribution wording.
[81] Pixabay — Content License summary — https://pixabay.com/service/license-summary/ — (WebFetch) no attribution; no standalone redistribution.
[82] Sonniss — GDC Game Audio Bundles — https://sonniss.com/gameaudiogdc/ — (WebFetch) royalty-free, no attribution, no AI training; GDC 2024 latest on that page.
[83] Kenney — Support (licence FAQ) — https://kenney.nl/support — CC0.
[84] FreePD — https://freepd.com/ — closure notice (2008–2025).
[85] BBC Sound Effects — https://sound-effects.bbcrewind.co.uk/licensing — "personal/educational projects, or licence them for use".
[86] Mixkit — License — https://mixkit.co/license/ — per-item-type licences; terms not extractable.
[87] Free Music Archive — https://freemusicarchive.org/ — (WebFetch) "Discovery / personal use" framing.
[88] Suno — Terms of Service — https://suno.com/terms — (WebFetch) revised 2026-08-10, effective 2026-09-03.
[89] US Copyright Office — Copyright and Artificial Intelligence — https://www.copyright.gov/ai/ — (WebFetch) Part 2 (Copyrightability) published 2025-01-29.
[90] Meta AudioCraft README — https://raw.githubusercontent.com/facebookresearch/audiocraft/main/README.md — (WebFetch) code MIT; weights CC-BY-NC 4.0.
[91] YouTube Help — Recommended upload encoding settings — https://support.google.com/youtube/answer/1722171 — MP4, H.264 High, AAC-LC 48 kHz, bitrates, BT.709.
[92] Library of Congress — Recommended Formats Statement, Moving Image Works — https://www.loc.gov/preservation/resources/rfs/moving.html — RFS 2025-2026; FFV1 v3/Matroska, ProRes/QuickTime, MP4 as viewing proxy.
[93] RFC 9043 — FFV1 Video Coding Format Versions 0, 1, and 3 — https://www.rfc-editor.org/rfc/rfc9043.html
[94] RFC 9559 — Matroska Media Container Format Specification — https://www.rfc-editor.org/rfc/rfc9559.html
[95] Wikipedia — Advanced Video Coding (levels table) — https://en.wikipedia.org/wiki/Advanced_Video_Coding — level 4.1 ≈ 1080p30; 4.2 ≈ 1080p64; 5.1 ≈ 4K31.7.
[96] Wikipedia — File Allocation Table — https://en.wikipedia.org/wiki/File_Allocation_Table — FAT32 max file 4 GB − 1.
[97] Wikipedia — EBU R 128 — https://en.wikipedia.org/wiki/EBU_R_128 — target −23 LUFS.
[98] YouTube channel listings read on 2026-10-18 (titles, lengths, relative ages only) — https://www.youtube.com/@BlenderGuru/videos ; https://www.youtube.com/@DefaultCube/videos ; https://www.youtube.com/@BlenderStudio/videos ; https://www.youtube.com/@grabbitt/videos ; https://www.youtube.com/@CaseyFaris/videos ; https://www.youtube.com/@nuxttux/videos ; https://www.youtube.com/@LogosByNick/videos ; https://www.youtube.com/@DaviesMediaDesign/videos ; https://www.youtube.com/@Audacity/videos ; https://www.youtube.com/@ShotcutVideoEditor/videos (look-alike, not official).
[99] YouTube video pages with readable metadata — https://www.youtube.com/watch?v=gcIKU4KxfLk (Arkengheist 2.0, Rotoscoping, 16:09, 2020-11-21) ; https://www.youtube.com/watch?v=F1h6Kg-WLDE (Nuxttux Creative Studio, Keyframe Interpolation, 5:34, 2025-05-29).
[100] Sandbox verification runs, 2026-10-18 — local, not a URL — ffmpeg 6.1.1, ImageMagick 6.9.12, Blender `bpy` 5.2.2 (Python 3.13), Inkscape 1.2.2, MLT melt 7.22.0, Synfig 1.5.1, Goxel 0.11.0 (Xvfb), librsvg 2.58.0, svgpathtools, Pillow; outputs inspected with `ffprobe` and by eye. Scripts reproduced in "Exemplars / recipes".
[101] Blender 5.2 LTS Manual — F-Curve Properties — https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html — interpolation/easing of animation curves.
