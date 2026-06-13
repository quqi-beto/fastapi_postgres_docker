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

## Project Structure

```
fastapi_postgres_sqlalchemy/
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
├── pyproject.toml              # Project metadata and dependencies
├── .env                        # Environment variables (production)
├── .env.test                   # Environment variables (testing)
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+ (for production)
- `uv` package manager

### Setup

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd fastapi_postgres_sqlalchemy
   ```

2. **Activate the virtual environment** (created by `uv init`)
   ```bash
   # On Windows
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

## Usage

### Run the API Server

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

To use this API in production with PostgreSQL:

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
