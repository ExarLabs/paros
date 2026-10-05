---
title: podcast description
date: 2026-10-05
status: active
description: Writes the video description of a podcast episode from a template derived from the show's own published descriptions; a quoted hook with a searchable keyword, context, a bullet block of open questions, a one-line guest introduction, related episodes most-viewed first, chapters, an optional guest contact block, the footer copied verbatim from LOCAL.md, and hashtags.
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# description: one template, a changing head and a fixed footer

A description has two parts. The **head** changes with every episode and decides whether anyone reads on. The **footer** is the same under every video, word for word: links, support, credits. The fastest way to break a channel's consistency is to reword the footer a little each week.

The template in this skill was not designed in theory. It was derived from two descriptions the show had actually published, which differed; at every point of difference, the better practice became the rule. Do the same with your own: derive `LOCAL.md` from your best published descriptions.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The footer in `LOCAL.md` is copied verbatim. It is never reworded or shortened. If it is out of date, it is fixed in `LOCAL.md`, not in one episode.
- Chapter times come from the `chapters` skill, which takes them from the edited cut. Guessing is not allowed.
- Only public contact details the guest has chosen to share go into the description. If in doubt, ask.
- A link that looks misspelled but works stays as it is if `LOCAL.md` says so; "fixing" it would break it.

## Personal settings: LOCAL.md

Show block, the footer (verbatim), mandatory and optional hashtags, the emoji rule, the related-episodes line format, whether a "continue in order" playlist line leads the related block, the guest line format, and the show's own rules for keywords. Without `LOCAL.md`, ask for the footer before writing; never invent one.

## When to use

- Title, thumbnail and chapters are decided.
- "Write the description", "check this description".

## The template

### Head (changes per episode)

1. **Hook, two lines.** This is what shows before "more". Start with a **verbatim quote** from the episode, in quotation marks: the strongest, most personal sentence. Then one sentence that states the stake and contains **at least one searchable keyword**, the word people actually type. If the title lacks the main keyword, it must be here. Do not repeat the title as the first line; the platform shows it above.
2. **Context, one or two paragraphs.** Who the guest is, what the situation is, why it is worth watching. Not a biography: the stake. Concrete, narrative.
3. **"In this episode:"** five to seven bullets, each an open question or a surprising claim. Not a table of contents: a reason not to skip.
4. **Guest line, one line:** `The guest: <name>, <what they do, years of experience, field>.` Cheap authority.
5. **Related episodes:** two by default, **the most viewed first**, not the oldest. If `LOCAL.md` asks for it, a "continue in order" playlist link starting at the most viewed related video leads the block. This is the series effect, one of the few proven ways to keep a viewer on the channel.
6. **Chapters** from `chapters`, without ★ marks.
7. **Guest contact (optional):** public, guest-approved links only, after the chapters and before the footer. Guests share videos more readily when their contact is there.

### Footer (identical under every video)

Copied from `LOCAL.md`, unchanged. Then hashtags on a separate last line: the mandatory ones from `LOCAL.md`, two or three main topics, three to five specific searchable ones, and the guest's name as one tag. Eight to eleven in total unless `LOCAL.md` says otherwise.

## Steps

1. Read `LOCAL.md`, the transcript or synthesis, the chosen title and thumbnail, and the clean chapters.
2. Find the strongest verbatim quote and the main search keyword.
3. Look up related episodes and their view counts; pick the two most viewed relevant ones.
4. Write the head, paste the chapters, paste the footer verbatim, add hashtags.
5. Run the checklist below and report it.

## Checklist before hand-over

- [ ] Emoji rule from `LOCAL.md` respected.
- [ ] First paragraph opens with a quote and contains a searchable keyword.
- [ ] If the title lacks the main keyword, the hook has it.
- [ ] "In this episode" block with five to seven bullets.
- [ ] One-line guest introduction.
- [ ] Two related episodes, the most viewed first (and the playlist line if `LOCAL.md` asks).
- [ ] Chapters start at `00:00:00`, full form, ten to twelve (full coverage for list episodes), no ★.
- [ ] Guest contact block if the guest has public, approved contacts.
- [ ] Footer present in full, verbatim.
- [ ] Hashtag count and the mandatory ones.

## Pitfalls

- Copy the footer verbatim, every time; one published episode dropped the support block without any reason, and the owner had to ask for it back. <!-- rule:R-001 since:2026-08-04 -->
- Derive the template from your own published descriptions, not from theory; where two differ, choose and write down why. <!-- rule:R-002 since:2026-08-04 -->
- Do not repeat the title as the first line; it wastes the most valuable line. <!-- rule:R-003 since:2026-08-04 -->
- Related episodes: two, most viewed first. <!-- rule:R-004 since:2026-08-04 -->
- One consistent chapter format (full `HH:MM:SS`), never mixed with the short form. <!-- rule:R-005 since:2026-08-04 -->
- Add the guest contact block only with public, guest-approved links. <!-- rule:R-006 since:2026-10-02 -->
- In list-format episodes the chapter list covers every item. Low evidence: from one episode. <!-- rule:R-007 since:2026-10-02 evidence:low -->
- When a footer element changes (new platform, new supporter, dead link), change `LOCAL.md` and say so in `LEARNINGS.md`; never patch one episode. <!-- rule:R-008 since:2026-08-04 -->
- When the owner edits the description by hand, record what changed as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-009 since:2026-10-02 -->
