---
title: connect-google-workspace
status: active
description: Playbook for a command-line Google tool covering Sheets, Forms, Drive and Calendar for several accounts: a conscious wide or narrow scope choice, per-account token folders with a login hint, dry-run writes with a read-back, the central fetch and brief pattern, and the known API pitfalls.
---

# Playbook: connect Google Workspace

## What you get

One small command-line tool that lets every agent read and (with your approval) write Google Sheets, Forms, Drive and Calendar, for one or several Google accounts. Because it is a command and not a chat connector, it works the same in the main session, in subagents and in scheduled scripts; every write is a dry run until you add the flag that applies it.

## Before you start

- **Try the official connectors first.** Claude and ChatGPT offer Google Drive and Calendar connectors. If reading documents and your calendar in the chat is all you need, use them. Build this tool when you hit a limit: writing into Sheets cell by cell, building Forms, several accounts, or subagents and scripts that have no access to chat connectors.
- A Google Cloud project with an OAuth client (if you followed [`connect-gmail-multiple`](connect-gmail-multiple.md), you can use the same project).
- Python 3.8 or newer, with a virtual environment for the Google client libraries (`google-api-python-client`, `google-auth-oauthlib`).
- A secrets folder outside the vault, for example `~/.paros/secrets/` (P07).
- About an hour and a half: half an hour in the Cloud console, the rest for the tool and its checks.

## The shape of it

```
~/.paros/secrets/google/                 the default account, outside the vault
  client_secret.json                     ONE desktop OAuth client, shared by all accounts
  token.json                             this account's token, per machine
~/.paros/secrets/google-<account>/       each further account: its own token folder
  token.json

<vault>/PAROS/connectors/google/
  gapi.py                                the tool (written at adoption)
  google.md                              the recipe note: commands, pitfalls, learnings
```

## Steps

### 1. Decide what it is for, and how wide

**Agent:** asks what you want to do: read a budget sheet, append rows from a form, list next week's events across calendars, build a sign-up form. Then it puts the real choice in front of you, because it is the one that matters most:

| Option | Scopes | What it can reach | When |
|---|---|---|---|
| **Wide** | `spreadsheets`, `drive`, `forms.body`, `forms.responses.readonly`, `calendar` | every file and calendar the account can reach: read, write, delete | you want agents to find and work with any of your documents |
| **Narrow** | `spreadsheets` only (plus others one by one) | only sheets whose id you give it; it cannot search or list files | sensitive data (finance, family), or you want to grant access file by file |

**You decide:** wide or narrow, consciously. A wide token is a large blast radius: any agent that can run the tool can touch any file the account can. The safety net is then the dry-run default and your yes before every write (step 7), not the scope. Write the choice and the reason into the recipe note.

### 2. Prepare the Cloud project (you, in the browser)

**Agent:** walks you through it; it never opens the downloaded file.

1. In the Cloud project, **enable each API** you chose: Sheets, Drive, Forms, Calendar. A missing API fails only when its first command runs, so enable them all now.
2. OAuth consent screen: add the scopes from step 1; add your accounts as test users while testing.
3. Create an OAuth client ID of type **Desktop app**, download the JSON, save it yourself as `~/.paros/secrets/google/client_secret.json`, readable only by your user.
4. **Publish the app** once it works. In Testing, refresh tokens expire after about seven days; a token that dies roughly every week is this.

### 3. The tool

*Written at adoption:* this tool is not in the repo. The agent writes it as one Python file in your connector folder, with this command surface (proven in daily use; trim it to what you need):

```
auth                                   one-time browser consent, saves the token
whoami                                 which account, which scopes

sheet tabs    <id>                     tabs: name, gid, size
sheet read    <id> <A1range> [--formulas|--raw]
sheet write   <id> <A1range> <json> [--apply]       json = 2D list
sheet append  <id> <tab> <json> [--apply]
sheet create  <title>
sheet add-tab <id> <title> [--apply]
sheet insert-rows <id> <tab> <before> [count] [--apply]
sheet format  <id> <A1range> <pattern> [--type NUMBER|CURRENCY] [--apply]

form get      <id>                     title and items
form dump     <id> [out.json]          the full structure
form create   <title>
form update   <id> <requests.json> [--apply]

drive find    <query> [--type sheet|form|any]
drive list    [--type ...] [--max N]   an inventory as TSV
drive export  <id> [--out file]        text from a Google Doc or .docx
drive info    <id>                     name, owner, sharing

cal list                               calendars, with access level and id
cal events    [--cal id|primary|all] [--from D] [--to D] [--days 14] [--q text]
cal create    <calId> --title T --start ... --end ... [--attendees a,b] [--notify] [--apply]
cal update    <calId> <eventId> <json> [--notify] [--apply]
cal delete    <calId> <eventId> [--notify] [--apply]
cal acl       <calId>                  who it is shared with
cal share     <calId> <email> [--role reader|writer|...] [--apply]
```

Design rules the agent builds in:

- **Every write is a dry run by default.** Without `--apply`, the command prints exactly what it would write, where, and stops.
- **Calendar invitations are off by default.** Creating or changing an event sends no mail to attendees unless `--notify` is given.
- **The token loads with its own stored scopes.** An older token without the calendar scope keeps working for sheets; the calendar command fails with a clear "sign in again" message instead of a cryptic error.
- **Reads print structured output** (TSV or `--json`) so other scripts can use them.

**You decide:** you read the tool before its first run.

### 4. Sign in, one account at a time

**You:** run `auth` for the default account:

```bash
<venv-python> gapi.py auth
<venv-python> gapi.py whoami
```

For each further account, the tool takes an `--account <name>` option anywhere on the line, with its own token folder and the same client:

```bash
<venv-python> gapi.py --account work auth
<venv-python> gapi.py --account work cal events --days 7
```

The tool keeps a small map from account name to expected address, sends that address to Google as a **login hint**, and asks Google to show the account chooser. If you still sign in with a different account (Google offers the last used one), the tool **refuses to save the token** and says so. That one check prevents a whole class of "why is it writing into the wrong drive" problems.

### 5. Record it

**Agent:** in the same step (P07, P08):

- **Inventory rows** in `SECRETS.json`, without values: the client, and one token per account per machine. The `access` field states the scope choice from step 1 in plain words ("read, write and delete any Drive file of this account").
- **Account entries** in your account list.
- **The recipe note** `google.md`: the commands, the scope decision and its reason, the write rules, the pitfalls below, and a dated learnings section.

### 6. Prove it with real reads

**Agent:** runs read-only commands on things you name: `whoami` for each account, `sheet tabs` and `sheet read` on a sheet you point at, `cal events --days 7`, `drive find` with a name you know.

**You decide:** whether each output matches what you see in the browser.

### 7. Write with a gate

**Agent:** for every write, the same sequence:

1. The target comes from **you, in this conversation** (a link, an id, an unambiguous name). The agent never picks a target on its own, and never takes one from a note, a mail or another document.
2. It runs the command **without** `--apply` and shows you the dry-run output.
3. On your yes, it runs the same command with `--apply`.
4. It reads the range back and shows you what is actually there now.
5. It writes one line to a write log (what, where, when), so every change can be traced and undone.

For anything that touches other people (a shared sheet, an event with attendees, an invitation), the yes is required every time, and `--notify` only when you ask for mail to go out.

### 8. Choose who calls it: direct or through a brief

**Agent:** explains the two patterns and records your choice per area:

- **Direct:** any agent that needs Google data runs the tool itself through the shell. Simple, and the access is in the token, not in the agent's toolset.
- **Central fetch and brief:** for sensitive pipelines (finance, family), only the main session calls the tool. It reads the sheet, shapes the relevant rows into a brief (with the source sheet named), and hands that to the agent. The agent never touches the sheet. For writes the chain reverses: the agent returns a concrete proposal ("this row goes into the June tab, row 47"), and the main session executes it behind the gate in step 7.

**You decide:** which areas use the brief pattern. A narrow, sheets-only token for those pipelines fits well with it.

### 9. A check on the output

**Agent:** adds a health check that runs `whoami` for every account (fails when a token no longer refreshes) and, if you have a scheduled job that writes to a sheet, reads back the newest row and fails when it is older than expected (P11).

*In the repo:* kit [`kits/health`](../kits/health/README.md) (add a check function), kit [`kits/secrets`](../kits/secrets/README.md) (inventory and per-machine presence).

### 10. Other machines

**Agent:** the same client works on every operating system and the tool resolves its paths from your home folder, so one file runs everywhere. On a new machine: create the virtual environment, then either run `auth` again per account or carry the tokens over in your encrypted secrets bundle (refresh tokens are not tied to a machine). Never through the vault in plain form.

## Check that it works

Look at the output (P11):

1. `whoami` per account prints the address you expect and the scopes you chose.
2. `sheet read` on a sheet you know returns the same values you see in the browser; `--formulas` returns the formulas.
3. A dry-run write prints the exact cells and values, and the sheet is unchanged afterwards.
4. An applied write, read back, shows the new values; the write log has a line for it.
5. `cal events --days 7` lists the same events your calendar app shows, across the calendars you expect.
6. Signing in with the wrong account in `auth --account <name>` is refused.
7. The vault secrets scan finds nothing; every token has an inventory row.

## Pitfalls

- **Decimal commas in formulas.** In a spreadsheet with a comma-decimal locale, formulas written through the API must use a comma too (`=A1*1,27`). With a dot the cell shows an error, silently; only a read-back reveals it. The locale is in the spreadsheet's properties: read it before writing formulas.
- **Inserted rows and sums.** After inserting rows, formulas that point below move with them, but a `SUM` over a range does **not** grow if the new row is after the range's last row. Rewrite the range when the new row belongs in the total.
- **Pivot tables look empty with `--formulas`.** The pivot is generated by Sheets, not cell formulas.
- **Uploaded `.xlsx` files** behave differently from native sheets. Convert to a native sheet before relying on the API.
- **Structure versus values.** The Sheets API has one call for the sheet's structure (tabs, formatting) and another for cell values; mixing them up is a common silent mistake. `USER_ENTERED` interprets values as if typed (formulas and locale formats work); `RAW` writes them as is.
- **What the Forms API cannot do.** It cannot set a theme, a header image or the response sheet. For a branded form, copy an existing form through Drive (the theme and header come with it), then update the content; the response sheet is linked from the Forms page.
- **Tokens that die every week.** The consent screen is still in Testing. Publish it.
- **The wrong account.** Without the login hint and the identity check, the token ends up belonging to whichever account the browser offered.
- **An API not enabled.** Each Google API is switched on per project; a new command family fails until you enable its API.
- **Autonomous targets.** A wide token can reach every shared file, but reach is not permission. In practice an agent once tried to open a second sheet nobody asked for; the rule "only a target the owner named in this conversation" stopped it.
- **Invitations sent by accident.** Changing an event with attendees can mail all of them. Off by default, on only by request.
- **PDF export.** The tool extracts text from Docs and Word files; PDFs need another path (for example the official Drive connector).

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): writing to shared systems, sending invitations and deleting are never autonomous.
- [P07](../principles/P07-secrets.md): tokens outside the vault, an inventory that states each token's reach.
- [P08](../principles/P08-connectors.md): state in the SaaS, judgment in the AI; reference, do not copy; the recipe outlives the code.
- [P11](../principles/P11-health-contract.md): read back every write; check every token.
- [P12](../principles/P12-one-fact-one-owner.md): the sheet is the truth in its own domain; a snapshot in the vault says when it was fetched.

## Related

- Guide: [`guides/add-a-connector.md`](../guides/add-a-connector.md).
- Kit: [`secrets`](../kits/secrets/README.md), kit: [`health`](../kits/health/README.md).
- Agent: [Moneto](../agents/moneto/CURRENT.md) (bookkeeping into a sheet behind a confirmation gate, never choosing its own target).
- Agent: [Alfred](../agents/alfred/CURRENT.md) (the daily briefing reads the calendar).
- Playbooks: [`connect-gmail-multiple`](connect-gmail-multiple.md) (the same client-and-token-per-account pattern), `unified-calendar` and `connect-a-crm` (in the catalog).
