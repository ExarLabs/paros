# Installing the PAROS Advisor (instructions for an AI agent)

A person sent you here (or to https://ignis.academy/paros) to install the PAROS Advisor. Do this, then tell them in one or two lines what happened, in their language.

1. **Check Python** (`python --version` or `python3 --version`). If it is missing, tell the person how to install it for their system and stop. Git is optional: with git the advisor is cloned, without it a zip is downloaded from GitHub (no account needed), and updates work either way.
2. **Get the repository** into a hidden folder in their home directory (not inside any notes folder):
   - with git:
     ```bash
     git clone https://github.com/ExarLabs/paros-advisor.git ~/.paros-advisor
     ```
     If `~/.paros-advisor` already exists, update it instead: `git -C ~/.paros-advisor pull --ff-only`.
   - without git: download the installer alone and let it fetch the rest:
     ```bash
     curl -fsSL -o paros-install.py https://raw.githubusercontent.com/ExarLabs/paros-advisor/main/install/install.py
     python paros-install.py
     ```
     It downloads the repository as a zip into `~/.paros-advisor` and installs `/paros` in one go (then skip step 3, and delete `paros-install.py`). On Windows `curl` is built in since Windows 10.
3. **Install the `/paros` command:**
   ```bash
   python ~/.paros-advisor/install/install.py
   ```
   (use `python3` if that is the name on their system). It works the same for a cloned and a downloaded copy. It writes the command for Claude Code (`~/.claude/commands/paros.md`) and, if Codex is used on this machine, for Codex (`~/.codex/prompts/paros.md`). It never touches their notes.
4. **Tell the person, in their language** (the install sentence is English by design; if you cannot tell their language, ask in one short line), that the advisor is installed and updates itself each time it is used. Then ask **one** question: do they already have a notes folder (for example an Obsidian vault)?
   - **Yes, and this session is in it:** offer to start right here (step 5).
   - **Yes, elsewhere:** explain how to open a session in that folder (Claude desktop app: the Code tab, a new session, choose that folder; terminal users: `cd` there and start the agent), then type `/paros`.
   - **No, or unsure:** offer to start from zero right now, in this session, with `~/.paros-advisor/playbooks/start-from-zero.md`: Obsidian first, one step at a time, no commands to type.
5. To start in this session, read `~/.paros-advisor/AGENTS.md` and follow it (the tour, or start-from-zero for someone without notes).

To remove: `python ~/.paros-advisor/install/install.py --uninstall`, then delete `~/.paros-advisor`.
