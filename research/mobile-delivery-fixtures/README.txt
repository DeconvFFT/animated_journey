Fixtures for research/mobile-delivery.md (phone delivery). Run 2026-10-19 in the cloud container (ffmpeg 6.1.1 with libx264, libx265, libass, libharfbuzz;
ImageMagick 6.9.12; rsvg-convert; Python 3.13 with numpy and Pillow). The round-1 follow-up of the same day (caption colour, shaping, scaler files below) also used ffmpeg n7.0, n8.0 and
n9.0.2, each built from its FFmpeg git tag in a RAM disk with the same libass 0.17.1 and HarfBuzz 8.3.0 as 6.1.1. Synthetic material only; nothing personal, nothing sent through any messaging app.
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
                                         ffmpeg reports no error. CAUSE (corrected in round 1): the build, not the font. The same .srt and font through ffmpeg n9.0.2 draw the line correctly (ink width 666 px
                                         against 940 px broken; re-run 2026-10-19), because the `subtitles` filter of ffmpeg before n9.0 shapes in SIMPLE mode (the sibling's finding, research/devotional-sound-script-fixtures/README.txt).
                                         The PC build (9.0.2, UNVERIFIED) must still be checked on the PC (P-LOCK addition). The line is the Devanagari honorific shri and two test words, not a verse.
  gujarati_shaping_freeserif_2026-10-19.*  The same failure in her script (Gujarati, D-31), re-cut in round 1 with the non-sacred test line only: kshatriya, jnana, dharma, ki, kshi (U+0A95 U+0ACD U+0AB7 ...).
                                         The .srt holds the one line `ક્ષત્રિય  જ્ઞાન  ધર્મ  કિ  ક્ષિ` (kṣatriya "the warrior order" (here only a conjunct test), jñāna "knowledge", dharma, ki and kṣi (the last two test the short-i sign)).
                                         The .png has two rows made from that same .srt and the same font (FreeSerif, FontSize 40 on a 1080p frame): top row ffmpeg 6.1.1 `subtitles` filter, which FAILS (viramas visible,
                                         conjuncts unformed, reph standing alone, short-i after its consonant); bottom row ffmpeg n9.0.2 `subtitles`, which is CORRECT. The earlier file carried a first line with a deity's
                                         name invocation rendered wrongly; it was removed (reviews/mobile-delivery-round1.md section 2 and nudge 1). The font is not the cause (see the Devanagari entry); FreeSerif is used
                                         here only because it was installed, it is not a film font. Fonts for the film: Noto Sans Gujarati (default caption face) and Hind Vadodara (lines without digits), both SIL OFL 1.1
                                         per research/devotional-sound-script-fixtures/font_table_2026-10-19.csv and the two OFL.txt files read 2026-10-19; their shaping fixture is the sibling's (shaping_fixture.tsv ids guj-shri, guj-ksha, guj-jna, guj-dharma, guj-om).
  caption_colour_ffmpeg_builds_2026-10-19.csv   Round 1: twelve caption colours (white, grey E6, cream, ochre, pure red, film red, film green, film indigo, skin, grey 50%, grey EB, film ink) burned as a solid block glyph
                                         (U+2588, DejaVu Sans) into a BT.709-tagged ProRes master and taken through the P1 chain (subtitles or ass filter, scale, yuv420p, libx264 CRF 20), decoded with the Q-F1 method,
                                         interior median compared with the source colour. Builds: 6.1.1 (Ubuntu apt), n7.0, n8.0, n9.0.2. Variants: SRT with force_style PrimaryColour (the P1 template path), SRT with <font color>,
                                         ASS with no YCbCr Matrix header, with `None`, with `TV.709`, with `TV.601`; an untagged master; an untagged master with setparams before the filter.
  caption_colour_summary_2026-10-19.csv  One row per build and variant: worst channel error in 0 to 255 units, which patch, how many patches exceed the +-3/255 rule.
  caption_colour_real_text_2026-10-19.csv  The same colours as real P1-size caption text (Liberation Sans, FontSize 28, Outline 2): median of the glyph interior (full-coverage pixels eroded by one pixel), 6.1.1 and n9.0.2,
                                         yuv420p and yuv444p (the 4:4:4 rows separate chroma subsampling from the matrix).
  caption_ycbcr_matrix_example_2026-10-19.ass  A synthetic .ass with the `YCbCr Matrix: TV.709` header, the portable fix for .ass captions; its comment lines say which ffmpeg versions read it.
  scaler_bracket_720p_panel_2026-10-19.csv  Round 1: a black line of 1, 2, 3, 4 and 6 px at 1080p scaled to 1280x720 device pixels (720x1600 panel, landscape fit) by six scalers at twelve sub-pixel phases:
                                         min, mean and max contrast retained. It brackets the phone's unknown real scaler; the note's "ideal bicubic" is the Catmull-Rom row (reproduces roundtrip_contrast_720p_panel within 0.01).
  roundtrip_contrast_720p_panel_2026-10-19.csv  The same chart chains shown at 0.667 scale, as on a 720x1600 panel in landscape fit (her likely class): master, P1, P2 shown natively, WA-class proxies.
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
  Caption colour through the P1 chain, first measurement (libass burn-in on the BT.709 master, then the P1 filter chain, ffmpeg 6.1.1): white stayed 255,255,255; grey E6E6E6 became 231; cream F3E9D2 became
  242,232,219 (blue +9); red FF0000 became 255,21,0; ochre F0B323 became 249,174,24. ROUND-1 RE-RUN (caption_colour_* files): on 6.1.1 the saturated colours reproduce (pure red 255,23,0; ochre 246,175,27;
  film red 193,52,41; film green 40,111,47; worst 23/255) but cream does NOT (re-run 242,230,208, within 3/255, in both a block glyph and real text); the earlier cream "blue +9" is not reproduced and its
  cause is unknown (the first harness was throwaway). On ffmpeg n7.0 and later, with a BT.709-tagged master, every colour is within 3/255; on an untagged master every build falls back to BT.601 (23/255).
  AAC and true peak: a -1.0 dBFS 220 Hz sine measured -1.0 dBTP before and -0.7 dBTP after AAC-LC 192 kbps; a -1 dBFS square wave measured +1.1 dBTP before and +1.8 dBTP after. Check the final MP4, not the WAV.
  Chapters: ffmpeg -i P1.mp4 -i chapters.txt -map 0 -map_metadata -1 -map_chapters 1 -c copy out.mp4 wrote three readable chapters (Nero chpl atom); ffprobe warned "Referenced QT chapter track not found".
  MP4 hygiene on P1/P2/HEVC: atom order ftyp, moov, free, mdat (faststart works); -map_metadata -1 leaves only encoder, handler_name and the x264/x265 SEI string.

Git note: *.png is git-ignored (CLAUDE.md: generated, non-personal images may be added with `git add -f` after review). The two shaping PNGs here
(indic_shaping_freesans_2026-10-19.png, gujarati_shaping_freeserif_2026-10-19.png) are synthetic text renders, 14 KB and 38 KB, with no personal content and (since round 1) no sacred invocation; add them with `git add -f` if the scribes want them kept.
Search budget note: the shared web-search allowance ran out during this track and again in the round-1 follow-up; see the notes' "How these notes were made" and "Follow-up research (round 1)" for what that left UNVERIFIED.

Round-1 method (so the follow-up numbers can be rebuilt; scripts were throwaway and stayed in the session scratchpad)
  Builds: git clone --depth 1 --branch n7.0 | n8.0 | n9.0.2 https://github.com/FFmpeg/FFmpeg.git; ./configure --disable-everything --disable-autodetect --enable-gpl --enable-zlib --enable-libass --enable-libfreetype
  --enable-libfontconfig --enable-libharfbuzz --enable-libfribidi --enable-libx264 with only the filters, decoders, demuxers and muxers the test needs; make -j4 (about a minute each). n9.0.2 is tag commit 946fcce (2026-09-18).
  Master: 12 frames at 1 fps, 1920x1080, ProRes 422 HQ 10-bit 4:2:2, flat 0x14110f, BT.709 tags (and an untagged twin). Chain: [setparams,] subtitles=one.srt:force_style=... or ass=all.ass, then the P1 scale and format strings, libx264 -preset slow -crf 20.
  Decode: crop 40x40 at the block centre, scale=in_color_matrix=bt709:in_range=tv:out_range=pc, format=rgb24, median. Source reading that explains the results: libavfilter/vf_subtitles.c n6.1.1 calls ff_draw_init() (YUV defaults to SMPTE170M, BT.601);
  n7.0 calls ff_draw_init2() with the link's colorspace; n8.0 adds ass_get_color_space(), which maps the ASS track's YCbCr Matrix header (None means the link; absent, TV.601 and unknown mean BT.601; TV.709 means BT.709); ffmpeg's own SRT-to-ASS header says `YCbCr Matrix: None` (libavcodec/ass.c).
  Scaler bracket: the 1080p chart or a one-line image scaled with Pillow (BICUBIC = Catmull-Rom, LANCZOS, BOX, BILINEAR, NEAREST, and a single-tap bilinear AFFINE transform with no prefilter, the GPU texture-sampling case), contrast retained as in hindu-visual M-H1.
