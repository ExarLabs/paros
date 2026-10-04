# P02. Megjelenítés HTML-ben, élő nézetként, ami a markdownba ír vissza

**Elv.** Amit az ember néz, az HTML: weboldal, gráf, interaktív felület. A felület a markdownból olvas, és ha ír, a markdownba ír vissza; saját tudástára nincs.

**Miért.** A markdown jó tárolásra, de rossz áttekintésre. A HTML-nézet adja az áttekintést, a markdown marad az igazság (P01).

**Gyakorlat.**
- **Élő nézet** (helyi webalkalmazás, dashboard): magától frissül, ha a vault változik; látszik rajta a forrás és a frissesség.
- **Pillanatkép** (PDF, kiküldött anyag, statikus oldal): nem frissül; rajta a dátum és a forrás („állapot: ÉÉÉÉ-HH-NN").
- Visszaírás (például egy feladat kipipálása) mindig a markdown-fájlba megy.

**Ellenőrzés.**
- Van-e olyan felület, aminek saját adattára van, ami a vaultban nem létezik?
- A pillanatképeken szerepel-e dátum és forrás?

**Átvétel.** Modul: kezdetben elég az Obsidian saját nézete. Ha nézet kell, előbb pillanatkép (generált HTML), később élő nézet.
