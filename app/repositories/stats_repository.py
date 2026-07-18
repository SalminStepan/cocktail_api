def get_dataset_stats(conn) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            WITH cocktail_stats AS (
                SELECT
                    COUNT(*) AS cocktails_total,
                    COUNT(*) FILTER (
                        WHERE parse_status = 'ok'
                    ) AS parse_ok,
                    COUNT(*) FILTER (
                        WHERE parse_status = 'partial'
                    ) AS parse_partial,
                    COUNT(*) FILTER (
                        WHERE parse_status = 'failed'
                    ) AS parse_failed,
                    COUNT(*) FILTER (
                        WHERE image_url IS NOT NULL
                    ) AS cocktails_with_image,
                    COUNT(*) FILTER (
                        WHERE image_url IS NULL
                    ) AS cocktails_without_image
                FROM cocktails
            ),
            ingredient_stats AS (
                SELECT
                    COUNT(*) AS ingredients_total,
                    COUNT(*) FILTER (
                        WHERE unresolved = true
                    ) AS unresolved_ingredients
                FROM ingredients
            )
            SELECT
                cocktail_stats.cocktails_total,
                ingredient_stats.ingredients_total,
                cocktail_stats.parse_ok,
                cocktail_stats.parse_partial,
                cocktail_stats.parse_failed,
                ingredient_stats.unresolved_ingredients,
                cocktail_stats.cocktails_with_image,
                cocktail_stats.cocktails_without_image
            FROM cocktail_stats
            CROSS JOIN ingredient_stats;""")
        stats = cur.fetchone()
        return stats