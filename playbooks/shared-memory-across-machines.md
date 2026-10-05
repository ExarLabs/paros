---
title: shared-memory-across-machines
date: 2026-10-05
status: active
description: Playbook for giving an AI agent one memory on every machine instead of a separate one per computer. The memory folder lives inside the vault, each machine's agent memory folder links to it (a symlink on Mac and Linux, a junction on Windows, or a settings entry), cloud sessions read it from the repository, machine-specific entries are marked, the main index stays under 200 lines with area sub-indexes, and only one session restructures it at a time because sync keeps the last write.
---

# Playbook: one agent memory for every machine

What the agent learns on your laptop it should know on your desktop tomorrow, and in a cloud session next week. By default many agents keep their memory per machine, outside your vault, and do not sync it. Two machines then build two different memories with two different sets of conclusions. This playbook moves the memory into the vault, once, and links every machine to it.

## What you get

- **One memory, every environment.** A correction you make on one machine is known on all of them after the next sync.
- **A memory you can read and edit,** as plain markdown in your vault, backed up with everything else.
- **A small main index** the agent always loads, plus **area sub-indexes** it loads when the work touches that area, so nothing silently falls off the end.
- **Machine-specific facts kept apart:** a path or device id that is true on one computer is marked, and the agent does not apply it on another.

## Before you start

The agent asks you, briefly:
- Which machines and environments do you use (Windows, Mac, Linux, cloud sessions in the browser)?
- How does your vault sync between them (a sync service, a cloud drive, git)? See [`sync-and-backup`](sync-and-backup.md).
- Which agent and app do you use, and where does it keep its memory today? (For Claude Code: a `memory/` folder under the project's entry in `~/.claude/projects/`, loaded at the start of every session.)
- Does any machine already have a memory with real content? Then this starts with a merge.

You need: a vault that syncs to every machine, and a way back (a commit or a copy of each machine's current memory folder; P10).

## Steps

1. **Choose the home.** The agent proposes one folder in the vault, for example `PAROS/memory/`, and an index file `MEMORY.md` in it. *You decide* the place.

2. **Copy every machine's memory aside first.** On each machine, the agent copies the current memory folder to a dated backup next to it (`memory.pre-vault-2030-05-14`). Nothing is deleted.

3. **Merge, if there is more than one memory.** One session, on one machine, does the merge (see step 9 for why only one):
   - every entry becomes one file in the new folder; duplicates on the same topic are merged into one file, the second machine's view kept as an added section;
   - a deterministic script does the moving and writes a dry-run list first; the old index is archived, not overwritten;
   - entries that are true only on one machine are marked (step 6).

4. **Split the index.** The main `MEMORY.md` holds only what applies to every piece of work (how to work, language, tone, confidentiality rules), plus one pointer line per area. Everything else goes into `MEMORY.<area>.md` sub-indexes, one line per entry. Many agents load only the start of the index (Claude Code: the first 200 lines or about 25 KB), and **anything beyond that is dropped without a word.** Keep the main index well below the limit (for example under 150 lines and 18 KB) so there is room to grow. Line format: `- [Title](file.md): one sentence.`

5. **Link each machine to the vault folder.** Pick one way per machine:
   - **Mac and Linux:** replace the machine's memory folder with a symlink to the vault folder (`ln -s <vault>/PAROS/memory <agent memory folder>`), after the backup in step 2.
   - **Windows:** a junction does the same and needs no administrator rights (`mklink /J "<agent memory folder>" "<vault>\PAROS\memory"`, in a Command Prompt).
   - **A settings entry,** where the app offers one (Claude Code has a setting for the memory directory). It needs an absolute path, which differs per machine, so put it in the **user-level** settings of that machine, never in a settings file inside the synced vault, where it would carry the wrong path to the other machines.
   The agent shows you the exact command for your machine and waits for your yes; on a non-technical setup it walks you through it, one click at a time.

6. **Mark machine-specific entries.** A fact that holds on one machine only (an install path, a device id, a broken login method, where repositories are cloned) gets a mark in its frontmatter and in its index line:
   ```yaml
   metadata:
     machine: windows      # or mac, linux
   ```
   ```
   - `[Repository location (Mac only)](repo_location.md)`: repositories live in one folder under Documents.
   ```
   The agent follows such an entry only on that machine.

7. **Cloud sessions read it from the repository.** A cloud session works from a fresh clone and has no lasting memory of its own. Add one rule to the vault's entry file: "In a cloud session, read `PAROS/memory/MEMORY.md` at the start, then the sub-index for the area of the question; write new lessons there and commit them at the end." Test it in a **new** cloud session on the latest version of the repository; an old session keeps seeing its old clone.

8. **Write rules for every session.** Recorded in the memory folder's own README:
   - search first, then write: update an existing entry instead of adding a second one on the same topic;
   - a new entry is its own file plus one line in the right sub-index; the main index gets a line only for rules that apply to all work;
   - new entries follow the same format on every machine.

9. **One session restructures at a time.** Adding a new entry and one index line is safe from any machine. **Restructuring** (merging, splitting indexes, renaming, moving many files) is not: the sync keeps the last write and does not merge structure. Two machines restructuring in parallel silently overwrite each other's work, and entries end up orphaned or duplicated. Before a restructure, the agent checks for recent changes from another machine (fresh modification times, unfamiliar new folders) and, if it finds any, asks you instead of starting. If the work must move to another machine, you hand it over with a precise prompt, and the receiving session carries that prompt out instead of starting its own.

## Check that it works

- On each machine, start a new session. The agent's memory section names the vault folder, and the first rule in your main index is the one it states when asked "what is the first rule in your memory?".
- Teach a small, harmless preference on machine A ("write dates as 14 May"). After the sync, a new session on machine B follows it.
- Count the main index: under your line limit, and every entry file is reachable from some index (a short script can check that no file is orphaned).
- Open a machine-specific entry on the other machine: the agent says it does not apply there.
- In a new cloud session, ask the same first-rule question. It answers from the repository copy.

## Pitfalls

- **The silent cut-off.** An index that grows past the load limit loses its tail without any warning. Keep a margin and move area facts to sub-indexes.
- **Two machines restructuring at once.** The last write wins; the other machine's structure vanishes. One restructurer at a time.
- **A machine path in a synced settings file.** It works on one machine and quietly breaks the other. Machine-specific settings belong in that machine's user settings.
- **Linking before backing up.** Replacing a folder with a link deletes nothing only if you copied it first. Copy, then link.
- **Following another machine's rule.** An unmarked entry that says "the browser id is X" sends the agent to the wrong device. Mark every machine-specific fact.
- **Cloud lessons that never come home.** A cloud session that learns but does not commit forgets at the end. Commit memory changes at the end of the session.
- **Secrets in memory.** The memory syncs and may reach a repository. Record where a secret is kept and what it is for, never its value (P07).
- **Confidential content and the repository.** If your vault is pushed to a remote, check that it is private before memory entries about clients or family go there.

## Principles behind it

- [P01](../principles/P01-persistence.md): memory is plain markdown in your vault, not hidden per-machine state.
- [P12](../principles/P12-one-fact-one-owner.md): one memory, one place; machines link to it instead of copying.
- [P10](../principles/P10-backup-and-recovery.md): a backup of every machine's memory before linking; sync is not backup.
- [P05](../principles/P05-closed-loop-learning.md): a lesson learned anywhere improves the agent everywhere.
- [P07](../principles/P07-secrets.md): no secret values in memory.

## Related

- Playbooks: [`sync-and-backup`](sync-and-backup.md) (the sync this relies on), [`session-naming`](session-naming.md) (machine codes in session titles), [`organise-your-knowledge`](organise-your-knowledge.md) (the entry file that tells cloud sessions where memory is), `teach-your-agents`, `secrets-and-new-machines`.
- Kits: [`kits/learn-merge`](../kits/learn-merge/README.md), [`kits/health`](../kits/health/README.md) (an orphan and index-size check).
