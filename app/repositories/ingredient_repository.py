from sqlalchemy import (
    select,
    func,
    distinct
)
from sqlalchemy.orm import Session

from app.db.models import Ingredient



def search_ingredient_names(
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


def count_ingredient_search_results(
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