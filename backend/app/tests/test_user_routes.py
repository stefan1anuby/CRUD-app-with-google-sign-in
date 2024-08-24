import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import app  
from app.database import Base, engine

# Initialize the test client
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user_and_get_auth_token(setup_test_db):
    # Simulate a login callback to create a user and get tokens

    TEST_AUTH_CODE = "test-code"
    response = client.get(f"/users/auth/test/callback?code={TEST_AUTH_CODE}")
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    access_token = tokens["access_token"]
    assert access_token

    return access_token

def test_getting_user_info(setup_test_db):
    
    # Prepare user
    access_token = test_create_user_and_get_auth_token(setup_test_db)

    # Test getting the user info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    email = user_data["email"]
    assert email.startswith("testuser") and email.endswith("@example.com") 

def test_notes_for_user(setup_test_db):
    
    # Prepare user
    access_token = test_create_user_and_get_auth_token(setup_test_db)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test getting all notes from the user
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    notes = user_data["notes"]
    assert notes == []

    # Test adding a note
    note_to_add = {"content": "This is a test note"}
    response = client.post("/users/me/notes", json=note_to_add, headers=headers)
    assert response.status_code == 200
    note_data = response.json()
    assert note_data["content"] == "This is a test note"

    # Test getting all notes from the user after adding 1
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    notes_received = user_data["notes"]
    assert len(notes_received) == 1 
    assert notes_received[0]["content"] == note_to_add["content"]
    assert notes_received[0]["id"] is not None

    # Test deleting note
    note_received_id = notes_received[0]["id"]
    response = client.delete(f"/users/me/notes/{note_received_id}", headers=headers)
    assert response.status_code == 200

    # Test getting all notes from the user after deleting 1
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    notes_received = user_data["notes"]
    assert len(notes_received) == 0

def test_delete_user(setup_test_db):
    
    # Prepare user
    access_token = test_create_user_and_get_auth_token(setup_test_db)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test deleting the user
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 200
    deletion_data = response.json()
    assert deletion_data["message"] == "User account deleted successfully"

    # Test if I can use the account to connect again
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 401

def test_change_name_user(setup_test_db):
    # Prepare user
    access_token = test_create_user_and_get_auth_token(setup_test_db)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test deleting the user
    NEW_NAME = "new-test-name"
    response = client.put(f"/users/me/name?new_name={NEW_NAME}", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["name"] == NEW_NAME
