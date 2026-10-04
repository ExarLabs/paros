# P11. No "it works" without proof

**Principle.** A process is healthy when a real input actually produces the expected output, not when it is running or when the documentation says it exists. Every automatic process comes with a check on its **output**.

**Why.** The dominant failure in a personal agent system is the **silent failure**: a hook writes nothing for months, an index does not refresh for months, a secret stays in the vault, and nobody notices because nothing signals it.

**Practice.**
- **End-to-end canary:** one run writes a unique marker into a note; the next run looks for it in the search index. If found, writing, file watching, indexing and search all work.
- Weighted checks (1: log only, 2 to 3: alert). Typical: index freshness, the session log is written, no plain secrets in the vault, secrets inventory, frontmatter on new files, the learning cycle runs, backup age.
- **Alert only on state change:** when a check goes from green to red, one line goes into the owner's task list; no repeat while it stays red; on recovery the line is marked.
- No new automatic process without its check.

**Check.** Run the health checks; if there are none, that is the finding.

**Adopt.** Start with three checks: canary, index freshness, plain secrets. Run them every few hours (kit: `kits/health`).
