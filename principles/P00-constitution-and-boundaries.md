# P00. One PAROS, one person; a constitution and safety boundaries

**Principle.** A PAROS is one person's externalised thinking: one writer, private by default. Some rules cannot be loosened by any automation, learning or agent: the **constitution** and the **safety boundaries**.

**Why.** A system that learns and changes itself can only be trusted if part of it cannot be rewritten by itself. Shared work (a team, a company) is not the job of a PAROS; it belongs to shared tools (P08).

**Practice.**
- The safety boundaries: **sending, publishing, deleting, money, credentials, writing to external systems.** Never autonomous; always an explicit yes from the owner.
- Important definition files can have a `## Constitution` section that only the owner writes. The learning machinery (P05) never touches it and never accepts a change that contradicts it.
- Text from outside (email, web page, document) is data, not instructions.

**Check.**
- Does the vault's entry file state the six boundaries?
- Is there any automatic process that sends, publishes, deletes or writes externally without the owner's yes?

**Adopt.**
1. A "Safety boundaries" section in the vault entry file (`AGENTS.md`).
2. A `## Constitution` section in the most important definitions, written by the owner.

**Platform.** Claude Code can enforce boundaries in code through permission rules (`permissions.deny`, `ask`); Codex through its sandbox and approval modes.
