from sqlalchemy import (
    select,
    func,
)
from sqlalchemy.orm import Session

from app.db.models import Cocktail, Ingredient


def get_dataset_stats(session: Session) -> dict:
    cocktail_stmt = select(
        func.count().label("cocktails_total"),

        func.count()
        .filter(Cocktail.parse_status == "ok")
        .label("parse_ok"),

        func.count()
        .filter(Cocktail.parse_status == "partial")
        .label("parse_partial"),

        func.count()
        .filter(Cocktail.parse_status  == "failed")
        .label("parse_failed"),

        func.count()
        .filter(Cocktail.image_url.is_not(None))
        .label("cocktails_with_image"),

        func.count()
        .filter(Cocktail.image_url.is_(None))
        .label("cocktails_without_image"),
        
    ).select_from(Cocktail)

    ingredient_stmt = select(
        func.count().label("ingredients_total"),

        func.count()
        .filter(Ingredient.unresolved.is_(True))
        .label("unresolved_ingredients"),
    ).select_from(Ingredient)

    cocktail_stats = session.execute(cocktail_stmt).mappings().one()
    ingredient_stats = session.execute(ingredient_stmt).mappings().one()

    stats = {
    **cocktail_stats,
    **ingredient_stats,
    }
    return stats