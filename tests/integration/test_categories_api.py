from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_categories():
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    cat = data[0]
    assert "id" in cat
    assert "name" in cat
    assert "icon" in cat
    assert "description" in cat


def test_category_hints():
    response = client.get("/api/v1/categories/游戏/hints")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "游戏"
    assert "context_keywords" in data
    assert len(data["context_keywords"]) > 0
    assert "hook_patterns" in data


def test_category_hints_invalid():
    response = client.get("/api/v1/categories/invalid/hints")
    assert response.status_code == 404


def test_reload_categories():
    response = client.post("/api/v1/categories/reload")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
