---
title: task-inbox
status: active
description: Playbook for one task list with an unformatted Inbox the owner drops anything into, sorted by the agent into Now, Waiting or an area's own task file with a pointer, two markers for owner decisions and outside blockers, and a dated Done log; nothing dropped is ever deleted.
---

# Playbook: task inbox

## What you get

One task list for your whole life and work, with an **Inbox** at the top where you drop anything, unformatted, even a single word. The agent reads the list at the start of every session, sorts the inbox into *Now*, *Waiting* or the right area's own task file, and never loses a line you wrote. You get one front door to your tasks instead of a dozen lists you have to remember to check.

## Before you start

- A vault with an entry file (`AGENTS.md`, or `CLAUDE.md` for Claude Code). If you have none yet, start with [`organise-your-knowledge`](organise-your-knowledge.md) or at least step 6 of it.
- A way back (git, a copy, or version history), because the agent will move lines in this file.
- Ten minutes. No scripts are needed: this is a markdown file and a rule.

## Steps

### 1. Choose the one file

**Agent:** looks for existing task lists in the vault (files named like `TODO`, `Tasks`, checkbox-heavy notes, area task files) and shows what it found, with how many open items each has.

**You decide:** where the single front door lives. Usually the vault root: `TODO.md`. Existing area lists stay where they are (step 5); this file becomes the entry to all of them.

### 2. Create the structure

**Agent:** creates the file (or reshapes the existing one, with your yes) with a frontmatter header and these sections, in this order:

```markdown
---
title: TODO
date: <YYYY-MM-DD>
author: <you>
status: active
description: <your single task list across your areas, with an unsorted inbox, current tasks, waiting items and a dated done log>
id: <uuid4>
tags: [tasks]
---

# TODO

> **For you:** write anything into the Inbox, as it comes. No format, no full sentence, no area needed. One line is enough.
>
> **For the agent:** read this file at the start of every session. Sort the Inbox: concrete items go to Now or Waiting; an item that belongs to one area goes to that area's task file, with a one-line pointer left here. Never delete a line the owner dropped in without asking; at most, move it.

## Conventions

- Area tag in square brackets at the start of a line: `[Bakery]`, `[Book Club]`, `[Personal]`
- ⚠️ = waiting on the owner's decision; the agent cannot move on without it
- ⛔ = blocked, and the blocker is outside our hands (write who or what)
- Area task files: <list of links, one per area that has its own>

## Inbox

<!-- Yours from here. Anything, one line is enough. -->

## Now

## Waiting

## Done
```

The two notes at the top are for both readers: they tell you that nothing needs formatting, and they tell any agent, in any session, what to do with the file.

**You decide:** the section names (in your language) and your area tags. The markers can be any symbol you like; what matters is that there are exactly two of them and that they mean different things (step 4).

### 3. Add the rule to the entry file

**Agent:** adds a short section to the vault entry file:

- the task list is at `<path>`; **read it at the start of every session**;
- the agent sorts the Inbox; a dropped line is never deleted without asking, only moved;
- a finished task moves to *Done* with the date; it is not deleted;
- area tasks live in the area's own task file, with a one-line pointer here.

**You decide:** you read the section before it is written.

### 4. Sort the inbox, the same way every time

**Agent:** at the start of a session (or when you say "sort my inbox"), takes each Inbox line and proposes one destination:

| The line is | It goes to |
|---|---|
| concrete and can be done now | *Now*, with the area tag, rewritten only as much as needed to be actionable, with your words kept |
| waiting on someone else | *Waiting*, with ⛔ and who it waits on ("waiting on the supplier, asked 2026-09-30") |
| waiting on your decision | *Now* or *Waiting*, with ⚠️ and the question you need to answer |
| the internal business of one area | that area's task file, and a one-line pointer stays here: `- [Bakery] Oven service: see [Bakery tasks](Areas/Bakery/TASKS.md)` |
| too vague to place | stays in the Inbox, and the agent asks one short question about it |
| not a task at all (an idea, a note) | a note in the right place, with a pointer, or stays put until you say |

**You decide:** you see the proposed moves as one list and say yes, or correct individual lines. Your corrections are lessons (P05): if you keep moving the same kind of line elsewhere, the agent learns where it belongs.

The two markers matter because they lead to different actions: ⚠️ items come to you in the briefing as questions; ⛔ items are chased with the person named, or simply waited on.

### 5. Connect the area task files

**Agent:** for each area with its own task list, adds a link under *Conventions* and makes sure the area file has the same simple shape (open items, a done log). From then on, area-internal items go there, and this file holds one pointer line per item, not a copy.

**You decide:** which areas deserve their own file. A rule of thumb: an area with many small tasks that only matter inside it (a team's tickets, a renovation's punch list). Everything else lives in the main file.

One fact, one owner (P12): a task lives in exactly one place. The pointer says where; it never duplicates the text.

### 6. Close tasks into Done, with a date

**Agent:** when you say something is finished (or the agent sees the result), moves the line to *Done* as `- [x] <task> (YYYY-MM-DD)`. It does not delete it.

**You decide:** nothing for an unambiguous tick. For an ambiguous one ("the flour thing is done?"), the agent asks.

The *Done* log is how you answer "what did I finish this month?" later, and how a recap or a review sees your actual pace. When it grows long, move older entries to an archive note per quarter or year (P09), not to the bin.

### 7. Let automatic processes report here

**Agent:** points any automatic process that needs your attention at this file. The health kit, for example, adds one line under *Now* when a check turns red and ticks it when it recovers, so problems appear where you already look.

*In the repo:* kit [`kits/health`](../kits/health/README.md) writes its alerts into this file (`PAROS_TASKS`, `PAROS_TASKS_SECTION`).

## Check that it works

Look at the file itself, not at what the agent says about it (P11):

1. **Drop three lines** into the Inbox: one concrete ("rye flour price"), one vague ("oven??"), one that belongs to an area. Start a new session. The agent should mention the list without being asked, and propose a destination for each line, with a question for the vague one.
2. **Nothing lost.** After sorting, every line you dropped is somewhere: in a section, in an area file with a pointer here, or still in the Inbox. Compare the count before and after.
3. **Done has dates.** Tick something off; it should appear under *Done* with today's date, and be gone from *Now*.
4. **Markers mean what they say.** Every ⛔ line names its blocker. Every ⚠️ line contains a question you can answer.
5. **One place per task.** Pick an area task; it exists once, in the area file, with only a pointer in the main list.

## Pitfalls

- **The agent deleting "obvious" junk.** A one-word line can be the only trace of something important to you. The rule is absolute: move, never delete without asking.
- **Formatting the inbox for you.** The inbox works because it costs nothing to use. If the agent demands a format, or rewrites your words heavily, you stop using it. Keep your words; add only the area tag and what makes it actionable.
- **The list not being read.** A task list the agent does not read at session start is a diary. The rule belongs in the entry file, not in the agent's memory.
- **Copying area tasks into the main list.** Two copies drift apart; one gets ticked, the other stays open forever. Pointer, not copy.
- **One marker for two meanings.** "Waiting" that mixes "waiting on me" and "waiting on someone else" hides the decisions only you can make. Two markers, two actions.
- **Everything becomes a task.** If every thought turns into a task, the list oppresses. Some lines are ideas or notes; some are simply archived.
- **Done without a date.** Without the date, the log cannot answer "when", and a later recap has nothing to stand on.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): the agent proposes, you decide; deleting is never autonomous.
- [P01](../principles/P01-persistence.md): the task list is plain markdown; any board or dashboard only renders it.
- [P05](../principles/P05-closed-loop-learning.md): your corrections to the sorting are lessons.
- [P09](../principles/P09-forgetting-and-archiving.md): done items move and archive, never vanish.
- [P11](../principles/P11-health-contract.md): alerts land where you already look.
- [P12](../principles/P12-one-fact-one-owner.md): a task lives in one place; elsewhere it is a pointer.

## Related

- Agent: [Alfred](../agents/alfred/CURRENT.md) (chief of staff: reads this list every briefing, captures raw thoughts, sorts, ticks; never deletes).
- Kit: [`view`](../kits/view/README.md) (a live view of the tasks that writes back to the same markdown).
- Kit: [`health`](../kits/health/README.md) (alerts as task lines on state change).
- Skill: [`project-state`](../skills/project-state/) (an area's current state, next to its task file).
- Demo: [`starter/TODO.md`](../starter/TODO.md) (a filled-in example with fictional areas).
- Guide: [`guides/daily-work.md`](../guides/daily-work.md).
- Playbooks: [`organise-your-knowledge`](organise-your-knowledge.md), `daily-briefing` and `capture` (in the catalog).
