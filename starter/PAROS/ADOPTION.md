---
title: ADOPTION
date: 2026-10-05
author: Alex Example
status: active
description: Filled example of a PAROS adoption checklist and log for the starter vault: status of each principle P00 to P12, what it means in this vault, the chosen kits, and a dated log.
id: bc70846c-1f99-4ac1-b8ef-b00d08225312
reference_version: 0.4.0
reference_path: ..
tags: [paros, adoption, example]
---

# PAROS adoption (example)

This is a **filled example**. In your own vault the advisor writes this file from your diagnosis (`../flows/4-adopt.md`), and every line reflects a decision you made.

## Checklist

| ID | Principle | Status | What it means for this vault |
|---|---|---|---|
| P00 | Constitution and boundaries | done | `AGENTS.md` lists the boundaries; price lists to cafes are drafted, never sent by the agent |
| P01 | Persistence | done | All knowledge is markdown with frontmatter; the dashboard holds nothing of its own |
| P02 | Presentation | done | `dashboard/` (minimal view kit, restyled): agent cards, search, tasks, freshness |
| P03 | Agent is a viewpoint | done | Three viewpoints: Librarian, Maestro, Alfred, defined in the reference |
| P04 | Thin entry, live definition | adapted | Entry is `AGENTS.md` plus `CLAUDE.md` (`@AGENTS.md`); agent definitions stay in the reference because this is a demo |
| P05 | Closed-loop learning | in progress | Packets go to `PAROS/observations/`; review by code not set up yet |
| P06 | Search | adapted | About fifteen notes: the dashboard's ranked search is enough; the index kit waits until the vault passes a few hundred notes |
| P07 | Secrets | not needed | No connectors, no secrets |
| P08 | Connectors | later | Maybe the bakery's order form, next year |
| P09 | Forgetting and archiving | done | `Archive/` with date and reason in the frontmatter |
| P10 | Backup and recovery | done | The vault is in git; a weekly copy to an external drive |
| P11 | Health contract | later | Health kit after the learning cycle |
| P12 | One fact, one owner | in progress | Prices live only in `Areas/Bakery/Pricing and costs.md`; the wholesale note links instead of copying the cost table |

Statuses: `present`, `to adopt`, `in progress`, `done`, `adapted` (with a reason), `later`, `not needed`.

## Skills and kits

| What | Status | Steps for this vault |
|---|---|---|
| `kits/view/node-minimal` | done | Copied to `dashboard/`, restyled with `tokens.css`, task file set to `TODO.md` |
| `kits/search` | later | When the vault grows past a few hundred notes |
| `skills/frontmatter-header` | to adopt | Run on new notes so every one gets a content description |

## Log

- 2026-09-01: diagnosis done, checklist approved, order: P00, P01, P09, P03, P04.
- 2026-09-03: `AGENTS.md` written with the boundaries (P00). Check passed: a fresh session refused to send the price list.
- 2026-09-05: frontmatter added to every note in two batches (P01).
- 2026-09-12: farmers market plan archived with reason (P09).
- 2026-09-20: minimal view adopted as `dashboard/` (P02).
- 2026-09-28: first learning packet written (P05): wholesale cutoff wording.
