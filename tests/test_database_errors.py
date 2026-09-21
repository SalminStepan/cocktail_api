import pytest
from sqlalchemy.exc import OperationalError

from app.exceptions import DatabaseUnavailableError


CASES = [
    ("/cocktails", "app.services.cocktail_service.SessionLocal"),
    ("/cocktails/search?q=gin", "app.services.cocktail_service.SessionLocal"),
    ("/cocktails/36843", "app.services.cocktail_service.SessionLocal"),
    ("/cocktails/by-name?name=Gin", "app.services.cocktail_service.SessionLocal"),
    ("/ingredients/search?q=gin", "app.services.ingredient_service.SessionLocal"),
    ("/stats", "app.services.stats_service.SessionLocal"),
]


def raise_database_error(*args, **kwargs):
    raise OperationalError(
        "SELECT 1",
        {},
        RuntimeError(
            "sqlalchemy: connection refused at 127.0.0.1; DB_USER and DB_PASSWORD"
        ),
    )


@pytest.mark.parametrize(("url", "dependency"), CASES)
def test_database_endpoints_return_503(client, monkeypatch, url, dependency):
    monkeypatch.setattr(dependency, raise_database_error)

    response = client.get(url)

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}


@pytest.mark.parametrize(("url", "dependency"), CASES)
def test_database_error_does_not_expose_internal_details(
    client, monkeypatch, url, dependency
):
    monkeypatch.setattr(dependency, raise_database_error)

    response_text = client.get(url).text.lower()

    for secret in (
        "sqlalchemy",
        "select 1",
        "localhost",
        "127.0.0.1",
        "db_user",
        "db_password",
        "connection refused",
    ):
        assert secret not in response_text


def test_legacy_database_error_returns_503(client, monkeypatch):
    def unavailable():
        raise DatabaseUnavailableError("secret connection details")

    monkeypatch.setattr("app.routers.stats.get_stats", unavailable)

    response = client.get("/stats")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
