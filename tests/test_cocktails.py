def make_page(items, page=1, page_size=20, total=None):
    total = len(items) if total is None else total
    total_pages = (total + page_size - 1) // page_size
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


def test_cocktail_list_returns_paginated_response(
    client, monkeypatch, cocktail_summary
):
    monkeypatch.setattr(
        "app.routers.cocktails.get_cocktail_page",
        lambda page, page_size: make_page([cocktail_summary], total=23),
    )

    response = client.get("/cocktails")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"items", "page", "page_size", "total", "total_pages"}
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["total"] == 23
    assert body["total_pages"] == 2
    assert set(body["items"][0]) == {
        "id",
        "name",
        "image_url",
        "glass",
        "parse_status",
    }


def test_cocktail_list_passes_pagination_parameters(
    client, monkeypatch, cocktail_summary
):
    received = {}

    def fake_page(page, page_size):
        received.update(page=page, page_size=page_size)
        return make_page([cocktail_summary], page, page_size, total=6)

    monkeypatch.setattr("app.routers.cocktails.get_cocktail_page", fake_page)

    body = client.get("/cocktails?page=2&page_size=5").json()

    assert received == {"page": 2, "page_size": 5}
    assert body["page"] == 2
    assert body["page_size"] == 5
    assert len(body["items"]) <= 5


def test_cocktail_list_returns_empty_page(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.cocktails.get_cocktail_page",
        lambda page, page_size: make_page([], page, page_size, total=42),
    )

    body = client.get("/cocktails?page=1000000").json()

    assert body["items"] == []
    assert body["total"] == 42
    assert body["total_pages"] == 3


def test_cocktail_search_returns_paginated_results(
    client, monkeypatch, cocktail_summary
):
    monkeypatch.setattr(
        "app.routers.cocktails.search_cocktails",
        lambda query, page, page_size: make_page(
            [cocktail_summary], page, page_size, total=7
        ),
    )

    response = client.get("/cocktails/search?q=gin")

    assert response.status_code == 200
    assert response.json() == make_page([cocktail_summary], total=7)


def test_cocktail_search_returns_empty_result(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.cocktails.search_cocktails",
        lambda query, page, page_size: make_page([], page, page_size, total=0),
    )

    response = client.get("/cocktails/search?q=salo-malo")

    assert response.status_code == 200
    assert response.json() == make_page([])


def test_cocktail_search_preserves_total_between_pages(
    client, monkeypatch, cocktail_summary
):
    def fake_search(query, page, page_size):
        return make_page([cocktail_summary], page, page_size, total=12)

    monkeypatch.setattr("app.routers.cocktails.search_cocktails", fake_search)

    first = client.get("/cocktails/search?q=gin&page=1&page_size=5").json()
    second = client.get("/cocktails/search?q=gin&page=2&page_size=5").json()

    assert first["total"] == second["total"] == 12
    assert first["total_pages"] == second["total_pages"] == 3
    assert (first["page"], second["page"]) == (1, 2)


def test_cocktail_search_handles_whitespace_query(client, monkeypatch):
    def database_must_not_be_opened():
        raise AssertionError("Для пустого поиска соединение с БД не нужно")

    monkeypatch.setattr(
        "app.services.cocktail_service.get_connection", database_must_not_be_opened
    )

    response = client.get("/cocktails/search", params={"q": "   "})

    assert response.status_code == 200
    assert response.json() == make_page([])


def test_cocktail_detail_returns_cocktail(client, monkeypatch, cocktail_detail):
    monkeypatch.setattr(
        "app.routers.cocktails.get_cocktail_detail",
        lambda cocktail_id: cocktail_detail,
    )

    response = client.get("/cocktails/36843")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "id",
        "name",
        "description",
        "image_url",
        "glass",
        "garnish",
        "method",
        "parse_status",
        "source_url",
        "ingredients",
    }
    assert body["id"] == 36843


def test_cocktail_detail_contains_ingredients(
    client, monkeypatch, cocktail_detail
):
    monkeypatch.setattr(
        "app.routers.cocktails.get_cocktail_detail",
        lambda cocktail_id: cocktail_detail,
    )

    ingredient = client.get("/cocktails/36843").json()["ingredients"][0]

    assert set(ingredient) == {
        "id",
        "position",
        "raw",
        "amount",
        "unit",
        "name",
        "comment",
        "unresolved",
    }
    assert ingredient["unresolved"] is False


def test_cocktail_detail_returns_404(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.cocktails.get_cocktail_detail", lambda cocktail_id: None
    )

    response = client.get("/cocktails/999999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cocktail not found"}
