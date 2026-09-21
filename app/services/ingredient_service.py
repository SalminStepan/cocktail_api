from math import ceil

from app.schemas.ingredient import IngredientSearchResult, IngredientPage
from app.repositories.ingredient_repository import (
    count_ingredient_search_results,
    search_ingredient_names,
)

from app.db.session import SessionLocal


def search_ingredients(
    query: str,
    page: int = 1,
    page_size: int = 20,
) -> IngredientPage:
    query = " ".join(query.split())
    limit = page_size
    offset = (page - 1) * page_size
    if not query:
        return IngredientPage(
            items=[],
            page=page,
            page_size=page_size,
            total=0,
            total_pages=0,
        )

    with SessionLocal() as session:
        rows = search_ingredient_names(session, query, limit, offset)

        ingredients = []
        for row in rows:
            ingredient = IngredientSearchResult(
                name=row.name,
                cocktail_count=row.cocktail_count
            )
            ingredients.append(ingredient)

        total_cocktails = count_ingredient_search_results(session, query)
        total_pages = ceil(total_cocktails / page_size)
        
        ingredients_page = IngredientPage(
            items = ingredients,
            page = page,
            page_size = page_size,
            total = total_cocktails,
            total_pages = total_pages
        )
        return ingredients_page
