import pytest


@pytest.fixture(autouse=True)
def services_must_not_be_called(monkeypatch):
    def fail(*args, **kwargs):
        pytest.fail("Service не должен вызываться при ошибке валидации")

    monkeypatch.setattr("app.routers.cocktails.get_cocktail_page", fail)
    monkeypatch.setattr("app.routers.cocktails.search_cocktails", fail)
    monkeypatch.setattr("app.routers.cocktails.get_cocktail_detail", fail)
    monkeypatch.setattr("app.routers.ingredients.search_ingredients", fail)


@pytest.mark.parametrize(
    "url",
    [
        "/cocktails?page=0",
        "/cocktails?page_size=0",
        "/cocktails?page_size=101",
        "/cocktails/search",
        "/cocktails/search?q=gi",
        "/cocktails/search?q=gin&page=0",
        "/cocktails/search?q=gin&page_size=101",
        "/cocktails/abc",
        "/ingredients/search",
        "/ingredients/search?q=g",
        "/ingredients/search?q=gin&page=0",
        "/ingredients/search?q=gin&page_size=101",
    ],
)
def test_invalid_parameters_return_422_without_calling_service(client, url):
    response = client.get(url)

    assert response.status_code == 422
    assert response.json()["detail"]
