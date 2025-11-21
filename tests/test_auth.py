import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/api/v1/auth/login", json={
        "email": "ana@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data

def test_login_invalid():
    response = client.post("/api/v1/auth/login", json={
        "email": "invalid@test.com",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_forgot_password():
    response = client.post("/api/v1/auth/forgot-password", json={
        "email": "ana@test.com"
    })
    assert response.status_code == 200