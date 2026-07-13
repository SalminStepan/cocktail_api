from app.db.connection import get_connection
from app.repositories.cocktail_repository import get_cocktail_summaries
from app.schemas.cocktail import CocktailSummary

def get_cocktail_page(
    page: int = 1,
    page_size: int = 20,
) -> list[CocktailSummary]:
    limit = page_size
    offset = (page - 1) * page_size
    with get_connection() as conn:
        rows = get_cocktail_summaries(conn, limit, offset)
        cocktails = []
        for row in rows:
            cocktail = CocktailSummary(**row)
            cocktails.append(cocktail)
        return cocktails