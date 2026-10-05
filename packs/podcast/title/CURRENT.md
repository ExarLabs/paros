---
title: podcast title
date: 2026-10-05
status: active
description: Writes five video titles for a podcast episode in the show's fixed format, paired with the already chosen thumbnail text; keeps the clickable part under 75 characters with the essence in the first 60, reframes niche topics as a universal burden when the content is deep enough, and ranks the proposals against measured channel patterns.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# title: the title that completes the thumbnail

The title is read after the thumbnail and next to it. Its job is to fill what the thumbnail opens: context, a quote, the stake. It also has to survive truncation on a phone, and it has to be findable by search.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The title follows the show's fixed format from `LOCAL.md`. The format is the brand, not a matter of taste.
- The parts the format marks as mandatory for search (for example the guest's name and the episode number) are always written, even when a phone cuts them off.
- The ranking comes from measured data (the channel intelligence file or `LOCAL.md`), not from a hunch. Where there is no data, say so.

## Personal settings: LOCAL.md

Show block, the title format with its mandatory parts, the length rule if the show measured its own, the emotional registers that work for this audience, patterns to avoid, and two or three accepted titles from the show's history as examples. Without `LOCAL.md`, use `"<quote or claim>": <topic> | <guest>` and the length rule below.

## When to use

- After the thumbnail text is chosen. If it is not, say so and suggest running `thumbnail` first; if the owner insists, work without it.
- "Title ideas", "is this title good?", "rank these titles".

## Inputs

The transcript (or the synthesis), guest name, episode number, the chosen thumbnail text.

## Steps

1. Read `LOCAL.md` and the channel intelligence file.
2. **Niche check first.** If the topic is specific to a profession, an industry or a region, ask before anything else: *which universal, unavoidable burden does this topic explain or cause?* The title sells that burden; the niche term goes into the description and tags. In one measured case, a niche episode reframed this way became one of the fastest-growing episodes of its year, far above the niche band. Brake: the reframed title needs deep content behind it. Shallow content under a universal title gets the click and loses the viewer; if that is the case, tell the owner the title promises more than the episode holds.
3. Write five titles in the format. Vary the register: one warning or negative, one inspiring or success story, one professional or educational, two free. Avoid stock openings ("A conversation about...").
4. **Pair each with the thumbnail.** The title does not repeat the thumbnail in words or idea; it fills what the thumbnail raises. One half-sentence per title on how they pair.
5. **Length.** The quote and topic part stays **under 75 characters**, and the part that makes someone click sits in the **first 60**. The mandatory tail (guest, number) may be cut off on a phone; write it anyway. Count the characters and show the count.
6. **Rank.** Give each title a score from 1 to 10 with one line of reasoning: which register fits this topic's audience, is there a searchable keyword, is there an earlier episode with this guest (series effect), does it avoid the channel's weak patterns (too abstract, poetic, generic), and for a niche topic, does it reframe to a universal burden.

## Output

Five titles, each with: the title, character count of the front part, the pairing with the thumbnail, the score and its reason. One recommendation.

## Pitfalls

- Run after the thumbnail is chosen; ask for it, and pair every title with it. <!-- rule:R-001 since:2026-09-08 -->
- Keep the front part under 75 characters with the essence in the first 60; a rigid 60-character ceiling did not match the owner's own accepted titles (71 and 72 characters). <!-- rule:R-002 since:2026-08-07 -->
- For a niche topic, sell the universal burden it explains, not the niche term; only over deep content. <!-- rule:R-003 since:2026-08-21 -->
- Always write the mandatory tail (guest, episode number) for search, even if a phone truncates it. <!-- rule:R-004 since:2026-07-28 -->
- Never let the title repeat the thumbnail text. <!-- rule:R-005 since:2026-10-02 -->
- Do not rank by feel; cite the measured pattern or say there is none. <!-- rule:R-006 since:2026-07-28 -->
- When the owner picks or rewrites a title, record it as a learning packet in this skill's `observations/` folder (P05); two independent cases that agree are enough to change a rule. <!-- rule:R-007 since:2026-10-02 -->
