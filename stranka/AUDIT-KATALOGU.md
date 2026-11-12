# Priebežné overenie katalógu

## Metóda a obmedzenia

Základom sú súbory `zaloha-dataset-clean/`. Detail každej nižšie uvedenej
súčiastky bol načítaný z `https://teslakatalog.cz/<označenie>.html` a obsah
HTML prvku `td.forContent` porovnaný s pôvodnou HTTrack kópiou po normalizácii
bieleho miesta. Certifikát webu bol expirovaný: spojenie neoverovalo identitu
servera. Nejde o porovnanie všetkého HTML ani o overenie online bajtov skenov.
Zhodu skopírovaných skenov s datasetom a s originálnymi súbormi v HTTrack
archíve sme overili SHA-256. Archívy ostali nezmenené.

Po prerušení zostavenia z nedostatku pamäte boli opakovane porovnané všetky
záznamy, 7 486 skenov, 58 strán puzdier a 21 PDF s datasetom. Konečný build
prebehol samostatne s obmedzením paralelizmu a výstupom na disk; kontrola
2 924 katalógových HTML stránok našla 140 905 interných odkazov a obrázkov
bez chýbajúceho cieľa. Test sa týka existencie ciest, nie obsahu externých
stránok ani fragmentov odkazov.

Vzorky katalógovej kategórie a detailu boli zobrazené na mobile a desktope,
v oboch farebných režimoch. Vyhľadávanie `KT508/50` otvorilo správny detail;
odkaz a dostupnosť Markdown exportu boli overené. V izolovanom prehliadači
Playwright sa po stlačení tlačidla prečítala schránka a overil sa očakávaný
obsah exportu detailu, kategórie aj stránky s PDF.

## Termistory Pramet

- 24 záznamov a 37 skenov v datasete aj na novej stránke.
- Živý zoznam `https://teslakatalog.cz/termistor.php` obsahuje všetkých 24
  označení zo zálohy. Všetky detailové stránky mali zhodný hlavný obsah s
  HTTrack HTML; neoverené stránky: žiadne. Kontrolované: NR105, NR107, NR121,
  NR302, NR321, NR331, NR341, NR342, NR351, NR352, NR371, NR380, NR506,
  NR510, NR511, NR516, NR522, NR531, NR536, NR541, NR551, PR301, PR302, PR304.
- Výstup s podcestou obsahoval všetky záznamy a skeny; ich bajty a odkazy boli
  porovnané s datasetom. Rozdiely: žiadne v rozsahu uvedených kontrol.

## Tlmivky, filtre

- 20 záznamov a 65 skenov v datasete aj na novej stránke.
- Všetky detailové stránky mali zhodný hlavný obsah s HTTrack HTML; neoverené
  stránky: žiadne. Kontrolované: TD100, TD101, TD102, TD103, TD104, WK05003,
  WK85203, WN68201, WN68202, WN68203, WN68205, WN68206, WN68207, WN68208,
  WN68209, WN68211, WN68212, WN68213, WN68218, WN85202.
- Výstup s podcestou obsahoval všetky záznamy a skeny; ich bajty a odkazy boli
  porovnané s datasetom. Rozdiely: žiadne v rozsahu uvedených kontrol.

## Rezistory

- 203 záznamov a 945 skenov v datasete aj na novej stránke. Výstup pod
  podcestou má všetky súbory; ich SHA-256 sa zhoduje s datasetom.
- Všetky detailové stránky boli porovnané s HTTrack HTML; [výsledky podľa
  jednotlivých záznamov](AUDIT-rezistory.tsv): 202 zhôd, jeden rozdiel,
  žiadne nedostupné detaily.
- WK65005: pôvodný HTML archív obsahuje tretí neplatný obrázok s `src="#"`,
  aktuálny web `src=""`. Dataset má dva skutočné skeny; oba sú zachované.
  Nejde o dôkaz nového alebo chýbajúceho skenu.
- Pri záznamoch s viac ako jedným katalógovým zdrojom sa vzťah medzi označením
  vydania a skenom doplnil podľa HTML archívu po kontrole bajtov skenu.

## Tyristory, triaky

- 100 záznamov a 264 skenov; SHA-256 a odkazy výsledného webu pod podcestou
  boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri viacerých
  vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 100 overených detailov a ich URL](AUDIT-tyristory.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Displeje, LED

- 175 záznamov a 285 skenov; SHA-256 a odkazy výsledného webu pod podcestou
  boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri viacerých
  vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 175 overených detailov a ich URL](AUDIT-displeje.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Kryštály, oscilátory

- 247 záznamov a 553 skenov; SHA-256 a odkazy výsledného webu pod podcestou
  boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri viacerých
  vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 247 overených detailov a ich URL](AUDIT-krystaly.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Kondenzátory

- 527 záznamov a 1 791 skenov; SHA-256 a odkazy výsledného webu pod
  podcestou boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri
  viacerých vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 527 overených detailov a ich URL](AUDIT-kondenzatory.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Diódy, varikapy

- 459 záznamov a 1 007 skenov; SHA-256 a odkazy výsledného webu pod
  podcestou boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri
  viacerých vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 459 overených detailov a ich URL](AUDIT-diody.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Tranzistory

- 395 záznamov a 772 skenov; SHA-256 a odkazy výsledného webu pod podcestou
  boli porovnané s datasetom. Vzťah medzi vydaním a skenom sa pri viacerých
  vydaniach doplnil podľa HTML archívu po kontrole bajtov.
- [Zoznam 395 overených detailov a ich URL](AUDIT-tranzistory.tsv): všetky
  dostupné, hlavný obsah sa zhoduje s HTML archívom. Rozdiely: žiadne v
  rozsahu uvedených kontrol.

## Integrované obvody a puzdrá

- 703 súčiastok a 1 767 skenov; SHA-256 a odkazy webu pod podcestou boli
  porovnané s datasetom. [Zoznam 703 detailov a výsledkov](AUDIT-integrovane-obvody.tsv):
  všetky dostupné, hlavný HTML obsah sa zhoduje s archívom.
- Záznamy MHB1012 a MHB1012C: pôvodné HTML dvakrát vkladá ten istý sken
  `io5/299.jpg`; záloha uchováva päť unikátnych skenov, nie šesť vložení.
  Na novej stránke sa zachováva päť skenov podľa zálohy.
- 58 samostatných záznamov puzdier a ich skeny boli porovnané s datasetom a
  archívom. Šesť strán [iop1.jpg](https://teslakatalog.cz/io0/iop1.jpg),
  [iop2.jpg](https://teslakatalog.cz/io0/iop2.jpg),
  [iop3.jpg](https://teslakatalog.cz/io0/iop3.jpg),
  [iop4.jpg](https://teslakatalog.cz/io0/iop4.jpg),
  [iop5.jpg](https://teslakatalog.cz/io0/iop5.jpg),
  [iop6.jpg](https://teslakatalog.cz/io0/iop6.jpg) sa bajtovo zhodovalo
  s archívom. Živý web nemá osobitné HTML detaily pre 58 označení. Vizuálne
  porovnanie šiestich strán 242–247 so zoznamom zálohy potvrdilo 58 označení
  a ich strany. Na strane 244 je pri označení `IO15/2` vynechaná pomlčka;
  záloha aj nová stránka používajú normalizovaný zápis `IO-15/2`.

## Zoznamy kategórií

Aktuálnych desať stránok kategórií obsahovalo rovnaké množiny odkazov na HTML
detaily ako dataset (2 853 typov); nezistené chýbajúce ani navyše uvedené
odkazy. Zdroje kategórií sú v `index.md` príslušných priečinkov datasetu.

## PDF dokumenty

- Všetkých 21 dokumentov bolo skopírovaných z `Ke stažení`; SHA-256 ich kópií
  v statických súboroch aj vo výstupe s podcestou sa zhoduje s datasetom.
- Aktuálna stránka `https://teslakatalog.cz/ke-stazeni.php` uvádza 21 odkazov;
  všetky zdroje vrátili na požiadavku HEAD stav 200 a veľkosti zodpovedajúce
  datasetu. Jeden zdroj je `www.ferity.cz`, ostatné `teslakatalog.cz/download`.
  Online bajty PDF sme nesťahovali ani neporovnávali; certifikát pôvodného
  webu pri kontrole nebol overený. Prípadná zmena obsahu pri rovnakej veľkosti
  by sa touto kontrolou nezistila.
