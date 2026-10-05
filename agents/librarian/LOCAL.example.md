---
title: Librarian LOCAL
date: 2026-10-05
status: active
description: Personal settings for the Librarian viewpoint, with a fictional worked example: which units get a tier 2 index, folders never to touch, outside folders to scan, separate collections, stale thresholds and known name variants. Copy to LOCAL.md and replace with your own.
---

# Librarian: personal settings

> A worked example with made-up values. At adoption, copy this file to `LOCAL.md` next to `CURRENT.md` and replace everything. `LOCAL.md` never leaves your vault.

## Index scope

**Tier 1:** the vault root.

**Tier 2 units** (each gets the five index files at its root):

| Unit | Why |
|---|---|
| `Areas/Hillside Bakery/` | 140 files, active |
| `Areas/Woodshop Course/` | has a current-state file |
| `Areas/Household/` | 60 files |
| `Resources/Books/` | 45 reading notes |

Last verified by `index` check: fill in from the check output, never by hand.

## Never touch

- `.git/`, `.obsidian/`, `.trash/`, `node_modules/`
- `Areas/Household/Private/` (not indexed, not audited)

## Archive

- Archive folder: `Archive/`, mirroring the original path.
- Indexed only when a scope names it explicitly.

## Outside folders for `integrate`

- `~/Downloads/`, `~/Documents/`, `~/Desktop/`
- File types: md, txt, pdf, docx, srt
- Never: system and application folders, photo and music libraries, `~/.ssh/`, any credential store.

## Separate collections

| Collection | Index location | What |
|---|---|---|
| `talks` | `~/collections/talks/index.db` | transcripts of conference talks the owner follows |
| `mail-archive` | `~/collections/mail/index.db` | an exported mailbox from a closed project |

## Thresholds

- Stale: no change for 90 days and status not archived (audit warns only).
- Deep-clean candidate: 180 days, unlinked.
- Temporary files: `*.bak`, `*.tmp`, `*~` older than 30 days and unlinked.

## Name variants

Known entities whose spelling varies in the notes:

| Canonical | Variants |
|---|---|
| Hillside Bakery Ltd | Hillside, Hill-side Bakery, HB |
| Weekend Woodshop | Woodshop, W-Shop, WW |
