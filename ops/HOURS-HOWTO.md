# Hours log: how to fill in `ops/hours.csv`

This is one of the three files you type into (the other two are the inventory sheet and the editor markers). The film's length is decided by the hours you really have, so **log honestly: the plan is built on what you actually did, not on what you hoped to do.** Your first logged week is read on Sun 1 Nov.

**What counts.** Any minute you spend on the project: learning a tool, a test, scanning, writing notes, emails to labs, watching a day's review pack, fixing something again, planning the venue or the night. What the AI team does does not count; yours does. Round each row to the nearest 5 minutes and write it the same day.

**One row per block of work.** Six columns, no extras:

| Column | Write | Example |
|---|---|---|
| `date` | year-month-day | `2026-10-19` |
| `shot_or_chapter` | `-` until shots exist, later `C01` or `LJ-C01-S014` | `-` |
| `activity` | one word from the list below, exactly as written | `learn` |
| `minutes` | a whole number, no "h" | `90` |
| `who` | `maker` or `agent` (only `maker` rows count towards your hours) | `maker` |
| `note` | a few words, under 80 characters | `PC inventory run` |

**Activity words.** `gather` (borrowing, asking, collecting) · `scan` · `story` (notes, inventory, outline) · `brief_G0` · `style_G1` · `review_G2` (watching a review pack) · `craft_refine_G3` (a touch-up in a Craft app) · `chapter_G4` · `dignity_G5` · `tech_G6` (the G-codes are the gate steps of the pipeline) · `sound` · `grade` · `mix` · `captions` · `master` · `qc` (checking) · `admin` (emails, folders, backups, devices) · `learn` · `rework` (doing something again) · `event` (venue, invitations, the night).

**Three examples** (each is one line in the file):

```
2026-10-19,-,learn,90,maker,read the ops how-to; PC inventory
2026-10-23,-,admin,30,maker,lab email draft
2026-10-25,-,gather,90,maker,OBJ-01 to OBJ-03 photographed
```

**No names in note: IDs and relation tokens only; `who` is `maker` or `agent`, nothing else.** This file lives in a public repository (D-26), so write `[relation]`, `DEV-01`, `OBJ-02` or `C01`, never a person's name, address or phone, and no e-mail address. Keep it short; a long note is usually a sentence about a person.

**Saving.** Keep it a plain CSV (comma-separated). If you use Excel, format the `date` column as Text first so `2026-10-19` stays as typed. Avoid commas inside `note`. Then give the file (or the new rows) to the orchestrator, who commits it.

**Checking it (the team runs this; you can ignore it).**

```
python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19
python3 -I scripts/ops_lint.py
```

The report adds up each week and prints an **indicative** reading of the runtime rule: under about 8 hours a week the 6-minute film would become the plan on Sun 1 Nov and 9 minutes the stretch; 8 to under 14 hours means 9 minutes; 14 to under 16 means 12 minutes only if you add hours or buy captions; 16 or more means 12. It is a guide only: your reliable-hours number, in writing, decides (O-01, W-02). The second command refuses any row that contains an e-mail address, an IP number, a folder path under a user name, a social-media handle (an at-sign followed by a name) or a name from your private deny list.
