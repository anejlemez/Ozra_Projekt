from db import get_connection

def get_all_tekmovanja_repo():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tekmovanja")
    data = cur.fetchall()
    conn.close()
    return data

def get_one_tekmovanje_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tekmovanja WHERE id_tekmovanja=%s", (id,))
    data = cur.fetchone()
    conn.close()
    return data

def get_rezultati_tekmovanja_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT r.*, t.ime_priimek
        FROM rezultati r
        JOIN tekmovalci t ON r.tk_tekmovalec=t.id_tekmovalec
        WHERE r.tk_tekmovanje=%s
    """, (id,))
    data = cur.fetchall()
    conn.close()
    return data