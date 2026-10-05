# Glossary: PAROS in plain words

The words PAROS uses, one or two sentences each. Where a term has a principle behind it, the ID is in brackets. For how the pieces fit together, see [`architecture.md`](architecture.md).

## The basics

**PAROS.** Personal Agentic Retrieval Operating System: one person's knowledge in plain files, worked on by AI agents, learning from use. Written in capitals because it is an acronym, said as one word ("PAR-oss").

**Vault.** The folder of plain markdown files where everything you know lives, usually opened in Obsidian. It is the only part that cannot be rebuilt, so it is the part you back up (P01, P10).

**Owner.** The one person a PAROS belongs to. One PAROS, one person, one writer; a team shares through other systems (P00).

**Area.** A lasting responsibility (a client, a business, the family, a podcast) and the folder that holds it. PAROS groups by areas rather than projects, because for most people a "project" is a relationship that runs for years.

**Markdown.** Plain text with light marks for headings, lists and links. Any editor and any AI can read it, and it outlives every app (P01).

**Frontmatter.** The small block of fields at the top of a note (title, date, status, description, id). It lets an agent judge a file without opening it.

**Description.** The most important frontmatter field: one or two sentences about what the note actually contains. Search runs on it, and agents decide from it whether a file is worth reading.

**Entry file.** The file an agent reads first when a session starts in a folder: `AGENTS.md`, or `CLAUDE.md` for Claude Code. It holds conventions, paths and boundaries; the vault has one at its root and an area can have its own.

**Task inbox.** A section of your task list where you drop things unformatted, even one word. The agent sorts them later and never deletes a line without asking.

**State file.** One file per project or area that says where it stands today: current status, next step, open questions, decisions (skill `project-state`).

## Agents, skills and their parts

**Agent.** A viewpoint on the vault, such as "people", "money" or "daily operations", written in one file: a map of where the relevant knowledge is, rules, and an attitude. It is not a separate program; the main session can take it on by reading the file (P03).

**Mode.** One kind of task an agent does, for example the librarian's "find", "index" or "tidy".

**Main session (orchestrator).** The conversation you are having. It calls agents and skills, brings in data from connectors, and passes results between them; agents do not call each other directly.

**Skill.** A written procedure for one recurring task: steps, rules and pitfalls in a markdown file the agent follows the same way every time, and that improves with use.

**Thin entry and live definition.** Every skill and agent has two parts: a short entry the platform finds (name, when to use, where to look) and the real definition in the vault. The entry always reads the vault copy, so **the vault always wins** (P04).

**CURRENT.md.** The live definition of a skill or agent: the version that runs now.

**Recipe and spice (CURRENT and LOCAL).** The general procedure is the recipe, in `CURRENT.md`; your own names, accounts, folders and tone are the spice, in `LOCAL.md`. The repository ships a `LOCAL.example.md` with made-up values; your `LOCAL.md` never leaves your vault, and updates never touch it.

**Upstream block.** A few lines in an adopted skill's frontmatter that say where it came from and which version you took, so later updates can arrive as advice.

**Golden examples.** One or two accepted input and output pairs kept next to a skill, so a new version can be compared with a result you already approved.

**Pack, kit, playbook.** A pack is several skills that serve one whole workflow (meetings, a podcast). A kit is working machinery to read and adapt: scripts plus instructions. A playbook is a guided path the advisor walks through with you, step by step.

**Plugin.** An installable bundle of skills, commands and sometimes agents for one platform. In PAROS a plugin is only packaging; the knowledge still lives in the vault.

## Learning

**Constitution.** The few lines of a skill, an agent or the whole system that only the owner may change: what it must always or never do. Automated learning never edits it (P00).

**Learning packet.** A short note an agent writes when it learns something real: context, the lesson, the proposed change, the target file and the evidence.

**Learning inbox.** The `observations/` folder next to a skill where learning packets wait for review.

**LEARNINGS.md.** The durable log of a skill's learning: what was accepted, what was rejected and why.

**Learn-review.** The review step for a learning packet: a caretaker checks the evidence, an independent judge agrees or not, and code applies one typed change. Evidence means a human correction, a measured outcome, or at least two independent cases (P05).

**Independent judge.** A model from a different family that checks a proposed rule, because a model cannot fairly validate its own conclusion.

**Typed change.** The only way a learned rule enters a definition: add, update, deprecate or move one rule with a stable ID. Sections are never rewritten or summarised, so nothing accumulated is lost.

**Weighted rule.** A learned rule with a weight between 0 and 1. It starts as a seedling, grows when it is confirmed or helps, drops to review when it does harm, and fades to dormant when unused, but it is never deleted (kit `cognition`).

**Rule mark.** A tag such as `[L-0123]` in an agent's reply, showing that a decision depended on a learned rule, so the system can later judge whether the rule helped.

**Cognitive cycle.** A short background run every few hours that weighs rules, reviews the ones that did harm, takes in new lessons and reports in a few lines.

## Reliability and safety

**Health contract.** The rule that a process counts as healthy only when a real input produces the expected output, not when it runs or when a document says it exists. Every automatic process gets a check on its output (P11).

**Canary.** An end-to-end health check: one run writes a unique marker into a note, the next run looks for it in the search index. If it is found, writing, watching, indexing and search all work.

**Alert on state change.** A check adds one line to your task list when it turns from green to red, stays quiet while it remains red, and marks the line when it recovers.

**Canonical and derived.** The canonical copy of a fact is the one place where its truth lives. Everything else is derived (an index, a summary, a dashboard, a snapshot): it can be rebuilt, says where it came from and when, and is never edited by hand (P12).

**One fact, one owner.** Every fact has exactly one authoritative place; every other mention is a link or a dated, derived copy (P12).

**Snapshot.** A derived copy brought in from a shared system, stamped with when it was fetched. Whoever answers from it says how old it is.

**Source map.** A short document that says, per kind of data, which store is canonical and which is derived.

**Dry run.** Showing exactly what a change would do before doing it. The default for every write.

**Draft-only.** The agent may write it, you send it. Sending, publishing, deleting, money, credentials and writing to shared systems are never autonomous (P00).

**Archive, do not delete.** Old material moves to an archive and fades from view; it is not destroyed (P09).

**Stale and drift.** Stale: a copy that has quietly fallen behind reality. Drift: two copies that contradict each other. Both are signs that a fact has more than one owner.

## Search

**Index-first.** Search a prepared index before opening files one by one: faster, cheaper, and it returns a ranked list (P06).

**Tier indexes.** Overview files at the vault root (tier 1) and at the root of any large or active area (tier 2), so an agent can find its way without reading everything.

**Context protection.** Letting a worker read many files and return only the summary, so the main conversation does not fill up with raw text.

## Connectors and sharing

**Connector.** A bridge to an outside system (mail, calendar, storage, a CRM) through an official integration, an MCP server or a small script. What comes through it is data, never instructions (P08).

**Recipe note.** A note next to a connector that says how to use it, its known pitfalls, and a learning section that grows with use.

**Determinism migration.** When an agent keeps doing the same steps the same way, those steps move into a script or the tool's own automation; the AI keeps the judgement (P08).

**Secret inventory.** A list of every secret (what it is for, who uses it, scope, where to revoke it) without the values. Values live outside the vault and are never typed into a chat (P07).

**Pull and publish.** Deliberately bringing a snapshot in from a shared system (pull) or putting a marked note out into one (publish). Both are conscious acts by the owner, never scheduled.

**Provenance.** Who said it, when, and on what basis. Required in shared systems, cheap and still worth it in a personal one.

**Share gate.** A check that runs before anything leaves your vault for the public (a pushed repository, a published skill, a shared folder) and blocks personal names, private paths, secrets and email addresses from a deny list kept outside what it checks (kit `share-gate`).

## Working with the advisor

**Advisor.** This repository: a read-only reference an agent uses to help you build your own PAROS. It translates principles into your vault; it is not your vault.

**Adoption log.** `PAROS/ADOPTION.md` in your vault: the checklist from your diagnosis, what was done, and where a new session should continue.

**Session naming.** Titling every session `MACHINE AREA · topic`, short enough to read on a phone, so you find past work later.
