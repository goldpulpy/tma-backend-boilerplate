#!/bin/sh
set -e

# Run migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Run the application
echo "Running the application..."
python -m backend