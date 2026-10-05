---
title: podcast-synthesis LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast synthesis skill (folders, template, analytics access). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-synthesis: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Folders

- Subtitle files: `Podcast/Subtitles/`, mapping of file names to episodes in `Podcast/Subtitles/MAPPING.md`.
- Syntheses: `Podcast/Synthesis/Episodes/<NN> - <Guest>.md`; series: `Podcast/Synthesis/Series/`.
- Tracking matrix: `Podcast/Synthesis/plan.md`.
- Patterns file: `Podcast/Synthesis/patterns.md` (session log at the end).

## Analytics

- Through the platform's analytics in the browser profile "Lantern work"; no API key.

## Template and quality

- Template: `Podcast/Synthesis/TEMPLATE.md`; best reference: `Podcast/Synthesis/Episodes/31 - Dana Mercer.md`.
- Quality levels by depth (tunable): under 4 KB "draft", 4 to 10 KB "deep", over 10 KB "reference".
- Series with their own template: "Five Workplaces" (recognized by the series name in the request).
