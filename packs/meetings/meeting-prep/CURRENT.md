---
title: meeting-prep
date: 2026-10-05
status: active
description: Writes a one-page prep note before a meeting from what the vault already knows (previous notes, open commitments both ways, open questions, recent decisions, the area's state), with the goal, questions to ask, sensitivities, a proposed agenda and a recording reminder; it reads, it never contacts anyone.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# meeting-prep

Most meetings start with "where were we?". The vault usually knows: what was promised last time, what is still open, what changed since. This skill puts that on one page before the call, so the person walks in knowing what they want to leave with, and the intake afterwards can compare what came out with what went in.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- Read-only on the vault, except for writing the prep note itself.
- Never contacts participants. An agenda or a reminder to others is a draft for the person to send.
- Only facts from the vault, each with a link to where it comes from. Gaps are named as gaps, not filled with guesses.
- Recording needs the participants' consent; the prep note reminds, the person decides.
- Notes about people (performance, pay, health, private matters) are not pulled into a prep note that others might see; if relevant, they are referenced by link only, in a section marked private.

## Personal settings: LOCAL.md

Read `LOCAL.md` next to this file. It names: the areas and their meeting folders, where state files, open questions, decisions and the task list live, how to search the vault, which calendar (if any) the agent may read, the consent rule for recording that applies to the person, and how long before a meeting the prep is useful. Without `LOCAL.md`: ask for the area or counterparty, search the vault, no calendar.

## When to use

- "Prepare me for the meeting with ...", "what do I need to know before the call", "where did we leave it with ...", "make an agenda for tomorrow's ...".
- In a morning briefing, for each meeting of the day that has an area or counterparty in the vault.

## Inputs

1. The meeting: who, when, what about. From the person's words, or from a calendar entry if `LOCAL.md` allows reading one.
2. The area or counterparty. If unclear, one question.

## Steps

### 1. Find the home

Resolve where this meeting will be archived, the same way `meeting-archive` classifies (internal, team, client, lead, partner). The prep note goes there, so the intake finds it later. If the classification is ambiguous, ask.

### 2. Gather, index first

Search the vault (P06) for the area or counterparty, then read, newest first:

- the last two or three meeting notes from that home: decisions, commitments, open questions, risks;
- the area's state file, decisions register and open questions;
- open tasks in the task list that link to those notes;
- anything newer than the last meeting that mentions the counterparty or topic (emails filed in the vault, notes, documents).

Stop when the picture is clear; a prep note is one page, not a dossier.

### 3. Sort the commitments

Split every commitment from the previous meetings into: **ours, done**; **ours, open** (with due date and whether it is late); **theirs, done**; **theirs, open**. Open items on both sides are the most useful lines in a prep note.

### 4. Write the note

`<home>/<stem>.prep.md`, where the stem is `YYYY-MM-DD-<slug>` with the meeting date. Template below. Keep it to one page. Every fact links to its source.

### 5. Report

Where the note is, the three most important lines (usually: what we want out of it, our late commitments, their open ones), any gap the vault could not answer, and a draft agenda if the person wants to send one (as a draft only).

## Output template

```markdown
---
title: <stem>.prep
date: <meeting date>
status: active
description: <1-2 sentences: the meeting's purpose and the main open items going in>
---

# Prep: <meeting title>

> Prepared <date> from the vault. Sources linked per line. Gaps are marked [gap].

## Purpose and what we want to leave with
- ...

## Since last time
- ...

## Commitments
| Side | What | Due | State | Source |
|---|---|---|---|---|
| ours | ... | ... | open, late by <n> days | [[...]] |
| theirs | ... | ... | open | [[...]] |

## Questions to ask
1. ... (closes Q-<n>)

## Sensitivities
- ...

## Proposed agenda
1. ...

## Recording
- Ask for consent at the start. <the person's rule from LOCAL.md>
- Recorder saves to the temporary folder, not the vault.
```

## Pitfalls

- Read the previous meeting notes to the end; open commitments sit in the last sections and in the follow-ups. <!-- rule:R-001 since:2026-10-05 -->
- Separate ours from theirs, and open from done; a flat list of "action items" hides who owes what. <!-- rule:R-002 since:2026-10-05 -->
- Mark a late commitment of ours as late; it is the first thing the other side will remember. <!-- rule:R-003 since:2026-10-05 -->
- A prep note is one page; a dossier is not read before a call. <!-- rule:R-004 since:2026-10-05 -->
- Write the prep note into the meeting's future home, under the meeting's stem, so the intake can compare. <!-- rule:R-005 since:2026-10-05 -->
- Never present a guess from an old note as a current fact; if the vault is silent or stale, write [gap]. <!-- rule:R-006 since:2026-10-05 -->
- Do not send or schedule anything; agendas and reminders are drafts. <!-- rule:R-007 since:2026-10-05 -->
- When the person corrects a prep note or says something was missing, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-008 since:2026-10-05 -->
