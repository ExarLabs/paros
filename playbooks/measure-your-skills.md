---
title: measure-your-skills
date: 2026-10-05
status: active
description: Playbook for a harness bench that measures an agent skill instead of trusting it. Runs the skill on a fixed set of tasks with one or more models, several times each, from the existing subscription, isolated from the vault, and scores the output with deterministic checks plus a judge model from outside the tested one. Tells whether a learned rule really helped and which model is good enough for a skill. The harness (the skill, its rules and the tool around it) matters more than the model.
---

# Playbook: measure your skills

Your agents learn: corrections become rules, skills get new versions. But did the last change actually help, or did it only feel better? And does this skill need the large model, or is a smaller one good enough? A **harness bench** answers both in numbers.

The picture is a test track. The car is the model, the track is a fixed set of tasks, the driving rules are your skill. You change one thing, drive several laps, and count the mistakes.

Why bother: the same model inside a better harness (the skill's instructions, its checks, the tool around it) often does far better than a stronger model inside a weak one. Your PAROS is a personal harness. Measuring it tells you where improvements really come from.

## What you get

- **A fixed task set per skill,** with known good answers, including a few secret (holdout) tasks you never tune against.
- **Repeatable runs** of one skill version with one or more models, several times each, isolated from your vault so nothing else leaks in.
- **Two kinds of score:** deterministic checks (found the expected items, reached the right verdict, broke no hard rule, quoted nothing that was not in the source) and a judge model's ratings (invented claims, faithfulness to the source, quality of questions asked).
- **A report** that puts skill versions and models side by side, with time and tokens per run.
- **A before and after number** for every learned rule, so learning becomes evidence, not belief.

## Before you start

The agent asks you, briefly:
- Which skill do you want to measure first? Pick one that runs often and whose output you can judge (for example: turning a meeting transcript into task cards, classifying incoming requests, drafting replies from a dossier).
- Can you produce five to ten example inputs **with the answer you would accept**? Invented cases are fine to start; real cases only with an approved expected answer, and only on your own machine.
- Which models can you run from your subscription, from the command line?
- Is there a model from **another family** available to act as judge?

You need: the skill's definition as a file, an agent CLI that runs one prompt non-interactively on your subscription (for Claude Code: `claude -p`), and Python.

## Steps

1. **Write the constitution of the bench.** Six rules, recorded with your yes:
   ```
   1. Subscription only. Every model call goes through the signed-in CLI; no API key in the environment.
   2. One variable at a time. Either the skill version changes or the model, never both in one comparison.
   3. Isolated runs. An empty temporary folder, the skill as the system prompt, no tools, no memory, no session saved.
   4. The judge is not the tested model. If they would match, a fallback judge runs.
   5. Secret tasks. Holdout cases are never used to tune the skill; a gain that shows only on the open cases is suspect.
   6. Real data stays home. Real cases run only on your machine, and the results stay in the vault.
   ```
   For Claude Code, rule 1 means: remove any API key variable from the environment of each call, and do not use a flag that forces key-based billing (`--bare` does).

2. **Build the task set.** One folder per case, with the input and a small expectation file:
   ```
   suites/meeting-to-tasks/
     harness.json              which files make up the skill, the run instruction, target models, judge
     cases/inventory-report/   transcript.md + case.json (expected items, expected verdict, holdout: false)
     cases/quote-template/     ...
     cases/quality-check/      ... (holdout: true)
     runs/<run id>/            raw outputs and judge verdicts, per case
     scores.jsonl              one line per run, append-only
     REPORT.md                 the summary table
   ```
   Start with three synthetic cases that cover every branch of the skill (for example: accept, accept with conditions, reject because too big, reject because not ours). Aim for **at least 8 cases** before you let a result block anything.

3. **Ask for compact output.** Have the tested model answer in a small JSON with each item's content and its source (quote or derivation), not in the long human format. It is faster, cheaper, and easier to check. Full-format and compact runs are not comparable; start a new baseline when you switch.

4. **Write the deterministic checks first.** They are cheap and do not drift:
   - expected items found (match on **word stems**, not dictionary forms, especially in inflected languages; "invoic" matches "invoices" where "invoice" may not);
   - correct verdict, and the correct reason for each rejection;
   - hard rule violations (for example: an accepted item whose source is "assumption");
   - **numbers in quotes:** an item marked as a quote that contains a number not present in the source (an added year, a converted unit, a computed duration). This is an invented claim found without any judge.

5. **Add the judge.** A different model (ideally a different family) gets the source and the compact output, and rates invented claims (target: zero), faithfulness and question quality on 1 to 5. Give the judge the skill's own vocabulary, or it will count legitimate terms as inventions. Record the **judge version** on every line: when your rules change, the judge must change with them, and old runs must be judged again before you compare.

6. **Run, cheaply.**
   - in parallel (for example three workers);
   - staged: one open case, one run first; if an expected item or verdict is missing, or invented claims jump against the baseline, the full round does not run;
   - cached: a combination is not run again if the skill text, the case, the CLI version and the exact model id are all unchanged. A CLI update or a model change triggers a new run by itself, even if your skill did not change.
   - token accounting per run, for the tested model and the judge.

7. **Repeat.** Models are noisy. Run every case at least **two or three times**; three cases times two runs shows a direction, not proof. The judge is noisy too: the same output can get different ratings on two passes, so small differences (half an invented claim per run) are noise at small sample sizes.

8. **Read the report.** One row per (skill version, model): found items, correct verdicts, rule violations, bad numbers in quotes, invented claims, faithfulness, time, tokens. Typical findings:
   - a new rule helps the larger model and hurts the smaller one; keep the rule and state the minimum model for the skill;
   - best-of-three with the small model helps only if the selector checks what that model is weak at; otherwise it costs three times the tokens for nothing.

9. **Wire it into learning.** After a learned rule is merged into a skill that has a task set, run the bench in the background against the previous version as baseline. A worse result **does not undo anything automatically**: it becomes a new learning packet with the numbers, reviewed like any other. Only when the set has at least 8 cases and 3 repeats may a worse result block a merge.

## Check that it works

- Run the same skill version twice with the cache on: the second run costs nothing and reports "cached".
- Change one sentence in the skill: only that version is rerun.
- Plant an obvious invented number in one expected quote and score it: the numbers-in-quotes check flags it without the judge.
- Configure the judge to be the tested model: the fallback judge runs instead.
- Open `scores.jsonl`: every line has the skill label, model id, CLI version, judge version and tokens.

## Pitfalls

- **Measuring the bench, not the skill.** The first failures are often the bench's own (word matching, an uncalibrated judge). Fix the instrument before you trust the numbers.
- **Two changes at once.** A new skill version run on a new model tells you nothing about either.
- **A judge that applies yesterday's rules.** After a rule change, recalibrate the judge and re-judge all runs.
- **Small samples treated as proof.** Three cases and two repeats point a direction. Decisions need more.
- **Tuning on the secret cases.** The moment you look at a holdout case to improve the skill, it is no longer secret.
- **The vault leaking into the run.** Without isolation, the model reads your entry file and memory, and you measure your whole setup instead of the skill.
- **Running on paid API calls by accident.** A key left in the environment, or a flag that requires one, turns a free-on-subscription bench into a bill.
- **A judge from the same family.** Better than none, weaker than independent. Add a second family when you can.

## Principles behind it

- [P05](../principles/P05-closed-loop-learning.md): learning needs evidence; the bench turns "it feels better" into a number.
- [P11](../principles/P11-health-contract.md): proof by result, with repeats and a baseline.
- [P04](../principles/P04-thin-entry-live-definition.md): the skill's live definition is what the bench loads, with its version as the label.
- [P00](../principles/P00-constitution-and-boundaries.md): the bench's own constitution, and real data stays on your machine.

## Related

- Kits: [`kits/learn-merge`](../kits/learn-merge/README.md) (merging learned rules, and `judge.py` as an independent judge), [`kits/cognition`](../kits/cognition/README.md) (weighted rules), [`kits/thin-entry`](../kits/thin-entry/README.md) (skill versions).
- Agent: [`agents/maestro`](../agents/maestro/CURRENT.md) (learn-review, which the bench reports to).
- Playbooks: `teach-your-agents`, `independent-judge`, [`report-as-code`](report-as-code.md), [`measure-your-ai-usage`](measure-your-ai-usage.md).
- Guide: [`guides/add-a-skill.md`](../guides/add-a-skill.md) (golden examples).
