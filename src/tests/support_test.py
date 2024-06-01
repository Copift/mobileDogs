from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_support():
    response = client.get("/support/")
    assert response.status_code == 200


def test_read_support_item():
    response = client.get("/support/1/")
    assert response.status_code == 200


def test_create_support():
    response = client.post("/support/", json={"email": "test_email", "password": "test_password"})
    assert response.status_code == 201
    assert response.json()["email"] == "test_email"


def test_update_support():
    response = client.put("/support/1/", json={"email": "updated_email"})
    assert response.status_code == 200
    assert response.json()["email"] == "updated_email"


def test_delete_support():
    response = client.delete("/support/1/")
    assert response.status_code == 204