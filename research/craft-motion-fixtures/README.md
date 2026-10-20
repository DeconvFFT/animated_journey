# research/craft-motion-fixtures: the Saturday FilmCraft test chapter

A small, made-up chapter for the maker's FilmCraft five-minute test on Windows (Sat 24 Oct 2026; `spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md`, Steps 6 and 7, and checklist B of `playbooks/craft-motion.md`). It holds no photograph, no person and no symbol of any kind: two generated test cards (a grid, colour bars, the words TEST CARD) and an OpenTimelineIO file that lays them on a timeline. Package k1-filmcraft-test-chapter.

| File | What it is |
|---|---|
| `ch01.otio` | the chapter, with `metadata.filmcraft` (the metadata version FilmCraft 0.9.0 reads): 24 fps, 1920x1080, 240 frames (10 seconds), no audio |
| `media/ch01_s01.png`, `media/ch01_s02.png` | two 2880x1620 test cards (the conformed still size, scale 66.67), about 80 KB each: card 1 dark navy, card 2 teal; the OTIO names them by relative path |
| `test-chapter.spec.json` | the neutral timeline spec the OTIO and the cards are made from |

## What is in the chapter

| Frames | Seconds | What happens |
|---|---|---|
| 0 to 119 | 0 to 5 | test card 1, the one Ken Burns move: scale 66.67 to 80.0 (zoom 1.2 from cover) with a small drift of the centre, 960,540 to 930,520, easing out |
| 114 to 126 | 4 s 18 frames to 5 s 6 frames | the one cross dissolve, 12 frames, centred on the cut at frame 120 (OTIO `in_offset` 6, `out_offset` 6) |
| 120 to 239 | 5 to 10 | test card 2 (teal), held still at scale 66.67 |

Two sequence markers: `Chapter 01` at frame 0 and `Dissolve starts` at frame 114. The second card is a hold on purpose, so the only move in the chapter is the Ken Burns on the first card. The two cards share one layout (grid, colour bars, circle, corner chips) and differ in their label and their background: card 2's background is set with `shots[].card_base` in the spec (`[40, 150, 170]`), because the default dark tints of two generated cards differ by at most about 30 levels. A model of a linear-light 12-frame blend (FilmCraft blends in linear light, `research/craft-motion.md` and the c1 report) puts the mean change of the whole picture between two neighbouring frames at 3.7 to 13.2 levels of 255 for this pair, against 0.55 to 0.75 for the default pair, so the step-through can be seen. That is a model, not a FilmCraft result.

## How it was made (one builder, not two)

The builder is the WP-06 emitter `pipeline/roundtrip/emit_otio.py`, which is also what SP1b's `t3_filmcraft.py` runs for its own input. `t3_filmcraft.py` now has `emit_chapter()` (its `inputs()` step calls it) and an `--emit-chapter` mode, so the fixture and the T3 test share the one function:

```bash
python3 -I spikes/sp1b_readback/drivers/t3_filmcraft.py --emit-chapter research/craft-motion-fixtures/test-chapter.spec.json research/craft-motion-fixtures/ch01.otio
python3 -I pipeline/roundtrip/validate_otio.py research/craft-motion-fixtures/ch01.otio      # 24 checks; add --with-otio <python> for 6 more
```

The emitter never overwrites a file that exists, so to rebuild, delete `ch01.otio` and `media/` first. The same Pillow gives the same bytes (checked on 20 Oct 2026, Pillow 12.3.0). The Ken Burns move is refused by the emitter if it would show black at the frame edge.

## Git

`.gitignore` ignores `*.png` and any `media/` folder, so the two cards are added by hand after review, as `CLAUDE.md` allows for a generated, non-personal image: `git add -f research/craft-motion-fixtures/media/ch01_s01.png research/craft-motion-fixtures/media/ch01_s02.png`. `ch01.otio`, the spec and this file are ordinary text. The two paths are the whole of the `force_added_ok` list in `scripts/public_lint.config.json`: the three checks that otherwise flag a tracked file that `.gitignore` ignores (`public_lint.py`, `build/run_all_checks.sh` `repo.gitignore_coverage`, `hygiene.no_ignored_file_tracked_or_staged`) let exactly these through, and only while each is a PNG under 200 KB; a third card, a rename or a bigger card fails them again.

## What is checked and what is not

Checked on Linux: `validate_otio.py` passes (24 checks, 30 with the OpenTimelineIO 0.18.1 library); `check_guide.py` G9 holds the guide's copy lines and figures to this file; the key structure of `ch01.otio` is a strict subset of the file FilmCraft 0.9.0 imported with no error in WP-10 T3.
UNVERIFIED: that FilmCraft opens **this exact file** (no FilmCraft CLI was in the container when it was made), anything on Windows, where FilmCraft shows the two markers, and how its timecode counts.
