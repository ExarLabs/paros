---
title: adversarial-second-pass
date: 2026-10-05
status: active
description: A fresh-eyes reviewer that tries to break an important result before the person relies on it; it rereads the original source, looks specifically for what the result missed or got wrong, and returns evidence-backed findings that are then integrated with the person's approval.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# adversarial-second-pass

A single pass that turns source material into a result (a meeting summary, a document digest, an analysis, a report, a decision memo) reliably catches the skeleton. It is structurally unable to refute its own confident claims. This skill closes that gap: a reviewer with fresh eyes rereads the source and looks **only** for what is missing or wrong.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The reviewer is not the author: it runs in a fresh context that did not produce the result.
- The reviewer refutes; it does not summarise or rewrite the result.
- Every finding carries evidence from the source (a short quote plus a line, page or timestamp).
- No canonical number, decision or commitment is changed without the person's explicit yes.
- Names are never invented: an uncertain person is described by role and marked "to verify".

## When to use

- "Run an adversarial pass", "try to break this", "what did you miss?", "check yourself against the source", "second pass".
- Right after producing an important result from a long source, when the person asks for a second look.
- **Always worth it** when something will be built on the result: a contract, an offer, a service definition, a budget, a public statement; when numbers, commitments or deadlines appear in the source; when legal, compliance, security or politically sensitive threads run through it.
- **Usually skippable:** routine status notes, low-stakes demos, domains where the knowledge base already covers most of what the source says.

## Inputs

1. **Source:** the original, verbatim material (transcript, document, dataset, thread, code).
2. **Result:** the output to be checked.
3. **Context files** (optional): the area's open questions and decisions, so the reviewer can tell "already known" from "new".

If the person names no result, use the most recent one in the relevant area and say which you picked. If either input is uncertain, ask before starting a long review.

## Steps

### 1. Start one reviewer with a strict role

Use the strongest model available. **One** reviewer is enough: in practice most of the value comes from the refuting role itself, not from many lenses, and the cost stays close to one ordinary pass. Start it as a subagent (Claude Code: an Agent call; Codex or other platforms: a fresh session or context). Give it this brief, filled in:

```
You are the adversarial reviewer of an already written result. Your goal is NOT to
summarise the source but to REFUTE the result: find what it LEFT OUT and what it states
WRONGLY.

Order (mandatory):
1. FIRST read the ENTIRE source: <source path>. Read it in chunks if it is long. Skip
   nothing, especially the last third (commitments and deadlines tend to land there).
   Do not open the result yet.
2. THEN read the whole result: <result path>, plus <context files>, so that "already
   known" is judged correctly.
3. Look specifically for:
   - commitments and deadlines (especially near ones) that the result omits;
   - risks nobody named as risks: security, legal, compliance, privacy, political,
     dependence on a single person or supplier;
   - statements recorded as decisions or facts that were only guesses in the source
     (signals: "I think", "probably", "eight or five, not sure");
   - attribution: who said or owns what, wrongly assigned;
   - numbers: rounding, misread amounts, misunderstood units;
   - transcription or extraction errors that put the wrong person, system or term into
     the result;
   - implicit signals that matter for action: tension, hesitation, an unspoken
     dependency.

Rules:
- Be strict: trivia, repetition and small talk are not findings. Only count what could
  change a future decision or piece of work.
- Be strict the other way too: do not report as new what the result already says in
  substance, even in other words.
- Every finding needs evidence: a short quote plus line number, page or timestamp.
- Never invent a name. An uncertain person is a role description marked "to verify".

Your final message is JSON with this schema:
{
  "net_new": [
    { "item": "...", "evidence": "quote + location", "value": "high|medium|low",
      "suggested_home": "open-questions|decisions|result-addendum|task-list|other" }
  ],
  "corrections": [
    { "result_claim": "...", "corrected": "...", "evidence": "quote + location",
      "severity": "high|medium|low", "suggested_home": "..." }
  ],
  "partial_nuances": [ "..." ],
  "summary_one_line": "one sentence: how much and what kind of new knowledge came out"
}
```

### 2. Integrate the findings

From the reviewer's JSON, act on **high** and **medium** items; list **low** items only.

- **net_new, high:** add to the area's open questions (or task list); a near deadline or a security risk also goes at the top of the report.
- **net_new, medium:** an open question, or an addendum at the end of the result.
- **corrections, high or medium:** fix the result in place, and update the decision or glossary it touches.
- **partial_nuances:** append to the matching section of the result, marked as a review clarification.

Where a correction touches a contractual, financial or committed number or decision, do not change it yourself: write it as a proposal and wait for the person's yes.

### 3. Refresh what depends on it

If the vault has a search index or derived views, refresh them for the files you changed (P06).

### 4. Report

- How many high, medium and low findings and corrections.
- The top three to five items, one line each, with their evidence.
- What you integrated and what waits for approval.
- One sentence on the quality of the original result.

## Output

- The reviewer's JSON (kept next to the result or in the area's review folder, if the vault keeps them).
- The integrated changes, and a list of proposals awaiting the person's decision.
- The short report above.

## Pitfalls

- Never let the author context review itself: a reviewer that saw the result being made inherits its blind spots. <!-- rule:R-001 since:2026-06-10 -->
- The reviewer must read the full source before the result; reading the result first anchors it to the result's framing. <!-- rule:R-002 since:2026-06-10 -->
- Do not skim the end of a long source: commitments, deadlines and the real decision tend to come late. <!-- rule:R-003 since:2026-06-10 -->
- One strong reviewer beats a fleet of reviewers on cost and almost matches it on value; add more lenses only when one pass demonstrably missed something. <!-- rule:R-004 since:2026-06-10 -->
- A finding without a quote and a location is not a finding; drop it or send it back. <!-- rule:R-005 since:2026-06-10 -->
- Hedged statements in the source ("probably", "I think") recorded as decisions are the most common and most costly error; check every recorded decision for them. <!-- rule:R-006 since:2026-06-10 -->
- Never overwrite a contractual or committed number or decision without the person's yes, even when the evidence looks clear. <!-- rule:R-007 since:2026-06-10 -->
- When the person rejects or corrects a finding, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-008 since:2026-10-02 -->
