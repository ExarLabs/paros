#!/usr/bin/env python3
"""Install or update the PAROS Advisor and its /paros command. Python 3.8+, no dependencies.

    python install.py                 # install or update (idempotent)
    python install.py --uninstall     # remove the /paros command files (keeps the repository copy)
    python install.py --dir <path>    # where the advisor repository lives (default: ~/.paros-advisor)

What it does:
1. Makes sure the advisor repository is at the install location: clones it if missing, pulls if present.
2. Writes the /paros command for every agent platform it finds:
   - Claude Code: ~/.claude/commands/paros.md        (type /paros in any session)
   - OpenAI Codex: ~/.codex/prompts/paros.md          (a custom prompt; type /prompts:paros or /paros, depending on the version)
3. Prints what it did. It never touches your vault.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_URL = "https://github.com/ExarLabs/paros-advisor.git"
HERE = Path(__file__).resolve().parent


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def ensure_repo(target: Path):
    if (target / ".git").exists():
        r = git("-C", str(target), "pull", "--ff-only", "-q")
        return "updated" if r.returncode == 0 else f"kept local copy (pull failed: {r.stderr.strip()[:120]})"
    if target.exists() and any(target.iterdir()):
        sys.exit(f"{target} exists and is not a git clone of the advisor; choose another --dir")
    if shutil.which("git") is None:
        sys.exit("git is not installed; install git, or download the repository as a zip into " + str(target))
    r = git("clone", "-q", REPO_URL, str(target))
    if r.returncode != 0:
        sys.exit("clone failed: " + r.stderr.strip())
    return "cloned"


def command_text(target: Path):
    src = (target / "install" / "paros.command.md")
    if not src.exists():
        src = HERE / "paros.command.md"
    return src.read_text(encoding="utf-8").replace("{{ADVISOR_DIR}}", target.as_posix())


def main():
    ap = argparse.ArgumentParser(description="Install the PAROS Advisor and the /paros command")
    ap.add_argument("--dir", default=str(Path.home() / ".paros-advisor"))
    ap.add_argument("--uninstall", action="store_true")
    a = ap.parse_args()
    target = Path(a.dir).expanduser().resolve()
    homes = {"Claude Code": Path.home() / ".claude" / "commands", "OpenAI Codex": Path.home() / ".codex" / "prompts"}

    if a.uninstall:
        for name, d in homes.items():
            f = d / "paros.md"
            if f.exists():
                f.unlink()
                print(f"removed /paros for {name}: {f}")
        print(f"the repository copy stays at {target}; delete it by hand if you want")
        return

    print(f"PAROS Advisor: {ensure_repo(target)} at {target}")
    text = command_text(target)
    installed = 0
    for name, d in homes.items():
        if not d.parent.exists():
            continue  # this platform is not used on this machine
        d.mkdir(parents=True, exist_ok=True)
        (d / "paros.md").write_text(text, encoding="utf-8")
        print(f"/paros installed for {name}: {d / 'paros.md'}")
        installed += 1
    if not installed:
        d = homes["Claude Code"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "paros.md").write_text(text, encoding="utf-8")
        print(f"/paros installed for Claude Code: {d / 'paros.md'}")
    version = (target / "VERSION").read_text(encoding="utf-8").strip() if (target / "VERSION").exists() else "?"
    print(f"\nDone (advisor v{version}). Start a NEW session in your notes folder and type: /paros")


if __name__ == "__main__":
    main()
