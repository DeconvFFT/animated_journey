# 03 — Verification of the integration review's fixes, round 1 (Fable advisor), 2026-10-18

**Scope.** `ROADMAP.md` v2.1 (363 lines), `PLAN-ON-A-PAGE.md` and `DECISIONS.md` v2 read in full; `reviews/03-integration-review.md` read in full; `CHARTER.md` read first. `playbooks/production-scale.md` lines 30–40 and 455–465 re-read to confirm the hours figures the fix relies on. The three documents were grepped for every retired spelling (`\bS[1-5]\b`, `\bL1\b`, "S1–S5", "all six", "1:30", "ten week-1", "hour or two", "30–45"). No web page was opened; no code was written. I did not edit any of the three documents.

**Verdict: approve.** Both critical issues are closed and all ten nudges are applied where the review asked for them. Four small residues remain, none of them a contradiction a maker or an agent would act on wrongly; they are listed as nudges for the next housekeeping pass.

| Score | 1–5 | Why |
|---|---|---|
| Meaning | 5 | Unchanged from the integration review: the only-me constraint is the film's form, and every device comes from her house. |
| Specificity | 5 | Every fix landed as a named file, command, number or date; `lj.ps1 close` has an owner, a deadline and a gate. |
| Accuracy | 4 | Cold open 1:15, five pinned apps, thirteen week-1 facts, two clips in week 3: all reconciled. Residue: §14 item 1 and the v2.1 changelog say "38 of 41" Table 4 rows applied when four rows are marked outstanding (37 of 41); the budget's "6–8 people" for S1 and S2 predates S1 shrinking to one or two. |
| Feasibility | 4 | The recommended rhythm now sums to the tier it buys (2 h + 2 h + 6 h = about 10 for 9 minutes; 16 for 12), the under-8 consequence is stated in all four places, review is 5–10 minutes a day, the session close is one command, and the maker types into three files. Up from 3. The 9-minute tier at about 10 h/week still depends on a fast slice (production-scale 36, 461), which the plan page states only as "the finished first chapter confirms it". |
| Ethics | 5 | Nothing in the fixes touched the consent, recording or dignity rules; the plan page's rule 3 now matches W-24 exactly rather than being stricter than the practice, so the maker will not be surprised by a `preview` request. |
| Craft / usability | 4 | L1 and S1 each mean one thing in all three documents; the plan page says it is rewritten every Sunday; the old spellings are on the `stale_check.py` list. The playbooks and skills still carry the old spellings (S-38, S-39, outstanding, Haiku before Fri 30 Oct), so an agent reading a playbook today can still misread "L1". |

---

## 1. Item-by-item check

| # | Item from the review | Status | Where I found it |
|---|---|---|---|
| C1 | Weekly rhythm cannot deliver the default runtime | **Applied.** | `PLAN-ON-A-PAGE.md` "What you do": "for 9 minutes, two weekday evenings of about 2 hours plus a 6-hour weekend block (about 10 hours, the weekend block holding the 3–4 hour Craft pass); for 12 minutes, 16 hours; under about 8 hours the honest plan is the 6-minute F-0, and we will say so". `DECISIONS.md` O-01 recommendation carries the same rhythm and cites W-02. `ROADMAP.md` §7 Hours: "At the recommended rhythm the plan buys its tier". |
| C1 | Under-8 consequence in risk 13 and W-02 | **Applied.** | `ROADMAP.md` §12 risk 13: "if the first logged week comes in under about 8 hours, F-0 (6 minutes) becomes the plan on Sun 1 Nov and 9 minutes the stretch, written in `decisions.csv` and on the plan page (W-02)". `DECISIONS.md` W-02 has the same sentence. Also mirrored in §6 settings-card row, §7 W2 gates column, `PLAN-ON-A-PAGE.md` runtime rule and Sun 1 Nov checklist line. |
| C2 | "an hour or two a day" of review | **Applied.** | `PLAN-ON-A-PAGE.md` "What you do": "five to ten minutes a day of watching with sound on and leaving coloured markers; you approve nothing until 48 hours have passed". Grep: no live "hour or two" anywhere outside research citations. Matches W-42 and §6 Dailies. |
| N3 | `lj.ps1 close` | **Applied.** | `ROADMAP.md` §5.1 "Close the day" row lists the seven actions, "Written by Sonnet before Sat 14 Nov; a P-LOCK pass condition"; §4.2 names it; §6 P-LOCK row "`lj.ps1 close` written and run once"; §7 W1 "v0", W4 "v1 run once end to end"; §0 says `stale_check.py` runs inside it. `DECISIONS.md` W-26 and W-06 carry the same. `PLAN-ON-A-PAGE.md` key dates: "including the one command that closes every session". |
| N4 | Three-files rule; merge consent and corrections into the rights log | **Applied.** | `ROADMAP.md` §5 opening paragraph, bold; `PLAN-ON-A-PAGE.md` "What you do". §5.1 "Manifest and ledgers" row: rights log (T8) with a `kind` column (`asset`, `person`, `cue`, `font`, `consent`, `correction`) "which absorbs the former consent and corrections ledgers so there is one ledger, not three". Residue: the name "consent ledger closed Mon 29 Mar" survives in W-48 and §7 "after" row, and W-21 still says "the rights log's `fonts` sheet" (nudges 2 and 3). |
| N5 | Per-chapter checks split gated / reported | **Applied.** | `ROADMAP.md` §6 "Per chapter, gated (a fail stops G4)" lists exactly the eight items asked for; "reported but not gated until G-DRAFT (… enforced only from Sun 31 Jan)" lists CoV ≥0.4, move families, holds ≥35%, ΔE00, half and double speed, sound-off and picture-off, plus the picture-led silence, blind A/B, squint and distance. `DECISIONS.md` W-42 mirrors it in one sentence. |
| N6 | S1 one or two strangers or the cold self-read; the two T7 questions | **Applied.** | `DECISIONS.md` W-43 ("S1 one or two strangers to her … remote on the redacted proxy if easier, or the cold self-read with Fable's rubric pass; S2 three to five … week 17"; both T7 questions with the cookie-cutter note); S-04 canonical column updated. `ROADMAP.md` §6 Strangers paragraph and G-SLICE row; §7 W9 gathering column. S2 unchanged. Codes block S1/S2 definition matches. |
| N7 | W-60 two clips, three optional films | **Applied.** | `DECISIONS.md` W-60: "Two clips (*Up* 'Married Life', *Danny & Annie*) timed with the stopwatch sheet in week 3 as G1 input (`story` Ex 1); three films optional in weeks 10–11 (`film-story` Template 9)". Matches `ROADMAP.md` §8 week 3 and 10–11 and §7 W3/W10. |
| N8 | S1–S5 → SP1–SP5; L1 → P-LOCK; old spellings on the stale list | **Applied in the three documents.** | `DECISIONS.md` Codes: P-LOCK and SP1–SP5 defined with "a spelling now retired"; S-38 and S-39 added to Table 4 (outstanding, Haiku before Fri 30 Oct); W-29 lists "L1 process lock", "L1 lock", "spikes S1–S5", "spike S1", "S1–S5", "S1-S5". `ROADMAP.md` §0 Codes bullet, §5.1 Gate column (P-LOCK), §5.2 ("spike SP1 T2/T4"), §6 ("Spikes SP1–SP5", "P-LOCK (process lock)"), §7 W1–W4, §8 header. Grep of the three documents: every remaining "S1"/"S2" is a stranger screening; every remaining "L1" is either the honesty level or a quoted stale string. The playbooks, skills and fixtures still carry the old spellings by design until the scribe pass (Table 4 S-38, S-39; §14 item 1). |
| N9 | Five pinned apps; cold open 1:15; thirteen week-1 facts | **Applied.** | `ROADMAP.md` §6 P-LOCK row and `DECISIONS.md` W-06: "five-minute tests on the five pinned apps (SoundCraft is unpinned and learning-only, D-12)"; grep finds no "six apps". `DECISIONS.md` W-36: "Cold open (about 1:15)", matching W-04 and §3.2. `ROADMAP.md` §7 W1 gates: "the thirteen week-1 facts answered (O-01…O-13)". `PLAN-ON-A-PAGE.md` Sat 24 Oct: "the five Craft apps". |
| N10 | Plan page rule 3 and the 14-day header | **Applied.** | Rule 3 ends "unless you yourself raise a photo set to 'preview', which lets a small 768-pixel copy reach the agents' review packs after the model-improvement setting is off; nothing full-size, ever", matching W-24 and §4.3. "The next 14 days" opens with "*Rewritten every Sunday by the orchestrator; the dates below are always the next fourteen days.*" |

**Arithmetic check on C1.** Two evenings at about 2 h plus a 6-h block is 10 h, which production-scale (Working answer, line 36; T2 worked reading, line 461) gives as the cost of 9 minutes "if the slice comes in near Prior speed". 16 h for 12 minutes matches W-02 and §3.2 (the four-lever figure is about 15.5 h). Under 8 h there is no tier above F-0, so the Sun 1 Nov consequence is the right one and is now stated. Consistent in all four places the review named and in three more.

## 2. Residues (none critical)

1. `ROADMAP.md` §14 item 1 and the v2.1 changelog line: "38 of the 41 rows of `DECISIONS.md` Table 4 are applied". Table 4 marks four rows **outstanding** (S-01, S-38, S-39, S-40), so the figure is 37 of 41.
2. `DECISIONS.md` W-48 and `ROADMAP.md` §7 "after" row still say "consent ledger closed Mon 29 Mar" after §5.1 folded the consent ledger into the rights log as `kind: consent`. Say "the rights log's consent rows close Mon 29 Mar" so there is one name for one log.
3. `DECISIONS.md` W-21 "Every font has a licence file in the rights log's `fonts` sheet" versus §5.1's `kind: font` row. One structure or the other; a `font` row with a `licence_file` column is the simpler match for a one-person log.
4. `ROADMAP.md` §10 "Strangers' thanks, S1 and S2 (6–8 people at $10–20)". With S1 at one or two and S2 at three to five, the count is 4–7; the dollar range still holds.

Optional, for honesty on the maker's page (not a contradiction): `PLAN-ON-A-PAGE.md` runtime rule says "about 10 is what 9 minutes costs"; W-02 and §7 Hours say "about 10 h/week **with a fast slice**". The page's next sentence ("The finished first chapter on 20 December confirms it") carries the caveat implicitly; four words ("if the first chapter comes in fast") would carry it explicitly.

## Critical issues

None open. C1 and C2 are closed.

## Nudges (at most six; file, section, exact change)

1. **`ROADMAP.md` §14 item 1 and changelog v2.1.** "38 of the 41 rows" → "37 of the 41 rows" (four outstanding: S-01, S-38, S-39, S-40).
2. **`DECISIONS.md` W-48; `ROADMAP.md` §7 "after" row.** "consent ledger closed Mon 29 Mar" → "the rights log's consent rows (kind `consent`) close Mon 29 Mar", so the merged log keeps one name.
3. **`DECISIONS.md` W-21.** "a licence file in the rights log's `fonts` sheet" → "a `font` row in the rights log (T8) with its licence file named", matching §5.1's `kind` column.
4. **`ROADMAP.md` §10 budget row "Strangers' thanks".** "(6–8 people at $10–20)" → "(4–7 people at $10–20)"; keep $60–160.
5. **`PLAN-ON-A-PAGE.md` "The runtime rule, in one line".** "about 10 is what 9 minutes costs" → "about 10 is what 9 minutes costs if the first chapter comes in fast" (optional; mirrors W-02 and §7 Hours).

## Advisor insight

The fix that mattered was arithmetic: the plan now asks the maker for the hours it actually needs, and tells them what happens if they cannot give them. Everything left is naming. The one thing to watch next is outside these three documents: until the Haiku pass of Fri 30 Oct lands S-38 and S-39, an agent that opens a playbook rather than the register will still read "L1" as the lock and "S1" as a spike, which is exactly the misread the rename was meant to prevent. The first `stale_check.py` run that day is the real close of this review.

## Changelog
- 2026-10-18, v1. Fable advisor, verification round 1 of `reviews/03-integration-review.md`. All twelve listed items confirmed applied in `ROADMAP.md` v2.1, `PLAN-ON-A-PAGE.md` and `DECISIONS.md` v2; four naming or counting residues recorded as nudges; verdict approve.
