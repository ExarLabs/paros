# Kit: thin-entry

**Principle:** [P04, thin entry and live definition](../../principles/P04-thin-entry-live-definition.md), with [P05](../../principles/P05-closed-loop-learning.md) and [P09](../../principles/P09-forgetting-and-archiving.md) for versions and learning. **Platform:** the scripts are independent (Python 3.8+, standard library only); the generated entry is an Agent Skills `SKILL.md`, read by Claude Code and Codex.

Three small scripts around one idea: the knowledge of a skill lives in a versioned markdown file in your vault (`CURRENT.md`), and the file your platform loads is a thin entry that finds it.

| File | What it does |
|---|---|
| [`build_entry.py`](build_entry.py) | Writes a `SKILL.md` thin entry for one `CURRENT.md`, or for every `CURRENT.md` under a folder. Optionally embeds a sha-locked fallback snapshot. |
| [`promote.py`](promote.py) | Bumps a live definition's version (patch, minor, major), snapshots the old one into `versions/`, logs a row in `LEARNINGS.md`. Refuses a changed Constitution unless the owner allows it. |
| [`digest.py`](digest.py) | Scans all skills and their `observations/` folders and says which need a review, and why. |

Like every kit, this is a reference. Read it, then rebuild or adapt it for your own vault; do not copy it in blindly.

## The pattern: the vault always wins

Every generated entry tells the agent to do the same things, in order:

1. **Locate** the live definition. First match wins, and a candidate counts only if the definition file exists under it:
   1. the `PAROS_VAULT` environment variable;
   2. `CLAUDE_PROJECT_DIR` (the folder Claude Code was started in);
   3. the current working directory;
   4. the folder named on the first line of `~/.paros/vault`, a one-line config file;
   5. optionally, a path you pass with `--default-vault` at build time (fine for a private build, avoid it in anything you share).
2. **Check integrity.** The file must be readable, have a `version:` in its frontmatter, and have a body of at least half its length at build time. A sync service can leave a half-downloaded or placeholder file; a file that fails counts as unavailable.
3. **Report the version before any work.** Exactly one of four cases:

   | Case | What the agent says | What runs |
   |---|---|---|
   | vault newer | `the vault has v<X>, newer than the built-in v<B>` | the vault |
   | same | `the vault has v<B>, the same as the built-in` | the vault |
   | vault older | `the vault has v<X>, older than the built-in v<B> ... working from the vault anyway` | the vault |
   | vault unavailable | `the live definition is unavailable (<reason>)` | the fallback snapshot, or nothing if none is embedded |

4. **Work** by the chosen definition; its `## Constitution` always wins.
5. **End** with one line: `<name> v<X> (vault|fallback) ran`. You always see which version ran, and from where.

### Why not "the highest version wins"

It sounds safer to run whichever copy has the higher version number. It is not. Your vault is where you fix things, and you do not always bump the version when you do: a quick hand edit, a rule fixed in the middle of a session, a learning applied without a promote. Under "highest version wins", a packaged plugin built last month at v1.4.0 would silently override your vault at v1.3.2 that already contains today's fix, and the fix would be lost without anyone noticing. Under "the vault always wins", the worst case is a visible line saying the vault looks older than expected, which is exactly what you want to know (usually: the vault has not synced yet).

## When to embed a fallback

Use `--fallback` only for entries that **travel without the vault**: a packaged plugin you install on another machine, share with a colleague, or use in a cloud session that cannot see your files. Then the entry still works, and it says plainly that it is running a snapshot that may be old.

For entries that live inside the vault (for example `.claude/skills/<name>/SKILL.md` in the vault itself), leave the fallback out: the vault is always there, and a second copy of the knowledge would only invite edits in the wrong place. Without a fallback, an unavailable vault makes the entry stop and say how to point it at the vault.

The fallback block is generated. Its header records the source, the version and a sha of the content; `build_entry.py --check` reports any hand edit in it (the sha no longer matches), because the next build would discard it. Fix the source instead.

## Commands

**Build entries.** One skill, or a whole folder:
```bash
python build_entry.py ~/vault/PAROS/skills/meeting-notes/CURRENT.md --vault-root ~/vault
#   meeting-notes   v1.0.0   new   -> entries/meeting-notes/SKILL.md

python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ~/vault/.claude/skills
```
`--vault-root` (default: `$PAROS_VAULT`, else the nearest folder above with `.obsidian`, `AGENTS.md` or `CLAUDE.md`) is used to write the definition's path relative to the vault, so the entry carries no machine path. The skill name comes from `entry_name:` in the frontmatter or the folder name; the description from `entry_description:` or `description:`. `--stdout` prints a single entry instead of writing it.

**A packaged plugin with a fallback, and a check before you ship:**
```bash
python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ./my-plugin/skills --fallback
python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ./my-plugin/skills --fallback --check
#   meeting-notes   v1.1.0   needs rebuild (changed)
#   Check done. Problems: 1
```

**Promote a version** after you changed a live definition by hand or with `learn_merge.py`:
```bash
python promote.py ~/vault/PAROS/skills/meeting-notes patch --note "action items now carry a due date"
# {"ok": true, "from": "1.0.0", "to": "1.0.1", "snapshot": "versions/v1.0.0.md", "constitution_changed": false, ...}

python promote.py ~/vault/PAROS/skills/meeting-notes minor --note "..." --dry-run
python promote.py --list ~/vault/PAROS/skills
```
- `versions/v<old>.md` gets the file exactly as it was before the bump. An existing snapshot is never overwritten; if one exists with different content, `v<old>+pre-<timestamp>.md` is written next to it (the same convention as `kits/learn-merge`).
- The `## Constitution` section is compared with the latest snapshot in `versions/`. If it changed, the promote is refused (exit code 2) unless `--allow-constitution` is given. **Only the owner gives that flag;** an agent never adds it on its own. With no earlier snapshot there is nothing to compare against, so the first promote of a skill sets the baseline.
- `LEARNINGS.md` gets one row in the `## Version log (promote.py)` table: date, from, to, note, and whether the Constitution changed.

**Digest the learning inboxes:**
```bash
python digest.py ~/vault/PAROS/skills                   # print
python digest.py ~/vault/PAROS/skills --out ~/vault/PAROS/SKILL_DIGEST.md
python digest.py --json                                 # uses $PAROS_SKILLS, else $PAROS_VAULT, else .
```
A pending packet is a `.md` (with frontmatter) or `.json` file directly in `observations/`, not marked `status: applied | rejected | done | processed | archived`. A skill is flagged when it has a `severity: high` packet, two or more packets with the same `proposes:`, five or more pending, the oldest older than 30 days, or the inbox close to its cap (16 of 20). All thresholds are flags. The digest also lists which skills do not learn yet (no `observations/` folder).

## How it fits skill adoption

[`skills/README.md`](../../skills/README.md) describes how a shared skill becomes yours: its `CURRENT.md` is copied into your vault with an `upstream:` block (`source`, `version`), and a `SKILL.md` entry is installed where your platform looks for skills. This kit is the machinery behind those steps:

- **Install the entry:** `build_entry.py` writes the entry for your adopted copy, pointing at your vault's path, not at this repository. Rebuild it when you move the skill.
- **Your version moves on:** when your copy learns, `promote.py` records the new version and keeps the old one. The `upstream.version` field is left alone: it says which reference version you adopted, and only moves when you accept an upstream change (step 4 of the adoption guide).
- **Upgrade as advice:** suggestions from an upstream `CHANGELOG.md` arrive as learning packets in `observations/`, so `digest.py` shows them next to your own lessons, to be judged by the same loop.

## Platforms

| Part | Claude Code | Codex | Other agents |
|---|---|---|---|
| Generated `SKILL.md` (name and description frontmatter) | `.claude/skills/<name>/SKILL.md`, or a plugin's `skills/` | its skills folder | a line in the vault's `AGENTS.md` that points to the live definition |
| `CLAUDE_PROJECT_DIR` in the lookup | set by Claude Code | not set, the next candidate applies | not set |
| Scripts | any OS with Python 3.8+ | same | same |
