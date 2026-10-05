# PAROS Advisor

**Personal Agentic Retrieval Operating System** (say it "PAR-oss").

**An advisor engine for building your own PAROS: a minimal, cognitive operating system that adapts to you.**

This repository is not PAROS itself. PAROS is what grows in *your* vault. This is the advisor that helps you build it: it explains the ideas, diagnoses your vault, writes you a personal guide, helps you adopt principles, skills and agents one step at a time, and answers your questions later (how to connect a new tool, how to turn a routine into a skill, how to work day to day).

PAROS is a way to turn a plain folder of markdown notes (an Obsidian vault, for example) into a personal operating system that AI agents work in: they find things, keep order, learn from every correction you make, and connect your personal knowledge with the tools you share with other people.

The name is the idea:

| Letter | Meaning | What it claims |
|---|---|---|
| **P**ersonal | one person | One PAROS belongs to one person. One writer, private by default. |
| **A**gentic | agents work in it | Not just storage: agents read, search, organise, and learn. |
| **R**etrieval | the mechanism | Knowledge is worth what you can bring back at the right moment. Frontmatter, descriptions and indexes all serve this. |
| **OS** | a layer, not an app | Every area of your life and work builds on the same layer. |

## If you are an AI agent reading this

Someone sent you here to set up PAROS for them. Do this:

1. Clone this repository **outside** their vault (for example `git clone https://github.com/ExarLabs/paros-advisor.git ~/paros-advisor`), or `git pull` if it is already there.
2. Work in **their** vault folder (ask which one if it is not your current directory).
3. Read [`AGENTS.md`](AGENTS.md) and follow it. Start with the tour, then offer the diagnosis. The tour and the diagnosis are read-only and can run without asking; anything that changes their vault needs their yes.

## This repository is an advisor, not a template

**Nobody uses this repository as the root of their vault, and nobody writes into it.** You download it next to your vault, point an AI agent at it, and the agent becomes your PAROS advisor: it explains the ideas, diagnoses your current vault, writes you a personal guide, and helps you adopt the principles one step at a time, on your terms.

Why this way:
- **No merge conflicts.** Every vault is different: areas, habits, machines, tools. If this repo were your base, every update would fight your own changes.
- **Updates are advice, not overwrites.** When a principle is added or refined, your agent reads what changed and suggests what is worth adopting. You decide.
- **The principle is the asset, not the code.** Scripts are disposable and can be regenerated. What lasts is the principle, the reason behind it, and the way to check it.
- **It gets more valuable the more people use it.** These are lessons learned from running a real PAROS daily. Use them, adapt them, and tell us what you learn.

## Quick start

1. Download the repository somewhere **outside** your vault:
   ```bash
   git clone https://github.com/ExarLabs/paros-advisor.git ~/paros-advisor
   ```
2. Open your vault folder (an existing one, or a brand new empty folder).
3. Start an AI agent in that folder (Claude Code, OpenAI Codex, or any agent that reads `AGENTS.md`) and say, in any language:
   > There is a reference system at `~/paros-advisor`. Read its `AGENTS.md` and be my PAROS advisor.
4. The agent will walk you through it step by step:
   - **Tour:** what PAROS is and why it works this way.
   - **Diagnosis:** where your vault stands today, principle by principle.
   - **Personal guide:** your vault explained, with what to change, why, and which principle is behind it.
   - **Adoption:** a checklist written into your vault, done one item at a time, with your approval.
   - **Advice, any time later:** how to add a connector, a skill, how to work day to day.
5. To update: `git pull` in `~/paros-advisor`, then tell your agent: "Check what is new in PAROS."

## What is inside

| Where | What |
|---|---|
| [`AGENTS.md`](AGENTS.md) | The agent's entry point on every platform. `CLAUDE.md` imports it. |
| [`flows/`](flows/) | What the agent does: tour, diagnosis, personal guide, adoption, advice, upgrade. |
| [`principles/`](principles/README.md) | The principles, one file each: the principle, why, practice, how to check, how to adopt. |
| [`tools/diagnose.py`](tools/diagnose.py) | A dependency-free scanner that measures a vault against the principles. Read-only. |
| [`guides/`](guides/) | Practical how-tos: add a connector, add a skill, daily work. |
| [`templates/`](templates/) | Starting points for your vault: entry file, frontmatter, skill definition, adoption checklist. |
| [`starter/`](starter/README.md) | A small demo vault with fictional areas, three agents and a dashboard: open it to **see** PAROS working before you build your own. |
| [`skills/`](skills/README.md) | Ready skills you can adopt into your vault (recipe in `CURRENT.md`, your settings in `LOCAL.md`). |
| [`agents/`](agents/README.md) | Six agents (viewpoints) you can adopt: Alfred, Iris, Moneto, Presto, Librarian, Maestro. |
| [`packs/`](packs/) | Skills for a whole workflow: [podcast production](packs/podcast/README.md), [meetings](packs/meetings/README.md). |
| [`kits/`](kits/README.md) | Working machinery: view, search, learning (learn-merge, cognition), health checks, secrets inventory, thin entries. |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed in each version, and what to review in an adopted vault. |

## Language

The repository is written in English. Your agent talks to you in your language and writes into your vault in your language.

## Platforms

Works with **Claude Code** and **OpenAI Codex**, and with any agent that follows the `AGENTS.md` convention. Platform-specific parts (hooks, scheduling) are marked as such.

## License

See [`LICENSE`](LICENSE). Current version: [`VERSION`](VERSION).

Made by [ExarLabs](https://github.com/ExarLabs), from a PAROS in daily use since 2026.
