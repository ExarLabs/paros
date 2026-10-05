#!/usr/bin/env python3
"""Install or update the PAROS Advisor and its /paros command. Python 3.8+, no dependencies.

    python install.py                 # install or update (idempotent)
    python install.py --uninstall     # remove the /paros command files (keeps the repository copy)
    python install.py --dir <path>    # where the advisor repository lives (default: ~/.paros-advisor)
    python install.py --update        # only refresh the advisor copy (what /paros runs each time)

Works with or without git. Without git it downloads the repository as a zip from GitHub (no account
needed) and refreshes it the same way later; your local state files (.feedback.json, .last-seen) are kept.

What it does:
1. Makes sure the advisor repository is at the install location: clones it if missing, pulls if present
   (or, without git, downloads and refreshes the zip).
2. Writes the /paros command for every agent platform it finds:
   - Claude Code: ~/.claude/commands/paros.md        (type /paros in any session)
   - OpenAI Codex: ~/.codex/prompts/paros.md          (a custom prompt; type /prompts:paros or /paros, depending on the version)
3. Prints what it did. It never touches your vault.
"""
import argparse
import io
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_URL = "https://github.com/ExarLabs/paros-advisor.git"
ZIP_URL = "https://codeload.github.com/ExarLabs/paros-advisor/zip/refs/heads/main"
ZIP_MARK = ".paros-zip"  # marks a copy that came from the zip, so it may be refreshed in place
KEEP = {".feedback.json", ".last-seen", ZIP_MARK}
HERE = Path(__file__).resolve().parent


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def from_zip(target: Path):
    """Download the current repository as a zip and put it at target, keeping local state files."""
    req = urllib.request.Request(ZIP_URL, headers={"User-Agent": "paros-advisor-installer"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(io.BytesIO(data)).extractall(tmp)
        roots = [p for p in Path(tmp).iterdir() if p.is_dir()]
        if len(roots) != 1 or not (roots[0] / "AGENTS.md").exists():
            raise RuntimeError("the download does not look like the advisor repository")
        target.mkdir(parents=True, exist_ok=True)
        for old in target.iterdir():
            if old.name in KEEP:
                continue
            shutil.rmtree(old) if old.is_dir() and not old.is_symlink() else old.unlink()
        for new in roots[0].iterdir():
            if new.name in KEEP:
                continue
            (shutil.copytree if new.is_dir() else shutil.copy2)(new, target / new.name)
    (target / ZIP_MARK).write_text(ZIP_URL + "\n", encoding="utf-8")


def ensure_repo(target: Path):
    if (target / ".git").exists():
        r = git("-C", str(target), "pull", "--ff-only", "-q")
        return "updated" if r.returncode == 0 else f"kept local copy (pull failed: {r.stderr.strip()[:120]})"
    zip_copy = (target / ZIP_MARK).exists()
    if target.exists() and any(target.iterdir()) and not zip_copy:
        sys.exit(f"{target} exists and is not a copy of the advisor; choose another --dir")
    if not zip_copy and shutil.which("git"):
        r = git("clone", "-q", REPO_URL, str(target))
        if r.returncode == 0:
            return "cloned"
        print("git clone failed, downloading the zip instead: " + r.stderr.strip()[:120])
    try:
        from_zip(target)
    except Exception as e:
        if zip_copy:
            return f"kept local copy (download failed: {str(e)[:120]})"
        sys.exit(f"download failed: {e}")
    return "updated (zip)" if zip_copy else "downloaded (zip, no git needed)"


def command_text(target: Path):
    src = (target / "install" / "paros.command.md")
    if not src.exists():
        src = HERE / "paros.command.md"
    return src.read_text(encoding="utf-8").replace("{{ADVISOR_DIR}}", target.as_posix())


def main():
    ap = argparse.ArgumentParser(description="Install the PAROS Advisor and the /paros command")
    ap.add_argument("--dir", default=str(Path.home() / ".paros-advisor"))
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--update", action="store_true", help="only refresh the advisor copy")
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

    if a.update:
        print(f"PAROS Advisor: {ensure_repo(target)}")
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
