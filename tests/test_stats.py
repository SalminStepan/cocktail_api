def stats_payload():
    return {
        "cocktails_total": 10,
        "ingredients_total": 35,
        "parse_status": {"ok": 7, "partial": 2, "failed": 1},
        "unresolved_ingredients": 3,
        "images": {"with_image": 8, "without_image": 2},
    }


def test_stats_returns_dataset_statistics(client, monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_stats", stats_payload)

    response = client.get("/stats")

    assert response.status_code == 200
    assert set(response.json()) == {
        "cocktails_total",
        "ingredients_total",
        "parse_status",
        "unresolved_ingredients",
        "images",
    }


def test_stats_contains_parse_status_breakdown(client, monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_stats", stats_payload)

    parse_status = client.get("/stats").json()["parse_status"]

    assert set(parse_status) == {"ok", "partial", "failed"}
    assert all(type(value) is int for value in parse_status.values())


def test_stats_contains_image_breakdown(client, monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_stats", stats_payload)

    images = client.get("/stats").json()["images"]

    assert set(images) == {"with_image", "without_image"}
    assert all(type(value) is int for value in images.values())


def test_stats_values_are_consistent(client, monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_stats", stats_payload)

    body = client.get("/stats").json()

    assert sum(body["parse_status"].values()) == body["cocktails_total"]
    assert sum(body["images"].values()) == body["cocktails_total"]
