# Frontmatter schema (P01)

```yaml
---
title: <file name>
date: <YYYY-MM-DD>
author: <owner>
status: active | draft | done | archived
description: <one or two sentences about the CONTENT, required>
id: <uuid4>
tags: [optional]
version: <semver, only for versioned files>
---
```

`description` is the most important field: search runs on it, and an agent decides from it whether a file is worth opening. Make it about the content ("Monthly 2026 budget with the three variances explained"), not generic ("Notes about the budget").
