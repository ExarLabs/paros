---
title: meetings pack
date: 2026-10-05
status: active
description: A pack of three skills (meeting-prep, meeting-intake, meeting-archive) that, together with the transcribe and adversarial-second-pass skills, turn a meeting into durable, searchable, attributed knowledge: prepared beforehand, recorded, transcribed, structured into decisions, commitments, open questions and risks, checked, archived, and fed into the task list.
version: 1.0.0
---

# Meetings pack

Meeting knowledge is the fastest knowledge to disappear. A week later nobody remembers who promised what, whether a number was a decision or a guess, or which risk somebody mentioned in passing. This pack is a complete, tested way to keep it: from the prep note before the call to the follow-ups in your task list after it.

A pack is a set of skills that work together. Each skill in it is adopted like any other PAROS skill ([`skills/README.md`](../../skills/README.md), "How a skill becomes yours"): it lives in your vault, learns from your corrections, and gets updates from here as advice. You can adopt one skill without the others.

## What is in the pack

| Skill | What it does | Lives in this pack |
|---|---|---|
| [`meeting-prep`](meeting-prep/) | Writes a short prep note from what the vault already knows: last meeting, open commitments both ways, open questions, what you want out of this one | yes |
| [`transcribe`](../../skills/transcribe/) | Recording to raw transcript, with a completeness and a language check | no, a shared skill; this pack only calls it |
| [`meeting-intake`](meeting-intake/) | Raw transcript to a structured note: decisions, commitments with owner and date, open questions, risks, numbers, follow-ups | yes |
| [`adversarial-second-pass`](../../skills/adversarial-second-pass/) | A fresh-eyes reviewer rereads the transcript and tries to break the note | no, a shared skill; this pack only calls it |
| [`meeting-archive`](meeting-archive/) | Decides where the meeting belongs, names and files the evidence, handles the audio, an optional shared mirror and the index | yes |

## The workflow

```
before            during          after
meeting-prep  ->  record      ->  transcribe -> meeting-archive (file) -> meeting-intake
                                   -> adversarial-second-pass -> meeting-archive (close)
                                   -> follow-ups into the task list
```

### 1. Before the meeting: prep note from the vault

`meeting-prep` searches the vault (index first, P06) for everything that already exists about this meeting's area or counterparty: the previous meeting notes, commitments still open on both sides, open questions, recent decisions, the area's state file. It writes a one-page prep note next to where the meeting will be archived: purpose, what you want to leave with, what changed since last time, open commitments, questions to ask, sensitivities, a proposed agenda, and a recording reminder. It never contacts anyone; sending an agenda is your decision.

### 2. Recording

Ask the participants before you record; the prep note reminds you, and your `LOCAL.md` says what your local rules require. Record the audio into the recorder's own folder or a temporary folder, **not** into the synced vault. Two things go wrong often enough to check every time: a recorder left running for hours (a file far longer than the meeting), and a recording that is still running (a file that is still growing). Neither is processed blindly.

Right after the call, if you have thirty seconds, dump your impressions as raw text: what surprised you, what you did not say, what you suspect. No structure. It goes into the note's "After the meeting" section later and is often the most valuable line in it.

### 3. Transcription

[`transcribe`](../../skills/transcribe/) produces the **raw transcript**: exactly what the model returned, checked for completeness (start and end match the recording, words per minute plausible) and language. Most transcription services do not separate speakers; then every speaker attribution in the note is inferred and marked as such.

### 4. Filing: where does this meeting live?

`meeting-archive` classifies the meeting (internal, team, client, lead or partner; see the skill), resolves its one home folder, gives every artefact the same stem `YYYY-MM-DD-<slug>` (the recording date), and files the raw transcript there, unedited.

### 5. Intake: the structured note

`meeting-intake` reads the whole transcript, start to end, and writes the processed note next to it:

- **Decisions**, numbered, with who decided, what, why, and whether it was really decided or only a position or a guess.
- **Commitments**, with owner and due date; "no date stated" when none was said, never an invented one.
- **Open questions**, numbered, continuing the area's own numbering.
- **Risks**, including the ones nobody called a risk.
- **Numbers and facts**, exactly as said, with uncertain ones marked.
- **Transcription uncertainties**: misheard names and terms, and how they were resolved.

### 6. Adversarial second pass

For anything others will act on (money, deadlines, commitments to a client, people matters), run [`adversarial-second-pass`](../../skills/adversarial-second-pass/) on the note against the raw transcript. A fresh reviewer reads the transcript first, then the note, and looks only for what is missing or wrong. In practice, most corrections and most unnamed risks come from this step, at a fraction of the cost of the first pass. Findings are integrated into the note as review clarifications; committed numbers and decisions change only with your yes.

### 7. Closing the archive

`meeting-archive` finishes the job: the note's header records how the evidence was made; the source audio is deleted once you confirm (or kept only where the recorder keeps it); if the area has a shared mirror (a team drive, for example), the transcript and the note go there **only after your yes**; the search index is refreshed and the new note is proven findable (P11).

### 8. Follow-ups into the task list

Your own commitments become tasks in your vault's task list, each linking back to the note. Other people's commitments to you become "waiting on" items. The default is to show the list and add it after your yes; `LOCAL.md` can allow adding without asking. Nothing is ever sent to the other participants by this pack; a follow-up email is a draft for you.

## What is evidence, what is temporary

| Artefact | Status | Why |
|---|---|---|
| Raw transcript (`<stem>.transcript.txt` or `<stem>.raw.md`) | **Durable evidence.** Never edited. | The only thing anyone can check a claim against. Your summary is lossy and your speaker attribution is inferred. |
| Processed note (`<stem>.md`) | **Durable.** Interpretation, and says so in its header. | What people read and search. Corrections of mishearings go here, never into the raw transcript. |
| Adversarial review result (JSON or section) | Durable, next to the note, if your vault keeps them. | Shows what was corrected and on what evidence. |
| Prep note (`<stem>.prep.md`) | Durable but minor; may fade (P09). | Shows what you went in with; the intake compares it with what came out. |
| Source audio or video | **Temporary.** | Large, and its job is done once the raw transcript is checked. Deleted after your confirmation; the note header then says so as a fact, so no dead link is left. Ask before deleting audio of a confidential or legally contestable meeting. |
| The recorder's own original | Not yours to delete. | The agent may say it is processed and could be removed; you decide. |

## Order of adoption

1. `transcribe` first, if you do not have a transcription path yet.
2. `meeting-archive`: it decides where things live, and the others depend on that.
3. `meeting-intake`, then `adversarial-second-pass` for high-stakes meetings.
4. `meeting-prep` last: it pays off once there are a few archived meetings to prepare from.

## Principles behind the pack

P01 (knowledge in markdown, the raw transcript as evidence), P04 (thin entry, live definition, `LOCAL.md` for your settings), P05 (every correction becomes a learning packet), P06 (index first; a note is not done until it is findable), P09 (fade and archive; temporary media is the exception), P11 (no "done" without proof), P12 (one transcript, one home), P00 (sending, publishing, deleting and writing to shared systems need your yes).
