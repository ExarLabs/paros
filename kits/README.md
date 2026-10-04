# Kitek: opcionális referencia-implementációk

A kit egy működő példa egy elvhez. **Nem kötelező**, és nem másoljuk vakon: az agent elolvassa, és a felhasználó vaultjához igazítva építi újra (vagy átveszi és adaptálja). A kód eldobható; az elv és az ellenőrzés a lényeg.

| Kit | Elv | Mit ad | Állapot |
|---|---|---|---|
| `search` | P06 | SQLite FTS5 index a vaultból, rangsorolt keresés 2-4 szótőre, read-only skill | tervezett |
| `cognition` | P05 | súlyozott tanult szabályok, használat-jelölés, kognitív ciklus, riport hőtérképpel; hookok Claude Code-hoz | tervezett |
| `learn-merge` | P05 | típusos, tömörítés nélküli szabály-változtatás (add, update, deprecate, move), verzió-pillanatkép, napló; független bíra egy másik modellcsaládból | tervezett |
| `health` | P11 | canary és súlyozott ellenőrzések, riasztás állapotváltáskor | tervezett |
| `secrets` | P07 | titok-leltár (érték nélkül), gépenkénti jelenlét, egészség-ellenőrzés; titkosított átviteli csomag | tervezett |
| `backup` | P10 | titkosított pillanatkép-mentés ütemezéssel és próba-visszaállítással | tervezett |

Platform-jelölés minden kitnél: mi működik Claude Code-ban, mi Codexben, és mi platformfüggetlen (a szkriptek Pythonban, függőség nélkül vagy minimális függőséggel).
