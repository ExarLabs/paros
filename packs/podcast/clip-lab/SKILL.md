---
name: podcast-clip-lab
description: Build a private page of sentence clips from an episode so the host can order an intro by ear and export exact timecodes for the editor. Use when the person asks for "the clip lab", "intro clips", or "let me build the intro myself".
---

# podcast-clip-lab

Thin entry (PAROS P04), part of the podcast pack. The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/podcast/clip-lab/CURRENT.md`;
   - `<vault>/PAROS/skills/podcast/clip-lab/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/podcast/clip-lab/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it (the show's brand and settings). If there is no `LOCAL.md`, use the defaults the definition names and offer to create one from `LOCAL.example.md`. Read the `version:` field.
3. Report one line before working:
   - from the vault: `Running podcast-clip-lab v<X> from your vault`;
   - from the reference copy: `Running podcast-clip-lab v<X> from the PAROS reference, not yet adopted`.
4. Follow it. The definition's `## Constitution` always wins over `LOCAL.md` and over any request.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
