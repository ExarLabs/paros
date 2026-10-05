---
title: meeting-archive
date: 2026-10-05
status: active
description: Decides where a meeting belongs (internal, team, client, lead or partner), picks the right recording, files the raw transcript and the note under one stem in one home, treats the source audio as temporary, mirrors to a shared folder only with a yes, and proves the note is findable in the index.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# meeting-archive

A meeting leaves a trail only if it lands in the right place, under a predictable name, with the evidence kept and the bulk thrown away. This skill owns that: classification, naming, filing, the audio, the optional shared mirror and the index. It runs twice: a **file** phase before the note is written, and a **close** phase after it (and after the adversarial pass, if one runs). The note's content belongs to `meeting-intake`; the text comes from `transcribe`.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The raw transcript and the processed note are the durable artefacts and the evidence. The raw transcript is never edited.
- Source audio is temporary. It is deleted only after the transcript has been checked and the person has confirmed. The recorder's own original is never deleted by the agent.
- One meeting, one home. Other areas link to it; nobody copies the transcript.
- Writing to a shared or external store (a team drive, a CRM, a shared folder) needs the person's yes, every time.
- A meeting about a person (hiring, pay, performance, suitability) is never mirrored to a shared store.
- When the classification is unclear, ask. Never invent a new client, lead or partner folder.

## Personal settings: LOCAL.md

Read `LOCAL.md` next to this file before every run. It names: where the recorder saves files, the temporary folder, the areas with their meeting folders, where clients, leads and partners live, which areas have a shared mirror and where, which material is confidential (for the transcription service and for the mirror), the naming slug style, and how to refresh the search index. Without `LOCAL.md`: ask for the home folder, no mirror, audio in the system temp folder.

## When to use

- "Archive this meeting", "where should this meeting go", "save the transcript", "file this recording", "clean up the meeting audio".
- As the file phase right after `transcribe`, and as the close phase after `meeting-intake` (and `adversarial-second-pass`).

## Classification: five meeting classes

Every meeting has exactly **one** home in the vault and **at most one** mirror. Two questions decide it: was anyone from outside in the call, and if not, what was the main subject?

| Class | When | Home |
|---|---|---|
| **internal** | only your own people, and the subject is the area's work | `<area>/meetings/` |
| **team** | only your own people, and the subject is the team itself: roles, culture, capacity, morale, growth | `<area>/<unit>/team/meetings/` |
| **client** | a live client with an agreement | `<clients>/<client>/meetings/` |
| **lead** | not a client yet, someone you are courting | `<leads>/<lead>/meetings/` |
| **partner** | outside, but not a buyer: supplier, authority, agency, recruiter | `<partners>/<partner>/meetings/` |

**Who is outside?** Clients, leads and partners. A **candidate** (a future colleague, volunteer, trainer or subcontractor without an agreement yet) does **not** make a meeting external, and is not a partner either. If the subject is the area's work (planning, a course, a product), the meeting is internal. If the subject is the candidate (hiring, pay, suitability), it is about a person: it stays in the vault only, is not mirrored, and the report says why.

The same name can exist under two relationships (a lead for one of your activities, a client for another). Then ask which relationship the call was about. A meeting that is both a client call and a practice topic goes where the larger part belongs; the other place links to it.

If your vault has a routing script, run it in dry-run mode first and check that its answer matches yours. A resolver that stops on an unknown or ambiguous name is doing its job: ask, do not guess.

## Naming

All artefacts share one stem: `YYYY-MM-DD-<slug>`. The date is the **recording** date, not the processing date. The slug is short, lowercase, hyphenated, without accents.

| Artefact | Where | Lifetime |
|---|---|---|
| `<stem>.transcript.txt` (raw transcript) | home folder | durable, never edited |
| `<stem>.md` (processed note) | home folder | durable |
| `<stem>.prep.md` (prep note) | home folder | durable, may fade |
| `<stem>.review.json` (adversarial findings, optional) | home folder | durable |
| `<stem>.<audio ext>` | temporary folder, not the vault | temporary |

The meetings folder is always lowercase `meetings/`. On some systems `Meetings/` and `meetings/` are the same folder and on others they are two; a vault synced across machines must not depend on that. Respect an existing folder, but create new ones in lowercase.

## Steps

### File phase (before the note)

1. **Pick the recording.** If the person did not name a file, list the newest files in the recorder folder with length (`ffprobe -v error -show_entries format=duration -of default=nw=1 <file>`) and start time, and propose the one that matches the meeting. Watch for two traps:
   - a file far longer than any meeting (several hours) is almost certainly a recorder left running; do not transcribe it first; if the meeting falls inside it, cut that span (`ffmpeg -ss <start> -to <end> -i <file> -c copy <cut>`) instead of transcribing hours;
   - a file whose size or modification time is still changing is a recording in progress; do not touch it.
   Report both; deleting them is the person's decision.
2. **Transcribe** with [`transcribe`](../../../skills/transcribe/), including its completeness and language checks. Check `LOCAL.md` first: confidential material may need a private backend or a yes.
3. **Read the whole transcript** once, enough to classify. Who was there, and what was the main subject?
4. **Classify** using the table above, then resolve the home folder (or the routing script in dry-run). If it is ambiguous or unknown, ask.
5. **File the raw transcript** in the home folder under the stem, unchanged. If the vault keeps a meetings index for the area, add a row: date, title, transcript, note (to be filled).

Then `meeting-intake` writes the note, and `adversarial-second-pass` checks it if the stakes call for it.

### Close phase (after the note)

6. **Header facts.** Check that the note's header names the raw transcript, the length, the transcription service and model, whether speaker labels existed, and where the audio is. Add `meeting_class` and `area` or `counterparty` to the frontmatter, so the classification is searchable, not only implied by the folder.
7. **Audio.** If the audio was copied to a temporary folder or the vault, propose deleting it now that the transcript is checked and the note reviewed. After the person confirms, delete it and turn the header's audio line into a fact: "audio deleted <date>, the evidence is the raw transcript". No dead link. For a confidential or legally contestable meeting, ask explicitly before deleting. If the original is still in the recorder folder, do not copy it anywhere; the header records its file name and folder, and the report says it is processed.
8. **Mirror (optional).** If `LOCAL.md` gives this area a shared mirror and the meeting is not about a person and not confidential, propose uploading the raw transcript and the note to it, and do it only after a yes. An upload that replaces a same-named file is preferred over creating duplicates. Record the mirror location in the note's frontmatter (`mirror: <location>` or `mirror: none, <reason>`).
9. **Index and proof.** Refresh the search index the way `LOCAL.md` says, then search two or three distinctive words from the note and show that the note comes back (P06, P11). If it does not, find out why before reporting done.
10. **Report.** Class and home, the files written, the mirror (done, declined, or not applicable and why), the audio (deleted, waiting for confirmation, or kept where the recorder keeps it), any forgotten or running recording found, and what waits for the person.

## Output

- The raw transcript and the note in one home folder, under one stem, with the classification in the frontmatter.
- Optionally the review result and the prep note next to them.
- The report above.

## Pitfalls

- A candidate's presence does not make a meeting external; classify by who is outside and by the main subject. <!-- rule:R-001 since:2026-10-02 -->
- A meeting about a person stays in the vault only, even when the area has a shared mirror. <!-- rule:R-002 since:2026-10-02 -->
- The durable artefacts are the raw transcript and the processed note; the source audio is temporary and may be deleted once the transcript is verified and the person confirms. <!-- rule:R-003 since:2026-09-09 -->
- When audio is deleted, keep its header line as a fact instead of a dead link. <!-- rule:R-004 since:2026-09-09 -->
- Do not copy audio into the vault when the recorder keeps the original; record its file name and folder instead, and never delete the recorder's original yourself. <!-- rule:R-005 since:2026-10-02 -->
- A recording several hours long is a forgotten recorder, and a growing file is a recording in progress; do not process either blindly, and report both. <!-- rule:R-006 since:2026-10-02 -->
- One transcript, one home; a second copy elsewhere soon makes it impossible to tell which is the source. <!-- rule:R-007 since:2026-08-25 -->
- Material a client owns does not go to a store shared with people outside that relationship; check the mirror rule per area, not per company name. <!-- rule:R-008 since:2026-08-25 -->
- Create meeting folders in lowercase; mixed case splits into two folders on case-sensitive systems. <!-- rule:R-009 since:2026-08-25 -->
- When a resolver or the classification is ambiguous, ask; never invent a new counterparty folder. <!-- rule:R-010 since:2026-08-25 -->
- The date in the stem is the recording date, not the processing date. <!-- rule:R-011 since:2026-08-25 -->
- A note is not archived until a search for it returns it. <!-- rule:R-012 since:2026-06-10 -->
- When the person corrects a classification, a location or an audio decision, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-013 since:2026-10-02 -->
