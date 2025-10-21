# Project configuration
SOURCE_DIR := src
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UV := $(VENV)/bin/uv
ENV_FILE := .env

# Colors for pretty output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default goal
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$(GREEN)Development Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)Environment Setup:$(NC)"
	@echo "  $(GREEN)install$(NC) - Create venv and install dependencies"
	@echo "  $(GREEN)requirements$(NC) - Export dependencies to requirements.txt"
	@echo "  $(GREEN)clean$(NC) - Clean development environment"
	@echo ""
	@echo "$(YELLOW)Application:$(NC)"
	@echo "  $(GREEN)run$(NC) - Run application"
	@echo ""
	@echo "$(YELLOW)Database:$(NC)"
	@echo "  $(GREEN)create-migration$(NC) - Create a new migration"
	@echo "  $(GREEN)migrate$(NC) - Apply all pending migrations"
	@echo "  $(GREEN)rollback-migration$(NC) - Rollback the last migration"
	@echo "  $(GREEN)migration-history$(NC) - Show migration history"
	@echo "  $(GREEN)db-current$(NC) - Show current database revision"
	@echo "  $(GREEN)db-reset$(NC) - Reset database"
	@echo ""
	@echo "$(YELLOW)Code Quality:$(NC)"
	@echo "  $(GREEN)format$(NC) - Format code (ruff)"
	@echo "  $(GREEN)lint$(NC) - Lint code (ruff)"
	@echo "  $(GREEN)type-check$(NC) - Type check code (pyright)"
	@echo "  $(GREEN)security$(NC) - Security check code (bandit)"
	@echo "  $(GREEN)pre-commit$(NC) - Run pre-commit checks (format, lint, security, type-check)"
	@echo ""

.PHONY: venv
venv:
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install uv
	@echo "$(GREEN)Virtual environment created successfully!$(NC)"

.PHONY: install
install: venv
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@$(UV) sync
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

.PHONY: requirements
requirements:
	@echo "$(YELLOW)Exporting dependencies to requirements.txt...$(NC)"
	@$(UV) export --no-dev --no-hashes > requirements.txt
	@echo "$(GREEN)Dependencies exported successfully!$(NC)"

.PHONY: run
run:
	@echo "$(YELLOW)Running application...$(NC)"
	@PYTHONPATH=src $(UV) run --env-file $(ENV_FILE) python -m backend

.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning development environment...$(NC)"
	@rm -rf $(VENV)
	@rm -rf $(ENV_FILE)
	@rm -rf .ruff_cache
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Development environment cleaned!$(NC)"


.PHONY: create-migration
create-migration:
	@if [ -z "$(m)" ]; then \
		echo "$(RED)Error: You must provide a migration message using m='message'$(NC)"; \
		echo "Example: make create-migration m='Add user table'"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Creating migration: $(m)$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini revision --autogenerate -m "$(m)"
	@echo "$(GREEN)Migration created successfully!$(NC)"

.PHONY: migrate
migrate:
	@echo "$(YELLOW)Applying migrations...$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini upgrade head
	@echo "$(GREEN)Migrations applied successfully!$(NC)"

.PHONY: rollback-migration
rollback-migration:
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini downgrade -1
	@echo "$(GREEN)Migration rolled back successfully!$(NC)"

.PHONY: migration-history
migration-history:
	@echo "$(YELLOW)Migration history:$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini history --verbose

.PHONY: db-current
db-current:
	@echo "$(YELLOW)Current database revision:$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini current

.PHONY: db-reset
db-reset:
	@echo "$(RED)WARNING: This will drop all database data!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "$(YELLOW)Resetting database...$(NC)"
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini downgrade base
	@PYTHONPATH=$(SOURCE_DIR) $(UV) run --env-file $(ENV_FILE) alembic -c $(SOURCE_DIR)/alembic.ini upgrade head
	@echo "$(GREEN)Database reset successfully!$(NC)"

.PHONY: format
format:
	@echo "$(YELLOW)Formatting code...$(NC)"
	@$(UV) run ruff format .
	@echo "$(GREEN)Code formatted successfully!$(NC)"

.PHONY: lint
lint:
	@echo "$(YELLOW)Linting code...$(NC)"
	@$(UV) run ruff check .
	@echo "$(GREEN)Code linted successfully!$(NC)"

.PHONY: type-check
type-check:
	@echo "$(YELLOW)Type checking code...$(NC)"
	@$(UV) run pyright .
	@echo "$(GREEN)Code type checked successfully!$(NC)"

.PHONY: security
security:
	@echo "$(YELLOW)Security checking code...$(NC)"
	@$(UV) run bandit -r $(SOURCE_DIR)
	@echo "$(GREEN)Code security checked successfully!$(NC)"

.PHONY: pre-commit
pre-commit: format lint security type-check
	@echo "$(GREEN)Pre-commit checks completed successfully!$(NC)"
