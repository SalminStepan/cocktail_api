from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.db.models import Cocktail


def get_cocktail_summaries(
    conn,
    limit: int,
    offset: int,
) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                name,
                image_url,
                glass,
                parse_status
            FROM cocktails
            ORDER BY id
            LIMIT %s
            OFFSET %s;""", (limit, offset)
        )
        cocktails = cur.fetchall()
        return cocktails


def get_cocktail_summaries_orm(
    session: Session,
    limit: int,
    offset: int,
) -> list[Cocktail]:
    stmt = (
        select(Cocktail)
        .order_by(Cocktail.id)
        .limit(limit)
        .offset(offset)
    )

    res = session.execute(stmt)
    cocktails = res.scalars().all()
    return cocktails

def get_cocktail_by_id(conn, cocktail_id :int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                name,
                description,
                image_url,
                glass,
                garnish,
                method,
                parse_status,
                source_url
            FROM cocktails
            WHERE id = %s;""",
            (cocktail_id,)
            )
        cocktail = cur.fetchone()
        return cocktail

def get_cocktail_by_id_orm(session: Session, cocktail_id:int) -> Cocktail | None:
    stmt = (
        select(Cocktail)
        .where(Cocktail.id == cocktail_id)
        .options(selectinload(Cocktail.ingredients))
        )

    return (session.execute(stmt)).scalar_one_or_none()

def search_cocktail_summaries(
        conn, 
        query: str,
        limit: int,
        offset: int
) -> list[dict]:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT DISTINCT
                c.id,
                c.name,
                c.image_url,
                c.glass,
                c.parse_status
            FROM cocktails AS c
            LEFT JOIN ingredients AS i
                ON i.cocktail_id = c.id
            WHERE c.name ILIKE %s
            OR i.name ILIKE %s
            OR i.raw ILIKE %s
            ORDER BY c.id
            LIMIT %s
            OFFSET %s;""", (pattern, pattern, pattern, limit, offset))
        cocktails = cur.fetchall()
        return cocktails

def count_cocktails(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS total
            FROM cocktails;""")
        total_cocktails = cur.fetchone()
        return total_cocktails["total"]

def count_cocktails_orm(session: Session) -> int:
    stmt = select(func.count()).select_from(Cocktail)
    return session.execute(stmt).scalar_one()

def count_cocktail_search_results(conn, query: str) -> int:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT COUNT(DISTINCT c.id) AS total
            FROM cocktails AS c
            LEFT JOIN ingredients AS i
                ON i.cocktail_id = c.id
            WHERE
                c.name ILIKE %s
                OR i.name ILIKE %s
                OR i.raw ILIKE %s;""", (pattern, pattern, pattern))
        row = cur.fetchone()
        return row["total"]

def get_cocktail_by_name(conn, name: str) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, description, image_url, glass, garnish, method, parse_status, source_url
            FROM cocktails
            WHERE name ILIKE %s
            ORDER BY id
            LIMIT 1;
            """,
            (name,)
        )
        result = cur.fetchone()
        return result
        