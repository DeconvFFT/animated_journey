Measurement scripts behind the (M) numbers in research/cinematic-quality.md (items M-C1 to M-C7).
Run on 2026-10-18 in the cloud container (ffmpeg 6.1.1, Python 3.13 with numpy and Pillow), made-up test material only.
These are throwaway measurement scripts, not production code. They expect a textured still named still.png in the working directory
(made with: convert -size 1920x1080 plasma:fractal -blur 0x1 still.png) and write temporary mp4 files; delete them afterwards.
Run with python3 -I from the same directory only after copying the script there (python -I ignores the current directory for imports).

zoom_velocity_classifier.py   M-C1 and M-C7 estimator: least-squares zoom per frame pair, classifies linear / in-out / ease-out, detects twos.
gen_synthetic_pushins.py      renders the synthetic push-ins (linear, cosine in-out, cubic out, back-out, and the on-twos versions) with Pillow.
zoompan_vs_subpixel.py        slow 4% push at 1080p from a 4K source: ffmpeg zoompan vs Pillow bicubic (roughness 0.35 vs 0.13).
thin_line_survival.py         M-C6: 1-4 px red and black lines through H.264 CRF 18 4:2:0.
grain_bitcost_and_banding.py  M-C5/M-C4 support: file size vs grain strength at CRF 18 (needs the g0..g32.mp4 files it describes).
Not saved as files: the signalstats flicker index (ffmpeg -vf signalstats,metadata=print + second difference of YAVG) and the grain-loop autocorrelation (numpy, 8 frames x2 vs fresh noise).
