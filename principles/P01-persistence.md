# P01. Knowledge lives in markdown (and JSON); everything else is derived

**Principle.** The source of knowledge is markdown, because both people and AI read and write it. JSON is accepted as a source for structured data. Everything else (databases, search indexes, caches, generated PDFs) is derived and can be rebuilt from the source at any time.

**Why.** Markdown does not age, does not lock you into an application, and every AI model reads it. If the truth lived in a database, your knowledge would be the prisoner of a tool.

**Practice.**
- Every file starts with **frontmatter**; the most important field is `description` (one or two sentences about the content). An agent decides from it whether a file is worth opening. Schema: `templates/frontmatter.md`.
- Incoming originals (PDF, spreadsheet, audio): if they matter, a markdown companion is made (summary and link), and work continues from it.
- Machine state (queues, logs, caches) may live in a database **if losing it loses no knowledge.** The test: "if I deleted it today, would I miss something I wanted to know?"
- Every JSON store gets a short markdown description next to it (what it is, who writes it, who reads it).

**Check.**
- Sample 20 random files: how many have frontmatter, and how many have a description about the content?
- Is there a database or application where some knowledge exists only there?

**Adopt.**
1. Fix the frontmatter schema in the vault entry file.
2. Add frontmatter to existing files gradually (an agent, in batches, with the owner's approval).
3. Every new file is born with frontmatter.
