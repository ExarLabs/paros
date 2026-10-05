# Changelog: think

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.0.0 (2026-10-05)

- First public version. An orchestrator agent assembles a team of external AIs with roles (researcher, strategist, validator, optional domain expert and creative), sends one fat prompt per member with a fenced findings JSON contract and an end token, runs all members in parallel, parses leniently (fenced block, raw JSON decode, flat shape), merges at field level by the source trust order, and persists everything in one brainstorm state file per topic.
- Transport rule: API by default; a browser only for voice, account-side data, AIs with no API, or a live human conversation. API payloads are built from a file with `jq --rawfile`.
- Browser choice: a per-machine registry of the last browser that worked, written only after a successful select, with the person asked only when the choice is ambiguous.
- Verbatim transcript archiving for browser threads with strategic value, regenerated in full and verified by parse and character count.
- **New convention, recipe and spice:** the general procedure lives in `CURRENT.md`; personal configuration (AIs, accounts, preferred team, presets, browser registry, key variable names) lives in `LOCAL.md`, started from `LOCAL.example.md`. `CURRENT.md` never holds personal values.
- Constitution: state file is canonical memory, drift rule, source trust order, verified browser identifiers only, verbatim archive for strategic threads, the person decides, personal values only in `LOCAL.md`.
- Pitfalls R-001 to R-010, carried over from a skill in daily use since mid 2026.
- To review: copy `LOCAL.example.md` to `LOCAL.md` and fill it in; if you already keep a browser registry or a list of AI accounts elsewhere, point `LOCAL.md` at it instead of duplicating (P12); keep `LOCAL.md` out of anything you share or publish.
