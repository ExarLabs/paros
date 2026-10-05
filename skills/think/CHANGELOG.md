# Changelog: think

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.1.0 (2026-10-05)

- An exhausted API credit is now its own failure mode, separate from a rate limit: no backoff, no retry; the member switches to the browser for the rest of the session, the state file records it, and the person gets one line saying the credit needs topping up (R-011). Team assembly notes that a present key is not proof of a usable key, with an optional cheap ping before an expensive round.
- Browser rounds: long prompts come in through a file (a temporary file input, one insert, a character count check) instead of typing or a local server fetch that the site's content security policy blocks (R-012); a send is confirmed by an empty composer and a conversation identifier in the page address.
- Deep reasoning modes get a long wait budget instead of a short fixed timeout (R-013); a return value blocked by the browser bridge as cookie or query-string data means a different read path, not a retry (R-014). Two new rows in the failure mode table.
- To review: if your setup has a fixed browser timeout, raise it for deep reasoning members; if you keep a provider list in `LOCAL.md`, note which accounts are prepaid, so a credit error is recognised at once; nothing in your `LOCAL.md` needs to change.

## 1.0.0 (2026-10-05)

- First public version. An orchestrator agent assembles a team of external AIs with roles (researcher, strategist, validator, optional domain expert and creative), sends one fat prompt per member with a fenced findings JSON contract and an end token, runs all members in parallel, parses leniently (fenced block, raw JSON decode, flat shape), merges at field level by the source trust order, and persists everything in one brainstorm state file per topic.
- Transport rule: API by default; a browser only for voice, account-side data, AIs with no API, or a live human conversation. API payloads are built from a file with `jq --rawfile`.
- Browser choice: a per-machine registry of the last browser that worked, written only after a successful select, with the person asked only when the choice is ambiguous.
- Verbatim transcript archiving for browser threads with strategic value, regenerated in full and verified by parse and character count.
- **New convention, recipe and spice:** the general procedure lives in `CURRENT.md`; personal configuration (AIs, accounts, preferred team, presets, browser registry, key variable names) lives in `LOCAL.md`, started from `LOCAL.example.md`. `CURRENT.md` never holds personal values.
- Constitution: state file is canonical memory, drift rule, source trust order, verified browser identifiers only, verbatim archive for strategic threads, the person decides, personal values only in `LOCAL.md`.
- Pitfalls R-001 to R-010, carried over from a skill in daily use since mid 2026.
- To review: copy `LOCAL.example.md` to `LOCAL.md` and fill it in; if you already keep a browser registry or a list of AI accounts elsewhere, point `LOCAL.md` at it instead of duplicating (P12); keep `LOCAL.md` out of anything you share or publish.
