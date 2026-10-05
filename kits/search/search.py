#!/usr/bin/env python3
"""PAROS search kit (P06): ranked vault search from the FTS5 index, kit version 0.1.0.

Opens the index built by index.py read-only. If there is no index (a new machine,
a cloud session), it falls back to a ranked walk over the vault's files.

    python search.py "invoice reminder"
    python search.py "garden plan" --area Home --limit 5
    python search.py "budget" --json
    python search.py --status          # which index, how old, how big

The query's words go into the index as OR-ed prefix terms (so "plan" also finds
"planning" and "plans"), stopwords drop out, and the ranking weights the title (10)
and the description (5) above the body (1). Give 2 to 4 characteristic word stems,
not the whole question.

Configuration (arguments win over environment):
    PAROS_VAULT   the vault root, for the file-walk fallback (default: the current directory)
    PAROS_INDEX   the database file (default ~/.paros/index.db)
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

# Small example lists: English, plus Hungarian to show a second language. Extend
# them for the vault's own languages; keep them short (only words that carry no meaning).
STOPWORDS = {
    "en": {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are", "was",
           "what", "how", "where", "when", "which", "who", "why", "do", "did", "we", "about", "it"},
    "hu": {"a", "az", "egy", "es", "és", "hogy", "nem", "is", "de", "mi", "mit", "van", "volt", "meg",
           "hol", "mikor", "hogyan", "miert", "miért", "melyik", "ki"},
}
ALL_STOPWORDS = set().union(*STOPWORDS.values())
SKIP_DIRS = {".git", ".obsidian", ".trash", ".venv", "venv", "node_modules", "__pycache__", ".claude"}
# bm25 column weights, in table order: path (unindexed), title, description, body, tags
WEIGHTS = (0.0, 10.0, 5.0, 1.0, 2.0)


def default_db():
    return Path(os.environ.get("PAROS_INDEX") or Path.home() / ".paros" / "index.db").expanduser()


def default_vault():
    return Path(os.environ.get("PAROS_VAULT") or os.getcwd()).expanduser()


def terms_of(q):
    words = [w.lower() for w in re.findall(r"\w+", q, re.UNICODE)]
    return [w for w in words if w not in ALL_STOPWORDS] or words


def fts_expr(terms):
    return " OR ".join('"%s"*' % t.replace('"', "") for t in terms) or '""'


def connect_ro(db):
    return sqlite3.connect("file:%s?mode=ro" % db.resolve().as_posix(), uri=True)


def search_index(db, terms, area, limit):
    con = connect_ro(db)
    sql = ("SELECT n.path, n.title, n.description, "
           "snippet(notes_fts, 3, '[', ']', ' ... ', 12), bm25(notes_fts, %s) AS r "
           "FROM notes_fts JOIN notes n ON n.path = notes_fts.path "
           "WHERE notes_fts MATCH ? " % ", ".join(str(w) for w in WEIGHTS))
    args = [fts_expr(terms)]
    if area:
        sql += "AND n.path LIKE ? "
        args.append("%" + area + "%")
    sql += "ORDER BY r LIMIT ?"
    args.append(limit)
    rows = con.execute(sql, args).fetchall()
    con.close()
    return [dict(path=p, title=t or "", description=d or "", snippet=(s or "").replace("\n", " "), score=round(-r, 2))
            for p, t, d, s, r in rows]


def search_files(vault, terms, area, limit):
    """Fallback without an index: walk the files, score by how many terms hit,
    with extra weight for hits in the header and the file name."""
    out = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = Path(root) / f
            rel = p.relative_to(vault).as_posix()
            if area and area.lower() not in rel.lower():
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            low = txt.lower()
            hit = [t for t in terms if t in low]
            if not hit:
                continue
            head = low[:1500]
            score = len(hit) * 3 + sum(2 for t in hit if t in head) + sum(1 for t in hit if t in f.lower())
            score += min(sum(low.count(t) for t in hit), 20) / 10
            m = re.search(r"^description:\s*(.*)$", txt[:3000], re.M)
            out.append(dict(path=rel, title=p.stem, description=(m.group(1).strip().strip("\"'") if m else ""),
                            snippet="", score=round(score, 2)))
    out.sort(key=lambda r: -r["score"])
    return out[:limit]


def status(db):
    if not db.is_file():
        print("No index at %s; search falls back to a file walk. Build one: python index.py" % db)
        return
    con = connect_ro(db)
    n = con.execute("SELECT count(*) FROM notes").fetchone()[0]
    meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
    con.close()
    built = meta.get("built_at")
    age = ""
    if built:
        t = dt.datetime.fromisoformat(built)
        hours = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600
        age = " (%.1f hours ago)" % hours
    print("Index:      %s" % db)
    print("Vault:      %s" % meta.get("vault", "?"))
    print("Notes:      %d" % n)
    print("Size:       %.1f MB" % (db.stat().st_size / 1e6))
    print("Last build: %s%s" % (built[:19] if built else "unknown", age))


def main():
    ap = argparse.ArgumentParser(description="PAROS search kit: ranked vault search (FTS5 index, read-only)")
    ap.add_argument("query", nargs="*")
    ap.add_argument("--area", default="", help="path fragment filter, for example Work or Areas/Home")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--status", action="store_true", help="show the index's age and size")
    ap.add_argument("--files", action="store_true", help="force the fallback: walk the files, no index")
    ap.add_argument("--db", type=Path, default=None)
    ap.add_argument("--vault", type=Path, default=None)
    a = ap.parse_args()
    db = (a.db or default_db()).expanduser()
    vault = (a.vault or default_vault()).expanduser()

    if a.status:
        status(db)
        return
    q = " ".join(a.query).strip()
    if not q:
        ap.error("give a query of 2 to 4 word stems")
    terms = terms_of(q)
    rows, source = None, "index"
    if not a.files and db.is_file():
        try:
            rows = search_index(db, terms, a.area, a.limit)
        except sqlite3.Error as e:
            source = "file walk (index error: %s)" % e
    else:
        source = "file walk (forced)" if a.files else "file walk (no index)"
    if rows is None:
        rows = search_files(vault, terms, a.area, a.limit)
    if a.json:
        print(json.dumps(dict(query=q, terms=terms, source=source, results=rows), ensure_ascii=False, indent=1))
        return
    print("Source: %s | terms: %s | %d results" % (source, ", ".join(terms), len(rows)))
    for i, r in enumerate(rows, 1):
        print("%2d. %s" % (i, r["path"]))
        if r["description"]:
            print("    %s" % r["description"][:220])
        if r["snippet"]:
            print("    ... %s" % r["snippet"][:220])


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
