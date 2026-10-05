---
title: report-as-code
date: 2026-10-05
status: active
description: Playbook for a recurring monthly report (timesheets, invoicing, usage, fuel, any export turned into figures) that is built by code instead of prose instructions. One executable rule source that stops on anything it cannot assign, an inverse check of every filter list, a headcount gap gate, two independent parsers, regression against accepted months, a month-over-month diff, and why matching totals can hide errors that cancel out.
---

# Playbook: the report is code, not prose

A monthly report that an agent rebuilds from a page of instructions drifts a little every month. Each run reinterprets the prose, makes a plausible guess where a rule is missing, and the guesses are invisible in the totals. The cure is to turn the procedure into code that refuses to guess, and to check that code from more than one direction.

The lesson behind it, from months of running such a report: **what was prose broke every month; what was code did not.**

## What you get

- **One executable rule source** for every assignment (which line goes to which category, project, client or cost centre). The documentation describes it; the code is the truth.
- **A run that stops** on any item without a rule, instead of putting it "where most of the others went".
- **Checks from several directions:** a second, independent parser; a read-back of the files the run produced; regression against months you already accepted; a month-over-month diff; an inverse check of every filter list; a headcount gap gate.
- **A short, repeatable monthly routine:** review, generate, verify, and only then "done".

## Before you start

The agent asks you, briefly:
- What is the input (an export file, a spreadsheet, an API), and how often does it arrive?
- What is the output (workbooks, a summary note, invoice lines, a dashboard row)?
- Who accepted the last few months' reports, and where are those accepted versions? They become your regression baseline.
- Which lists decide what is in scope (a team list, a project list, a client list)? Each one will get an inverse check.

You need: a few past months with accepted outputs, Python (or another language your agent can run), and a vault folder for the report's code and its changelog.

## Steps

1. **Write the rules as code first.** The agent turns the prose procedure into one module, for example `rules.py`: mappings, exclusions, aliases for renamed items, special cases with the date they were decided. Order of work for every change: **code first, then the documentation, then a changelog line.** A rule that exists only in a note does not exist.

2. **No guessed assignments.** Any input line the rules cannot place is marked `UNMAPPED`, and generation **stops** with a list of those lines. The agent asks you, you decide, the decision becomes a rule, and the run starts again. "Put it on the nearest line" or "the dominant category" are the guesses that cause most errors.

3. **Keep parallel things apart.** Two contracts with the same customer, two phases of one project, a fixed-price line and a time-based line: separate rows that never merge, even when their names look alike.

4. **Split the run into phases.**
   ```
   review    read the input, list what is new, missing or unmapped, diff against last month
   generate  build the outputs; refuses to run while anything is unmapped or a gate fails
   verify    the full checklist below; no month is done without it
   ```

5. **Add the inverse check to every filter list.** A list that decides who or what is in scope is a rule like any other, and it decays silently: someone joins, a project is added, and their lines are dropped without a sound. For each filter, also ask the opposite question: **what in the raw input is being dropped by this filter, and should it be?**

6. **Add the headcount gap gate.** A concrete case of step 5. Anyone (or anything) who appears in the raw input under the scope you report on, but is neither on the list nor on the explicit exclusion list, **stops the run**. Without this gate, a new team member's hours can be missing for months while every other check stays green, because every other check uses the same stale list.

7. **Verify with a second, independent path.** A check that reuses the first parser only proves the parser agrees with itself. Read the raw input a second way (a different library, or reading the file format directly), aggregate it a second way, and read the generated files back. All three must agree, line by line.

8. **Do not trust totals alone.** Two errors can cancel each other out: one line counted 40 too high and another 40 too low gives a perfect grand total. Compare **per line** (per person, per project, per category), not only the sum.

9. **Run regression on accepted months.** Re-run the new code on the last two or three accepted months. Their figures must match the accepted versions exactly. Where they do not, either the old report was wrong (and a rule decided since then explains the difference; write that down) or the new code is. Never accept an unexplained difference.

10. **Diff month over month.** The review phase lists lines that are new this month and lines that disappeared since last month. Most surprises show up here first.

11. **Read grids with a parser, never by eye.** If the input is a spreadsheet or a report grid, the agent reads it with code. A model reading a table visually miscounts rows and columns. If the latest period in the input is still open, the output says it is preliminary.

12. **Learn from each month.** A correction you make becomes a rule in the code plus a line in the report's lessons file (P05). The agent proposes it; you approve it.

## Check that it works

- Remove one mapping rule on a copy and run: generation stops and lists the affected lines. It does not produce a report.
- Add a made-up person to a copy of the raw input under your scope: the headcount gap gate stops the run and names them.
- Move 10 units from one line to another in a copy of last month's output: the totals still match, and the per-line comparison fails. This proves your verify step looks deeper than the sum.
- Run regression: the accepted months reproduce exactly, or every difference has a written reason.

## Pitfalls

- **Prose that "everyone knows".** If a rule is in a chat, a note or someone's head, the next run will not apply it. Put it in the code.
- **Green checks that share a blind spot.** Every check built on the same list or the same parser misses the same thing. Check the input from outside your own filters.
- **Totals as proof.** A matching grand total is the weakest evidence there is.
- **A library that reads only part of the file.** Some spreadsheet readers, in their fast mode, trust a size field in the file and see only the first rows of certain exports. Your second parser is what catches this; compare row counts first.
- **Merging look-alikes.** Two lines with similar names are not one line until a rule says so.
- **Writing code through a shell heredoc.** Large or backslash-heavy code passed through a shell here-document can be altered or cut off silently. Write files with a file tool; use the shell only to run them.
- **"Done" before verify.** A report is done when the full checklist passes, not when the files exist.

## Principles behind it

- [P11](../principles/P11-health-contract.md): proof by result, checked from more than one direction.
- [P12](../principles/P12-one-fact-one-owner.md): one rule source; the documentation points to it.
- [P05](../principles/P05-closed-loop-learning.md): each month's corrections become rules.
- [P00](../principles/P00-constitution-and-boundaries.md): sending a report or an invoice stays your act; the code prepares, you send.
- [P01](../principles/P01-persistence.md): rules, lessons and changelog are plain files in the vault.

## Related

- Playbooks: `business-finance` (methodology per organisation), [`build-a-dashboard`](build-a-dashboard.md) (show the verified figures), [`measure-your-skills`](measure-your-skills.md) (the same "measure, do not assume" idea for agent skills).
- Kits: [`kits/health`](../kits/health/README.md), [`kits/learn-merge`](../kits/learn-merge/README.md).
- Agent: [`agents/moneto`](../agents/moneto/CURRENT.md) (finance viewpoint).
