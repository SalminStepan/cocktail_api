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