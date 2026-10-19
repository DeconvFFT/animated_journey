# SP2 verdict: Route A frame capture (headless Chromium, `seekTo(t)`)

*Sonnet implementor, Mon 19 Oct 2026, work package WP-04, branch `build/process-lock`. Evidence:
`build/evidence/wp04/*.json` (one envelope per test), `spikes/sp2_route_a/results.json` (the SP2
rows), `pipeline/bin/README-render.md` (how to run it). Re-run everything with
`bash spikes/sp2_route_a/run_sp2.sh`. Nothing here ran on Windows, and Route A does not need to.*

## Verdict

**Route A passes SP2 in the container, with one design change that the spike found and fixed and one open item: the guarded 2,400-frame disk stage is BLOCKED by the disk guard (the same run passed with its output in RAM; see (f)).**
The rule of R11 is: at least 8 fps on a flat scene, at most 100 differing pixels per frame
between two runs, no out-of-memory, resume works, tags correct. Measured (4 vCPU shared volume,
Chromium 141, ffmpeg 6.1.1, timed runs under `lj_bench`, load under the guard's limit):

| R11 item | Result | Number | Test |
|---|---|---|---|
| (a) flat scene speed | PASS | **11.8 fps** with one page (mark 8) | `a6_flat_fps` |
| determinism, at most 100 px | PASS, better than the rule | **0 differing pixels**: 48 of 48 frames hash-identical between two processes, with and without `?filter=1` | `a1_determinism` |
| negative control | PASS | `?random=1` differs in about 511,000 pixels per frame, so the test would catch a nondeterministic scene | `a2_negative_control` |
| no OOM | PASS | peak 0.7 GB (browser tree) for one page, 1.1 GB for four; the 2,400-frame piped run peaked at 1.9 GB summed (browser tree 1.2 GB, x264 0.6 GB; RSS double-counts shared pages) with four pages, of 15 GB | `a6_*` |
| resume works | PASS | SIGKILL at 120 of 240 frames, truncated frame and stale `.tmp` planted, rerun finishes, 240 frames hash-equal to an uninterrupted run, no `.tmp`, no browser left behind; shards 0/2 + 1/2 equal a single run; a second invocation renders 0 frames; `--max-seconds` soft cap resumes | `a4`, `a3`, `max_seconds_resume` |
| tags correct | PASS | `ffprobe`: 1920x1080, 24/1, 48 frames, yuv420p, tv, bt709 for matrix, primaries and transfer, High profile | `a5_chain_output` |

SP2 subset as justified in the plan: (a), (d), (e), (f), (g) as specified; (b) rough.js is replaced
by the seeded-LCG texture with a float-precision push and its GSAP twin (identical frames, 0 differing
pixels on 12 sampled frames); **(c) the three.js voxel diorama is dropped under D-29**, and a
WebGL/SwiftShader smoke (one CSS 3D plane and one raw WebGL triangle) runs at 5.3 fps with a working
SwiftShader context. Nothing was run for the dropped diorama, and if hero shots later need three.js, SP2 (c) is re-opened then.

## Speed marks (what a shot costs)

| Scene | 1 page | 2 pages | 4 pages | Note |
|---|---|---|---|---|
| flat SVG, 1920x1080 (`flat.html`) | 11.8 fps | 17.9 fps | 22.6 fps | frames identical at every level |
| full test card (`scene.html`: full panel texture, text, grid) | 7.7 fps | | 11.4 fps | PNG about 314 KB a frame |
| WebGL + CSS 3D smoke (`smoke3d.html`) | 5.3 fps | | | SwiftShader |

At 24 fps a film minute is 1,440 frames: about 2 minutes of render for a flat scene on one page
(1 minute at four pages), about 3 minutes for a heavy full-frame scene on one page (2 minutes at four).
Four pages are the sweet spot on 4 vCPUs (about 2 times one page, not 4 times: the cost is the
frame readback and PNG encode, not the script). Where the pixels come out of Chromium is the
bottleneck, so nothing in a scene's own code changes these numbers much.

(e) `a6_concurrency`: frames are hash-identical at 1, 2 and 4 pages. (f) the 2,400-frame (100 second) chapter is piped into ffmpeg with the
H.264 venue chain from `pipeline/lib/chains.json` and **never writes a PNG**: **2,400 frames in 118.3 s (20.3 fps, four pages), output 4.43 MB, zero PNG or `.tmp`
files seen anywhere** (the test samples every 2 s), 2,400 frames at `nb_frames` 2400, 24/1, yuv420p. **Caveat on how (f) was run:** the plan makes it one
`lj_with_disk 250` stage. The guard refused it (the shared volume had 273 to 403 MB free during this work, the rule needs Avail minus planned at least 400 MB;
the planned figure was recomputed from a measured 240-frame clip, 12 MB, and was still refused) and it waited 10 minutes for headroom, so **`a6_chapter_2400`
is BLOCKED** and stays so until it is rerun with `bash tests/render/run_tests.sh --all --only a6_chapter_2400` when Avail is at least 415 MB. Because the run writes
only its 4.4 MB output, `a6_chapter_2400_ram` ran the same command with the output in RAM-backed `/dev/shm`, so the volume was not touched, still under `lj_bench`.
An earlier run of the guarded stage on the same day, before `chains.json` landed and with the plain Q-F1 chain, passed (2,400 frames in 111.9 s, 21.5 fps, 4.43 MB,
guard ledger minimum 341 MB while other jobs wrote to the volume); its evidence file was overwritten by the later BLOCKED run, so it is quoted here as history, not as proof.

## What the spike found (these change how Route A is used)

1. **A frame's edge pixels depended on the frames rendered before it.** With R7's Chromium flags, a flat SVG
   scene rendered by one page and by four pages differed in **58 to 64 of 96 frames** (a few anti-aliased
   edge pixels each), and a killed-and-resumed run did not equal an uninterrupted one, so A3 and A4 could not
   have passed on that scene. Chromium re-rasterises only the damaged rectangle ("partial raster"), so the
   result depends on history. The full test card happened not to show it, which is why the harness has a flat
   scene. **`--disable-partial-raster --disable-gpu-compositing` removes it** (software compositing, the same
   pixels in any frame order; WebGL still runs on SwiftShader) and is about 50% faster (7.8 to 11.9 fps on one page)
   because the readback through SwiftShader Vulkan was the cost. Both flags are in the harness defaults; the
   test `history_independence` proves 0 of 96 frames differ with them and that 62 of 96 differ without them
   (`PW_DROP_FLAGS` is the control). **For research/agent-pipeline.md R7 and the pipeline skill (WP-11b stages it):**
   "frames are identical per machine" holds only with these flags.
2. **The MO8 gate needs a texture it can measure.** A synthetic panel of random hairlines, dense hatch fields and
   converging lines read 0.04 to 0.12 px of "jitter" even for a perfect transform push, because fine structure at
   the pixel grid aliases when resampled. A posterised smooth value-noise field (10 levels per channel through a 5-6-5
   grid, three octaves) plus a few hundred crisp hairlines reads **MO8a 0.0023 px and MO8b 0.0039 px** for
   `?push=transform` (limits 0.05 and 0.04) and **0.242 and 0.450 px** for `?push=layout` (the negative control).
   A11 was run here ahead of WP-11b with `pipeline/validators/mo8_gate.py`: transform exits 0, layout exits 1.
   The frame set for the gate is `?view=detail` (the texture alone, full frame, 48 to 96 frames).
3. **Fonts: "document.fonts.check is true" proves little.** It also returns true when no face matches the text
   (a Devanagari string in a Latin-only family). The A7 test therefore renders each string loaded and with the
   font files blocked, compares ink masks cropped to their bounding boxes (the primary font's metrics move the baseline
   between a loaded and a fallback render, which hides an unchanged glyph shape if the masks are compared in place:
   the unaligned IoU of the control was 0.50, the aligned one 1.00), and compares the loaded ink with a Pillow-raqm reference.
   Latin and Devanagari pass (aligned IoU 0.19 to 0.55 against 0.8 allowed; loaded ink 0.96 to 1.00 of the reference
   against 0.5 required); the control fails (a) as required; six scripts are listed NOT TESTED because they have no
   strings. Adding a script is proved end to end with Tamil digits on a throw-away copy (`a7_add_script`).
4. **F-09 was real and is fixed.** The R7 static server joined the request path onto the root: the test reproduces a
   leak of a file above the root with the unfixed handler, and gets 404 for all 13 traversal, backslash and symlink request forms tested (encoded, double
   encoded, backslash, symlink, mount escape) from the fixed one; the server listens on 127.0.0.1 only and checks `Host`.
5. **Network off works and is loud.** `?net=1` exits 2 naming `https://example.invalid/lj-net-probe.png`; the browser also
   resolves nothing but loopback.
6. **Resume cannot trust old frames from a different scene.** The harness stores a fingerprint of the scene (every file the
   server delivered up to `ready`, the page and query, fps, size) beside the frames and refuses a folder rendered by another
   scene (exit 2), because "skip frames that exist" would otherwise mix scenes silently.

## What this does not show (UNVERIFIED or open)

* **Cross-machine determinism** is not claimed: frames are identical per machine, Chromium build and font set. The 100-pixel
  tolerance is for comparing across environments.
* **Windows**: nothing ran; Route A runs in the container (W-23).
* **The guarded 2,400-frame stage is BLOCKED** by the disk guard (shared volume under 415 MB free); the RAM-output fallback passed. Rerun the guarded stage when there is room.
* **Heavy 3D (three.js) and Blender**: not measured here (dropped and SP3). **GSAP's licence** is recorded in
  `pipeline/lib/licences/gsap-LICENSE.txt` (the package ships no licence file; the text was read from the vendor page on 2026-10-19);
  it is used at build time for the ease only and nothing of it ships in the film. The maker or orchestrator should read it once before any web keepsake that would ship GSAP.
* **Indic fonts beyond Devanagari and (on a throw-away copy) Tamil**: the other five packages are only confirmed to exist on npm
  (`pending_O-10`); glyph coverage is checked when the reader supplies strings.
* **A person has not read the Devanagari strings**: `checked_by_reader` is `false` for all of them until the maker confirms.

## Decision for the plan

Route A stays the default for drawn and typographic scenes in the container, at the speeds above, with the two flags,
the fingerprint guard and the network-off rule as the harness's defaults. Fallbacks (HyperFrames, Remotion, the PC) are not triggered.
Per-shot budgets should use the measured fps (a heavy full-frame shot costs about 3 minutes of render per film minute on one page).
