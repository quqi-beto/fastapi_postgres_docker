from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import todos, users


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle events."""
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create database tables on startup: {e}")
        print("Make sure PostgreSQL is running and accessible.")
    
    yield
    
    # Shutdown (if needed)
    pass


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    description="A simple Todo API with user management",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(users.router)
app.include_router(todos.router)


@app.get("/", tags=["health"])
def root():
    """Health check endpoint."""
    return {"message": "Todo API is running"}


@app.get("/health", tags=["health"])
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
