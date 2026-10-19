# Validators (WP-05): the G6 machinery for every shot

Three small tools, all read-only, all `python3 -I` (Windows: `py -3 -I`), none needs more than the standard library and ffmpeg.
They answer three different questions, and a shot needs all three (a file can pass one and fail another):

| Tool | Question | What it reads | Catches |
|---|---|---|---|
| `spec_check.py` | Does this finished file meet its delivery profile? | the file, with ffprobe and ffmpeg | wrong size, rate, pixel format, tags, audio format, loudness, truncation, stray metadata |
| `colour_patch.py` | Do the PIXELS come out right through this encode chain? (W-16) | nothing of yours: it encodes a synthetic three-patch frame | a BT.601 matrix under BT.709 tags, which every tag check passes |
| `mo8_gate.py` | Is this slow push or pull smooth at the sub-pixel level? (W-41) | a frame folder or a clip of at most 96 frames | `zoompan`-style shimmer, on the master before the delivery encode |

Exit codes for all three (build plan 4.3): `0` pass, `1` a check failed, `2` bad usage or invalid input (or a refusal), `3` environment problem
(ffmpeg missing). Every tool prints what it does first, names files by base name only, and writes nothing except the file named by `--json` / `--out`.
Everything here ran on ffmpeg 6.1.1 (Linux). **Nothing has run on Windows or on the PC's ffmpeg 9.0.2** (see "What is UNVERIFIED").

## Run them

```
python3 -I pipeline/validators/spec_check.py FILE --profile venue_h264
python3 -I pipeline/validators/spec_check.py FILE --profile phone_1080 --profiles-file pipeline/phone/profile.json
python3 -I pipeline/validators/spec_check.py --list-profiles
python3 -I pipeline/validators/colour_patch.py --ffmpeg ffmpeg --chain-file pipeline/lib/chains.json --all --json OUT.json
python3 -I pipeline/validators/colour_patch.py --chain h264_venue
python3 -I pipeline/validators/colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080 --chain phone_720_share
python3 -I pipeline/validators/colour_patch.py --derive-from RAW.json --out DERIVED.json
python3 -I pipeline/validators/mo8_gate.py renders/push_frames/ --json OUT.json
python3 -I pipeline/validators/spec_check.py --selftest        # needs only ffmpeg and ffprobe
python3 -I pipeline/validators/colour_patch.py --selftest      # needs only ffmpeg
bash tests/validators/run_tests.sh --quick                     # under 60 s; evidence in build/evidence/wp05/tests_quick.jsonl
bash tests/validators/run_tests.sh --all                       # one lj_with_disk stage; evidence in build/evidence/wp05/tests_all.jsonl
bash tests/validators/make_evidence.sh                         # both, plus the acceptance commands and summary.json
```
Each mode writes its own `tests_<mode>.jsonl`, so a later `--quick` can not overwrite the `--all` envelopes. `run_checks.py --work` must be a folder inside the
repository with no tracked file (it is deleted at the end and the lint tests need it under the repository root); anything else exits 2 at startup.

On the PC: `py -3 -I pipeline\validators\colour_patch.py --ffmpeg C:\...\ffmpeg.exe --all --json %TEMP%\colour_patch_pc.json` (WP-09's runner wraps this).
The colour test must be run on exactly the ffmpeg build you will render with: the container's 6.1.1 and the winget 9.0.2 build gave different pixels under identical tags.

## The colour-patch test in one paragraph

One 1920x1080 frame of three flat patches, red (255,0,0), 50% grey (128,128,128) and a skin tone (224,172,140), is encoded (2 frames) through a chain from
`pipeline/lib/chains.json` (or any file of that shape, such as WP-08's `pipeline/phone/profile.json`), decoded with
`scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24`, and the worst per-channel error out of 255 is reported. 3 or less passes.
**The measurement is made at the chain's own output size.** The colour conversion runs on the decoded picture at whatever size the chain made (the 1280x720 phone
copy is converted at 1280x720); only then is the RGB picture stretched back to 1920x1080 by nearest-neighbour (`scale=1920:1080:flags=neighbor`, which copies pixels
and changes no value) so the same patch boxes can be read. A 1920x1080 chain is read exactly as before. The output size is recorded per chain (`output_size`) and
printed as `measured at 1280x720` when it is not 1920x1080. A chain that cannot be encoded or decoded at all is **not** a colour result: it gets its own line,
`RESULT chains: could not be measured (encode/decode error)`, separate from `ABOVE TOLERANCE`, and both exit 1. Built-in controls
(format-first, bare `-pix_fmt`, bare ProRes 4444) show whether this build has the trap; two more test the tool itself. `approved: true` in `chains.json` is only
allowed where the chain measures 3 or less: the tool exits 1 if a file says otherwise. 10-bit 4:2:2 files read about 2 too far under the default decode path
(a property of swscale's decode, not of the file; `worst_error_accurate_decode` shows the file itself), so ProRes 422 HQ has one level of margin, not three.

**Both phone chains (`phone_1080` and `phone_720_share` in `pipeline/phone/profile.json`) must be run on the PC build (ffmpeg 9.0.2) before either is
`approved: true`.** On the container's 6.1.1 they measure 1/255 each, which proves the tool reads the 720p chain, not that the PC's ffmpeg gets the same pixels.

### The raw record and the filed form (do not mix them up)

* `--json OUT.json` writes the **raw** record: ffmpeg version line, build **configure flags**, SHA-256 of the binary, every chain result. A build someone compiled
  can carry folder names in its flags. **On the maker's PC the raw record is read by the maker and pasted in chat only. It is never copied into the project,
  committed or filed.** (`public_lint.py` refuses files named `colour_patch_pc*.json`.) The test runner follows the same rule even for the container's public Ubuntu
  build: its raw record is kept in the scratch folder beside the repository (`../build-scratch/wp05/`) and only the derived form is filed, so there is no exception to remember.
* `--derive-from RAW --out DERIVED` writes the **filed** form `lj-pc-chains/1` (`pc_chains.schema.json`): ffmpeg version number only, binary SHA-256, chain names,
  worst errors, pass flags. It is built from a fixed list of fields; configure flags, the version line's trailing text and any path are dropped by construction.
  File only this, under `build/evidence/pc/`.

## `spec_check.py` profiles

Profiles live in `pipeline/settings.json` (`profiles`) and in any `--profiles-file` (an object with a `profiles` object; the phone profile from WP-08 is one).
A profile name may not be defined twice. Shape (a null or absent field is not checked; a list means "any of these"):

```
"venue_h264": {
  "description": "...", "decision": ["W-17"], "chain": "h264_venue",
  "container": "mp4",              mp4 | mov | mkv
  "faststart": true,               moov must come before mdat
  "video": {"codec": "h264", "profile": ["High"], "level": [41], "pix_fmt": ["yuv420p"], "width": 1920, "height": 1080, "fps": "24/1",
            "color_range": ["tv"], "color_space": ["bt709"], "color_primaries": ["bt709"], "color_transfer": ["bt709"],
            "alpha": false, "max_mbps": 20},
  "audio": {"required": true, "codec": ["aac"], "profile": ["LC"], "sample_rate": 48000, "channels": [2], "bits_per_sample": null},
  "loudness": {"true_peak_max_dbtp": -1.0, "integrated_lufs": [-23, -18, -16], "tolerance_lu": 1.0},
  "metadata": "neutral" }
```

Check ids (a failure names one): `container.readable`, `container.type`, `container.moov`, `container.atoms`, `container.faststart`, `video.streams`, `video.codec`,
`video.profile`, `video.level`, `video.pix_fmt`, `video.alpha`, `video.size`, `video.fps`, `video.frame_count`, `video.color_range`, `video.color_space`,
`video.color_primaries`, `video.color_transfer`, `video.bitrate`, `audio.present`, `audio.codec`, `audio.profile`, `audio.sample_rate`, `audio.channels`, `audio.bits`,
`audio.true_peak`, `audio.integrated`, `integrity.decode`, `metadata.neutral`.

What `spec_check.py` cannot see: pixel colours (use `colour_patch.py`), and anything about the picture itself. Loudness is read to 0.1 dB.
ProRes: an `unknown` range tag is accepted with a note (ffmpeg 6.1.1 writes none); other builds may write `tv`, which is accepted too.
`metadata.neutral` treats the Matroska muxer's own per-stream `DURATION` tag (a timecode such as `00:00:02.000000000`, which `-map_metadata -1` cannot remove) as
structural, so the `ffv1_lossless` chain's own mkv passes; the same key with any other value is still reported. `--selftest` encodes one FFV1 clip through that chain
and expects every check to pass, so the PC's ffmpeg is tested for the same behaviour. The `integrity.decode` detail has the file path and ffmpeg's heap addresses
(`[NULL @ 0x55ce...]`) removed and its lines sorted and de-duplicated, so a filed verdict JSON carries no address and does not change with decoder thread timing.

## `chains.json` keys

The 4.5 shape (`container`, `vf`, `video_args[]`, `audio_args[]`, `expect{}`, `notes`) plus four additive keys: `alpha`, `approved`, `measured` (per ffmpeg version) and
`used_for`. `expect.profile` and `expect.color_range: null` follow the files the chains really make; a null `expect` value is not asserted.

## What is UNVERIFIED

Everything on Windows (ffmpeg.exe, `py -3 -I`, Windows paths); the numbers on ffmpeg 9.0.2 (including both phone chains, and whether that build still writes a
per-stream `DURATION` tag into mkv: the `spec_check.py --selftest` FFV1 case will tell); ProRes tag behaviour on Windows builds. The code uses only argument-list
subprocess calls, `os.path` and `tempfile`, and the self-tests pass under `python3 -I -S` (no site-packages at all) on Linux with ffmpeg 6.1.1.
