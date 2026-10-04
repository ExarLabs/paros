# Changelog

Every entry: what changed, and **what to review in a vault that has already adopted PAROS.**

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
