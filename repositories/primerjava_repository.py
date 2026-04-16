from db import get_connection

def get_stats_repo(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT COUNT(*) as nastopi, MIN(skupniCas) as najboljsi
        FROM rezultati WHERE tk_tekmovalec=%s
    """, (id,))
    data = cur.fetchone()
    conn.close()
    return data