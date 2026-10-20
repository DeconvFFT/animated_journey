# Staging note: agent-first-production-pipeline (week-2 close-out, package c1-filmcraft-dissolve)

*Tue 20 Oct 2026. A Sonnet implementor wrote `SKILL.md` here as a copy of the installed `.claude/skills/agent-first-production-pipeline/SKILL.md` (as of commit 3a500dd) with the edits below. Nothing under `.claude/` was touched; the orchestrator installs this copy (byte comparison of both files first, then remove this folder). Fable has not read it yet (D-32).*

**Why.** The week-2 gate (`reviews/build/w2-gate-r1.md`, nudge 1) asked for the SP1 outcome and the rule "one chapter, one dissolve route" to be carried into the playbook and this skill. `T2.mid_dissolve` was amended to a linear-light mid-point, `T2.dissolve_steps` was added, and the one FilmCraft 0.9.0 stage was re-run: T2 now passes 14 of 14 (`build/evidence/wp07/t2_filmcraft_v0.9.0.json`; the first run's envelopes are in `build/evidence/wp07/first-mark/`). The skill still said that SP1 had not run.

**What changed (six edits and a changelog line; nothing else, so `diff` against the installed file shows exactly these):**

| Where | Change |
|---|---|
| Step 3 (classify the shot) | "`craft` runs in the container only after spike SP1 passes" becomes: EffectCraft drafts may run in the container (T4 passed), FilmCraft draft renders are allowed too (T2 passed on the amended mark) but nothing is planned on them, and every chapter keeps its OTIO and ffmpeg route as the fallback. |
| Step 9 (Route B shot) | One sentence: a dissolve inside a Route B chain is ffmpeg `xfade`, which blends the encoded values; points to step 16. |
| Step 14 (EffectCraft hand-off line) | "Use `effectcraft-cli render` in the container only after spike SP1 passes" becomes "may be used in the container (SP1 T4 passed on Tue 20 Oct 2026; Linux only)". |
| Step 16 (assemble the chapter) | The rule **one chapter, one dissolve route**: FilmCraft blends in linear light, ffmpeg `xfade` and the Chromium route blend the encoded values; the figures for the spike's colour pair; choose the route when the chapter is briefed; what mixing does. Cites `build/evidence/wp07/dissolve_routes.json`. |
| References, open gaps | "SP1 T2 and T4 have not been run, SP3 is deferred for disk space" becomes the 20 Oct results (T2 PASS 14 of 14 on the amended mark, T4 PASS 9 of 9, SP3 ran on a stand-in scene and passed its four timings with the pass mark waiting for the real kitchen). The SP3 clause was brought to `spikes/VERDICTS-W2.md` in the same sentence because it was equally out of date. |
| References, corrections in force | "Spike SP1 is still the gate" becomes "Spike SP1 has run (Tue 20 Oct 2026)" with the same outcome. |
| Changelog | One dated line. |

**Not changed:** the description, the procedure order, every figure, check, floor and gate, the phone figures (3.5 Mb/s and 32 characters stay as the installed copy has them), and the Sources.

**How to install.** `diff .claude/skills/agent-first-production-pipeline/SKILL.md skills-staging/agent-first-production-pipeline/SKILL.md` should show the edits above and no others (if another package has changed the installed copy since 3a500dd, merge by hand). Then copy `SKILL.md` over the installed one. `CHANGES.md` is a staging note and is not installed.

**UNVERIFIED.** The skill was not loaded into an agent to see whether its triggers still fire. Every Craft result in it is a Linux container result on flat synthetic stills; the Windows builds, real photographs and the dissolve's look on a screen are the maker's Sat 24 Oct tests and later checks.
