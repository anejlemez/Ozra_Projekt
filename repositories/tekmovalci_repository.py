from db import get_connection

def search_tekmovalci_repo(ime):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tekmovalci WHERE ime_priimek LIKE %s", (f"%{ime}%",))
    data = cur.fetchall()
    conn.close()
    return data

def get_tekmovalec_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tekmovalci WHERE id_tekmovalec=%s", (id,))
    data = cur.fetchone()
    conn.close()
    return data

def get_nastopi_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT * FROM rezultati WHERE tk_tekmovalec=%s
    """, (id,))
    data = cur.fetchall()
    conn.close()
    return data

def get_najboljsi_cas_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT MIN(skupniCas) as najboljsi FROM rezultati WHERE tk_tekmovalec=%s
    """, (id,))
    data = cur.fetchone()
    conn.close()
    return data