---
title: build-a-dashboard
status: active
description: Playbook for a view on a PAROS vault in three levels. Level 0 is the notes editor, level 1 a zero-build local Node.js page (ranked search, note preview, tasks ticked back into markdown, live refresh), level 2 a React app on the same API. The view holds no knowledge and writes only into markdown. Built on the view kit and the starter dashboard.
---

# Playbook: build a dashboard

The view is the least important layer of PAROS: the markdown is the system. But an overview on one screen helps, for a morning look, a weekly review or a workshop. This playbook takes you from no app at all to a live local page in a few minutes, and shows how to grow it without ever locking knowledge inside it.

## What you get

| Level | What you see | What it costs |
|---|---|---|
| **0. No app** | Your notes editor (Obsidian, for example) | nothing |
| **1. Minimal view** (recommended start) | A local page: ranked search, note preview, open tasks you can tick (written back into the markdown file), live refresh when files change | Node.js 18+, no install step, no build |
| **2. React app** | Boards, timelines, graphs, forms on the same API | npm, a build tool, a frontend project to maintain |

A heavier application is possible: a full app that reads a search index of the vault and serves many pages (planner, timeline, usage) can grow out of this. It is not where to start. The zero-build view does most of what people need, and it cannot break on the next machine.

## Before you start

| Piece | Status |
|---|---|
| The three-level guide | exists in the repo: [`kits/view/README.md`](../kits/view/README.md) |
| The minimal server and page (`server.mjs`, `public/`) | exists in the repo: [`kits/view/node-minimal/`](../kits/view/node-minimal/README.md) |
| A working demo with agent cards and a freshness panel | exists in the repo: [`starter/dashboard/`](../starter/README.md) |
| React build instructions for an agent | exist in the repo: [`kits/view/react/INSTRUCTIONS.md`](../kits/view/react/INSTRUCTIONS.md) |
| Your copy of the view, your own panels, any new endpoints | written by the agent at adoption, **outside** your vault |
| A start command or skill entry ("start my dashboard") | written by the agent at adoption |

You need: Node.js 18 or newer. Your notes should have frontmatter with a real `description`; search ranks it five times above the body, so good descriptions make a good dashboard.

## Steps

1. **See it first (two minutes).** The agent starts the demo vault's dashboard so you can see what level 1 feels like:
   ```bash
   node <paros repo>/starter/dashboard/server.mjs
   # open http://localhost:4747
   ```
   Tick a task in the page and watch `starter/TODO.md` change. *You decide* whether this level is what you want, or whether the notes editor is enough for now (level 0 is a fine answer).

2. **Choose where the view lives.** The minimal view has no dependencies, so it can sit anywhere **outside** the vault, for example a tools folder next to it. *You decide* the folder. The agent copies `kits/view/node-minimal/` there; nothing from it goes into your notes.

3. **Point it at your vault and your task files.**
   ```bash
   node <view folder>/server.mjs "<your vault>" --tasks "TODO.md" --port 4747
   ```
   `--tasks` names the files that hold your task list, relative to the vault root, comma separated. *You decide* which files count as task lists.

4. **Open it and try the four things it does.** Search for a topic you know exists; open a note (the description is shown on top); tick a task and confirm the markdown line changed; edit a note in your editor and watch the page refresh.

5. **Add your own panels, one at a time.** Ask for what you actually look at:
   - "show my areas, each with its state file's last date" (a freshness panel, like the starter's);
   - "a board of notes by their `status` field";
   - "a timeline from the `date` in frontmatter";
   - "today's briefing on a page" (from the [daily briefing](daily-briefing.md) output file).

   The agent's rule for every panel: **if the page needs data the API does not give, add an endpoint to the server first, reading markdown.** Never a local database, never app-only fields. If a new field is needed, it goes into the notes' frontmatter. *You decide* each panel; keep the ones you use.

6. **Make starting it effortless.** The agent writes a one-line start command, or a skill entry so you can say "start my dashboard" in any session. Optionally it starts with your machine; *you decide*.

7. **Level 2, only if you outgrow level 1.** If you want rich interaction and are comfortable maintaining a frontend project, the agent follows `kits/view/react/INSTRUCTIONS.md`: a Vite project outside the vault, a typed client for the same six endpoints, search and preview first, task write-back through `/api/toggle` only, live refresh from `/api/events`, then your own views. A production build is served by the same minimal server:
   ```bash
   node server.mjs "<your vault>" --public "<react project>/dist"
   ```
   If answers to "what would you see that level 1 does not show?" are vague, the agent extends level 1 instead.

8. **Snapshots for sharing.** A view you send to someone (a PDF, a static page) is a snapshot: it carries "as of YYYY-MM-DD" and its source. Live views stay on localhost.

## Check that it works

Proof, not "the page loads" (P11):

- **Write-back:** tick a test task in the page; the exact line in the markdown file now reads `- [x]`. Untick it; it reads `- [ ]` again.
- **Stale-write guard:** read a task from `/api/tasks`, change its text in your editor, then send the old `raw` line to the server:
  ```bash
  curl -s -X POST http://localhost:4747/api/toggle -d '{"path":"TODO.md","line":<n>,"text":"<old raw line>"}'
  ```
  The server answers with a conflict ("the line changed since it was read"), and the file is unchanged.
- **Live:** edit any note; the page updates without a reload. (Live refresh needs recursive file watching; where the platform lacks it, the page still works and the agent says that refresh is manual.)
- **Holds nothing:** stop the server and delete the view folder. Nothing in your vault is missing. Copy it back and it works again.
- **Local only:** the server listens on `127.0.0.1`; from another device on the network the page does not open.
- **Search quality:** a search for a topic returns the note whose description is about it among the first three results.

## Pitfalls

- **Building the app before the habit.** Most people need no app for weeks. A dashboard nobody opens is maintenance with no return.
- **Knowledge in the view.** An app-only field, a local database, a board order stored in the browser: the day the app breaks, that knowledge is gone. Every fact lives in markdown (P01).
- **Writes that are too big.** Each kind of write is explicit and small, like ticking a task, and refused if the line changed since it was read.
- **`node_modules` in the synced vault.** Thousands of files syncing between machines. A view with dependencies lives outside the vault.
- **A heavy stack too early.** A framework, a build step and a dependency tree that breaks on the next machine. Prefer zero-build until a real need forces more.
- **Snapshots without dates.** A static page that looks live misleads. Every snapshot says when it was made and from what.
- **Exposing it on the network.** The view reads your whole vault. Keep it on localhost; sharing is a deliberate, separate act (P00).
- **A page nobody can find.** A new page with no menu entry or start command is effectively missing. Every page gets a link from the main view.
- **Silent frontmatter gaps.** Notes without a `description` rank poorly and show empty cards. The fix is in the notes, not in the view.

## Principles behind it

- [P02](../principles/P02-presentation.md): presentation is HTML, a live view that writes back to markdown; minimal and disposable.
- [P01](../principles/P01-persistence.md): the view holds no knowledge; everything is derived.
- [P06](../principles/P06-search.md): ranked search, description weighted above body.
- [P00](../principles/P00-constitution-and-boundaries.md): local only; sharing is a deliberate act.
- [P11](../principles/P11-health-contract.md): prove write-back and refresh, not just that the page loads.

## Related

- Kit: [`kits/view`](../kits/view/README.md) (levels 0, 1, 2), [`kits/view/node-minimal`](../kits/view/node-minimal/README.md), [`kits/view/react/INSTRUCTIONS.md`](../kits/view/react/INSTRUCTIONS.md).
- Demo: [`starter/dashboard`](../starter/README.md) (agent cards, search, tasks, freshness).
- Kits: [`kits/search`](../kits/search/README.md) (a stronger index behind a bigger view), [`kits/health`](../kits/health/README.md).
- Agent: [`agents/alfred`](../agents/alfred/CURRENT.md) (the briefing and task store a dashboard renders).
- Playbooks: [`daily-briefing`](daily-briefing.md), `publish-from-your-vault`, `planner-and-timeline`.
