from db import get_connection

def create_rezultat_repo(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO rezultati (tk_tekmovalec, tk_tekmovanje) VALUES (%s,%s)",
                (data["tk_tekmovalec"], data["tk_tekmovanje"]))
    conn.commit()
    id = cur.lastrowid
    conn.close()
    return id

def get_rezultat_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM rezultati WHERE id_rezultata=%s", (id,))
    data = cur.fetchone()
    conn.close()
    return data

def update_rezultat_repo(id, data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE rezultati SET overallRank=%s WHERE id_rezultata=%s",
                (data.get("overallRank"), id))
    conn.commit()
    return cur.rowcount

def delete_rezultat_repo(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM rezultati WHERE id_rezultata=%s", (id,))
    conn.commit()
    return cur.rowcount