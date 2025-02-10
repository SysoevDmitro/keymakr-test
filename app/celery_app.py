from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.autodiscover_tasks(['app'])


celery_app.conf.update(
    task_routes={
        'app.tasks.process_weather_task': {'queue': 'weather_queue'},
    }
)

celery_app.conf.broker_connection_retry_on_startup = True
