# Projekt OZRA

## 1 Namen projekta

Namen projekta je izdelava informacijskega sistema za pregled, analizo in upravljanje rezultatov triatlonskih tekmovanj. Sistem obravnava podatke za tekmovanja tipa IRONMAN, IRONMAN 70.3 in UltraTriatlon ter omogoča delo z rezultati tekmovalcev, primerjavo nastopov in pregled statistike.

Projekt je zasnovan tako, da združuje podatkovno bazo, REST API, namizno aplikacijo za administracijo in javni spletni vmesnik za pregled rezultatov.

## 2 Opis rešitve

Rešitev je razdeljena na več logičnih delov:

- uvoz podatkov iz CSV datotek v MySQL bazo,
- Flask strežnik, ki ponuja REST API,
- namizna aplikacija v PyQt5 za administracijo in uporabniški pregled,
- spletni vmesnik v mapi `web_app`, ki se streže iz Flask aplikacije,
- sloj repozitorijev in servisov, ki loči dostop do podatkov od poslovne logike.

Takšna razdelitev olajša vzdrževanje, testiranje in kasnejše razširitve sistema.

## 3 Struktura projekta

- `app.py` je vstopna točka za Flask strežnik in streže spletni vmesnik iz mape `web_app`.
- `uvoz.py` prebere CSV datoteke in jih uvozi v MySQL bazo.
- `db.py` vsebuje nastavitve za povezavo s podatkovno bazo.
- `routes/` vsebuje REST končne točke.
- `services/` vsebuje poslovno logiko in validacijo.
- `repositories/` vsebuje SQL poizvedbe in neposreden dostop do baze.
- `desktop_app/` vsebuje PyQt5 namizno aplikacijo, prevode, konfiguracijo in vizualni slog.
- `web_app/` vsebuje javni spletni pregled rezultatov.
- `docs/` vsebuje poročilo in spremljajočo dokumentacijo.
- `installer/` in `desktop_app/TriatlonAdmin.spec` sta namenjena pripravi namestljive različice programa.

## 4 Uporabljene tehnologije

- Python za strežnik, uvoz podatkov in namizno aplikacijo,
- Flask za REST API in streženje spletnega vmesnika,
- flask-cors za dovoljenje dostopa iz odjemalcev,
- MySQL za shranjevanje podatkov,
- mysql-connector-python za povezavo z bazo,
- PyQt5 za administratorski in uporabniški namizni vmesnik,
- requests za komunikacijo namizne aplikacije z API-jem,
- HTML, CSS, JavaScript in Bootstrap 5 za spletni vmesnik,
- PyInstaller za izdelavo samostojne izvršljive datoteke.

## 5 Podatkovni model

Osrednje entitete sistema so:

- `admini` za prijavo administratorja,
- `tekmovanja` za podatke o posameznih tekmah,
- `tekmovalci` za osnovne podatke o športnikih,
- `rezultati` za rezultate posameznih nastopov,
- `spremembe` za dnevnik sprememb v bazi.

Tabela `rezultati` je povezana s tabelama `tekmovalci` in `tekmovanja`, tabela `spremembe` pa beleži operacije nad podatki in lahko vsebuje sklic na administratorja. Tak model omogoča pregled nad tekmovanji, nastopi in zgodovino sprememb.

## 6 Funkcionalnosti sistema

### 6.1 Administratorski namizni vmesnik

- prijava administratorja ime admin geslo 1234,
- pregled tekmovanj in rezultatov,
- dodajanje, urejanje in brisanje rezultatov,
- iskanje tekmovalcev po imenu,
- prikaz nastopov izbranega tekmovalca,
- prikaz podatkov o nepopolnih rezultatih,
- prikaz duplikatov,
- primerjava dveh tekmovalcev,
- pregled dnevnika sprememb,
- izvoz rezultatov v CSV,
- preklop med slovenščino in angleščino.

### 6.2 Javni uporabniški vmesnik

- pregled vseh tekmovanj,
- pregled rezultatov izbranega tekmovanja,
- iskanje tekmovalcev po imenu,
- filtriranje tekmovalcev po starostni skupini,
- prikaz statistike izbranega tekmovalca,
- prikaz najboljšega časa,
- prikaz števila nastopov,
- prikaz povprečij po disciplinah,
- primerjava dveh tekmovalcev,
- preklop jezika.

### 6.3 Spletni vmesnik

Spletni vmesnik omogoča pregled tekmovanj, rezultatov, iskanje tekmovalcev in primerjavo rezultatov v brskalniku. Na voljo je tudi preklop med slovenščino in angleščino.

## 7 REST API

Glavne poti API-ja so:

- `POST /auth/login` za prijavo administratorja,
- `GET /tekmovanja` za seznam tekmovanj,
- `GET /tekmovanja/<id>` za posamezno tekmovanje,
- `GET /tekmovanja/<id>/rezultati` za rezultate tekmovanja,
- `GET /tekmovalci/iskanje?ime=...` za iskanje tekmovalcev,
- `GET /tekmovalci/<id>` za podatke o tekmovalcu,
- `GET /tekmovalci/<id>/nastopi` za nastope tekmovalca,
- `GET /tekmovalci/<id>/najboljsi-cas` za najboljši čas tekmovalca,
- `POST /rezultati` za dodajanje rezultata,
- `PUT /rezultati/<id>` za urejanje rezultata,
- `DELETE /rezultati/<id>` za brisanje rezultata,
- `GET /validacija/nepopolni` za nepopolne rezultate,
- `GET /validacija/duplikati` za duplikate,
- `GET /primerjava?tekmovalec1=...&tekmovalec2=...` za primerjavo dveh tekmovalcev,
- `GET /spremembe` za dnevnik sprememb.

## 8 Uvoz podatkov

Uvoz podatkov je izveden v datoteki `uvoz.py`. Skripta pregleda CSV datoteke v mapi s testnimi podatki, iz imena datoteke določi tekmovanje, nato pa za vsako vrstico ustvari zapis tekmovalca in rezultata.

Pri uvozu skripta:

- čisti prazne in neveljavne vrednosti,
- pretvori številčne podatke v ustrezne tipe,
- preprečuje podvajanje tekmovalcev in tekmovanj,
- združuje podatke iz različnih formatov CSV datotek,
- batchira vstavljanje rezultatov za hitrejši uvoz.

Pred zagonom je treba v `uvoz.py` nastaviti pravilno pot do CSV datotek.

## 9 Namestitev programa

Ker v projektu ni datoteke `requirements.txt`, je odvisnosti treba namestiti ročno. Priporočen postopek na Windows je naslednji:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask flask-cors mysql-connector-python pyqt5 requests pyinstaller
```

Nato je treba:

- zagnati MySQL strežnik,
- ustvariti bazo `mydb`,
- preveriti podatke za prijavo v `db.py` in po potrebi prilagoditi naslov, uporabnika, geslo in port,
- preveriti, ali je v `uvoz.py` pravilno nastavljena pot do CSV virov.

## 10 Zagon programa

1. Najprej uvozi podatke v bazo:

```powershell
python uvoz.py
```

2. Zaženi Flask strežnik in spletni vmesnik:

```powershell
python app.py
```

3. Odpri spletni pregled v brskalniku na naslovu `http://127.0.0.1:5000`.

4. Zaženi namizno aplikacijo:

```powershell
python desktop_app/main.py
```

5. V namizni aplikaciji se lahko prijavi administrator ali pa se odpre javni uporabniški pogled.

## 11 Uporaba programa

### 11.1 Administratorski potek

Administrator se najprej prijavi v sistem. Po prijavi dobi dostop do zavihkov za tekmovanja, tekmovalce, primerjavo, validacijo in spremembe. V zavihku tekmovanj lahko izbira posamezna tekmovanja in upravlja rezultate. V zavihku tekmovalcev lahko išče športnike in prikazuje njihove nastope. V zavihku validacije lahko pregleda nepopolne zapise in duplikate, v zavihku sprememb pa zgodovino operacij.

### 11.2 Uporabniški potek

Uporabnik brez prijave lahko pregleduje javni pogled, kjer izbira tekmovanje, gleda rezultate, išče tekmovalce, preverja statistiko posameznega tekmovalca in primerja dva športnika med seboj.

### 11.3 Spletni potek

V brskalniku je na voljo enostaven javni pregled rezultatov. Uporabnik lahko preklaplja med zavihki tekmovanj, tekmovalcev in primerjave, filtrira rezultate po diviziji ter preklaplja jezik vmesnika.

## 12 Priprava izvršljive datoteke

Za izdelavo samostojne izvršljive datoteke je pripravljen PyInstaller opis `desktop_app/TriatlonAdmin.spec`. S tem je mogoče namizno aplikacijo zapakirati v `.exe` datoteko za Windows distribucijo.

## 13 Zaključek

Projekt predstavlja celovito rešitev za delo s triatlonskimi rezultati. Vključuje uvoz podatkov iz CSV datotek, strukturirano podatkovno bazo, REST API, administratorski in uporabniški namizni vmesnik ter javni spletni pregled.

Rešitev podpira pregled tekmovanj, analizo rezultatov, validacijo podatkov, dnevnik sprememb, primerjavo tekmovalcev in večjezičnost, zato je primerna kot zaključena programska rešitev za prikaz in obdelavo triatlonskih podatkov.


