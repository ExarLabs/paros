---
name: podcast-publish
description: Fill in a podcast upload on the video platform after a gate that proves the upload is the edited cut; field checklist, hidden disclosures, publishing hour; visibility only on explicit instruction. Use when the person asks to "prepare the upload", "fill in the video settings", or "schedule the episode".
---

# podcast-publish

Thin entry (PAROS P04), part of the podcast pack. The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/podcast/publish/CURRENT.md`;
   - `<vault>/PAROS/skills/podcast/publish/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/podcast/publish/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it (the show's brand and settings). If there is no `LOCAL.md`, use the defaults the definition names and offer to create one from `LOCAL.example.md`. Read the `version:` field.
3. Report one line before working:
   - from the vault: `Running podcast-publish v<X> from your vault`;
   - from the reference copy: `Running podcast-publish v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Never set visibility or a schedule unless the person said so in this conversation. The definition's `## Constitution` always wins over `LOCAL.md` and over any request.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
