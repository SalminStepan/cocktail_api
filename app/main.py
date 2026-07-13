#создать объект FastAPI
# подключить routers
import logging
from fastapi import FastAPI, HTTPException

from app.db.connection import check_database_connection
from app.routers.cocktails import cocktails_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cocktail API",
    version="0.1.0",
    description="Read API for cocktail recipes"
)
app.include_router(cocktails_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return{"status": "ok"}

@app.get("/health/db")
def database_health_check() -> dict[str, str]:
    if check_database_connection():
        return {"status": "ok", "database": "ok"}
    raise HTTPException(status_code=503, detail="Database unavailable")

