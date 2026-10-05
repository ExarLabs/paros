---
title: podcast thumbnail
date: 2026-10-05
status: active
description: Writes five thumbnail texts for a podcast episode before the title exists; short, mobile-first, in deliberately varied forms with at most two questions, each with a direction the title should take, so the title can complement the thumbnail instead of repeating it.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# thumbnail: the first metadata decision

On a phone, the viewer sees the thumbnail before anything else, and the thumbnail text is read in a fraction of a second. That is why the thumbnail is decided **first**, and the title follows it. This skill writes the thumbnail text and gives the `title` skill a direction to work in.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The thumbnail never repeats the title. It complements it or creates tension against it.
- Mobile first: the text must be readable on a phone at thumbnail size.
- The owner picks the text; this skill proposes.

## Personal settings: LOCAL.md

Show block (with the measured share of mobile viewers), the word limit, the visual style of the show's thumbnails (where the face goes, where the text goes, case), good examples from the show's own history, and the forms that worked or failed on this channel. Without `LOCAL.md`: at most four words, two to three preferred.

## When to use

- After the recording, once there is a transcript (or the cold open), and before the title.
- "Thumbnail ideas", "what should the thumbnail say?"

## Steps

1. Read the transcript (or the cold-open sheet and the synthesis), the show block in `LOCAL.md`, and the channel intelligence file if it exists.
2. Write five texts. Rules:
   - **Length:** the limit in `LOCAL.md`; shorter wins on mobile.
   - **Style:** provocative, questioning or factual; never a lie the episode does not support.
   - **Varied forms.** At most two of the five are questions. The others come from different forms: statement, first-person confession, contrast pair, number, plain fact, single word. Ten variants of one form are not a choice.
   - Speak to the real audience of the topic: personal for personal topics, concrete for technical ones.
3. For each text give:
   - **Text**;
   - **Form** (question, statement, confession, contrast, number, fact, single word);
   - **Title direction:** what kind of title would complete it (contrast, complement, reinforcement). This is input for `title`, not a title.
4. If you ask another model for ideas, pass the form-variety rule to it explicitly.
5. Recommend one, and say why.

## Output

A list of five, each with text, form and title direction, plus one recommendation. After the owner picks, record the chosen text in the episode folder so `title` can read it.

## Pitfalls

- Decide the thumbnail before the title; the title adapts to it. Do not wait for title candidates. <!-- rule:R-001 since:2026-09-08 -->
- Never repeat the title in the thumbnail, word for word or in idea. <!-- rule:R-002 since:2026-07-28 -->
- At most two questions out of five, and varied forms; a "question marks get clicks" rule once produced ten two-word questions from an external model. <!-- rule:R-003 since:2026-10-02 -->
- Keep it within the word limit; two to three words read better on a phone than four. <!-- rule:R-004 since:2026-07-28 -->
- When the owner rejects or rewrites the proposals, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-005 since:2026-10-02 -->
