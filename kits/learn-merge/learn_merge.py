#!/usr/bin/env python3
"""learn_merge.py: deterministic integration of learned rules (PAROS principle P05).

The reviewer (a caretaker agent) never rewrites or summarises a section. It only
proposes typed, rule-level changes, and this script applies them as code:

  add        append a new rule to the end of a section, with a new stable ID
  update     replace the text of a rule by ID (the old text is kept in LEARNINGS.md)
  deprecate  retire a rule: it moves to the "## Retired rules" section, struck through,
             with the date and the reason (it is never deleted)
  move       relocate a rule verbatim to references/rules.md and leave a pointer
             (size management without rewriting)
  list       list the rules with their IDs
  check      integrity: print the hash of the "## Constitution" section

Rule format in the target file (one line per rule):
    - <rule text> <!-- rule:R-007 since:2026-10-03 -->

Safeguards:
  * no operation may write into or out of the "## Constitution" section
    (checked by comparing the section hash before and after the change);
  * before every change, a snapshot of the previous version goes to versions/,
    and the patch version in the frontmatter is bumped;
  * every change appends one row to the "Integration log" table in LEARNINGS.md
    (old text and new text);
  * apart from the change itself, the file stays byte-for-byte unchanged.

Home folder: versions/, LEARNINGS.md and references/ live next to the target file.
If the target is an agent definition (agents/<name>.md), they go into the agent's own
folder (agents/<name>/) instead of the shared agents/ root. Override with --home.

add --section accepts "Section" (a ## heading, matched by prefix) or
"Section > Subsection" (a ### heading inside that ## section). The new rule is inserted
before trailing blank lines and a closing "---" separator of the section.

Usage:
  python learn_merge.py add CURRENT.md --section "Heuristics" --text "..." --packet <id> --reason "..."
  python learn_merge.py add agents/reviewer.md --section "Rules > Output" --text "..." --reason "..."
  python learn_merge.py update CURRENT.md --id R-007 --text "..." --packet <id> --reason "..."
  python learn_merge.py deprecate CURRENT.md --id R-007 --packet <id> --reason "..."
  python learn_merge.py move CURRENT.md --id R-007 --reason "..."
  python learn_merge.py list CURRENT.md
  python learn_merge.py check CURRENT.md

Standard library only, Python 3.8+.
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import re
import sys

TODAY = datetime.date.today().isoformat()
CONSTITUTION = "Constitution"
RETIRED_HEAD = "## Retired rules"
LOG_HEAD = "## Integration log (learn_merge.py)"
REF_NAME = "rules.md"
RULE_RE = re.compile(r"<!--\s*rule:(R-\d+)(?:\s+since:[0-9-]+)?\s*-->")
# Every ID ever issued (active, retired or moved), so that next_id() never reuses one.
ID_RE = re.compile(r"<!--\s*(?:rule|deprecated|moved):(R-\d+)")


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def section_range(lines, title):
    """(start, end) line indexes of the first ## section whose title starts with `title`."""
    heads = [(i, ln[3:].strip()) for i, ln in enumerate(lines) if ln.startswith("## ")]
    for k, (i, t) in enumerate(heads):
        if t.lower().startswith(title.lower()):
            end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
            return i, end
    return None


def target_range(lines, path):
    """Target section: "Title" (a ## section) or "Title > Subtitle" (a ### subsection inside
    the ## section, up to the next ### heading or the end of the ## section)."""
    parts = [x.strip() for x in path.split(">")]
    r = section_range(lines, parts[0])
    if not r or len(parts) == 1:
        return r
    if len(parts) > 2:
        return None
    for i in range(r[0] + 1, r[1]):
        if lines[i].startswith("### ") and lines[i][4:].strip().lower().startswith(parts[1].lower()):
            end = i + 1
            while end < r[1] and not lines[end].startswith("### "):
                end += 1
            return i, end
    return None


def home_dir(cur, override=None):
    """Where versions/, LEARNINGS.md and references/ live. By default the target's folder;
    for agents/<name>.md it is agents/<name>/."""
    if override:
        return override
    d = os.path.dirname(os.path.abspath(cur))
    if os.path.basename(d) == "agents" and os.path.basename(cur) != "CURRENT.md":
        return os.path.join(d, os.path.splitext(os.path.basename(cur))[0])
    return d


def constitution_hash(text):
    lines = text.split("\n")
    r = section_range(lines, CONSTITUTION)
    if not r:
        return None
    body = "\n".join(lines[r[0]:r[1]]).strip()
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def in_constitution(lines, idx):
    r = section_range(lines, CONSTITUTION)
    return bool(r and r[0] <= idx < r[1])


def next_id(text):
    ids = [int(m.group(1)[2:]) for m in ID_RE.finditer(text)]
    return "R-%03d" % ((max(ids) + 1) if ids else 1)


def find_rule(lines, rid):
    for i, ln in enumerate(lines):
        m = RULE_RE.search(ln)
        if m and m.group(1) == rid:
            return i
    return None


def bump(text):
    """Bump the patch part of `version: X.Y.Z` in the frontmatter. Returns (text, old, new)."""
    m = re.search(r"^version:\s*([0-9]+)\.([0-9]+)\.([0-9]+)\s*$", text, re.M)
    if not m:
        return text, None, None
    old = "%s.%s.%s" % m.groups()
    new = "%s.%s.%d" % (m.group(1), m.group(2), int(m.group(3)) + 1)
    return text[:m.start()] + "version: " + new + text[m.end():], old, new


def snapshot(home, text, ver):
    d = os.path.join(home, "versions")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "v%s.md" % ver)
    if not os.path.exists(p):
        write(p, text)
    elif read(p) != text:
        # v<ver>.md already exists, but the file changed since without a version bump
        # (a manual edit): keep the pre-change state in a separate snapshot and never
        # overwrite an existing one.
        base = os.path.join(d, "v%s+pre-%s" % (ver, datetime.datetime.now().strftime("%Y%m%d%H%M")))
        q, n = base + ".md", 2
        while os.path.exists(q) and read(q) != text:
            q, n = "%s-%d.md" % (base, n), n + 1
        if not os.path.exists(q):
            write(q, text)


def ledger(home, op, rid, old, new, packet, reason, ver):
    os.makedirs(home, exist_ok=True)
    p = os.path.join(home, "LEARNINGS.md")
    s = read(p) if os.path.exists(p) else "# Learnings\n"
    if LOG_HEAD not in s:
        s = (s.rstrip("\n") + "\n\n" + LOG_HEAD + "\n\n"
             "| Date | Operation | Rule | Old text | New text | Packet | Reason | Version |\n"
             "|---|---|---|---|---|---|---|---|\n")

    def esc(x):
        return (x or "").replace("|", "\\|").replace("\n", " ")

    row = "| %s | %s | %s | %s | %s | %s | %s | %s |" % (
        TODAY, op, rid, esc(old), esc(new), esc(packet), esc(reason), ver or "")
    # If other content follows the log table, insert the row right after the table's last
    # row (appending at the end of the file would drop it out of the table). If the table
    # ends the file, or cannot be located unambiguously, append at the end.
    lines = s.split("\n")
    hs = [i for i, ln in enumerate(lines) if ln.strip() == LOG_HEAD]
    h = hs[0] if len(hs) == 1 else None
    last = None
    if h is not None:
        for j in range(h + 1, len(lines)):
            if lines[j].startswith("# ") or lines[j].startswith("## "):
                break
            if lines[j].startswith("|"):
                last = j
    if last is not None and any(ln.strip() for ln in lines[last + 1:]):
        lines.insert(last + 1, row)
        s = "\n".join(lines)
    else:
        s = s.rstrip("\n") + "\n" + row + "\n"
    write(p, s)


def rule_line(text, rid, since=None):
    return "- %s <!-- rule:%s since:%s -->" % (text.strip(), rid, since or TODAY)


def rule_text(line):
    return RULE_RE.sub("", line).strip().lstrip("-").strip()


def fail(msg):
    sys.exit("learn_merge: " + msg)


def apply(args):
    cur = args.file
    home = home_dir(cur, getattr(args, "home", None))
    text = read(cur)
    before_const = constitution_hash(text)
    lines = text.split("\n")
    old_txt, new_txt, rid = "", "", getattr(args, "id", None)

    if args.op == "add":
        if any(x.strip().lower().startswith(CONSTITUTION.lower()) for x in args.section.split(">")):
            fail("learning may not write into the %s section." % CONSTITUTION)
        r = target_range(lines, args.section)
        if not r:
            fail("no such section: %s" % args.section)
        rid = next_id(text)
        new_txt = args.text
        ins = r[1]
        # before trailing blank lines and a closing "---" separator of the section
        while ins > r[0] + 1 and lines[ins - 1].strip() in ("", "---"):
            ins -= 1
        lines.insert(ins, rule_line(args.text, rid))
    else:
        i = find_rule(lines, rid)
        if i is None:
            fail("no such rule ID: %s" % rid)
        if in_constitution(lines, i):
            fail("learning may not touch a %s rule." % CONSTITUTION)
        old_txt = rule_text(lines[i])
        if args.op == "update":
            new_txt = args.text
            m = re.search(r"since:([0-9-]+)", lines[i])
            lines[i] = rule_line(args.text, rid, m.group(1) if m else None)
        elif args.op == "deprecate":
            gone = lines.pop(i)
            if RETIRED_HEAD not in "\n".join(lines):
                while lines and lines[-1].strip() == "":
                    lines.pop()
                lines += ["", RETIRED_HEAD, "",
                          "<!-- Retired but preserved rules. They no longer apply; they stay for their history. -->",
                          ""]
            lines.append("- ~~%s~~ (retired %s: %s) <!-- deprecated:%s -->"
                         % (rule_text(gone), TODAY, args.reason, rid))
            new_txt = "retired"
        elif args.op == "move":
            gone = lines[i]
            ref = os.path.join(home, "references", REF_NAME)
            os.makedirs(os.path.dirname(ref), exist_ok=True)
            rs = read(ref) if os.path.exists(ref) else (
                "---\ntitle: rules\ndate: %s\nstatus: active\n"
                "description: \"Detailed rules moved verbatim out of the main definition by "
                "learn_merge.py move. They still apply; the main file points to them.\"\n"
                "---\n\n# Detailed rules\n\n" % TODAY)
            write(ref, rs.rstrip("\n") + "\n" + gone + "\n")
            lines[i] = "- (%s in detail: `references/%s`) <!-- moved:%s -->" % (rid, REF_NAME, rid)
            new_txt = "moved to references/%s" % REF_NAME

    out = "\n".join(lines)
    if text.endswith("\n") and not out.endswith("\n"):
        out += "\n"  # keep the final newline (deprecate appends after trimming blank lines)
    if constitution_hash(out) != before_const:
        fail("the %s section would have changed: aborted." % CONSTITUTION)
    out, old_ver, new_ver = bump(out)
    snapshot(home, text, old_ver or "before-%s" % TODAY)
    write(cur, out)
    ledger(home, args.op, rid, old_txt, new_txt, getattr(args, "packet", ""), args.reason, new_ver)
    print(json.dumps(dict(ok=True, op=args.op, rule=rid, version=new_ver), ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description="Deterministic integration of learned rules (PAROS P05)")
    sp = ap.add_subparsers(dest="op")
    sp.required = True
    for op in ("add", "update", "deprecate", "move"):
        p = sp.add_parser(op)
        p.add_argument("file")
        if op == "add":
            p.add_argument("--section", required=True)
        else:
            p.add_argument("--id", required=True)
        if op in ("add", "update"):
            p.add_argument("--text", required=True)
        if op != "move":
            p.add_argument("--packet", default="")
        p.add_argument("--reason", required=True)
        p.add_argument("--home", default=None,
                       help="folder for versions/, LEARNINGS.md and references/ "
                            "(default: the target's folder; agents/<name>/ for agents/<name>.md)")
    for op in ("list", "check"):
        p = sp.add_parser(op)
        p.add_argument("file")
    a = ap.parse_args()
    if a.op == "list":
        for ln in read(a.file).split("\n"):
            m = RULE_RE.search(ln)
            if m:
                print(m.group(1), rule_text(ln)[:150])
        return
    if a.op == "check":
        print(json.dumps(dict(constitution_hash=constitution_hash(read(a.file))), ensure_ascii=False))
        return
    apply(a)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
