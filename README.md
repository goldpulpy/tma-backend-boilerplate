<div align="center">
  <h1>TMA Backend Boilerplate 🚀</h1>

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

A modern boilerplate for developing Telegram Mini Apps backend using FastAPI, SQLAlchemy, and architectural best practices. ✨

## 🌟 Features

- **FastAPI** - ⚡ Fast and modern web framework
- **SQLAlchemy** - 🗃️ Powerful ORM for database operations
- **Alembic** - 🔄 Database migration management
- **Dependency Injector** - 💉 Dependency injection container
- **DDD approach** - 🏗️ Project structure based on Domain-Driven Design
- **Scalar** - 📚 API reference generator
- **SlowAPI** - 🛡️ Rate limiting for API endpoints

## 📋 Prerequisites

- 🐍 Python 3.12+
- 🐘 PostgreSQL
- ⚙️ Make (used for convenient command execution during development)

## 🚀 Quick Start

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
HOST=0.0.0.0 # default
PORT=5000 # default
ALLOWED_ORIGINS=["*"] # in production to set up your frontend.
ENVIRONMENT=development # or production
BOT_TOKEN=YOUR_BOT_TOKEN # from @BotFather

# JWT Env
JWT_ALGORITHM=HS256
JWT_SECRET=YOUR_JWT_SECRET # min 32 characters

# Postgres Env
DB_HOST=POSTGRES_HOST
DB_PORT=5432 # default
DB_USER=POSTGRES_USER
DB_PASSWORD=POSTGRES_PASSWORD
DB_NAME=POSTGRES_DATABASE_NAME
```

4. **Activate virtual environment**

**Note:** You need to have the virtual environment activated.

```bash
source .venv/bin/activate
```

5. **Run migrations**

```bash
make migrate
```

6. **Start the application**

```bash
make run
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

## 📄 Base points

- `/health` - health check endpoint
- `/docs` - API reference documentation (only in development mode)

## 📁 Project Structure

```
src/
├── alembic/                 # Database migrations
├── backend/
│   ├── domain/              # Domain layer
│   │   ├── entities/        # Entities
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
│   └── shared/              # Shared resources (config, logger, slowapi, etc.)
└── alembic.ini              # Alembic configuration
```

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) file for more information. ⚖️

<div align="center">
  <p>Created with ❤️ by <a href="https://github.com/goldpulpy">goldpulpy</a> 👨‍💻</p>
</div>
