---
title: capture
status: active
description: Playbook for frictionless capture in a PAROS vault. Raw thoughts dropped into an append-only inbox (at the desk or from the phone) without structure, then sorted in a periodic sync ritual that proposes a route for each item and acts only after the owner's yes, with an audit trail of what went where. Built on the Alfred agent.
---

# Playbook: capture

Good ideas arrive on a walk, in the car, right after a call. A system only lives when you sit at the desk. Capture closes that gap: you drop anything, any time, in your own words, and nothing is lost. Sorting happens later, at a healthy rhythm, and only with your yes.

## What you get

- **A one-line way to drop a thought:** "capture: call the plumber about the back tap", or one word in the inbox of your task list. No questions, no format, no confirmation.
- **An inbox that is only appended to,** with a timestamp per line, in exactly the words you used.
- **An optional on-the-go channel:** a phone-friendly place you dictate into (a notes app, a chat, a voice memo folder), read at the next sync.
- **A sync ritual** that sorts each new item (task, idea, reminder, family, priority, mood, insight), proposes where it should go, asks once for the whole batch, then moves what you approved and logs every move.
- **Nothing deleted.** An item may become a task, a note in an area, a signal to another viewpoint, or simply archived. Never dropped.

## Before you start

| Piece | Status |
|---|---|
| The Alfred viewpoint with its `capture` and `sync` modes | exists in the repo: [`agents/alfred/CURRENT.md`](../agents/alfred/CURRENT.md) |
| Settings template (inbox path, scopes, capture channels) | exists in the repo: [`agents/alfred/LOCAL.example.md`](../agents/alfred/LOCAL.example.md) |
| A task list with an `## Inbox` section | example in [`starter/TODO.md`](../starter/TODO.md); yours is created or confirmed at adoption |
| `inbox.md`, the `routes/` audit folder, `state/last_sync.md` | written by the agent in your vault at adoption |
| A `capture` command or skill entry | written by the agent at adoption (thin entry, P04) |
| A phone capture channel | optional; you choose it, the agent only reads it |

## Steps

1. **Adopt Alfred** (if not already done for the [daily briefing](daily-briefing.md)). The agent copies the definition into your vault, installs the entry, and fills `LOCAL.md` with you: inbox path, scopes, and whether you want a phone channel. *You decide* the scopes and the channel.

2. **Create the inbox.** The agent writes `inbox.md` in Alfred's home folder with a frontmatter and one heading. That is all the structure it ever gets.

3. **Install the capture entry.** The agent writes a thin entry (P04) that does exactly this and nothing else:
   ```
   1. take the whole text as given
   2. timestamp it from local time
   3. append to inbox.md:  - [YYYY-MM-DD HH:MM] <text>
   4. reply: "Captured." plus the first 60 characters
   ```
   No routing, no questions, no confirmation: an append-only write that destroys nothing is the one write Alfred may do without asking.

4. **Try it.** Say "capture: oven service before November?" and "capture: idea, a loyalty card for the cafes". Open `inbox.md`: two timestamped lines, your words unchanged.

5. **Decide the other front door.** Many people also drop items into the `## Inbox` section of their vault task list, unformatted, even one word. *You decide* whether that inbox and Alfred's `inbox.md` are both used. If both: the sync reads both, and the task-list inbox follows its own rule: **a dropped line is never deleted without asking; it is moved**, leaving a one-line reference where it was.

6. **Set up the phone channel (optional).** *You choose* the channel: a dedicated note in a synced notes app, a chat you dictate into, or a folder of voice memos. The agent records it in `LOCAL.md`. At sync it reads new entries since the last sync (voice memos through the [`transcribe`](../skills/transcribe/SKILL.md) skill) and treats them exactly like inbox lines.

7. **Run the first sync.** Say "sync" (or let it run at the rhythm you choose). The agent:
   1. reads the inbox items added since the last sync, plus the phone channel;
   2. sorts each into a kind: idea, task, reminder, family, priority, mood, insight;
   3. proposes a route for each:
      ```
      [14:05] oven service before November?   -> task, scope bakery, due 2026-10-31   Go?
      [14:07] idea, a loyalty card for cafes  -> note in Areas/Bakery/ideas.md         Go?
      [18:40] tired today                     -> archive (mood, no action)            Go?
      ```
   4. **asks before any change;** you answer per item or "all yes except 2";
   5. executes only the approved routes, inside the vault;
   6. logs every move in `routes/<YYYY-MM>.md` (what, from where, to where, when);
   7. updates `state/last_sync.md`.

   *You decide* every route. The agent never scatters items silently.

8. **Choose a rhythm.** A sync two or three times a day works well (morning with the briefing, afternoon, evening), plus an opportunistic sync whenever you open your dashboard. *You decide* the rhythm; capture itself is always instant.

9. **Watch the backlog.** The `status` mode shows inbox size and the last sync. A backlog that keeps growing is a signal that the rhythm is wrong, not a reason to sort faster with less care.

## Check that it works

Proof, not "the command ran" (P11):

- Capture a unique marker ("capture: canary 7f3a"). `inbox.md` ends with that line and a correct timestamp.
- Run a sync and approve routing the canary to archive. The line appears in `routes/<YYYY-MM>.md` with its destination, and the inbox no longer lists it as new.
- If you use a phone channel: add an entry on the phone, run sync, and see it proposed with the phone named as its source.
- Search for the routed item (index first, P06). It is found in its new home.
- After a week: `state/last_sync.md` is recent, and the inbox has no items older than your rhythm allows.

## Pitfalls

- **Structuring too early.** Adding fields, tags or questions at capture time kills the lightness that makes people capture at all. Structure is born in the sync, never in the inbox.
- **Real-time mania.** Processing every item the moment it arrives leads to noise and fatigue. A few syncs a day are healthier.
- **A to-do factory.** Not every thought is a task. "Archived" is a perfectly good fate for an item.
- **Silent scattering.** Moving items into areas, task scopes or another viewpoint without a yes. The confirmation gate exists for exactly this.
- **Deleting dropped lines.** Something you dropped may look meaningless ("oven??") and still matter. Move and leave a reference; never remove without asking.
- **Guessing the scope.** If the text does not say where it belongs, ask one question. A wrong scope hides the task.
- **A forgotten phone channel.** A capture channel nobody reads is worse than none, because you trust it. The sync names every channel it read, and the health check covers the last sync time.
- **Private items travelling.** Family and health items stay in the personal scope. A signal to another viewpoint carries a reference, not the content, and only after your yes.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): the only unasked write is an append; every other move needs your yes.
- [P01](../principles/P01-persistence.md): the inbox and the route log are plain markdown.
- [P03](../principles/P03-agent-is-a-viewpoint.md): capture is part of the owner's viewpoint, not a separate app.
- [P09](../principles/P09-forgetting-and-archiving.md): archive, never delete.
- [P11](../principles/P11-health-contract.md): the canary capture and the last-sync check.
- [P12](../principles/P12-one-fact-one-owner.md): a routed item lives in one place; the route log points to it.

## Related

- Agent: [`agents/alfred`](../agents/alfred/CURRENT.md) (`capture`, `sync`, `todo`, `remind`, `status`).
- Playbooks: [`daily-briefing`](daily-briefing.md) (routed tasks show up there), `task-inbox` (the vault task list and its inbox), `recap-and-journal`.
- Skill: [`skills/transcribe`](../skills/transcribe/SKILL.md) for voice memos.
- Kits: [`kits/health`](../kits/health/README.md) (last-sync check), [`kits/search`](../kits/search/README.md).
- Guide: [`guides/daily-work.md`](../guides/daily-work.md).
