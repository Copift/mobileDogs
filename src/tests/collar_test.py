from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

userToken = client.post(url="/token/", json={"username": "test","password": "string"}).json()["token"]
print(userToken)
def test_read_collar():
    response = client.get("/collar/")
    assert response.status_code == 200


def test_read_collar_item():
    response = client.get("/collar/1/")
    assert response.status_code == 200


def test_create_collar():
    response = client.post("/collar/", json={"mac": "test_mac"})
    assert response.status_code == 201
    assert response.json()["mac"] == "test_mac"


def test_update_collar():
    response = client.put("/collar/1/", json={"mac": "updated_mac"})
    assert response.status_code == 200
    assert response.json()["mac"] == "updated_mac"


def test_delete_collar():
    response = client.delete("/collar/1/")
    assert response.status_code == 204