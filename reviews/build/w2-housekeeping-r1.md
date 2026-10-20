# Fable review: the orchestrator's housekeeping of Tue 20 Oct 2026 (round 1)

*Fable advisor, Tue 20 Oct 2026, branch `build/process-lock`. Under D-32 every step is reviewed, this one included. Read: `git show 51f4789 --stat`, `git show 0b18d3e`, `git show 091835d`, `git show bd8377a`, `git log --oneline -12`; `build/apply_phone_row.py`, `build/apply_skill_rewords.py`; `DECISIONS.md` W-16, W-18, W-63 and the change log; `ops/decisions.csv`, `pipeline/phone/PHONE-ROW.md`, `pipeline/phone/profile.json`, `ops/SETTINGS-CARD.md`; `build/BUILD-STATUS.md`; `reviews/build/gate-r1.md`, `gate-r2.md`, `reviews/06-her-world-verify-r1.md`; `QUESTIONS-SUN-25-OCT.md`, `playbooks/production-scale.md`; `spikes/VERDICTS-W2.md`; `.gitignore`. Nothing here was edited or committed; the worktrees I made to test earlier commits were removed again. The later WIP commit `2fdbdb4` (week-2 sweep and spikes) is outside this review except where it changes what the maker sees today; it is noted, not scored.*

## Verdict: APPROVE

| Rubric axis | Score |
|---|---|
| Correctness | 4 |
| Safety and privacy | 5 |
| Maker usability | 4 |
| Fidelity to the plan and `DECISIONS.md` | 4 |
| Maintainability | 4 |

**In one line.** All six housekeeping claims check out against the tree and the disk: the 23 installed skills are byte-identical to their approved staged copies, the seven rewords are exactly the prepared edits, the register, its CSV mirror, `PHONE-ROW.md`, `profile.json` and the settings card agree on 3.5 Mb/s and 32 characters, the dated amendment note is in the register's change log, the bytecode and pid files are out of the index, about 14 GB was freed outside the repository with the named environments kept, and nothing identifying entered the repository. What remains is the follow-through the gate already listed (the scribe pass over the playbooks and skills that still quote 4 Mb/s and 36) plus one wording drift in the Sunday questions sheet that should be fixed before Sun 25 Oct.

## 1. What I checked and what I found

### 1.1 The skills install (`51f4789`)

* For each of the 23 directories under `skills-staging/` at `51f4789^` I compared every file with the same path under `.claude/skills/` at `51f4789`: **27 of 27 files identical** (23 `SKILL.md`, `free-creative-toolchain/references.md`, its two `recipes/r4_*.py`, `life-story-interviewing/beat-sheet.md`). The seven her-world skills are pure renames (0 lines changed); the sixteen reconciled skills replaced the earlier installed text with the staged text that `reviews/06-her-world-verify-r1.md` approved.
* The staged copies were removed in the same commit; `.claude/` was not edited by hand (the diff is the install only).

### 1.2 The phone row (`091835d`, `bd8377a`)

* `DECISIONS.md` W-63 now reads "1280x720, CRF 22, 3.5 Mb/s cap, level 3.1"; W-18 reads "at most 32 characters (measured to fit the 90% by 90% box in both scripts at FontSize=28; the venue file keeps its own guide of 42)". These are the two phrase replacements `apply_phone_row.py` documents, and nothing else in either row moved.
* **The dated amendment note is present**: the change log's last line, added in `bd8377a`, is dated 2026-10-20, names the gate item, both old and new values, the reason (WP-08's measured values; 3.5 inside the old cap; 32 fits the box in both scripts) and the three files that now match. The rows themselves carry no in-row marker; W-16 uses "**Added 2026-10-19:**" for its own amendment, so a reader of the W-63 or W-18 row alone cannot see that the figure changed (nudge 4).
* I re-ran the four parity checks from `tests/integration/run_checks.py` into my scratch folder: `parity.phone_profile_vs_register` (8 figures equal, PH2 3.5 Mb/s, 32 characters), `parity.card_phone_row_vs_phone_row_md` (19 facts equal), `parity.card_language_note_vs_scripts_tested`, `parity.decisions_csv_vs_register` (250 rows: D 32, W 79, O 74, S 65): **4 PASS**. `scripts/ops_lint.py`: PASS, 0 warnings.
* The card's Phone row is the PHONE-ROW.md section 1 row, word for word, and it is still marked "Proposed (J)" with "UNVERIFIED until you try it", which is right: the maker has not yet run `PHONE-TEST.md`.
* Note on the CSV mirror: `ops/decisions.csv` carries the W-18 and W-63 text truncated with "... see DECISIONS.md", so the mirror does not literally contain 3.5 or 32; the parity check compares the prefix and the register remains the source, which is the design. Fine, but anyone grepping the CSV for the figure will not find it.

### 1.3 The skill rewords and the baseline (`091835d`)

* I checked out `091835d^` in a scratch worktree, ran `apply_skill_rewords.py --apply` there, and compared the seven resulting `SKILL.md` files with `091835d`: **7 of 7 identical**. No hand edit rode along.
* The eight old phrases are gone from `.claude/skills` (the two remaining "atsc_1080p_25" strings are inside `recipes/r5_story.mlt`, the real profile name of a tested recipe, not a reconciliation note; `life-story-interviewing` line 181 says the "closest insider" role is removed, which is the point).
* `scripts/stale_check.py --new-only` at `bd8377a`: 0 new FAIL, 0 new WARN, 0 baseline hits missing. The baseline committed in `091835d` fell from 350 FAIL / 18 WARN to 176 / 12 (the sweep has since cut it further in the working tree, out of scope here).

### 1.4 Bytecode and the index

* `091835d` removed four `.pyc` files and `srv.pid` from the index; `git ls-files -i -c --exclude-standard` at HEAD is empty (nothing tracked is ignored). The 38 `.gitignore` lines added in the same commit ignore nothing that is tracked.

### 1.5 The scratch deletion

* `df -h`: 15 GB free on the 252 GB volume (gate round 2 saw 747 MB). `build/evidence/w2-sp3/run2_df_samples.txt` shows 14.5 GB available at 02:05 UTC on Tue 20 Oct, so the space was freed before SP3's second run.
* What was kept, as claimed: a `bpyenv` with `bpy` 5.2.2, `whisperenv_dir` (Whisper) and a `faster_whisper` environment, the FilmCraft source tree under a scratch `vendor/filmcraft`, plus the repo's own `vendor/` (fonts, js, craft) and `/home/user/build-scratch` (202 MB: `pwsh`, `venv-otio`, lock files and ledgers, untouched, as `VERDICTS-W2.md` step 1 asked). About 11 GB of Learn-phase scratch still sits outside the repository. Nothing under the repository was deleted. The deletion is recorded nowhere in the repo yet (nudge 5).

### 1.6 D-32 and the two her-world fixes (`0b18d3e`, `51f4789`)

* D-32 is in Table 1 with its date, source ("Fable reviews every step") and a change-log line; the CSV mirror has it (the parity check counts 32 D rows).
* `playbooks/production-scale.md` line 671 now says the 2:15 row is retired (S-17) and names W-04: exactly what verify-r1 nudge 3 asked.
* `QUESTIONS-SUN-25-OCT.md` Q4 (line 37) and Q16 (line 72), and line 7's parenthesis, now state the seva-article rule as "her Thakorji, chitraji or any picture of hers is never photographed without her knowing". The register's PR4 sentence (Codes, W-61, W-70, byte-identical in three documents) is "her Thakorji, chitraji, any picture of hers **and anything inside the mandir** are never photographed without her knowing", and verify-r1 nudge 1 asked for "anything inside the mandir" in both lines. The sheet is therefore narrower than the register in three places. It is a why-line on a sheet the maker answers from memory, not a rule the pipeline reads, so it is a nudge, not a critical issue; but it is the one maker-facing text of this housekeeping, and it goes to the maker on Sun 25 Oct (nudge 1).

### 1.7 Identifying data

* I grepped every added line of the four commits (evidence files included) for e-mail shapes, IPv4, profile paths, host names, serial-like runs and the maker's own identifiers: nothing identifying. The `/home/user/build-scratch` and `/home/user/...` strings in evidence and test harness text are the container's generic login, allowlisted by `scripts/redaction_patterns.json` and printed as `<scratch>` where the scripts control the output; `127.0.0.1` is the loopback of a test server. `public_lint.py` in diff mode: 0 findings. The only `--all` finding at HEAD is in `skills-staging/craft-apps-motion-refinement/SKILL.md:180`, re-staged by the later sweep commit, and it is the public KDE bug mailing-list address already allowlisted by value for `.claude/skills/**` (nudge 6, for the sweep review, not this one).
* The commit messages name no person, machine or place beyond what D-31 puts in the register.

### 1.8 What the gate asked for that is not done yet

Gate round 2, nudge 1, after the apply: "the scribe pass over the five playbooks and three skills that quote 4 Mb/s and 36 characters", then `run_all_checks.sh --quick` exit 0, then "remove both `build/apply_*.py` scripts". At `bd8377a` the old figures still stand in `playbooks/theatrical-delivery.md` (lines 256, 293), `playbooks/agent-pipeline.md` (182), `playbooks/mobile-delivery.md` (42, 201, 282), `playbooks/toolchain.md` (175), `playbooks/cinematic-quality.md` (337) and `.claude/skills/mobile-phone-delivery/SKILL.md` (33, 72); `pipeline/phone/profile.json`'s `phone_720_share.notes` still says "W-63 says a 4 Mbps cap". Both apply scripts are still tracked. `build/evidence/run_all_checks_quick.txt` as committed in `091835d` is the pre-apply run (integration FAIL on the two parity tests, 747 MB free), and `BUILD-STATUS.md` section 4 still lists issues 2 and 3 as open and the title says "after gate review round 1". None of this contradicts the register (the register wins and the checks read it), but it is the drift the stale check exists to catch, and the pattern file does not know "4 Mb/s" or "36" yet.

## 2. Scores, briefly

* **Correctness 4.** Every claim verified; the two committed evidence files that describe the state before the fix (quick run, BUILD-STATUS issues 2 and 3) are now wrong about the tree.
* **Safety and privacy 5.** Clean scans, generic container paths only, deletion confined to regenerable scratch outside the repo with the named environments kept, no family material anywhere, secrecy intact.
* **Maker usability 4.** The card row is the measured row and says so; the Sunday sheet is the one maker-facing text and it drifted from PR4.
* **Fidelity 4.** Register amended as the gate recommended, with the dated note; rewords exact; the scribe pass and script removal from the same gate nudge are still owed; the questions-sheet wording departs from the verifier's text.
* **Maintainability 4.** One prepared, dry-run-first script per edit, re-runnable and refusing on any ambiguity, is the right shape; the leftovers (old figures in eight files, stale notes, two one-shot scripts still tracked) are the cost of stopping at the register.

## 3. Critical issues

None.

## 4. Nudges (at most six)

1. **`QUESTIONS-SUN-25-OCT.md` lines 7, 37 and 72, before Sun 25 Oct:** restore "and anything inside the mandir" so the three why-lines say PR4 as the register says it ("her Thakorji, chitraji, any picture of hers and anything inside the mandir are never photographed without her knowing; a seva article outside it only by sight, untouched"). Three words each; then `scripts/ops_lint.py` and `public_lint.py` on the file.
2. **Finish gate nudge 1's scribe pass:** replace "4 Mb/s cap" and "at most 36 characters" / "36 characters a line" with the register's figures in `playbooks/theatrical-delivery.md` (256, 293), `agent-pipeline.md` (182), `mobile-delivery.md` (42, 201, 282), `toolchain.md` (175), `cinematic-quality.md` (337) and `.claude/skills/mobile-phone-delivery/SKILL.md` (33, 72; write the patched copy to `skills-staging/` for the orchestrator to install), and reword `profile.json`'s `phone_720_share.notes` ("W-63 says 3.5 Mb/s; the measured chain matches it"). Add a `S-` style pattern for the two retired figures to `scripts/stale_patterns.json` so they cannot come back, and re-cut the baseline.
3. **Re-file the evidence that describes the fixed tree:** run `bash build/run_all_checks.sh --quick` and commit its console copy over the pre-apply `build/evidence/run_all_checks_quick.txt`; in `build/BUILD-STATUS.md` mark issues 2, 3 and 4 closed with the commit ids and retitle the page; then remove `build/apply_phone_row.py` and `build/apply_skill_rewords.py` as gate round 2 asked (their headers are already quoted in the change log and in this review, so nothing is lost), or keep them with a first line "applied 2026-10-20 in 091835d; do not re-run".
4. **`DECISIONS.md` W-63 and W-18:** add an in-row marker in the register's own style ("**Amended 2026-10-20:** PH2 cap 3.5 Mb/s, was 4" and "**Amended 2026-10-20:** 32 characters, was 36") so the row shows the change without a trip to the change log; the change-log line is already right and stays.
5. **Record the disk work where the Fri 23 Oct reading will be judged:** in `spikes/VERDICTS-W2.md` disk-decision step 1 write "Done Tue 20 Oct: about 14 GB of Learn-phase scratch removed outside the repository; 15 GB free; kept the `bpy` 5.2.2 environment, the Whisper environments, `vendor/` and the FilmCraft trees; about 11 GB of older scratch remains". Because the kept environments live in a session scratchpad that a container restart can clear (the next commit's own message mentions a restart), add the one line that rebuilds each (`pip install bpy==5.2.2` in a Python 3.13 venv, about 1.4 GB and 402 MB of download; the Whisper venv likewise) so SP3 and the caption drafts do not depend on a folder nobody tracks.
6. **For the sweep review, not this one:** `skills-staging/` holds 17 staged copies again at HEAD (`2fdbdb4`); when they are approved, install them with the same staged-versus-installed byte comparison used here (every file under each staged directory, not only `SKILL.md`) and remove the staged copies in the same commit. The one `public_lint --all` finding at HEAD is the allowlisted KDE mailing-list address in a staged copy; add `skills-staging/**` to that allow entry's `paths` or clear it at install time, and note that the working tree's `stale_check` shows 9 hits in rows marked applied (the sweep's to explain).

## 5. What goes out now

Nothing in this housekeeping changes what the maker does this week (`BUILD-STATUS.md` section 2): hours daily, the PC inventory, `GATHER.md` Part A1 on Wed 21 Oct, the Craft zips on Sat 24 Oct, the Sunday questions on Sun 25 Oct, with nudge 1 applied to the sheet first.

*Nothing in this review was committed; the orchestrator commits. The housekeeping did what it said, verifiably, and left a dated trail; the nudges are the follow-through the gate already named plus one wording drift in the one maker-facing file.*
