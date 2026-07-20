from math import ceil

from app.db.connection import get_connection
from app.repositories.cocktail_repository import (
    get_cocktail_summaries,
    get_cocktail_by_id, 
    search_cocktail_summaries,
    count_cocktails,
    count_cocktail_search_results
)
from app.repositories.ingredient_repository import get_ingredients_by_cocktail_id
from app.schemas.cocktail import CocktailSummary, CocktailPage
from app.schemas.ingredient import (
    CocktailDetail,
    IngredientRead,
)


def get_cocktail_page(
    page: int = 1,
    page_size: int = 20,
) -> CocktailPage:
    limit = page_size
    offset = (page - 1) * page_size
    with get_connection() as conn:
        rows = get_cocktail_summaries(conn, limit, offset)
        cocktails = []
        for row in rows:
            cocktail = CocktailSummary(**row)
            cocktails.append(cocktail)

        total_cocktails = count_cocktails(conn)
        total_pages = ceil(total_cocktails / page_size)
        cocktail_page = CocktailPage(
            items = cocktails,
            page = page,
            page_size= page_size,
            total = total_cocktails,
            total_pages = total_pages
        )

        return cocktail_page

def get_cocktail_detail(cocktail_id: int) -> CocktailDetail | None:
    with get_connection() as conn:
        cocktail_row = get_cocktail_by_id(conn, cocktail_id)
        if cocktail_row is None:
            return None
        
        ingredient_rows = get_ingredients_by_cocktail_id(conn, cocktail_id)
        
        ingredients_clean = []
        for ing_row in ingredient_rows:
            ingredient = IngredientRead(**ing_row)
            ingredients_clean.append(ingredient)


        cocktail = CocktailDetail(**cocktail_row, ingredients=ingredients_clean)
        return cocktail

def search_cocktails(
    query: str,
    page: int = 1,
    page_size: int = 20,
) -> CocktailPage:
    query = " ".join(query.split())
    if not query:
        return CocktailPage(
            items=[],
            page=page,
            page_size=page_size,
            total=0,
            total_pages=0,
        )
    limit = page_size
    offset = (page - 1) * page_size
    with get_connection() as conn:
        rows = search_cocktail_summaries(conn, query, limit, offset)
        cocktails = []
        for row in rows:
            cocktail = CocktailSummary(**row)
            cocktails.append(cocktail)

        total_cocktails = count_cocktail_search_results(conn, query)
        total_pages = ceil(total_cocktails / page_size)
        
        cocktail_page = CocktailPage(
            items = cocktails,
            page = page,
            page_size= page_size,
            total = total_cocktails,
            total_pages = total_pages
        )

        return cocktail_page