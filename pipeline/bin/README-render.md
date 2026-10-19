# render.mjs: the Route A seek-capture harness

Renders a web scene frame by frame. The scene exposes `window.seekTo(t)`; the harness steps `t` in
`1/fps` seconds, takes a PNG screenshot of headless Chromium after two animation frames, and either
writes `f_000000.png`, `f_000001.png` ... (resumable, shardable) or pipes the frames straight into
ffmpeg. Output is 1920x1080 at 24 fps, tagged BT.709 when encoded. It runs in the cloud container
(Route A, decision W-23); the maker's PC is not needed for it.

Status: built and tested by work package WP-04 (spike SP2). Evidence is in `build/evidence/wp04/`,
the verdict in `spikes/sp2_route_a/VERDICT-SP2.md`. Nothing here has been run on Windows.

## Run it

```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers          # never run "playwright install"
bash pipeline/lib/fetch_libs.sh                           # once: GSAP and the test fonts into vendor/ (git-ignored)

# 2 seconds of the test card as PNG frames (48 frames), with a report
node pipeline/bin/render.mjs --dir pipeline --page scenes/testcard/scene.html --mount /vendor=vendor \
     --out renders/wp04/a --seconds 2 --json renders/wp04/a.json

# the same, piped into ffmpeg with the built-in H.264 chain (no PNGs on disk)
node pipeline/bin/render.mjs --dir pipeline --page scenes/testcard/scene.html --mount /vendor=vendor \
     --seconds 2 --chain h264 --ffmpeg renders/wp04/a.mp4

# a long shot in two shards, then one encode (shards are PNG only; they can run at the same time)
node pipeline/bin/render.mjs ... --frames 0:240 --shard 0/2 --out renders/x &
node pipeline/bin/render.mjs ... --frames 0:240 --shard 1/2 --out renders/x &  wait
node pipeline/bin/render.mjs ... --frames 0:240 --out renders/x --encode --chain h264 --ffmpeg renders/x.mp4

# look at a scene in a browser (serves --dir and mounts on 127.0.0.1 only and prints the URL)
node pipeline/bin/render.mjs --dir pipeline --mount /vendor=vendor --serve --serve-seconds 300
```

`bash tests/render/run_tests.sh --quick` (about 30 s) or `--all` (several minutes, timed runs under
`lj_bench`, the 2,400-frame run under `lj_with_disk`) checks all of it.

## What a scene must do

* Define `window.seekTo(t)` where `t` is seconds. It must be a **pure function of `t`**: same `t`,
  same picture, in any order. No `Date.now()`, no `Math.random()`, no CSS animation or timer that
  runs by itself (use a seeded generator; the test card shows one). It may return a promise.
* Set `window.ready = true` when fonts and images are loaded, or `window.readyError = "why"` if it
  cannot (the harness stops at once and prints the reason).
* Optional: `window.ljReport()` returns a JSON-able object that is copied into the `--json` report.
* Be self-contained: every file must come from `--dir` or a `--mount`. **The network is off.**
* Slow pushes: write `style.transform = 'scale(' + s + ')'` at full float precision; GSAP may supply
  the ease only (a paused timeline, `tl.time(t, false)`, `onUpdate` writes the transform); no
  `will-change`, no `force3D`; never animate `width`, `height`, `left` or `top` (W-41; the test
  card's `?push=layout` shows what that does to the MO8 numbers).

## Options

| Option | Meaning |
|---|---|
| `--page P` | scene page, relative to `--dir` or a mount, query string allowed (required) |
| `--dir DIR` | folder served at `/` (default `.`) |
| `--mount /u=DIR` | also serve `DIR` at `/u` (repeatable). The page can read nothing else |
| `--out DIR` | PNG frames `f_%06d.png` (default `frames`) |
| `--fps N` | default 24 |
| `--w N --h N` | viewport, default 1920 x 1080 |
| `--seconds S` or `--frames A:B` | frames `0 .. round(S*fps)-1`, or the range `[A, B)` (default 1 second) |
| `--shard i/n` | render frames with `frame mod n == i` (shards never overlap) |
| `--concurrency N` | pages used in parallel, 1 to 8. In video mode a reorder buffer keeps frames in order |
| `--alpha` | transparent background, RGBA frames; the scene must not paint its own background (test card: `?alpha=1`) |
| `--chain NAME` | encoding chain from `pipeline/lib/chains.json` (WP-05). `h264` means the file's `h264_venue`; when the file is absent the built-in `h264` (an equal copy) is used. Needs `--ffmpeg`/`--video`, or writes `OUT/video.EXT`. The encoded file is probed and checked against the chain's `expect` block (exit 1 on a mismatch) |
| `--ffmpeg OUT`, `--video OUT` | the video file. Frames are piped, the shot runs in one process, no `--shard` |
| `--encode` | do not render: pipe the existing PNG frames of `--out` for the range into the chain |
| `--json FILE` | report: frames rendered and skipped, seconds, fps, **peak RSS**, Chromium and Playwright versions, chain, scene fingerprint, **SHA-256 of every frame**, page errors, blocked requests |
| `--max-seconds S` | soft cap for container foreground limits: after `S` seconds finish the current frames, print a resume hint, exit 0 (PNG mode) |
| `--fail-on-pageerror` | stop at the first uncaught page error: exit 2 and remove this run's output |
| `--overwrite` | ignore existing frames and the scene fingerprint, render everything again |
| `--ready-timeout S`, `--frame-timeout S` | defaults 60 and 120 |
| `--serve [--serve-seconds S]` | only serve, print `{"serving": URL}` |
| `--chains-file F`, `--ffmpeg-bin F`, `--list-chains`, `--quiet`, `--help`, `--version` | as named |

Environment: `PW_PATH` (the playwright module folder), `PW_CHROMIUM` (browser executable; default
`/opt/pw-browsers/chromium`), `FFMPEG`. Experiments only: `PW_EXTRA_FLAGS` appends Chromium flags and `PW_DROP_FLAGS` removes
default ones; the report lists the flags actually used.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | done (also: `--max-seconds` soft cap reached; the report says `complete: false` and how to resume) |
| 1 | the encoded file does not match the chain's expected tags, size or frame count; or an internal error |
| 2 | bad usage, or the scene is broken: a request to any host but the local server (the URL is named), `seekTo` threw, a local file answered 404, the page never became ready, or an uncaught page error (the run finishes first unless `--fail-on-pageerror`) |
| 3 | environment problem: Playwright or Chromium or ffmpeg not found, time cap in video mode |
| 130, 143 | stopped by SIGINT or SIGTERM; finished frames are kept |

On exit 2 or 3 the output of **this run** is removed (the frames it wrote, `.tmp` files, a partial
video) and the report records `output_removed`. Frames written by earlier clean runs are untouched.

## What makes it deterministic, resumable and safe

* **Chromium flags** (fixed, listed in the report): `--force-device-scale-factor=1`,
  `--hide-scrollbars`, `--disable-lcd-text`, `--font-render-hinting=none`,
  `--force-color-profile=srgb`, SwiftShader for WebGL (`--use-gl=angle --use-angle=swiftshader
  --enable-unsafe-swiftshader --ignore-gpu-blocklist`), **`--disable-partial-raster
  --disable-gpu-compositing`**, no background throttling, no proxy, and a host-resolver rule that
  resolves nothing but loopback. The two bold flags remove *history* from the pixels: without them
  Chromium re-rasterises only the damaged rectangle, so the edge pixels of anti-aliased shapes
  depend on the frames rendered before (a flat SVG scene rendered by 1 page and by 4 pages differed
  in 58 to 64 of 96 frames; a killed and resumed run did not equal an uninterrupted one). With them
  sharded, concurrent, resumed and sequential runs are bit-identical, and capture is about 50%
  faster here (`history_independence` is the test, with the two flags dropped as its control). Locale `en-US`, time zone UTC, service
  workers blocked. Two `requestAnimationFrame` waits before every screenshot.
* **Frames are identical per machine, Chromium build and font set**, not across machines. Compare
  across environments with `compare -metric AE -fuzz 1%` and at most 100 differing pixels.
* **Resume.** A frame is written to `f_NNNNNN.png.tmp` and renamed, so a kill never leaves a half
  frame; at the start the harness removes stale `.tmp` files of its own shard and re-renders any
  existing frame whose PNG is incomplete. `.render-meta.json` holds a fingerprint of the scene
  (every file the server delivered up to `ready`, the page and query, fps, size, alpha); a folder
  rendered by a different scene is refused (exit 2) so resume can never mix scenes. `--overwrite`
  replaces it.
* **Path safety (F-09).** The server binds `127.0.0.1` only, answers only GET and HEAD with the
  right `Host`, rejects any request whose decoded path has a `..` segment, any backslash or NUL,
  anything that resolves outside `--dir` or a mount, and any symlink that leads out (all 404).
* **Network off.** Every request that is not to the local server is aborted and the run exits 2,
  naming the URL. Scenes must be self-contained.
* **No secrets, no identity.** The report holds no user name, host name or absolute path (paths are
  shown relative to the working folder).

## Known limits (recorded, not hidden)

* Video mode is one process (no shards) and cannot resume; its `--max-seconds` is an abort (exit 3).
  Render PNG shards and use `--encode` for long shots.
* A frame costs one PNG encode plus (in video mode) an x264 encode competing for the same 4 vCPUs;
  speed numbers are in `spikes/sp2_route_a/VERDICT-SP2.md`.
* Windows: not run. The harness is for the container (W-23); nothing in it needs the PC.
* The built-in `h264` chain must equal `h264_venue` in `chains.json` (WP-11b asserts it).
