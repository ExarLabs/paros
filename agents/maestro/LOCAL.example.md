---
title: Maestro LOCAL
date: 2026-10-05
status: active
description: Personal settings for the Maestro system caretaker, with a fictional worked example: where the roster and kits live, the learning inboxes to sweep, judge configuration, cycle cadence, routing overrides for this vault and the owner's task list for unattended questions. Copy to LOCAL.md and replace with your own.
---

# Maestro: personal settings

> A worked example with made-up values. At adoption, copy this file to `LOCAL.md` next to `CURRENT.md` and replace everything. `LOCAL.md` never leaves your vault. No secrets here: keys live outside the vault (P07).

## Where things live

| What | Path in this vault |
|---|---|
| Agent roster | `PAROS/agents/INDEX.md` |
| Live definitions | `PAROS/agents/<name>/CURRENT.md` |
| Skills | `PAROS/skills/<name>/CURRENT.md` |
| Claude Code entries | `.claude/agents/`, `.claude/skills/` |
| learn-merge kit | `PAROS/kits/learn-merge/` |
| cognition kit | `PAROS/kits/cognition/` |
| Owner's task list (for unattended questions) | `TODO.md`, section "Now", line format `- [Learning] <question> (<packet path>, <date>)` |

## Active family

| Agent | Status | Notes |
|---|---|---|
| Alfred | active | personal operations |
| Librarian | active | |
| Presto | active | only for the bakery and the course |
| Maestro | active | |
| Iris | not adopted | small team, not needed yet |
| Moneto | active | household and bakery books |

## Learning inboxes to sweep

- `PAROS/skills/*/observations/`
- `PAROS/agents/*/observations/`
- `PAROS/kits/*/observations/`
- Lessons without an owner: `PAROS/observations/` with `capability: _skill-gap`

## Judge

- Reviewer family: the one Claude Code runs on.
- Judge: an open-weights model on a different provider (the kit's default), fallback as configured in the kit.
- Key: from the secrets folder outside the vault, never in a note.

## Cycle

- Every 4 hours, started by the hook on the next message.
- Learning roots: `PAROS/`, `Areas/`.
- Report: verbatim, at the end of the answer that started it.

## Rate limits

- At most 5 integrations per capability per day.
- Sweep: daily, or when 5 packets wait.

## Routing overrides for this vault

| Request | Goes to |
|---|---|
| Wholesale orders for the bakery (one to one) | main session, `Areas/Hillside Bakery/Sales/AGENTS.md` |
| Course enrolment questions | main session, `Areas/Woodshop Course/AGENTS.md` |
