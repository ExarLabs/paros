---
name: language-editor
description: Native-quality editor for any language. Removes calques and AI filler, makes prose active and concise, keeps meaning, names, numbers and markup intact, and follows the person's language rules in LOCAL.md. Use when the person asks to "edit this", "proofread", "make it sound native", "it reads like a translation", or "too much AI tone".
---

# language-editor

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/language-editor/CURRENT.md`;
   - `<vault>/PAROS/skills/language-editor/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/language-editor/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it if present. Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running language-editor v<X> from your vault`;
   - from the reference copy: `Running language-editor v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
