# Kit: cognition (P05, weighted learned rules and the cognitive cycle)

A working reference for the last step of [P05](../../principles/P05-closed-loop-learning.md): learned rules carry a **weight**, the agent marks when a decision depended on one (`[L-xxxx]`), and a background **cognitive cycle** judges whether the rule helped, reviews the ones that hurt, takes in new lessons and reports with a text heat map.

The goal is the same as P05's: remove friction, the moments when a rule is wrong, cannot be applied, or does not exist and something has to be invented.

This kit is optional. Read it, then rebuild or adapt it for the vault; do not copy it blindly.

## The weighting model

Every learned rule has a weight between 0 and 1, computed from its events (never stored by hand).

| Event | Effect |
|---|---|
| **born** | base weight by evidence: owner decision 0.40, human correction 0.35, measured 0.30, convergence (2+ independent cases) 0.30, agent inference 0.15 |
| **confirm** | `w += 0.15 * (1 - w)`: +15% of what remains to 1 |
| **helpful** use | `w += 0.12 * (1 - w)`: +12% of what remains |
| **harmful** use | `w -= 0.30 * w`: -30%, and the rule goes to **review** |
| **neutral** use | only the exposure count grows |
| **idle** | after 60 days without any event, the weight decays 5% per month; rules of human origin (owner decision, human correction) have a floor, so they never fall asleep on their own |
| **dormant** | below 0.12 the rule is no longer listed as active, but it stays in the file and new evidence brings it back |

| Mark | Tier | Weight | Meaning |
|---|---|---|---|
| ░ | seedling | < 0.25 | new or weak evidence; only a suggestion, yields in a conflict |
| ▒ | growing | 0.25 to 0.50 | there is evidence; it is used |
| ▓ | strong | 0.50 to 0.75 | confirmed several times or proven |
| █ | root | 0.75 and above | a foundation of the system |
| ! | review | | it did harm; the next cycle decides about it |
| · | dormant | < 0.12 | not loaded, but kept |
| × | retired | | no longer valid; its history is kept |

A harmful use does not delete anything: the caretaker decides `keep`, `refine` (sharpen the text or scope) or `deprecate`. One bad application is not a reason to drop a rule; repeated harm is.

## Files

| What | Where | Kind |
|---|---|---|
| The engine | `cognition.py` | deterministic, no LLM, standard library only |
| The cycle procedure | [`CYCLE.md`](CYCLE.md) | what the caretaker agent does in cycle mode |
| Rule registry | `registry.json` | canonical: ID, source, text, scope, evidence, text history |
| Events | `events/<host>.jsonl` | canonical, append-only, one writer per machine (safe with file sync) |
| Cycle history | `state.json` | written only by `apply` |
| Lease | `lease.json` | which session is running a cycle (90 minutes) |
| Weights | `weights.json` | derived, can be recomputed at any time |
| Report log | `CYCLES.md` | append-only, for humans |
| Generated block | at the end of each target file, between the `COGNITION:BEGIN` and `COGNITION:END` HTML comment markers | the rule list with weights, rewritten by `render` and `apply` |

The data files are created on first use. Keep them in the vault (they sync); keep them out of a public repository.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `PAROS_COGNITION_DIR` | the script's folder | where the stores live |
| `PAROS_VAULT` | detected upwards from the data folder (`.obsidian`, `.git` or `AGENTS.md`) | the vault root; rule `source` and `target` paths are relative to it |
| `PAROS_LEARNING_ROOTS` | the whole vault | folders (separated by `:` or `;` per platform) scanned for changed `LEARNINGS.md` and `observations/*.md` |
| `PAROS_MEMORY_DIR` | unset | optional: an agent memory folder. Changed rule-type memory files (`feedback_*` or frontmatter `type: feedback` / `reference`) go into the packet, and a rule that targets a memory file gets its ID as a prefix on that file's line in the memory index instead of a generated block |
| `PAROS_MEMORY_INDEX` | `MEMORY.md` | the memory index file name inside the memory folder |
| `PAROS_CYCLE_DOC` | `kits/cognition/CYCLE.md` | the procedure the hook tells the session to follow |
| `PAROS_HOST` | the machine's host name | the name used for the event file and the lease |

## Commands

```bash
python cognition.py report                                   # current state, no cycle
python cognition.py used L-0042 --outcome helpful --note "..." # a manual signal
python cognition.py packet --out packet.json                 # the caretaker's work packet
python cognition.py apply decisions.json                     # the caretaker's decisions, then the report
python cognition.py render                                   # rewrite the generated blocks
python cognition.py due                                      # is a cycle due (JSON)
```

The owner can say at any time "L-0042 was good" or "L-0042 was wrong"; the main session records it with `used --outcome`.

The report is plain text: tier counts, a growth sparkline across cycles, what got stronger or weaker, the review queue, and a heat map with one row per capability and one cell per rule, darker meaning stronger.

## Hooks

### Claude Code

Two hooks in the vault's `.claude/settings.json` (adjust the path to where the kit lives in the vault):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {"hooks": [{"type": "command", "command": "python PAROS/cognition/cognition.py due --hook"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python PAROS/cognition/cognition.py stop-hook"}]}
    ]
  }
}
```

- `UserPromptSubmit` runs `due --hook`: if no cycle ran in the last 4 hours and no other session holds the lease, it takes the lease and adds context telling the session to start the caretaker agent in cycle mode in the background, following `CYCLE.md`, and to append the report to its answer.
- `Stop` runs `stop-hook`: every existing rule cited as `[L-xxxx]` in the answer becomes a pending use, judged in the next cycle from the person's next message.

Both hooks swallow every error silently: a hook must never block the work. The health check (P11) is what notices a cycle that has not run for 48 hours.

### Codex

Codex has no equivalent hooks. Put this in the vault's `AGENTS.md`: at the start of a session run `python <kit>/cognition.py due`; if it says `"due": true` and `"leased": false`, run the cycle (as a background task where available) following `CYCLE.md`. Mark rule use with `[L-xxxx]` as usual and record outcomes with `used` when the person reacts, since there is no Stop hook to do it automatically.

## Why it runs on the subscription, inside a session

The cycle is judgement work: reading what the person said next and deciding whether a rule helped. That needs a capable model, a few times a day, every day. Run as a scheduled API job it would bill API credits on top of the subscription the owner already pays for, and would need an API key stored for an unattended process (one more secret, see P07). Run as a background agent inside a session the owner has open anyway, it uses the subscription, it has the transcripts at hand, and it reports right where the owner is looking. The cost of this choice: no cycle runs while nobody works, which is fine, because nothing new is learned then either.

## Known limits

- Use marking depends on the agent's discipline; an unmarked use earns no credit.
- Transcripts live per machine; a pending use is judged on the machine where it happened (after 14 days elsewhere it is treated as neutral).
- The registry text is a short extract; the authoritative text stays in the source file.
- In documentation and examples always write the placeholder `[L-xxxx]`: the Stop hook records any cited existing ID as a use.
