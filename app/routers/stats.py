from fastapi import APIRouter, Query
from app.schemas.stats import DatasetStats
from app.services.stats_service import get_stats


stats_router = APIRouter()

@stats_router.get("/stats")
def dataset_stats() -> DatasetStats:
    stats = get_stats()
    return stats