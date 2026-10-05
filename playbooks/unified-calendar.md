---
title: unified-calendar
date: 2026-10-05
status: active
description: Playbook for one agenda built from every calendar a person has (several Google accounts, one or more Outlook tenants), with noise filtered out, each event tagged with an area by ordered rules, duplicates merged into one item, and a meeting prep that finds the relevant notes in the vault. Writes are dry runs by default; invitations only with approval; a written fan-out list keeps copies of one event in step.
---

# Playbook: every calendar in one agenda

## What you get

One view of your day and week, built from all your calendars: personal and work Google accounts, an Outlook calendar at work, another at a client or association. Coffee breaks and focus blocks are filtered out, every event carries its area (work, a client, family, a side project), the same meeting that appears in two calendars shows once, and for each meeting you get a short prep: who organises it, who attends, and the notes in your vault that belong to it.

Your daily briefing and planner read from this one agenda instead of each calendar separately.

## Before you start

- **Read access to each calendar.** Google: [`connect-google-workspace`](connect-google-workspace.md) (one token per account, calendar scope). Outlook: [`connect-microsoft-365`](connect-microsoft-365.md) (the official connector, or your own token for an extra tenant).
- **Your areas** and where their notes live ([`organise-your-knowledge`](organise-your-knowledge.md)).
- A vault index for the prep ([`kits/search`](../kits/search/README.md)); the prep works without one, but finds less.
- Python 3.9 or newer. About two hours for the first version.

## The shape of it

```
Sources, all pulled into ~/.paros/cache/calendar/agenda.json (derived, per machine, NOT in the vault):
  google:<account>   live, through your Google script
  outlook:<tenant>   live, through your own calendar token
  outlook:<tenant>   snapshot, saved by the main session's connector
<vault>/PAROS/calendar/
  agenda.py          pull, show, prep (written at adoption)
  rules.json         skip rules, area rules, de-duplication priority, area folders
  calendar.md        the recipe note: sources, freshness, fan-out list, learnings
```

The agenda file stays **outside the vault**: it contains personal events of other people (attendees, locations) and is rebuilt on every pull.

## Steps

### 1. List the calendars

**Agent:** lists every account and every calendar inside it (many accounts have several: primary, family, a team calendar, holidays), with who it is shared with. Shows you the list.

**You decide:** which calendars go into the agenda. Holiday and birthday calendars usually stay out.

### 2. Decide how each source is read

**Agent:** proposes per source:
- **live**, when a script with its own token can read it (Google through your Google script; an Outlook tenant through your own app registration and a separate calendar token);
- **snapshot**, when only the main session's connector can reach it (often your employer's Outlook): the main session searches the next 14 days and saves a small JSON file in a fixed shape (account, captured_at, window, events with id, subject, organizer, attendees, location, start, end, all-day, cancelled). The agenda then shows when the snapshot was taken.

**You decide:** live where possible. A snapshot is as fresh as the last time it was saved, and the agenda must say so.

### 3. Write the rules

**Agent:** drafts `rules.json` from your areas and your real calendar:

- **skip:** exact titles that are noise ("Coffee Break", "Focus time"), and cancelled events.
- **area tagging, in order, first match wins:**
  1. a keyword in the title, matched at the **start of a word** (so "mm" does not hit "summit");
  2. the organiser's email domain (`@acme.example` means the Acme area);
  3. the calendar's name or id (the family calendar means family);
  4. the source's default area.
- **de-duplication priority:** which source wins when one event appears in several calendars.
- **area folders:** for each area, the vault folders the prep may search.

**You decide:** you read the rules and correct the areas of a week of real events. That week of corrections is the best test set you will get.

### 4. Pull and merge

**Agent:** `agenda.py pull [--days 14]` reads all sources, normalises times to your time zone, applies skip and area rules, and merges duplicates: **same normalised title and same start time is one event**; the source with the higher priority stays, the others are listed in an `also_in` field, so you can see the meeting is in both calendars.

If you copy one event to several places on purpose (for example a team calendar, your personal calendar and a CRM), give the copies a shared key (an id in the event's private properties) and merge on that key too.

### 5. Show

**Agent:** `agenda.py show [--date D] [--days N] [--area A]`: one line per event, local time, area, title, location; a marker when it comes from a stale snapshot.

### 6. Prep

**Agent:** `agenda.py prep [--date D]`: for each meeting, the organiser, the attendees, and the vault notes that belong to it, found in this order:
1. **A path match in the event's area folders** (a folder or file name that contains a distinctive word of the title, for example a client name). This comes first because **an index is never complete**: a lead folder created yesterday may not be indexed yet.
2. The vault index: path, then full-text over title, description and tags.

Two filters keep the prep useful:
- words that are part of the area's own name do not count (they would match everything in that area);
- for meetings with more than about six attendees, attendee names are not searched (too much noise).

### 7. Connect the consumers

**Agent:** points the daily briefing ([`daily-briefing`](daily-briefing.md)) and any planner at `agenda.json`: today's events plus a "prepare for" section with the prep links.

### 8. Writing to calendars (only if you want it)

**Agent:** every write command (create, update, delete) is a **dry run by default** and shows what it would do; it writes only with `--apply` after your yes.

- **Invitations are messages.** Creating an event with attendees sends an invitation; deleting one as organiser sends a cancellation. Many calendar APIs cannot do this silently. Any write with attendees is a send, so it needs your explicit yes (P00).
- **The right account.** When signing in, pass the intended address as a login hint and refuse to save a token for a different address. The browser offers the account you used last.
- **A fan-out list.** If one kind of event must appear in several places (a course in a team calendar, your own calendar, a family calendar without client details, a CRM), write that list down once in the recipe note. When the event changes (time, place, cancelled), the agent updates every place on the list, found by the shared key. Never delete in a sync; mark as cancelled.

### 9. A check on the output

**Agent:** a health check that fails when a live source returns an error or a snapshot is older than your limit (for example two days), and adds one line to your task list (P11).

## Check that it works

1. Compare tomorrow in the agenda with each calendar app: every real event is there, noise is not.
2. A meeting that is in two calendars appears once, with `also_in`.
3. Ten random events: the area is right for at least nine. Fix the rules for the tenth.
4. The prep for a client meeting links to that client's notes, including a folder created today.
5. A dry-run create prints the event and writes nothing.

## Pitfalls

- **Prep that trusts only the index.** New notes are missed. Path match in the area folders first.
- **Keyword rules that match inside words.** Match at word start.
- **Area-name words in the prep search.** They match everything in the area.
- **Searching attendee names in a large meeting.** Noise.
- **A snapshot that looks live.** Always show its age.
- **The agenda inside the vault.** It holds other people's details and syncs everywhere; keep it in a local cache.
- **"Just add the meeting" with attendees.** That sends invitations.
- **The wrong Google account at sign-in.** Use a login hint and check the address.
- **Copies of one event without a shared key.** They drift apart, and the agenda cannot merge them.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): invitations and calendar writes are sends; never autonomous.
- [P06](../principles/P06-search.md): the prep searches your vault, path first, then index.
- [P07](../principles/P07-secrets.md): calendar tokens outside the vault, one per purpose.
- [P11](../principles/P11-health-contract.md): stale or failing sources are visible.
- [P12](../principles/P12-one-fact-one-owner.md): each event's owner is its calendar; the agenda is derived and rebuildable.

## Related

- Playbooks: [`daily-briefing`](daily-briefing.md), [`meetings`](meetings.md) (prep, recording, intake), [`connect-google-workspace`](connect-google-workspace.md), [`connect-microsoft-365`](connect-microsoft-365.md).
- Kits: [`google-workspace`](../kits/google-workspace/README.md), [`search`](../kits/search/README.md), [`health`](../kits/health/README.md).
