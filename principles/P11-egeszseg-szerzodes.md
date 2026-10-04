# P11. Bizonyíték nélkül nincs „működik"

**Elv.** Egy folyamat attól egészséges, hogy egy valódi bemenetből a várt kimenet ténylegesen előáll, nem attól, hogy fut, vagy hogy a leírás szerint létezik. Minden automatikus folyamat mellé kell egy ellenőrzés, ami a **kimenetét** nézi.

**Miért.** Egy személyes agent-rendszer domináns hibaosztálya a **csendes hiba**: egy hook hónapokig nem ír, egy index hónapokig nem frissül, egy titok a vaultban marad, és senki nem veszi észre, mert semmi nem jelez.

**Gyakorlat.**
- **Végponttól végpontig próba (canary):** egy futás egyedi jelzőt ír egy jegyzetbe, a következő a keresési indexben keresi. Ha megvan, az írás, a fájlfigyelés, az index és a keresés is működik.
- Ellenőrzések súllyal (1: csak napló, 2-3: riasztás). Tipikus: index frissessége, a munkamenet-napló írása, nyílt titok a vaultban, titok-leltár, frontmatter a friss fájlokon, a tanulási ciklus futása, a mentés kora.
- **Riasztás csak állapotváltáskor:** amikor egy ellenőrzés zöldből pirosba vált, egy sor kerül a gazda feladatlistájába; amíg piros, nem jön újabb; helyreálláskor a sor megjelölést kap.
- Új automatikus folyamat csak ellenőrzéssel együtt születik.

**Ellenőrzés.** Futtasd le az egészség-ellenőrzést; ha nincs, az maga a lelet.

**Átvétel.** Kezdetben 3 ellenőrzés: canary, index-frissesség, nyílt titok. Ütemezés: néhány óránként (kit: `kits/health`).
