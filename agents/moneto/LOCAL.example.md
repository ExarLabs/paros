---
title: Moneto LOCAL
date: YYYY-MM-DD
status: active
description: Personal settings for the Moneto viewpoint in this vault, with made-up example values: the organisations it follows and where their methodology notes live, their financial sources, the household bookkeeping playbook, ledger and undo journal, and the reconciliation target. No secrets.
---

# Moneto: local settings

> Copy this file to `LOCAL.md` next to the adopted `CURRENT.md` and replace the example values with yours. Identifiers and preferences only: **never an account number, password, token or key**. `CURRENT.md` reads this file; updates from the PAROS reference never touch it.

## Currency and language

- Reporting currency: EUR (convert others at the statement date's rate; say which rate)
- Language of notes: English

## Organisations

| Organisation | Area | Methodology note | Main sources |
|---|---|---|---|
| Bakery | `Areas/Bakery/` | `Areas/Bakery/Finance/Methodology.md` | point-of-sale monthly export (CSV), supplier invoices folder |
| Consulting | `Areas/Consulting/` | `Areas/Consulting/Finance/Methodology.md` | expenses spreadsheet "Consulting Expenses 2026" (tabs per month) |
| Client: Riverside Shop | `Areas/Clients/Riverside/` | `Areas/Clients/Riverside/Finance.md` | standard audit file export, quarterly |
| Household | `Areas/Personal/Finance/` | `Areas/Personal/Finance/Methodology.md` | bank statements (PDF), the household ledger |

Known distortions to carry forward (examples):

- Bakery: the point-of-sale export aggregates quantities per day, so per-item cost of goods is an estimate.
- Riverside Shop: stock transfers between shops appear as sales; exclude them from margin.

## Household bookkeeping

| Setting | Value |
|---|---|
| Playbook | `Areas/Personal/Finance/BOOKKEEPING_PLAYBOOK.md` |
| Statement source | PDF statements dropped into `Areas/Personal/Finance/inbox/` |
| Ledger | spreadsheet "Household Budget", one tab per month |
| Undo journal | `Areas/Personal/Finance/undo/` |
| Earmarked amounts | 10% of income routed to the "Giving" category |
| Reconciliation target | difference between ledger balance and statement balance = 0.00 |
| Cadence | every 3 days (Alfred reminds) |

Categories live in the playbook, not here.

## Access

- Spreadsheets are read and written through the main session's sheet tool, by name. Moneto never handles the credential.
- Write permission: only the household ledger and the Consulting expenses spreadsheet. Everything else is read-only.
