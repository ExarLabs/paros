#!/usr/bin/env python3
"""Cross-skill learning digest (PAROS P05): which skills need attention, and why.

Deterministic, no model, free to run. Walks every live definition (CURRENT.md) under the
given folders, counts the learning packets waiting in each skill's observations/ folder, and
flags the skills that need a review. It never edits a definition and never bumps a version.

Usage:
    python digest.py <folder> [<folder> ...]          # print the digest
    python digest.py ~/vault/PAROS/skills --out ~/vault/PAROS/SKILL_DIGEST.md
    python digest.py ~/vault --json                   # machine-readable status
    PAROS_SKILLS=~/vault/PAROS/skills python digest.py

Folders: the arguments, else $PAROS_SKILLS (several joined by the OS path separator),
else $PAROS_VAULT, else the current directory.

A pending packet is a .md file with frontmatter, or a .json file, directly inside
observations/ (subfolders such as observations/processed/ are ignored), whose `status` is not
one of: applied, rejected, done, processed, archived. Fields used: date, severity
(high | medium | low), proposes (the proposed change, for convergence).

Triggers (any one flags the skill):
    high severity            the skill gives wrong results now
    convergence >= 2         the same proposed change from 2+ independent packets
    pending >= 5             enough signal for one review
    oldest > 30 days         nothing should rot in the inbox
    pending >= 16            close to the inbox cap of 20 (urgent)

Standard library only, Python 3.8+.
"""
import argparse
import datetime
import json
import os
import re
import sys

DONE = {"applied", "rejected", "done", "processed", "archived"}
SKIP_DIRS = {"versions", "observations", "references", "golden", "__pycache__", ".git", ".obsidian"}
TODAY = datetime.date.today()


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if kv:
            out[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return out


def parse_date(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def load_packet(path):
    try:
        text = read(path)
    except (OSError, UnicodeDecodeError):
        return None
    if path.endswith(".json"):
        try:
            data = json.loads(text)
        except ValueError:
            return None
        return data if isinstance(data, dict) else None
    fm = frontmatter(text)
    return fm or None


def scan_skill(cur, root, a):
    sdir = os.path.dirname(cur)
    try:
        text = read(cur)
    except (OSError, UnicodeDecodeError):
        text = ""
    fm = frontmatter(text)
    obs_dir = os.path.join(sdir, "observations")
    s = {"name": os.path.relpath(sdir, root).replace(os.sep, "/") if sdir != root else os.path.basename(sdir),
         "path": sdir, "version": fm.get("version", "?"),
         "enrolled": os.path.isdir(obs_dir),
         "constitution": bool(re.search(r"^##\s+Constitution\b", text, re.M)),
         "packets": [], "triggers": [], "pending": 0}
    if not s["enrolled"]:
        return s
    for f in sorted(os.listdir(obs_dir)):
        p = os.path.join(obs_dir, f)
        if not os.path.isfile(p) or not f.endswith((".md", ".json")) or f.upper().startswith("README"):
            continue
        o = load_packet(p)
        if o is None or str(o.get("status", "")).lower() in DONE:
            continue
        d = parse_date(o.get("date")) or datetime.date.fromtimestamp(os.path.getmtime(p))
        s["packets"].append({"file": f, "date": d.isoformat(), "age_days": (TODAY - d).days,
                             "severity": str(o.get("severity") or "low").lower(),
                             "proposes": str(o.get("proposes") or "").strip()})
    pk = s["packets"]
    s["pending"] = len(pk)
    if not pk:
        return s
    s["oldest_days"] = max(x["age_days"] for x in pk)
    s["high"] = sum(1 for x in pk if x["severity"] == "high")
    groups = {}
    for x in pk:
        if x["proposes"]:
            groups.setdefault(x["proposes"], []).append(x["file"])
    s["converged"] = {k: v for k, v in groups.items() if len(v) >= a.convergence}

    if s["high"]:
        s["triggers"].append(("high severity", "now", "%d high-severity packet(s)" % s["high"]))
    for k, v in s["converged"].items():
        s["triggers"].append(("convergence", "ready", "%s (%d independent packets)" % (k, len(v))))
    if s["pending"] >= a.cap_warn:
        s["triggers"].append(("near cap", "urgent", "%d of %d, new packets may be refused" % (s["pending"], a.cap)))
    elif s["pending"] >= a.batch:
        s["triggers"].append(("batch", "due", "%d pending packets" % s["pending"]))
    if s["oldest_days"] > a.stale_days:
        s["triggers"].append(("stale", "due", "oldest is %d days old" % s["oldest_days"]))
    return s


def scan(roots, a):
    skills, seen = [], set()
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        for d, dirs, files in os.walk(root):
            dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
            if "CURRENT.md" in files:
                cur = os.path.join(d, "CURRENT.md")
                if cur not in seen:
                    seen.add(cur)
                    skills.append(scan_skill(cur, root, a))
    return skills


def esc(x):
    return str(x).replace("|", "\\|")


def render(skills):
    enrolled = [s for s in skills if s["enrolled"]]
    flagged = [s for s in enrolled if s["triggers"]]
    urgent = [s for s in flagged if any(t[1] in ("now", "urgent") for t in s["triggers"])]
    pending = sum(s["pending"] for s in enrolled)
    L = ["---", "title: Skill learning digest", "date: %s" % TODAY.isoformat(), "status: active",
         'description: "Generated digest of pending learning packets per skill: what needs a review now, '
         'what is ready, and which skills do not learn yet. Regenerated; do not edit by hand."',
         "---", "", "# Skill learning digest", "",
         "Generated %s. Skills: **%d**, learning: **%d**. Pending packets: **%d**. Need attention: **%d**."
         % (TODAY.isoformat(), len(skills), len(enrolled), pending, len(flagged)), "",
         "> Regenerated. Decisions happen in the review of each skill, not in this file.", "",
         "## Needs attention", ""]
    if not flagged:
        L += ["Nothing. No trigger fired for any learning skill.", ""]
    else:
        if urgent:
            L += ["**Urgent:** %s." % ", ".join("`%s`" % s["name"] for s in urgent), ""]
        L += ["| Skill | Version | Pending | Oldest | Trigger | Why |", "|---|---|---:|---:|---|---|"]
        for s in flagged:
            for kind, urg, why in s["triggers"]:
                L.append("| `%s` | v%s | %d | %d d | %s (%s) | %s |"
                         % (s["name"], s["version"], s["pending"], s.get("oldest_days", 0), kind, urg, esc(why)))
        L.append("")
    L += ["## Pending packets", ""]
    any_pk = False
    for s in enrolled:
        if not s["pending"]:
            continue
        any_pk = True
        L += ["### %s (v%s)" % (s["name"], s["version"]), "",
              "| Date | Severity | Age | Proposed change | File |", "|---|---|---:|---|---|"]
        for x in s["packets"]:
            L.append("| %s | %s | %d d | %s | `%s` |" % (x["date"], x["severity"], x["age_days"],
                                                       esc(x["proposes"] or "(not stated)"), x["file"]))
        L.append("")
    if not any_pk:
        L += ["No pending packets.", ""]
    L += ["## Coverage", "",
          "A skill learns only if it has an `observations/` folder next to its `CURRENT.md`.", "",
          "| Skill | Version | Learning | Constitution | Pending |", "|---|---|---|---|---:|"]
    for s in skills:
        L.append("| `%s` | v%s | %s | %s | %d |" % (s["name"], s["version"], "yes" if s["enrolled"] else "no",
                                                   "yes" if s["constitution"] else "no", s["pending"]))
    L.append("")
    return "\n".join(L)


def status(skills):
    enrolled = [s for s in skills if s["enrolled"]]
    flagged = [s for s in enrolled if s["triggers"]]
    return {"generated": TODAY.isoformat(), "skills": len(skills), "learning": len(enrolled),
            "pending": sum(s["pending"] for s in enrolled), "needs_attention": len(flagged),
            "urgent": sum(1 for s in flagged if any(t[1] in ("now", "urgent") for t in s["triggers"])),
            "flagged": [{"skill": s["name"], "version": s["version"], "pending": s["pending"],
                         "oldest_days": s.get("oldest_days", 0), "high": s.get("high", 0),
                         "triggers": [{"kind": k, "urgency": u, "why": w} for k, u, w in s["triggers"]]}
                        for s in flagged]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Digest of pending learning packets across skills.")
    ap.add_argument("roots", nargs="*", help="folders to scan for CURRENT.md")
    ap.add_argument("--out", help="also write the markdown digest to this file")
    ap.add_argument("--json", action="store_true", help="print a JSON status instead of the digest")
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--convergence", type=int, default=2)
    ap.add_argument("--cap", type=int, default=20)
    ap.add_argument("--cap-warn", type=int, default=16)
    a = ap.parse_args(argv)

    roots = a.roots
    if not roots and os.environ.get("PAROS_SKILLS"):
        roots = [r for r in os.environ["PAROS_SKILLS"].split(os.pathsep) if r]
    if not roots:
        roots = [os.environ.get("PAROS_VAULT") or os.getcwd()]
    missing = [r for r in roots if not os.path.isdir(os.path.expanduser(r))]
    if missing:
        print("ERROR: not a folder: %s" % ", ".join(missing), file=sys.stderr)
        return 1

    skills = scan(roots, a)
    md = render(skills)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
    if a.json:
        print(json.dumps(status(skills), ensure_ascii=False, indent=2))
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
