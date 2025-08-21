from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks.briefing_tasks", "app.tasks.scheduler"],
)

if __name__ == "__main__":
    celery_app.start()