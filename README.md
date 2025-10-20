<div align="center">
  <h1>TMA Backend Boilerplate 🚀</h1>

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

A modern boilerplate for developing Telegram Mini Apps backend using FastAPI, SQLAlchemy, and architectural best practices. This template provides a complete foundation with authentication, database integration, DDD architecture, and secure API design patterns to quickly build production-ready Telegram Mini App backends. ✨

## 🌟 Features

- **FastAPI** - ⚡ Fast and modern web framework
- **SQLAlchemy** - 🗃️ Powerful ORM for database operations
- **Alembic** - 🔄 Database migration management
- **Dependency Injector** - 💉 Dependency injection container
- **DDD approach** - 🏗️ Project structure based on Domain-Driven Design
- **Scalar** - 📚 API reference generator
- **SlowAPI** - 🛡️ Rate limiting for API endpoints
- **JWT** - 🔒 JSON Web Token for authentication
- **Unit of Work** - 🔄 Unit of Work pattern for database transactions
- **Docker** - 🐳 Containerization for easy deployment

## 📋 Prerequisites

- 🐍 Python 3.12+ (venv)
- 🐳 Docker
- ⚙️ Make (used for convenient command execution during development)

## 🚀 Quick Start

## 🐳 PostgreSQL (Docker)

This project includes a lightweight **docker-compose setup** for running PostgreSQL locally during development.

### 📁 Folder structure

```
docker/
└── postgres/
    └── docker-compose.yml
```

### ▶️ Run PostgreSQL container

From the project root, execute:

```bash
docker compose -f docker/postgres/docker-compose.yml up -d
```

This will start a PostgreSQL container with the configured environment.
By default:

- Port: `5432`
- User: `root`
- Password: `toor`
- Database: `db`

#### 🔎 Adminer UI

You can access the Adminer UI at [http://localhost:8080](http://localhost:8080)

Select the `PostgreSQL` database and log in with the provided credentials.

### 🔧 Custom PostgreSQL Configuration

To use different credentials, modify `docker/postgres/docker-compose.yml`:

- Update POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
- Update corresponding values in .env file
- Restart container: `docker compose -f docker/postgres/docker-compose.yml restart`

### 🧹 Stop and remove container

```bash
docker compose -f docker/postgres/docker-compose.yml down
```

with volumes:

```bash
docker compose -f docker/postgres/docker-compose.yml down --volumes
```

### 💻 Local Development

1. **Clone the repository**

```bash
git clone https://github.com/goldpulpy/tma-backend-boilerplate.git
cd tma-backend-boilerplate
```

2. **Setup environment**

```bash
make install
```

3. **Configure environment variables**

Create or copy `.env.example` to `.env` file in the project root:

```bash
# APP Env
HOST=0.0.0.0 # Optional, default is 0.0.0.0
PORT=5000 # Optional, default is 5000
ALLOWED_ORIGINS=* # in production to set up your frontends.
ENVIRONMENT=development # or production
BOT_TOKEN=YOUR_BOT_TOKEN # from @BotFather

# JWT Env
JWT_ALGORITHM=HS256 # Optional, default is "HS256"
JWT_ISSUER=YOUR_ISSUER_VALUE # Optional, default is "backend"
JWT_EXPIRY_DAYS=1 # Optional, default is 1
JWT_SECRET=YOUR_JWT_SECRET # min 32 characters

# Postgres Env
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=5432 # Optional, default is 5432
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_DB=POSTGRES_DATABASE_NAME
```

**Environment mode:**

- `development` - the application will run in development mode for local development
- `production` - the application will run in production mode

**Allowed origins:**

- `*` - allow all origins (not recommended for production)
- `http://localhost:3000` - allow only localhost:3000 (for local development)
- `https://your-frontend.com` - allow only your-frontend.com (for production)
- `https://your-frontend.com,http://localhost:3000` - allow only your-frontend.com and localhost:3000 (comma-separated list)

4. **Run migrations**

```bash
make migrate
```

5. **Start the application**

```bash
make run
```

#### 📝 Notes for local development

- Activate the virtual environment:

```bash
source .venv/bin/activate
```

- Load environment variables from the .env file:

```bash
export $(grep -v '^#' .env | xargs)
```

## 🛠️ Makefile Commands

| Command                             | Description                                         |
| ----------------------------------- | --------------------------------------------------- |
| `make venv`                         | 🔧 Create virtual environment                       |
| `make install`                      | 📦 Install dependencies                             |
| `make clean`                        | 🧹 Clean the development environment                |
| `make run`                          | 🚀 Run the application                              |
| `make create-migration m='Message'` | ➕ Create a new migration                           |
| `make migrate`                      | 🔄 Apply all pending migrations                     |
| `make rollback-migration`           | ⏪ Rollback the last migration                      |
| `make db-reset`                     | 🗑️ Reset the database                               |
| `make lint`                         | 🔍 Run ruff for code analysis                       |
| `make type-check`                   | ✓ Run pyright for type checking                     |
| `make format`                       | ✨ Format code with ruff                            |
| `make pre-commit`                   | 🔄 Run pre-commit checks (format, lint, type-check) |

## 📄 Base points

### 🔄 Service endpoints

- GET `/health` - health check endpoint
- GET `/docs` - API reference documentation (only in development mode)

### 🔒 Authentication

- POST `/api/v1/auth/telegram` - authenticate via Telegram Mini App init_data

**Authentication Flow:**

1. Client sends `init_data` from Telegram WebApp
2. Server validates and returns JWT token as httpOnly cookie
3. All subsequent API requests will automatically include the JWT token cookie
4. The server verifies the token and provides access to protected resources

**Note:** The `init_data` may be used as a refresh token.

#### ⛔ Excluding Routes from Authentication

If you want to define routes that do not require authentication, add them to the `AUTH_EXCLUDE_PATHS` constant located in:

```bash
src/backend/presentation/api/middlewares/authentication.py
```

**Example:**

```python
AUTH_EXCLUDE_PATHS: ClassVar[set[str]] = {
    "/api/v1/auth/telegram",
    "/health",
    "/docs",
    "/openapi.json",
    "/your/public/route",  # ← Add your route here
}
```

Any route listed here will bypass JWT authentication as well as all of its subpaths (e.g. `/your/public/route`, `/your/public/route/foo`, `/your/public/route/bar/123`, etc.).

#### 👤 Accessing User Data

Once a user is authenticated, you can access their user ID from the request state.

<details>
<summary>Example</summary>

```python
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from backend.shared.validators.fastapi import (
    UserIdNotFoundInStateError,
    get_user_id_from_state,
)

@router.get("/your/protected/route")
async def your_protected_route(request: Request) -> JSONResponse:
    try:

        user_id = get_user_id_from_state(request)  # int or raise UserIdNotFoundInStateError
        return JSONResponse(content={"user_id": user_id})

    except UserIdNotFoundInStateError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from e
```

</details>

also you can see the example in the `src/backend/presentation/api/v1/user/me.py` file.

### 🔄 User endpoints

- GET `/api/v1/user/me` - get current user profile (protected route)

## 📁 Project Structure

```
src/
├── alembic/                 # Database migrations
├── backend/
│   ├── domain/              # Domain layer
│   │   ├── entities/        # Entities
│   │   ├── constants/       # Constants
│   │   ├── exceptions/      # Exceptions
│   │   ├── repositories/    # Repositories interface
│   │   └── value_objects/   # Value objects
│   ├── application/         # Application layer (API endpoints, routers)
│   │   ├── dtos/            # Data Transfer Objects
│   │   ├── services/        # Services interface
│   │   └── use_cases/       # Use cases
│   ├── presentation/        # Presentation layer (API endpoints, routers)
│   │   └── api/             # API endpoints, routers (v1)
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── database/        # Database models
│   │   ├── repositories/    # Repositories implementation
│   │   └── services/        # Services implementation
│   ├── containers/          # Dependency Injection containers
│   └── shared/              # Shared resources (config, slowapi, jwt, etc.)
└── alembic.ini              # Alembic configuration
```

## 🧪 Code Quality Tools

The project uses several tools to ensure code quality:

- **Ruff** - 🧹 Code formatter that enforces a consistent style and linting
- **Pyright** - 🔍 Static type checker for Python

Run these tools using the commands listed in the Makefile Commands section.

## 🔄 Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality before committing changes. The pre-commit configuration automatically runs:

- **Ruff** - 🧹 For linting and formatting
- **pyright** - 🔍 For type checking

### 🔧 Installation

To install the pre-commit hooks:

**Note:** You need to have the virtual environment activated.

```bash
pre-commit install
```

After installation, the hooks will automatically run on every commit. If any issues are found, the commit will be blocked until they're fixed.

You can manually run all pre-commit hooks on all files with:

```bash
pre-commit run --all-files
```

**Note:** The `make pre-commit` command runs similar checks but doesn't integrate with git hooks.

## 🔒 Production Best Practices

### Security

- Use strong JWT_SECRET (min 32 random characters)
- Set specific ALLOWED_ORIGINS (never use `*` in production)
- Enable HTTPS with valid SSL certificate
- Use environment variables for all secrets
- Never commit `.env` files to git
- Use non-root user in Docker containers
- Keep dependencies updated regularly
- Implement rate limiting (SlowAPI is already configured)
- Set up proper CORS policies
- Enable security headers in Nginx

### Database

- Use connection pooling
- Set up automated backups
- Enable database SSL connections
- Use read replicas for scaling (if needed)
- Monitor database performance
- Set appropriate connection limits

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) file for more information. ⚖️

<div align="center">
  <p>Created with ❤️ by <a href="https://github.com/goldpulpy">goldpulpy</a> 👨‍💻</p>
</div>
