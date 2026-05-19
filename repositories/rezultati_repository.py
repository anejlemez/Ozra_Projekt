from db import get_connection


ALLOWED_FIELDS = [
    "overallRank",
    "genderRank",
    "divRank",
    "bib",
    "divizija",
    "tocke",
    "plavanje",
    "t1",
    "kolesarjenje",
    "t2",
    "tek",
    "skupniCas",
    "tk_tekmovalec",
    "tk_tekmovanje"
]


def create_rezultat_repo(data):
    conn = get_connection()
    cur = conn.cursor()

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

    values = (
        data.get("overallRank"),
        data.get("genderRank"),
        data.get("divRank"),
        data.get("bib"),
        data.get("divizija"),
        data.get("tocke"),
        data.get("plavanje"),
        data.get("t1"),
        data.get("kolesarjenje"),
        data.get("t2"),
        data.get("tek"),
        data.get("skupniCas"),
        data.get("tk_tekmovalec"),
        data.get("tk_tekmovanje")
    )

    cur.execute(sql, values)
    conn.commit()

    rezultat_id = cur.lastrowid

    cur.close()
    conn.close()

    return rezultat_id


def get_rezultat_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            r.*,
            tm.ime_priimek,
            tk.naziv AS naziv_tekmovanja,
            tk.leto,
            tk.tip_tekmovanja,
            tk.lokacija
        FROM rezultati r
        LEFT JOIN tekmovalci tm ON r.tk_tekmovalec = tm.id_tekmovalec
        LEFT JOIN tekmovanja tk ON r.tk_tekmovanje = tk.id_tekmovanja
        WHERE r.id_rezultata = %s
    """, (id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data


def update_rezultat_repo(id, data):
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    for field in ALLOWED_FIELDS:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data.get(field))

    if not fields:
        cur.close()
        conn.close()
        return 0

    values.append(id)

    sql = f"""
        UPDATE rezultati
        SET {", ".join(fields)}
        WHERE id_rezultata = %s
    """

    cur.execute(sql, values)
    conn.commit()

    updated = cur.rowcount

    cur.close()
    conn.close()

    return updated


def delete_rezultat_repo(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM rezultati WHERE id_rezultata = %s", (id,))
    conn.commit()

    deleted = cur.rowcount

    cur.close()
    conn.close()

    return deleted