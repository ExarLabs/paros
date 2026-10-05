---
title: podcast-clip-lab LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast clip-lab skill (hosting, URLs, shared files, audio source). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-clip-lab: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Hosting

- Site: `https://lanternroom.example`, deployed with the site's own deploy script; never from a working copy you did not create.
- Page address: `/episodes/<NN>/<5 random lowercase characters>/`, not linked from anywhere.
- Shared files: `episodes/editor.js?v=3`, `episodes/editor.css?v=3`, `episodes/vendor/sortable.min.js?v=1`.
- Per-file size limit: 25 MB.

## Audio

- Raw audio: the editor's shared cloud folder; download by file ID, check duration against the transcript.
- Low-quality audio: mono, 22050 Hz, 24 kbps.

## Selection

- Use the strongest model available for the selection step; build and deploy with a faster one.
- Export format for the editor: the page's default copy format.

## Scripts

- `scripts/make-words.py`, `scripts/find.py`, `scripts/make-clips.py` in this folder, written at adoption.
