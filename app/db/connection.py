import psycopg
from psycopg.rows import dict_row
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import logging

logger = logging.getLogger(__name__)


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def check_database_connection() -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS database_ok;")
                res = cur.fetchone()
                return res is not None and res["database_ok"] == 1

    except psycopg.Error as e:
        logger.warning("connection failed: %s", e)
        return False