# Animated Journey: project rules

This repo holds the production of a surprise animated film about the maker's mother's life, premiering Saturday, Feb 27, 2027 at a mostly public gathering, made to a standard that could screen in a theatre. Read `CHARTER.md` first. `ROADMAP.md` is the plan once it exists.

## Non-negotiables

- **Secrecy.** It's a surprise and only the maker knows. Never contact anyone, post anything, or put project details anywhere outside this repo and the maker's own machine.
- **Privacy.** Personal media (photos, scans, home video, letters, interview audio) is never committed to git and never uploaded to a third-party service without the maker's explicit OK for that service. Keep it in `media/` (git-ignored) or the maker's own storage.
- **Real memories stay real.** Restore, restyle, animate and connect real material. Never invent events, fabricate people, or clone voices. Reconstructions must read as reconstructions.
- **Theatrical bar and rights.** Every shot must hold up on a big screen, and everything shown in public must be cleared (music, other people's photos, footage, fonts, voices).

## Team and review gates

- Agents live in `.claude/agents/`: `fable-advisor` (reviews every artifact), `sonnet-researcher`, `sonnet-implementor`, `haiku-scribe`.
- Skills live in `.claude/skills/`. Each one is the agent form of a playbook in `playbooks/`, backed by sourced notes in `research/`.
- Nothing counts as done until `fable-advisor` approves it: every rubric score 4 or higher (rubric in `CHARTER.md`). Reviews are saved in `reviews/`.

## Layout

- `CHARTER.md`, `ROADMAP.md`: what we're making and the plan
- `research/`: sourced research notes
- `playbooks/`: guides for the maker
- `reviews/`: Fable reviews
- `.claude/agents/`, `.claude/skills/`: the AI team and its skills
- `media/`, `renders/`, `exports/`: git-ignored working media

## Git

- `main` holds reviewed work. New work goes on a feature branch (`learn/...`, `story/...`, `build/...`); save and push as you go, and merge to `main` when the maker agrees.
- Never commit personal media, secrets or large renders. Generated, non-personal images can be added with `git add -f` after review.

## Maker's setup

- Windows PC with the ArtCraft Crafting Apps (PhotoCraft, VectorCraft, FilmCraft, EffectCraft, LightCraft, SoundCraft) as refinement layers: agents generate, the apps refine. They are early alpha, so every step needs a fallback.
- The Claude desktop app is too memory-heavy there, so heavy work runs in the cloud.
