---
name: think
description: Orchestrate several AIs on one question in a PAROS vault: assemble a team with roles (researcher, strategist, validator), send fat prompts with a findings contract in parallel over API or browser, merge the answers, and keep a brainstorm state file. Use when the person asks to "think this through with several AIs", "brainstorm", "research from several angles", "attack this plan", or shares an AI conversation link to bring into the vault.
---

# think

Thin entry (PAROS P04). The knowledge lives in a live definition; this file only finds it.

1. Locate the live definition, first match wins:
   - where the vault entry file (`AGENTS.md` or `CLAUDE.md`) says skills live: `<skills folder>/think/CURRENT.md`;
   - `<vault>/PAROS/skills/think/CURRENT.md`;
   - the PAROS reference copy: `<paros repo>/skills/think/CURRENT.md`.
2. Read it in full. Read its `version:` field. Then read `LOCAL.md` next to it (personal setup); if missing, offer to create it from `LOCAL.example.md`.
3. Report one line before working:
   - from the vault: `Running think v<X> from your vault`;
   - from the reference copy: `Running think v<X> from the PAROS reference, not yet adopted`.
4. Follow it. Its `## Constitution` always wins.
5. If the person corrects the result, write a learning packet to the skill's `observations/` folder (P05).
