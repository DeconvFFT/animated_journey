# Life Journey — Project Charter

**What we're making.** An animated film of one person's life, from childhood to today (she is 50+): a feature film of her life journey, crafted to a standard that could screen in a theatre. It covers every major milestone and, just as much, the texture between milestones: routines, places, objects, jokes, people. It is not a presentation, not a slideshow, not a reel and not a template. Its visual and thematic world is Hindu: Sanatan Dharma and its sanskriti (deities, epics, temple architecture, classical and folk arts, Sanskrit and her own regional language and traditions), rendered as animated design she will love. It must work beautifully on a mobile phone as well as on the big screen. Minecraft was only an example of the playful, crafted feel the maker wants; no Minecraft assets are used. Playable pieces are an optional companion keepsake, not the main event.

**Deadline.** Premiere on Saturday, Feb 27, 2027, at a mostly public gathering (about 19 weeks from Sunday, Oct 18, 2026).

**Current phase.** Learn. No code yet. We build understanding, reusable skills, references and a plan. Real photos and stories are gathered only after the pipeline and process are locked.

## Known facts (updated Oct 18, 2026)

- **Who:** the maker's mother (50+). She is from India and Hindu.
- **Theme (maker's definition, 2026-10-19):** when the maker says "Indian themes" it always means Hindu themes: Sanatan Dharma and its sanskriti. Hindu gods, epics, Hindu history, temple architecture and Hindu art traditions are welcome. No Mughal or other Islamic motifs and no Christian motifs, ever. Deities are depicted with correct iconography and respect.
- **Phone first, too:** the film and any keepsake must play beautifully on a mobile phone, not only on the venue screen.
- **Build approved (2026-10-19):** the maker approved moving from Learn to building the process on synthetic material, and merging the Learn work into `main`.
- **It's a surprise.** She doesn't know. All story gathering is covert, and nothing may tip her off (shared devices, cloud photo libraries, family group chats).
- **Only the maker knows.** The maker is the sole producer and nobody else is in on it. Relatives and friends can still be sources (stories, photos, recordings) through low-key asks that don't reveal the project, unless the maker later decides to bring someone in. The maker is her proxy for hard chapters, with the Fable advisor flagging anything sensitive.
- **Occasion and venue:** a premiere at a mostly public gathering on Feb 27. The maker wants it good enough to show in theatres, so treat it as a film with a public audience, not a family slideshow.
- **Maker's computer:** Windows. The Claude desktop app uses too much memory there, so heavy work (research, generation, rendering) happens in the cloud wherever possible.
- **Production approach: agents generate, apps refine.** Claude and the agent team are the primary engine: generation, scripted pipelines, code-driven animation. The maker's ArtCraft "Crafting Apps" (getartcraft.com, source at github.com/storytold: PhotoCraft, VectorCraft, FilmCraft, EffectCraft, LightCraft, SoundCraft and others) are refinement layers for fast human touch-ups and iteration. They are free, open-source and early alpha, so every step needs a proven fallback and nothing critical may depend on one alpha app.
- **Material exists:** printed and digital photos, home videos, letters, and people to interview. Collection starts once the pipeline is locked.
- **Project repo:** github.com/DeconvFFT/animated_journey, public by the maker's choice (the family doesn't use GitHub). Because it's public, it holds only text, scripts and manifests keyed by person IDs: never names, photos, recordings or anything that identifies her or the family.

## Principles

1. **Story before software.** Her real voice, places, objects and turning points drive every design choice. Tools come second.
2. **Mechanics and devices must mean something.** Every visual device, motif or transition has to express something about her life (the *Florence* / *Unpacking* test). A Hindu motif earns its place by being hers (her deity, her temple, her festivals, her region's art), not by being generically "Indian". No decoration for its own sake.
3. **Texture over checklist.** Milestones give the skeleton. The life lives in the gaps: habits, sayings, smells, songs, the kitchen table.
4. **Real memories stay real.** AI may restore, restyle, animate and connect real photos and stories. It does not invent events, fake people, or put words in anyone's mouth (no cloned voices). Reconstructed scenes are visibly reconstructions.
5. **Dignity, even as a surprise.** She can't approve it in advance, so the maker acts as her proxy for hard chapters (loss, illness, separation, money, conflict), with the Fable advisor flagging sensitive material for a deliberate decision. Anything she might not want shown in front of a public audience stays out.
6. **Theatrical bar.** Every shot must hold up on a big screen: art-directed, consistent across the whole film, free of AI artifacts, with a real sound mix and a proper master. "Good for a party" is not the bar.
7. **Cleared for public screening.** Music, photos taken by others, archival footage, fonts and the voices of people who appear are cleared for public exhibition.
8. **Finish beats sprawl.** Scope runtime to what a learner plus an AI team can finish to the theatrical bar by the deadline. One great sequence first (a vertical slice), then expand.
9. **Prefer scriptable tools.** Anything repeatable runs from the command line, so AI agents can help without driving GUIs.

## Team

| Role | Model | Job |
|---|---|---|
| Orchestrator | this session | plans, delegates, integrates, keeps the schedule |
| Advisor (on call) | Fable | reviews every artifact at every gate, nudges, untangles complex flows |
| Researchers / implementers | Sonnet | web research now; asset building and prototypes later |
| Scribes | Haiku | ingests research into playbooks, reusable skills and writeups |

## Review rubric (every artifact, each scored 1–5)

- **Meaning**: serves a personal, emotionally true story, not a generic one.
- **Specificity**: concrete, named techniques, tools and steps.
- **Accuracy**: claims backed by cited sources; dated or unverified items flagged.
- **Feasibility**: doable by a learner with free tools plus agents by the deadline.
- **Ethics**: consent, dignity, rights, honest use of AI on real memories.
- **Craft / usability**: holds the theatrical bar, and the artifact is usable by its reader (human or agent).

Approve only when every score is 4 or higher and nothing critical is open.

## Learning tracks (Phase 0)

1. `story`: life-story craft (gathering and shaping a 50+ year life)
2. `games`: games that tell life stories (mechanics that carry meaning, Minecraft and others)
3. `animated`: animated, documentary and web life-journey exemplars
4. `ai-imagery`: AI imagery and motion from real photos
5. `toolchain`: free desktop toolchain and core techniques
6. `format`: delivery format and experience architecture
7. `creator-threads`: creator recipes from X/Twitter threads, Reddit, YouTube and blogs
8. `craft-visual`: ArtCraft visual apps as refinement layers (PhotoCraft, VectorCraft, LightCraft)
9. `craft-motion`: ArtCraft motion and sound apps as refinement layers (FilmCraft, EffectCraft, SoundCraft)
10. `agent-pipeline`: agent-first production pipeline (what agents generate, where it renders, how it round-trips)
11. `surprise-ops`: running a surprise tribute for a mother (covert gathering, family coordination, the reveal)
12. `film-story`: writing a biographical animated film (structure, narration, runtime, treatment to animatic)
13. `cinematic-quality`: what makes animation theatrical, and how AI-assisted work avoids looking like AI
14. `production-scale`: how much film a learner plus AI team can finish to the theatrical bar, and how to schedule it
15. `music-sound`: score, songs, voices and the mix
16. `theatrical-delivery`: theatre-grade masters, DCP, venue playback, and rights clearance for public screening

## Open decisions (the maker's to make)

- Runtime: short film, mid-length, or full feature (the biggest lever on quality and schedule).
- Country/jurisdiction of the premiere (affects music and image rights).
- Whether to bring anyone else in later (for example to borrow albums or record stories).
- Sensitive chapters to handle carefully or leave out.
- Language(s) and audience (family of all ages? non-gamers?).
- Whether to make the optional interactive companion keepsake.

## Constraints

- Windows PC with the ArtCraft Crafting Apps installed; desktop-app memory use is a concern.
- The cloud session's container is temporary: everything worth keeping goes to the GitHub repo (public, so text and IDs only).
- GUI control of the maker's apps isn't connected; plan around agent generation, scriptable tools, and the maker's own hands in the Craft apps.
- Personal material stays private. Nothing personal is published or uploaded to a third-party service without the maker's explicit say.
