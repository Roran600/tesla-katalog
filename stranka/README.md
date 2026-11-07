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
