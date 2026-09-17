from app.db.connection import get_connection
from app.repositories.cocktail_repository import (
    get_cocktail_summaries,
    get_cocktail_summaries_orm,
    count_cocktails,
    count_cocktails_orm,
    search_cocktail_summaries_orm,
    search_cocktail_summaries,
    count_cocktail_search_results,
    count_cocktail_search_results_orm
    
)
from app.services.cocktail_service import (
    get_cocktail_page, 
    get_cocktail_page_orm, 
    get_cocktail_detail_orm, 
    get_cocktail_detail,
    search_cocktails_orm,
    search_cocktails
)
from app.db.session import SessionLocal

limit = 5
offset =0 
# query = "rum"
# query = "gin"
# query = "lime"
query = "zzzzzzzz"

# with get_connection() as conn:
#     old_cocktails = get_cocktail_summaries(conn, limit, offset)

# with SessionLocal() as session:
#     new_cocktails = get_cocktail_summaries_orm(session, limit, offset)

# old_rows = [
#     {
#         "id": cocktail["id"],
#         "name": cocktail["name"],
#         "image_url": cocktail["image_url"],
#         "glass": cocktail["glass"],
#         "parse_status": cocktail["parse_status"],
#     }
#     for cocktail in old_cocktails
# ]

# new_rows = [
#     {
#         "id": cocktail.id,
#         "name": cocktail.name,
#         "image_url": cocktail.image_url,
#         "glass": cocktail.glass,
#         "parse_status": cocktail.parse_status,
#     }
#     for cocktail in new_cocktails
# ]

# print(old_rows == new_rows)


# with get_connection() as conn:
#     old_total = count_cocktails(conn)

# with SessionLocal() as session:
#     new_total = count_cocktails_orm(session)

# print(old_total)
# print(new_total)
# print(old_total == new_total)


# old_page = get_cocktail_page(page=1, page_size=5)
# new_page = get_cocktail_page_orm(page=1, page_size=5)

# print(old_page == new_page)
# print(old_page.model_dump() == new_page.model_dump())


# old_cocktail = get_cocktail_detail(cocktail_id=36843)
# new_cocktail = get_cocktail_detail_orm(cocktail_id=36843)

# print(old_cocktail)
# print(new_cocktail)

# print(old_cocktail == new_cocktail)



# with get_connection() as conn:
#     old = search_cocktail_summaries(conn, query, limit, offset)
#     old_data = [(row["id"], row["name"]) for row in old]
    

# with SessionLocal() as session:
#     new = search_cocktail_summaries_orm(session, query, limit, offset)
#     new_data = [(row.id, row.name) for row in new]

# print(old_data == new_data)

# with get_connection() as conn:
#     old_count_search = count_cocktail_search_results(conn, query)

# with SessionLocal() as session:
#     new_count_search = count_cocktail_search_results_orm(session, query)

# print(old_count_search == new_count_search)
# print(old_count_search, new_count_search)


old = search_cocktails("rum", page=1, page_size=5)
new = search_cocktails_orm("rum", page=1, page_size=5)

print(old.model_dump() == new.model_dump())