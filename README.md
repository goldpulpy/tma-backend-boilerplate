<div align="center">
  <h1>TMA Backend Boilerplate 🚀</h1>

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

A modern boilerplate for developing Telegram Mini Apps backend using FastAPI, SQLAlchemy, and architectural best practices.

## 🌟 Features

- **FastAPI** - Fast and modern web framework
- **SQLAlchemy** - Powerful ORM for database operations
- **Alembic** - Database migration management
- **Dependency Injector** - Dependency injection container
- **DDD approach** - Project structure based on Domain-Driven Design

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL (for local development)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/goldpulpy/tma-backend-boilerplate.git
cd tma-backend-boilerplate
```

2. **Setup environment**

```bash
make install
```

or

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment variables**

Create or copy `.env.example` to `.env` file in the project root:

```bash
# APP Env
ENVIRONMENT=development # or production
BOT_TOKEN=YOUR_BOT_TOKEN # from @BotFather
ALLOWED_ORIGIN=* # in production to set up your frontend.

# JWT Env
JWT_ALGORITHM=HS256
JWT_SECRET=YOUR_JWT_SECRET

# Postgres Env
DB_HOST=POSTGRES_HOST
DB_PORT=5432 # default
DB_USER=POSTGRES_USER
DB_PASSWORD=POSTGRES_PASSWORD
DB_NAME=POSTGRES_DATABASE_NAME
```

4. **Activate virtual environment**

```bash
source .venv/bin/activate
```

5. **Run migrations**

```bash
make migrate
```

6. **Start the application**

```bash
PYTHONPATH=src python -m backend
```

## 🛠️ Makefile Commands

| Command                             | Description                       |
| ----------------------------------- | --------------------------------- |
| `make venv`                         | Create virtual environment        |
| `make install`                      | Install dependencies              |
| `make create-migration m='Message'` | Create a new migration            |
| `make migrate`                      | Apply all pending migrations      |
| `make rollback-migration`           | Rollback the last migration       |
| `make db-reset`                     | Reset the database                |
| `make clean`                        | Clean the development environment |

## 📁 Project Structure

```
src/
├── alembic/                 # Database migrations
├── backend/
│   ├── app/                 # Application (API endpoints, routers)
│   ├── containers/          # DI containers
│   ├── domain/              # Business logic and domain models
│   └── infrastructure/      # External services (DB, API)
│       └── database/
│           ├── adapters/    # Repositories for DB operations
│           └── models/      # Database models
└── alembic.ini              # Alembic configuration
```

## 📝 Usage Examples

### Creating a New Endpoint

1. Create data models in `src/backend/infrastructure/database/models/`
2. Define services in `src/backend/domain/`
3. Add an endpoint in `src/backend/app/`

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.
