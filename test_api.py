import os
import time

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("CALMA_API_URL", "https://calma-pepb.onrender.com")


@pytest.fixture
def created_task_ids(auth_headers):
    ids = []
    yield ids  # the test runs here and adds ids to this list
    for task_id in ids:  # teardown: runs even if the test failed
        response = requests.delete(
            f"{API_URL}/api/tasks/{task_id}", headers=auth_headers, timeout=60
        )
        assert response.status_code == 204, f"Cleanup failed for {task_id}"


def test_login_returns_token(auth_headers):
    assert auth_headers["Authorization"].startswith("Bearer ")


def test_create_task_returns_201(auth_headers, created_task_ids):
    title = f"API Task {int(time.time())}"
    body = {"title": title, "priority": "normal", "dueDate": None, "notes": ""}
    response = requests.post(
        f"{API_URL}/api/tasks", json=body, headers=auth_headers, timeout=60
    )
    if response.ok:
        created_task_ids.append(response.json()["task"]["_id"])
    assert response.status_code == 201
    assert response.json()["task"]["title"] == title


def test_create_task_empty_title_rejected(auth_headers, created_task_ids):
    body = {"title": "", "priority": "normal", "dueDate": None, "notes": ""}
    response = requests.post(
        f"{API_URL}/api/tasks", json=body, headers=auth_headers, timeout=60
    )
    if response.ok:
        created_task_ids.append(response.json()["task"]["_id"])
    assert 400 <= response.status_code < 500, (
        f"Expected a 4xx, got {response.status_code}: {response.text}"
    )