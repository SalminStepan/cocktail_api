from fastapi import APIRouter, Query
from fastapi import HTTPException

from app.services.cocktail_service import (
    get_cocktail_page, 
    get_cocktail_detail, 
    search_cocktails
)
from app.schemas.cocktail import CocktailSummary, CocktailPage
from app.schemas.ingredient import CocktailDetail


cocktails_router = APIRouter()

@cocktails_router.get("/cocktails")
def list_cocktails(
    page: int = Query(default=1, ge = 1),
    page_size: int = Query(default = 20, ge = 1, le = 100)
) -> CocktailPage:
    cocktails = get_cocktail_page(page, page_size)
    return cocktails

@cocktails_router.get("/cocktails/search")
def search_cocktails_endpoint(
    q: str = Query(min_length=3, max_length=100),
    page: int = Query(default=1, ge = 1),
    page_size: int = Query(default = 20, ge = 1, le = 100)
) -> list[CocktailSummary]:
    cocktails = search_cocktails(q, page, page_size)
    return cocktails
    
@cocktails_router.get("/cocktails/{cocktail_id}")
def get_cocktail(cocktail_id: int) -> CocktailDetail:
    cocktail = get_cocktail_detail(cocktail_id)

    if cocktail is None:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    
    return cocktail