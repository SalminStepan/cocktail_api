import psycopg
import logging
from contextlib import contextmanager
from psycopg.rows import dict_row

from app.exceptions import DatabaseUnavailableError
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


logger = logging.getLogger(__name__)


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

@contextmanager
def get_connection():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            yield conn
    except (psycopg.OperationalError, psycopg.InterfaceError) as e:
        logger.exception("Database connection error")
        raise DatabaseUnavailableError("Database unavailable") from e

def check_database_connection() -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS database_ok;")
                res = cur.fetchone()
                return res is not None and res["database_ok"] == 1

    except DatabaseUnavailableError:
        return False