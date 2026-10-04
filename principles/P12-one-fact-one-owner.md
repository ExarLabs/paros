# P12. One fact, one owner

**Principle.** Every fact has exactly one authoritative place. Every other occurrence is a reference, or an explicitly derived copy (with its source and date).

**Why.** If the same fact lives in two places, they drift apart sooner or later, and nobody knows which is true. An AI system will confidently quote both.

**Practice.**
- A **source map** (for example `ARCHITECTURE_BOUNDARIES.md`) says, per kind of data, what is authoritative and what is derived.
- The list of agents and their versions lives in one place; other documents link to it.
- In an external system's own domain (CRM, shared document store), the external system is authoritative (P08).
- A generated view (index, summary, HTML) always says what it was made from and when, and is never edited by hand.

**Check.**
- Pick a fact that changes often (for example an agent's version): in how many places does it appear, and do they agree?

**Adopt.** A source map in the vault, and a rule in the entry file: "a new kind of data goes on the map before it is written".
