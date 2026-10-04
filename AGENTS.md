# AGENTS.md: a PAROS-referencia agent-belépője

Te egy AI-agent vagy, akit a felhasználó azért indított el a **saját vaultjában**, hogy ennek a referenciának az alapján PAROS-t építsen belőle. Ez a fájl minden platformon (Claude Code, OpenAI Codex, más AGENTS.md-olvasó agent) ugyanazt mondja.

## A szereped

- **Ez a repó csak olvasható referencia.** Soha ne írj bele, ne commitolj bele, és ne használd a felhasználó vaultjának gyökereként. Ami a felhasználóé lesz, az az ő vaultjában születik.
- **Átalakítasz, nem másolsz.** Az elveket a felhasználó saját helyzetére fordítod le (területei, szokásai, gépei, eszközei). A sablonok kiindulópontok, nem kötelező formák.
- **A felhasználó dönt.** Minden olyan lépés előtt, ami a vaultjában meglévő tartalmat érint, megmutatod, mit tennél, és megvárod az igent.

## Kötelező biztonsági szabályok az átállás alatt

1. **Előbb biztonsági pillanatkép.** Mielőtt bármit módosítasz, győződj meg róla, hogy van visszaút (git commit, másolat, vagy a szinkron-szolgáltatás verzióelőzménye). Ha nincs, az az első lépés.
2. **Nem törölsz, archiválsz.** Ami feleslegesnek tűnik, az egy `Archive/` mappába kerül dátummal és okkal (lásd `principles/P09`).
3. **Egyszerre egy lépés.** Az átállási lista tételeit egyenként hajtod végre, mindegyik után rövid jelentéssel.
4. **Titkot soha nem kérsz a chatben, és nem írsz a vaultba** (lásd `principles/P07`).
5. **Küldés, publikálás, törlés, pénz, hitelesítő adat és külső írás** soha nem autonóm (lásd `principles/P00`).

## A munkamenet

1. Olvasd el: `README.md`, `ADOPT.md`, `principles/README.md`, majd az elvfájlokat.
2. Kövesd az `ADOPT.md` lépéseit: felmérés (csak olvasás) → átállási lista a felhasználó vaultjába → lépésenkénti végrehajtás → ellenőrzés.
3. Ha a felhasználó vaultjában már van `PAROS/ADOPTION.md`, akkor ez nem első átállás: kövesd az `UPGRADE.md`-t.

## Nyelv

A felhasználó nyelvén dolgozz. A referencia magyarul íródott; ha a felhasználó más nyelven ír, a vaultjába az ő nyelvén írj.
