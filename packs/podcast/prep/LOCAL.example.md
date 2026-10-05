---
title: podcast-prep LOCAL
date: 2026-10-05
status: active
description: Personal settings for the podcast prep skill (fixed episode data, documents, folders). Copy to LOCAL.md and replace every value with your own show's.
---

# podcast-prep: personal settings

> Example values for a made-up show, *The Lantern Room*. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: keys and tokens live in the environment or your secrets folder (P07).

## Show

Keep this block identical in every podcast skill's `LOCAL.md`.

- Name: The Lantern Room. Host: Robin Vale. Language: English.
- Format: weekly long-form interview, one guest, 60 to 100 minutes, recorded on video.
- Audience, measured (platform analytics, last 12 months, read 2026-09-30): 58 % women, 70 % aged 35 and over, 66 % watch on a phone. Declared audience: people rebuilding a working life after a change.
- Tone: warm, curious, never confrontational. Titles and thumbnails may provoke, never promise what the episode does not hold.
- Platforms: YouTube (main channel), audio through an RSS host to the major podcast apps, short clips on two short-video apps.

## Fixed episode data

| What | Value |
|---|---|
| Recording location | Studio B, 14 Quay Street, Harbourtown |
| Usual length | 90 minutes, plus 20 minutes setup |
| Guest intake form | https://forms.example.com/lantern-intake |
| Shared folder for the guest | https://drive.example.com/folders/lantern-guests |
| What happens to the recording | edited, published on video and audio platforms; short clips only with the guest's yes |

## Documents

- Outputs: invitation and preparation questions, each as `.docx` and `.pdf`.
- Generator: `templates/invitation.docx` and `templates/questions.docx` in this folder, filled by the agent; PDF with `libreoffice --headless --convert-to pdf`.
- Episode folder pattern: `Podcast/Episodes/<NN> - <Guest>/`.
- File names: `invitation.docx`, `invitation.pdf`, `questions.docx`, `questions.pdf`, `prep-note.md`.

## Style

- Address the guest by first name; invitation under 250 words.
- Questions: 10 to 12, grouped as opening, the stake, the turning point, the practical part, the close.
- Always one question that asks for a concrete story from the guest's own life.
