Phone-legibility fixture for research/hindu-visual.md (finding M-H1). Run 2026-10-19 in the cloud container
(ffmpeg 6.1.1 with libx264, ImageMagick 6.9.12, rsvg-convert). Synthetic test chart only; no family or personal material.

Files
  phone_chart.svg                      the 1920x1080 test chart (markup only). Cells, left to right and top to bottom:
                                        A  black vertical lines on cream, widths 1,2,3,4,6 px, pixel-aligned
                                        B  the same lines shifted half a pixel (worst case for anti-aliasing)
                                        C  hatching, stroke w with gap 2w: 1px/pitch 3, 2px/pitch 6, 3px/pitch 9
                                        D  cream lines on indigo (a kolam-on-dark-floor case), widths 1,2,3,4
                                        E  black dots of diameter 2,3,4,6 px (pulli and Madhubani dot fills)
                                        F  colour pairs, widths 2 and 4 px: black on red, red on yellow, green on red
                                        G  black silhouette with holes of diameter 2,3,4,6 px (shadow-puppet perforation)
                                      cream #F3E9D2, ink #181410, indigo #1F2A5A, red #B5282B, yellow #F0B323, green #2E7D32.
  phone_chart_results_2026-10-19.csv   745 measurements: motion (static, pan), display (L, P), pipeline, metric, parameter, value.

Method (every number below the line is labelled (M) in the notes)
  1. Rasterise: rsvg-convert -w 1920 -h 1080 phone_chart.svg -o chart.png
  2. Masters (3 s, 24 fps, ProRes 422 HQ 10-bit, BT.709 tagged) with temporal grain, because the film's finish adds baked grain:
       static: ffmpeg -loop 1 -framerate 24 -t 3 -i chart.png -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv444p,noise=alls=7:allf=t,format=yuv422p10le" -c:v prores_ks -profile:v 3 master_static.mov
       pan:    the same with crop=1880:1080:x='trunc(n/2)':y=0,pad=1920:1080:0:0:color=0xF3E9D2 in front of the scale filter (0.5 px per frame)
  3. Encodes from the master:
       P1 (1080p phone master):  libx264 -preset medium -crf 18 -maxrate 8M -bufsize 16M -profile:v high -level 4.1, yuv420p
       WA-HD proxy:  scale=1280:720 (bicubic), libx264 -preset medium -profile:v main -b:v 2500k -maxrate 3000k -bufsize 5000k
       WA-STD proxy: scale=640:360 (bicubic), libx264 -preset medium -profile:v main -b:v 500k -maxrate 600k -bufsize 1000k
     The two WA proxies are NOT WhatsApp's encoder. They are two stress levels taken from anecdotal reports (about 640 px wide at about 500 kb/s,
     some clips at 15 fps; an "HD" option that means 720p). Real WhatsApp, Telegram and Signal output must be measured with ffprobe on the project phone.
  4. Decode frame 36, convert to full-range sRGB with scale=in_color_matrix=bt709:in_range=tv:out_range=full, then resize with a Catmull-Rom filter to
       L = 1920x1080 (phone held sideways, full screen on a 1080-pixel-tall display: one video pixel is about one device pixel)
       P = 1080x608  (phone upright, video fitted to a 1080-pixel-wide display: scale 0.5625)
  5. Measure by cropping the cell, averaging along the line direction to a one-pixel profile, and reading min or max of the profile:
       contrast retained = (background - darkest) / (background - ink), lines and dots; (lightest - ink) / (background - ink), holes;
       (lightest - indigo) / (cream - indigo), light lines on dark; (max - min of profile) / (background - ink), hatching;
       colour: largest sRGB distance from the panel colour divided by the distance between the two pure colours.
     Luma uses ImageMagick -colorspace Gray. Values slightly above 1.00 are resampling overshoot from the resize filter.
  Limits: synthetic lines, not traced artwork; two proxies, not the real apps; one frame (frame 36) of static and slow-pan clips; the dots measure takes a
  minimum over a small block, so grain biases it a few per cent toward "darker"; no HEVC variant; no Android player's own scaler. The measurement harness is a
  throwaway shell script that stayed in the session scratchpad because the sprint rule is "no code is written"; the commands above rebuild it.
