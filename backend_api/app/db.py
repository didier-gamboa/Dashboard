from collections.abc import Generator
from app import settings


def get_conn() -> Generator[object, None, None]:
    """
    Devuelve una conexión según DB_TYPE.
    - Postgres: psycopg (row_factory=dict)
    - MySQL: mysql-connector-python
    """
    if settings.IS_POSTGRES:
        import psycopg
        from psycopg.rows import dict_row

        conn = psycopg.connect(settings.PSYCOPG_DSN, row_factory=dict_row)
        conn.autocommit = True
        try:
            yield conn
        finally:
            conn.close()
        return

    # MySQL (mysql-connector-python)
    import mysql.connector

    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
    )
    conn.autocommit = True
    try:
        yield conn
    finally:
        conn.close()