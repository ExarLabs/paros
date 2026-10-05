#!/usr/bin/env python3
"""PAROS Advisor feedback: report something worth improving, without spamming anyone.

Python 3.8+, no dependencies. Used by the advisor agent (see AGENTS.md, "Feedback to the
PAROS Advisor"); a person can also run it by hand.

    python feedback.py status                     # is asking allowed, and when was the last ask
    python feedback.py can-ask --topic <slug>     # prints "yes" or "no: <reason>"; exit 0 or 1
    python feedback.py asked --topic <slug> --answer yes|no|never
    python feedback.py optout                     # never ask again (on this machine)
    python feedback.py optin                      # allow asking again
    python feedback.py submit --title "..." --body-file report.md [--kind improvement|missing|bug] [--dry-run]

How a report reaches the maintainers:
- with the GitHub CLI (`gh`, signed in): forks the repository if needed, creates a branch
  `proposal/<date>-<slug>` in the fork, adds `proposals/<date>-<slug>.md`, and opens a pull request.
  Nobody but the maintainers can change `main`; a pull request is only a proposal.
- without it: prints (and tries to open) a pre-filled "new issue" page; the person reviews it in
  their browser and clicks Submit themselves.

Settings live next to this repository copy, in `.feedback.json` (ignored by git, never uploaded).
Rules that keep it quiet: at most one question per day, never twice about the same topic,
and after the person says "never", no more questions until they run `optin`.
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import webbrowser
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = "ExarLabs/paros-advisor"
ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT / ".feedback.json"
MIN_HOURS_BETWEEN_ASKS = 24
PRIVATE = [
    ("email address", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}"),
    ("home path", r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)[^\s/\\]+"),
    ("API key or token", r"sk-[A-Za-z0-9_\-]{20,}|gsk_[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"),
    ("private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("phone number", r"\+?\d[\d \-]{8,}\d"),
]
ALLOWED_EMAIL = re.compile(r"@(?:[\w-]+\.)*(?:example|test|invalid)\b|@example\.(?:com|org|net)\b|noreply@")


def now():
    return dt.datetime.now(dt.timezone.utc)


def load():
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except Exception:
        return {"ask": True, "last_asked": None, "topics": {}, "reports": []}


def save(s):
    SETTINGS.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")


def can_ask(s, topic):
    if not s.get("ask", True):
        return False, "the person asked never to be asked again (run optin to allow)"
    if topic and topic in s.get("topics", {}):
        return False, f"already asked about '{topic}' ({s['topics'][topic]['answer']})"
    last = s.get("last_asked")
    if last:
        hours = (now() - dt.datetime.fromisoformat(last)).total_seconds() / 3600
        if hours < MIN_HOURS_BETWEEN_ASKS:
            return False, f"asked {hours:.0f} hours ago; at most one question per {MIN_HOURS_BETWEEN_ASKS} hours"
    return True, ""


def private_findings(text):
    found = []
    for label, pat in PRIVATE:
        for m in re.finditer(pat, text):
            if label == "email address" and ALLOWED_EMAIL.search(m.group(0)):
                continue
            found.append(label)
            break
    return found


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:50] or "proposal"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def submit_with_gh(title, body, kind, dry):
    slug = slugify(title)
    date = now().date().isoformat()
    branch = f"proposal/{date}-{slug}"
    path = f"proposals/{date}-{slug}.md"
    doc = f"---\ntitle: {title}\nkind: {kind}\ndate: {date}\nstatus: proposed\n---\n\n{body.strip()}\n"
    if dry:
        return f"[dry-run] would fork {REPO}, create branch {branch}, add {path}, open a pull request titled: {title}"
    who = run(["gh", "api", "user", "--jq", ".login"])
    if who.returncode != 0:
        raise RuntimeError("gh is installed but not signed in (run: gh auth login)")
    login = who.stdout.strip()
    work = Path(tempfile.mkdtemp(prefix="paros-proposal-"))
    run(["gh", "repo", "fork", REPO, "--clone=false"])
    fork = f"{login}/{REPO.split('/')[1]}"
    r = run(["gh", "repo", "clone", fork, str(work / "repo"), "--", "--depth", "1"])
    if r.returncode != 0:
        raise RuntimeError("could not clone the fork: " + r.stderr.strip()[:200])
    repo = work / "repo"
    run(["git", "checkout", "-b", branch], cwd=repo)
    (repo / "proposals").mkdir(exist_ok=True)
    (repo / path).write_text(doc, encoding="utf-8")
    run(["git", "add", path], cwd=repo)
    c = run(["git", "commit", "-m", f"proposal: {title}"], cwd=repo)
    if c.returncode != 0:
        raise RuntimeError("commit failed: " + (c.stderr or c.stdout).strip()[:200])
    p = run(["git", "push", "-u", "origin", branch], cwd=repo)
    if p.returncode != 0:
        raise RuntimeError("push to your fork failed: " + p.stderr.strip()[:200])
    pr = run(["gh", "pr", "create", "--repo", REPO, "--head", f"{login}:{branch}", "--base", "main",
              "--title", f"[{kind}] {title}", "--body", body.strip() + "\n\n(Sent from the PAROS Advisor feedback flow.)"])
    if pr.returncode != 0:
        raise RuntimeError("pull request failed: " + pr.stderr.strip()[:200])
    shutil.rmtree(work, ignore_errors=True)
    return pr.stdout.strip()


def issue_url(title, body, kind):
    q = urllib.parse.urlencode({"title": f"[{kind}] {title}", "body": body.strip() + "\n\n(Sent from the PAROS Advisor feedback flow.)",
                                "labels": f"proposal,{kind}"})
    return f"https://github.com/{REPO}/issues/new?{q}"


def main():
    ap = argparse.ArgumentParser(description="PAROS Advisor feedback")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    p = sp.add_parser("can-ask"); p.add_argument("--topic", default="")
    p = sp.add_parser("asked"); p.add_argument("--topic", required=True); p.add_argument("--answer", required=True, choices=["yes", "no", "never"])
    sp.add_parser("optout"); sp.add_parser("optin")
    p = sp.add_parser("submit"); p.add_argument("--title", required=True); p.add_argument("--body-file", required=True)
    p.add_argument("--kind", default="improvement", choices=["improvement", "missing", "bug"]); p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-gh", action="store_true", help="skip the GitHub CLI and use the issue page")
    a = ap.parse_args()
    s = load()

    if a.cmd == "status":
        ok, why = can_ask(s, "")
        print(json.dumps({"ask_allowed": s.get("ask", True), "can_ask_now": ok, "reason": why,
                          "last_asked": s.get("last_asked"), "topics_asked": len(s.get("topics", {})),
                          "reports": len(s.get("reports", []))}, ensure_ascii=False, indent=1))
    elif a.cmd == "can-ask":
        ok, why = can_ask(s, a.topic)
        print("yes" if ok else f"no: {why}")
        sys.exit(0 if ok else 1)
    elif a.cmd == "asked":
        s.setdefault("topics", {})[a.topic] = {"answer": a.answer, "at": now().isoformat(timespec="seconds")}
        s["last_asked"] = now().isoformat(timespec="seconds")
        if a.answer == "never":
            s["ask"] = False
        save(s)
        print("recorded" + (" (no more questions until optin)" if a.answer == "never" else ""))
    elif a.cmd == "optout":
        s["ask"] = False; save(s); print("ok: the advisor will not ask about reporting again on this machine")
    elif a.cmd == "optin":
        s["ask"] = True; save(s); print("ok: the advisor may ask again (at most once a day, never twice about one topic)")
    elif a.cmd == "submit":
        body = Path(a.body_file).read_text(encoding="utf-8")
        leaks = private_findings(a.title + "\n" + body)
        if leaks:
            print("STOP: the report seems to contain personal data: " + ", ".join(sorted(set(leaks))) +
                  ". Remove it, show the person the cleaned text, and try again.")
            sys.exit(2)
        if not a.no_gh and shutil.which("gh"):
            try:
                result = submit_with_gh(a.title, body, a.kind, a.dry_run)
                print(result)
                if not a.dry_run:
                    s.setdefault("reports", []).append({"title": a.title, "at": now().isoformat(timespec="seconds"), "via": "pull request", "url": result})
                    save(s)
                return
            except RuntimeError as e:
                print(f"GitHub CLI path failed ({e}); falling back to the issue page.")
        url = issue_url(a.title, body, a.kind)
        if a.dry_run:
            print("[dry-run] issue page: " + url)
            return
        print("Open this page, check the text, and click Submit (you need a GitHub account):\n" + url)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        s.setdefault("reports", []).append({"title": a.title, "at": now().isoformat(timespec="seconds"), "via": "issue page"})
        save(s)


if __name__ == "__main__":
    main()
