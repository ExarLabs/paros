---
name: podcast-title
description: Write five podcast video titles in the show format, paired with the chosen thumbnail text, under 75 characters with the essence in the first 60, ranked by measured patterns. Use when the person asks for "title ideas", "is this title good", or "rank these titles".
---

# podcast-title

Thin entry (PAROS P04), part of the podcast pack. The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/podcast/title/CURRENT.md`;
   - `<vault>/PAROS/skills/podcast/title/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/podcast/title/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it (the show's brand and settings). If there is no `LOCAL.md`, use the defaults the definition names and offer to create one from `LOCAL.example.md`. Read the `version:` field.
3. Report one line before working:
   - from the vault: `Running podcast-title v<X> from your vault`;
   - from the reference copy: `Running podcast-title v<X> from the PAROS reference, not yet adopted`.
4. Follow it. If no thumbnail text is chosen yet, suggest running podcast-thumbnail first. The definition's `## Constitution` always wins over `LOCAL.md` and over any request.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
