from db import get_connection

def get_nepopolni_repo():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM rezultati WHERE skupniCas IS NULL OR skupniCas=''")
    data = cur.fetchall()
    conn.close()
    return data

def get_duplikati_repo():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT tk_tekmovalec, tk_tekmovanje, COUNT(*) as cnt
        FROM rezultati
        GROUP BY tk_tekmovalec, tk_tekmovanje
        HAVING COUNT(*) > 1
    """)
    data = cur.fetchall()
    conn.close()
    return data