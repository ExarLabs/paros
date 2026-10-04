# P10. Mentés: a szinkron nem mentés (javaslat)

**Elv.** A szinkron (Obsidian Sync, iCloud, Drive, git több gépen) az egyidejűségért van; a mentés az időutazásért. A szinkron a törlést, a rossz agent-írást és a zsarolóvírus titkosította fájlt is szétviszi. Kell egy **egyirányú, verziózott, gépektől független** mentés, és **mentés csak az, amiből már visszaállítottunk.**

**Miért.** Egy agent-rendszerben a tömeges, gyors írás a természetes működés része; egy hibás írás percek alatt minden gépre eljut.

**Gyakorlat.**
- **Csak a pótolhatatlant mentjük:** a vault, a titkok átviteli csomagja és a helyreállító kulcs, a munkamenet-átiratok (ezekből tanul a rendszer), a saját média, a máshol nem létező szkriptek. Ami újraépíthető (index, telepített csomagok, távoli repók), az kimarad.
- **3-2-1:** három példány, két hordozón, egy a házon kívül (például: az élő gépek, egy titkosított pillanatkép-tár egy másik lemezen, és egy titkosított tár a felhőben). A mentés jelszava a titok-mechanizmusba kerül (P07).
- **Próba-visszaállítás** rendszeresen, automatikusan; az egészség-ellenőrzés nézi a legutóbbi pillanatkép korát és a próba sikerét (P11).
- **Egy oldalas helyreállítási útmutató:** új gép nulláról, a mentésből és egy jelmondatból.
- **A szinkron hibáit is figyeljük:** él-e mindkét irányban (a másik gép jelzőfájlja friss-e), van-e csendes duplikáció a fájlokban, maradt-e pusholatlan munka, van-e elég szabad hely.

**Ellenőrzés.**
- Vissza tudod-e állítani a vaultot a tegnapi állapotra? Próbáltad már?
- Mi van csak egy helyen?

**Átvétel.** Egy titkosított, pillanatkép-alapú mentőeszköz (például restic), napi ütemezéssel, helyi és felhős céllal, és havi próba-visszaállítás (kit: `kits/backup`, tervezett).
