# Kits: optional reference implementations

A kit is a working example of a principle. **Optional,** and never copied blindly: the agent reads it and rebuilds it for the person's vault (or adopts and adapts it). The code is disposable; the principle and its check are what matter.

| Kit | Principle | What it gives | Status |
|---|---|---|---|
| `search` | P06 | SQLite FTS5 index of the vault, ranked search on 2 to 4 word stems, a read-only skill | planned |
| [`cognition`](cognition/README.md) | P05 | weighted learned rules, use marks, the cognitive cycle, a report with a heat map; hooks for Claude Code | **available** |
| [`learn-merge`](learn-merge/README.md) | P05 | typed rule changes without compaction (add, update, deprecate, move), version snapshots, a log; an independent judge from another model family | **available** |
| `health` | P11 | canary and weighted checks, alerts on state change | planned |
| [`secrets`](secrets/README.md) | P07 | secrets inventory without values, per-machine presence, a health check (the encrypted transfer bundle is planned) | **available** |
| `backup` | P10 | encrypted snapshot backup on a schedule, with test restores | planned |
| [`view`](view/README.md) | P02 | three levels: no app, a zero-build Node.js view (search, note preview, tasks written back to markdown, live refresh), or a React app on the same API | **available** |

Every kit will say what works in Claude Code, what works in Codex, and what is platform-independent (Python scripts with no or minimal dependencies).

The diagnosis scanner is already here: [`tools/diagnose.py`](../tools/diagnose.py). Shared skills are in [`skills/`](../skills/README.md).
