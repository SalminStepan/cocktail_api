def make_ingredient_page(items, page=1, page_size=20, total=None):
    total = len(items) if total is None else total
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
    }


def test_ingredient_search_returns_paginated_results(client, monkeypatch):
    item = {"name": "Gin", "cocktail_count": 14}
    monkeypatch.setattr(
        "app.routers.ingredients.search_ingredients",
        lambda query, page, page_size: make_ingredient_page(
            [item], page, page_size, total=6
        ),
    )

    response = client.get("/ingredients/search?q=gin")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"items", "page", "page_size", "total", "total_pages"}
    assert set(body["items"][0]) == {"name", "cocktail_count"}


def test_ingredient_search_count_is_integer(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.ingredients.search_ingredients",
        lambda query, page, page_size: make_ingredient_page(
            [{"name": "Gin", "cocktail_count": 14}]
        ),
    )

    count = client.get("/ingredients/search?q=gin").json()["items"][0][
        "cocktail_count"
    ]

    assert type(count) is int


def test_ingredient_search_returns_empty_result(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.ingredients.search_ingredients",
        lambda query, page, page_size: make_ingredient_page([], page, page_size),
    )

    body = client.get("/ingredients/search?q=salo-malo").json()

    assert body["items"] == []
    assert body["total"] == 0
    assert body["total_pages"] == 0


def test_ingredient_search_handles_whitespace(client, monkeypatch):
    def database_must_not_be_opened():
        raise AssertionError("Для пустого поиска соединение с БД не нужно")

    monkeypatch.setattr(
        "app.services.ingredient_service.get_connection", database_must_not_be_opened
    )

    response = client.get("/ingredients/search", params={"q": "  "})

    assert response.status_code == 200
    assert response.json() == make_ingredient_page([])


def test_ingredient_search_pagination(client, monkeypatch):
    received = []

    def fake_search(query, page, page_size):
        received.append((query, page, page_size))
        return make_ingredient_page(
            [{"name": "Gin", "cocktail_count": 14}], page, page_size, total=8
        )

    monkeypatch.setattr("app.routers.ingredients.search_ingredients", fake_search)

    first = client.get("/ingredients/search?q=gin&page=1&page_size=5").json()
    second = client.get("/ingredients/search?q=gin&page=2&page_size=5").json()

    assert received == [("gin", 1, 5), ("gin", 2, 5)]
    assert second["page"] == 2
    assert second["page_size"] == 5
    assert len(second["items"]) <= 5
    assert first["total"] == second["total"] == 8
