---
title: README
date: 2026-10-05
author: PAROS reference
status: active
description: What the PAROS starter vault is (a small demo vault with fictional notes, three agents and a local dashboard), how to start it in three steps, and how to start the dashboard by hand.
id: 7a620b7b-8c01-4541-aca6-9655ff7f7a6e
tags: [starter, demo]
---

# PAROS starter vault

A small, complete example of a PAROS vault, so you can **see PAROS working** before you adopt anything into your own vault.

**This is a demo vault, not your vault.** Everything in it is fictional: a neighbourhood bakery, a half marathon training plan, a book club. Nothing here is meant to be copied into your notes. To build your own PAROS, go back to the repository root and use the advisor there ([`../README.md`](../README.md), "Quick start"): it diagnoses *your* vault and adapts the principles to it.

## What you will see

| Where | What it shows |
|---|---|
| [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md) | The vault's entry file: safety boundaries, frontmatter, search, learning, archiving, the task list (P00, P01, P04, P06, P05, P09) |
| [`TODO.md`](TODO.md) | One task list, with an inbox the agent sorts |
| [`Areas/`](Areas/) | Three areas, each note with frontmatter and a real `description` |
| [`Archive/`](Archive/) | One archived note, with the date and the reason (P09) |
| [`PAROS/ADOPTION.md`](PAROS/ADOPTION.md) | A filled example of the adoption checklist and log |
| [`PAROS/observations/`](PAROS/observations/) | One example learning packet (P05) |
| [`dashboard/`](dashboard/) | A local, zero dependency dashboard: agent cards, search, open tasks, freshness (P02) |

The three agents (Librarian, Maestro, Alfred) are defined in the repository, in [`../agents/`](../agents/). The starter links to them; it does not copy them.

## Start in 3 steps

1. **Open this folder** (`starter/`) in Obsidian as a vault, and in a terminal.
2. **Start an agent in it:** `claude` (Claude Code) or `codex` (OpenAI Codex). Both read `AGENTS.md`.
3. **Say:** "Start the PAROS dashboard". The agent starts the local server and gives you the address (default http://localhost:4747).

Then try: "What do we know about wholesale orders?", "What is open on my task list?", or tick a task in the dashboard and watch `TODO.md` change.

## Manual start

You need Node.js 18 or newer. Nothing to install, no build step.

```bash
# from the repository root
node starter/dashboard/server.mjs

# or from inside starter/
node dashboard/server.mjs

# options
node dashboard/server.mjs --port 4800
```

Open http://localhost:4747. Stop it with Ctrl+C.

## Resetting the demo

Ticking a task writes into `TODO.md`, and an agent may write notes while you try things. Because the starter lives inside the repository clone, one command puts it back as it was:

```bash
git restore starter/ && git clean -fd starter/
```

Obsidian creates a `.obsidian/` settings folder here when you open it; it is ignored by git.
