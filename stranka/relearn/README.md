# Tesla katalóg — relearn

Samostatný kompletný Hugo web: vlastná téma, konfigurácia, obsah aj skeny. Všetko potrebné je v tomto priečinku; ostatné tri weby ani pôvodný dataset nie sú potrebné na jeho zostavenie.

Upstream: https://github.com/McShelby/hugo-theme-relearn  
Commit témy: `ff1f513a6a1a77f94481eab23d8efe3668fff8b6`

Zo zložky `stranka/`:

```sh
./hugo.sh relearn build
./hugo.sh relearn serve
```

Alebo priamo v tomto priečinku (Hugo Extended >= 0.166):

```sh
../.bin/hugo --cacheDir ../.cache/hugo/relearn
../.bin/hugo server --cacheDir ../.cache/hugo/relearn --disableFastRender
```

`content/docs/`: všetkých 2 928 Markdown stránok zdrojového datasetu; pridaná je iba domovská stránka a vstup do katalógu. Sekcie majú `_index.md`, súčiastky a púzdra `index.md` s kópiami skenov. Odkazy sú prevedené na webové URL bez `.md`. Súbor `page-map.json` mapuje každý pôvodný záznam na nový súbor a URL. Upstream šablóny a štýly nie sú upravené.
