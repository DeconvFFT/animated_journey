Shaping, font and caption fixture for research/devotional-sound-script.md (track devotional-sound-script).
Run 2026-10-19 in the cloud container (second pass the same day after the register gained D-31: 16 more strings, 5 more Gujarati families, and a re-measure of captions with complex shaping). Strings are common devotional phrases and test words: nothing here is about her, her family or any real person.
Round 1 follow-up (2026-10-19, same container): ab.srt added (the A/B cue, test syllables only); the known_issue cells of Kumar One and Hind Vadodara in font_table_* updated; kumar_one_and_hind_vadodara_followup_*.csv added (method: fontTools 4.67.0 to delete tables and edit maxp, freetype-py 2.13.2 on FreeType 2.13.2 for the hinted-load test, libass 0.17.1 through the ffmpeg 6.1.1 `ass` filter at 86 px on 1920x1080 for the ink width, Pillow with a 40-grey-level threshold; scripts not kept).
It gates the Sun 1 Nov settings card (W-16, W-57). It is research, not production code: the numbers were produced by short throw-away scripts
(HarfBuzz via uharfbuzz 0.56.3 / HarfBuzz 14.6.0, fontTools 4.67.0, Pillow with Raqm, numpy) that are not kept in the repo; each method is described below so a build sprint can rebuild them.

Environment
  ffmpeg 6.1.1-3ubuntu5 (Ubuntu 24.04; --enable-libass --enable-libharfbuzz --enable-libfribidi --enable-libfreetype --enable-libfontconfig); libass 0.17.1, HarfBuzz 8.3.0, FriBidi 1.0.13, FreeType 2.13.2.
  ffmpeg n9.0.2 built from the FFmpeg git tag on the same machine with the same libraries (the version the maker's PC reportedly has: Gyan "release full" 9.0.2, dated 2026-09-19 on gyan.dev). The caption size and width tables were made with this n9.0.2 build's `subtitles` filter (complex shaping). A first run used 6.1.1's `subtitles`, which shapes in SIMPLE mode (see subtitles_vs_ass_shaping_*), and was discarded.
  Fonts: the weight-400 normal file of each family from github.com/google/fonts (main branch, read 2026-10-19), with that family's own OFL.txt and METADATA.pb.
  NOT run: Chromium (the Playwright download was blocked), any Windows build, any phone browser. Those are the maker's three renderings (below).

Files
  shaping_fixture.tsv              76 strings: id, script, OpenType script tag, label, text, code points, the correct render, the tell if broken. Devanagari 16, Tamil 6, Malayalam 6, Bengali 6, Telugu 6, Kannada 6, Gujarati 18, Odia 5, Gurmukhi 3, Latin 4. The Gujarati set includes a numeral string (guj-digits), the Om sign, candrabindu, visarga, and a Gujarati-plus-IAST line (guj-mixed).
  shaping_fixture.srt              the same strings as SRT cues (two lines per cue), for the project's own subtitles-filter template. It carries mantras, deity names, an aarti line and a Vedic verse: never render it through a path that fails the A/B (see commands 3 and 3b).
  ab.srt                           the A/B cue for command 3b: ONE cue of two lines, non-sacred test syllables only. Line 1 Gujarati: શ્રી ક્ષ જ્ઞ ધર્મ કિ ક્ષિ . Line 2 Devanagari, inside <font face="Noto Sans Devanagari">: क्ष त्र ज्ञ धर्म कि क्षि . On the 6.1.1 container build the default subtitles frame equals the shaping=simple frame (FAIL) and differs from the ass frame, which is what the cue is for.
  shaping_fixture_noto.ass         the same strings as an ASS page per script in the Noto Sans family of that script (names libass resolves).
  harfbuzz_shaping_results_*.csv   every font x every string of its script: glyph count, .notdef count, dotted-circle count, missing code points (1,517 rows).
  font_table_*.csv                 109 families (column known_issue added): licence read in the family's OFL.txt (copyright line with e-mail addresses omitted, Reserved Font Name), scripts, Latin and IAST gaps, Vedic marks, default instance, libass name check,
                                   KA height at FontSize=23, SHA-256 of the font file and of OFL.txt (the T8 evidence fields), OFL.txt URL.
  iast_coverage_*.csv              IAST (16 lower + 16 capital), ISO 15919 extras, combining ring below and candrabindu, per font; decomposed-form check.
  caption_size_FontSize23_*.csv    ink height of the base letter KA, of a sample line, of a two-line block and the line pitch, as % of 1080 px, through the subtitles filter of ffmpeg n9.0.2 (complex shaping) at the W-16 value FontSize=23. Mogra's line pitch is derived (two-line block minus one line's ink) because its two lines touch.
  caption_width_FontSize23_*.csv   width of one 40-51 code-point sample line per script/font as % of the 90% box (n9.0.2, complex shaping). Kumar One's 3.1% is a collapse, not a narrow face.
  devanagari_conjunct_pairs_*.csv  all 37 x 37 = 1,369 consonant+virama+consonant pairs shaped per Devanagari font: fused into one glyph, half form + base, other. An indicator of ligature richness, not a pass/fail.
  drawtext_n9.0.2_vs_harfbuzz_*.csv  72 strings through drawtext in n9.0.2: its logged glyph count equals HarfBuzz's for every one.
  libass_fontselect_*.txt          the libass lines that prove which font was really used, including the silent fallbacks (section F: the Gujarati run, incl. Hind Vadodara falling back for the digits).
  subtitles_vs_ass_shaping_*.csv   9 scripts x 8 renderings (ffmpeg 6.1.1 and 9.0.2; subtitles and ass; simple, complex, default): pixel hash and ink width of one controlled line, and the equalities that show 6.1.1's subtitles filter = simple shaping.
  subtitles_filter_shaping_6.1.1_vs_9.0.2_*.png   the picture of that difference (Devanagari line): row 1 broken, rows 2 and 3 correct.
  gujarati_conjunct_glyphs_*.csv   glyph counts per Gujarati font and string (a fused conjunct is 1 glyph; Mukta Vaani gives 3 to 4 for the same cluster).
  kumar_one_and_hind_vadodara_followup_*.csv   round 1: the Kumar One ablation (which font table makes libass collapse the line, in the Google Fonts and the foundry builds) and the Hind Vadodara digit check against the foundry's own source.
  libass_gujarati_fonts_*.png      the 11 Gujarati families rendered through libass (ass filter) at one size: look for Kumar One's collapsed row and Hind Vadodara's digit fallback.
  phone_speaker_model_*.csv        spectra of CC0/PD samples and the effect of a crude phone-speaker high-pass.

How to read the broken-shaping tells (named so a person can see them at 200%)
  dotted circle      a small dotted ring (U+25CC) where a mark has no valid base, or a box (tofu) where the font lacks the glyph.
  visible halant     the small slash/tick of the virama shown inside a word where a conjunct or half form was expected (Devanagari: kssa shown as ka + slash + ssa).
  standalone reph    the ra + halant shown as a full letter before/after the word instead of a hook above-right of the consonant (dharma shown as dha-r(slash)-ma).
  unmoved i-matra    the short-i sign (U+093F) drawn AFTER its consonant instead of before the whole cluster (ki shown as ka + i).
  detached matra     a vowel sign floating beside the letter (Bengali, Tamil two-part vowels, Malayalam chillus drawn as consonant + virama).
  fallback face      one word or mark visibly in a different design; confirm in the log line "fontselect: (...) -> FILE" and never from the picture alone.
  Reference of what broken looks like: render with shaping=simple (libass) or with a font-feature override that switches off akhn/rphf/half/blwf/vatu/cjct.

Commands for the PC (PowerShell; run from a folder that holds the fixture files and a "fonts" subfolder with the TTFs; use UTF-8 files only)
  1. Which libraries the build has:
       ffmpeg -hide_banner -buildconf | Select-String "libass|harfbuzz|fribidi|freetype|fontconfig"
  2. libass burn-in, with the proof lines (needs the debug log; the frames are the inspection copy):
       ffmpeg -hide_banner -loglevel debug -y -f lavfi -i color=c=0x14110f:s=1920x1080:r=1:d=40 -vf "ass=shaping_fixture_noto.ass:fontsdir=fonts" -frames:v 40 page_%02d.png 2>&1 | Select-String "Shaper|fontselect|not found|provider"
     PASS: every requested family maps to its own file; no "Glyph 0x... not found, selecting one more font"; the frames show none of the tells below. (The "Shaper: ... (COMPLEX)" line is printed at start-up in every mode and is NOT proof; see command 3b.)
  3. The project's real template (SRT + force_style), one script at a time, with <font face="..."> around any run in another script:
       ffmpeg -y -i test_clip.mp4 -vf "subtitles=shaping_fixture.srt:fontsdir=fonts:force_style='FontName=Mukta,FontSize=23'" out.mp4
     CAUTION: shaping_fixture.srt holds sacred strings (mantras, deity names, an aarti line, a Vedic verse). On any build older than n9.0 the subtitles filter renders them broken, which is a FAIL render. Run command 3b first; on a build that fails it, burn this file only through the ass filter (command 2), never through subtitles.
  3b. The A/B that proves the caption path shapes (ffmpeg before n9.0 fails it; n9.0 and later pass). One cue, test syllables only (ab.srt in this folder: Gujarati શ્રી ક્ષ જ્ઞ ધર્મ કિ ક્ષિ and Devanagari क्ष त्र ज्ञ धर्म कि क्षि), in the project's own style. Never run the FAIL or shaping=simple render on a mantra, a deity's name, an aarti line or a Vedic verse; the broken frame is kept only for the test syllables:
       ffmpeg -y -f lavfi -i color=c=0x14110f:s=1920x1080:d=1 -vf "subtitles=ab.srt:fontsdir=fonts:force_style='FontName=Noto Sans Gujarati,FontSize=23'" -frames:v 1 ab_default.png
       ffmpeg -y -f lavfi -i color=c=0x14110f:s=1920x1080:d=1 -vf "subtitles=ab.srt:fontsdir=fonts:force_style='FontName=Noto Sans Gujarati,FontSize=23':shaping=simple" -frames:v 1 ab_simple.png   (n9.0+ only; older builds reject the option)
       ffmpeg -y -i ab.srt ab.ass   (then edit the Style line: Fontname and Fontsize 23)  and   ffmpeg -y -f lavfi -i color=c=0x14110f:s=1920x1080:d=1 -vf "ass=ab.ass:fontsdir=fonts" -frames:v 1 ab_ass.png
     PASS: ab_default.png equals ab_ass.png and differs from ab_simple.png. FAIL: ab_default.png equals the simple look (visible halants, moved short-i not moved). On a build older than n9.0 there is no simple option on subtitles: compare ab_default.png with ab_ass.png; they must be the same.
  4. drawtext (only if a card is made with it): use textfile=, not text=, so the Windows code page cannot mangle the string:
       ffmpeg -hide_banner -loglevel verbose -y -f lavfi -i color=c=black:s=1500x200:d=1 -vf "drawtext=fontfile=fonts/Mukta-Regular.ttf:textfile=dt.txt:fontsize=80:fontcolor=white:x=20:y=50" -frames:v 1 dt.png 2>&1 | Select-String "shape:"
     n9.x prints "shape: script=Deva ..."; n6.1 to n8.1.1 print nothing and draw conjuncts broken.
  5. Chromium on the PC and a browser on her phone (cable transfer, D-15): open an HTML page that lists the same strings with lang="hi", "ta", "ml", "bn", "te", "kn", "gu", "or", "pa" and the same fonts via @font-face from the local files,
     font-synthesis: none; compare against the libass frames. Inspect at 200%. Which font each browser really used cannot be assumed from the picture: view it in the browser's developer tools.

Three-way results table to fill (one line per script): libass burn-in on the PC | Chromium on the PC | phone browser: pass / which tell / which string id.
