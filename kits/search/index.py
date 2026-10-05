#!/usr/bin/env python3
"""PAROS search kit (P06): a standalone full-text indexer, kit version 0.1.0.

Builds a SQLite FTS5 database from the markdown files of a vault: path, title,
description, tags and body. The database lives OUTSIDE the vault (it is derived,
P01, and can be rebuilt at any time), so it never syncs and never conflicts.
Incremental: only files whose modification time or size changed are re-read;
deleted files are dropped. Standard library only.

    python index.py                 # incremental update
    python index.py --full          # drop everything and rebuild
    python index.py --vault ~/notes --db ~/.paros/index.db

Configuration (arguments win over environment):
    PAROS_VAULT        the vault root (default: the current directory)
    PAROS_INDEX        the database file (default ~/.paros/index.db)
    PAROS_INDEX_SKIP   extra folder names to skip, separated by commas
"""
import argparse
import datetime as dt
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

SKIP_DIRS = {".git", ".obsidian", ".trash", ".venv", "venv", "node_modules", "__pycache__", ".claude"}
MAX_BYTES = 2_000_000
SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    path TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    tags TEXT,
    mtime REAL,
    size INTEGER
);
CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    path UNINDEXED, title, description, body, tags,
    tokenize = 'unicode61 remove_diacritics 2'
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def default_db():
    return Path(os.environ.get("PAROS_INDEX") or Path.home() / ".paros" / "index.db").expanduser()


def default_vault():
    return Path(os.environ.get("PAROS_VAULT") or os.getcwd()).expanduser()


def skip_dirs():
    extra = {s.strip() for s in os.environ.get("PAROS_INDEX_SKIP", "").split(",") if s.strip()}
    return SKIP_DIRS | extra


def split_frontmatter(text):
    """Returns (fields, body). A tiny reader for the flat keys the index needs;
    not a YAML parser, and it never needs to be one."""
    if not text.startswith("---"):
        return {}, text
    end = re.search(r"^---\s*$", text[3:], re.M)
    if not end:
        return {}, text
    head = text[3:3 + end.start()]
    body = text[3 + end.end():]
    fields, key = {}, None
    for line in head.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1).lower(), m.group(2).strip()
            fields[key] = val
        elif key and re.match(r"^\s+-\s+", line):
            # a block list, for example tags written one per line
            fields[key] = (fields[key] + ", " if fields[key] else "") + re.sub(r"^\s+-\s+", "", line).strip()
    for k, v in fields.items():
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if v.startswith("[") and v.endswith("]"):
            v = ", ".join(x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip())
        fields[k] = v
    return fields, body


def walk(vault, skips):
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in skips]
        for f in files:
            if f.lower().endswith(".md"):
                p = Path(root) / f
                yield p.relative_to(vault).as_posix(), p


def open_db(db):
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.executescript(SCHEMA)
    return con


def build(vault, db, full=False, quiet=False):
    vault = vault.resolve()
    if not vault.is_dir():
        sys.exit("vault not found: %s" % vault)
    con = open_db(db)
    if full:
        con.execute("DELETE FROM notes")
        con.execute("DELETE FROM notes_fts")
    known = {p: (m, s) for p, m, s in con.execute("SELECT path, mtime, size FROM notes")}
    seen, added, updated = set(), 0, 0
    t0 = time.time()
    for rel, p in walk(vault, skip_dirs()):
        try:
            st = p.stat()
        except OSError:
            continue
        seen.add(rel)
        if known.get(rel) == (st.st_mtime, st.st_size):
            continue
        if st.st_size > MAX_BYTES:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        fm, body = split_frontmatter(text)
        title = fm.get("title") or p.stem
        desc = fm.get("description", "")
        tags = fm.get("tags", "")
        con.execute("DELETE FROM notes_fts WHERE path = ?", (rel,))
        con.execute("INSERT INTO notes_fts (path, title, description, body, tags) VALUES (?, ?, ?, ?, ?)",
                    (rel, title, desc, body, tags))
        con.execute("INSERT OR REPLACE INTO notes (path, title, description, tags, mtime, size) VALUES (?, ?, ?, ?, ?, ?)",
                    (rel, title, desc, tags, st.st_mtime, st.st_size))
        if rel in known:
            updated += 1
        else:
            added += 1
    gone = [p for p in known if p not in seen]
    for rel in gone:
        con.execute("DELETE FROM notes WHERE path = ?", (rel,))
        con.execute("DELETE FROM notes_fts WHERE path = ?", (rel,))
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    con.executemany("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
                    [("built_at", now), ("vault", str(vault)), ("kit_version", "0.1.0")])
    con.commit()
    total = con.execute("SELECT count(*) FROM notes").fetchone()[0]
    con.close()
    if not quiet:
        print("Index %s: %d notes (%d new, %d changed, %d removed) in %.2f s"
              % (db, total, added, updated, len(gone), time.time() - t0))
    return {"total": total, "added": added, "updated": updated, "removed": len(gone)}


def main():
    ap = argparse.ArgumentParser(description="PAROS search kit: build or update the vault's FTS5 index")
    ap.add_argument("--vault", type=Path, default=None, help="vault root (default: PAROS_VAULT or the current directory)")
    ap.add_argument("--db", type=Path, default=None, help="database file (default: PAROS_INDEX or ~/.paros/index.db)")
    ap.add_argument("--full", action="store_true", help="drop the index and rebuild it from scratch")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    build((a.vault or default_vault()).expanduser(), (a.db or default_db()).expanduser(), a.full, a.quiet)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
