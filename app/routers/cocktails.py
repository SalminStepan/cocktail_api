from fastapi import APIRouter, Query

from app.services.cocktail_service import get_cocktail_page
from app.schemas.cocktail import CocktailSummary


cocktails_router = APIRouter()

@cocktails_router.get("/cocktails")
def list_cocktails(
    page: int = Query(default=1, ge = 1),
    page_size: int = Query(default = 20, ge = 1, le = 100)
) -> list[CocktailSummary]:
    cocktails = get_cocktail_page(page, page_size)
    return cocktails