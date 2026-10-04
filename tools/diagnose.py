#!/usr/bin/env python3
"""PAROS vault diagnosis scanner (read-only, no dependencies, Python 3.8+).

Measures a vault against the PAROS principles: what can be measured without
judgment. The agent adds the judgment (flows/2-diagnose.md). Nothing in the vault
is changed. Secret-like patterns are reported by file and type only, never by value.

    python diagnose.py <vault>                    # text map
    python diagnose.py <vault> --json out.json    # also write the full result as JSON
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKIP_DIRS = {".git", ".obsidian", ".trash", "node_modules", ".smart-env", "venv", ".venv",
             "__pycache__", ".cache", "dist", "build"}
TEXT_EXT = {".md", ".json", ".txt", ".yaml", ".yml", ".env", ".py", ".js", ".mjs", ".ts", ".sh", ".toml", ".ini", ".cfg"}
SECRET_PATTERNS = [
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI key", r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}"),
    ("Groq key", r"\bgsk_[A-Za-z0-9]{30,}"),
    ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    ("GitHub fine-grained token", r"\bgithub_pat_[A-Za-z0-9_]{40,}"),
    ("AWS key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Slack token", r"\bxox[abpr]-[A-Za-z0-9\-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("Private key", r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    ("Token in URL", r"https://[^/\s:@]+:[^/\s@]{16,}@"),
]
BOUNDARY_WORDS = [
    r"\bsend", r"\bpublish", r"\bdelet", r"\bmoney|\bpayment", r"\bcredential|\bpassword", r"\bexternal",
    r"küld", r"publik", r"törl", r"pénz", r"hitelesítő|jelszó", r"külső",
    r"envoy|envoi", r"publi", r"supprim", r"argent", r"senden|versend", r"veröffentl", r"lösch", r"geld",
]
LEVEL_BLOCKS = {0: "░░░", 1: "█░░", 2: "██░", 3: "███"}


DIR_COUNTS = {"observations": 0}


def is_link(path):
    """Symlinks and Windows junctions are aliases: following them double-counts the vault."""
    try:
        return os.path.islink(path) or (hasattr(os.path, "isjunction") and os.path.isjunction(path))
    except Exception:
        return False


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not is_link(os.path.join(dirpath, d))]
        DIR_COUNTS["observations"] += sum(1 for d in dirnames if d == "observations")
        for f in filenames:
            yield Path(dirpath) / f


def read(p, limit=1_000_000):
    try:
        if p.stat().st_size > limit:
            return None
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        k = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if k:
            fm[k.group(1).lower()] = k.group(2).strip().strip('"').strip("'")
    return fm


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def scan(root):
    root = Path(root).resolve()
    r = {"vault": str(root), "files": 0, "md": 0, "bytes": 0, "md_bytes": 0,
         "frontmatter": 0, "description": 0, "good_description": 0,
         "archive_dirs": [], "archive_files": 0, "learnings": 0, "observations_dirs": 0,
         "current_md": 0, "skills": [], "agents": [], "secret_hits": [], "secrets_inventory": False,
         "health_files": [], "source_map": [], "double_frontmatter": [], "search_index_hint": [],
         "memory_index": [], "cognition_registry": False}
    for p in walk(root):
        rel = p.relative_to(root).as_posix()
        r["files"] += 1
        try:
            size = p.stat().st_size
        except Exception:
            continue
        r["bytes"] += size
        parts_lower = [x.lower() for x in p.relative_to(root).parts]
        in_archive = any("archiv" in x for x in parts_lower[:-1])
        if in_archive:
            r["archive_files"] += 1
        name = p.name
        if name == "LEARNINGS.md":
            r["learnings"] += 1
        if name == "CURRENT.md" and "versions" not in parts_lower:
            r["current_md"] += 1
        if name == "SKILL.md":
            r["skills"].append(rel)
        if len(parts_lower) >= 3 and parts_lower[-2] == "agents" and parts_lower[-3] in (".claude", ".codex") and name.endswith(".md"):
            r["agents"].append(rel)
        if name in ("SECRETS.json", "secrets.json"):
            r["secrets_inventory"] = True
        if name == "registry.json" and "cognition" in parts_lower:
            r["cognition_registry"] = True
        if re.search(r"health", name, re.I) and p.suffix in (".py", ".md", ".sh", ".js", ".ts"):
            r["health_files"].append(rel)
        if re.match(r"(ARCHITECTURE_BOUNDARIES|SOURCES|SOURCE_MAP)", name, re.I):
            r["source_map"].append(rel)
        if name.upper() == "MEMORY.MD":
            r["memory_index"].append(rel)
        if p.suffix in (".db", ".sqlite", ".sqlite3"):
            r["search_index_hint"].append(rel)
        if p.suffix.lower() not in TEXT_EXT:
            continue
        text = read(p)
        if text is None:
            continue
        for label, pat in SECRET_PATTERNS:
            if re.search(pat, text):
                r["secret_hits"].append({"file": rel, "type": label})
        if p.suffix.lower() != ".md":
            continue
        r["md"] += 1
        r["md_bytes"] += size
        fm = frontmatter(text)
        if fm is not None:
            r["frontmatter"] += 1
            d = fm.get("description", "")
            if d:
                r["description"] += 1
                if len(d) >= 40 and d.lower() != fm.get("title", "").lower():
                    r["good_description"] += 1
            body = strip_code(text[text.find("---", 3) + 3:])
            if re.search(r"(?m)^---\s*\n(?:title|date|description):", body):
                r["double_frontmatter"].append(rel)
    for d in root.iterdir() if root.exists() else []:
        if d.is_dir() and "archiv" in d.name.lower():
            r["archive_dirs"].append(d.name)
    r["observations_dirs"] = DIR_COUNTS["observations"]
    entry = {}
    for n in ("AGENTS.md", "CLAUDE.md"):
        t = read(root / n)
        if t is not None:
            entry[n] = t
    r["entry_files"] = sorted(entry)
    blob = " ".join(entry.values()).lower()
    r["boundary_words"] = sum(1 for w in BOUNDARY_WORDS if re.search(w, blob))
    r["git"] = (root / ".git").exists()
    cp = read(root / ".obsidian" / "core-plugins.json") or ""
    r["obsidian_sync"] = bool(re.search(r'"sync"\s*:\s*true', cp)) or '"sync"' in cp and "[" in cp and '"sync"' in cp
    r["cloud_folder"] = next((c for c in ("iCloud", "OneDrive", "Dropbox", "Google Drive", "My Drive") if c.lower() in str(root).lower()), None)
    return r


def pct(a, b):
    return round(100 * a / b) if b else 0


def levels(r):
    fm, desc = pct(r["frontmatter"], r["md"]), pct(r["good_description"], r["md"])
    L = {}
    L["P00"] = (2 if r["entry_files"] and r["boundary_words"] >= 4 else 1 if r["entry_files"] else 0,
                f"entry files: {', '.join(r['entry_files']) or 'none'}; boundary words found: {r['boundary_words']} (heuristic)")
    L["P01"] = (3 if fm >= 95 and desc >= 80 else 2 if fm >= 70 else 1 if fm >= 10 else 0,
                f"frontmatter {fm}% of {r['md']} markdown files; content description {desc}%")
    L["P02"] = (None, "not measurable; ask the owner")
    L["P03"] = (1 if r["agents"] else 0, f"{len(r['agents'])} registered agents" + (" (check: does each cut across areas?)" if r["agents"] else ""))
    L["P04"] = (2 if r["current_md"] and r["current_md"] >= len(r["skills"]) else 1 if r["skills"] or r["current_md"] else 0,
                f"{len(r['skills'])} skill entries, {r['current_md']} live definitions (CURRENT.md)")
    lp = 3 if r["cognition_registry"] else 2 if r["learnings"] and r["observations_dirs"] else 1 if r["learnings"] or r["memory_index"] else 0
    L["P05"] = (lp, f"{r['learnings']} learning logs, {r['observations_dirs']} learning inboxes, memory index: {'yes' if r['memory_index'] else 'no'}, weighted registry: {'yes' if r['cognition_registry'] else 'no'}")
    need = r["md"] > 2000
    L["P06"] = (None, f"{r['md']} markdown files: {'an index is recommended' if need else 'built-in search is enough for now'}; database files seen: {len(r['search_index_hint'])}")
    sh = len(r["secret_hits"])
    L["P07"] = (0 if sh else (2 if r["secrets_inventory"] else 1),
                (f"{sh} secret-like patterns in the vault (fix first!)" if sh else "no secret-like patterns found") +
                f"; inventory: {'yes' if r['secrets_inventory'] else 'no'}")
    L["P08"] = (None, "not measurable; ask which external tools are used")
    L["P09"] = (2 if r["archive_dirs"] and r["archive_files"] else 1 if r["archive_dirs"] else 0,
                f"archive folders: {', '.join(r['archive_dirs']) or 'none'}; archived files: {r['archive_files']}")
    sync = "Obsidian Sync" if r["obsidian_sync"] else r["cloud_folder"] or ("git" if r["git"] else "none detected")
    L["P10"] = (1 if r["git"] else 0, f"version control in vault: {'git' if r['git'] else 'no'}; sync: {sync}; separate backup: ask (sync is not backup)")
    L["P11"] = (1 if r["health_files"] else 0, f"health-check files: {len(r['health_files'])}")
    L["P12"] = (1 if r["source_map"] else 0,
                f"source map: {', '.join(r['source_map'][:2]) or 'none'}; possible sync duplicates (frontmatter twice): {len(r['double_frontmatter'])}")
    return L


NAMES = {"P00": "Constitution & boundaries", "P01": "Persistence", "P02": "Presentation", "P03": "Agent = viewpoint",
         "P04": "Thin entry, live definition", "P05": "Closed-loop learning", "P06": "Search", "P07": "Secrets",
         "P08": "Connectors", "P09": "Forgetting & archiving", "P10": "Backup & recovery", "P11": "Health contract",
         "P12": "One fact, one owner"}


def main():
    ap = argparse.ArgumentParser(description="PAROS vault diagnosis (read-only)")
    ap.add_argument("vault")
    ap.add_argument("--json")
    a = ap.parse_args()
    r = scan(a.vault)
    L = levels(r)
    print(f"PAROS DIAGNOSIS  {r['vault']}")
    print(f"{r['files']} files, {r['md']} markdown, {r['bytes'] / 1e6:.0f} MB "
          f"(markdown {r['md_bytes'] / 1e6:.0f} MB)")
    print("-" * 72)
    for pid, (lvl, ev) in L.items():
        bar = "?? " if lvl is None else LEVEL_BLOCKS[lvl]
        lv = "?" if lvl is None else str(lvl)
        print(f"{pid} {NAMES[pid]:<28} {bar} {lv}  {ev}")
    print("-" * 72)
    print("Levels are a measured starting point (0 none, 1 started, 2 in place, 3 self-sustaining);")
    print("the agent completes them with judgment and the owner's answers. '?' = ask.")
    if r["secret_hits"]:
        print("\nSecret-like patterns (values not shown):")
        for h in r["secret_hits"][:20]:
            print(f"  {h['type']}: {h['file']}")
    if a.json:
        out = {"scan": r, "levels": {k: {"level": v[0], "evidence": v[1]} for k, v in L.items()}}
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nJSON written: {a.json}")


if __name__ == "__main__":
    main()
