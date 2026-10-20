# Proposed skill: `phone-delivery` (WP-08, staged for the orchestrator)

**Status (2026-10-20, stale-wording sweep): NOT installed, and NOT folded.** The phone decisions and figures live in `mobile-phone-delivery` (staged copy `skills-staging/mobile-phone-delivery/SKILL.md`, already at 32 characters a line and a 3.5 Mb/s cap on PH2); install that one for them. This folder is only the tools companion (the `encode_phone`, `phone_check` and `sim_share` commands, thresholds and failure answers, which exist nowhere else), waiting for the orchestrator to either install it beside `mobile-phone-delivery` or fold its Procedure, Thresholds and failure sections into it. Do not install it in place of `mobile-phone-delivery`. The row below that records "36" is closed: the register's W-18 was amended on 2026-10-20 to at most 32 characters (W-63 to a 3.5 Mb/s cap), which is the figure this skill already uses.

Nothing under `.claude/` was edited. This folder proposes a new skill and says where it overlaps an installed one.

## What it is

A new skill, `phone-delivery`: the commands, thresholds and failure answers for the three WP-08 tools (`encode_phone`, `phone_check`, `sim_share`). The installed `mobile-phone-delivery` holds the decisions (PH1 and PH2, the project-phone protocol, sharing and keepsake rules) and has no tool commands, no measured thresholds, no fill-crop check and no per-script rule, because the tools did not exist when it was written.

## Why a second skill and not an edit

The two answer different questions ("what do we promise, and to whom" against "which command proves it"). Either install `phone-delivery` beside `mobile-phone-delivery`, or fold its Procedure, Thresholds and "What to say when a check fails" sections into `mobile-phone-delivery` as a "Tools" section and drop this folder. The orchestrator decides; both are one-file changes.

## Lines in `mobile-phone-delivery` (and `playbooks/mobile-delivery.md`) that this work measured differently or left open

| Where | Says | Measured or proposed here | Why it matters |
|---|---|---|---|
| Procedure step 5; Quality bar | "at most 36 characters a line" | `max_chars_per_line` 32 in `profile.json` (the build plan's figure) | 32 is stricter and inside W-18's 36. The register wins, so the orchestrator must pick one; the PHONE-ROW says 32 and names the difference. |
| Procedure step 5 | "Outline 2" | the profile uses Outline 2 (7.5 px at 1080p on the 384x288 canvas) | agrees; stated so nobody re-derives it. |
| Frame checks | "Caption zone: phone 68% to 86%" | block measured at about 69% to 84% with FontSize 28, MarginV 40, two lines (Noto Sans) | inside the zone; the bottom limit is gated at 88% in `fill_20x9`. |
| Quality bar | "Must-read type x-height 3.2% (hard floor) and 3.8% (target)" | Latin x-height at FontSize 28 in Noto Sans is about 3.4% (above the floor, below the target); at 35 cm sideways it reads about 22 arcmin, at 40 cm about 19, at 50 cm about 15 | FontSize 28 meets the floor and the 35 cm target but not the 3.8% target; the maker's phone test decides whether a step up (30) is wanted. |
| Procedure step 5 | "FontSize 28 ... Latin" | FontSize means a different x-height in a different face: the research fixtures used Liberation Sans (3.81% at 23); this run uses Noto Sans from `libs.lock.json` (about 2.8% at 23) | the venue FontSize 23 is below the 3.2% floor in Noto Sans; recorded as a finding in `finding_fontsize23.json`, not asserted. |
| Exercise 4 | read both captions "at 50 cm in fit and fill" | the sideways-fit letters fall under the 18 arcmin floor at 50 cm (about 15); fill keeps them above | the phone test question 3 asks exactly this. |
| Exercise 7 / W-75 | the `ass` filter chosen "by a test" | measured on ffmpeg 6.1.1: `ass` reaches IoU 0.9 for Latin and Devanagari, the `subtitles` filter does not for Devanagari (it matches forced simple shaping) | confirms the single burn-in path; the PC build is still UNVERIFIED. |

## What is not changed

The decisions (D-27, D-28, W-17 to W-19, W-21, W-57, W-63, W-75), the Hindu-only rule, the privacy rules and the review gates are untouched; the skill repeats them where a command depends on them. No new decision is proposed. The `mobile-phone-delivery` description and triggers stay as they are; the new skill's description ends by pointing to it.
