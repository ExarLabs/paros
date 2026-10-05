# Skills: shared procedures you can adopt

These are skills from a PAROS in daily use, cleaned of personal data and written so anyone can adopt them. They follow P04: a **thin entry** (`SKILL.md`) and a **live definition** (`CURRENT.md`). As the original skills evolve, new versions appear here from time to time.

## The catalog

| Skill | What it does | Use it when | Principles |
|---|---|---|---|
| [`frontmatter-header`](frontmatter-header/) | Writes or repairs a note's frontmatter, with a description about the content | Your notes are hard to find, or the agent opens too many files to answer a question | P01, P06 |
| [`project-state`](project-state/) | Keeps one current-state file per project or area: where it stands, next step, open questions, decisions | You lose the thread between sessions, or every session starts with "where were we?" | P01, P12 |
| [`adversarial-second-pass`](adversarial-second-pass/) | A fresh-eyes reviewer that tries to break an important result before you rely on it | Meeting notes, decisions, numbers or documents that others will act on | P05, P11 |
| [`portfolio`](portfolio/) | A weekly overview of all your projects and areas: what moved, what is stuck, what needs you | You run several projects in parallel and lose the overview | P01, P12 |
| [`think`](think/) | Thinks a hard question through with several AIs at once (researcher, strategist, validator), with a state file as the durable memory | Strategy, research or a decision where one model's answer is not enough | P01, P05 |
| [`transcribe`](transcribe/) | Audio, video or YouTube to text (Groq Whisper), with a completeness check; the raw transcript is kept as evidence | Meetings, voice memos, interviews, podcasts | P01, P11 |
| [`speed-reader`](speed-reader/) | Reads a book, article or episode into a structured note: thesis, chapters, quotes with sources, questions | You want the substance of something long, in your vault, searchable | P01, P06 |
| [`language-editor`](language-editor/) | A native-quality editor for any language; your own language rules live in `LOCAL.md` | Texts that go out to people: posts, letters, course material | P04 |

Ask your agent, in any language:

> Which PAROS skills would help me most, and how would I use them in my vault?

> Adopt the project-state skill into my vault and set it up for my main project.

More are on the way (see `kits/` for the larger machinery: learning, search, health, secrets, view).

## Recipe and spice

A skill has two parts. **The recipe** (`CURRENT.md`) is the general procedure: shared here, improved over time. **The spice** (`LOCAL.md`) is yours: your names, accounts, folders, tone, language rules. Where a skill needs personal settings, it ships a `LOCAL.example.md` with made-up values; at adoption you copy it to `LOCAL.md` and fill it in. `LOCAL.md` never leaves your vault, and updates from here never touch it.

## How a skill becomes yours

A skill is **copied into your vault and lives there**; this repository stays read-only. Your copy learns from your corrections; updates from here arrive as advice.

1. **Adopt.** Your agent copies `CURRENT.md` into your vault (default `PAROS/skills/<name>/CURRENT.md`, or wherever your entry file says skills live), creates `LEARNINGS.md` and an `observations/` folder next to it, and fills in the `upstream:` block in the frontmatter:
   ```yaml
   upstream:
     source: https://github.com/ExarLabs/paros-advisor/tree/main/skills/<name>
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
