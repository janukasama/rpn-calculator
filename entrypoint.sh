#!/bin/bash
# Entrypoint script to launch the FastAPI app

# Exit on any error
set -e

# upgrade the db (only for this task, we can separate this into another service if there will be replicas)
alembic upgrade head

# Run the FastAPI app using uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000