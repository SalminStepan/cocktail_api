# SQLAlchemy: сервисы используют SessionLocal; общий мок исключает доступ к реальной БД.
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.services import cocktail_service, ingredient_service, stats_service


@pytest.fixture
def db_session(monkeypatch):
    session = MagicMock(spec=Session)
    session.__enter__.return_value = session
    for service in (cocktail_service, ingredient_service, stats_service):
        monkeypatch.setattr(service, "SessionLocal", lambda: session)
    return session
