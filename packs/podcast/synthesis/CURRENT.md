---
title: podcast synthesis
date: 2026-10-05
status: active
description: Writes a deep analysis of one published podcast episode from its full transcript and real platform analytics, or works through a back catalogue in prioritized batches one episode at a time; never estimates numbers, never uses parallel agents for the writing, and keeps a tracking matrix and a cross-episode patterns file current.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# synthesis: what an episode said, and how it did

A synthesis is the post-publish memory of an episode: its themes with timecodes, the strongest quotes, the host's own contributions, cold open material, and what the analytics say about who watched and how. Syntheses feed `prep` (callback questions), `title` and `description` (related episodes, series effect) and `channel-intel` (patterns).

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The **whole** transcript is read. Skipping parts is not allowed; it is the only real guarantee of quality.
- Numbers come from the platform's analytics. They are never estimated. Without access, the synthesis says "analytics missing, half done" and contains no invented figures.
- Syntheses are written one at a time, never by parallel agents; parallel writing has produced placeholder-quality output.
- The tracking matrix is updated after each episode; the patterns file at the end of the session.

## Personal settings: LOCAL.md

Show block, where transcripts or subtitle files live and how file names map to episodes, where syntheses, the tracking matrix and the patterns file live, the synthesis template and quality levels (for example by length), how to reach analytics (API or a logged-in browser profile), and which series use a different template. Without `LOCAL.md`, ask for the folders and use the template below.

## When to use

- "Synthesize episode NN", "analyse this episode", "continue the audit", "do the next one".
- Batch mode: "process three episodes from the back catalogue".

## Steps for one episode

### A. Transcript

Find the subtitle file or transcript. Convert it to readable text with a marker every five minutes (`[00:05:00]`), so quotes can be located. Read the **whole** text and take notes: theme blocks with timecodes, the strongest quotes, **the host's own contributions** (not only the questions), cold open material, controversial or surprising claims.

### B. Analytics

From the platform, for the video: views, watch time, subscribers gained, average view duration and percentage; impressions, click-through rate, traffic sources; device, age and gender, geography, subscriber share; and all comments (remove any default filter). If there is no access, write it down and continue with content only.

### C. Write the synthesis

Use the template from `LOCAL.md`, or this one: summary; theme blocks with timecodes; quotes; the host's thoughts; audience and performance with interpretation; what worked and what did not (title, thumbnail, hook); cold open and short-clip candidates; links to related episodes. Optionally run `title`, `thumbnail` and `cold-open` (quick mode) and record a better proposal as "Alternative suggestion".

### D. Patterns file

If the episode confirms or contradicts a general pattern (an audience shift, a topic and view correlation, a hook or intro pattern, a traffic source pattern), note it for the patterns file; write it at the end of the session.

### E. Tracking

Mark the episode done in the tracking matrix, with size and quality level.

## Batch mode

1. Ask how many (two to three deep ones per session is realistic).
2. Propose the order from the tracking matrix: most viewed missing episodes first (most to learn), then thematic groups (better cross-reference). **Get the owner's approval of the list** before starting.
3. Mechanical steps (converting subtitle files to text) can run for all at once.
4. The writing runs one episode at a time, steps A to E each.
5. After each: progress as `done/total (percent)`, and what is next. At the end of the session: the patterns file, a session log, and if interrupted, the phase reached, so the next session can resume.

## Output

The synthesis file, the updated tracking matrix, the patterns file at session end, and one line: `Episode NN synthesis done (<size>, <quality level>), <done>/<total> overall`.

## Pitfalls

- Read the entire transcript; partial reading produces generic theme blocks. <!-- rule:R-001 since:2026-07-28 -->
- Never estimate views or other metrics; take them from analytics or mark the gap. <!-- rule:R-002 since:2026-07-28 -->
- Do not use parallel agents for writing syntheses; they produced placeholders. Mechanical conversion may run in batch. <!-- rule:R-003 since:2026-07-28 -->
- Do not leave out the host's own thoughts; a synthesis that records only the guest misses half the episode. <!-- rule:R-004 since:2026-07-28 -->
- Get the owner's approval of the batch list before processing. <!-- rule:R-005 since:2026-07-28 -->
- Do not hard-code folder paths that may exist twice under different Unicode normalizations (a known issue with accented folder names on macOS); find the folder by a pattern and check it is the non-empty one. <!-- rule:R-006 since:2026-07-28 -->
- A length threshold for quality levels is a tunable heuristic, not a rule; depth is the goal. <!-- rule:R-007 since:2026-08-07 -->
- When the owner corrects a synthesis, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-008 since:2026-10-02 -->
