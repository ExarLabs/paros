# Contributing

The PAROS Advisor grows from what people learn while using it.

- **Easiest:** let your agent do it. When it notices a gap or an error, it asks you once whether to report it (you can say "never ask again"), shows you the exact text, and sends it with your yes, straight to the maintainers' inbox. **You do not need a GitHub account,** or any account. See "Feedback to the PAROS Advisor" in [`AGENTS.md`](AGENTS.md).
- **With GitHub:** your agent can send it as a pull request instead (`--via github`), or open an issue, or a pull request from your fork that adds `proposals/YYYY-MM-DD-<slug>.md` (see [`proposals/`](proposals/README.md)).

Rules for every contribution:
- **No personal data:** no names, emails, paths, company or client details, secrets, note contents. Use made-up examples.
- **English,** and no em dashes in prose.
- **Small and concrete:** what happened, what is missing or wrong, the change you suggest (which file), and why it helps others.

Only the maintainers change `main`. A pull request is a proposal; accepted ideas are integrated by the maintainers, usually as a separate commit, with a line in `CHANGELOG.md`.
