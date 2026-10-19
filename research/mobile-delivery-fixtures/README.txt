Fixtures for research/mobile-delivery.md (phone delivery). Run 2026-10-19 in the cloud container (ffmpeg 6.1.1 with libx264, libx265, libass, libharfbuzz;
ImageMagick 6.9.12; rsvg-convert; Python 3.13 with numpy and Pillow). Synthetic material only; nothing personal, nothing sent through any messaging app.
Every number below the line is labelled (M) in the notes. Windows numbers are UNVERIFIED until windows_check_report.json exists (DECISIONS.md W-28).

Files
  safe_area_template.svg                 1920x1080 transparent overlay: venue 5% box (W-18), the central 80% band, fill-crop lines for 18:9, 19.5:9, 20:9 and 21:9 screens,
                                         the phone essential-text box (12% to 88% of height), and the two caption zones (venue FontSize 23 / MarginV 20; phone FontSize 28 / MarginV 40).
                                         Composite it over a G2 review-pack frame: rsvg-convert -w 1920 -h 1080 safe_area_template.svg -o overlay.png, then ffmpeg overlay.
  phone_test_p1_fillcrop.svg             Test-card page 1: percentage rulers on all four edges. On a phone, read the first number still visible at the top and bottom: that is
                                         the share of picture height the player crops in that mode. Opaque page (not an overlay).
  phone_test_p2_type_dark_lines.svg      Test-card page 2: twelve dark-step patches (8-bit codes 16..100), a type ladder at x-height 2.5% to 5.0% of picture height (Liberation Sans;
                                         rendered sizes checked at 2.54 / 3.36 / 4.58 against the labels 2.5 / 3.3 / 4.5), and a stroke ladder (1, 2, 3, 4, 6 px lines on cream, 2, 3, 4 px on indigo,
                                         hatch 3 px at 9 px pitch, 6 px dots). Page 3 of the card is research/hindu-visual-fixtures/phone_chart.svg.
  indic_shaping_freesans_2026-10-19.*    Evidence: Devanagari conjuncts rendered by ffmpeg 6.1.1 (libass + HarfBuzz) with FreeSans. Conjuncts are NOT formed and the short-i matra is misplaced;
                                         ffmpeg reports no error. A font with proper Indic shaping tables must be chosen and checked on the PC (P-LOCK addition).
  encode_ladder_sizes_2026-10-19.csv     Measured bitrates of P1, P2 and HEVC on three 12 s synthetic masters, scaled to 9 and 12 minutes, plus the cap bounds.
  encode_ladder_sweep_2026-10-19.csv     CRF sweeps (P1 16..24, P2 20..26, HEVC 18..26 and --tune grain) with PSNR against the master and grain survival in a flat patch (PR3).
  roundtrip_contrast_2026-10-19.csv      Line, hatch and cream-on-indigo contrast retained on the M-H1 chart through master, P1, P2, HEVC, WA-class proxies, and double-encode chains (static clip, frame 36).
  colour_patch_2026-10-19.csv            W-16 colour-patch test (twelve patches, +-3/255) for the P1, P2 and HEVC templates, and the bare "-pix_fmt yuv420p from RGB" trap.
  caption_geometry_35cm_2026-10-19.csv   Physical size (mm) and visual angle (degrees) of the caption x-height and cap height at 30, 35 and 40 cm on five phone geometries in three views.
  fill_crop_2026-10-19.csv               Computed crop of a 16:9 picture on 18:9, 19:9, 19.5:9, 20:9 and 21:9 landscape screens.
  dark_steps_veil_2026-10-19.csv         Reflection veil (E x R / pi) and the first 8-bit code at 10% Weber contrast over it, by white level, ambient lux, glass reflectance and gamma.

Method (so the numbers can be rebuilt; the harness scripts were throwaway and stayed in the session scratchpad because the sprint rule is "no code is written")
  Masters (12 s, 24 fps, ProRes 422 HQ 10-bit 4:2:2, BT.709 tags), made from raw RGB frames with:
     scale=out_color_matrix=bt709:out_range=tv,format=yuv444p,noise=alls=S:allf=t,format=yuv422p10le   -c:v prores_ks -profile:v 3 -vendor apl0 + the four BT.709 tags
     C1 photo push: a 3840x2160 fractal plasma, blurred, 4% cosine push (Pillow EXTENT, bicubic), grain S=3.
     C2 drawn: flat-colour shapes with 4 px ink outlines on twos, a 3 px / 9 px hatch band, a 6 px dot grid, a 132 px card line, grain S=3.
     C3 chart pan: research/hindu-visual-fixtures/phone_chart.svg rasterised at 1920x1080, 0.5 px a frame pan, grain S=7 (worst case).
     C4 chart static (3 s, grain S=4) for the contrast chains.
  Encodes, all from the ProRes master (templates are in the notes, section Templates T-M1). P1 uses -preset slow -crf 20 -maxrate 8M -bufsize 16M -profile:v high -level:v 4.1;
     P2 uses scale=1280:720 (lanczos) -crf 22 -maxrate 4M -bufsize 8M -level:v 3.1; HEVC uses libx265 -preset medium -crf 24 with vbv 6000/12000 and -tag:v hvc1.
  WA-class proxies are the two stress levels of research/hindu-visual.md M-H1 (1280x720 at 2.5 Mb/s Main; 640x360 at 0.5 Mb/s Main). They are NOT WhatsApp's encoder.
  Contrast retained: the M-H1 method re-built (profile of the cell averaged along the line direction, (background - darkest) / (background - ink)); it reproduces M-H1 within 0.02.
  Grain survival (cinematic-quality PR3): standard deviation of luma in a flat paper patch, mean of six frames, relative to the master; luma from gray16le, 8-bit units.
  Colour patch: the agent-pipeline Q-F1 method (decode with scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24) with twelve patches instead of three.

Build the 20 s phone test card (commands only; run from a folder holding the three PNGs and cap.srt)
  rsvg-convert -w 1920 -h 1080 phone_test_p1_fillcrop.svg -o p1.png ; rsvg-convert -w 1920 -h 1080 phone_test_p2_type_dark_lines.svg -o p2.png
  rsvg-convert -w 1920 -h 1080 ../hindu-visual-fixtures/phone_chart.svg -o p3.png
  ffmpeg -y -loop 1 -t 6 -framerate 24 -i p1.png -loop 1 -t 8 -framerate 24 -i p2.png -loop 1 -t 6 -framerate 24 -i p3.png
         -f lavfi -t 2 -i sine=f=100:r=48000 -f lavfi -t 2 -i sine=f=200:r=48000 -f lavfi -t 2 -i sine=f=400:r=48000 -f lavfi -t 2 -i sine=f=800:r=48000
         -f lavfi -t 2 -i sine=f=1600:r=48000 -f lavfi -t 2 -i sine=f=3200:r=48000 -f lavfi -t 2 -i anoisesrc=c=pink:r=48000:a=0.3
         -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv420p[v];[3:a][4:a][5:a][6:a][7:a][8:a][9:a]concat=n=7:v=0:a=1,volume=-23dB,pan=stereo|c0=c0|c1=c0[a]"
         -map "[v]" -map "[a]" -r 24 -c:v libx264 -preset medium -crf 18 -profile:v high -level:v 4.1 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv
         -c:a aac -b:a 192k -ar 48000 -movflags +faststart -map_metadata -1 phone_test_card_clean.mp4          (ran in 8 s; 20.0 s, 523 KB)
  Phone burn-in:  -vf "subtitles=cap.srt:force_style='FontName=Liberation Sans,FontSize=28,MarginV=40,Outline=2,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,WrapStyle=2'"
  Venue burn-in:  -vf "subtitles=cap.srt:force_style='FontName=Liberation Sans,FontSize=23,MarginV=20,Outline=2,Shadow=0,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,WrapStyle=2'"
  The tone ladder (100, 200, 400, 800, 1600, 3200 Hz at -23 dBFS, then pink noise) tells the maker which tones a phone speaker passes at 50% volume in a quiet room.
  On Windows run ffmpeg inside the working folder with relative file names (a drive letter's colon breaks the subtitles filter string; research/cinematic-quality-fixtures/README.txt).

Limits: synthetic content (not the film); one frame (36) for the contrast chains; three clips of 12 s; WA-class proxies; x264 and x265 settings from the container build (the PC build is 9.0.2, UNVERIFIED);
no Android or iOS player's own scaler; all phone geometry is computed from published diagonal and pixel counts, not measured on a device; PSNR and SSIM are dominated by the temporal grain and do not rank the encodes.

Extra checks run 2026-10-19 (results quoted in the notes, no separate file)
  Caption colour through the P1 chain (libass burn-in on the BT.709 master, then the P1 filter chain): white 255,255,255 stays 255,255,255; grey E6E6E6 becomes 231; cream F3E9D2 becomes 242,232,219 (blue +9);
  red FF0000 becomes 255,21,0; ochre F0B323 becomes 249,174,24. Tinted caption text fails the +-3/255 colour-patch rule when it goes through the subtitles filter.
  AAC and true peak: a -1.0 dBFS 220 Hz sine measured -1.0 dBTP before and -0.7 dBTP after AAC-LC 192 kbps; a -1 dBFS square wave measured +1.1 dBTP before and +1.8 dBTP after. Check the final MP4, not the WAV.
  Chapters: ffmpeg -i P1.mp4 -i chapters.txt -map 0 -map_metadata -1 -map_chapters 1 -c copy out.mp4 wrote three readable chapters (Nero chpl atom); ffprobe warned "Referenced QT chapter track not found".
  MP4 hygiene on P1/P2/HEVC: atom order ftyp, moov, free, mdat (faststart works); -map_metadata -1 leaves only encoder, handler_name and the x264/x265 SEI string.
