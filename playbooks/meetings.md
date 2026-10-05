---
title: meetings
status: active
description: Playbook for turning meetings into durable, searchable knowledge in a PAROS vault. Prep note from the vault, recording, checked raw transcript, filing in one home, a structured note with decisions, commitments, open questions and risks, an adversarial second pass, closing the archive with temporary audio, and follow-ups into the task list. Built on the meetings pack.
---

# Playbook: meetings

Meeting knowledge disappears fastest. A week later nobody remembers who promised what, whether a number was decided or guessed, or which risk was mentioned in passing. This playbook adopts the [meetings pack](../packs/meetings/README.md) into your vault and runs it end to end on a real meeting.

## What you get

- **A prep note before the call,** written from what the vault already knows: last meeting, open commitments both ways, open questions, what you want to leave with.
- **A raw transcript** for every recorded meeting, checked for completeness and language, kept unedited as the evidence.
- **One home per meeting,** chosen by a fixed classification (internal, team, client, lead, partner), with every file sharing the same stem `YYYY-MM-DD-<slug>`.
- **A structured note:** decisions with who and status, commitments with owner and date, numbered open questions, risks, exact numbers, transcription uncertainties.
- **A second pass** for anything others will act on: a fresh reviewer tries to break the note against the transcript.
- **Follow-ups** in your task list, each linking back to the note.
- **Audio treated as temporary,** removed only after your confirmation, with no dead links left behind.

## Before you start

| Piece | Status |
|---|---|
| `meeting-prep`, `meeting-intake`, `meeting-archive` skills | exist in the repo: [`packs/meetings/`](../packs/meetings/README.md) |
| `transcribe` skill and its client `transcribe.py` | exists in the repo: [`skills/transcribe/`](../skills/transcribe/SKILL.md) |
| `adversarial-second-pass` skill | exists in the repo: [`skills/adversarial-second-pass/`](../skills/adversarial-second-pass/SKILL.md) |
| Each skill's `LOCAL.md` (recorder folder, areas and meeting folders, where clients and leads live, shared mirrors, confidentiality) | written by the agent with you at adoption, from each `LOCAL.example.md` |
| Thin entries for your platform, `observations/` folders | written by the agent at adoption |
| A transcription glossary per area (misheard names and terms) | started by the agent at the first intake, grows with every meeting |
| A search index | recommended: [`kits/search`](../kits/search/README.md), so a note can be proven findable |

You need: Python 3, `ffmpeg` and `ffprobe` on PATH, and a transcription API key that **you** set up outside the chat (the skill reads it from an environment variable or your secrets folder, never from the vault; P07).

## Steps

1. **Adopt in order.** The agent adopts one skill at a time, each with a short report:
   1. `transcribe`, if you have no transcription path yet;
   2. `meeting-archive`, because it decides where things live and the others depend on that;
   3. `meeting-intake`, then `adversarial-second-pass`;
   4. `meeting-prep` last; it pays off once a few meetings are archived.

   *You decide* whether to adopt all five or only some.

2. **Fill in the `LOCAL.md` files.** The agent asks, one question at a time:
   - where your recorder saves files, and a temporary folder **outside** the vault for copies and cuts;
   - your areas and their meeting folders (lowercase `meetings/`, always);
   - where clients, leads and partners live in your vault;
   - which areas have a shared mirror (a team drive, for example) and which material may never go there;
   - which recordings are too sensitive for an external transcription service;
   - the usual spoken language and a vocabulary hint (names and terms the model gets wrong).

   *You decide* every value. No tokens or passwords in these files.

3. **Check transcription readiness.** The agent runs a dry run, which uploads nothing:
   ```bash
   python transcribe.py "<any short recording>" --dry-run
   ```
   It reports whether the key was found (never its value) and whether ffmpeg is available.

4. **Before the meeting: prep.** Say "prep my meeting with <counterparty> on <date>". `meeting-prep` searches the vault index first, then writes `<stem>.prep.md` next to where the meeting will be archived: purpose and what you want to leave with, what changed since last time, open commitments both ways, questions, sensitivities, a proposed agenda, and a reminder to ask about recording. *You decide* whether to share an agenda; the agent never contacts anyone.

5. **During: record.** Ask the participants before recording; your `LOCAL.md` holds the rule that applies to you. Record into the recorder's folder, not the synced vault. Right after the call, if you have thirty seconds, dump raw impressions as plain text: what surprised you, what you did not say. That goes into the note's "After the meeting" section.

6. **After: transcribe and check.** Say "process the meeting from this afternoon". The agent:
   - finds the recording; a file several hours long is treated as a forgotten recorder, and a file still growing as a recording in progress; neither is processed blindly, both are reported;
   - runs `transcribe` with your language and vocabulary hint:
     ```bash
     python transcribe.py "<recording>" --lang <language> --prompt "<names, terms>" --format txt --download-dir "<temp folder>"
     ```
   - reads the **start and the end** of the transcript against the recording (greeting and goodbye both present, plausible words per minute), and reruns with another model if a passage is missing.

7. **File it.** `meeting-archive` classifies the meeting, resolves its one home folder, and copies the raw transcript there as `<stem>.transcript.txt`, unedited. If the class or folder is ambiguous it asks. *You decide* ambiguous cases; the agent never invents a new counterparty folder.

8. **Write the note.** `meeting-intake` loads the area's state (glossary, the next free decision and question numbers, the last notes), reads the transcript **to the last line**, and writes `<stem>.md`: participants with inferred roles marked, a short summary, decisions (`D-n`, who, what, why, status decided / position / guess), commitments (owner, due date or "no date stated"), numbers exactly as said, open questions (`Q-n`, continuing the area's numbering), risks, a comparison with the prep note, transcription uncertainties, follow-ups, and a change log. Its header says it is an interpretation and the transcript is the source.

9. **Second pass, when it matters.** For money, deadlines, client commitments or people matters, say "run a second pass". A fresh reviewer reads the transcript first, then the note, and looks only for what is missing or wrong. Findings are integrated as review clarifications. *You decide* any change to a committed number or decision.

10. **Close the archive.** `meeting-archive` records in the note's header how the evidence was made (service, model, whether speakers were separated). Then:
    - **audio:** the agent asks whether the source audio can be removed; after your yes the header keeps a line stating it as a fact ("audio removed <date>; the raw transcript is the evidence") instead of a dead link. The recorder's own original is yours to delete, not the agent's;
    - **shared mirror:** if the area has one, the transcript and note go there **only after your yes**; meetings about a person stay in the vault only;
    - **index:** the search index is refreshed and the note is searched for by two or three of its key words.

11. **Follow-ups.** Your commitments become tasks in your task list, each linking to the note; other people's commitments to you become "waiting on" items. *You decide* (default: the list is shown and added after your yes). A follow-up email is a draft; sending is yours.

## Check that it works

Proof, not "the command ran" (P11):

- The meeting's home folder holds `<stem>.transcript.txt` and `<stem>.md` with the **recording** date in the stem.
- The last two lines of the transcript are the last two things said in the meeting.
- A search for two or three distinctive words from the new note returns it (P06). Until it does, the meeting is not archived.
- Every decision in the note has a who and a status; every commitment has an owner and either a date or "no date stated".
- The follow-up tasks exist in your task list and link back to the note.
- If audio was removed, the header says so as a fact, and no link points to a missing file.

## Pitfalls

- **Working from a partial read.** Commitments and deadlines cluster at the end of a meeting. Skipping the last chunk is the most common loss. Read to the last line.
- **A guess recorded as a decision.** "Probably eight, maybe five" written as "decided: eight" is the costliest error. Give every decision a status.
- **Invented names and dates.** An unclear speaker stays a role description or `[?]`; a missing due date is "no date stated".
- **Editing the raw transcript.** Corrections of misheard words go into the note and the glossary, never into the evidence.
- **Two copies of one transcript.** A second copy elsewhere soon makes it impossible to tell which is the source. One home; link to it.
- **Mixed-case folders.** `Meetings/` and `meetings/` are one folder on some systems and two on others. Create lowercase only.
- **Shared mirrors decided by company name.** Check the mirror rule per area and per meeting class; material about a person or owned by a client never goes to a store others can read.
- **Forgotten or running recorders.** Hours-long files and still-growing files are reported, never processed blindly, and never deleted by the agent.
- **A weak model.** Mistakes in a note compound, because the next session reads the note as truth. Use a strong model for intake.
- **Instructions in the recording.** "Let's send this to everyone" becomes an action item in the note. It is never executed.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): sending, deleting audio and writing to shared drives need your yes.
- [P01](../principles/P01-persistence.md): the raw transcript is evidence; the note is markdown.
- [P04](../principles/P04-thin-entry-live-definition.md): thin entries, live definitions, your settings in `LOCAL.md`.
- [P05](../principles/P05-closed-loop-learning.md): every correction of a note, a class or an audio decision becomes a learning packet.
- [P06](../principles/P06-search.md): index first for prep; a note is done only when it is findable.
- [P09](../principles/P09-forgetting-and-archiving.md): fade and archive; temporary audio is the exception.
- [P11](../principles/P11-health-contract.md): completeness check and the search proof.
- [P12](../principles/P12-one-fact-one-owner.md): one transcript, one home.

## Related

- Pack: [`packs/meetings`](../packs/meetings/README.md) (`meeting-prep`, `meeting-intake`, `meeting-archive`).
- Skills: [`skills/transcribe`](../skills/transcribe/SKILL.md), [`skills/adversarial-second-pass`](../skills/adversarial-second-pass/SKILL.md), [`skills/project-state`](../skills/project-state/) (decisions feed the area state).
- Agent: [`agents/alfred`](../agents/alfred/CURRENT.md) (follow-ups and "Prepare" in the briefing).
- Kits: [`kits/search`](../kits/search/README.md), [`kits/health`](../kits/health/README.md).
- Playbooks: [`daily-briefing`](daily-briefing.md), `transcribe`, `unified-calendar`.
