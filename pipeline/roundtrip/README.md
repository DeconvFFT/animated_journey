# pipeline/roundtrip: emitters and validators for the Craft hand-offs (WP-06)

Synthetic-data tools for the three hand-offs the ArtCraft apps touch (D-11, D-12): layered stills as OpenRaster (`.ora`) for PhotoCraft, an SVG rig for VectorCraft, and
a 24 fps OpenTimelineIO file (`.otio`) with `metadata.filmcraft` for FilmCraft. Everything is generated at test time from test cards, a sine tone and a geometric rig. No
photograph, no family media, no deity image or text (build plan 4.10). Whether PhotoCraft, VectorCraft and FilmCraft accept and keep these files is **UNVERIFIED** here:
WP-10 (Linux CLIs) and the maker's Windows five-minute tests are the real evidence.

The project rate is 24 frames a second (W-14, S-01). The 25 fps E2 template of `research/craft-motion.md` R3 is rebased, not copied (see "OTIO" below).

## Run it

```bash
bash tests/roundtrip/run_tests.sh --quick    # about 10 s, no network
bash tests/roundtrip/run_tests.sh --all      # about 15 s; adds the plug-in adapter probe (pip, about 4 MB, throw-away venv)
bash tests/roundtrip/make_evidence.sh        # quick, all, the acceptance commands, summary.json (writes build/evidence/wp06/; tests_quick.jsonl and tests_all.jsonl are separate files)

# the venv for the optional library checks (about 16 MB on disk; outside the repo)
python3 -m venv <scratch>/venv-otio && <scratch>/venv-otio/bin/pip install --no-cache-dir opentimelineio==0.18.1
```

`<scratch>` is the folder beside the repository folder named `build-scratch` (in every committed file the build plan writes that literal path as `<scratch>`).
Tools run as `python3 -I` (`py -3 -I` on Windows). Exit codes follow build plan 4.3: 0 pass, 1 a check failed, 2 bad usage or invalid input, 3 environment problem.

## The tools

| File | What it does | Needs |
|---|---|---|
| `emit_ora_layers.py OUT.ora` | writes a layered still: `L30_label`, `L20_figure`, `L10_restored`, `L00_asfound` (bottom), 8-bit RGBA PNG layers, `mimetype` first and stored, `stack.xml`, `mergedimage.png`. Deterministic. | Pillow |
| `validate_ora.py FILE.ora` | the R8 ORA rules, one named check each; `--profile auto\|pipeline\|reference`, `--allow-offcanvas`, `--json` | standard library |
| `svg_rig.py gen\|plant\|gate\|finding` | the synthetic rig (17 authored ids, `data-pivot`, `data-z`), three planted defects, the gate around the reused `check_ids.py`, the Inkscape finding | standard library |
| `svg_roundtrip.sh` | rig, Inkscape plain-SVG export, reused `check_ids.py`, three planted defects, two touch-ups, the finding | bash, Inkscape |
| `kb_scale.py W H` | Ken Burns scale: fit, cover, move edge safety; `--selftest` | standard library |
| `emit_otio.py SPEC OUT.otio` | the neutral spec to OTIO at 24 fps; `--timeline169 PATH` also writes the reused `make_otio.py`'s input | standard library (Pillow only to make synthetic test media) |
| `validate_otio.py FILE.otio` | the R8 OTIO rules at JSON level (24 checks); `--with-otio [PYTHON]` also loads it with `opentimelineio` (6 more); `--no-media-check`, `--lenient-filmcraft`, `--json` | standard library |
| `adapter_probe.sh` | runs the reused `make_otio.py` unchanged against a 24 fps `timeline169.json` and records which adapters work; `--with-plugins` repeats it in a throw-away venv with the four adapter packages | bash, the venv |
| `make_media.py`, `rt_common.py` | test-card PNGs and a sine WAV (never overwrites a file); shared report and PNG-header helpers | Pillow for the cards |
| `spec/neutral_timeline.example.json` | the neutral spec: 24 fps, four 2880x1620 stills, three 24-frame dissolves, markers, one audio cue | |

Reused unchanged from earlier research (a test checks `git diff` is empty): `research/craft-visual-fixtures/make_ora.py`, `check_ids.py`, `at-layers.ora`, and
`research/sources/format-round1/make_otio.py`.

Copy the whole `pipeline/roundtrip` folder to use a tool elsewhere: the validators import `rt_common.py` and `kb_scale.py` from their own folder.

## ORA rules (`validate_ora.py`)

zip opens and passes its CRC; no duplicate or unsafe member names; `mimetype` is the first member, stored, and says `image/openraster`; `stack.xml` has no DTD, parses and
gives a canvas size; every layer has a `src` that exists and is a well-formed 8-bit RGBA PNG (no non-sRGB profile); every layer lies inside the canvas; layer names are unique
and match `^[A-Za-z][A-Za-z0-9._-]*$`; only supported attributes (image: `version w h xres yres`; layer: `name src x y opacity visibility composite-op`; stack adds
`isolation`); opacity 0 to 1, visibility visible or hidden, composite-op a known `svg:` operator; the bottom layer is `L00_asfound`; `mergedimage.png` is as large as the canvas.

**Two profiles.** `at-layers.ora` (the PhotoCraft acceptance fixture) names its layers `Title tint` and `Photo`, which break the id pattern, and it has no as-found layer. So `auto`
picks the **pipeline** profile (naming and `L00_asfound` are failures) when any layer name looks like `L10_...`, and the **reference** profile (the same structural rules; naming and
attribute rules are WARN) otherwise. `--profile pipeline` on `at-layers.ora` fails, so the choice is visible, not a blind spot.
**Layer values are not part of the naming rules:** opacity (0 to 1), visibility (`visible` or `hidden`), composite-op (a known `svg:` operator) and whole-number `x` and `y` are structural,
so a bad value is a **FAIL in both profiles** (`layer_value_invalid`); `at-layers.ora` still passes. Only the layer-name pattern, the supported-attribute list and the `L00_asfound` rule differ by profile.

## SVG: what the gate and the finding say

`svg_rig.py gate` runs the reused `check_ids.py` and names the reason: `ids_lost`, `data_attr_changed`, `element_kind_changed`.

* **`check_ids.py` does not fail on a changed element kind.** It prints `element kind changed: [...]` but exits 1 only for lost ids or changed `data-*`. A circle turned into an
  ellipse (same id, same data) has raw exit 0. The gate reads that line and exits 1 too; both numbers are printed. The reused script was not edited.
* **Inkscape 1.2.2, plain-SVG export, on the synthetic rig** (`build/evidence/wp06/svg_inkscape_finding.json`): all 18 `data-*` attributes survive verbatim, on `g`, `circle`, `rect`, `path`,
  `ellipse`, `use`, `text`, a `linearGradient` and an element with no id (including `data-pivot="320, 90"` with its space and `"120.50,220.0"` with its decimals); all 17 authored ids
  survive with the same element kinds; the `viewBox` is unchanged; no `inkscape:` or `sodipodi:` attributes in plain output (Inkscape's own format adds 5). Inkscape **adds ids of its own**
  to elements that had none (`svg31`, `defs10`, `g27`, `stop2`, `rect7`), so a tool that removes unreferenced ids removes those too. Moving a **child** rewrites its coordinates;
  moving a **group** adds `transform="translate(12,7)"` to it and leaves `data-pivot` unchanged. Optimized SVG (scour) was not run (scour is not installed); research R15 saw it strip ids.
  Windows Inkscape and versions after 1.2.2 are UNVERIFIED.

## OTIO

### What `validate_otio.py` refuses, beyond the shape of the numbers

* **`no_clips`**: no Video track holds a Clip. A timeline whose only Video track is empty has nothing to hand to FilmCraft, even if the stack has markers and the audio track has a cue.
* **`nested_composition`**: a Track holds a Stack or another Track, or the top Stack holds a Stack. OTIO allows nesting (an editor's export can do it), but every per-clip rule reads only a track's direct
  children, so clips inside a nested composition would pass unchecked. The tools refuse it instead; flatten the timeline.
* **`target_url_escapes_folder`**: a `..` segment anywhere in a `target_url` (`media/../media/x.png` included), the same test `emit_otio.py` applies to a spec. The hand-off folder must be copyable as a unit.

The other rules (rate 24, relative forward-slash URLs, media exists, source inside available range, dissolves fit, markers, `metadata.filmcraft`) are listed with their reason codes at the top of `validate_otio.py`.

### The neutral timeline spec, `lj-neutral-timeline/1`

`emit_otio.py SPEC.json OUT.otio` reads one JSON file; `spec/neutral_timeline.example.json` is a working one. Every field, and what the emitter does with it (a field marked *required* that is missing
or wrong makes the emitter exit 2 and name it, as `spec.shots[1].duration_frames must be ...`; nothing is written then):

| Field | Required | Meaning and limits |
|---|---|---|
| `schema` | yes | the text `lj-neutral-timeline/1` |
| `name` | no | the timeline's name in the `.otio` (default `Life Journey timeline`) |
| `synthetic_media` | no | `true` marks a TEST spec: missing media (numbered test cards, a sine WAV) is generated next to the `.otio`, never over an existing file. Absent or `false`: no media is ever created |
| `fps` | yes | must be `24` (W-14, S-01) |
| `sequence` | yes | `{"width": 1920, "height": 1080}`; any other size is refused (the shape of `metadata.filmcraft.settings` for it is not known) |
| `still_available_frames` | no | whole number > 0, default `240`; the `available_range` written on every still (a still has no length, so this is a convention); no shot may be longer |
| `markers[]` | no | sequence markers, placed on the top Stack: `name` (text), `at_frame` (whole number >= 0, a frame **of the whole timeline**), `color` (`PINK RED ORANGE YELLOW GREEN CYAN BLUE PURPLE MAGENTA BLACK WHITE`), `comment` (text, optional) |
| `shots[]` | yes | non-empty list, **in timeline order**; each shot becomes one clip on track `V1` (Video) |
| `shots[].id` | yes | `^[A-Za-z][A-Za-z0-9._-]*$`, unique; becomes the clip name |
| `shots[].source` | yes | relative path with forward slashes (no drive, scheme, backslash or `..`); becomes `target_url`, resolved from the `.otio`'s folder |
| `shots[].source_size` | when `motion.scale` is a `from` form | `[width, height]` in pixels; used for the scale and for the black-edge check (**without it that check is skipped**), and compared with the PNG header when the file exists |
| `shots[].duration_frames` | yes | whole number > 0 and not more than `still_available_frames` |
| `shots[].card_base` | no | `[r, g, b]`, three whole numbers 0 to 255: the background of this shot's generated test card (only when `synthetic_media` makes the card; it never reaches the `.otio`). Default: the dark tint `make_media.py` gives that card's number, so two default cards differ by at most about 30 levels, too little to see a dissolve between them one frame at a time. The Saturday test chapter (`research/craft-motion-fixtures/`) gives its second card a mid-bright teal |
| `shots[].motion` | no | the Ken Burns move (below). **A shot with no `motion` gets no `metadata.filmcraft`** and FilmCraft's default for it is unknown |
| `shots[].motion.scale` | yes, if `motion` | `[start, end]` in percent, or `{"from": "cover"\|"fit", "zoom": ratio, "direction": "in"\|"out"}`: `kb_scale.py` works out the base scale from `source_size` and the sequence; `zoom` (a number >= 1, default 1.0) is end divided by start; `direction` defaults to `in` |
| `shots[].motion.position` | no | `[[x, y], [x, y]]`: the picture's centre in sequence pixels at the start and at the end (default: the sequence centre both times, `[[960, 540], [960, 540]]`) |
| `shots[].motion.ease` | no | `Linear` (default) or `EaseOut`, the interpolation name written on the end keyframe (the start keyframe is always `Linear`; which side of a keyframe FilmCraft applies it to is UNVERIFIED); other names are refused |
| `shots[].transition_out` | no | `{"type": "dissolve", "frames": N}` with N > 0; not allowed on the last shot. Written as `in_offset` N//2 and `out_offset` N - N//2, centred on the cut to the next shot, and it takes no timeline time |
| `shots[].markers[]` | no | clip markers, same fields as `markers[]` but `at_frame` is a frame **inside the shot** (0 is its first frame, below `duration_frames`) |
| `audio[]` | no | cues on track `A1` (Audio), in time order, not overlapping; gaps between them are written as Gap items |
| `audio[].id` | yes | same pattern as a shot id; becomes the clip name |
| `audio[].source` | yes | relative path to the WAV, same rules as `shots[].source` |
| `audio[].start_frame` | no | whole number >= 0 (default 0): where the cue starts on the timeline |
| `audio[].duration_frames` | yes | whole number > 0, not more than the file's length at 24 fps (checked when the file exists) |
| `audio[].gain_db` | no | number (default 0.0), written to `metadata.filmcraft.gain_db` |
| `audio[].duck_against` | no | text or `null`; kept as `metadata.life_journey.duck_against`, a note for the mix, outside `metadata.filmcraft`. Nothing reads it yet |

Where a dissolve and a marker land: the timeline is the sum of the clip durations (dissolves take no time), so shot 1 of the example runs frames 0 to 120, shot 2 120 to 240, shot 3 240 to 360. The
12 + 12 dissolve between shots 2 and 3 is centred on the cut at 240 and runs frames **228 to 252**, which is why the example's second sequence marker, "Cue: title in", sits at `at_frame` 228.

### What the emitter writes

`emit_otio.py` writes `Timeline.1` / `Stack.1` / `Track.1` (V1 Video, A1 Audio) / `Clip.2` / `Transition.1` (`SMPTE_Dissolve`) / `Marker.2` / `Gap.1`. Rules it follows and the test
`otio.template_parity` proves: the output equals the R3 E2 template rebased to 24 fps (every rate 24; the 125-frame and 250-frame ranges become 120 and 240, the same seconds; the
24-frame dissolve stays 12 + 12; keyframe ticks are unchanged because they are seconds-based), ignoring only the timeline name and metadata, `available_range` and the audio clip's metadata.

* A dissolve of N frames is `in_offset N//2`, `out_offset N - N//2` and consumes no timeline time, so the timeline is the sum of the clip durations (480 frames, 20 s).
* `target_url` is a **relative** path with forward slashes (`media/ch01_s01.png`); Kdenlive and FilmCraft read it, absolute `file:///C:/...` URLs are not found (craft-motion.md F3).
* Ken Burns: `{"scale": {"from": "cover", "zoom": 1.2, "direction": "in"}}` or literal `[a, b]`; scale comes from `kb_scale.py` (2880x1620 into 1080p is 66.67 to 80.0). Position is the picture's
  centre in sequence pixels. A move that would show black at the frame edge is refused.
* `metadata.filmcraft` on every shot with motion: `scale_to_frame` false, `gain_db`, `source_in_ticks`, `duration_ticks` (254,016,000,000 ticks a second), and a `motion` effect with Float `scale`
  and Vec2 `position` keyframes (Linear, then the shot's ease; only `Linear` and `EaseOut` appear in the evidenced template, other names are a WARN). Audio clips carry `gain_db` and ticks.
* **A shot with no `motion` gets no `metadata.filmcraft`** and FilmCraft's default scale for it is unknown (`scale_to_frame` is not stated). The example spec gives the held last shot an explicit
  static motion (66.67 to 66.67) so nothing depends on that default.
* `available_range` is written for every clip: stills get `still_available_frames` (240, a convention: a still has no length), audio gets the WAV's length. The R3 template has `null` there; whether
  FilmCraft is happy with a value on a still is **UNVERIFIED** (WP-10 T3). The validator skips the rule when the field is null, so FilmCraft's own exports still pass.
* `synthetic_media: true` marks a test spec: missing media is generated next to the `.otio`. Without that flag no media is ever created. An existing file is never touched.
* `opentimelineio==0.18.1` alone ships only the `otio_json`, `otioz` and `otiod` adapters. EDL, FCPXML, Kdenlive and MLT need four separate packages. `adapter_probe.sh` records both cases
  (`build/evidence/wp06/adapter_probe.json` and `adapter_probe_with_plugins.json`): with the core install none of the four works; with `otio-cmx3600-adapter` 1.0.0, `otio-fcpx-xml-adapter` 1.0.0,
  `otio-kdenlive-adapter` 0.0.3 and `otio-mlt-adapter` 0.3.0 all four write a file at 24 fps (EDL ends at 00:00:20:00 for 480 frames; FCPXML `frameDuration` is `25/600s`, which is 1/24 s).

## On the maker's Windows PC (UNVERIFIED)

`validate_ora.py`, `validate_otio.py` and `kb_scale.py` use only the standard library, `os.path`, UTF-8 (and a UTF-8 BOM on read), ASCII output and no shell. They should run as
`py -3 -I pipeline\roundtrip\validate_ora.py C:\lj\at\file.ora` in Windows PowerShell 5.1 and 7, but nothing here was run on Windows. `svg_roundtrip.sh` and `adapter_probe.sh` are Linux-only;
on Windows the same Inkscape step is `inkscape.com in.svg --export-plain-svg --export-filename=out.svg` followed by `check_ids.py` (playbooks/craft-visual.md).

## What it never touches

It writes only under `renders/wp06/` (git-ignored, removed at the end of a test run), `<scratch>/wp06/` (removed), the `--json` and `--finding` files you name, and, for the venv, `<scratch>/venv-otio`.
It reads no image or sound file but the ones it generated. It makes no network call except `adapter_probe.sh --with-plugins` (pip, PyPI).
