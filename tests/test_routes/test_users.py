from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user(client):
    """Test creating a new user."""
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_username(client):
    """Test creating a user with duplicate username."""
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test1@example.com"},
    )
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test2@example.com"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_create_user_duplicate_email(client):
    """Test creating a user with duplicate email."""
    client.post(
        "/users/",
        json={"username": "user1", "email": "test@example.com"},
    )
    response = client.post(
        "/users/",
        json={"username": "user2", "email": "test@example.com"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_get_all_users(client):
    """Test getting all users."""
    # Create a few users
    client.post("/users/", json={"username": "user1", "email": "user1@example.com"})
    client.post("/users/", json={"username": "user2", "email": "user2@example.com"})

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_get_user_by_id(client):
    """Test getting a user by ID."""
    # Create a user
    create_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = create_response.json()["id"]

    # Get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_user_not_found(client):
    """Test getting a non-existent user."""
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_user(client):
    """Test updating a user."""
    # Create a user
    create_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = create_response.json()["id"]

    # Update the user
    response = client.put(
        f"/users/{user_id}",
        json={"username": "newuser", "email": "new@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"


def test_update_user_partial(client):
    """Test partial update of a user."""
    # Create a user
    create_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = create_response.json()["id"]

    # Update only username
    response = client.put(f"/users/{user_id}", json={"username": "newuser"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "test@example.com"  # Should remain unchanged


def test_update_user_not_found(client):
    """Test updating a non-existent user."""
    response = client.put("/users/9999", json={"username": "newuser"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_user(client):
    """Test deleting a user."""
    # Create a user
    create_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_delete_user_not_found(client):
    """Test deleting a non-existent user."""
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
