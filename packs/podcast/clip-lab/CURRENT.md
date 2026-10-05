---
title: podcast clip-lab
date: 2026-10-05
status: active
description: Builds a private web page of 30 to 50 sentence clips cut from an episode's audio, so the host can listen, select, reorder by drag and drop, nudge cuts to word boundaries and export an intro sequence with exact timecodes for the editor; clips are anchored on verbatim phrases from a word-level transcript, with the end anchor searched only after the start.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# clip-lab: build the intro by ear

The alternative is scrubbing a 75-minute timeline in an editing program to find the six sentences that make the intro. The clip lab shows those candidate sentences as cards with a waveform. The host listens, ticks, drags them into order, moves a cut a word earlier or later, and copies the finished sequence with exact timecodes. That text goes to the editor.

This skill is the selection-by-ear sibling of `cold-open`. Use `cold-open` when you want the skill to propose and verify a teaser; use the clip lab when the host wants to compose the intro personally from a wide pool.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The page is for the host only. It is never sent to the guest and never listed anywhere public; it lives at an unguessable address.
- Clip anchors are verbatim phrases from the same word-level transcript the clips are cut from.
- The selection is a proposal: a subset is pre-selected, never all of it.
- Generator scripts live in the vault, next to this definition, not in a deploy working copy.

## Personal settings: LOCAL.md

Show block, the hosting and deploy route, the URL pattern and slug length, the shared editor files and their current version numbers, the low-quality audio settings, where raw audio usually comes from (and how to download it), the model to use for selection, and the export format the editor prefers. Without `LOCAL.md`, build a local page and do not deploy.

## When to use

The recording is done, raw audio exists, and the task is to put the intro together. Not before recording (that is `prep`), not for the published chapters (that is `chapters`).

## Data

- `clips.json`: episode, title, source note, and a list of clips: `id` (`<theme-slug>-<n>`, stable under reordering), `theme`, `speaker` (always filled; the editor picks the camera by it), `in`, `out` (seconds, millisecond precision), `checked` (your proposal), `text` (cleaned, readable) and `words` (raw recognition with word times).
- The `words` list **starts four seconds before the cut and ends four seconds after**. This padding lets the host move a cut onto a neighbouring word without regenerating anything.
- Per-clip waveform peaks over the **padded** range, and one overview waveform of the whole episode.
- A low-quality mono audio file of the episode (for example `ffmpeg -i <raw> -ac 1 -ar 22050 -b:a 24k episode-lofi.mp3`); a phone can load 13 MB, not 90.

## What the shared page does

Cards by theme, playable with waveform; drag-and-drop order; word-boundary nudging of in and out; a live total; **copy for the editor** (a header, then per line `NN · HH:MM:SS.mmm > HH:MM:SS.mmm (X.X s) · Speaker` and the quoted text); a shareable state in the URL (no server); local storage under a per-episode key.

## Steps

0. **Get the raw audio.** If it sits in a link-shared cloud folder, a connector may not list it; fetch by file ID with a downloader that handles the provider's confirmation page. **The file name is not the episode ID** (editors name exports by their own order): compare the duration with the transcript's last timestamp before building on it.
1. **Low-quality audio**, and check its size against the host's per-file limit.
2. **Word-level transcript** of that audio, with names and terms as the vocabulary hint.
3. **Selection.** This is the real work and is not mechanical: look for what *sounds* good and catches a stranger's attention, not what is most important in content. Give the strongest model available a readable transcript built from the word-level one (`[HH:MM:SS]` per segment), plus the essentials of the prep note (topic, the host's threads, any anonymization requirement as context). Instructions that worked twice without a single anchor error: read everything first; think about what would stop a stranger with no context; 10 to 18 themes, 2 to 4 clip candidates each; verbatim start and end phrases of 3 to 8 words; speaker inferred from context; mark 6 to 9 as best, not all; extra weight on the opening clip; output only a machine-readable spec list.
4. **Spec:** one entry per clip: `(theme, speaker, start phrase, end phrase, pre-selected)`. Save it.
5. **Generate** `clips.json`, peaks and overview from audio, words and spec. Read every warning (too long, too short, partial anchor match) before going on.
6. **Page** from the template, with the per-episode key.
7. **Before deploying, compare the shared files on the live site with your local copy.** If they differ, the live version wins; do not push local files blindly.
8. **Deploy and check** that the page, `clips.json`, the overview, the audio and a sample of peak files all answer with HTTP 200. Send the link to the host only.

## Content rules

- A clip is not a quote: it must work as sound. A perfect thought is useless while the speaker searches for words.
- Cut at sentence boundaries, not clause boundaries.
- `text` is cleaned; `words` and timing are raw.
- When it is unclear where the good part starts, give two versions and let the host decide by ear.

## Pitfalls

- Search the end anchor only after the start anchor, within a window (75 seconds by default); a global search once produced a 2177-second "clip" with valid-looking data. <!-- rule:R-001 since:2026-08-20 -->
- Take anchors from the same transcript the clips are cut from; anchors written from a separate subtitle run missed 16 of 45. Fix a miss by rewriting the anchor, not by loosening the search. <!-- rule:R-002 since:2026-08-20 -->
- Pad each clip's word list by about four seconds on both sides so cuts stay movable. Low evidence: a design choice that worked, not a measured comparison. <!-- rule:R-003 since:2026-08-20 evidence:low -->
- Some static hosts answer audio range requests with 200 instead of 206, which makes seeking jump back to zero; load the audio once as a blob. <!-- rule:R-004 since:2026-08-20 -->
- Version the shared script and style files (`?v=N`) and raise the number on every change; otherwise open pages run old code without any visible error. <!-- rule:R-005 since:2026-08-20 -->
- Keep generator scripts in the vault; a parallel session once wiped untracked files in a deploy working copy. <!-- rule:R-006 since:2026-08-20 -->
- Compare live shared files with local ones before deploying; shared files once turned out never to have been in version control, and a blind deploy would have deleted them from live pages. <!-- rule:R-007 since:2026-08-23 -->
- Check the downloaded audio's duration against the transcript; exported file names follow the editor's order, not episode IDs. <!-- rule:R-008 since:2026-08-23 -->
- Pass an anonymization requirement to the selection step as context; do not edit the transcript. <!-- rule:R-009 since:2026-08-23 -->
- HTTP clients that send a default library User-Agent may be rejected by a CDN (HTTP 403); send a curl-like one. <!-- rule:R-010 since:2026-08-20 -->
- When the host corrects the selection or the page, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-011 since:2026-10-02 -->
