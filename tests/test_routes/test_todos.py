from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_todo(client):
    """Test creating a new todo."""
    # Create a user first
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "user_id": user_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["user_id"] == user_id
    assert data["completed"] is False
    assert data["date_completed"] is None


def test_create_todo_invalid_user(client):
    """Test creating a todo with non-existent user."""
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "user_id": 9999,
        },
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_get_all_todos(client):
    """Test getting all todos."""
    # Create a user
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    # Create a few todos
    client.post(
        "/todos/",
        json={"title": "Todo 1", "user_id": user_id},
    )
    client.post(
        "/todos/",
        json={"title": "Todo 2", "user_id": user_id},
    )

    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_get_todo_by_id(client):
    """Test getting a todo by ID."""
    # Create a user
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    # Create a todo
    create_response = client.post(
        "/todos/",
        json={"title": "Test Todo", "user_id": user_id},
    )
    todo_id = create_response.json()["id"]

    # Get the todo
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"
    assert data["user_id"] == user_id


def test_get_todo_not_found(client):
    """Test getting a non-existent todo."""
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_todo_title(client):
    """Test updating a todo's title."""
    # Create a user and todo
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/todos/",
        json={"title": "Old Title", "user_id": user_id},
    )
    todo_id = create_response.json()["id"]

    # Update the todo
    response = client.put(f"/todos/{todo_id}", json={"title": "New Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is False


def test_update_todo_mark_completed(client):
    """Test marking a todo as completed."""
    # Create a user and todo
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/todos/",
        json={"title": "Test Todo", "user_id": user_id},
    )
    todo_id = create_response.json()["id"]

    # Mark as completed
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["date_completed"] is not None


def test_update_todo_mark_incomplete(client):
    """Test marking a todo as incomplete."""
    # Create a user and todo
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    # Create todo and mark as completed
    create_response = client.post(
        "/todos/",
        json={"title": "Test Todo", "user_id": user_id},
    )
    todo_id = create_response.json()["id"]

    client.put(f"/todos/{todo_id}", json={"completed": True})

    # Mark as incomplete
    response = client.put(f"/todos/{todo_id}", json={"completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False
    assert data["date_completed"] is None


def test_update_todo_not_found(client):
    """Test updating a non-existent todo."""
    response = client.put("/todos/9999", json={"title": "New Title"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_todo(client):
    """Test deleting a todo."""
    # Create a user and todo
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/todos/",
        json={"title": "Test Todo", "user_id": user_id},
    )
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    # Verify todo is deleted
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    """Test deleting a non-existent todo."""
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_user_cascades_delete_todos(client):
    """Test that deleting a user cascades delete to todos."""
    # Create a user
    user_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    user_id = user_response.json()["id"]

    # Create a todo
    todo_response = client.post(
        "/todos/",
        json={"title": "Test Todo", "user_id": user_id},
    )
    todo_id = todo_response.json()["id"]

    # Delete the user
    client.delete(f"/users/{user_id}")

    # Verify todo is also deleted
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
