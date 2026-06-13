from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency to get database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
