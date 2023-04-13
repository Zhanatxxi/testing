#!/bin/sh

alembic upgrade head

uvicorn src.project_name.main:app --proxy-headers --host 0.0.0.0 --port 8080 --workers 4