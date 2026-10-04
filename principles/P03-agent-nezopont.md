# P03. Az agent nézőpont a vaulton, nem külön program

**Elv.** Az agent egy **nézőpont**: egy mód, ahogyan a vaultot megfogjuk (például „emberek", „pénz", „marketing", „a gazda napi operációja"). Egy fájlban él: térkép (hol van a releváns tudás), szabályok, hozzáállás. Agent akkor kell, ha a nézőpont **több területen átvág**; egy területen belül a terület saját belépője elég.

**Miért.** A vault területek szerint tagolódik (függőleges), az agent keresztbe vág (vízszintes). Ha minden feladathoz külön agent születik, sok sekély, ütköző szerep lesz. Cél: néhány mély nézőpont, nem sok sekély.

**Gyakorlat.**
- A nézőpontot a fő munkamenet is felveheti: beolvassa a nézőpont-fájlt. Nem kell hozzá külön futás.
- **Külön futás (munkás, subagent)** csak hat ok miatt: kontextus-védelem (sokat kell olvasni, csak összegzés kell vissza), párhuzamosság, függetlenség (friss szem kell), felügyelet nélküli futás, olcsóbb modell, szűk jogosultság. A munkás is a nézőpont-fájllal indul.
- **Új agent előtt írásos indoklás:** miért nem fér bele egy meglévőbe.
- Próba: ha ugyanaz a kérés név nélkül és névvel más eredményt ad, az útválasztási hiba. A rendszernek a témából kell felismernie a nézőpontot.

**Ellenőrzés.**
- Hány agent van, és mindegyik átvág-e legalább két területen?
- Van-e olyan agent, ami valójában egy eljárás (azt skillbe kell tenni, P04)?

**Átvétel.**
1. Kezdetben nulla vagy egy agent; a fő munkamenet és a területi belépők elegendők.
2. Nézőpont-fájl akkor születik, amikor egy keresztmetszeti téma harmadszor kerül elő.

**Platform.** Claude Code: `.claude/agents/<név>.md` vékony belépő a nézőpont-fájlra mutatva. Codex: az `AGENTS.md`-ben vagy egy skillben hivatkozott nézőpont-fájl.
