---
title: podcast chapters
date: 2026-10-05
status: active
description: Writes chapter timecodes for a published podcast video from the subtitles of the edited cut, never from the raw recording; ten to twelve chapters or full coverage for list-format episodes, exact times only, the platform's format, and internal hook marks that never reach the published description.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# chapters: timecodes the platform recognizes

Chapters help a viewer jump to what they came for, and on YouTube they also turn the progress bar into named segments. They only work if the format is exactly right and the times match the video that is actually published.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- Every time comes from the subtitles of the **edited** video. Guessing is not allowed.
- Format: `HH:MM:SS - Title`, one per line, no bullets, starting at `00:00:00`. With bullets or without the zero line the platform does not recognize chapters.
- The hook mark (★) is internal. It never appears in the published description.

## Personal settings: LOCAL.md

Show block, the default chapter count, the separator (`-` by default), title length, the language of chapter titles, and whether the show numbers list items. Without `LOCAL.md`: ten to twelve chapters, three to eight words each.

## When to use

- The edited video is uploaded (or the editor sent the final file), and the description is being written.
- "Make the timestamps", "chapters for this episode".

## Steps

1. **Get the subtitles of the edited cut.** From the platform (for example `yt-dlp --skip-download --write-auto-subs --sub-langs <code> --sub-format vtt <url>`, deduplicating rolling captions as `transcribe` describes) or by transcribing the final file. Not the raw recording's transcript: intros and cuts shift every time.
2. Scan for strong claims, changes of subject and the start of stories.
3. Pick **ten to twelve** moments. For episodes over two hours, up to fifteen; the point is selection, not coverage.
4. **Exception: list-format episodes** (N tips, N habits, N steps). The chapter list is the table of contents: cover every item, use the numbering spoken in the video, and let the count follow the list. If the video has no on-screen number cards, the chapter list is the only place the numbering appears; an item without a spoken title gets its name here.
5. Find the **exact** start time for each in the subtitles.
6. Write a short, clickable title, three to eight words.
7. Mark with ★ any moment with strong hook material (confession, myth-busting, a striking number). These are for `cold-open` and short clips, and are removed before publishing.

## Output

```
00:00:00 - Opening and the guest
00:02:15 - ★ Why the first business failed
00:05:30 - The limits of a small market
00:12:45 - ★ "I lost everything": the turning point
```

Plus a clean copy without ★ marks for `description`.

## Pitfalls

- Take every time from the subtitles, never estimate. <!-- rule:R-001 since:2026-07-28 -->
- Use the edited cut's subtitles, never the raw transcript; the two are offset by the intro and every cut. <!-- rule:R-002 since:2026-08-25 -->
- No bullets, one per line, start at `00:00:00`, full `HH:MM:SS` form even in the first minutes; mixing short and full forms confuses long episodes. <!-- rule:R-003 since:2026-08-04 -->
- Remove ★ marks before the chapters go into the description. <!-- rule:R-004 since:2026-07-28 -->
- In list-format episodes cover every item, and let the count follow the list. Low evidence: from one episode (a long list without on-screen cards). <!-- rule:R-005 since:2026-10-02 evidence:low -->
- When the owner corrects a chapter, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-006 since:2026-10-02 -->
