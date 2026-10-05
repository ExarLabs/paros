---
title: Iris LOCAL
date: YYYY-MM-DD
status: active
description: Personal settings for the Iris viewpoint in this vault, with made-up example values: teams and where their people notes live, roster and time-record sources, the growth framework, the people inbox, and what Iris may show about compensation. No secrets.
---

# Iris: local settings

> Copy this file to `LOCAL.md` next to the adopted `CURRENT.md` and replace the example values with yours. Identifiers and preferences only. `CURRENT.md` reads this file; updates from the PAROS reference never touch it. Do not paste personal data here: this file says **where** people notes live, not what is in them.

## Teams

| Team | Area | Person notes folder | Roster source |
|---|---|---|---|
| Studio | `Areas/Studio/` | `Areas/Studio/Team/People/` | `Areas/Studio/Team/team.md` (YAML list) |
| Bakery | `Areas/Bakery/` | `Areas/Bakery/people/` | the `People` section of `Areas/Bakery/AGENTS.md` |
| Volunteers | `Areas/Community/` | `Areas/Community/people/` | `Areas/Community/roster.md` |

Double appearances: the Studio delivery team is employed through the Consulting entity; one person, two notes, linked to each other. The Studio note holds the business context, the Consulting note the employer context.

## Activity sources (for allocation)

- Monthly summaries: `Areas/Studio/Reports/Monthly/HOURS_YYYY_MM.md` (person, level, hours, project)
- Raw exports: `Areas/Studio/Reports/raw/` (read-only; never edited)

## Roles and growth

- Role definitions: `Areas/Studio/Team/Roles.md`
- Growth framework entry: `Areas/Studio/Team/Growth/00_INDEX.md` (levels L1 to L7; tracks: engineering, design, operations)
- Direction the owner wants to grow towards: more people who can work directly on client sites (a "field engineer" path around L5 to L6). Measure paths against it; a "no, thanks" is a valid answer.

## People inbox

- `PAROS/agents/iris/people-inbox/` (processed signals in `processed/`)
- Main senders: Alfred (email triage), meeting notes.

## Compensation

- Iris may show the owner compensation that already appears in: `Areas/Studio/Team/Raises 2026.md`
- Mask in every output that leaves the owner: yes
- Never computed or written by Iris.

## Known gaps (live outside the vault)

- Contracts: in the payroll provider's system
- Onboarding checklists: not written yet

## Rhythm

| When | What |
|---|---|
| After each monthly hours summary | allocation |
| Monthly | pulse |
| When the inbox has signals | integrate, interactive |
