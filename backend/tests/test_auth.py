import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app, get_db
from backend.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_signup_duplicate_email():
    # First signup
    client.post("/api/auth/signup", json={"email": "test@example.com", "password": "password", "name": "Test User"})
    # Second signup with same email
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "password", "name": "Test User"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_invalid_password():
    client.post("/api/auth/signup", json={"email": "test2@example.com", "password": "password", "name": "Test User"})
    response = client.post("/api/auth/login", json={"email": "test2@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
