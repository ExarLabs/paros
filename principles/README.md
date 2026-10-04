# The PAROS principles

One principle per file, always the same structure: **Principle** (one or two sentences), **Why**, **Practice**, **Check** (how to see it in your own vault), **Adopt** (steps), and **Platform** notes where Claude Code and Codex differ. IDs (P00 to P12) are stable: the changelog refers to them.

**Core** = every PAROS needs it. **Module** = needed when it becomes relevant.

| ID | Principle | Type | Status |
|---|---|---|---|
| [P00](P00-constitution-and-boundaries.md) | One PAROS, one person; a constitution and safety boundaries | core | stable |
| [P01](P01-persistence.md) | Knowledge lives in markdown (and JSON); everything else is derived | core | stable |
| [P02](P02-presentation.md) | Presentation is HTML, a live view that writes back to markdown | module | stable |
| [P03](P03-agent-is-a-viewpoint.md) | An agent is a viewpoint on the vault, not a separate program | core | stable |
| [P04](P04-thin-entry-live-definition.md) | Thin entry point, live markdown definition | core | stable |
| [P05](P05-closed-loop-learning.md) | Closed-loop learning: use teaches, with weighted knowledge | core | stable |
| [P06](P06-search.md) | Search is a capability, index first | core | stable |
| [P07](P07-secrets.md) | Secrets live outside the vault, travel encrypted, and are inventoried without values | module (core once you connect tools) | stable |
| [P08](P08-connectors.md) | Connectors: SaaS is the backbone, AI is the glue | module | stable |
| [P09](P09-forgetting-and-archiving.md) | Forgetting: fade, archive, do not delete | core | stable |
| [P10](P10-backup-and-recovery.md) | Backup: sync is not backup | core | proposal |
| [P11](P11-health-contract.md) | No "it works" without proof | core | stable |
| [P12](P12-one-fact-one-owner.md) | One fact, one owner | core | stable |

## PAROS in one sentence

A person's knowledge in plain markdown, handled by AI agents through a few viewpoints, learning continuously from use, where fast, deterministic, shared work stays in external tools and judgment and glue come from the AI.
