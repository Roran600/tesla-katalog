# Tesla katalóg – stránka

## Spustenie a zostavenie

Priečinok `stranka/` je samostatný projekt Hugo s témou Hextra ako Hugo
modulom. Potrebuje Hugo a Go kompatibilné s verziou uvedenou v `go.mod`;
pri prvom získaní modulu môže byť potrebné sieťové pripojenie. Príkazy
spúšťajte z priečinka `stranka/`:

```sh
hugo server
```

Na vytvorenie statickej stránky použite `hugo`. Výstup sa štandardne uloží
do `public/`. Adresu nasadenia možno nastaviť v `hugo.yaml` alebo pri
zostavení napríklad pomocou `hugo --baseURL https://example.org/tesla/`.

**Font sa pri bežnom zostavení stránky negeneruje.** Hugo skopíruje už
pripravený `static/fonts/tesla-katalog-display.woff2` do výstupu. Python,
FontTools ani nástroje WOFF2 preto na bežný Hugo build nie sú potrebné.

## Dokumentácia a blog

Sekcie `content/docs/` a `content/blog/` používajú natívne šablóny Hextra
pre dokumentáciu a blog. Dokumentácia má na desktope strom stránok a obsah
aktuálnej stránky; na mobile je navigácia dostupná cez menu v hlavičke. Blog
zobrazuje príspevky podľa dátumu, ponúka ich stránkovanie a [RSS kanál](content/blog/_index.md).
Spoločná paleta a úpravy Hextra sú v `assets/css/custom.css`; slovenské texty
niektorých ovládacích prvkov sú v `i18n/sk.yaml`.

### Pridanie a údržba obsahu

Text značky, položiek hlavného menu, copyrightu a názvy dokumentačných
stránok, sekcií a blogových článkov môžu obsahovať priamo Unicode emoji
alebo skratku Huga, napríklad `:wrench:`. V zobrazení sa nahrádza iba
známa skratka; emoji sa nepridávajú automaticky. Zoznam skratiek uvádza
[Hugo](https://gohugo.io/quick-reference/emojis/). Tieto polia sú obyčajný
text, nie HTML ani Markdown. Zdrojový export Markdown zachováva pôvodný zápis.
Úpravy šablón a vyhľadávacieho indexu vychádzajú z Hextra 0.13.0; pri jej
aktualizácii ich treba porovnať s novou verziou témy.

Na priebežnú skúšku sú emoji výslovne vložené do položky `Docs` v `hugo.yaml`,
do názvu sekcie `content/docs/zaklady/_index.md`, stránky
`content/docs/zaklady/ukazka.md` a článku `content/blog/ukazka-archivu.md`.
Príklady používajú priamy Unicode aj skratky `:books:` a `:sparkles:`;
možno ich odstrániť alebo zmeniť bez zmeny adresy stránok.

- Dokumentačné sekcie majú `_index.md`, jednotlivé stránky vlastný súbor
  `.md`. Strom navigácie vychádza zo štruktúry obsahu a poradia `weight`.
  Polia `prev` a `next` vo front matter určujú prechody medzi súčasnými
  dokumentačnými stránkami; pri zmene poradia upravte aj susedné stránky.
- Blogový príspevok patrí do `content/blog/`. Front matter môže obsahovať
  `title`, `date`, `description` a `authors`; dátum určuje poradie vo výpise.
- Pre kontextové menu Hextra s kopírovaním Markdownu nastavte na jednotlivej
  stránke `outputs: [html, markdown]` a `contextMenu: true`. Na sekcii, ktorá
  má zachovať aj RSS výstup, použite `outputs: [html, rss, markdown]`.
  Skopírovaný zdroj môže obsahovať Hugo shortcody.
- Interné odkazy v obsahu používajú `relref`, aby fungovali aj pri nasadení
  do podpriečinka. Obrázky a iné verejné súbory patria do `static/`.

`content/docs/zaklady/ukazka.md` a oba články blogu s názvom „Ukážka“ sú
testovací obsah, nie katalógové záznamy. Po doplnení skutočného obsahu ich
možno odstrániť; treba pritom upraviť odkazy na ne aj príslušné `prev`/`next`.

### Overenie zmien

Zostavte web do samostatného adresára, aby ste neprepísali prípadné zmeny v
`public/`, a overte aj nasadenie pod URL podcestou:

```sh
hugo --destination /tmp/opencode/tesla-site-root
hugo --baseURL https://example.org/tesla/ --destination /tmp/opencode/tesla-site-subpath
node scripts/test_footer_year.js /tmp/opencode/tesla-site-root
python3 scripts/test_emoji.py
```

Test emoji vytvorí dočasnú kópiu projektu, vloží do nej samostatné skúšobné
hodnoty a overí zostavený HTML, escapovanie textu, vyhľadávací index, RSS,
Markdown a odkazy s podcestou. Nezapisuje testovacie údaje do obsahu ani do
`public/`. Používa existujúce ukážkové stránky a názov položky `Docs 📚`;
pri ich premenovaní treba upraviť aj test. Vizuálnu kontrolu v prehliadači
ani kontrolu obsahu schránky nenahrádza.

Skontrolujte odkazy, obrázky a Markdown výstupy, vrátane prefixu `/tesla/`
pri podceste. V prehliadači overte indexy a detaily dokumentácie aj blogu,
menu, vyhľadávanie, obsah stránky, prechody medzi článkami, kopírovanie a RSS.
Porovnajte mobil a desktop vo svetlom aj tmavom režime; po zmene spoločných
štýlov skontrolujte aj úvodnú stránku, hlavičku a pätičku. `/tmp/opencode`
je adresár tohto vývojového prostredia; inde zvoľte vhodný dočasný cieľ.

## Pätička

Texty a prvý rok copyrightu sa nastavujú v `hugo.yaml` pod `params.footer`.
Vlastný partial `layouts/_partials/footer.html` vychádza z Hextra 0.13.0
a zobrazuje nastavený copyright pod kreditom témy. Pri aktualizácii témy
treba porovnať tento partial s novou verziou pôvodnej pätičky.
Hook `layouts/_partials/custom/footer.html` načítava `static/js/footer-year.js`:
rok sa riadi miestnym dátumom návštevníka a aktualizuje sa pri otvorení,
po návrate na kartu a približne raz za hodinu aj bez nového buildu. Pri
vypnutom alebo blokovanom JavaScripte zostane rok zostavenia; nesprávne
hodiny návštevníka môžu zobraziť nesprávny rok. Na overenie logiky spustite
`node scripts/test_footer_year.js` po zostavení webu.

## Podklady k dizajnu

Priečinok `dizajn/` obsahuje [návrh farebnej schémy](dizajn/navrh-farebnej-schemy.md),
[samostatnú maketu](dizajn/navrh-farebnej-schemy.html) a jej snímky pre
[desktop](dizajn/navrh-farieb-desktop.png) a [mobil](dizajn/navrh-farieb-mobil.png).
Sú to dokumentačné podklady, nie súčasť Hugo webu ani vstupy jeho zostavenia.
Maketa používa existujúci katalógový sken z `static/images/`.

## Nastavenie úvodnej stránky

Súbor `content/_index.md` používa layout Hextra `hextra-home` a vkladá vlastný
shortcode `tesla-home`. Jeho šablóna je v `layouts/_shortcodes/tesla-home.html`.
Obsah a vzhľad úvodného bloku sa nastavujú v `hugo.yaml` pod `params.home`:

- `badge`, `headline` a `subtitle` určujú štítok, nadpis a podnadpis.
  Prázdny odkaz štítku ho ponechá neklikateľný; `headline.breakLine` zapína
  pevné zalomenie nadpisu medzi jeho dvoma časťami.
- `cta` a `secondaryCta` určujú text a cieľ oboch tlačidiel.
  `secondaryCta.showArrow` zapína šípku druhého tlačidla.
- `image` určuje cestu k obrázku, alternatívny text a rozmery zdrojového
  súboru v pixeloch. Obrázok musí byť dostupný v `static/`.
- `responsive` určuje šírky zlomov v pixeloch pre stĺpce a tlačidlá.
- `style` obsahuje CSS hodnoty rozloženia, typografie, tlačidiel, obrázka a
  jeho rámu. Hodnoty zapisujte ako reťazce vrátane potrebných CSS jednotiek.
- `light` a `dark` nastavujú farby a tieň zvlášť pre svetlý a tmavý režim.

Jednotlivé možnosti sú okomentované priamo v `hugo.yaml`. Predvolené hodnoty
vzhľadu pri vynechaní položiek sú v `assets/css/custom.css`; predvolené
hodnoty obrázka a šírok zlomov sú v šablóne shortcode.

### Výmena obrázka

Uložte obrázok napríklad ako `static/images/novy-obrazok.jpg` a v existujúcej
časti `params.home` upravte:

```yaml
image:
  path: "images/novy-obrazok.jpg" # Cesta vzhľadom na static/.
  alt: "Opis obsahu obrázka"
  width: 1200  # Skutočná šírka zdrojového súboru v pixeloch.
  height: 800  # Skutočná výška zdrojového súboru v pixeloch.
```

Výrez možno upraviť cez `style.image-ratio`, `style.image-fit` a
`style.image-position`. Po zmene skontrolujte čitateľnosť, svetlý aj tmavý
režim a rozloženie na veľkej aj malej obrazovke. Správanie pri nasadení do
podpriečinka overíte zostavením napríklad takto:

```sh
hugo --baseURL https://example.org/tesla/ --destination /tmp/opencode/tesla-site-check
```

Vo výslednej stránke skontrolujte, že odkazy aj obrázok používajú prefix
`/tesla/`. Adresár `/tmp/opencode` je určený pre toto vývojové prostredie;
inde použite vhodný dočasný cieľový adresár. Tento príkaz nemení nastavenú
`baseURL` v `hugo.yaml`.

## Font hlavičky

Zdrojom veľkých písmen fontu je `font-sources/tesla-slovak-uppercase-vector.svg`.
Je to pracovná kópia predlohy umiestnená priamo v projekte stránky, takže na
generovanie netreba priečinok `grafika/`. Zmeny v pôvodnej predlohe sa sem
neprenášajú automaticky; po jej úprave treba pracovnú kópiu aktualizovať.
Generátor preberá obrysy jednotlivých písmen; dvojice DZ, DŽ a CH sa v texte
skladajú z jednotlivých znakov. Malé písmená sa zámerne zobrazujú ako veľké:
ide o titulkový font, nie o plnohodnotný font na súvislý text. Číslice,
interpunkcia a doplnkové české znaky Ě, Ř a Ů pochádzajú z generátora.

Font treba znovu vygenerovať iba po zmene pracovnej predlohy alebo generátora.
Na generovanie je potrebný Python s balíkom `fonttools` a `woff2_compress`;
test navyše potrebuje `woff2_decompress` (nástroje z balíka WOFF2). Sú to
systémové závislosti, nie súčasť tohto priečinka. Zo zložky `stranka/` spustite:

```sh
python3 scripts/generate_tesla_display_font.py
python3 scripts/test_tesla_display_font.py
```

Generátor vytvorí oba súbory `static/fonts/tesla-katalog-display.ttf` a
`static/fonts/tesla-katalog-display.woff2`. Po zmene predlohy ich treba
znovu vygenerovať a vizuálne overiť; pri zmene štruktúry SVG môže byť potrebné
upraviť mapovanie alebo importér.
