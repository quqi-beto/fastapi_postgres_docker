from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    TodoBase,
    TodoCreate,
    TodoUpdate,
    TodoResponse,
)


def test_user_create_schema():
    """Test UserCreate schema validation."""
    user_data = {"username": "testuser", "email": "test@example.com"}
    user = UserCreate(**user_data)

    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_user_create_schema_missing_fields():
    """Test UserCreate schema with missing fields."""
    with pytest.raises(ValidationError):
        UserCreate(username="testuser")  # missing email


def test_user_update_schema():
    """Test UserUpdate schema with optional fields."""
    update_data = {"username": "newuser"}
    update = UserUpdate(**update_data)

    assert update.username == "newuser"
    assert update.email is None


def test_user_response_schema():
    """Test UserResponse schema."""
    now = datetime.utcnow()
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "created_at": now,
    }
    user = UserResponse(**user_data)

    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_todo_create_schema():
    """Test TodoCreate schema validation."""
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "user_id": 1,
    }
    todo = TodoCreate(**todo_data)

    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo"
    assert todo.user_id == 1


def test_todo_create_schema_missing_required():
    """Test TodoCreate schema with missing required field."""
    with pytest.raises(ValidationError):
        TodoCreate(description="Test", user_id=1)  # missing title


def test_todo_update_schema():
    """Test TodoUpdate schema with optional fields."""
    update_data = {"completed": True}
    update = TodoUpdate(**update_data)

    assert update.completed is True
    assert update.title is None
    assert update.description is None


def test_todo_response_schema():
    """Test TodoResponse schema."""
    now = datetime.utcnow()
    todo_data = {
        "id": 1,
        "title": "Test Todo",
        "description": "This is a test",
        "user_id": 1,
        "completed": False,
        "created_at": now,
        "updated_at": now,
        "date_completed": None,
    }
    todo = TodoResponse(**todo_data)

    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.completed is False
    assert todo.date_completed is None
