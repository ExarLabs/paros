# PAROS: referencia-rendszer

**PAROS** = Personal Agentic Retrieval Operating System (ejtsd: „PAR-oss"). Egy ember külsősített gondolkodása: markdown-fájlokból álló tudástár, amin AI-agentek dolgoznak, és amely használat közben folyamatosan tanul.

## Ez a repó nem sablon, hanem referencia

Ezt a repót **senki nem használja a vaultja gyökereként**, és senki nem ír bele. Olvasásra van: egy agent átnézi, és a te meglévő (vagy új) Obsidian-vaultodat ezek alapján alakítja át, lépésről lépésre, a te döntéseiddel.

Miért így:
- **Nincs merge-konfliktus.** Mindenki vaultja más (területek, szokások, gépek, eszközök). Ha a repó lenne az alap, minden frissítés ütközne a saját változtatásaiddal.
- **A frissítés tanács, nem felülírás.** Ha új elv vagy jobb megoldás jelenik meg, a repó frissül, és a te agented megnézi, mi változott, és javaslatlistát ad. Te döntesz, mit veszel át.
- **Az elv a lényeg, nem a kód.** A szkriptek eldobhatók és újragenerálhatók; ami marad, az az elv, az indoklás és az ellenőrzés módja.

## Használat

1. Töltsd le a repót egy **külön** könyvtárba, a vaultodon kívül:
   ```bash
   git clone <repo-url> ~/paros-reference
   ```
2. Nyisd meg a saját Obsidian-vaultodat (lehet vadonatúj, üres könyvtár is).
3. Indíts benne egy agentet (Claude Code, Codex vagy más AGENTS.md-t olvasó agent), és mondd neki:
   > Itt van egy referencia-rendszer: `~/paros-reference`. Olvasd el az `AGENTS.md`-jét és az `ADOPT.md`-t, nézd át a vaultomat, és készíts átállási listát.
4. Az agent felméri a vaultot, és egy **átállási listát** ír bele (`PAROS/ADOPTION.md`). Ezt egyenként végigjárjátok; minden lépés előtt megkérdez.
5. Frissítéskor: `git pull` a referencián, és szólj az agentnek: „Nézd meg, mi újat hozott a PAROS-referencia." (lásd `UPGRADE.md`)

## Tartalom

| Hol | Mi |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Az agent belépője (minden platformon). A `CLAUDE.md` erre mutat. |
| [`ADOPT.md`](ADOPT.md) | Az átállás menete: felmérés, lista, lépések, ellenőrzés. |
| [`UPGRADE.md`](UPGRADE.md) | Hogyan vegyél át egy újabb referencia-verziót. |
| [`principles/`](principles/README.md) | Az alapelvek, egyenként: elv, miért, gyakorlat, ellenőrzés, átvétel. |
| [`templates/`](templates/) | Sablonok a vaultodba (belépő, frontmatter, átállási lista). |
| [`kits/`](kits/README.md) | Opcionális referencia-implementációk (keresés, tanulási ciklus, egészség-ellenőrzés, titok-leltár). |
| [`CHANGELOG.md`](CHANGELOG.md) | Verziónként mi változott, és mit érdemes emiatt átnézni. |

## Platformok

Úgy készült, hogy **Claude Code-dal és OpenAI Codex-szel is** működjön, és bármely más agenttel, ami az `AGENTS.md` szabványt olvassa. A platformfüggő részek (hookok, ütemezés) külön, a `kits/` alatt vannak jelölve.

Verzió: lásd [`VERSION`](VERSION).
