from db import get_connection

def get_admin_by_username_repo(uporabnisko_ime):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM admini
        WHERE uporIme = %s
    """, (uporabnisko_ime,))

    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin