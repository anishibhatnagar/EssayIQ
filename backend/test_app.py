import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "EssayIQ Backend is running!"


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"


def test_analyze_valid_essay(client):
    essay = {
        "essay": (
            "Artificial intelligence is changing education. "
            "Students can use technology to learn more effectively. "
            "However, students should use technology responsibly."
        )
    }

    response = client.post(
        "/api/analyze",
        json=essay
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["word_count"] > 0
    assert data["sentence_count"] == 3
    assert data["overall_score"] >= 0
    assert data["overall_score"] <= 100


def test_analyze_empty_essay(client):
    response = client.post(
        "/api/analyze",
        json={"essay": ""}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data