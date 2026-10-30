import os
import time

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("CALMA_API_URL", "https://calma-pepb.onrender.com")
EMAIL = os.getenv("CALMA_EMAIL")
PASSWORD = os.getenv("CALMA_PASSWORD")


@pytest.fixture(scope="session")
def auth_headers():
    response = requests.post(
        f"{API_URL}/api/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=60,
    )
    assert response.ok, f"Login failed: {response.status_code} {response.text}"
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def unique_title(auth_headers):
    title = f"Test Task {int(time.time())}"
    yield title  # the UI test creates a task with this title
    # teardown: find the task by title through the API and delete it
    response = requests.get(f"{API_URL}/api/tasks", headers=auth_headers, timeout=60)
    assert response.ok, f"Could not list tasks: {response.status_code}"
    for task in response.json()["tasks"]:
        if task["title"] == title:
            delete = requests.delete(
                f"{API_URL}/api/tasks/{task['_id']}",
                headers=auth_headers,
                timeout=60,
            )
            assert delete.status_code == 204, f"Cleanup failed for {task['_id']}"