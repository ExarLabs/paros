---
title: connect-your-email
date: 2026-10-10
status: active
description: Router playbook for the common first request "connect my email". The agent asks which account (personal or work; Gmail, Microsoft 365, outlook.com or another provider; one account or several), then sends you to the right playbook (connect-gmail-multiple, connect-microsoft-365, connect-any-mailbox), with the IT check for work accounts and read-only access first.
---

# Playbook: connect your email (start here)

"Connect my email" is one of the most common first requests, and the right first move is a question, not a connector. Gmail, a work Microsoft 365 account, a personal outlook.com address and a mailbox at your own domain each take a different route. This short playbook asks, then hands over to the playbook that fits.

## What you get

- The right route for **each** of your mailboxes, chosen in a few questions.
- A short list of your accounts, so later playbooks (triage, briefing, calendar) know what exists.
- Read access first everywhere; sending only later, per purpose, and never without your yes.

## Before you start

Nothing to install. Have at hand: the addresses you want connected, and for a work account, whether you know who your IT contact is.

## Steps

### 1. Which accounts?

**Agent:** asks, in one message, in your language:

1. Which addresses do you want your agent to read? (List them; one or several.)
2. For each: is it **personal** or **work** (an organization, school, client, association)?
3. Who provides it, if you know: **Gmail or Google Workspace**, **Microsoft** (Outlook, Office 365, outlook.com, hotmail.com), or **something else** (your own domain, a hosting provider, another webmail)?

If you do not know the provider, the agent can tell from the address or from the mail settings page you see in your webmail. It never asks for a password here.

**You decide:** the list. Anything you leave out stays out.

### 2. One route per account

**Agent:** maps each account to a playbook and shows you the table before doing anything:

| The account | The route |
|---|---|
| One Gmail account, personal or Google Workspace | the official Gmail connector of your AI app; the start of [`connect-gmail-multiple`](connect-gmail-multiple.md) covers it |
| Two or more Gmail accounts | [`connect-gmail-multiple`](connect-gmail-multiple.md) |
| A work or school Microsoft 365 account | [`connect-microsoft-365`](connect-microsoft-365.md), **after the check with IT** in that playbook |
| A personal Microsoft account (`@outlook.com`, `@hotmail.com`, `@live.com`) | [`connect-any-mailbox`](connect-any-mailbox.md) (IMAP); check there whether an app password still works or a modern sign-in is required |
| Your own domain, a hosting provider, any other webmail | [`connect-any-mailbox`](connect-any-mailbox.md) |
| A Google Workspace account of an organization | as Gmail, but ask IT first, like a Microsoft work account: many organizations restrict which apps may read mail |

An example answer for someone with three mailboxes:

```
a gmail.com address             personal, Gmail        -> official Gmail connector
anna@bakery.example             work, Microsoft 365    -> connect-microsoft-365 (ask IT first)
anna@family-name.example        personal, own domain   -> connect-any-mailbox
```

**You decide:** the order. Start with the account you read most; one working account is worth more than three half-connected ones.

### 3. Work accounts: ask before connecting

**Agent:** for every work account, points out that the organization may require an administrator's approval ("Admin approval required") and offers the request template from [`connect-microsoft-365`](connect-microsoft-365.md). You send it yourself. If the answer is no, that account stays out, and the decision is noted so nobody asks again.

### 4. Hand over

**Agent:** opens the chosen playbook for the first account and follows it from its first step. When that account works, it comes back to this table for the next one.

### 5. Record it

**Agent:** keeps one list of all accounts (`PAROS/connectors/accounts.md`: address, kind, route, read or write, connected on), each secret outside the vault with an inventory row without its value (P07). The connector playbooks fill in the details.

## Check that it works

1. Every address you named has a route in the table, or a recorded reason why it stays out.
2. For each connected account, the agent lists the three newest subjects, and they match what you see in your mail app.
3. `accounts.md` lists every account once, and no password or token appears in the vault.

## Pitfalls

- **Picking a connector before knowing the account.** A personal outlook.com address and a work Microsoft 365 account look alike and need different routes.
- **Connecting a work account before asking IT.** Expect "Admin approval required"; ask first.
- **Everything at once.** Connect one account, check it, then the next.
- **Write access on day one.** Read first; sending comes later, per purpose, with your yes.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): nothing is sent, and no request goes to IT, without you.
- [P07](../principles/P07-secrets.md): secrets outside the vault, inventory rows without values.
- [P08](../principles/P08-connectors.md): the official connector first, your own route only at its limit.

## Related

- Playbooks: [`connect-gmail-multiple`](connect-gmail-multiple.md), [`connect-microsoft-365`](connect-microsoft-365.md), [`connect-any-mailbox`](connect-any-mailbox.md), then [`email-triage`](email-triage.md) and [`daily-briefing`](daily-briefing.md) once mail is readable.
