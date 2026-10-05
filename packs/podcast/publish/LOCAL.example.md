---
title: podcast-publish LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast publish skill (field reference values, publishing hour, post-publish list). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-publish: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Reference values (derived from episode #31, validated on #32)

| Field | Value |
|---|---|
| Playlists | always `Full episodes` and `The Lantern Room`; plus one topical list if it fits (`Work and burnout`, `Second careers`) |
| Audience | not made for kids |
| Tags | 10 to 12, about 200 of 500 characters; guest name, topics, `the lantern room`, `long form podcast` |
| Languages | English (video, title, description) |
| Altered content | No |
| Category | People & Blogs |
| Comments | on, basic moderation, sorted by top |
| Recording date and place | left empty |
| End screen | template "1 video, 1 subscribe", video element set to a specific related episode |
| Card | one, to the most related episode, where the topic peaks |
| Subtitles | cleaned English subtitle file of the cut, uploaded by hand |

## When to publish

- Thursday, 18:00 local time (UTC+1). The weekday is habit; the hour comes from the audience-activity heatmap (peak 20:00 to 23:00 every day), read 2026-09-30 over six months.
- An external date (a book launch, a conference) overrides this.

## After publishing

1. Pinned comment with the guest's link.
2. A/B thumbnail test once eligible.
3. `Podcast/EPISODES.md`: new row.
4. Publication log: `Podcast/publication-log.md`.
5. Audio upload to the RSS host.

## Browser

- Use the browser profile "Lantern work"; ask if several are connected.
