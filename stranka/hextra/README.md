# Tesla katalóg — hextra

Samostatný kompletný Hugo web: vlastná téma, konfigurácia, obsah aj skeny. Všetko potrebné je v tomto priečinku; ostatné tri weby ani pôvodný dataset nie sú potrebné na jeho zostavenie.

Upstream: https://github.com/imfing/hextra  
Commit témy: `f7568498c5ef38c9736549d771427a01bb270bf1`

Zo zložky `stranka/`:

```sh
./hugo.sh hextra build
./hugo.sh hextra serve
```

Alebo priamo v tomto priečinku (Hugo Extended >= 0.166):

```sh
../.bin/hugo --cacheDir ../.cache/hugo/hextra
../.bin/hugo server --cacheDir ../.cache/hugo/hextra --disableFastRender
```

`content/docs/`: všetkých 2 928 Markdown stránok zdrojového datasetu; pridaná je iba domovská stránka a vstup do katalógu. Sekcie majú `_index.md`, súčiastky a púzdra `index.md` s kópiami skenov. Odkazy sú prevedené na webové URL bez `.md`. Súbor `page-map.json` mapuje každý pôvodný záznam na nový súbor a URL. Upstream šablóny a štýly nie sú upravené.
