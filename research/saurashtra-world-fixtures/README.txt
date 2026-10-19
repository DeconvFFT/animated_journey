Fixtures for research/saurashtra-world.md (track saurashtra-world: Bhavnagar and Saurashtra, Gujarati Hindu home life, crafts and the festival year).
Run 2026-10-19 in the cloud container. Synthetic strings and public sources only: nothing here is about her, her family or any real person.
It builds on research/devotional-sound-script-fixtures/ (which already holds 18 Gujarati strings, the 104-family font table, the libass log and the Hind Vadodara, Farsan and Kumar One findings) and does not repeat it.
What this folder adds: 32 strings from her world (home, festival, greeting and card words, Gujarati digits in a date, a Latin-with-IAST line), shaped both without and with the Gujarati language tag;
the CAUSES of two failures the sibling found (Kumar One and Mukta Vaani); caption size and visual angle for ten Gujarati families; and the Bhavnagar festival table as data.
It is research, not production code: the numbers came from short throw-away scripts kept in the session scratchpad (the sprint rule is "no code"); each method is described below so a build sprint can rebuild them.

Environment
  ffmpeg 6.1.1-3ubuntu5 (--enable-libass --enable-libharfbuzz --enable-libfribidi --enable-libfreetype --enable-libfontconfig); libass 0.17.1, HarfBuzz 8.3.0, FriBidi 1.0.13, FreeType 2.13.2, font provider fontconfig.
  Python 3.13 with fontTools 4.67.0 and uharfbuzz 0.56.3 (a throw-away virtualenv), Pillow 12.3.0 (FreeType 2.14.3, Raqm 0.10.5, HarfBuzz 14.2.1), numpy.
  Fonts: ten Gujarati families, each file downloaded from https://raw.githubusercontent.com/google/fonts/main/ofl/<dir>/ on 2026-10-19 with its own OFL.txt and METADATA.pb.
  All ten families (Noto Sans Gujarati, Noto Serif Gujarati, Hind Vadodara, Mukta Vaani, Baloo Bhai 2, Anek Gujarati, Rasa, Shrikhand, Farsan, Kumar One) match the sibling's font_table SHA-256 values for both the font file and OFL.txt, so both tracks read the same files.
  NOT run: Chromium (no browser in the container), any Windows build (the PC's ffmpeg is reportedly Gyan 9.0.2), any Android device. Those are the maker's three renderings (steps below). Windows numbers stay UNVERIFIED (DECISIONS.md W-28).

Files
  shaping_fixture_gujarati.tsv / .srt         32 strings: id, label, text, code points, the correct render, the tell if broken.
  shaping_fixture_gujarati_libass.ass         the same strings as ASS pages, one style per family, 22 pages (11 style names x 2 pages; 'Anek Gujarati' and 'Anek Gujarati Medium' are both there on purpose). PlayRes 1920x1080, inspection size 42.
  harfbuzz_shaping_results_gujarati_both_languages_*.csv   every family x every string, shaped twice: buffer language unset ('default') and 'gu'. Columns: glyph count, .notdef, dotted circle, visible-halant glyphs, code points missing from the cmap, glyph names.
  libass_fontselect_gujarati_*.txt            the libass lines that prove which file was used and where a silent fallback happened (Anek plain name, Hind Vadodara digits, Farsan Om, IAST letters).
  font_table_gujarati_*.csv                   the ten families: OFL.txt first line, Reserved Font Name (none), files and default instance, libass name test, Om and digits coverage, conjuncts through libass, IAST, KA %, SHA-256 of font file and OFL.txt, OFL.txt URL.
  caption_size_width_FontSize23_gujarati_*.csv   ink height of the base letter KA, of a 54-code-point sample line and of a two-line block, and the line width, at FontSize=23, through the ass filter (complex shaping).
  caption_angle_35cm_gujarati_*.csv           KA height in mm and in degrees at 35 and 40 cm on a 64.9 mm picture height (a 6.1-inch phone, landscape fit; mobile-delivery caption_geometry_35cm), at FontSize 23 and 28.
  bhavnagar_festival_table_*.csv              the festival table of the notes as data (54 rows, 2026-10-19 to 2027-03-06), with Gujarati weekday and tithi names, the Template D delta, the schedule collision and a blank kept_by_her column.
  libass_gujarati_rasa_shrikhand_farsan_kumarone_page1_*.png and page2   the four families the brief named as unread, rendered through libass on both pages of strings.
  libass_kumar_one_shipped_vs_unhinted_copy_*.png   left: the shipped Kumar One collapsed to one point; right: a copy with the hinting program removed, rendering correctly.
  libass_mukta_vaani_unfused_conjuncts_*.png        Mukta Vaani through libass: every conjunct unfused, with a visible halant mark.
  libass_hind_vadodara_digits_fallback_*.png        Hind Vadodara: the digits are drawn by another face (FreeSerif), larger and in a different style.

Method (so the numbers can be rebuilt)
  1. Strings: shaping_fixture_gujarati.tsv, UTF-8, with code points listed. 32 rows: 31 in Gujarati script (including three open-card candidates, festival names, weekdays with the year in Gujarati digits, and home words) and one Latin row with IAST.
  2. HarfBuzz: uharfbuzz, face from the font bytes, buffer script Gujr and direction ltr, language either unset or 'gu'; a glyph is .notdef if its id is 0, a dotted circle if it is the font's U+25CC glyph, a visible halant if its glyph name contains Halant or Virama.
     A fused conjunct is fewer glyphs than code points (4 code points of shri give 2 glyphs; 3 code points of ksha, jna and tra give 1).
  3. libass: ffmpeg -loglevel debug -f lavfi -i color=c=0x14110f:s=1920x1080:r=1:d=22 -vf "ass=shaping_fixture_gujarati_libass.ass:fontsdir=fonts" -frames:v 22 page_%02d.png ; read the 'Shaper:' line (HarfBuzz-ng (COMPLEX) is the pass), the fontselect lines and any 'Glyph 0x... not found, selecting one more font' line. Every frame was inspected by eye at 100% and the contrast cases at 300%.
  4. Caption size: an ASS file with PlayResX 384, PlayResY 288 (the size ffmpeg gives a converted SRT), Style FontSize 23, Alignment 5, Outline 0, Shadow 0; rendered with the ass filter on a black 1920x1080 frame; the ink box measured with numpy at a luma threshold of 96. The 6.1.1 'subtitles' filter shapes these scripts in 'simple' mode (sibling finding), so it was NOT used for size or width.
     The values for Noto Sans Gujarati, Noto Serif Gujarati, Hind Vadodara, Baloo Bhai 2, Rasa, Shrikhand and Farsan equal the sibling's KA percentages; Mukta Vaani 2.96, Anek Gujarati 2.78 and Kumar One 3.06 (unhinted copy) agree too.
  5. Angle: degrees = atan(KA height in mm / viewing distance in mm); KA mm = KA % of picture height x picture height (64.9 mm, 6.1-inch phone, landscape fit, from research/mobile-delivery-fixtures/caption_geometry_35cm_2026-10-19.csv).
  6. Why Kumar One collapses (found in this track): Pillow with FreeType 2.14.3 and BASIC layout fails to load 31 of 31 base letters with 'execution context too long' (FT_Err_Execution_Too_Long, the hinting bytecode); Shrikhand, Farsan and Hind Vadodara load all of them. A copy made with fontTools.subset (hinting off, all glyphs and layout features kept) loads all 31 and renders correctly through libass. The font file has fpgm, prep and cvt tables and no GPOS. The exact faulty instruction was not isolated (J).
     An unhinted copy is allowed by the OFL (no Reserved Font Name, licence kept, not sold by itself); it was made only in the scratchpad and is not in the repo.
  7. Why Mukta Vaani breaks (found in this track): its GSUB has script records DFLT, gjr2, gujr and latn, and under both gjr2 and gujr the 'GUJ ' language-system record lists only typographic features (dlig, dnom, frac, liga, numr, onum, salt, smcp, ss01, subs, sups, tnum) and none of the shaping features the default record has (abvs, akhn, blwf, blws, cjct, half, pres, psts, rphf, and rkrf or vatu). With HarfBuzz's buffer language unset, the default language system is used and conjuncts fuse; with the language set to 'gu' (what libass evidently passes, and what a browser passes for lang="gu") they do not. The other nine families are identical under both settings.

Results in one table (container, libass 0.17.1 + HarfBuzz 8.3.0)
  family                 name resolves   Om   Gujarati digits   conjuncts           IAST dot-below letters   note
  Noto Sans Gujarati     yes             yes  yes               fused               missing (fallback face)  safe caption face; KA 3.33%
  Noto Serif Gujarati    yes             yes  yes               fused               missing                  KA 2.78%: FontSize about 25.6 for 3.1%
  Hind Vadodara          yes             yes  NO (FreeSerif)    fused               missing                  cannot carry a Gujarati year or date
  Mukta Vaani            yes             yes  yes               UNFUSED with gu     present                  do not use for Gujarati text
  Baloo Bhai 2           yes             yes  yes               fused (half forms)  present (no m-dot)       KA 3.06%
  Anek Gujarati          NO (plain name) yes  yes               fused               none                     only as 'Anek Gujarati Medium'
  Rasa                   yes             yes  yes               fused               present (not long vocalic r, l)  KA 3.06%; Gujarati and IAST in one serif face
  Shrikhand              yes             yes  yes               fused               missing                  title art; 54 code points fill 86% of the 90% box
  Farsan                 yes             NO (FreeSerif)  yes    fused               present (no m-dot)       title art only
  Kumar One              yes (then collapses)  yes yes          HarfBuzz fine; libass collapses  missing    excluded as shipped

The maker's three renderings (PowerShell, from a folder holding this folder's files and a 'fonts' subfolder with the ten TTFs; UTF-8 files only; relative file names, because a drive letter's colon breaks the subtitles filter string)
  1. Which libraries the PC build has:
       ffmpeg -hide_banner -buildconf | Select-String "libass|harfbuzz|fribidi|freetype|fontconfig"
  2. libass burn-in with the proof lines (PASS: a 'HarfBuzz-ng ... (COMPLEX)' line; every family maps to its own file; no 'Glyph 0x... not found' for the families you intend to use):
       ffmpeg -hide_banner -loglevel debug -y -f lavfi -i color=c=0x14110f:s=1920x1080:r=1:d=22 -vf "ass=shaping_fixture_gujarati_libass.ass:fontsdir=fonts" -frames:v 22 page_%02d.png 2>&1 | Select-String "Shaper|fontselect|not found|provider"
     Compare the frames with the PNGs here: Kumar One must be collapsed or readable on your build (record which); Mukta Vaani must show unfused conjuncts or fused ones (record which); Hind Vadodara digits and Farsan Om must fall back.
  3. Chromium on the PC and Chrome on her phone: a page that lists the strings of the TSV twice, once with lang="gu" and once without, in each family via @font-face from the local files with font-synthesis: none (a build sprint writes it; no HTML is kept here because of the no-code rule). On the phone, run it once with the phone's language set to English (India) and once to Gujarati, because Android passes the locale to the shaper.
     Which font each browser really used cannot be assumed from the picture: read it in developer tools.
  4. The phone player: play the burned-in MP4 (pixels, so shaping is already done) and open an SRT in the phone's own player to see how that player shapes. Noto Sans Gujarati sits in AOSP's noto-fonts project, but a given handset may ship a different Gujarati system font (UNVERIFIED for the maker's phone, O-54).
  Three-way results table to fill (one line per family): libass burn-in on the PC | Chromium on the PC | phone browser | pass or the tell | string id.

Limits: one container build of libass and HarfBuzz; ten families; synthetic strings; angle computed from published geometry, not measured on a device; the Gujarati spellings of the home, festival and card words are the researcher's and need a native reader (the maker) before any is used on a card.
