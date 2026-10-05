---
title: Alfred in Codex
date: 2026-10-05
status: active
description: How to use the Alfred chief-of-staff viewpoint in OpenAI Codex or any agent that reads AGENTS.md: a routing line, scheduled runs, and the learning loop without subagents.
---

# Alfred in Codex

Codex has no separate agent registry; a viewpoint is a file the session reads (P03). Add one line to the vault's `AGENTS.md`, in a "Viewpoints" section:

```markdown
- **Alfred** (personal operations: tasks, briefing, capture, email triage, recap): when the request is addressed to Alfred or is about my own tasks and day, read `PAROS/agents/alfred/CURRENT.md` and `LOCAL.md` next to it, say which version runs, and work by it.
```

Notes:

- The same `CURRENT.md` and `LOCAL.md` serve Claude Code and Codex; nothing is duplicated.
- Run Codex in an approval mode that asks before writing outside the workspace or using the network; Alfred's Constitution (never send, never delete) still applies on top.
- Scheduled runs (a morning briefing, an hourly triage) are started by your scheduler with a prompt such as "Alfred, today" or "Alfred, triage, unattended"; unattended runs only write internal dossiers.
- Learning packets go to `PAROS/agents/alfred/observations/`, the same folder on every platform. With no background worker, run Maestro's `learn-review` on them at the end of the task (read `PAROS/agents/maestro/CURRENT.md`), or at the start of the next session.
