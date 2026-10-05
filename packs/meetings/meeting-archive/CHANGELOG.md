# Changelog: meeting-archive

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.0.0 (2026-10-05)

- First public version, part of the meetings pack. Five meeting classes (internal, team, client, lead, partner) with exactly one home each; one stem per meeting (`YYYY-MM-DD-<slug>`, recording date); a file phase (pick the recording, transcribe, classify, file the raw transcript) and a close phase (header facts, audio, optional mirror, index proof).
- Evidence rule: the raw transcript and the processed note are durable; the source audio is temporary and is deleted after the transcript is verified and the person confirms, leaving a factual header line instead of a dead link.
- Learned rules carried over: a candidate's presence does not make a meeting external; a meeting about a person is never mirrored; a recording hours long is a forgotten recorder and a growing file is a recording in progress; one transcript, one home; lowercase meeting folders.
- Generalized from a meeting archive skill in daily use since mid 2026; company folders, shared drives and the routing script moved to `LOCAL.md`.
- Constitution: transcript never edited, audio temporary, one home, every write to a shared store needs a yes, people meetings never mirrored, ask instead of inventing a counterparty folder.
- Pitfalls R-001 to R-013.
- To review: copy `LOCAL.example.md` to `LOCAL.md`; list your areas and where clients, leads and partners live; decide which areas have a shared mirror and what never goes there; move any meeting audio stored in the vault to a temporary folder once its transcript is checked.
