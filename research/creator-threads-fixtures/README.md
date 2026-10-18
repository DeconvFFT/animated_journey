# creator-threads-fixtures

Runnable versions of the three tested recipe cores in `research/creator-threads.md` (T1, T3, T4).
They need Python 3 with Pillow and numpy, and ffmpeg with ffprobe on PATH. No bash, so they run in PowerShell.

- `align_eyes.py`: two-point eye alignment (T1, source [64]). Check: `python align_eyes.py --selftest`
- `kenburns_xfade.py`: Ken Burns push-in and crossfade via ffmpeg (T3, source [65]). Check: `python kenburns_xfade.py --selftest`
- `jitter_twos.py`: hold-on-twos paper wobble (T4, source [66]). Check: `python jitter_twos.py --selftest`
- `synthetic_face.png`: cartoon test face, eye dots at (300,400) and (500,400). No real person.

Original sandbox run, research note of 2026-10-18 (cases not saved):
- Alignment: worst error 1.36 px (rotation -12 to +9 degrees, scale 0.6 to 1.7). Ken Burns: 13.0 s, 312 frames, 5.7 s render. Wobble: 24 of 24 held pairs identical, 23 of 23 pose changes.

Re-run of these files, using the self-test cases in the scripts (not the original cases): alignment 0.51 px over six eye points; Ken Burns 312 frames, 13.000 s, 6.5 s render; wobble 24 of 24, 23 of 23, same seed repeats exactly.
Advisor re-run 2026-10-18, same sandbox: 0.51 px; 312 frames, 13.000 s, 5.8 s render; 24/24, 23/23, PASS.

Sandbox: Ubuntu 24.04.5 LTS, CPU only, no GPU, Python 3.13.16, Pillow 12.3.0, numpy 2.5.3, ffmpeg 6.1.1.
Windows: install Python 3 and ffmpeg (route: research note F2, written from official docs), then `python -m pip install Pillow numpy`.
First Windows run (Python 3.14.8, ffmpeg 9.0.2 per note F2): not yet done; record the three self-test outputs here when it is.
Charter: the cloud session runs only the synthetic face. Family photos are processed on the maker's PC only.
