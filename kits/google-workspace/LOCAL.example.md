---
title: google-workspace LOCAL
date: 2026-10-05
status: active
description: Personal settings for the google-workspace kit (accounts, well-known files, time zone, write rules, which data goes through fetch and brief). Copy to LOCAL.md in your vault and replace every value.
---

# google-workspace: personal settings

> Example values, all fictional. Copy this file to `LOCAL.md` where your vault keeps the kit (for example `PAROS/kits/google-workspace/LOCAL.md`) and replace everything. No secrets here: the client secret and the tokens live in `$PAROS_SECRETS_DIR/google/`.

## Accounts

| `--account` | Used for | Default |
|---|---|---|
| `personal` | household budget, personal calendar | yes |
| `work` | team sheets, course forms, the shared work calendar | |

The expected sign-in email of each account is in `$PAROS_SECRETS_DIR/google/accounts.json`, not here.

## Well-known files

Agents use these names instead of searching Drive. An ID is not a secret, but it is private: keep this file in the vault, never in a public repository.

| Name | Account | Kind | ID | Write rule |
|---|---|---|---|---|
| Household budget | personal | sheet | `1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789example` | fetch and brief only; owner confirms every write |
| Course sign-ups | work | form | `1FormIdExample0000000000000000000000000000` | read freely; structure changes need a yes |
| Team planning | work | sheet | `1PlanningSheetExample000000000000000000000` | dry run shown, then `--apply` |

## Time zone

- `GAPI_TZ=Europe/Lisbon` for new events and calendars.

## Write rules

- Every write: dry run first, shown to me, `--apply` after my yes.
- Calendar events with other attendees: never `--notify` without asking.
- Never write to a file someone else owns unless I named it in this conversation.

## Scopes

- `personal`: full set.
- `work`: `GAPI_SCOPES=sheets,forms,forms-responses,drive-readonly,calendar` (no Drive writes from agents).
