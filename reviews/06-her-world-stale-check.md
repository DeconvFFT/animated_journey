# 06 Her-world stale check (mechanical critic)

Sonnet critic, 2026-10-19 (UTC). Read-only: nothing was edited, nothing committed. `scripts/stale_check.py` was run unmodified; the independent grep was written separately (scratch only) and then compared with it.

Scanned for the independent grep: `playbooks/` (23 files), `.claude/skills/` (all files, including recipes and sub-files), `skills-staging/` (23 SKILL.md), `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `QUESTIONS-SUN-25-OCT.md`: 82 text files, 21448 lines, tree fingerprint `eff5b69399ada507` (unchanged between the first scan and a re-scan at the end of the session; the playbooks were last touched at 08:14, the registers at 07:10 to 07:19, `QUESTIONS-SUN-25-OCT.md` at 08:29). `DECISIONS.md` was checked for duplicate IDs and for scribe-pending markers only.

## 1. Verdict

**Not clean.** The check does not pass, but the residue is narrow and mostly mechanical.

- **Playbooks, staged skills, ROADMAP, PLAN-ON-A-PAGE, QUESTIONS:** no Table 4 value and no retired term survives as a live instruction or live fact. Every remaining hit is a negation, a "superseded/retired" note, a by-design S-01 line, a reference that names the stale term to describe the cleanup, or a false positive (sections 7 and 8). The exceptions are in section 3c and section 4.
- **Installed skills (`.claude/skills/`) are where the stale copies still sit:** 110 lines in 19 files. 96 of those lines (in 15 files) are already fixed in `skills-staging/` and clear on install. **14 lines in 4 files have no staged copy** because staging holds only `SKILL.md` files: the two `r4_*` voxel recipes, `free-creative-toolchain/references.md` and `life-story-interviewing/beat-sheet.md` (section 3a). Those need an orchestrator edit as well as the install.
- **Other residuals (4):** two unresolved notes in playbooks (section 3c) and two "not applied" headings inside Changelogs (section 4).
- **Duplicate IDs in `DECISIONS.md`:** none (248 table rows, 248 unique IDs; D-01 to D-31, W-01 to W-79, S-01 to S-65 and O-01 to O-84 all accounted for, with absorbed O-IDs named in their rows).
- **Specific haveli or temple she attends:** none named. No names, emails, phone numbers or addresses found. Public landmarks are named as place and tradition leads (section 6).
- **`stale_check.py`:** exit 1 (FAIL 350, WARN 18, allowlisted 82). 304 of its 368 hits are in this critic's scope; of its 146 FAIL lines there outside Changelogs, 93 are residual and 53 are not after reading each in context (section 8). The independent grep found 17 more residual lines that the script has no pattern for.

## 2. `stale_check.py` output (recorded, unmodified)

Command: `python3 -I scripts/stale_check.py` (report mode; also run with `--json` and `--md` into the scratchpad, not the repo). Exit code 1. Stdout, verbatim:

```
stale_check: scanned 336 files, 51949 lines
  FAIL 350, WARN 18, allowlisted 82, REGRESSIONS 80, outstanding-row hits 288, INFO candidate hits 0
  S-01  outstanding   FAIL  19 WARN   0 allowlisted  19
  S-05  applied       FAIL   6 WARN   0 allowlisted  25
  S-08  applied today FAIL   6 WARN  13 allowlisted  30
  S-09  applied       FAIL   3 WARN   0 allowlisted   0
  S-10  applied today FAIL   1 WARN   0 allowlisted   0
  S-11  applied       FAIL   1 WARN   0 allowlisted   0
  S-13  applied       FAIL   0 WARN   2 allowlisted   0
  S-16  applied today FAIL   1 WARN   0 allowlisted   0
  S-17  applied       FAIL   2 WARN   0 allowlisted   0
  S-18  applied       FAIL  22 WARN   0 allowlisted   0
  S-19  applied       FAIL   8 WARN   0 allowlisted   0
  S-20  applied       FAIL   9 WARN   0 allowlisted   0
  S-26  applied       FAIL   1 WARN   0 allowlisted   0
  S-28  applied       FAIL   3 WARN   0 allowlisted   0
  S-29  applied       FAIL   1 WARN   0 allowlisted   0
  S-31  applied       FAIL   1 WARN   0 allowlisted   0
  S-38  outstanding   FAIL  40 WARN   0 allowlisted   0
  S-39  outstanding   FAIL  22 WARN   0 allowlisted   0
  S-42  outstanding   FAIL   9 WARN   0 allowlisted   0
  S-43  outstanding   FAIL   1 WARN   0 allowlisted   0
  S-44  outstanding   FAIL  16 WARN   0 allowlisted   4
  S-45  outstanding   FAIL  56 WARN   0 allowlisted   0
  S-46  outstanding   FAIL  17 WARN   0 allowlisted   0
  S-47  outstanding   FAIL  18 WARN   0 allowlisted   0
  S-48  outstanding   FAIL   8 WARN   0 allowlisted   1
  S-49  outstanding   FAIL   5 WARN   0 allowlisted   2
  S-50  outstanding   FAIL  44 WARN   0 allowlisted   0
  S-51  outstanding   FAIL   1 WARN   0 allowlisted   0
  S-56  outstanding   FAIL  14 WARN   1 allowlisted   0
  S-61  outstanding   FAIL  10 WARN   2 allowlisted   0
  S-64  outstanding   FAIL   4 WARN   0 allowlisted   0
  S-65  outstanding   FAIL   1 WARN   0 allowlisted   0
```

Notes on the script's reach, so its numbers are read correctly:

- It does **not** scan `ROADMAP.md`, `PLAN-ON-A-PAGE.md` or `QUESTIONS-SUN-25-OCT.md` (excluded by its own scan list), so those three were checked by the independent grep only.
- It scans wider than this critic's scope: of its 368 hits, 59 are in `research/*-fixtures/`, 4 in `spikes/` and 1 in `pipeline/`. Those are the build sprint's and the orchestrator's and are not in this report. The S-50 fixtures and the `pipeline/scenes/testcard/smoke3d.html` hit are the ones to expect there.
- Its changelog test is "line starts with a date", so it counts some Changelog sub-bullets as prose (for example `playbooks/devotional-sound-script.md:723`, which is a v0.1 Changelog bullet). This report uses the section: everything under a `## Changelog` heading is excepted.
- Its pattern file has no row for `Replay Mod`, `Goxel` on its own, `voxelising`, the "Chinese New Year" source line, "scrubber page as the companion", `(L1, Sat 14 Nov` written without the word "lock", or the stale "still carries insider lines" self-description; the independent grep caught those (section 8).

## 3. Residual hits

Format: `file:line` then the text around the match. "Row" is the Table 4 row. Staged status: **fixed in staged copy** means `skills-staging/<same path>` exists and no longer has a live hit of that kind; **no staged copy** means the file is not in `skills-staging/` at all.

### 3a. Installed-skill lines with no staged copy (14 lines, 4 files)

**`.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py`**

- `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py:1` [S-46] # r4_photo2vox.py: photo -> 64x36 luminance relief -> MagicaVoxel .vox file (for a Goxel and Blender chain).
- `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py:6` [S-46] #     xvfb-run -a goxel scene.vox --export scene.obj      (Goxel 0.11.0, 0.24 s; xvfb-run is for servers only)
- `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py:7` [S-46] #   Then r4_render_voxel.py in Blender (bpy 5.2.2).
- `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py:9` [S-46] #   Use it as plumbing. For hero objects, hand-model in MagicaVoxel, Goxel or Blockbench (playbook Decision 3).

**`.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py`**

- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:1` [S-46] # r4_render_voxel.py: Blender side of the voxel chain. Import the Goxel OBJ, vertex-colour material, warm light, 960x540 still.
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:5` [S-46] ...Needs: ./scene.obj next to this file (from r4_photo2vox.py and Goxel).
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:6` [S-46] # Writes: ./voxel_still.png
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:7` [S-46] # Axis: the Goxel OBJ is Z-up, and Blender's OBJ importer assumes Y-up, so forward_axis='Y', up_axis='Z' is required.
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:10` [S-46] # Run:    blender -b --factory-startup -P r4_render_voxel.py   (or python3 with bpy installed)
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:12` [S-46] ...--factory-startup -noaudio --python-exit-code 3 -P .\r4_render_voxel.py
- `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:33` [S-46] sc.render.filepath = os.path.join(W, 'voxel_still.png'); bpy.ops.render.render(write_still=True)

**`.claude/skills/free-creative-toolchain/references.md`**

- `.claude/skills/free-creative-toolchain/references.md:25` [S-46] - [56] MagicaVoxel — https://ephtracy.github.io/mv_main.html ; https://ephtracy.github.io/mv_renderer.html ; https://ephtracy.github.io/mv_commands.html — 0.99.7.2 [7/12/2025]; licence; rend...
- `.claude/skills/free-creative-toolchain/references.md:51` [S-46] ... (Python 3.13), Inkscape 1.2.2, MLT melt 7.22.0, Synfig 1.5.1, Goxel 0.11.0 (Xvfb), librsvg 2.58.0, svgpathtools, Pillow; outputs inspected with 'ffprobe' and by eye. Runnable copies of rese...

**`.claude/skills/life-story-interviewing/beat-sheet.md`**

- `.claude/skills/life-story-interviewing/beat-sheet.md:10` [S-51/S-63] - Cold open: about 1:15 (black and one true room sound; hands and the object; the contract card; the title last)

Fix owner: orchestrator (S-46 says "skill and recipes"; S-51 and S-63 name `beat-sheet.md` as the "skill file"). The S-46 text retires `r4_photo2vox.py` and `r4_render_voxel.py` outright; `references.md` entries [56] MagicaVoxel and the Goxel 0.11.0 version in the tested-tools line go with them. `beat-sheet.md:10` should read the first-sound rule (a sound above about 400 Hz and a first light within about 4 s; W-36, W-76) instead of "black and one true room sound".

### 3b. Installed-skill lines fixed in the staged copy (96 lines, 15 files)

These clear when the staged `SKILL.md` replaces the installed one. Checked directly, not by pattern: for every kind of hit found in an installed file, the staged file has either no hit of that kind or only the canonical or negation lines listed in section 10.

**`.claude/skills/agent-first-production-pipeline/SKILL.md`** (staged: `skills-staging/agent-first-production-pipeline/SKILL.md`)

- `.claude/skills/agent-first-production-pipeline/SKILL.md:14` [S-38] ... card (W-14, W-16). Real family material enters only after the L1 process lock, Sat 14 Nov 2026, and covert collection starts Sun 15 Nov (D-13, W-06). Only-me (D-03): the maker is the proxy ...
- `.claude/skills/agent-first-production-pipeline/SKILL.md:30` [S-38] ...er. Real family material may enter the pipeline only after the L1 process lock (Sat 14 Nov 2026, proven on synthetic material) and the maker's go; covert collection starts Sun 15 Nov (D-13, ...
- `.claude/skills/agent-first-production-pipeline/SKILL.md:32` [S-39] ... 'craft' (EffectCraft titles) runs in the container only after spike S1 passes; on the maker's PC the EffectCraft template route is available once the five-minute test in 'research/craft-mot...
- `.claude/skills/agent-first-production-pipeline/SKILL.md:39` [S-39] ...at shots under 1.5 s are impact frames only. Both are built in spike S5. Until they exist, do these checks by hand and say so in the review.
- `.claude/skills/agent-first-production-pipeline/SKILL.md:46` [S-39] ...md'). Use 'effectcraft-cli render' in the container only after spike S1 passes; on the maker's PC the template route is available once the five-minute test in 'research/craft-motion.md' R7 p...
- `.claude/skills/agent-first-production-pipeline/SKILL.md:106` [S-39] ...ther a running background job keeps the cloud container awake (spike S4); whether cloud sessions accept image attachments; the maker's PC specifications ('lj.ps1 doctor' is designed, not bui...
- `.claude/skills/agent-first-production-pipeline/SKILL.md:107` [S-39] ...tainer (M14), but this is proven only for one image and scene. Spike S1 is still the gate for any Craft command-line use in the container. The Gemini 2.5 Flash Image shutdown date (2026-10-0...

**`.claude/skills/ai-photo-to-animation-pipeline/SKILL.md`** (staged: `skills-staging/ai-photo-to-animation-pipeline/SKILL.md`)

- `.claude/skills/ai-photo-to-animation-pipeline/SKILL.md:61` [S-38] ...). Her real photos are judged in the vertical slice, after the L1 process lock (Sat 14 Nov), by the maker alone from their own knowledge ("Does this look like her at that age?"); there is no...

**`.claude/skills/animated-biography-patterns/SKILL.md`** (staged: `skills-staging/animated-biography-patterns/SKILL.md`)

- `.claude/skills/animated-biography-patterns/SKILL.md:36` [S-38] ...hs or interview notes. Family material comes in only after the L1 process lock on Sat 14 Nov 2026; covert collection starts Sun 15 Nov (D-13, W-06).
- `.claude/skills/animated-biography-patterns/SKILL.md:66` [S-42/S-50] ...paper sets photographed, are the practice stand-ins [6][21]. A voxel look is never the marker: original voxel assets only, and no Mojang textures, sounds, UI or footage (D-23). Record it in ...

**`.claude/skills/animation-production-planning/SKILL.md`** (staged: `skills-staging/animation-production-planning/SKILL.md`)

- `.claude/skills/animation-production-planning/SKILL.md:69` [S-39] - [ ] G-READY Sun 15 Nov 2026: H in writing; spikes S1 to S5 pass or fallbacks named; style frames approved.
- `.claude/skills/animation-production-planning/SKILL.md:73` [S-61] - [ ] G-LOCK Sat 6 Feb (Lunar New Year falls on this date; if observed, lock Fri 5 Feb [94]); G-MIX Sat 13 Feb; G-MASTER Sat 20 Feb; G-REHEARSE Mon 22 Feb.
- `.claude/skills/animation-production-planning/SKILL.md:104` [S-39] ... s per frame on an RTX 4090 at 64 to 256 samples [82][83][84]; spike S3 measures the kitchen set and passes if one real hero frame lands within 2 times the table. Hero finals are GPU work by...
- `.claude/skills/animation-production-planning/SKILL.md:108` [S-64] ... out, and the her-turn conversation after the reveal (Saturday 6 March 2027) is how she can put it back [6]. Fable flags and never passes G5.
- `.claude/skills/animation-production-planning/SKILL.md:120` [S-39] ...'s weekly hours, pending, 'DECISIONS.md' O-01); the spike list S1 to S5 (S3 measures the real kitchen); the holiday and observance dates for the jurisdiction (the country is pending, O-02; r...
- `.claude/skills/animation-production-planning/SKILL.md:147` [S-61] - [94] Wikipedia, Chinese New Year — https://en.wikipedia.org/wiki/Chinese_New_Year — read 2026-10-18 — 2027: Saturday 6 February, Goat.

**`.claude/skills/cinematic-quality-bar/SKILL.md`** (staged: `skills-staging/cinematic-quality-bar/SKILL.md`)

- `.claude/skills/cinematic-quality-bar/SKILL.md:116` [S-42/S-50] - **Brand.** Do not use the Minecraft name as a title, and do not use unlicensed marks. A voxel look is never the reconstruction marker, and no Mojang textures, sounds, UI or footage enter t...
- `.claude/skills/cinematic-quality-bar/SKILL.md:155` [S-42/S-50] - [57] Minecraft usage guidelines excerpt (local): research/sources/minecraft-usage-guidelines-2026-10-18.txt

**`.claude/skills/craft-apps-motion-refinement/SKILL.md`** (staged: `skills-staging/craft-apps-motion-refinement/SKILL.md`)

- `.claude/skills/craft-apps-motion-refinement/SKILL.md:30` [S-38] ...ep where real family material would enter the tools before the L1 process lock (Sat 14 Nov 2026; covert collection starts Sun 15 Nov, D-13) and the five-minute test has passed. Use generated...
- `.claude/skills/craft-apps-motion-refinement/SKILL.md:34` [S-39] ...ve in 'research/craft-motion.md'. Look for a written result of spike S1 (tests T1 to T6, for example in 'research/' or in a 'build_info.json'). If none exists, the Craft command-line tools a...

**`.claude/skills/craft-apps-visual-refinement/SKILL.md`** (staged: `skills-staging/craft-apps-visual-refinement/SKILL.md`)

- `.claude/skills/craft-apps-visual-refinement/SKILL.md:14` [S-38] ...ore the premiere (D-12). Real family material enters after the L1 process lock, Sat 14 Nov 2026, with covert collection from Sun 15 Nov (D-13). Every photo set is 'cloud: none' unless the ma...
- `.claude/skills/craft-apps-visual-refinement/SKILL.md:35` [S-38] ...he maker has raised it; an agent never does (W-24). Before the L1 lock (Sat 14 Nov) no photo of hers is used at all (D-13).

**`.claude/skills/creator-recipe-library/SKILL.md`** (staged: `skills-staging/creator-recipe-library/SKILL.md`)

- `.claude/skills/creator-recipe-library/SKILL.md:3` [S-47] ...photo-motion, same-pose alignment, paper-collage, stop-motion, Minecraft-tour, AI-animation or music recipe, or must judge a creator thread or tutorial before reuse.
- `.claude/skills/creator-recipe-library/SKILL.md:16` [S-47] ...nt or morphing, a paper wobble, an editor move, stop-motion, a Minecraft tour, AI image-to-video or music.
- `.claude/skills/creator-recipe-library/SKILL.md:25` [S-38] ...e pipeline and process are locked. The charter forbids it: the L1 process lock is Sat 14 Nov 2026 and covert collection starts Sun 15 Nov (D-13).
- `.claude/skills/creator-recipe-library/SKILL.md:34` [S-47] - 'minecraft.net' and 'help.minecraft.net': HTTP 503 to the fetch tool and an HTTP/2 protocol error (INTERNAL_ERROR) to 'curl', so the block is on Mojang's side. The usage guidelines ('https...
- `.claude/skills/creator-recipe-library/SKILL.md:41` [S-38] ...s are gathered only after the pipeline and process are locked (L1, Sat 14 Nov; D-13).
- `.claude/skills/creator-recipe-library/SKILL.md:46` [S-47] ...h tool's status and record it in the card. Install editors and Minecraft helpers only from their official pages, for example Kdenlive [43] and Arnis [56]. Record whether the tool is archived...
- `.claude/skills/creator-recipe-library/SKILL.md:75` [S-38] - [ ] The maker has confirmed the L1 process lock (Sat 14 Nov) and that covert collection has started (Sun 15 Nov or later; D-13).
- `.claude/skills/creator-recipe-library/SKILL.md:122` [S-47] - **Minecraft.** No Mojang textures, sounds, UI or footage in the public cut; original voxel assets only (D-23). Replay Mod and Arnis recipes are practice or companion material, not premiere...
- `.claude/skills/creator-recipe-library/SKILL.md:137` [S-47] - https://www.replaymod.com/docs/ [53]
- `.claude/skills/creator-recipe-library/SKILL.md:161` [S-47] - [53] Replay Mod documentation. https://www.replaymod.com/docs/. Undated. Recording, keyframes, rendering, shaders.
- `.claude/skills/creator-recipe-library/SKILL.md:162` [S-47] ... https://github.com/louis-e/arnis. Copyright 2022-2026. Builds Minecraft worlds from OpenStreetMap; Apache-2.0; official sources are GitHub and arnismc.com only.
- `.claude/skills/creator-recipe-library/SKILL.md:168` [S-47] - [69] Minecraft: Java & Bedrock Edition for PC, Xbox store listing. https://xbox.com/en-us/games/store/minecraft-java-bedrock-edition-for-pc/9nxp44l49shj. Undated (release date 6/6/2022 sho...

**`.claude/skills/free-creative-toolchain/SKILL.md`** (staged: `skills-staging/free-creative-toolchain/SKILL.md`)

- `.claude/skills/free-creative-toolchain/SKILL.md:3` [S-46] ...oolchain for Life Journey shots (Blender 5.2 LTS for parallax, voxel and line-draw renders; Inkscape for SVG; Kdenlive or Resolve Free for assembly; ffmpeg and ImageMagick as glue). Use it w...
- `.claude/skills/free-creative-toolchain/SKILL.md:10` [S-46] ...'r2_param.py', 'r3_linedraw.py', 'r4_photo2vox.py', 'r4_render_voxel.py', 'r5_story.mlt', 'r7_era_looks.txt', 'r8_vse_xfade.py' and 'r9_deliver.sh'. Each file's header names the tool version...
- `.claude/skills/free-creative-toolchain/SKILL.md:12` [S-38] ...ness is -1 dBTP everywhere (W-19). Real photos enter after the L1 process lock, Sat 14 Nov 2026; covert collection starts Sun 15 Nov (D-13). Only-me (D-03): the maker is the proxy and nobody...
- `.claude/skills/free-creative-toolchain/SKILL.md:18` [S-46] - A voxel or Minecraft-style object must be modelled, converted or rendered.
- `.claude/skills/free-creative-toolchain/SKILL.md:36` [S-46] | New shot: Ken Burns, parallax, line reveal, voxel object, album look | 5 to 12 |
- `.claude/skills/free-creative-toolchain/SKILL.md:51` [S-38] ...on stock or synthetic images. Real photos enter only after the L1 process lock (Sat 14 Nov 2026), and covert collection starts Sun 15 Nov (D-13, W-10); the maker agrees each set and the 'clo...
- `.claude/skills/free-creative-toolchain/SKILL.md:78` [S-46] ...live, Shotcut, OpenShot, Inkscape, GIMP, Krita, Blender, MagicaVoxel, Goxel, Blockbench, Audacity.
- `.claude/skills/free-creative-toolchain/SKILL.md:80` [S-46] - Platform rules: MagicaVoxel runs on Windows and macOS only [56]; Blender 5 on macOS needs Apple Silicon [30].
- `.claude/skills/free-creative-toolchain/SKILL.md:89` [S-46] - Voxel models imported with forward axis Y and up axis Z [100].
- `.claude/skills/free-creative-toolchain/SKILL.md:132` [S-46] - A voxel model lying flat or sideways because the axes were not converted [100].
- `.claude/skills/free-creative-toolchain/SKILL.md:148` [S-46] - Inpainting, colourising, upscaling and voxelising change or invent pixels. Treat each output as a reconstruction.

**`.claude/skills/journey-format-architecture/SKILL.md`** (staged: `skills-staging/journey-format-architecture/SKILL.md`)

- `.claude/skills/journey-format-architecture/SKILL.md:12` [S-44] ...es that can take an optional interlude later, with the offline scrubber page as the companion ('DECISIONS.md' W-30). Only the maker can change that default. 'DECISIONS.md' is the source of t...
- `.claude/skills/journey-format-architecture/SKILL.md:33` [S-44/S-50] ...e shares the PC or room; the budget ceiling; whether she loves Minecraft and Java is owned), plus venue and AV operator and audience size and ages (O-20, O-21). "Partly playable" is defaulte...
- `.claude/skills/journey-format-architecture/SKILL.md:34` [S-44/S-50] ...anion 4.40; film with 2 to 3 interludes 3.80; scroll story and Minecraft film 3.55 each; explorable formats 2.45 to 2.95. Texture capacity asks what a format can carry of one life: a 5 means...
- `.claude/skills/journey-format-architecture/SKILL.md:45` [S-44/S-50] ...olating. Compare with the notes' ranges for the other formats: Minecraft film 130 to 220 h; scroll story 70 to 100 h; Godot explorable 120 to 200 h; three.js world 200 to 300 h; film with in...
- `.claude/skills/journey-format-architecture/SKILL.md:54` [S-38] ...k the dates: venue asked by 2026-11-06, answer due 2026-11-15; L1 process lock 2026-11-14; G9 (G-SLICE) on 2026-12-20; G13 (G-MID) on 2027-01-17; picture lock 2027-02-06 (G-LOCK); delivery o...
- `.claude/skills/journey-format-architecture/SKILL.md:124` [S-44/S-50] ...iting (research RQ1); the 'music-sound' track owns the recipe. Mojang's usage terms were read on 2026-10-18 [50][92], but the page reserves the right to change, so re-save the excerpt before...
- `.claude/skills/journey-format-architecture/SKILL.md:158` [S-44/S-50] [50] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 on the second attempt (HTTP 200); quotes from the dated excerpt [92...
- `.claude/skills/journey-format-architecture/SKILL.md:163` [S-44/S-50] [88] Sibling notes — research/games.md — read 2026-10-18 — Minecraft terms (Q7), memorial worlds (Q5), design devices.
- `.claude/skills/journey-format-architecture/SKILL.md:164` [S-44/S-50] [92] Mojang/Microsoft — Minecraft Usage Guidelines, dated excerpt — https://www.minecraft.net/en-us/usage-guidelines — 2026-10-18 — [P] excerpt saved in research/sources/minecraft-usage-guid...

**`.claude/skills/life-film-music-and-sound/SKILL.md`** (staged: `skills-staging/life-film-music-and-sound/SKILL.md`)

- `.claude/skills/life-film-music-and-sound/SKILL.md:57` [S-49/S-50] - [ ] No Minecraft or other game sound or music is used.
- `.claude/skills/life-film-music-and-sound/SKILL.md:106` [S-49/S-50] - **Minecraft.** Game sounds and music are brand assets under the Usage Guidelines, and sharing counts as commercial use. Do not use them. Build a sound language of your own.
- `.claude/skills/life-film-music-and-sound/SKILL.md:135` [S-49/S-50] - Minecraft Usage Guidelines, https://www.minecraft.net/en-us/usage-guidelines

**`.claude/skills/life-story-interviewing/SKILL.md`** (staged: `skills-staging/life-story-interviewing/SKILL.md`)

- `.claude/skills/life-story-interviewing/SKILL.md:8` [S-38] ...st insider" does not exist. The gate for real gathering is the L1 process lock, Sat 14 Nov 2026; covert collection starts Sun 15 Nov (D-13, W-06, W-10). Before the premiere the sessions are ...
- `.claude/skills/life-story-interviewing/SKILL.md:34` [S-38] 2. Check the gate. The gate is the L1 process lock on Sat 14 Nov 2026 (D-13, W-06); sessions start Sun 15 Nov (W-10). An earlier recorded Door A session with the consent script is itself a b...
- `.claude/skills/life-story-interviewing/SKILL.md:70` [S-64] ...eal, the subject has her say at the her-turn conversation (Sat 6 Mar), and nothing is shared beyond the room until she agrees; relatives first see the film as the April response recordings (...
- `.claude/skills/life-story-interviewing/SKILL.md:75` [S-38] - [ ] Gate passed for this recorded session (L1 lock Sat 14 Nov; sessions from Sun 15 Nov); no early Door A session without a TD-L2c decision
- `.claude/skills/life-story-interviewing/SKILL.md:145` [S-08] ...esearch Recipe 4). It is patched separately and still carries "insider" and consent-card lines that the register supersedes.

**`.claude/skills/meaningful-game-mechanics/SKILL.md`** (staged: `skills-staging/meaningful-game-mechanics/SKILL.md`)

- `.claude/skills/meaningful-game-mechanics/SKILL.md:3` [S-45] ...omeone proposes achievements, scores, timers, drag gestures or Minecraft assets, or when a device must pass the swap-the-subject test and the ethics checks.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:8` [S-45] ...SIONS.md' (2026-10-18); the register wins.** Decided there: no Mojang textures, sounds, UI or footage in the public cut, original voxel assets only (D-23); playable pieces are an optional co...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:16` [S-45] ...hapter: reveal, map, inventory, conversation, routine, pacing, voxel scene.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:18` [S-45] ...evels, progress bars, timers, a fail state, drag gestures or a Minecraft asset.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:27` [S-45] - Legal questions about Minecraft or venues. Flag them for the maker and a lawyer. Do not answer them as legal advice.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:41` [S-45] ...ault is OUT of the public cut. A locked chapter can follow the Minecraft Vault pattern: it opens once and only with its own key [55]; W-37 defaults to three visibly unfinished places and an ...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:42` [S-45] 11. Apply the IP rule (D-23). No Mojang textures, models, sounds, UI or footage appear in the public cut; original voxel assets only, and the name at most as a secondary description with the...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:57` [S-45] - [ ] No Minecraft asset, or the terms check is recorded.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:75` [S-45] - [ ] Minecraft terms re-read on the day of the showing, with the date recorded.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:76` [S-45] - [ ] No Mojang logo, and no claim of official status. A disclaimer is used.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:104` [S-45] - **Minecraft terms.** Permissions can be revoked at any time. Mojang's wording treats sharing with the community as commercial. Selling copies is not allowed, and endorsement must not be im...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:138` [S-45] [42] Mojang/Microsoft — Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18; no visible date — [P].
- `.claude/skills/meaningful-game-mechanics/SKILL.md:139` [S-45] [43] Mojang/Microsoft — Minecraft End User License Agreement — https://www.minecraft.net/en-us/eula — fetched 2026-10-18 — [P].
- `.claude/skills/meaningful-game-mechanics/SKILL.md:141` [S-45] [49] Blockbench — https://blockbench.net/ — fetched 2026-10-18 — [P].
- `.claude/skills/meaningful-game-mechanics/SKILL.md:142` [S-45] [50] Blockbench README — https://cdn.jsdelivr.net/gh/jannisx11/blockbench@master/README.md — fetched 2026-10-18 — [P] GPL-3.0; assets are yours.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:143` [S-45] [51] VoxelFans — MagicaVoxel page (third-party) — https://voxelfanscom.nuxt.dev/magicaVoxel — fetched 2026-10-18 — [T] "free for personal and commercial use"; superseded by [76] (official si...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:144` [S-45] [55] Minecraft Wiki — Vault — https://minecraft.wiki/w/Vault — fetched 2026-10-18.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:145` [S-45] [57] Salon (from The Daily Dot) — "Gamer uses 'Minecraft' to pay tribute to his wife" — https://salon.com/2014/03/13/gamer_uses_minecraft_to_pay_tribute_to_his_wife_partner — 2014-03-13 — [S...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:146` [S-45] [58] Everplans — Adam Seifer, "Minecraft video game memorial honors loved one" — https://everplans.com/articles/minecraft-video-game-memorial-honors-loved-one — undated — [S] cites a Reddit ...
- `.claude/skills/meaningful-game-mechanics/SKILL.md:147` [S-45] [64] Game Developer — Zach Soares, "Voxel Art: Reducing the Greebles" — https://www.gamedeveloper.com/design/voxel-art-reducing-the-greebles — 2017-06-05.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:148` [S-45] [65] 80.lv — Gabriel de Laubier, "Using Voxels for Simple Dioramas" — https://80.lv/articles/using-voxels-for-simple-dioramas — 2017-07-26.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:149` [S-45] [76] MagicaVoxel official site, main page fragment (the licence block and changelog) — https://ephtracy.github.io/mv_main.html — [P] version 0.99.7.2.
- `.claude/skills/meaningful-game-mechanics/SKILL.md:150` [S-45] [77] MagicaVoxel official site, Commands page — https://ephtracy.github.io/mv_commands.html — [P].

**`.claude/skills/surprise-tribute-operations/SKILL.md`** (staged: `skills-staging/surprise-tribute-operations/SKILL.md`)

- `.claude/skills/surprise-tribute-operations/SKILL.md:8` [S-38] ...03, W-08). Covert collection starts Sun 15 Nov 2026, after the L1 process lock (D-13, W-10).
- `.claude/skills/surprise-tribute-operations/SKILL.md:45` [S-64] ...t of the public cut, full stop; the her-turn conversation (Sat 6 Mar 2027) is the only way back in. If the maker is part of the story on an item, Fable's flag is read twice and the item defa...
- `.claude/skills/surprise-tribute-operations/SKILL.md:47` [S-64] ...orded. Dates (W-48, D-06): releases 4d to 4g Sun 28 Feb to Sat 6 Mar; her turn Sat 6 Mar; response recordings Sun 7 Mar to Sat 10 Apr; consent ledger closed Mon 29 Mar; April version deliver...
- `.claude/skills/surprise-tribute-operations/SKILL.md:84` [S-61] - [ ] Calendar clashes checked by the maker (the proxy): Ramadan [72], Lunar New Year [73]
- `.claude/skills/surprise-tribute-operations/SKILL.md:164` [S-61] [72] The National (UAE), "Ramadan 2027 dates" — https://www.thenationalnews.com/news/uae/2026/09/09/ramadan-2027-dates-eid-al-fitr-holiday/ — 2026-09-09, updated 2026-10-06 — fetched — Astro...
- `.claude/skills/surprise-tribute-operations/SKILL.md:166` [S-61] [73] ChinaTravel, Chinese New Year 2027 — https://www.chinatravel.com/chinese-new-year/date — undated — snippet only — Lunar New Year Sat Feb 6, 2027

**`.claude/skills/theatrical-delivery-and-rights/SKILL.md`** (staged: `skills-staging/theatrical-delivery-and-rights/SKILL.md`)

- `.claude/skills/theatrical-delivery-and-rights/SKILL.md:53` [S-48] ...en or a written RISK entry; no unlicensed commercial music; no Mojang assets. T3 (online): releases signed and the maker's explicit yes. T4 (cinema or festival): all T3 rows green, releases ...
- `.claude/skills/theatrical-delivery-and-rights/SKILL.md:86` [S-48] - [ ] No Mojang name, asset or footage; no third-party game footage.
- `.claude/skills/theatrical-delivery-and-rights/SKILL.md:113` [S-48] - Games and brands: no Mojang textures, sounds, UI or footage. "Minecraft" appears only as a secondary description, with the disclaimer [48].
- `.claude/skills/theatrical-delivery-and-rights/SKILL.md:123` [S-48] ...ps://files.isdcf.com/papers/ISDCF-Doc3-Delivery-Recs.pdf [26]; Minecraft Usage Guidelines https://www.minecraft.net/en-us/usage-guidelines [48]; Sundance FAQ https://www.sundance.org/submiss...
- `.claude/skills/theatrical-delivery-and-rights/SKILL.md:152` [S-48] - [48] Minecraft Usage Guidelines — https://www.minecraft.net/en-us/usage-guidelines — fetched 2026-10-18 about 07:00 GMT; no visible date — physical locations, 150 participants, sharing equ...

### 3c. Other residuals in playbooks

- `playbooks/production-scale.md:61` [S-17] stale commentary: says `playbooks/film-story.md` "still carry four chapters of 2:15 for 12 minutes"; film-story.md no longer has that row (grep: no "2:15" row), and the same sentence goes on to say W-04 resolved it. Delete the "still carry" clause.
- `playbooks/gujarati-devotional-sound.md:363` [pending/appended] unresolved note in Template J: "The sibling's patch list also says questions 21 to 28 are to be appended to the theatrical playbook's T10 (Changelog conflict). That must be reconciled." T10 in theatrical-delivery.md now runs 1 to 43 once (W-55), questions 26 to 28 are the sound track's, 29 to 40 match Template J. The note is closed; delete it.

## 4. Section-marker check: "pending", "for the scribe", "appended"

Searched headings and body text in the scoped files for `pending`, `for the scribe`, `pending scribe`, `appended`, `to be appended`, `not applied`, `Proposed changes`, `Deltas to existing`, `so that a scribe can patch`, `TODO(orchestrator)` and `must be reconciled`.

- **"For the scribe", "pending scribe", "Deltas to existing", "so that a scribe can patch":** none outside Changelogs. `playbooks/theatrical-delivery.md:581` is now "Record of deltas to other playbooks" with a Status column (S-40), as Table 4 says.
- **Residual: sections still headed as undone work**, both inside Changelogs:
  - `playbooks/mobile-delivery.md:492` heading "### Proposed changes to existing files (not applied)" (inside the Changelog) contradicts its own status line ("applied by the scribes and tracked in Table 4; this list stays as the record"). Retitle it as a record, or remove it.
  - `playbooks/pushtimarg-world.md:574` Changelog bullet "Suggested changes to existing files, not applied." with a status line saying the other rows are applied by their owners. Same fix: retitle as a record.
- **Residual (body text, not Changelog):** `playbooks/gujarati-devotional-sound.md:363` (section 3c).
- **Delta-record tables with open rows (known; tracked in Table 4, not residual here):** `playbooks/theatrical-delivery.md` 581 to 613 (three rows still **outstanding**: `toolchain.md` Step 13, `agent-pipeline.md` Gate G6, `ai-imagery.md` cue-sheet extensions; the fourth S-40 row, `games.md` Q7/F4, now reads "retired 2026-10-19", so Table 4 S-40 still saying "four rows" is one behind), `playbooks/devotional-sound-script.md` T-12 at 398 to 420, `playbooks/gujarati-devotional-sound.md` 562 to 580, `playbooks/saurashtra-world.md` 706 to 735 (inside its Changelog). Their open rows cite S-42, S-51, S-52 and S-54. These are records with a Status column, not scribe to-do lists.
- **Not a scribe marker:** `ROADMAP.md:293` "## 10. Budget (rough; ceiling pending, O-04)" is the maker's open budget answer; `ROADMAP.md:279` "(pending)" is the Sun 25 Oct sitting row for O-01 to O-04; `ROADMAP.md:348` "rows appended to the model" is a past-tense statement about `model.csv`; `skills-staging/meaningful-game-mechanics/SKILL.md:44` "Append one row to design/devices-log.md" is an instruction to the user of the skill.
- **Changelog-excepted, noted for completeness:** the v0.1 bullet at `playbooks/devotional-sound-script.md:715` to `:723` still reads "O-42 and O-43 are not yet rows. The orchestrator must enter them." and "Reconcile the two before either is run" (the S-65 phrase); the later bullets resolve both (O-rows re-keyed to Table 3; one shaping gate run once at P-LOCK). `playbooks/mobile-delivery.md:488` carries "TODO(orchestrator)" followed by "Resolved 2026-10-19".

## 5. Duplicate IDs in `DECISIONS.md`

Parsed every table row whose first cell is an ID (`D-`, `W-`, `O-`, `S-`): 31 D, 79 W, 65 S, 73 O rows = 248 rows, 248 unique IDs. **No duplicates.** Absorbed IDs named in parentheses in O-rows (for example O-06 absorbs O-40) were checked against the row IDs: none is also its own row, and none is claimed by two rows. `O-66 (absorbs O-53; with O-44)` mentions O-44 as a pairing, not an absorption; O-44 is its own row at line 225. Every number from 1 to the maximum is either a row or an absorbed ID in each family (O: 1 to 84). The O-row bound check (any `O-85` or higher in scope files) found none.

Observation outside the register: `playbooks/hindu-visual.md:380` and `playbooks/pushtimarg-world.md:464` say the exclusion-list numbers E27 to E34 collide between the two playbooks; both say they are cited with their file and reconcile at G1. Documented and deferred, so not residual.

## 6. Specific haveli or temple she attends; identifying data

- No haveli or temple is named as hers. Phrases such as "her haveli", "her mandir" and "a small temple or haveli she walks to" appear only as questions to the maker or as placeholders, with the answer kept offline (for example `playbooks/saurashtra-world.md:395` O-55 "by what it is, not where").
- Public landmarks are named as place and tradition leads, never as hers: Nathdwara and Shrinathji (the head seat of the tradition), Takhteshwar, Nishkalank Mahadev and Gopnath Mahadev (Bhavnagar district), Somnath, Dwarka, Ambaji (`playbooks/saurashtra-world.md` 10, 94 to 100, 465; `playbooks/hindu-visual.md` 174, 188, 527). `playbooks/saurashtra-world.md:10` reads "Her district's spine is Shiva, the sea and Krishna's rasa. Takhteshwar, Nishkalank Mahadev and Gopnath Mahadev are three Shaiva settings in Bhavnagar district". That is within "places and traditions in general", but it pairs her district with three named temples; the maker may want to confirm they are content with that under D-26 and O-69. Nothing says she attends any of them.
- No email addresses, phone numbers or street addresses of the family. `playbooks/surprise-ops.md:334` carries a film lab's public business contact (a vendor, from its published page). `PLAN-ON-A-PAGE.md:19` and the agent-pipeline and agent-first skills restate the rule itself.

## 7. Reviewed and not residual

Counts of lines outside Changelogs, by class. Each class was read in context, not accepted on pattern alone.

| Class | Lines | Meaning |
|---|---|---|
| NEG | 46 | The line says the term is dropped, retired, not hers, or absent (W-29 allowlist convention: "Minecraft is dropped", "there is no co-keeper", "there is no insider", "Chhath is not hers") |
| REF | 4 | `ROADMAP.md` lines that quote the stale value to describe the cleanup risk or the outstanding S-rows (349, 361, 398, 420) |
| BYDESIGN | 29 | S-01 only: a 25 fps value marked "tested at 25, UNVERIFIED at 24", a "made at 25 fps and not re-measured" estimate, or the 50 Hz access-copy exception. Table 4 keeps S-01 outstanding until r1, r5 and the colour-patch test are re-run at 24 |
| OK | 207 | Placeholder or conditional wording the register allows (contributors void unless TD-L2c, option rows with a "decided" note, "Fri 5 Feb only if she keeps Maha vad Amas", Sun 7 Mar), a superseded-value note, or a bibliographic entry |
| FP | 163 | A different meaning: PH1/PH2 and deity class P1/P2, `[P1]` source tags, E1-S1/E1-S2, stranger screening S1/S2, "decision 11" as `hindu_idiom`, "Gujarati New Year", "Yamuna Chhath", Business Insider, `H-1-row` in a Python file |
| ALLOW | 1 | `playbooks/music-sound.md:142` "not applied here" (allowlist AL-1) |

Line lists (file: line numbers) for the two classes that carry the most judgement:

**NEG (retirement or negation statements)**

- `.claude/skills/life-film-music-and-sound/SKILL.md`: 12
- `.claude/skills/life-film-story-structure/SKILL.md`: 12
- `.claude/skills/life-story-interviewing/SKILL.md`: 68, 128
- `.claude/skills/life-story-interviewing/beat-sheet.md`: 23
- `.claude/skills/life-story-interviewing/surprise-runbook.md`: 9
- `.claude/skills/surprise-tribute-operations/SKILL.md`: 38, 48
- `ROADMAP.md`: 52, 377, 379, 425
- `playbooks/ai-imagery.md`: 17, 27, 245, 350, 450
- `playbooks/craft-motion.md`: 10
- `playbooks/format.md`: 45, 292
- `playbooks/story.md`: 135, 149, 243, 301
- `playbooks/surprise-ops.md`: 5, 28, 63, 72, 206, 383, 567, 568
- `skills-staging/ai-photo-to-animation-pipeline/SKILL.md`: 63
- `skills-staging/journey-format-architecture/SKILL.md`: 33, 125
- `skills-staging/life-film-music-and-sound/SKILL.md`: 12, 58, 107
- `skills-staging/life-film-story-structure/SKILL.md`: 12
- `skills-staging/life-story-interviewing/SKILL.md`: 8, 68, 128
- `skills-staging/surprise-tribute-operations/SKILL.md`: 8, 38, 48
- `skills-staging/theatrical-delivery-and-rights/SKILL.md`: 113

**REF (names the stale term to describe the cleanup)**

- `ROADMAP.md`: 349, 361, 398, 420

**BYDESIGN (S-01, tested at 25, UNVERIFIED at 24)**

- `.claude/skills/craft-apps-motion-refinement/SKILL.md`: 64
- `.claude/skills/free-creative-toolchain/SKILL.md`: 60
- `.claude/skills/free-creative-toolchain/recipes/r1_kenburns.sh`: 9, 10, 11, 21, 22, 24, 25
- `.claude/skills/free-creative-toolchain/recipes/r2_parallax.py`: 49
- `.claude/skills/free-creative-toolchain/recipes/r5_story.mlt`: 5, 6, 9, 12
- `playbooks/agent-pipeline.md`: 175, 301
- `playbooks/craft-motion.md`: 305, 321, 322
- `playbooks/theatrical-delivery.md`: 547, 679
- `playbooks/toolchain.md`: 8, 84, 90, 107, 126
- `skills-staging/craft-apps-motion-refinement/SKILL.md`: 65
- `skills-staging/free-creative-toolchain/SKILL.md`: 12, 60

**OK (allowed wording, superseded notes, citations)**

- `.claude/skills/animation-production-planning/SKILL.md`: 51, 81
- `.claude/skills/cinematic-quality-bar/SKILL.md`: 115
- `.claude/skills/journey-format-architecture/SKILL.md`: 51, 149
- `.claude/skills/life-film-story-structure/SKILL.md`: 31, 197, 211
- `.claude/skills/life-story-interviewing/SKILL.md`: 48
- `.claude/skills/life-story-interviewing/session-protocol.md`: 10
- `.claude/skills/life-story-interviewing/surprise-runbook.md`: 14, 54
- `.claude/skills/surprise-tribute-operations/SKILL.md`: 85
- `QUESTIONS-SUN-25-OCT.md`: 109
- `ROADMAP.md`: 14, 91, 100, 124, 170, 180, 197, 200, 209, 210, 211, 213, 232, 239, 347, 355, 378
- `playbooks/agent-pipeline.md`: 300, 306, 390, 391
- `playbooks/animated.md`: 169, 173, 180, 182
- `playbooks/craft-motion.md`: 311, 326
- `playbooks/creator-threads.md`: 104, 164
- `playbooks/devotional-sound-script.md`: 163, 167, 374, 405, 422, 452, 654, 663, 664, 708
- `playbooks/film-story.md`: 5, 23, 35, 276, 351, 424, 436, 538, 558
- `playbooks/format.md`: 13, 17, 51, 61, 87, 113, 183, 195, 200, 205, 221, 237, 269, 271, 302, 304, 380
- `playbooks/games.md`: 170
- `playbooks/gujarati-devotional-sound.md`: 1, 42, 133, 399, 401, 407, 433, 463, 476, 478, 479, 482, 494, 519, 520, 538
- `playbooks/hindu-frameworks.md`: 15, 165, 170, 172, 303
- `playbooks/hindu-visual.md`: 412
- `playbooks/mobile-delivery.md`: 26, 265, 336
- `playbooks/music-sound.md`: 309, 539
- `playbooks/production-scale.md`: 31, 38, 61, 110, 242, 262, 450, 476, 565, 613, 614, 644, 662, 663, 671, 686, 696, 704, 715, 763
- `playbooks/pushtimarg-world.md`: 178, 499, 512
- `playbooks/saurashtra-world.md`: 150, 164, 168, 236, 238, 239, 299, 354, 380, 401, 439, 465, 477, 479, 533, 569
- `playbooks/story.md`: 75, 138, 140, 150, 154, 254
- `playbooks/surprise-ops.md`: 55, 115, 162, 192, 193, 287, 288, 290, 293, 302, 303, 357, 434, 479, 492, 499, 570, 574, 577, 771
- `playbooks/theatrical-delivery.md`: 171, 361, 372, 456, 462
- `playbooks/toolchain.md`: 154
- `skills-staging/animation-production-planning/SKILL.md`: 51, 73, 81
- `skills-staging/cinematic-quality-bar/SKILL.md`: 117
- `skills-staging/devotional-music-and-indic-scripts/SKILL.md`: 44, 112
- `skills-staging/gujarati-pushtimarg-music/SKILL.md`: 127, 129, 130, 133, 145, 170, 171, 189
- `skills-staging/hindu-visual-language/SKILL.md`: 92
- `skills-staging/journey-format-architecture/SKILL.md`: 12, 45, 51, 151
- `skills-staging/life-film-story-structure/SKILL.md`: 31, 127, 202, 216
- `skills-staging/life-story-interviewing/SKILL.md`: 48, 70
- `skills-staging/mobile-phone-delivery/SKILL.md`: 61
- `skills-staging/saurashtra-gujarati-world/SKILL.md`: 39
- `skills-staging/surprise-tribute-operations/SKILL.md`: 45, 47

**FP (other meaning)**

- `.claude/skills/cinematic-quality-bar/SKILL.md`: 136
- `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py`: 20
- `.claude/skills/life-film-story-structure/SKILL.md`: 139, 209, 210
- `ROADMAP.md`: 84, 168, 171, 280, 282, 350, 351, 360, 401, 424
- `playbooks/agent-pipeline.md`: 64, 214, 246
- `playbooks/ai-imagery.md`: 207
- `playbooks/animated.md`: 202
- `playbooks/cinematic-quality.md`: 33, 58, 61, 167, 304, 370, 393, 395, 421, 437, 480, 483, 496, 500, 648, 656, 658, 669, 671, 677, 681, 707, 708, 733, 766, 851, 852
- `playbooks/craft-visual.md`: 32
- `playbooks/devotional-sound-script.md`: 396, 522, 543, 565
- `playbooks/film-story.md`: 7, 43, 56, 67, 191, 212, 215, 264, 317, 362, 389, 426, 444, 445, 450, 460, 480, 556, 557
- `playbooks/format.md`: 80, 300
- `playbooks/gujarati-devotional-sound.md`: 237, 547
- `playbooks/hindu-frameworks.md`: 156, 187, 200, 301
- `playbooks/hindu-visual.md`: 7, 20, 23, 30, 36, 47, 53, 61, 138, 142, 151, 155, 186, 187, 188, 189, 190, 191, 219, 224, 244, 333, 380, 430, 434, 435, 472, 474, 477, 479, 493
- `playbooks/mobile-delivery.md`: 319
- `playbooks/music-sound.md`: 540
- `playbooks/production-scale.md`: 472
- `playbooks/pushtimarg-world.md`: 42, 99, 113, 114, 122, 251, 272, 464
- `playbooks/saurashtra-world.md`: 146, 147, 240, 296, 336, 362, 387, 512, 539
- `playbooks/theatrical-delivery.md`: 96, 287
- `skills-staging/agent-first-production-pipeline/SKILL.md`: 35
- `skills-staging/ai-photo-to-animation-pipeline/SKILL.md`: 54, 120
- `skills-staging/animated-biography-patterns/SKILL.md`: 39, 88, 143
- `skills-staging/cinematic-quality-bar/SKILL.md`: 36, 38, 70, 119, 140
- `skills-staging/craft-apps-visual-refinement/SKILL.md`: 61
- `skills-staging/gujarati-pushtimarg-music/SKILL.md`: 198
- `skills-staging/hindu-life-story-frameworks/SKILL.md`: 98
- `skills-staging/hindu-visual-language/SKILL.md`: 8, 12, 17, 36, 40, 64, 90, 105
- `skills-staging/life-film-story-structure/SKILL.md`: 144, 214, 215
- `skills-staging/mobile-phone-delivery/SKILL.md`: 80
- `skills-staging/pushtimarg-seva-and-pichwai/SKILL.md`: 30, 36
- `skills-staging/saurashtra-gujarati-world/SKILL.md`: 34, 51, 107

### Retired terms with no live hit outside the installed skills (section 3 lists those)

`MapartCraft` (no hit anywhere in scope), `Pongal` and `Kaanum Pongal` (none), `Ash Wednesday`, `Ramadan`, `Hanukkah`, `Thanksgiving`, `Christmas` and `Lunar New Year` (Changelog bullets and the installed skills named in section 3b only), "P1, the phone master", "P2, the small copy", "P1 by cable" (the only P1 and P2 uses are the deity classes and `[P1]` source tags), "the T2 rule" (only `ROADMAP.md` 361 and 398, naming the rename), "H-1 to H-7", "S1/S2" as sound source classes (only the rename notes at `playbooks/gujarati-devotional-sound.md:547` and `skills-staging/gujarati-pushtimarg-music/SKILL.md:198`), "photograph of a three-dimensional murti" and "the maker's own photograph of a three-dimensional murti on her shelf" (the P3 definition is the allowlisted AL-5 line in the pushtimarg-world research note, out of scope), "shown without him it changes meaning", "dark line of the river", "one room sound" and "one true room sound" (only the installed `beat-sheet.md:10`, section 3a), style-bible "decision 11" meaning moving footage, "may slip a week for Hanukkah" (Changelog only), "a relative's public-domain performance" in the premiere spine (Changelog and "left the premiere spine" notes only), "Saal Mubarak" used on a card (flagged and not used everywhere; offered only as the question in O-61, as the register has it), "haveli sangeet" as an on-screen label (internal term only; O-73), "Mataji" for her (never used for her), "Minecraft capture" and "Goxel as a tool choice" in playbooks and staged skills, and any `O-85` or higher.

## 8. Script versus independent grep

- Script FAIL lines outside its own changelog test, in this scope: 146 distinct lines. The independent grep agrees that 93 of them are residual (all in installed skills). The other 53 are not residual after reading: 42 are negations, superseded notes, option rows with a "decided" note or citations (patterns S-09, S-10, S-11, S-17 to S-20, S-26, S-28, S-31), 9 are S-01 by-design lines, 1 is a Changelog sub-bullet (`playbooks/devotional-sound-script.md:723`, which the script does not see as Changelog), and 1 is a negation (`skills-staging/life-story-interviewing/SKILL.md:8`, "the closest insider does not exist"). Full line list: the OK, BYDESIGN and NEG blocks in section 7.
- The script missed these residuals in installed skills (its patterns have no row for them):
  - `.claude/skills/animation-production-planning/SKILL.md:147`: [94] Wikipedia Chinese New Year source line
  - `.claude/skills/creator-recipe-library/SKILL.md:41`: "(L1, Sat 14 Nov; D-13)" for the process lock
  - `.claude/skills/creator-recipe-library/SKILL.md:137, 161`: Replay Mod documentation entries
  - `.claude/skills/free-creative-toolchain/SKILL.md:10, 148`: voxel recipe filenames; "voxelising"
  - `.claude/skills/free-creative-toolchain/recipes/r4_photo2vox.py:6, 7`: Goxel and Blender chain comments
  - `.claude/skills/free-creative-toolchain/recipes/r4_render_voxel.py:5, 6, 7, 10, 12, 33`: Goxel/voxel comments and code
  - `.claude/skills/free-creative-toolchain/references.md:51`: Goxel 0.11.0 in the tested-tools line
  - `.claude/skills/journey-format-architecture/SKILL.md:12`: "offline scrubber page as the companion"
  - `.claude/skills/life-story-interviewing/SKILL.md:145`: "still carries insider and consent-card lines" (the runbook has since been patched)
- Suggested additions to `scripts/stale_patterns.json` (the build sprint owns it, so this is a note, not an edit): `Replay ?Mod`, `\bGoxel\b` and `voxelis` under S-46, `\(L1, Sat 14 Nov`, `Chinese New Year` under S-61, `scrubber page as the companion` under S-44, and `still carries .{0,20}insider` under S-08. The script does catch `beat-sheet.md:10` (reported under S-51).

## 9. Changelog mentions excepted

98 hit lines sit under a `## Changelog` heading and are excepted: 8 of them are live-looking mentions in installed-skill Changelogs (`agent-first-production-pipeline` 128, `cinematic-quality-bar` 176, `craft-apps-motion-refinement` 193, `craft-apps-visual-refinement` 161, `creator-recipe-library` 185, `free-creative-toolchain` 173, `life-story-interviewing` 181, `meaningful-game-mechanics` 154; the staged copies keep their own Changelog lines, which are history), the rest are Changelog bullets that name a retired term to say it was retired (Hanukkah, Lunar New Year, Chhath, the 25-minute plan, "L1 process lock" becomes P-LOCK). By file: `.claude/skills/agent-first-production-pipeline/SKILL.md` 1; `.claude/skills/ai-photo-to-animation-pipeline/SKILL.md` 1; `.claude/skills/cinematic-quality-bar/SKILL.md` 1; `.claude/skills/craft-apps-motion-refinement/SKILL.md` 1; `.claude/skills/craft-apps-visual-refinement/SKILL.md` 1; `.claude/skills/creator-recipe-library/SKILL.md` 1; `.claude/skills/free-creative-toolchain/SKILL.md` 1; `.claude/skills/life-film-story-structure/SKILL.md` 1; `.claude/skills/life-story-interviewing/SKILL.md` 1; `.claude/skills/meaningful-game-mechanics/SKILL.md` 1; `.claude/skills/surprise-tribute-operations/SKILL.md` 1; `ROADMAP.md` 2; `playbooks/agent-pipeline.md` 1; `playbooks/ai-imagery.md` 2; `playbooks/animated.md` 3; `playbooks/cinematic-quality.md` 2; `playbooks/craft-motion.md` 2; `playbooks/creator-threads.md` 3; `playbooks/devotional-sound-script.md` 2; `playbooks/film-story.md` 3; `playbooks/format.md` 4; `playbooks/games.md` 4; `playbooks/gujarati-devotional-sound.md` 5; `playbooks/hindu-frameworks.md` 2; `playbooks/hindu-visual.md` 6; `playbooks/mobile-delivery.md` 3; `playbooks/music-sound.md` 1; `playbooks/production-scale.md` 3; `playbooks/pushtimarg-world.md` 4; `playbooks/saurashtra-world.md` 4; `playbooks/story.md` 4; `playbooks/surprise-ops.md` 5; `playbooks/toolchain.md` 2; `skills-staging/agent-first-production-pipeline/SKILL.md` 1; `skills-staging/ai-photo-to-animation-pipeline/SKILL.md` 1; `skills-staging/cinematic-quality-bar/SKILL.md` 1; `skills-staging/craft-apps-motion-refinement/SKILL.md` 1; `skills-staging/craft-apps-visual-refinement/SKILL.md` 1; `skills-staging/creator-recipe-library/SKILL.md` 1; `skills-staging/free-creative-toolchain/SKILL.md` 1; `skills-staging/hindu-life-story-frameworks/SKILL.md` 1; `skills-staging/hindu-visual-language/SKILL.md` 1; `skills-staging/journey-format-architecture/SKILL.md` 1; `skills-staging/life-film-music-and-sound/SKILL.md` 1; `skills-staging/life-film-story-structure/SKILL.md` 1; `skills-staging/life-story-interviewing/SKILL.md` 2; `skills-staging/meaningful-game-mechanics/SKILL.md` 2; `skills-staging/pushtimarg-seva-and-pichwai/SKILL.md` 1; `skills-staging/saurashtra-gujarati-world/SKILL.md` 1; `skills-staging/surprise-tribute-operations/SKILL.md` 2.

## 10. Method and limits

- Independent scan: a Python script in the scratchpad (not in the repo) with 87 patterns written from the Table 4 "Stale value" column and the retired-term list in the task, deliberately broader than the script (case-insensitive, no word boundaries on the D-29 terms), run line by line over the scoped files. Every non-Changelog hit was classified by reading it (section 7), with `Read`-level context for the borderline ones (`playbooks/animated.md:180`, `playbooks/production-scale.md:61` and `:671`, `.claude/skills/life-story-interviewing/surprise-runbook.md:14` and `:54`, `.../session-protocol.md:10`).
- Staged coverage: each `.claude/skills/<skill>/<file>` was mapped to `skills-staging/<skill>/<file>` and the staged file was searched for the same patterns. Staging holds only `SKILL.md` files. The staged hits that remain, all read and found to be canonical wording or negations, are: `animation-production-planning` 73 (lock Fri 5 Feb only if she keeps Maha vad Amas), `journey-format-architecture` 12 (scrubber demoted), 33 and 125 (Minecraft is dropped), `life-film-music-and-sound` 58 and 107, `theatrical-delivery-and-rights` 113 (Minecraft is dropped), `life-story-interviewing` 8, 68 and 128 (no insider) and 70 (her turn Sun 7 Mar), `surprise-tribute-operations` 45 and 47 (her turn Sun 7 Mar).
- Not checked: that each Table 4 **canonical** value is present (this is a stale-value check), the research notes, reviews, `build/`, `scripts/`, `tests/`, fixtures, and anything under `spikes/`, `ops/`, `win/` (owned by the build sprint). Table 4 rows S-52, S-53 and S-60 have no machine pattern in the script; S-53 and S-52 were checked here by reading the music-sound and film-story hits only.
- Files were being edited by parallel passes during the session; the tree fingerprint above is the state this report describes. Re-run after the install of the staged skills: the expected residue is then section 3a, section 3c and section 4 only.
