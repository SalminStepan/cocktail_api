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

def search_ingredient_names(
    conn,
    query: str,
    limit: int,
    offset: int,
) -> list[dict]:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT
                i.name,
                COUNT(DISTINCT i.cocktail_id) AS cocktail_count
            FROM ingredients AS i
            WHERE i.name IS NOT NULL
            AND i.unresolved = false
            AND i.name ILIKE %s
            GROUP BY i.name
            ORDER BY cocktail_count DESC, i.name
            LIMIT %s
            OFFSET %s;""", (pattern, limit, offset))
        counted_ingredients = cur.fetchall()
        return counted_ingredients

def count_ingredient_search_results(conn, query: str) -> int:
    with conn.cursor() as cur:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT COUNT(DISTINCT i.name) AS total
            FROM ingredients AS i
            WHERE i.name IS NOT NULL
            AND i.unresolved = false
            AND i.name ILIKE %s;""", (pattern,))
        total = cur.fetchone()
        return total["total"]