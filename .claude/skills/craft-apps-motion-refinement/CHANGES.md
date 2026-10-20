# Staging note: craft-apps-motion-refinement (week-2 close-out, package c1-filmcraft-dissolve)

*Tue 20 Oct 2026. A Sonnet implementor wrote `SKILL.md` here as a copy of the installed `.claude/skills/craft-apps-motion-refinement/SKILL.md` (as of commit 3a500dd) with one quality-bar line changed and one changelog line added. Nothing under `.claude/` was touched; the orchestrator installs this copy (byte comparison of both files first). Fable has not read it yet (D-32).*

**Why.** The installed quality bar says "A mid-dissolve pixel is within 2 levels of the average of its neighbours". That is the first wording of `T2.mid_dissolve`, which no compositor that blends in linear light can pass; the week-2 gate (`reviews/build/w2-gate-r1.md`, nudge 1) amended the mark to the linear-light mix. Left alone, an agent following this skill would fail FilmCraft on a correct dissolve.

**What changed.** Quality bar, "Dissolves are centred on the cut": the mid-dissolve pixel is within 2 levels of the 50/50 mix of its neighbours in linear light, an exported 12-frame dissolve shows at least 11 distinct levels, and "one chapter, one dissolve route". One changelog line. Nothing else (`diff` shows two places).

**Not changed.** The procedure, the Ken Burns maths, the hand-off formats, the checklists.

**How to install.** `diff .claude/skills/craft-apps-motion-refinement/SKILL.md skills-staging/craft-apps-motion-refinement/SKILL.md`, then copy `SKILL.md` over the installed one; `CHANGES.md` is a staging note and is not installed.
