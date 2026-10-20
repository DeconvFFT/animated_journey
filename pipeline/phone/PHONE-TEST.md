# Phone test: can you read it? (D-27)

*For the maker, written in plain words. About 15 minutes with one phone. The test file is synthetic: a card with numbers, lines and a few test words, a tone ladder for sound, and four caption cues. There is nobody in it and nothing personal, so for this file any route to the phone is fine (a cable, a local transfer, a chat attachment). For the real film it is different: cable or a private link only, never a service that keeps a copy without your say (D-15, D-02).*

## What you need

- The test file `phone.mp4` (about 1 MB) from the container's test run. The orchestrator hands it over in the chat. If you want to see the "after sharing" version too, ask for `shared.mp4` (the same file squeezed the way a messenger squeezes it).
- Your own phone, or the project phone. Do not use her phone (D-02).
- Your reading glasses if you normally use them for the phone.
- This page. You answer in the chat; the orchestrator records your answers in `ops/decisions.csv`.

## What is on the card

- Top left: a big title in Latin letters. Next to it: a headline in Devanagari (a neutral test word; see the note on question 5).
- A thin moving bar under them, so you can tell the picture is playing.
- On the left: a ladder of lines, 1, 2, 3, 4 and 6 pixels thick (flat lines and upright lines), and a dot.
- Three colour squares: red, mid grey and a skin tone.
- Numbers down both edges, every 5% of the picture height, with 12 and 88 in amber. When your phone zooms to fill the screen, the first number you can still see at the top and at the bottom tells you how much the player cut off.
- In the lower part: four caption cues made of neutral test words, two lines each, in white with a thin black outline. They are the part that matters.
- The sound: six steady tones (low to high), then a hiss. Nothing else.

## How to look

1. Copy the file to the phone and open it from the gallery or the files app (not from inside a chat).
2. Set the volume to about half.
3. Hold the phone as you normally hold it for reading a message: about 35 cm (a forearm) from your eyes. Then once at arm's length, about 50 cm.
4. Look at it **sideways** first (the way the file is made to be seen), then **upright**, then **sideways with the player set to fill or zoom** (most players have a button, or a pinch, that fills the screen; on a long 20:9 phone this cuts about a tenth off the top and the bottom).

## The seven questions

Answer yes or no, and add a few words if something was hard. "I could not tell" is a fine answer.

| # | Question | Yes / No | Notes |
|---|---|---|---|
| 1 | One tap, and it plays at once, with no error message and no waiting? | | |
| 2 | Sideways, at your normal reading distance (35 cm): can you read every caption line without squinting? | | which line, if any, was hard? |
| 3 | Sideways, at arm's length (50 cm, the way a 50-year-old viewer may hold it): can you still read every caption line? | | |
| 4 | Upright: can you read the captions? (We expect this to be hard; the plan is to say "turn it sideways". Tell us how hard: easy, hard, or not at all.) | | |
| 5 | Are the thin lines visible (which is the thinnest one you can see?), and do the small marks on the Devanagari words look crisp: the dot above a letter, the sign below, the little hook before a letter, the joined letters? | | see the note below |
| 6 | Do the three colour squares look right (clean red, plain grey, a believable skin tone), and could you hear the tones at half volume (say which: low, middle, high)? | | |
| 7 | When you zoom to fill, is the bottom caption line still whole (no letters cut off at the bottom)? Write the first number you can still see at the top and at the bottom of the percentage ruler. | | |

**Note on question 5.** The Devanagari words are neutral, plain nouns of Sanskrit origin, proposed by the planner and **not yet read by anyone who reads the script** (`checked_by_reader` is false in `pipeline/phone/test_strings.json`). If you read Devanagari, say whether the words look right (joined letters formed, vowel signs on the correct side of the letter). If you do not read it, say so; then answer only whether the marks look crisp and whole, not whether the words are right. Her own language is Gujarati (D-31): its shaping and caption test is a separate item that must pass before the settings card is signed, and it is **NOT TESTED** here.

## What the numbers predicted (so you know what to expect)

These are measured on a computer from the file, not by a person, and they assume a typical phone (every viewport figure and the arcminute limits are UNVERIFIED):

- Sideways at 35 cm, the caption letters were predicted to be at or above the target (see `PHONE-ROW.md` for the figures).
- Upright, the captions were predicted to fall **below** the floor; that is the reason the hand-over says "turn it sideways".
- When a 20:9 phone fills the screen, the bottom caption line was predicted to stay whole; the venue-sized caption does not (it is the same file with the venue's size and margin, and it is not part of this test).
- At 50 cm the sideways letters are predicted to fall slightly under the floor. Your answer to question 3 is the real measurement.

## What happens with your answers

| If you answered | What it changes |
|---|---|
| 2 or 3: no | The phone caption size goes up one step (the candidate table in `build/evidence/wp08/caption_candidates.json` shows what each step costs in block height). Re-run `phone_check.py --candidates`, then re-encode. |
| 4: not at all | Nothing changes in the file: upright is degraded by design; the hand-over text says "turn it sideways". |
| 5: a thin line that the plan relies on is gone | The 4 px floor for meaning-bearing lines stays; any line thinner than 3 px is redrawn or dropped in the shot brief (W-38). |
| 7: no | The caption block moves up (a larger `MarginV` in `profile.json`), and if the first visible number shows your player crops more than 10% the fill_20x9 bottom limit is lowered to match; the fill_20x9 check is then re-run. |
| 1: no | The file is re-made with a different profile (for example the 720p copy PH2) and the player is noted. |

## For the real film

PH1 or PH2 goes to her phone by cable (or a private link), with her yes, after the reveal (D-02, D-15, W-63). Relatives get a copy only after the ledger closes (W-48), with your yes. Nothing is sent before the reveal.
