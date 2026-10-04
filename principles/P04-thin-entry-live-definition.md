# P04. Thin entry point, live markdown definition

**Principle.** Every agent and every skill has two parts: a **thin entry** (name, when to use it, where it points) and a **live definition** in the vault (the actual knowledge in markdown, with a version). The entry always reads the live definition: **the vault always wins.**

**Why.** If the knowledge lived in the platform's own files (plugins, settings), it would not learn, would not be versioned, and would be lost when you change platforms. This way the knowledge is in the vault, and the entry can be written for any platform in a few lines.

**Practice.**
- A skill: `<skill>/CURRENT.md` (live definition), with `LEARNINGS.md` (log), `observations/` (learning inbox), `versions/` (old versions).
- An agent points to skills; anything that can be written as steps is a skill, not agent text.
- The entry says which version ran.

**Check.**
- Is there a skill or command whose entire content lives in the platform file (for example `SKILL.md`) without a live definition?

**Adopt.**
1. The first skill with a live definition (template: `templates/skill-CURRENT.md`).
2. Move existing skills over gradually.

**Platform.** The Agent Skills format (`SKILL.md`) works in both Claude Code and Codex; the entry can be the same in both: "read `<vault>/…/CURRENT.md` and work by it".
