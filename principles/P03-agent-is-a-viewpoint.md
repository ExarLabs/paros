# P03. An agent is a viewpoint on the vault, not a separate program

**Principle.** An agent is a **viewpoint**: a way of holding the vault (for example "people", "money", "marketing", "the owner's daily operations"). It lives in one file: a map (where the relevant knowledge is), rules, and an attitude. You need an agent when a viewpoint **cuts across several areas**; inside one area, the area's own entry file is enough.

**Why.** A vault is organised by areas (vertical); an agent cuts across them (horizontal). If every task gets its own agent, you end up with many shallow, overlapping roles. The goal: a few deep viewpoints, not many shallow ones.

**Practice.**
- The main session can take on a viewpoint by reading its file. No separate run is needed.
- **A separate run (a worker, a subagent)** is worth it for six reasons only: protecting context (read a lot, return a summary), parallelism, independence (fresh eyes), unattended runs, a cheaper model, narrow permissions. The worker also starts from the viewpoint file.
- **Before a new agent, a written reason** why it does not fit an existing one.
- Test: if the same request gives a different result with and without the agent's name, that is a routing bug. The system should recognise the viewpoint from the topic.

**Check.**
- How many agents are there, and does each cut across at least two areas?
- Is any agent really a procedure? (That belongs in a skill, P04.)

**Adopt.**
1. Start with zero or one agent; the main session and the area entry files are enough.
2. A viewpoint file is born when a cross-cutting topic comes up the third time.

**Platform.** Claude Code: `.claude/agents/<name>.md` as a thin entry pointing to the viewpoint file. Codex: the viewpoint file referenced from `AGENTS.md` or from a skill.
