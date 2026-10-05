#!/usr/bin/env python3
"""Promote a live definition (CURRENT.md) to a new version (PAROS P04, P09).

What it does, in order:
  1. reads the current `version: X.Y.Z` from the frontmatter,
  2. refuses if the `## Constitution` section differs from the latest snapshot in
     versions/, unless --allow-constitution is given (the owner's decision only),
  3. snapshots the file as it is now into versions/v<old>.md (never overwrites an existing
     snapshot; if one exists with different content, writes v<old>+pre-<timestamp>.md),
  4. bumps the version (patch, minor, major, or an explicit X.Y.Z) and the `date:` field,
  5. appends one row to the "Version log (promote.py)" table in LEARNINGS.md.

Usage:
    python promote.py <CURRENT.md | skill folder> patch|minor|major|X.Y.Z --note "<what changed>"
    python promote.py skills/meeting-notes patch --note "action items now carry a due date"
    python promote.py skills/meeting-notes minor --note "..." --dry-run
    python promote.py skills/meeting-notes patch --note "..." --allow-constitution   # owner only
    python promote.py --list <folder>          # skills under a folder and their versions

An agent never passes --allow-constitution on its own: the Constitution is the owner's.
Standard library only, Python 3.8+. Output: one JSON line on success.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

CONSTITUTION = "Constitution"
LOG_HEAD = "## Version log (promote.py)"
VER_RE = re.compile(r"^version:\s*[\"']?([0-9]+)\.([0-9]+)\.([0-9]+)[\"']?\s*$", re.M)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def version_of(text):
    m = VER_RE.search(text)
    return tuple(int(x) for x in m.groups()) if m else None


def vstr(t):
    return "%d.%d.%d" % t


def constitution(text):
    """Body of the first `## Constitution...` section, or None."""
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if start is None and re.match(r"^##\s+%s\b" % CONSTITUTION, ln):
            start = i + 1
        elif start is not None and re.match(r"^#{1,2}\s", ln):
            return "\n".join(lines[start:i]).strip()
    return "\n".join(lines[start:]).strip() if start is not None else None


def h16(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()[:16] if s is not None else "none"


def snap_key(fname):
    m = re.match(r"^v([0-9]+)\.([0-9]+)\.([0-9]+)(.*)\.md$", fname)
    return (tuple(int(x) for x in m.groups()[:3]), m.group(4)) if m else None


def latest_snapshot(vdir):
    if not os.path.isdir(vdir):
        return None
    keyed = [(snap_key(f), f) for f in os.listdir(vdir)]
    keyed = [(k, f) for k, f in keyed if k]
    if not keyed:
        return None
    # highest version; among equal versions the "+pre-<ts>" ones sort after the plain one
    keyed.sort(key=lambda kf: (kf[0][0], kf[0][1]))
    return os.path.join(vdir, keyed[-1][1])


def resolve(target):
    t = os.path.abspath(target)
    return os.path.join(t, "CURRENT.md") if os.path.isdir(t) else t


def bump(old, how):
    if how == "patch":
        return (old[0], old[1], old[2] + 1)
    if how == "minor":
        return (old[0], old[1] + 1, 0)
    if how == "major":
        return (old[0] + 1, 0, 0)
    m = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)$", how)
    if not m:
        raise ValueError("version must be patch, minor, major or X.Y.Z, got %r" % how)
    return tuple(int(x) for x in m.groups())


def ledger(home, today, old, new, note, const_changed):
    p = os.path.join(home, "LEARNINGS.md")
    s = read(p) if os.path.exists(p) else "# Learnings\n"
    if LOG_HEAD not in s:
        s = (s.rstrip("\n") + "\n\n" + LOG_HEAD + "\n\n"
             "| Date | From | To | Note | Constitution changed |\n|---|---|---|---|---|\n")
    row = "| %s | %s | %s | %s | %s |" % (today, old, new, note.replace("|", "\\|").replace("\n", " "),
                                          "yes" if const_changed else "no")
    lines = s.rstrip("\n").split("\n")
    h = [i for i, ln in enumerate(lines) if ln.strip() == LOG_HEAD]
    last = None
    if len(h) == 1:
        for j in range(h[0] + 1, len(lines)):
            if lines[j].startswith("# ") or lines[j].startswith("## "):
                break
            if lines[j].startswith("|"):
                last = j
    if last is not None:
        lines.insert(last + 1, row)
    else:
        lines.append(row)
    write(p, "\n".join(lines) + "\n")
    return p


def list_skills(folder):
    for root, dirs, files in os.walk(os.path.abspath(folder)):
        dirs[:] = sorted(d for d in dirs if d not in ("versions", "observations", "references", "golden")
                         and not d.startswith("."))
        if "CURRENT.md" in files:
            v = version_of(read(os.path.join(root, "CURRENT.md")))
            vd = os.path.join(root, "versions")
            n = len([f for f in os.listdir(vd) if snap_key(f)]) if os.path.isdir(vd) else 0
            print("  %-40s v%-9s %d snapshot(s)" % (os.path.relpath(root, folder), vstr(v) if v else "?", n))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bump a live definition's version with a snapshot and a log row.")
    ap.add_argument("target", nargs="?", help="CURRENT.md or the skill folder that holds it")
    ap.add_argument("level", nargs="?", help="patch | minor | major | X.Y.Z")
    ap.add_argument("--note", help="what changed and why (goes into LEARNINGS.md)")
    ap.add_argument("--allow-constitution", action="store_true",
                    help="the owner accepts a changed Constitution section (owner only)")
    ap.add_argument("--dry-run", action="store_true", help="report what would happen, write nothing")
    ap.add_argument("--list", metavar="FOLDER", help="list skills under FOLDER with their versions")
    a = ap.parse_args(argv)

    if a.list:
        return list_skills(a.list)
    if not (a.target and a.level and a.note):
        ap.error("target, level and --note are required")

    cur = resolve(a.target)
    if not os.path.isfile(cur):
        print(json.dumps({"ok": False, "error": "not found: %s" % cur}))
        return 1
    home = os.path.dirname(cur)
    text = read(cur)
    old = version_of(text)
    if not old:
        print(json.dumps({"ok": False, "error": "no `version: X.Y.Z` in the frontmatter"}))
        return 1
    try:
        new = bump(old, a.level)
    except ValueError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1
    if new <= old:
        print(json.dumps({"ok": False, "error": "new version %s is not above %s" % (vstr(new), vstr(old))}))
        return 1

    vdir = os.path.join(home, "versions")
    prev = latest_snapshot(vdir)
    const_now = constitution(text)
    const_changed = False
    if prev:
        const_changed = h16(constitution(read(prev))) != h16(const_now)
    if const_changed and not a.allow_constitution:
        print(json.dumps({"ok": False, "error": "the Constitution section differs from %s; only the owner "
                          "may accept that, with --allow-constitution" % os.path.basename(prev)}))
        return 2

    today = datetime.date.today().isoformat()
    snap = os.path.join(vdir, "v%s.md" % vstr(old))
    if os.path.exists(snap) and read(snap) != text:
        base = os.path.join(vdir, "v%s+pre-%s" % (vstr(old), datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        snap, n = base + ".md", 2
        while os.path.exists(snap):
            snap, n = "%s-%d.md" % (base, n), n + 1
    snap_needed = not (os.path.exists(snap) and read(snap) == text)

    m = VER_RE.search(text)
    newtext = text[:m.start()] + "version: " + vstr(new) + text[m.end():]
    fm_end = newtext.find("\n---", 3) if newtext.startswith("---") else -1
    if fm_end != -1:
        fm = newtext[:fm_end]
        fm2 = re.sub(r"^date:.*$", "date: %s" % today, fm, count=1, flags=re.M)
        newtext = fm2 + newtext[fm_end:]

    result = {"ok": True, "from": vstr(old), "to": vstr(new),
              "snapshot": os.path.relpath(snap, home).replace(os.sep, "/"),
              "constitution_changed": const_changed,
              "constitution_hash": h16(const_now), "dry_run": a.dry_run}
    if a.dry_run:
        print(json.dumps(result))
        return 0

    if snap_needed:
        os.makedirs(vdir, exist_ok=True)
        write(snap, text)
    write(cur, newtext)
    ledger(home, today, vstr(old), vstr(new), a.note, const_changed)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
