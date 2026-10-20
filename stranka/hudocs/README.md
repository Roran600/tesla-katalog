# Tesla katalóg — hudocs

Samostatný kompletný Hugo web: vlastná téma, konfigurácia, obsah aj skeny. Všetko potrebné je v tomto priečinku; ostatné tri weby ani pôvodný dataset nie sú potrebné na jeho zostavenie.

Upstream: https://github.com/zkreations/hudocs  
Commit témy: `5a7859e66bb904908030d1db0b273f6fa9331a87`

Zo zložky `stranka/`:

```sh
./hugo.sh hudocs build
./hugo.sh hudocs serve
```

Alebo priamo v tomto priečinku (Hugo Extended >= 0.166):

```sh
../.bin/hugo --cacheDir ../.cache/hugo/hudocs
../.bin/hugo server --cacheDir ../.cache/hugo/hudocs --disableFastRender
```

`content/docs/`: všetkých 2 928 Markdown stránok zdrojového datasetu; pridaná je iba domovská stránka a vstup do katalógu. Sekcie majú `_index.md`, súčiastky a púzdra `index.md` s kópiami skenov. Odkazy sú prevedené na webové URL bez `.md`. Súbor `page-map.json` mapuje každý pôvodný záznam na nový súbor a URL. Upstream šablóny a štýly nie sú upravené.
