# Kit: share-gate (P00, P07, a gate before anything goes public)

A working reference for the publishing boundary in [P00](../../principles/P00-constitution-and-boundaries.md) and the secrets rule in [P07](../../principles/P07-secrets.md): before you push a repository, publish a skill or share a folder, a script checks that nothing personal goes with it. It blocks when it finds:

- an entry of **your personal deny list** (names, companies, clients, machines, private paths, internal identifiers), kept **outside** the repository;
- a **secret-like pattern** (API keys and tokens of common providers, private key headers, password or token assignments);
- an **email address** that is not on the allow list (reserved example domains such as `example.com` and `.test`, and no-reply addresses, are always allowed);
- optionally an **em dash**, if you keep that house style (`--em-dash`).

It checks file contents and file names. It is a single Python file with no dependencies.

Optional. Read it, then adopt or rebuild it for your setup. It is a safety net, not a guarantee: it finds what your list and its patterns describe, and nothing else.

## Why the deny list lives outside the repository

The deny list is exactly the list of what must not be public. If it sits in the repository, publishing the repository publishes the list. The script refuses to run when the list is inside the folder it checks.

Default place: `~/.config/share-gate/DENYLIST.txt`. Another place: set `SHARE_GATE_DENYLIST`, or pass `--deny <file>`.

## Files

| What | Where |
|---|---|
| The script | [`share_gate.py`](share_gate.py) (standard library only, Python 3.8 or newer) |
| An example deny list with invented entries | [`DENYLIST.example.txt`](DENYLIST.example.txt) |
| Your deny list | outside the repository, for example `~/.config/share-gate/DENYLIST.txt` |

## Set up, step by step

1. Copy `DENYLIST.example.txt` to `~/.config/share-gate/DENYLIST.txt` (create the folder if needed).
2. Replace every example entry with your own: your name and the names around you, your companies and clients, machine names, the user name that appears in your paths, private domains and email addresses, internal identifiers. Use `re:` entries to catch spelling variants (`re:\bjane[- _.]?doe\b`).
3. Add `allow:` or `allow-re:` lines for what is public on purpose: the repository's own address, a public project name.
4. Run it once against the repository:

   ```bash
   python share_gate.py path/to/repo
   ```

   Every finding is a `BLOCK` line with the file, the line number and what matched (secrets are shown masked). Exit code 0 means clean, 1 means blocked, 2 means a setup problem.
5. Fix every `BLOCK` line in the files, not in the list. If a line is a deliberate, harmless exception (a test fixture, a documented fake key), add `share-gate: ignore` to that line, or an allow entry to your list.

## As a pre-commit hook

The `--staged` mode checks the **staged version** of each staged file, which is what the commit will contain. Save this as `.git/hooks/pre-commit` in the repository and make it executable (`chmod +x .git/hooks/pre-commit`):

```sh
#!/bin/sh
# share-gate: refuse a commit that carries personal traces
python3 "/path/to/share_gate.py" --staged --quiet . || {
  echo "share-gate blocked this commit. Fix the BLOCK lines above, then commit again."
  exit 1
}
```

On Windows with Git for Windows, the same file works; use `python` instead of `python3` if that is how Python is called on your machine. A hook lives in `.git/hooks/`, so it is per clone: set it up on every machine you commit from. A hook can be skipped with `git commit --no-verify`; that is a deliberate act, never a habit.

For a whole folder before you share it some other way (a zip, a shared drive), run the script on the folder.

## What an agent does with it

- Runs it before any publish, push or share step, and shows the person the result.
- Never edits the deny list on its own and never prints its contents into a chat or a file in the repository.
- Never adds an `allow` entry or an ignore marker to make a finding go away without the person's yes.
- Treats a clean run as "nothing on the list was found", not as "nothing personal is in here": a name nobody put on the list passes. Read the diff as well.

## Limits

- Literal entries match anywhere, case-insensitively; a short entry (three letters) will produce noise. Use a regex with word boundaries for short names.
- The secret patterns cover common providers; a token from a niche service may not look like a secret. Keep secrets out of repositories by design (P07), and treat this as the second line.
- If you run the gate with the example list itself, `DENYLIST.example.txt` matches its own entries; that is expected. Your real list has different entries.
- Binary files and files over 2 MB are skipped; images and documents can still carry names in their metadata.

## Check

A kit works when this passes:

```bash
python share_gate.py --deny /nonexistent/file path/to/repo   # secrets and emails only; exit 0 on a clean repo
```

and when a test file with an entry from your list, a fake key and a private email address gives three `BLOCK` lines and exit code 1.
