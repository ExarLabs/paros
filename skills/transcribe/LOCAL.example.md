---
title: transcribe LOCAL
date: 2026-10-05
status: active
description: Personal settings for the transcribe skill (language, vocabulary hint, folders, sensitivity rules, optional private backend). Copy to LOCAL.md and fill in your own values.
---

# transcribe: personal settings

> Example values. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below with your own. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself. No secrets here: the API key lives in `GROQ_API_KEY` or `$PAROS_SECRETS_DIR/groq/api_key`.

## Language

- Usual spoken language: `english`.
- Second language that appears in some recordings: `german`. For those, and for anything mixed, use `auto`.

## Vocabulary hint

Passed as `--prompt`. Names and terms the model tends to misspell. Keep it short (the hint is capped at about 224 tokens).

```
Northwind, Kestrel Project, OKR, retro, Jira, Miro, Anya, Tomasz, Ngozi
```

## Folders

| What | Where |
|---|---|
| Temporary audio and video | the system temp folder, or `~/Media/temp-audio/` (outside the vault) |
| Raw transcripts | `<area>/meetings/raw/` for meetings, `Resources/Transcripts/` otherwise |
| Processed notes | `<area>/meetings/` for meetings, next to the related project otherwise |
| File name | `YYYY-MM-DD-<short-topic>.raw.md` and `YYYY-MM-DD-<short-topic>.md` |

## Sensitivity

- Allowed on the external service: my own voice memos, public talks, podcasts, internal team meetings without personal data.
- **Not** allowed on the external service: recordings with health, legal or salary details, anything a client marked confidential. For these use the private backend below, or ask me.

## Private backend (optional)

- None yet. If one exists (for example a self-hosted Whisper on a home server), name it here with how to reach it, and when to prefer it.

## Defaults

- Model: `v3`.
- Subtitles: SRT.
- Delete temporary audio after checking: ask me each time.
