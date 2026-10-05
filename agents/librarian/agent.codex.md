---
title: Librarian in Codex
date: 2026-10-05
status: active
description: How to use the Librarian knowledge caretaker viewpoint in OpenAI Codex or any agent that reads AGENTS.md: a routing line, context protection without subagents, scheduled index checks, and the learning loop.
---

# Librarian in Codex

Codex has no agent registry like `.claude/agents/`. A viewpoint is a file (P03); the session takes it on by reading it.

## 1. A routing line in the vault's `AGENTS.md`

```markdown
- **Search first:** for "where is X" use the search skill (2 to 4 word stems); grep only for exact strings and code.
- **Librarian** (vault care: tier indexes, frontmatter and link audit, tidying and archiving with dry runs,
  integrating outside material and transcripts; wide reads that should come back as a summary):
  read `PAROS/agents/librarian/CURRENT.md` and `LOCAL.md` next to it, say
  "Running Librarian v<X> from your vault", work in one mode, and follow its Constitution.
```

## 2. Context protection without subagents

The Librarian's main value as a worker is that it reads so the caller does not. In Codex:

- If a separate task or worker is available, start it with the `retrieve` mode and ask for the ranked list and summary only.
- If not, follow `retrieve` inline with discipline: search first, read only the top three to five files fully, and list the rest by path and description.

## 3. Index checks on a schedule

`index` and `audit` are safe to run unattended (they write only derived files and reports). Run them from any scheduler, or at the start of a session when the last run is older than a week. `tidy` and `deep-clean` are never scheduled: they need a dry run and a yes.

## 4. Learning

Write learning packets to `PAROS/agents/librarian/observations/`, then run Maestro's `learn-review` at the end of the task (read `PAROS/agents/maestro/CURRENT.md`), or at the start of the next session.
