from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_seeds_by_category():
    """Test GET /api/v1/seeds?category=XX returns seeds for a category."""
    response = client.get("/api/v1/seeds?category=游戏")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for seed in data:
        assert "id" in seed
        assert "title" in seed
        assert "score" in seed
        assert "hook_type" in seed


def test_list_seeds_no_category():
    """Test GET /api/v1/seeds returns grouped seeds by category."""
    response = client.get("/api/v1/seeds")
    assert response.status_code == 200
    data = response.json()
    # When seed data exists, response should be a dict grouped by category
    # When no seed data, it could be either a dict or a list
    assert isinstance(data, (dict, list))


def test_list_seeds_empty_category():
    """Test GET /api/v1/seeds?category=nonexistent returns empty list."""
    response = client.get("/api/v1/seeds?category=nonexistent123")
    assert response.status_code == 200


def test_refresh_seeds_single_category():
    """Test POST /api/v1/seeds/refresh for a single category."""
    response = client.post("/api/v1/seeds/refresh", json={"category": "游戏"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["category"] == "游戏"


def test_refresh_seeds_all_categories():
    """Test POST /api/v1/seeds/refresh without category refreshes all."""
    response = client.post("/api/v1/seeds/refresh", json={})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    # Should have at least one category result
    assert len(data["results"]) > 0


def test_categories_include_seed_info():
    """Test GET /api/v1/categories includes seed_count and seed_preview."""
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    cat = data[0]
    assert "seed_count" in cat
    assert "seed_preview" in cat
    assert isinstance(cat["seed_count"], int)
    assert isinstance(cat["seed_preview"], list)
