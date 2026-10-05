---
title: activity-ledger LOCAL
date: 2026-10-05
status: active
description: Personal settings for the activity-ledger kit (area slugs, folders, machine names, summary language, privacy choice). Copy to LOCAL.md in your vault and replace every value.
---

# activity-ledger: personal settings

> Example values, all fictional. Copy to `LOCAL.md` next to where the kit lives in your vault. The script reads environment variables; this file records which values you chose and why, so an agent can set them the same way on every machine.

## Areas

`PAROS_LEDGER_AREAS=bakery,teaching,garden,household,system,other`

| Slug | Means |
|---|---|
| `bakery` | the small bakery business: suppliers, staff, the shop |
| `teaching` | the evening course: material, students, sign-ups |
| `garden` | the community garden plot |
| `household` | family admin, repairs, paperwork |
| `system` | work on the vault and its agents |
| `other` | anything that fits nowhere else |

## Folders

- Ledger: `PAROS/activity/` (default).
- Journal: `Journal/` (`PAROS_JOURNAL_DIR=<vault>/Journal`), so it sits next to the daily notes.

## Machines

| Host name | `PAROS_HOST` |
|---|---|
| the laptop | `laptop` |
| the shop computer | `shop` |

## Summary

- `PAROS_LEDGER_SUMMARY=cli`, `PAROS_LEDGER_MODEL=haiku`, `PAROS_LEDGER_LANG=English`.
- On the shop computer: `PAROS_LEDGER_SUMMARY=off` (shared machine, plain lines only).

## Recap habits

- Friday afternoon: "what did I do this week?", grouped by area, decisions first.
