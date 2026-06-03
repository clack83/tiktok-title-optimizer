from fastapi.testclient import TestClient
from unittest.mock import patch

from app.core.database import get_db
from main import app


def override_get_db():
    # Return a mock for simple API structure tests
    from tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_invalid_password():
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "short",
    })
    assert response.status_code == 422


def test_register_no_email():
    response = client.post("/api/v1/auth/register", json={
        "password": "StrongPass123!",
    })
    assert response.status_code == 422


def test_login_invalid_credentials():
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexist@test.com",
        "password": "WrongPass123!",
    })
    assert response.status_code == 401


def test_score_endpoint():
    response = client.post("/api/v1/optimize/score", json={
        "title": "测试标题"
    })
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "explanations" in data
    assert len(data["explanations"]) == 4


def test_score_empty_title():
    response = client.post("/api/v1/optimize/score", json={"title": ""})
    assert response.status_code == 422


def test_keywords_endpoint():
    response = client.post("/api/v1/optimize/keywords", json={
        "title": "新手必看的5个手机摄影技巧"
    })
    assert response.status_code == 200
    data = response.json()
    assert "keywords" in data
    assert "matched_topics" in data
