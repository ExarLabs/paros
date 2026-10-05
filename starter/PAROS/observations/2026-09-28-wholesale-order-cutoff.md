---
title: 2026-09-28-wholesale-order-cutoff
date: 2026-09-28
author: Alex Example
status: draft
schema: skill-observation.v1
description: Example learning packet: the owner corrected the agent for telling a cafe the weekend wholesale cutoff was Friday; the proposed rule is to always read the cutoff from the wholesale note.
id: 8c4e0146-a92f-473b-89d0-c00a7f915c10
target: Areas/Bakery/Wholesale orders.md, section "Terms"
tags: [learning, observation, example]
---

# Learning packet: wholesale order cutoff

**Context.** Drafting a reply to Fernhill Cafe about a Saturday order, the agent wrote that weekend orders close on Friday.

**Lesson.** The owner corrected it: weekend orders close on **Thursday at 12:00**. The agent guessed from a general pattern instead of reading the vault.

**Proposed change.** Add a rule to the Alfred viewpoint: "Before stating an order cutoff, delivery day or price to a customer, read it from the bakery area note; never infer it."

**Target.** The agent definition's rules section; the fact itself stays in `Areas/Bakery/Wholesale orders.md` (P12).

**Evidence.** An explicit human correction in the session of 2026-09-28 (the strongest kind, P05).

**Status.** Waiting for Maestro's review. If accepted, the rule gets an ID (`L-0001`) and starts as a seedling.
