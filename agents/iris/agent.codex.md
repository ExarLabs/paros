---
title: Iris in Codex
date: 2026-10-05
status: active
description: How to use the Iris people-steward viewpoint in OpenAI Codex or any agent that reads AGENTS.md: a routing line, the people inbox, and the learning loop without subagents.
---

# Iris in Codex

Codex has no separate agent registry; a viewpoint is a file the session reads (P03). Add one line to the vault's `AGENTS.md`, in a "Viewpoints" section:

```markdown
- **Iris** (people steward: roster, one person, allocation, team pulse, integrating people signals): when the request is about the internal team or a person who works with me, read `PAROS/agents/iris/CURRENT.md` and `LOCAL.md` next to it, say which version runs, and work by it.
```

Notes:

- The same `CURRENT.md` and `LOCAL.md` serve Claude Code and Codex; nothing is duplicated.
- Integrate is the only writing mode, and it asks before every write. Run Codex in an approval mode that asks before edits if you want a second gate.
- Other viewpoints (and Codex sessions) send people signals by writing a `people-signal.v1` file into `PAROS/agents/iris/people-inbox/`; they never edit a person note directly.
- Learning packets go to `PAROS/agents/iris/observations/`, the same folder on every platform. With no background worker, run Maestro's `learn-review` on them at the end of the task (read `PAROS/agents/maestro/CURRENT.md`), or at the start of the next session.
