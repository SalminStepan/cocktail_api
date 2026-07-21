from app.exceptions import DatabaseUnavailableError


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
    def unavailable() -> bool:
        raise DatabaseUnavailableError("secret connection details")

    monkeypatch.setattr("app.main.check_database_connection", unavailable)

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
