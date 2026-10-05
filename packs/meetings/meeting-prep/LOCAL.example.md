---
title: meeting-prep LOCAL
date: 2026-10-05
status: active
description: Personal settings for the meeting-prep skill (areas and sources to read, search command, calendar access, recording consent rule, timing). Copy to LOCAL.md and fill in your own values.
---

# meeting-prep: personal settings

> Example values for a fictional person who runs a small design studio and volunteers in a neighbourhood repair cafe. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below with your own.

## Where to look, per area

| Area | Meeting notes | State file | Decisions and open questions | Task list |
|---|---|---|---|---|
| Studio | `Work/Studio/meetings/`, `Work/Studio/Clients/<Client>/meetings/` | `Work/Studio/STATE.md` | `Work/Studio/decisions.md`, `open-questions.md` | `TODO.md`, section Studio |
| Repair Cafe | `Community/Repair Cafe/meetings/` | `Community/Repair Cafe/STATE.md` | `Community/Repair Cafe/decisions.md`, `open-questions.md` | `TODO.md`, section Repair Cafe |
| Home | `Home/meetings/` | none | none | `TODO.md`, section Home |

## Search

- `python ~/paros-kits/search/search.py "<2-4 word stems>"`; fall back to plain text search only for exact strings.

## Calendar

- The agent may read my calendar (read-only) to find today's and tomorrow's meetings. It never creates, moves or answers invitations.

## Recording consent

- I ask everyone at the start of the call and record only with a yes. For calls with clients I also mention it in the invitation. (Write the rule that applies where you live and work.)

## Timing

- Prep the evening before for client meetings, the same morning for internal ones.
- One page. If I ask for "the short version", three lines: goal, our open items, their open items.
