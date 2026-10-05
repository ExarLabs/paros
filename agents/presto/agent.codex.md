---
title: Presto in Codex
date: 2026-10-05
status: active
description: How to use the Presto marketing viewpoint in OpenAI Codex or any agent that reads AGENTS.md: a routing line in the vault's AGENTS.md, an optional skill entry, and how the publishing gate and learning loop work without subagents or hooks.
---

# Presto in Codex

Codex has no agent registry like `.claude/agents/`. That is fine: a viewpoint is a file (P03), and the main session takes it on by reading it.

## 1. A routing line in the vault's `AGENTS.md`

Add under the vault's agents or viewpoints section:

```markdown
- **Presto** (one-to-many marketing: campaigns, adapting an idea to several channels, preparing
  publications, audience learning, publication log): when the topic is marketing to an audience,
  read `PAROS/agents/presto/CURRENT.md` and `LOCAL.md` next to it, say
  "Running Presto v<X> from your vault", and work by it. Its Constitution wins.
  One-to-one sales is not Presto.
```

This is enough: the routing comes from the topic, not from the name (P03 test).

## 2. Optional: a skill entry

If you prefer an explicit trigger, put a `SKILL.md` in Codex's skills folder with the same four steps as `agent.claude.md` (find, read, report the version, follow). Keep it thin; the knowledge stays in `CURRENT.md`.

## 3. The publishing gate in Codex

Codex may run with broad permissions. The gate is in the Constitution, not in the tool list, so it still holds: Presto prepares and shows the plan block; the `publish` step runs only after an explicit yes for that one publication, in the same session, and is logged in the publication log. Do not configure any automation that publishes from a schedule.

## 4. Learning without subagents

There is no background worker. When a lesson appears, write the learning packet to `PAROS/agents/presto/observations/`, then run Maestro's `learn-review` for it **at the end of the task** (read `PAROS/agents/maestro/CURRENT.md`, mode `learn-review`), or at the start of the next session. Mark learned-rule use with `[L-xxxx]` as usual; record the outcome with the cognition kit's `used` command when the person reacts.

## 5. Context protection

For wide reading (many campaigns, many areas), use the search skill first and read only the top few files. If Codex offers a separate task or worker, give it the Librarian's `retrieve` instructions and ask for a summary back.
