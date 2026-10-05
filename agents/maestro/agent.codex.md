---
title: Maestro in Codex
date: 2026-10-05
status: active
description: How to use the Maestro system caretaker in OpenAI Codex or any agent that reads AGENTS.md: routing lines, running learn-review at the end of a task instead of in the background, starting the cognitive cycle from a session-start check, and keeping family-wide edits behind a dry run.
---

# Maestro in Codex

Codex has no agent registry like `.claude/agents/`, no background subagents in the same sense, and no `UserPromptSubmit` or `Stop` hooks. Maestro still works: it is a file the session reads (P03), and the scripts it relies on are plain Python.

## 1. Routing lines in the vault's `AGENTS.md`

```markdown
- **Unsure who owns a request?** Read `PAROS/agents/maestro/CURRENT.md`, section "Collaboration: the routing table",
  and route; do not guess.
- **Every lesson** (a correction, a rejection, a rule that did not fit, a better way): write a learning packet
  to the `observations/` folder next to the affected definition, then run Maestro's `learn-review` for it
  at the end of the task. Report one line: "Learned: ... -> <file>". Never show a dropped packet.
- **At session start:** run `python PAROS/kits/cognition/cognition.py due`; if it says due and not leased,
  run Maestro's `cycle` mode following the cognition kit's CYCLE.md, and append its report to your answer.
```

## 2. learn-review without a background worker

Run it inline, after the person's actual request is done, so it never delays their work. If a separate task or worker is available, give it the packet path and `mode: learn-review`. Either way the steps are the same: evidence threshold, one typed change, `judge.py` with a model from another family, `learn_merge.py` to apply. A lesson about Maestro itself is reviewed in a fresh session or task, not in the one that produced it.

## 3. Marking rule use

Mark a decision that rests on a weighted learned rule with `[L-xxxx]`. With no Stop hook, record the outcome yourself when the person reacts: `cognition.py used L-xxxx --outcome helpful|harmful|neutral`.

## 4. Family-wide edits

`team-promote`, `team-introduce` and `optimize` keep their dry run and yes. Codex may run with broad write permission; the gate is in the Constitution, not in the sandbox, so it still applies.
