from math import ceil

from app.repositories.cocktail_repository import (
    get_cocktail_summaries,
    count_cocktails,
    get_cocktail_by_id,
    search_cocktail_summaries,
    count_cocktail_search_results,
    get_cocktail_by_name,
)

from app.schemas.cocktail import CocktailSummary, CocktailPage
from app.schemas.ingredient import (
    CocktailDetail,
    IngredientRead,
)
from app.db.session import SessionLocal



def get_cocktail_page(
    page: int = 1,
    page_size: int = 20,
    
) -> CocktailPage:
    limit = page_size
    offset = (page - 1) * page_size
    with SessionLocal() as session:
        rows = get_cocktail_summaries(session, limit, offset)
        cocktails = []
        for row in rows:
            cocktail = CocktailSummary(
                id=row.id,
                name=row.name,
                image_url=row.image_url,
                glass=row.glass,
                parse_status=row.parse_status,
            )
            cocktails.append(cocktail)

        total_cocktails = count_cocktails(session)
        total_pages = ceil(total_cocktails / page_size)
        cocktail_page = CocktailPage(
            items = cocktails,
            page = page,
            page_size = page_size,
            total = total_cocktails,
            total_pages = total_pages
        )

        return cocktail_page

def get_cocktail_detail(cocktail_id: int) -> CocktailDetail | None:
    with SessionLocal() as session:
        row = get_cocktail_by_id(session, cocktail_id)
        if row is None:
            return None

        ingredients = []
        for ingredient in row.ingredients:
            ingredient_read = IngredientRead(
                id=ingredient.id,
                position=ingredient.position,
                raw=ingredient.raw,
                amount=ingredient.amount,
                unit=ingredient.unit,
                name=ingredient.name,
                comment=ingredient.comment,
                unresolved=ingredient.unresolved,
            )
            ingredients.append(ingredient_read)
        

        cocktail = CocktailDetail(    
            id=row.id,
            name=row.name,
            description=row.description,
            image_url=row.image_url,
            glass=row.glass,
            garnish=row.garnish,
            method=row.method,
            parse_status=row.parse_status,
            source_url=row.source_url,
            ingredients=ingredients,
            )
        return cocktail

def search_cocktails(
    query: str,
    page: int = 1,
    page_size: int = 20
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

    with SessionLocal() as session:
        rows = search_cocktail_summaries(session, query, limit, offset)
        cocktails = []
        for row in rows:
            cocktail = CocktailSummary(
                id=row.id,
                name=row.name,
                image_url=row.image_url,
                glass=row.glass,
                parse_status=row.parse_status
            )
            cocktails.append(cocktail)

        total_cocktails = count_cocktail_search_results(session, query)
        total_pages = ceil(total_cocktails / page_size)
        cocktail_page = CocktailPage(
            items=cocktails,
            page=page,
            page_size=page_size,
            total=total_cocktails,
            total_pages=total_pages
        )
        return cocktail_page

def get_cocktail_detail_by_name(name: str) -> CocktailDetail | None:
    name = " ".join(name.split())

    with SessionLocal() as session:
        row = get_cocktail_by_name(session, name)

        if row is None:
            return None

        ingredients = []
        for ingredient in row.ingredients:
            ingredient_read = IngredientRead(
                id=ingredient.id,
                position=ingredient.position,
                raw=ingredient.raw,
                amount=ingredient.amount,
                unit=ingredient.unit,
                name=ingredient.name,
                comment=ingredient.comment,
                unresolved=ingredient.unresolved,
            )
            ingredients.append(ingredient_read)

        cocktail = CocktailDetail(    
            id=row.id,
            name=row.name,
            description=row.description,
            image_url=row.image_url,
            glass=row.glass,
            garnish=row.garnish,
            method=row.method,
            parse_status=row.parse_status,
            source_url=row.source_url,
            ingredients=ingredients,
            )
        return cocktail