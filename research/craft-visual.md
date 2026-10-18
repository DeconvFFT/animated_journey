# ArtCraft visual apps as refinement layers: PhotoCraft, VectorCraft, LightCraft — research notes

Track `craft-visual`. Researcher: Sonnet. Date of research: 2026-10-18 (Sunday). Deadline for the project: Saturday 2027-02-27.

**How to read the evidence tags.** Every capability we need is tagged:
- **[T]** proven by a named test or corpus in the repo at the tag I read (I read the test; I did not run it).
- **[C]** present in code or in the app's own technical docs, with no test I could find for the exact behaviour.
- **[V]** vendor claim or README/marketing percentage (a lead, not evidence).
- **[U]** unverified: I could not check it from this container.

**What I did and did not do.** I shallow-cloned `storytold/photocraft` at tag `v0.9.0` (commit `c699e3c`), `storytold/vectorcraft` at `v0.12.0` (`8bc6532`) and `storytold/lightcraft` at `v0.8.0` (`16dbb90`) and read them with grep/read. I also made blobless bare clones to read tag dates and commit subjects (no file contents were checked out from them). **I built, installed and ran nothing from these repos.** The only code I ran was my own stdlib Python to create and sanity-check the acceptance-test fixtures (they are well-formed; I have not opened them in the Craft apps). github.com HTML pages and the API returned 403 from this container (see Open questions), so GitHub URLs below are locators built from tag + path; I read the files locally.

---

## Summary

1. **The whole suite is 18 days old.** First commit 2026-09-30 in all three repos. Tags: PhotoCraft 11 (2026-10-01 to 2026-10-14), VectorCraft 14 (10-02 to 10-16), LightCraft 9 (10-02 to 10-14). "Release cadence over eight weeks" is therefore the entire history: a tag every 1 to 2 days, then a pause (PhotoCraft and LightCraft have had no tag for 4 days; `main` is 301, 476 and 576 commits past the newest tags). [43]
2. **Newest tags today (2026-10-18):** PhotoCraft `v0.9.0` (10-14), VectorCraft `v0.12.0` (10-16), LightCraft `v0.8.0` (10-14). getartcraft.com still shows 0.7.0, 0.9.0 and 0.6.0, and its Windows download lists the CLI only as a macOS zip. If the maker installed from the website, they have those older builds. [43][44]
3. **The Windows MSI and the portable zip of all three apps ship the CLI** (`photocraft-cli.exe`, `vectorcraft-cli.exe`, `lightcraft-cli.exe`, console subsystem, statically linked CRT, no VC++ redistributable). Not on PATH. Cited from the WiX files and `package.ps1`. [11][29][41]
4. **Best agent-to-PhotoCraft layered contract: OpenRaster (.ora).** It is a zip of PNGs plus `stack.xml` that any script can write with the standard library; PhotoCraft reads and writes names, visibility, opacity, blend modes, nested groups, offsets (also off-canvas) and 8/16-bit; and it is the only layered format with a recorded third-party check (Krita 5.2.9, 2026-10-09: 32 of 35 files within 3/255; Krita rendered 33 of 34 PhotoCraft re-exports identically). It cannot carry adjustment layers, layer styles, vector masks, live text or non-sRGB profiles. [T][4]
5. **PSD is a fallback input and a private save format, not the pipeline's contract.** PhotoCraft's PSD reader is broad (groups, pixel and vector masks, 16 adjustment kinds, type, shapes, smart objects, 8/16/32-bit, ICC) but the vendor's own gap list says "PSDs we write are not always accepted by Photoshop" and no test opens its exports in a third-party editor (FILE-216-4). Against Photoshop-authored oracles PhotoCraft's render matches the file's own merged image for only **145 of about 256** files (56 percent; the vendor docs print both 256 and 258 as the total), 236 of 309 for the psd-tools set (76 percent). The README's "307 of 309" is a different thing: export-then-reimport self-consistency. [T][2][3][13]
6. **`photocraft-cli` can assemble and save a layered document headless, no GPU.** `run --new '{...}' --cmd file.placeEmbedded` with `"smartObject":false` places a PNG as a plain pixel layer named after the file; `layer.setProps` sets name, opacity and blend; `layer.newAdjustmentLayer.curves` adds an adjustment layer; `--out x.psd` or `x.ora` saves by extension. The engine, io and compositor crates have no wgpu dependency. [C][9][10]
7. **VectorCraft keeps ids, nested named groups and `data-*` attributes through an import/re-export, and loses `class`, `<style>` text, most filters, SMIL/CSS animation and transform attributes.** Ids become object names and are rewritten from names (hyphens, underscores, dots and letters survive; other characters become `_`; duplicates get `-2`). `data-*` (up to 64 per element, on g/a/use/path/rect/circle/ellipse/line/polyline/polygon/image only) is tested by an "animation rig" test, first shipped in v0.8.0. Classes are not kept: export can only generate `cls-1, cls-2...`. The export always rewrites `viewBox` to `0 0 W H`. [T][19][20][21][22]
8. **For GSAP/CSS animation the contract is: animate by `id` and `[data-*]`, add classes and `<style>` after the touch-up, and put pivots in `data-pivot` (transforms are baked).** Run `check_ids.py` (fixture provided) after every VectorCraft save.
9. **LightCraft treats TIFF/JPEG scans through the same develop pipeline as raw** (geometry, scene-linear tone, filmic tone map, OkLCh colour, curves, grain). Raw-only parts do not apply: Kelvin white balance (scans use a relative scale), camera matrices and profiles, DNG lens opcodes. Unedited JPEG passes through within 3/255 [T]. No scan or faded-print corpus exists. [T][C][35]
10. **LightCraft preset path is agent-friendly and scriptable:** `.lcpreset` is JSON (`{"format":"lightcraft.preset","version":1,"presets":[{id,name,group,settings}]}`); `lightcraft-cli run --script steps.jsonl` or `render in.tif -o out.jpg --preset ID --settings look.json --set light.exposure=0.3`; export naming templates `{name}`, `{seq:N}`, `{date:%Y-%m-%d}`. XMP `crs:` is read (approximate), never written; exact round trip is `lc:settings` JSON. [T][C][33][34][42]
11. **Recommended ~300 scans path:** LightCraft on the maker's PC (CLI script + `.lcpreset` + per-print white-balance pick in the GUI), gated on a 10-print pilot against darktable. Run the batch with `LIGHTCRAFT_GPU=0` to avoid DX12 driver risk. The scans should be processed locally: **scripts travel to the PC, scans never go to the cloud container** (Charter: personal material stays private).
12. **Stability is uneven and mostly unproven on Windows.** PhotoCraft has Windows CI (windows-latest) and the most safety plumbing (atomic saves, 10-minute autosave on by default, GPU start marker with Vulkan to DX12 to CPU fallback, `--safe-gpu`). VectorCraft and LightCraft have no workflow in the tree that runs the full test suite (VectorCraft: only an Affinity-corpus job on Ubuntu and a printing test job on windows-2022; LightCraft: none; the agents run `cargo xtask ci` locally), and their own docs say "Windows/Linux/browser QA" (VectorCraft) and "Windows installer UI unverified... DX12 unverified" (LightCraft gaps #27) are missing. [13][14][17][27][30][37]
13. **Data-loss guards landed late.** ORA "never overwrite an .ora with less than the document has" is first in `v0.9.0`; "Save: ask before overwriting a file another app changed" and "refuse to replace a read-only file" are only on `main` after `v0.9.0`. The website's 0.7.0 build has ORA but not the guard. [43]
14. **Privacy: no telemetry code path found in any of the three.** PhotoCraft links no HTTP client at runtime (reqwest appears in `Cargo.lock` only as a build-dependency of a Windows printing crate). VectorCraft has no HTTP client at all. LightCraft has its own rustls downloader used for opt-in model and place-name downloads. Control channels: PhotoCraft uses a bearer token; **VectorCraft and LightCraft have no authentication** on their loopback port. No source references `app.getartcraft.com`. [16][26][34][39]
15. **Web builds are real but are not the right learning route.** All three ship static wasm sites (PhotoCraft 23 MiB, VectorCraft 13 MB, LightCraft 13.5 MB raw); none needs COOP/COEP; PhotoCraft has `?cpu` and `?webgl`; VectorCraft's README documents `?cpu` but its code reads only `?webgl`; LightCraft is WebGL2 only and exposes `globalThis.lightcraft.command()`. The CLI/MCP route is strictly better for agents; use the web build only for UI screenshots. [12][29][38]

---

## Findings by question

### 1. Versions, cadence, Windows requirements, pin

**Newest tags, dates and cadence** (tag dates from `git for-each-ref --sort=creatordate` on blobless bare clones; `git ls-remote --tags` for the list) [43]:

| App | Newest tag | Tag date | Tags to date | All tags (date) | Website shows (2026-10-18) | Commits on `main` after tag |
|---|---|---|---|---|---|---|
| PhotoCraft | `v0.9.0` | 2026-10-14 | 11 | 0.1.0 (10-01), 0.1.1-rc.4 (10-01), rc.5 (10-02), 0.1.1 (10-03), 0.2.0 (10-05), 0.3.0 (10-07), 0.5.0 (10-08), 0.6.0 (10-09), 0.7.0 (10-10), 0.8.2 (10-12), 0.9.0 (10-14) | 0.7.0, "Early alpha" [44] | 301 |
| VectorCraft | `v0.12.0` | 2026-10-16 | 14 | 0.1.0 (10-02), 0.1.1 (10-03), 0.2.0 (10-05), 0.3.0 and 0.3.1 (10-06), 0.4.0 (10-07), 0.5.0 and 0.6.0 (10-08), 0.7.0 (10-09), 0.8.0 and 0.9.0 (10-10), 0.10.0 (10-12), 0.11.0 (10-14), 0.12.0 (10-16) | 0.9.0, "In development" [44] | 476 |
| LightCraft | `v0.8.0` | 2026-10-14 | 9 | 0.1.0 (10-02), 0.1.1 (10-03), 0.2.0 (10-05), 0.2.1 (10-06), 0.4.0 (10-08), 0.5.0 (10-09), 0.6.0 (10-10), 0.7.1 (10-12), 0.8.0 (10-14) | 0.6.0, "In development" [44] | 576 |

- Some minor versions never appear as tags on the remote (PhotoCraft 0.4.0, 0.8.0, 0.8.1; LightCraft 0.3.0, 0.7.0). Whether they exist as releases is **[U]** (release pages were 403).
- Commit rate is extreme (hundreds per day; PhotoCraft 2,498 commits, VectorCraft 3,889, LightCraft 2,913 in 18 days). The vendor says so itself: PhotoCraft's `docs/target-app-parity.md` records "about 1,230 issues filed since the first release (579 open on 2026-10-10)". [13]
- No `CHANGELOG.md` exists in any of the three trees. LightCraft keeps a user-facing `docs/whats-new.md` (entries 2026-10-02 to 10-14). For cadence I used tags and commit subjects. [40][43]
- Version-dependent facts that matter to us (first tag containing the commit, from `git tag --contains`): PhotoCraft ORA import/export `v0.7.0`; ORA no-overwrite guard (#3806) and Krita `.kra` import `v0.9.0`. VectorCraft SVG object ids and names survive `v0.2.0`; `data-*` and hidden-object round trip (#522) `v0.8.0`. LightCraft `.lcpreset`, XMP sidecars and `render` `v0.1.0`; "Edit in PhotoCraft" `v0.7.1`; portable mode `v0.8.0`. [43][40]

**Minimum Windows requirements stated anywhere in the repos:**
- **PhotoCraft:** `docs/releasing.md` lists "Windows 10+ x64" and "Windows 10+ x86 (32-bit)" built on `windows-latest`; arm64 MSI and portable also exist (cross-compiled, then installed and its CLI run on a native `windows-11-arm` runner in `windows-arm64.yml`). Static CRT, so no VC++ redistributable. [11][13]
- **VectorCraft:** no minimum is stated in its release table; `docs/windows7.md` says the ordinary Rust MSVC target "requires Windows 10", and an experimental, unsupported, community-maintained Windows 7 x64 build exists (OpenGL instead of wgpu). x64, x86 and arm64 MSI and portable are built. [29]
- **LightCraft:** x64, x86, arm64 MSI and portable; no minimum Windows version is stated. [41]
- **Do not use the x86 (32-bit) builds**: PhotoCraft caps a decode allocation at 2 GiB on 32-bit targets. [6]
- **Signing conflict:** the READMEs say "Installers and executables are code-signed", but PhotoCraft's own `docs/gaps.md` (G17) says "Windows code signing (material not obtained)" and `scorecard.md` DIST-2 says "signing skipped with a warning until the signing material exists". Expect SmartScreen or Smart App Control prompts; the acceptance test checks the file's Digital Signatures tab. [13]
- **GPU backends:** wgpu on DX12 first. PhotoCraft: Windows order Vulkan, DX12, CPU (WARP) with a start marker `gpu-starting.json`, `--safe-gpu`, `WGPU_BACKEND=dx12`; "With auto, Intel adapters on Windows use DX12". VectorCraft: DX12 then OpenGL, **no Vulkan unless `WGPU_BACKEND=vulkan` asks for it** (Intel `igvk64.dll` crash, #806); adapter that crashed at start is skipped next start (`graphics-start.json`). LightCraft: DX12, Vulkan, GL, then glow; `LIGHTCRAFT_GPU_BACKEND=dx12|vulkan|gl|glow|off` or `LIGHTCRAFT_GPU=0`. [14][27][37]
- **The "documented AMD driver crash with a `WGPU_BACKEND` workaround" is FilmCraft's, not these three.** Searching all three repos' docs for AMD/Radeon found only performance rows. Documented vendor-specific problems in our three: Intel (VectorCraft #806 Vulkan, #2243 UHD 605 DX12; PhotoCraft "black line on Intel HD #2426", "Rgba32Float panic #2020") and NVIDIA "Shader Cache Size = Disabled" hangs the window for minutes (LightCraft #374; the doc says PhotoCraft hangs the same way). `WGPU_BACKEND` is documented in all three. [27][37][13]

**Pin recommendation (single tag per app).** Provisional pins as of today are `v0.9.0`, `v0.12.0` and `v0.8.0`, but **do not freeze today**: each `main` is 300 to 600 commits ahead and the post-tag commits include exactly the save-safety and Windows fixes we care about (PhotoCraft: ask before overwriting a file another app changed #6596; refuse to replace a read-only file #6600; keep crash-recovery autosaves out of the roaming profile #5648 on Windows; VectorCraft: Save/Export ask before replacing a file, Windows file-name rules; LightCraft: turn GPU rendering off after GPU loss #1337). **Rule: pin the newest tag that exists on the day the maker passes the five-minute test below, no later than 2026-10-25, record it plus the `SHA256SUMS.txt` hash of the installer in the repo, install the portable zip, switch the Launcher's updater off, and change it only at a deliberate gate.** If no newer tag appears, pin the three tags above and add the save rules in Risks. [43]

### 2. PhotoCraft layered import, feature by feature

**Which parsers.** `crates/psd` is a standalone PSD/PSB reader/writer that keeps unknown blocks and round-trips byte-for-byte (`PsdFile::from_bytes(b)?.to_bytes()? == b`); its README still lists layer effects, type, smart objects, vector masks and adjustment layers as "preserved raw, not yet typed", which is **stale**: `crates/io/src/` (`psd_import.rs`, `adjust_map.rs`, `text_import.rs`, `vector_map.rs`, `smart_map.rs`, `effects_map.rs`, `psd_export.rs`) maps them into the document model, and `docs/file-format-parity.md` states the supported set. [5][2]

**Hand-off format matrix: PhotoCraft** (P = preserved, D = degraded, L = lost; evidence level in the last column)

| Feature | PSD written by ag-psd/psd-tools, read by PhotoCraft | PSD written by PhotoCraft (to agent or another editor) | ORA written by agent, read by PhotoCraft | ORA written by PhotoCraft (to agent or Krita) | Level and proof |
|---|---|---|---|---|---|
| Raster layers, names, positions | P (`luni` name, layer rect) | P | P, including off-canvas; whitespace in names kept (#3207) | P, cropped to their pixels | [T] `crates/io/tests/corpus.rs`; `ora/tests.rs`; `docs/ora.md` |
| Opacity | P | P | P | P | [T] ora tests; `automation/tests/openraster.rs` |
| Fill opacity | P (`iOpa`) | P | n/a | D: folded into pixels | [T] ora tests; [C] docs/ora.md |
| Blend modes | P: 27 modes plus pass-through; unknown keys kept raw | P | P: `svg:*`, `svg:plus`, `krita:*`; Krita Soft Light and Hard Mix open as Photoshop's with a warning | D: `svg:*` where the spec has it else `krita:*`; Xor and Paint.NET Color Burn/Dodge variants saved as Normal | [T] ora tests "every blend mode at 8 and 16 bit"; Krita corpus 32/35 |
| Visibility, locks | P | P | P (`edit-locked`, `alpha-preserve`) | P | [T] |
| Nested groups | P (`lsct`, open/closed, max depth 100) | P | P, pass-through when no blend and not `isolation="isolate"` | P | [T] psd layer-tree tests; ora tests |
| Pixel (raster) masks | P (20/36-byte forms, real mask) | P | not an ORA concept | D: mask applied to the layer's pixels | [T] psd crate tests; [C] docs/ora.md |
| Vector masks and shape layers | P for PhotoCraft-readable (`vmsk`, `vsms`, `vscg`); agent libraries cannot author them easily | P | L | L: rasterised, vector masks left out | [C]; [V] "116 of 116 shape layers match Photoshop's pixels" (README, corpus in a separate repo) |
| Adjustment layers | P for 16 kinds (levl, curv, hue2, brit, nvrt, thrs, post, expA, vibA, blnc, mixr, grdm, phfl, selc, blwh, clrL); other blocks kept as `Unsupported` raw | P | L | L; **and PhotoCraft refuses to overwrite the .ora with less than the document has** (from v0.9.0) | [T] `adjust_map.rs` + `adjust_blend_roundtrip.rs`; `openraster.rs` test |
| Layer styles (`lfx2`) | P (mapped) | P | L | L | [C] file-format-parity.md |
| Type layers | P: `TySh` plus EngineData read as live type, re-rendered by PhotoCraft's own engine; missing font gives a warning and fallback; ag-psd text layers carry no redrawn bitmap | P (`TySh` written; bug #2374 "text layers re-saved would not reopen" closed 2026-10-10) | D: ORA text elements skipped with a warning | D: rasterised | [T] `text_corpus.rs`, `psd_kerning.rs`; Photoshop text oracles in a separate repo |
| Smart objects | P: embedded `SoLd`/`PlLd` open as editable; linked sources are embedded on save | P (`SoLd`+`lnk2`; "Photoshop 2026 opens 8/16-bit exports as live smart objects" is [V]) | L | L: rasterised | [T] `smart_corpus.rs`; [V] Photoshop opening |
| 8/16/32-bit | P (ag-psd cannot write 16-bit; psd-tools can via arrays) | P | P (16-bit PNG) | P (8-bit docs as 8-bit PNGs; 16/32 as 16-bit PNGs) | [T] |
| ICC profile | P (resource 1039) | P | D: only sRGB survives | D | [T] `color.rs`; [C] docs/ora.md |
| Clipping masks | P | P | L | L | [C] |
| Merged image (composite) | read when real; thumbnail oracle otherwise | written real by default (`maximize_compatibility` true in headless export) | not read (renders its own) | `mergedimage.png` and thumbnail written | [C] psd_export.rs; docs/ora.md |
| Round trip back into the pipeline | n/a | PhotoCraft to PhotoCraft: self-consistent; **PhotoCraft to Photoshop/others: untested** (FILE-216-4 "missing") | n/a | Krita re-opened 34 PhotoCraft re-exports; 33 identical | [T] for ORA only |

**What the percentages actually measure** (`crates/io/tests/corpus.rs`, enforced floors) [3][13]:

| Corpus | Files | "Oracle pass" floor (our render equals the file's own merged image) | "Round trip" floor (export then re-import renders the same) |
|---|---|---|---|
| Mixed ag-psd and psd-tools samples (`corpus/psd`) | 170 | 146 | 169 |
| psd-tools test set (`corpus/psd-tools`) | 309 | 236 | 308 |
| Photoshop-authored oracles (`corpus/photoshop`, own repo) | 256 (`gaps.md` says 258) | **145** | 258 (the scorecard prints "258/256", i.e. a floor above the file count: the repo's own numbers are inconsistent) |

- README: "307 of 309 render the same" (the floor in code is 308; the README number has drifted) and "169 of 170": these are the **round-trip** column, a self-consistency check. The fidelity-versus-Photoshop column is 76 percent for psd-tools files and 56 percent for Photoshop-authored files. "Only the standalone `photocraft-psd` crate reproduces every parseable corpus file byte for byte" (`crates/psd/tests/corpus.rs`). The website's "134 of 135 real-world files round-trip byte for byte" has **no counterpart number in the repo** (the corpora are 170 and 309 files): **[V]**, cannot be reproduced from the tag. [1][3][44]
- The vendor's headline readiness: "feature breadth ~76 percent, ready for real work ~45 percent, stage alpha, PSD exchange with Photoshop not yet reliable enough for beta" (`docs/target-app-parity.md`, 2026-10-10). [13]

**Free libraries that can write a PSD from an agent (verified today):**

| Library | Version, date | Writes layered PSD? | Limits | Source |
|---|---|---|---|---|
| ag-psd (JS/TS, MIT) | 31.0.3, 2026-10-07 | Yes: `writePsd`/`writePsdBuffer` from a `children` tree with names, nested groups, opacity, blend mode, masks, text | RGB only; **no 16-bit**; no PSB; text layers carry no redrawn bitmap (Photoshop prompts); does not regenerate composite or layer bitmaps; works in Node without a browser (canvas only needed for image data and thumbnails) | [45][46] |
| psd-tools (Python) | 1.25.0, 2026-10-14 | Yes, "limited": `PSDImage.new(mode, size, depth)`, `create_group`, `create_pixel_layer(pil_image, name, opacity=255)`, `save()`; 16/32-bit via `create_pixel_layer_from_array` | Creating layers from PIL is "experimental"; blend mode not documented on the usage page; type, shape and smart-object editing "not supported"; rendered output "likely different from Photoshop's" | [47][48] |
| pytoshop (Python) | 1.2.1, 2018-11-30 | Writes PSD from scratch (per its summary) | Unmaintained since 2018: do not use | [49] |
| ImageMagick | n/a | PSD is "RW" on its formats page | ORA is **read-only**; XCF read-only; I did not verify multi-layer PSD output behaviour (**[U]**) | [50] |
| Krita | n/a | `krita file.ora --export --export-filename out.png` converts; ORA is its native layered interchange | The manual page does not describe a no-GUI mode or batch flag | [52] |
| GIMP | n/a | ORA and PSD plug-ins exist | A forum report on GIMP 3.0.4 says `.ora` export lost layer transparency and text (GNOME GitLab issue number comes only from a forum reply; **[U]**) | [56] |

**Is OpenRaster fully supported for read and write?** For everything a raster-layer hand-off needs, yes, with the loss list above. The reader takes the archive with a bounded ZIP reader (no ZIP64, CRC-checked), parses `stack.xml` with a 16 MiB cap, canvases up to 300,000 px a side, at most 8,192 layers and groups. Unknown elements or missing layer images open with a warning rather than fail the file. [T][4]

**Decision: the pipeline's layered contract.**
1. **Agent to app: OpenRaster.** Writable with stdlib (fixture `make_ora.py`), third-party-verified, lossless for layers/groups/names/opacity/blend/offset/16-bit.
2. **App to pipeline: whatever the maker saved, read back through `photocraft-cli`**: `info <file> --compact` (layer tree as JSON), `convert <file> out.png`, and per-layer PNG export (`doc.exportLayers` on `serve`, or `file.export.layersToFiles`). If the maker added adjustment layers, type or masks, PhotoCraft will not overwrite the .ora; it offers a PSD of the same name (a safety feature, #3806). Treat that PSD as PhotoCraft-private and take flattened or per-layer PNGs from it.
3. **`.pcraft` is never an interchange format.** It is a zip of `manifest.json` plus content-addressed zstd tiles (`tiles/<blake3>.zst`); the manifest is "versioned" but not field-documented; an agent cannot sensibly write it. It is the maker's autosave and working format. [6]
4. **PSD from ag-psd/psd-tools is a fallback input** when a feature ORA lacks is needed (text, adjustment layers). Keep it 8-bit RGB for ag-psd; supply a composite; expect Photoshop-style text to be re-rendered.

### 3. Can `photocraft-cli` build and save a layered document headless?

Yes, **[C]** for the exact sequence, **[T]** for its parts (`crates/automation/tests/openraster.rs` and `agent_tasks.rs` drive `doc.new`, `layer.new.layer`, `layer.setProps` with `{name, opacity, blend}`, `layer.newAdjustmentLayer.curves`, `doc.save` to `.ora` then reopen). [10]

- **Subcommands:** `convert`, `info`, `run`, `batch`, `droplet`, `commands`, `mcp`, `serve`. `photocraft-cli commands --json --filter layer.` lists the registry (the README says 500+ commands; my static grep recovered only about 250 ids because the registry is built with several macro styles, so use `commands --json` on the installed build as the authority). [7]
- **Relevant commands** (ids from `crates/engine/src/{commands,file_cmds,layer_multi_cmds}.rs`): `file.new {width,height,mode,depth:8|16|32,background:"transparent"|...,resolution,name}`; `file.placeEmbedded {path, scale (percent), fit, center:[x,y], smartObject:false}` (plain pixel layer named after the file stem; the default makes a smart object and "fits" large images, so pass `fit:false` or `scale:100`); `file.scripts.loadFilesIntoStack {paths|folder}` (one pixel layer per file, first file at the bottom); `layer.setProps {layer?, name, visible, opacity 0..1, fill 0..1, blend, clipped, locks}`; `layer.renameLayer`; `layer.new.layer {name, mode, opacity}`; `layer.groupLayers {name}` (acts on selected layers, so `select.allLayers` first); `layer.moveTo {layers, target, position}`; `layer.newAdjustmentLayer.{curves,levels,hueSaturation,vibrance,colorBalance,...}` (README example: `{"points":[[0,0],[64,48],[192,212],[255,255]]}`); `file.save`/`file.saveACopy`; `file.export.layersToFiles {dir, format}`. [9]
- **`run` shape:** `photocraft-cli run (<file> | --new <json>) --cmd <id> [--params <json>] ... [--out <file>] [--format ext] [--quality 1-100] [--tiff-layers]`. `--out` saves by extension: `.psd`, `.psb`, `.ora`, `.pcraft`, `.png`, `.tif`... The CLI is "trusted local": ambient file paths allowed. Output of each command is one JSON line. [7]
- **`batch --actions` shape:** applies an action list to every image in `--in` and writes to `--out` (refused when `--out` is the input folder unless `--in-place`). Steps are `[id, params]` pairs, `{"command": id, "params": {...}}` objects or bare ids, as a list or wrapped in `{"actions": [...]}`, `{"steps": [...]}`, a droplet, a recorded Actions-panel set (`--action <name>`), or a Photoshop `.atn` file. It processes **flat images**, not layered builds; `--format psd` writes a one-layer PSD. [7]
- **For many edits without shell quoting (Windows):** `photocraft-cli serve --automation-read-root DIR --automation-write-root DIR` reads JSON lines on stdin: methods `doc.new`, `doc.open`, `doc.place` (passes `smartObject`, `fit`, `scale`, `center` through; returns `{layer, scale, bounds}`), `engine.execute {command, params}`, `doc.save {path, format?, tiffLayers?}`, `doc.exportLayers`, `doc.inspect`, `doc.render`, `batch {steps, stopOnError}` (at most 256 steps). Filesystem access fails closed unless roots are given. The roots env vars work only for the desktop app, not for headless CLI modes. [8][10]
- **Needs a GPU?** No. `Cargo.toml` of `photocraft-cli`, `photocraft-engine`, `photocraft-automation`, `photocraft-io` and `photocraft-compose` contain no wgpu or `photocraft-gpu` dependency (searched); the control docs describe `serve` as "no window, no GPU". Previews are capped (longest edge 2048 px, 5 MiB PNG) unless `maxSide: 0` on a trusted-local session. [8]
- **Does the Windows MSI ship `photocraft-cli.exe`? Yes.** `packaging/windows/photocraft.wxs` has `<Component Id="PhotocraftCli"> <File Source="$(var.BinDir)\photocraft-cli.exe">`; `package.ps1` builds `-p photocraft -p photocraft-cli`, checks the PE header (CLI subsystem 3 = console), copies both exes into the portable zip and smoke-tests `photocraft-cli --version`. Default folder `Program Files\PhotoCraft` (remembered for upgrades). The website lists the CLI only as a macOS zip, which is misleading. [11][44]
- **MCP:** `photocraft-cli mcp [--bridge 127.0.0.1:PORT --control-token-file PATH] --automation-read-root DIR --automation-write-root DIR`; tools `command_list`, `command_run`, `command_batch`, `doc_inspect`, `render_preview`, `doc_new`, `doc_open`, `doc_place`, `doc_save`, `ui_screenshot`... Headless or bridged to the running app. [8]

### 4. VectorCraft SVG fidelity

**Hand-off format matrix: VectorCraft** (SVG authored by an agent, imported, edited, exported). Import = `crates/svg/src/import.rs` over `usvg` 0.45/0.48 (a normalized tree; **all transforms are baked into geometry**); export = VectorCraft's own writer (`export.rs`), SVG 1.1 or Tiny 1.2. [19][20][21]

| Construct | Import | Export | Does the animator's hook survive? | Level and proof |
|---|---|---|---|---|
| `id` on shapes and groups | Becomes the object **name**: from `data-name`, `inkscape:label`, `serif:id`, `aria-label` if present, else the id | Id regenerated from the name by `sanitize_id`: keeps letters, digits, `-`, `_`, `.`; everything else becomes `_`; a leading non-letter gets `_`; duplicates become `name-2`. `data-name` carries the exact name when the id had to differ | **Yes** for clean ids (`sun`, `arm-raised` survive verbatim). **No** if the maker picks Object IDs = "Minimal" (only referenced ids written) | [T] `tests/ids.rs`, `symbols_layers.rs` (v0.2.0+) |
| `class` attribute | **Not kept** (used only to resolve the CSS cascade) | `Styling = Internal CSS` writes global `class="cls-N"` + one `<style>`; other stylings write none | **No** | [T] `tests/options.rs`, `import_details.rs`; grep: no class retention in import |
| `<style>` element | Parsed for cascade (type, `#id`, `.class`, attribute, descendant, child selectors for text; usvg for shapes), then baked into appearances | Regenerated only as `cls-N` rules (and `@font-face` if fonts embedded) | **No** (re-add after touch-up) | [T] `import_text.rs`; [C] lib.rs |
| `<g>` nesting | Top-level `<g id>` become **layers** only if all top-level children are such groups; nested `<g id>` stay groups named by id; plain unnamed groups carrying nothing are not guaranteed | Groups written as `<g id=...>`; sublayers marked `data-vc-layer` | **Yes** for named groups | [T] `symbols_layers.rs::marked_groups_are_sublayers_only_in_layers`, `roundtrip.rs::groups_and_names_roundtrip`; anonymous groups **[U]** |
| `transform` on `<g>`/shapes | Baked into child geometry; group keeps its name | Written as coordinates (no `transform` attribute on baked groups) | **Pivot semantics lost** unless stored in `data-pivot` | [T] `roundtrip.rs::import_transforms_and_nested_groups` |
| `data-*` attributes | Kept on `g, a, use, path, rect, circle, ellipse, line, polyline, polygon, image`; max 64 each; **not** on `text`, `tspan`, root `svg` | Written back as `data-*` (invalid names dropped with a warning; duplicate keys written once) | **Yes** (v0.8.0+) | [T] `symbols_layers.rs::hidden_objects_and_data_attributes_round_trip` (an "animation rig") |
| Hidden objects (`display:none`) | Kept as hidden objects/layers | **Dropped by a plain Export**; kept (written `display="none"`) with Save or `hiddenLayers: true` (the CLI `convert` sets it) | Only if saved, not exported | [T] same test |
| Gradients and `gradientTransform` | usvg resolves units and transform; `spreadMethod` reflect/repeat expanded to at most 64 periods; focal radius ignored with a warning | `<defs>` with `userSpaceOnUse`; linear as x1,y1,x2,y2; radial uses `gradientTransform` for ellipses; identical gradients share one def named after the swatch; ids regenerated | Gradient **ids not stable** (do not target them) | [T] `gradients.rs`, `roundtrip.rs::import_gradient_with_transform` |
| `<clipPath>` | Clip groups (nested clipPaths are clip groups in clip groups); text in a clip path ignored | `<clipPath>`; inside/outside strokes become clip/mask constructs that re-import as groups | Yes; Group structure may gain wrapper groups | [T] `roundtrip.rs::clip_group_roundtrip`; [C] lib.rs |
| `<mask>` | Luminance **opacity mask**; own exports keep options via `data-vectorcraft-mask` | `<mask maskUnits="userSpaceOnUse" color-interpolation="sRGB">` | Yes (appearance); mask ids regenerated | [T] `mask_options.rs`; [C] |
| `<text>` | Read from XML as **live text** (no font database): tspans, `textPath` (`startOffset`, `side`), per-character x/y/dx/dy/rotate, spacing; approximations: later lines start at the first line's x, absolute positions inside textPath ignored, vertical text sets glyphs sideways | `<text>/<tspan>` by default (document setting `exportText: editable`); `outlineText` turns it into paths; fonts embedded as `@font-face` only with `embedFonts` | `id` on `<text>` survives; **no `data-*` on text** | [T] `import_text.rs`, `text_layout.rs`, `text_stroke.rs` |
| `<symbol>` + `<use>` | Symbol and instances; a `<use>` that shows the symbol differently, or any `<use>` of a non-symbol, becomes plain art (the link is lost) | One `<symbol>` per symbol and a `<use>` per instance, except stained/scaled-with-effects instances written as art | Instances yes; plain-art `use` ids may stay but are no longer references | [T] `symbols_layers.rs` |
| Filters | Only a Gaussian blur, drop shadow (incl. `feDropShadow` and the usual chains), glow or feather become live effects; **every other filter is ignored and reported as a warning** | Live raster effects written as SVG filters | `feColorMatrix`, `feTurbulence`, `feDisplacementMap` etc.: **lost** | [C] lib.rs docs; test coverage `effects_export.rs` for what is exported |
| `viewBox`, width/height, units | `viewBox` sets the artboard; absolute root units (mm, cm, in, pt) keep physical size (72 pt per inch); 1 CSS px = 1 pt | **Always `viewBox="0 0 W H"`** (origin re-based, content translated); `width`/`height` omitted only with `responsive` | **Coordinates shift** if the original `viewBox` origin is not 0,0 | [T] `import_units.rs`; export.rs line 117 |
| SMIL (`<animate>`), CSS `@keyframes`, `<script>`, `<foreignObject>` | No handling found (grep: none); usvg drops them | Not written | **Lost**: animate after the touch-up | [C]/[U] (negative evidence from grep) |
| `<pattern>`, `<image>`, `<a href>` | Pattern swatch; raster images stay linked or embedded (external SVGs become art without text); `<a href>` becomes an object URL | Back out | Yes | [C] lib.rs |
| Editing round trip | `preserveEditing` (SVG option, default **false**) embeds the whole native document in `<metadata>` (namespace `urn:vectorcraft:editing`) | `.ai` always embeds; SVG only when asked | Leave it **off** for pipeline SVGs (it bloats the file and carries a second copy of the art) | [C] svg.rs options |

**What this means for the animator:** ids and `data-*` are the stable hooks; classes, `<style>`, gradient ids, transforms and any animation are not. "Property-tested file round trips" (README) means own-export-then-own-import with a perceptual render comparison on documents VectorCraft generates (`prop_svg.rs`, `prop_format.rs`); the vendor itself writes "There is no real-world Illustrator corpus" and "no field record and no real-world file corpus yet" (`docs/file-format-parity.md`, `docs/target-app-parity.md`). The 88 percent figure is "menu items, tools, effects and formats **exist**" (353 of 375 menu items wired, 94.1 percent), not behaviour. [T][V][30]

**The `.vectorcraft` JSON format.** Documented only in the module comment of `crates/format/src/lib.rs`: UTF-8 JSON (optionally gzip), `{format:"vectorcraft", version:4, generator, preview, profiles, pdf, document:{...}, images}`; v4 may put large blobs after the JSON behind a `\n\0VCBLOBS\0` marker; unknown keys are kept (`Document::extra`); newer-version files are rejected. The `document` object is a verbose serde dump of the internal model (the 134 KB `examples/dusk-poster.vectorcraft` for a one-poster scene). **An agent could write it, but should not**: no field-level schema exists beyond the examples and Rust types, and every node carries ids and appearance structure that SVG import generates for free. Generate SVG (or call the command API), let VectorCraft make the `.vectorcraft`. Use `vectorcraft-cli convert in.svg out.vectorcraft` if a native file is wanted. [23]

### 5. VectorCraft tracing, batch and MCP

- **Image Trace presets (code, `crates/trace/src/lib.rs::preset`):** the tree has **15** built-in names, not 12: Default, Auto Color, High Fidelity Photo (64 colours, Paths 90, Corners 25, Noise 4, overlapping), Low Fidelity Photo (20 colours), 3 Colors, 6 Colors, 16 Colors, Shades of Gray (8 greys), Black and White Logo (threshold 128, paths 95, corners 80, snap curves to lines), Sketched Art (threshold 150, noise 100), Silhouettes (threshold 200), Line Art, Technical Drawing (paths 95, corners 90, snap), Outline (stroked centre lines), Flat Logo (own logo mode, colours found automatically, sub-pixel edges). Each is a `TraceParams` set (mode, colours, paths 0-100, corners 0-100, noise, method abutting/overlapping, threshold, strokes/fills). `enhanced_preset` adds Auto Grouping and Shapes. Commands: `imageTrace.make`, `imageTrace.makeAndExpand`, `imageTrace.presets`, `imageTrace.expand`. Quality is tracked by an in-repo harness ("Nothing here is a judgement by eye"); there are no comparisons with other products. For our project: useful for tracing a **scanned drawing, handwriting or a letter's stationery** into SVG; not for photos. [C][28]
- **Batch:** `vectorcraft-cli run [--in FILE] [--cmd ID [--params JSON]]... [--export FILE]... [--scale N]` exports each file in the format its extension picks. Writable formats (from `FORMATS` where `write` is true): SVG, SVGZ, PDF, EPS, DXF, EMF, WMF, PNG, PNG-8, JPEG, WebP, GIF, TIFF, BMP, TGA, PSD, `.ai` (PDF-compatible or legacy v7), TXT, `.vectorcraft`. So PNG, SVG and PDF in one call: `vectorcraft-cli run --in art.svg --export art.png --export art.pdf --export art.touched.svg --scale 2`. `convert IN OUT` adds `--outline-text`, `--decimals`, `--artboard/--range`, `--hidden-objects`, prints `importWarnings` (what reading IN left out) and refuses to overwrite its input when the read was lossy unless `--replace-lossy`. `$N.path` references let a later step use an earlier result. On Windows the CLI installs DirectWrite system fonts at start, so PNG/PDF export finds installed fonts. [C][24][31]
- **Needs a GPU?** No: `vectorcraft-cli`/engine/mcp have no wgpu or egui dependency, and the canvas is rasterised on the CPU (`vello_cpu`); the GPU only composites the UI. [27]
- **MCP (`crates/mcp`) for a human-in-the-loop session:** `vectorcraft-cli mcp --connect 127.0.0.1:7979` (the app started as `vectorcraft --control 7979`) forwards every call so the maker watches the artwork change; `--headless` runs an in-process engine. Tools: `command_list/run/batch`, `doc_inspect`, `render_preview`, `ui_inspect`, `ui_screenshot`, `draw_path`, `draw_shape`, `set_paint`, `add_text`, `apply_effect`, `pathfinder`, `transform`, `pointer_gesture`, `press_key`, `open_panel`, `screenshot`, `open_file`, `save_file`, `export`; resources `vectorcraft://document`, `.../document/json`, `.../object/{id}`; prompts `poster`, `icon-set`, `recolor`, `trace-and-style`, `export-set`. `--automation-read-root/--automation-write-root` confine file access. UI-only tools (`inspect_ui`, `type_text`, `open_panel`, window screenshots) need the live app. [25]

### 6. LightCraft for scans

- **Does the develop pipeline treat TIFF/JPEG like raw?** The same pipeline: `crates/pipeline/src/lib.rs` states stage order geometry, scene-linear (white balance, exposure, dehaze, local tone, texture, clarity, masks), filmic tone map, colour (vibrance, saturation, mixer, grading, B&W in OkLCh), display (gamut map, parametric and point curves, vignette, grain). Input is scene-referred linear Rec.2020; JPEG/TIFF are decoded (input ICC handled by moxcms) into that space with `SourceInfo.raw = false`. Differences for scans: white balance is a **relative** scale (6500 / 0 = as shot, shown as -100..+100) instead of Kelvin; no camera matrices/profiles, camera tone curve, DNG lens opcodes or raw-only denoise; Auto "changes [a rendered source's] exposure less". [T] `unedited_rendered_source_is_passthrough` (sRGB ramp renders back within 3/255) and a process-version test over rendered sources at 8 and 16-bit. **[U]** no faded-print or scanner corpus. [35]
- **TIFF:** import 8/16-bit (and 16 to 64-bit float, bilevel, CCITT); export TIFF 8/16-bit and 32-bit float, none/LZW/ZIP. [35]
- **Can an agent author a preset?** Yes. `.lcpreset` JSON: `{"format":"lightcraft.preset","version":1,"presets":[{id,name,group,settings}]}` where `settings` is a **partial** develop-settings object (only the groups it sets; e.g. the shipped Faded Matte is `{"curve":{"shadows":40,"highlights":-15},"light":{"contrast":-10},"color":{"saturation":-12},"grain":{...}}`). Also accepted by `preset.import`: XMP presets (`crs:` mapped, approximate), `.lrtemplate`, Luminar `.lmp`, zip bundles. A sample is in `craft-visual-fixtures/faded-print-a.lcpreset`. [33][42]
- **XMP `crs:`:** LightCraft **reads** ~60 process-2012 `crs:` fields (Exposure2012 ... crop, local masks, spots) and "never writes them"; "values carry over but the look is approximate"; `AlreadyApplied="True"` packets are skipped; its own exact settings go in `lc:settings` (JSON) and `lc:` flags, preferred over `crs:` on read. An existing sidecar is merged into, never replaced; an unreadable sidecar is copied to `.xmp.bak-<date>` first. [33]
- **Batch via CLI:** `lightcraft-cli run [--library DIR] [--import PATH]... COMMAND [key=value]... [COMMAND ...]` (one JSON line per command; non-zero exit on failure; `--script FILE|-` takes JSON lines; `--keep-going`). `render <in> -o <out> [--set control=value]... [--settings FILE.json] [--preset ID] [--size N] [--quality Q] [--opt KEY=VALUE]` develops one file (outputs .jpg .png .tif .webp .avif .jxl .psd .dng). Commands for a folder: `library.import {paths, mode: add|copy|move}` (**`add` references files in place; `move` deletes the source after verification: never use it on scans**), `library.selectAll`, `preset.import {paths}`, `preset.apply {id, amount 0..200, ids?}`, `develop.set {control, value}`, `develop.merge {settings}`, `develop.auto`, `develop.wb`, `develop.wbPick {x,y}` (normalised neutral point), `develop.sync`, `app.export {dir, ids, format, quality, naming, startNumber, subfolder, conflict: unique|overwrite|skip, longEdge, shortEdge, percent, ppi, colorSpace, bitDepth, metadata, watermark, sharpen}`. **Naming templates** (same tokens as batch rename): `{name}`, `{seq}` (3 digits) / `{seq:N}`, `{date:%Y-%m-%d}`, `{title}`, `{ext}`. [T] `export.rs` tests `naming_uses_the_rename_tokens`. [34][42]
- **Crash-safe op-log library, and external or shared drives:** `catalog.snap` (atomic temp+fsync+rename) plus `catalog.log` (JSON lines `{"seq","crc","op"}`, **fsynced before append returns**); a torn final record is dropped and the file cut back; a failed append (disk full, "a dropped network share") is cut back to the last whole record before the retry; a bad record **followed by good ones** is real damage: replay stops, the log is kept as `catalog.log.damaged-<seq>`, and a fresh snapshot is written. One process per library by `LockFileEx`/`flock` on `catalog.lock`; the lock is released by the OS on a crash. **File systems without lock support (some network shares): the library opens unlocked with a warning**, and SMB/NFS locks are advisory: "two computers on a shared folder" can silently drop each other's edits. Recommendation: keep the library on a **local NTFS** disk, keep the **scans** wherever they live (the library only references them with `add`), back up the library folder. [T] `tests_journal.rs`, `tests_torn_append.rs`, `tests_lock.rs`, `tests_repair.rs`. [36]
- **Comparison for ~300 faded prints on a modest Windows PC:**

| | LightCraft 0.8.0 | darktable (`darktable-cli`) | RawTherapee (`rawtherapee-cli`) | ImageMagick (`magick`/`mogrify`) |
|---|---|---|---|---|
| Non-raw TIFF/JPEG input | Yes, same pipeline | Yes: JPEG, 8/16-bit PNG and TIFF, float TIFF, EXR [54]; which modules apply to non-raw is not stated on that page | Man page says it processes non-raw photos; no explicit CLI example seen [55] | Yes |
| Agent-authorable look | `.lcpreset` JSON, `--settings` JSON, `--set control=value` | XMP sidecar with `--style`, needs a config dir and `data.db` for styles [53] | `.pp3` profile(s), several `-p` allowed, applied in order, partial profiles fine [55] | Operators only: `-auto-level`, `-auto-gamma`, `-contrast-stretch` (per-channel with `-channel`), `-color-matrix`, `-clut` [51] |
| Per-print eyeball tweak | In-app UI on the same catalog; `develop.wbPick` | Mature GUI | Mature GUI | None |
| Colour management of scanner profiles | ICC input (moxcms), 16-bit TIFF out, `colorSpace` option | Mature | Mature | Manual |
| Windows maturity | **Unverified** (gaps #27: Windows installer UI and DX12 unverified; GPU proven on Apple and one AMD GPU on Linux) | Mature | Mature | Mature |
| Weight on a modest PC | Pure Rust, memory budget default min(25 percent of RAM, 1.5 GiB), `LIGHTCRAFT_MEMORY_MB` overrides; M4 Pro measurement 0.83-0.99 GB peak RSS (14 raws) | Heavier install and database | Moderate | Light |

  **Recommended single path:** LightCraft, run on the maker's PC by a script Claude writes, as: create library; import prints with `mode: add`; apply one `.lcpreset` per batch of similarly faded prints (cluster by film stock/year); per print, `develop.wbPick` on a neutral patch (the unprinted paper border works if the scanner crop leaves it) or a manual pick in the GUI; export 16-bit TIFF masters (`format: tif, bitDepth: 16, colorSpace: srgb`) and JPEGs with `naming: "{date:%Y}-{seq:3}"`. **Gate:** a 10-print pilot processed the same way in darktable; choose by eye and by the measured mean RGB of the paper border. Fallbacks: darktable (XMP/style) then an ImageMagick `-channel RGB -auto-level` pre-pass. Run with `LIGHTCRAFT_GPU=0` for deterministic, driver-independent output (the CPU and GPU paths agree within 1/255, but DX12 is unverified on Windows). [37]

### 7. Stability and performance

**PhotoCraft** (most plumbing, most evidence):
- Autosave: **yes**. `autosave: true`, `autosave_minutes: 10`, `recover_on_launch: true` by default; `crates/format/src/autosave.rs` writes snapshots to a Recovery folder (`%APPDATA%\Photocraft\Recovery`, or `PhotoCraftData\` beside the exe in portable mode) on a background thread; an entry is deleted only when the document is saved or closed. Windows autosaves used to go to the roaming profile (fixed on `main` after the tag, #5648). **No autosave or crash recovery in the web build** ("save/download before closing or reloading"). [C][11][12][15]
- Atomic saves: `atomic_write` (same-directory temp, `sync_all`, rename; seven Windows `PermissionDenied` retries from 10 ms; original untouched on any failure; failure-injection tests, BUG-203-x) [T]. Panic net: command dispatch and import/export catch panics and keep the document unchanged [T]. "Never-crash" lints on 28 of 28 crate roots plus a `panic_hunt` test that runs every command with adversarial parameters [T]. [13]
- GPU: start marker, device-loss to CPU compositor, `--safe-gpu`. Known: NVIDIA Shader Cache Size Disabled hang; "Intel HD black line"; PSB larger than 4 GB fails on Windows (#375). [14][13]
- **Memory:** default "Memory Usage" budget in preferences is **8192 MB** for document plus History, then scratch-disk spill (`ScratchDisks` default: system temp). Vendor baseline (macOS, Apple M4 Pro 48 GB, 2026-10-05): opening a 20 MP layered PSD 1.75 s, **2.2 GB peak RSS and 1.9 GB GPU**; pasting a 12 MP layer 1.3 GB. Nearly every interactive scenario is "over budget (target not met yet)". On an 8 GB PC lower the Memory Usage preference and keep working canvases around 8.6 MP (3600x2400) rather than 20 MP. **[U]** no Windows or low-RAM measurement exists. [13][15]
- Windows CI: `ci.yml` runs the suite on `ubuntu-latest` and `windows-latest` (macOS only in `release.yml`). [17]

**VectorCraft:**
- **What "never crashes" guarantees** (`docs/development.md#robustness`): shipped code contains no `unwrap`/`expect`/`panic!`/`unreachable!`/`todo!` (clippy lints denied workspace-wide); implicit panics (indexing, division by zero, unbounded work) are to be avoided by convention; a `guard::catch_panic` wraps `Session::execute`, tool events, the MCP server and each control request and **restores the previous document state**; property and fuzz tests (`import_fuzz.rs`, `command_sweep.rs`, `prop_format.rs`, `protocol_props.rs`) check garbage SVG/PDF/`.vectorcraft`/MCP never panic. It does **not** cover GPU driver crashes, out-of-memory, or wasm: "On wasm a panic aborts the app, so the web build has no net at all." [T][27]
- Recovery: Data Recovery copies every `autosaveInterval` minutes (skipping documents over 20,000 objects while `recoveryOffForComplex`); copies persist after a crash; per-app areas with a `.lock` file; web uses `localStorage` with Web Locks. `.vectorcraft` saves are atomic. [C][25]
- GPU resilience: adapter ordering, restart on another adapter if the window fails or the first frame is not shown in 20 s, `graphics-start.json` crash marker. [27]
- The vendor's own table: "Robustness: good, new... Missing: a corpus of real-world files, **Windows/Linux/browser QA**"; "Performance: unverified". No workflow in `.github/workflows` at the tag runs the full suite: only `affinity-corpus.yml` (Ubuntu), `print.yml` (`cargo test -p vectorcraft` on windows-2022 for printing-path changes), a weekly Windows 7 compile check, release/packaging jobs and a Windows-ARM64 install smoke test. Contributors outside the team are fixing Windows bugs on `main` (file-name rules, print settings). [30][43]
- Memory: no figure stated; `vectorcraft-cli perf --deep` prints the working set on Windows. **[U]**

**LightCraft:**
- Catalog durability as above (best-in-class of the three, with tests). Exports are written atomically and "protect originals and XMP sidecars". [T][36]
- Reliability notes in `whats-new.md` (2026-10-13/14): zip-bomb refusal for presets, damaged-catalog repair on open (what was repaired goes to the log), crop-of-no-size crashes fixed. [40]
- GPU: window renderer probed DX12, Vulkan, GL, glow in error scopes; marker `window-init.marker` with automatic relaunch (at most 4); compute falls back to CPU per render. Known: NVIDIA shader-cache hang (#374). `gaps.md` #27: "Windows installer UI unverified on Windows (#79); GPU path proven on Apple and on one AMD GPU on Linux (Radeon 8060S, Vulkan); NVIDIA, Intel and DX12 unverified". One Windows datum: Radeon 780M iGPU, DX12, full-size export of a 24 MP raw with heavy edits 3.7 s to 1.9 s after a kernel fix. No workflow in the tree runs the test suite (release, packaging, FreeBSD and Windows-ARM64 install-smoke jobs only). [37][40]
- Memory: budget default min(25 percent of RAM, 1.5 GiB), `LIGHTCRAFT_MEMORY_MB`; peak RSS 0.83-0.99 GB (M4 Pro, 14 raws). The web build keeps a thumbnail cache of 2 GB. [37][38]

**Issue trackers: unreachable.** `github.com/.../issues` and `/releases` returned 403; `gh api` said the repository is not attached; `add_repo` (read) answered that git reads are already served anonymously and API access needs a push-attach, which I did not request. **I cannot say how many open crash or data-loss issues exist.** The vendor-internal documents quote issue numbers (PhotoCraft: #1281 Photoshop 26.6 cannot reopen our files, #2469 "PSD not opening in Photoshop", #2374 text-layer PSD would not reopen (closed 2026-10-10), #1764 PSB smart object blank; VectorCraft: #806, #2243; LightCraft: #374, #1196 build OOM); I did not see the issues themselves. [13][27][37]

### 8. Web builds

| | PhotoCraft web | VectorCraft web | LightCraft web |
|---|---|---|---|
| Zip contents | `photocraft-web-<ver>.zip` holds `photocraft-web-<ver>/`: `index.html`, `photocraft-web-<hash>.js` (~170 KB glue), `photocraft-web-<hash>_bg.wasm` (24,167,186 bytes = 23.0 MiB raw, 10.5 MiB gzip), `_headers`, `.htaccess`, `HOSTING.md`, optional `fonts/` + `fonts/manifest.txt` [12] | `index.html`, JS glue, `_bg.wasm` (~13 MB, ~5 MB compressed; release 17.5 MB / 7.1 MB gzip per development.md), `_headers`, `HOSTING.md`, optional Arabic fonts (~8 MB) [29] | `index.html`, `worker.js`, `lightcraft_web.js`, `lightcraft_web_bg.wasm` (13.5 MB, brotli 3.1 MB), `.gz/.br` copies [38] |
| MIME and headers | `.wasm` as `application/wasm` (else slow or fails), `.js` as `text/javascript`; fonts `font/ttf`/`font/otf`; **no COOP/COEP needed** ("doesn't use SharedArrayBuffer"); if the host sends COEP `require-corp`, add CORP `same-origin` | same | `application/wasm`; COOP/COEP/CORP sent by `cargo xtask web --serve` but **optional today** (needed only for a future wasm-threads build); cannot run from `file://` (module workers + OPFS) |
| Renderer | WebGPU if the page is a secure context (https or localhost), else WebGL2; `?webgl` forces WebGL2; **`?cpu` forces the CPU canvas path** (`web.rs`: `q.contains("cpu")`) [C] | WebGPU else WebGL2; `?webgl` in code; **README documents `?cpu` but `web.rs` and `main.rs` read only `?webgl` and `?lang=`**, so `?cpu` is doc-only here [C] | WebGL2 only (eframe glow), rendering in up to four Web Workers |
| Headless Chromium without WebGPU | Should reach WebGL2 or `?cpu` [U]; vendor tested only with real GPUs; "A browser with neither gets a message" | Same [U]; the vendor's own smoke test used headless Chrome on macOS with `--enable-unsafe-webgpu` | WebGL2 via a software GL (SwiftShader) is plausible [U]; the vendor's `?bench` runs "in a worker, headless Chrome" |
| How files get in | `rfd` file picker (an `<input type=file>`; Playwright `setInputFiles`) and drag-and-drop; Save/Export are browser downloads; preferences in `localStorage`; **no autosave, no TCP control** | Open via async file dialog, drag-drop with drop position; Save as Blob download; Data Recovery in `localStorage`; no control server ("drive headless Chrome with `--remote-debugging-port`") | File > Import Photos or drop; library in OPFS (IndexedDB fallback) with the same journal; export downloads; **`globalThis.lightcraft.command(id, json)`** runs any engine command and returns JSON text |
| Verdict | UI screenshots only | UI screenshots only | Useful for UI checks; still the CLI is better |

**Verdict.** A Playwright session can show an agent what the UI looks like (menus, panel layout) but adds nothing the CLI/MCP route does not do better: the CLI/MCP runs the same engine headless on the maker's actual files, returns JSON and PNG previews, and needs no GPU or browser. Two better UI-learning aids exist: PhotoCraft's README images were "rendered offscreen through its control channel" (`ui.screenshot`, desktop only), and `lightcraft-cli snapshot` "runs the full app UI headlessly (no window, no GPU: CPU-rasterized egui) and writes PNGs". Use the web builds only if the Linux desktop builds cannot start in the container; do that in the week-1 spike, not now. [8][12][34][38]

### 9. Privacy audit

Method: searched each tree for HTTP client crates (`Cargo.lock` + `Cargo.toml`), `http(s)://` literals in non-test Rust, `TcpListener`, update checks, "telemetry/analytics", and the hosted-studio domain.

| | PhotoCraft v0.9.0 | VectorCraft v0.12.0 | LightCraft v0.8.0 |
|---|---|---|---|
| HTTP client at runtime | **None.** `reqwest/hyper/quinn/rustls` appear in `Cargo.lock` only via `winprint` (Windows printing, git dependency of `craft-print`), where they are `[build-dependencies]` (a PDFium downloader behind a `pdfium` default feature that the craft-print dependency switches off) [C][16] | **None** (no reqwest/ureq/hyper in the lock); `open` and `webbrowser` crates open links in the default browser | **Own HTTPS client** `crates/fetch` (rustls + RustCrypto, size cap, SHA-256 pin, mirrors, `.part` files). Called for: SAM 3 mask weights (mirror list empty by default; user-configured `LIGHTCRAFT_SAM3_MIRRORS`), AI Denoise model (`github.com/darktable-org/darktable-ai/releases/...rawdenoise-nind.dtmodel`), face-recognition model (`huggingface.co/fal/AuraFace-v1`), and GeoNames place names (`download.geonames.org`, https or loopback only). I found no startup or periodic call; each is behind an explicit command or dialog ("only when the user asked for it"); **I did not trace every call path** [C][39] |
| Update check | None ("No update check in crates", DIST-220-1 missing). AppImage self-updates through AppImageUpdate (Linux) | None found | None ("Check for updates" row unchecked in parity checklist) |
| Telemetry or analytics | None found | None found | None found; README: "No account, no cloud, no telemetry, no subscription" |
| Remote features | Print to CUPS/IPP (local) | Print via `http://localhost:631` (CUPS) | **`lightcraft-cli denoise-serve`** (plain TCP, token env var, default `127.0.0.1:7990`) and `LIGHTCRAFT_DENOISE_URL` send photo tiles to another computer if you configure it; off by default [C] |
| Control channel / MCP bridge | `photocraft --control PORT`: loopback only (server refuses non-loopback), **first frame must be a 64-hex bearer token** (token file auto-created; on Windows protect with an ACL), 16 connections, 30 s timeouts; MCP bridge accepts loopback addresses only; roots fail closed | `vectorcraft --control PORT` loopback only, **"The port has no authentication, so only enable it while you use it"**; HTTP smuggling blocked because each line must be JSON; `--automation-*-root` confine files | `lightcraft --control PORT` loopback only, **"The port has no authentication"** |
| Links to the hosted ArtCraft studio (`app.getartcraft.com`) | None in source; Help menu opens `getartcraft.com/apps/photocraft`, Discord and GitHub in the browser | Same pattern | Same; plus a map link `openstreetmap.org/?mlat=..` opened in the browser from a photo's GPS |
| Verdict on "no telemetry" | **Confirmed from code (negative search)** | **Confirmed from code (negative search)** | **Confirmed for telemetry**; outbound traffic exists only for opt-in downloads and optional remote denoise |

Caveats: "confirmed" means I found no code path, from static search; dependencies (git deps `craft-libs`, `winprint.rs`) were read for the print stack only; I did not run network captures. The Launcher (`storytold/craft-launcher`) polls GitHub releases and is out of this track's scope but must be off in production. [39][16]

---

## Recipes / templates

All paths below assume a project folder `C:\lj\` on the maker's PC. **Rule: real family photos never leave the maker's PC for these steps.** The container makes and tests the recipes with synthetic files; Claude writes the scripts; the maker (or a script on the maker's PC) runs them on the real material.

### Recipe PhotoCraft: layered raster touch-up

1. **Claude generates:** `C:\lj\ch01\in\ch01_scene.ora` (OpenRaster). Layer order top-first in `stack.xml`; layer names are the pipeline's stable ids (`L10_sky`, `L20_figure`, `L30_texture`); opacity and `composite-op="svg:multiply"` etc. set as intended; 8-bit sRGB PNG layers at canvas resolution or smaller with `x`,`y` offsets. Generator: `research/craft-visual-fixtures/make_ora.py` (stdlib only). If a real PSD is needed use ag-psd 31.0.3 (RGB 8-bit, supply the composite) or psd-tools 1.25.0 (`PSDImage.new`, `create_group`, `create_pixel_layer`).
   - Or assemble headless (Windows PowerShell, no shell-quoting trouble because JSON goes through stdin):
     ```powershell
     $cli = "C:\Program Files\PhotoCraft\photocraft-cli.exe"
     @'
     {"id":1,"method":"doc.new","params":{"width":3600,"height":2400,"background":"transparent","depth":16,"resolution":300,"name":"ch01"}}
     {"id":2,"method":"doc.place","params":{"path":"L10_sky.png","smartObject":false,"fit":false,"scale":100}}
     {"id":3,"method":"engine.execute","params":{"command":"layer.setProps","params":{"name":"L10_sky","opacity":1}}}
     {"id":4,"method":"doc.place","params":{"path":"L20_figure.png","smartObject":false,"fit":false,"scale":100}}
     {"id":5,"method":"engine.execute","params":{"command":"layer.setProps","params":{"name":"L20_figure","opacity":0.9,"blend":"Multiply"}}}
     {"id":6,"method":"doc.save","params":{"path":"ch01_scene.ora"}}
     '@ | & $cli serve --automation-read-root C:\lj\ch01\in --automation-write-root C:\lj\ch01\out
     ```
     (Adding `layer.newAdjustmentLayer.curves` before saving forces a `.psd` or `.pcraft` target; the `.ora` would be refused.) **Not run; the sequence is read from the code and tests, Open question 1.**
2. **Maker's steps:** File > Open `ch01_scene.ora`. Paint, mask-by-erasing, move, rename inside the layers listed; if they add an adjustment layer, type, layer style or vector mask, PhotoCraft **will not overwrite the .ora**: accept its Save As `ch01_scene.psd` (same folder). Never "Save" over the original in `in\`; copy first to `work\`. Settings: Preferences > File Handling: leave autosave 10 minutes; Preferences > Performance: lower Memory Usage on 8 GB machines; do not use the x86 build.
3. **Export back:** the maker saves `work\ch01_scene.ora` (or `.psd`). Claude's script then runs, locally or on a copy: `photocraft-cli info work\ch01_scene.psd --compact` (layer tree JSON for the manifest), `photocraft-cli convert work\ch01_scene.psd out\ch01_scene.png`, and per-layer PNGs by `doc.exportLayers {dir:"layers", format:"png", visibleOnly:true}` on `serve`.
4. **Back in the pipeline:** the PNGs (`out\ch01_scene.png`, `out\layers\*.png`) plus the layer-tree JSON go into the asset manifest; the layered file stays the maker's private working copy.

### Recipe VectorCraft: SVG with stable ids

1. **Claude generates** `ch01_rig.svg`: unique clean ids on every element to animate (`[A-Za-z][A-Za-z0-9._-]*`, no spaces); pivots and z-order as `data-pivot`, `data-z` on `g/path/rect/circle/...` (not on `text`); no reliance on `class`, `<style>`, `transform` on groups, SMIL/CSS animation, `feColorMatrix`-type filters, or a `viewBox` with a non-zero origin (start at `0 0 W H`). Pre-flight in the container: `vectorcraft-cli convert ch01_rig.svg ch01_rig.rt.svg` and read `importWarnings` and `warnings`; then `check_ids.py ch01_rig.svg ch01_rig.rt.svg` (exit code 0 means every authored id and `data-*` survived).
2. **Maker's steps:** File > Open `ch01_rig.svg`; edit paths/colours; do not rename objects (the Layers panel name becomes the id). File > Save As, SVG, then in SVG Options: **Styling = Presentation Attributes** (author CSS can still override it; the dialog defaults to Internal CSS and Responsive, which produce `cls-N` classes), **Object IDs = Layer Names** (never "Minimal"), **Fonts = SVG** (text stays `<text>`) or Convert to Outlines for final art, **Images = Embed**, **Decimals = 3**, **Responsive = off** unless the page scales it, **Preserve editing / Illustrator editing capabilities = off**. Export (not Save) omits hidden objects: use Save As for rigs with `display:none` alternates.
3. **Export back:** `work\ch01_rig.touched.svg` plus, from the CLI, `vectorcraft-cli run --in work\ch01_rig.touched.svg --export out\ch01_rig.png --export out\ch01_rig.pdf --scale 2`.
4. **Back in the pipeline:** run `check_ids.py` (fails the gate on a lost id or changed `data-*`); then a script re-injects classes, `<style>` and the GSAP timeline by id. Keep `ch01_rig.svg` (the agent source) and diff against the touched file.

### Recipe LightCraft: ~300 scans

1. **Claude writes (not the scans):** `lj_scan_batch.ps1` and `faded-print-a.lcpreset` (sample in fixtures) for the maker's PC.
2. **Maker scans** to 16-bit TIFF into `D:\scans\raw\` (scanner software settings follow `ai-imagery.md`, not repeated here). Originals are only ever referenced.
3. **Script (JSON lines avoid quoting):** `steps.jsonl` (same shape as `craft-visual-fixtures/at-lightcraft-steps.jsonl`):
   ```
   {"command":"library.import","params":{"paths":["D:\\scans\\raw"],"mode":"add"}}
   {"command":"preset.import","params":{"paths":["C:\\lj\\faded-print-a.lcpreset"]}}
   {"command":"library.selectAll","params":{}}
   {"command":"preset.apply","params":{"id":"lj-faded-print-a","amount":100}}
   {"command":"app.export","params":{"dir":"D:\\scans\\out","format":"tif","bitDepth":16,"colorSpace":"srgb","naming":"{date:%Y}-{seq:3}","conflict":"skip"}}
   ```
   run as `set LIGHTCRAFT_GPU=0` then `"C:\Program Files\LightCraft\lightcraft-cli.exe" run --library D:\lc-lib --script steps.jsonl`. The preset keeps the id from the `.lcpreset` file unless it clashes with an existing one (`Session` import: "id clashes get a fresh id"), so check the `preset.import` result line once. Keep the library folder on a local NTFS disk and close the app first (one process per library). Running the preset import twice is harmless: identical presets are skipped. **[C] chain not executed.**
4. **Maker's steps:** open the library in LightCraft, sort by date, select a batch of similar prints, click a neutral border with the white-balance picker (or `develop.wbPick`), sync settings to the batch, nudge Color Mixer/Calibration, mark rejects. Settings live in the catalog (and in `.xmp` sidecars if Automatically Write Changes into XMP is on, in `lc:settings`).
5. **Back in the pipeline:** re-run the export step from the same catalog; outputs `out\*.tif` (masters) and `out\*.jpg` go to the manifest with checksums. "Edit in PhotoCraft" (right-click, 16-bit PSD stacked with the original; v0.7.1+) is the hand-off for dust spots or repairs.

### Five-minute acceptance tests (the maker, on their PC)

Record `--version` of each CLI first. Fixtures are in `research/craft-visual-fixtures/` (copy to `C:\lj\at\`). Any step that fails is a finding; do not fix by hand.

**PhotoCraft (about 5 min).** 1) `& "C:\Program Files\PhotoCraft\photocraft-cli.exe" --version`; right-click `photocraft.exe` > Properties > Digital Signatures (record signed/unsigned). 2) File > Open `at-layers.ora`: expect two layers, "Photo" (bottom) and "Title tint" (top, 60 percent, Multiply, offset 24,24) and no warning. 3) Set Title tint to 40 percent, add Layer > New Adjustment Layer > Curves, press Save. **Pass:** PhotoCraft refuses to overwrite the .ora and offers a PSD naming adjustment layers. **Fail (silent overwrite): the build predates the #3806 guard (< v0.9.0); upgrade before any ORA work.** 4) Save As `at-layers-edited.psd`, close, reopen: layers and Curves present. 5) File > Export (Quick Export) PNG; then in PowerShell `photocraft-cli info C:\lj\at\at-layers-edited.psd --compact` prints the layer tree and `photocraft-cli convert C:\lj\at\at-layers-edited.psd C:\lj\at\out.png` produces a PNG with no GPU activity.

**VectorCraft (about 5 min).** 1) `vectorcraft-cli --version`. 2) `vectorcraft-cli convert C:\lj\at\at-rig.svg C:\lj\at\at-rig.rt.svg`; read `importWarnings`: expect the `feColorMatrix` filter named as ignored; then `python check_ids.py at-rig.svg at-rig.rt.svg` (or open both in a text editor): **Pass:** no lost ids, `data-pivot` and `data-z` unchanged; `viewBox` changed from `100 50 400 300` to `0 0 400 300` (expected); classes `glow` gone or `cls-N` (expected). 3) Open `at-rig.svg` in VectorCraft, drag the sun a little, Save As SVG with the settings above to `at-rig.touchup.svg`; run the checker again (**Pass:** exit 0). 4) `vectorcraft-cli run --in C:\lj\at\at-rig.svg --export C:\lj\at\at-rig.png --export C:\lj\at\at-rig.pdf --scale 2`: both files open.

**LightCraft (about 5 min).** 1) `lightcraft-cli --version`; `set LIGHTCRAFT_GPU=0`. 2) Put any JPEG you own (not a family photo) at `C:\lj\at\print.jpg`. `lightcraft-cli render C:\lj\at\print.jpg -o C:\lj\at\print.out.jpg --set light.exposure=0.3 --set color.vibrance=25 --size 2048 --quality 92`. **Pass:** the file is written, brighter, 2048 px long edge. 3) Put two or three of your own non-family JPEGs in `C:\lj\at\prints\`, then `lightcraft-cli run --library C:\lj\at\lib --script C:\lj\at\at-lightcraft-steps.jsonl` (the JSON-lines file avoids Windows quoting; it imports with `mode: add`, imports the preset, applies `lj-faded-print-a`, exports `out\<name>-01.jpg`...). Read the JSON result lines: each must have `"ok": true`; an `id` clash on the preset import would make the apply step fail, which is a finding. 4) Start `lightcraft.exe` on the same library folder (File > Open Recent Library or the folder argument) while a CLI run is **not** active; edit one photo's white balance; quit; run the export again and check that the picture changed (catalog edits reached the CLI). **Pass:** all four. Then try the CLI while the app holds the library: **expected:** a clear "library in use" error, not corruption.

---

## Tools and formats

Cost and platform as of 2026-10-18: all three apps are free, open source (MIT or Apache-2.0 at your option), no account; Windows x64/x86/arm64 MSI + portable zip; macOS, Linux, FreeBSD, web. Alpha.

| Tool / format | Version | Maturity | Scriptability | Notes |
|---|---|---|---|---|
| PhotoCraft | v0.9.0 (website 0.7.0) | "Early alpha"; ready-for-real-work ~45 percent (vendor) | CLI `convert info run batch droplet commands mcp serve`; loopback JSON-lines control with bearer token; MCP | PSD/PSB/ORA/.pcraft/layered TIFF/Kra read; SVG read as shape layers (no SVG export) |
| VectorCraft | v0.12.0 (website 0.9.0) | Alpha; ~65 percent ready (vendor) | CLI `mcp run commands convert info bench perf`; control port without auth; MCP; no scripting language | SVG/PDF/.ai/EPS in and out; PSD out (merged image only on read) |
| LightCraft | v0.8.0 (website 0.6.0) | Alpha; ~61 percent of Lightroom (vendor) | CLI `run mcp render snapshot merge denoise-serve commands controls calibrate`; control port without auth | RAW + JPEG/TIFF/PNG/WebP/PSD composite/JXL/HEIC in; JPEG/PNG/TIFF/WebP/AVIF/JXL/DNG/PSD out |
| OpenRaster `.ora` | spec 0.0.x | Stable, simple | zip + XML + PNG, stdlib-writable | Agent to PhotoCraft contract |
| `.pcraft` | v-manifest | Native | Not agent-writable | Working format only |
| PSD via ag-psd 31.0.3 / psd-tools 1.25.0 | 2026-10-07 / 2026-10-14 | MIT / MIT (psd-tools license not stated in PyPI metadata I read) | Node / Python | Fallback input |
| `.vectorcraft` | format version 4 | Native JSON | Writable but not advised | Maker's working file |
| `.lcpreset` | version 1 | Native JSON | Agent-writable | Apply by `preset.apply` / `render --preset` |
| XMP sidecar `lc:settings` | n/a | Native | Read/merge safe | `crs:` read-only, approximate |
| Krita, GIMP, Inkscape, darktable, RawTherapee, ImageMagick | n/a | Mature (Inkscape and Krita not researched beyond the CLI page) | Krita export CLI; darktable-cli; rawtherapee-cli; `magick` | Fallbacks |

---

## Risks, pitfalls and ethics

Risk rating scale: Low / Medium / High for "a learner on a modest Windows PC depends on this for the 2027-02-27 deliverable".

| App | Rating | Why | Mitigation | Fallback |
|---|---|---|---|---|
| PhotoCraft | **Medium** for ORA in, PNG out (v0.9.0+); **High** for PSD interchange with anything else | Alpha; 56 percent match to Photoshop oracles; PSD export untested in other editors; GPU and low-RAM behaviour unproven on Windows; save-over guards on `main` only | Pin by the acceptance test; work on copies in `work\`; ORA for hand-off; flatten via CLI; `--safe-gpu` if the window misbehaves; lower Memory Usage | **Krita** (ORA is its native interchange; verified by the vendor's own test, 2026-10-09); GIMP weaker (3.0.x ORA export bug report) |
| VectorCraft | **Medium** (SVG touch-ups with the checker), **High** if animation depends on classes, filters, SMIL | Alpha; no real-world SVG corpus; Windows/browser QA missing; ids survive by test but rely on naming; no full-suite CI | `check_ids.py` gate on every save; ids/`data-*` only; keep agent source SVG as truth; export via Save As for hidden alternates | **Inkscape** (not researched here) |
| LightCraft | **Medium-High** | Youngest and fastest-moving; DX12/NVIDIA/Intel and installer unverified on Windows; no scan corpus; unauthenticated control port; face-recognition feature | Pilot of 10 prints vs darktable; CPU mode `LIGHTCRAFT_GPU=0`; library on local NTFS; references with `mode: add` only; turn off Faces and any model download | **darktable** (`darktable-cli` + styles) or **RawTherapee** (`.pp3`), ImageMagick for a crude pre-pass |

**Pitfalls worth a line each**
- **Silent loss on old builds:** PhotoCraft 0.7.0 (the website build) has ORA but not the no-overwrite guard; a Save after adding an adjustment layer could drop it.
- **"Save" is not "Export":** VectorCraft omits hidden objects from a plain Export; PhotoCraft writes a copy when the target cannot hold everything.
- **Percentages:** PhotoCraft "307 of 309" is self-consistency, not fidelity; VectorCraft "88 percent" counts existing menu items; website "134 of 135 byte for byte" is not in the repo; LightCraft "61 percent" is self-assessed. [V]
- **Unauthenticated loopback ports** (VectorCraft, LightCraft): enable `--control` only while using it; Windows firewall prompts must be declined for non-loopback; never expose to a network.
- **Traces left on the PC (surprise):** recent-file lists, recovery autosaves (`%APPDATA%\Photocraft\Recovery`, `%APPDATA%\VectorCraft`, `%APPDATA%\LightCraft` and logs, LightCraft thumbnail caches, XMP sidecars next to scans). Use the portable zips (`PhotoCraftData`, `VectorCraftData`, `LightCraftData` beside the exe) on a PC she does not use; clear Recent Files and Recovery after sessions.
- **Faces:** LightCraft has an opt-in face recognition feature (AuraFace model download from huggingface.co). Leave it off; faces of relatives are biometric data.
- **ArtCraft studio is separate** (`app.getartcraft.com`, cloud generation with pricing). Nothing in these three apps links to it from code; nothing about family photos goes through it.
- **Charter principle 4:** AI restoration of real prints and any generated layers must stay visibly marked in the manifest ("label ladder" in `ai-imagery`). The Craft apps' own AI features (PhotoCraft subject selection, content-aware fill, LightCraft masks) run locally and are classical or user-installed models.
- **Do not enable "Move" import in LightCraft** and do not point any batch `--in-place` at original scans.
- **Windows quoting:** passing JSON to native programs in Windows PowerShell 5.1 can strip inner double quotes (general knowledge, not from the sources). Use stdin JSON lines (`photocraft-cli serve`), `lightcraft-cli --script`, or PowerShell 7.

---

## Open questions / gaps

1. **Nothing here was executed.** Every "works" is from reading code, docs and tests. The week-1 acceptance test and the Design-phase spike (Linux CLIs in the container) are what convert [C] to proven. The exact `serve`/`run` assembly sequence for a layered PSD/ORA is assembled from the registry and tests; confirm it.
2. **Issue trackers, release notes, Discord: unreachable** from this container (403; the API needs an attached repo with push access, which I did not request). No statement about open crash or data-loss issues can be made. If the orchestrator attaches the repos with API access, re-run Q7.
3. **Maker's installed versions and build type** (Launcher table or Help > About) and the **hardware inventory** are unknown; PhotoCraft memory and LightCraft DX12 behaviour depend on them.
4. **Release notes for 0.8.0/0.4.0 etc. and tags missing from the remote** are unknown.
5. **Windows code signing status** of the actual MSI (README says signed; vendor gap doc says not obtained).
6. **usvg grouping:** nested plain groups without an id are not guaranteed to survive; I could not read the pinned usvg source (not vendored); named groups survive by test.
7. **Headless Chromium + web builds:** whether `?cpu`/`?webgl` runs under SwiftShader was not tested; VectorCraft's `?cpu` is documented but not read by the code.
8. **LightCraft versus darktable on faded prints:** no objective comparison exists; the pilot must make it. No evidence about LightCraft's behaviour on very large (600 dpi, 16-bit) TIFFs beyond "60 MP+ renders on the CPU".
9. **Krita as the ORA fallback** is evidenced only by the vendor's own corpus note; MyPaint and GIMP "have not been checked yet" (docs/ora.md).
10. **Inkscape** was not researched (no URL seen); treat the VectorCraft fallback as an assumption until the spike tests the same `at-rig.svg` in it.
11. **Fixtures** in `research/craft-visual-fixtures/`: `at-layers.ora`, `at-rig.svg`, `faded-print-a.lcpreset`, `at-lightcraft-steps.jsonl`, `check_ids.py` and `make_ora.py` were created and checked for well-formedness only (zip/XML/JSON parse, checker self-test); not opened in the Craft apps.

What this means for Life Journey: use the Craft apps as **three narrow, verifiable hand-offs**: ORA for layered stills, SVG with ids and `data-*` for animation art, and `.lcpreset` plus the LightCraft CLI for the scan batch. Pin versions after the acceptance test, keep every step reproducible by script, keep family material on the maker's PC, and keep Krita, Inkscape and darktable one step away.

---

## Sources

Repo files: `<repo>/<path>` at the pinned tag (PhotoCraft `v0.9.0` = `c699e3cda69f`, VectorCraft `v0.12.0` = `8bc653292861`, LightCraft `v0.8.0` = `16dbb90499d3`); GitHub locator `https://github.com/storytold/<repo>/blob/<tag>/<path>` (github.com HTML was 403 from the container; files were read in a local clone). Web pages: fetched 2026-10-18.

[1] photocraft/README.md (v0.9.0) — https://github.com/storytold/photocraft/blob/v0.9.0/README.md — 2026-10-14 — feature list, 307/309 claim, Windows downloads, status "early alpha".
[2] photocraft/docs/file-format-parity.md — PSD/ORA/SVG support table, oracle floors, `.pcraft` autosave/atomic save.
[3] photocraft/crates/io/tests/corpus.rs — floors 146/169, 236/308, 145/258 (or /256) and what "oracle pass" and "round trip" mean; crates/psd/tests/corpus.rs (byte-stable).
[4] photocraft/docs/ora.md — ORA kept/lost table, no-overwrite rule (#3806), Krita 5.2.9 verification (32/35, 33/34).
[5] photocraft/crates/psd/README.md — API, feature matrix, "preserved raw" (stale).
[6] photocraft/book/src/formats/{overview,psd-psb,pcraft,raster-formats,svg}.md — `.pcraft` layout, PSD limits, layered TIFF, SVG import table, 32-bit allocation limit.
[7] photocraft/apps/photocraft-cli/src/lib.rs; book/src/automation/cli.md — subcommands, `run --new`, `batch --actions` shape, usage text.
[8] photocraft/docs/control-protocol.md; docs/mcp.md; book/src/automation/security-model.md — bearer token, loopback, headless `serve` methods, limits, MCP tools, bridge.
[9] photocraft/crates/engine/src/{commands.rs,file_cmds.rs,layer_multi_cmds.rs} — `file.new`, `file.placeEmbedded` (smartObject param), `loadFilesIntoStack`, `layer.setProps`, `layer.renameLayer`, `layer.moveTo`.
[10] photocraft/crates/automation/src/{headless.rs,rpc.rs,files.rs}; crates/automation/tests/{openraster.rs,agent_tasks.rs} — save by extension, trusted-local vs workspace, tests of layered ORA save and ten scripted tasks.
[11] photocraft/packaging/windows/{photocraft.wxs,package.ps1,portable.txt}; docs/releasing.md — MSI components incl. CLI, PE checks, static CRT, "Windows 10+", portable mode.
[12] photocraft/packaging/web/{README.md,_headers,package.sh}; apps/photocraft-web/src/web.rs — web zip contents, headers, `?cpu`/`?webgl`, no autosave.
[13] photocraft/docs/{scorecard.md,gaps.md,target-app-parity.md,hardware-parity.md} — scorecard rows (REL, BUG-203, DIST), G1/G17, readiness numbers, 1,230 issues, perf baseline (macOS M4 Pro).
[14] photocraft/docs/development.md — graphics startup and device loss, env vars, logs.
[15] photocraft/crates/format/src/autosave.rs; crates/engine/src/prefs.rs — autosave 10 min, Memory Usage 8192 MB, scratch disks.
[16] photocraft/Cargo.lock; storytold/craft-libs rev 3d37da3 `crates/print/Cargo.toml`; storytold/winprint.rs rev 5f80b9b `Cargo.toml` — where reqwest comes from (build-dependency only).
[17] photocraft/.github/workflows/ci.yml; windows-arm64.yml — test matrix incl. windows-latest.
[18] vectorcraft/README.md (v0.12.0) — status, downloads, agent use, MCP registration.
[19] vectorcraft/crates/svg/src/lib.rs — import/export approximations, ExportOptions, editing data.
[20] vectorcraft/crates/svg/src/import.rs (+ import/*.rs) — usvg options, labels, layer mode, data-* handling, OBJECT_ELEMENTS.
[21] vectorcraft/crates/svg/src/export.rs — `sanitize_id`, `id_attr`, viewBox line, classes.
[22] vectorcraft/crates/svg/tests/{ids,symbols_layers,roundtrip,options,gradients,prop_svg}.rs — id/name, rig, nested group, class and style tests.
[23] vectorcraft/crates/format/src/lib.rs; examples/dusk-poster.vectorcraft — `.vectorcraft` JSON.
[24] vectorcraft/apps/vectorcraft-cli/src/main.rs — usage, `convert`, `run`, `info`.
[25] vectorcraft/docs/mcp.md — tools, roots, modes, Windows MSI path, Data Recovery.
[26] vectorcraft/docs/control-protocol.md — loopback, "no authentication", limits.
[27] vectorcraft/docs/development.md — web build, GPU selection and crash markers, logs, robustness ("never crashes").
[28] vectorcraft/crates/trace/src/lib.rs; docs/image-trace-quality.md — 15 presets and params.
[29] vectorcraft/packaging/windows/{vectorcraft.wxs,package.ps1}; docs/releasing.md; docs/windows7.md; packaging/web/README.md; apps/vectorcraft-web/src/web.rs.
[30] vectorcraft/docs/{target-app-parity.md,file-format-parity.md,hardware-parity.md,gaps.md} — 88 percent breakdown, no real-world corpus, robustness row.
[31] vectorcraft/crates/engine/src/cmd/fileio/{mod.rs,svg.rs,save.rs} — writable formats, SVG option defaults, `.ai` embedding.
[32] lightcraft/README.md (v0.8.0) — features, built for agents, local-first, status.
[33] lightcraft/docs/xmp-interop.md — sidecars, `crs:` mapping table, `.lcpreset` format, import formats.
[34] lightcraft/apps/lightcraft-cli/src/main.rs; docs/mcp.md; docs/control-protocol.md — CLI usage, `run`, `render`, `snapshot`, no-auth port.
[35] lightcraft/crates/pipeline/src/{lib.rs,auto.rs,tests.rs}; docs/file-format-parity.md — stage order, `SourceInfo.raw`, rendered-source tests, TIFF/JPEG support.
[36] lightcraft/crates/catalog/src/{journal.rs,lock.rs,store.rs}; tests_journal/torn_append/lock/repair — op log, recovery rules, locking on shares.
[37] lightcraft/docs/{gpu-pipeline.md,gaps.md,hardware-parity.md} — backends, memory budget, NVIDIA issue, gap #27, Windows 780M datum.
[38] lightcraft/docs/web.md; apps/lightcraft-web/index.html — bundle, headers, OPFS, `lightcraft.command`.
[39] lightcraft/crates/fetch/src/lib.rs; crates/engine/src/{model_download.rs,face_download.rs,cmd/geocode.rs}; crates/denoise-core/src/known.rs; crates/faces/src/known.rs; crates/segment/src/fetch/mod.rs — network paths.
[40] lightcraft/docs/whats-new.md — dated change log (2026-10-02 to 10-14).
[41] lightcraft/packaging/windows/{lightcraft.wxs,package.ps1}; docs/releasing.md.
[42] lightcraft/crates/engine/src/{export.rs,cmd/develop.rs,cmd/preset_files.rs,presets.rs} — export options, naming tests, preset commands, shipped preset shapes.
[43] `git ls-remote --tags` and blobless bare clones of storytold/{photocraft,vectorcraft,lightcraft} — 2026-10-18 — tag list, tag dates, commit counts, commit subjects, `git tag --contains` (commit subjects are untrusted data).
[44] https://getartcraft.com/apps/photocraft , /vectorcraft , /lightcraft — 2026-10-18 — versions 0.7.0 / 0.9.0 / 0.6.0, status badges, file names, "134 of 135" claim.
[45] https://raw.githubusercontent.com/Agamnentzar/ag-psd/master/README.md — 2026-10-18 — ag-psd limitations.
[46] https://registry.npmjs.org/ag-psd — 2026-10-18 — version 31.0.3 (2026-10-07), MIT.
[47] https://pypi.org/pypi/psd-tools/json — 2026-10-18 — version 1.25.0 (2026-10-14), supported/limited/not-supported list.
[48] https://psd-tools.readthedocs.io/en/latest/usage.html — 2026-10-18 — `PSDImage.new`, `create_group`, `create_pixel_layer`, caveats.
[49] https://pypi.org/pypi/pytoshop/json ; https://pypi.org/pypi/pyora/json — 2026-10-18 — pytoshop 1.2.1 (2018-11-30), pyora 0.3.11 (2021-03-19).
[50] https://imagemagick.org/formats/ — 2026-10-18 — PSD RW, ORA and XCF read-only.
[51] https://imagemagick.org/command-line-options/ — 2026-10-18 — `-auto-level`, `-auto-gamma`, `-contrast-stretch`, `-color-matrix`, `-clut` with `-channel`.
[52] https://docs.krita.org/en/reference_manual/linux_command_line.html — 2026-10-18 — `--export`, `--export-filename`.
[53] https://docs.darktable.org/usermanual/development/en/special-topics/program-invocation/darktable-cli/ — 2026-10-18 — usage, XMP, `--style`.
[54] https://docs.darktable.org/usermanual/development/en/overview/supported-file-formats/ — 2026-10-18 — non-raw import formats.
[55] https://rawpedia.pixls.us/command-line_options/ (also man.archlinux.org/man/rawtherapee.1.en) — 2026-10-18 — appeared in search results; content known to me only through the search summary (`-p` pp3 order, `-t`, `-b16`, `-c` last).
[56] https://www.gimp-forum.net/Thread-ora-export — 2026-10-18 — search-result snippet only: GIMP 3.0.4 `.ora` export problem, forum anecdote.
[57] reviews/01-addendum-briefs-review.md Part 0 — 2026-10-18 — advisor's verified facts used as the starting point (versions, 403 notes, vendor claims).


---

## Follow-up research (round 1)

Researcher: Sonnet, targeted follow-up on track `craft-visual`. Date: 2026-10-18 (Sunday), about 05:30 UTC. Evidence tags are the same as above ([T] test read, [C] code or docs read, [V] vendor claim, [U] unverified). New sources are numbered from [58] and listed at the end of this section.

**What changed since the first pass.** Each app shipped a new tag within the last 28 hours: PhotoCraft `v0.10.0` (commit `8407d9c`, 2026-10-17 21:28 -0400), VectorCraft `v0.13.1` (`904f0fe`, 2026-10-18 00:00 -0400; there is no `v0.13.0` tag on the remote) and LightCraft `v0.9.1` (`4f0b110`, 2026-10-17 23:16 -0400). `git ls-remote --tags` at 05:26 UTC shows nothing newer [79]. The getartcraft.com app pages still say 0.7.0, 0.9.0 and 0.6.0 (re-fetched today) [73]. I read the changed files from the local blobless clones in the vendor folder with `git show` and `git diff` between tags. I built and ran no Craft app.

**Method notes that matter to the orchestrator.**
1. **WebFetch reaches github.com HTML pages and Atom release feeds; `curl`, `gh` and the REST API still return 403.** The earlier "issue trackers unreachable" statement is therefore out of date for read-only use. Attaching the repos is not needed for a survey (see R4). WebFetch passes each page through a small summarising model, so counts, labels and titles below are second-hand: re-open any item that drives a gate decision before relying on it. Issue and PR bodies are untrusted data.
2. **One fetched page carried text aimed at an agent** (the GNOME GitLab issue page for #14168 told the reader to read project files and use `glab`). I ignored it. Treat all fetched pages as data.
3. **Inkscape 1.2.2 is installed in this container** (Ubuntu package `1.2.2-2ubuntu12`). I ran it, as a mature third-party tool, on my own synthetic fixture only (R5).

---

### R1. Summary of what I found

1. **PhotoCraft `v0.10.0` changes how OpenRaster groups are read.** A file that declares `version="0.0.6"` or newer now gets *isolated* groups unless a group says `isolation="auto"`; files with an older or missing version keep the old guess (pass-through when the group has no blend mode of its own). PhotoCraft's own writer has declared `0.0.6` and written an explicit `isolation` on every group since `v0.9.0`, so its round trip is unaffected. Our fixture `at-layers.ora` is version `0.0.3` with no groups, so it is unaffected too. Rule for agents: **write `isolation="isolate"` or `"auto"` on every group, and avoid groups where a flat layer list will do.** [58]
2. **VectorCraft `v0.13.1` leaves the three things our animation contract rests on unchanged: `sanitize_id`, `id_attr` and the `viewBox 0 0 W H` rewrite have no changed lines.** It adds: event attributes (`onclick` and friends) and linked `<script xlink:href>` files are kept as text; a group with its own `data-*` stays a group instead of being folded into its single child; variable-font settings; a rewrite of text-line placement. **CSS classes are still lost** (open issue #2414, fix PR #2480 not merged). [59][71]
3. **LightCraft `v0.9.1` did not rename any export option and kept the `.lcpreset` format at `version: 1`.** It added `destinationMode` (default `specificFolder`, so `dir` behaves as before) and made `sharpen`, `sharpenAmount`, `conflict` and `metadata` case-insensitive. `render --settings FILE.lcpreset` **now works**; in `v0.8.0` it silently applied nothing (#1730). The step file `at-lightcraft-steps.jsonl` is still valid. [60]
4. **New blocker for the scan path: LightCraft cannot open a TIFF whose single strip or tile is larger than 128 MiB** ("malformed TIFF data: decoder limits exceeded"). `v0.9.1` still has the old limit; the fix PR (#1989) is open and has a review finding. A 16-bit RGB 8x10 inch scan at 600 ppi is 172.8 MB and would hit it if the scanner writes one strip. Add the largest scan to the 10-print pilot. [60][72]
5. **Inkscape 1.2.2 passes the fallback test.** `--export-plain-svg` on `at-rig.svg` kept all 11 authored ids, both `data-pivot` and `data-z`, the `class`, the `<style>` text and the original `viewBox`; `check_ids.py` exit code 0. Inkscape's *Optimized SVG* output removes unused ids by default and would strip `leaf-1` and `leaf-2`. [63]
6. **`photocraft-cli serve` accepts Windows drive-letter paths in both root flags and in request paths, with rules** (R6). Root flags work; the env-var form stays desktop-only. Read from code and a test that CI runs on `windows-latest`; not run on Windows by me.
7. **GIMP report: confirmed as a real bug, but narrower and older than our note said** (R7). It is GIMP 3.0.4 (May to July 2025), GitLab #14168, now marked closed; I could not find the fix version. Do not cite it as current behaviour.
8. **Maker's versions and hardware are unknown** and cannot be learned from this container. A read-only PowerShell block to collect them is in R2. One new reason to ask about the Windows install: PhotoCraft fails to start on stripped-down ("debloated") Windows images (#6249).
9. **The trackers show real, current risk.** PhotoCraft has 1,689 open issues, 71 open with `priority: critical`, 87 open that match "crash". Several are save, overwrite or PSD-in-Photoshop problems. This supports the plan: ORA in, PNG out; PSD as a private save format; work only on copies. [69][70]

---

### R2. Maker's installed versions, install type and hardware (Q1) — UNVERIFIED

Nothing in the charter, the playbooks or this container records the maker's versions, install type or hardware (the grep for CPU, GPU, RAM and scanner terms in the project files found only the researcher's own container). The container itself (Ubuntu 24.04, 4 CPUs, 16 GB RAM, no GPU) is not the maker's PC. **UNVERIFIED.**

What each answer changes:

| Unknown | Why it matters | Source of the concern |
|---|---|---|
| Version of each app | If installed from the website: PhotoCraft 0.7.0 (has ORA, no no-overwrite guard #3806), VectorCraft 0.9.0, LightCraft 0.6.0. The ORA guard and the save guards are only in `v0.9.0`/`v0.10.0`. | [43][44][73] |
| MSI or portable zip; Launcher or website | Portable builds keep recovery and settings beside the exe (`PhotoCraftData`) and leave fewer traces on a shared PC. The Launcher polls GitHub for updates and must be off in production. LightCraft's install page names `C:\Program Files\LightCraft` and the Launcher as options. | [11][80] |
| CPU architecture (x64, x86, arm64) | Do not use the x86 builds (PhotoCraft caps decode memory at 2 GiB on 32-bit). arm64 is a separate build. | [6][73] |
| Windows edition and whether it is a stock install | PhotoCraft's `photocraft.exe` **and** `photocraft-cli.exe` import `Windows.Data.Pdf.dll` at load time; Windows images stripped with tools such as NTLite lack it and the app will not start. Fix PR #6395 is open, not in `v0.10.0`. Workaround: keep the Windows PDF component, or use a stock install. | [70] |
| GPU, VRAM, driver | VectorCraft crashes at start on Intel UHD 605 under DX12 (#2243, open; a skip-the-crashed-adapter fix has landed, first start may still crash). PhotoCraft has a red-block bug on Intel Iris Xe DX12 (#6790, open) and a Windows black-window fix that prefers WARP over GL (in `v0.10.0` notes). LightCraft has no Windows crash issue in the critical list, but gaps #27 still says DX12, NVIDIA and Intel are unverified. | [64][70][71][72] |
| RAM and free disk | PhotoCraft's Memory Usage preference defaults to 8192 MB; vendor baseline is a macOS machine with 48 GB. LightCraft's budget is min(25 percent of RAM, 1.5 GiB). A 16-bit 600 ppi scan batch needs tens of GB of disk. | [13][15][37] |
| Monitors with mixed display scaling | Open issues: window grows and crashes when dragged across monitors with different scales (VectorCraft #1459, LightCraft #1318); window-resize freeze on Windows 11 (PhotoCraft #7252). | [70][71][72] |
| Scanner make and model, and whether the PC is in a room she uses | Scanner drivers (see `ai-imagery.md` for the V600/V850 caveats). A shared room means portable zips, cleared recent-file lists and recovery folders after each session (Risks section above). | [57] |

**Collection script for the maker** (read-only; it prints to the screen and sends nothing anywhere; run it in an ordinary PowerShell window; the install folders are the MSI defaults and the portable zips need their own path):

```powershell
# Versions and install type
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -match 'craft' } | Select-Object DisplayName, DisplayVersion, InstallLocation
foreach ($a in 'PhotoCraft','VectorCraft','LightCraft') {
  $cli = "$env:ProgramFiles\$a\$($a.ToLower())-cli.exe"
  if (Test-Path $cli) { "$a CLI: " + (& $cli --version) } else { "$a CLI not at $cli (portable or other folder?)" }
}
# Windows and hardware
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, @{n='RAM_GB';e={[math]::Round($_.TotalPhysicalMemory/1GB,1)}}
Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{n='Free_GB';e={[math]::Round($_.Free/1GB,1)}}
Test-Path "$env:SystemRoot\System32\Windows.Data.Pdf.dll"
```
Also ask by hand: Launcher or website? MSI or zip? Is Windows a normal install (not stripped)? Scanner model? Does she use the room or the PC? (VRAM is not reliable from `Win32_VideoController` on some systems; read it from Task Manager, Performance, GPU, if it matters. That caveat is general knowledge, not from a source.)

---

### R3. Re-read of the changed files (Q2)

#### R3a. PhotoCraft `v0.9.0` to `v0.10.0`: `docs/ora.md` and `crates/io/src/ora.rs` [58]

Changed: `ora.rs` 37 lines and `docs/ora.md` 12 lines (42 insertions and 7 deletions together), plus `ora/tests.rs` +78 lines (synthetic 8/16-bit fixtures for modern and legacy group isolation). Nothing else in the ORA path changed.

| Aspect | `v0.9.0` | `v0.10.0` | Effect on us |
|---|---|---|---|
| Group becomes pass-through when | `isolation` is not `isolate` **and** the group's blend is Normal | If the file's `image@version` parses as `x.y.z` (exactly three numeric parts; anything after a `-` or `+` is ignored) and is >= `0.0.6`: only when `isolation="auto"`, group blend ignored; omitted `isolation` means isolate. Older, missing or unparseable version: the old rule | Third-party files that say 0.0.6+ and omit `isolation` can now render differently (a Multiply layer inside a group stops reaching the backdrop) |
| `version` written by PhotoCraft | `0.0.6`, and `isolation="auto"` for pass-through groups, else `"isolate"`, on every group | Same (`ora.rs` line 696 at `v0.10.0`; line 669 at `v0.9.0`) | PhotoCraft to PhotoCraft is stable in both builds |
| Pass-through group opacity | n/a | Doc: still PhotoCraft's own interpolation, "can differ from 0.0.6's per-child opacity multiplication for overlapping children" | Keep pass-through groups at opacity 1 |
| Everything else (layers, offsets, locks, blend names, 8/16-bit, the no-overwrite rule) | as in section 2 | unchanged | The first-pass matrix stands |

The spec text (fetched via a summariser) lists `isolation` with default `isolate`, added in 0.0.4, and says a non-isolated stack ignores its own `composite-op` [77]. PhotoCraft's source comment attributes the "default isolate" switch to 0.0.6, so the two disagree on the version; the practical rule below avoids the question.

**Rule for agents writing ORA for PhotoCraft:** declare `version="0.0.3"` (as `make_ora.py` does) or write `isolation` explicitly on every `<stack>` group; prefer flat layer lists. With an explicit attribute the old and new readers agree, except `auto` on a group with a non-Normal blend (old reader: isolate, new reader: pass-through). The Krita 5.2.9 corpus check (32 of 35, 33 of 34) was run on `v0.9.0` and **was not repeated** for the new rule (UNVERIFIED for `v0.10.0`). No change is needed to `make_ora.py` or `at-layers.ora`.

Related open and closed ORA issues: #7018 (open, high; `edit-locked` reopens as Lock All and Lock Position is dropped with no warning; PR #7019 open); #3806 (closed 2026-10-13, in-place Save of ORA omitted adjustment layers and marked the file clean: this is the guard); #3048 and #3049 (closed: group fill opacity, whitespace in names). **Do not rely on layer locks surviving an ORA round trip.** [70]

The `serve` method `doc.place` still passes `smartObject`, `fit`, `scale`, `center` through to `place_bytes`, which reads `smartObject` (explicit `false` gives a plain pixel layer); the control-protocol table for `doc.place` does not list `smartObject` but the code honours it [61]. The recipe above stands.

#### R3b. VectorCraft `v0.12.0` to `v0.13.1`: `export.rs` (+210) and `import.rs` (+88), plus neighbours [59]

Also changed in the `svg` crate: `css.rs` (+46), `import/files.rs` (+74), `import/fx.rs` (+3), `import/text.rs` (+25), `Cargo.toml` (+`craft-docpath`), and tests `interactivity.rs` (+176, new), `data_attributes.rs` (+16), `text_layout.rs` (+178), `css_rules.rs`, `encoding_profile_fonts.rs`, `import_live.rs`, `import_text.rs`.

| Contract item | Result at `v0.13.1` | Evidence |
|---|---|---|
| `sanitize_id` (letters, digits, `-`, `_`, `.`; other characters become `_`; a leading non-letter other than `_` gets `_`) | **Unchanged.** No hunk touches it (`export.rs` line 485 at `v0.13.1`) | `git diff` has no hit for `sanitize_id`, `id_attr`, `viewBox` |
| `id_attr` and `data-name` for the exact name | **Unchanged** | same |
| Root `viewBox` always `0 0 W H` | **Unchanged** (line 117) | same |
| `data-*` kept on `g, a, use, path, rect, circle, ellipse, line, polyline, polygon, image` | Kept. **New:** an id-less group that wraps one object and has its own `data-*` (or event attributes) now stays a group and keeps them; before it could be folded into the child [T] `data_attributes.rs::an_unnamed_group_around_one_object_keeps_its_own_data` | `import.rs` hunk `own = self.data.contains_key(...)` |
| `data-*` on `text` | Still not kept (the event-attribute list adds `text`, the data list does not) | `EVENT_ELEMENTS` vs `OBJECT_ELEMENTS` |
| `class` and `<style>` | **Still lost.** Open issue #2414 "CSS classes not preserved when exporting SVG" (priority medium); PR #2480 (open, force-pushed 2026-10-17) would keep imported classes, write them in every styling mode and drop `cls-N`; it says nothing about `data-*` | [71] |
| **New:** event attributes (`onclick`, `onmouseover`, `onload`, ...) | Read from `g, a, use, path, rect, circle, ellipse, line, polyline, polygon, image, text`; kept as text, never run; written back (once each, unknown names dropped with a warning; SVG Tiny leaves them out) | [T] `tests/interactivity.rs` |
| **New:** `<script xlink:href="x.js"/>` | Linked files kept in order (at most `MAX_SVG_SCRIPTS`), written after `<desc>`; **inline `<script>` text is dropped with a warning** | `linked_scripts`, `export.rs` hunk |
| Variable fonts | `font-variation-settings` and `wdth`/`wght` read and written; `font-stretch` in `@font-face` | `css.rs`, `import/text.rs` |
| Text placement | Large rewrite for justified and Mojikumi lines (`reader_advances`, `end_segment`); matters only for justified live text | `export.rs` |
| Linked image paths | Resolved by the new `craft-docpath`; `\\server\share` and `file://host/` hrefs are **not read** | `import/files.rs` test `hrefs_to_other_computers_are_not_read` |
| Filters | Outer glow now exports as a solid-silhouette filter; pixel and rasterise effects still dropped with a warning. `feColorMatrix`-type filters still ignored on import | `export.rs`, `fx.rs` |
| XML-id escaping (v0.13.1 release note: "XML IDs whose first character can't start an XML name are now escaped") | Concerns `crates/doc/src/xml_id.rs` (`from_object_name`, now escapes a leading `-`, `.`, digit and similar as `_xHH_`). I found **no use of it in `crates/svg` or `crates/pdf`**, so the SVG ids above are unaffected; the note is about another path | `git show v0.13.1:crates/doc/src/xml_id.rs` |

**Effect on the recipe:** none required. Two optional gains: a linked `<script xlink:href="gsap.min.js"/>` survives a VectorCraft save (inline scripts do not), and `data-*` on a wrapper group is safer. Keep "animate by `id` and `[data-*]`, re-add classes and `<style>` after the touch-up" until #2480 merges and a tag contains it.

#### R3c. LightCraft `v0.8.0` to `v0.9.1`: export option names and `.lcpreset` version [60]

The whole range is large (502 files, +83,660/-4,114 lines, including a new `docs/user/` guide folder). For our pipeline:

| Item | Result |
|---|---|
| `.lcpreset` format string and version | Unchanged: `"format": "lightcraft.preset"`, `"version": 1` (`presets.rs` line 16 and `docs/xmp-interop.md` at both tags). `presets.rs` changed 2 lines: the file extensions accepted by `expand_preset_paths` now include `.lceffect` |
| `app.export` parameter names | **No name removed or renamed.** One added: `destinationMode` (`specificFolder` default, or `sameAsOriginal`, which writes next to each original: **never use it on scans**). `OPTION_PARAMS` gains only that entry. `dngCompression` gains `lossy` |
| Case handling | `sharpen`, `sharpenAmount`, `conflict`, `metadata` are now parsed case-insensitively and an unknown value is an error. Fixes a bug where `metadata: "NONE"` passed validation, then fell back to `all` and kept GPS data [T] `accepted_choices_are_the_ones_exported` |
| `preset.apply {id, amount}` | Still valid. `v0.8.0` called `targets(p)` with `id` (the preset's id) in the params; a string id fell through to the selection by luck. `v0.9.1` passes only `ids` to `targets`, and `targets` now errors on a non-numeric `ids` or `id` (#1506). **Our step file uses a string preset id and `library.selectAll`, so it works at both tags** |
| `render --settings` | **Fixed:** a `.lcpreset` or XMP preset file now applies as a preset (one preset per file; several is an error). In `v0.8.0` it "dropped its wrapper and applied nothing" (#1730) with no error. `--preset ID` and `--set control=value` are unchanged |
| CLI `run`, `--library`, `--script` | No change in the usage text beyond `merge hdr-batch` |
| `preset.import` result | Adds `profile` per preset and `effects`/`effectDividers` keys. Existing keys unchanged |
| `preset.export` | Now refuses to overwrite an original or sidecar and writes durably (#1637) |
| TIFF decoder | `crates/codecs/src/tiff_codec.rs` `limits()` is **identical** at both tags: it raises `decoding_buffer_size` but not `intermediate_buffer_size`. See R4 |
| GPU | When the driver resets the GPU during export or render (#1337, seen on Windows with NVIDIA), LightCraft still stops, now says why, and the next start renders on the CPU |
| JPEG export | 12 to 14 percent smaller at the same pixels (per-file Huffman tables) |
| Windows packaging | Adds `FONT-LICENCES.txt` to the MSI and portable zip; PowerShell 5.1 architecture detection fix. Portable zip and MSI contents otherwise as before |
| New user docs | `docs/user/getting-started/install.md` (Windows 11, default `C:\Program Files\LightCraft`, "ArtCraft Launcher installs the release `.msi`"), `faq/free-and-private.md` (no telemetry, default library `~/Pictures/LightCraft Library`). **Pictures may be a cloud-synced folder on Windows** (general knowledge): always pass an explicit local `--library D:\lc-lib` as the recipe does |

`docs/gaps.md` row 27 is unchanged at `v0.9.1`: "Windows installer UI unverified; GPU path proven on Apple and one AMD GPU on Linux; NVIDIA, Intel and DX12 unverified" [60].

#### R3d. Other pin-relevant changes in the three new tags (vendor release notes) [64][65][66][67]

- **PhotoCraft `v0.10.0`** includes, per its notes: Save asks before overwriting a file another app changed (#6652); Save refuses to replace a read-only file (#6643); Quick Export "Same Folder" asks before replacing the document's own file (#6632); crash-recovery autosaves moved to `%LOCALAPPDATA%\Photocraft\Recovery` on Windows (also in the `v0.10.0` `docs/control-protocol.md`); Windows prefers WARP over GL to avoid a black window (the notes give the issue number two ways, #5191 and #5309); PSD recovers layers when the merged image data is damaged. Vendor test floors rose: Photoshop oracles 145 to 188 of 256, psd-tools 236 to 249 of 309; never-crash lints on 30 of 30 crates [V]. **This closes most of the "only on `main` after the tag" gap listed in finding 13 of the first pass.**
- **VectorCraft `v0.13.1`:** XML-id escaping, live-text spacing for justified lines, decode limit raised to 2 GB for sampling and recolouring [66].
- **LightCraft `v0.9.1`:** Windows packaging and CJK fonts (#1479), GPU-loss handling (#1337), raw-size checks before allocation (#1512), original-protecting preset export (#1637), CLI refuses non-object snapshot params instead of panicking (#1791) [67].

**Updated provisional pins (supersede the first-pass pins, same rule):** PhotoCraft `v0.10.0`, VectorCraft `v0.13.1`, LightCraft `v0.9.1`, **subject to the maker's five-minute test and to re-checking the tag lists on 2026-10-25** (the tags are one day old; the first-pass rule "pin the newest tag on the day the maker passes the test, no later than 2026-10-25" stands). Record the installer hashes from each release's `SHA256SUMS.txt`.

---

### R4. Issue trackers and release notes (Q3, and the original Q7)

**Access.** Reachable with WebFetch: `github.com/storytold/<repo>/issues`, issue and PR pages, issue search URLs (`/issues?q=...`), `/releases/tag/vX`, `/releases.atom` and `/commits/main.atom` (the release feeds are 1 to 2.5 MB; I read the first 100,000 characters only, which holds the newest release). Not reachable: the same URLs by `curl` (403), `/issues.atom` (406), the REST API (403). **Recommendation to the orchestrator: do not attach the repos** (push-level attachment would only widen credentials for a read-only job). Re-run this survey with WebFetch at each pin gate (suggest weekly until the pin, then at each gate). [68][69]

**Size of the trackers (2026-10-18).**

| Repo | Open issues | Open `priority: critical` | Open and matching crash/freeze/hang | Other searches run |
|---|---|---|---|---|
| PhotoCraft | 1,689 | 71 | 87 ("crash") | data-loss/overwrite words: 40 open; "OpenRaster / .ora": 13 (7 open, 6 closed) |
| VectorCraft | 440 | 8 | 22 | SVG + id/data/class/import/export words: 51 open |
| LightCraft | 475 | 13 | 38 | windows/DX12/nvidia/intel/tiff words: 128 open |

These are volumes, not severity: the vendor itself counted about 1,230 issues filed by 2026-10-10 and many reports are duplicates or "needs info" [13].

**Open issues that touch our three hand-offs, and what we do about each.**

| Repo and issue | Title (paraphrased), state, date | What it means for the plan |
|---|---|---|
| PhotoCraft #6249 | Launch crash, `Windows.Data.Pdf.dll` not found, on a Windows image edited with NTLite; open, critical; fix PR #6395 open; both `photocraft.exe` and `photocraft-cli.exe` import it at load time (contributor comment) | Ask whether Windows is a stock install. Not fixed in `v0.10.0` |
| PhotoCraft #7252 | Dragging the window edge fast for seconds causes artefacts and a freeze, Windows 11; open, critical (2026-10-18) | Do not resize the window while it holds unsaved work; autosave is 10 min |
| PhotoCraft #7018 | ORA: pixel lock becomes Lock All, position lock dropped, no warning; open, high; PR #7019 | Do not rely on locks in ORA |
| PhotoCraft #6895, #6968, #6703, #6311 | PSDs written by PhotoCraft will not open in, or crash, Photoshop; open, critical | Confirms: PSD is a private PhotoCraft format; hand-offs go through ORA and PNG |
| PhotoCraft #6424 | Several features store invalid (infinite) values and the document cannot be saved; open, critical | Save to a new name often; keep the autosave on |
| PhotoCraft #4968, #6597, #7102 | Save reports success after failed directory flush; Save As onto an open file leaves the other tab marked saved; action playback Save As overwrites the played file; open | Work only on copies in `work\`; never Save As onto a file that is open |
| PhotoCraft #6790 | Red or garbage blocks on Intel Iris Xe (DX12); open, high | Intel GPU: try `--safe-gpu` |
| PhotoCraft #6114, #6163 | Large PSB or large files crash; open, critical | Keep canvases at about 8.6 MP as advised |
| VectorCraft #2414 (PR #2480) | CSS classes dropped on SVG export; open | Unchanged contract (ids and `data-*` only) |
| VectorCraft #2243 | Windows 11, 0.9.0, Intel UHD 605: APPCRASH in `igd12umd64.dll` before the window; open, critical; PR #2298 landed (next start skips the crashed adapter; "the first start may still crash, the second should open"); untested on that GPU | Intel integrated GPU: expect one failed first start; `WGPU_BACKEND` documented in section 7 |
| VectorCraft #2141, #2196, #2460 | Freeze, then a crash, on Save As PDF; crash on select-all in an opened PDF; open, critical. The #2141 reporter later retracted the data-loss claim: the restore prompt recovered the work "perfectly" | Make PDFs with the CLI (`run --export x.pdf`), not Save As PDF in the GUI. Save SVG normally |
| VectorCraft #2707, #2096 | Export as TIFF and as JPEG problems; open, critical | We export PNG and PDF; add a PNG check to the acceptance test (already there) |
| LightCraft #2198 | "Does not preview or open TIFF files from photolab scans": "malformed TIFF data: decoder limits exceeded"; open, critical (2026-10-17); re-saving in Photoshop works | **Scan path blocker, see below** |
| LightCraft #1983, #2090 | Same limit on a 138 MB 16-bit RGB single-strip TIFF (3923x5877); "100+ MB TIFF fails, 80 MB works" (Windows 11 and macOS); open | Same |
| LightCraft #1944, #2122, #1501 | `keyword.export` can overwrite any file including originals; library files written through planted symlinks; Move removes originals before the destination is durable; open | We use `mode: add` only, no keyword export, no Move |
| LightCraft #2124 | A damaged `catalog.log` line makes library open hang (quadratic resync); open | Back up the library folder before big runs |
| LightCraft #1726, #1337, #1323 | Exporting several RAW files freezes the system; crash on export (0.6.0); open | We export TIFF/JPEG from scans, not raw; pilot first |
| LightCraft #1318, #1396 | Windows 11 mixed-DPI window jump; Lrcat import progress bar hang | Not on our path |

**The TIFF limit in numbers** (my arithmetic; the limit is 128 MiB = 134,217,728 bytes per strip or tile, per the contributor's diagnosis in #2198/#1983, not checked in the `tiff` crate itself):

| Scan | Pixels | Raw size (16-bit RGB = 6 bytes per pixel) | Single strip passes? |
|---|---|---|---|
| 4x6 in at 600 ppi | 2400x3600 | 51.8 MB | yes |
| 5x7 in at 600 ppi | 3000x4200 | 75.6 MB | yes |
| 8x10 in at 400 ppi | 3200x4000 | 76.8 MB | yes |
| 8x10 in at 600 ppi | 4800x6000 | 172.8 MB | **no**, if written as one strip |
| the #1983 file | 3923x5877 | 138.3 MB | no (matches the report) |

Issue #2090's "80 MB works, 100+ MB fails" does not match the 134 MB figure; the reporter gave no dimensions, so the threshold there is unexplained. The failure is about one strip or tile, so compressed or multi-strip TIFFs (small `RowsPerStrip`) should avoid it; I did not test this. **Actions:** (1) put the largest planned scan into the LightCraft pilot and check it opens; (2) read each scan's strip layout with `exiftool` (`RowsPerStrip`, `StripByteCounts`, `Compression`) before importing; (3) if a scan fails, set the scanner software to tiled or small-strip output, or rewrite it (for example with ImageMagick `-define tiff:rows-per-strip=...`, a define I know from general use and did not test here) before import, and never overwrite the master; (4) watch PR #1989 (open; its reviewer flagged that the new cap is lower than the old one for small `max_pixels`).

**Answer to the original Q7 (open crash and data-loss issues).** There are many open reports, mostly new (the oldest in these lists are 9 days old) and many unconfirmed. Those that hit our chosen path are in the table above. None is a confirmed, unfixed silent loss of an ORA file at `v0.10.0` (the one found, #3806, is closed; #7018 loses locks, not pixels). The two Windows start-up crashes (#6249 stripped Windows, #2243 Intel UHD 605) and the TIFF limit are the ones to test for on the maker's PC.

---

### R5. Inkscape as the VectorCraft fallback (Q4)

**Test run (container, Inkscape 1.2.2, `b0a8486541`, 2022-12-01), on `research/craft-visual-fixtures/at-rig.svg`** [63]:

```
inkscape at-rig.svg --export-plain-svg --export-filename=out-plain.svg
inkscape at-rig.svg --export-type=svg --export-filename=out-inkscape.svg
python3 -I check_ids.py at-rig.svg out-plain.svg      # exit 0
python3 -I check_ids.py at-rig.svg out-inkscape.svg   # exit 0
inkscape at-rig.svg --actions="select-by-id:sun-group;transform-translate:12,7;export-filename:out-moved-plain.svg;export-plain-svg;export-do"
python3 -I check_ids.py at-rig.svg out-moved-plain.svg  # exit 0
```

| Check | Inkscape 1.2.2 Plain SVG | VectorCraft (first-pass tests) |
|---|---|---|
| Authored ids (11: `scene, bg, sun-group, sun, sun-halo, tree, trunk, leaf-1, leaf-2, caption, faded`) | all kept | kept if Object IDs = Layer Names |
| `data-pivot`, `data-z` on groups | unchanged | kept (v0.8.0+) |
| `class="glow"` and `<style>` text | **kept verbatim** (`check_ids.py`: `<style> kept verbatim: True`) | lost |
| Root `viewBox` `100 50 400 300` | **unchanged** | rewritten to `0 0 W H` |
| Filters (`feGaussianBlur`, `feColorMatrix`), `mask`, `clipPath`, `symbol`/`use`, live `<text>` | all present in the output | `feColorMatrix` ignored |
| `sodipodi:` / `inkscape:` attributes | none in Plain SVG (0 matches); the `sodipodi` and `inkscape` namespaces are declared in the Inkscape SVG variant | none |
| Ids on elements that had none | **added** (`svg37`, `style2`, `defs24`, `stop4`, `rect9`, ...) | only named objects get ids |
| A move with `transform-translate` | the group gets `transform="translate(12,7)"`; ids and `data-*` intact | transforms are baked into coordinates |

Findings: (1) For the id/`data-*` gate the fallback passes and keeps more than VectorCraft does (classes, style, viewBox origin). (2) The `GtkRecentManager` warning on stderr is harmless in headless mode. (3) A moved group carries a `transform`, which conflicts with the "no transform on animated groups" rule: either apply the move to the coordinates (Inkscape has a "Store transformation" preference in Behavior, Transforms; I named it from memory and did not test it) or re-check `data-pivot` after the edit.

**Pitfall (read from the installed extension, not run).** Inkscape's *Optimized SVG* output (`org.inkscape.output.scour_inkscape`, `/usr/share/inkscape/extensions/output_scour.inx`) has **"Remove unused IDs" on by default** and "Preserve manually created IDs not ending with digits" on by default. So an unreferenced id that ends in a digit, such as `leaf-1`, would be removed, while `sun-group` would survive. Use **Plain SVG** or **Inkscape SVG**, never Optimized SVG, for rigs. `scour` is not installed here, so I did not run that output.

**Windows steps for the maker** (Inkscape 1.x is a separate download; I did not verify a Windows build): File, Save As, "Plain SVG (*.svg)"; or from PowerShell `inkscape.exe in.svg --export-plain-svg --export-filename=out.svg` (the 1.2.2 `--help` text: "-l, --export-plain-svg: Remove Inkscape-specific SVG attributes/properties"). **Not done:** the GUI Save As dialog itself, and any Inkscape 1.3 or 1.4 behaviour (the container has 1.2.2). Upgrade the Risks-table cell for VectorCraft from "Inkscape (not researched here)" to "Inkscape 1.2.2 Plain SVG: id/data-*/class/style/viewBox kept on the fixture [63]".

---

### R6. `photocraft-cli serve` roots with Windows drive-letter paths (Q5)

Answer: **yes for the flags, with these rules; not run on Windows.** [61][62]

1. **Flags.** `serve` takes `--automation-read-root <dir>` and `--automation-write-root <dir>` (usage text and arg tables in `apps/photocraft-cli/src/lib.rs`, lines 44 to 47, 90 to 96) and builds `AuthorizedWorkspace::new(Path::new(root))` from them (line 238). The roots are trusted launch configuration; `Dir::open_ambient_dir` fails if the directory does not exist, so create `C:\lj\ch01\in` and `C:\lj\ch01\out` first. The `PHOTOCRAFT_AUTOMATION_*_ROOT` environment variables work only for the desktop process, not for `serve` or `mcp` (`docs/control-protocol.md` lines 342 to 346 at `v0.10.0`; lines 328 to 329 in the `v0.9.0` text I quoted before).
2. **Request paths.** Three forms are accepted: a relative path with forward slashes and no `:` (so no drive letter, no stream name), `a/b.png`; or an *absolute* path whose text lies beneath the root. `request_path` compares the absolute path to the root component by component; the drive-letter prefix is compared **without case**, every other component **with case**. On Windows both `C:\lj\ch01\in\L10_sky.png` and `C:/lj/ch01/in/L10_sky.png` parse. The rest is re-joined with `/` and checked like a relative path. Backslashes in a *relative* path are rejected ("alternate separators ... use `/`"); `..`, `.`, empty components, device names (`CON`, `COM1`...) and components ending in a dot or space are rejected; `C:/escape` and `name:stream` are rejected.
3. **Test.** `absolute_paths_beneath_the_root_are_translated_and_others_refused` (#2176, in `workspace.rs`) writes and reads through `to_string_lossy()` paths of its temp directory, once in the native spelling and once with `\` replaced by `/`, and refuses outside, sibling-lookalike, traversal and `:hidden` forms. It is a plain `#[test]`, so it runs wherever the test job runs. `ci.yml` runs Linux plus Windows (`windows-latest`, unit and integration legs) on `main`, manual runs and PRs that touch platform code. I did not check whether that job was green at `v0.10.0` (**UNVERIFIED**). The same test exists at `v0.9.0`; `workspace.rs` changed only in the ambient-path deny list between the tags.
4. **Gotchas to put in the recipe.** (a) Non-prefix components are compared case-sensitively, so with root `C:\lj\ch01\in` the request `C:\LJ\ch01\in\x.png` is refused although NTFS would accept it: **use relative paths in requests** (the recipe already does). (b) The write root and read root are independent; a request path is checked against its own root. (c) The parent of an output file must already exist; `doc.exportLayers` additionally refuses to overwrite existing files, so use a fresh `dir` each run. (d) `doc.save` to a path replaces the file atomically (temp file, sync, rename). (e) General PowerShell knowledge, not from the sources: Windows PowerShell 5.1 pipes text to native programs in the console code page, so keep layer and file names ASCII or use PowerShell 7; and a quoted argument ending in a backslash (`"C:\lj\in\"`) can swallow the closing quote in 5.1, so write roots without a trailing backslash.

No change is needed to the here-string in the PhotoCraft recipe beyond creating the two folders first and using relative request paths.

---

### R7. GIMP 3.0.x `.ora` export report (Q6) — confirmed in narrow form; reword before citing

**What I verified.**
- Forum thread "ora export" (gimp-forum.net, thread 10914), started 2025-05-31 by TheRambler, "GIMP 3.04 on Windows 11": layers exported to `.ora` came out with no transparency and no text, where GIMP 2.x worked. Reply by rich2005 (2025-05-31): "does look like a bug", reproduced by re-opening the exported file ("scrambled"), and MyPaint and Krita show the same result. On 2025-06-01 rich2005 filed GitLab issue **#14168** [74].
- GitLab #14168, title "Openraster export / open broken": GIMP 3.0.4 and 3.1.1 (AppImages), Kubuntu 24.04; exporting a mix of text and graphic layers to `.ora` and reopening gives a "scrambled image", text and layers broken; reporter suspects #14084. Labels "1. Bug", "3.0.4", "5. Plugins". The `.json` shows **state closed**, `updated_at` 2025-07-06, no milestone, no `closed_at` field [76].
- A second thread (2025-09-17, "ora format... it really works?") has a user on GIMP 3.0.x reporting layers cropped or misplaced in Krita, and rich2005 saying "I think fixed with Gimp 3.1.4 (maybe)" [75]. That is a forum guess.

**What I could not verify.** The fix version and the commit; whether GIMP 3.2 (the search results suggest a March 2026 release, and 3.0.8 in January 2026: search snippets only, **UNVERIFIED**) exports `.ora` correctly [78]. The first-pass note [56] was a search snippet; this replaces it.

**Verdict for playbook Decision 3.** Keep the claim, but write it as: "GIMP 3.0.4 had a reproduced `.ora` export bug (GitLab #14168: layers and text scrambled on reopen; Krita and MyPaint also showed it; issue now closed, fix version not found). Current GIMP 3.x behaviour is not tested; Krita remains the verified ORA fallback." Do not cite "GIMP 3.0.x loses transparency and text" as a general statement. If the maker has GIMP 3, `at-layers.ora` is a ready test.

---

### R8. Changes to make in the earlier sections and recipes

1. Summary item 2 and the pin paragraph in section 1: replace the pins with `v0.10.0`, `v0.13.1`, `v0.9.1` (R3d); keep the 2026-10-25 re-check.
2. Summary item 13 (data-loss guards): the ask-before-overwrite, read-only refusal and `%LOCALAPPDATA%` recovery fixes are now in `v0.10.0`.
3. Summary item 5 and the PSD paragraph: the vendor's Photoshop-oracle pass rose from 145 to 188 of 256 (73 percent, vendor figure [V]); open issues #6895, #6968, #6703 and #6311 still say PhotoCraft-written PSDs fail in Photoshop. The conclusion (PSD is private, hand-off is ORA and PNG) is unchanged.
4. Section 2 matrix, "Nested groups" row: add "write `isolation` explicitly; `v0.10.0` changes the default for files that declare 0.0.6 or newer". "Visibility, locks" row: add "locks do not round-trip exactly (#7018)".
5. Section 3 and the recipe: no change to commands; create the two root folders first; use relative request paths (R6).
6. Section 4 matrix: add rows "event attributes: kept (v0.13.1)", "`<script xlink:href>`: kept; inline `<script>`: dropped", and "class: still lost, #2414".
7. Section 6 and the LightCraft recipe: add the TIFF strip limit (R4) to the pilot and to the scanner settings; add "`render --settings x.lcpreset` works only from `v0.9.1`" as a reason not to pin `v0.8.0`.
8. Risks table: VectorCraft fallback cell, see R5; PhotoCraft cell: add the stripped-Windows start-up crash (#6249); LightCraft cell: replace "no scan corpus" with "no scan corpus and a known 128 MiB strip limit".
9. Open questions 2, 3, 9 and 10 are answered or narrowed here (R4, R2, R7, R5). Open question 1 stands: nothing was run on Windows.
10. Acceptance tests, add: PhotoCraft step 0 "run the PowerShell block in R2 and record the output"; VectorCraft step 3 "repeat the touch-up in Inkscape Plain SVG and run `check_ids.py`" (optional); LightCraft step 3 "include the largest scan, and read its strip layout first".

### R9. Still open or UNVERIFIED after this round

- Everything about the maker's PC (R2).
- No Craft app was run; every "works" is still from code and tests.
- Whether the Windows CI job was green at the three tags (R6).
- The Krita ORA corpus result on `v0.10.0` (R3a).
- Counts and titles from the trackers are second-hand summaries (R4); issue bodies were read only for the issues listed.
- The release feeds were read only up to the newest entry; notes for older tags (0.8.x, 0.12.0) were not.
- Inkscape: GUI Save As, Windows build, versions after 1.2.2, Optimized SVG output (R5).
- GIMP 3.2 `.ora` export (R7).
- `tiff:rows-per-strip` as a rewrite define, and the 128 MiB limit semantics for compressed strips (R4).

---

### Sources (round 1)

Repo files are read from local clones at the stated tags (GitHub HTML is reachable only through WebFetch). Web pages were fetched 2026-10-18.

[58] storytold/photocraft `git diff v0.9.0 v0.10.0` on `docs/ora.md`, `crates/io/src/ora.rs`, `crates/io/src/ora/tests.rs` — commit `8407d9c` "Release 0.10.0 (#7192)", 2026-10-17 21:28 -0400. Locator: https://github.com/storytold/photocraft/blob/v0.10.0/crates/io/src/ora.rs (constructed).
[59] storytold/vectorcraft `git diff v0.12.0 v0.13.1` on `crates/svg/src/{export,import,css}.rs`, `import/{files,fx,text}.rs`, `Cargo.toml`, `tests/{interactivity,data_attributes}.rs`, `crates/doc/src/xml_id.rs`, `crates/engine/src/cmd/fileio/svg.rs` — commit `904f0fe` "Release 0.13.1: retry stapler validate on Apple network errors", 2026-10-18 00:00 -0400. Locator pattern as above (constructed).
[60] storytold/lightcraft `git diff v0.8.0 v0.9.1` on `crates/engine/src/{export,presets,lib}.rs`, `cmd/{preset_files,develop}.rs`, `crates/codecs/src/tiff_codec.rs`, `apps/lightcraft-cli/src/main.rs`, `docs/{gaps,whats-new,xmp-interop}.md`, `docs/user/**`, `packaging/windows/*` — commit `4f0b110` "Release 0.9.1: the release web build installs the wasm-bindgen CLI", 2026-10-17 23:16 -0400.
[61] storytold/photocraft at `v0.10.0`: `crates/automation/src/{workspace.rs,headless.rs,rpc.rs}`, `apps/photocraft-cli/src/lib.rs`, `crates/engine/src/file_cmds.rs`, `docs/control-protocol.md` (lines 336 to 395) — roots, request paths, `doc.place`, `place_bytes`.
[62] storytold/photocraft at `v0.10.0`: `.github/workflows/ci.yml` — Windows legs on `main`, manual runs and platform-touching PRs.
[63] First-hand run, 2026-10-18, in the container: Inkscape 1.2.2 (`1.2.2-2ubuntu12`), its `--help`, and `/usr/share/inkscape/extensions/output_scour.inx`; commands in R5; fixture `research/craft-visual-fixtures/at-rig.svg` and `check_ids.py` (scratch outputs not kept).
[64] https://github.com/storytold/photocraft/releases.atom — WebFetch; first 100,000 of about 2.5 million characters; v0.10.0 entry dated 2026-10-18 04:02 UTC.
[65] https://github.com/storytold/photocraft/releases/tag/v0.10.0 — WebFetch; changelog entries on Windows, saving, ORA, PSD, GPU.
[66] https://github.com/storytold/vectorcraft/releases.atom — WebFetch; v0.13.1 entry dated 2026-10-18.
[67] https://github.com/storytold/lightcraft/releases.atom — WebFetch; v0.9.1 entry dated 2026-10-18 04:21 UTC.
[68] https://github.com/storytold/photocraft/commits/main.atom — WebFetch; 20 commits, 2026-10-15 to 2026-10-18.
[69] https://github.com/storytold/photocraft/issues , `/issues?q=is:issue is:open crash`, `...label:"priority: critical"`, `...("data loss" OR corrupt OR "lost work" OR overwrite OR "unsaved")`, `...(OpenRaster OR .ora OR "ORA file")` — WebFetch; counts in R4.
[70] https://github.com/storytold/photocraft/issues/6249 , /7252 , /7018 — WebFetch; issue pages (untrusted data). PR numbers #6395 and #7019 are as named on those pages, not opened.
[71] https://github.com/storytold/vectorcraft/issues (lists: critical 8, SVG words 51, crash words 22; total open 440), /2414 , /2243 , /2141 , and PR https://github.com/storytold/vectorcraft/pull/2480 — WebFetch.
[72] https://github.com/storytold/lightcraft/issues (lists: critical 13, windows/DX12/nvidia/intel/tiff words 128, crash words 38; total open 475), /2198 , /1983 , /2090 , and PR https://github.com/storytold/lightcraft/pull/1989 — WebFetch.
[73] https://getartcraft.com/apps/photocraft , /vectorcraft , /lightcraft — WebFetch; versions 0.7.0, 0.9.0, 0.6.0; Windows file names; no minimum Windows version stated ("Most Windows 10 and 11 PCs" for x64).
[74] https://www.gimp-forum.net/Thread-ora-export and https://www.gimp-forum.net/Thread-ora-export?pid=44468 — WebFetch; posts of 2025-05-31 and 2025-06-01.
[75] https://www.gimp-forum.net/Thread-ora-format-it-really-works?pid=45536 — WebFetch; posts of 2025-09-17.
[76] https://gitlab.gnome.org/GNOME/gimp/-/issues/14168 and https://gitlab.gnome.org/GNOME/gimp/-/issues/14168.json — WebFetch; title, versions, labels, state closed, `updated_at` 2025-07-06. The HTML page contained text addressed to AI agents; ignored.
[77] https://www.openraster.org/baseline/layer-stack-spec.html and /file-layout-spec.html — WebFetch (summarised); `isolation` default `isolate`, added in 0.0.4; non-isolated stack ignores its `composite-op`; spec version 0.0.6 on the file-layout page.
[78] Web search results (snippets only, pages not read): GIMP 3.0.6 news (https://www.gimp.org/news/2025/10/06/gimp-3-0-6-released/), GIMP 3.0.8 and 3.2 coverage — used only to say that no ORA fix note was seen; dates **UNVERIFIED**.
[79] `git ls-remote --tags --refs https://github.com/storytold/{photocraft,vectorcraft,lightcraft}` — 2026-10-18 05:26 UTC — newest tags `v0.10.0`, `v0.13.1`, `v0.9.1`.
[80] storytold/lightcraft at `v0.9.1`: `docs/user/getting-started/install.md`, `docs/user/faq/{free-and-private,supported-files}.md`, `docs/user/AGENTS.md` — Windows 11 install steps, Launcher, default library path, no-telemetry statement (pages say `verified: 0.7.1`).
