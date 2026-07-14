def get_cocktail_summaries(
    conn,
    limit: int,
    offset: int,
) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                name,
                image_url,
                glass,
                parse_status
            FROM cocktails
            ORDER BY id
            LIMIT %s
            OFFSET %s;""", (limit, offset)
        )
        cocktails = cur.fetchall()
        return cocktails
    
def get_cocktail_by_id(conn, cocktail_id :int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                name,
                description,
                image_url,
                glass,
                garnish,
                method,
                parse_status,
                source_url
            FROM cocktails
            WHERE id = %s;""",
            (cocktail_id,)
            )
        cocktail = cur.fetchone()
        return cocktail

def get_ingredients_by_cocktail_id(conn, cocktail_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                position,
                raw,
                amount,
                unit,
                name,
                comment,
                unresolved
            FROM ingredients
            WHERE cocktail_id = %s
            ORDER BY position;""", 
            (cocktail_id,)
            )
        ingredients = cur.fetchall()
        return ingredients