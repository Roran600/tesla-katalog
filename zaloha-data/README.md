# Pôvodná HTTrack záloha

Tento priečinok je neupravená lokálna záloha webu [teslakatalog.cz](https://teslakatalog.cz/), vytvorená nástrojom HTTrack 16. októbra 2026.

> Toto **nie je Hugo obsah ani samostatný webový projekt**. Ide o zdrojovú archivovanú kópiu, z ktorej vznikol spracovaný dataset v `../zaloha-dataset-clean/`.

## Obsah

| Cesta alebo súbor | Účel |
| --- | --- |
| [`teslakatalog.cz/`](teslakatalog.cz/) | Zrkadlené HTML stránky, obrázky, PDF a ostatné zdroje hlavného katalógu. |
| [`hts-cache/`](hts-cache/) | Pracovná cache HTTracku. Môže obsahovať technické a citlivé údaje; nezdieľajte ju bez kontroly. |
| [`hts-log.txt`](hts-log.txt) | Záznam priebehu zrkadlenia, upozornení a chýb pri sťahovaní. |
| [`index.html`](index.html) | Lokálny rozcestník vygenerovaný HTTrackom. |
| [`www.belza.cz/`](www.belza.cz/) a [`www.ferity.cz/`](www.ferity.cz/) | Súbory zachytené pri prechádzaní externých odkazov z katalógu. |
| `backblue.gif`, `fade.gif` | Grafika lokálneho rozcestníka HTTracku. |

## Dôležité poznámky

- Zachovávajte túto zálohu ako zdrojový archív; nemeníte v nej HTML ani cesty súborov bez dôvodu.
- Neprítomnosť súboru nemusí znamenať, že na pôvodnom webe neexistoval: zrkadlenie môže naraziť na HTTP chyby, presmerovania alebo nedostupný externý zdroj.
- Konkrétne upozornenia a chyby sú zaznamenané v `hts-log.txt`; napríklad externý PDF súbor z `www.ferity.cz` vrátil HTTP 403.
- Spracovaný, kategorizovaný a auditovaný obsah je v susednom priečinku [`../zaloha-dataset-clean/`](../zaloha-dataset-clean/).

## Lokálne prehliadanie

Otvorte `index.html` v prehliadači. HTTrack prepisuje odkazy pre lokálne prehliadanie, preto ich neberte ako pôvodné produkčné URL adresy.
