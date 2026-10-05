---
title: principle-candidates
date: 2026-10-05
status: proposal
description: Five candidate principles from running a PAROS daily, published as open proposals, not as principles. Freshness and write-back; the harness matters more than the model; a wall between thinking and distribution; silence is the default; verb classes for agent permissions.
---

# Principle candidates (open proposals)

These ideas come from the maintainers' own PAROS. They are published as **proposals**: the principles in [`principles/`](../principles/README.md) do not change until a proposal has proven itself. Adopt any of them in your vault if it helps; tell us how it went (the advisor can send it for you).

## 1. Freshness and write-back

Whoever changes the state of something also updates its canonical file (a dated "current status" block). Whoever reads state says how fresh it is. No false completeness: a snapshot pulled from a shared tool carries its `pulled_at` date, and an answer built on it says so.

*Why:* a confident answer from a stale note is worse than "I do not know". *Related:* P12, [`share-with-your-team`](../playbooks/share-with-your-team.md).

## 2. The harness matters more than the model

Before blaming or switching the model, measure the harness: the instructions, the tools, the checks. Change one variable at a time, keep a hidden holdout set, and never let the model under test be its own judge.

*Why:* in practice a rule change often moved results more than a model change, and sometimes helped one model while hurting another. *Related:* P05, P11, [`measure-your-skills`](../playbooks/measure-your-skills.md).

## 3. A wall between thinking and distribution

The layer that publishes (marketing, newsletters, social posts) translates decisions; it does not make them. Feedback from the audience reaches the thinking layer only through an inbox, never by rewriting decisions directly.

*Why:* without the wall, whatever performs well publicly starts to steer what you believe. *Related:* P03.

## 4. Silence is the default

A system that reports everything is ignored. Few, strong signals: alerts only on a change of state, at most one learning proposal per answer, and most observations end as "nothing to report".

*Why:* attention is the scarcest resource the system spends. *Related:* P05, P11.

## 5. Verb classes for agent permissions

Describe what each agent may do with verbs, not with tools: read, write in its own scope, write derived files, delete, publish, send, drive a browser, write through a connector, run scripts. Least privilege per agent; the high-risk verbs (delete, publish, send, money, credentials) are logged and never autonomous.

*Why:* tool lists change every month; the verbs and their risk do not. *Related:* P00, P03.
