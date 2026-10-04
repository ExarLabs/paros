# P02. Presentation is HTML, a live view that writes back to markdown

**Principle.** What people look at is HTML: a web page, a graph, an interactive view. The view reads from markdown, and when it writes, it writes back into markdown; it has no knowledge store of its own.

**Why.** Markdown is good for storing and bad for overview. HTML gives the overview; markdown stays the truth (P01).

**Practice.**
- **Live view** (a local web app, a dashboard): updates itself when the vault changes; shows its source and freshness.
- **Snapshot** (PDF, a sent deck, a static page): does not update; carries its date and source ("as of YYYY-MM-DD").
- Writing back (ticking off a task, for example) always goes into the markdown file.

**Check.**
- Is there any view with its own data that does not exist in the vault?
- Do snapshots show their date and source?

**Adopt.** Module: at first, Obsidian's own views are enough. When a view is needed, start with a generated snapshot, then a live view.
