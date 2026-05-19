from db import get_connection


def create_sprememba_repo(tabela, operacija, opis, tk_admin=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COALESCE(MAX(id_spremembe), 0) + 1 FROM spremembe")
    next_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO spremembe (id_spremembe, tabela, operacija, cas, opis, tk_admin)
        VALUES (%s, %s, %s, NOW(), %s, %s)
    """, (next_id, tabela, operacija, opis, tk_admin))

    conn.commit()

    cur.close()
    conn.close()


def get_all_spremembe_repo():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            s.id_spremembe,
            s.tabela,
            s.operacija,
            s.cas,
            s.opis,
            s.tk_admin,
            a.uporIme,
            a.ime,
            a.priimek
        FROM spremembe s
        LEFT JOIN admini a ON s.tk_admin = a.id_admina
        ORDER BY s.cas DESC
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data