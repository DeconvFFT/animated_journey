# Inventory: column rules, texture quota and AI handling rules

Standalone part of the `life-story-interviewing` skill. Moved from Recipe 2 of `research/story.md` in round 1 (2026-10-18). The CSV header and three illustrative rows are in `inventory-template.csv`.

## Milestone-plus-texture inventory

**Purpose.** One table with two row types: `milestone` (a one-off event) and `texture` (a repeated pattern: routine, saying, smell, car, pet, the kitchen table). The template forces texture by (a) a mandatory `sensory_detail`, (b) a `recurrence` field, and (c) a quota (below). Columns required by the brief are first-class: date, place, people, objects, sensory detail, source, confidence, consent status.

**CSV template:** `inventory-template.csv` in this folder (header row plus three illustrative rows). Copy it into any spreadsheet app; the header line is also inline in `SKILL.md`.

**Column rules**
- `type`: `milestone` or `texture`.
- `date` + `date_precision`: `exact | month | year | range | decade | relative` (relative = "the summer after the move"). Prefer ranges and anchors (age, house, landmark public event) over guessed exact dates; a life-history calendar (years by domains: where lived, work, relationships, children) cross-references and helps dates [67].
- `people`: use names or roles; one cell per name separated by `;`.
- `sensory_detail`: exactly one concrete, specific detail (a smell, sound, texture, taste, light). Mandatory. If none is known the row cannot be marked `dramatise`.
- `recurrence` (texture): `daily | weekly | monthly | seasonal | annual | once`.
- `source`: who/what and where: `S` subject, `R` relative, `D` document, `O` object, `P` photo, `V` found voice (existing audio or video of her: voicemails, answering-machine tapes, home video, clips on relatives' phones; see surprise-runbook.md); add session id and timestamp (`@hh:mm:ss`) or file name. No source, no row.
- `confidence` (informed by genealogical evidence analysis: original vs derivative, primary vs secondary information [79]; and oral-history practice that "errors" are data [64]):
  - **A**: a dated original record (certificate, dated letter, dated photo) and at least one person agrees.
  - **B**: two or more independent people agree, no record.
  - **C**: one first-hand memory.
  - **D**: second-hand, family legend, or conflicting accounts. Keep conflicting versions as separate rows linked in `notes`; do not average them.
- `consent_status`: `asked-ok | asked-ok-with-limits | not-asked (surprise hold) | declined | third-party-needs-check | bottom-drawer (do not use)`.
- `allowed_use`: `hall | private-link | family-only | none`, the widest screening the person has agreed to, in the consent they actually gave. `hall` = the Feb 27 gathering (mostly public), and a later private link when the consent script named it. `private-link` = family only, by private link, not at the gathering. `family-only` = shown only to family in person. `none` = not cleared; do not use. A row whose consent was asked before the Tier 2 script named the use is `none` until it is asked again (inference from charter review C1 and OHA [8]).
- `drawer`: `top | middle | bottom` [34].
- `treatment`: `dramatise | glimpse | mention | hold`.
- `motif_tags`: free tags that build the through-line (objects, places, phrases).
- `who_can_verify`: person, not a source.

**Texture quota (inference)**: for each life stage, at least 6 texture rows from at least 4 categories (morning routine; meals; transport; sound and music; home layout; sayings and jokes; money; pets; clothes; the workplace; the weekly rhythm; the annual ritual), plus at least one texture row per decade for each of: a place, an object, a saying, a smell or sound. Count milestone and texture rows separately; target more texture rows than milestone rows.

**AI handling rules for the inventory (inference, from charter principle 4):** an AI may propose a row only from a transcript line or a document, and must put the quote and timestamp in `source`; it must not invent a sensory detail or a date; unknown cells stay empty; any conflicts become two rows; the human confirms `confidence` and `consent_status`.
