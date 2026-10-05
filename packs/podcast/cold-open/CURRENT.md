---
title: podcast cold-open
date: 2026-10-05
status: active
description: Finds and produces the cold open of a podcast episode; a quick mode gives hook ideas from the transcript, the full mode delivers a cut-ready teaser with a blocklist settled first, a thesis variant, waveform-verified cut points, re-transcribed clips, audio previews and a paste-ready block for the editor, including the transition after the cold open.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# cold-open: from hook ideas to a cut-ready teaser

The first thirty seconds of a long video decide whether anyone stays. A cold open is a few of the guest's strongest sentences placed before the music and the titles. Finding them is half the job. The other half is making sure the editor gets cut points that do not slice a word, and text that matches what the clip actually says.

Two failures happen almost every time someone works naively from a transcript. Both happened in production before this procedure existed:

1. **A speech-recognition timecode is not a cut point.** The model splits continuous speech arbitrarily. In one measured episode, four of six boundaries fell in the middle of speech; the worst sat 870 ms before the end of a sentence and would have cut off its last word, the punchline.
2. **A shortened clip does not say what the transcript shows.** A clip trimmed to nine seconds started one word too late and lost a negation. The transcript showed a full sentence; the clip said the opposite.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- Hook text is quoted word for word from the recording, never paraphrased.
- The blocklist (what may not appear in the teaser) is settled at the start, not at the end.
- Every cut point is verified on the waveform, and every rendered clip is transcribed again; the editor's sheet carries the re-transcribed text.
- If the opening uses the guest's sensitive personal material (health, family, children), the guest agrees before the editor starts. Consent to the recording is not consent to a sentence becoming the face of the episode.
- The owner chooses the variant, by ear. Nothing goes to the editor without the owner's yes.

## Personal settings: LOCAL.md

Show block, the working folder for rendered audio (outside the synced vault), the episode folder pattern, the editor's hand-off channel, the target cold-open length, the hook types that work for this audience (from channel intelligence), and the tool used to send audio files to the owner. Without `LOCAL.md`: 25 to 50 seconds, rendered audio in the system temp folder.

## When to use

- **Quick mode:** "give me hook ideas", "what could open this episode?" Steps 2 and 3 only, text output, no verification. Say clearly that the result is not cut-ready.
- **Full mode:** "make the cold open", "prepare the teaser for the editor". All steps.

## Steps

### 0. Prerequisites

- The episode audio in one file. Know which file's zero is the reference: if the editor's timeline starts elsewhere, every timecode needs an offset, and the sheet says so.
- Read the show block in `LOCAL.md` and the channel intelligence file if one exists.
- **Ask for the blocklist:** topics, people or scenes that may not appear (a guest's child, health data, a third party, an employer). If there is no answer, flag suspicious material in step 2 and ask before building on it.

### 1. Transcript

`transcribe` with SRT output, the guest's name and key terms as the vocabulary hint, completeness checked (starts near zero, reaches the end, no gap over 20 seconds). Saved in the episode folder.

### 2. Hook pool: ten candidates

Read the **whole** transcript, do not just search it. Ten candidates in descending score (out of 100), each with: score and hook type, start and end time, estimated length, the verbatim text.

What to look for:

- **Personal confession or story** of the guest or the host; usually the strongest type.
- **Myth-busting**: a claim against common belief.
- **A striking number.**
- **Universal recognition**: a problem the viewer nods at. Strong openings rarely start in the professional frame of the topic; they start with the human stake.
- **Open loop**: the hook raises a question the episode answers. Check that the answer does not come a few seconds later.
- **Shareability**: not "would they like it" but "who would they send it to".

Only self-contained passages, or ones that end on a strong question or claim. If a sentence breaks off, find the end of the thought.

### 3. Variants: at least five stacks

Build at least five stacks with different arcs (A, B, C, ...), each two to four clips. A stack is a dramatic arc, not the best hooks in a pile. For each: the arc in one sentence, per clip time, length, verbatim text and role in the arc, and a score from 1 to 10 with a real spread. If every variant scores 8, the scoring is worthless; say what pulls each one down.

Number shared clips once (C1, C2, ...) and let variants reference them.

**The thesis rule.** At least one variant states the **point of the episode**, not an anecdote. Look for the definition of the topic, the stake, the consequence, and myth-busting; these usually sit in the first five to ten minutes and in the close. A good thesis variant tells the viewer in three sentences why the whole episode is worth watching.

**Risk spread.** If the favourite rests on sensitive personal material, prepare at least one variant that is completely independent of it, marked as the fallback.

Check every variant:

- No repeated beat: two clips with the same structure on the same subject sound like repetition, not escalation.
- The guest speaks, not the host. A long host monologue is a weak opening.
- Promise matches content. A beautiful clip from a side thread makes the wrong promise; set it aside as a short clip.

### 4. The owner chooses: audio and text together

Deliver: a table of all variants sorted by score; for each the arc, who it is for and what pulls it down; one clear recommendation and why; **rendered audio of the best two or three**, sent so the owner can listen immediately; and any variant better suited elsewhere (short clip, pinned comment, end screen). No variant is marked accepted until the owner says so.

### 5. Verify every cut point (mandatory)

Measure the audio energy around each in and out point in short windows (about 25 ms RMS), relative to the quiet floor of the surrounding seconds:

- If the level at the point is well above the floor (as a rule of thumb, above about 12 % of the local peak), you are in speech. Move.
- List the pauses nearby. A tool cannot reliably tell a breath between words from the pause at a sentence end; choose deliberately, usually the longer pause is the sentence boundary.
- If no pause is found, raise the sensitivity and look again.

Render the clips and the stack from the verified points. A small script that does this measurement is worth writing once and keeping in this skill's folder.

### 6. Re-transcribe every rendered clip (mandatory)

Transcribe each rendered clip on its own. The editor's sheet carries **that** text. If it is not a whole sentence, the cut point is wrong: back to step 5.

### 7. Hand-over: two forms, both mandatory

**a. Editor's sheet in the vault** (`EDITOR SHEET - <variant> (ACCEPTED).md` in the episode folder), complete enough that the editor opens nothing else: source file name and length with the zero point and offset warning; per clip IN, OUT and length, as `HH:MM:SS,mmm` and in seconds; the re-transcribed text; subtitle uncertainties; cut instructions (order, hard cut or fade, where music starts); a **What must not be cut in** section (where the open loop would resolve too early, the blocklist); what the verification found; where the reference audio is.

**b. Transition after the cold open.** The end of the cold open is not the end of the job. On one measured episode, most viewers were still there at the end of the cold open, and roughly half of them left during the next seventy seconds of music, titles and host introduction. The sheet therefore also covers that stretch: keep the host introduction to **30 to 40 seconds at most**, do not repeat what the cold open said, carry the open loop straight into the conversation, keep music and titles short. **Low evidence: this limit comes from one retention curve.** Check it against your own curves and record what you find.

**c. Paste-ready block in the chat.** The owner talks to the editor in messages, not vault files. Give a plain-text, fixed-width, ASCII-ruled block (not a markdown table, which breaks elsewhere):

```
EPISODE <n> - COLD OPEN - CUT INSTRUCTIONS

SOURCE FILE: <name>  (length <HH:MM:SS,mmm>)
WARNING: all timecodes are measured from the zero point of THIS file.
If your timeline starts elsewhere, add the offset to every value.

TOTAL: <x.y> s, <n> clips, HARD CUT (no fade, no crossfade)

==================================================================
CLIP 1
IN:     <HH:MM:SS,mmm>   (<seconds> s)
OUT:    <HH:MM:SS,mmm>   (<seconds> s)
LENGTH: <x.y> s
TEXT:
"<re-transcribed, verbatim>"

==================================================================
ORDER: CLIP 1 > CLIP 2 > CLIP 3
<if not chronological, say it is intended>

==================================================================
TRANSITION
- Music and titles: <length>
- Host introduction: at most 30-40 s, IN <time> OUT <time>
- <what can be cut from it because it repeats the cold open>

==================================================================
DO NOT CUT IN
- <what follows the clips and must stay out, and why>
- <blocklist>

==================================================================
SUBTITLES
- <corrected spellings of misheard words>
- <deliberate ambiguities, so they are not "fixed">

==================================================================
REFERENCE AUDIO: <file> (<length>), this is how it should sound
```

After the block, one or two sentences on what was verified, and the final stack audio.

### 8. Close

- The accepted file gets `(ACCEPTED)` in its name; the episode's improvements index is updated.
- Set-aside variants are labelled as short-clip candidates, not lost.
- If the opening uses the guest's sensitive material, ask the guest and wait **before** the editor starts. If the guest says no, do not patch the stack clip by clip: if the arc rested on that material, the arc is gone. Go back to step 2. (The forced rebuild that taught this produced a better, thesis-based opening.)

## Output contract

| Step | What the owner gets |
|---|---|
| 2 | Ten candidates with scores and verbatim text |
| 4 | Variant table, a recommendation, and audio of the best two or three |
| 7 | Editor's sheet in the vault, the paste-ready block in the chat, the final stack audio |

If audio is missing from any row, the work is not done.

## Pitfalls

- Settle the blocklist at the start; a guest's late objection once forced a rebuild of a finished, verified stack. <!-- rule:R-001 since:2026-07-28 -->
- Never hand over a speech-recognition timecode as a cut point; verify it on the waveform. <!-- rule:R-002 since:2026-07-28 -->
- Re-transcribe every rendered clip and put that text on the sheet; a trimmed clip once lost its negation. <!-- rule:R-003 since:2026-07-28 -->
- At least one variant states the episode's thesis, not an anecdote. <!-- rule:R-004 since:2026-07-28 -->
- If the favourite rests on sensitive personal material, prepare an independent fallback; when the top four candidates come from the same two minutes, the stack is fragile. <!-- rule:R-005 since:2026-07-28 -->
- Get the guest's agreement before the cut, not before publishing. <!-- rule:R-006 since:2026-07-28 -->
- The owner decides by ear: no variant table without rendered audio of the best ones. <!-- rule:R-007 since:2026-07-28 -->
- The real hand-over is the paste-ready plain-text block, and its offset warning is never dropped. <!-- rule:R-008 since:2026-07-28 -->
- Build the hook pool on what was actually said; planned "wow points" from the prep note often never happen. <!-- rule:R-009 since:2026-07-28 -->
- Two clips with the same structure on the same subject sound like repetition, not escalation. <!-- rule:R-010 since:2026-07-28 -->
- Pause detection measured against a local peak is window-dependent and jumped to wrong points; measure against the quiet floor, and leave the final choice to a person. <!-- rule:R-011 since:2026-07-28 -->
- "The longer pause is the sentence end" fails for speakers who pause mid-sentence when moved; listen at emotional passages. <!-- rule:R-012 since:2026-07-28 evidence:low -->
- Cover the transition after the cold open: host introduction at most 30 to 40 seconds. Low evidence, from one retention curve; revisit with more curves. <!-- rule:R-013 since:2026-10-02 evidence:low -->
- When the owner corrects a variant, a cut or the sheet, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-014 since:2026-10-02 -->
