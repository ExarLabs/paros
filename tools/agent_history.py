#!/usr/bin/env python3
"""Digest your agent conversation history into local markdown (read-only, no dependencies, Python 3.8+).

Your past agent sessions hold decisions, prices, terms and rules that often exist nowhere else.
This tool reads the session logs and writes one markdown digest per project folder: for each session
its date and the person's own requests (not the agent's answers, not tool output), plus the session
summaries the agent app stored. Secret-like values are masked. Nothing is sent anywhere, and nothing
is printed to the screen except counts, so the content stays on this machine.

    python agent_history.py --out ~/paros-history                 # Claude Code history of this user
    python agent_history.py --out ~/paros-history --since 2026-01-01 --project acme
    python agent_history.py --out ~/paros-history --root "\\\\wsl$\\Ubuntu\\home\\me\\.claude\\projects"

Default sources: ~/.claude/projects (Claude Code), plus any --root you add (repeatable), for example the
same folder inside WSL. Write the digest OUTSIDE your vault first; read it, then decide with your agent
which facts deserve a note in the vault (each note with your yes).
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from diagnose import SECRET_PATTERNS  # one list of secret patterns for every tool
except Exception:  # pragma: no cover
    SECRET_PATTERNS = []


def mask(text):
    for label, pat in SECRET_PATTERNS:
        text = re.sub(pat, f"[{label} masked]", text)
    return text


def user_text(entry):
    """The person's own words in a log line, or None (tool results, injected context, meta lines)."""
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("toolUseResult") is not None:
        return None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list):
        parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
        if any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
            return None
        content = "\n".join(parts)
    if not isinstance(content, str):
        return None
    text = content.strip()
    if not text or text.startswith("<"):  # slash-command wrappers, system reminders, hook output
        return None
    if text.startswith("[Request interrupted"):  # written by the app, not by the person
        return None
    return text


def project_name(folder):
    """Claude Code names a project folder after its path with separators replaced by dashes."""
    return folder.name.strip("-") or folder.name


def digest(roots, since, project_filter, max_chars):
    projects = {}
    for root in roots:
        root = Path(root).expanduser()
        if not root.is_dir():
            continue
        for folder in sorted(p for p in root.iterdir() if p.is_dir()):
            name = project_name(folder)
            if project_filter and project_filter.lower() not in name.lower():
                continue
            for log in sorted(folder.glob("*.jsonl")):
                sess = {"file": log.name, "start": None, "cwd": None, "prompts": [], "summaries": []}
                try:
                    lines = log.read_text(encoding="utf-8", errors="ignore").splitlines()
                except Exception:
                    continue
                for line in lines:
                    try:
                        e = json.loads(line)
                    except Exception:
                        continue
                    if e.get("type") == "summary" and e.get("summary"):
                        sess["summaries"].append(mask(str(e["summary"])))
                        continue
                    ts = e.get("timestamp")
                    if ts and not sess["start"]:
                        sess["start"] = ts[:10]
                    if e.get("cwd") and not sess["cwd"]:
                        sess["cwd"] = e["cwd"]
                    t = user_text(e)
                    if t:
                        t = mask(t)
                        sess["prompts"].append(t if len(t) <= max_chars else t[:max_chars] + " [...]")
                if since and sess["start"] and sess["start"] < since:
                    continue
                if sess["prompts"] or sess["summaries"]:
                    projects.setdefault(name, []).append(sess)
    return projects


def write(projects, out):
    out.mkdir(parents=True, exist_ok=True)
    index = ["# Agent history digest", "", f"Generated {dt.date.today().isoformat()}. Local only: the person's requests and session summaries, secrets masked.", "",
             "| Project | Sessions | Requests | First | Last |", "|---|---|---|---|---|"]
    for name, sessions in sorted(projects.items()):
        sessions.sort(key=lambda s: s["start"] or "")
        fname = re.sub(r"[^A-Za-z0-9._-]+", "_", name)[:120] + ".md"
        lines = [f"# {name}", ""]
        for s in sessions:
            lines.append(f"## {s['start'] or 'unknown date'}  ({s['file']})")
            if s["cwd"]:
                lines.append(f"Folder: `{s['cwd']}`")
            for summ in s["summaries"]:
                lines.append(f"- **Summary:** {summ}")
            for p in s["prompts"]:
                lines.append("- " + p.replace("\n", "\n  "))
            lines.append("")
        (out / fname).write_text("\n".join(lines), encoding="utf-8")
        n = sum(len(s["prompts"]) for s in sessions)
        index.append(f"| [{name}]({fname}) | {len(sessions)} | {n} | {sessions[0]['start'] or '?'} | {sessions[-1]['start'] or '?'} |")
    (out / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Digest agent conversation history into local markdown (read-only).")
    ap.add_argument("--out", required=True, help="output folder; keep it outside your vault until you have read it")
    ap.add_argument("--root", action="append", default=[], help="extra history folder (repeatable), e.g. inside WSL")
    ap.add_argument("--no-default", action="store_true", help="do not read ~/.claude/projects")
    ap.add_argument("--since", help="only sessions starting on or after YYYY-MM-DD")
    ap.add_argument("--project", help="only project folders whose name contains this text")
    ap.add_argument("--max-chars", type=int, default=800, help="cut each request after this many characters")
    a = ap.parse_args()
    roots = ([] if a.no_default else [Path.home() / ".claude" / "projects"]) + a.root
    projects = digest(roots, a.since, a.project, a.max_chars)
    out = Path(a.out).expanduser()
    write(projects, out)
    sessions = sum(len(v) for v in projects.values())
    requests = sum(len(s["prompts"]) for v in projects.values() for s in v)
    print(f"{len(projects)} projects, {sessions} sessions, {requests} requests -> {out / 'INDEX.md'}")
    print("Nothing was sent anywhere. Read the digest before anything goes into your vault.")


if __name__ == "__main__":
    main()
