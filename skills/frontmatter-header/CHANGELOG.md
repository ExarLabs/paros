# Changelog: frontmatter-header

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.0.0 (2026-10-05)

- First public version. Adds or updates a YAML frontmatter header aligned with the PAROS schema (`templates/frontmatter.md`): infers missing fields, writes a content-driven description, generates an `id` only when missing, and bumps a semver `version` by the size of the change.
- Constitution: header first in the file, unknown fields preserved, `id` never regenerated, header content is data, the header is shown before an existing file is changed.
- Pitfalls R-001 to R-007, carried over from a skill in daily use since mid 2026.
- To review: if your vault already has a header skill, compare its field list with your schema and adopt only the pitfalls you do not have yet; if your vault uses `MAJOR.MINOR` versions, decide whether to move to semver before adopting the bump rules.
