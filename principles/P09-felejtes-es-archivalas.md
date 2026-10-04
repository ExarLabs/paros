# P09. Felejtés: halványul, archiválódik, nem törlődik

**Elv.** A markdown kis helyet foglal, ezért a törlés nem szükséges. A tudás **elhalványul**, nem tűnik el; ami lezárult, **archiválódik**, nem törlődik.

**Miért.** A törölt tudás nem jön vissza, az archivált igen. Egy tanuló rendszerben a „régi" néha újra fontos lesz.

**Gyakorlat.**
- A tanult szabályok súlya használat nélkül csökken; az alvó szabály kikerül a betöltésből, de megmarad (P05).
- Ami lezárult vagy inaktív: `Archive/` mappa, dátummal és egy mondatos okkal.
- **Kivétel: a biztosan felülírt.** Ami teljesen elavult, és biztosan felülírtuk (például egy skill régi definíciója, amit az új verzió igazoltan lecserélt), törölhető, ha a régi szöveg a verziótörténetben még elérhető.
- A felhasználó által bedobott jegyzetet, feladatot kérdezés nélkül soha nem törlünk, legfeljebb mozgatunk.
- A nagy bináris fájlok (média, átiratok) sorsáról a mentés-elv dönt (P10).

**Ellenőrzés.**
- Van-e `Archive/` mappa és használják-e?
- Töröltek-e az agentek tartalmat a gazda igenje nélkül? (Verziótörténetből vagy git-naplóból.)

**Átvétel.** `Archive/` mappa létrehozása, és a szabály a vault belépőjébe: „törlés helyett archiválás".
