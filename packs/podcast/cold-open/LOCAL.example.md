---
title: podcast-cold-open LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast cold-open skill (length, hook types, folders, hand-off). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-cold-open: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Cold open

- Target length: 25 to 45 seconds, two to four clips, hard cuts.
- After the cold open: 6 seconds of theme music and the title card, then the host introduction (our limit: 35 seconds).
- Hook types that worked on this channel (from channel intelligence): personal confession first, then myth-busting; striking numbers work only for money topics.
- Standing blocklist: guests' children, health details of third parties, current employers by name.

## Folders and tools

- Rendered audio (outside the vault): `~/Media/lantern-teaser/<NN>/`.
- Editor's sheet: `<episode>/improvements/EDITOR SHEET - <variant> (ACCEPTED).md`.
- Audio previews to the owner: send the mp3 files in the chat.
- Waveform check: `verify_cuts.py` in this folder (write it once; see step 5 of `CURRENT.md`).

## Editor

- Sam Okafor, receives the paste-ready block as a chat message.
- Timeline offset: the editor's timeline starts 4 seconds before the raw file's zero.
