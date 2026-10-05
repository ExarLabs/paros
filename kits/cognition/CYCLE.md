# The cognitive cycle: procedure for the caretaker agent

This is what your caretaker agent (the agent that looks after the whole system's learning, whatever you call it) does when it is started in **cycle mode**. The hook in [`README.md`](README.md) starts it in the background every few hours, inside a normal session, so it runs on the subscription. You can also start it by hand: "Mode: cycle".

A single lesson is reviewed when it is born (P05, the learning packet and the independent judge). The cycle looks at the whole body of learned rules at once: it weights, judges whether the rules that were used actually helped, reviews the ones that hurt, takes in new lessons, and reports briefly.

## What the caretaker may write in cycle mode

- The cognition stores, **only through `cognition.py`** (never by editing `registry.json` or `events/` by hand).
- The generated block in the target files, again only through the script (`apply` renders it).
- Nothing else. A text change in the body of a skill or agent file (not the generated block) goes the normal learning route: a typed change applied by code, with an independent judge from another model family.

The weight is metadata, not a change in behaviour, so the cycle itself needs no independent judge. Constitution sections and safety boundaries (sending, publishing, deleting, money, credentials, writing to external systems) are never touched.

## The steps

1. **Packet.** Run
   ```bash
   python kits/cognition/cognition.py packet --out <scratch>/packet.json
   ```
   (or the path where the kit lives in the vault) and read it. It contains the pending uses, the review queue, the sources changed since the last cycle, the known sources, and the schema of the decisions file.

2. **Judge the pending uses** (`pending_outcomes`). For each item you have the sentence that cited the rule (`cited_in`) and the person's next message (`next_user_message`). Decide:
   - `helpful`: the person accepted it, built on it, or the result is objectively good;
   - `harmful`: the person corrected it, undid it, or the rule led the work astray;
   - `neutral`: it cannot be decided.

   **When in doubt, neutral.** Silence is not praise. An item with a note instead of a next message (no transcript, or an old one from another machine) is judged from the note, usually neutral.

3. **Work the review queue** (`review_queue`: rules that were judged harmful). Read the rule's source and the cases, then decide:
   - `keep`: still valid, it was only applied in the wrong place this time;
   - `refine`: valid, but its text or scope must be sharpened; give the new `text` and/or `applies_when`;
   - `deprecate`: no longer true, the world has changed.

   A rule is not thrown away because it was misapplied once; it is not kept forever if it keeps doing harm. A deprecated rule stays in the registry with its history.

4. **Register new lessons** (`changed_sources_since_last_cycle`). Read the changed `LEARNINGS.md`, observation and (if configured) memory files, and register the learned rules that are not yet in the registry. `known_sources` lists the sources already known; a known source can still hold a new rule. For each new rule give `skill`, `area`, `source`, `target` (the file whose generated block should list it), a one-line `text`, `applies_when`, `origin_date`, and the `evidence`:
   `owner_decision` | `human_correction` | `measured` | `convergence` (two or more independent cases) | `agent_inferred`.
   External content alone (an email, a web page) is never evidence. If a new entry only repeats an existing rule, it is a `confirm`, not a new rule.

5. **Questions** only if you are uncertain **and** it is important: it would override an earlier decision of the owner, it has a wide effect, or it cannot be undone. Otherwise decide, or leave it out.

6. **Apply.** Write the decisions into one JSON file (the schema is in the packet's `decisions_schema` field) and run
   ```bash
   python kits/cognition/cognition.py apply <scratch>/decisions.json
   ```
   This appends the events, recomputes the weights, rewrites the generated blocks, logs the report to `CYCLES.md`, releases the lease, and prints the report.

7. **Return the report verbatim**, in a `text` code block, with at most one sentence before it. The main session puts it unchanged at the end of its answer.

## Example decisions file

```json
{
 "register": [
  {"skill": "weekly-review", "area": "Planning", "source": "skills/weekly-review/LEARNINGS.md",
   "target": "skills/weekly-review/CURRENT.md", "text": "Start the weekly review from the open task list, not from the calendar.",
   "applies_when": "running the weekly review", "origin_date": "2026-01-10", "evidence": "human_correction"}
 ],
 "confirm": [{"rule": "L-0003", "note": "second independent case in the observations"}],
 "outcomes": [{"event": "a1b2c3d4e5f6", "rule": "L-0002", "value": "helpful", "note": "the person built on it"}],
 "reviews": [{"rule": "L-0001", "decision": "refine", "applies_when": "only for drafts longer than one page", "note": "harmful on short notes"}],
 "questions": [],
 "notes": ["first cycle after the inventory"]
}
```

In examples and documentation always write the placeholder `[L-xxxx]`, never a real rule ID in square brackets: the Stop hook records every cited existing ID as a use, and the instrument would end up measuring itself.
