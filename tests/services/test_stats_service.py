from contextlib import nullcontext

from app.services import stats_service


def test_get_stats_builds_dataset_stats(monkeypatch):
    connection = object()
    monkeypatch.setattr(
        stats_service, "get_connection", lambda: nullcontext(connection)
    )
    repository_row = {
        "cocktails_total": 10,
        "ingredients_total": 35,
        "parse_ok": 7,
        "parse_partial": 2,
        "parse_failed": 1,
        "unresolved_ingredients": 3,
        "cocktails_with_image": 8,
        "cocktails_without_image": 2,
    }
    monkeypatch.setattr(
        stats_service, "get_dataset_stats", lambda conn: repository_row
    )

    result = stats_service.get_stats()

    assert result.cocktails_total == 10
    assert result.ingredients_total == 35
    assert result.parse_status.model_dump() == {"ok": 7, "partial": 2, "failed": 1}
    assert result.unresolved_ingredients == 3
    assert result.images.model_dump() == {"with_image": 8, "without_image": 2}
