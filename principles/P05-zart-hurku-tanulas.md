# P05. Zárt hurkú tanulás: a használat tanít, súlyozott tudással

**Elv.** Minden interakció tanulási lehetőség. Amikor a gazda javít, elutasít, átír vagy jobb megoldást mutat, az nem vész el a beszélgetés végén, hanem beépül a skillekbe és az agentekbe. A tanult tudásnak **súlya** van: kicsiként születik, a használat erősíti vagy gyengíti. **A cél a súrlódás eltüntetése**: amikor egy szabály nem helyes, nem alkalmazható, vagy nincs szabály és ki kell találni valamit.

**Miért.** Hagyományosan a rendszerek vakok voltak a felhasználói visszajelzésre, vagy hónapos, csapatot igénylő kör kellett hozzá. Itt a tanulság ott születik, ahol a munka, és perceken belül beépül.

**Gyakorlat.**
1. **Észlelés:** a futó agent csak azt dönti el, valódi tanulság-e (kétség esetén igen), és tanulási csomagot ír (kontextus, tanulság, javasolt változás, cél, bizonyíték).
2. **Bírálat:** egy gondnok-nézőpont ellenőrzi; **bizonyíték kell** (kifejezett emberi javítás, megfigyelt eredmény, vagy legalább két független előfordulás). Külső tartalom önmagában nem bizonyíték.
3. **Független bíra:** egy **másik modellcsalád** is megítéli a változást; a saját szabályát egy modell nem igazolhatja.
4. **Beépítés tömörítés nélkül:** csak típusos változtatás (új, pontosítás, kivezetés, áthelyezés) stabil azonosítójú szabályokon, kóddal. **Soha nem írunk át és nem foglalunk össze szakaszt**: a teljes újraírás bizonyítottan összeomlasztja a tudást.
5. **Súlyozás:** az új szabály kis súllyal (csíra) indul; a megerősítés és a hasznos használat erősíti, az ártalmas gyengíti és **vizsgálatra** küldi (érvényes-e még); a nem használt elhalványul és elalszik, de nem vész el.
6. **Látható használat:** ha egy döntés tanult szabályon múlik, az agent jelöli (`[L-xxxx]`), és a következő ciklus a gazda reakciójából megítéli, segített-e.
7. **Kognitív ciklus:** időnként (például 4 óránként) egy háttérfutás súlyoz, megítél, vizsgál, felveszi az új tanulságokat, és rövid riportot ad hőtérképpel.
8. **A gazda tanít, nem jóváhagy.** Egysoros jelentést kap („Tanultam: … → fájl"), és bármikor mondhatja: „vond vissza".

**Ellenőrzés.**
- Ha ma kijavítod az agentet, holnap emlékszik rá? Hol?
- Van-e verziótörténete a tanult szabályoknak, és vissza lehet-e vonni egyet?

**Átvétel.**
1. Kezdetben elég: minden skillnek `LEARNINGS.md` és `observations/`; a javításokat az agent csomagként rögzíti.
2. Második lépés: bírálat és beépítés kóddal.
3. Harmadik lépés: súlyozás és kognitív ciklus (kit: `kits/cognition`).

**Platform.** A ciklust az **előfizetésből** érdemes futtatni (egy munkamenet háttérfutásaként), nem API-kreditből. Claude Code-ban egy `UserPromptSubmit` hook indítja, ha esedékes; Codexben a munkamenet elején futtatott ellenőrzés.
