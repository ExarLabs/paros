# P06. Keresés index-first, képességként

**Elv.** A vaultban keresés egy **képesség** (skill), nem egy agent. Elsőként egy friss teljes szöveges indexből keresünk, rangsorolva; a nyers fájlkeresés (grep) csak pontos szövegre és kódra való.

**Miért.** Egy nagy vaultban a nyers keresés lassú, zajos és sok kontextust eszik. Mérve: az index az első helyen a jó találatot sokkal gyakrabban adja, mint a grep. Az index származtatott (P01), bármikor újraépíthető.

**Gyakorlat.**
- A kérdést 2-4 jellemző szótőre fordítjuk le, és az index rangsorolva adja a találatokat; a `title` és a `description` mező nagyobb súlyt kap, mint a törzs.
- Ha sok fájlt kell összeolvasni, egy kontextus-védő munkás végzi (P03), ugyanezzel a képességgel, és csak az összegzést hozza vissza.
- Az index frissességét az egészség-ellenőrzés figyeli (P11).

**Ellenőrzés.**
- Öt valódi kérdésre az első találat jó-e?
- Mennyi idős az index?

**Átvétel.**
1. Kicsi vaultnál elég az Obsidian keresője és a grep.
2. Pár ezer fájl felett: SQLite FTS5 index a frontmatterből és a törzsből (kit: `kits/search`), és egy skill, ami ezt használja.
