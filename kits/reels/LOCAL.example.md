---
title: reels LOCAL
date: 2026-10-05
status: active
description: Personal settings for the reels kit (brand theme as a json block read by reel.py, folders, language, hashtags, publishing platforms). Copy to LOCAL.md in your vault and replace every value.
---

# reels: personal settings

> Example values, all fictional. Copy to `LOCAL.md` where your vault keeps the kit and run `reel.py --theme LOCAL.md ...`. The script reads only the `json` block below; the rest is for the agent.

## Brand

- Show: "Kitchen Table Talks", a fictional weekly conversation podcast.
- Tone: warm, calm, no shouting colours. A deep green with a cream text colour.
- Language of the episodes and captions: English. Recognition fallback: `--lang English`.

## Theme (read by reel.py)

```json
{
  "subtitle_style": "Fontname=Arial,Fontsize=18,Bold=1,PrimaryColour=&H00E9F1F5,OutlineColour=&H00203A1E,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=62",
  "max_words_per_fragment": 3,
  "title": {
    "font_candidates": [
      "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
      "C:/Windows/Fonts/arialbd.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ],
    "font_size": 80,
    "bg_rgba": [30, 58, 32, 230],
    "text_rgb": [245, 241, 233],
    "top_frac": 0.07,
    "duration": 3.5
  },
  "fps": 30,
  "outro": "~/Media/kitchen-table/outro-1080x1920-30fps.mp4",
  "music_volume": 0.12,
  "hashtags": "#kitchentabletalks #podcast"
}
```

Colours in `subtitle_style` are `&HAABBGGRR` (alpha, blue, green, red), not RGB.

## Folders

| What | Where |
|---|---|
| Scratch (sources, intermediates) | `~/reels-scratch/` (`PAROS_REEL_SCRATCH`), outside the synced vault |
| Full episode transcripts | `Podcast/Episodes/<NN> <title>/transcript.srt` |
| Deliverables | `Podcast/Episodes/<NN> <title>/Clips/<slug>/` |
| Slug | `ep<NN>-<topic>-<seq>`, for example `ep12-sourdough-01` |

## Publishing

- Platforms: two vertical-video feeds and one video platform's shorts section.
- The owner publishes; the agent fills `PUBLISH.md` and logs nothing as published until told.
- Source video: ask before deleting once all clips of an episode are done.
