# P06. Search is a capability, index first

**Principle.** Searching the vault is a **capability** (a skill), not an agent. Search a fresh full-text index first, ranked; raw file search (grep) is for exact strings and code only.

**Why.** In a large vault, raw search is slow, noisy and eats context. Measured in practice: the index puts the right answer first far more often than grep. The index is derived (P01) and can be rebuilt at any time.

**Practice.**
- Turn the question into 2 to 4 characteristic word stems; the index ranks results, with `title` and `description` weighted above the body.
- If many files must be read together, a context-protecting worker (P03) does it with the same capability and returns only a summary.
- The health checks watch the index's freshness (P11).

**Check.**
- For five real questions, is the first hit right?
- How old is the index?

**Adopt.**
1. A small vault is fine with Obsidian's search and grep.
2. Above a few thousand files: a SQLite FTS5 index over frontmatter and body (kit: `kits/search`), and a skill that uses it.
