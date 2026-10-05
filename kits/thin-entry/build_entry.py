#!/usr/bin/env python3
"""Build thin entries (Agent Skills SKILL.md) for live definitions in a PAROS vault (P04).

A thin entry is the small file a platform loads (Claude Code, Codex, any agent that reads
the Agent Skills format). It holds no knowledge of its own. At run time it tells the agent to:

  1. locate the live definition (CURRENT.md) in the person's vault,
  2. check that the file is intact (readable, has a version, long enough),
  3. print a version report before any work (one of four cases),
  4. follow the live definition, or, if the vault is unavailable and the entry was built
     with --fallback, follow the embedded snapshot,
  5. end with one line: "<name> v<X> (vault|fallback) ran".

The vault always wins, even when its version is older than the embedded snapshot.

Usage:
    python build_entry.py <CURRENT.md | folder> [options]

    # one skill, entry written to ./entries/<name>/SKILL.md
    python build_entry.py ~/vault/PAROS/skills/meeting-notes/CURRENT.md --vault-root ~/vault

    # every CURRENT.md under a folder, straight into the Claude Code skills folder
    python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ~/vault/.claude/skills

    # a packaged plugin that travels without the vault: embed a snapshot
    python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ./plugin/skills --fallback

    # detect hand edits in embedded snapshots, write nothing
    python build_entry.py ~/vault/PAROS/skills --vault-root ~/vault --out ./plugin/skills --check

Frontmatter fields read from CURRENT.md (all optional):
    entry_name         the skill name (default: the folder name)
    entry_description  the entry's description (default: `description`)
    version            the live definition's version (required for a useful entry)

Standard library only, Python 3.8+.
"""
import argparse
import hashlib
import json
import os
import re
import sys

CONTRACT = "1.0.0"          # version of the entry text this script writes
BEGIN = "<!-- FALLBACK:BEGIN"
END = "<!-- FALLBACK:END -->"
SKIP_DIRS = {"versions", "observations", "references", "golden", "__pycache__", ".git"}
VAULT_MARKERS = (".obsidian", "AGENTS.md", "CLAUDE.md")
CONFIG_FILE = "~/.paros/vault"


# ------------------------------------------------------------------ frontmatter

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def split_fm(text):
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end], text[end + 4:].lstrip("\n")


def parse_fm(fm):
    """Flat keys plus folded `>` / `|` blocks. Not full YAML, enough for this."""
    out, key, buf = {}, None, []
    for line in fm.split("\n"):
        if key and (line.startswith("  ") or line.startswith("\t")) and line.strip():
            buf.append(line.strip())
            continue
        if key:
            out[key] = " ".join(buf)
            key, buf = None, []
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v in (">", ">-", "|", "|-"):
            key, buf = k, []
        else:
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            out[k] = v
    if key:
        out[key] = " ".join(buf)
    return out


def sha8(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


# ------------------------------------------------------------------ discovery

def find_vault_root(path):
    """Nearest ancestor that looks like a vault (has .obsidian, AGENTS.md or CLAUDE.md)."""
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if any(os.path.exists(os.path.join(d, m)) for m in VAULT_MARKERS):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def discover(target):
    target = os.path.abspath(target)
    if os.path.isfile(target):
        return [target]
    found = []
    for root, dirs, files in os.walk(target):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        if "CURRENT.md" in files:
            found.append(os.path.join(root, "CURRENT.md"))
    return sorted(found)


def load(path, vault_root, name_override=None, desc_override=None):
    fm, body = split_fm(read(path))
    meta = parse_fm(fm)
    name = name_override or meta.get("entry_name") or os.path.basename(os.path.dirname(path))
    name = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    desc = desc_override or meta.get("entry_description") or meta.get("description") or ""
    desc = " ".join(desc.split())
    root = vault_root or find_vault_root(path)
    if root:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root)).replace(os.sep, "/")
        if rel.startswith(".."):
            rel = None
    else:
        rel = None
    if not rel:
        rel = "PAROS/skills/%s/CURRENT.md" % name
    return {"path": path, "name": name, "description": desc, "version": meta.get("version", ""),
            "body": body.strip(), "rel": rel}


# ------------------------------------------------------------------ rendering

def min_length(body):
    """Half of the current body, with a floor; never more than the body itself."""
    n = len(body)
    return max(min(200, n), n // 2)


def render(cap, fallback, default_vault=None):
    v, name, rel = cap["version"] or "0.0.0", cap["name"], cap["rel"]
    desc = cap["description"] or ("Run the %s skill from its live definition in the vault." % name)
    lines = ["---",
             "name: %s" % name,
             # Always quoted: a bare "foo: bar" inside the text breaks YAML and the platform
             # may then drop the whole frontmatter silently.
             "description: %s" % json.dumps(desc, ensure_ascii=False),
             "metadata:",
             "  entry_contract: %s" % CONTRACT,
             "  source_version: %s" % v,
             "  generated_by: build_entry.py",
             "---", "", ""]
    out = "\n".join(lines)

    where = ["   - the `PAROS_VAULT` environment variable;",
             "   - `CLAUDE_PROJECT_DIR` (the project folder Claude Code was started in);",
             "   - the current working directory;",
             "   - the folder named on the first line of `%s` (a one-line config file), if it exists;"
             % CONFIG_FILE]
    if default_vault:
        where.append("   - `%s` (configured when this entry was built);" % default_vault)
    where[-1] = where[-1][:-1] + "."

    if fallback:
        intro = ("This entry was built from **v%s** of the live definition. A snapshot of that "
                 "version is embedded below in the `FALLBACK` block. It applies **only** when the "
                 "vault is unavailable." % v)
        unavailable = ("`Version: the live definition is unavailable (<short reason>). Working from "
                       "the built-in v%s snapshot; a newer version may exist.`" % v)
        endline = "`%s v<X> (vault|fallback) ran`" % name
        ignore = " If the vault won, ignore the `FALLBACK` block entirely."
    else:
        intro = ("This entry was built from **v%s** of the live definition. No snapshot is "
                 "embedded: without the vault this skill does not run." % v)
        unavailable = ("`Version: the live definition is unavailable (<short reason>). This entry "
                       "has no built-in snapshot, so it stops here.` Then tell the person how to "
                       "point it at the vault (`PAROS_VAULT` or `%s`) and stop." % CONFIG_FILE)
        endline = "`%s v<X> (vault) ran`" % name
        ignore = ""

    out += """# %(name)s

Thin entry (PAROS P04), generated by `build_entry.py`. The knowledge lives in the live definition in the person's vault; this file only finds it. Do not edit this file by hand: change the live definition and rebuild.

## 0. Locate, check, report: do this first

%(intro)s

1. **Find the vault.** The first match wins; a candidate counts only if `<candidate>/%(rel)s` exists:
%(where)s
2. **Read** `<vault>/%(rel)s` in full.
3. **Integrity check.** The file is intact only if it is readable, its frontmatter has a `version:` field, and its body (after the frontmatter) is at least %(minlen)d characters. If any check fails, treat it as unavailable (a sync service can leave a half-downloaded or placeholder file).
4. **Read** the `version:` value from its frontmatter; it is called v<X> below.
5. **Before any work, print the version report.** It is mandatory and is never skipped or shortened. Exactly one case applies:
   - the vault is **newer**: `Version: the vault has v<X>, newer than the built-in v%(v)s. Working from the vault.`
   - the **same**: `Version: the vault has v%(v)s, the same as the built-in. Working from the vault.`
   - the vault is **older**: `Version: the vault has v<X>, older than the built-in v%(v)s. The vault is the source of truth, so working from the vault anyway. If this is unexpected, the vault copy may not be synced yet.`
   - the vault is **unavailable**: %(unavailable)s
6. **Then work** by the chosen definition. Its `## Constitution` always wins.%(ignore)s
7. **At the end**, repeat in one line: %(endline)s.
8. If the person corrects the result, write a learning packet into the `observations/` folder next to the live definition (P05).
""" % {"name": name, "intro": intro, "rel": rel, "where": "\n".join(where),
       "minlen": min_length(cap["body"]), "v": v, "unavailable": unavailable,
       "ignore": ignore, "endline": endline}

    if fallback:
        out += ("\n---\n\n## FALLBACK: generated snapshot, do not edit by hand\n\n"
                "> `build_entry.py` writes this block from the live definition. A hand edit here is "
                "lost at the next build; fix the source instead.\n\n"
                "%s source=%s version=%s sha=%s -->\n\n%s\n\n%s\n"
                % (BEGIN, rel, v, sha8(cap["body"]), cap["body"], END))
    return out


def existing_fallback(path):
    """(recorded sha, current block body) of an entry on disk, or (None, None)."""
    if not os.path.exists(path):
        return None, None
    t = read(path)
    i, j = t.find(BEGIN), t.find(END)
    if i == -1 or j == -1:
        return None, None
    head_end = t.find("-->", i)
    m = re.search(r"sha=([0-9a-f]+)", t[i:head_end])
    return (m.group(1) if m else None), t[head_end + 3:j].strip()


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser(description="Build thin SKILL.md entries for live definitions (PAROS P04).")
    ap.add_argument("target", help="a CURRENT.md file, or a folder searched for CURRENT.md files")
    ap.add_argument("--out", default="entries",
                    help="output folder; each entry goes to <out>/<name>/SKILL.md (default: ./entries)")
    ap.add_argument("--vault-root", default=os.environ.get("PAROS_VAULT"),
                    help="the vault folder, to compute the definition's path inside it "
                         "(default: $PAROS_VAULT, else the nearest ancestor with .obsidian, AGENTS.md or CLAUDE.md)")
    ap.add_argument("--fallback", action="store_true",
                    help="embed a sha-locked snapshot for use when the vault is unavailable")
    ap.add_argument("--default-vault", default=None,
                    help="an extra, last vault location written into the entry (avoid in shared or public builds)")
    ap.add_argument("--name", help="override the skill name (single file only)")
    ap.add_argument("--description", help="override the description (single file only)")
    ap.add_argument("--stdout", action="store_true", help="print the entry instead of writing it (single file only)")
    ap.add_argument("--check", action="store_true",
                    help="write nothing; report hand-edited FALLBACK blocks and stale entries")
    a = ap.parse_args(argv)

    paths = discover(a.target)
    if not paths:
        print("ERROR: no CURRENT.md found under %s" % a.target, file=sys.stderr)
        return 1
    single = len(paths) == 1 and os.path.isfile(a.target)
    if (a.name or a.description or a.stdout) and not single:
        print("ERROR: --name, --description and --stdout need a single CURRENT.md", file=sys.stderr)
        return 1

    problems = written = 0
    for p in paths:
        cap = load(p, a.vault_root, a.name, a.description)
        text = render(cap, a.fallback, a.default_vault)
        if a.stdout:
            sys.stdout.write(text)
            return 0
        if not cap["version"]:
            print("  WARNING: %s has no version: field; the entry will report v0.0.0" % p)
        dst = os.path.join(a.out, cap["name"], "SKILL.md")
        old_sha, old_body = existing_fallback(dst)
        if old_sha and old_body is not None and sha8(old_body) != old_sha:
            print("  HAND EDIT in the FALLBACK block of %s (sha mismatch); a rebuild discards it" % dst)
            problems += 1
        status = "new"
        if os.path.exists(dst):
            status = "same" if read(dst) == text else "changed"
        if a.check:
            if status != "same":
                problems += 1
            print("  %-28s v%-9s %s" % (cap["name"], cap["version"] or "?", "up to date" if status == "same" else "needs rebuild (%s)" % status))
            continue
        if status != "same":
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            written += 1
        print("  %-28s v%-9s %-8s -> %s" % (cap["name"], cap["version"] or "?", status, dst))

    if a.check:
        print("Check done. Problems: %d" % problems)
    else:
        print("%d entr%s written, %d unchanged%s." % (written, "y" if written == 1 else "ies",
                                                     len(paths) - written,
                                                     ", with fallback" if a.fallback else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
