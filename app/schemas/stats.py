from pydantic import BaseModel


class ParseStatusStats(BaseModel):
    ok: int
    partial: int
    failed: int

class ImageStats(BaseModel):
    with_image: int
    without_image: int

class DatasetStats(BaseModel):
    cocktails_total: int
    ingredients_total: int
    parse_status: ParseStatusStats
    unresolved_ingredients: int
    images: ImageStats