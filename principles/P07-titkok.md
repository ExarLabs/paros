# P07. Titkok: a vaulton kívül, titkosítva utaznak, leltár érték nélkül

**Elv.** Minden connector egy titokhoz kötődik (API-kulcs, token, jelszó). A titok **értéke soha nem kerül a vaultba**, a chatbe vagy az agent kontextusába. A vaultba csak két dolog kerül: a titkosított átviteli csomag és a **leltár** (érték nélkül).

**Miért.** A vault szinkronizál, indexelődik, és az AI olvassa; egy oda került titok kiszivárgott titok. Egy agent-rendszerben külön kockázat, hogy az agent maga olvashatja ki és küldheti el a titkot (prompt-injekció).

**Gyakorlat: négy réteg.**

| Réteg | Hol | Mi | Szinkron |
|---|---|---|---|
| 1. A titok | gépenként, a vaulton kívül (például `~/.paros/secrets/`) | az érték | nem |
| 2. Átvitel | a vaultban | titkosított csomag: egy véletlen kulcs zárja (AES-256-GCM), amit minden gép publikus kulcsára rátitkosítunk; a gépen jelmondat nyitja a gép saját kulcsát | igen |
| 3. Leltár | a vaultban (`SECRETS.json` + generált nézet) | érték nélkül: mi, mire való, ki használja, jogkör, rotálás, hol kell visszavonni | igen |
| 4. Felügyelet | szkript + egészség-ellenőrzés | ismeretlen, hiányzó, lejárt titok; nyílt titok a vaultban | riasztás |

- Az agent **a leltárt olvassa**, a titkot soha; a szkript név szerint kéri le.
- Új titok = új leltársor, ugyanabban a lépésben.
- Kiszivárgott titok: azonnali rotálás a szolgáltatónál.
- Javasolt: egy **helyreállító címzett** (erős jelmondattal védett kulcs), hogy minden gép elvesztése után is visszaállíthatók legyenek a titkok.

**Ellenőrzés.**
- Keresés a vaultban titok-mintázatokra (API-kulcs-formátumok, privát kulcs fejléc).
- Van-e minden titoknak leltársora?

**Átvétel.** Az első connector bekötésekor: titok-mappa a vaulton kívül, leltár, és a vault-pásztázás az egészség-ellenőrzésben. Az átviteli csomag akkor kell, amikor a második gép megjelenik (kit: `kits/secrets`).
