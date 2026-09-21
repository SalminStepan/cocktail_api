from app.schemas.stats import DatasetStats, ParseStatusStats, ImageStats
from app.repositories.stats_repository import get_dataset_stats
from app.db.session import SessionLocal


def get_stats() -> DatasetStats:
    with SessionLocal() as session:

        rows = get_dataset_stats(session)

        parse_stats = ParseStatusStats(
            ok = rows["parse_ok"],
            partial = rows["parse_partial"],
            failed = rows["parse_failed"],
        )
        image_stats = ImageStats(
            with_image = rows["cocktails_with_image"],
            without_image = rows["cocktails_without_image"],
        )
        
        dataset_stats = DatasetStats(
            cocktails_total = rows["cocktails_total"],
            ingredients_total = rows["ingredients_total"],
            parse_status = parse_stats,
            unresolved_ingredients = rows["unresolved_ingredients"],
            images = image_stats
        )

        return dataset_stats