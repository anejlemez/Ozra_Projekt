from db import get_connection

def get_all_tekmovanja_repo():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tekmovanja ORDER BY leto DESC, naziv ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_one_tekmovanje_repo(tekmovanje_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tekmovanja WHERE id_tekmovanja = %s", (tekmovanje_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result else {}

def get_rezultati_za_tekmovanje_repo(tekmovanje_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, t.ime_priimek
        FROM rezultati r
        JOIN tekmovalci t ON r.tk_tekmovalec = t.id_tekmovalec
        WHERE r.tk_tekmovanje = %s
        ORDER BY r.overallRank ASC
    """, (tekmovanje_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results