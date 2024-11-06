#!/bin/sh

Create migration
alembic upgrade head

celery -A src.core.apps.app_celery.celery_app worker --loglevel="${CELERY_LOG_LEVEL:-info}" --autoscale="${CELERY_MAX_WORKERS:-10}","${CELERY_MIN_WORKERS:-2}" &
# run API server
gunicorn --config /app/gunicorn_conf.py