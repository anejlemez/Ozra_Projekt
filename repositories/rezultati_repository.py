from db import get_connection

def create_rezultat_repo(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rezultati (
            overallRank, genderRank, divRank, bib, divizija, tocke,
            plavanje, t1, kolesarjenje, t2, tek, skupniCas,
            tk_tekmovalec, tk_tekmovanje
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
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
    ))

    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

def update_rezultat_repo(rezultat_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rezultati
        SET overallRank = %s,
            genderRank = %s,
            divRank = %s,
            bib = %s,
            divizija = %s,
            tocke = %s,
            plavanje = %s,
            t1 = %s,
            kolesarjenje = %s,
            t2 = %s,
            tek = %s,
            skupniCas = %s
        WHERE id_rezultata = %s
    """, (
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
        rezultat_id
    ))

    conn.commit()
    count = cursor.rowcount
    cursor.close()
    conn.close()
    return count

def delete_rezultat_repo(rezultat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rezultati WHERE id_rezultata = %s", (rezultat_id,))
    conn.commit()

    count = cursor.rowcount
    cursor.close()
    conn.close()
    return count