"""
Celery worker configuration
"""

from celery import Celery
from src.config.settings import settings

celery_app = Celery(
    'agentice',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task
def daily_job_search():
    """Daily job search task"""
    from src.pipelines.job_application_pipeline import run_daily_job_search_for_all_users
    import asyncio
    asyncio.run(run_daily_job_search_for_all_users())


# Schedule daily task
celery_app.conf.beat_schedule = {
    'daily-job-search': {
        'task': 'src.worker.celery_app.daily_job_search',
        'schedule': 86400.0,  # Run daily (24 hours)
    },
}
