from contextlib import nullcontext

from app.services import cocktail_service


SUMMARY_ROW = {
    "id": 1,
    "name": "Gin Tonic",
    "image_url": None,
    "glass": "Highball",
    "parse_status": "ok",
}

DETAIL_ROW = {
    **SUMMARY_ROW,
    "description": None,
    "garnish": "Lime",
    "method": "Build",
    "source_url": None,
}

INGREDIENT_ROW = {
    "id": 10,
    "position": 1,
    "raw": "50 ml gin",
    "amount": "50",
    "unit": "ml",
    "name": "Gin",
    "comment": None,
    "unresolved": False,
}


def use_fake_connection(monkeypatch):
    connection = object()
    monkeypatch.setattr(
        cocktail_service, "get_connection", lambda: nullcontext(connection)
    )
    return connection


def test_get_cocktail_page_calculates_offset_and_builds_models(monkeypatch):
    connection = use_fake_connection(monkeypatch)
    received = {}

    def fake_summaries(conn, limit, offset):
        received.update(conn=conn, limit=limit, offset=offset)
        return [SUMMARY_ROW]

    monkeypatch.setattr(cocktail_service, "get_cocktail_summaries", fake_summaries)
    monkeypatch.setattr(cocktail_service, "count_cocktails", lambda conn: 11)

    result = cocktail_service.get_cocktail_page(page=2, page_size=5)

    assert received == {"conn": connection, "limit": 5, "offset": 5}
    assert result.items[0].name == "Gin Tonic"
    assert result.page == 2
    assert result.total == 11
    assert result.total_pages == 3


def test_get_cocktail_page_returns_empty_page(monkeypatch):
    use_fake_connection(monkeypatch)
    monkeypatch.setattr(cocktail_service, "get_cocktail_summaries", lambda *args: [])
    monkeypatch.setattr(cocktail_service, "count_cocktails", lambda conn: 7)

    result = cocktail_service.get_cocktail_page(page=99, page_size=5)

    assert result.items == []
    assert result.total == 7
    assert result.total_pages == 2


def test_search_cocktails_normalizes_query_and_calculates_pagination(monkeypatch):
    use_fake_connection(monkeypatch)
    received = {}

    def fake_search(conn, query, limit, offset):
        received.update(query=query, limit=limit, offset=offset)
        return [SUMMARY_ROW]

    def fake_count(conn, query):
        received["count_query"] = query
        return 6

    monkeypatch.setattr(cocktail_service, "search_cocktail_summaries", fake_search)
    monkeypatch.setattr(
        cocktail_service, "count_cocktail_search_results", fake_count
    )

    result = cocktail_service.search_cocktails("  gin   tonic  ", page=2, page_size=5)

    assert received == {
        "query": "gin tonic",
        "limit": 5,
        "offset": 5,
        "count_query": "gin tonic",
    }
    assert result.items[0].name == "Gin Tonic"
    assert result.total_pages == 2


def test_empty_cocktail_search_does_not_open_database(monkeypatch):
    def fail():
        raise AssertionError("get_connection не должен вызываться")

    monkeypatch.setattr(cocktail_service, "get_connection", fail)

    result = cocktail_service.search_cocktails(" \t\n ", page=3, page_size=10)

    assert result.model_dump() == {
        "items": [],
        "page": 3,
        "page_size": 10,
        "total": 0,
        "total_pages": 0,
    }


def test_get_cocktail_detail_keeps_none_and_skips_ingredients(monkeypatch):
    use_fake_connection(monkeypatch)
    monkeypatch.setattr(cocktail_service, "get_cocktail_by_id", lambda *args: None)

    def fail(*args):
        raise AssertionError("Ингредиенты отсутствующего коктейля запрашивать не нужно")

    monkeypatch.setattr(cocktail_service, "get_ingredients_by_cocktail_id", fail)

    assert cocktail_service.get_cocktail_detail(999) is None


def test_get_cocktail_detail_builds_nested_ingredients(monkeypatch):
    use_fake_connection(monkeypatch)
    monkeypatch.setattr(
        cocktail_service, "get_cocktail_by_id", lambda conn, cocktail_id: DETAIL_ROW
    )
    monkeypatch.setattr(
        cocktail_service,
        "get_ingredients_by_cocktail_id",
        lambda conn, cocktail_id: [INGREDIENT_ROW],
    )

    result = cocktail_service.get_cocktail_detail(1)

    assert result is not None
    assert result.id == 1
    assert len(result.ingredients) == 1
    assert result.ingredients[0].name == "Gin"
    assert result.ingredients[0].amount == 50
