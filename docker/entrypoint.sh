#!/bin/sh
set -e

# Apply database migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the API in the background
echo "Starting Arithmos API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait for API to be healthy before running tests
echo "Waiting for API healthcheck..."
until curl -s http://localhost:8000/health >/dev/null 2>&1; do
  sleep 1
done


# Wait for API process to exit (keep container running)
wait $API_PID