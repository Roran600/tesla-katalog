# Návrh modrej farebnej schémy

Tento dokument a súvisiaca maketa sú **návrh**, nie úprava stránky. Zdrojové
súbory webu, jeho obsah, prepínanie tém a funkčnosť zostávajú nezmenené.
Obmedzenie na modrú sa týka rozhrania; archívne skeny sa neprebieľujú ani
nepremaľúvajú. Všetky nižšie uvedené farby sú nepriehľadné farby sRGB.

## Zistenia z existujúceho webu

Úvodná stránka má text, dve tlačidlá a rámovaný sken katalógu. Dokumentácia má
hlavnú a bočnú navigáciu; v nastavení je systémový výber témy a prepínač.
Úvodné farby v `hugo.yaml` sú samostatné pre oba režimy a shortcode ich
premieta do CSS premenných. `assets/css/custom.css` zároveň obsahuje záložné
farby a globálne štýly. Zlato je teraz prítomné napríklad na bodke, tmavom
tlačidle, texte značky a obryse klávesového zamerania. Logo v SVG má modrú
výplň `#153A85`. Predložený návrh tieto prvky farebne zjednocuje bez menenia
ich obsahu. Pôvodná modrá výplň loga by však na navrhnutom tmavom paneli mala
kontrast iba 1,06 : 1; preto nestačí ponechať ju nezmenenú.

## Paleta

| Úloha | Denný režim | Nočný režim |
|---|---|---|
| Hlavné pozadie | `#F1F6FC` | `#142840` |
| Povrch panelu | `#E2EDF9` | `#203C5C` |
| Hlavný text | `#142D50` | `#E2EDFA` |
| Doplnkový text | `#355477` | `#B0C9E6` |
| Odkaz, aktívny prvok | `#174D92` | `#A9D0FF` |
| Hover a stlačenie | `#10386C` | `#D4E8FF` |
| Hranica ovládania | `#56789D` | `#789CC4` |

Žiadne hlavné pozadie nie je čistá biela ani čierna a zlaté ani iné farebné
akcenty nie sú navrhnuté. V makete zostáva pôvodný sken v pôvodných farbách.

## Priradenie prvkom a stavom

- Hlavné pozadie tvorí plochu stránky; povrch panela je pre navigáciu, pätu,
  karty, tabuľky, vyhľadávanie, bloky kódu a informačné panely. Keďže rozdiel
  medzi povrchmi je jemný, ich hranice aj hranice ovládacích prvkov majú mať
  uvedenú farbu hranice; odlíšenie nemá závisieť len od zmeny pozadia.
- Nadpisy a bežný text používajú hlavný text; popisy, menej výrazné navigačné
  položky a sekundárne informácie doplnkový text. Značka a ikony používajú
  farbu odkazu, pokiaľ sú na hlavnom pozadí alebo povrchu panela.
- Symbol Tesla má v návrhu zachovať existujúci tvar a na paneli použiť farbu
  odkazu daného režimu: `#174D92` cez deň a `#A9D0FF` v noci. Pri prípadnej
  realizácii je potrebné zabezpečiť zmenu výplne alebo farebný variant bez
  zmeny kresby; súčasný SVG súbor má pevne nastavenú tmavomodrú výplň. Nové
  kombinácie majú kontrast 7,05 : 1 a 7,06 : 1. Maketa zatiaľ zobrazuje iba
  text značky, preto samotné prefarbenie symbolu nie je vizuálne overené.
- Odkazy používajú farbu odkazu a podčiarknutie; pri hover a stlačení použijú
  príslušnú farbu hover. Aktívna položka navigácie sa navyše označí textovým
  alebo tvarovým indikátorom, napríklad podčiarknutím alebo vyššou váhou písma.
- Primárne tlačidlo má pozadie vo farbe odkazu a text vo farbe hlavného
  pozadia. Pri hover a stlačení sa pozadie zmení na farbu hover, text zostane.
  Sekundárne tlačidlo má pozadie svojho okolia, text vo farbe odkazu a hranicu
  vo farbe hranice; pri hover a stlačení má pozadie panela a text vo farbe
  hover. Neaktívne ovládanie má zostať jednoznačne označené ako neaktívne;
  nespoliehať sa len na farbu alebo odstránenie textu.
- Klávesové zameranie má aspoň 3 px obrys vo farbe odkazu s odstupom 3 px;
  jeho okolie má byť hlavné pozadie alebo povrch panela. Obrys sa nesmie
  prekrývať s inou hranicou či byť orezaný. Úvodná bodka namiesto zlata a rám
  skenu použijú modrú paletu. Upozornenia, chyby a výsledky nie sú rozlíšené
  ďalšou farbou: používajú aj výstižný text, ikonu alebo iné tvarové označenie.
- Pri prípadnej realizácii treba navrhnuté farby zladiť medzi `params.home`,
  záložnými hodnotami CSS a ostatnými štýlmi Hextra. Logo, vypínanie/prístupnosť
  prepínača, navigácia a URL sa touto štúdiou nemenia.

## Kontrola kontrastu

Výpočet používa relatívnu luminanciu sRGB podľa WCAG a pomer
`(Lsvetlejšia + 0,05) / (Ltmavšia + 0,05)`. Hodnoty nižšie sú zaokrúhlené;
pre normálny text sa porovnávajú s 4,5 : 1 a pre hranicu či obrys potrebný na
identifikáciu ovládania s 3 : 1. Tieto hodnoty platia pre uvedené nepriehľadné
kombinácie, nie pre ľubovoľné priehľadnosti či vrstvenie.

| Kombinácia | Denný režim | Nočný režim |
|---|---:|---:|
| Hlavný text / hlavné pozadie | 12,71 : 1 | 12,60 : 1 |
| Hlavný text / panel | 11,65 : 1 | 9,52 : 1 |
| Doplnkový text / hlavné pozadie | 7,20 : 1 | 8,77 : 1 |
| Doplnkový text / panel | 6,60 : 1 | 6,63 : 1 |
| Odkaz / hlavné pozadie | 7,69 : 1 | 9,35 : 1 |
| Odkaz / panel | 7,05 : 1 | 7,06 : 1 |
| Hover text / panel | 9,82 : 1 | 9,01 : 1 |
| Primárne tlačidlo: text / pozadie | 7,69 : 1 | 9,35 : 1 |
| Primárne tlačidlo: text / hover pozadie | 10,71 : 1 | 11,93 : 1 |
| Hranica / hlavné pozadie | 4,23 : 1 | 5,22 : 1 |
| Hranica / panel | 3,88 : 1 | 3,95 : 1 |
| Obrys zamerania / panel | 7,05 : 1 | 7,06 : 1 |

Farba odkazu sa od okolitého textu nemusí dostatočne kontrastne odlišovať,
preto návrh používa aj podčiarknutie. Na všetky uvedené stavy nebola vykonaná
automatická kontrola skutočnej vykreslenej stránky; pri realizácii treba
kontrolovať výsledné farby aj vrstvenie priamo v prehliadači.

## Náhľady a rozsah overenia

`navrh-farebnej-schemy.html` je samostatná ilustračná maketa úvodnej stránky
a dokumentácie v oboch režimoch. Obsahuje príklad panelu, ktorý nie je tvrdením
o existujúcom obsahu webu. `navrh-farieb-desktop.png` a
`navrh-farieb-mobil.png` zachytávajú maketu vytvorenú vo Firefoxe pri šírkach
1440 a 390 px. Pri oboch šírkach sú časti v makete v oboch režimoch súdržné;
na mobile sú stĺpce a úvodné tlačidlá pod sebou. Výšku snímok tvorí vysoký
viewport a následný orez prázdneho priestoru, nejde o konkrétne zariadenie.

Návrh nebol aplikovaný na skutočnú tému, preto nie sú vizuálne overené všetky
jej stránky, komponenty, hover a focus stavy ani skutočné prepínanie režimov
s novými farbami. Nejde o potvrdenie úplnej zhody webu s WCAG. Súčasný web sa
prehliadol spolu so zdrojmi, návrh zachováva jeho obsah a správanie a všetky
podstatné neistoty zostávajú uvedené tu.
