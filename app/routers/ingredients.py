from fastapi import APIRouter, Query
from app.services.ingredient_service import search_ingredients
from app.schemas.ingredient import IngredientPage

ingredients_router = APIRouter()

@ingredients_router.get("/ingredients/search")
def search_ingredients_endpoint(    
    q: str = Query(min_length=2, max_length=100),
    page: int = Query(default=1, ge = 1),
    page_size: int = Query(default = 20, ge = 1, le = 100)
) -> IngredientPage:
    ingredients = search_ingredients(q, page, page_size)
    return ingredients