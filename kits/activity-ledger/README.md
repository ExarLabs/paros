# Kit: activity-ledger (P01 and P11, a "what did I do" log nobody has to write)

A working reference for a **passive activity log**: every work session leaves one line behind without anyone writing it, and later you can ask "what did I do this week?" or "what happened on Wednesday?" and get an answer built from evidence, not memory.

Optional. Read it, then rebuild or adapt it for the vault.

## Why

Two reasons, one practical and one human.

- **Practical.** Reviews, invoices, status updates and "where did that week go" all need a record of what was done. Manual time logs die within a week. Derive the record instead of asking for it.
- **Human.** The recurring feeling of "I am not doing enough" is rarely checked against facts. A ledger shows the actual output, quietly.

## The two layers

| Layer | Where | What | Written by |
|---|---|---|---|
| **Ledger** (raw) | `<vault>/PAROS/activity/YYYY-MM.<machine>.md` | append-only, one line per big event, **one file per machine** | the session-end hook, agents, you |
| **Journal** (digested) | `<vault>/PAROS/journal/YYYY/MM-Month/YYYY-MM-DD.md` | one day file, area-tagged entries a person reads | the hook (when an AI summary exists), agents, you |

Line formats:

```
ledger:   - 2030-05-14T17:42 · session · session · Reworked the course sign-up form and its thank-you page.
journal:  - 17:42 · [work] · work · Reworked the course sign-up form and its thank-you page.
```

The journal day file ends with a `## Notes` section for free text; entries are inserted above it.

### Why markdown, why one file per machine

A vault usually syncs across machines through a file sync service. That rules out two obvious designs:

- **Git as the source:** a local repository per machine, not shared between them, so each machine sees half the truth.
- **A database file under sync:** last writer wins, so one machine's writes can vanish, or a conflicted copy appears that nothing reads.

Markdown sharded **per machine** avoids both: each machine appends only to its own file, two machines never write the same file, and the recap merges all shards by timestamp. A database may still exist as a cache for a dashboard, but it is not the ledger.

## Files

| What | Where |
|---|---|
| The script | `ledger.py` (standard library only, Python 3.9+) |
| The hook | one entry in your vault's `.claude/settings.json` (below) |
| Ledger and journal | in the vault, under `PAROS/` by default |

## Configuration

| Variable | Default |
|---|---|
| `PAROS_VAULT` | `$CLAUDE_PROJECT_DIR`, else the current folder |
| `PAROS_LEDGER_DIR` | `<vault>/PAROS/activity` |
| `PAROS_JOURNAL_DIR` | `<vault>/PAROS/journal` |
| `PAROS_LEDGER_AREAS` | `work,personal,system,other` (your area slugs; the last resort is `other`) |
| `PAROS_HOST` | the host name, slugified (set it if your host name is ugly or changes) |
| `PAROS_LEDGER_SUMMARY` | `cli`: summarize with the Claude Code CLI; `off`: never |
| `PAROS_LEDGER_MODEL` | `haiku` |
| `PAROS_LEDGER_LANG` | `English` (the language of the summaries) |

## Commands

```bash
python ledger.py append  --summary "Published the spring newsletter" --source manual --category publish
python ledger.py journal --text "Agreed the new delivery date with the printer" --area work --kind decision
python ledger.py recap                         # today
python ledger.py recap --days 7                # the last seven days
python ledger.py recap --since 2030-05-12 --until 2030-05-16 --json
python ledger.py hook                          # SessionEnd hook: hook JSON on stdin
python ledger.py hook --transcript t.jsonl --dry-run   # test the hook on a saved transcript
```

Every writer takes `--dry-run`. Categories are a convention, not a schema: `session`, `build`, `fix`, `publish`, `decision`, `note`, `capture`. Journal kinds are `work`, `mail`, `decision`.

## The session-end hook (Claude Code)

Add to the vault's `.claude/settings.json` (project scope, so it runs only for sessions in this vault):

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/PAROS/kits/activity-ledger/ledger.py\" hook || python \"$CLAUDE_PROJECT_DIR/PAROS/kits/activity-ledger/ledger.py\" hook"
          }
        ]
      }
    ]
  }
}
```

Adjust the path to where the script lives in your vault. The `|| python` fallback covers machines where only `python` exists.

What the hook does:

1. Reads the session transcript the hook payload points to.
2. Builds a digest: **all of the person's requests** (code blocks stripped), plus short tails of the answers. Requests are the cleanest signal of what the session was about, and they are hard for a summary model to echo.
3. If the `claude` CLI is available and signed in, asks a small model for one area slug and a one or two sentence factual summary, on the person's existing subscription. No API key is involved.
4. Writes the summary to the ledger and, with its area, to the journal.
5. Without a summary it writes a plain "session ended (N requests)" line to the **ledger only**; a content-free line in the journal is noise.
6. Exits 0 whatever happens. A hook must never block a session from ending.

**Codex and other agents:** there is no equivalent end-of-session hook everywhere. Call `ledger.py append` (or `journal`) at the end of meaningful work from the agent's own instructions, or run a small scheduled job that summarizes the day.

## Reading it back: the recap

`ledger.py recap` is read-only. It merges all machine shards for the window, sorted by time, lists the journal entries and the machines seen. An agent turns that into a short human answer: what was done, grouped by area, with the decisions called out. When the person is hard on themselves, the recap shows the actual output without commentary.

## Pitfalls

- **Silent death on Windows.** A hook that calls `bash` from Python can start the WSL bash in `System32` instead of Git Bash; it fails without a word, and one machine stops logging for months. This kit is pure Python for that reason. If you add shell helpers, resolve the full path of the right bash.
- **The hook environment is not your shell.** Desktop apps may not pass user environment variables (an API key, for example) to hooks. A design that needed an API key logged "no summary" for months before anyone looked. The subscription CLI avoids the key entirely.
- **Recursion.** The summarizer is itself a Claude Code session. Run it from a folder **outside** the vault, so the vault's project hooks do not fire again, and keep a guard variable (`PAROS_LEDGER_INNER`) that makes the hook exit at once inside it.
- **"Not logged in."** When the CLI is not signed in on a machine, the summary fails and the ledger gets the plain line. Check the ledger once after setup on each machine.
- **The summary model continues the transcript** instead of summarizing it if fed raw code and tool output. Feed requests, strip code, and say in the prompt that the digest is data.
- **No proof, no log.** "The hook is configured" is not "the hook writes". Add a health check (`kits/health`) that fails when the newest ledger line on a machine is older than, say, three days of active use.
- **The journal stops when nothing reads it.** If no dashboard or recap uses the digested layer, it quietly goes stale. Keep the ledger as the minimum, and treat the journal as optional.

## Principles

- **P01, markdown is the source of truth.** The ledger and the journal are plain files any tool can read; any database built from them is a cache.
- **P11, proof of work.** A passive feed needs a check that looks at its output, because its failure mode is silence.
- **One writer per file.** Per-machine shards make file sync safe without locks.
- **Derive, do not ask.** The person never has to log; the system records, and the person can still add a line by hand.
- **Privacy.** The ledger holds one-line summaries, not transcripts. The summary goes to the same model provider the session already used; set `PAROS_LEDGER_SUMMARY=off` for vaults where even that is too much.
