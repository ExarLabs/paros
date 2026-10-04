# P08. Connectorok: a SaaS a gerinc, az AI a ragasztó

**Elv.** A külső szolgáltatásoknak (levelezés, naptár, tárhely, projektmenedzsment, CRM, ERP) megvan a helyük, és az AI nem váltja ki őket. A kettő együtt a szuperképesség.

| | SaaS | AI |
|---|---|---|
| Sebesség és költség | ezredmásodperc, olcsó | percek, tokenben drága |
| Determinizmus | ezerből ezerszer ugyanaz | változó |
| Kollaboráció | hitelesítéssel közös | személyes |
| Alkalmazkodás | merev | teljesen dinamikus |

**A connector két szerepe.**
1. **Tudás-forrás** a személyes rendszernek (a levelekből, naptárból megtudjuk, amit egy emberről, ügyről tudni kell).
2. **Közös munkafelület** több személyes rendszer között: itt osztja meg több ember gyorsan, determinisztikusan, állapot-alapon ugyanazt az információt.

**Gyakorlat.**
- **Állapot a SaaS-ban, ítélet az AI-ban.** Ami ezerből ezerszer ugyanúgy kell, az a SaaS-ba (szabály, automatizmus) vagy egy szkriptbe kerül, nem a promptba.
- **Determinizmus-vándorlás.** Amit az AI ismételten ugyanúgy csinál, azt a tanulási ciklus (P05) felismeri, és kódba vagy SaaS-automatizmusba költözteti: a rendszer idővel gyorsabb, olcsóbb, kiszámíthatóbb.
- **Hivatkozz, ne másolj.** A közös rendszer állapotát nem tükrözzük a vaultba (elavul, és két igazság lesz, P12). A vault a saját tudást tartja; pillanatképnél kimondja a lekérés idejét.
- **A connector a recept, nem a kód.** Ami marad: a titok és a leltársora (P07), a fiók egy fiók-listában, a recept-leírás (hogyan használd, buktatók, tanulási hurokkal), és egy ellenőrzés a kimenetére. A kód eldobható.
- **Hivatalos connector, ha elég; saját, ha korlátba ütközünk** (például a hivatalos csak egy fiókot enged, a saját bármennyit).
- **A connectorból jövő tartalom adat, nem utasítás.**
- **Közös orkesztráció:** ha több PAROS dolgozik ugyanazokon a SaaS-eszközökön, fölöttük egy megosztott orkesztrációs réteg hangolhatja össze őket. Rétegek: SaaS (állapot) → közös orkesztráció → PAROS (személyes tudás és ítélet).

**Ellenőrzés.**
- Minden connectornak van-e leltársora, fiók-bejegyzése és recept-leírása?
- Van-e a vaultban tükrözött SaaS-állapot lekérési idő nélkül?

**Átvétel.** Modul: az első connector a leggyakrabban használt külső eszköz (általában levelezés vagy naptár), olvasási joggal.
