# Tesla katalóg — book

Samostatný kompletný Hugo web: vlastná téma, konfigurácia, obsah aj skeny. Všetko potrebné je v tomto priečinku; ostatné tri weby ani pôvodný dataset nie sú potrebné na jeho zostavenie.

Upstream: https://github.com/alex-shpak/hugo-book  
Commit témy: `79af35c876870c6c9f9edede15ef093f4a7bbf8a`

Zo zložky `stranka/`:

```sh
./hugo.sh book build
./hugo.sh book serve
```

Alebo priamo v tomto priečinku (Hugo Extended >= 0.166):

```sh
../.bin/hugo --cacheDir ../.cache/hugo/book
../.bin/hugo server --cacheDir ../.cache/hugo/book --disableFastRender
```

`content/docs/`: všetkých 2 928 Markdown stránok zdrojového datasetu; pridaná je iba domovská stránka a vstup do katalógu. Sekcie majú `_index.md`, súčiastky a púzdra `index.md` s kópiami skenov. Odkazy sú prevedené na webové URL bez `.md`. Súbor `page-map.json` mapuje každý pôvodný záznam na nový súbor a URL. Upstream šablóny a štýly nie sú upravené.
