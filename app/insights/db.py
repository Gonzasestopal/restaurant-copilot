import psycopg2
import psycopg2.extras


from app.config import settings


def get_connection():
    """
    Create a new psycopg2 connection using a full DATABASE_URL.
    Example URI:
        postgresql://user:pass@host:5432/dbname
    """
    return psycopg2.connect(settings.database_url)

def run_sql_raw(sql: str):
    """
    Execute SQL using psycopg2 raw cursor and return real columns + rows.
    Safest possible method, no eval, no string parsing.
    """
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()  # list[dict]
        return rows

    finally:
        cursor.close()
        conn.close()
