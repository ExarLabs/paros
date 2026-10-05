# Changelog

Every entry: what changed, and **what to review in a vault that has already adopted PAROS.**

## 0.6.0 (2026-10-05)

- **One-sentence install and the `/paros` command.** Tell your agent "Read https://ignis.academy/paros and install the PAROS Advisor": it clones this repository into `~/.paros-advisor` and installs `/paros` for Claude Code (and Codex if present). `/paros` updates the advisor on every use, tells you what is new, and answers questions about your vault.
- New `playbooks/`: the catalog of step-by-step guides (connectors, dashboards, organising knowledge, meetings, thinking with several AIs, and more), with what is ready and what is coming.
- To review: install `/paros` once; after that, updates reach you on their own.

## 0.5.0 (2026-10-05)

- **Renamed to PAROS Advisor** (`ExarLabs/paros-advisor`; the old address redirects). The repository is an advisor engine for building your own PAROS, not PAROS itself.
- New `agents/`: six viewpoints you can adopt, names kept: Alfred (chief of staff), Iris (people), Moneto (finance), Presto (marketing), Librarian (knowledge caretaker), Maestro (system caretaker, learning review and cognitive cycle). Each with a recipe, a `LOCAL.example.md`, and entries for Claude Code and Codex.
- New `packs/`: podcast production (12 skills) and meetings (3 skills).
- New `starter/`: a small demo vault with fictional areas, three agents and a dashboard (navy, red and yellow design tokens, zero dependencies), to see PAROS working before building your own.
- To review: if you use any of these viewpoints already under other names, compare their rules with yours; adopt Alfred first if you have none.

## 0.4.0 (2026-10-05)

- New kits, working and tested: `thin-entry` (build thin skill entries with the "vault always wins" version report, promote with snapshots, a learning digest), `search` (a standalone FTS5 index outside the vault and ranked search), `health` (canary, index, secrets, frontmatter, learning cycle and backup checks, alerts only on state change).
- New skills: `think` (several AIs on one question, with a state file), `transcribe` (Groq Whisper with a completeness check), `speed-reader`, `language-editor`.
- New convention, **recipe and spice**: the general procedure is in `CURRENT.md`; personal settings go into `LOCAL.md` (shipped as `LOCAL.example.md`), which never leaves your vault and is never touched by updates.
- To review: if you adopted a skill earlier, move anything personal from its `CURRENT.md` into a `LOCAL.md`, so future updates merge cleanly.

## 0.3.0 (2026-10-05)

- New kits, working and tested: `view` (no app, a zero-build Node.js view with search, note preview, tasks written back to markdown and live refresh, or step-by-step React instructions on the same API), `learn-merge` (typed rule changes without compaction, plus the independent judge), `cognition` (weighted rules and the cognitive cycle), `secrets` (inventory without values).
- New: shared skills in `skills/` (`frontmatter-header`, `project-state`, `adversarial-second-pass`), each with a live definition, a thin entry, a changelog and a golden example, and the adoption mechanism: a skill lives in your vault with an `upstream:` block, and updates from here arrive as suggestions judged by your own learning loop.
- The advisor now always offers matching skills and kits: at the end of the tour, the diagnosis and the personal guide, and whenever you ask what you can adopt.
- To review: ask your agent "Which PAROS skills and kits would help me most?" and adopt the ones that remove your biggest friction.

## 0.2.1 (2026-10-04)

- Vision stated: a minimal, cognitive operating system that adapts to you.
- P02 refined: the view is minimal and disposable; no app is needed at the start, and a live view should be zero-build (a small local server and plain HTML), never a required framework.
- To review: if your vault depends on a heavy frontend for daily use, check that no knowledge lives only there (P01), and consider whether a simpler view would do.

## 0.2.0 (2026-10-04)

- The repository is now in English, and is an **advisor**: tour, diagnosis, personal guide, adoption, advice and upgrade flows (`flows/`).
- New: `tools/diagnose.py`, a dependency-free, read-only scanner that measures a vault against the principles.
- New guides: add a connector, add a skill, daily work.
- Principles P00 to P12 translated and renamed (English file names); content unchanged.
- To review: nothing for adopted vaults beyond running the diagnosis once to get a baseline.

## 0.1.0 (2026-10-04)

- First internal version (Hungarian): entry file, adoption and upgrade flow, 13 principles, templates.
