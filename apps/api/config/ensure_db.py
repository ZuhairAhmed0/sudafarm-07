import os
import sys
from urllib.parse import urlparse


def ensure_database():
    db_url = os.environ.get("DATABASE_URL", "").strip()
    if not db_url or db_url.startswith("sqlite"):
        return

    try:
        import psycopg
    except ImportError:
        return

    # Check if database already exists and connects
    try:
        with psycopg.connect(db_url, connect_timeout=5):
            print("Database connection verified.")
            return
    except psycopg.OperationalError as e:
        err_msg = str(e)
        if "does not exist" not in err_msg:
            print(f"Database check warning: {e}", file=sys.stderr)
            return

    # Database does not exist — attempt to create it automatically
    parsed = urlparse(db_url)
    target_db = parsed.path.lstrip("/")
    if not target_db:
        return

    print(f"Database '{target_db}' does not exist on PostgreSQL server.")
    print("Attempting to create it automatically via maintenance database...")

    candidates = ["postgres"]
    if parsed.username and parsed.username not in candidates:
        candidates.append(parsed.username)

    for m_db in candidates:
        m_url = parsed._replace(path=f"/{m_db}").geturl()
        try:
            with psycopg.connect(m_url, autocommit=True, connect_timeout=5) as conn:
                with conn.cursor() as cur:
                    clean_name = target_db.replace('"', '""')
                    cur.execute(f'CREATE DATABASE "{clean_name}"')
                    print(f"Successfully created database '{target_db}'!")
                    return
        except Exception as ex:
            print(f"Note: Could not create '{target_db}' via '{m_db}': {ex}")

    print("Could not automatically create database. Please verify DATABASE_URL database name.")


if __name__ == "__main__":
    ensure_database()
