# Generovanie stránok — `build_sites.py`

Skript `build_sites.py` vygeneruje všetkých štyroch nezávislých Hugových webov (Relearn, Book, Hextra, Hudocs) z jedného zdrojového datasetu `zaloha-dataset-clean/`.

## Čo skript robí

1. **Ověří nemennosť zdrojových dát** — porovná SHA-256 všetkých súborov v `zaloha-dataset-clean/` so záznamom v `reports/source-sha256.json`. Ak sa dataset zmenil, skript sa zastaví.
2. **Prevedie Markdown na Hugo štruktúru** — každý zdrojový súbor dostane nové umístenie podľa kategórie a typu (`_index.md` pre sekcie, `index.md` pre súčiastky a púzdrá). Pôvodné `type` sa uloží ako `dataset_type`, `type` sa nastaví na `docs`.
3. **Prepíše odkazy** — relatívne odkazy `.md` medzi stránkami sa prevedú na webové URL bez prípony `.md`. Odkazy na média (obrázky, skeny, PDF) sa presmerujú na nové cesty.
4. **Skopíruje média** — 7 581 obrázkov a súborov (vrátane 21 PDF) sa zkopírujú do `static/` (statické) resp. `content/` (vlastné balíky stránok). Kopie sa nikdy nespojňujú symlinkami — weby sú plne samostatné.
5. **Vygeneruje konfiguráciu** — `hugo.toml` pre každú tému s vlastnými parametrami (vyhľadávanie, menu, breadcrumbs…).
6. **Vytvorí `page-map.json`** — mapuje každý pôvodný súbor na nový súbor a URL.
7. **Vytvorí domovské a katalógové stránky** — `_index.md` a `docs/_index.md` pre každý web.

Výsledok: každá zložka `relearn/`, `book/`, `hextra/`, `hudocs/` obsahuje kompletný, samostatný Hugo web, ktorý je možné zostaviť a spustiť bez akýchkoľvek ďalších súborov.

## Chyba: „Refusing to overwrite existing content“

```
RuntimeError: Refusing to overwrite existing content: .../stranka/relearn/content
```

### Príčina

Skript má úmyselnú bezpečnostnú kontrolu (zdrojový kód, riadok ~217), ktorá zamedzí prekrytiu existujúceho adresára `content/`. Chráni tak pred náhodným zmazaním manuálne upravených súborov alebo neúplne vygenerovaného obsahu.

Keď `content/` už existuje (napr. z predošlého behu `build_sites.py`), skript odmietne pokračovať a skončí s touto chybou.

### Riešenie

Vymaž existujúce `content/` adresáre pred opätovným spustením:

```bash
cd stranka
rm -rf relearn/content book/content hextra/content hudocs/content
python3 build_sites.py
```

Adresáre `content/` nie sú súčasťou zdrojových dát — vždy sa dá znovu vygenerovať z `zaloha-dataset-clean/`. Zdrojový dataset `zaloha-dataset-clean/` ani `zaloha-data/` sa nemenia.

### Často sa pýtané otázky

**Môžem editovať súbory v `content/`?**
Nedoporučuje sa. Ak chceš meniť obsah, uprav zdrojové súbory v `zaloha-dataset-clean/` a regeneruj cez `build_sites.py`. Manuálne zmeny v `content/` by sa pri ďalšom spustení stratili (alebo by skript odmietol prechovať, až kým adresár neodstráníš).

**Môžem použiť len jednu tému?**
Skript vždy generuje všetky štyri témy naraz. Ak potrebuješ len jeden web, môžeš po vygenerovaní ostatné zmazanie, ale `build_sites.py` sám nie partial build.

**Kde sú logy a reporty?**
- `reports/source-sha256.json` — kontrolné súčty zdrojového datasetu
- `reports/serve-<téma>.log` — logy development serverov
- `reports/browser/` — snímky z browser testov

## Kompletný postup od začiatku

```bash
cd stranka

# 1. Nainštalovať lokálny Hugo (jednorazovo)
python3 setup_hugo.py

# 2. Stiahnuť témy (jednorazovo)
python3 fetch_themes.py

# 3. Vygenerovať všetky 4 weby
python3 build_sites.py

# 4. Spustiť development servery (v rôznych termináloch)
bash hugo.sh relearn serve --port 1411
bash hugo.sh book serve --port 1412
bash hugo.sh hextra serve --port 1413
bash hugo.sh hudocs serve --port 1414

# 5. Spustiť testy
python3 test_builds.py
python3 test_content.py
python3 test_browser.py   # vyžaduje bežiace servery
```

## Odstránenie všetkého generovaného obsahu

Ak chceš úplne vyčistiť a začať znova:

```bash
cd stranka
rm -rf */content */public reports/server-pids.json reports/serve-*.log
python3 build_sites.py
```

`public/` adresáre sa vytvoria až pri `hugo build` alebo `hugo serve` — nie pri `build_sites.py`.