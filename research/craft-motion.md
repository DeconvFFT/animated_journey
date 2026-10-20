# ArtCraft motion and sound apps as refinement layers: FilmCraft, EffectCraft, SoundCraft — research notes

Track `craft-motion` · Researcher: Sonnet · Written 2026-10-18 (Sunday) for the Life Journey LEARN phase · Deadline Saturday 2027-02-27.

**How this note was made (read first).**
- Code was read from shallow clones at the newest tag of each repo: **filmcraft v0.8.0** (commit `f03e2155`, 2026-10-14 10:15 -04:00), **effectcraft v0.11.1** (commit `2a012268`, 2026-10-17 19:03 -04:00), **soundcraft v0.8.0** (commit `2578ea69`, 2026-10-17 17:16 -04:00) [39]. Nothing was built, installed or run. Cloned folders were read with grep/read tools and `git log`; the only interpreter run on them was `python3 -I` on data files (a fixture) and plain arithmetic.
- Code citations are written `repo/path @tag`. Clone with `git clone --depth 1 --branch <tag> https://github.com/storytold/<repo>`. I did not open GitHub "blob" pages; the raw pattern `https://raw.githubusercontent.com/storytold/<repo>/<tag>/<path>` returned HTTP 200 for `filmcraft/v0.8.0/ROADMAP.md`.
- **Reachability correction to review 01 Part 0.7.** `curl` through the proxy gets 403 on github.com HTML pages and the API, but (a) the **WebFetch tool does reach github.com issue lists, single issues and the releases pages** [42]-[48], and (b) **release assets and `SHA256SUMS.txt` download with curl** (302 to `release-assets.githubusercontent.com`, then 200) [40]. So issues were readable in this run. Issue pages were read through a summarising model, so numbers quoted from them are as that summary stated; the issue URLs are given so a human can re-read them.
- Evidence grades used below: **[T]** = a named test exists in the repo (oracle type stated: ffmpeg, After Effects, self round-trip, synthetic); **[C]** = code path exists, no test found; **[V]** = vendor/README/website claim only; **[I]** = issue or first-hand report; **[E]** = my estimate or extrapolation; **UNVERIFIED** = not checked.
- First-hand tests I did run: ffmpeg 6.1.1 (container system package) on synthetic audio to validate the ducking and loudness recipes [61]. The container baseline is in [62].
- Docs lag code in all three repos (examples are listed under Risks). Where a doc and the code disagree I report the code.

---

## Summary

1. **Maturity.** All three apps are about 2.5 weeks old (first commits 2026-10-01/02), agent-written Rust, alpha or pre-alpha. They cut a tag every 1 to 3 days: FilmCraft 9 tags in 12 days, EffectCraft 12 tags in 15 days, SoundCraft 6 tags in 9 days [39]. The website shows **FilmCraft 0.6.0, EffectCraft 0.8.0, SoundCraft 0.5.0** (re-checked today) while GitHub is at **v0.9.0 / v0.11.1 / v0.8.0** [41][39][65] (FilmCraft v0.9.0 was tagged on 2026-10-18; see follow-up F7). Quote tags, pin tags, and re-run the maker's five-minute test before any upgrade.
2. **Test depth is real but self-referential.** Test functions counted: FilmCraft 3,402, EffectCraft 3,564, SoundCraft 1,066 (about 401k, 383k and 97k lines of Rust). FilmCraft has genuine ffmpeg oracles (codecs, loudness). EffectCraft has exactly one After Effects comparison (168 scalar ease samples) and says so [22]. SoundCraft has none against another DAW. "Exists" is not "behaves".
3. **FilmCraft `.fcproj`:** the code's `SCHEMA_VERSION` at v0.8.0 is **15** (14 migrations, mostly no-op steps), not 13 as `docs/project-files.md` and review 01 say [2][3]. Time is an integer **tick**, 254,016,000,000 per second (a 5 s still is 1,270,080,000,000) [3][4]. The loader only checks time bounds and repairs audio-stream indices; it does not enforce overlaps, id uniqueness or effect parameter names [3]. Writing it by hand is high risk; use it as a template by example, never as the agent's primary output.
4. **Recommended FilmCraft agent path.** (1) Drive `filmcraft-cli` (commands or MCP) so the engine writes a valid `.fcproj` and can also export OTIO / FCP7 XML / FCPXML / EDL from the same session [9][14]. (2) Keep a neutral timeline spec in the repo plus a committed **OTIO** as the portable contract. (3) For the fallback editors emit a second file (FCP7 XML for Resolve). If the Linux CLI spike fails, the maker imports the OTIO on Windows.
5. **What survives import (code-verified).** Plain **OTIO**: clips, gaps, dissolves, speed, markers, nested stacks; **not** position/scale/rotation keyframes, opacity or audio gain unless they sit in `metadata.filmcraft` [6]. **FCPXML 1.9-1.11**: motion/opacity/volume keyframes survive, but FilmCraft skips a bare storyline `<video>`, `<title>`, `<audio>`, `<sync-clip>` and `<mc-clip>` with a warning [7][69] (`fcpxml.rs` @v0.8.0 line 402); a `<video ref=…>` nested inside a `<clip>` is read (line 386). One FCPXML 1.13 sample from a third-party repository shows Final Cut writing a still as a bare `<video>` [I][76], so FilmCraft would skip Final Cut's stills in that form; no 1.9-1.11 sample was found, and whether Resolve writes stills the same way is unverified. **FCP7 XML**: Basic Motion, Opacity, Audio Levels, dissolves, markers, nesting [8]. **EDL**: cuts, dissolves, speed, markers only [8]. See the matrix in Findings Q3.
6. **Trap: stills import at native pixel size.** No importer except OTIO-with-metadata sets `scale_to_frame`; `motion_matrix` treats Scale 100 as native pixels and `scale_to_frame` as fit-inside [5][6][11]. A 3600x2400 still in a 1920x1080 sequence therefore shows a native-size crop unless the agent computes the Motion scale (cover = max(W/w, H/h) x 100, e.g. 53.3 for 3600x2400 into 1080p) or pre-conforms the stills.
7. **Stills are decoded whole to 8-bit RGBA, with no EXIF orientation and no ICC handling** (the `image` crate, `to_rgba8()`), about 34.6 MB per 3600x2400 still; `file.import` and the interchange link step both decode each still at import time and keep the decoded source in a media pool that has no eviction, so importing 300 of them would hold roughly 10 GB [C][E] [10][9]. Pre-conform stills (orientation applied, sRGB, 8-bit, sized to the sequence plus Ken Burns headroom) in the container, and cut the film into chapters.
8. **Export numbers (vendor benchmarks, other hardware).** Software H.264 1080p: 15 fps on a 14-core/28-thread Xeon (1,050 CPU-ms/frame), 17.9 fps on an 8-core M1 with overlays; ProRes 422: about 5-6 fps; NVENC on an RTX 5060: 44 fps; Windows Media Foundation decode cuts CPU per 1080p frame from 77 ms to 3.3 ms [12]. A modest PC without NVIDIA is software-only (no Intel QSV or AMD AMF encoders yet [13]). My estimate for 4 cores is about 4-16 fps at 1080p [E]. **Archive master: ProRes 422 HQ from FilmCraft; premiere copy: x264 from ffmpeg off that master** (FilmCraft's own H.264 encoder has no trellis or psy-RD [18]).
9. **EffectCraft expressions run on the `boa` interpreter** (pure-Rust JavaScript, no JIT) with the After Effects object model written in `prelude.js`. 103 unit tests plus a fuzzer cover `wiggle`, `loopOut/In`, `time`, `thisComp.layer()`, `valueAtTime`, `ease/linear`, `effect()`, markers, `sampleImage` and more [25]. `wiggle` uses its own SplitMix noise, so it is deterministic but will not match After Effects. Per-frame cost is unpublished (one test asserts only "< 1000 ms" for 100 wiggles) [25]. Expressions are **not** exported to Lottie unless `includeExpressions` is set, and then as raw `x` text; bake with `prop.convertExpressionToKeyframes` first [26].
10. **EffectCraft imports.** **SVG import exists** (the README does not mention it): a static subset (paths, basic shapes, groups, `use`, CSS `<style>`, gradients, strokes and dashes); text, images, filters, clipPaths, masks, patterns, markers and animation are ignored; element ids become shape-group names; transforms are baked [27]. PSD imports as footage or comp, but all PSD fixtures are generated by the repo's own writer [28]. Lottie in/out has self round-trip tests and four fixtures, no player comparison [26]. Image sequences (PNG/JPEG/TIFF/EXR/BMP/WebP) import as one item [23].
11. **CLIs.** All three ship `<app>-cli` in the **Windows MSI and portable zip** and in the **Linux deb/rpm/tar.gz** (packaging files [15][31][38]). FilmCraft exports on the CPU by default (`GpuRendering::Off`) [14]; EffectCraft renders on the CPU unless `--gpu` [21][30]. **EffectCraft CPU renders have no memory cap** (batch = rayon threads clamped 2-16): a critical open issue with an OOM kill that leaves an unplayable MP4 [47]. In the container, start every comp at `RAYON_NUM_THREADS=1` and raise the thread count only after a 30-frame sample shows peak memory under half of free RAM (F4). `RAYON_NUM_THREADS=2` reached 6.8 GB in the #1615 reporter's project, and `EFFECTCRAFT_CPU_INFLIGHT` exists only in open PR #1763, so it does nothing in v0.11.1.
12. **SoundCraft (pre-alpha), honest verdict.** Session `.scraft` is JSON, `format_version` 1 [35]; **no sidechain/key input anywhere** (documented gap G-13) [34]; the BS.1770 meter has gating and true peak but no loudness range and is tested only on synthetic tones [36]; bounce is wav/aiff/flac at the session rate with peak-only normalise [37]; MP3 and AAC import drop frames or ignore edit lists (silent timing errors) [48]; every source is decoded whole into RAM [34]. **No step in this project (music under voice, interview cleanup, final loudness) is better in SoundCraft than in Audacity plus ffmpeg**, and FilmCraft's Essential Sound already offers auto-ducking, repair and loudness targets with an ffmpeg `ebur128` oracle [17].
13. **Fallback editors today.** Kdenlive **26.08.2** (2026-10-13) [49] imports/exports OTIO (tracks, clips, markers) [51][52], a feature added in 25.04.0 per search-result summaries of that release's notes [64]; I found no FCPXML/EDL/FCP7 import in its docs (UNVERIFIED absence). From the code at v26.08.2 (read, not run) [72]: cuts, gaps, markers and dissolves (as luma mixes, by code) survive; effects, metadata and image sequences do not; `file://` URLs are not decoded; the project profile is taken from the first still's pixel size. DaVinci Resolve **21** (free: 8-bit, up to UHD 60 fps) [55] reads OTIO natively (since 18.5 per a secondary source [56]), FCPXML, FCP7 XML and EDL; only basic dissolves survive OTIO [56]. The Resolve 21 manual [74] says FCP 7 XML Opacity, Position, Scale and Rotation keyframes import when 'Use sizing information' is ticked, and it marks no XML, OTIO or EDL import as Studio-only; that is an absence of a restriction, not a statement that none exists. The keyframes are supported at format level per the manual, FilmCraft's numbers untested, and are the maker's Exercise 6 test. Whether Resolve reads FCPXML stills or relative OTIO paths is **UNVERIFIED** (G1, G2).
14. **Stability.** Data-loss risk for a learner: **FilmCraft low-medium** (atomic saves with fsync and directory fsync, 20 rolling auto-saves, 1-second recovery journal [2]; open reports #2216 and #1939 [45]); **EffectCraft medium** (atomic write, auto-save slots, crash sentinel [32]; open #1230 export overwrite destroys the previous file, #1396 expression-editor corruption [47]); **SoundCraft medium for sessions, high for audio fidelity** (reworked save safety in v0.6.1-v0.7.0 [44], but silent import timing bugs [48]). Only FilmCraft's web build has a "FilmCraft stopped working" panic overlay [16].
15. **Network and privacy.** No telemetry or HTTP client in any default build (greps of `Cargo.lock` and sources [19][32][38]). Optional downloads: FilmCraft Whisper/Kokoro models via `ureq` behind non-default features; EffectCraft MobileSAM/MediaPipe via the system `curl`, SHA-256 checked. Control channels bind `127.0.0.1` with no token; **FilmCraft's MCP server has no folder-confinement flags** while EffectCraft and SoundCraft do [14][21][37]. For a surprise: auto-save, recovery, preview-cache and "recent" lists put copies of family media under `%APPDATA%` or beside the project; use the portable zips (FilmCraft and EffectCraft ship `portable.txt`; SoundCraft's zip does not) and keep everything in one encrypted project folder.
16. **Corrections to review 01 Part 0:** schema 15 not 13; the release web zip needs no COOP/COEP headers (only the dev server sends them) [16]; EffectCraft does import SVG [27]; GitHub issues and releases are reachable via WebFetch; EffectCraft's gap list still says "no relinking" but `docs/footage.md` documents `footage.relink` and `file.relinkFootage` [23][22].

---

## Findings by question

### Q1. Versions, cadence, Windows requirements and issues, recommended pin

**Tag history (commit dates of the tagged commit, US Eastern, from `git fetch --depth 1 origin tag` on each tag) [39].**

| App | Tags (date) | Count / span | Newest at read |
|---|---|---|---|
| FilmCraft | v0.1.0 10-02, v0.1.1 10-03, v0.2.0 10-05, v0.2.1 10-06, v0.4.0 10-08, v0.5.0 10-09, v0.6.0 10-10, v0.7.2 10-12, v0.8.0 10-14 | 9 tags in 12 days | **v0.8.0**, 2026-10-14 |
| EffectCraft | v0.1.0 10-02, v0.1.1 10-03, v0.2.0 10-05, v0.3.0 10-06, v0.3.1 10-06, v0.4.0 10-07, v0.6.0 10-08, v0.7.0 10-09, v0.8.0 10-10, v0.9.2 10-12, v0.10.0 10-14, v0.11.1 10-17 | 12 tags in 15 days | **v0.11.1**, 2026-10-17 (the releases page shows "18 Oct") |
| SoundCraft | v0.3.0 10-08, v0.4.0 10-09, v0.5.0 10-10, v0.6.1 10-12, v0.7.0 10-14, v0.8.0 10-17 | 6 tags in 9 days (earlier tags not listed) | **v0.8.0**, 2026-10-17 |

- **"Cadence over eight weeks" cannot be measured**: the oldest repo is 17 days old. The measurable cadence is roughly one tag every 1.3-1.5 days. Not every number is tagged (no FilmCraft v0.3.0, v0.7.0, v0.7.1; no EffectCraft v0.5.0, v0.9.0, v0.9.1, v0.11.0), so tags are release points, not every version [39]. There is no CHANGELOG file in any repo; release notes live only on the GitHub releases pages [42]-[44].
- **Schema churn is the pin argument.** FilmCraft's ROADMAP says schema v13 arrived with 0.5.0 on 2026-10-09 [13]; by v0.8.0 (2026-10-14) the code is at v15 (v14 narrations, v15 project notes) [3]. Newer files are refused by older builds ("saved by a newer version") [2], so a FilmCraft you upgrade past an agent-written file's tag can read it, but not the reverse.
- **Website versions (curl, 2026-10-18) [41]:** FilmCraft **0.6.0**, EffectCraft **0.8.0**, SoundCraft **0.5.0**, Launcher 0.3.2. The website also says FilmCraft has "About 55 video effects" while the README says 93 [41][1], and EffectCraft "259 effects" while the README says 306 [41][20].

**Windows requirements (what is stated).**
- Builds: x64, x86 and arm64 **MSI** (WiX v5, code-signed) and **portable zip** for each app; the portable zips contain the app plus `<app>-cli.exe` (FilmCraft and EffectCraft also `portable.txt`) [15][31][38]. Binaries link the C runtime statically, so no Visual C++ redistributable (shown for EffectCraft and SoundCraft; FilmCraft's package script builds the same way) [31][38].
- The CLI is **not on PATH** after an MSI install: `C:\Program Files\FilmCraft\filmcraft-cli.exe` (likewise EffectCraft) [14][21].
- **No minimum RAM, disk or GPU is published** for any of the three (a third-party article says the same, and its 8 GB / 2 GB figures belong to the separate ArtCraft AI studio) [58]. Windows 10/11 is stated by that article only. UNVERIFIED.
- FilmCraft draws with Vulkan or DirectX 12 (OpenGL is not in the default instance). After two launches that die within 15 s without painting, it falls back to DX12 only, then to a software adapter (WARP) with CPU compositing; `--graphics default|dx12|software` and `WGPU_BACKEND` override [1][13]. EffectCraft has a launch guard that switches Window Graphics to OpenGL after a crashed launch [31]. SoundCraft initialises only DirectX 12 by default and compiles shaders with FXC [33].

**Documented Windows problems (grouped).**
- FilmCraft: AMD `atio6axx.dll` crash when OpenGL is created (README, fixed by default backend list); duplicate-GPU `amdvlk64.dll` access violation (README, fixed in v0.8.0 notes) [1][42]. Open issues: #1390 "Not launching on Windows" (other Craft apps launch; opened 2026-10-12) and #2237 "Not opening or running at all"; #2205 Intel HD "not supported well"; #1972 Intel Gen 9 `igvk64.dll` access violation or hang with `--gpu-rendering auto`; #1705 and #2179 WASAPI/no sound on Windows 11; #1616 GPU export silently renders on CPU after an FXC compile failure; #1678 AV1 hardware decode detected but rejected by Media Foundation [45][46]. `docs/gaps.md` G9 adds Windows bins and Sequence Settings dialog problems [13].
- EffectCraft: README "Linux and Windows users have hit basic interaction bugs" [20]; Direct3D 12 fails (FXC cannot compile the `pointwise` kernel, #613) while Vulkan works [24]; web on Chrome/Windows loses the GPU device about 60 s after load (#1590) [47]; one search summary (not fetched) reports "all memory consumed on Windows 11 with an Intel Arc card" [60].
- SoundCraft: #722 crash when loading VST3 plugins (critical), WASAPI/ASIO device choice only added 2026-10-12, no Windows-specific data-loss report seen [48][34].

**Recommended pin (policy plus today's candidates).** Pin by acceptance, not by recency: install the **portable x64 zip** of the candidate tag into a project folder, run the maker's five-minute test (Recipes R7), record tag and SHA-256 in the repo, and disable the Launcher's updater during production (review 01 Part 1.4 [63]). Candidates today, with the checksums from each release's `SHA256SUMS.txt` [40]:

| App | Candidate tag | Windows x64 portable zip SHA-256 | Linux x86_64 tar.gz SHA-256 |
|---|---|---|---|
| FilmCraft | v0.9.0 (newest tag, 2026-10-18; test first) | `d370cac8ed2edd729c8129aa55f75d0123716ba3cddbf9c5e4e3f0fdaa101a5e` | `ea67953cc754bfd8272e0e5fa940518e16068ae96f6b72a2dce566ed69a61632` |
| FilmCraft | v0.8.0 (fallback) | `0119afd59dfd6ecb94470ba6b3a48108ade87dabd4972898dd6c04e1db396b0b` | `b166877905ae8a1b5505066d6dde60d7ce05831cfb309bacd5d7970f4bb017e1` |
| EffectCraft | v0.11.1 (adds unique temp files for atomic writes and a non-zero exit when a render fails [43]) | `78bd7f63c6bd814bc33f07bd523b003a5f8d095244c5f67bd70e902448fd6e34` | `b9cb2ce68dd66458cc164437e431376e94e38e33e3b6529fa8fd45f8cf968934` |
| SoundCraft | v0.8.0 (learning only) | `8846ec66fc3520d46c4a4453642ec2061567f8cb0ef378a2af54f7605f85ff90` | `57a2b8776d51880cee69118568a396c09faca6949dcbf50f19879d71d596f5cc` |

These values were copied from each release's `SHA256SUMS.txt` downloaded today [40]; the maker verifies the Windows zip with `Get-FileHash -Algorithm SHA256`. FilmCraft v0.9.0 is the candidate (test first, F7), v0.8.0 is the fallback, and v0.7.2 (2026-10-12) is retired from the pin list; its x64 portable zip hash is `8e22fabdf2f802573d3af4ad9993c05212dead5e933efda0fa290e825313cde7` [40].

### Q2. FilmCraft `.fcproj`: minimal project, migrations, time base, direct vs OTIO

**Format facts.** UTF-8 JSON envelope `{format: "filmcraft.project", schema_version, generator, project, view?}` [2][3]. `project` is the serde dump of `filmcraft_project::Project` (name, settings, root bin tree, `items` map keyed by id, `next_id`, plus optional luts/transcripts/search_bins/source_graphics/narrations/notes) [4]. Media is referenced by **absolute path**, never embedded; each media item also stores size and a 64-bit fingerprint of the first and last MiB ("identity") for relinking [2]. Files are written compact (a 2,000-clip project is 1.4 MB) [2].

**Schema version and migrations [3].**
- `MIGRATIONS` has 14 functions (v1->v2 ... v14->v15); `SCHEMA_VERSION = MIGRATIONS.len() + 1 = 15`. v1->v2 wraps the bare project in the envelope; steps v2->v3 through v14->v15 are mostly **no-op bumps** that exist so older builds refuse files they would silently damage. New `#[serde(default)]` fields need no bump.
- Older files are upgraded **in memory**; the first save over one keeps the original as `<name> (schema vN backup).fcproj` [2]. Files newer than the build are refused. So an agent may write an **older** schema_version with the older shape and FilmCraft will migrate it (the committed v11 minimal fixture is 477 bytes) [3]. This is a trick, not a contract.
- `docs/project-files.md` still says "schema_version 13" and its history table stops at 13; the code is at 15 [2][3]. Treat the code as truth and ask the CLI which version it writes: save an empty project once and read `schema_version`.

**Time base.** `Tick(i64)`, **254,016,000,000 ticks per second**, divisible by every common frame and sample rate [4]. Useful values (computed): 1 frame = 10,160,640,000 (25 fps); 10,584,000,000 (24); 10,594,584,000 (23.976); 8,475,667,200 (29.97); 8,467,200,000 (30); 5,292,000 per 48 kHz sample. The README example `duration: 1270080000000` is exactly **5.000 s**; its `sourceIn: 284298240000000` is 1119.214 s (an arbitrary media offset). Bounds: `Tick::MAX = i64::MAX / 4`, about 105 days [4]. Keyframe `time` is a tick count; for a still with `source_in = 0` clip time and media time coincide, which removes the ambiguity that exists for trimmed video (Motion is evaluated at media time `mt`) [11].

**A minimal project, as the serde structs and the committed `v1-edit.fcproj` fixture imply (SKETCH: assembled by reading, never loaded by any program).** One still media item, one sequence, one video track, two clips with a 1 s dissolve at the cut, and scale/position keyframes on the first. Frame rate 25, sequence 1920x1080. Comments are explanatory and must be stripped.

```jsonc
{
  "format": "filmcraft.project",
  "schema_version": 15,                       // read it from a CLI-saved empty project
  "generator": "agent-spec 1",
  "project": {
    "name": "Chapter 01 draft",
    "settings": { "renderer": "FilmCraft GPU Acceleration (wgpu)", "video_display": "Timecode",
                  "audio_display_samples": true, "default_still_duration": 1270080000000,
                  "default_transition_duration_frames": 24, "default_audio_transition_duration": 254016000000 },
    "root": { "id": 0, "name": "Chapter 01 draft", "children": [ { "Item": 5 }, { "Item": 21 } ] },
    "items": {
      "5": { "id": 5, "name": "IMG_0001.png", "label": "Iris",
        "kind": { "Media": {
          "media": { "File": { "path": "C:/LifeJourney/work/stills/IMG_0001.png" } },   // absolute, maker's machine
          "info": { "name": "IMG_0001.png", "kind": "Still", "duration": 1270080000000,
            "video": { "width": 2880, "height": 1620, "frame_rate": { "num": 30000, "den": 1001 }, "par": [1,1],
                       "codec": "PNG", "pixel_format": "RGB 8-bit",
                       "color": { "matrix": "Bt709", "transfer": "Srgb", "primaries": "Bt709", "range": "Full" },
                       "has_alpha": false, "bitrate": null },
            "audio_streams": [], "container": "Image", "start_timecode": null, "file_size": null },
          "interpret": { "frame_rate": null, "par": null, "ignore_alpha": false, "invert_alpha": false },
          "mark_in": null, "mark_out": null, "markers": [], "offline": false, "proxy": null } } },
      "6": { /* second still, same shape, id 6 */ },
      "21": { "id": 21, "name": "Seq", "label": "Forest",
        "kind": { "Sequence": {
          "settings": { "width": 1920, "height": 1080, "frame_rate": { "num": 25, "den": 1 }, "par": [1,1],
                        "sample_rate": 48000, "drop_frame": false, "preset": "HD 1080p 25", "audio_master": "Stereo",
                        "preview_codec": "ProRes 422", "max_bit_depth": false, "max_render_quality": false,
                        "working_space": "Rec. 709" },
          "video_tracks": [ { "id": 15, "kind": "Video", "name": "Video 1",
            "items": [
              { "id": 29, "item": 5, "name": "IMG_0001", "label": "Iris",
                "start": 0, "duration": 1270080000000, "source_in": 0, "speed": 1.0, "enabled": true,
                "effects": [ { "effect": "motion", "enabled": true, "params": {
                    "position": { "value": { "Vec2": { "x": 960.0, "y": 540.0 } }, "keyframes": [
                        { "time": 0,             "value": { "Vec2": { "x": 960.0, "y": 540.0 } }, "interp": "Linear" },
                        { "time": 1270080000000, "value": { "Vec2": { "x": 930.0, "y": 520.0 } }, "interp": "EaseOut" } ] },
                    "scale": { "value": { "Float": 100.0 }, "keyframes": [
                        { "time": 0,             "value": { "Float": 100.0 }, "interp": "Linear" },
                        { "time": 1270080000000, "value": { "Float": 112.0 }, "interp": "EaseOut" } ] } } } ] },
              { "id": 30, "item": 6, "name": "IMG_0002", "label": "Iris",
                "start": 1270080000000, "duration": 1270080000000, "source_in": 0, "speed": 1.0, "enabled": true, "effects": [] }
            ],
            "transitions": [ { "id": 31, "effect": { "effect": "cross_dissolve", "enabled": true, "params": {} },
                               "start": 1143072000000, "duration": 254016000000,   // centred on the cut at 5 s
                               "from": 29, "to": 30, "align": "CenterAtCut", "reverse": false } ],
            "locked": false, "sync_lock": true, "enabled": true, "muted": false, "solo": false,
            "channels": "Stereo", "volume_db": 0.0, "pan": 0.0 } ],
          "audio_tracks": [], "markers": [], "mark_in": null, "mark_out": null, "work_area": null, "start_timecode": 0 } } }
    },
    "next_id": 40                               // must exceed every id used (one counter for items, tracks, clips, transitions, markers)
  }
}
```

**Fields an agent must get right if it ever writes this directly [3][4][11].**
1. `schema_version` and a build that reads it; one shared id counter (`next_id` above every id; clip `item` must name an existing media item).
2. Ticks, not frames or seconds; clips on a track sorted by `start` and non-overlapping (not enforced on load, enforced by edit commands) [3].
3. `info.kind: "Still"` and correct `width/height` (stills are re-probed when the file is found, so wrong sizes self-correct on link, but anchors computed before that are off) [9].
4. **Motion semantics:** `position` is a pixel point in sequence space with origin top-left (centre = w/2, h/2), `scale` is percent where 100 = the source's native pixels (`scale_to_frame: true` multiplies a fit-inside factor on top), `rotation` degrees; anchor defaults to the source centre (`null` coordinates read as "auto") [11][4].
5. Keyframe `interp` names: `Linear`, `Hold`, `Bezier`, `AutoBezier`, `ContinuousBezier`, `EaseIn`, `EaseOut`; influence defaults to 1/3 [4].
6. Transition `from`/`to` are clip ids, `start`/`duration` are timeline ticks, `align` is `StartAtCut|CenterAtCut|EndAtCut`; the dissolve id string is `cross_dissolve`; stills have unlimited handles, trimmed video does not [8][4].
7. Absolute media paths for the maker's machine, or fix them afterwards with `media.autoRelink {from, to}` (a folder-prefix remap) [2].

**Direct write vs OTIO vs the CLI, risk comparison.**
- **Direct `.fcproj`:** richest (Bezier ease, titles, adjustment layers, masks), but coupled to a schema that moved 13 -> 15 in five days, validated only by "does it load". Failure modes are silent (unknown effect param ids ignored; malformed `metadata` dropped with `.ok()`; no overlap check) or a "Corrupt File" dialog [3][6]. Risk **high**.
- **OTIO import:** structure is stable (OTIO schemas), effects ride in `metadata.filmcraft` whose JSON is the same `EffectInstance` serde as `.fcproj`; a wrong shape is dropped silently (`effects_from(..).ok()`), never an error [6]. Risk **medium**, and fails soft.
- **CLI/MCP commands** (`file.newSequence`, `timeline.place`, `effects.setParam`, `sequence.applyVideoTransition`, `effects.setInterpolation`, `file.exportInterchange`): validated by the command layer, schema-independent, and self-documenting (`filmcraft-cli commands`, `describe <id>`) [9][14]. Risk **low-medium**; requires the Linux CLI to run in the container (spike S1).

### Q3. FilmCraft interchange: what survives, and what Resolve free and Kdenlive read

**How import works [9][5].** Each importer returns a standalone project fragment plus a **Report** of everything unrepresentable; `merge_into` adds it as one undo step; then every new file-backed media item that exists on disk is probed (`media.open_file`), its real `MediaInfo` replaces the guessed one (so a still becomes `kind: Still`), and Motion anchors are re-centred. Missing files stay offline (red "MEDIA NOT FOUND" slate) and are listed under `offlineMedia`. Relative `target_url`/`src`/`pathurl` values resolve against the document's folder; `file:///C:/x` URLs are decoded [5]. Report text for dropped features appears in the import dialog and in the CLI JSON `report` array [9].

**Interchange matrix.** Cells: **P** preserved, **D** degraded, **L** lost. "FC-meta" = only if the file carries FilmCraft's own `metadata.filmcraft`. Evidence grade in brackets; sources are the cited files.

| Feature (FilmCraft import) | OTIO (plain, foreign file) | OTIO + `metadata.filmcraft` | FCPXML 1.9-1.11 | FCP7 XML (xmeml 4/5) | CMX 3600 EDL | `.fcproj` direct |
|---|---|---|---|---|---|---|
| Still clip with duration | **P** (`Clip` + `ExternalReference`, `source_range`; kind set on probe) [T: golden test uses video clips] [6][9] | P | **D**: `asset-clip`, `ref-clip` and `clip` (its first inner `video`, `audio` or `asset-clip` with a `ref`, line 386) are read; a bare storyline `<video>` is skipped with a warning [C] [7][69]. Final Cut writes stills as a bare `<video>` in one FCPXML 1.13 sample [I][76]; Resolve's form is unverified | **P** (`clipitem`+`file`; kind guessed from extension) [C] [8] | **D**: event with reel and `* SOURCE FILE:` comment; no media size, assumed sequence size until Link Media [T] [8] | P |
| Speed / reverse / freeze | P (`LinearTimeWarp`, `FreezeFrame`) [T] [6] | P | P (two-point `timeMap`; ramps flattened to first/last) [T] [7] | P (Time Remap constant/reverse/freeze) [T] [8] | P (`M2` lines) [T] [8] | P |
| Position/scale/rotation keyframes (Ken Burns) | **L** (OTIO has no transform schema; report: "effect ... not supported") [6] | **P** incl. Bezier/ease (full `EffectInstance`) [T: lossless round-trip] [6] | **P** (`adjust-transform` `param`/`keyframeAnimation`); only linear and hold read, ease lost; position is % of frame height, uniform scale only (non-uniform warns) [T: scale keyframes round-trip] [7] | **P** (Basic Motion scale/rotation/center/anchor); `hold`/`bezier`/`fcpcurve` interpolation, handles not preserved [T: rich_roundtrip] [8] | **L** | P |
| Opacity (incl. keyframes) | **L** | P | P (`adjust-blend` amount keyframes) [T] [7] | P (Opacity filter) [8] | L | P |
| Dissolves | **P** (`Transition.1` `SMPTE_Dissolve`; in/out offsets give alignment) [T: golden] [6] | P (effect id kept) | P (`transition` on the primary storyline; elsewhere reported) [T] [7] | P ("Cross Dissolve & friends") [T] [8] | P (`D nnn`, wipes, keys) [T] [8] | P |
| Audio clip level | **L** | P (`gain_db`, effects) | P (`adjust-volume` dB, keyframes) [T] [7] | P (Audio Levels, keyframes; clip gain folded in with an info note) [8] | L (channel routing only) | P |
| Markers | P (`Marker.2`, colour name, comment, range) [T] [6] | P | P (`marker`/`chapter-marker`; 1-frame becomes a point) [T] [7] | P [8] | P (`* LOC:`) [8] | P |
| Nested sequences | P (`Stack` in a track) [6] | P | P (`ref-clip` to `media`) [T] [7] | P [8] | **D**: one event, reel `AX` [8] | P |
| Titles / graphic clips | **L** (becomes a `MissingReference`, offline) [5] | L | L | L (named in report) | D (ordinary event) | **P** (schema v3/v12) |
| Image sequences | **D**: `ImageSequenceReference` is read as one file path from `target_url_base` [6] | D | L | D | L | P (`file.import imageSequence:true`) |
| `metadata.filmcraft` round-trip | n/a | **P** for FilmCraft-written files [T] [6] | none (no equivalent) | none | none | n/a |
| Foreign effects (blur, Lumetri...) | L (warning per effect) | P only if FilmCraft effect JSON | D (`filter-video` matched by name to FilmCraft effects, float params only) [7] | D (matched by id or display name) [8] | L | P |

**Test evidence for the matrix [9]:** `tests/otio.rs` has a hand-written Premiere-style document (`golden_gaps_and_transitions`: gaps, three dissolves, markers, speed, offline media, audio effect reported) and `lossless_roundtrip_with_filmcraft_metadata`; `tests/fcpxml.rs` has a hand-written document (`golden_connected_clips`: transform, retime, transition, keyframed opacity, volume, compound clip, markers) and `roundtrip_all_versions`; `tests/fcp7.rs` has Premiere-style documents and `rich_roundtrip`; `tests/edl.rs` has golden drop-frame dissolves. **No test uses a file actually exported by Resolve, Kdenlive or Final Cut**; the nearest is "what Premiere Pro 26.5.2 writes, read off its exported files" (interchange README [5]). The owner has never validated AAF/OMF in Avid or Pro Tools (gap G15), and XML/OTIO import of a Premiere sequence took 66-97 s for three media files (#461) [13].

**Which of these open in the fallback editors today.**

| Format | Kdenlive 26.08.2 (2026-10-13) [49] | DaVinci Resolve 21, free [55] |
|---|---|---|
| OTIO | **Yes**: import and export documented in the File menu [51], added in 25.04 with a C++ rewrite (search-result summaries [64]); the 26.08.0 notes do not mention OTIO [50]; carries tracks, clips and markers (marker types stored under `kdenlive` metadata) [51]; cuts, gaps, markers and dissolves (as luma mixes, by code) survive; effects, metadata and image sequences do not; `file://` URLs are not decoded; the project profile is taken from the first still's pixel size [72]; a March 2026 post says metadata and effects are dropped on import and resolution/frame rate are not exported [52]; bug 503692: an OTIO whose media is missing aborts import, and Kdenlive->Resolve flips track order (V1<->V2) [54]. Stills as image clips: sized by code, not run [72]. | **Yes**: native since 18.5 per a secondary source [56]; timeline names and track names may reset, complex transitions become cuts, only basic dissolves survive, Resolve-specific effects stay behind [56]. Free vs Studio: the manual [74] marks no XML, OTIO or EDL import as Studio-only, but has no free-versus-Studio table, so this is an absence of a restriction, not a statement that none exists. |
| FCPXML | not found in docs (UNVERIFIED absence) | **Yes**: a July 2026 guide for Resolve 21.0.2 recommends exporting FCPXML 1.9 and File > Import > Timeline [57 search result only]; a 2025 Blackmagic forum thread reports clips arriving unlinked when imported via the scripting API (search summary) [60] |
| FCP7 XML (xmeml) | not found in docs (UNVERIFIED absence) | **Yes**, supported at format level per the Resolve 21 manual [74] (pp. 482, 484, 521-523): Opacity, Position, Scale and Rotation import, keyframes included, when 'Use sizing information' is ticked; still image clips are listed as 'all supported formats'. FilmCraft's numbers untested. |
| EDL | not found in docs (UNVERIFIED absence) | **Yes** (needs reel/timecode matching; awkward for stills) |

**Answer to "one agent-written file serves both the Craft app and the fallback".** Only **OTIO** is read by both Kdenlive and Resolve. A single `.otio` carrying (a) relative-or-absolute `ExternalReference`s, (b) `Transition.1` dissolves, (c) `Marker.2` markers and (d) FilmCraft's `metadata.filmcraft.effects` for Ken Burns and clip gain gives: **full** edit in FilmCraft; **cuts, markers and basic dissolves** in Kdenlive and Resolve (they ignore unknown metadata). Ken Burns and audio levels are then lost in the fallbacks. Two ways to avoid that loss:
1. **Bake motion** in the container (ffmpeg `zoompan` or code-to-video) into per-shot video intermediates and mix audio into one WAV; the OTIO then carries only cuts, dissolves and markers that every editor reads, at the price that the maker cannot adjust the camera moves in the editor.
2. **Emit a second file for Resolve**: FCP7 XML (Basic Motion keyframes, Opacity, Audio Levels), and the Resolve 21 manual [74] says its keyframes import, so the maker's test checks FilmCraft's numbers.
Media path caution: Kdenlive aborts on missing media [54] and does not decode `file://` URLs [72]; FilmCraft resolves relative paths against the document folder [5]. Use one fixed project root on the maker's PC (for example `C:\LifeJourney\`) and write relative `target_url`s in the OTIO (`media/ch01_s01.png`), resolved against the `.otio` file's folder, keeping the same relative layout in the repo.

### Q4. FilmCraft stills-heavy performance

**What the code does with stills [10][9].**
- Formats: PNG, JPEG, GIF, WebP, TIFF, BMP, Targa, DPX, EXR, Radiance HDR, DNG; not HEIC, PSD, camera RAW [10][13].
- Decode: the whole file is read (`std::fs::read`) and decoded by the `image` crate (`png, jpeg, gif, webp, tiff, bmp` features) to **8-bit RGBA** (`to_rgba8`); 16-bit TIFF is quantised to 8 bits; the colour is tagged sRGB full-range and **EXIF orientation and ICC profiles are not read** (no code references either) [C] [10]. TIFF compression support is whatever the `tiff` crate supports plus a custom YCbCr path [10].
- Memory: a decoded 3600x2400 still is 34.6 MB. **Import already decodes it**: `file.import` (`commands.rs`) and the interchange link step (`engine/src/interchange.rs`) call `open_file` (which fully decodes a still) and then `insert_file` it into the pool; the pool (`MediaPool.sources`, one source per item) is only emptied on relink or clear, with no memory-pressure eviction [C] [9]. So importing 300 such stills holds about **10 GB** before any playback [E]. The documented memory work (GOP-cache budget 1 GiB, 4 live decoders, 512 MiB export in-flight budget) concerns video, not stills [12]. The v0.4.0 notes report 12 GB -> 1.9 GB for twelve video clips [42].
- Duration: stills report a default duration of 5 s; clip durations on the timeline are free (`still` clips are treated as unbounded for trims) and the default for new placements is the `timeline.stillImageDuration` preference [10][9].
- **Proxies:** supported for video (ProRes Proxy/LT quarter or half, H.264 quarter/half; `media.createProxies`; export always uses full resolution) [2]; I found **no still-specific proxy path** (UNVERIFIED whether proxies work on stills). Pre-scaling stills yourself is the reliable equivalent.
- **Render previews:** cached by content hash, so an edit invalidates only touched segments; stored under `<data dir>/Media Cache` (location, age and size limits are preferences) [2][1]. Issue #1443 reports previews of 0.7-1.1 GB per 30-47 s of 1080x1920 sequence (ProRes preview codec) and an export that exhausted 14 GiB RAM and disk when the timeline was playing during export (open, 2026-10-12/15, Ubuntu, 0.7.2 and 0.8.0) [45]. Budget several GB of preview cache for a 6-minute film and avoid playing the Program monitor during an export.
- **Image sequences:** numbered stills import as one clip (`file.import {imageSequence: true}`; OTIO `ImageSequenceReference` does not map) [9][6]; open issues #2235 (sequence frames bypass the frame-size limit) and #2227 (oversized frame metadata can enter saved projects, critical) [45].
- **Compositing/effects:** Motion, opacity, blend modes and the most common effects run on the wgpu GPU path; **Lumetri, keys and export rendering run on the CPU**; GPU export rendering is opt-in (Off by default "until it has been measured on Windows and macOS") and was 2.3-3.2x faster on effects-heavy scenes in the one measurement, a Linux Ryzen 7 9700X + Radeon RX 7900 (13.0 s -> 5.0-5.6 s for 191 frames at 1080p; 39 s -> 12 s at 4K), with no gain on a plain clip [12][13]. A CPU path renders the same frames and "the two are tested against each other" (golden images) [1][17].

**Vendor benchmarks that bear on a modest Windows PC [12].**

| Measure | Machine | Result |
|---|---|---|
| Software H.264 export, 8 s 1080p23.976, default preset | Xeon E5-2680 v4 (14C/28T), RTX 5060, Windows 11 | **15.0 fps**, 1,050 CPU-ms/frame (12.7-12.8 s) |
| Software export (GPU rendering Off), 191 frames 1080p: plain clip / clip with Proc Amp + blur + vignette + two PiP copies / same at 4K | Linux, Ryzen 7 9700X (16 threads) | plain 6.0 s = **32 fps** (292 CPU-ms/frame); effects 13.0 s = **15 fps** (737 CPU-ms/frame); 4K effects 38.7-39.3 s = **4.9 fps** (2,955 CPU-ms/frame) |
| Same, NVENC (opt-in) | same | **44 fps**, 356-373 CPU-ms/frame |
| 1080p25 camera clip + ProRes 4444 overlays, 9:29 timeline, software H.264 | Apple M1 8-core | 793 s (17.9 fps, 1.4x slower than real time); hardware encoder 311 s |
| H.264 + AAC export 8 s 1080p | Apple M4 Pro (under load) | 10.2-11.9 fps, 250 CPU-ms/frame; ProRes 422: 6.3-9.6 fps, 232 CPU-ms/frame |
| H.264 hardware decode 1080p, Off -> Auto (Media Foundation) | RTX 5060, Windows 11 | CPU 77-80 -> 3.3 ms/frame; 162-166 -> 347-353 fps. HEVC needs the Microsoft HEVC extension |
| Peak RSS sections (macOS dev machine) | M4 Pro | decode 2.0-2.9 GB, playback 3.1-3.4 GB, export 2.6 GB, timeline 0.7 GB |

The README's own speed claim, "a 6-second 960x540 render takes 1.3 seconds" (about 110 fps at 540p; hardware unstated), is backed by the encoder correctness oracle, not by a speed test [1][18]. These are the vendor's own numbers on other hardware, not ours. The 9:29 M1 run also shows the export is bound by the CPU compositor and decoders, not the encoder [12].

**Estimate for the maker's PC (no NVIDIA) [E].** A still-based timeline has little decode cost, so per-frame cost is composite + colour conversion + encode: roughly 0.25-1.0 CPU-seconds per 1080p frame (the plain and effects scenes above bracket it; CPU-only Lumetri colour adds more). On 4 effective cores that is about 4-16 fps; on 8 cores about 8-30 fps. A 6-minute film at 25 fps (9,000 frames) therefore takes about 9-37 minutes at 1080p on 4 cores, and about four times that at 4K. ProRes 422 HQ is in the same range. These figures must be replaced by the spike's measurement and the maker's acceptance test.

**Hardware encode/decode on Windows.** Decode: Media Foundation/D3D11 for H.264, HEVC, VP9, AV1 when the driver and extensions exist; falls back to the project's own software decoders; zero-copy is missing (every frame is read back) [12][13]. Encode: **NVENC only** (H.264, HEVC Main/Main 10, opt-in in Export, "Hardware encoding"); no Intel Quick Sync or AMD AMF encoders (gap G5) [13]. Issue #1582 (SIGSEGV when cancelling an NVENC export; OS not shown in the listing) and #1616 (Windows GPU export silently on CPU) are open [45][46].

**Export settings.**
- **Archive master:** preset "Apple ProRes 422 HQ" (QuickTime MOV, 24-bit 48 kHz PCM, `render_at_max_depth`), sequence resolution and frame rate; or "Apple ProRes 4444" if the film contains alpha or very smooth gradients (4444 tag bug exists in EffectCraft only, #340 [22]). ProRes is checked against ffmpeg in both directions: `tests/oracle_decode.rs` decodes 29 ffmpeg-made fixtures, `tests/oracle_encode.rs` encodes every profile (including 4444 with an alpha disc) and has ffmpeg decode it [18]. DNxHR HQ/SQ/LB MOV and MXF exist but are 8-bit 4:2:2 [11].
- **Big-screen premiere:** take the ProRes master and encode with **ffmpeg x264** (`-preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart`, AAC 320 kbps or PCM in MOV) because FilmCraft's encoder has no trellis, no psy-RD, a single reference per list and no B-pyramid [18]. If an in-app export is wanted, "High Quality 1080p HD" (20 Mbps) or "High Quality 2160p 4K" (60 Mbps) are the built-in presets; the default "Match Source - Adaptive High Bitrate" is 0.2 bits per pixel (about 10 Mbps at 1080p25) [11]. A projector PC plays H.264 MP4 reliably; keep ProRes for archive.
- Keep frame rate and audio at 48 kHz throughout; pick the sequence frame rate once (24, 25 or 30) and bake stills to it.

### Q5. EffectCraft expressions

- **Engine:** crate `effectcraft-expr`, **`boa_engine`** (a pure-Rust JavaScript interpreter) [25]. Array arithmetic (`value + [10, 0]`) is implemented by rewriting `+ - * /` into helper calls (`rewrite.rs`, 907 lines) [25]. Scripting (`effectcraft-script`, `.jsx`/`.js` files, `run_script`) is a second boa-based layer with an After Effects scripting object model [25][21].
- **Object model implemented (`prelude.js`, 1,056 lines) and tested (103 `#[test]` functions in `src/tests.rs`, plus `tests/fuzz.rs`) [25][T: unit tests, synthetic projects, no After Effects oracle]:**

| Member (from the brief) | Implemented | Test names |
|---|---|---|
| `wiggle(freq, amp, octaves, ampMult, t)`, `temporalWiggle` | yes | `wiggle_is_deterministic`, `wiggle_amplitude_bounds_and_motion`, `wiggle_octaves_bound`, `wiggle_differs_per_layer_and_dimension`, `wiggle_on_other_layer_property`, `temporal_wiggle_stays_on_the_curve` |
| `loopOut/loopIn` (`cycle`, `pingpong`, `offset`, `continue`, duration/keyframe counts) | yes | `loop_out_cycle`, `loop_out_pingpong`, `loop_out_offset`, `loop_out_continue`, `loop_in_cycle_and_offset`, `loop_out_num_keyframes_and_duration`, `loop_on_two_dimensional_position` |
| `time`, `value` | yes | `time_times_360`, `value_is_the_keyframed_value` |
| `thisComp.layer(name or index)`, `thisLayer`, `comp(name)` | yes | `layer_by_name_and_index`, `cross_layer_position_reference`, `layer_shorthand_attributes`, `comp_by_name`, `parent_attributes` |
| `valueAtTime`, `velocityAtTime`, `speedAtTime`, `key()`, `nearestKey`, `numKeys`, `smooth` | yes | `value_at_time`, `value_at_time_respects_layer_start_time`, `velocity_and_speed`, `keys_and_nearest_key`, `smooth_on_linear_ramp_is_identity` |
| `linear`, `ease`, `easeIn`, `easeOut` (3 and 5 argument forms, arrays) | yes | `linear_three_args`, `linear_five_args_maps_and_clamps`, `ease_curves`, `interpolation_with_arrays` |
| `effect("Name")("Param")`, masks, shape `content`, markers, `toComp/fromComp/toWorld`, `sourceRectAtTime`, `sampleImage`, `footage()`, `posterizeTime`, `seedRandom/random/gaussRandom/noise`, `lookAt`, colour conversions, `text.sourceText` | yes | `effect_slider_reference`, `mask_properties`, `shape_content_paths`, `markers`, `to_comp_and_from_comp`, `source_rect_at_time`, `sample_image_reads_rendered_pixels`, `data_footage_json_csv_tsv`, `posterize_time`, `random_is_seeded_and_in_range`, `gauss_random_distribution`, `noise_is_smooth_and_bounded`, `angles_and_look_at`, `colour_conversions`, `source_text_*` |

- **Safety limits:** nesting depth 16, at most 20,000 script runs and 5 s per outermost evaluation, loops stop at a million iterations, circular references terminate; each limit has a test [25].
- **Fidelity to After Effects:** `wiggle`/`noise`/`random` use SplitMix hashing and value noise seeded by layer index and property uid (`noise.rs`), so output is **deterministic and platform-independent but not After Effects' sequence** [25]. The only live After Effects comparison in the repo is scalar Rotation ease (8 cases, 168 samples via AEsync 2.0.4; max error 3e-11 degrees) [22]. No expression is compared to After Effects. Treat expression behaviour as "plausibly AE-like, internally consistent".
- **Per-frame performance:** unpublished. `hundred_wiggles_are_fast` times 100 `wiggle(2,50)` properties and asserts only `< 1000 ms/frame` in an unoptimised build ("release is far below") [25]; no number is in the docs. Interpreter cost scales with expression complexity; reading many properties triggers host requests (memoised). To be measured in the spike.
- **Lottie:** expressions are **not exported by default**; with `includeExpressions` the raw After Effects expression text is written to the property's `x` field, which only lottie-web evaluates (and with lottie-web's own semantics, not boa's) [26]. For anything leaving EffectCraft as Lottie, run `prop.convertExpressionToKeyframes` on each expression property first (command exists in `commands/prop.rs` and has a test on reversed layers, `tests_timeline.rs`) [25]. Text-source expressions are never exported [26].
- **Agent first drafts:** yes. `set_property {expression}` or `run_script` lets an agent write expression-driven motion (drift, breathing scale, `loopOut("pingpong")`, `linear(time, ...)` reveals) as a draft that the maker refines by editing the expression, converting to keyframes and easing in the Graph Editor. Cautions: `wiggle` will not look like After Effects tutorials; a syntax error keeps the text but disables it and reports the line; an open issue reports corruption when entering multi-line scripts in the expression editor (#1396) and long "catching frames" waits after every edit on heavy comps (#1641) [47]. Put expression logic in the agent-side spec, keep each expression short, and save first.

### Q6. EffectCraft imports and exports

**Imports (EffectCraft v0.11.1) [23][27][28][26].**

| Source | Present? | What is preserved | Evidence |
|---|---|---|---|
| **SVG** (README is silent) | **Yes**, `.svg` import and clipboard paste (`edit.pasteSvg`) | SVG 1.1/2 static subset: `svg/viewBox/preserveAspectRatio`, `g`, `defs`, `use`/`symbol`, paths (all commands, arcs), `rect/circle/ellipse/line/polyline/polygon`, transforms, fill/stroke incl. `stroke-dasharray`, opacity, `display`, linear and radial gradients with `gradientTransform`, CSS via attributes, `style` and `<style>` (type, class, id, universal selectors). **Ignored: text, images, filters, clipPath, masks, patterns, markers, animation.** Imports as footage (continuously rasterised) or, via Layer > Create > Create Shapes from Vector Layer (`layer.create {op: "shapesFromVector"}`), as editable shape layers where each element or group becomes a shape group named by its **id** (or element name); transforms are baked into geometry | [T] 11 unit tests in `svg/src/tests.rs`, 2 fixtures, `paste_svg_markup_as_a_shape_layer` (two rects, pixel checks); no comparison with resvg or a browser |
| **Lottie** | Yes (File > Import > Lottie, `.json` or `.lottie`) | precomps, shape/solid/null/image/text layers, keyframes with temporal and spatial easing, masks, track mattes, blend modes, time remap, markers | [T] self round-trip with render comparison, 4 fixtures with attribution (`bouncing-ball`, `legacy-masks`, `precomp-matte-text`, `shapes-gradient`); no external player compared |
| **PNG/JPEG/TIFF/EXR/BMP/WebP sequences** | Yes: `file.import {paths:[first], sequence: true, frameRate}`; missing frames show colour bars; Interpret Footage sets alpha (straight/premultiplied/guess), fps, start timecode, Preserve RGB | alpha PNG/EXR/TIFF; multi-layer EXR shows the beauty layer | [C]/[D] docs `footage.md`; EXR HTJ2K compression fails (#482) |
| **PSD / PSB** | Yes, as footage, as a composition, or a composition with layer sizes retained | layers, groups, masks, blend modes, layer styles, smart objects (placed by corner quad, warps baked), adjustment layers, text (best-effort first style run), 1/8/16/32-bit; CMYK naive | [T] `psd_imports_as_composition` etc., but **every fixture is generated by the repo's own PSD writer**; spec-derived (Adobe Nov 2019), no real Photoshop files |
| **Video** | Yes, via FilmCraft's pure-Rust codecs (H.264, HEVC, ProRes, VP9, AV1, AAC, Opus...) | no hardware decode in EffectCraft; **variable-frame-rate phone video is listed "unverified"** | [D] `file-format-parity.md` |
| Other | `.ai`/PDF/EPS vector (partial), 3D models glTF/OBJ/STL/FBX 7.x, fonts, LUTs, OCIO; **no `.aep`, `.mogrt`, `.ffx`** | | [23] |

**Exports (render queue and CLI) [20][30][23].** H.264/HEVC/AV1 MP4, ProRes MOV (`--prores proxy|lt|standard|hq|4444|4444xq`, **with alpha**), WebM (VP9 or AV1, Opus; **alpha supported**), PNG/JPEG/TIFF/**32-bit EXR** sequences, GIF, WAV/AIFF, plus uncompressed RGB(+alpha) MOV. `--channels rgba` selects alpha. Known problems: ProRes 4444 is **tagged bt709 but sRGB-encoded** (#340, open) [22]; cancelling or failing an overwrite destroys the previous output file (#1230) [47]; HEVC/AV1 encoders have no B-frames and produce larger files [22]. **For alpha overlays headed into FilmCraft prefer an RGBA PNG sequence** (no colour-tag ambiguity) and import it as an image sequence; FilmCraft keeps alpha in PNG and TIFF sequence exports and decodes ProRes 4444 alpha [1][18].

**What Lottie export cannot express (from the warnings in `export.rs`, `shapes.rs`, `text.rs` [26]) and what our chapters would lose.** Most effects (blur, glow, Lumetri...) are skipped; adjustment layers become nulls; video, image-sequence and audio footage are not part of Lottie (exported as hidden nulls); cameras, lights and 3D model layers are dropped (3D layers get `ddd:1`, which most players ignore); layer styles (drop shadow...) are not exported; blend modes with no Lottie equivalent become Normal; reversed time stretch, Preserve Underlying Transparency and layer markers are unsupported; Offset Paths copies collapse to one; track mattes that are not directly above the matted layer may break; text on a path, per-character fonts and faux styles, more than one text-animator selector and Source Text expressions are lost (`textAsShapes` bakes static glyphs at time 0); mask feather is written as `f` and not every player renders it; still images are embedded as base64; expressions as above. **For Life Journey this means Lottie is only suitable for small vector motion pieces (icons, line-draws, simple title reveals) shown in a web page; photographic chapters, parallax, effects and anything with audio must be rendered to video or PNG sequences.**

**Agent-to-EffectCraft hand-offs.**
- **(a) Titles and typography.** Prefer FilmCraft's own graphic clips for static titles and lower thirds (OpenType shaping, bidirectional text, keyframable; schema v3/v12) [1]; use EffectCraft only when text animators, expressions or shape-layer ornaments are needed. Hand-off: a title spec JSON (string, family, size, tracking, fill, in/out times, animator preset) -> agent builds with `comp.new`, `layer.newText {name, text, size, fill}`, `add_keyframe ... interpolation: easyEase`, `batch` [21]; output RGBA PNG sequence or ProRes 4444 alpha. **Font trap:** EffectCraft bundles only Inter, JetBrains Mono and Noto Serif; an unavailable family falls back to Inter (#1677, open) [47][23]. Install the chosen OFL fonts on the maker's PC (list kept in the repo with files), or outline text with `layer.create {op: "shapesFromText"}` (tested against the text render) at the cost of editability [27].
- **(b) 2.5D parallax photo.** Hand-off: depth-ordered RGBA PNG layers (`NN_name.png`, inpainted background first) from the imagery track plus a manifest with z values and camera path. Build: `file.import` / `file.newCompFromSelection`, `layer.setSwitch {switch: "threeD", value: true}`, `layer.newCamera`, keyframed camera position or dolly with easy-ease, optional depth of field (CPU render cost unpublished; the only published CPU figure is Advanced 3D at 3,394 ms/frame at 1080p on an M4 Pro [22]). Classic 3D layers are the right feature; PSD with layers also imports as a comp but is less tested than PNG layers. Edge halos and stretched disocclusions need the maker's eye. Fallback: do parallax in code (three.js or Blender, per the agent-pipeline track).
- **(c) SVG line-draw.** Hand-off: SVG with `fill="none"` stroked paths, **unique `id` on every element**, no text/clipPath/mask/filter, flat or lightly nested groups, one `<style>` block at most [27]. Build: `edit.pasteSvg {svg}` (creates a shape layer, one shape group per element, named by id) or import + `layer.create {op: "shapesFromVector"}`, then `layer.addShapeItem {kind: "trim"}` on each group and keyframe Trim Paths End 0 -> 100, staggered per path. Tests exist for Trim Paths (`trim_below_stroke_trims_it`, `trim_individually_vs_simultaneously`) and SVG paste of filled rects, but **no test combines SVG strokes with Trim Paths** [T partial] [27]. Output: RGBA PNG sequence over the page colour. Alternative with fewer moving parts: CSS `stroke-dashoffset` or GSAP in headless Chromium (agent-pipeline track) or a Lottie for web delivery.

**`.ecproj` schema and migrations [29].** One JSON object, **no envelope**: `schema` (currently **2**), `settings`, `items` (map of folders/comps/footage/solids), `next_id` (one counter shared by items, layers and property uids), `render_queue`, `render_templates`, `render_prefs`, and next to them `savedBy`, `activeComp`, `openComps` (editor view) [29]. Only one migration exists (schema 1 -> 2: effect positions measured from the top-left of comp-sized bounds on layers without a source rectangle, #227). `from_json_repaired` clamps hostile values (zero frame rates, huge comps; v0.9.2 notes mention 30,000 px limits [43]) and reports what it corrected; a newer schema is refused [29]. There is **no committed sample `.ecproj` and no standalone schema document**; layers carry a property tree with uids. Hand-writing is high risk. Build compositions through `effectcraft-cli` (`exec`, `run`, `set`, `script FILE.jsx`) or MCP (`batch`, `run_script`), then save [21][30]. Footage paths are absolute; `footage.relink {item, path}` and `file.relinkFootage {folder, dryRun}` remap a moved folder [23].

### Q7. CLIs on Windows and Linux, headless CPU operation, and the container spike

**Packaging proof (files read at the tags).**

| App | Windows MSI | Windows portable zip | Linux deb/rpm | Linux tar.gz | macOS |
|---|---|---|---|---|---|
| FilmCraft | `filmcraft.wxs` component `FilmcraftCli` -> `filmcraft-cli.exe` [15] | `filmcraft.exe + filmcraft-cli.exe + portable.txt` (`package.ps1`) [15] | `nfpm.yaml` -> `/usr/bin/filmcraft-cli` [15] | `bin/filmcraft-cli` (`package.sh`) [15] | separate `filmcraft-cli-<v>-macos-universal.zip` [40] |
| EffectCraft | `effectcraft.wxs` component `EffectcraftCli` [31] | `effectcraft.exe + effectcraft-cli.exe + portable.txt` [31] | `nfpm.yaml` -> `/usr/bin/effectcraft-cli` [31] | yes [31] | separate zip [40] |
| SoundCraft | `soundcraft.wxs` component `SoundcraftCli` [38] | `soundcraft.exe + soundcraft-cli.exe` (no `portable.txt`) [38] | `nfpm.yaml` -> `/usr/bin/soundcraft-cli` [38] | yes [38] | separate zip [40] |

The website lists the CLI only as a macOS zip [41], which is misleading; the MSI/zip/deb files above do contain it. The deb `Depends:` of all three are `libc6 (>= 2.35)`, `libgcc-s1`, `libxkbcommon0`, `libvulkan1 | libegl1`, `libasound2 | libasound2t64` (the binaries link only glibc and libgcc_s; windowing and GPU libraries are loaded at run time) [15][31][38]. The container image already has `libvulkan1`, `libegl1`, `libxkbcommon0`, `libasound2t64`, glibc 2.39, 4 CPUs, 16 GB RAM, no GPU and ffmpeg 6.1.1 [62].

**GPU needed for headless?** No, by default. FilmCraft: `GpuRendering::Off` default; the GPU frame renderer is registered lazily and used only with `--gpu-rendering auto` [14]. EffectCraft: "renders on the CPU unless started with `--gpu`" [21][30]; with `--gpu` and no usable adapter the MCP server "says why and exits" [21]. SoundCraft CLI has no GPU path [37].

**Documented CPU performance.** FilmCraft: README "a 6-second 960x540 render takes 1.3 seconds" (hardware unstated) [1]; benchmarks in Q4 [12]. EffectCraft: the only CPU numbers are in issue #1615: **8 stacked 1080p 3D video layers, 30 frames: 36 s on 1 thread (about 1.2 s/frame, 2.1 GB), 17 s on 4 threads (4.2 GB), over 9 GB and OOM-killed at 16 threads; a single `render-frame` peaks at 1.8 GB** [47]. A real project with Glow, masks and Fractal Noise used 3.9-5.5 GB per frame, 6.8 GB even with 2 threads [47]. Cause (reporter, plus code at v0.11.1): the export batch equals the rayon thread count clamped to 2-16 and a whole batch renders at once; GPU renders have `EFFECTCRAFT_GPU_INFLIGHT`, CPU renders have no cap [30][47]. PR #1763 adds `EFFECTCRAFT_CPU_INFLIGHT`; it is **not in the v0.11.1 code** (grep finds only `EFFECTCRAFT_GPU_INFLIGHT`) [47][30]. **Mitigation in the container (F4): start every new comp at `RAYON_NUM_THREADS=1`; render a 30-frame sample under `/usr/bin/time -v` and record peak RSS; raise threads only while peak stays under half of free RAM; where that is too slow, render frame by frame (`render-frame` per frame, to PNG) and encode with ffmpeg. `RAYON_NUM_THREADS=2` is not a bound (6.8 GB in the #1615 reporter's project). `EFFECTCRAFT_CPU_INFLIGHT` exists only in open PR #1763 and does nothing in v0.11.1. One render per process, `--autosave`, check the MP4 with ffprobe (an OOM leaves no `moov` atom).**

**Spike scope:** see Recipes R8 (written, not run).

### Q8. SoundCraft, honestly

| Question | Answer | Evidence |
|---|---|---|
| Stage | "pre-alpha", ~40% of replacing Pro Tools by its own estimate; alpha blockers: channel routing/duplex low-latency, MIDI input, AAF/OMF. The README still lists "choosing an audio interface and buffer size" as missing, but `crates/playback/src/devices.rs` implements device, rate and buffer choice (gaps G-01 done 2026-10-12; ASIO only behind the non-default `asio` build feature) | [33][34][38] [V][C] |
| Session file | `.scraft` = pretty-printed JSON (serde) of `Session { format_version: 1, name, sample_rate, bit_depth, frame_rate, tempo, tracks, sources, videos, busses, outputs, markers, groups, edit, next_id, comments, ... }` plus an `Audio Files/` folder; `from_json` refuses newer versions and `sanitize()` repairs ids after loading untrusted data; a mutated-file property test loads or fails cleanly | `crates/model/src/session.rs` [35] [T] |
| Import formats | WAV/BWF/RF64, AIFF, FLAC (own readers, **sample-exact on 20 of 20 lossless references**), MP3/AAC/ALAC/Ogg/CAF via `symphonia` 0.5.5, audio of MP4/MOV; Standard MIDI Files; no AAF/OMF/`.ptx`; no HEVC/AV1/DNx video | [34][48] |
| **Import bugs (open)** | MP3: frames dropped in 7 of 11 real files, audio shortened and shifted (#710, Windows 11, 0.7.0); AAC MP4 edit list ignored, 20 of 74 files run long or start 1,024-2,112 samples late (#707); 5.1 AAC fails (#708); AC-3/E-AC-3 raw streams all fail (#709); HE-AAC imports as mono or half length (#712, #740) | corpus report #711 (124 files; frame counts match for 81 of 112) [48] [I] |
| Sidechain / ducking | **No key input in any host or built-in plugin** (G-13, plugin-parity "Sidechain / key input: no"); the compressor has an internal sidechain high-pass only. Ducking therefore means drawing volume automation (breakpoints, Write/Touch/Latch passes, clip gain lines, convert to clip gain). No auto-duck | [34] `compressor` source `dynamics.rs` [C] |
| Loudness metering | `LoudnessMeter` implements ITU-R BS.1770 / EBU R128: K-weighting, momentary (400 ms), short-term (3 s), gated integrated (absolute -70 LUFS, relative -10 LU), 4x oversampled true peak. **No loudness range (LRA).** Tests assert synthetic tones (997 Hz at -20 LUFS reads -20; gating ignores silence; low sample rates stay bounded); **no ffmpeg or other oracle** | `crates/dsp/src/meter.rs`, `tests/offline_meters.rs` [36] [T synthetic] |
| Bounce | `file.bounce_mix {path, format: wav\|aiff\|flac, bit_depth: 16\|24\|32f, start, end, source: main\|bus, normalize, dither, fold_down: stereo}`; stems via `file.bounce_stems`; returns `peak_db`, `lufs`, `true_peak_db`; **sample rate = the session's** (offline `convert --rate` resamples); `normalize` is a **peak** normalise to -0.1 dBFS, not a loudness target; bounces over 4 hours are refused; no MP3/AAC export (G-21) | `crates/engine/src/cmd/file.rs`, `apps/soundcraft-cli/src/main.rs` [37] |
| CLI | `soundcraft-cli run [--in S.scraft \| --demo] [--cmd id=json]... [--bounce OUT] [--save S]`, `convert IN OUT [--bit-depth 16\|24\|32f] [--rate HZ] [--normalize]`, `script FILE`, `mcp [--automation-read-root DIR --automation-write-root DIR]`, `app --port` | [37][33] |
| Autosave / recovery | Background crash-recovery copies of the open session in `<settings>/Autosave/` (written at most once per second while changes arrive, with the plan of a running recording), recovery offered at launch (v0.7.0), takes kept when input/output/disk fails or the app crashes, save-safety overhaul (never overwrites audio or sessions, syncs, keeps backups; v0.6.1). `docs/gaps.md` G-06 still says recording goes to RAM and sources are "decoded whole into the SourcePool"; the second part stays true (1 hour of stereo f32 is 1.38 GB) | `crates/engine/src/autosave.rs`, release notes [38][44][34] |
| CLAP on Windows | CLAP, VST3 and (macOS) AU hosting; CLAP floating windows plus embedded editors on Windows; VST3 editors verified with one free JUCE plugin on Windows; **#722 crash when loading VST3 plugins (critical, open)**; no CLAP plugins bundled; availability of any specific free CLAP plugin on Windows UNVERIFIED | `docs/plugin-parity.md` [34][48] |
| Known gaps | audio-interface routing/duplex low-latency, MIDI device input, AAF/OMF, sidechain, English only, Windows/Linux lightly exercised, no PR CI | `docs/gaps.md` [34] |

**Verdict versus Audacity plus ffmpeg (`sidechaincompress`, `loudnorm`).** There is **no step in this project where SoundCraft beats the incumbent today**:
- *Music under voice:* ffmpeg `sidechaincompress` ducks automatically from the voice; I validated the syntax on ffmpeg 6.1.1: music at -27.5 dB RMS dropped to -38.2 dB while a synthetic voice spoke and recovered afterwards [61]. SoundCraft has no sidechain and no auto-duck. FilmCraft's Essential Sound has auto-ducking that writes Volume keyframes (threshold -20 - 4*sensitivity dBFS on the summed trigger signal, regions under 100 ms dropped, pauses under 250 ms bridged, fades before and after), tested on a dialogue+music project to within 60 ms (measured 20 ms) and -15.00 dB [17][T synthetic].
- *Interview cleanup:* SoundCraft's built-in plugins are EQ, dynamics, de-esser, reverbs and so on; I found no noise-reduction or de-hum processor in its list (the plugin inventory in `plugin-parity.md` calls the catalogue "thin and unverified"). FilmCraft's Essential Sound repair chain has DeNoise, DeHummer, DeEsser, DeReverb and Enhance Speech (a DSP chain, not a model), each stage tested to improve its metric on synthetic material; Audacity has noise reduction and spectral tools [17].
- *Final loudness:* SoundCraft measures integrated LUFS and true peak at bounce but can only peak-normalise. FilmCraft can match clips to LUFS targets and normalise on export (BS.1770-4 integrated, true-peak limit) and its meter is tested against ffmpeg `ebur128` [17][11]. ffmpeg `loudnorm` (two-pass, linear mode) remains the reference.
- *Where it might be useful:* a human-friendly multitrack timeline for comping a voiceover, fades and clip gain with stems bounced at 24-bit. Audacity covers this too. Use SoundCraft for the maker's learning only, and never as the only copy of a unique interview recording.

### Q9. Stability, autosave, atomic saves, known data-loss issues

| | FilmCraft v0.8.0 | EffectCraft v0.11.1 | SoundCraft v0.8.0 |
|---|---|---|---|
| Atomic save | `filmcraft_format::atomic_write`: hidden temp file in the same directory, `fsync`, rename, `fsync` of the directory; applies to project, auto-save, recovery and preferences [2][3] | `config::atomic_write`: temp file, `sync_all`, rename (no directory fsync); v0.11.1 uses a unique temp name each time; test `atomic_write_survives_a_crash_mid_write` [32][43][T] | temp file, flush to disk, rename (`io.rs`); v0.6.1 "never overwrites audio or sessions, syncs saves, keeps backups" [38][44] |
| Auto-save | on by default, every 5 min (1-1440), 20 rolling versions in `Auto-Save/` next to the project (`<name>-YYYY-MM-DD_HH-MM-SS.fcproj`), also a **recovery journal** written about 1 s after each edit with an OS file lock, offered after a crash (`--recover`, `--no-recover`) [2] | `<name> auto-save N.ecproj` slots in `EffectCraft Auto-Save/`, a `session.lock` sentinel offers the latest auto-save after an unclean exit (loses up to one interval); `effectcraft-cli mcp --autosave` checkpoints before each reply [32][21] | background copies in `<settings>/Autosave/`, recovery at launch [38] |
| Older-schema safety | first save over a migrated file keeps `(schema vN backup)`; newer files refused [2] | newer schema refused; `from_json_repaired` clamps hostile values [29] | `format_version` > 1 refused [35] |
| Web | OPFS recovery snapshot every 5 s; **"FilmCraft stopped working" overlay with the panic message and a Reload button** (`apps/filmcraft-web/web/index.html`); out-of-memory also triggers it [16] | page sets `effectcraftLoad.error`; no overlay found; session restore with IndexedDB | no overlay or automation API found |
| Open data-loss or corruption reports (read 2026-10-18) | #2216 critical: user on Windows 11 deleted timeline content, "Ctrl+Z did nothing", lost work; a contributor could not reproduce from the code and pointed to the Auto-Save folder; #1939: on macOS 0.8.0 a saved demo `.fcproj` would not reopen ("cannot open files in the FilmCraft Project format"), no reply; #1943 Cmd-Q quits without save prompt (macOS); #1845 Audio Channels can silently replace stored mappings; #1443 export OOM [45] | #1230 cancelling or failing an overwrite destroys the previous output file; #1396 expression-editor corruption on multi-line scripts; #1240 browser session recovery commits content and metadata separately; #1615 OOM leaves an unplayable MP4; crashes #1666 (rotoscope, critical), #1556, #1388 [47] | #710/#707 silent audio timing errors; #665 export stuck at 95%; #722 VST3 crash (critical) [48] |
| Tracker size (counts as reported by the pages, 2026-10-18) | 710 issues in the tab; 35 open matches for a data-loss query; 101 results for a Windows crash/launch query; sitrep #2099 closed "not planned" by triage bot [45][46] | 449 open | search "Windows" 62 results (open) [48] |
| CI | none runs `cargo test`/`xtask ci` on pull requests (243 PRs merged 10-05..10-10 on local runs) [13] | same, no PR gate [22] | same (G-14) [34] |

**Data-loss risk for a learner (my rating, with mitigations).**
- **FilmCraft: LOW-MEDIUM.** Best save and recovery design of the three, but one critical user report of unrecoverable deleted content (unreproduced), macOS save/reopen failure, and memory exhaustion during export. Mitigate: keep the agent-written spec, OTIO and CLI script in git so `.fcproj` is regenerable; `File > Save a Copy` at the end of each session; auto-save interval 2 min; never save over the only copy; check the `Auto-Save` folder exists.
- **EffectCraft: MEDIUM.** Atomic saves and sentinel recovery exist, but the app is the youngest, 449 open issues, a critical OOM, and render outputs can be destroyed on overwrite. Mitigate: render to a new file name every time; keep project text in git via agent scripts; `--autosave` for headless.
- **SoundCraft: MEDIUM for sessions, HIGH for silent audio errors.** Do not import MP3/AAC for work; use WAV/FLAC only; keep originals untouched.

### Cross-cutting: footprint, web builds for Playwright, network audit

**Memory footprint.** FilmCraft (vendor numbers, macOS): project open/save bench ~0.12 GB; timeline 0.6-0.7 GB; export 2.6 GB; playback 3.1-3.4 GB; 12 video clips 1.9 GB after the v0.4.0 work; stills unmeasured (about 35 MB each as computed) [12][42][E]. EffectCraft: 1.8 GB for one 1080p frame of an 8-layer 3D comp; wasm 58 MB uncompressed [47][24]. SoundCraft: sources whole in RAM (1.4 GB per hour of stereo float) [34][E]. Publishing no minimum spec means the maker's PC (RAM unknown, review 01 gap 1.7) is the real test; run one Craft app at a time.

**Web builds (static zips `<app>-web-<ver>.zip`) [16][24][15].**
- FilmCraft web: wasm32 + wasm-bindgen, eframe on **WebGPU with WebGL2 fallback**, single-threaded (no `SharedArrayBuffer`), wasm ~13 MB (5 MB compressed), `.wasm` must be `application/wasm`; **no COOP/COEP needed** for the release zip (`packaging/web/README.md`; `docs/web.md` says only the `--serve` dev server sends them); URL flags `?cpu`, `?webgl`, `?empty`, `?norecover`, `?fresh`; media stays local (OPFS copies up to 4 GiB, file picker or drop); previews, proxies, Project Manager and mask tracking report errors on the web; no NVENC or Media Foundation. **`window.filmcraft`** exposes `execute`, `request` (any control method, `ui.inspect`, `ui.click`...), `commands`, `inspect`, `screenshot`, `importFiles`, `importUrl`, `openProject`, `files`, `readFile`, `info`. A Node CDP smoke test (`tests/smoke.mjs`, headless Chrome with `--enable-unsafe-webgpu`) loads, plays the demo, imports an ffmpeg-made MP4, exports H.264 and fails on any Rust panic [16].
- EffectCraft web: wasm ~58 MB raw (17 MB gzip, 10 MB Brotli), service worker, WebGPU frame workers with CPU fallback (`?noworkers`, `?nogpuworkers`), `window.effectcraft` API, `tests/smoke.mjs` over CDP, COOP/COEP sent by the dev server and service worker [24]. Open #1590: on Chrome/Windows the GPU device is lost about 60 s after every load [47].
- SoundCraft web: `trunk` build, WebAudio, no isolation headers needed; no automation API or smoke test found [38].
- **Verdict:** a Playwright session (Chromium with SwiftShader WebGL2, or `?cpu`) is feasible for FilmCraft and EffectCraft and is the best way for an agent to **learn the UI and produce annotated screenshots for the maker**, because the vendor already ships a headless-Chrome harness and a `window.<app>` API. For rendering and authoring the CLI/MCP route is strictly better (full speed, threads, ProRes, no wasm single-thread limit). Installing Playwright browsers in the container is UNVERIFIED (network to the browser CDN).

**Network audit (greps of `Cargo.lock`, sources and docs at the tags) [19][32][38].**
- **FilmCraft:** HTTP client crate `ureq` (rustls) appears only in `crates/speech` behind the `download` feature, which only the non-default `whisper` and `neural-voices` features enable (Whisper models and Kokoro-82M from huggingface.co with pinned revision and SHA-256); the Windows/Linux package scripts build with default features, so release binaries contain no HTTP client. The README states speech-to-text is optional and off by default. Control channel: `TcpListener::bind("127.0.0.1", port)`; the bridge client refuses non-loopback addresses; **no token or authentication**; **the MCP server has no folder confinement** ("the server can read and write wherever the user can") [14]. No telemetry found.
- **EffectCraft:** no HTTP crate in `Cargo.lock`; Roto Brush (MobileSAM, 40 MB) and face tracking (MediaPipe, 3.8 MB) models download by spawning the system `curl` and are SHA-256 verified; scripts get a `Socket` class only when Preferences > Scripting > "Allow Scripts to Write Files and Access Network" is on (default off); control server and bridge are loopback only; `mcp --automation-read-root/--automation-write-root` confine file access; README: "No telemetry, and no network access unless you ask for it" [32][20].
- **SoundCraft:** no HTTP crate; control server on 127.0.0.1; `--automation-read-root/--automation-write-root`; logs to `logs/soundcraft.log` and Autosave under `%APPDATA%\SoundCraft\` [33][38].
- Not audited here: the ArtCraft Launcher (polls GitHub releases), the Discord/ticket-bot flow (bug reports submitted through Discord are relayed to public GitHub issues by a bot, so **never paste family material or file names into a bug report**), and the hosted ArtCraft AI studio (a different product; family photos must not go there).


---

## Recipes / templates

Tier recommendation (confirms review 01 Part 1.1 with code evidence): **FilmCraft = Tier B** (use for cut, Ken Burns tweak, dissolves, titles, Essential Sound, export, after the spike and the maker's acceptance test pass); **EffectCraft = Tier B for short titles/line-draw, Tier C for 3D, Lottie and long CPU renders**; **SoundCraft = Tier C** (learning only). Every step below has a non-Craft fallback.

### R1. Pre-flight: always transcode and conform media before a Craft app

Why (all from the repos and issues): FilmCraft's decoders are "bit-exact on conformance streams, but camera and phone files in the wild are less tested" [1]. The H.264 decoder is 8-bit 4:2:0 only, with no High 10, no 4:2:2, no interlaced/MBAFF; DV is unsupported; camera RAW is unsupported [13]. An HEVC HLG `.mov` from an iPhone/Meta-glasses failed to import on Windows 10 (#1998, workaround "convert to H.264 MP4 with ffmpeg") [46]. A 92-file corpus run found frame rates misdetected on 30 files with jittered timestamps (#1700) and a 5.1 AC-3 downmix with correlation 0.29 against ffmpeg (#1701) [46]. EffectCraft lists variable-frame-rate phone video as unverified [23]. VHS/MiniDV captures are interlaced and often DV.

Commands (the still, ProRes and x264 lines were run on this container's ImageMagick 6.9.12 and ffmpeg 6.1.1 with synthetic inputs; the yadif chain is standard syntax, not run):

```sh
# 1. Stills: orientation applied, 8-bit sRGB, conformed to 16:9 with a recorded crop, EXIF stripped. Masters (16-bit TIFF) stay untouched.
convert IN.tif -auto-orient -depth 8 -resize 2880x1620^ -gravity center -extent 2880x1620 -strip OUT.png
#    If the scan carries a non-sRGB ICC profile, convert it with -profile <sRGB ICC> BEFORE -depth 8 (FilmCraft ignores ICC) and check with identify -verbose. Not run.

# 2. Phone / camcorder / VHS-capture video -> ProRes 422 HQ intermediate, constant frame rate, progressive, 48 kHz audio
ffmpeg -i IN -vf "yadif=mode=0:deint=interlaced,scale=1920:1080:flags=lanczos,format=yuv422p10le" -fps_mode cfr -r 25 \
       -c:v prores_ks -profile:v 3 -vendor apl0 -c:a pcm_s24le -ar 48000 OUT.mov

# 3. Audio sources
ffmpeg -i IN -vn -ar 48000 -c:a pcm_s24le OUT.wav

# 4. Verify and record in the manifest (pix_fmt, r_frame_rate = avg_frame_rate, nb_frames, sha256)
ffprobe -v error -count_frames -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_read_frames -of json OUT.mov
```

Stills policy: the agent decides crop versus pad per shot and writes it to the manifest (no silent cropping of a face). Choose **one** sequence size and frame rate for the whole film (for example 1920x1080 at 25 fps, or 3840x2160) before conforming anything.

### R2. FilmCraft refinement-layer recipe (a stills-heavy chapter)

1. **Agent builds (container, Linux CLI if the spike passes).** For each shot compute: duration in ticks (`seconds x 254016000000`), Motion `scale` start/end and `position` start/end. For a source of w x h px in a sequence of W x H px with `scale_to_frame = false`, the scale that shows the **whole image fitted** is `min(W/w, H/h) x 100` and the scale that **covers** the frame is `max(W/w, H/h) x 100`: 3600x2400 into 1080p is 45.0 / 53.3; the conformed 2880x1620 into 1080p is 66.67 for both. Ken Burns = cover scale x 1.00 -> 1.12-1.25. Then drive the engine with one `exec` per command (a JSON-lines `run` script has fixed parameters and cannot use ids returned by earlier lines, so use a small driver, or an MCP client, that reads each result and plans the next call): `file.newProject`, `file.import {paths}`, `file.newSequence {name,width,height,fps,sampleRate}` (the default `fps` is 23.976, so set it), `timeline.place {item, track:"V1", seconds, duration}` (or `items:[...]` for back-to-back default-length stills), `effects.setParam {clip, effect:"motion", param:"scale"|"position", value, keyframe:true, time}` twice per parameter, `effects.setInterpolation`, `sequence.applyVideoTransition {clip, effect:"cross_dissolve", frames}`, `markers.add`, then `file.save`. Confirm parameter names with `filmcraft-cli describe <id>` (the CLI prints each command's parameter document). Ids come from `inspect sequence`.
2. **Agent validates (no GUI).** `filmcraft-cli --project ch01.fcproj inspect sequence` (counts, ticks, transitions); `render --seconds 2.5 --out f.png` at a start, a mid-dissolve and an end frame (finding, 2026-10-20: a single-frame probe across a dissolve shows pairs of equal frames, at offsets -5 and -4, -2 and -1, 1 and 2, and 4 and 5 in the 0.9.0 T2 run, while the exported file steps cleanly, 12 distinct levels over 12 frames, so dissolve smoothness is judged on the export, never on the probe; the mid-dissolve mark itself was amended the same day, see T2 in R8); a draft `export draft.mp4 --preset "High Quality 1080p HD" --start 0 --end 10`; the export JSON must show `offlineMedia: []` (exit status 1 otherwise) [14]. `ffprobe` the draft. A Fable review of the sample frames happens here.
3. **Hand-off bundle to the maker** (one folder, copied to the Windows PC): `media/` (conformed stills, WAVs), `ch01.otio` (R3 template), `ch01.xml` (FCP7 XML, for Resolve), `build_info.json` (tags, SHA-256 of the Craft binaries, tick/fps settings), and the neutral spec JSON. Do **not** hand over a Linux-path `.fcproj` unless the maker is willing to run `media.autoRelink {from, to}`.
4. **Maker refines in FilmCraft (portable zip, `portable.txt` present):** File > Import > `ch01.otio`; read the import report; check no slate "MEDIA NOT FOUND"; adjust Ken Burns by dragging keyframes in Effect Controls (value and velocity graphs), retime dissolves, add titles with the Type tool, set Essential Sound > Music > Ducking against Dialogue, save the `.fcproj` into the project folder, `File > Save a Copy` at the end of the session.
5. **Back into the pipeline.** Maker exports interchange (`file.exportInterchange` OTIO + FCP7 XML) and marker CSV; commits `.fcproj`. The agent reads ground truth with `filmcraft-cli --project x.fcproj inspect sequence --compact` and diffs against its spec, never re-generating shots the maker has edited. Final render: ProRes 422 HQ master (R6).

### R3. Interchange contract and emitters

**Neutral timeline spec (kept in the repo, one JSON per chapter):** frame rate, sequence size, ordered shots `{id, source, duration_frames, motion:{scale:[a,b], position:[[x,y],[x,y]], ease}, transition_out:{type:"dissolve", frames}, markers:[...]}`, audio cues `{file, start, gain_db, duck_against}`. Emitters: (E1) CLI script for FilmCraft; (E2) `.otio` with `metadata.filmcraft`; (E3) FCP7 XML for Resolve; (E4) "bake-motion" variant (below). Never hand-edit emitted files.

**E2 template (derived from reading `otio.rs`; the file below parses as JSON but has not been loaded by FilmCraft; the spike's T3 must confirm it).** Two stills with a 24-frame dissolve at the cut, a Ken Burns on the first (Float `scale` 66.67 -> 80 with EaseOut, `position` drift), markers on the stack, a music track. Notes: `rate` is the exact frame rate as a float; dissolves use `in_offset`/`out_offset` and consume no timeline time; `duration_ticks`/`source_in_ticks` are optional cross-checks (used only if within 1/1000 s); without `metadata.filmcraft.settings` the sequence is 1920x1080 at the file's rate, so for any other size export a template OTIO from FilmCraft once and copy its `settings` object.

```json
{
  "OTIO_SCHEMA": "Timeline.1",
  "name": "Chapter 01 draft",
  "global_start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0},
  "metadata": {},
  "tracks": {
    "OTIO_SCHEMA": "Stack.1", "name": "tracks", "metadata": {},
    "markers": [{"OTIO_SCHEMA": "Marker.2", "name": "Chapter 01", "comment": "", "color": "GREEN", "metadata": {},
      "marked_range": {"OTIO_SCHEMA": "TimeRange.1",
        "start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0},
        "duration": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0}}}],
    "children": [
      {"OTIO_SCHEMA": "Track.1", "name": "V1", "kind": "Video", "metadata": {}, "children": [
        {"OTIO_SCHEMA": "Clip.2", "name": "ch01_s01", "enabled": true, "markers": [], "effects": [],
         "source_range": {"OTIO_SCHEMA": "TimeRange.1",
           "start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0},
           "duration": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 125.0}},
         "media_references": {"DEFAULT_MEDIA": {"OTIO_SCHEMA": "ExternalReference.1", "name": "ch01_s01.png",
           "target_url": "media/ch01_s01.png", "available_range": null, "metadata": {}}},
         "active_media_reference_key": "DEFAULT_MEDIA",
         "metadata": {"filmcraft": {"scale_to_frame": false, "gain_db": 0.0, "source_in_ticks": 0, "duration_ticks": 1270080000000,
           "effects": [{"effect": "motion", "enabled": true, "params": {
             "scale": {"value": {"Float": 66.67}, "keyframes": [
               {"time": 0, "value": {"Float": 66.67}, "interp": "Linear"},
               {"time": 1270080000000, "value": {"Float": 80.0}, "interp": "EaseOut"}]},
             "position": {"value": {"Vec2": {"x": 960.0, "y": 540.0}}, "keyframes": [
               {"time": 0, "value": {"Vec2": {"x": 960.0, "y": 540.0}}, "interp": "Linear"},
               {"time": 1270080000000, "value": {"Vec2": {"x": 930.0, "y": 520.0}}, "interp": "EaseOut"}]}}}]}}},
        {"OTIO_SCHEMA": "Transition.1", "name": "Cross Dissolve", "transition_type": "SMPTE_Dissolve", "metadata": {},
         "in_offset": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 12.0},
         "out_offset": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 12.0}},
        {"OTIO_SCHEMA": "Clip.2", "name": "ch01_s02", "enabled": true, "markers": [], "effects": [],
         "source_range": {"OTIO_SCHEMA": "TimeRange.1",
           "start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0},
           "duration": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 125.0}},
         "media_references": {"DEFAULT_MEDIA": {"OTIO_SCHEMA": "ExternalReference.1", "name": "ch01_s02.png",
           "target_url": "media/ch01_s02.png", "available_range": null, "metadata": {}}},
         "active_media_reference_key": "DEFAULT_MEDIA", "metadata": {}}]},
      {"OTIO_SCHEMA": "Track.1", "name": "A1", "kind": "Audio", "metadata": {}, "children": [
        {"OTIO_SCHEMA": "Clip.2", "name": "music_bed", "enabled": true, "markers": [], "effects": [],
         "source_range": {"OTIO_SCHEMA": "TimeRange.1",
           "start_time": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 0.0},
           "duration": {"OTIO_SCHEMA": "RationalTime.1", "rate": 25.0, "value": 250.0}},
         "media_references": {"DEFAULT_MEDIA": {"OTIO_SCHEMA": "ExternalReference.1", "name": "mix_ch01.wav",
           "target_url": "media/mix_ch01.wav", "available_range": null, "metadata": {}}},
         "active_media_reference_key": "DEFAULT_MEDIA", "metadata": {}}]}
    ]
  }
}
```

If `metadata.filmcraft.effects` has the wrong shape FilmCraft drops it silently (`effects_from` uses `.ok()`) and imports a plain cut with no Ken Burns [6]; the import report only names effects that are present in OTIO's own `effects` array. So the spike check is: after import, `inspect sequence` must show the `motion` effect with keyframes.

**E3 (FCP7 XML) and the fallback editors.** Prefer exporting it from FilmCraft (`file.exportInterchange {format:"xml"}`) over writing it by hand, because the exporter was built against what Premiere writes [5]. Ask the maker to open it in Resolve free once (R7) and note which of scale/position keyframes, dissolves and levels survive. Scale semantics differ between editors (FilmCraft Scale 100 = native pixels; Final Cut/Resolve Scale 1.0 = fitted); **stills conformed exactly to the sequence size make both agree at 100**, and are the cross-editor-safe choice when Ken Burns moves are re-created by hand in the fallback.

**E4 bake-motion variant (validated: ffmpeg 6.1.1, 2880x1620 PNG in, 125 frames out in about 5.5 s wall on 4 vCPU).** When the fallback must reproduce the move exactly, render each shot to a ProRes intermediate in the container and let the OTIO carry only cuts, dissolves and markers:

```sh
ffmpeg -y -loop 1 -framerate 25 -i IMG_0001.png \
  -vf "zoompan=z='min(1+0.12*on/124,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv422p10le" \
  -frames:v 125 -c:v prores_ks -profile:v 3 -vendor apl0 shot_0001.mov
```

The price is that the maker can no longer drag the move; FilmCraft remains the place for dissolves, titles, levels and export.

### R4. EffectCraft recipes (CLI and MCP; ids from `docs/agents.md` and the cookbook)

Common frame: `effectcraft-cli --project x.ecproj --save ...`; or MCP `batch {steps:[{command,params}], atomic}` where `"$N.key"` reuses an earlier result; render with `effectcraft-cli render --comp Main --out out --format png --channels rgba` (RGBA PNG sequence) or `--format prores --prores 4444 --channels rgba`. Start every comp at `RAYON_NUM_THREADS=1`, and raise the thread count only after a 30-frame sample shows peak memory under half of free RAM (F4). `RAYON_NUM_THREADS=2` reached 6.8 GB in the #1615 reporter's project [47][71]. Save after each milestone (or start `mcp --autosave`).

- **R4a Titles.** Spec JSON -> `comp.new {name,width,height,frameRate,duration}`; `layer.newText {name,text,size,fill}`; fonts only from `list_fonts` (Inter, JetBrains Mono, Noto Serif are bundled; install any other OFL family on the Windows PC and list the files in the repo); `add_keyframe {layer,path:"transform/position",keys:[...],interpolation:"easyEase"}`; text animators for per-character reveals; `render_frame {time, transparent:true}` for review. Output RGBA PNG sequence -> FilmCraft (import with `imageSequence:true`). For one static title or lower third use a FilmCraft graphic clip instead.
- **R4b Parallax.** Layers `NN_name.png` (RGBA) + manifest -> `file.import` each, `file.newCompFromSelection {single:false, dimensionsFrom, duration}` or add as layers; `layer.setSwitch {layers, switch:"threeD", value:true}`; set Z per layer; `layer.newCamera {name}`; keyframe camera position (slow dolly 3-6 percent of depth) with easy ease; optional depth of field; render 1080p25 as RGBA PNG or H.264. Measure CPU ms/frame first (spike T4); if it is above about 3 s/frame, move this effect to the code route.
- **R4c Line-draw.** SVG (ids, strokes, `fill="none"`) -> `edit.pasteSvg {svg}`; for each shape group `layer.addShapeItem {kind:"trim"}`; keyframe Trim Paths End 0 -> 100 with a stagger; background solid; render RGBA PNG. Check each id survives as a group name with `get_layer {layer, flat:true}`.
- **Expression first drafts.** `set_property {layer, path, expression}` for drift (`wiggle(0.3, 12)` on position), breathing scale (`100 + 3*Math.sin(time*0.8)`), reveals (`ease(time, 0, 1.2, 0, 100)`), loops (`loopOut("pingpong")`); then `prop.convertExpressionToKeyframes` before any Lottie export or hand-off where determinism matters.
- **Lottie** only for small web pieces: `exec file.exportLottie '{"comp":"Main","path":"x.json","includeExpressions":false}'`, read the returned warnings list aloud to the maker, and verify in lottie-web (Playwright) because EffectCraft's tests never compared a player.

### R5. Audio: music under voice, interview cleanup, final loudness (no SoundCraft)

All ffmpeg lines were run on ffmpeg 6.1.1 with synthetic signals (pink-noise "music", sine-burst "voice"): syntax valid; ducking measured -10.7 dB at the settings shown (music RMS -27.5 dB alone, -38.2 dB while the voice spoke, back to -27.3 dB after release) [61].

```sh
# Duck music under voice (voice is mono here; music stereo). threshold is linear (0.03 = about -30 dBFS).
ffmpeg -i music.wav -i voice.wav -filter_complex \
 "[1:a]asplit=2[sc][v];[0:a][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=600:makeup=1[duck];\
  [v]pan=stereo|c0=c0|c1=c0[v2];[duck][v2]amix=inputs=2:normalize=0:duration=longest[out]" \
 -map "[out]" -ar 48000 -c:a pcm_s24le mix.wav

# Loudness, pass 1 (measure) then pass 2 (linear mode with the measured values). Target is the maker's choice, see below.
ffmpeg -i mix.wav -af loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i mix.wav -af "loudnorm=I=-18:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" -ar 48000 -c:a pcm_s24le master_audio.wav

# Verify
ffmpeg -nostats -i master_audio.wav -af ebur128=peak=true -f null -
```

Interview cleanup choices, in order: (1) record clean (phone voice memo at 48 kHz WAV/FLAC if possible, close mic, quiet room); (2) FilmCraft Essential Sound > Dialogue > Repair (Reduce Noise, Reduce Rumble, DeHum 50/60 Hz, DeEss, Reduce Reverb) and Clarity, tested on synthetic material only [17]; (3) Audacity noise reduction and spectral tools; (4) ffmpeg `afftdn`/`highpass`. Never "enhance" a voice with a generative model, and never synthesise speech in a relative's voice (Principle 4); FilmCraft's Kokoro TTS is for neutral credits or narration, labelled, and off in release builds [13][19].

**Loudness target is a maker decision tied to the venue**: -23 LUFS integrated (EBU R128, broadcast), about -16 to -18 LUFS for home/online stereo, with true peak at or below -1.5 dBTP. FilmCraft's `Export > Loudness Normalization` defaults to -23 LUFS and -2 dBTP, off by default [11].

### R6. Export recipe (archive master, premiere copy, verification)

1. **Master:** FilmCraft preset "Apple ProRes 422 HQ" at the sequence size and rate, 48 kHz 24-bit PCM. (`filmcraft-cli --project x.fcproj export master.mov --preset "Apple ProRes 422 HQ"`.) If alpha or banding-sensitive gradients matter use "Apple ProRes 4444".
2. **Premiere copy (validated: ffmpeg 6.1.1):** `ffmpeg -i master.mov -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 320k premiere.mp4`. Add `-vf scale=3840:2160:flags=lanczos` only if the venue projects 4K and the sequence was built at 4K. Always produce a second, small safety copy (1080p, CRF 20, `-profile:v high -level 4.1`) for the venue laptop.
3. **Verify:** `ffprobe` (codec, pix_fmt, frame count equals sequence duration, `r_frame_rate`), play the first/last 10 s and a mid-dissolve, `ebur128` on the audio, and compare three frames against `filmcraft-cli render` frames.
4. **Archive:** master, `.fcproj`, OTIO, FCP7 XML, media manifest with SHA-256, tool tags, on two copies (review 00 media rule).

### R7. Maker's five-minute acceptance tests on Windows (run before the pin is final)

Common: download the **portable x64 zip** from the GitHub release, verify `Get-FileHash -Algorithm SHA256` against the table in Q1, unzip into `C:\LifeJourney\tools\<app>-<tag>\`. Keep the Launcher out of it. Note RAM use in Task Manager.

- **FilmCraft (5 min).** (1) Run `filmcraft.exe`. If the window flashes and exits, in PowerShell run `$env:WGPU_BACKEND="vulkan"; .\filmcraft.exe`, then `"dx12"`, then `.\filmcraft.exe --graphics software` [1][13]. (2) `.\filmcraft-cli.exe --version`. (3) File > Import the agent's `ch01.otio`; the import report must not say "not supported" for the motion effect, and the viewer must not show the red "MEDIA NOT FOUND" slate. (4) Play 10 s: Ken Burns moves, dissolve works. (5) Drag a Scale keyframe, Ctrl+S, close, reopen, confirm it persisted and an `Auto-Save` folder exists next to the file. (6) Export "High Quality 1080p HD" for the whole chapter, note wall time and play the MP4 (corrected 2026-10-20: this note first said 20 s; the synthetic test chapter `research/craft-motion-fixtures/ch01.otio` is 10 s long, so that is the export). (7) Pass if (3)-(6) work and RAM stays under about 4 GB.
- **FilmCraft + Resolve free (5 min, once).** Revised by F2 and G2. In DaVinci Resolve (File > Import Timeline, or Media Pool right-click > Timelines > Import), import `ch01.xml` with **Use sizing information** ticked and **Mixed frame rate format** left on 'DaVinci Resolve'. Check: stills online; each still 5 s (not one frame, not 29.97-based); Inspector > Edit Sizing shows Zoom and Position keyframes at the right frames; Opacity keyframes in Composite; dissolves present. Then import `ch01.otio` and note what is lost; record Help > About. G2 and G1 add a relative-path check (`ch01.otio` copied alone into an empty folder) and two FCPXML checks. This answers the UNVERIFIED cells in Q3.
- **EffectCraft (5 min).** Run `effectcraft.exe`; if it fails, `$env:WGPU_BACKEND="vulkan"` (the Direct3D 12 compositor is a known failure, #613 [24]); import an RGBA PNG; open the agent's `.ecproj`; check that the title font is the intended one (a fallback to Inter means the family is not installed); render 5 s as PNG sequence; confirm the PNGs have alpha; close and reopen.
- **SoundCraft (2 min, optional).** Open the demo, press Space (audio device works?), `File > Bounce Mix` to WAV. Do not import MP3/AAC for work.

### R8. Week-1 Design spike S1 "Craft headless in the container" — scope (written, NOT run)

**Goal.** Decide whether the Craft CLIs are a container **render engine** for agents (CPU, no GPU) or only a maker-side **refinement** tool. Out of scope here: any building from source.

**Environment to record first:** `uname -a; nproc; free -m; ldd --version | head -1; ffmpeg -version | head -1`. Reference container on 2026-10-18: Ubuntu 24.04.5, glibc 2.39, 4 CPUs, 16 GB RAM, 252 GB disk, ffmpeg 6.1.1, ImageMagick 6.9.12, Python 3, Node 22, no GPU, no Chromium/Playwright [62]. Required system libraries named by the deb dependencies (`libc6>=2.35, libgcc-s1, libxkbcommon0, libvulkan1|libegl1, libasound2t64`) are already installed in that image. No `apt-get` is needed to run the tar.gz CLIs.

**Packages (use the tar.gz, no root, no postinst).** Base URL `https://github.com/storytold/<repo>/releases/download/<tag>/<asset>` (302 to the release-asset host; `curl -L`). Verify with `sha256sum -c`.

| Asset | SHA-256 [40] |
|---|---|
| `filmcraft-0.8.0-linux-x86_64.tar.gz` | `b166877905ae8a1b5505066d6dde60d7ce05831cfb309bacd5d7970f4bb017e1` |
| `effectcraft-0.11.1-linux-x86_64.tar.gz` | `b9cb2ce68dd66458cc164437e431376e94e38e33e3b6529fa8fd45f8cf968934` |
| `soundcraft-0.8.0-linux-x86_64.tar.gz` | `57a2b8776d51880cee69118568a396c09faca6949dcbf50f19879d71d596f5cc` |
| `filmcraft-web-0.8.0.zip` (optional T6) | `6b13956fc741522427663517b1e483d6e0777891063fed02b1bd94bfada8a6c7` |
| `effectcraft-web-0.11.1.zip` (optional T6) | `8675e595d876408ce23d868d8530f17466029650da727d742028484cbde8a207` |

Each tarball unpacks to `<name>-<ver>-linux-x86_64/bin/<app>` and `bin/<app>-cli` [15][31][38]. Run each CLI once with `--version`; run `ldd` on it and record the list (the packaging comments say only glibc and libgcc_s are linked directly).

**Test content (generate in the container).** 20 and then 300 stills at 3600x2400 (ImageMagick gradients plus a numbered grid and text), conformed copies at 2880x1620 (R1), one 10 s 1080p25 H.264 clip and one 48 kHz stereo WAV (ffmpeg `testsrc2` / `sine`), a 30 s music-like and a 30 s voice-like WAV (R5).

| Test | Commands | Measure | Pass / fail |
|---|---|---|---|
| **T1 smoke** | `<cli> --version`; `filmcraft-cli commands \| head`; `effectcraft-cli info --json`; `soundcraft-cli commands \| head` | exit code, stderr, time | Pass: exit 0, no GPU error with `VK_ICD_FILENAMES` unset, no missing library |
| **T2 FilmCraft stills** | Driver script (Python, outside the vendor folders) calling `filmcraft-cli --project t2.fcproj --save exec ...` per R2 for N = 5, 20, 100, 300 stills of 3600x2400 and again with the 2880x1620 conformed set; then `export out.mp4 --preset "High Quality 1080p HD"` and `export out.mov --preset "Apple ProRes 422 HQ"` under `/usr/bin/time -v` | wall time, user+sys CPU, **max RSS**, frames/s = frames / wall, RSS slope per still = (RSS(N=100) - RSS(N=20)) / 80, preview-cache size on disk, exit code, `offlineMedia` | Pass (all required): no crash or hang at N = 100 (3600x2400) and N = 300 (conformed); H.264 export of 3,000 frames (20 stills x 5 s, 1080p25) completes in < 10 min on 4 vCPU (>= 5 fps) [E]; RSS slope < 40 MB per still (the inferred 35 MB) and RSS(N=300, conformed) < 12 GB; `ffprobe` frame count equals expected and `ffmpeg -v error -i out.mov -f null -` prints nothing; Ken Burns first/last frame positions of a gridded test still within 1 px of the computed values; mid-dissolve pixel within 2 levels of the average of the neighbours [amended 2026-10-20: the mark is the 50/50 mix of the neighbours in linear light, same 2-level tolerance, because FilmCraft blends in linear light and the average of the encoded values cannot be passed (the first wording failed by 28.50 levels); a second mark was added, at least 11 distinct levels over a 12-frame exported dissolve, judged on the export because the single-frame `render --seconds` probe shows pairs of equal frames and the export does not (R2, step 2); see the T2 row of `spikes/VERDICTS-W2.md`]. Record actual fps for H.264 and ProRes. Fail path: the container is demoted to ffmpeg/code rendering; FilmCraft is maker-side only |
| **T3 Interchange** | Write the R3 OTIO (plain and with metadata), a hand-made FCP7 XML and an FCPXML with `asset-clip`; `filmcraft-cli --project t3.fcproj --save exec file.import '{"paths":["/work/ch01.otio"]}'`; `inspect sequence`; `exec file.exportInterchange` to otio/xml/fcpxml/edl and diff the re-import | import report text, clip count, durations, transitions, `motion` keyframes present, offline count | Pass: plain OTIO gives correct durations and dissolve and **no** motion (expected); metadata OTIO gives the motion keyframes; FCPXML `<video>` produces the documented skip warning; exported OTIO from FilmCraft can be used as the template for sequence settings. Also validate the OTIO with the `opentimelineio` Python package in a venv (`pip install opentimelineio`) [optional] |
| **T4 EffectCraft** | Build with `run_script` or `exec` a 1080p25 4 s title comp (text, shape layer with Trim Paths, `wiggle`), a pasted SVG line-draw, and a 5-layer classic-3D parallax comp; `RAYON_NUM_THREADS=1 /usr/bin/time -v effectcraft-cli render --comp Main --out out --format png --channels rgba`; also `--format prores --prores 4444 --channels rgba` and `--format h264`; repeat the parallax comp with default threads; `render-frame --transparent` for frame 0 | ms/frame, max RSS, output sizes, ffprobe pix_fmt (`rgba` for PNG, `yuva444p12le` expected for ProRes 4444), colour tags of the 4444 file (#340) | Pass: no OOM at 1080p with default threads for the title and line-draw comps; parallax comp renders at < 3 s/frame at the thread count the F4 procedure allows (start at 1) and < 6 GB RSS; PNGs have alpha; 4444 file decodes in ffmpeg with no errors; expression comps produce identical frames on two runs (determinism); `ffprobe` of a deliberately OOM-killed H.264 render shows the missing `moov` (documents #1615 for the pipeline's guard) |
| **T4b Lottie** | `exec file.exportLottie` on the title comp with and without `includeExpressions`; parse the JSON; load it in lottie-web 5.12.x in headless Chromium if Playwright is available | warnings list, file size, SSIM of frame vs `render-frame` | Pass: warnings list is non-empty for unsupported items and equals the list in Q6; baked comp renders in lottie-web within SSIM 0.95 of EffectCraft's frame. Skip if no browser |
| **T5 SoundCraft** | `soundcraft-cli run --demo --cmd 'mix.volume={"track":"Kick","db":-6}' --bounce mix.wav`; import the WAV/FLAC test files, bounce to 24-bit WAV; import an MP3 made by ffmpeg `libmp3lame` and a Windows-Media-Foundation-style MP3 if available | bounce JSON (`peak_db`, `lufs`, `true_peak_db`), `ebur128` of the same file, duration and frame counts vs ffprobe | Pass: LUFS within 0.3 LU of ffmpeg `ebur128`; WAV/FLAC round-trip sample-exact; the MP3 case confirms or refutes #710 (expected to confirm for some files). This test only supports the verdict; it does not gate anything |
| **T6 Web (optional)** | Serve the unzipped web build with `python3 -m http.server -d <dir> 8765` (or any server that sends `application/wasm`); Playwright/Chromium headless with `--use-angle=swiftshader`/`--enable-unsafe-webgpu`; open `/?cpu`; call `await filmcraft.info()`, `filmcraft.importFiles`, `filmcraft.execute("file.exportMedia", ...)`, `filmcraft.screenshot()` | load time, panics, screenshot | Pass: demo loads, `info().compositor` reports CPU/WebGL, no "stopped working" overlay, a screenshot is produced. Purpose: UI learning and annotated screenshots only |

**What to log for every run:** tool tag + SHA-256, commands, `nproc`/RAM, wall/CPU/RSS, exit codes, ffprobe JSON, and a one-line verdict. **Decision rule:** if T2 and T4 pass, agents may render drafts and chapters with the Craft CLIs in the container (still producing OTIO and ffmpeg fallbacks); if T2 fails, FilmCraft stays maker-side and the container renders with ffmpeg/code; if T4 fails on memory or speed, EffectCraft is limited to titles and line-draw on the maker's PC.


---

## Tools and formats (cost and status as of 2026-10-18)

| Tool | Cost / licence | Platform | Maturity | Scriptability | Notes for this project |
|---|---|---|---|---|---|
| **FilmCraft** v0.8.0 | free, MIT or Apache-2.0 [1] | Windows x64/x86/arm64, macOS, Linux, web | alpha; "ready for real work ~56%" (vendor, re-measured 2026-10-10) [1]; macOS best tested | `filmcraft-cli` (commands, `exec`, `run`, `import`, `export --preset`, `render`, `probe`, `inspect`, `mcp`), loopback JSON-lines control channel, `window.filmcraft` on the web [14][16] | Cut, Ken Burns, dissolves, titles, Essential Sound, ProRes/H.264 export. 8-bit stills, no ICC/EXIF. CPU compositing for Lumetri |
| **EffectCraft** v0.11.1 | free, MIT or Apache-2.0 [20] | same | alpha; "about 45% of the way to replacing After Effects" (vendor) [20][22]; one AE oracle only | `effectcraft-cli` (`exec`, `run`, `set`, `get`, `props`, `render`, `render-frame`, `script FILE.jsx`, `mcp`), JS expressions/scripts on boa, control channel, `window.effectcraft` [21][30] | Titles, line-draw, short motion. CPU renders have no memory cap. No `.aep` |
| **SoundCraft** v0.8.0 | free, MIT or Apache-2.0 [33] | same (zip has no `portable.txt`) | pre-alpha, ~40% (vendor) [33] | `soundcraft-cli` (`run --cmd`, `convert`, `script`, `mcp` with read/write roots), control channel [37] | Learning only; no sidechain; import timing bugs |
| **ffmpeg** 6.1.1 (in container) | free (GPL/LGPL builds) | all | mature | everything | Pre-flight, ducking (`sidechaincompress`), loudness (`loudnorm`, `ebur128`), premiere encode, Ken Burns bake (`zoompan`) [61] |
| **ImageMagick** 6.9.12 (in container) | free | all | mature | CLI | Stills conform (R1) [62] |
| **DaVinci Resolve 21** | free edition: 8-bit video up to UHD 60 fps; Studio paid [55] | Windows, macOS, Linux | mature | Python API (not assessed) | Fallback editor; OTIO native since 18.5 per a secondary source [56]; FCPXML/FCP7 XML/EDL import; free vs Studio import limits not stated |
| **Kdenlive 26.08.2** | free, GPL | Windows, macOS, Linux | mature | MLT XML, limited | Fallback editor; OTIO only (tracks, clips, markers) [49][51]; aborts import if media is missing [54] |
| **Audacity** | free, GPL | all | mature | macros, mod-script-pipe | Fallback for voice work (noise reduction; an Auto Duck effect exists in Audacity, background knowledge, not re-checked here) |
| **Blender VSE/compositor, Natron, Shotcut** | free | all | mature | Python / project XML | Fallbacks named in the brief; not studied in this track (agent-pipeline covers Blender) |
| **ArtCraft Launcher** | free | Windows, macOS, Linux | early alpha | n/a | Installs and auto-updates all apps from GitHub; do not use for production pins [63] |

| Format | Where | Notes |
|---|---|---|
| `.fcproj` | FilmCraft | JSON, schema 15 at v0.8.0, ticks, absolute media paths, atomic saves [2][3] |
| `.ecproj` | EffectCraft | JSON, schema 2, property tree with uids, absolute footage paths, `savedBy` [29] |
| `.scraft` + `Audio Files/` | SoundCraft | JSON `format_version` 1 [35] |
| OTIO `.otio` | FilmCraft in/out; Kdenlive in/out; Resolve in/out | Portable cut list; Ken Burns/levels only via `metadata.filmcraft` [6][51][56] |
| FCP7 XML `.xml` | FilmCraft in/out; Resolve in | Best carrier of Basic Motion keyframes, opacity, audio levels [8] |
| FCPXML 1.9-1.11 | FilmCraft in/out; Resolve in | stills must be `asset-clip` for FilmCraft [7] |
| CMX 3600 EDL | FilmCraft in/out; Resolve in | cuts, dissolves, speed, markers only [8] |
| Lottie `.json`/`.lottie` | EffectCraft in/out | lossy by design (Q6 list) [26] |
| SVG | EffectCraft in (static subset) | ids survive as group names; no text/clip/mask/filter [27] |
| PNG/EXR sequences, ProRes 4444 | EffectCraft out; FilmCraft in | RGBA PNG is the safe alpha hand-off (#340 colour tag) [22][1] |
| ProRes 422 HQ, DNxHR, H.264 | FilmCraft out | master/archive/premiere roles in R6 [11][18] |
| WAV/FLAC 48 kHz 24-bit | all | the only audio formats SoundCraft imports sample-exactly [48] |

### Feature evidence table (watch-out: rate by tests and oracles, not by presence)

| Feature we need | App | Evidence at the tag | Rating |
|---|---|---|---|
| H.264/HEVC/ProRes/AAC decode | FilmCraft | bit-exact against ffmpeg on conformance and generated fixtures; phone/camera files in the wild less tested; 92-file corpus run: all open, frame-rate misdetection on 30 files (#1959) [18][46] | oracle-tested, real-world gaps |
| H.264 and ProRes encode | FilmCraft | H.264 output decoded by ffmpeg is bit-identical to the encoder's reconstruction; ProRes decode oracle on 29 fixtures and an encode oracle on every profile; no quality parity with x264 claimed [18] | oracle-tested; quality below x264 slow |
| Loudness meter and normalisation | FilmCraft | `loudness_oracle.rs` vs ffmpeg `ebur128`; Essential Sound auto-match +-0.5 LU on synthetic speech [17] | oracle-tested |
| Motion/Opacity/dissolve compositing | FilmCraft | unit tests, golden images (CPU vs committed PNGs, GPU vs CPU) [17] | tested, no external renderer oracle (gap G1) [13] |
| Stills: orientation, ICC, 16-bit | FilmCraft | none found; `to_rgba8` | code-only gap |
| Proxies for stills | FilmCraft | none found | not available (UNVERIFIED) |
| OTIO/FCPXML/FCP7/EDL import | FilmCraft | hand-written golden documents + self round trips; never with a real Resolve/Kdenlive/Final Cut file | tested (self) |
| Essential Sound ducking | FilmCraft | project of dialogue + music: keyframes within 60 ms, -15.00 dB [17] | tested (synthetic) |
| Scalar ease | EffectCraft | After Effects 26.3 comparison, 168 samples, max error 3e-11 deg [22] | oracle-tested (only item) |
| Expressions | EffectCraft | 103 unit tests + fuzz; `wiggle` is not AE's noise [25] | tested, no AE oracle |
| Trim Paths, shape layers | EffectCraft | unit tests in `render/src/shapes/tests.rs` | tested |
| SVG import | EffectCraft | 11 unit tests, 2 fixtures, pixel checks of pasted rects [27] | tested (small), no browser/resvg oracle |
| PSD import | EffectCraft | spec-derived; fixtures from the repo's own writer [28] | tested (self) |
| Lottie import/export | EffectCraft | self round trips with render comparison, 4 fixtures [26] | tested (self), no player oracle |
| ProRes 4444 alpha export | EffectCraft | decode oracle against ffmpeg for alpha; colour tag bug #340 [22] | tested, known tag bug |
| CPU render memory | EffectCraft | no cap; critical OOM issue [47] | failing |
| WAV/FLAC/AIFF I/O | SoundCraft | 20 of 20 lossless references sample-exact [48] | tested |
| MP3/AAC/HE-AAC import | SoundCraft | frames dropped / edit lists ignored (#710, #707, #712) [48] | failing |
| Session file | SoundCraft | serde JSON, mutated-file property test [34][35] | tested |
| LUFS meter | SoundCraft | synthetic tones only; no LRA; no oracle [36] | tested (synthetic) |

---

## Risks, pitfalls and ethics (with mitigations and fallbacks)

**Rating key:** impact on a learner producing one finished film by 2027-02-27. Data-loss risk is per Q9.

| App | Overall dependency risk | Data-loss risk | Main failure modes | Mitigation | Proven free fallback for the same step |
|---|---|---|---|---|---|
| **FilmCraft** | MEDIUM-HIGH if on the critical path; MEDIUM as a refinement layer | LOW-MEDIUM | Windows start-up driver crashes (AMD, Intel UHD/HD); exports exhausting RAM/disk; stills unbounded in RAM; 8-bit stills without ICC/EXIF; interchange never checked against a real Resolve/Kdenlive file; schema moves daily | Portable zip + `WGPU_BACKEND`/`--graphics`; pre-conform stills; chapters of about 1-2 minutes; no playback during export; keep Auto-Save on; spec + OTIO in git | DaVinci Resolve free (FCP7 XML or OTIO); Kdenlive (OTIO); Shotcut; Blender VSE; **code route**: ffmpeg `zoompan`/`xfade`, or the agent-pipeline code-to-video frameworks (bake-motion variant R3-E4) |
| **EffectCraft** | HIGH | MEDIUM | 17-day-old code; only one AE comparison; 449 open issues; CPU render OOM and truncated MP4s; Direct3D 12 compositor failure on Windows; font fallback to Inter; expression-editor corruption; Lottie loses effects, video and 3D | Use only for titles, line-draw, short motion; start at `RAYON_NUM_THREADS=1` and measure peak memory (F4); render to new file names; RGBA PNG hand-offs; fonts installed or text outlined; save often | Code-driven motion (Remotion, Motion Canvas, CSS/GSAP in headless Chromium, per agent-pipeline); Blender compositor; Natron; Kdenlive title editor; Inkscape + SVG animation for line-draw |
| **SoundCraft** | HIGH (do not depend) | MEDIUM sessions / HIGH silent audio errors | no sidechain, MP3/AAC timing bugs, whole-file RAM, VST3 crash, pre-alpha | Learning only; WAV/FLAC only; never the sole copy of an interview | Audacity + ffmpeg `sidechaincompress` + `loudnorm`; FilmCraft Essential Sound for in-timeline ducking |

**Pitfalls (specific and checkable).**
1. **Marketing counts drift.** FilmCraft: website "about 55 video effects", README 93; EffectCraft: 259 vs 306 effects; README percentages are vendor estimates [1][41][20]. Quote tags and tests.
2. **Docs lag code.** FilmCraft schema 13 (doc) vs 15 (code); EffectCraft gap 18 "no relinking" vs `docs/footage.md` relink commands; SoundCraft G-06 says recording goes to RAM while v0.7.0 notes say takes are kept on crash; the SoundCraft site shows 0.5.0 while v0.8.0 exists [2][3][22][23][34][44].
3. **Scale and units.** FilmCraft Scale 100 = native pixels, position = sequence pixels from top-left, ticks not frames; Resolve/Final Cut Scale 1.0 = fit. The cross-editor-safe stills are conformed exactly to the sequence size [11][7].
4. **FCPXML `<video>`/`<title>` are skipped by FilmCraft** (reported as warnings); FCPXML import/export has been tested only against FilmCraft's own output and a hand-written Final Cut-style document [7].
5. **Kdenlive aborts on missing media and flips V/A track order when its OTIO goes to Resolve** [54]; use stable absolute paths under one project root and one track-order convention.
6. **Plain OTIO has no Ken Burns, opacity or audio gain**; do not expect any NLE to read transforms from OTIO [6][52].
7. **Lottie "export works" is not "player renders it"**; warnings lists must be read, expressions baked, effects removed [26].
8. **CPU render memory in EffectCraft and FilmCraft** (items in Q7/Q4/Q9): render in the container with explicit thread caps, one process per render, and verify outputs with `ffprobe`.
9. **Windows GPU start-up**: both an AMD (`atio6axx.dll`, `amdvlk64.dll`) and an Intel (`igvk64.dll`) crash class are documented; the fix is a backend override or `--graphics` flag, not a different install [1][13][31].
10. **Phone/VHS inputs** go through R1 first (HEVC HLG fails in FilmCraft on Windows today).
11. **Bug-report channel leaks content.** The Discord-to-GitHub ticket bot files public issues; reports with file names, screenshots or clips of family material would be public. Reproduce with synthetic test cards only [45][46].
12. **Surprise leakage on the maker's PC.** FilmCraft keeps project, `Auto-Save/` copies, `Recovery/` snapshots, `Media Cache` previews and preferences (recent projects) under the project folder or `%APPDATA%\FilmCraft` (portable mode moves them to `data\` beside the exe); EffectCraft keeps auto-saves under `EffectCraft Auto-Save/` and settings in its config folder (portable mode via `portable.txt`); SoundCraft writes `Autosave/`, `logs/` and `ui.json` under `%APPDATA%\SoundCraft\` and its zip has no `portable.txt` [2][31][33][38]. Use the portable zips and put every working folder on one encrypted drive; never launch from the Launcher on a shared machine; clear recent-file lists before the maker's mother could use the PC.
13. **Any process on the maker's machine can drive an app that was started with `--control PORT`** (loopback, no token); start the control channel only for a session and never leave it running. FilmCraft's MCP server cannot be folder-confined [14].

**Ethics and honesty about real memories.**
- The Craft apps contain AI-ish features that matter here: FilmCraft Text-to-Speech (Kokoro-82M) and optional Whisper transcription (both off or optional in release builds [13][19]); EffectCraft Roto Brush (MobileSAM) and face tracking (MediaPipe), optional downloads [20]. Using them to cut out or track people in real photos is restyling; **never use TTS or any model to generate speech in a relative's voice or words they did not say** (Principle 4). If TTS narrates a credit line, label it as synthetic.
- Parallax and line-draw on a real photograph are animation of a real image (labelled per the imagery track's ladder), not reconstruction; a cut-out background that invents scenery is a visible reconstruction and gets the house look.
- Transcripts of interviews (Whisper) must stay local; the download step is the only network call and happens with a pinned SHA-256.
- Dignity: audio of hard chapters recorded for the proxy reviewer should not sit in cloud-synced folders. Windows setups often sync Desktop, Documents and Pictures to OneDrive by default (UNVERIFIED for this PC), so keep the working folders and each app's data folder outside synced locations (a dedicated encrypted drive or folder) and check sync status before the first import of real material.

### What this means for Life Journey
- Plan the film as chapters built by agents in the container (conformed stills, ffmpeg-mixed audio, OTIO + neutral spec in git) and **refined in FilmCraft on the maker's Windows PC**; keep EffectCraft for a few titles and one line-draw; treat SoundCraft as irrelevant to delivery.
- The pipeline survives the loss of every Craft app, because the spec, the media manifest, the OTIO/FCP7 XML, the ffmpeg audio recipe and the bake-motion variant live in the repo and open in Resolve free or Kdenlive.
- The only gating tests are cheap: the spike S1 (one day in the container) and the maker's five-minute acceptance tests (R7). Run both in week 1-2 and write the tags into the repo.
- Agent-written OTIO uses relative `target_url`s: Kdenlive does not decode `file://` URLs [72], and FilmCraft reads relative paths [5]. Keep one fixed project root, so the relative layout holds.

---

## Open questions / gaps

1. **Not run.** Nothing was built or executed from the repos, so every performance and behaviour claim is from code, vendor benchmarks or issue reports. The spike S1 (R8) closes this.
2. **Maker hardware unknown** (CPU, RAM, GPU/driver, disk). The decision table in Q4 is keyed on core count; replace estimates with S1 + R7 numbers. In particular whether the maker has an NVIDIA GPU (NVENC) or an AMD/Intel GPU affected by the documented driver crashes.
3. **Resolve free and Kdenlive on real files.** Resolve's manual [74] supports FCP 7 XML Opacity, Position, Scale and Rotation keyframes at format level, with 'Use sizing information' ticked; FilmCraft's numbers in Resolve are untested and are the maker's R7 test, as are stills, dissolves and levels. Kdenlive's OTIO import is read from code [72], not run, and its still-image clips are sized by code and untested. Resolve's relative `target_url` handling and its `.otioz` route with stills are UNVERIFIED (G2).
4. **FCPXML stills.** What Resolve 21 writes for a still in FCPXML, and whether it reads FilmCraft's `asset-clip` stills, are UNVERIFIED after a second search (G1). Final Cut writes a bare `<video>` in one sample (F1), which FilmCraft skips. The maker's check is in G1.
5. **Proxy path for stills in FilmCraft** and **eviction behaviour of the source pool** are inferred from code; confirm with S1 T2 (RSS slope).
6. **EffectCraft text and 3D on CPU**: no CPU numbers for classic 3D, text animators or Trim Paths; the only published CPU numbers are #1615 and the Advanced 3D figure.
7. **EffectCraft Lottie in a real player:** unchecked; S1 T4b if a browser is available. Installing Playwright browsers in the container is UNVERIFIED.
8. **SoundCraft:** whether v0.8.0 fixed the MP3/AAC import bugs (they were filed against 0.7.0 on 2026-10-16/17) and whether any free CLAP plugin of use runs on Windows are not checked. Not on the critical path.
9. **Release assets beyond SHA256SUMS.** I verified the release asset list and checksums, not the binaries themselves; code-signing status of the downloaded MSI/zip should be checked on Windows (`Get-AuthenticodeSignature`).
10. **Issue counts** (710 / 449 / 62-open "Windows" search) come from GitHub pages read through a summarising tool and mix open and closed items in places; re-read the linked issues before quoting a number outside this note.
11. **Part 0 of review 01 should be amended** (schema 15, web headers, SVG import, WebFetch reachability) before the scribes turn it into a playbook.
12. **Colour management end to end** (sRGB stills, Rec.709 sequence, ProRes tags, the 4444 tag bug, the venue projector) needs a test card pass; not studied beyond what is cited.

---

## Sources

Repo evidence is cited as `repo/path @tag`. Tags: filmcraft **v0.8.0** (`f03e21556d8e3a7155b91892d958debd5255d7af`, 2026-10-14T10:15:06-04:00); effectcraft **v0.11.1** (`2a01226894c6bc58ae4fadcc24a10198d693acaa`, 2026-10-17T19:03:26-04:00); soundcraft **v0.8.0** (`2578ea69a388395ddadb6394d7b4ab40f21aa670`, 2026-10-17T17:16:15-04:00). Clone URLs: `https://github.com/storytold/filmcraft`, `https://github.com/storytold/effectcraft`, `https://github.com/storytold/soundcraft` (read 2026-10-18 into `<scratch>/vendor/<repo>`; scratch, ephemeral).

**FilmCraft**
- [1] filmcraft/README.md @v0.8.0 — status, formats, export, interchange, agents, downloads, Windows `WGPU_BACKEND` note (vendor claims).
- [2] filmcraft/docs/project-files.md @v0.8.0 — `.fcproj`, schema history to 13 (stale), atomic saves, auto-save, recovery journal, proxies, ingest.
- [3] filmcraft/crates/format/src/lib.rs and tests/fixtures/*.fcproj @v0.8.0 — `MIGRATIONS` (14), `SCHEMA_VERSION` 15, decode/validate, minimal fixtures.
- [4] filmcraft/crates/project/src/{lib.rs,keyframe.rs,effect.rs} and crates/time/src/lib.rs @v0.8.0 — data model, `TrackItem`, `Param`, `Keyframe`, ticks (254,016,000,000/s).
- [5] filmcraft/crates/interchange/{README.md,src/lib.rs,src/common.rs} @v0.8.0 — formats, nested sequences, graphics not carried, path resolution.
- [6] filmcraft/crates/interchange/src/otio.rs and tests/otio.rs @v0.8.0 — OTIO import/export mapping, `metadata.filmcraft`, golden and round-trip tests.
- [7] filmcraft/crates/interchange/src/fcpxml.rs and tests/fcpxml.rs @v0.8.0 — `adjust-transform/blend/volume`, `timeMap`, skipped elements, tests.
- [8] filmcraft/crates/interchange/src/{edl.rs,fcp7.rs} and tests/{edl,fcp7}.rs @v0.8.0 — EDL and FCP7 XML support and tests.
- [9] filmcraft/crates/engine/src/{interchange.rs,commands.rs,media_pool.rs} @v0.8.0 — import then link media; `timeline.place`, `effects.setParam`, `sequence.applyVideoTransition`, `file.newSequence`; media pool without eviction.
- [10] filmcraft/crates/media/src/{still.rs,lib.rs} and crates/media/Cargo.toml @v0.8.0 — still decode to 8-bit RGBA, `image` crate features, default 5 s duration.
- [11] filmcraft/crates/render/src/lib.rs (`motion_matrix`), crates/export/src/{presets.rs,settings.rs} @v0.8.0 — Motion semantics, `scale_to_frame`, export presets, loudness-normalisation defaults.
- [12] filmcraft/docs/performance.md @v0.8.0 — vendor benchmarks (Xeon/RTX 5060 Windows 11, M1, M4 Pro, Ryzen 9700X/RX 7900), memory notes.
- [13] filmcraft/docs/{gaps.md,target-app-parity.md} and ROADMAP.md @v0.8.0 — ranked gaps G1-G20 (reviewed 2026-10-10), Windows/Linux items, hardware status, release log.
- [14] filmcraft/docs/agents.md and apps/filmcraft-cli/src/main.rs @v0.8.0 — MCP/CLI/control channel, install locations, CLI usage, GPU renderer registration, no folder confinement.
- [15] filmcraft/packaging/{windows/filmcraft.wxs,windows/package.ps1,linux/nfpm.yaml,linux/package.sh,web/README.md,web/_headers} @v0.8.0 — CLI in MSI/zip/deb/tar, dependencies, static CRT, web hosting headers.
- [16] filmcraft/docs/web.md, apps/filmcraft-web/{web/index.html,tests/smoke.mjs} @v0.8.0 — web build, URL flags, `window.filmcraft`, "FilmCraft stopped working" overlay, CDP smoke test.
- [17] filmcraft/docs/architecture.md section 5.2, crates/project/src/essential.rs, crates/audio-dsp/tests/loudness_oracle.rs, docs/testing.md @v0.8.0 — Essential Sound ducking/repair/loudness, ffmpeg `ebur128` oracle, test evidence.
- [18] filmcraft/crates/h264enc/README.md and crates/prores/README.md @v0.8.0 — encoder features/limits, ffmpeg oracle verification.
- [19] filmcraft network-audit greps: Cargo.lock, crates/speech/{Cargo.toml,src/models.rs}, crates/automation/src/bridge.rs, apps/filmcraft/src/control_server.rs @v0.8.0.

**EffectCraft**
- [20] effectcraft/README.md @v0.11.1 — features, Lottie, agents, status ("first commit 1 October 2026", 91% / 45%), downloads, "No telemetry".
- [21] effectcraft/docs/agents.md @v0.11.1 — MCP tools, headless CPU default, `--autosave`, install locations, cookbook, pitfalls.
- [22] effectcraft/docs/{gaps.md,target-app-parity.md} @v0.11.1 — dimensions, 216 open issues on 2026-10-12, stability, fidelity (168-sample AE comparison), gaps 1-21, Advanced 3D CPU/GPU timings.
- [23] effectcraft/docs/{file-format-parity.md,footage.md} @v0.11.1 — import/export formats, sequences, Interpret Footage, relinking.
- [24] effectcraft/docs/{hardware-parity.md,web.md} @v0.11.1 — Windows Direct3D 12 failure #613, web build, `window.effectcraft`.
- [25] effectcraft/crates/expr/{Cargo.toml,src/lib.rs,src/tests.rs,src/noise.rs,src/prelude.js}, docs/architecture.md sections 5 and 5a, crates/engine/src/commands/prop.rs and tests_timeline.rs @v0.11.1 — boa, object model, tests, limits, scripting, convert-expression-to-keyframes.
- [26] effectcraft/crates/lottie/src/{lib.rs,export.rs,anim.rs,shapes.rs,text.rs,tests.rs} and tests/fixtures @v0.11.1 — Lottie import/export, warnings (cannot-express list), tests.
- [27] effectcraft/crates/svg/{README.md,src/lib.rs,src/tests.rs}, crates/engine/src/{vector.rs,tests_vector_import.rs} @v0.11.1 — SVG import subset, id naming, paste test.
- [28] effectcraft/crates/psd/README.md @v0.11.1 — PSD reader scope, in-repo fixtures.
- [29] effectcraft/crates/project/src/lib.rs @v0.11.1 — `.ecproj` schema 2, `from_json_repaired`, saved view.
- [30] effectcraft/apps/effectcraft-cli/src/main.rs and crates/export/src/lib.rs (`batch_size`), pipeline.rs (`EFFECTCRAFT_GPU_INFLIGHT`) @v0.11.1 — CLI usage, render flags, CPU batch size.
- [31] effectcraft/packaging/{windows/effectcraft.wxs,windows/package.ps1,linux/nfpm.yaml} and apps/effectcraft/src/launch_guard.rs @v0.11.1 — CLI in MSI/zip/deb, `portable.txt`, launch guard.
- [32] effectcraft/crates/engine/src/{autosave.rs,config.rs,models.rs}, crates/script/src/socket.rs, apps/effectcraft/src/control_server.rs @v0.11.1 — atomic write, auto-save, models via `curl`, script network gate, loopback.

**SoundCraft**
- [33] soundcraft/README.md @v0.8.0 — pre-alpha status, features, CLI examples, Windows `WGPU_BACKEND`/FXC, logs.
- [34] soundcraft/docs/{file-format-parity.md,gaps.md,plugin-parity.md,mcp.md} @v0.8.0 — formats, gaps G-01..G-22, sidechain absence, CLAP/VST3 on Windows.
- [35] soundcraft/crates/model/src/session.rs @v0.8.0 — `Session`, `format_version` 1, `from_json`, `sanitize`.
- [36] soundcraft/crates/dsp/src/meter.rs and crates/dsp/tests/offline_meters.rs @v0.8.0 — BS.1770 meter and synthetic tests.
- [37] soundcraft/crates/engine/src/cmd/file.rs, apps/soundcraft-cli/src/main.rs @v0.8.0 — bounce parameters and CLI.
- [38] soundcraft/crates/engine/src/{autosave.rs,io.rs}, crates/playback/src/devices.rs, packaging/{windows/soundcraft.wxs,windows/package.ps1,linux/nfpm.yaml}, network-audit greps (Cargo.lock, TcpListener/TcpStream, URLs) @v0.8.0.

**Release and web facts**
- [39] `git ls-remote --tags` and `git fetch --depth 1 origin tag <t>` plus `git log -1 --format=%cI` for every tag of the three repos, run 2026-10-18.
- [40] `https://github.com/storytold/filmcraft/releases/download/v0.8.0/SHA256SUMS.txt` (also `.../v0.7.2/...`, `https://github.com/storytold/effectcraft/releases/download/v0.11.1/SHA256SUMS.txt`, `https://github.com/storytold/soundcraft/releases/download/v0.8.0/SHA256SUMS.txt`) — downloaded with curl 2026-10-18; asset lists and hashes.
- [41] `https://getartcraft.com/apps/filmcraft`, `https://getartcraft.com/apps/effectcraft`, `https://getartcraft.com/apps/soundcraft` — fetched 2026-10-18; website versions 0.6.0 / 0.8.0 / 0.5.0, launcher 0.3.2, "55 effects" / "259 effects".
- [42] `https://github.com/storytold/filmcraft/releases` — release notes v0.4.0-v0.8.0 (WebFetch, 2026-10-18; page truncated).
- [43] `https://github.com/storytold/effectcraft/releases` — release notes v0.8.0-v0.11.1 (WebFetch, 2026-10-18; page truncated).
- [44] `https://github.com/storytold/soundcraft/releases` — release notes v0.5.0-v0.8.0 (WebFetch, 2026-10-18).

**Issues (WebFetch, 2026-10-18; summarised by a small model)**
- [45] `https://github.com/storytold/filmcraft/issues/2216`, `/1939`, `/1443`, and the search `.../issues?q=is%3Aissue+is%3Aopen+%28data+loss+OR+corrupt+OR+lost+OR+autosave+OR+recover%29` and `.../issues?q=is%3Aissue+%28TIFF+OR+still+OR+photo+OR+JPEG+OR+%22image+sequence%22%29` — data-loss, export OOM, stills reports.
- [46] `https://github.com/storytold/filmcraft/issues/1959`, `/1998`, `/2099`, `/1390` and `.../issues?q=is%3Aissue+Windows+%28crash+OR+launch+OR+start%29` — corpus run, HEVC HLG import failure, sitrep, Windows launch failure, Windows issue list.
- [47] `https://github.com/storytold/effectcraft/issues/1615`, `.../issues?q=is%3Aissue+is%3Aopen+Windows`, `.../issues?q=is%3Aissue+is%3Aopen+%28%22data+loss%22+OR+corrupt+OR+lost+OR+autosave+OR+%22crash%22%29` — CPU render OOM, Windows list, crash and data-loss list.
- [48] `https://github.com/storytold/soundcraft/issues/711`, `/710`, `.../issues?q=is%3Aissue+is%3Aopen+Windows` — audio corpus report, MP3 import bug, Windows list.

**Fallback editors and third parties**
- [49] `https://kdenlive.org/news/` — Kdenlive 26.08.2 (2026-10-13), 26.08.1, 26.08.0, 26.04.x (fetched 2026-10-18).
- [50] `https://kdenlive.org/news/releases/26.08.0/` — 26.08.0 notes, no OTIO mention.
- [51] `https://docs.kdenlive.org/user_interface/menu/file_menu.html` — OTIO import/export scope and limits.
- [52] `https://discuss.kde.org/t/opentimelineio-metadata-and-effects/45813` — 2026-03-30 post: metadata and effects dropped on import.
- [53] `https://invent.kde.org/multimedia/kdenlive/-/work_items/1916` — OTIO adapter work item (Python version deprecated; C++ proof of concept).
- [54] `https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1051588.html` — KDE bug 503692 (2025-05-02): missing-asset abort, Kdenlive-to-Resolve track order flip.
- [55] `https://www.blackmagicdesign.com/products/davinciresolve` — Resolve 21; free edition 8-bit up to UHD 60 fps (fetched 2026-10-18).
- [56] `https://violetflare.ai/blog/davinci-resolve-otio-import/` — secondary source: native OTIO since 18.5, basic dissolves only, track and timeline names reset.
- [57] `https://tryuncle.com/learn/davinci-resolve/switching-from-final-cut-pro-to-davinci-resolve` — appeared in search results only (page not fetched): Resolve 21.0.2 guide recommending FCPXML 1.9.
- [58] `https://www.windowsmode.com/?p=47621` — 2026-10-12 article: portable zips, no minimum specs for the Craft apps, no hands-on testing.
- [59] `https://zeli.app/story/49958850` — 2026-10-04 thread: no first-hand FilmCraft/EffectCraft/SoundCraft reports; "very broken software produced by AI" comment about an unnamed app.
- [60] Search-result-only items, not fetched: `https://github.com/storytold/photocraft/issues/1975` ("Filmcraft and Effectscraft crash on startup", AMD driver DLL), `https://pasqualepillitteri.it/en/news/23653/effectcraft-free-after-effects-alternative-rust` (EffectCraft memory use on Windows 11 with Intel Arc), a Blackmagic forum thread on importing AAF/OTIO/FCPXML through the Python API (`https://forum.blackmagicdesign.com/viewtopic.php?p=1151748`, 403 on fetch).
- [61] First-hand: ffmpeg 6.1.1 (Ubuntu 24.04 package) on synthetic signals in the scratch folder, 2026-10-18 — `sidechaincompress` ducking (-27.5 dB to -38.2 dB), `loudnorm` two-pass, `ebur128` verification, `zoompan` to ProRes 422 HQ (125 frames) and ProRes to x264 CRF 16; ImageMagick 6.9.12 still conform.
- [62] First-hand container baseline, 2026-10-18: Ubuntu 24.04.5, glibc 2.39, 4 CPUs, 16 GB RAM, ffmpeg 6.1.1, ImageMagick 6.9.12, Node 22, Python 3, `libvulkan1`, `libegl1`, `libxkbcommon0`, `libasound2t64` installed, no GPU, no Playwright browsers.
- [63] `reviews/01-addendum-briefs-review.md` Part 0 and Part 2.2, and `CHARTER.md` — the brief, the Part 0 facts, the principles.
- [64] Search-result-only: `https://ubuntuhandbook.org/index.php/2025/04/kdenlive-25-04-0-released/` and a Neowin page on Kdenlive 25.04.0 — OTIO import/export rewritten in C++ in 25.04.0, effects/transitions not exported (not fetched).

---

## Follow-up research (round 1)

Written 2026-10-18 (Sunday, about 05:20-05:50 UTC) by a Sonnet researcher, answering the six follow-ups in `reviews/craft-motion-round1.md` Part 4 and the orchestrator's brief. Same rules as the main note: nothing was built or run (no Craft app, no Kdenlive, no Resolve); code was read from shallow clones in the scratchpad; the Resolve 21 manual was downloaded as data and searched as text; web pages were treated as data. Evidence grades as above: **[T]** test exists, **[C]** code path read, **[V]** vendor or official doc, **[I]** issue or third-party report, **[E]** estimate, **UNVERIFIED** not checked. New sources are numbered [65] onward at the end of this section.

### Answers at a glance

| # | Question | Short answer |
|---|---|---|
| F1 | How do Final Cut Pro and Resolve 21 write stills in FCPXML 1.9-1.11? | **Final Cut Pro: a bare `<video>` in the spine** (one FCPXML 1.13 sample from a third-party repo; no 1.9-1.11 sample found). **Resolve 21: UNVERIFIED** (no Resolve-written still found). FilmCraft **skips a bare `<video>`** and so cannot read Final Cut's stills. Do not plan any return path through FCPXML. |
| F2 | Does Resolve 21 (free) import FCP7 XML Basic Motion keyframes and Opacity? | **Yes, per the Resolve 21 Reference Manual**: Opacity, Position, Scale, Rotation imported from FCP7 XML, and "if these settings have been keyframed, the animation will appear". It needs the **"Use sizing information" checkbox** ticked in the import dialog. FilmCraft's exact XML in Resolve is still a maker test. |
| F3 | Does Kdenlive 26.08's OTIO importer create image clips with the right duration? | **Yes by code** (v26.08.2 and the 26.08 branch head are identical in `src/otio`): a still `ExternalReference` becomes an Image bin clip, is inserted and then resized to the clip's `source_range` duration. **New problems found:** a `file://` `target_url` is not decoded (media goes missing), `ImageSequenceReference` is skipped, and dissolves *do* import (as luma mixes). |
| F4 | Did PR #1763 (`EFFECTCRAFT_CPU_INFLIGHT`) land after v0.11.1? | **No.** PR open and unmerged, issue #1615 open, no maintainer comment. EffectCraft `main` is `Release 0.12.0`, a version bump only, with **no tag yet**. `RAYON_NUM_THREADS=2` is **not** a safe bound (6.8 GB reported). |
| F5 | What does FilmCraft's GUI New Sequence dialog default to? | **23.976 frames/second, 1920x1080, 48000 Hz, Stereo, 3 video + 3 audio tracks, named "Sequence NN"; there is no preset list in the dialog** (a headless UI test asserts the 23.976 timebase). Dropping a still on an empty timeline instead makes a sequence at the *still's pixel size* and **29.97 fps**. Windows-only differences: none in code; the maker's look at the dialog is still the confirmation. |
| F6 | Maker's installed versions and hardware | **Cannot be answered from here.** A read-only PowerShell block and the version commands are in F6; still outstanding. |
| F7 | New since the main note | **FilmCraft v0.9.0 was tagged and released on 2026-10-18**; the main note's pin tables stop at v0.8.0. |

### F1. How Final Cut Pro and Resolve 21 write stills in FCPXML 1.9-1.11

**What the standard says [V].** Apple's FCPXML DTD page (documented version 1.10; 1.5-1.9 DTDs are linked from the Final Cut Pro support page) [75]:
- `asset-clip` is "a clip that references an asset. All available media components in the asset are implicitly included", `ref` is an asset id, `duration` defaults to the asset's.
- `video` is "a range of video data in a source asset", `ref` is an `asset` or `effect` id. `video` is allowed directly in a `spine`, as a `clip_item`, and as the child of a `clip`.
- `asset` has optional `duration` and `hasVideo`; the DTD never says which element a *still* must use. The Library smart collection "Stills" uses `<match-media type="stills">`, so Final Cut does treat stills as a media type of their own.
- Apple's worked examples (versions 1.10) use `asset-clip` for movie files only [75].

**What Final Cut Pro actually writes for a still [I, one file].** The `cutlass` repository (a Go library for writing FCPXML, commit `4dbe20d`, 2025-07-06) carries `samples/png.fcpxml` [76]. It looks like an unedited Final Cut Pro export (FCPXML **1.13**, a `library location="file:///Users/aa/Movies/Untitled.fcpbundle/"`, an event and project, Apple's `sig` and `bookmark` blobs, an `ingestDate`, and Apple's default smart collections including "Stills"). For one PNG placed in a project it has:
- `<asset id="r2" ... start="0s" duration="0s" hasVideo="1" format="r3" videoSources="1">` with a `media-rep kind="original-media"`; the still's asset is **timeless** (`duration="0s"`), and its `<format id="r3" name="FFVideoFormatRateUndefined" width="1280" height="800"/>` has **no `frameDuration`**;
- in the spine: **`<video ref="r2" offset="0s" name="cs.pitt.edu" start="86399313/24000s" duration="241241/24000s"/>`**, a bare `video` element, not an `asset-clip` and not wrapped in a `clip`. (`start` is just under 3600 s, Final Cut's origin for timeless media.)
The repository's own rules say the same: "Images (PNG/JPG): Use `Video` elements with `duration="0s"` assets, no `frameDuration` in format; videos use `AssetClip`" [76]. That is the author's rule, not Apple's, and the page does not say it was copied from exports; I rate it as supporting the sample, not as proof.

**Corroboration from the other direction [I].** `davinci-slide-builder` (2020, FCPXML **1.8**) builds a slideshow of JPEG stills as a spine of bare `<video ref=... duration=... offset=.../>` elements with `<transition>` between them and says to import it into DaVinci Resolve (free) through "import timeline" [78]; so Resolve of that era read bare `<video>` stills. That is a statement by the tool's author, not a test I ran, and it is about reading, not about what Resolve writes.

**What I did not find.**
1. **No FCPXML 1.9, 1.10 or 1.11 sample with a still.** The DTD does not tie `video` to a version, and the 1.8 and 1.13 evidence points the same way, so a bare `<video>` is the likely form in 1.9-1.11 too, but this is [E].
2. **No `<clip>`-wrapped still.** The FCP-written 1.8 samples in OpenTimelineIO's `otio-fcpx-xml-adapter` (`tests/sample_data/fcpx_example.fcpxml` etc., commit `c61839e`) show `<clip><video ref=.../><clip lane="-1"><gap><audio/></gap></clip></clip>` for **movie** clips whose audio is split out, never for stills [77]. So "`<clip>`-wrapped `<video>`" is real Final Cut output for movies; for stills it is UNVERIFIED.
3. **No Resolve-written still.** The Resolve 21 manual says "Export of still images is limited to Final Cut Pro 7 and Final Cut Pro X XML formats" (p. 486) but names no element [74]. A third-party library README says its FCPXML reader covers "`asset-clip`-style spines -- what DaVinci Resolve exports" [79], and its Resolve fixture (version 1.8, video clips only) is `asset-clip` throughout [79]; neither says what Resolve 21 writes for a PNG. Blackmagic forum pages return 403 (as in the main note), so no forum evidence. **Resolve 21 stills in FCPXML: UNVERIFIED.**
4. **Which FCPXML versions Resolve 21 reads:** the manual does not say (searched for "FCPXML" and "1.9"/"1.10"; one mention, of exporting an FCPXML from the Edit page for a Final Cut Pro X round trip, p. 4191). Two July 2026 blog guides contradict each other (one: Resolve has supported 1.10 import for years; the other: export 1.9, because 1.10+ writes `.fcpxmld` bundles) [81]. Both are secondary. UNVERIFIED.

**What FilmCraft reads [C, unchanged in v0.9.0].** `fcpxml.rs` accepts versions above 1.11 with an info message ("newer than 1.11; unknown elements were ignored") and then handles `asset-clip` (asset by `ref`), `clip` (it takes the first inner `video`, `audio` or `asset-clip` that has a `ref`), `ref-clip`, and `gap`. A bare `title`, `video`, `audio`, `sync-clip`, `mc-clip` or `live-drawing` in a storyline logs "FCPXML <tag> elements are not supported and were skipped" and the clip is dropped [69]. So:
- Final Cut's own stills (bare `<video>`) **would be skipped** by FilmCraft;
- a `<clip>`-wrapped `<video>` still would be read (through the asset) but only if some tool writes it that way (none found);
- FilmCraft's FCPXML *exporter* writes stills as `asset-clip` over an asset with `duration` 5 s [69]. A third-party tool README reports that PNG/JPEG assets referenced directly crash Final Cut Pro on import (`addAssetClip` null pointer; FCP version not stated) [80]. Not tested, and the maker has no Mac, so low priority; whether Resolve 21 accepts such a still is UNVERIFIED.

**Decision.** FilmCraft cannot be assumed to read a fallback editor's FCPXML for stills, and FilmCraft's FCPXML for stills is untested in both Final Cut and Resolve. **Do not build any return path on FCPXML.** Use FCP7 XML (xmeml) both ways with Resolve (the manual lists "Still Image Clips" as supported for FCP 7 XML, F2) and OTIO both ways with Kdenlive. Keep FCPXML export as a third, untested option.

**Maker's 3-minute check (optional, also settles Resolve's output form).** In Resolve put two stills on a timeline, File > Export > Timeline > FCPXML, open the file in Notepad, and search for the still's file name. Report which element names appear around it (`video`, `asset-clip`, `clip`) and whether the `asset` has `duration="0s"`. The file holds only local paths, so it is safe to paste into the repo's private notes.

### F2. Does Resolve 21 (free) import FCP7 XML Basic Motion keyframes and Opacity?

**Source found.** The DaVinci Resolve 21 Reference Manual PDF is fetchable at `documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf` (4,444 pages, PDF created 2026-07-09 per its metadata, 187,277,990 bytes, SHA-256 `7bfdcf0296bd1e48aeca58a3d66026821cf9dec5f1f0e5fe7a4b936dbe34e799`) [74]. The main note's "manual unreachable" was true of the older mirror it tried; Resolve 18, 19 and 20 manuals are at the same pattern (HTTP 200 on a HEAD request). Quoted below as [V]; page numbers are PDF pages.

**What it says (Chapter 22, "Importing and Conforming Timelines") [74].**
- p. 482, table "Effects supported with imported AAF, XML, and EDL": for **FCP 7 XML**: Composite Modes Yes; Multiple Tracks Yes; Video Transitions Yes; Audio Transitions No; **Opacity Settings Yes; Position, Scale, Rotation Yes**; Flip and Flop No; Linear and Variable Speed Yes; **Still Image Clips "All supported formats in Resolve"**; Freeze Frames No; Nested Sequences Yes; Text Generators Yes. (EDL is "No" for opacity, motion and stills.)
- p. 484, "About Supported Opacity, Position, Scale, and Rotation Settings": "When importing XML project files from Final Cut Pro X, Premiere Pro, or legacy Final Cut Pro 7, DaVinci Resolve supports the import of Opacity, Position, Scale, and Rotation settings. Imported Composite and Transform settings for any given clip appear in the Inspector of the Edit page, or in the Edit Sizing mode of the Sizing palette in the Color page. **If these settings have been keyframed, the animation will appear in DaVinci Resolve.**"
- p. 486, "About Supported Still Image Formats": Resolve imports "greater-than-one-frame-in-duration TIF, JPG, PNG, DPX, TGA, and DNG still image files that appear in Final Cut Pro X, Final Cut Pro 7, and Premiere Pro XML files ... These clips appear as ordinary clips in the DaVinci Resolve Timeline."
- pp. 521-523, "Importing XML Project Files": File > Import Timeline (Shift-Command-I; on Windows presumably Shift-Ctrl-I, UNVERIFIED) or Media Pool right-click > Timelines > Import > AAF/EDL/XML/DRT/ADL/OTIO. The dialog has **"Use sizing information: Lets you import position, scale, and rotation transforms from the originating NLE via the imported XML project file"**, "Automatically set project settings" (frame size and rate from the file), "Automatically import source clips into media pool", and "Mixed frame rate format" (leave on "DaVinci Resolve" for files not from Final Cut, p. 481). p. 304 confirms the checkbox is what puts the transforms into the Inspector's Edit Sizing parameters ("If ... you turned on the 'Use sizing information' checkbox ..."). The manual does not state the checkbox's default; **tick it**.
- Nothing in pp. 476-546 is tagged Studio-only. The manual marks Studio-only items elsewhere (for example "IMF (Studio Version Only)"), so I found no free-version restriction on XML, OTIO or EDL import; the manual contains no free-versus-Studio table, so this is absence of a restriction, not a statement that none exists.

**What it does not say.** It never mentions FilmCraft, never uses the label "Basic Motion", and gives no interpretation of units (centre as a fraction of frame size, scale in percent, `when` in source frames). FilmCraft writes exactly the Premiere/FCP7 dialect: filter `Basic Motion` (`effectid` `basic`) with `scale`, `rotation`, `center`, `centerOffset`, and filter `Opacity` (`effectid` `opacity`), all with keyframes, `center` as a fraction of the frame size from the frame centre [69]. That is the structure the manual's "Final Cut Pro 7 / Premiere Pro XML" sentence covers, so the format-level answer is **yes**; whether Resolve 21 gets *FilmCraft's* numbers right (position origin, scale base, keyframe timing) is **UNVERIFIED** and remains the maker's test.

**Why the risk is small for stills [E].** FilmCraft writes keyframe `when` as source (media) frames "like `in`/`out`" [69]. For a still that is never trimmed at the head `in` is 0, so source-relative and clip-relative frames coincide and the ambiguity disappears. Another trap (new, [C]): a still's `<file>` carries `<rate>` = the still's reported rate, which is Settings > Media > Indeterminate Media Timebase, **default `29.97df`**, with a 5 s default duration in frames at that rate [68][69]. In a 25 fps sequence that gives Resolve a 29.97 fps source for every still. Stills should be unaffected by the mixed-rate conform, but this is UNVERIFIED. Cheap guard: before the agent's `.fcproj` or any import, set Indeterminate Media Timebase to the project rate (`prefs.set media.indeterminateTimebase "25"`; the engine has tests for this key) and re-check in Resolve.

**Revised Resolve test (replaces the Resolve line in R7).** (1) Import `ch01.xml` (FCP7 XML) with File > Import Timeline; tick **Use sizing information**; leave Mixed frame rate on "DaVinci Resolve". (2) Check: stills online, 5 s durations (not 1 frame, not 29.97-based), Inspector > Edit Sizing shows Zoom/Position keyframes at the right frames, Opacity keyframes in Composite, dissolves present. (3) Repeat with `ch01.otio` and write down what is lost (OTIO has no motion; expected from the main note). (4) Record the Resolve version (Help > About) and mark the matrix cells.

### F3. Kdenlive 26.08's OTIO importer and still-image clips

**Code state.** Read at tag `v26.08.2` (commit `ef54398259f2`, 2026-10-06) and at the `release/26.08` branch head (`9f19b4ca9f68`, 2026-10-18). The trees of `src/otio`, `src/bin/clipcreator.cpp` and `src/mltcontroller/clipcontroller.cpp` are **byte-identical** between the two (checked by comparing git object ids) [72].

**Chain for a still [C, with a Kdenlive test for part of it].**
1. `OtioImport::importFile` collects every `ExternalReference` `target_url` through `resolveFile` and creates **one bin clip per distinct file** with `ClipCreator::createClipFromFile` (`otioimport.cpp` lines 84-92 and 205-216).
2. `ClipCreator::getXmlFromUrl` (`clipcreator.cpp` lines 274-328): any file whose MIME type starts with `image/` (except GIF) becomes `ClipType::Image` with a producer duration from `KdenliveSettings::image_duration()`, default **`00:00:05:00`** (`kdenlivesettings.kcfg`, entry `image_duration`).
3. `ClipController::hasLimitedDuration()` returns **false** for `Image` (also Color, Text), and `ClipModel` sets `m_endlessResize = !binClip->hasLimitedDuration()` (`clipmodel.cpp` lines 45-51). So a timeline instance of an image clip can be made **any length**.
4. `OtioImport::importClip` (lines 304-370; insertion at 341, resize at 347): `duration = trimmed_range_in_parent().duration()` rescaled to the timeline rate (clip skipped if there is no value or it is <= 0); `requestClipInsertion(binId, trackId, position, ...)` at the clip's position; then **`requestItemResize(clipId, duration, true, ...)`** sets the length; a slip is applied only if the `source_range` start differs from the media's timecode (stills: 0, FilmCraft writes `origin + source_in` = 0 for a never-trimmed still [69]).
5. The result for a still: an Image clip of exactly the OTIO duration at the OTIO position. Gaps are kept by position.

**Test evidence [T, partial].** `tests/dataset/test-transitions.otio` uses `red.png`, `yellow.png`, `blue.png` as `ExternalReference`s with 24-frame `source_range`s and two `SMPTE_Dissolve` transitions, and `tests/otiotest.cpp` "Transitions" imports it, re-exports and asserts the transitions' names, types and offsets equal [72]. The "Multiple tracks and clips" test asserts equal item durations, but on `.mpg` movie files. **No test asserts a still's duration.** Not run.

**Other facts from the same code (each [C], none run).**
- **`file://` target URLs are not decoded. New, and it contradicts the main note's R3 advice.** `resolveFile` does `QUrl::fromLocalFile(file)` then `toLocalFile()`, and treats anything still relative as relative to the OTIO's folder. Qt's documentation says `fromLocalFile` "expects path, not url with scheme" [73]. A `target_url` such as `file:///C:/LifeJourney/work/stills/IMG_0001.png` therefore stays a string starting with `file:` and is joined onto the OTIO folder: the media is not found. Kdenlive's own exporter writes a plain path (`projectClip->url()`) [72]. FilmCraft reads relative paths, plain paths and `file://` URLs [69]; Resolve reads URLs (its own OTIOs use them; UNVERIFIED for plain paths).
- FilmCraft's own export already avoids the problem: `file.exportInterchange` sets `relative_to` to the output file's folder, so media on the same drive is written as a **relative path** (for example `../media/ch01_s01.png`); only when no leading path component is shared does it fall back to a `file://` URL [69]. The agent-written OTIO (R3 example, skill step 8, playbook Step 7) uses absolute `file:///C:/...` URLs and **would not open in Kdenlive**. Fix: write relative paths in agent-emitted OTIO (they are read by FilmCraft, by Kdenlive, and by Resolve through the media-relink prompt, which is UNVERIFIED for Resolve).
- **`ImageSequenceReference` is skipped silently**: the importer has the branch commented out with `// TODO: Image sequence references.`, so such clips get no bin id and are dropped (`importClip` returns -1) [72]. Stills must be single-file `ExternalReference`s.
- **Dissolves do import.** In `importTrack` (line 295), a `Transition` directly before a clip, with both neighbouring clips imported, becomes `requestClipMix("luma", ...)` with the in and out offsets. The main note's Q3 Kdenlive cell ("no effects or transitions mentioned") and Summary 13 should say: **cuts, markers (as guides or clip markers), gaps, and dissolves (as luma mixes) survive; effects and metadata do not** [C]. Dissolve length fidelity is untested.
- **Project profile comes from the first video-track clip whose file yields a size**: frame rate from the OTIO timeline duration's rate, frame size from the first still's pixel size (read with libavformat), else 1920x1080; Kdenlive picks a matching progressive profile or makes a custom one. So the **first still must already be the sequence's size** (R1 conforms stills to 16:9; keep them at the sequence size, or at least make the first one so), otherwise the project opens at the first still's pixel size [72].
- Missing media: `test-missing-media.otio` is tested to import **fewer clips than the file has** [72] (and the open bug 503692 aborts [54]); keep paths valid.
- Metadata other than Kdenlive's marker `kdenlive.type` is ignored, so FilmCraft's `metadata.filmcraft` Ken Burns is lost, as already stated.

**Maker test K1 (only if Kdenlive is ever needed; 5 minutes).** Import the 3-still `ch01.otio` that FilmCraft exported from the project folder (relative paths). Pass if three image clips appear at the right times with the right lengths and the profile is 1920x1080 at the sequence rate.

### F4. PR #1763 and the EffectCraft pin

**Answer: no, it has not landed.** As of 2026-10-18 about 05:20-05:30 UTC [70][71]:
- `git ls-remote --tags` still lists twelve tags, **newest `v0.11.1`**; the releases page shows v0.11.1 as Latest.
- `main` is `f36b2b3e` "Release 0.12.0" (2026-10-17 21:43 -04:00), whose diff against v0.11.1 is only `Cargo.toml` (version) and `Cargo.lock`; **no tag or release for 0.12.0 exists yet**, so a `v0.12.0` tag will probably appear soon and would be code-identical to v0.11.1. `grep CPU_INFLIGHT` on `main` finds nothing.
- PR #1763 (by an outside contributor, 2 commits, last on 2026-10-17 22:14 -04:00, based on that 0.12.0 commit) is **open, no reviews, not deployed** [71]. It adds `EFFECTCRAFT_CPU_INFLIGHT=N` (a positive whole number caps CPU frames in flight; unset or invalid means no cap, "today's behaviour"), with unit tests of the parser and a run test that at most 2 of 16 frames run at once [70]. It does **not** add an automatic cap from free memory, and does not fix the unplayable partial MP4 after a kill (both listed as follow-ups).
- Issue #1615 is open, labelled `priority: critical`, no maintainer comment visible; a ticket bot asked on 2026-10-16 for it to be split into the memory cap and the missing error/partial file [71].

**What changes for the pin and the skill.**
1. **Pin candidate for EffectCraft stays `v0.11.1`** (x64 portable SHA-256 as in Q1). Treat `v0.12.0`, if tagged, as the same code; re-run the hash check if used.
2. **`RAYON_NUM_THREADS=2` is not a bound** (skill step 10; playbook pitfall 10; R4). Issue #1615 numbers: 1 thread 2.1 GB (36 s) and 4 threads 4.2 GB (17 s) for a 30-frame test; 16 threads over 9 GB and killed; and "in a heavier project, `RAYON_NUM_THREADS=2` still reached 6.8 GB"; lowering the `memory.*` budgets with `prefs.set` "did not help" [71]. Replace the mitigation by: **start every new comp at `RAYON_NUM_THREADS=1`, measure peak memory on a 30-frame sample (`/usr/bin/time -v` in the container; Task Manager on Windows), then raise**; or render frame by frame (`render-frame` per frame, PNG sequence) and encode with ffmpeg, which is what the reporter did [71]. Keep comps light (few layers, no 3D) until a cap exists.
3. **`EFFECTCRAFT_CPU_INFLIGHT` does not exist in any tag**; setting it today does nothing. If it lands, document it as the preferred mitigation (`EFFECTCRAFT_CPU_INFLIGHT=1` or 2) and re-measure.
4. **Check weekly** (30 seconds): `git ls-remote --tags https://github.com/storytold/effectcraft | sort -V | tail -3` and the PR page.

### F5. FilmCraft's New Sequence dialog defaults

**Answer [T + C, Linux headless; no platform branch in the code].** At v0.8.0 (and unchanged at v0.9.0; neither `sequence_settings.rs`, `SequenceSettings::default` nor the UI test changed) [68]:
- **File > New > Sequence...** (menu spec `Cmd+N`; Ctrl+N on Windows is assumed, UNVERIFIED) opens the *Sequence Settings* dialog in "New Sequence" mode (v0.5.0 change). It starts from `SequenceSettings::default()`: **Timebase "23.976 frames/second"** (video display "23.976 fps Timecode"), **Frame Size 1920 x 1080** (aspect "16:9", square pixels), **Sample Rate 48000 Hz**, **Channel Format Stereo**, working colour space Rec. 709, name **"Sequence NN"** (NN = number of sequences + 1), and a **Tracks tab with 3 video and 3 audio tracks**.
- **There is no preset or "Editing Mode" list**: Editing Mode is shown greyed as "Custom" ("not supported in FilmCraft yet"). The fields are a Timebase drop-down (15 rates: 10, 12, 12.5, 15, 23.976, 24, 25, 29.97, 30, 48, 50, 59.94, 60, 119.88, 120), numeric Width and Height, a Sample Rate drop-down (32, 44.1, 48, 88.2, 96 kHz) and a Channel Format drop-down. The "HD 1080p 23.976" string in `SequenceSettings::default().preset` is internal and is rewritten to "1920x1080 23.976" by `file.newSequence`. The UI test `new_sequence_opens_its_dialog` asserts the 23.976 timebase, the name and the 3/3 tracks. This **corrects review nudge 6**, which told the maker to "pick the 1920x1080 25 fps preset": there is none; the maker opens the Timebase list and chooses **25 frames/second**, and picking a new timebase also sets the matching timecode display automatically.
- The engine default (`file.newSequence`, no parameters) is the same: 1920x1080 at 23.976.
- Pressing OK makes the sequence in one undo step; Cancel makes none.

**Two other ways to create a sequence that do not use these defaults [C].**
1. **Dragging a clip (or dropping files) onto an empty timeline** runs `file.newSequence {fromItem}`, which calls `default_seq_settings_for(clip)`: width, height, frame rate and pixel aspect come from the clip. For a **still** that means **its pixel size** (3600 x 2400 for an unconformed scan) and a frame rate that is the *Indeterminate Media Timebase*, **default "29.97df"** (`autosave.rs` preferences default; `import_source` overwrites a still's rate with it) [68]. So a first still dropped on the empty timeline gives a 29.97 fps sequence at the photo's size.
2. The **Project panel's "+" menu > Sequence...** opens the same dialog as File > New.

**Add to Template B (five-minute test), as three lines.**
- "Create the sequence first: File > New > Sequence. Write down what the dialog shows for Timebase, Frame Size and Sample Rate (expected: 23.976, 1920 x 1080, 48000 Hz). Set Timebase to 25 frames/second, leave 1920 x 1080 and 48000 Hz, name it `ch01`, OK."
- "Never drop the first clip on an empty timeline: that creates a sequence from the clip (a still gives its pixel size and 29.97 fps)."
- "Settings > Media > Indeterminate Media Timebase: set it to 25 fps before importing stills, then check Sequence > Sequence Settings still says 25."
If the dialog on Windows shows anything other than the expected defaults, the maker pastes the three values into the hand-off note; that closes the gap between the code and the Windows build.

### F6. The maker's installed versions and hardware (still outstanding)

**Status: cannot be answered by research.** Nothing in the repo or the conversation holds these; the user's reply on 2026-10-18 did not include them. Half of Q4 (export speed table) and playbook Decision 1 stay keyed on them. Ask the maker to run this once (read-only, prints no names, accounts or serial numbers; **not run by me, Windows PowerShell commands written from memory, UNVERIFIED**):

```powershell
# Life Journey inventory: paste the output into the private repo notes
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
"RAM GB: " + [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, BuildNumber
Get-PSDrive -PSProvider FileSystem | Where-Object { $null -ne $_.Used } | Select-Object Name, @{n='FreeGB';e={[math]::Round($_.Free/1GB)}}
```
- **GPU memory (VRAM):** read it in Task Manager > Performance > GPU > "Dedicated GPU memory". Do not use the WMI `AdapterRAM` value for it: from memory it is capped at 4 GB (UNVERIFIED here).
- **Installed Craft versions:** in each app's folder run `.\filmcraft-cli.exe --version`, `.\effectcraft-cli.exe --version`, `.\soundcraft-cli.exe --version` (all three CLIs implement `--version` [68]); in FilmCraft also Help > About FilmCraft (`app.about`). Also record whether each was installed from the **MSI or the portable zip**, and for a zip run `Get-FileHash -Algorithm SHA256 <zip>`; the hash identifies the tag unambiguously against the tables in Q1 and F7.
- **What each answer decides:** CPU cores and RAM pick the chapter size and the export table in Q4; GPU vendor decides the `WGPU_BACKEND` order to try first (NVIDIA: Vulkan or DX12; AMD: watch for the `atio6axx.dll` and `amdvlk64.dll` crashes; Intel Arc/Gen 9: see the issue list in Q1) and whether NVENC export exists; free disk decides whether ProRes 422 HQ masters (large) can live on the work drive; the Craft versions decide which of the checksums below applies.

### F7. Changes since the main note (found while answering the above)

**FilmCraft v0.9.0 exists.** Tag `v0.9.0`, commit `4a69a038d327` "Release 0.9.0" (2026-10-17 21:43 -04:00), shown as released 18 Oct; `main` of FilmCraft is the same commit [65][67]. The main note's pin tables stop at v0.8.0. `SHA256SUMS.txt` downloaded today [66]:

| Asset | SHA-256 |
|---|---|
| `filmcraft-0.9.0-windows-x64-portable.zip` | `d370cac8ed2edd729c8129aa55f75d0123716ba3cddbf9c5e4e3f0fdaa101a5e` |
| `filmcraft-0.9.0-windows-x64.msi` | `5db43e23998939bb1edbf20b1413df6bea23ca108b40af7ad7059bdca800540f` |
| `filmcraft-0.9.0-linux-x86_64.tar.gz` | `ea67953cc754bfd8272e0e5fa940518e16068ae96f6b72a2dce566ed69a61632` |

What changed from v0.8.0 (37 files, `git diff --stat`; read from the diff, not run) [65]:
- **Interchange importers and exporters unchanged** (`fcpxml.rs`, `fcp7.rs`, `otio.rs` are not in the diff): only a UTF-8-safe `file:` URL prefix check in `common.rs` plus a test. All F1-F3 statements about FilmCraft hold for v0.9.0.
- **Stored media paths are now restricted.** Paths read from a project, a template or an interchange file are opened only if they name a file on this computer or on the document's own network share; a UNC path or a `file://` URL to another host is refused and the item shows the offline slate, to be fixed with Link Media. Relative paths are taken from the document's folder. Folders named in a project file for auto-save, previews or proxies are used only if inside the project's folder or chosen in Scratch Disks on this computer. For us: keep everything on a local drive under the one project root (already advised); do not put the project on a NAS path [65].
- GPU-export deadlock fix (nested renderer pool; only matters with `--gpu-rendering`, which is off by default); Alt-selection delete/ripple-delete fix; image-sequence file names keep Unicode prefixes [65][67].
- No change to `sequence_settings.rs`, `SequenceSettings::default`, still decoding, or the Indeterminate Media Timebase default (checked), so F5 holds.

**Recommendation (judgement [E]).** Run the maker's five-minute test on **v0.9.0 first** (newer, small diff, fixes a UTF-8 panic that can hit Unicode file names such as a mother's name in a path), keep **v0.8.0 as the fallback**, and record whichever passes. Do not run both against the same project folder. SoundCraft is unchanged (newest tag v0.8.0 at 05:31 UTC). EffectCraft: see F4.

### Edits these answers imply (for the scribes; not applied here)

1. **Research Q3.** Kdenlive OTIO cell and Summary 13: dissolves import as luma mixes [C]; add the `file://` limitation, the `ImageSequenceReference` skip, and "profile size from the first still". Resolve FCP7 XML cells: Position/Scale/Rotation/Opacity with keyframes "supported" per the manual (needs "Use sizing information"); FCPXML "Still image clip" cell: Final Cut writes a bare `<video>` [I], FilmCraft skips it. Open questions 3 and 4: mostly closed (Resolve and Kdenlive claims now have sources); what remains is the maker's test.
2. **R3, skill step 8, playbook Step 7 and Template C.** Agent-emitted OTIO uses **relative** `target_url` paths (FilmCraft-exported OTIO already does); FCP7 XML keeps absolute `file://localhost/C:/...` `pathurl`s (Resolve relinks by prompt).
3. **R7 and playbook Exercise 6.** Replace the Resolve line by the revised test in F2 (tick "Use sizing information"; mixed frame rate "DaVinci Resolve"; stills 5 s; keyframes).
4. **Playbook Pitfall 8 and review nudge 5.** Use F1: FilmCraft skips a bare storyline `<video>`; Final Cut writes stills that way (one FCPXML 1.13 sample); Resolve 21's form is unverified; do not use FCPXML as a return path.
5. **Playbook Exercise 2, Template B, review nudge 6.** Replace "pick the 1920x1080 25 fps preset" by the F5 lines (no preset exists; choose Timebase 25; never drop the first still on an empty timeline; set Indeterminate Media Timebase to 25).
6. **Skill step 10 and playbook pitfall 10.** Replace `RAYON_NUM_THREADS=2` by the F4 procedure (start at 1, measure, or render frame by frame); note `EFFECTCRAFT_CPU_INFLIGHT` is not yet in any tag.
7. **Pin tables (Q1, Template A).** Add the FilmCraft v0.9.0 row above; test v0.9.0 first, v0.8.0 fallback; EffectCraft stays v0.11.1 (v0.12.0 if tagged is the same code).
8. **Outstanding for the maker:** F6 inventory and the three Windows checks (New Sequence dialog values, Resolve import test, optional FCPXML element check); K1 only if Kdenlive is used.

### Sources (follow-up, continuing the numbering)

- [65] `git ls-remote --tags https://github.com/storytold/filmcraft`, `git fetch --depth 1 ... tag v0.9.0` (commit `4a69a038d32761f604b3c7e4845b21fb40b3cbe4`, 2026-10-17T21:43:10-04:00, `Cargo.toml` version 0.9.0) and `git diff --stat f03e2155..v0.9.0` plus diffs of `crates/interchange`, `crates/engine/src/{commands,interchange,autosave,doc_path}.rs`, `crates/export/src/{job,pipeline}.rs`, `docs/project-files.md`; run 2026-10-18 about 05:25 UTC.
- [66] `https://github.com/storytold/filmcraft/releases/download/v0.9.0/SHA256SUMS.txt` (curl, HTTP 200, 2026-10-18). `.../effectcraft/releases/download/v0.12.0/SHA256SUMS.txt` returned 404 (no such release).
- [67] `https://github.com/storytold/filmcraft/releases` (WebFetch 2026-10-18; page truncated at 100,000 characters; v0.9.0 notes paraphrased by the tool).
- [68] FilmCraft source at v0.8.0 (shallow clone `f03e2155`) and v0.9.0: `crates/ui-egui/src/panels/sequence_settings.rs` (`open_new`, `TIMEBASES`), `crates/ui-egui/tests/sequence_ui.rs` (`new_sequence_opens_its_dialog`, `sequence_settings_dialog_shows_the_sequence`), `crates/ui-egui/src/panels/timeline.rs` (drop on empty timeline), `crates/project/src/lib.rs` (`impl Default for SequenceSettings`), `crates/engine/src/commands.rs` (`file.newSequence`, `default_seq_settings_for`, `import_source`), `crates/media/src/still.rs` (`DEFAULT_STILL_DURATION`, `FPS_29_97`), `crates/engine/src/autosave.rs` (`indeterminate_timebase: "29.97df"`), `crates/engine/src/settings.rs` (`TIMEBASE`, `timebase_rate`), `apps/filmcraft-cli/src/main.rs`, `apps/effectcraft-cli/src/main.rs`, `apps/soundcraft-cli/src/main.rs` (`--version`).
- [69] FilmCraft interchange source at v0.8.0: `crates/interchange/src/fcpxml.rs` (lines 150-153, 383-406, 987), `fcp7.rs` (lines 1119-1200), `otio.rs` (`media_ref`, `source_range`, `abs_url`), `common.rs` (`relative_path`, `path_to_file_url`), `crates/engine/src/interchange.rs` (`export`, `relative_to`).
- [70] EffectCraft: `git ls-remote` (tags and HEAD) at 2026-10-18 05:20-05:30 UTC; `git fetch --depth 1` of HEAD (`f36b2b3e6bd1`, "Release 0.12.0") and of `refs/pull/1763/head` (`cd5a45d853290b7a1646c2ee930c30c348650a18`); `git diff 2a01226..f36b2b3` (Cargo files only); `git diff 2a01226..cd5a45d -- crates/export/src/pipeline.rs`; `git grep CPU_INFLIGHT` on `main`.
- [71] `https://github.com/storytold/effectcraft/pull/1763`, `https://github.com/storytold/effectcraft/issues/1615`, `https://github.com/storytold/effectcraft/releases` (WebFetch 2026-10-18; summarised by a small model; the releases page was read to character 100,000 of 152,880).
- [72] Kdenlive source (`git fetch --depth 1 --filter=blob:none https://invent.kde.org/multimedia/kdenlive.git`): tag `v26.08.2` (`ef54398259f2af1d29095a798cab48ca4c52f141`, 2026-10-06) and `release/26.08` (`9f19b4ca9f6894aac0df8959c77aec1b240eec38`, 2026-10-18): `src/otio/otioimport.cpp`, `otioutil.cpp`, `otioexport.cpp`, `src/bin/clipcreator.cpp`, `src/mltcontroller/clipcontroller.cpp`, `src/timeline2/model/clipmodel.cpp`, `src/kdenlivesettings.kcfg`, `tests/otiotest.cpp`, `tests/dataset/test-transitions.otio`.
- [73] `https://doc.qt.io/qt-6/qurl.html` (WebFetch 2026-10-18; `fromLocalFile` "expects path, not url with scheme"; summarised by a small model, the exact wording should be re-read).
- [74] DaVinci Resolve 21 Reference Manual, `https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf` (curl 2026-10-18, 187,277,990 bytes, SHA-256 `7bfdcf0296bd1e48aeca58a3d66026821cf9dec5f1f0e5fe7a4b936dbe34e799`, 4,444 pages), searched with `pdftotext -layout`; pages 304, 476-486, 521-524, 544-546. The Resolve 18, 19 and 20 manuals answer HTTP 200 at the same URL pattern (HEAD only).
- [75] `https://developer.apple.com/documentation/professional-video-applications/document-type-definition.md` and `.../describing-final-cut-pro-items-in-fcpxml.md` (WebFetch 2026-10-18; the DTD page documents version 1.10 and says copyright 2026).
- [76] `https://github.com/andrewarrow/cutlass` at commit `4dbe20d` (2025-07-06; shallow clone and WebFetch): `samples/png.fcpxml`, `README.md`, `go/wiki/Images-vs-Videos-Architecture.md`. Third-party; provenance of the sample inferred, not stated.
- [77] `https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter` at `c61839e` (2024-06-25): `tests/sample_data/fcpx_example.fcpxml`, `fcpx_event.fcpxml` etc. (FCPXML 1.8, movie clips only).
- [78] `https://github.com/moos/davinci-slide-builder` at `44bf4be` (2020-03-29), `README.md`.
- [79] `https://github.com/ChatOctopus/timeline` at `352d8f8` (2026-06-24): `README.md` and `tests/fixtures/resolve-export.fcpxml` (version 1.8, `asset-clip` video clips; provenance not stated).
- [80] `https://github.com/DareDev256/fcp-mcp-server` README, "Known Issues" (WebFetch 2026-10-18).
- [81] `https://vod.ing/blog/fcpxml-for-davinci-resolve` and `https://tryuncle.com/learn/davinci-resolve/switching-from-final-cut-pro-to-davinci-resolve` (WebFetch 2026-10-18; secondary blog guides, the second dated 2026-07-25; they disagree on FCPXML versions).
- [82] Search-result-only, not fetched: `https://larryjordan.com/articles/round-tripping-projects-between-final-cut-pro-and-davinci-resolve/` (a Resolve 17.4.2 era article quoting the user guide on Opacity/Position/Scale/Rotation and "XML v1.3-1.9"); `https://github.com/elliotttate/SpliceKit/blob/main/docs/FCPXML_FORMAT_REFERENCE.md` was fetched and says nothing about stills; `https://github.com/jelloshooter848/ReCut/pull/83` was fetched and says Resolve import was not tested there. The Blackmagic forum thread `https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=209153` returned 403.

---

## Follow-up research (round 2)

Written 2026-10-18 (Sunday, about 06:10-06:40 UTC) by a Sonnet researcher, answering the six research follow-ups in `reviews/craft-motion-round2.md` Part 5. Same rules as before: no Craft app, Kdenlive or Resolve was built or run; FilmCraft code was read from a fresh shallow clone of tag **v0.9.0** (`4a69a038`, the newest FilmCraft tag) and compared with v0.8.0 where a claim depends on the diff; the Resolve 21 manual (the same PDF as [74], SHA-256 re-checked) was searched as text; web pages were read as data. The only thing run is a small first-hand test of the OpenTimelineIO Python writer (OTIO 0.18.1, `pip install` in a scratch virtualenv) on synthetic PNGs. Evidence grades as before: **[T]** test exists or was run here, **[C]** code path read, **[V]** vendor or official doc, **[I]** issue or third-party report, **[E]** estimate, **UNVERIFIED** not checked. New sources are numbered [83] onward at the end of this section. Items are G1-G6 (the round-1 items are F1-F7).

### Answers at a glance

| # | Question | Short answer |
|---|---|---|
| G1 | What does Resolve 21 write for a still in FCPXML, and does it read FilmCraft's `asset-clip` stills? | **Both halves UNVERIFIED after a second search.** The manual only says Resolve imports stills of more than one frame from Final Cut Pro X XML and that exporting stills is limited to the FCP7 and FCPX XML dialects [86]. No Resolve-written still was found anywhere. The maker's check stays the only answer; it is now a 5-minute, two-part check (what Resolve writes, and whether it reads FilmCraft's file). Low priority: FCP7 XML and OTIO are the contract. |
| G2 | Does Resolve 21 resolve a relative `target_url`, or need `file://` plus a relink prompt? | **UNVERIFIED for the relative case, but the downside is bounded and a better route exists.** The manual documents a Load OTIO dialog that links media "using the embedded file paths" and, if it cannot find them, **prompts for a folder and searches all its subfolders** [86]. For a path-independent route use an **`.otioz` bundle** (Resolve unzips the media beside it "unzip themselves into the same folder as that .otioz file, and automatically link themselves" [86]); the container can build one with the OTIO Python adapter without knowing the maker's drive letters (tested here, [T]). No second URL-style OTIO is needed. |
| G3 | FilmCraft GUI locations | **Markers > Export Markers as CSV…** (menu bar, no shortcut). **There is no image-sequence option inside File > Import…** (that is the operating-system file picker). Image sequences come from **File > Import Image Sequence…**, from the **Media Browser panel** ("Import as Image Sequence" checkbox or right-click item), or from **Edit > Preferences > Media… > "Import numbered stills as image sequences"** (default off). |
| G4 | `prefs.set` key and value for the Indeterminate Media Timebase | Key **`media.indeterminateTimebase`**, value a **JSON string** from `23.976, 24, 25, 29.97df, 29.97, 30, 50, 59.94df, 59.94, 60` (default `29.97df`). **The obvious CLI form `value=25` fails** (the CLI turns it into a JSON number and the preference is a string) [C]. Headless CLI sessions **do not load or save preferences**, so the setting must be made in the same `run` script as the import, or in the running app through `--bridge`. |
| G5 | Maker's hardware, versions, build type | **Still not answerable from here.** An extended read-only PowerShell block (G5) adds CPU architecture, MSI-versus-portable detection and installed versions of every Craft app. Send it now. |
| G6 | Tags and PR #1763 | At 06:18 UTC: **no FilmCraft v0.10.0 tag**; **no EffectCraft v0.12.0 tag** (but `main` is a "Release 0.12.0" commit); **PR #1763 still open, unreviewed, head unchanged** since round 1. New: SoundCraft `main` is a "Release 0.9.0" commit, untagged. Both untagged `main` commits differ from the last tag only in `Cargo.toml` and `Cargo.lock`. |

### G1. Resolve 21 and stills in FCPXML

**What the manual says [V].** Resolve 21 Reference Manual, chapter 22, "About Supported Still Image Formats": Resolve imports "greater-than-one-frame-in-duration TIF, JPG, PNG, DPX, TGA, and DNG still image files that appear in Final Cut Pro X, Final Cut Pro 7, and Premiere Pro XML files, and AAF files exported from Media Composer. These clips appear as ordinary clips in the DaVinci Resolve Timeline. Export of still images is limited to Final Cut Pro 7 and Final Cut Pro X XML formats." [86]. So: (a) a FilmCraft still (5 s by default) clears the "more than one frame" condition; (b) Resolve's FCPXML export is documented to carry stills; (c) the manual names no element and no FCPXML version.

**What a second search added: nothing decisive [I].** I looked for any Resolve-written FCPXML that contains an image. Searched: general web queries for Resolve FCPXML stills; the OpenTimelineIO `otio-fcpx-xml-adapter` sample directory (five samples, all named `fcpx_*`, all Final Cut-written [93]); the README of a Kotlin parser built for Resolve-exported FCPXML (no mention of stills, spine element types or samples [92]); an open issue comparing a tool's FCPXML with Resolve's (mentions `asset-clip` references only, no stills, no version [92]). GitHub code search is blocked in this container, so repository-wide searches for Resolve-written samples were not possible. **Resolve 21's still element: UNVERIFIED. Whether Resolve 21 reads FilmCraft's FCPXML stills: UNVERIFIED.**

**What FilmCraft does with each possible Resolve output [C, v0.9.0].** `fcpxml.rs` reads `asset-clip`, reads a `clip` by taking its first inner `video`/`audio`/`asset-clip` that has a `ref`, and skips a bare storyline `video` with the log line "FCPXML <tag> elements are not supported and were skipped" (round 1, [69]; the importer is unchanged between v0.8.0 and v0.9.0, checked by diff). So a Resolve-written bare `<video>` still would be dropped by FilmCraft, an `asset-clip` or `<clip>`-wrapped still would be read. FilmCraft's own exporter writes a still as an `asset-clip` on an `<asset>` whose `duration` is the still's duration (5 s by default), `hasVideo="1"`, a `format` with a `frameDuration` at the Indeterminate Media Timebase rate, and `<media-rep src="file:///C:/...">` (an absolute file URL; a relative path stays relative) [85].

**Maker's check (replaces the F1 check; run it inside the single Resolve session in G2).** Takes about 5 minutes with the two-still test project that R7 already needs.
1. *What Resolve writes.* In Resolve, put two PNGs on a timeline (5 s each; the Edit page, drag from the Media Pool), choose File > Export > Timeline… and pick FCPXML in the format list. Write down which FCPXML versions the list offers (a 2026 secondary source says 1.9; UNVERIFIED for 21). Open the file in Notepad and search for a PNG's file name. Write down (a) the element name that carries the still in the `<spine>`: `video`, `asset-clip` or `clip`; (b) the `<asset>`'s `duration` (`0s` or a number) and whether its `<format>` has a `frameDuration`; (c) the `src=` form.
2. *Whether Resolve reads FilmCraft's file.* In FilmCraft, with the same two stills on a sequence, File > Export > FCPXML… and save beside the media; in Resolve, File > Import > Timeline… (tick "Use sizing information"; leave "Mixed frame rate format" on "DaVinci Resolve") and pick the `.fcpxml`. Write down: stills online or offline, duration (5 s expected), any dialog.
3. Paste both results into the private repo notes; the files hold only local paths.

**Consequence.** None for the plan: FCPXML stays the untested third option, FCP7 XML and OTIO remain the contract (F1 decision unchanged). If step 1 shows a bare `<video>`, record "FilmCraft cannot read Resolve's FCPXML stills" and keep FCPXML out of every return path.

### G2. Relative `target_url` in Resolve 21 (and the `.otioz` route)

**What the manual documents [V]** (chapter 22, "Conforming OTIO Files" and "Importing OTIO Project Files", printed pages 544-547; chapter 190, "Exporting to OTIO", p. 4242) [86]:
- Import: File > Import Timeline (Shift-Command-I on a Mac; the Windows key is UNVERIFIED), or the Media Pool right-click Timelines > Import > AAF/EDL/XML/DRT/ADL/OTIO. A "Load OTIO" dialog follows. It has the options **"Automatically set project settings"**, **"Automatically import source clips into media pool"**, "Ignore file extensions when matching", "Set timeline resolution to", "Timeline frame rate", "Use drop frame timecode", "Mixed frame rate format". It has **no "Use sizing information" option**, which the XML and AAF dialogs have; OTIO import therefore cannot bring transforms, consistent with OTIO carrying no motion.
- Linking: "Automatically import source clips into media pool: ... automatically import the media referenced ... using the embedded file paths. If DaVinci Resolve can't locate the media at those locations, you'll be prompted to manually select a directory where the clips are located." The prompt offers Yes (pick a folder; "all subfolders will be automatically traversed as well") or No (import with all offline clips, shown in red). A warning says choosing a volume's top level can be very slow.
- Bundles: ".otio ... require the end user to link the Timeline to their own copies of the media. .otioz: bundle files contain both the Timeline metadata and all of the Timeline's media assets zipped together ... assures that whoever imports the file has all the media needed and is linked automatically." And: "If an .otioz file was selected for import, the media assets will unzip themselves into the same folder as that .otioz file, and automatically link themselves. Ensure you have enough storage space for this."
- Nothing in the manual says how a **relative** path is resolved or against what, and nothing says whether a `file:///` URL is accepted. **Resolve 21's handling of a relative `target_url`: UNVERIFIED.** Project Settings > Path Mapping ("Automatically setup when relinking", p. 168) says that once one offline clip is relinked Resolve maps the same relative layout for other offline media in the project [86]; that is about relinking, not about OTIO import, but it suggests one prompt per project, not one per clip.
- Third-party leads, none usable: an Adobe community thread was fetched, but its readable part (13,337 characters) has nothing on `target_url` [90]; a search-result summary of a later part claimed posts about a `file://` prefix and Resolve 20.2, and a second summary described the same posts the opposite way round, so I treat it as noise. The Resolve Python API has `ImportTimelineFromFile` with a `sourceClipsPath` "fallback search path" option [91], but the manual says external scripting is **Resolve Studio only** (only the in-app Console is available otherwise) [86], so it is not available to us on the free edition.

**What the OTIO side says [V][T].** The OTIO docs give no rule for `target_url` in the schema page [88] and call it "a file path or network URL, etc." in the tutorial [89]. The file-bundle adapter docs allow two forms: an absolute `file:///path/to/file` URL, or a relative path "relative to the current working directory of the command running the adapter" [87]. So "relative to the `.otio` file's folder" is a convention that several tools share, not an OTIO guarantee. First-hand test with OTIO 0.18.1 on two synthetic PNGs [T]:
- A `.otio` written with `target_url` `media/ch01_s01.png` keeps it verbatim.
- `write_to_file(tl, "ch01.otioz")` with the process started in the folder that holds `media/` produces a zip with `version.txt`, `content.otio` and a flat `media/ch01_s01.png`, `media/ch01_s02.png`; the `target_url`s inside `content.otio` are `media/<basename>`.
- The same call started from a different folder raises `NotAFileOnDisk` (the relative path was resolved against the process's working folder, as the docs say).
- Passing `file:///.../media/ch01_s01.png` URLs also works and the bundle again stores `media/<basename>`; media basenames must be unique (they are: shot-id file names).
So the container can build an `.otioz` from absolute paths in the container, and the result contains only relative paths and the media. It never needs the maker's drive letters.

**What FilmCraft writes [C, v0.9.0].** `otio.rs::media_ref` writes `target_url` relative to the **`.otio`'s own folder** when it can (`relative_to` is the export path's parent, `engine/src/interchange.rs` line 147), including `../` segments, and falls back to an absolute `file:///C:/...` URL when media and OTIO share no drive prefix [85]. FilmCraft does not read `.otioz` (no mention in the source). Kdenlive cannot decode `file://` (F3).

**Decision for the bundle (judgement [E], to be confirmed by the maker's Resolve session).**
1. The contract file is `chNN.otio` with **relative** `target_url`s, as already decided (FilmCraft and Kdenlive read it).
2. For Resolve add `chNN.otioz`, built in the container with the OTIO Python adapter from the same timeline. It is Resolve-only, duplicates the stills (about the size of the chapter's media, so budget disk and do not ship it for the whole film at once) and unzips next to itself, so import it from a scratch folder. Resolve's `.otioz` import with stills is UNVERIFIED; the manual describes it generally.
3. **No second URL-style OTIO.** If the relative `.otio` does not link in Resolve, the documented prompt (Yes, pick the bundle folder) is the fallback: one click, subfolders searched.
4. Minimal command for the container (not run for the final bundle; the test above used exactly this call): `otio.adapters.write_to_file(timeline, "chNN.otioz")` run with the working folder set to the bundle folder, or with absolute paths in `target_url`.

**Maker's Resolve session (one sitting, about 15 minutes, replaces the Resolve line in R7).** Import in this order and write one line each, then mark the matrix cells: (1) `chNN.xml` (FCP7 XML; tick "Use sizing information"; check Position/Scale keyframes and Opacity, F2); (2) `chNN.otio` from the bundle folder (did the stills link on their own, or did the folder prompt appear; are durations 5 s; is anything red); (3) `chNN.otio` copied alone into an empty folder (what happens to the prompt; this tells whether the paths are read relative to the file); (4) `chNN.otioz` (links on its own?); (5) the two FCPXML checks from G1. Record the Resolve version (Help > About).

### G3. FilmCraft GUI locations (v0.9.0; identical in v0.8.0 for these items)

**Marker list: Markers > Export Markers as CSV….**
- Command `markers.exportCsv`, label "Export Markers as CSV…", menu path `["Markers"]`, no keyboard shortcut (`commands.rs` line 2446) [C]. The README says the same: "export sequence review notes with **Markers ▸ Export Markers as CSV…**" [V][83].
- On Windows and Linux the menus are an in-window menu bar (File, Edit, Clip, Sequence, Markers, Graphics and Titles, View, Window, Help; `menus.rs` line 676), shown after the Import/Edit/Export mode tabs; only macOS uses a native menu bar (`apps/filmcraft/src/main.rs` lines 334-340) [C]. The item is **disabled until a sequence is open**.
- A UI test drives exactly this click path, then checks that a save dialog opens with the filter "Marker report (CSV)", extension `csv`, a suggested name ending `.csv`, and that the status line then starts with "Exported " (`export_menu_ui.rs`, `marker_csv_menu_exports_sequence_review_notes`) [T]. The dialog is the operating-system save dialog (the `rfd` library).
- What it writes (from `docs/agents.md`): all markers of the **active sequence** (including colours hidden in the UI and markers outside In/Out; **not** clip or source markers), UTF-8 CSV with header and CRLF records, columns Sequence, Marker ID, Name, Comment, Kind, Color, Start Timecode, End Timecode, Duration Frames, Start Ticks, Duration Ticks, Frame Rate; it leaves the project, dirty flag and undo history untouched [V][83]. Headless: `filmcraft-cli --project p.fcproj exec markers.exportCsv path=review.csv`.
- Not read: the row position inside the Markers menu.

**Image sequence: not in the Import dialog.**
- **File > Import…** (`file.import`, Ctrl+I on Windows since `Cmd` maps to `Ctrl`) and the Import mode's "Browse files…" card both open the operating-system file picker, whose filter lists media, caption and interchange extensions; it has no image-sequence checkbox. The engine option `imageSequence` is only reached through the routes below [C][83].
- **Route 1, the direct one: File > Import Image Sequence…** (`file.importImageSequence`, listed under `["File"]`, `project_tools.rs` line 117). It opens the file picker filtered to still-image types; **pick the first numbered frame**. The UI test `import_image_sequence_from_the_file_menu_and_media_browser` asserts the menu path and a 5-frame result [T].
- **Route 2: the Media Browser panel** (Window menu panel list, Shift+8; `media_browser.rs`). Tick **"Import as Image Sequence"** in the panel's second toolbar row (next to "Ingest"), select the first frame, then File > Import from Media Browser (Ctrl+Alt+I) or the Import context item; or right-click a numbered still and choose **"Import as Image Sequence"** (shown only for names that contain a digit run) [C].
- **Route 3: Edit > Preferences > Media… > "Import numbered stills as image sequences"** (`media.importImageSequences`, default **off**). When on, File > Import… of a **single** numbered still with later numbers beside it is imported as a sequence (`detect_image_sequence`, only when exactly one path is imported) [C].
- How the sequence is built (`crates/media/src/sequence.rs`, `commands.rs::import_image_sequence`) [C]: the number is the **last digit run in the file name**; the file must be a still type; frames run from the chosen file's number to the **highest number present**; a missing number is reported and shows the nearest earlier frame; the frame rate is the **Indeterminate Media Timebase** at import, not the comp's rate; the result is one movie-like item. PNG, JPEG, TIFF, BMP, WebP, GIF, Targa, DPX, OpenEXR and DNG decode.
- For Exercise 8: set the Indeterminate Media Timebase to the EffectCraft comp's frame rate **before** the import (G4), name the frames `title_0001.png`, pick `title_0001.png`.
- **Trap for the stills chapters [C]:** our shot files `ch01_s01.png`, `ch01_s02.png` end in a digit run, so with Route 3's preference **on**, importing `ch01_s01.png` alone would be taken as a 2-frame sequence. Keep that preference **off** (the default) for the film's stills; multi-file imports skip detection.

### G4. `prefs.set` and the Indeterminate Media Timebase

**Key and values [C][T].** The preference is `media.indeterminateTimebase` (schema `settings.rs` line 1209; struct `MediaPrefs.indeterminate_timebase: String`, default `"29.97df"`, `autosave.rs` lines 241-272). It is a *choice* whose valid values are exactly `23.976`, `24`, `25`, `29.97df`, `29.97`, `30`, `50`, `59.94df`, `59.94`, `60` (`TIMEBASE`, `settings.rs` line 934; the GUI shows them as "25 fps", "29.97 fps Drop-Frame", and so on). `timebase_rate` maps `25` to 25 fps and any unknown string to 29.97 [C]. The repo's own tests set it as the **string** `"25"` (`image_sequence_tests.rs`, `settings_tests.rs`) [T]. GUI: **Edit > Preferences > Media…** (Windows and Linux; on macOS FilmCraft > Settings), field "Indeterminate Media Timebase".

**Why the obvious CLI form fails [C, not run].** The CLI parses `key=value` values as JSON first (`args.rs::parse_value`), so `value=25` becomes the JSON number 25. `prefs.set` accepts a number for a choice at the validation step (it compares the number's text with the choices) but then stores a number in a field that is a string, and the final type check refuses it with "invalid type: integer ... expected a string" (`autosave.rs::Preferences::set`, lines 447-483). The same applies to `23.976`, `24`, `29.97`, `30`, `50`, `59.94`, `60`; `29.97df` and `59.94df` work only because they are not valid JSON. A string value needs JSON quotes, which a shell may strip; the repo's own unit test shows the form `s=\"7\"` giving a string. Passing quotes through Windows PowerShell 5.1 to a native program is a known trouble spot (UNVERIFIED here), so use a script file.

**Preferences are not persisted by the headless CLI [C].** Only the desktop app calls `start_autosave` (`apps/filmcraft/src/main.rs` line 211), which loads `preferences.json` and sets the path that `set_prefs` saves to; `filmcraft-cli` builds `Session::default()` (`apps/filmcraft-cli/src/main.rs` lines 150-170; no preferences are loaded or saved there), so every CLI process starts at the default `29.97df` and a `prefs.set` there lasts only for that process. Where the file lives for the app: `%APPDATA%\FilmCraft\preferences.json` for the MSI, `<exe folder>\data\preferences.json` when `portable.txt` sits beside the exe (`autosave.rs` lines 495-520) [C]. It is an **app-level** setting, not part of the `.fcproj`; the project stores each still's frame rate as read at import, but a changed still file on disk is re-stamped from the **current** preference (`media_watch.rs` line 137) [C]. Set it once, before any import, and record it in the manifest.

**Commands for the skill's guard (read from the code and the repo's tests, not run).**
1. Headless, one process (agent in the container or maker's CLI). Put the guard and the import in one JSON-lines script `guard.jsonl`:
   ```
   {"id":"prefs.set","params":{"key":"media.indeterminateTimebase","value":"25"}}
   {"id":"file.import","params":{"paths":["media/ch01_s01.png","media/ch01_s02.png"]}}
   {"id":"prefs.get","params":{"key":"media.indeterminateTimebase"}}
   ```
   Run it from the bundle folder (relative paths are taken from the folder you run it in [E]): `filmcraft-cli --project ch01.fcproj --save run guard.jsonl` (`run`, lines 347-374, reads one JSON object per line with `id` and `params`, stops at the first failure unless `--keep-going`, and prints one JSON line per command) [C]. Check the third output line is `"25"` and that the imported stills report a 25 fps rate (`inspect project`).
2. Running app: start `"C:\Program Files\FilmCraft\filmcraft.exe" --control 9876` (loopback only, `docs/agents.md`), then `filmcraft-cli --bridge 127.0.0.1:9876 run prefs25.jsonl` with the first line above in `prefs25.jsonl`. This runs `prefs.set` inside the app's session, which saves `preferences.json` [C]. Read back with `filmcraft-cli --bridge 127.0.0.1:9876 exec prefs.get key=media.indeterminateTimebase`.
3. Bash only (not PowerShell): `filmcraft-cli exec prefs.set key=media.indeterminateTimebase value='"25"'`.
Nothing here was run: the CLI was never built or started (rule of this track).

### G5. Maker's hardware, versions and build type (still outstanding)

Nothing in the repo or the conversation holds these; the user's 2026-10-18 replies gave Windows and nothing more. The F6 block stands. Two additions from the packaging files: FilmCraft's README (lines 329-331) and SoundCraft's list Windows **x64, arm64 and x86** builds, so the architecture matters for which asset and hash applies [96]; and the MSIs are per-machine, so MSI installs show up in the Windows uninstall registry while a portable zip does not. A portable FilmCraft has `portable.txt` beside the exe and keeps its data in `data\`; EffectCraft accepts `portable.txt` or `EffectCraft.portable`; I found no marker file in the SoundCraft source, so look for a `data` folder beside its exe [96]. Extended block, **not run, written from memory, UNVERIFIED** (read-only; prints no names or serial numbers):

```powershell
# Life Journey inventory v2: paste the output into the private repo notes
"Arch: " + $env:PROCESSOR_ARCHITECTURE
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
"RAM GB: " + [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, BuildNumber
Get-PSDrive -PSProvider FileSystem | Where-Object { $null -ne $_.Used } | Select-Object Name, @{n='FreeGB';e={[math]::Round($_.Free/1GB)}}
# MSI installs of any Craft app (a portable zip will not be listed)
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -match 'Craft' } | Select-Object DisplayName, DisplayVersion
```
Then, for each Craft app, from its own folder (the MSI default is `C:\Program Files\<App>\`; a portable zip is wherever it was unzipped; if the ArtCraft launcher installed the app, find its folder with Task Manager > right-click the running app > Open file location): `.\filmcraft-cli.exe --version` (likewise `effectcraft-cli`, `soundcraft-cli`), `Test-Path .\portable.txt` (True = a portable FilmCraft or EffectCraft), and for a zip `Get-FileHash -Algorithm SHA256 <zip>`. VRAM: Task Manager > Performance > GPU > "Dedicated GPU memory" (not the WMI `AdapterRAM` value). The orchestrator should send this block now; the maker can run it in two minutes, and half of Q4, Decision 1 and the pin choice wait on it.

### G6. Tags and PR #1763 as of 2026-10-18 06:18 UTC

| Item | State | How checked |
|---|---|---|
| FilmCraft newest tag | **v0.9.0** (`4a69a038`); `main` is the same commit; **no v0.10.0** (its `SHA256SUMS.txt` returns 404; v0.9.0's returns 200) | `git ls-remote --tags`, curl [94] |
| EffectCraft newest tag | **v0.11.1** (`2a012268`); `main` = `f36b2b3e` "Release 0.12.0", committed 2026-10-17 21:43:07 -04:00; **no v0.12.0 tag** (its `SHA256SUMS.txt` returns 404). `main` differs from v0.11.1 only in `Cargo.toml` (one line) and `Cargo.lock` | same, plus `git diff --stat v0.11.1 HEAD` [94] |
| SoundCraft newest tag | **v0.8.0**; `main` = `c1bf044a` "Release 0.9.0", committed 21:43:22 -04:00 the same evening; **no v0.9.0 tag** (404). `main` differs from v0.8.0 only in `Cargo.toml` and `Cargo.lock` | same [94] |
| PR #1763 (`EFFECTCRAFT_CPU_INFLIGHT`) | **Open**, "No reviews", no maintainer comment, head still `cd5a45d8` (the same commit round 1 read); the page says unset or blank = no cap, an invalid value logs a warning and leaves frames uncapped, and a GPU cap also set means "the smaller one applies" | WebFetch and `git ls-remote refs/pull/1763/*` [95] |

Reading: the three repos bumped their versions within 15 seconds of each other, FilmCraft's tag followed, the other two have not yet; so EffectCraft v0.12.0 and SoundCraft v0.9.0 tags are likely to appear soon with the same code as v0.11.1 and v0.8.0 [E]. The FilmCraft v0.9.0 pin row from F7 stands. Procedure before and during spike S1:
1. On the day S1 starts, run `for r in filmcraft effectcraft soundcraft; do git ls-remote --tags --refs https://github.com/storytold/$r | sed 's#.*refs/tags/##' | sort -V | tail -2; done` and the PR page.
2. If a **new tag** has appeared, do not re-pin in the middle of the spike. Test the pinned tag; then, for the new tag, run `git diff --stat <pinned>..<new> -- crates/interchange crates/engine/src/commands.rs crates/engine/src/interchange.rs crates/engine/src/settings.rs crates/engine/src/autosave.rs apps/filmcraft-cli`. A diff that touches only `Cargo.*` means the same behaviour (re-check the zip's SHA-256 against the new `SHA256SUMS.txt`). Anything else: repeat the five-minute test on it.
3. If #1763 has merged and a tag contains `EFFECTCRAFT_CPU_INFLIGHT`, use `EFFECTCRAFT_CPU_INFLIGHT=1` (or 2) as the first mitigation and still measure peak memory; until then F4 stands.

### Edits these answers imply (for the scribes; not applied here)

1. **Playbook Step 10 and the skill's hand-back step.** Replace the TODO by: "Markers > Export Markers as CSV… (needs an open sequence; sequence markers only). Headless: `markers.exportCsv path=review.csv`."
2. **Playbook Exercise 8 step 5.** Replace the TODO by: "File > Import Image Sequence… and pick the first numbered frame (or tick 'Import as Image Sequence' in the Media Browser). Set Edit > Preferences > Media… > Indeterminate Media Timebase to the comp's frame rate first; it sets the sequence's rate. There is no such option in File > Import…". Add a pitfall: keep Preferences > Media > "Import numbered stills as image sequences" **off** for the stills chapters.
3. **Skill step 7 (CLI guard) and playbook Template B.** Use the G4 commands: key `media.indeterminateTimebase`, **string** value; headless guard and import in the same `run` script; or `--bridge` against the running app; never `value=25`. State that the setting is app-level, persisted in `preferences.json`, and that changed still files are re-stamped from the live value.
4. **R3, skill steps 6-8, playbook Step 7 and Pitfall 6.** Keep OTIO `target_url`s relative. Add `chNN.otioz`, built in the container, as the Resolve-only companion (replaces "two OTIOs, one with URLs"); `.otioz` is not read by FilmCraft. State that Resolve's handling of relative paths is UNVERIFIED, the documented fallback is the folder prompt, and the maker's Resolve session is the test.
5. **R7 and playbook Exercise 6.** Replace the Resolve line by the five-import session in G2 (FCP7 XML, `.otio` in place, `.otio` alone in an empty folder, `.otioz`, the two FCPXML checks).
6. **Playbook Pitfall 8 and review nudge 5.** F1 plus G1: still UNVERIFIED for Resolve; the maker's check is now part of the Resolve session.
7. **Open questions.** Closed: marker CSV location, image-sequence location, `prefs.set` format, tag/PR state at 06:18 UTC. Open: Resolve FCPXML stills (both halves), Resolve relative `target_url`, Resolve `.otioz` with stills, the Windows shortcut for Import Timeline, F6 inventory.

### Sources (round 2, continuing the numbering)

- [83] FilmCraft source at tag v0.9.0 (shallow clone of `https://github.com/storytold/filmcraft`, commit `4a69a038d32761f604b3c7e4845b21fb40b3cbe4`, run 2026-10-18 about 06:15 UTC): `README.md` line 86; `docs/agents.md` (CLI, `markers.exportCsv`, install paths, `--control`); `crates/ui-egui/src/lib.rs` (`EXPORT_SAVE_DIALOGS` line 264, `file_dialog` lines 1271-1303); `crates/ui-egui/src/menus.rs` (`MENUS` line 676, `menu_bar` line 883, dialog routing lines 574-583); `crates/ui-egui/src/header.rs` and `apps/filmcraft/src/main.rs` lines 334-340 (native menu on macOS only); `crates/ui-egui/src/panels/{media_browser.rs,import_mode.rs}`; `crates/ui-egui/tests/{export_menu_ui.rs,menus_ui.rs}`; `crates/engine/src/{commands.rs (markers.exportCsv line 2446, file.import line 1332, import_image_sequence line 669, prefs.set line 1573),project_tools.rs (lines 93-125, 258),marker_export.rs,media_browser.rs}`; `crates/media/src/sequence.rs`; `crates/ui-egui/src/dock.rs` (panel shortcuts). `git diff v0.8.0 v0.9.0` over the menu, preference, importer and CLI files shows only the scratch-folder trust change (`autosave.rs`, `project_tools.rs`, `lib.rs` 2 lines): the menus and preferences answered here are the same in both tags.
- [84] FilmCraft v0.9.0 preferences and CLI: `crates/engine/src/autosave.rs` (`MediaPrefs` lines 241-290, `Preferences::set` lines 447-483, data directory and `portable.txt` lines 495-520); `crates/engine/src/settings.rs` (`timebase_rate` line 790, `TIMEBASE` line 934, field line 1209, `validate` line 1387); `crates/engine/src/lib.rs` (`start_autosave` line 577, `set_prefs` line 649); `crates/engine/src/{settings_tests.rs,image_sequence_tests.rs,media_watch.rs (line 137)}`; `apps/filmcraft-cli/src/{main.rs (Backend::open lines 150-170, run lines 349-376),args.rs (parse_value, params_from, unit tests)}`; `apps/filmcraft/src/main.rs` line 211.
- [85] FilmCraft v0.9.0 interchange writers: `crates/interchange/src/otio.rs` (`media_ref` lines 223-245, `abs_url`), `common.rs` (`relative_path` line 137, `path_to_file_url`), `fcpxml.rs` (`asset` lines 716-750, clip builder lines 983-990, importer lines 383-406), `lib.rs` (format detection; no `.otioz`), `crates/engine/src/interchange.rs` line 147 (`relative_to` = the export file's folder).
- [86] DaVinci Resolve 21 Reference Manual, the same PDF as [74] (SHA-256 `7bfdcf0296bd1e48aeca58a3d66026821cf9dec5f1f0e5fe7a4b936dbe34e799`, re-checked 2026-10-18), searched with `pdftotext`; printed pages 168 (Path Mapping), 481-486 (supported effects, stills), 520-547 (Reconform step 5, XML/AAF/OTIO import dialogs, "Conforming OTIO Files", "Importing .otioz Files"), 4242 ("Exporting to OTIO"), and the Preferences > General entry "External Scripting Using: (Resolve Studio only)". A Blackmagic "Studio and iPad Features" PDF (September 2026) found in the scratchpad also lists "Scripting API: Studio" for desktop; its download URL was not recorded, so it is not relied on.
- [87] `https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-filebundles.html` (WebFetch 2026-10-18, summarised by a small model): `target_url` forms for the bundle adapters, absolute `file:///` or relative to the working folder of the adapter command.
- [88] `https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-serialized-schema.html` (WebFetch 2026-10-18): `ExternalReference.target_url` has no description; `ImageSequenceReference` example uses a `file:///` base.
- [89] `https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-timeline-structure.html` (WebFetch 2026-10-18): "The target_url tells us where to find the media (e.g. a file path or network URL, etc.)".
- [90] `https://community.adobe.com/t5/premiere-pro-beta-discussions/now-in-beta-otio-import-and-export/m-p/14985932` (WebFetch 2026-10-18; readable part 13,337 characters, nothing on `target_url`). A search-result summary of other posts in the thread (Resolve 20.2, `file://`) is contradictory and unverified.
- [91] `https://gist.github.com/mhadifilms/2b84d469135315793220dbf2226cbe63` (WebFetch 2026-10-18): a third-party Resolve scripting reference; shows `ImportTimelineFromFile` options `timelineName`, `importSourceClips`, `sourceClipsPath` ("Fallback search path"); says scripting is not available in the free version (the manual [86] says external scripting is Studio only).
- [92] Search-result and page reads for Resolve-written FCPXML stills (2026-10-18): `https://github.com/Cubxity/ResolveParser` (README only), `https://github.com/striwmt/ai-director/issues/1` (page read; Resolve sample not shown), `https://discussions.apple.com/thread/253847393` and `https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=151297` (search results only, not fetched; the second was summarised as saying Resolve 17.4.2 exports FCPXML 1.9), `https://vod.ing/blog/fcpxml-for-davinci-resolve` (see [81]). None shows a Resolve-written still.
- [93] `https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter/tree/main/tests/sample_data` (WebFetch 2026-10-18): five samples `fcpx_clips`, `fcpx_event`, `fcpx_example`, `fcpx_library`, `fcpx_project` (the page may be incomplete).
- [94] `git ls-remote --tags` and `git ls-remote HEAD` for `storytold/filmcraft`, `effectcraft`, `soundcraft`; shallow clones of `main` of effectcraft (`f36b2b3e`) and soundcraft (`c1bf044a`) with `git diff --stat v0.11.1 HEAD` and `git diff --stat v0.8.0 HEAD`; curl status codes for `releases/download/<tag>/SHA256SUMS.txt` (effectcraft v0.12.0: 404; soundcraft v0.9.0: 404; filmcraft v0.10.0: 404; filmcraft v0.9.0: 200); all run 2026-10-18 06:12-06:20 UTC.
- [95] `https://github.com/storytold/effectcraft/pull/1763` (WebFetch 2026-10-18; summarised by a small model) and `git ls-remote https://github.com/storytold/effectcraft 'refs/pull/1763/*'` (head `cd5a45d853290b7a1646c2ee930c30c348650a18`).
- [96] Packaging: `packaging/windows/{filmcraft,effectcraft,soundcraft}.wxs` at v0.9.0 / `main` (`Scope="perMachine"`, install folder under `ProgramFiles6432Folder`, `filmcraft.exe` and `filmcraft-cli.exe`); `filmcraft/README.md` lines 329-331 and `soundcraft/README.md` lines 264-266 (x64, arm64, x86 assets); `effectcraft/docs/agents.md` line 57 (MSI CLI path); `effectcraft/crates/host/src/app_dirs.rs` (`PORTABLE_MARKERS`: `portable.txt`, `EffectCraft.portable`); FilmCraft `autosave.rs` `PORTABLE_MARKER`; a grep of the SoundCraft source for `portable.txt` found nothing.
- [97] First-hand test, 2026-10-18 about 06:21 UTC: OpenTimelineIO 0.18.1 (`pip install opentimelineio` in a scratch virtualenv) with two synthetic 320x180 PNGs made by ImageMagick 6.9.12: `.otio` and `.otioz` writing with relative and `file:///` `target_url`s, the `NotAFileOnDisk` failure from a different working folder, the bundle listing (`version.txt`, `content.otio`, `media/*.png`) and a read-back.
