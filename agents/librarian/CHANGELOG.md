# Changelog: Librarian

Every entry: what changed, and **what to review in a vault that has already adopted this agent.**

## 1.1.0 (2026-10-05)

- `integrate` checks a fixed deny list before any outside scan (system, application and media folders, key and credential stores, configuration and dot folders, `.git`, dependency folders) and stops to ask when a requested folder falls inside it (R-005).
- Never merges files that are similar but not byte-identical; an apply that touches an area with active work gets one more question (R-006, and a line in the safety boundaries).
- Search hits are handed on as a list, never retold in prose, by the Librarian and by the caller (R-007).
- To review: if your `LOCAL.md` lists outside folders to scan, check none of them falls inside the deny list; your own exclusions can extend it, not shorten it.

## 1.0.0 (2026-10-05)

- First public version, generalised from a knowledge caretaker in daily use since mid 2026.
- Role after the index-first change (P06): search is a skill; the Librarian is the caretaker of structure and a context-protecting worker for wide reads, and it searches with the same skill.
- Seven modes in one table (reads, writes, confirmation): `retrieve`, `index`, `audit`, `tidy`, `deep-clean`, `integrate`, `transcript-note`.
- Constitution: archive, do not delete; dry run by default; link check before any move; undo command in every log; `retrieve` never writes; outside folders read only.
- Learned rules R-001 to R-004: the list is not proof, name variants, extended regex, generator suspicion for headerless file groups.
- Recipe and spice split: tier 2 units, excluded folders, outside folders, collections, thresholds and name variants live in `LOCAL.md`; `LOCAL.example.md` carries a fictional example.
- To review: copy `LOCAL.example.md` to `LOCAL.md` and list your own units; adopt the search kit first if you have not; install `agent.claude.md` as `.claude/agents/librarian.md` or add the routing line from `agent.codex.md`; create `observations/` and `LEARNINGS.md` next to `CURRENT.md`.
