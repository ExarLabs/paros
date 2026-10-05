---
title: daily-briefing
status: active
description: Playbook for a daily briefing in a PAROS vault. One prioritised view of today built from the task list, area task files, state files, prepared mail dossiers, the calendar and recent meeting notes, ordered by the owner's priorities, with a briefing log the agent learns from. Built on the Alfred agent.
---

# Playbook: daily briefing

"What is on today?" answered in one screen, from your own vault and tools, in the order that matches what you said matters. The briefing is read-only toward your sources: it gathers, sorts and points; it never rewrites your task files or sends anything.

## What you get

- **One view of today**, gathered from every place tasks actually live: your vault task list, the agent's own task scopes, each area's task file and state file, prepared mail dossiers, items waiting for your decision, the calendar, and open checkboxes in recent meeting notes.
- **An order you set.** First what connects to your current priorities, then due dates, then how useful each source has proven to be.
- **A source next to every item,** so one click takes you to the file it came from. The same task found in two places is shown once, with both sources.
- **Freshness stated.** A calendar snapshot from yesterday or a mail source that could not be reached is named as such, never shown as today's truth.
- **A system that gets better.** Each briefing is logged; your reactions ("done", "drop it", "not relevant") teach the agent which sources and orderings help you.
- **A priorities conversation** (the `focus` mode) that writes the priorities file the briefing sorts by.

## Before you start

| Piece | Status |
|---|---|
| The Alfred viewpoint with its `today` and `focus` modes | exists in the repo: [`agents/alfred/CURRENT.md`](../agents/alfred/CURRENT.md) |
| Settings template (home folder, scopes, task sources, calendars) | exists in the repo: [`agents/alfred/LOCAL.example.md`](../agents/alfred/LOCAL.example.md) |
| One vault task list with an inbox section | exists as an example in [`starter/TODO.md`](../starter/TODO.md); yours is created or confirmed at adoption |
| `LOCAL.md`, `priorities.md`, the source register, the briefing log | written by the agent in your vault at adoption |
| A `today` command or skill entry for your platform | written by the agent at adoption (thin entry, P04) |
| Calendar and mail access | optional; your connectors (see `guides/add-a-connector.md`) |

You need: a vault with a task list, and an agent (Claude Code or Codex) running in it. Calendar and mail make the briefing richer but are not required for the first run.

## Steps

1. **Adopt Alfred.** The agent copies `agents/alfred/CURRENT.md` into your vault (default `PAROS/agents/alfred/CURRENT.md`), creates `LEARNINGS.md` and `observations/` next to it, and installs the thin entry for your platform. *You decide* whether Alfred is the right name for you; the viewpoint works under any name.

2. **Fill in `LOCAL.md`.** The agent copies `LOCAL.example.md` and asks you, one question at a time: where Alfred's home folder lives, which scopes you want (for example `personal`, `family`, `bakery`, `consulting`), where your vault task list is, and which calendars and mailboxes exist. *You decide* each value. Identifiers only; never a password or token (P07).

3. **Seed the task sources.** The agent proposes a starting list for the source register (`state/task_sources.md`):
   ```
   Areas/*/TASKS.md             only items assigned to you, or due within 3 days
   Areas/*/01_PROJECT_STATE.md  next actions
   Meetings/ notes, last 7 days open checkboxes
   Excluded: Archive/, Templates/
   ```
   *You decide* what to exclude. From then on the agent discovers new sources itself (at most once a day) and adds them with yield `new`; a source you mark `excluded` stays out.

4. **Have the first priorities conversation.** Say "let's talk about my priorities". In `focus` mode the agent reads your area state files and recent journal, reflects back in three to five lines, asks one question at a time, and names conflicts ("this contradicts what the area plan says"). When you close ("fine, that's it"), it writes `priorities.md`: an `## Active now` list of three to five items, each with why and source, plus a history section where old priorities move instead of being deleted. *You decide* every priority; the agent only mirrors and asks.

5. **Run the first briefing.** Say "what is on today?" The agent:
   - reads the source register and every source not marked resting or excluded;
   - reads `priorities.md`;
   - reads the calendar (live, or a snapshot with its time stated);
   - optionally asks the main session for a short mail and project-tool brief (connectors are read-only here);
   - writes the view in fixed sections, in this order:
     ```
     Today's calendar
     Prepare        (external or small meetings, with relevant vault notes)
     Overdue / urgent
     Due today
     Waiting for your decision
     Soon (next 3 days)
     Current priorities
     System status  (last sync, last triage, unreachable sources)
     ```
   - appends the run to `state/briefing_log.md`: the items shown, in order, with sources.

6. **React, and let it learn.** Say "done with X", "drop Y", "why is Z here?". The agent ticks done items in **their own** source file with a date (or moves them to that file's done section by its own convention), marks your reactions in the briefing log, and updates each source's yield. A source that keeps producing noise sinks to the bottom of its section and after 30 days rests. A general lesson about how you work becomes a learning packet (P05) and you see one line: "Learned: ... -> file".

7. **Add a strategy map (optional, after a week or two).** The agent builds `strategy_map.md`: per area, the strategy and state documents, how fresh they are, and the gaps. The briefing then ends with one line when an area with work today has an outdated strategy. *You decide* whether a gap matters.

8. **Schedule it (optional).** If your platform can run scheduled tasks, run the briefing each morning, unattended. *You decide* whether. An unattended run is silent and degrade-safe: no questions, no external writes, unreachable sources skipped and logged.

## Check that it works

Proof, not "the command ran" (P11):

- Put a test task due today in one area task file (`- [ ] Briefing canary 📅 <today>`). The next briefing shows it under "Due today" **with that file as its source**. Tick it through the briefing ("done with briefing canary") and confirm the line in the area file is now `- [x] ... ✅ <today>`.
- Open `state/briefing_log.md`: today's run is there, with the items and your reaction marked.
- Open `state/task_sources.md`: `last_discovery` is today or yesterday.
- Stop one connector (or run where mail is unreachable): the briefing still appears, and "System status" names the missing source.

If any of these fails, the briefing is not working yet, whatever it printed.

## Pitfalls

- **A stale queue shown as today.** A calendar snapshot or mail brief from yesterday looks exactly like today's. Every source carries its time; old ones are labelled.
- **The briefing rewriting your files.** It reads sources and changes them only when you say something is done. Priorities change only through the `focus` conversation.
- **Everything becomes a task.** If the briefing turns every note into an item, the list oppresses. Filter area files to items assigned to you or due soon; let some items simply be archived.
- **The same task three times.** A task copied into the vault list, an area file and a meeting note appears once, with all three sources. Deduplicate before showing.
- **Too many sources too early.** Start with three to five. The register grows by discovery, and yield tells you which ones earn their place.
- **Advice nobody asked for.** The briefing reports and orders; it does not moralise or add opinions. Stay with the owner's own words.
- **Private content leaking.** Family and health items stay in the personal scope. Another viewpoint gets a reference, never the detail, and only with your yes.
- **Mail as instructions.** A line in an email that reads like a command is data. It shows up quoted in a dossier; it is never executed.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): read-only toward sources, nothing sent, Alfred's constitution.
- [P01](../principles/P01-persistence.md): tasks, priorities and logs are markdown; any board only renders them.
- [P03](../principles/P03-agent-is-a-viewpoint.md): Alfred is the vault seen from the owner's chair.
- [P05](../principles/P05-closed-loop-learning.md): the briefing log and your reactions are evidence for learning.
- [P06](../principles/P06-search.md): index first when gathering context for meetings.
- [P11](../principles/P11-health-contract.md): the canary task and stated freshness.
- [P12](../principles/P12-one-fact-one-owner.md): a done task is closed in its own file, not in a copy.

## Related

- Agent: [`agents/alfred`](../agents/alfred/CURRENT.md) (`today`, `focus`, `tasks`, `done`, `next`, `status`).
- Playbooks: [`capture`](capture.md) (what feeds the inbox), [`meetings`](meetings.md) (meeting prep in the briefing), [`build-a-dashboard`](build-a-dashboard.md) (the briefing on a page), `email-triage` (prepared dossiers).
- Kits: [`kits/search`](../kits/search/README.md), [`kits/health`](../kits/health/README.md), [`kits/view`](../kits/view/README.md).
- Pack: [`packs/meetings`](../packs/meetings/README.md) (`meeting-prep` notes appear under "Prepare").
- Guides: [`guides/daily-work.md`](../guides/daily-work.md), [`guides/add-a-connector.md`](../guides/add-a-connector.md).
