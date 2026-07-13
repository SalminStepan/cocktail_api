from pydantic import BaseModel


class CocktailSummary(BaseModel):
    id: int
    name: str
    image_url: str | None
    glass: str | None
    parse_status: str