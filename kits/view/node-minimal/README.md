# Minimal view (zero build)

A local web page for your vault: one Node.js file and three static files. No `npm install`, no build step, no framework.

## Run

```bash
node server.mjs /path/to/your/vault
# then open http://localhost:4747
```

Options: `--port 4747`, `--tasks "TODO.md,00_TODO.md"` (which files hold your task list, relative to the vault root), `--public <folder>` (serve another front end, for example a built React app).

## What it does

- **Search:** ranked by title (x10), description (x5) and body (x1). Good descriptions in your frontmatter make it good (P01, P06).
- **Note preview:** the frontmatter description on top, then the note, with a small markdown renderer.
- **Tasks:** open `- [ ]` items from your task files. Ticking one writes `- [x]` back into the markdown file, and only if the line has not changed since it was read.
- **Live:** when a markdown file changes, the page refreshes its tasks and the open note.

## Safety

- Listens on `127.0.0.1` only.
- Reads and writes only `.md` files inside the vault; the only write is ticking a task.
- Holds nothing of its own: stop it, delete it, nothing is lost.

## API (shared with the React path)

| Method | Path | Returns |
|---|---|---|
| GET | `/api/notes` | every note: `path`, `title`, `description`, `status`, `mtime` |
| GET | `/api/search?q=` | up to 50 ranked notes (same fields plus `score`) |
| GET | `/api/note?path=` | `{ path, frontmatter, body }` |
| GET | `/api/tasks` | `{ path, line, done, text, raw }` per task |
| POST | `/api/toggle` | body `{ path, line, text }` (`text` = the `raw` line you read); flips the checkbox |
| GET | `/api/events` | server-sent events: `changed <path>` on every markdown change |

## Adapt it

It is meant to be changed. Ask your agent to add a view (a timeline from dates in frontmatter, a board from a status field, a page per area), and keep the rule: the view reads markdown and writes back only into markdown.
