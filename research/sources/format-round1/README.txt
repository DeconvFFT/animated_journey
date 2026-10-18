Evidence scripts for research/format.md, "Follow-up research (round 1)", question 2 (headless film assembly) and question 4 (hash list).
Written and run 2026-10-18 by a Sonnet researcher in the cloud container (Linux, 4 vCPU, no GPU; ffmpeg 6.1.1, bpy 5.2.2, OpenTimelineIO 0.18.1, FilmCraft CLI 0.8.0, PowerShell 7.5.4 on Linux).
The photos in the test were generated gradients, not real material. Paths inside the scripts are examples; run them from a folder that holds timeline.json, captions.srt and an assets/ folder.
  build_film.py            ffmpeg route: timeline.json + captions.srt -> mp4 (zoompan, xfade, subtitles burn-in, two audio tracks). Python standard library only.
  build_blender.py         Blender VSE route via the `bpy` pip module; parses the SRT itself because bpy 5.2.2 has no SRT import operator.
  make_otio.py             timeline.json -> OpenTimelineIO -> EDL, FCPXML, Kdenlive, MLT files (needs pip: opentimelineio, otio-cmx3600-adapter, otio-fcpx-xml-adapter, otio-kdenlive-adapter, otio-mlt-adapter).
  filmcraft_headless.jsonl FilmCraft CLI command lines (see header comments).
  verify_manifest.ps1      PowerShell: checks a folder or burned disc against that list (MISSING / MISMATCH / count). Same test status as mk_manifest.ps1.
  mk_manifest.ps1          PowerShell: SHA-256 list of a folder in sha256sum format, written one level above the folder. Tested on PowerShell 7.5.4 (Linux); NOT run on Windows PowerShell 5.1.
  timeline.example.json, captions.example.srt   the inputs used.
The Minecraft excerpt is one folder up: research/sources/minecraft-usage-guidelines-2026-10-18.txt
