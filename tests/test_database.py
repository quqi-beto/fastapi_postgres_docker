from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

import pytest

from app.database import SessionLocal, Base


def test_database_connection():
    """Test that database connection works."""
    # Use SQLite for testing
    test_engine = create_engine("sqlite:///./test_connection.db")
    assert test_engine is not None


def test_session_creation():
    """Test that a database session can be created."""
    session = SessionLocal()
    assert session is not None
    session.close()


def test_tables_created():
    """Test that tables are created."""
    # Create a test engine with SQLite
    test_engine = create_engine("sqlite:///./test_tables.db")
    Base.metadata.create_all(bind=test_engine)

    # Check if tables exist
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()

    assert "users" in tables
    assert "todos" in tables

    # Cleanup
    Base.metadata.drop_all(bind=test_engine)
