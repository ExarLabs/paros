---
title: Alfred LOCAL
date: YYYY-MM-DD
status: active
description: Personal settings for the Alfred viewpoint in this vault, with made-up example values: home folder, task scopes, the vault task list, task sources, mail accounts to triage, calendars, capture channels and briefing rhythm. No secrets.
---

# Alfred: local settings

> Copy this file to `LOCAL.md` next to the adopted `CURRENT.md` and replace the example values with yours. Identifiers and preferences only: **never a password, token or key**. `CURRENT.md` reads this file; updates from the PAROS reference never touch it.

## Owner

- Name used in drafts and greetings: `Sam`
- Language of replies and briefings: English
- Draft reply tone: short, warm, first name, no exclamation marks

## Home and stores

| Setting | Value |
|---|---|
| Home folder | `Areas/Personal/Alfred/` |
| Inbox | `Areas/Personal/Alfred/inbox.md` |
| Task store | `Areas/Personal/Alfred/todos/` |
| Dossiers | `Areas/Personal/Alfred/tasks/` |
| Vault task list (read every briefing) | `TODO.md` |
| Daily notes | `DailyNotes/YYYY/YYYY-MM-DD.md` |
| Activity record for recap | `PAROS/reports/` (daily `YYYY-MM-DD.md`, monthly `YYYY-MM.md`) |

## Scopes

| Scope | What belongs there |
|---|---|
| `personal` | Health, errands, learning |
| `family` | Household, school, birthdays |
| `bakery` | The small food business the owner runs |
| `consulting` | Client work and proposals |
| `podcast` | The weekly show |

## Task sources (seed for the source register)

Alfred discovers more on its own; these are the starting points.

- `Areas/*/TASKS.md` (only items assigned to the owner)
- `Areas/*/01_PROJECT_STATE.md` (next actions)
- `Meetings/` notes from the last 7 days (open checkboxes)
- Excluded: `Archive/`, `Templates/`

## Mail accounts to triage

Read through the main session's connectors. Names only, never credentials.

| Label | Kind | Triage | Notes |
|---|---|---|---|
| personal | Gmail | yes | family and personal mail |
| work | Outlook | yes | client mail; attachments matter |
| old | IMAP | weekly | mostly newsletters |

Skip senders or patterns: newsletters, receipts, `no-reply@*`, calendar notifications.

## Calendars

- `Personal` and `Work`, both read-only for the briefing.

## Capture channels

- Vault: the inbox above.
- On the go: a chat titled `Alfred Inbox` that the owner dictates into from the phone; read at sync time.
- Idea channel (optional, for harvest): none yet.

## Rhythm

| When | What |
|---|---|
| 07:00 | today (briefing) |
| Hourly, 08:00 to 20:00 | triage, unattended (dossiers only) |
| 13:00 and 19:00 | sync (interactive) |
| Every 3 days | remind the owner that bookkeeping is due (Moneto executes) |

## Privacy

- Family details never leave the `family` scope without a yes.
- People signals to Iris carry a reference only for health or private-life topics.
