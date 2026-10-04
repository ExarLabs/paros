# How to turn a repeated task into a skill

A skill is a procedure the agent can follow the same way every time, and that improves with use. Principles: P04 (thin entry, live definition), P05 (learning).

## When

When you have explained the same multi-step task to an agent the **second** time. The first time is a conversation; the second time is a pattern.

## Steps

1. **Live definition in the vault:** `<your-skills-folder>/<skill>/CURRENT.md` (template: `templates/skill-CURRENT.md`), with `LEARNINGS.md`, an `observations/` folder, and later `versions/`.
2. **Constitution:** a few lines that only you change (what the skill must always or never do).
3. **Thin entry for your platform:** a `SKILL.md` (works in Claude Code and Codex) that says when to use the skill and tells the agent to read `CURRENT.md` and report its version.
4. **Learning:** when you correct the skill's output, the agent writes a learning packet into `observations/`; the review step turns it into a typed change of the definition (P05).
5. **Check:** if the skill produces a file or a result, keep one or two accepted examples (`golden/`) to compare new versions against.

## Determinism

If the skill always does the same steps the same way, part of it belongs in a script, not in the prompt (P08, "state in SaaS, judgment in AI"). Keep the judgment in the skill, move the mechanics to code.

## Ask your agent

> Turn what we just did into a PAROS skill: live definition, constitution, thin entry, learning inbox.
