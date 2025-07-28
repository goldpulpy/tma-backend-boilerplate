# Project configuration
SOURCE_DIR := src
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

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
	@echo "  $(GREEN)venv$(NC) - Create virtual environment"
	@echo "  $(GREEN)install$(NC) - Install dependencies"
	@echo "  $(GREEN)clean$(NC) - Clean development environment"
	@echo ""
	@echo "$(YELLOW)Database:$(NC)"
	@echo "  $(GREEN)create-migration$(NC) - Create a new migration"
	@echo "  $(GREEN)migrate$(NC) - Apply all pending migrations"
	@echo "  $(GREEN)rollback-migration$(NC) - Rollback the last migration"
	@echo "  $(GREEN)migration-history$(NC) - Show migration history"
	@echo "  $(GREEN)db-current$(NC) - Show current database revision"
	@echo "  $(GREEN)db-reset$(NC) - Reset database"
	@echo ""

# Environment Setup
.PHONY: venv
venv:
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	@python3 -m venv $(VENV)
	@echo "$(GREEN)Virtual environment created successfully!$(NC)"

.PHONY: install
install: venv
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

# Database Operations
.PHONY: create-migration
create-migration:
	@if [ -z "$(m)" ]; then \
		echo "$(RED)Error: You must provide a migration message using m='message'$(NC)"; \
		echo "Example: make create-migration m='Add user table'"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Creating migration: $(m)$(NC)"
	@cd $(SOURCE_DIR) && alembic revision --autogenerate -m "$(m)"
	@echo "$(GREEN)Migration created successfully!$(NC)"

.PHONY: migrate
migrate:
	@echo "$(YELLOW)Applying migrations...$(NC)"
	@cd $(SOURCE_DIR) && alembic upgrade head
	@echo "$(GREEN)Migrations applied successfully!$(NC)"

.PHONY: rollback-migration
rollback-migration:
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	@cd $(SOURCE_DIR) && alembic downgrade -1
	@echo "$(GREEN)Migration rolled back successfully!$(NC)"

.PHONY: migration-history
migration-history:
	@echo "$(YELLOW)Migration history:$(NC)"
	@cd $(SOURCE_DIR) && alembic history --verbose

.PHONY: db-current
db-current:
	@echo "$(YELLOW)Current database revision:$(NC)"
	@cd $(SOURCE_DIR) && alembic current

.PHONY: db-reset
db-reset:
	@echo "$(RED)WARNING: This will drop all database data!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "$(YELLOW)Resetting database...$(NC)"
	@cd $(SOURCE_DIR) && alembic downgrade base
	@cd $(SOURCE_DIR) && alembic upgrade head
	@echo "$(GREEN)Database reset successfully!$(NC)"

# Cleanup
.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning development environment...$(NC)"
	@rm -rf $(VENV)
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Development environment cleaned!$(NC)"