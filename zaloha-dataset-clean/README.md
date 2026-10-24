# Archívny dataset TESLA

Tento priečinok obsahuje usporiadanú lokálnu zálohu katalógu súčiastok z [teslakatalog.cz](https://www.teslakatalog.cz/).

> Tento priečinok **nie je Hugo stránka ani Hugo obsah**. Je to samostatný archívny dátový balík určený na prehliadanie, kontrolu a ďalšie spracovanie mimo generovania webu.

Nejde ani o hlavný README repozitára; tento dokument vysvetľuje výhradne dataset v tomto priečinku.

## Organizácia dát

- Každá kategória má vlastný priečinok a opisný súbor `index.md`.
- Každá súčiastka má samostatný podpriečinok s `index.md` a dostupnými skenmi.
- Súbory `index.md` sú metadata v Markdown formáte, nie Hugo stránky.
- Obrázky a PDF zostávajú pri príslušných súčiastkach; spoločný priečinok `assets/` sa nepoužíva.

## Sprievodné súbory

| Súbor | Účel |
| --- | --- |
| [`OBSAH-SUCIASTKY.md`](OBSAH-SUCIASTKY.md) | Čitateľný úplný inventár typov súčiastok podľa kategórií, vrátane dostupných spoločných prehľadov puzdier. Nie je to Hugo obsah. |
| [`STRUCTURE.md`](STRUCTURE.md) | Prehľad kategórií, počtov súčiastok, záznamov puzdier IO, PDF a skenov. |
| [`AUDIT_COMPARISON.md`](AUDIT_COMPARISON.md) | Audit zhody HTML zálohy s webom teslakatalog.cz. Netýka sa binárneho obsahu obrázkov ani PDF. |
| [`MANIFEST.tsv`](MANIFEST.tsv) | Strojovo čitateľný manifest všetkých súborov: cesta, veľkosť v bajtoch a typ. |

## Rozsah datasetu

- 10 kategórií a 2 853 unikátnych typov súčiastok.
- 58 samostatných záznamov puzdier integrovaných obvodov, odvodených zo šiestich skenov.
- 21 PDF a 7 486 skenov skopírovaných do priečinkov súčiastok.

## Overenie zálohy

Audit zaznamenaný v `AUDIT_COMPARISON.md` porovnal 2 866 HTML stránok lokálnej zálohy s webom bez rozdielov v HTML obsahu po odstránení komentárov HTTrack. Nejde o kontrolný súčet obrázkov ani PDF voči live webu.

## Použitie

Dataset možno prehľadávať priamo podľa priečinkov, spracovať pomocou `MANIFEST.tsv` alebo analyzovať Markdown metadata a priložené skeny. Je nezávislý od konfigurácie a build procesu hlavného repozitára.
