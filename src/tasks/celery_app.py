from celery import Celery
from src.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.the_tasks"
        ],
    

)

celery_instance.conf.beat_schedule = {
    "anywhere-name": {
        "task": "bookings_today_check_in",
        "schedule": 5,
    }
}