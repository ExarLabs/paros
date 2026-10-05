---
title: Moneto in Codex
date: 2026-10-05
status: active
description: How to use the Moneto finance-steward viewpoint in OpenAI Codex or any agent that reads AGENTS.md: a routing line, approval settings for ledger writes, and the learning loop without subagents.
---

# Moneto in Codex

Codex has no separate agent registry; a viewpoint is a file the session reads (P03). Add one line to the vault's `AGENTS.md`, in a "Viewpoints" section:

```markdown
- **Moneto** (finance steward: per-organisation analysis and methodology notes, household bookkeeping): when the request is about the finances of a company, client, project or the household, read `PAROS/agents/moneto/CURRENT.md` and `LOCAL.md` next to it, say which version runs, and work by it.
```

Notes:

- The same `CURRENT.md` and `LOCAL.md` serve Claude Code and Codex; nothing is duplicated.
- Bookkeeping writes to an external ledger: run Codex in an approval mode that asks before network access and before running write scripts, and keep the dry run as the first step.
- Moneto never moves money on any platform; no tool that can pay, transfer or trade belongs in its session.
- Learning packets go to `PAROS/agents/moneto/observations/`, the same folder on every platform. With no background worker, run Maestro's `learn-review` on them at the end of the task (read `PAROS/agents/maestro/CURRENT.md`), or at the start of the next session.
