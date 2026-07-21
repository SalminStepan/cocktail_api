import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def cocktail_summary() -> dict:
    return {
        "id": 36843,
        "name": "Gin Tonic",
        "image_url": "https://example.com/gin-tonic.jpg",
        "glass": "Highball glass",
        "parse_status": "ok",
    }


@pytest.fixture
def cocktail_detail(cocktail_summary: dict) -> dict:
    return {
        **cocktail_summary,
        "description": "A simple highball cocktail.",
        "garnish": "Lime wedge",
        "method": "Build over ice",
        "source_url": "https://example.com/cocktails/36843",
        "ingredients": [
            {
                "id": 1,
                "position": 1,
                "raw": "50 ml gin",
                "amount": "50",
                "unit": "ml",
                "name": "Gin",
                "comment": None,
                "unresolved": False,
            }
        ],
    }
