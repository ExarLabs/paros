---
name: cv-tailoring
description: Tailor an existing CV to one bid, tender or job description in a PAROS vault: keep the source untouched, reframe a new version with evidence only, build a requirement coverage table and an internal covering note that names the gaps. Use when the person asks to "tailor this CV to this job", "prepare CVs for this bid", "retarget a profile", or hands over a job description with candidate names.
---

# cv-tailoring

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/cv-tailoring/CURRENT.md`;
   - `<vault>/PAROS/skills/cv-tailoring/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/cv-tailoring/CURRENT.md`.
2. Read it in full. Read its `version:` field. Then read `LOCAL.md` next to it (personal setup); if missing, offer to create it from `LOCAL.example.md`.
3. Report one line before working:
   - from the vault: `Running cv-tailoring v<X> from your vault`;
   - from the reference copy: `Running cv-tailoring v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
