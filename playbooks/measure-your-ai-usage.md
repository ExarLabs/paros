---
title: measure-your-ai-usage
date: 2026-10-05
status: active
description: Playbook for seeing how you use your AI coding and agent tools, per machine and over time. A small script reads each machine's local session transcripts, writes one derived data file per machine into the vault (one writer per file), and a merged note shows months, ISO weeks, models, agents and projects for every machine and combined. Covers the parsing traps that undercount (nested subagent transcripts, replies split over several lines), what the numbers mean, and what local data cannot see.
---

# Playbook: measure your AI usage

The built-in usage panel of most AI tools sees one machine and offers "last 7 days, last 30 days, all time". If you work on two or three computers, you never see the whole picture, and you cannot answer simple questions: which month was heaviest, which project eats the most, how much of the work do subagents do, did moving a skill to a smaller model change anything.

This playbook builds that picture from data already on your disks.

## What you get

- **A note in your vault** with tables for every machine and combined: by month, by ISO week, by model, by agent (main session versus each subagent), by project; plus a small weekly chart.
- **One data file per machine,** written only by that machine, carried between machines by your vault sync. No conflicts, no double counting.
- **Numbers you can trust,** because the known traps that undercount are handled and the definitions are written next to the tables.
- **An optional live view** on a dashboard, built on the same data files.

## Before you start

The agent asks you, briefly:
- Which machines do you use your AI tools on, and does the vault sync to all of them?
- Which tools? (For Claude Code, every session leaves a transcript as a `.jsonl` file under `~/.claude/projects/` on that machine. Other tools keep similar logs; the agent checks where.)
- Do you also work in cloud sessions or a chat app in the browser? Those transcripts never reach your disk, so they will not be counted (see Pitfalls).
- Is per-project detail fine to keep in the vault, or should project names be grouped?

You need: Python 3.9 or newer on each machine, and a vault folder for the note and its data, for example `PAROS/usage/`.

## Steps

1. **Agree on a short host name per machine.** Something stable and plain, like `desktop`, `laptop`, `studio`. Every writer on that machine uses the same name, so a later run overwrites its own file instead of adding a second one. *You decide* the names; the script can also detect them, with an override setting.

2. **Write the scanner.** The agent writes one standard-library script, for example `usage.py`, that:
   - reads every transcript file on this machine, **including nested subagent and workflow transcripts** (they sit in subfolders under the parent session; a one-level file pattern misses them);
   - takes each assistant reply's token counts (input, output, cache write, cache read) and model;
   - credits subagent work to the session and project that launched it, and records which agent did it;
   - buckets everything by day in the machine's local time zone, by project, model and agent;
   - writes `data/<host>.json` with a schema name and version in the file, so a future change is visible.

3. **Handle the split replies.** One reply is often written as several transcript lines that share a message id; only the last line carries the full output count. **Take the maximum per message id, never the first line.** A first version that missed this and the nested subagents undercounted output by about a third.

4. **Merge and render.** A second mode (`usage.py --merge-only`) reads every `data/*.json` present and regenerates a block in `usage.md` between two marker comments:
   ```
   <!-- usage:begin -->
   ... generated tables, do not edit by hand ...
   <!-- usage:end -->
   ```
   Tables: hosts (export date, files, first and last day), combined monthly, combined weekly, per host monthly, output by model, by agent, by project, and a weekly output chart (Obsidian renders Mermaid charts).

5. **Write the definitions next to the numbers.** The note says, above the tables:
   - **sessions** are counted in every period they touch, so a session over a month boundary appears in both;
   - **messages** count every transcript line of both sides, tool results and subagents included, so they run higher than the app's own count;
   - **output tokens** are the cleanest column for comparing periods;
   - **totals including cache reads** are dominated by cache reads and are not the same as the app's "total tokens";
   - **weeks** are ISO weeks starting Monday;
   - **not covered:** cloud sessions, scheduled cloud routines and browser chat.

6. **Run it on every machine.** On each machine, run the scanner once (a few seconds). After the vault syncs, run the merge anywhere. *You decide* whether to schedule it; a daily or half-hourly export per machine keeps the note current without anyone remembering.

7. **Keep writers in step.** If you later add a live dashboard that writes the same files, it must use the same schema and the same host names. Two scanners that disagree produce two truths. Test them against each other on past days: the files must be identical.

8. **Ask questions of it.** Now the agent can answer "which month was heaviest?", "how much do subagents do?", "what did the week after I switched that skill to the smaller model look like?" from the data, and say which machines and dates the answer covers.

## Check that it works

- On one machine, compare the scanner's message and output figures for one recent day with what you expect from that day's sessions. Then run a deliberately naive version (first line per message id, top-level files only): its output figure must be clearly lower. That proves both traps are handled.
- Run the scanner twice on the same machine: still one file for that host, same numbers.
- Delete one host's data file on a copy and merge: that host disappears from the tables and the combined figures drop by exactly its share.
- The hosts table shows a recent export date for every machine; an old date means that machine has stopped exporting. A health check can watch this.

## Pitfalls

- **Missing subagents.** A shallow file pattern skips nested transcripts and quietly drops a large share of the work.
- **First-line counting.** Reading the first of several lines for a reply undercounts output badly.
- **One machine's view taken as the whole.** The app's panel, or one host's file, is a part. Say which hosts an answer covers.
- **Cloud work is invisible.** Sessions in the browser or in the cloud leave no local transcript. If you work there a lot, the numbers are a floor, not a total.
- **Two writers, one file.** Only the machine itself writes its file; the sync carries it. Never let a machine write another machine's data.
- **Comparing different definitions.** "Total tokens" in an app panel and "total including cache reads" here are different measures. Compare output with output.
- **Project names as personal data.** Folder names can reveal clients. If the note may ever be shared, group or rename projects in the merge, not in the source.
- **Usage is not output.** Many tokens do not mean much was done. For what you did, see the recap.

## Principles behind it

- [P01](../principles/P01-persistence.md): the source stays local and untouched; the derived files and the note are plain files in the vault.
- [P12](../principles/P12-one-fact-one-owner.md): one writer per data file, one schema, writers kept in step.
- [P11](../principles/P11-health-contract.md): known traps tested, stale exports visible.
- [P02](../principles/P02-presentation.md): a generated block, never edited by hand; a dashboard only renders the same data.

## Related

- Playbooks: [`recap-and-journal`](recap-and-journal.md) (what you did, as opposed to how much you used), [`measure-your-skills`](measure-your-skills.md) (token cost per skill run), [`build-a-dashboard`](build-a-dashboard.md) (a live, filterable view), [`shared-memory-across-machines`](shared-memory-across-machines.md), [`sync-and-backup`](sync-and-backup.md).
- Kits: [`kits/view`](../kits/view/README.md), [`kits/health`](../kits/health/README.md).
