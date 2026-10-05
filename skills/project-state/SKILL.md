---
name: project-state
description: Create, update or read the short versioned state file of an area or long-running project in a PAROS vault (objective, status, metrics, problems, focus, next actions, map). Use when the person asks "where are we", "project status", "update the state", "initialize this project", or when starting work in an area that has a state file.
---

# project-state

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/project-state/CURRENT.md`;
   - `<vault>/PAROS/skills/project-state/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/project-state/CURRENT.md`.
2. Read it in full. Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running project-state v<X> from your vault`;
   - from the reference copy: `Running project-state v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
