# P01. A tudás markdownban (és JSON-ban) él, minden más származtatott

**Elv.** A tudás forrása a markdown, mert az ember és az AI egyaránt olvassa és írja. Strukturált adatra a JSON is elfogadott forrás. Minden más (adatbázis, keresőindex, gyorsítótár, generált PDF) származtatott, és a forrásból bármikor újraépíthető.

**Miért.** A markdown nem avul el, nem zár be egy alkalmazásba, és bármelyik AI-modell olvassa. Ha az igazság egy adatbázisban élne, a tudás egy eszköz foglya lenne.

**Gyakorlat.**
- Minden fájl **frontmatterrel** kezdődik; a legfontosabb mező a `description` (1-2 mondat a tartalomról): ebből dönti el egy agent, hogy érdemes-e megnyitni. Sablon: `templates/frontmatter.md`.
- Beérkezett eredeti (PDF, xlsx, hang): ha fontos, markdown-kísérő készül (kivonat és hivatkozás), onnantól abból dolgozunk.
- Gépi működési állapot (sor, napló, gyorsítótár) lehet adatbázisban, **ha az elvesztésével semmilyen tudás nem vész el.** A próba: „ha ma törlöm, hiányozni fog-e valami, amit tudni akartam?"
- Minden JSON-adattár mellé rövid markdown-leírás (mi ez, ki írja, ki olvassa).

**Ellenőrzés.**
- Mintavétel: 20 véletlen fájlból hánynak van frontmattere és tartalmi `description`-je?
- Van-e olyan adatbázis vagy alkalmazás, ahol egyedül él valamilyen tudás?

**Átvétel.**
1. Frontmatter-séma rögzítése a vault belépőjében.
2. A meglévő fájlok fokozatos ellátása frontmatterrel (agenttel, kötegekben, a gazda jóváhagyásával).
3. Minden új fájl már frontmatterrel születik.
