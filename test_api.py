import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("CALMA_API_URL", "https://calma-pepb.onrender.com")
EMAIL = os.getenv("CALMA_EMAIL")
PASSWORD = os.getenv("CALMA_PASSWORD")  

@pytest.fixture(scope="module")
def auth_headers():
    response = requests.post(
        f"{API_URL}/api/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=60,
    )
    assert response.ok, f"Login failed: {response.status_code} {response.text}"
    token = response.json().get("token")
    return {"Authorization": f"Bearer {token}"}

def test_login_returns_token(auth_headers):
    assert auth_headers["Authorization"].startswith("Bearer ")


def test_create_task_empty_title_rejected(auth_headers):
    body = {"title": "", "priority": "normal", "dueDate": None, "notes": ""}
    response = requests.post(
        f"{API_URL}/api/tasks", json=body, headers=auth_headers, timeout=60
    )
    assert 400 <= response.status_code < 500, (
        f"Expected a 4xx, got {response.status_code}: {response.text}"
    )