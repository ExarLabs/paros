---
title: podcast-chapters LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast chapters skill (count, separator, title style). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-chapters: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Chapters

- Count: 10 to 12; up to 15 over two hours; list episodes: one per item.
- Format: `HH:MM:SS - Title`, hyphen separator, no bullets.
- Titles: 3 to 8 words, sentence case, no guest name.
- List episodes: number items as spoken ("Tip 4: Say no on Mondays").
- Subtitles of the cut: `yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt <url>`.
