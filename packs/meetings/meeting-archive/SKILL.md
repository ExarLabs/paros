---
name: meeting-archive
description: Classify a meeting (internal, team, client, lead, partner), pick the right recording, file the raw transcript and the note under one name in one home, handle the temporary audio, an optional shared mirror and the index. Use when the person says "archive this meeting", "save the transcript", "file this recording", "where should this meeting go", "clean up the meeting audio".
---

# meeting-archive

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/meeting-archive/CURRENT.md`;
   - `<vault>/PAROS/skills/meeting-archive/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/meetings/meeting-archive/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it if present (your areas, folders and rules). Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running meeting-archive v<X> from your vault`;
   - from the reference copy: `Running meeting-archive v<X> from the PAROS reference, not yet adopted`.
4. Follow it. It runs a file phase before the note and a close phase after it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
