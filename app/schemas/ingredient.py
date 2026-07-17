from pydantic import BaseModel
from decimal import Decimal


class IngredientRead(BaseModel):
    id: int
    position: int
    raw: str
    amount: Decimal | None
    unit: str | None
    name: str | None
    comment: str | None
    unresolved: bool

class CocktailDetail(BaseModel):
    id: int
    name: str
    description: str | None
    image_url: str | None
    glass: str | None
    garnish: str | None
    method: str | None
    parse_status: str
    source_url: str | None
    ingredients: list[IngredientRead]

class IngredientSearchResult(BaseModel):
    name: str
    cocktail_count: int