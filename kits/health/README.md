# Kit: health (P11, no "it works" without proof)

A working reference for [P11](../../principles/P11-health-contract.md): weighted checks that look at the **output** of every automatic process, an end-to-end canary, and alerts that fire only when a check changes state.

Optional. Read it, then rebuild or adapt it for the vault.

## The contract

A process is healthy when a real input actually produces the expected output. Not when it is running, not when its log says "started", not when the documentation says it exists.

The reason is the dominant failure class of a personal agent system: the **silent failure**. A session hook that has written nothing for months. An index that stopped refreshing and kept serving old results. An API key pasted into a note. A generator that writes files without a header. None of these raise an error; each is found only by looking at what came out. So every check here looks at output, and every new automatic process gets a check of its own before it counts as done.

## Files

| What | Where |
|---|---|
| The script | `health_check.py` (standard library only) |
| Canary note | `<vault>/PAROS/health/canary-<host>.md` (machine-written; it must be in the vault, since it tests the vault's own indexing) |
| Per-host state | `~/.paros/health/state.<host>.json` (one writer per machine, safe with file sync if you move it into the vault) |
| Run log | `~/.paros/health/health.log`, one line per run |
| Alerts | the owner's task file, default `<vault>/TODO.md` |

## The checks

| Check | Weight | What it proves | Configured by |
|---|---|---|---|
| `canary` | 3 | **End to end.** Each run writes a unique marker into a note; the next run searches for the previous marker in the search index. Found means writing, indexing and search all work. Two-phase, so the indexer runs on its own schedule in between; if no index build happened since the marker was written, the run waits instead of failing. | `PAROS_INDEX`, `PAROS_HEALTH_DIR` |
| `index_fresh` | 2 | the search index was rebuilt within the limit (default 6 hours) | `--index-max-age`, `PAROS_INDEX_MAX_AGE_H` |
| `secrets` | 3 | no plain secret pattern in the vault: API key formats, tokens, private key headers. Full scan once a day; in between only changed files, plus files that had a hit last time (an unchanged leak stays red). Reports file names and the pattern's name, never the value. | always on |
| `metadata` | 1 | markdown files changed in the last 24 hours start with frontmatter (catches generators and templates that write headerless files) | always on |
| `cognition` | 1 | the cognition kit's cycle ran in the last 48 hours | `PAROS_COGNITION_DIR` ([`kits/cognition`](../cognition/README.md)) |
| `secrets_inventory` | 2 | the secrets kit reports no unknown and no overdue secret | `PAROS_SECRETS_INVENTORY` ([`kits/secrets`](../secrets/README.md)) |
| `backup` | 2 | the backup log was written within the limit (default 48 hours) | `PAROS_BACKUP_LOG`, `--backup-max-age` |

A check returns `ok` (green), `fail` (red), or `n/a` (not configured, or nothing to judge yet). A check that throws is itself a failure: a broken check must not look like a passing one.

## Weights and status

| Weight | Meaning |
|---|---|
| 3 | serious and urgent: a broken chain or a leaked secret; alerts |
| 2 | alerts once |
| 1 | log only |

The run's status: **RED** if any check of weight 2 or more fails, **YELLOW** if only weight 1 checks fail, **GREEN** otherwise.

## Alerting without noise

- **Only on a state change.** When a check of weight 2 or 3 goes from green (or unknown) to red, one line is added to the task file, under the heading `## Now` (or at the end if there is no such heading):
  ```
  - [ ] PAROS health: **secrets** on <host> since <time>: plain secret pattern in 1 file(s): Notes/config.md (AWS access key) <!-- paros-health:<host>:secrets -->
  ```
- **No repeat** while it stays red: the marker comment identifies the open line.
- **On recovery** the same line is ticked and stamped `(recovered <time>)`. It is never deleted; the owner archives it like any done task.
- Weight 1 failures only go to the log.

## Configuration

| Variable | Argument | Default |
|---|---|---|
| `PAROS_VAULT` | `--vault` | the current directory |
| `PAROS_INDEX` | `--db` | `~/.paros/index.db` |
| `PAROS_HEALTH_DIR` | `--health-dir` | `PAROS/health` (inside the vault) |
| `PAROS_HEALTH_STATE_DIR` | `--state-dir` | `~/.paros/health` |
| `PAROS_TASKS` | `--tasks` | `TODO.md` (relative to the vault) |
| `PAROS_TASKS_SECTION` | `--section` | `## Now` |
| `PAROS_COGNITION_DIR` | | unset |
| `PAROS_SECRETS_INVENTORY`, `PAROS_SECRETS_SCRIPT` | | unset; the script defaults to `../secrets/secrets_inventory.py` |
| `PAROS_BACKUP_LOG` | `--backup-log` | unset |
| `PAROS_HOST` | `--host` | the host name |

## Commands

```bash
python health_check.py                 # run, update state, alert on change
python health_check.py --dry-run       # print only: no canary, no state, no alert
python health_check.py --json          # one JSON object
python health_check.py --only secrets  # a subset, comma separated
```

## Scheduling

Run it every few hours, and run the search kit's `index.py` more often than that (the canary needs at least one index build between two health runs).

- **cron (Linux, macOS):**
  ```
  */30 * * * *  cd ~/paros-kits/search && PAROS_VAULT=~/vault python3 index.py --quiet
  0 */4 * * *   PAROS_VAULT=~/vault python3 ~/paros-kits/health/health_check.py >/dev/null
  ```
- **Windows Task Scheduler:** two tasks (`python index.py --quiet` every 30 minutes, `python health_check.py` every 4 hours), with `PAROS_VAULT` set as a user environment variable.
- **A session hook** (Claude Code `SessionStart`, or an instruction in `AGENTS.md` for Codex): run `health_check.py --json` at the start of a session and mention a RED status. This only runs while someone works, so pair it with the OS scheduler if the vault has unattended processes.

A scheduler can itself die silently. The `index_fresh` check covers the indexer's scheduler; for the health check's own schedule, the run log's last line tells you when it last ran, and a session hook that reads it closes the loop.

## Adding a check

1. **Start from a failure.** Add a check when a silent failure happened (its lesson becomes a check), or when a new automatic process is born. No new automatic process without its check.
2. **Look at the output, not at the process.** Not "is the service running" but "did a file it should have written in the last N hours appear", "does the index contain what was written", "does the log have a line after the last session". If you cannot name the output, the process is not understood yet.
3. Write a function `check_<name>(c)` that returns `(ok, detail)`: `True`, `False`, or `None` when it does not apply. Keep `detail` short, with file names and counts, never secret values.
4. Add it to `CHECKS` with a weight: 3 if the damage grows while nobody looks, 2 if it should be fixed this week, 1 if a log line is enough.
5. Make it fail on purpose once (break the input) and see the alert line appear; fix it and see the line ticked. A check that has never been red is not proven either.

## Platforms

| Part | Claude Code | Codex | Elsewhere |
|---|---|---|---|
| `health_check.py` | yes | yes | any Python 3.8+ |
| Scheduling | a hook or the OS scheduler | the OS scheduler, or `AGENTS.md` at session start | the OS scheduler |

## Known limits

- The secret patterns cover common key formats only; a password in plain prose is not found. Extend `SECRET_PATTERNS` with the providers you use.
- The canary needs the search kit's index (or any FTS5 index with a `notes_fts` table and a `meta.built_at` row).
- One machine, one state file: on several machines, each runs its own checks, and alert lines carry the host name.
