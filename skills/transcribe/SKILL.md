---
name: transcribe
description: Turn a local audio or video file, or a YouTube link, into a checked transcript and a processed note with Groq Whisper. Use when the person asks to "transcribe this", "what does this recording say", "turn this voice memo into a note", "make subtitles", or another skill needs text from speech.
---

# transcribe

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/transcribe/CURRENT.md`;
   - `<vault>/PAROS/skills/transcribe/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/transcribe/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it if present. Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running transcribe v<X> from your vault`;
   - from the reference copy: `Running transcribe v<X> from the PAROS reference, not yet adopted`.
4. Follow it. The client is `transcribe.py` in the same folder. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
