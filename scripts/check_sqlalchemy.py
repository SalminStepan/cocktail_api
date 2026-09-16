from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import SessionLocal
from app.db.models import Cocktail
from app.repositories.cocktail_repository import get_cocktail_summaries, get_cocktail_by_id_orm


# with SessionLocal() as session:
#     stmt = select(Cocktail).limit(3)
#     cocktails = session.execute(stmt).scalars().all()

#     for cocktail in cocktails:
#         print(cocktail.id, cocktail.name)


# with SessionLocal() as session:
#     stmt = (
#         select(Cocktail)
#         .options(selectinload(Cocktail.ingredients))
#         .where(Cocktail.id == 36843)
#     )
#     cocktail = session.execute(stmt).scalar_one_or_none()

#     if cocktail is None:
#         print("Cocktail not found")
#     else:
#         print(cocktail.id, cocktail.name)
#         for ingredient in cocktail.ingredients:
#             print("-", ingredient.name, ingredient.amount, ingredient.unit, ingredient.comment)

# #
# with SessionLocal() as session:
#     cocktails = get_cocktail_summaries(session, limit=5, offset=0)

#     for cocktail in cocktails:
#         print(cocktail.id, cocktail.name)

with SessionLocal() as session:
    cocktail = get_cocktail_by_id_orm(session, cocktail_id=36843)

    print(cocktail.id)
    print(cocktail.name)

