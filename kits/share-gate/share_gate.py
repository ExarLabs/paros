#!/usr/bin/env python3
"""share-gate: block publishing when a repository holds personal traces.

Checks every text file (and every file name) for:
  * entries of your personal deny list (names, companies, clients, machines,
    private paths), kept OUTSIDE the repository;
  * secret-like patterns (API keys, tokens, private keys, password assignments);
  * email addresses that are not on the allow list (reserved example domains and
    no-reply addresses are always allowed);
  * optionally, em dashes (--em-dash), for people who keep that style rule.

Usage:
  python share_gate.py <file or folder> ...         report; exit code 1 on any BLOCK
  python share_gate.py --staged [<repo>]            only the staged version of staged files
                                                    (for a pre-commit hook)
Options:
  --deny FILE      deny list (default: $SHARE_GATE_DENYLIST, then
                   ~/.config/share-gate/DENYLIST.txt)
  --allow FILE     extra allow list (same format as allow lines, one per line)
  --em-dash        also block the em dash character
  --quiet          print only BLOCK lines and the summary

Deny list format, one entry per line:
  # comment
  Jane Example            literal, case-insensitive
  re:\\bACME[- ]?Corp\\b    regular expression, case-insensitive
  allow:jane@example.org  literal that is always allowed (removed before checking)
  allow-re:github\\.com/your-org   regular expression that is always allowed

A line containing the marker "share-gate: ignore" is skipped entirely.
Standard library only. Exit codes: 0 clean, 1 blocked, 2 usage or setup error.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "1.0.0"
IGNORE_MARK = "share-gate: ignore"
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache"}
MAX_BYTES = 2_000_000

SECRETS = [
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI key", r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{32,}"),
    ("Groq key", r"\bgsk_[A-Za-z0-9]{30,}"),
    ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    ("GitHub token", r"\bgithub_pat_[A-Za-z0-9_]{40,}"),
    ("AWS access key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Google API key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    ("Stripe live key", r"\b[rs]k_live_[A-Za-z0-9]{20,}"),
    ("private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("password or token assignment",
     r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*[\"'][^\"'\s<>{}$]{12,}[\"']"),
]

EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
BUILTIN_ALLOW = [
    # RFC 2606 reserved names: safe for invented examples
    r"[\w.+\-]+@(?:[\w\-]+\.)*example(?:\.(?:com|org|net))?\b",
    r"[\w.+\-]+@[\w.\-]*\.(?:example|test|invalid|localhost)\b",
    # no-reply senders carry no person
    r"\b(?:no-?reply|do-?not-?reply)@[\w.\-]+\.[A-Za-z]{2,}\b",
    r"[\w.+\-]+@users\.noreply\.github\.com\b",
]
EM_DASH = chr(0x2014)


def default_deny():
    env = os.environ.get("SHARE_GATE_DENYLIST")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".config" / "share-gate" / "DENYLIST.txt"


def load_lists(deny_path, allow_path):
    deny, allow = [], list(BUILTIN_ALLOW)
    sources = []
    if deny_path and deny_path.is_file():
        sources.append(deny_path)
    if allow_path:
        if not allow_path.is_file():
            sys.exit(f"share-gate: allow list not found: {allow_path}")
        sources.append(allow_path)
    for src in sources:
        is_allow_file = src == allow_path
        for raw in src.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("allow-re:"):
                allow.append(line[len("allow-re:"):])
            elif line.startswith("allow:"):
                allow.append(re.escape(line[len("allow:"):]))
            elif is_allow_file:
                allow.append(line[3:] if line.startswith("re:") else re.escape(line))
            elif line.startswith("re:"):
                deny.append((line, re.compile(line[3:], re.I)))
            else:
                deny.append((line, re.compile(re.escape(line), re.I)))
    allow_re = re.compile("|".join(f"(?:{a})" for a in allow), re.I)
    return deny, allow_re


def walk(args):
    out = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                out += [Path(root) / n for n in names]
        elif p.is_file():
            out.append(p)
        else:
            sys.exit(f"share-gate: not found: {a}")
    return [(str(p), p.read_bytes) for p in out]


def staged(repo):
    def git(*a):
        return subprocess.run(["git", "-C", str(repo), *a], capture_output=True)
    names = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout.decode("utf-8", "replace")
    return [(n, (lambda n=n: git("show", f":{n}").stdout)) for n in names.split("\0") if n]


def text_of(reader):
    try:
        data = reader()
    except OSError:
        return None
    if len(data) > MAX_BYTES or b"\0" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def mask(s):
    return s[:4] + "..." if len(s) > 8 else "..."


def check(items, deny, allow_re, em_dash):
    blocks = []
    for name, reader in items:
        clean_name = allow_re.sub("", name)
        for label, pat in deny:
            m = pat.search(clean_name)
            if m:
                blocks.append(f"{name}: file name: deny list entry «{m.group(0)}»")
        text = text_of(reader)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if IGNORE_MARK in line:
                continue
            clean = allow_re.sub("", line)
            seen = set()
            for label, pat in deny:
                m = pat.search(clean)
                if m and m.group(0).lower() not in seen:
                    seen.add(m.group(0).lower())
                    blocks.append(f"{name}:{i}: deny list entry «{m.group(0)}»")
            for label, pat in SECRETS:
                m = re.search(pat, line)
                if m:
                    blocks.append(f"{name}:{i}: secret-like pattern ({label}) «{mask(m.group(0))}»")
            for m in EMAIL.finditer(clean):
                blocks.append(f"{name}:{i}: email address not on the allow list «{m.group(0)}»")
            if em_dash and EM_DASH in line:
                blocks.append(f"{name}:{i}: em dash")
    return blocks


def main(argv):
    args, deny_path, allow_path, em_dash, quiet, staged_repo = [], None, None, False, False, None
    it = iter(argv)
    for a in it:
        if a == "--deny":
            deny_path = Path(next(it, "")).expanduser()
        elif a == "--allow":
            allow_path = Path(next(it, "")).expanduser()
        elif a == "--em-dash":
            em_dash = True
        elif a == "--quiet":
            quiet = True
        elif a == "--staged":
            staged_repo = "."
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a == "--version":
            print(VERSION)
            return 0
        else:
            args.append(a)
    if staged_repo and args:
        staged_repo, args = args[0], args[1:]
    if not staged_repo and not args:
        print(__doc__)
        return 2

    deny_path = deny_path or default_deny()
    targets = [Path(staged_repo)] if staged_repo else [Path(a) for a in args]
    if deny_path.is_file():
        dp = deny_path.resolve()
        for t in targets:
            t = t.resolve()
            if t.is_dir() and (dp == t or t in dp.parents):
                print(f"share-gate: the deny list {deny_path} is inside {t}. Keep it outside "
                      f"the repository, or the list itself leaks what it protects.")
                return 2
    elif not quiet:
        print(f"share-gate: no deny list at {deny_path}; checking secrets and emails only.")

    deny, allow_re = load_lists(deny_path, allow_path)
    items = staged(Path(staged_repo)) if staged_repo else walk(args)
    blocks = check(items, deny, allow_re, em_dash)
    for b in blocks:
        print("BLOCK  " + b)
    if not quiet or blocks:
        print(f"\nshare-gate {VERSION}: {len(items)} files checked, {len(deny)} deny entries, "
              f"{len(blocks)} blocking findings")
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
