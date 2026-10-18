---
name: craft-apps-visual-refinement
description: Use when a Life Journey task makes or checks PhotoCraft layered stills (OpenRaster .ora and PSD hand-offs), VectorCraft SVG animation art (stable ids and data attributes), or LightCraft scan batches (CLI scripts and .lcpreset files), or when the maker asks how to touch up Life Journey files in the ArtCraft apps. It covers version pins, the five-minute acceptance tests, read-backs, privacy rules and fallbacks.
---

# Craft Apps Visual Refinement

## Purpose

Turn the three ArtCraft visual apps (PhotoCraft, VectorCraft, LightCraft) into three narrow hand-offs for the Life Journey pipeline. Claude generates the starting file. The maker makes the human touch-up in the app. Claude reads the result back and gates it. VectorCraft's trace presets (Sketched Art, Line Art and Black and White Logo) turn a scan of her handwriting, a recipe card or a letterhead into SVG chapter titles lettered in her own hand. LightCraft presets are authored and named per decade or film stock, so each decade keeps its own colour instead of every print getting one uniform restored look (charter principle 3).

Nothing in these apps has been run on a Windows PC yet. Treat every command here as untested until the playbook's Exercise 1 passes.

## When to use / when not to

Use it when:
- A layered still must be prepared for a hand touch-up in PhotoCraft, or a returned PhotoCraft file must be read back.
- SVG animation art must be prepared for VectorCraft, or ids must be checked after a VectorCraft save.
- A scan batch must be prepared for LightCraft, or its outputs read back.
- A version pin, install type or acceptance-test result must be checked.
- The maker needs a written touch-up sheet for one of the apps.

Do not use it when:
- The work is pure generation with no Craft app in the loop. Use the agent-pipeline track.
- The job would send real family material into the cloud container. Write the script and hand it to the maker to run on the PC. Scripts travel; scans do not.
- The task concerns FilmCraft, EffectCraft, SoundCraft or the Craft Launcher. Those belong to other tracks, or are out of scope.
- Someone asks about the hosted ArtCraft studio (the notes name it as app.getartcraft.com). It is separate, has cloud generation and its own pricing, and was not researched.
- Someone asks to upload, publish or share a file from these hand-offs that holds personal material.

## Procedure

1. **Classify the job.** Stills go to the PhotoCraft hand-off (steps 5 to 8). Vector art goes to the VectorCraft hand-off (steps 9 to 12). Scan batches go to the LightCraft hand-off (steps 13 to 15). If the job fits none of these, stop and say so.
2. **Check the privacy class.** If the input is real family material, container work uses only synthetic or non-personal test files. Anything that touches the real files runs on the maker's PC.
3. **Check the pin.** Read the hand-off log for each app's version and install type. If there is no entry, ask the maker to run `--version` and record it (playbook, Step 1). PhotoCraft must be v0.9.0 or newer for ORA work, because 0.7.0 lacks the no-overwrite guard. Also confirm the version passed the acceptance test (Template B in the playbook).
4. **Name everything before you write a file.** ORA layer names are the pipeline ids (for example `L10_sky`, `L20_figure`). SVG ids match `[A-Za-z][A-Za-z0-9._-]*`, are unique, and contain no spaces. On import, other characters become `_`, so choose clean names from the start.
5. **Build the stills file.** Preferred: write the ORA with the standard-library script `research/craft-visual-fixtures/make_ora.py`. The stack lists layers top first. Use 8-bit sRGB PNG layers at canvas size or smaller, with x and y offsets. Set each layer's blend with `composite-op`, for example `svg:multiply`. Prefer a flat layer list. If you use a `<stack>` group, write `isolation="isolate"` or `"auto"` explicitly: v0.10.0 changed how a group is read when the file declares version 0.0.6 or newer, and an omitted `isolation` then means isolate. `make_ora.py` declares 0.0.3, which PhotoCraft v0.9.0 and v0.10.0 both read the old way. Layer locks do not round-trip exactly (#7018), so never encode anything in a lock. [4][10][58][70]
6. **Optional, untested: headless build.** Send JSON lines to `photocraft-cli serve` on stdin: `doc.new`, then `doc.place` (`smartObject:false`, `fit:false`, `scale:100`), then `engine.execute` with `layer.setProps`, then `doc.save` to a `.ora` name. Do not inline the JSON in a Windows command line. Use a here-string or a file. Quoting in Windows PowerShell 5.1 is a known risk; that is general knowledge, not verified in our sources. [8][9] Before you start `serve`, create the read and write root folders; it fails if one is missing (`Dir::open_ambient_dir`). Request paths are relative, with forward slashes; backslashes in a relative path are refused, and an absolute path is compared case-sensitively after the drive letter, so `C:\LJ\...` is refused. Write each root without a trailing backslash in PowerShell 5.1 (general knowledge). [61]
7. **Write the maker's touch-up sheet.** It says: open the copy in `work\`; do not rename layers; which layers may change; the save target; that an adjustment layer, text, a layer style or a vector mask makes PhotoCraft write a PSD instead of overwriting the ORA; and where to save back.
8. **Read a returned stills file back.** Run `photocraft-cli info <file> --compact` for the layer tree, `photocraft-cli convert <file> <out.png>` for a flattened PNG, and `doc.exportLayers` for per-layer PNGs. `doc.exportLayers` refuses to overwrite, so give each run a fresh `dir`, and its request paths follow the relative, forward-slash rule in step 6 [61]. Check that every expected layer name is present, that opacity and blend match, and that every warning is recorded word for word. Some blend modes come back as Normal on export, so check them. [7][8]
   - PSD fallback, only when text or adjustment layers are essential: ag-psd 31.0.3 writes layered RGB PSDs without 16-bit, and psd-tools 1.25.0 writes "limited" PSDs. Supply a composite image with either one, and treat the PSD as a fallback input. [45][46][47][48]
9. **Build the SVG rig.** Give every moving element a clean, unique id. Put pivots in `data-pivot` and stacking in `data-z`, on g, path, rect, circle and similar elements, not on text. Use a viewBox that starts at `0 0 W H`. Do not rely on `class`, `<style>`, transforms on groups, SMIL, CSS animation, or any filter other than Gaussian blur, drop shadow, glow or feather. Those do not survive the import. [20][21][22]
10. **Pre-flight the rig.** Run `vectorcraft-cli convert in.svg rt.svg` and read `importWarnings`. Then run `python check_ids.py in.svg rt.svg`. Expect exit code 0, and expect the viewBox to become `0 0 W H`. [22][24]
11. **Gate the touched SVG.** After the maker's Save As, run `check_ids.py <source> <touched>`. Exit code 0 is the gate. A lost id or a changed `data-*` attribute fails it. Do not repair by hand. Report the failure.
12. **Re-add the animation hooks.** Add classes, the `<style>` block and the timeline (for example GSAP) by id and `data-*` attribute, after the touch-up. Keep the agent SVG as the source of truth, and diff it against the touched file. Export with `vectorcraft-cli run --in <touched.svg> --export <out.png> --export <out.pdf> --scale 2`. [24]
13. **Build the scan batch.** Write the `.lcpreset` as JSON: `{"format":"lightcraft.preset","version":1,"presets":[{id,name,group,settings}]}`. Its `settings` is a partial set of develop controls. Write a JSON-lines script with these steps: `library.import` with `mode:"add"` only; `preset.import`; `library.selectAll`; `preset.apply` with an id and an amount; and `app.export` with `format:"tif"`, `bitDepth:16`, `colorSpace:"srgb"`, a naming template and `conflict:"skip"`. The naming tokens are `{name}`, `{seq}` or `{seq:N}`, `{date:%Y-%m-%d}`, `{title}` and `{ext}`. The acceptance fixture `research/craft-visual-fixtures/at-lightcraft-steps.jsonl` runs this same 16-bit TIFF export as well as a JPEG, so Exercise 1 tests the master path. [33][34][42] Before the batch, the maker checks the strip layout of the largest scan with exiftool (`RowsPerStrip`, `StripByteCounts`, `Compression`). Pass only if every `StripByteCounts` value is below 134,217,728 bytes. LightCraft refuses a TIFF whose single strip or tile exceeds 128 MiB (issues #2198 and #1983; fix PR #1989 is open). If a scan fails, lower the scan resolution, or have the maker rewrite a copy with `magick in.tif -define tiff:rows-per-strip=64 -compress None out.tif` (tested with ImageMagick 6.9.12 in the container, not on Windows). Never overwrite the master. Put the largest planned scan into the 10-print pilot first. Stop and report if `library.import` returns a decoder-limits error. [72][83][84]
14. **Run it on the maker's PC with the GPU off.** Set `LIGHTCRAFT_GPU=0`, then run `lightcraft-cli run --library <local NTFS folder> --script <steps.jsonl>`. Every result line must say `"ok": true`. Any non-zero exit code is a failure to report. Never use the `move` import on scans, and never point an `--in-place` batch at originals. [34][36][42]
15. **Gate the scan tool.** LightCraft is the production scan tool only after the 10-print pilot against darktable (playbook, Exercise 5). Until then, run the same batch through darktable and report both. The darktable command line needs a config folder and a styles database first. [53]
16. **Log each step.** For every step, record the app and version, the input and output names with SHA-256 hashes, the changes made by hand, any AI-restored or generated label, and each warning word for word. Use Template A in the playbook.
17. **Report.** Give the list of files, the read-back results, the warnings, any open TODO(research) items, and any gate that failed. Do not carry on past a failed gate.

## Checklists

**Before handing a file to the maker**
- [ ] The input is a copy in `work\`, and the originals are read-only.
- [ ] Layer names or SVG ids are final and clean.
- [ ] The touch-up sheet names the save target and the settings.
- [ ] The version pin is in the log, and its acceptance test passed.
- [ ] PhotoCraft autosave is on. VectorCraft and LightCraft control ports are off.

**After the maker returns a file**
- [ ] The saved file was opened and read back (`info`, `convert`, or the checker).
- [ ] Any PSD offer is recorded, and the PNG exports come from the saved file.
- [ ] Output checksums are logged.
- [ ] Warnings are quoted word for word.

**Scan batch**
- [ ] Originals are referenced in place (`add`), never moved.
- [ ] The largest scan opens in LightCraft, with its strip layout checked (every `StripByteCounts` value below 134,217,728 bytes).
- [ ] The library is on a local NTFS disk, not in a synced folder, and only one process uses it.
- [ ] `LIGHTCRAFT_GPU=0` is set, and every result line says `"ok": true`.
- [ ] The neutral border point is recorded.
- [ ] Masters (16-bit TIFF) and JPEGs are logged with checksums.

## Quality bar

**Good**
- Names and ids survive the round trip. The ORA keeps names, opacity, blend and offsets. The SVG passes `check_ids.py` with exit code 0.
- The maker's change shows up in the read-back, and nothing else moved.
- Every command ran on a recorded version, and every warning is quoted.
- Scan outputs are 16-bit masters plus JPEGs, with checksums and a recorded neutral point.

**Mediocre**
- The work ran only in the container, on synthetic files, and has not yet run on the maker's PC.
- Warnings were paraphrased or ignored, and checksums are missing.
- The SVG depends on classes, `<style>` or SMIL surviving an app save.
- LightCraft was chosen without the pilot.

**Failing**
- Any silent overwrite or loss: an ORA replaced by a smaller file, a layer dropped with no warning, or a lost SVG id.
- A control port left on, a library on a network share or in a synced folder, or real family files sent to the container or any hosted service.
- Vendor headline numbers quoted as proof. "307 of 309", "88 percent", "134 of 135" and "61 percent" do not mean what they sound like. [3][30][44]

## Ethics and privacy guardrails

- Real family material stays on the maker's PC for these steps. Never upload it to the container, a cloud photo library, a hosted studio or a chat.
- AI-restored or generated content is labelled in the hand-off log, and the label carries into the manifest (charter principle 4; `playbooks/ai-imagery.md`). Never invent faces, events or words. Reconstructions must stay visibly reconstructions.
- Face recognition stays off, because faces of relatives are biometric data. Model downloads (SAM 3, AI denoise, faces, place names) and remote denoise stay off unless the maker asks for one at that moment and the log records it. [39]
- The `--control` ports of VectorCraft and LightCraft have no authentication. Turn them on only during a session, and never expose them to a network. [26][34]
- Traces are real: recovery autosaves, recent-file lists, thumbnail caches, logs and XMP sidecars. Clear them after each session and log what was cleared. A shared PC makes this matter more. [13][33][36]
- Never put the library or the scans in a synced cloud folder. The charter forbids any route that could tip her off.
- Never use LightCraft's `move` import, or PhotoCraft's `--in-place` batch, on original scans. [7][34]
- The Launcher README documents no off switch. Do not install or run the Launcher during production. Download the portable zip for the pinned tag from `github.com/storytold/<app>/releases/tag/<tag>` and check its SHA-256 against the `SHA256SUMS.txt` in that same release (`photocraft/docs/releasing.md` line 26; Launcher README).
- Do not cite a URL you have not opened. GitHub links in this skill are constructed from tag and path; mark them as constructed until someone opens them.

## References

- Playbook (exercises, templates, decisions): `playbooks/craft-visual.md`
- Research notes (hand-off matrices in sections 2 to 6, privacy in section 9): `research/craft-visual.md`
- Charter: `CHARTER.md`
- Fixtures: `research/craft-visual-fixtures/` (`make_ora.py`, `check_ids.py`, `at-layers.ora`, `at-rig.svg`, `faded-print-a.lcpreset`, `at-lightcraft-steps.jsonl`)
- Related playbook (labelling and scanner settings): `playbooks/ai-imagery.md`
- Product pages, fetched 2026-10-18: https://getartcraft.com/apps/photocraft , https://getartcraft.com/apps/vectorcraft , https://getartcraft.com/apps/lightcraft
- darktable command line: https://docs.darktable.org/usermanual/development/en/special-topics/program-invocation/darktable-cli/
- Krita command line: https://docs.krita.org/en/reference_manual/linux_command_line.html
- ag-psd README: https://raw.githubusercontent.com/Agamnentzar/ag-psd/master/README.md
- psd-tools usage: https://psd-tools.readthedocs.io/en/latest/usage.html
- ImageMagick formats (ORA is read-only): https://imagemagick.org/formats/

### Sources

*Link status.* The GitHub addresses are constructed locators, built from tag and path. The research container could not open github.com (403), so the researcher read the files in a local clone. Open each link before citing it outside this project. The getartcraft.com, darktable, Krita, ag-psd, psd-tools and ImageMagick pages were fetched by the researcher on 2026-10-18.

- [3] photocraft `crates/io/tests/corpus.rs`: floors 146/169, 236/308 and 145/258 (or /256), and what "oracle pass" and "round trip" mean. https://github.com/storytold/photocraft/blob/v0.9.0/crates/io/tests/corpus.rs (constructed locator)
- [4] photocraft `docs/ora.md`: ORA kept and lost table, no-overwrite rule (#3806), Krita 5.2.9 verification. https://github.com/storytold/photocraft/blob/v0.9.0/docs/ora.md (constructed locator)
- [7] photocraft `apps/photocraft-cli/src/lib.rs` and `book/src/automation/cli.md`: subcommands, `run --new`, `batch --actions`, usage. https://github.com/storytold/photocraft/blob/v0.9.0/apps/photocraft-cli/src/lib.rs (constructed locator)
- [8] photocraft `docs/control-protocol.md`, `docs/mcp.md`: bearer token, loopback, headless `serve` methods, limits, MCP tools. https://github.com/storytold/photocraft/blob/v0.9.0/docs/control-protocol.md (constructed locator)
- [9] photocraft `crates/engine/src/commands.rs` (with `file_cmds.rs` and `layer_multi_cmds.rs`): `file.new`, `file.placeEmbedded`, `loadFilesIntoStack`, `layer.setProps`, `layer.moveTo`. https://github.com/storytold/photocraft/blob/v0.9.0/crates/engine/src/commands.rs (constructed locator)
- [10] photocraft `crates/automation/tests/openraster.rs` (with `agent_tasks.rs`): layered ORA save test and scripted tasks. https://github.com/storytold/photocraft/blob/v0.9.0/crates/automation/tests/openraster.rs (constructed locator)
- [13] photocraft `docs/scorecard.md` (with `gaps.md`, `target-app-parity.md`, `hardware-parity.md`): readiness numbers, signing gap G17, performance baseline on macOS. https://github.com/storytold/photocraft/blob/v0.9.0/docs/scorecard.md (constructed locator)
- [15] photocraft `crates/format/src/autosave.rs`: autosave every 10 minutes, recovery on launch. https://github.com/storytold/photocraft/blob/v0.9.0/crates/format/src/autosave.rs (constructed locator)
- [20] vectorcraft `crates/svg/src/import.rs`: usvg options, labels, layer mode, `data-*` handling. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/src/import.rs (constructed locator)
- [21] vectorcraft `crates/svg/src/export.rs`: `sanitize_id`, the viewBox line, classes. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/src/export.rs (constructed locator)
- [22] vectorcraft `crates/svg/tests/ids.rs` (with `symbols_layers.rs`, `roundtrip.rs`, `options.rs`, `gradients.rs`, `prop_svg.rs`): id, rig, group, class and style tests. https://github.com/storytold/vectorcraft/blob/v0.12.0/crates/svg/tests/ids.rs (constructed locator)
- [24] vectorcraft `apps/vectorcraft-cli/src/main.rs`: `convert` (with importWarnings), `run`, `info`. https://github.com/storytold/vectorcraft/blob/v0.12.0/apps/vectorcraft-cli/src/main.rs (constructed locator)
- [26] vectorcraft `docs/control-protocol.md`: loopback, "no authentication", limits. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/control-protocol.md (constructed locator)
- [30] vectorcraft `docs/file-format-parity.md` (with `target-app-parity.md`): the 88 percent breakdown and the missing real-world corpus. https://github.com/storytold/vectorcraft/blob/v0.12.0/docs/file-format-parity.md (constructed locator)
- [33] lightcraft `docs/xmp-interop.md`: sidecars, `crs:` mapping, `.lcpreset` format. https://github.com/storytold/lightcraft/blob/v0.8.0/docs/xmp-interop.md (constructed locator)
- [34] lightcraft `apps/lightcraft-cli/src/main.rs` (with `docs/mcp.md`, `docs/control-protocol.md`): CLI usage, `run`, `render`, the port without authentication. https://github.com/storytold/lightcraft/blob/v0.8.0/apps/lightcraft-cli/src/main.rs (constructed locator)
- [36] lightcraft `crates/catalog/src/journal.rs` (with `lock.rs` and the repair tests): operation log, locking on shares. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/catalog/src/journal.rs (constructed locator)
- [39] lightcraft `crates/fetch/src/lib.rs` (with `model_download.rs`, `face_download.rs`, `cmd/geocode.rs`): network paths and opt-in downloads. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/fetch/src/lib.rs (constructed locator)
- [42] lightcraft `crates/engine/src/export.rs` (with `cmd/develop.rs`, `cmd/preset_files.rs`, `presets.rs`): export options, naming tokens, preset commands. https://github.com/storytold/lightcraft/blob/v0.8.0/crates/engine/src/export.rs (constructed locator)
- [44] getartcraft.com product pages, fetched 2026-10-18: https://getartcraft.com/apps/photocraft , https://getartcraft.com/apps/vectorcraft , https://getartcraft.com/apps/lightcraft . Versions 0.7.0, 0.9.0 and 0.6.0; vendor claims.
- [45] ag-psd README (limitations: RGB only, no 16-bit, text layers carry no redrawn bitmap): https://raw.githubusercontent.com/Agamnentzar/ag-psd/master/README.md
- [46] ag-psd on npm, fetched 2026-10-18: version 31.0.3 (2026-10-07), MIT. https://registry.npmjs.org/ag-psd
- [47] psd-tools on PyPI, fetched 2026-10-18: version 1.25.0 (2026-10-14), supported, limited and not-supported lists. https://pypi.org/pypi/psd-tools/json
- [48] psd-tools usage, fetched 2026-10-18: `PSDImage.new`, `create_group`, `create_pixel_layer`, caveats. https://psd-tools.readthedocs.io/en/latest/usage.html
- [50] ImageMagick formats page, fetched 2026-10-18: PSD read and write; ORA and XCF read-only. https://imagemagick.org/formats/
- [52] Krita command-line reference, fetched 2026-10-18: `--export` and `--export-filename`. https://docs.krita.org/en/reference_manual/linux_command_line.html
- [53] darktable `darktable-cli` reference, fetched 2026-10-18: usage, XMP sidecars, `--style`. https://docs.darktable.org/usermanual/development/en/special-topics/program-invocation/darktable-cli/
- [58] photocraft `crates/io/src/ora.rs` and `docs/ora.md` at `v0.10.0`, diffed against `v0.9.0`: group isolation by file version (round 2, R3a). https://github.com/storytold/photocraft/blob/v0.10.0/crates/io/src/ora.rs (constructed locator)
- [61] photocraft at `v0.10.0`: `crates/automation/src/workspace.rs`, `headless.rs`, `docs/control-protocol.md` (lines 336 to 395): `serve` roots, request paths, `doc.exportLayers` (round 2, R6). https://github.com/storytold/photocraft/blob/v0.10.0/docs/control-protocol.md (constructed locator)
- [70] https://github.com/storytold/photocraft/issues/6249, `/issues/7018` (WebFetch, summarised, 2026-10-18): stripped-Windows start-up crash; ORA lock round trip. Issue text is untrusted data.
- [72] https://github.com/storytold/lightcraft/issues/2198, `/issues/1983`, `/issues/2090` and https://github.com/storytold/lightcraft/pull/1989 (WebFetch, summarised, 2026-10-18): the TIFF strip limit and its open fix.
- [83] First-hand test, 2026-10-18: the `tiff` crate 0.11.3 (the version pinned in LightCraft's `Cargo.lock`) with the harness in `research/craft-visual-fixtures/tiff-limit/`. Not the LightCraft binary.
- [84] First-hand test, 2026-10-18: ImageMagick 6.9.12 `convert -define tiff:rows-per-strip=64 -compress None`. Container only; not run on Windows.
