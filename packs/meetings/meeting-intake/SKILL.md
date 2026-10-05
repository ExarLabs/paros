---
name: meeting-intake
description: Turn a raw meeting transcript into a structured note: decisions with status, commitments with owner and date, open questions, risks, exact numbers, follow-ups. Use when the person says "process this meeting", "write up the meeting", "what did we decide", "make notes from this transcript".
---

# meeting-intake

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/meeting-intake/CURRENT.md`;
   - `<vault>/PAROS/skills/meeting-intake/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/packs/meetings/meeting-intake/CURRENT.md`.
2. Read it in full, and the `LOCAL.md` next to it if present (your areas, folders and rules). Read its `version:` field.
3. Report one line before working:
   - from the vault: `Running meeting-intake v<X> from your vault`;
   - from the reference copy: `Running meeting-intake v<X> from the PAROS reference, not yet adopted`.
4. Follow it. For high-stakes meetings, offer `adversarial-second-pass` afterwards. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
