# Skills: shared procedures you can adopt

These are skills from a PAROS in daily use, cleaned of personal data and written so anyone can adopt them. They follow P04: a **thin entry** (`SKILL.md`) and a **live definition** (`CURRENT.md`). As the original skills evolve, new versions appear here from time to time.

## The catalog

| Skill | What it does | Use it when | Principles |
|---|---|---|---|
| [`frontmatter-header`](frontmatter-header/) | Writes or repairs a note's frontmatter, with a description about the content | Your notes are hard to find, or the agent opens too many files to answer a question | P01, P06 |
| [`project-state`](project-state/) | Keeps one current-state file per project or area: where it stands, next step, open questions, decisions | You lose the thread between sessions, or every session starts with "where were we?" | P01, P12 |
| [`adversarial-second-pass`](adversarial-second-pass/) | A fresh-eyes reviewer that tries to break an important result before you rely on it | Meeting notes, decisions, numbers or documents that others will act on | P05, P11 |

Ask your agent, in any language:

> Which PAROS skills would help me most, and how would I use them in my vault?

> Adopt the project-state skill into my vault and set it up for my main project.

More are on the way (see `kits/` for the larger machinery: learning, search, health, secrets, view).

## How a skill becomes yours

A skill is **copied into your vault and lives there**; this repository stays read-only. Your copy learns from your corrections; updates from here arrive as advice.

1. **Adopt.** Your agent copies `CURRENT.md` into your vault (default `PAROS/skills/<name>/CURRENT.md`, or wherever your entry file says skills live), creates `LEARNINGS.md` and an `observations/` folder next to it, and fills in the `upstream:` block in the frontmatter:
   ```yaml
   upstream:
     source: https://github.com/ExarLabs/paros/tree/main/skills/<name>
     version: 1.0.0      # the version you adopted
   ```
2. **Install the entry.** The agent puts `SKILL.md` where your platform looks for skills (Claude Code: `.claude/skills/<name>/SKILL.md`; Codex and other agents: their skills folder, or a line in your vault's `AGENTS.md` that points to the live definition).
3. **Use and teach.** When you correct the skill, the correction becomes a learning packet in `observations/` and changes **your** `CURRENT.md` (P05). Your version moves on: `1.0.0` becomes `1.0.1-local`, and so on.
4. **Upgrade as advice.** After `git pull` in this repository, the agent compares each adopted skill's `upstream.version` with the version here and reads the skill's `CHANGELOG.md` entries in between. Each entry becomes a **suggestion** (a learning packet in your `observations/`, or a line in `PAROS/ADOPTION.md`), judged by your own loop like any other lesson. Your own rules and your `## Constitution` are never overwritten. When you accept a change, `upstream.version` moves forward.
5. **Give back (optional).** If your copy learned something general, you may suggest it upstream, only with your explicit yes, and without personal data.

## The entry pattern

Every `SKILL.md` here does the same four things:
1. find the live definition in your vault (falling back to this repository's copy if not adopted yet);
2. read it;
3. say in one line which version runs and from where ("from your vault" or "from the PAROS reference, not yet adopted");
4. follow it.

This is the same pattern the original PAROS uses for its own skills: **the vault always wins**, and you can always see which version is running.
