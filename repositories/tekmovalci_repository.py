from db import get_connection

def search_tekmovalci_repo(ime):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM tekmovalci
        WHERE ime_priimek LIKE %s
        ORDER BY ime_priimek ASC
    """, (f"%{ime}%",))

    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results