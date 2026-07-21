from contextlib import nullcontext

from app.services import ingredient_service


def test_search_ingredients_normalizes_query_and_builds_page(monkeypatch):
    connection = object()
    monkeypatch.setattr(
        ingredient_service, "get_connection", lambda: nullcontext(connection)
    )
    received = {}

    def fake_search(conn, query, limit, offset):
        received.update(conn=conn, query=query, limit=limit, offset=offset)
        return [{"name": "London Dry Gin", "cocktail_count": 4}]

    def fake_count(conn, query):
        received["count_query"] = query
        return 11

    monkeypatch.setattr(ingredient_service, "search_ingredient_names", fake_search)
    monkeypatch.setattr(
        ingredient_service, "count_ingredient_search_results", fake_count
    )

    result = ingredient_service.search_ingredients(
        "  london   dry  ", page=2, page_size=5
    )

    assert received == {
        "conn": connection,
        "query": "london dry",
        "limit": 5,
        "offset": 5,
        "count_query": "london dry",
    }
    assert result.items[0].name == "London Dry Gin"
    assert result.items[0].cocktail_count == 4
    assert result.total == 11
    assert result.total_pages == 3


def test_empty_ingredient_search_does_not_call_repository(monkeypatch):
    def fail(*args):
        raise AssertionError("БД и repository не должны вызываться")

    monkeypatch.setattr(ingredient_service, "get_connection", fail)
    monkeypatch.setattr(ingredient_service, "search_ingredient_names", fail)
    monkeypatch.setattr(ingredient_service, "count_ingredient_search_results", fail)

    result = ingredient_service.search_ingredients("   ", page=4, page_size=10)

    assert result.model_dump() == {
        "items": [],
        "page": 4,
        "page_size": 10,
        "total": 0,
        "total_pages": 0,
    }


def test_search_ingredients_returns_empty_page_with_total(monkeypatch):
    monkeypatch.setattr(
        ingredient_service, "get_connection", lambda: nullcontext(object())
    )
    monkeypatch.setattr(ingredient_service, "search_ingredient_names", lambda *args: [])
    monkeypatch.setattr(
        ingredient_service, "count_ingredient_search_results", lambda *args: 8
    )

    result = ingredient_service.search_ingredients("gin", page=3, page_size=5)

    assert result.items == []
    assert result.page == 3
    assert result.total == 8
    assert result.total_pages == 2
