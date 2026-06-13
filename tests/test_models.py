from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models import User, Todo


def test_user_creation(db: Session):
    """Test creating a user."""
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.created_at is not None


def test_user_unique_username(db: Session):
    """Test that usernames must be unique."""
    user1 = User(username="testuser", email="test1@example.com")
    db.add(user1)
    db.commit()

    user2 = User(username="testuser", email="test2@example.com")
    db.add(user2)

    with pytest.raises(Exception):  # IntegrityError
        db.commit()


def test_user_unique_email(db: Session):
    """Test that emails must be unique."""
    user1 = User(username="user1", email="test@example.com")
    db.add(user1)
    db.commit()

    user2 = User(username="user2", email="test@example.com")
    db.add(user2)

    with pytest.raises(Exception):  # IntegrityError
        db.commit()


def test_todo_creation(db: Session):
    """Test creating a todo."""
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    todo = Todo(title="Test Todo", description="This is a test", user_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)

    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test"
    assert todo.completed is False
    assert todo.date_completed is None
    assert todo.created_at is not None
    assert todo.updated_at is not None


def test_todo_with_user_relationship(db: Session):
    """Test that a todo is linked to a user."""
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    todo = Todo(title="Test Todo", user_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)

    assert todo.user.username == "testuser"
    assert len(user.todos) == 1
    assert user.todos[0].title == "Test Todo"


def test_cascade_delete_user(db: Session):
    """Test that deleting a user cascades delete to todos."""
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    todo1 = Todo(title="Todo 1", user_id=user.id)
    todo2 = Todo(title="Todo 2", user_id=user.id)
    db.add_all([todo1, todo2])
    db.commit()

    # Verify todos exist
    todos_count = db.query(Todo).filter(Todo.user_id == user.id).count()
    assert todos_count == 2

    # Delete user
    db.delete(user)
    db.commit()

    # Verify todos are deleted
    todos_count = db.query(Todo).filter(Todo.user_id == user.id).count()
    assert todos_count == 0
