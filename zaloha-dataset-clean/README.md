# Záloha datasetu TESLA

Tento priečinok obsahuje usporiadanú lokálnu zálohu katalógu súčiastok z [teslakatalog.cz](https://www.teslakatalog.cz/). Nie je to hlavný README repozitára; popisuje iba obsah tohto datasetu.

## Štruktúra

- Každá kategória má vlastný priečinok a `index.md`.
- Každá súčiastka má samostatný podpriečinok s `index.md` a dostupnými skenmi.
- Súbory obrázkov a PDF zostávajú pri príslušných súčiastkach; spoločný priečinok `assets/` sa nepoužíva.

## Sprievodné súbory

| Súbor | Účel |
| --- | --- |
| [`STRUCTURE.md`](STRUCTURE.md) | Prehľad kategórií, počtov súčiastok, záznamov puzdier IO, PDF a skenov. |
| [`AUDIT_COMPARISON.md`](AUDIT_COMPARISON.md) | Audit zhody HTML zálohy s webom teslakatalog.cz. Netýka sa binárneho obsahu obrázkov ani PDF. |
| [`MANIFEST.tsv`](MANIFEST.tsv) | Strojovo čitateľný manifest všetkých súborov: cesta, veľkosť v bajtoch a typ. |

## Obsah datasetu

- 10 kategórií a 2 853 unikátnych typov súčiastok.
- 58 samostatných záznamov puzdier integrovaných obvodov, odvodených zo šiestich skenov.
- 21 PDF a 7 486 skenov skopírovaných do priečinkov súčiastok.

## Overenie

Audit zaznamenaný v `AUDIT_COMPARISON.md` porovnal 2 866 HTML stránok lokálnej zálohy s webom bez rozdielov v HTML obsahu po odstránení komentárov HTTrack. Nejde o kontrolný súčet obrázkov ani PDF voči live webu.
