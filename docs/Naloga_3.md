# Naloga 3

## Uporabljene tehnologije

- Python
- Flask za REST API
- MySQL za hranjenje podatkov
- PyQt5 za namizno aplikacijo
- `requests` za povezavo namizne aplikacije z API-jem

## Zasloni

- Prijavni zaslon: prijava administratorja in izbira jezika.
- Zavihek Tekmovanja: prikaz tekmovanj in rezultatov za izbrano tekmovanje.
- Zavihek Tekmovalci: iskanje tekmovalcev in pregled njihovih nastopov.
- Zavihek Primerjava: primerjava dveh tekmovalcev po številu nastopov in najboljšem času.
- Zavihek Validacija: prikaz nepopolnih zapisov in duplikatov.
- Zavihek Spremembe: pregled dodajanja, urejanja in brisanja v tabeli sprememb.

## REST Povezave

- `POST /auth/login` - prijava uporabnika.
- `GET /tekmovanja` - seznam tekmovanj.
- `GET /tekmovanja/<id>/rezultati` - rezultati izbranega tekmovanja.
- `GET /tekmovalci/iskanje?ime=...` - iskanje tekmovalcev.
- `GET /tekmovalci/<id>/nastopi` - nastopi izbranega tekmovalca.
- `POST /rezultati` - dodajanje rezultata.
- `PUT /rezultati/<id>` - posodobitev rezultata.
- `DELETE /rezultati/<id>` - brisanje rezultata.
- `GET /validacija/nepopolni` - nepopolni rezultati.
- `GET /validacija/duplikati` - podvojeni zapisi.
- `GET /primerjava?tekmovalec1=...&tekmovalec2=...` - primerjava dveh tekmovalcev.
- `GET /spremembe` - pregled sprememb.

## Validacija

- Tekmovalec in tekmovanje sta obvezna pri dodajanju rezultata.
- Številčna polja, kot so uvrstitve in točke, se preverjajo na celo ali decimalno število.
- Prazna neobvezna polja se shranijo kot `NULL` oziroma prazna vrednost, odvisno od tipa.
- Desktop aplikacija pred pošiljanjem preveri ID-je in uporabniku pokaže opozorilo, če so podatki neveljavni.

## Večjezičnost

- Aplikacija podpira slovenščino in angleščino.
- Prevajanje je izvedeno v datoteki `desktop_app/translations.py`.
- Prevajajo se naslov aplikacije, prijava, glavni zavihki in osnovni gumbi.

## Installer

- Namizni del se zaganja iz `desktop_app/main.py`.
- Za pripravo Windows paketa je primerna uporaba `PyInstaller`.
- Tipičen postopek je izdelava samostojnega `.exe` in nato zavijanje v installer, na primer z `Inno Setup` ali podobnim orodjem.
- Dokumentacija predvideva distribucijo namizne aplikacije kot pakiranega Windows programa skupaj s potrebnimi Python odvisnostmi in bazo podatkov.
