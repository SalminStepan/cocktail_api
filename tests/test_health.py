from sqlalchemy.exc import OperationalError

from app.db.session import check_database_connection


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_returns_ok(client, monkeypatch):
    monkeypatch.setattr("app.main.check_database_connection", lambda: True)

    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_database_health_returns_503_when_database_unavailable(client, monkeypatch):
    monkeypatch.setattr("app.main.check_database_connection", lambda: False)

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}


def test_database_connection_returns_false_on_sqlalchemy_error(monkeypatch):
    def unavailable():
        raise OperationalError(None, None, RuntimeError("secret connection details"))

    monkeypatch.setattr("app.db.session.engine.connect", unavailable)

    assert check_database_connection() is False
