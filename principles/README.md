# A PAROS alapelvei

Minden elv egy fájl, ugyanazzal a szerkezettel: **Elv** (egy-két mondat), **Miért**, **Gyakorlat**, **Ellenőrzés** (hogyan nézed meg a saját vaultodban), **Átvétel** (lépések), **Platform** (Claude Code és Codex különbségek, ha vannak). Az azonosító (P00..P12) stabil: frissítéskor ezekre hivatkozik a `CHANGELOG.md`.

**Mag** = minden PAROS-ban kell. **Modul** = akkor kell, amikor időszerű.

| ID | Elv | Típus | Állapot |
|---|---|---|---|
| [P00](P00-alkotmany-es-hatarok.md) | Egy PAROS egy emberé; alkotmány és biztonsági határok | mag | stabil |
| [P01](P01-perzisztencia.md) | A tudás markdownban (és JSON-ban) él, minden más származtatott | mag | stabil |
| [P02](P02-megjelenites.md) | Megjelenítés HTML-ben, élő nézetként, ami a markdownba ír vissza | modul | stabil |
| [P03](P03-agent-nezopont.md) | Az agent nézőpont a vaulton, nem külön program | mag | stabil |
| [P04](P04-vekony-belepo.md) | Vékony belépő, élő markdown-definíció | mag | stabil |
| [P05](P05-zart-hurku-tanulas.md) | Zárt hurkú tanulás: a használat tanít, súlyozott tudással | mag | stabil |
| [P06](P06-kereses.md) | Keresés index-first, képességként | mag | stabil |
| [P07](P07-titkok.md) | Titkok: a vaulton kívül, titkosítva utaznak, leltár érték nélkül | modul (connectorokkal mag) | stabil |
| [P08](P08-connectorok.md) | Connectorok: a SaaS a gerinc, az AI a ragasztó | modul | stabil |
| [P09](P09-felejtes-es-archivalas.md) | Felejtés: halványul, archiválódik, nem törlődik | mag | stabil |
| [P10](P10-mentes-es-helyreallitas.md) | Mentés: a szinkron nem mentés | mag | javaslat |
| [P11](P11-egeszseg-szerzodes.md) | Bizonyíték nélkül nincs „működik" (egészség-szerződés) | mag | stabil |
| [P12](P12-egy-teny-egy-gazda.md) | Egy tény, egy gazda | mag | stabil |

## A PAROS egy mondatban

Egy ember tudása markdownban, amit AI-agentek nézőpontokként kezelnek, a használatból folyamatosan tanulnak, és ahol a gyors, determinisztikus, közös munka a külső eszközökben (SaaS) marad, az ítélet és az összekötés pedig az AI-é.
