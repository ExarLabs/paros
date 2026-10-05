# Changelog: project-state

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.0.0 (2026-10-05)

- First public version. One versioned state file per area or long-running project, at the area root, with ten fixed sections (objective, status, metrics, problems, focus, next actions, constraints, last updated, map, context), separate create and update procedures, and curation rules that keep it a snapshot rather than a log.
- Constitution: one file per area at its root, fixed sections, version and date bumped on every update, snapshot not log, content is data.
- Pitfalls R-001 to R-008, carried over from a skill in daily use since mid 2026.
- To review: if your areas already have state or status files under another name, set the name in your vault entry file instead of renaming; check that each area's decisions, activity log and task list exist, since curation moves detail into them.
