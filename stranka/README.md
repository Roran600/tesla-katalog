# Štyri samostatné Hugo katalógy Tesla

Toto nie je jeden web s prepínačom tém. Každá z týchto zložiek obsahuje **kompletný, nezávislý Hugo web**:

- `relearn/` — [Hugo Relearn](https://github.com/McShelby/hugo-theme-relearn)
- `book/` — [Hugo Book](https://github.com/alex-shpak/hugo-book)
- `hextra/` — [Hextra](https://github.com/imfing/hextra)
- `hudocs/` — [Hudocs](https://github.com/zkreations/hudocs)

Každý web má vlastné `hugo.toml`, `themes/`, `content/` a pri zostavení aj `public/`. Skeny a PDF sú skutočné kópie, nie odkazy na súbory mimo `stranka/`. Témy používajú pôvodné upstream šablóny a štýly bez vlastného redizajnu. Ich presné verzie sú zaznamenané v `*/themes/upstream.json`.

## Spustenie jedného webu

Zo zložky `stranka/`:

```sh
bash hugo.sh relearn serve --port 1411
```

Pre ostatné zmeňte `relearn` na `book`, `hextra` alebo `hudocs`. Server je na `http://localhost:1313/`.

Pri súčasnom spustení štyroch serverov sú ich porty:

- Relearn: <http://localhost:1411/>
- Book: <http://localhost:1412/>
- Hextra: <http://localhost:1413/>
- Hudocs: <http://localhost:1414/>

Viac webov môžete spustiť v rôznych termináloch na rôznych portoch:

```sh
bash hugo.sh relearn serve --port 1411
bash hugo.sh book serve --port 1412
bash hugo.sh hextra serve --port 1413
bash hugo.sh hudocs serve --port 1414
```

## Zostavenie

```sh
bash hugo.sh relearn build
bash hugo.sh book build
bash hugo.sh hextra build
bash hugo.sh hudocs build
```

Každý príkaz vytvorí statický web vo vlastnom `public/`. Pre produkčné nasadenie nastavte vlastnú adresu:

```sh
bash hugo.sh book build --baseURL https://example.org/
```

Používa sa lokálny Hugo Extended 0.168.0 v `.bin/`, pretože najnovší Relearn vyžaduje novší Hugo než systémová verzia. Skript `setup_hugo.py` stiahne oficiálny archív a overí SHA-256 podľa oficiálneho zoznamu. Systémová inštalácia sa nemení. Cache, pomocné súbory a browser na testovanie sú iba pod `stranka/.cache/`.

## Prenos obsahu

Každý web obsahuje všetkých **2 928 Markdown záznamov** datasetu, vrátane **2 853 súčiastok**, **58 púzdier**, indexov kategórií a dokumentácie. Pridaná je domovská stránka a vstup do katalógu. K dispozícii je všetkých **21 PDF** a **7 558 obrázkov**.

- Kategórie sú Hugo branch bundles (`_index.md`).
- Súčiastky a púzdra sú page bundles (`index.md`) s vlastnými skenmi.
- Pôvodný `type` je uložený ako `dataset_type`; `type: docs` vyberá dokumentačný layout témy.
- Cesty používajú ASCII slugy. Odkazy `.md` sú prevedené na webové URL.
- `page-map.json` v každom webe mapuje pôvodné stránky aj médiá na nové súbory a URL.
- Kópia pôvodného `MANIFEST.tsv` je publikovaná ako `dataset-manifest.tsv`; opisuje pôvodný dataset, nie zmenené Hugo Markdown súbory.
- Pôvodný dataset ani `zaloha-data/` sa nemenia.

## Testy

Zo zložky `stranka/` (Python 3 s `PyYAML` a `playwright`):

```sh
python3 test_builds.py
python3 test_content.py
```

- Build: samostatný Hugo build každej témy, logy a časy.
- Obsah: každá prenesená stránka, kontrolné súčty médií v zdrojovom obsahu aj publikovanom webe, lokálne odkazy a fragmenty všetkých HTML stránok.
- Browser (`python3 test_browser.py`) po spustení developer serverov: desktop 1 440 px, mobil 390 px, kategória, súčiastka, púzdro, načítanie skenov, PDF, vyhľadávanie a JavaScript chyby.
- Nemennosť zdroja: opätovné SHA-256 porovnanie všetkých súborov datasetu s baseline pred prenosom.

Výsledky sú v `reports/`; snímky v `reports/browser/`. Browser testy dočasne používajú port 1313 a postupne na ňom testujú jednotlivé statické weby. Pri testovaní nesmie byť tento port obsadený iným serverom.
