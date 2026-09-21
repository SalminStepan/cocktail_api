# SQLAlchemy: результаты репозитория — ORM-объекты с отношением ingredients.
from decimal import Decimal
from unittest.mock import Mock

from app.db.models import Cocktail, Ingredient
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
    "amount": Decimal("50"),
    "unit": "ml",
    "name": "Gin",
    "comment": None,
    "unresolved": False,
}


def test_get_cocktail_page_calculates_offset_and_builds_models(monkeypatch, db_session):
    received = {}

    def fake_summaries(session, limit, offset):
        received.update(session=session, limit=limit, offset=offset)
        return [Cocktail(**SUMMARY_ROW)]

    monkeypatch.setattr(cocktail_service, "get_cocktail_summaries", fake_summaries)
    monkeypatch.setattr(cocktail_service, "count_cocktails", lambda session: 11)

    result = cocktail_service.get_cocktail_page(page=2, page_size=5)

    assert received == {"session": db_session, "limit": 5, "offset": 5}
    assert result.items[0].name == "Gin Tonic"
    assert result.page == 2
    assert result.total == 11
    assert result.total_pages == 3


def test_get_cocktail_page_returns_empty_page(monkeypatch, db_session):
    monkeypatch.setattr(cocktail_service, "get_cocktail_summaries", lambda *args: [])
    monkeypatch.setattr(cocktail_service, "count_cocktails", lambda session: 7)

    result = cocktail_service.get_cocktail_page(page=99, page_size=5)

    assert result.items == []
    assert result.total == 7
    assert result.total_pages == 2


def test_search_cocktails_normalizes_query_and_calculates_pagination(
    monkeypatch, db_session
):
    received = {}

    def fake_search(session, query, limit, offset):
        received.update(session=session, query=query, limit=limit, offset=offset)
        return [Cocktail(**SUMMARY_ROW)]

    def fake_count(session, query):
        received["count_session"] = session
        received["count_query"] = query
        return 6

    monkeypatch.setattr(cocktail_service, "search_cocktail_summaries", fake_search)
    monkeypatch.setattr(
        cocktail_service, "count_cocktail_search_results", fake_count
    )

    result = cocktail_service.search_cocktails("  gin   tonic  ", page=2, page_size=5)

    assert received == {
        "session": db_session,
        "count_session": db_session,
        "query": "gin tonic",
        "limit": 5,
        "offset": 5,
        "count_query": "gin tonic",
    }
    assert result.items[0].name == "Gin Tonic"
    assert result.total_pages == 2


def test_empty_cocktail_search_does_not_open_database(monkeypatch):
    def fail():
        raise AssertionError("SessionLocal не должен вызываться")

    monkeypatch.setattr(cocktail_service, "SessionLocal", fail)

    result = cocktail_service.search_cocktails(" \t\n ", page=3, page_size=10)

    assert result.model_dump() == {
        "items": [],
        "page": 3,
        "page_size": 10,
        "total": 0,
        "total_pages": 0,
    }


def test_get_cocktail_detail_returns_none(monkeypatch, db_session):
    get_by_id = Mock(return_value=None)
    monkeypatch.setattr(cocktail_service, "get_cocktail_by_id", get_by_id)

    assert cocktail_service.get_cocktail_detail(999) is None
    get_by_id.assert_called_once_with(db_session, 999)


def test_get_cocktail_detail_builds_nested_ingredients(monkeypatch, db_session):
    cocktail = Cocktail(
        **DETAIL_ROW, ingredients=[Ingredient(**INGREDIENT_ROW)]
    )
    get_by_id = Mock(return_value=cocktail)
    monkeypatch.setattr(cocktail_service, "get_cocktail_by_id", get_by_id)

    result = cocktail_service.get_cocktail_detail(1)

    get_by_id.assert_called_once_with(db_session, 1)
    assert result is not None
    assert result.id == 1
    assert len(result.ingredients) == 1
    assert result.ingredients[0].name == "Gin"
    assert result.ingredients[0].amount == 50
