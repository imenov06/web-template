#!/bin/sh
echo "Applying database migrations..."
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

