#создать объект FastAPI
#зарегистрировать health endpoint

from fastapi import FastAPI

app = FastAPI(
    title="Cocktail API",
    version="0.1.0",
    description="Read API for cocktail recipes"
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return{"status": "ok"}

