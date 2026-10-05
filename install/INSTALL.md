# Installing the PAROS Advisor (instructions for an AI agent)

A person sent you here (or to https://ignis.academy/paros) to install the PAROS Advisor. Do this, then tell them in one or two lines what happened, in their language.

1. **Check git and Python** (`git --version`, `python --version` or `python3 --version`). If git is missing, tell the person how to install it for their system and stop.
2. **Get the repository** into a hidden folder in their home directory (not inside any notes folder):
   ```bash
   git clone https://github.com/ExarLabs/paros-advisor.git ~/.paros-advisor
   ```
   If `~/.paros-advisor` already exists, update it instead: `git -C ~/.paros-advisor pull --ff-only`.
3. **Install the `/paros` command:**
   ```bash
   python ~/.paros-advisor/install/install.py
   ```
   (use `python3` if that is the name on their system). It writes the command for Claude Code (`~/.claude/commands/paros.md`) and, if Codex is used on this machine, for Codex (`~/.codex/prompts/paros.md`). It never touches their notes.
4. **Tell the person:** "The PAROS Advisor is installed. Open a new session in your notes folder and type `/paros` (or `/paros <your question>`). It updates itself each time you use it."
5. If they want to start right away in this session, read `~/.paros-advisor/AGENTS.md` and begin with the tour.

To remove: `python ~/.paros-advisor/install/install.py --uninstall`, then delete `~/.paros-advisor`.
