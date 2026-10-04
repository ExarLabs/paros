# Átállás PAROS-ra

Ez az agent munkaterve, amikor egy felhasználó vaultját először alakítja PAROS-szá. Négy fázis; az első csak olvas.

## 0. Biztonság

- Van-e visszaút a vaultban (git, másolat, szinkron-előzmény)? Ha nincs, az első tétel ennek megteremtése, a felhasználóval egyeztetve.
- A referencia elérési útja (például `~/paros-reference`) rögzül a vault belépőjében, hogy a későbbi sessionök is megtalálják.

## 1. Felmérés (csak olvasás)

Térképezd fel, és írd le röviden:

| Kérdés | Mit nézz |
|---|---|
| Mekkora és milyen a vault? | fájlszám, mappaszerkezet, markdown aránya, csatolmányok |
| Milyen területei vannak a felhasználó életének és munkájának? | felső szintű mappák, gyakori témák; kérdezd meg, ha nem egyértelmű |
| Van-e frontmatter, és milyen? | minta 20 fájlból |
| Van-e már agent-belépő (`AGENTS.md`, `CLAUDE.md`), memória, feladatlista? | gyökér és almappák |
| Milyen gépeken és szinkronnal él? | kérdezd meg: hány gép, milyen szinkron (Obsidian Sync, iCloud, git, Drive) |
| Milyen külső eszközöket használ? | levelezés, naptár, CRM, projektmenedzsment; kérdezd meg |
| Melyik agent-platformon dolgozik? | Claude Code, Codex, más |

A felmérés eredménye a felhasználó vaultjába kerül: `PAROS/SURVEY.md`.

## 2. Átállási lista

Az elvek (`principles/`) mindegyikéhez nézd meg az **Ellenőrzés** szakaszt a felmérés fényében, és döntsd el:
- **megvan**: az elv már teljesül, nincs teendő;
- **átvehető**: konkrét lépések kellenek (írd le őket a vault saját helyzetére szabva);
- **később**: az elv még nem időszerű (például nincs külső eszköz, így a connector-elv várhat);
- **nem kell**: a felhasználó tudatosan nem kéri (indoklással).

Írd a listát ide: `PAROS/ADOPTION.md` (sablon: `templates/ADOPTION.md`). Sorrend: előbb a **mag** elvek (P00, P01, P03, P04, P06, P09, P11), aztán a többi. Mutasd meg a felhasználónak, és kérd a jóváhagyását a sorrendre.

## 3. Végrehajtás

- Egyszerre egy tétel. Előtte egy mondat arról, mit fogsz tenni; utána egy mondat arról, mi lett.
- Ami meglévő tartalmat érint, ahhoz előbb igen kell.
- Ha egy tétel közben kiderül, hogy az elv nem illik a felhasználóhoz, ne erőltesd: jelöld `adaptálva` vagy `nem kell`, indoklással.
- Minden lezárt tétel dátummal kerül az `ADOPTION.md` naplójába. Ez a vault emlékezete arról, hogyan lett PAROS.

## 4. Ellenőrzés

Minden elvnél van **Ellenőrzés** szakasz: futtasd le, és rögzítsd az eredményt. Az átállás akkor kész, ha a mag elvek ellenőrzése zöld, és a felhasználó egy új sessionben azt tapasztalja, hogy az agent magától megtalálja, amit kell.

## Elvek az átállás közben

- **Adaptálj, ne másolj.** A sablon a kiindulópont.
- **A felhasználó szavai a mérce.** Ha valamit másképp akar, az az ő PAROS-a.
- **Kis lépésekben.** Egy jó első hét: belépő, frontmatter, feladatlista, keresés. A tanulási ciklus és a connectorok ráérnek.
