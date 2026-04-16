from db import get_connection

def get_admin_repo(username):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM admini WHERE uporIme=%s", (username,))
    data = cur.fetchone()
    conn.close()
    return data