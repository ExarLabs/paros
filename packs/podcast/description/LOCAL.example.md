---
title: podcast-description LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast description skill (footer, hashtags, related-episode format). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-description: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Rules

- No emoji, anywhere.
- Guest line: `The guest: <name>, <role>, <years> years in <field>.`
- Related episodes: `#<NN> - <short title> | <guest>: https://youtu.be/<id>`, two lines, most viewed first.
- Lead the related block with a playlist line: `Continue in order (Full episodes playlist): https://www.youtube.com/watch?v=<most-viewed-related-id>&list=<playlist-id>`.

## Footer (copy word for word, never reword)

```
Every episode and the show notes: https://lanternroom.example

Instagram: https://instagram.example/lanternroom
Audio: https://podcasts.example/lanternrom

If you want more of this:
Membership: https://members.example/lanternroom
Or press the Thanks button under the video.

Produced by: Harbour Sound Studio
Supported by: Northside Print Co., Quay Street Bakery

Contact: hello@lanternroom.example
```

## Hashtags

- Mandatory: `#TheLanternRoom` `#LongFormPodcast`.
- Then 2 to 3 main topics, 3 to 5 specific searchable ones, and the guest's name as one tag. 8 to 11 in total.

## Known quirks

- The audio link's path is `lanternrom`, with one "o" missing. It looks like a typo, but the show was registered that way and the link works. Do not "fix" it.
