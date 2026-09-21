from sqlalchemy import (
    select,
    or_,
    func,
    distinct
)
from sqlalchemy.orm import Session, selectinload

from app.db.models import Cocktail, Ingredient


def get_cocktail_summaries(
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

def get_cocktail_by_id(session: Session, cocktail_id:int) -> Cocktail | None:
    stmt = (
        select(Cocktail)
        .where(Cocktail.id == cocktail_id)
        .options(selectinload(Cocktail.ingredients))
        )

    return (session.execute(stmt)).scalar_one_or_none()

def search_cocktail_summaries(
    session: Session,
    query: str,
    limit: int,
    offset: int,
) -> list[Cocktail]:
    pattern = f"%{query}%"
    stmt = (
        select(Cocktail)
        .outerjoin(Cocktail.ingredients)
        .where(
        or_(
            Cocktail.name.ilike(pattern),
            Ingredient.name.ilike(pattern),
            Ingredient.raw.ilike(pattern),
            )
        )
        .distinct()
        .order_by(Cocktail.id)
        .limit(limit)
        .offset(offset)
        )
    
    res = session.execute(stmt)
    cocktails = res.scalars().all()
    return cocktails

def count_cocktails(session: Session) -> int:
    stmt = select(func.count()).select_from(Cocktail)
    return session.execute(stmt).scalar_one()


def count_cocktail_search_results(
    session: Session,
    query: str
    ) -> int:
    pattern = f"%{query}%"
    stmt = (
        select(func.count(distinct(Cocktail.id)))
        .outerjoin(Cocktail.ingredients)
        .where(
        or_(
            Cocktail.name.ilike(pattern),
            Ingredient.name.ilike(pattern),
            Ingredient.raw.ilike(pattern),
            )
        )
    )
    
    return session.execute(stmt).scalar_one()


def get_cocktail_by_name(
    session: Session,
    name: str,
) -> Cocktail | None:

    stmt = (
        select(Cocktail)
        .where(Cocktail.name.ilike(name))
        .options(selectinload(Cocktail.ingredients))
        .order_by(Cocktail.id)
        .limit(1)
    )

    return session.execute(stmt).scalar_one_or_none()

