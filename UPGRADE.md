# Frissítés egy újabb referencia-verzióra

A referencia időnként frissül: új elv, pontosított elv, jobb kit. A frissítés **tanács**, nem felülírás.

## Menet

1. A felhasználó frissíti a referenciát (`git pull`).
2. Olvasd ki a vaultban rögzített verziót: `PAROS/ADOPTION.md` fejléce (`reference_version`).
3. Olvasd el a `CHANGELOG.md` azon bejegyzéseit, amelyek ennél újabbak.
4. Minden változásnál nézd meg, érinti-e a felhasználót:
   - **új elv**: kerüljön az átállási listára új tételként (`átvehető`, `később` vagy `nem kell`);
   - **pontosított elv**: ha a felhasználó már átvette, nézd meg, kell-e igazítani a saját változatán; ha `adaptálva` jelölésű, a saját döntését tiszteld;
   - **új vagy javított kit**: csak akkor ajánld, ha a felhasználó használja az adott kitet, vagy szüksége lenne rá.
5. Írd a javaslatokat az `ADOPTION.md`-be egy új „Frissítés vX.Y.Z" szakaszba, mutasd meg a felhasználónak, és ugyanúgy egyenként menjetek végig rajtuk, mint az első átállásnál.
6. A végén frissítsd a `reference_version` mezőt.

## Amit soha

- Nem írod felül a felhasználó saját adaptációit csak azért, mert a referencia másképp mondja.
- Nem másolsz át automatikusan semmit a referenciából.
