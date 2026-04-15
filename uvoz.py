import os
import csv
import time
from dataclasses import dataclass
from typing import Optional
import mysql.connector

POT_DO_DATOTEK = r"C:/Users/anejl/OneDrive - Univerza v Mariboru/Documents/Faks/Drugi Letnik/Drugi semester/Orodja za razvoj aplikacij/Race-Results/Race-Results"

DB_CONFIG = {
    "user": "root",
    "password": "ozrageslo",
    "host": "127.0.0.1",
    "port": 3307,
    "database": "mydb"
}

BATCH_SIZE = 5000


@dataclass
class Tekmovanje:
    naziv: str
    leto: int
    tip_tekmovanja: str
    lokacija: str


@dataclass
class Tekmovalec:
    ime_priimek: str
    starost: Optional[int]
    drzava: Optional[str]


@dataclass
class Rezultat:
    overall_rank: Optional[int]
    gender_rank: Optional[int]
    div_rank: Optional[int]
    bib: Optional[str]
    divizija: Optional[str]
    tocke: Optional[float]
    plavanje: Optional[str]
    t1: Optional[str]
    kolesarjenje: Optional[str]
    t2: Optional[str]
    tek: Optional[str]
    skupni_cas: Optional[str]


def clean_str(v):
    if v is None:
        return None
    v = str(v).strip()
    if v in ("", "---", "-", "--"):
        return None
    return v


def clean_int(v):
    v = clean_str(v)
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def clean_float(v):
    v = clean_str(v)
    if v is None:
        return None
    try:
        return float(v.replace(",", "."))
    except Exception:
        return None


def detect_encoding(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.readline()
        return "utf-8"
    except UnicodeDecodeError:
        return "latin1"


def najdi_vse_csv(base_path):
    csv_datoteke = []

    discipline = ["IRONMAN", "IRONMAN70.3", "Ultra-triathlon"]

    for disciplina in discipline:
        csv_mapa = os.path.join(base_path, disciplina, "CSV")

        if not os.path.exists(csv_mapa):
            print(f"[OPOZORILO] Mapa ne obstaja: {csv_mapa}")
            continue

        for file in os.listdir(csv_mapa):
            if file.lower().endswith(".csv"):
                csv_datoteke.append(os.path.join(csv_mapa, file))

    return sorted(csv_datoteke)


def get_race_info(filename):
    name = os.path.basename(filename).replace(".csv", "")
    parts = name.split("_")
    lower = name.lower()

    if lower.startswith("im703_"):
        # primer: im703_augusta_2015
        # primer: im703_buenos_aires_2016
        # primer: im703_puerto_rico_2014
        leto = int(parts[-1])
        lokacija = "_".join(parts[1:-1]).replace("-", " ").strip().title()

        return Tekmovanje(
            naziv=f"IRONMAN 70.3 {lokacija}",
            leto=leto,
            tip_tekmovanja="IRONMAN70.3",
            lokacija=lokacija
        )

    elif lower.startswith("im_"):
        # primer: im_australia_2015
        # primer: im_world-championships_2014
        # primer: im_new-zealand_2016
        leto = int(parts[-1])
        lokacija = "_".join(parts[1:-1]).replace("-", " ").strip().title()

        return Tekmovanje(
            naziv=f"IRONMAN {lokacija}",
            leto=leto,
            tip_tekmovanja="IRONMAN",
            lokacija=lokacija
        )

    elif lower.startswith("double_") or lower.startswith("triple_"):
        # primer: Double_Germany_2015_Man
        # primer: Double_USA_Florida_2015_Man
        # primer: Double_Hungary__2014_Woman
        # primer: Triple_UK__2014_Man

        prefix = parts[0].lower()
        clean_parts = [p for p in parts if p != ""]

        # zadnji del je spol, predzadnji je leto
        leto = int(clean_parts[-2])
        lokacija = "_".join(clean_parts[1:-2]).replace("-", " ").strip().title()

        naziv = "Double Ultra Triathlon" if prefix == "double" else "Triple Ultra Triathlon"

        return Tekmovanje(
            naziv=naziv,
            leto=leto,
            tip_tekmovanja="ULTRA-TRIATHLON",
            lokacija=lokacija
        )

    else:
        raise ValueError(f"Neznan format datoteke: {filename}")


def parse_ironman_row(row):
    tekmovalec = Tekmovalec(
        ime_priimek=clean_str(row.get("name")) or "NEZNANO",
        starost=clean_int(row.get("age")),
        drzava=clean_str(row.get("country"))
    )

    rezultat = Rezultat(
        overall_rank=clean_int(row.get("overallRank")),
        gender_rank=clean_int(row.get("genderRank")),
        div_rank=clean_int(row.get("divRank")),
        bib=clean_str(row.get("bib")),
        divizija=clean_str(row.get("division")),
        tocke=clean_float(row.get("points")),
        plavanje=clean_str(row.get("swim")),
        t1=clean_str(row.get("t1")),
        kolesarjenje=clean_str(row.get("bike")),
        t2=clean_str(row.get("t2")),
        tek=clean_str(row.get("run")),
        skupni_cas=clean_str(row.get("overall"))
    )

    return tekmovalec, rezultat


def parse_ultra_row(row):
    competitor = (
        row.get("Competitor")
        or row.get("competitor")
        or row.get("Name")
        or row.get("name")
    )

    country = (
        row.get("Country")
        or row.get("country")
    )

    overall = row.get("Overall") or row.get("overall")
    rank = row.get("Rank") or row.get("rank")
    age_category = row.get("Age_Category") or row.get("Age category") or row.get("category")

    swim = row.get("Swim") or row.get("swim")
    trans1 = row.get("Trans1") or row.get("T1") or row.get("t1")
    bike = row.get("Bike") or row.get("bike")
    trans2 = row.get("Trans2") or row.get("T2") or row.get("t2")
    run = row.get("Run") or row.get("run")
    finish = row.get("Finish") or row.get("finish") or row.get("overall")

    tekmovalec = Tekmovalec(
        ime_priimek=clean_str(competitor) or "NEZNANO",
        starost=None,
        drzava=clean_str(country)
    )

    rezultat = Rezultat(
        overall_rank=clean_int(overall),
        gender_rank=clean_int(rank),
        div_rank=clean_int(rank),
        bib=None,
        divizija=clean_str(age_category),
        tocke=None,
        plavanje=clean_str(swim),
        t1=clean_str(trans1),
        kolesarjenje=clean_str(bike),
        t2=clean_str(trans2),
        tek=clean_str(run),
        skupni_cas=clean_str(finish)
    )

    return tekmovalec, rezultat


def get_or_create_tekmovanje(cursor, tekmovanje, cache):
    key = (tekmovanje.naziv, tekmovanje.leto, tekmovanje.tip_tekmovanja, tekmovanje.lokacija)

    if key in cache:
        return cache[key]

    sql = """
        INSERT INTO tekmovanja (naziv, leto, tip_tekmovanja, lokacija)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id_tekmovanja = LAST_INSERT_ID(id_tekmovanja)
    """
    cursor.execute(sql, key)
    tekmovanje_id = cursor.lastrowid
    cache[key] = tekmovanje_id
    return tekmovanje_id


def get_or_create_tekmovalec(cursor, tekmovalec, cache):
    key = (tekmovalec.ime_priimek, tekmovalec.starost, tekmovalec.drzava)

    if key in cache:
        return cache[key]

    sql = """
        INSERT INTO tekmovalci (ime_priimek, starost, drzava)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE id_tekmovalec = LAST_INSERT_ID(id_tekmovalec)
    """
    cursor.execute(sql, key)
    tekmovalec_id = cursor.lastrowid
    cache[key] = tekmovalec_id
    return tekmovalec_id


def flush_rezultati(cursor, batch):
    if not batch:
        return

    sql = """
        INSERT INTO rezultati
        (
            overallRank,
            genderRank,
            divRank,
            bib,
            divizija,
            tocke,
            plavanje,
            t1,
            kolesarjenje,
            t2,
            tek,
            skupniCas,
            tk_tekmovalec,
            tk_tekmovanje
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, batch)
    batch.clear()


def uvozi_vse():
    start = time.time()

    cnx = mysql.connector.connect(**DB_CONFIG, autocommit=False)
    cursor = cnx.cursor()

    cache_tekmovanja = {}
    cache_tekmovalci = {}
    batch_rezultati = []

    st_datotek = 0
    st_rezultatov = 0
    st_preskocenih = 0

    try:
        datoteke_csv = najdi_vse_csv(POT_DO_DATOTEK)
        print(f"Najdenih CSV datotek: {len(datoteke_csv)}")

        for pot in datoteke_csv:
            cas_datoteke_start = time.time()
            ime_datoteke = os.path.basename(pot)

            try:
                tekmovanje = get_race_info(ime_datoteke)
                tekmovanje_id = get_or_create_tekmovanje(cursor, tekmovanje, cache_tekmovanja)

                encoding = detect_encoding(pot)

                with open(pot, "r", encoding=encoding, errors="replace", newline="") as f:
                    reader = csv.DictReader(f)
                    headers = set(reader.fieldnames or [])

                    ironman_format = "name" in headers and "overallRank" in headers
                    ultra_format = (
                        "Competitor" in headers or "competitor" in headers or "Name" in headers or "name" in headers
                    ) and (
                        "Finish" in headers or "finish" in headers or "overall" in headers
                    )

                    if not ironman_format and not ultra_format:
                        print(f"Preskakujem nepodprt format: {ime_datoteke}")
                        st_preskocenih += 1
                        continue

                    st_vrstic_datoteke = 0

                    for row in reader:
                        if ironman_format:
                            tekmovalec, rezultat = parse_ironman_row(row)
                        else:
                            tekmovalec, rezultat = parse_ultra_row(row)

                        tekmovalec_id = get_or_create_tekmovalec(cursor, tekmovalec, cache_tekmovalci)

                        batch_rezultati.append((
                            rezultat.overall_rank,
                            rezultat.gender_rank,
                            rezultat.div_rank,
                            rezultat.bib,
                            rezultat.divizija,
                            rezultat.tocke,
                            rezultat.plavanje,
                            rezultat.t1,
                            rezultat.kolesarjenje,
                            rezultat.t2,
                            rezultat.tek,
                            rezultat.skupni_cas,
                            tekmovalec_id,
                            tekmovanje_id
                        ))

                        st_rezultatov += 1
                        st_vrstic_datoteke += 1

                        if len(batch_rezultati) >= BATCH_SIZE:
                            flush_rezultati(cursor, batch_rezultati)

                flush_rezultati(cursor, batch_rezultati)
                cnx.commit()

                st_datotek += 1
                trajanje_datoteke = round(time.time() - cas_datoteke_start, 2)
                print(f"Uvožena: {ime_datoteke} | vrstice: {st_vrstic_datoteke}")

            except Exception as file_error:
                cnx.rollback()
                batch_rezultati.clear()
                cache_tekmovanja.clear()
                cache_tekmovalci.clear()
                st_preskocenih += 1
                print(f"Napaka v datoteki {ime_datoteke}: {file_error}")

        end = time.time()
        print("\nKončano")
        print(f"Datotek: {st_datotek}")
        print(f"Preskočenih: {st_preskocenih}")
        print(f"Rezultatov: {st_rezultatov}")
        print(f"Čas: {round((end - start)/60, 2)} min")

    except Exception as e:
        cnx.rollback()
        print("Napaka pri uvozu:", e)

    finally:
        cursor.close()
        cnx.close()
        print("Povezava z bazo zaprta.")


if __name__ == "__main__":
    uvozi_vse()