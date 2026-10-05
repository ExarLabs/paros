---
title: speed-reader LOCAL
date: 2026-10-05
status: active
description: Personal settings for the speed-reader skill (output language, folders, file naming, frontmatter, tag vocabulary, depth, atomic and contrast note policy). Copy to LOCAL.md and fill in your own values.
---

# speed-reader: personal settings

> Example values. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below with your own. `CURRENT.md` reads `LOCAL.md`; it never contains these values itself.

## Language

- Notes in: `English`, whatever the language of the source.
- Quotes stay in the original language, with my own translation in brackets when it is not English.

## Folders and names

| Type | Folder | File name |
|---|---|---|
| Book | `Resources/Books/<Author> - <Title>/` | `<Author> - <Title>.md` |
| Article | `Resources/Articles/` | `YYYY-MM-DD <Title>.md` |
| Podcast | `Resources/Podcasts/<Show>/` | `<Show> <episode number> <Title>.md` |
| Atomic notes | `Resources/Ideas/` | `<Concept>.md` |
| Contrast notes | `Resources/Contrasts/` | `<A> vs <B> on <topic>.md` |

## Frontmatter

```yaml
title:
date:
status: active
description:
type: book | article | podcast
author:
year:
source:
tags: []
```

## Tag vocabulary

Prefer these before inventing new ones: `leadership`, `psychology`, `economics`, `history`, `writing`, `health`, `research`, `memoir`, `howto`.

## Depth

- Books: a few paragraphs per chapter; up to two pages for the chapters I mark as central.
- Articles: one paragraph per section.
- Podcasts: segments of 5 to 15 minutes with timestamps.

## Atomic and contrast notes

- Suggest only. Create them when I say "create the atomic notes".
