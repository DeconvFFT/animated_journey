# Surprise-mode runbook

Standalone part of the `life-story-interviewing` skill. Moved from Recipe 4 of `research/story.md` in round 1 (2026-10-18), with the found-voice and people-tab sections added. The relative script is also inline in `SKILL.md`. The charter fixes surprise mode (CHARTER.md, Known facts, 2026-10-18). Evidence: `research/story.md`, Q3 and Q4.

## Gates

| Gate | Actions |
|---|---|
| 0 Suitability | Write a one-page "points for and against" (the "feeza") [28]. Under only-me there is no insider (`DECISIONS.md` D-03, S-08): answer from your own knowledge (O-11): would she love it or hate it? Has she ever said she hates surprises, speeches, being photographed? Record yes/no/unsure. If "hate", stop, switch to collaborative, or use the two-step reveal (private first, then the room) [30]. |
| 1 Circle | Keep the circle as small as the work allows. Neutral project name; one shared folder; no group chats; no notes with the project name on paper the subject might find [28][29]. Two tiers, decided per person (playbook Step 8, Decision 2). **Tier 1** (the default; not brought in): ordinary family asks only, no briefing about the project, unrecorded; stories are written up afterwards as `R` rows with `not-asked (surprise hold)`. **Tier 2** (brought in): only by a written maker decision, reviewed by the advisor like a gate pull; the honest script; recorded; a dated `told_on` line and a `scripted_line_if_asked` in the people tab. The spouse is not briefed unless the maker decides so in writing: a current partner is the strongest leak path (`research/surprise-ops.md`, internal cross-reference; not re-fetched). Brief young children only if essential, and then as Tier 2. |
| 2 Sources | Tier 1 asks until a Tier 2 decision is written (Gate 1). Recorded relative interviews (R banks) are Tier 2 only; documents; objects; photos; **found voice**: her existing voicemails, answering-machine tapes, home video and clips on relatives' phones. In surprise mode this is the only route to her own voice, so it is a source class of its own (see the found-voice section below). Track who knows. |
| 3 Hard material | Bottom-drawer material is not solicited, not used [34]. Named third parties are checked with the right person. Any relative with a difficult history with the subject: under only-me nobody is asked; decide from your own knowledge and Fable's written flag before approaching, and default to not approaching (D-03, D-04; cf. the reported Mullard case) [30]. |
| 4 Facts | Inventory with confidence. Triangulate. Prepare a list of ten items only the subject can confirm. |
| 5 Reveal | Under only-me the first viewing before the room is the maker's own cold read (48 hours unopened, Fable's flags read first; D-03, S-08); relatives first see it at the premiere and answer in the April version (D-06). Reveal to the subject in a setting where they can say "stop". Give a veto window: nothing is shared beyond the room until they say so; they can ask for cuts [8][32] (inference). |
| 6 Contingency | If it leaks, tell the subject and convert to collaborative. If they refuse, stop [30]. |

Script for Tier 2 relatives (honest, no false pretext). **Void before the premiere under only-me (D-03, S-10): nobody is read this before Sat 27 Feb; it fires only if TD-L2c (Sun 3 Jan) brings someone in, and otherwise it is the April-version ask after release 4d.** "I'm making a piece about [NAME]'s life as a gift. It is a secret from [NAME] until [date]. It will be shown at a gathering on Feb 27 that is mostly public, and may be shared with family afterwards by private link; you can restrict any part. I'd love 45 minutes of your memories; you can skip anything, and nothing you say will be used without your OK. Please don't mention it to [NAME] or anyone who might." Found-voice ask, in the same conversation: "Do you have any video or voice message of her on your phone? Please don't delete anything. Please don't forward it to me or post it; just tell me what you have and roughly when it was made." Avoid inventing a cover story that requires the subject to do something on camera: the Blanchflower approach used a false pretext and it failed live [30].

## Found voice (a source class of its own)

Found voice is existing audio or video of her: voicemails, answering-machine tapes, home video, and clips on relatives' phones. In surprise mode it is the only route to her own voice (Fable round-1 review, nudge 7). Locate it now, and copy each item as soon as the relative agrees, by cable or direct transfer, never through a chat app, because phones get replaced and tapes wear out. Do not collect by forwarding files through chat apps: forwarding can recompress the file and may leave a trail she could notice.

Where her voice may be, and whom to ask (research Q4 checklist):

| Where her voice may be | Ask whom | Risk if not copied now |
|---|---|---|
| Phone videos and voice notes on relatives' phones (birthdays, holidays, toasts, video calls) | Siblings, children, cousins, close friends | Phone replaced or storage cleared |
| Saved voicemails on relatives' phones | Anyone who keeps them (often a parent or sibling) | Carrier retention rules: UNVERIFIED |
| Chat voice messages (WhatsApp, iMessage, others) | Same | Disappearing messages, app changes |
| Answering-machine tapes and microcassettes | Parents' or older relatives' homes | Tape wear; no player |
| Camcorder tapes (VHS, VHS-C, Hi8, MiniDV) and film | Whoever filmed family events | Tape ages; need a working player |
| Audio letters, cassettes sent between family | Older relatives | Same |
| Work, school, church, club or community recordings; local radio or TV | Her friends and institutions | Archives purge |
| Wedding video | The couple's families | Tape ages |

Item fields for each item found (record them as `source` V rows in the inventory): who holds it; device or format; rough date; who speaks; length; quality (clear, muffled, noisy); original in hand (yes or no); copied (yes or no, how many copies); consent status of everyone heard.

Handling: never edit the original. Keep at least two copies stored apart, and check them yearly; the Library of Congress advises refreshing media about every five years [38][88]. Found voice may be restored and used as itself. It may not be extended or imitated: no synthetic voice of any real person (playbook Decision 10). The Library of Congress pages do not cover cassette, answering-machine, voicemail or camcorder-tape transfer; a how-to is TODO(research).

**File plan (written 2026-10-18).** Keep two copies of every item on two encrypted drives, kept in different places. Never edit an original; work only on copies. Keep one manifest line per item: item id, file name, holder, device or format, rough date, who speaks, source, checksum (for example SHA-256; inference), and where each copy is. Copy each item as soon as the relative agrees, by cable or direct transfer, never through a chat app. Copying an existing file does not record anyone and does not touch the gate; asked as an ordinary family request, it is a Tier 1 ask. The storage rule is the one suggested in `reviews/00-charter-review.md` (item 5); the maker has not yet confirmed it. The manifest is also the catalogue the story work needs.

## People tab and door triage (research Q3)

Keep a people tab with one row per relative: name; relationship to the mother; approximate age; health and hearing notes (only what the maker already knows); where they live and when next seen in person; language; whether they are in on it; tier (1 or 2); `told_on` (the date; Tier 2 only); `scripted_line_if_asked` (the one line for if they are asked); likely sensitive topics; door (A or B). Health notes about relatives are private to the maker and do not go into any shared file.

**Door A (protect now)** if any one of these holds (inference; the thresholds are judgement calls, change them if the facts differ):
- aged 75 or older;
- a serious or progressive illness, or any memory change;
- a hearing or speech problem that makes a later phone call impractical;
- reachable in person only at one gathering before mid-November, or only abroad.

**Door B (wait for the gate):** everyone else.

Door A relatives are reached before the premiere only through album-and-hands sessions under a true sentence (`DECISIONS.md` W-49: hands and pages filmed, the face never in frame, a spoken "fine" on the file; the voice held as Tier C for release 4d). A recorded Door A session with the relative script and the consent card (which names the premiere use) is Tier 2, which is itself a bringing-in decision and waits for TD-L2c (Sun 3 Jan; D-03, S-10). If TD-L2c brings someone in, a Door A recording is a one-take rescue, not a polished interview: the voice may not make the final cut, but the memory exists.

For a hard-of-hearing relative the interviewer carries the load: face the person, speak up and slow down, pick a quiet place away from kitchens and music, and plan shorter sessions with printed question cards (NIDCD conversation tips [87]; the cards are inference).
