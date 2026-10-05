---
title: session-naming
date: 2026-10-05
status: active
description: Playbook for naming every agent session as MACHINE AREA · topic (for example "WIN WRK · Offer for Delta"), so that a person who works on several machines and in several areas sees at a glance, also on a phone, where each conversation runs, what it belongs to and what it is about. Codes are derived from the person's own areas; the agent renames the session itself where the app allows it, otherwise suggests the title once.
---

# Playbook: name every session (machine, area, topic)

## What you get

A session list you can read in one glance, even on a phone:

```
WIN WRK · Offer for Delta
MAC HOM · Kitchen renovation budget
WEB LRN · Course notes, week 3
```

Once you work in more than one area of life, or on more than one machine, this stops being cosmetic: it is how you find the right conversation again, how you know which machine a long task runs on, and how you avoid continuing a work topic in a family thread.

## When the advisor offers it

Without being asked, as soon as one of these is true:
- the person works in **two or more areas** (work and home, two companies, a course and a job);
- they use **two or more machines** or also start sessions from a phone or the web;
- they mention losing track of conversations, or have many open sessions.

The advisor offers it once, in one or two sentences, with an example built from their own areas.

## The format

```
<MACHINE> <AREA> · <topic>
```

| Part | Rule |
|---|---|
| `MACHINE` | three capital letters for where the session runs |
| `AREA` | three capital letters for the area of life or work; if a session touches two, use the main one and put the other in the topic |
| `·` | a middle dot with a space on each side (easy to see, not a dash) |
| `topic` | two to five words, starting with the thing itself (client, product, document), in the person's language |

**Length:** about 40 characters at most, because that is what a phone session list shows.

## Steps

### 1. Agree on the codes (one short conversation)

- **Machines:** ask which devices they start sessions on. Typical codes: `WIN` (Windows computer), `MAC`, `LIN` (Linux), `WEB` (browser or cloud), `MOB` (phone). Two computers of the same kind get distinct codes (`WIN`, `WI2`, or a short name they like).
- **Areas:** take the areas from their vault (the area folders or `organise-your-knowledge`), not from a template, and give each a three-letter code in their language. Keep a code for the advisor and system work itself (for example `SYS` or `PRS`).

### 2. Write the convention into the vault (with a yes)

Show the file first, then create it on a yes (AGENTS.md safety rule 7): `SESSION_NAMING.md` at the vault root (template: [`templates/SESSION_NAMING.md`](../templates/SESSION_NAMING.md)) with the format, the machine codes, the area codes, three examples from their own life, and one line: "When to rename".

### 3. Add one rule to the entry file (with a yes)

Propose this rule for their `AGENTS.md` (in their language):

> Every session is titled `<MACHINE> <AREA> · <topic>` (codes: `SESSION_NAMING.md`). Set it before your first real answer, as soon as the topic is clear, and update it when the topic changes substantially.

### 4. How the title is actually set

- **If the agent app lets the agent rename its own session** (some desktop apps give the agent a "rename session" or "set title" tool): the agent sets it itself, without asking each time, once the rule is adopted.
- **If not:** the agent writes the suggested title in one line at the start (for example "Title: `WIN WRK · Offer for Delta`") and the person renames the session in the app. Never repeat the suggestion in every answer.
- **Machine code:** the agent finds it out (for example from the hostname or the operating system) and maps it with the table in `SESSION_NAMING.md`; if it cannot tell, it asks once.

### 5. Keep it alive

- When a new area appears, add its code to `SESSION_NAMING.md` (with a yes).
- If titles drift (too long, dashes, no area), the agent corrects its own titles; repeated drift is a learning candidate (P05).

## Check that it works

- Open the session list on your phone: every title shows machine, area and topic, none is cut off.
- Start a session on another machine: its title starts with the right machine code.
- Change topic in a session: the title follows.

## Pitfalls

- Inventing area codes the person does not use. They come from their areas.
- Titles longer than a phone can show.
- Asking permission for every rename after the rule was adopted; or renaming before the rule was agreed.
- A different separator every time. One format, always.

## Principles behind it

[P00](../principles/P00-constitution-and-boundaries.md) (the person's own rules, in the entry file), [P03](../principles/P03-agent-is-a-viewpoint.md) (areas cut across agents), [P05](../principles/P05-closed-loop-learning.md) (drift becomes a lesson).

## Related

[`organise-your-knowledge`](organise-your-knowledge.md) (where the areas come from), [`shared-memory-across-machines`](README.md) (planned), [`daily-briefing`](daily-briefing.md).
