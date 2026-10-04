# P04. Vékony belépő, élő markdown-definíció

**Elv.** Minden agent és skill két részből áll: egy **vékony belépőből** (név, mikor kell használni, hová mutat) és egy **élő definícióból** a vaultban (a tényleges tudás markdownban, verzióval). A belépő mindig az élő definíciót olvassa: **a vault mindig nyer.**

**Miért.** Ha a tudás a platform saját fájljaiban (plugin, beállítás) élne, nem tanulna, nem lenne verziózva, és platformváltáskor elveszne. Így a tudás a vaultban van, a belépő pedig bármely platformra pár sorban megírható.

**Gyakorlat.**
- Skill: `<skill>/CURRENT.md` (élő definíció), mellette `LEARNINGS.md` (napló), `observations/` (tanulási inbox), `versions/` (régi verziók).
- Az agent a skillekre mutat; ami lépésről lépésre leírható, az skill, nem agent-szöveg.
- A belépő kiírja, melyik verzió futott.

**Ellenőrzés.**
- Van-e olyan skill vagy parancs, aminek a teljes tartalma a platform-fájlban (például `SKILL.md`) van, élő definíció nélkül?

**Átvétel.**
1. Az első skill élő definícióval (sablon: `templates/skill-CURRENT.md`).
2. A meglévő skillek fokozatos átköltöztetése.

**Platform.** Az Agent Skills formátum (`SKILL.md`) a Claude Code-ban és a Codexben is működik; a belépő mindkettőben ugyanaz lehet: „olvasd be a `<vault>/…/CURRENT.md`-t, és aszerint dolgozz".
