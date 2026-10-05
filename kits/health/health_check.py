#!/usr/bin/env python3
"""PAROS health kit (P11): no "it works" without proof, kit version 0.1.0.

Every check looks at real OUTPUT, never at whether a process is running or what the
documentation claims. Alerts go out only on a STATE CHANGE (green to red, and back),
as one line in the owner's task file, so the owner gets no noise.

    python health_check.py              # run the checks, update state, alert on change
    python health_check.py --dry-run    # print only, write nothing (no canary, no state, no alert)
    python health_check.py --json       # machine output

Checks (weight: 3 = alert now, 2 = alert once, 1 = log only):
  canary             3  end to end: the marker the previous run wrote into a note is found
                        by the search index (write, index, search all work); then a new marker
  index_fresh        2  the search index was rebuilt within --index-max-age hours
  secrets            3  no plain secret pattern in the vault (API keys, tokens, private keys);
                        a full scan once a day, in between only changed files plus earlier hits
  metadata           1  markdown files changed in the last 24 hours start with frontmatter
  cognition          1  the cognition kit's cycle ran in the last 48 hours (if configured)
  secrets_inventory  2  the secrets kit reports no unknown or overdue secret (if configured)
  backup             2  the last line of a backup log is younger than --backup-max-age (if configured)

A check returns (ok, detail): ok is True, False, or None (not applicable here). Names of
files are reported, never their content; a secret value is never printed.

Configuration (arguments win over environment):
  PAROS_VAULT               the vault root (default: the current directory)
  PAROS_INDEX               the search kit's database (default ~/.paros/index.db)
  PAROS_HEALTH_DIR          the folder in the vault for canary notes (default PAROS/health)
  PAROS_HEALTH_STATE_DIR    where per-host state and the log live (default ~/.paros/health)
  PAROS_TASKS               the owner's task file, relative to the vault (default TODO.md)
  PAROS_TASKS_SECTION       the heading alerts go under (default "## Now"; appended at the end if missing)
  PAROS_COGNITION_DIR       the cognition kit's data folder (optional)
  PAROS_SECRETS_INVENTORY   the secrets kit's SECRETS.json (optional; enables secrets_inventory)
  PAROS_SECRETS_SCRIPT      path to secrets_inventory.py (default: ../secrets/ next to this kit)
  PAROS_BACKUP_LOG          a backup log file whose modification time is the last backup (optional)
  PAROS_HOST                this machine's name (default: the host name)
"""
import argparse
import datetime as dt
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import time
import uuid
from pathlib import Path

KIT_VERSION = "0.1.0"
SKIP_DIRS = {".git", ".obsidian", ".trash", ".venv", "venv", "node_modules", "__pycache__"}
SECRET_PATTERNS = [
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI key", r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}"),
    ("Groq key", r"\bgsk_[A-Za-z0-9]{30,}"),
    ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    ("AWS access key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Slack token", r"\bxox[abpr]-[A-Za-z0-9\-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("Private key", r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]
SECRET_EXT = {".md", ".txt", ".json", ".py", ".sh", ".ps1", ".js", ".ts", ".yaml", ".yml", ".env",
              ".cfg", ".ini", ".toml", ".csv"}
ALERT_PREFIX = "PAROS health:"


class Ctx:
    """Everything a check needs: paths, settings, the persistent state, dry-run."""

    def __init__(self, a):
        env = os.environ.get
        self.vault = Path(a.vault or env("PAROS_VAULT") or os.getcwd()).expanduser().resolve()
        self.db = Path(a.db or env("PAROS_INDEX") or Path.home() / ".paros" / "index.db").expanduser()
        self.host = (a.host or env("PAROS_HOST") or socket.gethostname()).lower().split(".")[0]
        self.health_rel = (a.health_dir or env("PAROS_HEALTH_DIR") or "PAROS/health").strip("/\\")
        self.health_dir = self.vault / self.health_rel
        self.state_dir = Path(a.state_dir or env("PAROS_HEALTH_STATE_DIR") or Path.home() / ".paros" / "health").expanduser()
        self.state_file = self.state_dir / ("state.%s.json" % self.host)
        self.log_file = self.state_dir / "health.log"
        self.tasks = self.vault / (a.tasks or env("PAROS_TASKS") or "TODO.md")
        self.section = a.section or env("PAROS_TASKS_SECTION") or "## Now"
        self.cognition = env("PAROS_COGNITION_DIR")
        self.secrets_inv = env("PAROS_SECRETS_INVENTORY")
        self.secrets_script = Path(env("PAROS_SECRETS_SCRIPT") or Path(__file__).resolve().parent.parent / "secrets" / "secrets_inventory.py")
        self.backup_log = a.backup_log or env("PAROS_BACKUP_LOG")
        self.index_max_age = a.index_max_age
        self.backup_max_age = a.backup_max_age
        self.dry = a.dry_run
        self.now = dt.datetime.now()
        self.state = {}
        if self.state_file.exists():
            try:
                self.state = json.loads(self.state_file.read_text(encoding="utf-8"))
            except ValueError:
                self.state = {}

    def rel(self, p):
        return Path(p).relative_to(self.vault).as_posix()

    def walk(self, exts):
        for root, dirs, files in os.walk(self.vault):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if os.path.splitext(f)[1].lower() in exts:
                    yield Path(root) / f


# --- checks: each returns (ok: True | False | None, detail: str) -------------------------

def index_built_at(c):
    """The search kit's last build time (epoch seconds), or None."""
    if not c.db.is_file():
        return None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % c.db.resolve().as_posix(), uri=True)
        row = con.execute("SELECT value FROM meta WHERE key = 'built_at'").fetchone()
        con.close()
        if row:
            return dt.datetime.fromisoformat(row[0]).timestamp()
    except sqlite3.Error:
        pass
    return c.db.stat().st_mtime


def check_canary(c):
    """Two-phase: this run looks for the previous run's marker, then writes a new one.
    The indexer runs on its own schedule in between, so the whole chain is tested.
    If no index build has happened since the marker was written, there is nothing to
    judge yet: the marker stays, and index_fresh is the check that catches a dead indexer."""
    prev = c.state.get("canary_token")
    ok, detail = None, "first run: marker written, the next run looks for it"
    if prev:
        built = index_built_at(c)
        if built is None:
            return False, "no search index at the configured path, so the marker cannot be found"
        if built < c.state.get("canary_written_at", 0):
            return None, "no index build since the marker was written; judged after the next build"
        con = sqlite3.connect("file:%s?mode=ro" % c.db.resolve().as_posix(), uri=True)
        hit = con.execute("SELECT count(*) FROM notes_fts WHERE notes_fts MATCH ?", ('"%s"' % prev,)).fetchone()[0]
        con.close()
        ok = hit > 0
        detail = ("the previous marker is found by search" if ok else
                  "the previous marker (%s) is not found by search after an index build: "
                  "writing, indexing or search is broken" % prev)
    if not c.dry:
        tok = "parosCanary" + uuid.uuid4().hex[:12]
        c.health_dir.mkdir(parents=True, exist_ok=True)
        note = c.health_dir / ("canary-%s.md" % c.host)
        note.write_text(
            "---\ntitle: canary-%s\ndate: %s\nstatus: active\n"
            "description: \"Health check marker for machine %s; the next health run looks for it in the search index. Machine-written, do not edit.\"\n"
            "---\n\n%s\n" % (c.host, c.now.date().isoformat(), c.host, tok), encoding="utf-8", newline="\n")
        c.state["canary_token"] = tok
        c.state["canary_written_at"] = time.time()
    return ok, detail


def check_index_fresh(c):
    t = index_built_at(c)
    if t is None:
        return False, "no search index at %s" % c.db.name
    age = (time.time() - t) / 3600
    return age < c.index_max_age, "last index build %.1f hours ago (limit %g)" % (age, c.index_max_age)


def check_secrets(c):
    """Full scan once a day; in between only files changed since the last scan, plus the
    files that had a hit last time (so a hit cannot turn green just by not changing)."""
    pats = [(n, re.compile(p)) for n, p in SECRET_PATTERNS]
    full = time.time() - c.state.get("secrets_full_at", 0) > 24 * 3600
    since = 0 if full else c.state.get("secrets_scan_at", 0)
    recheck = set(c.state.get("secrets_hits", []))
    hits = {}
    for p in c.walk(SECRET_EXT):
        rel = c.rel(p)
        if rel.startswith(c.health_rel + "/"):
            continue
        try:
            st = p.stat()
            if since and st.st_mtime < since and rel not in recheck:
                continue
            if st.st_size > 2_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, rx in pats:
            if rx.search(text):
                hits[rel] = name
                break
    if not c.dry:
        c.state["secrets_scan_at"] = time.time()
        c.state["secrets_hits"] = sorted(hits)
        if full:
            c.state["secrets_full_at"] = time.time()
    mode = "full scan" if full else "changed files and earlier hits"
    if not hits:
        return True, "no plain secret (%s)" % mode
    return False, "plain secret pattern in %d file(s): %s" % (
        len(hits), "; ".join("%s (%s)" % (r, n) for r, n in sorted(hits.items())[:8]))


def check_metadata(c):
    cutoff = time.time() - 24 * 3600
    bad = []
    for p in c.walk({".md"}):
        rel = c.rel(p)
        if rel == c.rel(c.tasks):
            continue
        try:
            if p.stat().st_mtime < cutoff:
                continue
            with open(p, encoding="utf-8", errors="ignore") as f:
                if not f.read(3).startswith("---"):
                    bad.append(rel)
        except OSError:
            continue
    if not bad:
        return True, "every file changed in 24 hours has frontmatter"
    return False, "%d recent file(s) without frontmatter: %s" % (len(bad), "; ".join(bad[:5]))


def check_cognition(c):
    if not c.cognition:
        return None, "not configured (PAROS_COGNITION_DIR)"
    st = Path(c.cognition).expanduser() / "state.json"
    if not st.exists():
        return None, "no cycle has run yet"
    try:
        d = json.loads(st.read_text(encoding="utf-8"))
        last = dt.datetime.fromisoformat(d["last_cycle_at"].replace("Z", "+00:00"))
        if not last.tzinfo:
            last = last.replace(tzinfo=dt.timezone.utc)
        hours = (dt.datetime.now(dt.timezone.utc) - last).total_seconds() / 3600
    except Exception as e:
        return False, "unreadable cognition state: %s" % e
    return hours < 48, "last cycle %.0f hours ago (#%d)" % (hours, d.get("cycles", 0))


def check_secrets_inventory(c):
    if not c.secrets_inv:
        return None, "not configured (PAROS_SECRETS_INVENTORY)"
    if not c.secrets_script.exists():
        return False, "secrets_inventory.py not found at the configured path"
    r = subprocess.run([sys.executable, str(c.secrets_script), "check"], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore")
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return False, "the inventory check did not run: %s" % r.stderr.strip()[:120]
    return bool(d["ok"]), d["detail"]


def check_backup(c):
    if not c.backup_log:
        return None, "not configured (PAROS_BACKUP_LOG)"
    p = Path(c.backup_log).expanduser()
    if not p.exists():
        return False, "the backup log does not exist: no backup has ever been recorded"
    hours = (time.time() - p.stat().st_mtime) / 3600
    return hours < c.backup_max_age, "last backup record %.0f hours ago (limit %g)" % (hours, c.backup_max_age)


CHECKS = [
    ("canary", 3, check_canary),
    ("index_fresh", 2, check_index_fresh),
    ("secrets", 3, check_secrets),
    ("metadata", 1, check_metadata),
    ("cognition", 1, check_cognition),
    ("secrets_inventory", 2, check_secrets_inventory),
    ("backup", 2, check_backup),
]


# --- alerting: one line on change, marked on recovery ------------------------------------

def marker(c, name):
    return "<!-- paros-health:%s:%s -->" % (c.host, name)


def alert(c, name, detail, recovered=False):
    """Append one task line when a check turns red; mark that same line when it recovers.
    Never deletes a line. Returns what it did, for the report."""
    tag = marker(c, name)
    text = c.tasks.read_text(encoding="utf-8") if c.tasks.exists() else ""
    open_rx = re.compile(r"^- \[ \] %s.*%s[ \t]*$" % (re.escape(ALERT_PREFIX), re.escape(tag)), re.M)
    stamp = c.now.strftime("%Y-%m-%d %H:%M")
    if recovered:
        m = open_rx.search(text)
        if not m:
            return "recovered (no open line to mark)"
        line = m.group(0)
        done = line.replace("- [ ]", "- [x]", 1).replace(tag, "(recovered %s) %s" % (stamp, tag))
        new = text[:m.start()] + done + text[m.end():]
        what = "marked recovered"
    else:
        if open_rx.search(text):
            return "already open"
        line = "- [ ] %s **%s** on %s since %s: %s %s" % (ALERT_PREFIX, name, c.host, stamp, detail[:300], tag)
        if c.section and re.search(r"^%s[ \t]*$" % re.escape(c.section), text, re.M):
            new = re.sub(r"^(%s[ \t]*\n)" % re.escape(c.section), lambda m: m.group(1) + line + "\n", text, count=1, flags=re.M)
        else:
            new = text.rstrip("\n") + ("\n\n" if text.strip() else "") + line + "\n"
        what = "alert line added"
    if not c.dry:
        c.tasks.write_text(new, encoding="utf-8", newline="\n")
    return what


def log(c, status, res):
    failing = [n for n, r in res.items() if r["ok"] is False]
    extra = "" if not failing else " | " + "; ".join("%s: %s" % (n, res[n]["detail"][:120]) for n in failing)
    line = "%s %s %s %d/%d%s\n" % (c.now.strftime("%Y-%m-%dT%H:%M"), c.host, status,
                                    sum(1 for r in res.values() if r["ok"]),
                                    sum(1 for r in res.values() if r["ok"] is not None), extra)
    with open(c.log_file, "a", encoding="utf-8", newline="\n") as f:
        f.write(line)


def main():
    ap = argparse.ArgumentParser(description="PAROS health kit: weighted checks on real output, alerts on change")
    ap.add_argument("--vault")
    ap.add_argument("--db", help="the search kit's index database")
    ap.add_argument("--health-dir", help="folder inside the vault for canary notes")
    ap.add_argument("--state-dir", help="where per-host state and the log live")
    ap.add_argument("--tasks", help="the owner's task file, relative to the vault")
    ap.add_argument("--section", help="the heading alert lines go under")
    ap.add_argument("--backup-log")
    ap.add_argument("--host")
    ap.add_argument("--index-max-age", type=float, default=float(os.environ.get("PAROS_INDEX_MAX_AGE_H", 6)))
    ap.add_argument("--backup-max-age", type=float, default=float(os.environ.get("PAROS_BACKUP_MAX_AGE_H", 48)))
    ap.add_argument("--only", help="comma-separated check names to run")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    c = Ctx(a)
    if not c.vault.is_dir():
        sys.exit("vault not found: %s" % c.vault)
    only = {s.strip() for s in a.only.split(",")} if a.only else None

    prev = c.state.get("checks", {})
    res = {}
    for name, weight, fn in CHECKS:
        if only and name not in only:
            continue
        try:
            ok, detail = fn(c)
        except Exception as e:
            ok, detail = False, "the check itself failed: %s" % e
        res[name] = {"ok": ok, "weight": weight, "detail": detail}

    failing = [n for n, r in res.items() if r["ok"] is False]
    status = "RED" if any(res[n]["weight"] >= 2 for n in failing) else ("YELLOW" if failing else "GREEN")
    actions = {}
    for n, r in res.items():
        was = prev.get(n, {}).get("ok")
        if r["weight"] >= 2 and r["ok"] is False and was is not False:
            actions[n] = alert(c, n, r["detail"])
        elif r["weight"] >= 2 and r["ok"] is True and was is False:
            actions[n] = alert(c, n, r["detail"], recovered=True)

    if not c.dry:
        c.state_dir.mkdir(parents=True, exist_ok=True)
        merged = dict(prev)
        merged.update(res)
        c.state.update({"checks": merged, "last_run": c.now.isoformat(timespec="seconds"),
                        "status": status, "kit_version": KIT_VERSION})
        c.state_file.write_text(json.dumps(c.state, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        log(c, status, res)

    out = {"host": c.host, "at": c.now.isoformat(timespec="seconds"), "status": status,
           "dry_run": c.dry, "checks": res, "alerts": actions}
    if a.json:
        print(json.dumps(out, ensure_ascii=False))
        return
    print("PAROS health (%s): %s%s" % (c.host, status, "  [dry run, nothing written]" if c.dry else ""))
    for n, r in res.items():
        mark = {True: "ok  ", False: "FAIL", None: "--  "}[r["ok"]]
        print("  %s %-17s w%d  %s" % (mark, n, r["weight"], r["detail"]))
    for n, what in actions.items():
        print("  alert %s: %s%s" % (n, what, " (dry run)" if c.dry else ""))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
