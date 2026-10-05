---
name: search
description: Ranked search over the vault from a SQLite FTS5 index (index first). Use whenever something must be found in the vault, before grep or reading files one by one: "where did we write about X", "what do we know about Y", "is there already a note on Z", "which file has", "look it up in the vault". For an exact string or code, grep is the right tool.
---

# search

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/search/CURRENT.md`;
   - `<vault>/PAROS/skills/search/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/kits/search/CURRENT.md`.
2. Read it in full. Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running search v<X> from your vault`;
   - from the reference copy: `Running search v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result (a wrong first hit, a missed file), write a learning packet to the skill's `observations/` folder (P05).
