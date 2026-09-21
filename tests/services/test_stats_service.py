# SQLAlchemy: проверяем передачу сессии в репозиторий статистики.
from unittest.mock import Mock

from app.services import stats_service


def test_get_stats_builds_dataset_stats(monkeypatch, db_session):
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
    get_dataset_stats = Mock(return_value=repository_row)
    monkeypatch.setattr(stats_service, "get_dataset_stats", get_dataset_stats)

    result = stats_service.get_stats()

    get_dataset_stats.assert_called_once_with(db_session)
    assert result.cocktails_total == 10
    assert result.ingredients_total == 35
    assert result.parse_status.model_dump() == {"ok": 7, "partial": 2, "failed": 1}
    assert result.unresolved_ingredients == 3
    assert result.images.model_dump() == {"with_image": 8, "without_image": 2}
