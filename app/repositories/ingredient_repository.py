from sqlalchemy import (
    select,
    and_,
    func,
    distinct
)
from sqlalchemy.orm import Session, selectinload

from app.db.models import Cocktail, Ingredient


def get_ingredients_by_cocktail_id(conn, cocktail_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                position,
                raw,
                amount,
                unit,
                name,
                comment,
                unresolved
            FROM ingredients
            WHERE cocktail_id = %s
            ORDER BY position;""", 
            (cocktail_id,)
            )
        ingredients = cur.fetchall()
        return ingredients

def search_ingredient_names(
    conn,
    query: str,
    limit: int,
    offset: int,
) -> list[dict]:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT
                i.name,
                COUNT(DISTINCT i.cocktail_id) AS cocktail_count
            FROM ingredients AS i
            WHERE i.name IS NOT NULL
            AND i.unresolved = false
            AND i.name ILIKE %s
            GROUP BY i.name
            ORDER BY cocktail_count DESC, i.name
            LIMIT %s
            OFFSET %s;""", (pattern, limit, offset))
        counted_ingredients = cur.fetchall()
        return counted_ingredients

def search_ingredient_names_orm(
    session: Session,
    query: str,
    limit: int,
    offset: int
):
    pattern = f"%{query}%"

    cocktail_count = func.count(
        distinct(Ingredient.cocktail_id)
    ).label("cocktail_count")
    
    stmt = (
        select(
            Ingredient.name, 
            cocktail_count
        )        
        .where(
            Ingredient.name.is_not(None),
            Ingredient.unresolved.is_(False),
            Ingredient.name.ilike(pattern)
        )
        .group_by(Ingredient.name)
        .order_by(
            cocktail_count.desc(),
            Ingredient.name
        )
        .limit(limit)
        .offset(offset)
        )

    res = session.execute(stmt)
    return res.all()

def count_ingredient_search_results(conn, query: str) -> int:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT COUNT(DISTINCT i.name) AS total
            FROM ingredients AS i
            WHERE i.name IS NOT NULL
            AND i.unresolved = false
            AND i.name ILIKE %s;""", (pattern,))
        total = cur.fetchone()
        return total["total"]

def count_ingredient_search_results_orm(
    session: Session,
    query: str
    ) -> int:
    pattern = f"%{query}%"

    stmt = (
        select(func.count(distinct(Ingredient.name))).select_from(Ingredient)
        .where(
            Ingredient.name.is_not(None),
            Ingredient.unresolved.is_(False),
            Ingredient.name.ilike(pattern)
        )
    )

    return session.execute(stmt).scalar_one()