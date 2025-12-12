from celery import Celery

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"]
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
