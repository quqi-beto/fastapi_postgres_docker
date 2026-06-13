# Todo API with FastAPI, PostgreSQL, and SQLAlchemy

A production-ready Todo API service built with FastAPI, PostgreSQL, and SQLAlchemy. Includes full CRUD operations for users and todos, comprehensive unit tests, and automated database table creation.

## Features

- **User Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Todo Management**: Full CRUD operations with status tracking
- **Relationships**: One-to-many relationship between users and todos (cascading delete)
- **Automatic Timestamps**: `created_at`, `updated_at`, and `date_completed` fields
- **Data Validation**: Pydantic schemas for request/response validation
- **Unit Tests**: 40 comprehensive tests covering models, schemas, and all endpoints
- **SQLAlchemy ORM**: Type-safe database operations with declarative models
- **FastAPI**: Modern async web framework with automatic API documentation (Swagger UI)
- **Docker Ready**: Pre-configured Docker Compose setup for development and production with PostgreSQL

## Project Structure

```
fastapi_postgres_docker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app and router registration
│   ├── config.py               # Configuration loader
│   ├── database.py             # SQLAlchemy setup
│   ├── models.py               # User and Todo ORM models
│   ├── schemas.py              # Pydantic request/response models
│   └── routes/
│       ├── __init__.py
│       ├── users.py            # User CRUD endpoints
│       └── todos.py            # Todo CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration and fixtures
│   ├── test_models.py          # Model unit tests
│   ├── test_schemas.py         # Schema validation tests
│   ├── test_database.py        # Database connection tests
│   └── test_routes/
│       ├── __init__.py
│       ├── test_users.py       # User endpoint tests
│       └── test_todos.py       # Todo endpoint tests
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Production Docker Compose config
├── docker-compose.override.yml # Development overrides (hot-reload)
├── .dockerignore               # Docker build context exclusions
├── pyproject.toml              # Project metadata and dependencies
├── .env                        # Environment variables (local dev)
├── .env.test                   # Environment variables (testing)
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+ (for local development without Docker)
- PostgreSQL 12+ (for local development without Docker)
- `uv` package manager (for local development without Docker)
- **Docker** & **Docker Compose** (for containerized development/production)

### Setup

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd fastapi_postgres_docker
   ```

2. **Create and Activate the virtual environment** (created by `uv init`)
   ```bash
   # On Windows
   uv venv
   uv sync
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Configure environment variables**
   
   Edit `.env` with your PostgreSQL connection string:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
   ```

4. **Create PostgreSQL database** (if needed)
   ```bash
   createdb todo_db
   ```

### Docker Setup

Run the entire stack (app + PostgreSQL) with a single command using Docker Compose.

1. **Start the application** (development mode with hot-reload):
   ```bash
   docker compose up
   ```
   This builds the image, starts PostgreSQL, and runs the API with live code reloading. The `docker-compose.override.yml` is applied automatically.

2. **Start in production mode** (no hot-reload, no volume mounts):
   ```bash
   docker compose -f docker-compose.yml up
   ```

3. **Stop the application**:
   ```bash
   docker compose down
   ```

4. **Stop and remove volumes** (wipes the database):
   ```bash
   docker compose down -v
   ```

5. **Rebuild the image** (after dependency changes):
   ```bash
   docker compose build
   ```

6. **View logs**:
   ```bash
   docker compose logs -f
   ```

The API will be available at `http://localhost:8000`
PostgreSQL is exposed on port `5432` (can be used with local tools like psql).
**pgAdmin** is available at `http://localhost:8080` (email: `admin@admin.com`, password: `secret`).

To connect pgAdmin to your PostgreSQL database:

1. Log in at `http://localhost:8080`
2. Right-click **Servers** → **Register** → **Server**
3. On the **General** tab, give it a name (e.g. `Todo DB`)
4. On the **Connection** tab, enter:
   - **Host name/address**: `db` (the Docker service name — not `localhost` or `127.0.0.1`)
   - **Port**: `5432`
   - **Maintenance database**: `todo_db`
   - **Username**: `user`
   - **Password**: `password`
5. Click **Save**

You should now see the `todos` and `users` tables under **Databases** → **todo_db** → **Schemas** → **public** → **Tables**.

> **Note**: When running via Docker, the `DATABASE_URL` is set automatically in `docker-compose.yml` to `postgresql://user:password@db:5432/todo_db` (where `db` is the PostgreSQL container). Your local `.env` file remains untouched and is only used for local (non-Docker) development.

## Usage

### Run the API Server

#### Option 1: Docker (recommended)

```bash
docker compose up
```

#### Option 2: Local development (without Docker)

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**API Documentation**: 
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Run Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=app

# Run specific test file
uv run pytest tests/test_routes/test_users.py -v
```

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | Get all users |
| `GET` | `/users/{user_id}` | Get a specific user |
| `PUT` | `/users/{user_id}` | Update a user |
| `DELETE` | `/users/{user_id}` | Delete a user (cascades to todos) |

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/todos/` | Create a new todo |
| `GET` | `/todos/` | Get all todos |
| `GET` | `/todos/{todo_id}` | Get a specific todo |
| `PUT` | `/todos/{todo_id}` | Update a todo |
| `DELETE` | `/todos/{todo_id}` | Delete a todo |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status message |
| `GET` | `/health` | Health check |

## Request/Response Examples

### Create User

**Request:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com"}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2026-06-11T10:30:00"
}
```

### Create Todo

**Request:**
```bash
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "user_id": 1}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "user_id": 1,
  "completed": false,
  "created_at": "2026-06-11T10:30:00",
  "updated_at": "2026-06-11T10:30:00",
  "date_completed": null
}
```

### Mark Todo as Completed

**Request:**
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "user_id": 1,
  "completed": true,
  "created_at": "2026-06-11T10:30:00",
  "updated_at": "2026-06-11T10:31:00",
  "date_completed": "2026-06-11T10:31:00"
}
```

## Database Schema

Tables are **auto-created on application startup** via `Base.metadata.create_all()` in `app/main.py`. This reads the SQLAlchemy models and creates any missing tables — no manual migration or schema setup needed. The PostgreSQL data persists across restarts thanks to the Docker named volume (`postgres_data`).

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY |
| `username` | VARCHAR(255) | UNIQUE, NOT NULL |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW() |

### Todos Table

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY |
| `title` | VARCHAR(255) | NOT NULL |
| `description` | VARCHAR(500) | NULLABLE |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW() |
| `updated_at` | DATETIME | NOT NULL, DEFAULT NOW() |
| `date_completed` | DATETIME | NULLABLE |
| `user_id` | INTEGER | FOREIGN KEY (users.id), CASCADE DELETE |

## Testing

The project includes 40 comprehensive unit tests:

- **3 Database tests**: Connection, session creation, table verification
- **6 Model tests**: User/Todo creation, uniqueness, relationships, cascade delete
- **8 Schema tests**: Pydantic validation for UserCreate, UserUpdate, UserResponse, TodoCreate, TodoUpdate, TodoResponse
- **11 User endpoint tests**: CRUD operations, error handling
- **12 Todo endpoint tests**: CRUD operations, status updates, cascading deletes

Tests use SQLite in-memory database to avoid PostgreSQL dependency during testing.

## Features Implemented

✅ User full CRUD (Create, Read all, Read one, Update, Delete)  
✅ Todo full CRUD (Create, Read all, Read one, Update, Delete)  
✅ User-Todo one-to-many relationship with cascading delete  
✅ Automatic timestamp tracking (created_at, updated_at)  
✅ Completion date tracking (date_completed auto-set when todo marked complete)  
✅ Data validation with Pydantic schemas  
✅ Error handling with appropriate HTTP status codes  
✅ SQLAlchemy ORM with declarative models  
✅ FastAPI async web framework  
✅ 40 comprehensive unit tests (100% pass rate)  
✅ Database auto-creation on app startup  
✅ Swagger UI documentation at `/docs`  

## Future Enhancements

- [x] ~~User authentication (JWT tokens)~~ (planned for separate project)
- [x] ~~Pagination for large result sets~~ (planned for future version)
- [ ] User profile information (name, bio, avatar)
- [ ] Todo categories/tags
- [ ] Todo priority levels
- [ ] Todo due dates with reminders
- [ ] Shared todos (collaboration)
- [ ] Todo comments/notes
- [ ] Database migrations with Alembic
- [ ] Rate limiting and request throttling
- [ ] API versioning

## Dependencies

### Core Dependencies

- **fastapi** (0.136.3): Modern async web framework
- **uvicorn** (0.49.0): ASGI server
- **sqlalchemy** (2.0.50): SQL toolkit and ORM
- **psycopg2-binary** (2.9.12): PostgreSQL adapter
- **pydantic** (2.13.4): Data validation using Python type annotations
- **python-dotenv** (1.2.2): Load environment variables from .env

### Development Dependencies

- **pytest** (9.0.3): Testing framework
- **pytest-asyncio** (1.4.0): Async test support
- **httpx** (0.28.1): HTTP client for testing

## Configuration

### Environment Variables

`.env` (Production):
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

`.env.test` (Testing - uses SQLite automatically):
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db_test
```

The test configuration automatically uses SQLite to avoid PostgreSQL dependency during testing.

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request data (e.g., duplicate username)
- `404 Not Found`: Resource does not exist
- `500 Internal Server Error`: Server error

## Performance Notes

- **Database Indexes**: Usernames and emails are indexed for faster lookups
- **Foreign Keys**: Cascading delete ensures data integrity
- **Connection Pooling**: SQLAlchemy manages connection pooling automatically
- **Async Support**: FastAPI is fully async for concurrent request handling

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Implement the feature
3. Verify all tests pass: `uv run pytest tests/ -v`
4. Update documentation

## License

MIT License - feel free to use this project as a template or reference.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

## Next Steps

### Run with Docker (recommended for production)

```bash
docker compose -f docker-compose.yml up -d
```

This starts PostgreSQL and the API in the background. Access Swagger UI at `http://localhost:8000/docs`.

### Run locally without Docker

1. **Install PostgreSQL** and create a database
2. **Update `.env`** with your PostgreSQL credentials
3. **Run the server**: `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. **Access Swagger UI** at `http://your-server:8000/docs`

To add authentication (JWT tokens) for a future project:
- Extend `UserResponse` schema with password field
- Add login endpoint (`POST /login`)
- Add JWT token generation and validation
- Protect endpoints with Bearer token authentication
- See `notes/authentication.md` for implementation details (when created)

---

**Created**: June 11, 2026  
**Version**: 1.0.0  
**Status**: Production Ready (without authentication)
