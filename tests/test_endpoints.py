import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    response = client.post("/api/v1/auth/login", json={
        "email": "ana@test.com",
        "password": "123456"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_patients_list(auth_headers):
    response = client.get("/api/v1/patients/", headers=auth_headers)
    assert response.status_code == 200

def test_psychologists_list():
    response = client.get("/api/v1/psychologists/")
    assert response.status_code == 200

def test_appointments_list(auth_headers):
    response = client.get("/api/v1/appointments/", headers=auth_headers)
    assert response.status_code == 200

def test_requests_list(auth_headers):
    response = client.get("/api/v1/requests/", headers=auth_headers)
    assert response.status_code == 200

def test_schedule_list(auth_headers):
    response = client.get("/api/v1/schedule/", headers=auth_headers)
    assert response.status_code == 200

def test_notifications_list(auth_headers):
    response = client.get("/api/v1/notifications/", headers=auth_headers)
    assert response.status_code == 200

def test_dashboard_psychologist(auth_headers):
    response = client.get("/api/v1/dashboard/psychologist", headers=auth_headers)
    assert response.status_code == 200

def test_analytics_overview(auth_headers):
    response = client.get("/api/v1/analytics/overview", headers=auth_headers)
    assert response.status_code == 200

def test_search(auth_headers):
    response = client.get("/api/v1/search/?q=test", headers=auth_headers)
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200