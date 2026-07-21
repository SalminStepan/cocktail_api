import pytest

from app.exceptions import DatabaseUnavailableError


CASES = [
    ("/health/db", "app.main.check_database_connection"),
    ("/cocktails", "app.routers.cocktails.get_cocktail_page"),
    ("/cocktails/search?q=gin", "app.routers.cocktails.search_cocktails"),
    ("/cocktails/36843", "app.routers.cocktails.get_cocktail_detail"),
    ("/ingredients/search?q=gin", "app.routers.ingredients.search_ingredients"),
    ("/stats", "app.routers.stats.get_stats"),
]


def raise_database_error(*args, **kwargs):
    raise DatabaseUnavailableError(
        "psycopg: connection refused at 127.0.0.1; DB_USER and DB_PASSWORD"
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
        "psycopg",
        "localhost",
        "127.0.0.1",
        "db_user",
        "db_password",
        "connection refused",
    ):
        assert secret not in response_text
