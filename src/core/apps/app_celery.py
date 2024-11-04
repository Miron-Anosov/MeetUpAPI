"""Main Celery application."""

from celery import Celery
from kombu import Connection

from src.core.settings.env import settings


def create_celery_app():
    """Create Celery."""
    celery = Celery(
        main="tasks",
        broker=settings.redis.redis_url_broker,
        backend=settings.redis.redis_url_backend,
    )

    celery.conf.update(
        broker_connection_retry=True,
        broker_connection_retry_on_startup=True,
        broker_connection_max_retries=100,
        broker_connection_timeout=30,
        worker_concurrency=4,
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=100,
        task_time_limit=3600,
        task_soft_time_limit=3540,
    )

    celery.autodiscover_tasks(["src.core.apps.tasks"], force=True)

    return celery


celery_app = create_celery_app()


def check_redis_connection():
    """Check if Redis is available."""
    try:
        conn = Connection(celery_app.conf.broker_url)
        conn.ensure_connection(max_retries=3)
        conn.release()
        print("Successfully connected to Redis from Celery!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e} for Celery!")
        raise
