<div align="center">
  <h1>TMA Backend Boilerplate 🚀</h1>

![Telegram](https://img.shields.io/badge/Telegram-TMA-blue?logo=telegram)

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-316192.svg?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-ready-DC382D.svg?logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-ready-FF6600.svg?logo=rabbitmq&logoColor=white)

![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg?logo=github-actions&logoColor=white)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/goldpulpy/tma-backend-boilerplate/ruff.yaml?label=ruff)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/goldpulpy/tma-backend-boilerplate/pyright.yaml?label=pyright)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/goldpulpy/tma-backend-boilerplate/bandit.yaml?label=bandit)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/goldpulpy/tma-backend-boilerplate/docker.yaml?label=docker)

</div>

A modern, production-ready boilerplate for building Telegram Mini Apps backends with FastAPI. Features clean architecture, comprehensive authentication, and enterprise-grade patterns out of the box.

**What you get:**

- 🔐 **Secure by default** - JWT authentication, Telegram WebApp validation, rate limiting
- 🏗️ **Clean architecture** - DDD principles, dependency injection, unit of work pattern
- 🚀 **Developer-friendly** - Hot reload, type safety, automated migrations, pre-commit hooks
- 📦 **Production-ready** - Docker support, CI/CD with GitHub Actions, health checks
- 📚 **Well-documented** - Interactive API docs with Scalar, comprehensive README

Built with FastAPI, SQLAlchemy, and modern Python tooling to help you ship faster.

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
- **GitHub Actions** - 🚀 Continuous integration and deployment
- **Pre-commit** - 🔄 Automated code formatting and linting
- **uv** - 🐍 Python virtual environment manager

## 📋 Prerequisites

- 🐍 Python 3.12+ (venv)
- 🐳 Docker
- ⚙️ Make (used for convenient command execution during development)

## 🐳 Local Development Environment

This project includes a lightweight **docker-compose setup** for running PostgreSQL, Redis and RabbitMQ locally during development.

### 📁 Folder structure

```
docker/
├── postgres
├── redis
└── rabbitmq
```

<details>

<summary>🐘 PostgreSQL</summary>

#### ▶️ Run PostgreSQL container

From the project root, execute:

```bash
docker compose -f docker/postgres/docker-compose.yaml up -d
```

This will start a PostgreSQL container with the configured environment.

**Default configuration:**

- Port: `5432`
- User: `root`
- Password: `toor`
- Database: `db`

You can access the Adminer UI at [http://localhost:8080](http://localhost:8080)

Select the `PostgreSQL` database and log in with the provided credentials.

#### 🔧 Custom PostgreSQL Configuration

To use different credentials, modify `docker/postgres/docker-compose.yaml`:

- Update `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- Update corresponding values in `.env` file
- Restart container: `docker compose -f docker/postgres/docker-compose.yaml restart`

#### 🧹 Stop and remove PostgreSQL container

```bash
docker compose -f docker/postgres/docker-compose.yaml down

# or if you want to remove data

docker compose -f docker/postgres/docker-compose.yaml down --volumes
```

</details>

<details>

<summary>🔴 Redis (if needed)</summary>

#### ▶️ Run Redis container

From the project root, execute:

```bash
docker compose -f docker/redis/docker-compose.yaml up -d
```

This will start a Redis container with the configured environment.

**Default configuration:**

- Port: `6379`
- User: `default`
- Password: `toor`

#### 🔧 Custom Redis Configuration

To use different settings, modify `docker/redis/docker-compose.yaml`:

- Update `REDIS_PASSWORD` if authentication is needed or remove the line
- Update port mapping if necessary
- Update corresponding values in `.env` file
- Restart container: `docker compose -f docker/redis/docker-compose.yaml restart`

#### 🧪 Test Redis connection

You can test the connection using redis-cli:

```bash
docker exec -it redis redis-cli
AUTH toor # or your password
PING
```

Expected response: `PONG`

#### 🧹 Stop and remove Redis container

```bash
docker compose -f docker/redis/docker-compose.yaml down

# or if you want to remove data

docker compose -f docker/redis/docker-compose.yaml down --volumes
```

</details>

<details>

<summary>🐇 RabbitMQ (if needed)</summary>

#### ▶️ Run RabbitMQ container

From the project root, execute:

```bash
docker compose -f docker/rabbitmq/docker-compose.yaml up -d
```

This will start a RabbitMQ broker with the management UI.

**Default configuration:**

- AMQP Port: `5672`
- Management UI: [http://localhost:15672](http://localhost:15672)
- User: `root`
- Password: `toor`
- VHost: `/`

#### 🔧 Custom RabbitMQ Configuration

To use different credentials, modify `docker/rabbitmq/docker-compose.yaml`:

- Update `RABBITMQ_USER`, `RABBITMQ_PASS`, `RABBITMQ_VHOST`
- Update corresponding values in `.env` file
- Restart container: `docker compose -f docker/rabbitmq/docker-compose.yaml restart`

#### 🧪 Test RabbitMQ connection

You can use the built-in management UI:

[http://localhost:15672](http://localhost:15672)

Or connect from code using URI:

```bash
amqp://root:toor@localhost:5672/

```

#### 🧹 Stop and remove RabbitMQ container

```bash
docker compose -f docker/rabbitmq/docker-compose.yaml down

# or if you want to remove persisted message queues and data

docker compose -f docker/rabbitmq/docker-compose.yaml down --volumes
```

</details>

## 💻 Local Development

1. **Clone the repository**

```bash
git clone https://github.com/goldpulpy/tma-backend-boilerplate.git
cd tma-backend-boilerplate
```

2. **Create a virtual environment and install dependencies**

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

6. **Check health status**

```bash
curl -X GET http://localhost:5000/health
```

### 📝 Notes for local development

- Activate the virtual environment:

```bash
source .venv/bin/activate
```

- Load environment variables from the .env file:

```bash
export $(grep -v '^#' .env | xargs)
```

- Install package with `uv` (recommended):

```bash
uv add package_name
make requirements # for export to requirements.txt
```

> **Note:** `make requirements` is necessary for docker build and also for local development. This command updates the `requirements.txt` file with the latest dependencies.

## 🛠️ Makefile Commands

| Command                             | Description                                                  |
| ----------------------------------- | ------------------------------------------------------------ |
| `make install`                      | 📦 Create venv and install dependencies                      |
| `make requirements`                 | 📝 Export dependencies to requirements.txt                   |
| `make clean`                        | 🧹 Clean                                                     |
| `make run`                          | 🚀 Run the application                                       |
| `make create-migration m='Message'` | ➕ Create a new migration                                    |
| `make migrate`                      | 🔄 Apply all pending migrations                              |
| `make rollback-migration`           | ⏪ Rollback the last migration                               |
| `make db-reset`                     | 🗑️ Reset the database                                        |
| `make format`                       | ✨ Format code with ruff                                     |
| `make lint`                         | 🔍 Run ruff for code analysis                                |
| `make security`                     | 🚨 Run bandit for security analysis                          |
| `make type-check`                   | ✓ Run pyright for type checking                              |
| `make pre-commit`                   | 🔄 Run pre-commit checks (format, lint, security type-check) |

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
- **Bandit** - 🔒 Security checker

Run these tools using the commands listed in the Makefile Commands section.

## 🔄 Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality before committing changes. The pre-commit configuration automatically runs:

- **trailing-whitespace** - 🧹 Remove trailing whitespace
- **end-of-file-fixer** - 🧹 Ensure files end with a newline
- **check-yaml** - 🧹 Validate YAML files
- **check-added-large-files** - 🧹 Prevent large files from being committed
- **Ruff** - 🧹 For linting and formatting
- **pyright** - 🔍 For type checking
- **bandit** - 🔒 For security checks

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

<details>

<summary>Best Practices</summary>

### 🔒 Security

- Use strong `JWT_SECRET` (min 32 random characters)
- Set specific `ALLOWED_ORIGINS` (never use `*` in production)
- Enable **HTTPS** with valid SSL certificate
- Use environment variables for all secrets
- Never commit `.env` files to git
- Use non-root user in Docker containers
- Keep dependencies updated regularly
- Implement rate limiting (SlowAPI is already configured)
- Set up proper **CORS** policies
- Enable security headers in Nginx

### 📦 Database

- Use connection pooling
- Set up automated backups
- Enable database SSL connections
- Use read replicas for scaling (if needed)
- Monitor database performance
- Set appropriate connection limits
- Use **ACID** transactions

### 🚀 Infrastructure

- Implement **blue-green** or **rolling** deployments
- Implement **CI/CD** pipeline (GitHub Actions/GitLab CI)
- Use container registry (Docker Hub/ECR/GCR)
- Set up health checks for all services

</details>

## 🐛 Troubleshooting

<details>

<summary>Common Issues</summary>

**Problem:** `Port already in use`

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Problem:** `Migration conflicts`

```bash
make db-reset
make migrate
```

**Problem:** `Command not found: make`

```bash
# macOS: Install via Homebrew
brew install make
```

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install build-essential
```

</details>

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) file for more information. ⚖️

<div align="center">
  <p>Created with ❤️ by <a href="https://github.com/goldpulpy">goldpulpy</a> 👨‍💻</p>
</div>
