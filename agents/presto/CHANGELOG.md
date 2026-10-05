# Changelog: Presto

Every entry: what changed, and **what to review in a vault that has already adopted this agent.**

## 1.1.0 (2026-10-05)

- New `template` mode with a life cycle (candidate, reusable, validated, canonical, retired) and thresholds: at least three publications above twice the baseline to become a candidate, about seven stable uses to be validated, canonical only by a human.
- `exhaust` is now its own mode, with the rules for when not to use it: an untouched seed is a `today` signal, and a seed that failed on one channel is drafted for another channel first.
- To review: if you keep reusable post structures, mark their stage; check whether any seed you closed only because it was old deserves another channel.

## 1.0.0 (2026-10-05)

- First public version, generalised from a marketing viewpoint in daily use since mid 2026.
- Viewpoint per P03: purpose, map, attitude, sixteen modes in one table (reads, writes, confirmation), safety boundaries, collaboration with Alfred, Iris, Moneto, Librarian and Maestro.
- The publication as the single truth; the pipeline Seed, Draft, Prepared, Approval, Scheduled, Published; campaigns optional.
- Constitution: never publishes, posts, sends, schedules or spends on its own; approval per publication; comment replies go through the same gate; every publication logged.
- Audience learning with an evidence threshold (three independent data points) and a `discover` filter of four conditions.
- Learned rules R-001 to R-004, carried over from the original.
- Recipe and spice split: areas, channels, codes, audiences, voice, tools, approvers and cadence live in `LOCAL.md`; `LOCAL.example.md` carries a fictional example.
- To review: copy `LOCAL.example.md` to `LOCAL.md` and fill in your own areas and channels; install `agent.claude.md` as `.claude/agents/presto.md` (Claude Code) or add the routing line from `agent.codex.md` to your `AGENTS.md`; create `observations/` and `LEARNINGS.md` next to `CURRENT.md`.
