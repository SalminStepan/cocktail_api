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
    
def search_cocktail_summaries(
        conn, 
        query: str,
        limit: int,
        offset: int
) -> list[dict]:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT DISTINCT
                c.id,
                c.name,
                c.image_url,
                c.glass,
                c.parse_status
            FROM cocktails AS c
            LEFT JOIN ingredients AS i
                ON i.cocktail_id = c.id
            WHERE c.name ILIKE %s
            OR i.name ILIKE %s
            OR i.raw ILIKE %s
            ORDER BY c.id
            LIMIT %s
            OFFSET %s;""", (pattern, pattern, pattern, limit, offset))
        cocktails = cur.fetchall()
        return cocktails