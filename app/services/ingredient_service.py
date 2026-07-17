from app.schemas.ingredient import IngredientSearchResult
from app.repositories.ingredient_repository import search_ingredient_names
from app.db.connection import get_connection

def search_ingredients(
    query: str,
    page: int = 1,
    page_size: int = 20,
) -> list[IngredientSearchResult]:
    query = " ".join(query.split())
    limit = page_size
    offset = (page - 1) * page_size
    if not query:
        return []
    with get_connection() as conn:
        rows = search_ingredient_names(conn, query, limit, offset)
        ingredients = []
        for row in rows:
            ingredient = IngredientSearchResult(**row)
            ingredients.append(ingredient)
        return ingredients