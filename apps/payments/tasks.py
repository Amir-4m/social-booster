from celery.task import periodic_task
from celery.schedules import crontab

from .services import CustomService


@periodic_task(run_every=crontab(minute='*/5'))
def update_gateways_cache():
    CustomService.update_gateways_cache()
