---
title: mine-your-agent-history
date: 2026-10-06
status: active
description: Playbook for recovering the knowledge that lives only in past agent conversations (decisions, prices, terms, rules, preferences) and bringing the parts worth keeping into the vault. A local, read-only digest of the person's own requests and session summaries, secrets masked; reviewed by area with subagents; each new note created only with a yes.
---

# Playbook: mine your agent history

## What you get

The things you decided or explained to an agent and never wrote down, recovered into your vault: a price you agreed, a payment term, a rule you gave ("never send without asking"), a naming convention, why a project went the way it went. In practice the conversation history is often the richest source of knowledge a person has, and the least searchable.

## Before you start

- **Where the history is.** Claude Code keeps one log per session under `~/.claude/projects/` (one folder per working folder). If you also work inside WSL, the same folder exists there (for example `\\wsl$\<distro>\home\<you>\.claude\projects`). Other agent apps keep their own logs; add them as extra roots when their format is similar.
- **Privacy.** These logs hold everything you ever typed, including things about other people and, sometimes, secrets you pasted. The digest stays on your machine: the tool sends nothing and prints only counts. Read it yourself before anything moves into the vault.
- **Time.** About an hour for the first pass over a few months of history; later, a short monthly pass.

## Steps

### 1. Make the digest (read-only, outside the vault)

```bash
python <advisor>/tools/agent_history.py --out ~/paros-history
python <advisor>/tools/agent_history.py --out ~/paros-history --root "<WSL history folder>"   # also WSL
python <advisor>/tools/agent_history.py --out ~/paros-history --since 2026-01-01 --project acme  # narrower
```

It writes `INDEX.md` (projects, sessions, requests, date range) and one file per project folder: for each session the date, the folder, the summaries the app stored, and **only your own requests**. The agent's answers, tool output, injected system text and app notices are left out; secret-like values are masked.

### 2. Decide the scope together

Look at `INDEX.md` with your agent. Choose the projects and the period that matter (a client relationship, a product, a year). Skip the rest; not everything needs mining.

### 3. Extract by area, with helpers

For a large history, the agent gives each chosen project file to a separate helper (subagent) with one instruction: list **facts worth keeping**, each with the session date and a one-line quote of your own words as evidence, in these kinds: decisions, prices and terms, rules and preferences you stated, people and roles (only what the vault already handles), open threads. Helpers return lists; they write nothing.

### 4. Check against the vault before writing

For each fact the agent searches the vault: already there (skip), there but stale (propose an update), missing (propose a note or a line in the right area). Conflicts between an old chat and a newer note are shown to you, never resolved silently: the newer, written source usually wins, but you decide.

### 5. Write with a yes, in small batches

Each proposed note or change follows the advisor's write rule: which file, why, the exact change, how to undo, then your yes. Mark the source in the note ("from an agent session on 2026-03-02") so the fact can be traced. Rules you stated to agents become entries in your entry file or a skill's rules, through your learning loop, not by copying chat text.

### 6. Make it a habit

Once a month, run the digest with `--since` set to the last pass, and repeat steps 3 to 5. The second time is much shorter.

## Check that it works

- `INDEX.md` lists the projects you expect, with plausible session counts.
- A request you remember typing appears in the right project file; an agent answer you remember does not.
- A key you once pasted shows up masked, never in clear.
- After step 5, asking your agent "what did we agree with Acme about payment?" is answered from a vault note, with its source.

## Pitfalls

- **Mining everything.** Most chat is working talk. Choose the projects that carry decisions.
- **Copying chat into the vault.** Notes are written fresh, short, with a source line; the digest itself stays outside.
- **Trusting an old chat over a newer note.** History records what was said then; show conflicts.
- **Forgetting other people.** Facts about others go only where your vault already keeps them (P00, people notes), never into a new pile.
- **Leaving the digest lying around.** Delete or archive it outside the vault when the pass is done; it contains everything you ever typed.

## Principles behind it

[P01](../principles/P01-persistence.md) (knowledge lives in plain files, not in chat), [P05](../principles/P05-closed-loop-learning.md) (stated rules become reviewed rules), [P07](../principles/P07-secrets.md) (secrets masked, never moved), [P12](../principles/P12-one-fact-one-owner.md) (one fact, one place, with its source).

## Related

[`organise-your-knowledge`](organise-your-knowledge.md), [`recap-and-journal`](recap-and-journal.md), the ecosystem diagnosis in [`flows/2-diagnose.md`](../flows/2-diagnose.md) (`--also`), [`share-with-your-team`](share-with-your-team.md).
