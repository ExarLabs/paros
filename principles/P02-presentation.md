# P02. Presentation is HTML, a live view that writes back to markdown

**Principle.** What people look at is HTML: a web page, a graph, an interactive view. The view reads from markdown, and when it writes, it writes back into markdown; it has no knowledge store of its own.

**Why.** Markdown is good for storing and bad for overview. HTML gives the overview; markdown stays the truth (P01).

**Practice.**
- **Live view** (a local web app, a dashboard): updates itself when the vault changes; shows its source and freshness.
- **Snapshot** (PDF, a sent deck, a static page): does not update; carries its date and source ("as of YYYY-MM-DD").
- Writing back (ticking off a task, for example) always goes into the markdown file.
- **Keep the view minimal and disposable.** The view is the least important layer: the markdown is the system. Most people need no app at all at the start; the notes editor (Obsidian, for example) is the interface. When a live view is needed, prefer a **zero-build** setup over a heavy frontend stack: a small local server (Node.js or Python, no dependencies) serving plain HTML with a little JavaScript. No build step, no framework to keep updated, nothing that breaks on another machine. A richer framework is fine for power users, but it is never required, and nothing in it may hold knowledge (P01).

**Check.**
- Is there any view with its own data that does not exist in the vault?
- Do snapshots show their date and source?

**Adopt.** Module: at first, the notes editor's own views are enough. When a view is needed, start with a generated snapshot (one HTML file), then a zero-build live view.
