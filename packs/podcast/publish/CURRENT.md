---
title: podcast publish
date: 2026-10-05
status: active
description: Fills in a podcast episode's upload on the video platform field by field, after a mandatory gate that proves the uploaded file is the edited cut and not the raw recording; never sets visibility or a schedule without the owner's explicit instruction, checks the hidden fields a platform does not enforce, and picks the publishing hour from the audience's daily rhythm rather than the weekday.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# publish: from an unlisted upload to a scheduled episode

The editor uploads the video, usually unlisted. Between that upload and a live episode sit twenty-odd fields, several of them hidden, one of them a legal disclosure the platform does not force you to answer. And before any of that, one question that is easy to skip: is this upload actually the cut?

This skill fills fields. It does not write text: title, description, chapters and thumbnail text come from their own skills.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- Visibility and scheduling are set **only on the owner's explicit instruction**. Otherwise the video stays unlisted or private, and the report ends with "going live is waiting for you". When the owner names a time, set it, then verify it in the content list.
- Every time on the published video (chapters, card positions) comes from the subtitles of the **edited** video, never from the raw recording.
- Every text field comes from its own skill (`title`, `description`, `chapters`, `thumbnail`). This skill fills, it does not write.
- The upload gate (step 0) runs before anything else. If it fails, nothing is filled in.

## Personal settings: LOCAL.md

Show block, the platform and channel, the reference values for every field (playlists, audience setting, tags rule, language, category, comments, end screen template, cards), the publishing day and hour with the data they came from, the post-publish list, and the browser profile to use. Derive the reference values once from your best-performing published episode and validate them on the next one.

## When to use

- The editor has uploaded the episode; title, description, chapters and thumbnail are accepted.
- "Prepare the upload", "fill in the video settings", "schedule it for Thursday 18:00".

## Steps

### 0. Gate: is the upload the edited cut? (mandatory, before anything else)

That a video is uploaded does not mean the final cut is uploaded. A falsifiable identity test against the raw source:

1. **Length:** the uploaded video's duration (for example `yt-dlp --print duration <id>`) against the raw recording's (`ffprobe`). A match within a second or two is suspicious.
2. **Content:** at three to five sample points (start, middle, end, and where a cut was expected), compare the upload's subtitles with the raw transcript.

If length and samples match, the raw recording is up: **publishing is blocked.** Tell the owner and fill in nothing. If the raw source is not available, say that the gate did not run.

### 1. The field checklist, in order

| # | Field | Rule (values in `LOCAL.md`) |
|---|---|---|
| 0 | Upload is the cut | gate passed |
| 1 | Title | from `title` |
| 2 | Description | from `description` |
| 3 | Thumbnail | the image the owner approved; an A/B test may be unavailable while unlisted, check again after publishing |
| 4 | Playlists | the always-on ones from `LOCAL.md`, plus a matching topical list if one exists |
| 5 | Audience | made for kids: no (unless it is) |
| 6 | Tags | per `LOCAL.md`; guest name, topics, show name |
| 7 | Languages | video, title and description language |
| 8 | **Altered or synthetic content disclosure** | answer it explicitly; it sits in the advanced section and is **empty** on a new upload |
| 9 | Paid promotion | per the episode |
| 10 | Category | per `LOCAL.md` |
| 11 | Comments | per `LOCAL.md` |
| 12 | Recording date and place | per `LOCAL.md` |
| 13 | End screen | the show's template; the video element set to a **specific** related episode, not the platform's automatic choice |
| 14 | Card | one card to the most related episode, where the topic peaks in this one |
| 15 | **Subtitles** | a cleaned subtitle file for the cut, uploaded by hand; a separate work step, do not skip it |
| 16 | Visibility and schedule | only on explicit instruction (step 3) |

Report the list with a status per row: set, already correct, or open.

### 2. When to publish

Look at two different signals and do not mix them up:

- **The weekday** often does not matter at channel level. When most views come from the back catalogue through recommendations, daily averages across weekdays sit within a few percent of each other, and launch days give no causal signal: the biggest hits are driven by topic, not day. A weekday may still stay fixed for the core audience's habit.
- **The hour** does matter. The audience-activity heatmap usually shows the same daily rhythm on every day. Schedule two to three hours **before** the daily peak, so the notification wave and the first hours run into the peak.

An external deadline (a conference, a season, an anniversary) overrides both. Record the rule and its data in `LOCAL.md`.

### 3. Set visibility or schedule (only on instruction)

Open the visibility control, choose schedule, set date, time and time zone, save. Then **verify in the content list** that the row shows the scheduled state and the right date.

### 4. After publishing (separate round, on the owner's signal)

From the list in `LOCAL.md`, typically: pinned comment, A/B thumbnail test, the episode list in the vault, a publication log, the audio platforms, the website if it reads from a playlist.

## Output

The field table with statuses, the gate result, and one line: "Live: waiting for you" or "Scheduled for <date time zone>, verified in the content list".

## Pitfalls

- Run the upload gate first; a raw recording once sat "uploaded, waiting to publish" for six weeks with matching length and word-for-word matching samples. <!-- rule:R-001 since:2026-10-02 -->
- Never set visibility on your own; on an explicit instruction, set it and verify it in the content list. A blanket "never" was too rigid and was relaxed to "never on your own". <!-- rule:R-002 since:2026-08-25 -->
- The altered-content disclosure is hidden in the advanced section and empty on new uploads; it is the one required answer the platform does not enforce on save. <!-- rule:R-003 since:2026-08-25 -->
- In browser automation, enter non-ASCII text with an insert-text command (`document.execCommand('insertText', false, text)` after selecting the field), not by simulated typing, which silently drops accented characters. <!-- rule:R-004 since:2026-08-24 -->
- A tag field may not tokenize inserted text until Enter is pressed; check the counter. <!-- rule:R-005 since:2026-08-24 -->
- An end-screen template defaults its video element to the platform's choice; switch it to a specific related episode. <!-- rule:R-006 since:2026-08-24 -->
- A "show more" toggle closes on a second click, and a text dump may read the closed state; confirm advanced fields with a screenshot. <!-- rule:R-007 since:2026-08-24 -->
- Card and chapter times come from the cut's subtitles; card time fields may expect frames (`H:MM:SS:FF`). <!-- rule:R-008 since:2026-08-24 -->
- Optimize the hour, not the weekday, and let an external deadline override both. Based on half a year of one channel's data. <!-- rule:R-009 since:2026-08-25 -->
- Upload cleaned subtitles by hand as a separate step; automatic captions alone were left on an episode. <!-- rule:R-010 since:2026-08-25 -->
- When the owner corrects a field or the procedure, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-011 since:2026-10-02 -->
