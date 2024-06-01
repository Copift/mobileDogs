import unittest

from starlette.testclient import TestClient

from logger import logger
from main import app
from users import schemas


class TestUserRouter(unittest.TestCase):
    """
    Test the user/router.py file.
    """
    app = TestClient(app)

    def test_add_user(self):
        """
        Test the add_user function.
        """
        logger.info(f"Testing add_user function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        assert response.status_code == 200
        assert response.json()["email"] == "test_email"

    def test_add_support_user(self):
        """
        Test the add_support_user function.
        """
        logger.info(f"Testing add_support_user function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add_support/", json=test_user)
        assert response.status_code == 200
        assert response.json()["email"] == "test_email"

    def test_login_for_access_token(self):
        """
        Test the login_for_access_token function.
        """
        logger.info(f"Testing login_for_access_token function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/token", json={"username": "test_email", "password": "test_password"})
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_get_user_details(self):
        """
        Test the get_user_details function.
        """
        logger.info(f"Testing get_user_details function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        user_id = response.json()["id"]
        response =  app.get(f"/user/me/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "test_email"

    def test_add_collar(self):
        """
        Test the add_collar function.
        """
        logger.info(f"Testing add_collar function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        user_id = response.json()["id"]
        collar = schemas.Collar(mac="test_mac", description="test_description")
        response =  app.post(f"/user/add_collar/{user_id}", json=collar)
        assert response.status_code == 200
        assert response.json()["mac"] == "test_mac"

    def test_add_alert(self):
        """
        Test the add_alert function.
        """
        logger.info(f"Testing add_alert function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        user_id = response.json()["id"]
        alert = schemas.Alert(description="test_description")
        response =  app.post(f"/user/add_alert/{user_id}", json=alert)
        assert response.status_code == 200
        assert response.json()["description"] == "test_description"
        import unittest
        from main import app



    def test_get_user_by_id(self):
        """
        Test the get_user_by_id function.
        """
        logger.info(f"Testing get_user_by_id function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        user_id = response.json()["id"]
        response =  app.get(f"/user/get_user_by_id/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "test_email"

    def test_get_own_collars(self):
        """
        Test the get_own_collars function.
        """
        logger.info(f"Testing get_own_collars function")
        test_user = schemas.UserAdd(email="test_email", password="test_password")
        response =  app.post("/user/add/", json=test_user)
        user_id = response.json()["id"]
        response =  app.get(f"/user/me/collars/{user_id}")
        assert response.status_code == 200
        assert len(response.json()) > 0