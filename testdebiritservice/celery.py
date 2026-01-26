from celery import Celery

celery_app = Celery(
    "testdebiritservice",
    broker="redis://redis:6379/0",
)

from testdebiritservice.tasks.price_tasks import *  # noqa: E402, F403

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "testdebiritservice.tasks.price_tasks.fetch_prices",
        "schedule": 60.0,
    }
}

celery_app.conf.timezone = "UTC"
