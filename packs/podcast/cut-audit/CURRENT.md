---
title: podcast cut-audit
date: 2026-10-05
status: active
description: Audits a raw podcast recording before the editor cuts it, or checks whether an uploaded video was cut at all; checks promise consistency, separates real redundancy from deliberate callbacks, measures every silence and cut point instead of trusting the transcript, saves the transcript as evidence, and hands the editor a prioritized brief.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# cut-audit: from the raw recording to the editor's brief

An audit of a long recording is easy to write and easy to get wrong. The first version of this procedure estimated five to six minutes of removable repetition; a re-check against a fresh transcript found one to two. Every claim it made about silence and broken sentences failed. This skill exists so that each claim in a brief can be checked by someone else.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The transcript the audit rests on is saved next to the audit. An audit whose evidence is gone cannot be trusted.
- Every cut suggestion quotes both places it concerns, with timecodes.
- A timecode from speech recognition is never a cut point until it has been measured on the audio.
- The brief is advice to the editor; the owner decides what is sent.

## Personal settings: LOCAL.md

Show block, the episode folder pattern, where transcripts go, the editor's name and preferred hand-off channel, and the priority labels the editor is used to. Without `LOCAL.md`, use the defaults below.

## When to use

- A recording is done and the editor has not started.
- The owner asks "was this upload actually cut?" or "what can we cut?".
- Before `cold-open`, to collect candidates.

## Steps

### 0. Transcript, and save it

Transcribe with the `transcribe` skill (SRT, completeness check included). Save it in the episode folder (`<episode>/transcript/`) before writing a single claim.

### 1. Is it already cut? (when an upload exists)

Compare the uploaded video's duration with the raw recording's (`ffprobe`). A match within a second or two is suspicious. Then compare the transcript at three to five sample points (start, middle, end, and where a cut was expected). Matching length and matching samples mean the raw recording is what was uploaded.

### 2. Promise consistency

Every number spoken on the recording ("seven habits", "twenty tips") is checked against what is actually there. A transition between blocks ("the next few are about money") is not an item. If the count is off, there are two fixes: cut the number in the audio, or give the unnamed items a spoken title and an on-screen card.

### 3. Redundancy: a callback is not a duplicate

- A **spoken callback** ("remember, in the last tip I told you...") is deliberate. Do not cut it.
- The same story told twice is not a duplicate when it proves a different point, or when the second telling goes further.
- A rhetorical frame (claim, example, the claim again) may stay even when it repeats nearly word for word.
- Each suggestion: a quote from both places with timecodes, and one sentence on why it is not a callback.

### 4. Technical cut points: only measured

- **Silence** only by measurement: `ffmpeg -i <audio> -af silencedetect=noise=-30dB:d=1.0 -f null -`, cross-checked with the gaps in the transcript.
- **"Unfinished sentence"** only by listening to the audio and reading the transcript together. A sharp change of subject is not a broken sentence; it needs a bridge, not a rescue.
- Every concrete cut timecode is checked on the waveform the way `cold-open` does it (step 5 there).

### 5. Cold open and short-clip candidates

List only; the work is done in `cold-open`. For each short-clip candidate: timecode, one-sentence thesis, length.

### 6. The brief

`EDITOR_BRIEF.md` in the episode folder, in this order:

1. Pickups that must be recorded.
2. Numbering and on-screen cards.
3. Cuts in a priority table: `Must`, `Strongly suggested`, `Consider`, with timecode and action.
4. Cold open candidates.
5. Short-clip candidates.
6. Subtitle notes (misheard names, deliberate ambiguities).
7. If an earlier audit exists: "What the earlier audit got wrong".

Then the same brief as a **paste-ready plain-text block** in the chat for the editor.

## Output

- The saved transcript, the brief in the vault, the paste-ready block in the chat.
- One line: estimated removable time, and how many claims rest on measurement versus reading.

## Pitfalls

- Save the transcript the audit is based on; an earlier audit's evidence was lost and all four of its checked claims later failed. <!-- rule:R-001 since:2026-09-07 -->
- A spoken callback is not a duplicate; an unchecked audit overestimated removable time about three to five times. <!-- rule:R-002 since:2026-09-07 -->
- Never claim silence without measuring it; a reported multi-second silence did not exist in any measurement. <!-- rule:R-003 since:2026-09-07 -->
- Count promised items strictly; a transition sentence is not an item. <!-- rule:R-004 since:2026-09-07 -->
- A "broken sentence" claim needs audio and transcript together; the one reported had in fact finished. <!-- rule:R-005 since:2026-09-07 -->
- "Uploaded" does not mean "cut": test duration and sample transcripts against the raw recording. <!-- rule:R-006 since:2026-10-02 -->
- Give the editor a paste-ready block, not only a vault file. <!-- rule:R-007 since:2026-09-07 -->
- When the owner or the editor corrects the brief, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-008 since:2026-10-02 -->
