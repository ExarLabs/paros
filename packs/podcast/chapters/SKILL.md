---
name: podcast-chapters
description: Write chapter timecodes for a published podcast video from the subtitles of the edited cut, in the platform format, with internal hook marks. Use when the person asks for "timestamps", "chapters", or "timecodes for the description".
---

# podcast-chapters

Thin entry (PAROS P04), part of the podcast pack. The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/podcast/chapters/CURRENT.md`;
   - `<vault>/PAROS/skills/podcast/chapters/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/podcast/chapters/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it (the show's brand and settings). If there is no `LOCAL.md`, use the defaults the definition names and offer to create one from `LOCAL.example.md`. Read the `version:` field.
3. Report one line before working:
   - from the vault: `Running podcast-chapters v<X> from your vault`;
   - from the reference copy: `Running podcast-chapters v<X> from the PAROS reference, not yet adopted`.
4. Follow it. The definition's `## Constitution` always wins over `LOCAL.md` and over any request.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
