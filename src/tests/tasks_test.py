import unittest

from starlette.testclient import TestClient

from logger import logger
from main import app
from tasks import schemas


class TestTasksRouter(unittest.TestCase):
    """
    Test the tasks/router.py file.
    """
    app = TestClient(app)

    def test_add_task(self):
        """
        Test the add_task function.
        """
        logger.info(f"Testing add_task function")
        test_task = schemas.TaskBase(task_name="test_task", task_description="test_description")
        response = self.app.post("/tasks/add_task/", json=test_task)
        assert response.status_code == 200
        assert response.json()["task_name"] == "test_task"

    def test_get_task_list(self):
        """
        Test the get_task_list function.
        """
        logger.info(f"Testing get_task_list function")
        test_task = schemas.TaskBase(task_name="test_task", task_description="test_description")
        response = self.app.post("/tasks/add_task/", json=test_task)
        task_id = response.json()["id"]
        response = self.app.get("/tasks/get_task_list/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_task_list_available(self):
        """
        Test the get_task_list_available function.
        """
        logger.info(f"Testing get_task_list_available function")
        test_task = schemas.TaskBase(task_name="test_task", task_description="test_description")
        response = self.app.post("/tasks/add_task/", json=test_task)
        task_id = response.json()["id"]
        response = self.app.get("/tasks/get_task_list_available/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_task_statuses(self):
        """
        Test the get_task_statuses function.
        """
        logger.info(f"Testing get_task_statuses function")
        test_task = schemas.TaskBase(task_name="test_task", task_description="test_description")
        response = self.app.post("/tasks/add_task/", json=test_task)
        task_id = response.json()["id"]
        response = self.app.get(f"/tasks/get_task_statuses/{task_id}")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_task_types(self):
        """
        Test the get_task_types function.
        """
        logger.info(f"Testing get_task_types function")
        response = self.app.get("/tasks/get_task_types/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_task_types_available(self):
        """
        Test the get_task_types_available function.
        """
        logger.info(f"Testing get_task_types_available function")
        response = self.app.get("/tasks/get_task_types_available/")
        assert response.status_code == 200
        assert len(response.json()) > 0