---
name: frontmatter-header
description: Add or update the YAML frontmatter header of a markdown file in a PAROS vault (title, date, author, status, content-driven description, id, version). Use when the person says "add a header", "update the header", "frontmatter for this note", "bump the version", or when creating a new vault file that has no header.
---

# frontmatter-header

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/frontmatter-header/CURRENT.md`;
   - `<vault>/PAROS/skills/frontmatter-header/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/frontmatter-header/CURRENT.md`.
2. Read it in full. Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running frontmatter-header v<X> from your vault`;
   - from the reference copy: `Running frontmatter-header v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
