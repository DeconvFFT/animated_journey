# Production Scale: How Much Film Can One Maker and an AI Team Finish?

*Draft v3, 2026-10-18 (Sunday, week 1 of 19). Track `production-scale`. Built by the Haiku scribe from `research/production-scale.md` (researcher Sonnet, 2026-10-18, with follow-ups F0 to F5 and G1 to G6) and `CHARTER.md`. Rounds 1 and 2 of the review applied (`reviews/production-scale-round2.md`). Reconciled with `DECISIONS.md` (the decisions register; where this playbook and the register disagree, the register wins). Open items are marked TODO(research).*

*How to read the labels. [n] points to the Sources list at the end, using the same numbers as the research note. **[J]** is judgement, not a measurement. **ESTIMATE** is arithmetic on measured or sourced numbers. **UNVERIFIED** means nobody has checked it yet. **Hearsay** means a forum post, résumé or unnamed source. **Snippet-only** means we saw a search summary, not the page.*

## Why this matters for our film

The question is simple to say. How much finished film can one learner, working with an AI team, make to the theatrical bar by Saturday 27 February 2027?

The charter defines the bar. Every shot must hold up on a big screen. It must be art-directed, consistent across the whole film, free of AI artifacts, with a real sound mix and a proper master [1]. "Good for a party" is not the bar.

The honest answer today is that we can estimate it, but we cannot measure it yet. Three things drive the estimate.

**First, your hours.** The number of hours a week you can reliably give moves the answer more than anything else. We do not know it yet. At 10 hours a week a 12-minute film is not safe. At 20 hours it fits only with the levers in Step 3: in the Base case it passes the total-hours check but fails the post-holiday check (largest Base film at 20 h is 9.4 minutes). The research note says the answer moves by a factor of three to five between the optimistic and cautious cases.

**Second, the minutes per shot.** Every minute-per-shot number in our plan is a judgement [J]. No published source measures maker-hours per minute for a photo-forward documentary at the theatrical bar. The vertical slice (described below) is how we replace the guesses with our own numbers.

**Third, the calendar.** The holidays take two weeks out of the middle. Production after them is five weeks, finishing is two, and the last week already holds rehearsals. The real budget is 17 usable weeks, not 19.

**Benchmarks say the plan is ambitious.** Festival-quality animated features made by one person ran about 1.1 to 3.7 finished minutes per person-month. *Away* ran about 1.8 and *Sita Sings the Blues* about 1.4 [10][14]. Small teams ran about 0.06 to 0.3 [12][33]. For scale, *Sita* took an estimated 114 hours per finished minute [14], and *Away* about 150 by estimate [10]. Agency explainer videos are quoted at 40 to 60 hours per minute, but that is a vendor's rule of thumb and hearsay [40].

Our Base case implies about 6.8 finished minutes per person-month. The older playbook numbers imply about 13.6 [2][5]. That is two to twelve times the best solo results. It is only believable because about 85 percent of the model's shots are photo moves (class A, 60 percent) or designed graphics (class B, 25 percent). Those are far quicker than drawn or posed character animation [2]. Treat the 6.8 as a claim to prove, not a forecast.

Traditional feature animation ran about 1 to 7 seconds of finished film per animator-week at feature quality [25][26]. Our Base case implies about 101 seconds per person-week for a 12-minute film (ESTIMATE). That is several times the fastest traditional rates, such as the TV quotas of 25 to 30 seconds, which are hearsay [28]. It works only because most of our shots are not character animation.

The one shot class that does drive the schedule is the hero shot (class C). In the Base case it is 10 percent of shots but about 60 percent of shot-hours [2]. That is where the schedule is won or lost. One shot in *Spring* took two to three weeks to animate [34].

The closest relative to our subject is the StoryCorps animated short work, which took 13 weeks for 3 minutes 15 seconds with 6 to 8 people [31]. Our plan replaces drawn characters with real photographs. That is why the numbers can be lower. It is not proven yet.

The older estimate in the format playbook was 100 to 150 maker-hours for 8 to 12 minutes, a judgement and not a measurement [5]; the format playbook now defers to this model (`DECISIONS.md` W-02). Our model's 12-minute film needs 141 hours in the Prior case, 284 in Base, 201 with the levers and 116 in the best case. The older estimate fits only the optimistic cases.

### Working answer (current lean, to be confirmed)

- Commit to a **12-minute public cut**, built as a wrapper (cold open about 1:15 and ending about 1:45) and three modules of about 3:00, if you can give **16 hours a week or more** in writing and we adopt the four levers in Step 3 that need no purchase (`DECISIONS.md` W-01, W-02, W-04). Between 14 and 16 hours, plan 12 only if you add hours or buy captions; otherwise 9.
- If H is **under 14 hours a week**, plan **9 minutes (wrapper plus two modules)** from Sunday 15 November, not from 20 December. At 10 hours, 9 minutes fits only with all five levers and a slice of about 13 hours or less, about half the Base prediction; lever 3 (bought finishing) is off under only-me (W-50), so the rule is: **9 minutes if the slice comes in near Prior speed (about 10 hours); otherwise add hours.**
- Treat **15 to 18 minutes** as a stretch. It opens only at G-SLICE on 20 December, only if H is 20 or more and the slice fits T2, and it is not recommended for the premiere cut under only-me (W-03). The fallback F-0 is 6 minutes: the wrapper plus one 3:00 module (W-05).
- There is **no 25-minute plan.** The former private cut is re-purposed as the April version, the same locked picture with voices on (D-06). Do not plan **45 or 90 minutes** (D-24).

The story track's old floor of 12 minutes is retired: 12 is the target when H allows and 9 when it does not (W-02). The conflict is resolved.

The next step is the vertical slice. It is one complete chapter, built to final quality, that measures your real minutes. The 20 December gate uses that measurement to choose the runtime.

## Core principles

1. **Decide the runtime in the open.** Story sets the range. The schedule sets the limit. You choose inside both. Feasibility should neither shrink a film the story needs nor stretch it past the hours you can give [1][7].
2. **Finish beats sprawl.** One complete 12-minute film is worth more than a 45-minute film with half its modules missing [1].
3. **Build the slice first.** The slice chapter (C01 = first built, not first in the film) is one complete chapter at final quality, with real sound, grade, captions and a master. It is the only honest way to measure our minutes [64].
4. **Cap the hero shots.** Keep class C at 5 percent of shots and build them on reused sets. Hero shots decide the schedule [2].
5. **Lock in order, and make the lock a file.** Picture lock is the point where the cut stops changing [63]. We record it in the repo, with a timeline hash, a status flag and a git tag, so the lock does not depend on memory.
6. **Log every hour.** Your logged minutes replace our guesses. The model's calibration number (`mu`) is the ratio of your actual maker minutes to the estimated minutes, measured after the first 20 shots.
7. **Plan around what can vanish.** The Craft apps are early alpha, so every step needs a fallback [1]. Hosted AI services can be shut down. Sora's app went dark in April 2026, and *Critterz* lost its video model [44][45]. No shot class may depend on one hosted model.
8. **Real memories stay real, and family material stays home.** AI may restore, restyle, animate and connect real photos and stories. It may not invent events or people, or put words in anyone's mouth [1]. Personal files stay on your PC unless you decide otherwise.

## How to do it, step by step

### Words you will see

- **H**: the hours per week you can reliably give. Usable hours are 85 percent of H each week (u = 0.85) [J].
- **Runtime tier**: 6 (F-0), 9, 12, or 15 to 18 (stretch). The 25-, 45- and 90-minute rows in the tables below are kept for comparison only; they are not production targets (`DECISIONS.md` W-03, D-24).
- **Wrapper and modules**: the film is a wrapper (cold open about 1:15 and ending about 1:45) plus modules of about 3:00 each. Twelve minutes is the wrapper plus three modules; fifteen is the wrapper plus four [7]. The model's 100-second chapter is the learning-curve unit, not the cut structure, so seven of them for 12 minutes stays valid. The agent-pipeline playbook also defines a chapter as about 100 seconds [2]. Decided in round 2, with no open items: (a) this track plans 12 minutes as wrapper plus three 3:00 modules. `research/film-story.md` (runtime table, 12-minute row) and `playbooks/film-story.md` (runtime shapes) still carry four chapters of 2:15 for 12 minutes while their recommendation uses 3:00 modules; delta logged for film-story's next round; the cost model is unchanged either way (n = 7 learning units). Resolved by `DECISIONS.md` W-04: the 3:00 module is the shape; film-story's 2:15 row is superseded. (b) The 8-minute tier is replaced by 9 minutes (wrapper plus two modules), the nearest whole-module version. (c) At the 17 January gate, below 5.4 minutes approved, cut one module (the lowest-priority), not two; a second module is cut only at G-DRAFT if it is not at draft. (d) The slice is a 100-second piece of module M1 (acceptance 90 to 120 seconds), not all 180 seconds of it; the rest of M1 is built after the gate (Step 8). (e) Shot IDs carry wrapper shots: the pattern is `^LJ-(C\d{2}|W\d)-S\d{3}$`.
- **Shot classes**: A is a photo move, B a designed graphic, C a hero shot, D a title or caption. The model's mix is 60, 25, 10 and 5 percent of shots [2].
- **Animatic**: a timed rough cut made from real pictures and temporary sound.
- **Slice**: the one complete piece we use to measure (Principle 3): 100 seconds of module M1.
- **Master**: the final picture and sound files that everything else is made from. The plan uses ProRes 422 HQ, plus an H.264 access copy [3].
- **DCP**: the digital package cinemas use to play a film. Whether we need one is decided by the venue's written answer, due Sunday 15 November (`DECISIONS.md` W-17).
- **Cases**: *Prior* uses the older playbook numbers. *Base* is the research note's evidence-adjusted case. *Levers* is Base with the five levers (lever 3, bought finishing, is off for the premiere cut under only-me, `DECISIONS.md` W-50; read the *Four* case as the plan). *Four* is Base with the four levers that need no purchase. *Best* is Prior speeds with the structural levers. *Stress* is a plausible bad run.

### Who does what

Agents draft, render, measure and check files. You decide what the film says and how it feels. You also listen to every chapter on the speakers it will play on. Agents can measure loudness, but they cannot judge whether a sound feels right [2].

The table below shows the Base case for each stage, in maker-hours per finished minute.

| Stage | Output | Who | Base maker-hours per minute |
|---|---|---|---|
| Treatment, card text, beats (`film-story`) | beat sheet, card text and sound script | agent drafts, you decide | 0.5 |
| Storyboard and animatic | timed boards with temporary sound | agent assembles, you review | 0.5 |
| Gathering, scanning, labelling, clearances | manifest lines, consent notes | you | 1.2 |
| Layout and shot brief (G0, G1) | `brief.yaml`, three style frames | agent writes, you approve | counted in shot minutes |
| Animation and compositing (Routes A and B, Blender) | draft renders (G2) | agent builds, you review | 4.6, including rework and reuse |
| Hand refinement in the Craft apps (G3, classes B and C only) | Craft-app passes | you | counted in shot minutes |
| Chapter assembly and passes (G4 to G6) | chapter master | you and agent | 1.2 |
| Score, sound integration (no narrator) | cue sheet, stems | you choose; library, CC0, CC BY or your own sound, no composer (D-07, W-44); agent assembles | 0.6 |
| Grade, mix, captions, QC | final audio and picture | you (lever 3 is off for the premiere cut, W-50) | 2.7 |
| Master, access copy, DCP or file, verification | ProRes 422 HQ, H.264, checksums | agent scripts, you check | 24 fixed hours |

G0 to G6 are the review gates in the agent-pipeline playbook [2].

For the whole 12-minute film in the Base case, the total is about 284 hours. Shot production takes 94 hours, chapter passes 24 and sound integration 7. Story takes 12 hours, gathering 14, the risk reserve 15 and finishing 56. One-off learning, the reuse build and rehearsals take 60 [J/ESTIMATE].

### Step 1. Give the schedule your hours (by Sunday 15 November 2026)

Write one number in the repo: the hours per week you can reliably give from now until 27 February. "Reliably" means the number you could keep up in most weeks, not your best week [J].

Also say what you can give in the holiday weeks. The model counts zero hours for 20 December to 2 January. Tell us if that is wrong.

Tell us which family or cultural observances fall in production weeks. The jurisdiction is unknown, and the dates in the Decisions section are unverified.

If H is not written by 15 November, the gate allows one week of grace, to 22 November. After that, drop one runtime tier [notes, gates].

### Step 2. Choose a provisional runtime

Use the tables in the Templates section. The rules from the research note are these.

- **H under 14**: plan 9 minutes (wrapper plus two modules) from Sunday 15 November, not from 20 December (`DECISIONS.md` W-02; Words, item b). Skip the reuse program beyond the kitchen and the title system, and accept a templated look where you must (research note, Q5). A bought master chain is off under only-me (W-50); add hours instead.
- **H 14 to under 16**: plan 12 minutes only if you add hours or buy captions; otherwise 9.
- **H 16 or more, with the four levers in Step 3 adopted**: plan 12 minutes (wrapper plus three modules).
- **H about 20 or more**: 15 to 18 minutes becomes a stretch that can open only at G-SLICE on 20 December, if the slice meets the T2 thresholds (W-03); it is not recommended for the premiere cut under only-me.
- There is no 25-minute plan and no 25-minute private cut: the April version is the same locked picture with voices on (D-06).

Do not plan above 12 minutes before the slice speaks (D-24).

### Step 3. Adopt the levers now (four now; the fifth is off for the premiere cut)

Five changes make 12 minutes fit at 14 to 20 hours a week in the Base case. Lever 3 (bought finishing) is off for the premiere cut under only-me (`DECISIONS.md` D-07, W-50), so the other four are the plan: they fit 12 minutes at about 16 hours a week or more. Each is an input in the model.

1. **Hero shots at 5 percent, not 10.** Move the shots from class C to class A where you can. In Base, the 12-minute film drops from 19.6 to 17.6 hours a week.
2. **Eight shots per minute, not twelve.** Longer holds, closer to documentary pace. In Base, 19.6 falls to 17.2 hours a week. Stop-motion features run 6 to 12 shots per minute, and *Memoir of a Snail* used shots "only five to 10 seconds long" [70].
3. **Buy or template the mix, grade and captions (OFF for the premiere cut).** Finishing would fall from 2.7 to 0.8 maker-hours per minute, and in Base 19.6 would fall to 18.1 hours a week. Under only-me a bought mix is a person brought in, so do the mix and grade yourself, with the finishing chain rehearsed inside the slice and rolling chapter locks from 17 January (`DECISIONS.md` W-50, D-07). Captions are the small part: $25 to $36 bought from a transcription service, which sees text and not pictures or a name, or free in DaVinci Resolve or a local tool [77][78][79]; buy captions alone only if time is short. Two dated quotes (research F1; two logged quotes, each with both prices and a turnaround of 10 working days or less) are needed by G-READY (Sunday 15 November) only if you want the option, and a bought mix is re-opened for the April version.
4. **Triage the photos.** Decide which photos need hand work before you start. Class A falls from 7 to 4.5 minutes a shot. In Base, 19.6 falls to 19.1 hours a week.
5. **Front-load gathering.** Get material in hand before 20 December. Alone, the lever tests 60 percent of production built before the holidays. It changes little at 12 minutes, but it raises the largest film you can finish at 20 hours a week from 9.4 to 12.0 minutes. The all-levers case uses 50 percent.

Together, the five levers bring the 12-minute film from 19.6 to 13.9 hours a week, and the 25-minute film from 31.5 to 21.1. At 20 hours a week the largest film rises from 9.4 to 20.7 minutes. At 30 hours it rises from 15.5 to 32.7 minutes. Without the bought finishing (lever 3), the four levers give 15.5 hours a week for 12 minutes and 24.4 for 25 minutes; the largest film is 18.2 minutes at 20 hours and 29.0 minutes at 30 hours. Plan on these four-lever figures (`DECISIONS.md` W-02, W-50).

Buying the mix and grade is the largest finishing lever, but it is off for the premiere cut (W-50); the budget ceiling is still pending from the maker (O-04).

### Step 4. Set up the tracking files in the private repo

Create these plain-text files in the private repo. Templates are in the Templates section.

- `shots/status.csv`: one row per shot.
- `chapters.csv`: one row per chapter or module.
- `hours.csv`: one row per work session.
- `gates.csv`: the calendar of gates.
- `decisions.csv`: every kill, cut and unlock, with the measured number behind it.
- `brief.yaml` for each shot: the full shot brief, as the agent-pipeline playbook sets out [2].

We are not using a tracking tool. Kitsu is open-source and mature, and Blender Studio uses it [76]. But for one person its hosted plans cost €20 to €35 per user per month [58]. Self-hosting needs Ubuntu 22.04 or later, PostgreSQL, Redis and Nginx [59][60]. Revisit only if a second person joins and the shot count passes about 500.

Git history is the audit trail. Agents read and write these files directly, and a short script checks them against the rules in the Templates section.

### Step 5. Start logging hours today

Each work session is one row in `hours.csv`: date, shot or chapter, activity, minutes, who, and a note. The activity names are listed in the Templates section.

Log learning and rework too. They are real hours. The model allows 60 of the 284 Base hours for one-off learning, reuse build and rehearsals [J].

### Step 6. Make the look before you make the film (G1, by Sunday 15 November)

Write the style bible. It covers the look, the palette, type, motion rules and the rules for seeded variety. It also sets a template check: no more than 60 percent of tweens may share one ease [2].

Make three style frames. A suggested set is one class A, one class B and one class C shot [J].

Days are enough for this. Pixar's look tests were "super quick and dirty, just with a few days of work for each," so the team agreed the direction early [67].

### Step 7. Check the render setup (spikes S1 to S5)

The G-READY gate needs spikes S1 to S5 to pass, or fallbacks named. They are the spikes in the agent-pipeline playbook, Step 3 [2]:

- **S1:** the Craft command-line tools inside the container. The scope is in `research/craft-motion.md` (R8) [3].
- **S2:** frame capture for Route A.
- **S3:** Blender, for hero shots. It measures one real kitchen frame against the table in the render bullets below (pass: within 2 times the table).
- **S4:** how the cloud container behaves when idle. Open question: does a running background job keep it awake? TODO(research), not documented in the pages read.
- **S5:** the validators (the agent-pipeline templates).

The G-READY settings card is the project settings card in the agent-pipeline playbook [2]: picture 1920 x 1080; frame rate 24 frames per second (settled; signed on the settings card on Sunday 1 November, `DECISIONS.md` W-14, W-16); Rec. 709 and sRGB; sound 48 kHz, 24-bit; master ProRes 422 HQ. Decision 12 records that the frame rate is settled.

These numbers were measured in the project's cloud container on 18 October 2026. The container has 4 vCPUs, 16 GB of RAM, no GPU and 24 to 28 GB of free disk [3].

- Photo moves (Route B): about 7.8 frames per second at 1080p, in one process.
- Blender Workbench (drafts): about 1 second per frame.
- Blender Cycles, 24 samples with denoise, 1080p: 17.5 seconds per frame on one lit Suzanne scene, and 204 seconds on Blender's 'classroom' benchmark scene (research note F3). The stylised kitchen set will fall between them; spike S3 measures it. A stand-in kitchen with no photographs measured 112 seconds at 64 samples and 204 seconds at 128, with denoise, on the container (research note G2; no GPU run).
- Software EEVEE: 34 to 36 seconds per frame, which is slower than Cycles here.
- A 12-minute film is 17,280 frames at 24 frames per second. It needs about 18 CPU-hours at Suzanne speed and about 150 at classroom speed, almost all of it for hero frames (883 ten-minute jobs at classroom speed; 76 at Suzanne speed).
- A foreground command stops after 10 minutes. A background job gets 30 minutes by default, and up to 2 hours with a timeout. A reclaimed machine does not restore running jobs [3].
- A depth-parallax route measured 12.3 frames per second at 640 x 480. Scaled to 1080p it is about 1.8 frames per second. That is an ESTIMATE and UNVERIFIED [4].

So render in ranges of frames. Write each frame as it finishes, skip frames that already exist, encode each chunk, and delete its frames. Loose PNG frames for a 12-minute film would take about 35 GB, which is more than the free disk [3].

**Hero finals are GPU work by default.** The maker's own PC (Exercise 1) is the first choice. RunPod's RTX 4090 costs $0.34 to $0.89 an hour, on a page updated 8 October 2026 [54]; use it only for a scene with no family imagery, only on Secure Cloud with an encrypted volume and the maker's recorded OK, and never on Community Cloud (`DECISIONS.md` W-23, D-15). On a 4090 a classroom-class frame at 1080p takes about 1.6, 3.0 and 5.6 seconds at 64, 128 and 256 samples [82][83][84]. The 12-minute film's 2,592 hero finals would take 1.2 to 4.0 GPU-hours, about $0.4 to $3.6 (ESTIMATE; denoise and pod start-up are not included). A scene that uses her photographs as textures counts as family imagery for this rule, and needs the maker's explicit say before it goes to a pod. Spike S3 passes if one real hero frame on a rented or maker-owned GPU lands within 2 times the table for its samples and size, with pod start, load time, denoise time and bytes transferred written down; it costs under $1. Build the kitchen from primitives and hand-made textures, with no photograph used as a texture, and its passes can go to a pod (a suggestion, not yet tested).

**Free render farm.** SheepIt is free and lists Blender 5.2. It says nothing about confidentiality, so never send family imagery to it [57].

**AI video from photos.** Veo's image-to-video step probably refuses photos with children (UNVERIFIED) [8]. Her childhood photos are the likeliest to be refused. Do not plan AI video from childhood photos until a test says otherwise. Veo's Lite, Fast and Standard prices are $0.05, $0.10 and $0.40 a second at 720p, and $0.08, $0.12 and $0.40 at 1080p, which is the project's render size [55].

### Step 8. Choose and build the slice (brief by Sunday 15 November, animatic by Sunday 6 December)

Choose a 100-second piece of module M1 for the slice (acceptance 90 to 120 seconds; the model's 100-second unit). The story track picks the actual module; this is the production brief for that choice. The module should:

- sit in mid-life, where you already have the most photos (and, if one exists, a HER-PUBLIC line);
- not be a hard chapter, because hard chapters need one-key-three-guards, including the 72-hour double decision, from the story track [7] (`DECISIONS.md` D-04);
- not be the childhood chapter, which has the least material and the strongest pull toward invented content [1];
- not be the most recent decade, which has the most living people and the most rights questions [7].

The slice must include all of the following:

- the kitchen hero shot (class C, on the reusable kitchen set);
- at least 10 class A shots;
- at least 4 class B shots;
- at least 1 class D title or caption;
- one sound line from her world (and one HER-PUBLIC line if it passed one-key-three-guards; the maker-voice fragment is also tested here and decided at G-SLICE with the S1 sheets, `DECISIONS.md` W-35);
- one music cue;
- one still where the photo does not move;
- the transition into the next module's motif.

The remaining ~80 seconds of M1 is built after the gate, as the second learning-curve unit. T2 and the model's row 174 are per 100-second unit and stay as they are.

Build it through the gates G0 to G6 in order, as the agent-pipeline playbook sets out [2].

By Sunday 6 December (G-SLICE-0) you need an animatic: real photos and temporary sound, with the first hours logged. If the animatic does not exist on 6 December, the 20 December gate will fail. Cut one tier now [gates].

### Step 9. Finish the slice to the bar (Sunday 20 December, G-SLICE)

"Finished" means all of the following.

- Final-quality picture.
- A real mix, not temporary sound.
- A grade and captions.
- A master played end to end on venue-class playback: a TV or projector about 3 metres away.
- S1, the stranger screening on the slice (three strangers to her; Decision 8, `DECISIONS.md` W-43); if you decline, the cold self-read (T3).
- The measured hours, h_slice and h_slice_fin.

Log both in `hours.csv` as you go.

- **h_slice** (production side) is the sum of the minutes for the 100-second slice with activity brief_G0, style_G1, review_G2, craft_refine_G3, chapter_G4, dignity_G5, tech_G6, sound and rework. The model predicts **26.5 hours in Base** for shots, chapter pass and sound only.
- **h_slice_fin** is the sum for grade, mix, captions, master and qc. The model predicts **16.5 hours in Base**: 2.7 hours per finished minute for 1.67 minutes (4.5), plus the half of the 24 fixed finishing hours that is pre-built in the slice (12).

Learn and admin are excluded from both. Compare them with the 30-hour one-off allowance instead. G0 and G1 work is priced inside the per-shot minutes (the stage table under 'Who does what' says 'counted in shot minutes'), so brief_G0 and style_G1 belong in h_slice and are already in the prediction; story is the activity priced separately.

Then run the slice acceptance test in the Templates section. Record each result in `reviews/C01/` and in `decisions.csv` [notes].

### Step 10. Make the decision (Sunday 20 December)

Look up your h_slice in the slice table in the Templates section, at your H. Write one row in `decisions.csv`: the runtime before and after, the measured h_slice (and h_slice_fin), H, and the decision in words.

The rules from the gates file are these.

- **Green**: the slice fits your H at the planned runtime. Continue.
- **Amber**: continue only with the levers adopted.
- **Red**: drop to the next shorter scenario.
- **15 to 18 minutes (stretch)**: continue only if H is 20 or more and the table fits your H at G-SLICE; it is not recommended for the premiere cut under only-me (`DECISIONS.md` W-03). There is no 25-minute plan (D-06).
- **12 minutes**: if the table says it does not fit your H, cut to 9 minutes (wrapper plus two modules).

### Step 11. The holidays (20 December to 2 January)

The model counts zero hours for these two weeks. Do not plan production in them. Rest, or do ungated reading if you want to. The holiday capture list (room tone of her kitchen, the object clock in its light, the street, the house sounds; never a recording of her) is the only fieldwork (`DECISIONS.md` W-10). The schedule does not count it [3].

### Step 12. The restart check (Sunday 3 January, G-RESTART)

Reconfirm H, the list of chapters with material in hand, and the cut order. If H has fallen by more than 25 percent, recompute the plan and cut now [gates].

### Step 13. Production (weeks 12 to 16, 3 January to 6 February)

Each chapter moves from brief to approved. The model assumes about 40 percent of production hours can be built before the holidays. The rest falls in these five weeks [J].

- **Sunday 17 January (G-MID)**: at least 45 percent of target runtime approved. For 12 minutes that is 5.4 minutes. Below that, cut the lowest-priority module now (to 9 minutes). A second module is cut only at G-DRAFT, if it is not at draft.
- **Sunday 31 January (G-DRAFT)**: 100 percent of kept runtime at draft or better. At least 60 percent rolling-locked. The finishing chain rehearsed. Any module not drafted becomes a held-still plus card fallback, or is cut.

### Step 14. Picture lock (Saturday 6 February, G-LOCK)

Each chapter locks in order as it passes gates G4 and G5. For the 12-minute plan, rolling locks begin on Sunday 17 January [notes]. Lunar New Year falls on picture-lock day (Saturday 6 February 2027 [94]); if the household observes it, lock on Friday 5 February instead (Decision 16).

On 6 February, every shot is marked `locked=1` in `status.csv`. Record the timeline hash for the whole cut. Create the git tag `picture-lock-2027-02-06`.

**Allowed after lock:** sound editing, score fitted to the locked cut, grade, titles and captions in text, style and position at equal duration, finishing effects, mastering and delivery. An equal-frame-count swap of a photo or clip, such as a better scan or a corrected crop, is also allowed [63].

**Not allowed:** adding, removing or reordering shots. Changing any shot's duration by one frame. Moving a cut point. Changing a sync point for music or voice-over [63].

**How a team of one enforces the lock on itself.**

1. A lock is a file. The timeline hash, frame count and duration of each chapter go in `chapters.csv`.
2. A validator refuses any commit that changes the duration or order of a locked shot. The validator is not yet written.
3. Agents treat locked shots as read-only. They must refuse a change request and point to the unlock rule.
4. **Unlock rule.** Write the reason and the cost in hours (which sound, score and grade passes must be redone). Wait 24 hours. Unlock only for a factual, dignity or rights error. Allow at most two unlocks after 6 February. Each unlock adds a row to `decisions.csv`.
5. Ideas after lock go in `parking-lot.md`, and you read them after the premiere.
6. S2, the stranger screening of the whole locked cut (three to five strangers to her), is held in week 17 (Monday 8 to Sunday 14 February), before sound is final (`DECISIONS.md` W-43; Decision 8). That way a bad finding costs one unlock at most. If you decline, the cold self-read (T3) takes the same slot.

One solo film, *Away*, was reportedly made without a full script or storyboards [10]. Its maker could review a real-time playblast cheaply. We cannot. Our renders are shared with agents, the score is fitted to the cut, and the surprise leaves no time for a second pass.

### Step 15. Finishing (weeks 17 and 18, 7 to 20 February)

- **Saturday 13 February (G-MIX)**: mix v1 and grade v1 for every locked chapter. S2, the strangers screening (`DECISIONS.md` W-43), is held in week 17; if you decline, the cold self-read of the whole film (T3) is done this week. Saturday 13 February is also the latest acceptable picture lock, not an option to pick (W-08). Fix list only. No new picture.
- **Saturday 20 February (G-MASTER)**: the ProRes 422 HQ master and the H.264 access copy are verified. A DCP is made only if the venue's written answer says so (`DECISIONS.md` W-17). Produce ffprobe and loudness reports and checksums. Verify two backups. Play the film on venue-class playback. Loudness: -1 dBTP everywhere; three venue masters (-23, -18 and -16 LUFS) are rendered and one is chosen at the 22 February run (W-19) [notes].

The two finishing weeks hold about 34 usable hours at 20 hours a week. They hold 17 at 10 hours and 51 at 30. That makes finishing a crunch. The mitigations are to rehearse the master chain inside the slice, roll chapter locks, do the mix and grade yourself with the chain rehearsed (`DECISIONS.md` W-50), and get the venue's written answer on the DCP question by 15 November [J].

### Step 16. Buffer and rehearsal (week 19, 21 to 27 February)

The buffer week is for fixing, not for adding. Rehearsals use 8 to 12 hours of it.

- **Monday 22 February (G-REHEARSE)**: the film plays end to end at the venue; the three loudness masters are played against the hall's own room tone and one is chosen (`DECISIONS.md` W-19, W-52). If it fails, use the USB access copy as the fallback [gates].
- **Wednesday 24 February**: room brief.
- **Thursday and Friday**: cold starts.

### Step 17. Keep the schedule honest every week

- Every Sunday, update `hours.csv`, `status.csv` and the burn-down (see Templates).
- Compare approved runtime with the gate targets.
- Recompute the model when H, the material or `mu` changes. The model files are `model.csv` and `schedule.csv` in the fixtures folder.
- Write every kill, cut and unlock in `decisions.csv`.
- Gate dates fall on Sundays and Saturdays, so decisions can be made at the weekend [gates].

## Learn-by-doing exercises

Each exercise has a goal, steps, a time estimate and a description of what "good" looks like. The time estimates are the scribe's judgement [J]. Do them in order.

The first three exercises produce the numbers the schedule needs most. Use only material that is not family material for the first three. Keep any family photos on the PC with cloud level `none`.

### Exercise 1. Find out what your PC can do (about 2 hours)

**Goal.** Know your PC's facts and one real render time. The research note still lists the PC's CPU, RAM, GPU and free disk as unknown, and the FilmCraft estimate on the PC is an estimate only [9].

**Steps.**
1. Using Windows' built-in system information, write down the CPU model and core count, the RAM, the graphics card (and whether it is NVIDIA), the Windows edition and the free space on the drive where the film will live.
2. Make a 240-frame 1080p test clip of a non-personal scene, such as a gradient or a coloured shape. Export it with FilmCraft or Blender, and time the export.
3. Time one Blender Cycles frame of a simple test scene, at 24 samples with denoise [3].
4. Compare your results with the estimate. The research note estimates FilmCraft export at 0.25 to 1.0 CPU-seconds per 1080p frame on four cores without an NVIDIA GPU [9].

**Good looks like.** A one-page facts sheet in the repo, with no personal data. A timed 240-frame export. A Cycles frame time you can compare with the 17.5-second container figure and the 204-second classroom figure.

### Exercise 2. Measure your real hours for seven days (about 10 minutes a day)

**Goal.** Find your real H.

**Steps.**
1. For seven days, log every session in `hours.csv`, using the activity names. Include planning, reading and learning.
2. At the end, add the minutes and divide by 60.
3. Ask yourself what the lowest week you could still give would be.
4. Write two numbers: your average, and the figure you could keep up in nine weeks out of ten.

**Good looks like.** Seven days of rows in `hours.csv`, and the reliable figure written in the repo. That reliable figure is what G-READY needs.

### Exercise 3. Time one shot of each class (about 3 hours)

**Goal.** Learn the real minutes per shot, which the whole plan depends on.

**Steps.**
1. Choose five photos. Keep them on the PC with cloud level `none`. For each one, build a simple photo move. Log the minutes by activity, including crop choices, cut-out decisions, fixes and review. Log cut-out and inpainting decisions separately. A professional estimated a simple parallax move at about 30 minutes, and an elaborate one at about a week. That is hearsay [37].
2. Make one class B designed graphic, such as a simple title card or diagram. Log the minutes.
3. Make one class C hero camera move on a non-personal test set. Log the minutes.
4. Compare your times with the planning numbers. Class A is 2 minutes (Prior), 7 (Base) or 10 (Stress). Class B is 12, 15 or 18. Class C is 60, 120 or 180. Class D is 5, 6 or 8 [2].

**Good looks like.** A table with five class A times, one class B and one class C, all logged in `hours.csv`. You can say whether your photo moves land nearer the Prior or the Base figure.

### Exercise 4. Build and check a 30-second master (about 3 hours)

**Goal.** Learn the master chain before it matters. The slice's acceptance test depends on it [notes].

**Steps.**
1. Take any 30-second test sequence.
2. Export a ProRes 422 HQ master and an H.264 access copy.
3. Check the frame count with ffprobe. Duration in seconds times 24 must equal the frame count exactly.
4. Measure the loudness with `ebur128` and write the number down.
5. Save checksums for both files.
6. Play both files end to end on a TV or projector about 3 metres away.

**Good looks like.** The frame count is exact. Both files play. The checksums are saved. You can state the loudness number and whether it meets the target that the theatrical-delivery track sets.

### Exercise 5. Prove a picture lock (about 1 hour)

**Goal.** Understand why one frame matters. "Changes to shot order, timing, or duration should be treated as an unlock" [63].

**Steps.**
1. Take a 30-second test cut. Record its timeline hash, frame count and duration.
2. Change one shot's duration by one frame. Record the new hash.
3. Note which later work, such as sound, score and grade, would have to be redone.
4. Write one test unlock entry in a scratch copy of `decisions.csv`, not in the real file.

**Good looks like.** The hash changes. You can explain why a one-frame change counts as an unlock, and what it would cost.

### Exercise 6. Inventory the material you already have (about 3 hours)

**Goal.** Know the share of material in hand for each chapter, which the `material_in_hand_pct` column records. The gathering lag is calendar time, not hours [7].

**Steps.**
1. List every photo, video and recording you already hold. Group them by chapter, and refer to people by ID (for example `P-001`), not by name.
2. For each item, note whether it is scanned and labelled. Note whether it is yours to show. Photos taken by others need clearance for public screening [1].
3. Work out the share for each chapter.
4. Note which gaps would need a covert ask later. Do not contact anyone yet; covert collection opens on Sunday 15 November, after the L1 process lock (`DECISIONS.md` D-13, W-10).

**Good looks like.** A percentage per chapter, the top three chapters by material, and a list of gaps with no names in it.

### Exercise 7. Find every leak route (about 2 hours)

**Goal.** Protect the surprise. Notifications, repo names and shared devices are the leak routes [1][2].

**Steps.**
1. List every device, account and app that syncs photos, videos or messages. Include cloud photo libraries, shared family devices and group chats.
2. For each, write down who can see it.
3. Decide for each one: move it, stop the sync, or accept the risk.
4. Check every repo, folder and commit name for anything that would tip her off.

**Good looks like.** A list in which each route is closed or accepted. Repo and folder names are harmless. No personal data sits in any cloud service.

### Exercise 8. Write the strangers' questions now (about 30 minutes)

**Goal.** Fix the stranger-read test before a cut exists to show anyone.

**Steps.**
1. Write the questions: first "If you met her at the reception afterwards, what would you ask her?", then who is she (in three sentences), what did she want, and what did you feel [notes] (`DECISIONS.md` W-43).
2. Write a one-page answer sheet, and keep it in the repo.
3. Show it to no one.

**Good looks like.** The questions are fixed before any cut is shown to anyone. You know what a good answer would sound like.

## Templates and checklists

### T1. Runtime options: hours needed and weekly hours needed

Hours and weekly hours needed for each case, for the four runtimes. The model's usable hours are 144.5 at 10 hours a week, 289 at 20 and 433.5 at 30 (u = 0.85, over 17 weeks) [J].

| Runtime | Hours needed: Prior / Base / Base + levers / Best | Weekly hours needed: Prior / Base / Base + levers / Best |
|---|---|---|
| 12 min (144 shots at 12 per minute) | 141 / 284 / 201 / 116 | **9.8 / 19.6 / 13.9 / 8.1** |
| 25 min (300 shots) | 220 / 456 / 305 / 173 | **15.2 / 31.5 / 21.1 / 11.9** |
| 45 min (540 shots) | 341 / 717 / 462 / 259 | **23.6 / 49.6 / 32.0 / 17.9** |
| 90 min (1,080 shots) | 614 / 1,305 / 816 / 452 | **42.5 / 90.3 / 56.5 / 31.3** |

The headline weekly hours above are the total-hours check only. The largest-film table below and T2 include the post-holiday check, so T2 is the stricter, operative table. The 25-, 45- and 90-minute rows are kept for comparison only (`DECISIONS.md` W-03, D-24), and "Base + levers" includes lever 3, which is off under only-me (W-50): read the four-lever figures (15.5 hours a week for 12 minutes) as the plan.

*Best* is Prior speeds with the structural levers: hero share 5 percent, 8 shots per minute, finishing bought at 0.8 maker-hours per minute, and 50 percent of production built before 20 December. *Base + levers* uses all five levers, lever 3 (bought finishing) included; without it, the four levers give 15.5 hours a week for 12 minutes and 24.4 for 25 minutes.

Largest film, in minutes, that passes the total-hours and post-holiday checks:

| Case | H = 10 | H = 20 | H = 30 | H = 40 |
|---|---|---|---|---|
| Stress | 0 | 3.5 | 6.0 | |
| Base | 2.9 | 9.4 | 15.5 | |
| Base + four levers (no bought finishing) | 4.6 | 18.2 | 29.0 | |
| Base + five levers (lever 3 bought) | 5.5 | 20.7 | 32.7 | |
| Prior | 12.4 | 27.5 | 42.2 | |
| Best | 18.4 | 44.3 | 67.5 | 90.8 |

Verdicts by runtime, from the research note's model. OK means both checks pass. "post" means the total passes but post-holiday production does not. "SHORT" means the total fails. "fin" means the finishing weeks are a crunch. "levers" in this table means all five, lever 3 included.

| Runtime | H = 10 | H = 20 | H = 30 |
|---|---|---|---|
| 12 min | Prior +4 OK, fin; Base −139 SHORT; levers −57 SHORT; Best +28 OK | Prior +148 OK; Base +5 post, fin; levers +88 OK; Best +173 OK | all OK (+293, +150, +232, +317) |
| 25 min | all SHORT (−75, −311, −161, −28) | Prior +69 OK, fin; Base −167 SHORT; levers −16 SHORT; Best +116 OK | Prior +214 OK; Base −22 SHORT, fin; levers +128 OK; Best +261 OK |
| 45 min | all SHORT | Prior −52; Base −428; levers −173 SHORT; Best +30 post, fin | Prior +92 but short after the holidays; Base −284; levers −29 SHORT; Best +175 OK |
| 90 min | all SHORT | all SHORT (Best −163) | all SHORT (−180, −871, −383; Best −18) |

Where the numbers are negative, the plan is short of hours. Positive numbers are spare hours.

Hours in the Base case are small at 10 hours a week because fixed work uses 58 percent of the 144.5 usable hours before a minute is made. That fixed work is 84 hours: learning 30, reuse build 20, rehearsals 10 and fixed finishing 24.

### T2. Slice-to-runtime table

Measure h_slice for the slice as Step 9 defines it (production side). The model predicted 9.9 hours (Prior), 26.5 (Base) and 54 (Stress). This table holds finishing at Base (mu_fin = 1), and its weekly needs include the post-holiday check, so it is the stricter, operative table. Its all-levers column includes lever 3 (bought finishing at 0.8 maker-hours per minute), so while lever 3 is off under only-me (`DECISIONS.md` W-50), read the no-levers column as the conservative bound. The 8-minute tier is replaced by 9 (W-01); the 25-minute row is comparison only. Read across to find your runtime. A recalculation of the model gives 23.9 at h_slice 26 and 19.5 at 20 for 12 minutes (the table shows 24.1 and 19.6); the gap is under 1 percent and is the same small offset the other cells show, so the table is unchanged.

| Runtime | Needed hours a week at h_slice = 10 / 15 / 20 / 26 / 35 / 45 | Largest h_slice that fits, no levers: H = 10 / 20 / 30 | Largest h_slice that fits, all five levers (lever 3 bought): H = 10 / 20 / 30 |
|---|---|---|---|
| 9 min (wrapper plus two modules) | 11.9 / 13.3 / 15.4 / 18.9 / 24.2 / 30.1 | 3 / 28 / 45 | 13 / 63 / 99 |
| 10 min | 12.6 / 14.1 / 16.9 / 20.7 / 26.5 / 33.0 | 2 / 25 / 40 | 11 / 56 / 89 |
| 12 min | 13.7 / 15.9 / 19.6 / 24.1 / 30.8 / 38.2 | none / 21 / 34 | 7 / 47 / 76 |
| 15 min | 15.5 / 19.2 / 23.6 / 28.8 / 36.8 / 45.5 | none / 16 / 27 | 3 / 38 / 61 |
| 18 min | 17.3 / 22.3 / 27.4 / 33.4 / 42.5 / 52.6 | none / 13 / 23 | none / 31 / 52 |
| 25 min | 23.0 / 29.6 / 36.1 / 43.9 / 55.7 / 68.8 | none / 8 / 15 | none / 21 / 37 |

Worked reading: with 20 hours a week, a 26-hour slice fits 12 minutes only with the levers. Without them the limit is 21 hours. With 30 hours a week and a 26-hour slice, 15 minutes fits without levers and 25 does not. At 10 hours a week, 9 minutes fits only if the slice took about 13 hours or less and all five levers are pulled, lever 3 included (10 minutes needs 11 hours), about half the Base prediction. Without levers, 9 minutes needs a slice of about 3 hours. So at 10 hours: 9 minutes if the slice comes in near Prior speed (9.9 hours); otherwise add hours or buy finishing.

Paste h_slice and h_slice_fin into the model's calibration block (rows 173 and 176), copy the suggested mu and mu_fin, and the model recalculates.

### T3. Gates calendar

| Gate | Date | Must be true | If not |
|---|---|---|---|
| G-READY | Sun 15 Nov 2026 | settings card written (the agent-pipeline project settings card; Step 7); spikes S1 to S5 pass or fallbacks named (Step 7); style bible and three style frames approved (G1); H confirmed in writing; the venue's written answer on file (asked by Fri 6 Nov, W-17); `hours.csv` started | one week's grace (to 22 Nov); then drop one tier |
| G-SLICE-0 | Sun 6 Dec 2026 | the slice animatic with real photos and temporary sound; first measured hours logged | no animatic: cut one tier now |
| G-SLICE | Sun 20 Dec 2026 | the slice at final quality including sound mix, grade, captions and a master on venue-class playback at about 3 m; S1 held with three strangers to her (Decision 8, W-43), or the cold self-read passed if the maker declines; h_slice and h_slice_fin measured; material-in-hand share known | compare h_slice with T2; red: next shorter scenario; amber: continue only with levers |
| G-RESTART | Sun 3 Jan 2027 | H and material reconfirmed; chapters with material in hand listed; cut order reconfirmed | if H fell by more than 25 percent, recompute and cut now |
| G-MID | Sun 17 Jan 2027 | at least 45 percent of target runtime at approved or better | 12 minutes: cut the lowest-priority module now (to 9 minutes); a second only at G-DRAFT, if not at draft |
| G-DRAFT | Sun 31 Jan 2027 | 100 percent of kept runtime at draft or better; at least 60 percent rolling-locked; finishing chain rehearsed | replace unfinished modules with a held-still plus card fallback, or cut |
| G-LOCK | Sat 6 Feb 2027 | every shot `locked=1`; timeline hash recorded; git tag `picture-lock-2027-02-06` | unlock rule only (Step 14). Lunar New Year falls on this date; if observed, lock Fri 5 Feb. |
| G-MIX | Sat 13 Feb 2027 | mix v1 and grade v1 on all locked chapters; S2 held in week 17 (Decision 8, W-43); if the maker declines, the cold self-read of the whole film | fix list only; no new picture |
| G-MASTER | Sat 20 Feb 2027 | master and access copy verified; DCP if used; ffprobe and loudness reports; two backups verified; played on venue-class playback | buffer week is for fixing, not adding |
| G-REHEARSE | Mon 22 Feb 2027 | final file plays end to end on venue-class playback | fall back to the USB access copy |

**The cold self-read (the fallback if the maker declines S1 and S2).** You show the cut to no one. Leave it unopened for 48 hours. Then watch it once on venue-class playback at about 3 metres with the sound on. Before taking any notes, answer three questions in writing: who is she, what did she want, and what did you feel. The Fable advisor applies the cinematic-quality rubric to the same version. The W9 slot (the slice) and the W17 slot (the whole film) stay on the calendar, whichever read is used.

### T4. `shots/status.csv`

Header (one row per shot):

```
shot_id,chapter,module,class,route,beat,target_s,actual_s,status,gate,ver,kind,inputs,cloud_max,consent,hard_flag,label_level,reuse_set,seed,maker_est_min,maker_act_min,agent_est_min,agent_act_min,render_s,render_where,rework_n,gens_tried,gens_kept,owner_next,priority,locked,updated,note
```

The most important columns:

| Column | Allowed values |
|---|---|
| `shot_id` | pattern `^LJ-(C\d{2}|W\d)-S\d{3}$`, for example `LJ-C01-S014`; wrapper shots such as `LJ-W1-S001` validate too |
| `class` | `A` photo move, `B` designed graphic, `C` hero shot, `D` title or caption |
| `route` | `A` code scene, `B` photo move, `blender`, `craft` |
| `beat` | one short sentence with no names; use person IDs such as `P-001` |
| `status` | `idea, briefed, style_ok, drafting, draft, in_review, revise, approved, refine, final, locked, cut` |
| `gate` | last gate passed, `G0` to `G6` |
| `ver`, `kind` | for example `v007`; `draft` or `appr` |
| `cloud_max` | `none`, `preview` or `full`. Set by you, never by an agent |
| `consent` | `ok`, `pending` or `na`. `hard_flag` is `0`, `1` or `HOLD` |
| `label_level` | label ladder `L1` to `L4c` [8] |
| `reuse_set` | `kitchen, street, map, clock, titles, ladder, none` |
| `render_where` | `container`, `pc`, `gpu` or `none` |
| `gens_tried`, `gens_kept` | AI generations tried and kept |
| `priority` | `must`, `should` or `nice` |
| `locked` | `0` or `1` |

Example row (a synthetic test row, delete it):

```
LJ-C01-S003,C01,M1,C,blender,"hero camera move through the kitchen set, test",8.0,,drafting,G1,v001,draft,LJ-S-KITCHEN-01,none,na,0,L4a,kitchen,20261122,60,,60,,2150,container,0,,,agent,should,0,2026-11-23,"TEST ROW - delete"
```

Validator rules (a short script, not yet written):
- IDs match the pattern; every `status` and `class` value is on the list.
- `approved`, `final` and `locked` need a `ver`, `kind=appr`, and a gate of `G2` or higher.
- `locked=1` needs `status` of `final` or `locked`. After 6 February 2027 the target duration cannot change.
- No more than three class A shots in a row in a chapter, without a still, B, C, D or voice-only beat (gate G4).
- `cloud_max` is never raised by an agent.
- No non-ASCII or name-like strings in `beat` and `note`.

### T5. `chapters.csv`

Header:

```
chapter,module,title_code,target_s,priority,cut_order,material_in_hand_pct,status,approved_pct_of_runtime,rolling_lock_date,locked,hard_flag,note
```

The fixture has two wrapper rows (W1 cold open, W2 ending; never cut) and four modules, C01 to C04, each about 180 seconds. C01 is the slice module. Cut order 1 is cut first. C04 is needed only for 15 minutes. C01 carries slice_s = 100: the slice is 100 seconds of C01, and h_slice sums over those 100 seconds (Step 8).

### T6. `hours.csv`

Header:

```
date,shot_or_chapter,activity,minutes,who,note
```

Activity names: `gather, scan, story, brief_G0, style_G1, review_G2, craft_refine_G3, chapter_G4, dignity_G5, tech_G6, sound, grade, mix, captions, master, qc, admin, learn, rework`.

### T7. `decisions.csv`

Header:

```
date,gate_id,runtime_before_min,runtime_after_min,trigger,measured_value,hours_per_week_H,decision_text,who
```

The fixture has one blank row for G-SLICE on 2026-12-20, with `who` set to `maker`. Fill in continue, continue with levers, or cut.

### T8. Slice acceptance test (all must pass)

Record each result in `reviews/C01/` and in `decisions.csv`.

- [ ] **Length and frames.** The 100-second slice (accept 90 to 120 seconds). Frame count is exactly duration times 24. ffprobe is clean.
- [ ] **Picture at the bar.** Full-resolution crops of faces and type are clean. No invented faces. Reconstructions are visibly stylised. The template check passes (no more than 60 percent of tweens share one ease). No more than three class A shots in a row. At least one still.
- [ ] **Sound.** A real mix, not temporary sound. Her-world sound, room tone, any music cue and transitions are all present, and there is no recorded voice of a living person except a HER-PUBLIC line if it passed (`DECISIONS.md` D-05). Loudness is measured with `ebur128` at -1 dBTP true peak against the integrated target that theatrical-delivery sets (W-19). A person listened on the venue-class speakers.
- [ ] **Grade.** One look applied through the same chain to every shot. The colour-patch test passes within plus or minus 3 out of 255 on the final encode [2].
- [ ] **Captions.** Inside the reading-speed and length limits in the format track.
- [ ] **Master.** ProRes 422 HQ and H.264 access copy produced. A DCP test file if a DCP is in scope. Played end to end on a TV or projector about 3 metres away.
- [ ] **Strangers read it, or the cold self-read.** S1: three strangers to her and to the family see a redacted copy cold, under the truthful partial pretext (`DECISIONS.md` W-43). The first question is "If you met her at the reception afterwards, what would you ask her?", then who she is (in three sentences), what she wanted and what they felt. If the maker declines, the cold self-read in T3 takes the same slot. Protocol from the cinematic-quality track.
- [ ] **Hours logged.** `h_slice` and `h_slice_fin`, with learn and admin reported against the 30-hour allowance, agent hours, render seconds, rework counts and, if AI clips were used, generations tried and kept.
- [ ] **Surprise safety.** Repo, folder and commit names harmless. No personal data in any cloud service. Cloud levels respected.
- [ ] **Verdict.** Apply T2. Write the decision in `decisions.csv`.

### T9. Picture-lock checklist (Saturday 6 February)

- [ ] Every shot has `locked=1` in `status.csv`.
- [ ] Each chapter's timeline hash, frame count and duration are in `chapters.csv`.
- [ ] Git tag `picture-lock-2027-02-06` is created.
- [ ] The validator runs and no locked shot has changed.
- [ ] Any unlock is in `decisions.csv`, with its hours cost and its 24-hour wait.

### T10. Burn-down, selection and calibration

- **Approved runtime** = sum of `target_s` for shots whose status is approved, refine, final or locked, divided by the total target.
- **Checkpoints**: at least 45 percent approved on 17 January. 100 percent drafted on 31 January.
- **Selection ratio** = `gens_kept` divided by `gens_tried`, for AI clips only. Vendor figures are not our figures. One vendor's FAQ gives about 3 generations per usable shot and a 25 percent keep rate, which are planning claims [47].
- **Calibration `mu`** = sum of `maker_act_min` for finished shots, divided by the sum of `maker_est_min` for the same shots, after the first 20 shots.

The full model is in the research note (Q4 formulas) and in `model.csv`. Re-run it when H, the material or `mu` changes.

### T11. Render budget by runtime (ESTIMATE, from the container measurements)

| Runtime | Total frames | Hero frames | Container CPU-hours, Suzanne / classroom speed | 10-minute Cycles jobs for finals, Suzanne / classroom | ProRes master | Rented 4090 GPU-hours for hero finals at 128 samples (F3) | Cash at $0.34 / $0.89 an hour |
|---|---|---|---|---|---|---|---|
| 12 min | 17,280 | 1,728 | 18 / 153 | 76 / 883 | 7 GB | 2.2 | $0.7 / $1.9 |
| 25 min | 36,000 | 3,600 | 38 / 318 | 158 / 1,839 | 15 GB | 4.5 | $1.5 / $4.0 |
| 45 min | 64,800 | 6,480 | 68 / 572 | 284 / 3,310 | 27 GB | 8.1 | $2.8 / $7.2 |
| 90 min | 129,600 | 12,960 | 136 / 1,145 | 567 / 6,620 | 53 GB | 16.2 | $5.5 / $14.4 |

These assume 4 iterations for non-hero shots, and 4 Workbench drafts plus 1.5 Cycles finals for hero shots. The first CPU-hours figure is at Suzanne speed (17.5 s a frame) and the second at classroom speed (204 s a frame, F3). With a 5 percent hero share, the Suzanne-speed CPU-hours fall to 11, 23, 41 and 83. The GPU columns use F3's RTX 4090 figure at 128 samples (3.0 s a frame at 1080p), not the old 5 s UNVERIFIED assumption; 64 and 256 samples are 1.6 and 5.6 s a frame [82][83][84].

Render hours are not the bottleneck. Your attention and the number of hero shots are [3].

## Decisions you'll need to make

Each decision lists the options and the current lean. The lean is not final. You own every decision here.

### 1. How many hours a week can you reliably give? (needed in writing by 15 November)

- **Options**: the cases above. Roughly 10 hours, 14 to 20 hours, or 30 hours a week.
- **Lean**: none. This is the input that moves the answer most, and we need your number (pending from the maker, `DECISIONS.md` O-01, W-02).
- **Also needed**: which Claude plan you are on (Pro, Max 5x or Max 20x), and a weekly usage-bar reading before and after the slice week (research F4; usage bars under Settings > Usage [88], and `/usage` in Claude Code [90]).

### 2. Runtime (defaulted in `DECISIONS.md` W-01 to W-05)

- **Options**: 9 minutes, 12 minutes (wrapper plus three 3:00 modules), or 15 to 18 minutes as a stretch; 6 minutes is the fallback F-0. 25, 45 and 90 minutes are not production targets.
- **Lean**: 12 minutes if H is 16 or more in writing; 9 minutes if H is under 14, from Sunday 15 November; 12 at 14 to 16 only if hours are added or captions bought. 15 to 18 only if H is 20 or more and the slice fits T2 at G-SLICE, and not recommended under only-me. No 25-minute private cut: the April version is the same locked picture with voices (D-06). Not 45 or 90.
- **Resolved conflict**: the story track's 12-minute floor is retired. 12 is the target when H allows and 9 when it does not (W-02), and the orchestrator has reconciled this with the story track.

### 3. Which levers to adopt (Step 3)

- **Options**: all five, some, or none.
- **Lean**: the four levers that need no purchase (1, 2, 4 and 5) from today; lever 3 (bought finishing) is off for the premiere cut (`DECISIONS.md` W-50, W-51). Without levers, 12 minutes needs 19.6 hours a week in Base. With the four, 15.5; with all five, 13.9.

### 4. Buy or do the mix, grade and composer work yourself? (decided: do it yourself, `DECISIONS.md` W-50)

- **Options**: do it yourself (2.7 maker-hours per minute in Base, plus 24 fixed hours for the master). Buy the mix and grade (0.8 hours per minute). Use a composer or a music library.
- **Lean**: do it yourself for the premiere cut, with the finishing chain rehearsed inside the slice (week 9) and rolling chapter locks from Sunday 17 January; buy captions alone only if time is short, since a transcription vendor sees text and not pictures or a name (`DECISIONS.md` W-50, D-07). No composer under only-me; use a music library, CC0, CC BY or your own sound (W-44). Re-open buying the mix for the April version. Captions are the small part: $25 to $36 bought, or free in DaVinci Resolve or a local tool [77][78][79]. Lever 3 would be the largest finishing lever (2.7 to 0.8 maker-hours per minute, research F1), but under only-me a bought mix is a person brought in.
- **Music rights**: the *Sita* music rights were first asked at about $220,000 and settled at about $50,000 [14]. The music-sound track owns this. Clear rights before the mix, not after.

### 5. DCP or file for the venue

- **Options**: a DCP, the digital package cinemas play. Encoding is CPU-bound, and the research note could not find a CPU speed [61]. At an assumed 4 frames per second, a 12-minute 2K DCP would take about 70 minutes. This is an assumption, UNVERIFIED, and 4K takes three to four times as long. Fixed cost is 8 to 16 hours. The alternative is a file played on venue-class playback, with a USB fallback.
- **Lean**: the venue's written answer decides it (`DECISIONS.md` W-17). The venue is asked by Friday 6 November and its answer is due Sunday 15 November, before G-SLICE; the slice includes a DCP test file only if the venue ingests DCPs, otherwise the 1080p24 H.264 venue file is the master and a DCP is a contingency.

### 6. Hero share and shot rate

- **Options**: 10 percent hero shots at 12 per minute (Prior and Base), or 5 percent at 8 per minute (levers).
- **Lean**: 5 percent and 8 per minute. Settled (`DECISIONS.md` W-34, W-51).

### 7. Reuse program (recurring sets, one world map, the object clock, a title system, a portrait ladder)

- **Options**: the full program (20 build hours, 10 percent saving). In Base it loses about 8.5 hours at 12 minutes, breaks even at 25, and gains 13 at 45 and 42 at 90. A lite program (8 hours, 6 percent) is about neutral at 12 minutes. No program.
- **Lean**: for 12 minutes, build only the title system and one set, the kitchen (8 hours, 6 percent); the kitchen is the only built set (`DECISIONS.md` W-34). Reused sets and motion can read as a template, so use seeded variety and at least one still per chapter [2]. A 2026 study of a shared asset library found about a 12 percent cut in builds. That is snippet-only and counts builds, not hours [69].

### 8. The outside stranger read (W9 for the slice, W17 for the whole film)

The schedule has two reads by strangers to her, now decided (`DECISIONS.md` W-43). You are the only person on the project, and nobody else is in on the surprise. The readers are strangers to her and to the family, on a redacted copy, under the truthful partial pretext: they learn that a short film about one woman exists, never who and never that it is a surprise.

- **Options**: (a) hold S1 (three strangers on the slice, about Sunday 20 December) and S2 (three to five on the locked cut in week 17, with one viewer over 65 and, if possible, one teenager with a guardian); (b) drop the outside slots and use the cold self-read in T3 instead. It is the named fallback, and it brings nobody in.
- **Lean**: (a), strangers to her at S1 and S2. If you decline, the cold self-read (48 hours unopened) takes both slots, with Fable's rubric pass mandatory. Pass: at least 80 percent identify the reconstructions and one person across ages; no unread text; at most 2 tell-marks a minute.

### 9. Who else is in on it, and who approves the hard chapters? (decided: only-me)

Decided on 2026-10-18 (`DECISIONS.md` D-03, D-04): for now only you are on the project, as sole producer, sole keeper of the secret and sole proxy for hard chapters. The charter lets relatives and friends be sources through low-key asks that reveal nothing [1]; nobody else is brought in. The one re-open point is TD-L2c on Sunday 3 January 2027. Exercises 6 and 7 use only what you already hold.

For hard chapters the process is one-key-three-guards: a decision sheet per candidate; Fable's written flag [1]; your two decisions 72 hours apart (review 02 section 0.3's rule, adopted by the story track [6][7]); and default OUT of the public cut on any doubt. Anything HOLD or PRIVATE stays out of the public cut, and the her-turn conversation after the reveal (Saturday 6 March 2027) is how she can put it back [6]. Fable flags and never passes G5.

### 10. Week numbering (decided: the dates are the authority, `DECISIONS.md` D-21)

- **Options**: keep review 02's week list, or adopt Sunday-start weeks with the dates as the authority.
- **Lean**: adopt Sunday-start weeks with the dates as the authority. Review 02's list (12 to 15, 16 to 17, 18 to 19) is off by one. Production is W12 to W16, and finishing is W17 to W18 [6]. Owner: orchestrator.

### 11. Picture-lock date

- **Options**: Saturday 6 February 2027 (G-LOCK). Saturday 13 February (G-MIX) is the latest acceptable lock, not an option to pick; there is no 25-minute plan and so no earlier 30 January lock (`DECISIONS.md` W-08, D-06).
- **Lean**: 6 February, as fixed (Friday 5 February if the household observes Lunar New Year).

### 12. Frame rate

- **Settled**: 24 frames per second, signed on the settings card on Sunday 1 November (`DECISIONS.md` W-14, W-16). The model's frame rate (row 25) and the render budget are computed at 24. Craft-motion, the toolchain recipes and the motion skill carried 25 from their test runs; those are patched by hand after r1, r5 and the colour-patch test are re-run at 24 (W-14), so no other track is a reason to reopen this.

### 13. Chapter count

- **Options**: the wrapper plus three modules of about 3:00 (the recommendation for 12 minutes), or film-story's own 12-minute row of four chapters of 2:15 [7]. The model's seven 100-second units are the learning-curve unit, not a cut option.
- **Lean**: the wrapper plus three 3:00 modules. Decided (`DECISIONS.md` W-04). film-story's 2:15 row is superseded (see Words, item a); the cost model is unchanged either way.

### 14. Shot tracking

- **Options**: a hosted tracker such as Kitsu, or plain text in the repo.
- **Lean**: plain text in the repo, as Step 4 sets out.

### 15. Where to render

- **Options**: the cloud container for drafts; a rented GPU; a free farm.
- **Lean**: the container for drafts of drawn scenes (Route A); photo moves (Route B) go to the container only as `preview` proxies of about 768 px, after the account's model-improvement setting is off and only where the photo set's `cloud` level allows, and full-size renders run on the PC (`DECISIONS.md` W-23, W-24); hero finals on the maker's own PC, or on a rented GPU only for scenes with no family imagery, on Secure Cloud with the maker's recorded OK and never Community Cloud (research F3: hero finals are GPU work by default). Scripts travel to the photos; photos stay home. A scene that uses her photographs as textures counts as family imagery for this rule. Never send family imagery to a free farm [57].

### 16. Observances and holidays

The jurisdiction is unknown. The dated list below was checked on 2026-10-18 against the sources shown (research F5).

| Date | Observance | Weekday | Note | Source |
|---|---|---|---|---|
| Sun 8 Nov 2026 | Diwali, main day (festival 6 to 10 November) | Sunday | | [92] |
| Thu 26 Nov 2026 | US Thanksgiving | Thursday | fourth Thursday of November (computed) | none |
| Fri 4 Dec evening to Sat 12 Dec 2026 | Hanukkah | Friday to Saturday | sunset 4 December to nightfall 12 December | [93] |
| Sun 20 Dec 2026 | Planned G-SLICE | Sunday | five days before Christmas | playbook |
| Fri 25 Dec 2026 | Christmas Day | Friday | computed | none |
| Fri 1 Jan 2027 | New Year's Day | Friday | computed | none |
| Sat 6 Feb 2027 | Lunar (Chinese) New Year, Year of the Goat | Saturday | **same day as picture lock** | [94] |
| Mon 8 Feb to Mon 8 Mar 2027 | Ramadan (Umm al-Qura calendar; local moon sighting can move it by about a day) | Monday to Monday | **the premiere, Saturday 27 February, is about day 20** | [95] |
| Wed 10 Feb 2027 | Ash Wednesday, start of Lent | Wednesday | | [96] |
| Sat 27 Feb 2027 | Premiere | Saturday | | charter |

Two consequences:
- **Picture lock falls on Lunar New Year.** If the household or the audience observes it, lock on Friday 5 February instead. gates.csv says the same at G-LOCK.
- **The premiere falls on about day 20 of Ramadan.** If the audience observes it, an evening screening follows sunset and iftar. Log this as a delta for surprise-ops' run sheet. The research note (G3) gives approximate sunset times for 27 February as an estimate only; use a local prayer-times table.

- **Lean**: tell us which of these apply to you (research G3 is the one-message answer sheet). If one falls in a production week, treat that week as half.

### Kill-or-cut by runtime

| Runtime | Decision | Date | Rule |
|---|---|---|---|
| 90 min | Kill now. | Sun 18 Oct 2026 | Needs 42.5 hours a week at Prior speed, 31.3 even in the best case, and 90 in Base. Killed (`DECISIONS.md` D-24). |
| 45 min | Kill now. | Sun 18 Oct 2026 | Killed by D-24. Treat 45 as a post-premiere project, if at all. |
| 25 min | Kill now. | Sun 18 Oct 2026 | No 25-minute plan: the former private cut is the April version, the same locked picture with voices on (`DECISIONS.md` D-06, W-03). |
| 12 min | Decide at the slice. | 20 Dec 2026; 17 Jan 2027; 31 Jan 2027 | At 20 December, if T2 says it does not fit your H, cut to 9 minutes (wrapper plus two modules). At 17 January, below 5.4 minutes approved: cut the lowest-priority module (to 9 minutes); a second module is cut only at 31 January, if it is not at draft. At 31 January, any unfinished module becomes a fallback chapter. |

All of these dates fall on Sundays or Saturdays.

## Pitfalls

1. **Optimism.** People finish in about 1.6 times their prediction [65]. Plan on the Base case, not the Prior. Confirm with the slice.
2. **The first chapter is the most expensive.** In Base it takes about 2.5 times the steady-state time. The model assumes each doubling of output cuts unit time by about 10 to 25 percent, which is Wright's 80 percent learning curve [66]. Put the learning in the slice, not in the final chapters. Never schedule an unfamiliar technique into the last two production weeks [notes].
3. **Heroes decide the schedule.** In Base, 10 percent of shots take about 59 percent of shot-minutes. Give hero shots a budget in seconds per chapter, use them only on reused sets, and draft them in Workbench first [2].
4. **Material arrives on calendar time, not hours.** Covert access to albums and recordings is the constraint, not scanning speed.
5. **One pair of hands.** Scanning, labelling, consent notes, the lab and review are all you. Batch scanning. Let agents do manifests and checks. There is no second reviewer, so use the two stranger screenings S1 and S2 or, if you decline, the cold self-read (Decision 8), and for hard chapters one-key-three-guards with its 72-hour double decision and default-OUT guard [6][7].
6. **The Craft apps are early alpha.** Frequent releases mean failures cost days [2]. Keep the 10 percent risk reserve in Base. Every step needs a non-Craft fallback. Render to new file names.
7. **The finishing crunch.** Two finishing weeks hold about 34 hours at 20 hours a week. Rehearse the master chain inside the slice, roll chapter locks, do the mix and grade yourself (`DECISIONS.md` W-50), and get the venue's written answer on the DCP question by 15 November.
8. **AI tools vanish.** *Critterz* had about 30 people, a 9 to 12 month plan and under $30 million [43]. OpenAI shut Sora down in 2026, and the film missed its Cannes slot and now targets Q1 2027 [44][45]. Keep every generated clip with its prompt and seed in the manifest. Budget for a keep rate, not a price per clip.
9. **AI speed claims are not planning numbers.** *Air Head* took "a little over a week" for about a minute and a half, with hundreds of generations, a 300:1 ratio assumed by its post lead, and heavy compositing [41][42]. Vendor figures are the vendor's own planning numbers, not measured productions [47]. A how-to table with generic figures names no production [48]. *Catacombs* (242 hours, 3,229 generations) is UNVERIFIED. Do not use it [51].
10. **Survivorship.** *Copán La Leyenda* took about 15 years and was heavily panned [46]. *On This Day... 1776* drew backlash for "repetitive camera movements" and "waxen characters" [50]. "AI-finished" is not a quality tier.
11. **The template look.** Uniform easing, stock transitions, centred titles and the same slow zoom on every photo make any film look like a template [2][37]. Use deliberate seeded variety, asymmetry, and at least one still per chapter.
12. **Music rights can cost more than the animation.** See Decision 4 [14].
13. **Surprise leaks.** Notifications, repo names, shared devices, cloud photo libraries and group chats are the routes [1][2].
14. **Holidays and calendar blindness.** Weeks 10 and 11 are dead, and the jurisdiction is unknown. Check Decision 16.
15. **Feasibility quietly deciding the runtime.** Record every runtime decision in `decisions.csv`, with the story reasons as well as the numbers [7].
16. **The container's limits.** Foreground commands stop after 10 minutes. Loose frames fill the disk [3].
17. **Audio post hearsay.** "One hour per finished minute" and "six hours per linear minute" are forum claims and unverified [68]. iZotope advises doubling your mix-time estimate and adding days of buffer [62].
18. **Hosted render farms.** SheepIt does not state its confidentiality terms [57].
19. **Stranger reads that touch the family.** A stranger read must not be connected to her family (research note, Risk 14).
20. **Templates as shortcuts.** The reuse program saves less time than it sounds, but it buys coherence. Count the build hours before you build [2].

## Best references

1. **Cartoon Brew on *Away*** (https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html). How one person finished a 75-minute feature in about 3.5 years, with a few long takes through one built world. Read it for the design choices that made a solo film possible [10].
2. **Austin Chronicle on *Memoir of a Snail*** (https://www.austinchronicle.com/screens/how-memoir-of-a-snail-came-out-of-its-shell-13286572/). The phases and their timing: three years of script, five months of boards, 16 weeks of preproduction, a 33-week shoot. Read it to see how scheduling works for a stop-motion feature [22].
3. **Blender Studio on *Sprite Fright* and *Spring*** (https://studio.blender.org/blog/a-big-short-film-art-director-andy-goralczyk-on-blenders-most-ambitious-movie-yet). Shot counts and timings for short films made by a small studio team. Read it for real numbers on shot counts [33].
4. **Behind the Lens on *Flee*** (https://mande.net/btl/crafts/direction/flee-jonas-poher-rasmussen?amp=1). The director says he edited the film before animating it, so animators drew only shots that survived [20]. Read it for the rule about locking the edit first.
5. **Google's blog on *Dear Upstairs Neighbors*** (https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/). A Sundance short made with AI, and what it needed: animators, researchers and tools, with "none of our final shots" made in one click [49]. Read it for an honest picture of what AI-assisted work takes.
6. **ECG Productions on picture lock** (https://www.ecgprod.com/what-is-picture-lock-why-does-it-matter). What picture lock means, and why a change after lock causes a domino effect [63]. Read it before you enforce the lock on yourself.
7. **Unity Learn on the vertical slice** (https://learn.unity.com/course/game-development-in-a-nutshell/tutorial/production-and-post-release). The definition of a vertical slice, and why it is the milestone that shows whether production is ready to scale [64]. Read it for the logic of the slice. It is the milestone commercial games use to judge whether pre-production is complete.
8. **PremiumBeat on a Pixar short** (https://www.premiumbeat.com/blog/a-masterclass-in-making-a-pixar-animated-short). Look tests that were "super quick and dirty" and took a few days, so the team agreed the direction early [67]. Read it before you make the style frames.

## Sources

Primary input (not numbered here): `research/production-scale.md`, researcher Sonnet, 2026-10-18. It holds the full source list and the Q1 to Q10 findings. This playbook copies only the sources it cites, with the same numbers.

Project files
- [1] Life Journey Project Charter — `CHARTER.md` — 2026-10-18 — roles, principles, constraints, open decisions.
- [2] Agent-First Production Pipeline playbook — `playbooks/agent-pipeline.md` — 2026-10-18 — shot classes, minutes per shot [J], gates, validators, naming, rhythm.
- [3] Agent-first production pipeline research notes — `research/agent-pipeline.md` — 2026-10-18 — measurements M1 to M21, Q-F2 job limits.
- [4] Animated, documentary and web life-journey research — `research/animated.md` — 2026-10-18 — DepthFlow 12.3 fps at 640 x 480 (around line 614).
- [5] Delivery format playbook — `playbooks/format.md` — 2026-10-18 — 100 to 150 maker-hours for 8 to 12 minutes [J]; 6 to 10 hours per finished minute [J] (both figures superseded by this model, `DECISIONS.md` W-02); pacing guidance.
- [6] Film briefs review — `reviews/02-film-briefs-review.md` — 2026-10-18 — schedule prior, refined brief, week numbering.
- [7] Writing a biographical animated film research notes — `research/film-story.md` — 2026-10-18 — runtime recommendation, scene-grade memory counts, 72-hour double-decision rule.
- [8] AI imagery and motion research notes — `research/ai-imagery.md` — 2026-10-18 — Veo and Kling prices, children's photos, label ladder, RunPod.
- [9] ArtCraft motion and sound research notes — `research/craft-motion.md` — 2026-10-18 — FilmCraft export estimate for the maker's PC.

Benchmarks, indie films and documentaries
- [10] Cartoon Brew, "Yes, One Animator Made the CG Animated Feature *Away* on His Own" — https://www.cartoonbrew.com/feature-film/yes-one-animator-made-the-cg-animated-feature-away-on-his-own-172803.html — 2019-06-06 — 75 min, one person, Aug 2015 to Jan 2019, Maya, 8 to 10 h a day.
- [12] Blender.org, "Making Flow, interview with Gints Zilbalodis" — https://www.blender.org/?p=93732 — undated — 5.5 years, 15 to 20 people, 3 to 5 at a time, Blender and EEVEE.
- [14] Wikipedia, *Sita Sings the Blues* — https://en.wikipedia.org/wiki/Sita_Sings_the_Blues — read 2026-10-18 — 82 min, $290,000, Paley's estimate of 9,360 hours, music rights $220,000 reduced to $50,000.
- [20] Behind the Lens (mande.net), interview with Jonas Poher Rasmussen on *Flee* — https://mande.net/btl/crafts/direction/flee-jonas-poher-rasmussen?amp=1 — undated — 10 to 12 animators, 50 to 60 at peak, edit before animating.
- [22] Austin Chronicle, "How *Memoir of a Snail* Came Out of Its Shell" — https://www.austinchronicle.com/screens/how-memoir-of-a-snail-came-out-of-its-shell-13286572/ — undated (2025) — 3 years scripting, 5 months boards, 16 weeks preproduction, 33-week shoot, seven animators at 5 to 10 s a day, 6 months post.
- [25] *Post* magazine, "Animation: Wallace & Gromit: Vengeance Most Fowl" — https://postmagazine.com/Publications/Post-Magazine/2024/November-December-2024/Animation-I-Wallace-Gromit-Vengeance-Most-Fowl-I.aspx — Nov-Dec 2024 — 4.2 s per animator per week, up to 30 animators, shoot just over a year.
- [26] Annecy Festival, 2014 conference summaries — https://www.annecyfestival.com/about/archives/2014/meetings-2014/2014-conference-summaries/summary:100000301652 — 2014 — Laika: *Coraline* 2 to 7 s per animator per week, *Boxtrolls* 1 to 2 s.
- [28] Animator Island, "How Fast Should You Animate?" — https://www.animatorisland.com/how-fast-should-you-animate/ — undated — hearsay rates: 3D feature 3 to 4 s per week, Disney 14, TV 25 to 30.
- [31] Storybench, StoryCorps animated shorts interview — https://www.storybench.org/?p=13125 — undated — 8 weeks animation, 13 weeks total, 6 to 8 people, 3:15 average.
- [33] Blender Studio blog, "A big short film: Andy Goralczyk on Blender's most ambitious movie yet" — https://studio.blender.org/blog/a-big-short-film-art-director-andy-goralczyk-on-blenders-most-ambitious-movie-yet — 2021 — *Sprite Fright* about 10 min, about a year, about 10 people, about 220 shots; *Spring* 1.5 years, 7 people, about 100 shots.
- [34] Wikipedia, *Spring* (2019 film) — https://en.wikipedia.org/wiki/Spring_(2019_film) — read 2026-10-18 — 8 min; one shot took 2 to 3 weeks to animate.
- [37] Adobe Community, "Animate old photos" (Rick Gerard) — https://community.adobe.com/questions-529/animate-old-photos-28461 — 2020-08-03 — hearsay: about 30 min for a simple parallax move; "easily a week" for a 4 s elaborate shot.
- [40] Raka Creative, "How long does it take to complete a video marketing animation?" — https://rakacreative.com/blog/video-marketing/video-marketing-animation-how-to — undated — agency rule of thumb of 40 to 60 hours per minute (vendor).
- [48] MindStudio, "How to use AI for one-person short film production" — https://www.mindstudio.ai/blog/ai-one-person-short-film-production-workflow — undated — generic estimates, no named production.
- [67] PremiumBeat, "A masterclass in making a Pixar animated short" — https://www.premiumbeat.com/blog/a-masterclass-in-making-a-pixar-animated-short — undated — look tests "super quick and dirty, just with a few days of work".
- [70] VFX Voice, *Memoir of a Snail* — https://vfxvoice.com/?p=13144738 — undated — nine stages, bedroom set up for 16 weeks, shots "only five to 10 seconds long".
- [76] Blender Studio, *Charge* project page — https://studio.blender.org/projects/charge/ — read 2026-10-18 — 3-minute short; site navigation lists the "Blender Kitsu" add-on.

AI-assisted projects
- [41] No Film School, "How good is Sora actually? An interview with the filmmakers behind *Air Head*" — https://nofilmschool.com/sora-ai-filmmaker-interview — 2024 — "a little over a week", 20 s generations with 2 to 3 s used, VFX and grading.
- [42] heise, "Sora's Air Head: plenty of human post-processing" — https://heise.de/-9707198 — 2024 — "assumes a ratio of 300:1"; post steps.
- [43] The Decoder, "OpenAI backs Critterz" — https://the-decoder.com/openai-backs-critterz-to-show-generative-ai-can-deliver-on-the-big-screen/ — 2025-09-08 — about nine months, under $30M, about 30 people.
- [44] Forbes via Yahoo, "Why Critterz is the real test of AI filmmaking" — https://www.yahoo.com/entertainment/movies/articles/why-critterz-real-test-ai-212613673.html — updated 2026-05-26 — Q1 2027 target, Sora discontinued, first-look footage at the Cannes market.
- [45] The Next Web, "Sora shutdown leaves Critterz at the Cannes market without its model" — https://thenextweb.com/news/critterz-misses-cannes-openai-sora-shutdown — 2026-05-22 — Sora app dark 2026-04-26, API scheduled for 2026-09-24, in-festival slot missed.
- [46] Wikipedia, *Copán La Leyenda* — https://en.wikipedia.org/wiki/Cop%C3%A1n_La_Leyenda — read 2026-10-18 — 74 min, 15 years of development, panned.
- [47] invideo, "How many AI video generations do you need per usable shot?" — https://invideo.io/faq/how-many-ai-video-generations-do-you-need-per-usable/ — undated — vendor numbers (3 per usable shot, 25% kept, $315 to $750 per minute).
- [49] Google blog, "Dear Upstairs Neighbors" — https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/ — January 2026 — workflow, "none of our final shots ... one-click".
- [50] The Playlist, "On This Day... 1776 trailer" — https://theplaylist.net/on-this-day-1776-trailer-darren-aronofskys-ai-animated-revolution-series-drops-and-the-backlash-arrives-right-on-schedule-20260130/ — 2026-01-30 — backlash.
- [51] Creative Bloq, "A director generated 3,229 AI shots to make one film" — https://www.creativebloq.com/ai/how-a-filmmaker-turned-a-10-year-old-unmakeable-movie-idea-into-reality-with-ai — undated — **snippet-only** (page returned an unrelated headline); UNVERIFIED.
- [69] arXiv 2604.03315, "StoryBlender" — https://arxiv.org/pdf/2604.03315 — 2026 — **snippet-only**: shared asset library cut model builds by about 12%.

Tools, prices and process
- [54] RunPod pricing — https://www.runpod.io/pricing — "Updated October 8, 2026" — GPU rates and storage.
- [55] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing — "Last updated 2026-10-16 UTC" — Veo 3.1 and image prices.
- [56] Renderjuice RTX 4090 comparison — https://www.renderjuice.com/gpus/compare/rtx-4090-vs-rtx-5050 — "Checked Oct 14, 2026" — estimated 3.5 to 7.5 s per frame on three benchmark scenes (Blender 5.2.0).
- [57] SheepIt Render Farm — https://www.sheepit-renderfarm.com/ — read 2026-10-18 — free distributed Blender farm; no confidentiality statement.
- [58] CGWire Kitsu pricing — https://www.cg-wire.com/pricing — footer 2026 — hosted plan prices.
- [59] GitHub, cgwire/kitsu — https://github.com/cgwire/kitsu — read 2026-10-18 — AGPL-3.0.
- [60] Zou documentation — https://zou.cg-wire.com/ — undated — self-host prerequisites and hardware guidance.
- [61] DCP-o-matic speed page — https://dcpomatic.com/learn-more-speed — undated — Grok GPU benchmarks.
- [62] iZotope, "Tips for mixing short films" — https://www.izotope.com/community/blog/tips-for-mixing-short-films — undated — "double it"; add days.
- [63] ECG Productions, "What is picture lock and why does it matter?" — https://www.ecgprod.com/what-is-picture-lock-why-does-it-matter — undated — definition, effects of change.
- [64] Unity Learn, "Production and post-release" — https://learn.unity.com/course/game-development-in-a-nutshell/tutorial/production-and-post-release — undated — vertical slice definition.
- [65] Wikipedia, "Planning fallacy" — https://en.wikipedia.org/wiki/Planning_fallacy — read 2026-10-18 — thesis study, 33.9 predicted days, 55.5 actual.
- [66] Wikipedia, "Learning curve" — https://en.wikipedia.org/wiki/Learning_curve — read 2026-10-18 — Wright's law, 80 percent curve.
- [68] Indietalk and ZHdK audio-post pages — https://indietalk.com/goto/post?id=348469 and https://medienarchiv.zhdk.ch/files/f693e5ef-5249-491e-8bfa-ae379306539a?lang=en — undated — **snippet-only** (both returned errors): "one hour per finished minute", "six hours per linear minute".

Added in round 2 (cited above)
- [77] Rev pricing — https://www.rev.com/pricing — read 2026-10-18, page undated — human captions "Starting at $1.99/min", "delivered in 12 hours or less", English and Spanish only.
- [78] HappyScribe pricing — https://www.happyscribe.com/pricing — read 2026-10-18; page data dateModified 2026-10-13 — human subtitles "From $2.00/min" (Business $1.90), "Delivery in 4h+"; machine credits "$0.20/min".
- [79] Blackmagic Design, DaVinci Resolve — https://www.blackmagicdesign.com/products/davinciresolve — read 2026-10-18, copyright 2026 — free version with edit, colour, VFX, motion graphics and audio; Studio "$295".
- [82] Blender Open Data, About — https://opendata.blender.org/about/ — read 2026-10-18 — score definition (samples per minute, summed over scenes), snapshot address.
- [83] Blender Open Data daily snapshot — https://opendata.blender.org/snapshots/opendata-latest.zip — Last-Modified Sun, 18 Oct 2026 00:01:21 GMT, 101,626,337 bytes — licence Creative Commons 0 is stated in the archive's own README.txt and LICENSE.txt and on https://opendata.blender.org/download/ (the About page states no licence).
- [84] Blender Benchmark 2.0 files — https://mirrors.ocf.berkeley.edu/blender/release/BlenderBenchmark2.0/ — read 2026-10-18 — scenes classroom, junkshop and monster; script sets samples to 1<<24, 30-second time limit, adaptive sampling off.
- [88] Claude Help Center, "Usage limit best practices" — https://support.claude.com/en/articles/9797557-usage-limit-best-practices — "Updated over 3 weeks ago" — what consumes usage; progress bars under Settings > Usage.
- [90] Claude Code docs, "Manage costs effectively" — https://code.claude.com/docs/en/costs — read 2026-10-18 — about $13 per developer per active day, $150 to $250 per month, below $30 for 90 percent; agent teams about 7x tokens "when teammates run in plan mode"; `/usage` breakdown.
- [92] Wikipedia, Diwali — https://en.wikipedia.org/wiki/Diwali — read 2026-10-18 — 2026 dates 6 to 10 November.
- [93] Wikipedia, Hanukkah — https://en.wikipedia.org/wiki/Hanukkah — read 2026-10-18 — 2026: sunset 4 December to nightfall 12 December.
- [94] Wikipedia, Chinese New Year — https://en.wikipedia.org/wiki/Chinese_New_Year — read 2026-10-18 — 2027: Saturday 6 February, Goat.
- [95] Wikipedia, Ramadan — https://en.wikipedia.org/wiki/Ramadan — read 2026-10-18 — Umm al-Qura table: 2027 from 8 February to 8 March; moon-sighting caveat.
- [96] Wikipedia, Ash Wednesday — https://en.wikipedia.org/wiki/Ash_Wednesday — read 2026-10-18 — 2027: 10 February.

## Changelog

- **2026-10-18, Reconciled with DECISIONS.md (2026-10-18).** Sonnet implementor pass against the decisions register: 9-or-12 rule by H and the 15 Nov deadline (W-01, W-02); 15 to 18 stretch only at G-SLICE (W-03); no 25-minute plan, the April version replaces the private cut (D-06); 25-, 45- and 90-minute tiers killed or comparison-only (D-24); the 8-minute T2 row removed (W-01); lever 3 off, finishing done by the maker (W-50, D-07); frame rate settled at 24 on the Sunday 1 Nov settings card (W-14, W-16); venue and DCP decided by the venue's written answer (W-17); stranger screenings S1 and S2 decided (W-43); only-me and one-key-three-guards replace the deferred "who else is in on it" decision (D-03, D-04); no voice-over, no composer (D-05, D-07); picture lock Sat 6 Feb with no 30 January option (W-08). Superseded values S-02, S-19, S-34, S-35, S-36 and S-37 patched.
- **v3, 2026-10-18 (round 2 review applied by the Haiku scribe).** F3 and G2 render numbers, hero finals as GPU work by default and the family-imagery rule; lever 3 conditional on two quotes, with four-lever figures; the F5 calendar and its two consequences; the 9-minute tier and the G-MID rule; the 100-second slice of M1; the decided module shape and wrapper shot IDs; CC0 and 4K citations. TODO(research) closed in Words, Step 9, T2 and Decisions 13 to 16.
- **v2, 2026-10-18 (round 1 review applied by the Haiku scribe).** Slice calibration now defines h_slice on the production side and h_slice_fin separately, and the model has a mu_fin row wired into the finishing rows. The stranger read is conditional on Decision 8, with the cold self-read as the named substitute. Module shape is now a wrapper plus 3:00 modules, with the 12-minute and 8-minute shape issues left as TODO(research). The 20-hour claim now states its post-holiday failure. Spike list and settings card are copied from the agent-pipeline playbook. The 1080p Veo prices are added. The 72-hour rule is cited to [6][7], with the default-OUT guard. Still open: the TODO(research) items in Words, T2 and Decisions 8 to 13.
- **v1, 2026-10-18.** First draft by the Haiku scribe, from `research/production-scale.md` (Sonnet, 2026-10-18) and `CHARTER.md`. Covers Q1 to Q10 and the recommended runtime. Open items: TODO(research) for the spike list (Step 7), the settings card (G-READY), cash for the mix and grade, the DCP lean, the chapter count, the frame rate, the observances, and the outside stranger read. Decisions 2, 8, 9 and 10 need the orchestrator or the maker. Not yet reviewed against the rubric.
