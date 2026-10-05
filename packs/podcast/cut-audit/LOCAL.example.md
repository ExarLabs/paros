---
title: podcast-cut-audit LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast cut-audit skill (editor, folders, priority labels). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-cut-audit: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Editor and hand-off

- Editor: Sam Okafor (freelance), receives briefs as a chat message; the vault file is our copy.
- Priority labels the editor knows: `MUST`, `STRONG`, `MAYBE`.
- The editor's timeline usually starts 4 seconds before the raw file's zero (the clapper); say so in every brief.

## Folders

- Episode folder: `Podcast/Episodes/<NN> - <Guest>/`.
- Saved transcript: `<episode>/transcript/<NN>-raw.srt`.
- Brief: `<episode>/EDITOR_BRIEF.md`.

## Measurement defaults

- Silence detection: `noise=-30dB`, minimum `1.0` s.
- Sample points for the "already cut?" test: 00:01:00, the middle, 5 minutes before the end, plus any planned cut.
