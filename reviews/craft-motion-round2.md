# Review: track `craft-motion`, round 2 of 3

**Reviewer:** Fable advisor
**Date:** Sunday 2026-10-18 (week 1 of 19; deadline Saturday 2027-02-27)
**Reviewed:**
- `research/craft-motion.md` (main note plus the new "Follow-up research (round 1)" section, F1-F7)
- `playbooks/craft-motion.md` (v1.1, "round 1 review nudges applied")
- `.claude/skills/craft-apps-motion-refinement/SKILL.md`
- against `CHARTER.md`, my brief review `reviews/01-addendum-briefs-review.md` (Part 2.2) and my round-1 review `reviews/craft-motion-round1.md`

**Verdict: REVISE.** All eight round-1 nudges were addressed, three of them better than I asked (the scribe corrected my own wrong assumption about a sequence preset). Nothing critical is open. The reason for another round is new and specific: the researcher's follow-up section (F1-F7) answered my six research questions and found four facts that change the playbook and the skill, and then wrote "Edits these answers imply (for the scribes; not applied here)". Those edits were not applied. Today the two artefacts people act on tell the agent to write OTIO paths that the follow-up proves Kdenlive cannot open, tell it to rely on a memory mitigation the follow-up proves is not a bound, pin a FilmCraft tag the follow-up supersedes, and send the maker into Resolve without the one checkbox the manual says makes keyframes appear. Each fix is a paragraph.

---

## 0. Round-1 nudges: were they addressed?

| # | Nudge (round 1) | Where | Result |
|---|---|---|---|
| 1 | "Story pass first" paragraph before Step 9's technical bullets | Playbook Step 9 | **Done.** Four questions (carrying photo gets more time; cut, do not dissolve, at hard moments; moves end before the sentence; partly cropped faces checked against the manifest). Wording is the maker's register |
| 2 | Quality bar Good/Mediocre lines; `weight: 1|2|3` in the neutral spec | Skill Quality bar, Procedure step 5 | **Done.** Good and Mediocre lines present verbatim in meaning; `weight` added with a one-line definition. What is still missing is how weight maps to duration and move (nudge 8 below) |
| 3 | "playbook R5" → research R5; step 1 names R1-R8, T1-T6, Open questions | Skill "When not to use", step 1 | **Done** exactly |
| 4 | Units per command; lower-case interpolation names; ticks helper | Skill step 7 | **Done.** I re-read `commands.rs` @v0.8.0: `timeline.place` `duration` is read as a raw i64 tick (`p.get("duration").and_then(Value::as_i64).map(Tick)`), `effects.setInterpolation` takes `"mediaTime":ticks` and `"interpolation":"linear|bezier|autoBezier|continuousBezier|hold|easeIn|easeOut"`. The skill's text matches |
| 5 | Soften the FCPXML `<video>` claim; add the `<clip>` nuance | Playbook Pitfall 8; research Summary 5 and Q3 cell | **Done, and strengthened**: the follow-up F1 found a real Final Cut 1.13 sample with a bare `<video>` still, so the pitfall now says "Final Cut writes stills this way in one sample; Resolve unverified". I re-read `fcpxml.rs` @v0.8.0 lines 383-406: the `"clip"` arm reads the first inner `video|audio|asset-clip` with a `ref`; the bare `"title" | "video" | "audio" | "sync-clip" | "mc-clip" | "live-drawing"` arm warns and skips. Correct |
| 6 | Exercise 2 step 2 in GUI register | Playbook Exercise 2 | **Done, and corrected me.** There is no preset list: `sequence_settings.rs` @v0.8.0 has `TIMEBASES: [(i64,i64); 15]` and shows "Editing Mode: Custom" greyed with a not-yet note. The exercise now says "set Timebase to 25, keep 1920x1080, read it back". Right |
| 7 | Shot-id renaming rule at conform and in logs; manifest keeps the mapping | Skill steps 3 and 11; Playbook Templates C and H | **Done** in all four places, with the #2216 evidence cited |
| 8 | Who produces `chNN.xml` if S1 fails; checklist bullet | Playbook Step 7; Skill step 6 E3 and "Before a hand-off" | **Done.** Both say the maker exports FCP7 XML after Step 8. The scribe honestly flagged my menu path "File > Export > Interchange" as TODO(research); I have now read the real menu entries (section 1, check 9) and it becomes nudge 4 |

---

## 1. What I verified today (method and results)

Method: the researcher's shallow clones are still in the scratchpad (`filmcraft` `f03e2155` = v0.8.0, `effectcraft` `2a012268` = v0.11.1, `soundcraft` `2578ea69` = v0.8.0; confirmed with `git describe` and `git log -1`). I re-downloaded three `SHA256SUMS.txt` files with curl, fetched Kdenlive's `src/otio/otioimport.cpp` at tag v26.08.2 from invent.kde.org, read two GitHub pages and the Qt documentation with WebFetch (summarised by a small model), and sent a HEAD request for the Resolve 21 manual. Everything fetched was treated as data. Nothing was built or run.

| # | Claim (where) | Source checked | Result |
|---|---|---|---|
| 1 | Nine SHA-256 values: FilmCraft v0.8.0 and v0.9.0 (portable zip, MSI, Linux tar.gz) and EffectCraft v0.11.1 (research Q1 and F7, playbook Template A, skill step 2) | `github.com/storytold/<repo>/releases/download/<tag>/SHA256SUMS.txt`, HTTP 200 today | **All nine match byte for byte**, including the three new v0.9.0 hashes in F7 (`d370cac8…` portable, `5db43e23…` MSI, `ea67953c…` tar.gz) |
| 2 | FilmCraft newest tag is v0.9.0; EffectCraft newest is v0.11.1, no v0.12.0 tag (F4, F7) | `git ls-remote --tags` today | Confirmed: filmcraft `… v0.8.0 v0.9.0`; effectcraft `… v0.10.0 v0.11.1` |
| 3 | `SCHEMA_VERSION` 15; 254,016,000,000 ticks/s (unchanged from round 1) | `crates/format/src/lib.rs` (`assert_eq!(SCHEMA_VERSION, 15)`), `crates/time/src/lib.rs` (`TICKS_PER_SECOND: i64 = 254_016_000_000`) | Confirmed |
| 4 | `timeline.place` `duration` is ticks; `effects.setInterpolation` `mediaTime` ticks, lower-case names (skill step 7) | `crates/engine/src/commands.rs` @v0.8.0 (place: `p.get("duration").and_then(Value::as_i64).map(Tick)`; setInterpolation parameter doc at line 3201) | Confirmed |
| 5 | New Sequence dialog has no preset list; 15 timebases; Editing Mode "Custom" greyed (F5, playbook Exercise 2) | `crates/ui-egui/src/panels/sequence_settings.rs` @v0.8.0 lines 42, 305-308 | Confirmed |
| 6 | Issue #2216 was created by the `ticket-craft` GitHub App from a Discord report (skill step 3, playbook Pitfall 19) | github.com/storytold/filmcraft/issues/2216 (WebFetch) | Confirmed: author `ticket-craft` (bot); body: "Submitted through Discord by … and created by the Ticket Relay integration on their behalf"; open; Windows 11 |
| 7 | PR #1763 (`EFFECTCRAFT_CPU_INFLIGHT`) is open, unreviewed, not in any tag (F4) | github.com/storytold/effectcraft/pull/1763 (WebFetch) | Confirmed: open, "No reviews", only the author's description; adds `EFFECTCRAFT_CPU_INFLIGHT=N`, unset means no cap |
| 8 | Kdenlive's OTIO importer does not decode a `file://` `target_url`; dissolves import as luma mixes; image sequences skipped (F3) | `src/otio/otioimport.cpp` at v26.08.2 (fetched raw): `resolveFile` does `QUrl::fromLocalFile(file)` then `toLocalFile()` (lines 394-395); `requestClipMix(QString("luma"), …)` (line 295); `// TODO: Image sequence references.` (line 325). Qt 6 `QUrl` docs: example `QUrl::fromLocalFile("file:file.txt"); // doesn't make sense; expects path, not url with scheme` | **Confirmed in code.** The behavioural conclusion (a `file:///C:/…` URL is treated as a path and the media is not found) follows from the Qt note; it is [C], not run, and the follow-up says so |
| 9 | GUI path for exporting FCP7 XML (playbook Step 7 TODO) | `crates/engine/src/commands.rs` @v0.8.0 lines 1445-1470: `file.exportInterchange` has no menu path; the menu items are `file.exportEdl` "EDL…", `file.exportFcp7Xml` "Final Cut Pro XML…", `file.exportFcpxml` "FCPXML…", `file.exportOtio` "OpenTimelineIO…", all under `["File", "Export"]`; `markers.exportCsv` "Export Markers as CSV…" exists (line 2444) | **My round-1 menu path was wrong.** The item the maker clicks is **File > Export > Final Cut Pro XML…**. See nudge 4 |
| 10 | Resolve 21 Reference Manual PDF exists at the cited URL with the cited size (F2) | HEAD request to `documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21_Reference_Manual.pdf` | HTTP 200, `content-length: 187277990` (matches F2's 187,277,990 bytes). I did not download the 187 MB file; the page quotes ("Use sizing information", "If these settings have been keyframed, the animation will appear") are the researcher's and are the first primary-source answer we have for Resolve |

Ten of ten spot checks matched. The accuracy problem in this round is not wrong claims; it is that verified new facts stayed in the follow-up section and never reached the main note, the playbook or the skill.

---

## 2. Scores (track as a whole; per-artefact notes below)

| Criterion | Score | Why |
|---|---|---|
| Meaning | **4** | The story pass now exists in the one place the maker's hands touch the film, and the spec has a `weight` field. The agent still has no rule for turning weight into duration and move, so the first bundle will again be uniform unless someone remembers (nudge 8). The round-1 "still still" insight was not taken up; that is the maker's call, not a defect |
| Specificity | **5** | Hashes, line numbers, parameter documents, menu labels, test names; the follow-up section adds Kdenlive line numbers and Resolve manual page numbers |
| Accuracy | **4** | Every claim checked is right. But the bundle now contradicts itself: Summary 13 and the Q3 Kdenlive cell say "no effects or transitions" while F3 says dissolves import as luma mixes; Q3 and Open question 3 say Resolve keyframes are UNVERIFIED while F2 quotes the manual; Q1's pin table stops at v0.8.0 while F7 adds v0.9.0; R3's E2 template and the skill write `file:///C:/…` URLs that F3 shows Kdenlive cannot open. A reader of the main note alone is misled four times |
| Feasibility | **4** | Every step still has a non-Craft fallback and the spike is unchanged. Two feasibility holes: the Kdenlive fallback does not work as written (paths), and the EffectCraft memory guidance is unsafe as written (`RAYON_NUM_THREADS=2` reached 6.8 GB in the reporter's project) |
| Ethics | **5** | Shot-id renaming closes the last leak path; the Discord relay is verified twice now; the test-card rule is in both artefacts; v0.9.0's local-path restriction is good news for the private-folder rule |
| Craft / usability | **4** | Playbook: plain, well-ordered, two TODOs now answerable from code. Skill: description triggers well; procedure is executable; but it still carries the stale mitigation and the absolute-URL instruction, and its "Before a hand-off" checklist cannot catch either |

Per artefact: research note 4/5/4/4/5/4 (main body stale against its own follow-up); playbook 4/5/4/4/5/4; skill 4/5/4/4/5/4.

---

## 3. Critical issues

None. The LEARN phase has no code and no family material; every item below is a wording change that must land before the week-1 spike and the maker's first hand-off.

---

## 4. Nudges (eight, each with file, section and exact change)

1. **Skill, Procedure step 6 (E2) and step 8; Playbook, Step 7 and Pitfall 6; Research, R3 E2 template and "What this means".** Replace the absolute `file:///C:/LifeJourney/...` `target_url` instruction with: *"Agent-written OTIO uses **relative** `target_url` values (`media/ch01_s01.png`), resolved against the `.otio` file's own folder. FilmCraft resolves relative paths against the document folder (`common.rs` @v0.8.0); Kdenlive 26.08.2's `resolveFile` passes the string through `QUrl::fromLocalFile`, which does not decode a `file://` scheme, so an absolute URL makes every clip 'missing' and the import aborts (`otioimport.cpp` lines 390-399; KDE bug 503692). The bundle folder is therefore delivered whole and the maker never moves `chNN.otio` away from `media/`. FCP7 XML keeps absolute `file://localhost/C:/...` `pathurl`s (Resolve relinks by prompt)."* In the R3 E2 JSON change both `target_url` values to `media/IMG_0001.png` style (and, per round-1 nudge 7, to `media/ch01_s01.png`). Add to the skill's "Before a hand-off" checklist: "OTIO `target_url`s are relative; no `file://` in the OTIO."

2. **Skill, step 10 (EffectCraft renders) and "Fail" line; Playbook, Pitfall 10 and Decision 7; Research, Summary 11, Q7 mitigation and R4 header.** Replace "`RAYON_NUM_THREADS=2`" as the mitigation with F4's procedure: *"Start every new comp at `RAYON_NUM_THREADS=1`; render a 30-frame sample under `/usr/bin/time -v` (Task Manager on Windows) and record peak RSS; raise threads only while peak stays under half of free RAM. Where that is too slow, render frame by frame (`render-frame` per frame to PNG) and encode with ffmpeg, which is what the #1615 reporter did. `RAYON_NUM_THREADS=2` is not a bound: the reporter measured 6.8 GB with it. `EFFECTCRAFT_CPU_INFLIGHT` exists only in open PR #1763 (no reviews on 2026-10-18) and does nothing in v0.11.1."* Keep the ffprobe/moov check.

3. **Playbook, Template A, Decision 6, Exercise 1 step 1 and Step 4 folder name; Skill, step 2; Research, Q1 pin table.** Add the FilmCraft v0.9.0 row from F7 (portable zip `d370cac8ed2edd729c8129aa55f75d0123716ba3cddbf9c5e4e3f0fdaa101a5e`, Linux tar.gz `ea67953cc754bfd8272e0e5fa940518e16068ae96f6b72a2dce566ed69a61632`; I re-downloaded `SHA256SUMS.txt` today and they match) and change the lean to *"test v0.9.0 first (interchange code unchanged; fixes a UTF-8 `file:` prefix panic that Unicode paths can hit), v0.8.0 as fallback, v0.7.2 retired"*. Add one sentence from F7 to Core principle 7 or Template H: *"From v0.9.0 FilmCraft opens stored media paths only on local drives or the document's own share; do not put the project on a NAS or UNC path."* Replace the hard-coded `filmcraft-v0.8.0` folder names in Steps 1, 4 and Exercise 1 with `filmcraft-<tag>`.

4. **Playbook, Step 7 (TODO), Step 10 (TODO) and Exercise 6 step 1; Skill, step 6 E3.** Replace "File > Export > Interchange (TODO)" with the real menu items from `commands.rs` @v0.8.0 (lines 1445-1470): *"File > Export > **Final Cut Pro XML…** writes the FCP7 XML (`file.exportFcp7Xml`); File > Export > **OpenTimelineIO…** writes the OTIO (`file.exportOtio`); FCPXML… and EDL… sit beside them. Save as `chNN.xml` and `chNN.otio` into the bundle folder."* For the marker list: *"the command `markers.exportCsv`, labelled 'Export Markers as CSV…' (expected under the Markers menu; confirm on first use)."* This closes two TODOs and corrects my round-1 wording.

5. **Playbook, Exercise 6 and Template F; Skill, step 8 hand-off note; Research, R7 Resolve line.** Replace the Resolve steps with F2's revised test: *"File > Import Timeline (or Media Pool right-click > Timelines > Import), choose `ch01.xml`; in the dialog tick **'Use sizing information'** and leave 'Mixed frame rate format' on 'DaVinci Resolve'. Check: stills online; each still 5 s, not one frame and not 29.97-based; Inspector > Edit Sizing shows Zoom/Position keyframes at the right frames; Opacity keyframes in Composite; dissolves present. Then import `ch01.otio` and note what is lost (motion is expected to be lost). Record Help > About version."* In Template F, change the Resolve column header to "Resolve free (manual says supported; your result)" and cite the Resolve 21 Reference Manual pp. 482, 484, 521-523 [74] under the table; the playbook's "Resolve's own manual was not reachable" sentences (Exercise 6, Best references 7, Decision 3) are now false and should point to [74].

6. **Playbook, Template B (five-minute test) and Step 8; Skill, step 7 command list.** Add F5's three lines to Template B: *"Create the sequence first: File > New > Sequence; write down what the dialog shows (expected 23.976, 1920x1080, 48000 Hz); set Timebase 25, name it `ch01`, OK."*; *"Never drop the first clip on an empty timeline: that makes a sequence at the still's pixel size and 29.97 fps."*; *"Set the Indeterminate Media Timebase preference to 25 before importing stills (Settings > Media), then confirm Sequence Settings still says 25."* In the skill's step 7 add the same guard for the CLI path with the preference key the research names (`prefs.set media.indeterminateTimebase`), marked "confirm the key with `filmcraft-cli describe prefs.set`".

7. **Research note, main body.** Apply the researcher's own "Edits these answers imply" list 1 and 7 so the note no longer contradicts itself: Summary 13 and the Q3 Kdenlive cell say *"cuts, gaps, markers and dissolves (as luma mixes, by code) survive; effects, metadata and image sequences do not; `file://` URLs are not decoded; the project profile is taken from the first still's pixel size"*; the Q3 Resolve FCP7 cells and Open questions 3-4 cite the manual [74] as "supported at format level, FilmCraft's numbers untested"; the Q1 table gains the v0.9.0 row. Also fix Playbook Core principle 5 and Decision 3 ("not effects or transitions") to the same wording, since both now lean on a Kdenlive doc that the code contradicts.

8. **Skill, Procedure step 5 (neutral spec) and step 4 (Compute motion); Playbook, Step 9 story pass.** Give `weight` teeth with a default mapping the agent applies unless the spec overrides it: *"weight 1: 3-4 s, push 6-8 percent; weight 2: 5-6 s, push 10-12 percent, alternate push-in and drift; weight 3 (the photo that carries the chapter, at most one per chapter): hold for the full length of the voice line about it (minimum 7 s), motion `none` or a push under 4 percent, hard cuts both sides. Every duration is then trimmed so the move ends on or before the end of the voice line under it (`duration_frames` <= the line's end minus the shot's start)."* Add to the playbook story pass: *"The agents mark the weight-3 shot in the spec; your first job is to check they chose the right photo."* Without this, step 5's field is data nobody uses.

---

## 5. Research follow-ups (facts not in the notes; do not guess)

1. What DaVinci Resolve 21 writes for a still in FCPXML (`<video>`, `<asset-clip>` or `<clip>`-wrapped) and whether it reads FilmCraft's `asset-clip` stills; F1's maker check (two stills, File > Export > Timeline > FCPXML, open in Notepad) is the cheapest answer and the only one available without a Mac.
2. Whether Resolve 21 resolves a **relative** `target_url` in an imported OTIO, or needs a `file://` URL plus a relink prompt. If it needs URLs, the bundle may need two OTIOs (relative for FilmCraft and Kdenlive, URL for Resolve), or FilmCraft's own exported OTIO is used for Resolve.
3. The exact FilmCraft GUI locations of "Export Markers as CSV…" (`markers.exportCsv`) and of the image-sequence option in the Import dialog (`file.import {imageSequence:true}` in the engine; the dialog is in `crates/ui-egui`), to close the last two TODOs in Exercise 8 and Step 10.
4. The exact preference key and value format for the Indeterminate Media Timebase through `prefs.set` (`crates/engine/src/settings.rs` and `autosave.rs` @v0.8.0 name `indeterminate_timebase: "29.97df"`), so the skill's CLI guard in nudge 6 is a verified command.
5. Still outstanding since review 01: the maker's hardware inventory and installed Craft versions (F6 gives the read-only PowerShell block). Half of Q4, Decision 1 and the pin choice wait on it; the orchestrator should send F6's block to the maker now.
6. Whether a FilmCraft v0.10.0 or EffectCraft v0.12.0 tag has appeared by the time the spike runs (weekly `git ls-remote --tags | sort -V | tail -3`), and whether PR #1763 merged; the pin tables are dated 2026-10-18.

---

## 6. Strengths worth keeping

- Every round-1 nudge was applied, and where my nudge was wrong (the sequence preset; the "Interchange" menu path) the scribe flagged it instead of copying it. That is exactly the behaviour the charter's rubric asks for.
- The follow-up research is the best piece of work in this track: it read Kdenlive's importer and the Resolve 21 manual as primary sources, found the `file://` trap and the "Use sizing information" checkbox that would each have cost the maker an evening, and dated everything. Ten of ten spot checks matched today, including nine release hashes and two live GitHub pages.
- The evidence grades ([T]/[C]/[V]/[I]/[E], UNVERIFIED) are still applied consistently, and the follow-up is explicit about what it did not find (no Resolve-written still, no 1.9-1.11 sample).
- The playbook's story pass reads like advice from an editor, not a manual, and the shot-id renaming rule now appears in every place a file name could leak.
- The skill's description still triggers on the right nouns (Ken Burns scale, OTIO/FCP7/FCPXML/EDL, pinning, hand-off folder, EffectCraft title or line-draw) and excludes the right neighbours; its step 7 is now a complete, unit-safe command sequence an agent can run.

---

## 7. Advisor insight

The interchange matrix has one row where every column says **P**: markers. OTIO, FCP7 XML, FCPXML, EDL, `.fcproj`, Kdenlive (as guides) and Resolve all keep a marker with its colour and comment, and FilmCraft exports them as CSV. That makes markers the one channel through which the maker's voice can travel back to the agents without ever touching a keyframe or a file that could break. So give the maker's story pass a second mode, cheaper than editing: watch the chapter once and *only drop markers*, with a colour code the agents read as instructions. Red: "cut here, not a dissolve". Yellow: "hold this longer, she would want to look". Green: "she would laugh here" (the agents leave a breath). Blue: "wrong photo for this sentence" with the comment naming the right one. The agent diffs the marker CSV against the spec and re-emits the chapter; the maker then does the hands-on Ken Burns pass only on the second bundle, when the structure is already hers. For a surprise film about a mother, the comments themselves become a document: a list of the moments her child knew she would feel something, written in the week before she saw it. Keep that CSV. It belongs in the keepsake, after the gift.

---

## Changelog
- 2026-10-18: round 2 written by the Fable advisor after confirming all eight round-1 nudges were applied and verifying ten claims (nine release hashes, `commands.rs` units and menu items, `fcpxml.rs`, `sequence_settings.rs`, Kdenlive `otioimport.cpp` at v26.08.2, Qt docs, issue #2216, PR #1763, Resolve 21 manual URL). Verdict: revise, because the follow-up research's four verified changes (relative OTIO paths, EffectCraft memory bound, FilmCraft v0.9.0, Resolve "Use sizing information") have not been propagated into the main note, the playbook or the skill. No critical issues.
