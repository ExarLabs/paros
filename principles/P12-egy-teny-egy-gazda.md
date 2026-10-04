# P12. Egy tény, egy gazda

**Elv.** Minden ténynek pontosan egy irányadó helye van. Minden más előfordulása hivatkozás vagy kimondottan származtatott másolat (forrással és dátummal).

**Miért.** Ha ugyanaz a tény két helyen él, előbb-utóbb eltérnek, és nem tudni, melyik igaz. Egy AI-rendszer ráadásul mindkettőt magabiztosan idézi.

**Gyakorlat.**
- Egy **forrás-térkép** (például `ARCHITECTURE_BOUNDARIES.md`) adatfajtánként megmondja, mi az irányadó és mi származtatott.
- Az agentek listája, verziója egy helyen él; a többi dokumentum csak hivatkozik rá.
- Külső rendszer saját tartományában (CRM, közös dokumentumtár) a külső rendszer az irányadó (P08).
- Generált nézet (index, összefoglaló, HTML) mindig jelöli, miből és mikor készült, és kézzel nem szerkesztjük.

**Ellenőrzés.**
- Keress egy gyakran változó tényt (például egy agent verzióját): hány helyen szerepel, és egyeznek-e?

**Átvétel.** Forrás-térkép a vaultban, és szabály a belépőben: „új adatfajta előbb a térképre kerül, utána íródik".
