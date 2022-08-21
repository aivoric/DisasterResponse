from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200