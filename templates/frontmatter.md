# Frontmatter-séma (P01)

```yaml
---
title: <a fájl neve>
date: <ÉÉÉÉ-HH-NN>
author: <a gazda neve>
status: active | draft | done | archived
description: <1-2 mondat a TARTALOMRÓL, kötelező>
id: <uuid4>
tags: [opcionális]
version: <semver, csak verziózott fájlokhoz>
---
```

A `description` a legfontosabb mező: a keresés ezen fut, és az agent ebből dönti el, hogy érdemes-e megnyitni a fájlt. Tartalmi legyen („A 2026-os költségvetés havi bontása és a három eltérés oka"), ne általános („Jegyzet a költségvetésről").
