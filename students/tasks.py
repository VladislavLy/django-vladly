from datetime import datetime, timedelta

from celery import shared_task

from pytz import timezone

from .models import Logger


@shared_task
def delete_logs():
    logs_found = Logger.objects.filter(created__lte=datetime.now(timezone('UTC'))-timedelta(days=7)).all()

    if not logs_found:
        return 'Logs older than 7 days not found'
    else:
        logs_found.delete()
        return 'Logs older than 7 days deleted successfully!'
