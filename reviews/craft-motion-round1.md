# Review: track `craft-motion`, round 1 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:**
- `research/craft-motion.md` (researcher Sonnet, 2026-10-18)
- `playbooks/craft-motion.md` (scribe Haiku, draft v1, 2026-10-18)
- `.claude/skills/craft-apps-motion-refinement/SKILL.md`
- against `CHARTER.md` and my brief review `reviews/01-addendum-briefs-review.md` (Part 2.2 is the brief this track answered)

**Verdict: REVISE.** Nothing critical is open. Accuracy is the best I have seen on this project: every claim I spot-checked matched its source exactly. The revision is about *meaning* and *usability*: the two artefacts people will actually act on (the playbook and the skill) describe the maker's refinement pass as a purely mechanical operation and never say what the human hand is for, and the skill points to a recipe that is not where it says it is.

---

## 0. What I verified (method and results)

Method, this container, 2026-10-18: the researcher's shallow clones were still in the scratchpad (`filmcraft` at `f03e2155` = v0.8.0, `effectcraft` at `2a012268` = v0.11.1, `soundcraft` at `2578ea69` = v0.8.0; I confirmed the commits with `git log -1` and `git describe`). I also re-fetched nine cited files from `raw.githubusercontent.com` at the tags, downloaded the three `SHA256SUMS.txt` files with curl, fetched the Kdenlive, getartcraft and Blackmagic pages with curl, and read three GitHub issue pages with WebFetch (summarised by a small model, as the researcher did). Everything fetched was treated as data. Nothing was built or run.

| # | Claim (where) | Source checked | Result |
|---|---|---|---|
| 1 | Five SHA-256 values in the pin tables (research Q1, playbook Template A, skill step 2) | `SHA256SUMS.txt` of filmcraft v0.8.0, v0.7.2 and effectcraft v0.11.1 | **All five match byte for byte** (FilmCraft win-x64 portable `0119af…`, Linux tar.gz `b16687…`, v0.7.2 portable `8e22fa…`; EffectCraft portable `78bd7f…`, tar.gz `b9cb2c…`). The two web-zip hashes in R8 also match |
| 2 | `.fcproj` schema is **15** at v0.8.0, not 13 (research Summary 3; corrects my review 01) | `filmcraft/crates/format/src/lib.rs` @v0.8.0 | Confirmed: `SCHEMA_VERSION = MIGRATIONS.len() + 1`; a test asserts `SCHEMA_VERSION == 15`. `docs/project-files.md` still shows `"schema_version": 13` and its table stops at 13 (stale, as stated) |
| 3 | 254,016,000,000 ticks per second (research Q2, skill step 4) | `filmcraft/crates/time/src/lib.rs` @v0.8.0 | Confirmed: `pub const TICKS_PER_SECOND: i64 = 254_016_000_000`. Derived values (5 s = 1,270,080,000,000; 25 fps frame = 10,160,640,000) are arithmetically right |
| 4 | Stills decode to 8-bit RGBA, no EXIF orientation, no ICC (research Summary 7, playbook principle 3, skill step 3) | `filmcraft/crates/media/src/still.rs` @v0.8.0 | Confirmed: `img.to_rgba8()`; the file contains no reference to EXIF, orientation or ICC |
| 5 | Scale 100 = native pixels; `scale_to_frame` multiplies a fit-inside factor; position origin top-left with centre default (research Q2 item 4, skill step 4) | `filmcraft/crates/render/src/lib.rs` `motion_matrix` @v0.8.0 | Confirmed: `s = scale / 100`; `if item.scale_to_frame { fit = min(sw/src.w, sh/src.h); scale *= fit }`; default `pos = (sw/2, sh/2)`. The cover/fit numbers 53.3/45.0 and 66.67 are right |
| 6 | OTIO `metadata.filmcraft.effects` with a wrong shape is dropped silently; default sequence 1920x1080 at file rate; `scale_to_frame` defaults false (research Q3, skill step 6) | `filmcraft/crates/interchange/src/otio.rs` @v0.8.0 | Confirmed: `effects_from` does `serde_json::from_value(v).ok()?`; `settings_for(rate, 1920, 1080, false)` fallback; `scale_to_frame … unwrap_or(false)` |
| 7 | FCPXML `<video>`, `<title>`, `<audio>`, `<sync-clip>`, `<mc-clip>` are skipped with a warning (research Q3) | `filmcraft/crates/interchange/src/fcpxml.rs` @v0.8.0 line 402 | Confirmed, plus `live-drawing`. **Nuance the note misses:** line 386 reads a `<video ref=…>` nested inside a `<clip>`; only a bare storyline-level `<video>` is skipped. See nudge 5 |
| 8 | `file.newSequence` default fps is 23.976 (research R2, skill step 7, playbook Exercise 2) | `filmcraft/crates/engine/src/commands.rs` @v0.8.0 | Confirmed: `"fps":f64=23.976` in the parameter document; `FrameRate::FPS_23_976` fallback |
| 9 | `effects.setParam {clip, effect, param, value, time, keyframe}` and the other commands the skill tells agents to run | `commands.rs`, `relink.rs`, `apps/filmcraft-cli/src/main.rs` @v0.8.0 | All exist with those parameters: `effects.setParam` (`time` in ticks, `keyframe` bool), `effects.setInterpolation` (`mediaTime` ticks, names `linear|bezier|autoBezier|continuousBezier|hold|easeIn|easeOut`), `sequence.applyVideoTransition {clip, effect:"cross_dissolve", frames}`, `timeline.place` (`seconds` or `time`, **`duration` in ticks**), `markers.add`, `file.import {paths, imageSequence}`, `media.autoRelink {from,to}`, `file.exportInterchange` formats `edl|xml|fcpxml|otio|aaf|omf`; CLI has `commands`, `describe`, `exec`, `inspect`, `export --preset --start --end --gpu-rendering`, `render --seconds --out`, `--project`, `--save`, `--compact`, `--version`. See nudge 4 on units |
| 10 | Media pool has no memory-pressure eviction (research Summary 7) | `filmcraft/crates/engine/src/media_pool.rs` @v0.8.0 | Consistent: only `insert_file`, `remove`, `clear`; no evict/LRU/budget code |
| 11 | CLI ships in the Windows MSI and portable zip; `portable.txt` in FilmCraft and EffectCraft zips, not SoundCraft (research Q7, playbook Step 4) | `packaging/windows/filmcraft.wxs` (component `FilmcraftCli`), `package.ps1` of all three | Confirmed exactly, including SoundCraft's zip listing only `soundcraft.exe + soundcraft-cli.exe` |
| 12 | EffectCraft expressions run on `boa_engine`; CPU render unless `--gpu`; MSI path; `--autosave` (research Summary 9, Q5, Q7) | `effectcraft/crates/expr/Cargo.toml`, `docs/agents.md` @v0.11.1 | Confirmed verbatim |
| 13 | EffectCraft SVG import exists with exactly that unsupported list (research Summary 10, Q6) | `effectcraft/crates/svg/README.md` @v0.11.1 | Confirmed: "Not supported (ignored): text, images, filters, clip paths, masks, patterns, markers, animation" |
| 14 | CPU export batch = rayon threads clamped 2–16; only a GPU in-flight cap exists at v0.11.1 (research Q7, skill step 10) | `effectcraft/crates/export/src/lib.rs`, `pipeline.rs` @v0.11.1 | Confirmed: `rayon::current_num_threads().clamp(2, 16)`; only `EFFECTCRAFT_GPU_INFLIGHT` |
| 15 | Issue #1615 numbers (36 s/1 thread/2.1 GB; 17 s/4 threads/4.2 GB; >9 GB at 16 threads; 1.8 GB single frame; no `moov`; PR #1763 adds `EFFECTCRAFT_CPU_INFLIGHT`) | github.com/storytold/effectcraft/issues/1615 (WebFetch) | All match; open, "priority: critical", filed 2026-10-16 against 0.10.0 |
| 16 | Issue #2216 (Windows 11, deleted timeline, Ctrl+Z did nothing, maintainer could not reproduce, pointed to Auto-Save) | github.com/storytold/filmcraft/issues/2216 (WebFetch) | Matches. **Also confirms the privacy claim:** the issue was created by the `ticket-craft` GitHub App and its body says it was "submitted through Discord … created by the Ticket Relay integration". 17 of the 25 newest FilmCraft issues are by that bot. So "bug reports via Discord become public issues" is verified, not inferred |
| 17 | Essential Sound ducking writes Volume keyframes; defaults (research Q8) | `filmcraft/crates/project/src/essential.rs` @v0.8.0 | Confirmed (`reduce_db: -15.0`, `fade_s: 0.8`, `sensitivity: 6.0`, against Dialogue) |
| 18 | Export loudness normalisation default -23 LUFS, -2 dBTP, off (playbook Decision 5) | `filmcraft/crates/export/src/settings.rs` @v0.8.0 | Confirmed |
| 19 | Release web zip needs no COOP/COEP headers (research Summary 16, correcting my review 01) | `filmcraft/packaging/web/README.md` @v0.8.0 line 36 | Confirmed: "No special isolation headers". I accept the correction |
| 20 | SoundCraft has no sidechain/key input (G-13) | `soundcraft/docs/gaps.md`, `plugin-parity.md` @v0.8.0 | Confirmed |
| 21 | Kdenlive 26.08.2 released 2026-10-13; docs describe OTIO import as tracks, clips, markers only | kdenlive.org/news/releases/26.08.2/ ("13 October 2026"); docs.kdenlive.org file_menu | Confirmed; the docs section mentions nothing about effects or transitions, as stated |
| 22 | getartcraft.com shows FilmCraft 0.6.0, Launcher 0.3.2, "About 55 video effects" | getartcraft.com/apps/filmcraft (curl) | Confirmed |
| 23 | Resolve 21 free: 8-bit, up to 60 fps, Ultra HD | blackmagicdesign.com/products/davinciresolve (curl) | Confirmed wording |

**Corrections to review 01 Part 0 that I accept** (research Summary 16, Open question 11): schema 15 not 13; no COOP/COEP for the release web zip; EffectCraft does import SVG; GitHub issue and release pages are reachable via WebFetch (not via curl). The orchestrator should treat this review as the amendment.

---

## 1. Scores (track as a whole; per-artefact notes below)

| Criterion | Score | Why |
|---|---|---|
| Meaning | **3** | The research note closes with a real "What this means for Life Journey". But the playbook's Step 9 (the only place where "your hands come in") lists Ken Burns, dissolves, titles, ducking, save: a Premiere tutorial, not a pass over a mother's life. The skill's Quality bar is entirely pixel accuracy. Neither artefact says what the human pass is *for*, so the agents will deliver metronomic 5 s stills with a uniform 12 percent push and the maker will have no instruction to break it. Charter principles 1 and 3 are present only as ethics text |
| Specificity | **5** | Named files, tags, commands, parameter names, hashes, computed values, test names. Exemplary |
| Accuracy | **5** | 23 of 23 spot checks matched. Evidence grades ([T]/[C]/[V]/[I]/[E]) are used honestly; the researcher corrected my own review. One nuance (FCPXML `<video>` inside `<clip>`) and one over-firm sentence in the playbook (nudge 5) |
| Feasibility | **4** | Spike S1 is tightly scoped and cheap; every step has a non-Craft fallback; the hand-off bundle is realistic. One gap: who produces `ch01.xml` if S1 fails (nudge 8) |
| Ethics | **5** | Privacy audit from code; the Discord relay risk is now verified; portable zips and encrypted folder; no synthetic voices; test cards until the pipeline is locked |
| Craft / usability | **4** | Research: long but navigable. Playbook: clear plain English, good exercises and templates. Skill: the description triggers well and the procedure is an executable sequence of commands that exist; but it points to "playbook R5" (no such thing) and leaves units implicit in step 7 |

Per artefact: research note 4/5/5/4/5/4; playbook 3/5/4/4/5/4; skill 3/5/5/4/5/4.

---

## 2. Critical issues

None.

---

## 3. Nudges (eight, each with file, section and exact change)

1. **Playbook, "How to do it", Step 9.** Insert before the bullet list a short "Story pass first" paragraph: *Before touching a keyframe, watch the chapter once with the voice track and ask four things. (a) Which photo carries this chapter? Give it more time than the spec did; the agents give every still the same length. (b) Where is a hard moment (a loss, a leaving)? Cut there, do not dissolve; a dissolve softens, a cut states. (c) Does every move end before the sentence it accompanies ends? If not, shorten the move, not the sentence. (d) Is any face partly cropped? Check the manifest's crop decision for that shot.* Then the existing technical bullets. This is the one place the charter's Principle 1 and 3 can live in this track.

2. **Skill, "Quality bar".** Add to **Good**: "Shot durations vary with the weight of the photo; no two consecutive stills share both duration and move unless the spec says so. Each move ends on or before the end of the voice line it sits under." Add to **Mediocre**: "Every still gets the same 5 s and the same 12 percent push-in." Add to step 5 (neutral spec) the field `weight: 1|2|3` per shot so the agent can vary duration and move amplitude from it.

3. **Skill, "When not to use" (SoundCraft bullet) and Procedure step 1.** Replace "Use the ffmpeg recipe (playbook R5)" with "Use the ffmpeg recipe in `research/craft-motion.md` R5"; the playbook has no numbered recipes. In step 1 change "the research notes (recipes R1 to R8 and the gaps list)" to "the research notes `research/craft-motion.md` (recipes R1 to R8, spike tests T1 to T6, and the Open questions list)". Alternatively, give the playbook a one-line index mapping R1–R8 to its steps; either fix works, do one.

4. **Skill, Procedure step 7, command list.** State the units next to each command as read from `commands.rs` @v0.8.0: `timeline.place` takes `seconds` (f64) *or* `time` (ticks), but `duration` only in ticks; `effects.setParam` `time` is ticks; `effects.setInterpolation` takes `mediaTime` (ticks) and lower-case names `linear|bezier|autoBezier|continuousBezier|hold|easeIn|easeOut` (the capitalised `EaseOut` is the serialised spelling in `.fcproj` and OTIO metadata, not the command spelling). Add the one-line helper `ticks = round(seconds * 254016000000)`.

5. **Playbook, Pitfall 8; research note Summary 5 and Q3 matrix row "Still clip with duration" (FCPXML cell).** The researcher hedged "to my knowledge, not re-checked"; the playbook states "Final Cut often writes stills as `<video>`" as fact. Rewrite the pitfall: "FilmCraft skips FCPXML `<video>` and `<title>` elements that sit directly in a storyline (fcpxml.rs @v0.8.0 line 402); a `<video ref=…>` nested inside a `<clip>` is read (line 386). Whether Final Cut or Resolve writes stills the skipped way is unverified." Add the `<clip>` nuance to the research matrix cell.

6. **Playbook, Exercise 2, step 2.** This is a GUI exercise, so "The CLI's default frame rate is 23.976, so check it" is the wrong register. Replace with: "In the New Sequence dialog pick the 1920x1080 25 fps preset and read the frame rate back before pressing OK. The engine's default for a new sequence is 23.976 (`file.newSequence` @v0.8.0), so never accept a default."

7. **Skill, Procedure step 3 (conform) and step 11 (log); Playbook, Template C and Template H.** Add a renaming rule at conform time: working copies are named by stable shot id (`chNN_sNN.png`), never by the original file name, because OTIO `name` fields, ffprobe JSON, logs and the import report all carry file names and the Discord-to-GitHub relay is now verified (issue #2216). The manifest keeps the mapping id → original path in the private repo. This closes the only leak path the artefacts leave open.

8. **Playbook, Step 7 ("Receive a chapter bundle"); Skill, Procedure step 6, E3.** Say who produces `ch01.xml` when spike S1 fails. Today both texts assume FilmCraft exports it, which needs the Linux CLI in the container. Add: "If S1 fails, the bundle has no `ch01.xml`. After Step 8 the maker exports it from FilmCraft (File > Export > Interchange, FCP7 XML) and that file is what goes into Resolve in Exercise 6." Also add it as a bullet in the skill's "Before a hand-off" checklist ("`chNN.xml` present, or the hand-off note says the maker exports it").

---

## 4. Research follow-ups (facts not in the notes; do not guess)

1. How do current Final Cut Pro and DaVinci Resolve 21 write still images in FCPXML 1.9–1.11: bare `<video>` in the spine, `<clip>`-wrapped `<video>`, or `<asset-clip>`? Decides whether FilmCraft can read a fallback editor's FCPXML at all (nudge 5).
2. Does DaVinci Resolve 21 (free) import FCP7 XML Basic Motion keyframes (scale, position) and Opacity from FilmCraft's exporter? The manual was unreachable; a Blackmagic forum or the Resolve 21 reference PDF (if fetchable) would settle it before the maker's Exercise 6.
3. Kdenlive OTIO import of still-image `ExternalReference`s: does it create image clips with the given duration? Readable in Kdenlive's source (`src/otio/otioimport.cpp` or equivalent in the 26.08 branch) without running anything.
4. Did PR #1763 (`EFFECTCRAFT_CPU_INFLIGHT`) land in an EffectCraft tag after v0.11.1? If yes, the pin candidate and the `RAYON_NUM_THREADS=2` mitigation in the skill change.
5. What does FilmCraft's GUI "New Sequence" dialog default to on Windows (preset and frame rate), as opposed to the engine command default of 23.976? Only the maker's five-minute test can answer; add it to Template B.
6. Still outstanding from review 01: the maker's installed Craft versions and hardware inventory (CPU, RAM, GPU vendor). Half of Q4 and Decision 1 are keyed on these.

---

## 5. Strengths worth keeping

- Twenty-three of twenty-three spot checks matched their sources exactly, including five SHA-256 hashes, the schema number, the tick rate, the JS engine, the SVG unsupported list, an issue's memory figures and a release date. This is the standard the other tracks should meet.
- The evidence grading ([T] test, [C] code only, [V] vendor, [I] issue, [E] estimate) is applied consistently, and the note corrects the advisor's own earlier facts rather than deferring to them.
- The two traps that would have cost the maker days were found by reading code, not docs: stills import at native pixel size (with the cover-scale formula and worked numbers), and malformed `metadata.filmcraft` is dropped silently (with the inspection check that catches it).
- Every step has a named non-Craft fallback, and the SoundCraft verdict is honest to the point of excluding it from delivery.
- The skill's description names concrete triggers (Ken Burns scale, OTIO/FCP7/FCPXML/EDL, pinning, hand-off folders, EffectCraft titles) and concrete exclusions; its procedure is a sequence of commands that exist with the parameters it names.
- The playbook is written for a learner: plain words, one idea per sentence, exercises with "what good looks like", and templates the maker can fill in.

---

## 6. Advisor insight

In a film where every photograph moves, the one that does not move becomes the loudest thing on screen. Give each chapter exactly one **still still**: the photo the chapter's teller (her sister, her oldest friend, her child, per the "told by" structure from review 01) names as *the* picture, shown at fit scale with no Ken Burns, no dissolve in or out, hard cuts both sides, held for the full length of one spoken sentence about it. The agents then build everything else around that anchor: the moves before it drift toward where that photo will sit in the frame, the moves after it drift away. It costs nothing in tooling (it is a `weight: 3` shot with `motion: none` in the spec, which nudge 2 already adds), it gives the maker's Step 9 story pass a concrete job (find the still still, protect it), and it carries straight into a playable version: in the game, the world keeps moving until the player stands in front of that photo, and only then does it stop. Stillness as the mechanic that means "this one mattered".

---

## Changelog
- 2026-10-18: round 1 written by the Fable advisor after verifying 23 claims against repo files at the tags, release checksums, three GitHub issues and three third-party pages. Verdict: revise (meaning 3, craft 4, no critical issues).
