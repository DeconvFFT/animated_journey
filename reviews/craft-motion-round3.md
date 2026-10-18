# Review: track `craft-motion`, round 3 of 3 (final)

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:**
- `research/craft-motion.md` (main note, follow-up round 1 F1-F7, follow-up round 2 G1-G6)
- `playbooks/craft-motion.md` (v1.2, "round 2 review nudges applied")
- `.claude/skills/craft-apps-motion-refinement/SKILL.md`
- against `CHARTER.md`, `reviews/01-addendum-briefs-review.md` (Part 2.2) and my round-2 review `reviews/craft-motion-round2.md`

**Verdict: APPROVE.** All eight round-2 nudges were applied in every file and section I named, and the round-2 researcher's follow-up (G1-G6) closed four of the six open questions with code line numbers and a first-hand OTIO test. Eleven of eleven spot checks today matched their sources. What remains is polish and carry-forward work, listed in Part 4 so the orchestrator can schedule it; none of it blocks the week-1 spike or the maker's first hand-off, and none of it contradicts the charter.

---

## 0. Round-2 nudges: were they addressed?

| # | Nudge (round 2) | Where | Result |
|---|---|---|---|
| 1 | Relative OTIO `target_url`s, no `file://`; Kdenlive `resolveFile` evidence; "Before a hand-off" bullet | Skill step 6 E2, step 8, checklist; Playbook Step 7, Pitfall 6; Research R3 E2 template, "What this means" | **Done.** E2 template now carries `media/ch01_s01.png`, `media/ch01_s02.png`, `media/mix_ch01.wav`; the skill's checklist has "OTIO `target_url`s are relative; no `file://` in the OTIO"; Pitfall 6 cites `otioimport.cpp` lines 390-399 at v26.08.2 and says "not run". One stale sentence survives in the research Risks table (Pitfall 5: "use stable absolute paths under one project root"); see Part 4 item 1 |
| 2 | Replace `RAYON_NUM_THREADS=2` with the F4 measure-first procedure; 6.8 GB figure; PR #1763 does nothing in v0.11.1 | Skill step 10, Fail line; Playbook Pitfall 10, Decision 7; Research Summary 11, Q7, R4 header | **Done** in all seven places, with the `/usr/bin/time -v` / Task Manager instruction, the frame-by-frame `render-frame` fallback and the ffprobe/moov check kept. The Fail line now reads "a 30-frame sample at one thread whose peak memory is over half of free RAM" |
| 3 | FilmCraft v0.9.0 row and hashes; lean "test v0.9.0 first, v0.8.0 fallback, v0.7.2 retired"; NAS/UNC sentence; `filmcraft-<tag>` folder names | Playbook Template A, Decision 6, Exercise 1, Steps 1 and 4, Template H; Skill step 2; Research Q1 table | **Done.** Both v0.9.0 hashes match today's `SHA256SUMS.txt` (Part 1, check 1). Template H has the local-drive-only line citing [65]. Folder names are `filmcraft-<tag>` with v0.9.0 as the example. Not done: R8's spike package table still installs the v0.8.0 tar.gz (Part 4 item 2) |
| 4 | Real menu items: File > Export > Final Cut Pro XML… / OpenTimelineIO…; `markers.exportCsv` | Playbook Steps 7 and 10, Exercise 6; Skill step 6 E3 | **Done, and improved by G3:** Step 10 names Markers > Export Markers as CSV… with the "needs an open sequence" condition, and Exercise 8 gained the real image-sequence routes (File > Import Image Sequence…, Media Browser, the Preferences toggle) plus the new Pitfall 23 about our `chNN_sNN.png` names. The skill's E3 still carries one TODO that the code answers (Part 4 item 3) |
| 5 | Resolve test with "Use sizing information"; Template F header; remove "manual not reachable" sentences | Playbook Exercise 6, Template F, Best references 7, Decision 3; Skill step 8; Research R7 | **Done.** No "not reachable" sentence remains in the playbook (grep). Template F's Resolve column is "Resolve free (manual says supported; your result)" with pp. 482, 484, 521-523 cited. Exercise 6 also added the "`.otio` alone in an empty folder" relative-path check from G2. The `.otioz` import and the two FCPXML checks of G1/G2 were not adopted (Part 4 item 4) |
| 6 | Sequence-first guard in Template B and Step 8; CLI guard with `prefs.set media.indeterminateTimebase` | Playbook Template B, Step 8; Skill step 7 | **Done, and better than asked:** the skill's step 7 uses G4's verified key, insists on the JSON **string** `"25"` (a bare number is refused), puts `prefs.set` and the import in one `run` script because headless CLI sessions do not load or save preferences, and names the `--bridge` route for the running app. Checklist "Before importing media" gained the same line |
| 7 | Main research body stops contradicting its follow-up (Summary 13, Q3 Kdenlive and Resolve cells, Open questions 3-4, Q1 table); Playbook Core principle 5 and Decision 3 wording | Research; Playbook | **Done.** Summary 13, the Q3 Kdenlive cell, both Resolve FCP7 cells, Open questions 3-4 and the Q1 table all carry the new wording; "not effects or transitions" no longer appears in the playbook (grep) |
| 8 | Default `weight` mapping (1: 3-4 s, 6-8 percent; 2: 5-6 s, 10-12 percent alternating; 3: full voice line, min 7 s, none or under 4 percent, hard cuts); trim to the voice line; "check they chose the right photo" | Skill steps 4 and 5; Playbook Step 9 | **Done** verbatim in meaning in all three places; the skill's step 4 also states the trim rule as an inequality an agent can apply (`duration_frames` <= line end minus shot start) |

Eight of eight addressed. Items 3, 4 and 5 leave small residues that I list in Part 4; none changes a decision.

---

## 1. What I verified today (method and results)

Method: the researcher's shallow clones in the scratchpad (`vendor/filmcraft` at `f03e2155` = v0.8.0, `vendor/effectcraft` at `2a012268` = v0.11.1, `vendor/soundcraft` at `2578ea69` = v0.8.0, confirmed with `git describe`), fresh `curl` downloads of two `SHA256SUMS.txt` files and of Kdenlive's `otioimport.cpp` at tag v26.08.2 from invent.kde.org, `git ls-remote --tags` against the three repos, `pdftotext` on the researcher's local copy of the Resolve 21 Reference Manual (187,277,990 bytes, SHA-256 prefix `7bfdcf0296bd1e48`, matching [86]), and three WebFetch reads of GitHub and kdenlive.org pages through a summarising model. Everything fetched was treated as data. Nothing was built or run.

| # | Claim (where) | Source checked | Result |
|---|---|---|---|
| 1 | FilmCraft v0.9.0 portable zip `d370cac8…101a5e` and Linux tar.gz `ea67953c…a61632`; EffectCraft v0.11.1 zip `78bd7f63…e6e34` and tar.gz `b9cb2ce6…68934` (research Q1, playbook Template A, skill step 2) | `releases/download/<tag>/SHA256SUMS.txt`, HTTP 200 today | **All four match byte for byte** |
| 2 | Newest tags: FilmCraft v0.9.0, EffectCraft v0.11.1, SoundCraft v0.8.0; no v0.10.0 / v0.12.0 (G6) | `git ls-remote --tags` sorted; `SHA256SUMS.txt` for filmcraft v0.10.0 and effectcraft v0.12.0 | Confirmed; both absent files return 404 |
| 3 | Kdenlive `resolveFile` passes the string through `QUrl::fromLocalFile`; dissolves become luma mixes; image sequences are a TODO (Pitfall 6, Core principle 5, Decision 3, Summary 13) | `src/otio/otioimport.cpp` at v26.08.2, raw from invent.kde.org | Confirmed: `const QUrl url = QUrl::fromLocalFile(file); QFileInfo out(url.isValid() ? url.toLocalFile() : file); if (out.isRelative()) out = QFileInfo(timelineFile.path(), out.filePath());` (the function sits at lines 390-399); `requestClipMix(QString("luma"), …)` at line 295; `// TODO: Image sequence references.` at line 325. Relative paths resolve against the timeline file's folder, exactly as the playbook says |
| 4 | Kdenlive 26.08.2 released 2026-10-13 [49] | kdenlive.org/news (WebFetch; `/en/news/` is 404, `/news/` works) | Confirmed: "Kdenlive 26.08.2, Tuesday, 13 October 2026"; the page does not mention OTIO, consistent with the note's "26.08.0 notes do not mention OTIO" |
| 5 | Resolve 21 manual: "Use sizing information: Lets you import position, scale, and rotation transforms"; "If these settings have been keyframed, the animation will appear"; the supported-effects table lists Opacity and Position/Scale/Rotation (F2, Exercise 6, Template F) | `pdftotext -f 478 -l 488` and `-f 515 -l 530` on the local PDF | Confirmed: both phrases present; the table rows "Opacity Settings  No  Yes  Yes" and "Position, Scale, Rotation  No  Yes  Yes  Yes, via 3D Warp" are in the page range the note cites as 482-484 |
| 6 | Resolve 21 manual on OTIO linking and `.otioz` (G2): "using the embedded file paths. If DaVinci Resolve can't locate the media … you'll be prompted"; "the media assets will unzip themselves into the same folder as that .otioz file, and automatically link themselves" | `pdftotext -f 540 -l 550` | Confirmed, both quotations verbatim |
| 7 | `markers.exportCsv`, label "Export Markers as CSV…", menu path `["Markers"]` (G3, playbook Step 10) | `crates/engine/src/commands.rs` @v0.8.0 lines 2444-2446 | Confirmed (G3 cites line 2446 at v0.9.0; the two-line offset is the v0.9.0 diff) |
| 8 | `file.importImageSequence`, "Import Image Sequence…", menu `["File"]`, parameter `path` = "the first numbered still" (G3, Exercise 8) | `crates/engine/src/project_tools.rs` @v0.8.0 lines 117-118 | Confirmed |
| 9 | Preference key `media.indeterminateTimebase`, `Kind::Choice(TIMEBASE)`, `TIMEBASE` starts `23.976, 24, 25`; struct field is a `String` with default `"29.97df"`; the CLI parses values as JSON first; `filmcraft-cli` builds `Session::default()` and never touches preferences (G4, skill step 7) | `settings.rs` lines 934-937 and 1209; `autosave.rs` lines 231 and 260; `apps/filmcraft-cli/src/args.rs` line 111-113 (`serde_json::from_str(s).unwrap_or_else(… Value::String …)`); `main.rs` lines 157 and 579, zero hits for `preferences` or `start_autosave` | Confirmed on every point; the "`value=25` is refused" conclusion is [C] and the note says so |
| 10 | `file.newSequence` default `fps` is 23.976 (F5, Exercise 2, Template B, skill step 7) | `commands.rs` @v0.8.0 line 1176: `"fps":f64=23.976`; line 2201 falls back to `FrameRate::FPS_23_976` | Confirmed |
| 11 | PR #1763 open, "No reviews", unset = no cap; issue #1615 figures (1.8 GB single frame, 2.1 GB at 1 thread, 4.2 GB at 4, killed at 9 GB at 16, 6.8 GB with 2 threads on the real project; frame-by-frame workaround; no maintainer comment) (Q7, Pitfall 10, skill step 10) | github.com pull/1763 and issues/1615 (WebFetch, summarised) | Confirmed on every number quoted in the note; the only commenter besides the PR author is the `ticket-craft` bot |

Eleven of eleven matched. One extra finding while checking item 7: `file.exportFcp7Xml` is implemented as `file.exportInterchange` with `format` forced to `"xml"` and calls the same `crate::interchange::export` (`commands.rs` @v0.8.0, the block at lines 1445-1470), so the skill's open TODO "whether the two files are identical" is answered: they are the same exporter (Part 4 item 3).

---

## 2. Scores (track as a whole; per-artefact notes below)

| Criterion | Score | Why |
|---|---|---|
| Meaning | **4** | The spec's `weight` now drives duration and motion with a rule an agent can apply without asking, the weight-3 photo is a named decision the maker checks first, and the story pass precedes every keyframe. The round-1 "still still" and round-2 "markers as the maker's voice" ideas remain the maker's to take up; neither is a defect |
| Specificity | **5** | Hashes, tags, line numbers, menu labels, dialog checkbox names, manual page numbers, JSON-lines scripts, the exact inequality for trimming to the voice line |
| Accuracy | **4** | Eleven of eleven checks matched, including four hashes, two live GitHub pages, the Kdenlive source and six verbatim quotations from the Resolve manual. Residue: one stale sentence in the research Risks table (absolute paths) and a spike table still pinned to v0.8.0; both are internal inconsistencies, not wrong facts about the world |
| Feasibility | **4** | Every step has a non-Craft fallback that is now path-correct for Kdenlive and checkbox-correct for Resolve; the EffectCraft memory procedure is safe as written; the spike S1 is written and sized for the measured container. Still unknown, and outside this track's power: the maker's hardware and installed versions (G5 block not yet sent) |
| Ethics | **5** | Shot-id renaming everywhere a name could leak; the public-ticket relay verified twice; portable zips, no NAS, no synced folders; test cards until the pipeline is locked; the proxy-reviewer rule in the skill's guardrails |
| Craft / usability | **4** | Playbook: plain register, ordered steps, every TODO either closed or named as a maker test. Skill: the description triggers on the right nouns and excludes the right neighbours; the procedure is a sequence an agent can execute with units, value types and the preference guard. Two small usability residues (Part 4 items 3 and 4) |

Per artefact: research note 4/5/4/4/5/4 (two internal inconsistencies left); playbook 4/5/4/4/5/4; skill 4/5/4/4/5/4.

---

## 3. Critical issues

None. The LEARN phase has no code and no family material, and nothing in the three artefacts would, if followed, lose data, leak the surprise or put real material into an unverified tool.

---

## 4. Carry-forward items (polish, not blockers; each with file, section and exact change)

1. **Research note, "Risks, pitfalls and ethics", Pitfall 5.** Replace "use stable absolute paths under one project root and one track-order convention" with "use relative `target_url`s resolved against the `.otio`'s folder (see 'What this means', bullet 4) and one track-order convention". This is the last sentence in the bundle that still recommends absolute paths.
2. **Research note, R8 spike S1, "Packages" table.** Replace the `filmcraft-0.8.0-linux-x86_64.tar.gz` row with `filmcraft-0.9.0-linux-x86_64.tar.gz` `ea67953cc754bfd8272e0e5fa940518e16068ae96f6b72a2dce566ed69a61632` (candidate), keeping the v0.8.0 row marked "fallback"; the spike must test the tag the playbook pins. Also update "Each tarball unpacks to `<name>-<ver>-…`" examples accordingly and add G6's "tag check on the day S1 starts" one-liner above the table.
3. **Skill, Procedure step 6 E3.** Replace "whether the two files are identical is TODO(research)" with: "`file.exportFcp7Xml` is `file.exportInterchange` with `format` forced to `xml`; both call `crate::interchange::export` (`commands.rs` @v0.8.0, lines 1445-1470), so the GUI and headless files are the same exporter's output." Research R2 step 5 can name the GUI items beside `file.exportInterchange` for the maker's benefit.
4. **Playbook, Exercise 6.** Add an optional step 6 from G1/G2 for the same Resolve sitting: "(a) Put the two test stills on a Resolve timeline, File > Export > Timeline… as FCPXML, open it in Notepad and write down whether the still is a `video`, `asset-clip` or `clip` element and the `src=` form; (b) export the same two stills from FilmCraft as File > Export > FCPXML… and import that into Resolve with 'Use sizing information' ticked; note online/offline and duration." Then Pitfall 8's last TODO has a test behind it. Whether to add the `.otioz` companion to the bundle (G2 decision 2) stays the orchestrator's call; the skill's current "not part of the bundle" is a defensible default because the documented folder prompt is a one-click fallback.
5. **Playbook, Sources.** Add [85] and [86] (used by G2 and G3 through [83]/[84]) so the Exercise 6 and Exercise 8 citations resolve inside the playbook's own list, and mark [64] (Kdenlive 25.04 OTIO rewrite) as "search summary only" where Decision 3 cites it, as the research does.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. The maker's hardware, installed Craft versions and build type (G5's read-only PowerShell block). Still unsent after three rounds; half of Q4, Decision 1 and the final pin wait on it.
2. Resolve 21 (free) on real files, in one sitting: FCP7 XML keyframes with 'Use sizing information'; whether a relative `target_url` links without the folder prompt; whether an `.otioz` with stills links by itself; what Resolve writes for a still in FCPXML and whether it reads FilmCraft's `asset-clip` stills (G1, G2). The playbook's Exercise 6 plus item 4 above is the test.
3. Kdenlive 26.08.2 on an agent-written OTIO with still-image clips: do stills arrive with the right duration and does the project profile really follow the first still's pixel size (F3 is code-only).
4. Tag state on the day spike S1 starts: whether EffectCraft v0.12.0 and SoundCraft v0.9.0 tags appeared (both `main` branches are version-bump commits), whether a FilmCraft v0.10.0 exists, and whether PR #1763 merged (then `EFFECTCRAFT_CPU_INFLIGHT=1` becomes the first mitigation, still measured).
5. Whether the portable zips' executables carry an Authenticode signature (`Get-AuthenticodeSignature`), as the release packaging implies (Open question 9).
6. The Windows keyboard shortcut for Resolve's File > Import Timeline (the manual gives the macOS one), a one-line nicety for Exercise 6.
7. Resolve's FCPXML import behaviour for FilmCraft `asset-clip` stills is folded into item 2; no separate search is warranted (two searches found no Resolve-written sample).

---

## 6. Strengths worth keeping

- The track now has a complete chain from evidence to action: a verified fact in the research (with a line number), a sentence in the playbook in the maker's register, and a command or checklist line in the skill. The round-2 scribe propagated all eight nudges without diluting any of them.
- The round-2 follow-up (G1-G6) found two traps nobody asked about: `value=25` is silently the wrong type for `prefs.set`, and our `chNN_sNN.png` names would be read as image sequences if one preference is on. Both are now in the skill and the playbook with the default-safe setting named.
- Evidence grades remain honest: "read as code, not run" appears wherever it applies, the Resolve manual is quoted rather than paraphrased, and UNVERIFIED still means UNVERIFIED after a second search.
- The hand-off is privacy-clean by construction: shot-id names, relative paths inside a self-contained bundle, portable apps, no NAS, test cards until the pipeline is locked.
- The skill's description is short, nounful and bounded; an agent asked to "write the OTIO for chapter 3" or "pin FilmCraft" will land on it, and one asked about interviews or game mechanics will not.

---

## 7. Advisor insight

During covert digitisation, scan the **backs** of the prints too, at the same sitting, as a rule of the conform step (one extra manifest column, `back`). Many family prints carry a date stamp, a lab name, or a line in a parent's or grandparent's handwriting ("Summer 1978, the lake"). Those backs are the only title cards in this film that nobody has to design and nobody can accuse of being a template: real hand, real ink, written at the time, by someone who loved her. For each chapter's weight-3 photograph, open on the back (held still, native pixels, paper grain visible, no Ken Burns), then dissolve through to the front. The pipeline already supports it with nothing new: a second still in the bundle, a 1.5 s dissolve, a weight-3 hold. And at the premiere, the moment she recognises her mother's handwriting before she recognises the photo is the moment the room understands what kind of film this is.

---

## Changelog
- 2026-10-18: round 3 (final) written by the Fable advisor after confirming all eight round-2 nudges were applied and verifying eleven claims (four release hashes, newest tags, Kdenlive `otioimport.cpp` at v26.08.2, kdenlive.org release date, six Resolve 21 manual quotations via pdftotext, `commands.rs`/`project_tools.rs`/`settings.rs`/`autosave.rs`/`args.rs`/CLI `main.rs` lines, PR #1763 and issue #1615). Verdict: approve. Five carry-forward polish items and seven research follow-ups listed for the orchestrator.
