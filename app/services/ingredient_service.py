from math import ceil

from app.schemas.ingredient import IngredientSearchResult, IngredientPage
from app.repositories.ingredient_repository import search_ingredient_names, count_ingredient_search_results
from app.db.connection import get_connection

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
    with get_connection() as conn:
        rows = search_ingredient_names(conn, query, limit, offset)
        ingredients = []
        for row in rows:
            ingredient = IngredientSearchResult(**row)
            ingredients.append(ingredient)
        total_cocktails = count_ingredient_search_results(conn, query)
        total_pages = ceil(total_cocktails / page_size)
        ingredients_page = IngredientPage(
            items = ingredients,
            page = page,
            page_size = page_size,
            total = total_cocktails,
            total_pages = total_pages
        )
        return ingredients_page