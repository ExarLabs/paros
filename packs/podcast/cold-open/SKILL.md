---
name: podcast-cold-open
description: Find and produce the cold open of a podcast episode: hook ideas in quick mode, or a cut-ready teaser with verified cut points, re-transcribed clips, audio previews and a paste-ready block for the editor. Use when the person asks for "hook ideas", "the cold open", "the teaser", or "what should open this episode".
---

# podcast-cold-open

Thin entry (PAROS P04), part of the podcast pack. The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/podcast/cold-open/CURRENT.md`;
   - `<vault>/PAROS/skills/podcast/cold-open/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/podcast/cold-open/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it (the show's brand and settings). If there is no `LOCAL.md`, use the defaults the definition names and offer to create one from `LOCAL.example.md`. Read the `version:` field.
3. Report one line before working:
   - from the vault: `Running podcast-cold-open v<X> from your vault`;
   - from the reference copy: `Running podcast-cold-open v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Quick mode stops after the variants and says the result is not cut-ready. The definition's `## Constitution` always wins over `LOCAL.md` and over any request.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
