# TESLA katalóg

Archívny projekt pre zachovanie, overovanie a spracovanie obsahu katalógu súčiastok z [teslakatalog.cz](https://teslakatalog.cz/).

Projekt oddeľuje pôvodnú webovú zálohu od vyčisteného, ľahšie prehľadávateľného datasetu. Cieľom je zachovať pôvodné zdroje aj vytvoriť spoľahlivý inventár súčiastok, skenov a súvisiacich dokumentov.

## Obsah repozitára

| Cesta | Obsah |
| --- | --- |
| [`obsah-suciastky.md`](obsah-suciastky.md) | Súhrnný zoznam typov súčiastok podľa kategórií a dostupných prehľadov puzdier. |
| [`zaloha-data/`](zaloha-data/) | Pôvodná HTTrack záloha webu, vrátane HTML, obrázkov, PDF, cache a logu zrkadlenia. Pozri [README zálohy](zaloha-data/README.md). |
| [`zaloha-dataset-clean/`](zaloha-dataset-clean/) | Vyčistený a kategorizovaný archívny dataset s Markdown metadátami, skenmi, auditom a manifestom. Pozri [README datasetu](zaloha-dataset-clean/README.md). |
| [`stranka/`](stranka/) | Priestor vyhradený pre samostatnú prezentačnú stránku projektu. |

## Dataset v skratke

- 10 kategórií a 2 853 unikátnych typov súčiastok.
- 58 samostatných záznamov puzdier integrovaných obvodov.
- 21 PDF a 7 486 skenov v kategorizovanom datasete.
- Audit HTML zálohy porovnal 2 866 stránok s webom bez rozdielov v HTML obsahu po odstránení komentárov HTTrack.

Podrobnosti o štruktúre, audite a všetkých súboroch sú v [`zaloha-dataset-clean/README.md`](zaloha-dataset-clean/README.md).

## Dôležité poznámky

- Priečinky `zaloha-data/` a `zaloha-dataset-clean/` nie sú Hugo obsah ani samostatné webové aplikácie.
- `zaloha-data/` je zdrojový archív; pri jeho úpravách môže dôjsť k strate väzby na pôvodnú webovú zálohu.
- `zaloha-dataset-clean/` je spracovaný dátový balík určený na vyhľadávanie, analýzu a ďalšie spracovanie.
