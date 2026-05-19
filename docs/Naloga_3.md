# Naloga 3: Sistem za spremljanje triatlonskih rezultatov

## 1 Uvod

V tej nalogi je načrtovan informacijski sistem za spremljanje rezultatov triatlonskih tekmovanj po naročilu stranke Bruno. Sistem je namenjen shranjevanju, obdelavi in prikazu rezultatov iz tekmovanj IRONMAN, IRONMAN 70.3 in UltraTriatlon.

Naloga vključuje analizo testnih podatkov, načrtovanje podatkovne baze, pripravo ER modela ter uvoz podatkov iz CSV datotek v relacijsko bazo.

## 2 Opis projekta

Projekt predstavlja sistem za analizo rezultatov kondicijskih tekmovanj. Podatki se uvažajo iz CSV datotek, nato se shranijo v podatkovno bazo in prikazujejo uporabniku prek dveh vmesnikov:

- administratorskega namiznega vmesnika za upravljanje podatkov,
- uporabniškega namiznega vmesnika za pregled rezultatov in statistik.

Uporabnik lahko pregleduje tekmovanja, rezultate posameznih tekmovanj in statistiko tekmovalcev. Administrator pa lahko podatke ureja, dodaja, briše in preverja njihovo pravilnost.

## 3 Uporabljene tehnologije

- Python za logiko aplikacije in uvoz podatkov,
- Flask za REST API,
- MySQL za podatkovno bazo,
- PyQt5 za namizni administratorski vmesnik,
- requests za komunikacijo namizne aplikacije z API-jem,
- CSV datoteke kot vir testnih podatkov.

## 4 Funkcionalnost sistema

### 4.1 Administratorski vmesnik

- prijava administratorja v sistem,
- uvoz podatkov v bazo iz CSV datotek,
- pregled preteklih tekmovanj,
- filtriranje rezultatov po posameznem tekmovanju,
- dodajanje novega rezultata tekmovalcu,
- urejanje obstoječega rezultata,
- brisanje rezultata,
- iskanje rezultatov po tekmovalčevem imenu,
- izvoz filtriranih podatkov v CSV,
- dnevnik vseh sprememb,
- pregled nepopolnih rezultatov in duplikatov,
- primerjava dveh tekmovalcev.

### 4.2 Uporabniški namizni vmesnik

- pregled seznama vseh tekmovanj,
- pregled rezultatov posameznega tekmovanja,
- iskanje tekmovalca po imenu,
- filtriranje po starostni skupini,
- prikaz osebnih rekordov tekmovalca,
- prikaz povprečnih časov po disciplinah,
- prikaz vseh nastopov posameznega tekmovalca,
- prikaz najboljšega skupnega časa tekmovalca,
- prikaz uvrstitve tekmovalca na posameznem tekmovanju,
- primerjava med dvema tekmovalcema.

## 5 Analiza testnih podatkov

Podatki za nalogo so bili podani v treh glavnih sklopih: IRONMAN, IRONMAN 70.3 in UltraTriatlon. Vsak sklop vsebuje več CSV datotek, kjer posamezna datoteka predstavlja eno tekmovanje oziroma eno dirko v določenem letu.

CSV datoteke vsebujejo atribute, kot so ime tekmovalca, starost, država, uvrstitve, posamezni časi disciplin in skupni čas. Pri analizi podatkov sem ugotovil, da podatki niso popolnoma konsistentni, zato je bil potreben prilagojen uvoz.

Na podlagi analize sem zaključil, da so ključne entitete sistema:

- tekmovalci,
- tekmovanja,
- rezultati.

## 6 Načrt podatkovne baze

Podatkovna baza je zasnovana na treh glavnih entitetah.

### 6.1 Tekmovalci

- ime in priimek,
- starost,
- država.

### 6.2 Tekmovanja

- naziv tekmovanja,
- leto,
- tip tekmovanja,
- lokacija.

### 6.3 Rezultati

- uvrstitve,
- časi po disciplinah,
- skupni čas,
- povezava na tekmovalca,
- povezava na tekmovanje.

## 7 ER diagram

![ER diagram](attachment:dc13449f-b82c-453b-bc2c-5321a0155f5e:image.png)

## 8 Polnjenje podatkovne baze

Po izdelavi ER modela in ustvarjanju tabel v podatkovni bazi je sledilo polnjenje baze s testnimi podatki iz CSV datotek.

Uvoz je izveden v Pythonu. Skripta pregleda vse CSV datoteke v mapah IRONMAN, IRONMAN 70.3 in UltraTriatlon ter podatke zapisuje v bazo. Pri uvozu se najprej preberejo podatki o tekmovanju, kot so naziv, leto, tip tekmovanja in lokacija. Nato se za vsako vrstico CSV preveri, ali tekmovalec že obstaja v bazi. Če še ne obstaja, se doda nov zapis v tabelo tekmovalci. Na koncu se ustvari še zapis v tabeli rezultati.

Ker testni podatki vsebujejo tudi prazne in nepravilne vrednosti, skripta prazna polja pretvori v `NULL`, časovne podatke pa shrani kot besedilo, kjer je to potrebno za lažji uvoz. Poleg tega preverja obstoječe tekmovalce, da se prepreči podvajanje podatkov.

## 9 Statistika polnjenja baze

![Count rezultatov po 50min delovanja](attachment:76cc329e-707f-4cb0-b6d7-c4c727c62deb:image.png)

Count rezultatov po 50min delovanja.

![Count tekmovalcev po 50min delovanja](attachment:6b058212-5194-4f08-83f5-49e547309342:image.png)

Count tekmovalcev po 50min delovanja.

## 10 Validacija in večjezičnost

Pri vnosu in urejanju podatkov sistem preverja obvezna polja ter ustreznost tipov podatkov. Številčna polja morajo biti zapisana kot celo ali decimalno število, prazna neobvezna polja pa se shranijo kot prazna vrednost oziroma `NULL`.

Namizna aplikacija podpira slovenščino in angleščino. Prevajanje uporabniškega vmesnika je izvedeno centralno, zato je mogoče enostavno menjati jezik aplikacije.

## 11 REST povezave

Sistem uporablja REST API za povezavo med administrativnim in uporabniškim namiznim vmesnikom ter strežnikom. Glavne povezave so:

- `POST /auth/login` - prijava administratorja,
- `GET /tekmovanja` - seznam tekmovanj,
- `GET /tekmovanja/<id>/rezultati` - rezultati izbranega tekmovanja,
- `GET /tekmovalci/iskanje?ime=...` - iskanje tekmovalcev,
- `GET /tekmovalci/<id>/nastopi` - nastopi izbranega tekmovalca,
- `POST /rezultati` - dodajanje rezultata,
- `PUT /rezultati/<id>` - urejanje rezultata,
- `DELETE /rezultati/<id>` - brisanje rezultata,
- `GET /validacija/nepopolni` - nepopolni rezultati,
- `GET /validacija/duplikati` - duplikati,
- `GET /primerjava?tekmovalec1=...&tekmovalec2=...` - primerjava dveh tekmovalcev,
- `GET /spremembe` - dnevnik sprememb.

## 12 Installer

Namizna aplikacija se zažene iz datoteke `desktop_app/main.py`. Za distribucijo v okolju Windows je primerna izdelava samostojne `.exe` datoteke s pomočjo orodja PyInstaller, nato pa je mogoče pripraviti še namestitveni paket z orodjem, kot je Inno Setup.

## 13 Zaključek

Na koncu je pripravljen sistem za spremljanje rezultatov triatlonskih tekmovanj. Na začetku sem analiziral zahteve projekta in na tej osnovi določil funkcionalnosti za administracijo in uporabnika. Nato sem pripravil ER model in podatkovno bazo.

Sledi še uvoz podatkov iz CSV datotek, pri čemer je bilo treba upoštevati odstopanja v testnih podatkih. Sistem zato vključuje tudi validacijo podatkov, dnevnik sprememb in večjezični uporabniški vmesnik.
