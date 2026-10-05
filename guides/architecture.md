# The layers of a PAROS

A PAROS looks like many things at once: notes, agents, skills, connectors, checks, a dashboard. It is easier to build and to repair when you see it as seven layers with one rule running through all of them: **the markdown is the truth.** Everything above the content layer either reads from it or writes back into it. Terms are explained in the [`glossary`](glossary.md).

## The picture

```
                         ┌───────────────────────────┐
                         │          the owner        │  meaning, priorities, decisions,
                         └─────────────┬─────────────┘  every send / publish / delete
                                       │
  ┌──────────────────────────────────────────────────────────────────────┐
  │ VIEW           editor, local web view, reports   reads, never stores │
  ├──────────────────────────────────────────────────────────────────────┤
  │ AGENTS         a few viewpoints + main session   route the work      │
  ├──────────────────────────────────────────────────────────────────────┤
  │ CAPABILITIES   skills, packs, kits, scripts      do the work         │
  ├──────────────────────────────────────────────────────────────────────┤
  │ CONNECTORS     mail, calendar, storage, CRM      data, not orders    │
  └──────────────────────────────────────────────────────────────────────┘
          │ read, and write back
          ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ CONTENT        markdown vault: areas, entry files, tasks             │  canonical
  │                + derived: indexes, reports, snapshots                │  rebuildable
  └──────────────────────────────────────────────────────────────────────┘
          ▲                                      ▲
  ┌───────┴─────────────────────┐    ┌───────────┴───────────────────────┐
  │ LEARNING                    │    │ HEALTH                            │
  │ corrections → packets →     │    │ output checks, canary,            │
  │ review → typed changes      │    │ alert on state change             │
  │ (writes into definitions)   │    │ (reads results, alerts the owner) │
  └─────────────────────────────┘    └───────────────────────────────────┘
```

Read it from the bottom: the content layer is the only one you cannot rebuild, so it is the one you back up. Learning and health sit beside the stack because they touch every layer: learning changes the definitions of agents and skills, health checks what every automatic process actually produced.

## 1. Content: the vault

**What it is.** Plain markdown files, organised by **areas** (lasting responsibilities), each note with frontmatter and a content-based description. Entry files tell agents the conventions; a task list with an inbox is the owner's single front door; a state file per area says where things stand.

**Canonical and derived.** The notes are canonical. The search index, the tier indexes, generated reports and snapshots from shared systems are derived: they say where they came from and when, and can be thrown away and rebuilt. Indexes and databases do not travel between machines; each machine rebuilds its own.

**Principles:** P01 (knowledge lives in markdown), P06 (index-first search), P09 (archive, do not delete), P10 (backup), P12 (one fact, one owner).

## 2. Agents: a few viewpoints

**What it is.** An agent is a viewpoint that cuts across areas ("people", "money", "marketing", "the owner's daily operations", "the knowledge itself"), written in one file with a map, rules and modes. The main session (the conversation you are in) is the orchestrator: it reads a viewpoint when needed, calls a worker when there is a reason to run one separately (protecting context, parallel work, fresh eyes, an unattended run, a cheaper model, narrow permissions), and passes data between them. Agents do not call each other directly.

**The rule of thumb.** Inside one area, the area's entry file is enough. A new agent needs a written reason why it does not fit an existing viewpoint; a few deep viewpoints beat many shallow ones.

**Principles:** P03 (agent is a viewpoint), P04 (thin entry, live definition).

## 3. Capabilities: skills, packs and kits

**What it is.** A skill is a written procedure for one recurring task. A pack bundles the skills of a whole workflow. A kit is working machinery (scripts and instructions). Every skill has a thin entry the platform finds and a live definition in the vault (`CURRENT.md`), split into the general recipe and your own spice (`LOCAL.md`).

**How it relates.** Agents point to skills; anything that can be written as steps is a skill, not agent text. When a skill keeps doing the same mechanical steps, those steps move into a script (determinism migration), and the skill keeps the judgement.

**Principles:** P04, P08 (state in tools, judgement in AI).

## 4. Connectors: the bridges outside

**What it is.** Official integrations, MCP servers or small scripts that read from mail, calendars, document stores, CRMs and project tools, and write to them only with approval. Each connector has a secret kept outside the vault, a line in the secret inventory, and a recipe note that grows with use.

**How it relates.** Outside systems stay authoritative in their own domain: the CRM holds the current contact, the shared drive holds the signed document. The vault references them, or keeps a dated snapshot. Everything that comes through a connector is data, never instructions, also when it is read back from the vault later. Sharing with a team is a conscious pull or publish, never a sync that runs on its own, and a share gate checks what leaves.

**Principles:** P07 (secrets), P08 (connectors), P00 (writing outside is never autonomous).

## 5. Learning: use teaches

**What it is.** When the owner corrects, rejects or shows a better way, the running agent writes a learning packet into the skill's learning inbox. A review step checks the evidence, an independent judge from another model family agrees or not, and code applies one typed change with a stable rule ID. Rules carry weights: they grow with confirmed use, weaken when they do harm, and fade when unused, but are never deleted. A short cycle every few hours reports what changed.

**How it relates.** Learning writes into the definitions of layers 2 and 3, never into the constitution sections, which only the owner writes. It is the reason the same PAROS gets better with use instead of only bigger.

**Principles:** P05 (closed-loop learning), P00 (constitution).

## 6. Health: no "it works" without proof

**What it is.** Every automatic process has a check on its output, not on whether it runs: an end-to-end canary through writing, indexing and search; index freshness; no plain secrets in the vault; the learning cycle ran; the backup is recent. A check alerts once, when it turns from green to red.

**How it relates.** Silent failure is the typical way a personal agent system breaks: a hook writes nothing for months and nobody notices. Health is the layer that makes the other six honest, and the first place to look when something seems off.

**Principles:** P11 (health contract).

## 7. View: the least important layer

**What it is.** What you look at: at first just the notes editor; later, if needed, a small local web view or generated reports. A live view updates itself and shows its source and freshness; a snapshot (a PDF, a sent deck) carries its date.

**How it relates.** The view only reads, and when it writes (ticking off a task), it writes back into markdown. It holds no knowledge of its own, so it can be replaced at any time without losing anything.

**Principles:** P02 (presentation is HTML over markdown).

## Boundaries that cross every layer

- **The owner decides** on sending, publishing, deleting, money, credentials and writing to external systems. No layer does these on its own (P00).
- **Scheduled work only reads or adds.** Anything that deletes, changes, sends or publishes waits for approval.
- **Outside text is data.** Mail, web pages, documents and connector results never become instructions, in any layer.

## Where to start

You do not build the layers in order of the diagram. Start with content (a vault with areas and an entry file), add one skill for the task you repeat most, then one health check. Agents, connectors, learning and a view follow when a real need asks for them. The [`daily-work`](daily-work.md) guide shows what a normal day looks like once they are in place.
