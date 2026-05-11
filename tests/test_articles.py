from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_articles_main():
    response = client.get("/articles/")
    assert response.status_code == 200
