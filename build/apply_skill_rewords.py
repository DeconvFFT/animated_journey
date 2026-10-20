#!/usr/bin/env python3
"""build/apply_skill_rewords.py: the reworded lines that clear the 11 stale hits in the installed skills (gate-r1 nudge 1).

WHO RUNS IT   the orchestrator (the implementor may not edit .claude/). Standard library only.
WHAT IT DOES  For each of seven installed skills it replaces one exact phrase (or two) inside a "Reconciled with
              DECISIONS.md" line with a wording that no longer quotes a retired value. The meaning is unchanged:
              each line only said that the old value is retired.
HOW TO RUN    python3 -I build/apply_skill_rewords.py            dry run: prints every change, writes nothing
              python3 -I build/apply_skill_rewords.py --apply    writes the seven SKILL.md files in place
              afterwards: python3 -I scripts/stale_check.py --baseline   (re-cut; the 11 hits are then gone, not baselined)
SAFETY        Refuses to touch a file unless every phrase occurs exactly once (it prints which one and changes nothing in
              that file). Reads and writes only .claude/skills/<name>/SKILL.md. No network, no deletion, no names or paths
              beyond the repository-relative ones printed. Review the result with: git diff .claude/skills
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITS = {
    "free-creative-toolchain": [
        ("`r5_story.mlt` with `atsc_1080p_25`)", "`r5_story.mlt` with the 25 fps MLT profile)")],
    "hindu-life-story-frameworks": [
        ("Chhath is no longer a schedule constraint (W-77, S-61)",
         "the Bihar and UP observance is no longer a schedule constraint (W-77, S-61)")],
    "journey-format-architecture": [
        ("The notes' old 100 to 150 h for the linear film is retired:",
         "The notes' original linear-film hour range is retired:"),
        ("the Minecraft question, the game-render row,", "the game-world question, the game-render row,")],
    "life-story-interviewing": [
        ("and the \"closest insider\" does not exist.", "and no inside-helper role exists."),
        ("\"L1 process lock\" becomes P-LOCK (S-38);", "the earlier process-lock spelling becomes P-LOCK (S-38);")],
    "meaningful-game-mechanics": [
        ("The Minecraft and voxel clauses are retired under D-29 (S-45, S-50):",
         "The game-world clauses are retired under D-29 (S-45, S-50):")],
    "surprise-tribute-operations": [
        ("\"L1 process lock\" becomes P-LOCK (S-38);", "the earlier process-lock spelling becomes P-LOCK (S-38);")],
    "life-film-story-structure": [
        ("a co-reviewer or an insider (D-03;", "a co-reviewer or any inside helper (D-03;")],
}


def main(argv):
    apply = "--apply" in argv
    if any(a not in ("--apply",) for a in argv):
        print("usage: python3 -I build/apply_skill_rewords.py [--apply]")
        return 2
    bad = 0
    for name, reps in EDITS.items():
        rel = ".claude/skills/%s/SKILL.md" % name
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            print("MISSING  %s" % rel)
            bad += 1
            continue
        new, ok = text, True
        for old, repl in reps:
            n = new.count(old)
            if n == 0 and repl in new:
                print("already  %s: %r" % (rel, repl[:60]))
                continue
            if n != 1:
                print("REFUSED  %s: phrase occurs %d times, expected 1: %r" % (rel, n, old[:70]))
                ok = False
                break
            new = new.replace(old, repl)
            print("%-8s %s: %r -> %r" % ("change" if apply else "would", rel, old[:50], repl[:50]))
        if not ok:
            bad += 1
        elif apply and new != text:
            path.write_text(new, encoding="utf-8", newline="")
    print("%s. %s" % ("done" if apply else "dry run, nothing written", "%d file(s) refused or missing" % bad if bad else "all phrases found"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
